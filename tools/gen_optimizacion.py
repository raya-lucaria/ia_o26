"""Genera los diagramas SVG de la unidad de modelado y optimizacion.

Mismo patron que gen_complejidad.py: paleta en constantes, una funcion por
diagrama que devuelve una cadena SVG completa, y un catalogo DIAGRAMAS que el
generador y su prueba comparten como unica fuente de "que diagramas existen".

Los ids llevan prefijo "opt-" a proposito: los ids de objeto numerado de Raya
son unicos en TODO el curso, no por pagina.

Dos de los cinco CALCULAN su contenido en vez de dibujarlo a mano:
opt_poligono y opt_curvas_de_nivel derivan los vertices del modelo del episodio
(A, B, C mas abajo) con aritmetica exacta de fracciones. Si un parametro del
impresora cambia, el dibujo cambia solo y no hay que mover coordenadas.
"""
import math
import sys
from fractions import Fraction as F
from itertools import combinations
from xml.sax.saxutils import escape

from unidades import ASSETS_OPTIMIZACION

ASSETS = ASSETS_OPTIMIZACION

# Paleta del skin eva-cyberpunk, identica a gen_complejidad.py. FONDO es
# tokens.color.surface y va horneado en cada SVG: test_9 de test_aceptacion.py
# falla sin el.
FONDO, TEXTO, SUAVE, LINEA = "#211033", "#f7f2ff", "#c8b9d8", "#78419e"
ACENTO = "#f04cff"
SERIE = ["#a8ff5a", "#55ddff", "#ffd166"]
ALARMA = "#ff5a7a"
FUENTE = "system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

# El episodio de la impresora. Unica fuente de los numeros para los dos
# diagramas que calculan.
A = [[1, 1], [2, 1], [1, 2]]
B = [10, 18, 18]
C = [4, 3]
NOMBRES = ["horas", "polimero", "energia"]


def marco(ancho, alto, aria, titulo, desc):
    """Etiqueta <svg> raiz con los atributos que exigen las guardas.

    Ademas de los cinco heredados (width, height, viewBox, role, aria-label)
    esta unidad estrena <title> y <desc> internos: ningun SVG del curso los
    llevaba, y son lo que un lector de pantalla anuncia al entrar en la figura.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
        f'viewBox="0 0 {ancho} {alto}" role="img" aria-label="{escape(aria)}">'
        f"<title>{escape(titulo)}</title><desc>{escape(desc)}</desc>"
        f'<rect x="0" y="0" width="{ancho}" height="{alto}" rx="16" fill="{FONDO}"/>'
        f'<defs><marker id="p" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ACENTO}"/></marker>'
        f'<marker id="s" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{SUAVE}"/></marker></defs>'
    )


def cierre():
    return "</svg>"


def texto(x, y, s, color=TEXTO, tam=15, anclaje="middle", peso="normal", fuente=None):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{fuente or FUENTE}" '
        f'font-size="{tam}" font-weight="{peso}" text-anchor="{anclaje}">'
        f"{escape(s)}</text>"
    )


def caja(x, y, w, h, relleno="none", borde=LINEA, radio=10, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radio}" '
        f'fill="{relleno}" stroke="{borde}" stroke-width="{grosor}"{trazo}/>'
    )


def flecha(x1, y1, x2, y2, color=ACENTO, grosor=2, marcador="p"):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{grosor}" marker-end="url(#{marcador})"/>'
    )


def linea(x1, y1, x2, y2, color=LINEA, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{grosor}"{trazo}/>'
    )


def mezclar(color, fraccion, fondo=FONDO):
    """Color solido equivalente a pintar `color` con opacidad `fraccion`.

    Se mezcla aqui en vez de emitir fill-opacity: un sombreado opaco encima de
    otra curva la tapa en los renderizadores que ignoran la opacidad, y eso ya
    se publico una vez en la unidad de complejidad.
    """
    def canales(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

    r0, g0, b0 = canales(fondo)
    r1, g1, b1 = canales(color)
    return "#%02x%02x%02x" % tuple(
        round(c0 + (c1 - c0) * fraccion) for c0, c1 in ((r0, r1), (g0, g1), (b0, b1))
    )


def punto(x, y, r=5, color=ACENTO):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


# --------------------------------------------------------------------------
# geometria del episodio, exacta

def _region(filas_a, lados_b):
    """Vertices ordenados de {A x <= b, x >= 0}, en fracciones exactas."""
    filas = list(filas_a) + [[-1, 0], [0, -1]]
    lados = list(lados_b) + [0, 0]
    V = []
    for i, j in combinations(range(len(filas)), 2):
        (a1, b1), (a2, b2) = filas[i], filas[j]
        det = a1 * b2 - b1 * a2
        if det == 0:
            continue
        x = F(lados[i] * b2 - b1 * lados[j], det)
        y = F(a1 * lados[j] - lados[i] * a2, det)
        if any(filas[k][0] * x + filas[k][1] * y > lados[k] for k in range(len(filas))):
            continue
        if (x, y) not in V:
            V.append((x, y))
    import math
    cx = sum(p[0] for p in V) / len(V)
    cy = sum(p[1] for p in V) / len(V)
    V.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    return V


def vertices():
    """Las esquinas de la region factible, con fracciones exactas.

    Cruza las cinco rectas de dos en dos y se queda con los cruces que cumplen
    todas las desigualdades: es el mismo procedimiento que ensena la pagina 3.
    """
    filas = A + [[-1, 0], [0, -1]]
    lados = list(B) + [0, 0]
    V = []
    for i, j in combinations(range(len(filas)), 2):
        (a1, b1), (a2, b2) = filas[i], filas[j]
        det = a1 * b2 - b1 * a2
        if det == 0:
            continue
        x = F(lados[i] * b2 - b1 * lados[j], det)
        y = F(a1 * lados[j] - lados[i] * a2, det)
        if any(filas[k][0] * x + filas[k][1] * y > lados[k] for k in range(len(filas))):
            continue
        if (x, y) not in V:
            V.append((x, y))
    # orden antihorario alrededor del centroide, para que el path cierre bien
    cx = sum(p[0] for p in V) / len(V)
    cy = sum(p[1] for p in V) / len(V)
    import math
    V.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    return V


def valor(p):
    return C[0] * p[0] + C[1] * p[1]


def _activas(p):
    """Indices de las restricciones que p cumple con igualdad, las cinco."""
    filas = A + [[-1, 0], [0, -1]]
    lados = list(B) + [0, 0]
    return frozenset(i for i in range(len(filas))
                     if filas[i][0] * p[0] + filas[i][1] * p[1] == lados[i])


def vecinos(v, w):
    """Vecinos = los une una arista, decidido por RANGO n-1, no por conteo.

    Con n = 2 eso es rango 1 de las activas compartidas. Contarlas sin mirar
    la independencia declara vecinos a los extremos de la diagonal de una
    cara, y esa version falsa ya estuvo escrita una vez en el diseno.
    """
    if v == w:
        return False
    filas = A + [[-1, 0], [0, -1]]
    comp = [filas[i] for i in _activas(v) & _activas(w)]
    if not comp:
        return False                       # rango 0: no comparten nada
    base = comp[0]                         # rango 1 <=> todas paralelas
    return all(base[0] * f[1] - base[1] * f[0] == 0 for f in comp)


def camino_simplex():
    """La traza de simplex desde el origen, calculada, no transcrita.

    Empieza en el origen —que siempre es vertice factible aqui, porque todas
    las restricciones son <= con lado derecho no negativo—, y en cada paso se
    va al vecino que mas paga. La regla de desempate es la que declara la
    pagina: el de menor x1, y si tambien empatan, el de menor x2.
    """
    V = vertices()
    v = next(p for p in V if p[0] == 0 and p[1] == 0)
    ruta = [v]
    while True:
        mejores = [w for w in V if vecinos(ruta[-1], w) and valor(w) > valor(ruta[-1])]
        if not mejores:
            return ruta
        ruta.append(max(mejores, key=lambda w: (valor(w), -w[0], -w[1])))


def rotulo(p):
    def n(t):
        return str(t) if t.denominator == 1 else f"{t.numerator}/{t.denominator}"
    return f"({n(p[0])}, {n(p[1])})"


# --------------------------------------------------------------------------
# diagramas

def opt_anatomia():
    """El modelo escrito, con cada una de sus partes señalada por su nombre.

    No es un diagrama de proceso: es una radiografía. El lector debe poder
    apuntar a cualquier símbolo de la forma canónica y decir cómo se llama.
    """
    W, H = 940, 560
    s = [marco(
        W, H,
        "La forma canónica del modelo con cada parte señalada: sentido, función "
        "objetivo, coeficientes, variables de decisión, restricciones, lados "
        "derechos y dominio",
        "Las partes de un problema de optimización",
        "El modelo de la impresora escrito en forma canonica. Flechas y "
        "etiquetas nombran el sentido max, la funcion objetivo, los "
        "coeficientes de precio, las variables de decision, las tres "
        "restricciones de recurso, sus coeficientes de consumo, los lados "
        "derechos con lo disponible, y el dominio.",
    )]
    fx = 330                      # donde empieza la fórmula
    filas = [
        (150, "max", "4x\u2081 + 3x\u2082", ACENTO),
        (232, "sujeto a", "x\u2081 +  x\u2082  \u2264 10", SERIE[0]),
        (280, "", "2x\u2081 +  x\u2082  \u2264 18", SERIE[0]),
        (328, "", "x\u2081 + 2x\u2082  \u2264 18", SERIE[0]),
        (400, "", "x\u2081 \u2265 0,  x\u2082 \u2265 0", SERIE[1]),
    ]
    for y, izq, der, color in filas:
        if izq:
            s.append(texto(fx - 18, y + 6, izq, color=SUAVE, tam=17, anclaje="end",
                           fuente=MONO))
        s.append(texto(fx + 8, y + 6, der, color=color, tam=20, anclaje="start",
                       fuente=MONO))
    s.append(caja(fx - 8, 214, 320, 148, borde=mezclar(SERIE[0], 0.6), guiones="6 5"))
    s.append(caja(fx - 8, 380, 320, 40, borde=mezclar(SERIE[1], 0.6), guiones="6 5"))

    def etiqueta(x, y, texto_, color, hacia, anc="start"):
        s.append(flecha(x, y, hacia[0], hacia[1], color=color, grosor=1.6,
                        marcador="s" if color == SUAVE else "p"))
        s.append(texto(x + (6 if anc == "start" else -6), y + 5, texto_,
                       color=color, tam=13, anclaje=anc))

    # izquierda
    etiqueta(196, 118, "el sentido:", SUAVE, (300, 143), anc="end")
    s.append(texto(190, 136, "máximo o mínimo", color=SUAVE, tam=13, anclaje="end"))
    etiqueta(300, 200, "una restricción por recurso", SERIE[0], (360, 224), anc="end")
    etiqueta(258, 300, "coeficientes:", SERIE[0], (338, 284), anc="end")
    s.append(texto(252, 318, "cuánto consume cada pieza", color=SUAVE, tam=12,
                   anclaje="end"))
    etiqueta(240, 400, "el dominio", SERIE[1], (322, 400), anc="end")
    s.append(texto(234, 418, "con qué números", color=SUAVE, tam=12, anclaje="end"))
    s.append(texto(234, 434, "se trabaja", color=SUAVE, tam=12, anclaje="end"))
    # derecha
    etiqueta(700, 116, "la función objetivo:", ACENTO, (560, 143))
    s.append(texto(706, 134, "lo que se quiere", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(706, 150, "lo más grande posible", color=SUAVE, tam=13, anclaje="start"))
    etiqueta(700, 196, "coeficientes del objetivo:", SERIE[2], (430, 168))
    s.append(texto(706, 214, "cuánto vale cada pieza", color=SUAVE, tam=13, anclaje="start"))
    etiqueta(700, 300, "lado derecho:", SERIE[0], (620, 284))
    s.append(texto(706, 318, "cuánto hay de ese recurso", color=SUAVE, tam=13,
                   anclaje="start"))
    etiqueta(700, 412, "variables de decisión:", ACENTO, (580, 402))
    s.append(texto(706, 430, "lo único que eliges", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(W / 2, 40, "las siete partes de un problema de optimización",
                   color=SUAVE, tam=16))
    s.append(texto(W / 2, 505,
                   "si puedes nombrar cada símbolo, ya sabes leer un modelo",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_lienzo():
    W, H = 900, 400
    s = [marco(
        W, H,
        "Siete pasos en dos bloques: cuatro para construir el modelo y tres "
        "para revisarlo, con una flecha de regreso del segundo al primero",
        "El lienzo de modelado",
        "Bloque de construir con los pasos que decido, que se, que quiero y "
        "que no puedo. Bloque de revisar con las unidades, la solucion tonta y "
        "la forma. Una flecha regresa del segundo bloque al primero.",
    )]
    bloques = [
        ("Construir", 40, [
            ("1", "¿Qué decido?"),
            ("2", "¿Qué sé?"),
            ("3", "¿Qué quiero?"),
            ("4", "¿Qué no puedo?"),
        ]),
        ("Revisar", 500, [
            ("5", "¿Cuadran las unidades?"),
            ("6", "¿Hay una tonta, y ninguna absurda?"),
            ("7", "¿Qué forma tiene?"),
        ]),
    ]
    for titulo, x0, pasos in bloques:
        alto = 60 + 58 * len(pasos)
        s.append(caja(x0, 60, 360, alto, borde=SUAVE, guiones="6 5"))
        s.append(texto(x0 + 180, 48, titulo, color=SUAVE, tam=15, peso="600"))
        for k, (num, etiqueta) in enumerate(pasos):
            y = 96 + 58 * k
            s.append(caja(x0 + 20, y, 320, 44, relleno=mezclar(LINEA, 0.22), borde=LINEA))
            s.append(punto(x0 + 44, y + 22, r=13, color=ACENTO))
            s.append(texto(x0 + 44, y + 27, num, color=FONDO, tam=14, peso="700"))
            s.append(texto(x0 + 68, y + 27, etiqueta, anclaje="start", tam=14))
    s.append(flecha(400, 140, 500, 140))
    s.append(texto(450, 128, "se construye", color=SUAVE, tam=12))
    s.append(flecha(500, 330, 400, 330, color=SUAVE, marcador="s"))
    s.append(texto(450, 352, "si algo no cuadra, vuelves", color=SUAVE, tam=12))
    s.append(cierre())
    return "".join(s)


def opt_la_impresora():
    """La situacion entera de un vistazo, SIN numeros.

    Los numeros son la respuesta del ejercicio de la pagina 1; el diagrama
    ensena la estructura —que se gasta, que se decide, que se gana— para que el
    lector entienda la historia sin que nadie le resuelva la tabla.
    """
    W, H = 940, 400
    s = [marco(
        W, H,
        "Tres recursos limitados entran a la impresora, que produce filtros de "
        "aire y celdas de agua; el depósito paga créditos por cada pieza",
        "Qué decide la tripulación",
        "A la izquierda tres recursos que se gastan y se acaban: horas de "
        "impresora, polimero y energia. En medio la impresora, donde se decide "
        "cuantos filtros y cuantas celdas hacer. A la derecha el deposito, que "
        "paga creditos por cada pieza entregada.",
    )]
    # columna 1: los recursos
    s.append(texto(140, 44, "lo que se gasta", color=SERIE[0], tam=14, peso="600"))
    s.append(texto(140, 64, "y se acaba", color=SUAVE, tam=12))
    for k, (nombre, unidad) in enumerate([("Horas de impresora", "antes de la parada"),
                                          ("Polímero", "kilos en la bodega"),
                                          ("Energía", "kilowatt-hora del reactor")]):
        y = 96 + 76 * k
        s.append(caja(30, y, 220, 58, relleno=mezclar(SERIE[0], 0.16), borde=SERIE[0]))
        s.append(texto(140, y + 26, nombre, tam=14, peso="600"))
        s.append(texto(140, y + 45, unidad, color=SUAVE, tam=12))
        s.append(flecha(254, y + 29, 316, 200 if k != 1 else y + 29,
                        color=SERIE[0], grosor=2))
    # columna 2: la decision
    s.append(caja(320, 96, 220, 214, relleno=mezclar(ACENTO, 0.14), borde=ACENTO, grosor=2.5))
    s.append(texto(430, 44, "lo que se decide", color=ACENTO, tam=14, peso="600"))
    s.append(texto(430, 64, "y es la pregunta", color=SUAVE, tam=12))
    s.append(texto(430, 136, "LA IMPRESORA", color=ACENTO, tam=15, peso="700"))
    s.append(texto(430, 176, "¿cuántos filtros", tam=15))
    s.append(texto(430, 200, "y cuántas celdas", tam=15))
    s.append(texto(430, 224, "imprimir con esto?", tam=15))
    s.append(texto(430, 268, "no se puede todo:", color=SUAVE, tam=12))
    s.append(texto(430, 286, "los tres se acaban", color=SUAVE, tam=12))
    # columna 3: las piezas
    for k, (nombre, detalle) in enumerate([("Filtro de aire", "4 créditos"),
                                           ("Celda de agua", "3 créditos")]):
        y = 116 + 110 * k
        s.append(flecha(544, 203, 606, y + 30, color=ACENTO, grosor=2))
        s.append(caja(610, y, 180, 60, relleno=mezclar(SERIE[1], 0.16), borde=SERIE[1]))
        s.append(texto(700, y + 27, nombre, tam=14, peso="600"))
        s.append(texto(700, y + 46, detalle, color=SERIE[1], tam=13))
        s.append(flecha(794, y + 30, 856, 200, color=SERIE[1], grosor=2))
    s.append(texto(700, 44, "lo que se entrega", color=SERIE[1], tam=14, peso="600"))
    # columna 4: el deposito
    s.append(caja(860, 140, 60, 120, relleno=mezclar(SERIE[2], 0.16), borde=SERIE[2]))
    for i, ch in enumerate("DEPÓSITO"):
        s.append(texto(890, 162 + 13 * i, ch, color=SERIE[2], tam=12, peso="700"))
    s.append(texto(890, 292, "paga", color=SERIE[2], tam=13, peso="600"))
    s.append(texto(890, 310, "créditos", color=SERIE[2], tam=13, peso="600"))
    s.append(texto(W / 2, 360,
                   "3 recursos que se acaban, 2 piezas que se pueden imprimir, "
                   "1 total que se quiere lo más grande posible",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_historia_a_modelo():
    W, H = 900, 380
    s = [marco(
        W, H,
        "Dos columnas: a la izquierda las frases de la bitacora, a la derecha "
        "la desigualdad que produce cada una; el ultimo renglón tiene la "
        "columna izquierda vacía",
        "De la frase a la desigualdad",
        "Cinco renglones. Los cuatro primeros llevan una frase de la bitacora y "
        "su traduccion. El quinto tiene la izquierda vacia porque la no "
        "negatividad no la dice nadie.",
    )]
    s.append(texto(230, 44, "Lo que dice la bitácora", color=SUAVE, tam=14, peso="600"))
    s.append(texto(700, 44, "Lo que se escribe", color=SUAVE, tam=14, peso="600"))
    filas = [
        ("4 créditos por filtro, 3 por celda", "max 4x₁ + 3x₂", SERIE[2]),
        ("10 horas, y cada pieza se lleva 1", "x₁ + x₂ ≤ 10", SERIE[0]),
        ("18 kilos; el filtro 2, la celda 1", "2x₁ + x₂ ≤ 18", SERIE[0]),
        ("el filtro gasta 1, la celda 2", "x₁ + 2x₂ ≤ 18", SERIE[0]),
        (None, "x₁ ≥ 0,  x₂ ≥ 0", SERIE[1]),
    ]
    for k, (izq, der, color) in enumerate(filas):
        y = 70 + 58 * k
        if izq is None:
            s.append(caja(40, y, 380, 44, borde=SUAVE, guiones="5 5"))
            s.append(texto(230, y + 28, "(nadie lo dice)", color=SUAVE, tam=13))
        else:
            s.append(caja(40, y, 380, 44, relleno=mezclar(LINEA, 0.18), borde=LINEA))
            s.append(texto(58, y + 28, izq, anclaje="start", tam=13))
        s.append(flecha(430, y + 22, 500, y + 22, color=SUAVE, marcador="s"))
        s.append(caja(510, y, 350, 44, borde=color))
        s.append(texto(685, y + 28, der, color=color, tam=15, fuente=MONO))
    s.append(cierre())
    return "".join(s)


def _plano(W, H, ox, oy, esc, top):
    """Ejes, rejilla y numeros. Devuelve las funciones de conversion y el SVG."""
    def px(u):
        return ox + float(u) * esc

    def py(u):
        return oy - float(u) * esc

    s = []
    for u in range(0, int(top) + 1, 2):
        s.append(linea(px(u), py(0), px(u), py(top), color=mezclar(LINEA, 0.4), grosor=1))
        s.append(linea(px(0), py(u), px(top), py(u), color=mezclar(LINEA, 0.4), grosor=1))
    s.append(flecha(px(0), py(0), px(top) + 16, py(0), color=SUAVE, marcador="s"))
    s.append(flecha(px(0), py(0), px(0), py(top) + 16, color=SUAVE, marcador="s"))
    s.append(texto(px(top) + 30, py(0) + 6, "x\u2081", color=SUAVE, tam=15))
    s.append(texto(px(0) + 22, py(top) - 20, "x\u2082", color=SUAVE, tam=15, anclaje="start"))
    for u in range(2, int(top) + 1, 2):
        s.append(texto(px(u), py(0) + 24, str(u), color=SUAVE, tam=12))
        s.append(texto(px(0) - 12, py(u) + 5, str(u), color=SUAVE, tam=12, anclaje="end"))
    return px, py, s


def _corte(a1, a2, b, top):
    """Los dos extremos visibles de la recta a1 x1 + a2 x2 = b en la ventana."""
    cand = []
    if a2:
        for x in (0, top):
            y = (b - a1 * x) / a2
            if -0.01 <= y <= top + 0.01:
                cand.append((x, y))
    if a1:
        for y in (0, top):
            x = (b - a2 * y) / a1
            if -0.01 <= x <= top + 0.01:
                cand.append((x, y))
    vistos, out = set(), []
    for c in cand:
        k = (round(c[0], 6), round(c[1], 6))
        if k not in vistos:
            vistos.add(k)
            out.append(c)
    return out[:2]


def _leyenda(x, y, filas, ancho=250):
    """Caja de leyenda: un cuadro de color y un texto por fila."""
    s = [caja(x, y, ancho, 26 + 26 * len(filas), relleno=mezclar(LINEA, 0.16), borde=SUAVE)]
    for k, (color, etiqueta) in enumerate(filas):
        yy = y + 22 + 26 * k
        s.append(f'<rect x="{x + 14}" y="{yy - 9}" width="22" height="4" rx="2" '
                 f'fill="{color}"/>')
        s.append(texto(x + 46, yy - 3, etiqueta, color=TEXTO, tam=13, anclaje="start"))
    return s


# Desplazamiento del rotulo de cada esquina, elegido a mano para que ninguno
# choque con otro, con un eje o con una recta. Revisado renderizando en Chrome.
# El de (0,9) iba arriba a la derecha y la recta de las horas —que sale justo
# de (0,10), un paso mas arriba— le entraba por el parentesis de apertura; lo
# encontro la guarda de rotulos, no el ojo. A la derecha no hay corrimiento que
# lo salve: la recta baja con la misma pendiente con la que crece el texto. Se
# fue a la izquierda del eje, a la altura de su punto, donde no hay nada.
ROTULOS = {
    (0, 0): (0, 48, "middle"),
    (9, 0): (0, 48, "middle"),
    (8, 2): (16, -14, "start"),
    (2, 8): (14, -16, "start"),
    (0, 9): (-8, -6, "end"),
}


def opt_poligono():
    W, H = 720, 560
    ox, oy, esc, top = 90, 460, 34, 10
    V = vertices()
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    s = [marco(
        W, H,
        "Las tres rectas de recurso y los dos ejes recortan una región de "
        "cinco lados; sus cinco esquinas están marcadas y rotuladas",
        "La región factible de la impresora",
        "Region sombreada con esquinas en (0,0), (9,0), (8,2), (2,8) y (0,9). "
        "Las tres rectas de recurso la cierran por arriba y por la derecha. "
        "La esquina (8,2) esta resaltada porque es la mejor.",
    )]
    d = " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                 for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{d}" fill="{mezclar(ACENTO, 0.24)}" stroke="none"/>')
    s += plano
    for k, (a1, a2) in enumerate(A):
        extremos = _corte(a1, a2, B[k], top)
        if len(extremos) == 2:
            (x1, y1), (x2, y2) = extremos
            s.append(linea(px(x1), py(y1), px(x2), py(y2), color=SERIE[k], grosor=2.5))
    mejor = max(V, key=valor)
    for p in V:
        clave = (int(p[0]), int(p[1]))
        dx, dy, anc = ROTULOS[clave]
        es_mejor = p == mejor
        s.append(punto(px(p[0]), py(p[1]), r=8 if es_mejor else 5,
                       color=ACENTO if es_mejor else TEXTO))
        s.append(texto(px(p[0]) + dx, py(p[1]) + dy, rotulo(p),
                       color=ACENTO if es_mejor else SUAVE, tam=13, anclaje=anc,
                       peso="700" if es_mejor else "normal"))
    s += _leyenda(400, 60, [
        (SERIE[0], "x\u2081 + x\u2082 \u2264 10   horas"),
        (SERIE[1], "2x\u2081 + x\u2082 \u2264 18   polímero"),
        (SERIE[2], "x\u2081 + 2x\u2082 \u2264 18   energía"),
    ], ancho=290)
    s.append(texto(W / 2, 34, "cinco semiplanos, cinco esquinas", color=SUAVE, tam=15))
    s.append(cierre())
    return "".join(s)


def opt_curvas_de_nivel():
    W, H = 720, 560
    ox, oy, esc, top = 90, 460, 34, 10
    V = vertices()
    mejor = max(V, key=valor)
    optimo = int(valor(mejor))
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    s = [marco(
        W, H,
        "El polígono con cuatro rectas paralelas rotuladas con su valor; "
        "la de valor 38 toca la región en un solo punto",
        "La familia de curvas de nivel",
        "Cuatro rectas paralelas de la misma inclinacion. Las de valor 12 y 24 "
        "cruzan la region, la de 38 la toca solo en la esquina (8,2) y la de 48 "
        "queda fuera. Una flecha marca el sentido en que crece el valor.",
    )]
    d = " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                 for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{d}" fill="{mezclar(ACENTO, 0.20)}" '
             f'stroke="{mezclar(ACENTO, 0.85)}" stroke-width="2.5"/>')
    s += plano
    for v in (12, 24, optimo, 48):
        es_optimo = v == optimo
        color = ACENTO if es_optimo else SUAVE
        extremos = _corte(C[0], C[1], v, top)
        if len(extremos) != 2:
            continue
        (x1, y1), (x2, y2) = extremos
        s.append(linea(px(x1), py(y1), px(x2), py(y2), color=color,
                       grosor=3.2 if es_optimo else 1.8,
                       guiones=None if es_optimo else "7 6"))
        # el rotulo va sobre la recta, a un tercio de su extremo alto, para
        # que no choque ni con el eje ni con los numeros de la escala
        alto = max(extremos, key=lambda t: t[1])
        bajo = min(extremos, key=lambda t: t[1])
        rx = alto[0] + (bajo[0] - alto[0]) * 0.3
        ry = alto[1] + (bajo[1] - alto[1]) * 0.3
        s.append(texto(px(rx) + 14, py(ry) - 6, f"{v}", color=color,
                       tam=14, anclaje="start", peso="700" if es_optimo else "normal"))
    s.append(punto(px(mejor[0]), py(mejor[1]), r=8))
    s.append(texto(px(mejor[0]) + 16, py(mejor[1]) - 12, rotulo(mejor),
                   color=ACENTO, tam=13, anclaje="start", peso="700"))
    s.append(flecha(px(0.7), py(0.7), px(2.6), py(2.15), color=SERIE[0], grosor=2.5))
    s.append(texto(px(2.8), py(2.15) + 4, "crece el valor", color=SERIE[0], tam=13,
                   anclaje="start"))
    s += _leyenda(400, 60, [
        (ACENTO, "4x\u2081 + 3x\u2082 = 38, la que gana"),
        (SUAVE, "las demás: no tocan, o sobran"),
    ], ancho=290)
    s.append(texto(W / 2, 34, "se empuja hasta que sale", color=SUAVE, tam=15))
    s.append(cierre())
    return "".join(s)


def opt_sin_energia():
    """Los dos polígonos: el real y el que queda al tachar la energía.

    Es el dibujo del argumento del umbral. Calcula las dos regiones desde los
    mismos parámetros del episodio, así que si un dato cambia el dibujo cambia.
    """
    W, H = 720, 560
    ox, oy, esc, top = 90, 460, 34, 10
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    grande = _region([A[0], A[1]], [B[0], B[1]])      # sin la energía
    real = vertices()
    mejor = max(real, key=valor)
    s = [marco(
        W, H,
        "Dos regiones superpuestas: la que queda al quitar la restricción de "
        "energía, más grande, y la real dentro de ella; la esquina (8,2) "
        "pertenece a las dos",
        "El techo no depende de la energía",
        "Al tachar la restriccion de energia la region crece y pasa a tener "
        "cuatro esquinas: (0,0), (0,10), (8,2) y (9,0), que valen 0, 30, 38 y "
        "36. La esquina (8,2) sigue siendo la mejor, y esta tambien en la "
        "region real.",
    )]
    d = lambda V: " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                           for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{d(grande)}" fill="{mezclar(SERIE[1], 0.20)}" '
             f'stroke="{SERIE[1]}" stroke-width="2.5" stroke-dasharray="8 5"/>')
    s.append(f'<path d="{d(real)}" fill="{mezclar(ACENTO, 0.30)}" '
             f'stroke="{mezclar(ACENTO, 0.8)}" stroke-width="2"/>')
    s += plano
    for p in grande:
        es_mejor = p == mejor
        s.append(punto(px(p[0]), py(p[1]), r=8 if es_mejor else 5,
                       color=ACENTO if es_mejor else SERIE[1]))
        # desplazamientos a mano, revisados renderizando: (0,10) choca con el
        # rótulo del eje si va arriba, y (9,0) choca con el pie si va abajo.
        dx, dy, anc = {(0, 0): (14, 26, "start"),
                       (0, 10): (30, 20, "start"),
                       (9, 0): (-20, -18, "end")}.get(
                          (int(p[0]), int(p[1])), (16, -14, "start"))
        if es_mejor:
            dx, dy, anc = 18, -12, "start"
        s.append(texto(px(p[0]) + dx, py(p[1]) + dy,
                       f"{rotulo(p)} = {valor(p)}",
                       color=ACENTO if es_mejor else SERIE[1], tam=13, anclaje=anc,
                       peso="700" if es_mejor else "normal"))
    s += _leyenda(378, 60, [
        (SERIE[1], "sin la energía: 4 esquinas"),
        (ACENTO, "la región real, dentro"),
    ], ancho=312)
    s.append(texto(W / 2, 34, "el techo es 38 con energía o sin ella",
                   color=SUAVE, tam=15))
    s.append(texto(W / 2, 520,
                   "(8, 2) es esquina de las dos, y la mejor de las dos",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_fig_dos_cimas():
    W, H = 720, 380
    ox, oy, ancho, alto = 80, 320, 560, 220
    s = [marco(
        W, H,
        "Una curva de una variable con dos cimas de altura distinta separadas "
        "por un valle; la cima izquierda es más baja que la derecha",
        "Una cima que no es la más alta",
        "Curva con dos maximos locales. El de la izquierda es mas bajo y esta "
        "marcado como optimo local; el de la derecha es el optimo global.",
    )]
    s.append(flecha(ox, oy, ox + ancho + 16, oy, color=SUAVE, marcador="s"))
    s.append(flecha(ox, oy, ox, oy - alto - 16, color=SUAVE, marcador="s"))
    s.append(texto(ox + ancho + 30, oy + 5, "plan", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(ox - 10, oy - alto - 24, "valor", color=SUAVE, tam=13, anclaje="middle"))

    import math
    # dos cimas: la izquierda en t=0.28 con altura 0.55, la derecha en t=0.78 con 1.0
    def f(t):
        a = 0.55 * math.exp(-((t - 0.28) / 0.13) ** 2)
        b = 1.00 * math.exp(-((t - 0.78) / 0.15) ** 2)
        return max(a, b) + 0.06

    pts = []
    n = 160
    for i in range(n + 1):
        t = i / n
        pts.append((ox + t * ancho, oy - f(t) * alto))
    d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
                 for i, (x, y) in enumerate(pts))
    s.append(f'<path d="{d}" fill="none" stroke="{SERIE[1]}" stroke-width="3"/>')

    for t, etiqueta, color in ((0.28, "óptimo local", ALARMA),
                               (0.78, "óptimo global", ACENTO)):
        x, y = ox + t * ancho, oy - f(t) * alto
        s.append(punto(x, y, r=7, color=color))
        s.append(linea(x, y, x, oy, color=color, grosor=1.5, guiones="4 4"))
        s.append(texto(x, y - 18, etiqueta, color=color, tam=13, peso="700"))
    s.append(texto(W / 2, 356,
                   "gana en su vecindario y pierde contra el resto",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def _corchete(x, arriba, abajo, hacia, color=SUAVE, grosor=2):
    """Corchete de matriz: una barra vertical con dos puntas.

    `hacia` es +1 para el izquierdo y -1 para el derecho.
    """
    p = 10 * hacia
    return (
        f'<path d="M {x + p} {arriba} L {x} {arriba} L {x} {abajo} L {x + p} {abajo}" '
        f'fill="none" stroke="{color}" stroke-width="{grosor}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def opt_fig_matriz():
    """El modelo escrito y la terna (c, A, b), con las dos maneras de recorrer A.

    Esquematico, no calculado: los numeros son los del episodio de dos piezas y
    van a mano porque lo que ensena el dibujo es la POSICION de cada uno.

    Las dos marcas —el segundo renglon y la primera columna— llevan recuadro
    con trazo distinto (continuo y punteado) y rotulo de texto, no solo color:
    quien no distingue el cian del ambar tiene que poder leer el diagrama
    igual. Se marca el SEGUNDO renglon a proposito; el primero es (1,1) y sus
    dos entradas iguales no ensenan nada sobre que dice recorrer un renglon.
    """
    W, H = 1020, 510
    s = [marco(
        W, H,
        "A la izquierda el modelo de la impresora escrito con desigualdades; a "
        "la derecha la misma informacion como la terna c, A, b, con el segundo "
        "renglon de A recuadrado y rotulado como el polimero y la primera "
        "columna recuadrada y rotulada como el filtro",
        "El modelo como terna (c, A, b)",
        "Dos bloques unidos por una flecha. El izquierdo tiene el modelo en "
        "forma canonica: max 4x1+3x2 sujeto a tres desigualdades de recurso y "
        "las dos de no negatividad. El derecho tiene c igual a (4,3), la "
        "matriz A de tres renglones y dos columnas, y la columna b con 10, 18 "
        "y 18. Un recuadro de trazo continuo marca el segundo renglon de A, "
        "que es el del polimero y compara piezas; otro de trazo punteado marca "
        "la primera columna, que es el filtro y arma una receta. Los dos se "
        "cruzan en la entrada A21, igual a 2, senalada con un circulo.",
    )]
    s.append(texto(W / 2, 40, "un renglón por recurso, una columna por pieza",
                   color=SUAVE, tam=16))

    # ---- el modelo escrito, a la izquierda
    s.append(texto(175, 86, "el modelo escrito", color=SUAVE, tam=14, peso="600"))
    s.append(caja(30, 104, 290, 238, borde=SUAVE, guiones="6 5"))
    # Cada parte lleva su propia x: <text> colapsa los espacios de sangria, asi
    # que alinear con espacios en una sola cadena no alinea nada.
    fx = 122
    filas = [
        (150, "max", "4x\u2081 + 3x\u2082", ACENTO),
        (198, "s.a.", "x\u2081 + x\u2082 \u2264 10", TEXTO),
        (230, "", "2x\u2081 + x\u2082 \u2264 18", TEXTO),
        (262, "", "x\u2081 + 2x\u2082 \u2264 18", TEXTO),
        (310, "", "x\u2081 \u2265 0, x\u2082 \u2265 0", SUAVE),
    ]
    for y, izq, der, color in filas:
        if izq:
            s.append(texto(fx - 16, y, izq, color=SUAVE, tam=15, anclaje="end",
                           fuente=MONO))
        s.append(texto(fx, y, der, color=color, tam=15, anclaje="start", fuente=MONO))

    s.append(texto(396, 222, "es exactamente", color=SUAVE, tam=12))
    s.append(flecha(358, 238, 434, 238))

    # ---- la terna, a la derecha
    s.append(texto(700, 86, "la terna (c, A, b)", color=SUAVE, tam=14, peso="600"))
    s.append(texto(706, 158, "c = (4, 3)", color=ACENTO, tam=19, fuente=MONO))

    ay, alto_celda = 212, 46
    ys = [ay + 23 + alto_celda * i + 6 for i in range(3)]      # linea base
    s.append(texto(706, 190, "A", color=SUAVE, tam=14, peso="600"))
    s.append(_corchete(636, 200, 362, +1))
    s.append(_corchete(776, 200, 362, -1))
    for i, renglon in enumerate([["1", "1"], ["2", "1"], ["1", "2"]]):
        for j, entrada in enumerate(renglon):
            s.append(texto(677 + 58 * j, ys[i], entrada, tam=19, fuente=MONO))

    s.append(texto(885, 190, "b", color=SUAVE, tam=14, peso="600"))
    s.append(_corchete(844, 200, 362, +1))
    s.append(_corchete(926, 200, 362, -1))
    for i, entrada in enumerate(["10", "18", "18"]):
        s.append(texto(885, ys[i], entrada, tam=19, fuente=MONO))

    # ---- las dos marcas: recuadro con trazo propio, y rotulo
    s.append(caja(648, 206, 58, 150, borde=SERIE[2], radio=8, grosor=2.5, guiones="7 5"))
    s.append(linea(677, 360, 677, 376, color=SERIE[2], guiones="4 4"))
    s.append(texto(677, 396, "columna 1 = el filtro", color=SERIE[2], tam=13))
    s.append(texto(677, 414, "arma una receta", color=SUAVE, tam=12))

    s.append(caja(642, 254, 128, 54, borde=SERIE[1], radio=8, grosor=2.5))
    s.append(texto(614, 275, "renglón 2 = el polímero", color=SERIE[1], tam=13,
                   anclaje="end"))
    s.append(texto(614, 294, "compara piezas", color=SUAVE, tam=12, anclaje="end"))

    s.append(f'<circle cx="677" cy="281" r="17" fill="none" stroke="{SUAVE}" '
             f'stroke-width="1.5"/>')
    s.append(texto(W / 2, 468,
                   "A\u2082\u2081 = 2 está en los dos recorridos: por eso la misma "
                   "tabla contesta las dos preguntas",
                   color=SUAVE, tam=14))
    s.append(cierre())
    return "".join(s)

# --------------------------------------------------------------------------
# el modelo con sello: tres piezas, y el poliedro que sale

A3 = [[1, 1, 1], [2, 1, 2], [1, 2, 3]]
B3 = [10, 18, 18]
C3 = [4, 3, 5]
NOMBRES3 = ["horas", "polímero", "energía"]


def _reducir(M, ncol):
    """Gauss-Jordan sobre fracciones. Devuelve (matriz reducida, columnas pivote)."""
    M = [fila[:] for fila in M]
    piv, r = [], 0
    for col in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        f = M[r][col]
        M[r] = [v / f for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                fa = M[i][col]
                M[i] = [a - fa * b for a, b in zip(M[i], M[r])]
        piv.append(col)
        r += 1
        if r == len(M):
            break
    return M, piv


def _rango(filas, n):
    if not filas:
        return 0
    return len(_reducir([[F(v) for v in f] for f in filas], n)[1])


def _resolver(filas, rhs, n):
    M, piv = _reducir([[F(v) for v in f] + [F(r)] for f, r in zip(filas, rhs)], n)
    if len(piv) != n:
        return None
    return tuple(M[i][n] for i in range(n))


def _sistema3():
    """Las seis restricciones: tres de recurso y tres de no negatividad.

    El indice es el mismo que usa la hoja canonica clase2.py y la guarda de
    tools/test_gen_optimizacion.py: 0 horas, 1 polimero, 2 energia, 3 x1>=0,
    4 x2>=0, 5 x3>=0. Las tres ultimas se escriben -x_k <= 0 para que todas
    apunten en el mismo sentido y su normal sea la exterior.
    """
    filas = [(A3[i], B3[i]) for i in range(3)]
    filas += [(tuple(-1 if j == k else 0 for j in range(3)), 0) for k in range(3)]
    return filas


def vertices_sello():
    """Los vertices del poliedro de tres piezas, en fracciones exactas.

    Mismo procedimiento que la pagina ensena y que vertices() hace en dos
    dimensiones: cruza las restricciones de tres en tres, tira los sistemas
    singulares, y se queda con los puntos que cumplen todo lo demas.
    """
    filas = _sistema3()
    V = []
    for idx in combinations(range(len(filas)), 3):
        x = _resolver([filas[i][0] for i in idx], [filas[i][1] for i in idx], 3)
        if x is None or any(v < 0 for v in x):
            continue
        if any(sum(a * xx for a, xx in zip(A3[i], x)) > B3[i] for i in range(3)):
            continue
        if x not in V:
            V.append(x)
    return sorted(V, key=lambda v: (-sum(c * xi for c, xi in zip(C3, v)), v))


def activas_sello(x):
    filas = _sistema3()
    return frozenset(i for i, (a, bb) in enumerate(filas)
                     if sum(ai * xi for ai, xi in zip(a, x)) == bb)


def aristas_sello(V):
    """Pares de vertices unidos por una arista, con las dos caras que la forman.

    Se decide por RANGO n-1, no contando activas compartidas: contar declara
    vecinos a los extremos de la diagonal de una cara. En este poliedro las dos
    reglas coinciden porque ningun vertice es degenerado, pero el dibujo se
    calcula con la buena.
    """
    filas = _sistema3()
    out = []
    for i, j in combinations(range(len(V)), 2):
        comp = activas_sello(V[i]) & activas_sello(V[j])
        if _rango([filas[k][0] for k in comp], 3) == 2:
            out.append((i, j, sorted(comp)))
    return out


def rotulo3(p):
    def n(t):
        return str(t) if t.denominator == 1 else f"{t.numerator}/{t.denominator}"
    return f"({n(p[0])}, {n(p[1])}, {n(p[2])})"


# Direccion de camara, elegida buscando la que mas separa los ocho vertices
# proyectados y los aleja de las aristas que no los tocan. Con ella x1 baja a la
# derecha, x3 baja a la izquierda y x2 sube: la vista de siempre de una caja, y
# el origen queda en el vertice de atras, que es justo el que menos
# importa ver.
CAMARA = (1.1, 1.8, 1.35)


def _camara():
    """Base ortonormal de la vista: (derecha, arriba, hacia el observador)."""
    import math
    n = [c / math.sqrt(sum(v * v for v in CAMARA)) for c in CAMARA]
    arriba = [0, 1, 0]                                  # x2 manda hacia arriba
    w = [arriba[i] - sum(arriba[j] * n[j] for j in range(3)) * n[i] for i in range(3)]
    largo = math.sqrt(sum(v * v for v in w))
    w = [c / largo for c in w]
    u = [w[1] * n[2] - w[2] * n[1],
         w[2] * n[0] - w[0] * n[2],
         w[0] * n[1] - w[1] * n[0]]
    return u, w, n


# Desplazamiento del rotulo de cada vertice, en pixeles, elegido a mano
# mirando el render en Chrome AMPLIADO: a tamano normal no se ve que un glifo
# este partido. El de (2,8,0) iba anclado a la derecha y la arista punteada de
# x2 —la vertical— le cortaba el parentesis de apertura; con anclaje "end" no
# hay corrimiento que lo salve, porque para despejar esa vertical el texto
# tendria que empezar mas a la derecha que el propio vertice.
ROTULOS3 = {
    (0, 0, 0): (-14, -14, "end"),
    (0, 0, 6): (-14, 6, "end"),
    (0, 9, 0): (16, 6, "start"),
    (2, 8, 0): (16, -8, "start"),
    (9, 0, 0): (16, 20, "start"),
}


def opt_fig_poliedro():
    """El poliedro de tres piezas en proyeccion, con sus ocho vertices.

    Calcula todo: los vertices con fracciones exactas, las doce aristas por
    rango, y cuales quedan escondidas. Una arista esta escondida si las dos
    caras que la forman miran para el otro lado; con esta camara son
    exactamente las tres que salen del origen, que es el vertice de atras.

    Los desplazamientos de rotulo estan a mano porque se ajustaron mirando el
    render en Chrome: la primera version ponia (0,9,0) encima del titulo y el
    nombre de la cara de energia encima del origen.
    """
    W, H = 940, 610
    OX, OY, ESC = 320, 320, 40
    u, w, n = _camara()
    V = vertices_sello()
    E = aristas_sello(V)
    filas = _sistema3()
    de_frente = [sum(filas[k][0][i] * n[i] for i in range(3)) > 0 for k in range(6)]

    def pantalla(p):
        f = [float(t) for t in p]
        return (OX + sum(f[i] * u[i] for i in range(3)) * ESC,
                OY - sum(f[i] * w[i] for i in range(3)) * ESC)

    P = [pantalla(v) for v in V]
    s = [marco(
        W, H,
        "El poliedro de tres piezas en proyección, con sus ocho vértices "
        "rotulados; el óptimo (5,2,3) marcado con un punto lleno y el plan de "
        "la clase 1, (8,2,0), con un anillo",
        "El poliedro de la impresora con sello",
        "Cuerpo de ocho vertices y doce aristas. Las tres caras de recurso "
        "—horas, polimero y energia— quedan de frente y estan sombreadas; las "
        "tres aristas que salen del origen quedan detras y van punteadas. Los "
        "ocho vertices son (0,0,0), (0,9,0), (0,0,6), (2,8,0), (9,0,0), "
        "(8,2,0), (9/2,0,9/2) y (5,2,3). El optimo (5,2,3) vale 41 y el plan "
        "de la clase 1, (8,2,0), vale 38.",
    )]
    s.append(texto(W / 2, 40, "ocho vértices y doce aristas: el terreno con tres piezas",
                   color=SUAVE, tam=16))

    # Las tres caras de recurso, sombreadas: dan volumen sin tapar nada. El
    # nombre va en el centroide mas un desplazamiento; el de la energia no
    # puede ir en su centroide porque ahi esta el origen.
    # El de la energia iba arriba a la izquierda y la arista (0,9,0)-(0,0,6)
    # le partia el glifo: se vio ampliando el render a 4x, no a tamano normal.
    # Baja a la parte ancha de la cara, entre (0,0,6) y (9/2,0,9/2).
    CORRIMIENTO = {0: (0, 0), 1: (0, 0), 2: (-33, 144)}
    for k in range(3):
        if not de_frente[k]:
            continue
        cara = [P[i] for i, v in enumerate(V) if k in activas_sello(v)]
        cx = sum(p[0] for p in cara) / len(cara)
        cy = sum(p[1] for p in cara) / len(cara)
        cara.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
                     for i, (x, y) in enumerate(cara)) + " Z"
        s.append(f'<path d="{d}" fill="{mezclar(SERIE[k], 0.17)}" stroke="none"/>')
        dx, dy = CORRIMIENTO[k]
        s.append(texto(cx + dx, cy + dy + 5, NOMBRES3[k], color=SERIE[k], tam=15,
                       peso="600"))

    for i, j_, caras in E:                      # primero las de atras
        if not any(de_frente[k] for k in caras):
            s.append(linea(P[i][0], P[i][1], P[j_][0], P[j_][1],
                           color=mezclar(SUAVE, 0.55), grosor=1.6, guiones="6 5"))
    for i, j_, caras in E:
        if any(de_frente[k] for k in caras):
            s.append(linea(P[i][0], P[i][1], P[j_][0], P[j_][1], color=SUAVE, grosor=2.4))

    # Los tres ejes coinciden con las tres aristas de atras, asi que se rotulan
    # sobre ellas en vez de dibujar flechas aparte.
    origen = pantalla((F(0), F(0), F(0)))
    for nombre, destino, corr in [("x\u2081 filtros", (9, 0, 0), (15, -26)),
                                  ("x\u2082 celdas", (0, 9, 0), (-78, 0)),
                                  ("x\u2083 sellos", (0, 0, 6), (20, 26))]:
        dx, dy = pantalla(tuple(F(t) for t in destino))
        mx = origen[0] + (dx - origen[0]) * 0.6 + corr[0]
        my = origen[1] + (dy - origen[1]) * 0.6 + corr[1]
        s.append(texto(mx, my, nombre, color=mezclar(SUAVE, 0.8), tam=12))

    mejor = max(range(len(V)), key=lambda i: sum(c * x for c, x in zip(C3, V[i])))
    clase1 = V.index((F(8), F(2), F(0)))
    for i, v in enumerate(V):
        x, y = P[i]
        if i == mejor:
            s.append(punto(x, y, r=9, color=ACENTO))
            s.append(texto(x - 30, y - 24, "(5, 2, 3) = 41", color=ACENTO, tam=14,
                           anclaje="end", peso="700"))
            s.append(texto(x - 30, y - 6, "el óptimo", color=SUAVE, tam=12,
                           anclaje="end"))
            continue
        if i == clase1:
            s.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{FONDO}" '
                     f'stroke="{TEXTO}" stroke-width="3"/>')
            s.append(texto(x + 18, y - 4, "(8, 2, 0) = 38", tam=14, anclaje="start",
                           peso="700"))
            s.append(texto(x + 18, y + 14, "el plan de la clase 1", color=SUAVE,
                           tam=12, anclaje="start"))
            continue
        s.append(punto(x, y, r=5, color=TEXTO))
        clave = tuple(int(t) for t in v) if all(t.denominator == 1 for t in v) else None
        dx, dy, anc = ROTULOS3.get(clave, (0, 34, "middle"))
        s.append(texto(x + dx, y + dy, rotulo3(v), color=SUAVE, tam=13, anclaje=anc))

    s += _leyenda(660, 78, [
        (SERIE[0], "x\u2081 + x\u2082 + x\u2083 \u2264 10   horas"),
        (SERIE[1], "2x\u2081 + x\u2082 + 2x\u2083 \u2264 18   polímero"),
        (SERIE[2], "x\u2081 + 2x\u2082 + 3x\u2083 \u2264 18   energía"),
    ], ancho=250)
    s.append(caja(660, 206, 250, 142, borde=SUAVE, guiones="6 5"))
    for k, renglon in enumerate([
        "la línea punteada pasa por detrás:",
        "son las tres aristas del origen,",
        "que es el vértice de atrás.",
        "",
        "la cara x\u2083 = 0 es el polígono",
        "de la clase 1, y aquí queda detrás.",
    ]):
        if renglon:
            s.append(texto(674, 232 + 19 * k, renglon, color=SUAVE, tam=13,
                           anclaje="start"))
    s.append(texto(W / 2, 578,
                   "en tres dimensiones un vértice es donde se cortan tres planos, "
                   "no dos",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


# Relleno del poligono en opt_fig_circulos. Es tambien el color de la placa
# que va debajo de cada rotulo de curva, y por eso vive fuera de la funcion.
FONDO_POLIGONO = mezclar(LINEA, 0.34)


def opt_fig_circulos():
    """El mismo poligono de la clase 1 con curvas de nivel CIRCULARES.

    Es el contraejemplo del teorema del vertice: maximizar
    -(x1-4)^2-(x2-4)^2 sobre la region factible da (4,4), que es estrictamente
    interior. El poligono sale de los parametros del episodio y el consumo de
    (4,4) se calcula, para que nada este escrito a mano.
    """
    W, H = 820, 560
    ox, oy, esc, top = 90, 470, 34, 10
    CENTRO = (4, 4)
    RADIOS = [4, 3, 2, 1]
    # Angulo (grados) del rotulo de cada curva. Va SOBRE su circunferencia,
    # que es lo unico que lo asocia sin ambiguedad —las curvas estan a 34 px
    # una de otra, asi que un rotulo despegado queda a la misma distancia de
    # dos—, y por eso lleva placa del color del poligono debajo: sin ella el
    # trazo discontinuo parte el glifo, y eso solo se ve ampliando el render.
    # Los cuatro angulos estan separados para que no se toquen las placas ni
    # la linea guia del punto interior.
    ROTULO_CURVA = {4: 225, 3: 115, 2: 310, 1: 240}
    V = vertices()
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    consumo = [sum(a * c for a, c in zip(fila, CENTRO)) for fila in A]
    s = [marco(
        W, H,
        "El polígono de la clase 1 con cuatro curvas de nivel circulares "
        "concéntricas alrededor de (4,4), que está marcado como punto interior",
        "Cuando las curvas de nivel se curvan",
        "El mismo poligono de cinco esquinas de la clase 1. Encima, cuatro "
        "circunferencias concentricas centradas en (4,4) con valores -16, -9, "
        "-4 y -1. El punto (4,4) esta marcado con un punto lleno y vale 0: es "
        "el maximo, queda estrictamente dentro de la region y no es ninguna de "
        "las cinco esquinas, que van dibujadas como aros huecos.",
    )]
    d = " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                 for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{d}" fill="{FONDO_POLIGONO}" '
             f'stroke="{mezclar(SUAVE, 0.75)}" stroke-width="2.5"/>')
    s += plano
    cx, cy = px(CENTRO[0]), py(CENTRO[1])
    for r in RADIOS:
        ultima = r == min(RADIOS)
        color = ACENTO if ultima else SERIE[1]
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * esc}" fill="none" '
                 f'stroke="{color}" stroke-width="{3 if ultima else 2}"'
                 + ("" if ultima else ' stroke-dasharray="8 6"') + "/>")
        ang = math.radians(ROTULO_CURVA[r])
        rx, ry = cx + math.cos(ang) * r * esc, cy - math.sin(ang) * r * esc
        etiqueta = f"\u2212{r * r}"
        ancho = 14 + len(etiqueta) * 9
        s.append(f'<rect x="{rx - ancho / 2:.1f}" y="{ry - 13:.1f}" '
                 f'width="{ancho}" height="18" rx="4" fill="{FONDO_POLIGONO}"/>')
        s.append(texto(rx, ry, etiqueta, color=color, tam=14,
                       peso="700" if ultima else "normal"))
    for p in V:
        s.append(f'<circle cx="{px(p[0])}" cy="{py(p[1])}" r="5" fill="{FONDO}" '
                 f'stroke="{TEXTO}" stroke-width="2.5"/>')
    # linea guia del punto interior hasta el texto de la derecha
    s.append(linea(cx + 12, cy - 6, 486, 246, color=mezclar(ACENTO, 0.7), grosor=1.5))
    s.append(punto(cx, cy, r=8, color=ACENTO))
    s.append(texto(W / 2, 34,
                   "objetivo \u2212(x\u2081\u22124)\u00b2 \u2212 "
                   "(x\u2082\u22124)\u00b2: las curvas de nivel se curvan",
                   color=SUAVE, tam=15))

    s.append(caja(478, 84, 306, 116, borde=SUAVE, guiones="6 5"))
    for k, renglon in enumerate([
        "en la clase 1 las curvas de nivel",
        "eran rectas paralelas: se desplazaban",
        "sin girar, y la última tocaba",
        "el polígono en una esquina.",
    ]):
        s.append(texto(494, 112 + 22 * k, renglon, color=SUAVE, tam=13,
                       anclaje="start"))
    s.append(texto(494, 250, "(4, 4) = 0, el máximo", color=ACENTO, tam=15,
                   anclaje="start", peso="700"))
    for k, renglon in enumerate([
        f"cabe: {consumo[0]} horas de {B[0]}, {consumo[1]} kg de {B[1]},",
        f"{consumo[2]} kWh de {B[2]}. Y le sobra de los tres,",
        "así que está estrictamente por dentro.",
        "",
        "ninguna de las cinco esquinas lo alcanza.",
    ]):
        if renglon:
            s.append(texto(494, 276 + 21 * k, renglon, color=SUAVE, tam=13,
                           anclaje="start"))
    s.append(texto(W / 2, 528,
                   "los círculos se encogen hasta cerrarse sobre un punto de "
                   "adentro: ahí no hay ninguna esquina",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


# Desplazamiento del rotulo de cada esquina en opt-camino-simplex, a mano y
# revisado renderizando AMPLIADO. Los rotulos llevan el valor, asi que miden
# casi 80 px: los dos de abajo van fuera del eje horizontal, y los tres de
# arriba lejos de las dos flechas del camino.
ROTULOS_CAMINO = {
    (0, 0): (12, 48, "start"),
    (9, 0): (0, 48, "middle"),
    (8, 2): (20, -14, "start"),
    (2, 8): (16, -16, "start"),
    (0, 9): (16, -16, "start"),
}


def opt_camino_simplex():
    """El camino que simplex recorre sobre el poligono de la clase 1.

    Calcula las cinco esquinas, la relacion de vecindad y la traza entera con
    la aritmetica exacta del episodio: si un precio o un disponible cambia, el
    camino dibujado cambia solo. No lleva las tres rectas de recurso —eso ya
    lo dibuja opt-poligono— porque aqui lo que se sigue son las flechas.
    """
    W, H = 820, 560
    ox, oy, esc, top = 90, 460, 34, 10
    V = vertices()
    ruta = camino_simplex()
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    s = [marco(
        W, H,
        "El polígono de la clase 1 con las cinco esquinas rotuladas con su "
        "valor y dos flechas que van del origen a (9,0) y de ahí a (8,2)",
        "El camino de simplex, de esquina en esquina",
        "El poligono de cinco esquinas de la clase 1. Las esquinas valen "
        "(0,0)=0, (9,0)=36, (8,2)=38, (2,8)=32 y (0,9)=27. Dos flechas "
        "gruesas marcan el camino: del origen a (9,0), primer pivote, y de "
        "(9,0) a (8,2), segundo pivote. Las tres esquinas visitadas van con "
        "punto lleno y las dos que nadie visito con aro hueco. En (8,2) los "
        "dos vecinos valen 36 y 32, los dos menos que 38, y ahi para.",
    )]
    d = " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                 for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{d}" fill="{mezclar(ACENTO, 0.18)}" '
             f'stroke="{mezclar(SUAVE, 0.7)}" stroke-width="2"/>')
    s += plano
    for k in range(len(ruta) - 1):
        a, b = ruta[k], ruta[k + 1]
        # La flecha arranca despues del punto de salida y termina antes del de
        # llegada: si va de centro a centro, la punta se mete dentro del aro
        # de la parada y se lee como si la atravesara.
        x1, y1, x2, y2 = px(a[0]), py(a[1]), px(b[0]), py(b[1])
        largo = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / largo, (y2 - y1) / largo
        fin = (15 if b == ruta[-1] else 6) + 4      # el aro de la parada es mayor
        s.append(flecha(x1 + ux * 10, y1 + uy * 10, x2 - ux * fin, y2 - uy * fin,
                        color=ACENTO, grosor=3))
    # Los dos rotulos de pivote van al lado de su flecha, no encima.
    s.append(texto((px(ruta[0][0]) + px(ruta[1][0])) / 2, py(0) - 14,
                   "pivote 1", color=ACENTO, tam=13, peso="700"))
    s.append(texto(px(ruta[1][0]) + 30, (py(ruta[1][1]) + py(ruta[2][1])) / 2 + 4,
                   "pivote 2", color=ACENTO, tam=13, anclaje="start", peso="700"))
    visitadas = set(ruta)
    for p in V:
        x, y = px(p[0]), py(p[1])
        dx, dy, anc = ROTULOS_CAMINO[(int(p[0]), int(p[1]))]
        parada = p == ruta[-1]
        if p in visitadas:
            s.append(punto(x, y, r=9 if parada else 6, color=ACENTO))
            if parada:
                s.append(f'<circle cx="{x}" cy="{y}" r="15" fill="none" '
                         f'stroke="{ACENTO}" stroke-width="2.5"/>')
        else:
            s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{FONDO}" '
                     f'stroke="{SUAVE}" stroke-width="2.5"/>')
        s.append(texto(x + dx, y + dy, f"{rotulo(p)} = {int(valor(p))}",
                       color=ACENTO if p in visitadas else SUAVE, tam=13,
                       anclaje=anc, peso="700" if parada else "normal"))
    s.append(texto(W / 2, 34,
                   "desde el origen: dos pivotes y tres esquinas de cinco",
                   color=SUAVE, tam=16))
    # Leyenda propia, con los dos simbolos que de verdad usa el dibujo: la
    # distincion es punto lleno contra aro hueco, no color, y una barra de
    # color no la ensenaria.
    s.append(caja(506, 66, 280, 78, relleno=mezclar(LINEA, 0.16), borde=SUAVE))
    s.append(punto(530, 96, r=6, color=ACENTO))
    s.append(texto(556, 101, "esquina visitada", color=TEXTO, tam=13,
                   anclaje="start"))
    s.append(f'<circle cx="530" cy="124" r="6" fill="{FONDO}" '
             f'stroke="{SUAVE}" stroke-width="2.5"/>')
    s.append(texto(556, 129, "esquina que nadie miró", color=TEXTO, tam=13,
                   anclaje="start"))
    s.append(caja(506, 190, 280, 132, borde=SUAVE, guiones="6 5"))
    for k, renglon in enumerate([
        "en (8, 2) los dos vecinos valen",
        "36 y 32: ninguno mejora, y ahí",
        "para el método.",
        "",
        "las dos esquinas huecas nunca",
        "se miraron, y ninguna ganaba.",
    ]):
        if renglon:
            s.append(texto(522, 216 + 19 * k, renglon, color=SUAVE, tam=13,
                           anclaje="start"))
    s.append(cierre())
    return "".join(s)


# Los dos paneles de opt-fig-vertice-o-arista, sobre el poligono de la clase 1:
# el objetivo de cada uno, los dos valores de nivel que se dibujan punteados, y
# el pie del panel. Los vertices OPTIMOS y el valor que alcanzan no se escriben
# aqui: se calculan desde el objetivo, que es lo que impide que el dibujo
# contradiga a la pagina si un parametro del episodio cambia.
# Es una FUNCION y no una constante de modulo a proposito. Como constante se
# evalua al importar, y entonces `tuple(C)` y un `(4, 3)` escrito a mano son
# indistinguibles para cualquier prueba: la que lo intentaba era tautologica.
# Leyendo C al llamarse, una guarda puede cambiar el objetivo del episodio y
# exigir que el panel izquierdo lo siga.
def paneles_vertice_o_arista():
    """Los dos paneles de opt-fig-vertice-o-arista: objetivo, niveles, pie.

    El de la izquierda es el objetivo del episodio, leido de C y no copiado. El
    de la derecha es «la celda a 4» que la clase 1 ya uso para el empate: paga
    lo mismo por las dos piezas, asi que su recta de nivel es paralela al
    renglon de las horas —A[0] = [1, 1]— y toda esa arista empata.
    """
    return (
        (tuple(C), (20, 30), "toca en un solo vértice"),
        ((C[0], C[0]), (24, 32), "queda paralela a un lado"),
    )

# Desplazamiento del rotulo de cada vertice optimo de opt-fig-vertice-o-arista,
# a mano y revisado renderizando AMPLIADO. Los dos van arriba a la derecha
# porque es el unico cuadrante libre en los dos paneles: la recta de nivel sale
# de cada punto hacia arriba a la izquierda, y hacia abajo se va a la derecha,
# que es justo donde un rotulo anclado abajo la encontraria.
ROTULOS_VERTICE_O_ARISTA = {
    (8, 2): (16, -14, "start"),
    (2, 8): (14, -18, "start"),
}


def desplazamiento_vertice_o_arista(p):
    """El desplazamiento del rotulo de p, o un error que dice que hacer.

    Un KeyError pelado aqui revienta el generador desde el fixture de la
    prueba y arrastra todo el archivo a ERROR, que es la peor manera de
    enterarse. Esto falla igual, pero diciendo por que y donde se arregla.
    """
    clave = (int(p[0]), int(p[1]))
    if clave not in ROTULOS_VERTICE_O_ARISTA:
        raise ValueError(
            f"{rotulo(p)} gana en un panel de opt-fig-vertice-o-arista y no "
            "tiene entrada en ROTULOS_VERTICE_O_ARISTA. Los desplazamientos "
            "se eligen a mano mirando el render AMPLIADO a 4x: elige uno, "
            "declaralo ahi, y comprueba que ningun trazo parte el rotulo."
        )
    return ROTULOS_VERTICE_O_ARISTA[clave]


def optimos_con(c):
    """Los vertices del poligono de la clase 1 que maximizan c, y su valor.

    Devuelve los ganadores en el orden del poligono, asi que con c = (4, 4)
    salen (8, 2) y (2, 8) —los dos extremos de la arista de las horas— y no una
    pareja cualquiera.
    """
    V = vertices()

    def z(p):
        return c[0] * p[0] + c[1] * p[1]

    mejor = max(z(p) for p in V)
    return V, mejor, [p for p in V if z(p) == mejor]


def pie_vertice_o_arista(z, ganadores):
    """El pie de cada panel, redactado desde lo que el calculo devolvio."""
    if len(ganadores) == 1:
        return f"la recta de {z} toca solo en {rotulo(ganadores[0])}"
    a, b = ganadores
    return f"toda la arista de {rotulo(a)} a {rotulo(b)} vale {z}"


def opt_fig_vertice_o_arista():
    """Los dos desenlaces del teorema del vertice, sobre el mismo poligono.

    Izquierda, c = (4, 3): la ultima recta de nivel toca en un solo vertice.
    Derecha, c = (4, 4): queda paralela al lado de las horas, y toda esa arista
    empata —con sus dos extremos, que son vertices—. Es el caso que la pagina
    llama «al menos uno».

    Los dos casos se distinguen sin color: a la izquierda hay un punto sobre la
    recta, a la derecha una banda gruesa con un punto en cada extremo.
    """
    W, H = 720, 470
    esc, top, oy = 27, 10, 400
    s = [marco(
        W, H,
        "Dos paneles sobre el mismo polígono: a la izquierda la última recta "
        "de nivel toca la región en un solo vértice; a la derecha queda "
        "paralela a un lado y toda esa arista empata",
        "O toca en un vértice, o cae en una arista entera",
        "Panel izquierdo, objetivo (4, 3): la recta de valor 38 toca el "
        "poligono solo en (8, 2). Panel derecho, objetivo (4, 4): la recta de "
        "valor 40 se apoya en el lado que va de (8, 2) a (2, 8); toda esa "
        "arista vale 40, y sus dos extremos son vertices.",
    )]
    for k, (c, niveles, subtitulo) in enumerate(paneles_vertice_o_arista()):
        ox = 58 + 345 * k
        centro = ox + esc * top / 2
        V, z, ganadores = optimos_con(c)
        px, py, plano = _plano(W, H, ox, oy, esc, top)
        d = " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                     for i, p in enumerate(V)) + " Z"
        s.append(f'<path d="{d}" fill="{mezclar(ACENTO, 0.20)}" '
                 f'stroke="{mezclar(ACENTO, 0.85)}" stroke-width="2.5"/>')
        s += plano
        for v in niveles:
            extremos = _corte(c[0], c[1], v, top)
            if len(extremos) == 2:
                (x1, y1), (x2, y2) = extremos
                s.append(linea(px(x1), py(y1), px(x2), py(y2), color=SUAVE,
                               grosor=1.8, guiones="7 6"))
        # la arista ganadora va debajo de la recta de nivel: la recta la
        # atraviesa entera y se ve que el empate es el lado, no dos puntos
        if len(ganadores) == 2:
            a, b = ganadores
            s.append(linea(px(a[0]), py(a[1]), px(b[0]), py(b[1]),
                           color=ACENTO, grosor=9))
        (x1, y1), (x2, y2) = _corte(c[0], c[1], z, top)
        s.append(linea(px(x1), py(y1), px(x2), py(y2), color=SERIE[1], grosor=3.2))
        for p in ganadores:
            dx, dy, anc = desplazamiento_vertice_o_arista(p)
            s.append(punto(px(p[0]), py(p[1]), r=8))
            s.append(texto(px(p[0]) + dx, py(p[1]) + dy, rotulo(p),
                           color=ACENTO, tam=13, anclaje=anc, peso="700"))
        s.append(texto(centro, 32, f"c = ({c[0]}, {c[1]})", color=TEXTO, tam=16,
                       peso="700", fuente=MONO))
        s.append(texto(centro, 56, subtitulo, color=SUAVE, tam=14))
        s.append(texto(centro, 448, pie_vertice_o_arista(z, ganadores),
                       color=TEXTO, tam=13))
    s.append(cierre())
    return "".join(s)


# Las tres posiciones de la recta de las horas que dibuja opt-fig-precio-sombra,
# y el desplazamiento del rotulo de cada optimo, a mano y revisado renderizando
# AMPLIADO. Los rotulos llevan el valor, asi que miden casi 80 px: los tres van
# a la derecha de su punto, que es el unico lado libre. A la izquierda pasan las
# tres rectas de horas, y encima la de la energia.
HORAS = (10, 11, 12)
GUIONES_HORAS = (None, "9 6", "3 4")
ROTULOS_HORAS = {
    (8, 2): (18, 12, "start"),
    (7, 4): (18, 14, "start"),
    (6, 6): (22, -22, "start"),
}


def optimo_con_horas(h):
    """El mejor plan cuando hay h horas de impresora, con el resto igual.

    Se calcula, no se transcribe: recorta la region con [h, 18, 18] y se queda
    con el vertice que mas paga. Con h = 12 esa region tiene cuatro esquinas en
    vez de cinco, porque la recta de las horas, la del polimero y la de la
    energia pasan las tres por (6, 6).
    """
    return max(_region(A, [h, B[1], B[2]]), key=valor)


def opt_fig_precio_sombra():
    """Que compra una hora mas: el optimo corre por la arista del polimero.

    Calcula las dos regiones y los tres optimos desde los parametros del
    episodio. Los tres puntos caen sobre 2x1 + x2 = 18 —la arista del
    polimero— y el ultimo, (6, 6), es donde las tres rectas de recurso se
    juntan: ahi la energia deja de sobrar y la hora siguiente ya no compra
    nada.

    Cada recta de horas se dibuja SOLO hasta su optimo, y no cruzando toda la
    ventana como en opt-poligono. No es adorno: las tres son paralelas y quedan
    a 24 px una de otra, asi que con las tres enteras no hay un solo hueco a la
    derecha de los puntos donde quepa un rotulo de 80 px sin que un trazo lo
    parta. Ademas el corte cae justo donde el dibujo quiere que mires: donde la
    recta de las horas se encuentra con la del polimero. Quien identifica cada
    recta es la leyenda, con su trazo.
    """
    W, H = 880, 600
    ox, oy, esc, top = 90, 490, 34, 10
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    chica = _region(A, [HORAS[0], B[1], B[2]])
    grande = _region(A, [HORAS[-1], B[1], B[2]])
    optimos = [optimo_con_horas(h) for h in HORAS]
    s = [marco(
        W, H,
        "El polígono de la clase 1 con la recta de las horas en tres "
        "posiciones, 10, 11 y 12; el mejor plan corre por la arista del "
        "polímero de (8,2) a (7,4) y a (6,6), donde las tres rectas de recurso "
        "se juntan",
        "Qué compra una hora más de impresora",
        "Con 10 horas la region factible tiene cinco esquinas y el mejor plan "
        "es (8, 2), que vale 38 creditos. Al subir las horas a 11 y a 12 la "
        "region crece y el mejor plan se corre por la arista del polimero a "
        "(7, 4) con 40 y a (6, 6) con 42. En (6, 6) coinciden la recta de las "
        "horas, la del polimero y la de la energia: los tres recursos se "
        "acaban exactos y una hora mas ya no compra nada.",
    )]
    trazo = lambda V: " ".join(("M" if i == 0 else "L") + f" {px(p[0]):.1f} {py(p[1]):.1f}"
                               for i, p in enumerate(V)) + " Z"
    s.append(f'<path d="{trazo(grande)}" fill="{mezclar(ACENTO, 0.20)}" stroke="none"/>')
    s.append(f'<path d="{trazo(chica)}" fill="{mezclar(ACENTO, 0.34)}" stroke="none"/>')
    s += plano
    # las dos rectas que no se mueven, enteras
    for k in (1, 2):
        (x1, y1), (x2, y2) = _corte(A[k][0], A[k][1], B[k], top)
        s.append(linea(px(x1), py(y1), px(x2), py(y2), color=SERIE[k], grosor=2.5))
    # y las tres posiciones de la que si, cada una hasta su optimo
    for h, guiones, mejor in zip(HORAS, GUIONES_HORAS, optimos):
        alto = max(_corte(A[0][0], A[0][1], h, top), key=lambda t: t[1])
        s.append(linea(px(alto[0]), py(alto[1]), px(mejor[0]), py(mejor[1]),
                       color=SERIE[0], grosor=2.5, guiones=guiones))
    # el optimo corriendo por la arista: las flechas van ENCIMA de la recta del
    # polimero, no paralelas a ella. Paralelas y desplazadas quedaban cruzando
    # las dos rectas de horas punteadas, y el ojo no sabia por donde corre el
    # optimo; encima, el tramo (8,2)-(6,6) se lee como lo que es -- un tramo de
    # esa arista--, y la recta sigue a la vista antes y despues
    for a, b in zip(optimos, optimos[1:]):
        x1, y1, x2, y2 = px(a[0]), py(a[1]), px(b[0]), py(b[1])
        largo = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / largo, (y2 - y1) / largo
        s.append(flecha(x1 + ux * 12, y1 + uy * 12, x2 - ux * 16, y2 - uy * 16,
                        color=ACENTO, grosor=3.5))
    for k, p in enumerate(optimos):
        x, y = px(p[0]), py(p[1])
        ultimo = k == len(optimos) - 1
        # el punto de (6,6) NO va mas gordo que los otros dos: con r = 9 tapaba
        # justo lo que el dibujo tiene que ensenar, que es que las tres rectas
        # pasan por ahi. Lo que lo destaca es el aro, que no tapa nada.
        s.append(punto(x, y, r=6))
        if ultimo:
            s.append(f'<circle cx="{x}" cy="{y}" r="15" fill="none" '
                     f'stroke="{ACENTO}" stroke-width="2.5"/>')
        dx, dy, anc = ROTULOS_HORAS[(int(p[0]), int(p[1]))]
        s.append(texto(x + dx, y + dy, f"{rotulo(p)} = {int(valor(p))}", color=ACENTO,
                       tam=13, anclaje=anc, peso="700" if ultimo else "normal"))
    s.append(texto(px(optimos[-1][0]) + 22, py(optimos[-1][1]) - 4,
                   "tres rectas, un punto", color=ACENTO, tam=12, anclaje="start"))
    # Leyenda propia: las tres posiciones de la recta de horas son del mismo
    # color, asi que lo que las distingue es el trazo, y la barra solida de
    # _leyenda no lo ensenaria. Lleva una fila por recta —tambien las dos
    # dibujadas a guiones— porque ninguna va rotulada dentro del dibujo.
    # Las tres filas de horas salen de HORAS y de GUIONES_HORAS, no de literales:
    # la leyenda es lo unico que identifica esas tres rectas, y con el trazo y
    # el numero escritos a mano se desincronizan de la recta sin que nada lo
    # note. Aqui ya paso: la fila de 12 decia "3 5" y la recta iba a "3 4".
    filas = [
        (SERIE[1], None, "2x\u2081 + x\u2082 \u2264 18   polímero"),
        (SERIE[2], None, "x\u2081 + 2x\u2082 \u2264 18   energía"),
    ] + [
        (SERIE[0], GUIONES_HORAS[k],
         f"x\u2081 + x\u2082 \u2264 {h}   {glosa}")
        for k, (h, glosa) in enumerate(zip(
            HORAS, ("las horas de hoy", "con una hora más", "con dos horas más")))
    ]
    s.append(caja(500, 96, 348, 26 + 30 * len(filas),
                  relleno=mezclar(LINEA, 0.16), borde=SUAVE))
    for k, (color, guiones, etiqueta) in enumerate(filas):
        yy = 126 + 30 * k
        s.append(linea(516, yy, 552, yy, color=color, grosor=3, guiones=guiones))
        s.append(texto(566, yy + 5, etiqueta, tam=13, anclaje="start"))
    s.append(caja(500, 292, 348, 190, borde=SUAVE, guiones="6 5"))
    for k, renglon in enumerate([
        "cada hora más corre el óptimo por la",
        "misma arista, la del polímero, y paga",
        "2 créditos más: 38, 40, 42.",
        "",
        "en 12 el óptimo es (6, 6), y ahí se",
        "juntan las tres rectas: la energía se",
        "acaba también, y la hora siguiente ya",
        "no compra nada.",
    ]):
        if renglon:
            s.append(texto(520, 320 + 21 * k, renglon, color=SUAVE, tam=13,
                           anclaje="start"))
    s.append(texto(W / 2, 40, "una hora más corre el óptimo por la misma arista",
                   color=SUAVE, tam=16))
    s.append(texto(260, 556,
                   "de 10 a 12 cada hora paga 2 créditos; de 12 en adelante, ninguno",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


DIAGRAMAS = {
    "opt-la-impresora": opt_la_impresora,
    "opt-anatomia": opt_anatomia,
    "opt-lienzo": opt_lienzo,
    "opt-historia-a-modelo": opt_historia_a_modelo,
    "opt-poligono": opt_poligono,
    "opt-curvas-de-nivel": opt_curvas_de_nivel,
    "opt-sin-energia": opt_sin_energia,
    "opt-fig-dos-cimas": opt_fig_dos_cimas,
    "opt-fig-matriz": opt_fig_matriz,
    "opt-fig-poliedro": opt_fig_poliedro,
    "opt-fig-circulos": opt_fig_circulos,
    "opt-camino-simplex": opt_camino_simplex,
    "opt-fig-precio-sombra": opt_fig_precio_sombra,
    "opt-fig-vertice-o-arista": opt_fig_vertice_o_arista,
}


def escribir(nombre):
    ASSETS.mkdir(parents=True, exist_ok=True)
    destino = ASSETS / f"{nombre}.svg"
    destino.write_text(DIAGRAMAS[nombre](), encoding="utf-8")
    return destino


def main(argv):
    nombres = argv[1:] or list(DIAGRAMAS)
    for nombre in nombres:
        if nombre not in DIAGRAMAS:
            raise SystemExit(f"diagrama desconocido: {nombre}")
        print(escribir(nombre))


if __name__ == "__main__":
    main(sys.argv)
