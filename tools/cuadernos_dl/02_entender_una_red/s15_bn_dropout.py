# Sección 15 · Batch normalization y dropout.
# Produce: s15-sin-bn-003, s15-bn-003, s15-sin-bn-03, s15-bn-03, s15-dropout.
# Consume: s10-control (de §10); si falta, la entrena con la misma Config de §10.

# %% [texto] s15-intro

# %% [texto] s15-bn-formula

# %% [codigo] s15-bn-donde
# Dónde va batch normalization: entre la capa lineal y la ReLU.
# Construimos la red de §13 (seis ocultas de 128) con y sin BN e imprimimos
# sus primeras capas para ver el orden de los módulos.
import copy
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import pandas as pd

BASE_PROFUNDA = config_profunda("relu", id="s15-muestra", seccion=15)
print("capas:", BASE_PROFUNDA.capas)

for con_bn in (False, True):
    red_muestra = construir_red(BASE_PROFUNDA.capas, "relu",
                                batch_norm=con_bn, init=BASE_PROFUNDA.init)
    print(f"\n--- batch_norm={con_bn}: los primeros 6 módulos de "
          f"{len(red_muestra)} ---")
    for i, modulo in enumerate(list(red_muestra)[:6]):
        print(f"  [{i}] {modulo}")

# γ (weight) y β (bias) de la primera BN: empiezan en 1 y en 0,
# así que al inicializar BN solo estandariza; luego γ y β se aprenden.
bn = next(m for m in red_muestra if isinstance(m, nn.BatchNorm1d))
print("\nγ inicial (primeros 5):", bn.weight.data[:5].tolist())
print("β inicial (primeros 5):", bn.bias.data[:5].tolist())
print("parámetros por capa de BN: 2 ×", bn.num_features,
      "(γ y β por neurona)")

# %% [texto] s15-preact-explica

# %% [codigo] s15-preact
# Pre-activación z = lo que entra a cada ReLU, medida al inicializar,
# antes de cualquier paso de gradient descent. Un hook (gancho) es una
# función que PyTorch llama cada vez que un módulo recibe su entrada.
def preactivaciones(con_bn, n=1024):
    torch.manual_seed(BASE_PROFUNDA.semilla_init)    # mismos pesos iniciales
    red = construir_red(BASE_PROFUNDA.capas, "relu", batch_norm=con_bn,
                        init=BASE_PROFUNDA.init).to(DEVICE)
    red.train()          # como en el entrenamiento: BN usa las del batch
    medidas = []

    def gancho(modulo, entrada):
        z = entrada[0]                               # [n, 128]
        medidas.append((z.mean().item(), z.std().item()))

    relus = [m for m in red if isinstance(m, nn.ReLU)]
    ganchos = [m.register_forward_pre_hook(gancho) for m in relus]
    X = DATOS["estandar"]["train"][0][:n]
    with torch.no_grad():
        red(X)
    for g in ganchos:
        g.remove()                                   # no dejar ganchos vivos
    return pd.DataFrame(medidas, columns=["media", "desviacion"],
                        index=pd.RangeIndex(1, len(medidas) + 1, name="capa"))


PRE = {"sin BN": preactivaciones(False), "con BN": preactivaciones(True)}
display(pd.concat(PRE, axis=1).round(3))

COLOR_BN = {"sin BN": "#7f7f7f", "con BN": "#9467bd"}
fig, ejes = plt.subplots(1, 2, figsize=(11, 3.8), dpi=100)
for ax, col, nombre in zip(ejes, ["media", "desviacion"],
                           ["Media de z", "Desviación estándar de z"]):
    for k, (etiqueta, df) in enumerate(PRE.items()):
        ax.bar(df.index + (k - 0.5) * 0.38, df[col], width=0.38,
               color=COLOR_BN[etiqueta], label=etiqueta)
    ax.set_xlabel("capa oculta")
    ax.set_ylabel(nombre.lower())
    ax.set_title(f"{nombre} al inicializar, por capa")
    ax.set_xticks(PRE["sin BN"].index)
    ax.legend()
ejes[0].axhline(0, color="black", lw=0.8)
ejes[1].axhline(1, color="black", lw=0.8, ls="--")
fig.tight_layout()
plt.show()

# %% [texto] s15-preact-lee

# %% [texto] s15-apuesta

# %% [codigo] s15-bn-entrenar
# Cuatro corridas: {sin BN, con BN} × {η = 0.03, η = 0.3}.
# Todo lo demás igual: red de §13 con ReLU, SGD sin momentum, batch 128,
# mismos pesos iniciales (semilla_init) y mismo orden de batches.
# Una corrida que diverge no truena: entrenar la marca y la detiene.
CORRIDAS_BN = {}
for lr, sufijo in [(0.03, "003"), (0.3, "03")]:
    for con_bn in (False, True):
        ident = f"s15-{'bn' if con_bn else 'sin-bn'}-{sufijo}"
        cfg = config_profunda("relu", id=ident, seccion=15, lr=lr,
                              batch_norm=con_bn, batch=128, epochs=5,
                              max_pasos=None, eval_cada_pasos=50)
        CORRIDAS_BN[ident] = entrenar(cfg)

for ident, c in CORRIDAS_BN.items():
    estado = (f"DIVERGIÓ en el paso {c.paso_no_finito}" if c.divergio
              else "terminó")
    print(f"{ident:14s} η={c.config.lr:<5} {estado}")

# %% [codigo] s15-bn-curvas
# Small multiples: filas = learning rate, columnas = sin/con BN; mismos ejes.
orden = ["s15-sin-bn-003", "s15-bn-003", "s15-sin-bn-03", "s15-bn-03"]
fig = rejilla([CORRIDAS_BN[i] for i in orden], x="pasos", metrica="loss",
              columnas=2, misma_y=True)
for ax, i in zip(fig.axes, orden):       # el título dice si divergió
    c = CORRIDAS_BN[i]
    aviso = f" · DIVERGIÓ (paso {c.paso_no_finito})" if c.divergio else ""
    ax.set_title(f"{i} · η = {c.config.lr}{aviso}",
                 color="crimson" if c.divergio else "black")
fig.suptitle("Loss contra pasos: sin BN (izquierda) y con BN (derecha);\n"
             "η = 0.03 arriba, η = 0.3 abajo", y=1.02)
plt.show()

tabla = tabla_maestra([15])
display(tabla[tabla["id"].isin(orden)].set_index("id").loc[orden])

# %% [texto] s15-bn-lee

# %% [plegada] s15-apuesta-respuesta

# %% [texto] s15-bn-eval

# %% [codigo] s15-bn-train-eval
# La misma imagen, sola y acompañada de dos batches distintos.
# En eval() BN usa sus promedios corridos: la salida no depende del batch.
# En train() usa la media y varianza del batch: la salida sí depende.
red_bn = cargar(CORRIDAS_BN["s15-bn-003"])          # en eval()
primera_bn = next(m for m in red_bn if isinstance(m, nn.BatchNorm1d))
print("promedios corridos de la 1.ª BN (primeras 3 neuronas):")
print("  media   :", primera_bn.running_mean[:3].tolist())
print("  varianza:", primera_bn.running_var[:3].tolist())

Xv = DATOS["estandar"]["validation"][0]
x0 = Xv[:1]                                          # una sola imagen [1, 784]
lote_a = torch.cat([x0, Xv[1:64]])                   # x0 + 63 imágenes
lote_b = torch.cat([x0, Xv[64:127]])                 # x0 + otras 63

with torch.no_grad():
    sola = red_bn(x0)[0]
    en_a, en_b = red_bn(lote_a)[0], red_bn(lote_b)[0]
    print("\neval(): diferencia máxima entre los logits de x0")
    print(f"  sola vs lote A: {(sola - en_a).abs().max().item():.2e}")
    print(f"  lote A vs lote B: {(en_a - en_b).abs().max().item():.2e}")

    red_tr = copy.deepcopy(red_bn).train()           # copia: no tocar la original
    en_a, en_b = red_tr(lote_a)[0], red_tr(lote_b)[0]
    print("train(): diferencia máxima entre los logits de x0")
    print(f"  lote A vs lote B: {(en_a - en_b).abs().max().item():.2e}")
    try:
        red_tr(x0)
    except ValueError as error:                       # batch de 1: no hay varianza
        print("  sola, en train():", str(error).split(",")[0])

# %% [texto] s15-dropout-que-es

# %% [codigo] s15-dropout-capa
# Dropout sobre un vector de unos, con p = 0.4.
# train(): cada componente se apaga (0) con probabilidad p, y las que
# sobreviven se multiplican por 1/(1 − p) para que el promedio no cambie.
# eval(): dropout no hace nada.
torch.manual_seed(SEMILLA)
capa = nn.Dropout(p=0.4)
unos = torch.ones(10)
print(f"1/(1 − p) = {1 / (1 - 0.4):.4f}")
capa.train()
for vez in range(3):
    print(f"train(), vez {vez + 1}:", capa(unos).numpy().round(3))
grande = capa(torch.ones(100_000))
print(f"train(), promedio sobre 100 000 unos: {grande.mean().item():.4f}")
capa.eval()
print("eval():          ", capa(unos).numpy().round(3))

# Dónde queda dropout en la red: después de cada ReLU oculta.
print(construir_red([784, 256, 256, 10], "relu", dropout=0.4))

# %% [codigo] s15-dropout-entrenar
# Control sin dropout = la corrida de §10 (2000 ejemplos, 20 % de etiquetas
# cambiadas, validation limpia). Con dropout: la MISMA configuración,
# solo dropout = 0.4. Las dos se evalúan en eval(), sin dropout.
import dataclasses
BASE_CONTROL = dict(capas=[784, 256, 256, 10], activacion="relu",
                    optimizer="adam", lr=1e-3, batch=64, epochs=80,
                    idx_train=subconjunto(2000), ruido_etiquetas=0.2,
                    datos="2k-ruido20")
if "s10-control" in CORRIDAS:
    control = CORRIDAS["s10-control"]
    print("Uso la corrida s10-control que entrenó la sección 10.")
else:
    print("No encontré s10-control (¿no corriste la sección 10?): "
          "la entreno aquí con la misma configuración de §10.")
    control = entrenar(Config(id="s10-control", seccion=10, **BASE_CONTROL))

# replace copia la Config del control y cambia solo lo que se indica.
con_dropout = entrenar(dataclasses.replace(control.config, id="s15-dropout",
                                           seccion=15, dropout=0.4))

# %% [codigo] s15-dropout-curvas
# Lado a lado, con el mismo eje y: arriba loss, abajo accuracy.
fig, ejes = plt.subplots(2, 2, figsize=(12, 7.5), dpi=100,
                         sharey="row", sharex=True)
for col, (c, nombre) in enumerate([(control, "control, sin dropout"),
                                   (con_dropout, "dropout p = 0.4")]):
    curvas([c], x="epoch", metrica="loss", ax=ejes[0, col],
           titulo=f"Loss · {nombre}")
    curvas([c], x="epoch", metrica="accuracy", ax=ejes[1, col],
           titulo=f"Accuracy · {nombre}")
fig.suptitle("2000 ejemplos con 20 % de etiquetas cambiadas "
             "(validation y test limpios)")
fig.tight_layout()
plt.show()

# %% [codigo] s15-brecha
# Brecha por epoch. Con loss: validation − train (crece si memoriza).
# Con accuracy: train − validation. Ojo: la accuracy de train se mide
# contra las etiquetas alteradas, así que puede quedar por debajo de
# validation (brecha negativa) mientras la red no memoriza el ruido.
fig, ejes = plt.subplots(1, 2, figsize=(12, 3.8), dpi=100)
for c, nombre, estilo in [(control, "control", "-"),
                          (con_dropout, "dropout 0.4", "--")]:
    h = c.historial
    ejes[0].plot(h["epoch"], h["loss_validation"] - h["loss_train"],
                 ls=estilo, color="black", label=nombre)
    ejes[1].plot(h["epoch"], h["acc_train"] - h["acc_validation"],
                 ls=estilo, color="black", label=nombre)
ejes[0].set_title("Brecha de loss: validation − train")
ejes[1].set_title("Brecha de accuracy: train − validation")
for ax in ejes:
    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel("epoch")
    ax.legend()
ejes[0].set_ylabel("loss")
ejes[1].set_ylabel("accuracy")
fig.tight_layout()
plt.show()

# Resumen en la última epoch. «repite_falsa»: de los ejemplos de train con
# etiqueta alterada, qué fracción predice la red con la etiqueta FALSA
# (memorizar el ruido). La mejor epoch por validation está en la tabla maestra.
filas = []
for c in (control, con_dropout):
    X_tr, y_ruido = datos_de_entrenamiento(c.config)   # etiquetas alteradas
    sin_ruido = dataclasses.replace(c.config, ruido_etiquetas=0.0)
    y_limpia = datos_de_entrenamiento(sin_ruido)[1]     # las mismas, limpias
    alterada = y_ruido != y_limpia
    with torch.no_grad():
        pred = cargar(c, "ultima")(X_tr).argmax(1)
    u = c.historial.iloc[-1]
    filas.append({"id": c.id, "mejor_epoch": c.mejor_epoch,
                  "ultima_epoch": u["epoch"],
                  "acc_train_ultima": u["acc_train"],
                  "acc_val_ultima": u["acc_validation"],
                  "loss_val_ultima": u["loss_validation"],
                  "brecha_acc_ultima": u["acc_train"] - u["acc_validation"],
                  "repite_falsa": (pred[alterada] == y_ruido[alterada])
                  .float().mean().item()})
display(pd.DataFrame(filas).set_index("id").round(4))
tabla = tabla_maestra([10, 15])
display(tabla[tabla["id"].isin(["s10-control", "s15-dropout"])])

# %% [texto] s15-dropout-lee

# %% [codigo] s15-cinco-veces
# La misma imagen, cinco veces, por la red entrenada con dropout.
red_do = cargar(con_dropout, "ultima")              # cargar la deja en eval()
x0 = DATOS["estandar"]["validation"][0][:1]
y0 = DATOS["estandar"]["validation"][1][0].item()
torch.manual_seed(SEMILLA)
with torch.no_grad():
    for modo in ("train", "eval"):
        red_do.train(modo == "train")
        print(f"{modo}(): probabilidad de la clase real ({y0}) y predicción")
        for vez in range(5):
            p = torch.softmax(red_do(x0)[0], dim=0)
            print(f"  vez {vez + 1}: p = {p[y0].item():.4f}, "
                  f"predice {p.argmax().item()}")
red_do.eval()

# %% [texto] s15-que-viste
