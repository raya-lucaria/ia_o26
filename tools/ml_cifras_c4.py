"""Cifras de la clase 4 de la unidad de aprendizaje de maquina (unidad 9).

Una funcion por hecho que cita una pagina, un notebook o una figura de la
clase 4 (clase_4.md §10.7, tabla de ml_cifras_c4). Ninguna cifra se escribe a
mano: la pagina la copia de aqui, tools/test_ml_cifras_c4.py la fija en la
fuente y tools/test_ml_prosa_c4.py la busca en la pagina que la cita
(D-009.5, D-003).

Cada funcion devuelve un dict con los valores crudos y, en la clave "cita",
las formas literales con que la pagina y las figuras los escriben (cadenas ya
redondeadas). Las funciones se guardan en cache: la suite y el generador de
figuras las llaman muchas veces y algunas cuestan segundos.

Los procesos hilo salen de ml_lab, nunca se redefinen aqui (§10.3, v4):
PROCESOS["fraude"] y PROCESOS["mensajes3"], el caso 17 y el caso 25. Los
datos_* de este modulo son los mismos que dibujan tools/figuras_ml_c4.py y
los notebooks 08 y 09: una sola fuente por proceso.

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


def _ml():
    """tools/aprendizaje_maquina.py (ml_lab), importado al pedirlo."""
    return importlib.import_module("aprendizaje_maquina")


def _f(v, d):
    """La forma con que la pagina escribe un numero: d decimales."""
    return f"{float(v):.{d}f}"


@contextlib.contextmanager
def _silencio():
    """Los avisos de ml_lab (separables, soporte nulo) no son cifras."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


def _entropia(p):
    return -p * math.log(p) - (1 - p) * math.log(1 - p)


def _mcc_conteos(vp, fp, fn, vn):
    """MCC binario de cuatro conteos (0 si un factor del denominador es 0)."""
    den = (vp + fp) * (vp + fn) * (vn + fp) * (vn + fn)
    return 0.0 if den == 0 else (vp * vn - fp * fn) / math.sqrt(den)


def _mcc_esperado(prob, regla):
    """MCC poblacional de una regla binaria: conteos esperados con la prob verdadera.

    prob = Pr(y = 1 | x) en la muestra enorme; regla, booleana (anuncia 1). Usar la
    probabilidad en lugar de la etiqueta sorteada quita el ruido de las etiquetas.
    """
    prob = np.asarray(prob, float)
    r = np.asarray(regla, bool)
    vp = prob[r].sum()
    fp = (1 - prob[r]).sum()
    fn = prob[~r].sum()
    vn = (1 - prob[~r]).sum()
    return _mcc_conteos(vp, fp, fn, vn)


def _metricas_esperadas(prob, regla):
    """MCC, A_bal y A poblacionales de una regla binaria (conteos esperados)."""
    prob = np.asarray(prob, float)
    r = np.asarray(regla, bool)
    vp, fp = prob[r].sum(), (1 - prob[r]).sum()
    fn, vn = prob[~r].sum(), (1 - prob[~r]).sum()
    n = len(prob)
    return {"mcc": _mcc_conteos(vp, fp, fn, vn),
            "aciertos_balanceados": 0.5 * (vp / (vp + fn) + vn / (vn + fp)),
            "aciertos": (vp + vn) / n}


PHI_LINEAL = ("x1", "x2")
PHI_CUADRATICA = ("x1", "x2", "x1**2", "x2**2", "x1*x2")
MUS_CV = (1.0, 0.1, 0.01, 1e-3, 1e-4)  # de simple a complejo (μ decreciente)


def phi_lineal():
    ml = _ml()
    return ml.estandarizar(ml.columnas(*PHI_LINEAL))


def phi_cuadratica():
    ml = _ml()
    return ml.estandarizar(ml.columnas(*PHI_CUADRATICA))


def construir_logistica(mu, pesos=None, cuadratica=False):
    """La logística (o softmax) con φ estandarizada en cada ajuste, l2 con μ."""
    ml = _ml()

    def construir(df):
        phi = phi_cuadratica() if cuadratica else phi_lineal()
        with _silencio():
            return ml.ajustar(df, phi=phi, mu=mu, penalizacion="l2" if mu > 0 else None,
                              pesos=pesos, tarea="clasificacion")
    return construir


def mu_por_cv(df, pesos=None, cuadratica=False, mus=MUS_CV, k=5):
    """μ elegido por CV estratificada SOLO sobre df (el ent), con la pérdida sin pesos."""
    ml = _ml()
    cands = {mu: construir_logistica(mu, pesos, cuadratica) for mu in mus}
    with _silencio():
        el = ml.elegir(df, cands, con="cv", k=k, particion="estratificado",
                       criterio="logaritmica")
    return float(el.elegido)


# ======================================================== exactas · P1 ===

@functools.lru_cache(maxsize=None)
def cifras_c4_moda():
    """La moda con 1 % y 2 % (población) y la entropía del benchmark de proporción."""
    ml = _ml()
    out = {}
    for p in (0.01, 0.02):
        n1 = int(round(p * 10_000))
        y = np.r_[np.ones(n1, int), np.zeros(10_000 - n1, int)]
        yg = np.zeros_like(y)
        with _silencio():
            out[p] = {"aciertos": float(ml.aciertos(y, yg)),
                      "aciertos_balanceados": float(ml.aciertos_balanceados(y, yg, clases=[0, 1])),
                      "mcc": float(ml.mcc(y, yg, clases=[0, 1]))}
    ent = {p: _entropia(p) for p in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01)}
    cita = {"uno": {k: _f(v, 2) if k != "mcc" else "0" for k, v in out[0.01].items()},
            "dos": {k: _f(v, 2) if k != "mcc" else "0" for k, v in out[0.02].items()},
            "entropia": {p: _f(v, 3) for p, v in ent.items()}}
    cita["uno"]["aciertos_balanceados"] = "0.5"
    cita["dos"]["aciertos_balanceados"] = "0.5"
    return {"moda": out, "entropia": ent, "cita": cita}


Y_DOS_REGLAS = (0, 0, 1, 1)
P_REGLA_A = (0.01, 0.01, 0.49, 0.99)
P_REGLA_B = (0.40, 0.40, 0.60, 0.60)


@functools.lru_cache(maxsize=None)
def cifras_c4_dos_reglas():
    """El micro ml-c4-ej-dos-reglas: pérdida, A y MCC de las reglas A y B con τ = 0.5."""
    ml = _ml()
    y = np.array(Y_DOS_REGLAS)
    out = {}
    for nombre, p in (("A", P_REGLA_A), ("B", P_REGLA_B)):
        p = np.array(p)
        yg = (p >= 0.5).astype(int)
        out[nombre] = {"perdida": float(ml.log_loss(y, p)), "aciertos": float(ml.aciertos(y, yg)),
                       "mcc": float(ml.mcc(y, yg))}
    cita = {k: {"perdida": _f(v["perdida"], 3), "aciertos": _f(v["aciertos"], 2).rstrip("0").rstrip("."),
                "mcc": _f(v["mcc"], 3).rstrip("0").rstrip(".")} for k, v in out.items()}
    cita["A"]["aciertos"] = "0.75"
    return {**out, "cita": cita}


def p_ponderada(eta, razon):
    """p^w del teorema de los pesos: razon = w1/w0."""
    return razon * eta / (razon * eta + (1 - eta))


@functools.lru_cache(maxsize=None)
def cifras_c4_pesos_punto():
    """El ejemplo del teorema: η = 0.1, w1/w0 = 9 da p^w = 0.5; umbral equivalente 1/10."""
    pw = p_ponderada(0.1, 9)
    umbral = 1 / (1 + 9)
    return {"p_w": pw, "umbral": umbral, "cita": {"p_w": _f(pw, 2), "umbral": "0.1"}}


@functools.lru_cache(maxsize=None)
def cifras_c4_pesos_balanceados():
    """El micro ml-c4-ej-pesos-balanceados: 950 legítimos y 50 fraudes."""
    ml = _ml()
    y = np.r_[np.zeros(950, int), np.ones(50, int)]
    w = ml.pesos_de_clase(y)
    w = {int(k): float(v) for k, v in dict(w).items()}
    suma = 950 * w[0] + 50 * w[1]
    umbral = w[0] / (w[0] + w[1])
    return {"w0": w[0], "w1": w[1], "suma": suma, "umbral": umbral,
            "cita": {"w0": _f(w[0], 3), "w1": f"{w[1]:g}", "suma": f"{suma:.0f}",
                     "umbral": _f(umbral, 2)}}


@functools.lru_cache(maxsize=None)
def cifras_c4_cliente_tipico():
    """Con Pr(y=1) = 0.05 y pesos balanceados: razón 19 y p^w = 0.5 para η = 0.05."""
    razon = 0.95 / 0.05
    pw = p_ponderada(0.05, razon)
    return {"razon": razon, "p_w": pw, "cita": {"razon": f"{razon:.0f}", "p_w": _f(pw, 1)}}


@functools.lru_cache(maxsize=None)
def cifras_c4_mcc_un_fraude():
    """El micro ml-c4-ej-mcc-un-fraude: pliegos A (VP 1, FP 2, VN 97) y B (FN 1, VN 99)."""
    ml = _ml()

    def pliegue(vp, fp, fn, vn):
        y = np.r_[np.ones(vp + fn, int), np.zeros(fp + vn, int)]
        yg = np.r_[np.ones(vp, int), np.zeros(fn, int), np.ones(fp, int), np.zeros(vn, int)]
        with _silencio():
            return {"mcc": float(ml.mcc(y, yg, clases=[0, 1])),
                    "aciertos_balanceados": float(ml.aciertos_balanceados(y, yg, clases=[0, 1]))}
    a = pliegue(1, 2, 0, 97)
    b = pliegue(0, 0, 1, 99)
    return {"A": a, "B": b, "fraudes_por_pliegue_k5": 10 // 5,
            "cita": {"A": {"mcc": _f(a["mcc"], 3), "aciertos_balanceados": _f(a["aciertos_balanceados"], 3)},
                     "B": {"mcc": "0", "aciertos_balanceados": "0.5"}}}


@functools.lru_cache(maxsize=None)
def cifras_c4_quien_manda():
    """El micro ml-c4-ej-quien-manda: 98/1.5/0.5 y la regla constante en la clase 0."""
    ml = _ml()
    y = np.r_[np.zeros(980, int), np.ones(15, int), np.full(5, 2)]
    yg = np.zeros_like(y)
    with _silencio():
        pc = ml.por_clase("aciertos", y, yg, clases=[0, 1, 2])
        macro = float(ml.promediar("aciertos", y, yg, "macro", clases=[0, 1, 2]))
        pond = float(ml.promediar("aciertos", y, yg, "ponderado", clases=[0, 1, 2]))
        mcc = float(ml.mcc(y, yg, clases=[0, 1, 2]))
    por = tuple(float(v) for v in pc)
    return {"por_clase": por, "macro": macro, "ponderado": pond, "mcc": mcc,
            "cita": {"por_clase": "(1, 0, 0)", "macro": "1/3", "ponderado": _f(pond, 2), "mcc": "0"}}


# Ejemplo de noticias (deck 07·60, recalculado): Tecnología 100, Salud 60, Deporte 20.
# Renglones = verdad, columnas = lo anunciado. Los aciertos por clase, la precisión
# por clase y el MCC multiclase solo dependen de la diagonal y de los totales.
MATRIZ_NOTICIAS = ((90, 5, 5), (10, 40, 10), (5, 5, 10))
CLASES_NOTICIAS = ("Tecnología", "Salud", "Deporte")


def y_noticias():
    y, yg = [], []
    for i, fila in enumerate(MATRIZ_NOTICIAS):
        for j, n in enumerate(fila):
            y += [i] * n
            yg += [j] * n
    return np.array(y), np.array(yg)


@functools.lru_cache(maxsize=None)
def cifras_c4_noticias():
    """El ejemplo de noticias: aciertos por clase, macro, ponderado, MCC y precisión."""
    ml = _ml()
    y, yg = y_noticias()
    cl = [0, 1, 2]
    ac = tuple(float(v) for v in ml.por_clase("aciertos", y, yg, clases=cl))
    pr = tuple(float(v) for v in ml.por_clase("precision", y, yg, clases=cl))
    macro = float(ml.promediar("aciertos", y, yg, "macro", clases=cl))
    pond = float(ml.promediar("aciertos", y, yg, "ponderado", clases=cl))
    mcc = float(ml.mcc(y, yg, clases=cl))
    soporte = tuple(int(sum(f)) for f in MATRIZ_NOTICIAS)
    return {"aciertos": ac, "precision": pr, "macro": macro, "ponderado": pond, "mcc": mcc,
            "soporte": soporte,
            "cita": {"aciertos": tuple(_f(v, 3) for v in ac), "precision": tuple(_f(v, 3) for v in pr),
                     "macro": _f(macro, 3), "ponderado": _f(pond, 3), "mcc": _f(mcc, 3),
                     "soporte": "100/60/20"}}


@functools.lru_cache(maxsize=None)
def cifras_c4_final_p1():
    """El ejercicio final de la página 1: triaje 900/80/20."""
    n = {0: 900, 1: 80, 2: 20}
    tot = sum(n.values())
    w = {y: tot / (3 * ny) for y, ny in n.items()}
    return {"moda": {"aciertos": 0.9, "aciertos_balanceados": 1 / 3, "mcc": 0.0}, "w": w,
            "raros_por_pliegue_k5": n[2] // 5,
            "cita": {"moda": ("0.9", "1/3", "0"), "w": (_f(w[0], 3), _f(w[1], 2), _f(w[2], 1)),
                     "raros_por_pliegue_k5": "4"}}


@functools.lru_cache(maxsize=None)
def cifras_c4_bootstrap_aciertos_exacto():
    """El contraejemplo 90/10 con la regla constante: EE estratificado 0, por filas 0.030."""
    p = 0.9
    return {"ee_estratificado": 0.0, "ee_filas": math.sqrt(p * (1 - p) / 100),
            "cita": {"ee_estratificado": "0", "ee_filas": _f(math.sqrt(p * (1 - p) / 100), 3)}}


# ======================================================== exactas · P2 ===

C_CINCO = (0.1, 0.2, 0.4, 0.6, 0.8)
P_NUEVO = (0.45, 0.35, 0.20)


def rango_conformal(n_cal, delta):
    """⌈(n_cal + 1)(1 − δ)⌉ con aritmética exacta (la misma regla que ml._rango_conformal)."""
    return math.ceil(Fraction(n_cal + 1) * (1 - Fraction(delta).limit_denominator(10_000)))


@functools.lru_cache(maxsize=None)
def cifras_c4_cinco_puntajes():
    """El micro de los cinco puntajes: δ = 1/3 da {0}; δ = 1/6 da {0, 1, 2}."""
    ml = _ml()
    out = {}
    c = sorted(C_CINCO)
    puntajes_nuevo = tuple(round(1 - p, 10) for p in P_NUEVO)
    for nombre, delta in (("tercio", Fraction(1, 3)), ("sexto", Fraction(1, 6))):
        pos = int(ml._rango_conformal(len(c), delta))
        corte = c[pos - 1] if pos <= len(c) else math.inf
        conj = tuple(y for y, s in enumerate(puntajes_nuevo) if s <= corte + 1e-12)
        out[nombre] = {"posicion": pos, "corte": corte, "conjunto": conj}
    return {**out, "puntajes_nuevo": puntajes_nuevo,
            "cita": {"tercio": ("4", "0.6", "{0}"), "sexto": ("5", "0.8", "{0,1,2}")}}


@functools.lru_cache(maxsize=None)
def cifras_c4_minimo_por_clase():
    """El mínimo de casos de una clase en calibración con δ = 0.1: 9."""
    ml = _ml()
    n = 1
    while int(ml._rango_conformal(n, Fraction(1, 10))) > n:
        n += 1
    return {"minimo": n, "cita": {"minimo": str(n)}}


@functools.lru_cache(maxsize=None)
def cifras_c4_noventa_global():
    """El micro ml-c4-ej-noventa-global: 0.90 global, 0.91 en las clases de 98 %."""
    resto = Fraction(98, 100) * Fraction(91, 100)
    fraude = (Fraction(90, 100) - resto) / Fraction(2, 100)
    return {"parcial": float(resto), "falta": float(Fraction(90, 100) - resto),
            "fraude": float(fraude),
            "cita": {"parcial": "0.8918", "falta": "0.0082", "fraude": _f(fraude, 2)}}


@functools.lru_cache(maxsize=None)
def cifras_c4_tasa():
    """La tasa de equilibrio p/(1 − p) del cliente típico sin pesos (0.05) y con pesos (0.5)."""
    sin = 0.05 / 0.95
    con = 0.5 / 0.5
    return {"sin": sin, "con": con, "p_sin": 0.05, "p_con": 0.5,
            "cita": {"sin": _f(sin, 3), "con": "1", "con_pct": "100 %"}}


# =================================================== procesos de la clase ===

def datos_fraude(proporcion, n=600, semilla=0, **cambios):
    """PROCESOS["fraude"] de ml_lab, sin redefinirlo (§10.3)."""
    return _ml().PROCESOS["fraude"](n=n, semilla=semilla, proporcion=proporcion, **cambios)


def datos_mensajes3(proporcion=(0.90, 0.08, 0.02), n=10_000, semilla=0, **cambios):
    return _ml().PROCESOS["mensajes3"](n=n, semilla=semilla, proporcion=proporcion, **cambios)


# --- P1 §1 · el caso separable --------------------------------------------

MUS_SEPARABLE = tuple(float(v) for v in 10.0 ** np.arange(-6, 0.5, 0.5))
MUS_FIGURA_SEPARABLE = (1.0, 1e-2, 1e-5)
RUIDO_C17 = 0.2


def datos_separable(ruido=False):
    """El caso 17 (separable) o su versión con la fracción RUIDO_C17 de etiquetas reasignadas."""
    ml = _ml()
    return ml.caso(17, ruido_etiquetas=RUIDO_C17) if ruido else ml.caso(17)


@functools.lru_cache(maxsize=None)
def ajustes_separable(ruido=False):
    """ajustes_por_mu del caso 17 con φ = estandarizar(columnas("x")), como el NB08 bloque 1."""
    ml = _ml()
    phi = ml.estandarizar(ml.columnas("x"))
    with _silencio():
        return ml.ajustes_por_mu(datos_separable(ruido), phi, "l2", list(MUS_SEPARABLE),
                                 tarea="clasificacion")


def _norma_por_mu(aj):
    """Norma de las pendientes estandarizadas (sin β0) por μ, de la tabla de trayectorias."""
    t = aj.tabla
    return {float(mu): float(np.sqrt((g["valor"] ** 2).sum())) for mu, g in t.groupby("mu")}


@functools.lru_cache(maxsize=None)
def cifras_c4_separable():
    """Norma de las pendientes estandarizadas en la rejilla; subida media por década."""
    out = {}
    for nombre, ruido in (("separable", False), ("ruido", True)):
        normas = _norma_por_mu(ajustes_separable(ruido))
        mus = sorted(normas)
        bajas = [m for m in mus if m <= 1e-3 + 1e-15]
        subidas = [normas[bajas[i]] - normas[bajas[i + 1]] for i in range(len(bajas) - 1)]
        # cada paso de la rejilla es media década: la subida por década es 2 pasos
        por_decada = 2 * float(np.mean(subidas))
        out[nombre] = {"normas": normas, "subidas_media_decada": [2 * s for s in subidas],
                       "por_decada": por_decada}
    return {**out, "mus_figura": MUS_FIGURA_SEPARABLE,
            "cita": {"por_decada": _f(out["separable"]["por_decada"], 1),
                     "por_decada_ruido": _f(out["ruido"]["por_decada"], 2)}}


# --- P1 §2 · el umbral -----------------------------------------------------

@functools.lru_cache(maxsize=None)
def modelo_umbral():
    """fraude(proporcion=0.1), n = 600; μ por CV estratificada en ent (NB08 bloque 2)."""
    ml = _ml()
    datos = datos_fraude(0.1)
    mu = mu_por_cv(datos.ent)
    return datos, construir_logistica(mu)(datos.ent), mu


@functools.lru_cache(maxsize=None)
def cifras_c4_umbral():
    """τ elegido en validación con MCC; MCC en val y en despliegue con 0.5 y con el elegido."""
    ml = _ml()
    datos, m, mu = modelo_umbral()
    with _silencio():
        tau = float(ml.elegir_umbral(m, datos.val, "mcc"))
        p_val = m.predecir_p(datos.val)
        p_des = m.predecir_p(datos.despliegue)
        yv, yd = datos.val["y"].to_numpy(), datos.despliegue["y"].to_numpy()
        r = {}
        for nombre, t in (("05", 0.5), ("elegido", tau)):
            r[nombre] = {"val": float(ml.mcc(yv, (p_val >= t).astype(int), clases=[0, 1])),
                         "despliegue": float(ml.mcc(yd, (p_des >= t).astype(int), clases=[0, 1]))}
        perdida_val = float(m.L(datos.val))
    return {"mu": mu, "tau": tau, "mcc": r, "perdida_val": perdida_val, "n_val": len(datos.val),
            "cita": {"tau": _f(tau, 2), "mcc_val_05": _f(r["05"]["val"], 2),
                     "mcc_val_elegido": _f(r["elegido"]["val"], 2),
                     "mcc_des_05": _f(r["05"]["despliegue"], 2),
                     "mcc_des_elegido": _f(r["elegido"]["despliegue"], 2)}}


# --- P1 §3 · desbalanceo ---------------------------------------------------

PROPORCIONES = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01)
REPETICIONES_DESBALANCEO = 20


@functools.lru_cache(maxsize=None)
def tabla_desbalanceo():
    """metricas_vs_proporcion con fraude (n = 600), en despliegue y en validaciones frescas."""
    ml = _ml()
    with _silencio():
        return ml.metricas_vs_proporcion(list(PROPORCIONES), pesos=(None, "balanceado"),
                                         n=600, repeticiones=REPETICIONES_DESBALANCEO,
                                         contra=("despliegue", "val"))


@functools.lru_cache(maxsize=None)
def cifras_c4_desbalanceo():
    """La tabla de ml-c4-metricas-vs-proporcion y la banda de validación del MCC con pesos."""
    t = tabla_desbalanceo()
    d = t[t["conjunto"] == "despliegue"]

    def val(modelo, metrica, p):
        f = d[(d["modelo"] == modelo) & (d["metrica"] == metrica) & np.isclose(d["proporcion"], p)]
        return float(f["media"].iloc[0]), float(f["ee"].iloc[0])
    modelos = sorted(set(d["modelo"]))
    tabla = {(mo, me, p): val(mo, me, p) for mo in modelos for me in ("mcc", "aciertos_balanceados", "aciertos")
             for p in PROPORCIONES}
    v = t[(t["conjunto"] == "val") & (t["metrica"] == "mcc")]
    banda = {}
    for p in (0.5, 0.01):
        f = v[np.isclose(v["proporcion"], p) & (v["modelo"] == _modelo_pesos(modelos))]
        banda[p] = {"desv": float(f["desv"].iloc[0]), "media": float(f["media"].iloc[0]),
                    "tamano": int(f["tamano"].iloc[0])}
    return {"tabla": tabla, "modelos": modelos, "banda": banda,
            "cita": {"banda_01": _f(2 * banda[0.01]["desv"], 2), "banda_50": _f(2 * banda[0.5]["desv"], 2)}}


def _modelo_pesos(modelos):
    return [m for m in modelos if "balanceado" in str(m) or "pesos" in str(m) and "sin" not in str(m)][0]


@functools.lru_cache(maxsize=None)
def modelos_contribucion():
    """Los modelos sin pesos a 50 % y 1 % (fraude, n = 2000), μ = 10⁻³ estandarizado."""
    out = {}
    for p in (0.5, 0.01):
        datos = datos_fraude(p, n=2000)
        out[p] = (datos, construir_logistica(1e-3)(datos.ent))
    return out


@functools.lru_cache(maxsize=None)
def cifras_c4_contribucion():
    """Fracción de casos, de peso y de L_ent, y pérdida media por clase (50 % y 1 %)."""
    ml = _ml()
    out = {}
    for p, (datos, m) in modelos_contribucion().items():
        for pesos in (None, "balanceado"):
            with _silencio():
                t = ml.contribucion_por_clase(m, datos.ent, pesos=pesos)
            out[(p, pesos)] = t
    # la regla constante 0.01 con 1 % de positivos: parte de la pérdida en los positivos
    pos = 0.01 * -math.log(0.01)
    neg = 0.99 * -math.log(0.99)
    frac_pos = pos / (pos + neg)
    t1 = out[(0.01, None)]
    return {"tablas": out, "constante_frac_positivos": frac_pos,
            "cita": {"constante_frac_positivos": _f(frac_pos, 2),
                     "frac_peso_balanceado": "1/2",
                     "perdida_media_fraude_1": _f(_col(t1, 1, "perdida_media"), 2),
                     "perdida_media_legitimo_1": _f(_col(t1, 0, "perdida_media"), 3),
                     "frac_casos_fraude_1": _f(_col(t1, 1, "fraccion_casos"), 3)}}


def _col(t, clase, columna):
    if "clase" in t.columns:
        return float(t.loc[t["clase"] == clase, columna].iloc[0])
    return float(t.loc[clase, columna])


@functools.lru_cache(maxsize=None)
def modelo_bootstrap():
    """Un modelo de fraude(proporcion=0.1) evaluado en su validación."""
    datos = datos_fraude(0.1)
    return datos, construir_logistica(1e-2)(datos.ent)


@functools.lru_cache(maxsize=None)
def cifras_c4_bootstrap_aciertos():
    """A de un modelo en val: ±2 EE contra el intervalo por filas; y el contraejemplo exacto."""
    ml = _ml()
    datos, m = modelo_bootstrap()
    y = datos.val["y"].to_numpy()
    acierto = (np.asarray(m.predecir(datos.val)) == y).astype(float)
    a = float(acierto.mean())
    ee = float(ml.error_estandar(1 - acierto))
    with _silencio():
        inc = ml.incertidumbre(m, datos.val, "aciertos", repeticiones=1000)
    lo, hi = (float(v) for v in inc["intervalo"]) if isinstance(inc, dict) else (float(v) for v in inc.intervalo)
    ex = cifras_c4_bootstrap_aciertos_exacto()
    return {"aciertos": a, "ee": ee, "intervalo_filas": (lo, hi), "n_val": len(y),
            **{k: v for k, v in ex.items() if k != "cita"},
            "cita": {**ex["cita"], "aciertos": _f(a, 3), "dos_ee": _f(2 * ee, 3),
                     "intervalo": (_f(lo, 3), _f(hi, 3))}}


# --- P1 §4 · pesos -----------------------------------------------------------

RAZONES = tuple(float(v) for v in 10 ** np.linspace(0, 2, 21))
N_PESOS = 3000


@functools.lru_cache(maxsize=None)
def datos_pesos():
    """fraude(proporcion=0.05) del NB08 bloque 4 y de ml-c4-pesos-umbral."""
    return datos_fraude(0.05, n=N_PESOS)


@functools.lru_cache(maxsize=None)
def tabla_pesos():
    ml = _ml()
    with _silencio():
        return ml.efecto_de_pesos(datos_pesos(), list(RAZONES) + [19.0])


@functools.lru_cache(maxsize=None)
def cifras_c4_pesos_intercepto():
    """Pendientes con y sin pesos, salto del intercepto contra ln(w1/w0), coincidencia, p̂ medio."""
    t = tabla_pesos()
    sin = t.loc[np.isclose(t["razon"], 1.0)].iloc[0]
    con = t.loc[np.isclose(t["razon"], 19.0)].iloc[0]
    salto = float(con["beta0"] - sin["beta0"])
    return {"pendientes_sin": float(sin["pendientes"]), "pendientes_con": float(con["pendientes"]),
            "salto": salto, "ln_razon": math.log(19), "coincidencia": float(con["coincidencia"]),
            "p_sin": float(sin["p_promedio"]), "p_con": float(con["p_promedio"]),
            "prob_real": float(sin["prob_real"]),
            "cita": {"pendientes_sin": _f(sin["pendientes"], 2), "pendientes_con": _f(con["pendientes"], 2),
                     "salto": _f(salto, 2), "ln_razon": _f(math.log(19), 2),
                     "coincidencia": _f(100 * float(con["coincidencia"]), 1),
                     "p_sin": _f(sin["p_promedio"], 3), "p_con": _f(con["p_promedio"], 3),
                     "prob_real": _f(sin["prob_real"], 3)}}


RAZONES_METRICA = (1, 3, 5, 19, 100)


@functools.lru_cache(maxsize=None)
def cifras_c4_razon_por_metrica():
    """Con fraude(proporcion=0.05), en población: métricas de la regla de cada razón w1/w0."""
    prob = datos_pesos().realidad["prob"].to_numpy()
    rejilla = np.unique(np.r_[10 ** np.linspace(0, 2, 401), RAZONES_METRICA])
    met = {r: _metricas_esperadas(prob, prob >= 1 / (1 + r)) for r in rejilla}
    en = {r: met[float(r)] for r in RAZONES_METRICA}
    mejor = {k: float(max(rejilla, key=lambda r: met[r][k])) for k in ("mcc", "aciertos_balanceados", "aciertos")}
    return {"por_razon": en, "mejor_razon": mejor,
            "mejor_valor": {k: met[mejor[k]][k] for k in mejor},
            "cita": {"mcc": tuple(_f(en[r]["mcc"], 3) for r in RAZONES_METRICA),
                     "mcc_max": _f(met[mejor["mcc"]]["mcc"], 3), "razon_mcc": _f(mejor["mcc"], 1),
                     "abal_max": _f(met[mejor["aciertos_balanceados"]]["aciertos_balanceados"], 3),
                     "razon_abal": _f(mejor["aciertos_balanceados"], 0),
                     "aciertos_1": _f(en[1]["aciertos"], 3), "aciertos_100": _f(en[100]["aciertos"], 3)}}


def datos_mal_especificado(semilla=0):
    """Un proceso que la logística lineal no contiene: el puntaje tiene x1² (R7)."""
    ml = _ml()
    return ml.proceso_clasificacion(
        n=2000, x={"x1": ml.normal(0, 1), "x2": ml.normal(0, 1)},
        puntaje=lambda d: 1.5 * d["x1"] + 1.0 * d["x2"] + 1.0 * d["x1"] ** 2,
        proporcion=0.05, separar="estratificado", semilla=semilla)


MU_MAL_ESPECIFICADO = 0.1


@functools.lru_cache(maxsize=None)
def cifras_c4_pesos_mal_especificado():
    """R7: MCC en despliegue con pesos y τ = 0.5 contra sin pesos y el mejor τ en val.

    Mal especificado (x1² en la verdad, φ lineal) y con μ > 0; cinco semillas. Decide
    cuál de las dos respuestas lleva el Piensa «¿para qué pesar?» de P1 §4.
    """
    ml = _ml()
    filas = []
    for s in range(5):
        datos = datos_mal_especificado(s)
        con = construir_logistica(MU_MAL_ESPECIFICADO, "balanceado")(datos.ent)
        sin = construir_logistica(MU_MAL_ESPECIFICADO)(datos.ent)
        with _silencio():
            tau = float(ml.elegir_umbral(sin, datos.val, "mcc"))
            yd = datos.despliegue["y"].to_numpy()
            m_con = float(ml.mcc(yd, (con.predecir_p(datos.despliegue) >= 0.5).astype(int), clases=[0, 1]))
            m_sin = float(ml.mcc(yd, (sin.predecir_p(datos.despliegue) >= tau).astype(int), clases=[0, 1]))
        filas.append((m_con, m_sin, tau))
    dif = [a - b for a, b, _ in filas]
    sostiene = min(dif) > 0
    return {"filas": filas, "diferencias": dif, "sostiene": sostiene,
            "cita": {"con": _f(np.mean([f[0] for f in filas]), 2), "sin": _f(np.mean([f[1] for f in filas]), 2)}}


# --- P1 §4 · caso 25 -------------------------------------------------------

MU_C25 = 1e-4


@functools.lru_cache(maxsize=None)
def modelos_anillos():
    """Los tres paneles de ml-c4-anillos-metricas: lineal, lineal con pesos, cuadrática con pesos."""
    datos = _ml().caso(25)
    return datos, {
        "lineal": construir_logistica(MU_C25)(datos.ent),
        "lineal_pesos": construir_logistica(MU_C25, "balanceado")(datos.ent),
        "cuadratica_pesos": construir_logistica(MU_C25, "balanceado", cuadratica=True)(datos.ent),
        "cuadratica": construir_logistica(MU_C25, None, cuadratica=True)(datos.ent),
    }


@functools.lru_cache(maxsize=None)
def cifras_c4_anillos():
    """Caso 25: MCC en despliegue de los paneles; MCC poblacional de reglas de referencia."""
    ml = _ml()
    datos, mods = modelos_anillos()
    with _silencio():
        ajust = {k: float(ml.desempeno(m, datos, "mcc")) for k, m in mods.items()}
    real = datos.realidad
    prob = real["prob"].to_numpy()
    aciertos = _mcc_esperado(prob, prob >= 0.5)
    balanceada = _mcc_esperado(prob, prob >= 0.1)
    cortes = np.linspace(0.05, 0.95, 181)
    mccs = [_mcc_esperado(prob, prob >= c) for c in cortes]
    i = int(np.argmax(mccs))
    x1 = real["x1"].to_numpy()
    ts = np.linspace(-1.5, 1.5, 301)
    semis = [abs(_mcc_esperado(prob, x1 <= t)) for t in ts]
    j = int(np.argmax(semis))
    return {"ajustados": ajust, "mcc_regla_aciertos": aciertos, "mcc_regla_balanceada": balanceada,
            "mcc_mejor_corte": float(mccs[i]), "corte_mejor": float(cortes[i]),
            "mcc_mejor_semiespacio": float(semis[j]), "t_semiespacio": float(ts[j]),
            "cita": {k: _f(v, 2) for k, v in ajust.items()} | {
                "regla_aciertos": _f(aciertos, 2), "regla_balanceada": _f(balanceada, 2),
                "mejor_corte": _f(mccs[i], 2), "corte_mejor": _f(cortes[i], 2),
                "mejor_semiespacio": _f(semis[j], 2)}}


# --- P1 §5 · una métrica por pliegue ----------------------------------------

KS_PLIEGUE = (3, 5, 10)
MU_PLIEGUE = 1e-2


@functools.lru_cache(maxsize=None)
def datos_pliegue():
    """fraude(proporcion=0.02) con 600 casos de entrenamiento (unos 12 fraudes)."""
    return datos_fraude(0.02, n=1000)


@functools.lru_cache(maxsize=None)
def tablas_mcc_por_pliegue():
    """Por k: la tabla de validacion_cruzada con MCC y con A_bal (con_clases), estratificada."""
    ml = _ml()
    datos = datos_pliegue()
    df = datos.ent
    clases = list(df.attrs["ml"]["clases"])
    construir = construir_logistica(MU_PLIEGUE, "balanceado")
    out = {}
    for k in KS_PLIEGUE:
        with _silencio():
            cv_m = ml.validacion_cruzada(df, construir, k, particion="estratificado",
                                         estadistico=ml.con_clases(ml.mcc, clases))
            cv_a = ml.validacion_cruzada(df, construir, k, particion="estratificado",
                                         estadistico=ml.con_clases(ml.aciertos_balanceados, clases))
        out[k] = (cv_m, cv_a)
    return out


def _por_pliegue(cv):
    v = cv.por_pliegue_estadistico if hasattr(cv, "por_pliegue_estadistico") else cv["por_pliegue_estadistico"]
    return [float(x) for x in v]


@functools.lru_cache(maxsize=None)
def cifras_c4_mcc_por_pliegue():
    """MCC y A_bal por pliegue para k = 3, 5, 10; medias, rango y el valor en despliegue."""
    ml = _ml()
    datos = datos_pliegue()
    m = construir_logistica(MU_PLIEGUE, "balanceado")(datos.ent)
    with _silencio():
        des = {"mcc": float(ml.desempeno(m, datos, "mcc")),
               "aciertos_balanceados": float(ml.desempeno(m, datos, "aciertos_balanceados"))}
    out = {}
    for k, (cv_m, cv_a) in tablas_mcc_por_pliegue().items():
        mm, aa = _por_pliegue(cv_m), _por_pliegue(cv_a)
        out[k] = {"mcc": mm, "aciertos_balanceados": aa, "media_mcc": float(np.mean(mm)),
                  "rango_mcc": float(max(mm) - min(mm)),
                  "media_abal": float(np.nanmean(aa)) if not all(np.isnan(aa)) else float("nan")}
    n_fraudes = int(datos.ent["y"].sum())
    return {"por_k": out, "despliegue": des, "fraudes_ent": n_fraudes, "n_ent": len(datos.ent),
            "cita": {"fraudes_ent": str(n_fraudes),
                     "rango_mcc": {k: _f(v["rango_mcc"], 2) for k, v in out.items()},
                     "min_mcc_10": _f(min(out[10]["mcc"]), 2), "max_mcc_10": _f(max(out[10]["mcc"]), 2),
                     "mcc_despliegue": _f(des["mcc"], 2)}}


# --- P1 §6 · tres clases -----------------------------------------------------

MU_MULTICLASE = 1e-3


@functools.lru_cache(maxsize=None)
def modelos_multiclase(proporcion=(0.90, 0.08, 0.02)):
    """mensajes3 (n = 10 000, al azar); softmax lineal estandarizado sin y con pesos."""
    datos = datos_mensajes3(proporcion)
    return datos, {"sin": construir_logistica(MU_MULTICLASE)(datos.ent),
                   "con": construir_logistica(MU_MULTICLASE, "balanceado")(datos.ent)}


@functools.lru_cache(maxsize=None)
def cifras_c4_multiclase():
    """Aciertos por clase y MCC multiclase en despliegue, sin y con pesos, 90/8/2."""
    ml = _ml()
    datos, mods = modelos_multiclase()
    d = datos.despliegue
    y = d["y"].to_numpy()
    out = {}
    for k, m in mods.items():
        yg = np.asarray(m.predecir(d))
        with _silencio():
            out[k] = {"por_clase": tuple(float(v) for v in ml.por_clase("aciertos", y, yg, clases=[0, 1, 2])),
                      "mcc": float(ml.mcc(y, yg, clases=[0, 1, 2])),
                      "aciertos": float(ml.aciertos(y, yg)),
                      "aciertos_balanceados": float(ml.aciertos_balanceados(y, yg, clases=[0, 1, 2]))}
    return {**out, "cita": {k: {"por_clase": tuple(_f(v, 2) for v in o["por_clase"]),
                                "mcc": _f(o["mcc"], 2), "aciertos": _f(o["aciertos"], 2),
                                "aciertos_balanceados": _f(o["aciertos_balanceados"], 2)}
                            for k, o in out.items()}}


# ============================================================ página 2 ===

N_CALIBRACION = 2000
FRACCIONES_CALIBRACION = (0.5, 0.3, 0.2)


@functools.lru_cache(maxsize=None)
def datos_calibracion():
    """NB09 bloques 1–2: fraude(n=2000, proporcion=0.05, fracciones=(0.5, 0.3, 0.2)).

    Sin conformal no se crea cal: val_a, val_b = partir(val, 0.5, estratificado, semilla 0).
    """
    ml = _ml()
    datos = datos_fraude(0.05, n=N_CALIBRACION, fracciones=FRACCIONES_CALIBRACION)
    val_a, val_b = ml.partir(datos.val, 0.5, como="estratificado", semilla=0)
    return datos, val_a, val_b


@functools.lru_cache(maxsize=None)
def modelos_calibracion():
    """Sin pesos, con pesos balanceados (μ por CV en ent) y el de pesos recalibrado con Platt en val_a."""
    ml = _ml()
    datos, val_a, _ = datos_calibracion()
    mu = mu_por_cv(datos.ent)
    sin = construir_logistica(mu)(datos.ent)
    con = construir_logistica(mu, "balanceado")(datos.ent)
    with _silencio():
        rec = ml.recalibrar(con, val_a, "platt")
    return {"sin": sin, "con": con, "recalibrado": rec, "mu": mu}


@functools.lru_cache(maxsize=None)
def cifras_c4_calibracion():
    """Brier y pérdida logarítmica en val_b: sin pesos, con pesos, recalibrado y benchmark."""
    ml = _ml()
    datos, _, val_b = datos_calibracion()
    mods = modelos_calibracion()
    y = val_b["y"].to_numpy()
    out = {}
    for k in ("sin", "con", "recalibrado"):
        p = mods[k].predecir_p(val_b)
        out[k] = {"brier": float(ml.brier(y, p)), "logaritmica": float(ml.log_loss(y, p)),
                  "p_promedio_realidad": float(np.mean(mods[k].predecir_p(datos.realidad)))}
    with _silencio():
        b = ml.benchmarks(datos, val_b, criterios=("brier", "logaritmica"))
    fila = b.loc["proporcion"] if "proporcion" in getattr(b, "index", []) else b[b.iloc[:, 0] == "proporcion"].iloc[0]
    out["benchmark"] = {"brier": float(fila["brier"]), "logaritmica": float(fila["logaritmica"])}
    out["prob_real"] = float(datos.realidad["prob"].mean())
    return {**out, "n_val_b": len(val_b), "mu": mods["mu"],
            "cita": {"n_val_b": str(len(val_b)),
                     **{f"brier_{k}": _f(out[k]["brier"], 3) for k in ("sin", "con", "recalibrado", "benchmark")},
                     **{f"log_{k}": _f(out[k]["logaritmica"], 3) for k in ("sin", "con", "recalibrado", "benchmark")},
                     "p_sin": _f(out["sin"]["p_promedio_realidad"], 3),
                     "p_con": _f(out["con"]["p_promedio_realidad"], 3),
                     "p_rec": _f(out["recalibrado"]["p_promedio_realidad"], 3),
                     "prob_real": _f(out["prob_real"], 3)}}


@functools.lru_cache(maxsize=None)
def cifras_c4_platt():
    """β̂^cal de Platt (en val_a) sobre el modelo con pesos, contra −ln(w1/w0) y 1."""
    datos, _, _ = datos_calibracion()
    rec = modelos_calibracion()["recalibrado"]
    b = rec.hiperparametros["beta_cal"]
    b0, b1 = float(b[0]), float(b[1])
    y = datos.ent["y"].to_numpy()
    razon = float((y == 0).sum() / (y == 1).sum())
    return {"beta0": b0, "beta1": b1, "menos_ln_razon": -math.log(razon), "razon": razon,
            "cita": {"beta0": _f(b0, 2), "beta1": _f(b1, 2), "menos_ln_razon": _f(-math.log(razon), 2)}}


# --- P2 §4–§5 · conformal ------------------------------------------------------

DELTA = 0.1


@functools.lru_cache(maxsize=None)
def datos_conformal(n=10_000, proporcion=(0.90, 0.08, 0.02), semilla=0):
    """mensajes3 al azar; cal3 se aparta PRIMERO de la validación (mapa único, sufijo 3)."""
    ml = _ml()
    datos3 = datos_mensajes3(proporcion, n=n, semilla=semilla)
    cal3, resto3 = ml.partir(datos3.val, 1 / 3, como="azar", semilla=0)
    return datos3, cal3, resto3


@functools.lru_cache(maxsize=None)
def modelo_conformal(n=10_000, proporcion=(0.90, 0.08, 0.02), pesos=None):
    """Softmax lineal estandarizado con datos3.ent (μ fijo MU_MULTICLASE)."""
    datos3, _, _ = datos_conformal(n, proporcion)
    return construir_logistica(MU_MULTICLASE, pesos)(datos3.ent)


def _cobertura(cf, df):
    return {"global": cf.cobertura(df), "por_clase": tuple(float(v) for v in cf.cobertura_por_clase(df)),
            "tamano": cf.tamano_medio(df), "tamano_por_clase": tuple(float(v) for v in cf.tamano_por_clase(df))}


@functools.lru_cache(maxsize=None)
def cifras_c4_conformal_cobertura():
    """Cobertura y tamaño medio en despliegue, marginal y por clase (90/8/2, δ = 0.1)."""
    ml = _ml()
    datos3, cal3, _ = datos_conformal()
    m = modelo_conformal()
    out = {}
    for nombre, pc in (("marginal", False), ("por_clase", True)):
        with _silencio():
            cf = ml.conformal(m, cal3, DELTA, por_clase=pc)
        out[nombre] = _cobertura(cf, datos3.despliegue)
    fr_cal = int((cal3["y"] == 2).sum())
    return {**out, "fraudes_cal3": fr_cal, "n_cal3": len(cal3),
            "cita": {"n_cal3": str(len(cal3)), "fraudes_cal3": str(fr_cal),
                     **{f"{k}_global": _f(v["global"], 2) for k, v in out.items()},
                     **{f"{k}_fraude": _f(v["por_clase"][2], 2) for k, v in out.items()},
                     **{f"{k}_tamano": _f(v["tamano"], 2) for k, v in out.items()}}}


@functools.lru_cache(maxsize=None)
def cifras_c4_final_p2():
    """El ejercicio final de P2: conformal marginal (δ = 0.1) sobre mensajes3 90/8/2.

    DECISIÓN prog-c4 (C4.T5): el modelo base del enunciado es el softmax SIN pesos y
    sin recalibrar. Con pesos balanceados, el marginal ya cubre el fraude (0.91 con
    esta semilla) y el ejercicio dejaría de mostrar lo que el teorema no promete. Las
    cifras con pesos se guardan en "con_pesos" para el entregable 3 (los pesos y la
    recalibración no cambian la validez; cambian el tamaño de los conjuntos).
    """
    ml = _ml()
    datos3, cal3, _ = datos_conformal()
    out = {}
    for nombre, pesos in (("sin_pesos", None), ("con_pesos", "balanceado")):
        m = modelo_conformal(pesos=pesos)
        with _silencio():
            cf = ml.conformal(m, cal3, DELTA, por_clase=False)
        out[nombre] = _cobertura(cf, datos3.despliegue)
    s = out["sin_pesos"]
    c = out["con_pesos"]
    return {**out, "cita": {"global": _f(s["global"], 2), "fraude": _f(s["por_clase"][2], 2),
                            "tamano": _f(s["tamano"], 2), "global_pesos": _f(c["global"], 2),
                            "fraude_pesos": _f(c["por_clase"][2], 2), "tamano_pesos": _f(c["tamano"], 2),
                            "minimo": "9"}}


@functools.lru_cache(maxsize=None)
def cifras_c4_tamanos():
    """Los tamaños de §10.3 y §10.6: fraudes en cal3 (n = 10 000 y 2000) e impagos en cal de la tarea."""
    _, cal_g, _ = datos_conformal(10_000)
    _, cal_c, _ = datos_conformal(2000)
    return {"cal3_10000": int((cal_g["y"] == 2).sum()), "cal3_2000": int((cal_c["y"] == 2).sum()),
            "cita": {"cal3_10000": str(int((cal_g["y"] == 2).sum())),
                     "cal3_2000": str(int((cal_c["y"] == 2).sum()))}}


R_CALIBRACIONES = 30


@functools.lru_cache(maxsize=None)
def cifras_c4_conformal_repetido():
    """Cobertura por clase en despliegue promediada sobre R calibraciones frescas (90/8/2).

    El modelo queda congelado (ajustado con datos3.ent); cada calibración es la pieza
    cal3 de otra muestra independiente del mismo proceso (semillas 1…R). La garantía
    promedia sobre la calibración y el caso nuevo: una sola calibración puede quedar
    abajo de 1 − δ sin violar el teorema. Es la cifra que dibuja ml-c4-cobertura-por-clase.
    """
    ml = _ml()
    m = modelo_conformal()
    d3, _, _ = datos_conformal()
    cov = {False: [], True: []}
    tam = {False: [], True: []}
    glob = {False: [], True: []}
    for s in range(1, R_CALIBRACIONES + 1):
        dd = datos_mensajes3(semilla=s, con_realidad=False)
        cal, _ = ml.partir(dd.val, 1 / 3, como="azar", semilla=0)
        for pc in (False, True):
            with _silencio():
                cf = ml.conformal(m, cal, DELTA, por_clase=pc)
            cov[pc].append([float(v) for v in cf.cobertura_por_clase(d3.despliegue)])
            glob[pc].append(cf.cobertura(d3.despliegue))
            tam[pc].append([float(v) for v in cf.tamano_por_clase(d3.despliegue)])
    out = {}
    for pc, nombre in ((False, "marginal"), (True, "por_clase")):
        c = np.array(cov[pc])
        out[nombre] = {"media": tuple(c.mean(0)), "ee": tuple(c.std(0, ddof=1) / math.sqrt(len(c))),
                       "tamano": tuple(np.array(tam[pc]).mean(0)),
                       "global": float(np.mean(glob[pc])),
                       "ee_global": float(np.std(glob[pc], ddof=1) / math.sqrt(len(glob[pc])))}
    return {**out, "R": R_CALIBRACIONES,
            "cita": {"R": str(R_CALIBRACIONES),
                     "marginal_fraude": _f(out["marginal"]["media"][2], 2),
                     "por_clase_fraude": _f(out["por_clase"]["media"][2], 2),
                     "por_clase": tuple(_f(v, 2) for v in out["por_clase"]["media"])}}
