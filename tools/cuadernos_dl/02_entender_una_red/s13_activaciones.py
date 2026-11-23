# Sección 13 · Activaciones.
# Produce las corridas s13-relu, s13-sigmoide, s13-tanh y s13-gelu
# (config_profunda: 6 ocultas de 128, SGD 0.03, init ortogonal, sesgos 0,
# medir_por_paso=True). Publica: ACTIVACIONES_S13, CORRIDAS_S13,
# REDES_INICIALES_S13, DIAG_S13. Consume la caja (s01–s03).

# %% [texto] s13-intro

# %% [codigo] s13-funciones
# Las cuatro activaciones g(z) y sus derivadas g'(z). Las derivadas NO las
# escribimos a mano: se las pedimos a autograd, el mismo mecanismo que hace
# backpropagation en todo el notebook.
import math
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn
import matplotlib.pyplot as plt

ACTIVACIONES_S13 = ["relu", "sigmoide", "tanh", "gelu"]
FUNCIONES_S13 = {"relu": F.relu, "sigmoide": torch.sigmoid,
                 "tanh": torch.tanh, "gelu": F.gelu}
# Un color por activación (no usamos azul/naranja/verde: son train/val/test).
COLOR_ACT_S13 = {"relu": "#d62728", "sigmoide": "#9467bd",
                 "tanh": "#8c564b", "gelu": "#e377c2"}

z = torch.linspace(-6, 6, 1201, requires_grad=True)
fig, ejes = plt.subplots(2, 4, figsize=(15, 6), sharex=True)
for col, nombre in enumerate(ACTIVACIONES_S13):
    g = FUNCIONES_S13[nombre](z)
    (derivada,) = torch.autograd.grad(g.sum(), z)  # g'(z) en cada punto
    zz, gg, dd = z.detach().numpy(), g.detach().numpy(), derivada.numpy()
    color = COLOR_ACT_S13[nombre]
    ejes[0, col].plot(zz, gg, color=color, lw=2)
    ejes[0, col].set_title(f"{nombre}: g(z)")
    ejes[1, col].plot(zz, dd, color=color, lw=2)
    ejes[1, col].set_title(f"{nombre}: g'(z)   (máx ≈ {dd.max():.3f})")
    ejes[1, col].set_xlabel("preactivación z")
    ejes[1, col].set_ylim(-0.15, 1.25)
    for fila in range(2):
        ejes[fila, col].axhline(0, color="gray", lw=0.8)
        ejes[fila, col].axvline(0, color="gray", lw=0.8)
# La cota analítica de la sigmoide: σ'(z) = σ(z)(1 − σ(z)) ≤ 1/4, en z = 0.
ejes[1, 1].axhline(0.25, color="black", ls="--", lw=1, label="¼")
ejes[1, 1].legend(loc="upper right")
ejes[0, 0].set_ylabel("g(z)")
ejes[1, 0].set_ylabel("g'(z)")
fig.suptitle("Las cuatro activaciones (arriba) y sus derivadas (abajo)")
plt.tight_layout()
plt.show()

for nombre in ACTIVACIONES_S13:
    zg = torch.linspace(-6, 6, 1201, requires_grad=True)
    (d,) = torch.autograd.grad(FUNCIONES_S13[nombre](zg).sum(), zg)
    print(f"{nombre:9s} máx g'(z) en [-6, 6] = {d.max().item():.4f}")
print("sigmoide: cota analítica ¼ =", 0.25)

# %% [texto] s13-derivadas-lectura

# %% [texto] s13-atenuacion

# %% [texto] s13-apuesta

# %% [codigo] s13-red-inicial
# Cuatro redes iguales salvo la activación: 784 → 6 × 128 → 10, pesos
# ortogonales y sesgos en cero. Con la misma semilla, los pesos iniciales
# son los mismos en las cuatro: así la única diferencia es g.
REDES_INICIALES_S13 = {}
for nombre in ACTIVACIONES_S13:
    cfg = config_profunda(nombre)
    torch.manual_seed(cfg.semilla_init)
    REDES_INICIALES_S13[nombre] = construir_red(
        cfg.capas, activacion=cfg.activacion, init=cfg.init).to(DEVICE)

CAPAS_S13 = config_profunda("relu").capas
print("capas:", CAPAS_S13)
print(REDES_INICIALES_S13["sigmoide"])


def lineales(red):
    """Las capas nn.Linear de la red, en orden: W^(1), …, W^(L)."""
    return [m for m in red.modules() if isinstance(m, nn.Linear)]


ref = lineales(REDES_INICIALES_S13["relu"])
for nombre in ACTIVACIONES_S13[1:]:
    otras = lineales(REDES_INICIALES_S13[nombre])
    iguales = all(torch.equal(a.weight, b.weight) for a, b in zip(ref, otras))
    print(f"¿pesos iniciales de {nombre} == los de relu? {iguales}")
print("sesgos iniciales en cero:",
      all(bool((m.bias == 0).all()) for m in ref))
# Norma espectral de cada W: con init ortogonal de ganancia 1 vale 1. Las
# filas son ortonormales, así que W transpuesta (la que usa backpropagation)
# conserva la norma de cualquier vector; W en sí nunca estira.
print("‖W^(l)‖₂ por capa:",
      [round(torch.linalg.matrix_norm(m.weight.detach(), ord=2).item(), 3)
       for m in ref])

dibujar_red(CAPAS_S13, titulo="La red profunda de §13–§15: 6 ocultas de 128")
plt.show()

# %% [texto] s13-gradiente-texto

# %% [codigo] s13-gradiente-inicial
# Un batch FIJO de train (las mismas imágenes para las cuatro redes).
X_tr, y_tr = DATOS[config_profunda("relu").escala]["train"]
gen = torch.Generator().manual_seed(SEMILLA)
N_BATCH_S13 = 128 if RAPIDO else 512
idx = torch.randperm(len(y_tr), generator=gen)[:N_BATCH_S13].to(DEVICE)
xb, yb = X_tr[idx], y_tr[idx]


def recorrer(red, x):
    """Forward capa por capa. Guarda cada preactivación z^(l) (salida de una
    Linear) y cada activación a^(l) = g(z^(l)) (salida de la no linealidad)."""
    zs, activaciones = [], []
    for modulo in red:
        x = modulo(x)
        if isinstance(modulo, nn.Linear):
            if x.requires_grad:        # (dentro de no_grad no hay gradiente)
                x.retain_grad()        # queremos δ^(l) = ∂L/∂z^(l) al final
            zs.append(x)
        elif not isinstance(modulo, (nn.Dropout, nn.BatchNorm1d, nn.Identity)):
            activaciones.append(x)
    return x, zs, activaciones


filas = []
for nombre, red in REDES_INICIALES_S13.items():
    red.eval()                          # sin dropout ni BN: no cambia nada
    red.zero_grad()
    logits, zs, _ = recorrer(red, xb)
    perdida = nn.functional.cross_entropy(logits, yb)
    perdida.backward()                  # backpropagation: la regla de la cadena
    for l, (lin, z_l) in enumerate(zip(lineales(red), zs), start=1):
        filas.append({"activacion": nombre, "capa": l,
                      "norma_grad_W": lin.weight.grad.norm().item(),
                      "norma_delta": z_l.grad.norm().item()})
    red.zero_grad()                     # no dejamos gradientes colgados
DIAG_S13 = pd.DataFrame(filas)
tabla = DIAG_S13.pivot(index="capa", columns="activacion",
                       values="norma_grad_W")[ACTIVACIONES_S13]
print("‖∇_W^(l) L‖ antes del primer paso (filas = capa l, "
      "columnas = activación):")
display(tabla.map(lambda v: f"{v:.2e}"))

# %% [codigo] s13-grafica-gradiente
# Barras agrupadas: una por capa, una serie por activación, eje y en log.
n_capas = DIAG_S13["capa"].max()
ancho = 0.2
fig, (ax_w, ax_d) = plt.subplots(1, 2, figsize=(15, 4.8))
for k, nombre in enumerate(ACTIVACIONES_S13):
    d = DIAG_S13[DIAG_S13["activacion"] == nombre]
    pos = d["capa"] + (k - 1.5) * ancho
    ax_w.bar(pos, d["norma_grad_W"], ancho, color=COLOR_ACT_S13[nombre],
             label=nombre)
    ax_d.bar(pos, d["norma_delta"], ancho, color=COLOR_ACT_S13[nombre],
             label=nombre)

# La cota de la sigmoide sobre δ: cada capa oculta multiplica por ≤ ¼ y por
# ‖W‖₂ (≈ 1 con init ortogonal). Se parte del δ real de la salida.
sig = DIAG_S13[DIAG_S13["activacion"] == "sigmoide"].set_index("capa")
normas_W = [torch.linalg.matrix_norm(m.weight.detach(), ord=2).item()
            for m in lineales(REDES_INICIALES_S13["sigmoide"])]
cota = {n_capas: sig.loc[n_capas, "norma_delta"]}
for l in range(n_capas - 1, 0, -1):
    cota[l] = cota[l + 1] * normas_W[l] * 0.25   # normas_W[l] es W^(l+1)
capas_cota = sorted(cota)
ax_d.plot(capas_cota, [cota[l] for l in capas_cota], "k--", marker="o",
          label="cota sigmoide: × ¼ por capa")

for ax, titulo in [(ax_w, "‖∇ de W^(l)‖ al inicio"),
                   (ax_d, "‖δ^(l)‖ = ‖∂L/∂z^(l)‖ al inicio")]:
    ax.set_yscale("log")
    ax.set_xticks(range(1, n_capas + 1))
    ax.set_xlabel("capa l   (1 = junto a la entrada, "
                  f"{n_capas} = la de salida)")
    ax.set_ylabel("norma (escala log)")
    ax.set_title(titulo)
    ax.legend(fontsize=8)
plt.tight_layout()
plt.show()

for nombre in ACTIVACIONES_S13:
    d = DIAG_S13[DIAG_S13["activacion"] == nombre].set_index("capa")
    r = d.loc[1, "norma_delta"] / d.loc[n_capas, "norma_delta"]
    print(f"{nombre:9s} ‖δ^(1)‖ / ‖δ^({n_capas})‖ = {r:.2e}")
print(f"cota analítica de la sigmoide: (¼)^6 = {0.25 ** 6:.2e} "
      f"(× ∏‖W‖₂ = {math.prod(normas_W[1:]):.3f})")

# %% [texto] s13-lee-gradiente

# %% [codigo] s13-histogramas
# Las activaciones a^(l) de cada capa oculta, con la red recién creada y el
# mismo batch fijo. Filas = activación, columnas = capa oculta l = 1…6.
with torch.no_grad():
    salidas = {n: recorrer(r, xb)[2] for n, r in REDES_INICIALES_S13.items()}
n_ocultas = len(salidas["relu"])
fig, ejes = plt.subplots(len(ACTIVACIONES_S13), n_ocultas,
                         figsize=(2.4 * n_ocultas, 8), sharex="row")
for i, nombre in enumerate(ACTIVACIONES_S13):
    for l, a in enumerate(salidas[nombre], start=1):
        ax = ejes[i, l - 1]
        valores = a.flatten().cpu().numpy()
        ax.hist(valores, bins=40, color=COLOR_ACT_S13[nombre])
        ax.set_yticks([])
        ax.tick_params(labelsize=7)
        if i == 0:
            ax.set_title(f"capa oculta {l}", fontsize=9)
        if l == 1:
            ax.set_ylabel(nombre, fontsize=10)
        ax.text(0.97, 0.9, f"desv {valores.std():.2f}", fontsize=7,
                ha="right", transform=ax.transAxes)
fig.suptitle("Histogramas de a^(l) = g(z^(l)) con la red inicial "
             "(un batch fijo de train)")
fig.supxlabel("valor de la activación")
plt.tight_layout()
plt.show()
del salidas

# %% [texto] s13-lee-histogramas

# %% [texto] s13-entrenar-texto

# %% [codigo] s13-entrenar
# Las cuatro redes, ~500 pasos de SGD (η = 0.03, sin momentum) con batches
# de 128. Evaluamos train/validation/test completos cada 50 pasos.
CORRIDAS_S13 = {}
for nombre in ACTIVACIONES_S13:
    cfg = config_profunda(nombre, id=f"s13-{nombre}", seccion=13,
                          max_pasos=500, eval_cada_pasos=50,
                          medir_por_paso=True)
    CORRIDAS_S13[nombre] = entrenar(cfg)
    print(f"{cfg.id}: {CORRIDAS_S13[nombre].historial['pasos'].max()} pasos,"
          f" divergió = {CORRIDAS_S13[nombre].divergio}")

# %% [codigo] s13-curvas
# Mismos ejes en los cuatro paneles. Recuerda: mirar test en cada
# evaluación está mal; aquí es solo didáctico y nada se elige con test.
lista_s13 = [CORRIDAS_S13[n] for n in ACTIVACIONES_S13]
for metrica in ["loss", "accuracy"]:
    fig = rejilla(lista_s13, x="pasos", metrica=metrica, columnas=4)
    for ax in fig.axes:
        if metrica == "loss":   # referencia: adivinar uniforme, log 10
            ax.axhline(math.log(10), color="gray", ls=":", lw=1)
        else:                   # referencia: azar, 10 %
            ax.axhline(0.10, color="gray", ls=":", lw=1)
    referencia = "log 10" if metrica == "loss" else "azar, 10 %"
    fig.suptitle(f"§13 · {metrica} contra pasos, por activación "
                 f"(línea punteada = {referencia})")
    plt.tight_layout()
    plt.show()

# %% [codigo] s13-tabla
# Resumen: lo que pasó tras ~500 pasos y el gradiente de la capa 1 al inicio.
resumen = []
for nombre in ACTIVACIONES_S13:
    c = CORRIDAS_S13[nombre]
    ultima = c.historial.iloc[-1]
    d = DIAG_S13[(DIAG_S13["activacion"] == nombre)].set_index("capa")
    resumen.append({
        "activacion": nombre,
        "loss_validation final": round(float(ultima["loss_validation"]), 4),
        "acc_validation final": round(float(ultima["acc_validation"]), 4),
        "‖∇W^(1)‖ inicial": f"{d.loc[1, 'norma_grad_W']:.2e}",
        "‖δ^(1)‖/‖δ^(7)‖ inicial":
            f"{d.loc[1, 'norma_delta'] / d.loc[n_capas, 'norma_delta']:.2e}",
        "divergió": c.divergio})
display(pd.DataFrame(resumen).set_index("activacion"))
display(tabla_maestra([13]))

# %% [codigo] s13-durante
# medir_por_paso=True guardó ‖∇W^(l)‖ en cada paso. Miramos la capa 1 (junto
# a la entrada) y la 7 (la de salida): ¿la diferencia del inicio se mantiene?
capa_salida = len(CAPAS_S13) - 1
fig, ejes = plt.subplots(1, 2, figsize=(13, 4), sharey=True)
for ax, capa in zip(ejes, [1, capa_salida]):
    for nombre in ACTIVACIONES_S13:
        pp = CORRIDAS_S13[nombre].por_paso
        if pp is None:
            continue
        d = pp[(pp["capa"] == capa) & np.isfinite(pp["norma_grad"])]
        d = d[d["norma_grad"] > 0]                 # la escala log no admite 0
        ax.plot(d["paso"], d["norma_grad"], color=COLOR_ACT_S13[nombre],
                lw=1, label=nombre)
    ax.set_yscale("log")
    ax.set_xlabel("paso de SGD")
    ax.set_title(f"‖∇ de W^({capa})‖ durante el entrenamiento")
    ax.legend(fontsize=8)
ejes[0].set_ylabel("norma (escala log)")
plt.tight_layout()
plt.show()

# %% [texto] s13-lee-durante

# %% [plegada] s13-apuesta-respuesta

# %% [texto] s13-que-viste
