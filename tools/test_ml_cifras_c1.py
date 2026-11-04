"""Fija en la fuente las cifras de la clase 1 (tools/ml_cifras_c1.py).

Sin prosa (D-003): estas pruebas no leen ninguna pagina. Que la pagina cite
la misma cifra lo comprueba tools/test_ml_prosa_c1.py. Cada valor fijado aqui
es el que la pagina escribe (redondeado como lo escribe la pagina); si una
cifra cambia, esta prueba falla y obliga a revisar la prosa.

Anclas por tramo (protocolo p5.2 §7.1): cada rama agrega sus pruebas solo
antes del «fin» de su tramo.
"""
import math
from fractions import Fraction

import pytest

import ml_cifras_c1 as c

pd = pytest.importorskip("pandas")


def _r(v, d):
    return round(float(v), d)


# --- tramo 1a ---

# ---------------------------------------------------- cifras_c1_ganador ---

def comprobar_ganador(g):
    assert _r(g["intercepto_recta"], 6) == 10.6
    assert Fraction(g["pendiente_recta"]).limit_denominator(100) == Fraction(134, 35)
    assert _r(g["rmse_1"], 3) == 0.956
    assert _r(g["rmse_5"], 3) == 0.0
    assert _r(g["mse_1"], 3) == 0.914
    assert _r(g["mse_fija"], 3) == 1.0
    assert _r(g["mse_1"], 9) == _r(g["rmse_1"] ** 2, 9)
    p = g["prediccion"]
    assert (_r(p[7.0][0], 1), _r(p[7.0][1], 1)) == (37.4, -25.0)
    assert (_r(p[3.5][0], 1), _r(p[3.5][1], 1)) == (24.0, 24.0)
    assert (_r(p[0.0][0], 1), _r(p[0.0][1], 1)) == (10.6, 73.0)


def test_ganador_las_cifras_de_la_pagina():
    comprobar_ganador(c.cifras_c1_ganador())


def test_ganador_el_polinomio_de_grado_5_pasa_por_las_seis():
    g = c.cifras_c1_ganador()
    # Coeficientes exactos: -4/15, 14/3, -92/3, 280/3, -1876/15, 73.
    esperado = [Fraction(-4, 15), Fraction(14, 3), Fraction(-92, 3), Fraction(280, 3),
                Fraction(-1876, 15), Fraction(73)]
    for coef, exacto in zip(g["coeficientes_grado_5"], esperado):
        assert math.isclose(coef, float(exacto), rel_tol=1e-9, abs_tol=1e-9)


def test_ganador_las_fracciones_que_escribe_la_pagina_son_exactas():
    g = c.cifras_c1_ganador()
    fr = g["coeficientes_grado_5_fracciones"]
    assert fr == [Fraction(-4, 15), Fraction(14, 3), Fraction(-92, 3), Fraction(280, 3),
                  Fraction(-1876, 15), Fraction(73)]
    assert g["pendiente_recta_fraccion"] == Fraction(134, 35)
    # Con aritmetica exacta, el polinomio pasa por las seis entregas.
    for x, y in zip(c.ENTREGAS_X, c.ENTREGAS_Y):
        valor = sum(a * Fraction(int(x)) ** (5 - k) for k, a in enumerate(fr))
        assert valor == Fraction(int(y)), (x, valor)
    assert fr[-1] == 73          # su valor en 0 km es la constante
    assert sum(a * Fraction(7) ** (5 - k) for k, a in enumerate(fr)) == -25
    assert sum(a * Fraction(7, 2) ** (5 - k) for k, a in enumerate(fr)) == 24


def test_ganador_por_otro_camino_con_fracciones_exactas():
    # Minimos cuadrados de la recta con fracciones: pendiente = Sxy / Sxx.
    x = [Fraction(int(v)) for v in c.ENTREGAS_X]
    y = [Fraction(int(v)) for v in c.ENTREGAS_Y]
    mx, my = sum(x) / 6, sum(y) / 6
    b1 = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    b0 = my - b1 * mx
    assert (b0, b1) == (Fraction(53, 5), Fraction(134, 35))
    mse = sum((b - b0 - b1 * a) ** 2 for a, b in zip(x, y)) / 6
    assert mse == Fraction(32, 35)
    assert b0 + 7 * b1 == Fraction(187, 5)


def test_ganador_la_mutacion_de_un_dato_pone_roja_la_comprobacion(monkeypatch):
    monkeypatch.setattr(c, "ENTREGAS_Y", (15.0, 17.0, 23.0, 25.0, 31.0, 34.0))
    with pytest.raises(AssertionError):
        comprobar_ganador(c.cifras_c1_ganador())


# ------------------------------------------------------- cifras_c1_piso ---

def comprobar_piso(p):
    uno, dos = p[1.0], p[2.0]
    assert (uno["piso"], dos["piso"]) == (1.0, 4.0)
    assert uno["n_ent"] == dos["n_ent"] == 20
    assert uno["n_despliegue"] == 100_000
    # R aproximado con 100 000 observaciones, como lo escribe la pagina.
    assert (_r(uno["R_oraculo"], 3), _r(uno["R_recta"], 3), _r(uno["R_media"], 1)) == (
        0.991, 1.025, 49.1)
    assert (_r(dos["R_oraculo"], 3), _r(dos["R_recta"], 3), _r(dos["R_media"], 1)) == (
        3.965, 4.1, 52.1)
    assert _r(uno["ee_oraculo"], 4) == 0.0045
    assert _r(dos["ee_oraculo"], 3) == 0.018
    assert _r(uno["L_ent_recta"], 3) == 0.45
    assert _r(uno["L_ent_oraculo"], 3) == 0.489


def test_bloque_1_coincide_con_el_piso_por_otro_camino():
    b, p = c.cifras_c1_bloque_1(), c.cifras_c1_piso()[1.0]
    assert (_r(b["L_ent_recta"], 3), _r(b["R_recta"], 3), _r(b["R_media"], 3)) == (
        0.45, 1.025, 49.073)
    assert _r(b["L_ent_recta"], 9) == _r(p["L_ent_recta"], 9)
    assert _r(b["R_recta"], 9) == _r(p["R_recta"], 9)


def test_piso_las_cifras_de_la_pagina():
    comprobar_piso(c.cifras_c1_piso())


def test_piso_duplicar_sigma_cuadruplica_el_piso():
    p = c.cifras_c1_piso()
    assert p[2.0]["piso"] == 4 * p[1.0]["piso"]


def test_piso_ninguna_barra_queda_claramente_bajo_el_piso():
    # «Claramente» = mas de 3 errores estandar de la muestra enorme.
    for s, fila in c.cifras_c1_piso().items():
        for clave in ("oraculo", "recta", "media"):
            assert fila[f"R_{clave}"] > fila["piso"] - 3 * fila[f"ee_{clave}"], (s, clave)


def test_piso_mutacion_de_semilla_pone_roja_la_comprobacion():
    with pytest.raises(AssertionError):
        comprobar_piso(c.cifras_c1_piso(semilla=1))


# ----------------------------------------------------- cifras_c1_lluvia ---

def test_lluvia_pisos_y_pendientes():
    ll = c.cifras_c1_lluvia()
    assert ll["piso_sin_x2"] == pytest.approx(10.0, abs=1e-9)
    assert ll["piso_con_x2"] == pytest.approx(1.0, abs=1e-9)
    assert ll["piso_sin_x2_exacto"] == 1 + 36 * Fraction(1, 4) == 10
    assert ll["n_ent"] == 20
    assert ll["columnas_sin"] == ["x1"] and ll["columnas_con"] == ["x1", "x2"]
    assert (_r(ll["beta1_sin_x2"], 2), _r(ll["beta1_con_x2"], 2)) == (3.98, 4.01)
    assert (_r(ll["R_recta_sin_x2"], 1), _r(ll["R_recta_con_x2"], 2)) == (10.9, 1.23)


def test_lluvia_subir_el_grado_no_baja_el_riesgo():
    gr = c.cifras_c1_lluvia_grados()
    sin, con = gr[False], gr[True]
    assert (_r(sin[1], 2), _r(sin[5], 2)) == (10.89, 15.73)
    assert (_r(con[1], 2), _r(con[5], 2)) == (1.23, 1.71)
    # Ningun grado baja del de grado 1 por mas de una centesima, y el 5 es el peor.
    for d in (sin, con):
        assert min(d.values()) > d[1] - 0.01
        assert max(d, key=d.get) == 5
    assert gr["piso"] == {False: pytest.approx(10.0), True: pytest.approx(1.0)}
    assert _r(sin[1], 6) == _r(c.cifras_c1_lluvia()["R_recta_sin_x2"], 6)


# ---------------------------------------------------- cifras_c1_anillos ---

def comprobar_anillos(a):
    assert a["parametros"] == {"n": 400, "radio_interior": 1.0, "radio_exterior": 1.6,
                               "grosor": 0.4, "ruido": 0.15}
    assert a["n_ent"] == 400
    assert a["cartesianas"]["columnas"] == ["1", "x1", "x2"]
    assert a["polares"]["columnas"] == ["1", "r", "theta"]
    assert a["solo radio"]["columnas"] == ["1", "r"]
    # Lo que la pagina escribe, en porcentaje entero.
    assert round(100 * a["cartesianas"]["aciertos"]) == 48
    assert round(100 * a["moda"]) == 50
    assert round(100 * a["polares"]["aciertos"]) == 75
    assert round(100 * a["solo radio"]["aciertos"]) == 75
    assert round(100 * a["bayes"]) == 76
    assert _r(a["polares"]["beta"]["theta"], 2) == -0.07
    assert _r(a["solo radio"]["radio_corte"], 2) == 1.25
    assert _r(a["polares"]["radio_corte"], 2) == 1.25


def test_anillos_las_cifras_de_la_pagina():
    comprobar_anillos(c.cifras_c1_anillos())


def test_anillos_ni_bayes_llega_a_100_y_nadie_pasa_a_bayes_por_mucho():
    a = c.cifras_c1_anillos()
    assert a["bayes"] < 1
    for rep in c.REPRESENTACIONES:
        assert a[rep]["aciertos"] <= a["bayes"] + 0.01


def test_anillos_mutacion_de_semilla_pone_roja_la_comprobacion():
    with pytest.raises(AssertionError):
        comprobar_anillos(c.cifras_c1_anillos(semilla=3))


# ---------------------------------------------------- cifras_c1_omitida ---

def test_omitida_caso_1():
    o = c.cifras_c1_omitida()
    assert o["n_ent"] == 200
    assert abs(o["beta1_ajustada"] - 1.8) < 0.05
    assert _r(o["beta1_ajustada"], 2) == 1.84
    assert abs(o["beta1_estructural"] - 1) < 1e-2
    assert o["pendiente_f_visible"] == pytest.approx(1.8, abs=1e-12)
    assert abs(o["piso_visible"] - 0.86) < 0.01
    assert o["piso_visible_cuenta"] == pytest.approx(0.86, abs=1e-12)

# ------------------------------------------- cifras de la revision r3 ---

def test_residual_ruido_reducible_y_residual():
    r = c.cifras_c1_residual()
    assert (r["ruido"], r["reducible"], r["residual"]) == (3.0, -1.5, 1.5)
    assert r["ruido"] + r["reducible"] == r["residual"]


def test_ej_piso_es_sigma_cuadrada():
    e = c.cifras_c1_ej_piso()
    assert e["piso"] == pytest.approx(4.0) and e["n_muestra"] == 10


def test_lluvia_E_sin_x2_es_13_mas_4x1():
    ll = c.cifras_c1_lluvia()
    assert (ll["intercepto_sin_x2"], ll["pendiente_sin_x2"]) == pytest.approx((13.0, 4.0))


def test_arriba_abajo_con_solo_r_queda_en_50():
    a = c.cifras_c1_arriba_abajo()
    assert abs(a["aciertos"] - 0.5) < 0.02 and a["bayes_solo_r"] == 0.5


# --- fin tramo 1a ---


# --- tramo 1b ---

# ------------------------------------------------------ cifras_c1_taylor ---

def test_taylor_el_error_en_2_5_crece_de_grado_3_a_9():
    t = c.cifras_c1_taylor()
    assert (_r(t["taylor_3"][2.5], 3), _r(t["taylor_9"][2.5], 2)) == (10.125, 115.33)
    assert t["taylor_9"][2.5] > t["taylor_3"][2.5]
    # Del lado convergente (x = 0.3) subir el grado si ayuda.
    assert t["taylor_9"][0.3] < t["taylor_3"][0.3]
    # Minimos cuadrados reparte el error: en x = 2.5 queda muy por debajo.
    assert _r(t["mco_3"][2.5], 2) == 0.11
    assert t["micro"] == {"taylor_en_2": 0.0, "f_en_2": 0.5, "error": 0.5}


def test_taylor_coincide_con_la_serie_escrita_a_mano():
    # 2 + 5/x en x0 = 1: f^(k)(1)/k! = 5 (-1)^k, mas el 2 del termino constante.
    t = c.cifras_c1_taylor()
    for N in (3, 9):
        p = 2 + sum(5 * (-1) ** k * (2.5 - 1) ** k for k in range(N + 1))
        assert math.isclose(t[f"taylor_{N}"][2.5], abs(p - (2 + 5 / 2.5)), rel_tol=1e-12)


# ------------------------------------------------- cifras_c1_weierstrass ---

def test_weierstrass_el_error_maximo_baja_con_el_grado():
    w = c.cifras_c1_weierstrass()
    errores = [_r(w[N]["error_maximo"], 3) for N in (2, 6, 14)]
    assert errores == [0.094, 0.043, 0.021]
    assert errores == sorted(errores, reverse=True)


# ------------------------------------------------ cifras_c1_tres_ajustes ---

def test_tres_ajustes_L_ent_baja_y_R_hace_la_u():
    t = c.cifras_c1_tres_ajustes()
    assert [(_r(t[N]["L_ent"], 3), _r(t[N]["R"], 2)) for N in (1, 4, 15)] == [
        (4.352, 5.36), (0.184, 0.44), (0.034, 1450.97)]
    assert t[1]["L_ent"] > t[4]["L_ent"] > t[15]["L_ent"]
    assert t[4]["R"] < t[1]["R"] < t[15]["R"]


# --------------------------------------------------- cifras_c1_capacidad ---

def comprobar_capacidad(k):
    veinte, doscientos = k[20], k[200]
    assert veinte["N_menor_R"] == 6
    assert _r(veinte["R"][6], 3) == 0.366
    assert _r(veinte["R"][15], 0) == 1537
    assert _r(veinte["L_ent"][15], 3) == 0.034
    assert _r(veinte["benchmark"], 1) == 10.5
    assert doscientos["N_menor_R"] == 8


def test_capacidad_las_cifras_de_la_pagina():
    comprobar_capacidad(c.cifras_c1_capacidad())


def test_capacidad_la_u_del_plan():
    k = c.cifras_c1_capacidad()[20]
    assert 3 <= k["N_menor_R"] <= 6
    assert k["R"][15] >= 2 * k["R"][k["N_menor_R"]]
    assert k["piso"] == 0.25


def test_capacidad_L_ent_nunca_sube_con_familias_anidadas():
    for n in (20, 200):
        L = c.cifras_c1_capacidad()[n]["L_ent"]
        assert all(L[N + 1] <= L[N] + 1e-12 for N in range(1, 15)), n


def test_capacidad_L_ent_baja_del_piso_y_R_no():
    k = c.cifras_c1_capacidad()[20]
    assert k["L_ent"][15] < k["piso"]
    assert min(k["R"].values()) > k["piso"]


def test_capacidad_con_200_datos_casi_plana():
    R = c.cifras_c1_capacidad()[200]["R"]
    assert max(R[N] for N in range(5, 16)) < 1.1 * min(R.values())


def test_capacidad_mutacion_de_semilla_pone_roja_la_comprobacion():
    with pytest.raises(AssertionError):
        comprobar_capacidad(c.cifras_c1_capacidad(semilla=1))


# --------------------------------------- el ajuste rapido es el de ml_lab ---

def test_el_ajuste_rapido_coincide_con_ml_ajustar():
    import numpy as np
    import aprendizaje_maquina as ml
    x, y = c.trozos_inverso(3)[2]
    df = pd.DataFrame({"x": x, "y": y})
    malla = pd.DataFrame({"x": c.MALLA_R})
    for N in (1, 6, 15):
        pred, L = c.ajuste_rapido(x, y, N)
        m = ml.ajustar(df, phi=ml.polinomio(N), columnas_x=["x"], tarea="regresion")
        assert math.isclose(L, float(np.mean((y - m.predecir(df)) ** 2)), rel_tol=1e-8)
        assert np.allclose(pred(c.MALLA_R), m.predecir(malla), rtol=1e-7, atol=1e-7)


def test_el_riesgo_por_malla_coincide_con_la_muestra_enorme():
    import aprendizaje_maquina as ml
    datos = c.datos_inverso()
    m = ml.ajustar(datos, phi=ml.polinomio(4))
    pred, _ = c.ajuste_rapido(datos.ent.x.to_numpy(), datos.ent.y.to_numpy(), 4)
    assert abs(c.riesgo_inverso(pred) - ml.riesgo(m, datos)) < 0.01


# --------------------------------------------------- cifras_c1_optimismo ---

def test_optimismo_beta_fijo_insesgado_beta_gorro_optimista():
    o = c.cifras_c1_optimismo()
    assert o["repeticiones"] == 500
    assert (_r(o["R_fijo"], 2), _r(o["media_L_ent_fijo"], 2)) == (0.31, 0.30)
    assert (_r(o["media_L_ent_gorro"], 2), _r(o["media_R_gorro"], 2)) == (0.21, 0.71)
    assert abs(o["media_L_ent_fijo"] - o["R_fijo"]) < 0.02
    assert o["media_L_ent_gorro"] < o["R_fijo"] < o["media_R_gorro"]
    # En promedio, no en cada muestra: alguna sale al reves.
    assert o["muestras_al_reves"] == 9


# ------------------------------------------------------ cifras_c1_elegir ---

def test_elegir_L_ent_siempre_se_va_al_maximo():
    e = c.cifras_c1_elegir()
    assert (e["repeticiones"], e["N_max"], e["veces_N_max_ent"]) == (200, 15, 200)
    assert e["moda_N_R"] == 5
    assert e["veces_N_R_3_a_6"] == 166
    assert sum(e["reparto_N_R"].values()) == 200
    assert max(e["reparto_N_R"]) == 10


# ----------------------------------------------------- cifras_c1_inverso ---

def test_inverso_la_columna_correcta_gana_a_diez_potencias():
    i = c.cifras_c1_inverso()
    assert i["n"] == 60
    assert (_r(i["R_1"], 1), _r(i["R_4"], 1), _r(i["R_10"], 2), _r(i["R_inverso"], 2)) == (
        82.4, 18.2, 1.28, 0.25)
    assert (_r(i["beta_inverso"][0], 2), _r(i["beta_inverso"][1], 2)) == (2.03, 5.0)
    assert i["mejor_polinomio_R"] >= 1.5 * i["R_inverso"]


def test_inverso_razon_del_caso_3_con_20_y_60_datos():
    for n in (20, 60):
        i = c.cifras_c1_inverso(n=n)
        assert i["mejor_polinomio_R"] >= 1.5 * i["R_inverso"], n


def test_caso_4_sin_escalar_sube_L_ent_y_avisa():
    k = c.cifras_c1_inverso()["caso_4"]
    assert k[(25, False)]["L_ent"] > k[(10, False)]["L_ent"]
    assert any("mal condicionada" in a for a in k[(25, False)]["avisos"])
    assert not any("pseudoinversa" in a for a in k[(25, False)]["avisos"])
    assert k[(25, True)]["L_ent"] <= k[(10, True)]["L_ent"]
    assert (_r(k[(10, False)]["L_ent"], 2), _r(k[(25, False)]["L_ent"], 1),
            _r(k[(25, True)]["L_ent"], 2)) == (1.11, 13.4, 0.18)


def test_columnas_binomiales():
    assert c.cifras_c1_columnas() == {5: 56, 20: 1771}


# -------------------------------------------------- cifras_c1_extrapolar ---

def test_extrapolar_fuera_es_mucho_peor_que_dentro():
    e = c.cifras_c1_extrapolar()
    seno = e["seno"]["grado_7"]
    assert seno["fuera"] >= 10 * seno["dentro"]
    assert (_r(seno["dentro"], 2), _r(seno["fuera"], 0)) == (0.10, 609)
    ent = e["entregas"]
    assert ent["grado_7"]["fuera"] > 1e5
    assert (_r(ent["recta"]["dentro"], 2), _r(ent["recta"]["fuera"], 2)) == (1.03, 1.14)


def test_extrapolar_el_recursivo_necesita_el_tiempo_anterior():
    r = c.cifras_c1_extrapolar()["recursivo"]
    assert (r["n"], r["futuro"], r["piso"]) == (60, 20, 1.0)
    sin, con = r["sin_anterior"], r["con_anterior"]
    # Sin el tiempo anterior falla tambien dentro (le falta una variable)...
    assert sin["dentro"] > 3 * r["piso"]
    # ...y con el, a un paso, queda cerca del piso dentro y en el futuro.
    assert con["dentro"] < 1.1 and con["futuro"] < 1.1
    assert (_r(sin["dentro"], 1), _r(sin["futuro"], 1), _r(con["futuro"], 2)) == (
        5.5, 36.4, 1.05)


# ---------------------------------------------- cifras_c1_no_free_lunch ---

def test_no_free_lunch_promedio_exacto_un_medio():
    nfl = c.cifras_c1_no_free_lunch()
    assert nfl["funciones"] == 256
    assert nfl["entrenamiento"] == ("000", "011", "101", "110")
    for regla in ("vecino", "mayoria", "siempre_1"):
        assert nfl[regla]["promedio"] == Fraction(1, 2)
    assert set(nfl["siempre_1"]["por_rugosidad"].values()) == {Fraction(1, 2)}
    assert sorted(nfl["tamanos"]) == [0, 3, 4, 5, 6, 7, 8, 9, 12]
    assert sum(nfl["tamanos"].values()) == 256


def test_no_free_lunch_extremos_por_rugosidad():
    nfl = c.cifras_c1_no_free_lunch()
    for regla in ("vecino", "mayoria"):
        r = nfl[regla]["por_rugosidad"]
        assert (r[0], r[12]) == (1, 0)


def test_no_free_lunch_promedio_global_no_es_media_de_medias():
    nfl = c.cifras_c1_no_free_lunch()
    tam = nfl["tamanos"]
    for regla in ("vecino", "mayoria"):
        r = nfl[regla]["por_rugosidad"]
        ponderado = sum(r[g] * tam[g] for g in tam) / 256
        assert ponderado == Fraction(1, 2)


def test_no_free_lunch_la_mayoria_desempata_a_favor_de_1():
    # Entrenamiento 1, 1, 0, 0 y todo lo no visto en 0: si predijera 0 acertaria todo.
    assert c.cifras_c1_no_free_lunch()["desempate_mayoria"]["aciertos_fuera"] == 0


# --------------------------------------------------- cifras_c1_par_impar ---

def test_par_impar_el_polinomio_se_dispara_y_la_periodica_no():
    p = c.cifras_c1_par_impar()
    assert p["interpola"]
    assert p["grado_7"] == {9: 640, 10: 4485}
    assert p["periodica"][9] == 0.0 and p["periodica"][10] == 5.0
    assert all(p["periodica"][x] == (5.0 if x % 2 == 0 else 0.0) for x in range(1, 11))

# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---

