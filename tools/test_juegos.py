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
P1, P2, P3, P4, P5 = ("1_cortar_y_evaluar.md", "2_minimax_con_corte.md",
                      "3_mas_alla_del_horizonte.md", "4_jugar_contra_el_reloj.md",
                      "5_simular_en_vez_de_evaluar.md")
_JUGADA = r"[a-d][1-4][-x][a-d][1-4]"


def _pagina(nombre):
    return (CLASE_3 / nombre).read_text(encoding="utf-8")


def _limpio(s):
    """El texto de la pagina sin lo que no es la cifra: «−» pasa a «-», fuera
    espacios estrechos (U+202F), word joiners (U+2060), negritas, «$» y las
    llaves de ${…}$; \\text{a1}\\textbf{-}\\text{a2} queda «a1-a2»."""
    s = str(s).replace("\u2212", "-").replace("\u2060", "").replace("\u202f", "")
    s = s.replace("\u00a0", " ").replace("\\,", "")
    s = re.sub(r"\\(?:text|textbf|mathrm)\{([^{}]*)\}", r"\1", s)
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
    assert int(re.search(r"Su árbol tiene (\d+) nodos", limpio).group(1)) == nodos_4


def test_prosa_clase_3_la_cota_de_eval_que_citan_las_paginas():
    """#39 · El «36» (|EVAL| maximo fuera de los finales) en p1, p2 y p4."""
    cota = max(abs(j.evaluar_peones(t, 4)) for t, _ in _no_finales_4x4())
    p1 = _pagina(P1)
    assert [int(x) for x in re.findall(r"nunca pasa de (\d+)", _limpio(p1))] == [cota, cota]
    assert int(re.search(r"EVAL=(\d+)", _limpio(_respuesta(p1, "jue-c3-ej-escala")))[1]) == cota
    p2 = _limpio(_bloque(_pagina(P2), "jue-c3-que-afirma"))
    assert int(re.search(r"\|EVAL\|≤(\d+)", p2)[1]) == cota
    assert [int(x) for x in re.findall(r"\|EVAL\|≤(\d+)", _limpio(_pagina(P4)))] == [cota]


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


def test_prosa_clase_3_p2_evaluacion_y_traza_de_t_con_d_2():
    """#39 · @jue-c3-t-eval (EVAL y V de cada nodo interno), los dos tramos de
    la traza de DECIDIR-CON-CORTE(R, 2) y los «n de 14 nodos» de las figuras."""
    texto = _pagina(P2)
    devuelve = {f["hijo"]: f["w"] for f in j.traza_decidir(j.ARBOL_T)["filas"]
                if f["w"] is not None}
    assert {_c(f[0]): (_n(f[1]), _n(f[2])) for f in _tabla(texto, "jue-c3-t-eval")[1:]} == {
        k: (j.EVAL_T[k], devuelve[k]) for k in j.EVAL_T}
    leidas = _filas(_tabla(texto, "jue-c3-t-traza-d2")[1:] +
                    _tabla(texto, "jue-c3-t-traza-d2-tramo-2")[1:])
    assert leidas == _esperado(j.filas_corte_t(2))
    total = j.contar_nodos(j.ARBOL_T)
    filas = j.traza_decidir(j.ARBOL_T, profundidad=2, evaluar=j.EVAL_T)["filas"]
    tramo_1 = len(_tabla(texto, "jue-c3-t-traza-d2")) - 1
    for figura, generados in [("jue-c3-t-fig-d1", j.decidir_con_corte_t(1)[2]),
                              ("jue-c3-t-fig-d2-tramo-1", filas[tramo_1 - 1]["generados"]),
                              ("jue-c3-t-fig-d2-tramo-2", j.decidir_con_corte_t(2)[2])]:
        m = re.search(r"Se han generado (\d+) de (\d+) nodos", _alt(texto, figura))
        assert (int(m[1]), int(m[2])) == (generados, total), figura


def test_prosa_clase_3_p2_t_con_cada_profundidad():
    """#39 · @jue-c3-t-por-profundidad: I · C · D, la jugada y los nodos
    (4, 10, 14) con d = 1, 2, 3; y los 10 nodos de la cota."""
    texto = _pagina(P2)
    leido = [tuple(_c(x) for x in f) for f in _tabla(texto, "jue-c3-t-por-profundidad")[1:]]
    esperado = []
    for d in (1, 2, 3):
        w = {f["hijo"]: f["w"] for f in j.traza_decidir(
            j.ARBOL_T, profundidad=d, evaluar=j.EVAL_T)["filas"] if f["evento"] == "raiz"}
        jugada, _, nodos = j.decidir_con_corte_t(d)
        esperado.append((str(d), f"{w['I']} · {w['C']} · {w['D']}", jugada, str(nodos)))
    assert leido == esperado
    resp = _limpio(_respuesta(texto, "jue-c3-ej-cota"))
    assert int(re.search(r"suman los (\d+) nodos", resp)[1]) == j.decidir_con_corte_t(2)[2]
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[1])
    assert [int(x) for x in re.search(r"genera (\d+), (\d+) y (\d+) nodos", llevarse).groups()] \
        == [j.decidir_con_corte_t(d)[2] for d in (1, 2, 3)]


def test_prosa_clase_3_p2_la_traza_con_huecos_y_su_respuesta():
    """#39 · El ejercicio «Completa la traza con der primero»: el orden sale
    del enunciado; las celdas sin «?» y la tabla de la respuesta, de
    filas_corte_t con ese orden."""
    texto = _pagina(P2)
    ej = _bloque(texto, "jue-c3-ej-traza-d2")
    orden = _orden_de(re.search(r"otro orden: (\w+), (\w+), (\w+)", _limpio(ej)).groups())
    esperado = _esperado(j.filas_corte_t(2, orden=orden))
    _con_huecos(_filas(_tablas(ej)[0][1:]), esperado)
    resp = _respuesta(texto, "jue-c3-ej-traza-d2")
    assert _filas(_tablas(resp)[0][1:]) == esperado
    jugada, valor, _ = j.decidir_con_corte_t(2, orden=orden)
    assert re.search(r"Devuelve (\w+), con (\d+)", _limpio(resp)).groups() == (jugada, str(valor))


def test_prosa_clase_3_p2_ejercicio_final_empate_y_otra_eval():
    """#39 · El ejercicio final de «Minimax con corte»: el empate
    EVAL(C1) = 3 (izq con el orden de la pagina, centro con R al reves, y la
    traza de este), la variante EVAL(C2) = 1 con d = 1, 2, 3 y los nodos
    4, 10, 14."""
    texto = _pagina(P2)
    ej = _limpio(_bloque(texto, "jue-c3-ej-final-corte"))
    assert [int(x) for x in re.search(r"EVAL\(C1\)=(\d+) en vez de (\d+)", ej).groups()] == [
        j.EVAL_T_EMPATE["C1"], j.EVAL_T["C1"]]
    pagina = _orden_de(re.search(r"el orden de la página, (\w+), (\w+), (\w+)", ej).groups())
    orden = _orden_de(re.search(r"al\s+revés, (\w+), (\w+), (\w+)", ej).groups())
    assert pagina == ["I", "C", "D"] and orden == pagina[::-1]
    assert [int(x) for x in re.search(r"EVAL\(C2\)=(\d+) en vez de (\d+)", ej).groups()] == [
        j.EVAL_T_VARIANTE["C2"], j.EVAL_T["C2"]]
    resp = _respuesta(texto, "jue-c3-ej-final-corte")
    assert _filas(_tablas(resp)[0][1:]) == _esperado(
        j.filas_corte_t(2, orden=orden, evaluar=j.EVAL_T_EMPATE))
    limpio = _limpio(resp)
    empate, variante_txt = limpio.split("2. La variante.")
    c = j.EVAL_T_EMPATE
    assert re.search(r"C vale \\min\((\d+),(\d+)\)=(\d+), igual que I", empate).groups() == (
        str(c["C1"]), str(c["C2"]), str(min(c["C1"], c["C2"])))
    jugada, valor, _ = j.decidir_con_corte_t(2, evaluar=c)
    assert re.search(r"juega (\w+), con (\d+)", empate).groups() == (jugada, str(valor))
    jugada, valor, _ = j.decidir_con_corte_t(2, orden=orden, evaluar=c)
    assert re.search(r"Devuelve\s+(\w+), con (\d+)", empate).groups() == (jugada, str(valor))
    assert jugada != j.decidir_con_corte_t(2, evaluar=c)[0]
    variante = [j.decidir_con_corte_t(d, evaluar=j.EVAL_T_VARIANTE) for d in (1, 2, 3)]
    assert [(a, int(v)) for a, v in re.findall(r"juega (izq|centro|der), con (\d+)", variante_txt)] \
        == [v[:2] for v in variante]
    nodos = [int(x) for x in re.search(r"(\d+), (\d+) y (\d+) nodos en los dos casos",
                                       variante_txt).groups()]
    assert nodos == [v[2] for v in variante] == [
        j.decidir_con_corte_t(d, orden=orden, evaluar=c)[2] for d in (1, 2, 3)]


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


# ---- p4 · jugar contra el reloj

def test_prosa_clase_3_p4_el_reloj_en_la_posicion():
    """#39 · @jue-c3-reloj-por-d, los 4, 12 y 33 nodos de la figura y del
    ejercicio de costo, y su suma (49) y repeticion (16)."""
    texto = _pagina(P4)
    filas = _tabla(texto, "jue-c3-reloj-por-d")
    jugadas = [_c(x) for x in filas[0][1:]]
    assert {int(_c(f[0])): dict(zip(jugadas, [_n(x) for x in f[1:]])) for f in filas[1:]} == {
        d: _corte_en_la_posicion(d) for d in (1, 2, 3)}
    nodos = [j.nodos_con_corte(j.POSICION_C3, "B", d, 4) for d in (1, 2, 3)]
    alt = _alt(texto, "jue-c3-fig-profundizacion")
    assert [int(x) for x in re.findall(r"genera (\d+)", alt)] == nodos
    ej = _limpio(_bloque(texto, "jue-c3-ej-costo"))
    assert [int(x) for x in re.search(r"(\d+), (\d+) y (\d+) nodos", ej).groups()] == nodos
    resp = _limpio(_respuesta(texto, "jue-c3-ej-costo"))
    assert [int(x) for x in re.search(r"(\d+)\+(\d+)\+(\d+)= (\d+)", resp).groups()] == \
        nodos + [sum(nodos)]
    assert [int(x) for x in re.search(r"(?<![\d+])(\d+)\+(\d+)= (\d+)", resp).groups()] == \
        nodos[:2] + [sum(nodos[:2])]


def test_prosa_clase_3_p4_profundizar_sin_poda_en_t():
    """#39 · @jue-c3-t-sin-poda (I · C · D, lista, nodos), el 4 + 10 + 14 = 28
    y el ejercicio de orden: el orden no cambia los nodos."""
    texto = _pagina(P4)
    corridas = j.iterativa_sin_poda_t()
    esperado = []
    for d, _, jugada, _, nodos in corridas:
        w = {f["hijo"]: f["w"] for f in j.traza_decidir(
            j.ARBOL_T, profundidad=d, evaluar=j.EVAL_T)["filas"] if f["evento"] == "raiz"}
        esperado.append((str(d), f"{w['I']} · {w['C']} · {w['D']}", jugada, str(nodos)))
    assert _filas(_tabla(texto, "jue-c3-t-sin-poda")[1:]) == esperado
    m = re.search(r"generan (\d+)\+(\d+)\+(\d+)=(\d+) nodos", _limpio(texto))
    assert [int(x) for x in m.groups()] == [c[4] for c in corridas] + [
        sum(c[4] for c in corridas)]
    resp = _limpio(_respuesta(texto, "jue-c3-ej-orden-sin-poda"))
    assert [int(x) for x in re.search(r"(\d+), (\d+) y (\d+)\.", resp).groups()] == [
        c[4] for c in j.iterativa_sin_poda_t(anterior_primero=True)]


def _filas_reloj_d3():
    """La busqueda con d = 3, centro primero, en las dos tablas de la pagina:
    (#, línea · pila, (α,β)) y (#, v, w, compara)."""
    t = j.traza_decidir(j.ARBOL_T, poda=True, orden={"R": ["C", "I", "D"]}, profundidad=3,
                        evaluar=j.EVAL_T, lineas=j.LINEAS_RELOJ)
    donde, numeros, alfa_r = [], [], -INF
    for f in t["filas"]:
        n = str(f["n"])
        donde.append((n, f"{f['linea']} · {'›'.join(f['pila'])}",
                      f"({j.fmt_t(f['alfa'])},{j.fmt_t(f['beta'])})"))
        v = j.fmt_t(f["mejor_valor"] if f["nodo"] == "R" else f["v"])
        w = "" if f["w"] is None else (j.fmt_t(f["w"]) if f["hijo"] == str(f["w"])
                                       else f"{j.fmt_t(f['w'])} ({f['hijo']})")
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
    """#39 · Los dos tramos de la busqueda con d = 3: las tablas del tramo 1,
    el tramo 2 con huecos y su respuesta, y los 11 nodos generados."""
    texto = _pagina(P4)
    t, donde, numeros = _filas_reloj_d3()
    sin_espacios = lambda filas: [tuple(c.replace(" ", "") for c in f) for f in filas]  # noqa: E731
    tramo_1 = len(_tabla(texto, "jue-c3-t-traza-d3-donde")) - 1
    assert sin_espacios(_filas(_tabla(texto, "jue-c3-t-traza-d3-donde")[1:])) == \
        sin_espacios(donde[:tramo_1])
    assert sin_espacios(_filas(_tabla(texto, "jue-c3-t-traza-d3-numeros")[1:])) == \
        sin_espacios(numeros[:tramo_1])
    ej = _tablas(_bloque(texto, "jue-c3-ej-traza-d3"))
    _con_huecos(sin_espacios(_filas(ej[0][1:])), sin_espacios(donde[tramo_1:]))
    _con_huecos(sin_espacios(_filas(ej[1][1:])), sin_espacios(numeros[tramo_1:]))
    resp = _respuesta(texto, "jue-c3-ej-traza-d3")
    tablas = _tablas(resp)
    assert sin_espacios(_filas(tablas[0][1:])) == sin_espacios(donde[tramo_1:])
    assert sin_espacios(_filas(tablas[1][1:])) == sin_espacios(numeros[tramo_1:])
    m = re.search(r"Se generan (\d+) nodos: ([^.]*)\.", _limpio(resp))
    assert int(m[1]) == t["generados"]
    assert re.split(r", | y ", m[2]) == t["orden_generados"]


def test_prosa_clase_3_p4_iterativa_en_t_y_nodos_generados():
    """#39 · @jue-c3-t-iterativa, el «4, 10 y 11, que suman 25 / 28» y las dos
    tablas de nodos generados (T: 4, 10, 14 / 4, 9, 12 / 4, 10, 11; posicion:
    4, 12, 33 / 4, 12, 22 / 4, 10, 9), con sus totales."""
    texto = _pagina(P4)
    esperado = []
    for i, (d, _, t) in enumerate(j.profundizacion_iterativa_t()):
        hijos = []
        for k, f in enumerate(f for f in t["filas"] if f["evento"] == "raiz"):
            cota = "≤" if f["estado"][f["hijo"]]["cota"] else ""
            nombre = f"**{f['hijo']}**" if (i and not k) else f["hijo"]
            hijos.append(f"{nombre} {cota}{j.fmt_t(f['w'])}")
        esperado.append((str(d), " · ".join(hijos), t["jugada"]))
    filas = _tabla(texto, "jue-c3-t-iterativa")[1:]
    assert [(f[0], f[1], f[2]) for f in filas] == esperado
    tabla = j.tabla_nodos_generados()
    m = re.search(r"Nodos generados: (\d+), (\d+) y (\d+), que suman (\d+)\. Sin poda eran "
                  r"(\d+) \((\d+), (\d+)\s+y (\d+)\)", _limpio(texto))
    t_it, t_sp = tabla[("T", "iterativa")], tabla[("T", "sin poda")]
    assert [int(x) for x in m.groups()] == t_it + [sum(t_it), sum(t_sp)] + t_sp
    for ident, arbol in [("jue-c3-nodos-generados", "T"),
                         ("jue-c3-nodos-generados-posicion", "4x4")]:
        filas = _tabla(texto, ident)
        columnas = {"sin poda": "sin poda", "α-β fijo": "alfa-beta", "iterativa": "iterativa"}
        claves = [columnas[_c(x)] for x in filas[0][1:]]
        leido = {k: [_n(f[i + 1]) for f in filas[1:]] for i, k in enumerate(claves)}
        assert leido == {k: tabla[(arbol, k)] + [sum(tabla[(arbol, k)])] for k in claves}, ident
    llevarse = _limpio(texto.split("## Lo que hay que llevarse")[1])
    m = re.search(r"En T: (\d+) nodos sin poda, (\d+) con la iterativa \((\d+), (\d+) y (\d+)\)",
                  llevarse)
    assert [int(x) for x in m.groups()] == [sum(t_sp), sum(t_it)] + t_it
    m = re.search(r"posición de la clase: (\d+), (\d+) y (\d+)\.", llevarse)
    assert [int(x) for x in m.groups()] == [sum(tabla[("4x4", k)]) for k in
                                            ("sin poda", "alfa-beta", "iterativa")]


def test_prosa_clase_3_p4_valor_piso_y_techo():
    """#39 · @jue-c3-transposicion-iterativa y el ejercicio con el orden fijo:
    la ventana, el v y la clase de cada nodo, de clases_transposicion."""
    texto = _pagina(P4)
    nombre = {"exacto": "valor", "piso": "piso", "techo": "techo"}
    ventana = lambda a, b: f"({j.fmt_t(a)},{j.fmt_t(b)})"  # noqa: E731
    *_, (_, _, t) = j.profundizacion_iterativa_t()
    esperado = [(n, _c(ventana(a, b)), _c(j.fmt_t(v)), nombre[k])
                for n, (a, b, v, k) in j.clases_transposicion(t).items()]
    leido = [tuple(_c(x).replace(" ", "") for x in f)
             for f in _tabla(texto, "jue-c3-transposicion-iterativa")[1:]]
    assert leido == esperado
    fijo = j.clases_transposicion(j.traza_decidir(j.ARBOL_T, poda=True, profundidad=3,
                                                  evaluar=j.EVAL_T))
    ej = _limpio(_bloque(texto, "jue-c3-ej-clase"))
    vistos = re.findall(r"(I|C2|D) llega con \(([^)]*)\) y devuelve (\d+)", ej)
    assert len(vistos) == 3
    for n, v_ventana, v in vistos:
        a, b, valor, _ = fijo[n]
        assert (f"({v_ventana})".replace(" ", ""), int(v)) == (_c(ventana(a, b)), valor), n
    resp = _limpio(_respuesta(texto, "jue-c3-ej-clase"))
    assert dict(re.findall(r"(I|C2|D): (valor|piso|techo)", resp)) == {
        n: nombre[fijo[n][3]] for n, _, _ in vistos}


def test_prosa_clase_3_p4_ejercicio_final_otro_orden_y_un_reloj():
    """#39 · El ejercicio final de «Jugar contra el reloj»: el orden sale del
    enunciado; la tabla de la respuesta (4, 9, 11), el 24 contra 25, y lo que
    entrega cada reloj (10 y 20 nodos)."""
    texto = _pagina(P4)
    ej = _limpio(_bloque(texto, "jue-c3-ej-final-reloj"))
    acciones = list(re.search(r"A\(R\): (\w+), (\w+), (\w+)", ej).groups())
    corridas, entrega = j.iterativa_con_reloj_t(acciones)
    _, de_la_pagina = j.iterativa_con_reloj_t(["izq", "centro", "der"])
    assert int(re.search(r"con los (\d+) de la página", ej)[1]) == de_la_pagina["generados"]
    resp = _respuesta(texto, "jue-c3-ej-final-reloj")
    assert _filas(_tablas(resp)[0][1:]) == [
        (str(c["d"]), ", ".join(c["orden"]), c["jugada"], str(c["generados"])) for c in corridas]
    limpio = _limpio(resp)
    m = re.search(r"(\d+) nodos \((\d+), (\d+) y (\d+)\), uno menos que los (\d+)", limpio)
    assert [int(x) for x in m.groups()] == [entrega["generados"]] + [
        c["generados"] for c in corridas] + [de_la_pagina["generados"]]
    topes = [int(re.search(r"reloj de (\d+) nodos", ej)[1]),
             int(re.search(r"uno de (\d+)\?", ej)[1])]
    reloj = limpio.split("4. El reloj.")[1]
    segmentos = re.findall(r"Con (\d+) nodos:(.*?)(?=Con \d+ nodos:|$)", reloj, re.S)
    assert [int(t) for t, _ in segmentos] == topes
    for tope, seg in segmentos:
        _, e = j.iterativa_con_reloj_t(acciones, tope=int(tope))
        llega, tras = re.findall(r"a (\d+) tras (\w+)", seg)[-1]
        assert (int(llega), tras) == (e["generados"], e["despues_de"]), tope
        assert int(re.search(r"[Ll]a línea (\d+)", seg)[1]) == e["linea"], tope
        assert re.search(r"entrega (izq|centro|der)", seg)[1] == e["jugada"], tope
        assert int(re.search(r"de d=(\d+)", seg)[1]) == e["d"] - 1, tope


# ---- p5 · simular en vez de evaluar

def test_prosa_clase_3_p5_simulaciones_contra_corte_y_valor():
    """#39 · @jue-c3-simulaciones (0.21, 0.89, 0.15 / 2, 2, 13 / −1, +1, −1),
    @jue-c3-hexapawn-azar (7/36, 5/24 / 5/9, 3/4) y 17/18 y 29/48."""
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
    assert "las tres aperturas de Blancas valen -1" in prosa
    assert "Sus promedios de simulación son los tres positivos" in prosa
    assert all(x > 0 for par in esperado.values() for x in par)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-promedio"))
    pares = [(F(a), F(b)) for a, b in re.findall(r"p=\((\d+/\d+)\+1\)/2=(\d+/\d+)", resp)]
    d2d3 = j.promedio_simulaciones(j.mover(t, jugadas[1]), "N", 4)
    assert pares == [(d2d3, (d2d3 + 1) / 2), (ambos["b1-b2"], (ambos["b1-b2"] + 1) / 2)]


def test_prosa_clase_3_p5_la_vuelta_de_mcts():
    """#39 · La vuelta de la figura (2/4 → 3/5, 2/3 → 3/4, 0/1 → 1/2, 0/0 → 1/1),
    la misma con U = −1 (2/5, 2/4, 0/2, 0/1) y su ū en la raiz."""
    texto = _pagina(P5)
    gana = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    pierde = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=-1)
    camino = gana["camino"] + ["nuevo"]
    antes = {**gana["antes"], "nuevo": (0, 0)}
    fr = lambda gn: f"{gn[0]}/{gn[1]}"  # noqa: E731
    m = re.search(r"la raíz pasa de (\d+/\d+) a (\d+/\d+)", _titulo(texto, "jue-c3-fig-mcts"))
    assert m.groups() == (fr(antes["r"]), fr(gana["despues"]["r"]))
    alt = _alt(texto, "jue-c3-fig-mcts")
    retro = alt.split("retropropagación")[1]
    pares = re.findall(r"(\d+/\d+) (?:pasa )?a (\d+/\d+)", retro)
    assert pares == [(fr(antes[n]), fr(gana["despues"][n])) for n in camino]
    fuera = [n for n in j.MCTS_ARBOL if n not in camino]
    assert sorted(re.search(r"fuera del camino, (.*?), no cambian", retro)[1].replace(
        "el otro ", "").split(" y ")) == sorted(fr(antes[n]) for n in fuera)
    r, a, b = (antes[n] for n in ("r", "a", "b"))
    assert re.search(r"(\d+/\d+)=(\d+/\d+)\+(\d+/\d+)", _limpio(texto)).groups() == (
        fr(r), fr(a), fr(b))
    resp = _limpio(_respuesta(texto, "jue-c3-ej-retro"))
    uno = resp.split("2.")[0]
    assert re.findall(r"\d+/\d+", uno) == [x for n in camino
                                           for x in (fr(antes[n]), fr(pierde["despues"][n]))]
    g, n = pierde["despues"]["r"]
    m = re.search(r"=\((\d+)·(\d+)-(\d+)\)/(\d+)=(-?\d+(?:\.\d+)?)\. Antes de la vuelta valía (-?\d+(?:\.\d+)?)",
                  resp)
    g0, n0 = antes["r"]
    assert (int(m[1]), int(m[2]), int(m[3]), int(m[4])) == (2, g, n, n)
    assert (F(m[5]), F(m[6])) == (F(2 * g - n, n), F(2 * g0 - n0, n0))


def test_prosa_clase_3_p5_uct_en_el_ejercicio():
    """#39 · El ejercicio de MCTS: los datos x, y, z; ln 100 ≈ 4.61; los bonos
    0.28, 0.39, 0.68; los puntajes 0.78, 0.99, 0.88; seleccion y, entrega x."""
    import math
    texto = _pagina(P5)
    ej = _limpio(_bloque(texto, "jue-c3-ej-mcts"))
    datos = {k: (int(n), F(u)) for k, n, u in re.findall(
        r"([xyz]): N=(\d+) simulaciones, promedio \\bar u=(\d+(?:\.\d+)?)", ej)}
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
    # El resumen repite el puntaje de la seleccion: una lente de la ronda 3 no
    # vio 0.99→0.97 ahi, y ninguna prueba lo leia.
    resumen = _limpio(texto[texto.index("## Lo que hay que llevarse"):])
    elegido = max(puntajes, key=puntajes.get)
    m = re.search(r"la selección va a ([xyz]), que puntúa (\d+(?:\.\d+)?)", resumen)
    assert m and m[1] == elegido and float(m[2]) == round(puntajes[elegido], 2)


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
    """@jue-c3-ej-cinco (0.2, −0.2, mueve 0.4) y la frase de @jue-c3-resp-mcts:
    con G/N o con c = √2 la seleccion iria a z."""
    import math
    texto = _pagina(P5)
    resp = _limpio(_respuesta(texto, "jue-c3-ej-cinco"))
    ganadas = [(3, 2), (2, 3)]
    leidos = re.findall(r"\\bar u=\((\d)-(\d)\)/(\d)=(-?\d+(?:\.\d+)?)", resp)
    assert [(int(g), int(p)) for g, p, _, _ in leidos] == ganadas
    for g, p, n, u in leidos:
        assert int(n) == int(g) + int(p) and F(u) == F(int(g) - int(p), int(n))
    salto = F(re.search(r"promedio (\d+(?:\.\d+)?)", resp)[1])
    assert salto == abs(F(leidos[0][3]) - F(leidos[1][3]))
    mcts = _limpio(_respuesta(texto, "jue-c3-ej-mcts"))
    assert re.search(r"Con G/N o con c=\\sqrt2 la selección iría a ([xyz])", mcts)[1] == "z"
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
    assert {k: round(v, 2) for k, v in teoria.items()} == {"p": 1.22, "q": 1.44, "r": 2.1}
    assert {k: round(v, 2) for k, v in p5.items()} == {"p": 0.56, "q": 0.51, "r": 0.48}
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
            assert ahora["jugada"] == max(u, key=u.get), (semilla, ahora["t"])
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
