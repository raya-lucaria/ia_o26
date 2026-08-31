"""Genera los diagramas SVG de la unidad de complejidad.

Mismo patron que gen_computabilidad.py: paleta en constantes, una funcion por
diagrama que devuelve una cadena SVG completa, y un catalogo DIAGRAMAS que el
generador y su prueba comparten como unica fuente de "que diagramas existen".

Los ids llevan prefijo "cx-" a proposito: los ids de objeto numerado de Raya
son unicos en TODO el curso, no por pagina. "comp-" ya lo ocupa la unidad de
computabilidad y varios diagramas de aqui son su contraparte directa
(comp-tres-clases / cx-tres-clases), asi que sin prefijo propio chocarian.
"""
import sys
from xml.sax.saxutils import escape

from unidades import ASSETS_COMPLEJIDAD

ASSETS = ASSETS_COMPLEJIDAD

# Paleta del skin eva-cyberpunk, identica a gen_computabilidad.py. FONDO es
# tokens.color.surface y va horneado en cada SVG: test_9 de test_aceptacion.py
# falla sin el.
FONDO, TEXTO, SUAVE, LINEA = "#211033", "#f7f2ff", "#c8b9d8", "#78419e"
ACENTO = "#f04cff"
SERIE = ["#a8ff5a", "#55ddff", "#ffd166"]
# Un cuarto color para las curvas de crecimiento: cinco curvas en la misma
# grafica no caben en SERIE, y el rojo solo se usa donde "esto explota" es
# justamente lo que hay que leer.
ALARMA = "#ff5a7a"
FUENTE = "system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


def marco(ancho, alto, aria):
    """Etiqueta <svg> raiz con los cinco atributos que exigen las guardas.

    width/height explicitos ademas de viewBox: el sitio incrusta estos SVG con
    <img>, y sin tamano intrinseco el navegador cae al tamano por omision de un
    elemento reemplazado (~300x150 CSS px) en vez de llenar el contenedor de la
    figura. Misma convencion que gen_computabilidad.py.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
        f'viewBox="0 0 {ancho} {alto}" role="img" aria-label="{escape(aria)}">'
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

    Se mezcla aqui en vez de emitir fill-opacity porque el SVG viaja tambien a
    renderizadores pobres (el <img> del sitio esta bien, pero las capturas y
    las hojas de contacto se hacen con ImageMagick, que ignora la opacidad y
    pinta el rectangulo a todo color, tapando las curvas que hay debajo). Un
    color ya mezclado se ve igual en todos.
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


def curva_puntos(puntos, color, grosor=2.5, guiones=None):
    """Polilinea a partir de una lista de pares (x, y) ya en coordenadas SVG."""
    d = " ".join(
        ("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}"
        for i, (x, y) in enumerate(puntos)
    )
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}" '
        f'stroke-linecap="round" stroke-linejoin="round"{trazo}/>'
    )


# --- Pagina 1 · que es n ------------------------------------------------------


def cx_que_es_n():
    """Pagina 1. El tamano de la entrada no siempre es lo que uno cree.

    Los tres paneles son los tres tropiezos, en orden de frecuencia: la lista
    (facil), el grafo (son DOS numeros) y el entero (n es la cantidad de
    digitos, no el numero). El tercero es el que rompe la intuicion y por eso
    lleva el recuadro de aviso.
    """
    ancho, alto = 980, 400
    aria = (
        "Tres paneles con la misma pregunta '¿cuanto mide la entrada?': una "
        "lista de numeros mide n elementos, un grafo mide dos numeros (n "
        "vertices y m aristas), y un entero mide sus digitos, no su valor"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "¿Cuánto mide la entrada?", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La misma pregunta, tres respuestas distintas. Equivocarse aquí "
            "invalida todo lo que venga después.",
            SUAVE, 13.5,
        )
    )

    # Panel 1: una lista
    x0 = 40
    p.append(caja(x0, 96, 280, 216, borde=SERIE[1]))
    p.append(texto(x0 + 140, 126, "Una lista", SERIE[1], 16, peso="600"))
    for i, v in enumerate(["7", "2", "9", "4", "1"]):
        x = x0 + 36 + i * 42
        p.append(caja(x, 152, 36, 36, borde=SUAVE, radio=6, grosor=1.5))
        p.append(texto(x + 18, 177, v, TEXTO, 16))
    p.append(texto(x0 + 140, 224, "n = 5", TEXTO, 19, peso="600"))
    p.append(texto(x0 + 140, 250, "cuántos elementos hay", SUAVE, 13))
    p.append(texto(x0 + 140, 288, "Sin sorpresa.", SERIE[1], 13.5, peso="600"))

    # Panel 2: un grafo
    x0 = 350
    p.append(caja(x0, 96, 280, 216, borde=SERIE[0]))
    p.append(texto(x0 + 140, 126, "Un grafo", SERIE[0], 16, peso="600"))
    vs = [(x0 + 70, 168), (x0 + 140, 148), (x0 + 210, 172), (x0 + 105, 214), (x0 + 185, 216)]
    aristas = [(0, 1), (1, 2), (0, 3), (3, 4), (4, 2), (1, 4)]
    for a, b in aristas:
        p.append(linea(vs[a][0], vs[a][1], vs[b][0], vs[b][1], SUAVE, 1.5))
    for x, y in vs:
        p.append(punto(x, y, 7, SERIE[0]))
    p.append(texto(x0 + 140, 254, "n = 5   y   m = 6", TEXTO, 19, peso="600"))
    p.append(texto(x0 + 140, 288, "Son DOS números.", SERIE[0], 13.5, peso="600"))

    # Panel 3: un entero
    x0 = 660
    p.append(caja(x0, 96, 280, 216, borde=ALARMA))
    p.append(texto(x0 + 140, 126, "Un número entero", ALARMA, 16, peso="600"))
    p.append(texto(x0 + 140, 168, "N = 8 675 309", TEXTO, 20, fuente=MONO))
    p.append(texto(x0 + 140, 200, "n = 7,  no 8 675 309", TEXTO, 17, peso="600"))
    p.append(texto(x0 + 140, 226, "lo que se escribe son los dígitos", SUAVE, 13))
    p.append(caja(x0 + 16, 244, 248, 54, borde=ALARMA, radio=8, grosor=1.5, guiones="4 3"))
    p.append(texto(x0 + 140, 265, "n ≈ log N", ALARMA, 15, peso="600"))
    p.append(texto(x0 + 140, 286, "el número es exponencial en n", SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2, 352,
            "Un algoritmo que recorre de 1 a N no es lineal: es exponencial en "
            "el tamaño de su entrada.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 376,
            "Ese es el error clásico, y se llama complejidad pseudopolinomial.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_peor_caso():
    """Pagina 1. Peor caso, caso promedio y mejor caso sobre el mismo tamano.

    La nube de puntos importa: hay MUCHAS entradas de tamano n y cada una tarda
    lo suyo. Las tres lineas son tres maneras de resumir esa nube en un numero.
    """
    ancho, alto = 940, 400
    aria = (
        "Una nube de puntos: cada punto es una entrada distinta de tamano n y "
        "su altura es lo que tarda. Tres lineas horizontales marcan el mejor "
        "caso abajo, el caso promedio en medio y el peor caso arriba"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Muchas entradas del mismo tamaño", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Fijas n y todavía te quedan millones de entradas. Cada punto es "
            "una; su altura es lo que tarda.",
            SUAVE, 13.5,
        )
    )

    ix, iy, iw, ih = 90, 100, 560, 220
    p.append(linea(ix, iy + ih, ix + iw, iy + ih, SUAVE, 2))
    p.append(linea(ix, iy, ix, iy + ih, SUAVE, 2))
    p.append(texto(ix + iw / 2, iy + ih + 30, "todas las entradas de tamaño n", SUAVE, 13))
    p.append(
        f'<text x="{ix - 26}" y="{iy + ih / 2}" fill="{SUAVE}" '
        f'font-family="{FUENTE}" font-size="13" text-anchor="middle" '
        f'transform="rotate(-90 {ix - 26} {iy + ih / 2})">pasos que tarda</text>'
    )

    # Nube: alturas elegidas a mano para que la mayoria quede baja y unas
    # pocas entradas patologicas se despeguen hacia arriba.
    nube = [
        (0.04, 0.80), (0.09, 0.72), (0.13, 0.86), (0.17, 0.66), (0.21, 0.78),
        (0.25, 0.60), (0.29, 0.83), (0.33, 0.71), (0.37, 0.55), (0.41, 0.76),
        (0.45, 0.64), (0.49, 0.88), (0.53, 0.58), (0.57, 0.74), (0.61, 0.68),
        (0.65, 0.81), (0.69, 0.62), (0.73, 0.70), (0.77, 0.52), (0.81, 0.79),
        (0.85, 0.67), (0.89, 0.73), (0.93, 0.61), (0.97, 0.84),
        (0.31, 0.22), (0.62, 0.14), (0.88, 0.26), (0.11, 0.30),
    ]
    for fx, fy in nube:
        cx, cy = ix + fx * iw, iy + fy * ih
        color = ALARMA if fy < 0.35 else SUAVE
        p.append(punto(cx, cy, 4.5, color))

    marcas = [
        (0.14, "peor caso", ALARMA, "lo que garantiza el análisis"),
        (0.70, "caso promedio", SERIE[2], "necesita saber qué entradas llegan"),
        (0.92, "mejor caso", SERIE[1], "no sirve para nada"),
    ]
    for fy, etiqueta, color, glosa in marcas:
        y = iy + fy * ih
        p.append(linea(ix, y, ix + iw, y, color, 2, guiones="6 5"))
        p.append(texto(ix + iw + 16, y - 4, etiqueta, color, 14.5, anclaje="start", peso="600"))
        p.append(texto(ix + iw + 16, y + 15, glosa, SUAVE, 12, anclaje="start"))

    p.append(
        texto(
            ancho / 2, 372,
            "En este curso, «complejidad» significa siempre el peor caso: es la "
            "única de las tres que promete algo.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 2 · la notacion asintotica ----------------------------------------


def _ejes(p, ix, iy, iw, ih, etiqueta_x="n", etiqueta_y="pasos"):
    """Ejes en L con sus dos etiquetas. Devuelve nada; escribe sobre p."""
    p.append(linea(ix, iy + ih, ix + iw + 14, iy + ih, SUAVE, 2, ))
    p.append(linea(ix, iy - 10, ix, iy + ih, SUAVE, 2))
    p.append(texto(ix + iw + 6, iy + ih + 24, etiqueta_x, SUAVE, 13))
    p.append(
        f'<text x="{ix - 30}" y="{iy + ih / 2}" fill="{SUAVE}" '
        f'font-family="{FUENTE}" font-size="13" text-anchor="middle" '
        f'transform="rotate(-90 {ix - 30} {iy + ih / 2})">{etiqueta_y}</text>'
    )


def cx_o_grande():
    """Pagina 2. La definicion de O, dibujada: c·g(n) por encima DESDE n0.

    Las dos cosas que la definicion permite y que nadie recuerda estan aqui
    marcadas a proposito: la constante c (la curva de arriba es g escalada, no
    g) y el tramo previo a n0, donde f puede ir por encima sin que importe.
    """
    ancho, alto = 940, 430
    aria = (
        "Dos curvas sobre unos ejes: f de n y c por g de n. Antes de n cero f "
        "va por encima y no importa; a partir de n cero c por g queda siempre "
        "arriba, que es lo unico que exige la definicion de O grande"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "f(n) = O(g(n)), dibujado", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Existen una constante c y un punto n₀ tales que, de n₀ en "
            "adelante, f nunca pasa por encima de c·g.",
            SUAVE, 13.5,
        )
    )

    ix, iy, iw, ih = 100, 104, 620, 236
    nmax, vmax = 60.0, 15000.0

    def punto_xy(n, v):
        return (ix + n / nmax * iw, iy + ih - min(v, vmax) / vmax * ih)

    f = lambda n: 2 * n * n + 3000                    # noqa: E731
    cg = lambda n: 4 * n * n                          # noqa: E731

    # 2n^2 + 3000 <= 4n^2 en cuanto n^2 >= 1500, es decir desde n = 39. El
    # termino constante grande es a proposito: con el, el tramo previo a n0
    # --lo unico que esta figura tiene que ensenar-- se ve, en vez de quedar
    # aplastado contra el origen.
    n0 = 39
    x0 = ix + n0 / nmax * iw

    # El sombreado va ANTES que las curvas: pintado despues las tapa.
    p.append(
        f'<rect x="{ix}" y="{iy - 6}" width="{x0 - ix:.1f}" height="{ih + 6}" '
        f'fill="{mezclar(ALARMA, 0.16)}"/>'
    )
    _ejes(p, ix, iy, iw, ih)

    pf = [punto_xy(n, f(n)) for n in range(0, 61)]
    pcg = [punto_xy(n, cg(n)) for n in range(0, 61)]
    pg = [punto_xy(n, n * n) for n in range(0, 61)]

    p.append(curva_puntos(pg, LINEA, 2, guiones="5 6"))
    p.append(curva_puntos(pcg, SERIE[1], 2.8))
    p.append(curva_puntos(pf, ACENTO, 3))

    p.append(linea(x0, iy - 6, x0, iy + ih, TEXTO, 1.8, guiones="5 5"))
    p.append(punto(*punto_xy(n0, cg(n0)), 6, TEXTO))
    p.append(texto(x0, iy + ih + 24, "n₀ = 39", TEXTO, 14, peso="600"))
    p.append(texto((ix + x0) / 2, iy + 62, "aquí f va por ENCIMA", ALARMA, 13.5, peso="600"))
    p.append(texto((ix + x0) / 2, iy + 82, "y no importa", ALARMA, 13.5, peso="600"))
    p.append(texto(x0 + 116, iy + 40, "aquí ya no, y nunca más", SERIE[1], 13.5, peso="600"))

    etiquetas = [
        (pcg[-1], "c·g(n) = 4n²", SERIE[1]),
        (pf[-1], "f(n) = 2n² + 3000", ACENTO),
        (pg[-1], "g(n) = n²", LINEA),
    ]
    for (px, py), etiqueta, color in etiquetas:
        p.append(texto(px + 10, py + 5, etiqueta, color, 13.5, anclaje="start", peso="600"))

    p.append(
        texto(
            ancho / 2, 388,
            "La constante c y el arranque n₀ son lo que hace que O ignore "
            "constantes y términos de orden menor.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 410,
            "Con c = 4 basta, y f nunca vuelve a pasar de 4n² desde n₀ = 39.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_familia_asintotica():
    """Pagina 2. O, Omega, Theta y o pequena en un solo golpe de vista.

    Cada panel lleva su version con limite abajo, que es la que se usa para
    decidir casos concretos; el dibujo es para acordarse de cual es cual.
    """
    ancho, alto = 980, 430
    aria = (
        "Cuatro paneles: O grande como techo, Omega como piso, Theta como las "
        "dos cosas a la vez, y o pequena como un techo del que f se despega. "
        "Cada uno con su definicion por limites"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Los cuatro, y cuál dice qué", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Lee el dibujo para acordarte de cuál es cuál; usa el límite para "
            "decidir un caso concreto.",
            SUAVE, 13.5,
        )
    )

    paneles = [
        ("O(g)", "techo", "f crece a lo más como g",
         "lím sup f/g  <  ∞", SERIE[1], "techo"),
        ("Ω(g)", "piso", "f crece al menos como g",
         "lím inf f/g  >  0", SERIE[0], "piso"),
        ("Θ(g)", "las dos", "f crece exactamente como g",
         "0 < lím f/g < ∞", SERIE[2], "ambos"),
        ("o(g)", "techo que se abre", "f crece estrictamente menos que g",
         "lím f/g  =  0", ALARMA, "despega"),
    ]

    pw, ph = 218, 214
    for i, (simbolo, mote, glosa, limite, color, forma) in enumerate(paneles):
        x0 = 26 + i * (pw + 14)
        p.append(caja(x0, 96, pw, ph, borde=color))
        p.append(texto(x0 + pw / 2, 126, simbolo, color, 22, peso="600"))
        p.append(texto(x0 + pw / 2, 148, mote, SUAVE, 13))

        gx, gy, gw, gh = x0 + 34, 162, pw - 68, 74
        p.append(linea(gx, gy + gh, gx + gw, gy + gh, SUAVE, 1.5))
        p.append(linea(gx, gy, gx, gy + gh, SUAVE, 1.5))

        def curva_pot(exp, escala, col, grosor=2.4, guiones=None):
            pts = [
                (gx + t / 20 * gw, gy + gh - min((t / 20.0) ** exp * escala, 1.0) * gh)
                for t in range(21)
            ]
            return curva_puntos(pts, col, grosor, guiones)

        if forma == "techo":
            p.append(curva_pot(2.0, 1.0, color, 2.4, "5 4"))
            p.append(curva_pot(2.0, 0.55, ACENTO, 2.6))
        elif forma == "piso":
            p.append(curva_pot(2.0, 0.5, color, 2.4, "5 4"))
            p.append(curva_pot(2.0, 0.95, ACENTO, 2.6))
        elif forma == "ambos":
            p.append(curva_pot(2.0, 1.0, color, 2.2, "5 4"))
            p.append(curva_pot(2.0, 0.42, color, 2.2, "5 4"))
            p.append(curva_pot(2.0, 0.68, ACENTO, 2.6))
        else:  # despega
            p.append(curva_pot(2.0, 1.0, color, 2.4, "5 4"))
            p.append(curva_pot(1.0, 0.55, ACENTO, 2.6))

        p.append(texto(x0 + pw / 2, 262, glosa, TEXTO, 12.5))
        p.append(caja(x0 + 14, 274, pw - 28, 30, borde=color, radio=7, grosor=1.4))
        p.append(texto(x0 + pw / 2, 294, limite, color, 14, peso="600", fuente=MONO))

    p.append(texto(ancho / 2, 344, "La curva llena es siempre f. La punteada es g.", SUAVE, 13))
    p.append(
        texto(
            ancho / 2, 380,
            "Θ es la que casi siempre quieres decir cuando dices O.",
            TEXTO, 15, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 404,
            "Decir «este algoritmo es O(n²)» es cierto también si es O(n³) y si "
            "es lineal: O solo promete un techo.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 3 · contar un algoritmo -------------------------------------------


def cx_escalera():
    """Pagina 3. Los cuatro algoritmos de la pagina, por lo que cuesta duplicar n.

    La columna que importa no es la del medio sino la de la derecha: "si
    duplicas n" es lo que convierte una formula en una intuicion.
    """
    ancho, alto = 960, 430
    aria = (
        "Cuatro escalones ascendentes, uno por algoritmo: busqueda binaria con "
        "log n, busqueda lineal con n, multiplicacion de matrices con n al "
        "cubo y todos los subconjuntos con dos a la n. Cada uno dice que pasa "
        "al duplicar n"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "La escalera, y qué pasa si duplicas n", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La fórmula se olvida. La columna de la derecha, no.",
            SUAVE, 13.5,
        )
    )

    filas = [
        ("Búsqueda binaria", "log n", "un paso más", SERIE[0], 0),
        ("Búsqueda lineal", "n", "el doble de trabajo", SERIE[1], 1),
        ("Multiplicar matrices", "n³", "ocho veces más", SERIE[2], 2),
        ("Todos los subconjuntos", "2ⁿ", "el trabajo AL CUADRADO", ALARMA, 3),
    ]
    fh, base = 66, 336
    for nombre, formula, efecto, color, i in filas:
        y = base - i * fh
        w = 240 + i * 120
        p.append(caja(60, y - 46, w, 52, borde=color, radio=9))
        p.append(texto(78, y - 16, nombre, TEXTO, 15, anclaje="start", peso="600"))
        p.append(texto(60 + w - 18, y - 16, formula, color, 19, anclaje="end", peso="600"))
        p.append(texto(60 + w + 16, y - 21, efecto, color, 14, anclaje="start", peso="600"))
        p.append(texto(60 + w + 16, y - 3, "al duplicar n", SUAVE, 11.5, anclaje="start"))

    p.append(
        texto(
            ancho / 2, 380,
            "Los tres primeros escalones son el mismo mundo. El cuarto es otro.",
            TEXTO, 15, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 404,
            "Esa frontera —polinomio contra exponencial— es de lo que trata el "
            "resto de la unidad.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_matrices():
    """Pagina 3. De donde sale el n cubo: n celdas por lado, n productos cada una.

    Se dibuja la celda (i,j) de C con su fila y su columna resaltadas porque el
    conteo se sigue del dibujo: una celda cuesta n, y hay n**2 celdas.
    """
    ancho, alto = 960, 420
    aria = (
        "Tres cuadriculas: A por B igual a C. En A se resalta una fila, en B "
        "una columna, y en C la unica celda que producen. Debajo, la cuenta: n "
        "productos por celda y n al cuadrado celdas dan n al cubo"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Multiplicar dos matrices n×n", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "El n³ no hay que memorizarlo: se lee del dibujo.",
            SUAVE, 13.5,
        )
    )

    k, celda = 5, 34
    fila_res, col_res = 1, 3

    def cuadricula(x0, y0, nombre, color, resaltar):
        p.append(texto(x0 + k * celda / 2, y0 - 14, nombre, color, 18, peso="600"))
        for r in range(k):
            for c in range(k):
                x, y = x0 + c * celda, y0 + r * celda
                marcado = resaltar(r, c)
                p.append(
                    caja(x, y, celda, celda,
                         relleno=color if marcado else "none",
                         borde=color if marcado else LINEA,
                         radio=4, grosor=1.4)
                )

    y0 = 128
    cuadricula(90, y0, "A", SERIE[1], lambda r, c: r == fila_res)
    p.append(texto(90 + k * celda + 30, y0 + k * celda / 2 + 6, "×", TEXTO, 26))
    cuadricula(90 + k * celda + 60, y0, "B", SERIE[0], lambda r, c: c == col_res)
    p.append(texto(90 + 2 * k * celda + 90, y0 + k * celda / 2 + 6, "=", TEXTO, 26))
    cuadricula(90 + 2 * k * celda + 120, y0, "C", ACENTO,
               lambda r, c: r == fila_res and c == col_res)

    p.append(
        texto(
            90 + 2 * k * celda + 120 + k * celda + 26,
            y0 + fila_res * celda + celda / 2 + 6,
            "una celda", ACENTO, 14, anclaje="start", peso="600",
        )
    )

    cuentas = [
        ("una fila × una columna", "n productos y n−1 sumas", SERIE[1]),
        ("celdas que hay que llenar", "n × n = n² celdas", SERIE[0]),
        ("el total", "n² · n = n³", ACENTO),
    ]
    for i, (que, cuanto, color) in enumerate(cuentas):
        x0 = 70 + i * 285
        p.append(caja(x0, 322, 262, 60, borde=color, radio=9))
        p.append(texto(x0 + 131, 344, que, SUAVE, 12.5))
        p.append(texto(x0 + 131, 368, cuanto, color, 16, peso="600"))

    p.append(
        texto(
            ancho / 2, 404,
            "Θ(n³) — y no es óptimo: Strassen (1969) lo bajó a n^2,807, y "
            "nadie sabe cuál es el mínimo.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_crecimiento():
    """Pagina 3. Las cinco curvas en escala logaritmica.

    Escala log en el eje vertical por necesidad: en escala lineal 2**n aplasta
    todo lo demas contra el eje y la grafica no ensena nada. La consecuencia
    hay que decirla en la propia figura, porque una curva "casi recta" en log
    engana: cada raya vale mil veces la anterior.
    """
    import math

    ancho, alto = 960, 470
    aria = (
        "Cinco curvas de crecimiento en escala logaritmica: log n, n, n log n, "
        "n al cuadrado y dos a la n, para n de 1 a 60. Dos a la n atraviesa "
        "toda la grafica mientras las demas siguen pegadas abajo"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Cinco crecimientos, misma gráfica", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Escala logarítmica: cada raya horizontal vale mil veces la de abajo.",
            SUAVE, 13.5,
        )
    )

    ix, iy, iw, ih = 100, 100, 620, 268
    nmin, nmax = 1, 60
    dec_min, dec_max = 0.0, 18.0  # de 1 a 10^18 pasos

    def xy(n, v):
        x = ix + (n - nmin) / (nmax - nmin) * iw
        d = max(min(math.log10(max(v, 1.0)), dec_max), dec_min)
        return (x, iy + ih - (d - dec_min) / (dec_max - dec_min) * ih)

    for d in range(0, 19, 3):
        y = iy + ih - d / dec_max * ih
        p.append(linea(ix, y, ix + iw, y, LINEA, 1, guiones="3 6"))
        etiqueta = "1" if d == 0 else f"10^{d}"
        p.append(texto(ix - 12, y + 5, etiqueta, SUAVE, 11.5, anclaje="end", fuente=MONO))
    p.append(linea(ix, iy + ih, ix + iw, iy + ih, SUAVE, 2))
    p.append(linea(ix, iy - 10, ix, iy + ih, SUAVE, 2))
    for n in (1, 10, 20, 30, 40, 50, 60):
        x = ix + (n - nmin) / (nmax - nmin) * iw
        p.append(texto(x, iy + ih + 22, str(n), SUAVE, 11.5, fuente=MONO))
    p.append(texto(ix + iw + 20, iy + ih + 22, "n", SUAVE, 13.5))
    p.append(
        f'<text x="{ix - 58}" y="{iy + ih / 2}" fill="{SUAVE}" '
        f'font-family="{FUENTE}" font-size="13" text-anchor="middle" '
        f'transform="rotate(-90 {ix - 58} {iy + ih / 2})">pasos</text>'
    )

    curvas = [
        ("log₂ n", lambda n: math.log2(n) if n > 1 else 1.0, LINEA),
        ("n", lambda n: float(n), SERIE[1]),
        ("n log₂ n", lambda n: n * math.log2(n) if n > 1 else 1.0, SERIE[0]),
        ("n²", lambda n: float(n * n), SERIE[2]),
        ("2ⁿ", lambda n: 2.0 ** n, ALARMA),
    ]
    for etiqueta, f, color in curvas:
        pts = [xy(n, f(n)) for n in range(nmin, nmax + 1)]
        p.append(curva_puntos(pts, color, 2.8))
        px, py = pts[-1]
        p.append(texto(px + 10, py + 5, etiqueta, color, 14.5, anclaje="start", peso="600"))

    # Marca donde 2**n cruza "un segundo" (10^9 pasos) y "la edad del universo".
    for pasos, glosa in ((1e9, "≈ 1 segundo"), (1e17, "≈ 3 años")):
        n_cruce = math.log2(pasos)
        x, y = xy(n_cruce, pasos)
        p.append(punto(x, y, 5.5, TEXTO))
        p.append(texto(x - 10, y - 10, f"2ⁿ con n = {round(n_cruce)}: {glosa}",
                       TEXTO, 12.5, anclaje="end", peso="600"))

    p.append(
        texto(
            ancho / 2, 424,
            "A n = 60, un algoritmo 2ⁿ pide 10¹⁸ pasos: décadas de cómputo. Uno "
            "n² pide 3 600.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 448,
            "Y n = 60 es una entrada ridículamente pequeña.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 4 · por que importa -----------------------------------------------


def cx_frontera():
    """Pagina 4. Comprar una maquina el doble de rapida, y que compras con eso.

    Es el argumento decisivo a favor de que el corte sea "polinomial" y no un
    umbral de segundos: con hardware mejor, un polinomio gana un FACTOR de
    entrada y un exponencial gana un SUMANDO. La brecha no la cierra ninguna
    generacion de maquinas.
    """
    ancho, alto = 960, 420
    aria = (
        "Cuatro barras que comparan que tamano de entrada se vuelve alcanzable "
        "al duplicar la velocidad de la maquina: n lineal duplica el tamano, n "
        "al cuadrado lo multiplica por 1.41, n al cubo por 1.26 y dos a la n "
        "solo suma uno"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Compras una máquina el doble de rápida", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "¿Cuánto más grande puede ser la entrada que alcanzas a resolver?",
            SUAVE, 13.5,
        )
    )

    filas = [
        ("n", "n × 2", "el doble de entrada", SERIE[1], 1.00),
        ("n²", "n × 1,41", "un 41 % más", SERIE[0], 0.62),
        ("n³", "n × 1,26", "un 26 % más", SERIE[2], 0.44),
        ("2ⁿ", "n + 1", "UNA unidad más. Una.", ALARMA, 0.05),
    ]
    bx, bw = 300, 400
    for i, (formula, ganancia, glosa, color, frac) in enumerate(filas):
        y = 116 + i * 60
        p.append(texto(bx - 24, y + 22, formula, color, 20, anclaje="end", peso="600"))
        p.append(caja(bx, y, bw, 34, borde=LINEA, radio=7, grosor=1.2))
        p.append(
            f'<rect x="{bx}" y="{y}" width="{max(bw * frac, 8):.0f}" height="34" '
            f'rx="7" fill="{color}" opacity="0.85"/>'
        )
        p.append(texto(bx + bw + 18, y + 16, ganancia, color, 15, anclaje="start", peso="600"))
        p.append(texto(bx + bw + 18, y + 32, glosa, SUAVE, 12, anclaje="start"))

    p.append(
        texto(
            ancho / 2, 384,
            "Un polinomio gana un FACTOR con mejor hardware. Un exponencial "
            "gana un SUMANDO.",
            TEXTO, 15, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 406,
            "Por eso la frontera se traza en «polinomial», y no en «tarda menos "
            "de una hora»: la primera sobrevive al progreso.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_dijkstra_vs_tsp():
    """Pagina 4. El mismo grafo, dos preguntas, dos mundos.

    Es el par que mejor rompe la idea de "problema dificil = problema grande":
    la entrada es identica, byte por byte, y lo unico que cambia es la
    pregunta.
    """
    ancho, alto = 960, 440
    aria = (
        "El mismo grafo de seis ciudades dibujado dos veces. A la izquierda la "
        "pregunta del camino mas corto entre dos ciudades, que se resuelve en "
        "milisegundos con Dijkstra. A la derecha la pregunta del tour mas "
        "corto que pasa por todas, que es NP-completa"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "El mismo grafo, dos preguntas", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La entrada es idéntica. Lo único que cambia es qué se pregunta.",
            SUAVE, 13.5,
        )
    )

    vs_rel = [(0.18, 0.30), (0.52, 0.14), (0.86, 0.34), (0.80, 0.76), (0.46, 0.90), (0.14, 0.68)]
    aristas = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (1, 4), (2, 5)]
    nombres = ["A", "B", "C", "D", "E", "F"]

    def dibujar(x0, y0, w, h, camino, color, cerrado):
        pts = [(x0 + fx * w, y0 + fy * h) for fx, fy in vs_rel]
        for a, b in aristas:
            p.append(linea(pts[a][0], pts[a][1], pts[b][0], pts[b][1], LINEA, 1.5))
        recorrido = camino + [camino[0]] if cerrado else camino
        for a, b in zip(recorrido, recorrido[1:]):
            p.append(linea(pts[a][0], pts[a][1], pts[b][0], pts[b][1], color, 4))
        for i, (x, y) in enumerate(pts):
            p.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{FONDO}" '
                     f'stroke="{color if i in camino else SUAVE}" stroke-width="2"/>')
            p.append(texto(x, y + 5, nombres[i], TEXTO, 13, peso="600"))

    paneles = [
        (40, "«¿Cuál es el camino más corto de A a C?»", [0, 1, 2], SERIE[0], False,
         "Dijkstra", "O(m + n log n)", "milisegundos con un millón de nodos", "P"),
        (500, "«¿Cuál es el tour más corto que pasa por todas?»",
         [0, 1, 2, 3, 4, 5], ALARMA, True,
         "nadie sabe", "ningún algoritmo polinomial conocido", "y no lo hay para 40 ciudades",
         "NP-completo"),
    ]
    for x0, pregunta, camino, color, cerrado, algo, coste, glosa, clase in paneles:
        p.append(caja(x0, 92, 420, 302, borde=color))
        p.append(caja(x0 + 152, 104, 116, 28, borde=color, radio=14, grosor=1.5))
        p.append(texto(x0 + 210, 123, clase, color, 13.5, peso="600"))
        p.append(texto(x0 + 210, 156, pregunta, TEXTO, 14, peso="600"))
        dibujar(x0 + 60, 172, 300, 138, camino, color, cerrado)
        p.append(linea(x0 + 24, 324, x0 + 396, 324, LINEA, 1.2, guiones="4 4"))
        p.append(texto(x0 + 210, 348, algo, color, 17, peso="600"))
        p.append(texto(x0 + 210, 368, coste, SUAVE, 12.5))
        p.append(texto(x0 + 210, 386, glosa, SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2, 420,
            "«Difícil» no es una propiedad del tamaño de la entrada. Es una "
            "propiedad de la pregunta.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 5 · espacio -------------------------------------------------------


def cx_espacio_se_reusa():
    """Pagina 5. La asimetria que explica por que el espacio rinde mas.

    Un paso de tiempo se gasta y no vuelve; una celda de memoria se sobrescribe
    y vuelve a servir. De ahi salen las dos consecuencias que la pagina usa
    despues: espacio <= tiempo, y PSPACE mucho mas grande que P.
    """
    ancho, alto = 960, 400
    aria = (
        "Dos filas comparadas: arriba, ocho pasos de tiempo que se consumen uno "
        "tras otro y no se recuperan; abajo, tres celdas de memoria que se "
        "sobrescriben una y otra vez a lo largo de esos mismos ocho pasos"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "El tiempo se gasta; la memoria se reusa", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Toda la diferencia entre las dos medidas está en esta asimetría.",
            SUAVE, 13.5,
        )
    )

    celda, x0 = 60, 200
    p.append(texto(170, 138, "TIEMPO", SERIE[2], 15, anclaje="end", peso="600"))
    p.append(texto(170, 158, "8 pasos", SUAVE, 12.5, anclaje="end"))
    for i in range(8):
        x = x0 + i * (celda + 8)
        p.append(caja(x, 118, celda, 46, relleno=SERIE[2], borde=SERIE[2], radio=7))
        p.append(texto(x + celda / 2, 147, str(i + 1), FONDO, 15, peso="600"))
    p.append(texto(x0 + 4 * (celda + 8), 190, "cada uno se paga una vez y no vuelve",
                   SUAVE, 12.5))

    p.append(texto(170, 258, "MEMORIA", SERIE[1], 15, anclaje="end", peso="600"))
    p.append(texto(170, 278, "3 celdas", SUAVE, 12.5, anclaje="end"))
    escrituras = ["a", "b", "c"]
    for i in range(3):
        x = x0 + i * (celda + 8)
        p.append(caja(x, 238, celda, 46, borde=SERIE[1], radio=7))
        p.append(texto(x + celda / 2, 267, escrituras[i], SERIE[1], 16, peso="600"))
    for i in range(3):
        x = x0 + i * (celda + 8) + celda / 2
        p.append(
            f'<path d="M {x - 18} {232} C {x - 30} {206}, {x + 30} {206}, '
            f'{x + 18} {232}" fill="none" stroke="{SERIE[1]}" '
            f'stroke-width="1.6" marker-end="url(#s)"/>'
        )
    p.append(texto(x0 + 4 * (celda + 8), 267, "las mismas tres celdas, escritas ocho veces",
                   SUAVE, 12.5, anclaje="start"))

    conclusiones = [
        ("Espacio ≤ Tiempo", "en t pasos no puedes tocar más de t celdas", SERIE[0]),
        ("Tiempo NO ≤ Espacio", "con poca memoria puedes tardar muchísimo", ALARMA),
    ]
    for i, (titulo, glosa, color) in enumerate(conclusiones):
        x = 130 + i * 400
        p.append(caja(x, 306, 340, 58, borde=color, radio=9))
        p.append(texto(x + 170, 330, titulo, color, 16, peso="600"))
        p.append(texto(x + 170, 352, glosa, SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2, 388,
            "Por eso PSPACE contiene a NP: con memoria acotada puedes probar "
            "todos los certificados, uno tras otro, reusando el mismo espacio.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_memoria_logaritmica():
    """Pagina 5. Que cabe en O(log n) de memoria: indices, no datos.

    La clave contraintuitiva es que la entrada NO cuenta como espacio usado —es
    de solo lectura—, y por eso "memoria logaritmica" no significa "cabe el
    problema en la cabeza" sino "cabe un punterito".
    """
    ancho, alto = 960, 380
    aria = (
        "Una cinta de entrada larga y de solo lectura, y al lado una libreta "
        "diminuta con espacio para dos indices. La libreta es lo unico que "
        "cuenta como memoria usada"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Qué cabe en memoria logarítmica", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La entrada es de solo lectura y no cuenta. Solo cuenta lo que "
            "escribes aparte.",
            SUAVE, 13.5,
        )
    )

    celda = 32
    x0, y0 = 60, 130
    p.append(texto(x0, y0 - 16, "la entrada · solo lectura · no cuenta", SUAVE, 13, anclaje="start"))
    simbolos = "1011001110100110101100"
    for i, s in enumerate(simbolos):
        x = x0 + i * celda
        p.append(caja(x, y0, celda, celda, borde=LINEA, radio=4, grosor=1.2))
        p.append(texto(x + celda / 2, y0 + 22, s, SUAVE, 14, fuente=MONO))
    p.append(texto(x0 + len(simbolos) * celda + 16, y0 + 22, "…  n símbolos",
                   SUAVE, 13, anclaje="start"))
    for idx, color, nombre in ((3, SERIE[0], "i"), (14, SERIE[2], "j")):
        x = x0 + idx * celda + celda / 2
        p.append(flecha(x, y0 + celda + 34, x, y0 + celda + 6, color, 2))
        p.append(texto(x, y0 + celda + 52, nombre, color, 14, peso="600"))

    p.append(caja(320, 236, 320, 100, borde=SERIE[1], radio=10))
    p.append(texto(480, 262, "la libreta · esto SÍ cuenta", SERIE[1], 14.5, peso="600"))
    p.append(texto(480, 292, "i = 3        j = 14", TEXTO, 17, fuente=MONO))
    p.append(texto(480, 318, "dos índices: ⌈log₂ n⌉ bits cada uno", SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2, 364,
            "Con n = un millón, la libreta son 40 bits. Eso es la clase L.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 6 · las clases ----------------------------------------------------


def cx_no_determinista():
    """Pagina 6. Determinista es una linea; no determinista es un arbol.

    Lo que hay que leer en el dibujo es el COSTE: el tiempo de la maquina no
    determinista es la PROFUNDIDAD del arbol, no su cantidad de nodos. Sin eso,
    "NP en tiempo polinomial" suena a trampa.
    """
    ancho, alto = 960, 440
    aria = (
        "A la izquierda, una maquina determinista: una sola cadena de "
        "configuraciones. A la derecha, una no determinista: un arbol que se "
        "abre en dos en cada paso, y acepta si alguna hoja acepta"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Una línea, o un árbol", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La máquina no determinista no adivina bien: prueba todo a la vez, "
            "y le cobramos solo la profundidad.",
            SUAVE, 13.5,
        )
    )

    # Izquierda: determinista
    p.append(caja(40, 96, 320, 296, borde=SERIE[1]))
    p.append(texto(200, 124, "Determinista", SERIE[1], 17, peso="600"))
    p.append(texto(200, 145, "en cada paso, una sola opción", SUAVE, 12.5))
    for i in range(5):
        y = 172 + i * 42
        p.append(f'<circle cx="200" cy="{y}" r="13" fill="{FONDO}" '
                 f'stroke="{SERIE[1]}" stroke-width="2"/>')
        if i < 4:
            p.append(flecha(200, y + 14, 200, y + 27, SERIE[1], 1.8))
    p.append(texto(200, 386, "5 pasos = 5 configuraciones", SUAVE, 12.5))

    # Derecha: no determinista
    p.append(caja(400, 96, 520, 296, borde=ACENTO))
    p.append(texto(660, 124, "No determinista", ACENTO, 17, peso="600"))
    p.append(texto(660, 145, "en cada paso, varias opciones a la vez", SUAVE, 12.5))

    niveles = 4
    y0, dy = 172, 56
    aceptante = {1: 0, 2: 1, 3: 3}  # camino que acepta, por nivel
    for nivel in range(niveles):
        n_nodos = 2 ** nivel
        for k in range(n_nodos):
            x = 660 + (k - (n_nodos - 1) / 2) * (440 / max(n_nodos, 1))
            y = y0 + nivel * dy
            en_camino = aceptante.get(nivel, 0) == k if nivel else k == 0
            color = SERIE[0] if en_camino else LINEA
            p.append(f'<circle cx="{x:.1f}" cy="{y}" r="10" fill="{FONDO}" '
                     f'stroke="{color}" stroke-width="2"/>')
            if nivel < niveles - 1:
                n_hijos = 2 ** (nivel + 1)
                for h in (2 * k, 2 * k + 1):
                    hx = 660 + (h - (n_hijos - 1) / 2) * (440 / n_hijos)
                    hijo_en_camino = en_camino and aceptante.get(nivel + 1) == h
                    p.append(linea(x, y + 10, hx, y + dy - 10,
                                   SERIE[0] if hijo_en_camino else LINEA,
                                   2.4 if hijo_en_camino else 1.2))
    p.append(texto(660, 372, "acepta si ALGUNA rama acepta", SERIE[0], 14, peso="600"))

    p.append(
        texto(
            ancho / 2, 418,
            "El tiempo es la PROFUNDIDAD del árbol, no su tamaño. Por eso «NP = "
            "no determinista en tiempo polinomial» no es hacer trampa: es "
            "cobrar solo una rama.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_verificar_vs_buscar():
    """Pagina 6. La definicion util de NP: buscar es caro, verificar es barato.

    Esta es la definicion que se usa en la practica. La del arbol de arriba es
    equivalente y es la historica; esta es la que deja reconocer un problema de
    NP en dos segundos.
    """
    ancho, alto = 960, 420
    aria = (
        "Dos escenas con la misma formula logica: a la izquierda hay que "
        "buscar una asignacion entre dos a la n posibles; a la derecha alguien "
        "te la entrega y solo hay que sustituir y comprobar"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Buscar la respuesta, o comprobarla", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "NP no es «difícil». NP es «si alguien te da la respuesta, la "
            "compruebas rápido».",
            SUAVE, 13.5,
        )
    )

    formula = "(x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₄) ∧ (x₂ ∨ ¬x₃ ∨ ¬x₄)"
    p.append(caja(180, 92, 600, 44, borde=LINEA, radio=9, grosor=1.4))
    p.append(texto(480, 120, formula, TEXTO, 16, fuente=MONO))

    p.append(caja(40, 156, 420, 196, borde=ALARMA))
    p.append(texto(250, 184, "BUSCAR", ALARMA, 17, peso="600"))
    p.append(texto(250, 206, "«¿existe alguna asignación que la satisfaga?»", SUAVE, 12.5))
    for i in range(4):
        for j in range(8):
            x, y = 108 + j * 36, 224 + i * 26
            marcado = (i, j) == (2, 5)
            p.append(caja(x, y, 28, 18, relleno=SERIE[0] if marcado else "none",
                          borde=SERIE[0] if marcado else LINEA, radio=4, grosor=1))
    p.append(texto(250, 340, "2ⁿ candidatas. Una sirve. ¿Cuál?", ALARMA, 13.5, peso="600"))

    p.append(caja(500, 156, 420, 196, borde=SERIE[0]))
    p.append(texto(710, 184, "VERIFICAR", SERIE[0], 17, peso="600"))
    p.append(texto(710, 206, "«te doy ésta: compruébala»", SUAVE, 12.5))
    p.append(caja(560, 222, 300, 40, borde=SERIE[0], radio=8, grosor=1.6))
    p.append(texto(710, 248, "x₁=1  x₂=1  x₃=0  x₄=1", SERIE[0], 16, fuente=MONO))
    p.append(texto(710, 284, "sustituyes y lees: ✓ ✓ ✓", TEXTO, 15, peso="600"))
    p.append(texto(710, 308, "tres cláusulas, tres comprobaciones", SUAVE, 12.5))
    p.append(texto(710, 340, "Tiempo polinomial. Sin dudas.", SERIE[0], 13.5, peso="600"))

    p.append(
        texto(
            ancho / 2, 388,
            "Esa asignación que te entregan se llama certificado, y tiene que "
            "ser de tamaño polinomial.",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 410,
            "P vs NP es exactamente esto: ¿buscar cuesta lo mismo que comprobar?",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_tres_clases():
    """Pagina 6. P, NP y EXP anidadas, con inquilinos concretos.

    Las lineas punteadas entre P y NP son deliberadas: se dibuja lo que NO se
    sabe. La linea entre P y EXP es solida porque el teorema de jerarquia de
    tiempo si separa esas dos, y esa asimetria es justo lo que hay que ver.
    """
    ancho, alto = 960, 480
    aria = (
        "Tres regiones anidadas: P dentro de NP dentro de EXP. El borde entre "
        "P y NP va punteado porque no se sabe si son distintas; el de EXP va "
        "solido porque si se sabe que P es estrictamente menor que EXP"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Quién vive en cada clase", TEXTO, 21, peso="600"))

    p.append(f'<ellipse cx="480" cy="252" rx="430" ry="176" fill="none" '
             f'stroke="{SERIE[2]}" stroke-width="2.5"/>')
    p.append(texto(480, 104, "EXP · tiempo exponencial", SERIE[2], 16, peso="600"))

    p.append(f'<ellipse cx="440" cy="262" rx="316" ry="132" fill="none" '
             f'stroke="{ACENTO}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    p.append(texto(440, 156, "NP · verificable en polinomial", ACENTO, 16, peso="600"))

    p.append(f'<ellipse cx="330" cy="272" rx="180" ry="88" fill="none" '
             f'stroke="{SERIE[0]}" stroke-width="2.5"/>')
    p.append(texto(330, 208, "P · resoluble en polinomial", SERIE[0], 15, peso="600"))

    inquilinos_p = ["Dijkstra", "árbol generador mínimo", "2-SAT", "programación lineal", "primalidad"]
    for i, nombre in enumerate(inquilinos_p):
        p.append(texto(330, 236 + i * 22, nombre, SUAVE, 13))

    inquilinos_np = ["SAT · 3-SAT", "ciclo hamiltoniano", "TSP (decisión)", "clique · coloreo · mochila"]
    for i, nombre in enumerate(inquilinos_np):
        p.append(texto(628, 250 + i * 23, nombre, SUAVE, 13))
    p.append(texto(628, 226, "en NP, no se sabe si en P", ACENTO, 13, peso="600"))

    p.append(texto(838, 262, "ajedrez n×n", SUAVE, 13))
    p.append(texto(838, 240, "solo en EXP", SERIE[2], 13, peso="600"))

    marcas = [
        (250, 418, "P ⊆ NP: seguro", SERIE[0]),
        (480, 418, "P = NP: nadie sabe", ACENTO),
        (730, 418, "P ⊊ EXP: demostrado", SERIE[2]),
    ]
    for x, y, etiqueta, color in marcas:
        p.append(caja(x - 108, y - 20, 216, 32, borde=color, radio=16, grosor=1.5))
        p.append(texto(x, y + 1, etiqueta, color, 13.5, peso="600"))

    p.append(
        texto(
            ancho / 2, 462,
            "El borde punteado es el que no se sabe cerrar. Es el problema "
            "abierto más famoso de la computación.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 7 · azar ----------------------------------------------------------


def cx_monte_carlo():
    """Pagina 7. La maquina con moneda y la brecha de 2/3 contra 1/3.

    Lo que hay que ver es que el azar NO esta en la entrada: la entrada es fija
    y la maquina es la que tira la moneda. La probabilidad se toma sobre las
    tiradas, no sobre las entradas -- que es exactamente lo que distingue BPP
    de "complejidad en promedio".
    """
    ancho, alto = 960, 420
    aria = (
        "Una maquina con una moneda: la misma entrada fija entra muchas veces "
        "y la maquina responde distinto segun las tiradas. Dos barras muestran "
        "que al menos dos tercios de las tiradas dan la respuesta correcta"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Una máquina que tira una moneda", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La entrada es fija. El azar está DENTRO de la máquina, y la "
            "probabilidad se toma sobre sus tiradas.",
            SUAVE, 13.5,
        )
    )

    p.append(caja(50, 130, 150, 90, borde=SUAVE, radio=9))
    p.append(texto(125, 162, "una entrada", SUAVE, 13))
    p.append(texto(125, 190, "x", TEXTO, 22, fuente=MONO))
    p.append(flecha(206, 175, 254, 175, SUAVE, 2, marcador="s"))

    p.append(caja(260, 122, 210, 106, borde=ACENTO, radio=10))
    p.append(texto(365, 152, "M", ACENTO, 22, peso="600"))
    p.append(texto(365, 178, "tiempo polinomial", SUAVE, 12.5))
    for i in range(3):
        p.append(f'<circle cx="{312 + i * 42}" cy="204" r="11" fill="none" '
                 f'stroke="{SERIE[2]}" stroke-width="1.8"/>')
        p.append(texto(312 + i * 42, 209, "?", SERIE[2], 13, peso="600"))
    p.append(texto(365, 246, "sus monedas: r₁ r₂ r₃ …", SERIE[2], 12.5))

    p.append(flecha(476, 175, 524, 175, SUAVE, 2, marcador="s"))

    bx, bw = 540, 360
    p.append(texto(bx + bw / 2, 122, "sobre TODAS las tiradas posibles", SUAVE, 13))
    barras = [
        ("la respuesta correcta", 2 / 3, SERIE[0], "≥ ⅔"),
        ("la respuesta equivocada", 1 / 3, ALARMA, "≤ ⅓"),
    ]
    for i, (etiqueta, frac, color, marca) in enumerate(barras):
        y = 146 + i * 66
        p.append(texto(bx, y - 6, etiqueta, SUAVE, 12.5, anclaje="start"))
        p.append(caja(bx, y, bw, 36, borde=LINEA, radio=7, grosor=1.2))
        p.append(f'<rect x="{bx}" y="{y}" width="{bw * frac:.0f}" height="36" '
                 f'rx="7" fill="{color}" opacity="0.85"/>')
        p.append(texto(bx + bw * frac / 2, y + 24, marca, FONDO, 15, peso="600"))
    p.append(linea(bx + bw * 2 / 3, 138, bx + bw * 2 / 3, 256, TEXTO, 1.6, guiones="5 5"))
    p.append(texto(bx + bw * 2 / 3, 274, "la brecha", TEXTO, 13, peso="600"))

    p.append(
        texto(
            ancho / 2, 328,
            "Esa brecha entre ⅔ y ⅓ es toda la definición de BPP. Y el ⅔ no "
            "tiene nada de especial:",
            TEXTO, 14.5, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 352,
            "cualquier ventaja fija sobre ½ sirve, porque repetir y votar la "
            "amplifica tanto como quieras.",
            SUAVE, 13,
        )
    )
    p.append(
        texto(
            ancho / 2, 386,
            "Si la brecha depende de n y se encoge, deja de servir. Ahí está la "
            "letra B de «bounded».",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def _cadena_mr(n, a):
    """(s, d, cadena) del test de Miller-Rabin para n en base a.

    Se calcula aqui en vez de escribirse a mano: los numeros del diagrama son
    los de verdad, y una errata de transcripcion no puede colarse.
    """
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    cadena = [pow(a, d, n)]
    for _ in range(s):
        cadena.append(cadena[-1] * cadena[-1] % n)
    return s, d, cadena


def cx_miller_rabin():
    """Pagina 7. Las dos cadenas: un primo y un mentiroso de Fermat.

    561 es el ejemplo que hace falta, no uno cualquiera: es un numero de
    Carmichael, asi que ENGANIA al test de Fermat (su cadena termina en 1) y
    aun asi Miller-Rabin lo caza, porque 67 es una raiz cuadrada de 1 que no es
    ni 1 ni -1. Ese contraste es el contenido del diagrama.
    """
    ancho, alto = 980, 470
    aria = (
        "Dos cadenas de cuadrados sucesivos modulo n. Arriba, n igual a 97 que "
        "es primo: la cadena pasa por n menos uno antes de llegar a uno. "
        "Abajo, n igual a 561 que es compuesto: la cadena llega a uno saltando "
        "desde 67, que no es ni 1 ni menos 1, y eso lo delata"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "La cadena de cuadrados, en dos casos", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Escribes n − 1 = 2ˢ·d, calculas a^d y elevas al cuadrado s veces. "
            "Mira cómo llega cada cadena al 1.",
            SUAVE, 13.5,
        )
    )

    def dibujar(y0, n, a, veredicto, color, nota):
        s, d, cadena = _cadena_mr(n, a)
        p.append(texto(60, y0, f"n = {n},  a = {a}", TEXTO, 16, anclaje="start", peso="600"))
        p.append(texto(60, y0 + 20, f"n − 1 = {n - 1} = 2^{s} · {d}", SUAVE, 12.5, anclaje="start"))
        cw, gap = 92, 26
        x0 = 250
        for i, v in enumerate(cadena):
            x = x0 + i * (cw + gap)
            especial = v == n - 1 or (v == 1 and i > 0 and cadena[i - 1] not in (1, n - 1))
            borde = color if especial else LINEA
            p.append(caja(x, y0 - 26, cw, 46, borde=borde, radio=8,
                          grosor=2.4 if especial else 1.4))
            etiqueta = f"{v}" if v != n - 1 else f"{v} = −1"
            p.append(texto(x + cw / 2, y0 + 4, etiqueta, color if especial else TEXTO,
                           15 if v != n - 1 else 13.5, fuente=MONO))
            p.append(texto(x + cw / 2, y0 - 36,
                           f"a^{d}" if i == 0 else ("↑²" if i else ""), SUAVE, 11.5))
            if i < len(cadena) - 1:
                p.append(flecha(x + cw + 3, y0 - 3, x + cw + gap - 3, y0 - 3, SUAVE, 1.8,
                                marcador="s"))
        p.append(texto(60, y0 + 46, veredicto, color, 15, anclaje="start", peso="600"))
        p.append(texto(250, y0 + 46, nota, SUAVE, 12.5, anclaje="start"))

    dibujar(
        170, 97, 2,
        "pasa la prueba",
        SERIE[0],
        "la cadena toca −1 antes del 1: es lo que un primo obliga a hacer",
    )
    p.append(linea(60, 250, 920, 250, LINEA, 1.2, guiones="5 6"))
    dibujar(
        330, 561, 2,
        "COMPUESTO",
        ALARMA,
        "67² ≡ 1 con 67 ≠ ±1: módulo un primo eso es imposible",
    )

    p.append(
        texto(
            ancho / 2, 428,
            "561 = 3·11·17 es un número de Carmichael: engaña al test de Fermat, "
            "porque su cadena SÍ termina en 1.",
            TEXTO, 14, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 450,
            "Mirar la cadena entera, y no solo su final, es todo lo que "
            "Miller-Rabin agrega — y es suficiente.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_error_se_desploma():
    """Pagina 7. Por que 40 rondas bastan: 4^-k contra la intuicion.

    La ultima fila es la que convence, y por eso lleva la comparacion con el
    hardware: a partir de cierto punto el algoritmo aleatorio es mas confiable
    que la computadora que lo corre, y seguir pidiendo certeza deja de tener
    sentido fisico.
    """
    ancho, alto = 940, 400
    aria = (
        "Una tabla de cinco filas: con una ronda el error es de uno en cuatro, "
        "con cinco de uno en mil, con diez de uno en un millon, con veinte de "
        "uno en un billon y con cuarenta de uno en 10 elevado a 24"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Repetir k veces: el error se desploma", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Cada ronda usa una base a nueva e independiente. Basta con que UNA "
            "delate al compuesto.",
            SUAVE, 13.5,
        )
    )

    filas = [
        ("k = 1", "1 en 4", 1.00, SERIE[2], "una de cada cuatro bases falla"),
        ("k = 5", "1 en 1 000", 0.62, SERIE[2], ""),
        ("k = 10", "1 en 1 000 000", 0.42, SERIE[0], ""),
        ("k = 20", "1 en 10¹²", 0.24, SERIE[0], ""),
        ("k = 40", "1 en 10²⁴", 0.08, SERIE[1], "menos que un fallo del procesador"),
    ]
    bx, bw = 250, 340
    for i, (k, error, frac, color, nota) in enumerate(filas):
        y = 108 + i * 50
        p.append(texto(bx - 24, y + 22, k, TEXTO, 15, anclaje="end", peso="600"))
        p.append(caja(bx, y, bw, 32, borde=LINEA, radio=6, grosor=1.2))
        p.append(f'<rect x="{bx}" y="{y}" width="{max(bw * frac, 6):.0f}" height="32" '
                 f'rx="6" fill="{color}" opacity="0.85"/>')
        p.append(texto(bx + bw + 18, y + 21, error, color, 15, anclaje="start", peso="600"))
        if nota:
            p.append(texto(bx + bw + 132, y + 40, nota, SUAVE, 12, anclaje="start"))

    p.append(
        texto(
            ancho / 2, 372,
            "El error es de un solo lado: «compuesto» es certeza; «primo» es "
            "una apuesta que puedes hacer tan segura como quieras.",
            TEXTO, 14, peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 8 · reducciones, duro y completo ----------------------------------


def cx_reduccion():
    """Pagina 8. Una reduccion es un traductor barato, y se lee al reves.

    La flecha de abajo es la mitad del diagrama: A <=p B se USA en la direccion
    contraria a la que se lee. Casi todo el mundo lo aprende invertido la
    primera vez, asi que las dos lecturas van escritas, no insinuadas.
    """
    ancho, alto = 960, 430
    aria = (
        "Una instancia del problema A pasa por un traductor de tiempo "
        "polinomial que la convierte en una instancia del problema B; el "
        "solucionador de B contesta y esa misma respuesta vale para A"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Reducción: A ≤ₚ B", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "«Traduzco cualquier pregunta sobre A en una pregunta sobre B, "
            "barato, y sin cambiar la respuesta.»",
            SUAVE, 13.5,
        )
    )

    cajas = [
        (46, "instancia de A", "«¿hay un ciclo\nhamiltoniano?»", SERIE[1], 190),
        (300, "TRADUCTOR", "tiempo polinomial", ACENTO, 190),
        (554, "instancia de B", "«¿hay un tour\nde costo ≤ k?»", SERIE[2], 190),
        (812, "sí / no", "la MISMA respuesta", SERIE[0], 132),
    ]
    for x, titulo, glosa, color, w in cajas:
        p.append(caja(x, 110, w, 118, borde=color, radio=10))
        p.append(texto(x + w / 2, 142, titulo, color, 15.5, peso="600"))
        for i, l in enumerate(glosa.split("\n")):
            p.append(texto(x + w / 2, 176 + i * 20, l, SUAVE, 12.5))
    for x, largo in ((240, 52), (494, 52), (748, 56)):
        p.append(flecha(x, 169, x + largo, 169, SUAVE, 2, marcador="s"))

    lecturas = [
        ("Se lee así", "«A no es más difícil que B»", SERIE[1]),
        ("Se USA así", "si B es fácil, A también.  Si A es difícil, B también.", ALARMA),
    ]
    for i, (titulo, frase, color) in enumerate(lecturas):
        y = 264 + i * 62
        p.append(caja(80, y, 800, 50, borde=color, radio=9))
        p.append(texto(158, y + 30, titulo, color, 14.5, peso="600"))
        p.append(texto(520, y + 30, frase, TEXTO, 14.5))

    p.append(
        texto(
            ancho / 2, 406,
            "La segunda lectura es la que se usa todo el tiempo, y es la que "
            "todo el mundo invierte la primera vez.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_duro_vs_completo():
    """Pagina 8. Duro y completo son dos cosas, y la diferencia es una sola.

    Las dos definiciones van en una franja propia arriba, separadas del Venn:
    encimadas sobre el ovalo se leian como si NP-duro fuera una region del
    dibujo, que es justo lo contrario de lo que la figura dice.

    El problema de la parada esta puesto a proposito fuera del ovalo: es
    NP-duro y ni siquiera esta en NP, y es el ejemplo que ata esta unidad con
    la anterior.
    """
    ancho, alto = 960, 500
    aria = (
        "Arriba, las dos definiciones enfrentadas. Abajo, un ovalo que "
        "representa NP con P dentro y los NP-completos en su zona mas dificil; "
        "fuera del ovalo, el problema de la parada, que es NP-duro sin estar "
        "en NP"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "NP-duro y NP-completo", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Se diferencian en una sola condición, y no es la que suena más "
            "difícil.",
            SUAVE, 13.5,
        )
    )

    definiciones = [
        (50, "NP-duro", ALARMA, "todo problema de NP se reduce a él",
         "puede estar FUERA de NP"),
        (510, "NP-completo", SERIE[2], "NP-duro   Y   además está en NP",
         "los problemas más difíciles DE NP"),
    ]
    for x0, nombre, color, cond, glosa in definiciones:
        p.append(caja(x0, 92, 400, 96, borde=color, radio=10))
        p.append(texto(x0 + 200, 120, nombre, color, 17, peso="600"))
        p.append(texto(x0 + 200, 146, cond, SUAVE, 13))
        p.append(texto(x0 + 200, 172, glosa, color, 12.5, peso="600"))
    p.append(texto(478, 146, "≠", TEXTO, 22))

    p.append(f'<ellipse cx="400" cy="330" rx="278" ry="118" fill="none" '
             f'stroke="{ACENTO}" stroke-width="2.5"/>')
    p.append(texto(400, 232, "NP", ACENTO, 20, peso="600"))

    p.append(f'<ellipse cx="286" cy="344" rx="122" ry="62" fill="none" '
             f'stroke="{SERIE[0]}" stroke-width="2"/>')
    p.append(texto(286, 326, "P", SERIE[0], 16, peso="600"))
    p.append(texto(286, 350, "Dijkstra", SUAVE, 12))
    p.append(texto(286, 370, "2-SAT", SUAVE, 12))

    p.append(f'<ellipse cx="540" cy="332" rx="106" ry="80" fill="none" '
             f'stroke="{SERIE[2]}" stroke-width="2.5"/>')
    p.append(texto(540, 292, "NP-completos", SERIE[2], 14, peso="600"))
    for i, nombre in enumerate(["SAT · 3-SAT", "hamiltoniano", "TSP (decisión)", "clique"]):
        p.append(texto(540, 316 + i * 20, nombre, SUAVE, 12))

    p.append(caja(716, 396, 224, 76, borde=ALARMA, radio=10, guiones="6 5"))
    p.append(texto(828, 422, "el problema de la parada", ALARMA, 13, peso="600"))
    p.append(texto(828, 442, "NP-duro, y NI SIQUIERA", SUAVE, 12))
    p.append(texto(828, 460, "está en NP: es indecidible", SUAVE, 12))
    p.append(flecha(716, 410, 652, 372, ALARMA, 1.8))

    p.append(
        texto(
            364, 470,
            "Un NP-completo resuelto en tiempo polinomial resolvería TODOS",
            TEXTO, 13.5, peso="600",
        )
    )
    p.append(texto(364, 490, "los de NP. Por eso vale un millón de dólares.", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


def cx_sat_a_3sat():
    """Pagina 8. La reduccion de SAT a 3-SAT, en una clausula concreta.

    Se dibuja con cinco literales porque es el caso mas chico donde hacen falta
    DOS variables nuevas y se ve el encadenamiento; con cuatro literales el
    patron no se distingue de una casualidad.
    """
    ancho, alto = 980, 400
    aria = (
        "Una clausula de cinco literales se parte en tres clausulas de tres "
        "literales, encadenadas por dos variables nuevas y1 e y2 que aparecen "
        "negadas en la siguiente clausula"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "De SAT a 3-SAT, en tiempo polinomial", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Una cláusula larga se parte en cláusulas de tres, encadenadas por "
            "variables nuevas.",
            SUAVE, 13.5,
        )
    )

    p.append(texto(ancho / 2, 122, "una cláusula de 5 literales", SUAVE, 13))
    p.append(caja(280, 136, 420, 48, borde=SERIE[1], radio=9))
    p.append(texto(490, 166, "( x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅ )", SERIE[1], 18, fuente=MONO))

    p.append(flecha(490, 194, 490, 224, ACENTO, 2))
    p.append(texto(516, 214, "se convierte en", ACENTO, 13, anclaje="start", peso="600"))

    trozos = [
        ("( x₁ ∨ x₂ ∨ y₁ )", 60),
        ("( ¬y₁ ∨ x₃ ∨ y₂ )", 360),
        ("( ¬y₂ ∨ x₄ ∨ x₅ )", 660),
    ]
    for etiqueta, x in trozos:
        p.append(caja(x, 240, 262, 48, borde=SERIE[0], radio=9))
        p.append(texto(x + 131, 270, etiqueta, SERIE[0], 17, fuente=MONO))
    for x in (322, 622):
        p.append(texto(x + 20, 270, "∧", TEXTO, 20))

    p.append(texto(191, 312, "y₁", SERIE[2], 14, peso="600"))
    p.append(texto(491, 312, "y₂", SERIE[2], 14, peso="600"))
    p.append(f'<path d="M 240 292 C 260 322, 340 322, 360 292" fill="none" '
             f'stroke="{SERIE[2]}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    p.append(f'<path d="M 540 292 C 560 322, 640 322, 660 292" fill="none" '
             f'stroke="{SERIE[2]}" stroke-width="1.8" stroke-dasharray="5 4"/>')

    p.append(
        texto(
            ancho / 2, 348,
            "Una cláusula de k literales da k−2 cláusulas y k−3 variables "
            "nuevas: crecimiento lineal, no explosión.",
            TEXTO, 14, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 372,
            "Y las nuevas fórmulas son satisfacibles exactamente cuando lo era "
            "la vieja. Por eso 3-SAT es tan difícil como SAT.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_arbol_de_karp():
    """Pagina 8. Como se pobló NP-completo: un solo teorema y luego cadenas.

    El dibujo explica el metodo, no el catalogo: Cook-Levin hizo el trabajo
    duro UNA vez, y desde entonces demostrar que algo es NP-completo es
    encontrar una flecha desde un problema ya marcado.
    """
    ancho, alto = 960, 440
    aria = (
        "Un arbol de reducciones: de SAT sale 3-SAT, y de 3-SAT salen clique, "
        "ciclo hamiltoniano, coloreo y suma de subconjuntos; de clique sale "
        "cubierta de vertices, de hamiltoniano sale TSP y de suma de "
        "subconjuntos sale la mochila"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Cómo se pobló la lista", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "Cook y Levin lo demostraron una vez, desde cero. Todo lo demás son "
            "flechas.",
            SUAVE, 13.5,
        )
    )

    def nodo(x, y, etiqueta, color, w=180, glosa=None):
        p.append(caja(x - w / 2, y - 21, w, 42, borde=color, radio=9))
        p.append(texto(x, y + 5, etiqueta, color, 14.5, peso="600"))
        if glosa:
            p.append(texto(x, y + 34, glosa, SUAVE, 11.5))

    nodo(480, 122, "SAT", ACENTO, 150, "Cook–Levin, 1971: el primero, a mano")
    p.append(flecha(480, 148, 480, 182, ACENTO, 2))
    nodo(480, 206, "3-SAT", ACENTO, 150)

    hijos = [(150, "clique"), (370, "ciclo hamiltoniano"), (590, "coloreo"), (820, "suma de subconjuntos")]
    for x, etiqueta in hijos:
        p.append(f'<path d="M 480 228 C 480 268, {x} 258, {x} 296" fill="none" '
                 f'stroke="{SERIE[2]}" stroke-width="1.8" marker-end="url(#p)"/>')
        nodo(x, 318, etiqueta, SERIE[2], 200)

    nietos = [(150, "cubierta de vértices"), (370, "TSP"), (820, "mochila")]
    for x, etiqueta in nietos:
        p.append(flecha(x, 340, x, 368, SERIE[0], 1.8))
        nodo(x, 392, etiqueta, SERIE[0], 200)

    p.append(
        texto(
            ancho / 2, 428,
            "Demostrar que algo es NP-completo = encontrar UNA flecha desde "
            "algo que ya lo es. Karp encontró 21 en 1972.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


# --- Pagina 9 · el mapa -------------------------------------------------------


def cx_mapa():
    """Pagina 9. La cadena completa, con lo que se sabe y lo que no.

    Cada eslabon lleva marcado si la inclusion podria ser igualdad. Es el unico
    diagrama de la unidad que dibuja ignorancia a proposito: cuatro de las
    cinco contenciones podrian ser igualdades y nadie lo sabe.
    """
    ancho, alto = 980, 450
    aria = (
        "La cadena L contenido en P contenido en NP contenido en PSPACE "
        "contenido en EXP, dibujada como cinco cajas encadenadas. Debajo, lo "
        "que se sabe: que P es estrictamente menor que EXP, y que las demas "
        "contenciones podrian ser igualdades"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Todo lo que sabemos, y todo lo que no", TEXTO, 21, peso="600"))

    clases = [
        ("L", "memoria log n", SERIE[0]),
        ("P", "tiempo polinomial", SERIE[0]),
        ("NP", "verificable rápido", ACENTO),
        ("PSPACE", "memoria polinomial", SERIE[1]),
        ("EXP", "tiempo exponencial", SERIE[2]),
    ]
    cw, gap, x0, y0 = 150, 46, 46, 106
    for i, (nombre, glosa, color) in enumerate(clases):
        x = x0 + i * (cw + gap)
        p.append(caja(x, y0, cw, 84, borde=color, radio=10))
        p.append(texto(x + cw / 2, y0 + 36, nombre, color, 21, peso="600"))
        p.append(texto(x + cw / 2, y0 + 62, glosa, SUAVE, 12))
        if i < len(clases) - 1:
            p.append(texto(x + cw + gap / 2, y0 + 48, "⊆", TEXTO, 22))

    p.append(texto(ancho / 2, 226, "¿Alguna de esas contenciones es estricta?", TEXTO, 15, peso="600"))
    veredictos = [
        ("L ⊊ P", "nadie sabe", SUAVE),
        ("P ⊊ NP", "el problema del millón", ACENTO),
        ("NP ⊊ PSPACE", "nadie sabe", SUAVE),
        ("PSPACE ⊊ EXP", "nadie sabe", SUAVE),
    ]
    for i, (rel, veredicto, color) in enumerate(veredictos):
        x = 76 + i * 218
        p.append(caja(x, 244, 194, 58, borde=color, radio=9,
                      grosor=2.4 if color == ACENTO else 1.4))
        p.append(texto(x + 97, 268, rel, TEXTO, 15, peso="600"))
        p.append(texto(x + 97, 290, veredicto, color, 12.5, peso="600"))

    p.append(caja(200, 326, 580, 66, borde=SERIE[2], radio=10))
    p.append(texto(490, 352, "Lo único separado con certeza:  P ⊊ EXP", SERIE[2], 17, peso="600"))
    p.append(texto(490, 376, "teorema de jerarquía de tiempo — más tiempo compra más problemas",
                   SUAVE, 12.5))

    p.append(
        texto(
            ancho / 2, 424,
            "Sabemos que los dos extremos son distintos. No sabemos dónde, "
            "entre medio, está el corte.",
            TEXTO, 14, peso="600",
        )
    )
    p.append(cierre())
    return "".join(p)


def cx_dos_mundos():
    """Pagina 9. Que cambiaria si P = NP, y por que casi nadie lo cree.

    El panel de la izquierda no es ciencia ficcion inofensiva: si P = NP con
    algoritmos practicos, la criptografia de clave publica deja de existir. Va
    dicho porque es lo que vuelve la pregunta algo mas que una curiosidad.
    """
    ancho, alto = 960, 430
    aria = (
        "Dos columnas: el mundo si P fuera igual a NP, con criptografia rota y "
        "optimizacion resuelta, y el mundo si P es distinto de NP, que es el "
        "que casi todo el mundo cree y en el que ya vivimos"
    )
    p = [marco(ancho, alto, aria)]
    p.append(texto(ancho / 2, 46, "Los dos mundos posibles", TEXTO, 21, peso="600"))
    p.append(
        texto(
            ancho / 2, 70,
            "La respuesta no cambia qué algoritmos tienes hoy. Cambia qué "
            "puedes esperar que exista.",
            SUAVE, 13.5,
        )
    )

    columnas = [
        (40, "Si P = NP", ACENTO, [
            "Buscar cuesta lo mismo que comprobar.",
            "Toda la criptografía de clave pública",
            "se cae: factorizar deja de proteger nada.",
            "Optimización, diseño de fármacos y",
            "demostración automática se vuelven",
            "problemas resueltos.",
            "",
            "Casi nadie cree que sea este mundo.",
        ]),
        (500, "Si P ≠ NP", SERIE[0], [
            "Hay problemas cuya respuesta reconoces",
            "al verla y no puedes encontrar.",
            "La criptografía descansa en algo real.",
            "Y sigue habiendo mucho que hacer:",
            "aproximar, acotar, usar heurísticas,",
            "atacar los casos que sí aparecen.",
            "",
            "Es lo que casi todo el mundo cree,",
            "y nadie ha podido demostrar.",
        ]),
    ]
    for x0, titulo, color, lineas in columnas:
        p.append(caja(x0, 96, 420, 268, borde=color))
        p.append(texto(x0 + 210, 128, titulo, color, 19, peso="600"))
        for i, l in enumerate(lineas):
            if l:
                p.append(texto(x0 + 210, 160 + i * 23, l, SUAVE, 13))

    p.append(
        texto(
            ancho / 2, 396,
            "Y ojo con la trampa: incluso P = NP con un algoritmo de tiempo "
            "n¹⁰⁰ no cambiaría nada en la práctica.",
            TEXTO, 14, peso="600",
        )
    )
    p.append(
        texto(
            ancho / 2, 418,
            "«Polinomial» y «rápido» no son sinónimos. Solo se parecen mucho en "
            "la práctica.",
            SUAVE, 13,
        )
    )
    p.append(cierre())
    return "".join(p)


DIAGRAMAS = {
    "cx-que-es-n": cx_que_es_n,
    "cx-peor-caso": cx_peor_caso,
    "cx-o-grande": cx_o_grande,
    "cx-familia-asintotica": cx_familia_asintotica,
    "cx-escalera": cx_escalera,
    "cx-matrices": cx_matrices,
    "cx-crecimiento": cx_crecimiento,
    "cx-frontera": cx_frontera,
    "cx-dijkstra-vs-tsp": cx_dijkstra_vs_tsp,
    "cx-espacio-se-reusa": cx_espacio_se_reusa,
    "cx-memoria-logaritmica": cx_memoria_logaritmica,
    "cx-no-determinista": cx_no_determinista,
    "cx-verificar-vs-buscar": cx_verificar_vs_buscar,
    "cx-tres-clases": cx_tres_clases,
    "cx-monte-carlo": cx_monte_carlo,
    "cx-miller-rabin": cx_miller_rabin,
    "cx-error-se-desploma": cx_error_se_desploma,
    "cx-reduccion": cx_reduccion,
    "cx-duro-vs-completo": cx_duro_vs_completo,
    "cx-sat-a-3sat": cx_sat_a_3sat,
    "cx-arbol-de-karp": cx_arbol_de_karp,
    "cx-mapa": cx_mapa,
    "cx-dos-mundos": cx_dos_mundos,
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
