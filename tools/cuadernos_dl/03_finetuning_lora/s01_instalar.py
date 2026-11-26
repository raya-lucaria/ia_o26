# §1 · Instalar y configurar: MODO, paquetes que falten, GPU, tamaños, semillas.
# Define MODO, LARGO, RAPIDO, DEVICE, DTYPE, CUDA, MODELO, MODELO_CLIP,
# COLORES, semilla(s) y el diccionario P de tamaños por modo.

# %% [texto] s01-intro

# %% [codigo] s01-modo
MODO = "corto"   # "corto" (≈ 20–25 min en una T4) o "largo" (≈ 50–60 min)
LARGO = MODO == "largo"

# Instala solo lo que falta; no actualiza lo que Colab ya trae.
import importlib.util
import subprocess
import sys

FALTAN = [p for p in ["diffusers", "peft", "accelerate", "transformers"]
          if importlib.util.find_spec(p) is None]
if FALTAN:
    print("Instalando:", ", ".join(FALTAN))
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *FALTAN],
                   check=True)
else:
    print("No falta nada que instalar.")
print("MODO =", MODO, "· LARGO =", LARGO)

# %% [texto] s01-gpu-explica

# %% [codigo] s01-gpu
import os
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import diffusers
import peft
import transformers

# RAPIDO=1: prueba local en CPU con modelos diminutos (sus imágenes son ruido).
RAPIDO = os.environ.get("RAPIDO") == "1"
HAY_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if HAY_GPU and not RAPIDO else "cpu")
CUDA = DEVICE.type == "cuda"
DTYPE = torch.float16 if CUDA else torch.float32   # la T4 no tiene bf16

if not HAY_GPU and not RAPIDO:
    print("=" * 72)
    print("  ¡AVISO! ESTE ENTORNO NO TIENE GPU.")
    print("  Stable Diffusion en CPU tardaría horas. En Colab:")
    print("    Entorno de ejecución → Cambiar tipo de entorno → T4 GPU")
    print("    → Guardar, y luego Entorno de ejecución → Ejecutar todo.")
    print("=" * 72)

for nombre, mod in [("torch", torch), ("diffusers", diffusers),
                    ("peft", peft), ("transformers", transformers)]:
    print(f"{nombre:14s}{mod.__version__}")
print("DEVICE =", DEVICE, "· DTYPE =", DTYPE, "· RAPIDO =", RAPIDO)
if HAY_GPU:
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name} · {props.total_memory / 2**30:.1f} GiB")

# %% [texto] s01-constantes-explica

# %% [codigo] s01-constantes
# El modelo que ajustamos y el CLIP que mide las imágenes.
if RAPIDO:
    MODELO = "hf-internal-testing/tiny-stable-diffusion-pipe"
    MODELO_CLIP = "hf-internal-testing/tiny-random-CLIPModel"
else:
    MODELO = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    MODELO_CLIP = "openai/clip-vit-base-patch32"

# Tamaños por modo. pasos = actualizaciones del adaptador.
if RAPIDO:
    P = dict(res=32, max_imagenes=60, demo_personajes=0, demo_por_personaje=0,
             rango=8, lr=1e-4, batch=2, pasos=4, val_cada=2, n_val_ruido=2,
             semillas=[0, 1], n_gen=3, pasos_inferencia=2)
elif LARGO:
    P = dict(res=512, max_imagenes=3000, demo_personajes=40,
             demo_por_personaje=15, rango=8, lr=1e-4, batch=4, pasos=1200,
             val_cada=100, n_val_ruido=16, semillas=[0, 1, 2, 3], n_gen=16,
             pasos_inferencia=30)
else:
    P = dict(res=512, max_imagenes=1000, demo_personajes=20,
             demo_por_personaje=10, rango=8, lr=1e-4, batch=4, pasos=400,
             val_cada=50, n_val_ruido=8, semillas=[0, 1], n_gen=8,
             pasos_inferencia=20)
display(pd.Series(P, name="valor").to_frame())

# Un color fijo por conjunto, como en los notebooks 1 y 2.
COLORES = {"train": "#1f77b4", "validation": "#ff7f0e", "test": "#2ca02c",
           "base": "#7f7f7f", "LoRA": "#9467bd"}


def semilla(s: int):
    """Fija las semillas de random, NumPy y PyTorch (CPU y GPU)."""
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)        # también siembra la GPU


semilla(0)
plt.style.use("default")
plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 80, "savefig.dpi": 80,
                     "axes.spines.top": False, "axes.spines.right": False})
try:                            # en Colab: figuras en JPEG, el notebook pesa menos
    from matplotlib_inline.backend_inline import set_matplotlib_formats
    set_matplotlib_formats("jpeg", pil_kwargs={"quality": 80})
except Exception:
    pass
