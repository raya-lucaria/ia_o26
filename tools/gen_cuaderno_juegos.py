"""Genera el notebook de la unidad de juegos (unidad 7) para Colab.

Escribe course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb, guardado sin
salidas: minimax, expectiminimax, alfa-beta, minimax con corte y
profundizacion iterativa sobre el arbol T, paso a paso, con un deslizador.

Colab no tiene el repositorio, asi que el notebook no importa juegos.py: cada
celda «algoritmo» se arma aqui a partir del bloque ```python de su pagina,
renglon por renglon, y solo se le agrega la instrumentacion (`yield from` en
las llamadas recursivas y las lineas `yield paso(...)` / `yield from
corte(...)` en las anclas de INSTRUMENTOS). La prosa, la maquinaria plegada
y las celdas de corrida viven en este archivo.

Correrlo despues de cambiar el Python de una de esas paginas, o algo de
aqui: `python3 tools/gen_cuaderno_juegos.py`. Es idempotente: con las
paginas iguales produce el mismo archivo byte a byte, y
test_cuaderno_juegos.py falla si el notebook comiteado no es el que este
generador produce hoy.
"""
import json
import re
import sys
from pathlib import Path

from juegos import PAGINA_MODO, UNIDAD_JUEGOS

RAIZ = Path(__file__).resolve().parent.parent
RUTA = "course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb"
CELDAS = []


def md(texto):
    CELDAS.append({"cell_type": "markdown", "metadata": {},
                   "source": texto.strip("\n")})


def code(texto, *tags, oculta=False):
    meta = {}
    if oculta:
        meta["cellView"] = "form"
    if tags:
        meta["tags"] = list(tags)
    CELDAS.append({"cell_type": "code", "execution_count": None,
                   "metadata": meta, "outputs": [],
                   "source": texto.strip("\n")})


# --- Las celdas de algoritmo salen del bloque ```python de su página ---
RECURSIVAS = ("minimax", "expectiminimax", "alfa_beta", "minimax_con_corte",
              "alfa_beta_con_corte")


def funciones_de_pagina(modo):
    texto = (UNIDAD_JUEGOS / PAGINA_MODO[modo]).read_text(encoding="utf-8")
    bloque = re.search(r"^```python\n(.*?)^```$", texto, re.S | re.M).group(1)
    res, actual, pendientes = {}, None, []
    for r in bloque.split("\n"):
        if r.startswith("def "):
            actual = re.match(r"def (\w+)", r).group(1)
            res[actual] = pendientes + [r]
            pendientes = []
        elif r.startswith("#"):
            pendientes.append(r)
        elif not r.strip():
            pendientes = []
            if actual:
                res[actual].append(r)
        elif actual:
            res[actual].append(r)
    for k, v in res.items():
        while v and not v[-1].strip():
            v.pop()
    return res


# (ancla, texto, «despues» o «antes», sangria o None, ocurrencia)
def fila(ancla, linea, donde="despues", sangria=None, k=1):
    return (ancla, f'yield paso("{linea}", locals())', donde, sangria, k)

def cortar(ancla, linea):
    return (ancla, f'yield from corte("{linea}", locals())', "dentro",
            None, 1)

DECIDIR = [fila("mejor_jugada = None", "2"),
           fila("mejor_jugada = a", "4–5", sangria=8),
           fila("return mejor_jugada", "6", "antes")]
INSTRUMENTOS = {
    "decidir_minimax": DECIDIR, "decidir_expectiminimax": DECIDIR,
    "decidir_alfa_beta": DECIDIR, "decidir_con_corte": DECIDIR,
    "minimax": [fila("v = -inf", "10"), fila("v = max(v, w)", "12–13"),
                fila("v = inf", "16"), fila("v = min(v, w)", "18–19")],
    "expectiminimax": [fila("v = 0", "22"),
                       fila("v = v + pr(s, a) * w", "24–25")],
    "alfa_beta": [fila("v = -inf", "10"), cortar("if v >= beta:", "12–14"),
                  fila("alfa = max(alfa, v)", "12–15"),
                  fila("v = inf", "18"), cortar("if v <= alfa:", "20–22"),
                  fila("beta = min(beta, v)", "20–23")],
    "minimax_con_corte": [fila("v = -inf", "11"),
                          fila("v = max(v, w)", "13–14"),
                          fila("v = inf", "17"),
                          fila("v = min(v, w)", "19–20")],
    "alfa_beta_con_corte": [
        fila("v = -inf", "18"), cortar("if v >= beta:", "20–22"),
        fila("alfa = max(alfa, v)", "20–23"),
        fila("v = inf", "26"), cortar("if v <= alfa:", "28–30"),
        fila("beta = min(beta, v)", "28–31")],
    "profundizacion_iterativa": [
        fila("d = 1 ", "2–3"), fila("mejor_jugada = jugada", "5"),
        fila("mejor_jugada = a", "7–10", sangria=12),
        fila("jugada = mejor_jugada", "11–12"),
        fila("return jugada", "13", "antes", k=2)],
}


def instrumentar(nombre, lineas):
    lineas = [re.sub(r"\bw = (" + "|".join(RECURSIVAS) + r")\(",
                     r"w = yield from \1(", r) for r in lineas]
    for ancla, texto, donde, sangria, k in INSTRUMENTOS[nombre]:
        hits = [i for i, r in enumerate(lineas)
                if (r.strip() + " ").startswith(ancla)]
        i = hits[k - 1]
        base = len(lineas[i]) - len(lineas[i].lstrip())
        if donde == "dentro":
            nueva = " " * (base + 4) + texto
            lineas.insert(i + 1, nueva)
            continue
        nueva = " " * (base if sangria is None else sangria) + texto
        lineas.insert(i + 1 if donde == "despues" else i, nueva)
    return "\n".join(lineas)


def algoritmo_de(modo, nombre):
    lineas = funciones_de_pagina(modo)[nombre]
    code(instrumentar(nombre, lineas), "logica", "algoritmo", modo)


URL = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
       "blob/main/" + RUTA)

# ================================================================ 0 ===
md(f"""
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({URL})

# Notebook · Decidir en el árbol T

Cinco algoritmos en el mismo árbol de juguete: **minimax**,
**expectiminimax**, **alfa-beta**, **minimax con corte** y **profundización
iterativa**. El código es el Python de las páginas, con su número de línea
`# (n)`.

- Primero: **Entorno de ejecución → Ejecutar todas** (`Ctrl + F9`).
- La sección 1 es maquinaria: no hace falta leerla.
- Mueve el deslizador **paso** (o dale ▶): ves el árbol, la línea que corre
  y sus variables. Cada sección cierra con un **Pruébalo**.
""")

# ================================================================ 1 ===
md("""
## 1 · Preparación

Dos celdas plegadas: las reglas del árbol y el visor. Córrelas y sigue.
""")

code(r'''
# @title Reglas y árbol (no hace falta leerla)
from fractions import Fraction
from math import inf
import inspect
import re

# R (MAX) → I, C, D (MIN) por izq, centro, der;
# C → C1, C2 (MAX) por c1, c2. Los números son hojas.
ARBOL_T = ((3, 6), ((5, 2), (7, 8)), (2, 12))
ARBOL_T1 = ((3, 6), (2, 12))                 # T sin el centro
EVAL_T = {"I": 5, "C": 4, "D": 7, "C1": 6, "C2": 9}
JUGADAS_R = {3: ["izq", "centro", "der"], 2: ["izq", "der"]}
NOMBRE_R = {"izq": "I", "centro": "C", "der": "D"}


def armar(arbol, s="R", k=0, t=None):
    """Nombra los nodos: R; I, C, D; C1, C2; una hoja, «padre-lugar»."""
    t = t or dict(hijos={}, valor={}, prof={}, padre={})
    t["prof"][s] = k
    if not isinstance(arbol, tuple):
        t["valor"][s] = arbol
        return t
    t["hijos"][s] = {}
    for i, h in enumerate(arbol, 1):
        a = JUGADAS_R[len(arbol)][i - 1] if k == 0 else f"{s.lower()}{i}"
        sep = "" if isinstance(h, tuple) else "-"
        n = NOMBRE_R[a] if k == 0 else f"{s}{sep}{i}"
        t["hijos"][s][a], t["padre"][n] = n, s
        armar(h, n, k + 1, t)
    return t


def usar(arbol, azar=(), cien=False, al_reves=False):
    """Elige el árbol. azar: los nodos de azar. cien: la escala de la
    clase 3 (la hoja 3 es un final con U = 3/100). al_reves: cada A(s)
    en el orden inverso, sin cambiar nombres."""
    global JUEGO
    JUEGO = armar(arbol)
    JUEGO.update(azar=set(azar), cien=cien, al_reves=al_reves)


# --- Las reglas: S_F, U, Pl, A, T, Pr y EVAL -------------------------
def es_final(s):
    return s in JUEGO["valor"]

def utilidad(s):
    u = JUEGO["valor"][s]
    return Fraction(u, 100) if JUEGO["cien"] else u

def pl(s):
    if s in JUEGO["azar"]:
        return "AZAR"
    return ("MAX", "MIN")[JUEGO["prof"][s] % 2]

def acciones(s):
    a = list(JUEGO["hijos"][s])
    return a[::-1] if JUEGO["al_reves"] else a

def pr(s, a):
    return Fraction(1, len(JUEGO["hijos"][s]))

# Generar un nodo es llamar a transicion: la cuenta lo anota.
CUENTA = dict(generados=["R"], total=0, evaluados=set(), terminadas=0)

def transicion(s, a):
    hijo = JUEGO["hijos"][s][a]
    CUENTA["generados"].append(hijo)
    CUENTA["total"] += 1
    return hijo

def evaluar(s):                          # EVAL: una estimación de s
    CUENTA["evaluados"].add(s)
    return EVAL_T[s]


# --- paso: la foto de una fila de la traza ---------------------------
VISIBLES = ("s", "a", "v", "w", "alfa", "beta", "mejor_valor",
            "mejor_jugada", "jugada", "d")
EVENTO_R = {"2": "inicio", "5": "inicio", "2–3": "antes", "4–5": "raiz",
            "7–10": "raiz", "6": "fin", "11–12": "fin", "13": "entrega"}

def paso(linea, variables, evento=None, **extra):
    """Una fila: la línea de la página y las variables en ese instante."""
    x = {k: variables[k] for k in VISIBLES if k in variables}
    if evento is None and x["s"] == "R":
        evento = EVENTO_R[linea]
    evento = evento or ("regresa" if "–" in linea else "entra")
    if evento == "inicio" and linea == "5":   # otra búsqueda: la cuenta
        CUENTA.update(generados=["R"], evaluados=set(),  # vuelve a R
                      total=CUENTA["total"] + 1)
    if evento == "fin":
        CUENTA["terminadas"] += 1          # para el reloj de la sección 7
    return dict(evento=evento, linea=linea, vars=x, t=JUEGO, **extra,
                generados=list(CUENTA["generados"]),
                evaluados=set(CUENTA["evaluados"]))

def corte(linea, variables):
    """La fila del corte y una fila ✗ por cada hijo que ya no se genera."""
    s, a = variables["s"], variables["a"]
    tipo = "beta" if pl(s) == "MAX" else "alfa"
    yield paso(linea, variables, "corte " + tipo)
    for b in acciones(s)[acciones(s).index(a) + 1:]:
        yield paso("", {"s": s}, "podado", nodo=JUEGO["hijos"][s][b],
                   corta=tipo)


# --- correr: de fotos a la tabla de la página ------------------------
CARGA = ("mejor_jugada", "jugada", "d", "alfa")

def camino(t, n):                        # la pila: de R hasta n
    return camino(t, t["padre"][n]) + [n] if n in t["padre"] else [n]

def fila_de(n, p, arriba):
    x, ev, t = p["vars"], p["evento"], p["t"]
    s = x["s"]
    f = dict(n=n, evento=ev, linea=p["linea"], nodo=p.get("nodo", s),
             pila=camino(t, s), v=x.get("v"), w=None, hijo=None,
             alfa=x.get("alfa"), beta=x.get("beta"), corta=p.get("corta"),
             hechos=p["generados"], evaluados=p["evaluados"], t=t)
    if s == "R":                         # en R: α de la raíz y β = +∞
        arriba.update({k: x[k] for k in CARGA if k in x})
        f["alfa"] = arriba.get("alfa")
        f["beta"] = None if f["alfa"] is None else inf
        f["v"] = x.get("mejor_valor", f["alfa"])
    if ev in ("regresa", "raiz", "corte beta", "corte alfa"):
        f.update(w=x["w"], hijo=t["hijos"][s][x["a"]])
        f["corta"] = ev.split()[1] if ev.startswith("corte") else None
    if ev == "podado":
        f["w"] = t["valor"].get(f["nodo"])
    return dict(f, **{k: arriba.get(k) for k in CARGA[:3]})

def correr(algoritmo):
    """Corre el generador. Devuelve (filas, lo que devolvió)."""
    CUENTA.update(generados=["R"], total=0, evaluados=set(), terminadas=0)
    pasos = []
    while True:
        try:
            pasos.append(next(algoritmo))
        except StopIteration as fin:
            resultado = fin.value
            break
    arriba = {}
    filas = [fila_de(n, p, arriba) for n, p in enumerate(pasos, 1)]
    return filas, resultado


# --- el estado de cada nodo, fila por fila ---------------------------
def bajo(t, n):                          # n y sus descendientes
    return [n] + [m for h in t["hijos"].get(n, {}).values()
                  for m in bajo(t, h)]

def recordar(f, m):
    t = f["t"]
    if f["evento"] in ("antes", "inicio"):     # empieza una búsqueda
        m.update(v={}, ab={}, dev={}, podados=set(), cotas=set())
    if f["evento"] != "podado":
        m["v"][f["nodo"]] = f["v"]
        m["ab"][f["nodo"]] = (f["alfa"], f["beta"])
    if f["hijo"] is not None:
        m["dev"][f["hijo"]] = f["w"]
    if f["evento"].startswith("corte"):
        fuera = [h for h in t["hijos"][f["nodo"]].values()
                 if h not in f["hechos"]]
        m["podados"].update(y for h in fuera for y in bajo(t, h))
        m["cotas"].update([f["nodo"]] if fuera else [])

def estado_de(n, f, m):
    e = dict(estado="pormirar", v=None, alfa=None, beta=None, cota=False)
    abiertos = () if f["evento"] in ("fin", "entrega") else f["pila"]
    valor = f["t"]["valor"]
    if n in abiertos:
        a, b = m["ab"].get(n, (None, None))
        e.update(estado="pila", v=m["v"].get(n), alfa=a, beta=b)
    elif n in f["hechos"]:
        v = valor[n] if n in valor else m["dev"].get(n, m["v"].get(n))
        ev = "evaluado" if n in f["evaluados"] else "devuelto"
        e.update(estado=ev, v=v, cota=n in m["cotas"])
    elif n in m["podados"]:
        e["estado"] = "podado"
    return e

def fotos_de(filas):
    m = {}
    return [recordar(f, m) or {n: estado_de(n, f, m) for n in f["t"]["prof"]}
            for f in filas]


# --- imprimir ---------------------------------------------------------
def fmt(x):
    return "" if x is None else {inf: "+∞", -inf: "−∞"}.get(x, str(x))

def renglon(f):
    """# · línea · pila · (α, β) · v · w · ¿corta? · mejor_jugada"""
    if f["evento"] == "podado":
        return (f"{f['n']:>2} ✗ {f['nodo']} ({fmt(f['w'])}) no se genera:"
                f" corte {f['corta']}")
    ab = "" if f["alfa"] is None else f"({fmt(f['alfa'])}, {fmt(f['beta'])})"
    w = fmt(f["w"]) + (f" ({f['hijo']})" if f["hijo"] and "-" not in
                       f["hijo"] else "")
    return (f"{f['n']:>2} │ {f['linea']:<5} │ {'›'.join(f['pila']):<8} │ "
            f"{ab:<9} │ v {fmt(f['v']):<4} │ w {w:<8} │ "
            f"{f['corta'] or '':<4} │ {f['mejor_jugada'] or 'ninguna'}"
            f" │ gen {len(f['hechos'])}")

def tabla(filas):
    for f in filas:
        print(renglon(f))


# --- el código, con ▶ en las líneas del paso -------------------------
def rango(linea):                        # «12–15» → [12, 13, 14, 15]
    a, _, b = linea.partition("–")
    return list(range(int(a), int(b or a) + 1)) if a else []

def marcas(fn):
    return {int(n) for n in re.findall(r"# \((\d+)\)",
                                       inspect.getsource(fn))}

def elegir(f, fuentes):                  # la función que hace ese paso
    ls = set(rango(f["linea"]))
    return max(fuentes, key=lambda g: len(marcas(g) & ls))

def con_flechas(fuente, ls):
    """Sin las fotos; un (n) vale para su línea y las que le siguen,
    hasta otro (n) o hasta salir de su bloque."""
    actual, base = None, 0
    for r in fuente.splitlines():
        if re.search(r"\b(paso|corte)\(", r):
            continue
        ind = len(r) - len(r.lstrip())
        m = re.search(r"# \((\d+)\)", r)
        if m:
            actual, base = int(m.group(1)), ind
        elif r.strip() and ind < base:
            actual = None
        yield ("▶ " if r.strip() and actual in ls else "  ") + r

def codigo(f, fuentes):
    fuente = inspect.getsource(elegir(f, fuentes))
    return "\n".join(con_flechas(fuente, rango(f["linea"])))

def posiciones(t):
    """(x, y) de cada nodo: hojas en fila; un padre, al centro."""
    pos, hojas = {}, iter(range(99))
    def colocar(n):
        xs = [colocar(h) for h in t["hijos"].get(n, {}).values()]
        xs = xs or [next(hojas)]
        pos[n] = (sum(xs) / len(xs), -t["prof"][n])
        return pos[n][0]
    colocar("R")
    return pos


usar(ARBOL_T)
print("reglas listas · árbol T")
''', "logica", "maquinaria", oculta=True)

code(r'''
# @title Visor: dibujo y deslizador (no hace falta leerla)
import matplotlib.pyplot as plt

try:
    from ipywidgets import (HBox, IntSlider, Play, VBox,
                            interactive_output, jslink)
    from IPython.display import display
    HAY_WIDGETS = True
except ImportError:                      # sin widgets: se imprime con un for
    HAY_WIDGETS = False

COLOR = {"pormirar": "#eeeeee", "pila": "#ffcf5c", "devuelto": "#8ecae6",
         "evaluado": "#a7d7a0", "podado": "#ffffff"}
MARCA = {"MAX": "^", "MIN": "v", "AZAR": "o", "HOJA": "s"}
LEYENDA = ("▲ MAX   ▼ MIN   ● azar   ■ hoja   ·   gris: sin generar   ·   "
           "amarillo: en la pila   ·   azul: devuelto\n"
           "verde: EVAL (una estimación)   ·   punteado con ?: podado   ·   "
           "«cota»: hubo corte; lo devuelto puede no ser su valor")


def tipo(t, n):
    if n in t["valor"]:
        return "HOJA"
    return "AZAR" if n in t["azar"] else ("MAX", "MIN")[t["prof"][n] % 2]


def nodo(ax, n, x, y, e, t):
    k, est = tipo(t, n), e["estado"]
    pila = est == "pila"
    ax.scatter(x, y, s=1300, marker=MARCA[k], c=COLOR[est], zorder=2,
               edgecolors="#d1495b" if pila else "#444",
               linewidths=3 if pila else 1.2,
               linestyle="--" if est == "podado" else "-")
    txt = "?" if est == "podado" else fmt(t["valor"].get(n, e["v"]))
    ax.text(x, y + {"^": -.06, "v": .06}.get(MARCA[k], 0), txt, zorder=3,
            ha="center", va="center", fontsize=10, weight="bold",
            color="#999" if est == "pormirar" else "#111")
    if k != "HOJA":
        ax.text(x, y + .4, n, ha="center", fontsize=9, color="#333")
    if e["alfa"] is not None and pila:
        ax.text(x + .3, y, f"({fmt(e['alfa'])}, {fmt(e['beta'])})",
                fontsize=9, color="#d1495b", va="center")
    if e["cota"]:
        ax.text(x, y - .42, "cota", ha="center", fontsize=8, c="#d1495b")


def dibujar(foto, t, ax, titulo=""):
    pos = posiciones(t)
    for p, hs in t["hijos"].items():
        for h in hs.values():
            ls = ":" if foto[h]["estado"] == "podado" else "-"
            ax.plot(*zip(pos[p], pos[h]), ls=ls, c="#888", zorder=1)
    for n, (x, y) in pos.items():
        nodo(ax, n, x, y, foto[n], t)
    ax.set_ylim(min(y for _, y in pos.values()) - .55, .8)
    ax.set_title(titulo, loc="left", fontsize=10)
    ax.axis("off")


def figura():
    fig, ax = plt.subplots(figsize=(9, 4.8))
    fig.text(.01, .01, LEYENDA, fontsize=8, color="#555")
    return fig, ax


def ver_arbol(t):
    vacio = dict(estado="pormirar", v=None, alfa=None, beta=None, cota=False)
    fig, ax = figura()
    dibujar({n: vacio for n in t["prof"]}, t, ax, "el árbol T")
    plt.show()


def mostrar(filas, fotos, fuentes, k):
    f = filas[k - 1]
    fig, ax = figura()
    titulo = (f"paso {k} de {len(filas)} · línea {f['linea'] or '—'} · "
              f"generados {len(f['hechos'])}/{len(f['t']['prof'])} · "
              f"pila {' › '.join(f['pila'])}")
    dibujar(fotos[k - 1], f["t"], ax, titulo)
    plt.show()
    print(renglon(f), "\n")
    print(codigo(f, fuentes) if f["linea"] else "(fila ✗: no corre nada)")


def ver(filas, *fuentes):
    """El deslizador de pasos; sin widgets, todos los pasos con un for."""
    fotos = fotos_de(filas)
    if not HAY_WIDGETS:
        tabla(filas)
        return mostrar(filas, fotos, fuentes, len(filas))
    barra = IntSlider(value=1, min=1, max=len(filas), description="paso")
    play = Play(value=1, min=1, max=len(filas), interval=1800)
    jslink((play, "value"), (barra, "value"))
    vista = interactive_output(
        lambda k: mostrar(filas, fotos, fuentes, k), {"k": barra})
    display(VBox([HBox([play, barra]), vista]))


def lupa(filas, k, *fuentes):            # un solo paso, fijo
    mostrar(filas, fotos_de(filas), fuentes, k)


print("visor listo · widgets:", HAY_WIDGETS)
''', "maquinaria", oculta=True)

# ================================================================ 2 ===
md("""
## 2 · El árbol T

R es la raíz; mueve MAX. Sus jugadas `izq`, `centro` y `der` llevan a I, C
y D. De C salen `c1` y `c2` a C1 y C2. Los números son finales: su $U$.
""")

code("""
usar(ARBOL_T)
ver_arbol(JUEGO)
print("A(R) =", acciones("R"), "· A(C) =", acciones("C"))
print("T(C, c2) =", transicion("C", "c2"), "· Pl(C2) =", pl("C2"))
""")

md("""
**Pregunta.** ¿Quién mueve en cada nivel? (▲ es MAX, ▼ es MIN.)

<details><summary>Respuesta</summary>

R mueve MAX; en I, C y D mueve MIN; en C1 y C2 otra vez MAX. Los turnos
alternan. Las hojas son finales: nadie mueve.

</details>

**Cómo leer el código.** Es el Python de la página. Dos añadidos:
`yield paso("12–13", locals())` toma una foto de las variables en esa fila
de la tabla, y `yield from` deja pasar las fotos de los hijos. En alfa-beta,
`yield from corte(...)` es la foto del corte y de cada hijo que ya no se
genera.
""")

# ================================================================ 3 ===
md("""
## 3 · Minimax

MAX se queda con el mayor $w$ de sus hijos; MIN, con el menor. La raíz no
devuelve un valor: devuelve **la jugada**.
""")

algoritmo_de("minimax", "decidir_minimax")

algoritmo_de("minimax", "minimax")

code("""
usar(ARBOL_T)
filas_mm, jugada = correr(decidir_minimax("R"))
print("jugada:", jugada, "· generados:", len(filas_mm[-1]["hechos"]), "de 14")
ver(filas_mm, decidir_minimax, minimax)
""")

md("""
**Pruébalo.** Cambia la primera hoja de D, el 2, por un 9, y corre.

<details><summary>Qué pasa</summary>

D vale $\\min(9, 12) = 9$, más que el 5 de C: sale `der`. Una sola hoja
cambió la jugada, porque minimax mira todo.

</details>
""")

code("""
prueba = ((3, 6), ((5, 2), (7, 8)), (2, 12))     # cambia un número
usar(prueba)
print("jugada:", correr(decidir_minimax("R"))[1])
""")

# ================================================================ 4 ===
md("""
## 4 · Cuando decide un dado: expectiminimax

Ahora I, C y D son **volados parejos**: cada hijo sale con probabilidad ½.
Un nodo de azar no elige: suma `Pr · w` de todos sus hijos. La tabla sigue
solo a los nodos de azar; C1 y C2 se valoran por dentro, sin filas.
""")

algoritmo_de("azar", "decidir_expectiminimax")

algoritmo_de("azar", "expectiminimax")

code("""
usar(ARBOL_T, azar=("I", "C", "D"))
filas_az, jugada = correr(decidir_expectiminimax("R"))
for f in filas_az:
    if f["evento"] == "raiz":
        print(f"{f['hijo']} vale {fmt(f['w'])}")
print("jugada:", jugada, "  (minimax decía centro)")
ver(filas_az, decidir_expectiminimax, expectiminimax)
""")

md("""
**Pruébalo.** Cambia el 12 de D por un 4: ¿sigue ganando `der`?

<details><summary>Qué pasa</summary>

D vale $\\tfrac12\\cdot 2 + \\tfrac12\\cdot 4 = 3$, menos que $13/2$: gana
`centro`. Con azar cuenta cada hoja, no solo la peor.

</details>
""")

code("""
prueba = ((3, 6), ((5, 2), (7, 8)), (2, 12))     # cambia el 12
usar(prueba, azar=("I", "C", "D"))
print("jugada:", correr(decidir_expectiminimax("R"))[1])
""")

# ================================================================ 5 ===
md("""
## 5 · Alfa-beta

- **α**: lo que MAX ya tiene asegurado en el camino. Solo sube.
- **β**: lo que MIN ya tiene asegurado en el camino. Solo baja.

La regla: **MAX compara v ≥ β; MIN compara v ≤ α**. Cada uno mira el número
del rival, que heredó de arriba. Si se cumple, corta: el rival nunca
dejaría llegar la partida ahí.
""")

algoritmo_de("alfa-beta", "decidir_alfa_beta")

algoritmo_de("alfa-beta", "alfa_beta")

code("""
AB = (decidir_alfa_beta, alfa_beta)
usar(ARBOL_T1)                           # T sin el centro: 6 de 7
filas_t1, jugada = correr(decidir_alfa_beta("R"))
print("T1:", jugada, "·", len(filas_t1[-1]["hechos"]), "de 7 nodos")
ver(filas_t1, *AB)
""")

md("""
Ahora T: 12 de 14. Minimax generaba los 14; la jugada es la misma.
""")

code("""
usar(ARBOL_T)
filas_ab, jugada = correr(decidir_alfa_beta("R"))
print("T:", jugada, "·", len(filas_ab[-1]["hechos"]), "de 14 nodos")
ver(filas_ab, *AB)
""")

md("""
**Dos lupas.** En C2 (MAX): recibe 7, y $7 \\ge \\beta = 5$. C ya tiene 5 y
nunca escogería algo que vale 7 o más: la hoja 8 no se genera. C2
**devuelve 7 aunque vale 8**: es una cota, «al menos 7», no su valor.

En D (MIN): recibe 2, y $2 \\le \\alpha = 5$. R ya tiene 5 con `centro`, y
D vale a lo más 2: la hoja 12 no se genera.
""")

code("""
for corte_ in ("corte beta", "corte alfa"):
    k = next(f["n"] for f in filas_ab if f["evento"] == corte_)
    lupa(filas_ab, k, *AB)
""")

md("""
**Pruébalo.** Cambia el 7 de C2 por un 4: ¿cuántos nodos genera ahora?

<details><summary>Qué pasa</summary>

13. C2 ya no corta en su primera hoja ($4 < \\beta = 5$), así que genera
el 8; ahí $8 \\ge 5$, pero ya no quedan hijos. C sigue valiendo 5 y la
jugada sigue siendo `centro`.

</details>

El ejercicio «Llena la traza con el orden invertido», de la página
*Alfa-beta como algoritmo*, resuélvelo primero a mano. Después revísalo con
`usar(ARBOL_T, al_reves=True)` y `ver(correr(decidir_alfa_beta("R"))[0], *AB)`.
""")

code("""
prueba = ((3, 6), ((5, 2), (7, 8)), (2, 12))     # cambia el 7
usar(prueba)
filas, jugada = correr(decidir_alfa_beta("R"))
print("jugada:", jugada, "·", len(filas[-1]["hechos"]), "nodos")
""")

# ================================================================ 6 ===
md("""
## 6 · Minimax con corte

Si el árbol no cabe, se mira solo `d` jugadas adelante; donde se acaba el
horizonte, el nodo vale `EVAL(s)`, una estimación. Desde aquí el árbol usa
la escala de la clase 3: la hoja 3 es un final con $U = 3/100$, y la línea
8 devuelve $100 \\cdot U = 3$.
""")

algoritmo_de("corte", "decidir_con_corte")

algoritmo_de("corte", "minimax_con_corte")

code("""
usar(ARBOL_T, cien=True)
for d in (1, 2, 3):
    filas, jugada = correr(decidir_con_corte("R", d))
    print(f"d = {d}: {jugada:<6} con {fmt(filas[-1]['v'])},",
          f"{len(filas[-1]['hechos'])} nodos generados")
filas_c2, _ = correr(decidir_con_corte("R", 2))
ver(filas_c2, decidir_con_corte, minimax_con_corte)
""")

md("""
Con `d = 1` cae en una trampa: `der` parece valer 7, pero D vale 2. Con
`d = 2` ya ve la respuesta de MIN. En la figura, verde es `EVAL`.

**Pruébalo.** Con `d = 1`, sube `EVAL_T["C"]` a 8: ¿qué jugada sale?

<details><summary>Qué pasa</summary>

`centro`, con 8. Con el horizonte tan corto, la jugada la decide la
estimación, no el juego.

</details>
""")

code("""
EVAL_T["C"] = 4                          # cambia el 4
usar(ARBOL_T, cien=True)
print("d = 1:", correr(decidir_con_corte("R", 1))[1])
EVAL_T["C"] = 4                          # el de la página
""")

# ================================================================ 7 ===
md("""
## 7 · Profundización iterativa: jugar contra el reloj

No sabes cuánto tiempo queda. Busca con `d = 1`, luego `d = 2`, `d = 3`…
y entrega la jugada de **la última búsqueda completa**. La jugada anterior
va primero: α sube pronto y se poda más. Debajo de R corre el alfa-beta de
la sección 5, con `d`. Un 100 es $100\cdot U$ con $U = 1$: una victoria
segura (línea 9).
""")

algoritmo_de("iterativa", "alfa_beta_con_corte")

md("""
El reloj es una función, `queda_tiempo()`. El de la página alcanza justo
para tres búsquedas completas. Con `RELOJ["nodos"] = N`, el tiempo se acaba
al generar el nodo N; R lo revisa cada vez que vuelve un hijo (línea 8).
""")

code("""
RELOJ = {"nodos": None}                  # None: el reloj de la página

def queda_tiempo():
    if RELOJ["nodos"] is None:
        return CUENTA["terminadas"] < 3  # tres búsquedas completas
    return CUENTA["total"] < RELOJ["nodos"]
""", "logica")

algoritmo_de("iterativa", "profundizacion_iterativa")

code("""
usar(ARBOL_T, cien=True)
RELOJ["nodos"] = None
filas_pi, jugada = correr(profundizacion_iterativa("R"))
for f in filas_pi:
    if f["evento"] == "fin":
        print(f"d = {f['d']}: deja lista {f['jugada']:<6}",
              f"({len(f['hechos'])} nodos)")
print("se entrega:", jugada)
ver(filas_pi, profundizacion_iterativa, alfa_beta_con_corte)
""")

md("""
**El reloj de N nodos.** ¿Qué jugada se entrega si el tiempo se acaba al
generar el nodo N, contando todas las búsquedas?
""")

code("""
antes = None
for n in range(1, 27):
    RELOJ["nodos"] = n
    jugada = correr(profundizacion_iterativa("R"))[1]
    if jugada != antes:
        print(f"desde N = {n:>2}: se entrega {jugada}")
        antes = jugada
RELOJ["nodos"] = None
""")

md("""
**Pruébalo.** Con un reloj de 12 nodos se entrega `der`, aunque la
búsqueda con `d = 2` ya había visto que `centro` vale más. ¿Por qué?

<details><summary>Respuesta</summary>

Porque esa búsqueda no terminó. Una búsqueda a medias puede no haber visto
la respuesta que deshace su jugada; se entrega la de la última búsqueda
completa, la de `d = 1`.

</details>
""")

# ================================================================ 8 ===
md("""
## 8 · Cierre

| algoritmo | jugada | nodos generados |
|---|---|---|
| minimax | centro (5) | 14 de 14 |
| expectiminimax (I, C, D de azar) | der (7) | 14 de 14 |
| alfa-beta en T1 / en T | izq (3) / centro (5) | 6 de 7 / 12 de 14 |
| con corte, d = 1, 2, 3 | der, centro, centro | 4, 10, 14 |
| profundización iterativa | centro | 4 + 10 + 11 |

La celda de abajo vuelve a calcular toda la tabla.
""")

code("""
def resumen(nombre, algoritmo, arbol=ARBOL_T, **reglas):
    usar(arbol, **reglas)
    filas, jugada = correr(algoritmo())
    fines = [f for f in filas if f["evento"] == "fin"]
    nodos = " + ".join(str(len(f["hechos"])) for f in fines)
    print(f"{nombre:<14} {jugada:<7} {nodos} nodos")
resumen("minimax", lambda: decidir_minimax("R"))
resumen("azar", lambda: decidir_expectiminimax("R"), azar="ICD")
resumen("alfa-beta T1", lambda: decidir_alfa_beta("R"), ARBOL_T1)
resumen("alfa-beta T", lambda: decidir_alfa_beta("R"))
for d in (1, 2, 3):
    resumen(f"corte d = {d}", lambda: decidir_con_corte("R", d), cien=True)
resumen("iterativa", lambda: profundizacion_iterativa("R"), cien=True)
usar(ARBOL_T)
""")

md("""
**Tres preguntas.**

1. ¿Por qué alfa-beta da la misma jugada que minimax aunque genere menos?
2. ¿Por qué expectiminimax elige `der` si minimax elige `centro`?
3. ¿Qué entrega la profundización iterativa si el reloj se acaba a mitad
   de `d = 3`?

<details><summary>Respuestas</summary>

1. Solo deja de mirar lo que no puede cambiar la decisión: un nodo podado
   está fuera de la ventana (α, β), y su padre ya tiene algo mejor.
2. Con azar, D ya no es «la peor hoja», sino el promedio: $(2 + 12)/2 = 7$.
3. `centro`, la jugada que dejó lista `d = 2`. La de `d = 3` está a medias.

</details>
""")


def contenido():
    """El .ipynb como texto: nbformat 4, sin salidas."""
    celdas = []
    for c in CELDAS:
        lineas = c["source"].split("\n")
        fuente = [r + "\n" for r in lineas[:-1]] + [lineas[-1]]
        celdas.append(dict(c, source=fuente))
    nb = {"cells": celdas,
          "metadata": {"colab": {"provenance": [], "toc_visible": True},
                       "kernelspec": {"display_name": "Python 3",
                                      "name": "python3"},
                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 0}
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


def main(argv):
    destino = RAIZ / RUTA
    destino.write_text(contenido(), encoding="utf-8")
    print(f"escrito {destino.relative_to(RAIZ)}: {len(CELDAS)} celdas")


if __name__ == "__main__":
    main(sys.argv)
