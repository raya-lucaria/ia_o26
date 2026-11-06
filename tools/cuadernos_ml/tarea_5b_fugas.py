# Tarea 5b de la unidad 9 · Una victoria sospechosa (la separación mal hecha es
# la de un compañero; tu prueba está sellada) (clase 5). Código y orden de
# celdas: prog-c5 (clase_5.md §10.6). El texto de cada celda [texto] vive en
# tarea_5b_fugas.texto.md (guion de Codex). Sin -explica ni respuestas.
# Especificación privada (no va al guion ni a la página; D-009.7: inspirada en las
# fugas del proyecto del profesor, con datos propios): reingreso en 30 días (≈ 15 %)
# de visitas de 1 000 pacientes con efecto_grupo; prueba_sellada = las visitas de
# los pacientes 800–999, apartadas por paciente ANTES de todo (DECISION prog-c5-8:
# se filtra por grupo en lugar de leer datos.prueba, así ninguna celda fuera del
# bloque 5 lee la prueba). Las cinco fugas del compañero viven dentro de
# desarrollo: (1) costo_del_reingreso, posterior; (2) eligió 15 de 200 análisis por
# correlación con y usando todo desarrollo; (3) imputó su validación con un
# imputador reajustado en su validación; (4) 10 % de visitas capturadas dos veces
# antes de separar; (5) separó al azar por visita. La solución de B4 es
# tuberia(imputador(), estandarizar(seleccionar(k=15)), modelo={"familia":
# "logistica", "pesos": "balanceado"}) con CV por pacientes y estratificada.
# La sección «promesa» de tools/test_ml_cifras_c5.py ejecuta bloque-1-juega.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Los datos y la prueba sellada (no la abras hasta entregar)
SEMILLA = 0
import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
LABS = [f"lab_{j:03d}" for j in range(1, 201)]
X = {"edad": ml.uniforme(20, 90), "visitas_previas": ml.categorica([0, 1, 2, 3, 4]),
     "fecha": ml.uniforme(0, 730), **{c: ml.normal(0, 1) for c in LABS}}
puntaje = lambda d: (-3.4 + 0.03 * (d.edad - 55) + 0.5 * d.visitas_previas
                     + 0.8 * d.lab_007 - 0.6 * d.lab_031 + 0.5 * d.lab_112)
todo = ml.proceso_clasificacion(
    n=5000, x=X, puntaje=puntaje, fracciones=(1, 0, 0),
    ruido=ml.efecto_grupo(n_grupos=1000, desv_grupo=1.0, desv=0.0),
    faltantes={"lab_007": (0.2, "azar")}, semilla=SEMILLA, n_realidad=1000).ent
todo = todo.rename(columns={"grupo": "paciente"})
nuevos = todo["paciente"] >= 800               # 200 pacientes que nadie ha visto
prueba_sellada = ml.sellar(todo[nuevos].copy())
desarrollo = todo[~nuevos].copy()
rng = np.random.default_rng([SEMILLA, 1])
desarrollo["costo_del_reingreso"] = desarrollo["y"] * rng.lognormal(10, 0.5,
                                                                    len(desarrollo))
META = {"columnas_x": ["edad", "visitas_previas"] + LABS + ["costo_del_reingreso"],
        "columnas_contexto": ["paciente", "fecha"], "tarea": "clasificacion",
        "clases": [0, 1], "K": 2}
desarrollo.attrs = {"ml": META}
print(f"desarrollo: {len(desarrollo)} visitas de {desarrollo['paciente'].nunique()} "
      f"pacientes; reingresos: {desarrollo['y'].mean():.1%}")
print(f"prueba sellada: {len(prueba_sellada)} visitas, abierta "
      f"{prueba_sellada.aperturas} veces")

# %% [codigo] bloque-1-prueba
#@title El trabajo del compañero (léelo: es su separación y su tubería)
dup = desarrollo.sample(frac=0.10, random_state=SEMILLA)          # capturadas dos veces
compa = pd.concat([desarrollo, dup]).sample(frac=1, random_state=SEMILLA)
ent_c, val_c = compa.iloc[:int(0.75 * len(compa))], compa.iloc[int(0.75 * len(compa)):]
corr = compa[LABS + ["y"]].corr()["y"].drop("y").abs()             # con todo desarrollo
SUYAS = ["edad", "visitas_previas", "costo_del_reingreso"] + list(
    corr.sort_values(ascending=False).index[:15])
imp_ent = ml.imputar_simple(ent_c, ["lab_007"])
imp_val = ml.imputar_simple(val_c, ["lab_007"])                    # reajustado en val
ent_c, val_c = imp_ent.transformar(ent_c), imp_val.transformar(val_c)
for df in (ent_c, val_c):
    df.attrs = {"ml": {**META, "columnas_x": SUYAS + ["lab_007_falta"]}}
modelo_compa = ml.ajustar(ent_c, phi=ml.estandarizar(ml.columnas(
    *SUYAS, "lab_007_falta")), pesos="balanceado")
MCC_COMPA = ml.evaluar(modelo_compa, val_c, "mcc")
print(f"el compañero reporta un MCC de {MCC_COMPA:.2f} en su validación")

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
imp = ml.importancia(modelo_compa, val_c, "mcc")
ml.dibujar_importancia(imp.sort_values(ascending=False).head(10))
plt.show()
cols_adv = ["edad", "visitas_previas"] + LABS[:20]
a, b = ent_c.assign(grupo=ent_c["paciente"]), val_c.assign(grupo=val_c["paciente"])
adv = ml.validacion_adversarial(a, b, columnas=cols_adv, particion="grupo")
print(f"adversarial (pliegues por paciente): pérdida log {adv.log_loss:.3f} "
      f"contra {adv.log_loss_benchmark:.3f} → {adv.senal}")
ambos = set(ent_c["paciente"]) & set(val_c["paciente"])
repetidas = val_c.index.isin(ent_c.index).sum()
print(f"pacientes en los dos lados: {len(ambos)} · visitas de val repetidas en ent: "
      f"{repetidas}")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
limpio = desarrollo.drop(columns="costo_del_reingreso")
limpio.attrs = {"ml": {**META, "columnas_x": ["edad", "visitas_previas"] + LABS,
                       "columnas_universo": ["edad", "visitas_previas"] + LABS}}
PLIEGUES = ml.pliegues(limpio.assign(grupo=limpio["paciente"]), k=5, como="grupo",
                       estratificar=True, semilla=SEMILLA)


def cv(df, construir):
    r = ml.validacion_cruzada(df, construir, particion=lambda d: PLIEGUES,
                              criterio="mcc")
    return pd.Series(r.por_pliegue).describe()[["50%", "min", "max"]]


# ← propio: un arreglo por línea; esta es la del compañero sin la columna posterior
ARREGLOS = {"sin costo_del_reingreso": cv(limpio, ml.tuberia(
    ml.imputador(), ml.estandarizar(ml.columnas(*SUYAS[:2], *SUYAS[3:])),
    modelo={"familia": "logistica", "pesos": "balanceado"}))}
print(pd.DataFrame(ARREGLOS).T.round(2).to_string())

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
# τ = 0.5 fijo antes de empezar: aquí no se elige τ, no se recalibra ni se usa
# conformal, así que no hay reservas y el cierre usa todo desarrollo.
# Pasos disponibles: ml.imputador(), ml.seleccionar(k), ml.estandarizar(Φ), ml.columnas
TUBERIA = ml.tuberia(ml.imputador(),                       # ← completa: ¿qué falta?
                     ml.estandarizar(ml.columnas("edad", "visitas_previas")),
                     modelo={"familia": "logistica", "pesos": "balanceado"})
cv_limpia = cv(limpio, TUBERIA)
print(f"CV por pacientes, estratificada (mediana, mín, máx): "
      f"{cv_limpia.round(2).to_list()} · benchmark: MCC 0")

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
final = TUBERIA(limpio)                    # ← completa: reajusta con todo desarrollo

# %% [codigo] bloque-5-prueba
#@title Abre la prueba sellada, una sola vez
# abre-prueba: abre la prueba sellada una vez, con todo fijado
prueba = prueba_sellada.abrir().assign(costo_del_reingreso=0.0)  # al dar de alta: 0
prueba = prueba.assign(grupo=prueba["paciente"])
prueba.attrs = {"ml": META}
prueba_c = imp_ent.transformar(prueba)      # lo que necesita el modelo del compañero
filas = []
for nombre, m, df in (("tu modelo", final, prueba), ("el del compañero", modelo_compa,
                                                     prueba_c)):
    for crit in ("mcc", "aciertos_balanceados"):
        inc = ml.incertidumbre(m, df, crit, grupo="grupo", repeticiones=1000)
        filas.append((nombre, crit, inc.valor, *inc.intervalo, inc.esquema))
print(pd.DataFrame(filas, columns=["modelo", "criterio", "valor", "2.5 %", "97.5 %",
                                   "esquema"]).round(3).to_string(index=False))
y, pt, pc = prueba["y"].values, final.predecir(prueba), modelo_compa.predecir(prueba_c)
filas_de = prueba.groupby("paciente").indices                 # remuestrear pacientes
rng_b, difs = np.random.default_rng(SEMILLA), []
for _ in range(1000):
    elegidos = rng_b.choice(list(filas_de), len(filas_de))
    r = np.concatenate([filas_de[p] for p in elegidos])
    difs.append(ml.mcc(y[r], pt[r], clases=[0, 1]) - ml.mcc(y[r], pc[r], clases=[0, 1]))
print(f"(ii) tu MCC − el del compañero: {filas[0][2] - filas[2][2]:.2f} "
      f"[{np.percentile(difs, 2.5):.2f}, {np.percentile(difs, 97.5):.2f}] "
      "remuestreando pacientes")
print(f"(i) optimismo del compañero: {MCC_COMPA - filas[2][2]:.2f}")
print(f"la prueba sellada se abrió {prueba_sellada.aperturas} vez")

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] cierre
