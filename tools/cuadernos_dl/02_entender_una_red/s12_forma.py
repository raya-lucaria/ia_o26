# Sección 12 · La forma de la red. Cinco arquitecturas con el mismo presupuesto
# (~101–102k parámetros) entrenadas igual: Adam 1e-3, 20k de train, init He,
# 8 epochs, mismas semillas. Produce s12-embudo, s12-invertido, s12-cuello,
# s12-rectangular y s12-una-capa. No consume corridas de otras secciones.

# %% [texto] s12-intro

# %% [codigo] s12-formas
# Las cinco formas. Cada lista incluye la entrada (784) y la salida (10).
FORMAS_S12 = {
    "s12-embudo": ("embudo", [784, 124, 32, 10]),
    "s12-invertido": ("embudo invertido", [784, 96, 248, 10]),
    "s12-cuello": ("cuello de 2", [784, 128, 2, 128, 10]),
    "s12-rectangular": ("rectangular", [784, 112, 112, 10]),
    "s12-una-capa": ("una capa", [784, 128, 10]),
}


def contar_parametros(capas):
    """Σ_l d_l·(d_{l-1} + 1): pesos de W^(l) más sesgos de b^(l), capa por capa."""
    return sum(capas[l] * (capas[l - 1] + 1) for l in range(1, len(capas)))


for id_corrida, (nombre, capas) in FORMAS_S12.items():
    # La fórmula, término por término, para que se vea de dónde sale el total
    terminos = " + ".join(f"{capas[l]}·({capas[l - 1]}+1)"
                          for l in range(1, len(capas)))
    total = contar_parametros(capas)
    # Comprobación: PyTorch cuenta lo mismo que la fórmula
    red = construir_red(capas, init="he")
    assert total == sum(p.numel() for p in red.parameters()), nombre
    print(f"{nombre:>17}  {str(capas):<24} {total:>7,} parámetros")
    print(f"{'':>17}  = {terminos}")
del red

# %% [codigo] s12-dibujos
# Arriba, dibujar_red: columnas de nodos; una capa ancha se abrevia con «⋮»
# y su ancho real va debajo. Abajo, la silueta A ESCALA de las capas ocultas
# y la salida (la entrada de 784 se omite porque aplastaría a las demás):
# ahí sí se ven el embudo, el embudo invertido y el cuello.
fig, ejes = plt.subplots(2, 5, figsize=(20, 7),
                         gridspec_kw={"height_ratios": [3, 2]})
ancho_max = max(max(c[1:]) for _, c in FORMAS_S12.values())
for k, (nombre, capas) in enumerate(FORMAS_S12.values()):
    dibujar_red(capas, ax=ejes[0, k],
                titulo=f"{nombre}\n{contar_parametros(capas):,} parámetros")
    ax = ejes[1, k]
    anchos = capas[1:]                             # ocultas + salida
    etiquetas = [f"oculta {l}" for l in range(1, len(anchos))] + ["salida"]
    # Barra centrada en 0: su alto total es el ancho de la capa
    ax.bar(range(len(anchos)), anchos, bottom=[-d / 2 for d in anchos],
           color=COLORES["train"], alpha=0.6, edgecolor="black")
    for j, d in enumerate(anchos):
        ax.text(j, d / 2 + 6, str(d), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(range(len(anchos)))
    ax.set_xticklabels(etiquetas, fontsize=8)
    ax.set_ylim(-ancho_max / 2 - 10, ancho_max / 2 + 35)
    ax.set_yticks([])
    ax.set_title("silueta a escala (neuronas por capa)", fontsize=9)
fig.suptitle("Cinco formas con casi el mismo número de parámetros", fontsize=14)
fig.tight_layout()
plt.show()

# %% [texto] s12-apuesta

# %% [texto] s12-entrenar-explica

# %% [codigo] s12-entrenar
# Las cinco con exactamente la misma receta: lo único que cambia es la forma.
IDX_S12 = subconjunto(20000)    # el mismo subconjunto estratificado de §11

for id_corrida, (nombre, capas) in FORMAS_S12.items():
    # entrenar imprime una línea por corrida: parámetros, pasos, mejor epoch,
    # accuracy de validation en esa epoch y segundos
    entrenar(Config(
        id=id_corrida, seccion=12,
        capas=capas, activacion="relu", init="he",
        optimizer="adam", lr=1e-3, batch=128, epochs=8,
        idx_train=IDX_S12, datos="20k-limpio",
        semilla_init=SEMILLA, semilla_orden=SEMILLA,   # mismas semillas para todas
    ))

CORRIDAS_S12 = [CORRIDAS[i] for i in FORMAS_S12]

# %% [texto] s12-curvas-lee

# %% [codigo] s12-curvas
# Small multiples: un panel por forma, el mismo eje y en todos para poder
# comparar alturas a simple vista. Test aparece solo de manera didáctica.
for metrica, nombre_metrica in [("loss", "Loss"), ("accuracy", "Accuracy")]:
    fig = rejilla(CORRIDAS_S12, x="epoch", metrica=metrica, columnas=5,
                  misma_y=True)
    for ax, (nombre, capas) in zip(fig.axes, FORMAS_S12.values()):
        ax.set_title(f"{nombre}\nocultas {capas[1:-1]}", fontsize=10)
    # La leyenda común solo nombra el conjunto: el color es lo que importa
    for leyenda in fig.legends:
        leyenda.remove()
    fig.legend(handles=[plt.Line2D([], [], color=COLORES[c], marker="o", label=c)
                        for c in ("train", "validation", "test")],
               loc="upper right", fontsize=9)
    fig.suptitle(f"{nombre_metrica} por epoch de las cinco formas "
                 "(mismo eje y en los cinco paneles)", fontsize=13)
    fig.tight_layout(rect=(0, 0, 0.93, 1))
    plt.show()

# %% [codigo] s12-barras
# Resumen en la mejor epoch de cada corrida, elegida por la loss de
# validation (nunca por test). La tabla maestra ya trae accuracy de train y
# de validation en esa epoch, y la brecha = acc_train − acc_validation.
TABLA_S12 = tabla_maestra([12]).set_index("id").loc[list(FORMAS_S12)]
RESUMEN_S12 = pd.DataFrame({
    "forma": [FORMAS_S12[i][0] for i in TABLA_S12.index],
    "ocultas": [str(FORMAS_S12[i][1][1:-1]) for i in TABLA_S12.index],
    "parametros": TABLA_S12["parametros"].to_numpy(),
    "mejor_epoch": TABLA_S12["mejor_epoch"].to_numpy(),
    "acc_validation_%": 100 * TABLA_S12["acc_validation"].to_numpy(),
    "brecha_pp": 100 * TABLA_S12["brecha"].to_numpy(),   # puntos porcentuales
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))
x = range(len(RESUMEN_S12))
b1 = ax1.bar(x, RESUMEN_S12["acc_validation_%"], color=COLORES["validation"])
ax1.bar_label(b1, fmt="%.2f")
ax1.set_ylim(0, 105)                 # empieza en cero: no exagera diferencias
ax1.set_ylabel("accuracy de validation (%)")
ax1.set_title("Accuracy de validation en la mejor epoch")
b2 = ax2.bar(x, RESUMEN_S12["brecha_pp"], color="#7f7f7f")
ax2.bar_label(b2, fmt="%.2f")
ax2.axhline(0, color="black", linewidth=0.8)
ax2.set_ylabel("train − validation (puntos porcentuales)")
ax2.set_title("Brecha de accuracy en la mejor epoch")
for ax in (ax1, ax2):
    ax.set_xticks(list(x))
    ax.set_xticklabels(RESUMEN_S12["forma"], rotation=15)
    ax.set_xlabel("forma de la red")
fig.tight_layout()
plt.show()

# %% [codigo] s12-tabla
# Los mismos números en una tabla (accuracy en %, brecha en puntos
# porcentuales), y debajo las filas de §12 de la tabla maestra completa.
print(RESUMEN_S12.round(2).to_string(index=False))
print()
print(TABLA_S12.reset_index().round(4).to_string(index=False))

# %% [plegada] s12-apuesta-respuesta

# %% [texto] s12-que-viste
