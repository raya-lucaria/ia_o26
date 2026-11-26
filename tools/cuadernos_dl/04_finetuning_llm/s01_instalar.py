# §1 · Instalar: MODO, RAPIDO, paquetes que falten, GPU, constantes y semillas.
# Define MODO, LARGO, RAPIDO, DEVICE, DTYPE, AMP, CUDA, MODELO, DEMO, P, COLORES,
# semilla(s) y mostrar(df).

# %% [texto] s01-intro

# %% [codigo] s01-modo
MODO = "corto"   # "corto" (≈ 20–25 min en T4) o "largo" (≈ 45–60 min)
LARGO = MODO == "largo"

# Instala solo lo que falta; no actualiza lo que Colab ya trae.
import importlib.util
import subprocess
import sys

FALTAN = [p for p in ["transformers", "peft", "accelerate", "safetensors"]
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
import peft
import transformers
import huggingface_hub

# RAPIDO=1: prueba local en CPU con un Qwen diminuto (segundos).
RAPIDO = os.environ.get("RAPIDO") == "1"
HAY_GPU = torch.cuda.is_available()
DEVICE = torch.device("cuda" if HAY_GPU and not RAPIDO else "cpu")
CUDA = DEVICE.type == "cuda"
# Qwen se entrenó en bf16, que la T4 no tiene, y en fp16 puede desbordarse.
# Corto: el 0.5B en fp32 (≈ 2 GB, cabe). Largo: el 1.5B en fp16 con
# autocast + GradScaler (AMP), porque en fp32 apretaría la memoria.
DTYPE = torch.float16 if CUDA and LARGO else torch.float32
AMP = DTYPE == torch.float16

if not HAY_GPU and not RAPIDO:
    print("=" * 72)
    print("  ¡AVISO! ESTE ENTORNO NO TIENE GPU.")
    print("  Entrenar un LLM en CPU tardaría horas. En Colab:")
    print("    Entorno de ejecución → Cambiar tipo de entorno → T4 GPU")
    print("    → Guardar, y luego Entorno de ejecución → Ejecutar todo.")
    print("=" * 72)

for nombre, mod in [("torch", torch), ("transformers", transformers),
                    ("peft", peft), ("huggingface_hub", huggingface_hub)]:
    print(f"{nombre:16s}{mod.__version__}")
print("DEVICE =", DEVICE, "· DTYPE =", DTYPE, "· AMP =", AMP,
      "· RAPIDO =", RAPIDO)
if HAY_GPU:
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name} · {props.total_memory / 2**30:.1f} GiB")

# %% [texto] s01-constantes-explica

# %% [codigo] s01-constantes
# El modelo base. Los dos Qwen2.5-Instruct son Apache-2.0.
if RAPIDO:
    MODELO = "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5"
elif LARGO:
    MODELO = "Qwen/Qwen2.5-1.5B-Instruct"
else:
    MODELO = "Qwen/Qwen2.5-0.5B-Instruct"
DEMO = "b-mc2/sql-create-context"     # el dataset del demo (CC BY 4.0)

# Tamaños por modo. pasos = actualizaciones del adaptador; cada paso ve
# batch × acum ejemplos.
ATENCION = ["q_proj", "k_proj", "v_proj", "o_proj"]
if RAPIDO:
    P = dict(n_demo=200, max_len=128, batch=2, acum=1, pasos=6, lr=2e-4,
             val_cada=3, n_val_loss=8, n_eval=4,
             rango=8, alfa=16, modulos=ATENCION)
elif LARGO:
    P = dict(n_demo=3000, max_len=512, batch=4, acum=2, pasos=800, lr=2e-4,
             val_cada=50, n_val_loss=200, n_eval=150,
             rango=8, alfa=16, modulos=ATENCION)
else:
    P = dict(n_demo=1000, max_len=512, batch=4, acum=2, pasos=300, lr=2e-4,
             val_cada=25, n_val_loss=100, n_eval=100,
             rango=8, alfa=16, modulos=ATENCION)
if LARGO:                               # ➕ LoRA también en el MLP
    P["modulos"] = ATENCION + ["gate_proj", "up_proj", "down_proj"]
display(pd.Series({k: str(v) for k, v in P.items()}, name="valor").to_frame())

# Un color fijo por conjunto, igual que en los notebooks 2 y 3.
COLORES = {"train": "#1f77b4", "validation": "#ff7f0e", "test": "#2ca02c"}


def semilla(s: int):
    """Fija las semillas de random, NumPy y PyTorch (CPU y GPU)."""
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)        # también siembra la GPU


def mostrar(df):
    """Una tabla de texto: celdas alineadas a la izquierda y con saltos."""
    try:
        display(df.style.set_properties(
            **{"text-align": "left", "white-space": "pre-wrap"}))
    except Exception:           # sin jinja2 o fuera de Jupyter
        with pd.option_context("display.max_colwidth", 80):
            display(df)


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
