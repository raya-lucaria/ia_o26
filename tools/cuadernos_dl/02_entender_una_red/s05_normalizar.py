# Sección 5 · Normalizar la entrada.
# Produce las corridas s05-crudo, s05-01, s05-estandar (5 epochs) y
# s05-crudo-arranque, s05-01-arranque, s05-estandar-arranque (los mismos
# primeros 50 pasos, evaluados cada 2 pasos). Publica: ESCALAS_S05,
# CORRIDAS_S05, ARRANQUE_S05. Consume la caja (s01–s03): DATOS, MEDIA, DESV.

# %% [texto] s05-intro

# %% [codigo] s05-estadisticas
# Las tres escalas de la misma imagen viven ya en DATOS (sección 2):
#   "crudo"    : el píxel como viene, un entero de 0 a 255
#   "01"       : x / 255, en [0, 1]
#   "estandar" : (x/255 − MEDIA) / DESV, con MEDIA y DESV de TRAIN
ESCALAS_S05 = ["crudo", "01", "estandar"]
print(f"MEDIA = {MEDIA:.4f}   DESV = {DESV:.4f}   (escala [0, 1], solo train)")

# Comprobación: MEDIA y DESV salen de train y de nada más.
X01_train = DATOS["01"]["train"][0]
print(f"recalculadas sobre train: media = {X01_train.mean().item():.4f}, "
      f"desv = {X01_train.std().item():.4f}")

# Mínimo, máximo, media y desviación de los píxeles, por escala y conjunto.
filas = []
for escala in ESCALAS_S05:
    for conjunto in ["train", "validation", "test"]:
        X = DATOS[escala][conjunto][0]
        filas.append({"escala": escala, "conjunto": conjunto,
                      "mínimo": X.min().item(), "máximo": X.max().item(),
                      "media": X.mean().item(), "desv": X.std().item()})
display(pd.DataFrame(filas).round(4))
# Fíjate en "estandar": en train la media es 0 y la desviación 1 por
# construcción; en validation y test quedan CERCA de 0 y 1, no exactas,
# porque se les aplicó la receta de train sin recalcularla.

# %% [texto] s05-histogramas-guia

# %% [codigo] s05-histogramas
# Histograma de los píxeles de una muestra fija de imágenes de train, en las
# tres escalas. Es la misma muestra en los tres paneles: solo cambia el eje x.
generador = torch.Generator().manual_seed(SEMILLA)
n_train = DATOS["01"]["train"][0].shape[0]
n_muestra = min(n_train, 200 if RAPIDO else 2000)
muestra = torch.randperm(n_train, generator=generador)[:n_muestra]

titulos = {"crudo": "Crudo: 0 a 255", "01": "Dividido entre 255: [0, 1]",
           "estandar": "Estandarizado con train"}
fig, ejes = plt.subplots(1, 3, figsize=(14, 3.8))
for ax, escala in zip(ejes, ESCALAS_S05):
    X = DATOS[escala]["train"][0]
    valores = X[muestra.to(X.device)].flatten().cpu().numpy()
    ax.hist(valores, bins=50, color=COLORES["train"], alpha=0.85)
    ax.axvline(valores.mean(), color="black", linestyle="--",
               label=f"media = {valores.mean():.2f}")
    ax.set_yscale("log")                  # casi todo es fondo: escala log
    ax.set_title(titulos[escala])
    ax.set_xlabel("valor del píxel")
    ax.set_ylabel("número de píxeles (escala log)")
    ax.legend()
fig.suptitle(f"Los mismos píxeles de {n_muestra} imágenes de train, "
             "en tres escalas", y=1.03)
plt.tight_layout()
plt.show()

# %% [texto] s05-gradiente

# %% [codigo] s05-gradiente-inicial
# Antes de entrenar: el MISMO batch de 128 imágenes y los MISMOS pesos
# iniciales; solo cambia la escala de la entrada. ¿Qué tan grande sale el
# gradiente de cada capa, y qué tan grande sería un paso de SGD con η = 0.03?
perdida = nn.CrossEntropyLoss()
eta = 0.03
idx = torch.arange(128, device=DEVICE)
filas = []
for escala in ESCALAS_S05:
    torch.manual_seed(SEMILLA)                   # mismos pesos en las tres
    red = construir_red([784, 128, 10]).to(DEVICE)
    lineales = [m for m in red.modules() if isinstance(m, nn.Linear)]
    X, y = DATOS[escala]["train"]
    loss = perdida(red(X[idx]), y[idx])          # forward
    loss.backward()                              # backpropagation
    for l, capa in enumerate(lineales, start=1):
        W, g = capa.weight, capa.weight.grad     # g = ∇_W L, misma forma que W
        filas.append({
            "escala": escala, "capa": l, "loss inicial": loss.item(),
            "‖∇W‖": g.norm().item(),
            # tamaño del paso de SGD relativo al tamaño de los pesos
            "η‖∇W‖ / ‖W‖": (eta * g.norm() / W.norm()).item()})
    del red, lineales, loss
tabla_grad = pd.DataFrame(filas)
display(tabla_grad.round(4))

# Cuántas veces más grande es el gradiente de la capa 1 que con [0, 1].
capa1 = tabla_grad[tabla_grad["capa"] == 1].set_index("escala")["‖∇W‖"]
for escala in ESCALAS_S05:
    print(f"capa 1, {escala:>8}: ‖∇W‖ es {capa1[escala] / capa1['01']:8.1f} "
          "veces el de la escala [0, 1]")

# %% [texto] s05-apuesta

# %% [codigo] s05-entrenar
# Tres corridas idénticas salvo la escala de la entrada: red [784, 128, 10]
# con ReLU, SGD sin momentum, η = 0.03, batches de 128, 5 epochs, los mismos
# pesos iniciales (semilla_init) y el mismo orden de batches (semilla_orden).
CORRIDAS_S05 = {}
for escala in ESCALAS_S05:
    cfg = Config(id=f"s05-{escala}", seccion=5, capas=[784, 128, 10],
                 activacion="relu", optimizer="sgd", lr=0.03, batch=128,
                 epochs=5, escala=escala,
                 semilla_init=SEMILLA, semilla_orden=SEMILLA)
    CORRIDAS_S05[escala] = entrenar(cfg)   # imprime su resumen al terminar
# Si una corrida divergió, el resumen lo dice y marca el primer paso no finito.

# %% [codigo] s05-curvas
# Las tres corridas lado a lado, con los MISMOS ejes (misma_y=True).
# Arriba la accuracy; abajo la loss en escala log, porque la de "crudo"
# puede estar órdenes de magnitud por encima de las otras dos.
lista_s05 = [CORRIDAS_S05[e] for e in ESCALAS_S05]
fig_acc = rejilla(lista_s05, x="epoch", metrica="accuracy", columnas=3,
                  misma_y=True)
fig_acc.suptitle("Accuracy por epoch: crudo, [0, 1] y estandarizado", y=1.02)


def leyenda_por_conjunto(fig):
    """La leyenda común de rejilla copia las etiquetas del primer panel
    ("s05-crudo · train", …); aquí la dejamos solo con train/validation/test."""
    for leyenda in list(fig.legends):
        leyenda.remove()
    lineas, etiquetas = fig.axes[0].get_legend_handles_labels()
    fig.legend(lineas, [e.split(" · ")[-1] for e in etiquetas],
               loc="upper right", fontsize=8)


leyenda_por_conjunto(fig_acc)
plt.show()

fig_loss = rejilla(lista_s05, x="epoch", metrica="loss", columnas=3,
                   misma_y=True)
for ax in fig_loss.axes:                 # sharey: los tres paneles a la vez
    ax.set_yscale("log")
    ax.axhline(np.log(10), color="gray", linestyle=":", linewidth=1)
leyenda_por_conjunto(fig_loss)
fig_loss.suptitle("Loss (cross-entropy, escala log) por epoch · "
                  "punteada gris: adivinar uniforme, log 10 ≈ 2.30", y=1.02)
plt.show()

# %% [texto] s05-arranque-guia

# %% [codigo] s05-arranque
# Lupa sobre el arranque: las mismas tres configuraciones, pero solo 50 pasos
# y evaluando cada 2 pasos (eval_cada_pasos). Mismas semillas que arriba:
# mismos pesos iniciales y mismos batches, así que son los mismos primeros
# pasos de las corridas de 5 epochs, mirados de cerca.
ARRANQUE_S05 = {}
for escala in ESCALAS_S05:
    cfg = Config(id=f"s05-{escala}-arranque", seccion=5, capas=[784, 128, 10],
                 activacion="relu", optimizer="sgd", lr=0.03, batch=128,
                 epochs=5, max_pasos=50, eval_cada_pasos=2, escala=escala,
                 semilla_init=SEMILLA, semilla_orden=SEMILLA)
    ARRANQUE_S05[escala] = entrenar(cfg)

lista_arranque = [ARRANQUE_S05[e] for e in ESCALAS_S05]
n_pasos = int(max(c.historial["pasos"].max() for c in lista_arranque))
fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(13, 4.2))
curvas(lista_arranque, x="pasos", metrica="loss", conjuntos=("train",),
       ax=ax_loss, titulo=f"Primeros {n_pasos} pasos: loss de train (escala log)")
ax_loss.set_yscale("log")
ax_loss.axhline(np.log(10), color="gray", linestyle=":", linewidth=1)
curvas(lista_arranque, x="pasos", metrica="accuracy",
       conjuntos=("validation",), ax=ax_acc,
       titulo=f"Primeros {n_pasos} pasos: accuracy de validation")
ax_acc.axhline(0.1, color="gray", linestyle=":", linewidth=1,
               label="azar: 10 %")
ax_acc.legend(fontsize=8)
plt.tight_layout()
plt.show()

# %% [codigo] s05-tabla
# La parte de la tabla maestra que produjo esta sección.
display(tabla_maestra(secciones=[5]))

# %% [plegada] s05-apuesta-respuesta

# %% [texto] s05-pregunta-eta

# %% [plegada] s05-pregunta-eta-respuesta

# %% [texto] s05-que-viste
