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
    assert j.valor(j.inicio(), "B", util=j.utilidad_rapida,
                   sin_jugada_empata=True) == 0
    assert j.contar_arbol(sin_jugada_empata=True) == (252, 135)


def test_clase_2_minimax_y_alfa_beta():
    assert j.valor(j.inicio(), "B", util=j.utilidad_rapida) == -4
    hijos = {j.nombre_jugada(j.inicio(), m):
             j.valor(j.mover(j.inicio(), m), "N", 1, util=j.utilidad_rapida)
             for m in j.jugadas(j.inicio(), "B")}
    assert hijos == {"a1-a2": -6, "b1-b2": -4, "c1-c2": -6}
    assert j.contar_arbol(SUBARBOL) == (13, 13)
    assert j.valor(SUBARBOL, "B", 2, util=j.utilidad_rapida) == 7
    assert j.alfa_beta(SUBARBOL, "B", 2) == (7, 5, [("alfa", "a3xb2", 2)])
    assert j.alfa_beta(SUBARBOL, "B", 2, invertir=True) == (
        7, 8, [("beta", "b2xa3", 2)])


def test_clase_2_dado_y_tarea():
    d = j.dado_ejemplo()
    assert d["tirar"] == F(4, 3) and d["plantarse"] == 1
    assert d["tirar_si_el_dado_fuera_rival"] == -2
    assert j.monedas_valor((2, 1, 5, 3)) == 3
    assert j.monedas_codicioso_contra_optimo((2, 1, 5, 3)) == -1
    assert j.monedas_conteos(4) == (23, 8, 11)
    assert j.monedas_alfa_beta((2, 1, 5, 3)) == (3, 23)
    assert j.monedas_alfa_beta((2, 1, 5, 3), True) == (3, 21)
    assert j.cerdo_tirar(3, 1) == F(35, 6)
    assert j.cerdo(3, 2) == F(275, 36)
    # Con una sola tirada, tirar conviene mientras los puntos no pasen de 20.
    assert all(j.cerdo_tirar(s, 1) >= s for s in range(0, 21))
    assert j.cerdo_tirar(20, 1) == 20 and j.cerdo_tirar(21, 1) < 21


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


def test_clase_2_numeros_de_la_prosa():
    tras_a2 = j.mover(j.inicio(), (0, 3))  # a1-a2
    respuestas = {j.nombre_jugada(tras_a2, m): j.valor(j.mover(tras_a2, m), "B", 2,
                                                        util=j.utilidad_rapida)
                  for m in j.jugadas(tras_a2, "N")}
    assert respuestas["b3-b2"] == 7 and respuestas["b3xa2"] == -6
    assert j.valor(SUBARBOL, "B", 2) == 1
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
    assert (total, maximo) == (162, 4)
    # Ejercicio del dado: plantarse +2; con 1 se pierde -3; con 2 a 6 el rival
    # elige entre +4 y +6.
    assert F(1, 6) * -3 + F(5, 6) * 4 == F(17, 6)
    assert F(1, 6) * -3 + F(5, 6) * F(4 + 6, 2) == F(11, 3)
    # Ejemplo de la pagina si se promediara al rival.
    assert F(2, 6) * -2 + F(4, 6) * F(7, 2) == F(5, 3)


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


def test_clase_2_caso_propio_y_dado():
    assert sum(4 ** i for i in range(8)) == 21845
    assert F(2, 6) * -20 + F(4, 6) * min(F(3), F(4)) == F(-14, 3)
    assert j.contar_arbol("..B.B.NN.", "N") == (11, 11)
    assert j.valor("..B.B.NN.", "N", 3, util=j.utilidad_rapida) == -4
    for n in range(1, 9):
        assert j.monedas_conteos(n)[0] == 2 ** n - 1 + 2 ** (n - 1)


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
