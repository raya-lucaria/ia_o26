# §3 · Cómo aprende un modelo de difusión: la loss y el precomputo.
# Define LATENTS (CPU, fp32, ya por scaling_factor), EMB (1, 77, D) del
# PROMPT y RUIDO_VAL = (t, eps) fijos con semilla 0. Libera VAE y text encoder.

# %% [texto] s03-intro

# %% [texto] s03-precomputar-explica

# %% [codigo] s03-precomputar
import gc

from diffusers import AutoencoderKL, DDPMScheduler
from transformers import CLIPTextModel, CLIPTokenizer

VAE = AutoencoderKL.from_pretrained(MODELO, subfolder="vae",
                                    torch_dtype=DTYPE).to(DEVICE).eval()
TOKENIZER = CLIPTokenizer.from_pretrained(MODELO, subfolder="tokenizer")
TEXTO = CLIPTextModel.from_pretrained(MODELO, subfolder="text_encoder",
                                      torch_dtype=DTYPE).to(DEVICE).eval()
ESCALA_VAE = VAE.config.scaling_factor          # 0.18215 en SD 1.5


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
        z = VAE.encode(x).latent_dist.mode()     # la media: determinista
        salida.append((z * ESCALA_VAE).float().cpu())
    return torch.cat(salida)


LATENTS = {k: codificar(v) for k, v in DATOS.items()}

with torch.no_grad():
    ids = TOKENIZER(PROMPT, padding="max_length", truncation=True,
                    max_length=TOKENIZER.model_max_length,
                    return_tensors="pt").input_ids.to(DEVICE)
    EMB = TEXTO(ids)[0].float().cpu()            # (1, 77, D)

for k, z in LATENTS.items():
    print(f"LATENTS[{k!r}]: {tuple(z.shape)}")
print("EMB:", tuple(EMB.shape))
pix, lat = 3 * P["res"] ** 2, LATENTS["train"][0].numel()
print(f"una imagen: {pix:,} números → un latent: {lat:,} ({pix / lat:.0f}× menos)")

# %% [texto] s03-ruido-explica

# %% [codigo] s03-ruido
# Pares (t, ε) FIJOS para medir la loss de validation: misma semilla,
# mismos t ⇒ la curva de validation no tiembla por el azar del ruido.
RUIDO = DDPMScheduler.from_pretrained(MODELO, subfolder="scheduler")
T = RUIDO.config.num_train_timesteps
K = P["n_val_ruido"]
gen = torch.Generator().manual_seed(0)
t_val = torch.linspace(0, T - 1, K).round().long()      # espaciados en [0, T-1]
eps_val = torch.randn((K, *LATENTS["train"].shape[1:]), generator=gen)
RUIDO_VAL = (t_val, eps_val)
abar = RUIDO.alphas_cumprod
display(pd.DataFrame({"t": t_val.tolist(),
                      "√ᾱ_t (señal)": abar[t_val].sqrt().numpy().round(3),
                      "√(1-ᾱ_t) (ruido)": (1 - abar[t_val]).sqrt().numpy().round(3)}
                     ).set_index("t").T)

# %% [texto] s03-ver-explica

# %% [codigo] s03-ver
# Una cara de train: su latent (4 canales) y x_t para tres valores de t.
x0 = LATENTS["train"][:1]
eps = torch.randn(x0.shape, generator=torch.Generator().manual_seed(1))
TS = [100, 500, 900] if T > 900 else [T // 10, T // 2, 9 * T // 10]
xts = [RUIDO.add_noise(x0, eps, torch.tensor([t])) for t in TS]
with torch.no_grad():   # el VAE regresa cada latent a píxeles para verlo
    vistas = [VAE.decode((z / ESCALA_VAE).to(DEVICE, DTYPE)).sample
              for z in [x0, *xts]]
vistas = [((v[0].float().cpu().permute(1, 2, 0) + 1) / 2).clamp(0, 1).numpy()
          for v in vistas]

fig, ejes = plt.subplots(2, 5, figsize=(12, 5.2))
ejes[0, 0].imshow(DATOS["train"][0])
ejes[0, 0].set_title("imagen (píxeles)", fontsize=9)
for c in range(4):
    ejes[0, c + 1].imshow(x0[0, c].numpy(), cmap="RdBu_r")
    ejes[0, c + 1].set_title(f"latent, canal {c}", fontsize=9)
ejes[1, 0].imshow(vistas[0])
ejes[1, 0].set_title("x_0 decodificado", fontsize=9)
for j, t in enumerate(TS):
    ejes[1, j + 1].imshow(vistas[j + 1])
    ejes[1, j + 1].set_title(f"x_t con t = {t}, decodificado", fontsize=9)
ejes[1, 4].imshow(xts[-1][0, 0].numpy(), cmap="RdBu_r")
ejes[1, 4].set_title(f"x_t, t = {TS[-1]}, canal 0", fontsize=9)
for ax in ejes.flat:
    ax.axis("off")
fig.suptitle("Arriba: la cara y su latent. Abajo: más t, más ruido", fontsize=11)
fig.tight_layout()
plt.show()

# Ya no hacen falta: liberamos la GPU para entrenar el UNet.
del VAE, TEXTO
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
print("VAE y text encoder liberados.")
