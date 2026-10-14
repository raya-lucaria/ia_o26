"""7.3.8 · «Qué número da cada uno»: la prosa contra la fuente (defecto #39).

Cada cifra de T± que cita la página se localiza por un ancla estable (id de
directiva, sección, frase) y se compara con la función de juegos.py que la
calcula. Ninguna cifra esperada se escribe a mano.
"""
import re
from fractions import Fraction as F

import gen_resumen_juegos as resumen
import juegos as j
from test_juegos import (CLASE_3, _bloque, _c, _limpio, _llevarse, _respuesta,
                         _tabla)

P8 = "8_que_numero_da_cada_uno.md"
_Q = r"[+-]?\d+(?:/\d+|\.\d+)?"


def _texto():
    return (CLASE_3 / P8).read_text(encoding="utf-8")


def _seccion(texto, n):
    m = re.search(rf"^## {n} ·.*?$(.*?)(?=^## )", texto, re.M | re.S)
    assert m, f"no encuentro la seccion {n}"
    return _limpio(m.group(1))


def _q(s):
    return F(s.replace("+", ""))


def _sin_directivas(s):
    """La prosa de una seccion sin los bloques ::: (ejercicios, tablas…)."""
    return re.sub(r"^::: .*?^:::[ \t]*$", "", s, flags=re.M | re.S)


def test_8_el_valor_v_con_y_sin_dado():
    jugada, v, vs, _ = j.minimax_tpm()
    uno = _seccion(_texto(), 1)
    m = re.search(rf"En T±, V=({_Q}) por (\w+)\. MIN responde (\w+), y MAX empata con (\w+)\.",
                  uno)
    assert (_q(m[1]), m[2]) == (v, jugada)
    assert m[3] == "c1" and j.nodo_en(j.ARBOL_TPM, (1, 0, 0)) == 0 and m[4] == "c1a"
    m = re.search(r"Por izq o por der, MIN gana con (\w+) o con (\w+)\.", uno)
    ids = j.ids_tpm()
    for jugada_raiz, hoja in zip(("izq", "der"), m.groups()):
        camino = next(c for c, n in ids.items() if n == hoja)
        assert j.JUGADAS_RAIZ[camino[0]] == jugada_raiz
        assert j.nodo_en(j.ARBOL_TPM, camino) == -1 == vs[jugada_raiz]
    # El dado en D
    je, ve = j.expectiminimax_tpm()
    m = re.search(rf"D vale el promedio: \(({_Q})\+({_Q})\+({_Q})\)/3=({_Q})", uno)
    assert [_q(x) for x in m.groups()[:3]] == list(j.ARBOL_TPM[2])
    assert _q(m[4]) == ve["D"]
    m = re.search(rf"Con ese dado, MAX juega (\w+) y V=({_Q})\.", uno)
    assert (m[1], _q(m[2])) == (je, ve["R"])


def test_8_el_valor_con_corte_y_la_quietud():
    uno = _seccion(_texto(), 1)
    j1, v1, _, _ = j.corte_tpm(1)
    m = re.search(rf"El corte a d=({_Q}) eligió (\w+) con ({_Q})\. Ese \d+ no es una "
                  rf"utilidad: es EVAL\((\w+)\)", uno)
    assert (int(m[1]), m[2], int(m[3])) == (1, j1, v1)
    assert j.EVAL_TPM[m[4]] == v1 and m[4] == "ICD"[j.JUGADAS_RAIZ.index(j1)]
    vs = j.minimax_tpm()[2]
    m = re.search(rf"en realidad izq vale ({_Q}), o ({_Q}) en esa escala", uno)
    assert (_q(m[1]), _q(m[2])) == (vs["izq"], 100 * vs["izq"])
    m = re.search(rf"Con d=2 da ({_Q}); con d=3 ya llega a todos los finales y da ({_Q}), "
                  rf"que es 100· ?V", uno)
    assert int(m[1]) == j.corte_tpm(2)[1]
    _, v3, _, n3 = j.corte_tpm(3)
    assert int(m[2]) == v3 == 100 * j.minimax_tpm()[1] and n3 == j.contar_nodos(j.ARBOL_TPM)
    jq, vq, _, _, _ = j.quietud_tpm(1)
    m = re.search(rf"La quietud con d=1 elige (\w+), la jugada buena, pero con ({_Q})", uno)
    assert (m[1], int(m[2])) == (jq, vq) and jq == j.minimax_tpm()[0]
    assert vq != 100 * j.minimax_tpm()[1]


def test_8_el_promedio_de_simulaciones_y_uct():
    uno = _seccion(_texto(), 1)
    jugada, mu = j.todos_al_azar_tpm()
    leidos = {a: _q(x) for a, x in re.findall(rf"\\mu\\?\((izq|centro|der)\)=({_Q})", uno)}
    assert leidos == mu
    assert re.search(r"Con muchas simulaciones elige (\w+)\.", uno)[1] == jugada
    m = re.search(rf"Pero V\(der\)=({_Q}): un MIN racional juega (\w+)\.", uno)
    assert _q(m[1]) == j.minimax_tpm()[2]["der"] == j.nodo_en(j.ARBOL_TPM, (2, 0))
    assert m[2] == j.ids_tpm()[(2, 0)]
    # La corrida de UCT de la pagina anterior y la vuelta 100
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    m = re.search(rf"a las (\d+) vueltas centro tiene N=(\d+) y \\bar u=({_Q})\. Coincide "
                  rf"con V=({_Q}) por casualidad: a la vuelta (\d+) es ({_Q})\.", uno)
    assert int(m[1]) == j.VUELTAS_PAGINA_TPM
    assert u["mas_simulada"][-1] == "centro"
    assert (int(m[2]), _q(m[3])) == (u["N"][(1,)], F(u["S"][(1,)], u["N"][(1,)]))
    assert _q(m[4]) == j.minimax_tpm()[1] == _q(m[3])
    u2 = j.uct_tpm(1, int(m[5]), j.SEMILLA_TPM)
    assert _q(m[6]) == F(u2["S"][(1,)], u2["N"][(1,)]) != _q(m[3])


def test_8_v_con_dado_y_u_dan_el_mismo_tercio_en_der():
    rem = _limpio(_bloque(_texto(), "jue-c3-cmp-v-no-es-u"))
    m = re.search(rf"En der, V con dado y el \\mu de Monte Carlo plano dan ({_Q}) por la misma cuenta", rem)
    assert _q(m[1]) == j.expectiminimax_tpm()[1]["D"] == j.todos_al_azar_tpm()[1]["der"]
    m = re.search(rf"donde V\(der\)=({_Q})", rem)
    assert _q(m[1]) == j.minimax_tpm()[2]["der"]


def test_8_el_ejercicio_cambia_una_hoja():
    """d2 = −1: V no se mueve, el dado ya no paga más que centro, y MC plano
    cambia a izq, que también pierde. Todo con las funciones de T± sobre el
    árbol cambiado; la respuesta no está en la página anterior."""
    texto = _texto()
    ej = _limpio(_bloque(texto, "jue-c3-cmp-ej-cambia-hoja"))
    m = re.search(rf"cambia una sola hoja: ahora (\w+)=({_Q})", ej)
    ids = j.ids_tpm()
    camino = next(c for c, n in ids.items() if n == m[1])
    assert j.nodo_en(j.ARBOL_TPM, camino) != _q(m[2])
    d = list(j.ARBOL_TPM[camino[0]])
    d[camino[1]] = int(_q(m[2]))
    arbol = tuple(tuple(d) if i == camino[0] else h for i, h in enumerate(j.ARBOL_TPM))
    jm, v, vs, _ = j.minimax_tpm(arbol)
    assert (jm, v) == j.minimax_tpm()[:2]
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-cambia-hoja"))
    m = re.search(rf"1\. No: V=({_Q}) por (\w+)\. MIN ya respondía (\w+) en D, así que der "
                  rf"seguía valiendo ({_Q})\.", resp)
    assert (_q(m[1]), m[2]) == (v, jm) and _q(m[4]) == vs["der"] == j.minimax_tpm()[2]["der"]
    assert ids[(2, d.index(min(d)))] == m[3]
    je, ve = j.expectiminimax_tpm(arbol=arbol)
    # El inciso 2 no se contesta copiando @jue-c3-cmp-ej-dado (d3=-1): pregunta
    # por qué sale lo mismo. Y sale lo mismo de verdad: D y la jugada coinciden.
    p7 = (CLASE_3 / "7_un_arbol_todos_los_algoritmos.md").read_text(encoding="utf-8")
    m = re.search(rf"Cambia (\w+) de ({_Q}) a ({_Q}), con el dado parejo en D",
                  _limpio(_bloque(p7, "jue-c3-cmp-ej-dado")))
    otro = next(c for c, n in ids.items() if n == m[1])
    assert otro != camino and otro[0] == camino[0] and int(_q(m[3])) == int(_q(re.search(
        rf"ahora \w+=({_Q})", ej)[1]))
    d7 = list(j.ARBOL_TPM[otro[0]])
    d7[otro[1]] = int(_q(m[3]))
    arbol7 = tuple(tuple(d7) if i == otro[0] else h for i, h in enumerate(j.ARBOL_TPM))
    je7, ve7 = j.expectiminimax_tpm(arbol=arbol7)
    assert (je7, ve7["D"], ve7["R"]) == (je, ve["D"], ve["R"]) and sorted(d7) == sorted(d)
    assert ("Sale lo mismo que en @jue-c3-cmp-ej-dado, donde cambiabas d3. ¿Por qué, si "
            "cambiaste otra hoja?") in ej
    m = re.search(rf"2\. Porque un promedio no mira cuál hoja es cuál\. Con (\w+) o con (\w+) "
                  rf"en ({_Q}), D tiene dos hojas en ({_Q}) y una en ({_Q}): vale "
                  rf"\(({_Q})({_Q})\+({_Q})\)/3=({_Q})\. Ahora der queda debajo "
                  rf"del ({_Q}) de centro, y MAX juega (\w+) con V=({_Q})\.", resp)
    assert {m[1], m[2]} == {ids[camino], ids[otro]} and _q(m[3]) == min(d)
    assert [d.count(_q(m[4])), d.count(_q(m[5]))] == [2, 1]
    assert [_q(x) for x in m.groups()[5:8]] == d and _q(m[9]) == ve["D"]
    assert _q(m[10]) == ve["C"] > ve["D"] and (m[11], _q(m[12])) == (je, ve["R"])
    assert ve["R"] == v and j.expectiminimax_tpm()[1]["R"] != v   # casualidad nueva
    jt, mu = j.todos_al_azar_tpm(arbol)
    m = re.search(rf"3\. (\w+)\. Su μ=({_Q}) no cambia, centro sigue en ({_Q}) y der baja a "
                  rf"({_Q})\. Pero izq vale ({_Q}): MIN responde (\w+)\.", resp.replace("\\mu", "μ"))
    assert m[1].lower() == jt != j.todos_al_azar_tpm()[0]
    assert (_q(m[2]), _q(m[3]), _q(m[4])) == (mu["izq"], mu["centro"], mu["der"])
    assert mu["izq"] == j.todos_al_azar_tpm()[1]["izq"]
    assert mu["centro"] == j.todos_al_azar_tpm()[1]["centro"]
    assert _q(m[5]) == vs["izq"] < v and ids[(0, 1)] == m[6]


# Nombres cortos de la prosa sobre la tabla «Qué supone cada número»
_CORTOS = {"minimax": "Minimax", "expectiminimax": "Expectiminimax",
           "alfa-beta": "Alfa-beta", "el corte": "Minimax con corte",
           "la quietud": "Búsqueda de quietud", "la iterativa": "Profundización iterativa",
           "Monte Carlo plano": "Monte Carlo plano", "MCTS": "MCTS con UCT"}


def test_8_la_tabla_de_que_supone_cada_numero():
    """Tres filas, una por número, a dos columnas (cabe a 390 px). La frase
    de arriba reparte los ocho algoritmos entre los tres números, en el
    orden del curso, sin repetir ni olvidar ninguno."""
    texto = _texto()
    filas = _tabla(texto, "jue-c3-cmp-num-supone")
    assert [c.strip() for c in filas[0]] == ["Número", "Supone que"]
    assert [_c(f[0]) for f in filas[1:]] == ["V", "Valor con corte", "\\bar u"]
    # Monte Carlo plano juega todo al azar; MCTS, solo debajo del árbol.
    assert _c(filas[3][1]) == "Se juega al azar (en MCTS, solo debajo del árbol)"
    rem = _limpio(_bloque(texto, "jue-c3-cmp-v-no-es-u"))
    assert "el \\bar u de Monte Carlo plano no es V, ni con muchas simulaciones" in rem
    assert "El de MCTS, que dentro del árbol elige por puntaje, tiende a V conforme crecen las vueltas" in rem
    m = re.search(r"V lo dan (.+?)\. El valor con corte lo dan (.+?)\. Y \\bar u, (.+?)\.",
                  _seccion(texto, 2))
    dan = [_CORTOS[n] for g in m.groups() for n in re.split(r", | y ", g)]
    assert dan == [a["nombre"] for a in resumen.ALGORITMOS]


def test_8_garantiza_v_quien_llega_a_los_finales_o_prueba_que_no_cambia_nada():
    """El resumen de la sección 2 dice las dos mitades, como la respuesta al
    «Piensa» de arriba: alfa-beta garantiza V y no llega a todos los finales."""
    dos = _seccion(_texto(), 2)
    assert "Llegar a los finales, o probar que lo que no mira no cambia nada" in dos
    # Brief r2 W3-7: el orden al azar no rompe la exactitud; lo que la rompe
    # es que los jugadores dejen de elegir.
    assert ("y no cambiar las decisiones de los jugadores por jugadas al azar.") in dos
    assert "no tirar dados" not in dos
    assert ("Por eso garantiza V quien supone que todos eligen lo mejor y llega a los "
            "finales, o prueba que lo que no mira no cambia nada.") in dos
    _, _, generados, podados = j.alfa_beta_tpm("dado")
    assert podados and generados < j.contar_nodos(j.ARBOL_TPM)


def test_8_la_garantia_de_v_se_remite_a_la_tabla_de_p7():
    """p8 no repite la tabla «¿Garantiza V?»: la cita. Y su salvedad del corte
    es real en T±: con d=3 (y la iterativa) el valor con corte es 100·V."""
    texto = _texto()
    assert "@jue-c3-cmp-garantiza" in texto and "¿Garantiza" not in texto
    p7 = (CLASE_3 / "7_un_arbol_todos_los_algoritmos.md").read_text(encoding="utf-8")
    assert "{#jue-c3-cmp-garantiza " in p7
    assert j.corte_tpm(3)[1] == 100 * j.minimax_tpm()[1] != j.corte_tpm(1)[1]
    assert j.iterativa_tpm()[0][-1][3] == 100 * j.minimax_tpm()[1]


def test_8_el_ejercicio_ponle_nombre():
    texto = _texto()
    ej = _limpio(_bloque(texto, "jue-c3-cmp-ej-ponle-nombre"))
    # A 390 px, un paréntesis pegado a una fórmula se parte de ella (render r2).
    assert not re.search(r"\(\$|\$\)", _bloque(texto, "jue-c3-cmp-ej-ponle-nombre"))
    assert "di cuál de los tres es: V, valor con corte o \\bar u, y si es el V" in ej
    items = dict(re.findall(rf"(\d)\. ({_Q}), de", ej))
    items.update(dict(re.findall(rf"(\d)\. ({_Q}), el \\bar u", ej)))
    assert _q(items["1"]) == j.alfa_beta_tpm("al revés")[1]
    assert _q(items["2"]) == j.corte_tpm(1)[1]
    assert re.search(r"2\. \d+, del corte a d=(\d+)", ej)[1] == "1"
    filas, _ = j.iterativa_tpm()
    assert _q(items["3"]) == filas[-1][3]
    assert _q(items["4"]) == j.expectiminimax_tpm()[1]["R"]
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    assert _q(items["5"]) == F(u["S"][(1,)], u["N"][(1,)])
    assert int(re.search(r"tras (\d+) vueltas de UCT", ej)[1]) == j.VUELTAS_PAGINA_TPM
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-ponle-nombre"))
    m = re.search(rf"izq vale ({_Q})", resp)
    assert _q(m[1]) == j.minimax_tpm()[2]["izq"]
    m = re.search(rf"Con d=(\d+) todo lo que suma viene de finales: ({_Q})=100· ?V", resp)
    assert int(m[1]) == filas[-1][0] and _q(m[2]) == 100 * j.minimax_tpm()[1]
    m = re.search(rf"Sin dado, V=({_Q})", resp)
    assert _q(m[1]) == j.minimax_tpm()[1]
    m = re.search(rf"a la vuelta (\d+) ya es ({_Q})", resp)
    u2 = j.uct_tpm(1, int(m[1]), j.SEMILLA_TPM)
    assert _q(m[2]) == F(u2["S"][(1,)], u2["N"][(1,)])


def test_8_la_linea_9_es_la_de_la_pagina_del_reloj():
    """El renglón citado es, sin número ni comentario, la línea 9 del
    pseudocódigo de PROFUNDIZACIÓN-ITERATIVA en Jugar contra el reloj."""
    tres = _seccion_cruda(_texto(), 3)
    m = re.search(r"lo hace la línea (\d+) de\s+PROFUNDIZACIÓN-ITERATIVA, `([^`]+)`", tres)
    reloj = (CLASE_3 / "4_jugar_contra_el_reloj.md").read_text(encoding="utf-8")
    assert m[1] == "9" and "100" in m[2]
    assert re.search(rf"^ ?{m[1]}\s+{re.escape(m[2])}  # gana seguro$", reloj, re.M)
    assert "```" not in tres


def _seccion_cruda(texto, n):
    return re.search(rf"^## {n} ·.*?$(.*?)(?=^## )", texto, re.M | re.S).group(1)


def test_8_cuando_dejar_de_buscar_en_t_pm():
    tres = _seccion(_texto(), 3)
    m = re.search(r"en T± la EVAL más alta es (\d+), y en la posición de la clase nunca "
                  r"pasa de (\d+)", tres)
    assert int(m[1]) == max(j.EVAL_TPM.values()) < 100
    from test_juegos import _no_finales_4x4
    assert int(m[2]) == max(abs(j.evaluar_peones(t, 4)) for t, _ in _no_finales_4x4())
    m = re.search(rf"x tenía \\bar u=({_Q}) tras una simulación, y su \\mu era ({_Q})", tres)
    filas = j.filas_bandido("mejor_promedio", j.MUS_HILO, j.VUELTAS_MICRO, j.SEMILLA_ATORA)
    assert _q(m[1]) == filas[2]["u"]["x"] and _q(m[2]) == j.MUS_HILO["x"]
    # Lo que poda alfa-beta en el orden dado, y por qué ventana
    ids = j.ids_tpm()
    _, _, _, podados = j.alfa_beta_tpm("dado")
    m = re.search(r"alfa-beta ya se ahorra (\w+), (\w+) y (\w+)\.", tres)
    assert list(m.groups()) == [ids[c] for c in podados]
    cortes = {n: (w, a, b) for _, n, w, a, b in j.traza_decidir(j.ARBOL_TPM, poda=True)["cortes"]}
    m = re.search(rf"C2 ve c2a=({_Q}) cuando C ya asegura ({_Q}), y D ve d1=({_Q}) cuando la "
                  rf"raíz ya asegura ({_Q})", tres)
    assert (_q(m[1]), _q(m[2])) == (cortes["C2"][0], cortes["C2"][2])
    assert (_q(m[3]), _q(m[4])) == (cortes["D"][0], cortes["D"][1])
    # Con ix primero en I (primer hijo de la raíz), alfa-beta con la ventana
    # inicial (−∞, +∞) genera i1 igual; la regla del −1 no lo necesita. Y la
    # regla es abrir la ventana en los límites de U: con (−1, +1), alfa-beta
    # poda i1 tras ix.
    assert "Supón que ix fuera la primera hoja de I" in tres
    ix_primero = (tuple(reversed(j.ARBOL_TPM[0])),) + j.ARBOL_TPM[1:]
    _, _, _, podados_ix = j.alfa_beta_tpm("dado", arbol=ix_primero)
    assert (0, 1) not in podados_ix and j.nodo_en(ix_primero, (0, 1)) == 1   # i1, generado
    m = re.search(r"llega con la ventana inicial, \((-∞),\+(∞)\)\. Con esa ventana, alfa-beta "
                  r"generaría i1 igual\. La regla no: en I, MIN ve ix=-1", tres)
    assert m
    u = sorted({x for h in j.ARBOL_TPM for x in h if not isinstance(x, tuple)}
               | {x for h in j.ARBOL_TPM for c in h if isinstance(c, tuple) for x in c})
    # Brief r2 W3-5: abrir la ventana ahí INCLUYE la regla; alfa-beta además
    # poda por las cotas que hereda.
    m = re.search(rf"Abrir la ventana en los límites de U, \(({_Q}),({_Q})\), incluye la regla: "
                  r"con esa ventana, alfa-beta hace esta misma poda, y además poda por las "
                  r"cotas que hereda\.", tres)
    lo, hi = _q(m[1]), _q(m[2])
    assert (lo, hi) == (u[0], u[-1]) == (-1, 1)
    con_limites = j.alfa_beta_arbol(ix_primero, alfa=lo, beta=hi)
    assert (0, 1) in con_limites["podados"] and con_limites["valor"] == j.minimax_tpm()[1]
    # «además»: en T (hojas de 2 a 12), alfa-beta poda la segunda hoja de C2
    # tras ver 7, que no es el máximo, 12: esa poda viene de la cota heredada
    # (C ya tiene 5), no de la regla.
    en_t = j.alfa_beta_arbol(j.ARBOL_T)
    assert (1, 1, 1) in en_t["podados"]
    assert j.nodo_en(j.ARBOL_T, (1, 1, 0)) < max(max(h) if not isinstance(h[0], tuple) else
                                                 max(max(x) for x in h) for h in j.ARBOL_T)
    # La trampa: con α = −1 al inicio y «if w > α», si todas las jugadas
    # pierden, la raíz se queda sin jugada; empezando con la primera, no.
    assert ("Si \\alpha empieza en -1 y todas las jugadas pierden, ninguna lo supera, y la "
            "raíz se queda sin jugada. Por eso `mejor_jugada` empieza con la primera jugada, "
            "no con ninguna.") in _limpio(_seccion_cruda(_texto(), 3))
    pierde = ((1, -1), ((-1, -1), (1, -1)), (-1, 1, 1))     # c1a = -1: todo pierde
    assert set(j.minimax_tpm(pierde)[2].values()) == {-1}
    assert j.decidir_con_ventana_tpm(lo, hi, pierde)[0] is None
    assert j.decidir_con_ventana_tpm(lo, hi, pierde, primera=True)[0] == j.JUGADAS_RAIZ[0]
    assert j.decidir_con_ventana_tpm(float("-inf"), float("inf"), pierde)[0] is not None
    assert j.decidir_con_ventana_tpm(lo, hi)[0] == j.minimax_tpm()[0]
    # r3: en la raíz hay que salir cuando α llega a +1; si no, se siguen
    # buscando hijos con la ventana cerrada.
    m = re.search(rf"En la raíz falta una salida: cuando \\alpha llega a ({_Q}), se deja de "
                  rf"buscar\. Si no, se siguen buscando hijos con la ventana cerrada, "
                  rf"\(({_Q}),({_Q})\)", tres)
    assert _q(m[1]) == _q(m[2]) == _q(m[3]) == hi
    gana_izq = ((1, 1),) + j.ARBOL_TPM[1:]                  # I vale +1
    assert j.decidir_con_ventana_tpm(lo, hi, gana_izq) == ("izq", hi, ["izq"])
    assert j.decidir_con_ventana_tpm(float("-inf"), float("inf"), gana_izq)[2] == \
        list(j.JUGADAS_RAIZ)
    assert j.decidir_con_ventana_tpm(lo, hi)[2] == list(j.JUGADAS_RAIZ)


def test_8_el_ejercicio_puede_salir():
    texto = _texto()
    ej = _limpio(_bloque(texto, "jue-c3-cmp-ej-puede-salir"))
    from test_juegos import _no_finales_4x4
    cota = max(abs(j.evaluar_peones(t, 4)) for t, _ in _no_finales_4x4())
    assert int(re.search(r"devuelve (\d+), la EVAL más alta", ej)[1]) == cota
    m = re.search(rf"en D sale primero d1=({_Q})", ej)
    assert _q(m[1]) == j.ARBOL_TPM[2][0]
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-puede-salir"))
    assert re.findall(r"(\d)\. (Sí|No)\.", resp) == [("1", "No"), ("2", "No"), ("3", "Sí"),
                                                     ("4", "No")]
    # La objeción de la cota (fail-soft): un MIN que corta devuelve algo ≤ α; +1 no lo es.
    # Brief r2 W3-6: los dos casos. Si +1 supera a α, es valor; si α ya era
    # +1, puede ser cota (I con α = +1 devuelve +1 y vale −1), pero otra
    # jugada ya ganaba.
    assert ("3. Sí. Si +1 supera a \\alpha, ese hijo no cortó: si hubiera cortado, devolvería "
            "algo ≤\\alpha. Entonces +1 es su valor, sale de finales y es lo más que paga el "
            "juego. Si \\alpha ya era +1, este +1 puede ser solo una cota. Pero entonces una "
            "jugada anterior ya ganaba, y desde ella se podía dejar de buscar.") in resp
    como_cota = j.alfa_beta_arbol(j.ARBOL_TPM[0], es_max=False, alfa=1)
    assert como_cota["valor"] == 1 != j.minimax_arbol(j.ARBOL_TPM[0], False)
    assert int(re.search(r"2\. No\. (\d+) es una estimación", resp)[1]) == cota
    cuantas = re.search(r"el promedio de las (\w+) hojas", resp)[1]
    assert {"dos": 2, "tres": 3, "cuatro": 4}[cuantas] == len(j.ARBOL_TPM[2])


def test_8_lo_que_hay_que_llevarse():
    ll = _llevarse(_texto())
    jm, v, vs, _ = j.minimax_tpm()
    m = re.search(rf"en T±, V=({_Q}) por (\w+)\. Con un dado en D es otro juego, y V=({_Q}) "
                  rf"por (\w+)\.", ll)
    je, ve = j.expectiminimax_tpm()
    assert (_q(m[1]), m[2], _q(m[3]), m[4]) == (v, jm, ve["R"], je)
    m = re.search(rf"El corte a d=1 da ({_Q}) por (\w+), que vale ({_Q})\. Con d=3 llega a los "
                  rf"finales y da ({_Q})\. La quietud elige (\w+) con ({_Q})", ll)
    assert (m[2], int(m[1])) == j.corte_tpm(1)[:2] and _q(m[3]) == vs[m[2]]
    assert int(m[4]) == j.corte_tpm(3)[1]
    assert (m[5], int(m[6])) == j.quietud_tpm(1)[:2]
    assert "El \\bar u de Monte Carlo plano supone a todos al azar." in ll
    m = re.search(rf"Su límite en der es ({_Q}), y V\(der\)=({_Q})\. UCT elige por puntaje dentro "
                  rf"del árbol y al azar solo debajo; su \\bar u=({_Q}) en centro", ll)
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    assert (_q(m[1]), _q(m[2]), _q(m[3])) == (
        j.todos_al_azar_tpm()[1]["der"], vs["der"], F(u["S"][(1,)], u["N"][(1,)]))
    assert re.search(r"La línea (\d+) de la iterativa sale con (\d+)", ll).groups() == ("9", "100")
    m = re.search(rf"Un \\bar u=({_Q}) no basta: x valía ({_Q})", ll)
    assert (_q(m[1]), _q(m[2])) == (-1, j.MUS_HILO["x"])


def test_8_cierra_con_la_pregunta_y_continua_con_elegir():
    texto = _texto()
    cola = texto[texto.index("## Lo que hay que llevarse"):]
    assert "Todo esto supone cosas del juego. ¿Cuáles, y qué uso en cada caso?" in cola
    assert cola.rstrip().endswith("Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]].")
    assert "U_1" not in texto and "U_2" not in texto
