"""Los pasos de pasos_interactivos coinciden con las trazas de las paginas.

pasos_interactivos(modo, variante) es la unica fuente de los pasos que
muestran el cuaderno de la unidad 7 y la traza interactiva del arbol T. Un
paso es una fila de la traza tal como la escribe la pagina, asi que aqui se
lee cada tabla de traza del .md y se compara fila por fila: linea, pila, v,
w (y quien lo devuelve), la ventana (α, β), si corta, y mejor_jugada.

Las tablas se localizan por su id de directiva (::: table {#...}) cuando lo
tienen, o por su forma (la primera corrida de filas 1, 2, 3... sin «?»),
nunca por numero de renglon: las paginas se reordenan.
"""
import json
import re
from fractions import Fraction
from pathlib import Path

import pytest

import juegos as j

UNIDAD = Path(__file__).resolve().parent.parent / "course/7_juegos"
MODOS = [("minimax", None), ("azar", None), ("alfa-beta", "T1"), ("alfa-beta", "T"),
         ("corte", 1), ("corte", 2), ("corte", 3), ("iterativa", None)]


def texto(modo):
    return (UNIDAD / j.PAGINA_MODO[modo]).read_text(encoding="utf-8")


def limpia(celda):
    """Una celda de la pagina en texto plano y sin espacios."""
    c = celda.replace("$", "").replace("**", "")
    c = re.sub(r"\\(?:textit|textbf|mathbf|text)\{([^{}]*)\}", r"\1", c)
    c = re.sub(r"\\(?:textit|textbf|mathbf|text)\{([^{}]*)\}", r"\1", c)
    c = (c.replace("\\infty", "∞").replace("\\le", "≤").replace("\\ge", "≥")
          .replace("\\alpha", "α").replace("\\beta", "β"))
    c = c.replace("-∞", "−∞").replace(" ", "")
    return c


FILA = re.compile(r"^\|\s*(\d+)(\s*✗)?\s*\|")


def corridas(lineas):
    """Las corridas de filas de traza numeradas 1, 2, 3... seguidas (aunque
    vayan en varias tablas). Cada fila: (n, tachada, [celdas])."""
    res, actual = [], None
    for linea in lineas:
        if linea.startswith("## "):
            actual = None
            continue
        m = FILA.match(linea)
        if not m:
            continue
        n = int(m.group(1))
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        fila = (n, bool(m.group(2)), celdas[1:])
        if n == 1:
            actual = [fila]
            res.append(actual)
        elif actual is not None and n == actual[-1][0] + 1:
            actual.append(fila)
        else:
            actual = None
    return res


def corrida_tras_id(modo, id_):
    t = texto(modo)
    i = t.index("{#" + id_)
    return corridas(t[i:].split("\n"))[0]


def corridas_completas(modo):
    """Las corridas de la pagina sin «?» (las de los ejercicios por llenar)."""
    return [c for c in corridas(texto(modo).split("\n"))
            if not any("?" in x for _, _, cs in c for x in cs)]


def tabla_de(modo, variante):
    if modo == "minimax":
        return [c for c in corridas_completas(modo) if len(c) == 20
                and limpia(c[1][2][0]) == "16·R›I"][0]
    if modo == "azar":
        return corrida_tras_id(modo, "jue-c2-t-traza-azar")
    if modo == "corte":
        return corrida_tras_id(modo, "jue-c3-t-traza-d2") if variante == 2 else None
    if modo == "alfa-beta":
        largo = {"T1": 10, "T": 20}[variante]
        return [c for c in corridas_completas(modo) if len(c) == largo
                and limpia(c[1][2][0]) == "18·R›I"][0]
    return None


def separa_w(celda):
    """«3 (I)» -> ("3", "I"); «12» -> ("12", None)."""
    m = re.match(r"^(.*?)\((.*)\)$", celda)
    return (m.group(1), m.group(2)) if m else (celda, None)


def nombre(r, id_):
    return {x["id"]: x["nombre"] for x in r["arbol"]["nodos"]}[id_]


@pytest.mark.parametrize("modo,variante", [m for m in MODOS if tabla_de(*m)],
                         ids=lambda x: str(x))
def test_cada_paso_es_una_fila_de_la_tabla_de_la_pagina(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    tabla = tabla_de(modo, variante)
    pasos = r["pasos"]
    assert len(pasos) == len(tabla), (modo, variante)
    poda = modo == "alfa-beta"
    alfa_previo = "−∞"
    tipo = {x["id"]: x["tipo"] for x in r["arbol"]["nodos"]}
    for (n, tachada, cs), p in zip(tabla, pasos):
        assert p["n"] == n
        donde = f"{j.PAGINA_MODO[modo]} fila {n}"
        if poda:
            linea_pila, ventana, v, w, corta, jugada = map(limpia, cs)
        else:
            linea_pila, v, w, jugada = map(limpia, cs)
        if tachada:
            assert p["evento"] == "podado" and p["linea"] == "", donde
            assert linea_pila == "›".join(p["pila"]), donde
            assert w == p["w"] == nombre(r, p["nodo"]), donde
            continue
        linea, pila = linea_pila.split("·")
        assert (linea, pila) == (p["linea"], "›".join(p["pila"])), donde
        assert v == p["v"], donde
        valor_w, quien = separa_w(w)
        assert valor_w == p["w"], donde
        if quien:
            assert quien == nombre(r, p["hijo"]), donde
        elif p["w"]:
            assert p["hijo"] and nombre(r, p["hijo"]) == p["w"], donde
        assert jugada == ("—" if p["mejor_jugada"] == "ninguna" else p["mejor_jugada"]), donde
        if poda:
            assert ventana == f"({p['alfa']},{p['beta']})", donde
            if p["evento"] == "regresa":
                es_max = tipo[p["nodo"]] == "MAX"
                signo, borde = ("≥", p["beta"]) if es_max else ("≤", p["alfa"])
                si = "sí" if p["corta"] else "no"
                assert corta == f"{p['v']}{signo}{borde}{si}", donde
            elif p["evento"] == "raiz":
                si = "sí" if p["mejora"] else "no"
                assert corta == f"{p['w']}>{alfa_previo}{si}", donde
            else:
                assert corta == "", donde
            if p["nodo"] == "R":
                alfa_previo = p["alfa"]


def test_los_hechos_del_contrato():
    res = {m: j.pasos_interactivos(*m)["resultado"] for m in MODOS}
    corto = {m: (r["jugada"], r["valor"], r["generados"], r["total"]) for m, r in res.items()}
    assert corto == {
        ("minimax", None): ("centro", "5", 14, 14),
        ("azar", None): ("der", "7", 14, 14),
        ("alfa-beta", "T1"): ("izq", "3", 6, 7),
        ("alfa-beta", "T"): ("centro", "5", 12, 14),
        ("corte", 1): ("der", "7", 4, 14),
        ("corte", 2): ("centro", "6", 10, 14),
        ("corte", 3): ("centro", "5", 14, 14),
        ("iterativa", None): ("centro", "5", 25, 42),
    }
    por_d = res[("iterativa", None)]["por_d"]
    assert [(x["d"], x["orden"], x["jugada"], x["generados"]) for x in por_d] == [
        (1, ["izq", "centro", "der"], "der", 4),
        (2, ["der", "izq", "centro"], "centro", 10),
        (3, ["centro", "izq", "der"], "centro", 11)]
    # Los valores de I, C y D con azar: 9/2, 13/2 y 7.
    azar = j.pasos_interactivos("azar")
    assert [(p["hijo"], p["w"]) for p in azar["pasos"] if p["evento"] == "raiz"] == [
        ("I", "9/2"), ("C", "13/2"), ("D", "7")]
    # Por omision: alfa-beta en T, corte con d = 2.
    assert j.pasos_interactivos("alfa-beta")["variante"] == "T"
    assert j.pasos_interactivos("corte")["variante"] == 2
    with pytest.raises(ValueError):
        j.pasos_interactivos("corte", 4)
    with pytest.raises(ValueError):
        j.pasos_interactivos("nada")


def test_corte_y_reloj_coinciden_con_las_tablas_resumen():
    """Sin tabla fila por fila para d = 1 y d = 3 ni para la iterativa: se
    comparan con las tablas que resumen cada busqueda."""
    t = texto("corte")
    resumen = t[t.index("{#jue-c3-t-por-profundidad"):].split(":::")[0]
    filas = [list(map(limpia, f.strip().strip("|").split("|")))
             for f in resumen.split("\n") if re.match(r"^\|\s*\d", f)]
    for d, icd, juega, nodos in filas:
        r = j.pasos_interactivos("corte", int(d))
        ws = "·".join(p["w"] for p in r["pasos"] if p["evento"] == "raiz")
        assert (ws, juega, int(nodos)) == (icd, r["resultado"]["jugada"],
                                          r["resultado"]["generados"])
    t = texto("iterativa")
    resumen = t[t.index("{#jue-c3-t-iterativa"):].split(":::")[0]
    filas = [list(map(limpia, f.strip().strip("|").split("|")))
             for f in resumen.split("\n") if re.match(r"^\|\s*\d", f)]
    r = j.pasos_interactivos("iterativa")
    for (d, orden_w, lista), x in zip(filas, r["resultado"]["por_d"], strict=True):
        assert int(d) == x["d"]
        ws = "·".join(f"{w['hijo']}{'≤' if w['cota'] else ''}{w['w']}" for w in x["w"])
        assert (orden_w, lista) == (ws, x["jugada"])


def test_la_iterativa_va_seguida_y_numerada_con_la_pagina_del_reloj():
    r = j.pasos_interactivos("iterativa")
    pasos = r["pasos"]
    assert [p["d"] for p in pasos] == sorted(p["d"] for p in pasos)
    assert pasos[0]["linea"] == "2–3" and pasos[-1]["linea"] == "4, 13"
    assert [p["linea"] for p in pasos if p["evento"] == "inicio"] == ["5"] * 3
    assert [p["linea"] for p in pasos if p["evento"] == "fin"] == ["11–12"] * 3
    assert {p["linea"] for p in pasos if p["evento"] == "raiz"} == {"7–10"}
    cortes = [(p["corta"], p["pila"][-1]) for p in pasos if p["evento"] == "regresa" and p["corta"]]
    assert cortes == [("beta", "C2"), ("alfa", "I"), ("alfa", "D")]
    assert {p["linea"] for p in pasos if p["evento"] == "regresa" and p["corta"]} == {
        "20–22", "28–30"}
    # «jugada», la lista, cambia solo al terminar cada busqueda.
    listas = [p["jugada"] for p in pasos]
    assert listas[0] == "izq" and listas[-1] == "centro"
    assert [p["jugada"] for p in pasos if p["evento"] == "fin"] == ["der", "centro", "centro"]


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_el_pseudo_es_el_bloque_de_la_pagina(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    bloques = re.findall(r"^```text\n(.*?)^```$", texto(modo), re.S | re.M)
    funcion = j.FUNCION_MODO[modo]
    bloque = [b for b in bloques if re.search(rf"^\s*1 function {funcion}\(", b, re.M)]
    assert len(bloque) == 1
    assert "\n".join(r["pseudo"]) + "\n" == bloque[0]
    assert len(r["renglones"]) == len(r["pseudo"])
    # cada numero de linea aparece una vez, en orden, y nada se salta
    numeros = [n for n in r["renglones"] if n is not None]
    assert sorted(set(numeros)) == list(range(1, max(numeros) + 1))


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_cada_linea_resaltada_existe_en_el_pseudo(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    existen = {int(m.group(1)) for x in r["pseudo"] if (m := re.match(r"^\s*(\d+) ", x))}
    for p in r["pasos"]:
        assert set(p["lineas"]) <= existen, (p["n"], p["lineas"])
        assert p["lineas"] == j.lineas_de(p["linea"])
        assert bool(p["lineas"]) == (p["evento"] != "podado")


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_es_json_y_determinista(modo, variante):
    a = json.dumps(j.pasos_interactivos(modo, variante), ensure_ascii=False)
    b = json.dumps(j.pasos_interactivos(modo, variante), ensure_ascii=False)
    assert a == b
    assert json.loads(a)["modo"] == modo


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_cada_frase_es_una_oracion_corta(modo, variante):
    for p in j.pasos_interactivos(modo, variante)["pasos"]:
        f = p["frase"]
        assert 0 < len(f) <= 90, (p["n"], len(f), f)
        assert f[0].isupper() and f.endswith("."), f
        assert "inf" not in f and "None" not in f, f


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_el_estado_de_cada_nodo_es_coherente(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    ids = [x["id"] for x in r["arbol"]["nodos"]]
    validos = {"pormirar", "pila", "devuelto", "evaluado", "podado"}
    for p in r["pasos"]:
        e = p["estado"]
        assert list(e) == ids
        assert {x["estado"] for x in e.values()} <= validos
        if p["evento"] not in ("fin", "entrega"):
            assert [k for k in ids if e[k]["estado"] == "pila"] == p["pila"], p["n"]
        hechos = sum(x["estado"] in ("pila", "devuelto", "evaluado") for x in e.values())
        assert hechos == p["generados"], p["n"]
    final = r["pasos"][-1]["estado"]
    assert sum(x["estado"] == "podado" for x in final.values()) == (
        r["pasos"][-1]["total"] - r["pasos"][-1]["generados"]
        if modo in ("alfa-beta", "iterativa") else 0)


def test_alfa_beta_tiene_el_mismo_pseudo_en_sus_dos_paginas():
    """El modo alfa-beta lo enlazan 4_alfa_beta y 5_alfa_beta_como_algoritmo;
    su pseudo sale de la primera y tiene que ser el de la segunda."""
    otra = (UNIDAD / "2_mirar_todo_y_podar/5_alfa_beta_como_algoritmo.md").read_text(
        encoding="utf-8")
    bloques = re.findall(r"^```text\n(.*?)^```$", otra, re.S | re.M)
    assert "\n".join(j.pasos_interactivos("alfa-beta")["pseudo"]) + "\n" in bloques


# La secuencia de lineas de los modos sin tabla fila por fila en su pagina.
# Sale de la convencion de las tablas que si existen (una fila al entrar a un
# nodo y una por hijo que regresa) con la numeracion de cada pagina.
LINEAS_SIN_TABLA = {
    ("corte", 1): ["2", "4–5", "4–5", "4–5", "6"],
    ("corte", 3): ["2", "17", "19–20", "19–20", "4–5", "17", "11", "13–14", "13–14",
                   "19–20", "11", "13–14", "13–14", "19–20", "4–5", "17", "19–20",
                   "19–20", "4–5", "6"],
    ("iterativa", None): (
        ["2–3"]
        + ["5", "7–10", "7–10", "7–10", "11–12"]
        + ["5", "26", "28–31", "28–31", "7–10", "26", "28–31", "28–31", "7–10",
           "26", "28–31", "28–31", "7–10", "11–12"]
        + ["5", "26", "18", "20–23", "20–23", "28–31", "18", "20–22", "", "28–31",
           "7–10", "26", "28–30", "", "7–10", "26", "28–30", "", "7–10", "11–12"]
        + ["4, 13"]),
}


@pytest.mark.parametrize("modo,variante", list(LINEAS_SIN_TABLA), ids=lambda x: str(x))
def test_la_secuencia_de_lineas_sin_tabla_queda_fija(modo, variante):
    pasos = j.pasos_interactivos(modo, variante)["pasos"]
    assert [p["linea"] for p in pasos] == LINEAS_SIN_TABLA[(modo, variante)]
    if modo == "iterativa":
        assert pasos[-1]["lineas"] == [4, 13] and pasos[-1]["d"] == 3
        # mejor_jugada al empezar cada busqueda es la jugada lista (linea 5)
        assert [p["mejor_jugada"] for p in pasos if p["evento"] == "inicio"] == [
            "izq", "der", "centro"]
        assert "pasa a 4" not in pasos[-2]["frase"]


def _por_busqueda(pasos):
    """Los pasos partidos por busqueda (en iterativa, una por d)."""
    grupos = {}
    for p in pasos:
        grupos.setdefault(p.get("d"), []).append(p)
    return list(grupos.values())


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_la_foto_concuerda_con_el_paso(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    for grupo in _por_busqueda(r["pasos"]):
        evaluados, con_cota = set(), set()
        for p in grupo:
            e = p["estado"]
            if p["evaluado"]:
                evaluados.add(p["hijo"])
            # (b) «evaluado» exactamente en los hijos valorados con EVAL
            assert {k for k, x in e.items() if x["estado"] == "evaluado"} == evaluados, p["n"]
            # (a) la ventana del tope de la pila es la del paso
            if p["evento"] in ("inicio", "entra", "regresa", "raiz"):
                tope = e[p["pila"][-1]]
                assert (tope["alfa"], tope["beta"]) == (p["alfa"], p["beta"]), p["n"]
                assert tope["v"] == p["v"], p["n"]
            # el hijo que regresa guarda su w, y es cota si cortó dejando hijos
            if p["hijo"]:
                assert e[p["hijo"]]["v"] == p["w"], p["n"]
                assert e[p["hijo"]]["cota"] == (p["hijo"] in con_cota), p["n"]
            if p["evento"] == "podado":
                con_cota.add(p["pila"][-1])
                assert e[p["nodo"]]["estado"] == "podado"


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_cada_paso_trae_su_propia_copia(modo, variante):
    pasos = j.pasos_interactivos(modo, variante)["pasos"]
    ids_estado = [id(p["estado"]) for p in pasos]
    ids_pila = [id(p["pila"]) for p in pasos]
    ids_nodo = [id(x) for p in pasos for x in p["estado"].values()]
    assert len(set(ids_estado)) == len(pasos) and len(set(ids_pila)) == len(pasos)
    assert len(set(ids_nodo)) == len(ids_nodo)


@pytest.mark.parametrize("modo,variante", MODOS, ids=lambda x: str(x))
def test_la_frase_dice_lo_que_paso(modo, variante):
    r = j.pasos_interactivos(modo, variante)
    tipo = {x["id"]: x["tipo"] for x in r["arbol"]["nodos"]}
    prob = {x["id"]: x["prob"] for x in r["arbol"]["nodos"]}
    poda = modo in ("alfa-beta", "iterativa")
    for grupo in _por_busqueda(r["pasos"]):
        ventana, previo_v = {}, {}
        previo_r = "−∞"
        for p in grupo:
            f, t = p["frase"], tipo[p["pila"][-1]]
            if p["evento"] == "regresa":
                if p["corta"]:
                    marca = "≥ β" if t == "MAX" else "≤ α"
                    assert f"v = {p['v']} {marca} = " in f, f
                    borde = p["beta"] if t == "MAX" else p["alfa"]
                    assert f"{marca} = {borde} → corte {p['corta']}" in f, f
                elif t == "AZAR":
                    assert f"{prob[p['hijo']]} · {p['w']}" in f, f
                    peso = Fraction(prob[p["hijo"]]) * Fraction(p["w"])
                    assert f"v = {previo_v[p['nodo']]} + {j.fmt_t(peso)} = {p['v']}." in f, f
                else:
                    op = "max" if t == "MAX" else "min"
                    assert f": v = {op}(" in f and f"= {p['v']}" in f, f
                    if poda:
                        a0, b0 = ventana[p["nodo"]]
                        if t == "MAX":
                            esperado = (f"α sube a {p['alfa']}" if p["alfa"] != a0
                                        else f"α sigue en {p['alfa']}")
                        else:
                            esperado = (f"β baja a {p['beta']}" if p["beta"] != b0
                                        else f"β sigue en {p['beta']}")
                        assert esperado in f, f
            if p["evento"] == "raiz":
                nombre = "α" if poda else "mejor_valor"
                if p["mejora"]:
                    assert f"{p['w']} > {nombre} = {previo_r} → " in f, f
                    assert f"mejor_jugada = {p['mejor_jugada']}" in f, f
                else:
                    assert f"{p['w']} > {nombre} = {previo_r} es falso" in f, f
                    assert f"sigue en {p['mejor_jugada']}" in f, f
            if p["evento"] == "podado":
                hoja = tipo[p["nodo"]] == "HOJA"
                assert f.endswith("la deja fuera." if hoja else "lo deja fuera."), f
            if p["evento"] in ("inicio", "entra", "regresa"):
                ventana[p["nodo"]] = (p["alfa"], p["beta"])
                previo_v[p["nodo"]] = p["v"]
            if p["pila"] == ["R"] and p["evento"] in ("inicio", "raiz"):
                previo_r = p["v"]


@pytest.mark.parametrize("modo,variante", [
    ("corte", 0), ("corte", 4), ("corte", True), ("corte", "x"), ("alfa-beta", "T2"),
    ("alfa-beta", ""), ("minimax", "T"), ("azar", 1), ("iterativa", 3)])
def test_una_variante_invalida_da_value_error(modo, variante):
    with pytest.raises(ValueError):
        j.pasos_interactivos(modo, variante)


def test_el_total_de_la_iterativa_cuenta_las_tres_busquedas():
    r = j.pasos_interactivos("iterativa")["resultado"]
    assert (r["generados"], r["total"]) == (25, 42)
