"""Genera los diagramas SVG de la unidad de cadenas de Markov (unidad 8).

Mismo patron que gen_juegos.py: una funcion por diagrama que devuelve una
cadena SVG completa, un catalogo DIAGRAMAS que el generador y su prueba
comparten, y las primitivas de dibujo (marco, texto, caja, flecha...) de
gen_optimizacion para compartir paleta y convenciones.

Ningun numero se escribe a mano: cada cifra (las de la frase, las del corpus
y las simuladas) sale de tools/markov.py. Todas las figuras miden ANCHO =
300 px (lo que no cabe crece hacia abajo), con letra de 12 px o mas.

contenido(nombre) devuelve el SVG sin escribirlo: test_gen_markov.py lo
compara byte a byte con el archivo comiteado (si alguien edita el SVG a
mano, la prueba falla con «corre el generador»).

Los ids llevan prefijo "mkv-c1-" (clase 1) o "mkv-c2-" (clase 2): los ids de objeto numerado son unicos en
todo el curso.
"""
import math
import sys
from fractions import Fraction as F
from xml.sax.saxutils import escape

import markov as m
from gen_optimizacion import (ACENTO, FONDO, FUENTE, LINEA, SERIE, SUAVE, TEXTO,
                              _rombo, caja, cierre, flecha, linea, marco, mezclar)
from unidades import RAIZ

ASSETS = RAIZ / "course/8_markov/_assets"

ANCHO = 300
X_PIE = 16          # margen izquierdo del titulo, del pie y de la leyenda
COLOR_V = SERIE[1]  # vocal: azul claro (con circulo y la letra V)
COLOR_C = SERIE[2]  # consonante: amarillo (con cuadrado y la letra C)
COLOR_REAL = SERIE[0]


# -------------------------------------------------------------- formato ---

def fr(x):
    """Una fraccion como la escriben las paginas: 2/11, 1 (si es entera)."""
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x, cifras=3):
    return f"{float(x):.{cifras}f}"


def miles(n):
    """20 000: miles separados por espacio."""
    return f"{int(n):,}".replace(",", " ")


def pct(x, cifras=3):
    v = float(x) * 100
    return "0 %" if v == 0 else f"{v:.{cifras}f} %"


def texto(x, y, s, color=TEXTO, tam=14, anclaje="middle", peso="normal"):
    """Como gen_optimizacion.texto, con coordenadas redondeadas a 0.1."""
    return (f'<text x="{_n(x)}" y="{_n(y)}" fill="{color}" font-family="{FUENTE}" '
            f'font-size="{tam}" font-weight="{peso}" text-anchor="{anclaje}">'
            f"{escape(s)}</text>")


def _n(v):
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v)


def girado(x, y, s, angulo=-90, color=SUAVE, tam=13):
    return (f'<text x="{_n(x)}" y="{_n(y)}" fill="{color}" font-family="{FUENTE}" '
            f'font-size="{tam}" font-weight="700" text-anchor="middle" '
            f'transform="rotate({angulo} {_n(x)} {_n(y)})">{escape(s)}</text>')


def encabezado(out, renglones, y=30):
    """Primer renglon a 18 en negritas; los demas a 14 en el tono suave.
    Devuelve la y del primer renglon libre."""
    for k, r in enumerate(renglones):
        out.append(texto(X_PIE, y, r, tam=18 if k == 0 else 14, peso="700",
                         anclaje="start", color=TEXTO if k == 0 else SUAVE))
        y += 24 if k == 0 else 19
    return y


def pie(out, y, renglones, tam=13, color=SUAVE):
    for r in renglones:
        out.append(texto(X_PIE, y, r, tam=tam, anclaje="start", color=color))
        y += round(tam * 1.5)
    return y


def svg(titulo, desc, out, alto):
    nombre = " ".join(titulo)
    return "".join([marco(ANCHO, round(alto), desc, nombre, desc)] + out + [cierre()])


def _flecha(x1, y1, x2, y2, color=SUAVE):
    return flecha(_n(x1), _n(y1), _n(x2), _n(y2), color=color, grosor=2,
                  marcador="s" if color == SUAVE else "p")


# ------------------------------------------------- diagramas de flujo ---
#
# «…, en palabras» (plan de unidad §3.2), como jue-c3-rx-flujo-*: cajas con
# verbos cortos, una decision por rombo, salida explicita. Una columna:
# las cajas de FL_X0 a FL_X1; todas las flechas bajan por FL_CX (el eje del
# rombo); las vueltas suben por el carril izquierdo FL_CARRIL.

FL_X0, FL_X1 = 40, 284
FL_CX, FL_MX = 112, 70
FL_LADO_X0 = 204
FL_CARRIL = 22
FL_GAP = 34


FL_CARRIL_DER = 293


def _flujo(titulo, pasos, vueltas=(), notas=(), salidas=()):
    """pasos: dicts con «caja» (renglones; el primero en negritas; fin=True
    en la salida) o «rombo» (renglones), «abajo» (rotulo de la salida de
    abajo) y «lado» (rotulo, renglones): caja a la derecha que baja a la
    entrada del paso siguiente. vueltas: [(desde, hasta, rotulo)] suben por
    el carril izquierdo. salidas: [(rombo, hasta, rotulo)] bajan por el
    carril derecho desde la punta del rombo hasta un paso posterior, que
    lleva sin_flecha=True si no se llega a el desde el anterior."""
    out = []
    y = encabezado(out, titulo) + 8
    geo = []
    for k, p in enumerate(pasos):
        if k and not p.get("sin_flecha"):
            y0 = y - FL_GAP
            out.append(_flecha(FL_CX, y0, FL_CX, y - 3))
            ant = pasos[k - 1]
            if "rombo" in ant and ant.get("abajo"):
                out.append(texto(FL_CX + 8, y0 + 19, ant["abajo"], tam=13, color=SUAVE,
                                 anclaje="start", peso="700"))
        if "caja" in p:
            rs = p["caja"]
            h = 16 + 20 * len(rs)
            fin = p.get("fin")
            out.append(caja(FL_X0, _n(y), FL_X1 - FL_X0, h,
                            relleno=mezclar(ACENTO if fin else LINEA, 0.14 if fin else 0.18),
                            borde=ACENTO if fin else SUAVE, grosor=2.5 if fin else 1.5))
            for i, r in enumerate(rs):
                out.append(texto(FL_X0 + 10, y + 23 + 20 * i, r, tam=14,
                                 peso="700" if i == 0 else "normal", anclaje="start"))
            geo.append(("caja", y, y + h / 2))
            y += h + FL_GAP
        else:
            rs = p["rombo"]
            my = 26 + 9 * len(rs)
            cy = y + my
            out.append(_rombo(FL_CX, round(cy, 1), FL_MX, my, mezclar(COLOR_V, 0.08),
                              borde=COLOR_V))
            for i, r in enumerate(rs):
                out.append(texto(FL_CX, cy + 5 - 9 * (len(rs) - 1) + 18 * i, r, tam=14,
                                 peso="700"))
            if p.get("lado"):
                rot, lineas = p["lado"]
                hl = 12 + 18 * len(lineas)
                out.append(_flecha(FL_CX + FL_MX, cy, FL_LADO_X0 - 3, cy))
                out.append(texto((FL_CX + FL_MX + FL_LADO_X0) / 2, cy - 15, rot, tam=13,
                                 color=SUAVE, peso="700"))
                out.append(caja(FL_LADO_X0, _n(cy - hl / 2), FL_X1 - FL_LADO_X0, _n(hl),
                                relleno=mezclar(COLOR_REAL, 0.08), borde=COLOR_REAL,
                                grosor=1.5))
                for i, r in enumerate(lineas):
                    out.append(texto((FL_LADO_X0 + FL_X1) / 2, cy - hl / 2 + 19 + 18 * i, r,
                                     tam=13))
                # baja a la entrada del paso siguiente
                xb = (FL_LADO_X0 + FL_X1) / 2
                out.append(_flecha(xb, cy + hl / 2, xb, y + 2 * my + FL_GAP - 3))
            geo.append(("rombo", y, cy))
            y += 2 * my + FL_GAP
    for desde, hasta, rot in vueltas:
        tipo_a, _, ya = geo[desde]
        tipo_b, _, yb = geo[hasta]
        xa = FL_CX - FL_MX if tipo_a == "rombo" else FL_X0
        xb = FL_CX - FL_MX if tipo_b == "rombo" else FL_X0
        out.append(f'<polyline points="{_n(xa)},{_n(ya)} {FL_CARRIL},{_n(ya)} '
                   f'{FL_CARRIL},{_n(yb)}" fill="none" stroke="{SUAVE}" stroke-width="2"/>')
        out.append(_flecha(FL_CARRIL, yb, xb - 3, yb))
        out.append(girado(FL_CARRIL - 8, (ya + yb) / 2, rot))
    for desde, hasta, rot in salidas:
        _, _, ya = geo[desde]
        _, _, yb = geo[hasta]
        xa = FL_CX + FL_MX
        out.append(f'<polyline points="{_n(xa)},{_n(ya)} {FL_CARRIL_DER},{_n(ya)} '
                   f'{FL_CARRIL_DER},{_n(yb)}" fill="none" stroke="{SUAVE}" stroke-width="2"/>')
        out.append(_flecha(FL_CARRIL_DER, yb, FL_X1 + 3, yb))
        out.append(texto(xa + 10, ya - 8, rot, tam=13, color=SUAVE, anclaje="start",
                         peso="700"))
    y = y - FL_GAP + 26
    if notas:
        y = pie(out, y, notas)
    return out, y - 8


def _desc_flujo(nombre, pasos, vueltas, notas=(), salidas=()):
    partes = []
    for k, p in enumerate(pasos):
        if "caja" in p:
            partes.append(f"{k + 1}: " + " ".join(p["caja"]) + ".")
        else:
            s = f"{k + 1}, pregunta: " + " ".join(p["rombo"])
            if p.get("lado"):
                s += f" Si {p['lado'][0]}: " + " ".join(p["lado"][1]) + ", y sigue abajo."
            if p.get("abajo"):
                s += f" Si {p['abajo']}, sigue abajo."
            partes.append(s)
    for desde, hasta, rot in vueltas:
        partes.append(f"Desde el paso {desde + 1}, si {rot}, vuelve al paso {hasta + 1}.")
    for desde, hasta, rot in salidas:
        partes.append(f"Desde el paso {desde + 1}, si {rot}, salta al paso {hasta + 1}.")
    return (f"Diagrama de flujo de {nombre}, en palabras. " + " ".join(partes)
            + (" " + " ".join(notas) if notas else ""))


FLUJOS = {
    "muestrear": dict(
        nombre="muestrear una fila",
        titulo=["Muestrear una fila,", "en palabras"],
        pasos=[{"caja": ["Sortea u", "uniforme entre 0 y 1"]},
               {"caja": ["Empieza en el primer", "estado, con suma = 0"]},
               {"caja": ["Suma la probabilidad", "de ese estado"]},
               {"rombo": ["¿u es menor", "que la suma?"], "abajo": "sí"},
               {"caja": ["El siguiente estado", "es ese estado"], "fin": True}],
        vueltas=[(3, 2, "no: el que sigue")],
        notas=["Un solo u por paso. Es lo que usa", "toda simulación de la clase."]),
    "contar": dict(
        nombre="contar transiciones",
        titulo=["Contar, en palabras", "una pasada por el texto"],
        pasos=[{"caja": ["Empieza con todos", "los conteos en 0"]},
               {"caja": ["Toma el siguiente par", "(actual, siguiente)"]},
               {"caja": ["Suma 1 a N(s, s′)", "y 1 a N(s)"]},
               {"rombo": ["¿Quedan", "pares?"], "abajo": "no"},
               {"caja": ["Divide cada fila", "entre su total N(s)", "y devuelve N, N(s), P̂"],
                "fin": True}],
        vueltas=[(3, 1, "sí: el siguiente")],
        notas=["Una fila con N(s) = 0 queda sin", "estimar: los datos no la fijan."]),
    "predecir": dict(
        nombre="predecir",
        titulo=["Predecir, en palabras", "t multiplicaciones"],
        # pregunta antes de multiplicar: con t = 0 devuelve μ₀
        pasos=[{"caja": ["Empieza con μ₀", "(un vector fila)"]},
               {"rombo": ["¿Faltan", "pasos?"], "abajo": "sí"},
               {"caja": ["Multiplica por P̂:", "μ ← μ P̂"]},
               {"caja": ["Devuelve μₜ"], "fin": True, "sin_flecha": True}],
        vueltas=[(2, 1, "otro paso")],
        salidas=[(1, 3, "no")],
        notas=["Cada paso cuesta k² productos", "con k estados."]),
    "generar": dict(
        nombre="generar texto",
        titulo=["Generar, en palabras", "con memoria h"],
        # un ciclo «mientras»: con largo = 0 no escribe nada, como el
        # pseudocódigo de la página
        pasos=[{"caja": ["Empieza con un", "contexto de h símbolos"]},
               {"rombo": ["¿Faltan", "símbolos?"], "abajo": "sí"},
               {"rombo": ["¿Se vio el", "contexto?"], "abajo": "sí",
                "lado": ("no", ["usa la fila", "suavizada"])},
               {"caja": ["Muestrea su fila", "con un u nuevo"]},
               {"caja": ["Escribe el símbolo", "y desliza el contexto"]},
               {"caja": ["Devuelve el texto"], "fin": True, "sin_flecha": True}],
        vueltas=[(4, 1, "otro símbolo")],
        salidas=[(1, 5, "no")],
        notas=["Un contexto nunca visto no se", "reinicia: su fila suavizada da",
               "1/|Σ| a cada símbolo."]),
}


def flujo(clave):
    f = FLUJOS[clave]
    salidas = f.get("salidas", ())
    out, alto = _flujo(f["titulo"], f["pasos"], f["vueltas"], f["notas"], salidas)
    return svg(f["titulo"], _desc_flujo(f["nombre"], f["pasos"], f["vueltas"], f["notas"],
                                        salidas), out, alto)


# ------------------------------------------------------- el grafo V/C ---

def _nodo(cx, cy, letra, r=26, nuevo=False):
    color = COLOR_V if letra == "V" else COLOR_C
    if letra == "V":
        forma = (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{r}" fill="{mezclar(color, 0.18)}" '
                 f'stroke="{color}" stroke-width="{3 if nuevo else 2}"/>')
    else:
        forma = (f'<rect x="{_n(cx - r)}" y="{_n(cy - r)}" width="{2 * r}" height="{2 * r}" '
                 f'rx="6" fill="{mezclar(color, 0.18)}" stroke="{color}" '
                 f'stroke-width="{3 if nuevo else 2}"/>')
    return forma + texto(cx, cy + 7, letra, tam=20, peso="700")


def _curva(d, color=SUAVE):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" '
            f'marker-end="url(#s)"/>')


def mkv_c1_grafo_vc():
    P = m.matriz_estimada(m.frase_vc())
    (vv, vc), (cv, cc) = [[fr(x) for x in f] for f in P]
    titulo = ["El grafo de la frase", "V = vocal, C = consonante"]
    out = []
    y = encabezado(out, titulo)
    xv, xc, yn, r = 92, 208, y + 108, 26
    # lazos: salen arriba a la izquierda y vuelven arriba a la derecha
    for cx, rot in ((xv, vv), (xc, cc)):
        x0, y0 = cx - 13, yn - 22.5
        x1, y1 = cx + 15, yn - 23
        out.append(_curva(f"M {_n(x0)} {_n(y0)} C {_n(cx - 42)} {_n(yn - 82)} "
                          f"{_n(cx + 42)} {_n(yn - 82)} {_n(x1)} {_n(y1)}"))
        out.append(texto(cx, yn - 76, rot, tam=16, peso="700"))
    # V -> C por arriba, C -> V por abajo
    out.append(_curva(f"M {xv + 24} {_n(yn - 10)} Q {(xv + xc) / 2:g} {_n(yn - 38)} "
                      f"{xc - 28} {_n(yn - 10)}"))
    out.append(texto((xv + xc) / 2, yn - 32, vc, tam=16, peso="700"))
    out.append(_curva(f"M {xc - 24} {_n(yn + 10)} Q {(xv + xc) / 2:g} {_n(yn + 38)} "
                      f"{xv + 28} {_n(yn + 10)}"))
    out.append(texto((xv + xc) / 2, yn + 44, cv, tam=16, peso="700"))
    out.append(_nodo(xv, yn, "V"))
    out.append(_nodo(xc, yn, "C"))
    y = pie(out, yn + 80, ["Una flecha por cada entrada de P̂;",
                           "las de una misma salida suman 1:",
                           f"desde V, {vv} + {vc} = 1;",
                           f"desde C, {cv} + {cc} = 1."])
    desc = (f"Grafo de dos estados, V (vocal) y C (consonante), con la matriz estimada "
            f"de la frase «{m.FRASE}». Desde V: a V con {vv} (lazo) y a C con {vc}. "
            f"Desde C: a V con {cv} y a C con {cc} (lazo). Cada fila suma 1.")
    return svg(titulo, desc, out, y)


# ------------------------------------------------- el arbol de 2 pasos ---

def mkv_c1_arbol_2_pasos():
    P = m.matriz_estimada(m.frase_vc())
    idx = {"V": 0, "C": 1}
    hojas = m.arbol_dos_pasos(P, "C")
    pv2 = hojas[("V", "V")] + hojas[("C", "V")]
    assert pv2 == m.predecir(P, m.MU0_C, 2)[0]
    titulo = ["Dos pasos desde C", "con la matriz de la frase"]
    out = []
    y = encabezado(out, titulo)
    y_raiz, y1, y2 = y + 34, y + 124, y + 220
    x1 = {"V": 80, "C": 220}
    x2 = {("V", "V"): 40, ("V", "C"): 120, ("C", "V"): 180, ("C", "C"): 260}
    out.append(texto(150, y_raiz - 26, "S₀ = C", tam=13, color=SUAVE, peso="700"))
    for a in "VC":
        out.append(linea(150, _n(y_raiz + 18), x1[a], _n(y1 - 18), color=SUAVE))
        lado = -1 if a == "V" else 1
        out.append(texto((150 + x1[a]) / 2 + 14 * lado, (y_raiz + y1) / 2,
                         fr(P[idx["C"]][idx[a]]), tam=15, peso="700",
                         anclaje="end" if a == "V" else "start"))
        for b in "VC":
            out.append(linea(x1[a], _n(y1 + 18), x2[(a, b)], _n(y2 - 16), color=SUAVE))
            lado = -1 if b == "V" else 1
            out.append(texto((x1[a] + x2[(a, b)]) / 2 + 7 * lado, (y1 + y2) / 2 + 2,
                             fr(P[idx[a]][idx[b]]), tam=14, peso="700",
                             anclaje="end" if b == "V" else "start"))
    out.append(_nodo(150, y_raiz, "C", r=18))
    for a in "VC":
        out.append(_nodo(x1[a], y1, a, r=18))
    for (a, b), p in hojas.items():
        out.append(_nodo(x2[(a, b)], y2, b, r=16, nuevo=(b == "V")))
        out.append(texto(x2[(a, b)], y2 + 38, fr(p), tam=14, peso="700",
                         color=TEXTO if b == "V" else SUAVE))
    out.append(texto(X_PIE, y2 - 18, "S₂", tam=13, color=SUAVE, peso="700", anclaje="start"))
    out.append(texto(X_PIE, y1 + 5, "S₁", tam=13, color=SUAVE, peso="700", anclaje="start"))
    filas = [(a, b) for a in "VC" for b in "VC"]
    y = pie(out, y2 + 70, ["Bajo cada hoja, su camino: el producto",
                           "de sus dos flechas. Las hojas V",
                           f"(borde grueso) suman Pr(S₂ = V) =",
                           f"{fr(hojas[('V', 'V')])} + {fr(hojas[('C', 'V')])} = {fr(pv2)}."],
            tam=13, color=TEXTO)
    desc = ("Árbol de dos pasos desde C con la matriz de la frase. Primer paso: a V con "
            f"{fr(P[1][0])}, a C con {fr(P[1][1])}. Desde V: a V con {fr(P[0][0])}, a C con "
            f"{fr(P[0][1])}; desde C: a V con {fr(P[1][0])}, a C con {fr(P[1][1])}. "
            "Caminos: " + "; ".join(f"C, {a}, {b}: {fr(hojas[(a, b)])}" for a, b in filas)
            + f". Pr(S₂ = V) = {fr(hojas[('V', 'V')])} + {fr(hojas[('C', 'V')])} = {fr(pv2)}.")
    return svg(titulo, desc, out, y)


# --------------------------------------------------------- graficas ---

def _marca(forma, x, y, color, r=4.5):
    if forma == "circulo":
        return (f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{r}" fill="{FONDO}" '
                f'stroke="{color}" stroke-width="2"/>')
    if forma == "cuadro":
        return (f'<rect x="{_n(x - r)}" y="{_n(y - r)}" width="{_n(2 * r)}" '
                f'height="{_n(2 * r)}" fill="{color}" stroke="{color}" stroke-width="1"/>')
    if forma == "rombo":
        return (f'<polygon points="{_n(x)},{_n(y - r - 1)} {_n(x + r + 1)},{_n(y)} '
                f'{_n(x)},{_n(y + r + 1)} {_n(x - r - 1)},{_n(y)}" fill="{FONDO}" '
                f'stroke="{color}" stroke-width="2"/>')
    if forma == "triangulo":
        return (f'<polygon points="{_n(x)},{_n(y - r - 1)} {_n(x + r + 1)},{_n(y + r)} '
                f'{_n(x - r - 1)},{_n(y + r)}" fill="{color}" stroke="{color}" '
                f'stroke-width="1"/>')
    raise ValueError(forma)


def _polilinea(puntos, color, guiones=None, grosor=2):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    pts = " ".join(f"{_n(x)},{_n(y)}" for x, y in puntos)
    return (f'<polyline points="{pts}" fill="none" stroke="{color}" '
            f'stroke-width="{grosor}"{trazo}/>')


def _leyenda(out, y, items):
    """items: [(dibujo(x, y) -> svg, texto)]: una muestra de 26 px y su texto,
    un renglon por item."""
    for dibujo, rotulo in items:
        out.append(dibujo(X_PIE + 13, y - 4))
        out.append(texto(X_PIE + 34, y, rotulo, tam=13, anclaje="start"))
        y += 20
    return y


# ------------------------------------------------------------- mu-t ---

MU_X0, MU_X1 = 64, 276


def mkv_c1_mu_t():
    datos = m.mu_t_corpus()
    n = 10_000
    T = len(datos["V"]["cuenta"]) - 1
    titulo = ["La probabilidad de vocal,", "paso a paso (corpus)"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V)
         + _marca("circulo", x, yy, COLOR_V), "desde V: cuenta y réplicas"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_C, "5 4")
         + _marca("cuadro", x, yy, COLOR_C, r=4), "desde C: cuenta y réplicas"),
    ])
    out.append(texto(X_PIE, y + 6, "línea: la cuenta μ₀P̂ᵗ; marca: fracción",
                     tam=13, anclaje="start", color=SUAVE))
    out.append(texto(X_PIE, y + 25, f"de {miles(n)} réplicas en V en el paso t",
                     tam=13, anclaje="start", color=SUAVE))
    # panel de arriba: Pr(S_t = V) de 0 a 1
    top, alto = y + 66, 150

    def px(t):
        return MU_X0 + (MU_X1 - MU_X0) * t / T

    def py(p):
        return top + alto * (1 - p)
    out.append(texto(X_PIE, top - 10, "Pr(Sₜ = V)", tam=13, anclaje="start", peso="700"))
    for v in (0, 0.5, 1):
        out.append(linea(MU_X0, _n(py(v)), MU_X1, _n(py(v)), color=mezclar(LINEA, 0.5),
                         grosor=1))
        out.append(texto(MU_X0 - 12, py(v) + 4, f"{v:g}", tam=12, anclaje="end", color=SUAVE))
    for inicio, color, forma, guiones in (("V", COLOR_V, "circulo", None),
                                          ("C", COLOR_C, "cuadro", "5 4")):
        d = datos[inicio]
        out.append(_polilinea([(px(t), py(p)) for t, p in enumerate(d["cuenta"])], color,
                              guiones))
        for t, p in enumerate(d["simulada"]):
            out.append(_marca(forma, px(t), py(p), color, r=4.5 if forma == "circulo" else 4))
    # panel de abajo: simulada - cuenta, con la franja de 2 errores estandar
    ee = max(m.error_estandar(p, n) for d in datos.values() for p in d["cuenta"])
    tope = 0.02
    top2, alto2 = top + alto + 52, 110

    def py2(v):
        return top2 + alto2 * (tope - v) / (2 * tope)
    out.append(texto(X_PIE, top2 - 10, "réplicas − cuenta", tam=13, anclaje="start",
                     peso="700"))
    banda = 2 * ee
    out.append(f'<rect x="{MU_X0}" y="{_n(py2(banda))}" width="{MU_X1 - MU_X0}" '
               f'height="{_n(py2(-banda) - py2(banda))}" fill="{mezclar(ACENTO, 0.16)}"/>')
    for v in (-0.02, -0.01, 0, 0.01, 0.02):
        out.append(linea(MU_X0, _n(py2(v)), MU_X1, _n(py2(v)),
                         color=SUAVE if v == 0 else mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(MU_X0 - 12, py2(v) + 4, f"{v:+.2f}".replace("-", "−") if v else "0",
                         tam=12, anclaje="end", color=SUAVE))
    for inicio, color, forma in (("V", COLOR_V, "circulo"), ("C", COLOR_C, "cuadro")):
        d = datos[inicio]
        for t in range(T + 1):
            dx = -4 if inicio == "V" else 4
            out.append(_marca(forma, px(t) + dx, py2(d["simulada"][t] - d["cuenta"][t]), color,
                              r=4 if forma == "circulo" else 3.5))
    for t in range(T + 1):
        out.append(texto(px(t), top2 + alto2 + 18, str(t), tam=12, color=SUAVE))
    out.append(texto((MU_X0 + MU_X1) / 2, top2 + alto2 + 38, "paso t", tam=13, peso="700"))
    peor, peor_z = m.diferencia_maxima_mu_t()
    y = pie(out, top2 + alto2 + 62, [
        f"Franja: ±{dec(banda)}, dos errores estándar",
        "en el peor caso (p = 0.5). La mayor",
        f"diferencia: {dec(peor)}, unos {peor_z:.1f} errores",
        "estándar: en el borde de la franja."])
    desc = ("Probabilidad de estar en V en el paso t, de t = 0 a 8, con la matriz del corpus. "
            "Arriba, la cuenta μ₀P̂ᵗ (línea) y la fracción de "
            f"{miles(n)} réplicas en V (marcas). Desde V: cuenta "
            + ", ".join(dec(p) for p in datos["V"]["cuenta"]) + "; réplicas "
            + ", ".join(dec(p) for p in datos["V"]["simulada"]) + ". Desde C: cuenta "
            + ", ".join(dec(p) for p in datos["C"]["cuenta"]) + "; réplicas "
            + ", ".join(dec(p) for p in datos["C"]["simulada"])
            + f". Abajo, réplicas menos cuenta, con una franja de ±{dec(banda)}, dos errores "
            f"estándar en el peor caso (p = 0.5); la mayor diferencia es {dec(peor)}, unos {peor_z:.1f} errores "
            "estándar. En esta matriz las dos curvas se acercan.")
    return svg(titulo, desc, out, y)


# ------------------------------------------------------- recuperar-p ---

def _x_log(T, x0=66, x1=258, d0=1, d1=4):
    return x0 + (x1 - x0) * (math.log10(T) - d0) / (d1 - d0)


def mkv_c1_recuperar_p():
    datos = m.recuperar_p()
    P = m.redondear_matriz(m.matriz_corpus())
    titulo = ["Recuperar una matriz", "conocida, contando"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], ACENTO)
         + _marca("circulo", x, yy, ACENTO), "mediana de 200 réplicas"),
        (lambda x, yy: f'<rect x="{_n(x - 12)}" y="{_n(yy - 7)}" width="24" height="14" '
                       f'fill="{mezclar(ACENTO, 0.3)}"/>', "del 5 % al 95 % de ellas"),
    ])
    top, alto, tope = y + 36, 170, 0.35

    def py(v):
        return top + alto * (1 - v / tope)
    out.append(texto(X_PIE, top - 12, "error = máx |P̂ − P|", tam=13, anclaje="start",
                     peso="700"))
    for v in (0, 0.1, 0.2, 0.3):
        out.append(linea(58, _n(py(v)), 270, _n(py(v)), color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(50, py(v) + 4, f"{v:g}", tam=12, anclaje="end", color=SUAVE))
    Ts = list(datos)
    banda = ([(_x_log(T), py(datos[T]["p95"])) for T in Ts]
             + [(_x_log(T), py(datos[T]["p5"])) for T in reversed(Ts)])
    out.append(f'<polygon points="{" ".join(f"{_n(a)},{_n(b)}" for a, b in banda)}" '
               f'fill="{mezclar(ACENTO, 0.3)}"/>')
    out.append(_polilinea([(_x_log(T), py(datos[T]["mediana"])) for T in Ts], ACENTO))
    for T in Ts:
        out.append(_marca("circulo", _x_log(T), py(datos[T]["mediana"]), ACENTO, r=4))
    for T in (10, 100, 1000, 10000):
        out.append(texto(_x_log(T), top + alto + 18, miles(T), tam=12, color=SUAVE))
    out.append(texto(162, top + alto + 38, "largo T, en pasos (escala log)", tam=13, peso="700"))
    sin = sum(d["sin_salidas"] for d in datos.values())
    y = pie(out, top + alto + 62, [
        f"P verdadera: filas ({dec(P[0][0])}, {dec(P[0][1])})",
        f"y ({dec(P[1][0])}, {dec(P[1][1])}); cada réplica",
        "empieza en C. Réplicas con un",
        f"estado sin salidas: {sin}."])
    desc = ("Error de la matriz estimada contra el largo T de la trayectoria, en pasos, en 200 "
            "réplicas de una cadena conocida (la del corpus redondeada a 3 decimales), con T "
            "en escala logarítmica. " + "; ".join(
                f"T = {miles(T)}: mediana {dec(datos[T]['mediana'])}, del 5 % al 95 % entre "
                f"{dec(datos[T]['p5'])} y {dec(datos[T]['p95'])}" for T in Ts)
            + f". Réplicas con un estado sin salidas: {sin}.")
    return svg(titulo, desc, out, y)


# ------------------------------------------------------------- ceros ---

def mkv_c1_ceros():
    filas = [m.fraccion_no_vista(h) for h in range(4)]
    titulo = ["Lo que nunca se vio,", "por memoria"]
    out = []
    y = encabezado(out, titulo)
    y = pie(out, y + 4, ["Se cuenta con la primera mitad del", "corpus y se mide en la segunda:",
                         "¿qué fracción de las transiciones", "nunca apareció al contar?"],
            tam=13, color=TEXTO)
    x0, ancho_max = 106, 112
    tope = max(float(f["fraccion"]) for f in filas)
    y += 14
    for f in filas:
        w = ancho_max * float(f["fraccion"]) / tope
        out.append(texto(X_PIE, y + 13, f"memoria {f['memoria']}", tam=14, peso="700",
                         anclaje="start"))
        out.append(f'<rect x="{x0}" y="{_n(y)}" width="{ancho_max}" height="18" '
                   f'fill="none" stroke="{mezclar(LINEA, 0.8)}" stroke-width="1"/>')
        if w > 0:
            out.append(f'<rect x="{x0}" y="{_n(y)}" width="{_n(max(w, 1.5))}" height="18" '
                       f'fill="{ACENTO}"/>')
        out.append(texto(x0 + ancho_max + 6, y + 14, pct(f["fraccion"]), tam=13, peso="700",
                         anclaje="start"))
        out.append(texto(X_PIE, y + 38, f"no vistas: {miles(f['no_vistas'])} de "
                         f"{miles(f['total'])}", tam=12, anclaje="start", color=SUAVE))
        out.append(texto(X_PIE, y + 56, f"contextos vistos: {miles(f['contextos_vistos'])} "
                         f"de {miles(f['contextos_posibles'])}", tam=12, anclaje="start",
                         color=SUAVE))
        y += 78
    y = pie(out, y + 4, ["La barra llena es la mayor fracción;", "solo diagnostica escasez,",
                         "no elige la memoria."])
    desc = ("Fracción de las transiciones de la segunda mitad del corpus cuyo (contexto, "
            "siguiente) nunca apareció en la primera mitad, por memoria; las barras están "
            "a escala de la mayor (memoria 3). " + "; ".join(
                f"memoria {f['memoria']}: {pct(f['fraccion'])} ({miles(f['no_vistas'])} de "
                f"{miles(f['total'])}), contextos vistos {miles(f['contextos_vistos'])} de "
                f"{miles(f['contextos_posibles'])}" for f in filas) + ".")
    return svg(titulo, desc, out, y)


# ------------------------------------------------------------ rachas ---

def _y_log(v, top, alto, d1=6):
    return top + alto * (1 - math.log10(max(v, 1)) / d1)


SUPER = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def mkv_c1_rachas():
    r = m.rachas_resumen()
    sim = {"markov": m.rachas_simuladas("markov"), "independiente":
           m.rachas_simuladas("independiente")}
    reales = r["reales"]
    ells = range(1, 6)
    titulo = ["Rachas de consonantes", "reales contra simuladas"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: f'<rect x="{_n(x - 7)}" y="{_n(yy - 8)}" width="14" height="16" '
                       f'fill="{mezclar(COLOR_REAL, 0.35)}" stroke="{COLOR_REAL}" '
                       f'stroke-width="1.5"/>', "reales, en el corpus"),
        (lambda x, yy: _marca("rombo", x, yy, ACENTO),
         f"cadena (q = {dec(r['q_markov'])})"),
        (lambda x, yy: _marca("triangulo", x, yy, TEXTO, r=4),
         f"independientes (q = {dec(r['q_independiente'])})"),
    ])
    top, alto = y + 28, 180
    out.append(texto(X_PIE, top - 12, "número de rachas (escala log)", tam=13,
                     anclaje="start", peso="700"))
    for d in range(0, 7, 2):
        yy = _y_log(10 ** d, top, alto)
        out.append(linea(58, _n(yy), 284, _n(yy), color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(52, yy + 4, "1" if d == 0 else "10" + str(d).translate(SUPER),
                         tam=12, anclaje="end", color=SUAVE))
    base = _y_log(1, top, alto)
    for ell in ells:
        xc = 58 + 45 * (ell - 1) + 24
        n_real = reales.get(ell, 0)
        yr = _y_log(n_real, top, alto)
        out.append(f'<rect x="{_n(xc - 15)}" y="{_n(yr)}" width="14" height="{_n(base - yr)}" '
                   f'fill="{mezclar(COLOR_REAL, 0.35)}" stroke="{COLOR_REAL}" '
                   f'stroke-width="1.5"/>')
        # rombo y triángulo, no círculo y cuadrado: esas marcas son V y C en
        # toda la unidad, y aquí no se dibujan estados
        for modelo, dx, forma, color in (("markov", 6, "rombo", ACENTO),
                                         ("independiente", 16, "triangulo", TEXTO)):
            med, p5, p95 = sim[modelo][ell]
            out.append(linea(_n(xc + dx), _n(_y_log(p95, top, alto)), _n(xc + dx),
                             _n(_y_log(p5, top, alto)), color=color, grosor=1.5))
            out.append(_marca(forma, xc + dx, _y_log(med, top, alto), color,
                              r=4.5 if forma == "rombo" else 4))
        out.append(texto(xc, top + alto + 18, str(ell), tam=12, color=SUAVE))
    out.append(texto(170, top + alto + 38, "largo ℓ de la racha", tam=13, peso="700"))
    y = pie(out, top + alto + 62, [
        f"Marcas: mediana de {m.N_RACHAS} réplicas del largo",
        "del corpus. Su franja del 5 % al 95 %",
        "es más angosta que la marca:",
        "la diferencia no es azar."])
    desc = ("Número de rachas de consonantes de cada largo ℓ, de 1 a 5, en escala "
            "logarítmica: las reales del corpus (barras) contra la mediana de "
            f"{m.N_RACHAS} réplicas del largo del corpus de una cadena con q = "
            f"{dec(r['q_markov'])} (rombos) y de letras independientes con q = "
            f"{dec(r['q_independiente'])} (triángulos). " + "; ".join(
                f"ℓ = {ell}: reales {miles(reales.get(ell, 0))}, cadena "
                f"{miles(sim['markov'][ell][0])}, independientes "
                f"{miles(sim['independiente'][ell][0])}" for ell in ells)
            + ". La franja del 5 % al 95 % de las réplicas es más angosta que la marca.")
    return svg(titulo, desc, out, y)


# ----------------------------------------------------------- catalogo ---


# =========================================================== CLASE 2 ===
#
# Figuras «mkv-c2-*» de course/8_markov/2_a_la_larga/ (plan de la clase 2,
# §5). Cada cifra sale de markov.py (seccion «Clase 2»).

COLOR_CERRADA = SERIE[0]          # verde: clase cerrada (ademas: borde continuo)
COLOR_ABIERTA = COLOR_C           # amarillo: transitorio (ademas: borde punteado)


def _gnodo(cx, cy, rotulo, color=COLOR_V, r=20, guiones=None, tam=15):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{r}" fill="{mezclar(color, 0.18)}" '
            f'stroke="{color}" stroke-width="2"{trazo}/>'
            + texto(cx, cy + tam * 0.35, rotulo, tam=tam, peso="700"))


def _arista(a, b, rotulo, r=20, curva=0.0, lado=1, tam=13, desp=12):
    """Flecha de centro a centro recortada por el radio; curva = desviacion
    del punto de control, perpendicular a la cuerda (en px). El rotulo va
    del lado `lado` del punto medio de la curva."""
    (x1, y1), (x2, y2) = a, b
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    nx, ny = -dy / d, dx / d
    mx, my = (x1 + x2) / 2 + nx * curva, (y1 + y2) / 2 + ny * curva

    def recorta(px, py, qx, qy, rr):
        L = math.hypot(qx - px, qy - py)
        return px + (qx - px) * rr / L, py + (qy - py) * rr / L
    sx, sy = recorta(x1, y1, mx, my, r)
    ex, ey = recorta(x2, y2, mx, my, r + 2)
    camino = _curva(f"M {_n(sx)} {_n(sy)} Q {_n(mx)} {_n(my)} {_n(ex)} {_n(ey)}")
    # punto medio de la cuadratica
    qx = 0.25 * sx + 0.5 * mx + 0.25 * ex
    qy = 0.25 * sy + 0.5 * my + 0.25 * ey
    s = 1 if curva >= 0 else -1
    if curva == 0:
        s = lado
    tx, ty = qx + nx * desp * s, qy + ny * desp * s + tam * 0.35
    return camino + texto(tx, ty, rotulo, tam=tam, peso="700")


def _lazo(cx, cy, rotulo, r=20, hacia="arriba", tam=13):
    """Lazo de un estado a si mismo hacia arriba, abajo, izquierda o derecha."""
    ang = {"arriba": -90, "abajo": 90, "izquierda": 180, "derecha": 0}[hacia]
    a = math.radians(ang)
    a0, a1 = a - 0.45, a + 0.45
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + (r + 2) * math.cos(a1), cy + (r + 2) * math.sin(a1)
    L = r + 46
    c0x, c0y = cx + L * math.cos(a - 0.7), cy + L * math.sin(a - 0.7)
    c1x, c1y = cx + L * math.cos(a + 0.7), cy + L * math.sin(a + 0.7)
    camino = _curva(f"M {_n(x0)} {_n(y0)} C {_n(c0x)} {_n(c0y)} {_n(c1x)} {_n(c1y)} "
                    f"{_n(x1)} {_n(y1)}")
    tx, ty = cx + (r + 46) * math.cos(a), cy + (r + 46) * math.sin(a) + tam * 0.35
    ancla = "middle"
    if hacia == "derecha":
        ancla, tx = "start", tx - 4
    elif hacia == "izquierda":
        ancla, tx = "end", tx + 4
    return camino + texto(tx, ty, rotulo, tam=tam, peso="700", anclaje=ancla)


def _marco_clase(x, y, w, h, cerrada):
    """Caja de una clase: continua y verde si es cerrada; punteada y
    amarilla si no (la forma del borde lo dice sin el color)."""
    return caja(_n(x), _n(y), _n(w), _n(h), relleno="none",
                borde=COLOR_CERRADA if cerrada else COLOR_ABIERTA,
                grosor=2, guiones=None if cerrada else "3 4")


def mkv_c2_grafo_clasificar():
    P, nombres = m.T5_P, m.T5_ESTADOS
    cl = m.clases(P)
    assert [c["estados"] for c in cl] == [(0,), (1, 2), (3, 4)]
    assert [c["cerrada"] for c in cl] == [False, True, True]
    assert [c["periodo"] for c in cl] == [None, 2, 1]
    titulo = ["Clasificar cinco estados", "tres clases"]
    out = []
    y = encabezado(out, titulo)
    pos = {0: (150, y + 44), 1: (78, y + 150), 2: (78, y + 250),
           3: (198, y + 150), 4: (198, y + 250)}
    # marcos de clase
    out.append(_marco_clase(108, y + 16, 84, 56, False))
    out.append(_marco_clase(22, y + 112, 112, 178, True))
    out.append(_marco_clase(150, y + 112, 128, 178, True))
    sl = pos
    out.append(_arista(sl[0], sl[1], fr(P[0][1]), curva=0, lado=1))
    out.append(_arista(sl[0], sl[3], fr(P[0][3]), curva=0, lado=-1))
    out.append(_arista(sl[1], sl[2], fr(P[1][2]), curva=-16))
    out.append(_arista(sl[2], sl[1], fr(P[2][1]), curva=-16))
    out.append(_arista(sl[3], sl[4], fr(P[3][4]), curva=-16))
    out.append(_arista(sl[4], sl[3], fr(P[4][3]), curva=-16))
    out.append(_lazo(*sl[3], fr(P[3][3]), hacia="derecha"))
    for i, (cx, cy) in pos.items():
        cerrada = i != 0
        out.append(_gnodo(cx, cy, nombres[i], COLOR_CERRADA if cerrada else COLOR_ABIERTA,
                          guiones=None if cerrada else "3 3"))
    out.append(texto(200, y + 36, "transitoria", tam=12, anclaje="start", peso="700"))
    out.append(texto(200, y + 52, "(abierta)", tam=12, anclaje="start", color=SUAVE))
    yb = y + 310
    out.append(texto(78, yb, "cerrada", tam=13, peso="700"))
    out.append(texto(78, yb + 18, "periodo 2", tam=13))
    out.append(texto(214, yb, "cerrada", tam=13, peso="700"))
    out.append(texto(214, yb + 18, "aperiódica", tam=13))
    y = pie(out, yb + 48, ["Marco continuo: clase cerrada (no sale",
                           "ninguna flecha). Punteado: abierta;",
                           "de s1 se sale y no se vuelve."])
    desc = ("Grafo de cinco estados. s1 va a s2 con 1/2 y a s4 con 1/2. s2 va a s3 con 1 "
            "y s3 a s2 con 1. s4 se queda con 1/2 (lazo) y va a s5 con 1/2; s5 va a s4 con 1. "
            "Tres clases: {s1} transitoria (abierta, marco punteado); {s2, s3} cerrada de "
            "periodo 2; {s4, s5} cerrada aperiódica (el lazo de s4). Las cerradas llevan "
            "marco continuo.")
    return svg(titulo, desc, out, y)


def mkv_c2_grafo_contraejemplos():
    titulo = ["Tres contraejemplos", "pequeños"]
    out = []
    y = encabezado(out, titulo)
    # T2
    y += 10
    out.append(texto(X_PIE, y, "Alternante: periodo 2", tam=14, peso="700", anclaje="start"))
    yn = y + 52
    a, b = (100, yn), (200, yn)
    out.append(_marco_clase(62, yn - 34, 176, 68, True))
    out.append(_arista(a, b, "1", curva=-18))
    out.append(_arista(b, a, "1", curva=-18))
    out.append(_gnodo(*a, "A", COLOR_CERRADA))
    out.append(_gnodo(*b, "B", COLOR_CERRADA))
    y = pie(out, yn + 58, ["μ = (1/2, 1/2) es única, pero desde A",
                           "la cadena oscila: A, B, A, B, …"], color=TEXTO)
    # T3
    y += 14
    out.append(texto(X_PIE, y, "Identidad: dos clases cerradas", tam=14, peso="700",
                     anclaje="start"))
    yn = y + 96
    a, b = (100, yn), (200, yn)
    for c, rot in ((a, "s1"), (b, "s2")):
        out.append(_marco_clase(c[0] - 40, yn - 80, 80, 110, True))
        out.append(_lazo(*c, "1", hacia="arriba"))
        out.append(_gnodo(*c, rot, COLOR_CERRADA))
    y = pie(out, yn + 54, ["Nadie sale de donde empieza: toda", "distribución es estacionaria."],
            color=TEXTO)
    # T4
    y += 14
    out.append(texto(X_PIE, y, "Transitorio entre dos cerradas", tam=14, peso="700",
                     anclaje="start"))
    P = m.T4_P
    y1 = y + 96
    s1, s2, s3 = (150, y1), (100, y1 + 110), (200, y1 + 110)
    out.append(_marco_clase(108, y1 - 82, 84, 116, False))
    out.append(_lazo(*s1, fr(P[0][0]), hacia="arriba"))
    out.append(_arista(s1, s2, fr(P[0][1]), lado=1))
    out.append(_arista(s1, s3, fr(P[0][2]), lado=-1))
    for c, rot in ((s2, "s2"), (s3, "s3")):
        x = c[0] - 78 if rot == "s2" else c[0] - 34
        out.append(_marco_clase(x, c[1] - 32, 112, 64, True))
        lado = "izquierda" if rot == "s2" else "derecha"
        out.append(_lazo(*c, "1", hacia=lado))
        out.append(_gnodo(*c, rot, COLOR_CERRADA))
    out.append(_gnodo(*s1, "s1", COLOR_ABIERTA, guiones="3 3"))
    y = pie(out, y1 + 170, ["Desde s1 cae en s2 o en s3, al azar:",
                            "la fracción del tiempo en s2 tiende",
                            "a 1 o a 0 según la réplica."], color=TEXTO)
    y = pie(out, y + 6, ["Marco continuo: clase cerrada.", "Punteado: abierta."])
    desc = ("Tres cadenas apiladas. Primera, alternante: A va a B con 1 y B a A con 1; una "
            "clase cerrada de periodo 2; μ = (1/2, 1/2) única, pero desde A oscila. Segunda, "
            "identidad: s1 y s2 se quedan con 1; dos clases cerradas; toda distribución es "
            "estacionaria. Tercera: s1 se queda con 1/2 y va a s2 con 1/4 y a s3 con 1/4; s2 "
            "y s3 se quedan con 1; s1 es transitorio (marco punteado) y la fracción del "
            "tiempo en s2 tiende a 1 o a 0 según la réplica.")
    return svg(titulo, desc, out, y)


def mkv_c2_mu_t_inicios():
    T = 10
    P1, P2 = m.T1_P, m.T2_P
    mu = m.estacionaria(P1)
    desdeV = [x[0] for x in m.mu_t(P1, (F(1), F(0)), T)]
    desdeC = [x[0] for x in m.mu_t(P1, (F(0), F(1)), T)]
    alt = [x[0] for x in m.mu_t(P2, (F(1), F(0)), T)]
    titulo = ["¿Olvida su inicio?", "Pr(Sₜ = primer estado)"]
    out = []
    y = encabezado(out, titulo)
    COLOR_ALT = ACENTO
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V)
         + _marca("circulo", x, yy, COLOR_V), "frase, desde V"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_C, "5 4")
         + _marca("cuadro", x, yy, COLOR_C, r=4), "frase, desde C"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_ALT, "2 3")
         + _marca("triangulo", x, yy, COLOR_ALT, r=4), "alternante, desde A"),
        (lambda x, yy: linea(x - 12, yy, x + 12, yy, color=TEXTO, grosor=1, guiones="1 3"),
         f"μ(V) = {fr(mu[0])} de la frase"),
    ])
    top, alto = y + 24, 190

    def px(t):
        return MU_X0 + (MU_X1 - MU_X0) * t / T

    def py(p):
        return top + alto * (1 - float(p))
    for v in (0, 0.5, 1):
        out.append(linea(MU_X0, _n(py(v)), MU_X1, _n(py(v)), color=mezclar(LINEA, 0.5),
                         grosor=1))
        out.append(texto(MU_X0 - 12, py(v) + 4, f"{v:g}", tam=12, anclaje="end", color=SUAVE))
    out.append(linea(MU_X0, _n(py(mu[0])), MU_X1, _n(py(mu[0])), color=TEXTO, grosor=1,
                     guiones="1 3"))
    for serie, color, forma, guiones in ((alt, COLOR_ALT, "triangulo", "2 3"),
                                         (desdeV, COLOR_V, "circulo", None),
                                         (desdeC, COLOR_C, "cuadro", "5 4")):
        out.append(_polilinea([(px(t), py(p)) for t, p in enumerate(serie)], color, guiones))
        for t, p in enumerate(serie):
            out.append(_marca(forma, px(t), py(p), color, r=4))
    for t in range(0, T + 1, 2):
        out.append(texto(px(t), top + alto + 18, str(t), tam=12, color=SUAVE))
    out.append(texto((MU_X0 + MU_X1) / 2, top + alto + 38, "paso t", tam=13, peso="700"))
    lam = abs(m.segundo_valor_propio_2x2(P1))
    y = pie(out, top + alto + 62, [
        "La frase olvida su inicio: desde V y",
        f"desde C llega a {fr(mu[0])} ≈ {dec(mu[0])};",
        f"la distancia a μ se multiplica por {fr(lam)}",
        "en cada paso.",
        "La alternante no: 1, 0, 1, 0, …"], color=TEXTO)
    desc = ("Probabilidad de estar en el primer estado en el paso t, de t = 0 a 10. "
            "Matriz de la frase (V, C) desde V: " + ", ".join(dec(p) for p in desdeV)
            + ". Desde C: " + ", ".join(dec(p) for p in desdeC)
            + f". Las dos se juntan en μ(V) = {fr(mu[0])} ≈ {dec(mu[0])}; la distancia a μ se "
            f"multiplica por {fr(lam)} en cada paso. Cadena alternante desde A: "
            + ", ".join(fr(p) for p in alt) + "; oscila y no converge.")
    return svg(titulo, desc, out, y)


FLUJOS.update({
    "potencias": dict(
        nombre="la iteración de potencias",
        titulo=["Iteración de potencias,", "en palabras"],
        pasos=[{"caja": ["Empieza con μ₀", "y t = 0"]},
               {"caja": ["Multiplica: μ′ = μP", "y suma 1 a t"]},
               {"rombo": ["¿‖μ′ − μ‖₁", "≤ tol?"], "abajo": "no"},
               {"rombo": ["¿t llegó", "al tope?"], "abajo": "no"},
               {"caja": ["Avanza: μ ← μ′"]},
               {"caja": ["Devuelve μ′ y t"], "fin": True, "sin_flecha": True}],
        vueltas=[(4, 1, "otra vuelta")],
        salidas=[(2, 5, "sí"), (3, 5, "sí")],
        notas=["Si para por el tope, avisa: no", "convergió (la alternante desde A).",
               "Cada vuelta cuesta k² productos."]),
    "absorcion": dict(
        nombre="el tiempo medio de llegada",
        titulo=["Tiempo medio de llegada,", "en palabras"],
        pasos=[{"caja": ["Marca la meta A:", "m = 0 en A"]},
               {"caja": ["Quita de P las filas", "y columnas de A"]},
               {"caja": ["Arma el sistema", "(I − P𝒯) m = 1"]},
               {"rombo": ["¿Tiene una", "solución?"], "abajo": "sí"},
               {"caja": ["Resuélvelo y", "devuelve m"], "fin": True},
               {"caja": ["Avisa: desde algún", "estado no se llega"], "fin": True,
                "sin_flecha": True}],
        vueltas=[],
        salidas=[(3, 5, "no")],
        notas=["Cada renglón dice: un turno más", "lo que falta desde donde caes."]),
})


def mkv_c2_tablero_chico():
    cfg = m.TABLERO_CHICO
    estados, P = m.tablero_desde(cfg)
    mm = m.absorcion_tablero("chico")
    assert estados == [0, 1, 4, 5]
    titulo = ["Un tablero de 6 casillas", "moneda: avanza 1 o 2"]
    out = []
    y = encabezado(out, titulo)
    x0, w, yc = 18, 44, y + 74
    cx = {c: x0 + w * c + w / 2 for c in range(6)}
    for c in range(6):
        es = c not in cfg["saltos"]
        out.append(caja(_n(x0 + w * c + 2), _n(yc - 20), w - 4, 40,
                        relleno=mezclar(COLOR_V if es else LINEA, 0.12),
                        borde=COLOR_V if es else SUAVE, radio=6, grosor=2,
                        guiones=None if es else "3 3"))
        out.append(texto(cx[c], yc + 6, str(c), tam=16, peso="700"))
    # escalera 2 -> 4 por arriba, serpiente 3 -> 1 por abajo
    out.append(_curva(f"M {_n(cx[2])} {_n(yc - 22)} Q {_n((cx[2] + cx[4]) / 2)} {_n(yc - 64)} "
                      f"{_n(cx[4])} {_n(yc - 24)}", color=COLOR_CERRADA).replace(
                          'stroke-width="2"', 'stroke-width="3"'))
    out.append(texto((cx[2] + cx[4]) / 2, yc - 50, "escalera 2 → 4", tam=13, peso="700"))
    out.append(_curva(f"M {_n(cx[3])} {_n(yc + 22)} Q {_n((cx[1] + cx[3]) / 2)} {_n(yc + 64)} "
                      f"{_n(cx[1])} {_n(yc + 24)}", color=COLOR_C).replace(
                          'stroke-width="2"', 'stroke-width="2" stroke-dasharray="5 3"'))
    out.append(texto((cx[1] + cx[3]) / 2, yc + 60, "serpiente 3 → 1", tam=13, peso="700"))
    y = pie(out, yc + 92, ["Punteadas (2 y 3): al caer ahí te mueves;",
                           "no son estados. Si te pasas, llegas a 5."])
    # grafo de estados reales
    y += 10
    out.append(texto(X_PIE, y, "Estados al final del turno", tam=14, peso="700",
                     anclaje="start"))
    yn = y + 80
    pos = {0: (40, yn), 1: (110, yn), 4: (190, yn), 5: (262, yn)}
    i = {e: k for k, e in enumerate(estados)}
    out.append(_arista(pos[0], pos[1], fr(P[i[0]][i[1]]), lado=-1, r=18))
    out.append(_arista(pos[0], pos[4], fr(P[i[0]][i[4]]), curva=-46, r=18))
    out.append(_lazo(*pos[1], fr(P[i[1]][i[1]]), hacia="abajo", r=18))
    out.append(_arista(pos[1], pos[4], fr(P[i[1]][i[4]]), lado=-1, r=18))
    out.append(_arista(pos[4], pos[5], fr(P[i[4]][i[5]]), lado=-1, r=18))
    for e, (x, yy) in pos.items():
        meta = e == 5
        out.append(_gnodo(x, yy, str(e), COLOR_CERRADA if meta else COLOR_V, r=18,
                          guiones=None))
        if meta:
            out.append(f'<circle cx="{_n(x)}" cy="{_n(yy)}" r="23" fill="none" '
                       f'stroke="{COLOR_CERRADA}" stroke-width="2"/>')
    out.append(texto(262, yn + 44, "meta", tam=13, peso="700"))
    ym = yn + 92
    out.append(texto(X_PIE, ym, "Turnos que faltan, en promedio:", tam=13, anclaje="start",
                     color=SUAVE, peso="700"))
    for e, (x, _) in pos.items():
        out.append(texto(x, ym + 24, f"m = {fr(mm[e])}", tam=14, peso="700"))
    y = ym + 50
    desc = ("Tablero de casillas 0 a 5 con moneda: avanza 1 o 2 con probabilidad 1/2. "
            "Escalera en 2 que sube a 4; serpiente en 3 que baja a 1; si te pasas de 5 "
            "llegas a 5. Las casillas 2 y 3 no son estados. Grafo de estados al final del "
            f"turno: 0 va a 1 con {fr(P[i[0]][i[1]])} y a 4 con {fr(P[i[0]][i[4]])}; 1 se "
            f"queda con {fr(P[i[1]][i[1]])} (cae en 3 y baja) y va a 4 con "
            f"{fr(P[i[1]][i[4]])}; 4 va a 5 con 1; 5 es la meta. Turnos medios que faltan: "
            + ", ".join(f"m({e}) = {fr(mm[e])}" for e in estados) + ".")
    return svg(titulo, desc, out, y)


def mkv_c2_web_juguete():
    enl = m.T9_ENLACES
    pr = m.pagerank_exacto(enl)
    titulo = ["Una web de cuatro páginas", "D no tiene enlaces de salida"]
    out = []
    y = encabezado(out, titulo)
    pos = {"A": (80, y + 50), "B": (220, y + 50), "C": (80, y + 180), "D": (220, y + 180)}
    out.append(_arista(pos["A"], pos["B"], "", r=22))
    out.append(_arista(pos["A"], pos["C"], "", r=22, curva=14))
    out.append(_arista(pos["C"], pos["A"], "", r=22, curva=14))
    out.append(_arista(pos["B"], pos["C"], "", r=22))
    out.append(_arista(pos["C"], pos["D"], "", r=22))
    for p, (x, yy) in pos.items():
        d = p == "D"
        out.append(_gnodo(x, yy, p, COLOR_C if d else COLOR_V, r=22,
                          guiones="4 3" if d else None, tam=18))
    out.append(texto(220, y + 226, "sin salidas", tam=13, peso="700"))
    yb = y + 268
    out.append(texto(X_PIE, yb, f"PageRank con α = {dec(m.ALFA, 2)}", tam=14, peso="700",
                     anclaje="start"))
    x0, x1 = 40, 200
    tope = 0.6
    for k, (p, v) in enumerate(zip(m.T9_PAGINAS, pr)):
        yy = yb + 26 + 26 * k
        out.append(texto(X_PIE + 4, yy + 5, p, tam=14, peso="700", anclaje="start"))
        out.append(f'<rect x="{x0}" y="{_n(yy - 8)}" width="{_n((x1 - x0) * float(v) / tope)}" '
                   f'height="16" fill="{mezclar(COLOR_C if p == "D" else COLOR_V, 0.6)}"/>')
        out.append(texto(x0 + (x1 - x0) * float(v) / tope + 8, yy + 5,
                         f"{fr(v)} ≈ {dec(v)}", tam=13, anclaje="start"))
    y = pie(out, yb + 26 * 4 + 34, ["Desde D, el navegante salta a", "cualquier página (1/4 cada una)."])
    desc = ("Grafo dirigido de cuatro páginas: A enlaza a B y a C; B enlaza a C; C enlaza a "
            "A y a D; D no tiene enlaces de salida (borde punteado). PageRank con α = 0.85 y "
            "salto uniforme: " + ", ".join(f"{p} = {fr(v)} ≈ {dec(v)}"
                                           for p, v in zip(m.T9_PAGINAS, pr)) + ".")
    return svg(titulo, desc, out, y)


DIAGRAMAS = {
    "mkv-c1-flujo-muestrear": lambda: flujo("muestrear"),
    "mkv-c1-flujo-contar": lambda: flujo("contar"),
    "mkv-c1-flujo-predecir": lambda: flujo("predecir"),
    "mkv-c1-flujo-generar": lambda: flujo("generar"),
    "mkv-c1-grafo-vc": mkv_c1_grafo_vc,
    "mkv-c1-arbol-2-pasos": mkv_c1_arbol_2_pasos,
    "mkv-c1-mu-t": mkv_c1_mu_t,
    "mkv-c1-recuperar-p": mkv_c1_recuperar_p,
    "mkv-c1-ceros": mkv_c1_ceros,
    "mkv-c1-rachas": mkv_c1_rachas,
    "mkv-c2-grafo-clasificar": mkv_c2_grafo_clasificar,
    "mkv-c2-grafo-contraejemplos": mkv_c2_grafo_contraejemplos,
    "mkv-c2-mu-t-inicios": mkv_c2_mu_t_inicios,
    "mkv-c2-flujo-potencias": lambda: flujo("potencias"),
    "mkv-c2-tablero-chico": mkv_c2_tablero_chico,
    "mkv-c2-flujo-absorcion": lambda: flujo("absorcion"),
    "mkv-c2-web-juguete": mkv_c2_web_juguete,
}


def contenido(nombre):
    """El SVG de `nombre`, sin escribirlo."""
    return DIAGRAMAS[nombre]()


def escribir(nombre):
    ASSETS.mkdir(parents=True, exist_ok=True)
    destino = ASSETS / f"{nombre}.svg"
    destino.write_text(contenido(nombre), encoding="utf-8")
    return destino


def main(argv):
    nombres = argv[1:] or list(DIAGRAMAS)
    for nombre in nombres:
        if nombre not in DIAGRAMAS:
            raise SystemExit(f"diagrama desconocido: {nombre}")
        print(escribir(nombre))


if __name__ == "__main__":
    main(sys.argv)
