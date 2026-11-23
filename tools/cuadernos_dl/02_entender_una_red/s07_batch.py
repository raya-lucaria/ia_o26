# Sección 7 · Gradient descent y el tamaño del batch.
# Mismos 4096 ejemplos de train, SGD sin momentum, η = 0.03, mismas semillas:
# full-batch (gradient descent «normal»), batch 1 (stochastic), 8, 32, 128, 1024.
# Produce las corridas s07-b4096 (full-batch), s07-b1, s07-b8, s07-b32,
# s07-b128 y s07-b1024; el ruido del gradiente usa los pesos de s07-b128.

# %% [texto] s07-intro

# %% [texto] s07-apuesta

# %% [codigo] s07-presupuestos
import math
import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt

# Los mismos ejemplos de train para todas las corridas: solo cambia el batch.
IDX_S07 = subconjunto(512 if RAPIDO else 4096)   # estratificados y fijos
N_S07 = len(IDX_S07)                             # n: ejemplos de train
COMPLETO_S07 = 4096                      # la etiqueta del full-batch en los IDs
TAMANOS_S07 = [COMPLETO_S07, 1, 8, 32, 128, 1024]


def plan_s07(B):
    """Epochs y frecuencia de evaluación para un tamaño de batch B."""
    B = min(B, N_S07)                    # B = n es gradient descent full-batch
    por_epoch = math.ceil(N_S07 / B)     # actualizaciones de θ en una epoch
    if B == N_S07:
        epochs = 8 if RAPIDO else 80     # un paso por epoch: ~80 pasos
    elif B == 1:
        epochs = 1                       # n pasos ya son muchísimos
    else:
        epochs = 5
    # Evaluar a menudo: cada 8 pasos como máximo, para que TODAS las corridas
    # tengan puntos medidos dentro de los primeros 20 pasos (el presupuesto
    # común en pasos), y siempre al final de cada epoch. Evaluar no cuenta
    # en el reloj: `entrenar` para el cronómetro mientras mide.
    cada = 1 if por_epoch < 8 else min(8, por_epoch // 4)
    return B, por_epoch, epochs, cada


filas = []
for tam in TAMANOS_S07:
    B, por_epoch, epochs, cada = plan_s07(tam)
    filas.append({"ID": f"s07-b{tam}", "batch": B, "pasos por epoch": por_epoch,
                  "epochs": epochs, "pasos totales": por_epoch * epochs,
                  "ejemplos vistos": B * por_epoch * epochs,
                  "evaluar cada (pasos)": cada})
display(pd.DataFrame(filas).set_index("ID"))

# %% [codigo] s07-entrenar
# Una corrida por tamaño de batch. Todo lo demás es idéntico: los mismos
# pesos iniciales (semilla_init) y el mismo orden de barajar (semilla_orden).
for tam in TAMANOS_S07:
    B, por_epoch, epochs, cada = plan_s07(tam)
    cfg = Config(id=f"s07-b{tam}", seccion=7,
                 capas=[784, 128, 10], activacion="relu",
                 optimizer="sgd", lr=0.03,          # SGD sin momentum
                 batch=B, epochs=epochs, eval_cada_pasos=cada,
                 idx_train=IDX_S07, datos="4k-limpio",
                 semilla_init=SEMILLA, semilla_orden=SEMILLA)
    entrenar(cfg)       # imprime una línea por corrida y la guarda en CORRIDAS

CORRIDAS_S07 = {tam: CORRIDAS[f"s07-b{tam}"] for tam in TAMANOS_S07}

# %% [texto] s07-ejes

# %% [codigo] s07-cuatro-ejes
# Un color por tamaño de batch (del más chico, oscuro, al más grande, claro);
# full-batch en negro y punteado. Graficamos solo la loss de validation.
PALETA_S07 = plt.cm.viridis(np.linspace(0.0, 0.85, len(TAMANOS_S07) - 1))
ESTILO_S07 = {COMPLETO_S07: dict(color="black", ls="--", label="full-batch")}
for color, tam in zip(PALETA_S07, TAMANOS_S07[1:]):
    ESTILO_S07[tam] = dict(color=color, ls="-", label=f"batch {tam}")


def eje_x_s07(h, eje):
    """La columna del historial que va en x; «epochs» puede ser fraccionaria."""
    return h["ejemplos"] / N_S07 if eje == "epochs" else h[eje]


def al_presupuesto_s07(h, eje, tope):
    """La última evaluación con x <= tope: lo que la corrida midió a ese
    presupuesto (o un poco antes, si no evaluó justo en tope)."""
    return h.loc[eje_x_s07(h, eje) <= tope * (1 + 1e-9)].iloc[-1]


EJES_S07 = {"epochs": "epochs (pasadas por los ejemplos de train)",
            "pasos": "pasos (actualizaciones de θ)",
            "ejemplos": "ejemplos vistos",
            "segundos": "segundos de entrenamiento"}
PRESUPUESTO_S07 = {}

fig, ejes = plt.subplots(2, 2, figsize=(12, 8.5), sharey=True)
for ax, (eje, etiqueta) in zip(ejes.flat, EJES_S07.items()):
    for tam, corrida in CORRIDAS_S07.items():
        h = corrida.historial
        x, y = eje_x_s07(h, eje), h["loss_validation"]
        ok = (x > 0) & np.isfinite(y)           # el 0 no cabe en escala log
        marca = "o" if ok.sum() <= 100 else None   # muchos puntos: solo línea
        ax.plot(x[ok], y[ok], marker=marca, ms=3, lw=1.4, **ESTILO_S07[tam])
    # El presupuesto común: hasta dónde llegaron TODAS las corridas.
    tope = min(eje_x_s07(c.historial, eje).max() for c in CORRIDAS_S07.values())
    PRESUPUESTO_S07[eje] = tope
    ax.axvline(tope, color="gray", ls=":", lw=1.5)
    for tam, corrida in CORRIDAS_S07.items():   # ★ = el punto comparable
        f = al_presupuesto_s07(corrida.historial, eje, tope)
        fx = f["ejemplos"] / N_S07 if eje == "epochs" else f[eje]
        if fx > 0:
            ax.plot(fx, f["loss_validation"], marker="*", ms=13, ls="none",
                    mec="black", color=ESTILO_S07[tam]["color"])
    ax.axvspan(ax.get_xlim()[0], tope, color="gray", alpha=0.08)
    ax.set_xscale("log")
    ax.set_ylim(0, 3)          # los picos de batch 1 pueden salirse por arriba
    ax.set_xlabel(etiqueta + " (escala log)")
    ax.set_title(f"contra {eje}: ★ = medido en el presupuesto común")
for ax in ejes[:, 0]:
    ax.set_ylabel("loss de validation")
ejes[0, 0].axhline(math.log(10), color="gray", lw=1)   # adivinar uniforme
ejes[0, 0].legend(fontsize=9)
fig.suptitle("La misma familia de corridas contra cuatro ejes distintos")
fig.tight_layout()
plt.show()
for eje, tope in PRESUPUESTO_S07.items():
    print(f"presupuesto común en {eje}: {tope:,.4g}")

# %% [texto] s07-justa

# %% [codigo] s07-tabla
# «tras 1 epoch»: todas vieron los mismos n ejemplos, una vez cada uno.
filas = []
for tam, corrida in CORRIDAS_S07.items():
    h, final = corrida.historial, corrida.historial.iloc[-1]
    una_epoch = al_presupuesto_s07(h, "ejemplos", N_S07)
    completa = final["ejemplos"] >= N_S07     # con RAPIDO puede no llegar
    filas.append({
        "batch": "full-batch" if tam == COMPLETO_S07 else tam,
        "epochs": round(final["ejemplos"] / N_S07, 2),
        "pasos": int(final["pasos"]),
        "ejemplos": int(final["ejemplos"]),
        "segundos": round(final["segundos"], 2),
        "loss val tras 1 epoch": (round(una_epoch["loss_validation"], 3)
                                  if completa else "sin completar"),
        "loss val al final": round(final["loss_validation"], 3),
        "acc val al final": round(final["acc_validation"], 3),
    })
TABLA_S07 = pd.DataFrame(filas).set_index("batch")
display(TABLA_S07)
if RAPIDO:
    print("Modo RAPIDO: las corridas se cortaron a unos pocos pasos y con "
          f"n = {N_S07} el batch 1024 ya es full-batch; esta tabla solo prueba "
          "que el código corre, no compara nada.")

# %% [plegada] s07-apuesta-respuesta

# %% [texto] s07-ruido-idea

# %% [codigo] s07-ruido
# El ruido del gradiente con los pesos CONGELADOS: nada se entrena aquí.
X_S07, Y_S07 = (t[IDX_S07.to(t.device)] for t in DATOS["estandar"]["train"])
PERDIDA_S07 = nn.CrossEntropyLoss()       # promedio sobre el batch


def gradiente_s07(modelo, X, y):
    """∇L_𝓑(θ) de todas las capas, aplanado en un solo vector."""
    modelo.zero_grad(set_to_none=True)
    PERDIDA_S07(modelo(X), y).backward()
    return torch.cat([p.grad.reshape(-1) for p in modelo.parameters()])


def ruido_s07(modelo, tamanos, repeticiones=32, semilla=SEMILLA):
    """Promedio de ‖g_𝓑 − g_completo‖² sobre `repeticiones` batches por B."""
    modelo.eval()
    g_completo = gradiente_s07(modelo, X_S07, Y_S07)   # el de gradient descent
    azar = torch.Generator().manual_seed(semilla)
    filas = []
    for B in tamanos:
        d2 = []
        for _ in range(repeticiones):
            lote = torch.randperm(len(Y_S07), generator=azar)[:B]
            lote = lote.to(X_S07.device)                # sin reemplazo
            g_B = gradiente_s07(modelo, X_S07[lote], Y_S07[lote])
            d2.append(((g_B - g_completo) ** 2).sum().item())
        filas.append({"B": B, "ruido": float(np.mean(d2)),
                      "error estándar": float(np.std(d2) / math.sqrt(len(d2)))})
    modelo.zero_grad(set_to_none=True)
    return pd.DataFrame(filas), float((g_completo ** 2).sum())


TAMANOS_RUIDO_S07 = [B for B in (1, 8, 32, 128, 1024) if B < N_S07]
REPETICIONES_S07 = 8 if RAPIDO else 32

torch.manual_seed(SEMILLA)                 # la misma red recién inicializada
red_inicial = construir_red([784, 128, 10], "relu").to(DEVICE)
red_entrenada = cargar(CORRIDAS["s07-b128"], "ultima")   # tras sus 5 epochs
RUIDO_S07 = {}
for nombre, red in [("recién inicializada", red_inicial),
                    ("entrenada (s07-b128)", red_entrenada)]:
    tabla, senal = ruido_s07(red, TAMANOS_RUIDO_S07, REPETICIONES_S07)
    tabla["ruido / ‖g_completo‖²"] = tabla["ruido"] / senal
    RUIDO_S07[nombre] = tabla
    print(f"{nombre}: ‖g_completo‖² = {senal:.4g}")
    display(tabla.set_index("B").round(4))
del red_inicial, red_entrenada

# %% [codigo] s07-ruido-grafica
fig, ax = plt.subplots(figsize=(7.5, 5))
B = np.array(TAMANOS_RUIDO_S07, dtype=float)
for (nombre, tabla), marca in zip(RUIDO_S07.items(), ["o", "s"]):
    ax.errorbar(tabla["B"], tabla["ruido"], yerr=tabla["error estándar"],
                marker=marca, capsize=3, lw=1.8, label=nombre)
    # La recta 1/B anclada en la mediana de B·ruido: en log-log, pendiente −1.
    c = float(np.median(tabla["B"] * tabla["ruido"]))
    ax.plot(B, c / B, color="gray", ls="--", lw=1)
    # Con muestreo SIN reemplazo de n ejemplos el ruido cae un poco más:
    # se multiplica por (n − B)/(n − 1), que ya pesa en B = 1024.
    ax.plot(B, c / B * (N_S07 - B) / (N_S07 - 1), color="gray", ls=":", lw=1)
ax.plot([], [], color="gray", ls="--", label="referencia ∝ 1/B")
ax.plot([], [], color="gray", ls=":", label="1/B × (n − B)/(n − 1)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("tamaño del batch B (escala log)")
ax.set_ylabel(r"$\mathbb{E}\,\|g_{\mathcal{B}} - g_{\mathrm{completo}}\|^2$"
              "  (escala log)")
ax.set_title(f"Ruido del gradiente: promedio de {REPETICIONES_S07} batches por B")
ax.legend(fontsize=9)
fig.tight_layout()
plt.show()

# %% [texto] s07-que-viste
