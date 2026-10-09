"""El cuaderno de la unidad 7 dice lo mismo que las paginas y que juegos.py.

course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb corre en Colab, sin
el repositorio: no puede importar tools/juegos.py, asi que trae su propia
copia de cada algoritmo (el Python de la pagina, instrumentado como
generador). Esta prueba es lo que ata esa copia a la fuente:

- el archivo es un nbformat 4 guardado sin salidas, y su primera celda
  lleva el badge de Colab con la URL de su propia ruta en main;
- cada celda de codigo cabe en 15 lineas de a lo mas 79 caracteres (el
  cuaderno es compacto a proposito);
- las celdas marcadas «logica» (solo biblioteca estandar) se ejecutan aqui
  en orden, y los pasos que producen sus generadores se comparan, campo
  por campo, con juegos.pasos_interactivos para cada modo y variante;
- los marcadores «# (n)» de cada algoritmo cubren exactamente las lineas
  del pseudocodigo de su pagina.

No compara frases ni el «total» de iterativa: esos textos son de la web.
CI no tiene matplotlib ni ipywidgets: solo se ejecutan las celdas «logica».
"""
import json
import re
from pathlib import Path

import pytest

import juegos as j

REPO = Path(__file__).resolve().parent.parent
RUTA = "course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb"
CUADERNO = REPO / RUTA
URL = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
       "blob/main/" + RUTA)
MAX_LINEAS, MAX_ANCHO = 15, 79
SOLO_EN_LA_WEB = ("matplotlib", "ipywidgets", "IPython", "plt.")

MODOS = [("minimax", None), ("azar", None), ("alfa-beta", "T1"),
         ("alfa-beta", "T"), ("corte", 1), ("corte", 2), ("corte", 3),
         ("iterativa", None)]
CAMPOS = ("linea", "pila", "nodo", "v", "w", "hijo", "alfa", "beta",
          "corta", "mejor_jugada", "generados")


@pytest.fixture(scope="module")
def nb():
    return json.loads(CUADERNO.read_text(encoding="utf-8"))


def fuente(celda):
    s = celda["source"]
    return "".join(s) if isinstance(s, list) else s


def celdas(nb, tag=None, tipo="code"):
    return [c for c in nb["cells"] if c["cell_type"] == tipo
            and (tag is None or tag in c.get("metadata", {}).get("tags", []))]


@pytest.fixture(scope="module")
def ns(nb):
    espacio = {"__name__": "cuaderno"}
    for c in celdas(nb, "logica"):
        exec(compile(fuente(c), "<cuaderno>", "exec"), espacio)
    return espacio


def test_es_nbformat_4_sin_salidas(nb):
    assert nb["nbformat"] == 4
    assert nb["metadata"]["kernelspec"]["name"] == "python3"
    for c in nb["cells"]:
        assert c["cell_type"] in ("markdown", "code")
        if c["cell_type"] == "code":
            assert c["outputs"] == [], fuente(c)[:60]
            assert c["execution_count"] is None, fuente(c)[:60]


def test_la_primera_celda_abre_este_cuaderno_en_colab(nb):
    primera = fuente(nb["cells"][0])
    assert nb["cells"][0]["cell_type"] == "markdown"
    assert "colab-badge.svg" in primera
    assert f"]({URL})" in primera


def test_cada_celda_de_codigo_es_corta(nb):
    for c in celdas(nb):
        lineas = fuente(c).split("\n")
        assert len(lineas) <= MAX_LINEAS, (len(lineas), lineas[0])
        for r in lineas:
            assert len(r) <= MAX_ANCHO, r


def test_las_celdas_de_logica_solo_usan_la_biblioteca_estandar(nb):
    logica = celdas(nb, "logica")
    assert len(logica) >= 20
    for c in logica:
        for prohibido in SOLO_EN_LA_WEB:
            assert prohibido not in fuente(c), fuente(c)[:60]


def test_el_arbol_es_el_de_juegos(ns):
    assert ns["ARBOL_T"] == j.ARBOL_T
    assert ns["ARBOL_T1"] == j.ARBOL_T1
    assert ns["EVAL_T"] == j.EVAL_T


def correr(ns, modo, variante):
    ns["EVAL_T"].clear()
    ns["EVAL_T"].update(j.EVAL_T)
    arbol = ns["ARBOL_T1"] if variante == "T1" else ns["ARBOL_T"]
    ns["usar"](arbol, j.AZAR_T if modo == "azar" else ())
    ns["RELOJ"]["nodos"] = None
    gen = {"minimax": lambda: ns["decidir_minimax"]("R"),
           "azar": lambda: ns["decidir_expectiminimax"]("R"),
           "alfa-beta": lambda: ns["decidir_alfa_beta"]("R"),
           "corte": lambda: ns["decidir_con_corte"]("R", variante),
           "iterativa": lambda: ns["profundizacion_iterativa"]("R")}[modo]
    filas, jugada = ns["correr"](gen())
    return filas, jugada, ns["fotos_de"](filas)


def como_web(ns, f, campo):
    """El campo de una fila del cuaderno, con el formato de juegos.fmt_t."""
    fmt = ns["fmt"]
    if campo == "generados":
        return len(f["hechos"])
    if campo in ("v", "w", "alfa", "beta"):
        return fmt(f[campo])
    if campo in ("hijo", "corta"):
        return f[campo] or ""
    if campo == "mejor_jugada":
        return f[campo] or "ninguna"
    return f[campo]


@pytest.mark.parametrize("modo,variante", MODOS)
def test_los_pasos_del_cuaderno_son_los_de_juegos(ns, modo, variante):
    web = j.pasos_interactivos(modo, variante)
    filas, jugada, fotos = correr(ns, modo, variante)
    assert len(filas) == len(web["pasos"])
    for f, foto, p in zip(filas, fotos, web["pasos"]):
        donde = f"{modo} {variante} paso {p['n']}"
        for campo in CAMPOS:
            if campo == "linea" and p["evento"] == "entrega":
                assert 13 in p["lineas"], donde      # 13, o 4 y 13
                continue
            assert como_web(ns, f, campo) == p[campo], (donde, campo)
        if modo == "iterativa":
            assert f["jugada"] == p["jugada"], donde
            if p["evento"] != "entrega":
                assert f["d"] == p["d"], donde
        for nodo, e in p["estado"].items():
            mio = foto[nodo]
            assert mio["estado"] == e["estado"], (donde, nodo)
            assert ns["fmt"](mio["v"]) == e["v"], (donde, nodo)
            assert mio["cota"] == e["cota"], (donde, nodo)
    res = web["resultado"]
    assert jugada == res["jugada"]
    assert ns["fmt"](filas[-1]["v"]) == res["valor"]
    if modo == "iterativa":
        fines = [f for f in filas if f["evento"] == "fin"]
        assert [len(f["hechos"]) for f in fines] == [
            x["generados"] for x in res["por_d"]]
        assert [f["mejor_jugada"] for f in fines] == [
            x["jugada"] for x in res["por_d"]]
    else:
        assert len(filas[-1]["hechos"]) == res["generados"]


def test_el_reloj_de_nodos_entrega_la_ultima_busqueda_completa(ns):
    correr(ns, "iterativa", None)
    entregas = {}
    for n in (4, 13, 14, 24, 25):
        ns["RELOJ"]["nodos"] = n
        entregas[n] = ns["correr"](ns["profundizacion_iterativa"]("R"))[1]
    ns["RELOJ"]["nodos"] = None
    # d = 1 genera 4 nodos, d = 2 diez mas (14) y d = 3 once mas (25).
    assert entregas == {4: "izq", 13: "der", 14: "der", 24: "centro",
                        25: "centro"}


@pytest.mark.parametrize("modo", sorted(j.PAGINA_MODO))
def test_los_marcadores_son_las_lineas_de_la_pagina(nb, modo):
    pagina = set(n for n in j.renglones_pseudo(j.pseudo_de_pagina(modo)) if n)
    marcas = set()
    for c in celdas(nb, modo):
        for r in fuente(c).split("\n"):
            marcas |= {int(n) for n in re.findall(r"# \((\d+)\)", r)}
    assert marcas == pagina, (sorted(marcas - pagina), sorted(pagina - marcas))
