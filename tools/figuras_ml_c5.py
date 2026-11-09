"""Figuras de la clase 5 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C5: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c5-", es un error.

Dueno: prog-c5 (lo creo vacio prog-lab en U.T3). Reglas para llenarlo:
- los diagramas conceptuales se escriben como SVG a mano con las primitivas
  y la paleta de gen_aprendizaje_maquina (marco, texto, caja, flecha, ROLES...);
- las graficas de datos se dibujan con las funciones dibujar_* de ml_lab y
  tema="sitio", y se convierten con gen.svg_de_matplotlib(fig, aria=...);
- ml_lab se pide con gen.ml_lab() dentro de la funcion de la figura, nunca
  al importar este modulo (importacion perezosa, contrato §7.1);
- ningun color de rol se copia como literal: se lee de gen.ROLES;
- las cifras que se dibujan salen de ml_lab o de tools/ml_cifras_c5.py.

El catalogo se parte en dos dicts (clase_5.md §10.8): FIGURAS_C5_P1 (las
nueve de la pagina 1) y FIGURAS_C5_P2 (las siete de la pagina 2). FIGURAS_C5
es lo que lee el generador. Todas las funciones se llaman fig_* para que
fig_tuberia no tape a ml_lab.tuberia.

Sus pruebas propias van en tools/test_figuras_ml_c5.py (sin prosa); las
guardas comunes, en tools/test_gen_aprendizaje_maquina.py. Lo que ml_lab
dibuja con transparencia se hornea contra el panel (`_sin_opacidad`).
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
APAGADO = mezclar(SUAVE, 0.35)
ANCHO_IN = 5.4
_IT = {"estilo": "italic"}


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
    import ml_cifras_c5 as cif
    return cif


def _titulo(ax, s, tam=9.5):
    ax.set_title(s, color=TEXTO, fontsize=tam)


def _np():
    import numpy as np
    return np


def flecha_g(x1, y1, x2, y2, color=ACENTO, grosor=2, guiones="6 4"):
    """Flecha con trazo discontinuo («aplicar»): la punta es la de flecha."""
    f = flecha(x1, y1, x2, y2, color=color, grosor=grosor)
    return f.replace("/>", f' stroke-dasharray="{guiones}"/>')


def _renglones(x, y, lineas, tam=12, color=TEXTO, salto=16, anclaje="middle", **kw):
    return [texto(x, y + i * salto, s, tam=tam, color=color, anclaje=anclaje, **kw)
            for i, s in enumerate(lineas)]


# =========================================================== diagramas ===

# ------------------------------------------------ ml-c5-modelo-exitoso ---
ME_W, ME_H = 600, 300


def fig_modelo_exitoso():
    c = [texto(16, 30, "Un modelo exitoso: tres requisitos", tam=17, peso="700",
               anclaje="start"),
         texto(16, 52, "la clase 2 lo puso en un recuadro; aquí la tercera tarjeta es el tema",
               tam=13, color=SUAVE, anclaje="start")]
    tarjetas = [("1", ["error de", "entrenamiento", "pequeño"], "clases 1 a 4", False),
                ("2", ["brecha", "entrenamiento–prueba", "pequeña"], "clases 1 a 4", False),
                ("3", ["la prueba", "imita la", "realidad"], "clase 5", True)]
    w, h, y0 = 176, 170, 76
    for i, (num, lineas, rot, encendida) in enumerate(tarjetas):
        x = 16 + i * (w + 10)
        borde = ACENTO if encendida else APAGADO
        relleno = PANEL if encendida else FONDO
        c.append(caja(x, y0, w, h, relleno=relleno, borde=borde, radio=12,
                      grosor=3 if encendida else 1.5,
                      guiones=None if encendida else "5 4"))
        c.append(texto(x + w / 2, y0 + 38, num, tam=26, peso="700",
                       color=ACENTO if encendida else SUAVE))
        c += _renglones(x + w / 2, y0 + 72, lineas, tam=15, salto=20,
                        color=TEXTO if encendida else SUAVE,
                        peso="700" if encendida else "normal")
        c.append(texto(x + w / 2, y0 + h - 14, rot, tam=12,
                       color=ACENTO if encendida else SUAVE))
    c.append(texto(16, ME_H - 22, "las dos primeras comparan números de tus datos; la tercera "
                   "compara tus datos con el uso", tam=12, color=SUAVE, anclaje="start"))
    aria = ("Tres requisitos de un modelo exitoso: error de entrenamiento pequeño y brecha "
            "entrenamiento–prueba pequeña, atenuados, se vieron en las clases 1 a 4; el "
            "tercero, encendido, la prueba imita la realidad, es el de la clase 5")
    return svg(ME_W, ME_H, aria, "Tres requisitos de un modelo exitoso", c)


# ------------------------------------------------------- ml-c5-bolsas ---
BO_W, BO_H = 600, 440


def _bolsa(cx, cy, colores, borde=LINEA):
    """Una bolsa (rectangulo redondeado) con bolas rojas (ROSA) y verdes (VERDE)."""
    out = [caja(cx - 52, cy - 40, 104, 80, relleno=FONDO, borde=borde, radio=22)]
    for k, col in enumerate(colores):
        fila, colm = divmod(k, 5)
        x, y = cx - 36 + colm * 18, cy - 20 + fila * 18
        out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>')
    return out


def fig_bolsas():
    R, V = ROSA, VERDE
    c = [texto(16, 28, "Cuatro maneras de sacar bolas", tam=17, peso="700", anclaje="start")]
    # dos grupos rotulados
    c.append(caja(10, 44, 580, 236, relleno="none", borde=CIAN, radio=12, grosor=1.5))
    c.append(texto(22, 64, "¿tu muestra es iid?", tam=14, peso="700", color=CIAN,
                   anclaje="start"))
    c.append(caja(10, 290, 580, 140, relleno="none", borde=ORO, radio=12, grosor=1.5))
    c.append(texto(22, 310, "¿el uso sale de la misma bolsa?", tam=14, peso="700", color=ORO,
                   anclaje="start"))
    mezcla = [R, V, V, R, V, R, V, V, R, V, V, R, V, R, V]
    paneles = [
        (106, 140, "(a) iid", ["cada bola sale de la", "misma bolsa y se devuelve"], mezcla, LINEA),
        (300, 140, "(c) grupos", ["se sacan puñados: las de", "un puñado se parecen"],
         [R, R, R, V, V, V, V, V, R, R, R, R, V, V, V], LINEA),
        (494, 140, "(d) tiempo", ["la bolsa se tiñe poco", "a poco: las seguidas", "se parecen"],
         [V, V, V, V, V, V, V, R, V, R, R, R, R, R, R], LINEA),
    ]
    for cx, cy, rot, lin, cols, borde in paneles:
        c.append(texto(cx, 92, rot, tam=14, peso="700"))
        c += _bolsa(cx, cy, cols, borde)
        c += _renglones(cx, 210, lin, tam=12, color=SUAVE, salto=15)
    # (b) otra poblacion: dos bolsas
    c.append(texto(578, 310, "(b) otra población", tam=14, peso="700", anclaje="end"))
    c += _bolsa(170, 362, mezcla[:10])
    c.append(texto(170, 420, "tu muestra: puede ser iid", tam=12, color=SUAVE))
    c += _bolsa(430, 362, [R, R, R, V, R, R, V, R, R, R], borde=ORO)
    c.append(texto(430, 420, "el uso: otra bolsa, otra mezcla", tam=12, color=SUAVE))
    c.append(flecha(236, 370, 364, 370, color=SUAVE))
    c.append(texto(300, 360, "≠", tam=18, peso="700", color=ORO))
    aria = ("Cuatro maneras de sacar bolas: tres sobre la muestra (iid, a puñados, una bolsa "
            "que cambia de color) y una sobre el uso (otra bolsa)")
    return svg(BO_W, BO_H, aria, "Cuatro maneras de sacar bolas", c)


# --------------------------------------------------- ml-c5-particiones ---
PA_W, PA_H = 600, 330


def fig_particiones():
    c = [texto(16, 28, "Tres maneras de armar cinco pliegues", tam=17, peso="700",
               anclaje="start"),
         texto(16, 48, "renglón = iteración; celda = bloque de filas", tam=12, color=SUAVE,
               anclaje="start")]
    celda, gap, y0 = 14, 3, 84
    titulos = [("al azar", 16), ("por grupos", 214), ("temporal", 412)]
    np = _np()
    rng = np.random.default_rng(5)
    azar = rng.permutation(np.repeat(np.arange(5), 2))
    for nombre, x0 in titulos:
        c.append(texto(x0 + 85, 72, nombre, tam=14, peso="700"))
    marcas = {"ent": (CIAN, "●"), "val": (ORO, "▲"), "prueba": (ROSA, "■"), "nada": (FONDO, "")}
    for m in range(5):
        y = y0 + m * (celda + 14)
        c.append(texto(10, y + 11, str(m + 1), tam=12, color=SUAVE, anclaje="start"))
        for nombre, x0 in titulos:
            for j in range(10):
                x = x0 + 8 + j * (celda + gap)
                if nombre == "temporal":
                    if j >= 9:
                        rol = "prueba"
                    elif j < 3 + m:
                        rol = "ent"
                    elif j == 3 + m:
                        rol = "val"
                    else:
                        rol = "nada"
                elif nombre == "al azar":
                    rol = "val" if azar[j] == m else "ent"
                else:
                    rol = "val" if j // 2 == m else "ent"
                color, _ = marcas[rol]
                if rol == "nada":
                    c.append(caja(x, y, celda, celda, relleno=FONDO, borde=APAGADO, radio=3,
                                  grosor=1))
                elif rol == "val":
                    c.append(f'<path d="M {x + celda / 2} {y} L {x + celda} {y + celda} '
                             f'L {x} {y + celda} z" fill="{color}"/>')
                elif rol == "prueba":
                    c.append(caja(x, y, celda, celda, relleno=color, borde=color, radio=1,
                                  grosor=1))
                else:
                    c.append(f'<circle cx="{x + celda / 2}" cy="{y + celda / 2}" '
                             f'r="{celda / 2 - 0.5}" fill="{color}"/>')
    # grupos: un patron por cliente bajo la rejilla
    yb = y0 + 5 * (celda + 14) + 4
    for j in range(5):
        x = 214 + 8 + 2 * j * (celda + gap)
        c.append(linea(x, yb, x + 2 * celda + gap, yb, color=SUAVE, grosor=3))
        c.append(texto(x + celda + 1, yb + 15, "ABCDE"[j], tam=12, color=SUAVE))
    c.append(texto(16, PA_H - 50, "● entrenamiento   ▲ validación   ■ prueba (cerrada)",
                   tam=12, anclaje="start", color=TEXTO))
    c.append(texto(16, PA_H - 30, "por grupos: cada cliente (A–E) queda entero de un lado",
                   tam=12, anclaje="start", color=SUAVE))
    c.append(texto(16, PA_H - 12, "temporal: el entrenamiento crece y se valida el bloque "
                   "que sigue", tam=12, anclaje="start", color=SUAVE))
    aria = ("Tres maneras de armar cinco pliegues: al azar, la validación cae dispersa; por "
            "grupos, cada cliente entero queda de un solo lado; temporal, el entrenamiento "
            "crece hacia la derecha, la validación es el bloque siguiente y la prueba es el "
            "último tramo, cerrada")
    return svg(PA_W, PA_H, aria, "Tres maneras de armar cinco pliegues", c)


# ---------------------------------------------- ml-c5-momento-decision ---
MD_W, MD_H = 600, 300


def fig_momento_decision():
    c = [texto(16, 28, "Cada columna tiene un momento en que se conoce", tam=17, peso="700",
               anclaje="start")]
    y = 120
    c.append(flecha(24, y, 580, y, color=SUAVE))
    eventos = [(60, "se recibe"), (220, "sale"), (360, "llega"), (500, "el cliente califica")]
    for x, nombre in eventos:
        c.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{TEXTO}"/>')
        c.append(texto(x, y - 16, nombre, tam=13))
    # marca de prediccion
    c.append(linea(110, 60, 110, 270, color=ACENTO, grosor=3))
    c.append(texto(116, 72, "aquí se predice", tam=13, color=ACENTO, anclaje="start",
                   peso="700"))
    antes = ["distancia", "hora", "lluvia"]
    for i, nom in enumerate(antes):
        yy = 160 + i * 34
        c.append(caja(20, yy, 80, 26, relleno=PANEL, borde=CIAN, radio=6))
        c.append(texto(60, yy + 18, nom, tam=12, fuente=gen.MONO))
    c.append(texto(60, 268, "antes", tam=12, color=CIAN, peso="700"))
    despues = [(360, "minutos_reales"), (500, "calificacion")]
    for x, nom in despues:
        c.append(linea(x, y + 6, x, 180, color=ROSA, grosor=1.5, guiones="4 3"))
        c.append(caja(x - 62, 182, 124, 28, relleno=FONDO, borde=ROSA, radio=6,
                      guiones="6 4"))
        c.append(texto(x, 201, nom, tam=12, fuente=gen.MONO, color=ROSA))
    c.append(texto(430, 240, "después: no existen cuando predices", tam=12, color=ROSA,
                   peso="700"))
    aria = ("Línea del tiempo de un pedido: se recibe, sale, llega, el cliente califica. Cinco "
            "columnas: tres se conocen antes de predecir (distancia, hora, lluvia) y dos "
            "después (minutos reales y calificación)")
    return svg(MD_W, MD_H, aria, "Cada columna tiene un momento en que se conoce", c)


# ----------------------------------------------------------- ml-c5-tuberia ---
TU_W, TU_H = 600, 380


def _paso(x, y, w, lineas, borde=LINEA, relleno=PANEL):
    h = 18 + 16 * len(lineas)
    out = [caja(x, y, w, h, relleno=relleno, borde=borde, radio=8)]
    out += _renglones(x + w / 2, y + 22, lineas, tam=12, salto=16)
    return out


def fig_tuberia():
    c = [texto(16, 28, "Dónde se ajusta cada pieza", tam=17, peso="700", anclaje="start")]
    # mal
    c.append(texto(16, 62, "mal: todo se ajusta antes de separar", tam=14, peso="700",
                   color=ROSA, anclaje="start"))
    c += _paso(16, 76, 110, ["todas", "las filas"])
    c += _paso(156, 76, 150, ["imputar, escalar,", "elegir variables"], borde=ROSA)
    c += _paso(336, 76, 100, ["separar"])
    c += _paso(466, 76, 118, ["modelo"])
    for a, b in ((126, 156), (306, 336), (436, 466)):
        c.append(flecha(a + 2, 96, b - 4, 96, color=SUAVE))
    # bien
    c.append(texto(16, 168, "bien: separar primero; en cada pliegue, ajustar con su "
                   "entrenamiento", tam=14, peso="700", color=VERDE, anclaje="start"))
    c += _paso(16, 186, 100, ["separar"])
    c.append(caja(140, 180, 444, 150, relleno="none", borde=VERDE, radio=12, grosor=1.5,
                  guiones="6 4"))
    c.append(texto(152, 198, "en cada pliegue m", tam=12, color=VERDE, anclaje="start"))
    c += _paso(156, 208, 120, ["entrenamiento", "del pliegue"], borde=CIAN)
    c += _paso(316, 208, 252, ["imputar, escalar, elegir", "variables y el modelo"])
    c += _paso(156, 280, 120, ["su validación"], borde=ORO)
    c.append(flecha(118, 210, 152, 226, color=SUAVE))
    c.append(flecha(278, 228, 312, 228, color=ACENTO, grosor=2.5))
    c.append(texto(296, 252, "ajustar", tam=12, color=ACENTO))
    c.append(flecha_g(440, 262, 280, 296, color=SUAVE, grosor=2))
    c.append(texto(420, 300, "aplicar sin reajustar", tam=12, color=SUAVE, anclaje="start"))
    c.append(linea(24, 352, 64, 352, color=ACENTO, grosor=2.5))
    c.append(texto(70, 356, "ajustar (sólida)", tam=12, anclaje="start"))
    c.append(linea(210, 352, 250, 352, color=SUAVE, grosor=2, guiones="6 4"))
    c.append(texto(256, 356, "aplicar (discontinua)", tam=12, anclaje="start"))
    aria = ("Arriba, todo se ajusta antes de separar: imputar, escalar y elegir variables con "
            "todas las filas. Abajo, dentro de cada pliegue: se ajusta con su entrenamiento y "
            "se aplica sin reajustar a su validación")
    return svg(TU_W, TU_H, aria, "Dónde se ajusta cada pieza", c)


# ------------------------------------------------------------ ml-c5-receta ---
RE_W, RE_H = 600, 560


def fig_receta():
    c = [texto(16, 28, "La receta, de punta a punta", tam=17, peso="700", anclaje="start")]
    x, w = 96, 240
    pasos = [("paso 0", ["¿dónde y cuándo se usará?"]), ("paso 1", ["métrica y meta"]),
             ("paso 2", ["separar como se usará y", "apartar la prueba"]),
             ("paso 3", ["benchmark"]),
             ("paso 4", ["tubería de punta a punta,", "modelo simple"]),
             ("paso 5", ["analizar el error", "en validación"]),
             ("paso 6", ["cambiar una cosa"]),
             ("paso 7", ["fijar; reajustar sin las reservas;", "recalibración, τ y corte",
                         "en su reserva"]),
             ("al final", ["abrir la prueba una vez"])]
    caj = {}
    y = 48
    for nom, lineas in pasos:
        h = 22 + 15 * len(lineas)
        borde = ROSA if nom == "al final" else (ORO if nom in ("paso 5", "paso 6") else LINEA)
        c.append(caja(x, y, w, h, relleno=PANEL, borde=borde, radio=8))
        c.append(texto(x + 10, y + 15, nom, tam=12, color=SUAVE, anclaje="start"))
        for k, l in enumerate(lineas):
            c.append(texto(x + 10, y + 30 + 15 * k, l, tam=12, anclaje="start"))
        caj[nom] = (y, h)
        y += h + 12
    nombres = [n for n, _ in pasos]
    for a, b in zip(nombres[:-1], nombres[1:]):
        ya, ha = caj[a]
        yb, _ = caj[b]
        c.append(flecha(x + w / 2, ya + ha, x + w / 2, yb - 2, color=SUAVE))
    # lazo 6 -> 5, a la izquierda de los pasos
    y5, h5 = caj["paso 5"]
    y6, h6 = caj["paso 6"]
    c.append(f'<path d="M {x} {y6 + h6 / 2} C {x - 34} {y6 + h6 / 2} {x - 34} {y5 + h5 / 2} '
             f'{x - 4} {y5 + h5 / 2}" fill="none" stroke="{ORO}" stroke-width="2" '
             f'marker-end="url(#s)"/>')
    c += _renglones(16, y5 + 4, ["lazo:", "validación", "o CV ▲"], tam=12, color=ORO,
                    anclaje="start", salto=15)
    # la prueba y las reservas, junto al paso 2
    y2, _ = caj["paso 2"]
    xr, wr = 352, 232
    c.append(caja(xr, y2, wr, 34, relleno=FONDO, borde=ROSA, radio=8, grosor=2.5))
    c.append(texto(xr + 10, y2 + 22, "■ prueba: cerrada", tam=12, color=ROSA,
                   anclaje="start", peso="700"))
    c.append(flecha(x + w + 2, y2 + 17, xr - 4, y2 + 17, color=SUAVE))
    yr = y2 + 56
    c.append(texto(xr, yr, "reservas (si las usas), cerradas", tam=12, anclaje="start"))
    piezas = [("cal", "se aparta primero", "solo el corte conformal", VERDE),
              ("val_a", "recalibración y τ", "no reporta ninguna cifra", ORO),
              ("val_b", "método de recalibración", "diagnóstico y benchmark", CIAN)]
    yy = yr + 10
    centros = {}
    for nom, l1, l2, col in piezas:
        c.append(caja(xr, yy, wr, 44, relleno=PANEL, borde=col, radio=6))
        c.append(texto(xr + 8, yy + 18, [(nom, {"peso": "700", "color": col}), " · " + l1],
                       tam=12, anclaje="start"))
        c.append(texto(xr + 8, yy + 35, l2, tam=12, anclaje="start", color=SUAVE))
        centros[nom] = yy + 22
        yy += 50
    c.append(texto(xr, yy + 8, "al azar · por grupos · por tiempo:", tam=12, color=SUAVE,
                   anclaje="start"))
    c.append(texto(xr, yy + 24, "las reservas también", tam=12, color=SUAVE, anclaje="start"))
    # flechas punteadas del lazo a val_a y val_b (ninguna a cal)
    for nom in ("val_a", "val_b"):
        c.append(flecha_g(x + w + 2, y6 + h6 / 2, xr - 4, centros[nom], color=SUAVE,
                          grosor=1.5, guiones="2 4"))
    c += _renglones(xr, y6 + 16, ["τ en val_a, sobre la probabilidad", "ya recalibrada; método y",
                                  "diagnóstico en val_b"], tam=12, color=SUAVE, anclaje="start",
                    salto=15)
    # union discontinua de las reservas con el cierre
    y7, h7 = caj["paso 7"]
    c.append(flecha_g(xr + wr / 2, y6 + 66, x + w + 4, y7 + h7 / 2, color=SUAVE, grosor=1.5))
    aria = ("La receta en siete pasos; el lazo usa validación; las reservas se apartan con la "
            "prueba, como se usará el modelo: cal primero, que solo da el corte conformal; "
            "val_a ajusta la recalibración y elige el umbral, y no reporta ninguna cifra; val_b "
            "elige el método de recalibración, diagnostica y mide el benchmark; el reajuste "
            "final no toca las reservas; la prueba se abre una vez al final")
    return svg(RE_W, RE_H, aria, "La receta, de punta a punta", c)


# --------------------------------------------------- ml-c5-phi-aprendida ---
PH_W, PH_H = 600, 320


def fig_phi_aprendida():
    c = [texto(16, 28, "De la φ a mano a la φ aprendida", tam=17, peso="700", anclaje="start")]
    for fila, (y, rot, caja_txt, sub, sombreada) in enumerate((
            (64, "las clases 1 a 4", ["polares, potencias,", "dummies"], "la eliges tú", False),
            (188, "una red", ["unidades", "σ(γ₀,ₕ + γₕᵀx)"], "se aprende de los datos", True))):
        c.append(texto(16, y, rot, tam=14, peso="700", anclaje="start",
                       color=ACENTO if sombreada else CIAN))
        yc = y + 16
        c.append(caja(24, yc + 18, 70, 50, relleno=PANEL, borde=LINEA, radio=8))
        c.append(texto(59, yc + 49, "x", tam=18, estilo="italic"))
        c.append(flecha(96, yc + 43, 170, yc + 43, color=SUAVE))
        relleno = mezclar(ACENTO, 0.25) if sombreada else PANEL
        c.append(caja(174, yc + 4, 200, 78, relleno=relleno,
                      borde=ACENTO if sombreada else CIAN, radio=10,
                      guiones="6 4" if sombreada else None))
        c.append(texto(274, yc + 24, "φ", tam=17, peso="700", estilo="italic"))
        c += _renglones(274, yc + 44, caja_txt, tam=13, salto=16)
        c.append(texto(274, yc + 100, sub, tam=12, color=ACENTO if sombreada else CIAN))
        c.append(flecha(376, yc + 43, 440, yc + 43, color=SUAVE))
        c.append(caja(444, yc + 18, 140, 50, relleno=PANEL, borde=LINEA, radio=8))
        c.append(texto(514, yc + 49, ["β", ("ᵀ", {}), "φ(", ("x", _IT), ")"], tam=16))
    c.append(texto(16, PH_H - 14, "con los γ fijos, la salida es lineal en β", tam=13,
                   color=SUAVE, anclaje="start"))
    aria = ("Arriba, en las clases 1 a 4, la φ la eliges tú; abajo, unidades sigmoides se "
            "aprenden; con ellas fijas, la salida es lineal en β")
    return svg(PH_W, PH_H, aria, "De la φ a mano a la φ aprendida", c)


# ====================================================== graficas de datos ===

def _num(v, d=2):
    return f"{float(v):.{d}f}".replace("-", "−")


# ------------------------------------------------------ ml-c5-detectores ---

def fig_detectores():
    ml, cif = gen.ml_lab(), _cif()
    det = cif.datos_detectores()
    a = cif.cifras_c5_adversarial()
    resultados = {k: ml.validacion_adversarial(det["ent"], det["usos"][k],
                                               columnas=cif.COLUMNAS_DET) for k in
                  ("nada", "deriva")}
    ks = {k: ml.ks_por_variable(det["ent"], det["usos"][k], columnas=["distancia", "hora"])
          for k in ("nada", "deriva")}
    res = {"nada": cif.modelo_residuales("sin"), "deriva": cif.modelo_residuales("con")}

    def dibujar(fig, ejes):
        for col, (k, rot) in enumerate((("nada", "mismo proceso"),
                                         ("deriva", "el mes que viene"))):
            a0, a1, a2 = ejes[0][col], ejes[1][col], ejes[2][col]
            ml.dibujar_adversarial(resultados[k], ax=a0, tema="sitio")
            ml.dibujar_ks(ks[k], ax=a1, tema="sitio")
            m, v = res[k]
            ml.dibujar_residual_tiempo(m, v, ax=a2, tema="sitio")
            c = a[f"{k}_bosque"]
            _titulo(a0, f"{rot}\nadversarial: pérdida log {_num(c['log_loss'], 3)}\n"
                    f"(su benchmark: {_num(c['benchmark'], 3)})", 8.5)
            a0.set_xlabel("Pr(viene del uso), fuera de pliegue")
            a0.set_ylabel("densidad" if col == 0 else "")
            _titulo(a1, "KS por variable", 8.5)
            a1.set_xlabel("KS")
            _titulo(a2, "residuales de validación contra t" + (
                "\n(ruido con memoria)" if k == "deriva" else "\n(ruido sin memoria)"), 8.5)
            for ax in (a0, a1, a2):
                ley = ax.get_legend()
                if ley is not None:
                    ley.remove()
            if col == 1:
                a2.set_ylabel("")

    n, d = a["cita"]["nada_bosque"], a["cita"]["deriva_bosque"]
    au = cif.cifras_c5_autocorrelacion()["cita"]
    aria = (f"Con el mismo proceso, la validación adversarial queda en su benchmark (pérdida "
            f"logarítmica {n['log_loss']} contra {n['benchmark']}, {n['senal']}), KS no "
            f"separa las escaleras y los residuales no tienen memoria (rezago 1: "
            f"{au['rezago1_sin']}); con deriva el mes que viene, la adversarial baja a "
            f"{d['log_loss']} ({d['senal']}), la escalera de distancia se separa y, con ruido "
            f"con memoria, los residuales hacen ondas (rezago 1: {au['rezago1_con']}); la "
            f"banda de autocorrelación es aproximada")
    return _grafica(dibujar, aria, "Tres detectores, sin y con cambio", 8.2, 3, 2)


# -------------------------------------------------------- ml-c5-cv-miente ---

def tabla_cv_miente():
    import pandas as pd
    cif = _cif()
    r = cif.cifras_c5_cv_miente()["res"]
    filas = []
    for caso, contrato, sep in ((14, "clientes que repiten", "por grupos"),
                                (13, "días seguidos", "temporal")):
        for nombre, rot in (("clase2", "el de la clase 2"), ("lineal", "lineal en x")):
            v = r[(caso, nombre)]
            for separacion, clave in (("al azar", "azar"), (sep, "estructurada")):
                filas.append({"modelo": rot, "contrato": contrato, "separacion": separacion,
                              "estimado": v[clave][0], "R": v["R"][0], "benchmark": float("nan")})
    return pd.DataFrame(filas)


def fig_cv_miente():
    cif = _cif()
    r = cif.cifras_c5_cv_miente()["res"]
    np = _np()

    def dibujar(fig, ejes):
        for ax, (caso, rot, sep) in zip(ejes, ((14, "clientes que repiten", "por grupos"),
                                               (13, "días seguidos", "temporal"))):
            xs = np.arange(2)
            for j, (nombre, etiqueta) in enumerate((("clase2", "el de la clase 2"),
                                                    ("lineal", "lineal en x"))):
                v = r[(caso, nombre)]
                for k, (clave, color, marca, txt) in enumerate((
                        ("azar", ORO, "^", "CV al azar"),
                        ("estructurada", mezclar(ORO, 0.55), "v", f"CV {sep}"))):
                    med, q1, q3 = v[clave]
                    x = j + (k - 0.5) * 0.28
                    ax.bar(x, med, width=0.26, color=color, edgecolor=ORO,
                           hatch="//" if k else None, label=txt if j == 0 else None)
                    ax.plot([x, x], [q1, q3], color=TEXTO, lw=1.2)
                Rm = v["R"][0]
                ax.plot([j - 0.42, j + 0.42], [Rm, Rm], ls="--", color=CREMA, lw=2,
                        label="R (despliegue)" if j == 0 else None)
            ax.set_xticks(xs)
            ax.set_xticklabels(["el de la clase 2", "lineal en x"])
            ax.set_ylabel("error cuadrático (min²)")
            ax.set_ylim(0, 1.15 * max(max(r[(caso, n)][k][2] for k in ("azar", "estructurada",
                                                                          "R"))
                                      for n in ("clase2", "lineal")))
            _titulo(ax, rot)
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=1, fontsize=8)

    c = cif.cifras_c5_cv_miente()["cita"]
    aria = (f"Con el modelo que ve la cercanía, la CV al azar promete "
            f"{c['c14_clase2']['azar']} con clientes que repiten y los clientes nuevos dan "
            f"{c['c14_clase2']['R']}; en días seguidos, {c['c13_clase2']['azar']} contra "
            f"{c['c13_clase2']['R']}. Con el lineal en x, {c['c14_lineal']['azar']} contra "
            f"{c['c14_lineal']['R']} y {c['c13_lineal']['azar']} contra {c['c13_lineal']['R']}. "
            f"Cada barra es la mediana de {cif.REPETICIONES['cv_miente']} semillas, con su "
            f"rango intercuartil")
    return _grafica(dibujar, aria, "La validación cruzada al azar miente con un modelo que "
                    "ve la cercanía", 4.4, 1, 2)


# ------------------------------------------------------------ ml-c5-fugas ---

def tabla_fugas():
    import pandas as pd
    cif = _cif()
    f = cif.cifras_c5_fugas()
    rotulos = {"ninguna": "ninguna", "posterior": "calificación\nposterior",
               "preprocesar_antes": "escalar e\nimputar antes",
               "duplicados": "pedidos\nduplicados",
               "seleccion_previa": "elegir variables\nantes (caso 26)"}
    filas = [(rotulos[t], 1.0, f[t]["cv"][0], f[t]["uso"][0], f[t]["cv"][0] - f[t]["uso"][0])
             for t, _ in cif.RUTAS]
    tabla = pd.DataFrame(filas, columns=["tipo", "intensidad", "estimado", "en_uso", "inflado"])
    tabla.attrs["criterio"] = "mcc"
    return tabla


def fig_fugas():
    ml, cif = gen.ml_lab(), _cif()
    tabla = tabla_fugas()

    def dibujar(fig, ax):
        ml.dibujar_fugas(tabla, ax=ax, tema="sitio")
        ax.legend(loc="upper right")
        ax.tick_params(axis="x", labelsize=8)
        _titulo(ax, "Aquí y es «llegó tarde»: MCC de la CV contra MCC en el despliegue")

    c = cif.cifras_c5_fugas()["cita"]
    aria = (f"Aquí y es llegó tarde. Sin fuga, la CV promete un MCC de {c['ninguna']['cv']} y "
            f"en el despliegue da {c['ninguna']['uso']}. Con la calificación la CV promete "
            f"{c['posterior']['cv']} y en el despliegue da {c['posterior']['uso']}; escalar e "
            f"imputar antes, {c['preprocesar_antes']['cv']} contra "
            f"{c['preprocesar_antes']['uso']}; pedidos duplicados, {c['duplicados']['cv']} "
            f"contra {c['duplicados']['uso']}; elegir variables antes (500 columnas de ruido, "
            f"100 pedidos), {c['seleccion_previa']['cv']} contra "
            f"{c['seleccion_previa']['uso']}. Cada punto es la mediana de "
            f"{cif.REPETICIONES['fugas']} semillas; benchmark en 0")
    return _grafica(dibujar, aria, "Cuánto infla cada fuga", 4.0)


# -------------------------------------------------------- ml-c5-imputacion ---

def fig_imputacion():
    cif = _cif()
    r = cif.cifras_c5_imputacion()
    np = _np()

    def dibujar(fig, ejes):
        for ax in list(fig.axes):
            ax.remove()
        m = fig.subplot_mosaic([["h", "b"], ["p", "p"]])
        a0, a1, a2 = m["h"], m["b"], m["p"]
        for ax in (a0, a1, a2):
            ax.set_facecolor(PANEL)
            for lado in ax.spines.values():
                lado.set_color(LINEA)
            ax.tick_params(colors=SUAVE)
            ax.xaxis.label.set_color(TEXTO)
            ax.yaxis.label.set_color(TEXTO)
        ent = r["ent"]
        x = ent["distancia"].to_numpy(float)
        falta = ent["distancia_falta"].to_numpy(float) > 0
        a0.hist(x, bins=24, color=CIAN, edgecolor=FONDO)
        a0.plot(x[falta], np.full(falta.sum(), -4), "|", color=ROSA, ms=7)
        a0.set_xlabel("distancia imputada (km); franja rosa: faltaba")
        _titulo(a0, f"un pico en la mediana: {r['cita']['pico']} de las filas", 9)
        a1.bar([0, 1], [r["L_sin"], r["L_con"]], color=[mezclar(ORO, 0.55), ORO],
               edgecolor=ORO)
        a1.set_xticks([0, 1])
        a1.set_xticklabels(["sin indicadora", "con indicadora"])
        a1.set_ylabel("L en validación (min²)")
        _titulo(a1, "faltar informa", 9)
        d = r["datos"].ent
        ok = ~d["distancia"].isna()
        a2.plot(d.loc[ok, "distancia"], d.loc[ok, "y"], "o", color=CIAN, ms=2)
        a2.plot(np.full((~ok).sum(), -5.0), d.loc[~ok, "y"], "s", color=ROSA, ms=2)
        xs = np.linspace(-5, 6, 50)
        for b, col, ls in ((r["pendiente_mediana"], CIAN, "-"),
                           (r["pendiente_centinela"], ROSA, "--")):
            y0 = float(d.loc[ok, "y"].mean()) - b * float(d.loc[ok, "distancia"].mean())
            a2.plot(xs, y0 + b * xs, ls=ls, color=col, lw=2)
        a2.set_xlabel("distancia (km)")
        _titulo(a2, f"pendiente: {_num(r['pendiente_mediana'])} con la mediana,\n"
                f"{_num(r['pendiente_centinela'])} con el centinela −5", 9)

    c = r["cita"]
    aria = (f"Imputar con la mediana ({c['mediana']} km) deja un pico con el {c['pico']} de las "
            f"filas; con la indicadora, el error en validación baja de {c['L_sin']} a "
            f"{c['L_con']} porque faltar informa; el centinela −5 tuerce la pendiente de "
            f"distancia a {c['pendiente_centinela']}, contra {c['pendiente_mediana']} con la "
            f"mediana")
    return _grafica(dibujar, aria, "Imputar: la mediana, la indicadora y el centinela", 6.0,
                    2, 2)


# ----------------------------------------------------- ml-c5-trampa-dummy ---
TD_W, TD_H = 600, 360


def fig_trampa_dummy():
    cif = _cif()
    r = cif.cifras_c5_dummy()
    c = [texto(16, 28, "La trampa de la dummy", tam=17, peso="700", anclaje="start"),
         texto(16, 48, "seis pedidos; las tres dummies suman la columna de unos", tam=12,
               color=SUAVE, anclaje="start")]
    cols = list(r["nombres"])
    x0, y0, cw, rh = 16, 76, 54, 26
    for j, nm in enumerate(cols):
        c.append(texto(x0 + j * cw + cw / 2, y0, nm, tam=12, fuente=gen.MONO,
                       color=ORO if nm in ("norte", "centro", "sur") else TEXTO))
    for i in range(6):
        for j, v in enumerate(r["Phi"][i]):
            x, y = x0 + j * cw, y0 + 8 + i * rh
            dummy = cols[j] in ("norte", "centro", "sur")
            c.append(caja(x + 2, y, cw - 4, rh - 4,
                          relleno=mezclar(ORO, 0.3) if dummy and v else PANEL,
                          borde=ORO if dummy else LINEA, radio=4, grosor=1))
            c.append(texto(x + cw / 2, y + 16, f"{v:g}", tam=12))
    yb = y0 + 8 + 6 * rh + 22
    c.append(texto(x0 + 2.5 * cw, yb, "norte + centro + sur = 1", tam=13, color=ORO, peso="700"))
    c.append(texto(x0 + 2.5 * cw, yb + 20, "rango " + r["cita"]["rango"] + " columnas",
                   tam=12, color=SUAVE))
    xr = 310
    c.append(texto(xr, y0, "dos β̂ con las mismas ŷ", tam=13, peso="700", anclaje="start"))
    for k, (nombre, clave, col) in enumerate((("β̂ (norma mínima)", "b1", CIAN),
                                              ("β̂ + 10·(1, −1, −1, −1, 0)", "b2", ORO),
                                              ("ridge, μ = 0.1", "ridge", ACENTO))):
        y = y0 + 24 + k * 64
        c.append(texto(xr, y, nombre, tam=12, color=col, anclaje="start"))
        c.append(texto(xr, y + 20, "(" + ", ".join(v.replace("-", "−")
                                                  for v in r["cita"][clave]) + ")",
                       tam=12, anclaje="start", fuente=gen.MONO))
    yh = r["cita"]["yh"]
    c.append(texto(xr, y0 + 206, "ŷ = (" + ", ".join(yh[:3]) + ",", tam=12,
                   anclaje="start", fuente=gen.MONO))
    c.append(texto(xr + 36, y0 + 222, ", ".join(yh[3:]) + ")", tam=12,
                   anclaje="start", fuente=gen.MONO))
    c.append(texto(xr, y0 + 244, "las dos primeras: mismas predicciones", tam=12,
                   color=SUAVE, anclaje="start"))
    c.append(texto(xr, y0 + 262, "ridge: un mínimo único, otro ŷ", tam=12, color=SUAVE,
                   anclaje="start"))
    aria = ("Las tres dummies suman la columna de unos (rango " + r["cita"]["rango"] +
            "); dos β distintos dan las mismas predicciones; ridge tiene un mínimo único, "
            "con predicciones algo distintas")
    return svg(TD_W, TD_H, aria, "La trampa de la dummy", c)


# ------------------------------------------------------ ml-c5-diagnostico ---

def fig_diagnostico():
    cif = _cif()
    r = cif.cifras_c5_diagnostico()
    ns = list(cif.NS_DIAG)

    def serie(ax, dic, color, ls, marca, etiqueta):
        med = [dic[n][0] for n in ns]
        q1 = [dic[n][1] for n in ns]
        q3 = [dic[n][2] for n in ns]
        ax.fill_between(ns, q1, q3, color=mezclar(color, 0.25, PANEL), lw=0)
        ax.plot(ns, med, ls=ls, marker=marca, color=color, lw=2, label=etiqueta)

    def dibujar(fig, ejes):
        a0, a1 = ejes
        serie(a0, r["izq"]["L_ent"], CIAN, "-", "o", "L_ent")
        serie(a0, r["izq"]["azar"], ORO, "-", "^", "CV al azar")
        serie(a0, r["izq"]["grupos"], ORO, "--", "v", "CV por grupos")
        a0.set_xscale("log")
        a0.set_xlabel("n")
        a0.set_ylabel("error cuadrático (min²)")
        _titulo(a0, "la brecha que miente", 9)
        a0.legend(loc="upper right")
        for nombre, col in (("sesgo", CIAN), ("piso", ORO)):
            d = r["der"][nombre]
            serie(a1, d["cv"], col, "-", "^", f"CV ({'lejos del piso' if nombre == 'sesgo' else 'sobre el piso'})")
            a1.axhline(d["piso"], color=col, ls=":", lw=2)
        a1.set_xscale("log")
        a1.set_xlabel("n")
        _titulo(a1, "altos y juntos: ¿sesgo o piso?", 9)
        a1.legend(loc="upper right")

    c = r["cita"]
    aria = (f"Con CV al azar la brecha parece chica (vecinos que reconocen al cliente: "
            f"{c['azar']} contra L_ent {c['L_ent']} con el n mayor) y con CV por grupos la "
            f"curva sube a {c['grupos']}; altos y juntos puede ser sesgo o el piso: un "
            f"proceso queda {c['sesgo_sobre_piso']} sobre su piso y el otro "
            f"{c['piso_sobre_piso']}. Mediana de {c['repeticiones']} muestras, banda del "
            f"rango intercuartil; el piso es la línea punteada")
    return _grafica(dibujar, aria, "Auditar la evaluación antes de leer la curva", 3.4, 1, 2)


# -------------------------------------------------- ml-c5-arbol-escalones ---

def fig_arbol_escalones():
    ml, cif = gen.ml_lab(), _cif()
    r = cif.cifras_c5_arbol()
    d = cif.datos_diagonal()

    def dibujar(fig, ejes):
        for ax, p in zip(ejes, cif.PROFUNDIDADES_ARBOL):
            ml.dibujar_frontera(cif.arbol_diagonal(p), d.val, ax=ax, tema="sitio")
            ax.plot([0, 1], [0, 1], color=VERDE, lw=2)
            _titulo(ax, f"profundidad {p}\nMCC en validación {r['cita']['mcc'][str(p)]}", 9)
            ley = ax.get_legend()
            if ley is not None:
                ley.remove()

    m = r["cita"]["mcc"]
    aria = (f"La frontera diagonal x2 > x1 aproximada con escalones: con profundidad 1 el "
            f"MCC en validación es {m['1']}, con 3 es {m['3']} y con 6 es {m['6']}; la "
            f"logística, con un solo corte diagonal, llega a {r['cita']['logistica']}")
    return _grafica(dibujar, aria, "Un árbol aproxima la diagonal con escalones", 2.9, 1, 3)


# ------------------------------------------------ ml-c5-familias-capacidad ---

def fig_familias_capacidad():
    cif = _cif()
    r = cif.cifras_c5_familias()
    d = cif.datos_familias()
    np = _np()
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import GradientBoostingRegressor

    def dibujar(fig, ejes):
        dev = d.ent
        X, y = dev[["x"]].to_numpy(float), dev["y"].to_numpy(float)
        xs = np.linspace(0, 6, 300)[:, None]
        a = ejes[0][0]
        a.plot(X[:, 0], y, ".", color=GRIS, ms=3)
        rng = np.random.default_rng(0)
        preds = []
        for b in range(3):
            idx = rng.integers(0, len(y), len(y))
            t = DecisionTreeRegressor(max_depth=4, random_state=b).fit(X[idx], y[idx])
            p = t.predict(xs)
            preds.append(p)
            a.plot(xs[:, 0], p, color=CIAN, lw=0.9)
        a.plot(xs[:, 0], np.mean(preds, 0), color=ORO, lw=2.5, label="promedio de 3")
        _titulo(a, "bosque: promediar", 8.5)
        a.legend(loc="lower right")
        a = ejes[0][1]
        a.plot(X[:, 0], y, ".", color=GRIS, ms=3)
        for e, ls in ((1, ":"), (5, "--"), (50, "-")):
            g = GradientBoostingRegressor(n_estimators=e, learning_rate=0.1, max_depth=2,
                                          random_state=0).fit(X, y)
            a.plot(xs[:, 0], g.predict(xs), ls=ls, color=ACENTO, lw=2, label=f"{e} etapas")
        _titulo(a, "boosting: sumar", 8.5)
        a.legend(loc="lower right")
        a = ejes[1][0]
        ps = list(cif.PROF_CURVA)
        a.plot(ps, [r["cv_arbol"][p].media for p in ps], "^-", color=ORO, label="CV")
        a.set_xlabel("profundidad")
        a.set_ylabel("CV (min²)")
        _titulo(a, f"árbol: U, elige {r['profundidad']}", 8.5)
        a = ejes[1][1]
        Bs = list(cif.B_CURVA)
        for s in range(cif.REPETICIONES["familias"]):
            a.plot(Bs, [r["bosque"][B][s] for B in Bs], color=GRIS, lw=1)
        a.plot(Bs, [np.median(r["bosque"][B]) for B in Bs], "^-", color=ORO, lw=2)
        a.set_xscale("log")
        a.set_xlabel("árboles B")
        _titulo(a, "bosque: se estabiliza", 8.5)
        a = ejes[1][2]
        es = list(cif.ETAPAS_CURVA)
        a.plot(es, [r["cv_boost"][e].media for e in es], "^-", color=ORO)
        a.set_xscale("log")
        a.set_xlabel("etapas (ν = 0.1)")
        _titulo(a, f"boosting: U, elige {r['etapas']}", 8.5)
        ejes[0][2].axis("off")

    c = r["cita"]
    aria = (f"Promediar árboles suaviza; boosting suma correcciones. Abajo, con la misma "
            f"partición: el árbol hace U y la CV elige profundidad {c['profundidad']}; el bosque "
            f"se estabiliza (con B = 10 las cinco semillas difieren {c['rango_10']} y con B = 200 "
            f"{c['rango_200']}); boosting hace U y elige {c['etapas']} etapas")
    return _grafica(dibujar, aria, "Otras familias: el mecanismo y su perilla", 4.8, 2, 3)


# -------------------------------------------------------------- ml-c5-cybenko ---

def fig_cybenko():
    ml, cif = gen.ml_lab(), _cif()
    r = cif.cifras_c5_cybenko()
    np = _np()

    def dibujar(fig, ejes):
        a0, a1 = ejes
        ml.dibujar_sigmoides(cif.f_cybenko, r["ajustes"], ax=a0, tema="sitio")
        _titulo(a0, "existe: sin ruido", 9)
        ns = list(cif.NS_ANILLOS)
        for m, col, ls, rot in (("polar", CIAN, "-", "φ polar (a mano)"),
                                ("aprendida", ACENTO, "--", "10 sigmoides aprendidas")):
            a1.plot(ns, [r["curvas"][m][n] for n in ns], marker="^", ls=ls, color=col, lw=2,
                    label=rot)
        a1.axhline(r["piso"], color=gen.color_rol("piso_bayes"), ls=":", lw=2, label="piso")
        a1.set_xscale("log")
        a1.set_xlabel("n")
        a1.set_ylabel("pérdida logarítmica (CV)")
        _titulo(a1, "se encuentra: los anillos", 9)
        a1.legend(loc="upper right")

    c = r["cita"]
    aria = (f"Sin ruido, el error máximo con 1, 3 y 10 sigmoides es {c['error']['1']}, "
            f"{c['error']['3']} y {c['error']['10']}; en los anillos, la φ polar llega a 15 % "
            f"del piso con {c['n_polar']} filas y la aprendida con {c['n_aprendida']}; cada "
            f"ajuste sin ruido es la mediana de cinco arranques, y cada punto de los anillos "
            f"la de tres")
    return _grafica(dibujar, aria, "Existe contra se encuentra", 3.4, 1, 2)


FIGURAS_C5_P1 = {
    "ml-c5-modelo-exitoso": fig_modelo_exitoso,
    "ml-c5-bolsas": fig_bolsas,
    "ml-c5-particiones": fig_particiones,
    "ml-c5-momento-decision": fig_momento_decision,
    "ml-c5-tuberia": fig_tuberia,
    "ml-c5-detectores": fig_detectores,
    "ml-c5-cv-miente": fig_cv_miente,
    "ml-c5-fugas": fig_fugas,
    "ml-c5-imputacion": fig_imputacion,
}

FIGURAS_C5_P2 = {
    "ml-c5-receta": fig_receta,
    "ml-c5-phi-aprendida": fig_phi_aprendida,
    "ml-c5-trampa-dummy": fig_trampa_dummy,
    "ml-c5-diagnostico": fig_diagnostico,
    "ml-c5-arbol-escalones": fig_arbol_escalones,
    "ml-c5-familias-capacidad": fig_familias_capacidad,
    "ml-c5-cybenko": fig_cybenko,
}

FIGURAS_C5 = {**FIGURAS_C5_P1, **FIGURAS_C5_P2}
