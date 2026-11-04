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

import numpy as np


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
        fila["L_ent_recta"] = float(ml.L(modelos_piso(datos)["recta ajustada"], datos.ent))
        salida[s] = fila
    return salida


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
    }


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

# --- fin tramo 1a ---


# --- tramo 1b ---
# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---
