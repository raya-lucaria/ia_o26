"""Fija en la fuente las cifras de la clase 2 (tools/ml_cifras_c2.py).

Sin prosa (D-003): estas pruebas no leen ninguna pagina. Que la pagina cite
la misma cifra lo comprueba tools/test_ml_prosa_c2.py. Cada valor fijado aqui
es el que la pagina escribe (redondeado como lo escribe la pagina); si una
cifra cambia, esta prueba falla y obliga a revisar la prosa. Ademas de cada
valor, la propiedad que clase_2.md §10.7 exige a su funcion.

Anclas por tramo (protocolo p5.2 §7.1): cada rama agrega sus pruebas solo
dentro del ancla de su tramo.
"""
import inspect
import math
from fractions import Fraction

import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c2 as c  # noqa: E402


def _r(v, d):
    return round(float(v), d)


def test_las_cifras_importan_ml_lab_de_tools_y_no_de_assets():
    fuente = inspect.getsource(c)
    assert 'import_module("aprendizaje_maquina")' in fuente
    assert "_assets" not in fuente.split('"""', 2)[2].replace("_assets/", "")


# --- tramo rapido ---

# ------------------------------------------- cifras_c2_entrenamiento_elige ---

def test_entrenamiento_elige_el_grado_maximo():
    e = c.cifras_c2_entrenamiento_elige()
    assert e["elegido"] == 12
    assert (_r(e["L_ent_0"], 1), _r(e["L_ent_3"], 1), _r(e["L_ent_12"], 1)) == (51.2, 7.7, 4.5)


def test_entrenamiento_l_ent_no_crece_con_el_grado():
    L = c.cifras_c2_entrenamiento_elige()["L_ent"]
    assert all(L[N + 1] <= L[N] + 1e-9 for N in range(12))


# --------------------------------------------- cifras_c2_ajustes_con_prueba ---

def test_ajustes_con_prueba_las_cifras_de_la_pagina():
    a = c.cifras_c2_ajustes_con_prueba()
    assert {N: (_r(a[N]["L_ent"], 1), _r(a[N]["L_prueba"], 1)) for N in (1, 4)} == {
        1: (18.5, 15.3), 4: (7.1, 13.3)}
    assert (_r(a[1]["R"], 1), _r(a[4]["R"], 1)) == (14.8, 11.8)
    assert _r(a[12]["L_ent"], 1) == 4.5
    assert a[12]["L_prueba"] > 1000 and a[12]["R"] > 1000


def test_ajustes_con_prueba_el_grado_12_pierde_en_prueba():
    a = c.cifras_c2_ajustes_con_prueba()
    assert a[12]["L_prueba"] > a[4]["L_prueba"]


# ------------------------------------------------ cifras_c2_prueba_ruidosa ---

def test_prueba_ruidosa_las_cifras_de_la_pagina():
    p = c.cifras_c2_prueba_ruidosa()
    assert _r(p["R"], 1) == 11.8
    assert (_r(p["desv_20"], 1), _r(p["desv_200"], 1)) == (3.8, 1.1)
    assert (round(100 * p["cobertura_20"]), round(100 * p["cobertura_200"])) == (89, 96)


def test_prueba_ruidosa_el_ancho_baja_como_raiz_de_n():
    p = c.cifras_c2_prueba_ruidosa()
    assert abs(p["cociente_desv"] / math.sqrt(10) - 1) <= 0.15


def test_prueba_ruidosa_las_dos_nubes_se_centran_en_R():
    p = c.cifras_c2_prueba_ruidosa()
    for n in (20, 200):
        ee_mc = p[f"desv_{n}"] / math.sqrt(c.REP_PRUEBAS)
        assert abs(p[f"media_{n}"] - p["R"]) <= 3 * ee_mc


# ---------------------------------------------------- cifras_c2_optimismo ---

def test_optimismo_elegir_con_la_prueba_anuncia_de_menos():
    o = c.cifras_c2_optimismo()
    assert o["repeticiones"] == c.REP_OPTIMISMO
    assert o["sesgo_prueba"] < 0
    assert -o["sesgo_prueba"] > 3 * o["ee_prueba"]


def test_optimismo_las_cifras_de_la_pagina():
    o = c.cifras_c2_optimismo()
    assert (_r(o["sesgo_prueba"], 1), _r(o["ee_prueba"], 1)) == (-7.5, 1.8)
    assert round(100 * o["optimistas_prueba"]) == 74
    assert round(100 * o["optimistas_validacion"]) == 56
    assert (_r(o["media_L_ent"], 1), _r(o["media_L_val"], 1),
            _r(o["media_L_prueba"], 1)) == (8.5, 9.1, 12.6)


def test_optimismo_elegir_con_validacion_no_se_aleja_de_cero():
    o = c.cifras_c2_optimismo()
    assert abs(o["sesgo_validacion"]) < 2 * o["ee_validacion"]


def test_optimismo_el_modelo_final_reajustado_no_se_aleja_de_cero():
    o = c.cifras_c2_optimismo()
    assert abs(o["final_prueba_menos_R"]) < 2 * o["ee_final_prueba_menos_R"]


def test_optimismo_la_cadena_observada_ent_val_prueba():
    # P1 §4, idea 6: cada desigualdad a mas de 2 EE de Monte Carlo; si falla,
    # BLOQUEO y la pagina no la afirma (§10.12). Se cambia el texto, no la semilla.
    o = c.cifras_c2_optimismo()
    assert o["val_menos_ent"] > 2 * o["ee_val_menos_ent"]
    assert o["prueba_menos_val"] > 2 * o["ee_prueba_menos_val"]


def test_optimismo_sin_candidatos_que_elegir_no_hay_engano_que_crezca():
    por_M = c.cifras_c2_optimismo()["sesgo_prueba_por_M"]
    assert por_M[13] < por_M[1]


# ------------------------------------------------------- cifras_c2_imitar ---

def test_imitar_criterios_de_los_casos_13_a_15():
    k = c.cifras_c2_imitar()["criterios"]
    assert k["c13_R_sobre_azar"] >= 2
    assert k["c13_tiempo_rel"] <= 0.3
    assert k["c13_lineal_rel"] <= 0.1            # D-009.6: lineal en x no miente
    assert k["c14_R_sobre_azar"] >= 3
    assert k["c14_grupo_rel"] <= 0.3
    assert k["c15_R_sobre_prueba"] >= 3


def test_imitar_las_cifras_de_la_pagina():
    i = c.cifras_c2_imitar()
    tab = {ct: (_r(i[ct]["azar"]["L_prueba"], 1), _r(i[ct]["azar"]["R"], 1)) for ct in c.CONTRATOS}
    assert tab == {"más de lo mismo": (11.9, 9.3), "el mes que viene": (57.6, 135.6),
                   "pacientes nuevos": (1.9, 17.9), "otra ciudad": (13.1, 109.5)}
    assert (_r(i["el mes que viene"]["imita"]["L_prueba"], 1),
            _r(i["el mes que viene"]["imita"]["R"], 1)) == (119.4, 155.6)
    assert (_r(i["pacientes nuevos"]["imita"]["L_prueba"], 1),
            _r(i["pacientes nuevos"]["imita"]["R"], 1)) == (20.3, 18.0)
    k = i["criterios"]
    assert (_r(k["c13_R_sobre_azar"], 1), _r(k["c14_R_sobre_azar"], 1),
            _r(k["c15_R_sobre_prueba"], 1)) == (2.4, 9.7, 8.4)


def test_imitar_mas_de_lo_mismo_cae_dentro_de_2_ee():
    a = c.cifras_c2_imitar()["más de lo mismo"]["azar"]
    assert abs(a["L_prueba"] - a["R"]) <= 2 * a["ee"]


def test_imitar_r_del_caso_14_no_depende_del_orden_de_los_grupos():
    p = c.cifras_c2_imitar()["pacientes nuevos"]
    assert math.isclose(p["R_permutado"], p["azar"]["R"], rel_tol=1e-6)


# ------------------------------------------------------- cifras_c2_reparto ---

def test_reparto_los_extremos_que_se_citan():
    r = c.cifras_c2_reparto()
    assert r[0.5]["R"] - r[0.1]["R"] > 2 * math.hypot(r[0.5]["ee_R"], r[0.1]["ee_R"])
    assert r[0.1]["desv_error"] - r[0.5]["desv_error"] > 2 * math.hypot(
        r[0.5]["ee_desv"], r[0.1]["ee_desv"])


def test_reparto_las_cifras_de_la_pagina():
    r = c.cifras_c2_reparto()
    assert {f: (_r(r[f]["R"], 1), _r(r[f]["desv_error"], 1)) for f in (0.1, 0.2, 0.5)} == {
        0.1: (10.2, 7.2), 0.2: (10.4, 4.6), 0.5: (11.3, 3.0)}


# ---------------------------------------------------------- cifras_c2_hilo ---

def test_hilo_la_cv_elige_y_la_regla_de_un_ee_no_elige_mas():
    h = c.cifras_c2_hilo()
    assert (h["N_min"], h["N_un_ee"]) == (6, 6)
    assert h["N_un_ee"] <= h["N_min"]
    assert 3 <= h["N_min"] <= 6                  # criterio del hilo (§10.7 fila 1)


def test_hilo_las_cifras_de_la_pagina():
    h = c.cifras_c2_hilo()
    assert (_r(h["cv"][6], 2), _r(h["ee"][6], 2)) == (9.69, 1.33)
    assert _r(h["umbral"], 2) == 11.02
    assert h["costo_ajustes"] == 66
    assert _r(h["R_min"], 1) == 27.3
    assert (_r(h["L_prueba_min"], 1), _r(h["ee_prueba_min"], 1)) == (112.5, 73.5)
    assert (_r(h["benchmark_prueba"], 1), _r(h["benchmark_despliegue"], 1)) == (82.3, 51.4)
    assert h["N_mejor_R"] == 4 and _r(h["R_por_N"][4], 1) == 11.0
    assert _r(h["piso"], 1) == 9.0


def test_hilo_el_umbral_es_minimo_mas_un_ee():
    h = c.cifras_c2_hilo()
    assert math.isclose(h["umbral"], h["cv"][h["N_min"]] + h["ee"][h["N_min"]])


# ---------------------------------------------------- cifras_c2_cv_vs_val ---

def test_cv_vs_val_las_cifras_que_se_citan():
    v = c.cifras_c2_cv_vs_val()
    assert (_r(v["desv_val"], 1), _r(v["desv_cv"], 1)) == (4.9, 3.1)
    assert (_r(v["ee_val_medio"], 1), _r(v["ee_cv_medio"], 1)) == (4.4, 2.2)
    assert _r(v["media_R"], 1) == 11.2


# --------------------------------------------- cifras_c2_pliegue_anomalo ---

def test_pliegue_anomalo_los_dos_cocientes():
    p = c.cifras_c2_pliegue_anomalo()
    assert p[8]["cociente"] >= 5
    assert p[1]["cociente"] <= 2
    assert _r(p[1]["cociente"], 2) == 1.39


def test_pliegue_anomalo_las_dos_lejanas_caen_en_pliegues_distintos():
    # CAMBIO prog-lab-9: con pliegues(k=5, semilla=0) caen en los pliegues 2 y 3;
    # la pagina dice «los pliegues que traen una entrega lejana» (DECISION prog-c2-2).
    p = c.cifras_c2_pliegue_anomalo()
    assert p["pliegues_con_lejana"] == [2, 3]
    assert p[8]["pliegue_max"] in p["pliegues_con_lejana"]


def test_pliegue_anomalo_la_media_de_cada_estadistico_es_la_de_sus_pliegues():
    p = c.cifras_c2_pliegue_anomalo()
    for N in (1, 4, 8):
        for nombre in c.ESTADISTICOS:
            assert math.isclose(p[N][f"media_{nombre}"], float(p[N][nombre].mean()))


# ------------------------------------------------- cifras_c2_estratificada ---

def test_estratificada_las_cifras_de_la_pagina():
    e = c.cifras_c2_estratificada()
    assert round(100 * e["azar"]) == 88
    assert e["azar"] > 0.2
    assert e["estratificada"] == 0


def test_estratificada_con_tres_positivos_siempre_quedan_dos_vacios():
    assert c.cifras_c2_estratificada()["min_vacios_con_3"] >= 2


# ------------------------------------------------------ cifras_c2_anidada ---

def test_anidada_el_ganador_subestima_y_la_anidada_se_centra():
    a = c.cifras_c2_anidada()
    assert a["cv_ganador"] < a["R_procedimiento"]
    assert abs(a["anidada_menos_proc"]) < 2 * a["ee_anidada_menos_proc"]


def test_anidada_las_cifras_que_se_citan():
    a = c.cifras_c2_anidada()
    assert (_r(a["cv_ganador"], 1), _r(a["anidada"], 1), _r(a["R_procedimiento"], 1),
            _r(a["R_final"], 1)) == (10.0, 11.8, 12.7, 11.4)


# --------------------------------------------------- cifras_c2_ejercicios ---

def test_ejercicios_aritmetica_exacta():
    e = c.cifras_c2_ejercicios()
    a = e["ee_a_mano"]
    assert a["L_prueba"] == Fraction(5, 2) and a["s2"] == 3
    assert _r(a["ee"], 2) == 0.87
    assert e["cuadruplicar"] == {"ee_400": Fraction(2, 5), "n_para_02": 1600}
    assert e["tamano_prueba"] == 400
    assert e["cinco_pliegues"]["cv"] == Fraction("8.96")
    assert _r(e["cinco_pliegues"]["ee"], 3) == 0.093
    assert e["costo"] == {"cv": 66, "loo": 781, "anidada": 330}
    u = e["elige_un_ee"]
    assert (u["minimo"], u["umbral"], u["un_ee"], u["barra_2"]) == (4, Fraction("9.9"), 3,
                                                                     Fraction("9.7"))
    f = e["final_cv"]
    assert (f["cv_1"], f["cv_5"]) == (5, Fraction("4.8"))
    assert _r(f["desv_5"], 3) == 0.6 and _r(f["ee_5"], 3) == 0.346
    assert _r(f["umbral"], 3) == 5.146
    assert (f["minimo"], f["un_ee"], f["ajustes"]) == (5, 1, 7)
    t = e["tres_predicciones"]
    assert (t["sesgo"], t["varianza"], t["total"]) == (-1, Fraction(8, 3), Fraction(23, 3))
    assert e["clientes"] == {"por_entrega": 9, "por_cliente": 5}


def test_ejercicios_contraejemplo_de_la_cadena():
    # Razon del «No digas» de P1 §4: tras elegir, L_ent ≤ L_val no esta garantizada.
    cad = c.cifras_c2_ejercicios()["cadena"]
    assert cad == {"ent": Fraction(5, 6), "val": Fraction(2, 3), "R": Fraction(7, 6)}
    assert cad["ent"] > cad["val"]

# --- fin tramo rapido ---


# --- tramo m ---

def test_sesgo_varianza_el_ruido_es_la_varianza_del_proceso():
    s = c.cifras_c2_sesgo_varianza()
    for N in c.CANDIDATOS:
        assert abs(s[N]["ruido"] / s["sigma2_e"] - 1) <= 0.02
    assert _r(s["piso"], 1) == 9.0


def test_sesgo_varianza_el_sesgo_no_crece_con_el_grado_salvo_ruido_de_monte_carlo():
    # El sesgo² estimado lleva encima varianza/repeticiones (sesgo de Monte Carlo):
    # se compara contra el menor anterior con esa tolerancia y dos EE de la
    # estimacion (§10.7: «tolerancia MC»).
    s = c.cifras_c2_sesgo_varianza()
    r = c.REP_SV
    for N in range(1, 13):
        previo = min(s[M]["sesgo2"] for M in range(N))
        tol = s[N]["varianza"] / r + 2 * math.sqrt(4 * s[N]["sesgo2"] * s[N]["varianza"] / r
                                                   + 2 * (s[N]["varianza"] / r) ** 2)
        assert s[N]["sesgo2"] <= previo + tol + 0.05, N


def test_sesgo_varianza_el_total_es_la_suma():
    s = c.cifras_c2_sesgo_varianza()
    for N in c.CANDIDATOS:
        assert math.isclose(s[N]["total"], s[N]["ruido"] + s[N]["sesgo2"] + s[N]["varianza"],
                            rel_tol=1e-9)


def test_sesgo_varianza_n_estrella_igual_con_tres_semillas():
    s = c.cifras_c2_sesgo_varianza()
    assert s["N_estrella_semillas"] == [2, 2, 2]


def test_sesgo_varianza_las_cifras_de_la_diana():
    s = c.cifras_c2_sesgo_varianza()
    assert _r(s["f_x0"], 1) == 31.5
    assert (_r(s["diana_1"]["sesgo"], 1), _r(s["diana_1"]["desv"], 1)) == (1.5, 0.9)
    assert (_r(s["diana_12"]["sesgo"], 1), _r(s["diana_12"]["desv"], 1)) == (-0.5, 3.5)
    assert s["diana_1"]["fuera_eje"] == 0 and s["diana_12"]["fuera_eje"] == 0


def test_sesgo_varianza_la_tabla_que_se_cita():
    s = c.cifras_c2_sesgo_varianza()
    assert {N: _r(s[N]["total"], 1) for N in (1, 2, 4, 12)}[2] == 10.9
    assert (_r(s[1]["sesgo2"], 1), _r(s[1]["varianza"], 1)) == (6.0, 0.9)
    assert (_r(s[2]["sesgo2"], 1), _r(s[2]["varianza"], 1)) == (0.9, 1.0)


def test_numero_de_condicion_del_grado_12_con_36_entregas():
    # §10.7, antigua fila 16: polinomio(escalar=True) deja Φ^T Φ por debajo de 1e9
    # (sin escalar, x^12 con x en 0–6 lo lleva a ~1e20). DECISION prog-c2-2.
    assert c.cifras_c2_sesgo_varianza()["condicion_12"] < 1e9

# --- fin tramo m ---


# --- tramo completo ---

# ------------------------------------------- cifras_c2_curva_aprendizaje ---

def test_curva_aprendizaje_las_cifras_de_la_pagina():
    a = c.cifras_c2_curva_aprendizaje()
    assert a["piso"] == 9.0
    assert {n: _r(a["R"][(1, n)], 1) for n in (30, 480, 960)} == {30: 14.7, 480: 13.8, 960: 13.8}
    assert {n: _r(a["R"][(10, n)], 1) for n in (480, 960)} == {480: 9.1, 960: 9.0}
    assert a["elegido"][30] == 3 and a["elegido"][960] == 10


def test_curva_aprendizaje_la_recta_se_estanca_y_el_10_baja_hacia_el_piso():
    a = c.cifras_c2_curva_aprendizaje()
    assert a["R"][(1, 960)] > a["piso"] + 1
    assert a["R"][(10, 960)] < a["R"][(1, 960)]
    # el grado elegido sube con n (mediana)
    assert a["elegido"][960] > a["elegido"][30]


def test_curva_aprendizaje_las_medianas_citadas_son_estables_con_tres_semillas():
    a = c.cifras_c2_curva_aprendizaje()
    citadas = [(1, 30), (1, 480), (1, 960), (10, 480), (10, 960)]
    for otra in a["R_otras_semillas"].values():
        for k in citadas:
            assert abs(otra[k] / a["R"][k] - 1) < 0.05, k


def test_curva_aprendizaje_el_10_en_30_no_se_cita_pero_queda_arriba_de_la_recta():
    # su mediana cambia 40 % entre semillas maestras (18.6, 26.7, 25.6): la
    # pagina no la cita como numero, solo que queda arriba de la recta
    a = c.cifras_c2_curva_aprendizaje()
    assert a["R"][(10, 30)] > a["R"][(1, 30)]
    for otra in a["R_otras_semillas"].values():
        assert otra[(10, 30)] > otra[(1, 30)]


# ------------------------------------------------- cifras_c2_diagnostico ---

def test_diagnostico_cada_proceso_cae_en_su_hoja():
    d = c.cifras_c2_diagnostico()
    assert {k: v["hoja"] for k, v in d.items()} == c.HOJA_DIAGNOSTICO


def test_diagnostico_las_propiedades_de_cada_hoja():
    d = c.cifras_c2_diagnostico()
    A, B, C, D = (d[k] for k in "ABCD")
    assert B["CV"] > c.UMBRAL_BRECHA * B["L_ent"]
    for r in (A, C, D):
        assert r["CV"] <= c.UMBRAL_BRECHA * r["L_ent"]
    # C: en (a) no le gana al benchmark a 2 EE, y en (b) falta evidencia
    assert not C["dif_val"] < -2 * C["dif_val_ee"]
    assert not C["senal_b"]
    # A y D le ganan en (a)
    assert A["dif_val"] < -2 * A["dif_val_ee"] and D["dif_val"] < -2 * D["dif_val_ee"]
    # A: un grado mas alto baja la CV mas de un EE; D: ninguno
    assert A["CV_mejor_mas_flexible"] < A["CV"] - A["EE"]
    assert not D["CV_mejor_mas_flexible"] < D["CV"] - D["EE"]


def test_diagnostico_las_cifras_del_micro():
    d = c.cifras_c2_diagnostico()
    fila = {k: (_r(v["L_ent"], 1), _r(v["CV"], 1), _r(v["EE"], 1)) for k, v in d.items()}
    assert fila == {"A": (12.6, 15.1, 0.9), "B": (5.7, 262.2, 143.9),
                    "C": (59.2, 66.3, 4.9), "D": (8.5, 9.7, 0.5)}
    assert (_r(d["A"]["CV_mejor_mas_flexible"], 1), d["A"]["mejor_mas_flexible"]) == (9.7, 8)
    assert {k: (_r(v["dif_val"], 1), _r(v["dif_val_ee"], 1)) for k, v in d.items()
            if k != "B"} == {"A": (-40.2, 8.7), "C": (-0.1, 0.3), "D": (-49.6, 9.5)}


def test_diagnostico_no_calcula_un_ee_con_perdidas_fuera():
    # guarda negativa (contrato v4 §3): ninguna cifra de la clase 2 hace
    # s_d/√n sobre perdidas_fuera de CV
    fuente = inspect.getsource(c.cifras_c2_diagnostico)
    assert "perdidas_fuera" not in fuente.split('"""', 2)[2]
    assert "error_estandar" not in fuente


# ------------------------------------------- cifras_c2_diagnostico_final ---

def test_diagnostico_final_a_mejora_y_b_se_estanca():
    f = c.cifras_c2_diagnostico_final()
    assert f["A"]["mejora"] > 0.20
    assert f["B"]["mejora"] < 0.05


def test_diagnostico_final_las_cifras_del_ejercicio():
    f = c.cifras_c2_diagnostico_final()
    tabla = {k: tuple(_r(v[n][q], 1) for n in c.N_CONSULTOR for q in ("L_ent", "CV"))
             for k, v in f.items()}
    assert tabla == {"A": (8.1, 11.8, 8.7, 9.2), "B": (13.9, 14.4, 14.3, 14.4)}


# --- fin tramo completo ---


# ------------------------------------------- cifras_c2_taller_descomponer ---

def test_taller_descomponer_el_grado_12_se_dispara_en_los_bordes():
    """Revision r1: el guion 05 avisa del sesgo² enorme del grado 12 en el taller."""
    t = c.cifras_c2_taller_descomponer()
    assert round(t[12]["sesgo2"]) == 603 and t[12]["varianza"] > 10_000
    assert t[6]["sesgo2"] < 1


def test_sesgo_varianza_el_sesgo2_vuelve_a_crecer_y_en_el_interior_no():
    """Revision r1: P3 §3 limita «el sesgo baja» a N ≤ 7 y lo explica con el tramo
    interior, donde el sesgo² no pasa de 0.25 desde N = 6."""
    s = c.cifras_c2_sesgo_varianza()
    assert all(s[N]["sesgo2"] < 1 for N in range(2, 9))
    assert s[9]["sesgo2"] > 10 and s[12]["sesgo2"] > 50
    assert max(s["sesgo2_interior"][N] for N in range(6, 13)) <= 0.25
    assert s[1]["varianza"] < s[0]["varianza"]
