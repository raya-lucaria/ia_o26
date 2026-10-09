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
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import copy
import re

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


def profundizacion_iterativa_t(arbol=ARBOL_T, profundidades=(1, 2, 3), evaluar=None):
    """PROFUNDIZACION-ITERATIVA sobre T, sin reloj: para cada d, DECIDIR-
    ALFA-BETA con corte a profundidad d, con la jugada que dejo lista la
    iteracion anterior primero en la raiz (las demas, en el orden dado).
    Devuelve [(d, orden de la raiz, traza)]."""
    evaluar = evaluar or EVAL_T
    nombres = nombres_t(arbol)
    raiz = [nombres[(i,)] for i in range(len(arbol))]
    res, jugada = [], None
    for d in profundidades:
        orden_raiz = [n for n, a in raiz]
        if jugada:
            primero = next(n for n, a in raiz if a == jugada)
            orden_raiz = [primero] + [n for n in orden_raiz if n != primero]
        t = traza_decidir(arbol, poda=True, orden={"R": orden_raiz}, profundidad=d,
                          evaluar=evaluar)
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
    """Minimax con corte que, al llegar a d = 0, no evalua en seco: sigue
    mirando solo capturas hasta una posicion quieta. En cada paso de la
    quietud el jugador de turno puede no capturar y quedarse con EVAL."""
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
# muestran el cuaderno de la unidad y la traza interactiva del arbol T. Un
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
    "iterativa": "3_cuando_no_cabe/3_jugar_contra_el_reloj.md",
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
                frase = f"La búsqueda con d = {d} terminó: jugada = {mejor}; d pasa a {d + 1}."
                if ultima:
                    frase = f"La búsqueda con d = {d} terminó: jugada = {mejor}; ya no hay tiempo."
            elif poda:
                frase = f"Línea 6: R devuelve {mejor}; α = {mv} se queda dentro."
            else:
                frase = f"Línea 6: R devuelve {mejor}; el valor {mv} se queda dentro."
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
