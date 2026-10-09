"""El cuaderno de la unidad 7 dice lo mismo que las paginas y que juegos.py.

course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb corre en Colab, sin
el repositorio: no puede importar tools/juegos.py, asi que trae su propia
copia de cada algoritmo (el Python de la pagina, con `yield paso(...)` en
cada fila de la traza). Esta prueba es lo que ata esa copia a la fuente:

- el archivo es un nbformat 4 guardado sin salidas, y su primera celda
  lleva el badge de Colab con la URL de su propia ruta en main;
- celdas cortas: 15 lineas en general, 36 para una celda «algoritmo» (una
  funcion de la pagina entera, tal cual, mas sus yield), sin tope para la
  «maquinaria» plegada; 79 caracteres siempre;
- cada celda «algoritmo», sin sus lineas de instrumentacion y sin «yield
  from», es renglon por renglon la funcion del bloque ```python de su
  pagina: mismos comentarios, mismos marcadores, mismos saltos;
- las celdas «logica» (solo biblioteca estandar) se ejecutan aqui, y sus
  pasos se comparan campo por campo con juegos.pasos_interactivos para cada
  modo y variante, y con juegos.traza_decidir en arboles con empates, donde
  cambiar > por >= (o >= por >) cambia la jugada o los nodos generados;
- los marcadores «# (n)» de cada algoritmo son las lineas del pseudocodigo
  de su pagina, y la vista de codigo pone ▶ en cada linea de cada paso;
- con matplotlib instalado (no en CI), todas las celdas corren de punta a
  punta.

No compara frases ni el «total» de iterativa: esos textos son de la web.
"""
import json
import linecache
import re
from fractions import Fraction
from pathlib import Path

import pytest

import juegos as j

REPO = Path(__file__).resolve().parent.parent
RUTA = "course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb"
CUADERNO = REPO / RUTA
URL = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
       "blob/main/" + RUTA)
MAX_LINEAS, ALGORITMO_MAX, MAX_ANCHO = 15, 36, 79
SOLO_EN_LA_WEB = ("matplotlib", "ipywidgets", "IPython", "plt.")

MODOS = [("minimax", None), ("azar", None), ("alfa-beta", "T1"),
         ("alfa-beta", "T"), ("corte", 1), ("corte", 2), ("corte", 3),
         ("iterativa", None)]
CAMPOS = ("linea", "pila", "nodo", "v", "w", "hijo", "alfa", "beta",
          "corta", "mejor_jugada", "generados")
DECIDIR = {"minimax": "decidir_minimax", "azar": "decidir_expectiminimax",
           "alfa-beta": "decidir_alfa_beta", "corte": "decidir_con_corte",
           "iterativa": "profundizacion_iterativa"}
FUENTES = {"minimax": ("decidir_minimax", "minimax"),
           "azar": ("decidir_expectiminimax", "expectiminimax"),
           "alfa-beta": ("decidir_alfa_beta", "alfa_beta"),
           "corte": ("decidir_con_corte", "minimax_con_corte"),
           "iterativa": ("profundizacion_iterativa", "alfa_beta_con_corte")}

# Arboles con empates: en E1 la raiz empata (I y D valen 5) y la primera
# hoja de D empata con α = 5; en E2 la primera hoja de C2 empata con β = 5.
E1 = ((5, 6), (5, 9))
E2 = ((3, 6), ((5, 2), (5, 8)), (2, 12))
E3 = ((4, 6), (2, 8))                    # con azar en I y D: 5 y 5
EVAL_E1 = {"I": 5, "D": 5}


@pytest.fixture(scope="module")
def nb():
    return json.loads(CUADERNO.read_text(encoding="utf-8"))


def fuente(celda):
    s = celda["source"]
    return "".join(s) if isinstance(s, list) else s


def tags(celda):
    return celda.get("metadata", {}).get("tags", [])


def celdas(nb, tag=None, tipo="code"):
    return [c for c in nb["cells"] if c["cell_type"] == tipo
            and (tag is None or tag in tags(c))]


def ejecutar(celda, i, espacio):
    """exec con el codigo registrado en linecache, para inspect.getsource."""
    nombre = f"<celda {i}>"
    texto = fuente(celda)
    linecache.cache[nombre] = (len(texto), None, texto.splitlines(True),
                               nombre)
    exec(compile(texto, nombre, "exec"), espacio)


@pytest.fixture(scope="module")
def ns(nb):
    espacio = {"__name__": "cuaderno"}
    for i, c in enumerate(nb["cells"]):
        if "logica" in tags(c):
            ejecutar(c, i, espacio)
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
    assert "Ejecutar todas" in primera


def test_cada_celda_de_codigo_es_corta(nb):
    for c in celdas(nb):
        lineas = fuente(c).split("\n")
        for r in lineas:
            assert len(r) <= MAX_ANCHO, r
        if "maquinaria" in tags(c):
            assert c["metadata"].get("cellView") == "form"
            assert lineas[0].startswith("# @title"), lineas[0]
            continue
        tope = ALGORITMO_MAX if "algoritmo" in tags(c) else MAX_LINEAS
        assert len(lineas) <= tope, (len(lineas), lineas[0])


def test_la_maquinaria_son_dos_celdas_plegadas(nb):
    assert len(celdas(nb, "maquinaria")) == 2


def test_una_celda_por_funcion_de_la_pagina(nb):
    for c in celdas(nb, "algoritmo"):
        defs = re.findall(r"^def (\w+)", fuente(c), re.M)
        assert len(defs) == 1, defs
    nombres = {re.search(r"^def (\w+)", fuente(c), re.M).group(1)
               for c in celdas(nb, "algoritmo")}
    assert nombres == {n for par in FUENTES.values() for n in par}


def funciones_de_pagina(modo):
    """{nombre: renglones} del bloque ```python de la pagina del modo. Una
    funcion lleva los comentarios pegados encima de su def."""
    texto = (j.UNIDAD_JUEGOS / j.PAGINA_MODO[modo]).read_text(encoding="utf-8")
    bloque = re.search(r"^```python\n(.*?)^```$", texto, re.S | re.M).group(1)
    res, actual, pegados = {}, None, []
    for r in bloque.split("\n"):
        if r.startswith("def "):
            actual = re.match(r"def (\w+)", r).group(1)
            res[actual], pegados = pegados + [r], []
        elif r.startswith("#"):
            pegados.append(r)
        elif not r.strip():
            pegados = []
            if actual:
                res[actual].append(r)
        elif actual:
            res[actual].append(r)
    for renglones in res.values():
        while renglones and not renglones[-1].strip():
            renglones.pop()
    return res


def sin_instrumentar(texto):
    return [r.replace("yield from ", "") for r in texto.split("\n")
            if not re.search(r"yield paso\(|yield from corte\(", r)]


@pytest.mark.parametrize("modo", sorted(FUENTES))
def test_cada_funcion_es_la_de_la_pagina_tal_cual(nb, modo):
    pagina = funciones_de_pagina(modo)
    for c in celdas(nb, modo):
        if "algoritmo" not in tags(c):
            continue
        nombre = re.search(r"^def (\w+)", fuente(c), re.M).group(1)
        assert sin_instrumentar(fuente(c)) == pagina[nombre], nombre


def test_las_celdas_de_logica_solo_usan_la_biblioteca_estandar(nb):
    for c in celdas(nb, "logica"):
        for prohibido in SOLO_EN_LA_WEB:
            assert prohibido not in fuente(c), fuente(c)[:60]


def test_el_arbol_es_el_de_juegos(ns):
    assert ns["ARBOL_T"] == j.ARBOL_T
    assert ns["ARBOL_T1"] == j.ARBOL_T1
    assert ns["EVAL_T"] == j.EVAL_T


def correr(ns, modo, variante=None, arbol=None, azar=(), evaluar=None):
    ns["EVAL_T"].clear()
    ns["EVAL_T"].update(evaluar or j.EVAL_T)
    if arbol is None:
        arbol = ns["ARBOL_T1"] if variante == "T1" else ns["ARBOL_T"]
        azar = j.AZAR_T if modo == "azar" else ()
    ns["usar"](arbol, azar, cien=modo in ("corte", "iterativa"))
    ns["RELOJ"]["nodos"] = None
    args = ("R", variante) if modo == "corte" else ("R",)
    filas, jugada = ns["correr"](ns[DECIDIR[modo]](*args))
    return filas, jugada


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
    filas, jugada = correr(ns, modo, variante)
    fotos = ns["fotos_de"](filas)
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


def generados_como_juegos(f):
    """Los generados de la fila, con el nombre que les da juegos.nombres_t:
    una hoja se llama por su numero."""
    valor = f["t"]["valor"]
    return [str(valor[n]) if n in valor else n for n in f["hechos"]]


def cortes(ns, filas):
    return [(f["corta"], f["nodo"], f["w"], f["alfa"], f["beta"])
            for f in filas if f["evento"].startswith("corte")]


@pytest.mark.parametrize("arbol", [E1, E2, j.ARBOL_T], ids=["E1", "E2", "T"])
@pytest.mark.parametrize("modo", ["minimax", "alfa-beta"])
def test_con_empates_decide_y_genera_como_traza_decidir(ns, modo, arbol):
    t = j.traza_decidir(arbol, poda=modo == "alfa-beta")
    filas, jugada = correr(ns, modo, arbol=arbol)
    assert jugada == t["jugada"]
    assert filas[-1]["v"] == t["valor"]
    assert generados_como_juegos(filas[-1]) == t["orden_generados"]
    assert cortes(ns, filas) == t["cortes"]


@pytest.mark.parametrize("d", [1, 2])
@pytest.mark.parametrize("arbol,evaluar", [(E1, EVAL_E1), (E2, j.EVAL_T)],
                         ids=["E1", "E2"])
def test_con_empates_el_corte_es_el_de_traza_decidir(ns, arbol, evaluar, d):
    t = j.traza_decidir(arbol, profundidad=d, evaluar=evaluar)
    filas, jugada = correr(ns, "corte", d, arbol=arbol, evaluar=evaluar)
    assert jugada == t["jugada"]
    assert generados_como_juegos(filas[-1]) == t["orden_generados"]


@pytest.mark.parametrize("arbol,evaluar", [(E1, EVAL_E1), (E2, j.EVAL_T)],
                         ids=["E1", "E2"])
def test_con_empates_la_iterativa_es_la_de_juegos(ns, arbol, evaluar):
    esperado = j.profundizacion_iterativa_t(arbol, (1, 2, 3), evaluar)
    filas, jugada = correr(ns, "iterativa", arbol=arbol, evaluar=evaluar)
    fines = [i for i, f in enumerate(filas) if f["evento"] == "fin"]
    inicio = 0
    for (d, orden, t), fin in zip(esperado, fines):
        busqueda = filas[inicio:fin + 1]
        assert filas[fin]["mejor_jugada"] == t["jugada"], d
        assert generados_como_juegos(filas[fin]) == t["orden_generados"], d
        assert cortes(ns, busqueda) == t["cortes"], d
        inicio = fin + 1
    assert jugada == esperado[-1][2]["jugada"]


def test_con_empate_en_la_raiz_el_azar_deja_la_primera(ns):
    esperado, valores, _ = j.expectiminimax_t(E3, azar=("I", "D"))
    filas, jugada = correr(ns, "azar", arbol=E3, azar=("I", "D"))
    assert valores["I"] == valores["D"] == Fraction(5)
    assert jugada == esperado == "izq"


def test_el_reloj_de_nodos_entrega_la_ultima_busqueda_completa(ns):
    correr(ns, "iterativa")
    entregas = {}
    for n in (4, 5, 14, 15, 25):
        ns["RELOJ"]["nodos"] = n
        entregas[n] = ns["correr"](ns["profundizacion_iterativa"]("R"))[1]
    ns["RELOJ"]["nodos"] = None
    # d = 1 genera 4 nodos, d = 2 diez mas (14) y d = 3 once mas (25); R
    # mira el reloj cada vez que vuelve un hijo.
    assert entregas == {4: "izq", 5: "der", 14: "der", 15: "centro",
                        25: "centro"}


@pytest.mark.parametrize("modo", sorted(j.PAGINA_MODO))
def test_los_marcadores_son_las_lineas_de_la_pagina(nb, modo):
    pagina = set(n for n in j.renglones_pseudo(j.pseudo_de_pagina(modo)) if n)
    marcas = set()
    for c in celdas(nb, modo):
        marcas |= {int(n) for n in re.findall(r"# \((\d+)\)", fuente(c))}
    assert marcas == pagina, (sorted(marcas - pagina), sorted(pagina - marcas))


@pytest.mark.parametrize("modo,variante", MODOS)
def test_la_vista_de_codigo_marca_cada_linea_del_paso(ns, modo, variante):
    import inspect
    filas, _ = correr(ns, modo, variante)
    fuentes = [ns[n] for n in FUENTES[modo]]
    for f in filas:
        for n in ns["rango"](f["linea"]):
            fn = ns["elegir"](f, fuentes)
            vista = list(ns["con_flechas"](inspect.getsource(fn), [n]))
            assert any(r.startswith("▶") for r in vista), (modo, f["n"], n)


@pytest.mark.parametrize("modo", sorted(FUENTES))
def test_toda_llamada_recursiva_puede_llevar_flecha(ns, modo):
    import inspect
    for nombre in FUENTES[modo]:
        texto = inspect.getsource(ns[nombre])
        todas = list(range(1, 40))
        for r in ns["con_flechas"](texto, todas):
            if "yield from" in r:
                assert r.startswith("▶"), (nombre, r)


def test_de_punta_a_punta_con_matplotlib(nb, monkeypatch):
    pytest.importorskip("matplotlib")
    monkeypatch.setenv("MPLBACKEND", "Agg")
    import matplotlib
    matplotlib.use("Agg")
    espacio = {"__name__": "cuaderno"}
    for i, c in enumerate(celdas(nb)):
        ejecutar(c, i, espacio)
        if "HAY_WIDGETS" in espacio:
            espacio["HAY_WIDGETS"] = False       # el respaldo con un for
    import matplotlib.pyplot as plt
    plt.close("all")
    assert espacio["RELOJ"]["nodos"] is None
