# §5 · La caja: entrenar, medir y generar. Todas las secciones siguientes la
# usan tal cual (Contrato congelado): Corrida, entrenar, perdida_val, generar,
# malla, curvas, delta_w, norma_relativa, completo_en_subproceso,
# embeddings_clip, clip_score, CORRIDAS, tabla, liberar.

# %% [texto] s05-intro

# %% [codigo] s05-importar
import gc
import json
import math
import tempfile
import time
from dataclasses import dataclass, field

import torch.nn.functional as F
from diffusers import (DDPMScheduler, DPMSolverMultistepScheduler,
                       UNet2DConditionModel)
from diffusers.optimization import get_scheduler
from diffusers.training_utils import cast_training_params
from peft import LoraConfig
from peft.utils import get_peft_model_state_dict, set_peft_model_state_dict
from safetensors.torch import load_file, save_file

CUDA = DEVICE.type == "cuda"
CARPETA = "adaptadores"                  # aquí quedan los .safetensors
os.makedirs(CARPETA, exist_ok=True)

# %% [codigo] s05-corrida-clase
@dataclass
class Corrida:
    nombre: str
    metodo: str = "lora"                 # "lora" o "qlora"
    rango: int = 8
    alfa: float | None = None            # None → alfa = rango
    modulos: tuple = ("to_q", "to_k", "to_v", "to_out.0")
    lr: float = 1e-4
    pasos: int | None = None             # None → P["pasos"] / P["pasos_control"]
    schedule: str = "cosine"             # "cosine" o "constante"
    warmup: int | None = None            # None → 5 % de los pasos
    semilla: int = 0
    datos: str = "train"                 # "train" o "control"
    # --- resultados (los llena entrenar) ---
    perdidas_train: list = field(default_factory=list)   # [(paso, loss)]
    perdidas_val: list = field(default_factory=list)     # [(paso, loss)]
    mem_pico_gb: float = float("nan")
    seg_por_paso: float = float("nan")
    mb_adaptador: float = float("nan")
    n_entrenables: int = 0
    error: str | None = None
    ruta: str | None = None

    def __post_init__(self):
        if self.alfa is None:
            self.alfa = self.rango
        if self.pasos is None:
            self.pasos = P["pasos_control" if self.datos == "control"
                           else "pasos"]
        if self.warmup is None:
            self.warmup = max(1, round(0.05 * self.pasos))

    def config(self):
        """Lo que define la corrida (sin resultados): sirve para no repetirla."""
        return (self.metodo, self.rango, self.alfa, tuple(self.modulos),
                self.lr, self.pasos, self.schedule, self.warmup,
                self.semilla, self.datos)


CORRIDAS: dict[str, Corrida] = {}
_RUIDO = DDPMScheduler.from_pretrained(MODELO, subfolder="scheduler")
print("Corrida por defecto:", Corrida("ejemplo").config())

# %% [texto] s05-unet-explica

# %% [codigo] s05-unet
def _cargar_unet(metodo):
    """UNet congelado: fp16 en GPU (LoRA) o NF4 de 4 bits (QLoRA)."""
    extra = {}
    if metodo == "qlora":
        if not CUDA:
            raise RuntimeError("QLoRA necesita GPU de NVIDIA (bitsandbytes)")
        from diffusers import BitsAndBytesConfig
        extra["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16)
    unet = UNet2DConditionModel.from_pretrained(
        MODELO, subfolder="unet", torch_dtype=DTYPE, **extra)
    if metodo == "qlora":     # ya vive en la GPU; .to() no se permite en 4 bits
        n4 = sum(type(m).__name__ == "Linear4bit" for m in unet.modules())
        print(f"  módulos Linear4bit: {n4}")
        if n4 == 0:
            raise RuntimeError("el UNet no quedó cuantizado (0 Linear4bit)")
    else:
        unet = unet.to(DEVICE)
    unet.requires_grad_(False)
    return unet


def _config_lora(c):
    """LoraConfig de la corrida. Una tupla de nombres va como lista
    (sufijos o nombres completos); un solo texto con '*' o '(' va como regex."""
    m = list(c.modulos)
    if len(m) == 1 and any(ch in m[0] for ch in "*(|"):
        m = m[0]
    return LoraConfig(r=c.rango, lora_alpha=c.alfa, target_modules=m,
                      init_lora_weights="gaussian")


def _latents(datos):
    if datos == "control":
        return LATENTS["train"][:len(CONTROL)]
    return LATENTS[datos]

# %% [codigo] s05-perdida-val
@torch.no_grad()
def perdida_val(unet, latents):
    """MSE del ruido con (t, eps) FIJOS de RUIDO_VAL: la evaluación i usa
    el latent i mod N y el par i mod K, así que dos corridas se miden igual."""
    t_fijo, eps_fijo = RUIDO_VAL
    n, k = len(latents), len(t_fijo)
    idx = torch.arange(max(n, k))
    dt = next(unet.parameters()).dtype if not CUDA else torch.float16
    emb = EMB.to(DEVICE, dt)
    estaba = unet.training
    unet.eval()
    total, cuenta = 0.0, 0
    for lote in idx.split(2 * P["batch"]):
        x0 = latents[lote % n].to(DEVICE, dt)
        eps = eps_fijo[lote % k].to(DEVICE, dt)
        t = t_fijo[lote % k].to(DEVICE)
        xt = _RUIDO.add_noise(x0, eps, t)
        with torch.autocast("cuda", dtype=torch.float16, enabled=CUDA):
            pred = unet(xt, t, encoder_hidden_states=emb.expand(len(x0), -1, -1)
                        ).sample
        total += F.mse_loss(pred.float(), eps.float(), reduction="sum").item()
        cuenta += eps.numel()
    unet.train(estaba)
    return total / cuenta

# %% [texto] s05-entrenar-explica

# %% [codigo] s05-entrenar
def _preparar(c):
    """UNet congelado + adaptador fp32 + AdamW + schedule + GradScaler."""
    liberar()                        # suelta el pipeline y CLIP: GPU para entrenar
    if CUDA:
        torch.cuda.reset_peak_memory_stats()
    unet = _cargar_unet(c.metodo)
    unet.add_adapter(_config_lora(c))
    unet.enable_gradient_checkpointing()   # menos activaciones, más cómputo
    # Adaptador en fp32 sobre el UNet fp16: GradScaler no desescala fp16.
    cast_training_params([unet], dtype=torch.float32)
    entrenables = [p for p in unet.parameters() if p.requires_grad]
    c.n_entrenables = sum(p.numel() for p in entrenables)
    opt = torch.optim.AdamW(entrenables, lr=c.lr, weight_decay=1e-2)
    sched = get_scheduler("cosine" if c.schedule == "cosine"
                          else "constant_with_warmup", opt,
                          num_warmup_steps=c.warmup, num_training_steps=c.pasos)
    return unet, entrenables, opt, sched, torch.amp.GradScaler("cuda", enabled=CUDA)

# %% [codigo] s05-entrenar-bucle
def _entrenar(c):
    semilla(c.semilla)
    unet, entrenables, opt, sched, escalador = _preparar(c)
    X, g = _latents(c.datos), torch.Generator().manual_seed(c.semilla)
    emb = EMB.to(DEVICE, DTYPE)
    tiempos, paso, intentos = [], 0, 0
    unet.train()
    while paso < c.pasos and intentos < 2 * c.pasos:
        intentos += 1
        t0 = time.perf_counter()
        x0 = X[torch.randint(len(X), (P["batch"],), generator=g)]
        eps = torch.randn(x0.shape, generator=g)
        t = torch.randint(0, _RUIDO.config.num_train_timesteps,
                          (len(x0),), generator=g)
        x0, eps, t = x0.to(DEVICE, DTYPE), eps.to(DEVICE, DTYPE), t.to(DEVICE)
        xt = _RUIDO.add_noise(x0, eps, t)              # forward de difusión
        with torch.autocast("cuda", dtype=torch.float16, enabled=CUDA):
            pred = unet(xt, t, encoder_hidden_states=emb.expand(len(x0), -1, -1)
                        ).sample
        loss = F.mse_loss(pred.float(), eps.float())   # ‖ε − ε̂‖² promedio
        opt.zero_grad(set_to_none=True)
        escalador.scale(loss).backward()
        escalador.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(entrenables, 1.0)
        escala_previa = escalador.get_scale()
        escalador.step(opt)
        escalador.update()
        if escalador.get_scale() < escala_previa:      # inf/NaN: paso saltado
            continue
        paso += 1
        sched.step()
        if CUDA:
            torch.cuda.synchronize()
        tiempos.append(time.perf_counter() - t0)
        c.perdidas_train.append((paso, loss.item()))
        if paso % P["val_cada"] == 0 or paso == c.pasos:
            c.perdidas_val.append((paso, perdida_val(unet, LATENTS["validation"])))
    _cerrar(c, unet, tiempos)


def _cerrar(c, unet, tiempos):
    """Memoria pico, s/paso y el adaptador (solo A y B) a disco."""
    if CUDA:
        c.mem_pico_gb = torch.cuda.max_memory_allocated() / 1e9
    medidos = tiempos[4:15] if len(tiempos) >= 15 else tiempos[1:] or tiempos
    c.seg_por_paso = sum(medidos) / max(len(medidos), 1)
    estado = {k: v.detach().float().cpu().contiguous()
              for k, v in get_peft_model_state_dict(unet).items()}
    c.ruta = os.path.join(CARPETA, f"{c.nombre}.safetensors")
    save_file(estado, c.ruta)
    c.mb_adaptador = os.path.getsize(c.ruta) / 1e6

# %% [codigo] s05-entrenar-publica
def entrenar(c: Corrida) -> Corrida:
    """Entrena (o reutiliza) la corrida y la registra en CORRIDAS.
    Un error (OOM, bitsandbytes…) queda en c.error y el notebook sigue."""
    previa = CORRIDAS.get(c.nombre)
    if (previa is not None and previa.error is None
            and previa.config() == c.config()):
        print(f"{c.nombre}: ya estaba entrenada, la reutilizo")
        return previa
    _quitar_del_pipe(c.nombre)       # si se reentrena, el pipe la recarga
    print(f"{c.nombre}: {c.metodo} r={c.rango} α={c.alfa} lr={c.lr} "
          f"pasos={c.pasos} ({c.schedule}) datos={c.datos}")
    inicio = time.perf_counter()
    try:
        _entrenar(c)
    except Exception as e:           # OOM, bitsandbytes, sin GPU…
        c.error = f"{type(e).__name__}: {str(e).splitlines()[0][:200]}"
        print(f"  ✗ {c.error}")
    finally:
        gc.collect()
        if CUDA:
            torch.cuda.empty_cache()
    CORRIDAS[c.nombre] = c
    if c.error is None:
        print(f"  ✓ {time.perf_counter() - inicio:.0f} s · val final "
              f"{c.perdidas_val[-1][1]:.4f} · {c.mb_adaptador:.1f} MB")
    return c

# %% [texto] s05-generar-explica

# %% [codigo] s05-generar
_PIPE, _EN_PIPE = None, set()        # pipeline base en caché y adaptadores cargados


def _pipe():
    """StableDiffusionPipeline base (fp16 en GPU) armado pieza por pieza."""
    global _PIPE
    if _PIPE is None:
        from diffusers import AutoencoderKL, StableDiffusionPipeline
        from transformers import CLIPTextModel, CLIPTokenizer
        _PIPE = StableDiffusionPipeline(
            vae=AutoencoderKL.from_pretrained(MODELO, subfolder="vae",
                                              torch_dtype=DTYPE),
            text_encoder=CLIPTextModel.from_pretrained(
                MODELO, subfolder="text_encoder", torch_dtype=DTYPE),
            tokenizer=CLIPTokenizer.from_pretrained(MODELO, subfolder="tokenizer"),
            unet=UNet2DConditionModel.from_pretrained(
                MODELO, subfolder="unet", torch_dtype=DTYPE),
            scheduler=DPMSolverMultistepScheduler.from_pretrained(
                MODELO, subfolder="scheduler"),
            safety_checker=None, feature_extractor=None,
            requires_safety_checker=False).to(DEVICE)
        _PIPE.set_progress_bar_config(disable=True)
        _PIPE.vae.enable_slicing()     # decodifica de una en una: menos VRAM
        _EN_PIPE.clear()
    return _PIPE

# %% [codigo] s05-generar-adaptador
def _quitar_del_pipe(nombre):
    if _PIPE is not None and nombre in _EN_PIPE:
        _PIPE.unet.delete_adapters(nombre)
        _EN_PIPE.discard(nombre)


def _activar(nombre):
    """Pone el adaptador `nombre` (o ninguno, si es None) en el UNet del pipe.
    Un adaptador QLoRA se aplica sobre el UNet fp16, no sobre el cuantizado."""
    unet = _pipe().unet
    if nombre is None:
        if _EN_PIPE:
            unet.disable_adapters()
        return
    c = CORRIDAS[nombre]
    if c.error is not None:
        raise ValueError(f"la corrida {nombre} falló: {c.error}")
    if nombre not in _EN_PIPE:
        unet.add_adapter(_config_lora(c), adapter_name=nombre)
        set_peft_model_state_dict(unet, load_file(c.ruta), adapter_name=nombre)
        _EN_PIPE.add(nombre)
    unet.set_adapter(nombre)
    unet.enable_adapters()


@torch.no_grad()
def generar(nombre, prompts=PROMPT, semillas=None, escala=1.0):
    """Una imagen por (prompt, semilla), prompt-mayor. nombre=None → base.
    escala = λ multiplica a ΔW (λ=0 es el base)."""
    prompts = [prompts] if isinstance(prompts, str) else list(prompts)
    semillas = P["semillas"] if semillas is None else list(semillas)
    _activar(nombre)
    pipe, salida = _pipe(), []
    for p in prompts:                # lotes de 2 semillas: cabe en la T4
        for i in range(0, len(semillas), 2):
            lote = semillas[i:i + 2]
            gens = [torch.Generator("cpu").manual_seed(s) for s in lote]
            salida += pipe([p] * len(lote), generator=gens,
                           num_inference_steps=2 if RAPIDO else 20,
                           height=P["res"], width=P["res"],
                           cross_attention_kwargs={"scale": escala}).images
    return salida

# %% [texto] s05-ver-explica

# %% [codigo] s05-ver
def malla(imagenes, filas, titulo, etiquetas=None):
    """Malla de imágenes (≤ 256 px, dpi 80). etiquetas: una por imagen
    (título chico) o una por fila (a la izquierda)."""
    n = len(imagenes)
    cols = max(1, math.ceil(n / filas))
    fig, ejes = plt.subplots(filas, cols, figsize=(1.9 * cols, 1.9 * filas),
                             squeeze=False, dpi=80)
    for i, eje in enumerate(ejes.flat):
        eje.axis("off")
        if i >= n:
            continue
        im = imagenes[i].copy()
        im.thumbnail((256, 256))
        eje.imshow(im)
        if etiquetas is not None and len(etiquetas) == n:
            eje.set_title(etiquetas[i], fontsize=7)
    if etiquetas is not None and len(etiquetas) == filas and filas != n:
        for f in range(filas):
            ejes[f, 0].text(-0.05, 0.5, etiquetas[f], fontsize=8, ha="right",
                            va="center", transform=ejes[f, 0].transAxes)
    fig.suptitle(titulo, fontsize=10)
    plt.tight_layout()
    plt.show()


def curvas(nombres, titulo):
    """Loss por paso: train delgada y tenue, validation gruesa; un color
    por corrida. Las corridas con error se avisan y no se dibujan."""
    fig, eje = plt.subplots(figsize=(7.5, 3.6))
    for i, n in enumerate(nombres):
        c = CORRIDAS.get(n)
        if c is None or c.error is not None:
            print(f"(sin curva para {n}: {c.error if c else 'no existe'})")
            continue
        color = plt.cm.tab10(i % 10)
        if c.perdidas_train:
            eje.plot(*zip(*c.perdidas_train), color=color, lw=0.8, alpha=0.35,
                     label=f"{n} · train")
        if c.perdidas_val:
            eje.plot(*zip(*c.perdidas_val), color=color, lw=2.5, marker="o",
                     ms=3, label=f"{n} · validation")
    eje.set(xlabel="paso", ylabel="MSE del ruido", title=titulo)
    eje.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    plt.show()

# %% [texto] s05-medir-explica

# %% [codigo] s05-medir
def delta_w(nombre):
    """ΔW = (α/r)·B·A por capa adaptada, en CPU y fp32."""
    c = CORRIDAS[nombre]
    estado, s = load_file(c.ruta), c.alfa / c.rango
    salida = {}
    for k in estado:
        if k.endswith(".lora_A.weight"):
            capa = k[: -len(".lora_A.weight")]
            B = estado[capa + ".lora_B.weight"].float()
            salida[capa] = s * (B @ estado[k].float())     # [d_out, d_in]
    return salida


_NORMA_W0 = {}


def norma_relativa(nombre):
    """‖ΔW‖_F / ‖W₀‖_F por capa (índice = nombre de la capa)."""
    if not _NORMA_W0:
        for n, m in _pipe().unet.named_modules():
            if isinstance(m, torch.nn.Linear):
                n = n.removesuffix(".base_layer")
                _NORMA_W0[n] = m.weight.float().norm().item()
    dw = delta_w(nombre)
    return pd.Series({k: v.norm().item() / _NORMA_W0[k] for k, v in dw.items()},
                     name=nombre)

# %% [codigo] s05-clip
_CLIP = None


def _clip():
    global _CLIP
    if _CLIP is None:
        from transformers import CLIPModel, CLIPProcessor
        _CLIP = (CLIPModel.from_pretrained(MODELO_CLIP).to(DEVICE).eval(),
                 CLIPProcessor.from_pretrained(MODELO_CLIP))
    return _CLIP


def _vector(salida):
    """get_*_features devuelve un tensor o (versiones nuevas) un objeto."""
    if torch.is_tensor(salida):
        return salida
    for campo in ("image_embeds", "text_embeds", "pooler_output"):
        if getattr(salida, campo, None) is not None:
            return getattr(salida, campo)
    raise TypeError(type(salida))


@torch.no_grad()
def embeddings_clip(imagenes):
    """(N, D) con norma 1: el coseno entre dos imágenes es su producto punto."""
    modelo, proc = _clip()
    out = []
    for i in range(0, len(imagenes), 32):
        x = proc(images=imagenes[i:i + 32], return_tensors="pt").to(DEVICE)
        out.append(_vector(modelo.get_image_features(**x)).float().cpu())
    return F.normalize(torch.cat(out), dim=-1)


@torch.no_grad()
def clip_score(imagenes, prompt):
    """CLIP score = 100 · coseno(imagen, texto), promediado (más es mejor)."""
    modelo, proc = _clip()
    x = proc(text=[prompt], return_tensors="pt", padding=True).to(DEVICE)
    texto = F.normalize(_vector(modelo.get_text_features(**x)).float().cpu(), dim=-1)
    return float(100 * (embeddings_clip(imagenes) @ texto.T).mean())

# %% [texto] s05-tabla-explica

# %% [codigo] s05-tabla
def tabla(nombres=None):
    """Una fila por corrida: lo que se configuró y lo que se midió."""
    filas = []
    for n in (nombres or list(CORRIDAS)):
        c = CORRIDAS[n]
        filas.append({
            "corrida": n, "método": c.metodo, "rango": c.rango,
            "módulos": ",".join(c.modulos) if len(c.modulos) <= 6
            else f"{len(c.modulos)} capas",
            "lr": c.lr, "pasos": c.pasos,
            "loss val final": c.perdidas_val[-1][1] if c.perdidas_val
            else float("nan"),
            "mem pico GB": c.mem_pico_gb, "s/paso": c.seg_por_paso,
            "MB adaptador": c.mb_adaptador,
            "parámetros entrenables": c.n_entrenables, "error": c.error})
    return pd.DataFrame(filas).set_index("corrida")


def liberar():
    """Suelta el pipeline y CLIP de la memoria (GPU y RAM)."""
    global _PIPE, _CLIP
    _PIPE, _CLIP = None, None
    _EN_PIPE.clear()
    _NORMA_W0.clear()
    gc.collect()
    if CUDA:
        torch.cuda.empty_cache()

# %% [texto] s05-completo-explica

# %% [codigo] s05-completo
_GUION_COMPLETO = r'''
import json, sys, torch, torch.nn.functional as F
from diffusers import UNet2DConditionModel
modelo, lado = sys.argv[1], int(sys.argv[2])
r = {"ok": False, "error": None, "mem_pico_gb": None}
try:
    unet = UNet2DConditionModel.from_pretrained(
        modelo, subfolder="unet", torch_dtype=torch.float32).to("cuda").train()
    opt = torch.optim.AdamW(unet.parameters(), lr=1e-5,   # TODO el UNet
                            foreach=False)
    x = torch.randn(1, 4, lado, lado, device="cuda")      # batch 1
    t = torch.randint(0, 1000, (1,), device="cuda")
    emb = torch.randn(1, 77, unet.config.cross_attention_dim, device="cuda")
    pred = unet(x, t, encoder_hidden_states=emb).sample
    F.mse_loss(pred, torch.randn_like(pred)).backward()
    opt.step()                       # aquí nacen los dos momentos de Adam
    torch.cuda.synchronize()
    r["ok"] = True
except torch.cuda.OutOfMemoryError as e:
    r["error"] = "OOM: " + str(e).splitlines()[0][:160]
except Exception as e:
    r["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:160]}"
if torch.cuda.is_available():
    r["mem_pico_gb"] = torch.cuda.max_memory_allocated() / 1e9
print("JSON" + json.dumps(r))
'''


def completo_en_subproceso():
    """Un paso de fine-tuning COMPLETO (fp32 + AdamW) en otro proceso:
    si revienta por memoria, la VRAM se libera al terminar el proceso."""
    if not CUDA:
        return {"ok": False, "error": "sin GPU", "mem_pico_gb": None}
    liberar()                        # que el otro proceso tenga la GPU entera
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(_GUION_COMPLETO)
    lado = LATENTS["train"].shape[-1]
    try:
        r = subprocess.run([sys.executable, f.name, MODELO, str(lado)],
                           capture_output=True, text=True, timeout=1200)
        linea = [l for l in r.stdout.splitlines() if l.startswith("JSON")]
        if not linea:
            cola = (r.stderr or "").strip().splitlines()[-1:] or ["sin salida"]
            return {"ok": False, "error": cola[0][:200], "mem_pico_gb": None}
        return json.loads(linea[-1][4:])
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"[:200],
                "mem_pico_gb": None}
