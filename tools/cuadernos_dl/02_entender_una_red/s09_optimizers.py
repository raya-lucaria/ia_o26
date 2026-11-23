# Sección 9 · Optimizers. SGD, momentum, Adam y AdamW sobre la misma red;
# un paso a mano de Adam + L2 contra AdamW; y Adam + L2 contra AdamW en MNIST,
# mirando cómo se encogen los pesos. El texto vive en s09_optimizers.texto.md.

# %% [texto] s09-intro

# %% [texto] s09-apuesta

# %% [codigo] s09-comparar
# Cuatro configuraciones sobre la misma red 784→128→10, con los mismos pesos
# iniciales (semilla_init) y el mismo orden de batches (semilla_orden).
# Cambia la regla con la que cada paso mueve θ, y con ella su η: SGD y
# momentum usan 0.03, Adam y AdamW 1e-3. Solo AdamW lleva weight decay.
OPTIMIZERS_S09 = [
    # (ID,             optimizer,  η,    weight_decay)
    ("s09-sgd",        "sgd",      0.03, 0.0),
    ("s09-momentum",   "momentum", 0.03, 0.0),    # β = 0.9, ver la ecuación
    ("s09-adam",       "adam",     1e-3, 0.0),
    ("s09-adamw",      "adamw",    1e-3, 0.01),   # decay desacoplado, solo pesos
]

corridas_s09 = []
for id_, opt, lr, wd in OPTIMIZERS_S09:
    cfg = Config(id=id_, seccion=9, capas=[784, 128, 10], optimizer=opt,
                 lr=lr, weight_decay=wd, epochs=5, batch=128,
                 semilla_init=SEMILLA, semilla_orden=SEMILLA)
    corrida = entrenar(cfg)
    corridas_s09.append(corrida)
    ultima = corrida.historial.iloc[-1]
    print(f"{id_:14s} η = {lr:<6g} weight_decay = {wd:<5g} "
          f"loss validation final = {ultima['loss_validation']:.4f}   "
          f"accuracy validation final = {ultima['acc_validation']:.4f}")

# %% [codigo] s09-curvas
# Small multiples: un panel por optimizer, mismos ejes, para comparar de un
# vistazo. Colores = conjunto (train, validation, test); un panel = una corrida.
fig = rejilla(corridas_s09, x="epoch", metrica="loss", columnas=4)
fig.suptitle("Loss por epoch con cuatro configuraciones (red 784→128→10)")
plt.show()

# Las cuatro curvas de validation en un solo eje: aquí sí se ve quién baja
# más rápido. Color = validation (como en todo el notebook); el estilo de
# línea y el marcador distinguen la corrida, para que dos curvas encimadas
# (Adam y AdamW) se sigan viendo.
TRAZOS_S09 = [("-", "o"), ("--", "s"), (":", "^"), ("-.", "D")]


def por_corrida(corridas, columna, ax, titulo, etiqueta_y, color, log=False):
    """Una línea por corrida con la columna `columna` de su historial."""
    for c, (estilo, marca) in zip(corridas, TRAZOS_S09):
        h = c.historial
        ok = np.isfinite(h[columna].to_numpy(dtype=float))
        ax.plot(h["epoch"][ok], h[columna][ok], estilo, marker=marca, ms=4,
                color=color, label=c.id)
    if log:
        ax.set_yscale("log")
    ax.set_title(titulo)
    ax.set_xlabel("epoch")
    ax.set_ylabel(etiqueta_y)
    ax.legend(fontsize=8)


fig, ejes = plt.subplots(1, 2, figsize=(12, 4))
por_corrida(corridas_s09, "loss_validation", ejes[0],
            "Loss de validation (escala log)", "loss (cross-entropy)",
            COLORES["validation"], log=True)
por_corrida(corridas_s09, "acc_validation", ejes[1], "Accuracy de validation",
            "accuracy", COLORES["validation"])
plt.tight_layout()
plt.show()

# %% [codigo] s09-tabla
# La tabla maestra, solo con las filas de esta comparación. La «mejor epoch»
# se elige con la loss de validation; test solo se reporta.
ids_comparacion = [id_ for id_, *_ in OPTIMIZERS_S09]
tabla_s09 = tabla_maestra([9])
display(tabla_s09[tabla_s09["id"].isin(ids_comparacion)])

# %% [plegada] s09-apuesta-respuesta

# %% [texto] s09-l2-vs-adamw

# %% [codigo] s09-paso-a-mano
# Un paso de Adam escrito a mano, con las mismas ecuaciones del texto.
# desacoplado=False es Adam + L2 (el decay entra al gradiente);
# desacoplado=True es AdamW (el decay encoge los pesos aparte).
ETA_S09, WD_S09 = 0.1, 0.1                   # η y weight_decay (= 2μ)
B1, B2, EPS = 0.9, 0.999, 1e-8               # los valores por defecto de PyTorch


def paso_adam(w, g_datos, m, v, t, desacoplado, eta=ETA_S09, wd=WD_S09):
    """Un paso de Adam (t empieza en 1). Devuelve los nuevos w, m, v."""
    if desacoplado:
        w = w * (1 - eta * wd)               # AdamW: encoge θ aparte...
        g = g_datos                          # ...y el gradiente no lo sabe
    else:
        g = g_datos + wd * w                 # Adam + L2: ∇(μΣθ²) = 2μθ = wd·θ
    m = B1 * m + (1 - B1) * g                # promedio de gradientes
    v = B2 * v + (1 - B2) * g ** 2           # promedio de gradientes al cuadrado
    m_gorro = m / (1 - B1 ** t)              # corrección de sesgo
    v_gorro = v / (1 - B2 ** t)
    w = w - eta * m_gorro / (v_gorro.sqrt() + EPS)
    return w, m, v


# %% [codigo] s09-verificar
w0 = torch.tensor([1.0, 2.0], dtype=torch.float64)   # pesos (1, 2)
cero = torch.zeros_like(w0)                          # gradiente de datos = 0
w_l2, *_ = paso_adam(w0, cero, cero, cero, t=1, desacoplado=False)
w_dw, *_ = paso_adam(w0, cero, cero, cero, t=1, desacoplado=True)


def paso_torch(clase, pasos=1):
    """Lo mismo con el optimizer de PyTorch; devuelve la trayectoria de w."""
    w = w0.clone().requires_grad_(True)
    opt = clase([w], lr=ETA_S09, weight_decay=WD_S09, betas=(B1, B2), eps=EPS)
    trayectoria = [w.detach().clone()]
    for _ in range(pasos):
        w.grad = torch.zeros_like(w)         # gradiente de datos cero, a mano
        opt.step()                           # (zero_grad() lo dejaría en None)
        trayectoria.append(w.detach().clone())
    return torch.stack(trayectoria)


torch_l2 = paso_torch(torch.optim.Adam)[1]
torch_dw = paso_torch(torch.optim.AdamW)[1]
assert torch.allclose(w_l2, torch_l2, rtol=0, atol=1e-12), (w_l2, torch_l2)
assert torch.allclose(w_dw, torch_dw, rtol=0, atol=1e-12), (w_dw, torch_dw)

paso_tabla = pd.DataFrame({
    "peso": ["w₁", "w₂"],
    "antes": w0.numpy(),
    "Adam + L2 (a mano)": w_l2.numpy(), "Adam + L2 (torch)": torch_l2.numpy(),
    "AdamW (a mano)": w_dw.numpy(), "AdamW (torch)": torch_dw.numpy(),
    "cambio Adam + L2": (w_l2 - w0).numpy(),
    "cambio AdamW": (w_dw - w0).numpy(),
}).set_index("peso")
display(paso_tabla.round(6))
print("cambio relativo Adam + L2:", ((w_l2 - w0) / w0).numpy().round(4))
print("cambio relativo AdamW:    ", ((w_dw - w0) / w0).numpy().round(4))
print("La cuenta a mano coincide con torch.optim.Adam y torch.optim.AdamW.")

# %% [codigo] s09-varios-pasos
# Diez pasos con el gradiente de datos en cero: solo actúa el decay.
# Adam + L2 resta casi lo mismo a los dos pesos en cada paso (Adam normaliza
# el gradiente 2μθ y lo deja de tamaño ≈ 1); AdamW los multiplica por
# (1 − η·wd), así que w₂/w₁ se queda en 2.
PASOS_S09 = 10
tray_l2 = paso_torch(torch.optim.Adam, PASOS_S09).numpy()
tray_dw = paso_torch(torch.optim.AdamW, PASOS_S09).numpy()

fig, ejes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
for ax, tray, nombre in [(ejes[0], tray_l2, "Adam + L2 (torch.optim.Adam)"),
                         (ejes[1], tray_dw, "AdamW (torch.optim.AdamW)")]:
    ax.plot(tray[:, 0], "o-", color="0.2", label="w₁ (empieza en 1)")
    ax.plot(tray[:, 1], "s--", color="0.5", label="w₂ (empieza en 2)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(nombre)
    ax.set_xlabel("paso")
    ax.legend()
ejes[0].set_ylabel("valor del peso")
fig.suptitle(f"Solo el decay: gradiente de datos cero, η = {ETA_S09}, "
             f"weight_decay = {WD_S09}")
plt.tight_layout()
plt.show()
print("w₂/w₁ tras 5 pasos, Adam + L2:", round(tray_l2[5, 1] / tray_l2[5, 0], 3))
print("w₂/w₁ tras 5 pasos, AdamW:    ", round(tray_dw[5, 1] / tray_dw[5, 0], 3))

# %% [texto] s09-paso-que-viste

# %% [texto] s09-mnist-intro

# %% [codigo] s09-l2-entrenar
# Adam + L2 contra AdamW en MNIST, con el mismo η y el mismo weight_decay, y
# Adam sin decay como control. Red más ancha (784→256→10) y 8 epochs para que
# a los pesos les dé tiempo de crecer o de encogerse.
DECAY_S09 = [
    # (ID,             optimizer,  weight_decay)
    ("s09-adam-l2",  "adam_l2", 0.01),   # decay acoplado: entra al gradiente
    ("s09-adamw-wd", "adamw",   0.01),   # decay desacoplado: encoge aparte
    ("s09-adam-sin", "adam",    0.0),    # control: sin decay
]
corridas_decay = []
for id_, opt, wd in DECAY_S09:
    cfg = Config(id=id_, seccion=9, capas=[784, 256, 10], optimizer=opt,
                 lr=1e-3, weight_decay=wd, epochs=8, batch=128,
                 semilla_init=SEMILLA, semilla_orden=SEMILLA)
    corridas_decay.append(entrenar(cfg))

resumen = pd.DataFrame([{
    "id": c.id,
    "norma de los pesos al inicio": c.historial["norma_pesos"].iloc[0],
    "norma de los pesos al final": c.historial["norma_pesos"].iloc[-1],
    "loss validation final": c.historial["loss_validation"].iloc[-1],
    "accuracy validation final": c.historial["acc_validation"].iloc[-1],
    "mejor epoch (validation)": c.mejor_epoch,
} for c in corridas_decay]).set_index("id")
display(resumen.round(4))

# %% [codigo] s09-l2-graficas
# Izquierda: la norma de los pesos por epoch (lo que el decay sí cambia).
# Derecha: la loss de validation (lo que puede no cambiar casi nada).
# Cada corrida conserva su estilo de línea y su marcador en los dos paneles.
# La norma no es train ni validation: va en gris; la loss, en el color de
# validation y en escala log, para que la epoch 0 no aplaste el resto.
fig, ejes = plt.subplots(1, 2, figsize=(12, 4))
por_corrida(corridas_decay, "norma_pesos", ejes[0],
            "Norma de los pesos por epoch", "norma de los pesos (sin sesgos)",
            "0.3")
por_corrida(corridas_decay, "loss_validation", ejes[1],
            "Loss de validation (escala log)", "loss (cross-entropy)",
            COLORES["validation"], log=True)
plt.tight_layout()
plt.show()

# %% [texto] s09-que-viste
