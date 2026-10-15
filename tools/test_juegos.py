"""Los numeros que citan las paginas de course/7_juegos/, recalculados.

Si una pagina cita un numero, aqui hay una asercion que lo recalcula con
tools/juegos.py. Cambiar una regla del juego sin actualizar la prosa hace
fallar esta suite.
"""
from fractions import Fraction as F

import pytest

import juegos as j

# El subarbol de la clase 2: tras a1-a2 y b3-b2, mueven Blancas.
SUBARBOL = ".BBBN.N.N"
# La posicion de octapawn de la clase 3 (fila 1 primero).
HORIZONTE = "B..." + "..BB" + "..N." + "NN.."
# La posicion de octapawn de la tarea de la clase 3.
HORIZONTE_TAREA = ".BB." + "B..B" + "..NN" + "NN.."


def test_clase_1_hexapawn():
    assert j.contar_arbol() == (252, 135)
    assert [j.nombre_jugada(j.inicio(), m) for m in j.jugadas(j.inicio(), "B")] == [
        "a1-a2", "b1-b2", "c1-c2"]
    assert j.partida_mas_larga() == 7
    # En 3x3 el turno se deduce del tablero; en 4x4 ya no.
    assert j.tableros_con_dos_turnos(3) == []
    assert j.tableros_con_dos_contadores(3) == []
    assert j.contar_estados() == {"B": 33, "N": 37, "final": 65,
                                  "final_sin_jugada": 8}
    assert len(j.tableros_con_dos_turnos(4)) == 2925


def test_clase_1_tarea():
    assert j.gato_conteos() == (255168, 549946, 5478)
    assert j.gato_turno_se_deduce()
    # Si quedarse sin jugada empata, el valor exacto pasa de -1 a 0.
    assert j.valor(j.inicio(), "B") == -1
    assert j.valor(j.inicio(), "B", sin_jugada_empata=True) == 0
    assert j.contar_arbol(sin_jugada_empata=True) == (252, 135)


def test_clase_3_no_cabe_y_horizonte():
    assert j.contar_arbol(n=4) == (4197973, 20286)
    assert j.valor(j.inicio(4), "B", n=4) == 1
    nombres = lambda t: [j.nombre_jugada(t, m, 4) for m in j.jugadas(t, "B", 4)]
    assert nombres(HORIZONTE) == ["a1-a2", "d2-d3", "d2xc3"]
    prof = lambda t, d: {j.nombre_jugada(t, m, 4):
                         j.minimax_limitado(j.mover(t, m), "N", d, 4)
                         for m in j.jugadas(t, "B", 4)}
    assert prof(HORIZONTE, 0) == {"a1-a2": 2, "d2-d3": 2, "d2xc3": 13}
    assert prof(HORIZONTE, 1) == {"a1-a2": -10, "d2-d3": 1, "d2xc3": 0}
    exacto = {j.nombre_jugada(HORIZONTE, m, 4): j.valor(j.mover(HORIZONTE, m), "N", n=4)
              for m in j.jugadas(HORIZONTE, "B", 4)}
    assert exacto == {"a1-a2": -1, "d2-d3": 1, "d2xc3": -1}
    assert prof(HORIZONTE_TAREA, 0) == {"b1-b2": 1, "c1-c2": 1, "a2-a3": 1, "d2xc3": 12}
    assert prof(HORIZONTE_TAREA, 1) == {"b1-b2": -11, "c1-c2": -11, "a2-a3": -12, "d2xc3": -1}


def test_clase_3_tarea_gato():
    assert j.gato_profundidad_2() == {0: -1, 1: -2, 2: -1, 3: -2, 4: 1,
                                      5: -2, 6: -1, 7: -2, 8: -1}
    assert j.gato_valor() == 0


def test_clase_4_simultaneos():
    assert j.punto_de_silla(j.PARES_O_NONES) == (-1, 1)
    assert j.mezcla_2x2(j.PARES_O_NONES) == (F(1, 2), F(1, 2), 0)
    assert j.punto_de_silla(j.PIEDRA_PAPEL_TIJERA) == (-1, 1)
    assert j.garantia_mezcla(j.PIEDRA_PAPEL_TIJERA, [F(1, 3)] * 3) == 0
    assert j.punto_de_silla(j.PENALES) == (50, 80)
    assert j.mezcla_2x2(j.PENALES) == (F(3, 8), F(1, 2), 65)
    assert j.equilibrios_puros(j.GALLINA_FILA, j.GALLINA_COL) == [(0, 1), (1, 0)]
    assert j.equilibrios_puros(j.PRISIONERO_FILA, j.PRISIONERO_COL) == [(1, 1)]


def test_clase_4_gallina_mezcla():
    # Cada uno sigue con probabilidad 1/10: el rival queda indiferente.
    q = F(1, 10)
    desviarse = (1 - q) * j.GALLINA_FILA[0][0] + q * j.GALLINA_FILA[0][1]
    seguir = (1 - q) * j.GALLINA_FILA[1][0] + q * j.GALLINA_FILA[1][1]
    assert desviarse == seguir == F(-1, 10)


def test_clase_2_ramificacion_y_horizonte_detalle():
    H = "B..." + "..BB" + "..N." + "NN.."
    assert j.evaluar_peones(H, 4) == 1
    tras = j.mover(H, (7, 10))  # d2xc3
    assert {j.nombre_jugada(tras, m, 4): j.evaluar_peones(j.mover(tras, m), 4)
            for m in j.jugadas(tras, "N", 4)} == {"a4-a3": 12, "b4-b3": 12, "b4xc3": 0}


def test_clase_3_numeros_de_la_prosa():
    H = "B..." + "..BB" + "..N." + "NN.."
    T = ".BB." + "B..B" + "..NN" + "NN.."
    prof = lambda t, d: [j.minimax_limitado(j.mover(t, m), "N", d, 4)
                         for m in j.jugadas(t, "B", 4)]
    assert prof(H, 2) == [-9, 100, 1]
    assert j.evaluar_peones(T, 4) == 0
    assert prof(T, 2) == [1, 1, 0, 0]
    assert prof(T, 3) == [-100, -100, -1, -1]
    assert prof(T, 4) == [-100, -100, 100, 12]
    tras = j.mover(T, (7, 10))  # d2xc3
    assert [j.evaluar_peones(j.mover(tras, m), 4) for m in j.jugadas(tras, "N", 4)] == [
        11, 11, 11, -1]
    centro = "....X...."
    assert j.gato_eval("." * 9) == 0 and j.gato_eval(centro) == 4


def test_clase_4_numeros_de_la_prosa():
    assert j.garantia_mezcla(j.PARES_O_NONES, [F(3, 4), F(1, 4)]) == F(-1, 2)
    assert j.garantia_mezcla(j.PIEDRA_PAPEL_TIJERA, [F(1, 2), F(1, 2), 0]) == F(-1, 2)
    assert j.garantia_mezcla(j.PENALES, [F(1, 2), F(1, 2)]) == 60
    assert j.garantia_mezcla(j.PENALES, [0, 1]) == 50
    assert j.garantia_mezcla(j.PENALES, [1, 0]) == 40
    # El portero con q = 1/2 deja 65 contra cualquier tiro.
    assert [F(1, 2) * fila[0] + F(1, 2) * fila[1] for fila in j.PENALES] == [65, 65]
    tarea = [[60, 80], [70, 40]]
    assert j.punto_de_silla(tarea) == (60, 70)
    assert j.mezcla_2x2(tarea) == (F(3, 5), F(4, 5), 64)
    assert j.garantia_mezcla(tarea, [F(3, 5), F(2, 5)]) == 64


def test_clase_1_posiciones_de_negras_por_simetria():
    # 37 estados no finales con Negras al turno; 19 si se identifican reflejos.
    espejo = lambda t: "".join(t[f * 3:(f + 1) * 3][::-1] for f in range(3))
    vistos, pila, negras = set(), [(j.inicio(), "B")], set()
    while pila:
        t, p = pila.pop()
        if (t, p) in vistos:
            continue
        vistos.add((t, p))
        if j.ganador(t, p):
            continue
        if p == "N":
            negras.add(t)
        pila += [(j.mover(t, m), j.otro(p)) for m in j.jugadas(t, p)]
    assert len(negras) == 37
    assert len({min(t, espejo(t)) for t in negras}) == 19


def test_clase_4_tenis_y_silla():
    tenis = [[60, 80], [70, 40]]
    assert j.garantia_mezcla(tenis, [0, 1]) == 40
    assert j.garantia_mezcla(tenis, [1, 0]) == 60
    assert j.punto_de_silla([[3, 5], [1, 4]]) == (3, 3)


def _no_finales_4x4():
    vistos, pila = set(), [(j.inicio(4), "B")]
    while pila:
        t, p = pila.pop()
        if (t, p) in vistos:
            continue
        vistos.add((t, p))
        if j.ganador(t, p, 4):
            continue
        pila += [(j.mover(t, m), j.otro(p)) for m in j.jugadas(t, p, 4)]
    return {(t, p) for t, p in vistos if not j.ganador(t, p, 4)}


def test_clase_3_cotas_y_alcanzables():
    nf = _no_finales_4x4()
    assert max(abs(j.evaluar_peones(t, 4)) for t, _ in nf) == 36
    assert max(abs(j.evaluar_peones(t, 4) - 10 * (t.count("B") - t.count("N")))
               for t, _ in nf) == 6
    H = "B..." + "..BB" + "..N." + "NN.."
    T = ".BB." + "B..B" + "..NN" + "NN.."
    assert (H, "B") in nf and (T, "B") in nf


def test_clase_3_toda_primera_jugada_de_gato_empata():
    # Tras cualquier primera X, el valor exacto con O al turno es 0.
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def v(t, p):
        g = j.gato_gana(t)
        if g:
            return 1 if g == "X" else -1
        if "." not in t:
            return 0
        hijos = [v(t[:i] + p + t[i + 1:], "O" if p == "X" else "X")
                 for i in range(9) if t[i] == "."]
        return max(hijos) if p == "X" else min(hijos)
    assert [v("." * i + "X" + "." * (8 - i), "O") for i in range(9)] == [0] * 9


# La partida que la pagina «Escribir el juego» traza con las siete piezas.
PARTIDA_TRAZADA = ["a1-a2", "b3xa2", "b1-b2", "a2-a1"]


def test_clase_1_partida_trazada_con_las_piezas():
    t, p = j.inicio(), "B"
    jugadores, opciones = [], []
    for nombre in PARTIDA_TRAZADA:
        assert not j.ganador(t, p)  # no esta en S_F
        jugadores.append(p)
        ms = {j.nombre_jugada(t, m): m for m in j.jugadas(t, p)}
        opciones.append(list(ms))
        assert nombre in ms  # la jugada elegida es legal
        t, p = j.mover(t, ms[nombre]), j.otro(p)
    assert jugadores == ["B", "N", "B", "N"]
    assert opciones == [["a1-a2", "b1-b2", "c1-c2"],
                        ["b3-b2", "b3xa2", "c3-c2"],
                        ["b1-b2", "b1xa2", "c1-c2"],
                        ["a2-a1", "a3xb2", "c3-c2", "c3xb2"]]
    # s4: un peon negro llego a la fila 1. Final, gana Negras, U = -1.
    assert (t, p) == ("N.B" + ".B." + "N.N", "B")
    assert j.ganador(t, p) == "N"
    assert j.utilidad_simple(j.ganador(t, p), 0) == -1


def test_clase_1_racional_con_una_utilidad_mal_escrita():
    # «Jugar bien», caso 2: +3 por captura hace preferir c1xb2, que pierde.
    con_premio = j.valor_con_premio_por_captura(SUBARBOL, "B", 3)
    assert con_premio == {"c1-c2": 1, "c1xb2": 2}
    assert max(con_premio, key=con_premio.get) == "c1xb2"
    reglamento = {j.nombre_jugada(SUBARBOL, m):
                  j.valor(j.mover(SUBARBOL, m), "N")
                  for m in j.jugadas(SUBARBOL, "B")}
    assert reglamento == {"c1-c2": 1, "c1xb2": -1}
    # Tras c1xb2, Negras gana de inmediato con c3xb2.
    t = j.mover(SUBARBOL, (2, 4))
    ms = {j.nombre_jugada(t, m): m for m in j.jugadas(t, "N")}
    assert j.ganador(j.mover(t, ms["c3xb2"]), "B") == "N"
    # Con +2 empatan, por eso la pagina dice +3.
    assert j.valor_con_premio_por_captura(SUBARBOL, "B", 2) == {
        "c1-c2": 1, "c1xb2": 1}


# ------------------------------------------------------------- clase 2 ---
# Todo con la utilidad de la clase 1: +1 si gana Blancas y -1 si gana Negras.

E1 = "..B.B.NN."  # el caso propio de «Minimax como algoritmo»; mueven Negras


def test_clase_2_minimax_a_mano():
    assert j.contar_arbol(SUBARBOL) == (13, 13)
    assert j.valor(SUBARBOL, "B") == 1
    # Tras c1xb2 (n3), Negras gana con c3xb2.
    n3 = j.mover(SUBARBOL, (2, 4))
    assert {j.nombre_jugada(n3, m): j.valor(j.mover(n3, m), "B")
            for m in j.jugadas(n3, "N")} == {"a3xb2": 1, "c3-c2": 1, "c3xb2": -1}
    # El juego completo: las tres aperturas pierden.
    assert j.valor(j.inicio(), "B") == -1
    assert {j.nombre_jugada(j.inicio(), m): j.valor(j.mover(j.inicio(), m), "N")
            for m in j.jugadas(j.inicio(), "B")} == {"a1-a2": -1, "b1-b2": -1, "c1-c2": -1}
    # n1 viene de un error de Negras: tras a1-a2, solo la captura gana.
    tras_a2 = j.mover(j.inicio(), (0, 3))
    assert {j.nombre_jugada(tras_a2, m): j.valor(j.mover(tras_a2, m), "B")
            for m in j.jugadas(tras_a2, "N")} == {"b3-b2": 1, "b3xa2": -1, "c3-c2": 1}


def test_clase_2_minimax_como_algoritmo():
    assert j.partida_mas_larga() == 7
    assert sum(4 ** i for i in range(8)) == 21845
    # Ramificacion: 162 jugadas entre 70 estados no finales; maximo 4.
    vistos, pila, total, maximo = set(), [(j.inicio(), "B")], 0, 0
    while pila:
        t, p = pila.pop()
        if (t, p) in vistos:
            continue
        vistos.add((t, p))
        if j.ganador(t, p):
            continue
        ms = j.jugadas(t, p)
        total, maximo = total + len(ms), max(maximo, len(ms))
        pila += [(j.mover(t, m), j.otro(p)) for m in ms]
    assert (total, maximo, len(vistos) - 65) == (162, 4, 70)
    # El caso propio e1: tras b1-b2, c3xb2 y a1xb2.
    t, p = j.inicio(), "B"
    for nombre in ["b1-b2", "c3xb2", "a1xb2"]:
        m = {j.nombre_jugada(t, m): m for m in j.jugadas(t, p)}[nombre]
        t, p = j.mover(t, m), j.otro(p)
    assert (t, p) == (E1, "N")
    assert j.contar_arbol(E1, "N") == (11, 11)
    assert j.valor(E1, "N") == -1
    assert {j.nombre_jugada(E1, m): j.valor(j.mover(E1, m), "B")
            for m in j.jugadas(E1, "N")} == {"a3-a2": -1, "a3xb2": 1}


def test_clase_2_azar():
    # El volado: si empieza Negras, gana Blancas.
    assert j.valor(j.inicio(), "N") == 1
    assert F(1, 2) * -1 + F(1, 2) * 1 == 0
    # Una Negras que mueve al azar.
    assert j.expectiminimax_rival_al_azar(j.mover(SUBARBOL, (2, 4)), "N") == F(1, 3)
    aperturas = {j.nombre_jugada(j.inicio(), m):
                 j.expectiminimax_rival_al_azar(j.mover(j.inicio(), m), "N")
                 for m in j.jugadas(j.inicio(), "B")}
    assert aperturas == {"a1-a2": F(5, 9), "b1-b2": F(3, 4), "c1-c2": F(5, 9)}
    assert {k: (v + 1) / 2 for k, v in aperturas.items()} == {
        "a1-a2": F(7, 9), "b1-b2": F(7, 8), "c1-c2": F(7, 9)}
    # Con azar importa la escala: volado entre +1 y -L contra un empate seguro.
    volado = lambda L: F(1, 2) * 1 + F(1, 2) * -L
    assert volado(1) == 0 and volado(2) == F(-1, 2)
    assert volado(F(1, 2)) > 0 and volado(F(3, 2)) < 0


def test_clase_2_alfa_beta():
    assert j.alfa_beta(SUBARBOL, "B") == (1, 5, [("alfa", "a3xb2", 2)])
    assert j.alfa_beta(SUBARBOL, "B", invertir=True) == (1, 8, [("beta", "b2xa3", 2)])
    # Sin el igual en las condiciones, no se corta nada en n1.
    assert j.alfa_beta(SUBARBOL, "B", estricto=True)[:2] == (1, 13)
    # El juego completo.
    assert j.alfa_beta(j.inicio(), "B")[:2] == (-1, 82)
    assert j.alfa_beta(j.inicio(), "B", invertir=True)[:2] == (-1, 72)
    # Con la ventana [-1, +1], la de los valores de U.
    assert j.alfa_beta(SUBARBOL, "B", alfa=-1, beta=1) == (1, 2, [("beta", "c1-c2", 1)])
    assert j.alfa_beta(j.inicio(), "B", alfa=-1, beta=1)[:2] == (-1, 49)
    assert j.alfa_beta(j.inicio(), "B", invertir=True, alfa=-1, beta=1)[:2] == (-1, 53)


def test_clase_2_tarea():
    assert j.monedas_valor((2, 1, 5, 3)) == 3
    assert j.monedas_codicioso_contra_optimo((2, 1, 5, 3)) == -1
    assert j.monedas_conteos(4) == (23, 8, 11)
    assert j.monedas_alfa_beta((2, 1, 5, 3)) == (3, 23)
    assert j.monedas_alfa_beta((2, 1, 5, 3), True) == (3, 21)
    for n in range(1, 9):
        assert j.monedas_conteos(n)[0] == 2 ** n - 1 + 2 ** (n - 1)
    # n1 cuando quedarse sin jugada empata.
    assert j.valor(SUBARBOL, "B", sin_jugada_empata=True) == 0
    assert j.alfa_beta(SUBARBOL, "B", sin_jugada_empata=True) == (
        0, 10, [("beta", "a2-a3", 1), ("beta", "b1xc2", 2)])
    assert j.alfa_beta(SUBARBOL, "B", invertir=True, sin_jugada_empata=True) == (
        0, 8, [("beta", "b2xa3", 2)])


# ------------------------------------------------- la prosa de la clase 2 ---

import re
from pathlib import Path

UNIDAD = Path(__file__).resolve().parent.parent / "course/7_juegos"


def test_la_unidad_escribe_pl_y_no_p():
    """El jugador de turno es Pl(s), como en la clase 1, en toda la unidad."""
    for pagina in UNIDAD.rglob("*.md"):
        texto = pagina.read_text(encoding="utf-8")
        assert not re.search(r"(?<![A-Za-z\\])P\(s", texto), pagina.name


def test_cada_ejercicio_de_las_clases_2_y_3_trae_pista_y_respuesta():
    paginas = list((UNIDAD / "2_mirar_todo_y_podar").glob("*.md")) + \
        list((UNIDAD / "3_cuando_no_cabe").glob("*.md"))
    for pagina in sorted(paginas):
        texto = pagina.read_text(encoding="utf-8")
        for ejercicio in re.findall(r"::: exercise \{#([\w-]+)", texto):
            assert re.search(rf'::: hint \{{#[\w-]+ of="{ejercicio}"', texto), ejercicio
            assert re.search(rf'::: answer \{{#[\w-]+ of="{ejercicio}"', texto), ejercicio


def test_la_clase_2_usa_la_utilidad_de_la_clase_1():
    """±(10−j) solo aparece en el aviso que explica por qué no se usa (era
    10−k; la k quedó para Monte Carlo plano, ola 4 r1)."""
    for pagina in UNIDAD.rglob("*.md"):
        texto = pagina.read_text(encoding="utf-8")
        assert not re.findall(r"10\s*-\s*k\b", texto), pagina.name
        apariciones = re.findall(r"10\s*-\s*j\b", texto)
        if pagina.name == "1_minimax.md":
            assert len(apariciones) == 1
        else:
            assert not apariciones, pagina.name


# ------------------------------------------------------------- clase 3 ---

def test_clase_3_lo_nuevo():
    # En 4x4 el turno ya no se deduce del tablero.
    assert len(j.tableros_con_dos_turnos(4)) == 2925
    nombres = lambda t: [j.nombre_jugada(t, m, 4) for m in j.jugadas(t, "B", 4)]
    assert nombres(HORIZONTE) == ["a1-a2", "d2-d3", "d2xc3"]
    # Quietud a profundidad 1: -10, 2 y 0; elige d2-d3.
    assert [j.minimax_con_quietud(j.mover(HORIZONTE, m), "N", 0, 4)
            for m in j.jugadas(HORIZONTE, "B", 4)] == [-10, 2, 0]
    # Nodos que genera minimax con corte con d = 1, 2, 3 en la raiz.
    assert [j.nodos_con_corte(HORIZONTE, "B", d, 4) for d in (1, 2, 3)] == [4, 12, 33]
    # Con poda, la jugada anterior primero y la salida en 100: 4, 10 y 9.
    assert j.profundizacion_iterativa(HORIZONTE, (1, 2, 3), 4) == [
        (1, 4, "d2xc3"), (2, 10, "d2-d3"), (3, 9, "d2-d3")]
    assert [j.nodos_con_corte(HORIZONTE_TAREA, "B", d, 4) for d in range(1, 6)] == [
        5, 22, 90, 315, 1001]
    # Promedio exacto de las simulaciones al azar.
    assert [j.promedio_simulaciones(j.mover(HORIZONTE, m), "N", 4)
            for m in j.jugadas(HORIZONTE, "B", 4)] == [F(1097, 5184), F(8, 9), F(11, 72)]
    assert [round(float(x), 2) for x in (F(1097, 5184), F(8, 9), F(11, 72))] == [0.21, 0.89, 0.15]
    assert [j.promedio_simulaciones(j.mover(j.inicio(), m), "N")
            for m in j.jugadas(j.inicio(), "B")] == [F(7, 36), F(5, 24), F(7, 36)]
    assert (F(8, 9) + 1) / 2 == F(17, 18) and (F(5, 24) + 1) / 2 == F(29, 48)


def test_clase_3_el_rasgo_de_capturas_no_arregla_el_error():
    """El ejercicio «Decide si un rasgo nuevo arregla el error»."""
    def capturas(t, quien):
        return sum(1 for m in j.jugadas(t, quien, 4) if j.es_captura(t, m))
    simetrico, solo_negras = [], []
    for m in j.jugadas(HORIZONTE, "B", 4):
        t = j.mover(HORIZONTE, m)
        e = j.evaluar_peones(t, 4)
        simetrico.append(e - 10 * capturas(t, "N") + 10 * capturas(t, "B"))
        solo_negras.append(e - 10 * capturas(t, "N"))
    assert simetrico == [2, 2, 13]
    assert solo_negras == [-8, 2, 3]


def test_clase_2_el_arbol_t_con_minimax_y_alfa_beta():
    """El arbol T de la clase 2, en sus dos etapas: las cifras del contrato."""
    inf = float("inf")
    # Etapa 1, T1: R = 3 y juega izq; alfa-beta genera 6 de 7.
    m1 = j.traza_decidir(j.ARBOL_T1)
    assert (m1["jugada"], m1["valor"], m1["generados"]) == ("izq", 3, 7)
    assert j.contar_nodos(j.ARBOL_T1) == 7 and j.minimax_arbol(j.ARBOL_T1) == 3
    a1 = j.traza_decidir(j.ARBOL_T1, poda=True)
    assert (a1["jugada"], a1["valor"], a1["generados"]) == ("izq", 3, 6)
    assert a1["podados"] == ["12"] and a1["cortes"] == [("alfa", "D", 2, 3, inf)]
    assert len(m1["filas"]) == 10 and len(a1["filas"]) == 9
    # Etapa 2, T: I = 3, C1 = 5, C2 = 8, C = 5, D = 2, R = 5, juega centro.
    m = j.traza_decidir(j.ARBOL_T)
    assert (m["jugada"], m["valor"], m["generados"]) == ("centro", 5, 14)
    devuelve = {f["hijo"]: f["w"] for f in m["filas"] if f["w"] is not None}
    assert {k: devuelve[k] for k in ("I", "C1", "C2", "C", "D")} == {
        "I": 3, "C1": 5, "C2": 8, "C": 5, "D": 2}
    assert m["orden_generados"] == ["R", "I", "3", "6", "C", "C1", "5", "2", "C2",
                                    "7", "8", "D", "2", "12"]
    # mejor_jugada: ninguna, izq, centro; la de D no mejora (2 > 5 es falso).
    raiz = [(f["hijo"], f["w"], f["mejora"], f["mejor_jugada"])
            for f in m["filas"] if f["evento"] == "raiz"]
    assert raiz == [("I", 3, True, "izq"), ("C", 5, True, "centro"),
                    ("D", 2, False, "centro")]
    # Alfa-beta: 12 de 14 y la misma tabla con menos filas (20 contra 18).
    a = j.traza_decidir(j.ARBOL_T, poda=True)
    assert (a["jugada"], a["valor"], a["generados"]) == ("centro", 5, 12)
    assert len(m["filas"]) == 20 and len(a["filas"]) == 18
    assert a["podados"] == ["8", "12"]
    # Corte beta en C2, que llega con [3, 5]: 7 >= 5. Devuelve 7, una cota:
    # su valor exacto es 8. Corte alfa en D, que llega con [5, +inf]: 2 <= 5.
    assert a["cortes"] == [("beta", "C2", 7, 3, 5), ("alfa", "D", 2, 5, inf)]
    assert j.minimax_arbol(j.ARBOL_T[1][1]) == 8
    entra = {f["nodo"]: (f["alfa"], f["beta"]) for f in a["filas"] if f["evento"] == "entra"}
    assert entra == {"I": (-inf, inf), "C": (3, inf), "C1": (3, inf), "C2": (3, 5),
                     "D": (5, inf)}
    # La tabla impresa trae las columnas del contrato.
    tabla = j.tabla_traza(a)
    assert tabla.splitlines()[0] == (
        "| # | línea | pila | (α, β) | v | w | ¿corta? | mejor_jugada |")
    assert "| 12 | 12–14 | R›C›C2 | (3, 5) | 7 | 7 | sí: 7≥5 | izq |" in tabla
    assert "centro (2 > 5 falso)" in tabla
    assert j.tabla_traza(m).splitlines()[0] == "| # | línea | pila | v | w | mejor_jugada |"


def test_clase_2_el_arbol_t_con_azar():
    jugada, valores, generados = j.expectiminimax_t()
    assert jugada == "der" and len(generados) == 14
    assert (valores["I"], valores["C"], valores["D"]) == (F(9, 2), F(13, 2), F(7))
    assert (valores["C1"], valores["C2"]) == (5, 8)


def test_clase_3_el_arbol_t_con_corte_y_contra_el_reloj():
    jugadas, nodos = [], []
    for d in (1, 2, 3):
        t = j.traza_decidir(j.ARBOL_T, profundidad=d, evaluar=j.EVAL_T)
        jugadas.append((t["jugada"], t["valor"]))
        nodos.append(t["generados"])
    assert jugadas == [("der", 7), ("centro", 6), ("centro", 5)]
    assert nodos == [4, 10, 14]
    pi = j.profundizacion_iterativa_t()
    assert [(d, orden, t["jugada"], t["valor"], t["generados"]) for d, orden, t in pi] == [
        (1, ["izq", "centro", "der"], "der", 7, 4),
        (2, ["der", "izq", "centro"], "centro", 6, 10),
        (3, ["centro", "izq", "der"], "centro", 5, 11)]
    assert [c[:2] for c in pi[2][2]["cortes"]] == [("beta", "C2"), ("alfa", "I"), ("alfa", "D")]


def test_clase_3_la_iterativa_sale_con_100_como_la_linea_9():
    """`if w = 100: return a`: con I = (+1, +1), a d = 2 izq (la anterior,
    primero) devuelve 100 y la búsqueda acaba ahí: no mira C ni D, y no hay
    d = 3. En T y T± ningún hijo de la raíz llega a 100, y nada cambia."""
    gana = j.escalar_arbol(((1, 1),) + j.ARBOL_TPM[1:], 100)
    pi = j.profundizacion_iterativa_t(gana, (1, 2, 3), j.EVAL_TPM)
    assert [(d, orden, t["jugada"], t["valor"], t["generados"]) for d, orden, t in pi] == [
        (1, ["izq", "centro", "der"], "izq", 60, 4),
        (2, ["izq", "centro", "der"], "izq", 100, 4)]
    assert pi[-1][2]["orden_generados"] == ["R", "I", "100", "100"]
    for arbol, evaluar in ((j.ARBOL_T, j.EVAL_T), (j.escalar_arbol(j.ARBOL_TPM, 100), j.EVAL_TPM)):
        pi = j.profundizacion_iterativa_t(arbol, (1, 2, 3), evaluar)
        assert len(pi) == 3 and all(f["w"] != 100 for _, _, t in pi for f in t["filas"]
                                    if f["evento"] == "raiz")


def test_clase_2_sin_el_igual_se_pierde_la_poda():
    # Sin el igual, el juego completo pierde casi toda la poda: 228 y 171.
    assert j.alfa_beta(j.inicio(), "B", estricto=True)[:2] == (-1, 228)
    assert j.alfa_beta(j.inicio(), "B", invertir=True, estricto=True)[:2] == (-1, 171)


# ------------------------------------- clase 3: cifras de la reescritura ---
#
# Cada cifra que las paginas de «Cuando el arbol no cabe» van a citar tras la
# reescritura de 2026-10 (plan G2): una funcion de juegos.py y una asercion
# aqui. Las que antes nadie fijaba (EVAL de la raiz, el cociente de 16 000,
# cada EVAL de profundidad 2) tambien.

INF = float("inf")


def test_clase_3_micro_de_eval():
    inicio = j.desglose_eval(j.inicio(4), 4)
    assert inicio == dict(peones_b=4, peones_n=4, avance_b=0, avance_n=0,
                          material=0, avance=0, eval=0)
    # La posicion de la clase: 3 contra 3, avance 2 contra 1, EVAL = 1.
    assert j.desglose_eval(HORIZONTE, 4) == dict(peones_b=3, peones_n=3, avance_b=2,
                                                 avance_n=1, material=0, avance=1, eval=1)
    # La del micro: b1-b2, c4-c3, b2xc3 desde el inicio; mueven Negras.
    t, turno = j.jugar_nombres(j.inicio(4), "B", j.CAMINO_MICRO_EVAL, 4)
    assert j.CAMINO_MICRO_EVAL == ["b1-b2", "c4-c3", "b2xc3"]
    assert t == "B.BB" + "...." + "..B." + "NN.N" and turno == "N"
    assert j.desglose_eval(t, 4) == dict(peones_b=4, peones_n=3, avance_b=2, avance_n=0,
                                         material=1, avance=2, eval=12)
    assert (t, turno) in _no_finales_4x4()


def test_clase_3_crece_mas_de_16000_veces():
    nodos_3, _ = j.contar_arbol()
    nodos_4, _ = j.contar_arbol(n=4)
    assert nodos_4 // nodos_3 == 16658 and nodos_4 / nodos_3 > 16000


def test_clase_3_cada_eval_de_profundidad_2():
    assert j.evals_tras_respuestas(HORIZONTE, "B", 4) == {
        "a1-a2": {"c3xd2": -10, "a4-a3": 1, "b4-b3": 1},
        "d2-d3": {"a4-a3": 1, "b4-b3": 1},
        "d2xc3": {"a4-a3": 12, "b4-b3": 12, "b4xc3": 0}}


def test_clase_3_la_rama_d2_d3_a_profundidad_3():
    rama = j.arbol_con_corte(HORIZONTE, "B", 3, 4)["hijos"][1]
    assert rama["jugada"] == "d2-d3" and rama["valor"] == 100
    vistas = {r["jugada"]: {h["jugada"]: (h["valor"], h["final"]) for h in r["hijos"]}
              for r in rama["hijos"]}
    assert vistas == {"a4-a3": {"a1-a2": (2, None), "d3-d4": (100, "B")},
                      "b4-b3": {"a1-a2": (2, None), "c2xb3": (13, None),
                                "d3-d4": (100, "B")}}
    assert [r["valor"] for r in rama["hijos"]] == [100, 100]
    # La rama tiene 8 nodos contando el de d2-d3; 7 debajo de el.
    assert j.contar_con_corte(rama) == 8
    # Y los tres valores de la raiz con d = 3 siguen siendo -9, 100 y 1.
    raiz = j.arbol_con_corte(HORIZONTE, "B", 3, 4)
    assert [h["valor"] for h in raiz["hijos"]] == [-9, 100, 1]
    assert j.contar_con_corte(raiz) == 33


def test_clase_3_b_es_5_en_el_arbol_de_profundidad_3():
    b, donde = j.ramificacion_maxima(j.arbol_con_corte(HORIZONTE, "B", 3, 4))
    assert b == 5 and donde == [["a1-a2", "b4-b3"]]
    assert [j.ramificacion_maxima(j.arbol_con_corte(HORIZONTE, "B", d, 4))[0]
            for d in (1, 2)] == [3, 3]


def test_clase_3_traza_de_t_con_d_2_fila_por_fila():
    filas = j.filas_corte_t(2)
    assert [tuple(f) for f in filas] == [
        (1, "2 · R", "−∞", "", "—"),
        (2, "17 · R›I", "+∞", "", "—"),
        (3, "19–20 · R›I", "3", "3", "—"),
        (4, "19–20 · R›I", "3", "6", "—"),
        (5, "4–5 · R", "3", "3 (I)", "izq"),
        (6, "17 · R›C", "+∞", "", "izq"),
        (7, "19–20 · R›C", "6", "6 (C1)", "izq"),
        (8, "19–20 · R›C", "6", "9 (C2)", "izq"),
        (9, "4–5 · R", "6", "6 (C)", "centro"),
        (10, "17 · R›D", "+∞", "", "centro"),
        (11, "19–20 · R›D", "2", "2", "centro"),
        (12, "19–20 · R›D", "2", "12", "centro"),
        (13, "4–5 · R", "6", "2 (D)", "centro"),
        (14, "6 · R", "6", "", "centro")]


def test_clase_3_ejercicio_final_de_minimax_con_corte():
    # (a) El empate: EVAL(C1) = 3 iguala C con I; con «>» estricto, el orden
    # de R decide la jugada (sin empate, el orden no la cambia).
    assert j.EVAL_T_EMPATE == {"I": 5, "C": 4, "D": 7, "C1": 3, "C2": 9}
    assert j.decidir_con_corte_t(2, evaluar=j.EVAL_T_EMPATE) == ("izq", 3, 10)
    assert j.decidir_con_corte_t(2, orden=["D", "C", "I"], evaluar=j.EVAL_T_EMPATE) == (
        "centro", 3, 10)
    assert j.decidir_con_corte_t(2, orden=["D", "C", "I"]) == ("centro", 6, 10)
    # (b) EVAL(C2) = 1 en vez de 9: cambia d = 2, no d = 1 ni d = 3.
    assert j.EVAL_T_VARIANTE == {"I": 5, "C": 4, "D": 7, "C1": 6, "C2": 1}
    assert [j.decidir_con_corte_t(d, evaluar=j.EVAL_T_VARIANTE)[:2] for d in (1, 2, 3)] == [
        ("der", 7), ("izq", 3), ("centro", 5)]
    assert [j.decidir_con_corte_t(d)[:2] for d in (1, 2, 3)] == [
        ("der", 7), ("centro", 6), ("centro", 5)]
    # (c) Nodos generados con d = 1, 2, 3.
    assert [j.decidir_con_corte_t(d)[2] for d in (1, 2, 3)] == [4, 10, 14]


def test_clase_3_iterativa_sin_poda_en_t():
    for anterior_primero in (False, True):
        corridas = j.iterativa_sin_poda_t(anterior_primero=anterior_primero)
        assert [(d, jugada, valor, nodos) for d, _, jugada, valor, nodos in corridas] == [
            (1, "der", 7, 4), (2, "centro", 6, 10), (3, "centro", 5, 14)]
        assert sum(c[4] for c in corridas) == 28
    assert [c[1] for c in j.iterativa_sin_poda_t(anterior_primero=True)] == [
        ["izq", "centro", "der"], ["der", "izq", "centro"], ["centro", "izq", "der"]]


def test_clase_3_traza_de_alfa_beta_con_corte_d_3_centro_primero():
    t = j.traza_decidir(j.ARBOL_T, poda=True, orden={"R": ["C", "I", "D"]}, profundidad=3,
                        evaluar=j.EVAL_T, lineas=j.LINEAS_RELOJ)
    assert j.llamadas_alfa_beta(t) == [
        ("C", -INF, INF, 5, None),
        ("C1", -INF, INF, 5, None),
        ("C2", -INF, 5, 7, "beta"),
        ("I", 5, INF, 3, "alfa"),
        ("D", 5, INF, 2, "alfa")]
    assert (t["jugada"], t["valor"], t["generados"]) == ("centro", 5, 11)
    assert t["orden_generados"] == ["R", "C", "C1", "5", "2", "C2", "7", "I", "3", "D", "2"]


def test_clase_3_iterativa_con_otro_orden_y_un_reloj():
    corridas, entrega = j.iterativa_con_reloj_t(["der", "centro", "izq"])
    assert [(c["d"], c["orden"], c["jugada"], c["generados"]) for c in corridas] == [
        (1, ["der", "centro", "izq"], "der", 4),
        (2, ["der", "centro", "izq"], "centro", 9),
        (3, ["centro", "der", "izq"], "centro", 11)]
    assert entrega["jugada"] == "centro" and entrega["generados"] == 24
    # El orden de la pagina da 4, 10 y 11, y entrega centro.
    corridas, entrega = j.iterativa_con_reloj_t(["izq", "centro", "der"])
    assert [c["generados"] for c in corridas] == [4, 10, 11] and entrega["generados"] == 25
    # Un reloj de 10 nodos se acaba en d = 2, tras valorar centro: entrega der.
    _, entrega = j.iterativa_con_reloj_t(["der", "centro", "izq"], tope=10)
    assert entrega == dict(jugada="der", d=2, generados=11, linea=8, despues_de="centro")
    _, entrega = j.iterativa_con_reloj_t(["der", "centro", "izq"], tope=20)
    assert entrega == dict(jugada="centro", d=3, generados=20, linea=8, despues_de="centro")


def test_clase_3_tabla_unica_de_nodos_generados():
    tabla = j.tabla_nodos_generados()
    assert tabla == {
        ("T", "sin poda"): [4, 10, 14],
        ("T", "alfa-beta"): [4, 9, 12],
        ("T", "iterativa"): [4, 10, 11],
        ("4x4", "sin poda"): [4, 12, 33],
        ("4x4", "alfa-beta"): [4, 12, 22],
        ("4x4", "iterativa"): [4, 10, 9]}
    totales = {k: sum(v) for k, v in tabla.items()}
    assert totales[("T", "iterativa")] == 25 == 4 + 10 + 11
    assert totales[("T", "sin poda")] == 28 == 4 + 10 + 14
    assert totales[("T", "alfa-beta")] == 25
    assert totales[("4x4", "sin poda")] == 49 and totales[("4x4", "alfa-beta")] == 38
    assert totales[("4x4", "iterativa")] == 23
    # El orden de jugadas en la posicion 4x4: por casilla de origen.
    assert [j.nombre_jugada(HORIZONTE, m, 4) for m in j.jugadas(HORIZONTE, "B", 4)] == [
        "a1-a2", "d2-d3", "d2xc3"]


def test_clase_3_tabla_de_transposicion_por_la_ventana():
    assert j.clase_de_valor(-INF, INF, 5) == "exacto"
    assert j.clase_de_valor(-INF, 5, 7) == "piso" and j.clase_de_valor(3, 5, 5) == "piso"
    assert j.clase_de_valor(5, INF, 3) == "techo" and j.clase_de_valor(5, INF, 5) == "techo"
    *_, (_, _, t) = j.profundizacion_iterativa_t()
    assert j.clases_transposicion(t) == {
        "C": (-INF, INF, 5, "exacto"), "C1": (-INF, INF, 5, "exacto"),
        "C2": (-INF, 5, 7, "piso"), "I": (5, INF, 3, "techo"), "D": (5, INF, 2, "techo")}
    fijo = j.traza_decidir(j.ARBOL_T, poda=True, profundidad=3, evaluar=j.EVAL_T)
    assert j.clases_transposicion(fijo) == {
        "I": (-INF, INF, 3, "exacto"), "C": (3, INF, 5, "exacto"),
        "C1": (3, INF, 5, "exacto"), "C2": (3, 5, 7, "piso"), "D": (5, INF, 2, "techo")}


def test_clase_3_la_vuelta_de_mcts_cuadra():
    antes = j.mcts_cuentas(j.MCTS_ARBOL)
    assert antes == {"r": (2, 4), "a": (2, 3), "b": (0, 1), "a1": (1, 1), "a2": (0, 1)}
    # Cada nodo que no es la raiz: su simulacion mas las de sus hijos.
    for n, (padre, _, _) in j.MCTS_ARBOL.items():
        hijos = [h for h, (p, _, _) in j.MCTS_ARBOL.items() if p == n]
        propia = 0 if padre is None else 1
        assert antes[n][1] == propia + sum(antes[h][1] for h in hijos), n
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    assert vuelta["camino"] == ["r", "a", "a2"] and vuelta["padre_nuevo"] == "a2"
    assert vuelta["despues"] == {"r": (3, 5), "a": (3, 4), "b": (0, 1), "a1": (1, 1),
                                 "a2": (1, 2), "nuevo": (1, 1)}
    # Con U = -1: el camino suma simulaciones, no victorias.
    menos = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=-1)
    assert menos["despues"] == {"r": (2, 5), "a": (2, 4), "b": (0, 1), "a1": (1, 1),
                                "a2": (0, 2), "nuevo": (0, 1)}
    # Los puntajes con c = 1: MAX elige a en la raiz; MIN, a2 en a.
    assert {k: round(v, 2) for k, v in vuelta["puntajes"]["r"].items()} == {
        "a": 1.01, "b": 0.18}
    assert {k: round(v, 2) for k, v in vuelta["puntajes"]["a"].items()} == {
        "a1": 0.05, "a2": 2.05}


def test_clase_3_uct_en_el_ejercicio():
    # Con el promedio de U (el de la pagina) y c = 1: la vuelta siguiente
    # baja por y; se entrega x, la mas simulada.
    p = j.uct_ejercicio(c=1)
    assert {k: round(v, 2) for k, v in p.items()} == {"x": 0.78, "y": 0.99, "z": 0.88}
    assert max(p, key=p.get) == "y" and j.mas_simulada(j.EJERCICIO_MCTS) == "x"
    # Con G/N (victorias entre simulaciones) y c = 1, gana z; y gana si c < 0.69.
    g = j.uct_ejercicio(c=1, victorias=True)
    assert {k: round(v, 2) for k, v in g.items()} == {"x": 1.03, "y": 1.19, "z": 1.28}
    assert max(g, key=g.get) == "z"
    assert max(j.uct_ejercicio(c=F(1, 2), victorias=True).items(), key=lambda kv: kv[1])[0] == "y"
    assert {k: j.victorias(n, m) for k, (n, m) in j.EJERCICIO_MCTS.items()} == {
        "x": 45, "y": 24, "z": 6}


def test_clase_3_simular_con_solo_negras_al_azar():
    jugadas = j.jugadas(HORIZONTE, "B", 4)
    solo_negras = [j.expectiminimax_rival_al_azar(j.mover(HORIZONTE, m), "N", 4)
                   for m in jugadas]
    ambos = [j.promedio_simulaciones(j.mover(HORIZONTE, m), "N", 4) for m in jugadas]
    assert solo_negras == [F(2, 3), F(1), F(1, 3)]
    assert ambos == [F(1097, 5184), F(8, 9), F(11, 72)]
    # Hexapawn: 5/9, 3/4, 5/9 (la clase 2) contra 7/36, 5/24, 7/36.
    apertura = j.jugadas(j.inicio(), "B")
    assert [j.expectiminimax_rival_al_azar(j.mover(j.inicio(), m), "N") for m in apertura] == [
        F(5, 9), F(3, 4), F(5, 9)]


# ------------------------- clase 3: la prosa contra la fuente (defecto #39) ---
#
# Las pruebas de arriba fijan la FUENTE: si cambia una regla de juegos.py,
# fallan. Pero ninguna leia la pagina, y una cifra cambiada en la prosa no
# rompia nada: en la revision adversarial de la clase 7.3 una lente cambio
# un 11 por 12 en la prosa y la suite siguio verde (defectos.md, #39). Las
# de aqui localizan cada cifra EN LA PAGINA por un ancla estable (id de
# tabla, de figura, de ejercicio o de su respuesta), la extraen y la comparan
# con la funcion de juegos.py que la calcula. Ninguna cifra esperada se
# escribe a mano: si la prosa y la fuente se separan, por cualquiera de los
# dos lados, falla.

CLASE_3 = UNIDAD / "3_cuando_no_cabe"
P1, P2, P3, P4, P5 = ("1_cortar_y_evaluar.md", "1_cortar_y_evaluar.md",
                      "2_jugar_contra_el_reloj.md", "2_jugar_contra_el_reloj.md",
                      "3_simular_en_vez_de_evaluar.md")
# Ola 3: el MCTS de la antigua p5 vive ahora en su propia pagina (destinos R17).
P5b = "4_monte_carlo_en_un_arbol_grande.md"
_JUGADA = r"[a-d][1-4][-x][a-d][1-4]"


def _pagina(nombre):
    return (CLASE_3 / nombre).read_text(encoding="utf-8")


def _limpio(s):
    """El texto de la pagina sin lo que no es la cifra: «−» pasa a «-», fuera
    espacios estrechos (U+202F), word joiners (U+2060), negritas, «$» y las
    llaves de ${…}$; \\text{a1}\\textbf{-}\\text{a2} queda «a1-a2»."""
    s = str(s).replace("\u2212", "-").replace("\u2060", "").replace("\u202f", "")
    s = s.replace("\u00a0", " ").replace("\\,", "")
    s = re.sub(r"\\(?:text|textbf|mathrm|mathbf)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\le(?![a-z])", "≤", s)
    s = re.sub(r"\\ge(?![a-z])", "≥", s)
    s = s.replace("\\cdot", "·").replace("\\approx", "≈").replace("\\infty", "∞")
    s = s.replace("**", "").replace("$", "")
    return re.sub(r"\s+", " ", re.sub(r"(?<!\\)[{}]", "", s))


def _c(celda):
    return re.sub(r"\s+", " ", _limpio(celda)).strip()


def _bloque(texto, ident):
    """El cuerpo de la directiva «::: tipo {#ident …}» hasta su «:::»."""
    m = re.search(rf"^::: \w+ \{{#{re.escape(ident)}[ }}].*?$\n(.*?)^:::[ \t]*$",
                  texto, re.M | re.S)
    assert m, f"no encuentro {ident} en la pagina"
    return m.group(1)


def _titulo(texto, ident):
    m = re.search(rf'^::: \w+ \{{#{re.escape(ident)} title="([^"]*)"', texto, re.M)
    assert m, ident
    return _limpio(m.group(1))


def _respuesta(texto, ejercicio):
    m = re.search(rf'^::: answer \{{#[\w-]+ of="{re.escape(ejercicio)}".*?$\n(.*?)^:::[ \t]*$',
                  texto, re.M | re.S)
    assert m, f"no encuentro la respuesta de {ejercicio}"
    return m.group(1)


def _alt(texto, figura):
    return _limpio(re.search(r"!\[(.*?)\]\(", _bloque(texto, figura), re.S).group(1))


def _tablas(texto):
    """Cada tabla Markdown del texto: [filas], cada fila [celdas en crudo],
    sin la fila separadora."""
    tablas, actual = [], []
    for linea in texto.splitlines() + [""]:
        if linea.startswith("|"):
            celdas = [c.strip() for c in linea.strip()[1:-1].split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in celdas):
                actual.append(celdas)
        elif actual:
            tablas.append(actual)
            actual = []
    return tablas


def _tabla(texto, ident):
    tablas = _tablas(_bloque(texto, ident))
    assert len(tablas) == 1, ident
    return tablas[0]


def _n(celda):
    c = _c(celda)
    if c in ("+∞", "∞"):
        return INF
    if c == "-∞":
        return -INF
    if "/" in c:
        return F(c)
    return float(c) if "." in c else int(c)


def _negrita(celda):
    return "**" in celda


def _tablero(filas):
    """Un tablero de la pagina (fila 4 arriba) en la notacion de juegos.py
    (fila 1 primero)."""
    por_fila = {int(_c(f[0])): "".join(_c(x) if _c(x) in "BN" else "." for x in f[1:])
                for f in filas[1:]}
    return "".join(por_fila[r] for r in sorted(por_fila))


def _corte_en_la_posicion(d):
    """{jugada: valor con corte} de las tres jugadas de la posicion de la clase."""
    return {h["jugada"]: h["valor"]
            for h in j.arbol_con_corte(j.POSICION_C3, "B", d, 4)["hijos"]}


def _exacto_por_100():
    t = j.POSICION_C3
    return {j.nombre_jugada(t, m, 4): 100 * j.valor(j.mover(t, m), "N", n=4)
            for m in j.jugadas(t, "B", 4)}


def _revisa_tabla_de_profundidades(texto, ident):
    """Filas jugada | P1 | P2 | P3 | 100·V; la negrita, en el maximo de cada columna."""
    filas = _tabla(texto, ident)
    esperado = {d: _corte_en_la_posicion(d) for d in (1, 2, 3)}
    esperado[4] = _exacto_por_100()
    leido = {_c(f[0]): [_n(x) for x in f[1:]] for f in filas[1:]}
    assert leido == {m: [esperado[d][m] for d in (1, 2, 3, 4)] for m in esperado[1]}, ident
    for col in (1, 2, 3, 4):
        maximo = max(esperado[col].values())
        for f in filas[1:]:
            assert _negrita(f[col]) == (_n(f[col]) == maximo), (ident, f)


# ---- p1 · cortar y evaluar

def test_prosa_clase_3_p1_el_4x4_y_cuanto_crece_su_arbol():
    """#39 · 2925, la tabla de crecimiento y el «≈16 659» de la respuesta."""
    texto = _pagina(P1)
    limpio = _limpio(texto)
    assert int(re.search(r"encontró (\d+) tableros", limpio).group(1)) == len(
        j.tableros_con_dos_turnos(4))
    nodos_3, estados_3 = j.contar_arbol()
    nodos_4, estados_4 = j.contar_arbol(n=4)
    filas = _tabla(texto, "jue-c3-crecimiento")
    assert [(_c(f[0]), _n(f[1]), _n(f[2])) for f in filas[1:3]] == [
        ("3×3", nodos_3, estados_3), ("4×4", nodos_4, estados_4)]
    m = re.search(r"(\d+)/(\d+)≈(\d+)", _limpio(_respuesta(texto, "jue-c3-ej-crecimiento")))
    assert (int(m[1]), int(m[2]), int(m[3])) == (nodos_4, nodos_3, round(nodos_4 / nodos_3))
    por_estado = [(int(a), int(b), float(c)) for a, b, c in re.findall(
        r"(\d+)/(\d+)≈(\d+(?:\.\d)?)", _limpio(_respuesta(texto, "jue-c3-ej-crecimiento")))[1:]]
    assert por_estado == [(nodos_3, estados_3, round(nodos_3 / estados_3, 1)),
                          (nodos_4, estados_4, round(nodos_4 / estados_4))]
    assert int(re.search(r"Su árbol tiene (\d+) nodos", limpio).group(1)) == nodos_4


def test_prosa_clase_3_la_cota_de_eval_que_citan_las_paginas():
    """#39 · El «36» (|EVAL| maximo fuera de los finales) en p1, p2 y p4."""
    cota = max(abs(j.evaluar_peones(t, 4)) for t, _ in _no_finales_4x4())
    p1 = _pagina(P1)
    assert [int(x) for x in re.findall(r"nunca pasa de (\d+)", _limpio(p1))] == [cota, cota]
    assert int(re.search(r"EVAL=(\d+)", _limpio(_respuesta(p1, "jue-c3-ej-escala")))[1]) == cota
    p2 = _limpio(_bloque(_pagina(P2), "jue-c3-que-afirma"))
    assert int(re.search(r"\|EVAL\|≤(\d+)", p2)[1]) == cota
    # Ola 3: «Hasta dónde mirar» ya no escribe «|EVAL|≤36»; la cifra vive una
    # sola vez en la frase «|EVAL| nunca pasa de 36» (la fórmula general es |EVAL|<M).
    p4 = _limpio(_pagina(P4))
    assert [int(x) for x in re.findall(r"nunca pasa de (\d+)", p4)] == [cota]
    assert "|EVAL|<M" in p4


def test_prosa_clase_3_p1_la_evaluacion_de_la_posicion_y_del_micro():
    """#39 · El tablero de la clase, su EVAL rasgo por rasgo, y el micro de EVAL
    (jugadas, tablero, turno y las dos cuentas de la respuesta)."""
    texto = _pagina(P1)
    tablero = _tablero(_tabla(texto, "jue-c3-posicion"))
    assert tablero == j.POSICION_C3
    d = j.desglose_eval(tablero, 4)
    peones, avance = [[_c(x) for x in f] for f in _tabla(texto, "jue-c3-posicion-eval")[1:]]
    ultimo = lambda c: int(re.findall(r"-?\d+", c)[-1])  # noqa: E731
    assert [ultimo(peones[1]), ultimo(peones[2]), ultimo(avance[1]), ultimo(avance[2])] == [
        d["peones_b"], d["peones_n"], d["avance_b"], d["avance_n"]]
    casillas = lambda p: [j.casilla(i, 4) for i, x in enumerate(tablero) if x == p]  # noqa: E731
    assert re.findall(r"[a-d][1-4]", peones[1]) == casillas("B")
    assert sorted(re.findall(r"[a-d][1-4]", peones[2])) == sorted(casillas("N"))
    m = re.search(r"EVAL=10·\((\d+)-(\d+)\)\+\((\d+)-(\d+)\)=(-?\d+)", _limpio(texto))
    assert [int(x) for x in m.groups()] == [d["peones_b"], d["peones_n"], d["avance_b"],
                                            d["avance_n"], d["eval"]]
    # El micro: las jugadas del enunciado llevan al tablero del enunciado.
    ej = _bloque(texto, "jue-c3-ej-eval")
    assert re.findall(_JUGADA, _limpio(ej)) == j.CAMINO_MICRO_EVAL
    micro, turno = j.jugar_nombres(j.inicio(4), "B", j.CAMINO_MICRO_EVAL, 4)
    assert _tablero(_tablas(ej)[0]) == micro
    assert ("mueven Negras" if turno == "N" else "mueven Blancas") in ej
    resp = _limpio(_respuesta(texto, "jue-c3-ej-eval"))
    cuentas = [tuple(int(x) for x in t) for t in re.findall(r"10·(\d+)\+(\d+)=(\d+)", resp)]
    assert cuentas == [(e["material"], e["avance"], e["eval"])
                       for e in (j.desglose_eval(j.inicio(4), 4), j.desglose_eval(micro, 4))]
    dm = j.desglose_eval(micro, 4)
    assert [tuple(int(x) for x in t)
            for t in re.findall(r"(\d+)(?: peones)?, con avance (\d+)", resp)] == [
        (dm["peones_b"], dm["avance_b"]), (dm["peones_n"], dm["avance_n"])]


def _ramas(alt):
    """{jugada: {respuesta: valor}} de un alt que dice «Tras X, … Y (v) …»."""
    res = {}
    for m in re.finditer(rf"Tras ({_JUGADA}),(.*?)(?=Tras {_JUGADA},|$)", alt, re.S):
        res[m[1]] = {r: int(v) for r, v in re.findall(rf"({_JUGADA}) \((-?\d+)", m[2])}
    return res


def test_prosa_clase_3_p1_profundidad_1_2_y_3_a_mano():
    """#39 · Las cifras de las secciones 7, 8 y 9 de «Cortar y evaluar»: los
    EVAL de cada nodo de corte (en el alt de cada figura y en la respuesta),
    los minimos de Negras, la rama d2-d3 (8 nodos) y los 33 del arbol."""
    texto = _pagina(P1)
    v1, v2 = _corte_en_la_posicion(1), _corte_en_la_posicion(2)
    # Profundidad 1.
    alt1 = _alt(texto, "jue-c3-fig-prof-1")
    assert {m: int(v) for m, v in re.findall(rf"({_JUGADA}) da EVAL = (-?\d+)", alt1)} == v1
    resp1 = _limpio(_respuesta(texto, "jue-c3-ej-prof-1"))
    elegida = max(v1, key=v1.get)
    assert re.search(rf"2\. ({_JUGADA}), con (-?\d+)", resp1).groups() == (
        elegida, str(v1[elegida]))
    # Profundidad 2.
    alt2 = _alt(texto, "jue-c3-fig-prof-2")
    assert _ramas(alt2) == j.evals_tras_respuestas(j.POSICION_C3, "B", 4)
    assert [int(x) for x in re.findall(r"el mínimo es (-?\d+)", alt2)] == list(v2.values())
    resp2 = _limpio(_respuesta(texto, "jue-c3-ej-prof-2"))
    assert int(re.search(r"la captura vale (-?\d+)", resp2)[1]) == v2["d2xc3"]
    assert [int(x) for x in re.search(r"compara (-?\d+),\s+(-?\d+) y (-?\d+)", resp2).groups()] \
        == list(v2.values())
    # Profundidad 3: la rama d2-d3.
    raiz = j.arbol_con_corte(j.POSICION_C3, "B", 3, 4)
    rama = next(h for h in raiz["hijos"] if h["jugada"] == "d2-d3")
    alt3 = _alt(texto, "jue-c3-fig-prof-3")
    assert _ramas(alt3) == {r["jugada"]: {h["jugada"]: h["valor"] for h in r["hijos"]}
                            for r in rama["hijos"]}
    assert int(re.search(r"La rama tiene (\d+) nodos", alt3)[1]) == j.contar_con_corte(rama)
    resp3 = _limpio(_respuesta(texto, "jue-c3-ej-prof-3"))
    m = re.search(r"Tiene (\d+) nodos: 1 \+ (\d+) respuestas \+ (\d+) \+ (\d+)", resp3)
    assert [int(x) for x in m.groups()] == [j.contar_con_corte(rama), len(rama["hijos"])] + [
        len(r["hijos"]) for r in rama["hijos"]]
    assert int(re.search(r"la rama vale (-?\d+)", resp3)[1]) == rama["valor"]
    assert int(re.search(r"ya tiene (\d+) nodos", _limpio(texto))[1]) == j.contar_con_corte(raiz)


def test_prosa_clase_3_p1_tabla_de_profundidades_y_los_113_puntos():
    """#39 · @jue-c3-profundidades (2, 2, 13 / −10, 1, 0 / −9, 100, 1 / exacto)
    y la sobreestimacion de la respuesta, 113 = 13 − (−100)."""
    texto = _pagina(P1)
    _revisa_tabla_de_profundidades(texto, "jue-c3-profundidades")
    v1, exacto = _corte_en_la_posicion(1), _exacto_por_100()
    elegida = max(v1, key=v1.get)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-exacto"))
    m = re.search(r"en (\d+) puntos, (-?\d+)-\((-?\d+)\)", resp)
    assert [int(x) for x in m.groups()] == [v1[elegida] - exacto[elegida], v1[elegida],
                                            exacto[elegida]]
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[1])
    assert [int(x) for x in re.search(r"captura vale (\d+) a profundidad 1 y (-?\d+) a "
                                      r"profundidad 2", llevarse).groups()] == [
        v1["d2xc3"], _corte_en_la_posicion(2)["d2xc3"]]


# ---- p2 · minimax con corte

def _orden_de(texto_con_orden):
    return [j.JUGADA_A_NOMBRE[a] for a in texto_con_orden]


def _filas(filas):
    return [tuple(_c(x) for x in f) for f in filas]


def _esperado(filas):
    return [tuple(_c(x) for x in f) for f in filas]


def _con_huecos(leidas, esperadas):
    """Cada celda leida coincide con la esperada; un «?» vale por cualquier
    texto no vacio."""
    assert len(leidas) == len(esperadas)
    for fila, esp in zip(leidas, esperadas):
        assert len(fila) == len(esp), fila
        for celda, e in zip(fila, esp):
            patron = ".+".join(re.escape(p) for p in celda.split("?"))
            assert re.fullmatch(patron, e), (fila, esp)


def test_prosa_clase_3_p2_lo_que_genera_en_la_posicion():
    """#39 · 4 y 12 nodos con d = 1 y 2, cuantos se expanden y evaluan, el
    4, 12, 33 del costo y la b = 5."""
    texto = _pagina(P2)
    nodos = [j.nodos_con_corte(j.POSICION_C3, "B", d, 4) for d in (1, 2, 3)]
    ej = _limpio(_bloque(texto, "jue-c3-ej-genera"))
    assert int(re.search(r"Con d=2 genera (\d+) nodos", ej)[1]) == nodos[1]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-genera"))
    respuestas = j.evals_tras_respuestas(j.POSICION_C3, "B", 4)
    expandidos = 1 + len(respuestas)
    assert int(re.search(r"1\. (\d+) nodos", resp)[1]) == nodos[0] == expandidos
    assert [int(x) for x in re.search(r"se evalúan, con (\d+), (\d+) y (\d+)", resp).groups()] \
        == list(_corte_en_la_posicion(1).values())
    assert int(re.search(r"Se expanden (\d+)", resp)[1]) == expandidos
    assert int(re.search(r"Los otros (\d+)", resp)[1]) == nodos[1] - expandidos
    assert [int(x) for x in re.search(r"\((\d+), (\d+) y (\d+)\)", resp).groups()] == [
        len(r) for r in respuestas.values()]
    limpio = _limpio(texto)
    m = re.search(r"genera (\d+) nodos con d=1,\s+(\d+) con d=2 y (\d+) con d=3", limpio)
    assert [int(x) for x in m.groups()] == nodos
    b, _ = j.ramificacion_maxima(j.arbol_con_corte(j.POSICION_C3, "B", 3, 4))
    assert int(re.search(r"menos de b=(\d+)", limpio)[1]) == b
    assert [int(x) for x in re.search(r"posición de la clase, (\d+), (\d+) y (\d+) nodos",
                                      limpio).groups()] == nodos
    afirma = _limpio(_bloque(texto, "jue-c3-ej-afirma"))
    assert {m: int(v) for v, m in re.findall(rf"(-?\d+) para ({_JUGADA})", afirma)} == \
        _corte_en_la_posicion(3)
    # Inciso 2: dentro del horizonte Negras gana un peon y lo conserva tras
    # las dos respuestas de Blancas; las dos valen lo mismo que la jugada.
    resp = _limpio(_respuesta(texto, "jue-c3-ej-afirma")).split("2. ")[1]
    rama = j.arbol_con_corte(j.POSICION_C3, "B", 3, 4)["hijos"][0]
    elegida = min(rama["hijos"], key=lambda h: h["valor"])
    m = re.search(rf"Negras responde ({_JUGADA}), gana un peón y lo conserva tras las dos "
                  rf"respuestas de Blancas, ({_JUGADA}) y ({_JUGADA}): las dos valen (-?\d+)",
                  resp)
    assert m and m[1] == elegida["jugada"] and [m[2], m[3]] == [
        h["jugada"] for h in elegida["hijos"]]
    assert {h["valor"] for h in elegida["hijos"]} == {int(m[4]), rama["valor"]}
    material = j.desglose_eval(rama["tablero"], 4)["material"]
    assert all(j.desglose_eval(h["tablero"], 4)["material"] == material - 1
               for h in elegida["hijos"])


def test_prosa_clase_3_p2_evaluacion_y_traza_de_t_con_d_2():
    """#39 · @jue-c3-t-eval (EVAL y 100·V de cada nodo interno), los dos tramos
    de la traza de DECIDIR-CON-CORTE(R, 2) y los «n de 15 nodos» de las figuras.
    Ola 3: re-anclada del arbol base (ARBOL_T, 14 nodos) al arbol de resultados
    (ARBOL_TPM, finales en 100·U, EVAL_TPM; destinos D.2.1)."""
    texto = _pagina(P2)
    exacto = j.valores_con_corte_tpm(3)
    assert {_c(f[0]): (_n(f[1]), _n(f[2])) for f in _tabla(texto, "jue-c3-t-eval")[1:]} == {
        k: (j.EVAL_TPM[k], exacto[k]) for k in j.EVAL_TPM}
    leidas = _filas(_tabla(texto, "jue-c3-t-traza-d2")[1:] +
                    _tabla(texto, "jue-c3-t-traza-d2-tramo-2")[1:])
    assert leidas == _esperado(j.filas_corte_tpm(2))
    total = j.contar_nodos(j.ARBOL_TPM)
    filas = j.traza_decidir(j.ARBOL_TPM_100, profundidad=2, evaluar=j.EVAL_TPM)["filas"]
    tramo_1 = len(_tabla(texto, "jue-c3-t-traza-d2")) - 1
    for figura, generados in [("jue-c3-t-fig-d1", j.decidir_con_corte_tpm(1)[2]),
                              ("jue-c3-t-fig-d2-tramo-1", filas[tramo_1 - 1]["generados"]),
                              ("jue-c3-t-fig-d2-tramo-2", j.decidir_con_corte_tpm(2)[2])]:
        m = re.search(r"Se han generado (\d+) de (\d+) nodos", _alt(texto, figura))
        assert (int(m[1]), int(m[2])) == (generados, total), figura


def test_prosa_clase_3_p2_t_con_cada_profundidad():
    """#39 · @jue-c3-t-por-profundidad: I · C · D, la jugada y los nodos
    (4, 11, 15) con d = 1, 2, 3 en el arbol de resultados; y los 11 nodos de
    la cota. Ola 3: re-anclada a ARBOL_TPM (destinos D.2.1)."""
    texto = _pagina(P2)
    leido = [tuple(_c(x) for x in f) for f in _tabla(texto, "jue-c3-t-por-profundidad")[1:]]
    esperado = []
    for d in (1, 2, 3):
        w = {f["hijo"]: f["w"] for f in j.traza_decidir(
            j.ARBOL_TPM_100, profundidad=d, evaluar=j.EVAL_TPM)["filas"] if f["evento"] == "raiz"}
        jugada, _, nodos = j.decidir_con_corte_tpm(d)
        esperado.append((str(d), f"{w['I']} · {w['C']} · {w['D']}", jugada, str(nodos)))
    assert leido == esperado
    resp = _limpio(_respuesta(texto, "jue-c3-ej-cota"))
    assert int(re.search(r"suman los (\d+) nodos", resp)[1]) == j.decidir_con_corte_tpm(2)[2]
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[-1])
    assert [int(x) for x in re.search(r"genera (\d+), (\d+) y (\d+) nodos", llevarse).groups()] \
        == [j.decidir_con_corte_tpm(d)[2] for d in (1, 2, 3)]


def test_prosa_clase_3_p2_la_traza_con_huecos_y_su_respuesta():
    """#39 · El ejercicio «Completa la traza con der primero»: el orden sale
    del enunciado; las celdas sin «?» y la tabla de la respuesta, de
    filas_corte_tpm con ese orden (Ola 3: arbol de resultados)."""
    texto = _pagina(P2)
    ej = _bloque(texto, "jue-c3-ej-traza-d2")
    orden = _orden_de(re.search(r"otro orden: (\w+), (\w+), (\w+)", _limpio(ej)).groups())
    esperado = _esperado(j.filas_corte_tpm(2, orden=orden))
    _con_huecos(_filas(_tablas(ej)[0][1:]), esperado)
    resp = _respuesta(texto, "jue-c3-ej-traza-d2")
    assert _filas(_tablas(resp)[0][1:]) == esperado
    jugada, valor, _ = j.decidir_con_corte_tpm(2, orden=orden)
    assert re.search(r"Devuelve (\w+), con (\d+)", _limpio(resp)).groups() == (jugada, str(valor))


def test_prosa_clase_3_p2_ejercicio_final_empate_y_otra_eval():
    """#39 · El ejercicio final de «Cortar y evaluar» en el arbol de
    resultados (Ola 3; antes en el arbol base): el empate EVAL(C) = 60 (izq
    con el orden de la pagina, centro con R al reves, y la traza de este con
    d = 1), la variante EVAL(I) = 0 con d = 1, 2, 3 y los nodos 4, 11, 15.
    Los objetivos son los del original: un empate que decide el orden y una
    EVAL que solo cambia la jugada donde ese nodo es de corte."""
    texto = _pagina(P2)
    ej = _limpio(_bloque(texto, "jue-c3-ej-final-corte"))
    assert [int(x) for x in re.search(r"EVAL\(C\)=(\d+) en vez de (\d+)", ej).groups()] == [
        j.EVAL_TPM_EMPATE["C"], j.EVAL_TPM["C"]]
    pagina = _orden_de(re.search(r"el orden (\w+), (\w+), (\w+)", ej).groups())
    orden = _orden_de(re.search(r"al\s+revés: (\w+), (\w+), (\w+)", ej).groups())
    assert pagina == ["I", "C", "D"] and orden == pagina[::-1]
    assert [int(x) for x in re.search(r"EVAL\(I\)=(\d+) en vez de (\d+)", ej).groups()] == [
        j.EVAL_TPM_VARIANTE["I"], j.EVAL_TPM["I"]]
    resp = _respuesta(texto, "jue-c3-ej-final-corte")
    c = j.EVAL_TPM_EMPATE
    assert _filas(_tablas(resp)[0][1:]) == _esperado(
        j.filas_corte_tpm(1, orden=orden, evaluar=c))
    limpio = _limpio(resp)
    empate, resto = limpio.split("2. La variante.")
    variante_txt, costo = resto.split("3. El costo.")
    jugada, valor, _ = j.decidir_con_corte_tpm(1, evaluar=c)
    assert re.search(r"juega (\w+), con (\d+)", empate).groups() == (jugada, str(valor))
    jugada, valor, _ = j.decidir_con_corte_tpm(1, orden=orden, evaluar=c)
    assert re.search(r"Devuelve (\w+), con (\d+)", empate).groups() == (jugada, str(valor))
    assert jugada != j.decidir_con_corte_tpm(1, evaluar=c)[0]
    variante = [j.decidir_con_corte_tpm(d, evaluar=j.EVAL_TPM_VARIANTE) for d in (1, 2, 3)]
    assert [(a, int(v)) for a, v in re.findall(r"juega (izq|centro|der), con (-?\d+)", variante_txt)] \
        == [v[:2] for v in variante]
    # la variante solo cambia la jugada con d = 1 (I es nodo de corte solo ahi)
    assert [v[0] for v in variante] != [j.decidir_con_corte_tpm(d)[0] for d in (1, 2, 3)]
    assert [v[0] for v in variante[1:]] == [j.decidir_con_corte_tpm(d)[0] for d in (2, 3)]
    nodos = [int(x) for x in re.search(r"(\d+), (\d+) y (\d+) nodos en los dos casos",
                                       costo).groups()]
    assert nodos == [v[2] for v in variante] == [
        j.decidir_con_corte_tpm(d, orden=orden, evaluar=c)[2] for d in (1, 2, 3)]


# ---- p3 · mas alla del horizonte

def test_prosa_clase_3_p3_horizonte_y_quietud():
    """#39 · @jue-c3-horizonte-valores (copia de la tabla de p1), los valores
    con quietud −10, 2, 0, y el ejercicio de la posicion nueva (2, 2, 13, 2
    en seco; −10, 2, 0, 1 con quietud)."""
    texto = _pagina(P3)
    _revisa_tabla_de_profundidades(texto, "jue-c3-horizonte-valores")
    quieta = lambda t: [j.minimax_con_quietud(j.mover(t, m), "N", 0, 4)  # noqa: E731
                        for m in j.jugadas(t, "B", 4)]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-quietud"))
    assert [int(x) for x in re.search(r"Los valores son (-?\d+), (-?\d+) y (-?\d+)",
                                      resp).groups()] == quieta(j.POSICION_C3)
    ej = _bloque(texto, "jue-c3-ej-clasifica")
    nueva = _tablero(_tablas(ej)[0])
    nombres = [j.nombre_jugada(nueva, m, 4) for m in j.jugadas(nueva, "B", 4)]
    limpio = _limpio(ej)
    assert re.findall(_JUGADA, limpio.split("cuatro jugadas:")[1].split(".")[0]) == nombres
    assert [int(x) for x in re.search(r"valen (\d+), (\d+), (\d+) y (\d+)", limpio).groups()] \
        == [j.evaluar_peones(j.mover(nueva, m), 4) for m in j.jugadas(nueva, "B", 4)]
    con_quietud = quieta(nueva)
    dadas = {m: int(v) for m, v in re.findall(rf"({_JUGADA}) vale (-?\d+)", limpio)}
    assert dadas == {m: v for m, v in zip(nombres, con_quietud) if m in dadas} and dadas
    resp = _limpio(_respuesta(texto, "jue-c3-ej-clasifica"))
    m = re.search(r"Con quietud los valores son (-?\d+), (-?\d+), (-?\d+) y (-?\d+)", resp)
    assert [int(x) for x in m.groups()] == con_quietud


def test_prosa_clase_3_p3_quedarse_engana_si_todo_es_captura():
    """@jue-c3-quedarse-falla · quedarse (stand pat) no es una jugada legal:
    la posicion sale de las jugadas del texto, Blancas solo tiene capturas,
    Negras gana en la jugada siguiente, la quietud devuelve la EVAL (0) y el
    valor exacto es −100."""
    texto = _limpio(_bloque(_pagina(P3), "jue-c3-quedarse-falla"))
    camino = re.findall(_JUGADA, texto.split("Quedan")[0])
    t, turno = j.jugar_nombres(j.inicio(4), "B", camino, 4)
    assert turno == "B" and not j.ganador(t, turno, 4)
    lados = re.search(r"Quedan Blancas en ([^,]*(?:, [^,]*)*?), Negras en (.*?), y mueven", texto)
    casillas = lambda s: sorted(re.findall(r"[a-d][1-4]", s))  # noqa: E731
    assert casillas(lados[1]) == sorted(j.casilla(i, 4) for i, p in enumerate(t) if p == "B")
    assert casillas(lados[2]) == sorted(j.casilla(i, 4) for i, p in enumerate(t) if p == "N")
    propias = j.jugadas(t, "B", 4)
    dichas = re.search(rf"solo tiene dos jugadas, ({_JUGADA}) y ({_JUGADA})", texto).groups()
    assert list(dichas) == [j.nombre_jugada(t, m, 4) for m in propias]
    assert all(j.es_captura(t, m) for m in propias)
    # Tras cualquiera, Negras tiene una jugada que llega a la fila 1.
    assert all(any(j.ganador(j.mover(j.mover(t, m), r), "B", 4) == "N"
                   for r in j.jugadas(j.mover(t, m), "N", 4)) for m in propias)
    assert int(re.search(r"EVAL=(-?\d+)", texto)[1]) == j.evaluar_peones(t, 4)
    assert int(re.search(r"que valen (-?\d+)", texto)[1]) == \
        j.minimax_con_quietud(j.mover(t, propias[0]), "N", 0, 4) == \
        j.minimax_con_quietud(j.mover(t, propias[1]), "N", 0, 4)
    assert int(re.search(r"devuelve (-?\d+)", texto)[1]) == j.minimax_con_quietud(t, "B", 0, 4)
    assert int(re.search(r"100· ?V=(-?\d+)", texto)[1]) == 100 * j.valor(t, "B", n=4)
    assert j.minimax_con_quietud(t, "B", 0, 4) != 100 * j.valor(t, "B", n=4)


def test_prosa_clase_3_r3_quietud_evalua_el_corte_como_quedarse():
    """r3 · la definición no puede decir «en vez de evaluar ahí»: la quietud
    SÍ usa la EVAL del nodo de corte, como opción de quedarse (juegos.py:
    quieta() arranca en evaluar_peones). Stand pat va en ambos sentidos
    (MAX ≥ EVAL, MIN ≤ EVAL) y puede fallar también si toda jugada empeora;
    los jaques sin captura quedan fuera; el horizonte no siempre se mueve.
    Y en la p6, ū no «baja» monótono hacia μ."""
    p3 = " ".join(_pagina(P3).replace("\n> ", "\n").split())  # sin el «> » de los recuadros
    for viejo in ("En vez de evaluar ahí", "el corte ya no cae en medio de un intercambio",
                  "vale al menos la $\\mathrm{EVAL}$", "Falla si todas sus jugadas son",
                  "Los jaques no son capturas", "en un juego grande eso no pasa"):
        assert viejo not in p3, viejo
    for nuevo in ("No devuelve sin más la $\\mathrm{EVAL}$ del nodo de corte: la usa como opción "
                  "de **quedarse** y la compara con **las capturas**; cada captura sigue hasta "
                  "un final o una posición quieta.",
                  "**Qué significa.** Reduce los cortes a mitad de un intercambio.",
                  "al menos tan buena para quien mueve como quedarse: para MAX, "
                  "${\\geq \\mathrm{EVAL}}$; para MIN, ${\\leq \\mathrm{EVAL}}$.",
                  "Puede fallar si esa jugada no existe —por ejemplo, si todas son capturas— o "
                  "si toda jugada empeora su posición.",
                  "**Los jaques sin captura quedan fuera de esta versión**, que solo sigue "
                  "capturas",
                  "da un jaque tras otro, ninguno con captura,",
                  "en un juego grande no suele haber una profundidad práctica que lo logre en "
                  "toda posición."):
        assert nuevo in p3, nuevo
    # Lo que la prosa afirma, en juegos.py: en la posición de la clase tras
    # d2xc3 (no quieta), quedarse vale la EVAL del corte y la quietud la
    # compara con la captura: min(13, 0) = 0, no la EVAL en seco.
    nombres = {j.nombre_jugada(HORIZONTE, m, 4): m for m in j.jugadas(HORIZONTE, "B", 4)}
    corte = j.mover(HORIZONTE, nombres["d2xc3"])
    assert any(j.es_captura(corte, m) for m in j.jugadas(corte, "N", 4))  # no quieta
    capturas = [j.minimax_con_quietud(j.mover(corte, m), "B", 0, 4)
                for m in j.jugadas(corte, "N", 4) if j.es_captura(corte, m)]
    assert j.evaluar_peones(corte, 4) == 13 and capturas == [0]
    assert j.minimax_con_quietud(corte, "N", 0, 4) == min([13] + capturas) == 0
    nota = (UNIDAD / "A_notacion.md").read_text(encoding="utf-8")
    assert "seguir mirando solo capturas antes de evaluar" not in nota
    assert ("no devolver sin más la $\\mathrm{EVAL}$: usarla como opción de quedarse (una "
            "aproximación llamada *stand pat*) y compararla con las capturas") in nota
    p6 = " ".join(_pagina(P6).split())
    assert "Su $\\bar u$ baja hacia su $\\mu$" not in p6 and "El error costó" not in p6
    # Ola 3: la notación pasa a Q̂/Q_azar (plan §5.1) y el bono se reescribió
    # en seis bloques; la frase «se acerca a esa μ (al principio puede subir o
    # bajar)» ya no existe. Se conserva la prohibición en la notación nueva y
    # el ancla pasa a la definición de lo que estima el promedio.
    assert "baja hacia su $Q_{\\text{azar}}" not in p6
    assert ("**Qué significa.** Es el blanco del promedio: nadie lo ve, solo se ve "
            "$\\widehat Q(s,a)$.") in p6


# ---- p4 · jugar contra el reloj

def test_prosa_clase_3_p4_el_reloj_en_la_posicion():
    """#39 · La tabla de valores por profundidad (Ola 3: @jue-c3-reloj-por-d
    se archivó y su papel lo cumple @jue-c3-horizonte-valores, destinos R18),
    los 4, 12 y 33 nodos de la figura y del ejercicio de costo, y su suma (49)
    y repeticion (16)."""
    texto = _pagina(P4)
    _revisa_tabla_de_profundidades(texto, "jue-c3-horizonte-valores")
    nodos = [j.nodos_con_corte(j.POSICION_C3, "B", d, 4) for d in (1, 2, 3)]
    alt = _alt(texto, "jue-c3-fig-profundizacion")
    assert [int(x) for x in re.findall(r"(\d+) con d = \d", alt)] == nodos
    ej = _limpio(_bloque(texto, "jue-c3-ej-costo"))
    assert [int(x) for x in re.search(r"(\d+), (\d+) y (\d+) nodos", ej).groups()] == nodos
    # La version corta se pasa del limite: la ultima contra lo ya gastado.
    m = re.search(r"En la posición de la clase, (\d+) nodos contra (\d+)\.", _limpio(texto))
    assert m and (int(m[1]), int(m[2])) == (nodos[2], sum(nodos[:2]))
    resp = _limpio(_respuesta(texto, "jue-c3-ej-costo"))
    assert [int(x) for x in re.search(r"(\d+)\+(\d+)\+(\d+)= (\d+)", resp).groups()] == \
        nodos + [sum(nodos)]
    assert [int(x) for x in re.search(r"(?<![\d+])(\d+)\+(\d+)= (\d+)", resp).groups()] == \
        nodos[:2] + [sum(nodos[:2])]
    # 1/(B-1) con el crecimiento medido en el ultimo paso (33/12), no con el b
    # maximo: la cuenta es una guia que supone crecimiento parejo.
    b, _ = j.ramificacion_maxima(j.arbol_con_corte(j.POSICION_C3, "B", 3, 4))
    crece = F(nodos[2], nodos[1])
    guia = f"{float(1 / (crece - 1)):.2f}"
    medido = f"{float(F(sum(nodos[:2]), nodos[2])):.2f}"
    x = r"(\d+(?:\.\d+)?)"
    m = re.search(rf"por el máximo, b=(\d+) jugadas\. Con el crecimiento medido aquí en el último "
                  rf"paso, (\d+)/(\d+)={x}, da 1/\({x}-1\)≈{x}, cerca de lo medido, "
                  rf"(\d+)/(\d+)≈{x}", resp)
    assert m and m.groups() == (str(b), str(nodos[2]), str(nodos[1]), f"{float(crece):g}",
                                f"{float(crece):g}", guia, str(sum(nodos[:2])),
                                str(nodos[2]), medido)
    # Ola 3: el resumen ya no repite la cuenta 33/12 (vive en la respuesta de
    # arriba); dice lo repetido contra la ultima, sin poda, y con alfa-beta e
    # iterativa en el arbol de resultados y en la clase.
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[-1])
    m = re.search(r"sin poda, (\d+) nodos contra (\d+)\. Con alfa-beta y la jugada anterior "
                  r"primero: (\d+) contra (\d+) en el árbol de resultados, y (\d+) contra (\d+) "
                  r"en la clase", llevarse)
    tpm = j.tabla_nodos_generados_tpm()
    clase = j.tabla_nodos_generados()
    assert m and [int(v) for v in m.groups()] == [
        sum(nodos[:2]), nodos[2], j.iterativa_tpm()[1], sum(tpm["sin poda"]),
        sum(clase[("4x4", "iterativa")]), sum(nodos)]


def test_prosa_clase_3_p4_profundizar_sin_poda_en_t():
    """#39 · Profundizar sin poda en el arbol de resultados: la jugada lista,
    su valor y los nodos de cada busqueda, el 4 + 11 + 15 = 30 y el ejercicio
    de orden: el orden no cambia los nodos. Ola 3: @jue-c3-t-sin-poda se
    archivó (destinos R18); el ancla pasa a la lista de tres viñetas «En el
    árbol de resultados» y a la frase de la suma, con iterativa_sin_poda_tpm."""
    texto = _pagina(P4)
    corridas = j.iterativa_sin_poda_tpm()
    limpio = _limpio(texto)
    bloque = limpio.split("En el árbol de resultados, R prueba sus hijos")[1].split(
        "Las tres búsquedas generan")[0]
    vinetas = re.findall(r"- d=(\d)(.*?)genera (\d+) nodos", bloque)
    assert [int(d) for d, _, _ in vinetas] == [c[0] for c in corridas]
    for (d, cuerpo, nodos), (_, _, jugada, valor, generados) in zip(vinetas, corridas):
        assert int(nodos) == generados, d
        assert jugada in cuerpo and re.search(rf"(?<![\d-]){valor}(?!\d)", cuerpo), (d, cuerpo)
    m = re.search(r"generan (\d+)\+(\d+)\+(\d+)=(\d+) nodos", limpio)
    assert [int(x) for x in m.groups()] == [c[4] for c in corridas] + [
        sum(c[4] for c in corridas)]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-orden-sin-poda"))
    assert [int(x) for x in re.search(r"(\d+), (\d+) y (\d+)\.", resp).groups()] == [
        c[4] for c in j.iterativa_sin_poda_tpm(anterior_primero=True)]
    assert [c[2] for c in j.iterativa_sin_poda_tpm(anterior_primero=True)] == [
        c[2] for c in corridas]


_CAMINO_TPM = {"R": (), "I": (0,), "C": (1,), "D": (2,), "C1": (1, 0), "C2": (1, 1)}


def _hijos_con_nombre_tpm(traza):
    """Por fila de una traza en el arbol de resultados, el nombre del hijo que
    regresa: el nodo («C1») o la hoja por su nombre visible («c1a»), que la
    pagina escribe en vez de su valor (nombres_hojas_tpm). None si no regresa
    nadie."""
    hojas, vistas, res = j.nombres_hojas_tpm(), {}, []
    for f in traza["filas"]:
        if f["hijo"] is None:
            res.append(None)
        elif f["hijo"] in _CAMINO_TPM:
            res.append(f["hijo"])
        else:
            k = vistas.get(f["nodo"], 0)
            vistas[f["nodo"]] = k + 1
            res.append(hojas[_CAMINO_TPM[f["nodo"]] + (k,)])
    return res


def _filas_reloj_d3():
    """La busqueda con d = 3, centro primero, en las dos tablas de la pagina:
    (#, línea · pila, (α,β)) y (#, v, w, compara). Ola 3: en el arbol de
    resultados (traza_iterativa_tpm)."""
    t = j.traza_iterativa_tpm(3)
    donde, numeros, alfa_r = [], [], -INF
    for f, hijo in zip(t["filas"], _hijos_con_nombre_tpm(t)):
        n = str(f["n"])
        donde.append((n, f"{f['linea']} · {'›'.join(f['pila'])}",
                      f"({j.fmt_t(f['alfa'])},{j.fmt_t(f['beta'])})"))
        v = j.fmt_t(f["mejor_valor"] if f["nodo"] == "R" else f["v"])
        w = "" if f["w"] is None else f"{j.fmt_t(f['w'])} ({hijo})"
        compara = ""
        if f["evento"] == "regresa":
            es_max = len(f["pila"]) % 2 == 1
            signo, borde = ("≥", f["beta"]) if es_max else ("≤", f["alfa"])
            compara = f"{j.fmt_t(f['v'])}{signo}{j.fmt_t(borde)}: {'sí' if f['corta'] else 'no'}"
        elif f["evento"] == "raiz":
            compara = f"{j.fmt_t(f['w'])}>{j.fmt_t(alfa_r)}: {'sí' if f['mejora'] else 'no'}"
            alfa_r = f["mejor_valor"]
        numeros.append((n, v, w, compara))
    return t, _esperado(donde), _esperado(numeros)


def test_prosa_clase_3_p4_traza_de_la_busqueda_con_d_3():
    """#39 · Los tramos de la busqueda con d = 3 en el arbol de resultados:
    las tablas del tramo 1, el tramo 2 (sin id, entre el tramo 1 y el
    ejercicio), el tramo 3 con huecos y su respuesta, y los 12 nodos."""
    texto = _pagina(P4)
    t, donde, numeros = _filas_reloj_d3()
    sin_espacios = lambda filas: [tuple(c.replace(" ", "") for c in f) for f in filas]  # noqa: E731
    tramo_1 = len(_tabla(texto, "jue-c3-t-traza-d3-donde")) - 1
    assert sin_espacios(_filas(_tabla(texto, "jue-c3-t-traza-d3-donde")[1:])) == \
        sin_espacios(donde[:tramo_1])
    assert sin_espacios(_filas(_tabla(texto, "jue-c3-t-traza-d3-numeros")[1:])) == \
        sin_espacios(numeros[:tramo_1])
    entre = texto.split("{#jue-c3-t-traza-d3-numeros")[1].split("\n:::\n", 1)[1].split(
        "::: exercise {#jue-c3-ej-traza-d3")[0]
    tramo_2 = _tablas(entre)
    hasta = tramo_1 + len(tramo_2[0]) - 1
    assert sin_espacios(_filas(tramo_2[0][1:])) == sin_espacios(donde[tramo_1:hasta])
    assert sin_espacios(_filas(tramo_2[1][1:])) == sin_espacios(numeros[tramo_1:hasta])
    ej = _tablas(_bloque(texto, "jue-c3-ej-traza-d3"))
    _con_huecos(sin_espacios(_filas(ej[0][1:])), sin_espacios(donde[hasta:]))
    _con_huecos(sin_espacios(_filas(ej[1][1:])), sin_espacios(numeros[hasta:]))
    resp = _respuesta(texto, "jue-c3-ej-traza-d3")
    tablas = _tablas(resp)
    assert sin_espacios(_filas(tablas[0][1:])) == sin_espacios(donde[hasta:])
    assert sin_espacios(_filas(tablas[1][1:])) == sin_espacios(numeros[hasta:])
    m = re.search(r"Se generan (\d+) nodos: ([^.]*)\.", _limpio(resp))
    assert int(m[1]) == t["generados"]
    nombres = ["R"] + [f["nodo"] if f["evento"] == "entra" else h
                       for f, h in zip(t["filas"], _hijos_con_nombre_tpm(t))
                       if f["evento"] == "entra" or (h and h not in _CAMINO_TPM)]
    assert len(nombres) == len(t["orden_generados"])
    assert re.split(r", | y ", m[2]) == nombres


def test_prosa_clase_3_p4_iterativa_en_t_y_nodos_generados():
    """#39 · @jue-c3-t-iterativa, el «4, 9 y 12, que suman 25 / 30» y las dos
    tablas de nodos generados (arbol de resultados: 4, 11, 15 / 4, 9, 12 /
    4, 9, 12; posicion: 4, 12, 33 / 4, 12, 22 / 4, 10, 9), con sus totales.
    Ola 3: la parte del arbol base pasa al arbol de resultados (ARBOL_TPM)."""
    texto = _pagina(P4)
    esperado = []
    for i, (d, _, t) in enumerate(j.profundizacion_iterativa_t(j.ARBOL_TPM_100,
                                                                evaluar=j.EVAL_TPM)):
        hijos = []
        # Ola 3: «≤» marca lo que la tabla de transposicion guardaria como
        # techo (v ≤ α de entrada), como dice la pagina; en el arbol de
        # resultados I poda en su ultima hoja y devuelve una cota sin podar nada.
        clases = j.clases_transposicion(t)
        for k, f in enumerate(f for f in t["filas"] if f["evento"] == "raiz"):
            techo = f["hijo"] in clases and clases[f["hijo"]][3] == "techo"
            cota = "≤" if techo or f["estado"][f["hijo"]]["cota"] else ""
            nombre = f"**{f['hijo']}**" if not k else f["hijo"]
            hijos.append(f"{nombre} {cota}{j.fmt_t(f['w'])}")
        esperado.append((str(d), " · ".join(hijos), t["jugada"]))
    filas = _tabla(texto, "jue-c3-t-iterativa")[1:]
    assert [(f[0], f[1].replace("\u2212", "-"), f[2]) for f in filas] == [
        (a, b.replace("\u2212", "-"), c) for a, b, c in esperado]
    tpm = j.tabla_nodos_generados_tpm()
    tabla = j.tabla_nodos_generados()
    m = re.search(r"Nodos generados: (\d+), (\d+) y (\d+), que suman (\d+)\. Sin poda eran "
                  r"(\d+) \((\d+), (\d+)\s+y (\d+)\)", _limpio(texto))
    t_it, t_sp = tpm["iterativa"], tpm["sin poda"]
    assert [int(x) for x in m.groups()] == t_it + [sum(t_it), sum(t_sp)] + t_sp
    assert (t_it, sum(t_it)) == ([f[4] for f in j.iterativa_tpm()[0]], j.iterativa_tpm()[1])
    columnas = {"sin poda": "sin poda", "α-β fijo": "alfa-beta", "iterativa": "iterativa"}
    for ident, fuente in [("jue-c3-nodos-generados", tpm),
                          ("jue-c3-nodos-generados-posicion",
                           {k: tabla[("4x4", k)] for k in columnas.values()})]:
        filas = _tabla(texto, ident)
        claves = [columnas[_c(x)] for x in filas[0][1:]]
        leido = {k: [_n(f[i + 1]) for f in filas[1:]] for i, k in enumerate(claves)}
        assert leido == {k: fuente[k] + [sum(fuente[k])] for k in claves}, ident
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[-1])
    m = re.search(r"(\d+) contra (\d+) en el árbol de resultados, y (\d+) contra (\d+) en la "
                  r"clase", llevarse)
    assert [int(x) for x in m.groups()] == [sum(t_it), sum(t_sp),
                                            sum(tabla[("4x4", "iterativa")]),
                                            sum(tabla[("4x4", "sin poda")])]


def test_prosa_clase_3_p4_valor_piso_y_techo():
    """#39 · @jue-c3-transposicion-iterativa y el ejercicio con el orden fijo:
    la ventana, el v y la clase de cada nodo, de clases_transposicion, en el
    arbol de resultados (Ola 3)."""
    texto = _pagina(P4)
    nombre = {"exacto": "valor", "piso": "piso", "techo": "techo"}
    ventana = lambda a, b: f"({j.fmt_t(a)},{j.fmt_t(b)})"  # noqa: E731
    t = j.traza_iterativa_tpm(3)
    esperado = [(n, _c(ventana(a, b)), _c(j.fmt_t(v)), nombre[k])
                for n, (a, b, v, k) in j.clases_transposicion(t).items()]
    leido = [tuple(_c(x).replace(" ", "") for x in f)
             for f in _tabla(texto, "jue-c3-transposicion-iterativa")[1:]]
    assert leido == [tuple(c.replace(" ", "") for c in f) for f in esperado]
    fijo = j.clases_transposicion(j.traza_decidir(j.ARBOL_TPM_100, poda=True, profundidad=3,
                                                  evaluar=j.EVAL_TPM))
    ej = _limpio(_bloque(texto, "jue-c3-ej-clase"))
    vistos = re.findall(r"(I|C2|D) llega con \(([^)]*)\) y devuelve (-?\d+)", ej)
    assert len(vistos) == 3
    for n, v_ventana, v in vistos:
        a, b, valor, _ = fijo[n]
        assert (f"({v_ventana})".replace(" ", ""), int(v)) == (
            _c(ventana(a, b)).replace(" ", ""), valor), n
    resp = _limpio(_respuesta(texto, "jue-c3-ej-clase"))
    assert dict(re.findall(r"(I|C2|D): (valor|piso|techo)", resp)) == {
        n: nombre[fijo[n][3]] for n, _, _ in vistos}
    # Una entrada mas honda no da el valor con corte de esta busqueda.
    m = re.search(r"En el árbol de resultados, (I|C|D) vale (-?\d+) sin nada debajo, (-?\d+) "
                  r"con un nivel y (-?\d+) con dos", _limpio(texto))
    assert m and [int(m[2]), int(m[3]), int(m[4])] == [
        j.valor_con_corte_hijo_tpm(m[1], k) for k in (0, 1, 2)]
    assert len({m[2], m[3], m[4]}) == 3


def test_prosa_clase_3_p4_ejercicio_final_otro_orden_y_un_reloj():
    """#39 · El ejercicio final de «Hasta dónde mirar» en el arbol de
    resultados (Ola 3): el orden sale del enunciado; la tabla de la respuesta
    (4, 9, 12), el 25 igual que en la pagina, y lo que entrega cada reloj
    (10 y 20 nodos)."""
    texto = _pagina(P4)
    ej = _limpio(_bloque(texto, "jue-c3-ej-final-reloj"))
    acciones = list(re.search(r"A\(R\): (\w+), (\w+), (\w+)", ej).groups())
    corridas, entrega = j.iterativa_con_reloj_tpm(acciones)
    _, de_la_pagina = j.iterativa_con_reloj_tpm(["izq", "centro", "der"])
    assert int(re.search(r"con los (\d+) de la página", ej)[1]) == de_la_pagina["generados"]
    resp = _respuesta(texto, "jue-c3-ej-final-reloj")
    assert _filas(_tablas(resp)[0][1:]) == [
        (str(c["d"]), ", ".join(c["orden"]), c["jugada"], str(c["generados"])) for c in corridas]
    limpio = _limpio(resp)
    # Ola 3: en este arbol el otro orden no ahorra ni cuesta: «igual que en la
    # página» (antes «uno menos que los 25»).
    m = re.search(r"(\d+) nodos \((\d+), (\d+) y (\d+)\), igual que en la página", limpio)
    assert [int(x) for x in m.groups()] == [entrega["generados"]] + [
        c["generados"] for c in corridas]
    assert entrega["generados"] == de_la_pagina["generados"]
    assert entrega["jugada"] == de_la_pagina["jugada"]
    topes = [int(re.search(r"reloj de (\d+) nodos", ej)[1]),
             int(re.search(r"uno de (\d+)\?", ej)[1])]
    reloj = limpio.split("4. El reloj.")[1]
    segmentos = re.findall(r"Con (\d+) nodos:(.*?)(?=Con \d+ nodos:|$)", reloj, re.S)
    assert [int(t) for t, _ in segmentos] == topes
    for tope, seg in segmentos:
        _, e = j.iterativa_con_reloj_tpm(acciones, tope=int(tope))
        llega, tras = re.findall(r"a (\d+) tras (\w+)", seg)[-1]
        assert (int(llega), tras) == (e["generados"], e["despues_de"]), tope
        assert int(re.search(r"[Ll]a línea (\d+)", seg)[1]) == e["linea"], tope
        assert re.search(r"entrega (izq|centro|der)", seg)[1] == e["jugada"], tope
        assert int(re.search(r"de d=(\d+)", seg)[1]) == e["d"] - 1, tope


# ---- p5 · simular en vez de evaluar

def test_prosa_clase_3_p5_simulaciones_contra_corte_y_valor():
    """#39 · @jue-c3-simulaciones (0.21, 0.89, 0.15 / 2, 2, 13 / −1, +1, −1),
    @jue-c3-hexapawn-azar (7/36, 5/24 / 5/9, 3/4) y 17/18 y 29/48. Ola 3: en
    «Simular partidas» (Monte Carlo plano), con Q_azar en vez de μ."""
    texto = _pagina(P5)
    t = j.POSICION_C3
    jugadas = j.jugadas(t, "B", 4)
    esperado = {j.nombre_jugada(t, m, 4): (
        round(float(j.promedio_simulaciones(j.mover(t, m), "N", 4)), 2),
        _corte_en_la_posicion(1)[j.nombre_jugada(t, m, 4)],
        j.valor(j.mover(t, m), "N", n=4)) for m in jugadas}
    assert {_c(f[0]): tuple(_n(x) for x in f[1:])
            for f in _tabla(texto, "jue-c3-simulaciones")[1:]} == esperado
    h = j.inicio()
    ambos = {j.nombre_jugada(h, m): j.promedio_simulaciones(j.mover(h, m), "N")
             for m in j.jugadas(h, "B")}
    esperado = {k: (ambos[k], j.expectiminimax_rival_al_azar(j.mover(h, m), "N"))
                for k, m in zip(ambos, j.jugadas(h, "B"))}
    assert {_c(f[0]): tuple(_n(x) for x in f[1:])
            for f in _tabla(texto, "jue-c3-hexapawn-azar")[1:]} == esperado
    # V salio de la tabla (a 390 escondia la columna): la prosa la dice.
    assert {j.valor(j.mover(h, m), "N") for m in j.jugadas(h, "B")} == {-1}
    prosa = _limpio(texto)
    # Ola 3: la pregunta pasa a «Piensa» y la respuesta va en su primera frase.
    assert "las tres aperturas de hexapawn valen -1" in prosa
    assert "No: los tres son positivos" in prosa
    assert all(x > 0 for par in esperado.values() for x in par)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-promedio"))
    pares = [(F(a), F(b)) for a, b in re.findall(r"\((\d+/\d+)\+1\)/2=(\d+/\d+)", resp)]
    d2d3 = j.promedio_simulaciones(j.mover(t, jugadas[1]), "N", 4)
    assert pares == [(d2d3, (d2d3 + 1) / 2), (ambos["b1-b2"], (ambos["b1-b2"] + 1) / 2)]


def test_prosa_clase_3_p5_la_vuelta_de_mcts():
    """#39 · La vuelta a mano de «MCTS con UCT» (Ola 3: pasa de «Simular» a
    P5b y de G/N a N y V̂, plan §5.1): el titulo (N 4 → N 5), el alt de la
    figura, la tabla antes/después del camino, lo que queda fuera, N(R) como
    suma de sus hijos, y la respuesta con U = −1. Cifras de mcts_vuelta leidas
    como (N, V̂) con mcts_nv."""
    texto = _pagina(P5b)
    gana = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    pierde = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=-1)
    antes = j.mcts_nv(gana["antes"])
    despues, despues_p = j.mcts_nv(gana["despues"]), j.mcts_nv(pierde["despues"])
    camino = gana["camino"] + ["nuevo"]
    m = re.search(r"la raíz pasa de N (\d+) a N (\d+)", _titulo(texto, "jue-c3-fig-mcts"))
    assert (int(m[1]), int(m[2])) == (antes["r"][0], despues["r"][0])
    v = lambda q: f"{float(q):+.2g}" if q else "0"  # noqa: E731
    alt = _alt(texto, "jue-c3-fig-mcts")
    a_sel = next(n for n in gana["puntajes"]["r"] if n in camino)
    b_sel = next(n for n in gana["puntajes"]["a"] if n in camino)
    m = re.search(r"desde la raíz, N (\d+) y V̂ (\S+), MAX baja al hijo de N (\d+) y V̂ (\S+); "
                  r"ahí MIN baja al de N (\d+) y V̂ (\S+)", alt)
    assert m and (int(m[1]), F(m[2]), int(m[3]), round(float(F(m[4])), 2), int(m[5]),
                  F(m[6])) == (antes["r"][0], antes["r"][1], antes[a_sel][0],
                               round(float(antes[a_sel][1]), 2), antes[b_sel][0],
                               antes[b_sel][1])
    m = re.search(r"la raíz pasa a N (\d+) y V̂ ([+-]?\d+(?:\.\d+)?)", alt)
    assert m and (int(m[1]), F(m[2])) == despues["r"] and v(despues["r"][1]) == m[2]
    limpio = _limpio(texto)
    tabla = limpio.split("Pasos 3 a 5")[1].split("Cada pago mueve")[0]
    filas = re.findall(r"\| (R|a|a2|nuevo) \| (?:(\d+), (-?\d+(?:/\d+)?)|—) \| "
                       r"(\d+), ([+-]?\d+(?:\.\d+)?(?:/\d+)?) \|", tabla)
    nombre = {"r": "R"}
    assert [f[0] for f in filas] == [nombre.get(n, n) for n in camino]
    for (n, na, va, nd, vd), clave in zip(filas, camino):
        if clave in antes:
            assert (int(na), F(va)) == antes[clave], n
        assert (int(nd), F(vd)) == despues[clave], n
    fuera = [n for n in j.MCTS_ARBOL if n not in camino]
    m = re.search(r"Fuera del camino, (\w+) y (\w+) no cambian", limpio)
    assert sorted(m.groups()) == sorted(fuera)
    assert all(despues[n] == antes[n] for n in fuera)
    m = re.search(r"N\(R\)=(\d+), suma (-?\d+)", limpio)
    hijos = [n for n, (p, _, _) in j.MCTS_ARBOL.items() if p == "r"]
    assert int(m[1]) == antes["r"][0] == sum(antes[h][0] for h in hijos)
    assert int(m[2]) == antes["r"][0] * antes["r"][1]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-retro"))
    uno = resp.split(" 2. ")[0]
    m = re.search(r"R: N=(\d+), suma (-?\d+); a: N=(\d+), suma (-?\d+), \\widehat V=(-?\d+); "
                  r"a2: N=(\d+), \\widehat V=(-?\d+); el nuevo: N=(\d+), \\widehat V=(-?\d+)", uno)
    r, a, a2, nuevo = (despues_p[n] for n in ("r", "a", "a2", "nuevo"))
    assert m and [F(x) for x in m.groups()] == [
        r[0], r[0] * r[1], a[0], a[0] * a[1], a[1], a2[0], a2[1], nuevo[0], nuevo[1]]
    m = re.search(r"\\widehat V\(R\)=(-?\d+/\d+)=(-?\d+(?:\.\d+)?)\. Antes de la vuelta valía "
                  r"(-?\d+(?:\.\d+)?)", resp)
    assert m and F(m[1]) == F(m[2]) == r[1] and F(m[3]) == antes["r"][1]


def test_prosa_clase_3_p5_uct_en_el_ejercicio():
    """#39 · El ejercicio de MCTS (Ola 3: en P5b, con Q̂ en vez de ū): los
    datos x, y, z; ln 100 ≈ 4.61; los bonos 0.28, 0.39, 0.68; los puntajes
    0.78, 0.99, 0.88; seleccion y, entrega x. El resumen ya no repite el
    puntaje de la seleccion: su ancla pasa a las cifras de la corrida del
    arbol de resultados que si cita (izq vuelve en la 13; der hasta la 17,
    centro desde la 18), de uct_tpm."""
    import math
    texto = _pagina(P5b)
    ej = _limpio(_bloque(texto, "jue-c3-ej-mcts"))
    datos = {k: (int(n), F(u)) for k, n, u in re.findall(
        r"([xyz]): N=(\d+) visitas, \\widehat Q=(\d+(?:\.\d+)?)", ej)}
    assert datos == j.EJERCICIO_MCTS
    total = sum(n for n, _ in datos.values())
    assert int(re.search(r"Tras (\d+) vueltas", ej)[1]) == total
    ln = float(re.search(r"\\ln (\d+)≈(\d+(?:\.\d+)?)", ej)[2])
    assert ln == round(math.log(total), 2)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-mcts"))
    puntajes = j.uct_ejercicio(c=1)
    filas = re.findall(r"([xyz])&:\\ (\d+(?:\.\d+)?)\+\\sqrt(\d+(?:\.\d+)?)/(\d+)\\\\ &≈(\d+(?:\.\d+)?)\+(\d+(?:\.\d+)?)=(\d+(?:\.\d+)?)",
                       resp)
    assert [f[0] for f in filas] == list(datos)
    for k, u, ln_, n, u2, bono, puntaje in filas:
        assert F(u) == F(u2) == datos[k][1] and float(ln_) == ln and int(n) == datos[k][0], k
        assert float(bono) == round(j.mcts_puntaje(0, datos[k][0], total, 1), 2), k
        assert float(puntaje) == round(puntajes[k], 2), k
    assert re.search(r"baja por ([xyz])", resp)[1] == max(puntajes, key=puntajes.get)
    assert re.search(r"1\. ([xyz]):", resp)[1] == j.mas_simulada(datos)
    resumen = _limpio(texto[texto.index("## Lo que hay que llevarse"):])
    corrida = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    vuelve = [i + 1 for i, c in enumerate(corrida["caminos"]) if c[1] == (0,)][1]
    desde = j.vuelta_desde_la_que_tpm(1, j.SEMILLA_TPM)
    m = re.search(r"izq vuelve en la vuelta (\d+); UCT entrega der hasta la (\d+) y centro "
                  r"desde la (\d+)", resumen)
    assert m and [int(x) for x in m.groups()] == [vuelve, desde - 1, desde]
    assert corrida["mas_simulada"][desde - 2] == "der"


# ---- cifras de respuestas que ninguna otra prueba leia (r2, correccion §6)

def test_prosa_clase_3_p1_las_jugadas_tras_dos_avances():
    """El tablero del ejercicio sale de b1-b2, c4-c3; la respuesta nombra
    A(s) completo y su unica captura."""
    texto = _pagina(P1)
    ej = _bloque(texto, "jue-c3-ej-inicio")
    tablero, turno = j.jugar_nombres(j.inicio(4), "B", ["b1-b2", "c4-c3"], 4)
    assert _tablero(_tablas(ej)[0]) == tablero and turno == "B"
    nombres = [j.nombre_jugada(tablero, m, 4) for m in j.jugadas(tablero, "B", 4)]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-inicio"))
    uno, dos = resp.split(" 2. ", 1)
    assert sorted(re.findall(r"[a-d][1-4][-x][a-d][1-4]", uno)) == sorted(nombres)
    assert uno.startswith("1. Cinco:") and len(nombres) == 5
    capturas = [m for m in nombres if "x" in m]
    assert dos.startswith("Una:") and re.findall(r"[a-d][1-4]x[a-d][1-4]", dos)[0] == capturas[0]
    assert len(capturas) == 1


def test_prosa_clase_3_p2_que_linea_valora_cada_estado():
    """@jue-c3-ej-hoja: EVAL 0 tras d2xc3 b4xc3; 100 tras d2-d3 a4-a3 d3-d4
    (final); EVAL 2 de ese final si la linea 9 fuera primero."""
    resp = _limpio(_respuesta(_pagina(P2), "jue-c3-ej-hoja"))
    t1, turno1 = j.jugar_nombres(j.POSICION_C3, "B", ["d2xc3", "b4xc3"], 4)
    assert j.ganador(t1, turno1, 4) is None
    t2, turno2 = j.jugar_nombres(j.POSICION_C3, "B", ["d2-d3", "a4-a3", "d3-d4"], 4)
    assert j.ganador(t2, turno2, 4) == "B"
    evals = [int(x) for x in re.findall(r"EVAL=(-?\d+)", resp)]
    assert evals == [j.evaluar_peones(t1, 4), j.evaluar_peones(t2, 4)]
    d = j.desglose_eval(t2, 4)
    assert re.search(r"avance (\d+) contra (\d+)", resp).groups() == (
        str(d["avance_b"]), str(d["avance_n"]))
    assert d["peones_b"] == d["peones_n"] == 3 and "tres peones por lado" in resp


def test_prosa_clase_3_p5_dos_promedios_y_otras_formas_del_puntaje():
    """@jue-c3-ej-cinco (0.2, −0.2, mueve 0.4; Ola 3: con Q̂, en «Simular») y
    la frase de @jue-c3-resp-mcts (en P5b): con c = √2 la seleccion iria a z,
    por poco (1.160 contra 1.154), y con c = 2√2 con holgura (2.12 contra
    1.71). «Con G/N…» se retira de la pagina (plan §5.1 elimina G/N); la
    fuente con victorias=True se sigue comprobando abajo."""
    import math
    texto = _pagina(P5)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-cinco"))
    ganadas = [(3, 2), (2, 3)]
    leidos = re.findall(r"\\widehat Q=\((\d)-(\d)\)/(\d)=(-?\d+(?:\.\d+)?)", resp)
    assert [(int(g), int(p)) for g, p, _, _ in leidos] == ganadas
    for g, p, n, u in leidos:
        assert int(n) == int(g) + int(p) and F(u) == F(int(g) - int(p), int(n))
    salto = F(re.search(r"promedio (\d+(?:\.\d+)?)", resp)[1])
    assert salto == abs(F(leidos[0][3]) - F(leidos[1][3]))
    mcts = _limpio(_respuesta(_pagina(P5b), "jue-c3-ej-mcts"))
    m = re.search(r"Con c=\\sqrt2 la selección ya iría a ([xyz]), por poco: (\d+\.\d+) contra "
                  r"(\d+\.\d+)\. Con c=2\\sqrt2, con holgura: (\d+\.\d+) contra (\d+\.\d+)", mcts)
    assert m and m[1] == "z"
    for c, (a, b) in ((math.sqrt(2), (m[2], m[3])), (j.C_TEORIA, (m[4], m[5]))):
        p = j.uct_ejercicio(c=c)
        orden = sorted(p.values(), reverse=True)
        decimales = len(a.split(".")[1])
        assert max(p, key=p.get) == "z"
        assert [round(x, decimales) for x in orden[:2]] == [float(a), float(b)], c
    for puntajes in (j.uct_ejercicio(c=1, victorias=True), j.uct_ejercicio(c=math.sqrt(2))):
        assert max(puntajes, key=puntajes.get) == "z"


def test_prosa_clase_3_p3_lo_que_queda_detras_con_d_2():
    """@jue-c3-resp-detras: con d = 2 el corte cae en las dos respuestas de
    Negras a d2-d3, con su EVAL; detras, la jugada que llega a la fila 4."""
    resp = _limpio(_respuesta(_pagina(P3), "jue-c3-ej-detras"))
    rama = next(h for h in j.arbol_con_corte(j.POSICION_C3, "B", 2, 4)["hijos"]
                if h["jugada"] == "d2-d3")
    respuestas = [h["jugada"] for h in rama["hijos"]]
    assert re.findall(r"[a-d][1-4]-[a-d][1-4]", resp.split("Esos")[0])[1:] == respuestas
    evals = {h["valor"] for h in rama["hijos"]}
    assert all(not h["final"] for h in rama["hijos"]) and len(evals) == 1
    v = evals.pop()
    assert f"EVAL={v} los dos" in resp and f"min({v},{v})={v}" in resp
    assert rama["valor"] == v
    profunda = next(h for h in j.arbol_con_corte(j.POSICION_C3, "B", 3, 4)["hijos"]
                    if h["jugada"] == "d2-d3")
    ganadoras = {h["jugada"] for r in profunda["hijos"] for h in r["hijos"] if h["final"]}
    assert re.search(r"Detrás queda ([a-d][1-4]-[a-d][1-4])", resp)[1] in ganadoras


# --------------------------- clase 3, p6: de donde sale el bono (UCB) ---
#
# Escala ±1 de la p5. Cada cifra que la p6 va a citar, fijada en la fuente.
# Las que se escriben a mano aqui (1.92, 0.68, 83/10…) se comprobaron con la
# formula cerrada antes de fijarlas; las simulaciones, contra la probabilidad
# exacta de la binomial.

import math as _m


def test_clase_3_p6_hoeffding_margen_y_bono():
    # La cota en la escala ±1: e^(−Nε²/2); con N = 100, ε = 0.2 da e^(−2).
    assert _m.isclose(j.cota_hoeffding(100, 0.2), _m.exp(-2))
    assert j.cota_hoeffding(0, 0.5) == 1
    # El margen despeja la cota: con ese ε la cota vale justo δ.
    for delta, n in ((0.05, 30), (0.01, 10), (1e-8, 60)):
        assert _m.isclose(j.cota_hoeffding(n, j.margen(delta, n)), delta)
    assert round(j.margen(0.05, 30), 2) == 0.45
    # δ = N(s)^−4 ⇒ ε = 2√2·√(ln N(s)/N(s')): el bono con c = 2√2.
    assert j.C_TEORIA == 2 * _m.sqrt(2)
    for n_padre, n in ((100, 10), (100, 30), (100, 60), (5, 1), (10_000, 7)):
        assert _m.isclose(j.bono_ucb(n_padre, n), j.margen(n_padre ** -4, n))
        assert _m.isclose(j.bono_ucb(n_padre, n),
                          _m.sqrt(8 * _m.log(n_padre) / n))
    # Los micros: N(s) = 100 y N(s') = 10, 30, 60, con c = 2√2 y con c = 1.
    assert [round(j.bono_ucb(100, n), 2) for n in (10, 30, 60)] == [1.92, 1.11, 0.78]
    assert [round(j.bono_ucb(100, n, c=1), 2) for n in (10, 30, 60)] == [0.68, 0.39, 0.28]
    # El de c = 1 es el de la p5 (mcts_puntaje con ū = 0).
    for n in (10, 30, 60):
        assert j.bono_ucb(100, n, c=1) == j.mcts_puntaje(0, n, 100, 1)
    assert j.bono_ucb(100, 0) == j.INF


def test_clase_3_p6_la_escala_pm1_con_2_raiz_2_ordena_como_g_n_con_raiz_2():
    """ū = 2·(G/N) − 1, y el bono de ū con 2√2 es el doble del de G/N con √2:
    el puntaje de ū es 2·(puntaje de G/N) − 1. Mismo orden, misma eleccion."""
    con_u = j.puntajes_ucb(j.EJERCICIO_MCTS)
    con_g = j.uct_ejercicio(c=_m.sqrt(2), victorias=True)
    for k in con_u:
        assert _m.isclose(con_u[k], 2 * con_g[k] - 1), k
    assert sorted(con_u, key=con_u.get) == sorted(con_g, key=con_g.get) == ["x", "y", "z"]
    # Puntajes del ejercicio de la p5 con c = 2√2: la seleccion cambia de y
    # (c = 1, la p5) a z.
    assert {k: round(v, 2) for k, v in con_u.items()} == {"x": 1.28, "y": 1.71, "z": 2.12}
    assert j.mejor(con_u) == "z"
    assert j.mejor(j.puntajes_ucb(j.EJERCICIO_MCTS, c=1)) == "y"
    assert j.puntajes_ucb(j.EJERCICIO_MCTS, c=1) == j.uct_ejercicio(c=1)


def test_clase_3_p6_un_nodo_de_min():
    """MIN es optimista desde su lado: −ū + bono. Con c = 2√2 elige r, la poco
    probada aunque para MIN sea la peor; con c = 1, p. Se entrega p."""
    teoria = j.puntajes_ucb(j.EJEMPLO_MIN, mueve="MIN")
    p5 = j.puntajes_ucb(j.EJEMPLO_MIN, c=1, mueve="MIN")
    assert sum(n for n, _ in j.EJEMPLO_MIN.values()) == 50
    assert {k: round(v, 2) for k, v in teoria.items()} == {"p": 1.22, "q": 1.15, "r": 2.3}
    assert {k: round(v, 2) for k, v in p5.items()} == {"p": 0.56, "q": 0.24, "r": 0.49}
    # Cada ū sale de partidas enteras con U = ±1 (r2: q con N = 15 y ū = 0
    # pedia 7.5 victorias).
    assert [j.victorias_de(n, u) for n, u in j.EJEMPLO_MIN.values()] == [12, 10, 3]
    import pytest
    with pytest.raises(ValueError):
        j.victorias_de(15, 0)
    # r3 · N(s′) tiene que ser un entero positivo (0 partidas daba G = 0).
    for n_malo in (0, -4, 2.0, F(4), True):
        with pytest.raises(ValueError):
            j.victorias_de(n_malo, 0)
    # regreso_de_atoradas razona con x la mejor y primera en desempates:
    # solo vale para MUS_HILO.
    with pytest.raises(ValueError):
        j.regreso_de_atoradas(mus={"y": F(3, 10), "x": F(3, 5), "z": F(-1, 5)})
    with pytest.raises(ValueError):
        j.regreso_de_atoradas(mus={"x": F(1, 5), "y": F(3, 10), "z": F(-1, 5)})
    assert (j.mejor(teoria), j.mejor(p5), j.mas_simulada(j.EJEMPLO_MIN)) == ("r", "p", "p")
    # Sin bono, MIN iria a la de menor ū: p.
    assert j.mejor(j.puntajes_ucb(j.EJEMPLO_MIN, c=0, mueve="MIN")) == "p"


def test_clase_3_p6_el_hilo_y_el_atoramiento():
    """x es la mejor de verdad (μ = 0.6); con la semilla 36, «siempre el mejor
    promedio» pierde la unica prueba de x y de y y se queda en z para siempre."""
    assert j.MUS_HILO == {"x": F(3, 5), "y": F(3, 10), "z": F(-1, 5)}
    assert max(j.MUS_HILO, key=j.MUS_HILO.get) == j.mas_simulada(j.EJERCICIO_MCTS) == "x"
    assert j.prob_gana(j.MUS_HILO["x"]) == F(4, 5)
    filas = j.filas_bandido("mejor_promedio", j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA)
    assert "".join(f["jugada"] for f in filas) == "xyzzzzzzzzzz"
    assert [f["U"] for f in filas] == [-1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1]
    assert [f["u"]["z"] for f in filas[2:]] == [
        1, 0, F(-1, 3), F(-1, 2), F(-1, 5), F(-1, 3), F(-1, 7), 0, F(-1, 9), 0]
    assert filas[-1]["N"] == {"x": 1, "y": 1, "z": 10}
    assert filas[-1]["u"] == {"x": -1, "y": -1, "z": 0}
    b = j.bandido("mejor_promedio", j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA)
    assert b["arrepentimiento"][-1] == F(83, 10)          # 0.3 + 0.8·10
    # Para siempre: x y y quedan en ū = −1, el minimo, y z ya gano una vez.
    assert j.bandido("mejor_promedio", j.MUS_HILO, 1000, j.SEMILLA_ATORA)["N"] == {
        "x": 1, "y": 1, "z": 998}
    # La misma suerte con UCB (c = 2√2): vuelve a x en la vuelta 6.
    ucb = j.filas_bandido("ucb", j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA)
    assert "".join(f["jugada"] for f in ucb) == "xyzzzxyxyxyx"
    assert [f["U"] for f in ucb[:5]] == [f["U"] for f in filas[:5]]
    assert ucb[-1]["N"] == {"x": 5, "y": 4, "z": 3}
    assert j.bandido("ucb", j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA)[
        "arrepentimiento"][-1] == F(18, 5)


def test_clase_3_p6_las_reglas_hacen_lo_que_dicen():
    # Todas prueban cada jugada una vez, en orden, antes de comparar.
    for regla in j.REGLAS_BANDIDO:
        for semilla in (1, 2, 3):
            assert j.bandido(regla, j.MUS_HILO, 3, semilla)["elecciones"] == ["x", "y", "z"]
    # «Siempre el mejor promedio» no se mueve de una jugada si su ū es el mayor.
    for semilla in range(1, 30):
        f = j.filas_bandido("mejor_promedio", j.MUS_HILO, 40, semilla)
        for antes, ahora in zip(f[2:], f[3:]):
            u = antes["u"]
            assert ahora["jugada"] == max(u, key=u.get), (semilla, ahora["vuelta"])
    # «A veces al azar»: cerca de una vuelta de cada diez va al azar, asi que
    # z (la peor) se elige al menos ~1/30 de las vueltas, aunque tarde.
    b = j.bandido("a_veces_al_azar", j.MUS_HILO, 30_000, 5)
    assert 0.025 < b["N"]["z"] / 30_000 < 0.045
    # UCB con c = 0 es «siempre el mejor promedio».
    for semilla in (1, 36):
        assert (j.bandido("ucb", j.MUS_HILO, 200, semilla, c=0)["elecciones"]
                == j.bandido("mejor_promedio", j.MUS_HILO, 200, semilla)["elecciones"])
    # La suerte es de la jugada, no de la regla: la k-esima vez que se elige x
    # da lo mismo con cualquier regla.
    def de_x(regla):
        b = j.bandido(regla, j.MUS_HILO, 300, 7)
        return [r for a, r in zip(b["elecciones"], b["resultados"]) if a == "x"]
    a, u = de_x("a_veces_al_azar"), de_x("ucb")
    k = min(len(a), len(u))
    assert k > 20 and a[:k] == u[:k]


def test_clase_3_p6_frecuencia_contra_la_cota():
    """La figura jue-c3-hoeffding: jugada y (μ = 0.3), ε = 0.2, 20 000 tiradas
    de 200 simulaciones. Cada frecuencia queda bajo la cota y cerca de la
    probabilidad exacta (binomial)."""
    t = j.tabla_hoeffding()
    assert (j.MU_HOEFFDING, j.EPS_HOEFFDING) == (j.MUS_HILO["y"], F(1, 5))
    assert [t[n][0] for n in (10, 50, 100, 200)] == [
        F(2469, 10000), F(1429, 20000), F(241, 10000), F(11, 5000)]
    assert [round(t[n][1], 2) for n in (10, 50, 100, 200)] == [0.82, 0.37, 0.14, 0.02]
    reps = j.REPS_HOEFFDING
    for n, (frec, cota) in t.items():
        assert frec <= cota, n
        exacta = j.prob_desvio_exacta(j.MU_HOEFFDING, n, j.EPS_HOEFFDING)
        error = _m.sqrt(float(exacta) * (1 - float(exacta)) / reps)
        assert abs(float(frec - exacta)) <= 5 * error + 1e-9, n
    # La exacta a mano en n = 1: ū = −1 ≤ 0.1 cuando sale −1, Pr = 0.35.
    assert j.prob_desvio_exacta(F(3, 10), 1, F(1, 5)) == F(7, 20)
    # ū ≤ μ − ε es «a lo mas»: en n = 10, ū = 0.1 cuenta (0.3 − 0.2 exacto).
    assert j._umbral(0.3, 0.2, 10) == 1 and j._umbral(F(3, 10), F(1, 5), 10) == 1
    # Una sola n, otra semilla: tambien cerca de la exacta.
    una = j.frecuencia_desvio(F(3, 10), 50, F(1, 5), 4000, 3)
    exacta = float(j.prob_desvio_exacta(F(3, 10), 50, F(1, 5)))
    assert abs(float(una) - exacta) < 5 * _m.sqrt(exacta * (1 - exacta) / 4000)


def test_clase_3_p6_la_convergencia_del_bandido():
    """La figura jue-c3-bandido: 40 corridas de 10 000 vueltas por regla."""
    t = j.tabla_bandido()
    mp, az, ucb = (t[r] for r in j.REGLAS_BANDIDO)
    fin = max(j.MARCAS_BANDIDO)
    assert {r: round(t[r][fin], 2) for r in t} == {
        "mejor_promedio": 0.85, "a_veces_al_azar": 0.93, "ucb": 0.94, "ucb_c1": 0.99}
    # La c de la pagina 5 explora menos: en este bandido llega antes y mas alto.
    c1 = t["ucb_c1"]
    assert c1[fin] > ucb[fin] and c1[1000] > ucb[1000]
    # UCB empieza abajo (explora) y termina arriba; sube en cada marca.
    assert ucb[10] < az[10] and ucb[10] < mp[10] and ucb[fin] > az[fin] > mp[fin]
    marcas = j.MARCAS_BANDIDO
    assert all(ucb[a] < ucb[b] for a, b in zip(marcas, marcas[1:]))
    # «Siempre el mejor promedio» se aplana: entre 1000 y 10 000 casi no sube.
    assert mp[fin] - mp[1000] < 0.01
    # «A veces al azar» no pasa de 0.9 + 0.1/3: sigue tirando al azar.
    assert az[fin] < 0.9 + 0.1 / 3


def test_clase_3_p6_c_es_una_perilla():
    """Los valores del deslizador de c del interactivo (0, 1, 2√2, 5) y la
    respuesta del Pruebalo del notebook: en este bandido c = 1 llega mas alto
    que la teoria; c = 0 es «siempre el mejor promedio»."""
    fin = max(j.MARCAS_BANDIDO)
    f = {c: j.fraccion_en_la_mejor("ucb", j.MUS_HILO, j.MARCAS_BANDIDO,
                                   j.CORRIDAS_BANDIDO, c)[fin]
         for c in (0, 1, None, 5)}
    assert {c: round(v, 2) for c, v in f.items()} == {0: 0.85, 1: 0.99, None: 0.94, 5: 0.87}
    assert f[0] == j.tabla_bandido()["mejor_promedio"][fin]
    # Con c = 1 y la semilla del micro, UCB vuelve a x en la vuelta 7.
    assert "".join(j.bandido("ucb", j.MUS_HILO, 12, j.SEMILLA_ATORA, c=1)[
        "elecciones"]) == "xyzzzzxxxxxx"


# ------------------- clase 3, p6: la prosa de «De donde sale el bono» ---
#
# #39 para la p6: cada cifra que la pagina escribe se lee de la prosa (por id
# de tabla, figura, ejercicio o respuesta, o por la seccion «## n ·») y se
# compara con la funcion de juegos.py que la calcula. Los datos de entrada
# (μ, N, ū, δ, N(s)) tambien se leen del enunciado; las cifras de dos
# decimales se comparan como texto, con el formato con que la pagina las
# imprime («2.10», no 2.1). Los ejes de las figuras vienen de gen_juegos.

P6 = "5_de_donde_sale_el_bono.md"
_NUM = r"[+-]?\d+(?: \d{3})*(?:\.\d+)?"
_PALABRAS = {"una": 1, "tres": 3, "diez": 10, "doble": 2, "la mitad": F(1, 2),
             "un tercio": F(1, 3)}


def _x(s):
    """«1 000» → 1000, «0.6» → F(3, 5), «-1/3» → F(-1, 3), «una» → 1."""
    s = s.strip()
    if s in _PALABRAS:
        return F(_PALABRAS[s])
    return F(s.replace(" ", "").lstrip("+"))


def _d(x, k=2):
    return f"{float(x):.{k}f}"


def _pc(x):
    """Una probabilidad como la imprime la pagina: «24.7 %»."""
    return f"{100 * float(x):.1f} %"


def _seccion(texto, n):
    m = re.search(rf"^## {n} ·.*?$(.*?)(?=^## )", texto, re.M | re.S)
    assert m, f"no encuentro la seccion {n}"
    return _limpio(m.group(1))


def _llevarse(texto):
    return _limpio(texto[texto.index("## Lo que hay que llevarse"):])


def _ln(texto):
    """{n: «ln n» como lo escribe el texto}: \\ln5≈1.61 → {5: "1.61"}."""
    return {int(n): v for n, v in re.findall(r"\\ln ?(\d+)≈(\d+\.\d+)", texto)}


def _c_de(s):
    """La c de la pagina: «2\\sqrt2» es la de la teoria (None en juegos.py)."""
    return None if s.replace(" ", "") in ("2\\sqrt2", "2√2") else _x(s)


def _corrida(regla, c=None):
    return j.filas_bandido(regla, j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA, c)


def test_prosa_clase_3_p6_las_tres_jugadas_y_la_corrida_que_se_atora():
    """#39 · Bloque 1 (Ola 3: el bono en seis bloques, Q_azar y Q̂ en vez de μ
    y ū): la tabla de esperanzas (0.6, 0.3, −0.2; 0.80, 0.65, 0.40); las tres
    primeras vueltas de la semilla fija; @jue-c3-ej-atora (Q̂ = −1, −1, +1;
    z; 998 de 1000) y el resumen. Se retiran «La mejor es x, la que el
    ejercicio de MCTS entregaba» y «x vale de verdad μ…» del viejo §2: el
    bloque 1 ya no los dice (destinos D.2.1, §6.4)."""
    texto = _pagina(P6)
    uno = _seccion(texto, 1)
    filas = re.findall(rf"\| ([xyz]) \| ({_NUM}) \| ({_NUM}) \|", uno)
    mus = {k: _x(q) for k, q, _ in filas}
    assert mus == j.MUS_HILO
    assert {k: _x(p) for k, _, p in filas} == {k: j.prob_gana(mus[k]) for k in mus}
    assert all(p == _d(j.prob_gana(mus[k])) for k, _, p in filas)
    corrida = _corrida("mejor_promedio")
    m = re.search(r"Con la semilla (\d+), las tres primeras vueltas salen así: (.*?)\.", uno)
    assert int(m[1]) == j.SEMILLA_ATORA
    assert re.findall(r"([xyz]) (pierde|gana)", m[2]) == [
        (f["jugada"], "gana" if f["U"] == 1 else "pierde") for f in corrida[:3]]
    ej = _limpio(_bloque(texto, "jue-c3-ej-atora"))
    assert {k: _x(v) for k, v in re.findall(rf"\\widehat Q\(([xyz])\)=({_NUM})", ej)} \
        == corrida[2]["u"]
    assert int(re.search(r"La vuelta (\d+)\.", ej)[1]) == corrida[3]["vuelta"]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-atora"))
    m = re.search(rf"1\. ([xyz]), con \\widehat Q=({_NUM})", resp)
    assert m[1] == corrida[3]["jugada"] and _x(m[2]) == corrida[2]["u"][m[1]]
    piso = min(f["U"] for f in corrida)
    assert _x(re.search(rf"se quedan en ({_NUM}), el mínimo", resp)[1]) == piso
    assert _x(re.search(rf"nunca baja a ({_NUM})", resp)[1]) == piso
    assert corrida[2]["u"]["x"] == piso and corrida[-1]["N"]["x"] == 1
    m = re.search(rf"Tras ({_NUM}) vueltas, x e y llevan (\w+) simulación cada una y z, ({_NUM})",
                  resp)
    vueltas = int(_x(m[1]))
    n = j.bandido("mejor_promedio", j.MUS_HILO, vueltas, j.SEMILLA_ATORA)["N"]
    assert (n["x"], n["y"], n["z"]) == (_x(m[2]), _x(m[2]), _x(m[3]))
    m = re.search(rf"({_NUM}) de ({_NUM}) vueltas en la peor jugada", _llevarse(texto))
    assert (_x(m[1]), _x(m[2])) == (n["z"], vueltas) and "z" == min(mus, key=mus.get)


def test_prosa_clase_3_p6_la_tabla_y_la_figura_de_hoeffding():
    """#39 · Bloque 2 (Ola 3): @jue-c3-tabla-hoeffding (24.7/81.9 … 0.2/1.8
    %), la jugada y con Q_azar = 0.3, ε = 0.2, el umbral 0.1 y las 20 000
    tiradas; la tabla nueva @jue-c3-tabla-mover-eps y el alt de la figura
    rehecha (cota contra ε con N = 100; margen contra N para δ = 0.05 y
    0.005), de tabla_hoeffding_epsilon y margenes_hoeffding; y
    @jue-c3-ej-fila-cota. Se retira la frase del resumen con la cota (el
    resumen nuevo ya no cita cifras de Hoeffding), y los ejes que se leían
    de gen.plano_hoeffding (la figura se rehizo con otros ejes)."""
    texto = _pagina(P6)
    dos = _seccion(texto, 2)
    m = re.search(rf"lo medido para la jugada y, con Q_azar=({_NUM}): en ({_NUM}) tiradas, "
                  rf"cuántas veces \\widehat Q≤({_NUM}) al llegar a cada N", dos)
    assert _x(m[1]) == j.MUS_HILO["y"] == j.MU_HOEFFDING
    assert _x(m[2]) == j.REPS_HOEFFDING
    eps = _x(re.search(rf"Con \\varepsilon=({_NUM}) fijo", dos)[1])
    assert eps == j.EPS_HOEFFDING and _x(m[3]) == j.MU_HOEFFDING - j.EPS_HOEFFDING
    t = j.tabla_hoeffding()
    filas = _tabla(texto, "jue-c3-tabla-hoeffding")
    assert [_c(x) for x in filas[0][1:]] == ["Medido", "Cota"]
    leidas = [(int(_c(f[0])), _c(f[1]), _c(f[2])) for f in filas[1:]]
    assert leidas == [(n, _pc(t[n][0]), _pc(t[n][1])) for n, _, _ in leidas]
    assert all(frec <= cota for frec, cota in t.values())
    # Mover el margen con N = 100 fijo.
    n_eps = int(re.search(r"Con N=(\d+) fijo, pedir un error más grande", dos)[1])
    assert n_eps == j.N_HOEFFDING_HOMOLOGACION
    mover = {_x(_c(f[0])): _c(f[1]) for f in _tabla(texto, "jue-c3-tabla-mover-eps")[1:]}
    esperado = dict(j.tabla_hoeffding_epsilon())
    assert set(mover) == {_x(repr(e)) for e in esperado}
    for e, pct in esperado.items():
        cifra = mover[_x(repr(e))].removesuffix(" %")
        decimales = len(cifra.split(".")[1])
        assert cifra == f"{pct:.{decimales}f}", e
        assert f"{cifra} %" in _alt(texto, "jue-c3-fig-hoeffding"), e
    alt = _alt(texto, "jue-c3-fig-hoeffding")
    assert re.search(rf"contra el margen ε, con N = ({_NUM})", alt)[1] == str(n_eps)
    m = re.search(rf"para δ = ({_NUM}) y δ = ({_NUM}).*?con N = ({_NUM}), ({_NUM}) y ({_NUM})", alt)
    deltas = (float(m[1]), float(m[2]))
    assert deltas == j.DELTAS_HOEFFDING_HOMOLOGACION
    margenes = j.margenes_hoeffding((int(m[3]),))
    assert (m[4], m[5]) == tuple(f"{margenes[d][0][1]:.3f}" for d in deltas)
    m = re.search(rf"contra N, de ({_NUM}) a ({_NUM}), en la escala de U", alt)
    assert (int(m[1]), int(m[2])) == (10, 200)
    assert min(t) <= int(m[1]) and max(t) == int(m[2])
    assert "un tercio más arriba" in alt
    # La pregunta inicial: 13.5 % con 100 simulaciones y ε = 0.2.
    m = re.search(rf"con ({_NUM}) simulaciones, ¿qué tan seguido queda el promedio ({_NUM}) o más "
                  rf"por debajo.*?a lo más ({_NUM} %)", dos)
    assert (int(m[1]), _x(m[2]), m[3]) == (n_eps, eps, _pc(t[n_eps][1]))
    # El ejercicio: la cota con N = 100 y ε = 0.2, a mano.
    ej = _limpio(_bloque(texto, "jue-c3-ej-fila-cota"))
    m = re.search(rf"Con N=({_NUM}) y \\varepsilon=({_NUM})", ej)
    n, e = int(m[1]), _x(m[2])
    assert e == j.EPS_HOEFFDING and n in t
    assert re.search(rf"Lo medido fue ({_NUM} %)", ej)[1] == _pc(t[n][0])
    resp = _limpio(_respuesta(texto, "jue-c3-ej-fila-cota"))
    m = re.search(rf"1\. Sí coincide\. ({_NUM})·({_NUM})/2=({_NUM}) y e\^-({_NUM})≈({_NUM}): el "
                  rf"({_NUM} %)", resp)
    assert (int(m[1]), _x(m[2]), _x(m[3]), _x(m[4])) == (n, e ** 2, n * e ** 2 / 2, n * e ** 2 / 2)
    assert m[5] == f"{j.cota_hoeffding(n, float(e)):.3f}" and m[6] == _pc(t[n][1])
    m = re.search(rf"2\. No la contradice\..*?; ({_NUM} %) queda muy por debajo", resp)
    assert m[1] == _pc(t[n][0])


def test_prosa_clase_3_p6_despejar_el_margen():
    """#39 · Bloque 3 (Ola 3; antes §3): δ = e^−2 ≈ 0.14 da ε = 0.2 con N = 100;
    el 5 % da 0.24 con ln 20 ≈ 3.00 (y la pregunta inicial, «Unos 0.24»);
    @jue-c3-ej-despeja (÷2 al cuadruplicar N, un tercio más al pedir diez
    veces menos fallo: 0.245 → 0.326)."""
    texto = _pagina(P6)
    tres = _seccion(texto, 3)
    m = re.search(rf"con \\delta=e\^-({_NUM})≈({_NUM}) y N=({_NUM}), sale \\varepsilon=({_NUM}), la "
                  rf"fila de ({_NUM}) leída al revés", tres)
    k, n = _x(m[1]), int(m[3])
    delta = _m.exp(-k)
    assert m[2] == _d(delta)
    assert _x(m[4]) == _x(_d(j.margen(delta, n), 1)) == j.EPS_HOEFFDING
    assert int(m[5]) == n and _isclose_f(j.cota_hoeffding(n, float(_x(m[4]))), delta)
    m = re.search(rf"Con ({_NUM}) %, \\ln({_NUM})≈({_NUM}) y \\varepsilon≈({_NUM})", tres)
    delta = _x(m[1]) / 100
    assert _x(m[2]) == 1 / delta and m[3] == _d(_m.log(1 / delta))
    assert m[4] == _d(j.margen(float(delta), n))
    m = re.search(rf"si aceptas fallar ({_NUM}) % de las veces, ¿cuánto margen necesitas con "
                  rf"({_NUM}) simulaciones\? Unos ({_NUM})", tres)
    assert _x(m[1]) / 100 == delta and int(m[2]) == n and m[3] == _d(j.margen(float(delta), n))
    resp = _limpio(_respuesta(texto, "jue-c3-ej-despeja"))
    veces = _x(re.search(rf"se multiplica por ({_NUM})", _limpio(
        _bloque(texto, "jue-c3-ej-despeja")))[1])
    m = re.search(rf"1\. Se divide entre ({_NUM})\..*?\\sqrt({_NUM})=({_NUM})", resp)
    assert _x(m[2]) == veces and _x(m[1]) == _x(m[3]) == F(_m.isqrt(int(veces)))
    assert _isclose_f(j.margen(0.05, 100) / j.margen(0.05, 100 * int(veces)), _x(m[1]))
    m = re.search(rf"pedir (\w+) veces menos fallo, de ({_NUM}) a ({_NUM}), hace crecer el "
                  rf"margen solo (un tercio)\. Con N=({_NUM}), pasa de ({_NUM}) a ({_NUM})", resp)
    antes, despues = float(_x(m[2])), float(_x(m[3]))
    assert _x(m[1]) == _x(m[2]) / _x(m[3])
    n = int(m[5])
    crece = j.margen(despues, n) / j.margen(antes, n) - 1
    assert round(crece, 2) == round(float(_x(m[4])), 2)
    assert (m[6], m[7]) == (f"{j.margen(antes, n):.3f}", f"{j.margen(despues, n):.3f}")


def _isclose_f(a, b):
    return _m.isclose(float(a), float(b), rel_tol=1e-9)


def test_prosa_clase_3_p6_delta_n_a_la_menos_4_y_c_2_raiz_2():
    """#39 · Bloque 3 (Ola 3; antes §5): δ = N(s)^−4, ln(1/δ) = 4 ln N(s),
    √(8 ln N(s)/N(s,a)), c = 2√2 ≈ 2.83; la tabla de escalas del bloque 5
    ([0, 1] → e^(−2Nε²) y √2; [−1, 1] → e^(−Nε²/2) y 2√2; [−100, 100] →
    e^(−Nε²/20000) y 200√2) y «multiplica cada puntaje por 2 y resta 1»;
    N(s,a) = 0 se atiende antes (bono infinito). Se retiran: «c = √2 con la
    tasa G/N» (plan §5.1 elimina G/N; su lugar lo toma la escala de 0 a 1) y
    @jue-c3-ej-optimismo (archivado: duplica cuentas, destinos R18)."""
    texto = _pagina(P6)
    tres = _seccion(texto, 3)
    k = int(re.search(r"Con \\delta=N\(s\)\^-(\d+), \\ln\(1/\\delta\)=(\d+)\\ln N\(s\)", tres)[1])
    assert int(re.search(r"\\ln\(1/\\delta\)=(\d+)\\ln N\(s\)", tres)[1]) == k
    assert int(re.search(r"El (\d+) es una elección", tres)[1]) == k
    ocho = int(re.search(r"\\sqrt\\frac(\d+)\\ln N\(s\)N\(s,a\)", tres)[1])
    assert ocho == 2 * k and _isclose_f(_m.sqrt(ocho), j.C_TEORIA)
    assert int(re.search(r"\\delta=N\(s\)\^-(\d+)", _llevarse(texto))[1]) == k
    for n_padre, n in ((100, 10), (5, 1), (50, 30), (10_000, 7)):
        assert _isclose_f(j.bono_ucb(n_padre, n), j.margen(n_padre ** -k, n))
    aprox = re.findall(r"2\\sqrt2≈(\d+\.\d+)", _limpio(texto))
    assert aprox == [_d(j.C_TEORIA)]
    # La escala de los pagos: la cota y la c de UCB1 en cada una.
    cinco = _seccion(texto, 5)
    filas = re.findall(r"\| \[(-?\d+),(\d+)\] \| e\^-(\d*)N\\varepsilon\^2(?:/(\d+))? \| "
                       r"(\d*)\\sqrt2 \|", cinco)
    assert [(int(a), int(b)) for a, b, *_ in filas] == [(0, 1), (-1, 1), (-100, 100)]
    for a, b, arriba, abajo, factor in filas:
        ancho = int(b) - int(a)
        coef = F(int(arriba or 1), int(abajo or 1))
        for n, e in ((10, 0.1), (100, 0.2)):
            assert _isclose_f(j.cota_hoeffding_cola(n, e, ancho), _m.exp(-coef * n * e ** 2))
        assert _isclose_f(j.c_ucb1(ancho=ancho), int(factor or 1) * _m.sqrt(2))
    m = re.search(r"usan la escala de 0 a 1, \(U\+1\)/2, y escriben c=\\sqrt(\d)\. Es la misma "
                  r"regla: pasar a \[-1,1\] multiplica cada puntaje por (\d+) y resta (\d+), y con "
                  r"ello dobla c", cinco)
    assert m[1] == "2"
    a, b = int(m[2]), int(m[3])
    con_u = j.puntajes_ucb(j.EJERCICIO_MCTS)
    con_g = j.uct_ejercicio(c=_m.sqrt(2), victorias=True)
    assert all(_isclose_f(con_u[x], a * con_g[x] - b) for x in con_u)
    for x, (n, u) in j.EJERCICIO_MCTS.items():
        assert a * (u + 1) / 2 - b == u, x
    # Sin probar: bono infinito; por eso se atiende antes (bloque 1).
    assert ("Una jugada sin visitas se atiende primero. La fórmula solo se usa cuando todas "
            "tienen N(s,a)>0.") in _seccion(texto, 1)
    assert j.bono_ucb(100, 0) == j.INF


def test_prosa_clase_3_p6_tabla_y_figura_del_bono():
    """#39 · @jue-c3-tabla-bono (1.92, 1.11, 0.78 / 0.68, 0.39, 0.28 con
    N(s) = 100), «casi tres veces» (2√2/1), y el alt de @jue-c3-fig-bono
    (ejes, curvas, puntos, c = 1). Ola 3: bloque 5, N(s,a) y escala de U."""
    import gen_juegos as gen
    texto = _pagina(P6)
    n_padre = int(re.search(r"N\(s\) = (\d+)", _titulo(texto, "jue-c3-tabla-bono"))[1])
    prosa = _seccion(texto, 5)
    m = re.search(r"Con N\(s\)=(\d+), la de UCB1 da bonos (casi tres) veces más grandes que c=1",
                  prosa)
    assert int(m[1]) == n_padre and 2.5 < j.C_TEORIA < 3
    filas = _tabla(texto, "jue-c3-tabla-bono")
    cs = [_c_de(re.fullmatch(r"c=(.+)", _c(x))[1]) for x in filas[0][1:]]
    assert cs == [None, 1]
    tabla = {int(_c(f[0])): [_c(x) for x in f[1:]] for f in filas[1:]}
    assert tabla == {n: [_d(j.bono_ucb(n_padre, n, c)) for c in cs] for n in tabla}
    assert tuple(tabla) == gen.MARCAS_MICRO_BONO
    alt = _alt(texto, "jue-c3-fig-bono")
    pl = gen.plano_bono()
    m = re.search(rf"simulaciones de la jugada, de ({_NUM}) a ({_NUM})\.", alt)
    assert (_x(m[1]), _x(m[2])) == pl.xs
    assert tuple(_x(v) for v in re.search(rf"en la escala de U, de ({_NUM}) a ({_NUM})\.",
                                          alt).groups()) == pl.ys
    curvas = re.search(r"una por N\(s\): (.*?); las tres", alt)[1]
    assert tuple(int(_x(v)) for v in re.findall(rf"({_NUM}) (?:continua|con)", curvas)) \
        == gen.CURVAS_BONO
    m = re.search(rf"Puntos sobre la curva de ({_NUM}) en N\(s,a\) = ({_NUM}), ({_NUM}) y "
                  rf"({_NUM}): el bono vale ({_NUM}), ({_NUM}) y ({_NUM})\.", alt)
    assert int(m[1]) == n_padre
    assert dict(zip((int(v) for v in m.groups()[1:4]), m.groups()[4:])) == {
        n: v[0] for n, v in tabla.items()}
    m = re.search(rf"c = ({_NUM}) con N\(s\) = ({_NUM}), queda muy por debajo: ({_NUM}) en "
                  rf"N\(s,a\) = ({_NUM})", alt)
    assert (_x(m[1]), int(m[2])) == (1, n_padre)
    assert m[3] == _d(j.bono_ucb(n_padre, int(m[4]), 1)) == tabla[int(m[4])][1]


def test_prosa_clase_3_p6_el_ejercicio_de_mcts_con_la_c_de_la_teoria():
    """#39 · Ola 3: @jue-c3-ej-teoria y @jue-c3-ej-entregar se archivaron
    (duplicaban cuentas, destinos R18). Lo que sobrevive vive en la
    respuesta de @jue-c3-ej-mcts de «MCTS con UCT»: con c = 2√2 la
    selección va a z con 2.12 contra 1.71 de y (antes 1.28/1.71/2.12), con
    c = 1 a y; se entrega x, con 60, y no y, la de mejor promedio con 30."""
    texto = _pagina(P5b)
    datos = {k: (int(n), F(u)) for k, n, u in re.findall(
        r"([xyz]): N=(\d+) visitas, \\widehat Q=(\d+(?:\.\d+)?)",
        _limpio(_bloque(texto, "jue-c3-ej-mcts")))}
    assert datos == j.EJERCICIO_MCTS
    teoria, p5 = j.puntajes_ucb(datos), j.puntajes_ucb(datos, c=1)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-mcts"))
    assert re.search(r"La selección baja por ([xyz])", resp)[1] == j.mejor(p5)
    m = re.search(r"Con c=2\\sqrt2, con holgura: (\d+\.\d+) contra (\d+\.\d+)", resp)
    orden = sorted(teoria, key=teoria.get, reverse=True)
    assert (m[1], m[2]) == (_d(teoria[orden[0]]), _d(teoria[orden[1]]))
    assert orden[:2] == ["z", "y"] and j.mejor(p5) != j.mejor(teoria)
    entrega = j.mas_simulada(datos)
    por_u = max(datos, key=lambda k: datos[k][1])
    m = re.search(r"1\. ([xyz]): al final se entrega la jugada con más visitas, y \1 tiene (\d+)",
                  resp)
    assert (m[1], int(m[2])) == (entrega, datos[entrega][0])
    m = re.search(r"(\d+) vueltas pesan más que (\d+)", resp)
    assert (int(m[1]), int(m[2])) == (datos[entrega][0], datos[por_u][0]) and por_u != entrega


def test_prosa_clase_3_p6_la_corrida_sembrada_con_ucb_y_la_vuelta_6():
    """#39 · Bloque 3 (Ola 3; antes §6 y @jue-c3-ej-vuelta-seis, archivado):
    la semilla 36 con c = 2√2: x, y, z, z, z con −1, −1, +1, −1, −1; la tabla
    de la vuelta 6 (N(s) = 5, δ = 5^−4 = 1/625, ln 5 ≈ 1.61; x y y con 3.59
    y 2.59, z con −1/3, 2.07 y 1.74); x empata con y y va primero; y las
    1000 vueltas (817, 145, 38 contra 998 sin bono)."""
    texto = _pagina(P6)
    tres = _seccion(texto, 3)
    ucb, mp = _corrida("ucb"), _corrida("mejor_promedio")
    m = re.search(r"Las (\w+) primeras vueltas eligen ((?:[xyz], )*[xyz]) y pagan ([-+,\d]+)\.",
                  tres)
    hasta = {"cinco": 5}[m[1]]
    assert m[2].split(", ") == [f["jugada"] for f in ucb[:hasta]] == [
        f["jugada"] for f in mp[:hasta]]
    assert [int(u) for u in m[3].split(",")] == [f["U"] for f in ucb[:hasta]]
    antes = ucb[hasta - 1]
    n_padre, N, u = antes["vuelta"], antes["N"], antes["u"]
    m = re.search(r"Con N\(s\)=(\d+), \\delta=(\d+)\^-(\d+)=1/(\d+) y \\ln(\d+)≈(\d+\.\d+):", tres)
    assert int(m[1]) == int(m[2]) == int(m[5]) == n_padre
    assert _isclose_f(j.delta_de_c(j.C_TEORIA, n_padre), F(1, int(m[4])))
    assert n_padre ** int(m[3]) == int(m[4]) and m[6] == _d(_m.log(n_padre))
    puntaje = {k: float(u[k]) + j.bono_ucb(n_padre, N[k]) for k in u}
    filas = re.findall(rf"\| ([xyz]) \| (\d+) \| ({_NUM}(?:/\d+)?) \| ({_NUM}) \| ({_NUM}) \|", tres)
    assert [f[0] for f in filas] == list(u)
    for k, n, q, bono, p in filas:
        assert (int(n), _x(q)) == (N[k], u[k]), k
        assert bono == _d(j.bono_ucb(n_padre, N[k])) and p == _d(puntaje[k]), k
        # El bono es el margen con δ = N(s)^−4: la cota optimista de la corrida.
        assert _isclose_f(j.bono_ucb(n_padre, N[k]), j.margen(n_padre ** -4, N[k])), k
    m = re.search(r"Se le da otra oportunidad a ([xyz]): empata con ([xyz]), pero va primero", tres)
    assert m[1] == j.mejor(puntaje) == ucb[hasta]["jugada"] != mp[hasta]["jugada"]
    assert puntaje[m[1]] == puntaje[m[2]] and list(u).index(m[1]) < list(u).index(m[2])
    m = re.search(rf"Tras ({_NUM}) vueltas, x se lleva ({_NUM}), y ({_NUM}) y z ({_NUM}); sin bono, "
                  rf"z se llevaba ({_NUM})\.", tres)
    vueltas = int(_x(m[1]))
    n = j.bandido("ucb", j.MUS_HILO, vueltas, j.SEMILLA_ATORA)["N"]
    assert tuple(int(_x(v)) for v in m.groups()[1:4]) == (n["x"], n["y"], n["z"])
    assert max(n, key=n.get) == "x"
    assert int(_x(m[5])) == j.bandido("mejor_promedio", j.MUS_HILO, vueltas,
                                      j.SEMILLA_ATORA)["N"]["z"]


_REGLAS_TABLA = {"Mejor promedio": "mejor_promedio", "Al azar 10 %": "a_veces_al_azar",
                 "UCB, c=2\\sqrt2": "ucb", "UCB, c=1": "ucb_c1"}


def test_prosa_clase_3_p6_la_figura_del_pago_y_sus_vinetas():
    """#39 · Bloque 5 (Ola 3). La figura @jue-c3-fig-pago se retira (plan §7,
    destinos E.2): su título y su alt ya no existen. Lo demás se re-ancla a
    @jue-c3-tabla-pagos-finales (pago por vuelta en la 10 y la 10 000, de
    tabla_pago) y sus viñetas: sin bono gana al principio; 34/5/1 y 0.5425;
    c = 1 paga 0.598 y la de UCB1 0.580; las 40 corridas, semillas 1 a 40 y
    10 000 vueltas; 0.6 como lo mejor posible; la semilla 36 sin regreso y
    las otras 5 con x en 0 o −0.2; c = 0 es el mejor promedio; el resumen."""
    texto = _pagina(P6)
    cinco = _seccion(texto, 5)
    t = j.tabla_pago()
    e = j.pago_esperado_reparto()
    ini, fin = min(j.MARCAS_BANDIDO), max(j.MARCAS_BANDIDO)
    f3 = lambda v: f"{float(v):.3f}"  # noqa: E731
    assert "jue-c3-fig-pago" not in texto
    filas = _tabla(texto, "jue-c3-tabla-pagos-finales")
    marcas = [int(_x(re.fullmatch(rf"Vuelta ({_NUM})", _c(x))[1])) for x in filas[0][1:]]
    assert marcas == [ini, fin]
    leidas = {_REGLAS_TABLA[_c(f[0])]: tuple(_c(x) for x in f[1:]) for f in filas[1:]}
    assert leidas == {k: tuple(f3(t[k][mk]) for mk in marcas) for k in t}
    m = re.search(rf"Cada una corre ({_NUM}) veces, con las semillas ({_NUM}) a ({_NUM}), y cada "
                  rf"corrida tiene ({_NUM}) vueltas\.", cinco)
    assert (_x(m[1]), _x(m[2]), _x(m[3]), _x(m[4])) == (j.CORRIDAS_BANDIDO, 1,
                                                        j.CORRIDAS_BANDIDO, fin)
    assert _x(re.search(rf"Lo mejor posible es ({_NUM}), siempre x\.", cinco)[1]) == j.MUS_HILO["x"]
    assert _x(re.search(rf"elige al azar con probabilidad ({_NUM})", cinco)[1]) == \
        j._exacto(j.AL_AZAR)
    # Las viñetas.
    m = re.search(rf"En la vuelta ({_NUM}), la regla sin bono gana más que las dos UCB\.", cinco)
    mp = t["mejor_promedio"]
    assert _x(m[1]) == ini and mp[ini] > max(t["ucb"][ini], t["ucb_c1"][ini])
    en = e["en"]
    m = re.search(rf"Con ({_NUM}), ({_NUM}) y ({_NUM}) corridas en x, y, z se espera "
                  rf"\(({_NUM})·({_NUM})\+({_NUM})·({_NUM})-({_NUM})\)/({_NUM})=({_NUM})\.", cinco)
    assert tuple(int(v) for v in m.groups()[:3]) == (en["x"], en["y"], en["z"])
    assert (int(m[4]), _x(m[5]), int(m[6]), _x(m[7]), _x(m[8]), int(m[9])) == (
        en["x"], j.MUS_HILO["x"], en["y"], j.MUS_HILO["y"], -j.MUS_HILO["z"], j.CORRIDAS_BANDIDO)
    assert _x(m[10]) == e["esperado"] and _d(mp[fin]) == _d(e["esperado"])
    m = re.search(rf"Aquí c=1 juega mejor\. Explora menos, llega antes y paga ({_NUM}); la de "
                  rf"UCB1, ({_NUM})\.", cinco)
    assert (m[1], m[2]) == (f3(t["ucb_c1"][fin]), f3(t["ucb"][fin]))
    assert t["ucb"][fin] < t["ucb_c1"][fin] < j.MUS_HILO["x"]
    assert mp[fin] < t["a_veces_al_azar"][fin] < t["ucb"][fin]
    # Solo la semilla 36 está probada sin regreso (r2).
    regreso = j.regreso_de_atoradas()
    assert all(r["ultima_x"] < fin for r in regreso.values())
    sin_regreso = [k for k, r in regreso.items() if not r["puede_volver"]]
    assert sin_regreso == [j.SEMILLA_ATORA]
    m = re.search(rf"La semilla ({_NUM}) no tiene regreso\. x quedó en ({_NUM}) y ([xyz]) ya ganó\. "
                  rf"En las otras ({_NUM}), x quedó en ({_NUM}) o en ({_NUM}): una racha mala muy "
                  rf"larga de ([xyz]) podría devolverla\.", cinco)
    r36 = regreso[int(m[1])]
    assert int(m[1]) == j.SEMILLA_ATORA and _x(m[2]) == r36["u_x"] and m[3] == r36["en"]
    assert r36["ganadas_atorada"] > 0
    otras = {k: r for k, r in regreso.items() if r["puede_volver"]}
    assert int(m[4]) == len(otras) and {_x(m[5]), _x(m[6])} == {r["u_x"] for r in otras.values()}
    assert {r["en"] for r in otras.values()} == {m[7]}
    assert "no se corrigen nunca" not in cinco and "para siempre:" not in cinco
    # c = 0 es «siempre el mejor promedio», en las dos medidas.
    assert "Con c=0 no hay bono y la regla solo aprovecha." in _seccion(texto, 1)
    assert "compara siempre con c=0" in cinco
    p0 = j.pago_por_vuelta("ucb", j.MUS_HILO, j.MARCAS_BANDIDO, j.CORRIDAS_BANDIDO, 0)
    e0 = j.eligiendo_la_mejor("ucb", j.MUS_HILO, j.MARCAS_BANDIDO, j.CORRIDAS_BANDIDO, 0)
    assert p0 == mp and e0 == j.tabla_eligiendo_x()["mejor_promedio"]
    # El resumen.
    m = re.search(rf"Aquí c=1 paga ({_NUM}) contra ({_NUM})", _llevarse(texto))
    assert (m[1], m[2]) == (f3(t["ucb_c1"][fin]), f3(t["ucb"][fin]))
    # La figura vieja, acumulada, ya no está.
    assert "jue-c3-fig-bandido " not in texto and "jue-c3-fig-bandido}" not in texto
    assert "@jue-c3-fig-bandido" not in texto
    assert "jue-c3-bandido.svg" not in texto and "acumulada" not in texto


def test_prosa_clase_3_p6_la_figura_eligiendo_x_y_sus_vinetas():
    """#39 · Ola 3: la figura @jue-c3-fig-eligiendo-x se retira (plan §7);
    su título, su alt y las viñetas que la describían ya no existen. Lo que
    sobrevive, re-anclado al bloque 5: sin bono, desde la vuelta 100 el 85 %
    de las elecciones va a x, que es 34/40 (tabla_eligiendo_x y
    reparto_bandido); a veces al azar, ya en x, la elige 0.9 + 0.1/3 ≈ 93.3 %
    (tope_a_veces_al_azar)."""
    texto = _pagina(P6)
    cinco = _seccion(texto, 5)
    assert "jue-c3-fig-eligiendo-x" not in texto
    t = j.tabla_eligiendo_x()
    mp = t["mejor_promedio"]
    fin = max(j.MARCAS_BANDIDO)
    r = j.reparto_bandido()["mejor_promedio"]
    m = re.search(rf"desde la vuelta ({_NUM}), el ({_NUM}) % de las elecciones va a x, que es "
                  rf"({_NUM})/({_NUM})", cinco)
    desde = int(_x(m[1]))
    marcas = sorted(j.MARCAS_BANDIDO)
    primera = next(k for k in marcas if all(mp[x] == mp[fin] for x in marcas if x >= k))
    assert desde == primera and _x(m[2]) == mp[fin] * 100
    assert (int(m[3]), int(m[4])) == (r["n"] - r["atoradas"], r["n"])
    assert F(int(m[3]), int(m[4])) == mp[fin]
    tope = j.tope_a_veces_al_azar()
    m = re.search(rf"Ya en x, la elige ({_NUM})\+({_NUM})/(\d+)≈({_NUM})\\?%", cinco)
    a = j._exacto(j.AL_AZAR)
    assert (_x(m[1]), _x(m[2])) == (1 - a, a) and int(m[3]) == len(j.MUS_HILO)
    assert _x(m[1]) + _x(m[2]) / int(m[3]) == tope
    assert m[4] == f"{100 * float(tope):.1f}"
    assert any(v > tope for v in t["a_veces_al_azar"].values())
    assert t["ucb"][500] <= t["ucb"][200]


def test_prosa_clase_3_p6_el_nodo_de_min():
    """#39 · Bloque 4 (Ola 3): el ejemplo y @jue-c3-ej-final-bono con Q̂ en vez
    de ū. N(s) = 50; p/q/r con Q̂ −0.2, 0.25, 0.5 y N(s,a) 30, 16, 4; bonos
    1.02/1.40/2.80 y puntajes de MIN −1.22/−1.15/−2.30 (baja por r); ln 50 ≈
    3.91, ln 20 ≈ 3.00, ε = 0.45 y el piso −0.65 con δ = 0.05; con c = 1,
    0.36/0.49/0.99 y −0.56/−0.24/−0.49 (p); se entrega p, con 30; con el
    signo al revés, 0.82/1.65/3.30. Cifras de min_volteado."""
    texto = _pagina(P6)
    cuatro = _seccion(texto, 4)
    m = re.search(rf"Un nodo de MIN lleva N\(s\)=(\d+) vueltas\. Sus hijos p, q, r tienen "
                  rf"\\widehat Q de ({_NUM}), ({_NUM}) y ({_NUM}), medidos desde MAX, con N\(s,a\) "
                  rf"de (\d+), (\d+) y (\d+)\. Con c=2\\sqrt2, los bonos son ({_NUM}), ({_NUM}) y "
                  rf"({_NUM})\.", cuatro)
    n_padre = int(m[1])
    datos = {k: (int(m[5 + i]), _x(m[2 + i])) for i, k in enumerate("pqr")}
    assert datos == j.EJEMPLO_MIN and n_padre == sum(n for n, _ in datos.values())
    teoria, uno = j.min_volteado(), j.min_volteado(c=1)
    assert m.groups()[7:] == tuple(_d(teoria["filas"][k]["bono"]) for k in "pqr")
    m = re.search(rf"Los puntajes de MIN son ({_NUM}), ({_NUM}) y ({_NUM})\. Baja por ([pqr]): el "
                  rf"peor promedio para MIN, pero con solo (\d+) simulaciones", cuatro)
    assert m.groups()[:3] == tuple(_d(teoria["filas"][k]["abajo"]) for k in "pqr")
    assert m[4] == teoria["min"] and int(m[5]) == datos[m[4]][0] == min(
        n for n, _ in datos.values())
    alt = _alt(texto, "jue-c3-fig-min-volteado")
    assert re.search(rf"hasta Q̂ - bono: ({_NUM}), ({_NUM}) y ({_NUM})", alt).groups() == \
        tuple(_d(teoria["filas"][k]["abajo"]) for k in "pqr")
    ej = _limpio(_bloque(texto, "jue-c3-ej-final-bono"))
    delta = _x(re.search(rf"Con \\delta=({_NUM}), calcula el margen de p", ej)[1])
    ln = _ln(ej)
    assert set(ln) == {n_padre, int(1 / delta)}
    assert all(v == _d(_m.log(n)) for n, v in ln.items())
    resp = _limpio(_respuesta(texto, "jue-c3-ej-final-bono"))
    eps = j.margen(float(delta), datos["p"][0])
    m = re.search(rf"\\varepsilon=\\sqrt({_NUM})·({_NUM})/(\d+)≈({_NUM})", resp)
    assert (_x(m[1]), m[2], int(m[3]), m[4]) == (2, ln[int(1 / delta)], datos["p"][0], _d(eps))
    m = re.search(rf"su cota optimista es el piso ({_NUM})-({_NUM})=({_NUM})", resp)
    assert (_x(m[1]), m[2], m[3]) == (datos["p"][1], _d(eps), _d(float(datos["p"][1]) - eps))
    m = re.search(rf"El bono con c=2\\sqrt2, ({_NUM}), es más del (doble): pide \\delta=(\d+)\^-(\d+), "
                  rf"mucho menos que ({_NUM}) %", resp)
    bono_p = teoria["filas"]["p"]["bono"]
    assert m[1] == _d(bono_p) and bono_p > 2 * eps and int(m[3]) == n_padre
    assert _isclose_f(j.margen(float(n_padre) ** -int(m[4]), datos["p"][0]), bono_p)
    assert _x(m[5]) == delta * 100 and float(n_padre) ** -int(m[4]) < delta
    m = re.search(rf"2\. Con c=1 baja por ([pqr])\. Bonos ({_NUM}), ({_NUM}) y ({_NUM}); puntajes "
                  rf"({_NUM}), ({_NUM}) y ({_NUM})\.", resp)
    assert m[1] == uno["min"]
    assert m.groups()[1:] == tuple(_d(uno["filas"][k]["bono"]) for k in "pqr") + tuple(
        _d(uno["filas"][k]["abajo"]) for k in "pqr")
    entrega = j.mas_simulada(datos)
    m = re.search(r"3\. Se entrega ([pqr]), la de más visitas, (\d+)\.", resp)
    assert (m[1], int(m[2])) == (entrega, datos[entrega][0])
    m = re.search(rf"Con c=2\\sqrt2, los puntajes serían ({_NUM}), ({_NUM}) y ({_NUM}): elegiría "
                  rf"([pqr]) y dejaría ([pqr]) congelada", resp)
    arriba = {k: teoria["filas"][k]["arriba"] for k in "pqr"}
    assert m.groups()[:3] == tuple(_d(arriba[k]) for k in "pqr")
    assert m[4] == min(arriba, key=arriba.get) and m[5] == teoria["min"]


def test_prosa_clase_3_p5_p6_cada_promedio_sale_de_partidas_enteras():
    """r2 · Con U = ±1 y sin empates, G = N·(Q̂ + 1)/2 tiene que ser entero.
    Lee todo par (N, Q̂) de los ejemplos con U = ±1 de «MCTS con UCT» y del
    bono (Ola 3: la regex pasa de \\bar u a \\widehat Q, la p5 se parte y
    el MCTS vive en P5b) y lo pasa por victorias_de, que falla si G no es
    entero. Las tablas del árbol de resultados quedan fuera: ahí c1a = 0
    permite empates. El piso baja de 14 a 10 pares: @jue-c3-ej-teoria,
    -entregar y -optimismo se archivaron (destinos R18)."""
    mcts = _limpio(_pagina(P5b))
    pares = re.findall(rf"N=(\d+) visitas, \\widehat Q=({_NUM})", mcts)
    pares += [(_c(f[1]), _c(f[2])) for f in _tabla(_pagina(P5b), "jue-c3-tab-eleccion-uct")[1:]]
    bono = _limpio(_pagina(P6))
    pares += re.findall(rf"\| [xyz] \| (\d+) \| ({_NUM}(?:/\d+)?) \| {_NUM} \| {_NUM} \|", bono)
    m = re.search(rf"\\widehat Q de ({_NUM}), ({_NUM}) y ({_NUM}), medidos desde MAX, con "
                  rf"N\(s,a\) de (\d+), (\d+) y (\d+)", bono)
    pares += list(zip(m.groups()[3:], m.groups()[:3]))
    assert len(pares) >= 10, pares
    for n, u in pares:
        j.victorias_de(int(n), _x(u))


def test_prosa_clase_3_p5_p6_r2_lo_que_no_se_garantiza():
    """r2 · Afirmaciones demasiado generales que no deben volver: el bono de
    UCT como margen con garantía en el árbol, MIN eligiendo «su mejor
    respuesta», AlphaGo Zero «sin simulaciones», la más simulada como única
    regla de entrega, y la frecuencia de Hoeffding «siempre debajo». Ola 3:
    lo de MCTS pasa a «MCTS con UCT» (P5b); «δ acotaría si N se fijara» pasa
    al bono («cota nominal para N fijo»); la fila de la ficha de siete rasgos
    pasa a las propiedades («guarda los 15 nodos con 40 vueltas»). Con el
    léxico de §5.2 «simulación» ya es «hasta un final», así que «quitaron las
    simulaciones hasta el final» es la frase correcta; sigue prohibido «MCTS
    sin simulaciones»."""
    p5 = " ".join(_pagina(P5b).split())
    p6 = " ".join(_pagina(P6).split())
    assert "MIN elige su mejor respuesta por puntaje" not in p5
    assert "MIN elige lo que parece mejor para él, más un bono" in p5
    assert "MCTS sin simulaciones" not in p5
    assert "quitaron las simulaciones hasta el final.**" in p5
    assert "¿Sigue siendo MCTS sin esas simulaciones? Sí" in p5
    assert "Ese 10 % es una cota nominal para $N$ fijo, no una tasa real de errores." in p6
    assert "en el bandido, $\\delta$ es la probabilidad" not in p5
    assert "**La idea viene del bandido:**" in p5
    assert "el artículo original de UCT usa el mayor promedio" in p5
    assert "dentro del árbol no sortea nada" not in p5
    assert "Con un presupuesto finito, no" not in p5
    m = re.search(r"con (\d+) vueltas ya guarda los (\d+) nodos del árbol de resultados", p5)
    nodos, vueltas = int(m[2]), int(m[1])
    assert len(j.uct_tpm(1, vueltas, j.SEMILLA_TPM)["N"]) == nodos == j.contar_nodos(j.ARBOL_TPM)
    assert "Es el bono de UCT" not in p6 and "El bono de UCT es" not in p6
    assert "UCT pone un bandido en cada nodo" in p6
    assert "El bono conserva la forma del margen, pero ese margen, aquí, no se aplica directo." in p6
    assert "Nos basta **una cola**" not in p6 and "tiene la misma cota" in p6
    assert "No hay una $c$ óptima universal" in p6
    assert "una $c$ menor no hereda esa prueba" in p6
    html = (UNIDAD / "_assets/hoeffding_en_vivo.html").read_text(encoding="utf-8")
    assert "siempre debajo" not in html.lower() and "en una corrida corta puede pasarse" in html


def test_prosa_clase_3_p6_tabla_c_delta():
    """#39 · @jue-c3-tabla-c-delta (c = 1: δ = N(s)^−1/2, 10 %; c = 2√2:
    δ = N(s)^−4, 10^−8 con N(s) = 100) y la regla δ = N(s)^(−c²/2). Ola 3: la
    columna k se retira (plan §5.1 elimina la k del exponente); el exponente
    se lee del propio δ y se compara con exponente_de_c."""
    texto = _pagina(P6)
    filas = _tabla(texto, "jue-c3-tabla-c-delta")
    n_padre = int(re.search(r"Con N\(s\)=(\d+)", _c(filas[0][2]))[1])
    vistas = []
    for f in filas[1:]:
        c = _c_de(_c(f[0]))
        cf = j.C_TEORIA if c is None else float(c)
        vistas.append(c)
        k = _x(re.fullmatch(r"N\(s\)\^-(\S+)", _c(f[1]))[1])
        assert _isclose_f(j.exponente_de_c(cf), k), f
        celda = _c(f[2])
        m = re.fullmatch(rf"({_NUM}) %", celda) or re.fullmatch(r"10\^(-\d+)", celda)
        assert m, celda
        leido = float(_x(m[1])) / 100 if "%" in celda else 10.0 ** int(m[1])
        assert _isclose_f(j.delta_de_c(cf, n_padre), leido), f
    assert vistas == [1, None]
    tres = _seccion(texto, 3)
    assert "con c>0 y N(s)>1, sale \\delta=N(s)^-c^2/2" in tres
    for c in (1, j.C_TEORIA):
        assert _isclose_f(j.exponente_de_c(c), c ** 2 / 2)
    m = re.search(rf"Ese ({_NUM}) % es una cota nominal para N fijo", tres)
    assert _isclose_f(j.delta_de_c(1, n_padre) * 100, _x(m[1]))


def test_prosa_clase_3_p6_la_cota_optimista_en_la_corrida():
    """#39 · Bloque 3 (Ola 3; antes §4 y §5): la cota optimista es Q̂ + ε
    (definición) y, con δ = N(s)^−4, es el puntaje; en la corrida 36 tras
    cinco vueltas (N(s) = 5, 5^−4 = 1/625) la de x es la más alta, 2.59,
    «por encima de +1». Se retira el cálculo aparte con ln 625 ≈ 6.44: la
    página nueva lo hace con el bono (ln 5 ≈ 1.61) y da las mismas cotas,
    que fija test_prosa_clase_3_p6_la_corrida_sembrada_con_ucb_y_la_vuelta_6."""
    texto = _pagina(P6)
    defin = _limpio(_bloque(texto, "jue-c3-cota-optimista"))
    assert "La cota optimista de una jugada de MAX es \\widehat Q(s,a)+\\varepsilon" in defin
    assert "Puede pasar de +1" in defin
    tres = _seccion(texto, 3)
    mp = _corrida("mejor_promedio")
    vueltas = 5
    estado = mp[vueltas - 1]
    delta = F(1, vueltas ** 4)
    assert _isclose_f(j.delta_de_c(j.C_TEORIA, vueltas), delta)
    cotas = {k: float(estado["u"][k]) + j.margen(float(delta), estado["N"][k])
             for k in estado["u"]}
    for k in cotas:
        assert _isclose_f(cotas[k], float(estado["u"][k]) + j.bono_ucb(vueltas, estado["N"][k]))
    m = re.search(rf"Una cota de ({_NUM}), por encima de \+1", tres)
    alta = max(cotas, key=cotas.get)
    assert m[1] == _d(cotas[alta]) and cotas[alta] > 1 and alta == "x"
    assert "El puntaje del bloque 1 es la cota optimista." in tres


def test_prosa_clase_3_p6_la_vuelta_5_con_ucb():
    """#39 · Ola 3: la vuelta 5 de la corrida 36 (z 2.35 contra 2.33) ya no
    se narra en el bono reescrito (§6.4: duplicaba la vuelta 6, que sí queda
    en el bloque 3). Se retira la parte de prosa; la cifra sigue fijada por
    la fuente (test_p6_puntajes_de_las_vueltas_5_y_6_de_la_corrida_36) y
    aquí, contra la corrida: z gana con x e y empatadas."""
    texto = _pagina(P6)
    assert "2.35" not in texto
    n_padre, p = j.puntajes_ucb_en_vuelta(5)
    estado = _corrida("ucb")[n_padre - 1]
    assert n_padre == estado["vuelta"] == 4
    assert p["x"] == p["y"] and j.mejor(p) == "z" == _corrida("ucb")[n_padre]["jugada"]


def test_prosa_clase_3_p6_las_corridas_una_por_punto():
    """#39 · Ola 3: la figura @jue-c3-fig-bandido-corridas se retira (plan
    §7); su conclusión pasa a @jue-c3-tabla-corridas (34/6 sin bono, 40/0
    las demás) y sus viñetas: 5 en y y 1 en z; las peores corridas de las
    otras tres dejan en x 0.90, 0.92 y 0.96. Se retira la frase del resumen
    («En 40 corridas… todo o nada»): el resumen nuevo no la repite."""
    texto = _pagina(P6)
    assert "jue-c3-fig-bandido-corridas" not in texto
    r = j.reparto_bandido()
    mp = r["mejor_promedio"]
    otras = ("a_veces_al_azar", "ucb", "ucb_c1")
    filas = _tabla(texto, "jue-c3-tabla-corridas")
    assert [_c(x) for x in filas[0][1:]] == ["En x", "Atoradas"]
    leidas = {_REGLAS_TABLA[_c(f[0])]: (int(_c(f[1])), int(_c(f[2]))) for f in filas[1:]}
    assert leidas == {k: (v["n"] - v["atoradas"], v["atoradas"]) for k, v in r.items()}
    assert all(x < 0.01 or x > 0.99 for x in mp["fracciones"])
    cinco = _seccion(texto, 5)
    m = re.search(r"Sin bono es todo o nada\. De las (\d+) atoradas, (\d+) se quedan en y y (\d+) "
                  r"en z", cinco)
    assert tuple(int(v) for v in m.groups()) == (mp["atoradas"], mp["en"]["y"], mp["en"]["z"])
    m = re.search(rf"Su peor corrida deja en x ({_NUM}), ({_NUM}) y ({_NUM}) de sus vueltas\.", cinco)
    assert m.groups() == tuple(_d(r[f]["minimo"]) for f in otras)
    assert all(r[f]["atoradas"] == 0 for f in otras)
    assert re.search(r"Una corrida está atorada si deja en x menos de la mitad de sus vueltas",
                     cinco)
    assert sum(x < 0.5 for x in mp["fracciones"]) == mp["atoradas"]


def test_prosa_clase_3_p6_lo_que_garantizan_auer_y_kocsis():
    """#39 · Bloques 5 y 6 (Ola 3; antes §6 y §8): qué garantiza la cota de
    UCB1 (vueltas en una jugada peor ≲ ln N(s), en esperanza; Auer et al.
    2002, en el bloque 3) y que una c menor no hereda esa prueba; el teorema
    de Kocsis y Szepesvári como lo registra la verificación (probabilidad de
    elegir en la raíz una jugada peor → 0), y que llegar no pide una c
    grande."""
    texto = _pagina(P6)
    cinco, seis = _seccion(texto, 5), _seccion(texto, 6)
    assert re.search(r"Con c=2\\sqrt2 en el bandido estacionario, UCB1 asegura que, en esperanza, "
                     r"las vueltas gastadas en una jugada peor crecen a lo más como \\ln N\(s\)",
                     cinco)
    assert "(Auer, Cesa-Bianchi y Fischer, 2002)" in _seccion(texto, 3)
    assert "La teoría acota" not in cinco and "en cualquier bandido" not in cinco
    assert "una c menor no hereda esa prueba" in cinco
    assert re.search(r"la probabilidad de que UCT elija en la raíz una jugada peor que la de "
                     r"minimax tiende a 0", seis)
    assert re.search(r"Llegar no pide una c grande\. En un árbol finito, con cualquier c>0 fija",
                     seis)
    assert "La c grande es la que da una cota de qué tan rápido." in seis
    ver = (UNIDAD.parent.parent / "docs/verificacion/juegos/0_index.md").read_text(encoding="utf-8")
    assert "teorema 6" in ver and "la probabilidad de fallo en la raíz" in ver
    assert "Su teorema 1" in ver and "8\\ln n/\\Delta^2" in ver


def test_prosa_clase_3_p6_a_veces_al_azar_se_espera_no_se_topa():
    """#39 · Bloque 5 (Ola 3): el 93.3 % de «a veces al azar» es un valor
    esperado, no un tope: hay marcas que lo pasan, y la viñeta que lo cita
    no lo vuelve techo. Los alts de las figuras retiradas
    (@jue-c3-fig-eligiendo-x, @jue-c3-fig-pago) ya no existen."""
    texto = _pagina(P6)
    cinco = _seccion(texto, 5)
    tope = j.tope_a_veces_al_azar()
    az = j.reparto_bandido()["a_veces_al_azar"]
    assert az["promedio"] < tope < az["maximo"]
    assert max(j.tabla_eligiendo_x()["a_veces_al_azar"].values()) > tope
    vineta = re.search(r"A veces al azar no se atora, pero sigue tirando\.[^-]*", cinco)[0]
    assert "93.3" in vineta
    assert not re.search(r"no pasa de|se detiene|techo|tope", vineta), vineta


def test_prosa_clase_3_p5_la_raiz_el_bono_de_min_y_la_c_como_delta():
    """#39 · La vuelta a mano de «MCTS con UCT» (Ola 3: en P5b, con N y V̂ en
    vez de G/N): R con N = 4 y suma 0; a con su simulación (+1) más las de
    sus hijos, N = 3 y V̂ = 1/3; los puntajes de R (1.01 y 0.18) y de MIN en
    a (N = 3, bono √(ln 3) ≈ 1.05, −0.05 y −2.05, baja a a2); sin bono, b
    quedaría condenada porque a ya ganó dos. La c como δ (10 % con
    N(s) = 100) vive en el bono y la fija test_prosa_clase_3_p6_tabla_c_delta;
    «con G/N es como usar c = 2» se retira (plan §5.1 elimina G/N)."""
    texto = _pagina(P5b)
    limpio = _limpio(texto)
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    antes = vuelta["antes"]
    nv = j.mcts_nv(antes)
    m = re.search(r"a: su simulación \((\+?-?\d)\) más las de sus hijos: N=(\d+) y suma (\+?-?\d+), "
                  r"así que \\widehat V\(a\)=(\d+/\d+)", limpio)
    _, _, u_a = j.MCTS_ARBOL["a"]
    assert int(m[1]) == u_a and (int(m[2]), F(m[4])) == nv["a"]
    assert int(m[3]) == nv["a"][0] * nv["a"][1]
    assert nv["a"][0] == 1 + sum(nv[h][0] for h in ("a1", "a2"))
    # Paso 1 · R (MAX): a 1/3 + √(ln 4/3) ≈ 1.01; b −1 + √(ln 4) ≈ 0.18.
    m = re.search(r"Paso 1 · Selección en R \(MAX, N=(\d+)\)\. Los puntajes son a: .*?=(\d+\.\d+); "
                  r"b: .*?=(\d+\.\d+)\. Baja a ([ab])\.", limpio)
    pr = vuelta["puntajes"]["r"]
    assert int(m[1]) == nv["r"][0] and (m[2], m[3]) == (_d(pr["a"]), _d(pr["b"]))
    assert m[4] == j.mejor(pr) == vuelta["camino"][1]
    # Paso 2 · a (MIN): bono √(ln 3) ≈ 1.05; a1 +1 − 1.05 = −0.05; a2 −1 − 1.05 = −2.05.
    bono = j.bono_ucb(antes["a"][1], 1, 1)
    m = re.search(rf"Paso 2 · Selección en a \(MIN, N=(\d+)\)\. Las dos respuestas llevan una "
                  rf"visita, con bono \\sqrt\\ln(\d+)≈({_NUM})\. Los puntajes son a1: "
                  rf"({_NUM})-({_NUM})=({_NUM}); a2: ({_NUM})-({_NUM})=({_NUM})\. MIN baja a (a\d)",
                  limpio)
    assert int(m[1]) == int(m[2]) == antes["a"][1] and m[3] == _d(bono)
    # N(s) = 3 cuenta la simulacion propia de a: no es la suma de sus hijos,
    # asi que el puntaje sale de mcts_vuelta (que da −Q̂ + bono para MIN).
    puntajes = vuelta["puntajes"]["a"]
    for h, (q, b, p) in zip(("a1", "a2"), ((m[4], m[5], m[6]), (m[7], m[8], m[9]))):
        assert (_x(q), b, p) == (nv[h][1], _d(bono), _d(-puntajes[h])), h
    assert m[10] == j.mejor(puntajes) == vuelta["camino"][2]
    # Sin bono, b quedaría condenada: a ya ganó dos y su promedio no llega a −1.
    m = re.search(r"Tras una sola partida, \\widehat Q\(R,b\)=(-\d+)\. a ya ganó (\w+) y su "
                  r"promedio nunca baja a (-\d+)\.", limpio)
    g_a, n_a = antes["a"]
    assert int(m[1]) == nv["b"][1] == int(m[3]) == -1 and {"una": 1, "dos": 2}[m[2]] == g_a > 0
    assert j.exponente_de_c(1) == F(1, 2)
    con_g = j.uct_ejercicio(c=1, victorias=True)
    con_u = j.puntajes_ucb(j.EJERCICIO_MCTS, c=2)
    assert all(_isclose_f(2 * con_g[k] - 1, con_u[k]) for k in con_u)


def test_prosa_clase_3_p5_monte_carlo_plano_no_es_mcts():
    """Auditoría de la 7.3: no se aplana MCTS a «promedio de partidas al
    azar». Ola 3: Monte Carlo plano vive en «Simular partidas» (P5) y MCTS
    en «MCTS con UCT» (P5b), así que «Las secciones 1 a 3 / desde la sección
    4» se retira (dejó de ser cierta). Cada summary dice lo suyo; los
    resúmenes separan: plano converge a Q_azar; UCT elige por puntaje dentro
    del árbol. Además: lo que pide son las reglas (A, T, S_F y U), la
    expansión toma la primera jugada que falta (como uct_tpm), la garantía de
    UCT es «con c > 0 fija» (la fila «¿Garantiza V?» de la ficha de siete
    rasgos pasó a «Garantía:» de las seis propiedades), y AlphaGo mezcla red
    y simulación con λ = 0.5 (verificación)."""
    texto = _pagina(P5)
    mcts = _pagina(P5b)
    resumen = texto.split("\n---", 1)[0]
    # el summary lo dice en palabras (ola 4 r1); el símbolo, en el cuerpo
    assert re.search(r'^summary: ".*Monte Carlo plano promedia su U por jugada de la raíz y '
                     r'converge a lo que paga jugar si los dos eligen al azar', resumen, re.M)
    assert r"$\widehat Q(s_{\text{raíz}},a)$ estima $Q_{\text{azar}}(s_{\text{raíz}},a)$" \
        in texto
    assert re.search(r'^summary: ".*elige el mayor Q̂ \+ bono en MAX y el menor Q̂ − bono en MIN',
                     mcts.split("\n---", 1)[0], re.M)
    assert "Monte Carlo plano guarda ese promedio por jugada de la raíz, sin construir un árbol" \
        in texto
    llevarse = _llevarse(texto)
    assert llevarse.startswith("## Lo que hay que llevarse - Monte Carlo plano estima")
    assert "MCTS estima una jugada simulando" not in llevarse
    assert re.search(r"Ese promedio converge a Q_azar", llevarse)
    assert re.search(r"- MCTS es la familia; UCT, su miembro con UCB\. Cada vuelta selecciona, "
                     r"expande a lo más un nodo, simula al azar y retropropaga el mismo U\.",
                     _llevarse(mcts))
    # Lo que pide: todas las piezas de las reglas, no solo A y T.
    tabla = _tabla(texto, "jue-c3-eval-contra-mcts")
    assert _c(tabla[1][2]) == "Reglas: A,T,S_F,U"
    assert "Si A,T,S_F,U describen el juego nuevo" in _limpio(_respuesta(texto, "jue-c3-ej-cambio"))
    assert "Solo $A$ y $T$" not in texto and "Solo usa $A$ y $T$" not in texto
    # La expansión, en orden fijo: uct_tpm agrega el primer hijo que falta.
    assert "Agrega la primera jugada pendiente, en el orden dado" in " ".join(mcts.split())
    raiz = len(j.ARBOL_TPM)
    assert [c[-1] for c in j.uct_tpm(1, raiz, 1)["caminos"]] == [(i,) for i in range(raiz)]
    # UCT llega con cualquier c > 0 fija.
    assert re.search(r"- \*\*Garantía:\*\* en un árbol finito, con \$c>0\$ fija y vueltas sin "
                     r"límite, los promedios tienden a los valores de minimax", mcts)
    # AlphaGo: λ = 0.5, la fila de la verificación.
    ver = (UNIDAD.parent.parent / "docs/verificacion/juegos/0_index.md").read_text(encoding="utf-8")
    lam = re.search(r"λ = (\d+(?:\.\d+)?) fue la mejor", ver)[1]
    assert re.search(r"mitad y mitad \(\\lambda=(\d+(?:\.\d+)?)\)", _limpio(mcts))[1] == lam
    assert F(lam) == F(1, 2)


# ---- p6 · corridas y c↔δ (aclarar-bono-y-mcts)
#
# Pruebas de FUENTE: fijan contra juegos.py las cifras nuevas de la p6 (el
# reparto por corrida que esconde el promedio de jue-c3-bandido, el tope de
# «a veces al azar», la δ que esconde cada c, y los puntajes de las vueltas
# 5 y 6 de la corrida que se atora). Las de prosa las agregan las paginas.

import math  # noqa: E402

def test_p6_corridas_siempre_el_mejor_promedio_es_todo_o_nada():
    """El 0.85 de jue-c3-bandido no es «85 % en x»: son 34 corridas casi en
    1 y 6 atoradas casi en 0 (5 en y, 1 en z)."""
    r = j.reparto_bandido()
    mp = r["mejor_promedio"]
    assert mp["n"] == len(mp["fracciones"]) == j.CORRIDAS_BANDIDO == 40
    assert mp["atoradas"] == 6 and mp["n"] - mp["atoradas"] == 34
    assert mp["en"] == {"y": 5, "z": 1}
    # Todo o nada: ninguna corrida entre 0.01 y 0.99.
    assert all(x < 0.01 or x > 0.99 for x in mp["fracciones"])
    assert round(mp["minimo"], 4) == 0.0001 and round(mp["maximo"], 4) == 0.9998
    assert round(mp["mediana"], 4) == 0.9996
    assert round(mp["promedio"], 2) == 0.85


def test_p6_corridas_las_otras_tres_reglas_no_se_atoran():
    r = j.reparto_bandido()
    esperado = {  # (mín, mediana, máx) a 3 decimales
        "a_veces_al_azar": (0.903, 0.932, 0.938),
        "ucb": (0.923, 0.945, 0.959),
        "ucb_c1": (0.955, 0.994, 0.999)}
    for fila, (mn, med, mx) in esperado.items():
        d = r[fila]
        assert d["atoradas"] == 0 and not d["en"], fila
        assert (round(d["minimo"], 3), round(d["mediana"], 3), round(d["maximo"], 3)) \
            == (mn, med, mx), fila


def test_p6_corridas_el_promedio_es_el_de_la_figura_acumulada():
    """El reparto y jue-c3-bandido leen las mismas corridas: el promedio de
    las fracciones finales es, bit a bit, la ultima marca de tabla_bandido."""
    r, t = j.reparto_bandido(), j.tabla_bandido()
    fin = max(j.MARCAS_BANDIDO)
    assert list(r) == list(t) == list(j.FILAS_BANDIDO)
    for fila, (regla, c) in j.FILAS_BANDIDO.items():
        assert r[fila]["promedio"] == t[fila][fin], fila
        assert r[fila]["fracciones"] == j.fracciones_finales(
            regla, j.MUS_HILO, fin, j.CORRIDAS_BANDIDO, c)
    # Una corrida suelta: la fraccion final es N(x)/vueltas de bandido.
    b = j.bandido("mejor_promedio", j.MUS_HILO, fin, j.SEMILLA_ATORA)
    assert r["mejor_promedio"]["fracciones"][j.SEMILLA_ATORA - 1] == b["N"]["x"] / fin
    assert max(b["N"], key=b["N"].get) == "z"


def test_p6_el_tope_de_a_veces_al_azar_es_esperado_no_un_techo():
    """0.9 + 0.1/3 = 14/15: el promedio de las 40 corridas queda debajo, pero
    14 corridas lo pasan (tiraron al azar menos de 1 de cada 10)."""
    tope = j.tope_a_veces_al_azar()
    assert tope == F(14, 15) and f"{float(tope):.4f}" == "0.9333"
    assert j.tope_a_veces_al_azar(n_jugadas=2, al_azar=0.2) == F(9, 10)
    az = j.reparto_bandido()["a_veces_al_azar"]
    assert az["promedio"] < tope
    assert sum(x > tope for x in az["fracciones"]) == 14


def test_p6_c_es_delta_disfrazada():
    """δ = N(s)^−c²/2 da el margen c·√(ln N(s)/N(s,a)). La prosa no dice
    «δ disfrazada»: c fija el exponente, y δ sigue cambiando con N(s)
    (auditoría de la 7.3). Ola 3: la frase «k=c^2/2» se re-ancla a
    «δ=N(s)^-c^2/2» del bloque 3 (plan §5.1 elimina la k); la fuente se
    queda."""
    texto = _pagina(P6)
    assert "disfrazada" not in texto
    assert "sale \\delta=N(s)^-c^2/2." in _seccion(texto, 3)
    assert j.exponente_de_c(1) == F(1, 2)
    assert math.isclose(j.exponente_de_c(j.C_TEORIA), 4)
    assert math.isclose(j.exponente_de_c(math.sqrt(2)), 1)
    assert j.delta_de_c(1, 100) == 0.1
    assert math.isclose(j.delta_de_c(j.C_TEORIA, 100), 1e-8)
    for c in (0.5, 1, math.sqrt(2), 2, j.C_TEORIA, 5):
        for n_padre in (4, 100, 1000, 10_000):
            for n in (1, 3, 10, 30, 60):
                assert math.isclose(j.margen(j.delta_de_c(c, n_padre), n),
                                    j.bono_ucb(n_padre, n, c)), (c, n_padre, n)


def test_p6_puntajes_de_las_vueltas_5_y_6_de_la_corrida_36():
    """UCB con c = 2√2, semilla 36. Vuelta 5 (N(s) = 4): z gana por poco,
    2.35 contra 2.33 de x y de y. Vuelta 6 (N(s) = 5): x 2.59 (empatada con
    y; gana x por ir primero) contra z 1.74."""
    n5, p5 = j.puntajes_ucb_en_vuelta(5)
    n6, p6 = j.puntajes_ucb_en_vuelta(6)
    assert (n5, n6) == (4, 5)
    assert {a: f"{v:.2f}" for a, v in p5.items()} == {"x": "2.33", "y": "2.33", "z": "2.35"}
    assert {a: f"{v:.2f}" for a, v in p6.items()} == {"x": "2.59", "y": "2.59", "z": "1.74"}
    assert p5["x"] == p5["y"] and p6["x"] == p6["y"]
    # Es la corrida de verdad: la jugada de mayor puntaje es la que eligio.
    elecciones = j.bandido("ucb", j.MUS_HILO, 6, j.SEMILLA_ATORA)["elecciones"]
    assert (j.mejor(p5), j.mejor(p6)) == (elecciones[4], elecciones[5]) == ("z", "x")
    # A mano: x en la vuelta 5 es −1 + 2√2·√(ln 4 / 1).
    assert math.isclose(p5["x"], -1 + j.C_TEORIA * math.sqrt(math.log(4)))
    assert math.isclose(p5["z"], 0 + j.C_TEORIA * math.sqrt(math.log(4) / 2))


# ---- p6 · pago por vuelta y corridas que eligen x (aclarar-bono-y-mcts)
#
# Pruebas de FUENTE de las dos figuras que reemplazan a jue-c3-bandido (la
# fraccion ACUMULADA en x mezclaba el costo de explorar con las corridas
# atoradas; el profesor no la entendio, 2026-10-12): jue-c3-pago (cuanto paga
# cada regla) y jue-c3-eligiendo-x (cuantas corridas eligen x, no acumulado).
# Todo exacto, en Fraction: U es ±1 y los conteos son enteros.

MARCAS_CITADAS = (10, 100, 1000, 10000)


def test_p6_pago_por_vuelta_de_cada_regla():
    t = j.tabla_pago()
    assert list(t) == list(j.FILAS_BANDIDO)
    esperado = {
        "mejor_promedio": (F(2, 5), F(213, 400), F(1087, 2000), F(54311, 100000)),
        "a_veces_al_azar": (F(77, 200), F(1043, 2000), F(2803, 5000), F(22571, 40000)),
        "ucb": (F(59, 200), F(397, 1000), F(10389, 20000), F(29, 50)),
        "ucb_c1": (F(17, 50), F(1027, 2000), F(5831, 10000), F(119611, 200000))}
    for fila, valores in esperado.items():
        assert tuple(t[fila][m] for m in MARCAS_CITADAS) == valores, fila
    fin = {f: f"{float(d[10000]):.3f}" for f, d in t.items()}
    assert fin == {"mejor_promedio": "0.543", "a_veces_al_azar": "0.564",
                   "ucb": "0.580", "ucb_c1": "0.598"}
    # Al final el orden es el de la exploracion bien hecha: sin bono, lo
    # peor; UCB con c = 1, casi lo mejor posible (μ(x) = 0.6) sin llegar.
    v = [t[f][10000] for f in ("mejor_promedio", "a_veces_al_azar", "ucb", "ucb_c1")]
    assert v == sorted(v) and v[-1] < j.MUS_HILO["x"]
    # Al principio UCB paga lo que explora: en N(s) = 10 y 100 va ultimo.
    for m in (10, 100):
        assert min(t, key=lambda f: t[f][m]) == "ucb", m


def test_p6_pago_de_una_corrida_es_la_suma_de_sus_u():
    b = j.bandido("ucb", j.MUS_HILO, 1000, 7)
    suma = 0
    for u in b["resultados"]:
        suma += u
    finales = j.pagos_finales("ucb", j.MUS_HILO, 1000, 7)
    assert finales[6] == F(suma, 1000)


def test_p6_pago_siempre_el_mejor_promedio_tiene_tres_montones():
    """El 0.543 promedia 34 corridas cerca de 0.6 (en x), 5 cerca de 0.3 (en
    y) y 1 en −0.21 (en z): el reparto de las corridas, no un pago tipico."""
    p = sorted(j.pagos_finales("mejor_promedio", j.MUS_HILO, 10000, 40))
    assert len(p) == 40
    assert p[0] == F(-1039, 5000)            # −0.2078
    assert all(0.28 < x < 0.32 for x in p[1:6])
    assert all(0.58 < x < 0.63 for x in p[6:])
    for f in ("a_veces_al_azar", "ucb", "ucb_c1"):
        regla, c = j.FILAS_BANDIDO[f]
        q = j.pagos_finales(regla, j.MUS_HILO, 10000, 40, c)
        assert max(q) - min(q) < 0.06, f        # un solo monton


def test_p6_pago_esperado_del_reparto():
    """(34·0.6 + 5·0.3 + 1·(−0.2))/40 = 21.7/40 = 0.5425; simulado 0.54311."""
    e = j.pago_esperado_reparto()
    assert e["en"] == {"x": 34, "y": 5, "z": 1}
    assert e["esperado"] == (34 * F(3, 5) + 5 * F(3, 10) + 1 * F(-1, 5)) / 40 == F(217, 400)
    assert f"{float(e['esperado']):.4f}" == "0.5425"
    simulado = j.tabla_pago()["mejor_promedio"][10000]
    assert abs(simulado - e["esperado"]) < F(1, 1000)
    # Las reglas que no se atoran: las 40 en x, 0.6 esperado.
    assert j.pago_esperado_reparto("ucb")["esperado"] == F(3, 5)


def test_p6_corridas_que_eligen_x():
    """Ventana de 10 vueltas (N(s) − 9 .. N(s)), 40 corridas: 400 elecciones
    por punto. Sin bono se aplana en 34/40 = 85 % desde N(s) = 100: las 6
    atoradas no eligen x en esas ventanas. «A veces al azar», cerca de 0.9 + 0.1/3."""
    assert j.VENTANA_ELIGIENDO == 10
    t = j.tabla_eligiendo_x()
    assert list(t) == list(j.FILAS_BANDIDO)
    esperado = {
        "mejor_promedio": (F(49, 80), F(17, 20), F(17, 20), F(17, 20)),
        "a_veces_al_azar": (F(241, 400), F(21, 25), F(93, 100), F(37, 40)),
        "ucb": (F(167, 400), F(13, 20), F(367, 400), F(79, 80)),
        "ucb_c1": (F(109, 200), F(333, 400), F(199, 200), F(1))}
    for fila, valores in esperado.items():
        assert tuple(t[fila][m] for m in MARCAS_CITADAS) == valores, fila
    mp = t["mejor_promedio"]
    assert all(mp[m] == F(34, 40) for m in j.MARCAS_BANDIDO if m >= 100)
    assert all(abs(t["a_veces_al_azar"][m] - j.tope_a_veces_al_azar()) < F(1, 50)
               for m in j.MARCAS_BANDIDO if m >= 500)
    # Una vuelta suelta (ventana 1) en la ultima: lo mismo, sin promediar.
    una = j.eligiendo_la_mejor("mejor_promedio", j.MUS_HILO, (10000,), 40, ventana=1)
    assert una[10000] == F(34, 40)
    # «Entre las vueltas 100 y 10 000, las 6 atoradas no eligen x» (la
    # figura): la ultima vez que alguna eligio x cae antes de la primera
    # ventana citada (91..100). No dice «nunca»: la semilla 20 la probo
    # hasta la vuelta 20.
    regreso = j.regreso_de_atoradas()
    ultima = max(r["ultima_x"] for r in regreso.values())
    assert len(regreso) == 6 and 1 < ultima < 100 - j.VENTANA_ELIGIENDO + 1


def test_p6_eligiendo_x_no_es_acumulada():
    """La ventana mira solo sus vueltas: con ventana = N(s) es la fraccion
    acumulada de fraccion_en_la_mejor, y con 10 ya no."""
    marcas = (10, 100)
    acum = j.fraccion_en_la_mejor("ucb", j.MUS_HILO, marcas, 5)
    for m in marcas:
        v = j.eligiendo_la_mejor("ucb", j.MUS_HILO, (m,), 5, ventana=m)[m]
        assert abs(float(v) - acum[m]) < 1e-12
    assert j.eligiendo_la_mejor("ucb", j.MUS_HILO, (100,), 5)[100] != \
        j.eligiendo_la_mejor("ucb", j.MUS_HILO, (100,), 5, ventana=100)[100]


# ------------------------- 7.3.7: un arbol, todos los algoritmos (T±) ---
#
# Cada cifra de la tabla de la pagina 7.3.7 y del interactivo, recalculada.
# Las convenciones (desempates, orden, semillas) estan en los docstrings de
# juegos.py; si cambian, estas cifras cambian y la prosa tambien.

def test_tpm_es_t_con_una_hoja_mas_en_d():
    """Misma forma que T salvo D: tres hijos. 15 nodos, finales en {−1, 0, +1}
    con un solo empate, y una sola captura, ix."""
    assert [len(h) for h in j.ARBOL_TPM] == [len(h) for h in j.ARBOL_T][:2] + [3]
    assert [len(c) for c in j.ARBOL_TPM[1]] == [len(c) for c in j.ARBOL_T[1]]
    assert j.contar_nodos(j.ARBOL_TPM) == j.contar_nodos(j.ARBOL_T) + 1 == 15
    hojas = [j.nodo_en(j.ARBOL_TPM, c) for c in j.nombres_hojas_tpm()]
    assert set(hojas) <= {-1, 0, 1} and hojas.count(0) == 1
    assert sorted(j.ids_tpm().values()) == sorted(
        ["R", "I", "C", "D", "C1", "C2", "i1", "ix", "c1a", "c1b", "c2a", "c2b",
         "d1", "d2", "d3"])
    assert [j.ids_tpm()[c] for c in j.CAPTURAS_TPM] == ["ix"]
    assert j.nodo_en(j.ARBOL_TPM, (0, 1)) == -1      # la captura gana para MIN
    assert j.EVAL_TPM == {"I": 60, "C": 20, "D": 10, "C1": 10, "C2": 50}


def test_tpm_con_la_forma_exacta_de_t_ningun_dado_cambia_la_jugada():
    """Por que D tiene tres hojas: con dos, un volado entre −1 y +1 vale 0 y
    a lo mas empata. Busqueda exhaustiva sobre {−1, 0, +1}^8."""
    assert j.dados_que_cambian_la_jugada_forma_t(2) == 0
    # Con tres hojas en D si se puede: T± es uno (test_tpm_el_dado_en_d...).


def test_tpm_minimax_y_alfa_beta():
    assert j.minimax_tpm() == ("centro", 0, {"izq": -1, "centro": 0, "der": -1}, 15)
    # En el orden dado, d1 = −1 llega con α = 0 y corta d2 y d3; c2a = +1
    # corta c2b. Al reves, la unica hoja que se ahorra es i1.
    assert j.alfa_beta_tpm("dado") == ("centro", 0, 12, [(1, 1, 1), (2, 1), (2, 2)])
    assert j.alfa_beta_tpm("al revés") == ("centro", 0, 14, [(0, 0)])
    assert j.alfa_beta_tpm("centro primero")[:3] == ("centro", 0, 12)


def test_tpm_el_dado_en_d_cambia_la_jugada():
    jugada, v = j.expectiminimax_tpm()
    assert jugada == "der"
    assert (v["I"], v["C"], v["D"], v["R"]) == (-1, 0, F(1, 3), F(1, 3))
    assert j.minimax_tpm()[0] != jugada


def test_tpm_el_horizonte_engana_a_d_1_y_la_quietud_lo_arregla():
    assert j.corte_tpm(1) == ("izq", 60, {"izq": 60, "centro": 20, "der": 10}, 4)
    assert j.corte_tpm(2) == ("centro", 10, {"izq": -100, "centro": 10, "der": -100}, 11)
    assert j.corte_tpm(3) == ("centro", 0, {"izq": -100, "centro": 0, "der": -100}, 15)
    jugada, valor, ws, nodos, generados = j.quietud_tpm(1)
    assert (jugada, valor, ws, nodos) == ("centro", 20,
                                          {"izq": -100, "centro": 20, "der": 10}, 5)
    assert [j.ids_tpm()[c] for c in generados] == ["R", "I", "ix", "C", "D"]
    assert nodos < j.corte_tpm(2)[3]
    # La quietud arregla la jugada, no el valor: centro vale 0, no 20.
    assert valor != 100 * j.minimax_tpm()[1]


def test_tpm_profundizacion_iterativa():
    filas, total = j.iterativa_tpm()
    assert [(d, jugada, valor, nodos) for d, _, jugada, valor, nodos in filas] == [
        (1, "izq", 60, 4), (2, "centro", 10, 9), (3, "centro", 0, 12)]
    assert [orden[0] for _, orden, _, _, _ in filas] == ["izq", "izq", "centro"]
    assert total == 25


def test_tpm_monte_carlo_plano_es_todos_al_azar():
    """El limite de MC plano es expectiminimax con TODOS al azar, tambien C1 y
    C2 (de MAX): juega der. Con solo el rival al azar juega centro."""
    jugada, mu = j.todos_al_azar_tpm()
    assert (jugada, mu) == ("der", {"izq": 0, "centro": F(-1, 4), "der": F(1, 3)})
    for a, h in zip(j.JUGADAS_RAIZ, j.ARBOL_TPM):
        d = j.distribucion_simulacion(h)
        assert sum(u * p for u, p in d.items()) == mu[a]
    assert j.rival_al_azar_tpm() == ("centro", {"izq": 0, "centro": F(1, 2), "der": F(1, 3)})


# {k simulaciones por jugada: (semillas que entregan izq, centro, der en
# 1000, de ellas cuantas por empate de promedios)}
REPARTO_MC_TPM = {5: ((353, 106, 541), 233), 10: ((269, 53, 678), 157),
                  50: ((39, 1, 960), 15)}


def test_tpm_reparto_de_monte_carlo_plano():
    assert j.SIMS_MC_TPM == (5, 10, 50) and j.SEMILLAS_MC_TPM == 1000
    for k, (cuentas, empates) in REPARTO_MC_TPM.items():
        reparto, e = j.reparto_mc_plano_tpm(k)
        assert tuple(reparto.values()) == cuentas and e == empates, k
    assert j.mc_plano_tpm(5, j.SEMILLA_TPM) == ("der", {"izq": -3, "centro": -2, "der": 3})


def test_tpm_las_simulaciones_de_monte_carlo_plano_son_las_de_su_corrida():
    """La radiografia dibuja cada partida de la corrida de la pagina: con el
    mismo generador suman lo mismo que mc_plano_tpm, tocan los mismos nodos
    que _tocados_mc, cada camino acaba en un final y su U es el de ese final."""
    for k in j.SIMS_MC_TPM:
        sims = j.simulaciones_mc_plano_tpm(k, j.SEMILLA_TPM)
        _, sumas = j.mc_plano_tpm(k, j.SEMILLA_TPM)
        assert len(sims) == k * len(j.ARBOL_TPM)
        assert {a: sum(u for b, _, u in sims if b == a) for a in j.JUGADAS_RAIZ} == sumas
        tocados = {()} | {c[:m] for _, c, _ in sims for m in range(1, len(c) + 1)}
        assert tocados == j._tocados_mc(k, j.SEMILLA_TPM)
        for a, c, u in sims:
            assert j.JUGADAS_RAIZ[c[0]] == a and j.nodo_en(j.ARBOL_TPM, c) == u
    # La corrida de la radiografia, partida por partida.
    finales = [j.ids_tpm()[c] for _, c, _ in j.simulaciones_mc_plano_tpm(5, j.SEMILLA_TPM)]
    assert finales == ["ix", "ix", "i1", "ix", "ix", "c2b", "c2b", "c1a", "c2a", "c1b",
                       "d3", "d3", "d3", "d1", "d2"]


def test_tpm_probabilidad_exacta_de_monte_carlo_plano():
    p5 = j.prob_mc_plano_tpm(5)
    assert p5 == {"izq": F(487919, 1327104), "centro": F(41723, 442368),
                  "der": F(22313, 41472)}
    assert sum(p5.values()) == 1
    pct = {k: {a: round(float(x) * 100, 1) for a, x in j.prob_mc_plano_tpm(k).items()}
           for k in (5, 10, 50)}
    assert pct == {5: {"izq": 36.8, "centro": 9.4, "der": 53.8},
                   10: {"izq": 27.6, "centro": 4.7, "der": 67.7},
                   50: {"izq": 5.4, "centro": 0.0, "der": 94.6}}
    # Las 1000 semillas caen cerca de la probabilidad exacta.
    for k, (cuentas, _) in REPARTO_MC_TPM.items():
        for a, n in zip(j.JUGADAS_RAIZ, cuentas):
            assert abs(n / 1000 - float(j.prob_mc_plano_tpm(k)[a])) < 0.03, (k, a)


def test_tpm_uct_acaba_en_centro():
    """La vuelta desde la que centro es la mas simulada hasta la 200, en 500
    semillas. Ninguna se queda fuera."""
    assert (j.VUELTAS_UCT_TPM, j.SEMILLAS_UCT_TPM) == (200, 500)
    esperado = {1: (4, 8, 18, 31, 34), j.C_TEORIA: (4, 13, 29, 36, 39)}
    for c, cifras in esperado.items():
        r = j.reparto_uct_tpm(c)
        assert (r["minimo"], r["p10"], r["mediana"], r["p90"], r["maximo"]) == cifras, c
        assert r["nunca"] == 0
        # Con c = 1, 47 semillas ponen a centro arriba desde la vuelta 6 o
        # antes: el alumno no veria el error de MC plano en ellas.
        assert sum(v <= 6 for v in r["vueltas"]) == {1: 47, j.C_TEORIA: 15}[c]


def test_tpm_la_corrida_de_uct_de_la_pagina():
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    assert "".join(a[0] for a in u["mas_simulada"]) == (
        "iii" + "cccc" + "d" * 10 + "c" * 23)
    assert j.vuelta_desde_la_que_tpm(1, j.SEMILLA_TPM) == 18
    raiz = {a: (u["N"][(i,)], u["S"][(i,)]) for i, a in enumerate(j.JUGADAS_RAIZ)}
    assert raiz == {"izq": (5, -3), "centro": (26, 0), "der": (9, -3)}
    assert len(u["N"]) == 15
    # En la vuelta 18 centro y der empatan con 7: entrega la primera, centro.
    u18 = j.uct_tpm(1, 18, j.SEMILLA_TPM)
    assert u18["N"][(1,)] == u18["N"][(2,)] == 7 and u18["mas_simulada"][-1] == "centro"


def test_tpm_tabla_de_la_pagina():
    """En el orden del curso; «garantiza» es el rasgo del algoritmo y
    «da_v_aqui» si el número coincide con V (0, o 1/3 con dado) en T±."""
    filas = j.tabla_t_pm()
    corto = [(f["algoritmo"], f["jugada"], f["valor"], f["tipo"], f["nodos"], f["da_v_aqui"])
             for f in filas]
    assert corto == [
        ("minimax", "centro", 0, "V", 15, True),
        ("expectiminimax, D es un dado", "der", F(1, 3), "V con dado", 15, True),
        ("alfa-beta, orden dado", "centro", 0, "V", 12, True),
        ("alfa-beta, orden al revés", "centro", 0, "V", 14, True),
        ("corte d = 1", "izq", 60, "valor con corte", 4, False),
        ("corte d = 2", "centro", 10, "valor con corte", 11, False),
        ("corte d = 3", "centro", 0, "valor con corte", 15, True),
        ("quietud, d = 1", "centro", 20, "valor con quietud", 5, False),
        ("profundización iterativa, d = 1, 2, 3", "centro", 0, "valor con corte", 25, True),
        ("Monte Carlo plano, 5 por jugada", "der", F(3, 5), "ū", 15, False),
        ("Monte Carlo plano, 10 por jugada", "der", F(2, 5), "ū", 15, False),
        ("Monte Carlo plano, 50 por jugada", "der", F(12, 25), "ū", 15, False),
        ("UCT, c = 1, 40 vueltas", "centro", 0, "ū", 15, True),
    ]
    assert [f["garantiza"] for f in filas] == [
        "Sí", "Sí, el V del juego con dado", "Sí, en la raíz", "Sí, en la raíz"] + \
        ["No, salvo si llega a los finales"] * 3 + \
        ["No, salvo si llega a los finales antes de cortar"] + \
        ["No, salvo si llega a los finales"] + ["No"] * 3 + \
        ["No (con tiempo sin límite converge a él, con cualquier c > 0)"]
    assert filas[9]["nota"] == "límite: der con μ = 1/3"
    # Los nodos no miden lo mismo en todas las filas: por eso las de
    # simulación traen también cuántas partidas jugaron (k por jugada en MC
    # plano, una por vuelta en UCT); las búsquedas, ninguna.
    assert [f["simulaciones"] for f in filas] == [None] * 9 + [15, 30, 150, 40]
    assert filas[-1]["simulaciones"] == j.VUELTAS_PAGINA_TPM


def test_alfa_beta_nunca_genera_mas_que_minimax_y_puede_generarlo_todo():
    """Propiedades de alfa-beta (7.2) y Radiografía (7.4): «con el mismo
    orden, nunca genera más nodos; con buen orden, muchos menos», y puede
    generarlo completo (tiempo hasta O(b^m); en la radiografía, «con mal
    orden puede generar los mismos nodos que minimax»). Ola 3: la ficha de
    siete rasgos se reemplazó por las seis propiedades. En el árbol de
    resultados, en cualquier orden de los hijos, a lo más los 15 de minimax;
    y en un árbol con el peor orden, alfa-beta los genera todos."""
    import itertools
    total = j.contar_nodos(j.ARBOL_TPM)
    for perm in itertools.permutations(range(3)):
        arbol = tuple(j.ARBOL_TPM[i] for i in perm)
        assert j.alfa_beta_arbol(arbol)["generados"] <= total
    peor = ((1, 2), (3, 4))      # el segundo MIN ve 3 y 4, los dos sobre α = 1: no corta
    assert j.alfa_beta_arbol(peor)["generados"] == j.contar_nodos(peor) == 7
    assert j.alfa_beta_arbol(((3, 4), (1, 2)))["generados"] < 7
    ficha = " ".join((CLASE_3.parent / "2_mirar_todo_y_podar" / "4_alfa_beta_como_algoritmo.md")
                     .read_text(encoding="utf-8").split())
    assert ("**Frente a los demás:** da el resultado de minimax con trabajo menor o igual. "
            "**Con el mismo orden, nunca genera más nodos**; con buen orden, muchos menos.") in ficha
    assert "tiempo entre $O(b^{m/2})$ y $O(b^m)$" in ficha
    assert "misma jugada, menos nodos" not in ficha
    rx = _limpio((CLASE_3.parent / "4_radiografia" / "1_un_arbol_todos_los_algoritmos.md")
                 .read_text(encoding="utf-8"))
    assert "con mal orden puede generar los mismos nodos que minimax" in rx
    assert "con menos nodos que minimax" not in rx


def test_tpm_la_quietud_no_garantiza_v_aunque_sus_capturas_lleguen_a_los_finales():
    """GARANTIZA_TPM["quietud"] dice «antes de cortar»: con todas las jugadas
    bajo d = 1 marcadas como captura, la quietud genera los 15 nodos y llega
    a todos los finales, pero en cada nodo de corte quedarse vale EVAL y
    decide (C1: EVAL 10 contra c1a = 0 y c1b = −100). Da centro con 10, no
    el 0 de minimax."""
    jq, vq, ws, generados, _ = j.quietud_con_todo_captura_tpm(1)
    assert generados == j.contar_nodos(j.ARBOL_TPM) == 15
    assert (jq, vq) == ("centro", 10) != (j.minimax_tpm()[0], 100 * j.minimax_tpm()[1])
    assert ws == {"izq": -100, "centro": 10, "der": -100}
    assert j.GARANTIZA_TPM["quietud"] == "No, salvo si llega a los finales antes de cortar"


def test_tpm_datos_del_interactivo():
    import json
    d = j.datos_interactivo_tpm()
    texto = json.dumps(d, ensure_ascii=False)
    assert json.loads(texto) == json.loads(json.dumps(d, ensure_ascii=False))
    assert len(d["nodos"]) == 15
    assert [n["id"] for n in d["nodos"] if n["captura"]] == ["ix"]
    a = d["algoritmos"]
    assert len(a["minimax"]["visitados"]) == 15
    assert len(a["alfa-beta, dado"]["visitados"]) == 12
    assert a["alfa-beta, dado"]["podados"] == ["c2b", "d2", "d3"]
    assert a["alfa-beta, al revés"]["podados"] == ["i1"]
    assert a["quietud d = 1"]["visitados"] == ["R", "I", "ix", "C", "D"]
    assert [x["nodos"] for x in a["profundización iterativa"]] == [4, 9, 12]
    # la iterativa poda donde corta (D en d = 2; C2 y D en d = 3), no bajo el horizonte
    assert [x["podados"] for x in a["profundización iterativa"]] == [
        [], ["d2", "d3"], ["c2b", "d2", "d3"]]
    assert a["Monte Carlo plano"]["reparto"][5] == {"izq": 353, "centro": 106, "der": 541}
    assert a["UCT"]["mas_simulada"][-1] == "centro"
    assert len(d["tabla"]) == len(j.tabla_t_pm())


def test_tpm_el_interactivo_trae_el_valor_de_cada_nodo_interno():
    """Minimax: V de los seis nodos internos, a mano: C1 = max(0, −1) = 0,
    C2 = max(+1, −1) = +1, C = min(0, +1) = 0, I = min(+1, −1) = −1,
    D = min(−1, +1, +1) = −1, R = 0."""
    a = j.datos_interactivo_tpm()["algoritmos"]
    V = {"R": 0, "I": -1, "C": 0, "D": -1, "C1": 0, "C2": 1}
    assert a["minimax"]["valores"] == {k: ["=", v] for k, v in V.items()}
    for c, n in j.ids_tpm().items():
        if n in V:
            assert V[n] == j.minimax_arbol(j.nodo_en(j.ARBOL_TPM, c), len(c) % 2 == 0)
    # alfa-beta: D (orden dado) e I (al revés) quedan como cota tras su corte.
    assert a["alfa-beta, dado"]["valores"] == {
        "R": ["=", 0], "I": ["=", -1], "C": ["=", 0], "D": ["≤", -1],
        "C1": ["=", 0], "C2": ["≥", 1]}
    assert a["alfa-beta, al revés"]["valores"] == {
        "R": ["=", 0], "I": ["≤", -1], "C": ["=", 0], "D": ["=", -1],
        "C1": ["=", 0], "C2": ["=", 1]}
    # Cada valor o cota es el que devolvio alfa-beta fail-soft, y no contradice a V.
    for orden in ("dado", "al revés"):
        r = j.alfa_beta_arbol(j.ARBOL_TPM, invertir=(orden == "al revés"))
        ids = j.ids_tpm()
        devuelto = {ids[c]: v for c, tipo, _, _, v, _ in r["traza"] if tipo != "hoja"}
        for n, (tipo, x) in a[f"alfa-beta, {orden}"]["valores"].items():
            assert devuelto[n] == x, (orden, n)
            assert {"=": V[n] == x, "≥": V[n] >= x, "≤": V[n] <= x}[tipo], (orden, n)
    # corte: arriba del corte, minimax sobre EVAL; en el corte, EVAL.
    assert a["corte d = 1"]["valores"] == {
        "R": ["=", 60], "I": ["EVAL", 60], "C": ["EVAL", 20], "D": ["EVAL", 10]}
    assert a["corte d = 2"]["valores"] == {
        "R": ["=", 10], "I": ["=", -100], "C": ["=", 10], "D": ["=", -100],
        "C1": ["EVAL", 10], "C2": ["EVAL", 50]}
    assert a["corte d = 3"]["valores"] == {k: ["=", 100 * v] for k, v in V.items()}
    for d in (1, 2, 3):
        ws = j.corte_tpm(d)[2]
        for jug, n in zip(j.JUGADAS_RAIZ, "ICD"):
            assert a[f"corte d = {d}"]["valores"][n][1] == ws[jug]
    # quietud: I deja de valer EVAL(I) = 60 al ver la captura ix.
    assert a["quietud d = 1"]["valores"] == {
        "R": ["=", 20], "I": ["quietud", -100], "C": ["quietud", 20], "D": ["quietud", 10]}
    # iterativa: el valor (o cota) que deja en cada nodo la traza de alfa-beta con corte.
    it = j.profundizacion_iterativa_t(j.escalar_arbol(j.ARBOL_TPM, 100), (1, 2, 3), j.EVAL_TPM)
    for x, (d, _, t) in zip(a["profundización iterativa"], it):
        estado = t["filas"][-1]["estado"]
        for n, (tipo, v) in x["valores"].items():
            assert estado[n]["v"] == v, (d, n)
    assert a["profundización iterativa"][2]["valores"] == {
        "R": ["=", 0], "I": ["=", -100], "C": ["=", 0], "D": ["≤", -100],
        "C1": ["=", 0], "C2": ["≥", 100]}


def test_tpm_el_interactivo_trae_los_nodos_de_cada_corrida_de_mc_plano():
    c = j.datos_interactivo_tpm()["algoritmos"]["Monte Carlo plano"]["corridas"]
    assert {k: x["nodos"] for k, x in c.items()} == {5: 15, 10: 15, 50: 15}
    fila = next(f for f in j.tabla_t_pm() if f["algoritmo"].startswith("Monte Carlo"))
    assert c[5]["nodos"] == fila["nodos"]


def test_tpm_el_interactivo_trae_uct_vuelta_por_vuelta():
    u = j.datos_interactivo_tpm()["algoritmos"]["UCT"]
    corrida = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    ids = j.ids_tpm()
    assert len(u["U"]) == len(u["por_vuelta"]) == j.VUELTAS_PAGINA_TPM
    assert set(u["U"]) <= {-1, 0, 1}
    # La ultima vuelta es la corrida entera de uct_tpm.
    assert u["por_vuelta"][-1] == {ids[c]: [corrida["N"][c], corrida["S"][c]]
                                   for c in corrida["N"]}
    # Cada vuelta es la de una corrida mas corta con la misma semilla.
    for t in (1, 5, 18, 40):
        corta = j.uct_tpm(1, t, j.SEMILLA_TPM)
        assert u["por_vuelta"][t - 1] == {ids[c]: [corta["N"][c], corta["S"][c]]
                                          for c in corta["N"] if corta["N"][c]}
    # Lo que la pagina cita: vuelta 18, centro y der con N = 7; al final centro 26 con ū 0.
    v18 = u["por_vuelta"][17]
    assert v18["C"] == [7, -1] and v18["D"] == [7, -1] and v18["R"] == [18, -4]
    assert u["por_vuelta"][4] == {"R": [5, -1], "I": [1, -1], "C": [2, 0], "D": [2, 0],
                                  "C1": [1, -1], "d1": [1, -1]}
    assert u["por_vuelta"][-1]["C"] == [26, 0]


def test_tpm_orden_en_que_cada_algoritmo_genera_los_nodos():
    """El orden que recorre la animacion de las radiografias (7.3.6), por
    nombre: preorden de izquierda a derecha, sin lo podado ni lo que queda
    detras del horizonte; la quietud mete la captura ix justo tras I; la
    iterativa, a d = 3, empieza por centro (la jugada de d = 2)."""
    ids = j.ids_tpm()

    def nombres(algoritmo):
        return [ids[c] for c in j.orden_generados_tpm(algoritmo)]

    assert nombres("minimax") == ["R", "I", "i1", "ix", "C", "C1", "c1a", "c1b",
                                  "C2", "c2a", "c2b", "D", "d1", "d2", "d3"]
    assert nombres("alfa-beta") == ["R", "I", "i1", "ix", "C", "C1", "c1a", "c1b",
                                    "C2", "c2a", "D", "d1"]
    assert nombres("corte") == ["R", "I", "C", "D"]
    assert nombres("quietud") == ["R", "I", "ix", "C", "D"]
    assert [[ids[c] for c in o] for o in j.orden_generados_tpm("iterativa")] == [
        ["R", "I", "C", "D"],
        ["R", "I", "i1", "ix", "C", "C1", "C2", "D", "d1"],
        ["R", "C", "C1", "c1a", "c1b", "C2", "c2a", "I", "i1", "ix", "D", "d1"]]
    # y cuadra con los conteos de cada algoritmo
    assert len(nombres("minimax")) == j.minimax_tpm()[3]
    assert len(nombres("alfa-beta")) == j.alfa_beta_tpm("dado")[2]
    assert len(nombres("corte")) == j.corte_tpm(1)[3]
    assert len(nombres("quietud")) == j.quietud_tpm(1)[3]
    assert [len(o) for o in j.orden_generados_tpm("iterativa")] == [
        f[4] for f in j.iterativa_tpm()[0]]
    with pytest.raises(ValueError):
        j.orden_generados_tpm("uct")


# ------------------------------- homologacion de la unidad 7 (Ola 0) ---
#
# Cifras nuevas del plan de homologacion (§2 decision 2, §6.2, §6.4): las
# trazas de 7.3 sobre el arbol de resultados, los tres Monte Carlo y
# Hoeffding. Las pruebas de contrato de la actualizacion minimax se corren
# tambien contra mutantes (monkeypatch) para comprobar que detectan la regla
# rota: respaldo por promedio, desconocido como cero, jugada legal oculta.


def test_homologacion_corte_en_el_arbol_de_resultados():
    """Minimax con corte a d = 1, 2, 3 en el árbol de resultados (finales en
    100·U, EVAL_TPM): jugada, valor de R, nodos y valores de cada nodo."""
    assert [j.decidir_con_corte_tpm(d) for d in (1, 2, 3)] == [
        ("izq", 60, 4), ("centro", 10, 11), ("centro", 0, 15)]
    assert [j.decidir_con_corte_tpm(d)[:2] for d in (1, 2, 3)] == [
        j.corte_tpm(d)[:2] for d in (1, 2, 3)]
    assert j.valores_con_corte_tpm(1) == {"R": 60, "I": 60, "C": 20, "D": 10}
    assert j.valores_con_corte_tpm(2) == {"R": 10, "I": -100, "C": 10, "C1": 10, "C2": 50,
                                          "D": -100}
    assert j.valores_con_corte_tpm(3) == {"R": 0, "I": -100, "C": 0, "C1": 0, "C2": 100,
                                          "D": -100}
    # Con d = 3 alcanza todos los finales: devuelve 100·V, no V.
    assert j.valores_con_corte_tpm(3)["R"] == 100 * j.minimax_tpm()[1]
    filas = j.filas_corte_tpm(2)
    assert filas[0] == (1, "2 · R", "−∞", "", "—")
    assert filas[-1][2:] == ("10", "", "centro")
    assert [f[3] for f in filas if f[1].endswith("· R") and f[3]] == [
        "-100 (I)", "10 (C)", "-100 (D)"]
    # La traza tiene una fila por evento: entra/regresa de I, C, C1, C2, D,
    # mas inicio, tres de la raiz y fin.
    t = j.traza_decidir(j.ARBOL_TPM_100, profundidad=2, evaluar=j.EVAL_TPM)
    assert len(filas) == len(t["filas"])


def test_homologacion_iterativa_en_el_arbol_de_resultados():
    """Profundización iterativa sin poda y con alfa-beta, con y sin la jugada
    anterior primero, en el árbol de resultados."""
    for anterior_primero in (False, True):
        corridas = j.iterativa_sin_poda_tpm(anterior_primero=anterior_primero)
        assert [(d, jugada, valor, nodos) for d, _, jugada, valor, nodos in corridas] == [
            (1, "izq", 60, 4), (2, "centro", 10, 11), (3, "centro", 0, 15)]
        assert sum(c[4] for c in corridas) == 30
    assert [c[1] for c in j.iterativa_sin_poda_tpm(anterior_primero=True)] == [
        ["izq", "centro", "der"], ["izq", "centro", "der"], ["centro", "izq", "der"]]
    con, total = j.iterativa_alfa_beta_tpm()
    assert (con, total) == j.iterativa_tpm()
    assert con == [(1, ["izq", "centro", "der"], "izq", 60, 4),
                   (2, ["izq", "centro", "der"], "centro", 10, 9),
                   (3, ["centro", "izq", "der"], "centro", 0, 12)] and total == 25
    sin, total_sin = j.iterativa_alfa_beta_tpm(anterior_primero=False)
    assert [f[1] for f in sin] == [["izq", "centro", "der"]] * 3
    assert [(f[2], f[3], f[4]) for f in sin] == [("izq", 60, 4), ("centro", 10, 9),
                                                 ("centro", 0, 12)] and total_sin == 25
    # En este árbol poner primero la anterior no ahorra nodos con d = 3.
    assert j.tabla_nodos_generados_tpm() == {
        "sin poda": [4, 11, 15], "alfa-beta": [4, 9, 12], "iterativa": [4, 9, 12],
        "iterativa sin la anterior primero": [4, 9, 12]}
    # La búsqueda con d = 3, centro primero: llamadas, ventanas y tipos.
    t = j.traza_iterativa_tpm(3)
    assert j.llamadas_alfa_beta(t) == [
        ("C", -INF, INF, 0, None), ("C1", -INF, INF, 0, None), ("C2", -INF, 0, 100, "beta"),
        ("I", 0, INF, -100, "alfa"), ("D", 0, INF, -100, "alfa")]
    assert {n: k for n, (*_, k) in j.clases_transposicion(t).items()} == {
        "C": "exacto", "C1": "exacto", "C2": "piso", "I": "techo", "D": "techo"}
    assert t["orden_generados"] == ["R", "C", "C1", "0", "-100", "C2", "100", "I", "100",
                                    "-100", "D", "-100"]
    assert [j.valor_con_corte_hijo_tpm("C", k) for k in (0, 1, 2)] == [20, 10, 0]
    corridas, entrega = j.iterativa_con_reloj_tpm(["izq", "centro", "der"])
    assert [(c["d"], c["jugada"], c["generados"]) for c in corridas] == [
        (1, "izq", 4), (2, "centro", 9), (3, "centro", 12)]
    assert entrega == dict(jugada="centro", d=3, generados=25, linea=13, despues_de=None)
    # El parámetro nuevo no cambia el árbol T.
    assert j.iterativa_con_reloj_t(["izq", "centro", "der"]) == j.iterativa_con_reloj_t(
        ["izq", "centro", "der"], arbol=j.ARBOL_T)


def test_homologacion_expectiminimax_con_dado_en_d_y_q_azar():
    """Expectiminimax con un dado parejo en D (la ficha de la radiografía) y
    Q_azar = expectiminimax con los dos como dados."""
    assert j.expectiminimax_tpm() == ("der", {"I": -1, "C1": 0, "C2": 1, "C": 0,
                                              "D": F(1, 3), "R": F(1, 3)})
    q = j.q_azar_arbol(j.ARBOL_TPM)
    assert q == [0, F(-1, 4), F(1, 3)]
    _, todos = j.expectiminimax_tpm(("I", "C", "D", "C1", "C2"))
    assert q == [todos[n] for n in "ICD"]
    assert q == [j.todos_al_azar_tpm()[1][a] for a in j.JUGADAS_RAIZ]
    assert q != j.q_minimax_arbol(j.ARBOL_TPM) == [-1, 0, -1]
    # En el árbol de la refutación: Q_azar(A) = −10/3 > −10 = Q_azar(B).
    assert j.q_azar_arbol(j.ARBOL_REFUTACION) == [F(-10, 3), -10]
    assert j.expectiminimax_t(j.ARBOL_REFUTACION, ("I", "I3"))[1]["I"] == F(-10, 3)
    assert j.q_minimax_arbol(j.ARBOL_REFUTACION) == [-30, -10]
    assert j.valor_minimax_arbol(j.ARBOL_REFUTACION) == -10


def _violaciones_mc_minimax():
    """Las reglas del contrato de la actualización minimax (§6.2) que se
    rompen; [] si ninguna. Se corre normal y contra mutantes."""
    malas = []
    # 1. Respaldo max/min, no promedio: la refutación impuesta lleva Q̂(A) a −30.
    op = j.operadores_ante_la_refutacion()
    if (op["minimax_antes"], op["minimax_despues"], op["jugada_minimax"]) != (10, -30, "B"):
        malas.append("respaldo")
    # 2. Desconocido no es cero: tras una sola partida por A→p, MIN solo
    #    conoce p (+10); su V̂ es 10 (provisional) y B sigue desconocida.
    m = j.mc_minimax(j.ARBOL_REFUTACION, None, caminos=[(0, 0)])
    if m["V"][(0,)] != 10 or m["Q"] != [10, None] or m["exacto"][(0,)] or m["exacto"][()]:
        malas.append("desconocido")
    # 3. Todas las jugadas legales: con tiempo descubre el árbol entero y
    #    converge a V en cada nodo.
    for semilla in range(5):
        r = j.mc_minimax(j.ARBOL_TPM, 300, semilla)
        completo = set(j.ids_tpm()) | {()}
        if set(r["V"]) != completo or any(
                r["V"][c] != j.minimax_arbol(j.nodo_en(j.ARBOL_TPM, c), len(c) % 2 == 0)
                for c in completo):
            malas.append("legales")
            break
    return malas


def test_homologacion_mc_minimax_cumple_el_contrato():
    assert _violaciones_mc_minimax() == []


def test_homologacion_mc_minimax_mutante_promedio(monkeypatch):
    def promedio(es_max, qs):
        conocidas = [q for q in qs if q is not None]
        return F(sum(conocidas), len(conocidas)) if conocidas else None
    monkeypatch.setattr(j, "_respaldo_minimax", promedio)
    assert "respaldo" in _violaciones_mc_minimax()


def test_homologacion_mc_minimax_mutante_desconocido_cero(monkeypatch):
    def cero(es_max, qs):
        qs = [0 if q is None else q for q in qs]
        return max(qs) if es_max else min(qs)
    monkeypatch.setattr(j, "_respaldo_minimax", cero)
    assert "desconocido" in _violaciones_mc_minimax()


def test_homologacion_mc_minimax_mutante_oculta_una_jugada(monkeypatch):
    original = j.acciones_arbol
    monkeypatch.setattr(j, "acciones_arbol", lambda nodo: original(nodo)[:-1] or original(nodo))
    assert "legales" in _violaciones_mc_minimax()


def test_homologacion_mc_minimax_finales_exactos_y_entrega():
    """Un final da su Q exacta en la primera visita; un antecesor queda
    resuelto solo cuando lo conocido basta; sin muestras, la primera jugada."""
    m = j.mc_minimax(j.ARBOL_REFUTACION, None, caminos=[(1,)])
    assert m["Q"] == [None, -10] and m["exacto"][(1,)] and not m["exacto"][()]
    assert m["jugada"] == 1
    m = j.mc_minimax(j.ARBOL_REFUTACION, None, caminos=[(0, 2, 0)])
    # x tiene una sola jugada, final −30: exacto, y MIN en A ya no puede bajar más.
    assert m["V"][(0, 2)] == -30 and m["exacto"][(0, 2)] and m["exacto"][(0,)]
    assert m["Q"] == [-30, None] and not m["exacto"][()]
    assert j.mc_minimax(j.ARBOL_REFUTACION, 0)["jugada"] == 0          # sin muestras
    # Empate entre conocidas: la primera.
    assert j.mc_minimax(((1,), (1,)), None, caminos=[(1, 0), (0, 0)])["jugada"] == 0
    # En T±, un MIN con un final −1 queda resuelto en esa visita; la raíz no.
    m = j.mc_minimax(j.ARBOL_TPM, None, caminos=[(0, 1)])
    assert m["V"][(0,)] == -1 and m["exacto"][(0,)] and not m["exacto"][()]
    assert m["Q"] == [-1, None, None]
    m = j.mc_minimax(j.ARBOL_TPM, None, caminos=[(0, 0)])
    assert m["V"][(0,)] == 1 and not m["exacto"][(0,)]               # provisional
    # Semilla fija: el mismo llamado da lo mismo.
    assert j.mc_minimax(j.ARBOL_TPM, 50, 3) == j.mc_minimax(j.ARBOL_TPM, 50, 3)
    r = j.mc_minimax(j.ARBOL_TPM, 300, 0)
    assert r["Q"] == [-1, 0, -1] and j.JUGADAS_RAIZ[r["jugada"]] == "centro"
    assert r["exacto"][()]
    with pytest.raises(ValueError):
        j.mc_minimax(j.ARBOL_TPM, None, caminos=[(1,)])


def test_homologacion_refutacion_descubierta_tarde():
    """Las cifras de §6.2: la secuencia impuesta (29 × +10 y luego −30) y las
    corridas reales de Monte Carlo plano, actualización minimax y UCT."""
    assert j.ARBOL_REFUTACION == ((10, 10, (-30,)), -10)
    op = j.operadores_ante_la_refutacion()
    assert op == dict(promedio_antes=10, promedio_despues=F(26, 3), jugada_promedio="A",
                      minimax_antes=10, minimax_despues=-30, jugada_minimax="B")
    assert round(float(op["promedio_despues"]), 2) == 8.67
    caminos = j.caminos_refutacion()
    assert len(caminos) == 31 and sum(c[0] == 0 for c in caminos) == 30
    # Corridas reales, mismas partidas uniformes (semilla 0, 60 iteraciones).
    r = j.corridas_refutacion()
    d = r["descubre"]
    assert d == 9
    assert r["minimax"][d - 2][0] == 10 and r["minimax"][d - 1][0] == -30
    assert r["jugada_minimax"][d - 2] == "A" and r["jugada_minimax"][d - 1:] == ["B"] * (60 - d + 1)
    assert r["plano"][d - 1][0] == -10 and r["plano"][-1] == [F(-150, 29), -10]
    assert r["jugada_plano"][-1] == "A"
    assert r["minimax"][-1] == [-30, -10]
    # UCT real: pagos entre 30, c = 1, semilla 0.
    assert (j.ESCALA_REFUTACION, j.C_REFUTACION, j.SEMILLA_REFUTACION,
            j.VUELTAS_REFUTACION) == (30, 1, 0, 60)
    u = j.uct_refutacion()
    assert u["descubre"] == 5 and u["cambia"] == 13
    qa = [q[0] for q in u["Q"]]
    assert qa[u["descubre"] - 2:u["descubre"]] == [F(1, 3), 0]   # un −1 más en el promedio
    assert qa[u["descubre"] - 1] != -1                            # promedio, no min
    assert all(qa[i + 1] <= qa[i] for i in range(u["descubre"] - 1, len(qa) - 1))
    assert u["Q"][-1] == (F(-2, 3), F(-1, 3)) and u["N"][-1] == (12, 48)
    assert u["mas_visitada"][-1] == "B"
    assert j.uct_refutacion() == u


def test_homologacion_sesgo_del_maximo():
    assert j.sesgo_del_maximo() == (F(1, 2), F(-1, 2))


def test_homologacion_hoeffding_y_c_de_ucb1():
    tabla = j.tabla_hoeffding_epsilon()
    assert [e for e, _ in tabla] == [0.1, 0.2, 0.4]
    assert [round(p, 2) for _, p in tabla[:2]] == [60.65, 13.53]
    assert round(tabla[2][1], 4) == 0.0335
    for n in (1, 10, 100):
        for e in (0.1, 0.3):
            assert _m.isclose(j.cota_hoeffding_cola(n, e), j.cota_hoeffding(n, e))
            assert _m.isclose(j.cota_hoeffding_cola(n, e / 2, ancho=1), j.cota_hoeffding(n, e))
        for delta in (0.2, 0.05, 0.01):
            assert _m.isclose(j.margen_hoeffding(delta, n), j.margen(delta, n))
            assert _m.isclose(j.cota_hoeffding_cola(n, j.margen_hoeffding(delta, n, 1), 1),
                              delta)
    assert _m.isclose(j.c_ucb1(), 2 * _m.sqrt(2)) and _m.isclose(j.c_ucb1(), j.C_TEORIA)
    assert _m.isclose(j.c_ucb1(ancho=1), _m.sqrt(2))
    assert _m.isclose(j.c_ucb1(ancho=200), 200 * _m.sqrt(2))
    # δ = N(s)^−4 en el margen da el bono de UCB1.
    for n_padre, n in ((100, 10), (1000, 30)):
        assert _m.isclose(j.margen_hoeffding(n_padre ** -4, n),
                          j.c_ucb1() * _m.sqrt(_m.log(n_padre) / n))


def test_homologacion_la_corrida_de_la_figura_de_mmmc_muestra_lo_provisional():
    """La figura jue-rx-mmmc usa j.ITERACIONES_MMMC_TPM partidas: tienen que
    quedar a la vez una jugada sin visitar (izq), nodos exactos (D, C2) y uno
    provisional (C), y entregar centro con la mayor Q̂ disponible."""
    m = j.mc_minimax(j.ARBOL_TPM, j.ITERACIONES_MMMC_TPM, j.SEMILLA_TPM)
    assert m["Q"] == [None, 0, -1] and j.JUGADAS_RAIZ[m["jugada"]] == "centro"
    assert m["exacto"][(2,)] and m["exacto"][(1, 1)]
    assert not m["exacto"][(1,)] and not m["exacto"][()]
    # con una partida menos o mas el retrato cambia: la cifra es deliberada
    assert j.mc_minimax(j.ARBOL_TPM, j.ITERACIONES_MMMC_TPM + 2, j.SEMILLA_TPM)["exacto"][(1,)]


# ------------------------------- homologacion (Ola 2): cifras de figuras ---

def test_homologacion_el_margen_crece_un_tercio_al_pedir_diez_veces_menos_fallo():
    """Panel B de jue-c3-hoeffding: dos δ, uno diez veces menor; el margen
    crece √(ln 200 / ln 20) ≈ 1.33 para todo N, y baja como 1/√N."""
    d1, d2 = j.DELTAS_HOEFFDING_HOMOLOGACION
    assert (d1, d2) == (0.05, 0.005) and _m.isclose(d1 / d2, 10)
    m = j.margenes_hoeffding((10, 40, 100, 200))
    for (n, e1), (n2, e2) in zip(m[d1], m[d2]):
        assert n == n2 and _m.isclose(e2 / e1, _m.sqrt(_m.log(200) / _m.log(20)))
        assert _m.isclose(e1, j.margen(d1, n))
    assert round(m[d1][2][1], 3) == 0.245 and round(m[d2][2][1], 3) == 0.326
    # cuatro veces mas muestras parten el margen a la mitad
    assert _m.isclose(m[d1][0][1] / m[d1][1][1], 2)


def test_homologacion_min_volteado_usa_la_misma_c_y_voltea_el_lado():
    v = j.min_volteado()
    f = v["filas"]
    assert v["N_padre"] == 50 and _m.isclose(v["c"], 2 * _m.sqrt(2))
    assert [f[k]["N"] for k in "pqr"] == [30, 16, 4]
    assert [f[k]["Q"] for k in "pqr"] == [F(-1, 5), F(1, 4), F(1, 2)]
    assert [round(f[k]["bono"], 2) for k in "pqr"] == [1.02, 1.40, 2.80]
    assert [round(f[k]["arriba"], 2) for k in "pqr"] == [0.82, 1.65, 3.30]
    assert [round(f[k]["abajo"], 2) for k in "pqr"] == [-1.22, -1.15, -2.30]
    assert (v["max"], v["min"]) == ("r", "r")
    # MIN elige el menor Q̂ − bono = el mayor puntaje de puntajes_ucb con −Q̂
    assert v["min"] == j.mejor(j.puntajes_ucb(j.EJEMPLO_MIN, mueve="MIN"))
    # con c = 1 el bono pesa menos y MIN se queda con la de menor Q̂: p
    assert j.min_volteado(c=1)["min"] == "p"


def test_homologacion_mcts_en_n_y_v_gorro():
    """jue-c3-mcts-pasos sin G/N: raíz N 4, V̂ 0 → N 5, V̂ +0.2."""
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    antes, despues = j.mcts_nv(vuelta["antes"]), j.mcts_nv(vuelta["despues"])
    assert antes["r"] == (4, 0) and despues["r"] == (5, F(1, 5))
    assert antes["a"] == (3, F(1, 3)) and despues["a"] == (4, F(1, 2))
    assert antes["a2"] == (1, -1) and despues["a2"] == (2, 0) and despues["nuevo"] == (1, 1)
    assert antes["b"] == despues["b"] == (1, -1) and antes["a1"] == (1, 1)
    assert j.mcts_nv({"x": (0, 0)})["x"] == (0, None)


def test_homologacion_variantes_del_ejercicio_final_de_corte():
    """jue-c3-ej-final-corte en el árbol de resultados: el empate con d = 1,
    la EVAL que cambia la jugada y el costo (no depende de la EVAL)."""
    assert j.EVAL_TPM_EMPATE == {**j.EVAL_TPM, "C": 60}
    assert j.decidir_con_corte_tpm(1, evaluar=j.EVAL_TPM_EMPATE) == ("izq", 60, 4)
    assert j.decidir_con_corte_tpm(1, orden=["D", "C", "I"],
                                   evaluar=j.EVAL_TPM_EMPATE) == ("centro", 60, 4)
    assert j.decidir_con_corte_tpm(1, orden=["D", "C", "I"]) == ("izq", 60, 4)
    assert j.EVAL_TPM_VARIANTE == {**j.EVAL_TPM, "I": 0}
    assert [j.decidir_con_corte_tpm(d, evaluar=j.EVAL_TPM_VARIANTE) for d in (1, 2, 3)] == [
        ("centro", 20, 4), ("centro", 10, 11), ("centro", 0, 15)]
    assert [j.decidir_con_corte_tpm(d) for d in (1, 2, 3)] == [
        ("izq", 60, 4), ("centro", 10, 11), ("centro", 0, 15)]
    assert [j.corte_tpm(d)[2] for d in (1, 2, 3)] == [
        {"izq": 60, "centro": 20, "der": 10}, {"izq": -100, "centro": 10, "der": -100},
        {"izq": -100, "centro": 0, "der": -100}]
    filas, total = j.iterativa_tpm()
    assert [(d, o, jg, n) for d, o, jg, _, n in filas] == [
        (1, ["izq", "centro", "der"], "izq", 4), (2, ["izq", "centro", "der"], "centro", 9),
        (3, ["centro", "izq", "der"], "centro", 12)] and total == 25


# ------------------------------------------ Ola 3 · integración: cifras nuevas ---
#
# Cifras que las páginas y las tareas homologadas citan y que ninguna prueba
# leía todavía de la prosa. Mismo método que #39: se leen por su ancla y se
# comparan con la función de juegos.py que las calcula.

UNIDAD_2 = UNIDAD / "2_mirar_todo_y_podar"


def test_ola3_monedas_esperanza_contra_un_rival_que_tira_un_volado():
    """monedas_esperanza: con (2, 1, 5, 3), E[tomar 2] = 3 para todo p y
    E[tomar 3] = 6p − 1; en los extremos coincide con un rival que siempre
    toma un lado, y la garantía adversarial de tomar el 3 es −1."""
    fila = (2, 1, 5, 3)
    for p in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        e = j.monedas_esperanza(fila, p)
        assert e == {"izq": 3, "der": 6 * p - 1}, p
    assert j.monedas_esperanza(fila, F(1, 2)) == {"izq": 3, "der": 2}
    assert j.monedas_esperanza(fila, F(3, 4)) == {"izq": 3, "der": F(7, 2)}
    # Contra el rival perfecto: tomar el 3 asegura 3 − W(2, 1, 5) = −1.
    assert fila[-1] - j.monedas_valor(fila[:-1]) == -1
    assert fila[0] - j.monedas_valor(fila[1:]) == j.monedas_valor(fila) == 3
    # Una sola moneda: el volado no tiene a dónde elegir.
    assert j.monedas_esperanza((4,), F(1, 3)) == {"izq": 4, "der": 4}


def test_ola3_la_tarea_de_la_clase_2_cita_la_esperanza_de_monedas():
    """El inciso 9 de la tarea 7.2: E[U | tomar el 2] = 3, E[U | tomar el 3]
    = 6p − 1, la tabla con p = 1/2 y 3/4 (y qué elige MAX), y que la jugada
    del 3 solo asegura −1 ante un rival perfecto."""
    texto = _limpio((UNIDAD_2 / "6_tarea.md").read_text(encoding="utf-8"))
    fila = tuple(int(x) for x in re.search(
        r"cuatro monedas de (\d+), (\d+), (\d+) y (\d+) pesos", texto).groups())
    assert fila == (2, 1, 5, 3)
    m2 = re.search(r"E\[U\\mid ?tomar el (\d)\]=(\d+)", texto)
    m3 = re.search(r"E\[U\\mid ?tomar el (\d)\]=5p-\(1-p\)=(\d)p-(\d)", texto)
    assert int(m2[1]) == fila[0] and int(m3[1]) == fila[-1]
    for p in (F(1, 5), F(2, 3)):
        e = j.monedas_esperanza(fila, p)
        assert e["izq"] == int(m2[2]) and e["der"] == int(m3[2]) * p - int(m3[3])
    filas = re.findall(r"\| \\tfrac(\d)(\d) \| \+?([\d.]+) \| \+?([\d.]+) \| El (\d) \|", texto)
    assert len(filas) == 2
    for num, den, izq, der, elige in filas:
        e = j.monedas_esperanza(fila, F(int(num), int(den)))
        assert (F(izq), F(der)) == (e["izq"], e["der"])
        assert int(elige) == (fila[0] if e["izq"] >= e["der"] else fila[-1])
    m = re.search(r"esa jugada solo asegura (-\d+) si el rival en realidad juega perfecto", texto)
    assert int(m[1]) == fila[-1] - j.monedas_valor(fila[:-1])


def test_ola3_w18_el_bloque_de_simulacion_de_la_tarea_de_la_clase_3():
    """La tarea 7.3, bloque 3 (W18): árbol ((1,1,1,−1),(0,(0,1))), semilla 0.
    Q = (−1, 0) y Q_azar = (1/2, 1/4); las 11 partidas de la corrida; plano y
    actualización minimax tras 3, 5, 10 y 11 (con «?» y «✓»; tras la 11,
    plano 3/5 contra 1/2 entrega A y minimax −1 entrega B); UCT con c = 1:
    vuelta 1 en a4, tras la 15 N = 4/11 y Q̂ = 1/2, 1/11, bonos 0.823/0.496
    y puntajes 1.323/0.587 (selecciona A, entrega B); vueltas 16–18 con
    Q̂(A) = 1/5, 0, −1/7; vuelta 1000 con A 15 visitas y −3/5, B 985, y B
    entregada desde la vuelta 3."""
    import math
    arbol, nombres = j.ARBOL_TAREA_SIMULAR, j.NOMBRES_TAREA_SIMULAR
    semilla = j.SEMILLA_TAREA_SIMULAR
    texto = (CLASE_3 / "6_tarea.md").read_text(encoding="utf-8")
    bloque = texto.split("## 3 · Tres Monte Carlo ante una respuesta certera")[1]
    limpio = _limpio(bloque)
    # El árbol que describe el enunciado.
    m = re.search(r"a1=a2=a3=\+(\d) y a4=(-\d)", limpio)
    assert arbol[0] == (int(m[1]),) * 3 + (int(m[2]),)
    m = re.search(r"El final b1=(\d), o el estado E, donde MAX elige entre e1=(\d) y e2=\+(\d)",
                  limpio)
    assert arbol[1] == (int(m[1]), (int(m[2]), int(m[3])))
    assert re.search(r"con semilla (\d+); en UCT, c=(\d)", limpio).groups() == (str(semilla), "1")
    # 1 · Valores exactos.
    resp = _limpio(_respuesta(texto, "jue-tarea-3-ej-simular"))
    q, qa = j.q_minimax_arbol(arbol), j.q_azar_arbol(arbol)
    assert (q, qa) == ([-1, 0], [F(1, 2), F(1, 4)])
    m = re.search(r"Q\(A\)=\\min\(1,1,1,-1\)=(-\d),\\qquad Q\(B\)=\\min\\bigl\(0,\\max\(0,1\)"
                  r"\\bigr\)=(\d)", resp)
    assert [int(m[1]), int(m[2])] == q
    m = re.search(r"Q_azar\(A\)=\\frac1\+1\+1-14=\\frac(\d)(\d),\\qquad Q_azar\(B\)=\\frac0\+"
                  r"\\tfrac122=\\frac(\d)(\d)", resp)
    assert [F(int(m[1]), int(m[2])), F(int(m[3]), int(m[4]))] == qa
    # 2 · Las mismas 11 partidas.
    ej = _limpio(_bloque(texto, "jue-tarea-3-ej-simular"))
    orden = re.search(r"termina, en este orden, en (.*?)\. Para", ej)[1]
    leidas = re.split(r", | y ", orden)
    mm = j.mc_minimax(arbol, len(leidas), semilla)
    plano = j.mc_plano_uniforme(arbol, len(leidas), semilla)
    assert leidas == [nombres[h["camino"]] for h in mm["historia"]]
    assert [h["camino"] for h in plano["historia"]] == [h["camino"] for h in mm["historia"]]
    tabla = _tablas(_respuesta(texto, "jue-tarea-3-ej-simular"))[0]
    assert [int(_c(f[0])) for f in tabla[1:]] == [3, 5, 10, 11]
    fmt = lambda x: "?" if x is None else str(x)  # noqa: E731
    for f in tabla[1:]:
        k = int(_c(f[0]))
        corrida = j.mc_minimax(arbol, k, semilla)
        ph, mh = plano["historia"][k - 1], corrida["historia"][-1]
        celdas = [_c(x) for x in f[1:]]
        assert celdas[:2] == [fmt(v) for v in ph["Q"]], k
        for celda, v, a in zip(celdas[2:], mh["Q"], (0, 1)):
            marca = " ✓" if corrida["exacto"].get((a,)) else ""
            assert celda == fmt(v) + marca, (k, a)
    ultima = j.JUGADAS_REFUTACION
    assert ultima[plano["jugada"]] == "A" and ultima[mm["jugada"]] == "B"
    m = re.search(r"el promedio de A solo baja a (\d)/(\d) y sigue entregando A", resp)
    assert F(int(m[1]), int(m[2])) == plano["Q"][0]
    # 3 · Seleccionar frente a entregar.
    vueltas = j.uct_por_vuelta_tpm(1, 1000, semilla, arbol)
    uct = j.uct_tpm(1, 1000, semilla, arbol)
    assert uct["caminos"][0][-1] == (0,) and uct["U"][0] == -1  # la vuelta 1 cae en a4
    m = re.search(r"Tras la vuelta (\d+), N\(s_raíz\)=(\d+)", ej)
    v15 = vueltas[int(m[1]) - 1]
    assert int(m[2]) == int(m[1]) == v15[()][0]
    filas = re.findall(r"\| ([AB]) \| (\d+) \| (\d+/\d+) \|", ej)
    assert [f[0] for f in filas] == ["A", "B"]
    for jugada, n, qh in filas:
        a = (0,) if jugada == "A" else (1,)
        assert (int(n), F(qh)) == (v15[a][0], F(v15[a][1], v15[a][0])), jugada
    ln = math.log(v15[()][0])
    assert re.search(r"\\ln 15≈(\d\.\d+)", _limpio(texto))[1] == f"{ln:.3f}"
    puntajes = re.findall(r"\| ([AB]) \| (\d\.\d+) \| (\d\.\d+) \| (\d\.\d+) \|", resp)
    calc = {}
    assert [p[0] for p in puntajes] == ["A", "B"]
    for jugada, qh, bono, p in puntajes:
        a = (0,) if jugada == "A" else (1,)
        n, s = v15[a]
        b = j.bono_ucb(v15[()][0], n, 1)
        calc[jugada] = s / n + b
        assert (qh, bono, p) == (f"{s / n:.{len(qh.split('.')[1])}f}", f"{b:.3f}",
                                 f"{s / n + b:.3f}"), jugada
    assert max(calc, key=calc.get) == "A" == ("A" if uct["caminos"][15][1] == (0,) else "B")
    assert re.search(r"Si se acaba el tiempo, se entrega ([AB])", resp)[1] == "B"
    assert v15[(1,)][0] > v15[(0,)][0]
    # 4 · Una respuesta no es un voto: vueltas 16, 17 y 18.
    tras = re.findall(r"Vuelta (\d+)\..*?\\widehat Q\(A\)=(?:\(\d-1\)/\d=|\d/\d=)?(-?\d+/\d+|0)",
                      resp.split("4. Una respuesta no es un voto.")[1])
    assert [int(k) for k, _ in tras] == [16, 17, 18]
    for k, frac in ((int(k), f) for k, f in tras):
        n, s = vueltas[k - 1][(0,)]
        assert F(frac) == F(s, n), k
        assert uct["caminos"][k - 1][-1] == (0, 3), k
    # 5 · A qué converge: vuelta 1000 y desde cuándo entrega B.
    m = re.search(r"En la vuelta (\d+), A lleva (\d+) visitas y \\widehat Q\(A\)=(-\d/\d); B, (\d+) "
                  r"visitas, y UCT entrega B desde la vuelta (\d+)", resp)
    final = vueltas[int(m[1]) - 1]
    assert (int(m[2]), F(m[3]), int(m[4])) == (final[(0,)][0], F(final[(0,)][1], final[(0,)][0]),
                                               final[(1,)][0])
    mas = uct["mas_simulada"]
    desde = int(m[5])
    assert all(x == j.JUGADAS_RAIZ[1] for x in mas[desde - 1:]) and mas[desde - 2] != mas[desde - 1]


def test_ola3_reparto_de_monte_carlo_plano_en_simular_partidas():
    """@jue-c3-cmp-reparto-mc (353/106/541, 269/53/678, 39/1/960 en 1000
    corridas) y los empates (233, 157 y 15), de reparto_mc_plano_tpm; y el
    «960 de 1000 corridas con 50» del resumen."""
    texto = _pagina(P5)
    filas = _tabla(texto, "jue-c3-cmp-reparto-mc")
    jugadas = [_c(x) for x in filas[0][1:]]
    assert jugadas == list(j.JUGADAS_RAIZ)
    empates = []
    for f in filas[1:]:
        k = int(_c(f[0]))
        reparto, empate = j.reparto_mc_plano_tpm(k)
        assert [int(_c(x)) for x in f[1:]] == [reparto[a] for a in jugadas], k
        empates.append(empate)
    assert [int(_c(f[0])) for f in filas[1:]] == list(j.SIMS_MC_TPM)
    m = re.search(r"el empate decidió (\d+), (\d+) y (\d+) corridas", _limpio(texto))
    assert [int(x) for x in m.groups()] == empates
    m = re.search(r"(\d+) de (\d+) corridas con (\d+) simulaciones por jugada", _llevarse(texto))
    reparto, _ = j.reparto_mc_plano_tpm(int(m[3]))
    assert (int(m[1]), int(m[2])) == (reparto["der"], j.SEMILLAS_MC_TPM)


def test_ola3_la_refutacion_en_simular_partidas():
    """@jue-c3-tab-refutacion y @jue-c3-tab-propagacion (promedio 10 → 26/3 ≈
    8.67, minimax 10 → −30, raíz −10: B) con operadores_ante_la_refutacion;
    la corrida real: r aparece en la novena, el promedio empata en −10, y
    tras 60 simulaciones A tiene 29 y −150/29 ≈ −5.17 (corridas_refutacion)."""
    texto = _pagina(P5)
    op = j.operadores_ante_la_refutacion()
    filas = _tabla(texto, "jue-c3-tab-refutacion")
    ultima = filas[-1]
    assert int(_c(ultima[0])) == j.BUENAS_REFUTACION + 2
    assert _c(ultima[2]) == _d(op["promedio_despues"]) and _n(ultima[3]) == op["minimax_despues"]
    assert _n(filas[2][2]) == op["promedio_antes"] == op["minimax_antes"] == _n(filas[2][3])
    m = re.search(r"\((\d+)·(\d+)-(\d+)\)/(\d+)=(\d+)/(\d+)≈(\d+\.\d+)", _limpio(texto))
    assert int(m[1]) == j.BUENAS_REFUTACION and F(int(m[5]), int(m[6])) == op["promedio_despues"]
    assert m[7] == _d(op["promedio_despues"])
    prop = {_c(f[0]): (_c(f[1]), _c(f[2])) for f in _tabla(texto, "jue-c3-tab-propagacion")[1:]}
    assert prop["Tras A (MIN)"] == (str(op["minimax_antes"]), str(op["minimax_despues"]))
    assert prop["Raíz (MAX)"][1] == f"{j.valor_minimax_arbol(j.ARBOL_REFUTACION)}: " \
        f"{op['jugada_minimax']}"
    c = j.corridas_refutacion()
    limpio = _limpio(texto)
    m = re.search(r"Con semilla (\d+) y (\d+) simulaciones, la primera visita a r ocurre en la "
                  r"(\w+)\.", limpio)
    assert (int(m[1]), int(m[2])) == (j.SEMILLA_REFUTACION, j.VUELTAS_REFUTACION)
    assert {"novena": 9}[m[3]] == c["descubre"]
    k = c["descubre"] - 1
    assert c["minimax"][k][0] == -30 and c["jugada_minimax"][k:] == ["B"] * (len(c["minimax"]) - k)
    assert c["plano"][k][0] == c["plano"][k][1] == -10 and c["jugada_plano"][k] == "A"
    m = re.search(r"Tras (\d+) simulaciones, A recibió (\d+) y su media es (-\d+)/(\d+)≈(-\d+\.\d+)",
                  limpio)
    p = j.mc_plano_uniforme(j.ARBOL_REFUTACION, int(m[1]), j.SEMILLA_REFUTACION)
    assert int(m[2]) == p["N"][0] == int(m[4]) and F(-int(m[3][1:]), int(m[4])) == p["Q"][0]
    assert m[5] == _d(p["Q"][0])


def test_ola3_uct_ante_la_refutacion_en_mcts_con_uct():
    """«MCTS con UCT»: la corrida real de UCT en el árbol de la refutación
    (pagos entre 30, c = 1, semilla 0, 60 vueltas): el −30 aparece en la
    vuelta 5; Q̂(A) < Q̂(B) desde la 13; B la más visitada desde la 15; en
    la 60, B 48 y A 12 visitas, Q̂(A) = −20 y Q̂(B) = −10 (uct_refutacion)."""
    texto = _limpio(_pagina(P5b))
    u = j.uct_refutacion()
    m = re.search(r"pagos entre (\d+), para que queden en \[-1,1\], y usa c=(\d), semilla (\d+) y "
                  r"(\d+) vueltas", texto)
    assert tuple(int(x) for x in m.groups()) == (j.ESCALA_REFUTACION, j.C_REFUTACION,
                                                 j.SEMILLA_REFUTACION, j.VUELTAS_REFUTACION)
    assert int(re.search(r"Vuelta (\d+): aparece el -30", texto)[1]) == u["descubre"]
    assert int(re.search(r"Vuelta (\d+): \\widehat Q\(A\) queda debajo", texto)[1]) == u["cambia"]
    desde = next(i + 1 for i in range(len(u["mas_visitada"]))
                 if all(x == "B" for x in u["mas_visitada"][i:]))
    assert int(re.search(r"Vuelta (\d+): B pasa a ser la más visitada", texto)[1]) == desde
    m = re.search(r"Vuelta (\d+): B lleva (\d+) visitas y A (\d+); \\widehat Q\(A\)=(-\d+) y "
                  r"\\widehat Q\(B\)=(-\d+)", texto)
    assert int(m[1]) == len(u["N"])
    (na, nb), (qa, qb) = u["N"][-1], u["Q"][-1]
    assert (int(m[2]), int(m[3])) == (nb, na)
    assert (int(m[4]), int(m[5])) == (qa * j.ESCALA_REFUTACION, qb * j.ESCALA_REFUTACION)


def test_ola3_uct_en_el_arbol_de_resultados():
    """«MCTS con UCT» y el bono: la corrida de UCT con c = 1 y semilla 0 en el
    árbol de resultados. La más visitada por tramos (izq 1–3, centro 4–7, der
    8–17, centro desde la 18, con el 7 a 7 de la 18); la vuelta 12 (visitas
    1, 4, 7; 10 de 15 nodos; Q̂(der) = −1/7) en la prosa y en
    @jue-c3-tabla-uct-12 (bonos y puntajes); la 40 (centro 26 visitas y
    Q̂ = 0, der 9, V̂(R) = −3/20); la 100 (Q̂(centro) = 1/83)."""
    mcts, bono = _pagina(P5b), _pagina(P6)
    limpio = _limpio(mcts)
    u = j.uct_tpm(1, 100, j.SEMILLA_TPM)
    pv = j.uct_por_vuelta_tpm(1, 100, j.SEMILLA_TPM)
    mas = u["mas_simulada"]
    tramos = re.findall(r"- (izq|centro|der), (?:en las vueltas|de la|desde la) (\d+)", limpio)
    assert [t[0] for t in tramos] == ["izq", "centro", "der", "centro"]
    inicios = [int(t[1]) for t in tramos]
    for (jugada, _), ini, fin in zip(tramos, inicios, inicios[1:] + [len(mas) + 1]):
        assert set(mas[ini - 1:fin - 1]) == {jugada}, jugada
    raiz = [(i,) for i in range(3)]
    v18 = pv[17]
    assert v18[(1,)][0] == v18[(2,)][0] == 7 and mas[17] == "centro"
    # Vuelta 12.
    v12 = pv[11]
    m = re.search(r"Vuelta (\d+)\. Las visitas son (\d+), (\d+) y (\d+); el árbol guarda (\d+) de "
                  r"los (\d+) nodos\..*?\\widehat Q\(R,der\)=(-\d/\d)", limpio)
    assert int(m[1]) == 12
    assert [int(m[2]), int(m[3]), int(m[4])] == [v12[a][0] for a in raiz]
    assert (int(m[5]), int(m[6])) == (len(v12), j.contar_nodos(j.ARBOL_TPM))
    assert F(m[7]) == F(v12[(2,)][1], v12[(2,)][0])
    filas = _tabla(bono, "jue-c3-tabla-uct-12")
    for f, a in zip(filas[1:], raiz):
        n, s = v12[a]
        b = j.bono_ucb(12, n, 1)
        assert (_c(f[0]), int(_c(f[1]))) == (j.JUGADAS_RAIZ[a[0]], n)
        assert _c(f[2]) == (str(s // n) if s % n == 0 else f"{s / n:.3f}"), a
        assert (_c(f[3]), _c(f[4])) == (f"{b:.3f}", f"{s / n + b:.3f}")
    assert re.search(r"UCT con c=(\d) y semilla (\d+); en la raíz, N\(s\)=(\d+)",
                     _limpio(bono)).groups() == ("1", str(j.SEMILLA_TPM), "12")
    # Vuelta 40 y vuelta 100.
    v40, v100 = pv[39], pv[99]
    m = re.search(r"Tras (\d+) vueltas, \\widehat V\(R\)=(-\d+/\d+), aunque "
                  r"\\widehat Q\(R,centro\)=(\d)", limpio)
    assert int(m[1]) == 40 and F(m[2]) == F(v40[()][1], v40[()][0])
    assert F(m[3]) == F(v40[(1,)][1], v40[(1,)][0])
    m = re.search(r"En la vuelta (\d+), der lleva (\d+) visitas contra (\d+) de centro", limpio)
    assert int(m[1]) == 40 and (int(m[2]), int(m[3])) == (v40[(2,)][0], v40[(1,)][0])
    m = re.search(r"en la vuelta (\d+), \\widehat Q\(R,centro\)=(\d+/\d+)", limpio)
    assert int(m[1]) == 100 and F(m[2]) == F(v100[(1,)][1], v100[(1,)][0])


def test_ola3_la_c_en_el_arbol_de_resultados():
    """@jue-c3-tabla-c-semillas: con 500 semillas de 200 vueltas, la vuelta
    desde la que centro queda como la más visitada (mediana y percentil 90)
    con c = 1 y c = 2√2, de reparto_uct_tpm; ninguna semilla se queda sin
    centro."""
    texto = _pagina(P6)
    m = re.search(r"Con (\d+) semillas de (\d+) vueltas, las dos c terminan con centro",
                  _seccion(texto, 5))
    assert (int(m[1]), int(m[2])) == (j.SEMILLAS_UCT_TPM, j.VUELTAS_UCT_TPM)
    filas = _tabla(texto, "jue-c3-tabla-c-semillas")
    for f in filas[1:]:
        c = _c_de(_c(f[0]))
        r = j.reparto_uct_tpm(j.C_TEORIA if c is None else float(c))
        assert int(_c(f[1])) == r["mediana"], f
        assert re.fullmatch(r"(\d+) o antes", _c(f[2]))[1] == str(r["p90"]), f
        assert r["nunca"] == 0
