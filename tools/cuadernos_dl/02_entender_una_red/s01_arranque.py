# §1 · Arranque: imports, GPU, versiones, semillas, estilo de gráficas, RAPIDO.

# %% [texto] s01-intro

# %% [codigo] s01-imports
# Todo lo que usa el notebook, importado una sola vez aquí.
import os
import time
import math
import hashlib
import subprocess
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torchvision

print("torch", torch.__version__, "· torchvision", torchvision.__version__)

# %% [texto] s01-gpu-explica

# %% [codigo] s01-gpu
# ¿Hay GPU? En Colab: Entorno de ejecución → Cambiar tipo de entorno → T4.
HAY_GPU = torch.cuda.is_available()

# RAPIDO recorta datos y epochs para una prueba en CPU que tarda segundos.
# Se activa solo si no hay GPU, o a mano con la variable de entorno RAPIDO=1.
RAPIDO = os.environ.get("RAPIDO") == "1" or not HAY_GPU

# Con RAPIDO trabajamos en CPU aunque haya GPU (la prueba local corre en CPU).
DEVICE = torch.device("cuda" if HAY_GPU and not RAPIDO else "cpu")
if DEVICE.type == "cpu":
    torch.set_num_threads(min(4, os.cpu_count() or 1))

if not HAY_GPU:
    print("=" * 72)
    print("  ¡AVISO! ESTE ENTORNO NO TIENE GPU.")
    print("  El notebook sigue en modo RAPIDO: pocos datos y pocas epochs,")
    print("  así que las gráficas NO se parecerán a las de la clase.")
    print("  Para corregirlo en Colab:")
    print("    Entorno de ejecución → Cambiar tipo de entorno → T4 GPU")
    print("    → Guardar, y luego Entorno de ejecución → Ejecutar todo.")
    print("=" * 72)

# nvidia-smi describe la GPU; si no existe el comando, no pasa nada.
try:
    salida = subprocess.run(["nvidia-smi"], capture_output=True, text=True,
                            timeout=20)
    print(salida.stdout if salida.returncode == 0 else "nvidia-smi no respondió")
except (FileNotFoundError, subprocess.TimeoutExpired):
    print("nvidia-smi no está disponible (no hay GPU de NVIDIA).")

print("DEVICE =", DEVICE, "· RAPIDO =", RAPIDO)
print("CUDA (con la que se compiló torch):", torch.version.cuda)
print("cuDNN:", torch.backends.cudnn.version() if HAY_GPU else "—")
if HAY_GPU:
    print("GPU:", torch.cuda.get_device_name(0))

# %% [texto] s01-semillas-explica

# %% [codigo] s01-semillas
# Semillas: misma semilla ⇒ mismos pesos iniciales y mismo orden de batches.
SEMILLA = 0
np.random.seed(SEMILLA)
torch.manual_seed(SEMILLA)  # también siembra la GPU

# Estilo de las gráficas: fondo claro y rejilla suave, como en el notebook 01.
plt.style.use("default")
plt.rcParams.update({
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 100,
    "savefig.dpi": 100,
    "figure.figsize": (7, 4),
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Un color fijo por conjunto, en todo el notebook.
COLORES = {"train": "#1f77b4", "validation": "#ff7f0e", "test": "#2ca02c"}
print("Colores:", COLORES)
