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
ROTULOS = {
    (0, 0): (0, 48, "middle"),
    (9, 0): (0, 48, "middle"),
    (8, 2): (16, -14, "start"),
    (2, 8): (14, -16, "start"),
    (0, 9): (16, -16, "start"),
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
                       (0, 10): (18, 20, "start"),
                       (9, 0): (-8, -18, "end")}.get(
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
