"""Fija en la fuente las cifras de la clase 3 (tools/ml_cifras_c3.py).

Sin prosa (D-003): estas pruebas no leen ninguna pagina. Que la pagina cite
la misma cifra lo comprueba tools/test_ml_prosa_c3.py. Cada criterio es el de
clase_3.md §10.7.3 (lo que la pagina afirma) y cada forma citada («cita») se
fija literal: si una cifra cambia, esta prueba falla y obliga a revisar la
prosa. Ademas, test_caso_<n>_se_rompe para los casos 6–12 y 24 (§10.4.1):
cada uno se rompe con la semilla 0 y en al menos 8 de 10 semillas.

Anclas por tramo (protocolo p5.2 §7.1): la rama de clase agrega solo antes
del «fin tramo rapido»; la subrama -c, solo antes del «fin tramo completo».
"""
import warnings

import numpy as np
import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c3 as c  # noqa: E402

warnings.simplefilter("ignore")


def _ml():
    return c._ml()


def _ocho_de_diez(prueba):
    """La prueba (semilla -> bool) vale con la semilla 0 y en >= 8 de 0..9."""
    resultados = [bool(prueba(s)) for s in range(10)]
    assert resultados[0], "no se rompe con la semilla 0"
    assert sum(resultados) >= 8, f"se rompe solo en {sum(resultados)}/10 semillas: {resultados}"


# --- tramo rapido ---

# ------------------------------------------------------------- página 1 · §1 ---

def test_mismo_rmse():
    m = c.cifras_c3_mismo_rmse()
    assert round(m["rmse_val_correcto"], 2) == round(m["rmse_val_curva"], 2)
    assert m["corr_e_x2_curva"] > 0.5
    assert abs(m["corr_e_x2_correcto"]) < 0.2
    assert m["cita"] == {"rmse_val": "1.34", "sigma_correcto": "1.33", "sigma_curva": "0.5"}


def test_centro_entrenamiento():
    m = c.cifras_c3_centro_entrenamiento()
    assert abs(m["e_ent"]) < 1e-10
    assert m["cita"]["e_val"] == "0.22"


# ------------------------------------------------------------- página 1 · §2 ---

def test_escala_y_caso_11():
    m = c.cifras_c3_escala_y()
    assert m["rmse_sobre_ybar"] < 0.01
    assert 0 < m["mejora"] < 0.15
    assert m["rmse_sobre_desv"] > 0.9
    assert m["L_val"] < 1.15 * m["piso"]
    assert m["le_gana"] is True  # la página dice lo que da: le gana por más de 2 EE
    assert m["cita"] == {"rmse_modelo": "1.05", "rmse_media": "1.10", "rmse_mediana": "1.09",
                         "ybar": "1000", "rmse_sobre_ybar": "0.1 %", "desv_y_ent": "1.06",
                         "rmse_sobre_desv": "0.99", "mejora": "7.7 %", "dif_pareada": "-0.093",
                         "ee_dif": "0.041", "n_val": "200"}


def test_escala_y_sale_de_diferencia_pareada():
    """Origen de la cifra (D-004): la media y el EE son los de diferencia_pareada."""
    ml = _ml()
    d = ml.caso(11)
    m = ml.ajustar(d)
    l_mod = (d.val["y"] - m.predecir(d.val)) ** 2
    l_med = (d.val["y"] - d.ent["y"].mean()) ** 2
    dif, ee = ml.diferencia_pareada(l_mod.to_numpy(), l_med.to_numpy())
    got = c.cifras_c3_escala_y()
    assert (got["dif_pareada"], got["ee_dif"]) == (float(dif), float(ee))


def test_senal_debil():
    m = c.cifras_c3_senal_debil()
    # criterio fijado en C3.T3 (DECISIÓN prog-c3-2): el modelo a < 15 % del piso
    # (el mismo que el caso 11) y la mejora < 20 %
    assert m["L_val"] < 1.15 * m["piso"]
    assert 0 < m["mejora"] < 0.20
    assert m["cita"] == {"rmse_modelo": "1.05", "rmse_media": "1.15", "raiz_piso": "1.00",
                         "mejora": "15.7 %", "dif_pareada": "-0.205", "ee_dif": "0.064",
                         "senal": "0.75x"}


def test_cv_no_es_reserva():
    m = c.cifras_c3_cv_no_es_reserva()
    for caso in m["casos"]:
        assert caso["difs"][0] == caso["difs"][1]
        assert caso["difs"] in ((1.0, 1.0), (-3.0, -3.0))
        assert caso["ee_formula"] == 0.0
    assert m["media_esperada"] == -1.0
    assert m["desv_real"] == 2.0


# ------------------------------------------------------------- página 1 · §3 ---

def test_colas():
    m = c.cifras_c3_colas()
    assert m["normal"] < 1.1
    assert m["Pareto, exponente 1.5"] > 2
    assert m["Cauchy"] > 10
    assert m["cita"] == {"normal": "1.04", "pareto": "79", "cauchy": "13 196"}


def test_cola_en_x_vive_donde_x_es_raro():
    """nb06 B3 «en x»: >= 80 % de los 10 mayores |e| en el 5 % de x más grande."""
    fr = c.cifras_c3_cola_en_x()["fracciones"]
    assert fr[0] >= 0.8
    assert sum(f >= 0.8 for f in fr) >= 8, fr


# ------------------------------------------------------------- página 1 · §4 ---

def test_omitida_caso1():
    m = c.cifras_c3_omitida_caso1()
    a = m["a"]
    assert abs(a["beta"]["x1"] - 1.8) < 3 * a["ee_x1"]
    assert abs(a["beta"]["x1"] - 1.0) > 5 * a["ee_x1"]
    assert abs(m["pendiente_f_visible"] - 1.8) < 1e-12
    assert abs(m["estructural"] - 1.0) < 1e-2
    assert abs(m["b"]["beta"]["x1"] - 1.0) < 3 * m["b"]["ee_x1"]
    assert m["c"]["L_val"] < 1.1 * 0.25
    assert abs(m["piso_visible"] - 0.86) < 0.01
    assert m["cita"] == {"beta1_a": "1.79", "beta1_b": "1.00", "beta_c_x1": "1.01",
                         "beta_c_x2x3": "1.00", "L_val_c": "0.24", "piso_visible": "0.86"}


def test_piso_combinado():
    m = c.cifras_c3_piso_combinado()
    assert abs(m["piso"] - 9.84) < 0.05
    assert abs(m["pendiente_f_visible"] - 2.4) < 0.02
    assert m["L_val"] >= m["piso"] - 2 * m["ee_L_val"]
    assert abs(m["piso"] - m["formula_sin_omitidas"]) > 5  # piso no devuelve 0.84


def test_endogena_caso_8():
    m = c.cifras_c3_endogena()
    assert abs(m["media_beta1"] - m["cuenta"]) < 3 * m["ee_media"]
    assert abs(m["corr_e_x1"]) < 1e-10
    assert abs(m["piso"] - 0.75) < 0.01
    assert abs(m["L_val"] - m["piso"]) < 0.05 * m["piso"]
    assert m["L_val"] >= m["piso"] - 2 * m["ee_L_val"]
    assert m["cita"] == {"media_beta1": "2.50", "cuenta": "2.5", "L_val": "0.78", "piso": "0.75"}


def test_diana():
    m = c.cifras_c3_diana()
    desv1 = {k: v["desv"][0] for k, v in m.items() if k != "cita"}
    assert max(desv1, key=desv1.get) == "colineal"
    for corrido in ("omitida correlacionada", "endógena"):
        mu, sd = m[corrido]["media"][0], m[corrido]["desv"][0]
        assert abs(mu - 1) > 10 * sd / np.sqrt(c.REPETICIONES)
    mu, sd = m["correcto"]["media"][0], m["correcto"]["desv"][0]
    assert abs(mu - 1) < 3 * sd / np.sqrt(c.REPETICIONES)
    assert m["cita"] == {"omitida": "1.59", "endogena": "1.50"}


def test_abanico_los_dos_abren_igual():
    m = c.cifras_c3_abanico()
    assert m["A"] > 2 and m["B"] > 2
    assert abs(m["A"] / m["B"] - 1) < 0.2


# ------------------------------------------------------------- página 1 · §5 ---

def test_colineal_caso_9():
    m = c.cifras_c3_colineal()
    assert m["razon_beta1"] >= 5
    assert m["razon_dentro"] < 1.5
    assert m["razon_fuera"] >= 5
    assert m["cita"] == {"desv_beta1_0": "0.10", "desv_beta1_99": "0.75",
                         "desv_y_dentro_99": "0.13", "desv_y_fuera_99": "1.50"}


# ------------------------------------------------------------- página 2 · §1–§2 ---

def test_regiones():
    m = c.cifras_c3_regiones()
    assert m["l1"]["beta"][0] == 0.0
    assert m["l2"]["beta"][0] != 0 and m["l2"]["beta"][1] != 0
    assert m["elastica"]["beta"][0] != 0
    # nb07 B1 por omisión (d a la mitad): lasso anula β̂1 y ridge no
    assert m["l1"]["mitad"]["beta"][0] == 0.0 and m["l2"]["mitad"]["beta"][0] != 0
    assert m["cita"] == {"l2": {"mu": "0.60", "beta1": "0.29", "beta2": "0.96"},
                         "l1": {"mu": "1.36", "beta1": "0.00", "beta2": "1.00"},
                         "elastica": {"mu": "0.92", "beta1": "0.17", "beta2": "0.93"}}


def test_regiones_mu_reproduce_el_restringido():
    ml = _ml()
    d, phi = c.datos_regiones(), c.phi_regiones()
    for pen in c.PENALIZACIONES:
        beta, mu = ml.optimo_restringido(d, phi, pen, c.D_REGIONES)
        m = ml.ajustar(d, phi=phi, mu=mu, penalizacion=pen)
        assert np.allclose(m.beta_gorro[["x1", "x2"]], beta[["x1", "x2"]], atol=1e-4)


def test_recta_apoyo():
    m = c.cifras_c3_recta_apoyo()
    assert m["d"] > 0 and min(m["ds"]) > 0
    assert m["pendiente"] == -m["mu"]
    assert abs(m["derivada"] - m["pendiente"]) < 1e-4
    assert m["apoyo_min"] >= -1e-6           # la recta deja la curva por encima
    v = np.array(m["v"])
    assert np.all(np.diff(v) <= 1e-8)        # no creciente
    assert np.all(np.diff(v, 2) >= -1e-6)    # convexa en la rejilla
    assert m["cita"] == {"d": "1", "mu": "1.36"}


def test_sin_holgura_no_hay_mu():
    """L = (β − 1)², Ω = β² + 1, d = 1: el único factible es β = 0, y la forma
    penalizada da 1/(1 + μ) ≠ 0 para toda μ de la rejilla hasta 10⁶."""
    for mu in np.logspace(-6, 6, 400):
        beta = 1 / (1 + mu)              # argmin (β − 1)² + μ(β² + 1)
        malla = np.linspace(-0.5, 1.5, 20001)
        num = malla[np.argmin((malla - 1) ** 2 + mu * (malla ** 2 + 1))]
        assert abs(num - beta) < 2e-4
        assert beta > 0


# ------------------------------------------------------------- página 2 · §4 ---

def test_grado12():
    m = c.cifras_c3_grado12()
    p = m["paneles"]
    assert p["medio"]["R"] < p["grande"]["R"] and p["medio"]["R"] < p["chico"]["R"]
    assert p["medio"]["R"] < m["R_sin_penalizar"]
    u = m["u"]
    mus = sorted(u["cv"])
    assert u["mu_min"] not in (mus[0], mus[-1])
    for ext in (mus[0], mus[-1]):
        assert u["cv"][u["mu_min"]] < u["cv"][ext]
        assert u["R"][u["mu_min"]] < u["R"][ext]
    lent = [u["L_ent"][x] for x in mus]
    assert all(b >= a - 1e-9 for a, b in zip(lent, lent[1:]))
    assert u["mu_un_ee"] >= u["mu_min"]
    assert m["n_ent"] == 36
    assert m["cita"] == {"mu_grande": "100", "mu_medio": "0.0032", "mu_medio_log": "-2.5",
                         "mu_chico": "10⁻⁶",
                         "R": {"grande": "48.3", "medio": "29.3", "chico": "203.1"},
                         "L_val": {"grande": "56.4", "medio": "13.8", "chico": "7.6"},
                         "R_sin_penalizar": "1971"}


def test_grado12_vistas():
    m = c.cifras_c3_grado12_vistas()
    for k in ("grande", "medio", "chico"):
        assert abs(m[k]["centro"]) < 0.5 * m[k]["ancho"]
    assert m["medio"]["ancho"] == min(m[k]["ancho"] for k in ("grande", "medio", "chico"))
    assert m["cita"] == {"grande": {"centro": "0.8", "ancho": "6.9"},
                         "medio": {"centro": "0.7", "ancho": "5.4"},
                         "chico": {"centro": "2.5", "ancho": "14.0"}}


def test_trayectorias():
    m = c.cifras_c3_trayectorias()
    assert m["ceros_ridge"] == 0             # en estos datos (no se cita como ley)
    assert all(v is not None for v in m["apagado"].values())
    assert m["cita"] == {"primera_util": "1.1", "ultima_util": "6.3"}
    assert m["espurias_vivas"] == 0


def test_ridge_cruza_cero():
    r = c.cifras_c3_ridge_cruza_cero()["ridge"]
    assert abs(r[0]) < 1e-12 and abs(r[1] + 1) < 1e-12


def test_pareja():
    m = c.cifras_c3_pareja()
    assert min(m["l1"]["x1"], m["l1"]["x6"]) < 0.8
    assert m["elastica"]["x1"] > 0.8 and m["elastica"]["x6"] > 0.8
    assert m["cita"]["l1"] == {"x1": "100", "x6": "42", "ambas": "42"}


def test_ridge_colineal():
    m = c.cifras_c3_ridge_colineal()
    assert m["ridge"]["desv"] < m["sin"]["desv"] / 3
    assert abs(m["ridge"]["media"] - 1) > abs(m["sin"]["media"] - 1) - 0.05
    assert m["cita"] == {"sin": {"media": "0.96", "desv": "0.75"},
                         "ridge": {"media": "0.94", "desv": "0.09"}}


# ------------------------------------------------------------- página 2 · §5 ---

def test_estandarizar_caso_10():
    m = c.cifras_c3_estandarizar()
    assert m["sin"]["a_mu_2"]["x1"] == 0 and m["sin"]["a_mu_2"]["x2"] != 0
    assert m["con"]["a_mu_2"]["x1"] != 0 and m["con"]["a_mu_2"]["x2"] != 0
    assert m["sin"]["x2"] > 1000 * m["sin"]["x1"]
    assert m["cita"] == {"sin_x1": "1.1", "sin_x2": "2.8 × 10^6", "con_x1": "2.5", "con_x2": "2.9"}


def test_escala_objetivo_caso_24():
    m = c.cifras_c3_escala_objetivo()
    assert m["no_ceros_1000y"] > m["no_ceros_y"]
    assert m["no_ceros_1000y_1000mu"] == m["no_ceros_y"]
    assert m["dif_lasso"] < 1e-6 and m["dif_ridge"] < 1e-6
    assert m["cita"] == {"no_ceros_y": "5", "no_ceros_1000y": "10"}


# ------------------------------------------------------------- página 2 · §6 ---

def test_mu_cv():
    m = c.cifras_c3_mu_cv()
    mus = sorted(c.MUS_CV)
    assert m["mu_ent"] == mus[0]                      # L_ent elige la más chica
    assert m["mu_un_ee"] >= m["mu_min"]
    # la de un EE: la primera, de grande a chica, cuya MEDIA de CV5 no pasa del umbral
    tabla = c.selecciones_mu_cv()["minimo"].tabla.set_index("candidato")
    primera = next(x for x in sorted(mus, reverse=True) if tabla.loc[x, "valor"] <= m["umbral"])
    assert m["mu_un_ee"] == primera
    lent = [m["L_ent"][x] for x in mus]
    assert all(b >= a - 1e-9 for a, b in zip(lent, lent[1:]))
    s = c.selecciones_mu_cv()["un_ee"]
    assert s.modelo_final is s.modelo
    assert m["prueba"]["le_gana"] is True
    assert m["cita"] == {"mu_ent": "10⁻⁴", "mu_min": "0.14", "mu_un_ee": "0.24",
                         "cv_min": "1.05", "ee_min": "0.16", "cv_un_ee": "1.08",
                         "ee_un_ee": "0.16", "no_ceros_min": "15", "no_ceros_un_ee": "8",
                         "R_min": "1.07", "R_un_ee": "1.12", "L_prueba": "0.95",
                         "dos_ee_prueba": "0.32", "dif_prueba": "-18.4", "ee_dif_prueba": "3.1"}


def test_mu_cv_mutacion_del_orden():
    """Con la rejilla ascendente y sin orden_complejidad, la regla de un EE da
    una μ <= la del mínimo; con el orden explícito, una >=."""
    m = c.cifras_c3_mu_cv()
    assert m["mutacion_un_ee"] <= m["mu_min"] <= m["mu_un_ee"]


# ------------------------------------------------------------- ejercicios ---

def test_cuentas_de_los_ejercicios():
    e = c.cifras_c3_ejercicios()
    assert e["cancelan"] == {"centro": 0.0, "L": 2.8, "es_x2_menos_2": True}
    assert e["constante"] == {"mse_media": 16.0, "mse_mediana": 20.0,
                              "mae_media": 3.2, "mae_mediana": 2.0}
    assert round(e["cola"]["mse"], 2) == 25.99 and round(100 * e["cola"]["frac_mse"]) == 96
    assert round(e["cola"]["mae"], 2) == 1.49 and round(100 * e["cola"]["frac_mae"]) == 34
    assert e["pendiente"] == 3.5
    assert round(e["colineal"]["desv_0"], 3) == 0.1
    assert round(e["colineal"]["desv_09"], 3) == 0.229
    assert round(e["colineal"]["razon"], 1) == 2.3
    assert round(e["factor_099"]) == 50
    assert e["esquina"]["lasso"] == (0.0, 1.0) and round(e["esquina"]["mu_lasso"], 3) == 2.0
    assert tuple(round(v, 3) for v in e["esquina"]["ridge"]) == (0.148, 0.989)
    assert round(e["esquina"]["mu_ridge"], 3) == 1.022
    z = {k: tuple(round(v, 3) for v in t) for k, t in e["cero_a_mano"].items()}
    assert z == {"l2": (1.5, 0.2), "l1": (2.5, 0.0), "elastica": (1.833, 0.1)}


# ------------------------------------------------------- casos que se rompen ---

def test_caso_6_se_rompe():
    """máx/mín del MSE val en 10 semillas: > 10 con Cauchy, > 3 con Pareto, < 2 normal."""
    ml = _ml()

    def razon(**cambios):
        v = []
        for s in range(10):
            d = ml.caso(6, semilla=s, **cambios)
            v.append(float(ml.L(ml.ajustar(d), d.val)))
        return max(v) / min(v)

    assert razon() > 3
    assert razon(ruido=ml.cauchy()) > 10
    assert razon(ruido=ml.normal()) < 2


def test_caso_7_se_rompe():
    ml = _ml()

    def rompe(s):
        d = ml.caso(7, semilla=s)
        p = ml.piso(d)
        sin = ml.L(ml.ajustar(d), d.val)
        con = ml.L(ml.ajustar(d, phi=ml.combinar(ml.columnas("x1", "x2"),
                                                  ml.interacciones(("x1", "x2")))), d.val)
        return sin > 3 * p and con < 1.15 * p

    _ocho_de_diez(rompe)


def test_caso_8_se_rompe():
    ml = _ml()
    m = c.cifras_c3_endogena()
    assert abs(m["media_beta1"] - 2) > 10 * m["ee_media"]

    def rompe(s):
        d = ml.caso(8, semilla=s, n=2000)
        mod = ml.ajustar(d)
        ee = c._ee_pendientes(mod, d.ent)["x1"]
        e = d.ent["y"].to_numpy() - mod.predecir(d.ent)
        return (abs(mod.beta_gorro["x1"] - 2) > 10 * ee
                and abs(np.corrcoef(e, d.ent["x1"])[0, 1]) < 1e-10
                and abs(ml.piso(d) - 0.75) < 0.01)

    _ocho_de_diez(rompe)


def test_caso_9_se_rompe():
    ml = _ml()
    m = c.cifras_c3_colineal()
    assert m["razon_beta1"] >= 5 and m["razon_dentro"] < 1.5 and m["razon_fuera"] >= 5

    def rompe(s):
        base = 1000 * (s + 1)
        t9 = ml.beta_repetido(lambda q: ml.caso(9, semilla=q, con_realidad=False), None, 50,
                              semilla=base)
        t0 = ml.beta_repetido(lambda q: ml.caso(9, semilla=q, correlacion={("x1", "x2"): 0.0},
                                                con_realidad=False), None, 50, semilla=base)
        sd = lambda t, p: c.prediccion_repetida(t, p).std(ddof=1)
        return (t9["x1"].std() >= 5 * t0["x1"].std()
                and sd(t9, c.DENTRO) < 1.5 * sd(t0, c.DENTRO)
                and sd(t9, c.FUERA) >= 5 * sd(t0, c.FUERA))

    _ocho_de_diez(rompe)


def test_caso_10_se_rompe():
    ml = _ml()

    def rompe(s):
        d = ml.caso(10, semilla=s)
        sin = ml.ajustar(d, phi=ml.columnas("x1", "x2"), mu=2.0, penalizacion="l1").beta_gorro
        con = ml.ajustar(d, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=2.0,
                         penalizacion="l1").beta_gorro
        return sin["x1"] == 0 and sin["x2"] != 0 and con["x1"] != 0 and con["x2"] != 0

    _ocho_de_diez(rompe)


def test_caso_11_se_rompe():
    ml = _ml()

    def rompe(s):
        d = ml.caso(11, semilla=s)
        r = c._comparar_con_la_media(d)
        return (r["rmse_modelo"] / r["ybar"] < 0.01 and 0 < r["mejora"] < 0.15
                and r["rmse_modelo"] / r["desv_y_ent"] > 0.9 and r["L_val"] < 1.15 * r["piso"])

    _ocho_de_diez(rompe)


def test_caso_12_se_rompe():
    ml = _ml()
    t = ml.beta_repetido(lambda q: ml.caso(12, semilla=q, con_realidad=False), None,
                         c.REPETICIONES)
    assert abs(t["x"].mean() - 2) < 3 * t["x"].std(ddof=1) / np.sqrt(c.REPETICIONES)

    def rompe(s):
        d = ml.caso(12, semilla=s)
        m = ml.ajustar(d)
        df = c.pd_concat_dev(d)
        e = df["y"].to_numpy() - m.predecir(df)
        x = df["x"].to_numpy()
        lo, hi = np.quantile(x, [0.2, 0.8])
        ee = c._ee_pendientes(m, d.ent)["x"]
        return np.std(e[x >= hi]) >= 3 * np.std(e[x <= lo]) and abs(m.beta_gorro["x"] - 2) < 3 * ee

    _ocho_de_diez(rompe)


def test_caso_24_se_rompe():
    ml = _ml()
    phi = c.phi_muchas(10)

    def rompe(s):
        d1 = ml.muchas_variables(n=300, J=10, utiles=3, semilla=s)
        d2 = ml.caso(24, semilla=s)
        nz = lambda m: int((m.beta_gorro.drop("1") != 0).sum())
        a = ml.ajustar(d1, phi=phi, mu=0.3, penalizacion="l1")
        b = ml.ajustar(d2, phi=phi, mu=0.3, penalizacion="l1")
        cc = ml.ajustar(d2, phi=phi, mu=300.0, penalizacion="l1")
        ra = ml.ajustar(d1, phi=phi, mu=0.3, penalizacion="l2")
        rb = ml.ajustar(d2, phi=phi, mu=0.3, penalizacion="l2")
        return (nz(b) > nz(a)
                and float((cc.beta_gorro / 1000 - a.beta_gorro).drop("1").abs().max()) < 1e-6
                and float((rb.beta_gorro / 1000 - ra.beta_gorro).drop("1").abs().max()) < 1e-6)

    _ocho_de_diez(rompe)



def test_interaccion_caso_7():
    m = c.cifras_c3_interaccion()
    assert m["L_val_sin"] > 10 * m["L_val_con"]
    assert m["cita"] == {"L_val_sin": "5.59", "L_val_con": "0.24"}

# --- fin tramo rapido ---


# --- tramo completo ---
# --- fin tramo completo ---
