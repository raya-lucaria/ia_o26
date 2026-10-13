"""Cada cifra de 7.3.7, «Un árbol, todos los algoritmos», contra tools/juegos.py.

La página corre todos los algoritmos de la unidad sobre T± (ARBOL_TPM). Cada
número que cita —valores, jugadas, nodos, repartos por semilla— se lee del
texto y se compara con la función que lo calcula; ninguno se copia aquí.
"""
import re
from fractions import Fraction as F

import juegos as j
from test_juegos import (CLASE_3, _bloque, _c, _llevarse, _limpio, _respuesta,
                         _seccion, _tabla, _alt)

P7 = "7_un_arbol_todos_los_algoritmos.md"
_FR = r"[+-]?\d+(?:/\d+)?"


def _texto():
    return (CLASE_3 / P7).read_text(encoding="utf-8")


def _fr(s):
    return F(s.replace(" ", "").lstrip("+"))


def _hojas():
    """{nombre de hoja: U}: i1, ix, c1a, …, d3."""
    return {nombre: j.nodo_en(j.ARBOL_TPM, camino)
            for camino, nombre in j.nombres_hojas_tpm().items()}


def _podadas(orden):
    ids = j.ids_tpm()
    return [ids[c] for c in j.alfa_beta_tpm(orden)[3]]


def test_comparar_7_la_pagina_y_sus_enlaces():
    texto = _texto()
    assert re.search(r"^id: un-arbol-todos-los-algoritmos$", texto, re.M)
    assert "(../_assets/un_arbol_todos.html)" in texto
    assert "(../_assets/jue-t-pm-arbol.svg)" in texto
    assert texto.rstrip().endswith(
        "Continúa con [[que-numero-da-cada-uno|Qué número da cada uno]].")
    assert "Cada algoritmo dio un número distinto. ¿Qué es cada número?" in texto


def test_comparar_7_el_arbol_t_pm():
    """§1: un solo empate (c1a), la captura ix, la EVAL, los tres hijos de D
    y por qué: con dos, ningún dado cambia la jugada."""
    texto = _texto()
    uno = _seccion(texto, 1)
    hojas = _hojas()
    empates = [n for n, u in hojas.items() if u == 0]
    m = re.search(r"Hay un solo empate, (\w+)\.", uno)
    assert [m[1]] == empates
    capturas = [j.nombres_hojas_tpm()[c] for c in j.CAPTURAS_TPM]
    assert re.search(r"Una captura\. (\w+), la segunda jugada de MIN en I", uno)[1] \
        == capturas[0] == "ix"
    m = re.search(r"I (\d+), C (\d+), D (\d+), C1 (\d+) y C2 (\d+)\.", uno)
    assert dict(zip(["I", "C", "D", "C1", "C2"], map(int, m.groups()))) == j.EVAL_TPM
    assert len(j.ARBOL_TPM[2]) == 3 and re.search(r"D con tres hijos, d1, d2 y d3", uno)
    assert j.dados_que_cambian_la_jugada_forma_t(2) == 0
    m = re.search(rf"Con tres, \(({_FR})\+({_FR})\+({_FR})\)/3=({_FR})\.", uno)
    assert [_fr(x) for x in m.groups()[:3]] == list(j.ARBOL_TPM[2])
    assert _fr(m[4]) == j.expectiminimax_tpm()[1]["D"]
    alt = _alt(texto, "jue-c3-cmp-arbol")
    assert {n: _fr(u) for n, u in re.findall(rf"\b([icd]\w*) = ({_FR})", alt)} == hojas
    assert {n: int(v) for n, v in re.findall(r"\b(I|C|D|C1|C2) = (\d+)", alt)} == j.EVAL_TPM


def test_comparar_7_minimax_y_alfa_beta():
    """§2: I, C, D; centro con V = 0 y 15 nodos; alfa-beta 12 (poda c2b, d2,
    d3) y 14 al revés (poda i1); el micro de la poda."""
    texto = _texto()
    dos = _seccion(texto, 2)
    jugada, v, hijos, nodos = j.minimax_tpm()
    leidos = {n: _fr(x) for n, x in re.findall(rf"\b([ICD]) vale ({_FR})", dos)}
    assert leidos == {"I": hijos["izq"], "C": hijos["centro"], "D": hijos["der"]}
    m = re.search(rf"Minimax juega (\w+), con V=({_FR}), y genera los (\d+) nodos", dos)
    assert (m[1], _fr(m[2]), int(m[3])) == (jugada, v, nodos)
    m = re.search(r"En el orden dado, (\d+)\. Poda (\w+):.*?Poda (\w+) y (\w+):", dos)
    _, v_d, g_d, _ = j.alfa_beta_tpm("dado")
    assert (int(m[1]), [m[2], m[3], m[4]]) == (g_d, _podadas("dado")) and v_d == v
    m = re.search(r"Con todos los hijos al revés, (\d+)\. Solo poda (\w+):", dos)
    _, v_r, g_r, _ = j.alfa_beta_tpm("al revés")
    assert (int(m[1]), [m[2]]) == (g_r, _podadas("al revés")) and v_r == v
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-poda"))
    _, valores = j.expectiminimax_tpm(())
    assert _fr(re.search(rf"C1 vale ({_FR})", resp)[1]) == valores["C1"]


def test_comparar_7_el_dado_en_d():
    """§3: der con 1/3 y 15 nodos; el micro con d3 = −1: D = −1/3, centro."""
    texto = _texto()
    tres = _seccion(texto, 3)
    jugada, valores = j.expectiminimax_tpm()
    m = re.search(rf"\(({_FR})\+({_FR})\+({_FR})\)/3=({_FR})", tres)
    assert [_fr(x) for x in m.groups()[:3]] == list(j.ARBOL_TPM[2])
    assert _fr(m[4]) == valores["D"]
    m = re.search(rf"Expectiminimax juega (\w+), con valor ({_FR}), y genera los (\d+)", tres)
    assert (m[1], _fr(m[2]), int(m[3])) == (jugada, valores["R"], j.contar_nodos(j.ARBOL_TPM))
    otro = j.ARBOL_TPM[:2] + ((-1, 1, -1),)
    j2, v2 = j.expectiminimax_tpm(arbol=otro)
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-dado"))
    assert _fr(re.search(rf"D vale \(.*?\)/3=({_FR})", resp)[1]) == v2["D"]
    assert re.search(r"2\. (\w+), con 0", resp)[1].lower() == j2


def test_comparar_7_corte_quietud_e_iterativa():
    """§4: d = 1, 2, 3 (jugada, valor, nodos), la quietud (centro, 20, 5) y la
    iterativa (izq 4, centro 9, centro 12; 25); el micro del reloj (10, 13)."""
    texto = _texto()
    cuatro = _seccion(texto, 4)
    j1, v1, ws1, g1 = j.corte_tpm(1)
    m = re.search(r"EVAL de I, C y D: (\d+), (\d+) y (\d+)\. El corte a d=1 juega (\w+), con "
                  r"(\d+), y genera (\d+) nodos", cuatro)
    assert [int(x) for x in m.groups()[:3]] == list(ws1.values())
    assert (m[4], int(m[5]), int(m[6])) == (j1, v1, g1)
    assert int(re.search(r"I vale de verdad (-\d+)", cuatro)[1]) == j.corte_tpm(3)[2]["izq"]
    j2, v2, ws2, g2 = j.corte_tpm(2)
    m = re.search(r"d=2 ya ve los finales de I y D, los dos en (-\d+)\. En C corta en C1 y "
                  r"C2, con (\d+) y (\d+)\. Juega (\w+), con (\d+), y genera (\d+) nodos", cuatro)
    assert int(m[1]) == ws2["izq"] == ws2["der"]
    assert (int(m[2]), int(m[3])) == (j.EVAL_TPM["C1"], j.EVAL_TPM["C2"])
    assert (m[4], int(m[5]), int(m[6])) == (j2, v2, g2)
    j3, v3, _, g3 = j.corte_tpm(3)
    m = re.search(r"d=3 llega a todos los finales\. Juega (\w+), con (\d+):.*?mismos (\d+) "
                  r"nodos", cuatro)
    assert (m[1], int(m[2]), int(m[3])) == (j3, v3, g3) and v3 == 100 * j.minimax_tpm()[1]
    jq, vq, wq, gq, _ = j.quietud_tpm(1)
    m = re.search(r"quedarse con (\d+) o capturar, que da (-\d+)", cuatro)
    assert int(m[1]) == j.EVAL_TPM["I"] and int(m[2]) == wq["izq"]
    m = re.search(r"se quedan en (\d+) y (\d+)\.", cuatro)
    assert (int(m[1]), int(m[2])) == (wq["centro"], wq["der"])
    m = re.search(r"La quietud juega (\w+), con (\d+), y genera (\d+) nodos: los (\d+) del "
                  r"corte más (\w+)", cuatro)
    assert (m[1], int(m[2]), int(m[3])) == (jq, vq, gq) and int(m[4]) == g1
    filas, total = j.iterativa_tpm()
    leidas = re.findall(r"d=(\d): (\w+), con (\d+)", cuatro)
    assert [(int(d), a, int(g)) for d, a, g in leidas] == [(d, a, g) for d, _, a, _, g in filas]
    assert int(re.search(r"Son (\d+) nodos en total, más que los (\d+)", cuatro)[1]) == total
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-reloj"))
    m = re.search(r"1\. (\w+), con (\d+): la de d=(\d)", resp)
    assert (m[1].lower(), int(m[2]), int(m[3])) == (filas[1][2], filas[1][3], filas[1][0])
    m = re.search(r"(\d+)\+(\d+)=(\d+) nodos", resp)
    assert [int(x) for x in m.groups()] == [filas[0][4], filas[1][4], filas[0][4] + filas[1][4]]


def test_comparar_7_monte_carlo_plano():
    """§5: μ con todos al azar (0, −1/4, 1/3); la trampa (1/2); la corrida
    de la semilla 0; el reparto en 1000 semillas con su desempate."""
    texto = _texto()
    cinco = _seccion(texto, 5)
    jl, mu = j.todos_al_azar_tpm()
    m = re.search(rf"izq: .*?μ=({_FR})\. - centro: C1 al azar da \(.*?\)/2=({_FR}) y C2, "
                  rf"\(.*?\)/2=({_FR})\. Con C también al azar, μ=({_FR})\. - der: "
                  rf"μ=\(.*?\)/3=({_FR})\.", cinco.replace("\\mu", "μ"))
    _, todos = j.expectiminimax_tpm(("I", "C", "D", "C1", "C2"))
    assert _fr(m[1]) == mu["izq"] and _fr(m[4]) == mu["centro"] and _fr(m[5]) == mu["der"]
    assert (_fr(m[2]), _fr(m[3])) == (todos["C1"], todos["C2"])
    assert re.search(r"Monte Carlo plano elige (\w+), que pierde", cinco)[1] == jl
    assert j.minimax_tpm()[2][jl] == -1
    jr, rival = j.rival_al_azar_tpm()
    m = re.search(rf"C valdría ({_FR}) y ganaría (\w+)", cinco)
    assert (_fr(m[1]), m[2]) == (rival["centro"], jr)
    k = j.SIMS_MC_TPM[0]
    jp, sumas = j.mc_plano_tpm(k, j.SEMILLA_TPM)
    m = re.search(rf"Con (\d+) simulaciones por jugada y la semilla (\d+), las sumas de U son "
                  rf"({_FR}), ({_FR}) y ({_FR})\. Los promedios, ({_FR}), ({_FR}) y ({_FR}): "
                  rf"entrega (\w+)", cinco)
    assert (int(m[1]), int(m[2])) == (k, j.SEMILLA_TPM)
    assert [_fr(x) for x in m.groups()[2:5]] == list(sumas.values())
    assert [_fr(x) for x in m.groups()[5:8]] == [F(s, k) for s in sumas.values()]
    assert m[9] == jp
    assert int(re.search(r"con (\d+) semillas distintas", cinco)[1]) == j.SEMILLAS_MC_TPM
    filas = _tabla(texto, "jue-c3-cmp-reparto-mc")
    assert [_c(x) for x in filas[0][1:4]] == list(j.JUGADAS_RAIZ)
    leido = {int(_c(f[0])): [int(_c(x)) for x in f[1:]] for f in filas[1:]}
    esperado = {}
    for kk in j.SIMS_MC_TPM:
        cuenta, empates = j.reparto_mc_plano_tpm(kk, j.SEMILLAS_MC_TPM)
        esperado[kk] = [cuenta[a] for a in j.JUGADAS_RAIZ] + [empates]
    assert leido == esperado
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-mas-sims"))
    m = re.search(rf"^(\w+): .*?der tiene el mayor, ({_FR})\..*?centro vale ({_FR})", resp)
    assert (m[1].lower(), _fr(m[2]), _fr(m[3])) == (jl, mu["der"], rival["centro"])


def test_comparar_7_uct():
    """§6: la corrida de la semilla 0 (izq 1–3, centro 4–7, der 8–17,
    centro desde la 18; 7 a 7; 26, 9, 5 y ū = 0) y el reparto por semillas."""
    texto = _texto()
    seis = _seccion(texto, 6)
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    mas = u["mas_simulada"]
    tramos = re.findall(r"- (\w+), (?:en las vueltas (\d+) a (\d+)|de la (\d+) a la (\d+)|"
                        r"desde la (\d+))", seis)
    reconstruido = []
    for jug, a1, b1, a2, b2, desde in tramos:
        ini, fin = (int(a1 or a2 or desde), int(b1 or b2 or len(mas)))
        reconstruido += [jug] * (fin - ini + 1)
        assert len(reconstruido) == fin
    assert reconstruido == mas
    desde = int(tramos[-1][5])
    assert desde == j.vuelta_desde_la_que_tpm(1, j.SEMILLA_TPM)
    m = re.search(r"En la (\d+), centro y der empatan (\d+) a (\d+)", seis)
    n18 = j.uct_tpm(1, int(m[1]), j.SEMILLA_TPM)["N"]
    assert int(m[1]) == desde and (int(m[2]), int(m[3])) == (n18[(1,)], n18[(2,)])
    m = re.search(r"Tras (\d+) vueltas, centro lleva (\d+) simulaciones, der (\d+) e izq (\d+)\. "
                  rf"UCT entrega (\w+), con \\bar u=({_FR})", seis)
    assert int(m[1]) == j.VUELTAS_PAGINA_TPM
    assert [int(x) for x in m.groups()[1:4]] == [u["N"][(1,)], u["N"][(2,)], u["N"][(0,)]]
    assert m[5] == mas[-1] and _fr(m[6]) == F(u["S"][(1,)], u["N"][(1,)])
    assert int(re.search(r"es el promedio de (\d+) partidas", seis)[1]) == u["N"][(1,)]
    m = re.search(r"con (\d+) semillas, de (\d+) vueltas cada una", seis)
    assert (int(m[1]), int(m[2])) == (j.SEMILLAS_UCT_TPM, j.VUELTAS_UCT_TPM)
    r = j.reparto_uct_tpm(1)
    m = re.search(r"con c=1, las (\d+) terminan en centro\. La vuelta va de (\d+) a (\d+)\. La "
                  r"mediana es (\d+), como la semilla 0; el 10 % llega en la (\d+) o antes, y el "
                  r"90 %, en la (\d+) o antes", seis)
    assert int(m[1]) == j.SEMILLAS_UCT_TPM - r["nunca"] and r["nunca"] == 0
    assert [int(x) for x in m.groups()[1:]] == [r["minimo"], r["maximo"], r["mediana"],
                                                r["p10"], r["p90"]]
    assert r["mediana"] == desde
    r2 = j.reparto_uct_tpm(j.C_TEORIA)
    m = re.search(r"con c=2\\sqrt2, .*?también llegan todas, más tarde: la mediana es (\d+)", seis)
    assert r2["nunca"] == 0 and int(m[1]) == r2["mediana"] > r["mediana"]
    resp = _limpio(_respuesta(texto, "jue-c3-cmp-ej-uct"))
    vuelta = int(re.search(r"al terminar la vuelta (\d+)",
                           _limpio(_bloque(texto, "jue-c3-cmp-ej-uct")))[1])
    m = re.search(r"1\. (\w+): es la más simulada de la vuelta (\d+) a la (\d+)", resp)
    assert m[1].lower() == mas[vuelta - 1]
    assert set(mas[int(m[2]) - 1:int(m[3])]) == {mas[vuelta - 1]}
    assert vuelta < len(j.ids_tpm()) - 1    # «con 12, el árbol todavía no cubre T±»


def _valor(celda):
    return _fr(_c(celda))


def test_comparar_7_la_tabla_de_resultados():
    """@jue-c3-cmp-resultados = tabla_t_pm(), fila por fila."""
    texto = _texto()
    filas = _tabla(texto, "jue-c3-cmp-resultados")
    assert [_c(x) for x in filas[0]] == ["Algoritmo", "Jugada", "Valor", "Nodos", "¿Exacto?"]
    esperadas = j.tabla_t_pm()
    assert len(filas) - 1 == len(esperadas)
    for f, e in zip(filas[1:], esperadas):
        assert _c(f[1]) == e["jugada"], f
        assert _valor(f[2]) == e["valor"], f
        assert int(_c(f[3])) == e["nodos"], f
        exacto = "otro juego" if e["tipo"] == "V con dado" else ("sí" if e["exacto"] else "no")
        assert _c(f[4]) == exacto, f
    aciertan = sum(e["jugada"] == j.minimax_tpm()[0] for e in esperadas)
    m = re.search(r"Tres filas no dicen centro.*?Los otros (\w+) aciertan",
                  _seccion(texto + "\n## ", 7))
    assert len(esperadas) - aciertan == 3 and m[1] == {8: "ocho"}[aciertan]


def test_comparar_7_lo_que_hay_que_llevarse():
    """Las cifras del cierre, contra las mismas funciones."""
    ll = _llevarse(_texto())
    jm, v, _, n = j.minimax_tpm()
    m = re.search(rf"Minimax juega (\w+) con V=({_FR}) y (\d+) nodos", ll)
    assert (m[1], _fr(m[2]), int(m[3])) == (jm, v, n)
    m = re.search(r"(\d+) nodos en el orden dado, (\d+) al revés", ll)
    assert (int(m[1]), int(m[2])) == (j.alfa_beta_tpm("dado")[2], j.alfa_beta_tpm("al revés")[2])
    je, ve = j.expectiminimax_tpm()
    m = re.search(rf"expectiminimax juega (\w+) por ({_FR})", ll)
    assert (m[1], _fr(m[2])) == (je, ve["R"])
    j1, v1, _, _ = j.corte_tpm(1)
    m = re.search(r"(\w+) con (\d+), sin ver ix\. La quietud juega (\w+) con (\d+) nodos, pero "
                  r"su (\d+) no es el (\d+)", ll)
    jq, vq, _, gq, _ = j.quietud_tpm(1)
    assert (m[1], int(m[2]), m[3], int(m[4]), int(m[5]), int(m[6])) == (j1, v1, jq, gq, vq, v)
    filas, total = j.iterativa_tpm()
    m = re.search(r"La iterativa deja (\w+), (\w+) y (\w+), con (\d+), (\d+) y (\d+) nodos: (\d+)",
                  ll)
    assert list(m.groups()[:3]) == [f[2] for f in filas]
    assert [int(x) for x in m.groups()[3:]] == [f[4] for f in filas] + [total]
    jl, mu = j.todos_al_azar_tpm()
    m = re.search(rf"(\w+) promedia ({_FR}), izq ({_FR}) y centro ({_FR})", ll)
    assert (m[1], _fr(m[2]), _fr(m[3]), _fr(m[4])) == (jl, mu["der"], mu["izq"], mu["centro"])
    m = re.search(r"Con (\d+) simulaciones, der en (\d+) de (\d+)", ll)
    assert int(m[2]) == j.reparto_mc_plano_tpm(int(m[1]), int(m[3]))[0]["der"]
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    m = re.search(r"desde la vuelta (\d+); tras (\d+), con (\d+) simulaciones\. En (\d+) semillas "
                  r"con c=1, todas, con mediana (\d+)", ll)
    r = j.reparto_uct_tpm(1)
    assert [int(x) for x in m.groups()] == [
        j.vuelta_desde_la_que_tpm(1, j.SEMILLA_TPM), j.VUELTAS_PAGINA_TPM, u["N"][(1,)],
        j.SEMILLAS_UCT_TPM, r["mediana"]] and r["nunca"] == 0
