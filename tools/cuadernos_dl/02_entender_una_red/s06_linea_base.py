# Sección 6 · La línea base y cómo leer tres curvas.
# Consume la corrida s04-oculta (784→128→10, ReLU, Adam 1e-3, 8 epochs). Si
# falta porque el alumno saltó §4, la entrena con exactamente esa Config y lo
# dice. No produce corridas nuevas. Lleva el aviso completo sobre test.

# %% [texto] s06-intro

# %% [texto] s06-aviso-test

# %% [codigo] s06-linea-base
# La línea base es la red de una capa oculta de la sección 4. Si ya la
# entrenaste, la reutilizamos tal cual; si saltaste hasta aquí, la entrenamos
# con la MISMA configuración y el MISMO ID, así que todo lo que sigue es igual.
if "s04-oculta" in CORRIDAS:
    base = CORRIDAS["s04-oculta"]
    print("Reutilizo la corrida s04-oculta de la sección 4.")
else:
    print("No encontré s04-oculta (¿saltaste la sección 4?). La entreno ahora "
          "con la misma configuración.")
    base = entrenar(Config(id="s04-oculta", seccion=4, capas=[784, 128, 10],
                           activacion="relu", optimizer="adam", lr=1e-3,
                           epochs=8))

h = base.historial                       # una fila por evaluación (epoch)
cfg = base.config
print(f"red {cfg.capas}, activación {cfg.activacion}, optimizer {cfg.optimizer}, "
      f"η = {cfg.lr}, batch {cfg.batch}, epochs {h['epoch'].max():g}")
print(f"parámetros: {base.parametros:,}")
# La tabla de las curvas la mostramos después de la apuesta, junto a la figura.

# %% [texto] s06-referencias

# %% [codigo] s06-referencias-calcula
import math

# Dos referencias analíticas para «no saber nada». Se calculan, no se copian.
LOSS_UNIFORME = math.log(10)  # −log(1/10): dar 1/10 de probabilidad a cada dígito
ACC_AZAR = 1 / 10             # elegir un dígito al azar acierta 1 de cada 10

# Otra manera de no saber nada: predecir siempre la proporción de cada dígito
# en train. Su cross-entropy es la entropía de esas proporciones; como MNIST
# está casi balanceado, sale casi igual que log(10).
_, y_tr = DATOS[cfg.escala]["train"]
prop = torch.bincount(y_tr, minlength=10).float() / len(y_tr)
entropia = -(prop * prop.log()).sum().item()

print(f"loss de adivinar uniforme:            log(10) = {LOSS_UNIFORME:.4f}")
print(f"loss de predecir las proporciones:    {entropia:.4f}")
print(f"accuracy de adivinar al azar:         {ACC_AZAR:.0%}")

# La epoch 0 es la red recién inicializada, antes de cualquier paso.
cero = h[h["epoch"] == 0]
if len(cero):
    e0 = cero.iloc[0]
    print(f"\nepoch 0 (pesos aleatorios, sin entrenar):")
    for conj in ("train", "validation", "test"):
        print(f"  {conj:<10} loss = {e0['loss_' + conj]:.4f}   "
              f"accuracy = {e0['acc_' + conj]:.2%}")
else:
    print("\nEl historial no trae la epoch 0.")

# %% [texto] s06-apuesta

# %% [codigo] s06-figura
# Arriba, la vista completa con las referencias; abajo, un acercamiento a las
# epochs 1 en adelante, donde las tres curvas se separan.
fig, ejes = plt.subplots(2, 2, figsize=(14, 10))
ultima_epoch = float(h["epoch"].max())   # la última evaluación
tramo = h[h["epoch"] >= 1]

for col, metrica, ref, etiqueta_ref in [
        (0, "loss", LOSS_UNIFORME,
         f"adivinar uniforme: log 10 ≈ {LOSS_UNIFORME:.2f}"),
        (1, "accuracy", ACC_AZAR, f"azar: {ACC_AZAR:.0%}")]:
    arriba, abajo = ejes[0, col], ejes[1, col]
    nombre = "Loss (cross-entropy)" if metrica == "loss" else "Accuracy"
    curvas([base], metrica=metrica, ax=arriba,
           titulo=f"{nombre}: vista completa, con epoch 0")
    arriba.axhline(ref, color="gray", ls=":", lw=2, label=etiqueta_ref)
    curvas([base], metrica=metrica, ax=abajo,
           titulo=f"{nombre}: acercamiento a las epochs 1 a {ultima_epoch:g}")
    # Los límites del acercamiento salen de los datos de las epochs >= 1.
    pref = "loss_" if metrica == "loss" else "acc_"
    valores = tramo[[pref + c for c in ("train", "validation", "test")]]
    lo, hi = valores.min().min(), valores.max().max()
    margen = 0.08 * (hi - lo) + 1e-6
    abajo.set_xlim(0.8, ultima_epoch + 0.2)
    abajo.set_ylim(lo - margen, hi + margen)
    for ax in (arriba, abajo):
        ax.axvline(base.mejor_epoch, color=COLORES["validation"], ls="--",
                   alpha=0.6, label=f"mejor epoch por validation "
                                    f"({base.mejor_epoch:g})")
        ax.set_xlabel("epoch")
        ax.set_ylabel(nombre)
        ax.legend(fontsize=9)

fig.suptitle("La línea base 784→128→10 (ReLU, Adam): train, validation y test "
             "en cada epoch\n(test se grafica solo para aprender a leerlo; "
             "ninguna decisión lo usa)", fontsize=13)
fig.tight_layout()
plt.show()

print(f"mejor epoch por validation (menor loss): {base.mejor_epoch:g}")
columnas = ["epoch", "pasos", "loss_train", "loss_validation", "loss_test",
            "acc_train", "acc_validation", "acc_test"]
display(h[columnas].round(4).set_index("epoch"))

# %% [plegada] s06-apuesta-respuesta

# %% [texto] s06-como-leer

# %% [texto] s06-brechas

# %% [codigo] s06-brechas-tabla
# La brecha de cada epoch, con el signo elegido para que salga positiva
# cuando el primer conjunto «se ve mejor» que el segundo.
brechas = pd.DataFrame({
    "epoch": h["epoch"],
    # Loss: validation − train. Positiva = train es optimista.
    "brecha loss (val − train)": h["loss_validation"] - h["loss_train"],
    # Loss: test − validation. Dos estimaciones honestas del mismo riesgo.
    "diferencia loss (test − val)": h["loss_test"] - h["loss_validation"],
    # Accuracy: train − validation. Positiva = train es optimista.
    "brecha acc (train − val)": h["acc_train"] - h["acc_validation"],
    "diferencia acc (val − test)": h["acc_validation"] - h["acc_test"],
}).set_index("epoch")
display(brechas.round(4))

# ¿Qué tan grande es una diferencia «de ruido» entre validation y test?
# El error estándar de una accuracy p medida en n ejemplos es sqrt(p(1−p)/n),
# como el de una proporción en la unidad 9. La diferencia de DOS accuracies
# independientes suma las dos varianzas; lo calculamos en cada epoch.
n_val = len(DATOS[cfg.escala]["validation"][1])
n_test = len(DATOS[cfg.escala]["test"][1])
pv, pt = h["acc_validation"], h["acc_test"]
ee_dif = np.sqrt(pv * (1 - pv) / n_val + pt * (1 - pt) / n_test).to_numpy()
ee_mejor = ee_dif[(h["epoch"] == base.mejor_epoch).to_numpy()][0]
print(f"n de validation = {n_val:,}; n de test = {n_test:,}")
print(f"en la mejor epoch, error estándar de (acc val − acc test) ≈ "
      f"{ee_mejor:.2%}; 2 errores estándar ≈ {2 * ee_mejor:.2%}")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4))
a1.plot(brechas.index, brechas["brecha loss (val − train)"], "o-",
        color=COLORES["validation"], label="loss validation − loss train")
a1.plot(brechas.index, brechas["diferencia loss (test − val)"], "s-",
        color=COLORES["test"], label="loss test − loss validation")
a1.set_title("Brechas de la loss por epoch")
a2.plot(brechas.index, brechas["brecha acc (train − val)"], "o-",
        color=COLORES["validation"], label="acc train − acc validation")
a2.plot(brechas.index, brechas["diferencia acc (val − test)"], "s-",
        color=COLORES["test"], label="acc validation − acc test")
a2.fill_between(brechas.index, -2 * ee_dif, 2 * ee_dif, color="gray",
                 alpha=0.15, label="± 2 errores estándar de (val − test)")
a2.set_title("Brechas de la accuracy por epoch")
for ax in (a1, a2):
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("epoch")
    ax.set_ylabel("diferencia")
    ax.legend(fontsize=9)
fig.tight_layout()
plt.show()

# %% [texto] s06-confianza-intro

# %% [codigo] s06-confianza
import torch.nn.functional as F


def resumen_confianza(modelo, escala, conjunto="validation"):
    """Qué tan seguro está el modelo cuando acierta y cuando se equivoca."""
    X, y = DATOS[escala][conjunto]
    with torch.no_grad():                         # solo evaluamos, sin gradiente
        logits = torch.cat([modelo(X[i:i + 4096])
                            for i in range(0, len(X), 4096)])
    prob = torch.softmax(logits, dim=1)           # [n, 10], cada fila suma 1
    confianza, pred = prob.max(dim=1)             # p de la clase que eligió
    p_real = prob[torch.arange(len(y), device=y.device), y]  # p de la correcta
    perdida = F.cross_entropy(logits, y, reduction="none")    # −log p_real
    error = pred != y
    n = len(y)
    fila = {
        "accuracy": 1 - error.float().mean().item(),
        "loss (promedio de todos)": perdida.mean().item(),
        "número de errores": int(error.sum()),
        "confianza media en los errores": confianza[error].mean().item(),
        "p media de la clase correcta en los errores": p_real[error].mean().item(),
        "loss media de un error": perdida[error].mean().item(),
        "loss media de un acierto": perdida[~error].mean().item(),
        "aporte de los errores a la loss": perdida[error].sum().item() / n,
        "aporte de los aciertos a la loss": perdida[~error].sum().item() / n,
    }
    return fila, confianza[error].cpu()


filas, conf_errores = {}, {}
for cual, epoch in [("mejor", base.mejor_epoch), ("ultima", ultima_epoch)]:
    modelo = cargar(base, cual)                   # checkpoint en DEVICE, eval()
    nombre = f"{cual} (epoch {epoch:g})"
    filas[nombre], conf_errores[nombre] = resumen_confianza(modelo, cfg.escala)
    del modelo

tabla_conf = pd.DataFrame(filas).round(4).astype(object)
tabla_conf.loc["número de errores"] = tabla_conf.loc["número de errores"].astype(int)
display(tabla_conf)
if base.mejor_epoch == ultima_epoch:
    print("En esta corrida la mejor epoch por validation ES la última: las dos "
          "columnas son el mismo modelo y aquí no hay nada que comparar.")

# %% [codigo] s06-confianza-figura
# La confianza (probabilidad de la clase elegida) en cada error de validation.
fig, ax = plt.subplots(figsize=(9, 4.5))
cajas = [i / 20 for i in range(21)]                 # 20 intervalos en [0, 1]
for (nombre, conf), color in zip(conf_errores.items(),
                                 [COLORES["validation"], "#555555"]):
    ax.hist(conf.numpy(), bins=cajas, histtype="step", lw=2, color=color,
            label=f"{nombre}: {len(conf)} errores")
ax.set_xlabel("confianza en la clase elegida (equivocada)")
ax.set_ylabel("número de errores en validation")
ax.set_title("¿Qué tan seguros están los errores? Mejor epoch vs última")
ax.legend()
plt.show()

# %% [texto] s06-que-viste
