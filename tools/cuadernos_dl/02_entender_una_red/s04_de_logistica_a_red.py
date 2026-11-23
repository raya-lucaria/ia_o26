# Sección 4 · De la regresión logística a la red.
# Produce las corridas s04-logistica y s04-oculta (§6 y §16 reutilizan
# s04-oculta: NO cambiar su Config). Publica: corrida_logistica,
# corrida_oculta. Consume la caja (s01–s03).

# %% [texto] s04-intro

# %% [codigo] s04-logistica-red
# Una red SIN capas ocultas: capas = [784, 10]. Es una sola capa lineal:
#   z = W x + b,  W de 10 × 784 (filas = dígito destino, columnas = píxel)
# y nada más. Los 10 números z son los logits; CrossEntropyLoss los
# convierte en probabilidades con softmax (sección 18) y les cobra −ln p.
red_logistica = construir_red([784, 10], activacion="identidad")
print(red_logistica)

capa = next(m for m in red_logistica.modules()
            if isinstance(m, torch.nn.Linear))
print("W:", tuple(capa.weight.shape), "(filas = dígito i, columnas = píxel j)")
print("b:", tuple(capa.bias.shape))
print("parámetros:", sum(p.numel() for p in red_logistica.parameters()),
      "= 10·784 + 10")

# Un batch de 3 imágenes de train, para ver las formas de punta a punta.
X_tr, y_tr = DATOS["estandar"]["train"]
with torch.no_grad():
    logits = red_logistica.to(DEVICE)(X_tr[:3])
print("entrada:", tuple(X_tr[:3].shape), "→ logits:", tuple(logits.shape))
del red_logistica, capa, logits                   # aún sin entrenar: se tira

dibujar_red([784, 10], titulo="Regresión logística multiclase: [784, 10]")
plt.show()

# %% [texto] s04-logistica-entrena-texto

# %% [codigo] s04-logistica-entrena
# La regresión logística de la unidad 9, entrenada como una red: Adam,
# η = 1e-3, batches de 128, 8 epochs sobre los 50 000 de train.
cfg_logistica = Config(id="s04-logistica", seccion=4, capas=[784, 10],
                       activacion="identidad", optimizer="adam", lr=1e-3,
                       epochs=8)
corrida_logistica = entrenar(cfg_logistica)

fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(12, 4))
curvas([corrida_logistica], metrica="loss", ax=ax_loss,
       titulo="Logística [784, 10]: loss (cross-entropy)")
curvas([corrida_logistica], metrica="accuracy", ax=ax_acc,
       titulo="Logística [784, 10]: accuracy")
plt.tight_layout()
plt.show()

# El historial: una fila por evaluación (epoch 0 = antes de entrenar).
columnas = ["epoch", "loss_train", "loss_validation", "loss_test",
            "acc_train", "acc_validation", "acc_test"]
display(corrida_logistica.historial[columnas].round(4))
print("mejor epoch por validation:", corrida_logistica.mejor_epoch)

# %% [texto] s04-logistica-mira

# %% [texto] s04-pesos-texto

# %% [codigo] s04-pesos
# Cada fila i de W tiene 784 pesos, uno por píxel: se puede volver a doblar
# como una imagen de 28 × 28. Rojo = ese píxel encendido SUBE el logit del
# dígito i; azul = lo BAJA. Usamos el checkpoint de la mejor epoch.
modelo_logistica = cargar(corrida_logistica, "mejor")
lineal = next(m for m in modelo_logistica.modules()
              if isinstance(m, torch.nn.Linear))
W = lineal.weight.detach().cpu()                  # [10, 784]
print("W:", tuple(W.shape), "→ 10 imágenes de 28 × 28")

# Escala simétrica alrededor de 0 (mapa divergente): blanco = peso 0.
limite = float(W.abs().quantile(0.99))
fig, ejes = plt.subplots(2, 5, figsize=(13, 6))
for i, ax in enumerate(ejes.flat):
    im = ax.imshow(W[i].reshape(28, 28), cmap="RdBu_r",
                   vmin=-limite, vmax=limite)
    ax.set_title(f"fila i = {i} (dígito {i})")
    ax.set_xticks([0, 27])
    ax.set_yticks([0, 27])
    ax.grid(False)
for ax in ejes[1]:
    ax.set_xlabel("columna del píxel")
for ax in ejes[:, 0]:
    ax.set_ylabel("renglón del píxel")
barra = fig.colorbar(im, ax=ejes, shrink=0.8)
barra.set_label("peso $w_{ij}$: cambio del logit $z_i$ si el píxel $j$\n"
                "sube una unidad (rojo: sube; azul: baja)")
fig.suptitle("Los 10 renglones de W de la logística, doblados a 28 × 28")
plt.show()
del modelo_logistica, lineal

# %% [texto] s04-neurona

# %% [codigo] s04-relu
# La activación ReLU, g(z) = max(0, z), y su derivada g'(z) (g'(0) = 0
# por convención, como en el notebook 01).
z = torch.linspace(-4, 4, 401)
g = torch.relu(z)
g_prima = (z > 0).float()

fig, (ax_g, ax_d) = plt.subplots(1, 2, figsize=(11, 3.6))
ax_g.plot(z, g, color=COLORES["train"], lw=2.5, label="ReLU: max(0, z)")
ax_g.plot(z, z, color="gray", ls="--", lw=1, label="identidad: z")
ax_g.set_title("La activación ReLU")
ax_g.set_xlabel("preactivación z")
ax_g.set_ylabel("activación g(z)")
ax_g.legend()
ax_d.plot(z[z <= 0], g_prima[z <= 0], color=COLORES["train"], lw=2.5)
ax_d.plot(z[z > 0], g_prima[z > 0], color=COLORES["train"], lw=2.5,
          label="g'(z)")
ax_d.set_ylim(-0.2, 1.2)
ax_d.set_title("Su derivada: 0 o 1")
ax_d.set_xlabel("preactivación z")
ax_d.set_ylabel("g'(z)")
ax_d.legend()
plt.tight_layout()
plt.show()

# %% [codigo] s04-colapso
# ¿Por qué hace falta la activación? Dos capas SIN activación (identidad)
# colapsan en una sola capa afín: W' = W2 W1 y b' = W2 b1 + b2.
torch.manual_seed(SEMILLA)
dos_lineales = construir_red([784, 128, 10], activacion="identidad").to(DEVICE)
c1, c2 = [m for m in dos_lineales.modules() if isinstance(m, torch.nn.Linear)]
x = X_tr[:5]
with torch.no_grad():
    W_prima = c2.weight @ c1.weight               # [10, 128] @ [128, 784]
    b_prima = c2.weight @ c1.bias + c2.bias       # [10]
    por_la_red = dos_lineales(x)
    por_una_capa = x @ W_prima.T + b_prima        # filas = observaciones
print("W':", tuple(W_prima.shape), "  b':", tuple(b_prima.shape))
print("¿la red de dos capas lineales = una sola capa afín?",
      torch.allclose(por_la_red, por_una_capa, atol=1e-4))
del dos_lineales, c1, c2, W_prima, b_prima

# %% [texto] s04-apuesta

# %% [codigo] s04-tabla-parametros
# Las dos redes, dibujadas, y sus parámetros capa por capa:
# la capa l tiene d_l · d_{l-1} pesos + d_l sesgos.
def tabla_parametros(capas):
    filas = []
    for l in range(1, len(capas)):
        d_ant, d_l = capas[l - 1], capas[l]
        filas.append({"capa l": l, "d_{l-1}": d_ant, "d_l": d_l,
                      "pesos d_l·d_{l-1}": d_l * d_ant, "sesgos d_l": d_l,
                      "total": d_l * d_ant + d_l})
    tabla = pd.DataFrame(filas)
    total = int(tabla["total"].sum())
    # Comprobación: la fórmula coincide con lo que cuenta PyTorch.
    red = construir_red(capas, activacion="relu")
    assert total == sum(p.numel() for p in red.parameters())
    return tabla, total


for capas in ([784, 10], [784, 128, 10]):
    tabla, total = tabla_parametros(capas)
    print(f"\nRed {capas}: {total:,} parámetros")
    display(tabla)

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 4))
dibujar_red([784, 10], ax=ax_a, titulo="Logística: [784, 10]")
dibujar_red([784, 128, 10], ax=ax_b, titulo="Una capa oculta: [784, 128, 10]")
plt.show()

# %% [codigo] s04-oculta-entrena
# La red de una capa oculta: 128 neuronas ReLU entre la entrada y la salida.
# Mismo optimizer, η, batch y epochs que la logística: solo cambia la red.
# Esta corrida es la LÍNEA BASE del notebook (la reutilizan §6 y §16).
cfg_oculta = Config(id="s04-oculta", seccion=4, capas=[784, 128, 10],
                    activacion="relu", optimizer="adam", lr=1e-3, epochs=8)
corrida_oculta = entrenar(cfg_oculta)

# %% [codigo] s04-compara
# Las dos corridas lado a lado: columnas = red, renglones = loss y accuracy,
# mismos ejes en cada renglón. La línea punteada gris marca la mejor epoch
# de cada red, elegida con la loss de validation (nunca con test).
pareja = [(corrida_logistica, "Logística [784, 10]"),
          (corrida_oculta, "Una oculta [784, 128, 10]")]
fig, ejes = plt.subplots(2, 2, figsize=(12, 7.5), sharex=True, sharey="row")
for col, (c, nombre) in enumerate(pareja):
    curvas([c], metrica="loss", ax=ejes[0, col], titulo=f"{nombre}: loss")
    curvas([c], metrica="accuracy", ax=ejes[1, col],
           titulo=f"{nombre}: accuracy")
    for ax in ejes[:, col]:
        ax.axvline(c.mejor_epoch, color="gray", ls=":", lw=1.5)
        ax.legend(fontsize=8)
# La epoch 0 (≈ 10 % de aciertos) aplastaría las diferencias finales:
# el eje de accuracy arranca en lo peor que se ve desde la epoch 1.
desde_1 = [c.historial.loc[c.historial["epoch"] >= 1,
                           ["acc_train", "acc_validation", "acc_test"]]
           for c, _ in pareja]
piso = min(float(np.nanmin(d.to_numpy())) for d in desde_1 if len(d))
ejes[1, 0].set_ylim(max(0.0, piso - 0.02), 1.0)
ejes[1, 0].text(0.02, 0.03, "la epoch 0 (≈ 10 %) queda debajo del eje",
                transform=ejes[1, 0].transAxes, fontsize=8, color="gray")
fig.tight_layout()
plt.show()

display(tabla_maestra([4]))

# Error de validation en la mejor epoch (elegida con validation, no con test).
def error_validation(corrida):
    h = corrida.historial
    fila = h[h["epoch"] == corrida.mejor_epoch].iloc[-1]
    return 1.0 - float(fila["acc_validation"])


e_log = error_validation(corrida_logistica)
e_oculta = error_validation(corrida_oculta)
print(f"error de validation, logística:   {e_log:.2%}")
print(f"error de validation, una oculta:  {e_oculta:.2%}")
print(f"cambio en accuracy de validation al agregar la capa oculta: "
      f"{100 * (e_log - e_oculta):+.2f} puntos")
if e_oculta > 0:
    print(f"cociente de errores logística / oculta: {e_log / e_oculta:.2f}")
print("¿la red oculta se equivoca menos de la mitad de las veces? (opción d):",
      "sí" if e_oculta < e_log / 2 else "no")

# %% [plegada] s04-apuesta-respuesta

# %% [texto] s04-que-viste
