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
             w=150, h=160, celda=24, renglones=None, color=None, orden=None, radio=10):
    """Un nodo: rotulo arriba, tablero al centro y su tipo en dos renglones.

    Borde doble: final. Borde punteado: existe pero aun no se expande.
    Borde grueso de acento: lo nuevo de este paso. `renglones` reemplaza los
    dos renglones de abajo (para escribir su valor), `color` el color de su
    tipo (para el nodo de azar) y `orden` dibuja en la esquina el numero de
    visita de un recorrido."""
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
    f = min(1.5, max(0.88, w / 150))  # la letra crece con el nodo
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


def arista_svg(x1, y1, x2, y2, rotulo, nueva=False, h=160, tenue=False):
    """Flecha del borde inferior del padre al superior del hijo, con el
    nombre de la jugada sobre la flecha. `tenue`: la jugada se conoce, pero
    su estado nunca se genera."""
    color = ACENTO if nueva else (LINEA if tenue else SUAVE)
    ya, yb = y1 + h / 2, y2 - h / 2 - 8
    if tenue:
        s = [linea(x1, ya, x2, yb, color=color, grosor=2, guiones="6 5")]
    else:
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
        ["n7 ya vale +1: Negras está obligada a jugar a3xb2 y luego",
         "gana Blancas. max{+1, +1, +1} = +1: las tres jugadas empatan."]),
    2: (3, "Paso 2 · Valorar n3: Negras toma el mínimo",
        ["min{+1, +1, −1} = −1. A Negras le basta una respuesta",
         "buena: c3xb2 deja a Blancas sin jugada."]),
    3: (1, "Paso 3 · Valorar n1: la jugada de Blancas",
        ["max{+1, −1} = +1, con c1-c2. Capturar en b2 pierde:",
         "Negras respondería c3xb2."]),
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
    W, H, y_padre, y_hijo = ANCHO, 800, 210, 510
    k = len(hijos_)
    paso_x = 210 if k == 3 else 260
    xs = [W / 2 + (i - (k - 1) / 2) * paso_x for i in range(k)]
    operacion = "máximo" if pp == "B" else "mínimo"
    desc = (f"{titulo}. Arriba, n{n}, donde {'mueve Blancas (MAX)' if pp == 'B' else 'mueve Negras (MIN)'}; "
            "abajo, sus hijos con su valor: "
            + "; ".join(f"{nodos[m][3]} lleva a n{m}, que vale {fmt(valores[m])}" for m in hijos_)
            + f". El {operacion} es {fmt(valores[n])}, así que V(n{n}) = {fmt(valores[n])}; "
            "las jugadas que lo alcanzan van resaltadas.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(rastro_svg(68, camino_n1(n), f"n{n}"))
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
                              tenue=n in fantasmas))
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
    W, y0, dy = ANCHO, 175, 228
    H = y0 + 5 * dy + 150
    titulo = "El subgrafo de n1, resuelto"
    desc = ("El mismo grafo de n1 de la clase 1, con un valor en cada nodo: "
            + ", ".join(f"V(n{n}) = {fmt(v)}" for n, v in valores.items())
            + ". Van resaltadas las jugadas que alcanzan el valor de su padre: c1-c2 en n1, "
            "c3xb2 en n3 y las tres jugadas de n6, que empatan.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(rastro_svg(70, CAMINO_N1, "n1"))
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
    W, y0, dy = ANCHO, 175, 228
    H = y0 + 5 * dy + 150
    titulo = "MINIMAX a media ejecución"
    desc = ("El subgrafo de n1 en el momento en que MINIMAX empieza a valorar n8. "
            "En memoria solo está el camino n1, n3, n6, n7, n8, cada uno esperando a "
            "sus hijos con el mejor valor visto hasta ahora. n2 y n4 ya devolvieron "
            "+1 y se olvidaron, con n5. n9, n10, n11, n12 y n13 todavía no se generan.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(texto(W / 2, 70, "Empieza MINIMAX(n8). ¿Qué hay en memoria?", tam=15,
                     color=SUAVE))
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
            out.append(arista_svg(x1, y1, x2, y2, jugada, nueva=True, h=NODO_ALTO_SUB))
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
    out.append(caja(18, ly, 24, 16, borde=ACENTO, grosor=3, radio=4))
    out.append(texto(52, ly + 13, "en la pila: esperan", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(250, ly, 24, 16, borde=SUAVE, grosor=1.5, radio=4, guiones="2 4"))
    out.append(texto(284, ly + 13, "devolvió y se olvidó", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(480, ly, 24, 16, borde=LINEA, grosor=2, radio=4, guiones="5 3"))
    out.append(texto(514, ly + 13, "todavía no se genera", tam=13, color=SUAVE, anclaje="start"))
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
    W, H, y_padre, y_hijo = ANCHO, 800, 210, 510
    xs = [W / 2 + (i - 1) * 230 for i in range(3)]
    titulo = "Si Negras eligiera al azar en n3"
    desc = ("n3 dibujado como nodo de azar: nadie elige, cada una de las tres jugadas de "
            "Negras sale con probabilidad 1/3. Sus hijos valen "
            + ", ".join(f"n{m} = {fmt(valores[m])}" for m in hijos_)
            + f". El nodo vale su promedio, {fmt(promedio)}.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(rastro_svg(68, camino_n1(3), "n3"))
    for m, x in zip(hijos_, xs):
        out.append(arista_svg(W / 2, y_padre, x, y_hijo, f"{nodos[m][3]}: ⅓", h=190))
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
    out.append(caja(18, ly - 3, 30, 22, borde=COLOR_AZAR, grosor=2, radio=11))
    out.append(texto(58, ly + 13, "nodo de azar: esquinas redondas", tam=13, color=SUAVE,
                     anclaje="start"))
    out.append(caja(330, ly, 24, 16, borde=ACENTO, grosor=3, radio=4))
    out.append(texto(364, ly + 13, "se valora en este paso", tam=13, color=SUAVE,
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


def lugares_invertidos():
    """La geometria del subgrafo reflejada: de izquierda a derecha queda el
    orden de visita cuando todas las listas de jugadas se invierten."""
    return {n: (ANCHO - x, nivel) for n, (x, nivel) in LUGARES_N1.items()}


def jue_alfa_beta(invertir=False):
    """Alfa-beta desde n1: orden de visita, alfa y beta al llegar, lo que
    devuelve cada nodo, el corte y los nodos que nunca se generan."""
    nodos = subgrafo_n1()
    visitas, cortes = traza_n1(invertir)
    fantasmas = [n for n in nodos if n not in visitas]
    W, y0, dy = ANCHO, 190, 228
    H = y0 + 5 * dy + 150
    orden_txt = "invertido" if invertir else "fijo"
    titulo = f"Alfa-beta con el orden {orden_txt}: {len(visitas)} de {len(nodos)} nodos"
    corte_txt = "; ".join(f"corte {tipo} en n{padre}" for (padre, _), tipo in cortes.items())
    desc = (f"El subgrafo de n1 recorrido por alfa-beta con el orden {orden_txt}. "
            + " ".join(f"{orden}º n{n}: llega con α = {fmt(a)} y β = {fmt(b)} y devuelve {fmt(v)}."
                       for n, (orden, _, a, b, v) in sorted(visitas.items(), key=lambda x: x[1][0]))
            + f" {corte_txt}. Nunca se generan: "
            + ", ".join(f"n{n}" for n in fantasmas) + ".")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(texto(W / 2, 70, "Cada nodo: α y β al llegar, y lo que devuelve", tam=15,
                     color=SUAVE))

    def renglones(n, t, p):
        orden, tipo, a, b, v = visitas[n]
        if tipo == "final":
            return None
        return f"α {fmt(a)} · β {fmt(b)}", f"{tipo} · devuelve {fmt(v)}"

    etiquetas = {arista: f"corte {tipo}" for arista, tipo in cortes.items()}
    lugares = lugares_invertidos() if invertir else LUGARES_N1
    _dibujar_n1(out, lugares, y0, dy, renglones=renglones, fantasmas=fantasmas,
                ordenes={n: v[0] for n, v in visitas.items()}, etiquetas_corte=etiquetas)
    ly = H - 34
    out.append(f'<circle cx="30" cy="{ly + 8}" r="12" fill="{ACENTO}"/>')
    out.append(texto(30, ly + 13, "1º", tam=12, color=FONDO, peso="700"))
    out.append(texto(50, ly + 13, "orden de visita", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(240, ly, 24, 16, borde=LINEA, grosor=2, radio=4, guiones="5 3"))
    out.append(texto(274, ly + 13, "no se genera", tam=13, color=SUAVE, anclaje="start"))
    out.append(caja(440, ly - 3, 30, 22, borde=COLOR_FINAL, grosor=1.5, radio=5))
    out.append(caja(443, ly, 24, 16, borde=COLOR_FINAL, grosor=1.5, radio=4))
    out.append(texto(480, ly + 13, "final, con su U", tam=13, color=SUAVE, anclaje="start"))
    out.append(cierre())
    return "".join(out)


# ============================================================ clase 3 ===
#
# La posicion de la clase 3 en el tablero de 4x4: mueven Blancas. Las
# figuras de cortar y evaluar se dibujan sobre ella.

POSICION_C3 = "B..." + "..BB" + "..N." + "NN.."
N4 = 4


def hijos4(tablero, turno):
    return [(j.nombre_jugada(tablero, m, N4), j.mover(tablero, m), j.otro(turno))
            for m in j.jugadas(tablero, turno, N4)]


def ev(tablero):
    return j.evaluar_peones(tablero, N4)


def _nodo_corte(cx, cy, tablero, turno, rotulo, w=150, h=170, celda=19, nuevo=False):
    """Un nodo de corte: existe, pero la busqueda no lo expande; recibe EVAL.
    Lleva el borde punteado de «todavia no se expande» de la clase 1."""
    return nodo_svg(cx, cy, tablero, turno, rotulo, expandido=False, nuevo=nuevo, w=w, h=h,
                    celda=celda, renglones=("Nodo de corte", f"EVAL = {fmt(ev(tablero))}"))


def jue_c3_corte_prof_1():
    """Profundidad 1: las tres jugadas de Blancas y su EVAL. Gana la captura."""
    W, H = ANCHO, 660
    hs = hijos4(POSICION_C3, "B")
    valores = [ev(t) for _, t, _ in hs]
    mejor = max(valores)
    titulo = "Profundidad 1: mirar una jugada y evaluar"
    desc = ("La posición de la clase arriba, donde mueve Blancas. Sus tres jugadas llevan a "
            "nodos de corte, con borde punteado porque ahí la búsqueda se detiene: "
            + "; ".join(f"{nombre} da EVAL = {fmt(v)}" for (nombre, _, _), v in zip(hs, valores))
            + f". Blancas toma el máximo, {fmt(mejor)}: la captura, resaltada.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    y_raiz, y_hijo, xs = 175, 470, [130, 350, 570]
    for (nombre, t, p), x, v in zip(hs, xs, valores):
        out.append(arista_svg(W / 2, y_raiz, x, y_hijo, nombre, nueva=v == mejor, h=170))
    out.append(nodo_svg(W / 2, y_raiz, POSICION_C3, "B", "La posición", w=190, h=170, celda=19,
                        renglones=("Mueve Blancas · MAX", f"con corte: {fmt(mejor)}")))
    for (nombre, t, p), x in zip(hs, xs):
        out.append(_nodo_corte(x, y_hijo, t, p, nombre, nuevo=ev(t) == mejor))
    out.append(nota_svg(H - 60, ["d = 1 en la raíz: tras la jugada de Blancas queda d = 0,",
                                 "y la búsqueda estima con EVAL en vez de seguir."]))
    out.append(cierre())
    return "".join(out)


def jue_c3_corte_prof_2():
    """Profundidad 2: la jugada de Blancas, todas las respuestas de Negras y
    EVAL en las hojas. Negras toma el minimo; Blancas, el maximo."""
    W = ANCHO
    hs = hijos4(POSICION_C3, "B")
    nietos = [hijos4(t, p) for _, t, p in hs]
    total = sum(len(g) for g in nietos)
    paso = (W - 60) / total
    slots = [30 + paso / 2 + k * paso for k in range(total)]
    y_raiz, y_hijo, y_hoja = 175, 440, 650
    H = y_hoja + 150
    valores_hijo = [min(ev(t) for _, t, _ in g) for g in nietos]
    mejor = max(valores_hijo)
    titulo = "Profundidad 2: mirar también la respuesta"
    desc = ("La posición de la clase, sus tres jugadas y todas las respuestas de Negras, "
            "que son nodos de corte con su EVAL. "
            + " ".join(f"Tras {nombre}, Negras puede "
                       + ", ".join(f"{n2} ({fmt(ev(t2))})" for n2, t2, _ in g)
                       + f": el mínimo es {fmt(v)}."
                       for (nombre, _, _), g, v in zip(hs, nietos, valores_hijo))
            + f" Blancas toma el máximo, {fmt(mejor)}, con d2-d3.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
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
            elegida = ev(t2) == v
            out.append(flecha(x, y_hijo + 85, xh, y_hoja - hh / 2 - 8,
                              color=ACENTO if elegida else SUAVE, grosor=3 if elegida else 2,
                              marcador="p" if elegida else "s"))
    out.append(nodo_svg(W / 2, y_raiz, POSICION_C3, "B", "La posición", w=190, h=170, celda=19,
                        renglones=("Mueve Blancas · MAX", f"con corte: {fmt(mejor)}")))
    for (nombre, t, p), x, v in zip(hs, xs_hijo, valores_hijo):
        out.append(nodo_svg(x, y_hijo, t, p, nombre, w=150, h=170, celda=19, nuevo=v == mejor,
                            renglones=("Mueve Negras · MIN", f"mínimo: {fmt(v)}")))
    for g, mis, v in zip(nietos, hojas, valores_hijo):
        for (n2, t2, p2), xh in zip(g, mis):
            elegida = ev(t2) == v
            out.append(caja(xh - wh / 2, y_hoja - hh / 2, wh, hh, relleno=FONDO,
                            borde=ACENTO if elegida else LINEA, grosor=3 if elegida else 2,
                            guiones="7 5"))
            out.append(texto(xh, y_hoja - 10, n2, tam=14, peso="700", fuente=MONO))
            out.append(texto(xh, y_hoja + 20, fmt(ev(t2)), tam=18, peso="700",
                             color=ACENTO if elegida else TEXTO))
    out.append(texto(W / 2, y_hoja + hh / 2 + 32, "Hojas: nodos de corte, con su EVAL",
                     tam=14, color=SUAVE))
    out.append(cierre())
    return "".join(out)


def jue_c3_horizonte():
    """La captura a profundidad 1: lo que se ve antes del horizonte y la
    recaptura que queda detras."""
    W, H = ANCHO, 860
    nombre_c, t1, p1 = [h for h in hijos4(POSICION_C3, "B") if h[0] == "d2xc3"][0]
    nombre_r, t2, p2 = [h for h in hijos4(t1, p1) if "x" in h[0]][0]
    titulo = "El efecto horizonte"
    desc = (f"A profundidad 1, la búsqueda ve la captura {nombre_c} y evalúa en {fmt(ev(t1))}: "
            f"un peón de más. Una línea punteada marca el horizonte, donde se corta. Detrás, "
            f"sin que la búsqueda la vea, está la recaptura {nombre_r}, que deja EVAL = {fmt(ev(t2))}.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    x, y0, y1, y2, yh = 260, 175, 440, 720, 585
    out.append(arista_svg(x, y0, x, y1, nombre_c, nueva=True, h=170))
    out.append(nodo_svg(x, y0, POSICION_C3, "B", "La posición", w=190, h=170, celda=19,
                        renglones=("Mueve Blancas · MAX", f"EVAL = {fmt(ev(POSICION_C3))}")))
    out.append(_nodo_corte(x, y1, t1, p1, f"tras {nombre_c}", w=170, nuevo=True))
    out.append(linea(30, yh, W - 30, yh, color=ACENTO, grosor=3, guiones="12 8"))
    out.append(texto(W - 30, yh - 12, "horizonte: con d = 1 se corta aquí", tam=15,
                     color=ACENTO, peso="700", anclaje="end"))
    out.append(linea(x, y1 + 85, x, y2 - 93, color=LINEA, grosor=2, guiones="4 6"))
    out.append(texto(x + 12, (y1 + y2) / 2 + 52, nombre_r, tam=15, color=SUAVE, peso="700",
                     fuente=MONO, anclaje="start"))
    out.append(nodo_svg(x, y2, t2, p2, f"tras {nombre_r}", expandido=False, w=170, h=170, celda=19,
                        color=SUAVE, renglones=("No se ve", f"EVAL = {fmt(ev(t2))}")))
    nx = 400
    for k, (renglon, color, peso) in enumerate([
            ("Lo que la búsqueda ve:", TEXTO, "700"),
            (f"EVAL = {fmt(ev(t1))}, un peón de más.", TEXTO, "normal"),
            ("", TEXTO, "normal"),
            ("Lo que queda detrás:", SUAVE, "700"),
            (f"Negras recaptura y", SUAVE, "normal"),
            (f"EVAL baja a {fmt(ev(t2))}.", SUAVE, "normal")]):
        out.append(texto(nx, 400 + 24 * k if k < 3 else 650 + 24 * (k - 3), renglon, tam=16,
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
    termina la anterior, y cada una deja lista una jugada."""
    W, H = ANCHO, 560
    costos = [j.nodos_con_corte(POSICION_C3, "B", d, N4) for d in PROFUNDIDADES_RELOJ]
    total = sum(costos)
    x0, ancho = 60, W - 120
    esc = ancho / total
    titulo = "Profundizar mientras haya tiempo"
    listas = [jugada_lista(d) for d in PROFUNDIDADES_RELOJ]
    desc = ("Tres búsquedas seguidas sobre la posición de la clase, con d = 1, 2 y 3; el largo "
            "de cada barra es el número de nodos que genera: "
            + ", ".join(f"{c} con d = {d}" for d, c in zip(PROFUNDIDADES_RELOJ, costos))
            + ". Cada búsqueda completa deja lista una jugada: "
            + ", ".join(f"d = {d}: {n} ({fmt(v)})" for d, (n, v) in zip(PROFUNDIDADES_RELOJ, listas))
            + ". Si el reloj se acaba a media búsqueda, se entrega la jugada de la anterior.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    out.append(texto(W / 2, 64, "El largo de cada barra: nodos que genera esa búsqueda", tam=14,
                     color=SUAVE))
    inicio, ys = 0, []
    for k, (d, c, (nombre, v)) in enumerate(zip(PROFUNDIDADES_RELOJ, costos, listas)):
        y = 130 + 95 * k
        ys.append(y)
        xa = x0 + inicio * esc
        out.append(caja(xa, y, c * esc, 30, relleno=mezclar(SERIE[1], 0.35), borde=SERIE[1],
                        radio=5))
        out.append(texto(xa, y - 10, f"d = {d} · {c} nodos", tam=15, peso="700", anclaje="start"))
        lista = f"deja lista: {nombre}" + (" (gana)" if v == 100 else "")
        xt = xa + c * esc + 10
        if xt + 200 > W:
            out.append(texto(xa + c * esc, y + 52, lista, tam=15, color=SERIE[0], peso="700",
                             anclaje="end"))
        else:
            out.append(texto(xt, y + 21, lista, tam=15, color=SERIE[0], peso="700",
                             anclaje="start"))
        inicio += c
    # Dos relojes: uno que se acaba a media busqueda con d = 2 y otro con d = 3.
    # Cada linea empieza bajo el rotulo de la busqueda en curso, para no taparlo.
    marcas = [(costos[0] + costos[1] // 2, 1), (costos[0] + costos[1] + costos[2] // 2, 2)]
    yb = ys[-1] + 85
    for k, (t, ultima) in enumerate(marcas):
        x = x0 + t * esc
        out.append(linea(x, ys[ultima] - 8, x, yb, color=ACENTO, grosor=2, guiones="6 5"))
        out.append(f'<circle cx="{x:.1f}" cy="{yb + 14}" r="13" fill="{ACENTO}"/>')
        out.append(texto(round(x, 1), yb + 19, str(k + 1), tam=14, color=FONDO, peso="700"))
        entrega = listas[ultima - 1][0]
        out.append(texto(40, yb + 62 + 28 * k,
                         f"Reloj {k + 1}: se acaba durante d = {ultima + 1}, así que entrega {entrega}",
                         tam=15, color=ACENTO, peso="700", anclaje="start"))
    out.append(cierre())
    return "".join(out)


def jue_c3_mcts_pasos():
    """Las cuatro fases de una vuelta de MCTS, en cuatro paneles. Es un
    esquema: los numeros de cada nodo (victorias / simulaciones) son de
    ejemplo y solo muestran como cambian en la vuelta."""
    W, H = ANCHO, 940
    titulo = "Una vuelta de MCTS, en cuatro pasos"
    desc = ("Cuatro paneles con el mismo árbol; cada nodo dice victorias de MAX entre "
            "simulaciones. 1, selección: desde la raíz se baja por el camino resaltado, "
            "eligiendo en cada nodo al hijo con mejor puntaje para quien mueve ahí: MAX en la "
            "raíz, MIN en el nodo 3/6, que baja por 0/2, donde MAX ganó menos. 2, expansión: se agrega un hijo "
            "nuevo, 0/0. 3, simulación: desde ese hijo se juega una partida al azar hasta un "
            "final, que aquí gana MAX, U = +1. 4, retropropagación: el resultado sube por el "
            "camino y cada nodo suma una simulación y una victoria: 4/10 pasa a 5/11.")
    out = [marco(W, H, desc, titulo, desc), texto(W / 2, 36, titulo, tam=20, peso="700")]
    paneles = [("1 · Selección", "baja por el mejor puntaje"),
               ("2 · Expansión", "agrega un hijo nuevo"),
               ("3 · Simulación", "juega al azar hasta un final"),
               ("4 · Retropropagación", "sube el resultado")]
    rel = {"r": (0, 0), "a": (-55, 65), "b": (55, 65), "a1": (-95, 130), "a2": (-15, 130),
           "nuevo": (-15, 195)}
    camino = ["r", "a", "a2"]
    # La raiz es de MAX y sus hijos, de MIN: MIN baja por el hijo donde MAX
    # gana menos (a2, 0/2), como pide UCT con el signo cambiado. Cada cuenta
    # suma las de sus hijos mas la simulacion que se hizo desde el propio nodo.
    antes = {"r": "4/10", "a": "3/6", "b": "1/4", "a1": "2/3", "a2": "0/2", "nuevo": "0/0"}
    despues = {"r": "5/11", "a": "4/7", "b": "1/4", "a1": "2/3", "a2": "1/3", "nuevo": "1/1"}
    aristas = [("r", "a"), ("r", "b"), ("a", "a1"), ("a", "a2"), ("a2", "nuevo")]
    pw, ph = 325, 400
    for k, (nombre, sub) in enumerate(paneles):
        px, py = 17 + (k % 2) * (pw + 16), 66 + (k // 2) * (ph + 16)
        out.append(caja(px, py, pw, ph, relleno=mezclar(LINEA, 0.12), borde=LINEA, radio=12))
        out.append(texto(px + pw / 2, py + 32, nombre, tam=19, peso="700"))
        out.append(texto(px + pw / 2, py + 56, sub, tam=15, color=SUAVE))
        cx, cy = px + pw / 2 + 15, py + 105
        pos = {n: (cx + dx, cy + dy) for n, (dx, dy) in rel.items()}
        visibles = [n for n in rel if k >= 1 or n != "nuevo"]
        resaltados = {0: set(camino), 1: {"nuevo"}, 2: {"nuevo"}, 3: set(camino) | {"nuevo"}}[k]
        for u, v in aristas:
            if v not in visibles:
                continue
            fuerte = (k in (0, 3) and u in resaltados and v in resaltados) or \
                     (k == 1 and v == "nuevo")
            out.append(linea(*pos[u], *pos[v], color=ACENTO if fuerte else SUAVE,
                             grosor=3 if fuerte else 2))
        for n in visibles:
            x, y = pos[n]
            fuerte = n in resaltados
            out.append(f'<circle cx="{x}" cy="{y}" r="24" fill="{FONDO}" '
                       f'stroke="{ACENTO if fuerte else SERIE[1]}" stroke-width="{3 if fuerte else 2}"/>')
            etiqueta = (despues if k == 3 else antes)[n]
            out.append(texto(x, y + 5, etiqueta, tam=14, peso="700",
                             color=ACENTO if (k == 3 and fuerte) else TEXTO))
        if k == 2:
            x, y = pos["nuevo"]
            pts = " ".join(f"{x + (10 if i % 2 else -10):.0f},{y + 26 + 9 * i:.0f}" for i in range(6))
            out.append(f'<polyline points="{pts}" fill="none" stroke="{ACENTO}" stroke-width="2"/>')
            out.append(caja(x - 45, y + 76, 90, 28, borde=COLOR_FINAL, radio=6, grosor=2))
            out.append(texto(x, y + 96, "U = +1", tam=15, color=COLOR_FINAL, peso="700"))
        if k == 3:
            for n in ["nuevo", "a2", "a", "r"]:
                x, y = pos[n]
                out.append(flecha(x + 38, y + 14, x + 38, y - 12, color=ACENTO, grosor=2))
            out.append(texto(px + pw / 2, py + ph - 22, "el camino suma 1 victoria y 1 simulación",
                             tam=13, color=SUAVE))
        if k == 0:
            out.append(texto(px + pw / 2, py + ph - 22, "el árbol que ya se construyó", tam=13,
                             color=SUAVE))
    out.append(texto(W / 2, H - 14, "En cada nodo: victorias de MAX / simulaciones que pasaron por él",
                     tam=14, color=SUAVE))
    out.append(cierre())
    return "".join(out)


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
    "jue-c3-corte-prof-1": jue_c3_corte_prof_1,
    "jue-c3-corte-prof-2": jue_c3_corte_prof_2,
    "jue-c3-horizonte": jue_c3_horizonte,
    "jue-c3-profundizacion": jue_c3_profundizacion,
    "jue-c3-mcts-pasos": jue_c3_mcts_pasos,
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
