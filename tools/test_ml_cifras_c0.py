"""Pruebas puras de tools/ml_cifras_c0.py (clase 0, unidad 9; sin prosa).

Cada valor de la tabla de clase_0.md §10.7: los seis pares de la unidad 6, el
MAE de las tres reglas en lo visto y en lo nuevo, la recta de minimos
cuadrados sobre las cuatro vistas y la de las seis. Las que leen la pagina
viven en tools/test_ml_prosa_c0.py (D-003).

Mutacion anotada en el commit de C0.T1: cambiar y_5 de 31 a 30 en ENTREGAS
mueve el MAE de la recta en las nuevas (1.2 -> 0.7) y
test_mae_de_las_tres_reglas lo marca en rojo (6 de 15 pruebas fallan).
"""
from fractions import Fraction

import numpy as np
import pytest

import ml_cifras_c0 as c0

APROX = pytest.approx


def test_los_seis_pares_son_los_de_la_unidad_6():
    e = c0.entregas_c0()
    assert e["pares"] == ((1, 15), (2, 17), (3, 23), (4, 25), (5, 31), (6, 33))
    assert e["vistas"] == [0, 1, 2, 3]
    assert e["nuevas"] == [4, 5]


@pytest.mark.parametrize("regla, vistas, nuevas", [
    ("memorizar", 0, 7),
    ("recta", 0.8, 1.2),
    ("promedio", 4, 12),
])
def test_mae_de_las_tres_reglas(regla, vistas, nuevas):
    c = c0.cifras_c0_memorizar()
    assert c[regla]["mae_vistas"] == APROX(vistas, abs=1e-9)
    assert c[regla]["mae_nuevas"] == APROX(nuevas, abs=1e-9)


def test_anuncios_en_las_nuevas():
    c = c0.cifras_c0_memorizar()
    assert c["memorizar"]["anuncios_nuevas"] == [25, 25]
    assert c["promedio"]["anuncios_nuevas"] == [20, 20]
    assert c["recta"]["anuncios_nuevas"] == APROX([29, 32.6], abs=1e-9)
    assert c["promedio_vistas"] == 20


def test_memorizar_acierta_lo_visto_por_construccion():
    c = c0.cifras_c0_memorizar()
    assert c["memorizar"]["anuncios_vistas"] == [15, 17, 23, 25]
    assert c["memorizar"]["mae_vistas"] == 0


def test_memorizar_es_el_vecino_mas_cercano():
    # 5 y 6 km: la vista mas cercana es la de 4 km (25 min); 2.4 km -> 2 km.
    assert c0.anuncio_memorizar(5) == 25
    assert c0.anuncio_memorizar(6) == 25
    assert c0.anuncio_memorizar(2.4) == 17


def test_beta_estrella_es_11_y_3_6():
    b0, b1 = c0.cifras_c0_memorizar()["beta_estrella"]
    assert (b0, b1) == APROX((11, 3.6), abs=1e-9)
    assert c0.recta_exacta(c0.VISTAS) == (Fraction(11), Fraction(18, 5))


def test_la_recta_es_el_minimo_gradiente_cero():
    b0, b1 = c0.cifras_c0_memorizar()["beta_estrella"]
    x = np.array([1, 2, 3, 4], dtype=float)
    y = np.array([15, 17, 23, 25], dtype=float)
    r = y - b0 - b1 * x
    assert r.sum() == APROX(0, abs=1e-9)
    assert (r * x).sum() == APROX(0, abs=1e-9)
    # y es unico: las cuatro distancias no son todas iguales
    assert np.linalg.matrix_rank(np.column_stack([np.ones(4), x])) == 2


def test_la_recta_de_las_seis_es_la_de_la_unidad_6():
    c = c0.cifras_c0_memorizar()
    assert c["beta_seis_exacta"] == (Fraction(106, 10), Fraction(134, 35))
    assert c["beta_seis"] == APROX((10.6, 134 / 35), abs=1e-9)


def test_redondeo_como_en_la_pagina():
    assert [c0.redondeo(v) for v in (0, 0.8, 4, 7, 1.2, 12, 32.6, 29.0)] == \
        ["0", "0.8", "4", "7", "1.2", "12", "32.6", "29"]


def test_curva_del_tramo_completo_no_es_monotona():
    curva = c0.cifras_c0_curva()
    assert [curva[n][2] for n in (2, 3, 4)] == APROX([8, 1.0, 1.2], abs=1e-9)
    assert curva[2][:2] == APROX((13, 2), abs=1e-9)
    assert curva[3][:2] == APROX((31 / 3, 4), abs=1e-9)


def test_paquetes_y_agrupaciones():
    p = c0.cifras_c0_paquetes()
    assert len(p["paquetes"]) == len(p["zonas"]) == 6
    assert all(isinstance(k, int) and 1 <= k <= 12 for k in p["paquetes"])
    assert 2 <= len(set(p["zonas"])) <= 3
    grupos = {nombre: tuple(map(tuple, a["grupos"]))
              for nombre, a in p["agrupaciones"].items()}
    assert len(grupos) == 2
    # dos agrupaciones distintas, cada una parte las seis
    assert len(set(grupos.values())) == 2
    for g in grupos.values():
        assert sorted(g[0] + g[1]) == list(range(6)) and g[0] and g[1]
        # ninguna es vistas / nuevas
        assert set(g[0]) != set(c0.VISTAS) and set(g[1]) != set(c0.VISTAS)


def test_datos_de_los_ejercicios():
    assert c0.datos_c0_ejercicios() == {
        "por_semana": 10, "mae_visto": (3, 1), "semanas": 4,
        "mae_nuevo": 6, "entregas_zona": 200}


def test_no_importa_ml_lab_desde_assets():
    # guarda de origen (contrato §5.2): si algun dia importa ml_lab, de tools/.
    import inspect
    fuente = inspect.getsource(c0)
    assert "_assets" not in fuente.split('"""', 2)[2]


def test_phi_del_ejemplo_de_la_seccion_3():
    assert c0.phi_cuadratica(c0.PHI_EJEMPLO_KM) == (1, 3, 9)
