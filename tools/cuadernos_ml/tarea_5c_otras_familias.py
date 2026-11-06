# Tarea 5c (opcional) de la unidad 9 · Otras familias: árbol, bosque y boosting
# con la misma validación (clase 5). Código y orden de celdas: prog-c5
# (clase_5.md §10.6). El texto de cada celda [texto] vive en
# tarea_5c_otras_familias.texto.md (guion de Codex). Sin -explica ni respuestas.
# Proceso: las entregas del notebook 10 con una curva fuerte en distancia y una
# interacción lluvia × hora; despliegue con clientes nuevos. Regresión de minutos:
# sin pesos (r2-07). No lee la prueba. Galería: excepción pedida (plan-c5-9); si
# coord la rechaza, galeria(clase=5, casos=[16]), que es la que va aquí.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
SEMILLA = 0          # ← o los últimos cuatro dígitos de tu clave única
import time, warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
X = {"distancia": ml.uniforme(0, 6), "hora": ml.uniforme(8, 22),
     "lluvia": ml.categorica([0, 1], [0.8, 0.2])}
f = lambda d: (10 + 3 * d.distancia ** 2 - 0.3 * d.distancia ** 3
               + 0.8 * d.lluvia * (d.hora - 8))
datos = ml.proceso(n=600, x=X, f=f, ruido=ml.efecto_grupo(n_grupos=120, desv_grupo=2.0),
                   separar="grupo", despliegue="grupos_nuevos", semilla=SEMILLA)
PARTICION = ml.pliegues(ml._desarrollo(datos), k=5, como="grupo", semilla=SEMILLA)
mismos = lambda df: PARTICION          # la misma partición para todas las familias
print(f"desarrollo: {len(datos.ent) + len(datos.val)} pedidos; "
      f"pliegues de {[len(v) for _, v in PARTICION]} pedidos, por cliente")

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
PROF = list(range(1, 13))
cv_arbol = {p: ml.validacion_cruzada(datos, lambda df, p=p: ml.ajustar_otro(
    df, familia="arbol", profundidad=p), particion=mismos) for p in PROF}
medias = np.array([cv_arbol[p].media for p in PROF])
ees = np.array([cv_arbol[p].ee for p in PROF])
plt.errorbar(PROF, medias, yerr=ees, marker="^")
plt.xlabel("profundidad"); plt.ylabel("CV por clientes (min²)"); plt.show()
minimo = PROF[int(np.argmin(medias))]
un_ee = None         # ← completa: la profundidad más chica a un EE del mínimo
print(f"mínimo en profundidad {minimo}; regla de un EE: {un_ee}")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
from sklearn.ensemble import RandomForestRegressor   # para sortear su semilla
COLS = ["distancia", "hora", "lluvia"]
dev = ml._desarrollo(datos)


def cv_bosque(B, semilla_bosque):   # los datos no cambian: cambia el ajuste
    errores = []
    for ajuste, valida in PARTICION:
        b = RandomForestRegressor(n_estimators=B, random_state=semilla_bosque, n_jobs=1)
        b.fit(dev.iloc[ajuste][COLS], dev.iloc[ajuste]["y"])
        e = dev.iloc[valida]["y"] - b.predict(dev.iloc[valida][COLS])
        errores.append(float(np.mean(e ** 2)))
    return np.mean(errores)


BS = [10, 300]
tabla_b = pd.DataFrame({s: [cv_bosque(B, s) for B in BS] for s in (0, 1, 2)}, index=BS)
tabla_b.plot(marker="^", logx=True)
plt.xlabel("árboles B"); plt.ylabel("CV"); plt.show()
print(tabla_b.round(2).to_string())

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
ETAPAS = [10, 50, 200, 400]
for tasa in (0.1, 0.01):
    cv_b = [ml.validacion_cruzada(datos, lambda df, e=e: ml.ajustar_otro(
        df, familia="boosting", etapas=e, tasa=tasa), particion=mismos).media
        for e in ETAPAS]
    plt.plot(ETAPAS, cv_b, marker="^", label=f"ν = {tasa}")
plt.xscale("log"); plt.xlabel("etapas"); plt.ylabel("CV por clientes (min²)")
plt.legend(); plt.show()

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
FAMILIAS = {"lineal": lambda df: ml.ajustar(df, phi=ml.combinar(
                ml.polinomio(3, variable="distancia"), ml.columnas("hora", "lluvia"))),
            "árbol": lambda df: ml.ajustar_otro(df, familia="arbol",
                                                profundidad=minimo),
            "bosque": lambda df: ml.ajustar_otro(df, familia="bosque", n_arboles=100),
            "boosting": lambda df: ml.ajustar_otro(df, familia="boosting", etapas=100)}
filas = []
for nombre, c in FAMILIAS.items():
    t0 = time.time()
    r = ml.validacion_cruzada(datos, c, particion=mismos)
    filas.append((nombre, r.media, r.ee, time.time() - t0))
media = ml.validacion_cruzada(datos, lambda df: ml.ajustar(
    df, phi=ml.polinomio(0, variable="distancia")), particion=mismos)
filas.append(("benchmark (la media)", media.media, media.ee, 0.0))
print(pd.DataFrame(filas, columns=["familia", "CV", "EE entre pliegues", "segundos"])
      .round(2).to_string(index=False))
lejos = pd.DataFrame({"distancia": [12.0], "hora": [15.0], "lluvia": [0]})
print({n: float(c(dev).predecir(lejos)[0]) for n, c in FAMILIAS.items()},
      "f verdadera:", float(f(lejos)[0]))

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr la celda
datos = ml.proceso(n=600, x=X, f=f, ruido=ml.efecto_grupo(n_grupos=120, desv_grupo=2.0),
                   separar="grupo", despliegue="grupos_nuevos", semilla=SEMILLA)
ml.taller(datos, clase=5)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: el pliegue raro
ml.galeria(clase=5, casos=[16])

# %% [texto] cierre
