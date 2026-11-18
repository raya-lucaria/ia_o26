"""Las graficas de los resultados del torneo de Breakthrough de combate.

Leen los datos publicos de la liga de renna, copiados tal cual en
tools/datos_torneo/ desde el repositorio del torneo (no se calculan aqui:
salen de 7 corridas completas, 16 240 partidas). Solo hay nombres de equipo;
nada de calificaciones.

Los diagramas se registran en el catalogo DIAGRAMAS de gen_juegos.py, porque
viven en el _assets/ de la unidad de juegos y sus guardas exigen que todo SVG
de esa carpeta salga de ese catalogo. Por eso llevan el prefijo "jue-torneo-".

    python3 tools/gen_juegos.py jue-torneo-victorias jue-torneo-cara-a-cara \
        jue-torneo-corridas
"""
import csv
import json
from pathlib import Path

from gen_optimizacion import (ACENTO, LINEA, SERIE, SUAVE, TEXTO, cierre,
                              linea, marco, mezclar, punto, texto)

DATOS = Path(__file__).resolve().parent / "datos_torneo"
REFERENCIA = ("random", "montecarlo")
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

COLOR_ALUMNOS = ACENTO
COLOR_REFERENCIA = SERIE[1]


def es_referencia(equipo):
    return equipo in REFERENCIA or equipo.startswith("tier_")


def _color(equipo):
    return COLOR_REFERENCIA if es_referencia(equipo) else COLOR_ALUMNOS


def equipos():
    """Filas de equipos.csv en el orden oficial de la tabla."""
    with open(DATOS / "equipos.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tabla():
    with open(DATOS / "liga_o26_renna_tabla.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cara_a_cara():
    """(orden, {fila: {columna: victorias de fila contra columna}})."""
    with open(DATOS / "h2h_victorias.csv", encoding="utf-8") as f:
        filas = list(csv.reader(f))
    orden = filas[0][1:]
    matriz = {r[0]: {c: (int(v) if v else None) for c, v in zip(orden, r[1:])}
              for r in filas[1:]}
    return orden, matriz


def corridas():
    with open(DATOS / "corridas_pct.csv", encoding="utf-8") as f:
        filas = list(csv.reader(f))
    return filas[0][1:], {r[0]: [float(v) for v in r[1:]] for r in filas[1:]}


def resumen():
    return json.loads((DATOS / "resumen.json").read_text(encoding="utf-8"))


def _num(x):
    """78.1 -> «78,1»."""
    return f"{x:.1f}".replace(".", ",")


# --------------------------------------------------------------------------
# escala horizontal de porcentaje, compartida por las dos graficas de barras

ETIQ = 180      # donde terminan los nombres
X0 = ETIQ + 10  # donde empieza el 0 %
ANCHO_EJE = 320  # las figuras de la unidad no pasan de 600 de ancho
FILA = 24
ARRIBA = 92


def _x(pct):
    return X0 + ANCHO_EJE * pct / 100


def _rejilla(alto_datos):
    out = []
    for p in range(0, 101, 10):
        rotulo = p % 20 == 0
        x = _x(p)
        out.append(linea(x, ARRIBA - 8, x, ARRIBA + alto_datos,
                         color=mezclar(LINEA, 0.55) if p != 50 else SUAVE,
                         grosor=1, guiones=None if p in (0, 50) else "3 4"))
        if rotulo:
            out.append(texto(x, ARRIBA + alto_datos + 20, f"{p} %", color=SUAVE, tam=12))
    return out


def _leyenda(y):
    x = 34
    return [punto(x, y - 4, 6, COLOR_ALUMNOS),
            texto(x + 12, y, "equipos de alumnos", color=TEXTO, tam=13, anclaje="start"),
            punto(x + 170, y - 4, 6, COLOR_REFERENCIA),
            texto(x + 182, y, "bots de referencia", color=TEXTO, tam=13, anclaje="start")]


def _nombre(y, equipo, lugar):
    return [texto(22, y + 5, str(lugar), color=SUAVE, tam=12, anclaje="end"),
            texto(ETIQ, y + 5, equipo, color=_color(equipo), tam=12,
                  anclaje="end", fuente=MONO,
                  peso="normal" if es_referencia(equipo) else "700")]


def jue_torneo_victorias():
    filas = equipos()
    alto_datos = FILA * len(filas)
    ancho, alto = 600, ARRIBA + alto_datos + 64
    out = [texto(24, 34, "Victorias por bot, con IC al 95 %",
                 tam=16, peso="700", anclaje="start")]
    out += _leyenda(64)
    out += _rejilla(alto_datos)
    for i, f in enumerate(filas):
        y = ARRIBA + FILA * i + FILA / 2
        pct, bajo, alto_ic = (float(f[k]) for k in ("pct_victorias", "ic95_bajo", "ic95_alto"))
        color = _color(f["equipo"])
        out += _nombre(y, f["equipo"], i + 1)
        out.append(f'<rect x="{X0}" y="{y - 7:.1f}" width="{_x(pct) - X0:.1f}" '
                   f'height="14" rx="3" fill="{mezclar(color, 0.55)}"/>')
        out.append(linea(f"{_x(bajo):.1f}", y, f"{_x(alto_ic):.1f}", y, color=TEXTO, grosor=2))
        for extremo in (bajo, alto_ic):
            out.append(linea(f"{_x(extremo):.1f}", y - 5, f"{_x(extremo):.1f}", y + 5,
                             color=TEXTO, grosor=2))
        out.append(texto(f"{_x(alto_ic) + 8:.1f}", y + 5, f"{_num(pct)} %", color=TEXTO,
                         tam=12, anclaje="start"))
    out.append(texto(X0 + ANCHO_EJE / 2, alto - 14,
                     "de 1 120 partidas por bot; la línea clara marca el 50 %",
                     color=SUAVE, tam=12))
    desc = ("Barras horizontales del porcentaje de victorias de los 29 bots, en el orden "
            "de la tabla, con su intervalo de confianza al 95 %. Va de "
            f"{_num(float(filas[0]['pct_victorias']))} % de {filas[0]['equipo']} a "
            f"{_num(float(filas[-1]['pct_victorias']))} % de {filas[-1]['equipo']}.")
    return "".join([marco(ancho, alto, desc, "Porcentaje de victorias por bot", desc)]
                   + out + [cierre()])


def jue_torneo_corridas():
    nombres_corridas, pct = corridas()
    filas = equipos()
    alto_datos = FILA * len(filas)
    ancho, alto = 600, ARRIBA + alto_datos + 64
    out = [texto(24, 34, f"Victorias en las {len(nombres_corridas)} corridas",
                 tam=16, peso="700", anclaje="start")]
    out += _leyenda(64)
    out += _rejilla(alto_datos)
    for i, f in enumerate(filas):
        e = f["equipo"]
        y = ARRIBA + FILA * i + FILA / 2
        valores = pct[e]
        color = _color(e)
        out += _nombre(y, e, i + 1)
        out.append(linea(f"{_x(min(valores)):.1f}", y, f"{_x(max(valores)):.1f}", y,
                         color=mezclar(color, 0.6), grosor=6))
        for v in valores:
            out.append(punto(f"{_x(v):.1f}", y, 3.5, color))
        out.append(linea(f"{_x(float(f['pct_victorias'])):.1f}", y - 8,
                         f"{_x(float(f['pct_victorias'])):.1f}", y + 8, color=TEXTO, grosor=2))
        out.append(texto(f"{_x(max(valores)) + 8:.1f}", y + 5,
                         f"{_num(min(valores))}–{_num(max(valores))}",
                         color=SUAVE, tam=12, anclaje="start"))
    out.append(texto(X0 + ANCHO_EJE / 2, alto - 14,
                     "cada punto, una corrida de 160 partidas; la raya, el total",
                     color=SUAVE, tam=12))
    desc = ("Para cada uno de los 29 bots, sus porcentajes de victorias en las "
            f"{len(nombres_corridas)} corridas como puntos sobre una franja que va del "
            "mínimo al máximo, y una raya en el porcentaje total.")
    return "".join([marco(ancho, alto, desc, "Estabilidad entre corridas", desc)]
                   + out + [cierre()])


# --------------------------------------------------------------------------
# mapa de calor cara a cara

CELDA = 18


def _color_celda(v, total=40):
    """Verde si la fila gano la serie, magenta si la perdio, gris si empato."""
    if v is None:
        return mezclar(LINEA, 0.25), SUAVE
    margen = (v - total / 2) / (total / 2)       # -1 .. 1
    if not margen:
        return mezclar(LINEA, 0.6), TEXTO
    base = SERIE[0] if margen > 0 else ACENTO
    fuerza = abs(margen)
    letra = "#211033" if fuerza > 0.55 else TEXTO
    return mezclar(base, 0.12 + 0.78 * fuerza), letra


def jue_torneo_cara_a_cara():
    """Filas y columnas se rotulan con el lugar en la tabla: a 600 de ancho
    no caben 29 nombres de columna con letra legible."""
    orden, m = cara_a_cara()
    n = len(orden)
    izq, arriba = 50, 118
    ancho, alto = 600, arriba + CELDA * n + 56
    out = [texto(24, 34, "Cara a cara, de 40 partidas",
                 tam=16, peso="700", anclaje="start"),
           texto(24, 58, "verde, la fila ganó la serie; magenta, la perdió",
                 color=SUAVE, tam=13, anclaje="start"),
           texto(izq + CELDA * n / 2, 86, "columna: lugar del rival en la tabla →",
                 color=SUAVE, tam=12),
           f'<text x="16" y="{arriba + CELDA * n / 2}" fill="{SUAVE}" font-family="{MONO}" '
           f'font-size="12" text-anchor="middle" '
           f'transform="rotate(-90 16 {arriba + CELDA * n / 2})">'
           f'fila: lugar del equipo que gana →</text>'.replace(MONO, "system-ui, sans-serif")]
    for k, e in enumerate(orden):
        x = izq + CELDA * k + CELDA / 2
        out.append(texto(x, arriba - 8, str(k + 1), color=_color(e), tam=12))
        out.append(texto(izq - 6, arriba + CELDA * k + CELDA / 2 + 4, str(k + 1),
                         color=_color(e), tam=12, anclaje="end"))
    for i, fila in enumerate(orden):
        y = arriba + CELDA * i
        for k, col in enumerate(orden):
            v = m[fila][col]
            relleno, letra = _color_celda(v)
            x = izq + CELDA * k
            out.append(f'<rect x="{x}" y="{y}" width="{CELDA - 1}" height="{CELDA - 1}" '
                       f'fill="{relleno}"/>')
            if v is not None:
                out.append(texto(x + CELDA / 2 - 0.5, y + CELDA / 2 + 4, str(v),
                                 color=letra, tam=12))
    out.append(texto(izq + CELDA * n / 2, alto - 20,
                     "los números son los lugares de la tabla; azul, bot de referencia",
                     color=SUAVE, tam=12))
    desc = ("Mapa de calor de 29 por 29, con filas y columnas rotuladas por el lugar en "
            "la tabla: en cada celda, cuántas de las 40 partidas de la serie ganó el "
            "equipo de la fila contra el de la columna.")
    return "".join([marco(ancho, alto, desc, "Cara a cara", desc)] + out + [cierre()])


DIAGRAMAS = {
    "jue-torneo-victorias": jue_torneo_victorias,
    "jue-torneo-cara-a-cara": jue_torneo_cara_a_cara,
    "jue-torneo-corridas": jue_torneo_corridas,
}
