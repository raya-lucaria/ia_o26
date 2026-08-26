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
    """Pagina 2. Como se lee la notacion u q v.

    Muestra la cinta dibujada Y la notacion sobre LA MISMA configuracion, y esa
    configuracion es un paso real: el 3 de la traza de 0011 que la pagina trae
    mas abajo. La primera version invento X0 q1 Y1, que la maquina no alcanza
    nunca, y ademas no coincidia con el ejemplo de la prosa: la figura que
    enseniaba la notacion usaba una notacion distinta de la del resto.
    """
    ancho, alto = 940, 470
    aria = (
        "La misma configuracion mostrada de dos maneras: arriba la cinta con el "
        "cabezal sobre el primer uno, y abajo escrita como X0 q1 11, con llaves "
        "que marcan que quedo atras y que empieza en el cabezal"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Una configuración es la cinta, el cabezal y el estado, en una sola línea", TEXTO, 17, peso="600"))

    # --- Arriba: la cinta de verdad ---
    p.append(texto(ancho / 2, 84, "1 · La máquina, tal como está", SERIE[1], 15, peso="600"))
    celda, y = 64, 104
    x0 = (ancho - 5 * celda) / 2
    simbolos = ["X", "0", "1", "1", "␣"]
    cabezal = 2
    for i, s in enumerate(simbolos):
        x = x0 + i * celda
        p.append(caja(x, y, celda, celda, borde=ACENTO if i == cabezal else LINEA, radio=5))
        p.append(texto(x + celda / 2, y + 42, s, TEXTO, 24))
    cx = x0 + cabezal * celda + celda / 2
    p.append(
        f'<path d="M {cx - 15} {y - 22} L {cx + 15} {y - 22} L {cx} {y - 3} z" fill="{ACENTO}"/>'
    )
    p.append(texto(cx, y - 32, "el cabezal está aquí", ACENTO, 13))
    p.append(texto(x0 - 16, y + 42, "estado " , SUAVE, 14, anclaje="end"))
    p.append(texto(x0 - 16, y + 62, "q₁", ACENTO, 17, anclaje="end", peso="600"))

    # --- Abajo: lo mismo, escrito ---
    p.append(texto(ancho / 2, 246, "2 · Lo mismo, escrito en una línea", SERIE[1], 15, peso="600"))
    yn = 300
    piezas = [(360, "X0", SUAVE), (452, "q₁", ACENTO), (534, "11", TEXTO)]
    for x, s, color in piezas:
        p.append(texto(x, yn, s, color, 32, peso="600"))

    p.append(f'<path d="M 328 {yn+16} L 328 {yn+32} L 392 {yn+32} L 392 {yn+16}" '
             f'fill="none" stroke="{SUAVE}" stroke-width="2"/>')
    p.append(texto(360, yn + 54, "lo que quedó atrás", SUAVE, 13))
    p.append(texto(360, yn + 72, "(las dos primeras casillas)", SUAVE, 11))

    p.append(f'<path d="M 502 {yn+16} L 502 {yn+32} L 566 {yn+32} L 566 {yn+16}" '
             f'fill="none" stroke="{TEXTO}" stroke-width="2"/>')
    p.append(texto(534, yn + 54, "desde el cabezal en adelante", TEXTO, 13))
    p.append(texto(534, yn + 72, "(empieza en el símbolo que lee)", SUAVE, 11))

    p.append(texto(452, yn - 40, "el estado", ACENTO, 13))
    p.append(f'<line x1="452" y1="{yn-32}" x2="452" y2="{yn-18}" stroke="{ACENTO}" stroke-width="2"/>')

    # La flecha que ata las dos mitades: del cabezal de arriba al primer simbolo de v.
    p.append(
        f'<path d="M {cx} {y + celda + 12} C {cx} 230, 516 236, 516 {yn - 30}" '
        f'fill="none" stroke="{SERIE[1]}" stroke-width="2" stroke-dasharray="6 5" '
        f'marker-end="url(#p)"/>'
    )
    p.append(texto(cx + 96, 214, "el mismo símbolo", SERIE[1], 12, anclaje="start"))

    p.append(
        texto(
            ancho / 2,
            416,
            "El estado se escribe justo a la izquierda del símbolo que la máquina está leyendo. No hay más truco que ése.",
            SUAVE,
            13.5,
        )
    )
    p.append(
        texto(
            ancho / 2,
            444,
            "Y esto no es un ejemplo inventado: es el paso 3 de la traza de 0011 que viene más abajo en esta página.",
            SERIE[0],
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_automata():
    """Pagina 2. El automata de la maquina de juguete.

    La topologia se rediseno para que NO HAYA cruces posibles, despues de que
    dos revisiones visuales del PNG mostraran que arreglar un cruce a la vez
    creaba otro: al separar el arco q0->q3 del circulo de q1 empezo a partir el
    chip del bucle de q1, y el bucle de q3 acabo cortando la flecha de
    aceptacion.

    La forma que lo resuelve: el ciclo q0->q1->q2->q0 vive abajo a la izquierda,
    y la salida q0->q3->acc sube por un arco despejado a la banda superior
    derecha, que antes era hueco muerto. Ninguna arista tiene que pasar cerca de
    otra.

    Cada etiqueta es un CHIP con fondo opaco puesto SOBRE su propia trayectoria:
    la unica manera de que se sepa de quien es sin adivinar. Que un chip tape su
    propia arista es correcto; que lo cruce una arista ajena, no.
    """
    ancho, alto = 1100, 800
    TRAZO = "#a273d6"   # 5.09:1 sobre #211033. LINEA (#78419e) da 2.57:1
    aria = (
        "Automata de la maquina que decide 0 elevado a n seguido de 1 elevado a "
        "n: cinco estados y diez transiciones, cada una etiquetada con el "
        "simbolo que lee, el que escribe y la direccion en que se mueve"
    )
    p = [marco(ancho, alto, aria)]
    for nombre, color in [("pm", ACENTO), ("pv", SERIE[0]), ("pc", SERIE[1]), ("pt", TRAZO)]:
        p.append(
            f'<defs><marker id="{nombre}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker></defs>'
        )
    p.append(texto(300, 40, "La máquina de juguete, como autómata", TEXTO, 21, peso="600"))

    def chip(x, y, lee, escribe, direccion, color):
        txt = f"{lee} │ {escribe}"
        w = len(txt) * 9.2 + 24
        s = [f'<rect x="{x - w/2}" y="{y - 14}" width="{w}" height="24" rx="5" '
             f'fill="{FONDO}" stroke="{color}" stroke-width="1.2"/>']
        s.append(texto(x - 9, y + 3, txt, color, 14, peso="600"))
        s.append(texto(x + w/2 - 14, y + 3, direccion, SERIE[0], 14, peso="600"))
        return "".join(s)

    # --- Leyenda ---
    p.append(caja(620, 22, 452, 46, borde=SUAVE, radio=8))
    p.append(texto(648, 52, "0 │ X", TRAZO, 16, anclaje="start", peso="600"))
    p.append(texto(712, 52, "▶", SERIE[0], 15, anclaje="start", peso="600"))
    p.append(texto(740, 45, "lee 0, escribe X, se mueve a la derecha", SUAVE, 13, anclaje="start"))
    p.append(texto(740, 62, "◀", SERIE[0], 14, anclaje="start", peso="600"))
    p.append(texto(758, 62, "es a la izquierda", SUAVE, 13, anclaje="start"))

    pos = {"q0": (180, 470), "q1": (450, 370), "q2": (450, 600), "q3": (800, 190), "acc": (985, 190)}

    # --- Salida: sube por la banda superior, lejos de todo ---
    p.append(f'<path d="M 178 440 C 214 258, 470 168, 768 180" fill="none" '
             f'stroke="{ACENTO}" stroke-width="2.5" marker-end="url(#pm)"/>')
    p.append(chip(300, 216, "Y", "Y", "▶", ACENTO))
    p.append(texto(252, 240, "ya no quedan ceros que tachar", ACENTO, 13, anclaje="middle"))

    # --- Ciclo principal ---
    p.append(f'<path d="M 209 452 C 280 412, 350 386, 419 375" fill="none" '
             f'stroke="{TRAZO}" stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(chip(312, 404, "0", "X", "▶", TRAZO))

    p.append(f'<path d="M 478 396 C 528 445, 528 525, 478 574" fill="none" '
             f'stroke="{SERIE[1]}" stroke-width="2.5" marker-end="url(#pc)"/>')
    p.append(chip(540, 485, "1", "Y", "◀", SERIE[1]))

    p.append(f'<path d="M 419 588 C 350 578, 280 538, 210 494" fill="none" '
             f'stroke="{TRAZO}" stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(chip(312, 560, "X", "X", "▶", TRAZO))

    # --- Bucles grandes, con sus chips SOBRE el apice ---
    p.append(f'<path d="M 426 342 C 340 196, 560 196, 474 342" fill="none" '
             f'stroke="{TRAZO}" stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(chip(450, 300, "0", "0", "▶", TRAZO))
    p.append(chip(450, 270, "Y", "Y", "▶", TRAZO))

    p.append(f'<path d="M 426 630 C 340 776, 560 776, 474 630" fill="none" '
             f'stroke="{TRAZO}" stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(chip(450, 700, "0", "0", "◀", TRAZO))
    p.append(chip(450, 670, "Y", "Y", "◀", TRAZO))

    p.append(f'<path d="M 776 160 C 700 60, 900 60, 824 160" fill="none" '
             f'stroke="{TRAZO}" stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(chip(800, 106, "Y", "Y", "▶", TRAZO))

    # --- Aceptacion ---
    p.append(f'<line x1="832" y1="190" x2="951" y2="190" stroke="{SERIE[0]}" '
             f'stroke-width="2.5" marker-end="url(#pv)"/>')
    p.append(chip(891, 190, "␣", "␣", "▶", SERIE[0]))
    p.append(texto(891, 222, "fin de cinta", SERIE[0], 12.5))

    papeles = {
        "q0": ("busca el siguiente|cero sin tachar", "middle", 0),
        "q1": ("va a la derecha|buscando un uno", "start", 40),
        "q2": ("regresa a|la izquierda", "start", 46),
        "q3": ("verifica que solo|queden marcas", "middle", 0),
    }
    # De donde arranca todo. No es una transicion, pero sin ella el dibujo no
    # dice por donde se empieza a leer, que es la mitad de lo que hace falta.
    p.append(f'<line x1="96" y1="470" x2="140" y2="470" stroke="{TEXTO}" '
             f'stroke-width="2.5" marker-end="url(#pt)"/>')
    p.append(texto(60, 452, "empieza aquí", TEXTO, 12.5, anclaje="start"))

    for nombre, (x, y) in pos.items():
        if nombre == "acc":
            p.append(estado(x, y, "acc", r=32, borde=SERIE[0], color_texto=SERIE[0], doble=True))
            continue
        p.append(estado(x, y, nombre, r=32, borde=TRAZO))
    for nombre, (papel, anclaje, dx) in papeles.items():
        x, y = pos[nombre]
        if anclaje == "abajo":
            anclaje, dy = "middle", 62
        else:
            dy = 62 if anclaje == "middle" else -8
        for i, linea in enumerate(papel.split("|")):
            p.append(texto(x + dx, y + dy + i * 17, linea, SUAVE, 13, anclaje=anclaje))

    p.append(texto(660, 330, "Falta un estado: q\u1d63\u2091\u2c7c.", SUAVE, 13, anclaje="start"))
    p.append(texto(660, 350, "Todo lo que no aparece aquí va a él —", SUAVE, 13, anclaje="start"))
    p.append(texto(660, 370, "por eso δ es total aunque el dibujo", SUAVE, 13, anclaje="start"))
    p.append(texto(660, 390, "se vea incompleto.", SUAVE, 13, anclaje="start"))
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


def _panel_autorreferencia(p, x0, y0, titulo, etiqueta_maquina, color_maquina,
                           entrada, ramas, remate):
    """Encuadre compartido por comp-cortocircuito y comp-p-sobre-si.

    Los dos diagramas usan LA MISMA funcion a proposito: el parecido entre la
    demostracion de la parada y la de Godel es el contenido, no una
    coincidencia, y el alumno tiene que verlo antes de que se lo digan. Si un
    dia hay que reacomodar uno, se reacomodan los dos.
    """
    p.append(texto(x0 + 300, y0, titulo, TEXTO, 19, peso="600"))
    p.append(caja(x0 + 200, y0 + 40, 200, 110, borde=color_maquina, grosor=3, radio=14))
    p.append(texto(x0 + 300, y0 + 92, etiqueta_maquina, color_maquina, 26, peso="600"))
    p.append(texto(x0 + 300, y0 + 120, "con su propio código", SUAVE, 12))
    # El cortocircuito: la entrada sale de la propia maquina y vuelve a ella.
    p.append(
        f'<path d="M {x0+200} {y0+95} C {x0+120} {y0+95}, {x0+120} {y0+8}, '
        f'{x0+300} {y0+8} C {x0+480} {y0+8}, {x0+480} {y0+95}, {x0+400} {y0+95}" '
        f'fill="none" stroke="{SERIE[2]}" stroke-width="2" marker-end="url(#p)"/>'
    )
    p.append(texto(x0 + 300, y0 + 26, entrada, SERIE[2], 15, peso="600"))

    for i, (supuesto, medio, consecuencia) in enumerate(ramas):
        y = y0 + 190 + i * 96
        p.append(flecha(x0 + 300, y0 + 152, x0 + 150 + i * 300, y - 16, color=SUAVE))
        p.append(caja(x0 + 30 + i * 300, y - 6, 270, 78, borde=ACENTO, radio=8))
        p.append(texto(x0 + 165 + i * 300, y + 16, supuesto, TEXTO, 13, peso="600"))
        p.append(texto(x0 + 165 + i * 300, y + 38, medio, SUAVE, 12))
        p.append(texto(x0 + 165 + i * 300, y + 60, consecuencia, ACENTO, 13, peso="600"))

    p.append(texto(x0 + 300, y0 + 330, remate, TEXTO, 17, peso="600"))


def comp_cortocircuito():
    """Pagina 5. D sobre su propio codigo. La figura de la unidad."""
    ancho, alto = 980, 590
    aria = (
        "La maquina D recibiendo su propio codigo: las dos ramas posibles "
        "trazadas hasta su contradiccion, y el remate de que D se detiene si y "
        "solo si no se detiene"
    )
    p = [marco(ancho, alto, aria)]
    _panel_autorreferencia(
        p, 40, 46,
        "¿Qué hace D con su propio código?",
        "D", SERIE[1],
        "⟨D⟩",
        [
            ("Si suponemos que SE DETIENE…", "…entonces H contestó SÍ…", "…y entonces D cicla."),
            ("Si suponemos que CICLA…", "…entonces H contestó NO…", "…y entonces D se detiene."),
        ],
        "Las dos ramas se contradicen. Y no hay una tercera.",
    )
    p.append(caja(240, 496, 500, 52, borde=ACENTO, grosor=3, radio=26))
    p.append(texto(490, 528, "D se detiene con ⟨D⟩  ⟺  D NO se detiene con ⟨D⟩", ACENTO, 16, peso="600"))
    p.append(texto(490, 572, "Luego H no existe.", TEXTO, 15, peso="600"))
    p.append(cierre())
    return "".join(p)


def comp_cuadricula():
    """Pagina 5. Donde esta la diagonal: D difiere de cada Mi en la casilla (i,i)."""
    ancho, alto = 940, 500
    aria = (
        "Matriz de maquinas contra codigos con para y no para en cada casilla, "
        "la diagonal resaltada, y la fila de D construida invirtiendola"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Dónde está la diagonal", TEXTO, 20, peso="600"))

    x0, y0, cw, ch = 190, 90, 132, 60
    codigos = ["⟨M₁⟩", "⟨M₂⟩", "⟨M₃⟩", "⟨M₄⟩"]
    for j, c in enumerate(codigos):
        p.append(texto(x0 + j * cw + cw / 2, y0 + 22, c, SERIE[2], 14, peso="600"))
    tabla = [
        ["para", "no para", "para", "para"],
        ["no para", "no para", "para", "no para"],
        ["para", "para", "no para", "para"],
        ["no para", "para", "para", "no para"],
    ]
    for i, fila in enumerate(tabla):
        y = y0 + 40 + i * ch
        p.append(texto(x0 - 20, y + 36, f"M{'₁₂₃₄'[i]}", TEXTO, 15, anclaje="end", peso="600"))
        for j, celda in enumerate(fila):
            x = x0 + j * cw
            diag = i == j
            p.append(caja(x, y, cw, ch, borde=ACENTO if diag else LINEA,
                          grosor=3 if diag else 1, radio=4))
            p.append(texto(x + cw / 2, y + 36, celda, ACENTO if diag else SUAVE, 13,
                           peso="600" if diag else "normal"))

    yd = y0 + 40 + 4 * ch + 22
    p.append(texto(x0 - 20, yd + 36, "D", SERIE[1], 17, anclaje="end", peso="600"))
    invertida = ["no para", "para", "para", "para"]
    for j, celda in enumerate(invertida):
        x = x0 + j * cw
        p.append(caja(x, yd, cw, ch, borde=SERIE[1], grosor=2, radio=4))
        p.append(texto(x + cw / 2, yd + 36, celda, SERIE[1], 13, peso="600"))
    p.append(texto(x0 + 4 * cw + 24, yd + 30, "D se construye", SERIE[1], 12, anclaje="start"))
    p.append(texto(x0 + 4 * cw + 24, yd + 48, "invirtiendo la diagonal", SERIE[1], 12, anclaje="start"))

    p.append(
        texto(
            ancho / 2,
            478,
            "D difiere de cada Mᵢ justo en la casilla (i, i). Pero D es alguna Mⱼ de la lista "
            "— y entonces difiere de sí misma.",
            TEXTO,
            14,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_cantor():
    """Pagina 5. La diagonal de Cantor, sobre sucesiones binarias."""
    ancho, alto = 900, 460
    aria = (
        "La tabla de Cantor: una lista supuesta de todas las sucesiones "
        "binarias, con la diagonal resaltada y la sucesion nueva que se obtiene "
        "cambiando cada digito"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "El conteo: hay más funciones que programas", TEXTO, 20, peso="600"))
    p.append(texto(ancho / 2, 72, "Supón que ESTA lista tuviera todas las sucesiones de 0 y 1:", SUAVE, 13))

    filas = [
        "0 1 1 0 1 0 …",
        "1 1 0 0 1 1 …",
        "0 0 1 1 0 1 …",
        "1 0 0 1 1 0 …",
        "1 1 1 0 0 1 …",
    ]
    x0, y0, dy = 250, 118, 46
    for i, fila in enumerate(filas):
        y = y0 + i * dy
        p.append(texto(x0 - 24, y + 16, f"f{'₁₂₃₄₅'[i]}", SUAVE, 14, anclaje="end"))
        for j, ch in enumerate(fila.split()):
            x = x0 + j * 42
            if i == j:
                p.append(caja(x - 14, y - 6, 32, 32, borde=ACENTO, grosor=2, radio=4))
                p.append(texto(x + 2, y + 16, ch, ACENTO, 17, peso="600"))
            else:
                p.append(texto(x + 2, y + 16, ch, SUAVE, 16))

    y = y0 + 5 * dy + 24
    p.append(texto(x0 - 24, y + 16, "nueva", SERIE[0], 13, anclaje="end", peso="600"))
    for j, ch in enumerate(["1", "0", "0", "0", "1", "…"]):
        p.append(texto(x0 + j * 42 + 2, y + 16, ch, SERIE[0], 17, peso="600"))
    p.append(texto(x0 + 6 * 42 + 30, y + 16, "cambia cada dígito de la diagonal", SERIE[0], 13, anclaje="start"))

    p.append(
        texto(
            ancho / 2,
            420,
            "La nueva no puede ser ninguna de la lista: difiere de fᵢ justo en el lugar i.",
            TEXTO,
            14,
            peso="600",
        )
    )
    p.append(texto(ancho / 2, 444, "Luego no hay lista que las agote — y los programas sí forman una lista.", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


def comp_existir_exhibir():
    """Pagina 5. El conteo dice que HAY; la diagonal dice CUAL. No es lo mismo.

    Existe porque la revision adversarial predijo el malentendido: creer que el
    conteo demostro que HALT es indecidible. No lo demuestra, y ademas HALT no
    es representativo de esa mayoria, porque HALT si es reconocible.
    """
    ancho, alto = 900, 340
    aria = (
        "Dos paneles: el argumento de conteo demuestra que existe algun lenguaje "
        "indecidible sin exhibir ninguno; la diagonalizacion exhibe uno concreto "
        "con nombre"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Dos demostraciones distintas, y se parecen mucho", TEXTO, 20, peso="600"))
    p.append(
        f'<line x1="450" y1="76" x2="450" y2="286" stroke="{LINEA}" '
        f'stroke-width="1" stroke-dasharray="6 6"/>'
    )

    p.append(texto(225, 108, "El conteo", SERIE[2], 17, peso="600"))
    p.append(
        f'<ellipse cx="225" cy="186" rx="115" ry="52" fill="none" stroke="{SERIE[2]}" '
        f'stroke-width="2" stroke-dasharray="8 6"/>'
    )
    p.append(texto(225, 182, "hay alguno", SERIE[2], 16, peso="600"))
    p.append(texto(225, 204, "ahí dentro", SUAVE, 12))
    p.append(texto(225, 262, "Demuestra que EXISTE.", TEXTO, 14, peso="600"))
    p.append(texto(225, 284, "No exhibe ninguno.", SUAVE, 13))

    p.append(texto(675, 108, "La diagonalización", ACENTO, 17, peso="600"))
    p.append(caja(600, 152, 150, 68, borde=ACENTO, grosor=3))
    p.append(texto(675, 182, "HALT", ACENTO, 22, peso="600"))
    p.append(texto(675, 204, "con nombre y apellido", SUAVE, 11))
    p.append(texto(675, 262, "Exhibe UNO concreto.", TEXTO, 14, peso="600"))
    p.append(texto(675, 284, "Y es otra demostración.", SUAVE, 13))

    p.append(
        texto(
            ancho / 2,
            322,
            "El conteo no demuestra que HALT sea indecidible. Y HALT ni siquiera es típico de esa mayoría: HALT sí es reconocible.",
            SUAVE,
            12.5,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_que_es_demostracion():
    """Pagina 6. Una demostracion es un computo: verificarla es decidible."""
    ancho, alto = 940, 400
    aria = (
        "Axiomas arriba, reglas de inferencia aplicandose, una cadena finita de "
        "formulas, y un verificador mecanico palomeando cada paso"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Una demostración es un objeto finito que se puede revisar a máquina", TEXTO, 18, peso="600"))

    p.append(caja(60, 84, 200, 54, borde=SERIE[2], radio=8))
    p.append(texto(160, 116, "los axiomas", SERIE[2], 15, peso="600"))

    pasos = [
        ("φ₁", "es un axioma"),
        ("φ₂", "es un axioma"),
        ("φ₃", "de φ₁ y φ₂, modus ponens"),
        ("φ₄", "de φ₃, generalización"),
    ]
    for i, (formula, razon) in enumerate(pasos):
        y = 168 + i * 52
        p.append(caja(60, y, 470, 42, borde=LINEA, radio=6))
        p.append(texto(96, y + 27, formula, TEXTO, 16, peso="600"))
        p.append(texto(140, y + 27, razon, SUAVE, 13, anclaje="start"))
        p.append(texto(556, y + 27, "✓", SERIE[0], 20, peso="600"))

    p.append(caja(610, 168, 270, 198, borde=SERIE[0], radio=10))
    p.append(texto(745, 200, "el verificador", SERIE[0], 16, peso="600"))
    p.append(texto(745, 232, "¿cada renglón es un axioma", SUAVE, 12))
    p.append(texto(745, 250, "o se sigue de los de arriba", SUAVE, 12))
    p.append(texto(745, 268, "por una regla?", SUAVE, 12))
    p.append(texto(745, 308, "Es DECIDIBLE.", SERIE[0], 15, peso="600"))
    p.append(texto(745, 334, "Siempre termina, y no", SUAVE, 12))
    p.append(texto(745, 350, "se equivoca nunca.", SUAVE, 12))

    p.append(
        texto(
            ancho / 2,
            386,
            "De aquí cuelga todo lo que sigue: si revisar una demostración es un cómputo, un programa puede buscarlas.",
            TEXTO,
            13.5,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_aritmetizacion():
    """Pagina 6. Los DOS pasos, separados: codificar no es representar.

    El diseno original decia "el truco de la pagina 4 otra vez", y no lo es:
    codificar da una biyeccion, y Godel ademas necesita que la relacion sea
    EXPRESABLE por una formula. Este diagrama dibuja el hueco que el texto
    declara.
    """
    ancho, alto = 960, 380
    aria = (
        "Los dos pasos de la aritmetizacion, separados: primero codificar "
        "formulas como numeros, que es lo de la pagina 4, y despues "
        "representar la relacion como una formula de la aritmetica, que es lo "
        "que Godel ademas necesita"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Codificar no basta: hacen falta dos pasos, no uno", TEXTO, 19, peso="600"))

    p.append(caja(50, 96, 230, 120, borde=SUAVE, radio=10))
    p.append(texto(165, 128, "fórmulas y", TEXTO, 15))
    p.append(texto(165, 150, "demostraciones", TEXTO, 15))
    p.append(texto(165, 186, "objetos de sintaxis", SUAVE, 12))

    p.append(flecha(280, 156, 360, 156, color=SUAVE))
    p.append(texto(320, 132, "paso 1", SUAVE, 13, peso="600"))
    p.append(texto(320, 186, "codificar", SUAVE, 12))
    p.append(texto(320, 202, "(la página 4)", SUAVE, 11))

    p.append(caja(370, 96, 200, 120, borde=SERIE[1], radio=10))
    p.append(texto(470, 146, "números", SERIE[1], 18, peso="600"))
    p.append(texto(470, 178, "⌜φ⌝ = 34517…", SUAVE, 12))

    p.append(flecha(570, 156, 650, 156, color=ACENTO, grosor=3))
    p.append(texto(610, 132, "paso 2", ACENTO, 13, peso="600"))
    p.append(texto(610, 186, "representar", ACENTO, 12))
    p.append(texto(610, 202, "(lo que falta)", ACENTO, 11))

    p.append(caja(660, 96, 250, 120, borde=ACENTO, radio=10, grosor=3))
    p.append(texto(785, 134, "Dem(x, y)", ACENTO, 18, peso="600"))
    p.append(texto(785, 162, "una FÓRMULA de la", SUAVE, 12))
    p.append(texto(785, 180, "aritmética que dice", SUAVE, 12))
    p.append(texto(785, 198, "«x demuestra y»", SUAVE, 12))

    p.append(caja(120, 264, 720, 74, borde=ACENTO, radio=10))
    p.append(texto(480, 292, "El paso 2 funciona porque revisar una demostración es un cómputo,", TEXTO, 14))
    p.append(texto(480, 314, "y todo cómputo se puede expresar en aritmética. Ese es el teorema que damos por bueno.", TEXTO, 14))
    p.append(cierre())
    return "".join(p)


def comp_for_enumera():
    """Pagina 7. El motor de la demostracion de Godel es la enumeracion."""
    ancho, alto = 960, 380
    aria = (
        "El ciclo recorre todas las cadenas en orden shortlex y le pregunta a "
        "cada una si es una demostracion de la formula buscada"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "El motor es la enumeración, y nada más", TEXTO, 20, peso="600"))

    celda, y = 92, 130
    x0 = 60
    cadenas = ["ε", "0", "1", "00", "01", "10", "11", "…"]
    for i, s in enumerate(cadenas):
        x = x0 + i * celda
        if s == "…":
            p.append(texto(x + 30, y + 40, "· · ·", SUAVE, 20))
            continue
        p.append(caja(x, y, 76, 56, borde=LINEA, radio=6))
        p.append(texto(x + 38, y + 36, s, TEXTO, 17))
        p.append(texto(x + 38, y + 82, "¿eres?", SUAVE, 11))
        p.append(flecha(x + 38, y + 62, x + 38, y + 68, color=SUAVE))

    p.append(caja(240, 250, 480, 74, borde=ACENTO, radio=10))
    p.append(texto(480, 278, "¿eres una demostración de «x no termina con entrada x»?", ACENTO, 14, peso="600"))
    p.append(texto(480, 304, "Si alguna lo es, el ciclo la encuentra. Si ninguna, corre para siempre.", SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2,
            360,
            "Una demostración es una cadena finita, y este orden llega a toda cadena finita. Ese es todo el truco.",
            TEXTO,
            13.5,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_g_autorreferente():
    """Pagina 7. La oracion G preguntando por su propia demostrabilidad.

    Usa _panel_autorreferencia, la MISMA funcion que comp-cortocircuito: el
    parecido entre la demostracion de la parada y la de Godel es el contenido
    de la pagina 8, no una coincidencia. Compartir la funcion hace que no
    puedan separarse con una edicion futura.
    """
    ancho, alto = 980, 590
    aria = (
        "La oracion G preguntando si el sistema puede demostrarla, con las dos "
        "ramas trazadas y el mismo encuadre que la figura del problema de la "
        "parada"
    )
    p = [marco(ancho, alto, aria)]
    _panel_autorreferencia(
        p, 40, 46,
        "¿Puede el sistema demostrar G?",
        "G", SERIE[1],
        "«yo no puedo ser demostrada»",
        [
            ("Si SÍ la demuestra…", "…entonces también demuestra que la demuestra…",
             "…y G decía lo contrario. Se contradice."),
            ("Luego NO la demuestra…", "…y eso es justo lo que G afirmaba…",
             "…así que G es VERDADERA."),
        ],
        "Hay una verdad que el sistema no alcanza.",
    )
    p.append(caja(210, 496, 560, 52, borde=ACENTO, grosor=3, radio=26))
    p.append(texto(490, 528, "G es verdadera, y el sistema no la demuestra", ACENTO, 16, peso="600"))
    p.append(texto(490, 572, "Mismo encuadre que la figura de la parada: es el mismo movimiento.", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


def comp_verdadero_demostrable():
    """Pagina 7. Contencion PROPIA, no traslape.

    Un revisor pedia cortar este diagrama porque "dos manchas traslapadas"
    produce justo los malentendidos que la pagina combate. Se conserva
    dibujandolo como contencion estricta, y anotando lo que de verdad las
    distingue: los teoremas son enumerables, las verdades no.
    """
    ancho, alto = 900, 440
    aria = (
        "Los teoremas de F estrictamente dentro de las verdades de la "
        "aritmetica, con la oracion de Godel marcada en el hueco entre ambas"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "Verdadero y demostrable no son lo mismo", TEXTO, 20, peso="600"))

    cx, cy = 450, 240
    p.append(
        f'<ellipse cx="{cx}" cy="{cy}" rx="330" ry="140" fill="none" '
        f'stroke="{SERIE[0]}" stroke-width="2"/>'
    )
    p.append(texto(cx, 116, "las verdades de la aritmética", SERIE[0], 15, peso="600"))
    p.append(texto(cx, 136, "NO son enumerables", SUAVE, 12))

    p.append(
        f'<ellipse cx="{cx - 60}" cy="{cy + 10}" rx="200" ry="88" fill="none" '
        f'stroke="{SERIE[1]}" stroke-width="2"/>'
    )
    p.append(texto(cx - 60, cy + 6, "los teoremas de F", SERIE[1], 15, peso="600"))
    p.append(texto(cx - 60, cy + 28, "SÍ son enumerables — el «for»", SUAVE, 12))

    p.append(f'<circle cx="{cx + 210}" cy="{cy + 40}" r="7" fill="{ACENTO}"/>')
    p.append(texto(cx + 210, cy + 74, "«P no termina", ACENTO, 13, peso="600"))
    p.append(texto(cx + 210, cy + 92, "con ⟨P⟩»", ACENTO, 13, peso="600"))
    p.append(texto(cx + 210, cy + 114, "verdadera, no demostrable", SUAVE, 11))

    p.append(
        texto(
            ancho / 2,
            412,
            "La contención es ESTRICTA, y esa es la diferencia que importa: una lista puede enumerar los teoremas; ninguna enumera las verdades.",
            SUAVE,
            12.5,
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_con_f():
    """Pagina 7. Con(F) es la oracion de parada de un programa concreto."""
    ancho, alto = 940, 380
    aria = (
        "El buscador de contradicciones: un programa que enumera demostraciones "
        "de F y se detiene si encuentra una de que cero es igual a uno"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "La consistencia de F es un programa que no termina", TEXTO, 20, peso="600"))

    p.append(caja(60, 96, 420, 180, borde=SERIE[1], radio=12, grosor=3))
    p.append(texto(270, 128, "M_F — el buscador de contradicciones", SERIE[1], 15, peso="600"))
    lineas = [
        "for p in shortlex:",
        "    if EsDemostracion(p, «0 = 1»):",
        "        halt",
    ]
    for i, linea in enumerate(lineas):
        p.append(texto(90, 168 + i * 30, linea, TEXTO, 15, anclaje="start"))
    p.append(texto(270, 258, "enumera TODAS las demostraciones de F", SUAVE, 12))

    p.append(caja(530, 120, 360, 64, borde=ACENTO, radio=10, grosor=3))
    p.append(texto(710, 148, "F es consistente", ACENTO, 16, peso="600"))
    p.append(texto(710, 170, "⟺  este programa nunca se detiene", ACENTO, 14))

    p.append(caja(530, 208, 360, 74, borde=SUAVE, radio=10))
    p.append(texto(710, 234, "Y el segundo teorema dice:", TEXTO, 14, peso="600"))
    p.append(texto(710, 258, "F no puede demostrar que no se detiene", TEXTO, 14))
    p.append(texto(710, 276, "— aunque de hecho no se detenga.", SUAVE, 12))

    p.append(
        texto(
            ancho / 2,
            340,
            "Con(F) no es una fórmula opaca: es la oración de parada de un programa que cabe en tres renglones.",
            TEXTO,
            13.5,
            peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def comp_mismo_esqueleto():
    """Pagina 8. Los tres reducidos a su forma, en fila.

    No es la tabla de la pagina otra vez: la tabla lo dice con palabras, esto
    lo muestra con la forma.
    """
    ancho, alto = 980, 420
    aria = (
        "Cantor, Turing y Godel reducidos a su estructura y puestos en fila: la "
        "misma diagonal en los tres, con objetos distintos"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 44, "El mismo esqueleto, tres veces", TEXTO, 20, peso="600"))

    columnas = [
        (60, "Cantor", SERIE[2], "sucesiones", "cambiar cada dígito",
         "no hay lista que las agote"),
        (370, "Turing", SERIE[1], "máquinas", "hacer lo contrario de H",
         "HALT es indecidible"),
        (680, "Gödel", ACENTO, "fórmulas", "negar la propia demostrabilidad",
         "F es incompleta"),
    ]
    for x, titulo, color, objetos, giro, final in columnas:
        p.append(texto(x + 120, 84, titulo, color, 18, peso="600"))
        # La rejilla con su diagonal: identica en las tres columnas.
        gx, gy, c = x + 40, 106, 32
        for i in range(4):
            for j in range(4):
                diag = i == j
                p.append(
                    f'<rect x="{gx + j * c}" y="{gy + i * c}" width="{c - 4}" '
                    f'height="{c - 4}" rx="3" fill="none" '
                    f'stroke="{color if diag else LINEA}" '
                    f'stroke-width="{2 if diag else 1}"/>'
                )
        p.append(texto(x + 120, 258, objetos, TEXTO, 14, peso="600"))
        p.append(texto(x + 120, 286, giro, SUAVE, 12))
        p.append(caja(x + 10, 306, 220, 44, borde=color, radio=8))
        p.append(texto(x + 120, 334, final, color, 13, peso="600"))

    p.append(
        texto(
            ancho / 2,
            390,
            "El núcleo común no es la autorreferencia: es la diagonalización. En Cantor los objetos no hablan de sí mismos; en los otros dos, sí.",
            SUAVE,
            13,
        )
    )
    p.append(cierre())
    return "".join(p)


DIAGRAMAS = {
    "comp-for-enumera": comp_for_enumera,
    "comp-g-autorreferente": comp_g_autorreferente,
    "comp-verdadero-demostrable": comp_verdadero_demostrable,
    "comp-con-f": comp_con_f,
    "comp-mismo-esqueleto": comp_mismo_esqueleto,
    "comp-cantor": comp_cantor,
    "comp-existir-exhibir": comp_existir_exhibir,
    "comp-que-es-demostracion": comp_que_es_demostracion,
    "comp-aritmetizacion": comp_aritmetizacion,
    "comp-cortocircuito": comp_cortocircuito,
    "comp-cuadricula": comp_cuadricula,
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
