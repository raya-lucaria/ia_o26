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
