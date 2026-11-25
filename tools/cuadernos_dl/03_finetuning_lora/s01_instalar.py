# §1 · Instalar: MODO, RAPIDO, paquetes que falten, GPU, constantes y semillas.
# Define MODO, LARGO, RAPIDO, DEVICE, DTYPE, MODELO, MODELO_CLIP, DATASET,
# PROMPT, COLORES, semilla(s) y el diccionario P de tamaños por modo.

# %% [texto] s01-intro

# %% [codigo] s01-modo
MODO = "corto"   # "corto" (≈ 30 min en T4) o "largo" (≈ 75 min, todo lo ➕)
LARGO = MODO == "largo"

# Instala solo lo que falta; no actualiza lo que Colab ya trae.
import importlib.util
import subprocess
import sys

import torch

FALTAN = [p for p in ["diffusers", "peft", "accelerate", "transformers"]
          if importlib.util.find_spec(p) is None]
# bitsandbytes (4 bits, QLoRA) solo funciona con GPU de NVIDIA.
if torch.cuda.is_available() and importlib.util.find_spec("bitsandbytes") is None:
    FALTAN.append("bitsandbytes")
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
import diffusers
import peft
import transformers
import huggingface_hub

# RAPIDO=1: prueba local en CPU con un Stable Diffusion diminuto (segundos).
RAPIDO = os.environ.get("RAPIDO") == "1"
HAY_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if HAY_GPU and not RAPIDO else "cpu")
# fp16 en la GPU (la T4 no tiene bf16); fp32 en CPU.
DTYPE = torch.float16 if DEVICE.type == "cuda" else torch.float32

if not HAY_GPU and not RAPIDO:
    print("=" * 72)
    print("  ¡AVISO! ESTE ENTORNO NO TIENE GPU.")
    print("  Stable Diffusion en CPU tardaría horas. En Colab:")
    print("    Entorno de ejecución → Cambiar tipo de entorno → T4 GPU")
    print("    → Guardar, y luego Entorno de ejecución → Ejecutar todo.")
    print("=" * 72)

for nombre, mod in [("torch", torch), ("diffusers", diffusers),
                    ("peft", peft), ("transformers", transformers),
                    ("huggingface_hub", huggingface_hub)]:
    print(f"{nombre:16s}{mod.__version__}")
if importlib.util.find_spec("bitsandbytes") is not None:
    import bitsandbytes
    print(f"{'bitsandbytes':16s}{bitsandbytes.__version__}")
else:
    print(f"{'bitsandbytes':16s}— (sin GPU: QLoRA se saltará)")
print("DEVICE =", DEVICE, "· DTYPE =", DTYPE, "· RAPIDO =", RAPIDO)
if HAY_GPU:
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name} · {props.total_memory / 2**30:.1f} GiB")

# %% [texto] s01-constantes-explica

# %% [codigo] s01-constantes
# El modelo base y el modelo de CLIP que mide las imágenes.
if RAPIDO:
    MODELO = "hf-internal-testing/tiny-stable-diffusion-pipe"
    MODELO_CLIP = "hf-internal-testing/tiny-random-CLIPModel"
else:
    MODELO = "stable-diffusion-v1-5/stable-diffusion-v1-5"
    MODELO_CLIP = "openai/clip-vit-base-patch32"
DATASET = "ComputerVisionAnimeProject/AnimeFaceColorization"
PROMPT = "an anime face"      # el mismo caption para todas las caras

# Tamaños por modo. pasos = actualizaciones del UNet por corrida.
if RAPIDO:
    P = dict(n_personajes=4, n_por_personaje=4, res=32, batch=2, pasos=3,
             pasos_control=4, val_cada=1, n_val_ruido=2, semillas=[0, 1])
elif LARGO:
    P = dict(n_personajes=40, n_por_personaje=30, res=512, batch=4,
             pasos=400, pasos_control=800, val_cada=50, n_val_ruido=16,
             semillas=[0, 1, 2, 3, 4, 5])
else:
    P = dict(n_personajes=20, n_por_personaje=20, res=512, batch=4,
             pasos=150, pasos_control=300, val_cada=30, n_val_ruido=8,
             semillas=[0, 1, 2, 3])
display(pd.Series(P, name="valor").to_frame())

# Un color fijo por conjunto, igual que en el notebook 02.
COLORES = {"train": "#1f77b4", "validation": "#ff7f0e", "test": "#2ca02c"}


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
