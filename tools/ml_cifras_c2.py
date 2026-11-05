"""Cifras de la clase 2 de la unidad de aprendizaje de maquina (unidad 9).

Una funcion por hecho que cita una pagina, un notebook o una figura de la
clase 2 (clase_2.md §10.7, tabla «tools/ml_cifras_c2.py»). Ninguna cifra de la
clase se escribe a mano: la pagina la copia de aqui, tools/test_ml_cifras_c2.py
la fija en la fuente y tools/test_ml_prosa_c2.py la busca en la seccion de la
pagina que la cita (D-009.5, D-003).

Las funciones que calculan con ml_lab lo importan de tools/ (nunca de
_assets/, D-004) y solo dentro de la funcion (contrato v3 §5.2, r1-40). Cada
una se memoriza: la prueba, la figura y el brief leen el mismo diccionario.

Decisiones de ejecucion (bitacora/prog-c2.md, DECISION prog-c2-2):
- El hilo es PROCESOS["entregas_curvas"](n=60, semilla=0): 36 de
  entrenamiento, 12 de validacion y 12 de prueba (60/20/20), candidatos
  polinomio(N) con N = 0..12 (escalados a [-1, 1], §5.6).
- Las fabricas de los experimentos repetidos usan n_realidad=N_REALIDAD
  (2000): con la muestra enorme de 100 000, una repeticion de
  optimismo_por_seleccion tarda 0.7 s y el bloque 03·3 no cabe en 10 s.
  El error de Monte Carlo de R con 2000 observaciones es chico frente a las
  diferencias que se citan; la figura y el notebook usan la misma fabrica.
- Las repeticiones citadas son las del notebook (§10.12).

Anclas por tramo (protocolo p5.2 §7.1): este modulo se escribe completo en
C2.T2 (las cifras de las tres paginas); las anclas marcan que pagina cita
cada funcion.
"""
import importlib
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np
import pandas as pd


def _ml():
    """tools/aprendizaje_maquina.py (ml_lab), importado al pedirlo."""
    return importlib.import_module("aprendizaje_maquina")


SEMILLA = 0                 # semilla maestra
N_HILO = 60                 # entregas del hilo (36/12/12)
CANDIDATOS = tuple(range(13))
N_REALIDAD = 2000           # muestra enorme de las fabricas repetidas
REP_OPTIMISMO = 300         # 03·3 y ml-c2-optimismo (con 100, el sesgo con prueba queda a 2.5 EE)
REP_PRUEBAS = 500           # 03·2 y ml-c2-prueba-ruidosa (sin reajustar: instantaneo)
REP_REPARTO = 100           # 03·5 y ml-c2-reparto
FRACCIONES_REPARTO = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5)
N_REPARTO = 60
REP_CV_VS_VAL = 200         # 04·3
REP_ANIDADA = 30            # 04·6
CANDIDATOS_ANIDADA = tuple(range(9))
REP_SV = 100                # 05·1–2, ml-c2-abanico, ml-c2-diana
X0 = 5.0                    # el punto de la diana
UMBRAL_MIN = 5.0            # minutos: «error grande» en 04·4
N_MODELO_FIJO = 4           # el modelo congelado de 03·2 y del reparto
CONTRATOS = ("más de lo mismo", "el mes que viene", "pacientes nuevos", "otra ciudad")
# Caso 14: 48 pacientes (5 entregas cada uno) en vez de 24. Con 24, la prueba
# por grupos tiene 5 pacientes y su varianza entre pacientes la saca del 30 %
# de R con la semilla maestra (33.6 contra 18.8, CAMBIO prog-lab-9). Se cambia
# el proceso, no la semilla (§10.4, paso 3): CAMBIO prog-c2-3.
CAMBIOS_CASO_14 = {"n_grupos": 48}


def _deriva_otra_ciudad(t):
    # Caso 15: la otra ciudad con x en 4–10 km (no 4–9). Con 4–9, el elegido
    # por CV da R/L_prueba = 2.8 < 3 con la semilla maestra. CAMBIO prog-c2-3.
    return {"x": _ml().uniforme(4, 10)}


def construir(N):
    """El candidato de grado N: ajustar(df, phi=polinomio(N)) (escalado a [-1, 1])."""
    ml = _ml()
    return lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N))


def candidatos(ns=CANDIDATOS):
    return {N: construir(N) for N in ns}


@lru_cache(maxsize=None)
def hilo(semilla=SEMILLA, n=N_HILO):
    """El proceso hilo de la clase: entregas_curvas con 60 entregas (36/12/12)."""
    return _ml().PROCESOS["entregas_curvas"](n=n, semilla=semilla)


def fabrica(s, n=N_HILO):
    """fabrica(semilla) de los experimentos repetidos (muestra enorme de 2000)."""
    return _ml().PROCESOS["entregas_curvas"](n=n, semilla=int(s), n_realidad=N_REALIDAD)


def _silencio():
    import warnings
    w = warnings.catch_warnings()
    w.__enter__()
    warnings.simplefilter("ignore")
    return w


def _media_ee(v):
    v = np.asarray(v, float)
    return float(v.mean()), float(v.std(ddof=1) / math.sqrt(len(v)))


# ===================================================================
# --- tramo rapido ---  (paginas 1 y 2, notebooks 03 y 04, tarea)
# ===================================================================

@lru_cache(maxsize=None)
def cifras_c2_entrenamiento_elige():
    """P1 §1 y 03·1: el grado que elige L_ent entre 0 y 12 y L_ent en 0, 3, 12."""
    ml, w = _ml(), _silencio()
    try:
        d = hilo()
        s = ml.elegir(d, candidatos(), con="ent")
        L_ent = {N: float(ml.L(construir(N)(d), d.ent)) for N in CANDIDATOS}
    finally:
        w.__exit__(None, None, None)
    return {"elegido": int(s.elegido), "L_ent": L_ent,
            "L_ent_0": L_ent[0], "L_ent_3": L_ent[3], "L_ent_12": L_ent[12]}


@lru_cache(maxsize=None)
def cifras_c2_ajustes_con_prueba():
    """P1 §2 y ml-c2-ajustes-con-prueba: L_ent, L_prueba y R de los grados 1, 4, 12
    ajustados con entrenamiento."""
    ml, w = _ml(), _silencio()
    try:
        d = hilo()
        res = {}
        for N in (1, 4, 12):
            m = construir(N)(d)
            res[N] = {"L_ent": float(ml.L(m, d.ent)), "L_prueba": float(ml.L(m, d.prueba)),
                      "R": float(ml.riesgo(m, d))}
    finally:
        w.__exit__(None, None, None)
    return res


@lru_cache(maxsize=None)
def cifras_c2_prueba_ruidosa():
    """P1 §3, 03·2 y ml-c2-prueba-ruidosa: el modelo de grado 4 congelado; 500
    pruebas nuevas de 20 y de 200 sacadas del despliegue (100 000)."""
    ml, w = _ml(), _silencio()
    try:
        d = hilo()
        m = construir(N_MODELO_FIJO)(d)
        perd = np.asarray(ml.perdida(d.despliegue["y"], m.predecir(d.despliegue)), float)
    finally:
        w.__exit__(None, None, None)
    R = float(perd.mean())
    res = {"R": R, "estimaciones": {}}
    for n in (20, 200):
        # un generador nuevo por tamano: la misma receta que bloque_2 del
        # notebook 03, que lo reinicia en cada llamada (revision r1: con uno
        # compartido, la cifra de 200 del guion no era la que imprime el notebook)
        rng = np.random.default_rng(SEMILLA)
        L, cubre = [], []
        for _ in range(REP_PRUEBAS):
            l = perd[rng.choice(len(perd), size=n, replace=False)]
            ee = l.std(ddof=1) / math.sqrt(n)
            L.append(l.mean())
            cubre.append(abs(l.mean() - R) <= 2 * ee)
        L = np.array(L)
        res["estimaciones"][n] = L
        res[f"desv_{n}"] = float(L.std(ddof=1))
        res[f"media_{n}"] = float(L.mean())
        res[f"cobertura_{n}"] = float(np.mean(cubre))
    res["cociente_desv"] = res["desv_20"] / res["desv_200"]
    return res


@lru_cache(maxsize=None)
def tabla_optimismo():
    """El formato largo de optimismo_por_seleccion (100 repeticiones, 13 grados)."""
    ml, w = _ml(), _silencio()
    try:
        return ml.optimismo_por_seleccion(fabrica, candidatos(), repeticiones=REP_OPTIMISMO,
                                          semilla=SEMILLA, detalle=True)
    finally:
        w.__exit__(None, None, None)


def _elegidos(largo, columna, M=13):
    """Por repeticion, la fila del candidato de menor `columna` entre 0..M-1
    (empate: el menor N, que es el primero tras ordenar)."""
    t = largo[largo["candidato"] < M].sort_values(["repeticion", "candidato"])
    idx = t.groupby("repeticion")[columna].idxmin()
    return t.loc[idx]


@lru_cache(maxsize=None)
def cifras_c2_optimismo():
    """P1 §4, 03·3 y ml-c2-optimismo: anunciado − real del elegido SIN reajuste,
    eligiendo con la prueba y con validacion; la cadena observada de medias
    (elegido por validacion); el modelo final reajustado aparte; y el engaño
    medio por numero de candidatos M (ejercicio-optimismo-m)."""
    largo = tabla_optimismo()
    con_p = _elegidos(largo, "L_prueba")
    con_v = _elegidos(largo, "L_val")
    dp = (con_p["L_prueba"] - con_p["R"]).to_numpy()
    dv = (con_v["L_prueba"] - con_v["R"]).to_numpy()
    res = {"repeticiones": int(largo["repeticion"].nunique()),
           "anunciado_menos_real": {"prueba": dp, "validacion": dv}}
    res["sesgo_prueba"], res["ee_prueba"] = _media_ee(dp)
    res["sesgo_validacion"], res["ee_validacion"] = _media_ee(dv)
    # Medianas, descriptivas: con validacion la media la arrastran unas pocas
    # repeticiones en que gana un grado alto que explota en los bordes (R enorme).
    res["mediana_prueba"] = float(np.median(dp))
    res["mediana_validacion"] = float(np.median(dv))
    res["optimistas_prueba"] = float(np.mean(dp < 0))
    res["optimistas_validacion"] = float(np.mean(dv < 0))
    for col in ("L_ent", "L_val", "L_prueba", "R"):
        res[f"media_{col}"], res[f"ee_{col}"] = _media_ee(con_v[col])
    d1 = (con_v["L_val"] - con_v["L_ent"]).to_numpy()
    d2 = (con_v["L_prueba"] - con_v["L_val"]).to_numpy()
    res["val_menos_ent"], res["ee_val_menos_ent"] = _media_ee(d1)
    res["prueba_menos_val"], res["ee_prueba_menos_val"] = _media_ee(d2)
    fin = (con_v["L_prueba_final"] - con_v["R_final"]).to_numpy()
    res["R_final"], res["ee_R_final"] = _media_ee(con_v["R_final"])
    res["final_prueba_menos_R"], res["ee_final_prueba_menos_R"] = _media_ee(fin)
    res["sesgo_prueba_por_M"] = {
        M: float((lambda e: (e["L_prueba"] - e["R"]).mean())(_elegidos(largo, "L_prueba", M)))
        for M in range(1, 14)}
    return res


def _modelo_cv(d, M=9):
    s = _ml().elegir(d, candidatos(range(M)), con="cv")
    return s


@lru_cache(maxsize=None)
def datos_contrato(contrato, separacion):
    """Datos de cada contrato con la separacion «azar» o la que lo imita."""
    ml = _ml()
    if contrato == "más de lo mismo":
        return ml.PROCESOS["entregas_curvas"](n=240, semilla=SEMILLA)
    if contrato == "el mes que viene":
        return ml.caso(13, separar="azar" if separacion == "azar" else "tiempo")
    if contrato == "pacientes nuevos":
        return ml.caso(14, separar="azar" if separacion == "azar" else "grupo",
                       **CAMBIOS_CASO_14)
    if contrato == "otra ciudad":
        return ml.caso(15, deriva=_deriva_otra_ciudad)
    raise ValueError(contrato)


def modelo_contrato(contrato, d):
    """El modelo de cada contrato, fijado antes de mirar la prueba (§10.4):
    grado elegido por CV (0..8) en «más de lo mismo» y «otra ciudad»; vecinos
    en (x, t) en el caso 13; polinomio de grado 3 más un efecto por paciente
    (codificacion por efectos) en el caso 14."""
    ml = _ml()
    if contrato == "el mes que viene":
        return ml.ajustar_otro(d, familia="vecinos", columnas_x=["x", "t"], n_vecinos=5)
    if contrato == "pacientes nuevos":
        return ml.ajustar(d, phi=ml.combinar(ml.polinomio(3),
                                             ml.dummies("grupo", codificacion="efectos")))
    return _modelo_cv(d).modelo


def _medir_contrato(contrato, separacion):
    ml = _ml()
    d = datos_contrato(contrato, separacion)
    m = modelo_contrato(contrato, d)
    l = np.asarray(ml.perdida(d.prueba["y"], m.predecir(d.prueba)), float)
    return {"L_prueba": float(l.mean()), "ee": float(l.std(ddof=1) / math.sqrt(len(l))),
            "R": float(ml.riesgo(m, d)),
            "benchmark": float(ml.benchmarks(d, d.despliegue).loc["media"].iloc[0])}


@lru_cache(maxsize=None)
def cifras_c2_imitar():
    """P1 §5, 03·4 y ml-c2-prueba-miente: por contrato, L_prueba al azar, con la
    separacion que imita (tiempo, grupo; en «otra ciudad» no hay), R en el
    despliegue de ese contrato y el benchmark (media de ent evaluada en ese
    despliegue). Mas los criterios de §10.4 (casos 13–15) con la semantica de
    despliegue="futuro" de contrato v5 §5.5."""
    ml, w = _ml(), _silencio()
    try:
        res = {}
        for c in CONTRATOS:
            res[c] = {"azar": _medir_contrato(c, "azar")}
            if c in ("el mes que viene", "pacientes nuevos"):
                res[c]["imita"] = _medir_contrato(c, "imita")
        # D-009.6: el modelo lineal en x (sin t) no miente en el caso 13
        d = datos_contrato("el mes que viene", "azar")
        lin = ml.ajustar(d)
        res["el mes que viene"]["lineal_x"] = {"L_prueba": float(ml.L(lin, d.prueba)),
                                               "R": float(ml.riesgo(lin, d))}
        # grado elegido por CV en «más de lo mismo» y «otra ciudad»
        res["más de lo mismo"]["grado"] = int(
            _modelo_cv(datos_contrato("más de lo mismo", "azar")).elegido)
        res["otra ciudad"]["grado"] = int(_modelo_cv(datos_contrato("otra ciudad", "azar")).elegido)
        # invariancia del caso 14: R no depende del orden de las categorias
        res["pacientes nuevos"]["R_permutado"] = _R_caso14_permutado()
    finally:
        w.__exit__(None, None, None)
    a13, t13 = res["el mes que viene"]["azar"], res["el mes que viene"]["imita"]
    a14, g14 = res["pacientes nuevos"]["azar"], res["pacientes nuevos"]["imita"]
    a15 = res["otra ciudad"]["azar"]
    l13 = res["el mes que viene"]["lineal_x"]
    res["criterios"] = {
        "c13_R_sobre_azar": a13["R"] / a13["L_prueba"],
        "c13_tiempo_rel": abs(t13["L_prueba"] - t13["R"]) / t13["R"],
        "c13_cierra": (t13["R"] - t13["L_prueba"]) / (a13["R"] - a13["L_prueba"]),
        "c13_lineal_rel": abs(l13["L_prueba"] - l13["R"]) / l13["R"],
        "c14_R_sobre_azar": a14["R"] / a14["L_prueba"],
        "c14_grupo_rel": abs(g14["L_prueba"] - g14["R"]) / g14["R"],
        "c15_R_sobre_prueba": a15["R"] / a15["L_prueba"],
    }
    return res


def _R_caso14_permutado():
    """R del modelo del caso 14 con las categorias de grupo renombradas al reves
    (el grupo g pasa a ser G-1-g) en entrenamiento: con la codificacion por
    efectos, la fila de ceros es el grupo promedio y R no cambia."""
    ml = _ml()
    d = datos_contrato("pacientes nuevos", "azar")
    G = int(d.ent["grupo"].max()) + 1
    ent = d.ent.copy()
    ent["grupo"] = G - 1 - ent["grupo"]
    ent.attrs = d.ent.attrs
    m = ml.ajustar(ent, phi=ml.combinar(ml.polinomio(3),
                                        ml.dummies("grupo", codificacion="efectos")))
    l = ml.perdida(d.despliegue["y"], m.predecir(d.despliegue))
    return float(np.mean(l))


@lru_cache(maxsize=None)
def tabla_reparto(n_total=N_REPARTO):
    ml, w = _ml(), _silencio()
    try:
        return ml.reparto(lambda s: fabrica(s, n=n_total), construir(N_MODELO_FIJO),
                          fracciones_prueba=FRACCIONES_REPARTO, repeticiones=REP_REPARTO,
                          semilla=SEMILLA)
    finally:
        w.__exit__(None, None, None)


@lru_cache(maxsize=None)
def cifras_c2_reparto():
    """P1 §6, 03·5 y ml-c2-reparto: R medio y desviacion de L_prueba − R con
    10, 20 y 50 % de prueba (n = 60, grado 4, 100 repeticiones), con su EE de
    Monte Carlo (de la media; de la desviacion, desv/√(2(r−1)))."""
    t = tabla_reparto()
    res = {}
    for f in (0.1, 0.2, 0.5):
        g = t[np.isclose(t["fraccion"], f)]
        r = len(g)
        R, eeR = _media_ee(g["R"])
        sd = float(g["error"].std(ddof=1))
        res[f] = {"R": R, "ee_R": eeR, "desv_error": sd, "ee_desv": sd / math.sqrt(2 * (r - 1))}
    return res


@lru_cache(maxsize=None)
def seleccion_hilo(regla="un_ee", k=5):
    ml, w = _ml(), _silencio()
    try:
        return ml.elegir(hilo(), candidatos(), con="cv", k=k, regla=regla,
                         orden_complejidad=list(CANDIDATOS))
    finally:
        w.__exit__(None, None, None)


@lru_cache(maxsize=None)
def cifras_c2_hilo():
    """P2 §2–§3, 04·2 y ml-c2-cv-capacidad: N̂ por el minimo y por un EE, sus CV₅ ± EE,
    R y L_prueba ± 2 EE del modelo final; el benchmark (media de ent) en prueba
    y en el despliegue; las curvas que dibuja la figura."""
    ml, w = _ml(), _silencio()
    try:
        d = hilo()
        s = seleccion_hilo()
        tabla = s.tabla.set_index("candidato")
        res = {"N_min": int(s.elegido), "N_un_ee": int(s.elegido_un_ee),
               "cv": {N: float(tabla.loc[N, "valor"]) for N in CANDIDATOS},
               "ee": {N: float(tabla.loc[N, "ee"]) for N in CANDIDATOS},
               "costo_ajustes": int(s.costo_ajustes)}
        res["umbral"] = res["cv"][res["N_min"]] + res["ee"][res["N_min"]]
        des = ml._desarrollo(d)
        res["R_por_N"] = {N: float(ml.riesgo(construir(N)(des), d)) for N in CANDIDATOS}
        # L_ent del MISMO ajuste que R (el reajuste con las 48 de desarrollo), para
        # que R − L_ent sea la brecha de un solo modelo (revision r1: antes era
        # el ajuste con 36 y la diferencia mezclaba dos modelos)
        res["L_ent_por_N"] = {N: float(ml.L(construir(N)(des), des)) for N in CANDIDATOS}
        for nombre, N in (("min", res["N_min"]), ("un_ee", res["N_un_ee"])):
            m = construir(N)(des)
            l = np.asarray(ml.perdida(d.prueba["y"], m.predecir(d.prueba)), float)
            res[f"R_{nombre}"] = float(ml.riesgo(m, d))
            res[f"L_prueba_{nombre}"] = float(l.mean())
            res[f"ee_prueba_{nombre}"] = float(l.std(ddof=1) / math.sqrt(len(l)))
        media = float(d.ent["y"].mean())
        lb = (d.prueba["y"].to_numpy(float) - media) ** 2
        res["benchmark_prueba"] = float(lb.mean())
        res["ee_benchmark_prueba"] = float(lb.std(ddof=1) / math.sqrt(len(lb)))
        res["benchmark_despliegue"] = float(
            ml.benchmarks(d, d.despliegue).loc["media"].iloc[0])
        # Revision r1: la diferencia pareada en prueba (final − benchmark), que el
        # cuerpo de P2 §3 lee: no le gana; una entrega del borde domina la cifra.
        lm = np.asarray(ml.perdida(d.prueba["y"], construir(res["N_un_ee"])(des)
                                   .predecir(d.prueba)), float)
        dif = lm - lb
        res["dif_prueba"] = float(dif.mean())
        res["ee_dif_prueba"] = float(dif.std(ddof=1) / math.sqrt(len(dif)))
        res["n_prueba"] = int(len(dif))
        res["perdida_max_prueba"] = float(lm.max())
        res["piso"] = float(ml.piso(d))
        res["N_mejor_R"] = int(min(CANDIDATOS, key=lambda N: res["R_por_N"][N]))
    finally:
        w.__exit__(None, None, None)
    return res


@lru_cache(maxsize=None)
def cifras_c2_cv_vs_val():
    """P2 §3 (ml-c2-obs-ee-de-cv) y 04·3: en 200 muestras del hilo, L_val (12
    entregas) y CV₅ (48) del grado 4; su desviacion real, el EE medio que
    reporta cada uno y la media de R (E_D[R], modelo ajustado con ent)."""
    ml, w = _ml(), _silencio()
    try:
        def una(s):
            d = fabrica(s)
            m = construir(N_MODELO_FIJO)(d)
            lv = np.asarray(ml.perdida(d.val["y"], m.predecir(d.val)), float)
            cv = ml.validacion_cruzada(d, construir(N_MODELO_FIJO), k=5)
            return {"L_val": lv.mean(), "ee_val": lv.std(ddof=1) / math.sqrt(len(lv)),
                    "cv": cv.media, "ee_cv": cv.ee, "R": ml.riesgo(m, d)}
        t = ml.repetir(una, repeticiones=REP_CV_VS_VAL, semilla=SEMILLA)
    finally:
        w.__exit__(None, None, None)
    return {"tabla": t, "desv_val": float(t["L_val"].std(ddof=1)),
            "desv_cv": float(t["cv"].std(ddof=1)), "ee_val_medio": float(t["ee_val"].mean()),
            "ee_cv_medio": float(t["ee_cv"].mean()), "media_R": float(t["R"].mean()),
            "ajustes_val": 1, "ajustes_cv": 5}


def _var_residual(y, yg):
    r = np.asarray(y, float) - np.asarray(yg, float)
    return float(np.var(r, ddof=1)) if len(r) > 1 else float("nan")


def _prop_grandes(y, yg):
    return float(np.mean(np.abs(np.asarray(y, float) - np.asarray(yg, float)) > UMBRAL_MIN))


ESTADISTICOS = {"varianza_residual": _var_residual, "proporcion_grandes": _prop_grandes}


@lru_cache(maxsize=None)
def cifras_c2_pliegue_anomalo():
    """P2 §4, 04·4 y ml-c2-pliegue-anomalo: caso 16, k = 5 al azar. Por grado (1, 4,
    8): L de cada pliegue, el cociente maximo/mediana de los otros cuatro, y dos
    estadisticos por pliegue (varianza del residual con signo, divisor tamaño − 1;
    proporcion de errores de mas de UMBRAL_MIN minutos)."""
    ml, w = _ml(), _silencio()
    try:
        d = ml.caso(16)
        x = d.ent["x"].to_numpy(float)
        res = {"lejanas_por_pliegue": None}
        for N in (1, 4, 8):
            cv = ml.validacion_cruzada(d, construir(N), k=5)
            pp = np.asarray(cv.por_pliegue, float)
            m = int(np.argmax(pp))
            otros = np.delete(pp, m)
            fila = {"por_pliegue": pp, "media": float(cv.media), "pliegue_max": m + 1,
                    "cociente": float(pp[m] / np.median(otros))}
            for nombre, f in ESTADISTICOS.items():
                e = ml.validacion_cruzada(d, construir(N), k=5, estadistico=f)
                v = np.asarray(e.por_pliegue_estadistico, float)
                fila[nombre] = v
                fila[f"media_{nombre}"] = float(np.mean(v))
            res[N] = fila
            if res["lejanas_por_pliegue"] is None:
                res["lejanas_por_pliegue"] = [
                    int(np.sum(x[np.asarray(val)] > 5)) for _, val in cv.pliegues]
    finally:
        w.__exit__(None, None, None)
    res["pliegues_con_lejana"] = [i + 1 for i, c in enumerate(res["lejanas_por_pliegue"]) if c]
    return res


N_ESTRAT, POS_ESTRAT, K_ESTRAT, PARTICIONES_ESTRAT = 60, 6, 5, 1000


def df_estratificada(positivos=POS_ESTRAT, n=N_ESTRAT):
    """El juguete de clasificacion: n filas, los primeros `positivos` con y = 1."""
    return pd.DataFrame({"y": np.r_[np.ones(positivos, int), np.zeros(n - positivos, int)]})


def _fraccion_vacia(positivos, como, k=K_ESTRAT, particiones=PARTICIONES_ESTRAT):
    ml = _ml()
    df = df_estratificada(positivos)
    y = df["y"].to_numpy()
    vacias = []
    for s in range(particiones):
        part = ml.pliegues(df, k=k, como=como, semilla=s)
        vacias.append(sum(int(y[np.asarray(v)].sum() == 0) for _, v in part))
    return np.array(vacias)


@lru_cache(maxsize=None)
def cifras_c2_estratificada():
    """P2 §5, 04·5 y ml-c2-estratificada: con 6 positivos, n = 60, k = 5 y 1000
    particiones por metodo, la fraccion con algun pliegue sin positivos; con 3
    positivos, el minimo de pliegues vacios (palomar)."""
    azar = _fraccion_vacia(POS_ESTRAT, "azar")
    estr = _fraccion_vacia(POS_ESTRAT, "estratificado")
    tres = np.r_[_fraccion_vacia(3, "azar"), _fraccion_vacia(3, "estratificado")]
    return {"azar": float(np.mean(azar > 0)), "estratificada": float(np.mean(estr > 0)),
            "min_vacios_con_3": int(tres.min())}


@lru_cache(maxsize=None)
def cifras_c2_anidada():
    """P2 §6, 04·6: por repeticion, CV₅ del ganador, la anidada (5×5), R del
    procedimiento replicado con 4/5 del desarrollo (elegir por CV + reajustar) y
    R del modelo final con todo el desarrollo; medias con su EE de Monte Carlo.
    Candidatos 0..8 (con 0..12 una repeticion tarda mas de lo que cabe en 04·6)."""
    ml, w = _ml(), _silencio()
    cands = candidatos(CANDIDATOS_ANIDADA)
    try:
        def una(s):
            d = fabrica(s)
            sel = ml.elegir(d, cands, con="cv", k=5)
            an = ml.cv_anidada(d, cands, k_externo=5, k_interno=5)
            des = ml._desarrollo(d)
            rng = np.random.default_rng(s)
            sub = des.iloc[np.sort(rng.choice(len(des), size=len(des) * 4 // 5, replace=False))]
            sub.attrs = des.attrs
            proc = ml.elegir(sub, cands, con="cv", k=5)
            return {"cv_ganador": float(sel.tabla.set_index("candidato").loc[sel.elegido, "valor"]),
                    "anidada": float(an.media), "R_procedimiento": ml.riesgo(proc.modelo_final, d),
                    "R_final": ml.riesgo(sel.modelo_final, d)}
        t = ml.repetir(una, repeticiones=REP_ANIDADA, semilla=SEMILLA)
    finally:
        w.__exit__(None, None, None)
    res = {"tabla": t}
    for c in ("cv_ganador", "anidada", "R_procedimiento", "R_final"):
        res[c], res[f"ee_{c}"] = _media_ee(t[c])
    res["anidada_menos_proc"], res["ee_anidada_menos_proc"] = _media_ee(
        t["anidada"] - t["R_procedimiento"])
    res["ganador_menos_proc"], res["ee_ganador_menos_proc"] = _media_ee(
        t["cv_ganador"] - t["R_procedimiento"])
    return res


# ------------------------------------------------- aritmetica a mano ---

@lru_cache(maxsize=None)
def cifras_c2_ejercicios():
    """Toda la aritmetica a mano de las tres paginas y los notebooks, exacta."""
    F = Fraction
    # P1 §2: residuales 1, -1, 2, -2
    l = [F(1), F(1), F(4), F(4)]
    Lp = sum(l) / 4
    s2 = sum((x - Lp) ** 2 for x in l) / 3
    # P2 §1: cinco pliegues
    pl = [F("9.2"), F("9.0"), F("9.1"), F("8.7"), F("8.8")]
    cv5 = sum(pl) / 5
    s2cv = sum((x - cv5) ** 2 for x in pl) / 4
    # P2 §3: elige-un-ee
    tabla = {1: (F("14.0"), F("0.6")), 2: (F("10.2"), F("0.5")), 3: (F("9.6"), F("0.4")),
             4: (F("9.5"), F("0.4")), 5: (F("9.8"), F("0.5"))}
    n_min = min(tabla, key=lambda N: (tabla[N][0], N))
    umbral = tabla[n_min][0] + tabla[n_min][1]
    un_ee = min(N for N in tabla if tabla[N][0] <= umbral)
    # P2 final: 4, 5, 6 contra 4.2, 4.8, 5.4
    g1, g5 = [F(4), F(5), F(6)], [F("4.2"), F("4.8"), F("5.4")]
    cv1, cv5b = sum(g1) / 3, sum(g5) / 3
    s5 = math.sqrt(sum((x - cv5b) ** 2 for x in g5) / 2)
    ee5 = s5 / math.sqrt(3)
    # P3 §2: tres predicciones 8, 10, 12; f = 11; ruido 4
    p = [F(8), F(10), F(12)]
    pm = sum(p) / 3
    var3 = sum((x - pm) ** 2 for x in p) / 3
    # P1 §4 (No digas): contraejemplo de la cadena por enumeracion exacta
    cadena = _contraejemplo_cadena()
    return {
        "ee_a_mano": {"L_prueba": Lp, "s2": s2, "s": math.sqrt(s2), "ee": math.sqrt(s2) / 2},
        "cuadruplicar": {"ee_400": F("0.8") / 2, "n_para_02": int((F("0.8") / F("0.2")) ** 2 * 100)},
        "tamano_prueba": int((F(10) / F("0.5")) ** 2),
        "cinco_pliegues": {"cv": cv5, "ee": math.sqrt(s2cv) / math.sqrt(5)},
        "costo": {"cv": 13 * 5 + 1, "loo": 13 * 60 + 1, "anidada": 5 * (13 * 5 + 1)},
        "elige_un_ee": {"minimo": n_min, "umbral": umbral, "un_ee": un_ee,
                        "barra_2": tabla[2][0] - tabla[2][1]},
        "final_cv": {"cv_1": cv1, "cv_5": cv5b, "desv_5": s5, "ee_5": ee5,
                     "umbral": float(cv5b) + ee5, "minimo": 5,
                     "un_ee": 1 if float(cv1) <= float(cv5b) + ee5 else 5, "ajustes": 2 * 3 + 1},
        "tres_predicciones": {"sesgo": pm - 11, "varianza": var3,
                              "total": 4 + (pm - 11) ** 2 + var3},
        "cadena": cadena,
        "clientes": {"por_entrega": (F(0) * 1 + F(10) * 9) / 10, "por_cliente": (F(0) + F(10)) / 2},
    }


def _contraejemplo_cadena():
    """Respuestas iid ±1 equiprobables; 3 de entrenamiento y 1 de validacion;
    candidatos «constante cero» y «media de entrenamiento»; elige por validacion
    (empate: el mas simple, cero). E[L_ent], E[L_val] y E[R] exactos (16 casos)."""
    from itertools import product
    F = Fraction
    tot = {"ent": F(0), "val": F(0), "R": F(0)}
    for ys in product((-1, 1), repeat=4):
        ent, v = ys[:3], ys[3]
        m = F(sum(ent), 3)
        L0 = (sum(F(y) ** 2 for y in ent) / 3, F(v) ** 2, F(1))
        Lm = (sum((y - m) ** 2 for y in ent) / 3, (v - m) ** 2, 1 + m ** 2)
        elegido = L0 if L0[1] <= Lm[1] else Lm
        tot["ent"] += elegido[0]
        tot["val"] += elegido[1]
        tot["R"] += elegido[2]
    return {k: v / 16 for k, v in tot.items()}


# --- fin tramo rapido ---


# ===================================================================
# --- tramo m ---  (pagina 3 §1–§2; se calcula en C2.T2 con lo demas)
# ===================================================================

@lru_cache(maxsize=None)
def sesgo_varianza_hilo(semilla=SEMILLA):
    ml, w = _ml(), _silencio()
    try:
        return ml.sesgo_varianza(fabrica, candidatos(), repeticiones=REP_SV, semilla=semilla)
    finally:
        w.__exit__(None, None, None)


EJE_DIANA = (15.0, 55.0)    # eje fijo de ml-c2-diana (minutos); todas caen dentro
INTERIOR = (0.5, 5.5)       # tramo interior de x: sin los bordes donde el promedio de
                            # 100 ajustes de grado alto lo arrastran unos pocos (r1)


def _predicciones_en(sv, x0, N):
    punto = pd.DataFrame({"x": [float(x0)]})
    punto.attrs = sv.malla.attrs
    return np.array([float(np.asarray(m.predecir(punto))[0]) for m in sv._modelos[N]])


@lru_cache(maxsize=None)
def cifras_c2_sesgo_varianza():
    """P3 §1–§3, 05·1–2, ml-c2-abanico y ml-c2-diana: por N, ruido, sesgo², varianza
    y total (100 repeticiones, malla de 1000 puntos de la realidad); N⋆ (el menor
    total) con la semilla maestra y con otras dos; el piso; en x0 = 5, sesgo y
    desviacion de las predicciones de N = 1 y N = 12 y cuantas caen fuera del eje."""
    ml = _ml()
    sv = sesgo_varianza_hilo()
    t = sv.tabla.set_index("candidato")
    res = {"tabla": sv.tabla, "piso": float(ml.piso(fabrica(SEMILLA))),
           "sigma2_e": float(fabrica(SEMILLA).sigma2_e)}
    for N in CANDIDATOS:
        res[N] = {c: float(t.loc[N, c]) for c in ("ruido", "sesgo2", "varianza", "total")}
    res["N_estrella"] = int(t["total"].idxmin())
    res["N_estrella_semillas"] = [res["N_estrella"]] + [
        int(sesgo_varianza_hilo(s).tabla.set_index("candidato")["total"].idxmin())
        for s in (1000, 2000)]
    verdad = float(np.asarray(sv._f_visible(pd.DataFrame({"x": [X0]})), float)[0]) \
        if hasattr(sv, "_f_visible") else float(np.interp(X0, sv.malla["x"], sv.verdad))
    res["f_x0"] = verdad
    for N in (1, 12):
        p = _predicciones_en(sv, X0, N)
        res[f"diana_{N}"] = {"sesgo": float(p.mean() - verdad), "desv": float(p.std()),
                             "fuera_eje": int(np.sum((p < EJE_DIANA[0]) | (p > EJE_DIANA[1])))}
    # Revision r1: el sesgo² promediado en toda la malla deja de bajar desde N = 8
    # (20.5 en 9, 64.9 en 12): lo arrastran los bordes, donde unos pocos ajustes
    # se disparan, y el ruido de Monte Carlo del promedio de 100. En el tramo
    # interior sigue chico; la pagina lo dice con estas cifras.
    x = sv.malla["x"].to_numpy(float)
    dentro = (x > INTERIOR[0]) & (x < INTERIOR[1])
    verdad_malla = np.asarray(sv.verdad, float)
    res["sesgo2_interior"] = {
        N: float(np.mean((sv.predicciones[N].mean(axis=0) - verdad_malla)[dentro] ** 2))
        for N in CANDIDATOS}
    res["N_sesgo2_minimo"] = int(min(CANDIDATOS, key=lambda N: res[N]["sesgo2"]))
    prom12 = sv.predicciones[12].mean(axis=0)
    res["promedio_12_min"] = float(prom12.min())
    res["promedio_12_min_x"] = float(x[int(np.argmin(prom12))])
    # R2 de §10.13: numero de condicion de Φ^T Φ con grado 12 y n = 36 (escalado)
    d = hilo()
    phi = ml.polinomio(12).ajustar(d.ent)
    X = np.asarray(phi(d.ent), float)
    res["condicion_12"] = float(np.linalg.cond(X.T @ X))
    return res


# --- fin tramo m ---


# ===================================================================
# --- tramo completo ---  (pagina 3 §3–§5, notebook 05)
# ===================================================================
# C2.T2, segunda parte (DECISION prog-c2-9): curvas de aprendizaje (§4),
# los cuatro procesos del diagnostico (§5, 05·4) y el consultor del
# ejercicio final.

NS_CURVA = (30, 60, 120, 240, 480, 960)   # duplicando desde 30 >= 2·(10 + 1)
GRADOS_CURVA = (1, 10)
REP_CURVA = 50              # 05·3 y ml-c2-curva-aprendizaje (medianas)
REP_ELEGIDO = 20            # panel de abajo: grado elegido por CV_5
CANDIDATOS_ELEGIDO = tuple(range(13))
SEMILLAS_MAESTRAS = (0, 1000, 2000)


def fabrica_curva(s):
    """fabrica de 960 entregas (todas las filas: fracciones (1, 0, 0))."""
    return _ml().PROCESOS["entregas_curvas"](n=max(NS_CURVA), semilla=int(s),
                                             n_realidad=N_REALIDAD, fracciones=(1, 0, 0))


@lru_cache(maxsize=None)
def tabla_curva_aprendizaje(semilla=SEMILLA):
    ml, w = _ml(), _silencio()
    try:
        return ml.curva_aprendizaje(fabrica_curva, {N: construir(N) for N in GRADOS_CURVA},
                                    ns=NS_CURVA, repeticiones=REP_CURVA, semilla=semilla)
    finally:
        w.__exit__(None, None, None)


@lru_cache(maxsize=None)
def tabla_capacidad_elegida(semilla=SEMILLA):
    ml, w = _ml(), _silencio()
    try:
        return ml.capacidad_elegida(fabrica_curva, candidatos(CANDIDATOS_ELEGIDO), ns=NS_CURVA,
                                    k=5, repeticiones=REP_ELEGIDO, semilla=semilla)
    finally:
        w.__exit__(None, None, None)


def _medianas_R(t):
    return {(int(N), int(n)): float(v)
            for (N, n), v in t.groupby(["candidato", "n"])["R"].median().items()}


@lru_cache(maxsize=None)
def cifras_c2_taller_descomponer():
    """taller-intro del guion 05 (revision r1): lo que imprime
    ml.taller(hilo(), clase=2, que="descomponer") con sus valores por omision
    (50 repeticiones, malla de toda la realidad, bordes incluidos). El sesgo²
    del grado 12 sale enorme por los pocos ajustes que se disparan en los bordes;
    el guion lo avisa con esta cifra."""
    ml, w = _ml(), _silencio()
    try:
        d = hilo()
        construir_ = {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N, variable="x")))
                      for N in CANDIDATOS}
        t = ml.sesgo_varianza(d.rehacer, construir_, repeticiones=50).tabla
        t = t.set_index("candidato")
    finally:
        w.__exit__(None, None, None)
    return {N: {k: float(t.loc[N, k]) for k in ("sesgo2", "varianza", "total")}
            for N in CANDIDATOS}


@lru_cache(maxsize=None)
def cifras_c2_curva_aprendizaje():
    """P3 §4, 05·3 y ml-c2-curva-aprendizaje: medianas de R (50 repeticiones) de los
    grados 1 y 10 en n = 30, 480 y 960; mediana de L_ent; grado que elige CV_5
    (mediana de 20 repeticiones) en 30 y 960; el piso; y las mismas medianas con
    las otras dos semillas maestras (estabilidad)."""
    ml = _ml()
    t = tabla_curva_aprendizaje()
    med = _medianas_R(t)
    lent = {(int(N), int(n)): float(v)
            for (N, n), v in t.groupby(["candidato", "n"])["L_ent"].median().items()}
    el = tabla_capacidad_elegida().groupby("n")["elegido"].median()
    res = {"piso": float(ml.piso(fabrica_curva(SEMILLA))),
           "R": {(N, n): med[(N, n)] for N in GRADOS_CURVA for n in NS_CURVA},
           "L_ent": {(N, n): lent[(N, n)] for N in GRADOS_CURVA for n in NS_CURVA},
           "elegido": {int(n): float(v) for n, v in el.items()},
           "elegido_rango": {int(n): (int(g.min()), int(g.max())) for n, g in
                             tabla_capacidad_elegida().groupby("n")["elegido"]}}
    res["R_otras_semillas"] = {s: _medianas_R(tabla_curva_aprendizaje(s))
                               for s in SEMILLAS_MAESTRAS[1:]}
    return res


# ----------------------------------------------------- diagnostico (§5) ---
# Cuatro procesos misteriosos (05·4 y el micro ml-c2-ej-cuatro-curvas). Sus
# parametros los fija esta tabla (Decidir en ejecucion de clase_2.md §10.3);
# con n = 200 la diferencia pareada de A en validacion (40 entregas) no salia
# de 2 EE, asi que A, C y D usan n = 400 (80 de validacion), y B, n = 40
# (24 de entrenamiento: con 15 el grado 12 interpola y la CV vale 10^5).

def _f_casi_constante(d):
    return 30 + 0.2 * d["x"]


def proceso_diagnostico(nombre, semilla=SEMILLA):
    ml = _ml()
    if nombre == "C":
        return ml.proceso(n=400, x={"x": ml.uniforme(0, 6)}, f=_f_casi_constante,
                          ruido=ml.normal(0, 8), semilla=semilla, n_realidad=N_REALIDAD)
    n = 40 if nombre == "B" else 400
    return ml.PROCESOS["entregas_curvas"](n=n, semilla=semilla, n_realidad=N_REALIDAD)


GRADO_DIAGNOSTICO = {"A": 1, "B": 12, "C": 1, "D": 4}
HOJA_DIAGNOSTICO = {"A": "subajuste", "B": "sobreajuste", "C": "no aprende", "D": "listo"}
UMBRAL_BRECHA = 2.0         # brecha grande: CV_5 mayor que el doble de L_ent


def hoja_del_arbol(r):
    """Recorre el arbol de ml-c2-diagnostico con las cifras de un proceso."""
    if r["CV"] > UMBRAL_BRECHA * r["L_ent"]:
        return "sobreajuste"
    if not r["gana_a"]:
        return "no aprende"
    if r["mejor_mas_flexible"] is not None and \
            r["CV_mejor_mas_flexible"] < r["CV"] - r["EE"]:
        return "subajuste"
    return "listo"


@lru_cache(maxsize=None)
def cifras_c2_diagnostico():
    """P3 §5, 05·4 y ml-c2-ej-cuatro-curvas: por proceso, L_ent y CV_5 ± EE del modelo
    actual, la CV_5 del mejor grado mas flexible (0–8; 0–12 para B), el benchmark
    (grado 0) con su EE, (a) la diferencia pareada modelo − benchmark en validacion
    con su EE (los dos ajustados solo con ent: la validacion no eligio nada), (b) la
    diferencia de las CV_5 y sus cinco diferencias por pliegue (misma particion;
    descriptiva) y, solo para el notebook, piso y R − piso. Nunca s_d/√n sobre
    perdidas_fuera (guarda negativa en la prueba)."""
    ml, w = _ml(), _silencio()
    res = {}
    try:
        for nombre, N in GRADO_DIAGNOSTICO.items():
            d = proceso_diagnostico(nombre)
            M = max(8, N)
            cvs = {g: ml.validacion_cruzada(d, construir(g), k=5, semilla=SEMILLA)
                   for g in range(M + 1)}
            modelo, bench = construir(N)(d.ent), construir(0)(d.ent)
            yv = d.val["y"].to_numpy()
            dm, ee_d = ml.diferencia_pareada(
                ml.perdida(yv, np.asarray(modelo.predecir(d.val))),
                ml.perdida(yv, np.asarray(bench.predecir(d.val))))
            dpp = ml.diferencia_por_pliegue(cvs[N], cvs[0])
            por = [float(v) for v in dpp["diferencia"].iloc[:5]]
            mas = [g for g in range(N + 1, M + 1)]
            mejor = min(mas, key=lambda g: cvs[g].media) if mas else None
            media_b = float(dpp["diferencia"].iloc[5])
            r = {"grado": N, "n": len(d.ent) + len(d.val) + len(d.prueba),
                 "L_ent": float(ml.L(modelo, d.ent)), "CV": float(cvs[N].media),
                 "EE": float(cvs[N].ee), "mejor_mas_flexible": mejor,
                 "CV_mejor_mas_flexible": float(cvs[mejor].media) if mejor is not None
                 else float("nan"),
                 "benchmark": float(cvs[0].media), "benchmark_ee": float(cvs[0].ee),
                 "dif_val": float(dm), "dif_val_ee": float(ee_d),
                 "gana_a": bool(dm < -2 * ee_d),
                 "dif_cv": media_b, "dif_por_pliegue": por,
                 "senal_b": bool(abs(media_b) > float(np.std(por, ddof=1))),
                 "curva_cv": {g: float(cvs[g].media) for g in cvs},
                 "piso": float(ml.piso(d))}
            # R con la media condicional conocida: R = piso + E_x[(f̂ − f)²] en la
            # muestra de despliegue (revision r1: ml.riesgo es una estimacion con
            # 2000 y en C daba R < piso, un exceso negativo imposible)
            dep = d.despliegue
            exceso = np.mean((np.asarray(modelo.predecir(dep), float)
                              - np.asarray(d.f_visible(dep), float)) ** 2)
            r["R_menos_piso"] = float(exceso)
            r["R"] = r["piso"] + r["R_menos_piso"]
            r["hoja"] = hoja_del_arbol(r)
            res[nombre] = r
    finally:
        w.__exit__(None, None, None)
    return res


# ------------------------------------------------- ejercicio final (P3) ---
# El consultor reporta medianas de 20 muestras de cada tamaño (una sola
# muestra por tamaño daba mejoras de −14 % a 45 % para el mismo modelo: el
# ejercicio no se sostenia). A = grado 12 (sobreajusta), B = grado 1 (recta).

N_CONSULTOR = (120, 480)
REP_CONSULTOR = 20
GRADOS_CONSULTOR = {"A": 12, "B": 1}


@lru_cache(maxsize=None)
def cifras_c2_diagnostico_final():
    """Ejercicio final de P3: L_ent y CV_5 (medianas de 20 muestras) de los dos
    modelos del consultor con n_ent = 120 y 480, y la mejora relativa de la CV."""
    ml, w = _ml(), _silencio()
    res = {}
    try:
        for nombre, N in GRADOS_CONSULTOR.items():
            r = {"grado": N}
            for n in N_CONSULTOR:
                le, cv = [], []
                for i in range(REP_CONSULTOR):
                    d = ml.PROCESOS["entregas_curvas"](n=n, semilla=SEMILLA + i,
                                                     n_realidad=N_REALIDAD, fracciones=(1, 0, 0))
                    le.append(ml.L(construir(N)(d.ent), d.ent))
                    cv.append(ml.validacion_cruzada(d, construir(N), k=5,
                                                    semilla=SEMILLA + i).media)
                r[n] = {"L_ent": float(np.median(le)), "CV": float(np.median(cv))}
            r["mejora"] = 1 - r[N_CONSULTOR[1]]["CV"] / r[N_CONSULTOR[0]]["CV"]
            res[nombre] = r
    finally:
        w.__exit__(None, None, None)
    return res


# --- fin tramo completo ---
