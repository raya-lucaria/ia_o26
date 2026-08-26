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


DIAGRAMAS = {
    "comp-esencia": comp_esencia,
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
