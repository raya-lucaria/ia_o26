"""Fija cada cifra de la clase 2 de Markov (course/8_markov/2_a_la_larga/)
contra su funcion de tools/markov.py, con el valor escrito a mano.

La tabla de cifras que usan las paginas es
.superpowers/unidad/markov/clase-2/cifras.md (local); aqui se fija lo exacto
y lo simulado con su semilla. La busqueda de cada cifra en su pagina se
agrega cuando las paginas existan.
"""
from fractions import Fraction as F

import pytest

import markov as m


# ------------------------------------------------------------------ T1 ---

def test_t1_es_la_matriz_de_la_frase():
    assert m.t1_matriz() == m.T1_P == [[F(2, 11), F(9, 11)], [F(2, 3), F(1, 3)]]


def test_t1_estacionaria():
    assert m.estacionaria(m.T1_P) == [F(22, 49), F(27, 49)]


def test_t1_una_clase_cerrada_aperiodica():
    assert m.clases(m.T1_P) == [{"estados": (0, 1), "cerrada": True, "periodo": 1}]


def test_t1_la_distancia_se_multiplica_exactamente_por_16_33():
    assert m.segundo_valor_propio_2x2(m.T1_P) == F(-16, 33)
    assert abs(F(2, 11) - F(2, 3)) == F(16, 33)
    for mu0, d0 in (((F(1), F(0)), F(54, 49)), ((F(0), F(1)), F(44, 49))):
        d = m.distancias_t(m.T1_P, mu0, 10)
        assert d[0] == d0
        assert all(d[t] == d0 * F(16, 33) ** t for t in range(11))


def test_t1_distancias_a_mano():
    dV = m.distancias_t(m.T1_P, (F(1), F(0)), 3)
    dC = m.distancias_t(m.T1_P, (F(0), F(1)), 3)
    assert dV == [F(54, 49), F(288, 539), F(1536, 5929), F(8192, 65219)]
    assert dC == [F(44, 49), F(64, 147), F(1024, 4851), F(16384, 160083)]


def test_t1_potencias_21_pasos():
    for mu0 in ((1, 0), (0, 1)):
        mu, pasos = m.iteracion_potencias(m.T1_P, mu0, 1e-6)
        assert pasos == 21
        assert abs(mu[0] - 22 / 49) < 1e-6


def test_t1_fraccion_del_tiempo():
    assert m.SEMILLAS["c2-fraccion-frase"] == 2042
    assert round(m.fraccion_frase(), 4) == 0.4494


# ------------------------------------------------------------ T2 a T5 ---

def test_t2_alternante():
    assert m.estacionaria(m.T2_P) == [F(1, 2), F(1, 2)]
    assert m.clases(m.T2_P) == [{"estados": (0, 1), "cerrada": True, "periodo": 2}]
    mu, pasos = m.iteracion_potencias(m.T2_P, (1, 0))
    assert pasos is None
    assert m.distancias_t(m.T2_P, (F(1), F(0)), 10) == [F(1)] * 11


def test_t3_identidad_no_tiene_estacionaria_unica():
    assert [c["cerrada"] for c in m.clases(m.T3_P)] == [True, True]
    with pytest.raises(ValueError):
        m.estacionaria(m.T3_P)


def test_t4_clases_y_replicas():
    cl = m.clases(m.T4_P)
    assert [(c["estados"], c["cerrada"]) for c in cl] == [((0,), False), ((1,), True),
                                                         ((2,), True)]
    assert m.SEMILLAS["c2-replicas-t4"] == 2039
    assert [round(x, 3) for x in m.fracciones_t4()] == [0.0, 0.998, 0.0, 0.0, 0.998]


def test_t5_tres_clases():
    assert m.clases(m.T5_P) == [
        {"estados": (0,), "cerrada": False, "periodo": None},
        {"estados": (1, 2), "cerrada": True, "periodo": 2},
        {"estados": (3, 4), "cerrada": True, "periodo": 1},
    ]


# ------------------------------------------------------------------ T6 ---

def test_t6_estacionaria_del_quijote():
    mu = m.estacionaria(m.matriz_corpus())
    assert mu == [F(752551, 1620531), F(867980, 1620531)]
    assert f"{float(mu[0]):.3f}" == "0.464"


def test_t6_potencias_24_pasos():
    for mu0 in ((1, 0), (0, 1)):
        assert m.iteracion_potencias(m.matriz_corpus(), mu0, 1e-6)[1] == 24


def test_t6_contraccion():
    assert f"{float(m.segundo_valor_propio_2x2(m.matriz_corpus())):.3f}" == "-0.530"


def test_t6_fraccion_del_tiempo():
    assert m.SEMILLAS["c2-fraccion-quijote"] == 2037
    assert m.T_LARGO == 100_000
    assert m.fraccion_quijote() == 0.46434


# ------------------------------------------------------------------ T7 ---

def test_t7_estados_y_matriz():
    estados, P = m.tablero_desde(m.TABLERO_CHICO)
    assert estados == [0, 1, 4, 5]
    h = F(1, 2)
    assert P == [[0, h, h, 0], [0, h, h, 0], [0, 0, 0, 1], [0, 0, 0, 1]]


def test_t7_tiempo_medio():
    assert m.absorcion_tablero("chico") == {0: 3, 1: 3, 4: 1, 5: 0}


def test_t7_simulado():
    media, ee = m.partidas_chico()
    assert (round(media, 4), round(ee, 4)) == (3.0048, 0.0143)


# ------------------------------------------------------------------ T8 ---

def test_t8_tablero_bien_formado():
    saltos = m.TABLERO_100["saltos"]
    escaleras = [a for a, b in saltos.items() if b > a]
    serpientes = [a for a, b in saltos.items() if b < a]
    assert len(escaleras) == 8 and len(serpientes) == 8
    assert not set(saltos.values()) & set(saltos)
    assert 0 not in saltos and 100 not in saltos and 100 not in saltos.values()
    assert len(m.tablero_desde(m.TABLERO_100)[0]) == 85


def test_t8_tiempo_medio_exacto():
    m0 = m.absorcion_tablero("100")[0]
    assert m0 == F(39910799912908713627664662413307147744708895001971120792615379,
                   716948303291860608185402165157896874585212542027068980246952)
    assert f"{float(m0):.3f}" == "55.668"


def test_t8_simulado():
    assert m.SEMILLAS["c2-partidas-100"] == 2038
    media, ee = m.partidas_100()
    assert (f"{media:.3f}", f"{ee:.3f}") == ("56.008", "0.428")
    assert abs(media - 55.668) < 2 * ee


# ------------------------------------------------------------------ T9 ---

def test_t9_matriz_google():
    G = m.matriz_google(m.T9_ENLACES)
    a, b, c, q = F(3, 80), F(37, 80), F(71, 80), F(1, 4)
    assert G == [[a, b, b, a], [a, a, c, a], [b, a, a, b], [q, q, q, q]]


def test_t9_pagerank_exacto_y_pasos():
    assert m.pagerank_exacto(m.T9_ENLACES) == [F(1429, 6107), F(1140, 6107),
                                               F(2109, 6107), F(1429, 6107)]
    nodos, mu, pasos = m.pagerank(m.T9_ENLACES)
    assert pasos == 28
    assert max(abs(x - float(y)) for x, y in
               zip(mu, m.pagerank_exacto(m.T9_ENLACES))) < 1e-7


def test_t9_navegante():
    assert m.SEMILLAS["c2-navegante"] == 2040
    assert [f"{x:.3f}" for x in m.navegante()] == ["0.234", "0.185", "0.346", "0.235"]


# ----------------------------------------------------------------- T10 ---

def test_t10_la_foto_del_curso():
    c = m.pagerank_curso()
    assert (c["nodos"], c["enlaces"], c["sin_salidas"], c["pasos"]) == (134, 506, 5, 88)
    assert [(i, t, f"{v:.3f}") for i, t, v in c["top5"]] == [
        ("ia-y-sociedad", "IA y sociedad", "0.061"),
        ("imaginar-la-maquina", "Imaginar la máquina", "0.057"),
        ("todo-es-un-numero", "Todo es un número", "0.030"),
        ("problema-de-la-parada", "El problema de la parada", "0.028"),
        ("la-bitacora-del-taller", "La bitácora del taller", "0.025"),
    ]


def test_semillas_nuevas_no_chocan():
    assert len(set(m.SEMILLAS.values())) == len(m.SEMILLAS)
