"""Fija en la fuente las cifras de la clase 5 (tools/ml_cifras_c5.py).

Sin prosa (D-003): estas pruebas no leen ninguna pagina. Que la pagina cite la
misma cifra lo comprueba tools/test_ml_prosa_c5.py. Cada criterio es el de
clase_5.md §10.7 (tabla de ml_cifras_c5), §10.4 (casos borde) y §10.6 (la
promesa de cada tarea), con los ajustes que registra la bitacora de prog-c5
(DECISION prog-c5-2 a prog-c5-7). Cada forma citada («cita») se fija literal en
citas_c5.json: si una cifra cambia, esta prueba falla y obliga a revisar la
prosa y los briefs. Las cifras se calcularon con sklearn 1.6.1 (venv 3.12).
"""
import json
import math
import re
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")
pytest.importorskip("scipy")

import ml_cifras_c5 as c  # noqa: E402

TOOLS = Path(__file__).resolve().parent
CITAS = json.loads((TOOLS / "datos" / "citas_c5.json").read_text(encoding="utf-8"))
FUNCIONES = sorted(CITAS)


def _norm(v):
    return json.loads(json.dumps(v, ensure_ascii=False, sort_keys=True, default=str))


@pytest.mark.parametrize("nombre", FUNCIONES)
def test_cada_cita_es_la_de_la_fuente(nombre):
    assert _norm(getattr(c, nombre)()["cita"]) == CITAS[nombre], (
        f"{nombre} cambió: revisa la prosa y los briefs, y luego citas_c5.json")


def test_toda_funcion_cifras_tiene_su_cita_fijada():
    fuente = (TOOLS / "ml_cifras_c5.py").read_text(encoding="utf-8")
    nombres = set(re.findall(r"^def (cifras_c5_[a-z0-9_]+)\(", fuente, re.M))
    assert nombres == set(CITAS)


def test_requiere_la_version_de_la_clase_5():
    assert c.REQUIERE == "1.6"
    ml = c._ml()
    ml.requiere(c.REQUIERE)


# ----------------------------------------------------------- P1 §3 ---

def test_ks_a_mano_es_un_tercio_exacto():
    r = c.cifras_c5_ks_a_mano()
    assert r["ks"] == Fraction(1, 3)
    assert r["Fa"] == [Fraction(1, 3), Fraction(2, 3), 1, 1]
    assert r["Fb"] == [0, Fraction(1, 3), Fraction(2, 3), 1]
    assert abs(r["ks_lab"] - 1 / 3) < 1e-12


def test_ks_falsas_alarmas_mediana_entre_0_y_2():
    r = c.cifras_c5_ks()
    assert 0 <= r["mediana"] <= 2
    assert r["ks_deriva"] > r["ks_nada"]


def test_autocorrelacion_alterna_es_menos_cinco_sextos_y_no_pearson():
    r = c.cifras_c5_autocorrelacion()
    assert abs(r["alterna"] + 5 / 6) < 1e-12
    assert abs(r["pearson"] + 1) < 1e-12
    assert r["rezago1_con"] > 0.5 > abs(r["rezago1_sin"])
    assert 0 <= r["mediana_fuera"] <= 2


def test_el_docstring_de_autocorrelacion_dice_denominador_comun():
    doc = c._ml().autocorrelacion.__doc__
    assert "denominador común" in doc


def test_adversarial_nada_y_concepto_en_su_benchmark_sin_senal():
    r = c.cifras_c5_adversarial()
    for k in ("nada_bosque", "concepto_bosque"):
        v = r[k]
        assert abs(v["log_loss"] - v["benchmark"]) < 0.02
        assert v["senal"] == "sin señal"
        assert abs(v["reserva"]) < 2 * v["reserva_ee"]
    assert abs(r["nada_bosque"]["benchmark"] - r["benchmark_formula"]) < 1e-3


def test_adversarial_deriva_con_senal_y_confirmada_en_la_reserva():
    v = c.cifras_c5_adversarial()["deriva_bosque"]
    assert v["senal"] == "señal"
    assert v["dif_media"] < 0 and abs(v["dif_media"]) > v["dif_desv"]
    assert v["reserva"] + 2 * v["reserva_ee"] < 0
    assert v["benchmark"] - v["log_loss"] > 0.05


def test_mismas_marginales_bosque_lejos_logistica_cerca():
    r = c.cifras_c5_adversarial()
    assert r["marginales_bosque"]["senal"] == "señal"
    assert r["marginales_logistica"]["senal"] == "sin señal"
    assert abs(r["marginales_logistica"]["log_loss"]
               - r["marginales_logistica"]["benchmark"]) < 0.01


def test_control_obar_ve_lo_que_el_corte_en_medio_no():
    """DECISION prog-c5-3: el control es el de mismas marginales (diferencia moderada):
    cortar en o barra da MCC > 0.15; cortar en 0.5 se queda en 0. Mutacion: con la
    deriva fuerte el corte en 0.5 tambien ve (por eso no es el control)."""
    r = c.cifras_c5_adversarial()
    v = r["marginales_bosque"]
    assert abs(v["o_bar"] - 0.2) < 1e-9
    assert v["mcc"] > 0.15 and v["mcc"] > v["mcc_05"]
    assert v["mcc_05"] == 0
    assert r["deriva_bosque"]["mcc_05"] > 0


def test_adversarial_por_grupos_no_detecta_clientes():
    v = c.cifras_c5_adversarial()["clientes"]
    assert v["ll_azar"] < v["benchmark"] - 0.02
    assert v["ll_grupos"] > v["benchmark"]


# ----------------------------------------------------------- P1 §4 ---

def test_cv_miente_con_el_modelo_de_la_clase_2_y_no_con_el_lineal():
    r = c.cifras_c5_cv_miente()["res"]
    for caso in (13, 14):
        cl, li = r[(caso, "clase2")], r[(caso, "lineal")]
        assert cl["azar"][0] < 0.7 * cl["R"][0]
        assert abs(np.median(li["razones"]) - 1) < 0.10
        assert abs(cl["estructurada"][0] / cl["R"][0] - 1) < 0.25


# ----------------------------------------------------------- P1 §5–§6 ---

def test_fugas_calificacion_y_elegir_variables_inflan_mas_de_0_3():
    r = c.cifras_c5_fugas()
    assert r["posterior"]["cv"][0] >= 0.9
    assert r["posterior"]["uso"][0] <= r["ninguna"]["uso"][0]
    assert r["posterior"]["inflado"][0] > 0.3
    assert r["seleccion_previa"]["inflado"][0] > 0.3
    assert abs(r["seleccion_previa"]["uso"][0]) < 0.1


def test_caso_variable_posterior_se_rompe_a_la_vista():
    r = c.cifras_c5_fugas()
    assert r["posterior"]["cv"][0] >= 0.9


def test_caso_preprocesar_antes_casi_no_cambia_la_cv():
    """DECISION prog-c5-7: con la tuberia de vecinos (que reescala dentro del pliegue)
    la fuga de escalar e imputar antes casi no mueve la CV: la pagina dice «casi no
    cambia» con la cifra; nunca se cambia el proceso para exagerar."""
    c20 = c.cifras_c5_fugas()["caso20"]
    assert abs(c20["mediana_dif"]) < 0.02
    assert c20["optimistas"] <= c20["n"] // 2


def test_caso_duplicados_se_rompe_a_la_vista():
    r = c.cifras_c5_fugas()
    assert r["duplicados"]["inflado"][0] >= 0.1


def test_caso_seleccion_previa_se_rompe_a_la_vista_y_la_limpia_recupera():
    r = c.cifras_c5_fugas()
    assert r["seleccion_previa"]["cv"][0] > 0.3
    assert abs(r["seleccion_limpia"]["cv"][0]) < 0.1
    assert abs(r["seleccion_limpia"]["uso"][0]) < 0.1


def test_caso_seleccion_previa_mutacion_desde_columnas_x_no_recupera():
    ml = c._ml()
    d = ml.caso(26, semilla=0, n_realidad=1000)
    mala = ml.tuberia(ml.seleccionar(k=10, columnas=list(d.columnas_x)),
                      modelo={"familia": "logistica"})
    with c._silencio():
        cv = ml.validacion_cruzada(d, mala, criterio="mcc").media
    assert cv > 0.3


def test_caso_categoria_nueva_se_rompe_a_la_vista():
    ml = c._ml()
    d = ml.caso(27)
    assert "sur" not in set(d.ent["zona"]) and "sur" in set(d.prueba["zona"])
    base = ml.ajustar(d.ent, phi=ml.combinar(ml.columnas("distancia"), ml.dummies("zona")))
    with pytest.raises(ValueError, match="sur"):
        base.predecir(d.prueba)
    with c._silencio():
        ef = ml.ajustar(d.ent, phi=ml.combinar(ml.columnas("distancia"),
                                              ml.dummies("zona", codificacion="efectos")))
        pred = ef.predecir(d.prueba)
    e = (d.prueba["y"].to_numpy(float) - np.asarray(pred, float)) ** 2
    sur = (d.prueba["zona"] == "sur").to_numpy()
    assert e[sur].mean() > 3 * e[~sur].mean()


def test_caso_cambio_de_concepto_se_rompe_a_la_vista():
    r = c.cifras_c5_adversarial()["concepto_bosque"]
    assert abs(r["log_loss"] - r["benchmark"]) < 0.02
    ml = c._ml()
    d = ml.caso(28)
    m = ml.ajustar(d.ent)
    assert ml.riesgo(m, d) > 3 * ml.L(m, d.prueba)


def test_tuberia_recupera_dentro_de_dos_ee():
    r = c.cifras_c5_tuberia()
    for ruta in ("preprocesar", "seleccion"):
        v = r[ruta]
        assert abs(v["dif_con"]) < max(2 * v["ee_entre_semillas"], 0.1)
    assert r["seleccion"]["sin"] - r["seleccion"]["con"] > 0.3


def test_imputacion_con_indicadora_mejor_y_centinela_tuerce():
    r = c.cifras_c5_imputacion()
    assert r["L_con"] < r["L_sin"]
    assert abs(r["pico"] - 0.3) < 0.08
    assert abs(r["pendiente_centinela"] - r["pendiente_completos"]) > 2 * abs(
        r["pendiente_mediana"] - r["pendiente_completos"])


def test_escalar_mco_rango_completo_no_cambia_y_el_contraejemplo_si():
    r = c.cifras_c5_escalar_mco()
    assert r["mco"] < 1e-9
    assert r["imputacion"] < 1e-9
    assert r["ridge"] > 1e-9
    assert abs(r["contra_1"] - 0.5) < 1e-12
    assert abs(r["contra_2"] - 0.2) < 1e-12


# ----------------------------------------------------------- P2 ---

def test_dummy_rango_y_dos_betas_mismas_predicciones():
    r = c.cifras_c5_dummy()
    assert r["rango"] == 4
    assert r["max_dif_pred"] < 1e-10
    assert np.max(np.abs(r["b1"] - r["b2"])) > 1
    Phi, y = r["Phi"], r["y"]
    P = np.eye(5)
    P[0, 0] = 0
    otra = np.linalg.solve(Phi.T @ Phi / 6 + c.MU_DUMMY * P, Phi.T @ y / 6)
    assert np.allclose(otra, r["ridge"])


def test_diagnostico_brecha_por_grupos_y_dos_procesos():
    r = c.cifras_c5_diagnostico()
    assert r["brecha_grupos"] > 2 * r["brecha_azar"]
    assert r["rel"]["sesgo"] > 0.2
    assert abs(r["rel"]["piso"]) < 0.05


def test_depurar_exacto_y_mutacion_con_mu():
    r = c.cifras_c5_depurar()
    assert r["mse_recta"] == Fraction(264, 5)
    assert r["mse_cuadratica"] < 1e-12
    assert c.cifras_c5_depurar.__wrapped__(mu=1.0)["mse_cuadratica"] > 1e-3


def test_arbol_mcc_creciente_con_la_profundidad():
    m = c.cifras_c5_arbol()["mcc"]
    assert m[1] < m[3] < m[6]


def test_familias_el_bosque_se_estabiliza():
    r = c.cifras_c5_familias()
    assert r["rango"][200] < r["rango"][10]
    assert 1 < r["profundidad"] < max(c.PROF_CURVA)
    assert min(c.ETAPAS_CURVA) < r["etapas"] < max(c.ETAPAS_CURVA)


def test_bagging_simulada_dentro_de_5_por_ciento():
    r = c.cifras_c5_bagging()
    assert abs(r["simulada"] / r["formula"] - 1) < 0.05


def test_cybenko_decrece_y_la_aprendida_pide_mas_datos():
    r = c.cifras_c5_cybenko()
    e = r["errores"]
    assert e[1] > e[3] > e[10]
    assert r["llega"]["polar"] is not None and r["llega"]["aprendida"] is not None
    assert r["llega"]["aprendida"] > r["llega"]["polar"]


def test_final_metodologia_el_bosque_por_grupos_ya_no_gana():
    """DECISION prog-c5-5: el criterio del plan («a < 10 % del benchmark») no se cumple
    con una distancia que si informa; lo que la tabla sostiene es que, por grupos, el
    bosque deja de ganarle al lineal y su ventaja al azar era el cliente memorizado."""
    r = c.cifras_c5_final_metodologia()
    t = r["tabla"]
    assert t[("bosque", "azar")] < t[("bosque", "grupo")]
    assert t[("bosque", "grupo")] >= t[("lineal", "grupo")] - 0.2
    assert r["L_ent"] < 0.5 * t[("bosque", "azar")]
    assert r["benchmark"] > t[("bosque", "grupo")]


def test_escenarios_declarados():
    e = c.ESCENARIOS
    assert e["p1_final"]["semanas"] == 8 and e["p1_final"]["semana_uso"] == 9
    assert e["p2_final"] == {"pedidos": 2000, "clientes": 300}
    d = c.datos_final_p2()
    assert len(d.ent) == 2000
    assert d.ent["grupo"].nunique() <= 300


def test_referencia_a_diez_por_ciento_del_piso():
    assert c.cifras_c5_referencia()["razon"] < 1.10


# --- Promesa de las tareas (C5.T7) ---
# Lee la especificación privada de cada tarea ejecutando sus celdas de código del
# .py (sin el guion) con ml_lab de tools/, como lo correría Colab. Nada se duplica
# fuera del .py de la tarea (§10.12).

def _correr(stem, hasta, cambios=None):
    import gen_cuadernos_ml as gcn
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    celdas = gcn.leer_celdas((TOOLS / "cuadernos_ml" / f"{stem}.py").read_text(
        encoding="utf-8"))
    ns = {"ml": c._ml()}
    mostrar, plt.show = plt.show, (lambda *a, **k: None)
    try:
        for tipo, clave, cuerpo in celdas:
            if tipo == "texto":
                continue
            for viejo, nuevo in (cambios or {}).items():
                cuerpo = cuerpo.replace(viejo, nuevo)
            with c._silencio():
                exec(cuerpo, ns)
            plt.close("all")
            if clave == hasta:
                break
    finally:
        plt.show = mostrar
    return ns


@pytest.fixture(scope="module")
def tarea_5a():
    return _correr("tarea_5a_series_de_tiempo", "bloque-3-juega")


def test_promesa_5a_vecinos_miente_y_el_lineal_no(tarea_5a):
    """D-009.6, sin deriva: la CV al azar de vecinos promete a lo más la mitad del error
    de la temporal; la del lineal queda a menos de 10 %."""
    t = tarea_5a["TABLA"]
    assert t.loc["vecinos en (x, t)", "azar"] * 2 <= t.loc["vecinos en (x, t)", "temporal"]
    assert abs(t.loc["lineal en x", "azar"] / t.loc["lineal en x", "temporal"] - 1) < 0.10


def test_promesa_5a_la_serie_es_una_sola_y_el_futuro_la_continua(tarea_5a):
    h, f = tarea_5a["historia"], tarea_5a["futuro"]
    assert len(h) == 600 and len(f) == 120
    assert h["t"].max() < f["t"].min()
    assert f["ayer"].iloc[0] == h["y"].iloc[-1]


@pytest.fixture(scope="module")
def tarea_5b():
    return _correr("tarea_5b_fugas", "bloque-1-prueba")


def test_promesa_5b_el_companero_infla_mas_de_0_3(tarea_5b):
    ns = tarea_5b
    ml = c._ml()
    prueba = ns["prueba_sellada"]._Sellada__df.copy()     # la prueba no se abre: se mira
    prueba = ns["imp_ent"].transformar(prueba.assign(costo_del_reingreso=0.0))
    prueba.attrs = {"ml": ns["META"]}
    en_prueba = ml.evaluar(ns["modelo_compa"], prueba, "mcc")
    assert ns["MCC_COMPA"] - en_prueba > 0.3
    assert ns["prueba_sellada"].aperturas == 0


def test_promesa_5b_la_prueba_sellada_no_comparte_pacientes(tarea_5b):
    ns = tarea_5b
    sellada = ns["prueba_sellada"]._Sellada__df
    assert not set(sellada["paciente"]) & set(ns["desarrollo"]["paciente"])
    assert 150 <= sellada["paciente"].nunique() <= 200
    assert 0.10 <= ns["desarrollo"]["y"].mean() <= 0.20


def test_promesa_5b_el_desplazamiento_de_los_pesos_es_ln_w1_w0(tarea_5b):
    ml = c._ml()
    y = tarea_5b["desarrollo"]["y"].to_numpy()
    w = ml.pesos_de_clase(y, como="balanceado")
    n1, n0 = (y == 1).sum(), (y == 0).sum()
    assert abs(math.log(w[1] / w[0]) - math.log(n0 / n1)) < 0.01


def test_promesa_5b_b5_no_reporta_perdida_logaritmica():
    import gen_cuadernos_ml as gcn
    celdas = gcn.leer_celdas((TOOLS / "cuadernos_ml" / "tarea_5b_fugas.py").read_text(
        encoding="utf-8"))
    for tipo, clave, cuerpo in celdas:
        if clave.startswith("bloque-5"):
            assert "log_loss" not in cuerpo and "logaritmica" not in cuerpo
