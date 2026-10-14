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
    texto = _texto()
    filas = _tabla(texto, "jue-c3-cmp-cuando")
    assert [_c(x) for x in filas[0]] == ["Algoritmo", "Conviene cuando"]
    orden = ["Minimax", "Expectiminimax", "Alfa-beta", "Corte, quietud e iterativa",
             "Monte Carlo plano", "MCTS con UCT"]
    cuando = {_c(f[0]): _c(f[1]) for f in filas[1:]}
    assert list(cuando) == orden  # el orden del curso
    # El mapa pregunta por los dados dentro de «¿cabe?»: la tabla dice lo mismo.
    assert cuando["Expectiminimax"] == "Cabe y hay dados"
    assert cuando["Alfa-beta"] == "Cabe y no hay dados"
    # r3: con «cabe» = la búsqueda exacta CON poda termina, minimax pide más:
    # recorrer todo el árbol, sin poda.
    # La celda va corta (cinco palabras, abajo); la prosa de arriba lo dice.
    assert cuando["Minimax"] == "Cabe sin poda, sin dados"
    assert "Minimax pide más: que quepa recorrer todo el árbol, sin poda." in \
        " ".join(texto.split())
    costo = _tabla(texto, "jue-c3-cmp-cuesta")
    assert [_c(x) for x in costo[0]] == ["Algoritmo", "Le cuesta"]
    assert [_c(f[0]) for f in costo[1:]] == orden
    # Dos columnas y celdas cortas, para que quepan a 390 px.
    for f in filas[1:] + costo[1:]:
        assert len(f) == 2 and all(len(_c(x).split()) <= 5 for x in f), f
    # El juego real va en una lista, en el mismo orden que las tablas.
    lista = texto.split("Dónde se usó cada uno, en el mismo orden:")[1].split("::: table")[0]
    juego = dict(re.findall(r"^- \*\*([^*]+):\*\* (.*?)(?=^- |\Z)", lista, re.M | re.S))
    juego = {k: _limpio(v).strip() for k, v in juego.items()}
    assert list(juego) == orden
    # Allis (1988) usó reglas y búsqueda, no alfa-beta pura (registro, fila 2b).
    assert juego["Alfa-beta"] == ("Conecta 4, resuelto en 1988 con búsqueda y reglas; hoy "
                                  "alfa-beta con tablas de transposición lo resuelve sola.")
    assert "volado" not in texto  # el juguete no va como juego real
    assert "TD-Gammon (1992) miraba dos jugadas" in juego["Expectiminimax"]
    assert juego["Corte, quietud e iterativa"] == ("ajedrez (Deep Blue, 1997) y damas "
                                                   "(Chinook, con bases de finales).")
    assert all("Deep Blue" not in juego[a] for a in ("Minimax", "Alfa-beta"))
    assert juego["Monte Carlo plano"] == "Go, de 1993 a 2005."
    assert juego["MCTS con UCT"] == "Go (MoGo, 2006) y Hex (MoHex)."
    assert "Crazy Stone" not in texto
    uno = _seccion(_texto(), 1)
    # Los matices de rev-hechos: quietud no arregla todo; UCT llega con
    # cualquier c > 0 en un árbol finito, y lo que pide una c grande es la cota
    # de Kocsis y Szepesvári, que la c=1 del curso no tiene.
    assert "La quietud arregla los intercambios a medias, no todo" in uno
    assert ("UCT tiende a la jugada de minimax con tiempo sin límite, con cualquier c>0 en "
            "un árbol finito. Kocsis y Szepesvári acotaron qué tan rápido, con una c grande; "
            "la c=1 del curso no tiene esa cota, aunque aquí funcionó. De dónde sale la cota "
            "de UCB1 lo viste en [[de-donde-sale-el-bono|") in uno
    assert "suficientemente grande" not in _texto()
    assert j.GARANTIZA_TPM["UCT"] == "No (con tiempo sin límite converge a él, con cualquier c > 0)"
    # Monte Carlo plano también se interrumpe con el reloj (su ficha lo dice).
    assert "La iterativa, Monte Carlo plano y MCTS son las que se interrumpen con el reloj" in uno


def test_9_el_mapa_en_t_pm():
    dos = _seccion(_texto(), 2)
    t_pm = dos.split("En T±.")[1].split("En la posición de la clase.")[0]
    jm, v, _, nodos = j.minimax_tpm()
    m = re.search(rf"Tiene (\d+) nodos y no tiene dados: cabe, rama 1\. Alfa-beta juega (\w+) con "
                  rf"V=({_Q}) y genera (\d+)", t_pm)
    ja, va, generados, _ = j.alfa_beta_tpm("dado")
    assert m and (int(m[1]), m[2], int(m[3]), int(m[4])) == (nodos, ja, va, generados)
    assert (ja, va) == (jm, v)
    jc, vc, _, _ = j.corte_tpm(1)
    m = re.search(r"el corte a d=1 elige (\w+), con (\d+), y Monte Carlo plano elige (\w+)",
                  t_pm)
    assert m and (m[1], int(m[2]), m[3]) == (jc, vc, j.todos_al_azar_tpm()[0])
    je, ve = j.expectiminimax_tpm()
    m = re.search(rf"Si D fuera un dado, seguiría en la rama 1, ahora con dados: "
                  rf"expectiminimax juega (\w+), que vale ({_Q})", t_pm)
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
    m = re.search(rf"si desde ([a-d]\d-[a-d]\d) los dos juegan al azar hasta el final, U "
                  rf"promedia ({_Q}), lo más alto de las (\w+) jugadas", pos)
    assert m and m[3] == "tres" and len(medias) == 3
    assert m and max(medias, key=medias.get) == m[1] and medias[m[1]] == F(m[2])


def test_9_el_mapa_pregunta_por_los_dados_dentro_de_cabe():
    dos = _seccion(_texto(), 2)
    # «Cabe» es que la búsqueda exacta termine, no que se recorra todo el
    # árbol (brief r2 W3-9); y el mapa es para las versiones de la unidad:
    # MCTS también puede usar una evaluación (brief r2 W3-10).
    assert ("«Cabe» quiere decir que una búsqueda exacta (alfa-beta, con tablas de "
            "transposición) termina en el tiempo que hay, aunque no recorra todo el "
            "árbol.") in _seccion(_texto(), 1)
    assert ("Las ramas 3 y 4 eligen entre las versiones de esta unidad. Fuera de ella, MCTS "
            "también puede usar una evaluación: AlphaGo valoraba sus hojas con una red") in dos
    assert "Sí, sin dados: alfa-beta" in dos and "Sí, con dados: expectiminimax" in dos
    assert "No cabe: ¿hay dados?" in dos and "nada más importa" not in dos
    assert "No tiene dados, y en la computadora sí cabe, así que es la rama 1" in dos


def test_9_cuatro_supuestos_en_el_recuadro_y_en_la_seccion_3():
    texto = _limpio(_texto().replace("\n> ", "\n"))
    recuadro = texto.split("Supuestos de esta página.")[1].split("El azar")[0]
    assert "Los cuatro de toda la unidad: dos jugadores, suma cero, por turnos y todo a " \
           "la vista" in recuadro
    tres = _texto().split("## 3 ·")[1].split("## 4 ·")[0]
    lista = re.findall(r"^- \*\*([^*]+?)\.\*\*", tres.split("Los cuatro supuestos")[1]
                       .split("Para ubicar")[0], re.M)
    assert lista == ["Dos jugadores", "Suma cero", "Por turnos", "Todo a la vista"]
    assert "toda partida termina" not in texto
    # Suma no cero con dos: un ejemplo en palabras, sin pagos por jugador.
    assert "Con dos jugadores también se rompe, si cada uno tiene su propio pago" in texto
    assert "rompecabezas" in texto
    # max^n y el paranoico no cortan siempre: cortarían en un árbol que no cabe.
    resp = _limpio(_respuesta(_texto(), "jue-c3-cmp-ej-fronteras"))
    assert "pero cortan y estiman" not in resp
    assert "el paranoico llegan a los finales si el árbol cabe" in resp


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
    assert ("Con tiempo sin límite, y cualquier c>0, tendería a la de minimax; 10 segundos no "
            "son tiempo sin límite.") in resp
    # Con tabla de transposición no se recorren órdenes sino posiciones; aun
    # así no cabe (brief r2 W3-9).
    m = re.search(r"Aun contando cada posición una sola vez, como hace una tabla de "
                  r"transposición, son un número de (\d+) cifras", resp)
    assert m and int(m[1]) == len(str(j.posiciones_fronteras(11)))
    # «No se tiene una EVAL confiable», no «no hay EVAL buena» (brief r2 W3-12).
    assert ("No se tiene una EVAL confiable: la obvia, el grupo más grande, engaña según "
            "quienes lo juegan, y no hay otra.") in resp
    assert "No hay EVAL buena" not in resp
    assert "Nadie tiene otra estimación a la mano." in _limpio(
        _bloque(_texto(), "jue-c3-cmp-ej-fronteras"))
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


def test_9_la_regla_del_menos_uno_se_cobra_en_la_seccion_3():
    """p8 cierra la regla de dejar de buscar con «supone suma cero; la página
    siguiente lo pone en duda». La sección 3 la cobra: el −1 de MAX es el
    máximo de MIN, y con pagos propios MIN tendría que seguir mirando. Y el
    ix=-1 que cita es el de p8 (la hoja de I que hace parar a MIN)."""
    tres = _limpio(_texto().split("## 3 ·")[1].split("## 4 ·")[0])
    m = re.search(r"Y por lo mismo vale la regla de dejar de buscar de \[\[que-numero-da-cada-uno\|"
                  rf"Qué número da cada uno\]\]: en I, si ix fuera su primera hoja, MIN pararía al ver (\w+)=({_Q}) porque el "
                  r"-1 de MAX es el máximo de MIN\.", tres)
    assert m and m[1] == j.ids_tpm()[(0, 1)] and int(m[2]) == j.nodo_en(j.ARBOL_TPM, (0, 1)) == -1
    assert ("un final malo para MAX no le diría a MIN que deje de buscar: puede no ser el "
            "mejor para MIN, y tendría que seguir mirando") in tres
    # La promesa de p8 («la página siguiente dice por qué»), con un caso concreto:
    # el final es el mínimo de MAX pero no el máximo de MIN.
    m = re.search(rf"un final que para MAX vale ({_Q}) pero para MIN solo ({_Q}), mientras otra "
                  rf"hoja le da ({_Q}) a MIN: MIN no se detiene en ese final", tres)
    assert m and int(m[1]) == min(j.nodo_en(j.ARBOL_TPM, c) for c in j.ids_tpm()
                                  if not isinstance(j.nodo_en(j.ARBOL_TPM, c), tuple))
    assert int(m[2]) < int(m[3])
    p8 = (CLASE_3 / "8_que_numero_da_cada_uno.md").read_text(encoding="utf-8")
    assert "en I, MIN ve\n${\\text{ix}=-1}$ y ya no necesita mirar i1" in p8
    assert "y eso supone **suma\ncero**" in p8
    # La suma cero se retoma en su página de la clase 4, no en el índice.
    assert "La clase 4 lo retoma en [[cuando-no-es-suma-cero|Cuando no es suma cero]]" in tres
    assert "La clase 4 lo retoma: [[juegos-sin-turnos" not in _texto()
    cuatro = CLASE_3.parent / "4_sin_turnos" / "3_cuando_no_es_suma_cero.md"
    assert "id: cuando-no-es-suma-cero" in cuatro.read_text(encoding="utf-8")


def test_9_la_rama_2_sin_eval_va_a_simular():
    dos = _seccion(_texto(), 2)
    assert ("No cabe: ¿hay dados? Sí, con una EVAL: corte con nodos de azar, que se "
            "promedian, como TD-Gammon. Sí, sin EVAL: la rama 4, que también "
            "simula los dados.") in dos
    assert "4. ¿No la hay? MCTS con UCT. Solo pide las reglas, para simular." in dos


def test_9_monte_carlo_plano_supone_a_ambos_al_azar():
    costo = {_c(f[0]): _c(f[1]) for f in _tabla(_texto(), "jue-c3-cmp-cuesta")[1:]}
    assert costo["Monte Carlo plano"] == "Supone a ambos al azar"
    assert "rivales al azar" not in _texto()


def test_9_la_tabla_de_no_suma_cero():
    """Pedido del profesor: una tabla de suma cero y otra de no suma cero. Tres
    columnas, celdas cortas (390 px), sin U_1/U_2, en el orden de la prosa de
    abajo; los hechos son los de las filas 29–31 del registro."""
    texto = _texto()
    filas = _tabla(texto, "jue-c3-cmp-no-suma-cero")
    assert "{#jue-c3-cmp-no-suma-cero title=\"Más de dos jugadores o sin suma cero, para ubicar\"}" in texto
    assert [_c(x) for x in filas[0]] == ["Algoritmo", "Cada rival elige", "¿Poda?"]
    tabla = {_c(f[0]): (_c(f[1]), _c(f[2])) for f in filas[1:]}
    assert tabla == {"\\max^n": ("Lo mejor para él", "Casi no"),
                     "Paranoico": ("Lo peor para ti", "Sí: alfa-beta"),
                     "MCTS con varios jugadores": ("Por su propio promedio", "No: simula")}
    for f in filas[1:]:
        assert len(f) == 3 and all(len(_c(x).split()) <= 4 for x in f), f
    assert "U_1" not in texto and "U_2" not in texto
    # PUCT ya venía de AlphaGo (registro, fila 28); Zero y AlphaZero quitan
    # las partidas simuladas hasta el final, no las vueltas de MCTS (brief r2 W3-11).
    assert ("AlphaGo Zero (2017) y AlphaZero ya no juegan partidas simuladas hasta el final: "
            "cada vuelta de MCTS valora la hoja con la red (la selección con PUCT") in _limpio(texto)
    assert "ya no simulan" not in _limpio(texto)
    assert "ya venía de AlphaGo)" in _limpio(texto)
    # max^n necesita una regla de desempate (brief r2 W3-13).
    assert ("También pide una regla de desempate: si un rival tiene dos jugadas que le dan lo "
            "mismo a él pero no a ti, el resultado depende de cuál supongas que elige.") in \
        _limpio(texto.split("## 3 ·")[1].split("## 4 ·")[0])
    # MCTS no juega todo al azar: por puntaje en el árbol, al azar debajo.
    traes = _limpio(texto.split("Lo que traes de")[1].split("T±, en tres líneas")[0].replace("\n> ", "\n"))
    assert ("en Monte Carlo plano los dos juegan al azar; en MCTS, eligen por puntaje dentro "
            "del árbol y al azar solo debajo") in traes
    assert "o los dos jugando al azar (en MCTS, solo debajo del árbol)" in _llevarse(texto)
    tres = _limpio(texto.split("## 3 ·")[1].split("## 4 ·")[0])
    assert ("Cuando mueves tú, eliges por el tuyo; lo que cambia es qué se supone de los "
            "rivales") in tres
    for cita in ("Luckhardt e Irani (1986), y Korf (1991) mostró que casi no poda",
                 "El paranoico (Sturtevant y Korf, 2000)",
                 "MCTS con varios jugadores (Sturtevant, 2008)"):
        assert cita in tres
    registro = (CLASE_3.parents[2] / "docs" / "verificacion" / "juegos" /
                "0_index.md").read_text(encoding="utf-8")
    for fuente in ("Multi-player alpha-beta pruning", "On Pruning Techniques for Multi-Player",
                   "An Analysis of UCT in Multi-Player Games"):
        assert fuente in registro
    # Los ejercicios remiten a «para ubicar», ya no a «la lista».
    assert "la lista «para ubicar»" not in texto
