"""Fija cada cifra de la clase 3 de Markov (course/8_markov/3_decidir/,
«Decidir», MDP) contra su funcion de tools/markov.py, con el valor escrito a
mano.

La tabla de cifras ya formateadas que usan las paginas es
.superpowers/unidad/markov/clase-3/cifras.md (local). Las pruebas de la
ultima seccion buscan cada cifra en el texto de su pagina; mientras la pagina
sea un esqueleto (contiene «Esqueleto:» o un hueco ⟦…⟧) se omiten, porque
las paginas se escriben en paralelo.

Una correccion al plan v4 (§3): en J2, iteracion de valores desde 0, el error
max|V* - V^(t)| es IGUAL al residuo desde la ronda 2 (los dos 2^(2-t)); en la
ronda 1 el error es 2 y el residuo 3. El «2 × residuo» del plan compara el
error de la ronda t-1 con el residuo de la ronda t.
"""
import re
from fractions import Fraction as F
from pathlib import Path

import pytest

import markov as m

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/8_markov/3_decidir"

CC, CR, RC, RR = "caminar–caminar", "caminar–correr", "correr–caminar", "correr–correr"
VSTAR = {1: F(-5), 2: F(-2)}


def _pol(nombre):
    return m.POLITICAS_J2[nombre]


# ---------------------------------------------------------- J1 escalera ---

def test_escalera_costos():
    assert m.ESCALERA_COSTOS == (1, 2, 9, 1, 1)


def test_escalera_rutas_ocho():
    assert m.escalera_rutas() == [8, 5, 3, 2, 1, 1]
    assert len(m.escalera_todas_las_rutas()) == 8


def test_escalera_costo_que_falta():
    assert m.escalera_costo() == [4, 4, 2, 1, 1, 0]


def test_escalera_optima_unica():
    assert m.escalera_ruta_optima() == [0, 2, 4, 5]
    assert m.costo_ruta([0, 2, 4, 5]) == 4
    costos = sorted(m.costo_ruta(r) for r in m.escalera_todas_las_rutas())
    assert costos[0] == 4 and costos[1] > 4
    assert m.escalera_es_unica()


def test_escalera_codiciosa_falla():
    ruta = m.escalera_codiciosa()
    assert ruta == [0, 1, 2, 4, 5]
    assert m.costo_ruta(ruta) == 5


# ------------------------------------------------------------- J2 MDP ---

def test_j2_matrices_y_recompensas():
    j = m.pasillo()
    h = F(1, 2)
    assert j["estados"] == [1, 2]
    assert m.matriz_accion(j, m.CAMINAR) == [[0, 1, 0], [0, 0, 1]]
    assert m.matriz_accion(j, m.CORRER) == [[h, h, 0], [0, h, h]]
    assert j["r"] == {(1, "caminar"): -3, (1, "correr"): -6,
                      (2, "caminar"): -3, (2, "correr"): -1}
    for (s, a), fila in j["P"].items():
        assert sum(fila.values()) == 1
        esperado = sum(p * j["r_real"][(s, a, t)] for t, p in fila.items())
        assert esperado == j["r"][(s, a)]


def test_j2_orden_de_politicas():
    assert list(m.POLITICAS_J2) == [CC, CR, RC, RR]


@pytest.mark.parametrize("nombre,valor", [(CC, (-6, -3)), (CR, (-5, -2)),
                                          (RC, (-15, -3)), (RR, (-14, -2))])
def test_j2_los_cuatro_valores(nombre, valor):
    V = m.evaluar_politica(m.pasillo(), _pol(nombre))
    assert (V[1], V[2]) == valor


def test_j2_caminar_correr_es_la_optima():
    vals = {n: m.evaluar_politica(m.pasillo(), p) for n, p in m.POLITICAS_J2.items()}
    for n, V in vals.items():
        assert V[1] <= VSTAR[1] and V[2] <= VSTAR[2]
    assert vals[CR] == VSTAR
    assert m.cumple_bellman(m.pasillo(), VSTAR)
    assert m.codiciosa(m.pasillo(), VSTAR) == _pol(CR)


def _optima(caminar, castigo):
    return m.iterar_politicas(m.pasillo(caminar=caminar, castigo=castigo), _pol(CC))[-1]


@pytest.mark.parametrize("w", [F(1), F(5, 2), F(3), F(4), F(7)])
@pytest.mark.parametrize("x", [F(0), F(1, 2), F(3, 2), F(3), F(10)])
def test_j2_fronteras(w, x):
    """Correr en 1 si castigo < caminar - 2; correr en 2 si caminar > 2."""
    if x == w - 2 or w == 2:
        pytest.skip("empate en la frontera")
    pol = _optima(w, x)
    assert pol[2] == (m.CORRER if w > 2 else m.CAMINAR)
    assert pol[1] == (m.CORRER if x < w - 2 else m.CAMINAR)


def test_j2_con_caminar_3_correr_en_1_solo_si_castigo_menor_que_1():
    assert _optima(3, F(99, 100))[1] == m.CORRER
    assert _optima(3, F(101, 100))[1] == m.CAMINAR
    V = {s: max(m.evaluar_politica(m.pasillo(castigo=1), p)[s]
                for p in m.POLITICAS_J2.values()) for s in (1, 2)}
    assert m.q_valor(m.pasillo(castigo=1), V, 1, m.CAMINAR) == \
        m.q_valor(m.pasillo(castigo=1), V, 1, m.CORRER)


# ------------------------------------------------- iteracion de valores ---

def test_j2_traza_de_iteracion_de_valores():
    traza = m.iterar_valores(m.pasillo(), rondas=6)
    assert [(V[1], V[2]) for V in traza] == [
        (0, 0), (-3, -1), (-4, F(-3, 2)), (F(-9, 2), F(-7, 4)),
        (F(-19, 4), F(-15, 8)), (F(-39, 8), F(-31, 16)), (F(-79, 16), F(-63, 32))]


def test_j2_formulas_cerradas():
    traza = m.iterar_valores(m.pasillo(), rondas=30)
    for t, V in enumerate(traza):
        assert V[2] == -2 + F(2) ** (1 - t)
        assert V[1] == (0 if t == 0 else -5 + F(2) ** (2 - t))
        assert V[1] != -5 and V[2] != -2          # nunca llega en rondas finitas


def test_j2_error_igual_a_residuo_desde_la_ronda_2():
    traza = m.iterar_valores(m.pasillo(), rondas=30)
    res = m.residuos(traza)
    err = m.errores(traza, VSTAR)
    assert (res[0], err[1]) == (3, 2)             # ronda 1: residuo 3, error 2
    for t in range(2, 31):
        assert res[t - 1] == err[t] == F(2) ** (2 - t)
        assert err[t - 1] == 2 * res[t - 1]       # el «2 ×» del plan: ronda anterior


def test_j2_desde_cero_baja_monotona():
    traza = m.iterar_valores(m.pasillo(), rondas=20)
    for a, b in zip(traza, traza[1:]):
        assert all(b[s] <= a[s] for s in a)
        assert all(b[s] >= VSTAR[s] for s in a)


def test_cota_de_paro_en_j2():
    j = m.pasillo()
    assert m.prob_no_terminar(j, 1) == 1
    assert m.prob_no_terminar(j, 2) == F(3, 4)
    assert m.prob_no_terminar(j, 3) == F(1, 2)
    assert m.cota_paro(3, F(1, 2)) == 6
    assert m.cota_paro(2, F(3, 4)) == 8
    traza = m.iterar_valores(j, rondas=30)
    res, err = m.residuos(traza), m.errores(traza, VSTAR)
    for t in range(1, 31):
        assert err[t] <= 6 * res[t - 1]


def test_lazo_99_error_99_por_residuo():
    L = m.lazo_99()
    assert m.evaluar_politica(L, {1: m.CAMINAR}) == {1: -100}
    traza = m.iterar_valores(L, rondas=40)
    res, err = m.residuos(traza), m.errores(traza, {1: F(-100)})
    for t in range(1, 41):
        assert res[t - 1] == F(99, 100) ** (t - 1)
        assert err[t] == 99 * res[t - 1]
    assert m.prob_no_terminar(L, 1) == F(99, 100)
    assert m.cota_paro(1, F(99, 100)) == 100


def test_codiciosa_de_u_equivocado():
    j = m.pasillo()
    U = {1: F(-8), 2: F(-8)}
    assert (m.q_valor(j, U, 1, m.CAMINAR), m.q_valor(j, U, 1, m.CORRER)) == (-11, -14)
    assert (m.q_valor(j, U, 2, m.CAMINAR), m.q_valor(j, U, 2, m.CORRER)) == (-3, -5)
    assert m.codiciosa(j, U) == _pol(CC) != _pol(CR)


# ---------------------------------------------------------- esperar ---

def test_esperar_gratis():
    j = m.pasillo(esperar=0)
    quieto = {1: m.ESPERAR, 2: m.ESPERAR}
    with pytest.raises(ValueError):                # I - P_{pi,T} = 0, singular
        m.evaluar_politica(j, quieto)
    # esperar siempre vale 0 > -5: V* = (0, 0); iterar desde 0 se queda ahi
    assert m.iterar_valores(j, rondas=10)[-1] == {1: 0, 2: 0}
    for V in ({1: 0, 2: 0}, {1: -5, 2: -2}, {1: -1, 2: -1}):
        assert m.cumple_bellman(j, V)
    assert not m.cumple_bellman(j, {1: -6, 2: -2})     # V(1) < V(2) - 3
    assert not m.cumple_bellman(j, {1: -5, 2: F(-21, 10)})  # V(2) < -2


def test_esperar_gratis_soluciones_de_bellman_son_la_region():
    j = m.pasillo(esperar=0)
    for v2 in (F(-3), F(-2), F(-1), F(0), F(5, 2)):
        for v1 in (v2 - 4, v2 - 3, v2 - 1, v2 + 2):
            assert m.cumple_bellman(j, {1: v1, 2: v2}) == (v2 >= -2 and v1 >= v2 - 3)


def test_esperar_gratis_el_pl_sigue_dando_menos_cinco_menos_dos():
    V, res = m.programa_lineal(m.pasillo(esperar=0))
    assert res.status == 0
    assert abs(V[1] + 5) < 1e-7 and abs(V[2] + 2) < 1e-7


def test_esperar_con_costo_1_todo_como_antes():
    j = m.pasillo(esperar=1)
    with pytest.raises(ValueError):
        m.evaluar_politica(j, {1: m.ESPERAR, 2: m.ESPERAR})
    traza = m.iterar_valores(j, rondas=60)
    assert max(abs(traza[-1][s] - VSTAR[s]) for s in VSTAR) < F(1, 10**15)
    # las primeras rondas si cambian (esperar -1 gana con pocos pasos); el limite no
    assert m.cumple_bellman(j, VSTAR)
    assert not m.cumple_bellman(j, {1: 0, 2: 0})
    assert m.codiciosa(j, VSTAR) == _pol(CR)
    assert m.iterar_politicas(j, _pol(CC))[-1] == _pol(CR)
    V, _ = m.programa_lineal(j)
    assert abs(V[1] + 5) < 1e-7 and abs(V[2] + 2) < 1e-7


# ------------------------------------------------ iteracion de politicas ---

@pytest.mark.parametrize("inicio", [CC, RR])
def test_iteracion_de_politicas_una_mejora(inicio):
    pols = m.iterar_politicas(m.pasillo(), _pol(inicio))
    assert pols == [_pol(inicio), _pol(CR)]


def test_empates_conservar_termina_cambiar_alterna():
    # Caminar cuesta 2 solo en la casilla 2, como en 7_iterar_politicas.
    j = m.pasillo_empate()
    for p in (CC, CR):
        V = m.evaluar_politica(j, _pol(p))
        assert V == {1: -5, 2: -2}
        assert m.q_valor(j, V, 2, m.CAMINAR) == m.q_valor(j, V, 2, m.CORRER) == -2
    assert m.iterar_politicas(j, _pol(CC), empate="conservar") == [_pol(CC)]
    alt = m.iterar_politicas(j, _pol(CC), empate="cambiar", max_rondas=10)
    assert len(alt) == 11
    assert alt == [_pol(CC), _pol(CR)] * 5 + [_pol(CC)]


# --------------------------------------------------------- programa lineal ---

def test_programa_lineal_da_v_estrella():
    V, res = m.programa_lineal(m.pasillo())
    assert res.status == 0
    assert abs(V[1] + 5) < 1e-7 and abs(V[2] + 2) < 1e-7
    assert abs(res.fun + 7) < 1e-7


# ------------------------------------------------------------- volados ---

def test_volados():
    t = F(1, 3)
    assert m.volados(t) == {"audaz": (F(1, 9), F(1, 3), F(5, 9)),
                            "tímida": (F(1, 15), F(1, 5), F(7, 15))}
    v = m.volados(F(2, 3))
    assert v == {"audaz": (F(4, 9), F(2, 3), F(8, 9)),
                 "tímida": (F(8, 15), F(4, 5), F(14, 15))}
    assert all(a < b for a, b in zip(v["audaz"], v["tímida"]))
    assert m.volados(F(1, 2)) == {"audaz": (F(1, 4), F(1, 2), F(3, 4)),
                                  "tímida": (F(1, 4), F(1, 2), F(3, 4))}


# ------------------------------------------------------------- PASILLO ---

def test_pasillo_largo():
    d = m.pasillo_largo()
    assert d["v_inicio"] == -467
    assert d["rondas_vi"] == 451
    # Una mejora; la pagina cuenta 2 rondas: la que mejora y la que confirma.
    assert d["rondas_pi"] == 1
    assert d["politicas"] == 2 ** 200
    assert f"{float(d['politicas']):.3e}" == "1.607e+60"
    assert d["error_vi"] < 1e-8
    assert all(a == (m.CAMINAR if s % 3 == 1 else m.CORRER) for s, a in d["politica"].items())


def test_pasillo_caminar_siempre_vale_600():
    mdp = m.pasillo(n=200)
    assert m.evaluar_politica(mdp, {s: m.CAMINAR for s in mdp["estados"]})[1] == -600


# ---------------------------------------------------------- simulacion ---

def test_simulacion():
    assert m.SEMILLAS["c3-simular-politica"] == 2044
    g = m.simular_politica(m.pasillo(), _pol(CR))
    assert len(g) == 10_000 and max(g) == -4 and min(g) == -15
    media, ee = m.resumen_simulacion()
    assert (f"{media:.4f}", f"{ee:.4f}") == ("-5.0074", "0.0143")
    assert abs(media + 5) < 2 * ee


def test_semillas_no_chocan():
    assert len(set(m.SEMILLAS.values())) == len(m.SEMILLAS)


# ------------------------------------------------ cifras en las paginas ---
# (texto tras _limpio, pagina). Se busca en toda la pagina: los encabezados
# aun no existen. Formato: cifras.md.

P2, P3, P4 = "2_de_contar_a_decidir.md", "3_el_mdp.md", "4_evaluar_una_politica.md"
P5, P6, P7 = "5_bellman.md", "6_iterar_valores.md", "7_iterar_politicas.md"
P8, P9 = "8_como_programa_lineal.md", "9_resumen.md"

CIFRAS_EN_PAGINAS = [
    ("8", P2), ("9", P2), ("4", P2), ("5", P2),
    ("-6", P3), ("-3", P3), ("-1", P3),
    ("-5", P4), ("-2", P4), ("-15", P4), ("-14", P4), ("-5.0074", P4), ("0.0143", P4),
    ("10 000", P4), ("2044", P4),
    ("-11", P5), ("-14", P5), ("-8", P5), ("1/9", P5), ("5/9", P5), ("1/15", P5),
    ("7/15", P5),
    ("-79/16", P6), ("-63/32", P6), ("99", P6), ("6", P6), ("-467", P6), ("451", P6),
    ("-467", P7), ("451", P7), ("-600", P7),
    ("-5", P8), ("-2", P8),
]


def _limpio(s):
    s = s.replace("\u2212", "-").replace("\u2060", "")
    s = re.sub(r"\\[td]?frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
    for fino in ("\u202f", "\u2009", "\u00a0", "\\,", "\\;", "\\ ", "~"):
        s = s.replace(fino, " ")
    s = re.sub(r"\\(?:text|textbf|mathrm|mathbf)\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\times", "×").replace("**", "").replace("$", "").replace("`", "")
    return re.sub(r"\s+", " ", s)


def _esta(cifra, texto):
    return re.search(r"(?<![\d./])" + re.escape(cifra) + r"(?![\d/]|\.\d)", texto) is not None


def _es_esqueleto(nombre):
    ruta = CLASE / nombre
    if not ruta.is_file():
        return True
    texto = ruta.read_text(encoding="utf-8")
    return "Esqueleto:" in texto or "⟦" in texto


@pytest.mark.parametrize("pagina", sorted({p for _, p in CIFRAS_EN_PAGINAS}))
def test_cifras_en_su_pagina(pagina):
    if _es_esqueleto(pagina):
        pytest.skip(f"{pagina} aun es esqueleto o tiene huecos ⟦…⟧")
    texto = _limpio((CLASE / pagina).read_text(encoding="utf-8"))
    faltan = [c for c, p in CIFRAS_EN_PAGINAS if p == pagina and not _esta(c, texto)]
    assert not faltan, f"{pagina}: faltan {faltan}"


def test_el_limpiador_lee_los_formatos():
    assert _esta("-79/16", _limpio(r"$-\frac{79}{16}$"))
    assert _esta("-467", _limpio("$\u2212467$"))
    assert _esta("10 000", _limpio(r"$10\,000$"))
    assert not _esta("-5", _limpio("-5.0074")) and _esta("-5.0074", _limpio("-5.0074"))
