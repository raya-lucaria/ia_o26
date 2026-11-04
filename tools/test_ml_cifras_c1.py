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

pytest.importorskip("pandas")


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

# --- fin tramo 1a ---


# --- tramo 1b ---
# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---
