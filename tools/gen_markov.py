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

Los ids llevan prefijo "mkv-c1-" (clase 1), "mkv-c2-" (clase 2), "mkv-c3-"
(clase 3) o "mkv-c4-" (clase 4): los ids de objeto numerado son unicos en todo el curso.
"""
import math
import sys
from functools import lru_cache
from fractions import Fraction as F
from xml.sax.saxutils import escape

import markov as m
from gen_optimizacion import (ACENTO, ALARMA, FONDO, FUENTE, LINEA, SERIE, SUAVE, TEXTO,
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


def fr10(x):
    """Como la clase 4 escribe los decimos: 2/10, no 1/5 (0 y 1 quedan enteros)."""
    x = F(x)
    return f"{int(x * 10)}/10" if x not in (0, 1) and (x * 10).denominator == 1 else fr(x)


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
    mx_de = {}
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
            mx = p.get("mx", FL_MX)        # rombo mas ancho si el rotulo no cabe
            mx_de[k] = mx
            out.append(_rombo(FL_CX, round(cy, 1), mx, my, mezclar(COLOR_V, 0.08),
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
        xa = FL_CX - mx_de.get(desde, FL_MX) if tipo_a == "rombo" else FL_X0
        xb = FL_CX - mx_de.get(hasta, FL_MX) if tipo_b == "rombo" else FL_X0
        out.append(f'<polyline points="{_n(xa)},{_n(ya)} {FL_CARRIL},{_n(ya)} '
                   f'{FL_CARRIL},{_n(yb)}" fill="none" stroke="{SUAVE}" stroke-width="2"/>')
        out.append(_flecha(FL_CARRIL, yb, xb - 3, yb))
        out.append(girado(FL_CARRIL - 8, (ya + yb) / 2, rot))
    # Con dos salidas, la segunda baja por un carril interior: si las dos
    # compartieran carril no se sabria que rombo lleva a que caja.
    for i, (desde, hasta, rot) in enumerate(salidas):
        _, _, ya = geo[desde]
        _, _, yb = geo[hasta]
        xa = FL_CX + mx_de.get(desde, FL_MX)
        carril = FL_CARRIL_DER if len(salidas) == 1 else FL_CARRIL_DER + 4 - 7 * i
        out.append(f'<polyline points="{_n(xa)},{_n(ya)} {carril},{_n(ya)} '
                   f'{carril},{_n(yb)}" fill="none" stroke="{SUAVE}" stroke-width="2"/>')
        out.append(_flecha(carril, yb, FL_X1 + 3, yb))
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
    de = "del" if nombre.startswith("el ") else "de"
    nombre = nombre[3:] if de == "del" else nombre
    return (f"Diagrama de flujo {de} {nombre}, en palabras. " + " ".join(partes)
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


def _lazo(cx, cy, rotulo, r=20, hacia="arriba", tam=13, alcance=46):
    """Lazo de un estado a si mismo hacia arriba, abajo, izquierda o derecha."""
    ang = {"arriba": -90, "abajo": 90, "izquierda": 180, "derecha": 0}[hacia]
    a = math.radians(ang)
    a0, a1 = a - 0.45, a + 0.45
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + (r + 2) * math.cos(a1), cy + (r + 2) * math.sin(a1)
    L = r + alcance
    c0x, c0y = cx + L * math.cos(a - 0.7), cy + L * math.sin(a - 0.7)
    c1x, c1y = cx + L * math.cos(a + 0.7), cy + L * math.sin(a + 0.7)
    camino = _curva(f"M {_n(x0)} {_n(y0)} C {_n(c0x)} {_n(c0y)} {_n(c1x)} {_n(c1y)} "
                    f"{_n(x1)} {_n(y1)}")
    tx, ty = cx + (r + alcance) * math.cos(a), cy + (r + alcance) * math.sin(a) + tam * 0.35
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
    y = pie(out, yn + 58, ["Sí: μ = (1/2, 1/2) es única.",
                           "Sí: fracción del tiempo → 1/2.",
                           "No: desde A, μₜ alterna 1, 0, 1, …",
                           "y no converge. Lo rompe el periodo 2."],
            color=TEXTO)
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
    y = pie(out, yn + 54, ["Nadie sale de donde empieza.",
                           "Sí: μₜ converge (nunca cambia).",
                           "No es única: toda distribución es",
                           "estacionaria. Cada inicio se queda",
                           "con su límite. Lo rompen dos clases."],
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
    y = pie(out, y1 + 170, ["Desde s1 cae en s2 o en s3, al azar.",
                            "Sí: μₜ converge, pero a un límite",
                            "que depende del inicio. Desde s1,",
                            "a (0, 1/2, 1/2): la mitad de las",
                            "réplicas acaba en cada cerrada.",
                            "No es única: (0, p, 1 − p) lo es.",
                            "No: una sola trayectoria pasa 1 o 0",
                            "del tiempo en s2, nunca 1/2."],
            color=TEXTO)
    y = pie(out, y + 6, ["Marco continuo: clase cerrada.", "Punteado: abierta."])
    desc = ("Tres cadenas apiladas, cada una con lo que cumple y lo que rompe. Primera, "
            "alternante: A va a B con 1 y B a A con 1; una clase cerrada de periodo 2. Sí: "
            "μ = (1/2, 1/2) es única y la fracción del tiempo tiende a 1/2. No: desde A, μₜ "
            "alterna 1, 0, 1 y no converge; lo rompe el periodo 2. Segunda, identidad: s1 y s2 "
            "se quedan con 1; dos clases cerradas. Sí: μₜ converge, porque nunca cambia. No: "
            "toda distribución es estacionaria y cada inicio se queda con su límite. Tercera: "
            "s1 se queda con 1/2 y va a s2 con 1/4 y a s3 con 1/4; s2 y s3 se quedan con 1; s1 "
            "es transitorio (marco punteado). Sí: μₜ converge, a un límite que depende del inicio; desde s1, a (0, 1/2, 1/2). No: "
            "(0, p, 1 − p) es estacionaria para todo p, y una sola trayectoria pasa 1 o 0 del "
            "tiempo en s2, nunca 1/2.")
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
            + ", ".join(fr(p) for p in alt) + "; alterna entre 1 y 0 y no converge.")
    return svg(titulo, desc, out, y)


FLUJOS.update({
    "potencias": dict(
        nombre="la iteración de potencias",
        titulo=["Iteración de potencias,", "en palabras"],
        pasos=[{"caja": ["Empieza: μ ← μ₀", "y pasos = 1"]},
               {"caja": ["Multiplica:", "nuevo = μP"]},
               {"caja": ["Mide d = ‖nuevo − μ‖₁", "y avanza: μ ← nuevo"]},
               {"rombo": ["¿d ≤ tol?"], "abajo": "no"},
               {"rombo": ["¿pasos llegó", "al tope?"], "abajo": "no"},
               {"caja": ["Suma 1 a pasos"]},
               {"caja": ["Devuelve (μ, «no paró»)"], "fin": True, "sin_flecha": True},
               {"caja": ["Devuelve (μ, pasos)"], "fin": True, "sin_flecha": True}],
        vueltas=[(5, 1, "otra vuelta")],
        salidas=[(3, 7, "sí"), (4, 6, "sí")],
        notas=["«No paró» no prueba que no converja:", "solo que no cumplió tol a tiempo.",
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



# ------------------------------- ejemplo y contraejemplo (clase 2) ---
# Un SVG por definicion o teorema de las paginas 2 y 3: arriba la cadena que
# lo cumple, abajo la que no, cada una con su grafo y su matriz. Las matrices
# viven aqui (EJEMPLOS) y test_gen_markov.py comprueba que cada una aparece,
# entrada por entrada, en el recuadro «Ejemplo y contraejemplo» de su pagina.
# El color de cada nodo sale de m.clases(P): verde y borde continuo si su
# clase es cerrada; amarillo y punteado si es abierta.

R_EJ = 16
_UNO, _MEDIO, _CUARTO = F(1), F(1, 2), F(1, 4)
_ALTERNANTE = [[0, _UNO], [_UNO, 0]]
_LAZO_EN_S1 = [[_MEDIO, _MEDIO], [_UNO, 0]]
_SIN_VUELTA = [[_MEDIO, _MEDIO], [0, _UNO]]
_FILA2 = {0: (100, 0), 1: (200, 0)}
_FILA3 = {0: (60, 0), 1: (150, 0), 2: (240, 0)}
_TRIANGULO = {0: (150, -34), 1: (215, 34), 2: (85, 34)}


def _panel(P, nombres=("s1", "s2", "s3"), pos=None, lazos=None):
    return {"P": [[F(x) for x in f] for f in P], "nombres": nombres[:len(P)],
            "pos": pos or (_FILA2 if len(P) == 2 else _FILA3), "lazos": lazos or {}}


EJEMPLOS = {
    "comunican": {
        "pagina": "2_clasificar_estados.md", "titulo": "estados que se comunican",
        "si": (_panel(_LAZO_EN_S1), "s1 ↔ s2: hay ida y vuelta"),
        "no": (_panel(_SIN_VUELTA), "s1 → s2, pero no hay vuelta")},
    "clases": {
        "pagina": "2_clasificar_estados.md", "titulo": "comunicar parte en clases",
        "si": (_panel([[_MEDIO, _MEDIO, 0], [_MEDIO, _CUARTO, _CUARTO], [0, 0, 1]],
                      lazos={0: "arriba", 1: "arriba", 2: "arriba"}),
               "Clases {s1, s2} y {s3}, sin traslape"),
        "no": (_panel([[_MEDIO, _MEDIO, 0], [0, _MEDIO, _MEDIO], [0, 0, 1]],
                      lazos={0: "arriba", 1: "arriba", 2: "arriba"}),
               "Solo «alcanzar»: grupos traslapados")},
    "cerrada": {
        "pagina": "2_clasificar_estados.md", "titulo": "clase cerrada",
        "si": (_panel(_SIN_VUELTA), "{s2} cerrada: s2 es absorbente"),
        "no": (_panel([[0, 1, 0], [_MEDIO, 0, _MEDIO], [0, 0, 1]], lazos={2: "arriba"}),
               "{s1, s2} abierta: s2 sale a s3")},
    "hay-cerrada": {
        "pagina": "2_clasificar_estados.md", "titulo": "finita, hay una cerrada",
        "si": (_panel([[_MEDIO, _MEDIO, 0], [0, 0, 1], [0, 1, 0]]),
               "Finita: {s2, s3} es cerrada"),
        "no": ("corrimiento", "Infinita: ninguna clase es cerrada")},
    "transitorio": {
        "pagina": "2_clasificar_estados.md", "titulo": "recurrente y transitorio",
        "si": (_panel([[0, 1], [_MEDIO, _MEDIO]]), "s1 recurrente: regresa seguro"),
        "no": (_panel(_SIN_VUELTA), "s1 transitorio: regresa con 1/2")},
    "recurrente-cerrada": {
        "pagina": "2_clasificar_estados.md", "titulo": "recurrente equivale a cerrada",
        "si": (_panel([[_MEDIO, _MEDIO, 0], [0, _MEDIO, _MEDIO], [0, 1, 0]]),
               "Finita: abierta = transitoria"),
        "no": ("caminata", "Infinita: cerrada y aun así transitoria")},
    "periodo": {
        "pagina": "2_clasificar_estados.md", "titulo": "periodo",
        "si": (_panel(_LAZO_EN_S1), "Regresa en 1 y en 2 pasos: d = 1"),
        "no": (_panel([[0, 1, 0], [0, 0, 1], [1, 0, 0]], pos=_TRIANGULO),
               "Solo regresa en 3, 6, 9…: d = 3")},
    "periodo-clase": {
        "pagina": "2_clasificar_estados.md", "titulo": "un lazo vuelve el periodo 1",
        "si": (_panel(_LAZO_EN_S1), "Con lazo: d = 1 en toda la clase"),
        "no": (_panel(_ALTERNANTE), "Sin lazo: d = 2 en toda la clase")},
    "estacionaria": {
        "pagina": "3_la_estacionaria.md", "titulo": "distribución estacionaria",
        "si": (_panel(_LAZO_EN_S1), "μ = (2/3, 1/3): μP = μ"),
        "no": (_panel(_LAZO_EN_S1), "μ = (1/2, 1/2): μP = (3/4, 1/4)")},
    "limite": {
        "pagina": "3_la_estacionaria.md", "titulo": "el límite es estacionario",
        "si": (_panel(_LAZO_EN_S1), "μₜ → (2/3, 1/3), y es estacionaria"),
        "no": (_panel(_ALTERNANTE, nombres=("A", "B")), "Desde A, μₜ alterna: sin límite")},
    "existe": {
        "pagina": "3_la_estacionaria.md", "titulo": "existe una estacionaria",
        "si": (_panel(_LAZO_EN_S1), "Finita: μ = (2/3, 1/3)"),
        "no": ("corrimiento", "Infinita: μP = μ solo da μ = 0")},
    "unica": {
        "pagina": "3_la_estacionaria.md", "titulo": "una sola clase cerrada",
        "si": (_panel([[0, 1, 0], [_MEDIO, _MEDIO, 0], [_MEDIO, 0, _MEDIO]],
                      pos={0: (150, 0), 1: (240, 0), 2: (60, 0)},
                      lazos={1: "arriba", 2: "arriba"}),
               "Una cerrada: μ = (1/3, 2/3, 0)"),
        "no": (_panel([[1, 0, 0], [0, 1, 0], [_MEDIO, _MEDIO, 0]],
                      pos={0: (60, 0), 1: (240, 0), 2: (150, 0)},
                      lazos={0: "arriba", 1: "arriba"}),
               "Dos cerradas: toda (λ, 1 − λ, 0)")},
    "converge": {
        "pagina": "3_la_estacionaria.md", "titulo": "convergencia desde todo inicio",
        "si": (_panel(_LAZO_EN_S1), "Aperiódica: μₜ → (2/3, 1/3)"),
        "no": (_panel([[0, 1, 0], [_MEDIO, 0, _MEDIO], [0, 1, 0]]),
               "Periodo 2: μₜ alterna, no llega")},
    "ergodico": {
        "pagina": "3_la_estacionaria.md", "titulo": "teorema ergódico",
        "si": (_panel(_ALTERNANTE, nombres=("A", "B")), "Periodo 2, y aun así N/T → 1/2"),
        "no": (_panel([[_MEDIO, _CUARTO, _CUARTO], [0, 1, 0], [0, 0, 1]],
                      pos={0: (150, 0), 1: (60, 0), 2: (240, 0)},
                      lazos={0: "arriba", 1: "arriba", 2: "arriba"}),
               "Dos cerradas: N/T → 1 o 0, al azar")},
}
for _e in EJEMPLOS.values():
    for _lado in ("si", "no"):
        _p = _e[_lado][0]
        if isinstance(_p, dict):
            assert all(sum(_f) == 1 for _f in _p["P"]), _p["P"]


def matriz_latex(P):
    """La matriz como la escriben las paginas: \\begin{pmatrix}1/2&1/2\\\\1&0\\end{pmatrix}."""
    return ("\\begin{pmatrix}" + "\\\\".join("&".join(fr(x) for x in f) for f in P)
            + "\\end{pmatrix}")


def _ancho_txt(s, tam=12):
    return len(s) * tam * 0.62


def _pre_matriz(rotulo, sub, tam=12):
    """Ancho del rotulo «P_sub =» a la izquierda del corchete."""
    return _ancho_txt(rotulo, tam) + (_ancho_txt(sub, tam) + 2 if sub else 0) + 22


def _matriz_svg(out, xc, yc, filas, tam=12, rotulo="P", sub=None, cols=None, marcar=(),
                pre=None):
    """P = [ ... ] con corchetes, centrada en xc; filas son listas de cadenas.
    Clase 3: `sub` escribe el subindice aparte (P con «caminar» abajo),
    `cols` rotula las columnas encima, `marcar` encierra filas en el acento y
    `pre` fija el ancho del rotulo (para alinear varias matrices)."""
    k = len(filas[0])
    col = max(_ancho_txt(c, tam) for f in filas for c in f) + 12
    if cols:
        col = max(col, max(_ancho_txt(c, tam) for c in cols) + 8)
    simple = sub is None and rotulo == "P"
    if pre is None:
        pre = 30 if simple else _pre_matriz(rotulo, sub, tam)
    x = xc - (pre + 6 + k * col) / 2
    alto_fila = 17
    h = len(filas) * alto_fila + 4
    y0 = yc - h / 2
    if simple:
        out.append(texto(x, yc + tam * 0.35, "P =", tam=tam, anclaje="start", color=SUAVE))
    else:
        # P y su subindice desde la izquierda; «=» pegado al corchete
        out.append(texto(x, yc + tam * 0.35, rotulo, tam=tam, anclaje="start", color=SUAVE))
        if sub:
            out.append(texto(x + _ancho_txt(rotulo, tam) + 2, yc + tam * 0.35 + 6, sub,
                             tam=tam, anclaje="start", color=SUAVE))
        out.append(texto(x + pre - 8, yc + tam * 0.35, "=", tam=tam, anclaje="end",
                         color=SUAVE))
    xb = x + pre
    xe = xb + 6 + k * col
    for i in marcar:
        out.append(caja(_n(xb - 3), _n(y0 + 1 + alto_fila * i), _n(xe - xb + 6), alto_fila + 2,
                        relleno=mezclar(ACENTO, 0.16), borde=ACENTO, radio=4, grosor=1.5))
    if cols:
        for j, c in enumerate(cols):
            out.append(texto(xb + 3 + col * (j + 0.5), y0 - 6, c, tam=tam, color=SUAVE))
    for xx, d in ((xb, 5), (xe, -5)):
        out.append(f'<path d="M {_n(xx + d)} {_n(y0)} L {_n(xx)} {_n(y0)} L {_n(xx)} '
                   f'{_n(y0 + h)} L {_n(xx + d)} {_n(y0 + h)}" fill="none" '
                   f'stroke="{SUAVE}" stroke-width="1.5"/>')
    for i, f in enumerate(filas):
        for j, c in enumerate(f):
            out.append(texto(xb + 3 + col * (j + 0.5), y0 + 2 + alto_fila * (i + 0.5) + tam * 0.35,
                             c, tam=tam, peso="700" if c not in ("0", "⋮", "⋯", "⋱") else "normal",
                             color=TEXTO if c not in ("0",) else SUAVE))
    return xe


def _grafo_finito(out, p, yn):
    P, k = p["P"], len(p["P"])
    cerrado = {}
    for c in m.clases(P):
        for s in c["estados"]:
            cerrado[s] = c["cerrada"]
    pos = {i: (x, yn + dy) for i, (x, dy) in p["pos"].items()}
    for i in range(k):
        for j in range(k):
            if i == j or P[i][j] == 0:
                continue
            ida_y_vuelta = P[j][i] > 0
            out.append(_arista(pos[i], pos[j], fr(P[i][j]), r=R_EJ,
                               curva=-14 if ida_y_vuelta else 0, lado=-1, tam=12, desp=9))
    for i in range(k):
        if P[i][i] > 0:
            out.append(_lazo(*pos[i], fr(P[i][i]), r=R_EJ, hacia=p["lazos"].get(i, "arriba"),
                             tam=12, alcance=28))
    for i in range(k):
        c = cerrado[i]
        out.append(_gnodo(*pos[i], p["nombres"][i], COLOR_CERRADA if c else COLOR_ABIERTA,
                          r=R_EJ, guiones=None if c else "3 3", tam=13))


def _desc_finito(p):
    P, n = p["P"], p["nombres"]
    partes = []
    for i, f in enumerate(P):
        va = [f"a {n[j]} con {fr(x)}" if j != i else f"se queda con {fr(x)}"
              for j, x in enumerate(f) if x > 0]
        partes.append(f"{n[i]} " + " y ".join(va))
    filas = "; ".join(", ".join(fr(x) for x in f) for f in P)
    return "; ".join(partes) + f". Matriz por filas: {filas}."


def _corrimiento(out, yn):
    xs = (50, 120, 190)
    for a, b in zip(xs, xs[1:]):
        out.append(_arista((a, yn), (b, yn), "1", r=R_EJ, lado=-1, tam=12, desp=9))
    out.append(_flecha(xs[-1] + R_EJ, yn, 240, yn))
    out.append(texto(256, yn + 5, "⋯", tam=14, anclaje="middle"))
    for x, rot in zip(xs, ("0", "1", "2")):
        out.append(_gnodo(x, yn, rot, COLOR_ABIERTA, r=R_EJ, guiones="3 3", tam=13))
    return ("0 va a 1 con 1, 1 a 2 con 1, 2 a 3 con 1, y así sin fin; ningún estado "
            "regresa. Matriz infinita con unos arriba de la diagonal.")


def _caminata(out, yn):
    xs = (80, 150, 220)
    for a, b in zip(xs, xs[1:]):
        out.append(_arista((a, yn), (b, yn), "2/3", r=R_EJ, curva=-14, tam=12, desp=9))
        out.append(_arista((b, yn), (a, yn), "1/3", r=R_EJ, curva=-14, tam=12, desp=9))
    out.append(texto(36, yn + 5, "⋯", tam=14))
    out.append(texto(264, yn + 5, "⋯", tam=14))
    for x, rot in zip(xs, ("−1", "0", "1")):
        out.append(_gnodo(x, yn, rot, COLOR_CERRADA, r=R_EJ, tam=13))
    return ("En los enteros, cada k va a k + 1 con 2/3 y a k − 1 con 1/3. "
            "Matriz infinita: P(k, k+1) = 2/3, P(k, k−1) = 1/3.")


def _un_panel(out, y, lado, panel, dice):
    p = panel
    out.append(texto(X_PIE, y + 14, "✓ Lo cumple" if lado == "si" else "✗ No lo cumple",
                     tam=14, peso="700", anclaje="start"))
    out.append(texto(X_PIE, y + 33, dice, tam=13, anclaje="start", color=SUAVE))
    g0 = y + 44
    if p == "corrimiento":
        yn = g0 + 30
        desc = _corrimiento(out, yn)
        _matriz_svg(out, ANCHO / 2, yn + 72, [["0", "1", "0", "⋯"], ["0", "0", "1", "⋯"],
                                              ["0", "0", "0", "⋯"], ["⋮", "⋮", "⋮", "⋱"]])
        return yn + 112, desc
    if p == "caminata":
        yn = g0 + 30
        desc = _caminata(out, yn)
        out.append(texto(ANCHO / 2, yn + 50, "P(k, k+1) = 2/3,   P(k, k−1) = 1/3", tam=12,
                         peso="700"))
        return yn + 70, desc
    arriba = any(p["P"][i][i] > 0 and p["lazos"].get(i, "arriba") == "arriba"
                 for i in range(len(p["P"])))
    dys = [dy for _, dy in p["pos"].values()]
    yn = g0 + (56 if arriba else 26) - min(dys)
    _grafo_finito(out, p, yn)
    k = len(p["P"])
    ym = yn + max(dys) + 34 + k * 17 / 2
    _matriz_svg(out, ANCHO / 2, ym, [[fr(x) for x in f] for f in p["P"]])
    return ym + k * 17 / 2 + 10, _desc_finito(p)


def ejemplo(clave):
    e = EJEMPLOS[clave]
    titulo = ["Ejemplo y contraejemplo", e["titulo"]]
    out = []
    y = encabezado(out, titulo)
    descs = []
    for lado in ("si", "no"):
        panel, dice = e[lado]
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        y, d = _un_panel(out, y, lado, panel, dice)
        descs.append(("Lo cumple: " if lado == "si" else "No lo cumple: ") + dice + ". " + d)
        y += 8
    y = pie(out, y + 4, ["Verde, borde continuo: clase cerrada.",
                         "Amarillo, punteado: clase abierta."])
    return svg(titulo, " ".join(descs), out, y)


# =========================================================== CLASE 3 ===
#
# Figuras «mkv-c3-*» de course/8_markov/3_decidir/ (plan de la clase 3, §4 y
# §5). Cada cifra sale de markov.py (seccion «Decidir»). Notacion del plan
# §2: V(1), nunca V con subindice; politicas en palabras («caminar–correr»).
#
# Marcas: estado = circulo azul con su numero; meta = circulo verde con
# anillo doble; accion = punto pequeno, con su nombre y su recompensa al
# lado. En una politica o una codiciosa, la accion elegida va en el acento y
# con trazo continuo; la que no, punteada.

R_S, R_A = 18, 5
X_J2 = {1: 46, 2: 150, m.META: 254}
COLOR_META = COLOR_CERRADA
# desplazamiento del nodo de accion respecto a su estado
_OFF = {m.CAMINAR: (52, -44), m.CORRER: (40, 46), m.ESPERAR: (0, -56)}
# lado del rotulo de probabilidad en la flecha que avanza (+1: lado de la normal)
_LADO = {m.CAMINAR: -1, m.CORRER: 1}


def _v(x):
    """Una fraccion con signo menos tipografico: −5, −1/2."""
    return fr(x).replace("-", "−")


def _vd(x, cifras=3):
    return f"{float(x):.{cifras}f}".replace("-", "−")


def _aprox(x):
    """−467, o 1/3 ≈ 0.33 si no es entero."""
    x = F(x)
    return _v(x) if x.denominator == 1 else f"{_v(x)} ≈ {_vd(x, 2)}"


def _nombre_pol(pol):
    return f"{pol[1]}–{pol[2]}"


def _seg(a, b, r0=0.0, r1=0.0, color=SUAVE, punta=True, curva=0.0, grosor=2,
         guiones=None):
    """Curva cuadratica de a a b recortada por r0 y r1. Devuelve (svg, punto
    medio, normal unitaria del lado hacia donde se curva)."""
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / d, (x2 - x1) / d
    mx, my = (x1 + x2) / 2 + nx * curva, (y1 + y2) / 2 + ny * curva

    def rec(px, py, qx, qy, rr):
        L = math.hypot(qx - px, qy - py)
        return px + (qx - px) * rr / L, py + (qy - py) * rr / L
    sx, sy = rec(x1, y1, mx, my, r0)
    ex, ey = rec(x2, y2, mx, my, r1 + (2 if punta else 0))
    marca = ""
    if punta:
        marca = f' marker-end="url(#{"p" if color == ACENTO else "s"})"'
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    camino = (f'<path d="M {_n(sx)} {_n(sy)} Q {_n(mx)} {_n(my)} {_n(ex)} {_n(ey)}" '
              f'fill="none" stroke="{color}" stroke-width="{grosor}"{trazo}{marca}/>')
    medio = (0.25 * sx + 0.5 * mx + 0.25 * ex, 0.25 * sy + 0.5 * my + 0.25 * ey)
    s = 1 if curva >= 0 else -1
    return camino, medio, (nx * s, ny * s)


def _estado(cx, cy, rotulo):
    if rotulo == m.META:
        return (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{R_S + 5}" fill="none" '
                f'stroke="{COLOR_META}" stroke-width="2"/>'
                + _gnodo(cx, cy, "meta", COLOR_META, r=R_S, tam=12))
    return _gnodo(cx, cy, str(rotulo), COLOR_V, r=R_S, tam=15)


def _punto_accion(cx, cy, color=TEXTO):
    return (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{R_A}" fill="{color}" '
            f'stroke="{color}" stroke-width="1"/>')


def _grafo_mdp(out, mdp, y, acciones=None, resaltar=None, rotulos=None, xs=X_J2):
    """Estados en fila y, por cada (s, a) que se dibuja, su nodo de accion.
    acciones: dict s -> acciones a dibujar (por omision, todas). resaltar:
    dict s -> accion elegida (en el acento; las demas punteadas). rotulos:
    dict (s, a) -> segundo renglon (por omision «r = −3»). Devuelve la y de
    abajo del grafo."""
    acciones = acciones or mdp["acciones"]
    arriba = 92 if any(m.ESPERAR in acciones[s] for s in mdp["estados"]) else 80
    yn = y + arriba
    pos = {s: (xs[s], yn) for s in mdp["estados"]}
    pos[m.META] = (xs[m.META], yn)
    abajo = any(m.CORRER in acciones[s] for s in mdp["estados"])
    for s in mdp["estados"]:
        S = pos[s]
        for a in acciones[s]:
            dx, dy = _OFF[a]
            D = (S[0] + dx, S[1] + dy)
            elegida = resaltar is None or resaltar.get(s) == a
            color = ACENTO if resaltar and elegida else SUAVE
            guiones = None if elegida else "4 3"
            vuelve = s in mdp["P"][(s, a)]
            c = -12 if vuelve else 0
            camino, _, _ = _seg(S, D, R_S, R_A, color, punta=False, curva=c, guiones=guiones)
            out.append(camino)
            for t, p in mdp["P"][(s, a)].items():
                T = pos[t]
                camino, (qx, qy), (nx, ny) = _seg(D, T, R_A, R_S + (5 if t == m.META else 0),
                                                  color, curva=c if t == s else 0,
                                                  guiones=guiones)
                out.append(camino)
                lado = 1 if t == s else _LADO.get(a, 1)
                out.append(texto(qx + nx * 12 * lado, qy + ny * 12 * lado + 4, _v(p), tam=12,
                                 peso="700"))
            out.append(_punto_accion(*D, ACENTO if resaltar and elegida else TEXTO))
            segundo = (rotulos or {}).get((s, a), f"r = {_v(mdp['r'][(s, a)])}")
            if dy < 0:
                out.append(texto(D[0], D[1] - 24, a, tam=12, peso="700"))
                out.append(texto(D[0], D[1] - 10, segundo, tam=12))
            else:
                out.append(texto(D[0], D[1] + 22, a, tam=12, peso="700"))
                out.append(texto(D[0], D[1] + 37, segundo, tam=12))
    for s, (cx, cy) in pos.items():
        out.append(_estado(cx, cy, s))
    return yn + (88 if abajo else 34)


def _desc_mdp(mdp, acciones=None):
    acciones = acciones or mdp["acciones"]
    partes = []
    for s in mdp["estados"]:
        for a in acciones[s]:
            va = ", ".join((f"se queda con {fr(p)}" if t == s else f"a {t} con {fr(p)}")
                           for t, p in mdp["P"][(s, a)].items())
            partes.append(f"en {s}, {a} (r = {_v(mdp['r'][(s, a)])}): {va}")
    return "; ".join(partes) + "."


def _filas(M):
    return [[_v(x) for x in f] for f in M]


def _cols(mdp):
    return [str(s) for s in mdp["estados"]] + ["meta"]


def _matrices_mdp(out, y, mdp, acciones=(m.CAMINAR, m.CORRER), marcar=None):
    """Una matriz por accion, una debajo de otra; columnas rotuladas."""
    k = len(mdp["estados"])
    pre = max(_pre_matriz("P", a) for a in acciones)
    for a in acciones:
        yc = y + 22 + k * 17 / 2
        _matriz_svg(out, ANCHO / 2, yc, _filas(m.matriz_accion(mdp, a)), sub=a,
                    cols=_cols(mdp), marcar=(marcar or {}).get(a, ()), pre=pre)
        y = yc + k * 17 / 2 + 12
    return y


def _matriz_pi(out, y, mdp, pol, sub="π", pre=None):
    k = len(mdp["estados"])
    filas = [m.matriz_accion(mdp, pol[s])[i] for i, s in enumerate(mdp["estados"])]
    yc = y + 22 + k * 17 / 2
    _matriz_svg(out, ANCHO / 2, yc, _filas(filas), sub=sub, cols=_cols(mdp), pre=pre)
    return yc + k * 17 / 2 + 8, filas


def _panel_mdp(out, y, mdp, acciones=None, resaltar=None, rotulos=None, matrices=True):
    """Grafo del MDP y, debajo, una matriz por accion (plan §5)."""
    y = _grafo_mdp(out, mdp, y, acciones, resaltar, rotulos)
    if matrices:
        y = _matrices_mdp(out, y, mdp)
    return y


# ------------------------------------------------------------ graficas ---

def _plano(out, caja_px, xr, yr, xticks, yticks, xlab, ylab, fx=None, fy=None, log=False):
    """Ejes con rejilla. caja_px = (x0, top, x1, bot). Con log, yr va en
    log10 y yticks en valores. Devuelve (px, py)."""
    x0, top, x1, bot = caja_px
    fx = fx or (lambda v: _v(F(v).limit_denominator(100)))
    fy = fy or fx

    def px(x):
        return x0 + (x1 - x0) * (float(x) - xr[0]) / (xr[1] - xr[0])

    def py(v):
        v = math.log10(float(v)) if log else float(v)
        return bot - (bot - top) * (v - yr[0]) / (yr[1] - yr[0])
    for v in yticks:
        out.append(linea(x0, _n(py(v)), x1, _n(py(v)), color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(x0 - 8, py(v) + 4, fy(v), tam=12, anclaje="end", color=SUAVE))
    for v in xticks:
        out.append(linea(_n(px(v)), top, _n(px(v)), bot, color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(px(v), bot + 17, fx(v), tam=12, color=SUAVE))
    out.append(texto((x0 + x1) / 2, bot + 36, xlab, tam=13, peso="700"))
    out.append(texto(X_PIE, top - 12, ylab, tam=13, peso="700", anclaje="start"))
    return px, py


# --------------------------------------------------- el punto fijo, 1D ---

def _f_telarana(x):
    """La funcion de la pagina 1: f(x) = −1 + x/2 (plan §4, p1)."""
    return -1 + F(x) / 2


def _telarana(out, px, py, f, x0, pasos):
    """Iterar x ← f(x) desde x0: vertical a la curva, horizontal a y = x."""
    x = F(x0)
    xs = [x]
    camino = [(px(x), py(x))]
    for _ in range(pasos):
        fx = f(x)
        camino.append((px(x), py(fx)))
        camino.append((px(fx), py(fx)))
        x = fx
        xs.append(x)
    out.append(_polilinea(camino, ACENTO, grosor=2))
    for x in xs:
        out.append(_marca("circulo", px(x), py(x), ACENTO, r=3.5))
    return xs


def _panel_funcion(out, y, curvas, diagonal=True, xr=(-4, 1), yr=(-4, 1), alto=170,
                   telarana=None, marcas=(), pegada=None):
    """Grafica 1D: y = x punteada y las curvas [(f, color, guiones)].
    telarana = (f, x0, pasos). marcas = [(x, rotulo)] sobre y = x. pegada =
    (x_desde, x_hasta): tramo grueso donde la curva coincide con y = x."""
    top, bot = y + 30, y + 30 + alto
    px, py = _plano(out, (58, top, 280, bot), xr, yr, range(xr[0], xr[1] + 1),
                    range(yr[0], yr[1] + 1), "x", "y")
    def tramo(f, color, guiones=None, grosor=2):
        n = 80
        pts = []
        for i in range(n + 1):
            x = F(xr[0]) + F(xr[1] - xr[0]) * i / n
            v = f(x)
            if yr[0] <= v <= yr[1]:
                pts.append((px(x), py(v)))
        out.append(_polilinea(pts, color, guiones, grosor))
    if diagonal:
        tramo(lambda x: x, TEXTO, "2 4", 1.5)
    if pegada:
        a, b = pegada
        out.append(_polilinea([(px(a), py(a)), (px(b), py(b))], COLOR_C, None, 6))
    for f, color, guiones in curvas:
        tramo(f, color, guiones)
    xs = None
    if telarana:
        xs = _telarana(out, px, py, *telarana)
    for x, rot in marcas:
        out.append(f'<circle cx="{_n(px(x))}" cy="{_n(py(x))}" r="6" fill="none" '
                   f'stroke="{COLOR_CERRADA}" stroke-width="2.5"/>')
        out.append(texto(px(x) + 10, py(x) + 20, rot, tam=12, peso="700", anclaje="start"))
    return bot + 44, xs


# =============================================== figuras de la pagina 1 ===

def mkv_c3_punto_fijo():
    titulo = ["Iterar x ← f(x)", "f(x) = −1 + x/2, desde 0"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V), "y = f(x)"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], TEXTO, "2 4", 1.5), "y = x"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], ACENTO)
         + _marca("circulo", x, yy, ACENTO, r=3.5), "la telaraña: x ← f(x)"),
    ])
    y, xs = _panel_funcion(out, y, [(_f_telarana, COLOR_V, None)],
                           telarana=(_f_telarana, 0, 6), marcas=[(-2, "x = −2")])
    y = pie(out, y + 12, ["Sube o baja a la curva, cruza a y = x:",
                         "x = " + ", ".join(_v(x) for x in xs[:5]) + ", …",
                         "Cada vez a la mitad de distancia del",
                         "cruce en −2; se acerca, nunca llega."], color=TEXTO)
    desc = ("Gráfica de y = f(x) = −1 + x/2 y de y = x, con x de −4 a 1. Se cruzan una vez, "
            "en x = −2: el punto fijo. La telaraña itera x ← f(x) desde 0: "
            + ", ".join(_v(x) for x in xs) + "; la distancia a −2 se parte a la mitad en "
            "cada paso y nunca llega a cero.")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 2 ===

def _escalera_grafo(out, yn, resbalon=None, marcar_ruta=None, rotulo_falta=True):
    """Escalones 0..5 en fila; brincos de 1 abajo de la fila? No: los de 1
    rectos y los de 2 en arco (pares arriba, impares abajo)."""
    xs = {s: 64 + 43 * s for s in range(6)}
    ruta = set(zip(marcar_ruta, marcar_ruta[1:])) if marcar_ruta else set()
    for s in range(5):
        for a in (1, 2):
            t = s + a
            if t > 5:
                continue
            en_ruta = (s, t) in ruta
            color = ACENTO if en_ruta else SUAVE
            grosor = 2 if en_ruta else 1.5
            if a == 1:
                camino, _, _ = _seg((xs[s], yn), (xs[t], yn), 14, 14, color, grosor=grosor)
            else:
                curva = -30 if s % 2 == 0 else 30
                camino, _, _ = _seg((xs[s], yn), (xs[t], yn), 14, 14, color, curva=curva,
                                    grosor=grosor)
            out.append(camino)
    if resbalon is not None:
        out.append(_lazo(xs[resbalon], yn, "1/2", r=14, hacia="abajo", tam=12, alcance=36))
    for s in range(6):
        out.append(_gnodo(xs[s], yn, str(s), COLOR_META if s == 5 else COLOR_V, r=14, tam=13))
    return xs


def mkv_c3_escalera():
    cost = m.ESCALERA_COSTOS
    costo = m.escalera_costo()
    ruta = m.escalera_ruta_optima()
    cod = m.escalera_codiciosa()
    titulo = ["La escalera", "brinca 1 o 2; pisar cuesta"]
    out = []
    y = encabezado(out, titulo)
    # dibujo: escalones que suben a la derecha
    base, x0, w, h = y + 150, 72, 35, 20
    for s in range(6):
        top = base - h * (s + 1)
        flojo = s > 0 and cost[s - 1] == max(cost)
        out.append(caja(_n(x0 + w * s), _n(top), w, _n(base - top), radio=2,
                        relleno=mezclar(COLOR_C if flojo else LINEA, 0.25),
                        borde=COLOR_C if flojo else SUAVE, grosor=1.5,
                        guiones="4 3" if flojo else None))
        out.append(texto(x0 + w * s + w / 2, top + 15, str(s), tam=13, peso="700"))
        if flojo:
            out.append(texto(x0 + w * s + w / 2, base - 8, "flojo", tam=12, color=COLOR_C))
    # la ruta optima: arcos del centro de un escalon al de otro
    for a, b in zip(ruta, ruta[1:]):
        ya, yb = base - h * (a + 1) - 4, base - h * (b + 1) - 4
        xa, xb = x0 + w * a + w / 2, x0 + w * b + w / 2
        out.append(_curva(f"M {_n(xa)} {_n(ya)} Q {_n((xa + xb) / 2)} {_n(min(ya, yb) - 34)} "
                          f"{_n(xb)} {_n(yb - 4)}", color=ACENTO).replace('url(#s)', 'url(#p)'))
    out.append(texto(X_PIE, base - 128, "ruta óptima", tam=12, peso="700", anclaje="start",
                     color=ACENTO))
    # tabla alineada con los escalones
    filas = [("escalón", [str(s) for s in range(6)], "700"),
             ("pisar", ["—"] + [str(c) for c in cost], "normal"),
             ("falta", [str(c) for c in costo], "700")]
    yt = base + 24
    for k, (rot, vals, peso) in enumerate(filas):
        out.append(texto(X_PIE, yt + 20 * k, rot, tam=13, anclaje="start", color=SUAVE))
        for s, v in enumerate(vals):
            out.append(texto(x0 + w * s + w / 2, yt + 20 * k, v, tam=13, peso=peso,
                             color=TEXTO if k != 1 else SUAVE))
    y = pie(out, yt + 66, [
        "Fila «falta»: lo que falta pagar desde",
        "ese escalón, de 5 hacia atrás.",
        "Óptima: " + " → ".join(map(str, ruta)) + f", paga {m.costo_ruta(ruta)}.",
        "La codiciosa (pisa el más barato):",
        " → ".join(map(str, cod)) + f", paga {m.costo_ruta(cod)}."], color=TEXTO)
    desc = ("Escalera de escalones 0 a 5 que suben a la derecha; desde cada escalón se brinca "
            "1 o 2 sin pasarse del 5. Pisar los escalones 1 a 5 cuesta "
            + ", ".join(map(str, cost)) + " (el 3 está flojo). Lo que falta pagar desde cada "
            "escalón, de 0 a 5: " + ", ".join(map(str, costo)) + ". La ruta óptima, marcada, es "
            + " → ".join(map(str, ruta)) + f" y paga {m.costo_ruta(ruta)}; la codiciosa, que pisa "
            "el siguiente más barato, es " + " → ".join(map(str, cod))
            + f" y paga {m.costo_ruta(cod)}.")
    return svg(titulo, desc, out, y)


def _arbol_rutas():
    """El arbol de llamadas de rutas(0): cada nodo es un escalon; sus hijos,
    los escalones a 1 y 2 brincos. Devuelve [(nivel, escalon, x, padre)]."""
    nodos = []
    hojas = [0]

    def baja(s, nivel, padre):
        i = len(nodos)
        nodos.append([nivel, s, None, padre])
        hijos = [s + a for a in (1, 2) if s + a <= 5]
        if not hijos:
            nodos[i][2] = 26 + 35 * hojas[0]
            hojas[0] += 1
        else:
            xs = [baja(t, nivel + 1, i) for t in hijos]
            nodos[i][2] = sum(xs) / len(xs)
        return nodos[i][2]
    baja(0, 0, None)
    return nodos


def mkv_c3_escalera_arbol_vs_grafo():
    rutas = m.escalera_rutas()
    nodos = _arbol_rutas()
    hojas = sum(1 for n in nodos if n[1] == 5)
    assert hojas == rutas[0] == len(m.escalera_todas_las_rutas())
    titulo = ["Contar rutas: árbol", "contra grafo"]
    out = []
    y = encabezado(out, titulo)
    out.append(texto(X_PIE, y + 6, f"El árbol de rutas(0): {len(nodos)} nodos", tam=14,
                     peso="700", anclaje="start"))
    y0 = y + 36
    dy = 40
    for nivel, s, x, padre in nodos:
        if padre is not None:
            pn = nodos[padre]
            out.append(linea(_n(pn[2]), _n(y0 + dy * pn[0] + 11), _n(x),
                             _n(y0 + dy * nivel - 11), color=SUAVE, grosor=1.5))
    for nivel, s, x, padre in nodos:
        out.append(_gnodo(x, y0 + dy * nivel, str(s), COLOR_META if s == 5 else COLOR_V, r=11,
                          tam=12))
    prof = max(n[0] for n in nodos)
    y = y0 + dy * prof + 30
    veces = {s: sum(1 for n in nodos if n[1] == s) for s in range(6)}
    y = pie(out, y, [f"{hojas} hojas = {hojas} rutas. El 3 aparece {veces[3]} veces,",
                     f"el 4, {veces[4]}: el árbol repite la cuenta."], color=TEXTO)
    y += 8
    out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
    out.append(texto(X_PIE, y + 14, "El grafo: 6 nodos, uno por escalón", tam=14, peso="700",
                     anclaje="start"))
    yn = y + 62
    xs = _escalera_grafo(out, yn)
    out.append(texto(X_PIE, yn + 50, "rutas", tam=12, anclaje="start", color=SUAVE))
    for s in range(6):
        out.append(texto(xs[s], yn + 50, str(rutas[s]), tam=13, peso="700"))
    y = pie(out, yn + 80, ["Hacia atrás: rutas(s) = rutas(s + 1) +",
                            "rutas(s + 2); cada escalón se cuenta",
                            "una sola vez."], color=TEXTO)
    desc = (f"Arriba, el árbol de llamadas de rutas(0): {len(nodos)} nodos y {hojas} hojas, todas "
            f"en el escalón 5; el escalón 3 aparece {veces[3]} veces y el 4, {veces[4]}. Abajo, "
            "el grafo de la escalera: 6 nodos, de 0 a 5, con un brinco de 1 a s + 1 y uno de 2 "
            "a s + 2. Rutas desde cada escalón, de 0 a 5: " + ", ".join(map(str, rutas)) + ".")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 3 ===

def mkv_c3_pasillo():
    mdp = m.pasillo()
    r = mdp["r"]
    caminar = -r[(1, m.CAMINAR)]
    p_resbala = mdp["P"][(1, m.CORRER)][1]
    castigo = (r[(2, m.CORRER)] - r[(1, m.CORRER)]) / p_resbala
    titulo = ["El robot en el pasillo", "mojado"]
    out = []
    y = encabezado(out, titulo)
    yc = y + 40
    cx = {"1": 114, "2": 190, "meta": 266}
    out.append(texto(36, yc + 8, "inicio", tam=12, peso="700"))
    out.append(_flecha(60, yc + 4, 77, yc + 4))
    for rot, x in cx.items():
        meta = rot == "meta"
        out.append(caja(_n(x - 32), _n(yc - 22), 64, 52, radio=6,
                        relleno=mezclar(COLOR_META if meta else COLOR_V, 0.16),
                        borde=COLOR_META if meta else COLOR_V, grosor=2))
        out.append(texto(x, yc + 10, rot, tam=16, peso="700"))
    out.append(_flecha(147, yc + 4, 155, yc + 4))
    out.append(_flecha(223, yc + 4, 231, yc + 4))
    # el hueco junto a la 1 y el barandal junto a la 2
    out.append(caja(86, _n(yc + 40), 56, 26, radio=13, relleno="#000000", borde=COLOR_C,
                    grosor=2, guiones="4 3"))
    out.append(texto(114, yc + 84, "hueco", tam=13, peso="700"))
    out.append(texto(114, yc + 100, "sin barandal", tam=12, color=SUAVE))
    out.append(linea(162, _n(yc + 46), 218, _n(yc + 46), color=SUAVE, grosor=3))
    for x in (166, 181, 196, 211):
        out.append(linea(x, _n(yc + 46), x, _n(yc + 62), color=SUAVE, grosor=2))
    out.append(texto(190, yc + 84, "barandal", tam=13, peso="700"))
    y = yc + 128
    y = pie(out, y, [f"Caminar: avanza seguro; cuesta {fr(caminar)}.",
                     "Correr: cuesta 1; con " + fr(1 - p_resbala) + " avanza,",
                     f"con {fr(p_resbala)} resbala de lado y se queda.",
                     f"En la 1, resbalar es caer al hueco:",
                     f"lo levantan y cuesta {fr(castigo)} más.",
                     "En la 2, el barandal lo detiene."], color=TEXTO)
    desc = ("Pasillo: inicio, casilla 1, casilla 2 y la meta, en fila. Junto a la casilla 1 hay "
            "un hueco sin barandal; junto a la 2, un barandal. Caminar avanza seguro y cuesta "
            f"{fr(caminar)}. Correr cuesta 1: con {fr(1 - p_resbala)} avanza y con "
            f"{fr(p_resbala)} resbala de lado y se queda en su casilla; en la 1, al resbalar "
            f"cae al hueco y cuesta {fr(castigo)} más.")
    return svg(titulo, desc, out, y)


def mkv_c3_pasillo_mdp():
    mdp = m.pasillo()
    titulo = ["El pasillo como MDP", "estados, acciones, P y r"]
    out = []
    y = encabezado(out, titulo)
    y = _panel_mdp(out, y, mdp)
    y = pie(out, y + 14, ["Punto: una acción, con su recompensa", "esperada r(s, a). Fila = desde;",
                         "columna = hacia. Cada fila suma 1."])
    desc = ("MDP del pasillo: estados 1 y 2 y la meta. " + _desc_mdp(mdp)
            + " Debajo, P caminar y P correr, filas desde 1 y 2, columnas hacia 1, 2 y meta: "
            + " / ".join("; ".join(", ".join(_v(x) for x in f) for f in m.matriz_accion(mdp, a))
                         for a in (m.CAMINAR, m.CORRER)) + ".")
    return svg(titulo, desc, out, y)


def mkv_c3_politica_elige_filas():
    mdp = m.pasillo()
    pol = m.POLITICAS_J2["caminar–correr"]
    titulo = ["La política elige filas", "caminar–correr"]
    out = []
    y = encabezado(out, titulo)
    y = pie(out, y + 2, ["Caminar en 1, correr en 2: la fila 1", "sale de P caminar y la 2, de P correr."],
            color=TEXTO)
    marcar = {m.CAMINAR: (0,), m.CORRER: (1,)}
    y = _matrices_mdp(out, y, mdp, marcar=marcar)
    out.append(_flecha(ANCHO / 2, y + 2, ANCHO / 2, y + 24))
    y, filas = _matriz_pi(out, y + 26, mdp, pol,
                          pre=max(_pre_matriz("P", a) for a in (m.CAMINAR, m.CORRER)))
    PT, rpi = m.cadena_politica(mdp, pol)
    y = pie(out, y + 16, [f"Recompensas: ({', '.join(_v(x) for x in rpi)}); cada estado",
                         "paga la de su acción.",
                         "Pπ ya es una cadena de Markov."], color=TEXTO)
    desc = ("La política caminar–correr elige la fila 1 de P caminar ("
            + ", ".join(_v(x) for x in filas[0]) + ") y la fila 2 de P correr ("
            + ", ".join(_v(x) for x in filas[1]) + "), marcadas; juntas forman Pπ, la matriz de la política. Recompensas: ("
            + ", ".join(_v(x) for x in rpi) + ").")
    return svg(titulo, desc, out, y)


def mkv_c3_cuatro_cadenas():
    mdp = m.pasillo()
    titulo = ["Las cuatro políticas,", "cada una una cadena"]
    out = []
    y = encabezado(out, titulo)
    descs = []
    for nombre, pol in m.POLITICAS_J2.items():
        V = m.evaluar_politica(mdp, pol)
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        out.append(texto(X_PIE, y + 14, nombre, tam=14, peso="700", anclaje="start"))
        out.append(texto(X_PIE, y + 32, f"V(1) = {_v(V[1])}, V(2) = {_v(V[2])}",
                         tam=13, anclaje="start", color=SUAVE))
        acc = {s: [pol[s]] for s in mdp["estados"]}
        y = _grafo_mdp(out, mdp, y + 40, acc)
        descs.append(f"{nombre}: " + _desc_mdp(mdp, acc)[:-1]
                     + f"; V(1) = {_v(V[1])}, V(2) = {_v(V[2])}.")
        y += 4
    y = pie(out, y + 4, ["Fijar la política deja una sola acción", "por estado: una cadena con meta."])
    desc = "Las cuatro políticas del pasillo, cada una dibujada como su cadena. " + " ".join(descs)
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 4 ===

def mkv_c3_cuatro_politicas_plano():
    mdp = m.pasillo()
    vals = {n: m.evaluar_politica(mdp, p) for n, p in m.POLITICAS_J2.items()}
    optima = max(vals, key=lambda n: (vals[n][1], vals[n][2]))
    assert all(vals[optima][s] >= v[s] for v in vals.values() for s in (1, 2))
    titulo = ["Las cuatro políticas", "en el plano V(1)–V(2)"]
    out = []
    y = encabezado(out, titulo)
    top = y + 34
    px, py = _plano(out, (58, top, 280, top + 180), (-16, 0), (-4, 0), range(-16, 1, 4),
                    range(-4, 1), "V(1)", "V(2)")
    formas = dict(zip(m.POLITICAS_J2, ("cuadro", "circulo", "triangulo", "rombo")))
    # la esquina que domina la optima
    xo, yo = px(vals[optima][1]), py(vals[optima][2])
    out.append(linea(_n(xo), _n(yo), _n(xo), _n(py(-4)), color=ACENTO, grosor=1, guiones="3 3"))
    out.append(linea(_n(xo), _n(yo), _n(px(-16)), _n(yo), color=ACENTO, grosor=1, guiones="3 3"))
    for n, V in vals.items():
        color = ACENTO if n == optima else COLOR_V
        out.append(_marca(formas[n], px(V[1]), py(V[2]), color, r=5))
    yl = top + 180 + 58
    y = _leyenda(out, yl, [(lambda x, yy, n=n: _marca(formas[n], x, yy,
                                                       ACENTO if n == optima else COLOR_V, r=5),
                            f"{n}: ({_v(vals[n][1])}, {_v(vals[n][2])})") for n in vals])
    y = pie(out, y + 6, ["Las otras tres caen abajo o a la",
                         f"izquierda de {optima} (punteado):",
                         "ninguna la supera desde 1 ni desde 2."], color=TEXTO)
    desc = ("Las cuatro políticas del pasillo como puntos (V(1), V(2)): "
            + "; ".join(f"{n} ({_v(V[1])}, {_v(V[2])})" for n, V in vals.items())
            + f". Las otras tres caen abajo o a la izquierda de {optima}: ninguna la supera "
            "desde 1 ni desde 2.")
    return svg(titulo, desc, out, y)


def mkv_c3_simular_politica():
    mdp = m.pasillo()
    pol = m.POLITICAS_J2["caminar–correr"]
    g = m.simular_politica(mdp, pol)
    media, ee = m.resumen_simulacion()
    V = m.evaluar_politica(mdp, pol)
    n = len(g)
    cuenta = {}
    for x in g:
        cuenta[x] = cuenta.get(x, 0) + 1
    hi = max(cuenta)
    corte = hi - 6          # las colas largas se juntan en «o menos»
    barras = [(v, cuenta.get(v, 0)) for v in range(hi, corte, -1)]
    resto = sum(c for v, c in cuenta.items() if v <= corte)
    barras.append((corte, resto))
    titulo = ["Simular caminar–correr", f"{miles(n)} episodios desde 1"]
    out = []
    y = encabezado(out, titulo)
    top, bot = y + 34, y + 214
    tope = max(c for _, c in barras)
    escala = 10 ** int(math.log10(tope))
    tope_eje = math.ceil(tope / escala) * escala
    x0, x1 = 64, 280
    paso = (x1 - x0) / len(barras)
    for k in range(0, tope_eje + 1, tope_eje // 5 if tope_eje // 5 else 1):
        yy = bot - (bot - top) * k / tope_eje
        out.append(linea(x0, _n(yy), x1, _n(yy), color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(x0 - 8, yy + 4, miles(k), tam=12, anclaje="end", color=SUAVE))
    out.append(texto(X_PIE, top - 12, "episodios", tam=13, peso="700", anclaje="start"))
    for i, (v, c) in enumerate(barras):
        h = (bot - top) * c / tope_eje
        xb = x0 + paso * i
        out.append(f'<rect x="{_n(xb + 3)}" y="{_n(bot - h)}" width="{_n(paso - 6)}" '
                   f'height="{_n(h)}" fill="{mezclar(COLOR_V, 0.5)}" stroke="{COLOR_V}" '
                   f'stroke-width="1"/>')
        rot = _v(v) if i < len(barras) - 1 else f"≤{_v(v)}"
        out.append(texto(xb + paso / 2, bot + 17, rot, tam=12, color=SUAVE))
    out.append(texto((x0 + x1) / 2, bot + 36, "retorno del episodio", tam=13, peso="700"))
    xm = x0 + paso * (hi - media) + paso / 2
    out.append(linea(_n(xm), top + 30, _n(xm), bot, color=ACENTO, grosor=2, guiones="5 3"))
    out.append(texto(xm + 6, top + 44, f"media {_vd(media, 2)}", tam=12, peso="700",
                     anclaje="start", color=ACENTO))
    y = pie(out, bot + 62, [f"Media: {_vd(media)}; error estándar: {_vd(ee)}.",
                            f"La cuenta exacta da V(1) = {_v(V[1])}.",
                            "Ningún episodio vale la media: el",
                            f"retorno es entero; el más común, {_v(hi)}."], color=TEXTO)
    desc = (f"Histograma del retorno de {miles(n)} episodios de caminar–correr desde la casilla 1 "
            f"(semilla {m.SEMILLAS['c3-simular-politica']}). "
            + "; ".join(f"{_v(v) if i < len(barras) - 1 else 'menos de ' + _v(v + 1)}: "
                        f"{miles(c)}" for i, (v, c) in enumerate(barras))
            + f". Media {_vd(media)}, error estándar {_vd(ee)}; el valor exacto es "
            f"V(1) = {_v(V[1])}.")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 5 ===

def _bellman_2(mdp):
    """y(x) = max_a q(s = 2, a) con V(2) = x: la ecuacion de Bellman en 2."""
    def f(x):
        return max(m.q_valor(mdp, {1: F(0), 2: F(x)}, 2, a) for a in mdp["acciones"][2])
    return f


def _accion_2(mdp, a):
    def f(x):
        return m.q_valor(mdp, {1: F(0), 2: F(x)}, 2, a)
    return f


def mkv_c3_bellman_1d():
    mdp = m.pasillo()
    f = _bellman_2(mdp)
    V = m.evaluar_politica(mdp, m.POLITICAS_J2["caminar–correr"])
    assert f(V[2]) == V[2]
    titulo = ["Bellman en la casilla 2", "y = máx(caminar, correr)"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_C, "6 4"),
         f"caminar: {_v(mdp['r'][(2, m.CAMINAR)])}"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V, "2 3"),
         f"correr: {_v(mdp['r'][(2, m.CORRER)])} + x/2"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], ACENTO, None, 3),
         "el máximo de las dos"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], TEXTO, "2 4", 1.5), "y = x"),
    ])
    y, _ = _panel_funcion(out, y, [(_accion_2(mdp, m.CAMINAR), COLOR_C, "6 4"),
                                   (_accion_2(mdp, m.CORRER), COLOR_V, "2 3"),
                                   (f, ACENTO, None)],
                          marcas=[(V[2], f"V(2) = {_v(V[2])}")])
    y = pie(out, y + 12, ["x es V(2): lo que vale la casilla 2.",
                         f"Un solo cruce con y = x, en {_v(V[2])}: ahí",
                         "correr gana a caminar."], color=TEXTO)
    desc = ("Ecuación de Bellman en la casilla 2 como gráfica de una variable, x = V(2): "
            f"caminar vale {_v(mdp['r'][(2, m.CAMINAR)])}, correr vale "
            f"{_v(mdp['r'][(2, m.CORRER)])} + x/2, y y = máx de las dos. Cruza a y = x una sola "
            f"vez, en x = {_v(V[2])}, donde correr es la mayor.")
    return svg(titulo, desc, out, y)


def _politicas_optimas(mdp):
    """La mejor de las cuatro politicas de J2 en todo estado, o None si
    ninguna domina (se calcula con evaluar_politica, no con la formula)."""
    vals = {n: m.evaluar_politica(mdp, p) for n, p in m.POLITICAS_J2.items()}
    mejores = [n for n, V in vals.items()
               if all(V[s] >= W[s] for W in vals.values() for s in mdp["estados"])]
    return mejores


def mkv_c3_fronteras():
    titulo = ["¿Correr o caminar?", "según costo y castigo"]
    out = []
    y = encabezado(out, titulo)
    W, X = (0, 6), (0, 12)
    top = y + 34
    px, py = _plano(out, (58, top, 280, top + 220), W, X, range(0, 7), range(0, 13, 2),
                    "costo de caminar", "castigo del hueco")
    # fronteras de la pagina 5: correr en 2 si costo > 2; correr en 1 si castigo < costo − 2
    out.append(linea(_n(px(2)), _n(py(12)), _n(px(2)), _n(py(0)), color=TEXTO, grosor=2))
    out.append(linea(_n(px(2)), _n(py(0)), _n(px(6)), _n(py(4)), color=TEXTO, grosor=2))
    regiones = [(F(1), F(6)), (F(4), F(9)), (F(5), F(1, 2))]
    nombres = []
    for w, x in regiones:
        mejores = _politicas_optimas(m.pasillo(caminar=w, castigo=x))
        assert len(mejores) == 1, (w, x, mejores)
        nombres.append(mejores[0])
    # la frontera dibujada es la que da el calculo, en una rejilla
    for w in range(0, 7):
        for x in range(0, 13):
            mej = _politicas_optimas(m.pasillo(caminar=w, castigo=x))
            corre2, corre1 = w > 2, x < w - 2
            if w != 2 and x != w - 2:
                esperado = f"{'correr' if corre1 else 'caminar'}–{'correr' if corre2 else 'caminar'}"
                assert mej == [esperado], (w, x, mej)
    pos_rot = [(1, 9), (4.4, 6.5), (5, 0.9)]
    for (wx, xx), n in zip(pos_rot, nombres):
        a, b = n.split("–")
        out.append(texto(px(wx), py(xx), a + "–", tam=12, peso="700"))
        out.append(texto(px(wx), py(xx) + 15, b, tam=12, peso="700"))
    J = m.pasillo()
    w0, x0 = -J["r"][(1, m.CAMINAR)], (J["r"][(2, m.CORRER)] - J["r"][(1, m.CORRER)]) * 2
    out.append(f'<circle cx="{_n(px(w0))}" cy="{_n(py(x0))}" r="6" fill="{ACENTO}" '
               f'stroke="{ACENTO}" stroke-width="1"/>')
    out.append(texto(px(w0) + 10, py(x0) + 22, "el pasillo", tam=12, peso="700", anclaje="start",
                     color=ACENTO))
    y = pie(out, top + 220 + 62, [
        "Raya vertical: costo de caminar = 2;",
        "a la derecha conviene correr en 2.",
        "Raya inclinada: castigo = costo − 2;",
        "debajo conviene correr también en 1.",
        f"El pasillo: costo {fr(w0)}, castigo {fr(x0)}."], color=TEXTO)
    desc = ("Mapa de la mejor política del pasillo según el costo de caminar (de 0 a 6) y el "
            "castigo del hueco (de 0 a 12). Raya vertical en costo = 2: a la derecha conviene "
            "correr en 2. Raya inclinada castigo = costo − 2: debajo conviene correr también en "
            "1. Regiones: " + "; ".join(nombres) + f". El pasillo (costo {fr(w0)}, castigo "
            f"{fr(x0)}) cae en {_politicas_optimas(J)[0]}. En las rayas, "
            "empatan.")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 6 ===

def mkv_c3_iterar_valores():
    mdp = m.pasillo()
    T = 8
    traza = m.iterar_valores(mdp, rondas=T)
    Vs = m.evaluar_politica(mdp, m.POLITICAS_J2["caminar–correr"])
    titulo = ["Iteración de valores", "en el pasillo, desde 0"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V)
         + _marca("circulo", x, yy, COLOR_V), "V⁽ᵏ⁾(1)"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_C, "5 4")
         + _marca("cuadro", x, yy, COLOR_C, r=4), "V⁽ᵏ⁾(2)"),
        (lambda x, yy: linea(x - 12, yy, x + 12, yy, color=TEXTO, grosor=1, guiones="1 3"),
         f"V*: {_v(Vs[1])} y {_v(Vs[2])}"),
    ])
    top = y + 30
    px, py = _plano(out, (58, top, 280, top + 190), (0, T), (-6, 0), range(0, T + 1),
                    range(-6, 1), "ronda k", "valor")
    for s in (1, 2):
        out.append(linea(58, _n(py(Vs[s])), 280, _n(py(Vs[s])), color=TEXTO, grosor=1,
                         guiones="1 3"))
    for s, color, forma, g in ((1, COLOR_V, "circulo", None), (2, COLOR_C, "cuadro", "5 4")):
        pts = [(px(t), py(V[s])) for t, V in enumerate(traza)]
        out.append(_polilinea(pts, color, g))
        for x, yy in pts:
            out.append(_marca(forma, x, yy, color, r=4))
    y = pie(out, top + 190 + 62, [
        "Cada ronda acerca los dos valores a V*:",
        "V⁽ᵏ⁾ es lo mejor con k pasos restantes.",
        "Bajan sin pasarse y nunca llegan."], color=TEXTO)
    desc = (f"Iteración de valores en el pasillo desde V⁽⁰⁾ = 0, rondas 0 a {T}. V⁽ᵏ⁾(1): "
            + ", ".join(_v(V[1]) for V in traza) + ". V⁽ᵏ⁾(2): "
            + ", ".join(_v(V[2]) for V in traza)
            + f". Las dos bajan hacia V*(1) = {_v(Vs[1])} y V*(2) = {_v(Vs[2])} sin llegar.")
    return svg(titulo, desc, out, y)


def _serie_log(out, px, py, valores, color, forma, guiones=None, t0=1):
    pts = [(px(t0 + i), py(v)) for i, v in enumerate(valores)]
    out.append(_polilinea(pts, color, guiones))
    for x, yy in pts:
        out.append(_marca(forma, x, yy, color, r=4))


_EXP = {k: ("10" + str(k).replace("-", "⁻").translate(SUPER)) if k not in (0, 1)
        else ("1" if k == 0 else "10") for k in range(-6, 4)}


def _fy_log(v):
    return _EXP[round(math.log10(float(v)))]


def mkv_c3_residuo():
    mdp = m.pasillo()
    T = 10
    traza = m.iterar_valores(mdp, rondas=T)
    Vs = m.evaluar_politica(mdp, m.POLITICAS_J2["caminar–correr"])
    res = m.residuos(traza)
    err = m.errores(traza, Vs)[1:]
    mm, beta = 3, m.prob_no_terminar(mdp, 3)
    cota = m.cota_paro(mm, beta)
    titulo = ["Residuo, error y cota", "escala log"]
    out = []
    y = encabezado(out, titulo)
    y = _leyenda(out, y + 8, [
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_V)
         + _marca("circulo", x, yy, COLOR_V), "residuo res⁽ᵏ⁾"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], COLOR_C, "5 4")
         + _marca("cuadro", x, yy, COLOR_C, r=4), "error máx |V* − V⁽ᵏ⁾|"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], ACENTO, "2 3")
         + _marca("triangulo", x, yy, ACENTO, r=4), f"cota: {fr(cota)} × residuo"),
    ])
    top = y + 30
    px, py = _plano(out, (58, top, 280, top + 190), (1, T), (-3, 2), range(1, T + 1),
                    [10 ** k for k in range(-3, 3)], "ronda k", "tamaño", fy=_fy_log, log=True)
    _serie_log(out, px, py, [cota * r for r in res], ACENTO, "triangulo", "2 3")
    _serie_log(out, px, py, err, COLOR_C, "cuadro", "5 4")
    _serie_log(out, px, py, res, COLOR_V, "circulo")
    y = pie(out, top + 190 + 62, [
        f"m = {mm}, β = {fr(beta)}: la cota es {fr(cota)} × residuo.",
        "El error real queda debajo; parar con",
        "residuo ≤ tol garantiza error ≤ " + fr(cota) + " tol."], color=TEXTO)
    desc = (f"Escala logarítmica, rondas 1 a {T} de la iteración de valores en el pasillo. "
            "Residuo: " + ", ".join(_v(r) for r in res) + ". Error máximo contra V*: "
            + ", ".join(_v(e) for e in err) + f". Cota con m = {mm} y β = {fr(beta)}: "
            f"{fr(cota)} × residuo, siempre por encima del error.")
    return svg(titulo, desc, out, y)


@lru_cache(maxsize=None)
def _pasillo_largo_valores():
    d = m.pasillo_largo()
    mdp = m.pasillo(n=m.N_PASILLO)
    return d, mdp, m.evaluar_politica(mdp, d["politica"])


def mkv_c3_pasillo_largo():
    d, mdp, V = _pasillo_largo_valores()
    pol = d["politica"]
    n = len(mdp["estados"])
    titulo = ["El pasillo largo", f"{n} casillas"]
    out = []
    y = encabezado(out, titulo)
    k = 24
    out.append(texto(X_PIE, y + 6, f"La política óptima, casillas 1 a {k}", tam=13, peso="700",
                     anclaje="start"))
    x0, w = 20, 260 / k
    yc = y + 22
    for i in range(1, k + 1):
        corre = pol[i] == m.CORRER
        out.append(f'<rect x="{_n(x0 + w * (i - 1) + 1)}" y="{_n(yc)}" width="{_n(w - 2)}" '
                   f'height="22" fill="{mezclar(COLOR_C if corre else COLOR_V, 0.55 if corre else 0.2)}" '
                   f'stroke="{COLOR_C if corre else COLOR_V}" stroke-width="1"'
                   + ("" if corre else ' stroke-dasharray="2 2"') + "/>")
        if i % 3 == 1:
            cx = x0 + w * (i - 0.5)
            out.append(f'<polygon points="{_n(cx - 4)},{_n(yc + 27)} {_n(cx + 4)},{_n(yc + 27)} '
                       f'{_n(cx)},{_n(yc + 34)}" fill="{COLOR_C}"/>')
    for i in (1, 6, 12, 18, 24):
        out.append(texto(x0 + w * (i - 0.5), yc + 50, str(i), tam=12, color=SUAVE))
    y = _leyenda(out, yc + 76, [
        (lambda x, yy: f'<rect x="{_n(x - 7)}" y="{_n(yy - 8)}" width="14" height="16" '
                       f'fill="{mezclar(COLOR_V, 0.2)}" stroke="{COLOR_V}" stroke-width="1" '
                       f'stroke-dasharray="2 2"/>', "caminar"),
        (lambda x, yy: f'<rect x="{_n(x - 7)}" y="{_n(yy - 8)}" width="14" height="16" '
                       f'fill="{mezclar(COLOR_C, 0.55)}" stroke="{COLOR_C}" stroke-width="1"/>',
         "correr"),
        (lambda x, yy: f'<polygon points="{_n(x - 4)},{_n(yy - 6)} {_n(x + 4)},{_n(yy - 6)} '
                       f'{_n(x)},{_n(yy + 1)}" fill="{COLOR_C}"/>', "hueco sin barandal"),
    ])
    camina = sorted({i % 3 for i in mdp["estados"] if pol[i] == m.CAMINAR})
    assert camina == [1], camina
    top = y + 34
    vmin = min(V.values())
    piso = -100 * math.ceil(-float(vmin) / 100)
    px, py = _plano(out, (64, top, 280, top + 160), (0, n), (piso, 0), range(0, n + 1, 50),
                    range(piso, 1, 100), "casilla i", "V*(i)", fx=lambda v: str(v),
                    fy=lambda v: _v(v))
    out.append(_polilinea([(px(i), py(V[i])) for i in mdp["estados"]], ACENTO))
    y = pie(out, top + 160 + 62, [
        "Camina junto a cada hueco (i = 1, 4, 7…)",
        "y corre junto al barandal; nadie se lo",
        "dijo al algoritmo.",
        f"V*(1) = {_aprox(d['v_inicio'])}."], color=TEXTO)
    desc = (f"Pasillo de {n} casillas. Franja de la política óptima en las casillas 1 a {k}: "
            "camina en las casillas con hueco (1, 4, 7, …, las de i mod 3 = 1) y corre en las "
            f"demás. Debajo, V*(i) contra la casilla i, de 1 a {n}: sube casi en línea recta "
            f"desde V*(1) = {_aprox(d['v_inicio'])} hasta "
            f"V*({n}) = {_v(V[n])}.")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 7 ===

def mkv_c3_rondas_politicas():
    mdp = m.pasillo()
    d = m.pasillo_largo()
    titulo = ["Iteración de políticas,", "ronda a ronda"]
    out = []
    y = encabezado(out, titulo)
    descs = []
    for inicio in ("caminar–caminar", "correr–correr"):
        pols = m.iterar_politicas(mdp, m.POLITICAS_J2[inicio])
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        out.append(texto(X_PIE, y + 14, f"Desde {inicio}", tam=14, peso="700", anclaje="start"))
        y += 26
        partes = []
        for k, pol in enumerate(pols):
            V = m.evaluar_politica(mdp, pol)
            ultima = k == len(pols) - 1
            out.append(caja(X_PIE, _n(y), ANCHO - 2 * X_PIE, 40, radio=6,
                            relleno=mezclar(ACENTO if ultima else LINEA, 0.14 if ultima else 0.18),
                            borde=ACENTO if ultima else SUAVE, grosor=2 if ultima else 1.5))
            out.append(texto(X_PIE + 10, y + 17, f"ronda {k + 1}: {_nombre_pol(pol)}", tam=13,
                             peso="700", anclaje="start"))
            out.append(texto(X_PIE + 10, y + 33, f"Vπ = ({_v(V[1])}, {_v(V[2])})"
                             + ("; la mejora no cambia nada" if ultima else ""), tam=12,
                             anclaje="start", color=SUAVE))
            partes.append(f"ronda {k + 1}: {_nombre_pol(pol)}, Vπ = ({_v(V[1])}, {_v(V[2])})")
            y += 40
            if not ultima:
                out.append(_flecha(ANCHO / 2, y + 2, ANCHO / 2, y + 16))
                y += 20
        descs.append(f"Desde {inicio}: " + "; ".join(partes) + ".")
        y += 22
    # el pasillo largo: rondas de una y otra
    out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
    out.append(texto(X_PIE, y + 14, f"El pasillo de {m.N_PASILLO} casillas", tam=14, peso="700",
                     anclaje="start"))
    y += 30
    # Como la pagina: una ronda evalua y mejora; la ultima solo confirma.
    rondas_pi = d["rondas_pi"] + 1
    tope = max(d["rondas_vi"], rondas_pi)
    for rot, v, color in (("valores", d["rondas_vi"], COLOR_V),
                          ("políticas", rondas_pi, ACENTO)):
        out.append(texto(X_PIE, y + 13, rot, tam=13, peso="700", anclaje="start"))
        w = max(110 * v / tope, 2)
        out.append(f'<rect x="96" y="{_n(y)}" width="{_n(w)}" height="18" '
                   f'fill="{mezclar(color, 0.55)}" stroke="{color}" stroke-width="1"/>')
        out.append(texto(96 + w + 6, y + 14, f"{miles(v)} ronda" + ("" if v == 1 else "s"), tam=13, anclaje="start"))
        y += 28
    y = pie(out, y + 8, ["Valores: hasta residuo ≤ 10⁻⁹, desde 0.",
                         "Políticas: desde caminar siempre; la",
                         "última ronda solo confirma."])
    desc = ("Iteración de políticas en el pasillo de dos casillas. " + " ".join(descs)
            + f" En el pasillo de {m.N_PASILLO} casillas, la iteración de valores hace "
            f"{miles(d['rondas_vi'])} rondas hasta un residuo de 10⁻⁹ y la de políticas, "
            f"{d['rondas_pi'] + 1} rondas desde caminar siempre: una mejora y una que confirma.")
    return svg(titulo, desc, out, y)


# =============================================== figuras de la pagina 8 ===

def _restricciones(mdp):
    """(s, a, a1, a2, b): a1 V(1) + a2 V(2) >= b, una por (s, a) de J2."""
    filas = []
    for s in mdp["estados"]:
        for a in mdp["acciones"][s]:
            co = {1: F(0), 2: F(0)}
            co[s] += 1
            for t, p in mdp["P"][(s, a)].items():
                if t in co:
                    co[t] -= p
            filas.append((s, a, co[1], co[2], mdp["r"][(s, a)]))
    return filas


def _recorta_poligono(poli, a1, a2, b):
    """Sutherland-Hodgman: la parte de poli con a1 x + a2 y >= b."""
    sale = []
    for i, P in enumerate(poli):
        Q = poli[(i + 1) % len(poli)]
        fp = a1 * P[0] + a2 * P[1] - b
        fq = a1 * Q[0] + a2 * Q[1] - b
        if fp >= 0:
            sale.append(P)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            sale.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return sale


_VENTANA_LP = ((-14, 2), (-4, 2))


def _panel_lp(out, y, mdp, alto=170, rotular=True, vstar=None):
    (xa, xb), (ya, yb) = _VENTANA_LP
    top = y + 30
    px, py = _plano(out, (58, top, 280, top + alto), (xa, xb), (ya, yb), range(-12, xb + 1, 4),
                    range(ya, yb + 1), "V(1)", "V(2)")
    filas = [f for f in _restricciones(mdp) if f[2] or f[3]]
    poli = [(F(xa), F(ya)), (F(xb), F(ya)), (F(xb), F(yb)), (F(xa), F(yb))]
    for _, _, a1, a2, b in filas:
        poli = _recorta_poligono(poli, a1, a2, b)
    out.append(f'<polygon points="{" ".join(f"{_n(px(x))},{_n(py(v))}" for x, v in poli)}" '
               f'fill="{mezclar(COLOR_CERRADA, 0.3)}" stroke="none"/>')
    rotulos = []
    for s, a, a1, a2, b in filas:
        if a2 == 0 or a1 == 0:
            # horizontal (solo V(2)) o vertical (solo V(1))
            if a1 == 0:
                v = b / a2
                seg = ((xa, v), (xb, v))
            else:
                v = b / a1
                seg = ((v, ya), (v, yb))
        else:
            # V(1) = (b - a2 V(2)) / a1
            seg = (((b - a2 * ya) / a1, ya), ((b - a2 * yb) / a1, yb))
            if min(seg[0][0], seg[1][0]) < xa:
                y_en = (b - a1 * xa) / a2
                seg = ((F(xa), y_en), seg[1]) if seg[0][0] < xa else (seg[0], (F(xa), y_en))
        (x1, y1), (x2, y2) = seg
        out.append(linea(_n(px(x1)), _n(py(y1)), _n(px(x2)), _n(py(y2)), color=TEXTO, grosor=1.5))
        rotulos.append((s, a, seg))
    sol, _ = m.programa_lineal(mdp)
    opt = (sol[1], sol[2])
    # la recta de nivel V(1) + V(2) = optimo
    c = opt[0] + opt[1]
    out.append(_polilinea([(px(c - ya), py(ya)), (px(c - yb), py(yb))]
                          if xa <= c - yb else [(px(xa), py(c - xa)), (px(c - ya), py(ya))],
                          ACENTO, "4 3", 1.5))
    out.append(f'<circle cx="{_n(px(opt[0]))}" cy="{_n(py(opt[1]))}" r="6" fill="{ACENTO}" '
               f'stroke="{ACENTO}" stroke-width="1"/>')
    if vstar is not None:
        out.append(f'<circle cx="{_n(px(vstar[0]))}" cy="{_n(py(vstar[1]))}" r="7" fill="none" '
                   f'stroke="{COLOR_C}" stroke-width="2.5"/>')
    return top + alto + 44, rotulos, opt, filas


def _rotulo_restriccion(s, a):
    return f"{a} en {s}"


def mkv_c3_region_lp():
    mdp = m.pasillo()
    titulo = ["El MDP como programa", "lineal: la región"]
    out = []
    y = encabezado(out, titulo)
    y0 = y
    y, rotulos, opt, filas = _panel_lp(out, y, mdp, alto=200)
    # rotulos de las rectas: en la ventana, cerca de su extremo
    (xa, xb), (ya, yb) = _VENTANA_LP
    top = y0 + 30
    px = lambda x: 58 + 222 * (float(x) - xa) / (xb - xa)
    py = lambda v: top + 200 - 200 * (float(v) - ya) / (yb - ya)
    sitios = {(2, m.CAMINAR): (px(-13.6), py(-3) + 15, "start"),
              (2, m.CORRER): (px(-13.6), py(-2) - 6, "start"),
              (1, m.CAMINAR): (px(-1), py(2) - 8, "middle"),
              (1, m.CORRER): (px(-10), py(2) - 8, "middle")}
    for s, a, _ in rotulos:
        x, yy, anc = sitios[(s, a)]
        out.append(texto(x, yy, _rotulo_restriccion(s, a), tam=12, peso="700", anclaje=anc))
    Vs = m.evaluar_politica(mdp, m.POLITICAS_J2["caminar–correr"])
    assert all(abs(opt[i] - float(Vs[i + 1])) < 1e-9 for i in range(2))
    y = _leyenda(out, y + 16, [
        (lambda x, yy: f'<rect x="{_n(x - 10)}" y="{_n(yy - 7)}" width="20" height="14" '
                       f'fill="{mezclar(COLOR_CERRADA, 0.3)}"/>', "donde se cumplen las cuatro"),
        (lambda x, yy: _polilinea([(x - 12, yy), (x + 12, yy)], ACENTO, "4 3", 1.5),
         "V(1) + V(2) constante, la menor"),
        (lambda x, yy: f'<circle cx="{_n(x)}" cy="{_n(yy)}" r="5" fill="{ACENTO}"/>',
         f"el mínimo: ({_vd(opt[0], 0)}, {_vd(opt[1], 0)}) = V*"),
    ])
    y = pie(out, y + 6, ["Una recta por cada par (estado, acción):",
                         "V(s) ≥ r(s, a) + Σ P(s′ | s, a) V(s′)."], color=TEXTO)
    desc = ("Plano V(1)–V(2) con las cuatro restricciones del programa lineal del pasillo, una "
            "recta por par (estado, acción): "
            + "; ".join(f"{a} en {s}: {_v(a1)} V(1) + {_v(a2)} V(2) ≥ {_v(b)}".replace("+ −", "− ")
                        for s, a, a1, a2, b in filas)
            + ". La región donde se cumplen todas está sombreada; minimizar V(1) + V(2) lleva a "
            f"la esquina ({_vd(opt[0], 0)}, {_vd(opt[1], 0)}), que es V*.")
    return svg(titulo, desc, out, y)


# =============================================== figura de la pagina 9 ===

def mkv_c3_mapa_decidir():
    titulo = ["Decidir: pregunta,", "ecuación, algoritmo"]
    out = []
    y = encabezado(out, titulo)
    filas = [
        ("¿Sin ciclos?", "costo(s) = mín (pisar + costo)", ["HACIA-ATRÁS:", "una pasada"]),
        ("¿Cuánto vale π?", "V = r + P V, con las filas de π", ["EVALUAR-POLÍTICA:", "un sistema lineal"]),
        ("¿Cuál es la mejor?", "V*(s) = máx (r + Σ P V*)",
         ["iteración de valores,", "iteración de políticas", "o programa lineal"]),
    ]
    descs = []
    for preg, ec, alg in filas:
        out.append(caja(X_PIE, _n(y), ANCHO - 2 * X_PIE, 30, radio=6,
                        relleno=mezclar(COLOR_V, 0.14), borde=COLOR_V, grosor=1.5))
        out.append(texto(ANCHO / 2, y + 20, preg, tam=14, peso="700"))
        out.append(_flecha(ANCHO / 2, y + 31, ANCHO / 2, y + 46))
        y += 48
        out.append(caja(X_PIE, _n(y), ANCHO - 2 * X_PIE, 30, radio=6,
                        relleno=mezclar(LINEA, 0.18), borde=SUAVE, grosor=1.5))
        out.append(texto(ANCHO / 2, y + 20, ec, tam=13))
        out.append(_flecha(ANCHO / 2, y + 31, ANCHO / 2, y + 46))
        y += 48
        h = 12 + 18 * len(alg)
        out.append(caja(X_PIE, _n(y), ANCHO - 2 * X_PIE, h, radio=6,
                        relleno=mezclar(ACENTO, 0.14), borde=ACENTO, grosor=2))
        for i, r in enumerate(alg):
            out.append(texto(ANCHO / 2, y + 20 + 18 * i, r, tam=13, peso="700" if i == 0 else
                             "normal"))
        y += h + 26
        descs.append(f"{preg} Ecuación: {ec}. Algoritmo: {' '.join(alg)}.")
    y = pie(out, y - 6, ["Lo que rompe la pasada hacia atrás", "es el ciclo, no el azar."])
    desc = "Mapa de la clase en tres filas. " + " ".join(descs)
    return svg(titulo, desc, out, y)


# ---------------------------------------------------- flujos (clase 3) ---

FLUJOS.update({
    "hacia-atras": dict(
        nombre="la pasada hacia atrás",
        titulo=["Hacia atrás,", "en palabras"],
        pasos=[{"caja": ["Empieza arriba:", "costo(5) = 0, s = 4"]},
               {"caja": ["Para cada brinco: pisar", "el destino + su costo"]},
               {"caja": ["costo(s) = el menor;", "guarda ese brinco"]},
               {"rombo": ["¿s = 0?"], "abajo": "no"},
               {"caja": ["Baja: s ← s − 1"]},
               {"caja": ["Devuelve costo y,", "brinco a brinco, la ruta"], "fin": True,
                "sin_flecha": True}],
        vueltas=[(4, 1, "otro escalón")],
        salidas=[(3, 5, "sí")],
        notas=["Funciona porque cada brinco sube:", "el costo de arriba ya está listo."]),
    "evaluar": dict(
        nombre="evaluar una política",
        titulo=["Evaluar una política,", "en palabras"],
        pasos=[{"caja": ["Toma la política π"]},
               {"caja": ["Elige filas: la fila s", "de P y r con la acción π(s)"]},
               {"caja": ["Arma (I − P) V = r", "sin la columna de la meta"]},
               {"rombo": ["¿Tiene solución", "única?"], "abajo": "sí"},
               {"caja": ["Resuélvelo y devuelve", "el valor de π"], "fin": True},
               {"caja": ["Avisa: desde algún", "estado no termina"], "fin": True,
                "sin_flecha": True}],
        vueltas=[],
        salidas=[(3, 5, "no")],
        notas=["Cada renglón dice: lo que pagas", "ahora más lo que vale donde caes."]),
    "valores": dict(
        nombre="la iteración de valores",
        titulo=["Iteración de valores,", "en palabras"],
        pasos=[{"caja": ["Empieza: V(s) = 0", "en todo estado"]},
               {"caja": ["En cada s, el máximo", "sobre a de r + Σ P V"]},
               {"caja": ["Mide el residuo: el", "mayor cambio; V ← nuevo"]},
               {"rombo": ["¿residuo", "≤ tol?"], "abajo": "sí"},
               {"caja": ["Devuelve V y la", "codiciosa de V"], "fin": True}],
        vueltas=[(3, 1, "no: otra ronda")],
        notas=["Cada ronda usa los valores de la", "anterior en todos los estados."]),
    "politicas": dict(
        nombre="la iteración de políticas",
        titulo=["Iteración de políticas,", "en palabras"],
        pasos=[{"caja": ["Empieza con una π", "que termina"]},
               {"caja": ["Evalúa: resuelve el", "sistema del valor de π"]},
               {"caja": ["Mejora: en cada s, la", "codiciosa de ese valor;", "en empate, conserva π(s)"]},
               {"rombo": ["¿Cambió", "alguna?"], "abajo": "no"},
               {"caja": ["Devuelve π y su valor"], "fin": True}],
        vueltas=[(3, 1, "sí: otra ronda")],
        notas=["Cada ronda mejora o deja igual;", "hay un número finito de políticas."]),
})


# --------------------------------------------- ejemplo y contraejemplo ---
# Un SVG por clave del manifiesto del plan (§5): arriba lo que cumple, abajo
# lo que no; cada lado es una funcion (out, y) -> (y, descripcion).

def _mdp_fila_mal():
    """«Correr» con la fila de 1 que suma 3/2 (plan §5, p3): se queda con
    1/2 y avanza con 1."""
    mdp = m.pasillo()
    mdp["P"] = dict(mdp["P"])
    mdp["P"][(1, m.CORRER)] = {1: F(1, 2), 2: F(1)}
    return mdp


def _mdp_empate():
    """El pasillo del contraejemplo de empates: m.pasillo_empate()."""
    return m.pasillo_empate()


def _lado_mdp_completo(mdp, pie_txt):
    def dibuja(out, y):
        y = _grafo_mdp(out, mdp, y + 4)
        malas = {a: tuple(i for i, f in enumerate(m.matriz_accion(mdp, a)) if sum(f) != 1)
                 for a in (m.CAMINAR, m.CORRER)}
        y = _matrices_mdp(out, y, mdp, marcar=malas)
        sumas = [sum(f) for f in m.matriz_accion(mdp, m.CORRER)]
        return y, _desc_mdp(mdp) + " Filas de P correr suman " + " y ".join(map(fr, sumas)) + "."
    return dibuja


def _lado_politica(mdp, pol, nombre, evaluar=False):
    def dibuja(out, y):
        acc = {s: [pol[s]] for s in mdp["estados"]}
        y = _grafo_mdp(out, mdp, y + 4, acc)
        d = f"Política {nombre}: " + _desc_mdp(mdp, acc)
        if not evaluar:
            y, filas = _matriz_pi(out, y, mdp, pol)
            return y, d
        PT, rpi = m.cadena_politica(mdp, pol)
        IP = [[F(int(i == j)) - PT[i][j] for j in range(len(PT))] for i in range(len(PT))]
        yc = y + 8 + len(IP) * 17 / 2
        _matriz_svg(out, ANCHO / 2, yc, _filas(IP), rotulo="I − P", sub="π,𝒯")
        y = yc + len(IP) * 17 / 2 + 10
        try:
            V = m.evaluar_politica(mdp, pol)
            linea_ = f"r = ({', '.join(_v(x) for x in rpi)}) → V = ({_v(V[1])}, {_v(V[2])})"
            d += (" I − P π,𝒯 = " + "; ".join(", ".join(_v(x) for x in f) for f in IP)
                  + f", invertible; V(1) = {_v(V[1])}, V(2) = {_v(V[2])}.")
        except ValueError:
            linea_ = f"r = ({', '.join(_v(x) for x in rpi)}): 0 · V = 0, toda V sirve"
            d += (" I − P π,𝒯 = " + "; ".join(", ".join(_v(x) for x in f) for f in IP)
                  + ", la matriz cero: no se puede invertir y toda V resuelve el sistema.")
        out.append(texto(ANCHO / 2, y + 12, linea_, tam=12, peso="700"))
        return y + 24, d
    return dibuja


def _lado_funcion(curvas, marcas=(), pegada=None, texto_desc=""):
    def dibuja(out, y):
        y, _ = _panel_funcion(out, y + 4, curvas, alto=140, marcas=marcas, pegada=pegada)
        return y, texto_desc
    return dibuja


def _lado_codiciosa(mdp, U, nombre_u):
    def dibuja(out, y):
        pol = m.codiciosa(mdp, U)
        rot = {(s, a): f"vale {_v(m.q_valor(mdp, U, s, a))}" for s in mdp["estados"]
               for a in mdp["acciones"][s]}
        out.append(texto(X_PIE, y + 12, f"{nombre_u}: U(1) = {_v(U[1])}, U(2) = {_v(U[2])}",
                         tam=12, anclaje="start", color=TEXTO, peso="700"))
        y = _grafo_mdp(out, mdp, y + 20, resaltar=pol, rotulos=rot)
        d = (f"Con {nombre_u}, U(1) = {_v(U[1])} y U(2) = {_v(U[2])}: "
             + "; ".join(f"en {s}, {a} vale {_v(m.q_valor(mdp, U, s, a))}"
                         for s in mdp["estados"] for a in mdp["acciones"][s])
             + f". La codiciosa elige {_nombre_pol(pol)}.")
        return y, d
    return dibuja


def _lado_paro(mdp, Vs, T=10):
    def dibuja(out, y):
        traza = m.iterar_valores(mdp, rondas=T)
        res = m.residuos(traza)
        err = m.errores(traza, Vs)[1:]
        top = y + 28
        px, py = _plano(out, (58, top, 280, top + 120), (1, T), (-3, 2), range(1, T + 1),
                        [10 ** k for k in range(-3, 3)], "ronda k", "tamaño (escala log)",
                        fy=_fy_log, log=True)
        _serie_log(out, px, py, err, COLOR_C, "cuadro", "5 4")
        _serie_log(out, px, py, res, COLOR_V, "circulo")
        cocientes = [e / r for e, r in zip(err, res)]
        d = ("Rondas 1 a " + str(T) + ": residuo " + ", ".join(_vd(r, 4) for r in res)
             + "; error " + ", ".join(_vd(e, 4) for e in err) + ".")
        return top + 120 + 44, d, cocientes
    return dibuja


def _lado_empates(empate):
    def dibuja(out, y):
        mdp = _mdp_empate()
        pols = m.iterar_politicas(mdp, m.POLITICAS_J2["caminar–caminar"], empate=empate,
                                  max_rondas=4)
        V = m.evaluar_politica(mdp, pols[0])
        q = {a: m.q_valor(mdp, V, 2, a) for a in mdp["acciones"][2]}
        out.append(texto(X_PIE, y + 6, "En 2: " + ", ".join(f"{a} vale {_v(v)}"
                                                             for a, v in q.items()),
                         tam=12, anclaje="start", color=TEXTO))
        y += 18
        partes = []
        for k, pol in enumerate(pols):
            ultima = k == len(pols) - 1
            out.append(caja(40, _n(y), 220, 26, radio=6,
                            relleno=mezclar(LINEA, 0.18), borde=SUAVE, grosor=1.5))
            out.append(texto(ANCHO / 2, y + 18, f"ronda {k}: {_nombre_pol(pol)}", tam=13,
                             peso="700"))
            partes.append(_nombre_pol(pol))
            y += 26
            if not ultima:
                out.append(_flecha(ANCHO / 2, y + 2, ANCHO / 2, y + 14))
                y += 18
        para = len(pols) < 5
        out.append(texto(ANCHO / 2, y + 20, "para: la mejora no cambia nada" if para
                         else "… y así sin fin", tam=13, peso="700",
                         color=COLOR_CERRADA if para else COLOR_C))
        d = ("Iteración de políticas desde caminar–caminar, con caminar a costo "
             f"{_v(-mdp['r'][(2, m.CAMINAR)])} en la casilla 2: allí "
             + " y ".join(f"{a} vale {_v(v)}" for a, v in q.items()) + ". Rondas: "
             + ", ".join(partes) + (", y para." if para else ", y sigue alternando."))
        return y + 34, d
    return dibuja


def _lado_lp(mdp, vstar_txt):
    def dibuja(out, y):
        vstar = m.iterar_valores(mdp, rondas=1)[-1]
        es_fijo = m.cumple_bellman(mdp, vstar)
        y, _, opt, filas = _panel_lp(out, y, mdp, alto=130,
                                     vstar=(vstar[1], vstar[2]) if vstar_txt else None)
        V = m.evaluar_politica(m.pasillo(), m.POLITICAS_J2["caminar–correr"])
        mins = f"({_vd(opt[0], 0)}, {_vd(opt[1], 0)})"
        if vstar_txt:
            assert es_fijo and vstar[1] == vstar[2] == 0
            linea_ = f"mínimo {mins} ≠ V* = ({_v(vstar[1])}, {_v(vstar[2])}) (anillo)"
        else:
            linea_ = f"mínimo {mins} = V* (punto)"
        out.append(texto(ANCHO / 2, y + 12, linea_, tam=12, peso="700"))
        d = (f"Región del programa lineal en el plano V(1)–V(2); el mínimo de V(1) + V(2) es "
             f"{mins}." + (f" Con esperar gratis las restricciones nuevas dicen V(s) ≥ V(s), "
                           f"la región no cambia, pero V* = ({_v(vstar[1])}, {_v(vstar[2])})."
                           if vstar_txt else f" Coincide con V* = ({_v(V[1])}, {_v(V[2])})."))
        return y + 26, d
    return dibuja


def _ejemplos_c3():
    J = m.pasillo()
    E0 = m.pasillo(esperar=0)
    cc = m.POLITICAS_J2["caminar–correr"]
    esperar = {1: m.ESPERAR, 2: m.ESPERAR}
    Vs = m.evaluar_politica(J, cc)
    Ue = {1: F(-8), 2: F(-8)}
    lazo = m.lazo_99()
    V99 = m.evaluar_politica(lazo, {1: m.CAMINAR})
    return {
        "punto-fijo": {
            "pagina": "1_lo_que_necesitas.md", "titulo": "punto fijo",
            "si": (_lado_funcion([(_f_telarana, COLOR_V, None)], marcas=[(-2, "x = −2")],
                                 texto_desc="y = −1 + x/2 cruza a y = x una vez, en −2; iterar "
                                 "se acerca."),
                   "f(x) = −1 + x/2: un cruce, en −2"),
            "no": (_lado_funcion([(lambda x: x, COLOR_V, None)], pegada=(-4, 1),
                                 texto_desc="f(x) = x coincide con y = x: toda x es punto fijo."),
                   "f(x) = x: toda x es punto fijo"),
            "pie": ["Punteada: y = x. Anillo: el cruce.", "Amarillo grueso: pegada a y = x."]},
        "hacia-atras": {
            "pagina": "2_de_contar_a_decidir.md", "titulo": "una pasada hacia atrás",
            "si": (_lado_escalera(None), "Sin ciclos: costo(s) sale de arriba"),
            "no": (_lado_escalera(3), "Resbalón en 3: costo(3) usa costo(3)"),
            "pie": ["Lo que rompe la pasada es el ciclo,", "no el azar."]},
        "mdp": {
            "pagina": "3_el_mdp.md", "titulo": "un MDP",
            "si": (_lado_mdp_completo(J, ""), "Cada fila de P caminar y P correr suma 1"),
            "no": (_lado_mdp_completo(_mdp_fila_mal(), ""), "Fila 1 de P correr: 1/2 + 1 = 3/2"),
            "pie": ["Una fila que no suma 1 no es una", "distribución: no es un MDP."]},
        "termina": {
            "pagina": "3_el_mdp.md", "titulo": "termina con probabilidad 1",
            "si": (_lado_politica(J, cc, "caminar–correr"), "caminar–correr: llega a la meta"),
            "no": (_lado_politica(E0, esperar, "esperar siempre"),
                   "esperar siempre: nunca llega"),
            "pie": ["Con esperar, ninguna flecha llega", "a la meta: la cadena no termina."]},
        "evaluar": {
            "pagina": "4_evaluar_una_politica.md", "titulo": "evaluar una política",
            "si": (_lado_politica(J, cc, "caminar–correr", evaluar=True),
                   "caminar–correr: una sola solución"),
            "no": (_lado_politica(E0, esperar, "esperar siempre (gratis)", evaluar=True),
                   "esperar siempre: I − P es cero"),
            "pie": ["Sin terminar con probabilidad 1,", "I − P (sin la meta) no se invierte."]},
        "bellman": {
            "pagina": "5_bellman.md", "titulo": "ecuación de Bellman",
            "si": (_lado_funcion([(_bellman_2(J), ACENTO, None)], marcas=[(Vs[2], "−2")],
                                 texto_desc="y = máx(−3, −1 + x/2) cruza a y = x solo en −2."),
                   "y = máx(−3, −1 + x/2): cruza en −2"),
            "no": (_lado_funcion([(_bellman_2(E0), ACENTO, None)], pegada=(Vs[2], 1),
                                 texto_desc="Con esperar gratis, y = máx(−3, −1 + x/2, x) "
                                 "coincide con y = x para todo x ≥ −2: infinitas soluciones."),
                   "con esperar gratis: pegada a y = x"),
            "pie": ["x = V(2). Punteada: y = x.", "Amarillo grueso: infinitas soluciones."]},
        "codiciosa": {
            "pagina": "5_bellman.md", "titulo": "la codiciosa de V*",
            "si": (_lado_codiciosa(J, Vs, "U = V*"), "Codiciosa de V*: caminar–correr"),
            "no": (_lado_codiciosa(J, Ue, "U equivocado"),
                   "Codiciosa de U: " + _nombre_pol(m.codiciosa(J, Ue))),
            "pie": ["Acento: la acción que elige. «vale» =", "r(s, a) + Σ P(s′ | s, a) U(s′)."]},
        "paro": {
            "pagina": "6_iterar_valores.md", "titulo": "parar con un residuo chico",
            "si": (_lado_paro(J, Vs), None),
            "no": (_lado_paro(lazo, V99), None),
            "pie": ["Círculo: residuo. Cuadro: error.", "Sin la cota, un residuo chico no",
                    "asegura un error chico."]},
        "empates": {
            "pagina": "7_iterar_politicas.md", "titulo": "empates en la mejora",
            "si": (_lado_empates("conservar"), "En empate conserva: termina"),
            "no": (_lado_empates("cambiar"), "En empate cambia: alterna"),
            "pie": ["Caminar cuesta 2 en la casilla 2;", "allí caminar y correr empatan."]},
        "lineal": {
            "pagina": "8_como_programa_lineal.md", "titulo": "el programa lineal da V*",
            "si": (_lado_lp(J, False), "El pasillo: el mínimo es V*"),
            "no": (_lado_lp(E0, True), "Esperar gratis: región igual"),
            "pie": ["Sombreado: la región. Punto: el", "mínimo. Anillo: V* con esperar."]},
    }


def _lado_escalera(resbalon):
    def dibuja(out, y):
        costo = m.escalera_costo()
        yn = y + 40
        xs = _escalera_grafo(out, yn, resbalon=resbalon,
                             marcar_ruta=None if resbalon else m.escalera_ruta_optima())
        out.append(texto(X_PIE, yn + 88, "pisar", tam=12, anclaje="start", color=SUAVE))
        out.append(texto(X_PIE, yn + 106, "falta", tam=12, anclaje="start", color=SUAVE))
        for s in range(1, 6):
            out.append(texto(xs[s], yn + 88, str(m.ESCALERA_COSTOS[s - 1]), tam=12,
                             color=SUAVE))
        for s in range(6):
            v = str(costo[s]) if resbalon is None or s > resbalon else "?"
            out.append(texto(xs[s], yn + 106, v, tam=12, peso="700"))
        if resbalon is None:
            d = ("Escalera sin ciclos, escalones 0 a 5, brincos de 1 y de 2; pisar cuesta "
                 + ", ".join(map(str, m.ESCALERA_COSTOS)) + ". Lo que falta, de 0 a 5: "
                 + ", ".join(map(str, costo)) + "; una pasada de 5 hacia 0 basta. Ruta "
                 "óptima marcada: " + " → ".join(map(str, m.escalera_ruta_optima())) + ".")
        else:
            d = (f"La misma escalera, pero en el escalón {resbalon} un brinco falla con 1/2 y "
                 f"te deja donde estás (lazo): costo({resbalon}) depende de sí mismo, y de "
                 f"{resbalon} hacia abajo la pasada no puede llenar la tabla.")
        return yn + 118, d
    return dibuja


def ejemplo_c3(clave):
    e = EJEMPLOS_C3[clave]
    titulo = ["Ejemplo y contraejemplo", e["titulo"]]
    out = []
    y = encabezado(out, titulo)
    descs = []
    for lado in ("si", "no"):
        dibuja, dice = e[lado]
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        if clave == "paro":
            sub = []
            y2, d, coc = dibuja(sub, y + 40)
            k = coc[-1]
            igual = all(c == k for c in coc[1:])
            assert igual, coc
            dice = ("el pasillo: error = residuo desde k = 2" if k == 1
                    else f"el pasillo: error = {fr(k)} × residuo") \
                if lado == "si" else f"lazo 99/100: error = {fr(k)} × residuo"
            out.append(texto(X_PIE, y + 14, "✓ Lo cumple" if lado == "si" else "✗ No lo cumple",
                             tam=14, peso="700", anclaje="start"))
            out.append(texto(X_PIE, y + 33, dice, tam=13, anclaje="start", color=SUAVE))
            out.extend(sub)
            y = y2
            d = d + (" Desde la ronda 2, error y residuo coinciden." if k == 1 else
                     f" El error es {fr(k)} veces el residuo en toda ronda.")
        else:
            out.append(texto(X_PIE, y + 14, "✓ Lo cumple" if lado == "si" else "✗ No lo cumple",
                             tam=14, peso="700", anclaje="start"))
            out.append(texto(X_PIE, y + 33, dice, tam=13, anclaje="start", color=SUAVE))
            y, d = dibuja(out, y + 40)
        descs.append(("Lo cumple: " if lado == "si" else "No lo cumple: ") + dice + ". " + d)
        y += 8
    y = pie(out, y + 4, e["pie"])
    return svg(titulo, " ".join(descs), out, y)


EJEMPLOS_C3 = _ejemplos_c3()


# =========================================================== CLASE 4 ===
#
# Figuras «mkv-c4-*» de course/8_markov/4_lo_que_no_se_ve/. Cada cifra sale de
# markov.py (seccion «Lo que no se ve»: paraguas()). Marcas: estado oculto =
# circulo amarillo de BORDE PUNTEADO con el rotulo «oculto»; senal que se ve =
# caja azul de BORDE SOLIDO con el rotulo «se ve». El color nunca es la unica
# senal. Flechas entre estados: transicion (P); hacia abajo: emision (B).
#
# Helpers reutilizables por el resto de la clase:
#   _oculto, _visto         un estado oculto / una senal vista
#   grafo_oculto            el grafo completo de un modelo oculto
#   _matriz_con_sumas       una matriz por filas con su columna «suma»

COLOR_OCULTO = COLOR_C
COLOR_VISTO = COLOR_V
R_OC = 28            # radio de un estado oculto
W_VISTO, H_VISTO = 112, 46
GUIONES_OCULTO = "4 3"


def _oculto(cx, cy, nombre, r=R_OC):
    """Estado oculto: circulo punteado, su nombre y el rotulo «oculto»."""
    return (f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{r}" fill="{mezclar(COLOR_OCULTO, 0.18)}" '
            f'stroke="{COLOR_OCULTO}" stroke-width="2" stroke-dasharray="{GUIONES_OCULTO}"/>'
            + texto(cx, cy - 1, nombre, tam=14, peso="700")
            + texto(cx, cy + 13, "oculto", tam=12, color=SUAVE))


def _visto(cx, cy, nombre, w=W_VISTO, h=H_VISTO):
    """Senal que se ve: caja de borde solido, su nombre y el rotulo «se ve»."""
    return (caja(_n(cx - w / 2), _n(cy - h / 2), w, h,
                 relleno=mezclar(COLOR_VISTO, 0.18), borde=COLOR_VISTO, radio=8, grosor=2)
            + texto(cx, cy - 4, nombre, tam=14, peso="700")
            + texto(cx, cy + 13, "se ve", tam=12, color=SUAVE))


def _xs_equidistantes(n, x0=84, x1=216):
    return [(x0 + x1) / 2] if n == 1 else [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]


def _emision(origen, destino, rotulo, t=0.27, tam=13, cruzada=False):
    """Flecha recta del borde del estado oculto al borde de arriba de la
    senal; el rotulo cerca del origen, del lado hacia donde va la flecha, o
    del opuesto si la flecha cruza a otra (cruzada=True: asi dos rotulos que
    cruzan no se juntan en el centro)."""
    (x1, y1), (x2, y2) = origen, destino
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    sx, sy = x1 + ux * R_OC, y1 + uy * R_OC
    ex, ey = x2 - ux * 2, y2 - uy * 2
    lado = 1 if x2 >= x1 else -1
    if cruzada:
        lado = -lado
    # el rotulo va a un lado de la flecha; si es casi vertical, al lado de la salida
    px, py = sx + (ex - sx) * t, sy + (ey - sy) * t
    ancla = "start" if lado > 0 else "end"
    return (_flecha(sx, sy, ex, ey)
            + texto(px + lado * 6, py + tam * 0.35, rotulo, tam=tam, peso="700", anclaje=ancla))


def grafo_oculto(out, y, h, brecha=140, transiciones=True, emisiones=True):
    """Dibuja el grafo de un modelo oculto `h` (dict de markov._hmm): estados
    ocultos arriba, senales abajo, flechas de transicion entre los de arriba
    y de emision hacia abajo, con sus fracciones tal cual salen de `h`.
    `y` es la y libre de arriba; devuelve (y libre de abajo, descripcion)."""
    E, O = h["estados"], h["señales"]
    yn = y + 70 if transiciones else y + 34
    ys = yn + brecha
    xe, xo = _xs_equidistantes(len(E)), _xs_equidistantes(len(O), 80, 220)
    pos = {s: (x, yn) for s, x in zip(E, xe)}
    if transiciones:
        for s in E:
            for t in E:
                p = h["P"][s][t]
                if p == 0:
                    continue
                if s == t:
                    out.append(_lazo(*pos[s], fr10(p), r=R_OC, hacia="arriba", alcance=30))
                else:
                    ida_y_vuelta = h["P"][t][s] > 0
                    out.append(_arista(pos[s], pos[t], fr10(p), r=R_OC,
                                       curva=-14 if ida_y_vuelta else 0, lado=-1, desp=10))
    if emisiones:
        w_llegada = min(40, (W_VISTO - 24) / max(len(E) - 1, 1))
        for k, o in enumerate(O):
            for i, s in enumerate(E):
                tx = xo[k] + (i - (len(E) - 1) / 2) * w_llegada
                out.append(_emision(pos[s], (tx, ys - H_VISTO / 2), fr10(h["B"][s][o]),
                                    t=0.3, cruzada=abs(tx - pos[s][0]) > 40))
    for s in E:
        out.append(_oculto(*pos[s], s))
    for k, o in enumerate(O):
        out.append(_visto(xo[k], ys, o))
    desc = [f"Arriba, los estados ocultos {' y '.join(E)}, en nodos con borde punteado."]
    if transiciones:
        for s in E:
            va = [f"se queda con {fr10(h['P'][s][t])}" if t == s else f"pasa a {t} con {fr10(h['P'][s][t])}"
                  for t in E if h["P"][s][t] > 0]
            desc.append(f"{s[0].upper() + s[1:]} " + " y ".join(va) + ".")
    desc.append(f"Abajo, las señales que se ven, {' y '.join(O)}, en nodos con borde sólido.")
    if emisiones:
        for s in E:
            desc.append(f"De {s} salen flechas de emisión: " + ", ".join(
                f"a {o} con {fr10(h['B'][s][o])}" for o in O) + ".")
    return ys + H_VISTO / 2, " ".join(desc)


def mkv_c4_hmm_grafo():
    h = m.paraguas()
    titulo = ["El paraguas oculto,", "estados arriba, señales abajo"]
    out = []
    y = encabezado(out, titulo)
    y, desc = grafo_oculto(out, y, h)
    mu0 = "(" + ", ".join(fr(h["mu0"][s]) for s in h["estados"]) + ")"
    out.append(texto(ANCHO / 2, y + 30, f"μ₀ = {mu0}", tam=14, peso="700"))
    y = pie(out, y + 54, ["Entre estados: transición, P.", "Hacia abajo: emisión, B.",
                          "Punteado: oculto. Sólido: se ve."])
    return svg(titulo, desc + f" Al pie, μ₀ = {mu0}.", out, y)


def _matriz_con_sumas(out, yc, nombres, filas, sumas, malas=(), rotulo="B", tam=12):
    """rotulo = [ filas ] con el nombre de cada fila a la izquierda y, a la
    derecha, la columna «suma». Las sumas de `malas` van en doble borde
    (forma, no solo color). Devuelve la y libre de abajo."""
    alto_fila, col, xb = 28, 44, 96
    h = len(filas) * alto_fila + 4
    y0 = yc - h / 2
    xe = xb + 6 + len(filas[0]) * col
    xs = 240
    out.append(texto(X_PIE, yc + tam * 0.35, f"{rotulo} =", tam=tam, anclaje="start", color=SUAVE))
    out.append(texto(xs, y0 - 6, "suma", tam=tam, color=SUAVE))
    for xx, d in ((xb, 5), (xe, -5)):
        out.append(f'<path d="M {_n(xx + d)} {_n(y0)} L {_n(xx)} {_n(y0)} L {_n(xx)} '
                   f'{_n(y0 + h)} L {_n(xx + d)} {_n(y0 + h)}" fill="none" '
                   f'stroke="{SUAVE}" stroke-width="1.5"/>')
    for i, (nom, f, sm) in enumerate(zip(nombres, filas, sumas)):
        cy = y0 + 2 + alto_fila * (i + 0.5)
        out.append(texto(xb - 8, cy + tam * 0.35, nom, tam=tam, anclaje="end", color=SUAVE))
        for j, c in enumerate(f):
            out.append(texto(xb + 3 + col * (j + 0.5), cy + tam * 0.35, c, tam=tam, peso="700"))
        if i in malas:
            for grosor_extra in (0, 3):
                out.append(caja(_n(xs - 27 - grosor_extra), _n(cy - 9 - grosor_extra), 54 + 2 * grosor_extra,
                                18 + 2 * grosor_extra, relleno="none", borde=ACENTO, radio=4,
                                grosor=1.5))
        out.append(texto(xs, cy + tam * 0.35, sm, tam=tam, peso="700",
                         color=ACENTO if i in malas else TEXTO))
    return y0 + h


def _panel_modelo(out, y, lado, h, dice, malas):
    out.append(texto(X_PIE, y + 14, "✓ Lo cumple" if lado == "si" else "✗ No lo cumple",
                     tam=14, peso="700", anclaje="start"))
    out.append(texto(X_PIE, y + 33, dice, tam=13, anclaje="start", color=SUAVE))
    yf, desc = grafo_oculto(out, y + 44, h, brecha=112)
    E, O = h["estados"], h["señales"]
    filas = [[fr10(h["B"][s][o]) for o in O] for s in E]
    sumas = [fr10(sum(h["B"][s].values())) for s in E]
    yb = _matriz_con_sumas(out, yf + 56, E, filas, sumas, malas)
    matriz = "; ".join(", ".join(f) for f in filas)
    sumas_txt = ", ".join(f"{s} suma {x}" for s, x in zip(E, sumas))
    return yb + 10, f"{desc} B por filas: {matriz}. {sumas_txt}."


def ejemplo_c4_modelo():
    h = m.paraguas()
    E, O = h["estados"], h["señales"]
    # la misma tabla copiada por columnas: B[i][j] pasa a ser B[j][i]
    Bt = {s: {o: h["B"][E[j]][O[i]] for j, o in enumerate(O)} for i, s in enumerate(E)}
    malo = dict(h, B=Bt)
    titulo = ["Ejemplo y contraejemplo", "un modelo oculto"]
    out = []
    y = encabezado(out, titulo)
    descs = []
    for lado, hh, dice in (("si", h, "B del paraguas: cada fila suma 1"),
                           ("no", malo, "La misma B, copiada por columnas")):
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        malas = [i for i, s in enumerate(E) if sum(hh["B"][s].values()) != 1]
        y, d = _panel_modelo(out, y, lado, hh, dice, malas)
        descs.append(("Lo cumple: " if lado == "si" else "No lo cumple: ") + dice + ". " + d)
        y += 8
    y = pie(out, y + 4, ["Doble borde: una suma distinta de 1."])
    return svg(titulo, " ".join(descs), out, y)


# ------------------------------------------------ pagina 3: filtrar ---
#
# Helpers reutilizables de las paginas 3 a 8:
#   _cabecera             encabezado de un panel «lo cumple / no lo cumple»
#   _dos_paneles          el armazon de un ejemplo y contraejemplo
#   _barra                una probabilidad como barra dentro de su pista
#   FLUJOS_C4 / flujo_c4  diagramas de flujo de la clase (aparte de FLUJOS:
#                         la guarda de FLUJOS fija 3 a 6 cajas y una salida)
#   _tabla_viterbi        delta y apuntadores de VITERBI, con fracciones
#   _trellis              la reticula de Viterbi, siempre en las mismas posiciones

BARRA_X0, BARRA_W = 66, 100
COLOR_LLUVIA, COLOR_SOL = COLOR_V, COLOR_C


def _cabecera(out, y, lado, dice):
    out.append(texto(X_PIE, y + 14, "✓ Lo cumple" if lado == "si" else "✗ No lo cumple",
                     tam=14, peso="700", anclaje="start"))
    out.append(texto(X_PIE, y + 33, dice, tam=13, anclaje="start", color=SUAVE))
    return y + 44


def _dos_paneles(titulo, paneles, pie_txt=()):
    """paneles: [(lado, dice, f)] con f(out, y) -> (y libre, descripcion).
    Devuelve el SVG."""
    out = []
    y = encabezado(out, titulo)
    descs = []
    for lado, dice, f in paneles:
        out.append(linea(X_PIE, _n(y - 6), ANCHO - X_PIE, _n(y - 6), color=LINEA, grosor=1))
        y, d = f(out, _cabecera(out, y, lado, dice))
        descs.append(("Lo cumple: " if lado == "si" else "No lo cumple: ") + dice + ". " + d)
        y += 8
    if pie_txt:
        y = pie(out, y + 4, pie_txt)
    return svg(titulo, " ".join(descs), out, y)


def _fv(v):
    """9/11 ≈ 0.818; un entero va solo."""
    return fr(v) if F(v).denominator == 1 else f"{fr(v)} ≈ {dec(v)}"


def _barra(out, y, nombre, v, valor, color, guiones=None, tachada=False, x0=BARRA_X0,
           ancho=BARRA_W, gris=False, color_valor=TEXTO):
    """Una probabilidad `v` como barra dentro de su pista (la pista entera es 1).
    y es el centro del renglon. Oculto = borde punteado; gris = no es del modelo."""
    borde = SUAVE if gris else color
    out.append(texto(x0 - 8, y + 4, nombre, tam=13, anclaje="end", color=SUAVE))
    out.append(caja(x0, _n(y - 8), ancho, 16, relleno="none", borde=LINEA, radio=3, grosor=1))
    if v > 0:
        out.append(caja(x0, _n(y - 8), _n(ancho * float(v)), 16,
                        relleno=mezclar(borde, 0.3), borde=borde, radio=3, grosor=2,
                        guiones=guiones))
    else:
        out.append(linea(x0, _n(y - 8), x0, _n(y + 8), color=borde, grosor=3))
    if tachada:
        out.append(linea(x0 - 2, _n(y + 10), x0 + ancho + 2, _n(y - 10), color=ALARMA, grosor=2.5))
    out.append(texto(x0 + ancho + 8, y + 4, valor, tam=12, anclaje="start", peso="700",
                     color=color_valor))
    return y


def mkv_c4_ej_creencia():
    h = m.paraguas()
    E = h["estados"]
    b0 = m.filtrar(h, [m.PARAGUAS])[0]
    tray, obs = m.simular_hmm(h, 6, m.SEMILLAS["c4-simular-semana"])
    real = {s: F(1) if s == tray[6] else F(0) for s in E}
    crea = m.filtrar(h, obs)[6]
    col = {"lluvia": COLOR_LLUVIA, "sol": COLOR_SOL}
    assert sum(b0.values()) == 1 and tray[6] == "lluvia"

    def arriba(out, y):
        y += 8
        for s in E:
            _barra(out, y, s, b0[s], f"{fr(b0[s])} ≈ {dec(b0[s])}", col[s])
            y += 24
        out.append(texto(X_PIE, y + 6, f"suma = {fr(sum(b0.values()))}", tam=13, peso="700",
                         anclaje="start"))
        return y + 14, (f"Barras de la creencia del día 0 tras paraguas: lluvia {fr(b0['lluvia'])}, "
                        f"aproximadamente {dec(b0['lluvia'])}, y sol {fr(b0['sol'])}, "
                        f"aproximadamente {dec(b0['sol'])}; suman 1.")

    def abajo(out, y):
        out.append(texto(X_PIE, y + 8, "Clima real del día 6 (oculto)", tam=13, peso="700",
                         anclaje="start"))
        y += 26
        for s in E:
            _barra(out, y, s, real[s], fr(real[s]), col[s], guiones=GUIONES_OCULTO)
            y += 24
        out.append(texto(X_PIE, y + 8, "Creencia del día 6, siete señales", tam=13, peso="700",
                         anclaje="start", color=SUAVE))
        y += 26
        for s in E:
            _barra(out, y, s, crea[s], f"≈ {dec(crea[s])}", col[s], gris=True, color_valor=SUAVE)
            y += 24
        return y, (f"Arriba, en barras con borde punteado y marcado como oculto, el clima real del día 6: "
                   f"lluvia {fr(real['lluvia'])} y sol {fr(real['sol'])}. Debajo, en gris, la creencia "
                   f"de ese día con las siete señales: lluvia aproximadamente {dec(crea['lluvia'])} y "
                   f"sol aproximadamente {dec(crea['sol'])}.")

    return _dos_paneles(["Ejemplo y contraejemplo", "una creencia"], [
        ("si", "b₀ tras ver paraguas, prior (1/2, 1/2)", arriba),
        ("no", "El clima real, que no se ve", abajo)],
        ["Borde punteado: oculto.", "Gris: lo que sí sabes."])


def _cadena_filtro(out, y, h, señales, final_tachada=False):
    """Barras de Pr(lluvia): b₀, la predicción, b₁, unidas por las flechas
    «predecir» y «corregir». Si la evidencia del dia 1 es 0, la ultima barra
    queda tachada. Devuelve (y libre, descripcion)."""
    o0, o1 = señales
    b0 = m.filtrar(h, [o0])[0]
    ev0 = m.verosimilitud_hmm(h, [o0])
    pred = m.predecir_estado(h, b0)
    pesos = {s: pred[s] * h["B"][s][o1] for s in h["estados"]}
    ev1 = sum(pesos.values())
    L = "lluvia"
    out.append(texto(X_PIE, y + 10, f"Día 0, ve {o0}: ev₀ = {fr(ev0)}", tam=12, anclaje="start",
                     color=SUAVE))
    yc = y + 30
    _barra(out, yc, "b₀", b0[L], _fv(b0[L]), COLOR_LLUVIA)
    out.append(_flecha(34, yc + 11, 34, yc + 31))
    out.append(texto(46, yc + 26, "predecir con P", tam=13, anclaje="start", peso="700"))
    yc += 42
    _barra(out, yc, "b₁|₀", pred[L], _fv(pred[L]), COLOR_LLUVIA)
    out.append(_flecha(34, yc + 11, 34, yc + 31))
    out.append(texto(46, yc + 26, f"corregir con B · ev₁ = {fr(ev1)}", tam=13, anclaje="start",
                     peso="700"))
    yc += 42
    if ev1 == 0:
        _barra(out, yc, "b₁", F(0), "señal imposible", COLOR_LLUVIA, tachada=True,
               color_valor=ALARMA)
        # la barra tachada no es una creencia: no hay con que normalizar
        final = None
    else:
        final = m.corregir(h, pred, o1)
        _barra(out, yc, "b₁", final[L], _fv(final[L]), COLOR_LLUVIA)
    desc = (f"Día 0, con {o0}: la creencia de lluvia b₀ vale {fr(b0[L])} y la evidencia {fr(ev0)}. "
            f"Flecha predecir con P: la barra pasa a {fr(pred[L])}. Flecha corregir con B, con {o1}: ")
    if final is None:
        desc += (f"los pesos son {', '.join(fr(pesos[s]) for s in h['estados'])}, la evidencia es "
                 f"{fr(ev1)} y la última barra aparece tachada con el letrero señal imposible.")
    else:
        desc += (f"la evidencia es {fr(ev1)} y la barra sube a {fr(final[L])}, "
                 f"aproximadamente {dec(final[L])}.")
    return yc + 14, desc


def ejemplo_c4_filtrar():
    h = m.paraguas()
    I = m._hmm(h["estados"], h["señales"], [F(1, 2), F(1, 2)], [[1, 0], [0, 1]], [[1, 0], [0, 1]])
    return _dos_paneles(["Ejemplo y contraejemplo", "el filtrado recursivo"], [
        ("si", "El paraguas: paraguas, paraguas",
         lambda out, y: _cadena_filtro(out, y, h, m.SEÑALES_EJ["filtrar"])),
        ("no", "P = B = I; paraguas, sin paraguas",
         lambda out, y: _cadena_filtro(out, y, I, [m.PARAGUAS, m.SIN_PARAGUAS]))],
        ["Barra: Pr(lluvia); el resto es sol.", "Tachada: no se puede normalizar."])


def mkv_c4_filtrar_traza():
    h = m.paraguas()
    señ = m.SEÑALES_EJ["coinciden"][:3]
    b = m.filtrar(h, señ)
    L = "lluvia"
    cre = [x[L] for x in b]
    pre = [h["mu0"][L]] + [m.predecir_estado(h, x)[L] for x in b[:-1]]
    titulo = ["La creencia de lluvia,", "día por día"]
    out = []
    y = encabezado(out, titulo)
    x0, x1, top, bot = 58, 284, y + 22, y + 22 + 170
    out.append(texto(X_PIE, top - 12, "Pr(lluvia)", tam=13, peso="700", anclaje="start"))

    def py(v):
        return bot - (bot - top) * float(v)
    for v, rot in ((0, "0"), (F(1, 2), "1/2"), (1, "1")):
        out.append(linea(x0, _n(py(v)), x1, _n(py(v)), color=mezclar(LINEA, 0.5), grosor=1,
                         guiones="5 4" if v == F(1, 2) else None))
        out.append(texto(x0 - 8, py(v) + 4, rot, tam=12, anclaje="end", color=SUAVE))
    xd = [x0 + (x1 - x0) * (2 * k + 1) / 6 for k in range(3)]
    desc = []
    for k in range(3):
        xp, xb = xd[k] - 13, xd[k] + 13
        sube = cre[k] > pre[k]
        out.append(_flecha(xp + 7, py(pre[k]), xb - 7, py(cre[k])))
        out.append(f'<circle cx="{_n(xp)}" cy="{_n(py(pre[k]))}" r="5" fill="{FONDO}" '
                   f'stroke="{COLOR_LLUVIA}" stroke-width="2"/>')
        out.append(f'<circle cx="{_n(xb)}" cy="{_n(py(cre[k]))}" r="5" fill="{COLOR_LLUVIA}" '
                   f'stroke="{COLOR_LLUVIA}" stroke-width="2"/>')
        out.append(texto(xp, py(pre[k]) + (18 if sube else -10), dec(pre[k]), tam=12))
        out.append(texto(xb, py(cre[k]) + (-10 if sube else 18), dec(cre[k]), tam=12, peso="700"))
        out.append(texto(xd[k], bot + 17, f"día {k}", tam=12, color=SUAVE))
        out.append(texto(xd[k], bot + 34, señ[k], tam=12))
        desc.append(f"Día {k}: de {fr(pre[k])} a {fr(cre[k])}, aproximadamente {dec(cre[k])}.")
    y = bot + 54
    out.append(texto(x0 - 8, bot + 34, "señal", tam=12, anclaje="end", color=SUAVE))
    y = _leyenda(out, y + 10, [
        (lambda x, yy: f'<circle cx="{_n(x)}" cy="{_n(yy)}" r="5" fill="{FONDO}" '
                       f'stroke="{COLOR_LLUVIA}" stroke-width="2"/>', "predicción, antes de la señal"),
        (lambda x, yy: f'<circle cx="{_n(x)}" cy="{_n(yy)}" r="5" fill="{COLOR_LLUVIA}" '
                       f'stroke="{COLOR_LLUVIA}" stroke-width="2"/>', "creencia, después de corregir"),
        (lambda x, yy: linea(_n(x - 12), _n(yy), _n(x + 12), _n(yy), color=SUAVE, grosor=1,
                             guiones="5 4"), "1/2: lo que creías al empezar")])
    y = pie(out, y + 6, [f"Día {k}: {fr(pre[k])} → {fr(cre[k])}" for k in range(3)], tam=13,
            color=TEXTO)
    return svg(titulo, "Gráfica de la creencia de lluvia contra el día, 0 a 2, con las señales "
               + ", ".join(señ) + " al pie. Por día, un punto hueco con la predicción y un punto "
               "lleno con la creencia, unidos por una flecha. " + " ".join(desc)
               + " Una línea punteada horizontal marca 1/2.", out, y)


FLUJOS_C4 = {
    "filtrar": dict(
        nombre="FILTRAR",
        titulo=["FILTRAR, en palabras", "predecir, corregir, normalizar"],
        pasos=[{"caja": ["Arranca: la predicción", "es μ₀"]},
               {"caja": ["Corrige: multiplica cada", "estado por B de la señal"]},
               {"caja": ["Suma los pesos:", "esa suma es la evidencia"]},
               {"rombo": ["¿La evidencia", "es 0?"], "abajo": "no"},
               {"caja": ["Normaliza: divide entre", "la evidencia y guarda b"]},
               {"rombo": ["¿Quedan", "días?"], "abajo": "sí"},
               {"caja": ["Predice con P", "y pasa al día siguiente"]},
               {"caja": ["Devuelve las creencias", "y las evidencias"], "fin": True,
                "sin_flecha": True},
               {"caja": ["Para: señal imposible"], "fin": True, "sin_flecha": True}],
        vueltas=[(6, 1, "otro día")],
        salidas=[(3, 8, "sí"), (5, 7, "no")],
        notas=["Una señal que ningún estado", "emite no se puede normalizar."]),
    "viterbi": dict(
        nombre="VITERBI",
        titulo=["VITERBI, en palabras", "máximo en lugar de suma"],
        pasos=[{"caja": ["Día 0: mejor₀ = μ₀ · B", "de la primera señal"]},
               {"caja": ["Pasa al día siguiente"]},
               {"caja": ["Para cada estado: prueba", "cada estado de ayer, guarda",
                         "el máximo y de dónde vino;", "multiplica por la emisión"]},
               {"rombo": ["¿Quedan", "días?"], "abajo": "no"},
               {"caja": ["Elige el estado con mayor", "mejor al final; si vale 0:", "señal imposible"]},
               {"caja": ["Sigue los apuntadores hacia", "atrás; devuelve la ruta", "y su conjunta"],
                "fin": True}],
        vueltas=[(3, 1, "sí: otro día")],
        notas=["Mismo recorrido que FILTRAR, pero", "con máximo y apuntadores."]),
    "aprender": dict(
        nombre="el ciclo de Baum-Welch",
        titulo=["Baum-Welch, en palabras", "contar con fracciones"],
        pasos=[{"caja": ["Modelo de hoy:", "μ₀, P, B"]},
               {"caja": ["Reparte cada día y cada par", "de días entre los estados,", "con toda la secuencia"]},
               {"caja": ["Conteos esperados:", "fracciones en lugar de enteros"]},
               {"caja": ["Cuenta: cada fila", "entre su total"]},
               {"caja": ["Modelo nuevo"]},
               {"rombo": ["¿La verosimilitud", "dejó de subir?"], "abajo": "sí", "mx": 90},
               {"caja": ["Termina"], "fin": True}],
        vueltas=[(5, 0, "no: otra vuelta")],
        notas=["Cada vuelta no baja la verosimilitud,", "pero puede parar en un modelo", "que no es el mejor."]),
}


def flujo_c4(clave):
    f = FLUJOS_C4[clave]
    salidas = f.get("salidas", ())
    out, alto = _flujo(f["titulo"], f["pasos"], f["vueltas"], f["notas"], salidas)
    return svg(f["titulo"], _desc_flujo(f["nombre"], f["pasos"], f["vueltas"], f["notas"],
                                        salidas), out, alto)


# ----------------------------------------------- pagina 4: decodificar ---

def _tabla_viterbi(h, señales):
    """(delta, previo): delta[t][s] = la mejor conjunta de una trayectoria que
    acaba en s el dia t; previo[t][s] = de que estado de ayer viene (el primero
    en empate, como markov.viterbi). Con fracciones exactas."""
    E, P, B = h["estados"], h["P"], h["B"]
    delta = [{s: h["mu0"][s] * B[s][señales[0]] for s in E}]
    previo = [None]
    for o in señales[1:]:
        d = delta[-1]
        pr = {t: m._primer_max(E, lambda s: d[s] * P[s][t]) for t in E}
        delta.append({t: d[pr[t]] * P[pr[t]][t] * B[t][o] for t in E})
        previo.append(pr)
    return delta, previo


def _ruta_viterbi(h, señales):
    """La ruta de markov.viterbi y su conjunta (ValueError si es imposible)."""
    return m.viterbi(h, señales)


TR_X = (54, 150, 246)          # centros de las tres columnas (dias 0, 1, 2)
TR_W, TR_H, TR_DY = 74, 40, 62


def _flecha_gruesa(x1, y1, x2, y2, color=ACENTO, grosor=3.0, cabeza=8):
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x2 - ux * cabeza, y2 - uy * cabeza
    px, py = -uy * 5, ux * 5
    return (f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(bx)}" y2="{_n(by)}" stroke="{color}" '
            f'stroke-width="{grosor}"/>'
            f'<polygon points="{_n(x2)},{_n(y2)} {_n(bx + px)},{_n(by + py)} '
            f'{_n(bx - px)},{_n(by - py)}" fill="{color}"/>')


def _trellis(out, y, h, señales, delta, previo, llenas, nuevo=None, ruta=None, cero=False):
    """La reticula de Viterbi: 3 columnas (dias 0, 1, 2), 2 filas (los estados
    de `h`, el primero arriba), siempre en las mismas posiciones. Las primeras
    `llenas` columnas llevan valor; la columna `nuevo` lleva borde grueso de
    acento. ★ marca el mayor de su columna. Flecha gruesa: de donde viene el
    maximo; delgada y punteada: la que perdio. `ruta`: estados del camino de
    regreso, con linea doble. cero: las columnas llenas con 0 van tachadas y
    sin flechas. Devuelve la y libre de abajo."""
    E = h["estados"]
    yc = [y + 44 + TR_H / 2, y + 44 + TR_H / 2 + TR_DY]
    for k in range(3):
        out.append(texto(TR_X[k], y + 12, f"día {k}", tam=12, color=SUAVE))
        out.append(texto(TR_X[k], y + 29, señales[k], tam=12))
    # flechas primero: los nodos las tapan en los bordes
    def punto_sal(k, j, i):          # sale del estado j hacia el estado i
        return TR_X[k] + TR_W / 2, yc[j] + (-9 if i == 0 else 9)

    def punto_ent(k, i, j):          # llega al estado i desde el estado j
        return TR_X[k] - TR_W / 2, yc[i] + (-9 if j == 0 else 9)
    en_ruta = set()
    if ruta:
        en_ruta = {(k, ruta[k - 1], ruta[k]) for k in range(1, len(ruta))}
    for k in range(1, llenas):
        if cero and all(delta[k][s] == 0 for s in E):
            continue
        for i, t in enumerate(E):
            for j, s in enumerate(E):
                if previo[k][t] == s:
                    continue
                (x1, y1), (x2, y2) = punto_sal(k - 1, j, i), punto_ent(k, i, j)
                out.append(f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
                           f'stroke="{SUAVE}" stroke-width="1.2" stroke-dasharray="3 3" '
                           f'marker-end="url(#s)"/>')
        for i, t in enumerate(E):
            j = E.index(previo[k][t])
            if (k, E[j], t) in en_ruta:
                continue
            (x1, y1), (x2, y2) = punto_sal(k - 1, j, i), punto_ent(k, i, j)
            out.append(_flecha_gruesa(x1, y1, x2, y2))
    for (k, s, t) in sorted(en_ruta):
        i, j = E.index(t), E.index(s)
        (x1, y1), (x2, y2) = punto_sal(k - 1, j, i), punto_ent(k, i, j)
        out.append(linea(_n(x1), _n(y1), _n(x2 - 1), _n(y2), color=ACENTO, grosor=7))
        out.append(linea(_n(x1), _n(y1), _n(x2 - 1), _n(y2), color=FONDO, grosor=3))
        # punta hacia atras: el camino de regreso va del dia k al dia k - 1
        d = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x1 - x2) / d, (y1 - y2) / d
        out.append(f'<polygon points="{_n(x1 - 1)},{_n(y1)} {_n(x1 + 9 * (-ux) + uy * 6)},'
                   f'{_n(y1 + 9 * (-uy) - ux * 6)} {_n(x1 + 9 * (-ux) - uy * 6)},'
                   f'{_n(y1 + 9 * (-uy) + ux * 6)}" fill="{ACENTO}"/>')
    # nodos
    for k in range(3):
        mejor = None
        if k < llenas and any(delta[k][s] > 0 for s in E):
            mejor = m._primer_max(E, lambda s: delta[k][s])
        for i, s in enumerate(E):
            x, cy = TR_X[k], yc[i]
            if k < llenas:
                grueso = k == nuevo
                out.append(caja(_n(x - TR_W / 2), _n(cy - TR_H / 2), TR_W, TR_H,
                                relleno=mezclar(COLOR_V, 0.18),
                                borde=ACENTO if grueso else COLOR_V, radio=7,
                                grosor=3.5 if grueso else 1.5))
                out.append(texto(x, cy - 3, s + (" ★" if s == mejor else ""), tam=12, color=SUAVE))
                out.append(texto(x, cy + 13, fr(delta[k][s]), tam=12, peso="700"))
                if delta[k][s] == 0:
                    out.append(linea(_n(x - 9), _n(cy + 13), _n(x + 9), _n(cy + 7), color=ALARMA,
                                     grosor=2.5))
            else:
                out.append(caja(_n(x - TR_W / 2), _n(cy - TR_H / 2), TR_W, TR_H,
                                relleno="none", borde=SUAVE, radio=7, grosor=1.5, guiones="4 3"))
                out.append(texto(x, cy + 4, s, tam=12, color=SUAVE))
    return yc[1] + TR_H / 2


def _desc_trellis(h, señales, delta, previo, llenas, nuevo, ruta):
    E = h["estados"]
    partes = [f"Retícula de tres columnas, días 0, 1 y 2, con las señales {', '.join(señales)} "
              f"arriba de cada una; dos filas, {E[0]} arriba y {E[1]} abajo."]
    for k in range(llenas):
        vals = " y ".join(f"{s} {fr(delta[k][s])}" for s in E)
        extra = ""
        if k > 0:
            extra = " Cada uno con flecha gruesa desde " + " y ".join(
                f"{previo[k][s]} del día {k - 1}" for s in E) + ", las flechas que perdieron punteadas."
        partes.append(f"Día {k}{', nuevo, con borde grueso' if k == nuevo else ''}: {vals}.{extra}")
    if llenas < 3:
        partes.append("Las columnas sin llenar tienen nodos vacíos punteados.")
    if ruta:
        partes.append("El camino de regreso " + ", ".join(ruta) + " va con línea doble gruesa.")
    return " ".join(partes)


def mkv_c4_trellis(n):
    h = m.paraguas()
    señ = m.SEÑALES_EJ["viterbi"]
    delta, previo = _tabla_viterbi(h, señ)
    ruta, conj = _ruta_viterbi(h, señ)
    assert delta[2][ruta[2]] == conj and [ "sol", "sol", "sol"] == ruta
    titulo = {1: ["Retícula de Viterbi,", "tramo 1: el día 0"],
              2: ["Retícula de Viterbi,", "tramo 2: el día 1"],
              3: ["Retícula de Viterbi,", "tramo 3: el día 2"]}[n]
    out = []
    y = encabezado(out, titulo)
    y = _trellis(out, y, h, señ, delta, previo, llenas=n, nuevo=n - 1,
                 ruta=ruta if n == 3 else None)
    renglones = ["Borde grueso: lo nuevo. ★: el mayor", "de su columna."]
    if n >= 2:
        renglones += ["Flecha gruesa: de dónde viene el", "máximo. Punteada: la que perdió."]
    if n == 3:
        renglones += ["Doble línea: el camino de regreso."]
    y = pie(out, y + 26, renglones)
    if n == 3:
        out.append(texto(X_PIE, y + 4, f"conjunta {fr(conj)}", tam=14, peso="700", anclaje="start"))
        y += 22
    desc = _desc_trellis(h, señ, delta, previo, n, n - 1, ruta if n == 3 else None)
    if n == 3:
        desc += f" Al pie: conjunta {fr(conj)}."
    return svg(titulo, desc, out, y)


def ejemplo_c4_decodificar():
    h = m.paraguas()
    señ = m.SEÑALES_EJ["viterbi"]
    d1, p1 = _tabla_viterbi(h, señ)
    ruta, conj = _ruta_viterbi(h, señ)
    E, O = h["estados"], h["señales"]
    malo = dict(h, señales=O + ["nieve"], B={s: {**h["B"][s], "nieve": F(0)} for s in E})
    señ2 = [m.SIN_PARAGUAS, "nieve", m.SIN_PARAGUAS]
    d2, p2 = _tabla_viterbi(malo, señ2)
    try:
        m.viterbi(malo, señ2)
        raise AssertionError("la señal con nieve deberia ser imposible")
    except ValueError:
        pass

    def arriba(out, y):
        yf = _trellis(out, y, h, señ, d1, p1, llenas=3, ruta=ruta)
        out.append(texto(X_PIE, yf + 22, f"ruta {', '.join(ruta)} · conjunta {fr(conj)}", tam=13,
                         peso="700", anclaje="start"))
        return yf + 34, (_desc_trellis(h, señ, d1, p1, 3, None, ruta)
                         + f" Conjunta {fr(conj)}.")

    def abajo(out, y):
        yf = _trellis(out, y, malo, señ2, d2, p2, llenas=3, cero=True)
        out.append(texto(X_PIE, yf + 22, "sin ruta: señal imposible", tam=13, peso="700",
                         anclaje="start", color=ALARMA))
        vals = [fr(d2[k][s]) for k in range(3) for s in E]
        return yf + 34, (f"Retícula con las señales {', '.join(señ2)} y B de 2 por 3, con la columna "
                         f"de nieve en ceros. Día 0: lluvia {vals[0]} y sol {vals[1]}. Días 1 y 2: "
                         f"{vals[2]} y {vals[3]}, y {vals[4]} y {vals[5]}, tachados. Sin camino, "
                         "con el letrero señal imposible.")
    return _dos_paneles(["Ejemplo y contraejemplo", "Viterbi necesita una conjunta > 0"], [
        ("si", "Sin paraguas, paraguas, sin paraguas", arriba),
        ("no", "B de 2×3: nadie emite nieve", abajo)],
        ["★ mayor de su columna. Doble línea:", "el camino de regreso. Rojo tachado: 0."])


# ------------------------------------------- pagina 5: aprender lo oculto ---

def _tira(out, y, dias, primer_dia):
    """Una celda por dia anotado: el numero de dia arriba, el estado dentro
    (con su color y su nombre). Devuelve la y libre de abajo."""
    w = 36
    x0 = (ANCHO - w * len(dias)) / 2
    for k, s in enumerate(dias):
        cx = x0 + w * (k + 0.5)
        color = COLOR_LLUVIA if s == "lluvia" else COLOR_SOL
        out.append(texto(cx, y + 10, str(primer_dia + k), tam=12, color=SUAVE))
        out.append(caja(_n(cx - w / 2 + 1), _n(y + 16), w - 2, 26, relleno=mezclar(color, 0.2),
                        borde=color, radio=5, grosor=2))
        out.append(texto(cx, y + 33, s, tam=12))
    return y + 46


def _panel_aprender(h, tray):
    E = h["estados"]
    _, obs = m.simular_hmm(h, 6, m.SEMILLAS["c4-simular-semana"])
    Ph, _ = m.contar_con_etiquetas(E, h["señales"], tray, [m.PARAGUAS] * len(tray))
    sale = {s: sum(1 for x in tray[:-1] if x == s) for s in E}
    filas = [[fr(Ph[s][t]) for t in E] for s in E]
    sumas = [fr(sum(Ph[s].values())) for s in E]
    malas = [i for i, s in enumerate(E) if sum(Ph[s].values()) != 1]
    return Ph, sale, filas, sumas, malas


def ejemplo_c4_aprender():
    h = m.paraguas()
    E = h["estados"]
    tray, _ = m.simular_hmm(h, 6, m.SEMILLAS["c4-simular-semana"])
    assert tray == ["sol", "sol"] + ["lluvia"] * 5

    def panel(dias, primer):
        def f(out, y):
            y = _tira(out, y + 4, dias, primer)
            Ph, sale, filas, sumas, malas = _panel_aprender(h, dias)
            out.append(texto(X_PIE, y + 14, " · ".join(f"{s} sale {sale[s]}" for s in E),
                             tam=13, peso="700", anclaje="start"))
            yb = _matriz_con_sumas(out, y + 52, E, filas, sumas, malas, rotulo="P̂")
            desc = (f"La tira de días anotados, del {primer} al {primer + len(dias) - 1}: "
                    f"{', '.join(dias)}. " + ", ".join(f"{s} sale {sale[s]} veces" for s in E)
                    + ". P gorro con filas " + " y ".join("(" + ", ".join(fi) + ")" for fi in filas) + ".")
            if malas:
                out.append(texto(X_PIE, yb + 20, "La fila de " + ", ".join(E[i] for i in malas)
                                 + ": sin estimar.", tam=13, peso="700", anclaje="start",
                                 color=ACENTO))
                yb += 26
                desc += " La fila de " + ", ".join(E[i] for i in malas) + " va marcada como sin estimar."
            return yb + 10, desc
        return f
    return _dos_paneles(["Ejemplo y contraejemplo", "aprender lo oculto"], [
        ("si", "Los siete días anotados", panel(tray, 0)),
        ("no", "Solo los días 2 a 6", panel(tray[2:], 2))],
        ["Doble borde: una fila que no suma 1."])


# --------------------------------------------- pagina 6: lenguaje pequeño ---

def _cruz(x, y, r=4, color=ALARMA):
    return (linea(_n(x - r), _n(y - r), _n(x + r), _n(y + r), color=color, grosor=2)
            + linea(_n(x - r), _n(y + r), _n(x + r), _n(y - r), color=color, grosor=2))


def _pastilla(cx, cy, nombre, w=108, h=44):
    """Estado oculto con nombre largo: pastilla de borde punteado."""
    return (caja(_n(cx - w / 2), _n(cy - h / 2), w, h, relleno=mezclar(COLOR_OCULTO, 0.18),
                 borde=COLOR_OCULTO, radio=14, grosor=2, guiones=GUIONES_OCULTO)
            + texto(cx, cy - 2, nombre, tam=12, peso="700")
            + texto(cx, cy + 14, "oculto", tam=12, color=SUAVE))


def mkv_c4_lenguaje_grafo():
    h = m.lenguaje_pequeno()
    E, O = h["estados"], h["señales"]
    assert len(E) == 3
    titulo = ["El lenguaje pequeño", "como modelo oculto"]
    out = []
    y = encabezado(out, titulo)
    yt = y + 76
    yv = yt + 118
    C = {0: (62, yt), 1: (238, yt), 2: (150, yv)}       # determinante, sustantivo, verbo
    # (origen, destino): (x1, y1, x2, y2) de la flecha, y donde va su rotulo (dx, dy, ancla)
    G = {
        (0, 1): (118, yt - 8, 182, yt - 8, (150, yt - 14, "middle")),
        (1, 0): (182, yt + 8, 118, yt + 8, (150, yt + 26, "middle")),
        (1, 2): (258, yt + 22, 196, yv - 22, (+8, 0, "start")),
        (2, 1): (176, yv - 22, 222, yt + 22, (-8, 0, "end")),
        (2, 0): (112, yv - 22, 86, yt + 22, (+8, 0, "start")),
        (0, 2): (36, yt + 22, 96, yv - 6, (-8, 0, "end")),
    }
    lazos = {0: (-1, 62), 1: (-1, 238), 2: (+1, 150)}   # hacia arriba (-1) o abajo (+1)
    ceros, reales = [], []
    for i, s in enumerate(E):
        for j, t in enumerate(E):
            p = h["P"][s][t]
            if p == 0:
                ceros.append((s, t))
            else:
                reales.append((s, t, p))
                x1, y1, x2, y2, (lx, ly, an) = G[(i, j)]
                out.append(_flecha(x1, y1, x2, y2))
                if an == "middle":
                    out.append(texto(lx, ly, fr(p), tam=13, peso="700"))
                else:
                    out.append(texto((x1 + x2) / 2 + lx, (y1 + y2) / 2 + 4, fr(p), tam=13,
                                     peso="700", anclaje=an))
    for s, t in ceros:
        i, j = E.index(s), E.index(t)
        if i == j:
            cx, cy = C[i]
            dy, base = lazos[i][0], (cy - 22 if lazos[i][0] < 0 else cy + 22)
            out.append(f'<path d="M {cx - 22} {base} C {cx - 26} {base + dy * 42} {cx + 26} '
                       f'{base + dy * 42} {cx + 22} {base}" fill="none" stroke="{SUAVE}" '
                       f'stroke-width="1.5" stroke-dasharray="3 3"/>')
            out.append(_cruz(cx, base + dy * 31))
            out.append(texto(cx + 18, base + dy * 36 + 4, "0", tam=13, peso="700", anclaje="start"))
        else:
            x1, y1, x2, y2, _ = G[(i, j)]
            out.append(f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
                       f'stroke="{SUAVE}" stroke-width="1.5" stroke-dasharray="3 3"/>')
            out.append(_cruz((x1 + x2) / 2, (y1 + y2) / 2))
            out.append(texto((x1 + x2) / 2 - 10, (y1 + y2) / 2 + 4, "0", tam=13, peso="700",
                             anclaje="end"))
    for i, s in enumerate(E):
        out.append(_pastilla(*C[i], s))
    # lo que emite cada estado, en el orden del dibujo: determinante, verbo, sustantivo
    y0 = yv + 22 + 62
    out.append(texto(X_PIE, y0, "Lo que emite cada estado:", tam=12, anclaje="start", color=SUAVE))
    orden = [0, 2, 1]
    xs = {0: 62, 2: 150, 1: 238}
    filas_max = 0
    for i in orden:
        s = E[i]
        palabras = [(o, h["B"][s][o]) for o in O if h["B"][s][o] > 0]
        filas_max = max(filas_max, len(palabras))
        out.append(texto(xs[i], y0 + 22, s, tam=12, peso="700"))
        for k, (o, p) in enumerate(palabras):
            ty = y0 + 44 + 21 * k
            if o == "casa":
                out.append(caja(_n(xs[i] - 38), _n(ty - 15), 76, 21, relleno="none", borde=ACENTO,
                                radio=6, grosor=2))
            out.append(texto(xs[i] - 31, ty, f"{o} {fr(p)}", tam=13, anclaje="start"))
    y = y0 + 44 + 21 * filas_max
    mu0 = "(" + ", ".join(fr(h["mu0"][s]) for s in E) + ")"
    y = pie(out, y + 12, [f"μ₀ = {mu0}", "orden: determinante, sustantivo, verbo",
                          "Punteado: oculto. ×: cero de P.", "Recuadro: casa, de dos estados."])
    desc = ("Grafo de tres estados ocultos con borde punteado: " + ", ".join(E) + ". Flechas: "
            + "; ".join(f"de {s} a {t} {fr(p)}" for s, t, p in reales) + ". Los cuatro ceros "
            "van marcados con una cruz y el rótulo 0 sobre una línea punteada sin punta: "
            + "; ".join(f"{s} a {t}" for s, t in ceros) + ". Debajo, las palabras de cada estado "
            "con su probabilidad: " + "; ".join(
                f"{E[i]} " + ", ".join(f"{o} {fr(h['B'][E[i]][o])}" for o in O if h['B'][E[i]][o] > 0)
                for i in range(3)) + ". La palabra casa aparece bajo sustantivo y bajo verbo, "
            f"en recuadro. Al pie, μ₀ = {mu0}.")
    assert len(ceros) == 4
    return svg(titulo, desc, out, y)


# ------------------------------------------ pagina 7: decidir sin ver ---

def mkv_c4_ds_costos():
    h = m.paraguas()
    lo, hi = m.rango_mirar()
    assert (lo, hi) == (F(1, 6), F(1, 2))
    titulo = ["Los tres costos", "según la creencia b"]
    out = []
    y = encabezado(out, titulo)
    x0, x1, top = 48, 284, y + 24
    bot = top + 150

    def px(b):
        return x0 + (x1 - x0) * float(b)

    def py(c):
        return bot - (bot - top) * float(c) / 2
    out.append(texto(X_PIE, top - 12, "costo esperado del día", tam=13, peso="700", anclaje="start"))
    for c in (0, F(1, 2), 1, F(3, 2), 2):
        out.append(linea(x0, _n(py(c)), x1, _n(py(c)), color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(x0 - 8, py(c) + 4, fr(c), tam=12, anclaje="end", color=SUAVE))
    for b in (0, F(1, 4), F(1, 2), F(3, 4), 1):
        out.append(linea(_n(px(b)), top, _n(px(b)), bot, color=mezclar(LINEA, 0.5), grosor=1))
        out.append(texto(px(b), bot + 17, fr(b), tam=12, color=SUAVE))
    out.append(texto((x0 + x1) / 2, bot + 36, "b = Pr(lluvia)", tam=13, peso="700"))
    c = m.costos_dia
    # la envolvente inferior, debajo de las lineas
    env = [(b, min(c(b).values())) for b in (F(0), lo, hi, F(1))]
    assert [v for _, v in env] == [0, F(2, 3), 1, 1]
    out.append(_polilinea([(px(b), py(v)) for b, v in env], mezclar(ACENTO, 0.45), grosor=9))
    # las lineas: color, marca en la linea y rotulo en la leyenda
    lineas = [
        ("llevar", "rombo", COLOR_V, [(0, c(0)["llevar"]), (1, c(1)["llevar"])], F(9, 10), "llevar = 1"),
        ("no llevar", "triangulo", COLOR_C, [(0, c(0)["no llevar"]), (F(1, 2), c(F(1, 2))["no llevar"])],
         F(9, 20), "no llevar = 4b"),
        ("mirar", "cuadro", COLOR_REAL, [(0, c(0)["mirar"]), (1, c(1)["mirar"])], F(9, 10),
         "mirar = 1/2 + b"),
    ]
    gratis = [(F(0), c(0)["no llevar"] - c(0)["no llevar"]), (F(1), F(1) * m.COSTO_PARAGUAS)]
    assert m.costo_actuar(F(1, 3)) - m.valor_informacion(F(1, 3)) == F(1, 3)
    out.append(_polilinea([(px(b), py(v)) for b, v in gratis], TEXTO, guiones="2 4", grosor=2))
    for _, forma, color, pts, bm, _r in lineas:
        out.append(_polilinea([(px(b), py(v)) for b, v in pts], color, grosor=2.5))
    for nombre, forma, color, pts, bm, _r in lineas:
        (b0, v0), (b1, v1) = pts
        v = v0 + (v1 - v0) * (bm - b0) / (b1 - b0)
        out.append(_marca(forma, px(bm), py(v), color, r=5))
    # los puntos que se leen
    marcas = [(F(1, 6), F(2, 3), None, None),
              (F(1, 4), F(1), "1", (-9, -8, "end")),
              (F(1, 4), F(3, 4), "3/4", (7, 18, "start")),
              (F(1, 2), F(1), "(1/2, 1)", (8, 18, "start"))]
    assert c(F(1, 6))["no llevar"] == c(F(1, 6))["mirar"] == F(2, 3)
    assert c(F(1, 4))["llevar"] == c(F(1, 4))["no llevar"] == 1 and c(F(1, 4))["mirar"] == F(3, 4)
    assert c(F(1, 2))["llevar"] == c(F(1, 2))["mirar"] == 1
    for b, v, rot, pos in marcas:
        out.append(f'<circle cx="{_n(px(b))}" cy="{_n(py(v))}" r="3.5" fill="{TEXTO}"/>')
        if rot is None:
            # el punto (1/6, 2/3) queda entre tres lineas: su rotulo va arriba a la
            # izquierda, en el hueco libre, unido por una guia fina
            out.append(linea(_n(px(b) - 8), _n(py(1.42) + 5), _n(px(b)), _n(py(v) - 4),
                             color=SUAVE, grosor=1))
            out.append(texto(x0 + 4, py(1.42), "(1/6, 2/3)", tam=12, anclaje="start", peso="700"))
            continue
        dx, dy, an = pos
        out.append(texto(px(b) + dx, py(v) + dy, rot, tam=12, anclaje=an, peso="700"))
    # b = 9/11: llevar
    b911 = F(9, 11)
    assert m.decidir(b911) == "llevar"
    out.append(linea(_n(px(b911)), _n(py(1)), _n(px(b911)), bot, color=ACENTO, grosor=2, guiones="4 3"))
    out.append(_marca("rombo", px(b911), py(1), ACENTO, r=5))
    out.append(texto(px(b911) - 6, py(0.12), "b = 9/11: llevar", tam=12, anclaje="end", peso="700"))
    # las tres regiones
    yb = bot + 72
    out.append(texto(X_PIE, yb - 8, "Lo que conviene, según b:", tam=12, anclaje="start", color=SUAVE))
    yb += 2
    tramos = [(F(0), lo, "no llevar", COLOR_C), (lo, hi, "mirar", COLOR_REAL), (hi, F(1), "llevar", COLOR_V)]
    for a, z, nombre, color in tramos:
        out.append(caja(_n(px(a)), yb, _n(px(z) - px(a)), 36, relleno=mezclar(color, 0.3),
                        borde=color, radio=4, grosor=2))
        if nombre == "no llevar":
            out.append(texto((px(a) + px(z)) / 2, yb + 15, "no", tam=12))
            out.append(texto((px(a) + px(z)) / 2, yb + 29, "llevar", tam=12))
        else:
            out.append(texto((px(a) + px(z)) / 2, yb + 22, nombre, tam=13, peso="700"))
    for b in (F(0), lo, hi, F(1)):
        out.append(texto(px(b), yb + 52, fr(b), tam=12, color=SUAVE))
    y = yb + 66
    forma_mini = {"rombo": "rombo", "triangulo": "triangulo", "cuadro": "cuadro"}
    items = [(lambda x, yy, f=forma, col=color: linea(_n(x - 12), _n(yy), _n(x + 12), _n(yy), color=col,
                                                      grosor=2.5) + _marca(f, x, yy, col, r=5), r)
             for _n_, forma, color, _p, _b, r in lineas for f in [forma]]
    items.append((lambda x, yy: linea(_n(x - 12), _n(yy), _n(x + 12), _n(yy), color=TEXTO, grosor=2,
                                      guiones="2 4"), "y = b: ver gratis"))
    items.append((lambda x, yy: linea(_n(x - 12), _n(yy), _n(x + 12), _n(yy),
                                      color=mezclar(ACENTO, 0.45), grosor=9), "el menor de los tres"))
    y = _leyenda(out, y + 4, items)
    desc = ("Gráfica con la creencia b = Pr(lluvia) de 0 a 1 en el eje horizontal y el costo esperado "
            "del día de 0 a 2 en el vertical. Tres rectas sólidas, cada una con su marca: llevar, "
            "horizontal en 1; no llevar, 4b, que sube desde 0; mirar, 1/2 + b, que sube desde 1/2. "
            "Una recta punteada, y = b, marca ver gratis. Una banda ancha marca el menor de los tres. "
            "Abajo, tres regiones: no llevar de 0 a 1/6, mirar entre 1/6 y 1/2, llevar de 1/2 a 1. "
            "Puntos marcados: en 1/6, no llevar y mirar valen 2/3; en 1/4, llevar y no llevar valen 1 "
            "y mirar 3/4; en 1/2, mirar y llevar valen 1. Una marca en b = 9/11 dice llevar.")
    return svg(titulo, desc, out, y)


def _ventana(h, b, señal):
    """(Pr(señal), creencia tras verla): Bayes sobre el prior b."""
    pesos = {s: b[s] * h["B"][s][señal] for s in h["estados"]}
    ev = sum(pesos.values())
    return ev, {s: p / ev for s, p in pesos.items()}


def _hoja(out, cx, y, lineas, w=128):
    h = 16 + 18 * len(lineas)
    out.append(caja(_n(cx - w / 2), _n(y), w, h, relleno=mezclar(COLOR_V, 0.12), borde=SUAVE,
                    radio=8, grosor=1.5))
    for k, r in enumerate(lineas):
        out.append(texto(cx, y + 22 + 18 * k, r, tam=13, peso="700" if k == 1 else "normal"))
    return y + h


def _arbol_mirar(out, y, ramas, cuentas, veredicto):
    """Raiz «mirar» y dos ramas. ramas: [(rotulo en dos renglones, hoja)]."""
    out.append(caja(_n(150 - 70), _n(y), 140, 28, relleno=mezclar(COLOR_C, 0.18), borde=COLOR_C,
                    radio=8, grosor=2))
    out.append(texto(150, y + 19, "mirar: cuesta 1/2", tam=13, peso="700"))
    xs = (72, 228)
    fin = y
    for cx, (rot, hoja) in zip(xs, ramas):
        sx = 150 + (cx - 150) * 0.3
        out.append(_flecha(sx, y + 28, cx + (150 - cx) * 0.12, y + 80))
        mx = (sx + cx) / 2
        for k, r in enumerate(rot):
            if cx < 150:
                out.append(texto(mx - 8, y + 50 + 14 * k, r, tam=12, anclaje="end"))
            else:
                out.append(texto(mx + 8, y + 50 + 14 * k, r, tam=12, anclaje="start"))
        fin = _hoja(out, cx, y + 84, hoja)
    for k, r in enumerate(cuentas):
        out.append(texto(X_PIE, fin + 20 + 19 * k, r, tam=13, anclaje="start", peso="700"))
    out.append(texto(X_PIE, fin + 20 + 19 * len(cuentas), veredicto, tam=13, anclaje="start",
                     color=SUAVE))
    return fin + 28 + 19 * len(cuentas)


def ejemplo_c4_decidir():
    h = m.paraguas()
    b = {"lluvia": F(1, 3), "sol": F(2, 3)}
    c = m.costos_dia
    actuar = m.costo_actuar(b["lluvia"])
    assert actuar == 1

    def accion(bl):
        cs = c(bl)
        return ("llevar", cs["llevar"]) if cs["llevar"] <= cs["no llevar"] else ("no llevar", cs["no llevar"])

    # arriba: mirar revela el clima
    ramas1 = []
    tot1 = m.COSTO_MIRAR
    for s, bl in (("lluvia", F(1)), ("sol", F(0))):
        a, cost = accion(bl)
        ramas1.append(([f"{s} {fr(b[s])}"], [f"{s}: b = {fr(bl)}", a, f"costo {fr(cost)}"]))
        tot1 += b[s] * cost
    assert tot1 == m.costo_mirar(b["lluvia"]) == F(5, 6) < actuar

    def arriba(out, y):
        yf = _arbol_mirar(out, y + 4, ramas1,
                          [f"{fr(m.COSTO_MIRAR)} + {fr(b['lluvia'])}·1 + {fr(b['sol'])}·0 = {fr(tot1)}"],
                          f"{fr(tot1)} < {fr(actuar)}: mirar gana")
        return yf, ("Árbol de decisión con b = 1/3 y precio 1/2: mirar revela el clima; rama lluvia con "
                    "probabilidad 1/3 lleva a llevar, costo 1; rama sol con 2/3 lleva a no llevar, costo "
                    f"0; total {fr(m.COSTO_MIRAR)} + 1/3 = {fr(tot1)}, menor que actuar ya, {fr(actuar)}.")

    # abajo: la ventana empañada solo deja ver si el vecino trae paraguas
    ramas2, tot2, trozos = [], m.COSTO_MIRAR, []
    for o in (m.PARAGUAS, m.SIN_PARAGUAS):
        ev, post = _ventana(h, b, o)
        a, cost = accion(post["lluvia"])
        ramas2.append((o.split(" ", 1) if o != m.PARAGUAS else [o], None))
        ramas2[-1] = (([o, fr(ev)] if o == m.PARAGUAS else ["sin paraguas", fr(ev)]),
                      [f"lluvia: b = {fr(post['lluvia'])}", a, f"costo {fr(cost)}"])
        tot2 += ev * cost
        trozos.append((ev, cost))
    assert tot2 == F(16, 15) > actuar

    def abajo(out, y):
        yf = _arbol_mirar(out, y + 4, ramas2,
                          [f"{fr(m.COSTO_MIRAR)} + {fr(trozos[0][0])}·{fr(trozos[0][1])} + "
                           f"{fr(trozos[1][0])}·{fr(trozos[1][1])}", f"= {fr(tot2)}"],
                          f"{fr(tot2)} > {fr(actuar)}: mirar pierde")
        return yf, ("Árbol con la ventana empañada, que muestra solo una señal: rama paraguas con "
                    f"{fr(trozos[0][0])} deja la lluvia en {ramas2[0][1][0].split('= ')[1]} y lleva a "
                    f"llevar, costo 1; rama sin paraguas con {fr(trozos[1][0])} deja la lluvia en "
                    f"{ramas2[1][1][0].split('= ')[1]} y lleva a no llevar, costo {fr(trozos[1][1])}; "
                    f"total {fr(tot2)}, mayor que {fr(actuar)}.")
    return _dos_paneles(["Ejemplo y contraejemplo", "pagar por mirar"], [
        ("si", "b = 1/3; mirar revela el clima", arriba),
        ("no", "b = 1/3; ventana con niebla", abajo)])


# ------------------------------------------- pagina 8: hacia el refuerzo ---

def mkv_c4_mapa_2x2():
    titulo = ["El mapa de dos ejes", "lo visto y lo que falta"]
    out = []
    y = encabezado(out, titulo)
    cw, ch = 110, 104
    cx0 = (60, 174)                    # x de cada columna
    xc = (cx0[0] + cw / 2, cx0[1] + cw / 2)
    out.append(texto(xc[0], y + 14, "estado visible", tam=13, peso="700"))
    out.append(texto(xc[1], y + 14, "estado oculto", tam=13, peso="700"))
    # flecha horizontal del renglon de arriba
    ya = y + 50
    out.append(texto((xc[0] + xc[1]) / 2, ya - 14, "se deja de ver el estado", tam=12, color=SUAVE,
                     peso="700"))
    out.append(_flecha(xc[0] + 20, ya - 6, xc[1] - 20, ya - 6))
    yr = (ya + 4, ya + 4 + ch + 12)
    celdas = [
        (0, 0, True, ["Planificar", "un MDP"], ["clase 3: Bellman,", "iterar valores", "y políticas"]),
        (0, 1, True, ["POMDP"], ["clase 4: creencia,", "filtrar,", "decidir con b"]),
        (1, 0, False, ["Refuerzo", "clásico"], ["falta: el modelo;", "se aprende de", "episodios"]),
        (1, 1, False, ["Refuerzo con", "observación", "parcial"], ["falta: el modelo", "y el estado"]),
    ]
    for r, cc, visto, tit, nota in celdas:
        x, yy = cx0[cc], yr[r]
        if visto:
            out.append(caja(x, yy, cw, ch, relleno=mezclar(COLOR_V, 0.22), borde=COLOR_V, radio=10,
                            grosor=2))
        else:
            out.append(caja(x, yy, cw, ch, relleno="none", borde=SUAVE, radio=10, grosor=2,
                            guiones="5 4"))
        ty = yy + 20
        for k, t in enumerate(tit):
            out.append(texto(x + cw / 2, ty, t, tam=13, peso="700"))
            ty += 16
        ty += 3
        for t in nota:
            out.append(texto(x + cw / 2, ty, t, tam=12, color=TEXTO if visto else SUAVE))
            ty += 15
    # renglones (dos renglones de texto girado) y flecha vertical, a la izquierda
    for r, (a1, a2) in enumerate((("modelo", "conocido"), ("modelo", "desconocido"))):
        out.append(girado(12, yr[r] + ch / 2, a1, tam=12))
        out.append(girado(27, yr[r] + ch / 2, a2, tam=12))
    ymed = (yr[0] + yr[1] + ch) / 2
    out.append(_flecha(54, yr[0] + ch / 2, 54, yr[1] + ch / 2 - 2))
    out.append(girado(45, ymed, "se deja de conocer el modelo", tam=12))
    y = yr[1] + ch + 22
    y = pie(out, y, ["Relleno: ya se vio.", "Punteado: falta por ver."])
    desc = ("Cuadro de dos por dos. Columnas: estado visible y estado oculto. Renglones: modelo conocido "
            "y modelo desconocido. Arriba a la izquierda, Planificar un MDP, con la marca clase 3: "
            "Bellman, iterar valores y políticas. Arriba a la derecha, POMDP, con la marca clase 4: "
            "creencia, filtrar, decidir con b. Estas dos casillas van rellenas: ya se vieron. Abajo a "
            "la izquierda, Refuerzo clásico, con falta: el modelo; se aprende de episodios. Abajo a la "
            "derecha, Refuerzo con observación parcial, con falta: el modelo y el estado. Las dos de "
            "abajo van solo con borde punteado: no se han visto. Una flecha horizontal en el renglón de "
            "arriba dice se deja de ver el estado; una vertical en la columna izquierda dice se deja de "
            "conocer el modelo.")
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
    **{f"mkv-c2-ej-{c}": (lambda c=c: ejemplo(c)) for c in EJEMPLOS},
    "mkv-c3-punto-fijo": mkv_c3_punto_fijo,
    "mkv-c3-escalera": mkv_c3_escalera,
    "mkv-c3-escalera-arbol-vs-grafo": mkv_c3_escalera_arbol_vs_grafo,
    "mkv-c3-flujo-hacia-atras": lambda: flujo("hacia-atras"),
    "mkv-c3-pasillo": mkv_c3_pasillo,
    "mkv-c3-pasillo-mdp": mkv_c3_pasillo_mdp,
    "mkv-c3-politica-elige-filas": mkv_c3_politica_elige_filas,
    "mkv-c3-cuatro-cadenas": mkv_c3_cuatro_cadenas,
    "mkv-c3-flujo-evaluar": lambda: flujo("evaluar"),
    "mkv-c3-cuatro-politicas-plano": mkv_c3_cuatro_politicas_plano,
    "mkv-c3-simular-politica": mkv_c3_simular_politica,
    "mkv-c3-bellman-1d": mkv_c3_bellman_1d,
    "mkv-c3-fronteras": mkv_c3_fronteras,
    "mkv-c3-flujo-valores": lambda: flujo("valores"),
    "mkv-c3-iterar-valores": mkv_c3_iterar_valores,
    "mkv-c3-residuo": mkv_c3_residuo,
    "mkv-c3-pasillo-largo": mkv_c3_pasillo_largo,
    "mkv-c3-flujo-politicas": lambda: flujo("politicas"),
    "mkv-c3-rondas-politicas": mkv_c3_rondas_politicas,
    "mkv-c3-region-lp": mkv_c3_region_lp,
    "mkv-c3-mapa-decidir": mkv_c3_mapa_decidir,
    **{f"mkv-c3-ej-{c}": (lambda c=c: ejemplo_c3(c)) for c in EJEMPLOS_C3},
    "mkv-c4-hmm-grafo": mkv_c4_hmm_grafo,
    "mkv-c4-ej-modelo": ejemplo_c4_modelo,
    "mkv-c4-ej-creencia": mkv_c4_ej_creencia,
    "mkv-c4-ej-filtrar": ejemplo_c4_filtrar,
    "mkv-c4-flujo-filtrar": lambda: flujo_c4("filtrar"),
    "mkv-c4-filtrar-traza": mkv_c4_filtrar_traza,
    "mkv-c4-flujo-viterbi": lambda: flujo_c4("viterbi"),
    "mkv-c4-trellis-1": lambda: mkv_c4_trellis(1),
    "mkv-c4-trellis-2": lambda: mkv_c4_trellis(2),
    "mkv-c4-trellis-3": lambda: mkv_c4_trellis(3),
    "mkv-c4-ej-decodificar": ejemplo_c4_decodificar,
    "mkv-c4-ej-aprender": ejemplo_c4_aprender,
    "mkv-c4-flujo-aprender": lambda: flujo_c4("aprender"),
    "mkv-c4-lenguaje-grafo": mkv_c4_lenguaje_grafo,
    "mkv-c4-ds-costos": mkv_c4_ds_costos,
    "mkv-c4-ej-decidir": ejemplo_c4_decidir,
    "mkv-c4-mapa-2x2": mkv_c4_mapa_2x2,
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
