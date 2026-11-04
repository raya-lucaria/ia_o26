"""Figuras de la clase 1 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C1: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c1-", es un error.

Dueno: prog-c1 (lo creo vacio prog-lab en U.T3). Reglas para llenarlo:
- los diagramas conceptuales se escriben como SVG a mano con las primitivas
  y la paleta de gen_aprendizaje_maquina (marco, texto, caja, flecha, ROLES...);
- las graficas de datos se dibujan con las funciones dibujar_* de ml_lab y
  tema="sitio", y se convierten con gen.svg_de_matplotlib(fig, aria=...);
- ml_lab se pide con gen.ml_lab() dentro de la funcion de la figura, nunca
  al importar este modulo (importacion perezosa, contrato §7.1);
- ningun color de rol se copia como literal: se lee de gen.ROLES;
- las cifras que se dibujan salen de ml_lab o de tools/ml_cifras_c1.py.

Sus pruebas propias van en tools/test_figuras_ml_c1.py (sin prosa); las
guardas comunes, en tools/test_gen_aprendizaje_maquina.py.

Anclas por tramo (protocolo p5.2 §7.1): el catalogo es la suma de un dict por
tramo; cada rama escribe solo antes del «fin» de su tramo.

Lo que ml_lab dibuja y el sitio no admite se corrige aqui, despues de dibujar
y sin tocar ml_lab (SOLICITUD prog-c1 a prog-lab, en la bitacora):
- ml_lab sombrea con alpha (extrapolacion, regiones de la frontera, brecha);
  las guardas prohiben toda opacidad, asi que `_sin_opacidad` hornea cada
  relleno translucido contra el panel;
- dibujar_ajuste pinta la segunda curva con "--" (el trazo del rol realidad)
  y dibujar_proceso(color_por=...) usa el cuadrado de prueba para la segunda
  categoria; `_restilar_*` les devuelve marcas que no son de ningun rol;
- el gris de «observaciones nuevas» de ml_lab (crema al 55 %) se lleva al de
  gen.ROLES (al 60 %), que es la leyenda unica del sitio.
"""
import re

import gen_aprendizaje_maquina as gen
from gen_aprendizaje_maquina import (ACENTO, FONDO, LINEA, PANEL, SUAVE, TEXTO,
                                     _n, caja, flecha, linea, mezclar, svg, texto)

_IT = {"estilo": "italic"}
VERDE = gen.color_rol("f_verdadera")
CIAN = gen.color_rol("f_estimada")
NUEVAS = gen.color_rol("observaciones_nuevas")
PISO = gen.color_rol("piso_bayes")
# Dos colores que no son de ningun rol (contrato §7.3): para una segunda
# estimacion (el polinomio de grado 5) y para una categoria (llueve).
NARANJA = "#ff9e5e"
PERVINCA = "#9fb4ff"
# Ancho de las graficas de datos: 5.4 pulgadas = 388.8 puntos de viewBox, que
# a 600 px dan una escala de 1.54; asi la letra de 8 pt de ml_lab queda en
# 12.3 px (guarda comun de letra minima).
ANCHO_IN = 5.4


# ------------------------------------------------------------ utilidades ---

_ESTILO = re.compile(r'style="([^"]*)"')


def _sin_opacidad(texto_svg, fondo=PANEL):
    """Hornea cada fill/stroke translucido contra el panel y quita la opacidad.

    matplotlib escribe la transparencia como `opacity`, `fill-opacity` o
    `stroke-opacity` dentro de style="..."; el sitio la prohibe (contrato
    §7.3). Todos los rellenos translucidos de estas figuras caen dentro de
    los ejes, sobre PANEL.
    """
    def cambiar(m):
        decl = [d.strip() for d in m.group(1).split(";") if d.strip()]
        props = dict(d.split(":", 1) for d in decl)
        props = {k.strip(): v.strip() for k, v in props.items()}
        general = float(props.pop("opacity", 1))
        relleno = float(props.pop("fill-opacity", 1)) * general
        trazo = float(props.pop("stroke-opacity", 1)) * general
        for clave, alfa in (("fill", relleno), ("stroke", trazo)):
            valor = props.get(clave, "")
            if alfa < 1 and valor.startswith("#") and len(valor) == 7:
                props[clave] = mezclar(valor, alfa, fondo)
        return 'style="' + "; ".join(f"{k}: {v}" for k, v in props.items()) + '"'

    return _ESTILO.sub(cambiar, texto_svg)


def _rotulo(x, y, s, tam=14, anclaje="start", **kw):
    """Un renglon con un rectangulo del color del panel detras (para que una
    linea que pasa por debajo no lo cruce). El ancho es una estimacion."""
    largo = len(s if isinstance(s, str) else "".join(
        t if isinstance(t, str) else t[0] for t in s)) * tam * 0.58
    x0 = {"start": x, "middle": x - largo / 2, "end": x - largo}[anclaje]
    fondo = (f'<rect x="{_n(x0 - 3)}" y="{_n(y - tam)}" width="{_n(largo + 6)}" '
             f'height="{_n(tam * 1.35)}" rx="3" fill="{PANEL}"/>')
    return fondo + texto(x, y, s, tam=tam, anclaje=anclaje, **kw)


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return matplotlib, plt


def _grafica(dibujar, aria, titulo, alto_in, paneles=1, **subplots):
    """Arma una figura de datos con la paleta del sitio y la deja como SVG.

    Parte de los rcParams de fabrica: ml.tema() (seaborn) cambia el estado
    global de matplotlib, y una figura no puede depender de quien corrio antes
    en el mismo proceso (la guarda compara sin escribir)."""
    matplotlib, plt = _plt()
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(gen.RC_SITIO)
        fig, ejes = plt.subplots(paneles, 1, figsize=(ANCHO_IN, alto_in), **subplots)
        dibujar(fig, ejes)
        fig.tight_layout()
        crudo = gen.svg_de_matplotlib(fig, aria, titulo=titulo, ancho=600)
    return _sin_opacidad(crudo)


def _leyenda(ax, **kw):
    ley = ax.legend(frameon=True, fontsize=9, **kw)
    ley.get_frame().set_facecolor(PANEL)
    ley.get_frame().set_edgecolor(LINEA)
    for t in ley.get_texts():
        t.set_color(TEXTO)
    return ley


def _recolorear_nuevas(ax):
    for col in ax.collections:
        if col.get_gid() == "observaciones_nuevas":
            col.set_color(NUEVAS)


def _ajustes(ax):
    return [ln for ln in ax.get_lines() if ln.get_gid() == "ajuste"]


def _pct(v):
    return f"{round(100 * v)} %"


def _num(v, d=1):
    """Numero con punto decimal y el signo menos tipografico."""
    s = f"{v:.{d}f}"
    return s.replace("-", "−")


# --- tramo 1a ---

# ----------------------------------------------- diagrama: ml-c1-reducible ---
#
# P1 §2. Un punto observado y, en su misma x, la f verdadera y la f estimada.
# El segmento y − f̂(x) (el residual, lo unico que se ve con datos reales) se
# parte en f(x) − f̂(x) (reducible) y ε (el azar). Sin cifras.

RED_W, RED_H = 560, 380
RED_X0 = 300           # la x del punto
RED_Y = {"y": 92, "f": 178, "fg": 236}   # alturas en pantalla (y crece hacia abajo)


def _recta_pantalla(y_en_x0, pendiente, x):
    return y_en_x0 - pendiente * (x - RED_X0)


def ml_c1_reducible():
    c = []
    izq, der, arr, aba = 56, 532, 52, 318
    c.append(texto(16, 30, "El residual se parte en dos", tam=17, peso="700",
                   anclaje="start"))
    c.append(caja(izq, arr, der - izq, aba - arr, relleno=PANEL, borde=LINEA, radio=6))
    c.append(texto(izq + 8, aba + 22, ["distancia ", ("x", _IT)], tam=13, color=SUAVE,
                   anclaje="start"))
    c.append(texto(der - 8, arr + 18, ["tiempo ", ("y", _IT)], tam=13, color=SUAVE,
                   anclaje="end"))
    # f verdadera (gruesa, verde) y f estimada (delgada, cian)
    for clave, pendiente, color, grosor in (("f", 0.36, VERDE, 3.5), ("fg", 0.27, CIAN, 1.8)):
        y1 = _recta_pantalla(RED_Y[clave], pendiente, izq + 4)
        y2 = _recta_pantalla(RED_Y[clave], pendiente, der - 4)
        c.append(linea(izq + 4, y1, der - 4, y2, color=color, grosor=grosor))
    c.append(_rotulo(izq + 14, _recta_pantalla(RED_Y["f"], 0.36, izq + 14) - 12,
                   [("f", _IT), ": la regla"], tam=14, color=VERDE, anclaje="start"))
    c.append(_rotulo(izq + 96, _recta_pantalla(RED_Y["fg"], 0.27, izq + 96) - 9,
                   [("f̂", _IT), ": tu ajuste"], tam=14, color=CIAN, anclaje="start"))
    # la x del punto
    c.append(linea(RED_X0, arr + 4, RED_X0, aba - 4, color=LINEA, grosor=1.2, guiones="3 4"))
    # el punto observado
    c.append(f'<circle cx="{_n(RED_X0)}" cy="{_n(RED_Y["y"])}" r="7" fill="{CIAN}" '
             f'stroke="{TEXTO}" stroke-width="1.5"/>')
    c.append(texto(RED_X0, RED_Y["y"] - 16, ["lo que observas: ", ("y", _IT)],
                   tam=14, anclaje="middle"))
    c.append(f'<circle cx="{_n(RED_X0)}" cy="{_n(RED_Y["f"])}" r="4" fill="{VERDE}"/>')
    c.append(f'<circle cx="{_n(RED_X0)}" cy="{_n(RED_Y["fg"])}" r="4" fill="{CIAN}"/>')

    # a la derecha, las dos partes
    xd = RED_X0 + 26
    for y1, y2, color in ((RED_Y["y"], RED_Y["f"], VERDE), (RED_Y["f"], RED_Y["fg"], ACENTO)):
        c.append(linea(xd, y1 + 2, xd, y2 - 2, color=color, grosor=3))
        c.append(linea(xd - 6, y1 + 2, xd + 6, y1 + 2, color=color, grosor=2))
        c.append(linea(xd - 6, y2 - 2, xd + 6, y2 - 2, color=color, grosor=2))
    c.append(_rotulo(xd + 14, (RED_Y["y"] + RED_Y["f"]) / 2 - 4, [("ε", _IT), ": el azar"],
                   tam=14, peso="700", anclaje="start", color=VERDE))
    c.append(_rotulo(xd + 14, (RED_Y["y"] + RED_Y["f"]) / 2 + 15, "ningún ajuste lo baja",
                   tam=13, anclaje="start", color=TEXTO))
    c.append(_rotulo(xd + 14, (RED_Y["f"] + RED_Y["fg"]) / 2 - 2,
                   [("f", _IT), "(", ("x", _IT), ") − ", ("f̂", _IT), "(", ("x", _IT),
                    "): reducible"], tam=14, peso="700", anclaje="start", color=ACENTO))
    c.append(_rotulo(xd + 14, (RED_Y["f"] + RED_Y["fg"]) / 2 + 17, "baja si estimas mejor",
                   tam=13, anclaje="start", color=TEXTO))

    # a la izquierda, el residual completo
    xi = RED_X0 - 30
    c.append(linea(xi, RED_Y["y"] + 2, xi, RED_Y["fg"] - 2, color=TEXTO, grosor=2.5))
    c.append(linea(xi - 6, RED_Y["y"] + 2, xi + 6, RED_Y["y"] + 2, color=TEXTO, grosor=2))
    c.append(linea(xi - 6, RED_Y["fg"] - 2, xi + 6, RED_Y["fg"] - 2, color=TEXTO, grosor=2))
    yr = (RED_Y["y"] + RED_Y["fg"]) / 2 + 8
    c.append(texto(xi - 12, yr - 9, [("y", _IT), " − ", ("f̂", _IT), "(", ("x", _IT),
                                     "): el residual"], tam=14, peso="700", anclaje="end"))
    c.append(texto(xi - 12, yr + 10, "lo único que ves", tam=13, anclaje="end",
                   color=SUAVE))

    c.append(texto(16, RED_H - 16, ["Con datos reales no conoces ", ("f", _IT),
                                     ": ves el residual, nunca sus dos partes."],
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Una observación y, en la misma x, la f verdadera y el ajuste f gorro. "
            "El residual y menos f gorro de x, lo único que se ve, se parte en dos "
            "segmentos: f de x menos f gorro de x, la parte reducible, que baja si "
            "estimas mejor, y épsilon, el azar, que ningún ajuste baja.")
    return svg(RED_W, RED_H, aria, "El residual se parte en dos", c)


# ------------------------------------------ diagrama: ml-c1-cuatro-fuentes ---
#
# P1 §6 (F3, rediseno de la revision 1). Al centro, lo mejor con lo que mides
# con dos halos (1 azar; 2 lo que no mides, que encoge al medir otra
# variable); el ovalo de la familia con la mejor de la familia en su borde
# (3 aproximacion); f̂ con n datos (4 estimacion); aparte, punteado y fuera
# del recuento, lo que devuelve el optimizador (y ademas: optimizacion).

CF_W, CF_H = 600, 420


def ml_c1_cuatro_fuentes():
    c = []
    c.append(texto(16, 30, "Las cuatro fuentes del error", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "distancias hasta lo mejor que se puede hacer con lo que mides",
                   tam=13, color=SUAVE, anclaje="start"))
    cx, cy = 128, 206
    # halo 2: lo que no mides
    c.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="{mezclar(SUAVE, 0.10)}" '
             f'stroke="{SUAVE}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    # halo 1: azar
    c.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="{mezclar(SUAVE, 0.24)}" '
             f'stroke="{SUAVE}" stroke-width="1.5"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{VERDE}" stroke="{TEXTO}" '
             f'stroke-width="1.2"/>')
    c.append(texto(cx, cy - 16, "1 · azar", tam=13, peso="700"))
    c.append(texto(cx, cy - 56, "2 · lo que", tam=13, peso="700"))
    c.append(texto(cx, cy - 42, "no mides", tam=13, peso="700"))
    c.append(texto(cx, cy + 102, "lo mejor con", tam=13, color=VERDE, peso="700"))
    c.append(texto(cx, cy + 118, "lo que mides", tam=13, color=VERDE, peso="700"))
    c.append(texto(cx, cy + 138, "1 y 2 fijan el piso", tam=13, color=SUAVE))
    # medir otra variable: flecha que encoge el halo 2
    c.append(texto(16, 82, "medir otra variable", tam=13, color=SUAVE, anclaje="start"))
    c.append(texto(16, 98, "encoge el halo 2", tam=13, color=SUAVE, anclaje="start"))
    c.append(flecha(52, 106, cx - 50, cy - 56, color=SUAVE))

    # la familia
    fx, fy, rx, ry = 462, 200, 126, 100
    c.append(f'<ellipse cx="{fx}" cy="{fy}" rx="{rx}" ry="{ry}" fill="{PANEL}" '
             f'stroke="{LINEA}" stroke-width="2"/>')
    c.append(texto(fx + 30, fy - ry + 26, "la familia", tam=14, peso="700", color=SUAVE))
    mx, my = fx - rx, fy + 6            # la mejor de la familia, en el borde
    c.append(f'<circle cx="{mx}" cy="{my}" r="6" fill="{TEXTO}"/>')
    c.append(texto(mx + 12, my + 26, "la mejor de", tam=13, anclaje="start"))
    c.append(texto(mx + 12, my + 42, "la familia", tam=13, anclaje="start"))
    c.append(flecha(mx - 8, my, cx + 84, my, color=ACENTO, grosor=2.5))
    c.append(texto((mx + cx + 78) / 2, my - 12, "3 · aproximación", tam=13, peso="700",
                   color=ACENTO))
    # f gorro con n datos
    gx, gy = fx + 50, fy - 30
    c.append(f'<circle cx="{gx}" cy="{gy}" r="6" fill="{CIAN}"/>')
    c.append(texto(gx, gy - 14, [("f̂", _IT), " con ", ("n", _IT), " datos"], tam=13,
                   color=CIAN))
    c.append(flecha(gx - 8, gy + 4, mx + 12, my - 4, color=ACENTO, grosor=2.5))
    c.append(texto((gx + mx) / 2 + 4, (gy + my) / 2 - 14, "4 · estimación", tam=13,
                   peso="700", color=ACENTO))

    # aparte: optimizacion
    ox, oy = 462, 352
    c.append(caja(ox - 128, oy - 22, 256, 64, relleno=FONDO, borde=SUAVE, radio=8,
                  grosor=1.5, guiones="3 4"))
    c.append(texto(ox, oy - 2, "lo que devuelve el optimizador", tam=13, color=SUAVE))
    c.append(texto(ox, oy + 17, "y además: optimización", tam=13, peso="700",
                   color=SUAVE))
    c.append(texto(ox, oy + 34, "(fuera de las cuatro)", tam=12, color=SUAVE))
    c.append(linea(gx, oy - 24, gx, gy + 10, color=SUAVE, grosor=1.5, guiones="3 4"))
    aria = ("Diagrama de las cuatro fuentes del error. Al centro, lo mejor que se puede "
            "predecir con lo que mides, rodeado de dos halos: 1, el azar, y 2, lo que no "
            "mides, que se encoge al medir otra variable; las dos fijan el piso. A la "
            "derecha, el óvalo de la familia: la mejor de la familia, en su borde, está a "
            "una distancia de aproximación (3) del centro, y f gorro con n datos está a una "
            "distancia de estimación (4) de la mejor de la familia. Aparte, punteado y "
            "fuera de las cuatro: lo que devuelve el optimizador, el error de optimización.")
    return svg(CF_W, CF_H, aria, "Las cuatro fuentes del error", c)


# ---------------------------------------------- diagrama: ml-c1-matriz-phi ---
#
# P1 §8 (F7a). Las seis entregas de la unidad 6 con tres Φ lado a lado:
# (1, x), (1, x, x²) y (1, 1/x); debajo, la misma multiplicacion Φβ.

MP_W, MP_H = 600, 400
_RECIPROCOS = ("1", "1/2", "1/3", "1/4", "1/5", "1/6")


def _matriz(c, x0, y0, encabezados, filas, ancho_celda=40, alto=26):
    """Una rejilla con encabezados; la primera columna (la de unos) resaltada."""
    ncol = len(encabezados)
    c.append(caja(x0, y0, ncol * ancho_celda, alto * len(filas), relleno=PANEL,
                  borde=LINEA, radio=4, grosor=1.5))
    c.append(caja(x0, y0, ancho_celda, alto * len(filas),
                  relleno=mezclar(ACENTO, 0.18, PANEL), borde=ACENTO, radio=4, grosor=1.5))
    for j, enc in enumerate(encabezados):
        c.append(texto(x0 + (j + 0.5) * ancho_celda, y0 - 8, enc, tam=13, peso="700",
                       color=ACENTO if j == 0 else TEXTO))
    for i, fila in enumerate(filas):
        for j, v in enumerate(fila):
            c.append(texto(x0 + (j + 0.5) * ancho_celda, y0 + (i + 0.5) * alto + 5, v,
                           tam=13, fuente=gen.MONO))


def ml_c1_matriz_phi():
    c = []
    c.append(texto(16, 30, "Tres Φ para las mismas seis entregas", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "cada fila es una entrega; cada columna, algo que calculas de x",
                   tam=13, color=SUAVE, anclaje="start"))
    y0 = 118
    xs = [str(k) for k in range(1, 7)]
    # columna de x (los datos)
    c.append(texto(44, y0 - 34, "datos", tam=13, color=SUAVE))
    _matriz(c, 24, y0, [""], [[v] for v in xs])
    c.append(caja(24, y0, 40, 156, relleno=FONDO, borde=SUAVE, radio=4, grosor=1.2))
    for i, v in enumerate(xs):
        c.append(texto(44, y0 + (i + 0.5) * 26 + 5, v, tam=13, fuente=gen.MONO, color=CIAN))
    c.append(texto(44, y0 - 8, "x", tam=13, peso="700", estilo="italic", color=CIAN))

    bloques = [
        (100, ["(1, ", ("x", _IT), ")"], ["1", "x"], [["1", v] for v in xs], "q = 2"),
        (232, ["(1, ", ("x", _IT), ", ", ("x", _IT), "²)"], ["1", "x", "x²"],
         [["1", v, str(int(v) ** 2)] for v in xs], "q = 3"),
        (404, ["(1, 1/", ("x", _IT), ")"], ["1", "1/x"],
         [["1", r] for r in _RECIPROCOS], "q = 2"),
    ]
    for x0, titulo, enc, filas, q in bloques:
        ancho = 46 * len(enc)
        c.append(texto(x0 + ancho / 2, y0 - 50, ["φ(", ("x", _IT), ") = "] + titulo, tam=14,
                       peso="700"))
        c.append(texto(x0 + ancho / 2, y0 - 32, q, tam=13, color=SUAVE))
        _matriz(c, x0, y0, enc, filas, ancho_celda=46)
        yb = y0 + 156 + 34
        c.append(texto(x0 + ancho / 2, yb, ["Φ ", ("β", _IT), " = ", ("ŷ", _IT)], tam=15,
                       peso="700", color=CIAN))
        c.append(texto(x0 + ancho / 2, yb + 18, f"6×{len(enc)} por {len(enc)}", tam=12,
                       color=SUAVE))
    c.append(flecha(68, y0 + 78, 96, y0 + 78, color=SUAVE))
    c.append(texto(16, MP_H - 48, ["La primera columna es la de unos (su coeficiente es ",
                                    ("β", _IT), "₀)."], tam=13, anclaje="start",
                   color=ACENTO))
    c.append(texto(16, MP_H - 26, ["Cambia Φ; el ajuste es el mismo: ", ("β", _IT),
                                    " entra multiplicando columnas ya calculadas."],
                   tam=13, anclaje="start"))
    aria = ("Las seis entregas, con x de 1 a 6, escritas con tres matrices de diseño "
            "lado a lado: phi de x igual a (1, x), con 2 columnas; (1, x, x al cuadrado), "
            "con 3 columnas y valores 1, 4, 9, 16, 25 y 36; y (1, 1 entre x), con 2 "
            "columnas y valores 1, 1/2, 1/3, 1/4, 1/5 y 1/6. La primera columna de cada "
            "una es la de unos. Debajo de cada matriz, la misma multiplicación Φ por beta "
            "igual a y gorro.")
    return svg(MP_W, MP_H, aria, "Tres Φ para las mismas seis entregas", c)


# ------------------------------------- grafica: ml-c1-ganador-imposible ---
#
# P1 §1. Las seis entregas; la recta y el polinomio de grado 5 ajustados a las
# seis, extrapolados a 7 km. Cifras de cifras_c1_ganador().

def ml_c1_ganador_imposible():
    import numpy as np
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    g = cif.cifras_c1_ganador()
    p1 = [g["pendiente_recta"], g["intercepto_recta"]]
    p5 = g["coeficientes_grado_5"]
    r7, q7 = g["prediccion"][7.0]

    def dibujar(fig, ax):
        ax.axvspan(6, 7.5, color=SUAVE, alpha=0.16, lw=0)
        ax.axvspan(0, 1, color=SUAVE, alpha=0.16, lw=0)
        ax.axhline(0, color=SUAVE, lw=1)
        ml.dibujar_ajuste({f"recta de las seis (RMSE {g['rmse_1']:.3f})":
                           lambda x: np.polyval(p1, x),
                           "grado 5, pasa por las seis (RMSE 0)":
                           lambda x: np.polyval(p5, x)},
                          ventana=(0, 7.5), ax=ax, tema="sitio")
        recta, quinta = _ajustes(ax)
        recta.set_color(CIAN)
        recta.set_linewidth(2.2)
        quinta.set_linestyle("-")
        quinta.set_color(NARANJA)
        quinta.set_linewidth(2.2)
        rol = gen.ROLES["entrenamiento"]
        ax.scatter(cif.ENTREGAS_X, cif.ENTREGAS_Y, marker=rol["marcador"], s=46,
                   color=rol["color"], edgecolor=TEXTO, linewidths=0.8, zorder=6,
                   label="las seis entregas")
        ax.scatter([7, 7], [r7, q7], marker="D", s=40, color=[CIAN, NARANJA],
                   edgecolor=TEXTO, linewidths=0.8, zorder=7)
        ax.annotate(f"{_num(r7)} min", (7, r7), xytext=(-62, 4),
                    textcoords="offset points", color=CIAN, fontsize=10, fontweight="bold")
        ax.annotate(f"{_num(q7)} min", (7, q7), xytext=(-64, -3),
                    textcoords="offset points", color=NARANJA, fontsize=10,
                    fontweight="bold")
        ax.text(6.1, 73, "fuera de\nlos datos", color=TEXTO, fontsize=9, va="top")
        ax.text(0.15, -31, "tiempo negativo: imposible", color=TEXTO, fontsize=9)
        ax.set_xlim(0, 7.5)
        ax.set_ylim(-36, 78)
        ax.set_xlabel("distancia x (km)")
        ax.set_ylabel("tiempo (min)")
        _leyenda(ax, loc="upper left")

    aria = (f"Seis entregas de 1 a 6 km; la recta ajustada predice {_num(r7)} minutos a "
            f"7 km y el polinomio de grado 5, que pasa por los seis puntos, predice "
            f"{_num(q7)} minutos. A 3.5 km los dos predicen "
            f"{_num(g['prediccion'][3.5][0])} minutos.")
    return _grafica(dibujar, aria, "El ajuste que ganó predice un tiempo imposible", 3.7)


# ------------------------------------------- grafica: ml-c1-mismo-mundo ---
#
# P1 §2. La misma f = 10 + 4x y tres muestras de 20 entregas (semillas 0, 1,
# 2) con sus ajustes; al fondo, 200 observaciones nuevas de realidad. Con
# sigma_e = 3 (el tope del deslizador del bloque 1 de NB01) para que las tres
# rectas se separen a la vista; con sigma_e = 1 se enciman.
SIGMA_MISMO_MUNDO = 3.0

def ml_c1_mismo_mundo():
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    datos = cif.datos_entregas(sigma_e=SIGMA_MISMO_MUNDO)
    muestras = [datos] + [datos._rehacer(datos.semilla + i) for i in (1, 2)]
    modelos = [ml.ajustar(d) for d in muestras]
    pendientes = [float(m.beta_gorro["x"]) for m in modelos]

    def dibujar(fig, ax):
        ml.dibujar_proceso(datos, realizaciones=3, puntos_realidad=200, ax=ax,
                           tema="sitio")
        _recolorear_nuevas(ax)
        ml.dibujar_ajuste({f"ajuste a la muestra {k + 1}": m for k, m in enumerate(modelos)},
                          ventana=(0, 6), ax=ax, tema="sitio")
        for ln in _ajustes(ax):
            ln.set_color(CIAN)
            ln.set_linestyle("-")
            ln.set_linewidth(1.4)
        ax.set_xlabel("distancia x (km)")
        ax.set_ylabel("tiempo y (min)")
        ax.set_xlim(0, 6)
        manejadores, rotulos = ax.get_legend_handles_labels()
        quedan = [(h, r) for h, r in zip(manejadores, rotulos)
                  if not r.startswith("ajuste a la muestra") or r.endswith("1")]
        _leyenda(ax, handles=[h for h, _ in quedan],
                 labels=["f̂ de cada muestra" if r.startswith("ajuste") else
                         ("20 entregas (tres muestras)" if r == "entrenamiento" else r)
                         for _, r in quedan], loc="upper left")
        ax.set_ylabel("tiempo y (min)")

    aria = ("La misma f verdadera, 10 más 4x, con ruido de desviación estándar 3, y tres "
            "muestras de 20 entregas cada una "
            "con su recta ajustada; las pendientes ajustadas son "
            + ", ".join(_num(p, 2) for p in pendientes)
            + ". Al fondo, 200 observaciones nuevas del mismo proceso.")
    return _grafica(dibujar, aria, "Un proceso, tres muestras, tres ajustes", 3.7)


# ---------------------------------- grafica: ml-c1-aprender-es-minimizar ---
#
# P1 §3 (idea de DL fig. 5.1). Arriba, 20 entregas y la recta ajustada; abajo,
# L_ent como funcion de la pendiente con el intercepto en su valor ajustado,
# y su minimo.

def ml_c1_aprender_es_minimizar():
    import numpy as np
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    datos = cif.datos_entregas()
    m = ml.ajustar(datos)
    b0, b1 = float(m.beta_gorro["1"]), float(m.beta_gorro["x"])
    L_min = float(ml.L(m, datos.ent))

    def dibujar(fig, ejes):
        arriba, abajo = ejes
        ml.dibujar_ajuste(m, datos, ax=arriba, tema="sitio")
        recta = _ajustes(arriba)[0]
        recta.set_label(f"recta ajustada: {_num(b0, 2)} + {_num(b1, 2)}x")
        arriba.set_xlabel("distancia x (km)")
        arriba.set_ylabel("tiempo y (min)")
        manejadores, rotulos = arriba.get_legend_handles_labels()
        _leyenda(arriba, handles=manejadores, loc="upper left",
                 labels=["20 entregas" if r == "entrenamiento" else r for r in rotulos])
        ml.dibujar_perdida_1d(datos, None, "x", np.linspace(b1 - 1.5, b1 + 1.5, 121),
                              ax=abajo, tema="sitio")
        for ln in abajo.get_lines():
            if ln.get_gid() == "minimo":
                ln.set_label(rf"mínimo: $\widehat{{\beta}}_1$ = {_num(b1, 2)}")
            else:
                ln.set_label(r"$L_{\mathrm{ent}}$ al mover la pendiente")
        abajo.set_xlabel(r"pendiente $\beta_1$ (con $\beta_0$ fijo en su valor ajustado)")
        abajo.set_ylabel(r"$L_{\mathrm{ent}}(\beta_1)$")
        _leyenda(abajo, loc="upper center")

    aria = (f"Arriba, 20 entregas y la recta ajustada, {_num(b0, 2)} más {_num(b1, 2)} x. "
            f"Abajo, el error cuadrático medio de entrenamiento como función de la "
            f"pendiente, una parábola con su mínimo en {_num(b1, 2)}, donde vale "
            f"{_num(L_min, 2)}: aprender es minimizar.")
    return _grafica(dibujar, aria, "Aprender es minimizar", 6.0, paneles=2)


# ---------------------------------------------------- grafica: ml-c1-piso ---
#
# P1 §4. R (aproximado con 100 000 observaciones) del oraculo, la recta y la
# media contra la linea del piso, con sigma_e = 1 y 2. La media de
# entrenamiento (el benchmark) sale de la escala: se dibuja recortada y con
# su valor escrito.

def ml_c1_piso():
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    cifras = cif.cifras_c1_piso()
    tope = 6.0

    def dibujar(fig, ejes):
        for ax, s in zip(ejes, cif.SIGMAS_PISO):
            datos = cif.datos_entregas(sigma_e=s)
            ml.dibujar_piso(datos, cif.modelos_piso(datos), perdida="cuadratica", ax=ax,
                            tema="sitio")
            c = cifras[s]
            valores = [c["R_oraculo"], c["R_recta"], c["R_media"]]
            barras = [p for p in ax.patches if p.get_gid() == "riesgo"]
            barras[2].set_facecolor(mezclar(ACENTO, 0.35, PANEL))
            barras[2].set_edgecolor(ACENTO)
            barras[2].set_linestyle("-.")
            barras[2].set_linewidth(1.6)
            for k, (b, v) in enumerate(zip(barras, valores)):
                alto = min(v, tope)
                rotulo = _num(v, 2) if v < tope else f"{_num(v, 1)} ↑"
                ax.text(b.get_x() + b.get_width() / 2, alto - (0.5 if v >= tope else -0.12),
                        rotulo, ha="center", va="bottom", fontsize=10, color=TEXTO,
                        fontweight="bold")
            for ln in ax.get_lines():
                if ln.get_gid() == "piso":
                    ln.set_label(rf"piso $R_{{\mathrm{{Bayes}}}} = \sigma_\varepsilon^2$ = {c['piso']:g}")
            ax.set_ylim(0, tope)
            ax.set_ylabel("R (100 000 obs.)")
            ax.set_title(rf"$\sigma_\varepsilon = {s:g}$", color=TEXTO, fontsize=11)
            manejadores, rotulos = ax.get_legend_handles_labels()
            pares = [(h, r) for h, r in zip(manejadores, rotulos) if r.startswith("piso")]
            _leyenda(ax, handles=[h for h, _ in pares], labels=[r for _, r in pares],
                     loc="upper left")
            ax.set_xticks(range(3))
            ax.set_xticklabels(["oráculo f", "recta\najustada", "media\n(benchmark)"])

    uno, dos = cifras[1.0], cifras[2.0]
    aria = ("Riesgo aproximado con 100 000 observaciones de tres predictores contra la "
            "línea del piso. Con sigma épsilon igual a 1, el piso es 1: el oráculo f da "
            f"{_num(uno['R_oraculo'], 2)}, la recta ajustada {_num(uno['R_recta'], 2)} y "
            f"la media {_num(uno['R_media'], 1)}. Con sigma épsilon igual a 2, el piso es "
            f"4: el oráculo da {_num(dos['R_oraculo'], 2)}, la recta "
            f"{_num(dos['R_recta'], 2)} y la media {_num(dos['R_media'], 1)}. Duplicar "
            "sigma cuadruplica el piso, y ni el oráculo baja de él.")
    return _grafica(dibujar, aria, "El piso que nadie baja", 6.0, paneles=2)


# ---------------------------------------------- grafica: ml-c1-dos-franjas ---
#
# P1 §5 (ejemplo de la lluvia, caso 2). Arriba, la nube de tiempos contra
# distancia de un solo color, con E[y | x1] = 13 + 4 x1; abajo, la misma
# nube coloreada por x2 (llueve o no): dos franjas paralelas.

def ml_c1_dos_franjas():
    import numpy as np
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    con = cif.datos_lluvia(medir_lluvia=True)
    ll = cif.cifras_c1_lluvia()
    x = np.linspace(0, 6, 50)

    def dibujar(fig, ejes):
        arriba, abajo = ejes
        ml.dibujar_proceso(con, mostrar_f=False, ax=arriba, tema="sitio")
        arriba.plot(x, 13 + 4 * x, color=VERDE, lw=gen.ROLES["f_verdadera"]["grosor"],
                    label="lo mejor sin ver la lluvia: 13 + 4x₁", zorder=2)
        arriba.set_title(f"sin medir la lluvia: piso {ll['piso_sin_x2']:.0f}",
                         color=TEXTO, fontsize=11)
        ml.dibujar_proceso(con, mostrar_f=False, color_por="x2", ax=abajo, tema="sitio")
        estilos = {0: ("o", CIAN, "no llueve (x₂ = 0)"), 1: ("D", PERVINCA, "llueve (x₂ = 1)")}
        for col in abajo.collections:
            r = col.get_label()
            for valor, (marca, color, rotulo) in estilos.items():
                if r == f"x2 = {valor}":
                    col.set_color(color)
                    col.set_label(rotulo)
                    from matplotlib.markers import MarkerStyle
                    col.set_paths([MarkerStyle(marca).get_path().transformed(
                        MarkerStyle(marca).get_transform())])
        abajo.plot(x, 10 + 4 * x, color=VERDE, lw=gen.ROLES["f_verdadera"]["grosor"],
                   label="f con cada valor de x₂", zorder=2)
        abajo.plot(x, 16 + 4 * x, color=VERDE, lw=gen.ROLES["f_verdadera"]["grosor"],
                   zorder=2)
        abajo.set_title(f"midiendo la lluvia: piso {ll['piso_con_x2']:.0f}", color=TEXTO,
                        fontsize=11)
        for ax in ejes:
            ax.set_xlabel("distancia x₁ (km)")
            ax.set_ylabel("tiempo y (min)")
            ax.set_xlim(0, 6)
            ax.set_ylim(5, 42)
            manejadores, rotulos = ax.get_legend_handles_labels()
            rotulos = ["20 entregas" if r == "entrenamiento" else r for r in rotulos]
            _leyenda(ax, handles=manejadores, labels=rotulos, loc="upper left")

    aria = ("Arriba, 20 entregas, tiempo contra distancia, de un solo color, con la "
            "recta 13 más 4 x1, lo mejor sin ver la lluvia: el piso es 10. Abajo, la "
            "misma nube coloreada según si llueve: se parte en dos franjas paralelas, "
            "10 más 4 x1 y 16 más 4 x1, y el piso baja a 1.")
    return _grafica(dibujar, aria, "Ruido que no es ruido: la lluvia", 6.2, paneles=2)


# ----------------------------------------- grafica: ml-c1-anillos-polares ---
#
# P1 §7 (idea de DL fig. 1.1). La misma logistica en (1, x1, x2) y en
# (1, r, theta), con sus aciertos en el despliegue. En polares, la frontera
# radial ideal (la de Bayes, horizontal porque r es el eje vertical) y la
# ajustada, que se inclina un poco por el coeficiente de theta.

def ml_c1_anillos_polares():
    import numpy as np
    import ml_cifras_c1 as cif
    ml = gen.ml_lab()
    a = cif.cifras_c1_anillos()
    datos = cif.datos_anillos()
    modelos = {rep: ml.ajustar(datos, phi=cif.phi_anillos(rep), tarea="clasificacion")
               for rep in ("cartesianas", "polares")}
    r_bayes = a["radio_bayes"]
    b_theta = a["polares"]["beta"]["theta"]

    def dibujar(fig, ejes):
        arriba, abajo = ejes
        ml.dibujar_frontera(modelos["cartesianas"], datos.ent, vista="cartesianas",
                            ax=arriba, tema="sitio")
        arriba.set_title(f"cartesianas (1, x₁, x₂): aciertos en el despliegue "
                         f"{_pct(a['cartesianas']['aciertos'])}", color=TEXTO, fontsize=11)
        ml.dibujar_frontera(modelos["polares"], datos.ent, vista="polares", ax=abajo,
                            tema="sitio")
        th = np.linspace(-np.pi, np.pi, 50)
        abajo.plot(th, np.full_like(th, r_bayes), ls=":", color=PISO, lw=2,
                   label=f"ideal: r = {r_bayes:.2f}")
        abajo.set_title(f"polares (1, r, θ): aciertos en el despliegue "
                        f"{_pct(a['polares']['aciertos'])}", color=TEXTO, fontsize=11)
        abajo.text(np.pi * 0.98, r_bayes + 0.55, f"ajustada: coeficiente de θ = "
                   f"{_num(b_theta, 2)}", ha="right", fontsize=9, color=TEXTO,
                   bbox={"facecolor": PANEL, "edgecolor": LINEA, "boxstyle": "round"})
        abajo.set_xlabel("θ (ángulo)")
        abajo.set_ylabel("r (radio)")
        for ax in ejes:
            manejadores, rotulos = ax.get_legend_handles_labels()
            rotulos = [{"y = 0": "y = 0 (interior)", "y = 1": "y = 1 (exterior)"}.get(r, r)
                       for r in rotulos]
            _leyenda(ax, handles=manejadores, labels=rotulos, loc="upper right")

    aria = (f"La misma regresión logística sobre dos anillos. Arriba, en cartesianas "
            f"(1, x1, x2): la frontera es una recta y acierta "
            f"{_pct(a['cartesianas']['aciertos'])} en el despliegue, como la moda "
            f"({_pct(a['moda'])}). Abajo, en polares (1, r, theta): la frontera ajustada "
            f"es casi la línea r constante (el coeficiente de theta es "
            f"{_num(b_theta, 2)}), junto a la ideal r = {r_bayes:.2f}, y acierta "
            f"{_pct(a['polares']['aciertos'])}; ni el clasificador de Bayes pasa de "
            f"{_pct(a['bayes'])}.")
    return _grafica(dibujar, aria, "Los anillos en dos representaciones", 6.6, paneles=2)


_TRAMO_1A = {
    "ml-c1-ganador-imposible": ml_c1_ganador_imposible,
    "ml-c1-mismo-mundo": ml_c1_mismo_mundo,
    "ml-c1-reducible": ml_c1_reducible,
    "ml-c1-aprender-es-minimizar": ml_c1_aprender_es_minimizar,
    "ml-c1-piso": ml_c1_piso,
    "ml-c1-dos-franjas": ml_c1_dos_franjas,
    "ml-c1-cuatro-fuentes": ml_c1_cuatro_fuentes,
    "ml-c1-anillos-polares": ml_c1_anillos_polares,
    "ml-c1-matriz-phi": ml_c1_matriz_phi,
}

# --- fin tramo 1a ---


# --- tramo 1b ---
_TRAMO_1B = {}
# --- fin tramo 1b ---


# --- tramo tarea ---
_TRAMO_TAREA = {}
# --- fin tramo tarea ---


FIGURAS_C1 = {**_TRAMO_1A, **_TRAMO_1B, **_TRAMO_TAREA}
