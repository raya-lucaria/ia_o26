# Sección 17 · Una red convolucional, breve.
# Produce la corrida s17-cnn (Adam 1e-3, 50k limpio, mismas epochs y batch
# que el MLP elegido). Consume CORRIDAS["s16-elegido"]; si falta (el alumno
# saltó §16), usa el mejor MLP de CORRIDAS con datos "50k-limpio" por
# acc_validation, y si no hay ninguno entrena s04-oculta (8 epochs).
# Publica: construir_cnn, corrida_cnn, corrida_mlp. Consume la caja (s01–s03).

# %% [texto] s17-intro

# %% [codigo] s17-filtro-figura
# Un filtro 3×3 hecho a mano, para ver qué hace una convolución ANTES de
# entrenar nada. Este filtro resta la columna izquierda de la ventana a la
# derecha: responde a bordes verticales (más tinta a la derecha de la ventana
# da positivo; más tinta a la izquierda, negativo).
import torch.nn.functional as F

X_val01, y_val = DATOS["01"]["validation"]        # píxeles en [0, 1]
k_digito = int((y_val == 4).nonzero()[0])          # el primer 4 de validation
digito = X_val01[k_digito].detach().cpu().view(28, 28)
filtro = torch.tensor([[-1.0, 0.0, 1.0],
                       [-1.0, 0.0, 1.0],
                       [-1.0, 0.0, 1.0]])          # filas = u, columnas = v

# La convolución de PyTorch: entrada [B, canales, 28, 28], filtro
# [salidas, entradas, 3, 3]. padding=1 agrega un marco de ceros para que la
# salida también sea de 28×28.
mapa = F.conv2d(digito.view(1, 1, 28, 28), filtro.view(1, 1, 3, 3),
                padding=1)[0, 0]                   # [28, 28]

# Dos centros de ventana (renglón, columna), MISMOS 9 pesos: el máximo y el
# mínimo del mapa, buscando el mínimo a ≥ 5 píxeles para no encimar ventanas.
r0, c0 = divmod(int(mapa.argmax()), 28)
rr, cc = torch.meshgrid(torch.arange(28), torch.arange(28), indexing="ij")
lejos = (rr - r0).abs() + (cc - c0).abs() >= 5
posiciones = [(r0, c0), divmod(int(torch.where(lejos, mapa, 9.0).argmin()), 28)]
colores_pos = ["#d62728", "#9467bd"]
fig, (ax_x, ax_w, ax_z) = plt.subplots(
    1, 3, figsize=(14, 4.6), gridspec_kw={"width_ratios": [1, 0.55, 1]})
ax_x.imshow(digito, cmap="gray_r", vmin=0, vmax=1)
lim = float(mapa.abs().max())
ax_z.imshow(mapa, cmap="RdBu_r", vmin=-lim, vmax=lim)
for k, ((r, c), col) in enumerate(zip(posiciones, colores_pos)):
    ventana = digito[r - 1:r + 2, c - 1:c + 2]     # los 9 píxeles que lee
    valor = float((ventana * filtro).sum())        # suma de productos
    print(f"centro ({r:2d}, {c:2d}): Σ ventana·filtro = {valor:+.3f} "
          f"= mapa[{r}, {c}] = {float(mapa[r, c]):+.3f}")
    ax_x.add_patch(plt.Rectangle((c - 1.5, r - 1.5), 3, 3, fill=False,
                                 edgecolor=col, lw=2.5))
    ax_z.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False,
                                 edgecolor=col, lw=2.5))
    ax_z.annotate(f"{valor:+.2f}", (c, r), xytext=(2 + 13 * k, 26),  # rótulo abajo
                  color=col, fontsize=11, fontweight="bold",
                  arrowprops={"arrowstyle": "->", "color": col})
ax_w.imshow(filtro, cmap="RdBu_r", vmin=-1.5, vmax=1.5)
for u in range(3):
    for v in range(3):
        ax_w.text(v, u, f"{filtro[u, v]:+.0f}", ha="center", va="center",
                  fontsize=14)
ax_w.set(xticks=range(3), yticks=range(3), xlabel="columna v del filtro",
         ylabel="renglón u del filtro", title="El filtro: 9 pesos $w_{uv}$")
for ax, t in ((ax_x, f"Entrada: un {int(y_val[k_digito])} de validation"),
              (ax_z, "Salida: mapa de 28×28")):
    ax.set(title=t, xlabel="columna del píxel", ylabel="renglón del píxel")
for ax in (ax_x, ax_w, ax_z):
    ax.grid(False)
fig.suptitle("Una convolución: la MISMA ventana de 3×3 pesos recorre la imagen")
plt.tight_layout()
plt.show()

# %% [texto] s17-filtro-lee

# %% [codigo] s17-construir
# La CNN de esta sección. Los DATOS del notebook son planos, [B, 784]; la
# primera capa los vuelve a doblar como imagen [B, 1, 28, 28] (un canal:
# gris). Desde ahí: dos bloques conv 3×3 → ReLU → max-pooling 2×2, y al
# final una capa lineal, la misma de siempre, hacia los 10 logits.
def construir_cnn():
    return nn.Sequential(
        nn.Unflatten(1, (1, 28, 28)),                 # [B,784] → [B,1,28,28]
        nn.Conv2d(1, 16, kernel_size=3, padding=1),   # 16 filtros de 1×3×3
        nn.ReLU(),
        nn.MaxPool2d(2),                              # 28×28 → 14×14
        nn.Conv2d(16, 32, kernel_size=3, padding=1),  # 32 filtros de 16×3×3
        nn.ReLU(),
        nn.MaxPool2d(2),                              # 14×14 → 7×7
        nn.Flatten(),                                 # [B,32,7,7] → [B,1568]
        nn.Linear(32 * 7 * 7, 10),                    # → logits [B,10]
    )


# Pasamos un batch de 2 imágenes y anotamos la forma que sale de cada capa.
cnn_muestra = construir_cnn()
h = DATOS["estandar"]["validation"][0][:2].detach().cpu()
filas = [{"capa": "entrada", "forma de salida": str(list(h.shape)),
          "parámetros": 0}]
for capa in cnn_muestra:
    h = capa(h)
    filas.append({"capa": type(capa).__name__,
                  "forma de salida": str(list(h.shape)),
                  "parámetros": sum(p.numel() for p in capa.parameters())})
tabla_cnn = pd.DataFrame(filas)
display(tabla_cnn)
print("parámetros de la CNN:", int(tabla_cnn["parámetros"].sum()))

# Dibujo de la arquitectura: un bloque por capa, con su forma (sin el batch).
fig, ax = plt.subplots(figsize=(15, 3.2))
tonos = {"Conv2d": "#aec7e8", "ReLU": "#ffbb78", "MaxPool2d": "#98df8a",
         "Linear": "#c5b0d5"}
for i, fila in tabla_cnn.iterrows():
    forma = fila["forma de salida"].strip("[]").split(", ")[1:]
    ax.add_patch(plt.Rectangle((i * 1.6, 0), 1.3, 1, lw=1.5, edgecolor="k",
                               facecolor=tonos.get(fila["capa"], "#eeeeee")))
    ax.text(i * 1.6 + 0.65, 0.68, fila["capa"], ha="center", fontsize=9,
            fontweight="bold")
    ax.text(i * 1.6 + 0.65, 0.32, "×".join(forma), ha="center", fontsize=9)
    if i:
        ax.annotate("", (i * 1.6, 0.5), (i * 1.6 - 0.3, 0.5),
                    arrowprops={"arrowstyle": "->"})
ax.set_xlim(-0.2, len(tabla_cnn) * 1.6)
ax.set_ylim(-0.2, 1.2)
ax.axis("off")
ax.set_title("La CNN: forma de cada capa (canales × alto × ancho, sin el batch)")
plt.show()
del cnn_muestra, h

# %% [texto] s17-arquitectura-lee

# %% [texto] s17-apuesta

# %% [codigo] s17-elegido
# El MLP contra el que comparamos: el que §16 eligió por VALIDATION.
# Si saltaste §16, repetimos su regla aquí (nunca se mira test para elegir).
if "s16-elegido" in CORRIDAS:
    corrida_mlp = CORRIDAS["s16-elegido"]
    print("MLP elegido en §16:", corrida_mlp.id)
else:
    def acc_val_mejor(c):
        h = c.historial
        return float(h[h["epoch"] == c.mejor_epoch].iloc[-1]["acc_validation"])

    candidatos = [c for c in CORRIDAS.values()
                  if c.config.datos == "50k-limpio" and c.config.modelo is None
                  and c.config.idx_train is None and not c.divergio
                  and c.config.ruido_etiquetas == 0.0]
    if candidatos:
        corrida_mlp = max(candidatos, key=acc_val_mejor)
        print("AVISO: no existe s16-elegido; uso el mejor MLP por validation:",
              corrida_mlp.id)
    else:
        print("AVISO: no hay ningún MLP entrenado con los 50k; entreno la "
              "línea base s04-oculta (8 epochs).")
        corrida_mlp = entrenar(Config(id="s04-oculta", seccion=4,
                                      capas=[784, 128, 10], activacion="relu",
                                      optimizer="adam", lr=1e-3, epochs=8))
cfg_mlp = corrida_mlp.config
print("capas:", cfg_mlp.capas, "· optimizer:", cfg_mlp.optimizer,
      "· η:", cfg_mlp.lr, "· weight_decay:", cfg_mlp.weight_decay)
print("epochs:", cfg_mlp.epochs, "· tope de pasos:", cfg_mlp.max_pasos,
      "· batch:", cfg_mlp.batch, "· escala:", cfg_mlp.escala,
      "· parámetros:", corrida_mlp.parametros)

# %% [codigo] s17-entrena
# La CNN, con los mismos datos que el MLP: los 50 000 de train, la misma
# escala de entrada, el mismo batch y las mismas epochs (y el mismo tope de
# pasos y frecuencia de evaluación, si el MLP los tenía). El optimizer es
# Adam con η = 1e-3 y sin weight decay: si el MLP elegido usó otro, la tabla
# de abajo lo muestra, y la comparación es entre ESTAS dos corridas.
cfg_cnn = Config(id="s17-cnn", seccion=17, modelo=construir_cnn,
                 optimizer="adam", lr=1e-3, datos="50k-limpio",
                 epochs=cfg_mlp.epochs, max_pasos=cfg_mlp.max_pasos,
                 eval_cada_pasos=cfg_mlp.eval_cada_pasos,
                 batch=cfg_mlp.batch, escala=cfg_mlp.escala)
corrida_cnn = entrenar(cfg_cnn)
print("epochs:", cfg_cnn.epochs, "· batch:", cfg_cnn.batch,
      "· escala:", cfg_cnn.escala, "· parámetros:", corrida_cnn.parametros)

# %% [codigo] s17-curvas
# Las dos redes lado a lado: MISMO eje y en cada renglón para poder comparar.
pareja = [("MLP elegido", corrida_mlp), ("CNN", corrida_cnn)]
fig, ejes = plt.subplots(2, 2, figsize=(13, 8), sharey="row")
for j, (nombre, c) in enumerate(pareja):
    curvas([c], metrica="loss", ax=ejes[0, j], titulo=f"{nombre}: loss")
    curvas([c], metrica="accuracy", ax=ejes[1, j],
           titulo=f"{nombre}: accuracy")
plt.tight_layout()
plt.show()


# Tabla: parámetros y métricas en la mejor epoch POR VALIDATION de cada una.
def resumen(nombre, c):
    h = c.historial
    fila = h[h["epoch"] == c.mejor_epoch].iloc[-1]
    return {"red": nombre, "id": c.id, "optimizer": c.config.optimizer,
            "η": c.config.lr, "weight_decay": c.config.weight_decay,
            "parámetros": c.parametros,
            "mejor epoch (validation)": c.mejor_epoch,
            "loss validation": float(fila["loss_validation"]),
            "accuracy validation": float(fila["acc_validation"]),
            "errores en validation": round((1 - fila["acc_validation"])
                                           * len(DATOS["01"]["validation"][1])),
            "segundos": float(h["segundos"].iloc[-1])}


tabla_17 = pd.DataFrame([resumen(n, c) for n, c in pareja]).set_index("red")
display(tabla_17.round(4))
dif = (tabla_17.loc["CNN", "accuracy validation"]
       - tabla_17.loc["MLP elegido", "accuracy validation"])
print(f"CNN − MLP en accuracy de validation: {100 * dif:+.2f} puntos")
print(f"la CNN usa {corrida_cnn.parametros / corrida_mlp.parametros:.2f} "
      "veces los parámetros del MLP")

# %% [texto] s17-curvas-lee

# %% [codigo] s17-filtros
# ¿Qué aprendió la primera capa? Sus 16 filtros de 3×3, y lo que cada uno
# produce sobre el mismo dígito de validation de la figura del principio.
cnn = cargar(corrida_cnn, "mejor")                # en DEVICE, modo eval()
conv1 = cnn[1]                                    # Conv2d(1, 16, 3)
W1 = conv1.weight.detach().cpu()[:, 0]            # [16, 3, 3]
lim = float(W1.abs().max())
fig, ejes = plt.subplots(2, 8, figsize=(14, 4))
for f, ax in enumerate(ejes.flat):
    im = ax.imshow(W1[f], cmap="RdBu_r", vmin=-lim, vmax=lim)
    ax.set_title(f"filtro {f}")
    ax.set_xticks(range(3))
    ax.set_yticks(range(3))
    ax.grid(False)
for ax in ejes[1]:
    ax.set_xlabel("columna v")
for ax in ejes[:, 0]:
    ax.set_ylabel("renglón u")
fig.colorbar(im, ax=ejes, shrink=0.8).set_label("peso (rojo +, azul −)")
fig.suptitle("Los 16 filtros aprendidos de la primera capa (3×3 cada uno)")
plt.show()

# Mapas de activación: la salida de conv1 + ReLU (capas 0–2 del Sequential).
x = DATOS[cfg_cnn.escala]["validation"][0][k_digito:k_digito + 1]
with torch.no_grad():
    mapas = cnn[:3](x)[0].cpu()                   # [16, 28, 28]
fig, ejes = plt.subplots(2, 9, figsize=(16, 4.2))
ejes[0, 0].imshow(digito, cmap="gray_r")
ejes[0, 0].set_title("entrada")
ejes[1, 0].axis("off")
for f in range(16):
    ax = ejes.flat[f + 1 if f < 8 else f + 2]
    ax.imshow(mapas[f], cmap="magma")
    ax.set_title(f"mapa {f}")
for ax in ejes.flat:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
fig.suptitle("Mapas de activación de la primera capa (después de la ReLU) "
             "para el mismo dígito; cada mapa con su propia escala")
plt.show()
del cnn, conv1, W1, mapas                         # liberamos la CNN restaurada

# %% [texto] s17-filtros-lee

# %% [codigo] s17-confusion
# Matrices de confusión en VALIDATION, una junto a otra.
# Filas = clase real, columnas = clase predicha. La diagonal (aciertos) va
# en gris para que el color lo lleven los ERRORES, con la misma escala.
def predecir(corrida):
    modelo = cargar(corrida, "mejor")
    X, y = DATOS[corrida.config.escala]["validation"]
    with torch.no_grad():
        p = torch.cat([modelo(X[i:i + 1000]).argmax(1)
                       for i in range(0, len(X), 1000)])
    return y.cpu(), p.cpu()


def confusion(y, p):
    return torch.bincount(y * 10 + p, minlength=100).view(10, 10).numpy()


M = {n: confusion(*predecir(c)) for n, c in pareja}
fuera = {n: mat - np.diag(np.diag(mat)) for n, mat in M.items()}
tope = max(f.max() for f in fuera.values())
fig, ejes = plt.subplots(1, 2, figsize=(14, 6.4))
for ax, (n, matriz) in zip(ejes, M.items()):
    errores = np.where(np.eye(10, dtype=bool), np.nan, matriz)
    im = ax.imshow(errores, cmap="Reds", vmin=0, vmax=tope)
    for i in range(10):
        for j in range(10):
            ax.text(j, i, matriz[i, j], ha="center", va="center", fontsize=8,
                    color="dimgray" if i == j else "black")
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_xlabel("clase predicha (columna)")
    ax.set_ylabel("clase real (fila)")
    ax.set_title(f"{n}: {int(fuera[n].sum())} errores de {int(matriz.sum())}")
    ax.grid(False)
fig.colorbar(im, ax=ejes, shrink=0.8).set_label("conteo fuera de la diagonal")
fig.suptitle("Matrices de confusión en validation: MLP elegido vs CNN")
plt.show()

# Errores por clase real: ¿en qué dígitos cambia algo?
por_clase = pd.DataFrame({n: f.sum(axis=1) for n, f in fuera.items()})
por_clase.index.name = "clase real"
por_clase["CNN − MLP"] = por_clase["CNN"] - por_clase["MLP elegido"]
display(por_clase.T)

# %% [texto] s17-que-viste

# %% [plegada] s17-apuesta-respuesta
