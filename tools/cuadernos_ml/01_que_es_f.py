# Notebook 01 de la unidad 9 · ¿Qué es f? (acompaña ml-que-es-f, clase 1).
# Código y orden de celdas: prog-c1 (clase_1.md §10.3 NB01). El texto de cada
# celda [texto] vive en 01_que_es_f.texto.md (guion de Codex). Todo proceso se
# construye con fracciones=(1, 0, 0): en la clase 1 no hay validación ni
# prueba, y «20 datos» son 20 de entrenamiento.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: el proceso que no vemos
import numpy as np
import matplotlib.pyplot as plt

SEMILLA = 0
PROCESOS_B1 = {"entregas": "entregas", "recíproca": "inverso",
               "mezcla de logaritmos": "mezcla_logs", "seno": "seno"}


def bloque_1(proceso, sigma, n, semilla):
    datos = ml.PROCESOS[proceso](n=n, semilla=semilla, ruido=ml.normal(0, sigma),
                                 fracciones=(1, 0, 0))
    recta = ml.ajustar(datos)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ml.dibujar_proceso(datos, puntos_realidad=300, ax=ax)
    ml.dibujar_ajuste({"f̂: la recta ajustada": recta}, datos, ax=ax)
    plt.show()
    media = ml.benchmarks(datos, datos.despliegue).loc["media", "cuadratica"]
    print(f"L_ent (entrenamiento, {n} datos) = {ml.L(recta, datos.ent):.3f}")
    print(f"R(β̂) (despliegue, 100 000 obs.) = {ml.riesgo(recta, datos):.3f}"
          f"   ·   benchmark, la media de ent: R = {media:.3f}")


ml.laboratorio(
    bloque_1,
    proceso=ml.selector("proceso", PROCESOS_B1),
    sigma=ml.deslizador("ruido σ_ε", 0.0, 3.0, 0.25, 1.0),
    n=ml.deslizador("datos n", 10, 500, 10, 20),
    semilla=ml.deslizador("semilla", 0, 20, 1, SEMILLA),
)

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: el piso que nadie baja
SEMILLA = 0


class Fijo(ml.Modelo):
    """Un predictor que no se ajusta: predice con una función fija de x."""
    tarea = "regresion"

    def __init__(self, g):
        self.g = g

    def predecir(self, df):
        return np.asarray(self.g(df), dtype=float)


def bloque_2(sigma, n):
    datos = ml.PROCESOS["entregas"](n=n, sigma_e=sigma, semilla=SEMILLA,
                                     fracciones=(1, 0, 0))
    ybar = datos.ent["y"].mean()
    modelos = {"oráculo f": Fijo(lambda d: 10 + 4 * d["x"]),
               "recta ajustada": ml.ajustar(datos),
               "media (benchmark)": Fijo(lambda d: np.full(len(d), ybar))}
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ml.dibujar_piso(datos, modelos, ax=ax)
    plt.show()
    print(f"piso R_Bayes = σ_ε² = {ml.piso(datos):.3f}")
    for nombre, m in modelos.items():
        print(f"{nombre:>18}: L_ent = {ml.L(m, datos.ent):7.3f}"
              f"   R (despliegue) = {ml.riesgo(m, datos):7.3f}")


ml.laboratorio(
    bloque_2,
    sigma=ml.deslizador("ruido σ_ε", 0.0, 3.0, 0.25, 1.0),
    n=ml.deslizador("datos n", 10, 500, 10, 20),
)

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: ruido que no es ruido (la lluvia)
SEMILLA = 0
LLUVIA = {False: ml.caso(2, semilla=SEMILLA),
          True: ml.caso(2, omitir=None, semilla=SEMILLA)}


def _phi_lluvia(medir, N):
    if medir:
        return ml.combinar(ml.polinomio(N, "x1"), ml.columnas("x2"))
    return ml.polinomio(N, "x1")


AJUSTES_B3 = {(medir, N): ml.ajustar(LLUVIA[medir], phi=_phi_lluvia(medir, N))
              for medir in (False, True) for N in range(1, 6)}


def bloque_3(medir, N):
    datos, m = LLUVIA[medir], AJUSTES_B3[(medir, N)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
    ml.dibujar_proceso(datos, color_por="x2" if medir else None, ax=a1)
    ml.dibujar_piso(datos, {f"grado {N}": m}, ax=a2)
    plt.show()
    media = ml.benchmarks(datos, datos.despliegue).loc["media", "cuadratica"]
    print(f"columnas que ve el modelo: {datos.columnas_x}")
    print(f"piso = {ml.piso(datos):.2f}   ·   R (despliegue) = {ml.riesgo(m, datos):.2f}"
          f"   ·   benchmark, la media de ent: R = {media:.2f}")


ml.laboratorio(
    bloque_3,
    medir=ml.interruptor("medir la lluvia x₂", False),
    N=ml.deslizador("grado N", 1, 5, 1, 1),
)

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: laboratorio polar
import warnings

SEMILLA = 0
REPRESENTACIONES = {"cartesianas (1, x₁, x₂)": None,
                    "polares (1, r, θ)": ml.polares(),
                    "solo radio (1, r)": ml.polares(incluir=("r",))}


def bloque_4(radio_exterior, grosor, ruido, representacion):
    datos = ml.anillos(n=400, radio_exterior=radio_exterior, grosor=grosor,
                       ruido=ruido, semilla=SEMILLA, fracciones=(1, 0, 0))
    phi = REPRESENTACIONES[representacion]
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        m = ml.ajustar(datos, phi=phi, tarea="clasificacion")
    if any("separan" in str(a.message) for a in avisos):
        print("Los datos se separan: sin penalización la logística no tiene "
              "coeficientes óptimos finitos; crecen hasta que el optimizador se detiene.")
    vista = "cartesianas" if phi is None else "polares"
    ml.dibujar_frontera(m, datos.ent, vista=vista)
    plt.show()
    ml.imprimir_Phi(m, datos.ent, filas=4)
    desp = datos.despliegue
    moda = ml.benchmarks(datos, desp).loc["moda", "aciertos"]
    bayes = np.mean((desp["prob"] >= 0.5).astype(int) == desp["y"])
    print(f"aciertos en ent = {ml.evaluar(m, datos.ent, 'aciertos'):.3f}   ·   "
          f"aciertos en el despliegue = {ml.desempeno(m, datos, 'aciertos'):.3f}")
    print(f"benchmark, la moda: {moda:.3f}   ·   techo de Bayes: {bayes:.3f}")
    print("coeficientes β̂:", m.beta_gorro.round(3).to_dict())


ml.laboratorio(
    bloque_4,
    radio_exterior=ml.deslizador("radio exterior", 1.3, 2.2, 0.1, 1.6),
    grosor=ml.deslizador("grosor", 0.3, 0.8, 0.05, 0.4),
    ruido=ml.deslizador("ruido", 0.1, 0.4, 0.05, 0.15),
    representacion=ml.selector("representación", list(REPRESENTACIONES)),
)

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: lineal en β
import pandas as pd

SEMILLA = 0
DATOS_B5 = {"entregas con lluvia": (ml.caso(2, omitir=None, semilla=SEMILLA), "x1"),
            "recíproca": (ml.PROCESOS["inverso"](semilla=SEMILLA, fracciones=(1, 0, 0)), "x")}
PHIS_B5 = {"(1, x)": lambda v: ml.columnas(v),
           "(1, x, x²)": lambda v: ml.columnas(v, f"{v}**2"),
           "(1, 1/x)": lambda v: ml.columnas(f"1/{v}"),
           "(1, x) + lluvia": lambda v: ml.combinar(ml.columnas(v), ml.dummies("x2"))}


def bloque_5(proceso, phi):
    datos, v = DATOS_B5[proceso]
    if phi.endswith("lluvia") and "x2" not in datos.ent:
        print("La recíproca no trae lluvia: esta φ no aplica. Elige otra.")
        return
    m = ml.ajustar(datos, phi=PHIS_B5[phi](v))
    x = np.linspace(datos.ent[v].min(), datos.ent[v].max(), 300)
    curvas = {f"φ = {phi}, sin lluvia" if "x2" in datos.ent else f"φ = {phi}":
              lambda x: m.predecir(pd.DataFrame({v: x, "x2": 0}))}
    if phi.endswith("lluvia"):
        curvas["con lluvia"] = lambda x: m.predecir(pd.DataFrame({v: x, "x2": 1}))
    ml.dibujar_ajuste(curvas, datos)
    plt.show()
    print("m = ml.ajustar(datos, phi=...)   ← la misma línea con cualquier φ")
    ml.imprimir_Phi(m, datos.ent, filas=4)
    media = ml.benchmarks(datos, datos.despliegue).loc["media", "cuadratica"]
    print(f"L_ent = {ml.L(m, datos.ent):.3f}   ·   R (despliegue) = "
          f"{ml.riesgo(m, datos):.3f}   ·   benchmark, la media de ent: R = {media:.3f}")


ml.laboratorio(
    bloque_5,
    proceso=ml.selector("proceso", list(DATOS_B5)),
    phi=ml.selector("φ", list(PHIS_B5)),
)

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.proceso(n=20, x={"x": ml.uniforme(0, 6)},
                   f=lambda d: 10 + 4 * d.x, ruido=ml.normal(0, 1),
                   fracciones=(1, 0, 0))
# datos = ml.proceso(n=20, x={"x": ml.uniforme(0.3, 3)}, f=lambda d: 2 + 5 / d.x,
#                    ruido=ml.normal(0, 0.5), fracciones=(1, 0, 0))
# datos = ml.proceso(n=50, x={"x": ml.uniforme(0, 2)},
#                    f=lambda d: 4 + 2 * np.sin(5 * d.x),
#                    ruido=ml.normal(0, 0.3), fracciones=(1, 0, 0))
# datos = ml.caso(2)   # una variable que existe y no mides: la lluvia
ml.taller(datos, clase=1)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=1, casos=[1, 2])

# %% [texto] ejercicio-piso

# %% [texto] ejercicio-piso-respuesta

# %% [texto] ejercicio-phi

# %% [texto] ejercicio-phi-respuesta

# %% [texto] cierre
