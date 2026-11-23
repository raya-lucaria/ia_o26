# Sección 10 del notebook 02 · Early stopping.
# Produce las corridas s10-control (la consume §15: no cambiar su Config) y
# s10-paciencia. El texto de cada celda [texto]/[plegada] vive en
# s10_early_stopping.texto.md.

# %% [texto] s10-intro

# %% [codigo] s10-config
# El caso que sobreajusta: pocos datos, etiquetas con ruido y una red grande.
CFG_S10 = Config(id="s10-control", seccion=10, capas=[784, 256, 256, 10],
                 activacion="relu", optimizer="adam", lr=1e-3, batch=64,
                 epochs=80, idx_train=subconjunto(2000), ruido_etiquetas=0.2,
                 datos="2k-ruido20")

# Cuántos parámetros tiene la red: W^(l) tiene d_l · d_(l-1) entradas y
# b^(l) tiene d_l; la suma es θ.
anchos = CFG_S10.capas
n_parametros = sum(anchos[l] * anchos[l - 1] + anchos[l]
                   for l in range(1, len(anchos)))
print(f"red {anchos}: {n_parametros:,} parámetros")
print(f"ejemplos de train: {len(CFG_S10.idx_train):,}"
      f"  ({CFG_S10.ruido_etiquetas:.0%} con la etiqueta cambiada)")
print(f"parámetros por ejemplo de train: "
      f"{n_parametros / len(CFG_S10.idx_train):,.0f}")
dibujar_red(anchos, titulo="La red de §10: dos ocultas de 256")
plt.show()

# %% [texto] s10-apuesta

# %% [plegada] s10-apuesta-respuesta

# %% [codigo] s10-entrenar
# 80 epochs SIN paciencia: queremos ver todo lo que pasa después del mejor
# momento. entrenar guarda dos checkpoints: el de la mejor epoch por loss de
# validation y el de la última.
corrida_s10 = entrenar(CFG_S10)
h10 = corrida_s10.historial
print(f"epochs corridas: {int(h10['epoch'].max())}")
print(f"mejor epoch por loss de validation: {corrida_s10.mejor_epoch:g}")

# %% [texto] s10-paciencia-explica

# %% [codigo] s10-simular-paciencia
def epoch_de_parada(historial, paciencia=6):
    """Dónde habría parado early stopping, simulado sobre un historial.

    Recorre las evaluaciones en orden y cuenta cuántas seguidas van sin
    mejorar el mínimo de la loss de validation (un empate no mejora). La
    primera vez que el contador llega a `paciencia`, ésa es la epoch de
    parada. Devuelve (epoch de parada, mejor epoch hasta ese momento); si el
    contador nunca llega, (None, mejor epoch). Solo lee validation.
    """
    mejor, mejor_epoch, sin_mejora = float("inf"), None, 0
    for _, fila in historial.iterrows():
        if fila["loss_validation"] < mejor:
            mejor, mejor_epoch, sin_mejora = fila["loss_validation"], fila["epoch"], 0
        else:
            sin_mejora += 1
            if sin_mejora == paciencia:
                return fila["epoch"], mejor_epoch
    return None, mejor_epoch


PACIENCIA = 6
parada_simulada, mejor_al_parar = epoch_de_parada(h10, PACIENCIA)
ultima_epoch = h10["epoch"].max()
print(f"mínimo de la loss de validation en las {ultima_epoch:g} epochs: "
      f"epoch {corrida_s10.mejor_epoch:g}")
if parada_simulada is None:
    print(f"paciencia {PACIENCIA}: nunca se agotó; la corrida no habría parado")
else:
    print(f"paciencia {PACIENCIA}: habría parado en la epoch {parada_simulada:g} "
          f"y restaurado la epoch {mejor_al_parar:g}")
    print(f"epochs ahorradas: {ultima_epoch - parada_simulada:g} de {ultima_epoch:g}")
    if mejor_al_parar != corrida_s10.mejor_epoch:
        print("ojo: después de la parada validation volvió a mejorar; early "
              "stopping se habría quedado con un mínimo anterior")

# %% [codigo] s10-curvas
def marcar_parada(ax, mejor, parada, ultima):
    """Línea en la mejor epoch, línea en la parada y sombra de lo ahorrado."""
    ax.axvline(mejor, color="black", ls="--", lw=1.2,
               label=f"mínimo de la loss de validation ({mejor:g})")
    if parada is not None:
        ax.axvline(parada, color="crimson", ls=":", lw=1.5,
                   label=f"paciencia {PACIENCIA} para aquí ({parada:g})")
        ax.axvspan(parada, ultima, color="crimson", alpha=0.08,
                   label="epochs que early stopping se ahorra")


fig, (ax_l, ax_a) = plt.subplots(1, 2, figsize=(13, 4.5))
# Solo train y validation: las curvas sirven para elegir, y test no elige.
curvas([corrida_s10], x="epoch", metrica="loss",
       conjuntos=("train", "validation"), ax=ax_l, titulo="Loss por epoch")
curvas([corrida_s10], x="epoch", metrica="accuracy",
       conjuntos=("train", "validation"), ax=ax_a,
       titulo="Accuracy por epoch (train contra las etiquetas alteradas)")
for ax in (ax_l, ax_a):
    marcar_parada(ax, corrida_s10.mejor_epoch, parada_simulada, ultima_epoch)
    ax.legend(fontsize=8)
fig.suptitle("§10 · 2000 ejemplos, 20 % de etiquetas alteradas, sin paciencia")
plt.tight_layout()
plt.show()

# %% [texto] s10-memoriza-explica

# %% [codigo] s10-memoriza
# Los 2000 ejemplos tal como los vio la red: datos_de_entrenamiento (de la
# caja) aplica el subconjunto y altera las etiquetas con la misma semilla que
# usó entrenar. Las etiquetas verdaderas siguen en DATOS.
X10, y10_ruido = datos_de_entrenamiento(CFG_S10)
X_tr, y_tr = DATOS[CFG_S10.escala]["train"]
idx10 = CFG_S10.idx_train.to(DEVICE)
idx10 = idx10[idx10 < len(X_tr)]            # igual que la caja (RAPIDO)
y10_limpia = y_tr[idx10]
alterada = y10_ruido != y10_limpia          # máscara: dónde se cambió
print(f"etiquetas alteradas: {int(alterada.sum())} de {len(y10_ruido)}")


@torch.no_grad()
def predecir(modelo, X):
    """La clase con el logit más grande (cargar ya deja la red en eval())."""
    return modelo(X).argmax(dim=1)


filas = []
for cual in ("mejor", "ultima"):
    pred = predecir(cargar(corrida_s10, cual), X10)
    filas.append({
        "checkpoint": cual,
        "limpias: acierta la verdadera":
            (pred[~alterada] == y10_limpia[~alterada]).float().mean().item(),
        "alteradas: repite la etiqueta falsa":
            (pred[alterada] == y10_ruido[alterada]).float().mean().item(),
        "alteradas: acierta la verdadera":
            (pred[alterada] == y10_limpia[alterada]).float().mean().item(),
    })
memoria = pd.DataFrame(filas).set_index("checkpoint")
display(memoria.round(3))

ax = memoria.T.plot.bar(figsize=(9, 4), rot=0, color=["#555555", "crimson"])
ax.set_ylim(0, 1.05)
ax.set_ylabel("fracción de los ejemplos de train")
ax.set_title("¿Cuánto ruido memorizó la red? Mejor epoch vs última")
ax.legend(title="checkpoint")
plt.tight_layout()
plt.show()

# %% [texto] s10-restaurar-explica

# %% [codigo] s10-restaurar
# Restauramos los dos checkpoints y medimos cada uno desde cero con medir y
# evaluar de la caja. Train se mide sobre lo que la red vio: los 2000
# ejemplos con sus etiquetas alteradas. Validation y test, completos y limpios.
filas = []
for cual, epoch in (("mejor", corrida_s10.mejor_epoch), ("ultima", ultima_epoch)):
    modelo = cargar(corrida_s10, cual)
    l_tr, a_tr = medir(modelo, X10, y10_ruido)          # medir es de la caja
    l_va, a_va = evaluar(modelo, CFG_S10.escala, "validation")
    l_te, a_te = evaluar(modelo, CFG_S10.escala, "test")   # la única vez
    filas.append({"checkpoint": cual, "epoch": epoch,
                  "loss train": l_tr, "acc train": a_tr,
                  "loss validation": l_va, "acc validation": a_va,
                  "loss test": l_te, "acc test": a_te})
tabla_s10 = pd.DataFrame(filas).set_index("checkpoint")
display(tabla_s10.round(3))

# %% [texto] s10-corrida-paciencia-explica

# %% [codigo] s10-corrida-paciencia
# La misma Config, ahora con paciencia real: entrenar para sola.
CFG_S10_P = Config(id="s10-paciencia", seccion=10, capas=[784, 256, 256, 10],
                   activacion="relu", optimizer="adam", lr=1e-3, batch=64,
                   epochs=80, idx_train=subconjunto(2000), ruido_etiquetas=0.2,
                   paciencia=PACIENCIA, datos="2k-ruido20")
corrida_s10_p = entrenar(CFG_S10_P)
hp = corrida_s10_p.historial
fin_p = hp["epoch"].max()
paro = bool(hp["parada_temprana"].iloc[-1])   # ¿se agotó la paciencia?
if paro:
    print(f"paciencia {PACIENCIA}: se detuvo sola en la epoch {fin_p:g}")
else:
    print(f"paciencia {PACIENCIA}: no se agotó; corrió todo el presupuesto "
          f"({fin_p:g} epochs)")
sim = "no para" if parada_simulada is None else f"epoch {parada_simulada:g}"
print(f"la simulación sobre s10-control decía: {sim}")
print(f"checkpoint que entrega: epoch {corrida_s10_p.mejor_epoch:g}")

# El modelo que de verdad entrega early stopping, junto a los del control.
modelo_p = cargar(corrida_s10_p, "mejor")
l_va, a_va = evaluar(modelo_p, CFG_S10.escala, "validation")
l_te, a_te = evaluar(modelo_p, CFG_S10.escala, "test")
fila_p = pd.DataFrame([{"epoch": corrida_s10_p.mejor_epoch,
                        "loss validation": l_va, "acc validation": a_va,
                        "loss test": l_te, "acc test": a_te}],
                      index=pd.Index(["con paciencia"], name="checkpoint"))
display(pd.concat([tabla_s10.drop(columns=["loss train", "acc train"]),
                   fila_p]).round(3))

fig, ax = plt.subplots(figsize=(8, 4.5))
curvas([corrida_s10, corrida_s10_p], x="epoch", metrica="loss",
       conjuntos=("validation",), ax=ax,
       titulo=f"Loss de validation: sin paciencia vs con paciencia {PACIENCIA}")
if paro:
    ax.axvline(fin_p, color="crimson", ls=":", lw=1.5, label="aquí se detuvo")
    ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
display(tabla_maestra([10]))

# %% [texto] s10-que-viste
