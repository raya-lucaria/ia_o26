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
    # (a) Los hijos de la raiz al reves: der, centro, izq.
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
