"""Genera los diagramas SVG de la unidad de juegos (unidad 7).

Mismo patron que gen_optimizacion.py: una funcion por diagrama que devuelve
una cadena SVG completa, y un catalogo DIAGRAMAS que el generador y su prueba
comparten. Las primitivas de dibujo (marco, texto, caja, flecha...) se
importan de gen_optimizacion para que las dos unidades compartan paleta y
convenciones.

Ningun tablero se dibuja a mano: cada nodo se calcula con tools/juegos.py a
partir de las jugadas, asi que un cambio en las reglas cambia el dibujo.

Los ids llevan prefijo "jue-": los ids de objeto numerado son unicos en todo
el curso.
"""
import math
import sys
from fractions import Fraction as F
from xml.sax.saxutils import escape

import juegos as j
from gen_optimizacion import (ACENTO, FONDO, FUENTE, LINEA, SERIE, SUAVE,
                              TEXTO, _rombo, caja, cierre, flecha, linea,
                              marco, mezclar, punto, texto)
from unidades import ASSETS_JUEGOS

ASSETS = ASSETS_JUEGOS

# Colores de las dos clases de nodo y de los finales.
COLOR_MAX = SERIE[1]
COLOR_MIN = SERIE[2]
COLOR_FINAL = SERIE[0]

# El subgrafo de la unidad: tras a1-a2 y b3-b2, mueven Blancas.
CAMINO_N1 = ["a1-a2", "b3-b2"]


# ---------------------------------------------------------------- calculo ---

def jugar(tablero, turno, nombres):
    """Aplica una lista de jugadas por nombre y devuelve (tablero, turno)."""
    for nombre in nombres:
        opciones = {j.nombre_jugada(tablero, m): m for m in j.jugadas(tablero, turno)}
        tablero = j.mover(tablero, opciones[nombre])
        turno = j.otro(turno)
    return tablero, turno


def hijos(tablero, turno):
    """[(nombre de jugada, tablero, turno)] en el orden fijo de la unidad."""
    return [(j.nombre_jugada(tablero, m), j.mover(tablero, m), j.otro(turno))
            for m in j.jugadas(tablero, turno)]


def subgrafo_n1():
    """Nodos n1..n13 en preorden: dict n -> (tablero, turno, padre, jugada)."""
    raiz = jugar(j.inicio(), "B", CAMINO_N1)
    nodos = {}

    def visitar(tablero, turno, padre, jugada):
        n = len(nodos) + 1
        nodos[n] = (tablero, turno, padre, jugada)
        if j.ganador(tablero, turno):
            return
        for nombre, t2, p2 in hijos(tablero, turno):
            visitar(t2, p2, n, nombre)
    visitar(*raiz, None, None)
    return nodos


def motivo_final(tablero, turno):
    if "B" in tablero[6:9] or "N" in tablero[0:3]:
        return "llegó"
    if "B" not in tablero or "N" not in tablero:
        return "capturó todo"
    return "sin jugada"


# ---------------------------------------------------------------- dibujo ---
#
# Todas las figuras miden ANCHO px o menos. A 1280 px de pantalla la columna
# util de una figura mide ~614 px, y por debajo de ~1470 px el sitio no
# encoge los SVG (para no bajar de letra legible): lo que pase de ~614 se
# corta por la derecha. A 700 y a 640 se cortaban. Lo que no cabe a lo ancho
# crece hacia abajo.
#
# En un telefono de 390 px la figura se ve desde la izquierda, con
# desplazamiento lateral: por eso el titulo y las notas van alineados a la
# izquierda, en X_PIE, y en renglones que caben en los primeros ~340 px.

ANCHO = 600
X_PIE = 20          # margen izquierdo del titulo, del pie y de la leyenda
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


def encabezado(out, renglones, y=34):
    """Titulo a la izquierda: el primer renglon a 20, los demas a 17.
    Devuelve la base del ultimo renglon."""
    if isinstance(renglones, str):
        renglones = [renglones]
    for k, r in enumerate(renglones):
        out.append(texto(X_PIE, y, r, tam=20 if k == 0 else 17, peso="700", anclaje="start"))
        if k < len(renglones) - 1:
            y += 25
    return y


def lado_de(tablero):
    """3 para hexapawn, 4 para el tablero de 4x4 de la clase 3."""
    return int(round(len(tablero) ** 0.5))


def tablero_svg(cx, cy, tablero, celda=24):
    """Tablero de n x n con la ultima fila arriba. B y N se escriben, no solo
    se colorean: el color nunca es la unica senal."""
    n = lado_de(tablero)
    lado = n * celda
    x0, y0 = cx - lado / 2, cy - lado / 2
    s = [caja(x0, y0, lado, lado, relleno=mezclar(LINEA, 0.35), borde=SUAVE,
              radio=3, grosor=1)]
    for k in range(1, n):
        s.append(linea(x0 + k * celda, y0, x0 + k * celda, y0 + lado, color=SUAVE, grosor=1))
        s.append(linea(x0, y0 + k * celda, x0 + lado, y0 + k * celda, color=SUAVE, grosor=1))
    radio, letra = celda * 0.42, celda * 0.6
    for i, pieza in enumerate(tablero):
        if pieza == ".":
            continue
        fila, col = divmod(i, n)
        px = x0 + col * celda + celda / 2
        py = y0 + (n - 1 - fila) * celda + celda / 2
        if pieza == "B":
            s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{radio:.1f}" fill="{TEXTO}"/>')
            s.append(texto(round(px, 1), round(py + letra * 0.36, 1), "B", color=FONDO,
                           tam=round(letra, 1), peso="700"))
        else:
            s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{radio:.1f}" fill="{FONDO}" '
                     f'stroke="{TEXTO}" stroke-width="2"/>')
            s.append(texto(round(px, 1), round(py + letra * 0.36, 1), "N", color=TEXTO,
                           tam=round(letra, 1), peso="700"))
    return "".join(s)


def tipo_de_nodo(tablero, turno):
    """(color, renglon 1, renglon 2) segun el nodo sea final, de MAX o de MIN."""
    g = j.ganador(tablero, turno, lado_de(tablero))
    if g:
        quien = "Blancas" if g == "B" else "Negras"
        return COLOR_FINAL, f"Fin: gana {quien}", f"U = {'+1' if g == 'B' else '−1'}"
    if turno == "B":
        return COLOR_MAX, "Mueve Blancas", "MAX"
    return COLOR_MIN, "Mueve Negras", "MIN"


def nodo_svg(cx, cy, tablero, turno, arriba, nuevo=False, expandido=True,
             w=150, h=160, celda=24, renglones=None, color=None, orden=None, radio=10,
             escala=None):
    """Un nodo: rotulo arriba, tablero al centro y su tipo en dos renglones.

    Borde doble: final. Borde punteado: existe pero aun no se expande.
    Borde grueso de acento: lo nuevo de este paso. `renglones` reemplaza los
    dos renglones de abajo (para escribir su valor), `color` el color de su
    tipo (para el nodo de azar) y `orden` dibuja en la esquina el numero de
    visita de un recorrido. `escala` fija el tamano de la letra en vez de
    deducirlo del ancho (las figuras de alfa-beta por partes lo suben para
    que se lean en un telefono). La letra nunca baja de 12: los nodos chicos
    usan ESCALA_MIN."""
    color_tipo, r1, r2 = tipo_de_nodo(tablero, turno)
    color = color or color_tipo
    if renglones:
        r1, r2 = renglones
    final = bool(j.ganador(tablero, turno, lado_de(tablero)))
    x, y = cx - w / 2, cy - h / 2
    s = []
    if final:
        s.append(caja(x - 5, y - 5, w + 10, h + 10, borde=color, grosor=2))
    s.append(caja(x, y, w, h, relleno=mezclar(color, 0.16 if nuevo else 0.07),
                  borde=ACENTO if nuevo else color, grosor=3.5 if nuevo else 2,
                  guiones=None if (expandido or final) else "8 5", radio=radio))
    f = escala or min(1.5, max(ESCALA_MIN, w / 150))  # la letra crece con el nodo
    s.append(texto(cx, y + 22 * f, arriba, tam=round(16 * f, 1), peso="700"))
    lado = lado_de(tablero) * celda
    s.append(tablero_svg(cx, y + 32 * f + lado / 2, tablero, celda))
    s.append(texto(cx, y + h - 27 * f, r1, tam=round(13 * f, 1), color=color, peso="700"))
    s.append(texto(cx, y + h - 10 * f, r2, tam=round(13 * f, 1), color=color, peso="700"))
    if orden is not None:
        s.append(f'<circle cx="{x + 4:.1f}" cy="{y + 4:.1f}" r="15" fill="{ACENTO}"/>')
        s.append(texto(round(x + 4, 1), round(y + 9.5, 1), f"{orden}º", tam=13,
                       color=FONDO, peso="700"))
    return "".join(s)


# 13 x 0.93 = 12.1: el renglon mas chico de un nodo no baja de 12 px.
ESCALA_MIN = 0.93


def arista_svg(x1, y1, x2, y2, rotulo, nueva=False, h=160, tenue=False, t=0.5, tam=15):
    """Flecha del borde inferior del padre al superior del hijo, con el
    nombre de la jugada sobre la flecha, a la fraccion t de su largo.
    `tenue`: la jugada se conoce, pero su estado nunca se genera."""
    color = ACENTO if nueva else (LINEA if tenue else SUAVE)
    ya, yb = y1 + h / 2, y2 - h / 2 - 8
    if tenue:
        s = [linea(x1, ya, x2, yb, color=color, grosor=2, guiones="6 5")]
    else:
        s = [flecha(x1, ya, x2, yb, color=color, grosor=3 if nueva else 2,
                    marcador="p" if nueva else "s")]
    mx, my = x1 + (x2 - x1) * t, ya + (yb - ya) * t
    ancho = round(0.62 * tam * len(rotulo) + 14)
    s.append(caja(round(mx - ancho / 2, 1), round(my - 13, 1), ancho, 25, relleno=FONDO,
                  borde=color, radio=7, grosor=1.5))
    s.append(texto(round(mx, 1), round(my + 5, 1), rotulo, tam=tam, color=color, peso="700",
                   fuente=MONO))
    return "".join(s)


def leyenda_svg(y, items, ancho_item=None):
    """Fila de muestras al pie: (tipo, texto) con tipo en
    {'expandido', 'sin', 'final', 'nuevo'}."""
    s = []
    x = X_PIE
    for k, (tipo, rotulo) in enumerate(items):
        if k:
            # Cada muestra empieza donde acaba el texto anterior, con aire:
            # el ancho se estima por arriba (0.62 em por letra a 13 px), asi
            # que un rotulo largo nunca invade la muestra siguiente.
            x += ancho_item or (34 + 0.62 * 13 * len(items[k - 1][1]) + 26)
        if tipo == "final":
            s.append(caja(x - 3, y - 3, 30, 22, borde=COLOR_FINAL, grosor=1.5, radio=5))
            s.append(caja(x, y, 24, 16, borde=COLOR_FINAL, grosor=1.5, radio=4))
        elif tipo == "sin":
            s.append(caja(x, y, 24, 16, borde=SUAVE, grosor=2, radio=4, guiones="5 3"))
        elif tipo == "nuevo":
            s.append(caja(x, y, 24, 16, borde=ACENTO, grosor=3, radio=4))
        else:
            s.append(caja(x, y, 24, 16, borde=SUAVE, grosor=2, radio=4))
        s.append(texto(x + 34, y + 13, rotulo, tam=13, color=SUAVE, anclaje="start"))
    assert x + 34 + 0.62 * 13 * len(rotulo) <= ANCHO, items
    return "".join(s)


def rastro_svg(y, jugadas_previas, destino=None):
    """Renglon con el camino que lleva al nodo de arriba (ese nodo ya lleva
    su nombre en el dibujo)."""
    return texto(X_PIE, y, "Camino desde s₀: " + ", ".join(jugadas_previas), tam=14,
                 color=SUAVE, anclaje="start")


def nota_svg(y, renglones, tam=15):
    """Renglones cortos a la izquierda, uno debajo de otro."""
    return "".join(texto(X_PIE, y + 22 * k, r, tam=tam, anclaje="start")
                   for k, r in enumerate(renglones))


# ------------------------------------------- el ciclo de una partida (C1) ---

def texto_con_sub(x, y, partes, color=TEXTO, tam=16, peso="normal", anclaje="middle"):
    """Texto con subindices, como S_F: partes = [(cadena, es_sub)].

    El subindice baja con dy y no con baseline-shift, que Firefox ignora."""
    baja, chica = round(tam * 0.3, 1), round(tam * 0.72, 1)
    s, abajo = [], False
    for cadena, sub in partes:
        if sub and not abajo:
            s.append(f'<tspan dy="{baja}" font-size="{chica}">{escape(cadena)}</tspan>')
            abajo = True
        elif not sub and abajo:
            s.append(f'<tspan dy="-{baja}">{escape(cadena)}</tspan>')
            abajo = False
        else:
            s.append(f"<tspan>{escape(cadena)}</tspan>")
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{FUENTE}" '
            f'font-size="{tam}" font-weight="{peso}" text-anchor="{anclaje}">'
            + "".join(s) + "</text>")


# Lo que pregunta cada caja del ciclo y la pieza que la contesta.
CICLO_CAJAS = [
    ("estado", "Estado s", [("un elemento de S", False)]),
    ("pl", "¿A quién le toca?", [("Pl(s): MAX o MIN", False)]),
    ("a", "¿Qué puede hacer?", [("A(s): las jugadas permitidas", False)]),
    ("elige", "Elige una jugada a ∈ A(s)", [("ninguna regla dice cuál", False)]),
    ("t", "¿A dónde lleva?", [("el nuevo estado T(s, a)", False)]),
]


def jue_ciclo_partida():
    """Una partida como ciclo: las siete piezas son sus cajas.

    La caja de elegir va resaltada: es la unica que las reglas no contestan,
    y es la pregunta que resuelve el resto de la unidad. El texto es grande a
    proposito: la figura se lee entera en una pantalla, sin acercarse."""
    o = 24  # lo que baja todo por el titulo en dos renglones
    W, H = ANCHO, 745 + o
    cx, bw, bh = 240, 320, 60
    izq, carril = cx - bw / 2, 48
    regla = mezclar(LINEA, 0.22)
    desc = ("Diagrama de flujo de una partida. Se entra con el estado inicial s₀. "
            "En cada vuelta se pregunta si el estado s terminó, es decir, si está en "
            "S_F; si sí, la partida sale con U(s), lo que vale el resultado. Si no, "
            "Pl(s) dice a quién le toca, A(s) qué jugadas puede hacer, el jugador "
            "elige una jugada a, y T(s, a) da el nuevo estado, con el que se vuelve "
            "arriba. La caja de elegir está resaltada: es la única que no dan las "
            "reglas, y es lo que queremos decidir.")
    titulo = "Una partida, vuelta por vuelta"
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, ["Una partida,", "vuelta por vuelta"])

    # Entrada: el estado inicial.
    out.append(caja(cx - 130, 58 + o, 260, 44, relleno=mezclar(SERIE[0], 0.14),
                    borde=SERIE[0], radio=22))
    out.append(texto(cx, 87 + o, "Empieza: s = s₀", tam=19, peso="700"))
    out.append(flecha(cx, 102 + o, cx, 123 + o, color=SUAVE, marcador="s"))

    def caja_regla(cy, r1, r2, resaltada=False, alto=bh):
        borde = ACENTO if resaltada else LINEA
        relleno = mezclar(ACENTO, 0.2) if resaltada else regla
        s = [caja(izq, cy - alto / 2, bw, alto, relleno=relleno, borde=borde,
                  grosor=4 if resaltada else 2)]
        s.append(texto(cx, cy - 5, r1, tam=19, peso="700"))
        s.append(texto_con_sub(cx, cy + 19, r2, color=ACENTO if resaltada else SUAVE,
                               tam=16, peso="700" if resaltada else "normal"))
        return "".join(s)

    ys = {k: v + o for k, v in
          {"estado": 155, "rombo": 262, "pl": 369, "a": 456, "elige": 547, "t": 640}.items()}
    cajas = {clave: (r1, r2) for clave, r1, r2 in CICLO_CAJAS}

    out.append(caja_regla(ys["estado"], *cajas["estado"]))
    out.append(flecha(cx, ys["estado"] + bh / 2, cx, 208 + o, color=SUAVE, marcador="s"))

    # La pregunta de los finales.
    yr, mx, my = ys["rombo"], 140, 52
    out.append(_rombo(cx, yr, mx, my, mezclar(SERIE[1], 0.16), mezclar(SERIE[1], 0.6)))
    out.append(texto(cx, yr - 5, "¿Terminó?", tam=19, peso="700"))
    out.append(texto_con_sub(cx, yr + 19, [("¿s ∈ S", False), ("F", True), ("?", False)],
                             color=SUAVE, tam=16))

    # Si terminó: sale con su utilidad.
    ux, uw, uh = 505, 160, 104
    out.append(flecha(cx + mx, yr, ux - uw / 2 - 4, yr, color=SUAVE, marcador="s"))
    out.append(texto(cx + mx + 18, yr - 10, "sí", tam=17, color=SUAVE, peso="700"))
    out.append(caja(ux - uw / 2 - 5, yr - uh / 2 - 5, uw + 10, uh + 10,
                    borde=COLOR_FINAL, grosor=2))
    out.append(caja(ux - uw / 2, yr - uh / 2, uw, uh, relleno=mezclar(COLOR_FINAL, 0.12),
                    borde=COLOR_FINAL, grosor=2))
    out.append(texto(ux, yr - 18, "Fin de la partida", tam=16, peso="700"))
    out.append(texto(ux, yr + 8, "U(s):", tam=17, color=COLOR_FINAL, peso="700"))
    out.append(texto(ux, yr + 32, "cuánto vale", tam=16, color=SUAVE))

    # Si no terminó: las preguntas del turno.
    out.append(flecha(cx, yr + my, cx, ys["pl"] - bh / 2 - 2, color=SUAVE, marcador="s"))
    out.append(texto(cx + 14, yr + my + 22, "no", tam=17, color=SUAVE, peso="700",
                     anclaje="start"))
    out.append(caja_regla(ys["pl"], *cajas["pl"]))
    out.append(flecha(cx, ys["pl"] + bh / 2, cx, ys["a"] - bh / 2 - 2, color=SUAVE,
                      marcador="s"))
    out.append(caja_regla(ys["a"], *cajas["a"]))
    out.append(flecha(cx, ys["a"] + bh / 2, cx, ys["elige"] - 36 - 2, color=SUAVE,
                      marcador="s"))
    out.append(caja_regla(ys["elige"], *cajas["elige"], resaltada=True, alto=72))
    # La nota que distingue la caja de elegir.
    nx = izq + bw + 16
    for k, (renglon, peso) in enumerate([("Lo único que", "700"),
                                         ("no dan las", "700"),
                                         ("reglas:", "700"),
                                         ("es lo que", "normal"),
                                         ("queremos decidir", "normal")]):
        out.append(texto(nx, ys["elige"] - 36 + 22 * k, renglon, tam=16, color=ACENTO,
                         peso=peso, anclaje="start"))
    out.append(flecha(cx, ys["elige"] + 36, cx, ys["t"] - bh / 2 - 2, color=SUAVE,
                      marcador="s"))
    out.append(caja_regla(ys["t"], *cajas["t"]))

    # Carril de regreso: el nuevo estado vuelve arriba.
    out.append(linea(izq, ys["t"], carril, ys["t"], color=SUAVE))
    out.append(linea(carril, ys["t"], carril, ys["estado"], color=SUAVE))
    out.append(flecha(carril, ys["estado"], izq - 2, ys["estado"], color=SUAVE, marcador="s"))
    ym = (ys["estado"] + ys["t"]) / 2
    out.append(f'<text x="{carril - 14}" y="{ym}" fill="{SUAVE}" font-family="{FUENTE}" '
               f'font-size="16" font-weight="700" text-anchor="middle" '
               f'transform="rotate(-90 {carril - 14} {ym})">otra vuelta con el nuevo estado</text>')

    # Leyenda: qué cajas dan las reglas y cuál no.
    ly = H - 34
    out.append(caja(X_PIE, ly - 12, 30, 22, relleno=regla, borde=LINEA, radio=5))
    out.append(texto(X_PIE + 40, ly + 5, "lo contestan las reglas", tam=15, color=SUAVE,
                     anclaje="start"))
    out.append(caja(300, ly - 12, 30, 22, relleno=mezclar(ACENTO, 0.2), borde=ACENTO,
                    radio=5, grosor=3))
    out.append(texto(340, ly + 5, "lo decide el jugador", tam=15, color=SUAVE,
                     anclaje="start"))
    out.append(cierre())
    return "".join(out)


# --------------------------------------------- el grafo, paso a paso (C1) ---

PASOS_TITULO = {
    1: "Paso 1 · Un nodo: el estado inicial",
    2: "Paso 2 · Expandir s₀: una flecha por jugada",
    3: "Paso 3 · Expandir un nodo de MIN (mueve Negras)",
    4: "Paso 4 · Llegar a un final y escribir su U",
}


# El mismo titulo, partido en renglones que caben en un telefono.
PASOS_RENGLONES = {
    1: ["Paso 1 · Un nodo:", "el estado inicial"],
    2: ["Paso 2 · Expandir s₀:", "una flecha por jugada"],
    3: ["Paso 3 · Expandir un nodo", "de MIN (mueve Negras)"],
    4: ["Paso 4 · Llegar a un final", "y escribir su U"],
}


def _titulo_paso(titulo):
    paso = next(k for k, v in PASOS_TITULO.items() if v == titulo)
    assert " ".join(PASOS_RENGLONES[paso]) == titulo.replace("  ", " ")
    return PASOS_RENGLONES[paso]


def _paso_1():
    o = 24
    W, H = ANCHO, 540
    titulo = PASOS_TITULO[1]
    desc = ("El estado inicial s₀ dibujado en grande: el tablero con tres peones "
            "blancos en la fila 1 y tres negros en la fila 3, y el turno de Blancas, "
            "que es MAX. El borde punteado indica que todavía no se calcularon sus jugadas.")
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, _titulo_paso(titulo))
    cx, cy, w, h = 170, 250 + o, 250, 290
    out.append(nodo_svg(cx, cy, j.inicio(), "B", "s₀", expandido=False, w=w, h=h, celda=56))
    # Anotaciones a la derecha, con su flecha hacia la parte del nodo.
    notas = [
        (cy - 112, "Nombre del nodo:", "s₀, el estado inicial", cy - 118),
        (cy - 10, "El tablero τ: qué", "hay en cada casilla", cy - 18),
        (cy + 104, "El turno: Blancas,", "así que Pl(s₀) = MAX", cy + 112),
    ]
    for ytxt, l1, l2, ydest in notas:
        out.append(flecha(368, ytxt - 5, cx + w / 2 + 8, ydest, color=SUAVE, marcador="s"))
        out.append(texto(378, ytxt - 6, l1, tam=16, anclaje="start"))
        out.append(texto(378, ytxt + 16, l2, tam=16, anclaje="start", color=SUAVE))
    out.append(nota_svg(H - 76, ["Borde punteado: el nodo existe,",
                                 "pero todavía no sabemos qué",
                                 "jugadas salen de él."]))
    out.append(cierre())
    return "".join(out)


def _xs_hijos(n, paso3=200, paso2=250):
    paso_x = paso3 if n == 3 else paso2
    return [ANCHO / 2 + (k - (n - 1) / 2) * paso_x for k in range(n)]


def _paso_hijos(paso, previas, rotulo_padre, rotulos_hijos, notas):
    """Pasos 2 a 4: un padre arriba y sus hijos abajo."""
    W = ANCHO
    tp, pp = jugar(j.inicio(), "B", previas)
    hs = hijos(tp, pp)
    n = len(hs)
    xs_hijos = _xs_hijos(n)
    o = 30
    y_padre, y_hijo = 200 + o, 500 + o
    H = y_hijo + 135 + 22 * len(notas) + 52
    desc = (f"Arriba, {rotulo_padre}; abajo, sus {n} hijos: "
            + "; ".join(f"{nombre} lleva a un estado donde "
                        + tipo_de_nodo(t, p)[1].lower() for nombre, t, p in hs) + ".")
    titulo = PASOS_TITULO[paso]
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, _titulo_paso(titulo))
    if previas:
        out.append(rastro_svg(y + 26, previas))
    for (nombre, t, p), x in zip(hs, xs_hijos):
        out.append(arista_svg(W / 2, y_padre, x, y_hijo, nombre, nueva=True, h=190))
    out.append(nodo_svg(W / 2, y_padre, tp, pp, rotulo_padre, w=180, h=190, celda=32))
    for (nombre, t, p), x in zip(hs, xs_hijos):
        out.append(nodo_svg(x, y_hijo, t, p, rotulos_hijos.get(nombre, f"T(·, {nombre})"),
                            nuevo=True, expandido=bool(j.ganador(t, p)), w=180, h=190, celda=32))
    out.append(nota_svg(y_hijo + 135, notas))
    out.append(leyenda_svg(H - 34, [("nuevo", "nuevo en este paso"),
                                    ("sin", "sin expandir"),
                                    ("final", "final")]))
    out.append(cierre())
    return "".join(out)


def jue_grafo_paso(paso):
    """El grafo de hexapawn construido desde s0, una pieza por paso.

    Paso 1: s0 en grande, con sus partes anotadas. Pasos 2 a 4: el nodo que
    se expande y sus hijos, con el camino que lleva a el."""
    if paso not in PASOS_TITULO:
        raise ValueError("El grafo paso a paso admite pasos de 1 a 4")
    if paso == 1:
        return _paso_1()
    if paso == 2:
        return _paso_hijos(2, [], "s₀",
                           {"a1-a2": "T(s₀, a1-a2)", "b1-b2": "T(s₀, b1-b2)",
                            "c1-c2": "T(s₀, c1-c2)"},
                           ["A(s₀) tiene 3 jugadas: salen 3 flechas.",
                            "Cada flecha llega a T(s₀, a).",
                            "Ahora mueve Negras."])
    if paso == 3:
        return _paso_hijos(3, ["a1-a2"], "tras a1-a2",
                           {"b3-b2": "n1", "b3xa2": "tras b3xa2", "c3-c2": "tras c3-c2"},
                           ["Las mismas funciones A y T sirven",
                            "para Negras: 3 respuestas, y en los",
                            "hijos vuelve a mover Blancas."])
    return _paso_hijos(4, ["a1-a2", "b3-b2"], "n1",
                       {"c1-c2": "n2", "c1xb2": "n3"},
                       ["n2 es final: Negras no tiene jugada",
                        "y gana Blancas. Su número es",
                        "U(n2) = +1. n3 todavía no se expande."])


# ------------------------------------------- el subgrafo completo de n1 ---

# (x, nivel) de cada nodo; el ancho cabe en ANCHO. El nivel 3 lleva cuatro
# nodos (n5, n7, n11, n12): ahi se decide el ancho de los nodos.
LUGARES_N1 = {1: (300, 0), 2: (100, 1), 3: (360, 1),
              4: (76, 2), 6: (370, 2), 13: (518, 2),
              5: (76, 3), 7: (222, 3), 11: (370, 3), 12: (518, 3),
              8: (222, 4), 9: (150, 5), 10: (296, 5)}
NODO_SUB, NODO_ALTO_SUB = 130, 146  # nodos del subgrafo


def jue_subgrafo_n1():
    """Los 13 estados alcanzables desde n1, con su jugador o su utilidad."""
    nodos = subgrafo_n1()
    W, y0, dy = ANCHO, 185, 228
    H = y0 + 5 * dy + 150
    finales = [n for n, (t, p, _, _) in nodos.items() if j.ganador(t, p)]
    desc = (f"El grafo completo desde n1, el estado tras a1-a2 y b3-b2: "
            f"{len(nodos)} nodos numerados n1 a n{len(nodos)} en el orden en que se recorren, "
            f"{len(finales)} de ellos finales con su utilidad. Las flechas llevan el nombre de la jugada.")
    titulo = "El grafo completo desde n1"
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, titulo)
    out.append(rastro_svg(y + 26, CAMINO_N1, "n1"))
    for n, (t, p, padre, jugada) in nodos.items():
        if padre is None:
            continue
        x1, l1 = LUGARES_N1[padre]
        x2, l2 = LUGARES_N1[n]
        out.append(arista_svg(x1, y0 + l1 * dy, x2, y0 + l2 * dy, jugada, h=NODO_ALTO_SUB,
                              t=T_JUGADA_N1.get(n, 0.5)))
    for n, (t, p, _, _) in nodos.items():
        x, nivel = LUGARES_N1[n]
        out.append(nodo_svg(x, y0 + nivel * dy, t, p, f"n{n}", w=NODO_SUB, h=NODO_ALTO_SUB,
                            celda=21))
    out.append(leyenda_svg(H - 34, [("expandido", "con hijos"), ("final", "final, con su U")]))
    out.append(cierre())
    return "".join(out)


# Donde va el rotulo de la jugada en cada arista del subgrafo: las tres de
# n6 salen juntas, y a la mitad sus rotulos se encimarian.
T_JUGADA_N1 = {7: 0.62, 11: 0.4, 12: 0.62, 4: 0.55, 13: 0.55, 6: 0.42}


# ------------------------------------------------------ la transposicion ---

CAMINO_A = ["a1-a2", "b3-b2", "c1-c2"]
CAMINO_B = ["c1-c2", "b3-b2", "a1-a2"]
NODO_TR, NODO_ALTO_TR = 128, 146


def jue_transposicion():
    """Dos ordenes de jugadas, el mismo estado: dos nodos en el arbol y uno
    en el grafo."""
    W, y0, dy = ANCHO, 205, 228
    H = y0 + 3 * dy + 190
    final_a = jugar(j.inicio(), "B", CAMINO_A)
    final_b = jugar(j.inicio(), "B", CAMINO_B)
    assert final_a == final_b, "los dos caminos deben llegar al mismo estado"
    desc = ("Izquierda, árbol de partidas: los caminos a1-a2, b3-b2, c1-c2 y "
            "c1-c2, b3-b2, a1-a2 terminan en dos nodos con el mismo tablero, n2. "
            "Derecha, grafo de estados: los dos caminos llegan a un solo nodo.")
    titulo = "Dos caminos, el mismo estado"
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, ["Dos caminos,", "el mismo estado"])
    out.append(texto(148, 104, "Árbol de partidas", tam=17, peso="700", color=SUAVE))
    out.append(texto(452, 104, "Grafo de estados", tam=17, peso="700", color=SUAVE))
    out.append(linea(300, 86, 300, H - 100, color=LINEA, grosor=1.5, guiones="4 6"))
    kw = dict(w=NODO_TR, h=NODO_ALTO_TR, celda=20)

    def camino(x_raiz, x_rama, nombres, x_final=None, rotulos=("", "", "")):
        t, p = j.inicio(), "B"
        previo = (x_raiz, y0)
        aristas, nodos_ = [], []
        for k, nombre in enumerate(nombres):
            t, p = jugar(t, p, [nombre])
            x = x_final if (x_final is not None and k == len(nombres) - 1) else x_rama
            y = y0 + (k + 1) * dy
            aristas.append(arista_svg(previo[0], previo[1], x, y, nombre, h=NODO_ALTO_TR))
            if not (x_final is not None and k == len(nombres) - 1):
                nodos_.append(nodo_svg(x, y, t, p, rotulos[k], **kw))
            previo = (x, y)
        return aristas, nodos_

    a1, n1_ = camino(148, 76, CAMINO_A, rotulos=("", "n1", "n2 (copia 1)"))
    a2, n2_ = camino(148, 220, CAMINO_B, rotulos=("", "", "n2 (copia 2)"))
    a3, n3_ = camino(452, 380, CAMINO_A, x_final=452, rotulos=("", "n1", ""))
    a4, n4_ = camino(452, 524, CAMINO_B, x_final=452)
    out += a1 + a2 + a3 + a4
    out.append(nodo_svg(148, y0, j.inicio(), "B", "s₀", **kw))
    out.append(nodo_svg(452, y0, j.inicio(), "B", "s₀", **kw))
    out += n1_ + n2_ + n3_ + n4_
    out.append(nodo_svg(452, y0 + 3 * dy, *final_a, "n2: un nodo", nuevo=True, **kw))
    out.append(nota_svg(H - 58, ["El estado no recuerda por qué camino",
                                 "se llegó: en el grafo es un solo nodo."]))
    out.append(cierre())
    return "".join(out)


# ============================================================ clase 2 ===
#
# Las figuras de la clase 2 reusan la geometria del subgrafo de n1 de la
# clase 1 (LUGARES_N1): el lector ya conoce ese dibujo, y ahora se le van
# escribiendo encima los valores, el recorrido y las podas. Todo numero que
# aparece se calcula con juegos.py.

COLOR_AZAR = TEXTO


def fmt(v):
    """+1, −1, 0, 1/3, ±∞: como se escribe un valor en las figuras."""
    if v == float("inf"):
        return "+∞"
    if v == float("-inf"):
        return "−∞"
    if hasattr(v, "denominator") and v.denominator != 1:
        signo = "−" if v < 0 else ""
        return f"{signo}{abs(v.numerator)}/{v.denominator}"
    v = int(v)
    return f"+{v}" if v > 0 else ("0" if v == 0 else f"−{-v}")


def valores_n1(sin_jugada_empata=False):
    """n -> V(n) en el subgrafo de n1, con utilidad +1/−1."""
    return {n: j.valor(t, p, sin_jugada_empata=sin_jugada_empata)
            for n, (t, p, _, _) in subgrafo_n1().items()}


def elegidas_n1(valores):
    """Aristas (padre, hijo) cuyo hijo alcanza el valor del padre: las
    jugadas del arg max en MAX y del arg min en MIN."""
    nodos = subgrafo_n1()
    return {(padre, n) for n, (_, _, padre, _) in nodos.items()
            if padre is not None and valores[n] == valores[padre]}


def renglones_valor(tablero, turno, v):
    """Los dos renglones de un nodo ya valorado."""
    if j.ganador(tablero, turno):
        return None  # un final se queda como en la clase 1: quien gana y su U
    quien = "Mueve Blancas" if turno == "B" else "Mueve Negras"
    return quien, f"{'MAX' if turno == 'B' else 'MIN'} · V = {fmt(v)}"


# Que nodo se valora en cada paso de «Minimax a mano», y que se dice debajo.
PASOS_MINIMAX = {
    1: (6, "Paso 1 · Valorar n6: Blancas toma el máximo",
        ["n7 ya vale +1: Negras está obligada",
         "a jugar a3xb2 y luego gana Blancas.",
         "max{+1, +1, +1} = +1: las tres",
         "jugadas empatan."]),
    2: (3, "Paso 2 · Valorar n3: Negras toma el mínimo",
        ["min{+1, +1, −1} = −1. A Negras le basta",
         "una respuesta buena: c3xb2 deja",
         "a Blancas sin jugada."]),
    3: (1, "Paso 3 · Valorar n1: la jugada de Blancas",
        ["max{+1, −1} = +1, con c1-c2.",
         "Capturar en b2 pierde: Negras",
         "respondería c3xb2."]),
}


def camino_n1(n):
    """Las jugadas desde s0 hasta el nodo n del subgrafo."""
    nodos = subgrafo_n1()
    jugadas_ = []
    while nodos[n][2] is not None:
        jugadas_.append(nodos[n][3])
        n = nodos[n][2]
    return CAMINO_N1 + jugadas_[::-1]


def jue_minimax_paso(paso):
    """Un paso de minimax a mano: el nodo que se valora arriba, sus hijos ya
    valorados abajo y, resaltadas, las jugadas que alcanzan su valor."""
    if paso not in PASOS_MINIMAX:
        raise ValueError("Minimax paso a paso admite pasos de 1 a 3")
    n, titulo, notas = PASOS_MINIMAX[paso]
    nodos, valores = subgrafo_n1(), valores_n1()
    elegidas = elegidas_n1(valores)
    tp, pp, _, _ = nodos[n]
    hijos_ = [m for m, (_, _, padre, _) in nodos.items() if padre == n]
    W, y_padre, y_hijo = ANCHO, 236, 536
    H = y_hijo + 140 + 22 * len(notas) + 50
    xs = _xs_hijos(len(hijos_))
    operacion = "máximo" if pp == "B" else "mínimo"
    desc = (f"{titulo}. Arriba, n{n}, donde {'mueve Blancas (MAX)' if pp == 'B' else 'mueve Negras (MIN)'}; "
            "abajo, sus hijos con su valor: "
            + "; ".join(f"{nodos[m][3]} lleva a n{m}, que vale {fmt(valores[m])}" for m in hijos_)
            + f". El {operacion} es {fmt(valores[n])}, así que V(n{n}) = {fmt(valores[n])}; "
            "las jugadas que lo alcanzan van resaltadas.")
    out = [marco(W, H, desc, titulo, desc)]
    cabeza, resto = titulo.split(": ", 1)
    y = encabezado(out, [cabeza + ":", resto])
    out.append(rastro_svg(y + 26, camino_n1(n), f"n{n}"))
    for m, x in zip(hijos_, xs):
        out.append(arista_svg(W / 2, y_padre, x, y_hijo, nodos[m][3],
                              nueva=(n, m) in elegidas, h=190))
    out.append(nodo_svg(W / 2, y_padre, tp, pp, f"n{n}", nuevo=True, w=180, h=190, celda=32,
                        renglones=renglones_valor(tp, pp, valores[n])))
    for m, x in zip(hijos_, xs):
        t, p, _, _ = nodos[m]
        out.append(nodo_svg(x, y_hijo, t, p, f"n{m}", w=180, h=190, celda=32,
                            renglones=renglones_valor(t, p, valores[m])))
    out.append(nota_svg(y_hijo + 140, notas))
    out.append(leyenda_svg(H - 34, [("nuevo", "se valora en este paso"),
                                    ("expandido", "ya valorado"),
                                    ("final", "final, con su U")]))
    out.append(cierre())
    return "".join(out)


def _dibujar_n1(out, lugares, y0, dy, valores=None, elegidas=(), renglones=None,
                fantasmas=(), tenues=(), nuevos=(), ordenes=None, etiquetas_corte=None):
    """El subgrafo de n1 con la geometria de la clase 1.

    `fantasmas`: nodos que nunca se generan (sin tablero, borde punteado).
    `tenues`: aristas hacia un fantasma, con la jugada conocida.
    `etiquetas_corte`: {(padre, hijo): texto} sobre la arista donde se corta."""
    nodos = subgrafo_n1()
    etiquetas_corte = etiquetas_corte or {}
    for n, (t, p, padre, jugada) in nodos.items():
        if padre is None:
            continue
        x1, l1 = lugares[padre]
        x2, l2 = lugares[n]
        if padre in fantasmas:
            out.append(linea(x1, y0 + l1 * dy + NODO_ALTO_SUB / 2, x2,
                             y0 + l2 * dy - NODO_ALTO_SUB / 2, color=LINEA, grosor=1.5,
                             guiones="4 6"))
            continue
        out.append(arista_svg(x1, y0 + l1 * dy, x2, y0 + l2 * dy, jugada,
                              nueva=(padre, n) in elegidas, h=NODO_ALTO_SUB,
                              tenue=n in fantasmas, t=T_JUGADA_N1.get(n, 0.5)))
    # El corte: una barra de acento que atraviesa las aristas que ya no se
    # siguen, justo debajo del nodo que corta, con el tipo de corte al lado.
    for (padre, primero), rotulo in etiquetas_corte.items():
        hermanos = [m for m, (_, _, pa, _) in nodos.items() if pa == padre]
        cortados = [m for m in hermanos if m in fantasmas]
        xp, lp = lugares[padre]
        yb = y0 + lp * dy + NODO_ALTO_SUB / 2
        ym = y0 + (lp + 1) * dy - NODO_ALTO_SUB / 2 - 8
        yc = yb + 0.8 * (ym - yb)  # debajo de los rotulos de las jugadas
        xs = []
        for m in cortados:
            xm, _ = lugares[m]
            xs.append(xp + (xm - xp) * (yc - yb) / (ym - yb))
        x_a, x_b = min(xs) - 14, max(xs) + 14
        out.append(linea(x_a, yc, x_b, yc, color=ACENTO, grosor=5))
        a_la_derecha = x_b + 120 < ANCHO
        out.append(texto(x_b + 8 if a_la_derecha else x_a - 8, yc + 5, rotulo, tam=15,
                         color=ACENTO, peso="700", anclaje="start" if a_la_derecha else "end"))
    for n, (t, p, _, _) in nodos.items():
        x, nivel = lugares[n]
        y = y0 + nivel * dy
        if n in fantasmas:
            w, h = NODO_SUB, NODO_ALTO_SUB
            out.append(caja(x - w / 2, y - h / 2, w, h, relleno=FONDO, borde=LINEA,
                            grosor=2, guiones="7 6"))
            out.append(texto(x, y - 32, f"n{n}", tam=16, color=SUAVE, peso="700"))
            out.append(texto(x, y + 6, "?", tam=30, color=LINEA, peso="700"))
            out.append(texto(x, y + 44, "no se genera", tam=13, color=SUAVE))
            continue
        r = renglones(n, t, p) if renglones else (
            renglones_valor(t, p, valores[n]) if valores else None)
        out.append(nodo_svg(x, y, t, p, f"n{n}", nuevo=n in nuevos, w=NODO_SUB,
                            h=NODO_ALTO_SUB, celda=21, renglones=r,
                            orden=(ordenes or {}).get(n)))


def jue_minimax_n1():
    """El subgrafo de n1 resuelto: cada nodo con su V y, resaltadas, las
    jugadas que alcanzan el valor de su padre."""
    nodos, valores = subgrafo_n1(), valores_n1()
    W, y0, dy = ANCHO, 185, 228
    H = y0 + 5 * dy + 150
    titulo = "El subgrafo de n1, resuelto"
    desc = ("El mismo grafo de n1 de la clase 1, con un valor en cada nodo: "
            + ", ".join(f"V(n{n}) = {fmt(v)}" for n, v in valores.items())
            + ". Van resaltadas las jugadas que alcanzan el valor de su padre: c1-c2 en n1, "
            "c3xb2 en n3 y las tres jugadas de n6, que empatan.")
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, titulo)
    out.append(rastro_svg(y + 26, CAMINO_N1, "n1"))
    _dibujar_n1(out, LUGARES_N1, y0, dy, valores=valores, elegidas=elegidas_n1(valores))
    out.append(leyenda_svg(H - 34, [("nuevo", "jugada que alcanza el valor"),
                                    ("final", "final, con su U")]))
    out.append(cierre())
    return "".join(out)


# El momento que congela «Minimax como algoritmo»: MINIMAX(n8) acaba de
# empezar. En la pila esperan n1, n3, n6 y n7; n2 y n4 ya devolvieron su
# valor y se olvidaron (n5 con n4); lo demas todavia no existe.
EN_PILA = [1, 3, 6, 7, 8]
YA_DEVOLVIERON = [2, 4, 5]
SIN_GENERAR = [9, 10, 11, 12, 13]


def jue_minimax_genera():
    """Lo que hay en memoria a media ejecucion de MINIMAX desde n1."""
    nodos, valores = subgrafo_n1(), valores_n1()
    assert sorted(EN_PILA + YA_DEVOLVIERON + SIN_GENERAR) == sorted(nodos)
    W, y0, dy = ANCHO, 190, 228
    H = y0 + 5 * dy + 150
    titulo = "MINIMAX a media ejecución"
    desc = ("El subgrafo de n1 en el momento en que MINIMAX empieza a valorar n8. "
            "En memoria solo está el camino n1, n3, n6, n7, n8, cada uno esperando a "
            "sus hijos con el mejor valor visto hasta ahora. n2 y n4 ya devolvieron "
            "+1 y se olvidaron, con n5. n9, n10, n11, n12 y n13 todavía no se generan.")
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, [titulo, "Empieza MINIMAX(n8)."])
    out.append(texto(X_PIE, y + 26, "¿Qué hay en memoria?", tam=15, color=SUAVE,
                     anclaje="start"))
    # v visto hasta ahora en cada nodo de la pila, recorriendo en el orden fijo.
    v_hasta_ahora = {}
    for n in EN_PILA:
        t, p, _, _ = nodos[n]
        hechos = [valores[m] for m, (_, _, padre, _) in nodos.items()
                  if padre == n and m in YA_DEVOLVIERON]
        if p == "B":
            v_hasta_ahora[n] = max(hechos, default=float("-inf"))
        else:
            v_hasta_ahora[n] = min(hechos, default=float("inf"))
    lugares = LUGARES_N1
    for n, (t, p, padre, jugada) in nodos.items():
        if padre is None:
            continue
        x1, l1 = lugares[padre]
        x2, l2 = lugares[n]
        y1, y2 = y0 + l1 * dy, y0 + l2 * dy
        if n in EN_PILA:
            out.append(arista_svg(x1, y1, x2, y2, jugada, nueva=True, h=NODO_ALTO_SUB,
                                  t=T_JUGADA_N1.get(n, 0.5)))
        else:
            out.append(linea(x1, y1 + NODO_ALTO_SUB / 2, x2, y2 - NODO_ALTO_SUB / 2,
                             color=LINEA, grosor=1.5, guiones="4 6"))
    for n, (t, p, _, _) in nodos.items():
        x, nivel = lugares[n]
        y = y0 + nivel * dy
        w, h = NODO_SUB, NODO_ALTO_SUB
        if n in EN_PILA:
            quien = "MAX" if p == "B" else "MIN"
            out.append(nodo_svg(x, y, t, p, f"n{n}", nuevo=True, w=w, h=h, celda=21,
                                renglones=(f"{quien} · espera", f"v = {fmt(v_hasta_ahora[n])}")))
        elif n in YA_DEVOLVIERON:
            out.append(caja(x - w / 2, y - h / 2, w, h, relleno=FONDO, borde=SUAVE,
                            grosor=1.5, guiones="2 5"))
            out.append(texto(x, y - 32, f"n{n}", tam=16, color=SUAVE, peso="700"))
            out.append(texto(x, y + 2, f"devolvió {fmt(valores[n])}", tam=14, color=SUAVE,
                             peso="700"))
            out.append(texto(x, y + 26, "y se olvidó", tam=14, color=SUAVE))
        else:
            out.append(caja(x - w / 2, y - h / 2, w, h, relleno=FONDO, borde=LINEA,
                            grosor=2, guiones="7 6"))
            out.append(texto(x, y - 32, f"n{n}", tam=16, color=SUAVE, peso="700"))
            out.append(texto(x, y + 6, "?", tam=30, color=LINEA, peso="700"))
            out.append(texto(x, y + 44, "aún no existe", tam=13, color=SUAVE))
    ly = H - 34
    out.append(caja(X_PIE, ly, 24, 16, borde=ACENTO, grosor=3, radio=4))
    out.append(texto(X_PIE + 32, ly + 13, "en la pila: esperan", tam=13, color=SUAVE,
                     anclaje="start"))
    out.append(caja(212, ly, 24, 16, borde=SUAVE, grosor=1.5, radio=4, guiones="2 4"))
    out.append(texto(244, ly + 13, "devolvió y se olvidó", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(410, ly, 24, 16, borde=LINEA, grosor=2, radio=4, guiones="5 3"))
    out.append(texto(442, ly + 13, "todavía no se genera", tam=13, color=SUAVE, anclaje="start"))
    out.append(cierre())
    return "".join(out)


def jue_azar_n3():
    """n3 como nodo de azar: Negras elige al azar, cada jugada con 1/3."""
    nodos, valores = subgrafo_n1(), valores_n1()
    tp, pp, _, _ = nodos[3]
    hijos_ = [m for m, (_, _, padre, _) in nodos.items() if padre == 3]
    import fractions
    promedio = sum(fractions.Fraction(valores[m]) for m in hijos_) / len(hijos_)
    assert promedio == j.expectiminimax_rival_al_azar(tp, pp)
    W, H, y_padre, y_hijo = ANCHO, 760, 236, 536
    xs = _xs_hijos(3)
    titulo = "Si Negras eligiera al azar en n3"
    desc = ("n3 dibujado como nodo de azar: nadie elige, cada una de las tres jugadas de "
            "Negras sale con probabilidad 1/3. Sus hijos valen "
            + ", ".join(f"n{m} = {fmt(valores[m])}" for m in hijos_)
            + f". El nodo vale su promedio, {fmt(promedio)}.")
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, ["Si Negras eligiera", "al azar en n3"])
    out.append(rastro_svg(y + 26, camino_n1(3), "n3"))
    for m, x in zip(hijos_, xs):
        out.append(arista_svg(W / 2, y_padre, x, y_hijo, f"{nodos[m][3]}: ⅓", h=190,
                              t=0.55))
    out.append(nodo_svg(W / 2, y_padre, tp, pp, "n3", nuevo=True, w=180, h=190, celda=32,
                        color=COLOR_AZAR, radio=45,
                        renglones=("AZAR: nadie elige", f"V = {fmt(promedio)}")))
    for m, x in zip(hijos_, xs):
        t, p, _, _ = nodos[m]
        out.append(nodo_svg(x, y_hijo, t, p, f"n{m}", w=180, h=190, celda=32,
                            renglones=renglones_valor(t, p, valores[m])))
    out.append(nota_svg(y_hijo + 140, ["Se promedia con las probabilidades:",
                                       "⅓(+1) + ⅓(+1) + ⅓(−1) = 1/3."]))
    ly = H - 34
    out.append(caja(X_PIE, ly - 3, 30, 22, borde=COLOR_AZAR, grosor=2, radio=11))
    out.append(texto(X_PIE + 40, ly + 13, "nodo de azar: esquinas redondas", tam=13,
                     color=SUAVE, anclaje="start"))
    out.append(caja(320, ly, 24, 16, borde=ACENTO, grosor=3, radio=4))
    out.append(texto(354, ly + 13, "se valora en este paso", tam=13, color=SUAVE,
                     anclaje="start"))
    out.append(cierre())
    return "".join(out)


def traza_n1(invertir=False, sin_jugada_empata=False):
    """Alfa-beta desde n1, traducido a numeros de nodo.

    Devuelve (visitas, cortes): visitas es {n: (orden, tipo, alfa, beta,
    devuelve)} y cortes es {(padre, primer hijo no visitado): tipo}."""
    nodos = subgrafo_n1()
    por_camino = {tuple(camino_n1(n)[len(CAMINO_N1):]): n for n in nodos}
    t, p, _, _ = nodos[1]
    r = j.alfa_beta_traza(t, p, invertir=invertir, sin_jugada_empata=sin_jugada_empata)
    visitas = {por_camino[c]: (k + 1, tipo, a, b, v)
               for k, (c, tipo, a, b, v) in enumerate(r["visitas"])}
    cortes = {}
    for tipo, camino, jugada, _ in r["cortes"]:
        padre = por_camino[camino]
        hermanos = [m for m, (_, _, pa, _) in nodos.items() if pa == padre]
        if invertir:
            hermanos = hermanos[::-1]
        k = hermanos.index(por_camino[camino + (jugada,)])
        cortes[(padre, hermanos[k + 1])] = tipo
    return visitas, cortes


def jue_alfa_beta(invertir=False):
    """Alfa-beta desde n1: orden de visita, alfa y beta al llegar, lo que
    devuelve cada nodo, el corte y, en una caja por subarbol, lo que nunca se
    genera. Misma geometria que las figuras por partes, con letra chica."""
    nodos = subgrafo_n1()
    visitas, cortes = traza_n1(invertir)
    lugares = LUGARES_INV if invertir else LUGARES_FIJO
    grupos = FANTASMAS_INV if invertir else FANTASMAS_FIJO
    # Cada nodo no generado cae en exactamente un fantasma.
    assert sorted(m for g in grupos.values() for m in g) == sorted(
        n for n in nodos if n not in visitas)
    assert all(_subarbol(n) == g for n, g in grupos.items())
    # El nodo que corta devuelve una cota: ≤ en MIN, ≥ en MAX.
    cota = {padre: "≤ " if tipo == "alfa" else "≥ " for (padre, _), tipo in cortes.items()}
    esc = CHICA
    ys = esc["ys_inv" if invertir else "ys_fijo"]
    H = round(esc["y0"] + ys[3] + esc["h"] / 2 + 80)
    orden_txt = "invertido" if invertir else "fijo"
    titulo = f"Alfa-beta con el orden {orden_txt}: {len(visitas)} de {len(nodos)} nodos"
    corte_txt = "; ".join(f"corte {tipo} en n{padre}" for (padre, _), tipo in cortes.items())
    desc = (f"El subgrafo de n1 recorrido por alfa-beta con el orden {orden_txt}. "
            + " ".join(f"{orden}º n{n}: llega con α = {fmt(a)} y β = {fmt(b)} y devuelve "
                       f"v = {fmt(v)}" + (", una cota" if n in cota else "") + "."
                       for n, (orden, _, a, b, v) in sorted(visitas.items(), key=lambda x: x[1][0]))
            + f" {corte_txt}. Nunca se generan: "
            + ", ".join(f"n{n}" + (" y lo que cuelga de él" if len(g) > 1 else "")
                        for n, g in grupos.items()) + ".")
    out = [marco(ANCHO, H, desc, titulo, desc)]
    y = encabezado(out, [f"Alfa-beta, orden {orden_txt}",
                         f"{len(visitas)} de {len(nodos)} nodos"])
    out.append(nota_svg(y + 26, ["Cada nodo: su ventana (α, β) al llegar",
                                 "y el v que devuelve"], tam=14))
    specs = {}
    for n, (orden, tipo, a, b, v) in visitas.items():
        if tipo == "final":
            specs[n] = dict(modo="tablero", renglones=None)
        else:
            specs[n] = dict(modo="tablero", renglones=(
                f"llega ({fmt(a)}, {fmt(b)})",
                f"v = {fmt(v)}" + (" (cota)" if n in cota else "")))
    for n, g in grupos.items():
        specs[n] = dict(modo="fantasma",
                        lineas=["y lo que", "cuelga de él"] if len(g) > 1 else ["no se", "genera"])
    aristas = []
    for n in list(visitas) + list(grupos):
        padre = nodos[n][2]
        if padre is None:
            continue
        tenue = n in grupos
        t = ({11: 0.75, 7: 0.6}.get(n, 0.5) if invertir
             else {6: 0.6, 13: 0.6}.get(n, 0.5))
        aristas.append((padre, n, "tenue" if tenue else "normal",
                        [(t, nodos[n][3], LINEA if tenue else SUAVE)]))
    cortes_ = [(padre, [m for m in grupos if nodos[m][2] == padre], f"corte {tipo}", "der",
                0.18)
               for (padre, _), tipo in cortes.items()]
    _dibujar_partes(out, lugares, esc, ys, specs, aristas, cortes_,
                    ordenes={n: v[0] for n, v in visitas.items()})
    ly = H - 34
    out.append(f'<circle cx="{X_PIE + 12}" cy="{ly + 8}" r="12" fill="{ACENTO}"/>')
    out.append(texto(X_PIE + 12, ly + 13, "1º", tam=12, color=FONDO, peso="700"))
    out.append(texto(X_PIE + 32, ly + 13, "orden de visita", tam=13, color=SUAVE,
                     anclaje="start"))
    out.append(caja(212, ly, 24, 16, borde=LINEA, grosor=2, radio=4, guiones="5 3"))
    out.append(texto(244, ly + 13, "no se genera", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(400, ly - 3, 30, 22, borde=COLOR_FINAL, grosor=1.5, radio=5))
    out.append(caja(403, ly, 24, 16, borde=COLOR_FINAL, grosor=1.5, radio=4))
    out.append(texto(440, ly + 13, "final, con su U", tam=13, color=SUAVE, anclaje="start"))
    out.append(cierre())
    return "".join(out)


# ------------------------------------------- alfa-beta por partes (C2) ---
#
# «Alfa-beta a mano» enseña la poda primero en arboles chicos sin tableros
# (A y B, de tools/juegos.py) y luego en n1, por partes. Cada serie conserva
# la misma geometria de un paso al siguiente para que el lector vea crecer
# el mismo dibujo: solo cambia que se genera y que va en acento. Estas figuras
# se leen en un telefono (el sitio las escala a ~350 px), asi que su letra
# minima es de 22 unidades.

T_TIT, T_TXT, T_VAL = 26, 22, 26


def _ancho_pastilla(rotulo, tam, mono=True):
    return round((0.62 if mono else 0.55) * tam * len(rotulo) + 20)


def _pastilla(cx, cy, rotulo, color, tam=T_TXT, mono=True, relleno=FONDO, color_texto=None):
    """Rotulo en una caja redondeada, centrado en (cx, cy)."""
    ancho = _ancho_pastilla(rotulo, tam, mono)
    alto = round(tam * 1.45)
    return (caja(round(cx - ancho / 2, 1), round(cy - alto / 2, 1), ancho, alto,
                 relleno=relleno, borde=color, radio=8, grosor=2)
            + texto(round(cx, 1), round(cy + tam * 0.36, 1), rotulo, tam=tam,
                    color=color_texto or color, peso="700", fuente=MONO if mono else None))


def _arista_ab(x1, ya, x2, yb, estilo="normal", pastillas=(), tam=T_TXT):
    """Arista del borde inferior del padre (ya) al superior del hijo (yb).

    estilo: 'nueva' (acento), 'normal' o 'tenue' (hacia lo que no se genera).
    pastillas: [(t, rotulo, color)], t en [0, 1] a lo largo de la arista."""
    fin = yb - 8
    if estilo == "tenue":
        s = [linea(x1, ya, x2, yb, color=LINEA, grosor=2, guiones="6 5")]
        fin = yb
    else:
        s = [flecha(x1, ya, x2, fin, color=ACENTO if estilo == "nueva" else SUAVE,
                    grosor=3 if estilo == "nueva" else 2,
                    marcador="p" if estilo == "nueva" else "s")]
    for t, rotulo, color in pastillas:
        s.append(_pastilla(x1 + (x2 - x1) * t, ya + (fin - ya) * t, rotulo, color, tam=tam))
    return "".join(s)


def _corte_ab(x_padre, ya, hijos_xy, t, rotulo, lado="der", tam=T_TXT):
    """La barra de corte: atraviesa las aristas que ya no se siguen, a la
    fraccion t de su largo, con el tipo de corte en una pastilla al lado.
    hijos_xy: [(x, y superior)] de los hijos que no se generan."""
    y = ya + (hijos_xy[0][1] - ya) * t
    xs = [x_padre + (x - x_padre) * (y - ya) / (yh - ya) for x, yh in hijos_xy]
    pad = 26 if tam >= T_TXT else 16
    x_a, x_b = min(xs) - pad, max(xs) + pad
    ancho = _ancho_pastilla(rotulo, tam, mono=False)
    cx = x_b + 8 + ancho / 2 if lado == "der" else x_a - 8 - ancho / 2
    return (linea(round(x_a, 1), round(y, 1), round(x_b, 1), round(y, 1), color=ACENTO,
                  grosor=7 if tam >= T_TXT else 5)
            + _pastilla(cx, y, rotulo, ACENTO, tam=tam, mono=False, relleno=ACENTO,
                        color_texto=FONDO))


def _notas_ab(y, renglones, tam=T_TXT):
    return "".join(texto(X_PIE, y + round(tam * 1.45) * k, r, tam=tam, anclaje="start")
                   for k, r in enumerate(renglones))


# ======================================================= el arbol T (C2) ===
#
# Un solo arbol de juguete, T, que crece en etapas (T1 y luego T). Todas las
# figuras jue-t-* y jue-t1-* dibujan un momento de j.traza_decidir: la fila
# elegida da la linea del pseudocodigo que se ejecuta (la banda de arriba),
# la pila, lo que ya devolvio cada nodo, mejor_jugada y la ventana del nodo
# activo. Ningun numero se escribe a mano. Cada numero lleva su letra
# («v = 7», «α = 3»): nunca un «= 7» suelto.
#
# Ancho: 600, como todas las figuras de la unidad (ver ANCHO). En un
# telefono de 390 px la figura se ve desde la izquierda, con desplazamiento:
# por eso el titulo, el pie y la leyenda van a la izquierda, en renglones que
# caben en los primeros ~340 px.

ANCHO_T = 600
T_FIG = 17          # letra de los rotulos de estas figuras
NODO_T_W, NODO_T_H, HOJA_T_R = 108, 70, 24
ETIQ_W = 74         # la etiqueta con α y β junto a un nodo en la pila

# x de cada nodo (por camino) y nivel. Las hojas se llaman por su camino
# porque «2» aparece dos veces en T.
# En el nivel 2 caben, de izquierda a derecha: dos hojas, C1, la etiqueta
# de C2 (va a su izquierda), C2 y dos hojas; por eso C2 queda a la derecha
# del centro.
LUGARES_T = {(): 314, (0,): 68, (1,): 286, (2,): 519, (1, 0): 190, (1, 1): 382,
             (0, 0): 36, (0, 1): 100, (1, 0, 0): 158, (1, 0, 1): 222,
             (1, 1, 0): 350, (1, 1, 1): 414, (2, 0): 486, (2, 1): 552}
LUGARES_T1 = {(): 314, (0,): 160, (1,): 460, (0, 0): 106, (0, 1): 214,
              (1, 0): 406, (1, 1): 514}
# De que lado va la etiqueta (α, β) de cada nodo interno.
LADO_ETIQ = {"I": 1, "C": 1, "D": -1, "C1": 1, "C2": -1}
GAPS_T = (150, 130, 130)


def _titulo_t(out, renglones):
    """Titulo a la izquierda: el primer renglon grande, los demas menores.
    Devuelve la y de abajo."""
    y = 34
    for k, r in enumerate(renglones):
        out.append(texto(X_PIE, y, r, tam=22 if k == 0 else 18, peso="700", anclaje="start"))
        y += 26 if k == 0 else 24
    return y - 18


def _pie_t(out, y, renglones, tam=T_FIG, peso="normal"):
    """Renglones cortos a la izquierda. y: base del primero. Devuelve la base
    del siguiente."""
    for r in renglones:
        out.append(texto(X_PIE, y, r, tam=tam, peso=peso, anclaje="start"))
        y += round(tam * 1.6)
    return y


def _svg_t(titulo, desc, H, out, sep=". "):
    """sep une los renglones del titulo en el <title>. Las figuras de la
    clase 3 usan « · »: «. » dejaba una minuscula tras el punto."""
    nombre = titulo[0] + (sep + " ".join(titulo[1:]) if len(titulo) > 1 else "")
    return "".join([marco(ANCHO_T, round(H), desc, nombre, desc)] + out
                   + [cierre()])


def _orden_caminos(arbol):
    """Caminos en preorden (el orden dado)."""
    res = [()]

    def rec(nodo, c):
        if isinstance(nodo, tuple):
            for i, h in enumerate(nodo):
                res.append(c + (i,))
                rec(h, c + (i,))
    rec(arbol, ())
    return res


def _orden_generacion(arbol, traza):
    """Caminos en el orden en que la traza los genera."""
    return list(traza["caminos_generados"])


def _fotos_por_camino(arbol, traza, k):
    """Estado por camino tras la fila k (1-based). La foto de la traza va
    por nombre, y «2» es el nombre de dos hojas: las hojas se resuelven por
    el orden de generacion."""
    fila = traza["filas"][k - 1]
    nombres = j.nombres_t(arbol)
    generados = set(_orden_generacion(arbol, traza)[:fila["generados"]])
    nunca = set(_orden_caminos(arbol)) - set(_orden_generacion(arbol, traza))
    podados = {n for f in traza["filas"][:k] for n in f["podados"]}
    res = {}
    for c, (n, _) in nombres.items():
        e = dict(fila["estado"][n])
        if not isinstance(j.nodo_en(arbol, c), tuple):
            if c in generados:
                e["estado"] = "devuelto"
            elif c in nunca and n in podados:
                e["estado"] = "podado"
            else:
                e["estado"] = "pormirar"
        res[c] = e
    return res


def _niveles(y0):
    ys = [y0]
    for g in GAPS_T:
        ys.append(ys[-1] + g)
    return ys


def _caja_nodo_t(cx, cy, nombre, tipo, e, resaltado=False, olvidar=False, color=None,
                 renglon=None):
    """Nodo interno de T. e: dict(estado, v, cota). El v va dentro; α y β,
    fuera (en la etiqueta), para que nunca compartan casilla.

    Solo un nodo en la pila lleva el borde de acento. El que acaba de
    devolver (resaltado) ya salio de la pila: lleva su propio color, mas
    grueso, y la flecha de acento que sube a su padre."""
    color = color or (COLOR_MAX if tipo == "MAX" else COLOR_MIN)
    w, h = NODO_T_W, NODO_T_H
    x, y = cx - w / 2, cy - h / 2
    estado = e["estado"]
    olvidar = olvidar and estado == "devuelto"
    if estado in ("pormirar", "podado") or olvidar:
        s = [caja(x, y, w, h, relleno=FONDO, borde=LINEA if not olvidar else SUAVE,
                  grosor=2, guiones="8 6" if not olvidar else "2 5")]
        s.append(texto(cx, cy - 8, f"{nombre} · {tipo}", tam=T_FIG, color=SUAVE, peso="700"))
        if estado == "podado":
            s.append(texto(cx, cy + 22, "?", tam=24, color=LINEA, peso="700"))
        elif olvidar:
            s.append(texto(cx, cy + 20, f"devolvió {j.fmt_t(e['v'])}", tam=16, color=SUAVE))
        elif renglon:
            s.append(texto(cx, cy + 20, renglon, tam=16, color=SUAVE))
        return "".join(s)
    en_pila = estado == "pila"
    s = [caja(x, y, w, h, relleno=mezclar(color, 0.16 if en_pila else 0.07),
              borde=ACENTO if en_pila else color,
              grosor=3.5 if (en_pila or resaltado) else 2,
              guiones="8 5" if estado == "evaluado" else None)]
    s.append(texto(cx, cy - 10, f"{nombre} · {tipo}", tam=T_FIG, color=color, peso="700"))
    if renglon is None:
        if estado == "evaluado":
            renglon = f"EVAL = {j.fmt_t(e['v'])}"
        elif e["v"] is not None:
            renglon = f"v = {j.fmt_t(e['v'])}" + (" · cota" if e.get("cota") else "")
        else:
            renglon = ""
    tam = 19 if len(renglon) < 8 else (17 if len(renglon) <= 10 else 15)
    s.append(texto(cx, cy + 20, renglon, tam=tam, peso="700"))
    return "".join(s)


def _hoja_t(cx, cy, valor, estado, resaltado=False):
    r = HOJA_T_R
    if estado == "olvidada":
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FONDO}" stroke="{SUAVE}" '
                f'stroke-width="1.5" stroke-dasharray="2 4"/>'
                + texto(cx, cy + 7, j.fmt_t(valor), tam=20, color=SUAVE))
    if estado in ("pormirar", "podado"):
        rotulo = "?" if estado == "podado" else j.fmt_t(valor)
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FONDO}" stroke="{LINEA}" '
                f'stroke-width="2" stroke-dasharray="6 5"/>'
                + texto(cx, cy + 7, rotulo, tam=20, color=LINEA if estado == "podado" else SUAVE,
                        peso="700"))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="{COLOR_FINAL}" '
            f'stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{mezclar(COLOR_FINAL, 0.16 if resaltado else 0.07)}" '
            f'stroke="{COLOR_FINAL}" stroke-width="{3.5 if resaltado else 2}"/>'
            + texto(cx, cy + 7, j.fmt_t(valor), tam=20, peso="700"))


def _etiqueta_ab(cx, cy, lado, alfa, beta, rival=None):
    """α y β de un nodo en la pila, en una etiqueta pegada a su caja.

    rival: «alfa» o «beta» si el nodo esta evaluando su if. Ese renglon, el
    numero del rival con el que compara v, va relleno de acento; el propio,
    atenuado (el lo actualiza, pero no lo compara)."""
    x = cx + lado * (NODO_T_W / 2 + 4) - (ETIQ_W if lado < 0 else 0)
    s = [caja(x, cy - 30, ETIQ_W, 60, relleno=mezclar(ACENTO, 0.12), borde=ACENTO,
              radio=6, grosor=1.5)]
    for k, (letra, valor) in enumerate((("alfa", alfa), ("beta", beta))):
        yy = cy - 14 + 28 * k
        rot = f"{'α' if letra == 'alfa' else 'β'} = {j.fmt_t(valor)}"
        color = TEXTO
        if rival == letra:
            s.append(caja(x + 4, yy - 12, ETIQ_W - 8, 25, relleno=ACENTO, borde=ACENTO,
                          radio=4, grosor=1))
            color = FONDO
        elif rival:
            color = SUAVE
        s.append(texto(x + ETIQ_W / 2, yy + 6, rot, tam=16, color=color,
                       peso="700", fuente=MONO))
    return "".join(s)


def _pastilla_t(cx, cy, rotulo, color, tam=15, relleno=FONDO, color_texto=None, mono=True):
    ancho = _ancho_pastilla(rotulo, tam, mono)
    return (caja(round(cx - ancho / 2, 1), round(cy - 13, 1), ancho, 26, relleno=relleno,
                 borde=color, radio=7, grosor=1.5)
            + texto(round(cx, 1), round(cy + 5, 1), rotulo, tam=tam, color=color_texto or color,
                    peso="700", fuente=MONO if mono else None))


def _recuadro_t(out, x_raiz, y_raiz, renglones):
    """El recuadro de DECIDIR (mejor_jugada y su valor), a la izquierda de R,
    un renglon por variable."""
    ancho = max(_ancho_pastilla(r, 16) for r in renglones) + 4
    alto = 26 * len(renglones) + 12
    x = X_PIE - 4
    assert x + ancho < x_raiz - NODO_T_W / 2 - 8, renglones
    out.append(caja(x, y_raiz - alto / 2, ancho, alto, relleno=FONDO, borde=TEXTO, radio=6,
                    grosor=1.5))
    for k, r in enumerate(renglones):
        out.append(texto(x + 12, y_raiz - alto / 2 + 25 + 26 * k, r, tam=16, peso="700",
                         fuente=MONO, anclaje="start"))


def dibujar_t(out, arbol, estados, y0, resaltar=(), etiquetas=None, olvidar=False,
              cortes=(), tipos=None, rotulos_arista=None, renglones=None, ocultar=(),
              lugares=None, rotulos_tenues=True, recuadro=None, rival=None):
    """Dibuja T o T1 con raiz en y0.

    estados: {camino: dict(estado, v, cota)}; resaltar: caminos que acaban
    de devolver (flecha de acento hacia su padre); etiquetas: {camino:
    (alfa, beta)}; rival: {camino: «alfa»|«beta»}, el numero que ese nodo
    compara en su if; cortes: [(camino del nodo que corta, tipo)]; tipos:
    {camino: tipo} para otro tipo de nodo (azar); rotulos_arista: {camino
    del hijo: rotulo} extra; renglones: {camino: texto del segundo renglon};
    ocultar: caminos que no se dibujan; recuadro: renglones del recuadro de
    DECIDIR, junto a R."""
    lugares = lugares or (LUGARES_T if len(arbol) == 3 else LUGARES_T1)
    nombres = j.nombres_t(arbol)
    ys = _niveles(y0)
    tipos = tipos or {}
    renglones = renglones or {}
    rotulos_arista = rotulos_arista or {}
    rival = rival or {}

    def pos(c):
        return lugares[c], ys[len(c)]

    def es_hoja(c):
        return not isinstance(j.nodo_en(arbol, c), tuple)

    def medio_alto(c):
        return HOJA_T_R if es_hoja(c) else NODO_T_H / 2

    caminos = [c for c in _orden_caminos(arbol) if c not in ocultar]
    # Aristas.
    for c in caminos:
        if c == ():
            continue
        p = c[:-1]
        (x1, y1), (x2, y2) = pos(p), pos(c)
        ya, yb = y1 + NODO_T_H / 2, y2 - medio_alto(c) - (4 if es_hoja(c) else 0)
        e = estados[c]
        if olvidar and e["estado"] == "devuelto" and c not in resaltar:
            out.append(linea(x1, ya, x2, yb, color=SUAVE, grosor=1.5, guiones="2 4"))
            color = SUAVE
        elif e["estado"] in ("pormirar", "podado"):
            out.append(linea(x1, ya, x2, yb, color=LINEA, grosor=2, guiones="6 5"))
            color = LINEA
        elif c in resaltar and e["estado"] != "pila":
            # Acaba de devolver: la flecha sube, del hijo al padre.
            out.append(flecha(x2, yb, x1, ya + 6, color=ACENTO, grosor=3, marcador="p"))
            color = ACENTO
        else:
            activo = e["estado"] == "pila"
            out.append(flecha(x1, ya, x2, yb - 6, color=ACENTO if activo else SUAVE,
                              grosor=3 if activo else 2, marcador="p" if activo else "s"))
            color = ACENTO if activo else SUAVE
        rot = rotulos_arista.get(c, nombres[c][1])
        if not rotulos_tenues and e["estado"] in ("pormirar", "podado"):
            rot = None
        if rot:
            t = 0.42
            if rot == "½":
                # Las dos aristas de I (y de D) nacen juntas: a la altura del
                # rotulo cada «½» se corre hacia afuera de su arista, para
                # que no se encimen ni la tapen.
                t = 0.45
                dx = (-22 if c[-1] == 0 else 22) if es_hoja(c) else 0
                out.append(_pastilla_t(x1 + (x2 - x1) * t + dx, ya + (yb - ya) * t, rot, color,
                                       tam=19, mono=False))
            else:
                out.append(_pastilla_t(x1 + (x2 - x1) * t, ya + (yb - ya) * t, rot, color))
    # Cortes: una barra sobre cada arista que ya no se sigue.
    for c, tipo in cortes:
        x1, y1 = pos(c)
        fuera = [h for h in caminos if h[:-1] == c and estados[h]["estado"] == "podado"]
        for h in fuera:
            x2, y2 = pos(h)
            ya, yb = y1 + NODO_T_H / 2, y2 - medio_alto(h)
            mx, my = x1 + (x2 - x1) * 0.55, ya + (yb - ya) * 0.55
            out.append(linea(mx - 22, my, mx + 22, my, color=ACENTO, grosor=6))
        xs = [pos(h)[0] for h in fuera]
        yb = max(pos(h)[1] for h in fuera) + HOJA_T_R + 26
        rot = f"corte {tipo}"
        ancho = _ancho_pastilla(rot, 16, mono=False)
        cx = min(max(sum(xs) / len(xs), ancho / 2 + 8), ANCHO_T - ancho / 2 - 8)
        out.append(_pastilla_t(cx, yb, rot, ACENTO, tam=16, relleno=ACENTO, color_texto=FONDO,
                               mono=False))
    # Nodos.
    for c in caminos:
        x, y = pos(c)
        e = estados[c]
        if es_hoja(c):
            est = ("olvidada" if (olvidar and e["estado"] == "devuelto" and c not in resaltar)
                   else e["estado"])
            out.append(_hoja_t(x, y, j.nodo_en(arbol, c), est, c in resaltar))
            continue
        tipo = tipos.get(c, "MAX" if len(c) % 2 == 0 else "MIN")
        color = COLOR_AZAR if tipo == "azar" else None
        out.append(_caja_nodo_t(x, y, nombres[c][0], tipo, e, c in resaltar,
                                olvidar=olvidar, color=color, renglon=renglones.get(c)))
    for c, (alfa, beta) in (etiquetas or {}).items():
        x, y = pos(c)
        out.append(_etiqueta_ab(x, y, LADO_ETIQ[nombres[c][0]], alfa, beta, rival.get(c)))
    if recuadro:
        _recuadro_t(out, *pos(()), recuadro)
    return max(ys[len(c)] for c in caminos)


def _lineas_banda(fila, poda):
    ev = fila["evento"]
    if ev == "inicio":
        return [1, 2]
    if ev == "raiz":
        return [4, 5]
    if ev == "fin":
        return [6]
    es_max = len(fila["pila"]) % 2 == 1
    if not poda:
        if ev == "entra":
            return [7, 10] if es_max else [7, 16]
        return [12, 13] if es_max else [18, 19]
    if ev == "entra":
        return [7, 10] if es_max else [7, 18]
    if es_max:
        return [12, 13, 14] if fila["corta"] else [13, 14, 15]
    return [20, 21, 22] if fila["corta"] else [21, 22, 23]


def _banda(out, y, numeros, poda, alto_lineas):
    pseudo = j.PSEUDO_ALFA_BETA if poda else j.PSEUDO_MINIMAX
    alto = alto_lineas * 25 + 14
    out.append(caja(12, y, ANCHO_T - 24, alto, relleno=mezclar(ACENTO, 0.1), borde=ACENTO,
                    radio=8, grosor=1.5))
    for k, n in enumerate(numeros):
        yy = y + 25 + 25 * k
        out.append(texto(40, yy, str(n), tam=16, color=ACENTO, peso="700", anclaje="end",
                         fuente=MONO))
        out.append(texto(50, yy, pseudo[n], tam=16, color=TEXTO, anclaje="start", fuente=MONO))
    return y + alto


def _info(out, y, izquierda):
    """Renglon bajo la banda: que acaba de pasar."""
    out.append(texto(X_PIE, y + 22, izquierda, tam=T_FIG, color=ACENTO, peso="700",
                     anclaje="start"))
    return y + 30


def _que_paso(fila, poda):
    ev = fila["evento"]
    if ev == "inicio":
        return "empieza DECIDIR en R"
    if ev == "fin":
        return f"DECIDIR devuelve {fila['mejor_jugada']}"
    if ev == "entra":
        return f"entra en {fila['nodo']}"
    hijo = fila["hijo"]
    quien = f"la hoja {hijo}" if hijo.isdigit() else hijo
    return f"{quien} devuelve w = {j.fmt_t(fila['w'])}"


def _recuadro_lineas(fila, poda):
    jugada = fila["mejor_jugada"] or "ninguna"
    letra = "α" if poda else "mejor_valor"
    return [f"mejor_jugada = {jugada}", f"{letra} = {j.fmt_t(fila['mejor_valor'])}"]


def _recuadro(fila, poda):
    return " · ".join(_recuadro_lineas(fila, poda))


# La recta numerica de la ventana: 0..12 entre dos colas para ±∞.
RX0, RX1 = 92, 500


def _x_recta(v):
    if v == float("inf"):
        return ANCHO_T - 44
    if v == -float("inf"):
        return 44
    return RX0 + (RX1 - RX0) * v / 12


def _recta(out, y, titulo, alfa, beta, punto_v, letra_punto, veredicto, rival=None):
    """La ventana del nodo activo. y: base del titulo. rival: «alfa» o «beta»
    si el nodo evalua su if; entonces se dice cual numero compara (el del
    rival) y cual es suyo. Devuelve la y de abajo."""
    out.append(texto(X_PIE, y, titulo, tam=16, color=SUAVE, anclaje="start"))
    if veredicto:
        out.append(texto(X_PIE, y + 24, veredicto, tam=16, color=ACENTO, peso="700",
                         anclaje="start"))
    y = y + 24 + 52
    xa, xb = _x_recta(alfa), _x_recta(beta)
    out.append(linea(30, y, ANCHO_T - 30, y, color=SUAVE, grosor=2))
    out.append(caja(round(xa, 1), y - 10, round(xb - xa, 1), 20, relleno=mezclar(ACENTO, 0.3),
                    borde=ACENTO, radio=4, grosor=1.5))
    for v in range(0, 13):
        x = round(_x_recta(v), 1)
        out.append(linea(x, y - 5, x, y + 5, color=SUAVE, grosor=1.5))
        if v % 2 == 0:
            out.append(texto(x, y + 24, str(v), tam=15, color=SUAVE))
    out.append(texto(_x_recta(-float("inf")), y + 24, "−∞", tam=15, color=SUAVE))
    out.append(texto(_x_recta(float("inf")), y + 24, "+∞", tam=15, color=SUAVE))
    # α y β debajo, cada uno con su letra.
    sa, sb = f"α = {j.fmt_t(alfa)}", f"β = {j.fmt_t(beta)}"
    xa_t, xb_t = xa, xb
    if xb_t - xa_t < 90:
        xa_t, xb_t = (xa + xb) / 2 - 45, (xa + xb) / 2 + 45
    ca = ACENTO if rival != "beta" else SUAVE
    cb = ACENTO if rival != "alfa" else SUAVE
    out.append(texto(round(xa_t, 1), y + 50, sa, tam=16, color=ca, peso="700"))
    out.append(texto(round(xb_t, 1), y + 50, sb, tam=16, color=cb, peso="700"))
    if punto_v is not None:
        x = round(_x_recta(punto_v), 1)
        out.append(punto(x, y, r=8, color=TEXTO))
        out.append(texto(x, y - 16, f"{letra_punto} = {j.fmt_t(punto_v)}", tam=16, peso="700"))
    y += 50
    if rival:
        rv, pr = (sa, sb) if rival == "alfa" else (sb, sa)
        de = "MAX" if rival == "alfa" else "MIN"
        y += 30
        out.append(texto(X_PIE, y, f"{rv} ← de {de}: se compara", tam=16, color=ACENTO,
                         peso="700", anclaje="start"))
        y += 24
        out.append(texto(X_PIE, y, f"{pr} · suyo: no se compara", tam=16, color=SUAVE,
                         anclaje="start"))
    return y


def _veredicto(fila, antes=None):
    """antes: mejor_valor (α de R) antes de la fila, para las filas de R."""
    ev = fila["evento"]
    v, w, a, b = fila["v"], fila["w"], fila["alfa"], fila["beta"]
    f = j.fmt_t
    if ev == "raiz":
        if fila["mejora"]:
            return f"w = {f(w)} > α = {f(antes)}: α ← {f(w)}"
        return f"w = {f(w)} > α = {f(fila['mejor_valor'])} es falso"
    if ev == "entra":
        return f"{fila['nodo']} llega con ({f(a)}, {f(b)})"
    if ev != "regresa":
        return ""
    es_max = len(fila["pila"]) % 2 == 1
    if fila["corta"]:
        return (f"v = {f(v)} ≥ β = {f(b)}: corte beta" if es_max
                else f"v = {f(v)} ≤ α = {f(a)}: corte alfa")
    return (f"v = {f(v)} ≥ β = {f(b)} es falso: α ← {f(a)}" if es_max
            else f"v = {f(v)} ≤ α = {f(a)} es falso: β ← {f(b)}")


def _rival(fila):
    """El numero del rival que compara el nodo activo en su if (o None)."""
    if fila["evento"] != "regresa" or fila["nodo"] == "R":
        return None
    return "beta" if len(fila["pila"]) % 2 == 1 else "alfa"


def _leyenda_t(out, y, poda, devolvio=False, items=None):
    """Leyenda en dos columnas a la izquierda. Devuelve la y de abajo.
    items: [(tipo, rotulo)] en vez de los de la traza (clase 3)."""
    if items is None:
        items = [("pila", "en la pila"), ("devuelto", "ya devolvió")]
        if devolvio:
            items.append(("sube", "acaba de devolver"))
        items.append(("pormirar", "por mirar"))
        if poda:
            items.append(("podado", "no se genera"))
    for k, (tipo, rot) in enumerate(items):
        x, yy = 16 + (k % 2) * 200, y + (k // 2) * 30
        if tipo == "pila":
            out.append(caja(x, yy, 30, 20, relleno=mezclar(COLOR_MIN, 0.16), borde=ACENTO,
                            grosor=3, radio=4))
        elif tipo == "devuelto":
            out.append(caja(x, yy, 30, 20, relleno=mezclar(COLOR_MIN, 0.07), borde=COLOR_MIN,
                            radio=4))
        elif tipo == "sube":
            out.append(flecha(x + 15, yy + 20, x + 15, yy + 2, color=ACENTO, grosor=3,
                              marcador="p"))
        elif tipo == "pormirar":
            out.append(caja(x, yy, 30, 20, borde=LINEA, guiones="5 4", radio=4))
        elif tipo.startswith("corte"):
            # Nodo de corte de la clase 3: recibe EVAL. «corte_MIN» o «corte_MAX»
            # da el color del nivel donde corta la figura.
            color = COLOR_MIN if tipo == "corte_MIN" else COLOR_MAX
            out.append(caja(x, yy, 30, 20, relleno=mezclar(color, 0.07), borde=color,
                            guiones="5 4", radio=4))
        else:
            out.append(f'<circle cx="{x + 14}" cy="{yy + 10}" r="11" fill="{FONDO}" '
                       f'stroke="{LINEA}" stroke-width="2" stroke-dasharray="4 3"/>')
            out.append(texto(x + 14, yy + 16, "?", tam=15, color=LINEA, peso="700"))
        out.append(texto(x + 40, yy + 16, rot, tam=15, color=SUAVE, anclaje="start"))
    return y + 30 * ((len(items) + 1) // 2)


def figura_traza_t(arbol, poda, k, titulo, desc, notas=(), alto_banda=None):
    """Un cuadro de la traza: la fila k de traza_decidir(arbol, poda)."""
    traza = j.traza_decidir(arbol, poda=poda)
    fila = traza["filas"][k - 1]
    estados = _fotos_por_camino(arbol, traza, k)
    out = []
    y = _titulo_t(out, titulo) + 14
    y = _banda(out, y, _lineas_banda(fila, poda), poda, alto_banda or (3 if poda else 2))
    y = _info(out, y + 8, _que_paso(fila, poda))
    # Lo que acaba de devolver (para resaltarlo) y las etiquetas de la pila.
    nombres = j.nombres_t(arbol)
    camino_de = {}
    for c in _orden_generacion(arbol, traza)[:fila["generados"]]:
        camino_de[nombres[c][0]] = c
    resaltar = []
    if fila["hijo"]:
        resaltar.append(camino_de[fila["hijo"]])
    etiquetas = {}
    if poda:
        for c, e in estados.items():
            if e["estado"] == "pila" and c != ():
                etiquetas[c] = (e["alfa"], e["beta"])
    if fila["corta"]:
        # El cuadro del corte se dibuja en el instante de la prueba: el nodo
        # sigue en la pila, con su v y la ventana con que llego.
        c = camino_de[fila["nodo"]]
        estados[c].update(estado="pila", v=fila["v"], alfa=fila["alfa"], beta=fila["beta"])
        etiquetas[c] = (fila["alfa"], fila["beta"])
    rival = {}
    if poda and _rival(fila):
        rival[camino_de[fila["nodo"]]] = _rival(fila)
    cortes = []
    hechos = [f for f in traza["filas"][:k] if f["corta"] and f["podados"]]
    for f in hechos:
        cortes.append((camino_de[f["nodo"]], f["corta"]))
    y0 = y + 30 + NODO_T_H / 2
    fondo = dibujar_t(out, arbol, estados, y0, resaltar, etiquetas, cortes=cortes,
                      renglones={(): "DECIDIR"}, recuadro=_recuadro_lineas(fila, poda),
                      rival=rival)
    y = fondo + HOJA_T_R + (60 if cortes else 30)
    if poda:
        y += 26
        activo = fila["nodo"]
        a, b = fila["alfa"], fila["beta"]
        if activo == "R":
            tit = "La ventana de R: (α, +∞)"
            pv, letra = fila["w"], "w"
        else:
            tit = f"La ventana de {activo}, el nodo activo"
            pv, letra = (fila["v"], "v") if fila["evento"] == "regresa" else (None, "v")
        antes = traza["filas"][k - 2]["mejor_valor"] if k > 1 else None
        y = _recta(out, y, tit, a, b, pv, letra, _veredicto(fila, antes), _rival(fila)) + 16
    y = _pie_t(out, y + 20, notas)
    y = _leyenda_t(out, y - 4, poda, devolvio=bool(resaltar))
    return _svg_t(titulo, desc, y + 4, out)


def _desc_estado(arbol, traza, k):
    """Una frase por nodo: lo que se ve en el cuadro k (para aria-label)."""
    est = _fotos_por_camino(arbol, traza, k)
    nombres = j.nombres_t(arbol)
    partes = []
    for c in _orden_caminos(arbol):
        e, n = est[c], nombres[c][0]
        hoja = not isinstance(j.nodo_en(arbol, c), tuple)
        if hoja:
            if e["estado"] == "podado":
                partes.append(f"la hoja {n} no se genera")
            continue
        if e["estado"] == "pila":
            extra = (f", α = {j.fmt_t(e['alfa'])}, β = {j.fmt_t(e['beta'])}"
                     if e["alfa"] is not None else "")
            vv = f" con v = {j.fmt_t(e['v'])}" if n != "R" else ""
            partes.append(f"{n} en la pila{vv}{extra}")
        elif e["estado"] == "devuelto" and n != "R":
            partes.append(f"{n} ya devolvió v = {j.fmt_t(e['v'])}"
                          + (" (una cota)" if e["cota"] else ""))
        elif e["estado"] == "pormirar":
            partes.append(f"{n} por mirar")
    return "; ".join(partes)


def _desc_t(arbol, poda, k, inicio):
    traza = j.traza_decidir(arbol, poda=poda)
    fila = traza["filas"][k - 1]
    pseudo = j.PSEUDO_ALFA_BETA if poda else j.PSEUDO_MINIMAX
    lineas = "; ".join(f"línea {n}: {pseudo[n]}" for n in _lineas_banda(fila, poda))
    antes = traza["filas"][k - 2]["mejor_valor"] if k > 1 else None
    rival = ""
    if poda and _rival(fila):
        r, p = ("α", "β") if _rival(fila) == "alfa" else ("β", "α")
        rival = (f" {fila['nodo']} compara su v con {r}, el número del rival que heredó; "
                 f"{p} es el suyo.")
    # En la fila final no hay comparacion que contar: la recta solo muestra
    # la ventana de R.
    recta = _veredicto(fila, antes) or (
        f"la ventana de R, ({j.fmt_t(fila['alfa'])}, {j.fmt_t(fila['beta'])})")
    return (f"{inicio} Arriba, la banda del pseudocódigo: {lineas}. "
            f"{_que_paso(fila, poda).capitalize()}. Recuadro: {_recuadro(fila, poda)}. "
            f"En el árbol: {_desc_estado(arbol, traza, k)}."
            + (f" Abajo, la recta numérica: {recta}." if poda else "")
            + rival)


# ------------------------------------------------------------- el problema --

PIE_T_ARBOL = ["Cada hoja es un final:", "su número es lo que vale ese final."]


def jue_t_arbol():
    """El arbol T sin valores internos: el enunciado."""
    arbol = j.ARBOL_T
    titulo = ["El árbol T"]
    hojas = [j.fmt_t(j.nodo_en(arbol, c)) for c in _orden_caminos(arbol)
             if not isinstance(j.nodo_en(arbol, c), tuple)]
    desc = ("El árbol T, sin valores en los nodos internos. La raíz R es de MAX y tiene tres "
            "jugadas: izq lleva a I, centro a C y der a D, los tres de MIN. I tiene las hojas 3 "
            "y 6. C tiene dos hijos de MAX: C1, por c1, con las hojas 5 y 2, y C2, por c2, con "
            "las hojas 7 y 8. D tiene las hojas 2 y 12. Las hojas, de izquierda a derecha: "
            + ", ".join(hojas) + ". En total, 14 nodos. " + " ".join(PIE_T_ARBOL))
    out = []
    y = _titulo_t(out, titulo)
    estados = {c: dict(estado="devuelto", v=None, cota=False) for c in _orden_caminos(arbol)}
    fondo = dibujar_t(out, arbol, estados, y + 30 + NODO_T_H / 2,
                      renglones={c: "v = ?" for c in estados if c != ()} | {(): "DECIDIR"})
    y = _pie_t(out, fondo + HOJA_T_R + 40, PIE_T_ARBOL)
    return _svg_t(titulo, desc, y - 10, out)


# ------------------------------------------------------- minimax en T ---

def _fila_minimax(pred):
    t = j.traza_decidir(j.ARBOL_T)
    return next(f["n"] for f in t["filas"] if pred(f))


def _pasos_minimax_t():
    """{paso: (fila, titulo en renglones, inicio de la descripcion, notas)}."""
    p1 = _fila_minimax(lambda f: f["evento"] == "raiz" and f["hijo"] == "I")
    p2 = _fila_minimax(lambda f: f["pila"] == ("R", "C", "C2") and f["w"] == 7)
    p3 = _fila_minimax(lambda f: f["evento"] == "raiz" and f["hijo"] == "C")
    p4 = _fila_minimax(lambda f: f["evento"] == "raiz" and f["hijo"] == "D")
    return {
        1: (p1, ["Minimax en T · paso 1", "I devuelve 3:", "mejor_jugada = izq"],
            "DECIDIR-MINIMAX sobre el árbol T, paso 1 (fila %d de la traza)." % p1,
            ["Primera jugada de R:", "izq vale 3, y 3 > −∞."]),
        2: (p2, ["Minimax en T · paso 2", "A media ejecución: R›C›C2"],
            "DECIDIR-MINIMAX sobre el árbol T, paso 2 (fila %d de la traza): a media "
            "ejecución, con la pila R, C, C2." % p2,
            ["En la pila, solo el camino R, C, C2.", "C1 ya devolvió 5: su llamada",
             "terminó; en C solo queda su v = 5."]),
        3: (p3, ["Minimax en T · paso 3", "C devuelve 5:", "mejor_jugada = centro"],
            "DECIDIR-MINIMAX sobre el árbol T, paso 3 (fila %d de la traza)." % p3,
            ["centro vale 5, y 5 > 3:", "R cambia de jugada."]),
        4: (p4, ["Minimax en T · paso 4", "D devuelve 2: 2 > 5 es falso"],
            "DECIDIR-MINIMAX sobre el árbol T, paso 4 (fila %d de la traza), el último "
            "antes de devolver la jugada." % p4,
            ["der vale 2, y 2 > 5 es falso:", "mejor_jugada sigue en centro.",
             "DECIDIR-MINIMAX devuelve centro", "(línea 6). Se generaron 14 nodos."]),
    }


PASOS_MINIMAX_T = (1, 2, 3, 4)


def jue_t_minimax(paso):
    k, titulo, inicio, notas = _pasos_minimax_t()[paso]
    desc = _desc_t(j.ARBOL_T, False, k, inicio) + " " + " ".join(notas)
    return figura_traza_t(j.ARBOL_T, False, k, titulo, desc, notas)


# ------------------------------------------------------- alfa-beta en T ---

def _fila_ab(arbol, pred):
    t = j.traza_decidir(arbol, poda=True)
    return next(f["n"] for f in t["filas"] if pred(f))


def fila_pagina(arbol, k):
    """El numero con que la pagina llama a la fila k de la traza de poda.

    traza_decidir no tiene filas para lo que no se genera; las tablas de la
    pagina si: una fila ✗ por hoja podada, justo despues de la fila que
    corta, para que cada fila lleve el mismo numero que en la traza de
    minimax. La fila k corre tantos lugares como hojas se podaron antes."""
    filas = j.traza_decidir(arbol, poda=True)["filas"]
    return k + sum(len(f["podados"]) for f in filas[:k - 1])


def _pasos_ab_t1():
    t = j.traza_decidir(j.ARBOL_T1, poda=True)
    p1 = _fila_ab(j.ARBOL_T1, lambda f: f["evento"] == "raiz" and f["hijo"] == "I")
    p2 = _fila_ab(j.ARBOL_T1, lambda f: f["corta"] == "alfa")
    p3 = len(t["filas"])
    n, total = t["generados"], j.contar_nodos(j.ARBOL_T1)
    fp = {p: fila_pagina(j.ARBOL_T1, p) for p in (p1, p2, p3)}
    return {
        1: (p1, ["Alfa-beta en T1 · paso 1", "I devuelve 3: α = 3"],
            f"DECIDIR-ALFA-BETA sobre la etapa 1 del árbol T, paso 1 (fila {fp[p1]} de la traza).",
            ["R ya tiene asegurado 3:", "a D le pasa α = 3."]),
        2: (p2, ["Alfa-beta en T1 · paso 2", "Corte alfa en D"],
            f"DECIDIR-ALFA-BETA sobre la etapa 1 del árbol T, paso 2 (fila {fp[p2]} de la traza).",
            ["D valdrá a lo más 2, y R ya tiene 3:", "la hoja 12 no se genera."]),
        3: (p3, ["Alfa-beta en T1 · paso 3", f"{n} de {total} nodos, juega izq"],
            f"DECIDIR-ALFA-BETA sobre la etapa 1 del árbol T, paso 3: el final (fila {fp[p3]}).",
            ["D devolvió 2, una cota;", "2 > 3 es falso.", f"Se generaron {n} de {total} nodos."]),
    }


def _pasos_ab_t():
    t = j.traza_decidir(j.ARBOL_T, poda=True)
    p1 = _fila_ab(j.ARBOL_T, lambda f: f["evento"] == "raiz" and f["hijo"] == "I")
    p2 = _fila_ab(j.ARBOL_T, lambda f: f["nodo"] == "C" and f["hijo"] == "C1")
    p3 = _fila_ab(j.ARBOL_T, lambda f: f["corta"] == "beta")
    p4 = _fila_ab(j.ARBOL_T, lambda f: f["corta"] == "alfa")
    p5 = len(t["filas"])
    n, total = t["generados"], j.contar_nodos(j.ARBOL_T)
    exacto_c2 = j.minimax_arbol(j.ARBOL_T[1][1])
    fp = {p: fila_pagina(j.ARBOL_T, p) for p in (p1, p2, p3, p4, p5)}
    return {
        1: (p1, ["Alfa-beta en T · paso 1", "I devuelve 3: α = 3"],
            f"DECIDIR-ALFA-BETA sobre el árbol T, paso 1 (fila {fp[p1]} de la traza).",
            ["R ya tiene asegurado 3:", "a C le pasa α = 3."]),
        2: (p2, ["Alfa-beta en T · paso 2", "C1 devuelve 5: en C, β = 5"],
            f"DECIDIR-ALFA-BETA sobre el árbol T, paso 2 (fila {fp[p2]} de la traza).",
            ["C1 subió su α a 5, pero ese α se", "perdió al regresar: a C le llegó",
             "w = 5, y C actualiza su β."]),
        3: (p3, ["Alfa-beta en T · paso 3", "Corte beta en C2"],
            f"DECIDIR-ALFA-BETA sobre el árbol T, paso 3 (fila {fp[p3]} de la traza).",
            ["C2 devuelve 7: una cota", f"(su valor exacto es {exacto_c2}).",
             "A C le basta: con 7 ≥ 5,", "C no cambia su 5."]),
        4: (p4, ["Alfa-beta en T · paso 4", "Corte alfa en D"],
            f"DECIDIR-ALFA-BETA sobre el árbol T, paso 4 (fila {fp[p4]} de la traza).",
            ["D valdrá a lo más 2, y R ya tiene 5:", "la hoja 12 no se genera."]),
        5: (p5, ["Alfa-beta en T · paso 5", f"{n} de {total} nodos, juega centro"],
            f"DECIDIR-ALFA-BETA sobre el árbol T, paso 5: el final (fila {fp[p5]}).",
            ["Dos cortes, dos hojas sin generar:", f"{n} de {total} nodos. La misma",
             "jugada que minimax: centro."]),
    }


PASOS_AB_T1 = (1, 2, 3)
PASOS_AB_T = (1, 2, 3, 4, 5)


def jue_t1_ab(paso):
    k, titulo, inicio, notas = _pasos_ab_t1()[paso]
    desc = _desc_t(j.ARBOL_T1, True, k, inicio) + " " + " ".join(notas)
    return figura_traza_t(j.ARBOL_T1, True, k, titulo, desc, notas)


def jue_t_ab(paso):
    k, titulo, inicio, notas = _pasos_ab_t()[paso]
    desc = _desc_t(j.ARBOL_T, True, k, inicio) + " " + " ".join(notas)
    return figura_traza_t(j.ARBOL_T, True, k, titulo, desc, notas)


# ---------------------------------------- alfa-beta a media ejecucion ---

def jue_t_ab_pila():
    """Lo que ALFA-BETA tiene en memoria en el instante del corte beta en C2:
    tres marcos (R, C, C2), cada uno con sus α, β y v. I y C1 ya regresaron
    y sus marcos no existen: el α = 5 de C1 se perdio."""
    arbol = j.ARBOL_T
    traza = j.traza_decidir(arbol, poda=True)
    k = next(f["n"] for f in traza["filas"] if f["corta"] == "beta")
    fila = traza["filas"][k - 1]
    assert fila["pila"] == ("R", "C", "C2")
    estados = _fotos_por_camino(arbol, traza, k)
    # El instante de la prueba: C2 sigue en la pila.
    estados[(1, 1)].update(estado="pila", v=fila["v"], alfa=fila["alfa"], beta=fila["beta"])
    alfa_c1 = [f["alfa"] for f in traza["filas"][:k] if f["nodo"] == "C1"][-1]
    v_i = estados[(0,)]["v"]
    v_c1 = estados[(1, 0)]["v"]
    e_c, e_c2 = estados[(1,)], estados[(1, 1)]
    f = j.fmt_t
    titulo = ["ALFA-BETA en T", "a media ejecución: pila R›C›C2"]
    desc = (f"El árbol T a media ejecución de DECIDIR-ALFA-BETA (fila {fila_pagina(arbol, k)} "
            "de la traza): el "
            f"instante del corte beta en C2. En el árbol, resaltado, el camino R, C, C2. I y C1 "
            f"aparecen tenues, con «devolvió {f(v_i)}» y «devolvió {f(v_c1)}»: ya regresaron "
            f"y se olvidaron. La hoja {f(fila['w'])} acaba de devolver w = {f(fila['w'])}; la "
            "hoja 8 es un círculo punteado con «?»: no se generará. D y sus hojas siguen por "
            "mirar. C2 compara su v con β, el número del rival; su α es el suyo. Abajo, la "
            "pila de llamadas, tres marcos: R, con α = "
            f"{f(fila['mejor_valor'])} y mejor_jugada = {fila['mejor_jugada']}, va en centro; "
            f"C, con α = {f(e_c['alfa'])}, β = {f(e_c['beta'])} y v = {f(e_c['v'])}, va en c2; "
            f"C2, con α = {f(e_c2['alfa'])}, β = {f(e_c2['beta'])} y v = {f(e_c2['v'])}: "
            f"v ≥ β, corta. El α = {f(alfa_c1)} que C1 alcanzó se perdió al regresar: "
            f"a C le llegó w = {f(v_c1)}.")
    out = []
    y = _titulo_t(out, titulo) + 14
    y = _banda(out, y, _lineas_banda(fila, True), True, 3)
    y = _info(out, y + 8, _que_paso(fila, True))
    etiquetas = {(1,): (e_c["alfa"], e_c["beta"]), (1, 1): (e_c2["alfa"], e_c2["beta"])}
    y0 = y + 30 + NODO_T_H / 2
    fondo = dibujar_t(out, arbol, estados, y0, resaltar=[(1, 1, 0)], etiquetas=etiquetas,
                      olvidar=True, renglones={(): "DECIDIR"}, cortes=[((1, 1), "beta")],
                      recuadro=_recuadro_lineas(fila, True), rival={(1, 1): "beta"})
    y = fondo + HOJA_T_R + 76
    out.append(texto(X_PIE, y, "La pila: lo único en memoria", tam=18, peso="700",
                     anclaje="start"))
    marcos = [
        ("R · DECIDIR", [f"α = {f(fila['mejor_valor'])}", f"mejor_jugada = {fila['mejor_jugada']}",
                         "va en: centro"]),
        ("C · MIN", [f"α = {f(e_c['alfa'])}", f"β = {f(e_c['beta'])}", f"v = {f(e_c['v'])}",
                     "va en: c2"]),
        ("C2 · MAX", [f"α = {f(e_c2['alfa'])}", f"β = {f(e_c2['beta'])}", f"v = {f(e_c2['v'])}",
                      "v ≥ β: corta"]),
    ]
    # El de R es mas ancho: lleva «mejor_jugada = izq».
    anchos, gap, y1 = (200, 168, 168), 20, y + 20
    alto = 46 + 26 * 4
    for i, (cab, filas_) in enumerate(marcos):
        mw = anchos[i]
        x = 12 + sum(anchos[:i]) + i * gap
        out.append(caja(x, y1, mw, alto, relleno=mezclar(ACENTO, 0.08), borde=ACENTO,
                        grosor=2.5 if i == 2 else 1.5, radio=8))
        out.append(texto(x + mw / 2, y1 + 26, cab, tam=T_FIG, peso="700"))
        for r, renglon in enumerate(filas_):
            out.append(texto(x + 10, y1 + 56 + 26 * r, renglon, tam=15, fuente=MONO,
                             anclaje="start"))
        if i:
            out.append(flecha(x - gap + 1, y1 + alto / 2, x - 2, y1 + alto / 2, color=ACENTO,
                              marcador="p"))
    y = _pie_t(out, y1 + alto + 34, [
        "I y C1 ya regresaron:", "sus marcos ya no existen.",
        f"C1 había subido su α a {f(alfa_c1)};", "se perdió al regresar.",
        f"A C le llegó w = {f(v_c1)},", f"y con él C puso β = {f(e_c['beta'])}."])
    return _svg_t(titulo, desc, y - 12, out)


# ------------------------------------------------------------ azar en T ---

def jue_t_azar():
    """T con I, C y D como volados parejos: el valor esperado elige der."""
    arbol = j.ARBOL_T
    jugada, valores, generados = j.expectiminimax_t(arbol)
    nombres = j.nombres_t(arbol)
    f = j.fmt_t
    azar = {(0,), (1,), (2,)}
    estados = {c: dict(estado="devuelto", v=valores[n], cota=False)
               for c, (n, _) in nombres.items()}
    estados[()]["estado"] = "devuelto"
    medio = "½"
    rotulos = {c: medio for c in nombres if len(c) == 2}
    titulo = ["T con azar", f"juega {jugada}"]
    formulas = []
    for c in sorted(azar):
        hs = [valores[nombres[c + (i,)][0]] if isinstance(j.nodo_en(arbol, c + (i,)), tuple)
              else j.F(j.nodo_en(arbol, c + (i,))) for i in range(len(j.nodo_en(arbol, c)))]
        formulas.append(f"v({nombres[c][0]}) = ½·{f(hs[0])} + ½·{f(hs[1])} = {f(valores[nombres[c][0]])}")
    desc = ("El árbol T con I, C y D como nodos de azar: cada uno es un volado parejo, y cada "
            "rama tiene probabilidad ½. C1 y C2 siguen siendo de MAX. "
            + "; ".join(formulas) + f". C1 vale v = {f(valores['C1'])} y C2 v = "
            f"{f(valores['C2'])}. R elige el mayor: {jugada}, con {f(valores['R'])}. Gana der "
            "gracias a la hoja 12: con MIN en D, esa hoja no cuenta y D valdría 2.")
    out = []
    y = _titulo_t(out, titulo) + 8
    y = _info(out, y, "I, C y D: volados parejos")
    y0 = y + 30 + NODO_T_H / 2
    camino_jugada = next(c for c in nombres if nombres[c][1] == jugada)
    fondo = dibujar_t(out, arbol, estados, y0, resaltar=[camino_jugada],
                      tipos={c: "azar" for c in azar}, rotulos_arista=rotulos,
                      renglones={(): "DECIDIR"},
                      recuadro=[f"mejor_jugada = {jugada}", f"mejor_valor = {f(valores['R'])}"])
    y = _pie_t(out, fondo + HOJA_T_R + 44, formulas, peso="700")
    y = _pie_t(out, y, ["Gana der por la hoja 12:", "con MIN, D valdría 2."])
    return _svg_t(titulo, desc, y - 10, out)


# -------------------------------------------- T con corte por profundidad ---

SEP_C3 = " · "     # une los renglones del <title> en las figuras de la clase 3


def _fila_tramo_1(traza):
    """La fila que cierra el tramo 1 de la traza con corte: R recibe el w de C
    (cerro izq y centro). Se busca por evento, no por numero."""
    return next(f["n"] for f in traza["filas"] if f["evento"] == "raiz" and f["hijo"] == "C")


def jue_t_corte(d, tramo=None):
    """Minimax con corte a profundidad d en T: los nodos de la linea de corte
    reciben EVAL; lo de abajo no se genera (caja o circulo punteado con «?»,
    la marca de A_notacion). tramo=1 dibuja el estado al cerrar izq y centro
    (la serie va de parcial a resuelta); tramo=2, el final de esa serie, con
    su nombre; None, el final de una figura sin tramos."""
    arbol = j.ARBOL_T
    traza = j.traza_decidir(arbol, profundidad=d, evaluar=j.EVAL_T)
    exacta = j.traza_decidir(arbol)
    k = _fila_tramo_1(traza) if tramo == 1 else len(traza["filas"])
    fila = traza["filas"][k - 1]
    estados = _fotos_por_camino(arbol, traza, k)
    nunca = set(_orden_caminos(arbol)) - set(traza["caminos_generados"])
    for c in nunca:
        estados[c]["estado"] = "podado"
    nombres = j.nombres_t(arbol)
    f = j.fmt_t
    evaluados = [c for c in _orden_caminos(arbol) if estados[c]["estado"] == "evaluado"]
    raiz = {f_["hijo"]: f_["w"] for f_ in traza["filas"][:k] if f_["evento"] == "raiz"}
    reales = {f_["hijo"]: f_["w"] for f_ in exacta["filas"] if f_["evento"] == "raiz"}
    jugada, valor = fila["mejor_jugada"], fila["mejor_valor"]
    jugada_c = next(n for c, (n, a) in nombres.items() if a == jugada)
    if tramo == 1:
        anterior = traza["filas"][k - 2]["mejor_jugada"]
        titulo = [f"Corte con d = {d}, tramo 1", f"{jugada} sube a {f(valor)}"]
        evento = (f"Tramo 1: R recibe w = {f(raiz[jugada_c])} de {jugada_c}, y mejor_jugada pasa "
                  f"de {anterior} a {jugada}.")
    elif tramo == 2:
        ultimo = next(f_ for f_ in reversed(traza["filas"]) if f_["evento"] == "raiz")
        titulo = [f"Corte con d = {d}, tramo 2",
                  f"{ultimo['hijo']} devuelve {f(ultimo['w'])}: sigue {jugada}"]
        evento = (f"Tramo 2: R recibe w = {f(ultimo['w'])} de {ultimo['hijo']}, que no mejora "
                  f"{f(valor)}: mejor_jugada sigue en {jugada}, y R juega {jugada}, "
                  f"con {f(valor)}.")
    elif jugada != exacta["jugada"]:
        titulo = [f"Corte con d = {d}", f"{jugada} parece valer {f(valor)}"]
        evento = f"R juega {jugada}, con {f(valor)}."
    else:
        titulo = [f"Corte con d = {d}", f"juega {jugada}, con {f(valor)}"]
        evento = f"R juega {jugada}, con {f(valor)}."
    por_mirar = [nombres[c][0] for c in _orden_caminos(arbol)
                 if estados[c]["estado"] == "pormirar" and isinstance(j.nodo_en(arbol, c), tuple)]
    desc = (f"El árbol T con corte a profundidad {d}. Una línea punteada marca dónde se corta, "
            f"bajo el nivel {d}; lo que queda debajo no se genera y va en caja o círculo "
            f"punteado con «?». "
            + "; ".join(f"{nombres[c][0]} recibe EVAL = {f(estados[c]['v'])}" for c in evaluados)
            + ". " + "; ".join(f"{n} vale {f(v)}" for n, v in raiz.items())
            + (f"; {', '.join(por_mirar)} todavía por mirar" if por_mirar else "")
            + f". {evento} Se han generado {fila['generados']} de 14 nodos.")
    out = []
    y = _titulo_t(out, titulo) + 8
    y = _info(out, y, f"{fila['generados']} de 14 nodos"
              + (" hasta aquí" if tramo == 1 else ""))
    y0 = y + 30 + NODO_T_H / 2
    ys = _niveles(y0)
    resaltar = [(1,)] if tramo == 1 else []
    fondo = dibujar_t(out, arbol, estados, y0, resaltar=resaltar, renglones={(): "DECIDIR"},
                      rotulos_tenues=False,
                      recuadro=[f"mejor_jugada = {jugada}", f"mejor_valor = {f(valor)}"])
    # La linea va a media distancia entre el nivel d y el siguiente: su
    # rotulo no toca las cajas de arriba ni los nodos de abajo.
    yh = (ys[d] + NODO_T_H / 2 + ys[d + 1] - NODO_T_H / 2) / 2
    out.append(linea(16, yh, ANCHO_T - 16, yh, color=ACENTO, grosor=2.5, guiones="10 7"))
    out.append(_pastilla_t(412 if d == 1 else 300, yh, f"corte (d = {d} en la raíz)", ACENTO,
                           tam=16, mono=False, relleno=FONDO))
    if tramo == 1:
        notas = [f"Tras izq y centro: {jugada} vale {f(valor)};",
                 f"su valor real es {f(reales[jugada_c])}. D todavía",
                 "no se mira: es el tramo 2."]
    elif jugada != exacta["jugada"]:
        notas = [f"{jugada} parece valer {f(raiz[jugada_c])} (EVAL);",
                 f"su valor real es {f(reales[jugada_c])}.",
                 "Lo que queda bajo el corte", "no se genera: es una trampa."]
    else:
        notas = [f"Con este corte, {jugada} vale {f(raiz[jugada_c])};",
                 f"su valor real es {f(reales[jugada_c])}.",
                 "La jugada ya es la de minimax", f"sin corte: {exacta['jugada']}."]
    y = _pie_t(out, fondo + HOJA_T_R + 44, notas)
    items = ([("pila", "en la pila"), ("sube", "acaba de devolver"), ("pormirar", "por mirar")]
             if tramo == 1 else [])
    corte = ("corte_MIN" if d % 2 else "corte_MAX", "de corte, con EVAL")
    y = _leyenda_t(out, y - 4, True, items=items + [corte, ("podado", "no se genera")])
    return _svg_t(titulo, desc, y + 4, out, sep=SEP_C3)


# ------------------------------------------------ profundizacion iterativa ---

def _mini_arbol(out, arbol, traza, y0, gaps=(136, 80, 80)):
    """Dibujo compacto de lo que una busqueda genero, con los hijos de cada
    nodo en el orden en que se visitaron. Las hojas podadas van con «?», y
    un nodo que corto lleva «cota» bajo su v: su valor real puede ser otro."""
    nombres = j.nombres_t(arbol)
    gen_ = traza["caminos_generados"]
    podados = set(traza["podados"])
    hijos = {}
    for c in gen_:
        if c:
            hijos.setdefault(c[:-1], []).append(c)
    # Los podados: hermanos que siguen a un corte, en el orden dado.
    for c in _orden_caminos(arbol):
        if c and c not in gen_ and nombres[c][0] in podados and c[:-1] in hijos:
            hijos[c[:-1]].append(c)
    terminales = []

    def rec(c):
        if c in hijos:
            for h in hijos[c]:
                rec(h)
        else:
            terminales.append(c)
    rec(())
    bw, bh, r, gap = 124, 44, 18, 22
    ancho = {c: (44 if not isinstance(j.nodo_en(arbol, c), tuple) else bw) for c in terminales}
    total = sum(ancho.values()) + gap * (len(terminales) - 1)
    x = (ANCHO_T - total) / 2
    xs = {}
    for c in terminales:
        xs[c] = x + ancho[c] / 2
        x += ancho[c] + gap

    def centro(c):
        if c not in xs:
            hs = [centro(h) for h in hijos[c]]
            xs[c] = (hs[0] + hs[-1]) / 2
        return xs[c]
    centro(())
    final = traza["filas"][-1]["estado"]
    ys = [y0]
    for g in gaps:
        ys.append(ys[-1] + g)
    dibujados = list(xs)
    for c in dibujados:
        if not c:
            continue
        p = c[:-1]
        x1, y1 = xs[p], ys[len(p)] + bh / 2
        hoja = not isinstance(j.nodo_en(arbol, c), tuple)
        x2, y2 = xs[c], ys[len(c)] - (r if hoja else bh / 2)
        if c in gen_:
            out.append(flecha(x1, y1, x2, y2 - 5, color=SUAVE, marcador="s"))
        else:
            out.append(linea(x1, y1, x2, y2, color=LINEA, guiones="6 5"))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            out.append(linea(mx - 14, my, mx + 14, my, color=ACENTO, grosor=5))
        if len(c) == 1:
            # Primer nivel mas alto (136) y rotulo a 0.6: la arista casi vertical
            # se ve arriba y abajo del rotulo, con su punta libre.
            out.append(_pastilla_t(x1 + (x2 - x1) * 0.6, y1 + (y2 - y1) * 0.6, nombres[c][1],
                                   SUAVE))
    for c in dibujados:
        x, y = xs[c], ys[len(c)]
        n = nombres[c][0]
        if not isinstance(j.nodo_en(arbol, c), tuple):
            if c in gen_:
                out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{mezclar(COLOR_FINAL, 0.07)}" '
                           f'stroke="{COLOR_FINAL}" stroke-width="2"/>')
                out.append(texto(x, y + 6, n, tam=16, peso="700"))
            else:
                out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FONDO}" stroke="{LINEA}" '
                           f'stroke-width="2" stroke-dasharray="5 4"/>')
                out.append(texto(x, y + 6, "?", tam=16, color=LINEA, peso="700"))
            continue
        e = final[n]
        tipo = "MAX" if len(c) % 2 == 0 else "MIN"
        color = COLOR_MAX if tipo == "MAX" else COLOR_MIN
        cota = bool(e.get("cota"))
        if c == ():
            rot = "R · MAX"
        elif e["estado"] == "evaluado":
            rot = f"{n} · EVAL = {j.fmt_t(e['v'])}"
        else:
            rot = f"{n} · v = {j.fmt_t(e['v'])}"
        alto = bh + (16 if cota else 0)
        out.append(caja(x - bw / 2, y - bh / 2, bw, alto, relleno=mezclar(color, 0.07),
                        borde=color, grosor=2,
                        guiones="6 4" if e["estado"] == "evaluado" else None, radio=7))
        out.append(texto(x, y + (0 if cota else 6), rot, tam=15 if len(rot) > 11 else 16,
                         peso="700", color=TEXTO))
        if cota:
            out.append(texto(x, y + 20, "· cota", tam=15, color=ACENTO, peso="700"))
    return ys[max(len(c) for c in dibujados)]


def jue_t_iterativa():
    """Profundizacion iterativa en T: tres busquedas de alfa-beta con corte,
    cada una con la jugada que dejo lista la anterior primero."""
    arbol = j.ARBOL_T
    corridas = j.profundizacion_iterativa_t(arbol)
    f = j.fmt_t
    listas = [t["jugada"] for _, _, t in corridas]
    cambia = next((d for (d, _, t), antes in zip(corridas[1:], listas) if t["jugada"] != antes),
                  None)
    if cambia:
        titulo = ["Profundización iterativa", f"en T: {listas[0]} con d = 1,",
                  f"{listas[-1]} desde d = {cambia}"]
    else:
        titulo = ["Profundización iterativa", f"en T: {listas[-1]} desde d = 1"]
    partes = []
    for d, orden, t in corridas:
        cortes = ", ".join(f"corte {tipo} en {n}" for tipo, n, *_ in t["cortes"]) or "ningún corte"
        cotas = [n for n, e in t["filas"][-1]["estado"].items() if e.get("cota")]
        cotas_ = (f"; {', '.join(cotas)} devuelven una cota, no su valor" if cotas else "")
        partes.append(f"d = {d}: la raíz mira {', '.join(orden)}; {t['generados']} nodos; "
                      f"{cortes}{cotas_}; deja lista {t['jugada']} ({f(t['valor'])})")
    total = sum(t["generados"] for _, _, t in corridas)
    desc = ("Tres búsquedas de alfa-beta con corte sobre el árbol T, una debajo de otra, "
            "cada una con la jugada que dejó lista la anterior primero en la raíz. "
            + ". ".join(partes) + f". En total, {total} nodos.")
    out = []
    y = _titulo_t(out, titulo) + 16
    for d, orden, t in corridas:
        out.append(caja(12, y, ANCHO_T - 24, 54, relleno=mezclar(ACENTO, 0.1), borde=ACENTO,
                        radio=6, grosor=1.5))
        out.append(texto(24, y + 22, f"d = {d} · lista: {t['jugada']}", tam=T_FIG,
                         color=ACENTO, peso="700", anclaje="start"))
        out.append(texto(24, y + 44, f"orden: {', '.join(orden)} · {t['generados']} nodos",
                         tam=16, anclaje="start"))
        fondo = _mini_arbol(out, arbol, t, y + 54 + 40)
        y = fondo + 18 + 34
    y = _pie_t(out, y + 4, [f"En total, {total} nodos.",
                            "Punteada con barra: rama podada.",
                            "«cota»: su v salió de la ventana; solo",
                            "es un techo o un piso de su valor."], tam=16)
    return _svg_t(titulo, desc, y - 10, out, sep=SEP_C3)


def jue_ab_ventana():
    """La ventana (α, β) como una banda en la recta: tocar un extremo o salir
    de ella corta. Los dos ejemplos de abajo son los dos cortes del arbol T."""
    W = ANCHO_T
    t = j.traza_decidir(j.ARBOL_T, poda=True)
    beta_f = next(f for f in t["filas"] if f["corta"] == "beta")
    alfa_f = next(f for f in t["filas"] if f["corta"] == "alfa")
    f = j.fmt_t
    titulo = "La ventana (α, β)"
    desc = ("Una recta numérica de −∞ a +∞ con dos marcas, α y β. La banda entre ellas va "
            "resaltada: aquí el valor importa. A la izquierda de α, o en α, v ≤ α: corte alfa, "
            "en un nodo de MIN. A la derecha de β, o en β, v ≥ β: corte beta, en un nodo de "
            "MAX. El igual cuenta. Abajo, los dos cortes del árbol T: D llega con "
            f"({f(alfa_f['alfa'])}, {f(alfa_f['beta'])}) y su hoja {f(alfa_f['w'])} cae a la "
            f"izquierda de α; C2 llega con ({f(beta_f['alfa'])}, {f(beta_f['beta'])}) y su hoja "
            f"{f(beta_f['w'])} cae a la derecha de β.")
    out = [texto(X_PIE, 44, titulo, tam=T_TIT, peso="700", anclaje="start")]
    x0, x1, xa, xb, y = 24, W - 24, 210, 390, 166
    # la banda
    out.append(caja(xa, y - 78, xb - xa, 78, relleno=mezclar(ACENTO, 0.22), borde=ACENTO,
                    grosor=2, radio=6))
    out.append(texto((xa + xb) / 2, y - 46, "aquí el valor", tam=T_TXT, peso="700"))
    out.append(texto((xa + xb) / 2, y - 18, "importa", tam=T_TXT, peso="700"))
    out.append(linea(x0, y, xa, y, color=SUAVE, grosor=4))
    out.append(linea(xb, y, x1, y, color=SUAVE, grosor=4))
    out.append(linea(xa, y, xb, y, color=ACENTO, grosor=6))
    for x, letra in ((xa, "α"), (xb, "β")):
        out.append(linea(x, y - 14, x, y + 14, color=ACENTO, grosor=3))
        out.append(texto(x, y + 44, letra, tam=30, color=ACENTO, peso="700"))
    out.append(texto(x0, y + 44, "−∞", tam=T_TXT, color=SUAVE, anclaje="start"))
    out.append(texto(x1, y + 44, "+∞", tam=T_TXT, color=SUAVE, anclaje="end"))
    for cx, r1, r2, r3 in (((x0 + xa) / 2, "v ≤ α:", "corte alfa", "(nodo de MIN)"),
                           ((xb + x1) / 2, "v ≥ β:", "corte beta", "(nodo de MAX)")):
        out.append(texto(cx, y - 46, r1, tam=T_VAL, peso="700"))
        out.append(texto(cx, y - 16, r2, tam=T_TXT, color=ACENTO, peso="700"))
        out.append(texto(cx, y + 78, r3, tam=T_TXT, color=SUAVE))
    out.append(texto(X_PIE, y + 120, "El igual cuenta:", tam=T_TXT, anclaje="start"))
    out.append(texto(X_PIE, y + 150, "v = α o v = β ya corta.", tam=T_TXT, anclaje="start"))

    # Los dos cortes de T, cada uno en su recta (0 a 12, con colas para ±∞).
    def xv(v):
        if v == float("inf"):
            return x1 - 10
        if v == -float("inf"):
            return x0 + 10
        return 56 + v * 41

    def recta(y, titulo_, alfa, beta, hoja, leyenda):
        s = [texto(X_PIE, y - 76, titulo_, tam=T_TXT, color=SUAVE, anclaje="start"),
             texto(X_PIE, y - 46, leyenda, tam=T_TXT, color=ACENTO, peso="700",
                   anclaje="start")]
        s.append(linea(x0, y, x1, y, color=SUAVE, grosor=3))
        s.append(caja(xv(alfa), y - 9, xv(beta) - xv(alfa), 18, relleno=mezclar(ACENTO, 0.22),
                      borde=ACENTO, grosor=2, radio=4))
        for v, letra in ((alfa, "α"), (beta, "β")):
            if abs(v) == float("inf"):
                continue
            s.append(linea(xv(v), y - 14, xv(v), y + 14, color=ACENTO, grosor=3))
            s.append(texto(xv(v), y + 40, f"{letra} = {f(v)}", tam=T_TXT, color=ACENTO,
                           peso="700"))
        s.append(punto(xv(hoja), y, r=11, color=TEXTO))
        s.append(texto(xv(hoja), y - 18, f"v = {f(hoja)}", tam=T_TXT, peso="700"))
        return "".join(s)

    a_, b_ = alfa_f["alfa"], alfa_f["beta"]
    assert alfa_f["v"] <= a_
    out.append(recta(y + 290, f"D llega con ({f(a_)}, {f(b_)})", a_, b_, alfa_f["v"],
                     f"{f(alfa_f['v'])} ≤ {f(a_)}: corte alfa"))
    a_, b_ = beta_f["alfa"], beta_f["beta"]
    assert beta_f["v"] >= b_
    out.append(recta(y + 460, f"C2 llega con ({f(a_)}, {f(b_)})", a_, b_, beta_f["v"],
                     f"{f(beta_f['v'])} ≥ {f(b_)}: corte beta"))
    H = y + 520
    return "".join([marco(W, H, desc, titulo, desc)] + out + [cierre()])


# ------------------------------------------------ n1, por partes ---
#
# Las posiciones de cada orden: la del orden fijo pone a la izquierda lo que
# se visita primero; la del invertido, tambien (n3 antes que n2). Los
# fantasmas agrupan un subarbol entero que no se genera en una sola caja.

LUGARES_FIJO = {1: (290, 0), 2: (110, 1), 3: (330, 1), 4: (170, 2), 6: (390, 2),
                13: (535, 2), 5: (170, 3)}
LUGARES_INV = {1: (300, 0), 3: (200, 1), 2: (470, 1), 13: (85, 2), 6: (290, 2),
               4: (500, 2), 12: (85, 3), 11: (215, 3), 7: (340, 3), 5: (505, 3)}
# Ancho de cada fantasma en el resumen (letra de 15) y en las partes (de 22,
# pero con renglones mas cortos).
ANCHO_FANTASMA = {6: 120, 13: 100, 11: 96, 7: 120}
ANCHO_FANTASMA_GRANDE = {6: 110, 13: 80, 11: 80, 7: 110}
# Lo que cada fantasma agrupa: el nodo y todo lo que cuelga de el.
FANTASMAS_FIJO = {6: [6, 7, 8, 9, 10, 11, 12], 13: [13]}
FANTASMAS_INV = {11: [11], 7: [7, 8, 9, 10]}

# Tamanos de las dos escalas: las partes (letra de 22) y los resumenes.
# Un nodo grande mide 150: los que llevan un renglon largo («v = +1 (cota)»)
# piden su propio ancho en su spec.
GRANDE = dict(w=150, h=200, celda=22, escala=22 / 13, tam=T_TXT, y0=225,
              ys_fijo=(0, 320, 640, 960), ys_inv=(0, 320, 640, 990),
              fantasmas=ANCHO_FANTASMA_GRANDE)
CHICA = dict(w=130, h=NODO_ALTO_SUB, celda=21, escala=None, tam=15, y0=200,
             ys_fijo=(0, 210, 420, 630), ys_inv=(0, 210, 420, 640),
             fantasmas=ANCHO_FANTASMA)


def _subarbol(n):
    """n y todos sus descendientes en el subgrafo."""
    nodos = subgrafo_n1()
    fuera = [n]
    for m, (_, _, padre, _) in nodos.items():
        if padre in fuera:
            fuera.append(m)
    return sorted(fuera)


def _dibujar_partes(out, lugares, escala, ys, specs, aristas, cortes=(), ordenes=None):
    """Dibuja los nodos de `specs` en `lugares`.

    specs: {n: dict(modo, renglones, nuevo, lineas, ancho)} con modo
    'tablero' (con su tablero), 'pormirar' (tablero, borde punteado),
    'fantasma' (no se genera: «?») u 'olvidado' (devolvio y se olvido).
    aristas: [(padre, hijo, estilo, pastillas)].
    cortes: [(padre, [hijos podados], rotulo, lado, t)]."""
    nodos = subgrafo_n1()
    w, h, tam = escala["w"], escala["h"], escala["tam"]

    def centro(n):
        x, nivel = lugares[n]
        return x, escala["y0"] + ys[nivel]

    for padre, hijo, estilo, pastillas in aristas:
        if estilo == "normal" and specs.get(hijo, {}).get("modo") == "pormirar":
            estilo = "tenue"  # como el nodo: aun no se recorre
        x1, y1 = centro(padre)
        x2, y2 = centro(hijo)
        out.append(_arista_ab(x1, y1 + h / 2, x2, y2 - h / 2, estilo, pastillas, tam=tam))
    for padre, hijos_, rotulo, lado, t in cortes:
        xp, yp = centro(padre)
        out.append(_corte_ab(xp, yp + h / 2, [(centro(m)[0], centro(m)[1] - h / 2) for m in hijos_],
                             t, rotulo, lado=lado, tam=tam))
    grande = tam >= T_TXT
    for n, spec in specs.items():
        x, y = centro(n)
        t, p, _, _ = nodos[n]
        modo = spec["modo"]
        if modo == "pormirar":
            # Existe, pero el algoritmo aun no llega: tablero tenue, sin tipo
            # ni borde doble (un final por mirar no debe parecer ya valorado).
            f = escala["escala"] or 1
            out.append(caja(x - w / 2, y - h / 2, w, h, relleno=FONDO, borde=LINEA, grosor=2,
                            guiones="8 6"))
            out.append(texto(x, round(y - h / 2 + 22 * f, 1), f"n{n}", tam=round(16 * f, 1),
                             color=SUAVE, peso="700"))
            lado = lado_de(t) * escala["celda"]
            out.append(tablero_svg(x, round(y - h / 2 + 32 * f + lado / 2, 1), t, escala["celda"]))
            out.append(texto(x, round(y + h / 2 - 20 * f, 1), "por mirar", tam=tam, color=SUAVE))
            continue
        if modo == "tablero":
            out.append(nodo_svg(x, y, t, p, spec.get("nombre", f"n{n}"), nuevo=spec.get("nuevo", False),
                                expandido=True, w=spec.get("ancho", w), h=h,
                                celda=escala["celda"], renglones=spec["renglones"],
                                escala=escala["escala"],
                                orden=(ordenes or {}).get(n)))
            continue
        ancho = spec.get("ancho", escala["fantasmas"].get(n, w))
        borde, guiones = (LINEA, "7 6") if modo == "fantasma" else (SUAVE, "2 5")
        out.append(caja(x - ancho / 2, y - h / 2, ancho, h, relleno=FONDO, borde=borde,
                        grosor=2 if modo == "fantasma" else 1.5, guiones=guiones))
        out.append(texto(x, y - h / 2 + (32 if grande else 24), f"n{n}", tam=tam, color=SUAVE,
                         peso="700"))
        lineas = spec.get("lineas", [])
        if modo == "fantasma":
            out.append(texto(x, y + (4 if grande else 0) - (14 if lineas else 0), "?",
                             tam=40 if grande else 30, color=LINEA, peso="700"))
            y_l = y + (40 if grande else 26) - (14 if lineas else 0)
        else:
            y_l = y - (len(lineas) - 1) * (tam * 0.65)
        for k, r in enumerate(lineas):
            out.append(texto(x, round(y_l + k * tam * 1.3, 1), r, tam=tam, color=SUAVE,
                             peso="700" if (modo == "olvidado" and k == 0) else "normal"))


def _fila_final(nuevo=False):
    return dict(modo="tablero", renglones=("final", "U = +1"), nuevo=nuevo)


def _jugada(padre, hijo):
    return subgrafo_n1()[hijo][3] if subgrafo_n1()[hijo][2] == padre else None


def _parte(titulo, desc, notas, lugares, ys_clave, specs, aristas, cortes=(), extra=None):
    """Una figura por partes: alto segun el nivel mas bajo que dibuja."""
    esc = GRANDE
    ys = esc[ys_clave]
    nivel = max(lugares[n][1] for n in specs)
    y_fondo = esc["y0"] + ys[nivel] + esc["h"] / 2
    extra_alto = 32 * len(extra) + 10 if extra else 0
    H = round(y_fondo + extra_alto + 40 + len(notas) * 32 + 20)
    out = [marco(ANCHO, H, desc, titulo, desc)]
    # «Orden fijo · 2. Corte alfa en n3» en dos renglones, a la izquierda.
    cabeza, resto = titulo.split(". ", 1)
    out.append(texto(X_PIE, 40, cabeza, tam=T_TIT, peso="700", anclaje="start"))
    out.append(texto(X_PIE, 72, resto, tam=T_TXT, peso="700", anclaje="start"))
    _dibujar_partes(out, lugares, esc, ys, specs, aristas, cortes)
    for k, r in enumerate(extra or ()):
        out.append(texto(X_PIE, y_fondo + 44 + 32 * k, r, tam=T_TXT, color=ACENTO, peso="700",
                         anclaje="start"))
    out.append(_notas_ab(y_fondo + extra_alto + 52, notas))
    out.append(cierre())
    return "".join(out)


def _a(padre, hijo, estilo="normal", ventana=None, t_jugada=0.45, t_ventana=0.82):
    """Una arista con su jugada y, si se da, la ventana con la que llega el hijo."""
    color = ACENTO if estilo == "nueva" else (LINEA if estilo == "tenue" else SUAVE)
    pastillas = [(t_jugada, _jugada(padre, hijo), color)]
    if ventana:
        rotulo, nueva = ventana
        pastillas.append((t_ventana, rotulo, ACENTO if nueva else SUAVE))
    return (padre, hijo, estilo, pastillas)


def _datos_fijo():
    visitas, cortes = traza_n1(False)
    assert list(visitas) == [1, 2, 3, 4, 5] and cortes == {(3, 6): "alfa"}
    _, _, a3, b3, v3 = visitas[3]
    _, _, a4, b4, v4 = visitas[4]
    v1 = visitas[1][4]
    v2 = visitas[2][4]
    v5 = visitas[5][4]
    assert a3 == v2 and v3 <= a3  # el corte alfa con el igual
    return dict(a3=a3, b3=b3, v3=v3, a4=a4, b4=b4, v4=v4, v1=v1, v2=v2, v5=v5,
                generados=len(visitas))


def jue_ab_fijo_parte(parte):
    d = _datos_fijo()
    f = fmt
    v_exacto_n3 = valores_n1()[3]
    ventana3 = f"({f(d['a3'])}, {f(d['b3'])})"
    ventana4 = f"({f(d['a4'])}, {f(d['b4'])})"
    raiz = dict(modo="tablero", renglones=(f"α = {f(d['v2'])}", f"ya tiene {f(d['v2'])}"),
                ancho=160)
    if parte == 1:
        titulo = f"Orden fijo · 1. n2 vale {f(d['v2'])}"
        specs = {1: dict(raiz, nuevo=True), 2: _fila_final(True),
                 3: dict(modo="pormirar", renglones=("por mirar", ""))}
        aristas = [_a(1, 2, "nueva"), _a(1, 3)]
        notas = [f"n2 es final y vale {f(d['v2'])}:", f"MAX ya tiene {f(d['v2'])},",
                 f"así que α = {f(d['v2'])}.", "n3 todavía no se mira."]
        desc = (f"Alfa-beta desde n1 con el orden fijo, parte 1. n1, con su tablero, arriba: "
                f"mueve Blancas (MAX). Su primer hijo, n2, tras c1-c2, va resaltado: final, "
                f"vale {f(d['v2'])}. La raíz lleva la anotación α = {f(d['v2'])}. n3, tras "
                "c1xb2, aparece punteado y sin expandir.")
        return _parte(titulo, desc, notas, LUGARES_FIJO, "ys_fijo", specs, aristas)
    if parte == 2:
        titulo = "Orden fijo · 2. Corte alfa en n3"
        specs = {1: raiz, 2: _fila_final(),
                 3: dict(modo="tablero", nuevo=True, ancho=176,
                         renglones=("v ≤ α: corta", f"v = {f(d['v3'])} (cota)")),
                 4: dict(modo="tablero", nuevo=True, ancho=156,
                         renglones=("una jugada", f"v = {f(d['v4'])}")),
                 5: _fila_final(True),
                 6: dict(modo="fantasma", lineas=["y lo que", "cuelga"]),
                 13: dict(modo="fantasma")}
        aristas = [_a(1, 2), _a(1, 3, "nueva", (ventana3, True)),
                   _a(3, 4, "nueva", (ventana4, True)),
                   _a(4, 5, "nueva"),
                   _a(3, 6, "tenue", t_jugada=0.7), _a(3, 13, "tenue", t_jugada=0.7)]
        cortes = [(3, [6, 13], "corte alfa", "der", 0.28)]
        generados = d["generados"]
        notas = [f"n3 llega con {ventana3}.", f"n4 da {f(d['v4'])}, y en n3",
                 f"v = {f(d['v3'])} ≤ α = {f(d['a3'])}.", "n6 (con lo que cuelga) y n13",
                 f"no se generan: {generados} de 13."]
        desc = (f"Alfa-beta desde n1 con el orden fijo, parte 2. n3, de MIN, llega con {ventana3}. "
                f"Debajo, n4, de MAX, llega con {ventana4}, y su único hijo n5, final, vale "
                f"{f(d['v5'])}. n3 muestra v = {f(d['v3'])} ≤ α = {f(d['a3'])}: corta y "
                f"devuelve una cota, su valor exacto es {f(v_exacto_n3)}. Una barra de acento "
                "con la leyenda «corte alfa» va bajo n3. Al lado, dos cajas punteadas con «?»: "
                f"n6 con lo que cuelga de él, tras c3-c2, y n13, tras c3xb2; no se generan. "
                f"{generados} de 13 nodos.")
        return _parte(titulo, desc, notas, LUGARES_FIJO, "ys_fijo", specs, aristas, cortes)
    raise ValueError("El orden fijo admite partes 1 y 2")


def _datos_inv():
    visitas, cortes = traza_n1(True)
    assert list(visitas) == [1, 3, 13, 6, 12, 4, 5, 2] and cortes == {(6, 11): "beta"}
    return visitas, cortes


def jue_ab_invertido_parte(parte):
    visitas, _ = _datos_inv()
    f = fmt
    v13 = visitas[13][4]
    _, _, a6, b6, v6 = visitas[6]
    v12 = visitas[12][4]
    _, _, a4, b4, v4 = visitas[4]
    v5 = visitas[5][4]
    _, _, a2, b2, v2 = visitas[2]
    v3, v1 = visitas[3][4], visitas[1][4]
    assert v6 >= b6 and v5 >= b4 and v3 == valores_n1()[3]
    ventana6, ventana4, ventana2 = (f"({f(a6)}, {f(b6)})", f"({f(a4)}, {f(b4)})",
                                    f"({f(a2)}, {f(b2)})")
    por_mirar = dict(modo="pormirar", renglones=("por mirar", ""))
    n3_beta = (f"β: +∞ → {f(v13)}", "MIN tiene " + f(v13))
    n6_corte = ("v ≥ β: corta", f"v = {f(v6)} (cota)")
    # Ancho propio de los nodos con renglones largos.
    a3_, a6_, a4_ = dict(ancho=176), dict(ancho=176), dict(ancho=160)
    fantasmas = {11: dict(modo="fantasma"), 7: dict(modo="fantasma", lineas=["y lo que", "cuelga"])}
    if parte == 1:
        titulo = f"Orden invertido · 1. n13 vale {f(v13)}"
        specs = {1: dict(modo="tablero", renglones=("MAX", "espera")),
                 3: dict(modo="tablero", nuevo=True, renglones=n3_beta, **a3_),
                 2: por_mirar, 13: _fila_final(True) | dict(renglones=("final", f"U = {f(v13)}")),
                 6: por_mirar, 4: por_mirar}
        aristas = [_a(1, 3, "nueva"), _a(1, 2),
                   _a(3, 13, "nueva", t_jugada=0.55), _a(3, 6, t_jugada=0.3), _a(3, 4)]
        notas = ["Al revés, n1 mira primero", "c1xb2, y n3 mira", "primero c3xb2.",
                 f"n13 vale {f(v13)}: en n3,", f"β pasa de +∞ a {f(v13)}."]
        desc = (f"Alfa-beta desde n1 con el orden invertido, parte 1. n1, con su tablero, "
                "arriba. Su primer hijo ahora es n3, tras c1xb2: mueve Negras (MIN). El primer "
                f"hijo de n3, n13, tras c3xb2, va resaltado: final, vale {f(v13)}. n3 lleva la "
                f"anotación «β: +∞ → {f(v13)}»: β pasa de +∞ a {f(v13)}. n6, n4 y n2 aparecen punteados: aún no se miran.")
        return _parte(titulo, desc, notas, LUGARES_INV, "ys_inv", specs, aristas)
    if parte == 2:
        titulo = "Orden invertido · 2. Corte beta en n6"
        specs = {1: dict(modo="tablero", renglones=("MAX", "espera")),
                 3: dict(modo="tablero", renglones=n3_beta, **a3_),
                 2: por_mirar, 13: dict(modo="tablero", renglones=("final", f"U = {f(v13)}")),
                 6: dict(modo="tablero", nuevo=True, renglones=n6_corte, **a6_),
                 12: _fila_final(True), 4: por_mirar, **fantasmas}
        aristas = [_a(1, 3), _a(1, 2),
                   _a(3, 13, t_jugada=0.55), _a(3, 6, "nueva", (ventana6, True), t_jugada=0.3),
                   _a(3, 4),
                   _a(6, 12, "nueva"), _a(6, 11, "tenue", t_jugada=0.78),
                   _a(6, 7, "tenue", t_jugada=0.5)]
        cortes = [(6, [11, 7], "corte beta", "der", 0.27)]
        notas = [f"n6 llega con {ventana6}.", f"n12 vale {f(v12)}:", f"v = {f(v6)} ≥ β = {f(b6)}.",
                 "Corte beta: n11 y n7", "(con lo que cuelga)", "no se generan."]
        desc = (f"Alfa-beta desde n1 con el orden invertido, parte 2. n6, de MAX, llega con "
                f"{ventana6}. Su primer hijo, n12, tras b2xa3, va resaltado: final, vale {f(v12)}. "
                f"n6 muestra v = {f(v6)} ≥ β = {f(b6)}: corta y devuelve v = {f(v6)}, una cota. Una barra de acento con la "
                "leyenda «corte beta» va bajo n6. Sus otros dos hijos, n11 tras b2-b3 y n7 tras "
                "b1xc2 con lo que cuelga de él, son cajas punteadas con «?»: no se generan.")
        return _parte(titulo, desc, notas, LUGARES_INV, "ys_inv", specs, aristas, cortes)
    if parte == 3:
        titulo = f"Orden invertido · 3. n1 vale {f(v1)}"
        specs = {1: dict(modo="tablero", nuevo=True, renglones=("MAX", f"v = {f(v1)}")),
                 3: dict(modo="tablero", nuevo=True, renglones=("MIN", f"v = {f(v3)}"), **a3_),
                 2: _fila_final(True),
                 13: dict(modo="tablero", renglones=("final", f"U = {f(v13)}")),
                 6: dict(modo="tablero", renglones=n6_corte, **a6_),
                 12: _fila_final(),
                 4: dict(modo="tablero", nuevo=True, renglones=("v ≥ β: corta", f"v = {f(v4)}"),
                         **a4_),
                 5: _fila_final(True), **fantasmas}
        aristas = [_a(1, 3, t_jugada=0.4), _a(1, 2, "nueva", (ventana2, True)),
                   _a(3, 13, t_jugada=0.55), _a(3, 6, ventana=(ventana6, False), t_jugada=0.3),
                   _a(3, 4, "nueva", (ventana4, True)),
                   _a(6, 12), _a(6, 11, "tenue", t_jugada=0.78),
                   _a(6, 7, "tenue", t_jugada=0.5), _a(4, 5, "nueva", t_jugada=0.72)]
        cortes = [(6, [11, 7], "corte beta", "der", 0.27)]
        notas = [f"n3 devuelve v = {f(v3)}, su valor", f"exacto: en n1, α = {f(v3)}.",
                 f"n2 llega con {ventana2}", f"y vale {f(v2)}. n1 vale {f(v1)}:", "8 de 13."]
        desc = (f"Alfa-beta desde n1 con el orden invertido, parte 3. De vuelta en n3, falta n4, "
                f"de MAX, que llega con {ventana4}; su único hijo, n5, vale {f(v5)}, y debajo "
                f"una nota sobre n4: «en n4, v = {f(v5)} ≥ β = {f(b4)}: corta, pero no ahorra». n3 "
                f"devuelve v = {f(v3)}, y en n1 α sube a {f(v3)}. Su último hijo, n2, llega con "
                f"{ventana2} y vale {f(v2)}. La raíz muestra v = {f(v1)}. Se generan 8 de 13 nodos.")
        extra = [f"en n4: v = {f(v5)} ≥ β = {f(b4)},", "corta, pero no ahorra"]
        return _parte(titulo, desc, notas, LUGARES_INV, "ys_inv", specs, aristas, cortes, extra)
    raise ValueError("El orden invertido admite partes de 1 a 3")


# ============================================================ clase 3 ===
#
# La posicion de la clase 3 en el tablero de 4x4: mueven Blancas. Las
# figuras de cortar y evaluar se dibujan sobre ella.

POSICION_C3 = j.POSICION_C3
N4 = 4


def hijos4(tablero, turno):
    return [(j.nombre_jugada(tablero, m, N4), j.mover(tablero, m), j.otro(turno))
            for m in j.jugadas(tablero, turno, N4)]


def ev(tablero):
    return j.evaluar_peones(tablero, N4)


def fmt_eval(v):
    """Un EVAL o un 100·U como lo escriben las paginas: sin «+», con «−»."""
    v = int(v)
    return f"−{-v}" if v < 0 else str(v)


def _nodo_corte(cx, cy, tablero, turno, rotulo, w=150, h=170, celda=19):
    """Un nodo de corte: existe, pero la busqueda no lo expande; recibe EVAL.
    Lleva el borde punteado de «todavia no se expande» de la clase 1."""
    return nodo_svg(cx, cy, tablero, turno, rotulo, expandido=False, w=w, h=h,
                    celda=celda, renglones=("Nodo de corte", f"EVAL = {fmt_eval(ev(tablero))}"))


def _no_generado(cx, cy, w, h, rotulo, tam=15):
    """Un estado que la busqueda nunca genera: caja punteada con «?», la marca
    de A_notacion (la misma que _caja_nodo_t da a un nodo podado de T)."""
    return (caja(cx - w / 2, cy - h / 2, w, h, relleno=FONDO, borde=LINEA, grosor=2,
                 guiones="8 6")
            + texto(cx, cy - h / 2 + 24, rotulo, tam=tam, color=SUAVE, peso="700", fuente=MONO)
            + texto(cx, cy + 14, "?", tam=40, color=LINEA, peso="700")
            + texto(cx, cy + h / 2 - 14, "no se genera", tam=13, color=SUAVE))


def jue_c3_corte_prof_1():
    """Profundidad 1: las tres jugadas de Blancas y su EVAL. Gana la captura.
    La eleccion va en la flecha resaltada; ningun nodo lleva borde de «nuevo»."""
    W, H = ANCHO, 700
    hs = hijos4(POSICION_C3, "B")
    valores = [ev(t) for _, t, _ in hs]
    mejor = max(valores)
    elegida = hs[valores.index(mejor)][0]
    renglones = ["Profundidad 1:", f"{elegida} parece la mejor, con {fmt_eval(mejor)}"]
    titulo = " ".join(renglones)
    desc = ("La posición de la clase arriba, donde mueve Blancas. Sus tres jugadas llevan a "
            "nodos de corte, con borde punteado porque ahí la búsqueda se detiene: "
            + "; ".join(f"{nombre} da EVAL = {fmt_eval(v)}"
                        for (nombre, _, _), v in zip(hs, valores))
            + f". Blancas toma el máximo, {fmt_eval(mejor)}: la flecha de {elegida} va "
            "resaltada.")
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, renglones)
    y_raiz, y_hijo, xs = 185, 470, _xs_hijos(3, paso3=190)
    for (nombre, t, p), x, v in zip(hs, xs, valores):
        out.append(arista_svg(W / 2, y_raiz, x, y_hijo, nombre, nueva=v == mejor, h=170))
    out.append(nodo_svg(W / 2, y_raiz, POSICION_C3, "B", "La posición", w=200, h=170, celda=19,
                        escala=1.1,
                        renglones=("Mueve Blancas · MAX", f"con corte: {fmt_eval(mejor)}")))
    for (nombre, t, p), x in zip(hs, xs):
        out.append(_nodo_corte(x, y_hijo, t, p, nombre))
    out.append(nota_svg(H - 98, ["d = 1 en la raíz: tras la jugada de",
                                 "Blancas queda d = 0, y la búsqueda",
                                 "estima con EVAL en vez de seguir."]))
    out.append(cierre())
    return "".join(out)


def jue_c3_corte_prof_2():
    """Profundidad 2: la jugada de Blancas, todas las respuestas de Negras y
    EVAL en las hojas. Negras toma el minimo; Blancas, el maximo. La eleccion
    va solo en las flechas resaltadas."""
    W = ANCHO
    hs = hijos4(POSICION_C3, "B")
    nietos = [hijos4(t, p) for _, t, p in hs]
    total = sum(len(g) for g in nietos)
    paso = (W - 60) / total
    slots = [30 + paso / 2 + k * paso for k in range(total)]
    y_raiz, y_hijo, y_hoja = 210, 475, 685
    H = y_hoja + 110
    valores_hijo = [min(ev(t) for _, t, _ in g) for g in nietos]
    mejor = max(valores_hijo)
    elegida = hs[valores_hijo.index(mejor)][0]
    # La jugada que gustaba a profundidad 1 y la respuesta que la deshace.
    antes = max(hs, key=lambda h: ev(h[1]))[0]
    g_antes = nietos[[h[0] for h in hs].index(antes)]
    respuesta = min(g_antes, key=lambda h: ev(h[1]))[0]
    verbo = "recaptura con" if "x" in respuesta else "responde"
    renglones = [f"Profundidad 2: tras {antes},", f"Negras {verbo} {respuesta}",
                 f"y Blancas elige {elegida}"]
    titulo = " ".join(renglones)
    desc = ("La posición de la clase, sus tres jugadas y todas las respuestas de Negras, "
            "que son nodos de corte con su EVAL. "
            + " ".join(f"Tras {nombre}, Negras puede "
                       + ", ".join(f"{n2} ({fmt_eval(ev(t2))})" for n2, t2, _ in g)
                       + f": el mínimo es {fmt_eval(v)}."
                       for (nombre, _, _), g, v in zip(hs, nietos, valores_hijo))
            + f" Blancas toma el máximo, {fmt_eval(mejor)}, con {elegida}: las flechas "
            "resaltadas.")
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, renglones)
    k, xs_hijo, hojas = 0, [], []
    for g in nietos:
        mis = slots[k:k + len(g)]
        xs_hijo.append(sum(mis) / len(mis))
        hojas.append(mis)
        k += len(g)
    for (nombre, t, p), x, v in zip(hs, xs_hijo, valores_hijo):
        out.append(arista_svg(W / 2, y_raiz, x, y_hijo, nombre, nueva=v == mejor, h=170))
    wh, hh = paso - 8, 74
    for x, g, mis, v in zip(xs_hijo, nietos, hojas, valores_hijo):
        for (n2, t2, p2), xh in zip(g, mis):
            alcanza = ev(t2) == v
            out.append(flecha(x, y_hijo + 85, xh, y_hoja - hh / 2 - 8,
                              color=ACENTO if alcanza else SUAVE, grosor=3 if alcanza else 2,
                              marcador="p" if alcanza else "s"))
    out.append(nodo_svg(W / 2, y_raiz, POSICION_C3, "B", "La posición", w=200, h=170, celda=19,
                        escala=1.1,
                        renglones=("Mueve Blancas · MAX", f"con corte: {fmt_eval(mejor)}")))
    for (nombre, t, p), x, v in zip(hs, xs_hijo, valores_hijo):
        out.append(nodo_svg(x, y_hijo, t, p, nombre, w=150, h=170, celda=19,
                            renglones=("Negras · MIN", f"mínimo: {fmt_eval(v)}")))
    for g, mis, v in zip(nietos, hojas, valores_hijo):
        for (n2, t2, p2), xh in zip(g, mis):
            out.append(caja(xh - wh / 2, y_hoja - hh / 2, wh, hh, relleno=FONDO,
                            borde=LINEA, grosor=2, guiones="7 5"))
            out.append(texto(xh, y_hoja - 10, n2, tam=14, peso="700", fuente=MONO))
            out.append(texto(xh, y_hoja + 20, fmt_eval(ev(t2)), tam=18, peso="700"))
    out.append(texto(X_PIE, y_hoja + hh / 2 + 32, "Hojas: nodos de corte, con su EVAL",
                     tam=14, color=SUAVE, anclaje="start"))
    out.append(cierre())
    return "".join(out)


# La rama que la pagina dibuja a profundidad 3: la jugada que gana.
RAMA_PROF_3 = "d2-d3"


def jue_c3_corte_prof_3():
    """Profundidad 3, solo la rama d2-d3: las dos respuestas de Negras y, bajo
    cada una, las jugadas de Blancas, con EVAL o 100·U. En las dos, d3-d4
    llega a la fila 4: la rama vale 100. Mide 520 de ancho."""
    W = 520
    raiz = j.arbol_con_corte(POSICION_C3, "B", 3, N4)
    rama = next(h for h in raiz["hijos"] if h["jugada"] == RAMA_PROF_3)
    respuestas = rama["hijos"]
    hojas = [h for r in respuestas for h in r["hijos"]]
    wh, gap = 88, 8
    x0 = (W - (len(hojas) * wh + (len(hojas) - 1) * gap)) / 2 + wh / 2
    xs_hoja = [x0 + k * (wh + gap) for k in range(len(hojas))]
    xs_resp, k = [], 0
    for r in respuestas:
        mis = xs_hoja[k:k + len(r["hijos"])]
        xs_resp.append(sum(mis) / len(mis))
        k += len(r["hijos"])
    ganadoras = sorted({h["jugada"] for h in hojas if h["final"]})
    renglones = ["Profundidad 3, rama d2-d3:", f"{' y '.join(ganadoras)} llega a la fila 4"]
    titulo = " ".join(renglones)
    partes = []
    for r in respuestas:
        partes.append(f"Tras {r['jugada']}, Blancas puede "
                      + ", ".join(f"{h['jugada']} ({fmt_eval(h['valor'])}"
                                  + (", final: gana Blancas)" if h["final"] else ", EVAL)")
                                  for h in r["hijos"])
                      + f": el máximo es {fmt_eval(r['valor'])}.")
    desc = (f"Solo la rama {RAMA_PROF_3} del árbol con d = 3 en la raíz. Tras {RAMA_PROF_3} "
            f"mueve Negras, que tiene {len(respuestas)} respuestas. " + " ".join(partes)
            + f" Negras toma el mínimo, {fmt_eval(rama['valor'])}: {RAMA_PROF_3} vale "
            f"{fmt_eval(rama['valor'])}. La rama tiene {j.contar_con_corte(rama)} nodos.")
    out = [marco(W, 0, desc, titulo, desc)]
    y = encabezado(out, renglones)
    y_rama = y + 120
    y_resp = y_rama + 265
    y_hoja = y_resp + 215
    hh = 96
    H = round(y_hoja + hh / 2 + 70)
    out[0] = marco(W, H, desc, titulo, desc)
    for r, x in zip(respuestas, xs_resp):
        out.append(arista_svg(W / 2, y_rama, x, y_resp, r["jugada"],
                              nueva=r["valor"] == rama["valor"], h=170))
    for r, x, k0 in zip(respuestas, xs_resp, [0, len(respuestas[0]["hijos"])]):
        for h, xh in zip(r["hijos"], xs_hoja[k0:k0 + len(r["hijos"])]):
            alcanza = h["valor"] == r["valor"]
            out.append(flecha(x, y_resp + 85, xh, y_hoja - hh / 2 - (13 if h["final"] else 8),
                              color=ACENTO if alcanza else SUAVE, grosor=3 if alcanza else 2,
                              marcador="p" if alcanza else "s"))
    out.append(nodo_svg(W / 2, y_rama, rama["tablero"], rama["turno"], f"tras {RAMA_PROF_3}",
                        w=170, h=170, celda=19,
                        renglones=("Negras · MIN", f"mínimo: {fmt_eval(rama['valor'])}")))
    for r, x in zip(respuestas, xs_resp):
        out.append(nodo_svg(x, y_resp, r["tablero"], r["turno"], r["jugada"], w=150, h=170,
                            celda=19,
                            renglones=("Blancas · MAX", f"máximo: {fmt_eval(r['valor'])}")))
    for h, xh in zip(hojas, xs_hoja):
        x, yy = xh - wh / 2, y_hoja - hh / 2
        if h["final"]:
            out.append(caja(x - 5, yy - 5, wh + 10, hh + 10, borde=COLOR_FINAL, grosor=2))
            out.append(caja(x, yy, wh, hh, relleno=mezclar(COLOR_FINAL, 0.07),
                            borde=COLOR_FINAL, grosor=2))
            tipo, color = "final", COLOR_FINAL
        else:
            out.append(caja(x, yy, wh, hh, relleno=FONDO, borde=LINEA, grosor=2, guiones="7 5"))
            tipo, color = "EVAL", SUAVE
        out.append(texto(xh, yy + 26, h["jugada"], tam=14, peso="700", fuente=MONO))
        out.append(texto(xh, yy + 58, fmt_eval(h["valor"]), tam=20, peso="700"))
        out.append(texto(xh, yy + 82, tipo, tam=13, color=color, peso="700"))
    out.append(nota_svg(y_hoja + hh / 2 + 34, ["Borde doble: final, 100 · U = 100.",
                                                "Punteado: nodo de corte, con su EVAL."],
                        tam=14))
    out.append(cierre())
    return "".join(out)


def jue_c3_horizonte():
    """La captura a profundidad 1: lo que se ve antes del horizonte y la
    recaptura que queda detras, que nunca se genera (caja punteada con «?»)."""
    W, H = ANCHO, 830
    nombre_c, t1, p1 = [h for h in hijos4(POSICION_C3, "B") if h[0] == "d2xc3"][0]
    nombre_r, t2, p2 = [h for h in hijos4(t1, p1) if "x" in h[0]][0]
    renglones = ["El efecto horizonte:", "la recaptura queda detrás"]
    titulo = " ".join(renglones)
    desc = (f"A profundidad 1, la búsqueda ve la captura {nombre_c} y evalúa en "
            f"{fmt_eval(ev(t1))}: un peón de más. Una línea punteada marca el horizonte, donde "
            f"se corta con d = 1 en la raíz. Detrás está la recaptura {nombre_r}, en una caja "
            f"punteada con «?»: la búsqueda no la genera. Con ella, EVAL bajaría a "
            f"{fmt_eval(ev(t2))}.")
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, renglones)
    x, y0, y1, y2, yh = 190, 200, 465, 735, 610
    out.append(arista_svg(x, y0, x, y1, nombre_c, nueva=True, h=170))
    out.append(nodo_svg(x, y0, POSICION_C3, "B", "La posición", w=200, h=170, celda=19,
                        escala=1.1,
                        renglones=("Mueve Blancas · MAX", f"EVAL = {fmt_eval(ev(POSICION_C3))}")))
    out.append(_nodo_corte(x, y1, t1, p1, f"tras {nombre_c}", w=170))
    out.append(linea(30, yh, W - 30, yh, color=ACENTO, grosor=3, guiones="12 8"))
    out.append(texto(W - 30, yh - 12, "horizonte (d = 1 en la raíz)", tam=15,
                     color=ACENTO, peso="700", anclaje="end"))
    out.append(linea(x, y1 + 85, x, y2 - 70, color=LINEA, grosor=2, guiones="6 5"))
    out.append(texto(x + 12, (y1 + y2) / 2 + 40, nombre_r, tam=15, color=SUAVE, peso="700",
                     fuente=MONO, anclaje="start"))
    out.append(_no_generado(x, y2, 170, 140, f"tras {nombre_r}"))
    nx = 320
    for k, (renglon, color, peso) in enumerate([
            ("Lo que la búsqueda ve:", TEXTO, "700"),
            (f"EVAL = {fmt_eval(ev(t1))}, un peón de más.", TEXTO, "normal"),
            ("", TEXTO, "normal"),
            ("Lo que queda detrás:", SUAVE, "700"),
            (f"Negras recaptura con {nombre_r}", SUAVE, "normal"),
            (f"(EVAL = {fmt_eval(ev(t2))}); la búsqueda", SUAVE, "normal"),
            ("no lo genera.", SUAVE, "normal")]):
        out.append(texto(nx, 425 + 24 * k if k < 3 else 690 + 24 * (k - 3), renglon, tam=16,
                         color=color, peso=peso, anclaje="start"))
    out.append(cierre())
    return "".join(out)


# La profundizacion iterativa sobre la posicion de la clase. El reloj se
# mide en nodos generados por minimax con corte: es la cuenta de trabajo.
PROFUNDIDADES_RELOJ = (1, 2, 3)


def jugada_lista(d):
    """La mejor jugada de la busqueda completa con d en la raiz (la primera
    del arg max, en el orden fijo) y su valor."""
    vals = [(j.minimax_limitado(t, p, d - 1, N4), nombre) for nombre, t, p in hijos4(POSICION_C3, "B")]
    mejor = max(v for v, _ in vals)
    return [n for v, n in vals if v == mejor][0], mejor


def jue_c3_profundizacion():
    """Gantt de la profundizacion iterativa: cada busqueda empieza cuando
    termina la anterior, y cada una deja lista una jugada. Cada reloj es una
    linea con su nombre escrito («reloj 1»): el circulo con numero es, en la
    unidad, el orden de visita."""
    o = 46  # el titulo y el subtitulo en dos renglones cada uno
    W, H = ANCHO, 580 + o
    costos = [j.nodos_con_corte(POSICION_C3, "B", d, N4) for d in PROFUNDIDADES_RELOJ]
    total = sum(costos)
    x0, ancho = 40, W - 80
    esc = ancho / total
    renglones = ["El reloj decide", "qué jugada se entrega"]
    titulo = " ".join(renglones)
    listas = [jugada_lista(d) for d in PROFUNDIDADES_RELOJ]
    desc = ("Tres búsquedas seguidas sobre la posición de la clase, con d = 1, 2 y 3; el largo "
            "de cada barra es el número de nodos que genera: "
            + ", ".join(f"{c} con d = {d}" for d, c in zip(PROFUNDIDADES_RELOJ, costos))
            + ". Cada búsqueda completa deja lista una jugada: "
            + ", ".join(f"d = {d}: {n} ({fmt_eval(v)})"
                        for d, (n, v) in zip(PROFUNDIDADES_RELOJ, listas))
            + ". Dos líneas punteadas, reloj 1 y reloj 2, marcan dos momentos en que se acaba "
            "el tiempo; se entrega la jugada de la última búsqueda completa.")
    out = [marco(W, H, desc, titulo, desc)]
    y = encabezado(out, renglones)
    out.append(nota_svg(y + 26, ["El largo de cada barra: nodos que",
                                 "genera esa búsqueda"], tam=14))
    # Dos relojes: uno que se acaba a media busqueda con d = 2 y otro con d = 3.
    marcas = [(costos[0] + costos[1] // 2, 1), (costos[0] + costos[1] + costos[2] // 2, 2)]
    inicio, ys = 0, []
    for k, (d, c, (nombre, v)) in enumerate(zip(PROFUNDIDADES_RELOJ, costos, listas)):
        y = 130 + o + 95 * k
        ys.append(y)
        xa = x0 + inicio * esc
        out.append(caja(xa, y, c * esc, 30, relleno=mezclar(SERIE[1], 0.35), borde=SERIE[1],
                        radio=5))
        out.append(texto(xa, y - 10, f"d = {d} · {c} nodos", tam=15, peso="700", anclaje="start"))
        lista = f"deja lista: {nombre}" + (" (gana)" if v == 100 else "")
        xt = xa + c * esc + 10
        if xt + 200 > W:
            # Abajo de la barra, y a la izquierda de la linea del reloj que
            # cae en ella: la linea no lo cruza.
            x_fin = xa + c * esc
            for t_, ultima in marcas:
                if ultima == k:
                    x_fin = x0 + t_ * esc - 10
            out.append(texto(round(x_fin, 1), y + 52, lista, tam=15, color=SERIE[0],
                             peso="700", anclaje="end"))
        else:
            out.append(texto(xt, y + 21, lista, tam=15, color=SERIE[0], peso="700",
                             anclaje="start"))
        inicio += c
    # Cada linea empieza bajo el rotulo de la busqueda en curso, para no taparlo.
    yb = ys[-1] + 85
    for k, (t, ultima) in enumerate(marcas):
        x = x0 + t * esc
        out.append(linea(x, ys[ultima] - 2, x, yb, color=ACENTO, grosor=2, guiones="6 5"))
        out.append(texto(round(x, 1), yb + 20, f"reloj {k + 1}", tam=15, color=ACENTO,
                         peso="700"))
        entrega = listas[ultima - 1][0]
        for r, renglon in enumerate([f"Reloj {k + 1}: se acaba durante d = {ultima + 1},",
                                     f"así que entrega {entrega}"]):
            out.append(texto(X_PIE, yb + 62 + 56 * k + 22 * r, renglon, tam=15, color=ACENTO,
                             peso="700", anclaje="start"))
    out.append(cierre())
    return "".join(out)


def _gn(cuenta):
    g, n = cuenta
    return f"{g}/{n}"


def jue_c3_mcts_pasos():
    """Las cuatro fases de una vuelta de MCTS, en cuatro paneles. Los conteos
    (G/N: victorias de MAX / simulaciones) salen de juegos.mcts_vuelta: la raiz
    suma los de sus hijos, cada otro nodo vale 1 (su simulacion) mas los de
    sus hijos, la seleccion usa UCT con c = 1 y la vuelta dibujada actualiza
    el camino con U = +1."""
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    antes = {**vuelta["antes"], "nuevo": (0, 0)}
    despues = vuelta["despues"]
    camino = vuelta["camino"]
    o = 24
    pw, ph = 282, 420
    fin_paneles = 90 + o + 2 * ph + 16
    W, H = ANCHO, fin_paneles + 100
    renglones = ["Una vuelta de MCTS:", f"la raíz pasa de {_gn(antes['r'])} a {_gn(despues['r'])}"]
    titulo = " ".join(renglones)
    desc = ("Cuatro paneles con el mismo árbol; cada nodo dice G/N: victorias de MAX entre "
            "simulaciones que pasaron por él. La raíz no simula: sus cuentas son la suma de las "
            "de sus hijos; cada otro nodo, su propia simulación más las de sus hijos. "
            f"1, selección: desde la raíz, {_gn(antes['r'])}, se baja por el camino resaltado "
            "eligiendo en cada nodo al hijo de mejor promedio para quien mueve ahí: MAX en la "
            f"raíz elige {_gn(antes[camino[1]])}; MIN en ese nodo elige {_gn(antes[camino[2]])}, "
            "donde MAX ganó menos. 2, expansión: se agrega un hijo nuevo, 0/0. 3, simulación: "
            "desde ese hijo se juega una partida al azar hasta un final, que aquí gana MAX, "
            "U = +1. 4, retropropagación: cada nodo del camino suma una simulación y, como ganó "
            "MAX, una victoria: "
            + ", ".join(f"{_gn(antes[n])} pasa a {_gn(despues[n])}"
                        for n in camino + ["nuevo"]) + ".")
    out = [marco(W, H, desc, titulo, desc)]
    encabezado(out, renglones)
    paneles = [("1 · Selección", "baja por el mejor promedio"),
               ("2 · Expansión", "agrega un hijo nuevo"),
               ("3 · Simulación", "juega al azar hasta un final"),
               ("4 · Retropropagación", "sube el resultado")]
    rel = {"r": (0, 0), "a": (-55, 70), "b": (60, 70), "a1": (-100, 140), "a2": (-10, 140),
           "nuevo": (-10, 210)}
    assert camino == ["r", "a", "a2"] and vuelta["padre_nuevo"] == "a2", camino
    aristas = [(p, n) for n, (p, _, _) in j.MCTS_ARBOL.items() if p] + [("a2", "nuevo")]
    bw, bh = 56, 30
    for k, (nombre, sub) in enumerate(paneles):
        px, py = 12 + (k % 2) * (pw + 12), 90 + o + (k // 2) * (ph + 16)
        out.append(caja(px, py, pw, ph, relleno=mezclar(LINEA, 0.12), borde=LINEA, radio=12))
        out.append(texto(px + pw / 2, py + 32, nombre, tam=19, peso="700"))
        out.append(texto(px + pw / 2, py + 56, sub, tam=15, color=SUAVE))
        cx, cy = px + pw / 2 + 15, py + 105
        pos = {n: (cx + dx, cy + dy) for n, (dx, dy) in rel.items()}
        visibles = [n for n in rel if k >= 1 or n != "nuevo"]
        # El camino de la seleccion va en las aristas; el borde de acento,
        # solo en lo nuevo de cada paso: el hijo que se agrega (2) y los
        # nodos cuyas cuentas cambian (4).
        aristas_fuertes = {0: set(zip(camino, camino[1:])), 1: {("a2", "nuevo")}, 2: set(),
                           3: set(zip(camino, camino[1:])) | {("a2", "nuevo")}}[k]
        nuevos = {0: set(), 1: {"nuevo"}, 2: set(), 3: set(camino) | {"nuevo"}}[k]
        for u, v in aristas:
            if v not in visibles:
                continue
            fuerte = (u, v) in aristas_fuertes
            out.append(linea(*pos[u], *pos[v], color=ACENTO if fuerte else SUAVE,
                             grosor=3 if fuerte else 2))
        for n in visibles:
            x, y = pos[n]
            fuerte = n in nuevos
            out.append(caja(x - bw / 2, y - bh / 2, bw, bh, relleno=FONDO,
                            borde=ACENTO if fuerte else SERIE[1], grosor=3 if fuerte else 2,
                            radio=3))
            out.append(texto(x, y + 6, _gn((despues if k == 3 else antes)[n]), tam=15,
                             peso="700", color=TEXTO))
        if k == 2:
            x, y = pos["nuevo"]
            pts = " ".join(f"{x + (10 if i % 2 else -10):.0f},{y + bh / 2 + 4 + 9 * i:.0f}"
                           for i in range(6))
            out.append(f'<polyline points="{pts}" fill="none" stroke="{ACENTO}" stroke-width="2"/>')
            out.append(caja(x - 45, y + bh / 2 + 54, 90, 28, borde=COLOR_FINAL, radio=6, grosor=2))
            out.append(texto(x, y + bh / 2 + 74, "U = +1", tam=15, color=COLOR_FINAL, peso="700"))
        if k == 3:
            for n in ["nuevo"] + camino[::-1]:
                x, y = pos[n]
                out.append(flecha(x + bw / 2 + 12, y + 12, x + bw / 2 + 12, y - 12, color=ACENTO,
                                  grosor=2))
            out.append(texto(px + pw / 2, py + ph - 40, "cada nodo del camino suma",
                             tam=14, color=SUAVE))
            out.append(texto(px + pw / 2, py + ph - 20, "1 simulación y 1 victoria",
                             tam=14, color=SUAVE))
        if k == 0:
            out.append(texto(px + pw / 2, py + ph - 22, "el árbol que ya se construyó", tam=14,
                             color=SUAVE))
    out.append(nota_svg(fin_paneles + 30, ["En cada nodo: G/N, victorias de MAX /",
                                 "simulaciones que pasaron por él. La raíz",
                                 "suma sus hijos; los demás, 1 más sus hijos."], tam=14))
    out.append(cierre())
    return "".join(out)


# ------------------------------------- p6: de donde sale el bono (UCB) ---
#
# Tres graficas con ejes: todo numero dibujado sale de juegos.py (las
# simulaciones con su semilla fija), nada se escribe a mano. Miden ANCHO_UCB
# de ancho; el nombre de cada eje va horizontal (el del eje y, arriba de el),
# para leerse sin girar la cabeza.
#
# ANCHO_UCB = 300 y no 520: a 390 px el sitio no escala los SVG de figura y
# el parrafo que los contiene mide 305 px; a 520 cada grafica se cortaba con
# scroll horizontal y la leyenda o el final del eje x quedaban fuera (ronda 3
# de render). Como jue-c3-bandido-corridas: titulo a 17, margen MARGEN_UCB,
# leyenda y notas debajo, y lo que no cabe en un renglon va en dos.

ANCHO_UCB = 300
MARGEN_UCB = 12
COLOR_COTA = ACENTO
COLOR_FRECUENCIA = SERIE[1]
# Una regla, un trazo y una marca: el color nunca es la unica senal.
ESTILO_REGLA = {
    "mejor_promedio": dict(color=SERIE[2], guiones="8 5", marca="cuadro",
                           rotulo="siempre el mejor promedio"),
    "a_veces_al_azar": dict(color=SERIE[1], guiones="2 4", marca="rombo",
                            rotulo="a veces al azar (10 %)"),
    "ucb": dict(color=ACENTO, guiones=None, marca="circulo", rotulo="UCB, c = 2√2"),
    "ucb_c1": dict(color=COLOR_FINAL, guiones="10 4 2 4", marca="circulo", rotulo="UCB, c = 1"),
}
CURVAS_BONO = (100, 1000, 10000)            # N(s) de cada curva de jue-c3-bono
COLOR_BONO = {100: SERIE[0], 1000: SERIE[1], 10000: SERIE[2]}
GUIONES_BONO = {100: None, 1000: "9 5", 10000: "3 4"}
MARCAS_MICRO_BONO = (10, 30, 60)            # los N(s') del micro, con N(s) = 100
GUIONES_C1 = "10 4 2 4"                     # raya-punto: la curva de c = 1


class Plano:
    """Un rectangulo de grafica: de datos a pixeles, con eje x o y log."""

    def __init__(self, x0, y0, w, h, xs, ys, xlog=False, ylog=False):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xs, self.ys, self.xlog, self.ylog = xs, ys, xlog, ylog

    @staticmethod
    def _t(v, rango, log):
        a, b = rango
        if log:
            return (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a))
        return (v - a) / (b - a)

    def x(self, v):
        return round(self.x0 + self.w * self._t(v, self.xs, self.xlog), 1)

    def y(self, v):
        return round(self.y0 + self.h * (1 - self._t(v, self.ys, self.ylog)), 1)


def _num(v):
    """Rotulo de una marca de escala: 0.001, 0.1, 1, 10 000."""
    if v >= 1000:
        return f"{v:,.0f}".replace(",", " ")
    return f"{v:g}"


def _renglones(r):
    return (r,) if isinstance(r, str) else tuple(r)


def _encabezado_ucb(out, titulo, subtitulos):
    """Titulo a 17 (a 20 no cabe en ANCHO_UCB) y subtitulos a 14, en
    MARGEN_UCB. Devuelve la base del ultimo renglon."""
    y = 30
    out.append(texto(MARGEN_UCB, y, titulo, tam=17, peso="700", anclaje="start"))
    for r in subtitulos:
        y += 22
        out.append(texto(MARGEN_UCB, y, r, tam=14, color=TEXTO, anclaje="start"))
    return y


def _ejes_ucb(out, pl, marcas_x, marcas_y, nombre_x, nombre_y, menores_y=(), margen=MARGEN_UCB):
    """Rejilla tenue en cada marca, ejes, rotulos de escala (14 px) y el
    nombre de cada eje: el de x centrado abajo, el de y arriba a la izquierda.
    Un nombre largo va en varios renglones (una tupla). Devuelve la base del
    ultimo renglon del nombre del eje x."""
    x1, y1 = pl.x0 + pl.w, pl.y0 + pl.h
    for v in menores_y:
        out.append(linea(pl.x0, pl.y(v), x1, pl.y(v), color=mezclar(LINEA, 0.35), grosor=1))
    for v in marcas_y:
        out.append(linea(pl.x0, pl.y(v), x1, pl.y(v), color=mezclar(LINEA, 0.7), grosor=1))
        out.append(texto(pl.x0 - 8, pl.y(v) + 5, _num(v), tam=14, color=SUAVE, anclaje="end"))
    for v in marcas_x:
        out.append(linea(pl.x(v), pl.y0, pl.x(v), y1, color=mezclar(LINEA, 0.7), grosor=1))
        out.append(texto(pl.x(v), y1 + 22, _num(v), tam=14, color=SUAVE))
    out.append(linea(pl.x0, y1, x1, y1, color=SUAVE, grosor=2))
    out.append(linea(pl.x0, pl.y0, pl.x0, y1, color=SUAVE, grosor=2))
    y = y1 + 26
    for r in _renglones(nombre_x):
        y += 22
        out.append(texto(pl.x0 + pl.w / 2, y, r, tam=15, color=TEXTO))
    renglones = _renglones(nombre_y)
    for k, r in enumerate(renglones):
        out.append(texto(margen, pl.y0 - 16 - 22 * (len(renglones) - 1 - k), r, tam=15,
                         color=TEXTO, anclaje="start"))
    return y


def _nota_ucb(y, renglones):
    """Renglones de 14 px en MARGEN_UCB, uno debajo de otro."""
    return "".join(texto(MARGEN_UCB, y + 22 * k, r, tam=14, anclaje="start")
                   for k, r in enumerate(renglones))


def _polilinea(puntos, color, grosor=3, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    pts = " ".join(f"{x},{y}" for x, y in puntos)
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
            f'stroke-width="{grosor}" stroke-linejoin="round"{trazo}/>')


def _marca(x, y, forma, color, r=5):
    if forma == "cuadro":
        return (f'<rect x="{x - r}" y="{y - r}" width="{2 * r}" height="{2 * r}" '
                f'fill="{FONDO}" stroke="{color}" stroke-width="2"/>')
    if forma == "rombo":
        return (f'<polygon points="{x},{y - r - 1} {x + r + 1},{y} {x},{y + r + 1} '
                f'{x - r - 1},{y}" fill="{FONDO}" stroke="{color}" stroke-width="2"/>')
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def _caja_leyenda(out, x, y, w, filas, dx_muestra=12, dx_texto=52):
    """Leyenda debajo de la grafica: [(muestra(x, y) -> svg, rotulo)], la
    muestra de 30 px. Devuelve el borde de abajo de la caja."""
    alto = 14 + 26 * len(filas)
    out.append(caja(x, y, w, alto, relleno=FONDO, borde=LINEA, radio=8, grosor=1))
    for k, (muestra, rotulo) in enumerate(filas):
        yy = y + 20 + 26 * k
        out.append(muestra(x + dx_muestra, yy))
        out.append(texto(x + dx_texto, yy + 5, rotulo, tam=14, color=TEXTO, anclaje="start"))
    return y + alto


def _leyenda_ucb(out, y, filas):
    """_caja_leyenda a todo el ancho de ANCHO_UCB, en MARGEN_UCB."""
    return _caja_leyenda(out, MARGEN_UCB, y, ANCHO_UCB - 2 * MARGEN_UCB + 6, filas,
                         dx_muestra=8, dx_texto=46)


def _dec(v):
    """0.6, −0.2: con signo menos tipografico, como en las paginas."""
    return f"{float(v):g}".replace("-", "−")


def _pct(v):
    return f"{100 * float(v):.1f}".rstrip("0").rstrip(".") + " %"


def puntos_hoeffding(pl):
    """[(n, x, y)] de cada frecuencia observada: n con frecuencia 0 no cabe
    en el eje log y no se dibuja (no ocurre con la semilla de la figura)."""
    t = j.tabla_hoeffding()
    return [(n, pl.x(n), pl.y(float(f))) for n, (f, _) in t.items() if f > 0]


def plano_hoeffding():
    # y0 = 126: arriba van titulo, subtitulo y el nombre del eje y en dos renglones.
    return Plano(56, 126, 214, 240, (0, 200), (0.001, 1), ylog=True)


def jue_c3_hoeffding():
    """Frecuencia observada de ū(s′) ≤ μ(s′) − ε contra N(s′) (puntos) y la
    cota de Hoeffding (linea), eje y logaritmico. Jugada y: μ = 0.3, ε = 0.2."""
    t = j.tabla_hoeffding()
    mu, eps, reps = float(j.MU_HOEFFDING), float(j.EPS_HOEFFDING), j.REPS_HOEFFDING
    pl = plano_hoeffding()
    W = ANCHO_UCB
    renglones = ["Cuánto falla un promedio", f"jugada y: μ = {_dec(mu)}, ε = {_dec(eps)}"]
    citas = ", ".join(f"con N(s′) = {n}, {_pct(t[n][0])} contra una cota de {_pct(t[n][1])}"
                      for n in (10, 50, 100))
    desc = (f"Gráfica con eje y logarítmico. Eje x: N(s′), simulaciones, de 0 a 200. Eje y: "
            f"frecuencia con que el promedio ū(s′) queda en μ(s′) − ε o menos, de 0.001 a 1. "
            f"Puntos: la frecuencia observada en {reps:,} tiradas de 200 simulaciones de la "
            f"jugada y, con μ = {mu:g} y ε = {eps:g}. Línea: la cota de Hoeffding, "
            f"exp(−N(s′)·ε²/2). Todos los puntos quedan bajo la línea: {citas}. "
            "Los dos bajan con N(s′); la cota es holgada pero vale para todo N(s′).").replace(
                ",000", " 000")
    out = []
    _encabezado_ucb(out, renglones[0], renglones[1:])
    y_pie = _ejes_ucb(out, pl, (0, 50, 100, 150, 200), (0.001, 0.01, 0.1, 1),
                      "N(s′): simulaciones de la jugada",
                      ("frecuencia de ū(s′) ≤ μ(s′) − ε", "(escala log)"),
                      menores_y=[k * 10.0 ** e for e in (-3, -2, -1) for k in range(2, 10)])
    out.append(_polilinea([(pl.x(n), pl.y(c)) for n, (_, c) in t.items()], COLOR_COTA,
                          grosor=3))
    for _, x, y in puntos_hoeffding(pl):
        out.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{COLOR_FRECUENCIA}"/>')
    # Debajo de la grafica: dentro de ella, en cualquier esquina, tapaba
    # puntos o la linea (visto renderizando).
    y_pie = _leyenda_ucb(out, y_pie + 18, [
        (lambda x, y: f'<circle cx="{x + 14}" cy="{y}" r="4" fill="{COLOR_FRECUENCIA}"/>',
         "observada (simulación)"),
        (lambda x, y: linea(x, y, x + 30, y, color=COLOR_COTA, grosor=3),
         "cota: exp(−N(s′)·ε²/2)")])
    nota = [f"{reps:,} tiradas de 200 simulaciones".replace(",", " "),
            "de y, con semilla fija; un punto", "por N(s′)."]
    out.append(_nota_ucb(y_pie + 28, nota))
    H = y_pie + 28 + 22 * (len(nota) - 1) + 18
    return "".join([marco(W, H, desc, " ".join(renglones), desc)] + out + [cierre()])


def plano_bono():
    return Plano(56, 100, 214, 240, (0, 200), (0, 4))


def jue_c3_bono():
    """El bono 2√2·√(ln N(s)/N(s′)) contra N(s′) para N(s) = 100, 1000 y
    10 000, y la curva de c = 1 (la de la p5) con N(s) = 100, de raya y punto."""
    pl = plano_bono()
    W = ANCHO_UCB
    ns = list(range(5, 201))
    renglones = ["El bono contra N(s′)", "c = 2√2, escala ±1"]
    micro = ", ".join(f"{j.bono_ucb(100, n):.2f} con N(s′) = {n}" for n in MARCAS_MICRO_BONO)
    desc = ("Gráfica. Eje x: N(s′), simulaciones de la jugada, de 0 a 200. Eje y: el bono "
            "2√2·√(ln N(s)/N(s′)), de 0 a 4. Tres curvas, una por N(s): 100, 1 000 y 10 000; "
            "las tres bajan al crecer N(s′), y con más N(s) quedan más arriba. Con N(s) = 100 "
            f"el bono vale {micro}. Una cuarta curva, tenue y de raya y punto: c = 1, la de la p5, "
            f"con N(s) = 100: {j.bono_ucb(100, 10, c=1):.2f} con N(s′) = 10.")
    out = []
    _encabezado_ucb(out, renglones[0], renglones[1:])
    y_pie = _ejes_ucb(out, pl, (0, 50, 100, 150, 200), (0, 1, 2, 3, 4),
                      "N(s′): simulaciones de la jugada", "bono (en unidades de ū)")
    out.append(_polilinea([(pl.x(n), pl.y(j.bono_ucb(100, n, c=1))) for n in ns], SUAVE,
                          grosor=2, guiones=GUIONES_C1))
    for n_padre in CURVAS_BONO:
        out.append(_polilinea([(pl.x(n), pl.y(j.bono_ucb(n_padre, n))) for n in ns],
                              COLOR_BONO[n_padre], grosor=3, guiones=GUIONES_BONO[n_padre]))
    # Sin rotulo junto al punto: las curvas de arriba lo cruzaban; los
    # valores van en el pie.
    for n in MARCAS_MICRO_BONO:
        out.append(_marca(pl.x(n), pl.y(j.bono_ucb(100, n)), "circulo", COLOR_BONO[100], r=5))
    filas = [(lambda x, y, n=n: linea(x, y, x + 30, y, color=COLOR_BONO[n], grosor=3,
                                      guiones=GUIONES_BONO[n]),
              f"N(s) = {_num(n)}") for n in CURVAS_BONO]
    filas.append((lambda x, y: linea(x, y, x + 30, y, color=SUAVE, grosor=2, guiones=GUIONES_C1),
                  "c = 1, N(s) = 100"))
    # Debajo del eje, a la izquierda, como en jue-c3-hoeffding: dentro de la
    # grafica, a la derecha, quedaba fuera de vista a 390 px (visto en la
    # ronda 1 de render) y era la unica clave de las cuatro curvas.
    y_pie = _leyenda_ucb(out, y_pie + 18, filas)
    nota = ["Puntos: N(s) = 100 y N(s′) = " + ", ".join(str(n) for n in MARCAS_MICRO_BONO) + ";",
            "el bono vale " + ", ".join(f"{j.bono_ucb(100, n):.2f}" for n in MARCAS_MICRO_BONO)
            + "."]
    out.append(_nota_ucb(y_pie + 28, nota))
    H = y_pie + 28 + 22 * (len(nota) - 1) + 18
    return "".join([marco(W, H, desc, " ".join(renglones), desc)] + out + [cierre()])


# ------------- jue-c3-pago y jue-c3-eligiendo-x: las dos preguntas ---
#
# Reemplazan a jue-c3-bandido, que graficaba la fraccion ACUMULADA de vueltas
# en x promediada sobre 40 corridas: mezclaba el costo de explorar (las
# primeras vueltas, que cuentan para siempre) con las corridas atoradas, y
# el profesor no la entendio (2026-10-12). Cada una contesta una pregunta:
# ¿cuanto gana cada regla? (pago por vuelta, con la referencia de siempre x)
# y ¿cuantas corridas ya eligen x? (en esa vuelta, no acumulado). Miden
# ANCHO_UCB, como las otras de la p6.

MARCAS_X_BANDIDO = (10, 100, 1000, 10000)
TITULO_PAGO = "¿Cuánto gana cada regla?"
SUBTITULO_PAGO = (f"cada punto: promedio de {j.CORRIDAS_BANDIDO} corridas",
                  "μ de x, y, z: " + ", ".join(_dec(v) for v in j.MUS_HILO.values()))
EJE_Y_PAGO = ("pago promedio por vuelta,", "de la vuelta 1 a N(s)")
ROTULO_SIEMPRE_X = "siempre x (lo mejor posible)"
# Un punto de jue-c3-eligiendo-x cuenta ELECCIONES, no corridas: 40 corridas
# × 10 vueltas = 400. Con «corridas que eligen x», el 98.8 % de UCB se leia
# como «1 de 40 corridas no eligio x», y ninguna se atora (lente de
# correccion r2, H5). Solo sin bono coinciden: 85 % son justo 34 corridas.
TITULO_ELIGIENDO = "¿Qué tanto se elige x?"
SUBTITULO_ELIGIENDO = (f"cada punto: {j.CORRIDAS_BANDIDO} corridas × {j.VENTANA_ELIGIENDO} vueltas",
                       f"(de N(s) − {j.VENTANA_ELIGIENDO - 1} a N(s)), no acumulado")
EJE_Y_ELIGIENDO = ("elecciones que van a x (%),", f"en esas {j.VENTANA_ELIGIENDO} vueltas")
EJE_X_BANDIDO = "N(s): vueltas (escala log)"


def _redondeo(v, decimales):
    """v (Fraction) redondeado hacia arriba en el medio: 0.9875 → 0.988, y
    no lo que haga el binario mas cercano de un float."""
    return math.floor(v * 10 ** decimales + F(1, 2)) / 10 ** decimales


def _f3(v):
    return f"{_redondeo(v, 3):.3f}"


def _pct_f(v):
    """Fraction → «85 %», «92.5 %», «98.8 %», «100 %»."""
    return f"{_redondeo(v * 100, 1):g} %"


def plano_pago():
    # y0 = 150: arriba van titulo, dos subtitulos y el nombre del eje y en
    # dos renglones. De 0.25 a 0.65: el peor punto es 0.295 y el rotulo de
    # «siempre x» va entre 0.6 y el borde de arriba.
    return Plano(56, 150, 214, 240, (10, 10000), (0.25, 0.65), xlog=True)


def plano_eligiendo():
    # Dos subtitulos, como plano_pago. De 40 % a 100 %: el peor punto es
    # 41.8 % y las curvas de arriba quedan separadas (a 0–100 % se tapaban).
    # y0 = 162, 12 mas que plano_pago: el «100» de la escala va en el borde
    # de arriba y a 12 px menos quedaba pegado al nombre del eje (render r4).
    return Plano(56, 162, 214, 240, (10, 10000), (40, 100), xlog=True)


def puntos_pago(pl):
    """{regla: [(N(s), x, y)]} de jue-c3-pago."""
    return {r: [(m, pl.x(m), pl.y(float(v))) for m, v in d.items()]
            for r, d in j.tabla_pago().items()}


def puntos_eligiendo(pl):
    """{regla: [(N(s), x, y)]} de jue-c3-eligiendo-x (y en %)."""
    return {r: [(m, pl.x(m), pl.y(float(v * 100))) for m, v in d.items()]
            for r, d in j.tabla_eligiendo_x().items()}


def _curvas_reglas(out, puntos):
    for r, pts in puntos.items():
        e = ESTILO_REGLA[r]
        out.append(_polilinea([(x, y) for _, x, y in pts], e["color"], grosor=3,
                              guiones=e["guiones"]))
        for _, x, y in pts:
            out.append(_marca(x, y, e["marca"], e["color"], r=4))


def _leyenda_reglas(out, y, valores):
    """La leyenda de las cuatro reglas, cada una con su valor final: en
    N(s) = 10 000 las marcas quedan a ~10 px y el dibujo solo no dice cual
    va arriba (ronda 2 de render de jue-c3-bandido)."""
    filas = [(lambda x, yy, e=ESTILO_REGLA[r]: linea(x, yy, x + 30, yy, color=e["color"],
                                                     grosor=3, guiones=e["guiones"])
              + _marca(x + 15, yy, e["marca"], e["color"], r=4),
              f"{ESTILO_REGLA[r]['rotulo']}: {v}")
             for r, v in valores.items()]
    # Mas ancha y con la muestra mas pegada que _leyenda_ucb: con el valor,
    # «siempre el mejor promedio: 0.543» tocaba el borde (render r4, 1x).
    return _caja_leyenda(out, MARGEN_UCB, y, ANCHO_UCB - MARGEN_UCB - 4, filas,
                         dx_muestra=6, dx_texto=40)


def _cifras(t, fmt):
    """«siempre el mejor promedio, 0.400, 0.533, 0.544 y 0.543; …» en
    N(s) = 10, 100, 1 000 y 10 000, para el aria-label."""
    return "; ".join(f"{ESTILO_REGLA[r]['rotulo']}, "
                     + ", ".join(fmt(d[m]) for m in MARCAS_X_BANDIDO[:-1])
                     + f" y {fmt(d[MARCAS_X_BANDIDO[-1]])}" for r, d in t.items())


def jue_c3_pago():
    """Pago promedio por vuelta de las primeras N(s) vueltas contra N(s), eje
    x log, cuatro reglas, promedio de 40 corridas; la referencia μ(x) = 0.6."""
    t = j.tabla_pago()
    e = j.pago_esperado_reparto()
    pl = plano_pago()
    W, fin, mu_x = ANCHO_UCB, max(j.MARCAS_BANDIDO), j.MUS_HILO["x"]
    en = e["en"]
    cuenta = " + ".join(f"{en[a]}·{_dec(j.MUS_HILO[a])}" if en[a] > 1 else _dec(j.MUS_HILO[a])
                        for a in j.MUS_HILO if en[a])
    cuenta = cuenta.replace("+ −", "− ")
    reparto = (f"Sin bono, {en['x']} corridas se quedan en x, {en['y']} en y y {en['z']} en z: "
               f"se espera ({cuenta})/{j.CORRIDAS_BANDIDO} = {float(e['esperado']):g}; "
               f"simulado, {_f3(t['mejor_promedio'][fin])}.")
    desc = ("Gráfica con eje x logarítmico. Eje x: N(s), vueltas, de 10 a 10 000. Eje y: "
            "pago promedio por vuelta, el promedio de los U de las vueltas 1 a N(s), de 0.25 "
            f"a 0.65. Cada punto es el promedio de {j.CORRIDAS_BANDIDO} corridas con semilla "
            "fija; μ de x, y, z: " + ", ".join(_dec(v) for v in j.MUS_HILO.values())
            + f". Una raya horizontal en {_dec(mu_x)}: siempre x, lo mejor posible. "
            f"En N(s) = 10, 100, 1 000 y 10 000: {_cifras(t, _f3)}. "
            "UCB empieza abajo, porque explora, y termina arriba; ninguna llega a "
            f"{_dec(mu_x)}. {reparto}")
    out = []
    y = _encabezado_ucb(out, TITULO_PAGO, SUBTITULO_PAGO)
    y_pie = _ejes_ucb(out, pl, MARCAS_X_BANDIDO, (0.3, 0.4, 0.5, 0.6), EJE_X_BANDIDO,
                      EJE_Y_PAGO)
    # La referencia, de raya fina y con su rotulo arriba a la izquierda: ahi
    # las curvas van en 0.3–0.4, lejos.
    y_ref = pl.y(float(mu_x))
    out.append(linea(pl.x0, y_ref, pl.x0 + pl.w, y_ref, color=TEXTO, grosor=2, guiones="6 4"))
    out.append(texto(pl.x0 + 6, y_ref - 8, ROTULO_SIEMPRE_X, tam=14, color=TEXTO,
                     anclaje="start"))
    _curvas_reglas(out, puntos_pago(pl))
    y_pie = _leyenda_reglas(out, y_pie + 18, {r: _f3(d[fin]) for r, d in t.items()})
    nota = [f"Sin bono, {en['x']} corridas se quedan en x,",
            f"{en['y']} en y y {en['z']} en z; se espera",
            f"({cuenta})/{j.CORRIDAS_BANDIDO} = {float(e['esperado']):g}."]
    out.append(_nota_ucb(y_pie + 28, nota))
    H = y_pie + 28 + 22 * (len(nota) - 1) + 18
    titulo = " ".join((TITULO_PAGO,) + SUBTITULO_PAGO)
    return "".join([marco(W, H, desc, titulo, desc)] + out + [cierre()])


def jue_c3_eligiendo_x():
    """Porcentaje de las 40 corridas que eligen x en la vuelta N(s) (ventana
    de VENTANA_ELIGIENDO vueltas, no acumulado) contra N(s), eje x log."""
    t = j.tabla_eligiendo_x()
    pl = plano_eligiendo()
    W, fin = ANCHO_UCB, max(j.MARCAS_BANDIDO)
    n, v = j.CORRIDAS_BANDIDO, j.VENTANA_ELIGIENDO
    atoradas = j.reparto_bandido()["mejor_promedio"]["atoradas"]
    tope = j.tope_a_veces_al_azar()
    desc = ("Gráfica con eje x logarítmico. Eje x: N(s), vueltas, de 10 a 10 000. Eje y: "
            f"porcentaje de las elecciones que van a x, no acumulado, de 40 % a 100 %; "
            f"cada punto cuenta {n * v} elecciones: las vueltas N(s) − {v - 1} a N(s) de "
            f"cada una de las {n} corridas. En N(s) = 10, 100, 1 000 y 10 000: "
            f"{_cifras(t, _pct_f)}. Siempre el mejor promedio se aplana en "
            f"{_pct_f(F(n - atoradas, n))}, que aquí sí son {n - atoradas} de {n} corridas: "
            f"las {atoradas} atoradas nunca eligen x y las otras {n - atoradas} siempre. "
            "A veces al azar se queda cerca de 0.9 + 0.1/3 = "
            f"{_pct_f(tope)}. Las dos UCB suben hacia 100 %.")
    out = []
    _encabezado_ucb(out, TITULO_ELIGIENDO, SUBTITULO_ELIGIENDO)
    y_pie = _ejes_ucb(out, pl, MARCAS_X_BANDIDO, (40, 55, 70, 85, 100), EJE_X_BANDIDO,
                      EJE_Y_ELIGIENDO)
    _curvas_reglas(out, puntos_eligiendo(pl))
    y_pie = _leyenda_reglas(out, y_pie + 18, {r: _pct_f(d[fin]) for r, d in t.items()})
    # Sin bono, y solo ahi, el porcentaje de elecciones es tambien el de
    # corridas: las atoradas nunca eligen x y las demas siempre.
    nota = [f"Sin bono, {_pct_f(F(n - atoradas, n))} son justo {n - atoradas} corridas",
            f"de {n}: las {atoradas} atoradas nunca eligen x.",
            "A veces al azar se queda cerca de",
            f"0.9 + 0.1/3 = {_pct_f(tope)}."]
    out.append(_nota_ucb(y_pie + 28, nota))
    H = y_pie + 28 + 22 * (len(nota) - 1) + 18
    titulo = " ".join((TITULO_ELIGIENDO,) + SUBTITULO_ELIGIENDO)
    return "".join([marco(W, H, desc, titulo, desc)] + out + [cierre()])


# ---------------- jue-c3-bandido-corridas: lo que el promedio esconde ---
#
# Una fila por regla, un punto por corrida: el 0.85 de «siempre el mejor
# promedio» en jue-c3-bandido son 34 corridas casi en 1 y 6 casi en 0, y el
# alumno leia «elige la mejor el 85 % de las veces» (2026-10-12).

# A 390 px el sitio no escala los SVG de figura: los pone a su ancho natural
# con scroll propio, y a 520 px se veia solo de 0 a ~0.6 (justo lo que
# importa, cerca de 1, quedaba fuera). Por eso esta figura mide ANCHO_CORRIDAS:
# el parrafo de la figura mide 305 px a 390 (medido en el sitio construido),
# y cada fila apila nombre, promedio y banda. Margen propio, MARGEN_CORRIDAS,
# mas angosto que X_PIE.
ANCHO_CORRIDAS = 300
MARGEN_CORRIDAS = 12
# La x de cada punto ES su fraccion, a ±BIN_CORRIDAS/2 (lente r3, H3): el
# apilado anterior ponia cada grupo en columnas de 10 centradas en la
# mediana, y las tres reglas sin atoradas se pintaban de 0.88 a 1.0 aunque
# sus rangos reales son 0.90–0.94, 0.92–0.96 y 0.96–1.0; las 34 buenas sin
# bono, todas ≥ 0.997, salian desde 0.89, pegadas a la raya del promedio.
# Ahora cada corrida cae en el bin de BIN_CORRIDAS mas cercano a su valor y
# las de un mismo bin se apilan en VERTICAL, como un histograma de puntos.
# El bin mide lo que mide un punto con su hueco: a 260 px de 0 a 1, 0.02 son
# 5.2 px, y el punto, de 2·R_CORRIDAS = 4.4 px. Un bin de 0.01 (2.6 px)
# obligaria a puntos de 2 px. Las filas crecen lo que pida su columna mas
# alta: la de 34 en 1.0 mide 34 puntos.
BIN_CORRIDAS = 0.02
PASO_CORRIDAS = 5.2         # px entre centros vecinos, en x (un bin) y en y
R_CORRIDAS = 2.2            # medio lado de la marca
Y_FILAS = 100               # donde empieza la primera fila
ALTO_MIN_FILA = 104         # cuatro renglones de texto a la izquierda
EJE_X_CORRIDAS = (f"fracción de las {_num(max(j.MARCAS_BANDIDO))} vueltas"
                  " que fueron a x")
# Los mismos textos partidos en renglones que caben en ANCHO_CORRIDAS.
EJE_X_CORRIDAS_RENGLONES = (f"fracción de las {_num(max(j.MARCAS_BANDIDO))} vueltas",
                            "que fueron a x")
SUBTITULO_CORRIDAS = (f"cada punto es una corrida de {_num(max(j.MARCAS_BANDIDO))}"
                      " vueltas")
SUBTITULO_CORRIDAS_RENGLONES = ("cada punto es una corrida",
                                f"de {_num(max(j.MARCAS_BANDIDO))} vueltas")


def columnas_corridas(fr):
    """{bin: [indices de fr]} con bin = el multiplo de BIN_CORRIDAS mas
    cercano a la fraccion (en unidades de bin), cada lista de la fraccion
    menor (abajo) a la mayor."""
    cols = {}
    for s in sorted(range(len(fr)), key=lambda s: (fr[s], s)):
        cols.setdefault(round(fr[s] / BIN_CORRIDAS), []).append(s)
    return cols


def filas_corridas():
    """[(top, fondo, alto)] de cada fila: fondo es la y del punto de mas
    abajo; las columnas crecen hacia arriba desde ahi. La fila que se parte
    (con atoradas) lleva un renglon mas arriba de la banda, «34 en x»."""
    salida, top = [], Y_FILAS
    for d in j.reparto_bandido().values():
        alto_col = PASO_CORRIDAS * max(len(c) for c in columnas_corridas(d["fracciones"]).values())
        if d["atoradas"]:
            alto = round(alto_col + 74, 1)
            fondo = round(top + 58 + alto_col - PASO_CORRIDAS, 1)
        else:
            alto = max(ALTO_MIN_FILA, round(alto_col + 46, 1))
            fondo = round(top + alto - 16, 1)
        salida.append((round(top, 1), fondo, alto))
        top += alto
    return salida


def plano_corridas():
    n = len(j.FILAS_BANDIDO)
    top, _, alto = filas_corridas()[-1]
    return Plano(20, Y_FILAS, 260, round(top + alto - Y_FILAS, 1), (0, 1), (0, n))


def puntos_corridas(pl):
    """{fila: [(semilla, fraccion, x, y)]} de jue-c3-bandido-corridas, en
    orden de semilla: x en el centro del bin de la fraccion, y apilada
    desde el fondo de la fila."""
    r = j.reparto_bandido()
    salida = {}
    for (fila, d), (_, fondo, _) in zip(r.items(), filas_corridas()):
        fr = d["fracciones"]
        lugar = {}
        for b, col in columnas_corridas(fr).items():
            for i, s in enumerate(col):
                lugar[s] = (pl.x(b * BIN_CORRIDAS), round(fondo - PASO_CORRIDAS * i, 1))
        salida[fila] = [(s + 1, f, *lugar[s]) for s, f in enumerate(fr)]
    return salida


def marca_corrida(x, y, forma, color, r=R_CORRIDAS):
    """La marca de una corrida, rellena: a este tamaño el contorno de 2 px
    de _marca la llenaria igual. El rombo, de media diagonal r + 0.3."""
    if forma == "cuadro":
        return (f'<rect x="{round(x - r, 1)}" y="{round(y - r, 1)}" width="{round(2 * r, 1)}" '
                f'height="{round(2 * r, 1)}" fill="{color}"/>')
    if forma == "rombo":
        a = round(r + 0.3, 1)
        return (f'<polygon points="{x},{round(y - a, 1)} {round(x + a, 1)},{y} {x},{round(y + a, 1)} '
                f'{round(x - a, 1)},{y}" fill="{color}"/>')
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def rotulo_atoradas(d):
    """«6 de 40 atoradas: 5 en y, 1 en z» o «0 de 40 atoradas»."""
    base = f"{d['atoradas']} de {d['n']} atoradas"
    if not d["atoradas"]:
        return base
    return base + ": " + ", ".join(f"{v} en {a}" for a, v in sorted(d["en"].items()))


def _f2(v):
    return f"{v:.2f}"


def rango_corridas(d):
    """«de 0.90 a 0.94»: el rango real de la fila, a dos decimales."""
    return f"de {_f2(d['minimo'])} a {_f2(d['maximo'])}"


def resumen_corridas(d):
    """La frase del aria-label de una fila, con sus cifras."""
    if d["atoradas"]:
        buenas = [f for f in d["fracciones"] if f >= j.UMBRAL_ATORADA]
        malas = [f for f in d["fracciones"] if f < j.UMBRAL_ATORADA]
        return (f"{len(buenas)} corridas en {math.floor(min(buenas) * 100) / 100:g} o más "
                f"y {len(malas)} atoradas en {math.ceil(max(malas) * 1000) / 1000:g} o menos "
                f"({', '.join(f'{v} en {a}' for a, v in sorted(d['en'].items()))}), "
                f"promedio {_f2(d['promedio'])}")
    return (f"ninguna atorada, de {d['minimo']:.3f} a {d['maximo']:.3f}, "
            f"promedio {_f2(d['promedio'])}")


def jue_c3_bandido_corridas():
    """Fraccion final en x de cada una de las 40 corridas de 10 000 vueltas,
    una fila por regla, con el promedio de la fila marcado: el reparto que
    el promedio de jue-c3-bandido esconde."""
    r = j.reparto_bandido()
    pl = plano_corridas()
    filas_px = filas_corridas()
    W, y1 = ANCHO_CORRIDAS, pl.y0 + pl.h
    renglones = ["Dónde termina cada corrida"]
    filas = ". ".join(f"{ESTILO_REGLA[f]['rotulo'][:1].upper()}{ESTILO_REGLA[f]['rotulo'][1:]}: "
                      f"{resumen_corridas(d)}" for f, d in r.items())
    n = j.CORRIDAS_BANDIDO
    desc = (f"Gráfica de puntos, una fila por regla. Eje x: {EJE_X_CORRIDAS}, de 0 a 1. "
            f"Cada punto es una corrida de {_num(max(j.MARCAS_BANDIDO))} vueltas: {n} por fila, "
            f"con semillas 1 a {n}. La posición horizontal de cada punto es su valor, "
            f"a ±{_num(BIN_CORRIDAS / 2)}; las corridas de valor cercano se apilan en "
            "vertical, en una columna; una raya vertical marca el promedio de la fila. "
            f"Atorada: menos de la mitad de sus vueltas en x. {filas}.")
    nota = ["Atorada: termina debajo de 0.5.",
            f"Raya vertical: el promedio de las {n}",
            "corridas de la fila. Una columna junta",
            f"las corridas a {_num(BIN_CORRIDAS / 2)} o menos de su x,",
            "apiladas hacia arriba."]
    H = round(y1 + 106 + 22 * (len(nota) - 1) + 18, 1)
    out = [marco(W, H, desc, " ".join(renglones + [SUBTITULO_CORRIDAS]), desc)]
    # El titulo a 17 y no a los 20 de encabezado(): a 20 no cabe en ANCHO_CORRIDAS.
    y = 34
    out.append(texto(MARGEN_CORRIDAS, y, renglones[0], tam=17, peso="700", anclaje="start"))
    for i, r_ in enumerate(SUBTITULO_CORRIDAS_RENGLONES):
        out.append(texto(MARGEN_CORRIDAS, y + 24 + 20 * i, r_, tam=14, color=TEXTO, anclaje="start"))
    # Rejilla y separadores primero: los puntos van encima.
    for v in (0, 0.25, 0.5, 0.75, 1):
        out.append(linea(pl.x(v), pl.y0, pl.x(v), y1, color=mezclar(LINEA, 0.7), grosor=1))
        out.append(texto(pl.x(v), y1 + 22, _num(v), tam=14, color=SUAVE))
    for top, _, _ in filas_px[1:]:
        out.append(linea(pl.x0, top, pl.x0 + pl.w, top, color=mezclar(LINEA, 0.35), grosor=1))
    out.append(linea(pl.x0, y1, pl.x0 + pl.w, y1, color=SUAVE, grosor=2))
    for i, r_ in enumerate(EJE_X_CORRIDAS_RENGLONES):
        out.append(texto(pl.x0 + pl.w / 2, y1 + 46 + 20 * i, r_, tam=15, color=TEXTO))
    puntos = puntos_corridas(pl)
    for (fila, d), (top, fondo, _) in zip(r.items(), filas_px):
        e = ESTILO_REGLA[fila]
        out.append(marca_corrida(MARGEN_CORRIDAS + 6, top + 17, e["marca"], e["color"], r=4.5))
        out.append(texto(MARGEN_CORRIDAS + 20, top + 22, e["rotulo"], tam=15, color=TEXTO, anclaje="start",
                         peso="700"))
        for _, _, x, yy in puntos[fila]:
            out.append(marca_corrida(x, yy, e["marca"], e["color"]))
        cima = min(yy for _, _, _, yy in puntos[fila])
        xm = pl.x(d["promedio"])
        if d["atoradas"]:
            # La fila que se parte: «6 de 40 atoradas» junto a su columna en
            # 0, «34 en x» (con su rango) arriba de la de 1, y el promedio en
            # el hueco entre las dos, donde no hay ninguna corrida.
            partes = rotulo_atoradas(d).split(": ")
            for i, p_ in enumerate([partes[0] + ":", partes[1]]):
                out.append(texto(pl.x(0.06), fondo - 13 + 18 * i, p_, tam=14, color=TEXTO,
                                 anclaje="start"))
            buenas = [f for f in d["fracciones"] if f >= j.UMBRAL_ATORADA]
            out.append(texto(pl.x(1) + 4, top + 46,
                             f"{len(buenas)} en x, {math.floor(min(buenas) * 100) / 100:g} o más",
                             tam=14, color=TEXTO, anclaje="end"))
            y_raya = top + 54
            out.append(texto(xm - 5, round((top + 54 + fondo) / 2, 1), f"promedio {_f2(d['promedio'])}",
                             tam=14, color=TEXTO, anclaje="end"))
        else:
            # Las demas: todo cae de 0.90 a 1, y el texto va a la izquierda.
            for i, p_ in enumerate([rotulo_atoradas(d), rango_corridas(d),
                                    f"promedio {_f2(d['promedio'])}"]):
                out.append(texto(MARGEN_CORRIDAS + 20, top + 46 + 20 * i, p_, tam=14, color=TEXTO,
                                 anclaje="start"))
            # Aqui la raya cae dentro de la columna y la tapaba (render r6):
            # va en dos tramos, arriba y abajo de los puntos, sin cruzarlos.
            out.append(linea(xm, top + 8, xm, round(cima - 6, 1), color=TEXTO, grosor=2))
            out.append(linea(xm, round(fondo + 6, 1), xm, round(fondo + 14, 1), color=TEXTO, grosor=2))
            continue
        out.append(linea(xm, y_raya, xm, round(fondo + 8, 1), color=TEXTO, grosor=2))
    for i, r_ in enumerate(nota):
        out.append(texto(MARGEN_CORRIDAS, y1 + 106 + 22 * i, r_, tam=14, anclaje="start"))
    out.append(cierre())
    return "".join(out)


# ------------------------------- 7.3.7: el arbol T± (un arbol, todos) ---
#
# Figura de problema, angosta: a 390 px el sitio no escala los SVG y el
# parrafo mide ~305, asi que mide ANCHO_TPM. Las hojas van a su profundidad
# real (las de I y D junto a C1 y C2), como en jue-t-arbol.

ANCHO_TPM = 300
LUGARES_TPM = {(): 134, (0,): 38, (1,): 134, (2,): 248,
               (0, 0): 22, (0, 1): 54, (1, 0): 101, (1, 1): 167,
               (2, 0): 216, (2, 1): 248, (2, 2): 280,
               (1, 0, 0): 85, (1, 0, 1): 117, (1, 1, 0): 151, (1, 1, 1): 183}
YS_TPM = (0, 132, 238, 336)          # y de cada nivel, desde la raiz
NODO_TPM_W, NODO_TPM_H, HOJA_TPM_R = 62, 66, 13
COLOR_CAPTURA = COLOR_MIN            # la captura la hace MIN
PIE_TPM = ["Cada hoja es un final con su U:", "+1 gana MAX y −1 gana MIN;",
           "0 es empate.", "En I, C, D, C1 y C2: su EVAL,", "en la escala 100·U.",
           "La x de ix: es una captura de MIN.", "D tiene tres hijos; en T, dos."]


def _signo(u):
    return {1: "+1", -1: "−1", 0: "0"}[u]


def jue_t_pm_arbol():
    """T±: la forma de T con finales en U, una hoja mas en D, la EVAL de los
    nodos internos y la captura ix marcada. Figura de problema."""
    arbol = j.ARBOL_TPM
    ids = j.ids_tpm(arbol)
    caminos = _orden_caminos(arbol)
    es_hoja = {c: not isinstance(j.nodo_en(arbol, c), tuple) for c in caminos}
    hojas = {c: j.nodo_en(arbol, c) for c in caminos if es_hoja[c]}
    jugadas_raiz = {(i,): a for i, a in enumerate(j.JUGADAS_RAIZ)}
    titulo = ["El árbol T±", "T con finales en U"]

    def hojas_de(c):
        xs = [f"{ids[h]} = {_signo(hojas[h])}" for h in caminos if h[:-1] == c and es_hoja[h]]
        return ", ".join(xs[:-1]) + " y " + xs[-1]
    n_hojas = {c: len(j.nodo_en(arbol, c)) for c in caminos if not es_hoja[c]}
    captura = ", ".join(ids[c] for c in sorted(j.CAPTURAS_TPM))
    desc = (f"El árbol T±: la forma del árbol T, con {j.contar_nodos(arbol)} nodos porque D "
            f"tiene {n_hojas[(2,)]} hijos y no 2. La raíz R es de MAX; izq lleva a I, centro a "
            f"C y der a D, los tres de MIN. I tiene las hojas {hojas_de((0,))}; {captura} es "
            f"una captura de MIN. C tiene dos hijos de MAX: C1, con {hojas_de((1, 0))}, y C2, "
            f"con {hojas_de((1, 1))}. D tiene las hojas {hojas_de((2,))}. Cada hoja es un "
            "final con su U: +1 gana MAX, −1 gana MIN, 0 empate. La EVAL de los nodos "
            "internos, en la escala 100·U: "
            + ", ".join(f"{n} = {v}" for n, v in j.EVAL_TPM.items()) + ".")
    out = []
    y = _titulo_t(out, titulo)
    y0 = y + 30 + 25
    ys = [y0 + d for d in YS_TPM]

    def pos(c):
        return LUGARES_TPM[c], ys[len(c)]

    def medio(c):
        return HOJA_TPM_R + 2.5 if es_hoja[c] else NODO_TPM_H / 2

    for c in caminos[1:]:
        (x1, y1), (x2, y2) = pos(c[:-1]), pos(c)
        if c[:-1] == ():
            x1 += 36 * (c[0] - 1)    # las tres aristas de R salen separadas
        ya = y1 + (25 if c[:-1] == () else NODO_TPM_H / 2)
        yb = y2 - medio(c) - 6
        if c in j.CAPTURAS_TPM:
            # La captura: un trazo ancho del color de MIN bajo la flecha comun
            # (el marcador crece con el grosor; asi la punta no cambia).
            out.append(linea(x1, ya, x2, yb, color=COLOR_CAPTURA, grosor=6))
        out.append(flecha(x1, ya, x2, yb, color=SUAVE, grosor=2, marcador="s"))
        if c in jugadas_raiz:
            t = 0.5
            out.append(_pastilla_t(x1 + (x2 - x1) * t, ya + (yb - ya) * t, jugadas_raiz[c],
                                   SUAVE, tam=14))
    # R: una sola caja ancha.
    x, yr = pos(())
    out.append(caja(x - 50, yr - 25, 100, 50, relleno=mezclar(COLOR_MAX, 0.07),
                    borde=COLOR_MAX))
    out.append(texto(x, yr + 6, "R · MAX", tam=17, color=COLOR_MAX, peso="700"))
    for c in caminos[1:]:
        x, yc = pos(c)
        if es_hoja[c]:
            u = hojas[c]
            out.append(f'<circle cx="{x}" cy="{yc}" r="{HOJA_TPM_R + 2.5}" fill="none" '
                       f'stroke="{COLOR_FINAL}" stroke-width="1.5"/>'
                       f'<circle cx="{x}" cy="{yc}" r="{HOJA_TPM_R}" '
                       f'fill="{mezclar(COLOR_FINAL, 0.07)}" stroke="{COLOR_FINAL}" '
                       f'stroke-width="2"/>')
            out.append(texto(x, yc + 5, _signo(u), tam=14, peso="700"))
            captura = c in j.CAPTURAS_TPM
            out.append(texto(x, yc + 34, ids[c], tam=14, peso="700" if captura else "normal",
                             color=COLOR_CAPTURA if captura else SUAVE, fuente=MONO))
            continue
        tipo = "MAX" if len(c) % 2 == 0 else "MIN"
        color = COLOR_MAX if tipo == "MAX" else COLOR_MIN
        w, h = NODO_TPM_W, NODO_TPM_H
        out.append(caja(x - w / 2, yc - h / 2, w, h, relleno=mezclar(color, 0.07), borde=color))
        out.append(texto(x, yc - 13, f"{ids[c]}", tam=17, color=color, peso="700"))
        out.append(texto(x, yc + 5, tipo, tam=14, color=color, peso="700"))
        out.append(texto(x, yc + 24, f"EVAL {j.EVAL_TPM[ids[c]]}", tam=14))
    fondo = ys[3] + HOJA_TPM_R + 34
    y = _pie_t(out, fondo + 34, PIE_TPM, tam=15)
    nombre = titulo[0] + SEP_C3 + titulo[1]
    return "".join([marco(ANCHO_TPM, round(y - 10), desc, nombre, desc)] + out + [cierre()])


DIAGRAMAS = {
    "jue-ciclo-partida": jue_ciclo_partida,
    **{f"jue-grafo-paso-{paso}": (lambda paso=paso: jue_grafo_paso(paso))
       for paso in PASOS_TITULO},
    "jue-subgrafo-n1": jue_subgrafo_n1,
    "jue-transposicion": jue_transposicion,
    **{f"jue-minimax-paso-{paso}": (lambda paso=paso: jue_minimax_paso(paso))
       for paso in PASOS_MINIMAX},
    "jue-minimax-n1": jue_minimax_n1,
    "jue-minimax-genera": jue_minimax_genera,
    "jue-azar-n3": jue_azar_n3,
    "jue-alfa-beta-fijo": lambda: jue_alfa_beta(False),
    "jue-alfa-beta-invertido": lambda: jue_alfa_beta(True),
    "jue-ab-ventana": jue_ab_ventana,
    "jue-ab-fijo-parte-1": lambda: jue_ab_fijo_parte(1),
    "jue-ab-fijo-parte-2": lambda: jue_ab_fijo_parte(2),
    "jue-ab-invertido-parte-1": lambda: jue_ab_invertido_parte(1),
    "jue-ab-invertido-parte-2": lambda: jue_ab_invertido_parte(2),
    "jue-ab-invertido-parte-3": lambda: jue_ab_invertido_parte(3),
    "jue-t-arbol": jue_t_arbol,
    **{f"jue-t-minimax-{paso}": (lambda paso=paso: jue_t_minimax(paso))
       for paso in PASOS_MINIMAX_T},
    **{f"jue-t1-ab-{paso}": (lambda paso=paso: jue_t1_ab(paso)) for paso in PASOS_AB_T1},
    **{f"jue-t-ab-{paso}": (lambda paso=paso: jue_t_ab(paso)) for paso in PASOS_AB_T},
    "jue-t-ab-pila": jue_t_ab_pila,
    "jue-t-azar": jue_t_azar,
    "jue-t-corte-d1": lambda: jue_t_corte(1),
    "jue-t-corte-d2-tramo-1": lambda: jue_t_corte(2, tramo=1),
    "jue-t-corte-d2": lambda: jue_t_corte(2, tramo=2),
    "jue-t-iterativa": jue_t_iterativa,
    "jue-c3-corte-prof-1": jue_c3_corte_prof_1,
    "jue-c3-corte-prof-2": jue_c3_corte_prof_2,
    "jue-c3-corte-prof-3": jue_c3_corte_prof_3,
    "jue-c3-horizonte": jue_c3_horizonte,
    "jue-c3-profundizacion": jue_c3_profundizacion,
    "jue-c3-mcts-pasos": jue_c3_mcts_pasos,
    "jue-c3-hoeffding": jue_c3_hoeffding,
    "jue-c3-bono": jue_c3_bono,
    "jue-c3-pago": jue_c3_pago,
    "jue-c3-eligiendo-x": jue_c3_eligiendo_x,
    "jue-c3-bandido-corridas": jue_c3_bandido_corridas,
    "jue-t-pm-arbol": jue_t_pm_arbol,
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
