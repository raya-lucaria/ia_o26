"""Genera los diagramas SVG de la unidad de computabilidad.

Mismo patron que gen_timeline.py y gen_computo.py: paleta en constantes, una
funcion por diagrama que devuelve una cadena SVG completa, y un catalogo
DIAGRAMAS que el generador y su prueba comparten como unica fuente de "que
diagramas existen".

Los ids llevan prefijo "comp-" a proposito: los ids de objeto numerado de Raya
son unicos en TODO el curso, no por pagina, y "computo" ya lo ocupa una figura
de la unidad de historia.
"""
import sys
from xml.sax.saxutils import escape

from unidades import ASSETS_COMPUTABILIDAD

ASSETS = ASSETS_COMPUTABILIDAD

# Paleta del skin eva-cyberpunk, identica a gen_computo.py. FONDO es
# tokens.color.surface y va horneado en cada SVG: test_9 de test_aceptacion.py
# falla sin el.
FONDO, TEXTO, SUAVE, LINEA = "#211033", "#f7f2ff", "#c8b9d8", "#78419e"
ACENTO = "#f04cff"
SERIE = ["#a8ff5a", "#55ddff", "#ffd166"]
FUENTE = "system-ui, sans-serif"


def marco(ancho, alto, aria):
    """Etiqueta <svg> raiz con los cinco atributos que exigen las guardas.

    width/height explicitos ademas de viewBox: el sitio incrusta estos SVG con
    <img>, y sin tamano intrinseco el navegador cae al tamano por omision de un
    elemento reemplazado (~300x150 CSS px) en vez de llenar el contenedor de la
    figura. Misma convencion que gen_computo.py y gen_timeline.py.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
        f'viewBox="0 0 {ancho} {alto}" role="img" aria-label="{escape(aria)}">'
        f'<rect x="0" y="0" width="{ancho}" height="{alto}" rx="16" fill="{FONDO}"/>'
        f'<defs><marker id="p" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ACENTO}"/></marker></defs>'
    )


def cierre():
    return "</svg>"


def texto(x, y, s, color=TEXTO, tam=15, anclaje="middle", peso="normal"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{FUENTE}" '
        f'font-size="{tam}" font-weight="{peso}" text-anchor="{anclaje}">'
        f"{escape(s)}</text>"
    )


def caja(x, y, w, h, relleno="none", borde=LINEA, radio=10, grosor=2):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radio}" '
        f'fill="{relleno}" stroke="{borde}" stroke-width="{grosor}"/>'
    )


def flecha(x1, y1, x2, y2, color=ACENTO, grosor=2):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{grosor}" marker-end="url(#p)"/>'
    )


def comp_esencia():
    """Pagina 1. La tesis: simbolos + tabla de reglas FINITA + pasos discretos.

    Las celdas son las mismas de una cinta a proposito: prefiguran la maquina
    de la pagina 2 sin nombrarla todavia.
    """
    ancho, alto = 960, 430
    aria = (
        "Una cadena de simbolos se transforma paso a paso segun una tabla de "
        "reglas finita: tres estados sucesivos de la misma cinta, con la tabla "
        "de reglas al lado"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(300, 46, "Un computo es esto, y nada mas", TEXTO, 20, peso="600"))

    celda = 54
    filas = [
        (100, ["1", "1", "0", "1", ""], 0, "al principio"),
        (205, ["1", "1", "0", "1", ""], 1, "un paso despues"),
        (310, ["1", "1", "1", "1", ""], 2, "dos pasos despues"),
    ]
    x0 = 70
    for y, simbolos, col, glosa in filas:
        for i, s in enumerate(simbolos):
            x = x0 + i * celda
            borde = ACENTO if i == col else LINEA
            p.append(caja(x, y, celda, celda, borde=borde, radio=6))
            if s:
                p.append(texto(x + celda / 2, y + 36, s, TEXTO, 22))
        p.append(texto(x0 + col * celda + celda / 2, y - 8, "▼", ACENTO, 13))
        p.append(texto(x0, y + celda + 20, glosa, SUAVE, 13, anclaje="start"))

    tx, ty = 620, 92
    p.append(caja(tx, ty, 280, 250, borde=SUAVE))
    p.append(texto(tx + 140, ty + 34, "La tabla de reglas", TEXTO, 16, peso="600"))
    p.append(texto(tx + 140, ty + 58, "es FINITA", ACENTO, 15, peso="600"))
    reglas = [
        "si lees 0 → escribe 1, avanza",
        "si lees 1 → no cambies, avanza",
        "si lees ␣ → detente",
    ]
    for i, r in enumerate(reglas):
        p.append(texto(tx + 20, ty + 104 + i * 32, r, SUAVE, 13.5, anclaje="start"))
    p.append(texto(tx + 140, ty + 222, "La cinta no lo es.", TEXTO, 15, peso="600"))

    p.append(
        texto(
            ancho / 2,
            405,
            "Sin intuición, sin comprensión, sin salto: cada paso lo decide "
            "una cantidad finita de información local.",
            SUAVE,
            13.5,
        )
    )
    p.append(cierre())
    return "".join(p)


def estado(x, y, etiqueta, r=34, borde=LINEA, color_texto=TEXTO, doble=False):
    """Un estado del automata: circulo con su nombre dentro."""
    p = [
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FONDO}" stroke="{borde}" '
        f'stroke-width="2"/>'
    ]
    if doble:
        p.append(
            f'<circle cx="{x}" cy="{y}" r="{r - 6}" fill="none" stroke="{borde}" '
            f'stroke-width="2"/>'
        )
    p.append(texto(x, y + 6, etiqueta, color_texto, 16, peso="600"))
    return "".join(p)


def curva(x1, y1, x2, y2, comba=40, color=LINEA, grosor=2):
    """Arista curva entre dos puntos, con punta de flecha."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    largo = max((dx * dx + dy * dy) ** 0.5, 1)
    cx, cy = mx - dy / largo * comba, my + dx / largo * comba
    return (
        f'<path d="M {x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" '
        f'stroke="{color}" stroke-width="{grosor}" marker-end="url(#p)"/>'
    )


def bucle(x, y, r=34, color=LINEA):
    """Bucle sobre si mismo, dibujado arriba del estado."""
    return (
        f'<path d="M {x - 14} {y - r + 4} C {x - 40} {y - r - 46}, '
        f'{x + 40} {y - r - 46}, {x + 14} {y - r + 4}" fill="none" '
        f'stroke="{color}" stroke-width="2" marker-end="url(#p)"/>'
    )


def comp_tres_vistas():
    """Pagina 1. Pregunta, funcion caracteristica y lenguaje son el mismo objeto."""
    ancho, alto = 980, 340
    aria = (
        "Tres paneles conectados por flechas: la pregunta '¿es n primo?', la "
        "funcion caracteristica que devuelve 0 o 1, y el conjunto de cadenas "
        "que la cumplen. Los tres son el mismo objeto"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "El mismo objeto, visto de tres maneras", TEXTO, 20, peso="600"))

    paneles = [
        (50, "Una pregunta", ["«¿es n primo?»", "", "sí o no, para cada n"], SERIE[1]),
        (370, "Una función", ["χ(n) = 1  si n es primo", "χ(n) = 0  si no", "", "χ : ℕ → {0,1}"], SERIE[2]),
        (690, "Un lenguaje", ["{ 10, 11, 101, 111,", "  1011, 1101, … }", "", "L ⊆ Σ*"], SERIE[0]),
    ]
    for x, titulo, lineas, color in paneles:
        p.append(caja(x, 82, 240, 170, borde=color))
        p.append(texto(x + 120, 112, titulo, color, 16, peso="600"))
        for i, linea in enumerate(lineas):
            if linea:
                p.append(texto(x + 120, 148 + i * 26, linea, SUAVE, 14))
    p.append(flecha(300, 167, 360, 167))
    p.append(flecha(620, 167, 680, 167))
    p.append(
        texto(
            ancho / 2,
            300,
            "Por eso «este problema es indecidible» se puede decir sin ambigüedad: "
            "un problema de decisión es un conjunto de cadenas.",
            SUAVE,
            13.5,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_anatomia():
    """Pagina 2. Que es finito y que es infinito: ese contraste ES la maquina."""
    ancho, alto = 960, 400
    aria = (
        "Anatomia de la maquina de Turing: una cinta con tope izquierdo que se "
        "pierde hacia la derecha, un cabezal, y un control finito con su tabla "
        "de reglas"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Las tres piezas, y cuál de ellas es infinita", TEXTO, 20, peso="600"))

    celda, y = 62, 210
    x0 = 70
    simbolos = ["0", "0", "1", "1", "␣", "␣", "␣", ""]
    for i, s in enumerate(simbolos):
        x = x0 + i * celda
        if i == len(simbolos) - 1:
            p.append(texto(x + 26, y + 40, "· · ·", SUAVE, 22))
            continue
        p.append(caja(x, y, celda, celda, borde=LINEA, radio=4))
        p.append(texto(x + celda / 2, y + 40, s, TEXTO, 22))
    # Tope izquierdo: la cinta empieza aqui y no hay nada a la izquierda.
    p.append(
        f'<line x1="{x0 - 6}" y1="{y - 10}" x2="{x0 - 6}" y2="{y + celda + 10}" '
        f'stroke="{ACENTO}" stroke-width="4"/>'
    )
    p.append(texto(x0 - 12, y + celda + 34, "tope: no hay nada", ACENTO, 12, anclaje="start"))
    p.append(texto(x0 - 12, y + celda + 50, "a la izquierda", ACENTO, 12, anclaje="start"))
    p.append(texto(x0 + 6 * celda, y - 18, "infinita hacia la derecha", SUAVE, 13, anclaje="start"))

    # Cabezal
    cx = x0 + 2 * celda + celda / 2
    p.append(
        f'<path d="M {cx - 16} {y - 16} L {cx + 16} {y - 16} L {cx} {y + 4} z" '
        f'fill="{ACENTO}"/>'
    )
    p.append(texto(cx, y - 26, "cabezal", ACENTO, 13))

    # Control finito
    p.append(caja(660, 96, 250, 86, borde=SERIE[0]))
    p.append(texto(785, 128, "control", SERIE[0], 16, peso="600"))
    p.append(texto(785, 154, "la tabla de δ — FINITA", TEXTO, 14, peso="600"))
    p.append(flecha(785, 186, cx + 40, y - 30, color=SERIE[0]))

    p.append(
        texto(
            ancho / 2,
            370,
            "La tabla de reglas es finita; la cinta no. Ese contraste es la máquina.",
            TEXTO,
            15,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_configuracion():
    """Pagina 2. Como se lee la notacion u q v. El calentamiento antes de delta."""
    ancho, alto = 900, 300
    aria = (
        "La notacion de configuracion u q v anotada: u es lo que quedo atras, "
        "q es el estado, y v empieza en el simbolo que el cabezal esta leyendo"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Cómo se lee una configuración", TEXTO, 20, peso="600"))

    y = 140
    piezas = [(250, "X0", SUAVE), (360, "q₁", ACENTO), (450, "Y1", TEXTO)]
    for x, s, color in piezas:
        p.append(texto(x, y, s, color, 34, peso="600"))

    p.append(f'<path d="M 210 {y+22} L 210 {y+38} L 292 {y+38} L 292 {y+22}" '
             f'fill="none" stroke="{SUAVE}" stroke-width="2"/>')
    p.append(texto(251, y + 62, "lo que quedó atrás", SUAVE, 13))

    p.append(f'<path d="M 410 {y+22} L 410 {y+38} L 496 {y+38} L 496 {y+22}" '
             f'fill="none" stroke="{TEXTO}" stroke-width="2"/>')
    p.append(texto(453, y + 62, "desde el cabezal en adelante", TEXTO, 13))

    p.append(texto(360, y - 44, "el estado", ACENTO, 13))
    p.append(f'<line x1="360" y1="{y-36}" x2="360" y2="{y-22}" stroke="{ACENTO}" stroke-width="2"/>')

    p.append(flecha(440, y - 40, 428, y - 14, color=SERIE[1]))
    p.append(texto(470, y - 48, "el cabezal lee ESTE símbolo", SERIE[1], 13, anclaje="start"))

    p.append(
        texto(
            ancho / 2,
            258,
            "El estado va escrito justo a la izquierda de lo que la máquina está leyendo. "
            "No hay más truco que ése.",
            SUAVE,
            13.5,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_automata():
    """Pagina 2. El automata de la maquina de juguete, con los papeles en espanol."""
    ancho, alto = 980, 480
    aria = (
        "Automata de la maquina de juguete que decide 0 elevado a n seguido de "
        "1 elevado a n: seis estados con sus transiciones etiquetadas"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 42, "La máquina de juguete, como autómata", TEXTO, 20, peso="600"))

    pos = {
        "q₀": (150, 200),
        "q₁": (420, 140),
        "q₂": (420, 300),
        "q₃": (690, 200),
        "acc": (880, 200),
    }
    papeles = {
        "q₀": "busca el siguiente\ncero sin tachar",
        "q₁": "va a la derecha\nbuscando un uno",
        "q₂": "regresa a\nla izquierda",
        "q₃": "verifica que solo\nqueden marcas",
    }

    p.append(curva(184, 186, 388, 152, comba=18))
    p.append(texto(280, 150, "0 → X, →", SERIE[0], 13))
    p.append(bucle(420, 140))
    p.append(texto(420, 74, "0 → 0, →   ·   Y → Y, →", SUAVE, 12))
    p.append(curva(420, 174, 420, 266, comba=-52))
    p.append(texto(505, 222, "1 → Y, ←", SERIE[1], 13))
    p.append(bucle(420, 300))
    p.append(texto(420, 234, "0 → 0, ←   ·   Y → Y, ←", SUAVE, 12))
    p.append(curva(388, 320, 172, 232, comba=18))
    p.append(texto(275, 305, "X → X, →", SUAVE, 13))
    p.append(curva(184, 190, 656, 190, comba=-84))
    p.append(texto(420, 96, "Y → Y, →   (ya no quedan ceros)", ACENTO, 13))
    p.append(bucle(690, 200))
    p.append(texto(690, 134, "Y → Y, →", SUAVE, 12))
    p.append(flecha(724, 200, 842, 200, color=SERIE[0]))
    p.append(texto(783, 188, "␣", SERIE[0], 15))

    for nombre, (x, y) in pos.items():
        if nombre == "acc":
            p.append(estado(x, y, "acc", borde=SERIE[0], color_texto=SERIE[0], doble=True))
            continue
        p.append(estado(x, y, nombre))
    for nombre, papel in papeles.items():
        x, y = pos[nombre]
        for i, linea in enumerate(papel.split("\n")):
            p.append(texto(x, y + 56 + i * 16, linea, SUAVE, 12))

    p.append(
        texto(
            ancho / 2,
            452,
            "Falta un estado: q_rej. Todo lo que no aparece aquí va a él — por eso δ es total "
            "aunque el dibujo se vea incompleto.",
            SUAVE,
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_tres_desenlaces():
    """Pagina 3. El tercer desenlace es el que hace posible la unidad entera."""
    ancho, alto = 900, 380
    aria = (
        "Una maquina con tres salidas posibles: acepta, rechaza, y cicla para "
        "siempre, dibujado como una flecha que vuelve sobre si misma"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Tres desenlaces, no dos", TEXTO, 20, peso="600"))

    p.append(caja(90, 150, 150, 90, borde=SUAVE))
    p.append(texto(165, 186, "M", TEXTO, 22, peso="600"))
    p.append(texto(165, 214, "con entrada w", SUAVE, 12))

    salidas = [
        (110, "acepta", SERIE[0], "w ∈ L(M)"),
        (200, "rechaza", SUAVE, "w ∉ L(M)"),
    ]
    for y, etiqueta, color, glosa in salidas:
        p.append(flecha(240, 195, 470, y + 20, color=color))
        p.append(caja(480, y - 8, 150, 56, borde=color))
        p.append(texto(555, y + 20, etiqueta, color, 16, peso="600"))
        p.append(texto(660, y + 24, glosa, SUAVE, 13, anclaje="start"))

    p.append(flecha(240, 215, 470, 300, color=ACENTO))
    p.append(caja(480, 272, 150, 56, borde=ACENTO))
    p.append(texto(555, 300, "cicla", ACENTO, 16, peso="600"))
    p.append(
        f'<path d="M 630 288 C 700 250, 700 350, 630 314" fill="none" '
        f'stroke="{ACENTO}" stroke-width="2" marker-end="url(#p)"/>'
    )
    p.append(texto(712, 304, "para siempre", ACENTO, 13, anclaje="start"))

    p.append(
        texto(
            ancho / 2,
            356,
            "El tercero es el que hace posible esta unidad. Sin él no habría nada que demostrar.",
            TEXTO,
            14,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_decidir_vs_reconocer():
    """Pagina 3. La promesa de detenerse, dibujada."""
    ancho, alto = 940, 420
    aria = (
        "Dos maquinas sobre la misma entrada: el decisor siempre llega a una de "
        "dos puertas; el reconocedor tiene una tercera salida que no llega a "
        "ninguna parte"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "La única diferencia es la promesa de detenerse", TEXTO, 20, peso="600"))

    bloques = [
        (86, "Un DECISOR de L", SERIE[0], True),
        (250, "Un RECONOCEDOR de L", ACENTO, False),
    ]
    for y, titulo, color, es_decisor in bloques:
        p.append(texto(60, y, titulo, color, 16, anclaje="start", peso="600"))
        p.append(caja(60, y + 14, 130, 78, borde=color))
        p.append(texto(125, y + 60, "M", TEXTO, 20, peso="600"))
        p.append(flecha(190, y + 40, 380, y + 30, color=SERIE[0]))
        p.append(texto(400, y + 34, "acepta", SERIE[0], 14, anclaje="start"))
        p.append(flecha(190, y + 66, 380, y + 76, color=SUAVE))
        p.append(texto(400, y + 80, "rechaza", SUAVE, 14, anclaje="start"))
        if es_decisor:
            p.append(texto(560, y + 56, "siempre llega a una de las dos", SERIE[0], 13, anclaje="start"))
        else:
            p.append(
                f'<line x1="190" y1="{y+82}" x2="380" y2="{y+120}" stroke="{ACENTO}" '
                f'stroke-width="2" stroke-dasharray="7 6"/>'
            )
            p.append(texto(400, y + 124, "cicla — nunca contesta", ACENTO, 14, anclaje="start"))
            p.append(texto(560, y + 156, "¿cuánto espero antes de rendirme?", ACENTO, 14, anclaje="middle", peso="600"))

    p.append(
        texto(
            ancho / 2,
            398,
            "Si la respuesta es «sí», el reconocedor te lo dice. Si es «no», quizá esperas para siempre "
            "— y no hay momento en que puedas rendirte con derecho.",
            SUAVE,
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_tres_clases():
    """Pagina 3. Los tres anillos, poblados con ejemplos con nombre."""
    ancho, alto = 880, 460
    aria = (
        "Tres anillos anidados: los lenguajes decidibles dentro de los "
        "reconocibles, y estos dentro de todos los lenguajes, con un ejemplo "
        "con nombre en cada region"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Tres clases, y las dos son contenciones estrictas", TEXTO, 20, peso="600"))

    cx, cy = 440, 250
    anillos = [
        (330, 160, SUAVE, "todos los lenguajes", 108),
        (230, 112, ACENTO, "reconocibles", 158),
        (130, 64, SERIE[0], "decidibles", 208),
    ]
    for rx, ry, color, etiqueta, y_et in anillos:
        p.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        p.append(texto(cx, y_et, etiqueta, color, 14, peso="600"))

    p.append(texto(cx, 258, "0ⁿ1ⁿ", SERIE[0], 17, peso="600"))
    p.append(texto(cx, 278, "la máquina de la pág. 2", SUAVE, 11))
    p.append(texto(cx, 330, "HALT", ACENTO, 17, peso="600"))
    p.append(texto(cx, 348, "reconocible, no decidible", SUAVE, 11))
    p.append(texto(cx, 392, "el complemento de HALT", TEXTO, 15, peso="600"))
    p.append(texto(cx, 410, "ni siquiera reconocible", SUAVE, 11))

    p.append(
        texto(
            ancho / 2,
            440,
            "Cada anillo tiene un habitante con nombre. Los dos de afuera se ganan en la página 5.",
            SUAVE,
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_shortlex():
    """Pagina 4. La biyeccion concreta, y la advertencia de que no es binario."""
    ancho, alto = 900, 360
    aria = (
        "El orden shortlex emparejado con los naturales: cadena vacia a 0, "
        "cero a 1, uno a 2, y asi. No es leer la cadena como numero binario"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Toda cadena tiene su número, y todo número su cadena", TEXTO, 20, peso="600"))

    pares = [("ε", 0), ("0", 1), ("1", 2), ("00", 3), ("01", 4), ("10", 5), ("11", 6), ("000", 7)]
    x0, y = 90, 130
    ancho_col = 92
    for i, (cadena, n) in enumerate(pares):
        x = x0 + i * ancho_col
        p.append(caja(x, y, 68, 48, borde=LINEA, radio=6))
        p.append(texto(x + 34, y + 32, cadena, TEXTO, 17))
        p.append(flecha(x + 34, y + 56, x + 34, y + 86, color=SUAVE))
        p.append(texto(x + 34, y + 112, str(n), SERIE[1], 19, peso="600"))
    p.append(texto(x0 + 8 * ancho_col - 10, y + 32, "· · ·", SUAVE, 20, anclaje="start"))

    p.append(caja(150, 268, 600, 56, borde=ACENTO))
    p.append(
        texto(
            450,
            292,
            "No es «leer la cadena en binario»: eso no sería inyectivo,",
            ACENTO,
            14,
            peso="600",
        )
    )
    p.append(texto(450, 312, "porque 0, 00 y 000 darían todos 0. Es la posición en el orden.", ACENTO, 14))
    p.append(cierre())
    return "".join(p)


def comp_maquina_dato():
    """Pagina 4. La maquina universal: el programa es dato."""
    ancho, alto = 900, 380
    aria = (
        "La maquina universal U recibe el codigo de una maquina M junto con una "
        "entrada w, y simula M sobre w: el programa entra como dato"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Una sola máquina, y el programa entra como dato", TEXTO, 20, peso="600"))

    p.append(caja(70, 140, 200, 100, borde=SERIE[2], radio=8))
    p.append(texto(170, 176, "⟨M, w⟩", SERIE[2], 20, peso="600"))
    p.append(texto(170, 204, "una cadena, nada más", SUAVE, 12))
    p.append(texto(170, 226, "el código de M, y su entrada", SUAVE, 12))

    p.append(flecha(270, 190, 360, 190))

    p.append(caja(370, 110, 300, 160, borde=ACENTO, radio=12, grosor=3))
    p.append(texto(520, 146, "U", ACENTO, 26, peso="600"))
    p.append(texto(520, 172, "la máquina universal", ACENTO, 13))
    p.append(caja(410, 190, 220, 62, borde=SUAVE, radio=6))
    p.append(texto(520, 216, "aquí adentro corre M", SUAVE, 13))
    p.append(texto(520, 238, "paso por paso, sobre w", SUAVE, 12))

    p.append(flecha(670, 190, 760, 190))
    p.append(texto(830, 186, "lo mismo que", TEXTO, 13))
    p.append(texto(830, 206, "habría hecho M", TEXTO, 13))

    p.append(
        texto(
            ancho / 2,
            330,
            "No hace falta una máquina por problema: hay una, y el programa es su entrada.",
            TEXTO,
            15,
            peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2,
            356,
            "Es la computadora de programa almacenado, enunciada en 1936, antes de que existiera ninguna.",
            SUAVE,
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_de_h_a_d():
    """Pagina 5. Los dos paneles: H sola, y D construida CON H adentro.

    Que se vea que D esta hecha con H es medio argumento: es lo que justifica
    "si H existe, D existe".
    """
    ancho, alto = 980, 440
    aria = (
        "Dos paneles. A la izquierda la maquina H que decidiria el problema de "
        "la parada. A la derecha la maquina D, construida con H dentro, un "
        "duplicador a la entrada y un inversor a la salida"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(245, 44, "1. Lo que H sería", TEXTO, 18, peso="600"))
    p.append(texto(715, 44, "2. Y lo que construimos con ella", TEXTO, 18, peso="600"))
    p.append(
        f'<line x1="490" y1="70" x2="490" y2="400" stroke="{LINEA}" '
        f'stroke-width="1" stroke-dasharray="6 6"/>'
    )

    # Panel izquierdo: H sola
    p.append(texto(70, 150, "⟨M, w⟩", SERIE[2], 16, anclaje="start"))
    p.append(flecha(160, 145, 215, 145))
    p.append(caja(225, 110, 130, 110, borde=ACENTO, grosor=3))
    p.append(texto(290, 158, "H", ACENTO, 26, peso="600"))
    p.append(texto(290, 182, "decide HALT", ACENTO, 11))
    p.append(flecha(355, 132, 410, 122, color=SERIE[0]))
    p.append(texto(420, 126, "SÍ", SERIE[0], 16, anclaje="start", peso="600"))
    p.append(flecha(355, 198, 410, 208, color=SUAVE))
    p.append(texto(420, 212, "NO", SUAVE, 16, anclaje="start", peso="600"))
    p.append(caja(150, 250, 280, 44, borde=SERIE[0], radio=22))
    p.append(texto(290, 278, "y SIEMPRE se detiene", SERIE[0], 14, peso="600"))
    p.append(texto(290, 330, "Es la máquina que suponemos", SUAVE, 13))
    p.append(texto(290, 350, "que existe. Todo lo demás", SUAVE, 13))
    p.append(texto(290, 370, "sale de ahí.", SUAVE, 13))

    # Panel derecho: D, con H adentro
    p.append(texto(530, 150, "⟨M⟩", SERIE[2], 16, anclaje="start"))
    p.append(flecha(580, 145, 615, 145))
    p.append(caja(605, 92, 340, 210, borde=SERIE[1], grosor=3, radio=14))
    p.append(texto(775, 84, "D", SERIE[1], 22, peso="600"))
    p.append(caja(620, 120, 96, 50, borde=SUAVE, radio=6))
    p.append(texto(668, 142, "duplica", SUAVE, 11))
    p.append(texto(668, 158, "⟨M⟩ → M,⟨M⟩", SUAVE, 10))
    p.append(flecha(716, 145, 748, 145))
    p.append(caja(756, 112, 96, 66, borde=ACENTO, grosor=2))
    p.append(texto(804, 150, "H", ACENTO, 20, peso="600"))
    p.append(flecha(852, 130, 890, 122, color=SERIE[0]))
    p.append(texto(896, 126, "SÍ", SERIE[0], 12, anclaje="start"))
    p.append(flecha(852, 162, 890, 172, color=SUAVE))
    p.append(texto(896, 176, "NO", SUAVE, 12, anclaje="start"))
    p.append(caja(700, 208, 220, 76, borde=ACENTO, radio=8))
    p.append(texto(810, 232, "el inversor", ACENTO, 13, peso="600"))
    p.append(texto(810, 254, "SÍ → cicla para siempre", SUAVE, 12))
    p.append(texto(810, 272, "NO → se detiene", SUAVE, 12))

    p.append(
        texto(
            ancho / 2,
            424,
            "D está construida CON H adentro: por eso, si H existiera, D existiría también.",
            TEXTO,
            14,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


DIAGRAMAS = {
    "comp-esencia": comp_esencia,
    "comp-tres-vistas": comp_tres_vistas,
    "comp-anatomia": comp_anatomia,
    "comp-configuracion": comp_configuracion,
    "comp-automata": comp_automata,
    "comp-tres-desenlaces": comp_tres_desenlaces,
    "comp-decidir-vs-reconocer": comp_decidir_vs_reconocer,
    "comp-tres-clases": comp_tres_clases,
    "comp-shortlex": comp_shortlex,
    "comp-maquina-dato": comp_maquina_dato,
    "comp-de-h-a-d": comp_de_h_a_d,
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
