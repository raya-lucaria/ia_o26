# §5 · Entrenar un LoRA r = P["rango"]: precomputar latents y embeddings
# (uno por caption distinto), ruido fijo de validation, AdamW + cosine con
# warmup, curvas. Define LATENTS, EMBS, CAP, RUIDO, RUIDO_VAL, perdida,
# PERDIDAS_TRAIN, PERDIDAS_VAL y N_ENTRENABLES. El adaptador vive en UNET.

# %% [texto] s05-intro

# %% [codigo] s05-precomputar
import time

import torch.nn.functional as F
from diffusers import DDPMScheduler

ESCALA_VAE = PIPE.vae.config.scaling_factor      # 0.18215 en SD 1.5


def a_tensor(imgs):
    """Lista de PIL → tensor (N, 3, H, W) en [-1, 1], como lo espera el VAE."""
    x = torch.stack([torch.from_numpy(np.array(im)) for im in imgs])
    return x.permute(0, 3, 1, 2).float().div(127.5).sub(1)


@torch.no_grad()
def codificar(imgs, lote=8):
    """Latents x_0 = escala · media del VAE, por lotes, guardados en CPU."""
    salida = []
    for i in range(0, len(imgs), lote):
        x = a_tensor(imgs[i:i + lote]).to(DEVICE, DTYPE)
        z = PIPE.vae.encode(x).latent_dist.mode()  # la media: determinista
        salida.append((z * ESCALA_VAE).float().cpu())
    return torch.cat(salida)


LATENTS = {k: codificar(v) for k, v in IMGS.items()}

# Un embedding por caption DISTINTO; CAP[k][i] dice cuál le toca a la imagen i.
CAPTIONS = sorted({t for v in TEXTOS.values() for t in v})
INDICE = {t: i for i, t in enumerate(CAPTIONS)}
CAP = {k: torch.tensor([INDICE[t] for t in v]) for k, v in TEXTOS.items()}
tok = PIPE.tokenizer
with torch.no_grad():
    lotes = []
    for i in range(0, len(CAPTIONS), 32):
        ids = tok(CAPTIONS[i:i + 32], padding="max_length", truncation=True,
                  max_length=tok.model_max_length, return_tensors="pt")
        lotes.append(PIPE.text_encoder(ids.input_ids.to(DEVICE))[0])
    EMBS = torch.cat(lotes).to(DTYPE)            # (captions, 77, D)
largos = sum(len(tok(t).input_ids) > tok.model_max_length for t in CAPTIONS)

for k, z in LATENTS.items():
    print(f"LATENTS[{k!r}]: {tuple(z.shape)}")
print(f"EMBS: {tuple(EMBS.shape)} · {len(CAPTIONS)} captions distintos")
if largos:
    print(f"Ojo: {largos} captions pasan de {tok.model_max_length} tokens; "
          "CLIP solo lee el principio.")

# %% [texto] s05-ruido-explica

# %% [codigo] s05-ruido
RUIDO = DDPMScheduler.from_pretrained(MODELO, subfolder="scheduler")
T = RUIDO.config.num_train_timesteps
gen = torch.Generator().manual_seed(0)
RUIDO_VAL = (torch.linspace(0, T - 1, P["n_val_ruido"]).round().long(),
             torch.randn((P["n_val_ruido"], *LATENTS["train"].shape[1:]),
                         generator=gen))


@torch.no_grad()
def perdida(conjunto, lora=True):
    """MSE del ruido en `conjunto` con (t, ε) FIJOS: la evaluación i usa la
    imagen i mod N y el par i mod K. Dos mediciones usan la misma vara."""
    usar_lora(lora)
    X, C = LATENTS[conjunto], CAP[conjunto]
    t_fijo, eps_fijo = RUIDO_VAL
    n, k = len(X), len(t_fijo)
    estaba = UNET.training
    UNET.eval()
    total, cuenta = 0.0, 0
    for lote in torch.arange(max(n, k)).split(2 * P["batch"]):
        x0 = X[lote % n].to(DEVICE, DTYPE)
        eps = eps_fijo[lote % k].to(DEVICE, DTYPE)
        t = t_fijo[lote % k].to(DEVICE)
        xt = RUIDO.add_noise(x0, eps, t)
        with torch.autocast("cuda", dtype=torch.float16, enabled=CUDA):
            pred = UNET(xt, t, encoder_hidden_states=EMBS[C[lote % n]]).sample
        total += F.mse_loss(pred.float(), eps.float(), reduction="sum").item()
        cuenta += eps.numel()
    UNET.train(estaba)
    return total / cuenta


print("t fijos de validation:", RUIDO_VAL[0].tolist())
print(f"loss de validation del base: {perdida('validation', lora=False):.4f}")

# %% [texto] s05-entrenar-explica

# %% [codigo] s05-preparar
from diffusers.optimization import get_scheduler
from diffusers.training_utils import cast_training_params
from peft import LoraConfig

if tiene_lora():                      # si vuelves a correr esta celda
    UNET.delete_adapters("default")
semilla(0)
UNET.add_adapter(LoraConfig(r=P["rango"], lora_alpha=P["rango"],
                            init_lora_weights="gaussian",
                            target_modules=list(MODULOS)))
# A y B en fp32 sobre el UNet fp16: GradScaler no desescala gradientes fp16.
cast_training_params(UNET, dtype=torch.float32)
UNET.enable_gradient_checkpointing()  # menos memoria, un poco más de tiempo
ENTRENABLES = [p for p in UNET.parameters() if p.requires_grad]
N_ENTRENABLES = sum(p.numel() for p in ENTRENABLES)
print(f"parámetros entrenables: {N_ENTRENABLES:,} (la cuenta de la sección 04"
      f" dio {N_LORA:,})")
OPT = torch.optim.AdamW(ENTRENABLES, lr=P["lr"], weight_decay=1e-2)
WARMUP = max(1, round(0.05 * P["pasos"]))
SCHED = get_scheduler("cosine", OPT, num_warmup_steps=WARMUP,
                      num_training_steps=P["pasos"])
ESCALADOR = torch.amp.GradScaler("cuda", enabled=CUDA)
print(f"AdamW lr={P['lr']} · warmup {WARMUP} pasos · cosine hasta "
      f"{P['pasos']} · batch {P['batch']}")

# %% [codigo] s05-entrenar
def un_paso(g):
    """Un paso de difusión sobre un batch de train. Devuelve la loss, o
    None si GradScaler encontró inf/NaN y saltó el paso."""
    X, C = LATENTS["train"], CAP["train"]
    i = torch.randint(len(X), (P["batch"],), generator=g)
    x0 = X[i].to(DEVICE, DTYPE)
    eps = torch.randn(x0.shape, generator=g).to(DEVICE, DTYPE)
    t = torch.randint(0, T, (len(i),), generator=g).to(DEVICE)
    xt = RUIDO.add_noise(x0, eps, t)                   # ensuciar: forward
    with torch.autocast("cuda", dtype=torch.float16, enabled=CUDA):
        pred = UNET(xt, t, encoder_hidden_states=EMBS[C[i]]).sample
    loss = F.mse_loss(pred.float(), eps.float())       # ‖ε − ε̂‖² promedio
    OPT.zero_grad(set_to_none=True)
    ESCALADOR.scale(loss).backward()                   # solo llega a A y B
    ESCALADOR.unscale_(OPT)
    torch.nn.utils.clip_grad_norm_(ENTRENABLES, 1.0)
    escala_previa = ESCALADOR.get_scale()
    ESCALADOR.step(OPT)
    ESCALADOR.update()
    if ESCALADOR.get_scale() < escala_previa:          # inf/NaN: no cuenta
        return None
    SCHED.step()
    return loss.item()


# El punto del paso 0 es el modelo base: B = 0 ⇒ ΔW = 0.
PERDIDAS_TRAIN, PERDIDAS_VAL = [], [(0, perdida("validation"))]
g = torch.Generator().manual_seed(0)
paso, intentos, inicio = 0, 0, time.perf_counter()
usar_lora(True)
UNET.train()
while paso < P["pasos"] and intentos < 2 * P["pasos"]:
    intentos += 1
    loss = un_paso(g)
    if loss is None:
        continue
    paso += 1
    PERDIDAS_TRAIN.append((paso, loss))
    if paso == min(10, P["pasos"]):
        seg = (time.perf_counter() - inicio) / paso
        print(f"{seg:.2f} s/paso → el entrenamiento tardará ≈ "
              f"{seg * P['pasos'] / 60:.1f} min")
    if paso % P["val_cada"] == 0 or paso == P["pasos"]:
        PERDIDAS_VAL.append((paso, perdida("validation")))
        UNET.train()
        print(f"paso {paso:5d} · loss de validation {PERDIDAS_VAL[-1][1]:.4f}")
UNET.eval()
UNET.disable_gradient_checkpointing()
del OPT, SCHED                        # suelta los momentos de AdamW
gc.collect()
if CUDA:
    torch.cuda.empty_cache()
print(f"listo: {paso} pasos en {(time.perf_counter() - inicio) / 60:.1f} min")

# %% [texto] s05-curvas-explica

# %% [codigo] s05-curvas
pasos_tr, loss_tr = map(np.array, zip(*PERDIDAS_TRAIN))
ventana = max(1, min(25, len(loss_tr) // 5))
media = np.convolve(loss_tr, np.ones(ventana) / ventana, mode="valid")
fig, eje = plt.subplots(figsize=(8, 3.8))
eje.plot(pasos_tr, loss_tr, color=COLORES["train"], lw=0.7, alpha=0.3,
         label="train (cada paso)")
eje.plot(pasos_tr[ventana - 1:], media, color=COLORES["train"], lw=1.8,
         label=f"train (media de {ventana} pasos)")
eje.plot(*zip(*PERDIDAS_VAL), color=COLORES["validation"], lw=2.5,
         marker="o", ms=4, label="validation (t, ε fijos)")
eje.scatter([0], [PERDIDAS_VAL[0][1]], s=90, color=COLORES["base"], zorder=5,
            label="paso 0 = el modelo base")
eje.set(xlabel="paso", ylabel="MSE del ruido",
        title=f"LoRA r={P['rango']}: loss de train y de validation")
eje.legend(fontsize=8)
plt.tight_layout()
plt.show()
cambio = PERDIDAS_VAL[-1][1] - PERDIDAS_VAL[0][1]
print(f"validation: {PERDIDAS_VAL[0][1]:.4f} (base) → {PERDIDAS_VAL[-1][1]:.4f}"
      f" (LoRA) · cambio {cambio:+.4f} ({100 * cambio / PERDIDAS_VAL[0][1]:+.1f} %)")
