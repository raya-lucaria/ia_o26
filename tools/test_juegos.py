"""Los numeros que citan las paginas de course/7_juegos/, recalculados.

Si una pagina cita un numero, aqui hay una asercion que lo recalcula con
tools/juegos.py. Cambiar una regla del juego sin actualizar la prosa hace
fallar esta suite.
"""
from fractions import Fraction as F

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
    """±(10−k) solo aparece en el aviso que explica por qué no se usa."""
    for pagina in UNIDAD.rglob("*.md"):
        texto = pagina.read_text(encoding="utf-8")
        apariciones = re.findall(r"10\s*-\s*k", texto)
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


def test_clase_2_alfa_beta_en_arboles_genericos():
    """Los arboles A, B y C de «Alfa-beta a mano» y «Alfa-beta como algoritmo»."""
    inf = float("inf")
    # Arbol A: raiz MAX, hijos MIN (3, 5) y (2, ?). Se generan 6 de 7.
    a = j.alfa_beta_arbol(j.ARBOL_A, es_max=True)
    assert (a["valor"], a["generados"], j.contar_nodos(j.ARBOL_A)) == (3, 6, 7)
    assert a["podados"] == [(1, 1)]  # la hoja «?»
    paso = {c: (tipo, al, be, v, corte) for c, tipo, al, be, v, corte in a["traza"]}
    assert paso[(0,)] == ("MIN", -inf, inf, 3, None)
    # R llega con [3, +inf], su hoja 2 cumple 2 <= 3 y devuelve 2, una cota:
    # su valor exacto es 1.
    assert paso[(1,)] == ("MIN", 3, inf, 2, "alfa")
    assert j.minimax_arbol(j.ARBOL_A[1], es_max=False) == 1
    # Al reves, R primero: 7 de 7 y ningun corte.
    a_inv = j.alfa_beta_arbol(j.ARBOL_A, es_max=True, invertir=True)
    assert (a_inv["valor"], a_inv["generados"], a_inv["podados"]) == (3, 7, [])
    # Con un 3 en lugar del 2 tambien corta: el igual cuenta.
    a3 = j.alfa_beta_arbol(((3, 5), (3, 1)), es_max=True)
    assert (a3["valor"], a3["generados"], a3["podados"]) == (3, 6, [(1, 1)])
    # Arbol B: raiz MIN, hijos MAX (8, 6) y (9, ?). 6 de 7, corte beta.
    b = j.alfa_beta_arbol(j.ARBOL_B, es_max=False)
    assert (b["valor"], b["generados"], b["podados"]) == (8, 6, [(1, 1)])
    paso = {c: (tipo, al, be, v, corte) for c, tipo, al, be, v, corte in b["traza"]}
    assert paso[(0,)] == ("MAX", -inf, inf, 8, None)
    assert paso[(1,)] == ("MAX", -inf, 8, 9, "beta")
    # Arbol C: 15 nodos, vale 5; 11 en el orden dado, 15 al reves.
    c = j.alfa_beta_arbol(j.ARBOL_C, es_max=True)
    assert (c["valor"], c["generados"], j.contar_nodos(j.ARBOL_C)) == (5, 11, 15)
    assert j.minimax_arbol(j.ARBOL_C) == 5
    # Se poda la hoja 9 (corte beta en MAX(6, 9), que llega con [-inf, 5]) y
    # el subarbol (7, 1), tres nodos (corte alfa en el MIN derecho).
    assert c["podados"] == [(0, 1, 1), (1, 1)]
    paso = {cam: (tipo, al, be, v, corte) for cam, tipo, al, be, v, corte in c["traza"]}
    assert paso[(0, 1)] == ("MAX", -inf, 5, 6, "beta")
    assert paso[(1,)] == ("MIN", 5, inf, 4, "alfa")
    c_inv = j.alfa_beta_arbol(j.ARBOL_C, es_max=True, invertir=True)
    assert (c_inv["valor"], c_inv["generados"], c_inv["podados"]) == (5, 15, [])
    # Sin el igual, el juego completo pierde casi toda la poda: 228 y 171.
    assert j.alfa_beta(j.inicio(), "B", estricto=True)[:2] == (-1, 228)
    assert j.alfa_beta(j.inicio(), "B", invertir=True, estricto=True)[:2] == (-1, 171)
