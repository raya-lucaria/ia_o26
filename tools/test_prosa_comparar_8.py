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
    m = re.search(rf"En der, los dos dan ({_Q}) por la misma cuenta", rem)
    assert _q(m[1]) == j.expectiminimax_tpm()[1]["D"] == j.todos_al_azar_tpm()[1]["der"]
    m = re.search(rf"donde V\(der\)=({_Q})", rem)
    assert _q(m[1]) == j.minimax_tpm()[2]["der"]


def test_8_el_ejercicio_del_rival_al_azar():
    texto = _texto()
    jr, vr = j.rival_al_azar_tpm()
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-rival-al-azar"))
    m = re.search(rf"1\. Centro vale ({_Q})\. MAX elige c1a en C1, que vale ({_Q}), y c2a en "
                  rf"C2, que vale ({_Q})\. El volado de MIN en C da \(({_Q})\+({_Q})\)/2=({_Q})",
                  resp)
    c1, c2 = (max(h) for h in j.ARBOL_TPM[1])
    assert _q(m[1]) == _q(m[6]) == vr["centro"] == (c1 + c2) / F(2)
    assert (_q(m[2]), _q(m[3]), _q(m[4]), _q(m[5])) == (c1, c2, c1, c2)
    m = re.search(rf"2\. (\w+), porque izq vale ({_Q}) y der ({_Q})\. Monte Carlo plano "
                  rf"elige (\w+)", resp)
    assert m[1].lower() == jr and (_q(m[2]), _q(m[3])) == (vr["izq"], vr["der"])
    assert m[4] == j.todos_al_azar_tpm()[0]
    m = re.search(rf"por eso centro baja a ({_Q})", resp)
    assert _q(m[1]) == j.todos_al_azar_tpm()[1]["centro"]


def test_8_la_tabla_de_como_busca_coincide_con_el_recuadro():
    """La columna «Hasta dónde mira» es la del recuadro «Lo que ya viste»
    (gen_resumen_juegos.ALGORITMOS), en el mismo orden: una sola fuente."""
    filas = _tabla(_texto(), "jue-c3-cmp-como-busca")
    assert [c.strip() for c in filas[0]] == [
        "Algoritmo", "Hasta dónde mira", "¿Genera todo?", "¿Quién tira dados?"]
    assert [(f[0], f[1]) for f in filas[1:]] == [(a["nombre"], a["mira"])
                                                 for a in resumen.ALGORITMOS]
    dados = {f[0]: f[3] for f in filas[1:]}
    assert dados["Expectiminimax"] == "El juego"
    assert [n for n, d in dados.items() if d.startswith("El algoritmo")] == [
        "Monte Carlo plano", "MCTS con UCT"]


def test_8_la_tabla_de_que_numero_da():
    filas = _tabla(_texto(), "jue-c3-cmp-que-numero")
    assert [c.strip() for c in filas[0]] == ["Algoritmo", "Número", "¿Es V?", "Qué entrega"]
    assert [f[0] for f in filas[1:]] == [a["nombre"] for a in resumen.ALGORITMOS]
    es_v = {f[0]: _c(f[2]).startswith("Sí") for f in filas[1:]}
    assert [n for n, s in es_v.items() if s] == ["Minimax", "Expectiminimax", "Alfa-beta"]
    entrega = {f[0]: _c(f[3]) for f in filas[1:]}
    assert entrega["MCTS con UCT"] == "La jugada más simulada"


def test_8_el_ejercicio_ponle_nombre():
    texto = _texto()
    ej = _limpio(_bloque(texto, "jue-c3-cmp-ej-ponle-nombre"))
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
    """El renglón citado es, tal cual, la línea 9 del pseudocódigo de
    PROFUNDIZACIÓN-ITERATIVA en Jugar contra el reloj."""
    texto = _texto()
    citado = re.search(r"```text\n(.*?)\n```", _seccion_cruda(texto, 3), re.S)[1]
    reloj = (CLASE_3 / "4_jugar_contra_el_reloj.md").read_text(encoding="utf-8")
    assert citado in reloj.splitlines()
    assert re.match(r"\s*9\s", citado)
    assert "lo hace la línea 9 de" in _limpio(_seccion_cruda(texto, 3))


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
    # Al revés poda solo i1; con ix primero, alfa-beta genera i1 igual
    _, _, n_reves, podados_reves = j.alfa_beta_tpm("al revés")
    m = re.search(r"Con los hijos al revés, alfa-beta poda (\w+) y genera (\d+) nodos", tres)
    assert [m[1]] == [ids[c] for c in podados_reves] and int(m[2]) == n_reves
    assert j.alfa_beta_tpm("dado")[0:2] == j.alfa_beta_tpm("al revés")[0:2]
    ix_primero = (tuple(reversed(j.ARBOL_TPM[0])),) + j.ARBOL_TPM[1:]
    _, _, _, podados_ix = j.alfa_beta_tpm("dado", arbol=ix_primero)
    assert (0, 1) not in podados_ix and j.nodo_en(ix_primero, (0, 1)) == 1   # i1, generado
    assert "Si ix fuera su primera hoja, alfa-beta generaría i1 igual" in tres


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
    m = re.search(rf"Su límite en der es ({_Q}), y V\(der\)=({_Q})\. El \\bar u=({_Q}) de UCT", ll)
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
