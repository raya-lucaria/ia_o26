"""Calculos de la unidad de cadenas de Markov (unidad 8), clases 1 y 2.

Unica fuente de los numeros que citan las paginas de
course/8_markov/1_que_es_una_cadena/ (clase 1) y
course/8_markov/2_a_la_larga/ (clase 2: estacionaria, clases, absorcion,
PageRank; seccion «CLASE 2» al final, fijada en test_markov_c2.py) y las
figuras de gen_markov.py. Nada se
copia a mano: test_markov.py fija cada cifra con su valor escrito a mano y la
busca en el bloque de su pagina.

Convenciones (plan de la clase 1, §2):

- Orden de estados: V primero, C segundo (fila 0 = desde V, columna 0 =
  hacia V). mu0 = (0, 1) es «empiezo en C».
- normalizar_vc: minusculas; toda vocal con diacritico pasa a su vocal (NFD
  y quitar marcas), salvo la ñ, que se conserva; solo a-z y ñ; sin espacios
  ni puntuacion. Vocales: a e i o u; la «y» es consonante.
- normalizar_caracteres: lo mismo, pero todo lo que no es letra separa y los
  separadores se colapsan a UN espacio (27 letras + espacio = 28 simbolos).
  Es " ".join(normalizar_palabras(texto)).
- normalizar_palabras: tokens [a-zñ]+ tras quitar diacriticos.
- Los juguetes usan Fraction; el corpus, conteos enteros y Fraction donde la
  pagina cita una fraccion.
- Muestreo propio y reproducible: random.Random(semilla) y la fila acumulada
  de MUESTREAR-FILA; nunca random.choices (sus resultados pueden cambiar
  entre versiones de Python). Cada paso gasta exactamente un u.

Semillas (plan §2: 2026 para la primera figura simulada y siguientes; la
clase 2 usa 2037 en adelante): SEMILLAS dice cual usa cada simulacion.

`python3 tools/markov.py foto` reescribe la foto fija de la web del curso
(tools/datos/markov/enlaces_curso.tsv); no se corre sin decidirlo.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import math
import random
import re
import statistics
import sys
import unicodedata

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "tools/datos/quijote/quijote.txt"

VOCALES = "aeiou"
LETRAS = "abcdefghijklmnñopqrstuvwxyz"          # 27 letras
ALFABETO = LETRAS + " "                          # 28 simbolos (Σ con espacio)
ESTADOS_VC = ("V", "C")                          # orden V, C
ESPACIO = "_"                                    # el estado «espacio»
ESTADOS_VCE = ("V", "C", ESPACIO)                # orden V, C, espacio
MU0_C = (F(0), F(1))                             # empiezo en C

FRASE = "Con la iglesia hemos dado, Sancho"      # Quijote, II, 9
FRASE_EN_EL_CORPUS = "— Con la iglesia hemos dado, Sancho."
FRASE_ESPACIOS = "En un lugar de la Mancha"      # ejercicio de la pagina 1
FRASE_E = "Llaneza, muchacho; no te encumbres"   # Quijote, II, 26; p2 ej. (b)

SEMILLAS = {
    "rachas-markov": 2026,
    "rachas-independiente": 2027,
    "recuperar-p": 2028,
    "mu-t-desde-V": 2029,
    "mu-t-desde-C": 2030,
    "ejercicio-simulacion": 2031,
    "generar-0": 2032,
    "generar-1": 2033,
    "generar-2": 2034,
    "generar-3": 2035,
    "generar-palabras": 2036,
}


# ---------------------------------------------------------- normalizar ---

def _sin_marcas(texto):
    """Minusculas y sin diacriticos, salvo la ñ."""
    salida = []
    for c in texto.lower():
        if c == "ñ":
            salida.append(c)
            continue
        for d in unicodedata.normalize("NFD", c):
            if unicodedata.category(d) != "Mn":
                salida.append(d)
    return "".join(salida)


def normalizar_vc(texto):
    """Solo las letras a-z y ñ, en minusculas, sin espacios (como Markov)."""
    return "".join(c for c in _sin_marcas(texto) if c in LETRAS)


def normalizar_palabras(texto):
    """Lista de palabras [a-zñ]+; todo otro caracter separa."""
    return re.findall(r"[a-zñ]+", _sin_marcas(texto))


def normalizar_caracteres(texto):
    """Letras y un solo espacio entre palabras: el alfabeto de 28 simbolos."""
    return " ".join(normalizar_palabras(texto))


def clase_vc(letra):
    """V o C. La «y» es consonante. Rechaza lo que no sea letra."""
    if len(letra) != 1 or letra not in LETRAS:
        raise ValueError(f"no es una letra normalizada: {letra!r}")
    return "V" if letra in VOCALES else "C"


def clase_vce(simbolo):
    """V, C o _ (espacio): los tres estados del ejemplo de 3 estados."""
    if simbolo == " ":
        return ESPACIO
    return clase_vc(simbolo)


def secuencia_vc(texto):
    """'CVCC…': la clase de cada letra de normalizar_vc(texto)."""
    return "".join(clase_vc(c) for c in normalizar_vc(texto))


def secuencia_vce(texto):
    """V, C y _ sobre normalizar_caracteres(texto)."""
    return "".join(clase_vce(c) for c in normalizar_caracteres(texto))


def secuencia_e(texto):
    """E si la letra es «e», N si no (ejercicio (b) de «El problema de Markov»)."""
    return "".join("E" if c == "e" else "N" for c in normalizar_vc(texto))


# -------------------------------------------------------------- corpus ---

@lru_cache(maxsize=None)
def cargar_corpus():
    """El corte versionado del Quijote, tal cual (UTF-8, \\n)."""
    return CORPUS.read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def letras_corpus():
    return normalizar_vc(cargar_corpus())


@lru_cache(maxsize=None)
def vc_corpus():
    return letras_corpus().translate(
        {ord(c): "V" if c in VOCALES else "C" for c in LETRAS})


@lru_cache(maxsize=None)
def caracteres_corpus():
    return normalizar_caracteres(cargar_corpus())


@lru_cache(maxsize=None)
def palabras_corpus():
    return tuple(normalizar_palabras(cargar_corpus()))


def capitulo_de(frase=FRASE):
    """(parte, capitulo en romanos) del primer renglon del corpus que trae
    `frase`. La segunda parte empieza en «Segunda parte del ingenioso
    caballero»; los capitulos se titulan «Capítulo <romano>.» salvo el
    primero de la primera parte («Capítulo primero.»)."""
    lineas = cargar_corpus().splitlines()
    k = next(i for i, l in enumerate(lineas) if frase in l)
    parte = 2 if any(l.startswith("Segunda parte del ingenioso caballero")
                     for l in lineas[:k]) else 1
    cap = next(l for l in reversed(lineas[:k]) if l.startswith("Capítulo "))
    return parte, cap.split(".")[0].split()[1]


# ------------------------------------------------------- la frase a mano ---

def frase_a_mano():
    """La instancia congelada: «Con la iglesia hemos dado, Sancho»."""
    return normalizar_vc(FRASE)


def frase_vc():
    return secuencia_vc(FRASE)


# -------------------------------------------------------------- contar ---

def _contexto(secuencia, i, memoria):
    c = secuencia[i - memoria:i]
    return tuple(c) if isinstance(c, list) else c


def contar(secuencia, memoria=1):
    """{contexto: Counter({siguiente: N})} con contexto = los `memoria`
    simbolos anteriores. Una transicion por posicion i >= memoria."""
    if isinstance(secuencia, str):
        bloques = Counter(secuencia[i:i + memoria + 1]
                          for i in range(len(secuencia) - memoria))
        conteos = {}
        for b, n in bloques.items():
            conteos.setdefault(b[:memoria], Counter())[b[memoria]] = n
        return conteos
    secuencia = list(secuencia)
    conteos = {}
    for i in range(memoria, len(secuencia)):
        ctx = _contexto(secuencia, i, memoria)
        conteos.setdefault(ctx, Counter())[secuencia[i]] += 1
    return conteos


def contar_transiciones(secuencia, estados=None):
    """El algoritmo de «Ajustar contando»: (N, salidas, P̂) con N = {(s, s'): N(s, s')}
    para todo par de `estados` (los no vistos en 0), salidas = {s: N(s)} y
    P̂ = {(s, s'): N(s, s')/N(s)} solo para las filas con N(s) > 0. Sin
    `estados`, usa los que aparecen en la secuencia."""
    if estados is None:
        estados = sorted(set(secuencia))
    N = {(s, s2): 0 for s in estados for s2 in estados}
    salidas = {s: 0 for s in estados}
    for s, s2 in zip(secuencia, secuencia[1:]):
        N[(s, s2)] += 1
        salidas[s] += 1
    P_gorro = {(s, s2): F(N[(s, s2)], salidas[s])
               for s in estados if salidas[s] > 0 for s2 in estados}
    return N, salidas, P_gorro


def traza_contar(secuencia, estados=ESTADOS_VC):
    """Una fila por transicion: (j, s, s', N acumulado tras sumarla), con N
    acumulado como tupla en el orden (s, s') de estados x estados."""
    N = {(a, b): 0 for a in estados for b in estados}
    filas = []
    for j, (s, s2) in enumerate(zip(secuencia, secuencia[1:])):
        N[(s, s2)] += 1
        filas.append((j, s, s2, tuple(N[(a, b)] for a in estados for b in estados)))
    return filas


def matriz_conteos(secuencia, estados):
    """N como lista de filas en el orden de `estados`."""
    c = contar(secuencia, 1)
    return [[c.get(s, Counter())[s2] for s2 in estados] for s in estados]


def salidas(conteos_matriz):
    return [sum(f) for f in conteos_matriz]


def estimar(conteos, suavizado=0, alfabeto=None):
    """P̂ (suavizado=0) o p̃ de Laplace (suavizado=1) a partir de conteos.

    `conteos` es una matriz [[N]] (filas en orden) o un dict
    {contexto: Counter}. Con suavizado, `alfabeto` da las columnas y
    p̃(z | ctx) = (N(ctx z) + 1) / (N(ctx) + |Σ|). Sin suavizado, una fila con
    N(s) = 0 queda en None: los datos no la determinan."""
    if isinstance(conteos, list):
        filas = []
        for fila in conteos:
            total = sum(fila)
            if suavizado:
                filas.append([F(n + suavizado, total + suavizado * len(fila)) for n in fila])
            else:
                filas.append([F(n, total) for n in fila] if total else None)
        return filas
    salida = {}
    for ctx, c in conteos.items():
        total = sum(c.values())
        if suavizado:
            k = len(alfabeto)
            salida[ctx] = {z: F(c[z] + suavizado, total + suavizado * k) for z in alfabeto}
        else:
            salida[ctx] = {z: F(n, total) for z, n in c.items()}
    return salida


def matriz_estimada(secuencia, estados=ESTADOS_VC):
    return estimar(matriz_conteos(secuencia, estados))


def verosimilitud(P, secuencia, estados=ESTADOS_VC):
    """L(P) condicionada a s0: el producto de P(s'|s) sobre las transiciones."""
    idx = {s: k for k, s in enumerate(estados)}
    L = F(1)
    for s, s2 in zip(secuencia, secuencia[1:]):
        L *= F(P[idx[s]][idx[s2]])
    return L


def probabilidad_trayectoria(P, mu0, trayectoria, estados=ESTADOS_VC):
    """mu0(s0) por el producto de P(s_{j+1} | s_j)."""
    idx = {s: k for k, s in enumerate(estados)}
    return F(mu0[idx[trayectoria[0]]]) * verosimilitud(P, trayectoria, estados)


# ------------------------------------------------------------ muestrear ---

def muestrear_fila(fila, u):
    """MUESTREAR-FILA: recorre la fila sumando; devuelve el primer indice cuya
    suma acumulada pasa a u (u en [0, 1)). Si el redondeo deja la suma final
    por debajo de u, devuelve el ultimo indice con probabilidad positiva."""
    acumulado = 0
    for k, p in enumerate(fila):
        acumulado += p
        if u < acumulado:
            return k
    return max(k for k, p in enumerate(fila) if p > 0)


def fila_acumulada(fila):
    acumulado, salida = 0, []
    for p in fila:
        acumulado += p
        salida.append(acumulado)
    return salida


def trayectoria_a_mano(P, s0, us, estados=ESTADOS_VC):
    """Trayectoria desde s0 con los uniformes dados: [(s, u, s')] y la lista
    de estados visitados."""
    idx = {s: k for k, s in enumerate(estados)}
    s, pasos, visitados = s0, [], [s0]
    for u in us:
        s2 = estados[muestrear_fila(P[idx[s]], u)]
        pasos.append((s, u, s2))
        visitados.append(s2)
        s = s2
    return pasos, "".join(visitados)


def simular(P, mu0, n, T, semilla):
    """n replicas de T pasos. Cada replica: S0 con muestrear_fila(mu0, u) y
    luego un u por paso. Devuelve una lista de listas de indices de estado
    (cada una de largo T + 1)."""
    rng = random.Random(semilla)
    filas = [[float(p) for p in f] for f in P]
    m0 = [float(p) for p in mu0]
    replicas = []
    for _ in range(n):
        s = muestrear_fila(m0, rng.random())
        tray = [s]
        for _ in range(T):
            s = muestrear_fila(filas[s], rng.random())
            tray.append(s)
        replicas.append(tray)
    return replicas


# ------------------------------------------------------------- predecir ---

def predecir(P, mu0, t):
    """mu_t = mu0 P^t, vector fila a la izquierda, t multiplicaciones."""
    mu = list(mu0)
    k = len(mu)
    for _ in range(t):
        mu = [sum(mu[i] * P[i][j] for i in range(k)) for j in range(k)]
    return mu


def mu_t(P, mu0, t_max):
    """[mu_0, mu_1, …, mu_t_max]."""
    return [predecir(P, mu0, t) for t in range(t_max + 1)]


def arbol_dos_pasos(P, s0="C", estados=ESTADOS_VC):
    """{(s1, s2): probabilidad del camino s0 -> s1 -> s2}."""
    idx = {s: k for k, s in enumerate(estados)}
    i0 = idx[s0]
    return {(a, b): P[i0][idx[a]] * P[idx[a]][idx[b]] for a in estados for b in estados}


def fraccion_simulada(P, mu0, n, t_max, semilla, estado=0):
    """Fraccion de las n replicas en `estado` en cada paso t = 0..t_max."""
    replicas = simular(P, mu0, n, t_max, semilla)
    return [sum(1 for r in replicas if r[t] == estado) / n for t in range(t_max + 1)]


def error_estandar(p, n):
    return math.sqrt(p * (1 - p) / n)


@lru_cache(maxsize=None)
def mu_t_corpus(t_max=8, n=10_000):
    """La comparacion de la figura mkv-c1-mu-t: con P̂ del corpus, desde V y
    desde C. {inicio: {"cuenta": [Pr(S_t=V)], "simulada": [fraccion]}}."""
    P = matriz_corpus()
    salida = {}
    for inicio, mu0 in (("V", (F(1), F(0))), ("C", (F(0), F(1)))):
        cuenta = [float(m[0]) for m in mu_t(P, mu0, t_max)]
        sim = fraccion_simulada(P, mu0, n, t_max, SEMILLAS[f"mu-t-desde-{inicio}"])
        salida[inicio] = {"cuenta": cuenta, "simulada": sim}
    return salida


def diferencia_maxima_mu_t(t_max=8, n=10_000):
    """max |simulada - cuenta| sobre t y los dos inicios, y en errores
    estandar sqrt(p(1-p)/n) de cada punto (t = 0 no cuenta: es exacto)."""
    datos = mu_t_corpus(t_max, n)
    peor, peor_z = 0.0, 0.0
    for d in datos.values():
        for t in range(1, t_max + 1):
            p, q = d["cuenta"][t], d["simulada"][t]
            peor = max(peor, abs(q - p))
            peor_z = max(peor_z, abs(q - p) / error_estandar(p, n))
    return peor, peor_z


# --------------------------------------------------------------- corpus ---

@lru_cache(maxsize=None)
def conteos_vc_corpus():
    """N del corpus V/C como matriz [[N(V,V), N(V,C)], [N(C,V), N(C,C)]]."""
    return matriz_conteos(vc_corpus(), ESTADOS_VC)


@lru_cache(maxsize=None)
def matriz_corpus():
    """P̂ del corpus V/C en Fraction."""
    return estimar([list(f) for f in conteos_vc_corpus()])


def vocales_corpus():
    return vc_corpus().count("V")


def pr_vocal_corpus():
    return F(vocales_corpus(), len(vc_corpus()))


def redondear_matriz(P, cifras=3):
    """Cada entrada redondeada a `cifras` decimales, como Fraction exacta del
    decimal (la P «verdadera» de recuperar-p)."""
    return [[F(f"{float(p):.{cifras}f}") for p in fila] for fila in P]


@lru_cache(maxsize=None)
def condicionales_memoria_2():
    """Pr(V | anterior C) frente a Pr(V | anterior C y la de antes V) y
    Pr(V | anterior C y la de antes C), en el corpus V/C. Las tres filas
    usan el mismo universo, las posiciones con dos letras siguientes, para
    que la primera sea exactamente la mezcla de las otras dos."""
    c2 = contar(vc_corpus(), 2)
    def pr(*ctxs):
        return F(sum(c2[x]["V"] for x in ctxs),
                 sum(sum(c2[x].values()) for x in ctxs))
    return {"C": pr("VC", "CC"), "VC": pr("VC"), "CC": pr("CC"),
            "V": pr("VV", "CV"), "VV": pr("VV"), "CV": pr("CV")}


# -------------------------------------------------------------- rachas ---

def rachas(secuencia, estado="C"):
    """Counter {ℓ: veces} de las rachas de `estado`, sin las truncadas por
    los extremos (la primera si empieza en la posicion 0, la ultima si
    llega al final)."""
    cuenta = Counter()
    for m in re.finditer(f"{estado}+", secuencia):
        if m.start() == 0 or m.end() == len(secuencia):
            continue
        cuenta[m.end() - m.start()] += 1
    return cuenta


@lru_cache(maxsize=None)
def rachas_corpus():
    return rachas(vc_corpus(), "C")


def rachas_geometrica(q, ell):
    """Pr(L = ℓ) = (1 - q) q^(ℓ-1)."""
    return (1 - q) * q ** (ell - 1)


def _rachas_de_replica(P, s0, T, rng):
    """Rachas completas de C en una replica de T pasos de la cadena de dos
    estados (MUESTREAR-FILA en linea: con dos estados la fila acumulada es
    (P[s][V], 1), asi que el siguiente es V si u < P[s][V])."""
    pv = (float(P[0][0]), float(P[1][0]))
    rnd = rng.random
    cuenta = Counter()
    s = s0
    largo = 1 if s == 1 else 0
    truncada = s == 1      # una racha que toca el inicio no cuenta
    for _ in range(T):
        s2 = 0 if rnd() < pv[s] else 1
        if s2 == 1:
            largo += 1
        elif s == 1:       # termina una racha de C
            if not truncada:
                cuenta[largo] += 1
            largo = 0
            truncada = False
        s = s2
    return cuenta          # la racha abierta al final no se cuenta


N_RACHAS = 10              # replicas por modelo (cada una del largo del corpus)
ELL_MAX = 6


@lru_cache(maxsize=None)
def rachas_simuladas(modelo, n=N_RACHAS, ell_max=ELL_MAX):
    """Por ℓ = 1..ell_max: (mediana, percentil 5, percentil 95) del numero de
    rachas de largo ℓ en n replicas del largo del corpus, empezando en la
    primera letra del corpus. modelo: "markov" (P̂ del corpus) o
    "independiente" (cada fila = (Pr(V), Pr(C)))."""
    if modelo == "markov":
        P = matriz_corpus()
    else:
        pv = pr_vocal_corpus()
        P = [[pv, 1 - pv], [pv, 1 - pv]]
    seq = vc_corpus()
    s0 = ESTADOS_VC.index(seq[0])
    rng = random.Random(SEMILLAS[f"rachas-{modelo}"])
    replicas = [_rachas_de_replica(P, s0, len(seq) - 1, rng) for _ in range(n)]
    salida = {}
    for ell in range(1, ell_max + 1):
        valores = sorted(r[ell] for r in replicas)
        salida[ell] = (statistics.median(valores), percentil(valores, 5),
                       percentil(valores, 95))
    return salida


def percentil(valores_ordenados, p):
    """Percentil p (0-100) con interpolacion lineal entre ordenados (el
    metodo «inclusive» de statistics.quantiles)."""
    v = valores_ordenados
    x = (len(v) - 1) * p / 100
    i = int(math.floor(x))
    if i + 1 >= len(v):
        return float(v[-1])
    return float(v[i] + (v[i + 1] - v[i]) * (x - i))


# ------------------------------------------------------- recuperar-p ---

LONGITUDES_T = (10, 30, 100, 300, 1000, 3000, 10000)
REPLICAS_RECUPERAR = 200


def error_recuperacion(P, Phat):
    """max |P̂(s'|s) - P(s'|s)| sobre las filas con N(s) > 0 (Phat None)."""
    return max(abs(float(ph) - float(p))
               for fila_h, fila in zip(Phat, P) if fila_h is not None
               for ph, p in zip(fila_h, fila))


@lru_cache(maxsize=None)
def recuperar_p():
    """{T: {"errores": [...], "mediana", "p5", "p95", "sin_salidas"}} para
    la P verdadera = P̂ del corpus redondeada a 3 decimales, desde C, con
    200 replicas por T y una sola semilla para toda la figura."""
    P = redondear_matriz(matriz_corpus())
    rng = random.Random(SEMILLAS["recuperar-p"])
    pv = (float(P[0][0]), float(P[1][0]))
    rnd = rng.random
    salida = {}
    for T in LONGITUDES_T:
        errores, sin_salidas = [], 0
        for _ in range(REPLICAS_RECUPERAR):
            # una replica desde C (mu0 = (0, 1): S0 = C sin gastar u)
            N = [[0, 0], [0, 0]]
            s = 1
            for _ in range(T):
                s2 = 0 if rnd() < pv[s] else 1
                N[s][s2] += 1
                s = s2
            Phat = estimar(N)
            if any(f is None for f in Phat):
                # una fila sin estimar se reporta aparte: su error no se mide
                sin_salidas += 1
                continue
            errores.append(error_recuperacion(P, Phat))
        errores.sort()
        salida[T] = {"errores": errores, "mediana": statistics.median(errores),
                     "p5": percentil(errores, 5), "p95": percentil(errores, 95),
                     "sin_salidas": sin_salidas}
    return salida


# ------------------------------------------------- lo general: 784 y ceros ---

@lru_cache(maxsize=None)
def conteos_caracteres(memoria=1):
    return contar(caracteres_corpus(), memoria)


def entradas_memoria_1():
    """(entradas, en cero, con menos de 5 conteos y mas de 0, con < 5 incl.
    ceros) de la tabla 28 x 28 de memoria 1 de caracteres del corpus."""
    c = conteos_caracteres(1)
    valores = [c.get(a, Counter())[b] for a in ALFABETO for b in ALFABETO]
    return {"entradas": len(valores),
            "ceros": sum(1 for v in valores if v == 0),
            "menos_de_5": sum(1 for v in valores if v < 5),
            "entre_1_y_4": sum(1 for v in valores if 0 < v < 5),
            "contextos_sin_salidas": [a for a in ALFABETO if a not in c]}


def fila_caracteres(contexto, siguientes, suavizado=0):
    """{z: p} de la fila `contexto` de memoria len(contexto), con o sin
    Laplace sobre los 28 simbolos, solo para los `siguientes` pedidos."""
    c = conteos_caracteres(len(contexto)).get(contexto, Counter())
    total = sum(c.values())
    if suavizado:
        return {z: F(c[z] + 1, total + len(ALFABETO)) for z in siguientes}, total
    return {z: F(c[z], total) for z in siguientes}, total


@lru_cache(maxsize=None)
def fraccion_no_vista(memoria):
    """Cuenta con la primera mitad del corpus (por caracteres) y mide en la
    segunda: fraccion de transiciones de prueba (contexto, siguiente) que no
    aparecieron al contar. La mitad se corta en len // 2; la prueba empieza
    en su posicion `memoria` (su primer contexto completo)."""
    texto = caracteres_corpus()
    mitad = len(texto) // 2
    entrena, prueba = texto[:mitad], texto[mitad:]
    h = memoria
    vistos = {entrena[i:i + h + 1] for i in range(len(entrena) - h)}
    contextos = {b[:h] for b in vistos}
    pruebas = Counter(prueba[i:i + h + 1] for i in range(len(prueba) - h))
    total = sum(pruebas.values())
    no_vistas = sum(n for b, n in pruebas.items() if b not in vistos)
    return {"memoria": h, "total": total, "no_vistas": no_vistas,
            "fraccion": F(no_vistas, total), "contextos_vistos": len(contextos),
            "contextos_posibles": len(ALFABETO) ** h}


# -------------------------------------------------------------- generar ---

def generar_desde(tabla, alfabeto, contexto, largo, rng):
    """GENERAR: `tabla` es {contexto: fila de probabilidades en el orden de
    `alfabeto`}. Un contexto que no esta en la tabla usa Laplace con
    conteos 0: la fila uniforme 1/|Σ| (no se reinicia). Devuelve el
    contexto inicial seguido de `largo` simbolos generados."""
    h = len(contexto)
    salida = list(contexto)
    uniforme = [1 / len(alfabeto)] * len(alfabeto)
    for _ in range(largo):
        ctx = tuple(salida[len(salida) - h:]) if h else ()
        if isinstance(contexto, str):
            ctx = "".join(ctx)
        fila = tabla.get(ctx, uniforme)
        salida.append(alfabeto[muestrear_fila(fila, rng.random())])
    return "".join(salida) if isinstance(contexto, str) else salida


def tabla_desde_conteos(conteos, alfabeto):
    """{contexto: [N(ctx z)/N(ctx) en el orden de alfabeto]} (floats)."""
    tabla = {}
    for ctx, c in conteos.items():
        total = sum(c.values())
        tabla[ctx] = [c[z] / total for z in alfabeto]
    return tabla


CONTEXTO_INICIAL = "en un lugar"           # se toman sus primeros h simbolos
LARGO_GENERAR = 200
LARGO_PALABRAS = 30


@lru_cache(maxsize=None)
def generar(memoria, unidad="caracteres", largo=None, semilla=None):
    """Texto generado con memoria h sobre el corpus. unidad: "caracteres"
    (28 simbolos; contexto inicial = primeros h simbolos de «en un lugar»;
    devuelve largo simbolos en total, contexto incluido) o "palabras"
    (memoria 1; contexto inicial «en»; largo palabras en total)."""
    if unidad == "caracteres":
        largo = largo or LARGO_GENERAR
        semilla = SEMILLAS[f"generar-{memoria}"] if semilla is None else semilla
        tabla = _tabla_caracteres(memoria)
        ctx = CONTEXTO_INICIAL[:memoria]
        return generar_desde(tabla, ALFABETO, ctx, largo - memoria, random.Random(semilla))
    largo = largo or LARGO_PALABRAS
    semilla = SEMILLAS["generar-palabras"] if semilla is None else semilla
    vocab = vocabulario()
    conteos = conteos_palabras(memoria)
    rng = random.Random(semilla)
    salida = list(normalizar_palabras(CONTEXTO_INICIAL)[:memoria])
    uniforme = None
    for _ in range(largo - memoria):
        ctx = tuple(salida[len(salida) - memoria:])
        c = conteos.get(ctx)
        if c is None:
            uniforme = uniforme or [1 / len(vocab)] * len(vocab)
            salida.append(vocab[muestrear_fila(uniforme, rng.random())])
            continue
        # La fila completa en el orden del vocabulario sin sus ceros: un 0 no
        # mueve la suma acumulada, asi que MUESTREAR-FILA elige lo mismo.
        total = sum(c.values())
        siguientes = sorted(c)
        k = muestrear_fila([c[z] / total for z in siguientes], rng.random())
        salida.append(siguientes[k])
    return " ".join(salida)


@lru_cache(maxsize=None)
def _tabla_caracteres(memoria):
    return tabla_desde_conteos(conteos_caracteres(memoria), ALFABETO)


@lru_cache(maxsize=None)
def vocabulario():
    return tuple(sorted(set(palabras_corpus())))


@lru_cache(maxsize=None)
def conteos_palabras(memoria=1):
    return contar(list(palabras_corpus()), memoria)


def subcadena_mas_larga_en_corpus(texto):
    """Largo de la subcadena mas larga de `texto` que aparece literal en el
    corpus (normalizar_caracteres)."""
    corpus = caracteres_corpus()
    mejor = 0
    for i in range(len(texto)):
        largo = mejor + 1
        while i + largo <= len(texto) and texto[i:i + largo] in corpus:
            mejor = largo
            largo += 1
    return mejor


def fraccion_ngramas_en_corpus(texto, n=8):
    """Fraccion de los n-gramas de caracteres de `texto` presentes en el
    corpus."""
    corpus = caracteres_corpus()
    grams = [texto[i:i + n] for i in range(len(texto) - n + 1)]
    return F(sum(1 for g in grams if g in corpus), len(grams))


# ================================================ instancias por pagina ===
#
# Cada funcion devuelve lo que una pagina cita; test_markov.py fija cada
# valor a mano y lo busca en la pagina.

# ----------------------------------------- pagina 1 · lo que necesitas ---

def experimento_posiciones(secuencia=None):
    """El experimento de la pagina 1: elegir al azar una de las posiciones
    con letra siguiente (26 en la frase). A = «la siguiente es vocal»,
    B = «la actual es vocal». Frecuencias exactas."""
    seq = secuencia or frase_vc()
    pares = list(zip(seq, seq[1:]))
    n = len(pares)
    a = sum(1 for s, s2 in pares if s2 == "V")
    b = sum(1 for s, s2 in pares if s == "V")
    ab = sum(1 for s, s2 in pares if s == "V" and s2 == "V")
    a_no_b = sum(1 for s, s2 in pares if s == "C" and s2 == "V")
    return {"posiciones": n, "A": F(a, n), "B": F(b, n), "AyB": F(ab, n),
            "A|B": F(ab, b), "A|noB": F(a_no_b, n - b), "noB": F(n - b, n),
            "A*B": F(a, n) * F(b, n),
            "total": F(ab, b) * F(b, n) + F(a_no_b, n - b) * F(n - b, n)}


def regla_del_producto(tramo="CVC", secuencia=None):
    """Pr(S_i=x, S_{i+1}=y, S_{i+2}=z) con i al azar entre las posiciones que
    tienen dos siguientes, y sus tres factores de la regla encadenada."""
    seq = secuencia or frase_vc()
    ventanas = [seq[i:i + 3] for i in range(len(seq) - 2)]
    n = len(ventanas)
    x = sum(1 for v in ventanas if v[0] == tramo[0])
    xy = sum(1 for v in ventanas if v[:2] == tramo[:2])
    xyz = sum(1 for v in ventanas if v == tramo)
    return {"ventanas": n, "x": x, "xy": xy, "xyz": xyz,
            "Pr(x)": F(x, n), "Pr(y|x)": F(xy, x), "Pr(z|x,y)": F(xyz, xy),
            "conjunta": F(xyz, n)}


# ------------------------------------------------ el problema de Markov ---

MARKOV_1913 = {"letras": 20000, "vocales": 8638, "VV": 1104, "CV": 7534}


def aritmetica_markov_1913():
    """Solo la aritmetica de las cifras historicas (no se recalculan)."""
    d = MARKOV_1913
    consonantes = d["letras"] - d["vocales"]
    return {"consonantes": consonantes, "Pr(V|V)": F(d["VV"], d["vocales"]),
            "Pr(V|C)": F(d["CV"], consonantes)}


def matriz_vce(texto=FRASE):
    """N y P̂ del ejemplo de 3 estados (V, C, _) sobre la frase con espacios."""
    seq = secuencia_vce(texto)
    N = matriz_conteos(seq, ESTADOS_VCE)
    return seq, N, estimar(N)


U_A_MANO = (0.40, 0.75, 0.90, 0.25, 0.10)   # MUESTREAR-FILA a mano, desde C

# Ejercicio (a) de «El problema de Markov»: una cadena de 3 estados dada como grafo.
EJ_P2_ESTADOS = ("1", "2", "3")
EJ_P2_P = [[F(0), F(3, 4), F(1, 4)],
           [F(1, 2), F(0), F(1, 2)],
           [F(1, 3), F(1, 3), F(1, 3)]]
EJ_P2_MU0 = (F(1), F(0), F(0))
EJ_P2_TRAYECTORIA = "1233"


def ejercicio_p2_e():
    """Ejercicio (b) de «El problema de Markov»: «e» (E) contra no «e» (N) en FRASE_E,
    y lo mismo en el corpus."""
    seq = secuencia_e(FRASE_E)
    N = matriz_conteos(seq, ("E", "N"))
    L = letras_corpus()
    seq_c = L.translate({ord(x): ("E" if x == "e" else "N") for x in LETRAS})
    Nc = matriz_conteos(seq_c, ("E", "N"))
    return {"letras": normalizar_vc(FRASE_E), "secuencia": seq, "N": N,
            "P": estimar(N), "Pr(e)": F(seq.count("E"), len(seq)),
            "corpus_Pr(e)": F(seq_c.count("E"), len(seq_c)),
            "corpus_P": estimar(Nc)}


def rachas_resumen():
    """q de cada modelo, Pr(L = ℓ) y el numero de rachas reales."""
    P = matriz_corpus()
    reales = rachas_corpus()
    total = sum(reales.values())
    q_m = P[1][1]
    q_i = 1 - pr_vocal_corpus()
    return {"q_markov": q_m, "q_independiente": q_i, "reales": reales,
            "total": total,
            "pr_markov": {l: rachas_geometrica(q_m, l) for l in range(1, ELL_MAX + 1)},
            "pr_independiente": {l: rachas_geometrica(q_i, l)
                                 for l in range(1, ELL_MAX + 1)}}


# ------------------------------------------------------ ajustar contando ---

P_MITADES = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]

EJ_P3_TEXTO = "abacabbcabac"
EJ_P3_ESTADOS = ("a", "b", "c")


def ejercicio_p3():
    N = matriz_conteos(EJ_P3_TEXTO, EJ_P3_ESTADOS)
    return {"N": N, "salidas": salidas(N), "P": estimar(N),
            "laplace": estimar(N, suavizado=1)}


# -------------------------------------------------------------- predecir ---

EJ_P4_ESTADOS = ("x", "y", "z")
EJ_P4_P = [[F(1, 2), F(1, 4), F(1, 4)],
           [F(1, 3), F(0), F(2, 3)],
           [F(0), F(1, 2), F(1, 2)]]
EJ_P4_MU0 = (F(1, 2), F(1, 2), F(0))
N_EJ_SIMULACION = 400
T_EJ_SIMULACION = 3   # largo de cada trayectoria: cambia la sucesion de u


def ejercicio_p4_simulacion(t_max=T_EJ_SIMULACION):
    """Ejercicio (b): n = 400 replicas desde C con P̂ del corpus; fraccion en
    V por paso, la cuenta y el error estandar."""
    P = matriz_corpus()
    sim = fraccion_simulada(P, MU0_C, N_EJ_SIMULACION, t_max,
                            SEMILLAS["ejercicio-simulacion"])
    cuenta = [float(m[0]) for m in mu_t(P, MU0_C, t_max)]
    return {"simulada": sim, "cuenta": cuenta,
            "ee": [error_estandar(p, N_EJ_SIMULACION) for p in cuenta]}


# --------------------------------------------------------- generar texto ---

U_GENERAR_A_MANO = (0.90, 0.55, 0.30)        # con la tabla V/C/_ de la frase, desde C

EJ_P5_SIMBOLOS = ("a", "n", " ")
EJ_P5_TABLA = [[F(0), F(1, 2), F(1, 2)],
               [F(3, 4), F(0), F(1, 4)],
               [F(1, 2), F(1, 2), F(0)]]
EJ_P5_INICIO = " "
EJ_P5_U = (0.62, 0.15, 0.40, 0.90)


def generar_a_mano(tabla, simbolos, inicio, us):
    """Memoria 1 con uniformes dados: [(contexto, u, simbolo)]."""
    s, pasos = inicio, []
    for u in us:
        k = muestrear_fila(tabla[simbolos.index(s)], u)
        pasos.append((s, u, simbolos[k]))
        s = simbolos[k]
    return pasos


# ======================================================== CLASE 2 ========
#
# Qué pasa a la larga (course/8_markov/2_a_la_larga/). Plan de la clase 2,
# §4 (instancias T1–T10) y §5 (funciones). Los juguetes van en Fraction;
# el corpus, el tablero de 100 y la web del curso en float donde hace falta
# iterar o simular. Las semillas nuevas (2037+) estan en SEMILLAS.

SEMILLAS.update({
    "c2-fraccion-quijote": 2037,       # T6: una trayectoria de T = 100 000
    "c2-partidas-100": 2038,           # T8: n = 10 000 partidas
    "c2-replicas-t4": 2039,            # T4: replicas 2039..2043
    "c2-navegante": 2040,              # T9: el navegante al azar
    "c2-partidas-chico": 2041,         # T7: partidas simuladas
    "c2-fraccion-frase": 2042,         # T1: fraccion del tiempo en V
})

TOL_POTENCIAS = F(1, 10**6)
TOL_PAGERANK = F(1, 10**8)
MAX_PASOS = 10_000

# --------------------------------------------------------- instancias ---

T1_P = [[F(2, 11), F(9, 11)], [F(2, 3), F(1, 3)]]           # V/C de la frase
T2_P = [[F(0), F(1)], [F(1), F(0)]]                         # alternante A, B
T3_P = [[F(1), F(0)], [F(0), F(1)]]                         # identidad
T4_P = [[F(1, 2), F(1, 4), F(1, 4)],                        # s1 transitorio
        [F(0), F(1), F(0)],
        [F(0), F(0), F(1)]]
T5_ESTADOS = ("s1", "s2", "s3", "s4", "s5")
T5_P = [[F(0), F(1, 2), F(0), F(1, 2), F(0)],
        [F(0), F(0), F(1), F(0), F(0)],
        [F(0), F(1), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(1, 2), F(1, 2)],
        [F(0), F(0), F(0), F(1), F(0)]]
T9_PAGINAS = ("A", "B", "C", "D")
T9_ENLACES = {"A": ("B", "C"), "B": ("C",), "C": ("A", "D"), "D": ()}
ALFA = F(17, 20)                                            # 0.85

# T7: casillas 0..5, moneda (avanza 1 o 2), escalera 2 -> 4, serpiente 3 -> 1.
TABLERO_CHICO = {"n": 5, "dado": 2, "saltos": {2: 4, 3: 1}}

# T8: 0..100, dado de 6. Tablero nuestro (no historico). Ningun salto cae
# en la base de otro, ni en 0 ni en 100.
TABLERO_100 = {
    "n": 100, "dado": 6,
    "saltos": {
        # escaleras
        3: 22, 8: 30, 17: 45, 28: 55, 36: 57, 51: 72, 63: 81, 71: 92,
        # serpientes
        33: 6, 47: 26, 49: 11, 62: 19, 64: 42, 87: 24, 95: 56, 98: 78,
    },
}


def t1_matriz():
    """T1 desde la frase (es T1_P; la prueba lo compara)."""
    return matriz_estimada(frase_vc())


# ------------------------------------------------- algebra con Fraction ---

def _resolver(A, b):
    """Gauss-Jordan exacto: A x = b (A cuadrada). Falla si A es singular."""
    k = len(A)
    M = [list(map(F, fila)) + [F(bi)] for fila, bi in zip(A, b)]
    for c in range(k):
        piv = next((r for r in range(c, k) if M[r][c] != 0), None)
        if piv is None:
            raise ValueError("sistema singular: la solucion no es unica")
        M[c], M[piv] = M[piv], M[c]
        p = M[c][c]
        M[c] = [x / p for x in M[c]]
        for r in range(k):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[r][k] for r in range(k)]


def estacionaria(P):
    """mu con mu P = mu, sum mu = 1, exacta. Sistema (P^T - I) mu^T = 0 con
    la ultima ecuacion cambiada por sum = 1. Falla si no es unica."""
    k = len(P)
    A = [[F(P[j][i]) - (1 if i == j else 0) for j in range(k)] for i in range(k)]
    A[-1] = [F(1)] * k
    b = [F(0)] * (k - 1) + [F(1)]
    return _resolver(A, b)


def distancia_1(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def iteracion_potencias(P, mu0, tol=TOL_POTENCIAS, max_pasos=MAX_PASOS):
    """ITERACION DE POTENCIAS en float: mu <- mu P hasta que
    ||mu_nuevo - mu||_1 <= tol. Devuelve (mu, pasos): pasos = cuantas
    multiplicaciones se hicieron. Si llega a max_pasos, pasos = None."""
    Pf = [[float(p) for p in f] for f in P]
    mu = [float(p) for p in mu0]
    k = len(mu)
    for t in range(1, max_pasos + 1):
        nuevo = [sum(mu[i] * Pf[i][j] for i in range(k)) for j in range(k)]
        if distancia_1(nuevo, mu) <= float(tol):
            return nuevo, t
        mu = nuevo
    return mu, None


def distancias_t(P, mu0, t_max=10):
    """[||mu_t - mu||_1 para t = 0..t_max], exactas."""
    mu = estacionaria(P)
    return [distancia_1(m_, mu) for m_ in mu_t(P, mu0, t_max)]


def segundo_valor_propio_2x2(P):
    """En 2x2 el otro valor propio es traza - 1 = 1 - p - q."""
    return F(P[0][0]) + F(P[1][1]) - 1


# ------------------------------------------------------------- clases ---

def _alcanzables(P, s):
    k, vistos, pila = len(P), {s}, [s]
    while pila:
        a = pila.pop()
        for b in range(k):
            if P[a][b] > 0 and b not in vistos:
                vistos.add(b)
                pila.append(b)
    return vistos


def clases(P):
    """Clases de comunicacion en orden de su primer estado:
    [{"estados": (i, …), "cerrada": bool, "periodo": d}]."""
    k = len(P)
    alc = [_alcanzables(P, s) for s in range(k)]
    asignado, salida = set(), []
    for s in range(k):
        if s in asignado:
            continue
        clase = tuple(sorted(t for t in alc[s] if s in alc[t]))
        asignado.update(clase)
        cerrada = all(P[a][b] == 0 for a in clase for b in range(k) if b not in clase)
        # periodo: niveles por BFS dentro de la clase; mcd de nivel(a)+1-nivel(b)
        nivel, cola = {clase[0]: 0}, [clase[0]]
        for a in cola:
            for b in clase:
                if P[a][b] > 0 and b not in nivel:
                    nivel[b] = nivel[a] + 1
                    cola.append(b)
        d = 0
        for a in clase:
            for b in clase:
                if P[a][b] > 0:
                    d = math.gcd(d, nivel[a] + 1 - nivel[b])
        salida.append({"estados": clase, "cerrada": cerrada, "periodo": abs(d) or None})
    return salida


# ------------------------------------------------- fraccion del tiempo ---

def fraccion_del_tiempo(P, s0, T, semilla, estado=0):
    """N_T(estado)/T de UNA trayectoria desde s0 (indice): visitas en los
    pasos 0..T-1. Un u por paso con muestrear_fila."""
    rng = random.Random(semilla)
    filas = [[float(p) for p in f] for f in P]
    s, visitas = s0, 0
    for _ in range(T):
        visitas += s == estado
        s = muestrear_fila(filas[s], rng.random())
    return visitas / T


T_LARGO = 100_000
REPLICAS_T4 = 5


@lru_cache(maxsize=None)
def fraccion_quijote():
    """T6: fraccion del tiempo en V, desde C, T = 100 000, semilla 2037."""
    return fraccion_del_tiempo(matriz_corpus(), 1, T_LARGO, SEMILLAS["c2-fraccion-quijote"])


def fraccion_frase(T=10_000):
    """T1: fraccion del tiempo en V desde C, semilla 2042."""
    return fraccion_del_tiempo(T1_P, 1, T, SEMILLAS["c2-fraccion-frase"])


def fracciones_t4(T=1000, n=REPLICAS_T4):
    """T4 desde s1: fraccion del tiempo en s2 de n replicas (semillas
    2039, 2040, …)."""
    base = SEMILLAS["c2-replicas-t4"]
    return [fraccion_del_tiempo(T4_P, 0, T, base + r, estado=1) for r in range(n)]


# ------------------------------------------------------------ absorcion ---

def tiempo_absorcion(P, objetivo):
    """m(s) = E_s[tau_A] exacto: (I - P_T) m = 1 sobre los estados fuera de
    A = objetivo (indices). Devuelve {s: m(s)} con m = 0 en A."""
    fuera = [s for s in range(len(P)) if s not in objetivo]
    A = [[(1 if i == j else 0) - F(P[i][j]) for j in fuera] for i in fuera]
    m_ = _resolver(A, [F(1)] * len(fuera))
    salida = {s: F(0) for s in objetivo}
    salida.update(dict(zip(fuera, m_)))
    return dict(sorted(salida.items()))


def tablero(n, dado, saltos):
    """Serpientes y escaleras: casillas 0..n, dado de `dado` caras (cada una
    con prob. 1/dado); si te pasas de n llegas a n; al caer en la base de un
    salto vas a su destino. Estados = casillas donde se puede estar al final
    de un turno (las bases de saltos no lo son). Devuelve (estados, P) en
    Fraction; n es absorbente."""
    estados = [c for c in range(n + 1) if c not in saltos]
    idx = {c: i for i, c in enumerate(estados)}
    P = [[F(0)] * len(estados) for _ in estados]
    for c in estados:
        if c == n:
            P[idx[c]][idx[c]] = F(1)
            continue
        for cara in range(1, dado + 1):
            d = min(c + cara, n)
            d = saltos.get(d, d)
            P[idx[c]][idx[d]] += F(1, dado)
    return estados, P


def tablero_desde(config):
    return tablero(config["n"], config["dado"], config["saltos"])


@lru_cache(maxsize=None)
def absorcion_tablero(nombre):
    """{casilla: m(casilla)} exacto de TABLERO_CHICO o TABLERO_100."""
    config = {"chico": TABLERO_CHICO, "100": TABLERO_100}[nombre]
    estados, P = tablero_desde(config)
    m_ = tiempo_absorcion(P, {estados.index(config["n"])})
    return {estados[i]: v for i, v in m_.items()}


def simular_partidas(config, n, semilla):
    """n partidas desde 0: turnos hasta llegar a la meta. Un u por turno
    con muestrear_fila sobre la fila del estado."""
    estados, P = tablero_desde(config)
    filas = [[float(p) for p in f] for f in P]
    meta = estados.index(config["n"])
    rng = random.Random(semilla)
    turnos = []
    for _ in range(n):
        s, t = 0, 0
        while s != meta:
            s = muestrear_fila(filas[s], rng.random())
            t += 1
        turnos.append(t)
    return turnos


def resumen_partidas(config, n, semilla):
    """(media, error estandar s/sqrt(n))."""
    t = simular_partidas(config, n, semilla)
    return statistics.fmean(t), statistics.stdev(t) / math.sqrt(n)


N_PARTIDAS = 10_000


@lru_cache(maxsize=None)
def partidas_100():
    return resumen_partidas(TABLERO_100, N_PARTIDAS, SEMILLAS["c2-partidas-100"])


def partidas_chico():
    return resumen_partidas(TABLERO_CHICO, N_PARTIDAS, SEMILLAS["c2-partidas-chico"])


# ------------------------------------------------------------- PageRank ---

def matriz_barra(enlaces, nodos=None):
    """P̄: cada pagina reparte por igual entre sus enlaces; una sin
    salidas reparte uniforme entre todas (v = 1/k). Fraction."""
    nodos = list(nodos or enlaces)
    idx = {n: i for i, n in enumerate(nodos)}
    k = len(nodos)
    P = []
    for n in nodos:
        destinos = enlaces.get(n, ())
        fila = [F(0)] * k
        if destinos:
            for d in destinos:
                fila[idx[d]] += F(1, len(destinos))
        else:
            fila = [F(1, k)] * k
        P.append(fila)
    return P


def matriz_google(enlaces, alfa=ALFA, nodos=None):
    """G = alfa P̄ + (1 - alfa) 1 v, v uniforme."""
    Pb = matriz_barra(enlaces, nodos)
    k = len(Pb)
    return [[F(alfa) * p + (1 - F(alfa)) * F(1, k) for p in fila] for fila in Pb]


def pagerank(enlaces, alfa=ALFA, tol=TOL_PAGERANK, nodos=None, max_pasos=MAX_PASOS):
    """Iteracion de potencias sin armar G densa:
    mu <- alfa (mu P̄) + (1 - alfa) v, desde mu0 = v, en float.
    Devuelve (nodos, mu, pasos)."""
    nodos = list(nodos or enlaces)
    idx = {n: i for i, n in enumerate(nodos)}
    k = len(nodos)
    a, tolf = float(alfa), float(tol)
    salidas = [[idx[d] for d in enlaces.get(n, ())] for n in nodos]
    mu = [1 / k] * k
    for t in range(1, max_pasos + 1):
        nuevo = [0.0] * k
        colgado = 0.0
        for i, ds in enumerate(salidas):
            if ds:
                parte = mu[i] / len(ds)
                for j in ds:
                    nuevo[j] += parte
            else:
                colgado += mu[i]
        nuevo = [a * (x + colgado / k) + (1 - a) / k for x in nuevo]
        if distancia_1(nuevo, mu) <= tolf:
            return nodos, nuevo, t
        mu = nuevo
    return nodos, mu, None


def pagerank_exacto(enlaces, alfa=ALFA, nodos=None):
    return estacionaria(matriz_google(enlaces, alfa, nodos))


def navegante(enlaces=T9_ENLACES, alfa=ALFA, T=T_LARGO, semilla=None):
    """Fraccion del tiempo del navegante al azar en cada pagina (UNA
    trayectoria desde la primera pagina, un u por paso sobre la fila de G)."""
    semilla = SEMILLAS["c2-navegante"] if semilla is None else semilla
    G = matriz_google(enlaces, alfa)
    filas = [[float(p) for p in f] for f in G]
    rng = random.Random(semilla)
    s, visitas = 0, [0] * len(G)
    for _ in range(T):
        visitas[s] += 1
        s = muestrear_fila(filas[s], rng.random())
    return [v / T for v in visitas]


# ---------------------------------------------------- la web del curso ---

CURSO = RAIZ / "course"
ENLACES_CURSO = RAIZ / "tools/datos/markov/enlaces_curso.tsv"
FECHA_FOTO = "2026-10-21"
_RE_WIKI = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
_RE_RAYA = re.compile(r"raya:([A-Za-z0-9_-]+)")


def _frontmatter(texto):
    if not texto.startswith("---"):
        return {}
    fin = texto.find("\n---", 3)
    datos = {}
    for renglon in texto[3:fin].splitlines():
        if ":" in renglon and not renglon.startswith((" ", "-")):
            clave, valor = renglon.split(":", 1)
            datos[clave.strip()] = valor.strip().strip('"').strip("'")
    return datos


def enlaces_curso(raiz=CURSO):
    """Lee course/: nodos = cada .md con id fuera de directorios _*;
    enlaces = wikilinks [[id|…]] y raya:id entre ellas (por id o alias),
    sin repetir ni a si misma. Devuelve (nodos {id: titulo}, enlaces
    {id: tuple(destinos)}), ordenados por id."""
    paginas, alias = {}, {}
    for ruta in sorted(raiz.rglob("*.md")):
        if any(p.startswith("_") for p in ruta.relative_to(raiz).parts[:-1]):
            continue
        texto = ruta.read_text(encoding="utf-8")
        fm = _frontmatter(texto)
        if not fm.get("id"):
            continue
        pid = fm["id"]
        paginas[pid] = (fm.get("title", pid), texto)
        alias[pid] = pid
        al = fm.get("aliases", "")
        for a in re.findall(r"[A-Za-z0-9_-]+", al.strip("[]")):
            alias.setdefault(a, pid)
    nodos = {pid: paginas[pid][0] for pid in sorted(paginas)}
    enlaces = {}
    for pid in nodos:
        texto = paginas[pid][1]
        destinos = set()
        for objetivo in _RE_WIKI.findall(texto) + _RE_RAYA.findall(texto):
            d = alias.get(objetivo.strip())
            if d and d != pid:
                destinos.add(d)
        enlaces[pid] = tuple(sorted(destinos))
    return nodos, enlaces


def escribir_foto(ruta=ENLACES_CURSO):
    """La foto fija: renglones «nodo<TAB>id<TAB>titulo» y
    «enlace<TAB>origen<TAB>destino»."""
    nodos, enlaces = enlaces_curso()
    renglones = ["tipo\ta\tb"]
    renglones += [f"nodo\t{i}\t{t}" for i, t in nodos.items()]
    renglones += [f"enlace\t{o}\t{d}" for o, ds in enlaces.items() for d in ds]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text("\n".join(renglones) + "\n", encoding="utf-8")


def leer_foto(ruta=ENLACES_CURSO):
    """(nodos, enlaces) de la foto fija, como enlaces_curso()."""
    nodos, enlaces = {}, {}
    for renglon in ruta.read_text(encoding="utf-8").splitlines()[1:]:
        tipo, a, b = renglon.split("\t")
        if tipo == "nodo":
            nodos[a] = b
            enlaces[a] = ()
        else:
            enlaces[a] = enlaces[a] + (b,)
    return nodos, enlaces


@lru_cache(maxsize=None)
def pagerank_curso():
    """T10 sobre la foto: {"nodos", "enlaces", "sin_salidas", "top5":
    [(id, titulo, valor)], "pasos"}."""
    nodos, enlaces = leer_foto()
    ids, mu, pasos = pagerank(enlaces, nodos=list(nodos))
    orden = sorted(range(len(ids)), key=lambda i: -mu[i])
    return {
        "nodos": len(nodos),
        "enlaces": sum(len(d) for d in enlaces.values()),
        "sin_salidas": sum(1 for d in enlaces.values() if not d),
        "top5": [(ids[i], nodos[ids[i]], mu[i]) for i in orden[:5]],
        "pasos": pasos,
    }


if __name__ == "__main__":
    if sys.argv[1:] == ["foto"]:
        escribir_foto()
        print(f"escrita {ENLACES_CURSO}")
