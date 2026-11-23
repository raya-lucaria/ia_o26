# Sección 16 · Análisis del error.
# Elige el mejor MLP por accuracy de validation (solo corridas comparables:
# 50k de train, etiquetas limpias, sin modelo propio), lo restaura de su
# checkpoint «mejor» y lo analiza en validation. Test se mira UNA vez, al final.
# Publica: CORRIDAS["s16-elegido"] (el mismo objeto Corrida) y ELEGIDO_ID.

# %% [texto] s16-intro

# %% [codigo] s16-elegir
# 1) Candidatos comparables: mismos datos (50k de train, etiquetas limpias),
#    un MLP de construir_red (modelo is None) con al menos una capa oculta
#    (la regresión logística [784, 10] no es un MLP), de §4–§15, sin divergir.
def acc_val_en_mejor_epoch(c):
    """Accuracy de validation en la epoch que eligió la propia corrida."""
    h = c.historial
    fila = h[h["epoch"] == c.mejor_epoch]
    if len(fila) == 0:            # por si la epoch no tiene fila exacta
        return float("nan")
    return float(fila["acc_validation"].iloc[-1])


candidatos = {
    clave: c for clave, c in CORRIDAS.items()
    if clave != "s16-elegido"                  # no nos elegimos a nosotros mismos
    and c.config.datos == "50k-limpio"
    and c.config.modelo is None
    and len(c.config.capas) > 2                # al menos una capa oculta
    and c.config.seccion <= 15
    and c.config.idx_train is None and c.config.ruido_etiquetas == 0.0
    and not c.divergio
}

if not candidatos:
    # Saltaste secciones: entrenamos la línea base de §4 y lo decimos.
    print("No hay corridas comparables en CORRIDAS: entreno la línea base "
          "s04-oculta (784→128→10, ReLU, Adam 1e-3, 8 epochs).")
    base = entrenar(Config(id="s04-oculta", seccion=4, capas=[784, 128, 10],
                           activacion="relu", optimizer="adam", lr=1e-3,
                           epochs=8))
    candidatos = {base.id: base}

# 2) Tabla de candidatos ordenada SOLO por validation (ninguna columna de test).
filas = [{"id": clave, "seccion": c.config.seccion,
          "capas": str(c.config.capas), "optimizer": c.config.optimizer,
          "mejor_epoch": c.mejor_epoch,
          "acc_validation": acc_val_en_mejor_epoch(c)}
         for clave, c in candidatos.items()]
ranking = (pd.DataFrame(filas)
           .sort_values("acc_validation", ascending=False, na_position="last")
           .reset_index(drop=True))
display(ranking.head(10))

# 3) El ganador: la primera fila. Se publica para §17 y §18.
ELEGIDO_ID = ranking.loc[0, "id"]
ELEGIDO = candidatos[ELEGIDO_ID]
CORRIDAS["s16-elegido"] = ELEGIDO       # el mismo objeto, con otro nombre
print(f"Elegido por validation: {ELEGIDO_ID}  (capas {ELEGIDO.config.capas}, "
      f"epoch {ELEGIDO.mejor_epoch}, "
      f"acc_validation {ranking.loc[0, 'acc_validation']:.4f})")

# %% [codigo] s16-predicciones
# Restauramos el checkpoint de la MEJOR epoch (no el de la última) y sacamos
# las probabilidades de cada clase para todo un conjunto.
modelo_16 = cargar(ELEGIDO, "mejor")     # en DEVICE y en modo eval()


@torch.no_grad()
def probabilidades(modelo, escala, conjunto, bloque=4096):
    """Devuelve (P [n,10], y [n]) en CPU como numpy. P = softmax(logits)."""
    X, y = DATOS[escala][conjunto]
    partes = []
    for i in range(0, len(X), bloque):
        logits = modelo(X[i:i + bloque])          # [b, 10]
        partes.append(torch.softmax(logits, dim=1).cpu())
    return torch.cat(partes).numpy(), y.cpu().numpy()


ESCALA_16 = ELEGIDO.config.escala        # la misma escala con la que se entrenó
P_val, y_val = probabilidades(modelo_16, ESCALA_16, "validation")
pred_val = P_val.argmax(axis=1)          # la clase predicha: el argmax
conf_val = P_val.max(axis=1)             # su «confianza»: la probabilidad mayor
acierto_val = pred_val == y_val
print(f"validation: {len(y_val)} imágenes, accuracy {acierto_val.mean():.4f}, "
      f"errores {(~acierto_val).sum()}")

# %% [texto] s16-apuesta

# %% [texto] s16-confusion-texto

# %% [codigo] s16-confusion
DIGITOS = np.arange(10)


def matriz_confusion(y, pred, k=10):
    """C[i, j] = cuántas imágenes de clase real i se predijeron como j."""
    C = np.zeros((k, k), dtype=int)
    np.add.at(C, (y, pred), 1)
    return C


def dibujar_confusion(C, ax, titulo, normalizar=False):
    """Mapa de calor rotulado: filas = clase real, columnas = clase predicha."""
    # Normalizada: en % de la fila, con un decimal (0.3 % no se vuelve 0.00).
    M = 100 * C / C.sum(axis=1, keepdims=True) if normalizar else C
    ax.imshow(M, cmap="Blues", vmin=0, vmax=M.max())
    for i in range(10):
        for j in range(10):
            txt = f"{M[i, j]:.1f}" if normalizar else f"{M[i, j]}"
            color = "white" if M[i, j] > 0.6 * M.max() else "black"
            ax.text(j, i, txt, ha="center", va="center", fontsize=7, color=color)
    ax.set_xticks(DIGITOS)
    ax.set_yticks(DIGITOS)
    ax.set_xlabel("clase predicha (columna j)")
    ax.set_ylabel("clase real (fila i)")
    ax.set_title(titulo)
    ax.grid(False)


C_val = matriz_confusion(y_val, pred_val)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.5))
dibujar_confusion(C_val, a1, f"Validation · conteos ({ELEGIDO_ID})")
dibujar_confusion(C_val, a2, "Validation · % de cada fila (clase real)",
                  normalizar=True)
fig.tight_layout()
plt.show()
print("suma de la matriz de validation:", C_val.sum())

# %% [plegada] s16-apuesta-respuesta

# %% [texto] s16-metricas-texto

# %% [codigo] s16-metricas
def metricas_por_clase(C):
    """precision, recall y F1 de cada dígito, uno contra el resto."""
    vp = np.diag(C)                         # verdaderos positivos
    predichos = C.sum(axis=0)               # columna: todo lo que dije «es j»
    reales = C.sum(axis=1)                  # fila: todo lo que de verdad es j
    precision = vp / np.maximum(predichos, 1)
    recall = vp / np.maximum(reales, 1)
    f1 = 2 * precision * recall / np.maximum(precision + recall, 1e-12)
    return pd.DataFrame({"digito": DIGITOS, "soporte": reales,
                         "precision": precision, "recall": recall, "F1": f1})


metricas_val = metricas_por_clase(C_val)
display(metricas_val.round(4))
peor = metricas_val.loc[metricas_val["F1"].idxmin()]
print(f"dígito con menor F1 en validation: {int(peor['digito'])} "
      f"(precision {peor['precision']:.3f}, recall {peor['recall']:.3f})")

fig, ax = plt.subplots(figsize=(10, 3.8))
ancho = 0.4
ax.bar(DIGITOS - ancho / 2, metricas_val["precision"], ancho,
       label="precision", color=COLORES["validation"])
ax.bar(DIGITOS + ancho / 2, metricas_val["recall"], ancho,
       label="recall", color="#9467bd")
piso = max(0.0, min(metricas_val["precision"].min(),
                    metricas_val["recall"].min()) - 0.03)
ax.set_ylim(piso, 1.0)                  # eje recortado: las diferencias son chicas
ax.set_xticks(DIGITOS)
ax.set_xlabel("dígito")
ax.set_ylabel("valor (eje recortado)")
ax.set_title(f"Precision y recall por dígito · validation ({ELEGIDO_ID})")
ax.legend()
plt.show()

# %% [codigo] s16-pares
# Los pares (real → predicho) fuera de la diagonal, de más a menos casos.
pares = [(i, j, C_val[i, j]) for i in range(10) for j in range(10) if i != j]
pares = pd.DataFrame(pares, columns=["real", "predicho", "casos"])
pares["% de la clase real"] = 100 * pares["casos"] / C_val.sum(axis=1)[pares["real"]]
top_pares = (pares.sort_values("casos", ascending=False)
             .head(10).reset_index(drop=True))
display(top_pares.round(2))

fig, ax = plt.subplots(figsize=(8, 4))
etiquetas = [f"{r} → {p}" for r, p in zip(top_pares["real"], top_pares["predicho"])]
ax.barh(etiquetas[::-1], top_pares["casos"][::-1], color=COLORES["validation"])
ax.set_xlabel("imágenes de validation")
ax.set_ylabel("clase real → clase predicha")
ax.set_title("Los diez pares más confundidos · validation")
plt.show()

# %% [texto] s16-galeria-texto

# %% [codigo] s16-galeria
# Imágenes de validation en [0, 1] para dibujarlas (DATOS["01"] = píxel / 255).
IMAGENES_VAL = DATOS["01"]["validation"][0].reshape(-1, 28, 28).cpu().numpy()

errores = np.flatnonzero(~acierto_val)
# Los errores ordenados por confianza, de mayor a menor.
mas_confiados = errores[np.argsort(-conf_val[errores])][:16]

fig, ejes = plt.subplots(4, 4, figsize=(8.5, 9.5))
for ax in ejes.ravel():
    ax.axis("off")
for ax, k in zip(ejes.ravel(), mas_confiados):
    ax.imshow(IMAGENES_VAL[k], cmap="gray_r")
    ax.set_title(f"real {y_val[k]} · predicho {pred_val[k]}\n"
                 f"confianza {conf_val[k]:.3f}", fontsize=9)
fig.suptitle(f"Los {len(mas_confiados)} errores más confiados · validation",
             fontsize=13)
fig.tight_layout()
plt.show()

# %% [texto] s16-confianza-texto

# %% [codigo] s16-confianza
COLOR_ACIERTO, COLOR_ERROR = "#7f7f7f", "#d62728"
cortes_conf = np.linspace(0.1, 1.0, 37)      # la confianza nunca baja de 1/10

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(conf_val[acierto_val], bins=cortes_conf, density=True, alpha=0.6,
        color=COLOR_ACIERTO, label=f"aciertos (n = {acierto_val.sum()})")
ax.hist(conf_val[~acierto_val], bins=cortes_conf, density=True, alpha=0.6,
        color=COLOR_ERROR, label=f"errores (n = {(~acierto_val).sum()})")
ax.set_xlabel("confianza = probabilidad de la clase predicha")
ax.set_ylabel("densidad (cada grupo integra 1)")
ax.set_title("¿Qué tan seguro estaba cuando acertó y cuando falló? · validation")
ax.legend()
plt.show()

print(f"confianza mediana en aciertos: {np.median(conf_val[acierto_val]):.3f}")
print(f"confianza mediana en errores:  {np.median(conf_val[~acierto_val]):.3f}")

# %% [texto] s16-calibracion-texto

# %% [codigo] s16-calibracion
# 10 intervalos de igual ancho sobre la confianza; en cada uno comparamos lo que
# el modelo ANUNCIA (confianza promedio) con lo que OCURRE (fracción de aciertos).
bordes = np.linspace(0, 1, 11)
grupo = np.clip(np.digitize(conf_val, bordes) - 1, 0, 9)
filas = []
for b in range(10):
    dentro = grupo == b
    hay = dentro.any()                  # un intervalo puede quedar vacío
    cierre = "]" if b == 9 else ")"     # el último incluye la confianza 1.0
    filas.append({"intervalo": f"[{bordes[b]:.1f}, {bordes[b + 1]:.1f}{cierre}",
                  "casos": int(dentro.sum()),
                  "confianza_media": conf_val[dentro].mean() if hay else np.nan,
                  "accuracy": acierto_val[dentro].mean() if hay else np.nan})
calibracion = pd.DataFrame(filas)
display(calibracion.round(4))

fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 8), sharex=True,
                             gridspec_kw={"height_ratios": [3, 1]})
a1.plot([0, 1], [0, 1], "--", color="gray", label="calibración perfecta")
ok = calibracion["casos"] > 0
a1.plot(calibracion.loc[ok, "confianza_media"], calibracion.loc[ok, "accuracy"],
        "o-", color=COLORES["validation"], label="modelo elegido")
for _, f in calibracion[ok].iterrows():
    a1.annotate(f"n={f['casos']}", (f["confianza_media"], f["accuracy"]),
                textcoords="offset points", xytext=(-14, 7), fontsize=8)
a1.set_ylabel("accuracy observada en el intervalo")
a1.set_title("Diagrama de calibración · validation")
a1.legend(loc="upper left")
a2.bar(bordes[:-1] + 0.05, calibracion["casos"], width=0.09,
       color=COLORES["validation"])
a2.set_yscale("log")                    # casi todo cae en el último intervalo
a2.set_xlabel("confianza anunciada")
a2.set_ylabel("casos (log)")
a2.set_xlim(0, 1)
fig.tight_layout()
plt.show()

# %% [texto] s16-test-texto

# %% [codigo] s16-test
# UNA sola vez, al final, y sin cambiar nada de lo elegido: reportar en test.
P_test, y_test = probabilidades(modelo_16, ESCALA_16, "test")
pred_test = P_test.argmax(axis=1)
C_test = matriz_confusion(y_test, pred_test)
print(f"accuracy en validation (con la que elegimos): {acierto_val.mean():.4f}")
print(f"accuracy en test (reporte, una vez):          "
      f"{(pred_test == y_test).mean():.4f}")
print("suma de la matriz de confusión de test:", C_test.sum())

fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.5))
dibujar_confusion(C_test, a1, f"Test · conteos ({ELEGIDO_ID})")
dibujar_confusion(C_test, a2, "Test · % de cada fila (clase real)",
                  normalizar=True)
fig.tight_layout()
plt.show()
display(metricas_por_clase(C_test).round(4))

# %% [texto] s16-tabla-texto

# %% [codigo] s16-tabla
# La tabla maestra hasta esta sección, un bloque por tipo de datos:
# solo se comparan entre sí las corridas que vieron los mismos datos.
tabla_16 = tabla_maestra(list(range(1, 17)))
# CORRIDAS["s16-elegido"] es la MISMA corrida que ganó: aparecería dos veces
# con su ID original. Dejamos una sola fila por ID.
tabla_16 = tabla_16.drop_duplicates("id").reset_index(drop=True)
# El presupuesto total de cada corrida: pasos y ejemplos de su última fila.
por_id = {c.id: c for c in CORRIDAS.values()}
tabla_16["pasos_total"] = [por_id[i].historial["pasos"].iloc[-1]
                           for i in tabla_16["id"]]
tabla_16["ejemplos_total"] = [por_id[i].historial["ejemplos"].iloc[-1]
                              for i in tabla_16["id"]]
for datos, bloque in tabla_16.groupby("datos", sort=False):
    print(f"\n=== datos: {datos} · {len(bloque)} corridas ===")
    display(bloque.sort_values(["pasos_total", "seccion"]).reset_index(drop=True))

# %% [texto] s16-que-viste
