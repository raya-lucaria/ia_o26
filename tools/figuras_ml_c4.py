"""Figuras de la clase 4 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C4: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c4-", es un error.

Dueno: prog-c4 (lo creo vacio prog-lab en U.T3). Reglas para llenarlo:
- los diagramas conceptuales se escriben como SVG a mano con las primitivas
  y la paleta de gen_aprendizaje_maquina (marco, texto, caja, flecha, ROLES...);
- las graficas de datos se dibujan con las funciones dibujar_* de ml_lab y
  tema="sitio", y se convierten con gen.svg_de_matplotlib(fig, aria=...);
- ml_lab se pide con gen.ml_lab() dentro de la funcion de la figura, nunca
  al importar este modulo (importacion perezosa, contrato §7.1);
- ningun color de rol se copia como literal: se lee de gen.ROLES;
- las cifras que se dibujan salen de ml_lab o de tools/ml_cifras_c4.py.

Tres graficas de datos no tienen su dibujar_* en ml_lab 1.5 y se dibujan aqui
con matplotlib y los mismos objetos de ml_cifras_c4 (DECISIÓN prog-c4-2):
las regiones de tres clases (dibujar_frontera es binaria; SOLICITUD
prog-c4-1), el mapa de tamaños de C(x) con la cobertura contra 1 − δ, y la
cobertura por clase promediada sobre calibraciones repetidas (la garantía es
un promedio; una sola calibración puede quedar abajo de 1 − δ).

Sus pruebas propias van en tools/test_figuras_ml_c4.py (sin prosa); las
guardas comunes, en tools/test_gen_aprendizaje_maquina.py.

Como en las clases 1 y 3, lo que ml_lab dibuja con transparencia se hornea
aqui contra el panel (`_sin_opacidad`): las guardas prohiben toda opacidad.
"""
import math
import re

import gen_aprendizaje_maquina as gen
from gen_aprendizaje_maquina import (ACENTO, FONDO, LINEA, PANEL, SUAVE, TEXTO,
                                     caja, flecha, linea, mezclar, svg, texto)

VERDE = gen.color_rol("f_verdadera")
CIAN = gen.color_rol("entrenamiento")
ORO = gen.color_rol("validacion")
ROSA = gen.color_rol("prueba")
CREMA = gen.color_rol("realidad")
GRIS = mezclar(SUAVE, 0.55)
ANCHO_IN = 5.4


# ------------------------------------------------------------ utilidades ---

_ESTILO = re.compile(r'style="([^"]*)"')


def _sin_opacidad(texto_svg, fondo=PANEL):
    """Hornea cada fill/stroke translucido contra el panel y quita la opacidad."""
    def cambiar(m):
        decl = [d.strip() for d in m.group(1).split(";") if d.strip()]
        props = {k.strip(): v.strip() for k, v in (d.split(":", 1) for d in decl)}
        general = float(props.pop("opacity", 1))
        relleno = float(props.pop("fill-opacity", 1)) * general
        trazo = float(props.pop("stroke-opacity", 1)) * general
        for clave, alfa in (("fill", relleno), ("stroke", trazo)):
            valor = props.get(clave, "")
            if alfa < 1 and valor.startswith("#") and len(valor) == 7:
                props[clave] = mezclar(valor, alfa, fondo)
        return 'style="' + "; ".join(f"{k}: {v}" for k, v in props.items()) + '"'

    return _ESTILO.sub(cambiar, texto_svg)


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return matplotlib, plt


_SUPER = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _potencia(v, _pos=None):
    if v <= 0:
        return ""
    k = math.log10(v)
    if abs(k - round(k)) > 1e-9:
        return ""
    return "10" + str(int(round(k))).translate(_SUPER)


def _grafica(dibujar, aria, titulo, alto_in, filas=1, columnas=1, **subplots):
    """Arma una figura de datos con la paleta del sitio y la deja como SVG."""
    matplotlib, plt = _plt()
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(gen.RC_SITIO)
        matplotlib.rcParams.update({"font.size": 9, "axes.titlesize": 9.5,
                                    "axes.labelsize": 9, "xtick.labelsize": 8.5,
                                    "ytick.labelsize": 8.5, "legend.fontsize": 8.5})
        fig, ejes = plt.subplots(filas, columnas, figsize=(ANCHO_IN, alto_in), **subplots)
        dibujar(fig, ejes)
        from matplotlib.text import Text
        from matplotlib.ticker import FuncFormatter, NullFormatter
        for ax in fig.axes:
            for eje in (ax.xaxis, ax.yaxis):
                if eje.get_scale() == "log":
                    eje.set_major_formatter(FuncFormatter(_potencia))
                    eje.set_minor_formatter(NullFormatter())
        for t in fig.findobj(Text):
            if t.get_fontsize() < 8:
                t.set_fontsize(8)
        for ax in fig.axes:
            ley = ax.get_legend()
            if ley is not None:
                for t in ley.get_texts():
                    t.set_fontsize(8.5)
                    t.set_color(TEXTO)
                ley.get_frame().set_facecolor(PANEL)
                ley.get_frame().set_edgecolor(LINEA)
                ley.get_frame().set_alpha(1.0)
                ley.get_title().set_color(TEXTO)
        fig.tight_layout()
        crudo = gen.svg_de_matplotlib(fig, aria, titulo=titulo, ancho=600)
        plt.close("all")
    return _sin_opacidad(crudo)


def _cif():
    import ml_cifras_c4 as cif
    return cif


def _num(v, d=2):
    return f"{v:.{d}f}".replace("-", "−")


def _titulo(ax, s, tam=9.5):
    ax.set_title(s, color=TEXTO, fontsize=tam)


def _np():
    import numpy as np
    return np


# =========================================================== diagramas ===

# ------------------------------------------------- ml-c4-moda-99 (a mano) ---
MODA_W, MODA_H = 600, 430


def ml_c4_moda_99():
    m = _cif().cifras_c4_moda()["cita"]["uno"]
    c = [texto(16, 30, "Cien mensajes; la regla dice siempre «legítimo»", tam=17,
               peso="700", anclaje="start"),
         texto(16, 52, "uno solo es fraude, y la regla lo pinta de gris como a los demás",
               tam=13, color=SUAVE, anclaje="start")]
    lado, gap, x0, y0 = 24, 4, 160, 70
    for i in range(100):
        f, k = divmod(i, 10)
        x, y = x0 + k * (lado + gap), y0 + f * (lado + gap)
        if i == 57:
            c.append(caja(x, y, lado, lado, relleno=GRIS, borde=ROSA, radio=4, grosor=3))
        else:
            c.append(caja(x, y, lado, lado, relleno=GRIS, borde=GRIS, radio=4, grosor=1))
    c.append(texto(16, 120, "gris: la regla", tam=13, color=SUAVE, anclaje="start"))
    c.append(texto(16, 138, "dijo «legítimo»", tam=13, color=SUAVE, anclaje="start"))
    c.append(texto(16, 176, "borde rosa:", tam=13, color=ROSA, anclaje="start"))
    c.append(texto(16, 194, "el único fraude", tam=13, color=ROSA, anclaje="start"))
    yb = y0 + 10 * (lado + gap) + 22
    c.append(caja(16, yb - 4, 568, 50, relleno=PANEL, borde=LINEA, radio=8))
    c.append(texto(96, yb + 27, ["aciertos ", ("A", {"estilo": "italic"}), f" = {m['aciertos']}"],
                   tam=15, peso="700"))
    c.append(texto(316, yb + 27, "aciertos balanceados = " + m["aciertos_balanceados"], tam=15,
                   peso="700"))
    c.append(texto(520, yb + 27, "MCC = " + m["mcc"], tam=15, peso="700", color=ACENTO))
    aria = (f"Cien mensajes; la regla que siempre dice legítimo acierta 99 y no detecta el único "
            f"fraude: aciertos {m['aciertos']}, aciertos balanceados {m['aciertos_balanceados']}, "
            f"MCC {m['mcc']}")
    return svg(MODA_W, MODA_H, aria, "Cien mensajes y una regla que nunca detecta nada", c)


# ---------------------------------------------- ml-c4-cadena-decision ---
CAD_W, CAD_H = 600, 330


def ml_c4_cadena_decision():
    c = [texto(16, 30, "Del dato a la etiqueta: tres decisiones", tam=17, peso="700",
               anclaje="start")]
    nodos = [("x", "el mensaje"), ("φ(x)", "sus columnas"), ("z", "el puntaje"),
             ("p̂", "probabilidad"), ("ŷ", "la etiqueta")]
    w, h, y = 92, 60, 150
    xs = [16 + i * 118 for i in range(5)]
    for (s, sub), x in zip(nodos, xs):
        borde = ACENTO if s in ("p̂", "ŷ") else LINEA
        c.append(caja(x, y, w, h, relleno=PANEL, borde=borde, radio=8))
        c.append(texto(x + w / 2, y + 28, s, tam=18, peso="700", estilo="italic"))
        c.append(texto(x + w / 2, y + 48, sub, tam=12, color=SUAVE))
    for a, b in zip(xs[:-1], xs[1:]):
        c.append(flecha(a + w + 2, y + h / 2, b - 4, y + h / 2, color=SUAVE))
    # τ: perilla entre p̂ y ŷ
    xm = (xs[3] + w + xs[4]) / 2
    c.append(caja(xm - 22, y + h + 22, 44, 32, relleno=FONDO, borde=ORO, radio=16))
    c.append(texto(xm, y + h + 44, "τ", tam=17, peso="700", color=ORO, estilo="italic"))
    c.append(linea(xm, y + h + 22, xm, y + h / 2 + 6, color=ORO, grosor=2, guiones="4 3"))
    c.append(texto(xm, y + h + 76, "el umbral: una perilla aparte,", tam=12, color=ORO))
    c.append(texto(xm, y + h + 92, "se elige en validación", tam=12, color=ORO))
    # pérdida sobre p̂, métrica sobre ŷ
    xp = xs[3] + w / 2
    c.append(caja(xp - 56, 58, 112, 50, relleno=FONDO, borde=CIAN, radio=8))
    c.append(texto(xp, 80, "la pérdida", tam=14, peso="700", color=CIAN))
    c.append(texto(xp, 98, "entrenar", tam=12, color=SUAVE))
    c.append(linea(xp, 108, xp, y - 2, color=CIAN, grosor=2))
    xe = xs[4] + w / 2
    c.append(caja(xe - 52, 58, 104, 50, relleno=FONDO, borde=ACENTO, radio=8))
    c.append(texto(xe, 80, "la métrica", tam=14, peso="700", color=ACENTO))
    c.append(texto(xe, 98, "juzgar", tam=12, color=SUAVE))
    c.append(linea(xe, 108, xe, y - 2, color=ACENTO, grosor=2))
    c.append(texto(16, 312, "Tres objetos que el uso diario llama «predicción».", tam=13,
                   color=SUAVE, anclaje="start"))
    aria = ("Del dato a la etiqueta: x, sus columnas phi de x, el puntaje z, la probabilidad "
            "p gorro y la etiqueta y gorro. La pérdida se mide en la probabilidad, la métrica en "
            "la etiqueta y el umbral tau es una perilla aparte que se elige en validación")
    return svg(CAD_W, CAD_H, aria, "Del dato a la etiqueta: tres decisiones", c)


# ---------------------------------------------------- ml-c4-softmax ---
SM_W, SM_H = 600, 360


def ml_c4_softmax():
    c = [texto(16, 30, "Regresión softmax con tres clases", tam=17, peso="700", anclaje="start"),
         texto(16, 52, "cada clase y tiene su intercepto y sus coeficientes", tam=13,
               color=SUAVE, anclaje="start")]
    ent = [("1", "intercepto"), ("x₁", ""), ("x₂", ""), ("⋮", "")]
    ye = [96, 156, 216, 276]
    for (s, sub), yy in zip(ent, ye):
        c.append(caja(20, yy - 22, 70, 40, relleno=PANEL, borde=LINEA, radio=8))
        c.append(texto(55, yy + 4, s, tam=16, peso="700"))
    c.append(texto(16, 322, "las entradas de φ(x)", tam=12, color=SUAVE, anclaje="start"))
    ys = [116, 186, 256]
    for k, yy in enumerate(ys):
        c.append(caja(220, yy - 24, 120, 44, relleno=PANEL, borde=CIAN, radio=8))
        c.append(texto(280, yy + 4, [("z", {"estilo": "italic"}), f"ᵢ,{k}"], tam=16, peso="700"))
        for ya in ye:
            c.append(linea(92, ya, 218, yy, color=mezclar(SUAVE, 0.5), grosor=1.2))
    c.append(texto(280, 300, "puntajes lineales:", tam=12, color=SUAVE))
    c.append(texto(280, 316, "β₀,ᵧ + βᵧᵀφ(x)", tam=12, color=SUAVE))
    c.append(caja(380, 92, 80, 188, relleno=FONDO, borde=ACENTO, radio=10))
    c.append(texto(420, 190, "softmax", tam=14, peso="700", color=ACENTO))
    for yy in ys:
        c.append(flecha(342, yy, 376, yy, color=SUAVE))
        c.append(flecha(462, yy, 494, yy, color=ACENTO))
    for k, yy in enumerate(ys):
        c.append(caja(498, yy - 22, 84, 40, relleno=PANEL, borde=ORO, radio=8))
        c.append(texto(540, yy + 4, [("p", {"estilo": "italic"}), f"ᵢ,{k}"], tam=16, peso="700"))
    c.append(texto(540, 300, "suman 1", tam=12, color=ORO))
    c.append(texto(16, 350, "Es una red de una sola capa; la unidad de redes la retoma.", tam=12,
                   color=SUAVE, anclaje="start"))
    aria = ("Regresión softmax: cada clase tiene su puntaje lineal en las entradas de phi de x "
            "y softmax los convierte en tres probabilidades que suman uno")
    return svg(SM_W, SM_H, aria, "Regresión softmax con tres clases", c)


# ------------------------------------------------ ml-c4-mapa-reservas ---
MR_W, MR_H = 600, 505
# (pieza, ancho relativo, color, qué ajusta o decide, renglón 2)
PIEZAS_MAPA = (
    ("ent", 0.5, CIAN, "β₀, β y la φ estandarizada;", "μ y los pesos por CV dentro de ent"),
    ("val_a", 0.1, ORO, "la recalibración", "y el umbral τ"),
    ("val_b", 0.1, ORO, "benchmark, diagnóstico", "y elección de lo que queda"),
    ("cal", 0.1, VERDE, "solo el corte conformal ĉ:", "no elige ni diagnostica nada"),
    ("prueba", 0.2, ROSA, "se abre una vez:", "las cifras finales"),
)


def piezas_mapa_reservas():
    """Los rótulos de las cinco piezas, en orden (la prueba los lee de aquí)."""
    return [p[0] for p in PIEZAS_MAPA]


def ml_c4_mapa_reservas():
    c = [texto(16, 30, "Qué conjunto ajusta cada pieza", tam=17, peso="700", anclaje="start"),
         texto(16, 52, "cada cosa que se ajusta necesita datos que no tocó otra", tam=13,
               color=SUAVE, anclaje="start")]
    x, y, ancho = 16, 92, 568
    xs = []
    for nombre, frac, color, _, _ in PIEZAS_MAPA:
        w = ancho * frac
        c.append(caja(x, y, w - 3, 40, relleno=mezclar(color, 0.35), borde=color, radio=6))
        c.append(texto(x + (w - 3) / 2, y + 26, nombre, tam=13, peso="700", fuente=gen.MONO))
        xs.append((x, w))
        x += w
    # marca «se aparta primero» sobre cal
    xc, wc = xs[3]
    c.append(texto(xc + wc / 2 - 1, 80, "se aparta primero", tam=12, color=VERDE, peso="700"))
    c.append(texto(xs[1][0] + (xs[1][1] * 3) / 2, 154, "la validación, partida en tres", tam=12,
                   color=SUAVE))
    yy = 184
    for (nombre, _, color, r1, r2), (xx, w) in zip(PIEZAS_MAPA, xs):
        c.append(caja(16, yy, 568, 44, relleno=PANEL, borde=color, radio=6))
        c.append(texto(28, yy + 27, nombre, tam=13, peso="700", color=color, anclaje="start",
                       fuente=gen.MONO))
        c.append(texto(110, yy + 19, r1, tam=13, anclaje="start"))
        c.append(texto(110, yy + 36, r2, tam=13, anclaje="start", color=SUAVE))
        yy += 50
    c.append(texto(16, yy + 14, "cal, resto = ml.partir(datos.val, 1/3, como=C, semilla=S)",
                   tam=12, anclaje="start", fuente=gen.MONO, color=VERDE))
    c.append(texto(16, yy + 32, "val_a, val_b = ml.partir(resto, 0.5, como=C, semilla=S + 1)",
                   tam=12, anclaje="start", fuente=gen.MONO, color=ORO))
    aria = ("Qué conjunto ajusta cada pieza: ent ajusta el modelo, mu y los pesos; val_a la "
            "recalibración y el umbral; val_b el diagnóstico y la elección; cal solo el corte "
            "conformal, y se aparta primero; la prueba, la evaluación final, una vez. Al azar, "
            "garantía marginal; estratificada, por clase")
    desc = aria
    cuerpo = c + [texto(16, MR_H - 12, "al azar: garantía marginal · estratificada: por clase",
                        tam=12, color=SUAVE, anclaje="start")]
    return svg(MR_W, MR_H, aria, "Qué conjunto ajusta cada pieza", cuerpo, desc=desc)


# --------------------------------------------- ml-c4-conformal-rangos ---
CR_W, CR_H = 600, 330


def ml_c4_conformal_rangos():
    k = _cif().cifras_c4_cinco_puntajes()
    cal = _cif().C_CINCO
    nuevo = k["puntajes_nuevo"]
    corte = k["tercio"]["corte"]
    c = [texto(16, 30, "Cinco puntajes y un corte", tam=17, peso="700", anclaje="start"),
         texto(16, 52, "δ = 1/3: el ⌈(5 + 1)(1 − δ)⌉ = 4.º menor es el corte", tam=13,
               color=SUAVE, anclaje="start")]
    x0, x1 = 50, 560

    def X(v):
        return x0 + (x1 - x0) * v
    y = 130
    c.append(linea(x0, y, x1, y, color=SUAVE, grosor=2))
    for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        c.append(linea(X(v), y - 5, X(v), y + 5, color=SUAVE, grosor=1.5))
        c.append(texto(X(v), y + 24, f"{v:g}", tam=12, color=SUAVE))
    for i, v in enumerate(cal, 1):
        col = ACENTO if math.isclose(v, corte) else CIAN
        c.append(f'<circle cx="{X(v):.1f}" cy="{y}" r="8" fill="{col}"/>')
        c.append(texto(X(v), y - 16, f"{i}.º", tam=12, color=col))
    c.append(linea(X(corte), 140, X(corte), 242, color=ACENTO, grosor=2, guiones="6 4"))
    c.append(texto(X(corte) + 6, 84, "ĉ = 0.6", tam=14, peso="700", color=ACENTO, anclaje="start"))
    c.append(texto(16, 190, "mensaje nuevo, sus tres puntajes 1 − p̂ᵧ:", tam=13, anclaje="start"))
    yn = 230
    c.append(linea(x0, yn, x1, yn, color=SUAVE, grosor=1))
    for clase, v in enumerate(nuevo):
        dentro = v <= corte + 1e-12
        col = VERDE if dentro else GRIS
        c.append(f'<rect x="{X(v) - 7:.1f}" y="{yn - 7}" width="14" height="14" fill="{col}"/>')
        c.append(texto(X(v), yn + 28, f"clase {clase}", tam=12, color=col))
        c.append(texto(X(v), yn + 44, f"{v:g}", tam=12, color=col))
    c.append(texto(16, 312, "Solo la clase 0 queda a la izquierda del corte: C(x) = {0}.", tam=13,
                   anclaje="start", color=VERDE))
    aria = ("Cinco puntajes de calibración, 0.1, 0.2, 0.4, 0.6 y 0.8, el cuarto menor como corte "
            "0.6, y los tres puntajes de un mensaje nuevo, 0.55, 0.65 y 0.8: solo una clase entra")
    return svg(CR_W, CR_H, aria, "Cinco puntajes y un corte", c)


# ------------------------------------------------------------ ml-c4-tasa ---
TA_W, TA_H = 600, 380


def ml_c4_tasa():
    t = _cif().cifras_c4_tasa()
    c = [texto(16, 30, "Una probabilidad que se usa como precio", tam=17, peso="700",
               anclaje="start"),
         texto(16, 52, "tasa de equilibrio = p̂ / (1 − p̂): prestar 1 y cobrar 1 + tasa si paga",
               tam=13, color=SUAVE, anclaje="start")]
    x0, x1, y0, y1 = 80, 570, 320, 80
    pmax, tmax = 0.6, 1.5

    def X(p):
        return x0 + (x1 - x0) * p / pmax

    def Y(v):
        return y0 - (y0 - y1) * v / tmax
    c.append(linea(x0, y0, x1, y0, color=SUAVE, grosor=1.5))
    c.append(linea(x0, y0, x0, y1, color=SUAVE, grosor=1.5))
    for p in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        c.append(texto(X(p), y0 + 20, f"{p:g}", tam=12, color=SUAVE))
    for v in (0, 0.5, 1.0, 1.5):
        c.append(texto(x0 - 8, Y(v) + 4, f"{int(v * 100)} %", tam=12, color=SUAVE, anclaje="end"))
        c.append(linea(x0, Y(v), x1, Y(v), color=gen.REJILLA, grosor=0.8))
    pts = []
    for i in range(121):
        p = pmax * i / 120
        pts.append(f"{X(p):.1f},{Y(p / (1 - p)):.1f}")
    c.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CIAN}" stroke-width="2.5"/>')
    c.append(texto(X(0.3), y0 + 44, "probabilidad anunciada p̂", tam=13))
    for p, tv, col, rot in ((t["p_sin"], t["sin"], VERDE, f"sin pesos: p̂ = 0.05, tasa {t['cita']['sin']}"),
                            (t["p_con"], t["con"], ACENTO, "con pesos: p̂ = 0.5, tasa 100 %")):
        c.append(f'<circle cx="{X(p):.1f}" cy="{Y(tv):.1f}" r="7" fill="{col}"/>')
        c.append(texto(X(p) + (12 if p < 0.3 else -12), Y(tv) - (90 if p < 0.3 else 12), rot, tam=13, peso="700",
                       color=col, anclaje="start" if p < 0.3 else "end"))
    aria = (f"La tasa de interés de equilibrio crece con la probabilidad anunciada; el cliente "
            f"típico sin pesos recibe 0.05 y pagaría {t['cita']['sin']}; con pesos recibe 0.5 y "
            "pagaría cien por ciento")
    return svg(TA_W, TA_H, aria, "Una probabilidad que se usa como precio", c)


# ====================================================== gráficas de datos ===

# --------------------------------------------------- ml-c4-separable ---

def ml_c4_separable():
    cif = _cif()
    ml = gen.ml_lab()
    s = cif.cifras_c4_separable()
    ajustes = {"separable": cif.ajustes_separable(False), "con ruido": cif.ajustes_separable(True)}
    datos = {"separable": cif.datos_separable(False), "con ruido": cif.datos_separable(True)}

    def dibujar(fig, ejes):
        ml.dibujar_separable(ajustes, mu=list(cif.MUS_FIGURA_SEPARABLE), datos=datos,
                             ax=list(ejes), tema="sitio")
        ejes[1].set_ylabel("‖β̂‖₂ (variables estandarizadas)")
        ejes[1].set_xlabel("log₁₀ μ")
        ley = ejes[0].get_legend()
        if ley is not None:
            for t in ley.get_texts():
                t.set_text(t.get_text().replace("1e-05", "10⁻⁵"))

    aria = ("Con datos separables la norma de los coeficientes crece sin tope al bajar mu, "
            f"despacio y lo mismo por cada década: unas {s['cita']['por_decada']} unidades por "
            "década; con ruido se aplana. A la izquierda, tres curvas p gorro de x para mu 1, "
            "0.01 y 0.00001, la última casi un escalón")
    return _grafica(dibujar, aria, "Sin penalización, los coeficientes no se detienen", 5.6, filas=2)


# ------------------------------------------ ml-c4-perdida-vs-metrica ---

def ml_c4_perdida_vs_metrica():
    cif = _cif()
    ml = gen.ml_lab()
    np = _np()
    datos = cif.datos_perfil()

    def dibujar(fig, ax):
        tabla = ml.perfil_en_beta(datos.ent, "x1", np.linspace(-1, 4, 201))
        ml.dibujar_perfil_en_beta(tabla, ax=ax, tema="sitio")
        ax.set_xlabel("pendiente β₁ (β₀ reoptimizado en cada punto)")

    aria = ("La pérdida logarítmica cambia suave con la pendiente; aciertos y MCC cambian a "
            "saltos: la pérdida tiene pendiente en todas partes y las métricas son planas a trozos")
    return _grafica(dibujar, aria, "La pérdida cambia suave; las métricas, a saltos", 3.4)


# ---------------------------------------------------- ml-c4-umbral ---

def ml_c4_umbral():
    cif = _cif()
    ml = gen.ml_lab()
    datos, m, _ = cif.modelo_umbral()
    u = cif.cifras_c4_umbral()

    def dibujar(fig, ejes):
        ml.dibujar_umbral(m, datos.val, tau=0.5, tau_elegido=u["tau"], ax=list(ejes), tema="sitio")

    aria = (f"Mover el umbral cambia MCC y aciertos y no cambia la pérdida. En validación, el "
            f"umbral que elige MCC es {u['cita']['tau']}; el MCC en validación pasa de "
            f"{u['cita']['mcc_val_05']} con 0.5 a {u['cita']['mcc_val_elegido']}")
    return _grafica(dibujar, aria, "Mover el umbral no toca la pérdida", 5.4, filas=2)


# ------------------------------------------ ml-c4-contribucion-clases ---

def ml_c4_contribucion_clases():
    cif = _cif()
    ml = gen.ml_lab()
    np = _np()
    t = cif.cifras_c4_contribucion()["tablas"]

    def dibujar(fig, ejes):
        filas = [("50 %, sin pesos", t[(0.5, None)]), ("1 %, sin pesos", t[(0.01, None)]),
                 ("1 %, con pesos", t[(0.01, "balanceado")])]
        for ax, col, tit in ((ejes[0], "fraccion_casos", "fracción de casos"),
                             (ejes[1], "fraccion_peso", "fracción del peso total")):
            ml.dibujar_contribucion_por_clase({n: tb[col] for n, tb in filas}, ax=ax, tema="sitio")
            _titulo(ax, tit)
            ax.set_ylabel("fracción")
            ley = ax.get_legend()
            if ley is not None:
                for tx in ley.get_texts():
                    tx.set_text({"clase 0": "legítimo", "clase 1": "fraude"}.get(tx.get_text(), tx.get_text()))
        ax = ejes[2]
        nombres = [n for n, _ in filas[:2]]
        x = np.arange(2)
        for j, (clase, color, etiqueta) in enumerate(((0, GRIS, "legítimo"), (1, ROSA, "fraude"))):
            v = [cif._col(tb, clase, "perdida_media") for _, tb in filas[:2]]
            ax.bar(x + (j - 0.5) * 0.36, v, 0.34, color=color, label=etiqueta)
            for xi, vi in zip(x, v):
                ax.text(xi + (j - 0.5) * 0.36, vi + 0.05, _num(vi, 2), ha="center", color=TEXTO,
                        fontsize=8.5)
        ax.set_xticks(x, nombres)
        ax.set_ylabel("pérdida media por caso")
        _titulo(ax, "pérdida media dentro de cada clase (modelo sin pesos)")
        ax.legend(loc="upper left")

    aria = ("Con uno por ciento de fraudes, su parte de los casos y del peso total casi "
            "desaparece, aunque cada fraude pierde mucho; con pesos balanceados cada clase tiene "
            "la mitad del peso")
    return _grafica(dibujar, aria, "Cuántos votos tiene cada clase en el ajuste", 7.4, filas=3)


# --------------------------------------- ml-c4-metricas-vs-proporcion ---

def ml_c4_metricas_vs_proporcion():
    cif = _cif()
    ml = gen.ml_lab()
    tabla = cif.tabla_desbalanceo()
    d = cif.cifras_c4_desbalanceo()

    n = len(set(tabla["metrica"]))

    def dibujar(fig, ejes):
        ml.dibujar_metricas_vs_proporcion(tabla, ax=list(ejes[:n]), tema="sitio")
        manijas, rotulos = ejes[0].get_legend_handles_labels()
        for ax in ejes[:n]:
            if ax.get_legend() is not None:
                ax.get_legend().remove()
            ax.set_xlabel("")
        for ax in ejes[:n]:              # A_bal y aciertos no pasan de 1: la banda ±2 desv
            if ax.get_ylim()[1] > 1.0:   # se corta en la cota, no se dibuja arriba de ella
                ax.set_ylim(top=1.02)
        ejes[n - 1].set_xlabel("proporción de fraude Pr(y = 1), escala log")
        ejes[n].axis("off")
        ejes[n].legend(manijas, rotulos, loc="center", ncol=2,
                       title="puntos: despliegue ±2 EE de la media; banda: ±2 desv. entre validaciones",
                       title_fontsize=8.5)

    aria = ("Al volverse rara la clase, la moda gana en aciertos y sigue en cero de MCC; con "
            "pesos, MCC y aciertos balanceados suben y los aciertos bajan; medido en una "
            f"validación chica, el MCC baila mucho: banda de ancho {d['cita']['banda_01']} con uno "
            "por ciento de fraude")
    return _grafica(dibujar, aria, "Aciertos, aciertos balanceados y MCC contra la proporción de fraude",
                    8.6, filas=n + 1, gridspec_kw={"height_ratios": [1] * n + [0.42]})


# ------------------------------------------------- ml-c4-pesos-umbral ---

def ml_c4_pesos_umbral():
    """Dibujada aquí con la tabla de ml.efecto_de_pesos: dibujar_efecto_de_pesos de ml_lab 1.5
    encima su recuadro interior sobre el panel central a 600 px (SOLICITUD prog-c4-1)."""
    cif = _cif()
    ml = gen.ml_lab()
    np = _np()
    p = cif.cifras_c4_pesos_intercepto()
    t = cif.tabla_pesos().sort_values("razon")
    t = t[~t["razon"].duplicated()]
    datos = cif.datos_pesos()
    base = t.loc[np.isclose(t["razon"], 1.0), "beta0"].iloc[0]

    def dibujar(fig, ejes):
        ax = ejes[0]
        sub = datos.ent.iloc[:700]
        for k, col, mk, rot in ((0, GRIS, "o", "legítimo"), (1, ROSA, "^", "fraude")):
            s = sub[sub["y"] == k]
            ax.scatter(s["x1"], s["x2"], s=8 if k == 0 else 20, color=col, marker=mk,
                       edgecolors="none", label=rot)
        con = ml.ajustar(datos, pesos={0: 1.0, 1: 19.0})
        sin = ml.ajustar(datos)
        g = np.linspace(-3, 3, 50)
        for m, tau, col, ls, rot in ((con, 0.5, CIAN, "-", "con pesos (razón 19), τ = 0.5"),
                                     (sin, 1 / 20, ACENTO, "--", "sin pesos, τ = 1/20")):
            b = m.beta_gorro
            b0 = float(b["1"]) - math.log(tau / (1 - tau))
            ax.plot(g, -(b0 + float(b["x1"]) * g) / float(b["x2"]), color=col, ls=ls, lw=2, label=rot)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_xlabel("x₁ (enlaces)")
        ax.set_ylabel("x₂ (urgencia)")
        _titulo(ax, "las dos fronteras casi se enciman", 9)
        ax.legend(loc="lower left", fontsize=8)
        ax = ejes[1]
        ax.plot(t["ln_razon"], t["beta0"] - base, marker="o", ms=4, color=CIAN,
                label="cambio del intercepto ajustado")
        ax.plot(t["ln_razon"], t["ln_razon"], color=CREMA, ls="--", lw=1.5, label="ln(w₁/w₀)")
        ax.set_xlabel("ln(w₁/w₀)")
        ax.set_ylabel("cambio de β̂₀")
        ax.legend(loc="upper left")
        _titulo(ax, "el intercepto sigue a ln(w₁/w₀)", 9)
        ax = ejes[2]
        ax.plot(t["razon"], t["mcc_tau05"], color=ROSA, lw=2, label="MCC")
        ax.plot(t["razon"], t["aciertos_balanceados_tau05"], color=CIAN, lw=2, ls="--",
                label="aciertos balanceados")
        ax.plot(t["razon"], t["aciertos_tau05"], color=ORO, lw=2, ls="-.", label="aciertos")
        ax.plot(t["razon"], t["p_promedio"], color=VERDE, lw=2, ls=":", label="p̂ promedio")
        ax.axhline(float(t["prob_real"].iloc[0]), color=CREMA, lw=1, ls="--", label="Pr(y = 1)")
        ax.set_xscale("log")
        ax.set_ylim(0, 1.32)
        ax.set_xlabel("razón w₁/w₀")
        ax.set_ylabel("en el despliegue, τ = 0.5")
        _titulo(ax, "cada métrica tiene su mejor razón; p̂ promedio se despega", 9)
        ax.legend(loc="upper center", fontsize=8, ncol=3)

    aria = ("Pesar la clase rara mueve el intercepto en el logaritmo de la razón de pesos, como "
            f"mover el umbral: con razón 19 el intercepto sube {p['cita']['salto']} contra "
            f"ln 19 = {p['cita']['ln_razon']}, y las etiquetas coinciden en "
            f"{p['cita']['coincidencia']} por ciento con las del umbral equivalente")
    return _grafica(dibujar, aria, "Pesar es mover el intercepto", 9.0, filas=3)


# ------------------------------------------------ ml-c4-anillos-metricas ---

def ml_c4_anillos_metricas():
    cif = _cif()
    ml = gen.ml_lab()
    datos, mods = cif.modelos_anillos()
    a = cif.cifras_c4_anillos()["cita"]
    paneles = (("lineal", "φ lineal, sin pesos"), ("lineal_pesos", "φ lineal, con pesos"),
               ("cuadratica_pesos", "φ cuadrática, con pesos"))

    def dibujar(fig, ejes):
        ejes = list(ejes.ravel())
        for ax, (k, t) in zip(ejes, paneles):
            ml.dibujar_frontera(mods[k], datos.ent, ax=ax, tema="sitio")
            np = _np()
            import pandas as pd
            g = np.linspace(-3, 3, 121)
            U, V = np.meshgrid(g, g)
            P = mods[k].predecir_p(pd.DataFrame({"x1": U.ravel(), "x2": V.ravel()})).reshape(U.shape)
            if P.min() < 0.5 < P.max():
                ax.contour(U, V, P, levels=[0.5], colors=[ACENTO], linewidths=2.5, zorder=5)
            _titulo(ax, f"{t}\nMCC en el despliegue = {a[k]}", 9)
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_xlabel("x₁")
            ax.set_ylabel("x₂")
        manijas, rotulos = ejes[0].get_legend_handles_labels()
        for ax in ejes[:3]:
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        ejes[3].axis("off")
        ejes[3].legend(manijas, rotulos, loc="center")
        ejes[3].text(0.5, 0.12, f"la regla óptima para aciertos:\nMCC = {a['regla_aciertos']}",
                     ha="center", color=SUAVE, fontsize=8.5, transform=ejes[3].transAxes)

    aria = ("Los pesos no separan una clase que vive en el centro; una representación cuadrática "
            f"sí, y sigue siendo lineal en los parámetros. MCC en el despliegue: {a['lineal']}, "
            f"{a['lineal_pesos']} y {a['cuadratica_pesos']}")
    return _grafica(dibujar, aria, "Los pesos no cambian la forma de la frontera; la representación sí",
                    5.6, filas=2, columnas=2)


# ------------------------------------------------ ml-c4-mcc-por-pliegue ---

def tabla_metrica_por_pliegue():
    """La tabla larga (k, pliegue, metrica, valor, raros) de cifras_c4_mcc_por_pliegue."""
    import pandas as pd
    cif = _cif()
    np = _np()
    df = cif.datos_pliegue().ent
    y = df["y"].to_numpy()
    filas = []
    for k, (cv_m, cv_a) in cif.tablas_mcc_por_pliegue().items():
        for i, (vm, va, (_, idx_val)) in enumerate(zip(cv_m.por_pliegue_estadistico,
                                                        cv_a.por_pliegue_estadistico,
                                                        cv_m.pliegues), 1):
            raros = int(np.sum(y[np.asarray(idx_val)] == 1))
            filas.append({"k": k, "pliegue": i, "metrica": "mcc", "valor": float(vm), "raros": raros})
            filas.append({"k": k, "pliegue": i, "metrica": "aciertos_balanceados", "valor": float(va),
                          "raros": raros})
    return pd.DataFrame(filas)


def ml_c4_mcc_por_pliegue():
    cif = _cif()
    ml = gen.ml_lab()
    m = cif.cifras_c4_mcc_por_pliegue()
    tabla = tabla_metrica_por_pliegue()

    def dibujar(fig, ax):
        ml.dibujar_metrica_por_pliegue(tabla, ax=ax, tema="sitio")
        ax.axhline(m["despliegue"]["mcc"], color=CREMA, ls="--", lw=1.5,
                   label=f"MCC en el despliegue = {m['cita']['mcc_despliegue']}")
        ax.legend(loc="upper left")

    aria = (f"Con pocos fraudes por pliegue, el MCC de cada pliegue salta mucho: {m['cita']['fraudes_ent']} "
            f"fraudes en entrenamiento; con diez pliegues hay uno o dos fraudes en cada uno, el MCC "
            f"va de {m['cita']['min_mcc_10']} a {m['cita']['max_mcc_10']} y la media apenas describe")
    return _grafica(dibujar, aria, "Una métrica por pliegue, con pocos fraudes", 4.2)


# -------------------------------------------- ml-c4-fronteras-tres-clases ---

def _regiones(ax, modelo, df, titulo):
    np = _np()
    import pandas as pd
    colores = [GRIS, ORO, ROSA]
    g = np.linspace(-3, 3, 161)
    U, V = np.meshgrid(g, g)
    malla = pd.DataFrame({"x1": U.ravel(), "x2": V.ravel()})
    Z = np.argmax(modelo.predecir_prob(malla), axis=1).reshape(U.shape)
    ax.contourf(U, V, Z, levels=[-0.5, 0.5, 1.5, 2.5],
                colors=[mezclar(c, 0.35, PANEL) for c in colores])
    sub = df.iloc[:600]
    marcas = ("o", "^", "s")
    for k, (col, mk) in enumerate(zip(colores, marcas)):
        s = sub[sub["y"] == k]
        ax.scatter(s["x1"], s["x2"], s=10 if k == 0 else 22, color=col, marker=mk,
                   edgecolors="none", label=("legítimo", "publicidad", "fraude")[k])
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("x₁ (enlaces)")
    ax.set_ylabel("x₂ (urgencia)")
    _titulo(ax, titulo, 9)


def ml_c4_fronteras_tres_clases():
    cif = _cif()
    datos, mods = cif.modelos_multiclase()
    m = cif.cifras_c4_multiclase()["cita"]

    def dibujar(fig, ejes):
        _regiones(ejes[0], mods["sin"], datos.val, f"sin pesos\nMCC en el despliegue = {m['sin']['mcc']}")
        _regiones(ejes[1], mods["con"], datos.val, f"con pesos\nMCC en el despliegue = {m['con']['mcc']}")
        ejes[1].legend(loc="lower right", markerscale=1.2)

    aria = ("Tres clases, 90, 8 y 2 por ciento. Sin pesos la región del fraude casi desaparece y "
            f"acierta {m['sin']['por_clase'][2]} de los fraudes; con pesos crece y acierta "
            f"{m['con']['por_clase'][2]}")
    return _grafica(dibujar, aria, "Tres clases, sin pesos y con pesos", 3.3, columnas=2)


# --------------------------------------------------- ml-c4-macro-ponderado ---

def ml_c4_macro_ponderado():
    cif = _cif()
    ml = gen.ml_lab()
    import pandas as pd
    n = cif.cifras_c4_noticias()
    serie = pd.Series(n["aciertos"], index=list(cif.CLASES_NOTICIAS))
    soporte = pd.Series(n["soporte"], index=list(cif.CLASES_NOTICIAS))

    def dibujar(fig, ax):
        ml.dibujar_promedios(serie, soporte, ax=ax, tema="sitio")
        ax.set_xlabel("aciertos dentro de cada clase")
        if ax.get_legend() is not None:
            ax.legend(loc="upper right")

    c = n["cita"]
    aria = ("Aciertos por clase en el ejemplo de noticias: Tecnología "
            f"{c['aciertos'][0]}, Salud {c['aciertos'][1]}, Deporte {c['aciertos'][2]}; el promedio "
            f"ponderado, {c['ponderado']}, sigue a la clase grande y el macro, {c['macro']}, no")
    return _grafica(dibujar, aria, "Macro contra ponderado en el ejemplo de noticias", 3.2)


# ------------------------------------------------- ml-c4-recuadro-confusion ---

def ml_c4_recuadro_confusion():
    cif = _cif()
    ml = gen.ml_lab()
    np = _np()
    datos, m, _ = cif.modelo_umbral()
    u = cif.cifras_c4_umbral()
    y = datos.val["y"].to_numpy()
    p = m.predecir_p(datos.val)

    def dibujar(fig, ejes):
        yg = (p >= u["tau"]).astype(int)
        ml.dibujar_confusion(ml.matriz_confusion(y, yg), ax=ejes[0], tema="sitio")
        _titulo(ejes[0], f"matriz de confusión (τ = {u['cita']['tau']})", 9)
        ml.dibujar_roc_pr(p, y, ax=list(ejes[1:]), tema="sitio")
        vp, fp = int(((yg == 1) & (y == 1)).sum()), int(((yg == 1) & (y == 0)).sum())
        tpr, fpr = vp / max(int((y == 1).sum()), 1), fp / max(int((y == 0).sum()), 1)
        prec = vp / max(vp + fp, 1)
        ejes[1].plot([fpr], [tpr], marker="o", ms=8, color=ORO, ls="none", label=f"τ = {u['cita']['tau']}")
        ejes[2].plot([tpr], [prec], marker="o", ms=8, color=ORO, ls="none", label=f"τ = {u['cita']['tau']}")
        for ax in ejes[1:]:
            ax.legend(loc="lower right" if ax is ejes[1] else "upper right")

    aria = ("Vocabulario clásico: matriz de confusión, curva ROC y curva PR del mismo modelo, "
            f"en validación, con el umbral {u['cita']['tau']}")
    return _grafica(dibujar, aria, "La matriz de confusión, la curva ROC y la curva PR", 7.0, filas=3)


# ---------------------------------------------------- ml-c4-confiabilidad ---

def ml_c4_confiabilidad():
    cif = _cif()
    ml = gen.ml_lab()
    datos, _, val_b = cif.datos_calibracion()
    mods = cif.modelos_calibracion()
    k = cif.cifras_c4_calibracion()["cita"]
    y = val_b["y"].to_numpy()

    def dibujar(fig, ax):
        tablas = {"sin pesos": ml.calibracion(mods["sin"].predecir_p(val_b), y, bins=10),
                  "con pesos balanceados": ml.calibracion(mods["con"].predecir_p(val_b), y, bins=10)}
        real = datos.realidad
        verdadera = ml.calibracion(real["prob"].to_numpy(), real["y"].to_numpy(), bins=10)
        ml.dibujar_calibracion(tablas, verdadera=verdadera, ax=ax, tema="sitio")
        ybar = float(datos.ent["y"].mean())
        ax.plot([ybar], [float(y.mean())], marker="D", ms=8, color=ACENTO, ls="none",
                label="benchmark: la proporción")
        ax.legend(loc="upper left")
        _titulo(ax, f"en val_b ({k['n_val_b']} casos): Brier sin pesos {k['brier_sin']}, "
                    f"con pesos {k['brier_con']}, benchmark {k['brier_benchmark']}", 8.5)

    aria = ("Con pesos la curva cae bajo la diagonal: el modelo anuncia más fraude del que ocurre. "
            f"Brier en val_b: sin pesos {k['brier_sin']}, con pesos {k['brier_con']}, benchmark "
            f"{k['brier_benchmark']}")
    return _grafica(dibujar, aria, "¿Ocurre lo que anuncia?", 4.6)


# ------------------------------------------------ ml-c4-conformal-conjuntos ---

DELTAS_CONFORMAL = tuple(round(0.01 * i, 2) for i in range(1, 31))


def ml_c4_conformal_conjuntos():
    cif = _cif()
    ml = gen.ml_lab()
    np = _np()
    import pandas as pd
    eq = cif.cifras_c4_conformal_equilibrado()
    datos3, cal3, _ = cif.datos_conformal(proporcion=(1 / 3, 1 / 3, 1 / 3))
    m = cif.modelo_conformal(proporcion=(1 / 3, 1 / 3, 1 / 3))
    cf = ml.conformal(m, cal3, cif.DELTA)

    def dibujar(fig, ejes):
        ax = ejes[0]
        g = np.linspace(-3, 3, 181)
        U, V = np.meshgrid(g, g)
        malla = pd.DataFrame({"x1": U.ravel(), "x2": V.ravel()})
        tam = np.array([len(s) for s in cf.predecir_conjunto(malla)]).reshape(U.shape)
        cols = [PANEL, mezclar(CIAN, 0.45, PANEL), mezclar(ORO, 0.55, PANEL), mezclar(ROSA, 0.7, PANEL)]
        ax.contourf(U, V, tam, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], colors=cols)
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=c, label=f"|C(x)| = {i}") for i, c in enumerate(cols) if i],
                  loc="lower right")
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        _titulo(ax, "tamaño de C(x) con δ = 0.1 (tres clases iguales)", 9)
        ax = ejes[1]
        ax.plot([0.68, 1], [0.68, 1], color=SUAVE, lw=1)
        ax.plot([1 - d for d in DELTAS_CONFORMAL], eq["cobertura"], ls="none", marker="o", ms=4,
                color=CREMA, label="cobertura en el despliegue")
        ax.plot([1 - d for d in DELTAS_CONFORMAL], eq["tamano"], ls="none", marker="s", ms=4,
                color=ORO, label="tamaño medio de C(x) / 3")
        ax.set_xlabel("1 − δ")
        _titulo(ax, "la cobertura medida sigue a 1 − δ", 9)
        ax.legend(loc="upper left")

    aria = ("Los conjuntos crecen donde las clases se mezclan; la cobertura medida sigue a uno "
            f"menos delta: con delta 0.1 cubre {eq['cita']['cobertura_01']} y el tamaño medio es "
            f"{eq['cita']['tamano_01']}")
    return _grafica(dibujar, aria, "Conjuntos que crecen donde hay duda", 6.8, filas=2)


# ------------------------------------------------ ml-c4-cobertura-por-clase ---

def ml_c4_cobertura_por_clase():
    cif = _cif()
    np = _np()
    r = cif.cifras_c4_conformal_repetido()

    def dibujar(fig, ax):
        x = np.arange(3)
        for j, (nombre, col, etiqueta) in enumerate((("marginal", GRIS, "marginal"),
                                                    ("por_clase", VERDE, "por clase"))):
            med, ee, tam = r[nombre]["media"], r[nombre]["ee"], r[nombre]["tamano"]
            xs = x + (j - 0.5) * 0.38
            ax.bar(xs, med, 0.36, color=col, label=etiqueta)
            ax.errorbar(xs, med, yerr=[2 * e for e in ee], fmt="none", ecolor=TEXTO, lw=1.2)
            for xi, mi, ti in zip(xs, med, tam):
                ax.text(xi, min(mi, 1) + 0.03, f"|C| {ti:.1f}", ha="center", color=TEXTO, fontsize=8.5)
        ax.axhline(0.9, color=CREMA, ls="--", lw=1.5, label="1 − δ = 0.9")
        ax.set_xticks(x, ["legítimo (90 %)", "publicidad (8 %)", "fraude (2 %)"])
        ax.set_ylim(0, 1.32)
        ax.set_ylabel("cobertura en el despliegue")
        _titulo(ax, f"promedio sobre {r['R']} calibraciones (±2 EE); arriba, tamaño medio de C(x)", 9)
        ax.legend(loc="upper center", ncol=3)

    aria = ("Con conformal marginal el fraude queda muy por debajo de 0.9: "
            f"{r['cita']['marginal_fraude']} en promedio sobre {r['R']} calibraciones; por clase, "
            f"todas llegan a cerca de 0.9 (el fraude, {r['cita']['por_clase_fraude']})")
    return _grafica(dibujar, aria, "La garantía marginal, clase por clase", 3.8)


FIGURAS_C4 = {
    "ml-c4-moda-99": ml_c4_moda_99,
    "ml-c4-separable": ml_c4_separable,
    "ml-c4-cadena-decision": ml_c4_cadena_decision,
    "ml-c4-perdida-vs-metrica": ml_c4_perdida_vs_metrica,
    "ml-c4-umbral": ml_c4_umbral,
    "ml-c4-contribucion-clases": ml_c4_contribucion_clases,
    "ml-c4-metricas-vs-proporcion": ml_c4_metricas_vs_proporcion,
    "ml-c4-pesos-umbral": ml_c4_pesos_umbral,
    "ml-c4-anillos-metricas": ml_c4_anillos_metricas,
    "ml-c4-mcc-por-pliegue": ml_c4_mcc_por_pliegue,
    "ml-c4-softmax": ml_c4_softmax,
    "ml-c4-fronteras-tres-clases": ml_c4_fronteras_tres_clases,
    "ml-c4-macro-ponderado": ml_c4_macro_ponderado,
    "ml-c4-recuadro-confusion": ml_c4_recuadro_confusion,
    "ml-c4-confiabilidad": ml_c4_confiabilidad,
    "ml-c4-tasa": ml_c4_tasa,
    "ml-c4-mapa-reservas": ml_c4_mapa_reservas,
    "ml-c4-conformal-rangos": ml_c4_conformal_rangos,
    "ml-c4-conformal-conjuntos": ml_c4_conformal_conjuntos,
    "ml-c4-cobertura-por-clase": ml_c4_cobertura_por_clase,
}
