"""Calculos exactos de la unidad de juegos (unidad 7).

Unica fuente de los numeros que citan las paginas de course/7_juegos/. Cada
funcion calcula por fuerza bruta o con aritmetica exacta de fracciones; nada
se copia a mano. test_juegos.py comprueba que los numeros que la prosa cita
siguen saliendo de aqui.

Convenciones de hexapawn (las mismas que la bitacora de la clase 1):

- Tablero de n x n guardado como cadena de n*n caracteres. El indice
  i = (fila - 1) * n + columna; la fila 1 es la de salida de Blancas.
- 'B' es un peon blanco, 'N' uno negro y '.' una casilla vacia.
- Blancas avanzan hacia filas mayores y empiezan la partida.
- Gana quien llega a la fila contraria, quien captura todos los peones
  rivales, o quien deja al rival sin jugada en su turno.
- Las utilidades se miden siempre en puntos de Blancas (MAX).
- Orden de las jugadas: por casilla de origen (a1, b1, ..., luego fila 2...),
  y para cada peon: avanzar, capturar a la izquierda, capturar a la derecha.
"""
from array import array
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import copy
import math
import random
import re
import statistics

COLUMNAS = "abcdefgh"


# --------------------------------------------------------------- hexapawn ---

def inicio(n=3):
    return "B" * n + "." * (n * (n - 2)) + "N" * n


def otro(jugador):
    return "N" if jugador == "B" else "B"


def casilla(i, n=3):
    return COLUMNAS[i % n] + str(i // n + 1)


def jugadas(tablero, jugador, n=3):
    """Lista de (origen, destino) en el orden fijo descrito arriba."""
    paso = 1 if jugador == "B" else -1
    rival = otro(jugador)
    lista = []
    for i, pieza in enumerate(tablero):
        if pieza != jugador:
            continue
        fila, col = divmod(i, n)
        fila2 = fila + paso
        if not 0 <= fila2 < n:
            continue
        frente = fila2 * n + col
        if tablero[frente] == ".":
            lista.append((i, frente))
        for dc in (-1, 1):
            col2 = col + dc
            if 0 <= col2 < n and tablero[fila2 * n + col2] == rival:
                lista.append((i, fila2 * n + col2))
    return lista


def mover(tablero, jugada):
    origen, destino = jugada
    t = list(tablero)
    t[destino], t[origen] = t[origen], "."
    return "".join(t)


def nombre_jugada(tablero, jugada, n=3):
    origen, destino = jugada
    signo = "x" if tablero[destino] != "." else "-"
    return casilla(origen, n) + signo + casilla(destino, n)


def ganador(tablero, turno, n=3, sin_jugada_empata=False):
    """'B', 'N', 'empate' o None si la partida sigue. `turno` es quien mueve."""
    if "B" in tablero[n * (n - 1):]:
        return "B"
    if "N" in tablero[:n]:
        return "N"
    if "N" not in tablero:
        return "B"
    if "B" not in tablero:
        return "N"
    if not jugadas(tablero, turno, n):
        return "empate" if sin_jugada_empata else otro(turno)
    return None


def utilidad_simple(g, k):
    """+1 si ganan Blancas, -1 si ganan Negras, 0 si empatan."""
    return {"B": 1, "N": -1, "empate": 0}[g]


def valor(tablero, turno, k=0, n=3, util=utilidad_simple,
          sin_jugada_empata=False):
    """Valor minimax exacto, en puntos de Blancas."""
    @lru_cache(maxsize=None)
    def v(t, j, kk):
        g = ganador(t, j, n, sin_jugada_empata)
        if g:
            return util(g, kk)
        hijos = [v(mover(t, m), otro(j), kk + 1) for m in jugadas(t, j, n)]
        return max(hijos) if j == "B" else min(hijos)
    return v(tablero, turno, k)


def valor_con_premio_por_captura(tablero, turno, premio, n=3):
    """Valor de cada jugada de Blancas con una utilidad mal escrita: la del
    reglamento mas `premio` por cada peon que captura Blancas. Negras minimiza
    esa misma utilidad. Devuelve {nombre de la jugada: valor}."""
    @lru_cache(maxsize=None)
    def v(t, j, capturas):
        g = ganador(t, j, n)
        if g:
            return utilidad_simple(g, 0) + premio * capturas
        hijos = [v(mover(t, m), otro(j),
                   capturas + (j == "B" and t[m[1]] != "."))
                 for m in jugadas(t, j, n)]
        return max(hijos) if j == "B" else min(hijos)
    return {nombre_jugada(tablero, m, n):
            v(mover(tablero, m), otro(turno), int(tablero[m[1]] != "."))
            for m in jugadas(tablero, turno, n)}


def contar_arbol(tablero=None, turno="B", n=3, sin_jugada_empata=False):
    """(nodos del arbol, situaciones distintas). Una situacion es (tablero, turno)."""
    tablero = tablero or inicio(n)
    situaciones = set()

    @lru_cache(maxsize=None)
    def nodos(t, j):
        situaciones.add((t, j))
        if ganador(t, j, n, sin_jugada_empata):
            return 1
        return 1 + sum(nodos(mover(t, m), otro(j)) for m in jugadas(t, j, n))
    total = nodos(tablero, turno)
    return total, len(situaciones)


def partida_mas_larga(tablero=None, turno="B", n=3):
    tablero = tablero or inicio(n)

    @lru_cache(maxsize=None)
    def largo(t, j):
        if ganador(t, j, n):
            return 0
        return 1 + max(largo(mover(t, m), otro(j)) for m in jugadas(t, j, n))
    return largo(tablero, turno)


def tableros_con_dos_turnos(n=3):
    """Tableros alcanzables tanto con Blancas como con Negras al turno."""
    vistos = set()
    pila = [(inicio(n), "B")]
    while pila:
        t, j = pila.pop()
        if (t, j) in vistos:
            continue
        vistos.add((t, j))
        if ganador(t, j, n):
            continue
        for m in jugadas(t, j, n):
            pila.append((mover(t, m), otro(j)))
    return sorted({t for t, j in vistos if (t, otro(j)) in vistos})


def tableros_con_dos_contadores(n=3):
    """Tableros alcanzables con dos valores distintos de k (jugadas hechas)."""
    vistos = set()
    pila = [(inicio(n), "B", 0)]
    while pila:
        t, j, k = pila.pop()
        if (t, j, k) in vistos:
            continue
        vistos.add((t, j, k))
        if ganador(t, j, n):
            continue
        for m in jugadas(t, j, n):
            pila.append((mover(t, m), otro(j), k + 1))
    ks = {}
    for t, j, k in vistos:
        ks.setdefault(t, set()).add(k)
    return sorted(t for t, v in ks.items() if len(v) > 1)


def contar_estados(n=3, sin_jugada_empata=False):
    """Cuenta estados por clase: no finales por turno y finales por motivo."""
    vistos = set()
    pila = [(inicio(n), "B")]
    cuenta = {"B": 0, "N": 0, "final": 0, "final_sin_jugada": 0}
    while pila:
        t, j = pila.pop()
        if (t, j) in vistos:
            continue
        vistos.add((t, j))
        if ganador(t, j, n, sin_jugada_empata):
            cuenta["final"] += 1
            llego = "B" in t[n * (n - 1):] or "N" in t[:n]
            capturo = "B" not in t or "N" not in t
            if not llego and not capturo:
                cuenta["final_sin_jugada"] += 1
            continue
        cuenta[j] += 1
        for m in jugadas(t, j, n):
            pila.append((mover(t, m), otro(j)))
    return cuenta


def alfa_beta_traza(tablero, turno, n=3, invertir=False, sin_jugada_empata=False,
                    alfa=float("-inf"), beta=float("inf"), estricto=False):
    """Alfa-beta con utilidad +1/-1 (0 si empatan), anotando cada visita.

    Es el pseudocodigo de la pagina «Alfa-beta como algoritmo», linea por
    linea: corte beta si v >= beta en un nodo de MAX, corte alfa si v <= alfa
    en uno de MIN, y el nodo devuelve v (una cota si hubo corte).

    Devuelve un dict con:
    - valor: lo que devuelve la raiz;
    - visitas: en orden, (camino, tipo, alfa al llegar, beta al llegar,
      devuelve). El camino es la tupla de nombres de jugada desde la raiz y el
      tipo es "MAX", "MIN" o "final";
    - cortes: (tipo, camino del nodo que corta, jugada tras la que corta,
      hermanos que no se visitan). Solo cuentan los cortes que dejan hermanos
      sin visitar.
    """
    visitas, cortes = [], []

    def ab(t, j, a, b, camino):
        fila = len(visitas)
        visitas.append(None)
        g = ganador(t, j, n, sin_jugada_empata)
        if g:
            u = utilidad_simple(g, 0)
            visitas[fila] = (camino, "final", a, b, u)
            return u
        tipo = "MAX" if j == "B" else "MIN"
        a0, b0 = a, b
        lista = jugadas(t, j, n)
        if invertir:
            lista = lista[::-1]
        v = float("-inf") if j == "B" else float("inf")
        for idx, m in enumerate(lista):
            nombre = nombre_jugada(t, m, n)
            h = ab(mover(t, m), otro(j), a, b, camino + (nombre,))
            quedan = len(lista) - idx - 1
            if j == "B":
                v = max(v, h)
                if v > b or (v == b and not estricto):
                    if quedan:
                        cortes.append(("beta", camino, nombre, quedan))
                    break
                a = max(a, v)
            else:
                v = min(v, h)
                if v < a or (v == a and not estricto):
                    if quedan:
                        cortes.append(("alfa", camino, nombre, quedan))
                    break
                b = min(b, v)
        visitas[fila] = (camino, tipo, a0, b0, v)
        return v

    v = ab(tablero, turno, alfa, beta, ())
    return {"valor": v, "visitas": visitas, "cortes": cortes}


def alfa_beta(tablero, turno, n=3, invertir=False, sin_jugada_empata=False,
              alfa=float("-inf"), beta=float("inf"), estricto=False):
    """(valor, nodos visitados, cortes como (tipo, jugada, hermanos sin visitar))."""
    r = alfa_beta_traza(tablero, turno, n, invertir, sin_jugada_empata, alfa, beta,
                        estricto)
    return (r["valor"], len(r["visitas"]),
            [(tipo, jugada, quedan) for tipo, _, jugada, quedan in r["cortes"]])


# -------------------------------------- alfa-beta sobre un arbol generico ---
#
# El arbol de juguete de la clase 2 (el «arbol T») no es hexapawn: es una
# tupla anidada. Una hoja es un numero; un nodo interno, la tupla de sus hijos
# en el orden dado. Los niveles alternan MAX y MIN a partir de la raiz.

# Arbol T, etapa 1: R (MAX) con dos hijos MIN, I por «izq» y D por «der».
# Minimax: R = 3, juega izq. Alfa-beta poda la hoja 12 (corte alfa en D).
ARBOL_T1 = ((3, 6), (2, 12))
# Arbol T, etapa 2: se agrega C (MIN) por «centro», en medio, con dos hijos
# MAX, C1 y C2 (jugadas c1 y c2). Minimax: R = 5, juega centro. Alfa-beta
# poda la hoja 8 (corte beta en C2) y la hoja 12 (corte alfa en D).
ARBOL_T = ((3, 6), ((5, 2), (7, 8)), (2, 12))
# La EVAL de «Minimax con corte» para los nodos internos de T.
EVAL_T = {"I": 5, "C": 4, "D": 7, "C1": 6, "C2": 9}


def invertir_arbol(arbol):
    """El mismo arbol con cada lista de hijos al reves."""
    if not isinstance(arbol, tuple):
        return arbol
    return tuple(invertir_arbol(h) for h in reversed(arbol))


def contar_nodos(arbol):
    if not isinstance(arbol, tuple):
        return 1
    return 1 + sum(contar_nodos(h) for h in arbol)


def alfa_beta_arbol(arbol, es_max=True, alfa=float("-inf"), beta=float("inf"),
                    invertir=False, estricto=False):
    """Alfa-beta fail-soft sobre un arbol de tuplas anidadas.

    Las mismas lineas que alfa_beta_traza: corte beta si v >= beta en un nodo
    de MAX, corte alfa si v <= alfa en uno de MIN (sin el igual si
    `estricto`), y el nodo devuelve v, que es una cota si hubo corte.

    Los caminos son tuplas de indices en el orden *dado* del arbol, aunque se
    recorra invertido, para que un mismo nodo se llame igual en los dos
    recorridos. Devuelve un dict con:
    - valor: lo que devuelve la raiz;
    - generados: cuantos nodos se generan (hojas incluidas);
    - traza: en orden de visita, (camino, tipo, alfa al llegar, beta al
      llegar, v devuelto, corte), con tipo "MAX", "MIN" u "hoja" y corte
      "alfa", "beta" o None. Solo cuenta el corte que deja hermanos sin
      generar;
    - podados: los caminos de las raices de los subarboles que no se generan.
    """
    traza, podados = [], []

    def ab(nodo, maximiza, a, b, camino):
        fila = len(traza)
        traza.append(None)
        if not isinstance(nodo, tuple):
            traza[fila] = (camino, "hoja", a, b, nodo, None)
            return nodo
        a0, b0 = a, b
        indices = list(range(len(nodo)))
        if invertir:
            indices.reverse()
        v = float("-inf") if maximiza else float("inf")
        corte = None
        for k, i in enumerate(indices):
            h = ab(nodo[i], not maximiza, a, b, camino + (i,))
            quedan = indices[k + 1:]
            if maximiza:
                v = max(v, h)
                if v > b or (v == b and not estricto):
                    corte = "beta" if quedan else None
                    break
                a = max(a, v)
            else:
                v = min(v, h)
                if v < a or (v == a and not estricto):
                    corte = "alfa" if quedan else None
                    break
                b = min(b, v)
        else:
            quedan = []
        podados.extend(camino + (i,) for i in quedan)
        traza[fila] = (camino, "MAX" if maximiza else "MIN", a0, b0, v, corte)
        return v

    v = ab(arbol, es_max, alfa, beta, ())
    return {"valor": v, "generados": len(traza), "traza": traza, "podados": podados}


def minimax_arbol(arbol, es_max=True):
    """El valor exacto de un nodo del arbol generico."""
    if not isinstance(arbol, tuple):
        return arbol
    hijos = [minimax_arbol(h, not es_max) for h in arbol]
    return max(hijos) if es_max else min(hijos)


# ------------------------------------------- el arbol T, linea por linea ---
#
# Las paginas de la clase 2 trazan DECIDIR-MINIMAX y DECIDIR-ALFA-BETA sobre
# el arbol T con el pseudocodigo de abajo (numeracion fija, la misma en todas
# las paginas) y las figuras jue-t-* dibujan esa misma traza. Las dos leen de
# traza_decidir: una fila al entrar a un nodo interno y una cada vez que un
# hijo regresa a su padre; las hojas se pliegan en la celda w.

PSEUDO_MINIMAX = {
    1: "function DECIDIR-MINIMAX(s)",
    2: "mejor_valor ← −∞ ; mejor_jugada ← ninguna",
    3: "for each a in A(s)",
    4: "w ← MINIMAX(T(s, a))",
    5: "if w > mejor_valor: mejor_valor ← w ; mejor_jugada ← a",
    6: "return mejor_jugada",
    7: "function MINIMAX(s)",
    8: "if s ∈ S_F: return U(s)",
    9: "if Pl(s) = MAX",
    10: "v ← −∞",
    11: "for each a in A(s)",
    12: "w ← MINIMAX(T(s, a))",
    13: "v ← max(v, w)",
    14: "return v",
    15: "else",
    16: "v ← +∞",
    17: "for each a in A(s)",
    18: "w ← MINIMAX(T(s, a))",
    19: "v ← min(v, w)",
    20: "return v",
}

PSEUDO_ALFA_BETA = {
    1: "function DECIDIR-ALFA-BETA(s)",
    2: "α ← −∞ ; mejor_jugada ← ninguna",
    3: "for each a in A(s)",
    4: "w ← ALFA-BETA(T(s, a), α, +∞)",
    5: "if w > α: α ← w ; mejor_jugada ← a",
    6: "return mejor_jugada",
    7: "function ALFA-BETA(s, α, β)",
    8: "if s ∈ S_F: return U(s)",
    9: "if Pl(s) = MAX",
    10: "v ← −∞",
    11: "for each a in A(s)",
    12: "w ← ALFA-BETA(T(s, a), α, β)",
    13: "v ← max(v, w)",
    14: "if v ≥ β: return v",
    15: "α ← max(α, v)",
    16: "return v",
    17: "else",
    18: "v ← +∞",
    19: "for each a in A(s)",
    20: "w ← ALFA-BETA(T(s, a), α, β)",
    21: "v ← min(v, w)",
    22: "if v ≤ α: return v",
    23: "β ← min(β, v)",
    24: "return v",
}

# La linea (o el tramo de lineas) que resume cada fila de la traza.
LINEAS_MINIMAX = {"inicio": "2", "raiz": "4–5", "fin": "6",
                  "entra_MAX": "10", "entra_MIN": "16",
                  "regresa_MAX": "12–13", "regresa_MIN": "18–19"}
LINEAS_ALFA_BETA = {"inicio": "2", "raiz": "4–5", "fin": "6",
                    "entra_MAX": "10", "entra_MIN": "18",
                    "regresa_MAX": "12–15", "regresa_MIN": "20–23",
                    "corta_MAX": "12–14", "corta_MIN": "20–22"}

INF = float("inf")


def nombres_t(arbol):
    """{camino: (nombre, jugada que lleva ahi)} para el arbol T o T1.

    La raiz es R; sus hijos, I, C y D por izq, centro y der (en T1 solo I y
    D); los hijos internos de C, C1 y C2 por c1 y c2. Una hoja se llama por
    su numero y la jugada que lleva a ella no tiene nombre."""
    jugadas_raiz = {2: ("izq", "der"), 3: ("izq", "centro", "der")}[len(arbol)]
    res = {(): ("R", None)}

    def visitar(nodo, camino, nombre):
        if not isinstance(nodo, tuple):
            return
        for i, hijo in enumerate(nodo):
            c = camino + (i,)
            if not isinstance(hijo, tuple):
                res[c] = (str(hijo), None)
            elif camino == ():
                jugada = jugadas_raiz[i]
                res[c] = ({"izq": "I", "centro": "C", "der": "D"}[jugada], jugada)
            else:
                res[c] = (f"{nombre}{i + 1}", f"{nombre.lower()}{i + 1}")
            visitar(hijo, c, res[c][0])
    visitar(arbol, (), "R")
    return res


def nodo_en(arbol, camino):
    for i in camino:
        arbol = arbol[i]
    return arbol


def fmt_t(x):
    """Un numero de las trazas de T: ±∞, fracciones como 13/2, enteros sin signo."""
    if x is None:
        return ""
    if x == INF:
        return "+∞"
    if x == -INF:
        return "−∞"
    if isinstance(x, F):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)


def traza_decidir(arbol=ARBOL_T, poda=False, orden=None, profundidad=None,
                  evaluar=None, lineas=None):
    """DECIDIR-MINIMAX (poda=False) o DECIDIR-ALFA-BETA (poda=True) sobre un
    arbol de tuplas con raiz MAX, fila por fila.

    - orden: {nombre de nodo: [nombres de sus hijos en el orden de visita]}
      para cambiar el orden de algunos nodos (los demas, el dado).
    - profundidad: si se da, corte por profundidad (la raiz esta a 0); un nodo
      interno a esa profundidad no se expande y vale evaluar[nombre].
    - lineas: {evento: linea}, para otra numeracion (por omision, la
      canonica: LINEAS_MINIMAX o LINEAS_ALFA_BETA).

    Devuelve un dict con:
    - filas: lista de dicts con n, evento ('inicio', 'entra', 'regresa',
      'raiz', 'fin'), linea, pila (tupla de nombres hasta el nodo de la
      fila), nodo, v, w, hijo (quien devolvio w), evaluado (si w es EVAL),
      alfa, beta (los del nodo tras la fila; en R, el α de DECIDIR y +∞),
      corta (None, 'alfa' o 'beta'), podados (nombres que no se generan por
      ese corte, con sus descendientes), mejor_jugada, mejor_valor, mejora
      (en filas de R: si w > mejor_valor), estado (foto de todos los nodos
      tras la fila: {nombre: dict(estado, v, alfa, beta, cota)} con estado
      'pila', 'devuelto', 'evaluado', 'pormirar' o 'podado') y generados
      (nodos generados hasta esa fila, raiz incluida);
    - jugada, valor, generados, orden_generados (nombres en el orden en que
      se generan), caminos_generados (lo mismo, por camino: «2» nombra dos
      hojas), podados (todos), cortes [(tipo, nodo, w, alfa, beta)].
    """
    lineas = lineas or (LINEAS_ALFA_BETA if poda else LINEAS_MINIMAX)
    nombres = nombres_t(arbol)
    camino_de = {nombre: c for c, (nombre, _) in nombres.items()}
    orden = orden or {}
    evaluar = evaluar or {}
    estado = {nombre: dict(estado="pormirar", v=None, alfa=None, beta=None, cota=False)
              for nombre, _ in nombres.values()}
    filas, generados, caminos, podados, cortes = [], [], [], [], []
    raiz = dict(mejor_jugada=None, mejor_valor=-INF)

    def hijos_de(camino):
        nodo = nodo_en(arbol, camino)
        cs = [camino + (i,) for i in range(len(nodo))]
        nombre = nombres[camino][0]
        if nombre in orden:
            cs = [camino_de[h] for h in orden[nombre]]
        return cs

    def descendientes(camino):
        res = [camino]
        nodo = nodo_en(arbol, camino)
        if isinstance(nodo, tuple):
            for i in range(len(nodo)):
                res += descendientes(camino + (i,))
        return res

    def foto():
        return {k: dict(e) for k, e in estado.items()}

    def fila(evento, linea, pila, v=None, w=None, hijo=None, evaluado=False, alfa=None,
             beta=None, corta=None, podados_=(), mejora=None):
        filas.append(dict(n=len(filas) + 1, evento=evento, linea=linea, pila=tuple(pila),
                          nodo=pila[-1], v=v, w=w, hijo=hijo, evaluado=evaluado,
                          alfa=alfa, beta=beta, corta=corta, podados=list(podados_),
                          mejor_jugada=raiz["mejor_jugada"],
                          mejor_valor=raiz["mejor_valor"], mejora=mejora,
                          estado=foto(), generados=len(generados)))

    def generar(camino):
        generados.append(nombres[camino][0])
        caminos.append(camino)

    def valorar(camino, a, b, d, pila):
        """Lo que devuelve el hijo en `camino`: (w, evaluado)."""
        nodo = nodo_en(arbol, camino)
        nombre = nombres[camino][0]
        if not isinstance(nodo, tuple):
            estado[nombre].update(estado="devuelto", v=nodo)
            return nodo, False
        if profundidad is not None and d == profundidad:
            estado[nombre].update(estado="evaluado", v=evaluar[nombre])
            return evaluar[nombre], True
        return recursion(camino, a, b, d, pila + [nombre]), False

    def recursion(camino, a, b, d, pila):
        nombre = nombres[camino][0]
        es_max = len(camino) % 2 == 0
        tipo = "MAX" if es_max else "MIN"
        v = -INF if es_max else INF
        e = estado[nombre]
        e.update(estado="pila", v=v, alfa=a if poda else None, beta=b if poda else None)
        fila("entra", lineas[f"entra_{tipo}"], pila, v=v,
             alfa=a if poda else None, beta=b if poda else None)
        hs = hijos_de(camino)
        for k, c in enumerate(hs):
            generar(c)
            w, evaluado = valorar(c, a, b, d + 1, pila)
            hijo = nombres[c][0]
            v = max(v, w) if es_max else min(v, w)
            e["v"] = v
            corta = None
            if poda and ((es_max and v >= b) or (not es_max and v <= a)):
                corta = "beta" if es_max else "alfa"
            if corta:
                fuera = [nombres[x][0] for q in hs[k + 1:] for x in descendientes(q)]
                for x in fuera:
                    estado[x]["estado"] = "podado"
                podados.extend(fuera)
                cortes.append((corta, nombre, w, a, b))
                e.update(estado="devuelto", cota=bool(fuera), alfa=None, beta=None)
                fila("regresa", lineas[f"corta_{tipo}"], pila, v=v, w=w, hijo=hijo,
                     evaluado=evaluado, alfa=a, beta=b, corta=corta, podados_=fuera)
                return v
            if poda:
                if es_max:
                    a = max(a, v)
                else:
                    b = min(b, v)
                e.update(alfa=a, beta=b)
            if k == len(hs) - 1:
                e.update(estado="devuelto", alfa=None, beta=None)
            fila("regresa", lineas[f"regresa_{tipo}"], pila, v=v, w=w, hijo=hijo,
                 evaluado=evaluado, alfa=a if poda else None, beta=b if poda else None)
        return v

    generar(())
    estado["R"].update(estado="pila")
    fila("inicio", lineas["inicio"], ["R"], alfa=-INF if poda else None,
         beta=INF if poda else None)
    for c in hijos_de(()):
        generar(c)
        a = raiz["mejor_valor"]
        w, evaluado = valorar(c, a if poda else None, INF if poda else None, 1, ["R"])
        mejora = w > raiz["mejor_valor"]
        if mejora:
            raiz.update(mejor_valor=w, mejor_jugada=nombres[c][1])
        estado["R"]["v"] = raiz["mejor_valor"]
        fila("raiz", lineas["raiz"], ["R"], w=w, hijo=nombres[c][0], evaluado=evaluado,
             alfa=raiz["mejor_valor"] if poda else None, beta=INF if poda else None,
             mejora=mejora)
    estado["R"]["estado"] = "devuelto"
    fila("fin", lineas["fin"], ["R"], alfa=raiz["mejor_valor"] if poda else None,
         beta=INF if poda else None)
    return dict(filas=filas, jugada=raiz["mejor_jugada"], valor=raiz["mejor_valor"],
                generados=len(generados), orden_generados=generados,
                caminos_generados=caminos, podados=podados,
                cortes=cortes)


def tabla_traza(traza, poda=None, combinar=False):
    """La traza como tabla Markdown, con las columnas de las paginas:

    minimax:   | # | línea | pila | v | w | mejor_jugada |
    alfa-beta: | # | línea | pila | (α, β) | v | w | ¿corta? | mejor_jugada |

    La ventana se escribe como intervalo abierto, (α, β): tocar un extremo
    ya corta (decision de la pagina «Alfa-beta a mano»).

    En las filas de R, v es mejor_valor (en alfa-beta, α: es lo mismo) y la
    columna w dice quien lo devolvio («3 (I)»); una hoja va sola («3»). Si
    w > mejor_valor es falso, mejor_jugada lo dice («centro (2 > 5 falso)»).
    combinar=True junta línea y pila en una columna (para el telefono)."""
    filas = traza["filas"] if isinstance(traza, dict) else traza
    if poda is None:
        poda = any(f["alfa"] is not None for f in filas)

    def celda_w(f):
        if f["w"] is None:
            return ""
        if f["evaluado"]:
            return f"{fmt_t(f['w'])} (EVAL {f['hijo']})"
        if f["hijo"] == str(f["w"]):
            return fmt_t(f["w"])
        return f"{fmt_t(f['w'])} ({f['hijo']})"

    def celda_v(f):
        if f["nodo"] == "R":
            return fmt_t(f["mejor_valor"])
        return fmt_t(f["v"])

    def celda_corta(f):
        if f["evento"] != "regresa":
            return ""
        if not f["corta"]:
            return "no"
        signo, borde = ("≥", f["beta"]) if f["corta"] == "beta" else ("≤", f["alfa"])
        return f"sí: {fmt_t(f['v'])}{signo}{fmt_t(borde)}"

    def celda_mejor(f):
        jugada = f["mejor_jugada"] or "ninguna"
        if f["evento"] == "raiz" and not f["mejora"]:
            return f"{jugada} ({fmt_t(f['w'])} > {fmt_t(f['mejor_valor'])} falso)"
        return jugada

    pila = lambda f: "›".join(f["pila"])
    if combinar:
        cab = ["#", "línea · pila"]
        base = lambda f: [str(f["n"]), f"{f['linea']} · {pila(f)}"]
    else:
        cab = ["#", "línea", "pila"]
        base = lambda f: [str(f["n"]), f["linea"], pila(f)]
    if poda:
        cab += ["(α, β)", "v", "w", "¿corta?", "mejor_jugada"]
        resto = lambda f: [f"({fmt_t(f['alfa'])}, {fmt_t(f['beta'])})", celda_v(f),
                           celda_w(f), celda_corta(f), celda_mejor(f)]
    else:
        cab += ["v", "w", "mejor_jugada"]
        resto = lambda f: [celda_v(f), celda_w(f), celda_mejor(f)]
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for f in filas:
        out.append("| " + " | ".join(base(f) + resto(f)) + " |")
    return "\n".join(out)


def expectiminimax_t(arbol=ARBOL_T, azar=("I", "C", "D")):
    """DECIDIR sobre T con los nodos de `azar` como volados parejos: cada
    hijo con probabilidad 1/len(hijos). Los demas nodos siguen alternando
    MAX y MIN. Devuelve (jugada, {nombre: valor exacto}, orden de generados)."""
    nombres = nombres_t(arbol)
    valores, generados = {}, ["R"]

    def ev(camino):
        nodo = nodo_en(arbol, camino)
        nombre = nombres[camino][0]
        if not isinstance(nodo, tuple):
            valores[nombre] = F(nodo)
            return F(nodo)
        hs = []
        for i in range(len(nodo)):
            generados.append(nombres[camino + (i,)][0])
            hs.append(ev(camino + (i,)))
        if nombre in azar:
            v = sum(hs) / len(hs)
        else:
            v = max(hs) if len(camino) % 2 == 0 else min(hs)
        valores[nombre] = v
        return v
    mejor, jugada = -INF, None
    for i in range(len(arbol)):
        generados.append(nombres[(i,)][0])
        w = ev((i,))
        if w > mejor:
            mejor, jugada = w, nombres[(i,)][1]
    valores["R"] = mejor
    return jugada, valores, generados


def profundizacion_iterativa_t(arbol=ARBOL_T, profundidades=(1, 2, 3), evaluar=None,
                               anterior_primero=True):
    """PROFUNDIZACION-ITERATIVA sobre T, sin reloj: para cada d, DECIDIR-
    ALFA-BETA con corte a profundidad d, con la jugada que dejo lista la
    iteracion anterior primero en la raiz (las demas, en el orden dado).
    Devuelve [(d, orden de la raiz, traza)].

    La linea 9 del pseudocodigo, `if w = 100: return a`: si un hijo de la
    raiz devuelve 100, la busqueda en curso se detiene en ese hijo y no hay
    profundidades siguientes. El orden que se devuelve es el que tenia
    planeado; su traza, la de la raiz recorrida solo hasta ese hijo
    (alfa-beta no mira hermanos posteriores para valorar los anteriores, asi
    que es el mismo prefijo), y su jugada es la de ese hijo.

    anterior_primero=False: cada busqueda recorre la raiz en el orden dado
    (para comparar cuanto ahorra poner primero la jugada anterior)."""
    evaluar = evaluar or EVAL_T
    nombres = nombres_t(arbol)
    raiz = [nombres[(i,)] for i in range(len(arbol))]
    res, jugada = [], None
    for d in profundidades:
        orden_raiz = [n for n, a in raiz]
        if jugada and anterior_primero:
            primero = next(n for n, a in raiz if a == jugada)
            orden_raiz = [primero] + [n for n in orden_raiz if n != primero]
        t = traza_decidir(arbol, poda=True, orden={"R": orden_raiz}, profundidad=d,
                          evaluar=evaluar)
        gana = next((f["hijo"] for f in t["filas"]
                     if f["evento"] == "raiz" and f["w"] == 100), None)
        if gana is not None:                                    # linea 9
            t = traza_decidir(arbol, poda=True, profundidad=d, evaluar=evaluar,
                              orden={"R": orden_raiz[:orden_raiz.index(gana) + 1]})
            res.append((d, [dict(raiz)[n] for n in orden_raiz], t))
            return res
        res.append((d, [dict(raiz)[n] for n in orden_raiz], t))
        jugada = t["jugada"]
    return res


def expectiminimax_rival_al_azar(tablero, turno, n=3):
    """Valor esperado para Blancas si Negras elige cada jugada al azar, con la
    misma probabilidad. Blancas sigue maximizando. Fracciones exactas."""
    @lru_cache(maxsize=None)
    def v(t, j):
        g = ganador(t, j, n)
        if g:
            return F(utilidad_simple(g, 0))
        hijos = [v(mover(t, m), otro(j)) for m in jugadas(t, j, n)]
        return max(hijos) if j == "B" else sum(hijos) / len(hijos)
    return v(tablero, turno)


def evaluar_peones(tablero, n):
    """EVAL para tableros de peones: 10 por peon de ventaja mas el avance.

    El avance de un peon blanco es cuantas filas ha subido desde la fila 1;
    el de uno negro, cuantas ha bajado desde la fila n.
    """
    peones = tablero.count("B") - tablero.count("N")
    avance = 0
    for i, pieza in enumerate(tablero):
        fila = i // n
        if pieza == "B":
            avance += fila
        elif pieza == "N":
            avance -= (n - 1 - fila)
    return 10 * peones + avance


def minimax_limitado(tablero, turno, profundidad, n, util=utilidad_simple,
                     escala=100):
    """Minimax con corte: en un final usa escala*U; al cortar, EVAL."""
    def v(t, j, d):
        g = ganador(t, j, n)
        if g:
            return escala * util(g, 0)
        if d == 0:
            return evaluar_peones(t, n)
        hijos = [v(mover(t, m), otro(j), d - 1) for m in jugadas(t, j, n)]
        return max(hijos) if j == "B" else min(hijos)
    return v(tablero, turno, profundidad)


def es_captura(tablero, jugada):
    return tablero[jugada[1]] != "."


def minimax_con_quietud(tablero, turno, profundidad, n, escala=100):
    """Minimax con corte que, al llegar a d = 0, no devuelve la EVAL en seco:
    la usa como valor de «quedarse» y la compara con las capturas, cada una
    seguida hasta un final o una posicion quieta. Quedarse (stand pat) no es
    una jugada legal de pasar: es una aproximacion del algoritmo, que supone
    que el jugador de turno tiene alguna jugada sin captura al menos tan buena
    como la EVAL; falla si no la tiene (ver @jue-c3-quedarse-falla)."""
    def quieta(t, j):
        g = ganador(t, j, n)
        if g:
            return escala * utilidad_simple(g, 0)
        v = evaluar_peones(t, n)
        for m in jugadas(t, j, n):
            if es_captura(t, m):
                h = quieta(mover(t, m), otro(j))
                v = max(v, h) if j == "B" else min(v, h)
        return v

    def v(t, j, d):
        g = ganador(t, j, n)
        if g:
            return escala * utilidad_simple(g, 0)
        if d == 0:
            return quieta(t, j)
        hijos = [v(mover(t, m), otro(j), d - 1) for m in jugadas(t, j, n)]
        return max(hijos) if j == "B" else min(hijos)
    return v(tablero, turno, profundidad)


def nodos_con_corte(tablero, turno, profundidad, n):
    """Nodos que genera minimax con corte, contando la raiz."""
    def c(t, j, d):
        if ganador(t, j, n) or d == 0:
            return 1
        return 1 + sum(c(mover(t, m), otro(j), d - 1) for m in jugadas(t, j, n))
    return c(tablero, turno, profundidad)


def profundizacion_iterativa(tablero, profundidades, n):
    """PROFUNDIZACION-ITERATIVA de «Jugar contra el reloj», sin reloj: para
    cada d, alfa-beta con corte en cada hijo de la raiz, alfa compartido, la
    jugada anterior primero y salida temprana con 100. Devuelve
    [(d, nodos generados contando la raiz, jugada lista)]. Mueve Blancas."""
    def ab(t, j, d, a, b, c):
        c[0] += 1
        g = ganador(t, j, n)
        if g:
            return 100 * utilidad_simple(g, 0)
        if d == 0:
            return evaluar_peones(t, n)
        v = float("-inf") if j == "B" else float("inf")
        for m in jugadas(t, j, n):
            h = ab(mover(t, m), otro(j), d - 1, a, b, c)
            if j == "B":
                v = max(v, h)
                if v >= b:
                    return v
                a = max(a, v)
            else:
                v = min(v, h)
                if v <= a:
                    return v
                b = min(b, v)
        return v
    res, jugada = [], None
    for d in profundidades:
        c, alfa = [1], float("-inf")
        orden = jugadas(tablero, "B", n)
        if jugada is not None:
            orden = [jugada] + [m for m in orden if m != jugada]
        mejor = jugada
        for m in orden:
            v = ab(mover(tablero, m), "N", d - 1, alfa, float("inf"), c)
            if v == 100:
                mejor = m
                break
            if v > alfa:
                alfa, mejor = v, m
        jugada = mejor
        res.append((d, c[0], nombre_jugada(tablero, jugada, n)))
    return res


def promedio_simulaciones(tablero, turno, n=3):
    """Lo que promediarian infinitas simulaciones desde (tablero, turno):
    partidas donde los dos eligen cada jugada al azar, con la misma
    probabilidad, hasta un final. Fraccion exacta, en la escala de U."""
    @lru_cache(maxsize=None)
    def r(t, j):
        g = ganador(t, j, n)
        if g:
            return F(utilidad_simple(g, 0))
        hijos = [r(mover(t, m), otro(j)) for m in jugadas(t, j, n)]
        return sum(hijos) / len(hijos)
    return r(tablero, turno)


# ------------------------------------------------------------------- gato ---

LINEAS_GATO = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
               (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def gato_gana(t):
    for a, b, c in LINEAS_GATO:
        if t[a] != "." and t[a] == t[b] == t[c]:
            return t[a]
    return None


def gato_conteos():
    """(partidas, nodos del arbol, tableros distintos alcanzables)."""
    partidas = [0]
    nodos = [0]
    tableros = set()

    def rec(t, j):
        nodos[0] += 1
        tableros.add(t)
        if gato_gana(t) or "." not in t:
            partidas[0] += 1
            return
        for i in range(9):
            if t[i] == ".":
                rec(t[:i] + j + t[i + 1:], "O" if j == "X" else "X")
    rec("." * 9, "X")
    return partidas[0], nodos[0], len(tableros)


def gato_turno_se_deduce():
    """En todo tablero alcanzable, X tiene las mismas marcas que O o una mas."""
    ok = True

    def rec(t, j):
        nonlocal ok
        x, o = t.count("X"), t.count("O")
        esperado = "X" if x == o else "O"
        ok = ok and (x - o in (0, 1)) and esperado == j
        if gato_gana(t) or "." not in t:
            return
        for i in range(9):
            if t[i] == ".":
                rec(t[:i] + j + t[i + 1:], "O" if j == "X" else "X")
    rec("." * 9, "X")
    return ok


def gato_eval(t):
    """Lineas todavia abiertas para X menos lineas abiertas para O."""
    abiertas_x = sum(1 for l in LINEAS_GATO if all(t[i] != "O" for i in l))
    abiertas_o = sum(1 for l in LINEAS_GATO if all(t[i] != "X" for i in l))
    return abiertas_x - abiertas_o


def gato_profundidad_2(t="." * 9):
    """Para cada jugada de X: el peor EVAL tras la respuesta de O."""
    res = {}
    for i in range(9):
        if t[i] != ".":
            continue
        t1 = t[:i] + "X" + t[i + 1:]
        res[i] = min(gato_eval(t1[:k] + "O" + t1[k + 1:])
                     for k in range(9) if t1[k] == ".")
    return res


def gato_valor():
    """Valor exacto de gato para X: +1, 0 o -1."""
    @lru_cache(maxsize=None)
    def v(t, j):
        g = gato_gana(t)
        if g:
            return 1 if g == "X" else -1
        if "." not in t:
            return 0
        hijos = [v(t[:i] + j + t[i + 1:], "O" if j == "X" else "X")
                 for i in range(9) if t[i] == "."]
        return max(hijos) if j == "X" else min(hijos)
    return v("." * 9, "X")


# --------------------------------------------------------- monedas en fila ---

def monedas_valor(fila):
    """Diferencia que asegura quien mueve (su suma menos la del rival)."""
    fila = tuple(fila)

    @lru_cache(maxsize=None)
    def v(i, j):
        if i > j:
            return 0
        return max(fila[i] - v(i + 1, j), fila[j] - v(i, j - 1))
    return v(0, len(fila) - 1)


def monedas_codicioso_contra_optimo(fila):
    """Diferencia de quien empieza si toma siempre la moneda mayor."""
    fila = tuple(fila)

    @lru_cache(maxsize=None)
    def opt(i, j):
        if i > j:
            return 0
        return max(fila[i] - cod(i + 1, j), fila[j] - cod(i, j - 1))

    @lru_cache(maxsize=None)
    def cod(i, j):
        if i > j:
            return 0
        if fila[i] >= fila[j]:
            return fila[i] - opt(i + 1, j)
        return fila[j] - opt(i, j - 1)
    return cod(0, len(fila) - 1)


def monedas_conteos(n):
    """(nodos del arbol, finales, intervalos distintos incluido el vacio).

    Con una sola moneda hay una sola jugada: tomarla.
    """
    def nodos(k):
        if k == 0:
            return 1
        if k == 1:
            return 2
        return 1 + 2 * nodos(k - 1)
    finales = 2 ** (n - 1) if n else 1
    return nodos(n), finales, n * (n + 1) // 2 + 1


def monedas_alfa_beta(fila, derecha_primero=False):
    """Alfa-beta sobre la diferencia en puntos de quien empieza (MAX).

    Devuelve (valor, nodos visitados).
    """
    visitados = [0]

    def ab(i, j, max_turno, a, b):
        visitados[0] += 1
        if i > j:
            return 0
        opciones = [("izq", i + 1, j, fila[i]), ("der", i, j - 1, fila[j])]
        if i == j:
            opciones = opciones[:1]
        if derecha_primero:
            opciones.reverse()
        signo = 1 if max_turno else -1
        v = float("-inf") if max_turno else float("inf")
        for _, i2, j2, moneda in opciones:
            h = signo * moneda + ab(i2, j2, not max_turno, a - signo * moneda,
                                    b - signo * moneda)
            if max_turno:
                v = max(v, h)
                if v >= b:
                    return v
                a = max(a, v)
            else:
                v = min(v, h)
                if v <= a:
                    return v
                b = min(b, v)
        return v
    return ab(0, len(fila) - 1, True, float("-inf"), float("inf")), visitados[0]


# -------------------------------------------------------------------- azar ---

# ------------------------------------------------------ juegos simultaneos ---

def mezcla_2x2(m):
    """Mezcla optima de filas y columnas de un juego de suma cero 2x2 sin punto
    de silla. Devuelve (p fila 1, q columna 1, valor) en fracciones exactas."""
    (a, b), (c, d) = [[F(x) for x in fila] for fila in m]
    den = a - b - c + d
    p = (d - c) / den
    q = (d - b) / den
    v = (a * d - b * c) / den
    return p, q, v


def punto_de_silla(m):
    """(maximin puro de filas, minimax puro de columnas)."""
    maximin = max(min(fila) for fila in m)
    minimax = min(max(col) for col in zip(*m))
    return maximin, minimax


def garantia_mezcla(m, p):
    """Peor pago esperado de la mezcla de filas p contra cada columna pura."""
    return min(sum(F(pi) * fila[j] for pi, fila in zip(p, m))
               for j in range(len(m[0])))


def equilibrios_puros(pagos_fila, pagos_col):
    """Pares (i, j) donde ninguno gana desviandose solo."""
    filas, cols = len(pagos_fila), len(pagos_fila[0])
    res = []
    for i, j in product(range(filas), range(cols)):
        mejor_fila = all(pagos_fila[i][j] >= pagos_fila[k][j] for k in range(filas))
        mejor_col = all(pagos_col[i][j] >= pagos_col[i][k] for k in range(cols))
        if mejor_fila and mejor_col:
            res.append((i, j))
    return res


PARES_O_NONES = [[1, -1], [-1, 1]]
PIEDRA_PAPEL_TIJERA = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
# Probabilidad de gol (%) para el tirador. Filas: tira a Izquierda / Derecha.
# Columnas: el portero se lanza a Izquierda / Derecha.
PENALES = [[40, 90], [80, 50]]
# Gallina: filas y columnas son Desviarse / Seguir.
GALLINA_FILA = [[0, -1], [1, -10]]
GALLINA_COL = [[0, 1], [-1, -10]]
# Dilema del prisionero en anos de carcel con signo negativo.
# Filas y columnas: Callar / Delatar.
PRISIONERO_FILA = [[-1, -10], [0, -5]]
PRISIONERO_COL = [[-1, 0], [-10, -5]]


# ------------------------------------- pasos para el cuaderno y la web ---
#
# pasos_interactivos(modo, variante) es la unica fuente de los pasos que
# muestra el cuaderno de la unidad (la traza interactiva del arbol T usa
# pasos_por_linea, mas abajo, que se proyecta sobre estas filas). Un
# paso es una fila de la traza tal como la escribe la pagina del modo: mismas
# filas, misma linea, misma pila. Las filas salen de traza_decidir (minimax,
# alfa-beta, corte, iterativa) o de traza_expectiminimax_t (azar); aqui solo
# se les agrega lo que la web necesita: la foto de cada nodo, una frase, los
# valores ya formateados. test_pasos_interactivos.py compara cada paso con la
# tabla de la pagina.
#
# Decisiones:
# - Las filas ✗ de alfa-beta (una hoja que no se genera por un corte) son un
#   paso propio, como en la pagina, que las numera: T1 tiene 10 pasos y T 20.
#   No ejecutan ninguna linea: «linea» es "" y «lineas» [].
# - En azar, C1 y C2 se valoran como en minimax sin filas propias (como en la
#   tabla de la pagina): su w aparece en la fila de C.
# - En corte, la linea 9 (EVAL) no tiene fila: el valor estimado va en w de
#   la fila del padre, marcado con «evaluado».
# - En iterativa, el reloj se acaba despues de d = 3. Hay una fila antes de
#   buscar (lineas 2–3), por cada busqueda una al empezar (5), una por hijo de
#   la raiz (7–10: la llamada, el reloj, la salida temprana y la comparacion)
#   y una al terminar (11–12), y una ultima al entregar (4 y 13: el while ve
#   que no queda tiempo y se devuelve jugada). La «d» de cada paso es la de la
#   busqueda a la que pertenece; la entrega lleva d = 3. resultado.total es
#   3 × 14: tres busquedas sobre el mismo arbol.

LINEAS_EXPECTIMINIMAX = {"inicio": "2", "raiz": "4–5", "fin": "6",
                         "entra_MAX": "10", "entra_MIN": "16", "entra_AZAR": "22",
                         "regresa_MAX": "12–13", "regresa_MIN": "18–19",
                         "regresa_AZAR": "24–25"}
# DECIDIR-CON-CORTE: la linea 9 (if d = 0: return EVAL(s)) corre todo lo demas.
LINEAS_CORTE = {"inicio": "2", "raiz": "4–5", "fin": "6",
                "entra_MAX": "11", "entra_MIN": "17",
                "regresa_MAX": "13–14", "regresa_MIN": "19–20"}
# PROFUNDIZACION-ITERATIVA (1–13) con ALFA-BETA-CON-CORTE (14–32).
LINEAS_RELOJ = {"antes": "2–3", "inicio": "5", "raiz": "7–10", "fin": "11–12",
                "entrega": "4, 13",
                "entra_MAX": "18", "entra_MIN": "26",
                "regresa_MAX": "20–23", "regresa_MIN": "28–31",
                "corta_MAX": "20–22", "corta_MIN": "28–30"}

UNIDAD_JUEGOS = Path(__file__).resolve().parent.parent / "course/7_juegos"
PAGINA_MODO = {
    "minimax": "2_mirar_todo_y_podar/2_minimax_como_algoritmo.md",
    "azar": "2_mirar_todo_y_podar/3_cuando_decide_un_dado.md",
    "alfa-beta": "2_mirar_todo_y_podar/4_alfa_beta.md",
    "corte": "3_cuando_no_cabe/2_minimax_con_corte.md",
    "iterativa": "3_cuando_no_cabe/4_jugar_contra_el_reloj.md",
}
FUNCION_MODO = {"minimax": "DECIDIR-MINIMAX", "azar": "DECIDIR-EXPECTIMINIMAX",
                "alfa-beta": "DECIDIR-ALFA-BETA", "corte": "DECIDIR-CON-CORTE",
                "iterativa": "PROFUNDIZACIÓN-ITERATIVA"}
AZAR_T = ("I", "C", "D")


def pseudo_de_pagina(modo):
    """El bloque ```text de la pagina del modo, renglon por renglon, literal."""
    texto = (UNIDAD_JUEGOS / PAGINA_MODO[modo]).read_text(encoding="utf-8")
    for bloque in re.findall(r"^```text\n(.*?)^```$", texto, re.S | re.M):
        if f"function {FUNCION_MODO[modo]}(" in bloque:
            return bloque.rstrip("\n").split("\n")
    raise ValueError(f"{PAGINA_MODO[modo]} no trae el pseudocodigo de {modo}")


def renglones_pseudo(pseudo):
    """Para cada renglon del pseudocodigo, el numero de linea al que
    pertenece: el suyo, el de la linea que continua, o None (INPUT, OUTPUT,
    comentarios y renglones en blanco)."""
    res, actual = [], None
    for r in pseudo:
        m = re.match(r"^\s*(\d+) ", r)
        if m:
            actual = int(m.group(1))
            res.append(actual)
        elif not r.strip() or not r.startswith(" "):    # blanco, INPUT, OUTPUT
            actual = None
            res.append(None)
        elif r.lstrip().startswith("#"):                 # comentario de una linea
            res.append(None)
        else:                                            # continua la anterior
            res.append(actual)
    return res


def lineas_de(linea):
    """«12–15» -> [12, 13, 14, 15]; «2» -> [2]; «4, 13» -> [4, 13]; «» -> []."""
    if not linea:
        return []
    res = []
    for tramo in linea.split(","):
        if "–" in tramo:
            a, b = tramo.split("–")
            res += list(range(int(a), int(b) + 1))
        else:
            res.append(int(tramo))
    return res


def ids_t(arbol):
    """{camino: id unico}. Los nodos internos se llaman como en nombres_t; una
    hoja, por su padre y su posicion («D-2»), porque dos hojas valen 2."""
    nombres = nombres_t(arbol)
    res = {}
    for c in sorted(nombres):                     # preorden: el padre antes
        if isinstance(nodo_en(arbol, c), tuple):
            res[c] = nombres[c][0]
        else:
            res[c] = f"{res[c[:-1]]}-{c[-1] + 1}"
    return res


def traza_expectiminimax_t(arbol=ARBOL_T, azar=AZAR_T, lineas=None):
    """DECIDIR-EXPECTIMINIMAX sobre T, fila por fila, con la convencion de la
    pagina: una fila al entrar a un nodo de azar (v = 0) y una por cada hijo
    que regresa a el; los nodos que no son de azar se valoran como en minimax
    sin filas propias. Cada hijo de un nodo de azar tiene probabilidad
    1/len(hijos). Las filas tienen las llaves de traza_decidir; valores
    exactos con Fraction."""
    lineas = lineas or LINEAS_EXPECTIMINIMAX
    nombres = nombres_t(arbol)
    filas, caminos = [], []
    raiz = dict(mejor_jugada=None, mejor_valor=-INF)

    def fila(evento, linea, pila, v=None, w=None, hijo=None, mejora=None):
        filas.append(dict(n=len(filas) + 1, evento=evento, linea=linea, pila=tuple(pila),
                          nodo=pila[-1], v=v, w=w, hijo=hijo, evaluado=False,
                          alfa=None, beta=None, corta=None, podados=[],
                          mejor_jugada=raiz["mejor_jugada"],
                          mejor_valor=raiz["mejor_valor"], mejora=mejora,
                          generados=len(caminos)))

    def silencioso(camino):
        """Valor minimax (o esperado) sin filas; genera todo el subarbol."""
        nodo = nodo_en(arbol, camino)
        if not isinstance(nodo, tuple):
            return F(nodo)
        hs = []
        for i in range(len(nodo)):
            caminos.append(camino + (i,))
            hs.append(silencioso(camino + (i,)))
        if nombres[camino][0] in azar:
            return sum(hs) / len(hs)
        return max(hs) if len(camino) % 2 == 0 else min(hs)

    def valorar(camino, pila):
        nodo = nodo_en(arbol, camino)
        nombre = nombres[camino][0]
        if not isinstance(nodo, tuple) or nombre not in azar:
            return silencioso(camino)
        pila = pila + [nombre]
        v = F(0)
        fila("entra", lineas["entra_AZAR"], pila, v=v)
        p = F(1, len(nodo))
        for i in range(len(nodo)):
            c = camino + (i,)
            caminos.append(c)
            w = valorar(c, pila)
            v = v + p * w
            fila("regresa", lineas["regresa_AZAR"], pila, v=v, w=w, hijo=nombres[c][0])
        return v

    caminos.append(())
    fila("inicio", lineas["inicio"], ["R"])
    for i in range(len(arbol)):
        c = (i,)
        caminos.append(c)
        w = valorar(c, ["R"])
        mejora = w > raiz["mejor_valor"]
        if mejora:
            raiz.update(mejor_valor=w, mejor_jugada=nombres[c][1])
        fila("raiz", lineas["raiz"], ["R"], w=w, hijo=nombres[c][0], mejora=mejora)
    fila("fin", lineas["fin"], ["R"])
    return dict(filas=filas, jugada=raiz["mejor_jugada"], valor=raiz["mejor_valor"],
                generados=len(caminos), caminos_generados=caminos)


def arbol_interactivo(arbol, azar=(), evaluar=None):
    """{"nodos": [...]} en preorden, con id, nombre, tipo, padre, jugada,
    hoja, valor (el de la hoja), prob (la de la flecha que llega, si sale de
    un nodo de azar) y eval (si hay EVAL)."""
    nombres, ids = nombres_t(arbol), ids_t(arbol)
    nodos = []

    def tipo(c):
        nodo = nodo_en(arbol, c)
        if not isinstance(nodo, tuple):
            return "HOJA"
        if nombres[c][0] in azar:
            return "AZAR"
        return "MAX" if len(c) % 2 == 0 else "MIN"

    def visitar(c):
        nodo = nodo_en(arbol, c)
        hoja = not isinstance(nodo, tuple)
        padre = c[:-1] if c else None
        prob = None
        if padre is not None and tipo(padre) == "AZAR":
            prob = fmt_t(F(1, len(nodo_en(arbol, padre))))
        nodos.append({"id": ids[c], "nombre": nombres[c][0], "tipo": tipo(c),
                      "padre": None if padre is None else ids[padre],
                      "jugada": nombres[c][1], "hoja": hoja,
                      "valor": fmt_t(nodo) if hoja else None, "prob": prob,
                      "eval": (fmt_t(evaluar[nombres[c][0]])
                               if evaluar and not hoja and nombres[c][0] in evaluar
                               else None)})
        if not hoja:
            for i in range(len(nodo)):
                visitar(c + (i,))
    visitar(())
    return {"nodos": nodos}


def _texto_hoja_o_nodo(ids, arbol, c):
    nodo = nodo_en(arbol, c)
    return f"la hoja {nodo}" if not isinstance(nodo, tuple) else ids[c]


def _pasos_de_traza(arbol, traza, modo, poda, azar=(), d=None, primeros=None,
                    ultima=False):
    """Convierte las filas de una traza en pasos. Reconstruye que nodo es cada
    uno por su camino (las hojas se repiten de nombre) a partir de cuantos
    nodos se habian generado en cada fila. `primeros`: la mejor_jugada que
    hay antes de que regrese el primer hijo de la raiz (en iterativa, la
    jugada lista; en los demas, ninguna). `ultima`: en iterativa, si tras
    esta busqueda se acaba el tiempo."""
    ids, nombres = ids_t(arbol), nombres_t(arbol)
    camino_de = {nombres[c][0]: c for c in nombres if isinstance(nodo_en(arbol, c), tuple)}
    caminos = traza["caminos_generados"]
    total = contar_nodos(arbol)
    v_de, ab_de, devuelto, evaluado, cota, podado = {}, {}, {}, set(), set(), set()
    pasos = []

    def es_hoja(c):
        return not isinstance(nodo_en(arbol, c), tuple)

    def tipo(c):
        if es_hoja(c):
            return "HOJA"
        if nombres[c][0] in azar:
            return "AZAR"
        return "MAX" if len(c) % 2 == 0 else "MIN"

    def descendientes(c):
        res = [c]
        if not es_hoja(c):
            for i in range(len(nodo_en(arbol, c))):
                res += descendientes(c + (i,))
        return res

    def foto(generados, pila, fin):
        hechos = set(caminos[:generados])
        abiertos = set() if fin else set(pila)
        res = {}
        for c in sorted(ids):                     # preorden
            e = dict(estado="pormirar", v="", alfa="", beta="", cota=False)
            if c in abiertos:
                a, b = ab_de.get(c, (None, None))
                e.update(estado="pila", v=fmt_t(v_de.get(c)), alfa=fmt_t(a), beta=fmt_t(b))
            elif c in hechos:
                if es_hoja(c):
                    e.update(estado="devuelto", v=fmt_t(nodo_en(arbol, c)))
                else:
                    e.update(estado="evaluado" if c in evaluado else "devuelto",
                             v=fmt_t(devuelto.get(c, v_de.get(c))), cota=c in cota)
            elif c in podado:
                e["estado"] = "podado"
            res[ids[c]] = e
        return res

    def txt_w(f, hijo_c):
        if f["evaluado"]:
            return f"EVAL({ids[hijo_c]}) = {fmt_t(f['w'])}"
        if es_hoja(hijo_c):
            return f"{fmt_t(f['w'])} de la hoja"
        extra = ", una cota" if hijo_c in cota else ""
        return f"{fmt_t(f['w'])} de {ids[hijo_c]}{extra}"

    for f in traza["filas"]:
        g = f["generados"]
        pila_c = [camino_de[x] for x in f["pila"]]
        yo = pila_c[-1]
        hijo_c = None
        if f["w"] is not None:
            hijo_c = [c for c in caminos[:g] if len(c) == len(yo) + 1 and c[:-1] == yo][-1]
            devuelto[hijo_c] = f["w"]
            if f["evaluado"]:
                evaluado.add(hijo_c)
        v0 = v_de.get(yo)
        a0, b0 = ab_de.get(yo, (None, None))
        if yo == ():
            mv = f["mejor_valor"]
            v_de[yo] = mv
            if poda:
                ab_de[yo] = (mv, INF)
        else:
            v_de[yo] = f["v"]
            if poda:
                ab_de[yo] = (f["alfa"], f["beta"])
        fuera = []
        if f["corta"]:
            hechos = set(caminos[:g])
            fuera = [yo + (i,) for i in range(len(nodo_en(arbol, yo)))
                     if yo + (i,) not in hechos]
            for q in fuera:
                podado.update(descendientes(q))
            if fuera:
                cota.add(yo)
        mejor = f["mejor_jugada"]
        if mejor is None and primeros:
            mejor = primeros
        N = ids[yo]
        ev = f["evento"]
        t = tipo(yo)
        fmt = fmt_t
        # --- la frase ---
        if ev == "inicio":
            if modo == "iterativa":
                frase = f"Búsqueda con d = {d}: α = −∞ y mejor_jugada = {mejor}, la jugada lista."
            elif poda:
                frase = "R empieza: α = −∞, aún no hay jugada."
            else:
                frase = "R empieza: mejor_valor = −∞, aún no hay jugada."
        elif ev == "entra":
            if t == "AZAR":
                frase = f"{N} es de azar: v = 0; sumará Pr · w de cada hijo."
            else:
                cual = "menor" if t == "MAX" else "mayor"
                frase = f"{N} es de {t}: v = {fmt(f['v'])}, {cual} que todo"
                if poda:
                    frase = f"{N} es de {t}: v = {fmt(f['v'])}; llega con la ventana ({fmt(f['alfa'])}, {fmt(f['beta'])})"
                frase += "."
        elif ev == "regresa":
            w, v = fmt(f["w"]), fmt(f["v"])
            if t == "AZAR":
                p = F(1, len(nodo_en(arbol, yo)))
                de = " de la hoja" if es_hoja(hijo_c) else f" de {ids[hijo_c]}"
                frase = (f"{N} suma {fmt(p)} · {w}{de}: "
                         f"v = {fmt(v0)} + {fmt(p * f['w'])} = {v}.")
            else:
                op = "max" if t == "MAX" else "min"
                base = f"{N} recibe {txt_w(f, hijo_c)}: v = {op}({fmt(v0)}, {w}) = {v}"
                if f["corta"]:
                    signo, borde, nombre_corte = (("≥", "β", f["beta"]) if t == "MAX"
                                                  else ("≤", "α", f["alfa"]))
                    if fuera:
                        quien = " y ".join(_texto_hoja_o_nodo(ids, arbol, q) for q in fuera)
                        cola = f"{quien} no se genera" if len(fuera) == 1 else f"no se generan {quien}"
                    else:
                        cola = "no quedaban hijos"
                    frase = (f"{N} recibe {txt_w(f, hijo_c)}: v = {v} {signo} {borde} = "
                             f"{fmt(nombre_corte)} → corte {f['corta']}; {cola}.")
                elif poda:
                    if t == "MAX":
                        cambio = (f"α sube a {fmt(f['alfa'])}" if f["alfa"] != a0
                                  else f"α sigue en {fmt(f['alfa'])}")
                        frase = f"{base}; {v} ≥ β = {fmt(f['beta'])} es falso, {cambio}."
                    else:
                        cambio = (f"β baja a {fmt(f['beta'])}" if f["beta"] != b0
                                  else f"β sigue en {fmt(f['beta'])}")
                        frase = f"{base}; {v} ≤ α = {fmt(f['alfa'])} es falso, {cambio}."
                else:
                    frase = base + "."
        elif ev == "raiz":
            w = fmt(f["w"])
            antes = fmt(pasos[-1]["_mv"] if pasos else -INF)
            if poda:
                if f["mejora"]:
                    frase = f"R recibe {txt_w(f, hijo_c)}: {w} > α = {antes} → α = {w}, mejor_jugada = {mejor}."
                else:
                    frase = f"R recibe {txt_w(f, hijo_c)}: {w} > α = {antes} es falso; mejor_jugada sigue en {mejor}."
            else:
                if f["mejora"]:
                    frase = (f"R recibe {txt_w(f, hijo_c)}: {w} > mejor_valor = {antes} → "
                             f"mejor_valor = {w}, mejor_jugada = {mejor}.")
                else:
                    frase = (f"R recibe {txt_w(f, hijo_c)}: {w} > mejor_valor = {antes} es falso; "
                             f"mejor_jugada sigue en {mejor}.")
        else:  # fin
            mv = fmt(f["mejor_valor"])
            if modo == "iterativa":
                frase = f"La búsqueda con d = {d} terminó: jugada = {mejor}; la siguiente usará d = {d + 1}."
                if ultima:
                    frase = f"La búsqueda con d = {d} terminó: jugada = {mejor}; ya no hay tiempo."
            elif poda:
                frase = f"R devuelve {mejor}; α = {mv} se queda dentro."
            else:
                frase = f"R devuelve {mejor}; el valor {mv} se queda dentro."
        es_r = yo == ()
        paso = {
            "n": 0, "evento": ev, "linea": f["linea"], "lineas": lineas_de(f["linea"]),
            "pila": list(f["pila"]), "nodo": N,
            "v": fmt(f["mejor_valor"] if es_r else f["v"]),
            "w": fmt(f["w"]), "hijo": ids[hijo_c] if hijo_c is not None else "",
            "evaluado": bool(f["evaluado"]),
            "alfa": fmt(f["mejor_valor"] if es_r else f["alfa"]) if poda else "",
            "beta": fmt(INF if es_r else f["beta"]) if poda else "",
            "corta": f["corta"] or "",
            "mejora": None if f["mejora"] is None else bool(f["mejora"]),
            "mejor_jugada": mejor or "ninguna", "generados": g, "total": total,
            "estado": foto(g, pila_c, ev == "fin"), "frase": frase,
            "_mv": f["mejor_valor"],
        }
        if d is not None:
            paso["d"] = d
        pasos.append(paso)
        for q in fuera:
            leaf = es_hoja(q)
            quien = f"La hoja {nodo_en(arbol, q)}" if leaf else ids[q]
            pasos.append({
                "n": 0, "evento": "podado", "linea": "", "lineas": [],
                "pila": list(f["pila"]), "nodo": ids[q], "v": "",
                "w": fmt(nodo_en(arbol, q)) if leaf else "", "hijo": "",
                "evaluado": False, "alfa": "", "beta": "", "corta": f["corta"],
                "mejora": None, "mejor_jugada": mejor or "ninguna", "generados": g,
                "total": total, "estado": copy.deepcopy(paso["estado"]),
                "frase": (f"{quien} no se genera: el corte {f['corta']} de {N} "
                          f"{'la' if leaf else 'lo'} deja fuera."),
                "_mv": f["mejor_valor"], **({"d": d} if d is not None else {})})
    return pasos


def pasos_interactivos(modo, variante=None):
    """Los pasos de un algoritmo sobre el arbol T, para el cuaderno y la web.

    modo: "minimax", "azar" (I, C y D de azar, cada hijo a 1/2), "alfa-beta"
    (variante "T1" o "T", T por omision), "corte" (variante d = 1, 2 o 3, 2
    por omision) o "iterativa" (d = 1, 2 y 3 seguidas). Devuelve un dict
    serializable con modo, variante, titulo, pseudo (el bloque de la pagina),
    renglones (el numero de linea de cada renglon de pseudo), arbol, pasos y
    resultado. Cada valor va ya formateado con fmt_t."""
    if modo not in PAGINA_MODO:
        raise ValueError(f"modo desconocido: {modo}")
    if modo in ("minimax", "azar", "iterativa") and variante is not None:
        raise ValueError(f"{modo} no tiene variantes: {variante!r}")
    arbol, azar, evaluar = ARBOL_T, (), None
    if modo == "minimax":
        traza = traza_decidir(ARBOL_T)
        pasos = _pasos_de_traza(arbol, traza, modo, False)
        titulo = "DECIDIR-MINIMAX en el árbol T"
    elif modo == "azar":
        azar = AZAR_T
        traza = traza_expectiminimax_t(ARBOL_T, AZAR_T)
        pasos = _pasos_de_traza(arbol, traza, modo, False, azar=AZAR_T)
        titulo = "DECIDIR-EXPECTIMINIMAX en el árbol T, con I, C y D de azar"
    elif modo == "alfa-beta":
        variante = "T" if variante is None else variante
        if variante not in ("T", "T1"):
            raise ValueError(f"variante de alfa-beta desconocida: {variante}")
        arbol = ARBOL_T if variante == "T" else ARBOL_T1
        traza = traza_decidir(arbol, poda=True)
        pasos = _pasos_de_traza(arbol, traza, modo, True)
        titulo = f"DECIDIR-ALFA-BETA en el árbol {variante}"
    elif modo == "corte":
        variante = 2 if variante is None else variante
        if isinstance(variante, bool) or variante not in (1, 2, 3, "1", "2", "3"):
            raise ValueError(f"profundidad de corte desconocida: {variante!r}")
        variante = int(variante)
        evaluar = EVAL_T
        traza = traza_decidir(ARBOL_T, profundidad=variante, evaluar=EVAL_T,
                              lineas=LINEAS_CORTE)
        pasos = _pasos_de_traza(arbol, traza, modo, False)
        titulo = f"DECIDIR-CON-CORTE en el árbol T con d = {variante}"
    else:
        evaluar = EVAL_T
        jugada = nombres_t(ARBOL_T)[(0,)][1]      # linea 2: cualquiera, la primera
        ids = ids_t(ARBOL_T)
        estado0 = {i: dict(estado="pormirar", v="", alfa="", beta="", cota=False)
                   for i in ids.values()}
        estado0["R"]["estado"] = "pila"
        pasos = [{"n": 0, "evento": "antes", "linea": LINEAS_RELOJ["antes"],
                  "lineas": lineas_de(LINEAS_RELOJ["antes"]), "pila": ["R"], "nodo": "R",
                  "v": "", "w": "", "hijo": "", "evaluado": False, "alfa": "", "beta": "",
                  "corta": "", "mejora": None, "mejor_jugada": "ninguna", "jugada": jugada,
                  "generados": 1, "total": contar_nodos(ARBOL_T), "estado": estado0,
                  "frase": f"Antes de buscar: jugada = {jugada}, una cualquiera, y d = 1.",
                  "d": 1}]
        por_d = []
        for d, orden, t in profundizacion_iterativa_t(ARBOL_T, (1, 2, 3), EVAL_T):
            # la misma busqueda, con la numeracion de la pagina del reloj
            t = traza_decidir(ARBOL_T, poda=True, orden={"R": [
                {"izq": "I", "centro": "C", "der": "D"}[a] for a in orden]},
                profundidad=d, evaluar=EVAL_T, lineas=LINEAS_RELOJ)
            ps = _pasos_de_traza(ARBOL_T, t, modo, True, d=d, primeros=jugada,
                                 ultima=d == 3)
            jugada = t["jugada"]
            pasos += ps
            por_d.append({"d": d, "orden": orden, "jugada": t["jugada"],
                          "valor": fmt_t(t["valor"]), "generados": t["generados"],
                          "w": [{"hijo": p["hijo"], "w": p["w"],
                                 "cota": p["estado"][p["hijo"]]["cota"]}
                                for p in ps if p["evento"] == "raiz"]})
        # «jugada» (la lista) en cada paso: cambia en la linea 11
        lista = None
        for p in pasos:
            if p["evento"] in ("antes", "fin"):
                lista = p["jugada"] if p["evento"] == "antes" else p["mejor_jugada"]
            p["jugada"] = lista
        ultimo = pasos[-1]
        pasos.append(dict(copy.deepcopy(ultimo), evento="entrega",
                          linea=LINEAS_RELOJ["entrega"],
                          lineas=lineas_de(LINEAS_RELOJ["entrega"]), w="", hijo="",
                          evaluado=False, corta="", mejora=None, d=3,
                          frase=f"Se acaba el tiempo: se entrega {lista}, "
                                f"de la búsqueda con d = 3."))
        titulo = "PROFUNDIZACIÓN-ITERATIVA en el árbol T con d = 1, 2 y 3"
    for k, p in enumerate(pasos, 1):
        p["n"] = k
        p.pop("_mv", None)
    pseudo = pseudo_de_pagina(modo)
    if modo == "iterativa":
        resultado = {"jugada": por_d[-1]["jugada"], "valor": por_d[-1]["valor"],
                     "generados": sum(x["generados"] for x in por_d),
                     # tres busquedas sobre el mismo arbol: 3 × 14
                     "total": len(por_d) * contar_nodos(ARBOL_T), "por_d": por_d}
    else:
        resultado = {"jugada": traza["jugada"], "valor": fmt_t(traza["valor"]),
                     "generados": traza["generados"], "total": contar_nodos(arbol)}
    return {"modo": modo, "variante": variante, "titulo": titulo,
            "pagina": PAGINA_MODO[modo], "pseudo": pseudo,
            "renglones": renglones_pseudo(pseudo),
            "arbol": arbol_interactivo(arbol, azar, evaluar),
            "pasos": pasos, "resultado": resultado}


# ------------------------------------- pasos renglon por renglon ---
#
# pasos_interactivos da una fila de la tabla de traza por paso: salta de la
# linea 2 a la 18 porque la tabla resume. pasos_por_linea(modo, variante)
# ejecuta el mismo pseudocodigo de la pagina y da un paso por CADA linea que
# corre, en el orden real de ejecucion, aunque se quede en el mismo nodo. Es
# la fuente de la traza interactiva (traza_arbol_t.html); el cuaderno sigue
# leyendo pasos_interactivos. test_pasos_por_linea.py comprueba que la
# secuencia es una ejecucion valida y que, proyectada a filas, da la tabla.
#
# Semantica (una decision por renglon, la misma en los cinco pseudocodigos):
# - Entrar a una funcion es un paso en su linea `function`, con los
#   argumentos ya ligados. Las hojas tambien entran (7 → 8: return U(s)).
# - Un `if` es un paso con la condicion evaluada; si su rama es un return
#   en la misma linea (8, 14, 22...), el return es ese mismo paso. El `if`
#   de la linea 5 con su asignacion tambien es un paso.
# - `else` es un paso cuando se toma esa rama; `else if` (azar, 15) es un
#   paso con su condicion.
# - `for each` es un paso por cada hijo que toma, con `a` ya ligado, y uno
#   mas cuando ya no quedan hijos («sale del bucle»), como el `while` de
#   iterativa, que tambien es un paso cuando dice «no». Un corte sale por su
#   return y no llega a ese ultimo paso del for. La jugada hacia una hoja se
#   llama «hoja 3»; en un nodo de azar, a es un resultado, no una jugada.
# - El `if` de la linea 5 de DECIDIR ocupa dos renglones impresos en
#   minimax, azar y corte: `parcial` dice que la condicion fue falsa y su
#   cuerpo (el segundo renglon) no corre.
# - Una llamada son dos pasos en su linea: «llama» (el hijo se GENERA aqui;
#   su estado es «generado») y, tras los pasos del hijo, «w ← valor».
# - Un nodo esta «pila» mientras su marco existe, incluido su return; pasa a
#   «devuelto» (o «evaluado», si devolvio EVAL) en el paso «w ←» del padre.
#   La raiz sigue «pila», con su ventana, hasta su ultimo paso: su marco
#   existe hasta el final. (La ultima fila de pasos_interactivos la pinta
#   «devuelto»; es la unica diferencia entre las dos fotos, a proposito.)
# - Los podados no se llaman y no tienen pasos: el return del corte dice
#   cuales quedan sin generar, y en `filas_x` lleva las filas ✗ de la tabla.
# - El reloj de iterativa alcanza para d = 1, 2 y 3: el while (4) es «sí»
#   tres veces y «no» la cuarta; la linea 8 siempre es «no». El dibujo, el
#   conteo de generados y la d del paso cambian a la busqueda nueva en la
#   linea 5, cuando empieza; en el 4 con «sí» todavia se ve la anterior.
#
# Cada paso: n, linea, fila (la fila de la tabla de la pagina que este paso
# ayuda a cerrar: los pasos entre el fin de la fila k-1 y el de la fila k son
# de la fila k), filas_x, nodo (el del marco actual), marco (la pila de
# llamadas, del mas externo al actual: func, nodo, args y locales como pares
# [nombre, valor ya formateado]), cambia (las variables que ESTA linea
# acaba de escribir: [indice de marco, nombre, valor anterior]), estado (por
# nodo, como en pasos_interactivos, mas «generado»), generados, frase (≤ 90
# caracteres), parcial y, en iterativa, d (la de la busqueda que se dibuja).
# La traza lleva ademas tabla_en_pagina: si la pagina escribe esa traza
# fila por fila (corte con d = 1 o 3 e iterativa solo traen resumenes).

ORDINAL = ["primer", "segundo", "tercer"]


class _PorLinea:
    def __init__(self, modo, arbol, azar=(), evaluar=None, ab=False, orden_raiz=None):
        self.modo, self.arbol, self.azar, self.ab = modo, arbol, azar, ab
        self.evaluar = evaluar or {}
        self.ids, self.nombres = ids_t(arbol), nombres_t(arbol)
        self.pila, self.pasos, self.d, self.escritas = [], [], None, []
        self.reiniciar()

    def reiniciar(self):
        self.estado = {c: dict(estado="pormirar", v=None, alfa=None, beta=None, cota=False)
                       for c in self.ids}
        self.generados = 1

    # --- el arbol ---
    def hoja(self, c):
        return not isinstance(nodo_en(self.arbol, c), tuple)

    def valor_hoja(self, c):
        return nodo_en(self.arbol, c)

    def hijos(self, c):
        return [c + (i,) for i in range(len(nodo_en(self.arbol, c)))]

    def tipo(self, c):
        if self.hoja(c):
            return "HOJA"
        if self.nombres[c][0] in self.azar:
            return "AZAR"
        return "MAX" if len(c) % 2 == 0 else "MIN"

    def N(self, c):
        """El nombre en prosa: «C1» o «la hoja 3»."""
        return f"la hoja {self.valor_hoja(c)}" if self.hoja(c) else self.ids[c]

    def etiqueta(self, c):
        """El nodo como argumento de una llamada: «C1» o «hoja 3»."""
        return f"hoja {self.valor_hoja(c)}" if self.hoja(c) else self.ids[c]

    def accion(self, c):
        return self.nombres[c][1] or f"hoja {self.valor_hoja(c)}"

    def descendientes(self, c):
        res = [c]
        if not self.hoja(c):
            for h in self.hijos(c):
                res += self.descendientes(h)
        return res

    # --- marcos ---
    def asigna(self, nombre, valor):
        """Escribe una variable del marco actual (argumento si lo es, si no
        local) y la anota como escrita por la linea del proximo paso, aunque
        conserve su valor (v ← min(3, 6) = 3 tambien escribe v)."""
        m = self.pila[-1]
        (m["args"] if nombre in m["args"] else m["loc"])[nombre] = valor
        self.escritas.append([len(self.pila) - 1, nombre])

    @property
    def loc(self):
        return self.pila[-1]["loc"]

    @property
    def args(self):
        return self.pila[-1]["args"]

    def entrar(self, func, c, args, linea, frase):
        self.pila.append(dict(func=func, c=c, args=dict(args), loc={}))
        e = self.estado[c]
        e.update(estado="pila", v=None, alfa=None, beta=None, cota=False)
        if self.ab and c != ():
            e.update(alfa=args["α"], beta=args["β"])
        self.paso(linea, frase)

    def llamar(self, linea, c, frase):
        self.generados += 1
        self.estado[c]["estado"] = "generado"
        self.paso(linea, frase)

    def retorna(self, linea, frase, v, evaluado=False, cota=False, cierra=None):
        self.paso(linea, frase, cierra=cierra)
        marco = self.pila.pop()
        return dict(v=v, c=marco["c"], evaluado=evaluado, cota=cota)

    def recibe(self, linea, r, cierra=None):
        """El paso «w ← valor» del padre, ya sin el marco del hijo."""
        c = r["c"]
        self.estado[c].update(estado="evaluado" if r["evaluado"] else "devuelto",
                              v=r["v"], alfa=None, beta=None, cota=r["cota"])
        self.asigna("w", r["v"])
        if r["evaluado"]:
            de = f"EVAL({self.ids[c]})"
        elif self.hoja(c):
            de = "la hoja"
        else:
            de = self.ids[c] + (", una cota" if r["cota"] else "")
        self.paso(linea, f"w ← {fmt_t(r['v'])}: lo que devolvió {de}.", cierra=cierra)
        return r["v"]

    def podar(self, c, desde):
        """Marca podados los hermanos que siguen a `desde`; devuelve las
        raices de lo que no se genera."""
        hs = self.hijos(c)
        fuera = hs[hs.index(desde) + 1:]
        for q in fuera:
            for x in self.descendientes(q):
                self.estado[x]["estado"] = "podado"
        return fuera

    def texto_fuera(self, fuera):
        if not fuera:
            return "no quedaban hijos"
        quien = " y ".join(self.N(q) for q in fuera)
        return f"{quien} no se genera" if len(fuera) == 1 else f"no se generan {quien}"

    # --- un paso ---
    def _fmt(self, v):
        if v is None:
            return "ninguna"
        if isinstance(v, str):
            return v
        return fmt_t(v)

    def paso(self, linea, frase, cierra=None, parcial=False):
        if len(frase) > 90:
            raise ValueError(f"frase de {len(frase)} caracteres: {frase}")
        marco = [{"func": m["func"], "nodo": self.ids[m["c"]],
                  "args": [[k, self._fmt(v)] for k, v in m["args"].items()],
                  "locales": [[k, self._fmt(v)] for k, v in m["loc"].items()]}
                 for m in self.pila]
        estado = {self.ids[c]: dict(estado=e["estado"], v=fmt_t(e["v"]), alfa=fmt_t(e["alfa"]),
                                    beta=fmt_t(e["beta"]), cota=bool(e["cota"]))
                  for c, e in sorted(self.estado.items())}
        p = {"linea": linea, "nodo": self.ids[self.pila[-1]["c"]], "marco": marco,
             "estado": estado, "generados": self.generados, "frase": frase,
             "_cierra": cierra, "_escritas": self.escritas, "_parcial": parcial}
        self.escritas = []
        if self.d is not None:
            p["d"] = self.d
        self.pasos.append(p)

    def raiz_estado(self, valor):
        e = self.estado[()]
        e["v"] = valor
        if self.ab:
            e.update(alfa=valor, beta=INF)




def _frase_for(x, c, k, padre):
    """La frase de un `for each` que toma un hijo. En un nodo de azar nadie
    elige: a es un resultado del azar, no una jugada."""
    yo = c[:-1]
    if yo and x.tipo(yo) == "AZAR":
        lleva = "" if x.hoja(c) else f", que lleva a {x.ids[c]}"
        return f"Toma a = {x.accion(c)}: el {ORDINAL[k]} resultado del azar en {padre}{lleva}."
    if x.hoja(c):
        return f"Toma a = {x.accion(c)}: el {ORDINAL[k]} hijo de {padre}."
    return f"Toma a = {x.accion(c)}: el {ORDINAL[k]} hijo de {padre} es {x.ids[c]}."


FRASE_SALE = "for each: ya no quedan hijos → sale del bucle."


def _texto_args(args):
    return "".join(f", {k} = {fmt_t(v)}" for k, v in args.items())


# Las lineas de cada funcion recursiva: function, s ∈ S_F, d = 0 (si hay
# corte), Pl = MAX, la primera del caso MAX (v ← −∞) y el else (en azar, el
# «else if Pl(s) = MIN»; su v ← +∞ es la siguiente). Tras cada v ← ...
# vienen for (+1), la llamada (+2), v ← max/min (+3) y, con poda, el if del
# corte (+4) y la ventana (+5); el return es +4 sin poda y +6 con ella.
LINEAS_INTERNA = {
    "minimax": dict(func=7, sf=8, d0=None, max=9, vmax=10, otro=15),
    "azar": dict(func=7, sf=8, d0=None, max=9, vmax=10, otro=15, azar=21),
    "alfa-beta": dict(func=7, sf=8, d0=None, max=9, vmax=10, otro=17),
    "corte": dict(func=7, sf=8, d0=9, max=10, vmax=11, otro=16),
    "iterativa": dict(func=14, sf=15, d0=16, max=17, vmax=18, otro=25),
}
FUNCION_INTERNA = {"minimax": "MINIMAX", "azar": "EXPECTIMINIMAX", "alfa-beta": "ALFA-BETA",
                   "corte": "MINIMAX-CON-CORTE", "iterativa": "ALFA-BETA-CON-CORTE"}


def _interna(x):
    """La funcion recursiva del modo, renglon por renglon. Cada variable se
    escribe ANTES de emitir el paso de su linea: un paso muestra el estado
    justo despues de ejecutar su linea."""
    modo = x.modo
    L, func = LINEAS_INTERNA[modo], FUNCION_INTERNA[modo]
    corte, ab, azar = L["d0"] is not None, x.ab, modo == "azar"

    def interna(c, **args):
        N = x.ids[c]
        x.entrar(func, c, args, L["func"], f"Entra a {func}: s = {x.N(c)}{_texto_args(args)}.")
        if x.hoja(c):
            u = F(x.valor_hoja(c)) if azar else x.valor_hoja(c)
            u_txt = "100·U(s)" if corte else "U(s)"
            return x.retorna(L["sf"], f"s ∈ S_F? sí: la hoja es final → return {u_txt} = "
                                      f"{fmt_t(u)}.", u)
        x.paso(L["sf"], f"s ∈ S_F? no: {N} no es final.")
        if corte:
            if args["d"] == 0:
                e = x.evaluar[x.nombres[c][0]]
                return x.retorna(L["d0"], f"d = 0? sí → return EVAL({N}) = {fmt_t(e)}: "
                                          f"aquí se estima.", e, evaluado=True)
            x.paso(L["d0"], f"d = 0? no: d = {args['d']}, aún se mira más hondo.")
        t = x.tipo(c)
        if t == "MAX":
            x.paso(L["max"], f"Pl({N}) = MAX? sí: en {N} elige MAX.")
            base, ini, op = L["vmax"], -INF, max
        else:
            x.paso(L["max"], f"Pl({N}) = MAX? no.")
            if azar and t == "MIN":
                x.paso(L["otro"], f"Pl({N}) = MIN? sí: en {N} elige MIN.")
                base, ini, op = L["otro"] + 1, INF, min
            elif azar:
                x.paso(L["otro"], f"Pl({N}) = MIN? no: {N} es de azar.")
                x.paso(L["azar"], f"else: {N} es de azar; nadie elige.")
                base, ini, op = L["azar"] + 1, F(0), None
            else:
                x.paso(L["otro"], f"else: en {N} elige MIN.")
                base, ini, op = L["otro"] + 1, INF, min
        # en azar, solo los nodos de azar tienen filas en la tabla
        cz = 0 if (not azar or t == "AZAR") else None
        x.asigna("v", ini)
        x.estado[c]["v"] = ini
        if op is None:
            x.paso(base, "v ← 0: aquí se suma, no se compara.", cierra=cz)
        else:
            x.paso(base, f"v ← {fmt_t(ini)}: {'menor' if op is max else 'mayor'} que todo.",
                   cierra=cz)
        hs = x.hijos(c)
        for k, h in enumerate(hs):
            x.asigna("a", x.accion(h))
            x.paso(base + 1, _frase_for(x, h, k, N))
            ha = {}
            if corte:
                ha["d"] = args["d"] - 1
            if ab:
                ha["α"], ha["β"] = x.args["α"], x.args["β"]
            x.llamar(base + 2, h, f"Genera {x.N(h)} y llama {func}({x.etiqueta(h)}{_texto_args(ha)}).")
            w = x.recibe(base + 2, interna(h, **ha))
            v0 = x.loc["v"]
            if op is None:
                p = F(1, len(hs))
                v = v0 + p * w
                x.asigna("v", v)
                x.estado[c]["v"] = v
                x.paso(base + 3, f"v ← {fmt_t(v0)} + {fmt_t(p)} · {fmt_t(w)} = {fmt_t(v)}.",
                       cierra=cz)
                continue
            v = op(v0, w)
            x.asigna("v", v)
            x.estado[c]["v"] = v
            nom = "max" if op is max else "min"
            x.paso(base + 3, f"v ← {nom}({fmt_t(v0)}, {fmt_t(w)}) = {fmt_t(v)}.",
                   cierra=None if ab else cz)
            if not ab:
                continue
            es_max = op is max
            borde, letra, signo = ((x.args["β"], "β", "≥") if es_max
                                   else (x.args["α"], "α", "≤"))
            corta = v >= borde if es_max else v <= borde
            cond = f"v {signo} {letra}? {fmt_t(v)} {signo} {fmt_t(borde)}"
            if corta:
                fuera = x.podar(c, h)
                tipo_corte = "beta" if es_max else "alfa"
                return x.retorna(base + 4, f"{cond} sí → return {fmt_t(v)}, corte {tipo_corte}; "
                                           f"{x.texto_fuera(fuera)}.",
                                 v, cota=bool(fuera), cierra=len(fuera))
            x.paso(base + 4, f"{cond} no: sigue.")
            otra = "α" if es_max else "β"
            a0 = x.args[otra]
            a1 = max(a0, v) if es_max else min(a0, v)
            x.asigna(otra, a1)
            x.estado[c]["alfa" if es_max else "beta"] = a1
            if a1 != a0:
                cola = f"{otra} {'sube' if es_max else 'baja'}"
            else:
                cola = f"{otra} sigue igual"
            x.paso(base + 5, f"{otra} ← {nom}({fmt_t(a0)}, {fmt_t(v)}) = {fmt_t(a1)}: {cola}.",
                   cierra=0)
        x.paso(base + 1, FRASE_SALE)
        ret = base + (6 if ab else 4)
        return x.retorna(ret, f"return v = {fmt_t(x.loc['v'])}.", x.loc["v"])
    interna.nombre = func
    return interna


def _decidir_linea(x, func, d=None):
    """DECIDIR-* (lineas 1–6), comun a minimax, azar, alfa-beta y corte."""
    R, ab = (), x.ab
    interna = _interna(x)
    mv = "α" if ab else "mejor_valor"
    args = {} if d is None else {"d": d}
    x.entrar(func, R, args, 1, f"Empieza {func} en la raíz R{_texto_args(args)}.")
    x.asigna(mv, -INF)
    x.asigna("mejor_jugada", None)
    x.raiz_estado(-INF)
    x.paso(2, f"{mv} ← −∞ y mejor_jugada ← ninguna: aún no hay jugada.", cierra=0)
    for k, c in enumerate(x.hijos(R)):
        x.asigna("a", x.accion(c))
        x.paso(3, _frase_for(x, c, k, "R"))
        ha = {}
        if d is not None:
            ha["d"] = d - 1
        if ab:
            ha["α"], ha["β"] = x.loc["α"], INF
        x.llamar(4, c, f"Genera {x.N(c)} y llama {interna.nombre}({x.etiqueta(c)}{_texto_args(ha)}).")
        w = x.recibe(4, interna(c, **ha))
        _compara_raiz(x, 5, w, c, mv)
    # la raiz sigue en la pila hasta su ultimo paso, con su ventana
    x.paso(3, "for each: ya no quedan jugadas → sale del bucle.")
    x.paso(6, f"return mejor_jugada = {x.loc['mejor_jugada']}.", cierra=0)
    return x.loc["mejor_jugada"], x.loc[mv]


def _compara_raiz(x, linea, w, c, mv):
    antes = x.loc[mv]
    if w > antes:
        x.asigna(mv, w)
        x.asigna("mejor_jugada", x.accion(c))
        x.raiz_estado(w)
        f = (f"w > {mv}? {fmt_t(w)} > {fmt_t(antes)} sí → {mv} ← {fmt_t(w)}, "
             f"mejor_jugada ← {x.accion(c)}.")
    else:
        f = (f"w > {mv}? {fmt_t(w)} > {fmt_t(antes)} no: mejor_jugada sigue en "
             f"{x._fmt(x.loc['mejor_jugada'])}.")
    x.paso(linea, f, cierra=0, parcial=not w > antes)


def _iterativa_linea(x, busquedas=3):
    """PROFUNDIZACIÓN-ITERATIVA (1–13) con ALFA-BETA-CON-CORTE (14–32). El
    reloj alcanza para `busquedas` busquedas completas."""
    R = ()
    interna = _interna(x)
    func = "PROFUNDIZACIÓN-ITERATIVA"
    x.d = 1
    x.estado[R]["estado"] = "pila"
    x.entrar(func, R, {}, 1, f"Empieza {func} en la raíz R.")
    hijos = x.hijos(R)
    jugada = x.accion(hijos[0])
    x.asigna("jugada", jugada)
    x.paso(2, f"jugada ← {jugada}, una cualquiera: siempre hay algo que entregar.")
    x.asigna("d", 1)
    x.paso(3, "d ← 1: la primera búsqueda mira una sola jugada.", cierra=0)
    por_d = []
    d = 1
    while True:
        if d > busquedas:
            x.paso(4, f"¿Queda tiempo? no: el reloj se acabó tras la búsqueda con d = {d - 1}.")
            break
        x.paso(4, f"¿Queda tiempo? sí → una búsqueda con d = {d}.")
        # el dibujo y el conteo empiezan de nuevo cuando empieza la busqueda
        # (linea 5), no antes: hasta ahi se ve la busqueda anterior
        if d > 1:
            x.reiniciar()
            x.d = d
            x.estado[R]["estado"] = "pila"
        x.asigna("α", -INF)
        x.asigna("mejor_jugada", jugada)
        x.raiz_estado(-INF)
        x.paso(5, f"α ← −∞ y mejor_jugada ← {jugada}, la jugada lista.", cierra=0)
        orden = sorted(hijos, key=lambda c: x.accion(c) != jugada)
        for k, c in enumerate(orden):
            x.asigna("a", x.accion(c))
            if k == 0:
                x.paso(6, f"Toma a = {x.accion(c)} primero: es la jugada lista.")
            else:
                x.paso(6, f"Toma a = {x.accion(c)}: el siguiente hijo de R es {x.ids[c]}.")
            ha = {"d": d - 1, "α": x.loc["α"], "β": INF}
            x.llamar(7, c, f"Genera {x.ids[c]} y llama ALFA-BETA-CON-CORTE({x.ids[c]}"
                           f"{_texto_args(ha)}).")
            w = x.recibe(7, interna(c, **ha))
            x.paso(8, "¿Se acabó el tiempo? no: la búsqueda sigue.")
            x.paso(9, f"w = 100? {fmt_t(w)} = 100 no: no es una victoria segura.")
            _compara_raiz(x, 10, w, c, "α")
        x.paso(6, "for each: ya no quedan jugadas → sale del bucle.")
        jugada = x.loc["mejor_jugada"]
        x.asigna("jugada", jugada)
        x.paso(11, f"jugada ← {jugada}: la búsqueda con d = {d} terminó completa.")
        por_d.append({"d": d, "orden": [x.accion(c) for c in orden], "jugada": jugada,
                      "valor": fmt_t(x.loc["α"]), "generados": x.generados})
        x.asigna("d", d + 1)
        x.paso(12, f"d ← {d} + 1 = {d + 1}.", cierra=0)
        d += 1
    x.paso(13, f"return jugada = {jugada}: se entrega la de la búsqueda con d = {d - 1}.",
           cierra=0)
    return por_d


def _numerar_filas(pasos):
    """fila y filas_x de cada paso (ver la explicacion arriba); quita _cierra."""
    fila, pendientes = 0, []
    for p in pasos:
        pendientes.append(p)
        p["filas_x"] = []
        c = p.pop("_cierra")
        if c is None:
            continue
        fila += 1
        for q in pendientes:
            q["fila"] = fila
        p["filas_x"] = list(range(fila + 1, fila + 1 + c))
        fila += c
        pendientes = []
    if pendientes:
        raise ValueError("hay pasos despues de la ultima fila")


def _marcar_cambios(pasos):
    """cambia: [indice de marco, variable, valor anterior] de cada variable que
    el paso acaba de escribir (o ligar, al entrar a una funcion)."""
    previo = []
    for p in pasos:
        cambia = []
        for i, m in enumerate(p["marco"]):
            antes = {}
            if i < len(previo) and (previo[i]["func"], previo[i]["nodo"]) == (m["func"], m["nodo"]):
                antes = dict(previo[i]["args"] + previo[i]["locales"])
            for k, v in m["args"] + m["locales"]:
                if antes.get(k) != v or [i, k] in p["_escritas"]:
                    cambia.append([i, k, antes.get(k, "")])
        p.pop("_escritas")
        p["cambia"] = cambia
        previo = p["marco"]


def pasos_por_linea(modo, variante=None):
    """Los pasos de un algoritmo sobre el arbol T, uno por cada linea del
    pseudocodigo de la pagina que se ejecuta, en orden. Mismos modos y
    variantes que pasos_interactivos; devuelve un dict con sus mismas claves
    (pasos con otro formato: ver arriba)."""
    base = pasos_interactivos(modo, variante)     # valida modo y variante
    variante = base["variante"]
    arbol, azar, evaluar = ARBOL_T, (), None
    if modo == "alfa-beta" and variante == "T1":
        arbol = ARBOL_T1
    if modo == "azar":
        azar = AZAR_T
    if modo in ("corte", "iterativa"):
        evaluar = EVAL_T
    x = _PorLinea(modo, arbol, azar=azar, evaluar=evaluar,
                  ab=modo in ("alfa-beta", "iterativa"))
    if modo == "iterativa":
        por_d = _iterativa_linea(x)
        resultado = {"jugada": por_d[-1]["jugada"], "valor": por_d[-1]["valor"],
                     "generados": sum(b["generados"] for b in por_d),
                     "total": len(por_d) * contar_nodos(arbol), "por_d": por_d}
    else:
        jugada, valor = _decidir_linea(x, FUNCION_MODO[modo],
                                       d=variante if modo == "corte" else None)
        resultado = {"jugada": jugada, "valor": fmt_t(valor), "generados": x.generados,
                     "total": contar_nodos(arbol)}
    pasos = x.pasos
    continuadas = {r for k, r in enumerate(base["renglones"])
                   if r is not None and k > 0 and base["renglones"][k - 1] == r}
    for p in pasos:
        p["parcial"] = bool(p.pop("_parcial")) and p["linea"] in continuadas
    _numerar_filas(pasos)
    _marcar_cambios(pasos)
    for k, p in enumerate(pasos, 1):
        p["n"] = k
    return {"modo": modo, "variante": variante, "titulo": base["titulo"],
            "pagina": base["pagina"], "pseudo": base["pseudo"],
            "renglones": base["renglones"], "arbol": base["arbol"],
            "tabla_en_pagina": (modo, variante) not in SIN_TABLA_EN_PAGINA,
            "pasos": pasos, "resultado": resultado}


# Las trazas que su pagina no escribe fila por fila (solo en resumen).
SIN_TABLA_EN_PAGINA = {("corte", 1), ("corte", 3), ("iterativa", None)}


# ================================ clase 3: cifras de la reescritura (G2) ===
#
# Lo que citan las paginas de «Cuando el arbol no cabe» tras la reescritura
# de 2026-10: micros de EVAL, la rama de profundidad 3, la traza de T con
# d = 2 tal como la escribe la pagina, las variantes de los ejercicios
# finales, la tabla unica de nodos generados, la clase de cada valor en una
# tabla de transposicion y una vuelta de MCTS cuyos conteos cuadran. Las
# funciones de arriba no cambian: la animacion y el notebook leen de ellas.

# ---------------------------------------------- p1: cortar y evaluar ---

# Una posicion sencilla con material desigual, para el micro de EVAL: desde
# el inicio del 4x4, Blancas gana un peon en c3. Mueven Negras.
CAMINO_MICRO_EVAL = ["b1-b2", "c4-c3", "b2xc3"]


def jugar_nombres(tablero, turno, nombres, n=3):
    """Aplica jugadas por nombre («b1-b2», «b2xc3»); devuelve (tablero, turno)."""
    for nombre in nombres:
        opciones = {nombre_jugada(tablero, m, n): m for m in jugadas(tablero, turno, n)}
        tablero, turno = mover(tablero, opciones[nombre]), otro(turno)
    return tablero, turno


def desglose_eval(tablero, n):
    """Las piezas de EVAL = 10·material + avance, lado por lado."""
    peones_b, peones_n = tablero.count("B"), tablero.count("N")
    avance_b = sum(i // n for i, p in enumerate(tablero) if p == "B")
    avance_n = sum(n - 1 - i // n for i, p in enumerate(tablero) if p == "N")
    res = dict(peones_b=peones_b, peones_n=peones_n, avance_b=avance_b, avance_n=avance_n,
               material=peones_b - peones_n, avance=avance_b - avance_n)
    res["eval"] = 10 * res["material"] + res["avance"]
    assert res["eval"] == evaluar_peones(tablero, n)
    return res


def arbol_con_corte(tablero, turno, d, n, jugada=None):
    """El arbol que recorre minimax con corte con d en la raiz, nodo por nodo:
    dict(jugada, tablero, turno, final ('B', 'N' o None), corte (si se
    estima con EVAL), valor (100·U, EVAL o el max/min de sus hijos), hijos)."""
    g = ganador(tablero, turno, n)
    nodo = dict(jugada=jugada, tablero=tablero, turno=turno, final=g, corte=False, hijos=[])
    if g:
        nodo["valor"] = 100 * utilidad_simple(g, 0)
    elif d == 0:
        nodo.update(corte=True, valor=evaluar_peones(tablero, n))
    else:
        nodo["hijos"] = [arbol_con_corte(mover(tablero, m), otro(turno), d - 1, n,
                                         nombre_jugada(tablero, m, n))
                         for m in jugadas(tablero, turno, n)]
        vs = [h["valor"] for h in nodo["hijos"]]
        nodo["valor"] = max(vs) if turno == "B" else min(vs)
    return nodo


def contar_con_corte(nodo):
    """Nodos de un arbol_con_corte, contando su raiz."""
    return 1 + sum(contar_con_corte(h) for h in nodo["hijos"])


def ramificacion_maxima(nodo, camino=()):
    """(b, caminos): el mayor numero de jugadas de un nodo que se expande, y
    los caminos (listas de jugadas desde la raiz) de los nodos que lo tienen."""
    b, donde = len(nodo["hijos"]), [list(camino)] if nodo["hijos"] else []
    for h in nodo["hijos"]:
        bh, dh = ramificacion_maxima(h, camino + (h["jugada"],))
        if bh > b:
            b, donde = bh, dh
        elif bh == b and bh:
            donde += dh
    return b, donde


def evals_tras_respuestas(tablero, turno, n):
    """{jugada: {respuesta: EVAL}}: la tabla de profundidad 2, completa."""
    res = {}
    for m in jugadas(tablero, turno, n):
        t = mover(tablero, m)
        res[nombre_jugada(tablero, m, n)] = {
            nombre_jugada(t, r, n): evaluar_peones(mover(t, r), n)
            for r in jugadas(t, otro(turno), n)}
    return res


# --------------------------------------------- p2: minimax con corte ---

# La variante del ejercicio final: EVAL(C2) = 1 en vez de 9. Con d = 2 cambia
# la jugada (izq); con d = 1 no se mira C2 y con d = 3 no se evalua nada.
EVAL_T_VARIANTE = {**EVAL_T, "C2": 1}

# El empate del ejercicio final: EVAL(C1) = 3 en vez de 6. Con d = 2, C vale
# min(3, 9) = 3 e iguala a I; con «>» estricto gana la que R prueba primero:
# izq con el orden de la pagina, centro con R al reves.
EVAL_T_EMPATE = {**EVAL_T, "C1": 3}


def decidir_con_corte_t(d, orden=None, evaluar=None):
    """DECIDIR-CON-CORTE(R, d) en T: (jugada, valor, nodos generados). orden:
    los hijos de R en el orden de visita, por nombre («D», «C», «I»)."""
    t = traza_decidir(ARBOL_T, profundidad=d, evaluar=evaluar or EVAL_T,
                      orden={"R": orden} if orden else None)
    return t["jugada"], t["valor"], t["generados"]


def filas_corte_t(d=2, orden=None, evaluar=None):
    """La traza de DECIDIR-CON-CORTE(R, d) en T con las columnas de la pagina:
    (#, «línea · pila», v, w, jugada). En w, una hoja va sola y un nodo lleva
    su nombre; jugada es mejor_jugada, «—» si ninguna."""
    t = traza_decidir(ARBOL_T, profundidad=d, evaluar=evaluar or EVAL_T,
                      orden={"R": orden} if orden else None, lineas=LINEAS_CORTE)
    res = []
    for f in t["filas"]:
        v = f["mejor_valor"] if f["nodo"] == "R" else f["v"]
        w = ""
        if f["w"] is not None:
            w = fmt_t(f["w"]) if f["hijo"] == str(f["w"]) else f"{fmt_t(f['w'])} ({f['hijo']})"
        res.append((f["n"], f"{f['linea']} · {'›'.join(f['pila'])}", fmt_t(v), w,
                    f["mejor_jugada"] or "—"))
    return res


# -------------------------------------------- p4: jugar contra el reloj ---

JUGADA_A_NOMBRE = {"izq": "I", "centro": "C", "der": "D"}


def iterativa_sin_poda_t(profundidades=(1, 2, 3), evaluar=None, anterior_primero=False):
    """Profundizacion iterativa con DECIDIR-CON-CORTE (sin poda) en T:
    [(d, orden de la raiz, jugada lista, valor, nodos generados)]. Sin poda,
    el orden solo cambia algo si hay empates."""
    res, jugada = [], None
    for d in profundidades:
        orden = ["izq", "centro", "der"]
        if anterior_primero and jugada:
            orden = [jugada] + [a for a in orden if a != jugada]
        jugada, valor, nodos = decidir_con_corte_t(d, [JUGADA_A_NOMBRE[a] for a in orden],
                                                   evaluar)
        res.append((d, orden, jugada, valor, nodos))
    return res


def llamadas_alfa_beta(traza):
    """Una fila por llamada a ALFA-BETA-CON-CORTE en un nodo interno, en el
    orden en que entra: (nodo, α al llegar, β al llegar, v que devuelve,
    corte o None)."""
    res, abiertas = [], {}
    for f in traza["filas"]:
        if f["evento"] == "entra":
            abiertas[f["nodo"]] = len(res)
            res.append([f["nodo"], f["alfa"], f["beta"], None, None])
        elif f["evento"] == "regresa":
            fila = res[abiertas[f["nodo"]]]
            fila[3], fila[4] = f["v"], f["corta"]
    return [tuple(r) for r in res]


def clase_de_valor(alfa, beta, v):
    """Lo que vale v para una tabla de transposicion, segun la ventana con que
    se llamo al nodo: exacto si α < v < β; piso si v ≥ β; techo si v ≤ α."""
    if v >= beta:
        return "piso"
    if v <= alfa:
        return "techo"
    return "exacto"


def clases_transposicion(traza):
    """{nodo: (α, β, v, clase)} para cada llamada de una traza de alfa-beta."""
    return {n: (a, b, v, clase_de_valor(a, b, v)) for n, a, b, v, _ in llamadas_alfa_beta(traza)}


def valor_con_corte_hijo_t(hijo, niveles, evaluar=None):
    """El valor con corte (sin poda) del hijo de R en T («I», «C» o «D»)
    cuando le quedan `niveles` jugadas por mirar. Para la tabla de
    transposicion: una entrada guardada con mas profundidad no da el valor
    con corte de una busqueda menos honda (C vale 6 con un nivel, 5 con dos)."""
    t = traza_decidir(ARBOL_T, profundidad=niveles + 1, evaluar=evaluar or EVAL_T)
    return {f["hijo"]: f["w"] for f in t["filas"] if f["evento"] == "raiz"}[hijo]


def _ab_t(arbol, camino, d, a, b, evaluar, nombres, cuenta):
    """ALFA-BETA-CON-CORTE en T (el nodo en `camino` ya se conto)."""
    nodo = nodo_en(arbol, camino)
    if not isinstance(nodo, tuple):
        return nodo
    if d == 0:
        return evaluar[nombres[camino][0]]
    es_max = len(camino) % 2 == 0
    v = -INF if es_max else INF
    for i in range(len(nodo)):
        cuenta[0] += 1
        w = _ab_t(arbol, camino + (i,), d - 1, a, b, evaluar, nombres, cuenta)
        if es_max:
            v = max(v, w)
            if v >= b:
                return v
            a = max(a, v)
        else:
            v = min(v, w)
            if v <= a:
                return v
            b = min(b, v)
    return v


def iterativa_con_reloj_t(acciones, tope=None, profundidades=(1, 2, 3), evaluar=None,
                          arbol=None):
    """PROFUNDIZACION-ITERATIVA (las 32 lineas de la pagina) en T, con A(R) en
    el orden `acciones` y un reloj que se acaba cuando se han generado `tope`
    nodos, contando todas las busquedas. El reloj se mira donde lo mira el
    pseudocodigo: en la linea 4 (antes de cada busqueda) y en la 8 (tras cada
    hijo de la raiz). Sin tope, se acaba al terminar la ultima profundidad.

    Devuelve (corridas, entrega): corridas = [dict(d, orden, jugada,
    generados)] de las busquedas completas; entrega = dict(jugada, d,
    generados, linea, despues_de) con d la busqueda en curso y despues_de el
    hijo de la raiz tras el que se miro el reloj (None en la linea 4/13).

    arbol: otro arbol con la forma de T (por omision, ARBOL_T); el arbol de
    resultados entra con sus finales en 100·U (iterativa_con_reloj_tpm)."""
    evaluar = evaluar or EVAL_T
    arbol = ARBOL_T if arbol is None else arbol
    nombres = nombres_t(arbol)
    camino_de = {a: c for c, (_, a) in nombres.items() if len(c) == 1}
    cuenta = [0]
    acabado = lambda: tope is not None and cuenta[0] >= tope  # noqa: E731
    jugada, corridas = acciones[0], []                          # linea 2
    for d in profundidades:                                     # lineas 3, 4, 12
        if acabado():
            return corridas, dict(jugada=jugada, d=d, generados=cuenta[0], linea=4,
                                  despues_de=None)
        cuenta[0] += 1                                          # R
        alfa, mejor = -INF, jugada                              # linea 5
        orden = [jugada] + [a for a in acciones if a != jugada]  # linea 6
        inicio = cuenta[0] - 1
        for a in orden:
            cuenta[0] += 1
            w = _ab_t(arbol, camino_de[a], d - 1, alfa, INF, evaluar, nombres, cuenta)
            if acabado():                                       # linea 8
                return corridas, dict(jugada=jugada, d=d, generados=cuenta[0], linea=8,
                                      despues_de=a)
            if w == 100:                                        # linea 9
                mejor = a
                break
            if w > alfa:                                        # linea 10
                alfa, mejor = w, a
        jugada = mejor                                          # linea 11
        corridas.append(dict(d=d, orden=orden, jugada=jugada, generados=cuenta[0] - inicio))
    return corridas, dict(jugada=jugada, d=profundidades[-1], generados=cuenta[0], linea=13,
                          despues_de=None)


def decidir_alfa_beta_con_corte(tablero, turno, d, n):
    """DECIDIR-ALFA-BETA con corte en un tablero de peones: α compartido entre
    los hijos de la raiz, jugadas en el orden fijo y sin la salida temprana
    con 100. Devuelve (jugada, valor, nodos generados contando la raiz)."""
    def ab(t, p, d, a, b, c):
        c[0] += 1
        g = ganador(t, p, n)
        if g:
            return 100 * utilidad_simple(g, 0)
        if d == 0:
            return evaluar_peones(t, n)
        v = -INF if p == "B" else INF
        for m in jugadas(t, p, n):
            h = ab(mover(t, m), otro(p), d - 1, a, b, c)
            if p == "B":
                v = max(v, h)
                if v >= b:
                    return v
                a = max(a, v)
            else:
                v = min(v, h)
                if v <= a:
                    return v
                b = min(b, v)
        return v
    c, alfa, mejor = [1], -INF, None
    for m in jugadas(tablero, turno, n):
        w = ab(mover(tablero, m), otro(turno), d - 1, alfa, INF, c)
        if w > alfa:
            alfa, mejor = w, m
    return nombre_jugada(tablero, mejor, n), alfa, c[0]


# La posicion de la clase 3 (fila 1 primero); mueven Blancas.
POSICION_C3 = "B..." + "..BB" + "..N." + "NN.."


def tabla_nodos_generados(profundidades=(1, 2, 3)):
    """Nodos generados (contando la raiz) por arbol y algoritmo, para cada d.

    - T: sin poda = DECIDIR-CON-CORTE; alfa-beta = DECIDIR-ALFA-BETA con
      corte, hijos en el orden dado (izq, centro, der); iterativa = la de la
      pagina, con la jugada lista de la busqueda anterior primero.
    - 4x4 (la posicion de la clase): las jugadas en el orden fijo de la unidad
      (por casilla de origen: a1-a2, d2-d3, d2xc3); alfa-beta sin la salida
      temprana; iterativa = profundizacion_iterativa, con la anterior primero
      y la salida en 100."""
    ds = list(profundidades)
    return {
        ("T", "sin poda"): [decidir_con_corte_t(d)[2] for d in ds],
        ("T", "alfa-beta"): [traza_decidir(ARBOL_T, poda=True, profundidad=d,
                                           evaluar=EVAL_T)["generados"] for d in ds],
        ("T", "iterativa"): [t["generados"] for _, _, t in
                             profundizacion_iterativa_t(ARBOL_T, ds, EVAL_T)],
        ("4x4", "sin poda"): [nodos_con_corte(POSICION_C3, "B", d, 4) for d in ds],
        ("4x4", "alfa-beta"): [decidir_alfa_beta_con_corte(POSICION_C3, "B", d, 4)[2]
                               for d in ds],
        ("4x4", "iterativa"): [c for _, c, _ in profundizacion_iterativa(POSICION_C3, ds, 4)],
    }


# ----------------------------------------------- p5: simular (MCTS) ---
#
# El arbol de la figura de MCTS, antes de la vuelta: {nodo: (padre, quien
# mueve, U de la simulacion que se hizo al crearlo)}. La raiz no simula
# (es el estado de partida): sus cuentas son la suma de sus hijos. Cada otro
# nodo: su simulacion mas las de sus hijos. Asi los conteos salen de los
# cuatro pasos de la pagina y no se escriben a mano.
MCTS_ARBOL = {
    "r": (None, "MAX", None),
    "a": ("r", "MIN", 1),
    "b": ("r", "MIN", -1),
    "a1": ("a", "MAX", 1),
    "a2": ("a", "MAX", -1),
}


def victorias(n, media):
    """G a partir de N simulaciones y su promedio de U (U = ±1): (media+1)/2·N."""
    g = F(media + 1) / 2 * n
    assert g.denominator == 1
    return int(g)


def mcts_cuentas(arbol):
    """{nodo: (G, N)}: victorias de MAX y simulaciones que pasaron por el."""
    hijos = {n: [h for h, (p, _, _) in arbol.items() if p == n] for n in arbol}

    def cuenta(n):
        _, _, u = arbol[n]
        g, s = (0, 0) if u is None else (1 if u == 1 else 0, 1)
        for h in hijos[n]:
            gh, sh = cuenta(h)
            g, s = g + gh, s + sh
        return g, s
    return {n: cuenta(n) for n in arbol}


def mcts_puntaje(media, n, n_padre, c):
    """UCT: media + c·sqrt(ln N(s) / N(s')). media ya vista desde quien elige."""
    return float(media) + float(c) * math.sqrt(math.log(n_padre) / n)


def mcts_vuelta(arbol, c, u):
    """Una vuelta de MCTS sobre `arbol`: seleccion con UCT (MIN cambia el signo
    del promedio de U), expansion de un hijo «nuevo» bajo el nodo sin hijos al
    que llega, simulacion con resultado u y retropropagacion. Devuelve
    dict(camino, padre_nuevo, antes, despues, puntajes)."""
    antes = mcts_cuentas(arbol)
    hijos = {n: [h for h, (p, _, _) in arbol.items() if p == n] for n in arbol}
    camino, n, puntajes = ["r"], "r", {}
    while hijos[n]:
        _, pl, _ = arbol[n]
        signo = 1 if pl == "MAX" else -1
        p = {}
        for h in hijos[n]:
            g, s = antes[h]
            p[h] = mcts_puntaje(signo * F(2 * g - s, s), s, antes[n][1], c)
        puntajes[n] = p
        n = max(hijos[n], key=lambda h: p[h])
        camino.append(n)
    pl_nuevo = "MIN" if arbol[n][1] == "MAX" else "MAX"
    nuevo = {**arbol, "nuevo": (n, pl_nuevo, u)}
    return dict(camino=camino, padre_nuevo=n, antes=antes, despues=mcts_cuentas(nuevo),
                puntajes=puntajes)


# El ejercicio «Decide qué jugada entrega MCTS»: {jugada: (N, promedio de U)}
# tras 100 vueltas en la raiz, donde mueve MAX.
EJERCICIO_MCTS = {"x": (60, F(1, 2)), "y": (30, F(3, 5)), "z": (10, F(1, 5))}


def uct_ejercicio(c, victorias=False, datos=None):
    """{jugada: puntaje UCT} en la raiz del ejercicio, con N(s) = suma de los
    N. Con victorias=True el primer termino es G/N (entre 0 y 1) en vez del
    promedio de U (entre −1 y 1)."""
    datos = datos or EJERCICIO_MCTS
    total = sum(n for n, _ in datos.values())
    return {k: mcts_puntaje((media + 1) / 2 if victorias else media, n, total, c)
            for k, (n, media) in datos.items()}


def mas_simulada(datos):
    return max(datos, key=lambda k: datos[k][0])


# ------------------------------------- p6: de donde sale el bono (UCB) ---
#
# Escala de la p5: cada simulacion da U = +1 o −1, y ū(s′) es su promedio,
# en [−1, 1]. μ(s′) es el promedio verdadero: lo que daria ū(s′) con
# infinitas simulaciones. Hoeffding (citado, no demostrado) para resultados
# independientes en [a, b]: Pr(ū ≤ μ − ε) ≤ exp(−2Nε²/(b − a)²); con
# b − a = 2 queda exp(−Nε²/2). Todo con la biblioteca estandar y semilla
# fija: el mismo llamado da siempre los mismos numeros.

C_TEORIA = 2 * math.sqrt(2)      # el c de UCB1 en la escala ±1 (√2 con G/N)


def cota_hoeffding(n, eps):
    """Cota de Hoeffding para la escala ±1: Pr(ū ≤ μ − ε) ≤ e^(−n·ε²/2)."""
    return math.exp(-n * eps ** 2 / 2)


def margen(delta, n):
    """El ε que deja la cota en δ: e^(−nε²/2) = δ ⇒ ε = √(2·ln(1/δ)/n)."""
    return math.sqrt(2 * math.log(1 / delta) / n)


def bono_ucb(n_padre, n, c=None):
    """c·√(ln N(s)/N(s′)); c=None es el de la teoria, 2√2 (margen con
    δ = N(s)^−4). Una jugada sin probar (N(s′) = 0) tiene bono infinito."""
    if n == 0:
        return INF
    return (C_TEORIA if c is None else c) * math.sqrt(math.log(n_padre) / n)


def puntajes_ucb(datos, c=None, mueve="MAX"):
    """{jugada: puntaje} con datos = {jugada: (N(s′), ū(s′))}, ū medido desde
    MAX. MIN es optimista desde su lado: usa −ū. N(s) = suma de los N(s′)."""
    signo = 1 if mueve == "MAX" else -1
    total = sum(n for n, _ in datos.values())
    return {k: signo * float(u) + bono_ucb(total, n, c) for k, (n, u) in datos.items()}


def mejor(puntajes):
    """La de mayor puntaje; en empate, la primera en el orden de los datos."""
    return max(puntajes, key=puntajes.get)


def prob_gana(mu):
    """Pr(U = +1) para que el promedio verdadero sea μ: (1 + μ)/2."""
    return (1 + mu) / 2


def _resultado(rng, p):
    """Una simulacion: +1 con probabilidad p, si no −1."""
    return 1 if rng.random() < p else -1


def _exacto(x):
    """0.3 como 3/10, no como el binario mas cercano: F(0.3) no es 3/10."""
    return x if isinstance(x, (int, F)) else F(repr(x))


def _umbral(mu, eps, k):
    """El mayor total de U con ū ≤ μ − ε tras k simulaciones: ⌊(μ − ε)·k⌋,
    en fracciones exactas (0.3 − 0.2 en coma flotante no es 0.1)."""
    return math.floor((_exacto(mu) - _exacto(eps)) * k)


def frecuencias_desvio(mu, ns, eps, repeticiones, semilla):
    """{n: fraccion de las repeticiones con ū ≤ μ − ε tras n simulaciones}.
    Cada repeticion es UNA tirada de max(ns) simulaciones; se mira su
    promedio parcial en cada n de ns. Asi la tabla sale en una pasada."""
    rng = random.Random(semilla)
    ns = sorted(set(ns))
    tope, cuenta = ns[-1], {n: 0 for n in ns}
    umbral = {n: _umbral(mu, eps, n) for n in ns}
    p = float(prob_gana(_exacto(mu)))
    for _ in range(repeticiones):
        suma = 0
        for k in range(1, tope + 1):
            suma += _resultado(rng, p)
            if k in umbral and suma <= umbral[k]:
                cuenta[k] += 1
    return {n: F(cuenta[n], repeticiones) for n in ns}


def frecuencia_desvio(mu, n, eps, repeticiones, semilla):
    """Fraccion de `repeticiones` promedios de n simulaciones con ū ≤ μ − ε."""
    return frecuencias_desvio(mu, [n], eps, repeticiones, semilla)[n]


def prob_desvio_exacta(mu, n, eps):
    """Pr(ū ≤ μ − ε) exacta: ū = (2K − n)/n con K ~ Binomial(n, (1+μ)/2)."""
    p = prob_gana(_exacto(mu))
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k)
               for k in range(n + 1) if 2 * k - n <= _umbral(mu, eps, n))


REGLAS_BANDIDO = ("mejor_promedio", "a_veces_al_azar", "ucb")
AL_AZAR = 0.1                    # «a veces al azar»: una vuelta de cada diez


def bandido(regla, mus, vueltas, semilla, c=None, al_azar=AL_AZAR):
    """Elige entre las jugadas de `mus` ({jugada: μ}) `vueltas` veces.

    - "mejor_promedio": prueba cada una una vez (en el orden de mus) y luego
      elige siempre la de mayor ū; en empate, la primera.
    - "a_veces_al_azar": igual, pero con probabilidad al_azar elige una al
      azar (puede caer en la mejor).
    - "ucb": sin probar = bono infinito; luego mayor ū(s′) + c·√(ln N(s)/N(s′)),
      con N(s) = vueltas ya hechas (n_padre) y N(s′) = N[a].

    La suerte de cada jugada es su propia fila de tiradas (la k-esima vez que
    se elige x da siempre el mismo resultado, sea cual sea la regla), y las
    decisiones al azar usan otra: asi las tres reglas comparten la suerte.
    Devuelve dict(N, u, elecciones, resultados, arrepentimiento): N[a] es
    N(s′) y u[a] es ū(s′) de cada jugada; arrepentimiento[k] es lo que se
    perdio en las primeras k + 1 vueltas por no elegir siempre la mejor: la
    suma de μ(mejor) − μ(elegida). La pagina no lo usa (mira la fraccion de
    vueltas en x); las pruebas si."""
    if regla not in REGLAS_BANDIDO:
        raise ValueError(regla)
    nombres = list(mus)
    suerte = {a: random.Random(semilla * 1000 + i) for i, a in enumerate(nombres)}
    dado = random.Random(semilla * 1000 + 999)
    N = {a: 0 for a in nombres}
    # suma_u[a]: la suma de los U de a, asi ū(s′) = suma_u[a] / N[a]. No es
    # G(s′) de la p5 (victorias): con ±1, ū = 2·G/N − 1.
    suma_u = {a: 0 for a in nombres}
    mu_max = max(mus.values())
    p = {a: float(prob_gana(mus[a])) for a in nombres}
    elecciones, resultados, arrep, perdido = [], [], [], 0
    for n_padre in range(vueltas):          # N(s): vueltas ya hechas
        sin_probar = [a for a in nombres if N[a] == 0]
        if regla == "a_veces_al_azar" and not sin_probar and dado.random() < al_azar:
            a = dado.choice(nombres)
        elif sin_probar:
            a = sin_probar[0]
        elif regla == "ucb":
            a = mejor({b: suma_u[b] / N[b] + bono_ucb(n_padre, N[b], c)
                       for b in nombres})
        else:
            a = mejor({b: suma_u[b] / N[b] for b in nombres})
        r = _resultado(suerte[a], p[a])
        N[a] += 1
        suma_u[a] += r
        perdido += mu_max - mus[a]
        elecciones.append(a)
        resultados.append(r)
        arrep.append(perdido)
    return dict(N=N, u={a: (F(suma_u[a], N[a]) if N[a] else None) for a in nombres},
                elecciones=elecciones, resultados=resultados, arrepentimiento=arrep)


def filas_bandido(regla, mus, vueltas, semilla, c=None):
    """La corrida de `bandido`, vuelta por vuelta, para una tabla: dict(vuelta,
    jugada, U, N, u), con N(s′) y ū(s′) de cada jugada DESPUES de esa vuelta;
    `vuelta` es N(s) tras ella."""
    b = bandido(regla, mus, vueltas, semilla, c)
    N, suma_u, filas = {a: 0 for a in mus}, {a: 0 for a in mus}, []
    for n_padre, (a, r) in enumerate(zip(b["elecciones"], b["resultados"]), 1):
        N[a] += 1
        suma_u[a] += r
        filas.append(dict(vuelta=n_padre, jugada=a, U=r, N=dict(N),
                          u={k: (F(suma_u[k], N[k]) if N[k] else None) for k in mus}))
    return filas


@lru_cache(maxsize=None)
def _corridas(regla, mus_items, vueltas, corridas, c):
    """Una entrada por semilla 1..corridas: (veces, N, pagos). veces[k]
    cuenta cuantas de las primeras k vueltas fueron a la mejor jugada
    (veces[0] = 0); pagos[k] es la suma de los U de las primeras k vueltas
    (enteros: U es ±1, asi que los promedios salen exactos); N es
    {jugada: N(s′)} al terminar. Todas las figuras del bandido leen de aqui:
    las 160 corridas de 10 000 vueltas se simulan una sola vez."""
    mus = dict(mus_items)
    la_mejor = max(mus, key=mus.get)
    salida = []
    for semilla in range(1, corridas + 1):
        b = bandido(regla, mus, vueltas, semilla, c)
        veces, k = array("l", [0]), 0
        pagos, total = array("l", [0]), 0
        for a, u in zip(b["elecciones"], b["resultados"]):
            k += a == la_mejor
            total += u
            veces.append(k)
            pagos.append(total)
        salida.append((veces, b["N"], pagos))
    return tuple(salida)


def fraccion_en_la_mejor(regla, mus, marcas, corridas, c=None):
    """{N(s): fraccion de las primeras N(s) vueltas que fueron a la mejor
    jugada, promediada sobre `corridas` corridas con semillas 1..corridas}.
    Es acumulada: en N(s) = 10 000 cuenta tambien las primeras vueltas."""
    por_corrida = _corridas(regla, tuple(mus.items()), max(marcas), corridas, c)
    suma = {m: 0.0 for m in marcas}
    for veces, _, _ in por_corrida:
        for m in marcas:
            suma[m] += veces[m] / m
    return {m: suma[m] / corridas for m in marcas}


def fracciones_finales(regla, mus, vueltas, corridas, c=None):
    """[fraccion de las `vueltas` vueltas que fueron a la mejor jugada, por
    semilla 1..corridas]: lo que promedia fraccion_en_la_mejor en su ultima
    marca, sin promediar."""
    return [veces[vueltas] / vueltas
            for veces, _, _ in _corridas(regla, tuple(mus.items()), vueltas, corridas, c)]


def pago_por_vuelta(regla, mus, marcas, corridas, c=None):
    """{N(s): pago promedio por vuelta de las primeras N(s) vueltas (la suma
    de sus U entre N(s)), promediado sobre `corridas` corridas con semillas
    1..corridas}. Exacto: suma de enteros entre corridas·N(s), en Fraction
    (sin floats que sumar, no depende de como redondee cada Python)."""
    por_corrida = _corridas(regla, tuple(mus.items()), max(marcas), corridas, c)
    total = {m: 0 for m in marcas}
    for _, _, pagos in por_corrida:
        for m in marcas:
            total[m] += pagos[m]
    return {m: F(total[m], corridas * m) for m in marcas}


def pagos_finales(regla, mus, vueltas, corridas, c=None):
    """[pago promedio por vuelta de las `vueltas` vueltas, por semilla
    1..corridas]: lo que promedia pago_por_vuelta en su ultima marca."""
    return [F(pagos[vueltas], vueltas)
            for _, _, pagos in _corridas(regla, tuple(mus.items()), vueltas, corridas, c)]


def eligiendo_la_mejor(regla, mus, marcas, corridas, c=None, ventana=None):
    """{N(s): fraccion de las elecciones que fueron a la mejor jugada en las
    vueltas N(s) − ventana + 1 .. N(s), contando las `corridas` corridas}.
    NO es acumulada: mira solo esas vueltas. Con ventana = 1 es «cuantas
    corridas eligen la mejor en la vuelta N(s)»; la ventana de 10 quita el
    ruido de una sola vuelta. Exacto, en Fraction."""
    ventana = ventana or VENTANA_ELIGIENDO
    por_corrida = _corridas(regla, tuple(mus.items()), max(marcas), corridas, c)
    cuenta = {m: 0 for m in marcas}
    for veces, _, _ in por_corrida:
        for m in marcas:
            cuenta[m] += veces[m] - veces[max(m - ventana, 0)]
    return {m: F(cuenta[m], corridas * min(ventana, m)) for m in marcas}


# El hilo de la p6: las tres jugadas del ejercicio de la p5 (x, y, z), ahora
# con un promedio verdadero oculto. La mejor de verdad es x, la que la p5
# entrega por ser la mas simulada, aunque su ū (0.5) sea menor que el de y
# (0.6 en 30 simulaciones, con suerte). z es mala de verdad.
MUS_HILO = {"x": F(3, 5), "y": F(3, 10), "z": F(-1, 5)}
SEMILLA_ATORA = 36          # «siempre el mejor promedio» se queda en z
VUELTAS_MICRO = 12
# La figura de Hoeffding: la jugada y (μ = 0.3), ε = 0.2.
MU_HOEFFDING, EPS_HOEFFDING = F(3, 10), F(1, 5)
REPS_HOEFFDING, SEMILLA_HOEFFDING = 20000, 1
NS_HOEFFDING = tuple(range(1, 201))
# La figura del bandido: 40 corridas de 10 000 vueltas por regla.
MARCAS_BANDIDO = (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)
CORRIDAS_BANDIDO = 40
# jue-c3-eligiendo-x mira las vueltas N(s) − 9 .. N(s): una sola vuelta de
# 40 corridas salta de 33 a 40 entre marcas vecinas en «a veces al azar».
VENTANA_ELIGIENDO = 10


@lru_cache(maxsize=None)
def tabla_hoeffding():
    """{n: (frecuencia observada, cota)} de la figura jue-c3-hoeffding."""
    f = frecuencias_desvio(MU_HOEFFDING, NS_HOEFFDING, EPS_HOEFFDING,
                           REPS_HOEFFDING, SEMILLA_HOEFFDING)
    return {n: (f[n], cota_hoeffding(n, float(EPS_HOEFFDING))) for n in NS_HOEFFDING}


# Las cuatro filas de las figuras del bandido: {fila: (regla, c)}. ucb_c1 es
# la c de la pagina 5: explora menos que la teorica y aqui converge antes.
FILAS_BANDIDO = {"mejor_promedio": ("mejor_promedio", None),
                 "a_veces_al_azar": ("a_veces_al_azar", None),
                 "ucb": ("ucb", None), "ucb_c1": ("ucb", 1)}
# Una corrida «atorada» dejo menos de la mitad de sus vueltas en la mejor.
UMBRAL_ATORADA = F(1, 2)


def tabla_bandido():
    """{regla: {N(s): fraccion en la mejor}} de la figura jue-c3-bandido."""
    return {f: fraccion_en_la_mejor(r, MUS_HILO, MARCAS_BANDIDO, CORRIDAS_BANDIDO, c)
            for f, (r, c) in FILAS_BANDIDO.items()}


def tabla_pago():
    """{regla: {N(s): pago promedio por vuelta}} de la figura jue-c3-pago."""
    return {f: pago_por_vuelta(r, MUS_HILO, MARCAS_BANDIDO, CORRIDAS_BANDIDO, c)
            for f, (r, c) in FILAS_BANDIDO.items()}


def tabla_eligiendo_x():
    """{regla: {N(s): fraccion de corridas que eligen x}} de la figura
    jue-c3-eligiendo-x (ventana VENTANA_ELIGIENDO, no acumulada)."""
    return {f: eligiendo_la_mejor(r, MUS_HILO, MARCAS_BANDIDO, CORRIDAS_BANDIDO, c)
            for f, (r, c) in FILAS_BANDIDO.items()}


def pago_esperado_reparto(fila="mejor_promedio", vueltas=None, corridas=CORRIDAS_BANDIDO):
    """El pago por vuelta que se espera de una regla si cada corrida se
    queda en la jugada que mas eligio: dict(en=Counter {jugada: corridas},
    esperado=Σ corridas·μ / total). Para «siempre el mejor promedio»: 34 en
    x, 5 en y, 1 en z, (34·0.6 + 5·0.3 − 0.2)/40 = 217/400 = 0.5425. No
    cuenta las primeras vueltas, que exploran: por eso lo simulado queda un
    poco abajo o arriba."""
    vueltas = vueltas or max(MARCAS_BANDIDO)
    r, c = FILAS_BANDIDO[fila]
    en = Counter(max(N, key=N.get)
                 for _, N, _ in _corridas(r, tuple(MUS_HILO.items()), vueltas, corridas, c))
    total = 0
    for a, k in en.items():
        total += k * MUS_HILO[a]
    return dict(en=en, esperado=F(total) / corridas)


def reparto_bandido(vueltas=None, corridas=CORRIDAS_BANDIDO):
    """{fila: reparto} de la figura jue-c3-bandido-corridas: lo que el
    promedio de jue-c3-bandido esconde. Por fila: n (corridas), fracciones
    (una por semilla), atoradas (cuantas con fraccion < 1/2), en (Counter de
    la jugada que mas eligio cada atorada), minimo, mediana, maximo y
    promedio (el mismo numero que tabla_bandido en su ultima marca)."""
    vueltas = vueltas or max(MARCAS_BANDIDO)
    salida = {}
    for f, (r, c) in FILAS_BANDIDO.items():
        corr = _corridas(r, tuple(MUS_HILO.items()), vueltas, corridas, c)
        fr = [veces[vueltas] / vueltas for veces, _, _ in corr]
        atoradas = [max(N, key=N.get) for (_, N, _), x in zip(corr, fr) if x < UMBRAL_ATORADA]
        suma = 0.0
        for x in fr:
            suma += x
        salida[f] = dict(n=corridas, fracciones=fr, atoradas=len(atoradas),
                         en=Counter(atoradas), minimo=min(fr),
                         mediana=statistics.median(fr), maximo=max(fr),
                         promedio=suma / corridas)
    return salida


def tope_a_veces_al_azar(n_jugadas=3, al_azar=AL_AZAR):
    """Lo que se espera que «a veces al azar» deje en la mejor cuando ya la
    encontro: la elige en las vueltas sin azar (1 − al_azar) y en 1 de cada
    n_jugadas de las de azar. Con 3 jugadas y 10 %: 0.9 + 0.1/3 = 14/15. Es
    un valor esperado, no un techo: una corrida con menos tiradas al azar de
    lo esperado lo pasa."""
    a = _exacto(al_azar)
    return (1 - a) + a / n_jugadas


def exponente_de_c(c):
    """El k de δ = N(s)^−k que da el bono con esa c: ε = √(2·ln(1/δ)/N(s′))
    = √(2k)·√(ln N(s)/N(s′)), asi que c = √(2k) y k = c²/2."""
    return c * c / 2


def delta_de_c(c, n_padre):
    """La δ que esconde una c con N(s) = n_padre: N(s)^(−c²/2)."""
    return n_padre ** (-exponente_de_c(c))


def puntajes_ucb_en_vuelta(vuelta, semilla=SEMILLA_ATORA, c=None, mus=MUS_HILO):
    """(N(s), {jugada: puntaje}) justo antes de elegir en la vuelta `vuelta`
    (la primera es la 1) de la corrida de UCB con esa semilla y esa c: los
    datos son los de las vuelta − 1 vueltas ya hechas, como en `bandido`."""
    datos = {a: (0, F(0)) for a in mus}
    if vuelta > 1:
        ultima = filas_bandido("ucb", mus, vuelta - 1, semilla, c)[-1]
        datos = {a: (ultima["N"][a], ultima["u"][a] or F(0)) for a in mus}
    return vuelta - 1, puntajes_ucb(datos, c)


# Un nodo donde mueve MIN, para el ejercicio final: {jugada: (N(s′), ū(s′))},
# ū medido desde MAX. Con c = 2√2 la seleccion va a r (poco probada); con
# c = 1, a p. Se entrega p, la mas simulada. Cada ū sale de partidas enteras
# (victorias_de): la version vieja, q con N = 15 y ū = 0, pedia 7.5 victorias.
EJEMPLO_MIN = {"p": (30, F(-1, 5)), "q": (16, F(1, 4)), "r": (4, F(1, 2))}


def victorias_de(n, u):
    """G(s′) = N(s′)·(ū + 1)/2: las victorias de MAX que dan ese promedio con
    pagos ±1 y sin empates. ValueError si no es entero: ese ū no puede salir
    de N(s′) partidas. ValueError tambien si n no es un entero positivo."""
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError(f"N(s′) = {n!r} no es un numero de partidas: pide un entero > 0")
    g = F(n) * (_exacto(u) + 1) / 2
    if g.denominator != 1 or not 0 <= g <= n:
        raise ValueError(f"ū = {u} no sale de {n} partidas con U = ±1: G = {g}")
    return int(g)


def regreso_de_atoradas(vueltas=None, corridas=CORRIDAS_BANDIDO, mus=MUS_HILO):
    """{semilla: dict(en, ultima_x, u_x, puede_volver)} de las corridas de
    «siempre el mejor promedio» que no se quedaron en la mejor jugada (x).
    Solo para el hilo de la p6: `mus` tiene que ser MUS_HILO (ValueError si
    no), porque el razonamiento de puede_volver supone que x es la mejor y
    la primera en los desempates.
    ultima_x es la ultima vuelta que eligio x; u_x, el ū con que x quedo
    congelada. puede_volver dice si x PODRIA volver a elegirse en alguna
    vuelta futura: la jugada atorada, con al menos una victoria, nunca baja
    a ū = −1, y en empate gana x (va primero); asi que x solo queda fuera
    para siempre si su ū congelado es −1 y la atorada ya gano alguna vez.
    Si no, una racha mala de la atorada podria devolver la eleccion a x."""
    if list(mus.items()) != list(MUS_HILO.items()):  # tambien el orden: x primero
        raise ValueError("regreso_de_atoradas solo vale para MUS_HILO")
    vueltas = vueltas or max(MARCAS_BANDIDO)
    la_mejor = "x"
    salida = {}
    for semilla in range(1, corridas + 1):
        b = bandido("mejor_promedio", mus, vueltas, semilla)
        en = max(b["N"], key=b["N"].get)
        if en == la_mejor:
            continue
        ganadas = sum(r == 1 for a, r in zip(b["elecciones"], b["resultados"]) if a == en)
        u_x = b["u"][la_mejor]
        salida[semilla] = dict(
            en=en, u_x=u_x, ganadas_atorada=ganadas,
            ultima_x=max(i for i, a in enumerate(b["elecciones"], 1) if a == la_mejor),
            puede_volver=not (u_x == -1 and ganadas > 0))
    return salida


def ultimo_cambio_de_eleccion(fila="mejor_promedio", vueltas=None,
                              corridas=CORRIDAS_BANDIDO):
    """{semilla: la ultima vuelta (la primera es la 1) cuya eleccion difiere
    de la de la vuelta anterior; 0 si nunca cambia}, por regla de
    FILAS_BANDIDO. Sin bono, la mayor es la 89 (semilla 9): en las ventanas
    de jue-c3-eligiendo-x desde N(s) = 100 (vueltas 91 a 100 en adelante)
    cada corrida repite una sola jugada."""
    vueltas = vueltas or max(MARCAS_BANDIDO)
    r, c = FILAS_BANDIDO[fila]
    salida = {}
    for semilla in range(1, corridas + 1):
        e = bandido(r, MUS_HILO, vueltas, semilla, c)["elecciones"]
        salida[semilla] = max((i + 1 for i in range(1, len(e)) if e[i] != e[i - 1]),
                              default=0)
    return salida


# ------------------------- 7.3.7: un arbol, todos los algoritmos (T±) ---
#
# T± es el arbol T con finales en la escala de U (+1 gana MAX, −1 gana MIN,
# 0 empate) y UN cambio de forma: D tiene tres hijos en vez de dos (15
# nodos en vez de 14). Con dos hijos por nodo de MIN, un volado parejo
# entre −1 y lo mejor que puede haber (+1) vale 0: a lo mas empata con una
# jugada que vale 0 y nunca la supera, asi que con la forma exacta de T y
# una sola jugada mejor, ningun nodo de MIN convertido en dado cambia la
# jugada (busqueda exhaustiva en dados_que_cambian_la_jugada_forma_t). Con tres hijos,
# (+1, +1, −1) promedia 1/3 > 0.
#
# Lo que muestra cada algoritmo:
# - minimax: V = 0, juega centro (el empate es lo mejor que MAX asegura);
# - el corte a d = 1 elige izq por EVAL(I) = 60, que no ve la captura ix;
# - la quietud a d = 1 mira esa captura, I pasa a −100 y elige centro;
# - un dado en D (expectiminimax) juega der, por 1/3;
# - Monte Carlo plano promedia con TODOS al azar y tambien juega der;
# - UCT construye arbol, MIN deja de jugar al azar y acaba en centro.
ARBOL_TPM = ((1, -1), ((0, -1), (1, -1)), (-1, 1, 1))
# EVAL de T± en la escala 100·U, para los nodos internos que puede tocar un
# corte. Es un dato, como EVAL_T: I parece ir ganando (60) porque la
# estimacion no ve la captura ix; C1 y C2 se estiman por debajo de 100.
EVAL_TPM = {"I": 60, "C": 20, "D": 10, "C1": 10, "C2": 50}
# Las jugadas que son captura, por camino: ix, la segunda jugada de MIN en I.
CAPTURAS_TPM = frozenset({(0, 1)})
# El nodo de MIN que el expectiminimax de la pagina convierte en dado parejo.
DADO_TPM = ("D",)
JUGADAS_RAIZ = ("izq", "centro", "der")


def dados_que_cambian_la_jugada_forma_t(hojas_d=2):
    """Cuantos arboles con la forma de T (D con `hojas_d` hojas) y finales en
    {−1, 0, +1}, con una sola jugada de minimax en la raiz, cambian de jugada
    (sin empate) al convertir uno de I, C o D en un dado parejo. Con
    hojas_d = 2 (la forma exacta de T) son 0: por eso T± tiene tres en D."""
    total = 0
    for hojas in product((-1, 0, 1), repeat=6 + hojas_d):
        arbol = (hojas[:2], (hojas[2:4], hojas[4:6]), hojas[6:])
        vs = [minimax_arbol(h, False) for h in arbol]
        if vs.count(max(vs)) > 1:
            continue
        jugada = vs.index(max(vs))
        for y in range(3):
            if y == jugada:
                continue
            nombre = "ICD"[y]
            _, valores, _ = expectiminimax_t(arbol, (nombre,))
            ws = vs[:y] + [valores[nombre]] + vs[y + 1:]
            if ws.count(max(ws)) == 1 and ws.index(max(ws)) == y:
                total += 1
                break
    return total


def escalar_arbol(arbol, k):
    """El mismo arbol con cada final multiplicado por k (U → 100·U)."""
    if not isinstance(arbol, tuple):
        return k * arbol
    return tuple(escalar_arbol(h, k) for h in arbol)


def nombres_hojas_tpm(arbol=ARBOL_TPM):
    """{camino de una hoja: nombre de la jugada que lleva a ella}: i1 e ix
    bajo I (la x de las capturas, como en d2xc3); c1a, c1b bajo C1; c2a, c2b
    bajo C2; d1, d2, d3 bajo D."""
    res = {}
    for i, hijo in enumerate(arbol):
        letra = "icd"[i]
        for k, nieto in enumerate(hijo):
            if isinstance(nieto, tuple):
                for m in range(len(nieto)):
                    res[(i, k, m)] = f"{letra}{k + 1}{'abc'[m]}"
            else:
                res[(i, k)] = f"{letra}x" if (i, k) in CAPTURAS_TPM else f"{letra}{k + 1}"
    return res


def _jugada_estricta(valores):
    """La primera jugada de la raiz con el mayor valor (DECIDIR usa «>»)."""
    mejor, jugada = -INF, None
    for a, w in zip(JUGADAS_RAIZ, valores):
        if w > mejor:
            mejor, jugada = w, a
    return jugada


def minimax_tpm(arbol=ARBOL_TPM):
    """(jugada, V, {izq/centro/der: V del hijo}, nodos generados)."""
    vs = [minimax_arbol(h, False) for h in arbol]
    return (_jugada_estricta(vs), max(vs), dict(zip(JUGADAS_RAIZ, vs)),
            contar_nodos(arbol))


ORDENES_TPM = ("dado", "al revés", "centro primero")


def alfa_beta_tpm(orden="dado", arbol=ARBOL_TPM):
    """DECIDIR-ALFA-BETA en T± con tres ordenes: el dado; «al revés» (todos
    los hijos invertidos, como jue-alfa-beta-invertido); «centro primero»
    (solo la raiz cambia: la jugada de minimax va primero, como la deja la
    profundizacion iterativa). (jugada, valor, generados, caminos podados)."""
    if orden == "centro primero":
        t = traza_decidir(arbol, poda=True, orden={"R": ["C", "I", "D"]})
        return t["jugada"], t["valor"], t["generados"], _podados_por_camino(arbol, t)
    r = alfa_beta_arbol(arbol, invertir=(orden == "al revés"))
    raiz = {c[0]: v for c, tipo, a, b, v, corte in r["traza"] if len(c) == 1}
    jugada = None
    mejor = -INF
    visita = sorted(raiz, reverse=(orden == "al revés"))
    for i in visita:
        if raiz[i] > mejor:
            mejor, jugada = raiz[i], JUGADAS_RAIZ[i]
    return jugada, r["valor"], r["generados"], sorted(r["podados"])


def _podados_por_camino(arbol, t):
    """Caminos de las raices de los subarboles que una traza no genero."""
    generados = set(t["caminos_generados"])
    res = []

    def visitar(nodo, camino):
        if camino not in generados:
            res.append(camino)
            return
        if isinstance(nodo, tuple):
            for i, h in enumerate(nodo):
                visitar(h, camino + (i,))
    visitar(arbol, ())
    return sorted(res)


def expectiminimax_tpm(azar=DADO_TPM, arbol=ARBOL_TPM):
    """(jugada, {nombre: valor exacto}) con los nodos de `azar` como dados
    parejos. Las hojas comparten nombre («1»), asi que solo valen los de
    los nodos internos."""
    jugada, valores, _ = expectiminimax_t(arbol, azar)
    return jugada, {k: v for k, v in valores.items() if k in ("R", "I", "C", "D", "C1", "C2")}


def corte_tpm(d, evaluar=None, arbol=ARBOL_TPM):
    """DECIDIR-CON-CORTE(R, d) en T± (finales 100·U): (jugada, valor,
    {izq/centro/der: valor con corte}, generados)."""
    t = traza_decidir(escalar_arbol(arbol, 100), profundidad=d,
                      evaluar=evaluar or EVAL_TPM)
    ws = {JUGADAS_RAIZ["ICD".index(f["hijo"])]: f["w"] for f in t["filas"]
          if f["evento"] == "raiz"}
    return t["jugada"], t["valor"], ws, t["generados"]


def quietud_tpm(d, evaluar=None, capturas=CAPTURAS_TPM, arbol=ARBOL_TPM, valores=None):
    """MINIMAX-CON-CORTE con busqueda de quietud en T± (finales 100·U): en un
    nodo de corte, el que mueve elige entre quedarse con EVAL o seguir una de
    sus capturas, y solo las capturas se generan. (jugada, valor,
    {izq/centro/der: valor}, generados, caminos generados).

    Si `valores` es un dict, se llena con {camino: valor} de cada nodo
    interno generado (R incluida); no cambia nada de lo que devuelve."""
    evaluar = evaluar or EVAL_TPM
    if valores is None:
        valores = {}
    nombres = nombres_t(arbol)
    generados = [()]

    def quieta(camino):
        nodo = nodo_en(arbol, camino)
        if not isinstance(nodo, tuple):
            return 100 * nodo
        es_max = len(camino) % 2 == 0
        v = evaluar[nombres[camino][0]]
        for i in range(len(nodo)):
            if camino + (i,) in capturas:
                generados.append(camino + (i,))
                h = quieta(camino + (i,))
                v = max(v, h) if es_max else min(v, h)
        valores[camino] = v
        return v

    def valor(camino, prof):
        nodo = nodo_en(arbol, camino)
        if not isinstance(nodo, tuple):
            return 100 * nodo
        if prof == d:
            return quieta(camino)
        hs = []
        for i in range(len(nodo)):
            generados.append(camino + (i,))
            hs.append(valor(camino + (i,), prof + 1))
        valores[camino] = max(hs) if len(camino) % 2 == 0 else min(hs)
        return valores[camino]

    ws = []
    for i in range(len(arbol)):
        generados.append((i,))
        ws.append(valor((i,), 1))
    valores[()] = max(ws)
    return (_jugada_estricta(ws), max(ws), dict(zip(JUGADAS_RAIZ, ws)), len(generados),
            generados)


def quietud_con_todo_captura_tpm(d=1, arbol=ARBOL_TPM):
    """quietud_tpm(d) en T± con TODAS las jugadas bajo la profundidad d
    marcadas como captura: las capturas llegan a todos los finales, y aun
    asi en cada nodo de corte la opcion de quedarse vale EVAL y puede
    decidir. Con d = 1 da centro con 10, no el 0 de minimax: por eso
    GARANTIZA_TPM["quietud"] dice «antes de cortar». Mismo formato que
    quietud_tpm."""
    capturas = frozenset(c for c in ids_tpm(arbol) if len(c) > d)
    return quietud_tpm(d, capturas=capturas, arbol=arbol)


def decidir_con_ventana_tpm(alfa, beta, arbol=ARBOL_TPM, primera=False):
    """El ciclo de la raiz de DECIDIR-ALFA-BETA (lineas 2-6) con α inicial
    `alfa` y la ventana (α, beta) para los hijos: cambia de jugada solo si
    un hijo devuelve w > α. Con primera=True, mejor_jugada arranca en la
    primera jugada en vez de en «ninguna». Sale del ciclo cuando α llega a
    beta: con la ventana en (−1, +1), al ver un +1 ya no hay nada mejor, y
    seguir buscaria hijos con la ventana cerrada. (jugada o None, α final,
    [jugadas de la raiz que se buscaron]).

    Con α = −1 (abrir la ventana en los limites de U) y todas las jugadas
    perdiendo, ningun w supera a α y, sin primera=True, no hay jugada."""
    mejor = JUGADAS_RAIZ[0] if primera else None
    buscadas = []
    for a, hijo in zip(JUGADAS_RAIZ, arbol):
        buscadas.append(a)
        w = alfa_beta_arbol(hijo, es_max=False, alfa=alfa, beta=beta)["valor"]
        if w > alfa:
            alfa, mejor = w, a
        if alfa >= beta:
            break
    return mejor, alfa, buscadas


def posiciones_fronteras(lado):
    """Posiciones distintas de Fronteras (7.3.9) en un tablero lado×lado:
    tras k jugadas hay k casillas pintadas, ceil(k/2) de Rojo (empieza) y
    floor(k/2) de Azul. Es lo que recorreria una busqueda que guarda cada
    posicion una sola vez (tabla de transposicion), en vez de los lado²!
    ordenes de jugadas."""
    n = lado * lado
    return sum(math.comb(n, k) * math.comb(k, (k + 1) // 2) for k in range(n + 1))


def iterativa_tpm(profundidades=(1, 2, 3), evaluar=None, arbol=ARBOL_TPM):
    """PROFUNDIZACION-ITERATIVA en T± (alfa-beta con corte, la jugada anterior
    primero): [(d, orden de la raiz, jugada, valor, generados)] y el total."""
    filas = [(d, orden, t["jugada"], t["valor"], t["generados"])
             for d, orden, t in profundizacion_iterativa_t(
                 escalar_arbol(arbol, 100), profundidades, evaluar or EVAL_TPM)]
    return filas, sum(f[4] for f in filas)


ALGORITMOS_ORDEN_TPM = ("minimax", "alfa-beta", "corte", "quietud", "iterativa")


def orden_generados_tpm(algoritmo, d=1, arbol=ARBOL_TPM):
    """Los caminos de T± en el orden en que `algoritmo` los genera, la raiz
    primero: lo que recorre la animacion de las radiografias (7.3.6).

    - "minimax": DECIDIR-MINIMAX, los 15 en profundidad;
    - "alfa-beta": DECIDIR-ALFA-BETA con el orden dado;
    - "corte": DECIDIR-CON-CORTE(R, d), finales en 100·U con EVAL_TPM;
    - "quietud": quietud_tpm(d): tras cada nodo de corte, sus capturas;
    - "iterativa": una lista por busqueda (d = 1, 2, 3), cada una con la
      jugada de la anterior primero.
    Los caminos van en el orden *dado* del arbol aunque se recorra en otro."""
    if algoritmo == "minimax":
        return list(traza_decidir(arbol)["caminos_generados"])
    if algoritmo == "alfa-beta":
        return list(_generados_alfa_beta("dado", arbol))
    if algoritmo == "corte":
        return list(traza_decidir(escalar_arbol(arbol, 100), profundidad=d,
                                  evaluar=EVAL_TPM)["caminos_generados"])
    if algoritmo == "quietud":
        return list(quietud_tpm(d, arbol=arbol)[4])
    if algoritmo == "iterativa":
        return [list(t["caminos_generados"]) for _, _, t in profundizacion_iterativa_t(
            escalar_arbol(arbol, 100), (1, 2, 3), EVAL_TPM)]
    raise ValueError(algoritmo)


def todos_al_azar_tpm(arbol=ARBOL_TPM):
    """Expectiminimax con TODOS los nodos bajo la raiz como dados parejos,
    tambien los de MAX (C1 y C2): el limite de Monte Carlo plano. La raiz
    sigue eligiendo el maximo. (jugada, {izq/centro/der: μ exacto})."""
    jugada, valores = expectiminimax_tpm(("I", "C", "D", "C1", "C2"), arbol)
    return jugada, {a: valores[n] for a, n in zip(JUGADAS_RAIZ, "ICD")}


def rival_al_azar_tpm(arbol=ARBOL_TPM):
    """La trampa: solo el RIVAL al azar (I, C y D como dados; C1 y C2 siguen
    maximizando). No es el limite de MC plano: C sube a 1/2 y juega centro.
    (jugada, {izq/centro/der: valor exacto})."""
    jugada, valores = expectiminimax_tpm(("I", "C", "D"), arbol)
    return jugada, {a: valores[n] for a, n in zip(JUGADAS_RAIZ, "ICD")}


def simular_tpm(nodo, rng):
    """Una partida al azar desde `nodo` (subarbol): cada jugada con la misma
    probabilidad, de los dos lados, hasta un final. Devuelve su U."""
    while isinstance(nodo, tuple):
        nodo = nodo[rng.randrange(len(nodo))]
    return nodo


def distribucion_simulacion(nodo):
    """{U: probabilidad exacta} de una simulacion desde `nodo`."""
    if not isinstance(nodo, tuple):
        return {nodo: F(1)}
    res = {}
    for h in nodo:
        for u, p in distribucion_simulacion(h).items():
            res[u] = res.get(u, 0) + p / len(nodo)
    return res


def mc_plano_tpm(k, semilla, arbol=ARBOL_TPM):
    """Monte Carlo plano en T±: k simulaciones por jugada de la raiz, en el
    orden izq, centro, der, con un solo generador random.Random(semilla).
    Entrega la de mayor promedio; en un empate, la primera en ese orden.
    (jugada, {jugada: suma de U})."""
    rng = random.Random(semilla)
    sumas = {a: sum(simular_tpm(h, rng) for _ in range(k))
             for a, h in zip(JUGADAS_RAIZ, arbol)}
    return _jugada_estricta(list(sumas.values())), sumas


def simulaciones_mc_plano_tpm(k, semilla, arbol=ARBOL_TPM):
    """Las simulaciones de mc_plano_tpm(k, semilla), una por una y con el
    mismo generador en el mismo orden: [(jugada de la raiz, camino hasta el
    final, U)]. Es lo que dibuja la radiografia de Monte Carlo plano: por
    donde paso cada partida, que no se guarda."""
    rng = random.Random(semilla)
    res = []
    for i, (a, h) in enumerate(zip(JUGADAS_RAIZ, arbol)):
        for _ in range(k):
            camino, nodo = (i,), h
            while isinstance(nodo, tuple):
                m = rng.randrange(len(nodo))
                camino, nodo = camino + (m,), nodo[m]
            res.append((a, camino, nodo))
    return res


@lru_cache(maxsize=None)
def reparto_mc_plano_tpm(k, semillas=1000, arbol=ARBOL_TPM):
    """{jugada: en cuantas de las semillas 0..semillas−1 la entrega MC plano}
    y cuantas de esas corridas se decidieron por un empate de promedios."""
    cuenta = {a: 0 for a in JUGADAS_RAIZ}
    empates = 0
    for s in range(semillas):
        jugada, sumas = mc_plano_tpm(k, s, arbol)
        cuenta[jugada] += 1
        empates += list(sumas.values()).count(max(sumas.values())) > 1
    return cuenta, empates


@lru_cache(maxsize=None)
def prob_mc_plano_tpm(k, arbol=ARBOL_TPM):
    """{jugada: probabilidad exacta de que MC plano la entregue} con k
    simulaciones por jugada y el desempate «la primera»: der gana solo si su
    suma supera estrictamente a las otras dos; centro, si supera a izq y no
    es superada por der; izq, en el resto."""
    def suma(nodo):
        d = distribucion_simulacion(nodo)
        res = {0: F(1)}
        for _ in range(k):
            nuevo = {}
            for s, p in res.items():
                for u, q in d.items():
                    nuevo[s + u] = nuevo.get(s + u, 0) + p * q
            res = nuevo
        return res
    di, dc, dd = (suma(h) for h in arbol)

    def hasta(d, m):          # Pr(suma <= m)
        return sum((p for s, p in d.items() if s <= m), F(0))
    prob = {a: F(0) for a in JUGADAS_RAIZ}
    for si, pi in di.items():
        for sc, pc in dc.items():
            m = max(si, sc)
            p_no_der = hasta(dd, m)
            prob["der"] += pi * pc * (1 - p_no_der)
            prob["centro" if sc > si else "izq"] += pi * pc * p_no_der
    return prob


def uct_tpm(c, vueltas, semilla, arbol=ARBOL_TPM):
    """MCTS con UCT en T±, con las reglas de «Simular en vez de evaluar»:
    la seleccion baja mientras el nodo tenga todos sus hijos en el arbol,
    por el de mayor ū + c·√(ln N(s)/N(s′)) (MIN usa −ū; empate → el primero);
    la expansion agrega el primer hijo que falta, en el orden dado; la
    simulacion juega al azar desde el hijo nuevo (un final da su U); la
    retropropagacion suma 1 y U a cada nodo del camino. La raiz no simula.
    ū es el promedio de U (con empates, no 2G/N − 1).

    Devuelve dict(N, S: {camino: N y suma de U}, mas_simulada: la de la raiz
    tras cada vuelta, empate → la primera en el orden dado; caminos; U: el
    U que retropropago cada vuelta)."""
    rng = random.Random(semilla)
    N, S = {(): 0}, {(): 0}
    mas, caminos, us = [], [], []
    for _ in range(vueltas):
        camino = [()]
        nodo = arbol
        while True:
            if not isinstance(nodo, tuple):
                u = nodo
                break
            cam = camino[-1]
            hijos = [cam + (i,) for i in range(len(nodo))]
            falta = [h for h in hijos if h not in N]
            if falta:
                h = falta[0]
                N[h], S[h] = 0, 0
                camino.append(h)
                u = simular_tpm(nodo[h[-1]], rng)
                break
            signo = 1 if len(cam) % 2 == 0 else -1
            ln = math.log(N[cam])

            def puntaje(h):
                return signo * S[h] / N[h] + c * math.sqrt(ln / N[h])
            elegido = max(hijos, key=puntaje)
            camino.append(elegido)
            nodo = nodo[elegido[-1]]
        for x in camino:
            N[x] += 1
            S[x] += u
        caminos.append(tuple(camino))
        us.append(u)
        raiz = [(i,) for i in range(len(arbol))]
        mas.append(JUGADAS_RAIZ[max(raiz, key=lambda h: N.get(h, 0))[0]])
    return dict(N=N, S=S, mas_simulada=mas, caminos=caminos, U=us)


VUELTAS_UCT_TPM = 200        # «para siempre» = hasta esta vuelta (con 2000 da lo mismo)
SEMILLAS_UCT_TPM = 500
C_UCT_TPM = (1, C_TEORIA)


def vuelta_desde_la_que_tpm(c, semilla, jugada="centro", vueltas=VUELTAS_UCT_TPM):
    """La primera vuelta desde la cual `jugada` es la mas simulada en todas
    las siguientes, hasta `vueltas`; None si al final no lo es."""
    mas = uct_tpm(c, vueltas, semilla)["mas_simulada"]
    if mas[-1] != jugada:
        return None
    k = len(mas)
    while k > 0 and mas[k - 1] == jugada:
        k -= 1
    return k + 1


def _percentil(xs, q):
    """El de la posicion q·(n−1) en la lista ordenada (sin interpolar)."""
    xs = sorted(xs)
    return xs[int(q * (len(xs) - 1))]


@lru_cache(maxsize=None)
def _vueltas_uct_tpm(c, semillas, vueltas):
    return tuple(vuelta_desde_la_que_tpm(c, s, vueltas=vueltas) for s in range(semillas))


def reparto_uct_tpm(c, semillas=SEMILLAS_UCT_TPM, vueltas=VUELTAS_UCT_TPM):
    """La vuelta desde la que centro queda como la mas simulada, en las
    semillas 0..semillas−1: dict(minimo, p10, mediana, p90, maximo, nunca,
    vueltas: la lista)."""
    vs = list(_vueltas_uct_tpm(c, semillas, vueltas))
    ok = [v for v in vs if v is not None]
    return dict(minimo=min(ok), p10=_percentil(ok, 0.1), mediana=_percentil(ok, 0.5),
                p90=_percentil(ok, 0.9), maximo=max(ok), nunca=len(vs) - len(ok),
                vueltas=vs)


SEMILLA_TPM = 0              # la corrida de la pagina: MC plano y UCT
SIMS_MC_TPM = (5, 10, 50)    # simulaciones por jugada en el reparto
SEMILLAS_MC_TPM = 1000
VUELTAS_PAGINA_TPM = 40      # la corrida de UCT que muestra la pagina


def ids_tpm(arbol=ARBOL_TPM):
    """{camino: id} para todos los nodos de T±: R, I, C, D, C1, C2 y las
    hojas por la jugada que lleva a ellas (i1, …, d3)."""
    res = {c: n for c, (n, _) in nombres_t(arbol).items()
           if isinstance(nodo_en(arbol, c), tuple)}
    res.update(nombres_hojas_tpm(arbol))
    return res


def _ids(caminos, arbol=ARBOL_TPM):
    ids = ids_tpm(arbol)
    return [ids[tuple(c)] for c in caminos]


def _generados_alfa_beta(orden, arbol=ARBOL_TPM):
    if orden == "centro primero":
        return traza_decidir(arbol, poda=True, orden={"R": ["C", "I", "D"]})["caminos_generados"]
    r = alfa_beta_arbol(arbol, invertir=(orden == "al revés"))
    return [f[0] for f in r["traza"]]


# «¿Garantiza V?»: un rasgo del algoritmo, no de la corrida (la convencion
# unica de las tablas de 7.3.7-7.3.9, las fichas y el interactivo): si, por
# como funciona, devuelve el valor minimax. La quietud dice «antes de cortar»:
# aunque sus capturas lleguen a todos los finales, en cada nodo de corte la
# opcion de quedarse vale EVAL y puede decidir (quietud_con_todo_captura_tpm).
GARANTIZA_TPM = {
    "minimax": "Sí",
    "expectiminimax": "Sí, el V del juego con dado",
    "alfa-beta": "Sí, en la raíz",
    "corte": "No, salvo si llega a los finales",
    "quietud": "No, salvo si llega a los finales antes de cortar",
    "iterativa": "No, salvo si llega a los finales",
    "Monte Carlo plano": "No",
    "UCT": "No (con tiempo sin límite converge a él, con cualquier c > 0)",
}


def tabla_t_pm(arbol=ARBOL_TPM):
    """Una fila por algoritmo corrido sobre T±, para la tabla de 7.3.7, en el
    orden del curso (minimax, expectiminimax, alfa-beta en orden dado y al
    revés, corte d = 1..3, quietud, iterativa, Monte Carlo plano con 5, 10 y
    50 simulaciones por jugada, UCT):
    dict(algoritmo, jugada, valor, tipo, escala, nodos, simulaciones, garantiza,
    da_v_aqui, nota).

    tipo: «V» (minimax y alfa-beta), «V con dado» (otro juego: D es azar),
    «valor con corte» (EVAL donde corta, 100·U en los finales), «valor con
    quietud» (en el corte, lo mejor entre quedarse con EVAL y seguir las
    capturas), «ū» (promedio de simulaciones; el limite μ va en la nota).
    nodos: NO miden el mismo trabajo en todas las filas. En las busquedas,
    nodos generados contando R (con repeticion en la iterativa, que suma sus
    tres busquedas); en MC plano, nodos distintos que tocaron sus
    simulaciones; en UCT, nodos que quedaron guardados en su arbol (corrida
    de la pagina, semilla SEMILLA_TPM). simulaciones: partidas al azar
    jugadas hasta un final (k por jugada en MC plano, una por vuelta en
    UCT); None en las busquedas. garantiza: el texto de la
    convencion GARANTIZA_TPM, igual para toda fila de una familia.
    da_v_aqui: si en T± el numero coincide con el V que le corresponde —el
    de minimax, 0, en su escala (U o 100·U); en expectiminimax, el V del
    juego con dado—, garantizado o por casualidad."""
    jm, v, _, n = minimax_tpm(arbol)
    G = GARANTIZA_TPM

    def fila(familia, algoritmo, jugada, valor, tipo, escala, nodos, nota="", da_v=None,
             simulaciones=None):
        if da_v is None:
            da_v = valor == (100 * v if escala == "100·U" else v)
        return dict(algoritmo=algoritmo, jugada=jugada, valor=valor, tipo=tipo, escala=escala,
                    nodos=nodos, simulaciones=simulaciones, garantiza=G[familia],
                    da_v_aqui=da_v, nota=nota)

    filas = [fila("minimax", "minimax", jm, v, "V", "U", n)]
    je, ve = expectiminimax_tpm(DADO_TPM, arbol)
    # su numero es, por construccion, el V del juego con dado: el que le toca
    filas.append(fila("expectiminimax", "expectiminimax, D es un dado", je, ve["R"],
                      "V con dado", "U", contar_nodos(arbol),
                      nota="exacto para el juego con dado, que es otro", da_v=True))
    for orden in ("dado", "al revés"):
        j_, v_, g, _ = alfa_beta_tpm(orden, arbol)
        filas.append(fila("alfa-beta", f"alfa-beta, orden {orden}", j_, v_, "V", "U", g))
    for d in (1, 2, 3):
        jc, vc, _, g = corte_tpm(d, arbol=arbol)
        filas.append(fila("corte", f"corte d = {d}", jc, vc, "valor con corte", "100·U", g))
    jq, vq, _, g, _ = quietud_tpm(1, arbol=arbol)
    filas.append(fila("quietud", "quietud, d = 1", jq, vq, "valor con quietud", "100·U", g))
    it, total = iterativa_tpm(arbol=arbol)
    filas.append(fila("iterativa", "profundización iterativa, d = 1, 2, 3", it[-1][2],
                      it[-1][3], "valor con corte", "100·U", total,
                      nota=" · ".join(f"d = {d}: {j_} ({g})" for d, _, j_, _, g in it)))
    jl, mu = todos_al_azar_tpm(arbol)
    for k in SIMS_MC_TPM:
        jp, sumas = mc_plano_tpm(k, SEMILLA_TPM, arbol)
        filas.append(fila("Monte Carlo plano", f"Monte Carlo plano, {k} por jugada", jp,
                          F(sumas[jp], k), "ū", "U", len(_tocados_mc(k, SEMILLA_TPM, arbol)),
                          nota=f"límite: {jl} con μ = {fmt_t(mu[jl])}",
                          simulaciones=k * len(arbol)))
    u = uct_tpm(1, VUELTAS_PAGINA_TPM, SEMILLA_TPM, arbol)
    ju = u["mas_simulada"][-1]
    h = (JUGADAS_RAIZ.index(ju),)
    filas.append(fila("UCT", f"UCT, c = 1, {VUELTAS_PAGINA_TPM} vueltas", ju,
                      F(u["S"][h], u["N"][h]), "ū", "U", len(u["N"]),
                      nota=f"N = {u['N'][h]} de {VUELTAS_PAGINA_TPM}",
                      simulaciones=sum(u["N"][(i,)] for i in range(len(arbol)))))
    return filas


def _podados_iterativa(traza, arbol=ARBOL_TPM):
    """Caminos que una busqueda con corte no genero porque un nodo corto
    (alfa o beta): los hijos sin generar de cada nodo de traza["cortes"]. Lo
    que queda bajo el horizonte no cuenta: no se poda, no se mira."""
    por_nombre = {n: c for c, (n, _) in nombres_t(arbol).items()
                  if isinstance(nodo_en(arbol, c), tuple)}
    generados = set(map(tuple, traza["caminos_generados"]))
    res = []
    for _, nombre, *_ in traza["cortes"]:
        c = por_nombre[nombre]
        res += [c + (i,) for i in range(len(nodo_en(arbol, c))) if c + (i,) not in generados]
    return sorted(res)


def _tocados_mc(k, semilla, arbol=ARBOL_TPM):
    """Caminos distintos por los que pasaron las simulaciones de MC plano."""
    rng = random.Random(semilla)
    tocados = {()}
    for i, h in enumerate(arbol):
        for _ in range(k):
            camino, nodo = (i,), h
            tocados.add(camino)
            while isinstance(nodo, tuple):
                m = rng.randrange(len(nodo))
                camino, nodo = camino + (m,), nodo[m]
                tocados.add(camino)
    return tocados


def intervalos_tpm(generados, profundidad=None, evaluar=None, escala=1, arbol=ARBOL_TPM):
    """Lo que una busqueda sabe de cada nodo interno que genero, como
    intervalo {camino: (lo, hi)}: un final generado vale escala·U; un nodo
    interno a `profundidad` vale EVAL (no se expande); un hijo que no se
    genero puede valer cualquier cosa (−∞, +∞); MAX toma el maximo de los
    dos extremos y MIN el minimo. lo == hi es un valor; hi = +∞, una cota
    «≥ lo»; lo = −∞, una cota «≤ hi». No reproduce el fail-soft: dice lo que
    los nodos generados demuestran, y la prueba coteja que coincida con lo
    que devuelve alfa-beta."""
    generados = set(map(tuple, generados))
    evaluar = evaluar or {}
    ids = ids_tpm(arbol)
    res = {}

    def iv(camino):
        if camino not in generados:
            return (-INF, INF)
        nodo = nodo_en(arbol, camino)
        if not isinstance(nodo, tuple):
            return (escala * nodo, escala * nodo)
        if profundidad is not None and len(camino) == profundidad:
            e = evaluar[ids[camino]]
            res[camino] = (e, e)
            return (e, e)
        hs = [iv(camino + (i,)) for i in range(len(nodo))]
        f = max if len(camino) % 2 == 0 else min
        res[camino] = (f(h[0] for h in hs), f(h[1] for h in hs))
        return res[camino]
    iv(())
    return res


def _valores_ids(intervalos, profundidad=None, arbol=ARBOL_TPM):
    """{id: [tipo, valor]} para el interactivo: tipo «=» (un valor), «≥» o
    «≤» (una cota) o «EVAL» (nodo donde corto la busqueda)."""
    ids = ids_tpm(arbol)
    res = {}
    for c, (lo, hi) in sorted(intervalos.items(), key=lambda x: (len(x[0]), x[0])):
        if profundidad is not None and len(c) == profundidad:
            res[ids[c]] = ["EVAL", lo]
        elif lo == hi:
            res[ids[c]] = ["=", lo]
        elif hi == INF:
            res[ids[c]] = ["≥", lo]
        elif lo == -INF:
            res[ids[c]] = ["≤", hi]
        else:
            raise ValueError(f"intervalo acotado de los dos lados en {ids[c]}: {lo}, {hi}")
    return res


def uct_por_vuelta_tpm(c, vueltas, semilla, arbol=ARBOL_TPM):
    """Tras cada vuelta de la corrida de uct_tpm: {camino: (N, suma de U)},
    reconstruido sumando 1 y el U de la vuelta a cada nodo de su camino."""
    u = uct_tpm(c, vueltas, semilla, arbol)
    N, S, res = {}, {}, []
    for camino, x in zip(u["caminos"], u["U"]):
        for nodo in camino:
            N[nodo] = N.get(nodo, 0) + 1
            S[nodo] = S.get(nodo, 0) + x
        res.append({k: (N[k], S[k]) for k in N})
    return res


def datos_interactivo_tpm(arbol=ARBOL_TPM):
    """Todo lo que el interactivo de 7.3.7 necesita, serializable a JSON
    (fracciones como «1/3»). Sin azar en el navegador: las corridas de MC
    plano y UCT vienen hechas con semilla fija."""
    ids = ids_tpm(arbol)
    s = lambda x: fmt_t(x) if isinstance(x, F) else x
    nodos = []
    for c in sorted(ids, key=lambda c: (len(c), c)):
        nodo = nodo_en(arbol, c)
        interno = isinstance(nodo, tuple)
        nodos.append(dict(id=ids[c], padre=ids[c[:-1]] if c else None,
                          tipo=("MAX" if len(c) % 2 == 0 else "MIN") if interno else "final",
                          U=None if interno else nodo,
                          EVAL=EVAL_TPM.get(ids[c]) if c else None,
                          captura=c in CAPTURAS_TPM))
    algs = {}
    jm, v, hijos, _ = minimax_tpm(arbol)
    gen = traza_decidir(arbol)["caminos_generados"]
    algs["minimax"] = dict(visitados=_ids(gen), jugada=jm, valor=v, raiz=hijos,
                           valores=_valores_ids(intervalos_tpm(gen, arbol=arbol), arbol=arbol))
    for orden in ("dado", "al revés"):
        j_, v_, g, pod = alfa_beta_tpm(orden, arbol)
        gen = _generados_alfa_beta(orden, arbol)
        algs[f"alfa-beta, {orden}"] = dict(
            visitados=_ids(gen), podados=_ids(pod), jugada=j_, valor=v_,
            valores=_valores_ids(intervalos_tpm(gen, arbol=arbol), arbol=arbol))
    je, ve = expectiminimax_tpm(DADO_TPM, arbol)
    algs["expectiminimax"] = dict(azar=list(DADO_TPM), jugada=je,
                                  valores={k: s(x) for k, x in ve.items()})
    for d in (1, 2, 3):
        t = traza_decidir(escalar_arbol(arbol, 100), profundidad=d, evaluar=EVAL_TPM)
        jc, vc, ws, _ = corte_tpm(d, arbol=arbol)
        algs[f"corte d = {d}"] = dict(
            visitados=_ids(t["caminos_generados"]), jugada=jc, valor=vc, raiz=ws,
            valores=_valores_ids(intervalos_tpm(t["caminos_generados"], d, EVAL_TPM, 100, arbol),
                                 d, arbol))
    vals = {}
    jq, vq, ws, _, gen = quietud_tpm(1, arbol=arbol, valores=vals)
    algs["quietud d = 1"] = dict(
        visitados=_ids(gen), jugada=jq, valor=vq, raiz=ws,
        valores={ids[c]: ["quietud" if len(c) == 1 else "=", x]
                 for c, x in sorted(vals.items(), key=lambda x: (len(x[0]), x[0]))})
    it = profundizacion_iterativa_t(escalar_arbol(arbol, 100), (1, 2, 3), EVAL_TPM)
    algs["profundización iterativa"] = [
        dict(d=d, orden=orden, jugada=t["jugada"], valor=t["valor"], nodos=t["generados"],
             visitados=_ids(t["caminos_generados"]), podados=_ids(_podados_iterativa(t, arbol)),
             valores=_valores_ids(intervalos_tpm(t["caminos_generados"], d, EVAL_TPM, 100, arbol),
                                  d, arbol))
        for d, orden, t in it]
    jl, mu = todos_al_azar_tpm(arbol)
    algs["Monte Carlo plano"] = dict(
        limite=dict(jugada=jl, mu={a: s(x) for a, x in mu.items()}),
        corridas={k: dict(sumas=mc_plano_tpm(k, SEMILLA_TPM, arbol)[1],
                          jugada=mc_plano_tpm(k, SEMILLA_TPM, arbol)[0],
                          nodos=len(_tocados_mc(k, SEMILLA_TPM, arbol)))
                  for k in SIMS_MC_TPM},
        reparto={k: reparto_mc_plano_tpm(k, SEMILLAS_MC_TPM, arbol)[0] for k in SIMS_MC_TPM})
    u = uct_tpm(1, VUELTAS_PAGINA_TPM, SEMILLA_TPM, arbol)
    algs["UCT"] = dict(c=1, semilla=SEMILLA_TPM, mas_simulada=u["mas_simulada"],
                       caminos=[_ids(cm[1:]) for cm in u["caminos"]],
                       N={ids[c]: n for c, n in u["N"].items()},
                       S={ids[c]: x for c, x in u["S"].items()},
                       U=u["U"],
                       por_vuelta=[{ids[c]: list(ns) for c, ns in sorted(
                                       v.items(), key=lambda x: (len(x[0]), x[0]))}
                                   for v in uct_por_vuelta_tpm(1, VUELTAS_PAGINA_TPM,
                                                               SEMILLA_TPM, arbol)])
    return dict(nodos=nodos, jugadas_raiz=list(JUGADAS_RAIZ),
                algoritmos=algs, tabla=[{k: s(x) for k, x in f.items()} for f in tabla_t_pm(arbol)])


# ------------------------------- homologacion: el arbol de resultados en 7.3 ---
#
# Las trazas de corte y de profundizacion iterativa de 7.3 pasan del arbol
# base (ARBOL_T, hojas 2–12) al arbol de resultados (ARBOL_TPM, finales
# +1/0/−1; plan de homologacion, decision 2). Un corte compara EVAL con
# finales en la escala 100·U, asi que todo se corre sobre ARBOL_TPM_100 con
# EVAL_TPM. Las funciones de ARBOL_T se quedan como estaban.

ARBOL_TPM_100 = escalar_arbol(ARBOL_TPM, 100)


def decidir_con_corte_tpm(d, orden=None, evaluar=None):
    """DECIDIR-CON-CORTE(R, d) en el arbol de resultados (finales 100·U, EVAL
    de EVAL_TPM): (jugada, valor, nodos generados). orden: los hijos de R en
    el orden de visita, por nombre («C», «I», «D»)."""
    t = traza_decidir(ARBOL_TPM_100, profundidad=d, evaluar=evaluar or EVAL_TPM,
                      orden={"R": orden} if orden else None)
    return t["jugada"], t["valor"], t["generados"]


def valores_con_corte_tpm(d, evaluar=None):
    """{nombre: valor con corte} de cada nodo interno que DECIDIR-CON-CORTE(R,
    d) genera en el arbol de resultados: EVAL donde corta, el max/min de sus
    hijos (finales en 100·U) donde no. R vale lo que devuelve."""
    t = traza_decidir(ARBOL_TPM_100, profundidad=d, evaluar=evaluar or EVAL_TPM)
    ultimo = t["filas"][-1]["estado"]
    return {n: e["v"] for n, e in ultimo.items()
            if e["estado"] in ("devuelto", "evaluado") and n[0] in "RICD"}


def filas_corte_tpm(d=2, orden=None, evaluar=None):
    """La traza de DECIDIR-CON-CORTE(R, d) en el arbol de resultados con las
    columnas de filas_corte_t: (#, «línea · pila», v, w, jugada). Una hoja va
    por su valor en 100·U («-100»)."""
    t = traza_decidir(ARBOL_TPM_100, profundidad=d, evaluar=evaluar or EVAL_TPM,
                      orden={"R": orden} if orden else None, lineas=LINEAS_CORTE)
    res = []
    for f in t["filas"]:
        v = f["mejor_valor"] if f["nodo"] == "R" else f["v"]
        w = ""
        if f["w"] is not None:
            w = fmt_t(f["w"]) if f["hijo"] == str(f["w"]) else f"{fmt_t(f['w'])} ({f['hijo']})"
        res.append((f["n"], f"{f['linea']} · {'›'.join(f['pila'])}", fmt_t(v), w,
                    f["mejor_jugada"] or "—"))
    return res


def iterativa_sin_poda_tpm(profundidades=(1, 2, 3), evaluar=None, anterior_primero=False):
    """Profundizacion iterativa con DECIDIR-CON-CORTE (sin poda) en el arbol de
    resultados: [(d, orden de la raiz, jugada lista, valor, nodos generados)].
    Sin poda el orden solo cambia algo si hay empates."""
    res, jugada = [], None
    for d in profundidades:
        orden = list(JUGADAS_RAIZ)
        if anterior_primero and jugada:
            orden = [jugada] + [a for a in orden if a != jugada]
        jugada, valor, nodos = decidir_con_corte_tpm(d, [JUGADA_A_NOMBRE[a] for a in orden],
                                                     evaluar)
        res.append((d, orden, jugada, valor, nodos))
    return res


def iterativa_alfa_beta_tpm(profundidades=(1, 2, 3), evaluar=None, anterior_primero=True):
    """Profundizacion iterativa con alfa-beta y corte en el arbol de
    resultados, con o sin la jugada anterior primero en la raiz:
    ([(d, orden de la raiz, jugada, valor, nodos generados)], total). Con
    anterior_primero=True es iterativa_tpm."""
    filas = [(d, orden, t["jugada"], t["valor"], t["generados"])
             for d, orden, t in profundizacion_iterativa_t(
                 ARBOL_TPM_100, profundidades, evaluar or EVAL_TPM,
                 anterior_primero=anterior_primero)]
    return filas, sum(f[4] for f in filas)


def traza_iterativa_tpm(d=3, evaluar=None):
    """La traza de la busqueda de profundidad d de la profundizacion iterativa
    en el arbol de resultados (alfa-beta con corte, la anterior primero), con
    la numeracion de lineas de PROFUNDIZACION-ITERATIVA (LINEAS_RELOJ)."""
    _, orden, _ = profundizacion_iterativa_t(ARBOL_TPM_100, tuple(range(1, d + 1)),
                                             evaluar or EVAL_TPM)[-1]
    return traza_decidir(ARBOL_TPM_100, poda=True, orden={"R": [JUGADA_A_NOMBRE[a] for a in orden]},
                         profundidad=d, evaluar=evaluar or EVAL_TPM, lineas=LINEAS_RELOJ)


def valor_con_corte_hijo_tpm(hijo, niveles, evaluar=None):
    """El valor con corte (sin poda) del hijo de R («I», «C» o «D») en el arbol
    de resultados cuando le quedan `niveles` jugadas por mirar."""
    t = traza_decidir(ARBOL_TPM_100, profundidad=niveles + 1, evaluar=evaluar or EVAL_TPM)
    return {f["hijo"]: f["w"] for f in t["filas"] if f["evento"] == "raiz"}[hijo]


def iterativa_con_reloj_tpm(acciones, tope=None, profundidades=(1, 2, 3), evaluar=None):
    """iterativa_con_reloj_t (las 32 lineas de la pagina) en el arbol de
    resultados, finales en 100·U y EVAL_TPM. Mismo formato."""
    return iterativa_con_reloj_t(acciones, tope, profundidades, evaluar or EVAL_TPM,
                                 arbol=ARBOL_TPM_100)


def tabla_nodos_generados_tpm(profundidades=(1, 2, 3)):
    """Nodos generados (contando R) en el arbol de resultados para cada d: sin
    poda, alfa-beta en el orden dado, e iterativa con y sin la anterior
    primero (cada busqueda por separado)."""
    ds = tuple(profundidades)
    return {
        "sin poda": [decidir_con_corte_tpm(d)[2] for d in ds],
        "alfa-beta": [traza_decidir(ARBOL_TPM_100, poda=True, profundidad=d,
                                    evaluar=EVAL_TPM)["generados"] for d in ds],
        "iterativa": [f[4] for f in iterativa_alfa_beta_tpm(ds)[0]],
        "iterativa sin la anterior primero": [
            f[4] for f in iterativa_alfa_beta_tpm(ds, anterior_primero=False)[0]],
    }


# ------------------------------- homologacion: los tres Monte Carlo ---
#
# Tres formas de usar partidas simuladas, sobre arboles de tuplas (raiz MAX,
# niveles alternados; un numero es un final con su U desde MAX):
#
# - Monte Carlo plano: promedia el U crudo por jugada de la raiz. Converge a
#   Q_azar, el valor si los dos juegan al azar (= expectiminimax con todos
#   los nodos bajo la raiz como dados parejos), no a V.
# - Monte Carlo con actualizacion minimax (MMMC; Kocsis, Szepesvari y
#   Willemson 2006): muestrea igual, pero guarda los estados descubiertos y
#   sube max/min: Q̂(s,a) = V̂(T(s,a)). Converge a V en un arbol finito,
#   determinista y de ramificacion finita.
# - UCT: uct_tpm, promedio del mismo U por arista con la seleccion UCB.
#
# El arbol de juguete de la refutacion (plan §6.2): MAX elige A o B; tras A,
# MIN elige p (+10), q (+10) o r, que lleva a x (MAX) con una sola jugada a
# un final −30; B es un final −10. V = −10, y lo correcto es B.

ARBOL_REFUTACION = ((10, 10, (-30,)), -10)
JUGADAS_REFUTACION = ("A", "B")
ESCALA_REFUTACION = 30        # UCT corre con los pagos entre 30: rango [−1, 1]
C_REFUTACION = 1              # la c de la corrida de UCT (escala ±1)
SEMILLA_REFUTACION = 0
VUELTAS_REFUTACION = 60       # vueltas de la corrida de la figura
# La secuencia impuesta para comparar operadores (no es una corrida): B una
# vez, luego 29 partidas por A que terminan en +10 (p y q alternadas) y, al
# final, la que descubre r, x, −30.
BUENAS_REFUTACION = 29


def acciones_arbol(nodo):
    """Las jugadas legales de un nodo interno de un arbol de tuplas: todos sus
    hijos, en el orden dado."""
    return list(range(len(nodo)))


def valor_minimax_arbol(arbol):
    """V exacto de un arbol de tuplas con raiz MAX (fracciones si las hay)."""
    return minimax_arbol(arbol, True)


def q_minimax_arbol(arbol):
    """[Q(s₀, a)] exactos de la raiz: el V de cada hijo, que mueve MIN."""
    return [minimax_arbol(h, False) for h in arbol]


def q_azar_arbol(arbol):
    """[Q_azar(s₀, a)] exactos: el pago esperado de cada jugada de la raiz si
    despues los dos juegan al azar, cada jugada legal con la misma
    probabilidad. Es el limite de Monte Carlo plano."""
    return [sum((u * p for u, p in distribucion_simulacion(h).items()), F(0)) for h in arbol]


def _primera_mejor(valores, es_max=True):
    """El indice de la mejor de `valores` (None = desconocida, no cuenta);
    empate → la primera; si ninguna se conoce, la primera jugada legal (0)."""
    mejor, k = None, 0
    for i, x in enumerate(valores):
        if x is None:
            continue
        if mejor is None or (x > mejor if es_max else x < mejor):
            mejor, k = x, i
    return k


def _respaldo_minimax(es_max, qs):
    """V̂ de un nodo a partir de sus Q̂: max en MAX, min en MIN, solo sobre las
    jugadas visitadas. Una jugada no visitada (None) es desconocida, nunca
    cero; si ninguna se conoce, V̂ tambien es desconocido. El resultado es
    provisional mientras falte alguna."""
    conocidas = [q for q in qs if q is not None]
    if not conocidas:
        return None
    return max(conocidas) if es_max else min(conocidas)


def partida_uniforme(arbol, rng):
    """Una partida desde la raiz eligiendo cada jugada legal con la misma
    probabilidad, hasta un final: el camino (tupla de indices)."""
    camino, nodo = (), arbol
    while isinstance(nodo, tuple):
        a = rng.choice(acciones_arbol(nodo))
        camino, nodo = camino + (a,), nodo[a]
    return camino


def _rango_arbol(arbol):
    if not isinstance(arbol, tuple):
        return arbol, arbol
    rs = [_rango_arbol(h) for h in arbol]
    return min(r[0] for r in rs), max(r[1] for r in rs)


def mc_minimax(arbol, iteraciones, semilla=0, caminos=None, rango=None):
    """Monte Carlo con actualizacion minimax (MMMC) sobre un arbol de tuplas.

    Contrato (plan de homologacion §6.2): cada iteracion elige jugadas legales
    uniformemente hasta un final (random.Random(semilla)) y agrega al arbol
    guardado los estados que descubre. En un final z, V̂(z) = U(z), exacto.
    Para una arista visitada, Q̂(s,a) = V̂(T(s,a)); luego V̂(s) = max en MAX,
    min en MIN, solo sobre las jugadas visitadas: una no visitada es
    desconocida (None), nunca cero, y ese max/min es provisional. No se
    promedia el U crudo. Entrega la mejor Q̂ de la raiz (empate → la primera;
    sin muestras, la primera jugada legal).

    caminos: en vez de muestrear, una lista de partidas impuestas (cada una
    un camino legal hasta un final); sirve para comparar operadores sobre la
    misma secuencia. rango: (U minimo, U maximo) que declara el juego (por
    omision, el menor y el mayor final del arbol); solo decide cuando un nodo
    queda resuelto antes de conocer a todos sus hijos.

    Devuelve dict:
    - V: {camino: V̂} de cada estado guardado;
    - N: {camino: visitas};
    - exacto: {camino: bool}: un final es exacto; un nodo interno lo es si
      todos sus hijos se conocen y son exactos, o si un hijo exacto ya da el
      mejor U posible para quien mueve (rango);
    - Q: [Q̂(s₀, a) o None] al final; jugada: el indice entregado;
    - historia: una entrada por iteracion: dict(camino, U, Q, jugada,
      nuevos: cuantos estados se agregaron)."""
    rng = random.Random(semilla)
    lo, hi = rango if rango is not None else _rango_arbol(arbol)
    V, N, exacto, historia = {}, {}, {}, []
    pendientes = list(caminos) if caminos is not None else None
    total = iteraciones if pendientes is None else len(pendientes)
    for it in range(total):
        camino = partida_uniforme(arbol, rng) if pendientes is None else tuple(pendientes[it])
        z = nodo_en(arbol, camino)
        if isinstance(z, tuple):
            raise ValueError(f"la partida {camino} no termina en un final")
        nuevos = sum(1 for k in range(len(camino) + 1) if camino[:k] not in V)
        V[camino], exacto[camino] = z, True
        for k in range(len(camino) + 1):
            N[camino[:k]] = N.get(camino[:k], 0) + 1
        for k in range(len(camino) - 1, -1, -1):
            s = camino[:k]
            nodo = nodo_en(arbol, s)
            es_max = k % 2 == 0
            hijos = [s + (a,) for a in acciones_arbol(nodo)]
            qs = [V.get(h) for h in hijos]
            V[s] = _respaldo_minimax(es_max, qs)
            mejor_posible = hi if es_max else lo
            exacto[s] = (all(exacto.get(h, False) for h in hijos)
                         or any(exacto.get(h, False) and V[h] == mejor_posible for h in hijos))
        qs = [V.get((a,)) for a in acciones_arbol(arbol)]
        historia.append(dict(camino=camino, U=z, Q=qs, jugada=_primera_mejor(qs), nuevos=nuevos))
    qs = [V.get((a,)) for a in acciones_arbol(arbol)]
    return dict(V=V, N=N, exacto=exacto, Q=qs, jugada=_primera_mejor(qs), historia=historia)


def mc_plano_uniforme(arbol, iteraciones, semilla=0, caminos=None):
    """Monte Carlo plano sobre las MISMAS partidas que mc_minimax con la misma
    semilla (o los mismos caminos impuestos): guarda N y la suma de U por
    jugada de la raiz y nada mas; Q̂(s₀,a) = suma/N, el promedio del U crudo.
    Converge a Q_azar. Devuelve dict(N, S: listas por jugada, Q: [Q̂ o None],
    jugada, historia: [dict(camino, U, Q, jugada)])."""
    rng = random.Random(semilla)
    n = len(arbol)
    Ns, Ss, historia = [0] * n, [0] * n, []
    pendientes = list(caminos) if caminos is not None else None
    total = iteraciones if pendientes is None else len(pendientes)
    for it in range(total):
        camino = partida_uniforme(arbol, rng) if pendientes is None else tuple(pendientes[it])
        u = nodo_en(arbol, camino)
        Ns[camino[0]] += 1
        Ss[camino[0]] += u
        qs = [F(Ss[a], Ns[a]) if Ns[a] else None for a in range(n)]
        historia.append(dict(camino=camino, U=u, Q=qs, jugada=_primera_mejor(qs)))
    qs = [F(Ss[a], Ns[a]) if Ns[a] else None for a in range(n)]
    return dict(N=Ns, S=Ss, Q=qs, jugada=_primera_mejor(qs), historia=historia)


def caminos_refutacion(buenas=BUENAS_REFUTACION):
    """La secuencia impuesta: B una vez, `buenas` partidas por A que terminan
    en +10 (p y q alternadas) y la que descubre r, x, −30."""
    return [(1,)] + [(0, k % 2) for k in range(buenas)] + [(0, 2, 0)]


def operadores_ante_la_refutacion(buenas=BUENAS_REFUTACION):
    """Promedio contra actualizacion minimax sobre la secuencia impuesta del
    arbol de la refutacion (no es una corrida). dict con Q̂(A) antes y despues
    de la ultima partida y la jugada que entrega cada uno despues:
    promedio: 10 → 26/3 (sigue en A); minimax: 10 → −30 (cambia a B)."""
    caminos = caminos_refutacion(buenas)
    plano = mc_plano_uniforme(ARBOL_REFUTACION, None, caminos=caminos)
    mm = mc_minimax(ARBOL_REFUTACION, None, caminos=caminos)
    hp, hm = plano["historia"], mm["historia"]
    return dict(
        promedio_antes=hp[-2]["Q"][0], promedio_despues=hp[-1]["Q"][0],
        jugada_promedio=JUGADAS_REFUTACION[hp[-1]["jugada"]],
        minimax_antes=hm[-2]["Q"][0], minimax_despues=hm[-1]["Q"][0],
        jugada_minimax=JUGADAS_REFUTACION[hm[-1]["jugada"]])


def corridas_refutacion(iteraciones=VUELTAS_REFUTACION, semilla=SEMILLA_REFUTACION):
    """Corridas REALES de Monte Carlo plano y de la actualizacion minimax en el
    arbol de la refutacion, con las mismas partidas uniformes (misma semilla):
    dict(descubre: la iteracion (desde 1) que pasa por primera vez por r,
    plano: [Q̂(A), Q̂(B)] tras cada iteracion, minimax: lo mismo, jugada_plano,
    jugada_minimax: lo que entrega cada uno tras cada iteracion)."""
    p = mc_plano_uniforme(ARBOL_REFUTACION, iteraciones, semilla)
    m = mc_minimax(ARBOL_REFUTACION, iteraciones, semilla)
    descubre = next((i + 1 for i, h in enumerate(m["historia"]) if h["camino"][:2] == (0, 2)),
                    None)
    return dict(descubre=descubre,
                plano=[h["Q"] for h in p["historia"]],
                minimax=[h["Q"] for h in m["historia"]],
                jugada_plano=[JUGADAS_REFUTACION[h["jugada"]] for h in p["historia"]],
                jugada_minimax=[JUGADAS_REFUTACION[h["jugada"]] for h in m["historia"]])


def uct_refutacion(c=C_REFUTACION, vueltas=VUELTAS_REFUTACION, semilla=SEMILLA_REFUTACION):
    """Una corrida REAL de UCT (uct_tpm, sus mismas reglas) en el arbol de la
    refutacion con los pagos divididos entre ESCALA_REFUTACION (rango
    [−1, 1], donde c = 1 y c = 2√2 tienen su sentido de siempre).

    dict(descubre: la vuelta cuyo U es por primera vez −30/30 = −1;
    Q: [(Q̂(A), Q̂(B))] tras cada vuelta, en escala ±1, None si no hay
    visitas; N: [(N(A), N(B))] tras cada vuelta; cambia: la primera vuelta
    con Q̂(A) < Q̂(B); mas_visitada: la jugada que se entregaria (A o B)
    tras cada vuelta, empate → la primera)."""
    arbol = escalar_arbol(ARBOL_REFUTACION, F(1, ESCALA_REFUTACION))
    u = uct_tpm(c, vueltas, semilla, arbol)
    por_vuelta = uct_por_vuelta_tpm(c, vueltas, semilla, arbol)
    Q, Ns = [], []
    for v in por_vuelta:
        Q.append(tuple(F(v[(a,)][1], v[(a,)][0]) if (a,) in v else None for a in (0, 1)))
        Ns.append(tuple(v.get((a,), (0, 0))[0] for a in (0, 1)))
    descubre = next((i + 1 for i, x in enumerate(u["U"]) if x == -1), None)
    cambia = next((i + 1 for i, (qa, qb) in enumerate(Q)
                   if qa is not None and qb is not None and qa < qb), None)
    mas = [JUGADAS_REFUTACION[0 if na >= nb else 1] for na, nb in Ns]
    return dict(descubre=descubre, Q=Q, N=Ns, cambia=cambia, mas_visitada=mas)


def sesgo_del_maximo():
    """Dos jugadas de media 0, cada una con una sola muestra ±1 (parejas):
    (E[max], E[min]) exactos = (1/2, −1/2), aunque el maximo real es 0."""
    pares = list(product((-1, 1), repeat=2))
    return (sum((F(max(p)) for p in pares), F(0)) / len(pares),
            sum((F(min(p)) for p in pares), F(0)) / len(pares))


# ------------------------------- homologacion: Hoeffding y la c de UCB1 ---

EPS_HOEFFDING_HOMOLOGACION = (0.1, 0.2, 0.4)
N_HOEFFDING_HOMOLOGACION = 100


def cota_hoeffding_cola(n, eps, ancho=2):
    """Una cola de Hoeffding para n muestras independientes en un intervalo de
    ancho `ancho`, con n fijado de antemano: Pr(Q̂ ≤ Q − ε) ≤ e^(−2nε²/ancho²).
    En la escala ±1 (ancho 2) es e^(−nε²/2), cota_hoeffding."""
    return math.exp(-2 * n * eps ** 2 / ancho ** 2)


def margen_hoeffding(delta, n, ancho=2):
    """El ε que deja esa cola en δ: ε = ancho·√(ln(1/δ)/(2n)); en ±1,
    √(2·ln(1/δ)/n), como margen."""
    return ancho * math.sqrt(math.log(1 / delta) / (2 * n))


def c_ucb1(ancho=2, exponente=4):
    """La c de UCB1 que sale de pedir δ = N(s)^(−exponente) en el margen:
    ε = ancho·√(exponente·ln N(s)/(2·N(s,a))), asi que c = ancho·√(exponente/2).
    Con δ = N(s)^−4: 2√2 en ±1 (ancho 2), √2 en [0, 1] (ancho 1)."""
    return ancho * math.sqrt(exponente / 2)


def tabla_hoeffding_epsilon(n=N_HOEFFDING_HOMOLOGACION, epsilones=EPS_HOEFFDING_HOMOLOGACION):
    """[(ε, cota en %)] con n muestras en ±1: 0.1 / 0.2 / 0.4 con n = 100 dan
    60.65 % / 13.53 % / 0.0335 %."""
    return [(e, 100 * cota_hoeffding_cola(n, e)) for e in epsilones]
