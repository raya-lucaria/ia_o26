"""Genera los diagramas SVG de la unidad 10 (aprendizaje profundo).

Mismo patron que gen_complejidad.py: paleta en constantes, una funcion por
diagrama que devuelve una cadena SVG completa, y un catalogo DIAGRAMAS que el
generador y su prueba (test_gen_deep_learning.py) comparten como unica fuente
de "que diagramas existen". De la unidad 9 se toman el tope de 600 px de ancho,
la letra minima de 12 px y los colores de entrenamiento y validacion.

Los ids llevan prefijo "dl-": los ids de objeto numerado de Raya son unicos en
TODO el curso. Ningun numero se escribe a mano: dl-curvas-rmse lee sus curvas y
sus marcas de tools/redes.py (entrenar_ejemplo, cifras).

Jerarquia de color, la misma en las siete figuras:

- capa de entrada / origen j ........ CIAN
- capas ocultas / destino i ......... VERDE
- salida y-gorro .................... AMARILLO
- parametros W, b (y actualizar) .... ROSA
- pase hacia adelante ............... SUAVE, trazo continuo
- perdida y pase hacia atras (delta)  ACENTO (magenta), trazo punteado

El color nunca va solo: cada papel lleva ademas su rotulo, su trazo o su
forma. La notacion es la del plan de la unidad, escrita con sub y
superindices Unicode (en SVG no hay LaTeX); solo el subindice de nabla y de
f_theta, que Unicode no tiene, se baja con un <tspan dy>. Se revisa
renderizando con Chrome: ImageMagick descarta los subindices Unicode.

Uso:  python3 tools/gen_deep_learning.py [id ...]
"""
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/10_deep_learning/_assets"

# ------------------------------------------------------------- paleta ---
# Skin eva-cyberpunk (skins/eva-cyberpunk.yaml). FONDO es
# tokens.color.surface y va horneado en cada SVG (test_9 de test_aceptacion).
FONDO = "#211033"     # tokens.color.surface
TEXTO = "#f7f2ff"     # tokens.color.text
SUAVE = "#c8b9d8"     # tokens.color.muted
LINEA = "#78419e"     # tokens.color.border
ACENTO = "#f04cff"    # tokens.color.accent: perdida y retropropagacion
CIAN = "#55ddff"      # graph.group_3: entrada, origen j
VERDE = "#a8ff5a"     # graph.group_2: ocultas, destino i
AMARILLO = "#ffd166"  # graph.group_4: salida y-gorro
ROSA = "#ff8fab"      # graph.group_6: parametros W, b
# Curvas de dl-curvas-rmse: los colores de los roles «entrenamiento» y
# «validacion» de la unidad 9 (gen_aprendizaje_maquina.ROLES).
ENTRENA = "#64dce3"
VALIDA = "#ffd166"
FUENTE = "system-ui, sans-serif"

ANCHO_MAX = 600       # figuras.md: ninguna figura pasa de 600 px
LETRA_MIN = 12        # letra minima a ese ancho (como la unidad 9)

MARCADORES = {"fw": SUAVE, "bw": ACENTO, "pa": ROSA, "ci": CIAN, "ve": VERDE}


def mezclar(color, fraccion, fondo=FONDO):
    """Color solido equivalente a pintar `color` con opacidad `fraccion`.

    Se hornea aqui en vez de emitir fill-opacity: un sombreado translucido
    tapa lo que hay debajo en renderizadores que ignoran la opacidad (se
    publico asi una vez en complejidad). La prueba prohibe cualquier opacidad.
    """
    def canales(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

    c0, c1 = canales(fondo), canales(color)
    return "#%02x%02x%02x" % tuple(
        round(a + (b - a) * fraccion) for a, b in zip(c0, c1))


ARISTA = mezclar(SUAVE, 0.42)   # flechas de la red que no se destacan
REJILLA = mezclar(SUAVE, 0.22)

# ------------------------------------------------------- primitivas ---


def _n(v):
    """Coordenada redondeada a 0.1, sin ceros de sobra (salida estable)."""
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v)


def marco(ancho, alto, aria, titulo):
    """Raiz <svg> con width/height en px, viewBox, role, aria-label, <title>,
    el fondo del skin y un marcador de flecha por color."""
    marcas = "".join(
        f'<marker id="{k}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" '
        f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        f'fill="{c}"/></marker>'
        for k, c in MARCADORES.items()
    )
    marcas += (
        f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" markerUnits="userSpaceOnUse" '
        f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        f'fill="{ARISTA}"/></marker>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(ancho)}" '
        f'height="{_n(alto)}" viewBox="0 0 {_n(ancho)} {_n(alto)}" role="img" '
        f'aria-label="{escape(aria, {chr(34): "&quot;"})}">'
        f"<title>{escape(titulo)}</title>"
        f'<rect x="0" y="0" width="{_n(ancho)}" height="{_n(alto)}" rx="16" '
        f'fill="{FONDO}"/><defs>{marcas}</defs>'
    )


def cierre():
    return "</svg>"


_TOKEN = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]*\})")


def _trozos(s, tam, base=None):
    """Mini marcado matematico para un renglon:

    *v*    cursiva (escalares y funciones: w, a, z, f, g, l)
    **V**  negrita recta (vectores y matrices: x, a, z, W, b, delta)
    _{..}  subindice bajado con dy, para lo que Unicode no tiene (nabla_W,
           f_theta); adentro vale el mismo marcado.
    Todo lo demas, incluidos los sub/superindices Unicode, va tal cual.
    """
    partes = []
    sube = 0.0   # lo que bajo el ultimo subindice: se devuelve en el trozo siguiente
    for tok in _TOKEN.split(s):
        if not tok:
            continue
        pendiente, sube = sube, 0.0
        dy = f' dy="{_n(pendiente)}"' if pendiente else ""
        if tok.startswith("**"):
            partes.append(f'<tspan font-weight="700"{dy}>{escape(tok[2:-2])}</tspan>')
        elif tok.startswith("*"):
            letra = tok[1:-1]
            # la f cursiva se monta sobre el ⁽ que la sigue: un espacio fino
            if letra.endswith("f"):
                letra += " "
            partes.append(f'<tspan font-style="italic"{dy}>{escape(letra)}</tspan>')
        elif tok.startswith("_{"):
            sub = max(LETRA_MIN, round(tam * 0.8, 1))
            baja = round(tam * 0.3, 1) + pendiente
            dentro = _trozos(tok[2:-1], sub)
            partes.append(
                f'<tspan dy="{_n(baja)}" font-size="{_n(sub)}">{dentro}</tspan>')
            sube = -round(tam * 0.3, 1)
        else:
            partes.append(f"<tspan{dy}>{escape(tok)}</tspan>" if dy else escape(tok))
    return "".join(partes)


def texto(x, y, s, color=TEXTO, tam=14, anclaje="middle", peso="normal",
          rotar=None):
    extra = f' font-weight="{peso}"' if peso != "normal" else ""
    if rotar is not None:
        extra += f' transform="rotate({rotar} {_n(x)} {_n(y)})"'
    return (
        f'<text x="{_n(x)}" y="{_n(y)}" fill="{color}" font-family="{FUENTE}" '
        f'font-size="{_n(tam)}" text-anchor="{anclaje}"{extra}>'
        f"{_trozos(s, tam)}</text>"
    )


def caja(x, y, w, h, relleno="none", borde=LINEA, radio=10, grosor=2,
         guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" '
        f'rx="{_n(radio)}" fill="{relleno}" stroke="{borde}" '
        f'stroke-width="{_n(grosor)}"{trazo}/>'
    )


def circulo(x, y, r, borde, relleno=None, grosor=2.5):
    relleno = relleno or mezclar(borde, 0.14)
    return (
        f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{_n(r)}" fill="{relleno}" '
        f'stroke="{borde}" stroke-width="{_n(grosor)}"/>'
    )


def linea(x1, y1, x2, y2, color=LINEA, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
        f'stroke="{color}" stroke-width="{_n(grosor)}"{trazo}/>'
    )


def flecha(x1, y1, x2, y2, color=SUAVE, marcador="fw", grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (
        f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
        f'stroke="{color}" stroke-width="{_n(grosor)}"{trazo} '
        f'marker-end="url(#{marcador})"/>'
    )


def camino(d, color, marcador=None, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    fin = f' marker-end="url(#{marcador})"' if marcador else ""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" '
        f'stroke-width="{_n(grosor)}" stroke-linecap="round"{trazo}{fin}/>'
    )


def entre_circulos(p, q, r1, r2, holgura=3):
    """Extremos de una flecha de borde a borde de dos circulos."""
    (x1, y1), (x2, y2) = p, q
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (x1 + ux * (r1 + holgura), y1 + uy * (r1 + holgura),
            x2 - ux * (r2 + holgura), y2 - uy * (r2 + holgura))


def borde_caja(cx, cy, w, h, hacia_x, hacia_y, holgura=4):
    """Punto donde la recta del centro (cx, cy) hacia (hacia_x, hacia_y) sale
    de la caja w x h centrada en (cx, cy)."""
    dx, dy = hacia_x - cx, hacia_y - cy
    t = min((w / 2 + holgura) / abs(dx) if dx else math.inf,
            (h / 2 + holgura) / abs(dy) if dy else math.inf)
    return cx + dx * t, cy + dy * t


# ------------------------------------------------ 1 · la red 2-3-2-1 ---

ANCHOS_RED = (2, 3, 2, 1)
COLOR_CAPA = (CIAN, VERDE, VERDE, AMARILLO)
NOMBRE_CAPA = ("entrada", "oculta", "oculta", "salida")
SUP = {0: "⁽⁰⁾", 1: "⁽¹⁾", 2: "⁽²⁾", 3: "⁽³⁾"}
SUB = {1: "₁", 2: "₂", 3: "₃"}


def dl_red_2_3_2_1():
    """Pagina 1. La red del hilo con cada neurona rotulada a_i^(l), las capas
    0..3 con su ancho d_l, todas las flechas de peso, dos pesos de la capa 1
    con su nombre w_ij^(1) y, abajo, el tamano de cada W^(l)."""
    ancho, alto = 600, 440
    aria = (
        "La red 2–3–2–1: capa 0 de entrada con x₁ y x₂ (d₀ = 2), capa 1 oculta "
        "con tres neuronas (d₁ = 3), capa 2 oculta con dos (d₂ = 2) y capa 3 de "
        "salida con una (d₃ = 1), que es ŷ. Cada neurona se llama aᵢ⁽ˡ⁾. Cada "
        "flecha entre capas vecinas es un peso; se rotulan dos de la capa 1: "
        "w₁₁⁽¹⁾ de x₁ a a₁⁽¹⁾ y w₃₂⁽¹⁾ de x₂ a a₃⁽¹⁾. Abajo, los tamaños: W⁽¹⁾ "
        "es 3×2, W⁽²⁾ es 2×3 y W⁽³⁾ es 1×2."
    )
    p = [marco(ancho, alto, aria, "La red 2–3–2–1")]
    xs, cy, sep, r = (100, 240, 380, 506), 222, 92, 26
    pos = [
        [(xs[l], cy + (i - (d - 1) / 2) * sep) for i in range(d)]
        for l, d in enumerate(ANCHOS_RED)
    ]
    destacados = {(0, 0, 0): "*w*₁₁⁽¹⁾", (0, 1, 2): "*w*₃₂⁽¹⁾"}

    # flechas: primero las grises, encima las destacadas
    for l in range(3):
        for j, a in enumerate(pos[l]):
            for i, b in enumerate(pos[l + 1]):
                if (l, j, i) in destacados:
                    continue
                p.append(flecha(*entre_circulos(a, b, r, r, 2), ARISTA, "ar", 1.4))
    for (l, j, i), rotulo in destacados.items():
        a, b = pos[l][j], pos[l + 1][i]
        p.append(flecha(*entre_circulos(a, b, r, r, 2), ROSA, "pa", 3))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        arriba = b[1] < a[1]
        p.append(texto(mx - 8, my + (-16 if arriba else 26), rotulo, ROSA, 15,
                       peso="600"))

    for l, capa in enumerate(pos):
        color = COLOR_CAPA[l]
        p.append(texto(xs[l], 40, f"capa {l}", color, 15, peso="700"))
        p.append(texto(xs[l], 59, NOMBRE_CAPA[l], SUAVE, 13))
        p.append(texto(xs[l], 78, f"*d*{['₀', '₁', '₂', '₃'][l]} = {len(capa)}",
                       TEXTO, 14))
        for i, (x, y) in enumerate(capa):
            p.append(circulo(x, y, r, color))
            p.append(texto(x, y + 5, f"*a*{SUB[i + 1]}{SUP[l]}", TEXTO, 15))
    for i, (x, y) in enumerate(pos[0]):
        p.append(texto(x - r - 8, y + 5, f"**x**{SUB[i + 1]} =", CIAN, 15,
                       anclaje="end"))
    x, y = pos[3][0]
    p.append(texto(x + r + 8, y + 6, "= **ŷ**", AMARILLO, 16, anclaje="start"))

    # tamanos de cada W^(l), entre las capas que conecta
    for l, (fil, col) in enumerate([(3, 2), (2, 3), (1, 2)], start=1):
        x0, x1 = xs[l - 1] + 4, xs[l] - 4
        p.append(linea(x0, 352, x1, 352, ROSA, 1.5))
        p.append(linea(x0, 346, x0, 352, ROSA, 1.5))
        p.append(linea(x1, 346, x1, 352, ROSA, 1.5))
        p.append(texto((x0 + x1) / 2, 374, f"**W**{SUP[l]}: {fil}×{col}", ROSA,
                       14, peso="600"))
    p.append(texto(ancho / 2, 408, "Cada flecha es un peso. Cada neurona de las "
                   "capas 1 a 3 suma además", SUAVE, 13))
    p.append(texto(ancho / 2, 426, "su sesgo *b*ᵢ⁽ˡ⁾ (no dibujado).", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------- 2 · un peso de cerca ---


def dl_peso_wij():
    """Pagina 1. Acercamiento a una sola conexion: de a_j^(l-1) (origen j,
    capa l-1) a z_i^(l) (destino i, capa l) con el peso w_ij^(l), y como se
    leen sus tres indices."""
    ancho, alto = 600, 330
    aria = (
        "Una sola conexión vista de cerca. A la izquierda la neurona de origen "
        "j en la capa l − 1, con su activación aⱼ⁽ˡ⁻¹⁾; a la derecha la neurona "
        "de destino i en la capa l, con su preactivación zᵢ⁽ˡ⁾. La flecha entre "
        "ellas es el peso wᵢⱼ⁽ˡ⁾ y aporta wᵢⱼ⁽ˡ⁾ · aⱼ⁽ˡ⁻¹⁾ a zᵢ⁽ˡ⁾. Abajo: "
        "zᵢ⁽ˡ⁾ = Σⱼ wᵢⱼ⁽ˡ⁾ aⱼ⁽ˡ⁻¹⁾ + bᵢ⁽ˡ⁾, y la lectura de los índices: el "
        "primero, i, es el destino; el segundo, j, el origen; (l) es la capa "
        "a la que llega."
    )
    p = [marco(ancho, alto, aria, "Un peso de cerca")]
    (ox, oy), (dx, dy), r = (112, 130), (488, 130), 40
    p.append(texto(ox, 52, "origen *j*", CIAN, 16, peso="700"))
    p.append(texto(ox, 71, "capa *l* − 1", SUAVE, 13))
    p.append(texto(dx, 52, "destino *i*", VERDE, 16, peso="700"))
    p.append(texto(dx, 71, "capa *l*", SUAVE, 13))
    p.append(circulo(ox, oy, r, CIAN))
    p.append(circulo(dx, dy, r, VERDE))
    p.append(texto(ox, oy + 6, "*a*ⱼ⁽ˡ⁻¹⁾", TEXTO, 17))
    p.append(texto(dx, dy + 6, "*z*ᵢ⁽ˡ⁾", TEXTO, 17))
    p.append(flecha(ox + r + 6, oy, dx - r - 6, dy, ROSA, "pa", 3.5))
    p.append(texto(300, oy - 16, "*w*ᵢⱼ⁽ˡ⁾", ROSA, 24, peso="700"))
    p.append(texto(300, oy + 30, "aporta  *w*ᵢⱼ⁽ˡ⁾ · *a*ⱼ⁽ˡ⁻¹⁾", SUAVE, 14))
    p.append(texto(300, oy + 50, "a la suma del destino", SUAVE, 13))

    p.append(linea(40, 210, 560, 210, REJILLA, 1))
    p.append(texto(300, 240, "*z*ᵢ⁽ˡ⁾ = Σⱼ *w*ᵢⱼ⁽ˡ⁾ *a*ⱼ⁽ˡ⁻¹⁾ + *b*ᵢ⁽ˡ⁾",
                   TEXTO, 17))
    p.append(texto(300, 272, "Cómo leer *w*ᵢⱼ⁽ˡ⁾:", SUAVE, 13))
    p.append(texto(150, 298, "*i* = destino", VERDE, 14, peso="600"))
    p.append(texto(300, 298, "*j* = origen", CIAN, 14, peso="600"))
    p.append(texto(450, 298, "(*l*) = capa a la que llega", ROSA, 14,
                   peso="600"))
    p.append(texto(150, 316, "primer índice", SUAVE, 12))
    p.append(texto(300, 316, "segundo índice", SUAVE, 12))
    p.append(texto(450, 316, "superíndice", SUAVE, 12))
    p.append(cierre())
    return "".join(p)


# --------------------------------------------- 3 · la matriz W^(1) ---


def dl_matriz_w():
    """Pagina 1. W^(1) en forma general, 3 x 2, con filas rotuladas
    «destino i» y columnas «origen j». Se destacan la fila 3 (todo lo que
    llega a a_3^(1)), la columna 2 (todo lo que sale de x_2) y su cruce
    w_32^(1), que es UNA flecha de la red dibujada a la derecha."""
    ancho, alto = 600, 430
    aria = (
        "La matriz W⁽¹⁾ en forma general, de 3 filas por 2 columnas, con "
        "entradas w₁₁⁽¹⁾ a w₃₂⁽¹⁾. Las filas se rotulan destino i = 1, 2, 3 "
        "(las neuronas a₁⁽¹⁾, a₂⁽¹⁾, a₃⁽¹⁾ de la capa 1) y las columnas origen "
        "j = 1, 2 (las entradas x₁ y x₂). Se destaca la fila 3, que son las "
        "flechas que llegan a a₃⁽¹⁾; la columna 2, que son las flechas que "
        "salen de x₂; y su cruce w₃₂⁽¹⁾, que es la flecha de x₂ a a₃⁽¹⁾ en la "
        "red dibujada a la derecha. W⁽¹⁾ está en ℝ³ˣ²: d₁ = 3 filas, d₀ = 2 "
        "columnas."
    )
    p = [marco(ancho, alto, aria, "La matriz W⁽¹⁾")]

    # --- la matriz, forma general ---
    cols, filas = (196, 276), (148, 200, 252)
    cw, ch = 76, 46
    x_izq, x_der = cols[0] - cw / 2 - 6, cols[1] + cw / 2 + 6
    y_arr, y_aba = filas[0] - ch / 2 - 6, filas[2] + ch / 2 + 6
    # bandas: columna 2, fila 3 y su cruce (colores ya mezclados)
    p.append(caja(cols[1] - cw / 2, filas[0] - ch / 2, cw, 3 * ch + 2 * 6,
                  mezclar(CIAN, 0.18), "none", 6, 0))
    p.append(caja(cols[0] - cw / 2, filas[2] - ch / 2, 2 * cw + 4, ch,
                  mezclar(VERDE, 0.2), "none", 6, 0))
    p.append(caja(cols[1] - cw / 2, filas[2] - ch / 2, cw, ch,
                  mezclar(ROSA, 0.26), ROSA, 6, 2))
    # corchetes
    for x, s in ((x_izq, 1), (x_der, -1)):
        p.append(camino(f"M {_n(x + 9 * s)} {_n(y_arr)} H {_n(x)} V {_n(y_aba)} "
                        f"H {_n(x + 9 * s)}", TEXTO, grosor=2))
    for i, y in enumerate(filas, start=1):
        for j, x in enumerate(cols, start=1):
            cruce = (i, j) == (3, 2)
            p.append(texto(x, y + 6, f"*w*{SUB[i]}{SUB[j]}⁽¹⁾",
                           ROSA if cruce else TEXTO, 17,
                           peso="700" if cruce else "normal"))
    # rotulos de columnas (origen j) y de filas (destino i)
    p.append(texto(sum(cols) / 2, 52, "origen *j*", CIAN, 15, peso="700"))
    for j, x in enumerate(cols, start=1):
        p.append(texto(x, 76, f"*j* = {j}", CIAN, 14))
        p.append(texto(x, 96, f"(**x**{SUB[j]})", SUAVE, 13))
    p.append(texto(30, sum(filas) / 3, "destino *i*", VERDE, 15, peso="700",
                   rotar=-90))
    for i, y in enumerate(filas, start=1):
        p.append(texto(118, y - 2, f"*i* = {i}", VERDE, 14, anclaje="end"))
        p.append(texto(118, y + 16, f"(*a*{SUB[i]}⁽¹⁾)", SUAVE, 13,
                       anclaje="end"))

    # --- la red capa 0 -> capa 1 ---
    ent = [(410, 160), (410, 240)]
    ocu = [(540, 120), (540, 200), (540, 280)]
    r = 22
    p.append(texto(475, 52, "capa 0 → capa 1", SUAVE, 13))
    for j, a in enumerate(ent):
        for i, b in enumerate(ocu):
            if (i, j) == (2, 1):
                continue
            if i == 2:
                p.append(flecha(*entre_circulos(a, b, r, r, 2), VERDE, "ve", 2.2,
                                "6 4"))
            elif j == 1:
                p.append(flecha(*entre_circulos(a, b, r, r, 2), CIAN, "ci", 2.2))
            else:
                p.append(flecha(*entre_circulos(a, b, r, r, 2), ARISTA, "ar", 1.4))
    p.append(flecha(*entre_circulos(ent[1], ocu[2], r, r, 2), ROSA, "pa", 3.5))
    p.append(texto(468, 292, "*w*₃₂⁽¹⁾", ROSA, 15, peso="700"))
    for j, (x, y) in enumerate(ent, start=1):
        p.append(circulo(x, y, r, CIAN))
        p.append(texto(x, y + 5, f"**x**{SUB[j]}", TEXTO, 15))
    for i, (x, y) in enumerate(ocu, start=1):
        p.append(circulo(x, y, r, VERDE))
        p.append(texto(x, y + 5, f"*a*{SUB[i]}⁽¹⁾", TEXTO, 13))

    # --- leyenda de lo destacado ---
    y0 = 330
    p.append(caja(cols[0] - cw / 2 - 26, y0 - 10, 18, 14, mezclar(VERDE, 0.2),
                  VERDE, 3, 1.5, "4 3"))
    p.append(texto(cols[0] - cw / 2 - 2, y0 + 2, "fila 3: las flechas que "
                   "llegan a *a*₃⁽¹⁾ (punteadas)", VERDE, 13, anclaje="start"))
    p.append(caja(cols[0] - cw / 2 - 26, y0 + 14, 18, 14, mezclar(CIAN, 0.18),
                  CIAN, 3, 1.5))
    p.append(texto(cols[0] - cw / 2 - 2, y0 + 26, "columna 2: las flechas que "
                   "salen de **x**₂ (continuas)", CIAN, 13, anclaje="start"))
    p.append(caja(cols[0] - cw / 2 - 26, y0 + 38, 18, 14, mezclar(ROSA, 0.26),
                  ROSA, 3, 1.5))
    p.append(texto(cols[0] - cw / 2 - 2, y0 + 50, "su cruce *w*₃₂⁽¹⁾: una sola "
                   "flecha, de **x**₂ a *a*₃⁽¹⁾", ROSA, 13, anclaje="start"))
    p.append(texto(ancho / 2, 412, "**W**⁽¹⁾ ∈ ℝ³ˣ²:  *d*₁ = 3 filas (destinos), "
                   "*d*₀ = 2 columnas (orígenes)", TEXTO, 14))
    p.append(cierre())
    return "".join(p)


# --------------------------------------- 4 y 5 · la cadena de capas ---

# Geometria compartida por dl-composicion y dl-retropropagacion: la misma
# cadena en el mismo lugar, para que la segunda se lea como la primera mas
# la fila de delta.
CADENA = [
    ("act", "**x**", CIAN, "ℝ²"),
    ("f", 1),
    ("act", "**a**⁽¹⁾", VERDE, "ℝ³"),
    ("f", 2),
    ("act", "**a**⁽²⁾", VERDE, "ℝ²"),
    ("f", 3),
    ("act", "**ŷ**", AMARILLO, "ℝ¹"),
    ("perdida",),
]
F_W, F_H, ACT_W, L_W, HUECO = 64, 46, 40, 46, 23
G_NOMBRE = {1: "ReLU", 2: "ReLU", 3: "identidad"}


def _centros_cadena(x0=14):
    """Centro x de cada elemento de CADENA, con un hueco fijo entre ellos."""
    xs, x = [], x0
    for e in CADENA:
        w = {"act": ACT_W, "f": F_W, "perdida": L_W}[e[0]]
        xs.append(x + w / 2)
        x += w + HUECO
    return xs


def _cadena(p, y, con_parametros=True, con_y=True, tenue=False):
    """Dibuja la cadena x -> f1 -> a1 -> f2 -> a2 -> f3 -> y-gorro -> l con su
    fila central en `y`. Devuelve los centros x."""
    xs = _centros_cadena()
    color_fw = ARISTA if tenue else SUAVE
    marca_fw = "ar" if tenue else "fw"
    for k, (e, x) in enumerate(zip(CADENA, xs)):
        if e[0] == "act":
            p.append(texto(x, y + 7, e[1], e[2], 19))
            p.append(texto(x, y + 34, e[3], SUAVE, 13))
        elif e[0] == "f":
            l = e[1]
            p.append(caja(x - F_W / 2, y - F_H / 2, F_W, F_H,
                          mezclar(SUAVE, 0.08), SUAVE, 8, 2))
            p.append(texto(x, y + 7, f"*f*{SUP[l]}", TEXTO, 19))
            if con_parametros:
                p.append(texto(x, y - 66, f"**W**{SUP[l]}, **b**{SUP[l]}", ROSA,
                               14, peso="600"))
                p.append(flecha(x, y - 58, x, y - F_H / 2 - 3, ROSA, "pa", 2))
                p.append(texto(x, y + 40, f"*g*{SUP[l]}: {G_NOMBRE[l]}",
                               SUAVE, 12))
        else:
            p.append(caja(x - L_W / 2, y - F_H / 2, L_W, F_H,
                          mezclar(ACENTO, 0.14), ACENTO, 8, 2.5))
            p.append(texto(x, y + 8, "*ℓ*", TEXTO, 22))
            if con_y:
                p.append(texto(x, y + 70, "**y**", TEXTO, 18))
                p.append(flecha(x, y + 54, x, y + F_H / 2 + 3, SUAVE, "fw", 2))
        if k + 1 < len(CADENA):
            w = {"act": ACT_W, "f": F_W, "perdida": L_W}
            a = x + w[e[0]] / 2 + 2
            b = xs[k + 1] - w[CADENA[k + 1][0]] / 2 - 2
            p.append(flecha(a, y, b, y, color_fw, marca_fw, 2))
    return xs


def dl_composicion():
    """Pagina 2. La red como composicion de capas: x -> f^(1) -> a^(1) ->
    f^(2) -> a^(2) -> f^(3) -> y-gorro -> l, con W^(l), b^(l) entrando a cada
    caja, el espacio de cada vector debajo y la formula de f^(l)."""
    ancho, alto = 600, 300
    aria = (
        "La red como una cadena de funciones: x entra a f⁽¹⁾ y sale a⁽¹⁾; a⁽¹⁾ "
        "entra a f⁽²⁾ y sale a⁽²⁾; a⁽²⁾ entra a f⁽³⁾ y sale ŷ; ŷ y la etiqueta "
        "y entran a la pérdida ℓ. A cada caja f⁽ˡ⁾ le entran sus parámetros "
        "W⁽ˡ⁾ y b⁽ˡ⁾. Debajo de cada vector, su espacio: x en ℝ², a⁽¹⁾ en ℝ³, "
        "a⁽²⁾ en ℝ², ŷ en ℝ¹; g⁽¹⁾ y g⁽²⁾ son ReLU y g⁽³⁾ la identidad. Abajo: "
        "ŷ = f⁽³⁾(f⁽²⁾(f⁽¹⁾(x))) = f_θ(x), con f⁽ˡ⁾(u) = g⁽ˡ⁾(W⁽ˡ⁾u + b⁽ˡ⁾)."
    )
    p = [marco(ancho, alto, aria, "La red como composición")]
    _cadena(p, 112)
    p.append(linea(30, 218, 570, 218, REJILLA, 1))
    p.append(texto(ancho / 2, 250, "**ŷ** = *f*⁽³⁾(*f*⁽²⁾(*f*⁽¹⁾(**x**))) = "
                   "*f*_{*θ*}(**x**)", TEXTO, 17))
    p.append(texto(ancho / 2, 280, "cada capa:  *f*⁽ˡ⁾(**u**) = "
                   "*g*⁽ˡ⁾(**W**⁽ˡ⁾**u** + **b**⁽ˡ⁾)", SUAVE, 15))
    p.append(cierre())
    return "".join(p)


def dl_retropropagacion():
    """Pagina 4. La misma cadena (tenue, sin parametros) con la fila de delta
    debajo: de l nace delta^(3) = 2(y-gorro - y) (.) g^(3)'; cada flecha
    delta^(l+1) -> delta^(l) multiplica por W^(l+1)T y luego (.) g^(l)'; de
    cada delta^(l) salen los gradientes de W^(l) y b^(l)."""
    ancho, alto = 600, 366
    aria = (
        "La misma cadena de capas, arriba y en tenue, recorrida hacia "
        "adelante. Debajo, en magenta y punteado, el pase hacia atrás: de la "
        "pérdida ℓ nace δ⁽³⁾ = 2(ŷ − y) ⊙ g⁽³⁾′; de δ⁽³⁾ se pasa a δ⁽²⁾ "
        "con W⁽³⁾ᵀδ⁽³⁾ y luego ⊙ g⁽²⁾′; de δ⁽²⁾ a δ⁽¹⁾ con W⁽²⁾ᵀδ⁽²⁾ y "
        "luego ⊙ g⁽¹⁾′. Cada δ⁽ˡ⁾ queda bajo su capa f⁽ˡ⁾ y da los "
        "gradientes de sus parámetros: ∇ de W⁽ˡ⁾ es δ⁽ˡ⁾ a⁽ˡ⁻¹⁾ᵀ y ∇ de b⁽ˡ⁾ "
        "es δ⁽ˡ⁾."
    )
    p = [marco(ancho, alto, aria, "Retropropagación")]
    y_fw, y_bw = 70, 190
    p.append(texto(14, 30, "adelante", SUAVE, 13, anclaje="start", peso="600"))
    xs = _cadena(p, y_fw, con_parametros=False, con_y=False, tenue=True)
    xf = {l: xs[2 * l - 1] for l in (1, 2, 3)}
    xl = xs[-1]
    p.append(texto(14, y_bw - 44, "atrás", ACENTO, 13, anclaje="start",
                   peso="600"))

    dw, dh = 52, 40
    for l in (1, 2, 3):
        x = xf[l]
        p.append(linea(x, y_fw + F_H / 2 + 4, x, y_bw - dh / 2 - 4, REJILLA, 1,
                       "2 4"))
        p.append(caja(x - dw / 2, y_bw - dh / 2, dw, dh, mezclar(ACENTO, 0.14),
                      ACENTO, 8, 2.5, "6 3"))
        p.append(texto(x, y_bw + 7, f"**δ**{SUP[l]}", TEXTO, 19))
    # de l a delta^(3)
    x3 = xf[3]
    d = (f"M {_n(xl)} {_n(y_fw + F_H / 2 + 4)} V {_n(y_bw - 14)} "
         f"Q {_n(xl)} {_n(y_bw)} {_n(xl - 14)} {_n(y_bw)} "
         f"H {_n(x3 + dw / 2 + 4)}")
    p.append(camino(d, ACENTO, "bw", 2.5, "7 4"))
    p.append(texto(xl - 10, y_bw - 34, "2(**ŷ** − **y**)", ACENTO, 14,
                   anclaje="end"))
    p.append(texto(xl - 10, y_bw - 14, "⊙ *g*⁽³⁾′", ACENTO, 14, anclaje="end"))
    # delta^(l+1) -> delta^(l)
    for l in (2, 1):
        a, b = xf[l + 1] - dw / 2 - 4, xf[l] + dw / 2 + 4
        p.append(camino(f"M {_n(a)} {_n(y_bw)} H {_n(b)}", ACENTO, "bw", 2.5,
                        "7 4"))
        m = (a + b) / 2
        p.append(texto(m, y_bw - 11, f"**W**{SUP[l + 1]}ᵀ**δ**{SUP[l + 1]}",
                       ACENTO, 14))
        p.append(texto(m, y_bw + 25, f"⊙ *g*{SUP[l]}′", ACENTO, 14))
    # gradientes de cada capa
    for l in (1, 2, 3):
        x = xf[l]
        p.append(flecha(x, y_bw + dh / 2 + 3, x, y_bw + 48, ROSA, "pa", 2))
        ant = "**x**" if l == 1 else f"**a**{SUP[l - 1]}"
        p.append(texto(x, y_bw + 70, f"∇_{{**W**{SUP[l]}}}*ℓ* = "
                       f"**δ**{SUP[l]}{ant}ᵀ", ROSA, 13))
        p.append(texto(x, y_bw + 94, f"∇_{{**b**{SUP[l]}}}*ℓ* = **δ**{SUP[l]}",
                       ROSA, 13))
    # leyenda
    y = 320
    p.append(linea(70, y, 110, y, SUAVE, 2))
    p.append(texto(118, y + 5, "adelante: activaciones **a**⁽ˡ⁾", SUAVE, 13,
                   anclaje="start"))
    p.append(linea(330, y, 370, y, ACENTO, 2.5, "7 4"))
    p.append(texto(378, y + 5, "atrás: errores **δ**⁽ˡ⁾", ACENTO, 13,
                   anclaje="start"))
    p.append(texto(ancho / 2, 348, "**δ**⁽ˡ⁾ = ∇_{**z**⁽ˡ⁾}*ℓ*, de una observación",
                   SUAVE, 13))
    p.append(cierre())
    return "".join(p)


# ------------------------------------------------ 6 · el ciclo ---

PASOS_CICLO = [
    ("1 · Adelante", "**z**⁽ˡ⁾, **a**⁽ˡ⁾ para *l* = 1…*L*; **ŷ**ₖ", SUAVE, None),
    ("2 · Pérdida", "*L*_{ℬ} + *μ*Ω(*θ*)", ACENTO, None),
    ("3 · Atrás", "**δ**⁽ᴸ⁾, …, **δ**⁽¹⁾", ACENTO, "6 3"),
    ("4 · Gradientes", "**δ**⁽ˡ⁾**a**⁽ˡ⁻¹⁾ᵀ en ℬ + 2*μ***W**⁽ˡ⁾", ACENTO, "6 3"),
    ("5 · Actualizar", "*θ* ← *θ* − *η* ∇_{*θ*}ℒ(*θ*, *μ*)", ROSA, None),
]


def dl_ciclo():
    """Pagina 5. El entrenamiento como un ciclo de cinco pasos, los de la
    lista de la pagina: adelante, perdida, atras, gradientes, actualizar.
    Tomar un lote no es un paso numerado: va al centro, como la entrada del
    ciclo, y la flecha de regreso dice «siguiente lote»."""
    ancho, alto = 600, 400
    aria = (
        "El ciclo de entrenamiento en cinco pasos, en círculo: 1, pase hacia "
        "adelante, z⁽ˡ⁾ y a⁽ˡ⁾ para cada capa hasta ŷ; 2, la pérdida "
        "promediada en el lote, L_ℬ, más μΩ(θ); 3, pase hacia atrás, de δ⁽ᴸ⁾ "
        "a δ⁽¹⁾; 4, los gradientes, δ⁽ˡ⁾ a⁽ˡ⁻¹⁾ᵀ promediado en el lote, más "
        "2μW⁽ˡ⁾; 5, actualizar θ ← θ − η ∇ℒ(θ, μ). Luego, de nuevo con el "
        "siguiente lote. Al centro, la entrada del ciclo: tomar un lote ℬ de "
        "|ℬ| pares (xₖ, yₖ). Debajo: θ son todos los W⁽ˡ⁾ y b⁽ˡ⁾; "
        "una vuelta es un paso de descenso y pasar por todos los lotes es "
        "una época."
    )
    p = [marco(ancho, alto, aria, "El ciclo de entrenamiento")]
    cx = 300
    bw, bh = 190, 62
    # un pentagono achatado: los dos de abajo separados para que la flecha
    # 3 -> 4 (atras -> gradientes) se vea entera
    centros = [(300, 70), (490, 190), (430, 340), (170, 340), (110, 190)]
    # flechas del ciclo, de borde a borde, curvadas hacia afuera
    for k in range(5):
        (x1, y1), (x2, y2) = centros[k], centros[(k + 1) % 5]
        a = borde_caja(x1, y1, bw, bh, x2, y2, 5)
        b = borde_caja(x2, y2, bw, bh, x1, y1, 7)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = mx - 300, my - 214   # hacia afuera del pentagono
        nn = math.hypot(nx, ny)
        largo = math.hypot(b[0] - a[0], b[1] - a[1])
        qx, qy = mx + nx / nn * largo * 0.18, my + ny / nn * largo * 0.18
        color, marca, guion = SUAVE, "fw", None
        if k in (1, 2):   # perdida -> atras -> gradientes: el pase hacia atras
            color, marca, guion = ACENTO, "bw", "7 4"
        p.append(camino(f"M {_n(a[0])} {_n(a[1])} Q {_n(qx)} {_n(qy)} "
                        f"{_n(b[0])} {_n(b[1])}", color, marca, 2.5, guion))
        if k == 4:
            p.append(texto(qx - 10, qy - 4, "siguiente lote", ROSA, 13,
                           anclaje="end", peso="600"))
    for (x, y), (titulo, formula, color, guion) in zip(centros, PASOS_CICLO):
        p.append(caja(x - bw / 2, y - bh / 2, bw, bh, mezclar(color, 0.12),
                      color, 10, 2.5, guion))
        p.append(texto(x, y - 6, titulo, color, 15, peso="700"))
        p.append(texto(x, y + 17, formula, TEXTO, 13))
    # al centro, la entrada del ciclo: tomar un lote, que alimenta el paso 1
    lw, lh, ly = 170, 54, 160
    p.append(caja(cx - lw / 2, ly - lh / 2, lw, lh, mezclar(CIAN, 0.12), CIAN,
                  10, 2.5))
    p.append(texto(cx, ly - 5, "Tomar un lote ℬ", CIAN, 14, peso="700"))
    p.append(texto(cx, ly + 15, "|ℬ| pares (**x**ₖ, **y**ₖ)", TEXTO,
                   13))
    p.append(flecha(cx, ly - lh / 2 - 3, cx, 70 + bh / 2 + 6, CIAN, "ci", 2.5))
    p.append(texto(cx, 222, "*θ* = todos los **W**⁽ˡ⁾ y **b**⁽ˡ⁾", TEXTO,
                   14, peso="600"))
    p.append(texto(cx, 246, "una vuelta = un paso de descenso", SUAVE, 13))
    p.append(texto(cx, 266, "todos los lotes = una época", SUAVE, 13))
    p.append(cierre())
    return "".join(p)


# ------------------------------------------- 7 · curvas de RMSE ---

# Geometria publica: la prueba la usa para invertir las coordenadas de cada
# curva y compararlas con redes.entrenar_ejemplo().
CURVAS = {
    "ancho": 600, "alto": 580,
    "x0": 64, "x1": 582,                 # eje de epocas
    "y_min": 0.10, "y_max": 0.60,        # escala del RMSE
    "paneles": {"sin-mu": (90, 266), "con-mu": (330, 506)},   # (arriba, abajo)
}
# Ventana de epocas donde va el rotulo de cada curva (dentro del panel, sobre
# la validacion y bajo el entrenamiento: su altura se calcula con los datos
# para que nunca pise una curva).
VENTANA_ROTULOS = (1000, 1400)


def _redes():
    import redes  # numpy; solo lo necesita esta figura
    return redes


def escala_x(epoca, epocas):
    return CURVAS["x0"] + (CURVAS["x1"] - CURVAS["x0"]) * epoca / epocas


def escala_y(v, panel):
    arriba, abajo = CURVAS["paneles"][panel]
    f = (v - CURVAS["y_min"]) / (CURVAS["y_max"] - CURVAS["y_min"])
    return abajo - (abajo - arriba) * f


def epocas_dibujadas(epocas):
    """Epocas que entran a cada curva: todas desde la 1. La 0 (la red sin
    entrenar) queda fuera de escala y su valor se dice en el pie."""
    return list(range(1, epocas + 1))


def dl_curvas_rmse():
    """Pagina 5. RMSE de entrenamiento y de validacion contra epoca, sin mu
    (arriba) y con mu (abajo), de redes.entrenar_ejemplo; un punto es el RMSE
    sobre todo el conjunto al final de una epoca, sin suavizar. El minimo de
    validacion va marcado: sin mu la validacion baja y luego sube mientras el
    entrenamiento sigue bajando; con mu se queda cerca de su minimo."""
    redes = _redes()
    c = redes.cifras()
    epocas = redes.EPOCAS
    mu = redes.MU_ENTRENAMIENTO
    historias = {"sin-mu": redes.entrenar_ejemplo(0.0),
                 "con-mu": redes.entrenar_ejemplo(mu)}
    sufijo = {"sin-mu": "sin_mu", "con-mu": "con_mu"}
    ancho, alto = CURVAS["ancho"], CURVAS["alto"]
    x0, x1 = CURVAS["x0"], CURVAS["x1"]

    def f3(v):
        return f"{v:.3f}"

    aria = (
        f"Dos gráficas de RMSE contra época, de 0 a {epocas} épocas, con la "
        f"misma red y los mismos datos; cada punto es el RMSE al final de una "
        f"época. Arriba, sin μ: el RMSE de entrenamiento baja hasta "
        f"{f3(c['rmse_entrenamiento_final_sin_mu'])}, y el de validación baja "
        f"hasta su mínimo, {f3(c['rmse_validacion_min_sin_mu'])} en la época "
        f"{c['epoca_validacion_min_sin_mu']}, y luego sube hasta "
        f"{f3(c['rmse_validacion_final_sin_mu'])}. Abajo, con μ = {mu}: el de "
        f"entrenamiento termina en {f3(c['rmse_entrenamiento_final_con_mu'])} y "
        f"el de validación llega a {f3(c['rmse_validacion_min_con_mu'])} en la "
        f"época {c['epoca_validacion_min_con_mu']} y termina en "
        f"{f3(c['rmse_validacion_final_con_mu'])}, casi sin subir."
    )
    p = [marco(ancho, alto, aria, "Curvas de RMSE, sin μ y con μ")]

    # leyenda
    y = 30
    p.append(linea(64, y, 100, y, ENTRENA, 3))
    p.append(texto(106, y + 5, "entrenamiento", ENTRENA, 13, anclaje="start"))
    p.append(linea(222, y, 258, y, VALIDA, 3))
    p.append(texto(264, y + 5, "validación", VALIDA, 13, anclaje="start"))
    p.append(f'<circle cx="399" cy="{y}" r="5.5" fill="{ACENTO}" '
             f'stroke="{TEXTO}" stroke-width="1.5"/>')
    p.append(texto(412, y + 5, "mínimo de validación", ACENTO, 13,
                   anclaje="start"))
    for arriba, abajo in CURVAS["paneles"].values():
        p.append(texto(20, (arriba + abajo) / 2, "RMSE", SUAVE, 13, rotar=-90))

    titulos = {"sin-mu": "sin *μ*  (*μ* = 0)", "con-mu": f"con *μ* = {mu}"}
    ks = epocas_dibujadas(epocas)
    for panel, (arriba, abajo) in CURVAS["paneles"].items():
        h = historias[panel]
        s = sufijo[panel]
        ent, val = h["rmse_entrenamiento"], h["rmse_validacion"]
        # rejilla y ejes
        for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
            yy = escala_y(v, panel)
            if v > CURVAS["y_min"]:
                p.append(linea(x0, yy, x1, yy, REJILLA, 1))
            p.append(texto(x0 - 8, yy + 4, f"{v:.1f}", SUAVE, 12, anclaje="end"))
        for e in range(0, epocas + 1, 250):
            xx = escala_x(e, epocas)
            p.append(linea(xx, abajo, xx, abajo + 5, SUAVE, 1.5))
            p.append(texto(xx, abajo + 19, str(e), SUAVE, 12))
        p.append(linea(x0, abajo, x1, abajo, SUAVE, 1.5))
        p.append(linea(x0, arriba - 4, x0, abajo, SUAVE, 1.5))
        # titulo del panel y valores finales en el mismo renglon
        p.append(texto(x0, arriba - 14, titulos[panel], TEXTO, 15,
                       anclaje="start", peso="700"))
        p.append(
            f'<text x="{x1}" y="{arriba - 14}" font-family="{FUENTE}" '
            f'font-size="13" text-anchor="end" fill="{SUAVE}">al final: '
            f'<tspan fill="{ENTRENA}" font-weight="700">{f3(ent[-1])}</tspan>'
            f' y <tspan fill="{VALIDA}" font-weight="700">{f3(val[-1])}</tspan>'
            f"</text>"
        )
        # curvas, cada epoca un punto, sin suavizar
        for clave, color, grosor in (("rmse_entrenamiento", ENTRENA, 1.5),
                                     ("rmse_validacion", VALIDA, 1.5)):
            pts = " ".join(
                ("M" if n == 0 else "L")
                + f" {_n(escala_x(k, epocas))} {_n(escala_y(h[clave][k], panel))}"
                for n, k in enumerate(ks)
            )
            p.append(f'<path id="dl-curva-{panel}-{clave.split("_")[1]}" '
                     f'd="{pts}" fill="none" stroke="{color}" '
                     f'stroke-width="{grosor}" stroke-linejoin="round"/>')
        # rotulos directos: sobre la validacion, bajo el entrenamiento
        a, b = VENTANA_ROTULOS
        xr = escala_x((a + b) / 2, epocas)
        p.append(texto(xr, escala_y(max(val[a:b + 1]), panel) - 8, "validación",
                       VALIDA, 13, peso="600"))
        p.append(texto(xr, escala_y(min(ent[a:b + 1]), panel) + 18,
                       "entrenamiento", ENTRENA, 13, peso="600"))
        # minimo de validacion: triangulo en el punto, linea al eje y rotulo
        # por encima de todo lo que la validacion hace alrededor
        k_min = c[f"epoca_validacion_min_{s}"]
        v_min = c[f"rmse_validacion_min_{s}"]
        mx, my = escala_x(k_min, epocas), escala_y(val[k_min], panel)
        p.append(linea(mx, my + 6, mx, abajo, ACENTO, 1.5, "2 3"))
        techo = escala_y(max(val[max(1, k_min - 120):k_min + 121]), panel)
        ty = techo - 30
        p.append(linea(mx, ty + 6, mx, my - 6, ACENTO, 1.5, "2 3"))
        p.append(f'<circle id="dl-minimo-{panel}" cx="{_n(mx)}" cy="{_n(my)}" '
                 f'r="5.5" fill="{ACENTO}" stroke="{TEXTO}" stroke-width="1.5" '
                 f'data-epoca="{k_min}"/>')
        p.append(texto(mx, ty - 14, f"mínimo {f3(v_min)}", ACENTO, 13,
                       peso="700"))
        p.append(texto(mx, ty + 2, f"en la época {k_min}", ACENTO, 13))
    p.append(texto((x0 + x1) / 2, 546, "época", SUAVE, 13))
    sin = historias["sin-mu"]
    p.append(texto(ancho / 2, alto - 10,
                   f"Época 0, sin entrenar: {f3(sin['rmse_entrenamiento'][0])} "
                   f"y {f3(sin['rmse_validacion'][0])}, fuera de escala.",
                   SUAVE, 12))
    p.append(cierre())
    return "".join(p)


DIAGRAMAS = {
    "dl-red-2-3-2-1": dl_red_2_3_2_1,
    "dl-peso-wij": dl_peso_wij,
    "dl-matriz-w": dl_matriz_w,
    "dl-composicion": dl_composicion,
    "dl-retropropagacion": dl_retropropagacion,
    "dl-ciclo": dl_ciclo,
    "dl-curvas-rmse": dl_curvas_rmse,
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
