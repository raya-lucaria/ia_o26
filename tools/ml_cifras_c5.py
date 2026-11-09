"""Cifras de la clase 5 de la unidad de aprendizaje de maquina (unidad 9).

Una funcion por hecho que cita una pagina, un notebook o una figura de la
clase 5 (clase_5.md §10.7, tabla de ml_cifras_c5). Ninguna cifra se escribe a
mano: la pagina la copia de aqui, tools/test_ml_cifras_c5.py la fija en la
fuente y tools/test_ml_prosa_c5.py la busca en la pagina que la cita
(D-009.5, D-003).

Cada funcion devuelve un dict con los valores crudos y, en la clave "cita",
las formas literales con que la pagina y las figuras los escriben (cadenas ya
redondeadas). Las funciones se guardan en cache: la suite y el generador de
figuras las llaman muchas veces y varias cuestan segundos.

Los procesos salen de ml_lab, nunca se redefinen aqui (§10.3): los casos 13,
14, 19, 20, 21, 26, 27 y 28, «llego tarde» (la base de los casos de fugas) y
PROCESOS["entregas_curvas"] con mas columnas (ENTREGAS_C5, la de los bloques
B2 y la taller del notebook 10). Repeticiones: lo que plan llama «200
semillas» se mide con las que caben en el tiempo de la suite (REPETICIONES,
DECISION prog-c5-2); toda figura reporta mediana y rango intercuartil.

ml_lab se importa de tools/ (nunca de _assets/, D-004) y solo dentro de las
funciones.
"""
import contextlib
import functools
import importlib
import math
import warnings
from fractions import Fraction

import numpy as np

REQUIERE = "1.6"
SEMILLA = 0


def _ml():
    """tools/aprendizaje_maquina.py (ml_lab), importado al pedirlo."""
    return importlib.import_module("aprendizaje_maquina")


def _f(v, d):
    """La forma con que la pagina escribe un numero: d decimales."""
    return f"{float(v):.{d}f}"


@contextlib.contextmanager
def _silencio():
    """Los avisos de ml_lab (pseudoinversa, categorias nuevas) no son cifras."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


def _mediana_ric(valores):
    v = np.asarray(valores, float)
    q1, q2, q3 = np.percentile(v, [25, 50, 75])
    return float(q2), float(q1), float(q3)


# Cantidades de escenario de los enunciados (§10.7, D-009.5 leido estricto).
# Las de P2 son los parametros con que cifras_c5_final_metodologia calcula su
# tabla. test_ml_prosa_c5 las busca en la pagina.
ESCENARIOS = {
    "p1_final": {"semanas": 8, "semana_uso": 9, "pedidos": 3000, "clientes": 400,
                 "nuevos_semana_8": 60, "pedidos_semana_8": 450,
                 "nuevos_semanas_3_7": (40, 60)},
    "p2_final": {"pedidos": 2000, "clientes": 300},
    "phi_perfecta": {"unidades": 50, "filas": 400},
    "ks_a_mano": {"ent": (0, 1, 2), "nuevo": (1, 2, 3)},
}

# Repeticiones (DECISION prog-c5-2): las que caben en la suite.
REPETICIONES = {"cv_miente": 20, "fugas": 5, "preprocesar": 20, "ks": 200,
                "autocorrelacion": 200, "diagnostico": 10, "familias": 5,
                "bagging": 2000, "cybenko": 5, "cybenko_anillos": 3}


# ------------------------------------------------------------ procesos ---

def f_entregas_c5(d):
    """Las entregas de la clase 2 (f de entregas_curvas en distancia) mas lluvia y hora."""
    x = np.asarray(d["distancia"], float)
    base = 10 + 12 * np.log1p(x) + 4 * np.exp(-(x - 3) ** 2 / 0.5)
    return base + 6.0 * np.asarray(d["lluvia"], float) + 0.4 * (np.asarray(d["hora"], float) - 15)


def x_entregas_c5():
    ml = _ml()
    return {"distancia": ml.uniforme(0, 6), "hora": ml.uniforme(8, 22),
            "lluvia": ml.categorica([0, 1], [0.8, 0.2])}


def entregas_c5(n=400, semilla=SEMILLA, **cambios):
    """PROCESOS["entregas_curvas"] con mas columnas: distancia, hora y lluvia (sigma 3)."""
    ml = _ml()
    base = dict(n=n, x=x_entregas_c5(), f=f_entregas_c5, semilla=semilla)
    base.update(cambios)
    return ml.PROCESOS["entregas_curvas"](**base)


def phi_referencia():
    """La tuberia de referencia: polinomio de grado 6 en distancia, mas lluvia y hora."""
    ml = _ml()
    return ml.combinar(ml.polinomio(6, variable="distancia"), ml.columnas("lluvia", "hora"))


@functools.lru_cache(maxsize=None)
def cifras_c5_referencia():
    """Criterio de §10.3: la tuberia de referencia a <= 10 % del piso con despliegue igual."""
    ml = _ml()
    with _silencio():
        d = entregas_c5()
        m = ml.ajustar(d, phi=phi_referencia())
        R, piso = float(ml.riesgo(m, d)), float(ml.piso(d))
    return {"R": R, "piso": piso, "razon": R / piso,
            "cita": {"R": _f(R, 1), "piso": _f(piso, 1)}}


def llego_tarde(n=600, semilla=SEMILLA, **cambios):
    """«Llego tarde» de ml_lab (distancia, hora y lluvia; ~25 % tarde) con faltantes en
    distancia (30 %, «depende_x»): el Datos de la figura ml-c5-fugas y del bloque B4."""
    ml = _ml()
    cambios.setdefault("faltantes", {"distancia": (0.3, "depende_x")})
    return ml._llego_tarde(n=n, semilla=semilla, **cambios)


# --------------------------------------------------------- P1 §3: KS ---

@functools.lru_cache(maxsize=None)
def cifras_c5_ks_a_mano():
    """El micro de KS: entrenamiento (0,1,2), nuevo (1,2,3) -> 1/3, exacto."""
    a, b = ESCENARIOS["ks_a_mano"]["ent"], ESCENARIOS["ks_a_mano"]["nuevo"]
    puntos = sorted(set(a) | set(b))
    Fa = [Fraction(sum(v <= p for v in a), len(a)) for p in puntos]
    Fb = [Fraction(sum(v <= p for v in b), len(b)) for p in puntos]
    ks = max(abs(x - y) for x, y in zip(Fa, Fb))
    ml = _ml()
    import pandas as pd
    lab = ml.ks_por_variable(pd.DataFrame({"x": a}), pd.DataFrame({"x": b}))
    return {"ks": ks, "Fa": Fa, "Fb": Fb, "ks_lab": float(lab["estadistico"].iloc[0]),
            "cita": {"ks": "1/3", "Fa": "(1/3, 2/3, 1, 1)", "Fb": "(0, 1/3, 2/3, 1)"}}


@functools.lru_cache(maxsize=None)
def cifras_c5_ks():
    """KS_j de la variable que deriva (el mes que viene) y falsas alarmas con J = 20
    variables de ruido iid en REPETICIONES["ks"] repeticiones (cuantas p < 0.05)."""
    from scipy import stats
    ml = _ml()
    det = datos_detectores()
    ks = ml.ks_por_variable(det["ent"], det["usos"]["deriva"], columnas=["distancia", "hora"])
    ks_nada = ml.ks_por_variable(det["ent"], det["usos"]["nada"], columnas=["distancia", "hora"])
    rng = np.random.default_rng([SEMILLA, 51])
    alarmas = []
    for _ in range(REPETICIONES["ks"]):
        a = rng.standard_normal((N_ENT_DET, 20))
        b = rng.standard_normal((N_USO_DET, 20))
        p = [stats.ks_2samp(a[:, j], b[:, j]).pvalue for j in range(20)]
        alarmas.append(int(np.sum(np.asarray(p) < 0.05)))
    med, q1, q3 = _mediana_ric(alarmas)
    v = float(ks.set_index("variable").loc["distancia", "estadistico"])
    v0 = float(ks_nada.set_index("variable").loc["distancia", "estadistico"])
    return {"ks_deriva": v, "ks_nada": v0, "alarmas": alarmas, "mediana": med,
            "cita": {"ks_deriva": _f(v, 2), "ks_nada": _f(v0, 2), "mediana_alarmas": f"{med:g}",
                     "J": "20"}}


# ------------------------------------------- P1 §3: autocorrelacion ---

@functools.lru_cache(maxsize=None)
def modelo_residuales(memoria):
    """La tuberia de referencia ajustada en los primeros 360 dias y la validacion (los
    240 que siguen), con ruido sin memoria (ar1 0) o con memoria (ar1 0.9)."""
    ml = _ml()
    ruido = ml.ar1(0.9 if memoria == "con" else 0.0, 3.0)
    with _silencio():
        d = entregas_c5(n=600, ruido=ruido, fracciones=(0.6, 0.4, 0.0), separar="tiempo")
        m = ml.ajustar(d, phi=phi_referencia())
    return m, d.val.sort_values("t")


@functools.lru_cache(maxsize=None)
def cifras_c5_autocorrelacion():
    """(1,-1,...) -> -5/6 con autocorrelacion; rezago 1 de residuales de validacion con
    y sin memoria (ar1 0.9); cuantos de 20 rezagos de ruido blanco salen de la banda."""
    ml = _ml()
    alterna = np.array([1, -1, 1, -1, 1, -1], float)
    r_alt = float(ml.autocorrelacion(alterna, rezagos=1)[0])
    pearson = float(np.corrcoef(alterna[:-1], alterna[1:])[0, 1])
    res = {}
    for nombre in ("sin", "con"):
        m, v = modelo_residuales(nombre)
        e = v["y"].to_numpy(float) - np.asarray(m.predecir(v), float)
        res[nombre] = float(ml.autocorrelacion(e, rezagos=1)[0])
    rng = np.random.default_rng([SEMILLA, 52])
    fuera = []
    n = 200
    for _ in range(REPETICIONES["autocorrelacion"]):
        r = ml.autocorrelacion(rng.standard_normal(n), rezagos=20)
        fuera.append(int(np.sum(np.abs(r) > 2 / math.sqrt(n))))
    med, q1, q3 = _mediana_ric(fuera)
    return {"alterna": r_alt, "pearson": pearson, "rezago1_sin": res["sin"],
            "rezago1_con": res["con"], "fuera": fuera, "mediana_fuera": med,
            "cita": {"alterna": "−5/6", "pearson": "−1", "rezago1_sin": _f(res["sin"], 2),
                     "rezago1_con": _f(res["con"], 2), "mediana_fuera": f"{med:g}"}}


# ------------------------------------- P1 §3: validacion adversarial ---

N_ENT_DET, N_USO_DET = 600, 150  # o barra = 150 / 750 = 0.2


def _deriva_mes(t):
    return {"distancia": _ml().uniforme(1.5, 7.5)}


def _deriva_concepto(t):
    def f_trafico(d):
        x = np.asarray(d["distancia"], float)
        return f_entregas_c5(d) + 0.5 * 12 * np.log1p(x)
    return {"f": f_trafico}


def _mismas_marginales(n, semilla):
    """Distancia y hora con las marginales de ENTREGAS_C5 y otra correlacion: con
    u, v ~ U(0, 1) independientes, distancia = 6u y hora = 8 + 14·frac(u + 0.15 v),
    que sigue siendo uniforme en (8, 22) (u + algo independiente, modulo 1)."""
    import pandas as pd
    rng = np.random.default_rng([semilla, 53])
    u, v = rng.random(n), rng.random(n)
    w = rng.random(n)
    return pd.DataFrame({"distancia": 6 * u, "hora": 8 + 14 * np.mod(u + 0.15 * v, 1.0),
                         "lluvia": (w < 0.2).astype(int)})


@functools.lru_cache(maxsize=None)
def datos_detectores():
    """Los escenarios del bloque B2 y de ml-c5-detectores: entrenamiento de 600 filas y
    usos de 150 (o barra = 0.2): nada, el mes que viene (deriva en distancia), el
    trafico (caso 28: cambia f, no x) y mismas marginales con otra correlacion."""
    with _silencio():
        nada = entregas_c5(n=N_ENT_DET, fracciones=(1, 0, 0))
        deriva = entregas_c5(n=N_ENT_DET, fracciones=(1, 0, 0), despliegue="otra_poblacion",
                             deriva=_deriva_mes)
        concepto = entregas_c5(n=N_ENT_DET, fracciones=(1, 0, 0), despliegue="otra_poblacion",
                               deriva=_deriva_concepto)
    usos = {"nada": nada.despliegue.iloc[:N_USO_DET].copy(),
            "deriva": deriva.despliegue.iloc[:N_USO_DET].copy(),
            "concepto": concepto.despliegue.iloc[:N_USO_DET].copy(),
            "marginales": _mismas_marginales(N_USO_DET, SEMILLA)}
    return {"ent": nada.ent, "usos": usos, "datos": {"nada": nada, "deriva": deriva,
                                                     "concepto": concepto}}


COLUMNAS_DET = ["distancia", "hora", "lluvia"]


def _reserva_pareada(ent, uso, familia, semilla=SEMILLA):
    """Caso (a) de ml-c3-def-benchmark: una reserva que no toco ninguna decision. Se
    parte cada tabla en mitades; el clasificador y la proporcion se ajustan con una
    mitad y se mide en la otra la diferencia pareada de perdida logaritmica contra el
    benchmark de la proporcion, con su EE por filas."""
    ml = _ml()
    rng = np.random.default_rng([semilla, 54])
    ia, iu = rng.permutation(len(ent)), rng.permutation(len(uso))
    a1, a2 = ent.iloc[ia[: len(ia) // 2]], ent.iloc[ia[len(ia) // 2:]]
    u1, u2 = uso.iloc[iu[: len(iu) // 2]], uso.iloc[iu[len(iu) // 2:]]
    X1 = np.vstack([a1[COLUMNAS_DET].to_numpy(float), u1[COLUMNAS_DET].to_numpy(float)])
    o1 = np.r_[np.zeros(len(a1)), np.ones(len(u1))]
    X2 = np.vstack([a2[COLUMNAS_DET].to_numpy(float), u2[COLUMNAS_DET].to_numpy(float)])
    o2 = np.r_[np.zeros(len(a2)), np.ones(len(u2))]
    est = ml._clasificador_adversarial(familia, semilla).fit(X1, o1)
    p = np.clip(est.predict_proba(X2)[:, 1], 1e-15, 1 - 1e-15)
    ob = float(o1.mean())
    l_m = -(o2 * np.log(p) + (1 - o2) * np.log(1 - p))
    l_b = -(o2 * math.log(ob) + (1 - o2) * math.log(1 - ob))
    dif, ee = ml.diferencia_pareada(l_m, l_b)
    return float(dif), float(ee)


@functools.lru_cache(maxsize=None)
def cifras_c5_adversarial():
    """P1 §3, ml-c5-detectores y B2: perdida logaritmica contra el benchmark de la
    proporcion y MCC con tau = o barra, en cuatro escenarios (los de las marginales con
    bosque y con logistica); senal por pliegue y reserva pareada; clientes repetidos
    con pliegues al azar contra por grupos; y el control con o barra = 0.2 y deriva:
    MCC cortando en o barra contra cortando en 0.5."""
    ml = _ml()
    det = datos_detectores()
    ent = det["ent"]
    res = {}
    with _silencio():
        for nombre, uso in det["usos"].items():
            familias = ("bosque", "logistica") if nombre == "marginales" else ("bosque",)
            for fam in familias:
                r = ml.validacion_adversarial(ent, uso, columnas=COLUMNAS_DET, familia=fam)
                dif = np.asarray(r.diferencias_por_pliegue, float)
                d_res, ee_res = _reserva_pareada(ent, uso, fam)
                p05 = (np.asarray(r.prob) >= 0.5).astype(int)
                res[f"{nombre}_{fam}"] = {
                    "log_loss": r.log_loss, "benchmark": r.log_loss_benchmark,
                    "mcc": r.mcc, "o_bar": r.o_bar, "senal": r.senal,
                    "dif_media": float(dif.mean()), "dif_desv": float(dif.std(ddof=1)),
                    "reserva": d_res, "reserva_ee": ee_res,
                    "mcc_05": ml.mcc(r.origen, p05, clases=[0, 1])}
        res["clientes"] = _adversarial_clientes()
    o = res["nada_bosque"]["o_bar"]
    bench = -(o * math.log(o) + (1 - o) * math.log(1 - o))
    cita = {k: {"log_loss": _f(v["log_loss"], 3), "benchmark": _f(v["benchmark"], 3),
                "mcc": _f(v["mcc"], 2), "senal": v["senal"]}
            for k, v in res.items() if k != "clientes"}
    cita["o_bar"] = _f(o, 1)
    cita["benchmark_formula"] = _f(bench, 3)
    # El control de §10.7 (DECISION prog-c5-3): con la deriva fuerte del mes que viene
    # el corte en 0.5 tambien ve la diferencia (y da mas MCC); donde se queda en 0 es con
    # una diferencia moderada, la de «mismas marginales»: ahi el corte en o barra la ve.
    cita["control"] = {"mcc_obar": _f(res["marginales_bosque"]["mcc"], 2),
                       "mcc_05": _f(res["marginales_bosque"]["mcc_05"], 2),
                       "deriva_mcc_obar": _f(res["deriva_bosque"]["mcc"], 2),
                       "deriva_mcc_05": _f(res["deriva_bosque"]["mcc_05"], 2)}
    cita["clientes"] = {k: _f(v, 2) for k, v in res["clientes"].items()}
    return {**res, "benchmark_formula": bench, "cita": cita}


def _adversarial_clientes(n_clientes=100, pedidos=5, semilla=SEMILLA):
    """Clientes que repiten: cada uno pide desde su casa (distancia y hora casi fijas).
    A: los primeros 80 clientes; B: los ultimos 20. Mismo proceso: al azar el bosque
    «reconoce» clientes y detecta; por grupos, no."""
    import pandas as pd
    ml = _ml()
    rng = np.random.default_rng([semilla, 55])
    casa = rng.uniform(0, 6, n_clientes)
    costumbre = rng.uniform(8, 22, n_clientes)
    g = np.repeat(np.arange(n_clientes), pedidos)
    df = pd.DataFrame({"distancia": casa[g] + rng.normal(0, 0.05, len(g)),
                       "hora": costumbre[g] + rng.normal(0, 0.2, len(g)),
                       "lluvia": (rng.random(len(g)) < 0.2).astype(int), "grupo": g})
    a, b = df[df["grupo"] < 80], df[df["grupo"] >= 80]
    azar = ml.validacion_adversarial(a, b, columnas=COLUMNAS_DET, particion="estratificado")
    grupos = ml.validacion_adversarial(a, b, columnas=COLUMNAS_DET, particion="grupo")
    return {"mcc_azar": azar.mcc, "mcc_grupos": grupos.mcc,
            "ll_azar": azar.log_loss, "ll_grupos": grupos.log_loss,
            "benchmark": azar.log_loss_benchmark}


# ---------------------------------------------- P1 §4: la CV que miente ---

CAMBIOS_CASO_13 = {"persistencia": 0.9, "n": 600}  # «más filas que en la clase 2»
CAMBIOS_CASO_14 = {}


def modelo_caso_13(d):
    """El modelo de la clase 2 para el caso 13: vecinos sobre (x, t)."""
    return _ml().ajustar_otro(d, familia="vecinos", columnas_x=["x", "t"], n_vecinos=5)


def modelo_caso_14(d):
    """El modelo de la clase 2 para el caso 14: polinomio de grado 3 mas un efecto por
    cliente (codificacion por efectos)."""
    ml = _ml()
    return ml.ajustar(d, phi=ml.combinar(ml.polinomio(3),
                                         ml.dummies("grupo", codificacion="efectos")))


def modelo_lineal_x(d):
    return _ml().ajustar(d)


def _una_cv_miente(caso, cambios, modelo, particion, semilla):
    ml = _ml()
    d = ml.caso(caso, semilla=semilla, **cambios)
    azar = ml.validacion_cruzada(d, modelo, k=5, particion="azar").media
    est = ml.validacion_cruzada(d, modelo, k=5, particion=particion).media
    R = ml.riesgo(modelo(ml._desarrollo(d)), d)
    return float(azar), float(est), float(R)


@functools.lru_cache(maxsize=None)
def cifras_c5_cv_miente():
    """Casos 13 y 14 x {lineal en x, el modelo de la clase 2}: CV al azar, CV
    estructurada (temporal / por grupos) y R en el despliegue; mediana y rango
    intercuartil en REPETICIONES["cv_miente"] semillas."""
    res = {}
    with _silencio():
        for caso, cambios, modelo, part in (
                (13, CAMBIOS_CASO_13, modelo_caso_13, "temporal"),
                (14, CAMBIOS_CASO_14, modelo_caso_14, "grupo")):
            for nombre, m in (("clase2", modelo), ("lineal", modelo_lineal_x)):
                filas = np.array([_una_cv_miente(caso, cambios, m, part, s)
                                  for s in range(REPETICIONES["cv_miente"])])
                res[(caso, nombre)] = {
                    clave: _mediana_ric(filas[:, i])
                    for i, clave in enumerate(("azar", "estructurada", "R"))}
                res[(caso, nombre)]["razones"] = filas[:, 0] / filas[:, 2]
    cita = {}
    for (caso, nombre), v in res.items():
        cita[f"c{caso}_{nombre}"] = {k: _f(v[k][0], 0 if caso == 13 else 1)
                                     for k in ("azar", "estructurada", "R")}
    return {"res": res, "cita": cita}


# ------------------------------------------------- P1 §5: fugas ---

N_VECINOS_FUGAS = 1  # «vecinos con pocos vecinos» (caso 21); la misma tuberia para todas
N_REALIDAD_FUGAS = 4000
RUTAS = (("ninguna", "ninguna"), ("posterior", "calificación posterior"),
         ("preprocesar_antes", "escalar e imputar antes"),
         ("duplicados", "pedidos duplicados"),
         ("seleccion_previa", "elegir variables antes"))


def construir_vecinos(df):
    """La tuberia de vecinos de la figura ml-c5-fugas y del bloque B4: imputa (mediana e
    indicadora) y estandariza dentro del ajuste las columnas que trae el Datos."""
    ml = _ml()
    cols = list(df.attrs["ml"]["columnas_x"])
    falta = [f"{c}_falta" for c in cols if df[c].isna().any() and f"{c}_falta" not in cols]
    phi = ml.estandarizar(ml.columnas(*(cols + falta)))
    return ml.tuberia(ml.imputador(), phi, modelo={"familia": "vecinos",
                                                   "n_vecinos": N_VECINOS_FUGAS})(df)


def construir_logistica(df):
    """La logistica sin castigo sobre las columnas del Datos (el caso 26)."""
    return _ml().ajustar(df)


def construir_logistica_limpia():
    """La version limpia del caso 26: elegir 10 columnas dentro de cada pliegue, desde
    columnas_universo (las 500 de ruido mas las tres del proceso)."""
    ml = _ml()
    return ml.tuberia(ml.seleccionar(k=10), modelo={"familia": "logistica"})


@functools.lru_cache(maxsize=None)
def _fugas_semilla(s):
    ml = _ml()
    with _silencio():
        d = llego_tarde(semilla=s, n_realidad=N_REALIDAD_FUGAS)
        t = ml.medir_fugas(d, construir_vecinos, tipos=("ninguna", "posterior",
                                                       "preprocesar_antes", "duplicados"),
                           criterio="mcc")
        d26 = ml.caso(26, semilla=s, n_realidad=N_REALIDAD_FUGAS)
        cv26 = ml.validacion_cruzada(d26, construir_logistica, criterio="mcc").media
        uso26 = ml.desempeno(construir_logistica(ml._desarrollo(d26)), d26, "mcc")
        limpia = construir_logistica_limpia()
        cv26l = ml.validacion_cruzada(d26, limpia, criterio="mcc").media
        uso26l = ml.desempeno(limpia(ml._desarrollo(d26)), d26, "mcc")
    filas = {r.tipo: (r.estimado, r.en_uso) for r in t.itertuples()}
    filas["seleccion_previa"] = (cv26, uso26)
    filas["seleccion_limpia"] = (cv26l, uso26l)
    return filas


@functools.lru_cache(maxsize=None)
def cifras_c5_fugas():
    """ml-c5-fugas y P1 §5: por ruta, MCC de la CV y MCC en el despliegue (mediana y
    RIC en REPETICIONES["fugas"] semillas). Las cuatro primeras sobre «llego tarde»
    (n = 600, distancia con 30 % de faltantes) con la tuberia de vecinos; «elegir
    variables antes» es el caso 26 (n = 100, y no depende de nada) con la logistica
    (DECISION prog-c5-4: sobre «llego tarde», con senal real, elegir 10 de 503 casi no
    infla). Y el caso 20: proporcion de semillas en que la CV con la fuga promete mas
    que la limpia, y la mediana de la diferencia."""
    sem = range(REPETICIONES["fugas"])
    por = [_fugas_semilla(s) for s in sem]
    res = {}
    for tipo in [t for t, _ in RUTAS] + ["seleccion_limpia"]:
        cv = [p[tipo][0] for p in por]
        uso = [p[tipo][1] for p in por]
        res[tipo] = {"cv": _mediana_ric(cv), "uso": _mediana_ric(uso),
                     "inflado": _mediana_ric(np.subtract(cv, uso))}
    res["caso20"] = _caso_20_semillas()
    cita = {t: {"cv": _f(v["cv"][0], 2), "uso": _f(v["uso"][0], 2),
                "inflado": _f(v["inflado"][0], 2)} for t, v in res.items() if t != "caso20"}
    c20 = res["caso20"]
    cita["caso20"] = {"optimistas": f"{c20['optimistas']} de {c20['n']}",
                      "mediana_dif": _f(c20["mediana_dif"], 3)}
    return {**res, "cita": cita}


@functools.lru_cache(maxsize=None)
def _caso_20_semillas():
    """Caso 20 en REPETICIONES["preprocesar"] semillas: CV de la tuberia de vecinos sobre
    los datos ya imputados y escalados con todas las filas, contra la misma CV sobre los
    datos crudos (todo se ajusta dentro del pliegue)."""
    ml = _ml()
    dif = []
    with _silencio():
        for s in range(REPETICIONES["preprocesar"]):
            d = llego_tarde(semilla=s, n_realidad=1000)
            fuga = ml.sembrar_fuga(d, "preprocesar_antes")
            a = ml.validacion_cruzada(fuga, construir_vecinos, criterio="mcc").media
            b = ml.validacion_cruzada(d, construir_vecinos, criterio="mcc").media
            dif.append(a - b)
    dif = np.asarray(dif)
    return {"dif": dif, "optimistas": int(np.sum(dif > 0)), "n": len(dif),
            "mediana_dif": float(np.median(dif))}


@functools.lru_cache(maxsize=None)
def cifras_c5_tuberia():
    """P1 §6 y B5: la CV con y sin tuberia para escalar e imputar antes y para elegir
    variables antes, contra el MCC en el despliegue (mediana de las semillas de fugas y
    EE entre semillas)."""
    f = cifras_c5_fugas()
    por = [_fugas_semilla(s) for s in range(REPETICIONES["fugas"])]
    out = {}
    for ruta, sin, con in (("preprocesar", "preprocesar_antes", "ninguna"),
                           ("seleccion", "seleccion_previa", "seleccion_limpia")):
        dif_con = np.array([p[con][0] - p[con][1] for p in por])
        out[ruta] = {"sin": f[sin]["cv"][0], "con": f[con]["cv"][0], "uso": f[con]["uso"][0],
                     "dif_con": float(np.median(dif_con)),
                     "ee_entre_semillas": float(np.std(dif_con, ddof=1) / math.sqrt(len(por)))}
    cita = {r: {"sin": _f(v["sin"], 2), "con": _f(v["con"], 2), "uso": _f(v["uso"], 2)}
            for r, v in out.items()}
    return {**out, "cita": cita}


# ---------------------------------------------- P1 §6: imputacion ---

def datos_imputacion(semilla=SEMILLA):
    """Entregas (ENTREGAS_C5, n = 600) con 30 % de faltantes en distancia que dependen
    de y: las entregas largas faltan mas (faltar informa)."""
    with _silencio():
        return entregas_c5(n=600, semilla=semilla,
                           faltantes={"distancia": (0.3, "depende_y")})


def _phi_lineal_imputado(indicadora):
    ml = _ml()
    cols = ["distancia", "hora", "lluvia"] + (["distancia_falta"] if indicadora else [])
    return ml.columnas(*cols)


@functools.lru_cache(maxsize=None)
def cifras_c5_imputacion():
    """ml-c5-imputacion: (1) fraccion de filas de ent en la mediana tras imputar (el
    pico); (2) L_val del modelo lineal con y sin la indicadora; (3) pendiente de
    distancia con la mediana y con el centinela -5, mismo modelo lineal."""
    ml = _ml()
    d = datos_imputacion()
    imp = ml.imputar_simple(d.ent, ["distancia"])
    ent, val = imp.transformar(d.ent), imp.transformar(d.val)
    mediana = float(imp.valores["distancia"]) if hasattr(imp, "valores") else float(
        d.ent["distancia"].median())
    pico = float(np.mean(np.isclose(ent["distancia"].to_numpy(float), mediana)))
    with _silencio():
        m_con = ml.ajustar(ent, phi=_phi_lineal_imputado(True))
        m_sin = ml.ajustar(ent, phi=_phi_lineal_imputado(False))
        L_con, L_sin = float(ml.L(m_con, val)), float(ml.L(m_sin, val))
        cent = d.ent.copy()
        cent["distancia"] = cent["distancia"].fillna(-5.0)
        cent.attrs = d.ent.attrs
        m_cent = ml.ajustar(cent, phi=_phi_lineal_imputado(False))
        completos = d.ent.dropna(subset=["distancia"]).copy()
        completos.attrs = d.ent.attrs
        m_comp = ml.ajustar(completos, phi=_phi_lineal_imputado(False))
    b_med = float(m_sin.beta_gorro["distancia"])
    b_cent = float(m_cent.beta_gorro["distancia"])
    b_comp = float(m_comp.beta_gorro["distancia"])
    return {"mediana": mediana, "pico": pico, "L_con": L_con, "L_sin": L_sin,
            "pendiente_mediana": b_med, "pendiente_centinela": b_cent,
            "pendiente_completos": b_comp, "ent": ent, "datos": d,
            "cita": {"mediana": _f(mediana, 1), "pico": _f(100 * pico, 0) + " %",
                     "L_con": _f(L_con, 1), "L_sin": _f(L_sin, 1),
                     "pendiente_mediana": _f(b_med, 2), "pendiente_centinela": _f(b_cent, 2),
                     "pendiente_completos": _f(b_comp, 2)}}


# -------------------------------- P1 §6: escalar antes con MCO (control) ---

def _mco(X, y, mu=0.0):
    """Minimos cuadrados con intercepto (columna 0) sin penalizar; ridge en el resto."""
    if mu == 0:
        return np.linalg.pinv(X) @ y
    P = np.eye(X.shape[1])
    P[0, 0] = 0.0
    return np.linalg.solve(X.T @ X / len(y) + mu * P, X.T @ y / len(y))


@functools.lru_cache(maxsize=None)
def cifras_c5_escalar_mco():
    """ml-c5-obs-escalar-mco: diferencia maxima entre predicciones de validacion con el
    escalado global (todas las filas) y por entrenamiento: MCO con Phi de rango completo
    (~0), con mu > 0 (pequena, no nula), con imputacion mas indicadora (~0); y el
    contraejemplo de rango deficiente del contrato v3 §4.8 (0.5 contra 0.2)."""
    with _silencio():
        d = entregas_c5(n=600, semilla=SEMILLA)
        dm = datos_imputacion()
    cols = ["distancia", "hora", "lluvia"]

    def difmax(ent, val, mu, columnas):
        A, V = ent[columnas].to_numpy(float), val[columnas].to_numpy(float)
        y = ent["y"].to_numpy(float)
        todo = np.vstack([A, V])
        preds = []
        for base in (todo, A):
            c, s = base.mean(0), base.std(0)
            s[s == 0] = 1.0
            X = np.column_stack([np.ones(len(A)), (A - c) / s])
            Xv = np.column_stack([np.ones(len(V)), (V - c) / s])
            preds.append(Xv @ _mco(X, y, mu))
        return float(np.max(np.abs(preds[0] - preds[1])))

    mco = difmax(d.ent, d.val, 0.0, cols)
    ridge = difmax(d.ent, d.val, 1.0, cols)
    ent, val = dm.ent.copy(), dm.val.copy()
    med = float(np.nanmedian(np.r_[ent["distancia"], val["distancia"]]))
    for df in (ent, val):
        df["distancia_falta"] = df["distancia"].isna().astype(float)
        df["distancia"] = df["distancia"].fillna(med)
    imput = difmax(ent, val, 0.0, cols + ["distancia_falta"])
    # contraejemplo (rango deficiente)
    X1 = np.array([[1.0, 0, 0], [1, 1, 1]])
    y1 = np.array([0.0, 1.0])
    p1 = float(np.array([1.0, 1, 0]) @ np.linalg.pinv(X1) @ y1)
    X2 = np.array([[1.0, 0, 0], [1, 1, 2]])       # la tercera columna, multiplicada por 2
    p2 = float(np.array([1.0, 1, 0]) @ np.linalg.pinv(X2) @ y1)
    return {"mco": mco, "ridge": ridge, "imputacion": imput, "contra_1": p1, "contra_2": p2,
            "cita": {"ridge": f"{ridge:.2g}"}}


# --------------------------------------------- P2 §2: la trampa de la dummy ---

ZONAS_DUMMY = ("norte", "centro", "sur", "norte", "centro", "sur")
DISTANCIAS_DUMMY = (1.0, 2.0, 3.0, 4.0, 2.5, 1.5)
MU_DUMMY = 0.1


@functools.lru_cache(maxsize=None)
def cifras_c5_dummy():
    """ml-c5-trampa-dummy: Phi de seis pedidos con 1, norte, centro, sur y distancia;
    rango 4 de 5; dos beta distintos con las mismas predicciones; el unico de ridge
    (intercepto sin penalizar, mu = MU_DUMMY)."""
    z = np.array(ZONAS_DUMMY)
    dist = np.array(DISTANCIAS_DUMMY)
    efecto = {"norte": 0.0, "centro": 3.0, "sur": 12.0}
    y = 10 + 4 * dist + np.array([efecto[v] for v in z])
    y = y + np.array([0.4, -0.3, 0.2, -0.5, 0.3, -0.1])
    Phi = np.column_stack([np.ones(6), z == "norte", z == "centro", z == "sur", dist]).astype(float)
    rango = int(np.linalg.matrix_rank(Phi))
    b1 = np.linalg.pinv(Phi) @ y
    b2 = b1 + 10.0 * np.array([1.0, -1, -1, -1, 0])
    yh1, yh2 = Phi @ b1, Phi @ b2
    P = np.eye(5)
    P[0, 0] = 0
    br = np.linalg.solve(Phi.T @ Phi / 6 + MU_DUMMY * P, Phi.T @ y / 6)
    nombres = ("1", "norte", "centro", "sur", "distancia")
    cita = {"rango": f"{rango} de 5",
            "b1": [_f(v, 1) for v in b1], "b2": [_f(v, 1) for v in b2],
            "yh": [_f(v, 1) for v in yh1], "ridge": [_f(v, 1) for v in br]}
    return {"Phi": Phi, "y": y, "rango": rango, "b1": b1, "b2": b2, "ridge": br,
            "max_dif_pred": float(np.max(np.abs(yh1 - yh2))), "nombres": nombres,
            "cita": cita}


# ------------------------------------------------ P2 §3: diagnostico ---

NS_DIAG = (40, 80, 160, 320)


def _proceso_clientes(n, semilla):
    """Entregas con clientes que repiten (40 clientes, desv del cliente 4)."""
    ml = _ml()
    return ml.PROCESOS["entregas_curvas"](
        n=n, semilla=semilla, ruido=ml.efecto_grupo(40, 4.0, 1.0), fracciones=(1, 0, 0))


def _vecinos_x(df):
    """Vecinos (5) sobre la distancia y el numero de cliente: reconoce al cliente."""
    return _ml().ajustar_otro(df, familia="vecinos", n_vecinos=5, columnas_x=["x", "grupo"])


@functools.lru_cache(maxsize=None)
def cifras_c5_diagnostico():
    """ml-c5-diagnostico. Izquierda: la curva de aprendizaje de vecinos (5, sobre la
    distancia y el numero de cliente) sobre entregas
    con clientes que repiten: L_ent y la CV al azar contra la CV por grupos, por n
    (mediana y RIC de REPETICIONES["diagnostico"] muestras). Derecha: dos procesos
    altos y juntos: la recta sobre las entregas curvas (lejos del piso) y la recta sobre
    las entregas rectas con mucho ruido (sobre el piso)."""
    ml = _ml()
    izq = {"L_ent": {}, "azar": {}, "grupos": {}}
    with _silencio():
        for n in NS_DIAG:
            vals = {k: [] for k in izq}
            for s in range(REPETICIONES["diagnostico"]):
                d = _proceso_clientes(n, s)
                df = d.ent
                vals["L_ent"].append(float(ml.L(_vecinos_x(df), df)))
                vals["azar"].append(ml.validacion_cruzada(df, _vecinos_x).media)
                vals["grupos"].append(ml.validacion_cruzada(df, _vecinos_x,
                                                            particion="grupo").media)
            for k in izq:
                izq[k][n] = _mediana_ric(vals[k])
        der = {}
        for nombre, fab in (
                ("sesgo", lambda n, s: ml.PROCESOS["entregas_curvas"](
                    n=n, semilla=s, fracciones=(1, 0, 0), sigma_e=3.0)),
                ("piso", lambda n, s: ml.PROCESOS["entregas"](
                    n=n, semilla=s, fracciones=(1, 0, 0), sigma_e=4.0))):
            vals = {"L_ent": {}, "cv": {}}
            for n in NS_DIAG:
                le, cv = [], []
                for s in range(REPETICIONES["diagnostico"]):
                    df = fab(n, s).ent
                    le.append(float(ml.L(ml.ajustar(df), df)))
                    cv.append(ml.validacion_cruzada(df, lambda x: ml.ajustar(x)).media)
                vals["L_ent"][n], vals["cv"][n] = _mediana_ric(le), _mediana_ric(cv)
            vals["piso"] = float(ml.piso(fab(100, 0)))
            der[nombre] = vals
    nmax = NS_DIAG[-1]
    brecha_azar = izq["grupos"][nmax][0] - izq["L_ent"][nmax][0]
    brecha_azar_cv = izq["azar"][nmax][0] - izq["L_ent"][nmax][0]
    rel = {k: der[k]["cv"][nmax][0] / der[k]["piso"] - 1 for k in der}
    cita = {"azar": _f(izq["azar"][nmax][0], 1), "grupos": _f(izq["grupos"][nmax][0], 1),
            "L_ent": _f(izq["L_ent"][nmax][0], 1),
            "sesgo_sobre_piso": _f(100 * rel["sesgo"], 0) + " %",
            "piso_sobre_piso": _f(100 * rel["piso"], 0) + " %",
            "repeticiones": str(REPETICIONES["diagnostico"])}
    return {"izq": izq, "der": der, "brecha_grupos": brecha_azar,
            "brecha_azar": brecha_azar_cv, "rel": rel, "cita": cita}


# -------------------------------------------- P2 §3: prueba de depuracion ---

@functools.lru_cache(maxsize=None)
def cifras_c5_depurar(mu=0.0):
    """Recta con intercepto sobre x = 0..9, y = x^2: minimo del error cuadratico medio
    exacto (264/5 = 52.8); la phi cuadratica sobre las mismas filas llega a 0 (con
    mu = 0; con mu > 0 ya no)."""
    xs = list(range(10))
    ys = [x * x for x in xs]
    n = Fraction(len(xs))
    mx = sum(map(Fraction, xs)) / n
    my = sum(map(Fraction, ys)) / n
    sxy = sum((Fraction(x) - mx) * (Fraction(y) - my) for x, y in zip(xs, ys))
    sxx = sum((Fraction(x) - mx) ** 2 for x in xs)
    b1 = sxy / sxx
    b0 = my - b1 * mx
    mse = sum((Fraction(y) - b0 - b1 * x) ** 2 for x, y in zip(xs, ys)) / n
    X = np.column_stack([np.ones(10), xs, np.square(xs)]).astype(float)
    b = _mco(X, np.array(ys, float), mu)
    mse_q = float(np.mean((X @ b - np.array(ys, float)) ** 2))
    return {"mse_recta": mse, "mse_cuadratica": mse_q,
            "cita": {"mse_recta": "52.8"}}


# ------------------------------------------------- P2 §4: arboles ---

PROFUNDIDADES_ARBOL = (1, 3, 6)


@functools.lru_cache(maxsize=None)
def datos_diagonal():
    """La frontera x2 > x1 en el cuadrado (puntaje 40·(x2 − x1))."""
    ml = _ml()
    with _silencio():
        return ml.proceso_clasificacion(
            n=600, x={"x1": ml.uniforme(0, 1), "x2": ml.uniforme(0, 1)},
            puntaje=lambda d: 40 * (d["x2"] - d["x1"]), semilla=SEMILLA)


def arbol_diagonal(p):
    return _ml().ajustar_otro(datos_diagonal().ent, familia="arbol", profundidad=p)


@functools.lru_cache(maxsize=None)
def cifras_c5_arbol():
    """ml-c5-arbol-escalones: MCC en validacion de arboles de profundidad 1, 3 y 6 sobre
    la diagonal, y el de la logistica lineal."""
    ml = _ml()
    d = datos_diagonal()
    y = d.val["y"].to_numpy()
    res = {p: ml.mcc(y, arbol_diagonal(p).predecir(d.val), clases=d.clases)
           for p in PROFUNDIDADES_ARBOL}
    with _silencio():
        log = ml.ajustar(d.ent)
    res_log = ml.mcc(y, log.predecir(d.val), clases=d.clases)
    return {"mcc": res, "logistica": res_log,
            "cita": {"mcc": {str(p): _f(v, 2) for p, v in res.items()},
                     "logistica": _f(res_log, 2)}}


PROF_CURVA = tuple(range(1, 13))
ETAPAS_CURVA = (1, 2, 5, 10, 20, 50, 100, 200, 400)
B_CURVA = (1, 2, 5, 10, 20, 50, 100, 200)


@functools.lru_cache(maxsize=None)
def datos_familias():
    """Las entregas curvas de una variable (distancia), n = 300."""
    with _silencio():
        return _ml().PROCESOS["entregas_curvas"](n=300, semilla=SEMILLA)


def _bosque_sk(B, semilla):
    """Un bosque con B arboles y semilla propia (ml_lab fija random_state=0): solo para
    medir cuanto difieren las semillas del bosque con los mismos datos."""
    from sklearn.ensemble import RandomForestRegressor

    class _B:
        def __init__(self, df):
            self.est = RandomForestRegressor(n_estimators=B, random_state=semilla, n_jobs=1)
            self.est.fit(df[["x"]].to_numpy(float), df["y"].to_numpy(float))

    return _B


@functools.lru_cache(maxsize=None)
def cifras_c5_familias():
    """ml-c5-familias-capacidad y P2 §4: profundidad del arbol y etapas de boosting que
    elige la CV (minimo); la CV del bosque con B = 10 y B = 200 en cinco semillas del
    bosque (mismos datos, misma particion): mediana y rango."""
    ml = _ml()
    d = datos_familias()
    with _silencio():
        cv_arbol = {p: ml.validacion_cruzada(
            d, lambda df, p=p: ml.ajustar_otro(df, familia="arbol", profundidad=p))
            for p in PROF_CURVA}
        cv_boost = {e: ml.validacion_cruzada(
            d, lambda df, e=e: ml.ajustar_otro(df, familia="boosting", etapas=e, tasa=0.1))
            for e in ETAPAS_CURVA}
        dev = ml._desarrollo(d)
        part = ml.pliegues(dev, k=5, como="azar", semilla=SEMILLA)
        bosque = {}
        for B in B_CURVA:
            por_sem = []
            for s in range(REPETICIONES["familias"]):
                errs = []
                for a, v in part:
                    m = _bosque_sk(B, s)(dev.iloc[a]).est
                    p = m.predict(dev.iloc[v][["x"]].to_numpy(float))
                    errs.append(float(np.mean((dev.iloc[v]["y"].to_numpy(float) - p) ** 2)))
                por_sem.append(float(np.mean(errs)))
            bosque[B] = por_sem
    p_el = min(cv_arbol, key=lambda p: cv_arbol[p].media)
    e_el = min(cv_boost, key=lambda e: cv_boost[e].media)
    rango = {B: float(np.ptp(v)) for B, v in bosque.items()}
    cita = {"profundidad": str(p_el), "etapas": str(e_el),
            "bosque_10": _f(np.median(bosque[10]), 1), "bosque_200": _f(np.median(bosque[200]), 1),
            "rango_10": _f(rango[10], 2), "rango_200": _f(rango[200], 2)}
    return {"cv_arbol": cv_arbol, "cv_boost": cv_boost, "bosque": bosque, "rango": rango,
            "profundidad": p_el, "etapas": e_el, "cita": cita}


@functools.lru_cache(maxsize=None)
def cifras_c5_bagging(B=10, corr=0.3):
    """Varianza del promedio de B variables de varianza 1 con correlacion corr: simulada
    (REPETICIONES["bagging"]) contra la formula corr + (1 − corr)/B."""
    rng = np.random.default_rng([SEMILLA, 56])
    S = np.full((B, B), corr) + (1 - corr) * np.eye(B)
    L_ = np.linalg.cholesky(S)
    z = rng.standard_normal((REPETICIONES["bagging"], B)) @ L_.T
    sim = float(np.var(z.mean(1), ddof=1))
    formula = corr + (1 - corr) / B
    return {"simulada": sim, "formula": formula,
            "cita": {"simulada": _f(sim, 3), "formula": _f(formula, 2)}}


# ------------------------------------------------- P2 §5: Cybenko ---

UNIDADES = (1, 3, 10)


def f_cybenko(x):
    """La curva del panel «existe»: una joroba y una subida en [0, 1]."""
    x = np.asarray(x, float)
    return np.sin(3 * np.pi * x) + 2 * x


def _sigmoides(theta, x, h):
    b0, b, g0, g = theta[0], theta[1:h + 1], theta[h + 1:2 * h + 1], theta[2 * h + 1:]
    z = g0[None, :] + np.outer(x, g)
    return b0 + (1 / (1 + np.exp(-np.clip(z, -50, 50)))) @ b


def ajustar_sigmoides(h, semilla, x=None, y=None):
    """Minimos cuadrados no lineales (scipy) de b0 + sum_h b_h·σ(γ0h + γh x) en una
    rejilla sin ruido; un arranque al azar. Devuelve la funcion ajustada y su error max."""
    from scipy.optimize import least_squares
    x = np.linspace(0, 1, 201) if x is None else x
    y = f_cybenko(x) if y is None else y
    rng = np.random.default_rng([semilla, 57, h])
    theta0 = np.r_[0.0, rng.normal(0, 1, h), rng.normal(0, 5, h), rng.normal(0, 10, h)]
    def jac(t):
        b, g0, g = t[1:h + 1], t[h + 1:2 * h + 1], t[2 * h + 1:]
        s = 1 / (1 + np.exp(-np.clip(g0[None, :] + np.outer(x, g), -50, 50)))
        ds = s * (1 - s) * b[None, :]
        return np.column_stack([np.ones(len(x)), s, ds, ds * x[:, None]])

    r = least_squares(lambda t: _sigmoides(t, x, h) - y, theta0, jac=jac, max_nfev=2000)
    t = r.x
    return (lambda xx, t=t: _sigmoides(t, np.asarray(xx, float), h)), float(
        np.max(np.abs(_sigmoides(t, x, h) - y)))


NS_ANILLOS = (100, 200, 400, 800, 1600, 3200)
CERCA_DEL_PISO = 1.15  # DECISION prog-c5-6: con 10 % la aprendida no llega en 3 200 filas
UNIDADES_ANILLOS = 10


def _cv_log_anillos(n, modo, semilla):
    """CV_5 de perdida logaritmica en los anillos: logistica sobre la phi polar, o una
    capa de UNIDADES_ANILLOS sigmoides aprendida con la logistica encima (MLP)."""
    from sklearn.model_selection import StratifiedKFold
    ml = _ml()
    d = ml.anillos(n=n, fracciones=(1, 0, 0), semilla=semilla)
    df = d.ent
    X = df[["x1", "x2"]].to_numpy(float)
    y = (df["y"].to_numpy() == d.clases[1]).astype(int)
    perd = []
    for a, v in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
        if modo == "polar":
            with _silencio():
                m = ml.ajustar(df.iloc[a], phi=ml.polares())
            p = np.asarray(m.predecir_p(df.iloc[v]), float)
        else:
            from sklearn.neural_network import MLPClassifier
            ps = []
            for arr in range(REPETICIONES["cybenko_anillos"]):
                red = MLPClassifier((UNIDADES_ANILLOS,), activation="logistic",
                                    solver="lbfgs", alpha=1e-3, max_iter=2000,
                                    random_state=arr)
                with _silencio():
                    red.fit(X[a], y[a])
                ps.append(red.predict_proba(X[v])[:, 1])
            pv = np.clip(np.asarray(ps), 1e-15, 1 - 1e-15)
            ls = [-np.mean(y[v] * np.log(q) + (1 - y[v]) * np.log(1 - q)) for q in pv]
            perd.append(float(np.median(ls)))
            continue
        p = np.clip(p, 1e-15, 1 - 1e-15)
        perd.append(float(-np.mean(y[v] * np.log(p) + (1 - y[v]) * np.log(1 - p))))
    return float(np.mean(perd))


@functools.lru_cache(maxsize=None)
def cifras_c5_cybenko():
    """Envoltura de _cifras_c5_cybenko con BLAS en un solo hilo.

    Los ajustes no convexos (least_squares, MLP con lbfgs) llegan a puntos distintos
    según cuántos hilos use BLAS: con OMP_NUM_THREADS=2 la curva de ml-c5-cybenko se
    movía un píxel y el SVG dejaba de ser el del generador. Con un hilo, el orden de
    las sumas no depende de la máquina."""
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1):
        return _cifras_c5_cybenko()


def _cifras_c5_cybenko():
    """ml-c5-cybenko: error maximo con 1, 3 y 10 unidades sin ruido (mediana de cinco
    arranques); en los anillos, CV de perdida logaritmica contra n de la phi polar y de
    10 sigmoides aprendidas (cada ajuste, mediana de REPETICIONES["cybenko_anillos"]
    arranques), y el n mas chico con el que cada una queda a menos de 15 % del piso."""
    ml = _ml()
    errores, ajustes = {}, {}
    for h in UNIDADES:
        corridas = [ajustar_sigmoides(h, s) for s in range(REPETICIONES["cybenko"])]
        errs = [e for _, e in corridas]
        orden = int(np.argsort(errs)[len(errs) // 2])
        errores[h] = float(np.median(errs))
        ajustes[h] = corridas[orden][0]
    d = ml.anillos(n=400, semilla=SEMILLA)
    real = d.realidad
    p = np.clip(real["prob"].to_numpy(float), 1e-15, 1 - 1e-15)
    uno = (real["y"].to_numpy() == d.clases[1]).astype(float)
    piso = float(-np.mean(uno * np.log(p) + (1 - uno) * np.log(1 - p)))
    curvas = {m: {n: _cv_log_anillos(n, m, SEMILLA) for n in NS_ANILLOS}
              for m in ("polar", "aprendida")}
    llega = {}
    for m, c in curvas.items():
        ok = [n for n in NS_ANILLOS if c[n] <= CERCA_DEL_PISO * piso]
        llega[m] = ok[0] if ok else None
    cita = {"error": {str(h): _f(e, 2) for h, e in errores.items()},
            "piso": _f(piso, 3), "n_polar": str(llega["polar"]),
            "n_aprendida": str(llega["aprendida"])}
    return {"errores": errores, "ajustes": ajustes, "piso": piso, "curvas": curvas,
            "llega": llega, "cita": cita}


# ------------------------------------------- P2: ejercicio final ---

@functools.lru_cache(maxsize=None)
def datos_final_p2():
    """2 000 pedidos de 300 clientes (entregas curvas con efecto del cliente)."""
    ml = _ml()
    e = ESCENARIOS["p2_final"]
    with _silencio():
        return ml.PROCESOS["entregas_curvas"](
            n=e["pedidos"], semilla=SEMILLA, fracciones=(1, 0, 0),
            ruido=ml.efecto_grupo(e["clientes"], 6.0, 2.0), despliegue="grupos_nuevos")


@functools.lru_cache(maxsize=None)
def cifras_c5_final_metodologia():
    """La tabla de 4 filas del ejercicio final de P2 (MAE, minutos): bosque sin tope (con
    la distancia y el numero de cliente como columnas) y
    lineal, cada uno con CV al azar y por grupos; L_ent del bosque y el benchmark de la
    media (CV de la media, por grupos)."""
    ml = _ml()
    d = datos_final_p2()
    # el compañero le da al bosque el numero de cliente como una columna mas
    bosque = lambda df: ml.ajustar_otro(df, familia="bosque", n_arboles=100,  # noqa: E731
                                        columnas_x=["x", "grupo"])
    lineal = lambda df: ml.ajustar(df)  # noqa: E731
    media = lambda df: ml.ajustar(df, phi=ml.polinomio(0))  # noqa: E731
    tabla = {}
    with _silencio():
        for nombre, m in (("bosque", bosque), ("lineal", lineal)):
            for part in ("azar", "grupo"):
                tabla[(nombre, part)] = ml.validacion_cruzada(
                    d, m, particion=part, criterio="absoluta").media
        L_ent = float(ml.evaluar(bosque(d.ent), d.ent, "absoluta"))
        bench = ml.validacion_cruzada(d, media, particion="grupo", criterio="absoluta").media
    cita = {f"{a}_{b}": _f(v, 1) for (a, b), v in tabla.items()}
    cita.update({"L_ent": _f(L_ent, 1), "benchmark": _f(bench, 1)})
    return {"tabla": tabla, "L_ent": L_ent, "benchmark": bench, "cita": cita}
