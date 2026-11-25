# Notebook 03 · §10 · Cuánto cambia el modelo.
# SVD de ΔW = (α/r)·B·A de la corrida "lora_r8" (➕ también "lora_r64"):
# valores singulares normalizados de 3 capas y rango efectivo al 90 % de la
# energía. Después, la perilla λ ∈ {0, 0.5, 1, 1.5} y la prueba de que λ = 0
# es el modelo base. Consume "lora_r8" y "lora_r64" de s07; no entrena nada.

# %% [texto] s10-intro

# %% [codigo] s10-svd
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt


def espectro_s10(nombre):
    """Valores singulares de cada ΔW = (α/r)·B·A sin armar ΔW: con B = Q_B R_B
    y Aᵀ = Q_A R_A (QR reducidas), ΔW = (α/r)·Q_B (R_B R_Aᵀ) Q_Aᵀ, y los
    σ de ΔW son los de la matriz chica r×r R_B R_Aᵀ, por |α/r|."""
    c = CORRIDAS[nombre]
    estado, s = load_file(c.ruta), abs(c.alfa / c.rango)
    salida = {}
    for k in sorted(estado):
        if k.endswith(".lora_A.weight"):
            capa = k[: -len(".lora_A.weight")]
            A = estado[k].float().reshape(estado[k].shape[0], -1)   # [r, d_in]
            B = estado[capa + ".lora_B.weight"].float()             # [d_out, r]
            B = B.reshape(B.shape[0], -1)
            R_B = torch.linalg.qr(B, mode="reduced").R               # [r, r]
            R_A = torch.linalg.qr(A.T, mode="reduced").R             # [r, r]
            salida[capa] = (torch.linalg.svdvals(R_B @ R_A.T) * s).numpy()
    return salida

# %% [codigo] s10-svd-rango
def rango_efectivo(s, energia=0.9):
    """El k más chico cuya energía acumulada, con σ², llega a `energia`."""
    acumulada = np.cumsum(s ** 2) / max(float(np.sum(s ** 2)), 1e-30)
    return int(np.searchsorted(acumulada, energia) + 1)


def tres_capas(capas):
    """Una capa de down_blocks, una de mid_block y una de up_blocks."""
    elegidas = []
    for bloque in ("down_blocks", "mid_block", "up_blocks"):
        c = next((c for c in capas if bloque in c and c not in elegidas), None)
        if c is not None:
            elegidas.append(c)
    for c in (capas[0], capas[len(capas) // 2], capas[-1]):  # por si acaso
        if len(elegidas) < 3 and c not in elegidas:
            elegidas.append(c)
    return elegidas


def resumen_s10(nombre):
    """Grafica σ_i/σ_1 de 3 capas e imprime el rango efectivo de todas."""
    c = CORRIDAS.get(nombre)
    if c is None or c.error:
        print(f"{nombre}: no hay adaptador ({c.error if c else 'no entrenado'})")
        return
    esp = espectro_s10(nombre)
    capas = tres_capas(list(esp))
    fig, ax = plt.subplots(figsize=(7, 3.5))
    for capa in capas:
        s = esp[capa][: 2 * c.rango + 4]
        ax.semilogy(np.arange(1, len(s) + 1), np.maximum(s / s[0], 1e-8),
                    "o-", ms=3, label=capa.replace(".processor", "")[-45:])
    ax.axvline(c.rango, color="gray", ls="--", lw=1)
    ax.text(c.rango, 1e-7, f"  r = {c.rango}", color="gray")
    ax.set(xlabel="índice i", ylabel="σ_i / σ_1", ylim=(1e-8, 2),
           title=f"{nombre}: espectro de ΔW en 3 capas")
    ax.legend(fontsize=7)
    plt.show()
    rangos = pd.Series({k: rango_efectivo(s) for k, s in esp.items()})
    display(pd.DataFrame({"σ_1": [esp[k][0] for k in capas],
                          "rango efectivo 90 %": [rangos[k] for k in capas]},
                         index=capas).round(5))
    print(f"{nombre}: {len(rangos)} capas adaptadas, r = {c.rango}; rango "
          f"efectivo mediano {rangos.median():.0f} (mín {rangos.min()}, "
          f"máx {rangos.max()})")


resumen_s10("lora_r8")

# %% [codigo] s10-svd-r64
# ➕ El mismo análisis con r = 64: ¿usa el adaptador todo el rango que tiene?
if LARGO:
    resumen_s10("lora_r64")
else:
    print("(solo en MODO largo)")

# %% [texto] s10-perilla

# %% [codigo] s10-lambda
# Mismas semillas en cada fila: lo único que cambia es λ.
LAMBDAS_S10 = [0.0, 0.5, 1.0, 1.5]
SEM_S10 = P["semillas"][:4]
imgs_s10 = []
for lam in LAMBDAS_S10:
    imgs_s10 += generar("lora_r8", PROMPT, SEM_S10, escala=lam)
malla(imgs_s10, filas=len(LAMBDAS_S10),
      titulo=f"lora_r8 con λ = {LAMBDAS_S10} (filas), «{PROMPT}»",
      etiquetas=[f"λ={lam} · s{s}" for lam in LAMBDAS_S10 for s in SEM_S10])

# λ = 0 contra el modelo base, píxel por píxel (escala 0–255).
base_s10 = generar(None, PROMPT, SEM_S10)
dif_s10 = [np.abs(np.asarray(a, np.float32) - np.asarray(b, np.float32))
           for a, b in zip(imgs_s10[: len(SEM_S10)], base_s10)]
print("λ = 0 vs base: diferencia media de píxeles "
      f"{np.mean([d.mean() for d in dif_s10]):.3f}, máxima "
      f"{max(d.max() for d in dif_s10):.0f} (de 255)")

# %% [texto] s10-que-viste
