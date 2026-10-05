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
import sys
from xml.sax.saxutils import escape

import juegos as j
from gen_optimizacion import (ACENTO, FONDO, FUENTE, LINEA, SERIE, SUAVE,
                              TEXTO, _rombo, caja, cierre, flecha, linea,
                              marco, mezclar, texto)
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
# Todas las figuras miden ANCHO px: la columna del sitio. Por debajo de
# 1470 px de pantalla el sitio muestra los SVG a tamano nativo y desplaza lo
# que sobra, asi que una figura mas ancha obliga a desplazarse de lado. Lo
# que no cabe a lo ancho crece hacia abajo.

ANCHO = 700
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"


def tablero_svg(cx, cy, tablero, celda=24):
    """Tablero de 3x3 con la fila 3 arriba. B y N se escriben, no solo se
    colorean: el color nunca es la unica senal."""
    lado = 3 * celda
    x0, y0 = cx - lado / 2, cy - lado / 2
    s = [caja(x0, y0, lado, lado, relleno=mezclar(LINEA, 0.35), borde=SUAVE,
              radio=3, grosor=1)]
    for k in range(1, 3):
        s.append(linea(x0 + k * celda, y0, x0 + k * celda, y0 + lado, color=SUAVE, grosor=1))
        s.append(linea(x0, y0 + k * celda, x0 + lado, y0 + k * celda, color=SUAVE, grosor=1))
    radio, letra = celda * 0.42, celda * 0.6
    for i, pieza in enumerate(tablero):
        if pieza == ".":
            continue
        fila, col = divmod(i, 3)
        px = x0 + col * celda + celda / 2
        py = y0 + (2 - fila) * celda + celda / 2
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
    g = j.ganador(tablero, turno)
    if g:
        quien = "Blancas" if g == "B" else "Negras"
        return COLOR_FINAL, f"Fin: gana {quien}", f"U = {'+1' if g == 'B' else '−1'}"
    if turno == "B":
        return COLOR_MAX, "Mueve Blancas", "MAX"
    return COLOR_MIN, "Mueve Negras", "MIN"


def nodo_svg(cx, cy, tablero, turno, arriba, nuevo=False, expandido=True,
             w=150, h=160, celda=24):
    """Un nodo: rotulo arriba, tablero al centro y su tipo en dos renglones.

    Borde doble: final. Borde punteado: existe pero aun no se expande.
    Borde grueso de acento: lo nuevo de este paso."""
    color, r1, r2 = tipo_de_nodo(tablero, turno)
    final = bool(j.ganador(tablero, turno))
    x, y = cx - w / 2, cy - h / 2
    s = []
    if final:
        s.append(caja(x - 5, y - 5, w + 10, h + 10, borde=color, grosor=2))
    s.append(caja(x, y, w, h, relleno=mezclar(color, 0.16 if nuevo else 0.07),
                  borde=ACENTO if nuevo else color, grosor=3.5 if nuevo else 2,
                  guiones=None if (expandido or final) else "8 5"))
    f = min(1.5, max(0.88, w / 150))  # la letra crece con el nodo
    s.append(texto(cx, y + 22 * f, arriba, tam=round(16 * f, 1), peso="700"))
    lado = 3 * celda
    s.append(tablero_svg(cx, y + 32 * f + lado / 2, tablero, celda))
    s.append(texto(cx, y + h - 27 * f, r1, tam=round(13 * f, 1), color=color, peso="700"))
    s.append(texto(cx, y + h - 10 * f, r2, tam=round(13 * f, 1), color=color, peso="700"))
    return "".join(s)


def arista_svg(x1, y1, x2, y2, rotulo, nueva=False, h=160):
    """Flecha del borde inferior del padre al superior del hijo, con el
    nombre de la jugada sobre la flecha."""
    color = ACENTO if nueva else SUAVE
    ya, yb = y1 + h / 2, y2 - h / 2 - 8
    s = [flecha(x1, ya, x2, yb, color=color, grosor=3 if nueva else 2,
                marcador="p" if nueva else "s")]
    mx, my = (x1 + x2) / 2, (ya + yb) / 2
    ancho = 11 * len(rotulo) + 14
    s.append(caja(mx - ancho / 2, my - 14, ancho, 26, relleno=FONDO, borde=color,
                  radio=7, grosor=1.5))
    s.append(texto(mx, my + 5, rotulo, tam=15, color=color, peso="700", fuente=MONO))
    return "".join(s)


def leyenda_svg(y, items):
    """Fila de muestras al pie: (tipo, texto) con tipo en
    {'expandido', 'sin', 'final', 'nuevo'}."""
    s = []
    ancho_item = ANCHO / len(items)
    for k, (tipo, rotulo) in enumerate(items):
        x = k * ancho_item + 18
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
    return "".join(s)


def rastro_svg(y, jugadas_previas, destino):
    """Linea de texto con el camino que lleva al nodo de arriba."""
    jugadas_ = ", ".join(jugadas_previas)
    return texto(ANCHO / 2, y, f"Desde s₀ con las jugadas {jugadas_} se llega a {destino}",
                 tam=14, color=SUAVE)


def nota_svg(y, renglones):
    s = []
    for k, r in enumerate(renglones):
        s.append(texto(ANCHO / 2, y + 22 * k, r, tam=15))
    return "".join(s)


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
    W, H = ANCHO, 745
    cx, bw, bh = 300, 340, 60
    izq, carril = cx - bw / 2, 62
    regla = mezclar(LINEA, 0.22)
    desc = ("Diagrama de flujo de una partida. Se entra con el estado inicial s₀. "
            "En cada vuelta se pregunta si el estado s terminó, es decir, si está en "
            "S_F; si sí, la partida sale con U(s), lo que vale el resultado. Si no, "
            "Pl(s) dice a quién le toca, A(s) qué jugadas puede hacer, el jugador "
            "elige una jugada a, y T(s, a) da el nuevo estado, con el que se vuelve "
            "arriba. La caja de elegir está resaltada: es la única que no dan las "
            "reglas, y es lo que queremos decidir.")
    titulo = "Una partida, vuelta por vuelta"
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=22, peso="700")]

    # Entrada: el estado inicial.
    out.append(caja(cx - 130, 58, 260, 44, relleno=mezclar(SERIE[0], 0.14),
                    borde=SERIE[0], radio=22))
    out.append(texto(cx, 87, "Empieza: s = s₀", tam=19, peso="700"))
    out.append(flecha(cx, 102, cx, 123, color=SUAVE, marcador="s"))

    def caja_regla(cy, r1, r2, resaltada=False, alto=bh):
        borde = ACENTO if resaltada else LINEA
        relleno = mezclar(ACENTO, 0.2) if resaltada else regla
        s = [caja(izq, cy - alto / 2, bw, alto, relleno=relleno, borde=borde,
                  grosor=4 if resaltada else 2)]
        s.append(texto(cx, cy - 5, r1, tam=19, peso="700"))
        s.append(texto_con_sub(cx, cy + 19, r2, color=ACENTO if resaltada else SUAVE,
                               tam=16, peso="700" if resaltada else "normal"))
        return "".join(s)

    ys = {"estado": 155, "rombo": 262, "pl": 369, "a": 456, "elige": 547, "t": 640}
    cajas = {clave: (r1, r2) for clave, r1, r2 in CICLO_CAJAS}

    out.append(caja_regla(ys["estado"], *cajas["estado"]))
    out.append(flecha(cx, ys["estado"] + bh / 2, cx, 208, color=SUAVE, marcador="s"))

    # La pregunta de los finales.
    yr, mx, my = ys["rombo"], 150, 52
    out.append(_rombo(cx, yr, mx, my, mezclar(SERIE[1], 0.16), mezclar(SERIE[1], 0.6)))
    out.append(texto(cx, yr - 5, "¿Terminó?", tam=19, peso="700"))
    out.append(texto_con_sub(cx, yr + 19, [("¿s ∈ S", False), ("F", True), ("?", False)],
                             color=SUAVE, tam=16))

    # Si terminó: sale con su utilidad.
    ux, uw, uh = 590, 180, 104
    out.append(flecha(cx + mx, yr, ux - uw / 2 - 4, yr, color=SUAVE, marcador="s"))
    out.append(texto(cx + mx + 20, yr - 10, "sí", tam=17, color=SUAVE, peso="700"))
    out.append(caja(ux - uw / 2 - 5, yr - uh / 2 - 5, uw + 10, uh + 10,
                    borde=COLOR_FINAL, grosor=2))
    out.append(caja(ux - uw / 2, yr - uh / 2, uw, uh, relleno=mezclar(COLOR_FINAL, 0.12),
                    borde=COLOR_FINAL, grosor=2))
    out.append(texto(ux, yr - 18, "Fin de la partida", tam=17, peso="700"))
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
    nx = izq + bw + 22
    for k, (renglon, peso) in enumerate([("Lo único que", "700"),
                                         ("no dan las reglas:", "700"),
                                         ("es lo que queremos", "normal"),
                                         ("decidir", "normal")]):
        out.append(texto(nx, ys["elige"] - 26 + 22 * k, renglon, tam=16, color=ACENTO,
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
    out.append(caja(110, ly - 12, 30, 22, relleno=regla, borde=LINEA, radio=5))
    out.append(texto(150, ly + 5, "lo contestan las reglas", tam=15, color=SUAVE,
                     anclaje="start"))
    out.append(caja(400, ly - 12, 30, 22, relleno=mezclar(ACENTO, 0.2), borde=ACENTO,
                    radio=5, grosor=3))
    out.append(texto(440, ly + 5, "lo decide el jugador", tam=15, color=SUAVE,
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


def _paso_1():
    W, H = ANCHO, 520
    titulo = PASOS_TITULO[1]
    desc = ("El estado inicial s₀ dibujado en grande: el tablero con tres peones "
            "blancos en la fila 1 y tres negros en la fila 3, y el turno de Blancas, "
            "que es MAX. El borde punteado indica que todavía no se calcularon sus jugadas.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    cx, cy, w, h = 205, 250, 270, 300
    out.append(nodo_svg(cx, cy, j.inicio(), "B", "s₀", expandido=False, w=w, h=h, celda=60))
    # Anotaciones a la derecha, con su flecha hacia la parte del nodo.
    notas = [
        (cy - 120, "Nombre del nodo: s₀,", "el estado inicial", cy - 128),
        (cy - 10, "El tablero τ: qué hay", "en cada casilla", cy - 20),
        (cy + 120, "El turno: mueve Blancas,", "así que Pl(s₀) = MAX", cy + 122),
    ]
    for ytxt, l1, l2, ydest in notas:
        out.append(flecha(440, ytxt - 5, cx + w / 2 + 8, ydest, color=SUAVE, marcador="s"))
        out.append(texto(450, ytxt - 6, l1, tam=16, anclaje="start"))
        out.append(texto(450, ytxt + 16, l2, tam=16, anclaje="start", color=SUAVE))
    out.append(nota_svg(H - 70, ["Borde punteado: el nodo existe, pero todavía",
                                 "no sabemos qué jugadas salen de él."]))
    out.append(cierre())
    return "".join(out)


def _paso_hijos(paso, previas, rotulo_padre, rotulos_hijos, notas):
    """Pasos 2 a 4: un padre arriba y sus hijos abajo."""
    W = ANCHO
    tp, pp = jugar(j.inicio(), "B", previas)
    hs = hijos(tp, pp)
    xs = {2: [W / 2], 3: [W / 2]}
    n = len(hs)
    paso_x = 210 if n == 3 else 260
    xs_hijos = [W / 2 + (k - (n - 1) / 2) * paso_x for k in range(n)]
    y_padre, y_hijo = 200, 500
    H = 790
    desc = (f"Arriba, {rotulo_padre}; abajo, sus {n} hijos: "
            + "; ".join(f"{nombre} lleva a un estado donde "
                        + tipo_de_nodo(t, p)[1].lower() for nombre, t, p in hs) + ".")
    titulo = PASOS_TITULO[paso]
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    destino = rotulo_padre if previas else "s₀"
    if previas:
        out.append(rastro_svg(68, previas, destino))
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
                            "Cada flecha llega a T(s₀, a). Ahora mueve Negras."])
    if paso == 3:
        return _paso_hijos(3, ["a1-a2"], "tras a1-a2",
                           {"b3-b2": "n1", "b3xa2": "tras b3xa2", "c3-c2": "tras c3-c2"},
                           ["Las mismas funciones A y T sirven para Negras:",
                            "3 respuestas, y en los hijos vuelve a mover Blancas."])
    return _paso_hijos(4, ["a1-a2", "b3-b2"], "n1",
                       {"c1-c2": "n2", "c1xb2": "n3"},
                       ["n2 es final: Negras no tiene jugada y gana Blancas.",
                        "Su número es U(n2) = +1. n3 todavía no se expande."])


# ------------------------------------------- el subgrafo completo de n1 ---

# (x, nivel) de cada nodo; el ancho cabe en ANCHO.
LUGARES_N1 = {1: (350, 0), 2: (130, 1), 3: (420, 1),
              4: (100, 2), 6: (390, 2), 13: (610, 2),
              5: (100, 3), 7: (250, 3), 11: (400, 3), 12: (550, 3),
              8: (250, 4), 9: (175, 5), 10: (325, 5)}
NODO_SUB, NODO_ALTO_SUB = 132, 146  # nodos del subgrafo


def jue_subgrafo_n1():
    """Los 13 estados alcanzables desde n1, con su jugador o su utilidad."""
    nodos = subgrafo_n1()
    W, y0, dy = ANCHO, 175, 228
    H = y0 + 5 * dy + 150
    finales = [n for n, (t, p, _, _) in nodos.items() if j.ganador(t, p)]
    desc = (f"El grafo completo desde n1, el estado tras a1-a2 y b3-b2: "
            f"{len(nodos)} nodos numerados n1 a n{len(nodos)} en el orden en que se recorren, "
            f"{len(finales)} de ellos finales con su utilidad. Las flechas llevan el nombre de la jugada.")
    titulo = "El grafo completo desde n1"
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(rastro_svg(70, CAMINO_N1, "n1"))
    for n, (t, p, padre, jugada) in nodos.items():
        if padre is None:
            continue
        x1, l1 = LUGARES_N1[padre]
        x2, l2 = LUGARES_N1[n]
        out.append(arista_svg(x1, y0 + l1 * dy, x2, y0 + l2 * dy, jugada, h=NODO_ALTO_SUB))
    for n, (t, p, _, _) in nodos.items():
        x, nivel = LUGARES_N1[n]
        out.append(nodo_svg(x, y0 + nivel * dy, t, p, f"n{n}", w=NODO_SUB, h=NODO_ALTO_SUB,
                            celda=21))
    out.append(leyenda_svg(H - 34, [("expandido", "con hijos"), ("final", "final, con su U")]))
    out.append(cierre())
    return "".join(out)


# ------------------------------------------------------ la transposicion ---

CAMINO_A = ["a1-a2", "b3-b2", "c1-c2"]
CAMINO_B = ["c1-c2", "b3-b2", "a1-a2"]
NODO_TR, NODO_ALTO_TR = 128, 146


def jue_transposicion():
    """Dos ordenes de jugadas, el mismo estado: dos nodos en el arbol y uno
    en el grafo."""
    W, y0, dy = ANCHO, 185, 228
    H = y0 + 3 * dy + 170
    final_a = jugar(j.inicio(), "B", CAMINO_A)
    final_b = jugar(j.inicio(), "B", CAMINO_B)
    assert final_a == final_b, "los dos caminos deben llegar al mismo estado"
    desc = ("Izquierda, árbol de partidas: los caminos a1-a2, b3-b2, c1-c2 y "
            "c1-c2, b3-b2, a1-a2 terminan en dos nodos con el mismo tablero, n2. "
            "Derecha, grafo de estados: los dos caminos llegan a un solo nodo.")
    titulo = "Dos caminos, el mismo estado"
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(texto(175, 84, "Árbol de partidas", tam=17, peso="700", color=SUAVE))
    out.append(texto(525, 84, "Grafo de estados", tam=17, peso="700", color=SUAVE))
    out.append(linea(350, 66, 350, H - 90, color=LINEA, grosor=1.5, guiones="4 6"))
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

    a1, n1_ = camino(175, 90, CAMINO_A, rotulos=("", "n1", "n2 (copia 1)"))
    a2, n2_ = camino(175, 260, CAMINO_B, rotulos=("", "", "n2 (copia 2)"))
    a3, n3_ = camino(525, 440, CAMINO_A, x_final=525, rotulos=("", "n1", ""))
    a4, n4_ = camino(525, 610, CAMINO_B, x_final=525)
    out += a1 + a2 + a3 + a4
    out.append(nodo_svg(175, y0, j.inicio(), "B", "s₀", **kw))
    out.append(nodo_svg(525, y0, j.inicio(), "B", "s₀", **kw))
    out += n1_ + n2_ + n3_ + n4_
    out.append(nodo_svg(525, y0 + 3 * dy, *final_a, "n2: un nodo", nuevo=True, **kw))
    out.append(nota_svg(H - 58, ["El estado no recuerda por qué camino se llegó:",
                                 "en el grafo es un solo nodo."]))
    out.append(cierre())
    return "".join(out)


DIAGRAMAS = {
    "jue-ciclo-partida": jue_ciclo_partida,
    **{f"jue-grafo-paso-{paso}": (lambda paso=paso: jue_grafo_paso(paso))
       for paso in PASOS_TITULO},
    "jue-subgrafo-n1": jue_subgrafo_n1,
    "jue-transposicion": jue_transposicion,
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
