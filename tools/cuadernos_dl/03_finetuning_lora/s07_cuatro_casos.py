# Sección 7 · Los cuatro casos.
# Fine-tuning completo (en un subproceso, con la cuenta de 16 bytes por
# parámetro), LoRA r = 8 y QLoRA r = 8; ➕ LoRA r = 1 y r = 64.
# Produce las corridas "lora_r8" y "qlora_r8" (y ➕ "lora_r1", "lora_r64"),
# que consumen s08, s10, s11, s12 y s13.

# %% [texto] s07-intro

# %% [codigo] s07-cuenta
import pandas as pd
import torch
from diffusers import UNet2DConditionModel

# Contamos los parámetros del UNet sin cargar pesos: en el device «meta»
# los tensores no ocupan memoria (solo se baja el config.json).
try:
    config_s07 = UNet2DConditionModel.load_config(MODELO, subfolder="unet")
    with torch.device("meta"):
        unet_vacio = UNet2DConditionModel.from_config(config_s07)
    N_UNET_S07 = sum(p.numel() for p in unet_vacio.parameters())
    origen = "contado del config"
    del unet_vacio
except Exception as e:                       # sin red, versión rara, etc.
    N_UNET_S07, origen = int(8.6e8), f"aproximado ({type(e).__name__})"

# AdamW en fp32: cada parámetro ENTRENABLE paga cuatro copias de 4 bytes.
PARTES_S07 = {"pesos (fp32)": 4, "gradiente": 4, "m de AdamW": 4,
              "v de AdamW": 4}
filas = [{"qué": k, "bytes/param": b, "GB": N_UNET_S07 * b / 1e9,
          "GiB": N_UNET_S07 * b / 2**30} for k, b in PARTES_S07.items()]
filas.append({"qué": "TOTAL", "bytes/param": 16, "GB": N_UNET_S07 * 16 / 1e9,
              "GiB": N_UNET_S07 * 16 / 2**30})
print(f"Parámetros del UNet: {N_UNET_S07:,} ({origen})")
display(pd.DataFrame(filas).set_index("qué").round(2))
print("…y eso es ANTES de activaciones, temporales y el resto del pipeline.")
if torch.cuda.is_available():
    total = torch.cuda.get_device_properties(0).total_memory / 2**30
    print(f"Memoria de esta GPU: {total:.1f} GiB")

# %% [codigo] s07-completo
# El completo corre en OTRO proceso: si se queda sin memoria, este notebook
# sigue vivo, y al terminar ese proceso la GPU queda libre otra vez.
liberar()            # soltamos el pipeline de s06 para no competir por VRAM
RES_COMPLETO_S07 = completo_en_subproceso()
if RES_COMPLETO_S07["ok"]:
    print("El fine-tuning completo CUPO: dio un paso de AdamW con "
          f"{RES_COMPLETO_S07['mem_pico_gb']:.2f} GB de pico. "
          "Resultado raro en una T4: lee el comentario de abajo.")
else:
    print(f"El fine-tuning completo NO corrió: {RES_COMPLETO_S07['error']}")
    if RES_COMPLETO_S07.get("mem_pico_gb"):
        print(f"memoria pico antes de fallar: "
              f"{RES_COMPLETO_S07['mem_pico_gb']:.2f} GB")

# %% [texto] s07-lora

# %% [codigo] s07-entrenar
# LoRA r = 8 en la atención (to_q, to_k, to_v, to_out.0), lr 1e-4, cosine.
# Es la corrida base del notebook: la usan s08, s10, s11, s12 y s13.
R8_S07 = entrenar(Corrida("lora_r8"))
if R8_S07.error:
    print(f"lora_r8 falló: {R8_S07.error}")
elif R8_S07.seg_por_paso:
    # Estimación de tiempo con el s/paso medido (tras calentar la GPU).
    minutos = R8_S07.seg_por_paso * P["pasos"] / 60
    print(f"lora_r8: {R8_S07.seg_por_paso:.3f} s/paso → una corrida LoRA de "
          f"este MODO ({P['pasos']} pasos) tarda ≈ {minutos:.1f} min")

# QLoRA: el mismo adaptador, pero W₀ guardada en 4 bits NF4.
# Sin CUDA o sin bitsandbytes la caja deja el error en la corrida y sigue.
Q8_S07 = entrenar(Corrida("qlora_r8", metodo="qlora"))
if Q8_S07.error:
    print(f"qlora_r8 no corrió: {Q8_S07.error} (el notebook sigue)")
elif not R8_S07.error and R8_S07.seg_por_paso:
    razon = Q8_S07.seg_por_paso / R8_S07.seg_por_paso
    print(f"qlora_r8: {Q8_S07.seg_por_paso:.3f} s/paso = {razon:.2f}× LoRA")

# %% [codigo] s07-rangos
# ➕ El rango: r = 1 (casi nada) y r = 64 (8× más parámetros que r = 8).
# alfa = rango en las tres, así la escala α/r vale 1 en todas.
if LARGO:
    for r in (1, 64):
        c = entrenar(Corrida(f"lora_r{r}", rango=r))
        print(f"lora_r{r}: " + (c.error or "lista"))
else:
    print("(solo en MODO largo)")

# %% [texto] s07-tabla-idea

# %% [codigo] s07-tabla
NOMBRES_S07 = [n for n in ("lora_r8", "qlora_r8", "lora_r1", "lora_r64")
               if n in CORRIDAS]
OK_S07 = [n for n in NOMBRES_S07 if CORRIDAS[n].error is None]
display(tabla(NOMBRES_S07))

# Lo entrenable frente al completo, y lo que AdamW paga por ello (16 B/param).
for n in OK_S07:
    c = CORRIDAS[n]
    print(f"{n:>9}: {c.n_entrenables:>10,} entrenables = "
          f"{100 * c.n_entrenables / N_UNET_S07:.2f} % del UNet · "
          f"AdamW: {16 * c.n_entrenables / 2**20:.1f} MiB "
          f"(vs {16 * N_UNET_S07 / 2**30:.1f} GiB el completo)")
if RAPIDO:
    print("Modo RAPIDO: modelo diminuto y unos pocos pasos; la tabla solo "
          "prueba que el código corre.")

# %% [texto] s07-curvas-idea

# %% [codigo] s07-curvas
if OK_S07:
    curvas(OK_S07, "Los casos que corrieron: train (delgada) y validation (gruesa)")
else:
    print("Ninguna corrida terminó: no hay curvas que mostrar.")

# %% [texto] s07-malla-idea

# %% [codigo] s07-malla
import numpy as np

# Una fila por método, las MISMAS semillas de s06 en cada columna.
FILAS_S07 = [None] + OK_S07                     # None = modelo base
imgs = []
for nombre in FILAS_S07:
    imgs += generar(nombre, PROMPT, P["semillas"])
n_sem = len(P["semillas"])
malla(imgs, filas=len(FILAS_S07),
      titulo=f"«{PROMPT}» · una fila por método, mismas semillas",
      etiquetas=[n or "base" for n in FILAS_S07])    # una por fila

# ¿Cuánto se movió cada fila respecto al base? Diferencia media de píxeles
# (0 = idéntica, 255 = opuesta), semilla por semilla.
base = [np.asarray(im, dtype=np.float32) for im in imgs[:n_sem]]
for i, nombre in enumerate(OK_S07, start=1):
    fila = imgs[i * n_sem:(i + 1) * n_sem]
    dif = [np.abs(np.asarray(im, dtype=np.float32) - b).mean()
           for im, b in zip(fila, base)]
    print(f"{nombre:>9} vs base: |Δpíxel| medio = {np.mean(dif):.1f} / 255")

# %% [texto] s07-que-mirar
