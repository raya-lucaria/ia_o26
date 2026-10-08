"""Los bloques de Python de la unidad de juegos corren y dan los numeros.

Cada pagina de course/7_juegos/ que trae pseudocodigo trae debajo el mismo
algoritmo en Python. Aqui se extrae cada bloque ```python de la pagina, se
ejecuta con las reglas de hexapawn de juegos.py conectadas como funciones
(es_final, pl, acciones, transicion, utilidad, pr, evaluar) y se compara lo
que devuelve con los numeros que cita la prosa y que juegos.py recalcula.

Si alguien rompe un bloque de Python de una pagina, esta prueba falla.
`transicion` cuenta sus llamadas: cada llamada genera un nodo, asi que
nodos generados = llamadas + 1 (la raiz).
"""
import re
from fractions import Fraction as F
from pathlib import Path

import pytest

import juegos as j

UNIDAD = Path(__file__).resolve().parent.parent / "course/7_juegos"
CLASE_2 = UNIDAD / "2_mirar_todo_y_podar"
CLASE_3 = UNIDAD / "3_cuando_no_cabe"

SUBARBOL = ".BBBN.N.N"                         # n1, mueven Blancas
HORIZONTE = "B..." + "..BB" + "..N." + "NN.."  # la posicion de la clase 3

PAGINAS = {
    CLASE_2 / "2_minimax_como_algoritmo.md": ["minimax", "decidir_minimax"],
    CLASE_2 / "3_cuando_decide_un_dado.md": [
        "expectiminimax", "decidir_expectiminimax"],
    CLASE_2 / "5_alfa_beta_como_algoritmo.md": [
        "alfa_beta", "decidir_alfa_beta"],
    CLASE_3 / "2_minimax_con_corte.md": [
        "minimax_con_corte", "decidir_con_corte"],
    CLASE_3 / "3_jugar_contra_el_reloj.md": [
        "alfa_beta_con_corte", "profundizacion_iterativa"],
}


def bloques_python(pagina):
    texto = pagina.read_text(encoding="utf-8")
    return re.findall(r"^```python\n(.*?)^```$", texto, re.S | re.M)


def bloques_pseudocodigo(pagina):
    texto = pagina.read_text(encoding="utf-8")
    return re.findall(r"^```text\n(.*?)^```$", texto, re.S | re.M)


def reglas(n=3, azar=False, invertir=False, queda_tiempo=None):
    """Hexapawn como funciones. El estado es (tablero, turno)."""
    contador = {"T": 0}

    def es_final(s):
        return j.ganador(s[0], s[1], n) is not None

    def pl(s):
        if s[1] == "B":
            return "MAX"
        return "AZAR" if azar else "MIN"

    def acciones(s):
        lista = j.jugadas(s[0], s[1], n)
        return lista[::-1] if invertir else lista

    def transicion(s, a):
        contador["T"] += 1
        return (j.mover(s[0], a), j.otro(s[1]))

    def utilidad(s):
        return j.utilidad_simple(j.ganador(s[0], s[1], n), 0)

    def pr(s, a):
        return F(1, len(acciones(s)))

    def evaluar(s):
        return j.evaluar_peones(s[0], n)

    ns = dict(es_final=es_final, pl=pl, acciones=acciones,
              transicion=transicion, utilidad=utilidad, pr=pr,
              evaluar=evaluar, queda_tiempo=queda_tiempo or (lambda: True))
    return ns, contador


def cargar(pagina, **kw):
    ns, contador = reglas(**kw)
    for codigo in bloques_python(pagina):
        exec(compile(codigo, str(pagina), "exec"), ns)
    return ns, contador


def jugada(tablero, nombre, turno="B", n=3):
    return {j.nombre_jugada(tablero, m, n): m
            for m in j.jugadas(tablero, turno, n)}[nombre]


@pytest.mark.parametrize("pagina", sorted(PAGINAS), ids=lambda p: p.name)
def test_cada_pseudocodigo_trae_su_python_y_define_lo_que_dice(pagina):
    pseudo, python = bloques_pseudocodigo(pagina), bloques_python(pagina)
    assert pseudo, pagina.name
    assert len(python) == len(pseudo), pagina.name
    ns, _ = cargar(pagina)
    for nombre in PAGINAS[pagina]:
        assert callable(ns.get(nombre)), (pagina.name, nombre)


@pytest.mark.parametrize("pagina", sorted(PAGINAS), ids=lambda p: p.name)
def test_los_bloques_caben_en_un_telefono(pagina):
    """Ninguna linea de codigo pasa de 64 caracteres en los Python nuevos."""
    for codigo in bloques_python(pagina):
        for linea in codigo.splitlines():
            assert len(linea) <= 64, (pagina.name, linea)


def test_minimax_en_python():
    pagina = CLASE_2 / "2_minimax_como_algoritmo.md"
    ns, c = cargar(pagina)
    # V(n1) = +1 y genera los 13 nodos de n1.
    assert ns["minimax"]((SUBARBOL, "B")) == 1
    assert c["T"] + 1 == 13 == j.contar_arbol(SUBARBOL)[0]
    # El juego completo vale -1 y genera los 252 nodos del arbol.
    c["T"] = 0
    assert ns["minimax"]((j.inicio(), "B")) == -1 == j.valor(j.inicio(), "B")
    assert c["T"] + 1 == 252
    # Los hijos de n1: c1-c2 vale +1 y c1xb2 vale -1.
    hijos = {j.nombre_jugada(SUBARBOL, m):
             ns["minimax"]((j.mover(SUBARBOL, m), "N"))
             for m in j.jugadas(SUBARBOL, "B")}
    assert hijos["c1-c2"] == 1 and hijos["c1xb2"] == -1
    # DECIDIR-MINIMAX(n1) devuelve c1-c2.
    assert ns["decidir_minimax"]((SUBARBOL, "B")) == jugada(SUBARBOL, "c1-c2")


def test_expectiminimax_en_python():
    pagina = CLASE_2 / "3_cuando_decide_un_dado.md"
    ns, _ = cargar(pagina, azar=True)
    e = ns["expectiminimax"]
    n3 = j.mover(SUBARBOL, jugada(SUBARBOL, "c1xb2"))
    assert e((n3, "N")) == F(1, 3)
    aperturas = {j.nombre_jugada(j.inicio(), m): e((j.mover(j.inicio(), m), "N"))
                 for m in j.jugadas(j.inicio(), "B")}
    assert aperturas == {"a1-a2": F(5, 9), "b1-b2": F(3, 4), "c1-c2": F(5, 9)}
    for t, turno in [(SUBARBOL, "B"), (j.inicio(), "B")]:
        assert e((t, turno)) == j.expectiminimax_rival_al_azar(t, turno)
    # DECIDIR con Negras al azar abre con b1-b2, la de 3/4.
    a = ns["decidir_expectiminimax"]((j.inicio(), "B"))
    assert j.nombre_jugada(j.inicio(), a) == "b1-b2"
    # Sin azar (Negras como MIN), las tres aperturas valen -1, como minimax.
    ns, _ = cargar(pagina)
    assert [ns["expectiminimax"]((j.mover(j.inicio(), m), "N"))
            for m in j.jugadas(j.inicio(), "B")] == [-1, -1, -1]


@pytest.mark.parametrize("tablero, invertir, valor, nodos", [
    (SUBARBOL, False, 1, 5),
    (SUBARBOL, True, 1, 8),
    (j.inicio(), False, -1, 82),
    (j.inicio(), True, -1, 72),
])
def test_alfa_beta_en_python(tablero, invertir, valor, nodos):
    pagina = CLASE_2 / "5_alfa_beta_como_algoritmo.md"
    ns, c = cargar(pagina, invertir=invertir)
    inf = float("inf")
    assert ns["alfa_beta"]((tablero, "B"), -inf, inf) == valor
    assert c["T"] + 1 == nodos
    assert (valor, nodos) == j.alfa_beta(tablero, "B", invertir=invertir)[:2]


@pytest.mark.parametrize("tablero, invertir, entrega, nodos", [
    (SUBARBOL, False, "c1-c2", 5),
    (SUBARBOL, True, "c1-c2", 8),
    (j.inicio(), False, "a1-a2", 82),
    (j.inicio(), True, "c1-c2", 72),
])
def test_decidir_alfa_beta_en_python(tablero, invertir, entrega, nodos):
    """DECIDIR-ALFA-BETA genera lo mismo que ALFA-BETA en la raiz y, en n1,
    entrega c1-c2 en los dos ordenes."""
    pagina = CLASE_2 / "5_alfa_beta_como_algoritmo.md"
    ns, c = cargar(pagina, invertir=invertir)
    a = ns["decidir_alfa_beta"]((tablero, "B"))
    assert j.nombre_jugada(tablero, a) == entrega
    assert c["T"] + 1 == nodos


def test_en_la_raiz_una_cota_que_empata_no_gana():
    """La regla del empate: en orden fijo, c1xb2 devuelve +1 (una cota) y su
    valor exacto es -1. Con >= en la linea 5, DECIDIR elegiria c1xb2."""
    pagina = CLASE_2 / "5_alfa_beta_como_algoritmo.md"
    ns, _ = cargar(pagina)
    n3 = (j.mover(SUBARBOL, jugada(SUBARBOL, "c1xb2")), "N")
    assert ns["alfa_beta"](n3, 1, float("inf")) == 1
    assert j.valor(n3[0], "N") == -1
    codigo = bloques_python(pagina)[0]
    assert codigo.count("if w > alfa:") == 1
    ns, _ = reglas()
    exec(codigo.replace("if w > alfa:", "if w >= alfa:"), ns)
    a = ns["decidir_alfa_beta"]((SUBARBOL, "B"))
    assert j.nombre_jugada(SUBARBOL, a) == "c1xb2"


def test_sin_el_igual_se_pierde_casi_toda_la_poda():
    """El ejercicio «Decide si importa el igual»: con < y > estrictos en las
    lineas 14 y 22, n1 genera los 13 y el juego completo 228 y 171."""
    pagina = CLASE_2 / "5_alfa_beta_como_algoritmo.md"
    codigo = bloques_python(pagina)[0]
    assert "if v >= beta:" in codigo and "if v <= alfa:" in codigo
    estricto = codigo.replace("if v >= beta:", "if v > beta:").replace(
        "if v <= alfa:", "if v < alfa:")
    inf = float("inf")
    for tablero, invertir, nodos in [(SUBARBOL, False, 13),
                                     (j.inicio(), False, 228),
                                     (j.inicio(), True, 171)]:
        ns, c = reglas(invertir=invertir)
        exec(estricto, ns)
        v = ns["alfa_beta"]((tablero, "B"), -inf, inf)
        assert v == j.valor(tablero, "B")
        assert c["T"] + 1 == nodos == j.alfa_beta(
            tablero, "B", invertir=invertir, estricto=True)[1]


def test_alfa_beta_en_python_con_ventana_estrecha():
    """Con alfa = -1 y beta = +1, como en «Para profundizar»."""
    pagina = CLASE_2 / "5_alfa_beta_como_algoritmo.md"
    for tablero, invertir in [(SUBARBOL, False), (j.inicio(), False),
                              (j.inicio(), True)]:
        ns, c = cargar(pagina, invertir=invertir)
        v = ns["alfa_beta"]((tablero, "B"), -1, 1)
        assert (v, c["T"] + 1) == j.alfa_beta(
            tablero, "B", invertir=invertir, alfa=-1, beta=1)[:2]


def test_minimax_con_corte_en_python():
    pagina = CLASE_3 / "2_minimax_con_corte.md"
    ns, c = cargar(pagina, n=4)
    m = ns["minimax_con_corte"]
    # Valor de cada jugada de la raiz con d = 3: -9, 100 y 1.
    assert [m((j.mover(HORIZONTE, a), "N"), 2)
            for a in j.jugadas(HORIZONTE, "B", 4)] == [-9, 100, 1]
    for d in range(4):
        for a in j.jugadas(HORIZONTE, "B", 4):
            t = j.mover(HORIZONTE, a)
            assert m((t, "N"), d) == j.minimax_limitado(t, "N", d, 4)
    # Nodos generados con d = 1, 2 y 3 en la raiz: 4, 12 y 33.
    nodos = []
    for d in (1, 2, 3):
        c["T"] = 0
        m((HORIZONTE, "B"), d)
        nodos.append(c["T"] + 1)
    assert nodos == [4, 12, 33]
    # DECIDIR-CON-CORTE juega d2xc3, d2-d3 y d2-d3, con los mismos nodos.
    jugadas_d, nodos = [], []
    for d in (1, 2, 3):
        c["T"] = 0
        a = ns["decidir_con_corte"]((HORIZONTE, "B"), d)
        jugadas_d.append(j.nombre_jugada(HORIZONTE, a, 4))
        nodos.append(c["T"] + 1)
    assert jugadas_d == ["d2xc3", "d2-d3", "d2-d3"]
    assert nodos == [4, 12, 33]
    # El ejercicio: tras d2xc3 y b4xc3 la linea 9 da EVAL = 0; tras d2-d3,
    # a4-a3 y d3-d4 la linea 8 da 100.
    t = j.mover(HORIZONTE, jugada(HORIZONTE, "d2xc3", n=4))
    t = j.mover(t, jugada(t, "b4xc3", "N", 4))
    assert m((t, "B"), 0) == 0
    t = j.mover(HORIZONTE, jugada(HORIZONTE, "d2-d3", n=4))
    t = j.mover(t, jugada(t, "a4-a3", "N", 4))
    t = j.mover(t, jugada(t, "d3-d4", n=4))
    assert m((t, "N"), 0) == 100


def reloj(presupuesto, contador):
    """Hay tiempo mientras las llamadas a transicion no pasen del presupuesto."""
    return lambda: contador["T"] <= presupuesto


@pytest.mark.parametrize("presupuesto, entrega", [
    (2, "a1-a2"),     # d = 1 no termina: la jugada de la linea 2
    (3, "d2xc3"),     # d = 1 cabe justa (4 nodos); d = 2 queda a medias
    (11, "d2xc3"),    # a d = 2 le falta un nodo
    (12, "d2-d3"),    # d = 2 cabe justa (10 nodos)
    (10 ** 5, "d2-d3"),  # sale en la linea 9 mucho antes de agotarlo
])
def test_profundizacion_iterativa_en_python(presupuesto, entrega):
    pagina = CLASE_3 / "3_jugar_contra_el_reloj.md"
    ns, c = cargar(pagina, n=4)
    ns["queda_tiempo"] = reloj(presupuesto, c)
    a = ns["profundizacion_iterativa"]((HORIZONTE, "B"))
    assert j.nombre_jugada(HORIZONTE, a, 4) == entrega


def test_profundizacion_iterativa_en_python_genera_4_10_y_9():
    pagina = CLASE_3 / "3_jugar_contra_el_reloj.md"
    ns, c = cargar(pagina, n=4)
    # Un reloj holgado: si la linea 9 se rompe, la prueba falla en vez de
    # profundizar para siempre.
    ns["queda_tiempo"] = reloj(10 ** 5, c)
    a = ns["profundizacion_iterativa"]((HORIZONTE, "B"))
    # Con tiempo de sobra sale en la linea 9 con d = 3: 3 + 9 + 8 llamadas a T.
    assert j.nombre_jugada(HORIZONTE, a, 4) == "d2-d3"
    esperado = j.profundizacion_iterativa(HORIZONTE, (1, 2, 3), 4)
    assert [nodos for _, nodos, _ in esperado] == [4, 10, 9]
    assert c["T"] == sum(nodos - 1 for nodos in (4, 10, 9))


# El arbol T de la clase 2: raiz MAX con izq, centro y der. Un nodo es
# ("MAX" | "MIN", hijos); una hoja, un numero. Las jugadas son los indices.
ARBOL_T = ("MAX", [("MIN", [3, 6]),
                   ("MIN", [("MAX", [5, 2]), ("MAX", [7, 8])]),
                   ("MIN", [2, 12])])
NOMBRES_T = ["izq", "centro", "der"]


def _invertir(nodo):
    if isinstance(nodo, int):
        return nodo
    return (nodo[0], [_invertir(h) for h in nodo[1]][::-1])


def _reglas_arbol():
    contador = {"T": 0}

    def transicion(s, a):
        contador["T"] += 1
        return s[1][a]

    ns = dict(es_final=lambda s: isinstance(s, int),
              pl=lambda s: s[0],
              acciones=lambda s: range(len(s[1])),
              transicion=transicion,
              utilidad=lambda s: s)
    return ns, contador


@pytest.mark.parametrize("pagina, decidir, invertido, nodos", [
    (CLASE_2 / "2_minimax_como_algoritmo.md", "decidir_minimax", False, 14),
    (CLASE_2 / "2_minimax_como_algoritmo.md", "decidir_minimax", True, 14),
    (CLASE_2 / "5_alfa_beta_como_algoritmo.md", "decidir_alfa_beta",
     False, 12),
    (CLASE_2 / "5_alfa_beta_como_algoritmo.md", "decidir_alfa_beta",
     True, 14),
], ids=lambda x: str(x) if not isinstance(x, Path) else x.stem)
def test_decidir_en_el_arbol_t_juega_centro(pagina, decidir, invertido,
                                            nodos):
    """El ejemplo a mano de las dos paginas: en el orden dado minimax genera
    los 14 nodos y alfa-beta 12; al reves, los 14. Siempre juega centro."""
    arbol = _invertir(ARBOL_T) if invertido else ARBOL_T
    ns, contador = _reglas_arbol()
    exec(bloques_python(pagina)[0], ns)
    a = ns[decidir](arbol)
    nombres = NOMBRES_T[::-1] if invertido else NOMBRES_T
    assert nombres[a] == "centro"
    assert contador["T"] + 1 == nodos


def test_alfa_beta_en_el_arbol_t_devuelve_cotas():
    """C2 llega con (3, 5) y devuelve 7 aunque vale 8; D llega con
    (5, +inf) y devuelve 2."""
    ns, _ = _reglas_arbol()
    exec(bloques_python(CLASE_2 / "5_alfa_beta_como_algoritmo.md")[0], ns)
    c2 = ARBOL_T[1][1][1][1]
    assert ns["alfa_beta"](c2, 3, 5) == 7 and max(c2[1]) == 8
    assert ns["alfa_beta"](ARBOL_T[1][2], 5, float("inf")) == 2
