# Tarea 5a de la unidad 9 · Series de tiempo: la CV al azar contra la temporal
# (clase 5). Código y orden de celdas: prog-c5 (clase_5.md §10.6). El texto de
# cada celda [texto] vive en tarea_5a_series_de_tiempo.texto.md (guion de Codex).
# Sin -explica ni respuestas. Especificación privada (no va al guion): UNA serie
# de 720 días generada con proceso(..., fracciones=(1, 0, 0), ruido=ar1(0.9)); los
# días 1–600 son la historia y 601–720 su continuación (no despliegue="futuro",
# contrato v5 §5.5, r3-10). La deriva lenta es un término en t dentro de f (nunca
# deriva=, que con despliegue="igual" es ValueError). D-009.6: sin deriva, la CV
# al azar de vecinos promete al menos la mitad del error de la temporal y la del
# lineal queda a menos de 10 %; lo fija la sección «promesa» de
# tools/test_ml_cifras_c5.py, que ejecuta la celda bloque-1-juega de este archivo.
# No lee la prueba: el despliegue son los días 601–720.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
SEMILLA = 0          # ← o los últimos cuatro dígitos de tu clave única
PERSISTENCIA = 0.9   # ← la memoria del ruido (bloque 5: prueba 0)
DERIVA = False       # ← una subida lenta del nivel (bloque 5: prueba True)

import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


def nivel(d):        # minutos del día: semana, lluvia de ayer y, si hay, deriva
    finde = np.isin(np.asarray(d["t"]) % 7, (5, 6))
    return 30 + 4 * finde + 5 * d["lluvia_ayer"] + (0.02 * d["t"] if DERIVA else 0)


serie = ml.proceso(n=720, x={"lluvia_ayer": ml.categorica([0, 1], [0.75, 0.25])},
                   f=nivel, ruido=ml.ar1(PERSISTENCIA, 3.0), fracciones=(1, 0, 0),
                   semilla=SEMILLA).ent.sort_values("t").reset_index(drop=True)
serie["dia_semana"] = serie["t"] % 7
serie["ayer"] = serie["y"].shift(1)                # y de ayer: se conoce al emitir
historia, futuro = serie.iloc[:600].copy(), serie.iloc[600:].copy()
for parte in (historia, futuro):
    parte.attrs = {"ml": {"columnas_x": ["dia_semana", "lluvia_ayer"],
                          "columnas_contexto": ["t"], "tarea": "regresion"}}
COLUMNAS = pd.DataFrame({"columna": ["t", "dia_semana", "lluvia_ayer", "ayer", "y"],
                         "¿se conoce al emitir?": ["", "", "", "", ""]})
print(COLUMNAS.to_string(index=False))
ax = serie.plot(x="t", y="y", figsize=(10, 3), legend=False)
ax.axvline(600, color="k", ls="--")
ax.set_title("La serie: historia (días 1–600) y su continuación (601–720)")
plt.show()

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
azar = ml.pliegues(historia, k=5, como="azar", semilla=SEMILLA)
temporal = ml.pliegues(historia, k=5, como="temporal")
fig, (a, b) = plt.subplots(2, 1, figsize=(10, 5))
ml.dibujar_pliegues(600, 5, particion=azar, ax=a)
ml.dibujar_pliegues(600, 5, particion=temporal, ax=b)
plt.show()
ajuste, valida = azar[0]
fraccion = None      # ← completa: días de valida con su día anterior en ajuste
if fraccion is not None:
    print(f"en el primer pliegue al azar: {fraccion:.2f}")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
PHI = ml.combinar(ml.dummies("dia_semana"), ml.columnas("lluvia_ayer"))
XT = ["dia_semana", "lluvia_ayer", "t"]
CANDIDATOS = {
    "lineal en x": lambda df: ml.ajustar(df, phi=PHI),
    "vecinos en (x, t)": lambda df: ml.ajustar_otro(
        df, familia="vecinos", n_vecinos=5, columnas_x=XT),
    "bosque en (x, t)": lambda df: ml.ajustar_otro(
        df, familia="bosque", n_arboles=100, columnas_x=XT),
}
TABLA = pd.DataFrame({
    nombre: {p: ml.validacion_cruzada(historia, c, k=5, particion=p).media
             for p in ("azar", "temporal")}
    for nombre, c in CANDIDATOS.items()}).T
benchmark = None     # ← completa: «el valor de ayer» (shift(1)), mismos pliegues
if benchmark is not None:
    TABLA.loc["el valor de ayer"] = benchmark
print(TABLA.round(1).to_string())

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
PARTICION = "azar"   # ← cambia: ¿con qué partición eliges? Corre con las dos
sel = ml.elegir(historia, CANDIDATOS, con="cv", particion=PARTICION)
final = sel.modelo_final                       # reajustado con los días 1–600
error_601_720 = ml.evaluar(final, futuro)    # error en los días 601–720 (no es R)
print(f"elegido: {sel.elegido}; error en los días 601–720: {error_601_720:.1f}")
for nombre, c in CANDIDATOS.items():
    m = c(historia)
    print(f"{nombre}: error en los días 601–720 = {ml.evaluar(m, futuro):.1f}; "
          f"CV al azar {TABLA.loc[nombre, 'azar']:.1f}, "
          f"temporal {TABLA.loc[nombre, 'temporal']:.1f}")

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
# Cambia PERSISTENCIA y DERIVA en la celda del bloque 1, vuelve a correr todo y
# mira aquí los residuales del lineal en el orden del tiempo.
lineal = CANDIDATOS["lineal en x"](historia)
ml.dibujar_residual_tiempo(lineal, historia)
plt.show()
r = ml.autocorrelacion(historia["y"] - lineal.predecir(historia), rezagos=10)
print("autocorrelación, rezagos 1–10:", np.round(r, 2))

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr la celda
datos = ml.proceso(n=600, x={"lluvia_ayer": ml.categorica([0, 1], [0.75, 0.25])},
                   f=lambda d: 30 + 5 * d["lluvia_ayer"],
                   ruido=ml.ar1(persistencia=0.9, desv=3.0), separar="tiempo",
                   despliegue="futuro")
ml.taller(datos, clase=5)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: la memoria y el pliegue raro
ml.galeria(clase=5, casos=[13, 16])

# %% [texto] cierre
