"""Fija en la fuente las cifras de la clase 4 (tools/ml_cifras_c4.py).

Sin prosa (D-003): estas pruebas no leen ninguna pagina. Que la pagina cite la
misma cifra lo comprueba tools/test_ml_prosa_c4.py. Cada criterio es el de
clase_4.md §10.7 (tabla de ml_cifras_c4 y «pruebas extra») y cada forma
citada («cita») se fija literal en CITAS: si una cifra cambia, esta prueba
falla y obliga a revisar la prosa y los briefs. Las cifras se comprobaron
iguales con numpy 1.26 + sklearn 1.5.1 (python3 del sistema) y con
sklearn 1.6.1 (venv 3.12) (C4.T5, R2).
"""
import ast
import json
import math
import re
import warnings
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c4 as c  # noqa: E402

warnings.simplefilter("ignore")
TOOLS = Path(__file__).resolve().parent


def _ml():
    return c._ml()


def _norm(v):
    return json.loads(json.dumps(v, ensure_ascii=False, sort_keys=True, default=str))


CITAS = {
    'cifras_c4_anillos': {"corte_mejor": "0.41", "cuadratica": "0.82", "cuadratica_pesos": "0.73", "lineal": "0.00", "lineal_pesos": "0.02", "mejor_corte": "0.83", "mejor_semiespacio": "0.22", "regla_aciertos": "0.83", "regla_balanceada": "0.78"},
    'cifras_c4_banda_no_medibles': {"medibles": "140", "no_medibles": "60", "tamano": "120", "total": "200"},
    'cifras_c4_bootstrap_aciertos': {"aciertos": "0.900", "dos_ee": "0.055", "ee_estratificado": "0", "ee_filas": "0.030", "intervalo": ["0.842", "0.950"]},
    'cifras_c4_bootstrap_aciertos_exacto': {"ee_estratificado": "0", "ee_filas": "0.030"},
    'cifras_c4_calibracion': {"brier_benchmark": "0.044", "brier_con": "0.133", "brier_recalibrado": "0.037", "brier_sin": "0.036", "log_benchmark": "0.189", "log_con": "0.416", "log_recalibrado": "0.129", "log_sin": "0.127", "n_val_b": "300", "p_con": "0.313", "p_rec": "0.044", "p_sin": "0.051", "prob_real": "0.050"},
    'cifras_c4_cinco_puntajes': {"sexto": ["5", "0.8", "{0,1,2}"], "tercio": ["4", "0.6", "{0}"]},
    'cifras_c4_cliente_tipico': {"p_w": "0.5", "razon": "19"},
    'cifras_c4_conformal_cobertura': {"fraudes_cal3": "18", "marginal_fraude": "0.01", "marginal_global": "0.89", "marginal_tamano": "0.98", "n_cal3": "1000", "por_clase_fraude": "0.83", "por_clase_global": "0.92", "por_clase_tamano": "1.80"},
    'cifras_c4_conformal_equilibrado': {"cobertura_01": "0.90", "tamano_01": "1.94"},
    'cifras_c4_conformal_repetido': {"R": "30", "marginal_fraude": "0.03", "por_clase": ["0.90", "0.90", "0.90"], "por_clase_fraude": "0.90"},
    'cifras_c4_contribucion': {"constante_frac_positivos": "0.82", "frac_casos_fraude_1": "0.009", "frac_peso_balanceado": "1/2", "perdida_media_fraude_1": "3.41", "perdida_media_legitimo_1": "0.009"},
    'cifras_c4_desbalanceo': {"banda_01": "0.24", "banda_50": "0.16"},
    'cifras_c4_dos_reglas': {"A": {"aciertos": "0.75", "mcc": "0.577", "perdida": "0.186"}, "B": {"aciertos": "1", "mcc": "1", "perdida": "0.511"}},
    'cifras_c4_final_p1': {"moda": ["0.9", "1/3", "0"], "raros_por_pliegue_k5": "4", "w": ["0.370", "4.17", "16.7"]},
    'cifras_c4_final_p2': {"fraude": "0.01", "fraude_pesos": "0.91", "global": "0.89", "global_pesos": "0.91", "minimo": "9", "tamano": "0.98", "tamano_pesos": "2.00"},
    'cifras_c4_mcc_por_pliegue': {"fraudes_ent": "14", "max_mcc_10": "0.39", "mcc_despliegue": "0.21", "min_mcc_10": "-0.06", "rango_mcc": {"10": "0.45", "3": "0.07", "5": "0.23"}},
    'cifras_c4_mcc_un_fraude': {"A": {"aciertos_balanceados": "0.990", "mcc": "0.571"}, "B": {"aciertos_balanceados": "0.5", "mcc": "0"}},
    'cifras_c4_minimo_por_clase': {"minimo": "9"},
    'cifras_c4_moda': {"dos": {"aciertos": "0.98", "aciertos_balanceados": "0.5", "mcc": "0"}, "entropia": {"0.01": "0.056", "0.02": "0.098", "0.05": "0.199", "0.1": "0.325", "0.2": "0.500", "0.5": "0.693"}, "uno": {"aciertos": "0.99", "aciertos_balanceados": "0.5", "mcc": "0"}},
    'cifras_c4_multiclase': {"con": {"aciertos": "0.57", "aciertos_balanceados": "0.65", "mcc": "0.22", "por_clase": ["0.56", "0.65", "0.73"]}, "sin": {"aciertos": "0.90", "aciertos_balanceados": "0.36", "mcc": "0.16", "por_clase": ["1.00", "0.05", "0.02"]}},
    'cifras_c4_noticias': {"aciertos": ["0.900", "0.667", "0.500"], "macro": "0.689", "mcc": "0.611", "ponderado": "0.778", "precision": ["0.857", "0.800", "0.400"], "soporte": "100/60/20"},
    'cifras_c4_noventa_global': {"falta": "0.0082", "fraude": "0.41", "parcial": "0.8918"},
    'cifras_c4_pesos_balanceados': {"suma": "1000", "umbral": "0.05", "w0": "0.526", "w1": "10"},
    'cifras_c4_pesos_intercepto': {"coincidencia": "98.1", "ln_razon": "2.94", "p_con": "0.244", "p_sin": "0.047", "pendientes_con": "2.50", "pendientes_sin": "2.22", "prob_real": "0.050", "salto": "2.67"},
    'cifras_c4_pesos_mal_especificado': {"con": "0.41", "sin": "0.66"},
    'cifras_c4_pesos_punto': {"p_w": "0.50", "umbral": "0.1"},
    'cifras_c4_platt': {"beta0": "-3.08", "beta1": "0.78", "menos_ln_razon": "-3.03"},
    'cifras_c4_quien_manda': {"macro": "1/3", "mcc": "0", "ponderado": "0.98", "por_clase": "(1, 0, 0)"},
    'cifras_c4_razon_por_metrica': {"abal_max": "0.793", "aciertos_1": "0.953", "aciertos_100": "0.456", "mcc": ["0.276", "0.356", "0.361", "0.297", "0.176"], "mcc_max": "0.362", "razon_abal": "19", "razon_mcc": "4.4"},
    'cifras_c4_separable': {"por_decada": "3.6", "por_decada_ruido": "0.00"},
    'cifras_c4_tamanos': {"cal3_10000": "18", "cal3_2000": "4"},
    'cifras_c4_tasa': {"con": "1", "con_pct": "100 %", "sin": "0.053"},
    'cifras_c4_umbral': {"mcc_des_05": "0.38", "mcc_des_elegido": "0.40", "mcc_val_05": "0.33", "mcc_val_elegido": "0.51", "tau": "0.18"},
}


@pytest.mark.parametrize("nombre", sorted(CITAS))
def test_cita_literal(nombre):
    """Cada forma citada, literal: la prosa y los briefs copian estas cadenas."""
    assert _norm(getattr(c, nombre)()["cita"]) == CITAS[nombre]


def test_toda_funcion_de_cifras_tiene_su_cita_fijada():
    funciones = {n for n in dir(c) if n.startswith("cifras_c4_")}
    assert funciones == set(CITAS)


# ---------------------------------------------------------------- exactas ---

def test_moda_y_entropias():
    m = c.cifras_c4_moda()
    assert m["moda"][0.01] == {"aciertos": 0.99, "aciertos_balanceados": 0.5, "mcc": 0.0}
    assert m["moda"][0.02] == {"aciertos": 0.98, "aciertos_balanceados": 0.5, "mcc": 0.0}
    for p, h in m["entropia"].items():
        assert h == pytest.approx(-p * math.log(p) - (1 - p) * math.log(1 - p))


def test_dos_reglas():
    m = c.cifras_c4_dos_reglas()
    assert m["A"]["perdida"] < m["B"]["perdida"]
    assert m["B"]["aciertos"] == 1 and m["B"]["mcc"] == pytest.approx(1)
    assert m["A"]["mcc"] == pytest.approx(1 / math.sqrt(3))


def test_pesos_punto_y_balanceados():
    assert c.cifras_c4_pesos_punto()["p_w"] == pytest.approx(0.5)
    b = c.cifras_c4_pesos_balanceados()
    assert b["w0"] == pytest.approx(1000 / 1900) and b["w1"] == pytest.approx(10)
    assert b["suma"] == pytest.approx(1000) and b["umbral"] == pytest.approx(0.05)
    t = c.cifras_c4_cliente_tipico()
    assert t["razon"] == pytest.approx(19) and t["p_w"] == pytest.approx(0.5)


def test_mutacion_pesos_balanceados():
    """Cambiar w_y = n/(K n_y) por n_y/(K n) hace fallar la cifra (S1)."""
    y = np.r_[np.zeros(950, int), np.ones(50, int)]
    n, K = len(y), 2
    bien = {k: n / (K * (y == k).sum()) for k in (0, 1)}
    mal = {k: (y == k).sum() / (K * n) for k in (0, 1)}
    b = c.cifras_c4_pesos_balanceados()
    assert (b["w0"], b["w1"]) == pytest.approx((bien[0], bien[1]))
    assert (b["w0"], b["w1"]) != pytest.approx((mal[0], mal[1]))


def test_mcc_un_fraude_contra_sklearn():
    from sklearn.metrics import matthews_corrcoef
    m = c.cifras_c4_mcc_un_fraude()
    assert m["A"]["mcc"] == pytest.approx(97 / math.sqrt(3 * 1 * 99 * 97))
    y = np.r_[1, np.zeros(99, int)]
    yg = np.r_[1, 1, 1, np.zeros(97, int)]
    assert m["A"]["mcc"] == pytest.approx(matthews_corrcoef(y, yg))
    assert m["B"]["mcc"] == 0 and m["B"]["aciertos_balanceados"] == 0.5


def test_noticias_y_quien_manda_contra_sklearn():
    from sklearn.metrics import matthews_corrcoef
    n = c.cifras_c4_noticias()
    y, yg = c.y_noticias()
    assert n["mcc"] == pytest.approx(matthews_corrcoef(y, yg))
    assert n["macro"] == pytest.approx(np.mean(n["aciertos"]))
    assert n["ponderado"] == pytest.approx(np.mean(y == yg))
    q = c.cifras_c4_quien_manda()
    assert q["por_clase"] == (1.0, 0.0, 0.0) and q["macro"] == pytest.approx(1 / 3)
    assert q["ponderado"] == pytest.approx(0.98) and q["mcc"] == 0


def test_final_p1():
    f = c.cifras_c4_final_p1()
    assert f["w"][0] == pytest.approx(1000 / 2700) and f["w"][2] == pytest.approx(1000 / 60)
    assert f["raros_por_pliegue_k5"] == 4


@pytest.mark.parametrize("n_cal,delta,esperado", [
    (5, Fraction(1, 3), 4), (5, Fraction(1, 6), 5), (9, Fraction(1, 10), 9), (8, Fraction(1, 10), 9)])
def test_rango_conformal_exacto(n_cal, delta, esperado):
    assert int(_ml()._rango_conformal(n_cal, delta)) == esperado
    assert c.rango_conformal(n_cal, delta) == esperado


def test_corte_infinito_y_empates():
    """El índice que pasa de n_cal da ĉ = ∞; los puntajes empatados entran."""
    ml = _ml()
    assert int(ml._rango_conformal(8, Fraction(1, 10))) > 8
    m = c.cifras_c4_minimo_por_clase()
    assert m["minimo"] == 9
    cinco = c.cifras_c4_cinco_puntajes()
    assert cinco["tercio"]["conjunto"] == (0,) and cinco["sexto"]["conjunto"] == (0, 1, 2)
    # empate: un puntaje nuevo igual al corte entra
    assert 0.6 <= cinco["tercio"]["corte"]


def test_noventa_global_y_tasa():
    g = c.cifras_c4_noventa_global()
    assert g["fraude"] == pytest.approx(0.41)
    t = c.cifras_c4_tasa()
    assert t["sin"] == pytest.approx(0.05 / 0.95) and t["con"] == 1


def test_bootstrap_contraejemplo():
    e = c.cifras_c4_bootstrap_aciertos_exacto()
    assert e["ee_estratificado"] == 0 and e["ee_filas"] == pytest.approx(0.03)
    b = c.cifras_c4_bootstrap_aciertos()
    lo, hi = b["intervalo_filas"]
    # con A, el bootstrap por filas y ±2 EE dan casi lo mismo
    assert abs((hi - lo) / 2 - 2 * b["ee"]) < 0.01


# -------------------------------------------------------- procesos hilo ---

def test_fuente_unica_caso_18():
    ml = _ml()
    a = ml.caso(18)
    b = ml.PROCESOS["fraude"](n=1000, proporcion=0.01)
    for parte in ("ent", "val", "prueba"):
        assert getattr(a, parte).equals(getattr(b, parte))


def test_caso_25_por_numero_y_por_nombre():
    ml = _ml()
    assert ml.caso(25).ent.equals(ml.caso("rara_en_el_centro").ent)


def test_ningun_cuaderno_de_la_clase_4_redefine_los_procesos():
    patron = re.compile(r"^(fraude|mensajes3) *= *lambda|def (fraude|mensajes3)\b", re.M)
    coef = re.compile(r"1\.5 \* d\.x1 \+ 1\.0 \* d\.x2|1\.2 \* d\.x1 - 0\.4 \* d\.x2")
    for stem in ("08_perdida_metrica_y_desbalanceo", "09_calibracion_y_conformal",
                 "tarea_4_desbalanceo_multiclase"):
        p = TOOLS / "cuadernos_ml" / f"{stem}.py"
        if not p.exists():
            pytest.skip(f"{p.name} todavía no existe")
        texto = p.read_text()
        assert not patron.search(texto), p.name
        assert not coef.search(texto), p.name


# ------------------------------------------------------ simulación · P1 ---

def test_separable_sube_lo_mismo_por_decada():
    s = c.cifras_c4_separable()
    sub = s["separable"]["subidas_media_decada"]
    assert min(sub) > 0.5 * s["separable"]["por_decada"]  # casi constante y positiva
    assert max(sub) < 10 * min(sub)
    normas = s["separable"]["normas"]
    assert all(normas[a] / normas[b] < 2 for a, b in zip(sorted(normas)[:-1], sorted(normas)[1:]) if a <= 1e-3)
    assert s["ruido"]["por_decada"] < 0.05
    for mu in s["mus_figura"]:
        assert any(math.isclose(mu, m) for m in c.MUS_SEPARABLE)


def test_umbral_elegido_en_validacion():
    u = c.cifras_c4_umbral()
    assert u["mcc"]["elegido"]["val"] >= u["mcc"]["05"]["val"]
    # la cifra de validación del τ elegido sale optimista frente al despliegue
    assert u["mcc"]["elegido"]["val"] > u["mcc"]["elegido"]["despliegue"]


def test_desbalanceo_criterio():
    d = c.cifras_c4_desbalanceo()["tabla"]
    assert d[("balanceado", "mcc", 0.01)][0] > d[("sin pesos", "mcc", 0.01)][0]
    assert d[("balanceado", "aciertos_balanceados", 0.01)][0] > d[("sin pesos", "aciertos_balanceados", 0.01)][0]
    assert d[("balanceado", "aciertos", 0.01)][0] < d[("sin pesos", "aciertos", 0.01)][0]
    assert d[("moda", "mcc", 0.01)][0] == 0
    b = c.cifras_c4_desbalanceo()["banda"]
    assert b[0.01]["desv"] > b[0.5]["desv"]


def test_banda_no_medibles_son_las_que_ml_lab_descarta():
    """La cuenta reproduce las validaciones de ml_lab: con el modelo balanceado de la
    primera repetición, A_bal es nan justo en esas, y la desviación sin ellas es la
    de la tabla (nanstd). El MCC de esas mismas validaciones vale 0, no nan."""
    ml = _ml()
    k = c.cifras_c4_banda_no_medibles(0.01)
    datos0 = ml.PROCESOS["fraude"](n=600, semilla=0, proporcion=0.01)
    mod = ml.ajustar(datos0, pesos="balanceado")
    rng = np.random.default_rng([0, 9, k["tamano"]])
    abal, mccs = [], []
    for _ in range(k["total"]):
        f = ml._fresca(datos0, k["tamano"], rng)
        abal.append(ml._metrica_con_tau(mod, f, "aciertos_balanceados", 0.5))
        mccs.append(ml._metrica_con_tau(mod, f, "mcc", 0.5))
    abal, mccs = np.asarray(abal, float), np.asarray(mccs, float)
    assert int(np.isnan(abal).sum()) == k["no_medibles"] > 0
    assert not np.isnan(mccs).any()
    t = c.tabla_desbalanceo()
    f = t[(t["conjunto"] == "val") & (t["metrica"] == "aciertos_balanceados")
          & (t["modelo"] == "balanceado") & np.isclose(t["proporcion"], 0.01)]
    assert math.isclose(float(f["desv"].iloc[0]), float(np.nanstd(abal, ddof=1)), rel_tol=1e-9)


def test_contribucion():
    t = c.cifras_c4_contribucion()
    assert t["constante_frac_positivos"] == pytest.approx(0.82, abs=0.005)
    bal = t["tablas"][(0.01, "balanceado")]
    for k in (0, 1):
        assert c._col(bal, k, "fraccion_peso") == pytest.approx(0.5)
    sin = t["tablas"][(0.01, None)]
    assert c._col(sin, 1, "perdida_media") > 10 * c._col(sin, 0, "perdida_media")


def test_pesos_intercepto_y_razon_por_metrica():
    p = c.cifras_c4_pesos_intercepto()
    assert p["coincidencia"] > 0.95
    assert 0.8 * p["ln_razon"] < p["salto"] < 1.2 * p["ln_razon"]
    assert p["p_con"] > 3 * p["prob_real"]
    r = c.cifras_c4_razon_por_metrica()
    assert 3 <= r["mejor_razon"]["mcc"] <= 6
    assert r["mejor_razon"]["aciertos_balanceados"] == pytest.approx(19, rel=0.05)
    assert r["mejor_razon"]["aciertos"] == pytest.approx(1)
    mcc = [r["por_razon"][k]["mcc"] for k in c.RAZONES_METRICA]
    assert mcc[0] < max(mcc) and mcc[-1] < max(mcc)  # a los dos lados del máximo


def test_pesos_mal_especificado_decide_r7():
    """R7: la cifra NO sostiene que pesar gane a mover τ: el Piensa lleva la segunda respuesta."""
    assert c.cifras_c4_pesos_mal_especificado()["sostiene"] is False


def test_anillos_poblacional_primero_y_ajustado():
    a = c.cifras_c4_anillos()
    assert a["mcc_regla_aciertos"] > 0.75 and a["mcc_regla_balanceada"] > 0.7
    assert a["mcc_mejor_corte"] >= a["mcc_regla_aciertos"] and a["corte_mejor"] < 0.5
    assert 0.18 < a["mcc_mejor_semiespacio"] < 0.25
    aj = a["ajustados"]
    assert aj["lineal_pesos"] < 0.15 < 0.5 < aj["cuadratica_pesos"]
    assert aj["cuadratica_pesos"] < aj["cuadratica"]


def test_mcc_por_pliegue_rango_crece_con_k():
    m = c.cifras_c4_mcc_por_pliegue()
    assert m["por_k"][10]["rango_mcc"] > m["por_k"][3]["rango_mcc"]
    for k in c.KS_PLIEGUE:
        assert len(m["por_k"][k]["mcc"]) == k


def test_multiclase_pesos():
    m = c.cifras_c4_multiclase()
    assert m["sin"]["por_clase"][2] < 0.3 < 0.6 < m["con"]["por_clase"][2]
    assert m["con"]["mcc"] > m["sin"]["mcc"]


# ------------------------------------------------------ simulación · P2 ---

def test_calibracion_y_platt():
    k = c.cifras_c4_calibracion()
    assert k["con"]["brier"] > k["sin"]["brier"] and k["recalibrado"]["brier"] < k["con"]["brier"]
    assert k["con"]["p_promedio_realidad"] > 3 * k["prob_real"]
    assert k["n_val_b"] == 300
    p = c.cifras_c4_platt()
    assert p["beta0"] == pytest.approx(p["menos_ln_razon"], abs=0.5)
    assert 0.6 < p["beta1"] < 1.2


def test_conformal_criterio_y_tamanos():
    k = c.cifras_c4_conformal_cobertura()
    assert k["marginal"]["por_clase"][2] <= 0.6
    t = c.cifras_c4_tamanos()
    assert t["cal3_10000"] >= 9 > t["cal3_2000"]


def test_conformal_promediado_sobre_calibraciones():
    """La garantía promedia sobre calibraciones: [1−δ−3EE, 1−δ+1/(n_cal+1)+3EE]."""
    r = c.cifras_c4_conformal_repetido()
    g, ee = r["marginal"]["global"], r["marginal"]["ee_global"]
    n_cal = 1000
    assert 0.9 - 3 * ee <= g <= 0.9 + 1 / (n_cal + 1) + 3 * ee
    for y in range(3):
        assert r["por_clase"]["media"][y] >= 0.9 - 3 * r["por_clase"]["ee"][y]
    assert r["marginal"]["media"][2] <= 0.6


# --------------------------------------------- pruebas numéricas de teoremas ---

@pytest.mark.parametrize("eta,razon", [(0.1, 9), (0.05, 19), (0.3, 2), (0.6, 0.5), (0.9, 5)])
def test_teorema_de_los_pesos_contra_optimizacion(eta, razon):
    from scipy.optimize import minimize_scalar
    f = lambda p: -razon * eta * math.log(p) - (1 - eta) * math.log(1 - p)  # noqa: E731
    r = minimize_scalar(f, bounds=(1e-9, 1 - 1e-9), method="bounded", options={"xatol": 1e-10})
    assert r.x == pytest.approx(c.p_ponderada(eta, razon), abs=1e-6)


def _softmax_objetivo(B, X, y, mu, K):
    Z = X @ B.reshape(K, -1).T
    Z = Z - Z.max(1, keepdims=True)
    lp = Z - np.log(np.exp(Z).sum(1, keepdims=True))
    pend = B.reshape(K, -1)[:, 1:]
    return -lp[np.arange(len(y)), y].mean() + mu * (pend ** 2).sum()


def test_softmax_k2_es_logistica_con_mu_medio():
    from scipy.optimize import minimize
    rng = np.random.default_rng(0)
    x = rng.normal(size=200)
    y = (rng.random(200) < 1 / (1 + np.exp(-(0.5 + 2 * x)))).astype(int)
    X = np.c_[np.ones(200), x]
    mu = 0.05
    s = minimize(_softmax_objetivo, np.zeros(4), args=(X, y, mu, 2), method="BFGS",
                 options={"gtol": 1e-10}).x.reshape(2, 2)
    d = s[1] - s[0]

    def logit(b):
        z = X @ b
        return np.mean(np.logaddexp(0, z) - y * z) + (mu / 2) * b[1] ** 2
    lg = minimize(logit, np.zeros(2), method="BFGS", options={"gtol": 1e-10}).x
    assert d == pytest.approx(lg, abs=1e-4)
    assert s[1, 1] == pytest.approx(-s[0, 1], abs=1e-4)  # pendientes opuestas


def test_unicidad_de_softmax():
    """Con μ = 0 y tres clases vistas solo en x = 0, dos mínimos anuncian distinto en x = 1;
    con μ = 10⁻², dos arranques dan las mismas probabilidades en x = 1."""
    from scipy.optimize import minimize
    X = np.c_[np.ones(30), np.zeros(30)]
    y = np.repeat([0, 1, 2], 10)
    x1 = np.array([1.0, 1.0])

    def prob(B):
        z = B.reshape(3, 2) @ x1
        return np.exp(z - z.max()) / np.exp(z - z.max()).sum()
    a = np.array([0, 2.0, 0, 0, 0, -2.0])
    b = np.array([0, -2.0, 0, 0, 0, 2.0])
    assert _softmax_objetivo(a, X, y, 0, 3) == pytest.approx(_softmax_objetivo(b, X, y, 0, 3))
    assert np.argmax(prob(a)) != np.argmax(prob(b))
    sols = [minimize(_softmax_objetivo, x0, args=(X, y, 1e-2, 3), method="BFGS",
                     options={"gtol": 1e-12}).x for x0 in (a, b)]
    assert prob(sols[0]) == pytest.approx(prob(sols[1]), abs=1e-6)


def test_clase_ausente_intercepto_sin_tope():
    """Con una clase ausente, bajar su intercepto siempre baja el objetivo (aun con μ > 0):
    no hay mínimo finito, y el optimizador lo baja más mientras más se le deje correr."""
    from scipy.optimize import minimize
    X = np.c_[np.ones(40), np.random.default_rng(1).normal(size=40)]
    y = np.repeat([0, 1], 20)  # la clase 2 no aparece
    r = minimize(_softmax_objetivo, np.zeros(6), args=(X, y, 1e-2, 3), method="BFGS")
    B = r.x.reshape(3, 2)
    valores = []
    for t in (5, 10, 20, 40):
        Bt = B.copy()
        Bt[2, 0] = B[:2, 0].mean() - t
        valores.append(_softmax_objetivo(Bt.ravel(), X, y, 1e-2, 3))
    assert all(a > b for a, b in zip(valores, valores[1:]))


# ------------------------------------------------ guarda estática de la tarea ---

def _llamadas_bloques_1_a_5(texto):
    """(bloque, función, [argumentos como texto]) de cada ml.<f>( de los bloques 1–5."""
    out = []
    bloque = 0
    celdas = re.split(r"^# %% ", texto, flags=re.M)
    for celda in celdas:
        cab = celda.split("\n", 1)[0]
        m = re.search(r"bloque-(\d)", cab)
        if m:
            bloque = int(m.group(1))
        if not 1 <= bloque <= 5:
            continue
        cuerpo = celda.split("\n", 1)[1] if "\n" in celda else ""
        try:
            arbol = ast.parse(cuerpo)
        except SyntaxError:
            continue
        for nodo in ast.walk(arbol):
            if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                    and isinstance(nodo.func.value, ast.Name) and nodo.func.value.id == "ml"):
                args = [ast.unparse(a) for a in nodo.args] + [ast.unparse(k.value) for k in nodo.keywords]
                out.append((bloque, nodo.func.attr, args))
    return out


def _guarda_tarea(texto):
    llamadas = _llamadas_bloques_1_a_5(texto)
    prohibidos = {"datos.val", "cal", "datos.prueba"}
    partir = 0
    benchmarks = []
    for bloque, f, args in llamadas:
        if f == "partir" and bloque == 1:
            partir += 1
            continue
        if f == "benchmarks":
            benchmarks.append(args)
        malos = prohibidos.intersection(args)
        assert not malos, f"bloque {bloque}: ml.{f} recibe {malos}"
    assert partir == 2, "el bloque 1 aparta cal y después val_a/val_b con dos ml.partir"
    assert benchmarks and all(a[1] == "val_b" for a in benchmarks), "ml.benchmarks evalúa en val_b"
    assert all(any("criterios" in x or x.startswith("(") for x in a[2:]) for a in benchmarks)


def _texto_tarea():
    p = TOOLS / "cuadernos_ml" / "tarea_4_desbalanceo_multiclase.py"
    if not p.exists():
        pytest.skip("la tarea 4 todavía no existe")
    return p.read_text()


def test_guarda_estatica_de_la_tarea():
    _guarda_tarea(_texto_tarea())


def test_guarda_estatica_de_la_tarea_mutacion():
    """Cambiar val_b por datos.val en la llamada a benchmarks hace fallar la guarda."""
    texto = _texto_tarea()
    mutado = re.sub(r"ml\.benchmarks\(datos, val_b", "ml.benchmarks(datos, datos.val", texto)
    assert mutado != texto
    with pytest.raises(AssertionError):
        _guarda_tarea(mutado)


# Revisión ronda 1 (H9): la fuente fija μ = MU_MULTICLASE para conformal,
# mientras el NB09 (bloques 3 y 4) elige μ por CV estratificada entre
# 1, 0.1, 0.01 y 0.001 con pérdida logarítmica. Las cifras que cita la página
# solo valen para el notebook si la CV elige ese mismo μ en los tres casos.
@pytest.mark.parametrize("n,proporcion", [(10_000, (1 / 3, 1 / 3, 1 / 3)),
                                          (2000, (0.9, 0.08, 0.02)),
                                          (10_000, (0.9, 0.08, 0.02))])
def test_la_cv_del_nb09_elige_el_mu_de_la_fuente(n, proporcion):
    import aprendizaje_maquina as ml
    d = ml.PROCESOS["mensajes3"](n=n, semilla=0, proporcion=list(proporcion))
    phi = ml.estandarizar(ml.columnas("x1", "x2"))
    cands = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=phi, mu=mu, penalizacion="l2"))
             for mu in [1.0, 0.1, 0.01, 1e-3]}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        elegido = ml.elegir(d.ent, cands, con="cv", particion="estratificado",
                            criterio="logaritmica").elegido
    assert elegido == c.MU_MULTICLASE
