"""pasos_por_linea: un paso por cada linea del pseudocodigo que se ejecuta.

La traza interactiva del arbol T avanzaba una FILA de la tabla por paso: en
alfa-beta, del paso de la linea 2 saltaba a la 18 y se comia las lineas 3,
4, 7, 8, 9 y 17. pasos_por_linea ejecuta el pseudocodigo de la pagina de cada
modo renglon por renglon. Estas pruebas lo atan por cuatro lados:

(a) la secuencia de lineas es una ejecucion valida del pseudocodigo: se
    recorre con el grafo de control de cada pagina, escrito aqui a mano
    (SUCESORES), y una pila de llamadas propia;
(b) proyectada a filas (el ultimo paso de cada fila) da los mismos valores
    que pasos_interactivos, que a su vez test_pasos_interactivos compara con
    las tablas de las paginas;
(c) los resultados y los nodos generados son los hechos de la unidad;
(d) ninguna linea se salta: el conjunto de lineas que corre cada modo es el
    esperado, y ninguna variable cambia sin que el paso lo declare;
(e) frases cortas, deterministas y todo serializable.
"""
import json
import re
from fractions import Fraction

import pytest

import juegos as j

MODOS = [("minimax", None), ("azar", None), ("alfa-beta", "T1"), ("alfa-beta", "T"),
         ("corte", 1), ("corte", 2), ("corte", 3), ("iterativa", None)]
IDS = [f"{m}-{v}" if v else m for m, v in MODOS]

RET, FIN = "RET", "FIN"

# El grafo de control de cada pseudocodigo, linea por linea: a que lineas
# puede seguir. RET: la funcion devuelve (lo siguiente es la linea de la
# llamada, en el marco de abajo). FIN: termina el programa. LLAMA: las lineas
# de llamada y la linea `function` a la que saltan.
_DECIDIR = {1: {2}, 2: {3}, 3: {4}, 4: {5}, 5: {3, 6}, 6: {FIN}}
SUCESORES = {
    "minimax": {**_DECIDIR, **{
        7: {8}, 8: {9, RET}, 9: {10, 15}, 10: {11}, 11: {12}, 12: {13}, 13: {11, 14},
        14: {RET}, 15: {16}, 16: {17}, 17: {18}, 18: {19}, 19: {17, 20}, 20: {RET}}},
    "azar": {**_DECIDIR, **{
        7: {8}, 8: {9, RET}, 9: {10, 15}, 10: {11}, 11: {12}, 12: {13}, 13: {11, 14},
        14: {RET}, 15: {16, 21}, 16: {17}, 17: {18}, 18: {19}, 19: {17, 20}, 20: {RET},
        21: {22}, 22: {23}, 23: {24}, 24: {25}, 25: {23, 26}, 26: {RET}}},
    "alfa-beta": {**_DECIDIR, **{
        7: {8}, 8: {9, RET}, 9: {10, 17}, 10: {11}, 11: {12}, 12: {13}, 13: {14},
        14: {15, RET}, 15: {11, 16}, 16: {RET}, 17: {18}, 18: {19}, 19: {20}, 20: {21},
        21: {22}, 22: {23, RET}, 23: {19, 24}, 24: {RET}}},
    "corte": {**_DECIDIR, **{
        7: {8}, 8: {9, RET}, 9: {10, RET}, 10: {11, 16}, 11: {12}, 12: {13}, 13: {14},
        14: {12, 15}, 15: {RET}, 16: {17}, 17: {18}, 18: {19}, 19: {20}, 20: {18, 21},
        21: {RET}}},
    "iterativa": {
        1: {2}, 2: {3}, 3: {4}, 4: {5, 13}, 5: {6}, 6: {7}, 7: {8}, 8: {9, FIN},
        9: {10, FIN}, 10: {6, 11}, 11: {12}, 12: {4}, 13: {FIN},
        14: {15}, 15: {16, RET}, 16: {17, RET}, 17: {18, 25}, 18: {19}, 19: {20},
        20: {21}, 21: {22}, 22: {23, RET}, 23: {19, 24}, 24: {RET}, 25: {26}, 26: {27},
        27: {28}, 28: {29}, 29: {30}, 30: {31, RET}, 31: {27, 32}, 32: {RET}},
}
LLAMA = {"minimax": {4: 7, 12: 7, 18: 7}, "azar": {4: 7, 12: 7, 18: 7, 24: 7},
         "alfa-beta": {4: 7, 12: 7, 20: 7}, "corte": {4: 7, 13: 7, 19: 7},
         "iterativa": {7: 14, 20: 14, 28: 14}}
FUNCIONES = {"minimax": {1, 7}, "azar": {1, 7}, "alfa-beta": {1, 7}, "corte": {1, 7},
             "iterativa": {1, 14}}


@pytest.fixture(scope="module", params=MODOS, ids=IDS)
def caso(request):
    modo, variante = request.param
    return modo, j.pasos_por_linea(modo, variante), j.pasos_interactivos(modo, variante)


def num(s):
    if s == "+∞":
        return float("inf")
    if s == "−∞":
        return float("-inf")
    return Fraction(s)


def todas(m):
    return dict(m["args"] + m["locales"])


# ---------------------------------------------------------------- (a) ---

def test_a_la_secuencia_de_lineas_es_una_ejecucion_valida(caso):
    modo, d, _ = caso
    suc, llama = SUCESORES[modo], LLAMA[modo]
    pasos = d["pasos"]
    pila = []                      # lineas de llamada pendientes de recibir
    regreso = False                # el paso actual es «w ←» tras un RET
    assert pasos[0]["linea"] == 1
    for k in range(len(pasos) - 1):
        p, q = pasos[k], pasos[k + 1]
        l, m = p["linea"], q["linea"]
        if l in llama and not regreso:
            # «llama»: el hijo se genera aqui y lo siguiente es su function
            assert m == llama[l], f"paso {p['n']}: tras llamar en {l} viene {m}"
            assert len(q["marco"]) == len(p["marco"]) + 1
            assert q["marco"][-1]["nodo"] == q["nodo"]
            assert p["generados"] == pasos[k - 1]["generados"] + 1   # se genera al llamar
            assert q["generados"] == p["generados"]
            pila.append(l)
            regreso = False
            continue
        if m in suc[l]:
            assert len(q["marco"]) == len(p["marco"]), f"paso {q['n']}: cambia la pila sin llamar"
            regreso = False
            continue
        assert RET in suc[l], f"paso {p['n']} → {q['n']}: {l} → {m} no es una arista"
        assert pila and m == pila.pop(), f"paso {q['n']}: el RET de {l} no vuelve a su llamada"
        assert len(q["marco"]) == len(p["marco"]) - 1
        regreso = True
    assert FIN in suc[pasos[-1]["linea"]] and not pila


def test_a_cada_paso_corre_en_el_marco_de_su_funcion(caso):
    modo, d, _ = caso
    inicio = sorted(FUNCIONES[modo])
    for p in d["pasos"]:
        f = 0 if len(p["marco"]) == 1 else 1
        assert (p["linea"] >= inicio[1]) == bool(f), p["n"]
        assert p["nodo"] == p["marco"][-1]["nodo"]


def test_a_el_problema_reportado_alfa_beta_ya_no_salta_lineas():
    pasos = j.pasos_por_linea("alfa-beta", "T")["pasos"]
    assert [p["linea"] for p in pasos[:9]] == [1, 2, 3, 4, 7, 8, 9, 17, 18]
    assert [p["linea"] for p in pasos[9:17]] == [19, 20, 7, 8, 20, 21, 22, 23]


# ---------------------------------------------------------------- (b) ---

def _ultimo_de_cada_fila(pasos):
    res = {}
    for p in pasos:
        res[p["fila"]] = p
        for x in p["filas_x"]:
            res[x] = p
    return res


def test_b_las_filas_se_numeran_como_la_tabla(caso):
    _, d, b = caso
    pasos = d["pasos"]
    filas = [p["fila"] for p in pasos]
    assert filas == sorted(filas) and filas[0] == 1
    cubiertas = set(filas) | {x for p in pasos for x in p["filas_x"]}
    assert cubiertas == set(range(1, len(b["pasos"]) + 1))
    for p in pasos:
        for x in p["filas_x"]:
            assert b["pasos"][x - 1]["evento"] == "podado"


def test_b_proyectar_a_filas_da_pasos_interactivos(caso):
    modo, d, b = caso
    ab = modo in ("alfa-beta", "iterativa")
    ult = _ultimo_de_cada_fila(d["pasos"])
    for f in b["pasos"]:
        p = ult[f["n"]]
        donde = f"{modo} fila {f['n']} (paso {p['n']})"
        assert p["estado"] == f["estado"], donde
        assert p["generados"] == f["generados"], donde
        if f["evento"] == "podado":
            assert f["n"] in p["filas_x"], donde
            continue
        assert p["linea"] in f["lineas"], donde
        pila = [m["nodo"] for m in p["marco"]]
        assert pila == f["pila"], donde
        raiz, yo = todas(p["marco"][0]), todas(p["marco"][-1])
        assert raiz.get("mejor_jugada", "ninguna") == f["mejor_jugada"], donde
        if len(pila) == 1:
            assert raiz.get("α" if ab else "mejor_valor", "") == f["v"], donde
            if ab:
                assert raiz.get("α", "") == f["alfa"], donde
                assert f["beta"] in ("+∞", ""), donde
        else:
            assert yo["v"] == f["v"], donde
            if ab:
                assert (yo["α"], yo["β"]) == (f["alfa"], f["beta"]), donde
        if f["evento"] in ("regresa", "raiz"):
            assert yo["w"] == f["w"], donde
        if modo == "iterativa":
            assert p["d"] == f["d"], donde
            assert raiz["jugada"] == f["jugada"], donde


# ---------------------------------------------------------------- (c) ---

HECHOS = {
    ("minimax", None): ("centro", "5", 14, 14),
    ("azar", None): ("der", "7", 14, 14),
    ("alfa-beta", "T1"): ("izq", "3", 6, 7),
    ("alfa-beta", "T"): ("centro", "5", 12, 14),
    ("corte", 1): ("der", "7", 4, 14),
    ("corte", 2): ("centro", "6", 10, 14),
    ("corte", 3): ("centro", "5", 14, 14),
}


@pytest.mark.parametrize("modo,variante", MODOS, ids=IDS)
def test_c_resultados_y_generados_son_los_hechos(modo, variante):
    d = j.pasos_por_linea(modo, variante)
    r, ultimo = d["resultado"], d["pasos"][-1]
    if modo == "iterativa":
        assert [(x["d"], x["jugada"], x["generados"]) for x in r["por_d"]] == [
            (1, "der", 4), (2, "centro", 10), (3, "centro", 11)]
        assert r["jugada"] == "centro" and r["generados"] == 25
        assert todas(ultimo["marco"][0])["jugada"] == "centro"
        assert sum(1 for p in d["pasos"] if p["linea"] == 4) == 4
        assert [p["frase"].split("?")[1].split()[0].strip(":") for p in d["pasos"] if p["linea"] == 4] == [
            "sí", "sí", "sí", "no"]
        return
    jugada, valor, generados, total = HECHOS[(modo, variante)]
    assert (r["jugada"], r["valor"], r["generados"], r["total"]) == (jugada, valor, generados,
                                                                     total)
    assert ultimo["generados"] == generados
    llamadas = sum(1 for p, q in zip(d["pasos"], d["pasos"][1:])
                   if len(q["marco"]) > len(p["marco"]))
    assert llamadas == generados - 1          # cada nodo generado, salvo R, se llama
    # en azar, las sumas exactas de I, C y D
    if modo == "azar":
        ws = [todas(p["marco"][0])["w"] for p in d["pasos"] if p["linea"] == 5]
        assert ws == ["9/2", "13/2", "7"]


# ---------------------------------------------------------------- (d) ---

def _rango(a, b):
    return set(range(a, b + 1))


# Las lineas que corre cada modo (todas las demas, nunca): en azar no hay
# nodos de MIN; con d = 1 todo hijo de R se estima en la linea 9; con d = 2,
# C1 y C2 se estiman y solo I, C y D (de MIN) llegan a preguntar Pl(s).
LINEAS_QUE_CORREN = {
    ("minimax", None): _rango(1, 20),
    ("azar", None): _rango(1, 15) | _rango(21, 26),
    ("alfa-beta", "T1"): _rango(1, 9) | _rango(17, 24),
    ("alfa-beta", "T"): _rango(1, 24),
    ("corte", 1): _rango(1, 9),
    ("corte", 2): _rango(1, 10) | _rango(16, 21),
    ("corte", 3): _rango(1, 21),
    ("iterativa", None): _rango(1, 32),
}


@pytest.mark.parametrize("modo,variante", MODOS, ids=IDS)
def test_d_corren_exactamente_las_lineas_esperadas(modo, variante):
    d = j.pasos_por_linea(modo, variante)
    corren = {p["linea"] for p in d["pasos"]}
    assert corren == LINEAS_QUE_CORREN[(modo, variante)]
    ejecutables = {r for r in d["renglones"] if r is not None}
    assert corren <= ejecutables


def test_d_ninguna_variable_cambia_sin_que_su_paso_lo_diga(caso):
    """Lo que el panel muestra en el paso k es lo que escribio la linea k:
    cada diferencia entre dos marcos seguidos esta en `cambia`, y cada
    entrada de `cambia` guarda el valor de antes."""
    _, d, _ = caso
    previo = []
    for p in d["pasos"]:
        declaradas = {(i, k): antes for i, k, antes in p["cambia"]}
        for i, m in enumerate(p["marco"]):
            mismo = (i < len(previo) and previo[i]["func"] == m["func"]
                     and previo[i]["nodo"] == m["nodo"])
            antes = todas(previo[i]) if mismo else {}
            for k, v in todas(m).items():
                if antes.get(k) != v:
                    assert (i, k) in declaradas, f"paso {p['n']}: {k} cambia sin aviso"
            for (ii, k), a in declaradas.items():
                if ii == i:
                    assert a == antes.get(k, ""), f"paso {p['n']}: «antes» de {k}"
        previo = p["marco"]


def test_d_las_asignaciones_escriben_lo_que_dice_su_linea(caso):
    """v ← max/min, v ← v + Pr · w, α ← max, β ← min: el valor nuevo de cada
    una sale del de antes y de w, y la escribe el paso de ESA linea."""
    modo, d, _ = caso
    for p in d["pasos"]:
        f = p["frase"]
        m = re.match(r"^(v|α|β) ← (max|min)\((.+?), (.+?)\) = (.+?)[.:]", f)
        if m:
            var, op, a, b, r = m.groups()
            yo = todas(p["marco"][-1])
            esperado = (max if op == "max" else min)(num(a), num(b))
            assert num(r) == esperado and num(yo[var]) == esperado, f
            assert [len(p["marco"]) - 1, var] in [c[:2] for c in p["cambia"]], f
            if var == "v":
                assert num(b) == num(yo["w"]), f
        m = re.match(r"^v ← (.+?) \+ 1/2 · (.+?) = (.+?)\.", f)
        if m:
            yo = todas(p["marco"][-1])
            assert num(yo["v"]) == num(m.group(1)) + num(m.group(2)) / 2 == num(m.group(3))


# ---------------------------------------------------------------- (e) ---

@pytest.mark.parametrize("modo,variante", MODOS, ids=IDS)
def test_e_frases_cortas_deterministas_y_serializable(modo, variante):
    a = j.pasos_por_linea(modo, variante)
    b = j.pasos_por_linea(modo, variante)
    assert json.dumps(a, ensure_ascii=False) == json.dumps(b, ensure_ascii=False)
    for p in a["pasos"]:
        assert 0 < len(p["frase"]) <= 90, p["frase"]
        assert not p["frase"][0].isspace(), p["frase"]
        assert p["frase"].endswith("."), p["frase"]
        assert "I-1" not in p["frase"] and not re.search(r"\b[A-Z]\d?-\d\b", p["frase"]), (
            "los ids internos de las hojas no se muestran")
    assert [p["n"] for p in a["pasos"]] == list(range(1, len(a["pasos"]) + 1))
