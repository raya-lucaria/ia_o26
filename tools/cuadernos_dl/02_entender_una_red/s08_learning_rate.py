# Sección 8 · El learning rate.
# Primero una cuadrática 2D (sin datos, numpy puro, cifras analíticas) y
# luego MNIST: ~300 pasos por tasa con SGD y con Adam. Produce las corridas
# s08-sgd-<η> y s08-adam-<η> (η con formato :g, p. ej. s08-sgd-0.03,
# s08-adam-1e-05). Publica: CORRIDAS_LR, TABLA_LR. Consume la caja (s01–s03).

# %% [texto] s08-intro

# %% [texto] s08-cuadratica-texto

# %% [codigo] s08-cuadratica
# f(x, y) = ½ (x² + 100 y²): curvatura 1 en la dirección x, 100 en la y.
# Su gradiente es ∇f = (x, 100 y). Un paso de gradient descent con η:
#     x ← x − η·x     = (1 − η)·x
#     y ← y − η·100·y = (1 − 100η)·y
# Cada dirección se multiplica por un factor fijo en cada paso.
def f_cuadratica(x, y):
    return 0.5 * (x ** 2 + 100 * y ** 2)


def descenso_cuadratica(eta, pasos=100, inicio=(1.0, 1.0)):
    """Los puntos (x, y) que visita gradient descent: arreglo [pasos+1, 2]."""
    puntos = [np.array(inicio, dtype=float)]
    for _ in range(pasos):
        x, y = puntos[-1]
        gradiente = np.array([x, 100 * y])            # ∇f en el punto actual
        puntos.append(puntos[-1] - eta * gradiente)   # el paso: θ ← θ − η ∇f
    return np.array(puntos)


ETAS_2D = [0.001, 0.01, 0.018, 0.025]
NOMBRE_2D = {0.001: "muy bajo", 0.01: "bueno",
             0.018: "alto: oscila", 0.025: "demasiado alto: diverge"}
TRAYECTORIAS = {eta: descenso_cuadratica(eta) for eta in ETAS_2D}

# Los factores por paso son cifras analíticas (no dependen de semillas):
# una dirección converge si y solo si |factor| < 1.
for eta in ETAS_2D:
    fx, fy = 1 - eta, 1 - 100 * eta
    veredicto = "converge" if abs(fx) < 1 and abs(fy) < 1 else "DIVERGE"
    print(f"η = {eta:<6}  factor en x = {fx:+.3f}  factor en y = {fy:+.3f}"
          f"  → {veredicto}")
print(f"Límite de estabilidad: |1 − 100η| < 1  ⇔  0 < η < 2/100 = {2 / 100}")

# Curvas de nivel de f y la trayectoria encima, un panel por η, mismos ejes.
xs, ys = np.meshgrid(np.linspace(-0.3, 1.3, 400), np.linspace(-2.5, 2.5, 400))
niveles = np.logspace(-2, 2.5, 14)
fig, ejes = plt.subplots(1, 4, figsize=(17, 4.4), sharex=True, sharey=True)
for ax, eta in zip(ejes, ETAS_2D):
    ax.contour(xs, ys, f_cuadratica(xs, ys), levels=niveles,
               colors="0.65", linewidths=0.8)
    tr = TRAYECTORIAS[eta]
    fuera = np.nonzero(np.abs(tr[:, 1]) > 2.5)[0]
    if len(fuera):                    # se sale del dibujo: hasta ahí la vemos
        tr = tr[:fuera[0] + 1]
        ax.text(0.5, 0.06, f"en el paso {fuera[0]} sale de la gráfica",
                transform=ax.transAxes, ha="center", color="crimson")
    ax.plot(tr[:, 0], tr[:, 1], "-o", color=COLORES["train"], ms=2.5, lw=1)
    ax.plot(1, 1, "ks", ms=7, label="inicio (1, 1)")
    ax.plot(0, 0, "r*", ms=13, label="mínimo (0, 0)")
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(-2.5, 2.5)
    ax.set_title(f"η = {eta}: {NOMBRE_2D[eta]}")
    ax.set_xlabel("x (curvatura 1)")
ejes[0].set_ylabel("y (curvatura 100)")
ejes[0].legend(loc="upper left", fontsize=8)
fig.suptitle("Gradient descent sobre f(x, y) = ½(x² + 100 y²), 100 pasos")
plt.tight_layout()
plt.show()

# %% [texto] s08-cuadratica-f-texto

# %% [codigo] s08-cuadratica-f
# El valor de f en cada paso, en escala log: una recta que baja es una
# convergencia geométrica (el mismo factor en cada paso).
COLORES_ETA_2D = dict(zip(ETAS_2D, plt.cm.viridis(np.linspace(0, 0.85, 4))))
fig, ax = plt.subplots(figsize=(8, 4.5))
for eta in ETAS_2D:
    tr = TRAYECTORIAS[eta]
    ax.plot(f_cuadratica(tr[:, 0], tr[:, 1]), color=COLORES_ETA_2D[eta],
            lw=2, label=f"η = {eta} ({NOMBRE_2D[eta]})")
ax.set_yscale("log")
ax.set_ylim(1e-3, 1e4)                    # la que diverge se sale por arriba
ax.set_xlabel("paso")
ax.set_ylabel("f(x, y)  (escala log)")
ax.set_title("El valor de f paso a paso, para cada learning rate")
ax.legend()
plt.tight_layout()
plt.show()

for eta in ETAS_2D:
    x, y = TRAYECTORIAS[eta][-1]
    print(f"η = {eta:<6}  tras 100 pasos: x = {x:+.3e}  y = {y:+.3e}"
          f"  f = {f_cuadratica(x, y):.3e}")

# %% [texto] s08-mnist-texto

# %% [texto] s08-apuesta

# %% [codigo] s08-mnist-correr
# La misma red 784 → 128 → 10 (ReLU) y los mismos pesos iniciales
# (semilla_init = 0) para todas: lo ÚNICO que cambia es η (y el optimizer).
# Cada corrida da ~300 pasos de batch 128 (menos de una epoch) y evalúa
# train y validation completos cada 25 pasos.
PASOS_LR = 30 if RAPIDO else 300
EVAL_LR = 5 if RAPIDO else 25
# El último valor de SGD (1000) es absurdo a propósito: con ReLU y
# cross-entropy, un η grande suele «matar» la red sin producir NaN; con 1000
# los números se desbordan y vemos cómo entrenar() atrapa el NaN sin tronar.
BARRIDO_LR = {
    "sgd": [1e-4, 1e-3, 1e-2, 3e-2, 1e-1, 0.5, 1.0, 5.0, 1000.0],
    "adam": [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
}
CORRIDAS_LR = {"sgd": [], "adam": []}

for opt, etas in BARRIDO_LR.items():
    for eta in etas:
        cfg = Config(id=f"s08-{opt}-{eta:g}", seccion=8,
                     capas=[784, 128, 10], optimizer=opt, lr=eta, batch=128,
                     epochs=10, max_pasos=PASOS_LR, eval_cada_pasos=EVAL_LR)
        # entrenar imprime una línea por corrida. Si la loss deja de ser
        # finita, NO truena: marca divergio, anota el paso y se detiene.
        CORRIDAS_LR[opt].append(entrenar(cfg))

# %% [texto] s08-rejilla-texto

# %% [codigo] s08-rejilla
# Una gráfica por η: loss de train y de validation contra pasos.
# Mismos ejes en todas; la línea punteada es log 10 ≈ 2.30, la loss de
# adivinar uniforme entre 10 dígitos.
TECHO_LR = 3.5            # lo que pasa de aquí ya es «peor que adivinar»


NOMBRE_OPT = {"sgd": "SGD", "adam": "Adam"}


def panel_lr(ax, c):
    """Las curvas de una corrida del barrido; si divergió, lo dice encima."""
    nombre = NOMBRE_OPT[c.config.optimizer]
    curvas([c], x="pasos", metrica="loss", conjuntos=("train", "validation"),
           ax=ax, titulo=f"{nombre}, η = {c.config.lr:g}")
    if ax.get_legend():
        ax.get_legend().remove()          # una sola leyenda por figura, abajo
    ax.axhline(math.log(10), color="0.4", ls=":", lw=1)
    ax.set_ylim(0, TECHO_LR)
    ax.set_xlim(0, PASOS_LR)
    v = c.historial[["loss_train", "loss_validation"]].to_numpy(dtype=float)
    v = v[np.isfinite(v)]
    if len(v) and v.max() > TECHO_LR:     # avisa lo que se sale por arriba
        ax.text(0.98, 0.04, f"máx. {v.max():.3g}: sale del eje",
                transform=ax.transAxes, ha="right", va="bottom", color="crimson")
    if c.divergio:
        ax.text(0.5, 0.5, f"DIVERGIÓ\nprimer paso no finito: {c.paso_no_finito}",
                transform=ax.transAxes, ha="center", va="center",
                color="crimson", fontsize=11, fontweight="bold")


for opt, columnas in (("sgd", 3), ("adam", 5)):
    lista = CORRIDAS_LR[opt]
    filas = math.ceil(len(lista) / columnas)
    fig, ejes = plt.subplots(filas, columnas, figsize=(4 * columnas, 3.3 * filas),
                             squeeze=False)
    for ax, c in zip(ejes.flat, lista):
        panel_lr(ax, c)
    for ax in list(ejes.flat)[len(lista):]:
        ax.set_visible(False)
    fig.suptitle(f"{NOMBRE_OPT[opt]}: loss contra pasos, de η pequeño a η grande")
    fig.legend(handles=[plt.Line2D([], [], color=COLORES["train"], label="train"),
                        plt.Line2D([], [], color=COLORES["validation"],
                                   label="validation"),
                        plt.Line2D([], [], color="0.4", ls=":",
                                   label="log 10 ≈ 2.30 (adivinar)")],
               loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0))
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    plt.show()

# %% [texto] s08-u-texto

# %% [codigo] s08-u
# La «U»: loss de validation al final de los pasos contra η (escala log).
# Una × arriba = la corrida divergió (su loss ya no es un número);
# un triángulo hueco arriba = loss finita, pero más alta que el techo.
ESTILO_OPT = {"sgd": ("#9467bd", "o", "SGD"), "adam": ("#8c564b", "s", "Adam")}
filas_tabla = []
fig, ax = plt.subplots(figsize=(9, 4.8))
for opt, lista in CORRIDAS_LR.items():
    color, marca, nombre = ESTILO_OPT[opt]
    etas_ok, finales = [], []
    for c in lista:
        ultima = c.historial.iloc[-1]
        final = float(ultima["loss_validation"])
        roto = c.divergio or not math.isfinite(final)
        filas_tabla.append({
            "optimizer": nombre, "η": c.config.lr,
            "loss train final": float(ultima["loss_train"]),
            "loss validation final": final,
            "acc validation final": float(ultima["acc_validation"]),
            "divergió": c.divergio, "primer paso no finito": c.paso_no_finito,
            "loss final no finita": not math.isfinite(final)})
        if roto:
            ax.plot(c.config.lr, TECHO_LR, "x", color=color, ms=12, mew=3)
        else:
            etas_ok.append(c.config.lr)
            finales.append(min(final, TECHO_LR))  # fuera de escala → al techo
            if final > TECHO_LR:
                ax.plot(c.config.lr, TECHO_LR, "^", color=color, ms=12,
                        mfc="none", mew=2)
                ax.annotate(f"{final:.3g}", (c.config.lr, TECHO_LR), color=color,
                            textcoords="offset points", xytext=(8, -14))
    ax.plot(etas_ok, finales, "-", marker=marca, color=color, lw=2, ms=7,
            label=f"{nombre} (× = divergió, △ = fuera de escala)")
ax.axhline(math.log(10), color="0.4", ls=":", lw=1,
           label="log 10 ≈ 2.30: adivinar uniforme")
ax.set_xscale("log")
ax.set_ylim(0, TECHO_LR + 0.2)
ax.set_xlabel("learning rate η (escala log)")
ax.set_ylabel(f"loss de validation tras {PASOS_LR} pasos")
ax.set_title("Loss de validation según el learning rate")
ax.legend()
plt.tight_layout()
plt.show()

TABLA_LR = pd.DataFrame(filas_tabla)
# El ganador de cada optimizer se elige con validation (nunca con test).
validas = ~TABLA_LR["divergió"] & ~TABLA_LR["loss final no finita"]
for nombre, grupo in TABLA_LR[validas].groupby("optimizer"):
    mejor = grupo.loc[grupo["loss validation final"].idxmin()]
    print(f"Mejor η para {nombre} (por loss de validation): {mejor['η']:g}")
display(TABLA_LR.round({"loss train final": 4, "loss validation final": 4,
                        "acc validation final": 4}))

# %% [plegada] s08-apuesta-respuesta

# %% [texto] s08-que-viste
