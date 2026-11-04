"""Figuras de la clase 2 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C2: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c2-", es un error.

Dueno: prog-c2 (lo creo vacio prog-lab en U.T3). Reglas para llenarlo:
- los diagramas conceptuales se escriben como SVG a mano con las primitivas
  y la paleta de gen_aprendizaje_maquina (marco, texto, caja, flecha, ROLES...);
- las graficas de datos se dibujan con las funciones dibujar_* de ml_lab y
  tema="sitio", y se convierten con gen.svg_de_matplotlib(fig, aria=...);
- ml_lab se pide con gen.ml_lab() dentro de la funcion de la figura, nunca
  al importar este modulo (importacion perezosa, contrato §7.1);
- ningun color de rol se copia como literal: se lee de gen.ROLES;
- las cifras que se dibujan salen de ml_lab o de tools/ml_cifras_c2.py.

Sus pruebas propias van en tools/test_figuras_ml_c2.py (sin prosa); las
guardas comunes, en tools/test_gen_aprendizaje_maquina.py.

Anclas por tramo (protocolo p5.2 §7.1, clase_2.md §10.11): el catalogo es la
suma de un dict por tramo (rapido, m, completo); cada rama escribe solo
dentro del ancla de su tramo. La rama de clase escribe el tramo rapido; la
subrama -m, el m; la -completo, el completo.

Lo que ml_lab dibuja y el sitio no admite se corrige aqui, despues de dibujar
y sin tocar ml_lab (el mismo arreglo que figuras_ml_c1): `_sin_opacidad`
hornea cada relleno translucido contra el panel.
"""
import re

import numpy as np

import gen_aprendizaje_maquina as gen
from gen_aprendizaje_maquina import (ACENTO, FONDO, LINEA, PANEL, SUAVE, TEXTO,
                                     _n, caja, flecha, linea, mezclar, svg, texto)

_IT = {"estilo": "italic"}
ENT = gen.color_rol("entrenamiento")
VAL = gen.color_rol("validacion")
PRU = gen.color_rol("prueba")
REAL = gen.color_rol("realidad")
VERDE = gen.color_rol("f_verdadera")
CIAN = gen.color_rol("f_estimada")
PISO = gen.color_rol("piso_bayes")
BENCH = gen.color_rol("benchmark")
# Ancho de las graficas de datos: 5.4 pulgadas = 388.8 puntos de viewBox, que
# a 600 px dan una escala de 1.54; asi la letra de 8 pt de ml_lab queda en
# 12.3 px (guarda comun de letra minima). Igual que figuras_ml_c1.
ANCHO_IN = 5.4


# ------------------------------------------------------------ utilidades ---

_ESTILO = re.compile(r'style="([^"]*)"')


def _sin_opacidad(texto_svg, fondo=PANEL):
    """Hornea cada fill/stroke translucido contra el panel y quita la opacidad
    (contrato §7.3: el sitio la prohibe). Copia de figuras_ml_c1."""
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


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return matplotlib, plt


def _grafica(dibujar, aria, titulo, alto_in, paneles=1, **subplots):
    """Arma una figura de datos con la paleta del sitio y la deja como SVG.

    Parte de los rcParams de fabrica (ml.tema() cambia el estado global de
    matplotlib y una figura no puede depender de quien corrio antes)."""
    matplotlib, plt = _plt()
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(gen.RC_SITIO)
        fig, ejes = plt.subplots(paneles, 1, figsize=(ANCHO_IN, alto_in), **subplots)
        dibujar(fig, ejes)
        fig.tight_layout()
        crudo = gen.svg_de_matplotlib(fig, aria, titulo=titulo, ancho=600)
    return _sin_opacidad(crudo)


def _leyenda(ax, renombrar=None, **kw):
    """Leyenda con el panel del sitio; renombrar={rotulo viejo: nuevo}."""
    kw.setdefault("fontsize", 9)
    if renombrar:
        h, r = ax.get_legend_handles_labels()
        kw["handles"], kw["labels"] = h, [renombrar.get(x, x) for x in r]
    ley = ax.legend(frameon=True, **kw)
    ley.get_frame().set_facecolor(PANEL)
    ley.get_frame().set_edgecolor(LINEA)
    for t in ley.get_texts():
        t.set_color(TEXTO)
    return ley


_SUB = {"color": "SUB"}


def tx(x, y, partes, tam=14, **kw):
    """texto() con subindices: un trozo (cadena, _SUB) baja la linea base y usa
    letra de 12 px (la minima de las guardas)."""
    t = texto(x, y, partes, tam=tam, **kw)
    return t.replace(' fill="SUB"', ' baseline-shift="sub" font-size="12"')


def _L(sub):
    """L con subindice (L_ent, L_val, ...)."""
    return [("L", _IT), (sub, _SUB)]


def _num(v, d=1):
    """Un numero como lo escribe la pagina (signo menos tipografico)."""
    return f"{v:.{d}f}".replace("-", "−")


def _pct(v):
    return f"{100 * v:.0f} %"


# Marcas de los roles (contrato §7.3) en los diagramas: entrenamiento ●,
# validacion ▲, prueba ■. El color nunca es la unica senal.

def _circulo(x, y, r=6, color=ENT):
    return f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{_n(r)}" fill="{color}"/>'


def _triangulo(x, y, r=7, color=VAL):
    pts = f"{_n(x)},{_n(y - r)} {_n(x + r * 0.95)},{_n(y + r * 0.7)} {_n(x - r * 0.95)},{_n(y + r * 0.7)}"
    return f'<polygon points="{pts}" fill="{color}"/>'


def _cuadrado(x, y, r=6, color=PRU):
    return (f'<rect x="{_n(x - r)}" y="{_n(y - r)}" width="{_n(2 * r)}" '
            f'height="{_n(2 * r)}" fill="{color}"/>')


def _candado(x, y, color=PRU, tam=1.0):
    """Un candado cerrado (cuerpo y arco), centrado en (x, y)."""
    w, h = 14 * tam, 11 * tam
    return (f'<path d="M {_n(x - 4.5 * tam)} {_n(y - h / 2)} v {_n(-4 * tam)} '
            f'a {_n(4.5 * tam)} {_n(4.5 * tam)} 0 0 1 {_n(9 * tam)} 0 v {_n(4 * tam)}" '
            f'fill="none" stroke="{color}" stroke-width="{_n(2 * tam)}"/>'
            f'<rect x="{_n(x - w / 2)}" y="{_n(y - h / 2)}" width="{_n(w)}" height="{_n(h)}" '
            f'rx="{_n(2 * tam)}" fill="{color}"/>')


def _llave_vertical(x, y1, y2, color=SUAVE, ancho=10):
    """Llave «}» que junta de y1 a y2, con la punta a la derecha en x + ancho."""
    m = (y1 + y2) / 2
    return (f'<path d="M {_n(x)} {_n(y1)} q {_n(ancho / 2)} 0 {_n(ancho / 2)} {_n(ancho / 2)} '
            f'L {_n(x + ancho / 2)} {_n(m - ancho / 2)} q 0 {_n(ancho / 2)} {_n(ancho / 2)} {_n(ancho / 2)} '
            f'q {_n(-ancho / 2)} 0 {_n(-ancho / 2)} {_n(ancho / 2)} L {_n(x + ancho / 2)} {_n(y2 - ancho / 2)} '
            f'q 0 {_n(ancho / 2)} {_n(-ancho / 2)} {_n(ancho / 2)}" fill="none" stroke="{color}" '
            f'stroke-width="1.6"/>')


def _llave_horizontal(x1, x2, y, color=SUAVE, alto=10):
    """Llave que junta de x1 a x2 por debajo, con la punta hacia abajo en y + alto."""
    m = (x1 + x2) / 2
    a = alto / 2
    return (f'<path d="M {_n(x1)} {_n(y)} q 0 {_n(a)} {_n(a)} {_n(a)} L {_n(m - a)} {_n(y + a)} '
            f'q {_n(a)} 0 {_n(a)} {_n(a)} q 0 {_n(-a)} {_n(a)} {_n(-a)} L {_n(x2 - a)} {_n(y + a)} '
            f'q {_n(a)} 0 {_n(a)} {_n(-a)}" fill="none" stroke="{color}" stroke-width="1.6"/>')


def _rejilla_pliegues(c, x0, y0, k=5, celda=34, alto=24, marcas=True, borde=LINEA,
                      relleno_ent=None, relleno_val=None):
    """La rejilla k×k de la CV con el mismo trazo que dibujar_pliegues de ml_lab:
    fila m = vuelta m; la celda m de la fila m es el pliegue de validacion
    (oro, triangulo); las demas, entrenamiento (cian, circulo)."""
    relleno_ent = mezclar(ENT, 0.30, PANEL) if relleno_ent is None else relleno_ent
    relleno_val = mezclar(VAL, 0.45, PANEL) if relleno_val is None else relleno_val
    for m in range(k):
        for j in range(k):
            x, y = x0 + j * celda, y0 + m * alto
            valida = j == m
            c.append(caja(x + 1, y + 1, celda - 2, alto - 2,
                          relleno=relleno_val if valida else relleno_ent,
                          borde=VAL if valida else borde, radio=3,
                          grosor=2 if valida else 1))
            if marcas:
                cx, cy = x + celda / 2, y + alto / 2
                c.append(_triangulo(cx, cy + 1, r=6) if valida
                         else _circulo(cx, cy, r=4.5))


# ===================================================================
# --- tramo rapido ---
# ===================================================================

# ----------------------------------------------- diagrama: ml-c2-dos-niveles ---
#
# P1 §1. Dos optimizaciones, una dentro de otra: la de afuera elige N con
# validacion; la de adentro, beta con N fijo y entrenamiento. Sin cifras.

DN_W, DN_H = 580, 360


def ml_c2_dos_niveles():
    c = []
    c.append(texto(16, 30, "Dos decisiones, dos conjuntos", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "una optimización dentro de otra: mira qué datos usa cada una",
                   tam=13, color=SUAVE, anclaje="start"))
    # caja de afuera
    c.append(caja(24, 70, 360, 222, relleno=PANEL, borde=VAL, radio=12, grosor=2.2))
    c.append(texto(40, 96, ["afuera: elige el grado ", ("N", _IT)], tam=15, peso="700",
                   anclaje="start", color=VAL))
    c.append(tx(40, 118, ["compara los ", ("N", _IT), " candidatos con "] + _L("val"),
                tam=13, anclaje="start"))
    # caja de adentro
    c.append(caja(48, 140, 312, 128, relleno=FONDO, borde=ENT, radio=10, grosor=2))
    c.append(texto(64, 166, ["adentro: elige ", ("β", _IT), " con ", ("N", _IT), " fijo"],
                   tam=15, peso="700", anclaje="start", color=ENT))
    c.append(tx(64, 188, ["minimiza "] + _L("ent") + ["(", ("β", _IT), ") con grado ≤ ",
                                                     ("N", _IT)], tam=13, anclaje="start"))
    c.append(texto(64, 212, ["devuelve ", ("β̂", _IT), "(", ("N", _IT), "), uno por candidato"],
                   tam=13, anclaje="start", color=SUAVE))
    c.append(texto(64, 236, ["afuera recibe los ", ("β̂", _IT), "(", ("N", _IT), ") ya ajustados"],
                   tam=13, anclaje="start", color=SUAVE))
    # los dos conjuntos, a la derecha
    for y, color, marca, nombre, que in (
            (112, VAL, "val", "validación", "solo mide"),
            (210, ENT, "ent", "entrenamiento", "ajusta")):
        c.append(caja(420, y - 26, 148, 52, relleno=PANEL, borde=color, radio=8, grosor=2))
        c.append(_triangulo(436, y - 3, r=8) if marca == "val" else _circulo(436, y - 3, r=7))
        c.append(texto(450, y + 1, nombre, tam=13, peso="700", anclaje="start", color=color))
        c.append(texto(494, y + 19, que, tam=12, color=SUAVE))
    c.append(flecha(384, 112, 416, 112, color=ACENTO, grosor=2.2))
    c.append(flecha(360, 210, 416, 210, color=ACENTO, grosor=2.2))
    c.append(tx(16, DN_H - 42, ["Si afuera mirara "] + _L("ent") + [", ganaría siempre la "
                                                       "caja más grande:"], tam=13,
                anclaje="start"))
    c.append(tx(16, DN_H - 22, ["con familias anidadas, "] + _L("ent") + [" nunca sube con ",
                                                                  ("N", _IT), "."], tam=13,
                anclaje="start", color=SUAVE))
    aria = ("Dos cajas anidadas. La de afuera elige el grado N comparando los candidatos "
            "con la pérdida de validación, y su flecha va al conjunto de validación, que "
            "solo mide. La de adentro elige beta con N fijo minimizando la pérdida de "
            "entrenamiento con grado a lo más N, y su flecha va al conjunto de "
            "entrenamiento, que ajusta; devuelve un beta gorro por candidato. Al pie: si "
            "afuera se mirara el entrenamiento, ganaría siempre la caja más grande.")
    return svg(DN_W, DN_H, aria, "Dos decisiones, dos conjuntos", c)


# ------------------------------------------ diagrama: ml-c2-tres-conjuntos ---
#
# P1 §4. La barra de la muestra en 60/20/20 con el rol de cada conjunto, el
# candado de la prueba y la casilla del modelo final (reajuste con ent ∪ val).

TC_W, TC_H = 580, 330


def ml_c2_tres_conjuntos():
    c = []
    c.append(texto(16, 30, "Tres conjuntos, tres decisiones", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "la misma muestra, partida antes de mirar nada",
                   tam=13, color=SUAVE, anclaje="start"))
    x0, y0, ancho, alto = 24, 78, 532, 56
    partes = (("entrenamiento", ENT, 0.6, "ajusta", ["β̂", "(", "N", ")"]),
              ("validación", VAL, 0.2, "elige", ["N̂"]),
              ("prueba", PRU, 0.2, "se abre una vez", []))
    x = x0
    centros = []
    for nombre, color, frac, que, simb in partes:
        w = ancho * frac
        c.append(caja(x + 1, y0, w - 2, alto, relleno=mezclar(color, 0.28, PANEL),
                      borde=color, radio=6, grosor=2))
        cx = x + w / 2
        centros.append((x, x + w, cx))
        if nombre == "entrenamiento":
            c.append(_circulo(cx - 26, y0 + 40, r=6))
        elif nombre == "validación":
            c.append(_triangulo(cx - 26, y0 + 41, r=7))
        else:
            c.append(_cuadrado(cx - 26, y0 + 40, r=6))
            c.append(_candado(cx + 34, y0 + 41, color=TEXTO, tam=0.9))
        c.append(texto(cx, y0 + 24, nombre, tam=14, peso="700"))
        c.append(texto(cx + 4, y0 + 45, f"{round(100 * frac)} %", tam=13, color=SUAVE))
        x += w
    # roles debajo
    yr = y0 + alto + 28
    (e0, e1, ec), (v0, v1, vc), (p0, p1, pc) = centros
    c.append(texto(ec, yr, ["ajusta ", ("β̂", _IT), "(", ("N", _IT), ") de cada candidato"],
                   tam=13, color=ENT))
    c.append(texto(vc, yr, ["elige ", ("N̂", _IT)], tam=13, color=VAL))
    c.append(texto(pc, yr, "al final", tam=13, color=PRU))
    # casilla del modelo final: llave bajo ent ∪ val
    yl = yr + 16
    c.append(_llave_horizontal(e0 + 4, v1 - 4, yl, color=SUAVE, alto=14))
    yc = yl + 28
    c.append(caja(e0 + 70, yc, (v1 - e0) - 140, 58, relleno=PANEL, borde=TEXTO, radio=8,
                  grosor=1.6))
    c.append(texto((e0 + v1) / 2, yc + 23, "modelo final", tam=14, peso="700"))
    c.append(texto((e0 + v1) / 2, yc + 43, ["el elegido ", ("N̂", _IT),
                                             ", reajustado con ent ∪ val"], tam=13))
    c.append(flecha(v1 - 70, yc + 29, p0 + 10, y0 + alto + 4, color=ACENTO, grosor=2))
    c.append(texto(pc, yc + 58, ["estima ", ("R", _IT), " del"], tam=13, color=PRU))
    c.append(texto(pc, yc + 75, "modelo final", tam=13, color=PRU))
    c.append(texto(16, TC_H - 16, "La fórmula de la pérdida es la misma en los tres; "
                                  "cambia qué decisión tocó cada uno.",
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Una barra con la muestra partida en tres: entrenamiento, 60 por ciento, con "
            "círculo, ajusta beta gorro de N para cada candidato; validación, 20 por "
            "ciento, con triángulo, elige N gorro; prueba, 20 por ciento, con cuadrado y "
            "candado, se abre una vez, al final. Una llave junta entrenamiento y "
            "validación en la casilla del modelo final: el elegido, reajustado con "
            "entrenamiento unión validación; una flecha lleva el modelo final a la prueba, "
            "que estima su riesgo R.")
    return svg(TC_W, TC_H, aria, "Tres conjuntos, tres decisiones", c)


# ----------------------------------------------- diagrama: ml-c2-simulacro ---
#
# P1 §5 (F2 de los insumos). Cuatro contratos de uso; en cada fila, la barra
# de la muestra con la prueba marcada y, a la derecha, la separacion correcta.

SM_W, SM_H = 600, 420
SM_FILAS = (
    ("más de lo mismo", "al azar"),
    ("el mes que viene", "el último tramo de tiempo"),
    ("pacientes nuevos", "pacientes enteros a un lado"),
    ("otra ciudad", "ninguna; declara el alcance"),
)


def ml_c2_simulacro():
    c = []
    c.append(texto(16, 30, "La prueba imita cómo se usará el modelo", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "cada fila es un contrato de uso; ■ marca lo que va a prueba",
                   tam=13, color=SUAVE, anclaje="start"))
    c.append(texto(24, 80, "¿cómo se usará?", tam=13, peso="700", color=SUAVE,
                   anclaje="start"))
    c.append(texto(176, 80, "la muestra (y la prueba)", tam=13, peso="700", color=SUAVE,
                   anclaje="start"))
    c.append(texto(398, 80, "separación correcta", tam=13, peso="700", color=SUAVE,
                   anclaje="start"))
    bx, bw, bh = 176, 204, 30
    ncel = 12
    cw = bw / ncel
    for i, (contrato, sep) in enumerate(SM_FILAS):
        y = 100 + i * 78
        c.append(texto(24, y + 20, contrato, tam=14, peso="700", anclaje="start"))
        if i == 0:      # al azar: celdas sueltas
            prueba = {2, 7, 10}
        elif i == 1:    # tiempo: el ultimo tramo
            prueba = {9, 10, 11}
        elif i == 2:    # grupos: dos pacientes enteros (de tres celdas cada uno)
            prueba = {3, 4, 5}
        else:
            prueba = set()
        for j in range(ncel):
            x = bx + j * cw
            es = j in prueba
            c.append(caja(x + 1, y, cw - 2, bh, relleno=mezclar(PRU, 0.45, PANEL) if es
                          else mezclar(ENT, 0.22, PANEL), borde=PRU if es else LINEA,
                          radio=2, grosor=1.6 if es else 1))
            if es:
                c.append(_cuadrado(x + cw / 2, y + bh / 2, r=4.5))
        if i == 1:      # eje de tiempo
            c.append(flecha(bx, y + bh + 12, bx + bw + 6, y + bh + 12, color=SUAVE))
            c.append(texto(bx + bw - 2, y + bh + 27, ["tiempo ", ("t", _IT)], tam=12,
                           color=SUAVE, anclaje="end"))
        if i == 2:      # los pacientes: cuatro grupos de tres celdas
            for g in range(4):
                gx = bx + g * 3 * cw
                c.append(caja(gx + 2, y - 4, 3 * cw - 4, bh + 8, relleno="none", borde=SUAVE,
                              radio=6, grosor=1.2, guiones="4 3"))
            c.append(texto(bx + bw / 2, y + bh + 20, "cada recuadro, un paciente", tam=12,
                           color=SUAVE))
        if i == 3:      # otra poblacion, fuera de la muestra
            c.append(texto(bx + bw / 2, y + bh + 18, "ninguna fila es de la otra ciudad",
                           tam=12, color=SUAVE))
        if i < 3:
            c.append(texto(398, y + 20, sep, tam=13, anclaje="start"))
        else:
            c.append(texto(398, y + 12, "ninguna separación;", tam=13, anclaje="start",
                           color=PRU, peso="700"))
            c.append(texto(398, y + 30, "declara el alcance", tam=13, anclaje="start",
                           color=PRU, peso="700"))
    c.append(texto(16, SM_H - 16, "El azar es la respuesta de un solo contrato: el primero.",
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Cuatro contratos de uso, uno por fila, cada uno con la barra de la muestra y "
            "sus celdas de prueba marcadas con cuadrados. Más de lo mismo: celdas sueltas "
            "al azar; separación correcta, al azar. El mes que viene: el último tramo del "
            "eje de tiempo; separación correcta, el último tramo de tiempo. Pacientes "
            "nuevos: un paciente entero a prueba; separación correcta, pacientes enteros a "
            "un lado. Otra ciudad: ninguna fila de la muestra es de la otra ciudad; "
            "ninguna separación la imita, se declara el alcance.")
    return svg(SM_W, SM_H, aria, "La prueba imita cómo se usará el modelo", c)


# ------------------------------------------------ diagrama: ml-c2-pliegues ---
#
# P2 §1. Rejilla 5×5 (fila m = vuelta m) con el mismo trazo que
# dibujar_pliegues: el pliegue de validacion en oro con triangulo, el resto en
# cian con circulo; a la derecha L_{D_m}; una llave junta las cinco en CV_5;
# aparte, la prueba cerrada. A mano, sin ml_lab (§10.12), para que los
# diagramas arranquen en paralelo.

PL_W, PL_H = 600, 362


def ml_c2_pliegues():
    c = []
    k, celda, alto = 5, 46, 34
    x0, y0 = 92, 92
    c.append(texto(16, 30, "Validación cruzada con cinco pliegues", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "cada fila es un ajuste completo; la prueba no entra",
                   tam=13, color=SUAVE, anclaje="start"))
    for j in range(k):
        c.append(texto(x0 + (j + 0.5) * celda, y0 - 10, str(j + 1), tam=13, color=SUAVE))
    c.append(texto(x0 - 10, y0 - 10, "pliegue", tam=12, color=SUAVE, anclaje="end"))
    _rejilla_pliegues(c, x0, y0, k=k, celda=celda, alto=alto)
    xd = x0 + k * celda + 14
    for m in range(k):
        y = y0 + (m + 0.5) * alto + 5
        c.append(texto(24, y, f"vuelta {m + 1}", tam=13, anclaje="start"))
        c.append(tx(xd, y, [("L", _IT), ("𝒟" + "₁₂₃₄₅"[m], _SUB), "(", ("β̂", _IT),
                            f"⁽⁻{m + 1}⁾)"], tam=14, anclaje="start"))
    c.append(_llave_vertical(xd + 108, y0 + 4, y0 + k * alto - 4, ancho=14))
    c.append(tx(xd + 128, y0 + k * alto / 2 - 2, ["CV", ("5", _SUB)], tam=15, peso="700",
                   anclaje="start", color=VAL))
    c.append(texto(xd + 128, y0 + k * alto / 2 + 16, "promedio", tam=12, anclaje="start",
                   color=SUAVE))
    c.append(texto(xd + 128, y0 + k * alto / 2 + 31, "de los cinco", tam=12,
                   anclaje="start", color=SUAVE))
    # la prueba, aparte y cerrada
    yp = y0 + k * alto + 22
    c.append(caja(x0 + 1, yp, k * celda - 2, 34, relleno=mezclar(PRU, 0.30, PANEL),
                  borde=PRU, radio=4, grosor=2))
    c.append(_cuadrado(x0 + 18, yp + 17, r=6))
    c.append(_candado(x0 + k * celda - 20, yp + 17, color=TEXTO))
    c.append(texto(x0 + k * celda / 2, yp + 22, "prueba: cerrada", tam=14, peso="700"))
    c.append(texto(16, PL_H - 14, "Cada observación de desarrollo valida exactamente una vez.",
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Una rejilla de cinco por cinco: cada fila es una vuelta de la validación "
            "cruzada. En la vuelta m, el pliegue m, en oro con triángulo, valida, y los "
            "otros cuatro, en cian con círculo, ajustan beta gorro sin el pliegue m. A la "
            "derecha de cada fila, la pérdida en su pliegue de validación; una llave junta "
            "las cinco en CV 5, su promedio. Aparte, debajo, la prueba, con cuadrado y "
            "candado: cerrada, nunca rota. Cada observación de desarrollo valida "
            "exactamente una vez.")
    return svg(PL_W, PL_H, aria, "Validación cruzada con cinco pliegues", c)


# ------------------------------------------------ diagrama: ml-c2-costo-cv ---
#
# P2 §2. La rejilla de ml-c2-pliegues apilada en tres capas desplazadas (tres
# candidatos N), el contador M·k + 1 y el reajuste final del elegido.

CC_W, CC_H = 600, 360
CC_CANDIDATOS = (2, 4, 8)


def ml_c2_costo_cv():
    c = []
    k, celda, alto = 5, 28, 18
    M = len(CC_CANDIDATOS)
    c.append(texto(16, 30, "Lo que cuesta elegir con validación cruzada", tam=17,
                   peso="700", anclaje="start"))
    c.append(texto(16, 50, "una CV completa por candidato, más un ajuste final",
                   tam=13, color=SUAVE, anclaje="start"))
    bordes = (SUAVE, TEXTO, ACENTO)
    for i, N in enumerate(CC_CANDIDATOS):
        dx, dy = 40 + i * 34, 100 + i * 30
        c.append(caja(dx - 8, dy - 26, k * celda + 16, k * alto + 34, relleno=FONDO,
                      borde=bordes[i], radio=8, grosor=1.6,
                      guiones=None if i == M - 1 else "5 3"))
        c.append(texto(dx, dy - 9, ["grado ", ("N", _IT), f" = {N}"], tam=13, peso="700",
                       anclaje="start", color=bordes[i]))
        _rejilla_pliegues(c, dx, dy, k=k, celda=celda, alto=alto, marcas=(i == M - 1))
    xc = 330
    c.append(caja(xc, 84, 250, 104, relleno=PANEL, borde=LINEA, radio=10, grosor=1.6))
    c.append(texto(xc + 125, 112, "ajustes", tam=14, peso="700", color=SUAVE))
    c.append(texto(xc + 125, 140, ["M·k + 1 = ", f"{M}·{k} + 1 = {M * k + 1}"], tam=17,
                   peso="700"))
    c.append(texto(xc + 125, 166, [f"{M} candidatos × {k} pliegues, más 1"], tam=13,
                   color=SUAVE))
    c.append(caja(xc, 230, 250, 64, relleno=PANEL, borde=CIAN, radio=10, grosor=2))
    c.append(texto(xc + 125, 256, "el +1: reajuste del elegido", tam=14, peso="700",
                   color=CIAN))
    c.append(texto(xc + 125, 278, "con todo el desarrollo (ent ∪ val)", tam=13))
    c.append(flecha(256, 290, xc - 6, 262, color=ACENTO, grosor=2.2))
    c.append(texto(16, CC_H - 36, ["Con 13 grados y 5 pliegues: 13·5 + 1 = 66 ajustes."],
                   tam=13, anclaje="start"))
    c.append(texto(16, CC_H - 16, "El costo crece con candidatos por pliegues.", tam=13,
                   color=SUAVE, anclaje="start"))
    aria = ("Tres rejillas de cinco por cinco apiladas y desplazadas, una por candidato: "
            "grado 2, grado 4 y grado 8; cada una es una validación cruzada completa. Un "
            "contador dice M por k más 1 igual a 3 por 5 más 1, 16 ajustes: 3 candidatos "
            "por 5 pliegues, más 1. Una flecha lleva al más 1: el reajuste del elegido con "
            "todo el desarrollo, entrenamiento unión validación. Al pie: con 13 grados y 5 "
            "pliegues, 13 por 5 más 1, 66 ajustes.")
    return svg(CC_W, CC_H, aria, "Lo que cuesta elegir con validación cruzada", c)


# ------------------------------------------------- diagrama: ml-c2-anidada ---
#
# P2 §6. La CV anidada: afuera k pliegues que estiman; dentro de cada vuelta
# externa, una CV interna completa que elige el grado sin ver su pliegue
# externo; la flecha del elegido al pliegue externo que lo evalua.

AN_W, AN_H = 600, 420


def ml_c2_anidada():
    c = []
    k = 5
    c.append(texto(16, 30, "Afuera se estima; adentro se elige", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "validación cruzada anidada: el número de afuera mide todo el "
                           "procedimiento", tam=13, color=SUAVE, anclaje="start"))
    # una vuelta externa, ampliada (la m = 2), y las otras cuatro en miniatura
    x0, y0, w, h = 24, 74, 552, 34
    cw = w / k
    for j in range(k):
        externo = j == 1
        c.append(caja(x0 + j * cw + 1, y0, cw - 2, h,
                      relleno=mezclar(VAL, 0.45, PANEL) if externo else mezclar(ENT, 0.25, PANEL),
                      borde=VAL if externo else LINEA, radio=4, grosor=2 if externo else 1))
        c.append(texto(x0 + (j + 0.5) * cw, y0 + 22,
                       "externo 2" if externo else f"pliegue {j + 1}",
                       tam=13, peso="700" if externo else "normal",
                       color=TEXTO))
    c.append(texto(x0 + 1.5 * cw + 10, y0 + h + 26, ["el elegido ", ("N̂", _IT),
                                                     "₂ se mide aquí"], tam=12,
                   color=SUAVE, anclaje="start"))
    # la caja de adentro: CV interna sobre los otros cuatro pliegues
    yi = y0 + h + 40
    c.append(caja(x0, yi, 340, 196, relleno=PANEL, borde=ENT, radio=12, grosor=2))
    c.append(texto(x0 + 16, yi + 24, "adentro: CV interna con los otros cuatro", tam=14,
                   peso="700", anclaje="start", color=ENT))
    c.append(texto(x0 + 16, yi + 44, "no ve el pliegue externo 2", tam=12, anclaje="start",
                   color=SUAVE))
    _rejilla_pliegues(c, x0 + 22, yi + 60, k=4, celda=30, alto=20)
    c.append(texto(x0 + 160, yi + 92, ["CV interna de cada ", ("N", _IT)], tam=13,
                   anclaje="start"))
    c.append(texto(x0 + 160, yi + 112, ["→ elige ", ("N̂", _IT), "₂ y reajusta"], tam=13,
                   anclaje="start", color=VAL, peso="700"))
    c.append(texto(x0 + 160, yi + 132, "con los cuatro pliegues", tam=13, anclaje="start"))
    c.append(texto(x0 + 16, yi + 180, "elegir es parte del procedimiento", tam=12,
                   anclaje="start", color=SUAVE))
    # flecha del elegido al pliegue externo
    c.append(flecha(x0 + 1.5 * cw, yi - 2, x0 + 1.5 * cw, y0 + h + 4, color=ACENTO, grosor=2.2))
    # a la derecha: el promedio de afuera
    xr = 392
    c.append(caja(xr, yi + 20, 184, 128, relleno=FONDO, borde=VAL, radio=10, grosor=2))
    c.append(texto(xr + 92, yi + 48, "afuera:", tam=14, peso="700", color=VAL))
    c.append(texto(xr + 92, yi + 72, "la pérdida del elegido", tam=13))
    c.append(texto(xr + 92, yi + 90, "en el pliegue externo,", tam=13))
    c.append(texto(xr + 92, yi + 108, "promediada en las cinco", tam=13))
    c.append(texto(xr + 92, yi + 126, "vueltas externas", tam=13))
    c.append(texto(16, AN_H - 34, "Vuelta externa 2; las otras cuatro son iguales, con otro "
                                  "pliegue que mide.", tam=12, color=SUAVE, anclaje="start"))
    c.append(texto(16, AN_H - 14, "La prueba sigue cerrada: la anidada usa solo el desarrollo.",
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Validación cruzada anidada. Arriba, cinco pliegues externos; en la vuelta "
            "externa 2, el pliegue externo 2 mide. Dentro de esa vuelta, una validación "
            "cruzada interna con los otros cuatro pliegues, que no ve el pliegue externo "
            "2, elige el grado N gorro 2 y lo reajusta con los cuatro; una flecha lleva al "
            "elegido al pliegue externo, que lo evalúa. Afuera, la pérdida del elegido en "
            "cada pliegue externo se promedia en las cinco vueltas. Rótulo: afuera se "
            "estima, adentro se elige. La prueba sigue cerrada.")
    return svg(AN_W, AN_H, aria, "Afuera se estima; adentro se elige", c)


# ============================================== graficas de datos (rapido) ---
#
# Todas leen sus cifras de tools/ml_cifras_c2.py (el mismo diccionario que la
# pagina y la prueba) y dibujan con las dibujar_* de ml_lab, tema="sitio".

def _cif():
    import ml_cifras_c2
    return ml_cifras_c2


# --------------------------------------- grafica: ml-c2-ajustes-con-prueba ---
#
# P1 §2. Grados 1, 4 y 12 sobre el hilo: circulos de entrenamiento, cuadrados
# de prueba, f gruesa y el ajuste; arriba de cada panel L_ent y L_prueba.
YLIM_AJUSTES = (0, 75)


def ml_c2_ajustes_con_prueba():
    cif = _cif()
    ml = gen.ml_lab()
    d = cif.hilo()
    a = cif.cifras_c2_ajustes_con_prueba()

    def dibujar(fig, ejes):
        for ax, N in zip(ejes, (1, 4, 12)):
            ml.dibujar_proceso(d, conjuntos=("ent", "prueba"), ax=ax, tema="sitio")
            ml.dibujar_ajuste([cif.construir(N)(d)], ventana=(0, 6), ax=ax, tema="sitio")
            ax.set_ylim(*YLIM_AJUSTES)
            ax.set_xlim(0, 6)
            ax.set_title(f"grado {N}:  L_ent = {_num(a[N]['L_ent'])}   ·   "
                         f"L_prueba = {_num(a[N]['L_prueba'])}", color=TEXTO, fontsize=9)
            ax.set_ylabel("tiempo y (min)")
            ax.set_xlabel("")
            if ax.get_legend():
                ax.get_legend().remove()
        ejes[-1].set_xlabel("distancia x (km)")
        h, r = ejes[0].get_legend_handles_labels()
        r = ["f̂ (el ajuste)" if x.startswith("lineal") else x for x in r]
        _leyenda(ejes[0], handles=h, labels=r, loc="lower right", fontsize=8)

    aria = ("Tres paneles con las mismas 60 entregas: círculos de entrenamiento y "
            "cuadrados de prueba, la f verdadera y el ajuste. Grado 1: L_ent "
            f"{_num(a[1]['L_ent'])}, L_prueba {_num(a[1]['L_prueba'])}. Grado 4: L_ent "
            f"{_num(a[4]['L_ent'])}, L_prueba {_num(a[4]['L_prueba'])}. Grado 12: L_ent "
            f"{_num(a[12]['L_ent'])}, el más bajo, pero la curva pasa cerca de los círculos "
            "y se dispara en los bordes, y su L_prueba es enorme, "
            f"{_num(a[12]['L_prueba'], 0)}.")
    return _grafica(dibujar, aria, "Grados 1, 4 y 12 con entrenamiento y prueba", 7.4,
                    paneles=3, sharex=True)


# ------------------------------------------- grafica: ml-c2-prueba-ruidosa ---
#
# P1 §3. El modelo de grado 4 congelado; 500 pruebas nuevas de 20 y de 200
# sacadas del despliegue; linea en R; cobertura de ±2 EE en cada panel.

def ml_c2_prueba_ruidosa():
    cif = _cif()
    ml = gen.ml_lab()
    p = cif.cifras_c2_prueba_ruidosa()

    def dibujar(fig, ejes):
        for ax, n in zip(ejes, (20, 200)):
            ml.dibujar_histograma_estimaciones(p["estimaciones"][n], verdadero=p["R"],
                                               etiqueta="L_prueba", ax=ax, tema="sitio")
            ax.set_title(f"{cif.REP_PRUEBAS} pruebas de {n}: desv. {_num(p[f'desv_{n}'])}; "
                         f"±2 EE cubre R en {_pct(p[f'cobertura_{n}'])}", color=TEXTO,
                         fontsize=9)
            ax.set_xlim(0, 32)
            _leyenda(ax, loc="upper right", renombrar={"verdadero": f"R = {_num(p['R'])}"})
            ax.set_xlabel("")
        ejes[-1].set_xlabel("L_prueba del mismo modelo (grado 4, congelado)")

    aria = (f"Dos histogramas de L_prueba del mismo modelo de grado 4, congelado, con "
            f"{cif.REP_PRUEBAS} pruebas nuevas cada uno. Con 20 entregas por prueba la nube "
            f"es ancha, desviación {_num(p['desv_20'])}, y el intervalo de ±2 EE cubre R en "
            f"{_pct(p['cobertura_20'])} de las pruebas; con 200, desviación "
            f"{_num(p['desv_200'])} y cobertura {_pct(p['cobertura_200'])}. Las dos nubes "
            f"se centran en R = {_num(p['R'])}.")
    return _grafica(dibujar, aria, "Una prueba honesta también baila", 5.2, paneles=2,
                    sharex=True)


# ------------------------------------------------ grafica: ml-c2-optimismo ---
#
# P1 §4 (F4). Anunciado menos real del elegido, SIN reajuste, eligiendo con la
# prueba (izquierda en la pagina: arriba aqui) y con validacion (abajo).
XLIM_OPTIMISMO = (-30, 20)


def ml_c2_optimismo():
    cif = _cif()
    ml = gen.ml_lab()
    o = cif.cifras_c2_optimismo()
    serie = o["anunciado_menos_real"]

    def dibujar(fig, ejes):
        for ax, (clave, nombre) in zip(ejes, (("prueba", "eliges con la prueba"),
                                              ("validacion", "eliges con validación"))):
            v = np.clip(serie[clave], *XLIM_OPTIMISMO)
            ml.dibujar_histograma_estimaciones({nombre: v}, verdadero=0,
                                               etiqueta="anunciado − real del elegido (sin reajuste)",
                                               ax=ax, tema="sitio")
            ax.set_xlim(*XLIM_OPTIMISMO)
            ax.set_title(f"{nombre}: {_pct(o['optimistas_' + clave])} anuncian de menos",
                         color=TEXTO, fontsize=9)
            _leyenda(ax, loc="upper left", renombrar={"verdadero": "0: anuncio honesto"})
        ejes[0].set_xlabel("")
        ejes[1].annotate("sin reajuste: el mismo\nentrenamiento en los dos paneles",
                         (0.99, 0.95), xycoords="axes fraction", ha="right", va="top",
                         fontsize=8, color=TEXTO)

    aria = (f"Dos histogramas con {o['repeticiones']} repeticiones del hilo: lo anunciado "
            "menos el riesgo real del grado elegido, sin reajuste. Arriba, eligiendo con la "
            f"prueba: la nube se corre a la izquierda de 0, la media es "
            f"{_num(o['sesgo_prueba'])} y {_pct(o['optimistas_prueba'])} de las repeticiones "
            "anuncian menos error del real. Abajo, eligiendo con validación y anunciando en "
            f"prueba: la mediana queda en {_num(o['mediana_validacion'])} y "
            f"{_pct(o['optimistas_validacion'])} anuncian de menos. Los valores fuera de "
            f"{XLIM_OPTIMISMO[0]} a {XLIM_OPTIMISMO[1]} se apilan en los bordes.")
    return _grafica(dibujar, aria, "El engaño de elegir con la prueba", 5.2, paneles=2,
                    sharex=True)


# --------------------------------------------- grafica: ml-c2-prueba-miente ---
#
# P1 §5. Id congelado (lo cita la clase 5). Por contrato, L_prueba al azar y
# con la separacion que lo imita, contra R del despliegue y el benchmark.

def tabla_contratos():
    cif = _cif()
    i = cif.cifras_c2_imitar()
    filas = []
    for c in cif.CONTRATOS:
        a = i[c]["azar"]
        filas.append({"contrato": c, "separacion": "al azar", "L_prueba": a["L_prueba"],
                      "R": a["R"], "benchmark": a["benchmark"]})
        if "imita" in i[c]:
            m = i[c]["imita"]
            sep = "por tiempo" if c == "el mes que viene" else "por paciente"
            filas.append({"contrato": c, "separacion": sep, "L_prueba": m["L_prueba"],
                          "R": m["R"], "benchmark": m["benchmark"]})
    import pandas as pd
    return pd.DataFrame(filas)


def ml_c2_prueba_miente():
    cif = _cif()
    ml = gen.ml_lab()
    i = cif.cifras_c2_imitar()
    t = tabla_contratos()

    def dibujar(fig, ax):
        ml.dibujar_contratos(t, ax=ax, tema="sitio")
        ax.set_xticklabels([f"{c}\n{s}".replace("el mes que viene", "el mes\nque viene")
                            .replace("más de lo mismo", "más de\nlo mismo")
                            .replace("pacientes nuevos", "pacientes\nnuevos")
                            for c, s in zip(t["contrato"], t["separacion"])], fontsize=8)
        ax.set_yscale("log")
        ax.set_ylim(1, 3000)
        ax.set_ylabel("pérdida (escala log)")
        _leyenda(ax, loc="upper left", fontsize=8, ncol=2)

    def par(c, k="azar"):
        return f"{_num(i[c][k]['L_prueba'])} contra R {_num(i[c][k]['R'])}"

    aria = ("Por contrato, lo que promete la prueba contra el riesgo del despliegue, en "
            "escala logarítmica. Más de lo mismo, al azar: " + par("más de lo mismo") +
            ". El mes que viene, al azar: " + par("el mes que viene") + "; por tiempo: " +
            par("el mes que viene", "imita") + ". Pacientes nuevos, al azar: " +
            par("pacientes nuevos") + "; por paciente: " + par("pacientes nuevos", "imita") +
            ". Otra ciudad, al azar: " + par("otra ciudad") + "; ninguna separación de la "
            "muestra la imita. La raya y punto es el benchmark, la media de entrenamiento.")
    return _grafica(dibujar, aria, "Lo que promete la prueba según cómo se separó", 4.4)


# ------------------------------------------------- grafica: ml-c2-reparto ---
#
# P1 §6. R medio del modelo (arriba) y dispersion de L_prueba − R (abajo)
# contra la fraccion de prueba, n = 60; marcas en 20 % y 50 %.

def ml_c2_reparto():
    cif = _cif()
    ml = gen.ml_lab()
    r = cif.cifras_c2_reparto()
    t = cif.tabla_reparto()

    def dibujar(fig, ejes):
        ml.dibujar_reparto(t, marca=0.2, ax=list(ejes), tema="sitio")
        for ax in ejes:
            ax.axvline(0.5, color=SUAVE, ls=":", lw=1.2)
        ejes[0].set_title(f"{cif.REP_REPARTO} repeticiones por fracción; n = {cif.N_REPARTO}",
                          color=TEXTO, fontsize=9)
        ejes[0].set_ylabel("R medio del modelo")
        ejes[1].set_ylabel("desv. del error")

    aria = ("Contra la fracción de la muestra que va a prueba, de 5 a 50 por ciento, con "
            f"60 entregas. Arriba, el riesgo medio del modelo: {_num(r[0.1]['R'])} con 10 por "
            f"ciento, {_num(r[0.2]['R'])} con 20 y {_num(r[0.5]['R'])} con 50: empeora al "
            "quitarle datos. Abajo, la desviación de L_prueba menos R: "
            f"{_num(r[0.1]['desv_error'])} con 10 por ciento, {_num(r[0.2]['desv_error'])} "
            f"con 20 y {_num(r[0.5]['desv_error'])} con 50: la medición mejora. Marcas en 20 "
            "y 50 por ciento.")
    return _grafica(dibujar, aria, "Aprender y medir compiten por los mismos datos", 5.2,
                    paneles=2, sharex=True)


# --------------------------------------------- grafica: ml-c2-cv-capacidad ---
#
# P2 §3. Id congelado (lo cita la clase 3). Una sola llamada a dibujar_cv con
# R (muestra enorme, solo en el simulador), L_ent, piso y benchmark.

def ml_c2_cv_capacidad():
    cif = _cif()
    ml = gen.ml_lab()
    h = cif.cifras_c2_hilo()
    s = cif.seleccion_hilo()

    def dibujar(fig, ax):
        ml.dibujar_cv(s, R=h["R_por_N"], L_ent=h["L_ent_por_N"], piso=h["piso"],
                      benchmark=h["benchmark_despliegue"], ax=ax, tema="sitio")
        ax.set_yscale("log")
        ax.set_ylim(4, 400)
        ax.set_xlabel("grado N")
        ax.set_ylabel("pérdida (escala log)")
        _leyenda(ax, loc="upper center", fontsize=8, ncol=2, bbox_to_anchor=(0.5, -0.2))

    aria = (f"CV 5 con barras de ±1 EE contra el grado N de 0 a 12. El mínimo está en N = "
            f"{h['N_min']}, con CV {_num(h['cv'][h['N_min']], 2)} ± "
            f"{_num(h['ee'][h['N_min']], 2)}; el umbral mínimo más un EE es "
            f"{_num(h['umbral'], 2)} y la regla de un EE también elige N = {h['N_un_ee']}. "
            f"L_ent baja siempre, de {_num(h['L_ent_por_N'][0])} a "
            f"{_num(h['L_ent_por_N'][12])}. El riesgo R de cada grado, que solo existe en el "
            f"simulador, es mínimo en N = {h['N_mejor_R']} ({_num(h['R_por_N'][4])}) y vale "
            f"{_num(h['R_por_N'][h['N_min']])} en el elegido. Piso {_num(h['piso'])}; "
            f"benchmark, la media de entrenamiento, {_num(h['benchmark_despliegue'])}.")
    return _grafica(dibujar, aria, "La validación cruzada contra el grado", 5.0)


# ------------------------------------------- grafica: ml-c2-pliegue-anomalo ---
#
# P2 §4. Caso 16: la perdida de cada pliegue para los grados 1, 4 y 8.

def ml_c2_pliegue_anomalo():
    cif = _cif()
    ml = gen.ml_lab()
    p = cif.cifras_c2_pliegue_anomalo()
    d = ml.caso(16)
    res = {N: ml.validacion_cruzada(d, cif.construir(N), k=5) for N in (1, 4, 8)}

    def dibujar(fig, ax):
        ml.dibujar_cajas_pliegues(res, ax=ax, tema="sitio")
        ax.set_yscale("log")
        ax.set_xlabel("grado N")
        ax.set_ylabel("L de cada pliegue (escala log)")
        _leyenda(ax, loc="upper left", fontsize=8)

    lejanos = " y ".join(str(m) for m in p["pliegues_con_lejana"])
    aria = ("Caso 16, cinco pliegues, un triángulo por pliegue y una raya en la media, para "
            f"los grados 1, 4 y 8, en escala logarítmica. Con grado 1 los cinco quedan juntos: "
            f"el mayor es {_num(p[1]['cociente'], 2)} veces la mediana de los otros. Con grado "
            f"8, los pliegues {lejanos}, los que traen una entrega lejana, se disparan: el "
            f"pliegue {p[8]['pliegue_max']} da {_num(p[8]['por_pliegue'][p[8]['pliegue_max'] - 1], 0)}, "
            f"miles de veces la mediana de los otros.")
    return _grafica(dibujar, aria, "Un pliegue que carga casi todo el error", 3.6)


# ---------------------------------------------- grafica: ml-c2-estratificada ---
#
# P2 §5. Id congelado (lo cita la clase 4). 60 casos con 6 positivos, k = 5:
# arriba una particion al azar, abajo la estratificada; en el titulo, la
# fraccion de 1000 particiones con algun pliegue sin positivos.
SEMILLA_ESTRAT = 0


def ml_c2_estratificada():
    cif = _cif()
    ml = gen.ml_lab()
    e = cif.cifras_c2_estratificada()
    df = cif.df_estratificada()
    azar = ml.pliegues(df, k=cif.K_ESTRAT, como="azar", semilla=SEMILLA_ESTRAT)
    estr = ml.pliegues(df, k=cif.K_ESTRAT, como="estratificado", semilla=SEMILLA_ESTRAT)
    y = df["y"].to_numpy()
    cuenta = {n: [int(y[v].sum()) for _, v in part] for n, part in (("azar", azar),
                                                                     ("estr", estr))}

    def dibujar(fig, ejes):
        for ax, part, nombre, clave in ((ejes[0], azar, "al azar", "azar"),
                                        (ejes[1], estr, "estratificada", "estratificada")):
            ml.dibujar_pliegues(len(df), cif.K_ESTRAT, prueba=False, y=df["y"], particion=part,
                                ax=ax, tema="sitio")
            ax.set_title(f"{nombre}: positivos por pliegue "
                         f"{', '.join(map(str, cuenta['azar' if clave == 'azar' else 'estr']))}"
                         f"\nen 1000 particiones, {_pct(e[clave])} con algún pliegue vacío",
                         color=TEXTO, fontsize=9)

    aria = ("Sesenta casos con 6 positivos en cinco pliegues. Arriba, una partición al azar: "
            f"positivos por pliegue {', '.join(map(str, cuenta['azar']))}. Abajo, la "
            f"estratificada: {', '.join(map(str, cuenta['estr']))}. En 1000 particiones de "
            f"cada método, al azar {_pct(e['azar'])} dejan algún pliegue sin positivos; "
            f"estratificando, {_pct(e['estratificada'])}.")
    return _grafica(dibujar, aria, "Pliegues al azar y estratificados", 6.0, paneles=2)


_RAPIDO = {
    "ml-c2-dos-niveles": ml_c2_dos_niveles,
    "ml-c2-tres-conjuntos": ml_c2_tres_conjuntos,
    "ml-c2-simulacro": ml_c2_simulacro,
    "ml-c2-pliegues": ml_c2_pliegues,
    "ml-c2-costo-cv": ml_c2_costo_cv,
    "ml-c2-anidada": ml_c2_anidada,
    "ml-c2-ajustes-con-prueba": ml_c2_ajustes_con_prueba,
    "ml-c2-prueba-ruidosa": ml_c2_prueba_ruidosa,
    "ml-c2-optimismo": ml_c2_optimismo,
    "ml-c2-prueba-miente": ml_c2_prueba_miente,
    "ml-c2-reparto": ml_c2_reparto,
    "ml-c2-cv-capacidad": ml_c2_cv_capacidad,
    "ml-c2-pliegue-anomalo": ml_c2_pliegue_anomalo,
    "ml-c2-estratificada": ml_c2_estratificada,
}

# --- fin tramo rapido ---


# --- tramo m ---

# ------------------------------------------------- grafica: ml-c2-abanico ---
#
# P3 §1. Cien ajustes (cien muestras del hilo) por grado 1, 4 y 12, su
# promedio y E[y | x]; la translucidez de ml_lab se hornea (sin fill-opacity,
# §10.12). El ancho del abanico en x0 = 5 sale de ml_cifras_c2.
ABANICO = (1, 4, 12)


def ml_c2_abanico():
    cif = _cif()
    ml = gen.ml_lab()
    sv = cif.sesgo_varianza_hilo()
    ancho = {N: float(cif._predicciones_en(sv, cif.X0, N).std()) for N in ABANICO}

    def dibujar(fig, ejes):
        for ax, N in zip(ejes, ABANICO):
            ml.dibujar_abanico(sv, N, ax=ax, tema="sitio")
            ax.set_title(f"grado {N}: {cif.REP_SV} muestras; en x = {cif.X0:g}, "
                         f"desviación {_num(ancho[N])}", color=TEXTO, fontsize=9)
            ax.set_ylim(0, 50)
            ax.set_xlabel("")
            ax.set_ylabel("predicción (min)")
            if ax is not ejes[0] and ax.get_legend():
                ax.get_legend().remove()
        # sin mathtext: el acento de $\widehat{f}$ sale en letra de 5 px
        _leyenda(ejes[0], loc="lower right", fontsize=8,
                 renombrar={r"$\widehat{f}$ de cada muestra": "f̂ de cada muestra",
                            r"promedio de las $\widehat{f}$": "promedio de las f̂"})
        ejes[-1].set_xlabel("distancia x (km)")

    aria = (f"Tres paneles con {cif.REP_SV} ajustes cada uno, uno por muestra del mismo "
            "proceso, su promedio y la verdadera E[y | x]. Grado 1: las rectas casi no se "
            f"separan (desviación {_num(ancho[1])} en x = 5) pero su promedio se aleja de "
            f"la curva. Grado 4: abanico angosto (desviación {_num(ancho[4])}) y promedio "
            "pegado a la curva. Grado 12: el promedio sigue la curva, pero cada ajuste se "
            f"sacude, sobre todo en los bordes (desviación {_num(ancho[12])} en x = 5).")
    return _grafica(dibujar, aria, "Cien muestras, cien ajustes", 7.0, paneles=3, sharex=True)


# --------------------------------------------------- grafica: ml-c2-diana ---
#
# P3 §2. Id congelado (lo cita la clase 3). Las predicciones de cada
# repeticion en x0 = 5 para los grados 1 y 12, su promedio y f(x0), con eje
# fijo EJE_DIANA y sin recorte (ninguna cae fuera: lo prueba ml_cifras_c2).

def ml_c2_diana():
    cif = _cif()
    ml = gen.ml_lab()
    sv = cif.sesgo_varianza_hilo()
    s = cif.cifras_c2_sesgo_varianza()

    def dibujar(fig, ax):
        ml.dibujar_diana(sv, cif.X0, candidatos=[1, 12], ax=ax, tema="sitio")
        ax.set_xlim(*cif.EJE_DIANA)
        ax.set_yticklabels(["grado 1", "grado 12"])
        ax.set_ylabel("")
        _leyenda(ax, loc="upper center", fontsize=8, ncol=3, bbox_to_anchor=(0.5, -0.32))

    d1, d12 = s["diana_1"], s["diana_12"]
    aria = (f"Predicciones en x = {cif.X0:g} de {cif.REP_SV} ajustes, cada uno con otra "
            f"muestra, junto a E[y | x = 5] = {_num(s['f_x0'])}. Grado 1: las cruces se "
            f"agrupan apretadas (desviación {_num(d1['desv'])}) pero corridas "
            f"{_num(d1['sesgo'])} minutos del valor verdadero. Grado 12: centradas "
            f"(sesgo {_num(d12['sesgo'])}) pero dispersas (desviación {_num(d12['desv'])}). "
            f"Eje fijo de {cif.EJE_DIANA[0]:g} a {cif.EJE_DIANA[1]:g} minutos; ninguna "
            "predicción queda fuera.")
    return _grafica(dibujar, aria, "La diana en x = 5", 3.4)


_M = {
    "ml-c2-abanico": ml_c2_abanico,
    "ml-c2-diana": ml_c2_diana,
}
# --- fin tramo m ---


# --- tramo completo ---

# --------------------------------------------- grafica: ml-c2-sesgo-varianza ---
#
# P3 §3 (fig. 5.6 del libro). Arriba, las barras apiladas ruido + sesgo² +
# varianza por grado (100 muestras, f conocida) y la estrella en N⋆. Abajo,
# mismo eje: la CV_5 de una sola muestra (la de ml-c2-cv-capacidad) y el total
# calculado, en escala log (el total del grado 12 se sale: se dice en el rotulo).
YLIM_SV = (4, 400)


def ml_c2_sesgo_varianza():
    cif = _cif()
    ml = gen.ml_lab()
    sv = cif.sesgo_varianza_hilo()
    s = cif.cifras_c2_sesgo_varianza()
    h = cif.cifras_c2_hilo()
    sel = cif.seleccion_hilo()
    Ns = list(cif.CANDIDATOS)
    total = [s[N]["total"] for N in Ns]

    def dibujar(fig, ejes):
        arriba, abajo = ejes
        ml.dibujar_sesgo_varianza(sv, ax=arriba, tema="sitio")
        fuera = [N for N in Ns if s[N]["total"] > arriba.get_ylim()[1]]
        arriba.set_title(f"en el simulador: f conocida, {cif.REP_SV} muestras; "
                         f"{fuera[0]} a {fuera[-1]} salen del eje", color=TEXTO,
                         fontsize=9)
        arriba.set_xlabel("")
        arriba.set_ylabel("error esperado")
        _leyenda(arriba, loc="upper left", fontsize=8,
                 renombrar={f"menor total: {s['N_estrella']}": f"menor total: N⋆ = "
                                                                f"{s['N_estrella']}"})
        ml.dibujar_cv(sel, ax=abajo, tema="sitio")
        ln, = abajo.plot(Ns, total, ls="-", lw=2.0, color=REAL, label="total calculado")
        ln.set_gid("total-calculado")
        abajo.set_yscale("log")
        abajo.set_ylim(*YLIM_SV)
        abajo.set_xticks(Ns)
        abajo.set_xlabel("grado N")
        abajo.set_ylabel("pérdida (escala log)")
        abajo.set_title("medido con una sola muestra: CV 5", color=TEXTO, fontsize=9)
        _leyenda(abajo, loc="upper center", fontsize=8, ncol=2, bbox_to_anchor=(0.5, -0.3),
                 renombrar={"CV_k": "CV 5 de una muestra"})

    N0 = s["N_estrella"]
    aria = (f"Dos paneles con el grado N de 0 a 12. Arriba, barras apiladas de ruido, sesgo "
            f"al cuadrado y varianza calculadas con f conocida y {cif.REP_SV} muestras: el "
            f"ruido mide {_num(s[0]['ruido'])} en todos los grados, el sesgo al cuadrado baja "
            f"de {_num(s[0]['sesgo2'])} en N = 0 a {_num(s[N0]['sesgo2'], 2)} en N = {N0} y la "
            f"varianza sube; el menor total, {_num(s[N0]['total'], 2)}, está en N⋆ = {N0}. "
            f"Abajo, en escala log, la CV 5 de una sola muestra, con mínimo en N = "
            f"{h['N_min']}, junto al total calculado: las dos bajan y suben en la misma zona "
            f"sin coincidir punto por punto; el total del grado 12 sale del eje.")
    return _grafica(dibujar, aria, "La U calculada y la U medida", 7.2, paneles=2, sharex=True,
                    gridspec_kw={"height_ratios": [1.2, 1]})


# ------------------------------------------- grafica: ml-c2-curva-aprendizaje ---
#
# P3 §4 (fig. 5.4 del libro, con su panel de abajo). Medianas de 50 repeticiones
# de L_ent y R de los grados 1 y 10 contra n (log, duplicando desde 30), el piso;
# abajo, el grado que elige CV_5 (mediana de 20). resumen="mediana" EXPLICITO:
# la prueba de posicion compara cada punto con cifras_c2_curva_aprendizaje.
YLIM_CURVA = (0, 30)


def ml_c2_curva_aprendizaje():
    cif = _cif()
    ml = gen.ml_lab()
    a = cif.cifras_c2_curva_aprendizaje()

    def dibujar(fig, ejes):
        ml.dibujar_curva_aprendizaje(cif.tabla_curva_aprendizaje(), piso=a["piso"],
                                     elegido=cif.tabla_capacidad_elegida(),
                                     resumen="mediana", ax=list(ejes), tema="sitio")
        arriba, abajo = ejes
        arriba.set_ylim(*YLIM_CURVA)
        arriba.set_ylabel("pérdida (mediana de 50)")
        _leyenda(arriba, loc="upper right", fontsize=8, ncol=2,
                 renombrar={"L_ent · 1": "L ent · grado 1", "R · 1": "R · grado 1",
                            "L_ent · 10": "L ent · grado 10", "R · 10": "R · grado 10"})
        abajo.set_ylim(0, 12.5)
        abajo.set_ylabel("grado elegido")
        abajo.set_xlabel("entregas de entrenamiento n (escala log)")
        _leyenda(abajo, loc="lower right", fontsize=8,
                 renombrar={"elegido por CV (mediana)": "elegido por CV 5 (mediana de 20)"})

    R = a["R"]
    aria = (f"Arriba, medianas de 50 muestras contra el número de entregas, de 30 a 960 en "
            f"escala log: el riesgo R del grado 1 baja de {_num(R[(1, 30)])} a "
            f"{_num(R[(1, 480)])} y se queda en {_num(R[(1, 960)])}, arriba del piso de "
            f"{_num(a['piso'])}; el del grado 10 empieza arriba de la recta y baja a "
            f"{_num(R[(10, 480)])} y {_num(R[(10, 960)])}, pegado al piso. Abajo, el grado que "
            f"elige la CV 5 (mediana de 20 muestras) sube de {a['elegido'][30]:g} con 30 "
            f"entregas a {a['elegido'][960]:g} con 960.")
    return _grafica(dibujar, aria, "Más datos: a quién le ayudan", 6.4, paneles=2, sharex=True,
                    gridspec_kw={"height_ratios": [3, 1.4]})


# ------------------------------------------------ diagrama: ml-c2-diagnostico ---
#
# P3 §5. Id congelado (lo cita la clase 5). El arbol de cuatro preguntas que
# se contestan con datos reales, de arriba abajo, y sus cinco hojas.

DG_W, DG_H = 600, 600


def _hoja(c, x, y, w, nombre, accion, color):
    c.append(caja(x, y, w, 50, relleno=mezclar(color, 0.22, PANEL), borde=color, radio=8,
                  grosor=2))
    c.append(texto(x + w / 2, y + 21, nombre, tam=14, peso="700", color=TEXTO))
    c.append(texto(x + w / 2, y + 40, accion, tam=12, color=SUAVE))


def _pregunta(c, x, y, w, renglones, nota=None):
    alto = 24 + 18 * len(renglones) + (16 if nota else 0)
    c.append(caja(x, y, w, alto, relleno=FONDO, borde=ACENTO, radio=10, grosor=2))
    for i, r in enumerate(renglones):
        c.append(tx(x + 14, y + 24 + 18 * i, r, tam=13, anclaje="start"))
    if nota:
        c.append(texto(x + 14, y + 24 + 18 * len(renglones), nota, tam=12, color=SUAVE,
                       anclaje="start"))
    return alto


def ml_c2_diagnostico():
    c = []
    c.append(texto(16, 30, "Diagnosticar con dos curvas y un benchmark", tam=17, peso="700",
                   anclaje="start"))
    c.append(texto(16, 50, "se lee de arriba abajo; cada pregunta se contesta con datos reales",
                   tam=13, color=SUAVE, anclaje="start"))
    xq, wq, xh, wh = 16, 350, 398, 186
    filas = [
        (66, [["1 · ¿Brecha "] + _L("val") + [" − "] + _L("ent") + [" (o CV − "]
              + _L("ent") + [") grande?"]], None,
         "sobreajuste", "menos capacidad, más datos", PRU),
        (160, [["2 · ¿Le gana al benchmark (la media de ent)?"],
               ["(a) en validación que no eligió: la"],
               ["diferencia pareada baja de 0 a más de 2 EE"]],
         "(b) con CV solo da señal o «falta evidencia»",
         "no aprende", "otras variables o familias", BENCH),
        (300, [["3 · ¿Subir el grado baja la CV más de un EE?"]],
         "heurística, como la regla de un EE",
         "subajuste", "más capacidad, mejor φ", VAL),
        (400, [["4 · ¿Tu prueba imita el despliegue?"]], None,
         "listo", "lo que queda: ruido o familia", VERDE),
    ]
    centros = []
    for y, renglones, nota, nombre, accion, color in filas:
        alto = _pregunta(c, xq, y, wq, renglones, nota)
        yc = y + alto / 2
        centros.append((y, alto))
        _hoja(c, xh, yc - 25, wh, nombre, accion, color)
        c.append(flecha(xq + wq, yc, xh - 4, yc, color=ACENTO, grosor=2))
        c.append(texto(xq + wq + 16, yc - 8, "sí" if nombre != "no aprende" else "no",
                       tam=12, color=SUAVE))
    # flechas hacia abajo entre preguntas ("no", salvo la 2, que sigue con "sí")
    for i in range(len(filas) - 1):
        (y, alto), (y2, _) = centros[i], centros[i + 1]
        c.append(flecha(xq + 60, y + alto, xq + 60, y2 - 4, color=ACENTO, grosor=2))
        c.append(texto(xq + 68, (y + alto + y2) / 2 + 4, "sí" if i == 1 else "no", tam=12,
                       color=SUAVE, anclaje="start"))
    # la quinta hoja: la prueba no imita
    y4, a4 = centros[-1]
    c.append(flecha(xq + 60, y4 + a4, xq + 60, 494, color=ACENTO, grosor=2))
    c.append(texto(xq + 68, 486, "no", tam=12, color=SUAVE, anclaje="start"))
    _hoja(c, xq, 498, 260, "rehacer la separación", "página 1, §5: imitar el despliegue",
          ACENTO)
    c.append(texto(16, DG_H - 34, "El subajuste se reconoce porque una familia más flexible",
                   tam=13, color=SUAVE, anclaje="start"))
    c.append(texto(16, DG_H - 14, "baja el error honesto; el piso solo se ve en el simulador.",
                   tam=13, color=SUAVE, anclaje="start"))
    aria = ("Árbol de diagnóstico con cuatro preguntas que se leen de arriba abajo. Uno: la "
            "brecha entre validación, o CV, y entrenamiento es grande; si sí, sobreajuste: "
            "menos capacidad o más datos. Dos: le gana al benchmark, la media de "
            "entrenamiento; en una validación que no eligió el modelo, la diferencia pareada "
            "baja de cero a más de dos errores estándar; con CV solo da señal o falta "
            "evidencia; si no, no aprende: otras variables o familias. Tres: subir el grado "
            "baja la CV más de un error estándar, una heurística; si sí, subajuste: más "
            "capacidad o mejor phi. Cuatro: la prueba imita el despliegue; si sí, listo; si "
            "no, rehacer la separación.")
    return svg(DG_W, DG_H, aria, "Diagnosticar con dos curvas y un benchmark", c)


_COMPLETO = {
    "ml-c2-sesgo-varianza": ml_c2_sesgo_varianza,
    "ml-c2-curva-aprendizaje": ml_c2_curva_aprendizaje,
    "ml-c2-diagnostico": ml_c2_diagnostico,
}
# --- fin tramo completo ---


FIGURAS_C2 = {**_RAPIDO, **_M, **_COMPLETO}
