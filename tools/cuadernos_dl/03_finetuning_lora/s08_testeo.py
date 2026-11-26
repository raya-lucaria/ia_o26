# §8 · Testeo, una sola vez: todas las métricas de s07 en TEST (base vs
# LoRA), ejemplos, tus prompts antes/después, olvido con semillas nuevas,
# guardar y descargar el adaptador, y la receta «si salió mal».
# Es la ÚNICA sección que toca test.

# %% [texto] s08-intro

# %% [codigo] s08-test
# Semillas 3000, 3001, … y 4000, …: ninguna sección anterior las usó.
GEN_TEST = generadas("test", 3000)
OLVIDO_TEST, OLVIDO_IMGS = m_olvido([4000 + i for i in range(len(P["semillas"]))])
TEST = {"loss de difusión": m_loss("test"),
        "CLIP score": m_clip(GEN_TEST),
        "parecido al estilo": m_estilo("test", GEN_TEST),
        "vecino en train": m_memoria("test", GEN_TEST),
        "olvido": OLVIDO_TEST.mean().to_dict()}
TABLA_TEST = resumen(TEST)
display(TABLA_TEST.style.format(
    {c: "{:.4f}" for c in ("base", "LoRA", "referencia", "LoRA − base")},
    na_rep="—").set_caption("TEST · base vs LoRA (una sola vez)"))
# Validation contra test, solo para LoRA: ¿fue validation un buen juez?
# Sin «olvido»: usa los mismos prompts ajenos en los dos; solo cambian semillas.
display(pd.DataFrame({"validation": resumen(VAL)["LoRA"],
                      "test": TABLA_TEST["LoRA"]}).drop(index="olvido").round(4))

# %% [texto] s08-tabla-leer

# %% [codigo] s08-ejemplos
# Test: real / base / LoRA con el mismo caption y semilla.
k = min(8 if LARGO else 4, len(IMGS["test"]), P["n_gen"])
malla(IMGS["test"][:k] + GEN_TEST["base"][:k] + GEN_TEST["LoRA"][:k],
      filas=3, titulo="test · real / base / LoRA (mismo caption y semilla)",
      etiquetas=["real", "base", "LoRA"])

# Tus prompts.txt: las MISMAS parejas de la sección 03, ahora con LoRA.
DESPUES = generar(combinar(PROMPTS, P["semillas"]), lora=True)
n = len(P["semillas"])
imgs, filas = [], []
for j, prompt in enumerate(PROMPTS):
    imgs += ANTES[j * n:(j + 1) * n] + DESPUES[j * n:(j + 1) * n]
    filas += [f"antes · {prompt}", f"después · {prompt}"]
malla(imgs, filas=2 * len(PROMPTS), titulo="Tus prompts: antes y después",
      etiquetas=filas)

# %% [texto] s08-olvido-explica

# %% [codigo] s08-olvido
n = len(P["semillas"])
imgs, filas = [], []
for j, prompt in enumerate(PROMPTS_AJENOS):
    for quien in ("base", "LoRA"):
        imgs += OLVIDO_IMGS[quien][j * n:(j + 1) * n]
        filas.append(f"{quien} · {prompt}")
malla(imgs, filas=len(filas), titulo="Prompts ajenos: base y LoRA",
      etiquetas=filas)
display(OLVIDO_TEST.assign(**{"LoRA − base": OLVIDO_TEST["LoRA"] -
                              OLVIDO_TEST["base"]}).round(2))

# %% [texto] s08-guardar-explica

# %% [codigo] s08-guardar
from diffusers.utils import convert_state_dict_to_diffusers
from peft.utils import get_peft_model_state_dict

CARPETA_LORA = Path("mi_lora")
pesos = convert_state_dict_to_diffusers(get_peft_model_state_dict(UNET))
StableDiffusionPipeline.save_lora_weights(CARPETA_LORA, unet_lora_layers=pesos,
                                          safe_serialization=True)
ARCHIVO_LORA = CARPETA_LORA / "pytorch_lora_weights.safetensors"
mb = ARCHIVO_LORA.stat().st_size / 1e6
print(f"{ARCHIVO_LORA}: {mb:.1f} MB (la cuenta de la sección 04 decía "
      f"{4 * N_LORA / 1e6:.1f} MB) · el UNet en fp16: {2 * N_UNET / 1e6:,.0f} MB")
try:                                  # en Colab: lo baja tu navegador
    from google.colab import files
    files.download(str(ARCHIVO_LORA))
except ImportError:
    print("(fuera de Colab: el archivo quedó en", ARCHIVO_LORA.resolve(), ")")

# %% [texto] s08-receta
