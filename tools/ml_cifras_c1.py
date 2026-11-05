"""Cifras de la clase 1 de la unidad de aprendizaje de maquina (unidad 9).

Una funcion por hecho que cita una pagina, un notebook o una figura de la
clase 1 (clase_1.md §10.7). Ninguna cifra de la clase se escribe a mano: la
pagina la copia de aqui, tools/test_ml_cifras_c1.py la fija en la fuente y
tools/test_ml_prosa_c1.py la busca en la seccion de la pagina que la cita
(D-009.5, D-003).

Las funciones que calculan con ml_lab lo importan de tools/ (nunca de
_assets/, D-004) y solo dentro de la funcion: las de numpy puro no lo
necesitan (contrato v3 §5.2, r1-40).

Anclas por tramo (protocolo p5.2 §7.1): cada rama escribe solo antes del
«fin» de su tramo. La rama de clase escribe el tramo 1a; la subrama -b, el
1b; la -c, el de la tarea.
"""
import importlib
import math
from fractions import Fraction

import numpy as np
import pandas as pd


def _ml():
    """tools/aprendizaje_maquina.py (ml_lab), importado al pedirlo."""
    return importlib.import_module("aprendizaje_maquina")


# Las seis entregas de la unidad 6 (course/6_optimizacion/5_practica_de_modelado/
# 4_regresion_practica.md, § «Los datos»): distancia en km y tiempo en minutos.
ENTREGAS_X = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
ENTREGAS_Y = (15.0, 17.0, 23.0, 25.0, 31.0, 33.0)


def _predictor_fijo(funcion):
    """Un Modelo de ml_lab que predice con una funcion fija del DataFrame.

    Sirve para medir el riesgo del oraculo (f misma) y de la media de
    entrenamiento con las mismas funciones de ml_lab que miden un ajuste.
    """
    ml = _ml()

    class _Fijo(ml.Modelo):
        familia = "fija"
        tarea = "regresion"

        def predecir(self, df):
            return np.asarray(funcion(df), dtype=float)

    return _Fijo()


# --- tramo 1a ---

def cifras_c1_ganador():
    """P1 §1, §3 (micro) y cierre: la recta y el polinomio de grado 5 de las
    seis entregas. RMSE y MSE en las seis, MSE de la recta fija 10 + 4x
    (elegida antes de ver los datos) y las predicciones a 7, 3.5 y 0 km.
    Numpy puro (C1.T2a)."""
    x = np.array(ENTREGAS_X)
    y = np.array(ENTREGAS_Y)
    p1 = np.polyfit(x, y, 1)
    p5 = np.polyfit(x, y, 5)
    mse_1 = float(np.mean((np.polyval(p1, x) - y) ** 2))
    mse_5 = float(np.mean((np.polyval(p5, x) - y) ** 2))
    mse_fija = float(np.mean((10 + 4 * x - y) ** 2))
    prediccion = {km: (float(np.polyval(p1, km)), float(np.polyval(p5, km)))
                  for km in (7.0, 3.5, 0.0)}
    return {
        "intercepto_recta": float(p1[1]),
        "pendiente_recta": float(p1[0]),
        "coeficientes_grado_5": [float(c) for c in p5],
        # Los mismos coeficientes como fracciones (de x^5 a la constante): la
        # pagina escribe el polinomio con ellas para que el ejercicio de §1 se
        # pueda resolver sustituyendo (revision r1 del tramo 1a).
        "coeficientes_grado_5_fracciones": [Fraction(float(c)).limit_denominator(100)
                                            for c in p5],
        "pendiente_recta_fraccion": Fraction(float(p1[0])).limit_denominator(100),
        "rmse_1": float(np.sqrt(mse_1)),
        "rmse_5": float(np.sqrt(max(mse_5, 0.0))),
        "mse_1": mse_1,
        "mse_fija": mse_fija,
        "prediccion": prediccion,
    }


# Las entregas de la clase 1 en ml_lab: PROCESOS["entregas"], f = 10 + 4x,
# x ~ U(0, 6), 20 datos, todos de entrenamiento (clase_1.md §10.3).
N_ENTREGAS = 20
SIGMAS_PISO = (1.0, 2.0)


def datos_entregas(sigma_e=1.0, semilla=0):
    """Las 20 entregas de la clase 1 (todas de entrenamiento)."""
    return _ml().PROCESOS["entregas"](n=N_ENTREGAS, sigma_e=sigma_e, semilla=semilla,
                                       fracciones=(1, 0, 0))


def modelos_piso(datos):
    """Los tres predictores de ml-c1-piso y del bloque 2 de NB01: el oraculo
    (f misma), la recta ajustada y la media de entrenamiento (benchmark)."""
    ml = _ml()
    media = float(datos.ent["y"].mean())
    return {
        "oráculo f": _predictor_fijo(lambda df: 10 + 4 * df["x"]),
        "recta ajustada": ml.ajustar(datos),
        "media (benchmark)": _predictor_fijo(lambda df: np.full(len(df), media)),
    }


def cifras_c1_piso(semilla=0):
    """P1 §3 y §4, NB01 bloque 2, figura ml-c1-piso. Para sigma_e = 1 y 2:
    el piso (sigma_e²), el R de oraculo, recta y media aproximado con las
    100 000 observaciones de despliegue, y el error de aproximacion de esa
    muestra enorme (desviacion estandar de la perdida / sqrt(100 000))."""
    ml = _ml()
    salida = {}
    for s in SIGMAS_PISO:
        datos = datos_entregas(sigma_e=s, semilla=semilla)
        desp = datos.despliegue
        fila = {"piso": float(ml.piso(datos)), "n_despliegue": len(desp),
                "n_ent": len(datos.ent)}
        for nombre, modelo in modelos_piso(datos).items():
            l_i = ml.perdida(desp["y"], modelo.predecir(desp))
            clave = nombre.split()[0].replace("á", "a")
            fila[f"R_{clave}"] = float(ml.riesgo(modelo, datos))
            fila[f"ee_{clave}"] = float(np.std(l_i, ddof=1) / np.sqrt(len(l_i)))
        modelos = modelos_piso(datos)
        fila["L_ent_recta"] = float(ml.L(modelos["recta ajustada"], datos.ent))
        fila["L_ent_oraculo"] = float(ml.L(modelos["oráculo f"], datos.ent))
        salida[s] = fila
    return salida


def cifras_c1_bloque_1(semilla=0):
    """NB01 bloque 1 con sus controles iniciales (proceso «entregas», ruido
    normal de desviacion 1, 20 datos, semilla 0), por el mismo camino que la
    celda: L_ent de la recta, su R en el despliegue y el de la media
    (benchmark) en el despliegue."""
    ml = _ml()
    datos = ml.PROCESOS["entregas"](n=N_ENTREGAS, semilla=semilla, ruido=ml.normal(0, 1.0),
                                    fracciones=(1, 0, 0))
    recta = ml.ajustar(datos)
    return {
        "L_ent_recta": float(ml.L(recta, datos.ent)),
        "R_recta": float(ml.riesgo(recta, datos)),
        "R_media": float(ml.benchmarks(datos, datos.despliegue).loc["media", "cuadratica"]),
    }


def datos_lluvia(medir_lluvia=False, semilla=0):
    """El caso 2 (la lluvia): 20 entregas; con medir_lluvia, x2 es visible."""
    ml = _ml()
    if medir_lluvia:
        return ml.caso(2, omitir=None, semilla=semilla)
    return ml.caso(2, semilla=semilla)


def cifras_c1_lluvia():
    """P1 §5 (ml-c1-ejm-lluvia), NB01 bloque 3, figura ml-c1-dos-franjas: el
    piso sin y con la lluvia, la cuenta exacta 1 + 36·(1/4), y la pendiente de
    x1 ajustada sin y con x2 (insesgada en los dos casos)."""
    ml = _ml()
    sin = datos_lluvia(False)
    con = datos_lluvia(True)
    m_sin = ml.ajustar(sin)
    m_con = ml.ajustar(con)
    return {
        "piso_sin_x2": float(ml.piso(sin)),
        "piso_con_x2": float(ml.piso(con)),
        "piso_sin_x2_exacto": 1 + 6 ** 2 * 0.25,
        "piso_con_x2_exacto": 1.0,
        "beta1_sin_x2": float(m_sin.beta_gorro["x1"]),
        "beta1_con_x2": float(m_con.beta_gorro["x1"]),
        "R_recta_sin_x2": float(ml.riesgo(m_sin, sin)),
        "R_recta_con_x2": float(ml.riesgo(m_con, con)),
        "n_ent": len(sin.ent),
        "columnas_sin": list(sin.columnas_x),
        "columnas_con": list(con.columnas_x),
        # E[y | x1] sin la lluvia, leida del proceso: 13 + 4 x1 (revision r3)
        "intercepto_sin_x2": float(np.asarray(sin.f_visible(pd.DataFrame({"x1": [0.0]})))[0]),
        "pendiente_sin_x2": float(np.asarray(sin.f_visible(pd.DataFrame({"x1": [1.0]})))[0]
                                  - np.asarray(sin.f_visible(pd.DataFrame({"x1": [0.0]})))[0]),
    }


GRADOS_LLUVIA = (1, 2, 3, 4, 5)


def phi_lluvia(medir_lluvia, N):
    """La phi del bloque 3 de NB01: polinomio de grado N en x1 y, si se mide
    la lluvia, la columna x2."""
    ml = _ml()
    if medir_lluvia:
        return ml.combinar(ml.polinomio(N, "x1"), ml.columnas("x2"))
    return ml.polinomio(N, "x1")


def cifras_c1_lluvia_grados():
    """NB01 bloque 3 (explicacion): el riesgo en el despliegue del ajuste de
    grado N = 1..5 en x1, sin y con la lluvia, con los mismos datos del caso 2
    (semilla 0) y la misma phi que el notebook. Subir el grado no baja el piso
    y con 20 datos sube el riesgo (10.89 -> 15.73 sin medir la lluvia)."""
    ml = _ml()
    salida = {}
    for medir in (False, True):
        datos = datos_lluvia(medir)
        salida[medir] = {N: float(ml.riesgo(ml.ajustar(datos, phi=phi_lluvia(medir, N)),
                                            datos))
                         for N in GRADOS_LLUVIA}
    salida["piso"] = {medir: float(ml.piso(datos_lluvia(medir))) for medir in (False, True)}
    return salida


# Los anillos de P1 §7 y del bloque 4 de NB01 (los valores por omision de sus
# deslizadores, clase_1.md §10.3): la pagina y el notebook dicen la misma cifra.
ANILLOS = {"n": 400, "radio_interior": 1.0, "radio_exterior": 1.6, "grosor": 0.4,
           "ruido": 0.15}
REPRESENTACIONES = ("cartesianas", "polares", "solo radio")


def datos_anillos(semilla=0, **cambios):
    """Los anillos de la clase 1, todos de entrenamiento."""
    return _ml().anillos(**{**ANILLOS, **cambios}, semilla=semilla, fracciones=(1, 0, 0))


def phi_anillos(representacion):
    """La phi de cada representacion: (1, x1, x2), (1, r, theta) o (1, r)."""
    ml = _ml()
    return {"cartesianas": None, "polares": ml.polares(),
            "solo radio": ml.polares(incluir=("r",))}[representacion]


def cifras_c1_anillos(semilla=0):
    """P1 §7 y cierre, NB01 bloque 4, figura ml-c1-anillos-polares. Con los
    mismos anillos recien generados: aciertos en el despliegue de la misma
    logistica en cartesianas, polares y solo radio; aciertos de la moda
    (benchmark) y del clasificador de Bayes (el oraculo); coeficientes
    ajustados, el radio de corte -b0/b1 y las columnas de cada Phi."""
    ml = _ml()
    salida = {"parametros": dict(ANILLOS)}
    for rep in REPRESENTACIONES:
        datos = datos_anillos(semilla=semilla)
        m = ml.ajustar(datos, phi=phi_anillos(rep), tarea="clasificacion")
        beta = {k: float(v) for k, v in m.beta_gorro.items()}
        fila = {"aciertos": float(ml.desempeno(m, datos, "aciertos")),
                "aciertos_ent": float(ml.evaluar(m, datos.ent, "aciertos")),
                "beta": beta, "columnas": list(m.Phi(datos.ent).columns)}
        if "r" in beta:
            fila["radio_corte"] = -beta["1"] / beta["r"]
        salida[rep] = fila
    datos = datos_anillos(semilla=semilla)
    desp = datos.despliegue
    tabla = ml.benchmarks(datos, desp)
    salida["moda"] = float(tabla.loc["moda", "aciertos"])
    salida["bayes"] = float(np.mean((desp["prob"].to_numpy() >= 0.5).astype(int)
                                    == desp["y"].to_numpy()))
    salida["radio_bayes"] = radio_bayes(datos)
    salida["n_ent"] = len(datos.ent)
    salida["n_despliegue"] = len(desp)
    return salida


def radio_bayes(datos):
    """El radio donde Pr(y = 1 | x) cruza 1/2: la frontera ideal (la del
    clasificador de Bayes) es el circulo de ese radio. Lo lee del oraculo del
    proceso (la probabilidad depende solo del radio)."""
    import pandas as pd
    rejilla = np.linspace(ANILLOS["radio_interior"], ANILLOS["radio_exterior"], 20001)
    p = np.asarray(datos._pob.prob(pd.DataFrame({"x1": rejilla, "x2": 0.0})))
    k = int(np.argmax(p >= 0.5))
    return float(np.interp(0.5, p[k - 1:k + 1], rejilla[k - 1:k + 1]))


def cifras_c1_omitida(semilla=0):
    """Galeria de NB01, caso 1 (contrato v4 §5.5): la pendiente ajustada de x1
    (va a 1.8), el coeficiente estructural de x1 (1) con beta_verdadero, la
    pendiente de E[y | x1] (1.8) y el piso con lo visible (0.86)."""
    ml = _ml()
    datos = ml.caso(1, semilla=semilla)
    m = ml.ajustar(datos)
    estructural = ml.beta_verdadero(datos, None)
    uno = datos.realidad.iloc[:1].copy()
    cero = uno.copy()
    uno["x1"], cero["x1"] = 1.0, 0.0
    pendiente_visible = float(np.asarray(datos.f_visible(uno))[0]
                              - np.asarray(datos.f_visible(cero))[0])
    return {
        "beta1_ajustada": float(m.beta_gorro["x1"]),
        "beta1_estructural": float(estructural["x1"]),
        "pendiente_f_visible": pendiente_visible,
        "piso_visible": float(ml.piso(datos)),
        "piso_visible_cuenta": 0.45 + 0.16 * 1.0 + 0.25,
        "n_ent": len(datos.ent),
    }

# P1 §2, ejercicio ml-c1-ej-residual: los datos del enunciado y sus tres
# cuentas (revision r3, D-009.5: la cifra de la respuesta sale de aqui).
RESIDUAL = {"x": 3, "f": 22.0, "y": 25.0, "f_gorro": 23.5}


def cifras_c1_residual():
    r = RESIDUAL
    return {**r, "ruido": r["y"] - r["f"], "reducible": r["f"] - r["f_gorro"],
            "residual": r["y"] - r["f_gorro"]}


def cifras_c1_ej_piso():
    """P1 §4, ejercicio ml-c1-ej-piso: y = 2x + ε con σ_ε² = 4. El MSE
    poblacional del predictor 2x es el piso, que ml_lab confirma."""
    ml = _ml()
    datos = ml.proceso(n=10, x={"x": ml.uniforme(0, 6)}, f=lambda d: 2 * d.x,
                       ruido=ml.normal(0, 2), fracciones=(1, 0, 0))
    return {"sigma2": 4.0, "piso": float(ml.piso(datos)), "n_muestra": len(datos.ent)}


def cifras_c1_arriba_abajo(semilla=0):
    """P1 §7, respuesta ml-c1-resp-representacion (a): con la etiqueta «arriba»
    (x2 > 0) sobre los mismos anillos, la logistica con phi = (1, r) acierta
    cerca de 50 % en el despliegue; por simetria, ningun clasificador que solo
    vea r pasa de 50 % (exacto: Pr(x2 > 0 | r) = 1/2)."""
    ml = _ml()
    datos = datos_anillos(semilla=semilla)
    ent, desp = datos.ent.copy(), datos.despliegue.copy()
    for df in (ent, desp):
        df["y"] = (df["x2"] > 0).astype(int)
    m = ml.ajustar(ent, phi=phi_anillos("solo radio"), tarea="clasificacion",
                   columnas_x=["x1", "x2"])
    return {"aciertos": float(ml.evaluar(m, desp, "aciertos")), "bayes_solo_r": 0.5}

# --- fin tramo 1a ---


# --- tramo 1b ---
#
# P2 (ml-polinomios-y-capacidad), NB02 y las figuras de la 1b. El hilo de P2
# es la reciproca de PROCESOS["inverso"]: f = 2 + 5/x, x ~ U(0.3, 3),
# sigma_e = 0.5 (piso 0.25), 20 datos de entrenamiento, semilla 0.

SEMILLA_1B = 0
N_MAX = 15
INVERSO_RANGO = (0.3, 3.0)
INVERSO_SIGMA2 = 0.25


def f_inverso(x):
    return 2 + 5 / np.asarray(x, float)


def datos_inverso(n=20, semilla=SEMILLA_1B, **cambios):
    """La reciproca de P2: n datos, todos de entrenamiento."""
    return _ml().PROCESOS["inverso"](n=n, semilla=semilla, fracciones=(1, 0, 0), **cambios)


def polinomios(N_max=N_MAX, variable="x", escalar=True):
    """Los candidatos de la curva de capacidad: polinomio(N) para N = 1..N_max."""
    ml = _ml()
    return {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N, variable, escalar)))
            for N in range(1, N_max + 1)}


def cifras_c1_taylor():
    """P2 §1, figura ml-c1-taylor-vs-mco: Taylor de 2 + 5/x centrado en
    x0 = 1 (grados 3 y 9) contra el polinomio de grado 3 ajustado por minimos
    cuadrados a los 20 datos. Errores |f - p| en x = 0.3, 2, 2.5 y 3 (los
    bordes del intervalo y el lado donde la serie de 1/x ya no converge).
    Ademas, el micro ml-c1-ej-taylor: Taylor de grado 1 de 1/x en 1 es 2 - x."""
    ml = _ml()
    puntos = (0.3, 2.0, 2.5, 3.0)
    datos = datos_inverso()
    mco = ml.ajustar(datos, phi=ml.polinomio(3))
    pred_mco = mco.predecir(pd.DataFrame({"x": puntos}))
    salida = {"centro": 1.0, "puntos": puntos, "rango_datos": (float(datos.ent.x.min()),
                                                                float(datos.ent.x.max()))}
    for N in (3, 9):
        t = ml.taylor("inverso", centro=1.0, N=N)
        salida[f"taylor_{N}"] = {x: float(abs(t(np.array([x]))[0] - f_inverso(x)))
                                 for x in puntos}
    salida["mco_3"] = {x: float(abs(p - f_inverso(x))) for x, p in zip(puntos, pred_mco)}
    salida["micro"] = {"taylor_en_2": 2 - 2.0, "f_en_2": 1 / 2.0, "error": abs(0.0 - 0.5)}
    return salida


def cifras_c1_micro_taylor():
    """P2 §1, micro ml-c1-ej-taylor: el Taylor de grado 1 de 1/x en x0 = 1 es
    2 - x; en x = 2 predice 0, el valor verdadero es 1/2 y el error, 1/2."""
    from fractions import Fraction
    x0, x = Fraction(1), Fraction(2)
    valor, derivada = 1 / x0, -1 / x0 ** 2          # 1/x y su derivada en x0
    pred = valor + derivada * (x - x0)
    return {"prediccion": pred, "verdadero": 1 / x, "error": abs(1 / x - pred)}


WEIERSTRASS_GRADOS = (2, 6, 14)


def cifras_c1_weierstrass(puntos_ajuste=4001, puntos_error=20001):
    """P2 §2, figura ml-c1-weierstrass: |x - 0.5| en [0, 1], ajustada por
    minimos cuadrados en una malla fina (base de Chebyshev, sin ruido) con
    grados 2, 6 y 14; el error maximo en una malla mas fina. El mejor
    polinomio en maximo tiene error a lo mas ese. Numpy puro."""
    from numpy.polynomial import chebyshev as C
    x = np.linspace(0, 1, puntos_ajuste)
    fina = np.linspace(0, 1, puntos_error)
    salida = {}
    for N in WEIERSTRASS_GRADOS:
        coef = C.chebfit(2 * x - 1, np.abs(x - 0.5), N)
        salida[N] = {"coeficientes": coef,
                     "error_maximo": float(np.max(np.abs(C.chebval(2 * fina - 1, coef)
                                                         - np.abs(fina - 0.5))))}
    return salida


TRES_GRADOS = (1, 4, 15)


def cifras_c1_tres_ajustes(semilla=SEMILLA_1B):
    """P2 §3, figura ml-c1-tres-ajustes: L_ent y R de los grados 1, 4 y 15
    sobre los 20 datos de la reciproca. R se mide con la MISMA muestra enorme
    (realidad, 100 000 observaciones) que la curva de capacidad de §4, para
    que el grado 15 tenga un solo R en toda la pagina (revision r1 del tramo
    1b: con despliegue daba 1451 en §3 y 1537 en §4). Ademas, x_max de los
    datos, la prediccion del grado 15 en x = 3 y la parte del riesgo
    reducible del grado 15 que cae a la derecha del ultimo dato (malla fina):
    el disparo es extrapolacion, no oscilacion entre los datos."""
    ml = _ml()
    datos = datos_inverso(semilla=semilla)
    salida = {"x_max": float(datos.ent.x.max())}
    for N in TRES_GRADOS:
        m = ml.ajustar(datos, phi=ml.polinomio(N))
        salida[N] = {"L_ent": float(ml.L(m, datos.ent)), "R": float(ml.L(m, datos.realidad))}
        if N == TRES_GRADOS[-1]:
            x = np.linspace(*INVERSO_RANGO, 200_001)
            p = m.predecir(pd.DataFrame({"x": x}))
            e = (f_inverso(x) - p) ** 2
            salida[N]["prediccion_en_3"] = float(p[-1])
            salida[N]["fraccion_reducible_tras_x_max"] = float(e[x > salida["x_max"]].sum()
                                                               / e.sum())
    return salida


def _curva(datos, N_max=N_MAX):
    import warnings
    ml = _ml()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tabla = ml.curva_capacidad(datos, polinomios(N_max), conjuntos=("ent", "realidad"))
    return tabla


def cifras_c1_capacidad(semilla=SEMILLA_1B):
    """P2 §4 y cierre, figura ml-c1-capacidad-brecha, NB02 bloque 2: la curva
    de capacidad N = 1..15 de la reciproca con 20 datos (L_ent y R medido
    con la muestra enorme realidad), el N de menor R, la brecha en N = 15,
    el piso y el benchmark (la media de ent evaluada en realidad); y lo mismo
    con 200 datos (el panel de contraste)."""
    ml = _ml()
    salida = {}
    for n in (20, 200):
        datos = datos_inverso(n=n, semilla=semilla)
        tabla = _curva(datos)
        ancha = tabla.pivot(index="candidato", columns="conjunto", values="L")
        L_ent = {int(N): float(v) for N, v in ancha["ent"].items()}
        R = {int(N): float(v) for N, v in ancha["realidad"].items()}
        N_opt = min(R, key=R.get)
        salida[n] = {
            "tabla": tabla, "L_ent": L_ent, "R": R, "N_menor_R": N_opt,
            "brecha_15": R[N_MAX] - L_ent[N_MAX],
            "piso": float(ml.piso(datos)),
            "benchmark": float(ml.benchmarks(datos, datos.realidad).loc["media", "cuadratica"]),
        }
    return salida


# Los «500 / 200 veces» de P2 §4 y §5 y del bloque 3 de NB02: muestras de 20
# datos de la reciproca, tomadas como trozos consecutivos de UNA muestra
# grande (son muestras independientes del mismo proceso; generarlas una por
# una tarda decenas de veces mas). Cada ajuste es el de ml.ajustar con
# polinomio(N) (x escalada a [-1, 1] con el rango de ese trozo), resuelto en
# forma cerrada con numpy; test_ml_cifras_c1 comprueba que coincide con
# ml.ajustar. R se calcula con su definicion: E_x[(f - f_gorro)²] + sigma²,
# con x uniforme en [0.3, 3], por cuadratura de Gauss-Legendre de 64 nodos
# (convergida: 200 nodos dan lo mismo a 1e-12 relativo). La malla uniforme de 1000
# puntos que habia antes sesgaba el riesgo lo bastante para mover una
# eleccion de grado (166 -> 167 entre 3 y 6) y la media del optimismo
# (0.706 -> 0.700); revision r1 del tramo 1b.
_NODOS, _PESOS = np.polynomial.legendre.leggauss(64)
MALLA_R = (INVERSO_RANGO[1] - INVERSO_RANGO[0]) / 2 * _NODOS + sum(INVERSO_RANGO) / 2
PESOS_R = _PESOS / 2


def trozos_inverso(repeticiones, n=20, semilla=SEMILLA_1B):
    """repeticiones muestras de n datos de la reciproca: lista de (x, y)."""
    grande = _ml().PROCESOS["inverso"](n=n * repeticiones, semilla=semilla,
                                       fracciones=(1, 0, 0), con_realidad=False).ent
    x, y = grande["x"].to_numpy(float), grande["y"].to_numpy(float)
    return [(x[i * n:(i + 1) * n], y[i * n:(i + 1) * n]) for i in range(repeticiones)]


def ajuste_rapido(x, y, N):
    """El ajuste de ml.ajustar(phi=polinomio(N)) en forma cerrada: devuelve
    (prediccion, L_ent) con prediccion(x_nuevo) -> y_gorro."""
    lo, hi = float(np.min(x)), float(np.max(x))
    escalar = lambda v: 2 * (np.asarray(v, float) - lo) / (hi - lo) - 1  # noqa: E731
    M = np.vander(escalar(x), N + 1, increasing=True)
    beta = np.linalg.lstsq(M, y, rcond=None)[0]
    prediccion = lambda v: np.vander(escalar(v), N + 1, increasing=True) @ beta  # noqa: E731
    return prediccion, float(np.mean((y - M @ beta) ** 2))


def riesgo_inverso(prediccion):
    """R = E_x[(f - f_gorro)²] + sigma², x uniforme en [0.3, 3] (cuadratura)."""
    return float(np.sum(PESOS_R * (f_inverso(MALLA_R) - prediccion(MALLA_R)) ** 2)
                 + INVERSO_SIGMA2)


GRADO_OPTIMISMO = 4
REPETICIONES_OPTIMISMO = 500


def cifras_c1_optimismo(repeticiones=REPETICIONES_OPTIMISMO, semilla=SEMILLA_1B):
    """P2 §4 (cifra que ilustra el teorema del optimismo): en 500 muestras de
    20 datos de la reciproca, con polinomios de grado 4. beta fijo = el ajuste
    de grado 4 a otra muestra (100 000 datos, semilla 1000), elegido antes de
    ver ninguna de las 500: la media de L_ent(beta) coincide con R(beta). Con
    beta_gorro de cada muestra, la media de L_ent queda abajo de la de R."""
    fija = trozos_inverso(1, n=100_000, semilla=1000)[0]
    pred_fija, _ = ajuste_rapido(*fija, GRADO_OPTIMISMO)
    R_fijo = riesgo_inverso(pred_fija)
    L_fijo, L_gorro, R_gorro = [], [], []
    for x, y in trozos_inverso(repeticiones, semilla=semilla):
        L_fijo.append(float(np.mean((y - pred_fija(x)) ** 2)))
        pred, L = ajuste_rapido(x, y, GRADO_OPTIMISMO)
        L_gorro.append(L)
        R_gorro.append(riesgo_inverso(pred))
    return {"repeticiones": repeticiones, "grado": GRADO_OPTIMISMO, "R_fijo": R_fijo,
            "media_L_ent_fijo": float(np.mean(L_fijo)),
            "media_L_ent_gorro": float(np.mean(L_gorro)),
            "media_R_gorro": float(np.mean(R_gorro)),
            "muestras_al_reves": int(np.sum(np.array(L_gorro) > np.array(R_gorro)))}


REPETICIONES_ELEGIR = 200


def elecciones(repeticiones=REPETICIONES_ELEGIR, N_max=N_MAX, semilla=SEMILLA_1B):
    """La tabla de NB02 bloque 3 y de ml-c1-elegir-con-entrenamiento: por
    muestra, el N que elige L_ent y el de menor R (N = 1..N_max)."""
    trozos = trozos_inverso(repeticiones, semilla=semilla)

    def experimento(s):
        x, y = trozos[s - semilla]
        L, R = [], []
        for N in range(1, N_max + 1):
            pred, l = ajuste_rapido(x, y, N)
            L.append(l)
            R.append(riesgo_inverso(pred))
        return {"N_ent": int(np.argmin(L)) + 1, "N_R": int(np.argmin(R)) + 1}

    return _ml().repetir(experimento, repeticiones=repeticiones, semilla=semilla)


def cifras_c1_elegir(semilla=SEMILLA_1B):
    """P2 §5 y cierre: en 200 muestras de 20 datos, cuantas veces L_ent
    elige N_max = 15, y el reparto del N de menor R."""
    tabla = elecciones(semilla=semilla)
    reparto = {int(k): int(v) for k, v in tabla["N_R"].value_counts().sort_index().items()}
    return {"tabla": tabla, "repeticiones": len(tabla), "N_max": N_MAX,
            "veces_N_max_ent": int((tabla["N_ent"] == N_MAX).sum()),
            "reparto_N_R": reparto,
            "veces_N_R_3_a_6": int(tabla["N_R"].between(3, 6).sum()),
            "moda_N_R": int(tabla["N_R"].mode().iloc[0])}


INVERSO_N = 60
INVERSO_GRADOS = (1, 4, 10)
# Tope del eje y del panel de arriba de ml-c1-inverso-vs-potencias (y de NB02
# bloque 4): los datos que quedan arriba se marcan con un triangulo y se nombran.
INVERSO_YTOPE = 40


def cifras_c1_inverso(n=INVERSO_N, semilla=SEMILLA_1B):
    """P2 §6 y cierre, figura ml-c1-inverso-vs-potencias, NB02 bloque 4: el
    caso 3 (2 + 5/x con x ~ U(0.05, 3)) con 60 datos. R (despliegue) de los
    polinomios de grado 1, 4 y 10 y de phi = (1, 1/x); beta_gorro de (1, 1/x);
    el piso y el benchmark. Tambien el caso 4: L_ent de N = 10 y 25 sin
    escalar y con escalar."""
    import warnings
    ml = _ml()
    datos = ml.caso(3, n=n, semilla=semilla)
    salida = {"n": n}
    for N in INVERSO_GRADOS:
        salida[f"R_{N}"] = float(ml.riesgo(ml.ajustar(datos, phi=ml.polinomio(N)), datos))
    m = ml.ajustar(datos, phi=ml.columnas("1/x"))
    salida["R_inverso"] = float(ml.riesgo(m, datos))
    salida["beta_inverso"] = (float(m.beta_gorro["1"]), float(m.beta_gorro["1/x"]))
    salida["mejor_polinomio_R"] = min(
        float(ml.riesgo(ml.ajustar(datos, phi=ml.polinomio(N)), datos)) for N in range(1, 11))
    salida["piso"] = float(ml.piso(datos))
    salida["fuera_del_cuadro"] = sorted(float(v) for v in datos.ent.y
                                        if v > INVERSO_YTOPE)
    salida["benchmark"] = float(ml.benchmarks(datos, datos.despliegue)
                                .loc["media", "cuadratica"])
    d4 = ml.caso(4, semilla=semilla)
    cuatro = {}
    for N in (10, 25):
        for escalar in (False, True):
            with warnings.catch_warnings(record=True) as avisos:
                warnings.simplefilter("always")
                m4 = ml.ajustar(d4, phi=ml.polinomio(N, escalar=escalar))
            cuatro[(N, escalar)] = {"L_ent": float(ml.L(m4, d4.ent)),
                                    "avisos": [str(a.message) for a in avisos]}
    salida["caso_4"] = cuatro
    # NB02 bloque 4 pide llevar el grado a 40 (escalado): su R y su L_ent.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")   # grados altos: avisos de condicionamiento
        m40 = ml.ajustar(datos, phi=ml.polinomio(40))
        ajustes = {N: ml.ajustar(datos, phi=ml.polinomio(N)) for N in range(25, 41)}
    salida["R_40"] = float(ml.riesgo(m40, datos))
    salida["L_ent_40"] = float(ml.L(m40, datos.ent))
    # NB02 bloque 4 con «escalar x» apagado (revision r2 del tramo 1b): L_ent
    # sube aunque la familia es la misma, y el mayor coeficiente NO es la
    # alarma: con escala, los de grado alto tambien son enormes (sobreajuste);
    # sin escalar, el calculo cae a la pseudoinversa y los deja pequenos.
    escala = {}
    for N in (15, 25, 40):
        for escalar in (True, False):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                mN = ml.ajustar(datos, phi=ml.polinomio(N, escalar=escalar))
            escala[(N, escalar)] = {"L_ent": float(ml.L(mN, datos.ent)),
                                    "coef_max": float(mN.beta_gorro.abs().max())}
    salida["escalar_contra_no"] = escala
    # Escalar no garantiza la monotonia numerica: el primer grado (de 25 a 40)
    # donde L_ent escalado sube respecto al anterior, con los dos valores.
    previo = None
    for N in range(25, 41):
        L = float(ml.L(ajustes[N], datos.ent))
        if previo is not None and L > previo[1]:
            salida["sube_escalado"] = {"de": previo[0], "a": N, "L_de": previo[1], "L_a": L}
            break
        previo = (N, L)
    return salida


def cifras_c1_columnas():
    """P2 §6, micro ml-c1-ej-columnas: monomios de grado a lo mas 3 en J
    variables, binom(J + 3, 3)."""
    return {5: math.comb(5 + 3, 3), 20: math.comb(20 + 3, 3)}


EXTRAPOLAR_GRADO = 7
EXTRAPOLAR_ZONAS = {
    "entregas": {"dentro": (0.0, 6.0), "fuera": (6.0, 9.0)},
    "seno": {"dentro": (0.0, 2.0), "fuera": (2.0, 3.0)},
}


def datos_extrapolar(panel, semilla=SEMILLA_1B):
    ml = _ml()
    if panel == "entregas":
        return ml.PROCESOS["entregas"](semilla=semilla, fracciones=(1, 0, 0))
    if panel == "seno":
        return ml.caso(5, semilla=semilla)
    return ml.PROCESOS["recursivo"](semilla=semilla)


def phi_recursivo(con_anterior):
    """El panel recursivo: la recta en x, con o sin el tiempo anterior."""
    ml = _ml()
    return ml.columnas("x", "y_anterior") if con_anterior else ml.columnas("x")


def cifras_c1_extrapolar(semilla=SEMILLA_1B):
    """P2 §7, figura ml-c1-extrapolar: error_por_zona (riesgo si el uso cayera
    uniforme en la zona; el despliegue no cambia) dentro y fuera de la zona de
    datos para el polinomio de grado 7 (entregas y seno) y para la recta de
    las entregas; en el recursivo (x creciente en el tiempo), L en el tramo
    de entrenamiento (realidad, t < n) y R a un paso en el futuro
    (despliegue, t >= n) de la recta en x, sin y con el tiempo anterior.
    «dentro» y «futuro» promedian series nuevas del proceso (realidad y
    despliegue); «serie_dibujada» es L_ent sobre los 60 pasos observados."""
    ml = _ml()
    salida = {}
    for panel, zonas in EXTRAPOLAR_ZONAS.items():
        datos = datos_extrapolar(panel, semilla)
        modelos = {"grado_7": ml.ajustar(datos, phi=ml.polinomio(EXTRAPOLAR_GRADO))}
        if panel == "entregas":
            modelos["recta"] = ml.ajustar(datos)
        salida[panel] = {
            nombre: {fila.zona: float(fila.R_zona)
                     for fila in ml.error_por_zona(m, datos, zonas).itertuples()}
            for nombre, m in modelos.items()}
        salida[panel]["piso"] = float(ml.piso(datos))
    datos = datos_extrapolar("recursivo", semilla)
    rec = {"n": len(datos.ent), "futuro": len(datos.prueba), "piso": float(ml.piso(datos))}
    for nombre, con in (("sin_anterior", False), ("con_anterior", True)):
        m = ml.ajustar(datos, phi=phi_recursivo(con))
        rec[nombre] = {"dentro": float(ml.L(m, datos.realidad)),
                       "futuro": float(ml.riesgo(m, datos)),
                       "serie_dibujada": float(ml.L(m, datos.ent))}
    salida["recursivo"] = rec
    return salida


NFL_ENTRENAMIENTO = (0, 3, 5, 6)   # 000, 011, 101, 110


def cifras_c1_no_free_lunch():
    """P2 §8 y cierre, figura ml-c1-no-free-lunch: las 256 funciones de 3 bits
    con entrenamiento 000, 011, 101, 110; promedio exacto por regla (sobre
    funciones), media por rugosidad, «siempre 1» en cada grupo, tamanos de
    los grupos y el desempate de la mayoria (2-2 -> 1)."""
    ml = _ml()
    tabla = ml.no_free_lunch(entrenamiento=NFL_ENTRENAMIENTO)
    salida = {"funciones": int(tabla["funcion"].nunique()),
              "entrenamiento": tuple(format(i, "03b") for i in NFL_ENTRENAMIENTO),
              "tamanos": {int(k): int(v) // 3 for k, v in
                          tabla["rugosidad"].value_counts().sort_index().items()}}
    for regla, trozo in tabla.groupby("regla", sort=False):
        salida[regla] = {
            "promedio": sum(trozo["aciertos_fuera"], Fraction(0)) / len(trozo),
            "por_rugosidad": {int(r): sum(g, Fraction(0)) / len(g)
                              for r, g in trozo.groupby("rugosidad")["aciertos_fuera"]}}
    # Desempate: con entrenamiento 1, 1, 0, 0 la mayoria predice 1 en todo lo no visto.
    f_empate = 0b00001001   # unos en 000 y 011; ceros en 101 y 110 (y fuera)
    fila = tabla[(tabla.funcion == f_empate) & (tabla.regla == "mayoria")].iloc[0]
    salida["desempate_mayoria"] = {"funcion": f_empate,
                                   "aciertos_fuera": fila["aciertos_fuera"]}
    # El vecino: cada entrada no vista esta a distancia de Hamming 1 de tres
    # de entrenamiento (empate triple) y ml_lab desempata por el indice menor.
    ent = list(NFL_ENTRENAMIENTO)
    dist = lambda a, b: bin(a ^ b).count("1")  # noqa: E731
    fuera = [i for i in range(8) if i not in ent]
    salida["fuera"] = tuple(format(i, "03b") for i in fuera)
    salida["vecinos_empatados"] = {
        format(i, "03b"): tuple(format(j, "03b") for j in ent if dist(i, j) == 1)
        for i in fuera}
    salida["vecino_elegido"] = {
        format(i, "03b"): format(min(ent, key=lambda j: (dist(i, j), j)), "03b")
        for i in fuera}
    return salida


def cifras_c1_nb02_parte_b(semilla=SEMILLA_1B):
    """NB02, celda bloque-6-prueba (parte B de no free lunch): R (despliegue)
    del polinomio de grado 3 y de vecinos (3) en un proceso suave y en uno
    periodico, 60 datos cada uno. Misma construccion que la celda."""
    ml = _ml()
    curvas = {"suave": (lambda d: 10 + 4 * d.x - 0.3 * d.x ** 2, 1.0),
              "periódico": (lambda d: 4 + 2 * np.sin(5 * d.x), 0.3)}
    salida = {}
    for nombre, (f, sigma) in curvas.items():
        datos = ml.proceso(n=60, x={"x": ml.uniforme(0, 6)}, f=f, semilla=semilla,
                           ruido=ml.normal(0, sigma), fracciones=(1, 0, 0))
        polinomio = ml.ajustar(datos, phi=ml.polinomio(3))
        vecinos = ml.ajustar_otro(datos, familia="vecinos", n_vecinos=3)
        salida[nombre] = {"polinomio": float(ml.riesgo(polinomio, datos)),
                          "vecinos": float(ml.riesgo(vecinos, datos))}
    return salida


def cifras_c1_par_impar():
    """P2, ejercicio final: en x = 1..8, y = 5 si x es par y 0 si es impar.
    El polinomio de grado 7 que pasa por los 8 (Lagrange con fracciones
    exactas) en x = 9 y 10, y la phi periodica (1, cos pi x): 2.5 + 2.5 cos pi x."""
    xs = list(range(1, 9))
    ys = [Fraction(5) if x % 2 == 0 else Fraction(0) for x in xs]

    def lagrange(v):
        total = Fraction(0)
        for i, (xi, yi) in enumerate(zip(xs, ys)):
            termino = yi
            for j, xj in enumerate(xs):
                if j != i:
                    termino *= Fraction(v - xj, xi - xj)
            total += termino
        return total

    periodica = {x: 2.5 + 2.5 * math.cos(math.pi * x) for x in range(1, 11)}
    return {"grado_7": {9: lagrange(9), 10: lagrange(10)},
            "interpola": all(lagrange(x) == y for x, y in zip(xs, ys)),
            "periodica": {x: round(v, 12) for x, v in periodica.items()},
            "beta_periodica": (2.5, 2.5)}

# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---
