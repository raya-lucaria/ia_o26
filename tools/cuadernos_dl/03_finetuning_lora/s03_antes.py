# §3 · Antes: el modelo base, sin adaptador, con tus prompts.txt y con 3
# captions de validation. Define PIPE, UNET, usar_lora, tiene_lora,
# combinar, generar y ANTES (imágenes del base con PROMPTS × P["semillas"]).

# %% [texto] s03-intro

# %% [codigo] s03-pipeline
import gc

from diffusers import (AutoencoderKL, DPMSolverMultistepScheduler,
                       StableDiffusionPipeline, UNet2DConditionModel)
from transformers import CLIPTextModel, CLIPTokenizer


def pesos(clase, sub):
    """En la GPU baja la variante fp16 (la mitad de GB); si el repo no la
    tiene, baja los pesos normales y los convierte."""
    if CUDA:
        try:
            return clase.from_pretrained(MODELO, subfolder=sub,
                                         torch_dtype=DTYPE, variant="fp16")
        except (OSError, ValueError) as e:
            print(f"{sub}: sin variante fp16 ({type(e).__name__}); bajo la normal")
    return clase.from_pretrained(MODELO, subfolder=sub, torch_dtype=DTYPE)


def cargar_pipe():
    """StableDiffusionPipeline armado pieza por pieza (fp16 en la GPU)."""
    piezas = dict(
        vae=pesos(AutoencoderKL, "vae"),
        text_encoder=pesos(CLIPTextModel, "text_encoder"),
        tokenizer=CLIPTokenizer.from_pretrained(MODELO, subfolder="tokenizer"),
        unet=pesos(UNet2DConditionModel, "unet"),
        scheduler=DPMSolverMultistepScheduler.from_pretrained(
            MODELO, subfolder="scheduler"))
    pipe = StableDiffusionPipeline(**piezas, safety_checker=None,
                                   feature_extractor=None,
                                   requires_safety_checker=False).to(DEVICE)
    pipe.set_progress_bar_config(disable=True)
    pipe.vae.enable_slicing()          # decodifica de una en una: menos VRAM
    for pieza in (pipe.vae, pipe.text_encoder, pipe.unet):
        pieza.requires_grad_(False)    # nada del modelo base se entrena
    return pipe


PIPE = cargar_pipe()
UNET = PIPE.unet                       # el que recibirá el adaptador LoRA
for nombre in ("unet", "vae", "text_encoder"):
    n = sum(p.numel() for p in getattr(PIPE, nombre).parameters())
    print(f"{nombre:13s}{n / 1e6:8.1f} M parámetros")

# %% [texto] s03-generar-explica

# %% [codigo] s03-generar
def tiene_lora():
    """¿Ya tiene el UNet un adaptador? (antes de la sección 05, no)."""
    return bool(getattr(UNET, "peft_config", None))


def usar_lora(si):
    """Prende (si=True) o apaga el adaptador. W0 nunca se toca."""
    if tiene_lora():
        (UNET.enable_adapters if si else UNET.disable_adapters)()
    elif si:
        raise RuntimeError("Aún no hay adaptador: corre la sección 05.")


def combinar(prompts, semillas):
    """Todas las parejas (prompt, semilla), prompt por prompt."""
    return [(p, s) for p in prompts for s in semillas]


@torch.no_grad()
def generar(pares, lora=False, escala=1.0):
    """Una imagen por pareja (prompt, semilla). lora=False → el modelo base.
    escala = λ multiplica a ΔW (solo con lora=True)."""
    usar_lora(lora)
    UNET.eval()
    # sin adaptador no se pasa scale: diffusers lo exige solo con LoRA
    extra = {"cross_attention_kwargs": {"scale": escala}} if lora else {}
    salida = []
    for i in range(0, len(pares), 2):  # de 2 en 2: cabe en la T4
        lote = pares[i:i + 2]
        gens = [torch.Generator("cpu").manual_seed(s) for _, s in lote]
        salida += PIPE([p for p, _ in lote], generator=gens,
                       num_inference_steps=P["pasos_inferencia"],
                       height=P["res"], width=P["res"], **extra).images
    return salida

# %% [texto] s03-prompts-explica

# %% [codigo] s03-prompts
ANTES = generar(combinar(PROMPTS, P["semillas"]))
malla(ANTES, filas=len(PROMPTS), titulo="ANTES · el modelo base con tus prompts",
      etiquetas=PROMPTS)                   # una etiqueta por fila

# %% [texto] s03-validation-explica

# %% [codigo] s03-validation
# Tres imágenes reales de validation (arriba) y lo que el base genera con
# su mismo caption (abajo). Semillas 1000, 1001, … : ninguna otra celda las usa.
k = min(3, len(IMGS["validation"]))
pares_val = [(TEXTOS["validation"][i], 1000 + i) for i in range(k)]
base_val = generar(pares_val)
malla(IMGS["validation"][:k] + base_val, filas=2,
      titulo="validation: real (arriba) y el base con el mismo caption (abajo)",
      etiquetas=[f"real · {t}" for t, _ in pares_val]
      + [f"base · {t}" for t, _ in pares_val])
