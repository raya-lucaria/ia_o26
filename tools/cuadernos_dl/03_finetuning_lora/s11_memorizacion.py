# Notebook 03 · §11 · Memorización.
# Produce la corrida "control" (Corrida("control", datos="control"): pocas
# caras y muchos pasos, para que SÍ memorice). Consume "lora_r8" de s07.
# Mide el vecino más cercano en train con dos cosenos (CLIP y píxeles 64×64)
# para: base, lora_r8, control y caras reales de validation.

# %% [texto] s11-intro

# %% [codigo] s11-control
# El control: CONTROL (pocas caras de train), P["pasos_control"] pasos.
CTRL_S11 = entrenar(Corrida("control", datos="control"))
if CTRL_S11.error:
    print(f"control falló: {CTRL_S11.error}")
print(f"control: {len(CONTROL)} caras, {CTRL_S11.pasos or P['pasos_control']} "
      f"pasos; lora_r8: {len(DATOS['train'])} caras, "
      f"{CORRIDAS['lora_r8'].pasos or P['pasos']} pasos")
curvas(["lora_r8", "control"], "train vs validation: lora_r8 y el control")

# %% [codigo] s11-vecinos
import numpy as np
import pandas as pd
import torch


def pixeles_64(imagenes):
    """Vectores de píxeles 64×64 centrados (sin su media) y de norma 1."""
    x = np.stack([np.asarray(im.convert("RGB").resize((64, 64)), np.float32)
                  .ravel() for im in imagenes])
    x -= x.mean(axis=1, keepdims=True)
    return x / (np.linalg.norm(x, axis=1, keepdims=True) + 1e-8)


def vecino(consulta, referencia):
    """Para cada fila de `consulta`: (coseno máximo, índice) en `referencia`."""
    sim = torch.as_tensor(consulta) @ torch.as_tensor(referencia).T
    mejor, idx = sim.max(dim=1)
    return mejor.float().numpy(), idx.numpy()


# Las mismas semillas para los tres modelos; ninguna es de P["semillas"].
N_S11 = 2 if RAPIDO else (16 if LARGO else 8)
SEM_S11 = list(range(100, 100 + N_S11))
GRUPOS_S11 = {"base": generar(None, PROMPT, SEM_S11),
              "lora_r8": generar("lora_r8", PROMPT, SEM_S11),
              "control": generar("control", PROMPT, SEM_S11),
              "validation (reales)": DATOS["validation"]}

TRAIN_CLIP = embeddings_clip(DATOS["train"]).float().cpu()
TRAIN_PIX = pixeles_64(DATOS["train"])
NN_S11 = {}
for grupo, imgs in GRUPOS_S11.items():
    c, ic = vecino(embeddings_clip(imgs).float().cpu(), TRAIN_CLIP)
    p, ip = vecino(pixeles_64(imgs), TRAIN_PIX)
    NN_S11[grupo] = {"clip": c, "idx_clip": ic, "pix": p, "idx_pix": ip}

display(pd.DataFrame({g: {"n": len(v["clip"]),
                          "CLIP mediana": np.median(v["clip"]),
                          "CLIP máx": v["clip"].max(),
                          "píxeles mediana": np.median(v["pix"]),
                          "píxeles máx": v["pix"].max()}
                      for g, v in NN_S11.items()}).T.round(3))

# %% [texto] s11-como-leer

# %% [codigo] s11-grafica
import matplotlib.pyplot as plt

COLOR_S11 = {"base": "#7f7f7f", "lora_r8": "#9467bd", "control": "#d62728",
             "validation (reales)": COLORES["validation"]}
fig, ejes = plt.subplots(1, 2, figsize=(10, 3.8))
rng_s11 = np.random.default_rng(0)
for ax, medida, nombre in zip(ejes, ["clip", "pix"],
                              ["coseno CLIP (parecido)", "coseno de píxeles (copia)"]):
    datos = [NN_S11[g][medida] for g in GRUPOS_S11]
    ax.boxplot(datos, showfliers=False, widths=0.5)
    for i, (g, d) in enumerate(zip(GRUPOS_S11, datos), start=1):
        x = i + rng_s11.uniform(-0.15, 0.15, len(d))
        ax.scatter(x, d, s=12, color=COLOR_S11[g], alpha=0.8, zorder=3)
    ax.set_xticks(range(1, len(GRUPOS_S11) + 1), list(GRUPOS_S11), fontsize=8)
    ax.set(title=f"vecino más cercano en train: {nombre}",
           ylabel="coseno máximo contra train")
plt.tight_layout()
plt.show()

# %% [codigo] s11-pares
# Las 4 imágenes del control más parecidas en píxeles a una cara de train,
# arriba; su vecino más cercano en train, abajo.
v = NN_S11["control"]
orden = np.argsort(-v["pix"])[:4]
gen_ctrl = [GRUPOS_S11["control"][i] for i in orden]
vec_ctrl = [DATOS["train"][v["idx_pix"][i]] for i in orden]
malla(gen_ctrl + vec_ctrl, filas=2,
      titulo="control: generada (arriba) ↔ vecino en train (abajo)",
      etiquetas=[f"píx {v['pix'][i]:.2f} · CLIP {v['clip'][i]:.2f}"
                 for i in orden] + ["vecino en train"] * len(orden))

# %% [texto] s11-que-viste
