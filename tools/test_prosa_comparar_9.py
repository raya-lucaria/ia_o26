"""7.3.9 · «Elegir el algoritmo»: la prosa contra la fuente (defecto #39).

Cada cifra que cita la página (T±, la posición de peones de la clase, el
4×4 entero y el juego nuevo del ejercicio final) se localiza por un ancla
estable (id de directiva, sección, frase) y se compara con la función de
juegos.py o con la cuenta que la produce. Ninguna cifra esperada se escribe
a mano. Además fija los hechos corregidos de la tabla «cuándo conviene»
(rev-hechos.md): quién va en qué fila y qué no debe volver a aparecer.
"""
import math
import re
from fractions import Fraction as F

import juegos as j
from test_juegos import CLASE_3, _bloque, _c, _limpio, _llevarse, _respuesta, _tabla

P9 = "9_elegir_el_algoritmo.md"
_Q = r"[+-]?\d+(?:/\d+)?"


def _texto():
    return (CLASE_3 / P9).read_text(encoding="utf-8")


def _seccion(texto, n):
    m = re.search(rf"^## {n} ·.*?$(.*?)(?=^## )", texto, re.M | re.S)
    assert m, f"no encuentro la seccion {n}"
    return _limpio(m.group(1))


def _numero(s):
    return int(s.replace(" ", ""))


def _posicion():
    t = j.POSICION_C3
    return t, j.jugadas(t, "B", 4)


def test_9_la_tabla_de_cuando_conviene_con_los_juegos_corregidos():
    filas = _tabla(_texto(), "jue-c3-cmp-cuando")
    assert [_c(x) for x in filas[0]] == ["Algoritmo", "Conviene cuando", "Le cuesta",
                                         "Juego real"]
    assert all(len(f) == 4 for f in filas)
    juego = {_c(f[0]): _c(f[3]) for f in filas[1:]}
    assert list(juego) == ["Minimax y alfa-beta", "Expectiminimax",
                           "Alfa-beta con corte, quietud e iterativa", "Monte Carlo plano",
                           "MCTS con UCT"]
    exacto = juego["Minimax y alfa-beta"]
    assert "Conecta 4, resuelto en 1988" in exacto
    assert "Deep Blue" not in exacto and "Chinook" not in exacto
    assert "TD-Gammon (1992) miraba dos jugadas" in juego["Expectiminimax"]
    corte = juego["Alfa-beta con corte, quietud e iterativa"]
    assert "Deep Blue, 1997" in corte and "Chinook, con bases de finales" in corte
    assert "de 1993 a 2005" in juego["Monte Carlo plano"]
    assert juego["MCTS con UCT"] == "Go (MoGo, 2006); Hex (MoHex)"
    assert "Crazy Stone" not in _texto()
    uno = _seccion(_texto(), 1)
    # Los matices de rev-hechos: quietud no arregla todo; UCT converge con c
    # grande, y la del curso queda debajo de la hipotesis.
    assert "La quietud arregla los intercambios a medias, no todo" in uno
    assert "c suficientemente grande y tiempo sin límite" in uno
    assert "La c=1 del curso queda debajo de esa hipótesis" in uno


def test_9_el_mapa_en_t_pm():
    dos = _seccion(_texto(), 2)
    t_pm = dos.split("En T±.")[1].split("En la posición de la clase.")[0]
    jm, v, _, nodos = j.minimax_tpm()
    m = re.search(rf"Tiene (\d+) nodos: cabe, rama 1\. Alfa-beta juega (\w+) con "
                  rf"V=({_Q}) y genera (\d+)", t_pm)
    ja, va, generados, _ = j.alfa_beta_tpm("dado")
    assert m and (int(m[1]), m[2], int(m[3]), int(m[4])) == (nodos, ja, va, generados)
    assert (ja, va) == (jm, v)
    jc, vc, _, _ = j.corte_tpm(1)
    m = re.search(r"el corte a d=1 elige (\w+), con (\d+), y Monte Carlo plano elige (\w+)",
                  t_pm)
    assert m and (m[1], int(m[2]), m[3]) == (jc, vc, j.todos_al_azar_tpm()[0])
    je, ve = j.expectiminimax_tpm()
    m = re.search(rf"expectiminimax juega (\w+), que vale ({_Q})", t_pm)
    assert m and (m[1], F(m[2])) == (je, ve["R"])


def test_9_el_mapa_en_la_posicion_de_la_clase():
    dos = _seccion(_texto(), 2)
    pos = dos.split("En la posición de la clase.")[1]
    t, jugadas = _posicion()
    nodos, _ = j.contar_arbol(t, "B", 4)
    valor, generados, _ = j.alfa_beta(t, "B", 4)
    m = re.search(r"su árbol completo tiene (\d+) nodos, y alfa-beta lo resuelve "
                  r"generando (\d+)\. Juega ([a-d]\d-[a-d]\d), que gana: V=([+-]?\d+)", pos)
    assert m and (int(m[1]), int(m[2]), int(m[4])) == (nodos, generados, valor)
    ganadora = [j.nombre_jugada(t, a, 4) for a in jugadas
                if j.valor(j.mover(t, a), "N", n=4) == valor]
    assert ganadora == [m[3]]
    m = re.search(r"con ([\d ]+) nodos, también cabe; así se sabe que gana el primero", pos)
    assert m and _numero(m[1]) == j.contar_arbol(None, "B", 4)[0]
    assert j.valor(j.inicio(4), "B", n=4) == 1
    # Si no cupiera: corte a d = 1, quietud y simulacion.
    cortes = {j.nombre_jugada(t, a, 4): h["valor"]
              for a, h in zip(jugadas, j.arbol_con_corte(t, "B", 1, 4)["hijos"])}
    m = re.search(r"El corte a d=1 elige ([a-d]\dx[a-d]\d), con (\d+), que pierde", pos)
    assert m and max(cortes, key=cortes.get) == m[1] and cortes[m[1]] == int(m[2])
    assert j.valor(j.mover(t, jugadas[[j.nombre_jugada(t, a, 4) for a in jugadas]
                                       .index(m[1])]), "N", n=4) == -1
    quieta = {j.nombre_jugada(t, a, 4): j.minimax_con_quietud(j.mover(t, a), "N", 0, 4)
              for a in jugadas}
    m = re.search(r"Con quietud elige ([a-d]\d-[a-d]\d)", pos)
    assert m and max(quieta, key=quieta.get) == m[1]
    medias = {j.nombre_jugada(t, a, 4): j.promedio_simulaciones(j.mover(t, a), "N", 4)
              for a in jugadas}
    m = re.search(rf"([a-d]\d-[a-d]\d) promedia ({_Q}) en las simulaciones", pos)
    assert m and max(medias, key=medias.get) == m[1] and medias[m[1]] == F(m[2])


def test_9_el_ejercicio_del_mapa_cita_los_252_nodos_de_hexapawn():
    ej = _limpio(_bloque(_texto(), "jue-c3-cmp-ej-mapa"))
    m = re.search(r"Hexapawn, con sus (\d+) nodos", ej)
    assert m and int(m[1]) == j.contar_arbol()[0]


def test_9_fronteras_cuantas_partidas():
    resp = _limpio(_respuesta(_texto(), "jue-c3-cmp-ej-fronteras"))
    m = re.search(r"hay (\d+) jugadas y la partida siempre las juega todas, así que hay "
                  r"(\d+)! órdenes posibles, un número de (\d+) cifras", resp)
    assert m and int(m[1]) == int(m[2]) == 11 * 11
    assert int(m[3]) == len(str(math.factorial(int(m[2]))))
    m = re.search(r"Son (\d+) jugadas: (\d+)!= ([\d ]+) partidas", resp)
    assert m and int(m[1]) == int(m[2]) == 3 * 3
    assert _numero(m[3]) == math.factorial(9)
    enunciado = _limpio(_bloque(_texto(), "jue-c3-cmp-ej-fronteras"))
    assert "tablero de 11×11 casillas" in enunciado and "tras 121 jugadas" in enunciado


def test_9_el_ejercicio_final_tiene_preambulo_dos_pistas_y_respuesta():
    texto = _texto()
    cuatro = texto.split("## 4 ·")[1]
    assert ("**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin\n"
            "pedir ayuda a ChatGPT.**") in cuatro
    pistas = re.findall(r'^::: hint \{#[\w-]+ of="jue-c3-cmp-ej-fronteras" title="([^"]+)"',
                        texto, re.M)
    assert [p.split(" · ")[0] for p in pistas] == ["Pista 1", "Pista 2"]
    # Prueba de fuga: ninguna pista nombra el algoritmo de la respuesta.
    for ident in ("jue-c3-cmp-pista-fronteras-1", "jue-c3-cmp-pista-fronteras-2"):
        assert not re.search(r"MCTS|UCT|simul", _bloque(texto, ident), re.I)
    assert re.search(r'^::: answer \{#jue-c3-cmp-resp-fronteras of="jue-c3-cmp-ej-fronteras" '
                     r'title="Respuesta · ', texto, re.M)
    resp = _respuesta(texto, "jue-c3-cmp-ej-fronteras")
    assert [int(n) for n in re.findall(r"^\*\*(\d)\. ", resp, re.M)] == [1, 2, 3, 4, 5]
    for ej in re.findall(r"^::: exercise \{#([\w-]+)", texto, re.M):
        _respuesta(texto, ej)


def test_9_lo_que_hay_que_llevarse():
    llevarse = _llevarse(_texto())
    jm, v, _, nodos = j.minimax_tpm()
    ja, _, generados, _ = j.alfa_beta_tpm("dado")
    m = re.search(rf"minimax juega (\w+) con V=({_Q}) en (\d+) nodos, y alfa-beta lo "
                  rf"mismo en (\d+)", llevarse)
    assert m and (m[1], int(m[2]), int(m[3]), int(m[4])) == (jm, v, nodos, generados)
    jc, vc, _, _ = j.corte_tpm(1)
    m = re.search(r"El corte a d=1 elige (\w+), con (\d+), y la quietud lo corrige: (\w+)",
                  llevarse)
    assert m and (m[1], int(m[2]), m[3]) == (jc, vc, j.quietud_tpm(1)[0])
    m = re.search(r"Monte Carlo plano elige (\w+); UCT vuelve a (\w+)", llevarse)
    uct = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)["mas_simulada"][-1]
    assert m and (m[1], m[2]) == (j.todos_al_azar_tpm()[0], uct)
    je, ve = j.expectiminimax_tpm()
    m = re.search(rf"Con un dado en D, la jugada es (\w+), que vale ({_Q})", llevarse)
    assert m and (m[1], F(m[2])) == (je, ve["R"])
    t, jugadas = _posicion()
    m = re.search(r"(\d+) nodos, (\d+) con alfa-beta, y ([a-d]\d-[a-d]\d) gana\. El corte a "
                  r"d=1 elegía ([a-d]\dx[a-d]\d), con (\d+)", llevarse)
    assert m and (int(m[1]), int(m[2])) == (j.contar_arbol(t, "B", 4)[0],
                                            j.alfa_beta(t, "B", 4)[1])
    cortes = {j.nombre_jugada(t, a, 4): h["valor"]
              for a, h in zip(jugadas, j.arbol_con_corte(t, "B", 1, 4)["hijos"])}
    assert cortes[m[4]] == int(m[5]) == max(cortes.values())
    assert j.valor(j.mover(t, jugadas[[j.nombre_jugada(t, a, 4) for a in jugadas]
                                       .index(m[3])]), "N", n=4) == 1


def test_9_continua_a_la_clase_4():
    texto = _texto()
    assert texto.rstrip().endswith(
        "Continúa con [[juegos-sin-turnos|la clase 4, cuando no hay turnos]].")
    assert "[[que-numero-da-cada-uno|" in texto
