"""Cifras de la clase 3 de la unidad de aprendizaje de maquina (unidad 9).

Una funcion por hecho que cita una pagina, un notebook o una figura de la
clase 3 (clase_3.md §10.7.3). Ninguna cifra se escribe a mano: la pagina la
copia de aqui, tools/test_ml_cifras_c3.py la fija en la fuente y
tools/test_ml_prosa_c3.py la busca en la pagina que la cita (D-009.5, D-003).

Cada funcion devuelve un dict con los valores crudos y, en la clave "cita",
las formas literales con que la pagina y las figuras los escriben (cadenas ya
redondeadas). Las funciones se guardan en cache: la suite y el generador de
figuras las llaman muchas veces y algunas cuestan segundos (la CV con lasso).

Los procesos con que se calculan (datos_*) son los mismos que dibujan
tools/figuras_ml_c3.py y los notebooks 06 y 07: una sola fuente por proceso.

Las funciones que calculan con ml_lab lo importan de tools/ (nunca de
_assets/, D-004) y solo dentro de la funcion.

Anclas por tramo (protocolo p5.2 §7.1): la rama de clase escribe solo antes
del «fin tramo rapido»; la subrama -c, solo antes del «fin tramo completo».
"""
import contextlib
import functools
import importlib
import warnings

import numpy as np


def _ml():
    """tools/aprendizaje_maquina.py (ml_lab), importado al pedirlo."""
    return importlib.import_module("aprendizaje_maquina")


def _f(v, d):
    """La forma con que la pagina escribe un numero: d decimales."""
    return f"{float(v):.{d}f}"


@contextlib.contextmanager
def _silencio():
    """Los avisos de ml_lab (mínimo no único, piso con Monte Carlo) no son cifras."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


def _perdidas(modelo, df):
    """Las pérdidas cuadráticas por observación de un modelo en df."""
    y = df["y"].to_numpy(float)
    return (y - np.asarray(modelo.predecir(df), float)) ** 2


def _perdidas_constante(valor, df):
    y = df["y"].to_numpy(float)
    return (y - float(valor)) ** 2


F = (0.6, 0.2, 0.2)


# --- tramo rapido ---

# ---------------------------------------------------------- página 1 · §1 ---
# Dos modelos con el mismo RMSE de validación (F1, nb06 B1): x ~ U(-2, 2),
# n = 300 con 0.6/0.2/0.2. Fila «correcto»: f = 1 + 2x con ruido grande; fila
# «curva»: f = 1 + 2x + x² ajustada con una recta, con ruido chico. El ruido
# de la fila correcta se elige para igualar el RMSE de validación: con el
# modelo correcto los residuales son lineales en el ruido (σ·(I − H)z), así
# que el RMSE escala exacto con σ.

SIGMA_CURVA = 0.5
N_B1 = 300


def f_b1(modelo):
    """f de cada opción del bloque 1 de nb06 (y de las filas de F1)."""
    if modelo == "correcto":
        return lambda d: 1 + 2 * d["x1"]
    if modelo == "curva":
        return lambda d: 1 + 2 * d["x1"] + d["x1"] ** 2
    if modelo == "omitida":
        return lambda d: 1 + 2 * d["x1"] + 1.5 * d["x2"]
    raise ValueError(modelo)


def datos_b1(modelo, sigma, semilla=0):
    """Los datos del bloque 1 de nb06 y de F1: x1, x2 ~ U(-2, 2)."""
    ml = _ml()
    x = {"x1": ml.uniforme(-2, 2), "x2": ml.uniforme(-2, 2)}
    return ml.proceso(n=N_B1, x=x, f=f_b1(modelo), ruido=ml.normal(0, sigma),
                      omitir=["x2"], semilla=semilla)


@functools.lru_cache(maxsize=None)
def sigma_correcto():
    """σ_ε de la fila correcta de F1, a 3 decimales, que iguala el RMSE de val."""
    ml = _ml()
    curva = datos_b1("curva", SIGMA_CURVA)
    r_curva = float(np.sqrt(ml.L(ml.ajustar(curva, phi=ml.columnas("x1")), curva.val)))
    uno = datos_b1("correcto", 1.0)
    r_uno = float(np.sqrt(ml.L(ml.ajustar(uno, phi=ml.columnas("x1")), uno.val)))
    return round(r_curva / r_uno, 3)


def datos_mismo_rmse(fila):
    """Los datos de una fila de F1: "correcto" o "curva"."""
    sigma = sigma_correcto() if fila == "correcto" else SIGMA_CURVA
    return datos_b1(fila, sigma)


@functools.lru_cache(maxsize=None)
def cifras_c3_mismo_rmse():
    """P1 §1 y F1: RMSE de validación de las dos filas (iguales a 2 decimales),
    el σ_ε de cada una y la correlación de e con x² en la fila curva."""
    ml = _ml()
    out = {}
    for fila in ("correcto", "curva"):
        d = datos_mismo_rmse(fila)
        m = ml.ajustar(d, phi=ml.columnas("x1"))
        e = d.val["y"].to_numpy() - m.predecir(d.val)
        out[f"rmse_val_{fila}"] = float(np.sqrt(np.mean(e ** 2)))
        out[f"corr_e_x2_{fila}"] = float(np.corrcoef(e, d.val["x1"] ** 2)[0, 1])
    out["sigma_correcto"] = sigma_correcto()
    out["sigma_curva"] = SIGMA_CURVA
    out["cita"] = {"rmse_val": _f(out["rmse_val_curva"], 2),
                   "sigma_correcto": _f(out["sigma_correcto"], 2),
                   "sigma_curva": _f(SIGMA_CURVA, 1)}
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_centro_entrenamiento():
    """P1 §1: ē_ent (0 por la ecuación del intercepto) y ē_val de la fila curva."""
    ml = _ml()
    d = datos_mismo_rmse("curva")
    m = ml.ajustar(d, phi=ml.columnas("x1"))
    e_ent = d.ent["y"].to_numpy() - m.predecir(d.ent)
    e_val = d.val["y"].to_numpy() - m.predecir(d.val)
    out = {"e_ent": float(np.mean(e_ent)), "e_val": float(np.mean(e_val))}
    out["cita"] = {"e_val": _f(out["e_val"], 2)}
    return out


# ---------------------------------------------------------- página 1 · §2 ---

def _comparar_con_la_media(d):
    """Caso (a) de ml-c3-def-benchmark: la recta y la media, fijadas con ent, en val.

    val no elige nada aquí: es una reserva para esta comparación.
    """
    ml = _ml()
    m = ml.ajustar(d)
    media = float(d.ent["y"].mean())
    l_mod = _perdidas(m, d.val)
    l_med = _perdidas_constante(media, d.val)
    bench = ml.benchmarks(d, d.val, criterios=["cuadratica", "absoluta"])
    dif, ee = ml.diferencia_pareada(l_mod, l_med)
    L_val = float(np.mean(l_mod))
    L_media = float(bench.loc["media", "cuadratica"])
    return {
        "rmse_modelo": float(np.sqrt(L_val)), "L_val": L_val,
        "rmse_media": float(np.sqrt(L_media)),
        "rmse_mediana": float(np.sqrt(bench.loc["mediana", "cuadratica"])),
        "mae_modelo": float(np.mean(np.abs(d.val["y"].to_numpy() - m.predecir(d.val)))),
        "mae_media": float(bench.loc["media", "absoluta"]),
        "mae_mediana": float(bench.loc["mediana", "absoluta"]),
        "ybar": media, "desv_y_ent": float(d.ent["y"].std(ddof=1)),
        "mejora": 1 - L_val / L_media,
        "dif_pareada": float(dif), "ee_dif": float(ee),
        "le_gana": bool(dif < -2 * ee),
        "piso": float(ml.piso(d)), "n_val": len(d.val),
    }


@functools.lru_cache(maxsize=None)
def cifras_c3_escala_y():
    """P1 §2, F2 (izquierda), nb06 B2: el caso 11 con el modelo correcto."""
    ml = _ml()
    out = _comparar_con_la_media(ml.caso(11))
    out["rmse_sobre_ybar"] = out["rmse_modelo"] / out["ybar"]
    out["rmse_sobre_desv"] = out["rmse_modelo"] / out["desv_y_ent"]
    out["cita"] = {
        "rmse_modelo": _f(out["rmse_modelo"], 2), "rmse_media": _f(out["rmse_media"], 2),
        "rmse_mediana": _f(out["rmse_mediana"], 2), "ybar": _f(out["ybar"], 0),
        "rmse_sobre_ybar": _f(100 * out["rmse_sobre_ybar"], 1) + " %",
        "desv_y_ent": _f(out["desv_y_ent"], 2),
        "rmse_sobre_desv": _f(out["rmse_sobre_desv"], 2),
        "mejora": _f(100 * out["mejora"], 1) + " %",
        "dif_pareada": _f(out["dif_pareada"], 3), "ee_dif": _f(out["ee_dif"], 3),
        "n_val": str(out["n_val"]),
    }
    return out


# La señal débil (F2 derecha, nb06 B2): f = señal·2x, x ~ U(-1, 1), σ = 1,
# n = 1000 como el caso 11. Con señal 0.375 (f = 0.75x) la mejora es chica y
# el modelo está en el piso; con 0.25 sería el caso 11 sin el nivel.
SENAL_DEBIL = 0.375


def datos_senal(nivel=0.0, senal=SENAL_DEBIL, n=1000, semilla=0):
    """El proceso del bloque 2 de nb06: f = nivel + señal·(2x)."""
    ml = _ml()
    return ml.proceso(n=n, x={"x": ml.uniforme(-1, 1)},
                      f=lambda d: nivel + senal * 2 * d["x"], ruido=ml.normal(0, 1),
                      semilla=semilla)


@functools.lru_cache(maxsize=None)
def cifras_c3_senal_debil():
    """P1 §2, F2 (derecha): señal débil, el modelo casi en el piso."""
    out = _comparar_con_la_media(datos_senal())
    out["raiz_piso"] = float(np.sqrt(out["piso"]))
    out["cita"] = {
        "rmse_modelo": _f(out["rmse_modelo"], 2), "rmse_media": _f(out["rmse_media"], 2),
        "raiz_piso": _f(out["raiz_piso"], 2), "mejora": _f(100 * out["mejora"], 1) + " %",
        "dif_pareada": _f(out["dif_pareada"], 3), "ee_dif": _f(out["ee_dif"], 3),
        "senal": "0.75x",
    }
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_cv_no_es_reserva():
    """P1 §2, ml-c3-obs-cv-no-es-reserva: los cuatro casos equiprobables de
    (y1, y2) en {±1}², CV dejando una fuera; modelo: 0; benchmark: la otra y."""
    casos = []
    medias = []
    for y1 in (1, -1):
        for y2 in (1, -1):
            y = np.array([y1, y2], float)
            difs = []
            for i in range(2):
                otra = y[1 - i]
                difs.append((y[i] - 0.0) ** 2 - (y[i] - otra) ** 2)
            difs = np.array(difs)
            s_d = float(np.std(difs, ddof=1))
            casos.append({"y": (y1, y2), "difs": tuple(float(v) for v in difs),
                          "ee_formula": s_d / np.sqrt(2)})
            medias.append(float(difs.mean()))
    medias = np.array(medias)
    return {"casos": casos, "media_esperada": float(medias.mean()),
            "desv_real": float(np.sqrt(np.mean((medias - medias.mean()) ** 2)))}


# ---------------------------------------------------------- página 1 · §3 ---

def piezas_colas():
    """Los tres ruidos de F3 y del bloque 3 de nb06, con su nombre de panel."""
    ml = _ml()
    return {"normal": ml.normal(), "Pareto, exponente 1.5": ml.pareto(1.5),
            "Cauchy": ml.cauchy()}


N_COLAS, SEMILLAS_COLAS = 10_000, 20


@functools.lru_cache(maxsize=None)
def cifras_c3_colas():
    """P1 §3, F3: cociente máx/mín del MSE a n = 10⁴ entre 20 semillas, por ruido,
    con los mismos sorteos que dibuja dibujar_media_acumulada (semillas 0..19)."""
    out = {}
    for nombre, pieza in piezas_colas().items():
        mse = [float(np.mean(np.asarray(pieza.muestrear(N_COLAS, np.random.default_rng(i)),
                                         float) ** 2)) for i in range(SEMILLAS_COLAS)]
        out[nombre] = max(mse) / min(mse)
    out["cita"] = {"normal": _f(out["normal"], 2),
                   "pareto": _f(out["Pareto, exponente 1.5"], 0),
                   "cauchy": f"{out['Cauchy']:,.0f}".replace(",", " ")}
    return out


# ---------------------------------------------------------- página 1 · §4 ---
# El caso 1 (especificación compartida, contrato §5.5) con n = 5000 y la
# partición 0.6/0.2/0.2: las tres láminas usan los mismos datos y L_val se lee
# en 1000 filas de validación (con 40 el ruido de L_val tapa el 1.1×).
N_CASO_1 = 5000


def datos_caso_1(ver_todo=False):
    ml = _ml()
    cambios = {"n": N_CASO_1, "fracciones": F}
    if ver_todo:
        cambios["omitir"] = None
    return ml.caso(1, **cambios)


def phi_lamina(lamina):
    ml = _ml()
    if lamina == "a":
        return ml.columnas("x1")
    if lamina == "b":
        return ml.columnas("x1", "x2", "x3")
    return ml.combinar(ml.columnas("x1", "x2", "x3"), ml.interacciones(("x2", "x3")))


def _ee_pendientes(modelo, df):
    """EE de mínimos cuadrados de cada coeficiente: s²(ΦᵀΦ)⁻¹ en ent."""
    M = modelo.Phi(df).to_numpy(float)
    e = df["y"].to_numpy(float) - M @ modelo.beta_gorro.to_numpy(float)
    s2 = float(e @ e) / (len(e) - M.shape[1])
    return dict(zip(modelo.beta_gorro.index, np.sqrt(np.diag(s2 * np.linalg.inv(M.T @ M)))))


@functools.lru_cache(maxsize=None)
def cifras_c3_omitida_caso1():
    """P1 §4, ml-c3-ejm-omitida: β̂1 en las tres láminas, el coeficiente
    estructural (beta_verdadero, la fuente de cifras_c1_omitida), la pendiente
    de f_visible, L_val de cada lámina y el piso con lo visible de (a)."""
    import pandas as pd
    ml = _ml()
    out = {}
    with _silencio():
        for lamina in ("a", "b", "c"):
            d = datos_caso_1(ver_todo=lamina != "a")
            m = ml.ajustar(d, phi=phi_lamina(lamina))
            ee = _ee_pendientes(m, d.ent)
            out[lamina] = {"beta": {k: float(v) for k, v in m.beta_gorro.items()},
                           "ee_x1": float(ee["x1"]), "L_val": float(ml.L(m, d.val))}
        da = datos_caso_1()
        out["estructural"] = float(ml.beta_verdadero(da, ml.columnas("x1"))["x1"])
        fv = da.f_visible(pd.DataFrame({"x1": [0.0, 1.0]}))
        out["pendiente_f_visible"] = float(fv[1] - fv[0])
        out["piso_visible"] = float(ml.piso(da))
        out["piso_todo"] = float(ml.piso(datos_caso_1(ver_todo=True)))
    out["cita"] = {"beta1_a": _f(out["a"]["beta"]["x1"], 2),
                   "beta1_b": _f(out["b"]["beta"]["x1"], 2),
                   "beta_c_x1": _f(out["c"]["beta"]["x1"], 2),
                   "beta_c_x2x3": _f(out["c"]["beta"]["x2*x3"], 2),
                   "L_val_c": _f(out["c"]["L_val"], 2),
                   "piso_visible": _f(out["piso_visible"], 2)}
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_piso_combinado():
    """Nota de P1 §4, nb06 B4: el control combinado de contrato v4 §5.8.
    y = 1 + 2x1 + 3x2 + ε, ε = 0.4x1 + √0.84·u, sin ver x2."""
    import pandas as pd
    ml = _ml()
    with _silencio():
        d = ml.proceso(n=20_000, x={"x1": ml.normal(), "x2": ml.normal()},
                       f=lambda q: 1 + 2 * q["x1"] + 3 * q["x2"], ruido=ml.normal(0, 1),
                       endogeno=0.4, omitir=["x2"], semilla=0)
        m = ml.ajustar(d)
        l_i = _perdidas(m, d.val)
        fv = d.f_visible(pd.DataFrame({"x1": [0.0, 1.0]}))
        piso_ = float(ml.piso(d))
    return {"piso": piso_, "pendiente_f_visible": float(fv[1] - fv[0]),
            "L_val": float(np.mean(l_i)), "ee_L_val": float(np.std(l_i, ddof=1) / np.sqrt(len(l_i))),
            "formula_sin_omitidas": 1 - 0.4 ** 2,
            "cita": {"piso": _f(piso_, 2), "formula": "0.84"}}


REPETICIONES = 200


@functools.lru_cache(maxsize=None)
def cifras_c3_endogena():
    """P1 §4: el caso 8. Media y desviación de 200 β̂1, la cuenta 2.5,
    corr(e, x1) en ent, L_val con n grande y piso(caso(8)) = 0.75."""
    ml = _ml()
    d = ml.caso(8)
    tabla = ml.beta_repetido(lambda s: d.rehacer(s), None, REPETICIONES)
    m = ml.ajustar(d)
    e = d.ent["y"].to_numpy() - m.predecir(d.ent)
    grande = ml.caso(8, n=20_000)
    mg = ml.ajustar(grande)
    l_i = _perdidas(mg, grande.val)
    out = {"media_beta1": float(tabla["x1"].mean()), "desv_beta1": float(tabla["x1"].std(ddof=1)),
           "cuenta": 2 + 0.5, "corr_e_x1": float(np.corrcoef(e, d.ent["x1"])[0, 1]),
           "L_val": float(np.mean(l_i)), "ee_L_val": float(np.std(l_i, ddof=1) / np.sqrt(len(l_i))),
           "piso": float(ml.piso(d))}
    out["ee_media"] = out["desv_beta1"] / np.sqrt(REPETICIONES)
    out["cita"] = {"media_beta1": _f(out["media_beta1"], 2), "cuenta": "2.5",
                   "L_val": _f(out["L_val"], 2), "piso": _f(out["piso"], 2)}
    return out


# F5 · las cuatro dianas de β̂ (200 entrenamientos de 150 filas, σ = 1).
N_DIANA = 150


def fabricas_diana():
    """{panel: fabrica(semilla) -> Datos} de F5; el coeficiente estructural es (1, 1)."""
    ml = _ml()
    x2 = {"x1": ml.normal(), "x2": ml.normal()}
    x3 = {"x1": ml.normal(), "x2": ml.normal(), "x3": ml.normal()}
    return {
        "correcto": lambda s: ml.proceso(n=N_DIANA, x=x2, f=lambda q: 1 + q["x1"] + q["x2"],
                                         semilla=s, con_realidad=False),
        "omitida correlacionada": lambda s: ml.proceso(
            n=N_DIANA, x=x3, f=lambda q: 1 + q["x1"] + q["x2"] + q["x3"],
            correlacion={("x1", "x3"): 0.6}, omitir=["x3"], semilla=s, con_realidad=False),
        "colineal": lambda s: ml.caso(9, semilla=s, con_realidad=False),
        "endógena": lambda s: ml.proceso(n=N_DIANA, x=x2, f=lambda q: 1 + q["x1"] + q["x2"],
                                         endogeno=0.5, semilla=s, con_realidad=False),
    }


@functools.lru_cache(maxsize=None)
def tablas_diana():
    ml = _ml()
    with _silencio():
        return {k: ml.beta_repetido(f, None, REPETICIONES) for k, f in fabricas_diana().items()}


@functools.lru_cache(maxsize=None)
def cifras_c3_diana():
    """P1 §4, F5: media y desviación de β̂1 y β̂2 en cada nube."""
    out = {}
    for k, t in tablas_diana().items():
        out[k] = {"media": (float(t["x1"].mean()), float(t["x2"].mean())),
                  "desv": (float(t["x1"].std(ddof=1)), float(t["x2"].std(ddof=1)))}
    out["cita"] = {"omitida": _f(out["omitida correlacionada"]["media"][0], 2),
                   "endogena": _f(out["endógena"]["media"][0], 2)}
    return out


# ---------------------------------------------------------- página 1 · §5 ---
DENTRO, FUERA = (1.0, 1.0), (1.0, -1.0)


@functools.lru_cache(maxsize=None)
def tablas_colineal():
    """200 β̂ del caso 9 con correlación 0.99 y con 0 (mismo proceso)."""
    ml = _ml()
    return {
        0.0: ml.beta_repetido(lambda s: ml.caso(9, semilla=s, correlacion={("x1", "x2"): 0.0},
                                                con_realidad=False), None, REPETICIONES),
        0.99: ml.beta_repetido(lambda s: ml.caso(9, semilla=s, con_realidad=False), None,
                               REPETICIONES),
    }


def prediccion_repetida(tabla, punto):
    """ŷ en el punto (x1, x2) de cada fila de una tabla de beta_repetido."""
    return tabla["1"] + tabla["x1"] * punto[0] + tabla["x2"] * punto[1]


@functools.lru_cache(maxsize=None)
def cifras_c3_colineal():
    """P1 §5, F7: desv. de β̂1 con corr 0 y 0.99; desv. de ŷ dentro y fuera."""
    t = tablas_colineal()
    out = {"desv_beta1": {c: float(t[c]["x1"].std(ddof=1)) for c in t},
           "desv_y_dentro": {c: float(prediccion_repetida(t[c], DENTRO).std(ddof=1)) for c in t},
           "desv_y_fuera": {c: float(prediccion_repetida(t[c], FUERA).std(ddof=1)) for c in t}}
    out["razon_beta1"] = out["desv_beta1"][0.99] / out["desv_beta1"][0.0]
    out["razon_dentro"] = out["desv_y_dentro"][0.99] / out["desv_y_dentro"][0.0]
    out["razon_fuera"] = out["desv_y_fuera"][0.99] / out["desv_y_fuera"][0.0]
    out["cita"] = {"desv_beta1_0": _f(out["desv_beta1"][0.0], 2),
                   "desv_beta1_99": _f(out["desv_beta1"][0.99], 2),
                   "desv_y_dentro_99": _f(out["desv_y_dentro"][0.99], 2),
                   "desv_y_fuera_99": _f(out["desv_y_fuera"][0.99], 2)}
    return out


# ---------------------------------------------- página 1 · nb06 (C3.T3) ---

def datos_cola_en_x(semilla=0):
    """«Dónde vive la cola: en x» de nb06 B3: x lognormal, f curva, ruido normal."""
    ml = _ml()
    return ml.proceso(n=1000, x={"x": ml.lognormal(0, 1)},
                      f=lambda d: 2 + np.exp(d["x"] / 3), ruido=ml.normal(0, 0.5),
                      semilla=semilla)


@functools.lru_cache(maxsize=None)
def cifras_c3_cola_en_x():
    """nb06 B3, C3.T3: fracción de los 10 mayores |e| de val que caen en el 5 %
    de x más grande, en 10 semillas (criterio: ≥ 0.8 en ≥ 8)."""
    ml = _ml()
    fr = []
    for s in range(10):
        d = datos_cola_en_x(s)
        m = ml.ajustar(d)
        df = d.val
        e = np.abs(df["y"].to_numpy() - m.predecir(df))
        top = np.argsort(e)[-10:]
        corte = np.quantile(df["x"], 0.95)
        fr.append(float(np.mean(df["x"].to_numpy()[top] >= corte)))
    return {"fracciones": fr}


SIGMA_ABANICO = 0.5


def datos_abanico(cual, semilla=0):
    """ejercicio-abanico de nb06: (A) ruido con desviación √(0.25 + x1²);
    (B) f con x1·x2 y ruido normal 0.5. Los dos tienen la misma desviación
    condicional de e dado x1, así que el abanico de e contra x1 es el mismo."""
    ml = _ml()
    x = {"x1": ml.normal(), "x2": ml.normal()}
    if cual == "A":
        return ml.proceso(n=600, x=x, f=lambda d: 1 + d["x1"] + d["x2"],
                          ruido=ml.heterocedastico(
                              lambda d: np.sqrt(SIGMA_ABANICO ** 2 + d["x1"] ** 2)),
                          semilla=semilla)
    return ml.proceso(n=600, x=x, f=lambda d: 1 + d["x1"] + d["x2"] + d["x1"] * d["x2"],
                      ruido=ml.normal(0, SIGMA_ABANICO), semilla=semilla)


@functools.lru_cache(maxsize=None)
def cifras_c3_abanico():
    """C3.T3: cociente de la desviación de e en el quinto de |x1| más grande
    contra el más chico, en val, para A y B (deben quedar a ±20 %)."""
    ml = _ml()
    out = {}
    for cual in ("A", "B"):
        d = datos_abanico(cual)
        m = ml.ajustar(d)
        df = pd_concat_dev(d)
        e = df["y"].to_numpy() - m.predecir(df)
        a = np.abs(df["x1"].to_numpy())
        lo, hi = np.quantile(a, [0.2, 0.8])
        out[cual] = float(np.std(e[a >= hi]) / np.std(e[a <= lo]))
    return out


def pd_concat_dev(d):
    """ent ∪ val (lo que el ejercicio mira; la prueba no se toca)."""
    import pandas as pd
    return pd.concat([d.ent, d.val])


# ---------------------------------------------------------- página 2 · §1–§2 ---
# Datos de F9, F16 y nb07 B1: dos variables con correlación 0.5,
# β = (0.3, 1.5), 200 de entrenamiento (n = 334 con 0.6/0.2/0.2), estandarizadas.
D_REGIONES = 1.0
PENALIZACIONES = ("l2", "l1", "elastica")


def datos_regiones(semilla=0):
    ml = _ml()
    return ml.proceso(n=334, x={"x1": ml.normal(), "x2": ml.normal()},
                      f=lambda d: 0.3 * d["x1"] + 1.5 * d["x2"],
                      correlacion={("x1", "x2"): 0.5}, semilla=semilla)


def phi_regiones():
    ml = _ml()
    return ml.estandarizar(ml.columnas("x1", "x2"))


@functools.lru_cache(maxsize=None)
def cifras_c3_regiones():
    """P2 §2, F9: por región, d, μ equivalente y β̂ (pendientes) con el mismo d = 1.
    Además el ajuste sin penalizar y la mitad de su Ω (nb07 B1 por omisión)."""
    ml = _ml()
    d = datos_regiones()
    phi = phi_regiones()
    mc = ml.ajustar(d, phi=phi)
    b = mc.beta_gorro[["x1", "x2"]]
    out = {"mc": (float(b["x1"]), float(b["x2"]))}
    for pen in PENALIZACIONES:
        beta, mu = ml.optimo_restringido(d, phi, pen, D_REGIONES)
        omega = ml._omega(b, pen, 0.5)
        beta_m, mu_m = ml.optimo_restringido(d, phi, pen, omega / 2)
        out[pen] = {"d": D_REGIONES, "mu": float(mu),
                    "beta": (float(beta["x1"]), float(beta["x2"])),
                    "omega_mc": float(omega),
                    "mitad": {"mu": float(mu_m), "beta": (float(beta_m["x1"]), float(beta_m["x2"]))}}
    out["cita"] = {pen: {"mu": _f(out[pen]["mu"], 2),
                         "beta1": _f(out[pen]["beta"][0], 2), "beta2": _f(out[pen]["beta"][1], 2)}
                   for pen in PENALIZACIONES}
    return out


D_MARCADO = 1.0


def rejilla_presupuesto():
    """La rejilla de d de F16 y de nb07 B1: 40 valores > 0 (nunca d = 0)."""
    omega = cifras_c3_regiones()["l1"]["omega_mc"]
    return np.linspace(0.05, 1.2 * omega, 40)


@functools.lru_cache(maxsize=None)
def cifras_c3_recta_apoyo():
    """P2 §1, F16: d marcado, μ y la pendiente −μ de la recta de apoyo, con lasso
    y los datos de F9; la derivada numérica de v(d) en d marcado."""
    ml = _ml()
    d = datos_regiones()
    phi = phi_regiones()
    beta, mu = ml.optimo_restringido(d, phi, "l1", D_MARCADO)
    v = lambda x: float(ml._presupuesto(d, phi, "l1", x, 0.5)[2])
    h = 1e-4
    ds = rejilla_presupuesto()
    curva = [v(x) for x in ds]
    v0 = v(D_MARCADO)
    out = {"d": D_MARCADO, "mu": float(mu), "pendiente": -float(mu),
           "derivada": (v(D_MARCADO + h) - v(D_MARCADO - h)) / (2 * h),
           "ds": [float(x) for x in ds], "v": curva, "v_marcado": v0,
           "apoyo_min": float(min(c - (v0 - mu * (x - D_MARCADO)) for x, c in zip(ds, curva)))}
    out["cita"] = {"d": _f(D_MARCADO, 0), "mu": _f(mu, 2)}
    return out


# ---------------------------------------------------------- página 2 · §4 ---
# F11, nb07 B3: las entregas curvas de la clase 2 (n = 60, 36 de entrenamiento),
# grado 12 con estandarizar(polinomio(12, escalar=True)) y ridge.
MUS_GRADO12 = tuple(float(m) for m in np.logspace(-6, 2, 17))
MU_GRANDE, MU_CHICO = 100.0, 1e-6


def datos_entregas_curvas(semilla=0):
    return _ml().PROCESOS["entregas_curvas"](n=60, semilla=semilla)


def phi_grado12():
    ml = _ml()
    return ml.estandarizar(ml.polinomio(12, escalar=True))


def candidatos_grado12():
    ml = _ml()
    phi = phi_grado12()
    return {m: (lambda df, m=m: ml.ajustar(df, phi=phi, mu=m, penalizacion="l2"))
            for m in MUS_GRADO12}


@functools.lru_cache(maxsize=None)
def seleccion_grado12(semilla=0):
    """elegir con CV5 y orden explícito (μ de mayor a menor) y curva_capacidad."""
    ml = _ml()
    d = datos_entregas_curvas(semilla)
    cand = candidatos_grado12()
    sel = ml.elegir(d, cand, con="cv", k=5, orden_complejidad=sorted(cand, reverse=True))
    curva = ml.curva_capacidad(d, cand, conjuntos=("ent", "realidad"))
    return sel, curva


def mus_paneles_grado12():
    """(grande, medio, chico): el medio es el mínimo de CV5 en la rejilla."""
    sel, _ = seleccion_grado12()
    return (MU_GRANDE, float(sel.elegido), MU_CHICO)


@functools.lru_cache(maxsize=None)
def cifras_c3_grado12():
    """P2 §4, F11: por panel, L_ent, L_val y R; el R del grado 12 sin penalizar
    (el de la clase 2); y la U del cuarto panel sobre las 17 μ."""
    ml = _ml()
    d = datos_entregas_curvas()
    phi = phi_grado12()
    sel, curva = seleccion_grado12()
    paneles = {}
    for nombre, mu in zip(("grande", "medio", "chico"), mus_paneles_grado12()):
        m = ml.ajustar(d, phi=phi, mu=mu, penalizacion="l2")
        paneles[nombre] = {"mu": mu, "L_ent": float(ml.L(m, d.ent)),
                           "L_val": float(ml.L(m, d.val)), "R": float(ml.riesgo(m, d))}
    sin = ml.ajustar(d, phi=ml.polinomio(12, escalar=True))
    tabla = sel.tabla.set_index("candidato")
    piv = curva.pivot(index="candidato", columns="conjunto", values="L")
    mus = list(MUS_GRADO12)
    u = {"mu_min": float(sel.elegido), "mu_un_ee": float(sel.elegido_un_ee),
         "cv": {m: float(tabla.loc[m, "valor"]) for m in mus},
         "ee": {m: float(tabla.loc[m, "ee"]) for m in mus},
         "R": {m: float(piv.loc[m, "realidad"]) for m in mus},
         "L_ent": {m: float(piv.loc[m, "ent"]) for m in mus}}
    out = {"paneles": paneles, "R_sin_penalizar": float(ml.riesgo(sin, d)), "u": u,
           "piso": float(ml.piso(d)), "n_ent": len(d.ent)}
    out["cita"] = {
        "mu_grande": "100", "mu_medio": f"{u['mu_min']:.4f}".rstrip("0"),
        "mu_medio_log": _f(np.log10(u["mu_min"]), 1), "mu_chico": "10⁻⁶",
        "R": {k: _f(v["R"], 1) for k, v in paneles.items()},
        "L_val": {k: _f(v["L_val"], 1) for k, v in paneles.items()},
        "R_sin_penalizar": _f(out["R_sin_penalizar"], 0),
    }
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_grado12_vistas():
    """P2 §4 (idea 3), nb07 B3 «tres vistas»: centro y ancho (desviación) de los
    residuales de los tres paneles de F11. Se leen en la muestra enorme
    (despliegue): con 12 filas de validación el ancho no ordena los paneles
    (DECISIÓN prog-c3-2); también se devuelven los de validación."""
    ml = _ml()
    d = datos_entregas_curvas()
    phi = phi_grado12()
    out = {}
    for nombre, mu in zip(("grande", "medio", "chico"), mus_paneles_grado12()):
        m = ml.ajustar(d, phi=phi, mu=mu, penalizacion="l2")
        e = d.despliegue["y"].to_numpy() - m.predecir(d.despliegue)
        ev = d.val["y"].to_numpy() - m.predecir(d.val)
        out[nombre] = {"centro": float(e.mean()), "ancho": float(e.std()),
                       "centro_val": float(ev.mean()), "ancho_val": float(ev.std())}
    out["cita"] = {k: {"centro": _f(v["centro"], 1), "ancho": _f(v["ancho"], 1)}
                   for k, v in out.items()}
    return out


# F12, F15, nb07 B4–B5: 50 variables, 5 útiles, n = 300 (muchas_variables).
J_MUCHAS, UTILES = 50, ("x1", "x2", "x3", "x4", "x5")
MUS_TRAYECTORIAS = tuple(float(m) for m in np.logspace(-3, 1, 60))


def datos_muchas(semilla=0, gemela=False):
    ml = _ml()
    return ml.muchas_variables(n=300, J=J_MUCHAS, utiles=5,
                               gemelas={"x1": 0.95} if gemela else None, semilla=semilla)


def phi_muchas(J=J_MUCHAS):
    ml = _ml()
    return ml.estandarizar(ml.columnas(*[f"x{j}" for j in range(1, J + 1)]))


@functools.lru_cache(maxsize=None)
def tabla_trayectorias(penalizacion, semilla=0, gemela=False, rho=0.5):
    ml = _ml()
    return ml.trayectorias(datos_muchas(semilla, gemela), phi_muchas(), penalizacion,
                           MUS_TRAYECTORIAS, rho=rho)


def mu_de_apagado(tabla):
    """{coeficiente: la primera μ de la rejilla desde la cual vale 0 hasta el final}."""
    ancha = tabla.pivot(index="mu", columns="coeficiente", values="valor").sort_index()
    out = {}
    for c in ancha.columns:
        vivo = (ancha[c] != 0).to_numpy()
        if vivo[-1]:
            out[c] = None
        else:
            ult = np.where(vivo)[0]
            out[c] = float(ancha.index[ult.max() + 1]) if len(ult) else float(ancha.index[0])
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_trayectorias():
    """P2 §4, F12: μ (de la rejilla) en que lasso apaga cada útil; espurias
    vivas justo antes de apagarse la última útil; ceros de ridge en la rejilla."""
    t1 = tabla_trayectorias("l1")
    ap = mu_de_apagado(t1)
    ultima = max(ap[u] for u in UTILES)
    primera = min(ap[u] for u in UTILES)
    ancha = t1.pivot(index="mu", columns="coeficiente", values="valor").sort_index()
    antes = ancha.index[ancha.index < ultima].max()
    espurias = [c for c in ancha.columns if c not in UTILES]
    t2 = tabla_trayectorias("l2")
    out = {"apagado": {u: ap[u] for u in UTILES}, "primera_util": primera, "ultima_util": ultima,
           "espurias_vivas": int((ancha.loc[antes, espurias] != 0).sum()),
           "ceros_ridge": int((t2["valor"] == 0).sum())}
    out["cita"] = {"primera_util": _f(primera, 1), "ultima_util": _f(ultima, 1)}
    return out


@functools.lru_cache(maxsize=None)
def cifras_c3_ridge_cruza_cero():
    """nb07 B4 (Explica): correlación 0.5, β̂_MC = (1, −3), μ = 1.5: ridge da (0, −1)."""
    S = np.array([[1.0, 0.5], [0.5, 1.0]])
    b = np.array([1.0, -3.0])
    r = np.linalg.solve(S + 1.5 * np.eye(2), S @ b)
    return {"ridge": (float(r[0]), float(r[1]))}


MU_PAREJA, REPETICIONES_PAREJA = 0.3, 100


@functools.lru_cache(maxsize=None)
def cifras_c3_pareja():
    """P2 §4, nb07 B4: frecuencia con que lasso y la elástica (ρ = 0.5) conservan
    x1 y su gemela x6 (correlación 0.95) en 100 réplicas, μ = 0.3."""
    ml = _ml()
    fab = lambda s: ml.muchas_variables(n=300, J=J_MUCHAS, utiles=5, gemelas={"x1": 0.95},
                                        semilla=s, con_realidad=False)
    out = {}
    for pen in ("l1", "elastica"):
        t = ml.beta_repetido(fab, phi_muchas(), REPETICIONES_PAREJA, mu=MU_PAREJA,
                             penalizacion=pen)
        out[pen] = {"x1": float((t["x1"] != 0).mean()), "x6": float((t["x6"] != 0).mean()),
                    "ambas": float(((t["x1"] != 0) & (t["x6"] != 0)).mean())}
    out["cita"] = {pen: {k: str(round(100 * v)) for k, v in out[pen].items()}
                   for pen in ("l1", "elastica")}
    return out


MU_RIDGE_COLINEAL = 0.1


@functools.lru_cache(maxsize=None)
def tablas_ridge_colineal():
    ml = _ml()
    fab = lambda s: ml.caso(9, semilla=s, con_realidad=False)
    return {"sin": tablas_colineal()[0.99],
            "ridge": ml.beta_repetido(fab, None, REPETICIONES, mu=MU_RIDGE_COLINEAL,
                                      penalizacion="l2")}


@functools.lru_cache(maxsize=None)
def cifras_c3_ridge_colineal():
    """P2 §4, F13: media y desviación de β̂1 sin penalizar y con ridge (μ = 0.1)."""
    t = tablas_ridge_colineal()
    out = {k: {"media": float(v["x1"].mean()), "desv": float(v["x1"].std(ddof=1))}
           for k, v in t.items()}
    out["cita"] = {k: {"media": _f(v["media"], 2), "desv": _f(v["desv"], 2)}
                   for k, v in out.items()}
    return out


# ---------------------------------------------------------- página 2 · §5 ---

def mu_apagado_exacto(d, phi, variable, lo=1e-4, hi=1e9):
    """La μ (bisección en log) desde la cual lasso deja la variable en 0."""
    ml = _ml()
    cero = lambda mu: ml.ajustar(d, phi=phi, mu=float(mu), penalizacion="l1").beta_gorro[variable] == 0
    if not cero(hi):
        return None
    a, b = np.log(lo), np.log(hi)
    for _ in range(50):
        m = (a + b) / 2
        if cero(np.exp(m)):
            b = m
        else:
            a = m
    return float(np.exp(b))


@functools.lru_cache(maxsize=None)
def cifras_c3_estandarizar():
    """P2 §5, F14: el caso 10. μ de apagado de x1 y x2 sin y con estandarizar,
    y los coeficientes a la μ de referencia 2 (DECISIÓN prog-lab-12.1)."""
    ml = _ml()
    d = ml.caso(10)
    out = {}
    for nombre, phi in (("sin", ml.columnas("x1", "x2")),
                        ("con", ml.estandarizar(ml.columnas("x1", "x2")))):
        m = ml.ajustar(d, phi=phi, mu=2.0, penalizacion="l1")
        out[nombre] = {"x1": mu_apagado_exacto(d, phi, "x1"), "x2": mu_apagado_exacto(d, phi, "x2"),
                       "a_mu_2": {k: float(v) for k, v in m.beta_gorro.items() if k != "1"}}
    out["cita"] = {"sin_x1": _f(out["sin"]["x1"], 1),
                   "sin_x2": f"{out['sin']['x2']:.1e}".replace("e+0", " × 10^"),
                   "con_x1": _f(out["con"]["x1"], 1), "con_x2": _f(out["con"]["x2"], 1)}
    return out


MU_ESCALA_OBJETIVO = 0.3


@functools.lru_cache(maxsize=None)
def cifras_c3_escala_objetivo():
    """P2 §5, caso 24: no ceros de lasso con y y con 1000y a μ = 0.3; con 1000μ,
    los mismos coeficientes ×1000; ridge con la misma μ, ×1000."""
    ml = _ml()
    phi = phi_muchas(10)
    d1 = ml.muchas_variables(n=300, J=10, utiles=3, semilla=0)
    d2 = ml.caso(24)
    nz = lambda m: int((m.beta_gorro.drop("1") != 0).sum())
    a = ml.ajustar(d1, phi=phi, mu=MU_ESCALA_OBJETIVO, penalizacion="l1")
    b = ml.ajustar(d2, phi=phi, mu=MU_ESCALA_OBJETIVO, penalizacion="l1")
    c = ml.ajustar(d2, phi=phi, mu=1000 * MU_ESCALA_OBJETIVO, penalizacion="l1")
    ra = ml.ajustar(d1, phi=phi, mu=MU_ESCALA_OBJETIVO, penalizacion="l2")
    rb = ml.ajustar(d2, phi=phi, mu=MU_ESCALA_OBJETIVO, penalizacion="l2")
    out = {"no_ceros_y": nz(a), "no_ceros_1000y": nz(b), "no_ceros_1000y_1000mu": nz(c),
           "dif_lasso": float((c.beta_gorro / 1000 - a.beta_gorro).drop("1").abs().max()),
           "dif_ridge": float((rb.beta_gorro / 1000 - ra.beta_gorro).drop("1").abs().max()),
           "J": 10}
    out["cita"] = {"no_ceros_y": str(out["no_ceros_y"]), "no_ceros_1000y": str(out["no_ceros_1000y"])}
    return out


# ---------------------------------------------------------- página 2 · §6 ---
MUS_CV = tuple(float(m) for m in np.logspace(-4, 3, 30))


class _Memo:
    """construir(df) con caché por (μ, penalización, filas): elegir llamado dos
    veces con la misma partición reusa los ajustes (la CV con lasso cuesta)."""

    def __init__(self):
        self.cache = {}

    def candidatos(self, penalizacion="l1", mus=MUS_CV, phi=None):
        ml = _ml()
        phi = phi or phi_muchas()

        def construir(df, mu):
            clave = (mu, penalizacion, tuple(df.index), len(df.columns))
            if clave not in self.cache:
                self.cache[clave] = ml.ajustar(df, phi=phi, mu=mu, penalizacion=penalizacion)
            return self.cache[clave]

        return {m: (lambda df, m=m: construir(df, m)) for m in mus}


_MEMO = _Memo()


@functools.lru_cache(maxsize=None)
def selecciones_mu_cv(penalizacion="l1"):
    """Las selecciones de F15 y nb07 B5: con ent, y con CV5 por el mínimo y por un EE
    (orden explícito: μ de mayor a menor)."""
    ml = _ml()
    d = datos_muchas()
    cand = _MEMO.candidatos(penalizacion)
    orden = sorted(cand, reverse=True)
    with _silencio():
        return {
            "ent": ml.elegir(d, cand, con="ent", orden_complejidad=orden),
            "minimo": ml.elegir(d, cand, con="cv", k=5, regla="minimo", orden_complejidad=orden),
            "un_ee": ml.elegir(d, cand, con="cv", k=5, regla="un_ee", orden_complejidad=orden),
        }


@functools.lru_cache(maxsize=None)
def curvas_mu_cv():
    """F15 y la tabla de P2 §6: por cada μ de la rejilla, las pendientes distintas
    de cero y R del modelo que describe la página, el REAJUSTE con ent ∪ val
    (Seleccion.modelo con con="cv"), no el ajuste de 180 filas. L_ent va aparte
    (cifras_c3_mu_cv()["L_ent"]), con el ajuste de entrenamiento."""
    import pandas as pd
    ml = _ml()
    d = datos_muchas()
    desarrollo = pd.concat([d.ent, d.val])
    nz, R = {}, {}
    for mu, cons in _MEMO.candidatos("l1").items():
        m = cons(desarrollo)
        nz[mu] = int((m.beta_gorro.drop("1") != 0).sum())
        R[mu] = float(ml.riesgo(m, d))
    return {"no_ceros": nz, "R": R, "filas": len(desarrollo)}


@functools.lru_cache(maxsize=None)
def cifras_c3_mu_cv():
    """P2 §6, F15: μ que elige L_ent, la del mínimo de CV5 y la de un EE, con su
    CV5 ± EE, no ceros y R; L_prueba ± 2 EE del modelo final (un EE), abierta una
    vez, y la diferencia pareada contra la media (de ent ∪ val) en prueba.
    Más la mutación del orden (rejilla ascendente sin orden_complejidad)."""
    import pandas as pd
    ml = _ml()
    d = datos_muchas()
    s = selecciones_mu_cv()
    tabla = s["minimo"].tabla.set_index("candidato")
    nz = lambda m: int((m.beta_gorro.drop("1") != 0).sum())
    out = {"mu_ent": float(s["ent"].elegido), "mu_min": float(s["minimo"].elegido),
           "mu_un_ee": float(s["minimo"].elegido_un_ee)}
    for k in ("min", "un_ee"):
        mu = out[f"mu_{k}"]
        modelo = s["minimo" if k == "min" else "un_ee"].modelo
        out[k] = {"cv": float(tabla.loc[mu, "valor"]), "ee": float(tabla.loc[mu, "ee"]),
                  "no_ceros": nz(modelo), "R": float(ml.riesgo(modelo, d))}
    out["umbral"] = out["min"]["cv"] + out["min"]["ee"]
    out["L_ent"] = {m: float(ml.L(c(d.ent), d.ent))
                    for m, c in _MEMO.candidatos("l1").items()}
    # la prueba, una vez, con el procedimiento fijado (lasso, CV5, un EE)
    final = s["un_ee"].modelo_final
    l_mod = _perdidas(final, d.prueba)
    media = float(pd.concat([d.ent, d.val])["y"].mean())
    l_med = _perdidas_constante(media, d.prueba)
    dif, ee = ml.diferencia_pareada(l_mod, l_med)
    out["prueba"] = {"L": float(np.mean(l_mod)),
                     "ee": float(np.std(l_mod, ddof=1) / np.sqrt(len(l_mod))),
                     "media": float(np.mean(l_med)), "dif": float(dif), "ee_dif": float(ee),
                     "le_gana": bool(dif < -2 * ee)}
    out["R_media"] = float(ml.benchmarks(d, d.despliegue).loc["media", "cuadratica"])
    # mutación: rejilla ascendente, sin orden_complejidad
    with _silencio():
        sa = ml.elegir(d, _MEMO.candidatos("l1"), con="cv", k=5, regla="un_ee")
    out["mutacion_un_ee"] = float(sa.elegido_un_ee)
    out["cita"] = {"mu_ent": "10⁻⁴", "mu_min": _f(out["mu_min"], 2),
                   "mu_un_ee": _f(out["mu_un_ee"], 2),
                   "cv_min": _f(out["min"]["cv"], 2), "ee_min": _f(out["min"]["ee"], 2),
                   "cv_un_ee": _f(out["un_ee"]["cv"], 2), "ee_un_ee": _f(out["un_ee"]["ee"], 2),
                   "no_ceros_min": str(out["min"]["no_ceros"]),
                   "no_ceros_un_ee": str(out["un_ee"]["no_ceros"]),
                   "R_min": _f(out["min"]["R"], 2), "R_un_ee": _f(out["un_ee"]["R"], 2),
                   "L_prueba": _f(out["prueba"]["L"], 2),
                   "dos_ee_prueba": _f(2 * out["prueba"]["ee"], 2),
                   "dif_prueba": _f(out["prueba"]["dif"], 1),
                   "ee_dif_prueba": _f(out["prueba"]["ee_dif"], 1)}
    return out


# ---------------------------------------------------------- ejercicios ---

@functools.lru_cache(maxsize=None)
def cifras_c3_ejercicios():
    """Todas las cuentas de §10.5, con numpy y encoger_1d (ninguna a mano)."""
    ml = _ml()
    out = {}
    x = np.array([-2, -1, 0, 1, 2], float)
    e = np.array([2, -1, -2, -1, 2], float)
    out["cancelan"] = {"centro": float(e.mean()), "L": float(np.mean(e ** 2)),
                       "es_x2_menos_2": bool(np.allclose(e, x ** 2 - 2))}
    y = np.array([0, 0, 0, 0, 10], float)
    out["constante"] = {"mse_media": float(np.mean((y - 2) ** 2)), "mse_mediana": float(np.mean(y ** 2)),
                        "mae_media": float(np.mean(np.abs(y - 2))), "mae_mediana": float(np.mean(np.abs(y)))}
    r = np.array([1.0] * 99 + [50.0])
    out["cola"] = {"mse": float(np.mean(r ** 2)), "frac_mse": float(2500 / np.sum(r ** 2)),
                   "mae": float(np.mean(r)), "frac_mae": float(50 / np.sum(r))}
    out["pendiente"] = 2 + 3 * 0.5
    out["colineal"] = {"desv_0": float(np.sqrt(1 / (100 * 1 * (1 - 0 ** 2)))),
                       "desv_09": float(np.sqrt(1 / (100 * 1 * (1 - 0.9 ** 2))))}
    out["colineal"]["razon"] = out["colineal"]["desv_09"] / out["colineal"]["desv_0"]
    out["factor_099"] = 1 / (1 - 0.99 ** 2)
    # esquina: (0.3, 2), d = 1, ortonormal. Lasso: proyección sobre el diamante.
    b = np.array([0.3, 2.0])
    mu_l = _mu_restringido_ortonormal(b, "l1", 1.0)
    mu_r = _mu_restringido_ortonormal(b, "l2", 1.0)
    out["esquina"] = {"lasso": tuple(float(v) for v in ml.encoger_1d(b, mu_l, "l1")), "mu_lasso": mu_l,
                      "ridge": tuple(float(v) for v in ml.encoger_1d(b, mu_r, "l2")), "mu_ridge": mu_r}
    b2 = np.array([3.0, 0.4])
    out["cero_a_mano"] = {p: tuple(float(v) for v in ml.encoger_1d(b2, 1.0, p, rho=0.5))
                          for p in ("l2", "l1", "elastica")}
    out["umbral_que_apaga"] = "μ/2"
    return out


def _mu_restringido_ortonormal(b, penalizacion, d):
    """μ con Ω(encoger_1d(b, μ)) = d (diseño ortonormal), por bisección."""
    ml = _ml()
    om = lambda mu: ml._omega(ml.encoger_1d(b, mu, penalizacion), penalizacion, 0.5)
    if om(0.0) <= d:
        return 0.0
    lo, hi = 0.0, 1.0
    while om(hi) > d:
        hi *= 2
    for _ in range(200):
        m = (lo + hi) / 2
        if om(m) > d:
            lo = m
        else:
            hi = m
    return float(hi)



@functools.lru_cache(maxsize=None)
def cifras_c3_interaccion():
    """P1 §4, F6 (alt): caso 7 con semilla 0, L_val de la recta en x1, x2 sin y con
    la columna x1·x2 (la silla de residuales y el ruido sin forma)."""
    ml = _ml()
    d = ml.caso(7)
    sin = ml.ajustar(d, phi=ml.columnas("x1", "x2"))
    con = ml.ajustar(d, phi=ml.combinar(ml.columnas("x1", "x2"),
                                        ml.interacciones(("x1", "x2"))))
    out = {"L_val_sin": float(ml.L(sin, d.val)), "L_val_con": float(ml.L(con, d.val))}
    out["cita"] = {"L_val_sin": _f(out["L_val_sin"], 2), "L_val_con": _f(out["L_val_con"], 2)}
    return out

# --- fin tramo rapido ---


# --- tramo completo ---
# --------------------------------------------------- tarea 3 · cincuenta variables ---
# El proceso que escribe el bloque 1 de tarea_3_cincuenta_variables.py, copiado
# aquí para medir sus criterios (clase_3.md §10.6.1): 50 normales, 5 útiles con
# coeficientes (3, −2, 1.5, 1, 0.5) en unidades estándar, x6 gemela de x1 con
# corr 0.95, ruido N(0, 1), n = 300 con 0.6/0.2/0.2, escalas 10^((j mod 10) − 4).
# Las escalas bajan una década respecto del plan (1e-3 … 1e6): con 1e-2 la útil
# x1 (coeficiente 3) sobrevivía sin estandarizar en μ = 0.01 y el criterio (b)
# no se cumplía con ninguna rejilla que dejara el mínimo estandarizado adentro
# (DECISIÓN prog-c3-6).

J_TAREA, N_TAREA = 50, 300
COEF_TAREA = {"x1": 3.0, "x2": -2.0, "x3": 1.5, "x4": 1.0, "x5": 0.5}
MUS_TAREA = [float(m) for m in np.logspace(-2, 1, 16)]


def escalas_tarea():
    return {f"x{j}": 10.0 ** ((j % 10) - 4) for j in range(1, J_TAREA + 1)}


def datos_tarea(semilla=0, con_realidad=False):
    ml = _ml()
    x = {f"x{j}": ml.normal() for j in range(1, J_TAREA + 1)}
    f = lambda d: sum(c * d[v] for v, c in COEF_TAREA.items())  # noqa: E731
    return ml.proceso(n=N_TAREA, x=x, f=f, ruido=ml.normal(0, 1),
                      correlacion={("x1", "x6"): 0.95}, escala=escalas_tarea(),
                      semilla=semilla, con_realidad=con_realidad)


@functools.lru_cache(maxsize=None)
def seleccion_tarea(semilla=0, estandarizar=True):
    """Lasso elegido con CV₅ (mínimo; orden μ decreciente) sobre la rejilla de la
    tarea: (μ del mínimo, μ de un EE, útiles vivas en el modelo final)."""
    ml = _ml()
    cols = ml.columnas(*[f"x{j}" for j in range(1, J_TAREA + 1)])
    phi = ml.estandarizar(cols) if estandarizar else cols
    cand = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=phi, mu=mu, penalizacion="l1"))
            for mu in MUS_TAREA}
    with _silencio():
        sel = ml.elegir(datos_tarea(semilla), cand, con="cv", k=5, regla="minimo",
                        orden_complejidad=sorted(MUS_TAREA, reverse=True))
    b = sel.modelo_final.beta_gorro
    return sel.elegido, sel.elegido_un_ee, tuple(u for u in COEF_TAREA if b[u] != 0)


@functools.lru_cache(maxsize=None)
def cifras_c3_tarea():
    """Lo que la página de la tarea y su guion citan del montaje (no de resultados)."""
    n_ent = int(round(0.6 * N_TAREA))
    out = {"n": N_TAREA, "n_ent": n_ent, "J": J_TAREA, "utiles": len(COEF_TAREA),
           "mus": len(MUS_TAREA), "mu_min": MUS_TAREA[0], "mu_max": MUS_TAREA[-1]}
    out["cita"] = {"n": str(N_TAREA), "n_ent": str(n_ent), "J": str(J_TAREA),
                   "utiles": str(len(COEF_TAREA)), "corr_gemela": "0.95"}
    return out

# --- fin tramo completo ---
