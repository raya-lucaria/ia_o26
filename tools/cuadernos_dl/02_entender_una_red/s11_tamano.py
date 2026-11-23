# Sección 11 · El tamaño de la red. Rejilla ancho × profundidad tras cinco
# epochs (20k de train, Adam 1e-3, init He) y el cuello de 2 neuronas.
# Produce: s11-a<ancho>-p<prof> (20 corridas) y s11-cuello-256.

# %% [texto] s11-intro

# %% [codigo] s11-parametros
# (time, numpy, pandas, torch, nn y plt ya vienen del arranque, §1)
T0_S11 = time.perf_counter()          # reloj de toda la sección

ANCHOS = [2, 16, 64, 256, 1024]       # d_l: neuronas por capa oculta
PROFUNDIDADES = [1, 2, 4, 8]          # número de capas ocultas
if RAPIDO:                            # prueba en CPU: rejilla chica de 3 × 3
    ANCHOS, PROFUNDIDADES = [2, 16, 64], [1, 2, 4]


def capas_s11(ancho, prof):
    """[784, ancho, ..., ancho, 10] con `prof` capas ocultas iguales."""
    return [784] + [ancho] * prof + [10]


def contar_parametros(capas):
    """Cada capa l tiene una matriz W de d_l × d_{l-1} y d_l sesgos."""
    return sum((d_ant + 1) * d for d_ant, d in zip(capas[:-1], capas[1:]))


IDX_20K = subconjunto(20000)          # los mismos 20k ejemplos para las 20 redes


def config_s11(ancho, prof):
    """Una celda de la rejilla: todo igual salvo la forma de la red."""
    return Config(
        id=f"s11-a{ancho}-p{prof}", seccion=11,
        capas=capas_s11(ancho, prof), activacion="relu", init="he",
        optimizer="adam", lr=1e-3, batch=128, epochs=5,
        escala="estandar", idx_train=IDX_20K, datos="20k-limpio",
    )


# Conteo exacto, antes de entrenar nada: filas = profundidad, columnas = ancho
conteo = pd.DataFrame(
    [[contar_parametros(capas_s11(a, p)) for a in ANCHOS] for p in PROFUNDIDADES],
    index=pd.Index(PROFUNDIDADES, name="capas ocultas"),
    columns=pd.Index(ANCHOS, name="ancho"),
)
# comprobación: el conteo a mano coincide con el de PyTorch
red = construir_red(capas_s11(64, 2), init="he")
assert contar_parametros(capas_s11(64, 2)) == sum(t.numel() for t in red.parameters())
del red
print("Parámetros de cada red de la rejilla:")
display(conteo)

# %% [texto] s11-apuesta

# %% [codigo] s11-rejilla
# 20 redes, de la más angosta y somera a la más ancha y profunda.
# entrenar() imprime una línea por red; las gráficas leen la ÚLTIMA epoch.
REJILLA = {}                          # (ancho, prof) -> Corrida
for prof in PROFUNDIDADES:
    for ancho in ANCHOS:
        REJILLA[(ancho, prof)] = entrenar(config_s11(ancho, prof))

# %% [texto] s11-mapas-lee

# %% [codigo] s11-mapas


def matriz_s11(columna):
    """Matriz profundidad × ancho con el valor final (tras 5 epochs)."""
    M = np.full((len(PROFUNDIDADES), len(ANCHOS)), np.nan)
    for i, p in enumerate(PROFUNDIDADES):
        for j, a in enumerate(ANCHOS):
            h = REJILLA[(a, p)].historial
            M[i, j] = h[columna].iloc[-1]
    return M


def mapa_de_calor(M, ax, titulo, cmap, vmin, vmax, formato):
    im = ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(ANCHOS)), [str(a) for a in ANCHOS])
    ax.set_yticks(range(len(PROFUNDIDADES)), [str(p) for p in PROFUNDIDADES])
    ax.set_xlabel("ancho (neuronas por capa oculta)")
    ax.set_ylabel("profundidad (capas ocultas)")
    ax.set_title(titulo)
    ax.grid(False)
    for i in range(M.shape[0]):           # anota cada celda con su valor
        for j in range(M.shape[1]):
            v = M[i, j]
            texto = "—" if not np.isfinite(v) else format(v, formato)
            r, g, b, _ = im.cmap(im.norm(v)) if np.isfinite(v) else (1, 1, 1, 1)
            claro = 0.299 * r + 0.587 * g + 0.114 * b > 0.5   # fondo claro?
            ax.text(j, i, texto, ha="center", va="center", fontsize=9,
                    color="black" if claro else "white")
    plt.colorbar(im, ax=ax, shrink=0.8)


ACC_VAL = matriz_s11("acc_validation")
BRECHA = matriz_s11("acc_train") - ACC_VAL      # brecha train − validation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
mapa_de_calor(ACC_VAL, ax1, "Accuracy de validation tras 5 epochs",
              "viridis", np.nanmin(ACC_VAL), np.nanmax(ACC_VAL), ".3f")
m = max(np.nanmax(np.abs(BRECHA)), 1e-3)        # escala simétrica alrededor de 0
mapa_de_calor(BRECHA, ax2, "Brecha de accuracy: train − validation",
              "RdBu_r", -m, m, "+.3f")
fig.suptitle("La rejilla ancho × profundidad (Adam 1e-3, init He, "
             + ("RAPIDO: datos y pasos recortados)" if RAPIDO
                else "20k de train, 5 epochs)"))
fig.tight_layout()
plt.show()

# %% [plegada] s11-apuesta-respuesta

# %% [texto] s11-parametros-lee

# %% [codigo] s11-dispersion
fig, ax = plt.subplots(figsize=(8, 5))
colores_prof = plt.cm.viridis(np.linspace(0, 0.85, len(PROFUNDIDADES)))
for color, p in zip(colores_prof, PROFUNDIDADES):
    xs = [REJILLA[(a, p)].parametros for a in ANCHOS]
    ys = [REJILLA[(a, p)].historial["acc_validation"].iloc[-1] for a in ANCHOS]
    ax.plot(xs, ys, "o-", color=color, label=f"{p} capa(s) oculta(s)")
    for a, x, y in zip(ANCHOS, xs, ys):  # rotula cada punto con su ancho
        ax.annotate(f"{a}", (x, y), textcoords="offset points",
                    xytext=(4, -10), fontsize=8, color=color)
ax.set_xscale("log")
ax.set_xlabel("número de parámetros (escala log)")
ax.set_ylabel("accuracy de validation tras 5 epochs")
ax.set_title("¿Cuándo deja de servir agrandar la red?  (número = ancho)")
ax.legend(title="profundidad")
plt.show()

# %% [texto] s11-dibujos-lee

# %% [codigo] s11-dibujos
medio = ANCHOS[len(ANCHOS) // 2]      # 64 en la rejilla completa
EJEMPLOS = [(ANCHOS[0], PROFUNDIDADES[0], "la más chica"),       # [784, 2, 10]
            (medio, PROFUNDIDADES[1], "una mediana"),           # 64 × 2
            (ANCHOS[-1], PROFUNDIDADES[0], "la más ancha"),     # 1024 × 1
            (medio, PROFUNDIDADES[-1], "la más profunda")]      # 64 × 8
anchos_fig = [len(capas_s11(a, p)) for a, p, _ in EJEMPLOS]   # columnas de nodos
fig, axes = plt.subplots(1, 4, figsize=(18, 4.4),
                         gridspec_kw={"width_ratios": anchos_fig})
for ax, (a, p, nombre) in zip(axes, EJEMPLOS):
    c = REJILLA[(a, p)]
    val = c.historial["acc_validation"].iloc[-1]
    dibujar_red(capas_s11(a, p), ax=ax,
                titulo=f"{nombre}: {c.parametros:,} parámetros\n"
                       f"accuracy de validation {val:.3f}")
plt.show()

# %% [texto] s11-cuello-intro

# %% [codigo] s11-cuello-entrena
# La red de ancho 2 y una capa oculta ya está en la rejilla: [784, 2, 10].
if "s11-a2-p1" not in CORRIDAS:      # por si se saltó la celda de la rejilla
    entrenar(config_s11(2, 1))
# Una segunda: primero 256 neuronas, luego el cuello de 2: [784, 256, 2, 10]
cfg = config_s11(2, 1)
cfg.id, cfg.capas = "s11-cuello-256", [784, 256, 2, 10]
entrenar(cfg)
CUELLOS = [CORRIDAS["s11-a2-p1"], CORRIDAS["s11-cuello-256"]]
for c in CUELLOS:
    print(f"{c.id:>15} {c.config.capas}  val "
          f"{c.historial['acc_validation'].iloc[-1]:.3f}")

# %% [codigo] s11-cuello-activaciones


@torch.no_grad()
def activaciones_cuello(modelo, X):
    """Pasa X capa por capa y se detiene tras la activación que sigue a la
    capa lineal de 2 neuronas. Devuelve z (antes de la ReLU) y a (después)."""
    h, z = X, None
    for capa in modelo:
        if z is not None and isinstance(capa, nn.Linear):
            break                     # la siguiente lineal ya es la salida
        h = capa(h)
        if isinstance(capa, nn.Linear) and capa.out_features == 2:
            z = h                     # z: la combinación lineal del cuello
    return z.cpu().numpy(), h.cpu().numpy()


Xv, yv = DATOS["estandar"]["validation"]
digitos = yv.cpu().numpy()
orden = np.random.default_rng(SEMILLA).permutation(len(digitos))
# leyenda a mano: un punto de cada color
muestras = [plt.Line2D([], [], ls="", marker="o", color=plt.cm.tab10(d),
                       label=str(d)) for d in range(10)]
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for fila, c in zip(axes, CUELLOS):
    z, a = activaciones_cuello(cargar(c, "ultima"), Xv)
    for ax, M, que in [(fila[0], z, "z, antes de la ReLU"),
                       (fila[1], a, "a = ReLU(z), lo que ve la capa siguiente")]:
        # orden al azar: si dibujáramos dígito por dígito, el 9 taparía al 0
        ax.scatter(M[orden, 0], M[orden, 1], s=3, alpha=0.4,
                   c=plt.cm.tab10(digitos[orden]))
        ax.set_xlabel("neurona 1 del cuello")
        ax.set_ylabel("neurona 2 del cuello")
        ax.set_title(f"{c.config.capas}: {que}", fontsize=10)
    fila[1].legend(handles=muestras, title="dígito", fontsize=8, loc="best")
    ceros = (a == 0)
    print(f"{c.id}: neurona 1 en cero {ceros[:, 0].mean():.1%}, "
          f"neurona 2 en cero {ceros[:, 1].mean():.1%}, "
          f"las dos en cero {ceros.all(axis=1).mean():.1%} de validation")
    en_origen = np.bincount(digitos[ceros.all(axis=1)], minlength=10)
    print("   imágenes en el origen (0, 0), por dígito:", en_origen.tolist())
fig.suptitle("Validation vista por las dos neuronas del cuello (color = dígito)")
fig.tight_layout()
plt.show()

# %% [texto] s11-cuello-lee

# %% [codigo] s11-tabla
filas = []
# las 20 de la rejilla (ordenadas por profundidad y ancho) y el cuello de 256
ordenadas = sorted(REJILLA, key=lambda k: (k[1], k[0]))
for c in [REJILLA[k] for k in ordenadas] + [CORRIDAS["s11-cuello-256"]]:
    final = c.historial.iloc[-1]                 # tras las 5 epochs
    filas.append({"id": c.id, "capas ocultas": c.config.capas[1:-1],
                  "parametros": c.parametros,
                  "acc train": final["acc_train"],
                  "acc validation": final["acc_validation"],
                  "brecha": final["acc_train"] - final["acc_validation"],
                  "segundos": final["segundos"], "divergio": c.divergio})
RESUMEN_S11 = pd.DataFrame(filas).set_index("id").round(4)
display(RESUMEN_S11)
print(f"Tiempo total de la sección 11: {time.perf_counter() - T0_S11:.0f} s")

# %% [texto] s11-que-viste
