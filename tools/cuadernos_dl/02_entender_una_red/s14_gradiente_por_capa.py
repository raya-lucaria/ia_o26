# Notebook 02 de deep learning · §14 El gradiente por capa (avanzado).
# Tres corridas de config_profunda (sigmoide, ReLU, ReLU + batch normalization)
# con medir_por_paso=True: norma del gradiente por capa y cociente
# actualización/peso en cada paso. Aparte, un loop propio (misma configuración
# que s14-relu) guarda los pesos en tres momentos para comparar, con la red
# congelada, el gradiente sobre todo train contra 32 gradientes de mini-batch.
# IDs producidos: s14-sigmoide, s14-relu, s14-relu-bn. No consume corridas.

# %% [texto] s14-intro

# %% [texto] s14-que-medimos

# %% [codigo] s14-corridas
# Tres redes profundas (6 ocultas de 128, SGD 0.03, init ortogonal, sesgos 0)
# que solo difieren en la activación y en batch normalization, y una cuarta,
# sigmoide con Adam, que solo se usa en la última gráfica (‖ΔW‖/‖W‖).
# medir_por_paso=True: en cada paso, entrenar guarda por capa la norma del
# gradiente y el cociente ‖ΔW‖/‖W‖ en corrida.por_paso.
PASOS_S14 = 600                    # ~1.5 epochs de 50k con batch 128
VARIANTES_S14 = {                  # ID → (activación, cambios a config_profunda)
    "s14-sigmoide": ("sigmoide", {}),
    "s14-relu": ("relu", {}),
    "s14-relu-bn": ("relu", {"batch_norm": True}),
    "s14-sigmoide-adam": ("sigmoide", {"optimizer": "adam", "lr": 1e-3}),
}
for id_, (act, cambios) in VARIANTES_S14.items():
    entrenar(config_profunda(
        act, id=id_, seccion=14, **cambios,
        epochs=2, max_pasos=PASOS_S14,       # se corta en el paso 600
        eval_cada_pasos=100,                 # un punto de las curvas cada 100 pasos
        medir_por_paso=True))
C14_TODAS = [CORRIDAS[i] for i in VARIANTES_S14]
C14 = C14_TODAS[:3]                          # las tres de SGD
display(tabla_maestra([14]))

# %% [codigo] s14-curvas
# Primero el contexto: ¿cuál aprendió algo en estos pasos?
# Solo train y validation; las decisiones nunca miran test.
fig, ejes = plt.subplots(1, 4, figsize=(16, 3.8), sharey=True)
for corrida, ax in zip(C14_TODAS, ejes):
    curvas([corrida], x="pasos", metrica="loss",
           conjuntos=("train", "validation"), ax=ax, titulo=corrida.id)
    ax.axhline(np.log(10), color="gray", ls=":", lw=1)   # adivinar uniforme
ejes[0].set_ylabel("loss (cross-entropy)")
fig.suptitle("Loss contra pasos; la línea punteada es log 10 ≈ 2.30")
fig.tight_layout()
plt.show()

# %% [texto] s14-apuesta

# %% [plegada] s14-apuesta-respuesta

# %% [texto] s14-leer-norma

# %% [codigo] s14-norma-por-capa
def suavizar(valores, ventana):
    """Media móvil centrada del logaritmo: en escala log es la que no se
    deja jalar por un solo pico."""
    s = pd.Series(np.log10(valores))
    return 10 ** s.rolling(ventana, center=True, min_periods=1).mean().to_numpy()


def dibujar_por_capa(corrida, columna, ax):
    """Una línea por capa: la serie cruda tenue y la suavizada encima."""
    pp = corrida.por_paso
    pp = pp[np.isfinite(pp[columna]) & (pp[columna] > 0)]
    capas = list(dict.fromkeys(pp["capa"]))           # en el orden de la red
    tonos = plt.cm.viridis(np.linspace(0, 0.9, len(capas)))
    ventana = max(1, min(25, pp["paso"].nunique() // 10))
    for capa, tono in zip(capas, tonos):
        una = pp[pp["capa"] == capa].sort_values("paso")
        ax.plot(una["paso"], una[columna], color=tono, alpha=0.15, lw=0.8)
        ax.plot(una["paso"], suavizar(una[columna].to_numpy(), ventana),
                color=tono, lw=1.8, label=f"capa {capa}"
                + (" (salida)" if capa == capas[-1] else ""))
    ax.set_yscale("log")
    ax.set_xlabel("paso (actualización)")
    ax.set_title(corrida.id)


fig, ejes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
for corrida, ax in zip(C14, ejes):
    dibujar_por_capa(corrida, "norma_grad", ax)
ejes[0].set_ylabel("‖gradiente de la capa‖ (escala log)")
ejes[-1].legend(fontsize=8, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.suptitle("Norma del gradiente de cada capa en cada paso "
             "(tenue: crudo; grueso: media móvil)")
fig.tight_layout()
plt.show()

# Resumen numérico: mediana de la norma por capa en todo el entrenamiento.
resumen = pd.DataFrame({
    c.id: c.por_paso.groupby("capa", sort=False)["norma_grad"].median()
    for c in C14})
resumen.index = [f"capa {i}" for i in resumen.index]   # 7 = salida
print("Mediana de ‖gradiente‖ por capa (filas: capa; columnas: corrida)")
display(resumen.apply(lambda col: col.map("{:.2e}".format)))

# %% [texto] s14-norma-que-viste

# %% [texto] s14-va-a-cero

# %% [codigo] s14-tres-momentos
# Misma configuración que s14-relu (sin BN), pero con un loop propio visible
# para guardar una copia de los pesos al inicio, a la mitad y al final.
import copy
import torch.nn.functional as F
cfg14 = CORRIDAS["s14-relu"].config
X14, y14 = DATOS[cfg14.escala]["train"]   # todo train (con RAPIDO ya viene recortado)
pasos14 = 30 if RAPIDO else PASOS_S14     # con RAPIDO, como el tope de entrenar
momentos14 = {"inicio": 0, "mitad": pasos14 // 2, "fin": pasos14}

torch.manual_seed(cfg14.semilla_init)        # mismos pesos iniciales cada vez
red14 = construir_red(cfg14.capas, cfg14.activacion, init=cfg14.init).to(DEVICE)
opt14 = torch.optim.SGD(red14.parameters(), lr=cfg14.lr)
gen14 = torch.Generator().manual_seed(cfg14.semilla_orden)
pesos14, paso, orden = {}, 0, torch.empty(0, dtype=torch.long)
while True:
    for nombre, p in momentos14.items():     # ¿toca guardar una copia?
        if p == paso:
            pesos14[nombre] = copy.deepcopy(red14.state_dict())
    if paso == pasos14:
        break
    if len(orden) == 0:                      # se acabó la epoch: nuevo orden
        orden = torch.randperm(len(y14), generator=gen14)
    lote, orden = orden[:cfg14.batch].to(DEVICE), orden[cfg14.batch:]
    red14.train()
    opt14.zero_grad()
    F.cross_entropy(red14(X14[lote]), y14[lote]).backward()
    opt14.step()
    paso += 1
print({m: f"paso {p}" for m, p in momentos14.items()}, "de", pasos14,
      "| ejemplos de train:", len(y14))

# %% [codigo] s14-gradientes-congelados
def gradiente(red, X, y, bloque=8192):
    """∇ de la loss promedio sobre (X, y), como un solo vector.
    Va por bloques: .grad acumula, y dividir cada suma entre n hace que la
    suma de los bloques sea exactamente el gradiente del promedio."""
    red.zero_grad(set_to_none=True)
    n, perdida = len(y), 0.0
    for i in range(0, n, bloque):
        l = F.cross_entropy(red(X[i:i + bloque]), y[i:i + bloque],
                            reduction="sum") / n
        l.backward()
        perdida += l.item()
    g = torch.cat([p.grad.flatten() for p in red.parameters()])
    return g.detach().clone(), perdida


N_LOTES14, TAM_LOTE14 = 32, 128
filas14, normas_lote14 = [], {}
for nombre, estado in pesos14.items():
    red14.load_state_dict(estado)            # la red congelada en ese momento
    g_todo, loss_todo = gradiente(red14, X14, y14)
    gen = torch.Generator().manual_seed(1)   # los mismos 32 lotes en cada momento
    normas, ruido = [], []
    for _ in range(N_LOTES14):
        lote = torch.randperm(len(y14), generator=gen)[:TAM_LOTE14].to(DEVICE)
        g_lote, _ = gradiente(red14, X14[lote], y14[lote])
        normas.append(g_lote.norm().item())
        ruido.append((g_lote - g_todo).norm().item())   # lo que no es señal
    normas_lote14[nombre] = np.array(normas)
    filas14.append({"momento": nombre, "paso": momentos14[nombre],
                    "loss_train": loss_todo, "‖g_completo‖": g_todo.norm().item(),
                    "mediana ‖g_B‖": np.median(normas),
                    "mediana ‖g_B − g‖": np.median(ruido)})
grad14 = pd.DataFrame(filas14).set_index("momento")
display(grad14.apply(lambda col: col.map("{:.3g}".format)))

# %% [codigo] s14-cajas
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2),
                             gridspec_kw={"width_ratios": [1.6, 1]})
pos = np.arange(len(grad14))
a1.boxplot([normas_lote14[m] for m in grad14.index], positions=pos, widths=0.5,
           patch_artist=True, boxprops={"facecolor": "#dddddd"},
           medianprops={"color": "black"})
a1.scatter(pos, grad14["‖g_completo‖"], marker="D", s=60, zorder=3,
           color=COLORES["train"], label="‖g_completo‖ (todo train)")
a1.scatter(pos, grad14["mediana ‖g_B − g‖"], marker="x", s=60, zorder=3,
           color="black", label="mediana ‖g_B − g_completo‖ (ruido)")
a1.plot([], [], "s", color="#dddddd", label=f"‖g_B‖, {N_LOTES14} mini-batches")
etiquetas = [f"{m}\n(paso {p})" for m, p in zip(grad14.index, grad14["paso"])]
a1.set_xticks(pos, etiquetas)
a1.set_yscale("log")
a1.set_ylabel("norma del gradiente (escala log)")
a1.set_title(f"Red congelada: g_completo ({len(y14):,} de train) vs mini-batch")
a1.legend(fontsize=8)
a2.plot(pos, grad14["loss_train"], "o-", color=COLORES["train"])
a2.set_xticks(pos, etiquetas)
a2.set_ylabel("loss de train (todo train)")
a2.set_title("La loss en esos mismos pesos")
fig.tight_layout()
plt.show()

# %% [texto] s14-cero-que-viste

# %% [texto] s14-cociente

# %% [codigo] s14-cociente-graf
# Mismo dibujo que la norma, ahora con ‖W_{t+1} − W_t‖ / ‖W_t‖ por capa.
# El cuarto panel es la sigmoide con Adam: mismo gradiente que se desvanece,
# pero Adam divide cada paso entre la escala típica del gradiente de cada peso.
fig, ejes = plt.subplots(1, 4, figsize=(16, 4.2), sharey=True)
for corrida, ax in zip(C14_TODAS, ejes):
    dibujar_por_capa(corrida, "cociente_actualizacion", ax)
    ax.axhline(1e-3, color="gray", ls="--", lw=1, alpha=0.5)   # heurística
ejes[0].set_ylabel("‖ΔW‖ / ‖W‖ (escala log)")
ejes[-1].legend(fontsize=8, loc="center left", bbox_to_anchor=(1.01, 0.5))
fig.suptitle("Cuánto cambia cada capa en cada paso, relativo a su tamaño "
             "(gris: la regla práctica 1e-3)")
fig.tight_layout()
plt.show()

# %% [texto] s14-que-viste
