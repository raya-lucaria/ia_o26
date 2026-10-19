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

Los ids llevan prefijo "mkv-c1-": los ids de objeto numerado son unicos en
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


def _flujo(titulo, pasos, vueltas=(), notas=()):
    """pasos: dicts con «caja» (renglones; el primero en negritas; fin=True
    en la salida) o «rombo» (renglones), «abajo» (rotulo de la salida de
    abajo) y «lado» (rotulo, renglones): caja a la derecha que baja a la
    entrada del paso siguiente. vueltas: [(desde, hasta, rotulo)]."""
    out = []
    y = encabezado(out, titulo) + 8
    geo = []
    for k, p in enumerate(pasos):
        if k:
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
                out.append(texto((FL_CX + FL_MX + FL_LADO_X0) / 2, cy - 9, rot, tam=13,
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
    y = y - FL_GAP + 26
    if notas:
        y = pie(out, y, notas)
    return out, y - 8


def _desc_flujo(nombre, pasos, vueltas, notas=()):
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
        pasos=[{"caja": ["Empieza con μ₀", "(un vector fila)"]},
               {"caja": ["Multiplica por P̂:", "μ ← μ P̂"]},
               {"rombo": ["¿Ya van", "t pasos?"], "abajo": "sí"},
               {"caja": ["Devuelve μₜ"], "fin": True}],
        vueltas=[(2, 1, "no: otro paso")],
        notas=["Cada paso cuesta k² productos", "con k estados."]),
    "generar": dict(
        nombre="generar texto",
        titulo=["Generar, en palabras", "con memoria h"],
        pasos=[{"caja": ["Empieza con un", "contexto de h símbolos"]},
               {"rombo": ["¿Se vio el", "contexto?"], "abajo": "sí",
                "lado": ("no", ["usa la fila", "suavizada"])},
               {"caja": ["Muestrea su fila", "con un u nuevo"]},
               {"caja": ["Escribe el símbolo", "y desliza el contexto"]},
               {"rombo": ["¿Llegaste", "al largo?"], "abajo": "sí"},
               {"caja": ["Devuelve el texto"], "fin": True}],
        vueltas=[(4, 1, "no: otro símbolo")],
        notas=["Un contexto nunca visto no se", "reinicia: su fila suavizada da",
               "1/|Σ| a cada símbolo."]),
}


def flujo(clave):
    f = FLUJOS[clave]
    out, alto = _flujo(f["titulo"], f["pasos"], f["vueltas"], f["notas"])
    return svg(f["titulo"], _desc_flujo(f["nombre"], f["pasos"], f["vueltas"], f["notas"]),
               out, alto)


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
        f"Franja: ±2 errores estándar (±{dec(banda)}).",
        f"La mayor diferencia: {dec(peor)}, unos",
        f"{peor_z:.1f} errores estándar."])
    desc = ("Probabilidad de estar en V en el paso t, de t = 0 a 8, con la matriz del corpus. "
            "Arriba, la cuenta μ₀P̂ᵗ (línea) y la fracción de "
            f"{miles(n)} réplicas en V (marcas). Desde V: cuenta "
            + ", ".join(dec(p) for p in datos["V"]["cuenta"]) + "; réplicas "
            + ", ".join(dec(p) for p in datos["V"]["simulada"]) + ". Desde C: cuenta "
            + ", ".join(dec(p) for p in datos["C"]["cuenta"]) + "; réplicas "
            + ", ".join(dec(p) for p in datos["C"]["simulada"])
            + f". Abajo, réplicas menos cuenta, con una franja de ±2 errores estándar "
            f"(±{dec(banda)}); la mayor diferencia es {dec(peor)}, unos {peor_z:.1f} errores "
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
        (lambda x, yy: _marca("circulo", x, yy, COLOR_V),
         f"cadena (q = {dec(r['q_markov'])})"),
        (lambda x, yy: _marca("cuadro", x, yy, COLOR_C, r=4),
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
        for modelo, dx, forma, color in (("markov", 6, "circulo", COLOR_V),
                                         ("independiente", 16, "cuadro", COLOR_C)):
            med, p5, p95 = sim[modelo][ell]
            out.append(linea(_n(xc + dx), _n(_y_log(p95, top, alto)), _n(xc + dx),
                             _n(_y_log(p5, top, alto)), color=color, grosor=1.5))
            out.append(_marca(forma, xc + dx, _y_log(med, top, alto), color,
                              r=4.5 if forma == "circulo" else 4))
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
            f"{dec(r['q_markov'])} (círculos) y de letras independientes con q = "
            f"{dec(r['q_independiente'])} (cuadrados). " + "; ".join(
                f"ℓ = {ell}: reales {miles(reales.get(ell, 0))}, cadena "
                f"{miles(sim['markov'][ell][0])}, independientes "
                f"{miles(sim['independiente'][ell][0])}" for ell in ells)
            + ". La franja del 5 % al 95 % de las réplicas es más angosta que la marca.")
    return svg(titulo, desc, out, y)


# ----------------------------------------------------------- catalogo ---

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
