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


# --------------------------------------------------------------------------
# Clase 3 - el reactor. Cinco diagramas.
#
# Los cinco CALCULAN lo que dibujan: la curva de rendimiento, sus curvas de
# nivel, la descomposicion del gradiente y las trayectorias del descenso salen
# de los mismos numeros que verifica
# docs/superpowers/verificacion-optimizacion/clase3.py. Si un parametro del
# reactor cambia, el dibujo cambia solo.

# El episodio del reactor: rendimiento u_i(p) = b_i p - p^2/2.
B_REACTOR = (6, 8, 10)
P_TOTAL = 15


def _u(p, b=8):
    return b * p - p * p / 2


def _flechac(x1, y1, x2, y2, color, ident, grosor=3):
    """Flecha cuya PUNTA lleva el color de su linea.

    flecha() apunta a los dos marcadores de marco(), que son magenta y gris:
    una flecha verde salia con punta magenta. Se vio renderizando, no leyendo
    el XML. Cada llamada emite su propio marcador, asi que `ident` tiene que
    ser unico dentro del archivo.
    """
    return (
        f'<defs><marker id="{ident}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker></defs>'
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{grosor}" marker-end="url(#{ident})"/>'
    )


def _ejes(ox, oy, ancho, alto, etx, ety):
    """Los dos ejes con punta y sus rotulos, en el gris del skin."""
    return [
        flecha(ox, oy, ox + ancho + 16, oy, color=SUAVE, marcador="s"),
        flecha(ox, oy, ox, oy - alto - 16, color=SUAVE, marcador="s"),
        texto(ox + ancho + 26, oy + 5, etx, color=SUAVE, tam=13, anclaje="start"),
        texto(ox - 4, oy - alto - 26, ety, color=SUAVE, tam=13, anclaje="start"),
    ]


def _curva(puntos, color, grosor=3, guiones=None):
    d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
                 for i, (x, y) in enumerate(puntos))
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}" '
            f'stroke-linejoin="round"{trazo}/>')


def _trozos(puntos, dentro):
    """Parte una lista de puntos en los tramos que caen dentro del cuadro.

    Recortar muestreando en vez de con <clipPath> porque un SVG suelto se abre
    en visores que no siempre lo respetan, y estas figuras se miran tambien
    fuera del sitio.
    """
    salida, actual = [], []
    for p in puntos:
        if dentro(*p):
            actual.append(p)
        elif actual:
            salida.append(actual)
            actual = []
    if actual:
        salida.append(actual)
    return [t for t in salida if len(t) > 1]


def opt_cuerda():
    """La prueba de la cuerda sobre el rendimiento real de un sistema.

    La curva es u(p) = 8p - p^2/2, el sistema de motores del episodio. La
    cuerda va de p=2 a p=7 y en su punto medio la curva saca 3.125 de ventaja:
    ese hueco es la concavidad, y esta calculado, no dibujado a ojo.
    """
    W, H = 840, 470
    ox, oy, ancho, alto = 100, 380, 620, 290
    pmax, umax = 10.5, 34.0
    X = lambda p: ox + p / pmax * ancho
    Y = lambda u: oy - u / umax * alto

    s = [marco(
        W, H,
        "La curva de rendimiento de un sistema con una cuerda trazada entre dos "
        "de sus puntos; la cuerda queda por debajo de la curva en todo el tramo",
        "La prueba de la cuerda",
        "Curva concava u(p) = 8p - p cuadrado medios. Entre p=2 y p=7 se traza "
        "una cuerda recta que queda por debajo de la curva; en el punto medio "
        "p=4.5 la curva vale 25.875 y la cuerda 22.75.",
    )]
    s += _ejes(ox, oy, ancho, alto, "potencia p", "rendimiento u(p)")

    s.append(_curva([(X(i / 20), Y(_u(i / 20))) for i in range(0, int(pmax * 20) + 1)],
                    SERIE[1]))

    a, c = 2.0, 7.0
    s.append(linea(X(a), Y(_u(a)), X(c), Y(_u(c)), color=ACENTO, grosor=3))
    for t in (a, c):
        s.append(punto(X(t), Y(_u(t)), r=6, color=ACENTO))
        s.append(linea(X(t), Y(_u(t)), X(t), oy, color=SUAVE, grosor=1.5, guiones="4 4"))
        s.append(texto(X(t), oy + 24, f"p = {t:.0f}", color=SUAVE, tam=13))

    m = (a + c) / 2
    ucurva, ucuerda = _u(m), (_u(a) + _u(c)) / 2
    s.append(linea(X(m), Y(ucurva), X(m), Y(ucuerda), color=SERIE[0], grosor=3))
    s.append(punto(X(m), Y(ucurva), r=5, color=SERIE[0]))
    s.append(punto(X(m), Y(ucuerda), r=5, color=SERIE[0]))
    # los tres numeros van juntos en el hueco de abajo a la derecha: puestos
    # junto a sus trazos se montaban encima de la curva y de la cuerda.
    for i, (etiqueta, color) in enumerate((
        (f"la curva en p = {m:g}:  {ucurva:g}", SERIE[1]),
        (f"la cuerda en p = {m:g}:  {ucuerda:g}", ACENTO),
        (f"ventaja de la curva:  {ucurva - ucuerda:g}", SERIE[0]),
    )):
        s.append(texto(X(7.5), Y(13) + i * 24, etiqueta, color=color, tam=14,
                       anclaje="start", peso="700" if i == 2 else "normal"))
    s.append(texto(W / 2, H - 16,
                   "repartir la potencia entre dos puntos rinde menos que ponerla en medio",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_concava_convexa():
    """La misma curva y su reflejo: maximizar una es minimizar la otra.

    Los dos paneles comparten orientacion —eje vertical hacia arriba, cero en
    la misma altura— para que el reflejo se lea como reflejo. La primera
    version puso el eje del panel derecho apuntando hacia abajo y parecia otra
    convencion en vez de la misma funcion cambiada de signo.
    """
    W, H = 980, 470
    ancho, alto = 340, 150
    pmax, umax = 10.5, 34.0
    s = [marco(
        W, H,
        "Dos paneles con la misma curva reflejada: a la izquierda una funcion "
        "concava con su maximo senalado, a la derecha su negativo, una funcion "
        "convexa con su minimo en la misma potencia",
        "Cóncava y convexa son el mismo problema",
        "Panel izquierdo: u(p) concava, maximo en p=8 con valor 32. Panel "
        "derecho: menos u(p) convexa, minimo en p=8 con valor menos 32. La "
        "potencia optima es la misma en los dos.",
    )]

    cero = 230          # la altura del cero, identica en los dos paneles
    for ox, signo, titulo, color, etiqueta in (
        (80, +1, "u es cóncava — se maximiza", SERIE[1], "máximo"),
        (560, -1, "−u es convexa — se minimiza", SERIE[2], "mínimo"),
    ):
        X = lambda p, ox=ox: ox + p / pmax * ancho
        Y = lambda u, signo=signo: cero - signo * u / umax * alto
        s.append(texto(ox + ancho / 2, 56, titulo, color=TEXTO, tam=15, peso="700"))
        s.append(flecha(ox, cero + 170, ox, cero - 170, color=SUAVE, marcador="s"))
        s.append(linea(ox, cero, ox + ancho + 14, cero, color=SUAVE, grosor=1.5))
        s.append(texto(ox - 12, cero + 5, "0", color=SUAVE, tam=13, anclaje="end"))
        s.append(texto(ox + ancho + 20, cero + 5, "p", color=SUAVE, tam=13, anclaje="start"))
        s.append(_curva([(X(i / 20), Y(_u(i / 20))) for i in range(0, int(pmax * 20) + 1)],
                        color))
        s.append(punto(X(8), Y(_u(8)), r=7, color=ACENTO))
        s.append(linea(X(8), Y(_u(8)), X(8), cero, color=ACENTO, grosor=1.5, guiones="4 4"))
        cifra = "32" if signo > 0 else "−32"      # menos tipografico, no guion
        s.append(texto(X(8) + 14, Y(_u(8)) - signo * 14 + 5,
                       f"{etiqueta}: {cifra}", color=ACENTO, tam=14,
                       peso="700", anclaje="start"))
        s.append(texto(X(8), cero + (22 if signo > 0 else -12), "p = 8", color=SUAVE, tam=13))
    s.append(texto(W / 2, H - 16,
                   "la misma potencia resuelve los dos: cambiar de signo cambia la pregunta, no la respuesta",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_tangencia():
    """Curvas de nivel del reactor de dos sistemas, la recta, y los gradientes.

    Con dos sistemas (b = 6 y 8) y potencia 8 el optimo es (3,5) y lambda vale
    3: el MISMO lambda que el reactor de tres sistemas con potencia 15, elegido
    asi para que el dibujo ensene el numero que la pagina calcula.

    Las curvas de nivel son circunferencias centradas en (6,8) porque
    f(p) = 50 - ((p1-6)^2 + (p2-8)^2)/2. Las dos flechas del optimo son
    paralelas por definicion, asi que la de la restriccion va desplazada en
    perpendicular: dibujadas una encima de otra solo se veia la larga.
    """
    import math
    W, H = 780, 690
    ox, oy, lado = 95, 560, 470
    k = lado / 9.6
    X = lambda p: ox + p * k
    Y = lambda p: oy - p * k
    dentro = lambda p1, p2: -0.05 <= p1 <= 9.5 and -0.05 <= p2 <= 9.5

    s = [marco(
        W, H,
        "Curvas de nivel circulares del rendimiento, la recta que fija la "
        "potencia total, y en el punto donde la recta toca la curva de nivel "
        "mas alta, dos flechas que apuntan en la misma direccion",
        "Tangencia: los dos gradientes se alinean",
        "Circunferencias centradas en (6,8) cortadas por la recta p1+p2=8. En "
        "(3,5) la recta es tangente a una de ellas y el gradiente del objetivo, "
        "(3,3), es multiplo del de la restriccion, (1,1). En (6,2) las dos "
        "flechas apuntan distinto y todavia se puede mejorar.",
    )]
    s += _ejes(ox, oy, lado, lado, "p₁ escudos", "p₂ motores")

    for r, papel in ((1.6, "alta"), (3.0, "alta"), (math.sqrt(18), "toca"), (5.6, "cruza")):
        puntos = []
        for i in range(721):
            th = math.radians(i / 2)
            puntos.append((6 + r * math.cos(th), 8 + r * math.sin(th)))
        color = SERIE[1] if papel == "toca" else mezclar(SERIE[1], 0.45)
        for t in _trozos(puntos, dentro):
            s.append(_curva([(X(p1), Y(p2)) for p1, p2 in t], color,
                            grosor=3 if papel == "toca" else 2))

    s.append(punto(X(6), Y(8), r=4, color=mezclar(SERIE[1], 0.7)))
    s.append(texto(X(6) + 12, Y(8) - 12, "sin límite se iría aquí",
                   color=mezclar(SERIE[1], 0.85), tam=12, anclaje="start"))
    # Las circunferencias son curvas de nivel de f, y la recta es h. El dibujo
    # nombraba ∇h sin que h apareciera en ninguna parte.
    s.append(texto(X(0.5), Y(3.1), "curvas de nivel de f",
                   color=mezclar(SERIE[1], 0.9), tam=13, anclaje="start"))
    s.append(linea(X(0), Y(8), X(8), Y(0), color=ACENTO, grosor=3))
    # El rotulo de h va ROTADO sobre la recta. Horizontal la cruzaba: cualquier
    # texto horizontal cerca de una recta diagonal termina encima de ella.
    lx, ly = X(1.6) - 13, Y(6.4) + 13   # tramo alto de la recta, que está vacío
    s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{ACENTO}" '
             f'font-family="{FUENTE}" font-size="14" font-weight="700" '
             f'text-anchor="middle" transform="rotate(45 {lx:.1f} {ly:.1f})">'
             f'h(p) = p₁ + p₂ = 8</text>')

    # el optimo: las dos flechas, la de la restriccion desplazada en perpendicular
    px, py = X(3), Y(5)
    s.append(punto(px, py, r=7, color=TEXTO))
    s.append(texto(px - 16, py + 6, "(3, 5)", color=TEXTO, tam=15, peso="700", anclaje="end"))
    s.append(_flechac(px, py, px + 3 * 22, py - 3 * 22, SERIE[0], "gf1"))
    dx, dy = 13, 13      # desplazamiento perpendicular, hacia abajo-derecha
    s.append(_flechac(px + dx, py + dy, px + dx + 42, py + dy - 42, SERIE[2], "gh1"))
    s.append(texto(px + 76, py - 74, "∇f = (3,3)", color=SERIE[0], tam=14,
                   anclaje="start", peso="700"))
    s.append(texto(px + 76, py - 54, "= 3 × ∇h", color=SERIE[0], tam=13, anclaje="start"))
    s.append(texto(px + 66, py + 26, "∇h = (1,1)", color=SERIE[2], tam=13, anclaje="start"))
    # Angulo recto entre la recta y ∇h: es la razon por la que el gradiente de la
    # restriccion se dibuja saliendo de la recta y no a lo largo de ella.
    import math as _m
    lado_recta = (1 / _m.sqrt(2), 1 / _m.sqrt(2))     # (1,-1) en pantalla baja
    lado_grad = (1 / _m.sqrt(2), -1 / _m.sqrt(2))     # (1,1) en pantalla sube
    a = 15
    esquinas = [(px + lado_recta[0] * a, py + lado_recta[1] * a),
                (px + (lado_recta[0] + lado_grad[0]) * a,
                 py + (lado_recta[1] + lado_grad[1]) * a),
                (px + lado_grad[0] * a, py + lado_grad[1] * a)]
    d = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
                 for i, (x, y) in enumerate(esquinas))
    s.append(f'<path d="{d}" fill="none" stroke="{SUAVE}" stroke-width="1.5"/>')

    # un punto factible peor, donde las dos flechas NO son multiplos
    qx, qy = X(6), Y(2)
    s.append(punto(qx, qy, r=6, color=SUAVE))
    s.append(_flechac(qx, qy, qx, qy - 6 * 11, SERIE[0], "gf2", grosor=2.5))
    s.append(_flechac(qx + 10, qy + 10, qx + 10 + 34, qy + 10 - 34, SERIE[2], "gh2", grosor=2.5))
    s.append(texto(qx - 12, qy - 70, "∇f = (0,6)", color=SERIE[0], tam=13, anclaje="end"))
    s.append(texto(qx - 12, qy + 24, "(6, 2): todavía mejora", color=SUAVE, tam=13,
                   anclaje="end"))

    s.append(texto(W / 2, H - 38,
                   "∇h sale de la recta en ángulo recto: caminar por la recta no cambia h",
                   color=SUAVE, tam=13))
    s.append(texto(W / 2, H - 16,
                   "la curva de nivel que solo la toca una vez es la mejor alcanzable: ahí se alinean",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_normales():
    """De donde sale el signo: ∇f como suma de las normales activas.

    Sobre el poligono de la clase 1, en su optimo (8,2), el gradiente del
    objetivo c = (4,3) se escribe como 2·(1,1) + 1·(2,1): las normales
    exteriores de las dos restricciones activas, con coeficientes 2 y 1, que
    son EXACTAMENTE los precios sombra que la clase 2 calculo. El dibujo es la
    estacionariedad de KKT, y los coeficientes no pueden ser negativos sin que
    la flecha apunte hacia dentro de la region.

    Se dibuja como paralelogramo de suma de vectores: la primera version puso
    las dos piezas una detras de otra y quedaban casi alineadas con la
    diagonal, asi que no se veia que fueran dos.
    """
    W, H = 900, 580
    ox, oy, k = 90, 470, 36
    X = lambda x: ox + x * k
    Y = lambda y: oy - y * k

    s = [marco(
        W, H,
        "El poligono de la clase 1 con su esquina optima; desde ella salen las "
        "dos normales de las restricciones activas y la flecha del objetivo, "
        "que es la diagonal del paralelogramo que forman",
        "El gradiente, escrito con las normales activas",
        "En la esquina (8,2) del poligono, la flecha del objetivo c=(4,3) es la "
        "diagonal del paralelogramo que forman dos veces la normal de horas "
        "(1,1) y una vez la normal de polimero (2,1). Los coeficientes 2 y 1 "
        "son los precios sombra de esos dos recursos.",
    )]
    s += _ejes(ox, oy, 400, 400, "filtros x₁", "celdas x₂")

    V = [(0, 0), (9, 0), (8, 2), (2, 8), (0, 9)]
    pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in V)
    s.append(f'<polygon points="{pts}" fill="{mezclar(SERIE[1], 0.16)}" '
             f'stroke="{mezclar(SERIE[1], 0.6)}" stroke-width="2"/>')
    s.append(texto(X(2.6), Y(3.2), "región factible", color=mezclar(SERIE[1], 0.95), tam=13))

    # los dos lados activos, cada uno del color de su normal
    s.append(linea(X(2), Y(8), X(8), Y(2), color=SERIE[2], grosor=3.5))
    s.append(texto(X(2.4), Y(8.0) - 10, "lado de horas", color=SERIE[2], tam=13, anclaje="start"))
    s.append(linea(X(8), Y(2), X(9), Y(0), color=SERIE[0], grosor=3.5))
    s.append(texto(X(9.2), Y(0.4), "lado de polímero", color=SERIE[0], tam=13, anclaje="start"))

    vx, vy = 8, 2
    P = (X(vx), Y(vy))
    A = (X(vx + 2), Y(vy + 2))          # 2 × (1,1)
    Bp = (X(vx + 2), Y(vy + 1))         # 1 × (2,1)
    S = (X(vx + 4), Y(vy + 3))          # la suma, c = (4,3)
    s.append(linea(*A, *S, color=mezclar(SERIE[0], 0.7), grosor=2, guiones="6 5"))
    s.append(linea(*Bp, *S, color=mezclar(SERIE[2], 0.7), grosor=2, guiones="6 5"))
    s.append(_flechac(*P, *A, SERIE[2], "na"))
    s.append(_flechac(*P, *Bp, SERIE[0], "nb"))
    s.append(_flechac(*P, *S, ACENTO, "nc", grosor=3.5))
    s.append(punto(*P, r=7, color=TEXTO))
    s.append(texto(P[0] - 12, P[1] + 24, "(8, 2)", color=TEXTO, tam=14, peso="700", anclaje="end"))
    s.append(texto(A[0] - 6, A[1] - 12, "2 × (1,1)", color=SERIE[2], tam=14,
                   anclaje="end", peso="700"))
    s.append(texto(Bp[0] + 10, Bp[1] + 20, "1 × (2,1)", color=SERIE[0], tam=14,
                   anclaje="start", peso="700"))
    s.append(texto(S[0] + 12, S[1] - 6, "∇f = c = (4,3)", color=ACENTO, tam=15,
                   anclaje="start", peso="700"))

    s.append(texto(W / 2, H - 42,
                   "2 y 1 son los precios sombra de la clase 2: horas 2, polímero 1",
                   color=TEXTO, tam=14, peso="700"))
    s.append(texto(W / 2, H - 18,
                   "con un coeficiente negativo la flecha apuntaría hacia dentro, y todavía se podría mejorar",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_pasos_gradiente():
    """Las tres tasas sobre el desgaste (x-3)^2 + 4(y-2)^2, desde (0,0).

    Un panel por tasa, con las mismas curvas de nivel y el mismo encuadre para
    que las tres trayectorias se comparen. Los puntos se ITERAN aqui con el
    mismo paso que la pagina tabula, no se copian a mano, y las elipses se
    recortan contra su panel: sin recorte se salian al panel vecino.
    """
    import math
    W, H = 1020, 440
    ancho = alto = 280
    xmin, xmax, ymin, ymax = -1.2, 5.6, -2.6, 6.4

    def trayectoria(alpha, n=5, x=0.0, y=0.0):
        salida = [(x, y)]
        for _ in range(n):
            x, y = x - alpha * 2 * (x - 3), y - alpha * 8 * (y - 2)
            salida.append((x, y))
        return salida

    s = [marco(
        W, H,
        "Tres paneles con las mismas curvas de nivel elipticas del desgaste y "
        "una trayectoria en cada uno: la primera llega al centro, la segunda "
        "salta entre dos alturas, la tercera se sale del cuadro",
        "Tres tamaños de paso sobre el mismo valle",
        "Con alpha un decimo la trayectoria converge al minimo (3,2). Con un "
        "cuarto la coordenada vertical salta entre 0 y 4 sin acercarse mientras "
        "la horizontal si converge. Con tres decimos las dos se alejan.",
    )]

    paneles = (
        (0.10, "α = 1/10", "converge", SERIE[0]),
        (0.25, "α = 1/4", "la y salta para siempre", SERIE[2]),
        (0.30, "α = 3/10", "se va", ALARMA),
    )
    for i, (alpha, etiqueta, nota, color) in enumerate(paneles):
        ox, oy = 50 + i * 330, 350
        X = lambda x, ox=ox: ox + (x - xmin) / (xmax - xmin) * ancho
        Y = lambda y, oy=oy: oy - (y - ymin) / (ymax - ymin) * alto
        dentro = lambda x, y: xmin <= x <= xmax and ymin <= y <= ymax
        s.append(caja(ox, oy - alto, ancho, alto, borde=mezclar(SUAVE, 0.35), radio=8, grosor=1.5))
        s.append(texto(ox + ancho / 2, 46, etiqueta, color=color, tam=16, peso="700"))
        s.append(texto(ox + ancho / 2, 66, nota, color=SUAVE, tam=13))

        for nivel in (1, 4, 9, 16):
            a, b = math.sqrt(nivel), math.sqrt(nivel) / 2
            elipse = [(3 + a * math.cos(math.radians(t)), 2 + b * math.sin(math.radians(t)))
                      for t in range(0, 361, 3)]
            for t in _trozos(elipse, dentro):
                s.append(_curva([(X(x), Y(y)) for x, y in t], mezclar(SERIE[1], 0.45),
                                grosor=1.5))
        s.append(punto(X(3), Y(2), r=5, color=SERIE[1]))
        s.append(texto(X(3) + 10, Y(2) - 8, "(3,2)", color=SERIE[1], tam=12, anclaje="start"))

        puntos = trayectoria(alpha)
        visibles, fuga = [], None
        for x, y in puntos:
            if dentro(x, y):
                visibles.append((X(x), Y(y)))
            else:
                fuga = (X(x), Y(y))
                break
        if len(visibles) > 1:
            s.append(_curva(visibles, color, grosor=2.5))
        for j, (px, py) in enumerate(visibles):
            s.append(punto(px, py, r=4.5 if j else 6, color=color))
        if fuga is not None:
            # La trayectoria sale POR EL BORDE, con la punta justo donde lo
            # cruza. Dos versiones anteriores fallaron aqui: una apuntaba
            # siempre hacia abajo y hacia la derecha —y este paso se dispara
            # hacia arriba—, y otra dibujaba un tramo corto que quedaba encima
            # de la propia trayectoria. El rotulo sobra: el subtitulo del panel
            # ya dice "se va".
            ux, uy = visibles[-1]
            dx, dy = fuga[0] - ux, fuga[1] - uy
            t = 1.0
            for lim, d, v in ((ox, dx, ux), (ox + ancho, dx, ux),
                              (oy - alto, dy, uy), (oy, dy, uy)):
                if d:
                    tt = (lim - v) / d
                    if 0 < tt < t:
                        t = tt
            largo = math.hypot(dx * t, dy * t) or 1
            t *= max(0.0, (largo - 14) / largo)   # la punta cabe dentro del panel
            s.append(_flechac(ux, uy, ux + dx * t, uy + dy * t, color, f"fuga{i}", grosor=2.5))
        s.append(texto(X(0) + 4, Y(0) + 22, "arranca en (0,0)", color=SUAVE, tam=12))
    s.append(texto(W / 2, H - 14,
                   "mismo valle, mismo punto de arranque: lo único que cambia es cuánto se avanza",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


# --------------------------------------------------------------------------
# clase 4: el taller. Enteras generales, sin ninguna continua.
#
# Los dos diagramas de abajo CALCULAN su contenido desde estas tres constantes,
# como opt_poligono: la caja sale de las restricciones, la factibilidad de
# A x <= b y el valor de c. La tabla de la pagina 3 es copia de rejilla_taller().

A_TALLER = [[6, 4], [1, 2]]      # aleacion (kg), calibracion (horas)
B_TALLER = [24, 6]
C_TALLER = [5, 4]                # MB al dia: rover, sonda


def caja_taller():
    """Cota superior de cada variable, deducida del propio modelo.

    a_ij x_j <= sum_k a_ik x_k <= b_i cuando todo es no negativo, asi que cada
    restriccion con coeficiente positivo da un techo y el menor manda.
    """
    return [
        min(B_TALLER[i] // A_TALLER[i][j]
            for i in range(len(B_TALLER)) if A_TALLER[i][j] > 0)
        for j in range(len(C_TALLER))
    ]


def rejilla_taller():
    """Los candidatos de la caja, en el orden en que los mira el pseudocodigo.

    Devuelve (x1, x2, factible, valor, orden) con x1 por fuera y x2 por dentro,
    que es lo que hace el for anidado de la pagina.
    """
    u1, u2 = caja_taller()
    filas, orden = [], 0
    for x1 in range(u1 + 1):
        for x2 in range(u2 + 1):
            orden += 1
            factible = all(
                A_TALLER[i][0] * x1 + A_TALLER[i][1] * x2 <= B_TALLER[i]
                for i in range(len(B_TALLER))
            )
            filas.append((x1, x2, factible, C_TALLER[0] * x1 + C_TALLER[1] * x2, orden))
    return filas


def optimo_taller():
    """(x1, x2, valor, orden) del mejor candidato factible."""
    factibles = [f for f in rejilla_taller() if f[2]]
    mejor = max(factibles, key=lambda f: f[3])
    return mejor[0], mejor[1], mejor[3], mejor[4]


def _rombo(cx, cy, mx, my, relleno, borde=LINEA, grosor=2):
    puntos = f"{cx},{cy - my} {cx + mx},{cy} {cx},{cy + my} {cx - mx},{cy}"
    return (
        f'<polygon points="{puntos}" fill="{relleno}" stroke="{borde}" '
        f'stroke-width="{grosor}"/>'
    )


def _paso(numero, cx, cy):
    """El disco numerado que llevan los cuatro pasos del flujo."""
    return (
        punto(cx, cy, r=13, color=ACENTO)
        + texto(cx, cy + 5, numero, color=FONDO, tam=14, peso="700")
    )


def _paralelogramo(cx, cy, w, h, sesgo, relleno, borde=LINEA, grosor=2):
    """Entrada o salida, en la convencion clasica de diagrama de flujo."""
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    puntos = f"{x0 + sesgo},{y0} {x1},{y0} {x1 - sesgo},{y1} {x0},{y1}"
    return (
        f'<polygon points="{puntos}" fill="{relleno}" stroke="{borde}" '
        f'stroke-width="{grosor}"/>'
    )


def opt_flujo_enumerar():
    """Diagrama de flujo completo del pseudocodigo de la pagina 3.

    Completo quiere decir que no empieza a media ejecucion: lleva la entrada, la
    inicializacion del incumbente, la construccion de la caja, la prueba del
    ciclo, las dos decisiones, la actualizacion y la salida con su caso de
    infactibilidad. Cada nodo lleva la linea del pseudocodigo que le toca, y el
    orden de los nodos es el del pseudocodigo, no uno comodo para dibujar.
    """
    W, H = 760, 1050
    s = [marco(
        W, H,
        "Diagrama de flujo de la enumeracion, de la entrada a la salida: leer "
        "los datos, poner la mejor solucion en menos infinito, construir la "
        "caja de candidatos, y repetir un ciclo que toma el siguiente "
        "candidato, descarta el que no cumple las restricciones, descarta el "
        "que no supera a la mejor solucion y guarda el que si la supera; "
        "cuando la caja se agota devuelve la mejor solucion, o el aviso de que "
        "no hay ninguna factible",
        "Genera, filtra, compara",
        "Diagrama de flujo con diez pasos en una columna. Los paralelogramos "
        "son la entrada y la salida, los rectangulos son calculos y los rombos "
        "son decisiones. Cada nodo lleva entre corchetes la linea del "
        "pseudocodigo que representa. Un carril de retorno a la izquierda "
        "devuelve a la prueba del ciclo desde las dos respuestas negativas y "
        "desde la actualizacion; un carril a la derecha lleva a la salida "
        "cuando ya no quedan candidatos.",
    )]
    cx, izq, der = 380, 90, 690
    anchoc, altoc, my, mx = 380, 52, 46, 210
    proceso, decision = mezclar(LINEA, 0.22), mezclar(SERIE[1], 0.16)
    borde_dec, extremo = mezclar(SERIE[1], 0.5), mezclar(SERIE[0], 0.18)
    borde_ext = mezclar(SERIE[0], 0.5)

    def rect(cy, etiqueta, cuerpo, relleno=proceso, borde=LINEA, alto=altoc):
        return [
            caja(cx - anchoc // 2, cy - alto // 2, anchoc, alto,
                 relleno=relleno, borde=borde),
            texto(cx - anchoc // 2 + 14, cy - alto // 2 + 20, etiqueta,
                  color=SUAVE, tam=11, anclaje="start", fuente=MONO),
            texto(cx + 14, cy + 6, cuerpo, tam=15),
        ]

    def rombo(cy, etiqueta, cuerpo):
        return [
            _rombo(cx, cy, mx, my, decision, borde_dec),
            texto(cx - 145, cy + 4, etiqueta, color=SUAVE, tam=11,
                  anclaje="start", fuente=MONO),
            texto(cx + 25, cy + 6, cuerpo, tam=15),
        ]

    # Entrada
    s.append(_paralelogramo(cx, 82, anchoc, altoc, 22, extremo, borde_ext))
    s.append(texto(cx - anchoc // 2 + 36, 62, "[ENTRADA]", color=SUAVE, tam=11,
                   anclaje="start", fuente=MONO))
    s.append(texto(cx, 90, "c, A, b, l, u", tam=15))

    s += rect(160, "[L1]", "mejor ← −∞ ;   x* ← «ninguno»")
    s += rect(238, "[L2]", "X ← { l₁..u₁ } × ⋯ × { lₙ..uₙ }")
    s += rombo(336, "[L3]", "¿queda algún x ∈ X sin revisar?")
    s += rect(434, "[L3]", "x ← el siguiente de X")
    s += rombo(532, "[L4]", "¿Ax ≤ b?")
    s += rect(630, "[L5]", "z ← cᵀx")
    s += rombo(728, "[L6]", "¿z > mejor?")
    s += rect(826, "[L7]", "mejor ← z ;   x* ← x")

    # Salida, con su caso de infactibilidad
    s.append(_paralelogramo(cx, 952, anchoc, 64, 22, extremo, borde_ext))
    s.append(texto(cx - anchoc // 2 + 36, 930, "[L9–L10]", color=SUAVE, tam=11,
                   anclaje="start", fuente=MONO))
    s.append(texto(cx, 950, "devuelve x*, mejor", tam=15))
    s.append(texto(cx, 972, "«no hay factible» si x* = «ninguno»",
                   color=SUAVE, tam=12))

    for y0, y1 in ((108, 132), (186, 210), (264, 288), (382, 406),
                   (460, 484), (578, 602), (656, 680), (774, 798)):
        s.append(flecha(cx, y0, cx, y1))
    s.append(texto(cx + 18, 400, "sí", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(cx + 18, 596, "sí", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(cx + 18, 792, "sí", color=SUAVE, tam=13, anclaje="start"))

    # Carril de retorno: las dos negativas y la actualizacion vuelven a [L3].
    for cy in (532, 728):
        s.append(flecha(cx - mx, cy, izq, cy, color=SUAVE, marcador="s"))
        s.append(texto(cx - mx - 12, cy - 10, "no", color=SUAVE, tam=13,
                       anclaje="end"))
    s.append(flecha(cx - anchoc // 2, 826, izq, 826, color=SUAVE, marcador="s"))
    s.append(linea(izq, 826, izq, 336, color=SUAVE))
    s.append(flecha(izq, 336, cx - mx, 336))
    s.append(texto(izq + 10, 310, "vuelve al ciclo", color=SUAVE, tam=12,
                   anclaje="start"))

    # Carril de salida: solo se toma cuando la caja se agota.
    s.append(linea(cx + mx, 336, der, 336, color=SUAVE))
    s.append(texto(cx + mx + 12, 326, "no", color=SUAVE, tam=13, anclaje="start"))
    s.append(linea(der, 336, der, 952, color=SUAVE))
    s.append(flecha(der, 952, cx + anchoc // 2 - 11, 952, color=SUAVE, marcador="s"))

    # Leyenda de formas.
    ly = 1018
    s.append(_paralelogramo(140, ly, 44, 22, 8, extremo, borde_ext))
    s.append(texto(170, ly + 5, "entrada / salida", color=SUAVE, tam=12,
                   anclaje="start"))
    s.append(caja(320, ly - 11, 44, 22, relleno=proceso, borde=LINEA, radio=5))
    s.append(texto(374, ly + 5, "cálculo", color=SUAVE, tam=12, anclaje="start"))
    s.append(_rombo(470, ly, 26, 13, decision, borde_dec))
    s.append(texto(504, ly + 5, "decisión", color=SUAVE, tam=12, anclaje="start"))
    s.append(texto(620, ly + 5, "[Ln] = línea", color=SUAVE, tam=12,
                   anclaje="start", fuente=MONO))
    s.append(cierre())
    return "".join(s)


def opt_rejilla():
    filas = rejilla_taller()
    u1, u2 = caja_taller()
    gx, gy = u1 + 1, u2 + 1
    cw, ch = 96, 68
    x0, y0 = 170, 86
    W, H = x0 + gx * cw + 40, y0 + gy * ch + 150
    mx1, mx2, mejor, orden_mejor = optimo_taller()
    s = [marco(
        W, H,
        f"Rejilla de {gx} columnas por {gy} renglones con los {gx * gy} planes "
        f"posibles; {sum(1 for f in filas if f[2])} llevan su valor y el resto "
        "están tachados por no caber, y el ganador está resaltado",
        "La caja entera, con su valor",
        "Cada celda es un plan: una columna por número de rovers y un renglón "
        "por número de sondas. Las celdas que cumplen las dos restricciones "
        "llevan los MB que transmite ese plan; las que no, van tachadas. El "
        "número pequeño de cada celda es el lugar que ocupa en el recorrido.",
    )]
    for x1, x2, factible, valor, orden in filas:
        x = x0 + x1 * cw
        y = y0 + (u2 - x2) * ch
        gana = (x1, x2) == (mx1, mx2)
        if gana:
            s.append(caja(x + 4, y + 4, cw - 8, ch - 8,
                          relleno=mezclar(ACENTO, 0.24), borde=ACENTO, grosor=3))
        elif factible:
            s.append(caja(x + 4, y + 4, cw - 8, ch - 8,
                          relleno=mezclar(SERIE[0], 0.14), borde=mezclar(SERIE[0], 0.4)))
        else:
            s.append(caja(x + 4, y + 4, cw - 8, ch - 8,
                          relleno=mezclar(ALARMA, 0.10), borde=mezclar(ALARMA, 0.3)))
            tachado = mezclar(ALARMA, 0.65)
            s.append(linea(x + 26, y + 20, x + cw - 26, y + ch - 20, color=tachado))
            s.append(linea(x + cw - 26, y + 20, x + 26, y + ch - 20, color=tachado))
        s.append(texto(x + 14, y + 24, str(orden), color=SUAVE, tam=11, anclaje="start"))
        if factible:
            s.append(texto(x + cw // 2, y + 44, str(valor), tam=22,
                           peso="700" if gana else "500"))
    for x1 in range(gx):
        s.append(texto(x0 + x1 * cw + cw // 2, y0 - 14, str(x1), color=SUAVE, tam=14))
    for x2 in range(gy):
        s.append(texto(x0 - 18, y0 + (u2 - x2) * ch + ch // 2 + 5, str(x2),
                       color=SUAVE, tam=14, anclaje="end"))
    s.append(texto(36, y0 - 14, "x₂ = sondas", color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(x0 + gx * cw // 2, y0 + gy * ch + 34, "x₁ = rovers",
                   color=SUAVE, tam=15))
    ly = y0 + gy * ch + 74
    s.append(caja(x0, ly - 14, 22, 20, relleno=mezclar(SERIE[0], 0.14),
                  borde=mezclar(SERIE[0], 0.4), radio=5))
    s.append(texto(x0 + 32, ly + 2, "cabe", color=SUAVE, tam=13, anclaje="start"))
    s.append(caja(x0 + 110, ly - 14, 22, 20, relleno=mezclar(ALARMA, 0.10),
                  borde=mezclar(ALARMA, 0.3), radio=5))
    s.append(texto(x0 + 142, ly + 2, "no cabe", color=SUAVE, tam=13, anclaje="start"))
    # La nota va en su propio renglon: en la misma linea que los cuadros se
    # salia del lienzo por la derecha, y eso solo se vio renderizando.
    s.append(texto(W // 2, ly + 34,
                   f"el número pequeño es el orden de revisión: el ganador "
                   f"sale en el {orden_mejor} de {len(filas)}",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)



# --------------------------------------------------------------------------
# clase 4, pagina 4: ramificar y acotar sobre el mismo taller.
#
# El arbol NO se dibuja a mano: se ramifica de verdad, con aritmetica exacta de
# fracciones y con las dos reglas de desempate que la pagina declara. Si un dato
# del taller cambia, el arbol cambia solo y su guarda lo comprueba.

def _lp_caja(lo, hi):
    """Optimo exacto del PL del taller sobre la caja [lo, hi].

    Enumera vertices: el optimo de un lineal acotado esta en uno de ellos.
    Devuelve (punto, valor) o (None, None) si la caja no deja nada factible.
    """
    rectas = [
        (F(A_TALLER[0][0]), F(A_TALLER[0][1]), F(B_TALLER[0])),
        (F(A_TALLER[1][0]), F(A_TALLER[1][1]), F(B_TALLER[1])),
        (F(1), F(0), F(hi[0])), (F(-1), F(0), -F(lo[0])),
        (F(0), F(1), F(hi[1])), (F(0), F(-1), -F(lo[1])),
    ]
    mejor, punto = None, None
    for (a1, b1, c1), (a2, b2, c2) in combinations(rectas, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if any(a * x + b * y > c for a, b, c in rectas):
            continue
        z = F(C_TALLER[0]) * x + F(C_TALLER[1]) * y
        if mejor is None or z > mejor:
            mejor, punto = z, (x, y)
    return punto, mejor


def arbol_taller():
    """Ramifica y acota el taller. Un nodo por entrada, en orden de apertura.

    Reglas de desempate, las mismas que imprime la pagina: de la lista sale el
    ultimo que entro, se empuja primero el hijo del <= para que abra el del >=,
    y se parte por la primera variable fraccionaria en el orden en que estan
    escritas.
    """
    u = caja_taller()
    pila = [([0, 0], list(u), "raíz", None)]
    mejor, x_mejor, nodos = None, None, []
    while pila:
        lo, hi, etiqueta, padre = pila.pop()
        x, z = _lp_caja(lo, hi)
        n = len(nodos) + 1
        if z is None:
            nodos.append(dict(n=n, etiqueta=etiqueta, padre=padre, cota=None,
                              x=None, cierre="infactible"))
            continue
        if mejor is not None and z <= mejor:
            nodos.append(dict(n=n, etiqueta=etiqueta, padre=padre, cota=z,
                              x=x, cierre="poda"))
            continue
        frac = [j for j in (0, 1) if x[j].denominator != 1]
        if not frac:
            mejor, x_mejor = z, x
            nodos.append(dict(n=n, etiqueta=etiqueta, padre=padre, cota=z,
                              x=x, cierre="entera"))
            continue
        j = frac[0]
        piso, techo = int(x[j]), int(x[j]) + 1
        nodos.append(dict(n=n, etiqueta=etiqueta, padre=padre, cota=z, x=x,
                          cierre="parte", j=j, piso=piso, techo=techo))
        lo1, hi1 = list(lo), list(hi)
        hi1[j] = piso
        lo2, hi2 = list(lo), list(hi)
        lo2[j] = techo
        pila.append((lo1, hi1, f"x{_sub(j+1)} ≤ {piso}", n))
        pila.append((lo2, hi2, f"x{_sub(j+1)} ≥ {techo}", n))
    return nodos, x_mejor, mejor


def _sub(k):
    return "\u2081\u2082\u2083\u2084"[k - 1]


def _frac(z, decimal=False):
    """La cota como la imprime la pagina: entera si lo es, si no a/b."""
    if z.denominator == 1:
        return str(z.numerator)
    texto_ = f"{z.numerator}/{z.denominator}"
    return f"{texto_} ≈ {float(z):.2f}" if decimal else texto_


def _plano_taller(W, H):
    """El plano del taller, con su poligono y sus puntos enteros."""
    # top = 4 y no 6: con 6 la mitad del lienzo quedaba vacia sobre la region.
    ox, oy, esc, top = 80, H - 96, 80, 5
    px, py, plano = _plano(W, H, ox, oy, esc, top)
    V = _region([[F(a) for a in fila] for fila in A_TALLER], [F(b) for b in B_TALLER])
    ruta = " ".join(f"{px(x)},{py(y)}" for x, y in V)
    poligono = (f'<polygon points="{ruta}" fill="{mezclar(LINEA, 0.30)}" '
                f'stroke="{mezclar(SERIE[1], 0.6)}" stroke-width="2"/>')
    return px, py, plano, poligono, top


def _puntos_enteros(px, py, resaltar=None):
    """Los puntos de la reticula que caben, como circulos."""
    s = []
    for x1, x2, factible, valor, _ in rejilla_taller():
        if not factible:
            continue
        gana = resaltar is not None and (x1, x2) == resaltar
        s.append(punto(px(x1), py(x2), r=8 if gana else 5,
                       color=ACENTO if gana else SERIE[0]))
    return s


def opt_relajacion_corte():
    W, H = 640, 560
    px, py, plano, poligono, top = _plano_taller(W, H)
    x_ent, _, z_ent = optimo_taller()[0], None, optimo_taller()[2]
    s = [marco(
        W, H,
        "El poligono del taller con los trece planes enteros que caben dentro, "
        "el optimo continuo marcado con una cruz sobre el borde y el mejor plan "
        "entero resaltado en la esquina de abajo a la derecha",
        "La cota que da la relajación",
        "Region factible del taller. Los circulos son los planes enteros. La "
        "cruz es el optimo de la relajacion, que vale 21 y no es un punto "
        "entero. El circulo grande es el mejor plan entero, que vale 20: por "
        "debajo de la cruz, como manda la cota.",
    )]
    s.append(poligono)
    s += plano
    s += _puntos_enteros(px, py, resaltar=(4, 0))
    cx, cy = px(3), py(1.5)
    for dx, dy in ((-9, -9, ), (-9, 9)):
        s.append(linea(cx + dx, cy + dy, cx - dx, cy - dy, color=ALARMA, grosor=3))
    s.append(texto(cx + 16, cy - 10, "relajación: (3, 3/2)", color=ALARMA, tam=14,
                   anclaje="start"))
    s.append(texto(cx + 16, cy + 10, "cota = 21", color=ALARMA, tam=14, peso="700",
                   anclaje="start"))
    s.append(texto(px(4), py(0) + 46, "mejor entero: (4, 0) = 20",
                   color=ACENTO, tam=14))
    s.append(texto(W // 2, H - 26,
                   "ningún plan entero puede pasar de 21, porque todos están dentro",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_ramas():
    W, H = 640, 560
    px, py, plano, poligono, top = _plano_taller(W, H)
    s = [marco(
        W, H,
        "El mismo poligono partido en dos por una franja horizontal entre uno y "
        "dos, que no contiene ningun punto entero; arriba la rama de x dos mayor "
        "o igual que dos y abajo la de x dos menor o igual que uno",
        "Partir no pierde ninguna solución",
        "La franja abierta entre x2 igual a uno y x2 igual a dos esta sombreada "
        "y vacia de puntos enteros. Las dos ramas se reparten los trece planes: "
        "cuatro arriba y nueve abajo, y ninguno se queda en medio.",
    )]
    s.append(poligono)
    # La franja se corta en x1 = 4: fuera de la region no hay nada que decir.
    franja = (f'<rect x="{px(0)}" y="{py(2)}" width="{px(4) - px(0)}" '
              f'height="{py(1) - py(2)}" fill="{mezclar(ALARMA, 0.22)}"/>')
    s.append(franja)
    s += plano
    s += _puntos_enteros(px, py)
    for u, etiqueta, color in ((2, "x₂ ≥ 2", SERIE[1]), (1, "x₂ ≤ 1", SERIE[2])):
        s.append(linea(px(0), py(u), px(4.6), py(u), color=mezclar(color, 0.9),
                       grosor=2, guiones="7 5"))
        s.append(texto(px(4.6) + 8, py(u) + 5, etiqueta, color=mezclar(color, 0.9),
                       tam=14, anclaje="start"))
    s.append(texto(px(2), py(1.5) + 5, "ningún punto entero",
                   color=ALARMA, tam=13))
    s.append(texto(W // 2, H - 26,
                   "la mitad de arriba se queda 4 planes; la de abajo, 9",
                   color=SUAVE, tam=13))
    s.append(cierre())
    return "".join(s)


def opt_arbol_paso(paso):
    """Snapshot of the workshop tree after 0–4 processed nodes.

    Reuse the exact trace behind the final tree, revealing a node only once
    its parent has branched and revealing its result only once processed.
    Fixed positions keep the same branches recognizable across snapshots.
    """
    if paso not in range(5):
        raise ValueError("El recorrido parcial admite pasos de 0 a 4")
    nodos, _, _ = arbol_taller()
    visibles = [nd for nd in nodos if nd["padre"] is None or nd["padre"] <= paso]
    pendientes = [nd for nd in visibles if nd["n"] > paso]
    siguiente = min(nd["n"] for nd in pendientes)
    guardadas = [nd for nd in nodos if nd["n"] <= paso and nd["cierre"] == "entera"]
    guardada = max(guardadas, key=lambda nd: nd["cota"]) if guardadas else None

    W = 700
    H = 296 if paso == 0 else 486 if paso <= 2 else 676
    lugares = {1: (350, 68), 3: (230, 258), 2: (560, 258),
               5: (110, 448), 4: (350, 448)}
    ancho, alto = 196, 134
    titulo = "Antes de resolver el primer nodo" if paso == 0 else f"Árbol después del paso {paso}"
    resumen = []
    for nd in visibles:
        if nd["n"] <= paso:
            estado = "dividido" if nd["cierre"] == "parte" else "cerrado con solución entera"
            resumen.append(f'Nodo {nd["n"]}, {nd["etiqueta"]}: {estado}, cota {_frac(nd["cota"])}.')
        else:
            turno = "por resolver" if paso == 0 else "siguiente" if nd["n"] == siguiente else "pendiente"
            herencia = ", heredando x₂ ≤ 1" if nd["padre"] == 3 else ""
            resumen.append(f'{nd["etiqueta"]}{herencia}: {turno}, relajación sin resolver.')
    desc = " ".join(resumen)
    s = [marco(W, H, desc, titulo, desc)]
    s.append(texto(W / 2, 29, titulo, tam=18, peso="700"))

    for nd in visibles:
        if nd["padre"] is None:
            continue
        px, py = lugares[nd["padre"]]
        x, y = lugares[nd["n"]]
        s.append(flecha(px, py + alto, x, y - 4, color=SUAVE, grosor=2, marcador="s"))

    for nd in visibles:
        n = nd["n"]
        cx, y = lugares[n]
        x = cx - ancho / 2
        procesado = n <= paso
        if not procesado:
            estado = "POR RESOLVER" if paso == 0 else "SIGUIENTE" if n == siguiente else "PENDIENTE"
            color = SERIE[2] if n == siguiente else SUAVE
        else:
            estado = "DIVIDIDO" if nd["cierre"] == "parte" else "CERRADO · ENTERO"
            color = SERIE[1] if nd["cierre"] == "parte" else SERIE[0]
        s.append(caja(x, y, ancho, alto, relleno=mezclar(color, 0.10), borde=color,
                      grosor=3 if n == siguiente else 2,
                      guiones="7 4" if not procesado else None))
        nombre = "Taller original" if n == 1 else nd["etiqueta"]
        # Processing numbers belong only to resolved nodes, except the sole root.
        if procesado or n == 1:
            nombre = f"[{n}] {nombre}"
        contexto = "Problema 1 de la bitácora" if n == 1 else "hereda x₂ ≤ 1" if nd["padre"] == 3 else "más restricciones del P1"
        s.append(texto(cx, y + 23, nombre, tam=16, peso="700"))
        s.append(texto(cx, y + 45, contexto, tam=13, color=SUAVE))
        s.append(texto(cx, y + 69, estado, tam=14, peso="700", color=color))
        if procesado:
            s.append(texto(cx, y + 92, f'cota = {_frac(nd["cota"])}', tam=15))
            punto_ = ", ".join(_frac(v) for v in nd["x"])
            etiqueta = "plan entero" if nd["cierre"] == "entera" else "óptimo relajado"
            s.append(texto(cx, y + 115, f"{etiqueta}: ({punto_})", tam=12))
        else:
            s.append(texto(cx, y + 94, "relajación sin resolver", tam=13, color=SUAVE))

    if guardada is None:
        registro = "Mejor solución entera guardada: ninguna"
    else:
        punto_ = ", ".join(_frac(v) for v in guardada["x"])
        registro = f'Mejor solución entera: ({punto_}) · valor {_frac(guardada["cota"])}'
    s.append(texto(W / 2, H - 50, registro, tam=16, peso="700"))
    s.append(texto(W / 2, H - 24, "Cada nodo conserva las restricciones del taller y las de su camino.",
                   tam=13, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_arbol():
    W, H = 940, 560
    nodos, x_mejor, mejor = arbol_taller()
    por_n = {nd["n"]: nd for nd in nodos}
    lugar = {1: (470, 76), 3: (250, 250), 2: (720, 250), 5: (130, 424), 4: (390, 424)}
    color_cierre = {"entera": SERIE[0], "poda": ALARMA, "parte": SERIE[1],
                    "infactible": ALARMA}
    s = [marco(
        W, H,
        "Arbol de cinco nodos: la raiz con cota veintiuno se parte en dos ramas; "
        "la de la derecha cierra con una solucion entera de dieciocho y la de la "
        "izquierda se vuelve a partir, y de ahi salen la solucion entera de "
        "veinte y una poda por cota",
        "El árbol del taller",
        "Cada caja es un subproblema con su cota. Verde, la relajacion salio "
        "entera y cierra la rama. Rojo, la cota no supera a la mejor solucion y "
        "se poda. Azul, hay que partir. El numero entre corchetes es el orden "
        "en que se abrieron, que no es el de izquierda a derecha.",
    )]
    ancho, alto = 218, 96
    for n, (cx, cy) in lugar.items():
        nd = por_n[n]
        if nd["padre"] is not None:
            pcx, pcy = lugar[nd["padre"]]
            s.append(flecha(pcx, pcy + alto // 2, cx, cy - alto // 2,
                            color=SUAVE, marcador="s"))
    for n, (cx, cy) in lugar.items():
        nd = por_n[n]
        col = color_cierre[nd["cierre"]]
        s.append(caja(cx - ancho // 2, cy - alto // 2, ancho, alto,
                      relleno=mezclar(col, 0.16), borde=mezclar(col, 0.55)))
        s.append(texto(cx - ancho // 2 + 12, cy - alto // 2 + 20, f"[{n}]",
                       color=SUAVE, tam=12, anclaje="start", fuente=MONO))
        s.append(texto(cx + 10, cy - alto // 2 + 20, nd["etiqueta"], tam=15, peso="600"))
        s.append(texto(cx, cy + 4, f"cota = {_frac(nd['cota'], decimal=True)}", tam=15))
        if nd["cierre"] == "parte":
            detalle = f"x{_sub(nd['j']+1)} = {_frac(nd['x'][nd['j']])} → parte"
        elif nd["cierre"] == "entera":
            px_, py_ = nd["x"]
            detalle = f"entera ({px_}, {py_}) → mejor {_frac(nd['cota'])}"
        else:
            detalle = f"{_frac(nd['cota'])} ≤ {mejor} → poda"
        s.append(texto(cx, cy + alto // 2 - 12, detalle, color=mezclar(col, 0.95), tam=13))
    filas = [(mezclar(SERIE[1], 0.9), "hay que partir"),
             (mezclar(SERIE[0], 0.9), "entera: cierra la rama"),
             (mezclar(ALARMA, 0.9), "poda por cota")]
    s += _leyenda(640, 400, filas, ancho=270)
    s.append(texto(470, H - 22,
                   f"cinco nodos, y el óptimo es ({x_mejor[0]}, {x_mejor[1]}) = {mejor}",
                   color=SUAVE, tam=14))
    s.append(cierre())
    return "".join(s)



def opt_flujo_ramificar():
    """Diagrama de flujo completo de ramificar y acotar.

    Mismo contrato que opt_flujo_enumerar: entrada, inicializacion, el ciclo
    entero con sus tres salidas —poda por infactibilidad, poda por cota y cierre
    por solucion entera— y la salida. Cada nodo lleva su linea [Ln].
    """
    W, H = 1000, 1290
    s = [marco(
        W, H,
        "Diagrama de flujo de ramificar y acotar, de la entrada a la salida: "
        "inicializar la mejor solucion, meter el problema original en la lista "
        "de nodos vivos, y repetir un ciclo que saca un nodo, lo descarta si su "
        "relajacion es infactible o si su cota no supera a la mejor solucion, "
        "lo guarda si la relajacion salio entera, y si no lo parte en dos por "
        "una variable fraccionaria; cuando la lista se vacia devuelve la mejor "
        "solucion",
        "Ramificar y acotar, paso a paso",
        "Doce pasos en una columna. Los paralelogramos son la entrada y la "
        "salida, los rectangulos son calculos y los rombos son decisiones. Tres "
        "caminos vuelven al ciclo: las dos podas por la izquierda y, tras "
        "guardar o partir, tambien por la izquierda. Un carril a la derecha "
        "lleva a la salida cuando la lista de nodos vivos queda vacia. Al pie, una "
        "leyenda dice que x con barra y z con barra son el punto y el valor que "
        "devuelve la relajacion, y que x estrella y mejor son la mejor solucion "
        "entera encontrada hasta ahora y su valor.",
    )]
    cx, izq, rodeo, salida_x = 430, 90, 770, 910
    anchoc, altoc, my, mx = 420, 52, 46, 200
    proceso, decision = mezclar(LINEA, 0.22), mezclar(SERIE[1], 0.16)
    borde_dec, extremo = mezclar(SERIE[1], 0.5), mezclar(SERIE[0], 0.18)
    borde_ext = mezclar(SERIE[0], 0.5)

    def rect(cy, etiqueta, cuerpo, alto=altoc):
        return [
            caja(cx - anchoc // 2, cy - alto // 2, anchoc, alto,
                 relleno=proceso, borde=LINEA),
            texto(cx - anchoc // 2 + 14, cy - alto // 2 + 20, etiqueta,
                  color=SUAVE, tam=11, anclaje="start", fuente=MONO),
            texto(cx + 14, cy + 6, cuerpo, tam=15),
        ]

    def rombo(cy, etiqueta, cuerpo):
        return [
            _rombo(cx, cy, mx, my, decision, borde_dec),
            texto(cx - 142, cy + 4, etiqueta, color=SUAVE, tam=11,
                  anclaje="start", fuente=MONO),
            texto(cx + 28, cy + 6, cuerpo, tam=15),
        ]

    s.append(_paralelogramo(cx, 82, anchoc, altoc, 22, extremo, borde_ext))
    s.append(texto(cx - anchoc // 2 + 36, 62, "[ENTRADA]", color=SUAVE, tam=11,
                   anclaje="start", fuente=MONO))
    s.append(texto(cx, 90, "c, A, b, l, u", tam=15))

    s += rect(160, "[L1]", "mejor ← −∞ ;   x* ← «ninguno»")
    s += rect(236, "[L2]", "L ← { el problema original }", alto=74)
    s.append(texto(cx + 14, 262, "L es la lista de nodos vivos", color=SUAVE, tam=12))
    s += rombo(336, "[L3]", "¿L ≠ { } ?")
    s += rect(434, "[L4]", "P ← saca un nodo de L")
    s += rombo(532, "[L5]", "¿la relajación de P es factible?")
    s += rect(630, "[L6]", "x̄, z̄ ← óptimo de la relajación")
    s += rombo(728, "[L7]", "¿z̄ > mejor?")
    s += rombo(838, "[L8]", "¿x̄ es entera?")
    s += rect(948, "[L9]", "mejor ← z̄ ;   x* ← x̄")
    s += rect(1050, "[L10–L11]", "parte en xⱼ ≤ ⌊x̄ⱼ⌋  y  xⱼ ≥ ⌈x̄ⱼ⌉")

    s.append(_paralelogramo(cx, 1140, anchoc, 60, 22, extremo, borde_ext))
    s.append(texto(cx - anchoc // 2 + 36, 1120, "[L13]", color=SUAVE, tam=11,
                   anclaje="start", fuente=MONO))
    s.append(texto(cx, 1140, "devuelve x*, mejor", tam=15))
    s.append(texto(cx, 1162, "«no hay factible» si x* = «ninguno»", color=SUAVE, tam=12))

    for y0, y1 in ((108, 132), (186, 210), (264, 288), (382, 406),
                   (460, 484), (578, 602), (656, 680), (774, 790),
                   (884, 920)):
        s.append(flecha(cx, y0, cx, y1))
    for y, etiqueta in ((786, "sí"), (896, "sí"), (602, "sí")):
        s.append(texto(cx + 18, y, etiqueta, color=SUAVE, tam=13, anclaje="start"))

    # Los tres retornos al ciclo, por la izquierda.
    for cy, nota in ((532, "poda por infactibilidad"), (728, "poda por cota")):
        s.append(flecha(cx - mx, cy, izq, cy, color=SUAVE, marcador="s"))
        s.append(texto(cx - mx - 12, cy - 10, "no", color=SUAVE, tam=13, anclaje="end"))
        # La nota va DEBAJO de la flecha: en la misma linea se montaba con el "no".
        s.append(texto(izq + 10, cy + 20, nota, color=SUAVE, tam=12, anclaje="start"))
    for cy in (948, 1050):
        s.append(flecha(cx - anchoc // 2, cy, izq, cy, color=SUAVE, marcador="s"))
    s.append(linea(izq, 1050, izq, 336, color=SUAVE))
    s.append(flecha(izq, 336, cx - mx, 336))
    s.append(texto(izq + 10, 310, "vuelve al ciclo", color=SUAVE, tam=12, anclaje="start"))

    # El "no" de L8 rodea por la derecha hasta el nodo que parte.
    s.append(linea(cx + mx, 838, rodeo, 838, color=SUAVE))
    s.append(texto(cx + mx + 12, 828, "no", color=SUAVE, tam=13, anclaje="start"))
    s.append(linea(rodeo, 838, rodeo, 1050, color=SUAVE))
    s.append(flecha(rodeo, 1050, cx + anchoc // 2, 1050, color=SUAVE, marcador="s"))

    # El carril de salida, mas a la derecha para no cruzar el rodeo.
    s.append(linea(cx + mx, 336, salida_x, 336, color=SUAVE))
    s.append(texto(cx + mx + 12, 326, "no", color=SUAVE, tam=13, anclaje="start"))
    s.append(linea(salida_x, 336, salida_x, 1140, color=SUAVE))
    s.append(flecha(salida_x, 1140, cx + anchoc // 2 - 11, 1140, color=SUAVE, marcador="s"))

    # La leyenda va dentro: la figura se lee sola, sin la tabla de la pagina.
    s.append(linea(140, 1200, W - 140, 1200, color=mezclar(LINEA, 0.5), grosor=1))
    s.append(texto(cx, 1228,
                   "x̄, z̄  —  el punto y el valor que devuelve la relajación: pueden tener fracciones",
                   color=SUAVE, tam=14))
    s.append(texto(cx, 1256,
                   "x*, mejor  —  la mejor solución entera encontrada hasta ahora, y su valor",
                   color=SUAVE, tam=14))
    s.append(cierre())
    return "".join(s)



def opt_arbol_vocabulario():
    """El recordatorio de vocabulario de la pagina 4, sin numeros.

    Generico a proposito: aqui no se resuelve nada, solo se senala como se
    llama cada parte. El arbol con los datos del taller es opt_arbol.
    """
    W, H = 860, 500
    s = [marco(
        W, H,
        "Arbol generico de tres niveles: una raiz arriba, dos hijos debajo, y "
        "el hijo de la izquierda con dos hijos propios; un recuadro punteado "
        "encierra al hijo de la izquierda con todo lo que cuelga de el",
        "Cómo se llama cada parte",
        "Esquema sin numeros para nombrar las partes de un arbol de "
        "subproblemas: la raiz es el problema original, cada circulo es un "
        "nodo, los dos que salen de uno son sus hijos, un nodo que no se "
        "partio es una hoja, y un nodo con todo lo que cuelga de el es una "
        "rama.",
    )]
    raiz, izq, der = (430, 86), (280, 216), (600, 216)
    nieto_a, nieto_b = (200, 336), (360, 336)
    r = 24

    s.append(caja(146, 172, 268, 216, relleno=mezclar(ACENTO, 0.12),
                  borde=ACENTO, radio=18, guiones="7 6"))
    s.append(texto(150, 160, "rama", color=ACENTO, tam=15, peso="700",
                   anclaje="start"))

    for a, b in ((raiz, izq), (raiz, der), (izq, nieto_a), (izq, nieto_b)):
        s.append(linea(a[0], a[1] + r, b[0], b[1] - r, color=SUAVE))
    for centro in (raiz, izq, der, nieto_a, nieto_b):
        s.append(punto(centro[0], centro[1], r=r, color=mezclar(SERIE[1], 0.5)))

    s.append(texto(raiz[0] + r + 16, raiz[1] + 5, "raíz", tam=15, peso="700",
                   anclaje="start"))
    s.append(texto(raiz[0] + r + 70, raiz[1] + 5, "el problema original",
                   color=SUAVE, tam=13, anclaje="start"))
    s.append(texto(der[0] + r + 16, der[1] + 5, "hoja", tam=15, peso="700",
                   anclaje="start"))
    s.append(texto(der[0] + r + 74, der[1] + 5, "no se partió", color=SUAVE,
                   tam=13, anclaje="start"))
    # "hijos" va sobre la arista derecha, que esta vacia: en el centro chocaba
    # con la descripcion de "rama".
    s.append(texto(430, 156, "hijos", color=SUAVE, tam=13))
    s.append(texto(W // 2, H - 56,
                   "cada círculo es un nodo, es decir, un subproblema",
                   color=SUAVE, tam=14))
    s.append(texto(W // 2, H - 28,
                   "abrir un nodo es resolver su relajación",
                   color=SUAVE, tam=14))
    s.append(cierre())
    return "".join(s)



def opt_clasificacion_sigmoide():
    """Sigmoide calculada; las rectas 0 y 1 son límites, no valores alcanzados."""
    W, H = 560, 538
    izquierda, derecha, arriba, abajo = 110, 514, 128, 366

    def coord(z, probabilidad):
        return (izquierda + (z + 4) / 8 * (derecha - izquierda),
                abajo - probabilidad * (abajo - arriba))

    s = [marco(
        W, H,
        "Sigmoide de z igual a alfa más beta por x; el score normalizado p "
        "se interpreta como probabilidad estimada. Sube de 0 a 1 sin "
        "alcanzar esos límites y vale 0.5 cuando z es cero",
        "La sigmoide convierte z en un score normalizado p",
        "Curva calculada p = 1 / (1 + exp(-z)) para z entre -4 y 4. "
        "El score p se interpreta como probabilidad estimada del modelo; "
        "su normalización no garantiza calibración con frecuencias reales. "
        "El eje horizontal es z = alfa + beta por x. Las líneas "
        "discontinuas p = 0 y p = 1 son asíntotas. El punto central es "
        "z = 0, p = 0.5. Para todo z real finito, 0 < p < 1.",
    )]
    s.append(texto(W / 2, 38, "La sigmoide", tam=28, peso="700"))
    s.append(texto(W / 2, 77, "p = 1 / (1 + exp(−z))", tam=23, color=SERIE[1]))
    s.append('<g transform="rotate(-90 26 247)">'
             + texto(26, 247, "Score normalizado p", tam=22) + '</g>')
    for probabilidad in (0, 0.5, 1):
        _, y = coord(0, probabilidad)
        s.append(linea(izquierda, y, derecha, y,
                       color=SERIE[2] if probabilidad != 0.5 else LINEA,
                       grosor=1.5, guiones="7 7"))
        s.append(texto(izquierda - 14, y + 7, f"{probabilidad:g}",
                       tam=22, anclaje="end"))
    s.append(flecha(izquierda, abajo, izquierda, arriba - 12,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(derecha, abajo, derecha + 20, abajo,
                    color=SUAVE, grosor=1.5, marcador="s"))
    cero, _ = coord(0, 0)
    s.append(linea(cero, arriba, cero, abajo, color=LINEA, grosor=1))
    for z in (-4, -2, 0, 2, 4):
        x, _ = coord(z, 0)
        s.append(linea(x, abajo + 5, x, abajo + 12, color=SUAVE, grosor=1.5))
        s.append(texto(x, abajo + 36, str(z).replace("-", "−"), tam=22))
    muestras = [-4 + k / 20 for k in range(161)]
    s.append(_curva([coord(z, 1 / (1 + math.exp(-z))) for z in muestras],
                    SERIE[1], grosor=4))
    x, y = coord(0, 0.5)
    s.append(punto(x, y, r=6, color=SERIE[1]))
    s.append(texto(x + 20, y + 36, "(0, 0.5)", tam=22, anclaje="start"))
    s.append(texto(W / 2, 441, "Score z", tam=25))
    s.append(texto(W / 2, 477, "z = α + βx", tam=24))
    s.append(texto(W / 2, 519, "Asíntotas: p = 0 y p = 1", color=SERIE[2], tam=22))
    s.append(cierre())
    return "".join(s)


def opt_clasificacion_log_loss():
    """Pérdidas calculadas en 0 < p < 1, con flechas hacia infinito."""
    W, H = 560, 570
    izquierda, derecha, arriba, abajo = 110, 514, 180, 420

    def coord(probabilidad, perdida):
        return (izquierda + probabilidad * (derecha - izquierda),
                abajo - perdida * (abajo - arriba) / 4)

    s = [marco(
        W, H,
        "Pérdida logarítmica frente al score normalizado p de clase 1: "
        "si y es 1, menos ln p decrece; "
        "si y es 0, menos ln uno menos p crece. Ambas divergen hacia "
        "infinito al asignar un score casi cero a la clase correcta",
        "La pérdida depende de la clase correcta",
        "Dos curvas calculadas para 0 < p < 1. El score normalizado p se "
        "interpreta como probabilidad estimada de clase 1 bajo el modelo. "
        "La verde, y = 1, representa "
        "-ln(p) y crece sin límite cuando p tiende a 0. La azul, y = 0, "
        "representa -ln(1-p) y crece sin límite cuando p tiende a 1. "
        "Las flechas superiores indican continuación sin cota, no un máximo. "
        "Los círculos abiertos en pérdida cero muestran límites no incluidos.",
    )]
    s.append(texto(W / 2, 36, "Pérdida logarítmica", tam=28, peso="700"))
    for y, color, etiqueta in ((77, SERIE[0], "y = 1:  −ln(p)"),
                               (111, SERIE[1], "y = 0:  −ln(1 − p)")):
        s.append(linea(82, y - 7, 123, y - 7, color=color, grosor=4))
        s.append(texto(142, y, etiqueta, tam=23, color=color, anclaje="start"))
    s.append('<g transform="rotate(-90 26 300)">'
             + texto(26, 300, "Pérdida (nats)", tam=22) + '</g>')
    for perdida in (0, 2, 4):
        _, y = coord(0, perdida)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 15, y + 7, str(perdida), tam=22, anclaje="end"))
    for probabilidad in (0, 1):
        x, _ = coord(probabilidad, 0)
        s.append(linea(x, arriba - 24, x, abajo, color=SUAVE,
                       grosor=1.5, guiones="6 7"))
    s.append(flecha(izquierda, abajo, derecha + 20, abajo,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(izquierda, abajo, izquierda, arriba - 44,
                    color=SUAVE, grosor=1.5, marcador="s"))
    for probabilidad in (0, 0.5, 1):
        x, _ = coord(probabilidad, 0)
        s.append(linea(x, abajo, x, abajo + 8, color=SUAVE, grosor=1.5))
        s.append(texto(x, abajo + 33, f"{probabilidad:g}", tam=22))
    # Muestreo uniforme en pérdida: resuelve bien las colas cerca de 0 y 1.
    # Los puntos se evalúan con ln; ninguno toca los extremos excluidos.
    perdidas = [0.001 + k * (4.5 - 0.001) / 300 for k in range(301)]
    for clase, color in ((1, SERIE[0]), (0, SERIE[1])):
        probabilidades = [math.exp(-t) if clase == 1 else -math.expm1(-t)
                          for t in perdidas]
        puntos = [coord(p, -math.log(p) if clase == 1 else -math.log1p(-p))
                  for p in probabilidades]
        s.append(_curva(puntos, color, grosor=4))
        # Una punta en la dirección de la tangente indica que la curva sigue.
        x, y = puntos[-1]
        s.append(f'<path d="M {x - 5:.1f} {y + 10:.1f} L {x:.1f} {y:.1f} '
                 f'L {x + 5:.1f} {y + 10:.1f}" fill="none" stroke="{color}" '
                 f'stroke-width="3"/>')
        extremo = 1 if clase == 1 else 0
        x0, y0 = coord(extremo, 0)
        s.append(f'<circle cx="{x0}" cy="{y0}" r="5" fill="{FONDO}" '
                 f'stroke="{color}" stroke-width="2.5"/>')
        s.append(texto(x + (22 if clase == 1 else -22), y + 6, "∞",
                       tam=27, color=color))
    s.append(texto(W / 2, 492, "Score de clase p", tam=25))
    s.append(texto(W / 2, 528, "p → 0:  −ln(p) → ∞", tam=22, color=SERIE[0]))
    s.append(texto(W / 2, 557, "p → 1:  −ln(1 − p) → ∞", tam=22, color=SERIE[1]))
    s.append(cierre())
    return "".join(s)



def opt_panaderia_criterios():
    """Tres criterios calculados para los 101 valores enteros de producción."""
    W, H = 560, 1152
    izquierda, derecha = 78, 514
    producciones = list(range(101))
    ganancias = [(8 * min(q, 20) - 2 * q, 8 * min(q, 80) - 2 * q)
                 for q in producciones]
    paneles = [
        ("1 · Promedio: datos 0.8 / 0.2", SERIE[1],
         [(8 * g1 + 2 * g2) / 10 for g1, g2 in ganancias]),
        ("2 · Supuesto uniforme 0.5 / 0.5", SERIE[0],
         [(g1 + g2) / 2 for g1, g2 in ganancias]),
        ("3 · Menor ganancia", SERIE[2],
         [min(g1, g2) for g1, g2 in ganancias]),
    ]
    s = [marco(
        W, H,
        "Tres paneles comparan la ganancia con probabilidades dadas, "
        "con uniformidad supuesta y en el peor caso. Las producciones "
        "óptimas son 20, 80 y 20 piezas respectivamente",
        "Producción óptima y valor máximo según el criterio",
        "Curvas calculadas para q entero de 0 a 100, con demandas 20 y 80, "
        "precio 8 y costo unitario 2. Los tres paneles comparten escala: "
        "producción en piezas y ganancia en pesos. Con probabilidades 0.8 y "
        "0.2, el máximo es 120 pesos con 20 piezas. Con el supuesto uniforme "
        "0.5 y 0.5, es 240 pesos con 80 piezas. La menor ganancia alcanza "
        "su máximo de 120 pesos con 20 piezas. Los segmentos solo unen "
        "los valores de las cantidades enteras.",
    )]
    s.append(texto(W / 2, 37, "Tres criterios de ganancia", tam=27, peso="700"))
    s.append(texto(W / 2, 73, "Producción y ganancia por criterio", tam=22, color=SUAVE))
    for k, (titulo, color, valores) in enumerate(paneles):
        inicio = 98 + 344 * k
        arriba, abajo = inicio + 102, inicio + 282

        def coord(q, ganancia):
            return (izquierda + q / 100 * (derecha - izquierda),
                    abajo - (ganancia + 60) / 360 * (abajo - arriba))

        maximo = max(valores)
        optimos = [q for q, valor in zip(producciones, valores) if valor == maximo]
        s.append(texto(W / 2, inicio + 22, titulo, tam=24, color=color, peso="600"))
        s.append(texto(W / 2, inicio + 55,
                       f"q* = {optimos[0]} piezas · máximo = {maximo:g} pesos", tam=22))
        s.append(texto(izquierda, inicio + 87, "Ganancia (pesos)",
                       tam=20, color=SUAVE, anclaje="start"))
        for ganancia in (-60, 0, 120, 240):
            _, y = coord(0, ganancia)
            s.append(linea(izquierda, y, derecha, y,
                           color=SUAVE if ganancia == 0 else LINEA, grosor=1))
            s.append(texto(izquierda - 13, y + 7, str(ganancia).replace("-", "−"),
                           tam=20, anclaje="end"))
        s.append(linea(izquierda, arriba, izquierda, abajo, color=SUAVE, grosor=1.5))
        s.append(linea(izquierda, abajo, derecha, abajo, color=SUAVE, grosor=1.5))
        for q in (0, 20, 80, 100):
            x, _ = coord(q, 0)
            s.append(linea(x, abajo, x, abajo + 7, color=SUAVE, grosor=1.5))
            s.append(texto(x, abajo + 28, str(q), tam=21))
        puntos = [coord(q, valor) for q, valor in zip(producciones, valores)]
        s.append(_curva(puntos, color, grosor=3.5))
        for q in optimos:
            x, y = coord(q, maximo)
            s.append(linea(x, y, x, abajo, color=color, grosor=1.5, guiones="5 6"))
            s.append(punto(x, y, r=6, color=color))
        s.append(texto(W / 2, abajo + 56, "q (piezas)", tam=23))
    s.append(cierre())
    return "".join(s)




# Datos didácticos compartidos por las tres figuras de regresión.
_REG_X = tuple(map(F, range(1, 7)))
_REG_Y = tuple(map(F, (15, 17, 23, 25, 31, 33)))
_REG_X_VAL = tuple(F(k, 2) for k in (3, 5, 7, 9, 11))
_REG_Y_VAL = tuple(map(F, (16, 20, 24, 28, 32)))


def _regresion_ajuste(grado):
    """OLS exacto para estas seis observaciones, solo para generar la figura."""
    # Sistema de momentos resuelto con fracciones: no es una recomendación
    # de resolver ecuaciones normales con flotantes en aplicaciones reales.
    matriz = [[sum(x ** (i + j) for x in _REG_X) for j in range(grado + 1)]
              + [sum(x ** i * y for x, y in zip(_REG_X, _REG_Y))]
              for i in range(grado + 1)]
    for j in range(grado + 1):
        pivote = matriz[j][j]
        matriz[j] = [v / pivote for v in matriz[j]]
        for i in range(grado + 1):
            if i != j:
                factor = matriz[i][j]
                matriz[i] = [v - factor * w for v, w in zip(matriz[i], matriz[j])]
    return tuple(fila[-1] for fila in matriz)


def _regresion_prediccion(coeficientes, x):
    return sum(c * x ** j for j, c in enumerate(coeficientes))


def _regresion_rmse(coeficientes, xs, ys):
    return math.sqrt(float(sum((y - _regresion_prediccion(coeficientes, x)) ** 2
                               for x, y in zip(xs, ys)) / len(xs)))


def opt_regresion_residuos():
    W, H = 560, 652
    izquierda, derecha = 110, 514
    ax = lambda x: izquierda + (float(x) - 1) / 5 * (derecha - izquierda)
    ay = lambda y: 470 - (float(y) - 10) / 26 * 300
    s = [marco(W, H,
        "Tiempos de entrega observados, recta de ejemplo y residuos verticales",
        "Una predicción y su residuo",
        "Distancia en kilómetros, tiempo en minutos. Seis observaciones en "
        "x=1,2,3,4,5,6 con tiempos 15,17,23,25,31,33. La recta elegida "
        "y estimada=10+4x es un ejemplo, no la recta óptima de mínimos cuadrados. "
        "Los residuos observado menos predicho son 1,-1,1,-1,1,-1 minutos. "
        "Se destaca el tercer residuo: 23 menos 22 es un minuto.")]
    s.append(texto(W / 2, 36, "Una predicción y su residuo", tam=27, peso="700"))
    s.append(texto(W / 2, 73, "Recta de ejemplo: ŷ = 10 + 4x", tam=23, color=ACENTO))
    s.append(texto(W / 2, 109, "Recta elegida para ilustrar los residuos.", tam=22, color=SUAVE))
    s.append('<g transform="rotate(-90 26 320)">'
             + texto(26, 320, "Tiempo de entrega (min)", tam=22) + '</g>')
    for valor in (10, 15, 20, 25, 30, 35):
        y = ay(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 14, y + 7, str(valor), tam=22, anclaje="end"))
    s.append(flecha(izquierda, 470, izquierda, 157, color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(izquierda, 470, derecha + 20, 470, color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(ax(1), ay(14), ax(6), ay(34), color=ACENTO, grosor=3))
    for i, (x, y) in enumerate(zip(_REG_X, _REG_Y)):
        xp, observado, predicho = ax(x), ay(y), ay(10 + 4 * x)
        color = SERIE[2] if i == 2 else SUAVE
        s.append(linea(xp, observado, xp, predicho, color=color, grosor=4))
        s.append(f'<rect x="{xp - 5}" y="{predicho - 5}" width="10" height="10" '
                 f'fill="{SERIE[1]}"/>')
        s.append(punto(xp, observado, r=5, color=SERIE[0]))
        s.append(linea(xp, 470, xp, 478, color=SUAVE, grosor=1.5))
        s.append(texto(xp, 505, str(x), tam=22))
    s.append(linea(280, 405, ax(3) + 5, ay(F(45, 2)), color=SERIE[2], grosor=1.5))
    s.append(texto(302, 437, "e₃ = 23 − 22 = +1 min", tam=22, color=SERIE[2]))
    s.append(texto(W / 2, 544, "Distancia x (km)", tam=24))
    s.append(punto(120, 582, r=5, color=SERIE[0]))
    s.append(texto(137, 589, "Observado yᵢ", tam=22, anclaje="start"))
    s.append(f'<rect x="318" y="577" width="10" height="10" fill="{SERIE[1]}"/>')
    s.append(texto(339, 589, "Predicho ŷᵢ", tam=22, anclaje="start"))
    s.append(texto(W / 2, 632, "Residuo: eᵢ = yᵢ − ŷᵢ (min)", tam=23, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_regresion_perdidas():
    W, H = 560, 980
    izquierda, derecha = 110, 514
    ax = lambda e: izquierda + (e + 4) / 8 * (derecha - izquierda)
    s = [marco(W, H,
        "Dos pérdidas puntuales frente al residuo: valor absoluto y cuadrado",
        "Cómo pesa el tamaño del error",
        "Arriba, valor absoluto del residuo, con ambos ejes en minutos. "
        "Abajo, residuo al cuadrado, con eje horizontal en minutos y "
        "vertical en minutos cuadrados. Las escalas verticales son diferentes. "
        "RMSE no es una pérdida puntual: es la raíz del promedio de cuadrados.")]
    s.append(texto(W / 2, 36, "Cómo pesa el tamaño del error", tam=26, peso="700"))
    s.append(texto(W / 2, 74, "Dos pérdidas; distintas unidades", tam=22, color=SUAVE))
    for panel, (titulo, etiqueta, funcion, maximo, ticks, color) in enumerate((
        ("Valor absoluto |e|", "Pérdida |e| (min)", abs, 4, (0, 1, 2, 3, 4), SERIE[1]),
        ("Error al cuadrado e²", "Pérdida e² (min²)", lambda e: e * e, 16, (0, 4, 8, 12, 16), ACENTO),
    )):
        abajo = 400 + panel * 410
        ay = lambda valor: abajo - valor / maximo * 220
        s.append(texto(W / 2, abajo - 267, titulo, tam=25, color=color))
        centro = abajo - 110
        s.append(f'<g transform="rotate(-90 26 {centro})">'
                 + texto(26, centro, etiqueta, tam=22) + '</g>')
        for valor in ticks:
            y = ay(valor)
            s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
            s.append(texto(izquierda - 14, y + 7, str(valor), tam=22, anclaje="end"))
        s.append(flecha(izquierda, abajo, izquierda, abajo - 235,
                        color=SUAVE, grosor=1.5, marcador="s"))
        s.append(flecha(izquierda, abajo, derecha + 20, abajo,
                        color=SUAVE, grosor=1.5, marcador="s"))
        for e in (-4, -2, 0, 2, 4):
            x = ax(e)
            s.append(linea(x, abajo, x, abajo + 8, color=SUAVE, grosor=1.5))
            s.append(texto(x, abajo + 35, str(e).replace("-", "−"), tam=22))
        s.append(texto(W / 2, abajo + 74, "Residuo e (min)", tam=24))
        s.append(_curva([(ax(e / 50), ay(funcion(e / 50))) for e in range(-200, 201)],
                         color, grosor=3.5))
    s.append(texto(W / 2, 932, "RMSE: raíz del promedio de cuadrados.", tam=22, color=SUAVE))
    s.append(texto(W / 2, 965, "No es una pérdida de un solo caso.", tam=22, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_regresion_grado():
    W, H = 560, 1660
    izquierda, derecha = 110, 514
    ajustes = {n: _regresion_ajuste(n) for n in range(1, 6)}
    ax = lambda x: izquierda + (float(x) - 1) / 5 * (derecha - izquierda)
    s = [marco(W, H,
        "Ajustes polinomiales de grados uno, tres y cinco, y RMSE por grado",
        "Ajustar mejor no siempre generaliza mejor",
        "Tres paneles muestran ajustes OLS calculados solo con seis casos de "
        "entrenamiento; cinco casos de validación independientes solo evalúan "
        "los ajustes. Se comparan grados uno, tres y cinco en las mismas escalas. "
        "El último panel muestra RMSE de entrenamiento y validación para los "
        "grados discretos uno a cinco, sin unirlos como si el grado fuera continuo. "
        "El grado cinco interpola entrenamiento, pero aquí su error de validación "
        "es mayor. Los grados uno y dos empatan en ambos errores.")]
    s.append(texto(W / 2, 35, "Más grado, ¿mejor predicción?", tam=26, peso="700"))
    s.append(texto(W / 2, 72, "Ajuste solo con entrenamiento", tam=22, color=SUAVE))
    s.append(punto(113, 109, r=5, color=SERIE[0]))
    s.append(texto(129, 116, "Entrenamiento", tam=22, anclaje="start"))
    s.append(f'<path d="M 346 102 L 353 109 L 346 116 L 339 109 Z" fill="{SERIE[1]}"/>')
    s.append(texto(362, 116, "Validación", tam=22, anclaje="start"))
    for panel, grado in enumerate((1, 3, 5)):
        abajo = 402 + panel * 350
        ay = lambda y: abajo - (float(y) - 10) / 30 * 220
        centro = abajo - 110
        s.append(texto(W / 2, abajo - 251, f"Grado N = {grado}", tam=25, color=ACENTO))
        s.append(f'<g transform="rotate(-90 26 {centro})">'
                 + texto(26, centro, "Tiempo (min)", tam=22) + '</g>')
        for valor in (10, 20, 30, 40):
            y = ay(valor)
            s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
            s.append(texto(izquierda - 14, y + 7, str(valor), tam=22, anclaje="end"))
        s.append(flecha(izquierda, abajo, izquierda, abajo - 231,
                        color=SUAVE, grosor=1.5, marcador="s"))
        s.append(flecha(izquierda, abajo, derecha + 20, abajo,
                        color=SUAVE, grosor=1.5, marcador="s"))
        for x in range(1, 7):
            s.append(linea(ax(x), abajo, ax(x), abajo + 7, color=SUAVE, grosor=1.5))
            s.append(texto(ax(x), abajo + 32, str(x), tam=22))
        s.append(texto(W / 2, abajo + 65, "Distancia x (km)", tam=23))
        muestras = [F(1) + F(k, 60) for k in range(301)]
        s.append(_curva([(ax(x), ay(_regresion_prediccion(ajustes[grado], x)))
                         for x in muestras], ACENTO, grosor=3))
        for x, y in zip(_REG_X, _REG_Y):
            s.append(punto(ax(x), ay(y), r=5, color=SERIE[0]))
        for x, y in zip(_REG_X_VAL, _REG_Y_VAL):
            xp, yp = ax(x), ay(y)
            s.append(f'<path d="M {xp} {yp - 6} L {xp + 6} {yp} L {xp} {yp + 6} '
                     f'L {xp - 6} {yp} Z" fill="{SERIE[1]}"/>')
    abajo = 1497
    nx = lambda n: izquierda + (n - 1) / 4 * (derecha - izquierda)
    ey = lambda error: abajo - error / 2 * 220
    s.append(texto(W / 2, 1220, "RMSE por grado", tam=25))
    s.append(texto(W / 2, 1255, "Validación evalúa; no ajusta coeficientes.", tam=22, color=SUAVE))
    s.append('<g transform="rotate(-90 26 1387)">'
             + texto(26, 1387, "RMSE (min)", tam=22) + '</g>')
    for valor in (0, .5, 1, 1.5, 2):
        y = ey(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 14, y + 7, f"{valor:g}", tam=22, anclaje="end"))
    s.append(flecha(izquierda, abajo, izquierda, 1268, color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(izquierda, abajo, derecha, abajo, color=SUAVE, grosor=1.5))
    for n, coef in ajustes.items():
        x = nx(n)
        s.append(linea(x, abajo, x, abajo + 7, color=SUAVE, grosor=1.5))
        s.append(texto(x, abajo + 34, str(n), tam=22))
        s.append(punto(x, ey(_regresion_rmse(coef, _REG_X, _REG_Y)), r=6, color=SERIE[0]))
        y = ey(_regresion_rmse(coef, _REG_X_VAL, _REG_Y_VAL))
        s.append(f'<path d="M {x} {y - 7} L {x + 7} {y} L {x} {y + 7} '
                 f'L {x - 7} {y} Z" fill="{SERIE[1]}"/>')
    s.append(texto(W / 2, 1570, "Grado N (entero)", tam=24))
    s.append(texto(W / 2, 1612, "Grado 5: error cero al entrenar;", tam=22, color=SUAVE))
    s.append(texto(W / 2, 1645, "mayor error de validación en estos datos.", tam=22, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_clasificacion_accuracy():
    """Accuracy calculada en un corte con beta fija, sin unir los saltos."""
    W, H = 560, 690
    izquierda, derecha = 110, 514
    casos = [(0, 0), (1, 0), (2, 1), (3, 1)]
    beta = 1

    def accuracy(alfa):
        return sum(int(alfa + beta * x >= 0) == y for x, y in casos) / len(casos)

    def ax(alfa):
        return izquierda + (alfa + 4) / 5 * (derecha - izquierda)

    def ay(valor):
        return 450 - 240 * valor

    s = [marco(
        W, H,
        "Accuracy frente al intercepto alfa para cuatro casos, con beta fija en uno",
        "La accuracy cambia a saltos",
        "Casos x=(0,1,2,3), y=(0,0,1,1). Predicción uno si alfa+x es "
        "mayor o igual a cero. Beta se fija en uno solo para visualizar un "
        "corte del problema original, donde alfa y beta son libres. La "
        "accuracy vale un medio antes de -3, tres cuartos en [-3,-2), "
        "uno en [-2,-1), tres cuartos en [-1,0) y un medio desde cero. "
        "Los círculos cerrados incluyen el extremo y los abiertos lo "
        "excluyen. Alfa=-2.5 da tres cuartos. La ventana es [-4,1], "
        "pero alfa tiene dominio real. No son iteraciones de entrenamiento.",
    )]
    s.append(texto(W / 2, 36, "La accuracy cambia a saltos", tam=27, peso="700"))
    s.append(texto(W / 2, 72, "β = 1 · cuatro casos", tam=23, color=SUAVE))
    s.append(texto(W / 2, 108, "x = (0, 1, 2, 3)", tam=22))
    s.append(texto(W / 2, 139, "y = (0, 0, 1, 1)", tam=22))
    s.append('<g transform="rotate(-90 26 330)">'
             + texto(26, 330, "Aciertos (proporción)", tam=22) + '</g>')
    for valor, etiqueta in ((0, "0"), (.25, "1/4"), (.5, "1/2"), (.75, "3/4"), (1, "1")):
        y = ay(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 14, y + 7, etiqueta, tam=22, anclaje="end"))
    s.append(flecha(izquierda, 450, izquierda, 195,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(izquierda, 450, derecha + 20, 450,
                    color=SUAVE, grosor=1.5, marcador="s"))
    for alfa in (-4, -3, -2, -1, 0, 1):
        x = ax(alfa)
        s.append(linea(x, 450, x, 458, color=SUAVE, grosor=1.5))
        s.append(texto(x, 485, str(alfa).replace("-", "−"), tam=22))
    s.append(texto(W / 2, 524, "α (intercepto)", tam=24))

    cortes = sorted(-x / beta for x, _ in casos)
    bordes = [-4] + cortes + [1]
    for i, (a, b) in enumerate(zip(bordes, bordes[1:])):
        valor = accuracy((a + b) / 2)
        y = ay(valor)
        color = SERIE[1] if valor == 1 else ACENTO
        s.append(linea(ax(a), y, ax(b), y, color=color, grosor=4))
        if i > 0:
            s.append(punto(ax(a), y, r=6, color=color))
        if i < len(bordes) - 2:
            s.append(f'<circle cx="{ax(b)}" cy="{y}" r="6" '
                     f'fill="{FONDO}" stroke="{color}" stroke-width="2.5"/>')
    # Las colas continúan fuera de la ventana; no son extremos del dominio.
    for alfa, lado in ((-4, 1), (1, -1)):
        x, y = ax(alfa), ay(accuracy(alfa))
        s.append(f'<path d="M {x + lado * 10} {y - 5} L {x} {y} '
                 f'L {x + lado * 10} {y + 5}" fill="none" '
                 f'stroke="{ACENTO}" stroke-width="3"/>')
    s.append(texto(ax(-1.5), 184, "A = 1 en [−2, −1)", tam=22, color=SERIE[1]))
    x, y = ax(-2.5), ay(accuracy(-2.5))
    s.append(linea(x, y + 7, 217, 290, color=SERIE[0], grosor=1.5))
    s.append(punto(x, y, r=6, color=SERIE[0]))
    s.append(texto(214, 315, "α = −2.5: A = 3/4", tam=22, color=SERIE[0]))
    s.append(punto(122, 567, r=6, color=TEXTO))
    s.append(texto(140, 574, "Incluido", tam=22, anclaje="start"))
    s.append(f'<circle cx="325" cy="567" r="6" fill="{FONDO}" '
             f'stroke="{TEXTO}" stroke-width="2.5"/>')
    s.append(texto(343, 574, "Excluido", tam=22, anclaje="start"))
    s.append(texto(W / 2, 615, "α varía; β = 1 solo en esta vista.", tam=22, color=SUAVE))
    s.append(texto(W / 2, 646, "No son iteraciones de entrenamiento.", tam=22, color=SUAVE))
    s.append(texto(W / 2, 677, "Ventana: [−4, 1]; dominio: α real.", tam=22, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_clasificacion_alfa():
    """Pérdida y aciertos frente al intercepto real, con beta fija en cero."""
    W, H = 560, 1158
    izquierda, derecha = 110, 514
    elegidas = [(0.49, "0.49", SERIE[0]),
                (2 / 3, "2/3", SERIE[1]),
                (0.9, "0.9", SERIE[2])]

    def perdida(alfa):
        return math.log1p(math.exp(alfa)) - (2 / 3) * alfa

    def ax(alfa):
        return izquierda + (alfa + 4) / 8 * (derecha - izquierda)

    def ly(valor):
        return 410 - valor / 3 * 220

    def ay(valor):
        return 790 - valor * 220

    s = [marco(
        W, H,
        "Dos paneles frente al intercepto alfa, con beta cero: pérdida "
        "promedio y proporción de aciertos. Tres reglas elegidas a mano, "
        "no iteraciones de entrenamiento",
        "El intercepto cambia la regla constante",
        "Eje horizontal alfa real, mostrado de -4 a 4, con flechas de "
        "continuación. Dos tercios de los casos son de clase 1. Arriba, "
        "L(alfa,0) = ln(1+exp(alfa)) - dos tercios por alfa, en nats por "
        "caso. No hay asíntotas verticales: la curva continúa hacia ambos "
        "lados fuera de la ventana. Abajo, accuracy es un tercio para alfa "
        "negativa y dos tercios para alfa mayor o igual a cero. En cero, "
        "el punto inferior está abierto y el superior cerrado. Las marcas "
        "son ln(0.49/0.51), ln(2) y ln(9), correspondientes a los scores "
        "constantes 0.49, dos tercios y 0.9. Sus pérdidas son 0.700, 0.637 "
        "y 0.838; no se presentan como óptimos del modelo completo.",
    )]
    s.append(texto(W / 2, 36, "El intercepto cambia la regla", tam=27, peso="700"))
    s.append(texto(W / 2, 70, "β = 0 · 2/3 de casos con clase 1", tam=22, color=SUAVE))
    s.append(texto(W / 2, 102, "Tres valores de α elegidos a mano", tam=22))
    s.append(texto(W / 2, 150, "Pérdida promedio", tam=25, color=ACENTO))
    s.append('<g transform="rotate(-90 26 300)">'
             + texto(26, 300, "Pérdida (nats/caso)", tam=22) + '</g>')
    for valor in (0, 1, 2, 3):
        y = ly(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 14, y + 7, str(valor), tam=22, anclaje="end"))
    s.append(flecha(izquierda, 410, izquierda, 178,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(izquierda, 410, derecha, 410, color=SUAVE, grosor=1.5))
    s.append(flecha(derecha, 410, derecha + 20, 410,
                    color=SUAVE, grosor=1.5, marcador="s"))
    muestras = [-4 + k / 50 for k in range(401)]
    puntos = [(ax(alfa), ly(perdida(alfa))) for alfa in muestras]
    s.append(_curva(puntos, ACENTO, grosor=3.5))
    # Las puntas siguen las tangentes en los bordes finitos de la ventana.
    # No hay asíntotas verticales ni puntos abiertos en alfa = -4 o alfa = 4.
    for extremo, interior in ((puntos[0], puntos[1]), (puntos[-1], puntos[-2])):
        x, y = extremo
        dx, dy = x - interior[0], y - interior[1]
        largo = math.hypot(dx, dy)
        ux, uy = dx / largo, dy / largo
        x1, y1 = x - 10 * ux - 5 * uy, y - 10 * uy + 5 * ux
        x2, y2 = x - 10 * ux + 5 * uy, y - 10 * uy - 5 * ux
        s.append(f'<path d="M {x1:.1f} {y1:.1f} L {x:.1f} {y:.1f} '
                 f'L {x2:.1f} {y2:.1f}" fill="none" stroke="{ACENTO}" '
                 f'stroke-width="3"/>')
    # Anotaciones separadas del tick alfa = 0 y entre sí.
    rotulos = [(228, 338, 260, 345), (366, 397, 354, 377), (470, 317, 450, 328)]
    for (p, _, color), (tx, ty, lx, ly_rotulo) in zip(elegidas, rotulos):
        alfa = math.log(p / (1 - p))
        x, y = ax(alfa), ly(perdida(alfa))
        s.append(linea(lx, ly_rotulo, x, y, color=color, grosor=1.5))
        s.append(punto(x, y, r=6, color=color))
        etiqueta = f"{alfa:.3f}".replace("-", "−")
        s.append(texto(tx, ty, etiqueta, tam=22, color=color))
    for alfa in (-4, -2, 0, 2, 4):
        x = ax(alfa)
        s.append(linea(x, 410, x, 418, color=SUAVE, grosor=1.5))
        s.append(texto(x, 445, str(alfa).replace("-", "−"), tam=22))
    s.append(texto(W / 2, 484, "α (intercepto)", tam=24))

    s.append(texto(W / 2, 534, "Proporción de aciertos", tam=25))
    s.append('<g transform="rotate(-90 26 680)">'
             + texto(26, 680, "Aciertos (proporción)", tam=22) + '</g>')
    for valor, etiqueta in ((0, "0"), (1 / 3, "1/3"), (2 / 3, "2/3"), (1, "1")):
        y = ay(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 14, y + 7, etiqueta, tam=22, anclaje="end"))
    s.append(flecha(izquierda, 790, izquierda, 558,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(izquierda, 790, derecha, 790, color=SUAVE, grosor=1.5))
    s.append(flecha(derecha, 790, derecha + 20, 790,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(ax(-4), ay(1 / 3), ax(0), ay(1 / 3), color=TEXTO, grosor=4))
    s.append(linea(ax(0), ay(2 / 3), ax(4), ay(2 / 3), color=TEXTO, grosor=4))
    # Continuación horizontal de ambos escalones hacia alfa infinita.
    for x, y, lado in ((ax(-4), ay(1 / 3), 1), (ax(4), ay(2 / 3), -1)):
        s.append(f'<path d="M {x + lado * 10} {y - 5} L {x} {y} '
                 f'L {x + lado * 10} {y + 5}" fill="none" stroke="{TEXTO}" '
                 f'stroke-width="3"/>')
    s.append(f'<circle cx="{ax(0)}" cy="{ay(1 / 3)}" r="6" '
             f'fill="{FONDO}" stroke="{TEXTO}" stroke-width="2.5"/>')
    s.append(punto(ax(0), ay(2 / 3), r=6, color=TEXTO))
    s.append(texto(ax(-2), ay(1 / 3) - 22, "α < 0", tam=22))
    s.append(texto(ax(2), ay(2 / 3) - 22, "α ≥ 0", tam=22))
    for alfa in (-4, -2, 0, 2, 4):
        x = ax(alfa)
        s.append(linea(x, 790, x, 798, color=SUAVE, grosor=1.5))
        s.append(texto(x, 825, str(alfa).replace("-", "−"), tam=22))
    s.append(texto(W / 2, 864, "α (intercepto)", tam=24))
    s.append(texto(W / 2, 905, "Tres reglas; no son iteraciones", tam=22, color=SUAVE))
    for k, (p, etiqueta, color) in enumerate(elegidas):
        alfa = math.log(p / (1 - p))
        etiqueta_alfa = f"{alfa:.4f}".replace("-", "−")
        aciertos = "1/3" if alfa < 0 else "2/3"
        s.append(texto(W / 2, 939 + 63 * k,
                       f"α ≈ {etiqueta_alfa} · p = {etiqueta}", tam=22, color=color))
        s.append(texto(W / 2, 967 + 63 * k,
                       f"Pérdida {perdida(alfa):.3f} · aciertos {aciertos}", tam=22, color=color))
    s.append(texto(W / 2, 1134, "Ventana: [−4, 4]; dominio: α real.", tam=22, color=SUAVE))
    s.append(cierre())
    return "".join(s)


def opt_clasificacion_proxy():
    """Compara pérdida y aciertos de tres reglas constantes elegidas a mano."""
    W, H = 560, 1018
    izquierda, derecha = 110, 514
    ancho = derecha - izquierda
    elegidas = [(0.49, "0.49", SERIE[0]),
                (2 / 3, "2/3", SERIE[1]),
                (0.9, "0.9", SERIE[2])]

    def perdida(p):
        return -(2 / 3) * math.log(p) - (1 / 3) * math.log1p(-p)

    def px(p):
        return izquierda + ancho * p

    def ly(valor):
        return 400 - valor / 1.6 * 210

    def ay(valor):
        return 750 - valor * 200

    s = [marco(
        W, H,
        "Dos paneles con el mismo eje p comparan pérdida y aciertos de reglas "
        "constantes, con beta cero y dos tercios de casos de clase 1. "
        "Los scores 0.49, dos tercios y 0.9 se eligieron a mano",
        "Tres reglas constantes, dos medidas distintas",
        "Arriba, curva calculada L constante de p igual a menos dos tercios "
        "por ln p menos un tercio por ln uno menos p, en 0 < p < 1. "
        "Las flechas indican divergencia hacia infinito en ambos extremos. "
        "Las tres marcas representan reglas elegidas a mano, no iteraciones "
        "de entrenamiento. Sus pérdidas son 0.700, 0.637 y 0.838. "
        "Abajo, accuracy vale un tercio si p < 0.5 y dos tercios si p >= 0.5. "
        "En p = 0.5 el punto inferior está abierto y el superior cerrado; "
        "el empate anuncia clase 1. Los extremos p = 0 y p = 1 están excluidos. "
        "La comparación solo abarca reglas constantes, no óptimos del modelo completo.",
    )]
    s.append(texto(W / 2, 36, "Tres reglas constantes", tam=28, peso="700"))
    s.append(texto(W / 2, 70, "β = 0 · 2/3 de casos con clase 1", tam=22, color=SUAVE))
    s.append(texto(W / 2, 101, "Scores p elegidos a mano", tam=23))
    s.append(texto(W / 2, 148, "Pérdida promedio", tam=25, color=ACENTO))
    s.append('<g transform="rotate(-90 26 295)">'
             + texto(26, 295, "Pérdida (nats/caso)", tam=22) + '</g>')
    for valor in (0, 0.8, 1.6):
        y = ly(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 13, y + 7, f"{valor:g}", tam=21, anclaje="end"))
    for p in (0, 1):
        s.append(linea(px(p), 176, px(p), 400, color=SUAVE,
                       grosor=1.5, guiones="6 7"))
    s.append(flecha(izquierda, 400, derecha + 20, 400,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(izquierda, 400, izquierda, 176,
                    color=SUAVE, grosor=1.5, marcador="s"))
    muestras = [k / 5000 for k in range(1, 5000)]
    puntos = [(px(p), ly(perdida(p))) for p in muestras if perdida(p) <= 1.75]
    s.append(_curva(puntos, ACENTO, grosor=3.5))
    # Puntas siguiendo la tangente exterior: el recorte no es un máximo finito.
    for extremo, interior, lado in ((puntos[0], puntos[1], 1),
                                     (puntos[-1], puntos[-2], -1)):
        x, y = extremo
        dx, dy = x - interior[0], y - interior[1]
        largo = math.hypot(dx, dy)
        ux, uy = dx / largo, dy / largo
        x1, y1 = x - 10 * ux - 5 * uy, y - 10 * uy + 5 * ux
        x2, y2 = x - 10 * ux + 5 * uy, y - 10 * uy - 5 * ux
        s.append(f'<path d="M {x1:.1f} {y1:.1f} L {x:.1f} {y:.1f} '
                 f'L {x2:.1f} {y2:.1f}" fill="none" stroke="{ACENTO}" '
                 f'stroke-width="3"/>')
        s.append(texto(x + lado * 22, y + 5, "∞", tam=27, color=ACENTO))
    for p, etiqueta, color in elegidas:
        x, y = px(p), ly(perdida(p))
        s.append(punto(x, y, r=6, color=color))
        # Los valores elegidos se rotulan dentro del panel, lejos del tick 0.5.
        s.append(texto(x, y + (34 if p < 0.8 else -22), etiqueta, tam=22, color=color))
    for p in (0, 0.5, 1):
        x = px(p)
        s.append(linea(x, 400, x, 408, color=SUAVE, grosor=1.5))
        s.append(texto(x, 435, f"{p:g}", tam=22))
    s.append(texto(W / 2, 474, "p (score constante)", tam=24))

    s.append(texto(W / 2, 521, "Proporción de aciertos", tam=25))
    s.append('<g transform="rotate(-90 26 650)">'
             + texto(26, 650, "Aciertos (proporción)", tam=22) + '</g>')
    for valor, etiqueta in ((0, "0"), (1 / 3, "1/3"), (2 / 3, "2/3"), (1, "1")):
        y = ay(valor)
        s.append(linea(izquierda, y, derecha, y, color=LINEA, grosor=1))
        s.append(texto(izquierda - 13, y + 7, etiqueta, tam=21, anclaje="end"))
    s.append(flecha(izquierda, 750, izquierda, 538,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(flecha(izquierda, 750, derecha + 20, 750,
                    color=SUAVE, grosor=1.5, marcador="s"))
    s.append(linea(px(0), ay(1 / 3), px(0.5), ay(1 / 3), color=TEXTO, grosor=4))
    s.append(linea(px(0.5), ay(2 / 3), px(1), ay(2 / 3), color=TEXTO, grosor=4))
    # Los círculos abiertos distinguen extremos excluidos y el salto en 0.5.
    for p, valor in ((0, 1 / 3), (0.5, 1 / 3), (1, 2 / 3)):
        s.append(f'<circle cx="{px(p)}" cy="{ay(valor)}" r="6" '
                 f'fill="{FONDO}" stroke="{TEXTO}" stroke-width="2.5"/>')
    s.append(punto(px(0.5), ay(2 / 3), r=6, color=TEXTO))
    s.append(texto(px(0.24), ay(1 / 3) - 22, "p < 0.5", tam=22))
    s.append(texto(px(0.75), ay(2 / 3) - 22, "p ≥ 0.5", tam=22))
    for p in (0, 0.5, 1):
        x = px(p)
        s.append(linea(x, 750, x, 758, color=SUAVE, grosor=1.5))
        s.append(texto(x, 785, f"{p:g}", tam=22))
    s.append(texto(W / 2, 824, "p (score constante)", tam=24))
    s.append(texto(W / 2, 868, "Mismas reglas, dos medidas", tam=22, color=SUAVE))
    for k, (p, etiqueta, color) in enumerate(elegidas):
        aciertos = "1/3" if p < 0.5 else "2/3"
        s.append(texto(W / 2, 904 + 34 * k,
                       f"p = {etiqueta} · pérdida {perdida(p):.3f} · aciertos {aciertos}",
                       tam=22, color=color))
    s.append(texto(W / 2, 1006, "Las marcas no son iteraciones.", tam=21, color=SUAVE))
    s.append(cierre())
    return "".join(s)



def opt_juego_turnos():
    """Árbol de nueve estados; solo las hojas llevan utilidades conocidas."""
    W, H = 560, 802
    # id: (x, y, anchura, jugador o None, utilidad terminal o None, rótulo)
    nodos = {
        "s0": (280, 115, 174, "MAX", None, "s₀ · inicio"),
        "s1": (120, 280, 174, "MIN", None, "s₁"),
        "s2": (405, 280, 174, "MIN", None, "s₂"),
        "s3": (455, 455, 174, "MAX", None, "s₃"),
        "t1": (60, 455, 100, None, 1, "t₁"),
        "t2": (180, 455, 100, None, -1, "t₂"),
        "t3": (300, 455, 100, None, 1, "t₃"),
        "t4": (370, 655, 100, None, -1, "t₄"),
        "t5": (500, 655, 100, None, 1, "t₅"),
    }
    # origen, destino, acción y posición de su etiqueta, lejos del trazo.
    aristas = [
        ("s0", "s1", "Guardar", 126, 202),
        ("s0", "s2", "Sacrificar", 433, 202),
        ("s1", "t1", "I", 61, 374),
        ("s1", "t2", "D", 189, 374),
        ("s2", "t3", "I", 330, 374),
        ("s2", "s3", "D", 480, 374),
        ("s3", "t4", "X", 390, 568),
        ("s3", "t5", "Y", 510, 568),
    ]
    s = [marco(
        W, H,
        "Árbol de nueve estados. En s0 elegimos Guardar o Sacrificar. "
        "El rival responde I o D. Tras Sacrificar y D volvemos a elegir: "
        "X lleva a derrota y Y a victoria",
        "Una decisión más después de Sacrificar y D",
        "Cuatro estados de decisión y cinco finales, unidos por ocho "
        "acciones. s0 es nuestro turno MAX; Guardar lleva a s1 y Sacrificar "
        "a s2, ambos del rival MIN. Desde s1, I llega a t1 con utilidad +1 "
        "y D a t2 con -1. Desde s2, I llega a t3 con +1 y D a s3, nuestro "
        "turno MAX. Desde s3, X llega a t4 con -1 e Y a t5 con +1. "
        "Todas las utilidades son nuestras; los estados intermedios no "
        "llevan valores anticipados. Una partida sigue un único camino "
        "desde s0 hasta una hoja.",
    )]
    s.append(texto(W / 2, 37, "Una decisión más tras S → D", tam=25, peso="700"))
    for origen, destino, accion, lx, ly in aristas:
        x1, y1, _, jugador1, _, _ = nodos[origen]
        x2, y2, _, jugador2, _, _ = nodos[destino]
        medio1 = 45 if jugador1 else 35
        medio2 = 45 if jugador2 else 35
        s.append(flecha(x1, y1 + medio1 + 1, x2, y2 - medio2 - 5,
                        color=SUAVE, grosor=2.5, marcador="s"))
        s.append(texto(lx, ly, accion, tam=24))
    for x, y, ancho, jugador, utilidad, rotulo in nodos.values():
        if jugador:
            color = SERIE[1] if jugador == "MAX" else SERIE[2]
            s.append(caja(x - ancho / 2, y - 45, ancho, 90,
                          relleno=mezclar(color, 0.09), borde=color, radio=12))
            s.append(texto(x, y - 18, rotulo, tam=24, peso="600"))
            s.append(texto(x, y + 10, "Nuestro turno" if jugador == "MAX" else "Turno rival",
                           tam=23))
            s.append(texto(x, y + 35, jugador, tam=21, color=color, peso="600"))
        else:
            color = SERIE[0] if utilidad > 0 else ALARMA
            s.append(caja(x - ancho / 2, y - 35, ancho, 70,
                          relleno=mezclar(color, 0.09), borde=color, radio=10))
            s.append(texto(x, y - 8, rotulo, tam=24))
            valor = f"+{utilidad}" if utilidad > 0 else str(utilidad).replace("-", "−")
            s.append(texto(x, y + 21, f"U = {valor}", tam=23, color=color, peso="600"))
    s.append(texto(W / 2, 751, "Hojas: utilidad para nosotros", tam=23))
    s.append(texto(W / 2, 785, "Una partida recorre un solo camino.", tam=22, color=SUAVE))
    s.append(cierre())
    return "".join(s)


DIAGRAMAS = {
    "opt-regresion-residuos": opt_regresion_residuos,
    "opt-regresion-perdidas": opt_regresion_perdidas,
    "opt-regresion-grado": opt_regresion_grado,
    "opt-clasificacion-accuracy": opt_clasificacion_accuracy,
    "opt-clasificacion-alfa": opt_clasificacion_alfa,
    "opt-juego-turnos": opt_juego_turnos,
    "opt-clasificacion-proxy": opt_clasificacion_proxy,
    "opt-panaderia-criterios": opt_panaderia_criterios,
    "opt-clasificacion-sigmoide": opt_clasificacion_sigmoide,
    "opt-clasificacion-log-loss": opt_clasificacion_log_loss,
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
    "opt-cuerda": opt_cuerda,
    "opt-concava-convexa": opt_concava_convexa,
    "opt-tangencia": opt_tangencia,
    "opt-normales": opt_normales,
    "opt-pasos-gradiente": opt_pasos_gradiente,
    "opt-flujo-enumerar": opt_flujo_enumerar,
    "opt-rejilla": opt_rejilla,
    "opt-relajacion-corte": opt_relajacion_corte,
    "opt-ramas": opt_ramas,
    "opt-arbol": opt_arbol,
    **{f"opt-arbol-paso-{paso}": (lambda paso=paso: opt_arbol_paso(paso))
       for paso in range(5)},
    "opt-flujo-ramificar": opt_flujo_ramificar,
    "opt-arbol-vocabulario": opt_arbol_vocabulario,
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
