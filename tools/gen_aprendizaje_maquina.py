"""Genera las figuras de la unidad de aprendizaje de maquina (unidad 9).

Es el generador comun de la unidad (contrato §7.1). Lo que vive aqui:

- La **paleta del sitio** (skin eva-cyberpunk; FONDO es tokens.color.surface
  y va horneado en cada SVG: test_9 de test_aceptacion.py falla sin el) y
  los **roles de §7.3** (ROLES): marca, trazo y color de cada papel que un
  dato juega en una figura. Ninguna figura copia un literal de color de rol;
  lo lee de ROLES. ml_lab.ROLES repite los mismos roles para el tema claro.
- Las **primitivas de dibujo** (marco, texto, caja, flecha, linea,
  mezclar...) para los diagramas escritos a mano, con el patron de
  gen_markov.py / gen_optimizacion.py.
- El **posproceso SVG** de matplotlib (svg_de_matplotlib / posprocesar_svg):
  quita el prologo (<?xml?>, <!DOCTYPE>, comentarios), deja el archivo
  empezando con <svg y pone en la raiz width/height en px, viewBox,
  role, aria-label, <title> y el <rect fill="#211033"/> de fondo.
- El **catalogo**: FIGURAS_U (las figuras de las paginas de la unidad, hoy
  solo ml-u-mapa) mas los seis FIGURAS_C<N> de tools/figuras_ml_c<N>.py,
  uno por clase y cada uno de su prog-cN. figuras() los une; un id repetido
  o un id sin el prefijo de su clase es un error, y un modulo de
  MODULOS_FIGURAS que falta tambien (no un catalogo vacio silencioso).

Importacion perezosa (contrato §7.1, r1-34): este modulo no importa ml_lab
(tools/aprendizaje_maquina.py) ni matplotlib al cargarse. ml_lab() y
svg_de_matplotlib() los importan cuando una figura los necesita, de modo que
FIGURAS_U y FIGURAS_C0 se generan y se prueban sin ellos.

Uso (contrato §7.1, r1-56 y r2-24):

    python3 tools/gen_aprendizaje_maquina.py              # todo, o lo que diga ML_CLASES
    python3 tools/gen_aprendizaje_maquina.py --clase 2    # solo FIGURAS_C2
    python3 tools/gen_aprendizaje_maquina.py --unidad     # solo FIGURAS_U
    ML_CLASES=2,u python3 tools/gen_aprendizaje_maquina.py

ML_CLASES es una lista separada por comas de numeros de clase (0 a 5) y
«u» para FIGURAS_U. Solo se lee cuando no hay argumentos: un --clase o
--unidad explicito manda sobre la variable. Asi
`ML_CLASES=N .claude/skills/unidad/scripts/generadores_limpios.sh ...`
regenera solo la clase N en una rama de clase.

contenido(id) devuelve el SVG sin escribirlo: test_gen_aprendizaje_maquina.py
lo compara byte a byte con el archivo comiteado en
course/9_aprendizaje_maquina/_assets/ (si alguien lo edita a mano, la prueba
falla con «corre el generador»).
"""
import argparse
import colorsys
import importlib
import io
import os
import re
import sys
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD_ML = RAIZ / "course/9_aprendizaje_maquina"
ASSETS_ML = UNIDAD_ML / "_assets"

# ------------------------------------------------------------- paleta ---
#
# Skin eva-cyberpunk (skins/eva-cyberpunk.yaml). FONDO y PANEL son los de
# gen_regresion_experimentos.py (contrato §7.3): fondo de la figura y fondo
# de los ejes de una grafica de datos.
FONDO = "#211033"   # tokens.color.surface
PANEL = "#2e1945"
TEXTO = "#f7f2ff"   # tokens.color.text
SUAVE = "#c8b9d8"   # tokens.color.muted
LINEA = "#78419e"   # tokens.color.border
ACENTO = "#f04cff"  # tokens.color.accent
REJILLA = "#665075"
FUENTE = "system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

# Ancho maximo de una figura (contrato §7.1; figuras.md) y letra minima a
# ese ancho. Las guardas comunes los exigen a toda figura del catalogo.
ANCHO_MAX = 600
LETRA_MIN = 12


def mezclar(color, fraccion, fondo=FONDO):
    """Color solido equivalente a pintar `color` con opacidad `fraccion`.

    La transparencia se hornea aqui en vez de emitir fill-opacity: un
    sombreado translucido encima de otra curva la tapa en renderizadores que
    ignoran la opacidad, y eso ya se publico una vez en la unidad de
    complejidad. Las guardas comunes prohiben cualquier opacidad en un SVG.
    """
    def canales(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

    c0, c1 = canales(fondo), canales(color)
    return "#%02x%02x%02x" % tuple(
        round(a + (b - a) * fraccion) for a, b in zip(c0, c1))


# -------------------------------------------------------------- roles ---
#
# Contrato §7.3: una sola leyenda para toda la unidad. Cada rol lleva marca o
# trazo ademas del color (el color nunca es la unica senal). Los campos
# `marcador` y `linea` usan los codigos de matplotlib ("o", "^", "s", "."; "-",
# "--", ":", "-.") para que una grafica de datos los pase tal cual; `guiones`
# es el stroke-dasharray equivalente para un diagrama SVG a mano.
#
# observaciones_nuevas: casos que el ajuste no vio, sacados de la realidad,
# antes de que exista la prueba (clases 0 y 1). Crema con la transparencia
# horneada contra el fondo (sin fill-opacity).
# benchmark: la media o la moda de entrenamiento; magenta = accent del skin.
# Comprobado: 5.4:1 contra PANEL y a ~45 grados de tono del rosa de prueba
# (test_gen_aprendizaje_maquina.py lo vigila).
ROLES = {
    "entrenamiento": {
        "nombre": "entrenamiento", "marcador": "o", "simbolo": "●",
        "linea": None, "guiones": None, "grosor": None, "color": "#64dce3"},
    "validacion": {
        "nombre": "validación / CV", "marcador": "^", "simbolo": "▲",
        "linea": None, "guiones": None, "grosor": None, "color": "#ffd166"},
    "prueba": {
        "nombre": "prueba", "marcador": "s", "simbolo": "■",
        "linea": None, "guiones": None, "grosor": None, "color": "#ff87ad"},
    "realidad": {
        "nombre": "realidad / riesgo R", "marcador": None, "simbolo": "– –",
        "linea": "--", "guiones": "8 5", "grosor": 2, "color": "#fff8ed"},
    "f_verdadera": {
        "nombre": "f verdadera", "marcador": None, "simbolo": "━",
        "linea": "-", "guiones": None, "grosor": 3.5, "color": "#a9e88f"},
    "f_estimada": {
        "nombre": "f estimada", "marcador": None, "simbolo": "─",
        "linea": "-", "guiones": None, "grosor": 1.5, "color": "#64dce3"},
    "piso_bayes": {
        "nombre": "piso R_Bayes", "marcador": None, "simbolo": "···",
        "linea": ":", "guiones": "2 4", "grosor": 2, "color": "#dfd0e8"},
    "observaciones_nuevas": {
        "nombre": "observaciones nuevas", "marcador": ".", "simbolo": "·",
        "linea": None, "guiones": None, "grosor": None,
        "color": mezclar("#fff8ed", 0.6)},
    "benchmark": {
        "nombre": "benchmark", "marcador": None, "simbolo": "–·–",
        "linea": "-.", "guiones": "10 4 2 4", "grosor": 2, "color": ACENTO},
}


def color_rol(rol):
    return ROLES[rol]["color"]


# Tono (grados) de un color: lo usan las guardas para comprobar que el
# magenta del benchmark se distingue del rosa de prueba.
def tono(color):
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360


# ----------------------------------------------------------- primitivas ---

def _n(v):
    """Coordenada redondeada a 0.1, sin ceros de sobra (salida estable)."""
    v = round(float(v), 1)
    return str(int(v)) if v == int(v) else str(v)


def marco(ancho, alto, aria, titulo, desc=None):
    """Etiqueta <svg> raiz con lo que exigen las guardas: width/height en px,
    viewBox, role, aria-label, <title>, <desc> y el fondo del skin."""
    desc = aria if desc is None else desc
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(ancho)}" '
        f'height="{_n(alto)}" viewBox="0 0 {_n(ancho)} {_n(alto)}" role="img" '
        f'aria-label="{escape(aria, {chr(34): "&quot;"})}">'
        f"<title>{escape(titulo)}</title><desc>{escape(desc)}</desc>"
        f'<rect x="0" y="0" width="{_n(ancho)}" height="{_n(alto)}" rx="16" '
        f'fill="{FONDO}"/>'
        f'<defs><marker id="p" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{ACENTO}"/></marker>'
        f'<marker id="s" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{SUAVE}"/></marker></defs>'
    )


def cierre():
    return "</svg>"


def texto(x, y, s, color=TEXTO, tam=14, anclaje="middle", peso="normal",
          estilo="normal", fuente=FUENTE):
    """Un renglon. `s` puede ser una cadena o una lista de trozos
    (cadena, o (cadena, {"estilo": "italic", "peso": "700", "color": ...}))
    para poner en cursiva una letra matematica dentro del renglon."""
    attrs = (f'x="{_n(x)}" y="{_n(y)}" fill="{color}" font-family="{fuente}" '
             f'font-size="{_n(tam)}" text-anchor="{anclaje}"')
    if peso != "normal":
        attrs += f' font-weight="{peso}"'
    if estilo != "normal":
        attrs += f' font-style="{estilo}"'
    if isinstance(s, str):
        return f"<text {attrs}>{escape(s)}</text>"
    partes = []
    for trozo in s:
        if isinstance(trozo, str):
            partes.append(escape(trozo))
            continue
        cadena, fmt = trozo
        extra = ""
        if "estilo" in fmt:
            extra += f' font-style="{fmt["estilo"]}"'
        if "peso" in fmt:
            extra += f' font-weight="{fmt["peso"]}"'
        if "color" in fmt:
            extra += f' fill="{fmt["color"]}"'
        partes.append(f"<tspan{extra}>{escape(cadena)}</tspan>")
    return f"<text {attrs}>{''.join(partes)}</text>"


def caja(x, y, w, h, relleno="none", borde=LINEA, radio=10, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" '
            f'rx="{_n(radio)}" fill="{relleno}" stroke="{borde}" '
            f'stroke-width="{_n(grosor)}"{trazo}/>')


def linea(x1, y1, x2, y2, color=LINEA, grosor=2, guiones=None):
    trazo = f' stroke-dasharray="{guiones}"' if guiones else ""
    return (f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
            f'stroke="{color}" stroke-width="{_n(grosor)}"{trazo}/>')


def flecha(x1, y1, x2, y2, color=ACENTO, grosor=2):
    """Flecha recta; la punta es el marcador del mismo color (ACENTO o SUAVE)."""
    marcador = "p" if color == ACENTO else "s"
    return (f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" '
            f'stroke="{color}" stroke-width="{_n(grosor)}" '
            f'marker-end="url(#{marcador})"/>')


def svg(ancho, alto, aria, titulo, cuerpo, desc=None):
    return "".join([marco(ancho, alto, aria, titulo, desc)] + list(cuerpo) + [cierre()])


# ------------------------------------------------- ml_lab y matplotlib ---

def ml_lab():
    """tools/aprendizaje_maquina.py, importado solo cuando una figura lo pide."""
    return importlib.import_module("aprendizaje_maquina")


# Parametros de matplotlib que hacen el SVG determinista y legible en el
# sitio: texto como <text> (no trazos), ids con sal fija, sin fecha, leyenda
# opaca (la guarda comun prohibe cualquier opacidad) y la paleta del skin.
RC_SITIO = {
    "svg.fonttype": "none",
    "svg.hashsalt": "ml",
    "figure.facecolor": FONDO,
    "savefig.facecolor": FONDO,
    "axes.facecolor": PANEL,
    "axes.edgecolor": SUAVE,
    "axes.labelcolor": TEXTO,
    "text.color": TEXTO,
    "xtick.color": SUAVE,
    "ytick.color": SUAVE,
    "grid.color": REJILLA,
    "legend.framealpha": 1.0,
    "legend.facecolor": PANEL,
    "legend.edgecolor": LINEA,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 13,
}

_PROLOGO = re.compile(r"\A(?:\s|<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->)*", re.S)
_RAIZ = re.compile(r"<svg\b[^>]*>")


def _atributo(etiqueta, nombre):
    m = re.search(rf'\s{re.escape(nombre)}="([^"]*)"', etiqueta)
    return m.group(1) if m else None


def posprocesar_svg(texto_svg, aria, titulo=None, ancho=None):
    """Deja un SVG de matplotlib como lo piden las guardas del curso.

    - Quita el prologo (<?xml ...?>, <!DOCTYPE ...>, comentarios previos): el
      archivo empieza con <svg, porque test_9 usa re.match(r"<svg\\b[^>]*>").
    - Reescribe la etiqueta raiz: xmlns (y xmlns:xlink si estaba),
      width/height en px enteros, el viewBox original, role="img" y
      aria-label. `ancho` (px) fija el ancho y escala el alto; sin el, el
      ancho es el del viewBox (puntos de matplotlib, que el navegador trata
      como px de usuario).
    - Agrega <title> y un <rect fill="#211033"/> que cubre el viewBox.
    """
    sin_prologo = _PROLOGO.sub("", texto_svg, count=1)
    raiz = _RAIZ.match(sin_prologo)
    if not raiz:
        raise ValueError("el SVG no empieza con <svg tras quitar el prologo")
    etiqueta = raiz.group()
    caja_vista = _atributo(etiqueta, "viewBox")
    if caja_vista is None:
        raise ValueError("el SVG de matplotlib no trae viewBox")
    x0, y0, vw, vh = (float(v) for v in caja_vista.split())
    w = round(ancho) if ancho else round(vw)
    h = round(w * vh / vw)
    if w > ANCHO_MAX:
        raise ValueError(f"ancho {w} px > {ANCHO_MAX}: pasa ancho=")
    xlink = ' xmlns:xlink="http://www.w3.org/1999/xlink"' if "xmlns:xlink" in etiqueta else ""
    nueva = (
        f'<svg xmlns="http://www.w3.org/2000/svg"{xlink} width="{w}" height="{h}" '
        f'viewBox="{caja_vista}" role="img" aria-label="{escape(aria, {chr(34): "&quot;"})}">'
        f"<title>{escape(titulo if titulo is not None else aria)}</title>"
        f'<rect x="{_n(x0)}" y="{_n(y0)}" width="{_n(vw)}" height="{_n(vh)}" '
        f'fill="{FONDO}"/>'
    )
    cuerpo = sin_prologo[raiz.end():]
    return nueva + cuerpo.rstrip() + "\n"


def svg_de_matplotlib(fig, aria, titulo=None, ancho=None):
    """Guarda `fig` como SVG determinista y lo posprocesa. Cierra la figura.

    Se llama dentro de una figura del catalogo que dibuja con las funciones
    dibujar_* de ml_lab (tema="sitio"); matplotlib se importa aqui, no al
    cargar el modulo.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    buf = io.StringIO()
    with matplotlib.rc_context({"svg.fonttype": "none", "svg.hashsalt": "ml"}):
        fig.savefig(buf, format="svg", metadata={"Date": None},
                    facecolor=FONDO)
    plt.close(fig)
    return posprocesar_svg(buf.getvalue(), aria, titulo=titulo, ancho=ancho)


# --------------------------------------------------------- figuras U ---
#
# ml-u-mapa: el mapa de las seis clases que usa el 0_index.md de la unidad
# (contrato §1.2, §7.1). Una columna de seis cajas en el orden de la unidad;
# cada una dice el nombre de la clase (el de su directorio y su titulo),
# la pregunta que contesta, y que se lleva el alumno (notebooks y tarea). La
# clase 0 va con borde punteado: es repaso, sin sesion ni notebook (D-008,
# D-011). Al pie, los tres hilos que recorren toda la unidad (diseno §0).
# Sin fechas (D-008).

MAPA_ANCHO = 360
MAPA_X0 = 16
MAPA_W = MAPA_ANCHO - 2 * MAPA_X0

_IT = {"estilo": "italic"}

MAPA_CLASES = (
    {"n": 0, "nombre": "Qué es aprender",
     "renglones": ["tarea, experiencia y desempeño;",
                   "supervisado o no supervisado"],
     "lleva": "repaso · sin notebook", "repaso": True},
    {"n": 1, "nombre": "El problema",
     "renglones": [["la ", ("f", _IT), " que no vemos: ", ("y", _IT), " = ",
                    ("f", _IT), "(", ("x", _IT), ") + ε,"],
                   "el error que nadie baja"],
     "lleva": "notebooks 01–02 · tarea 1"},
    {"n": 2, "nombre": "Separar los datos",
     "renglones": ["entrenamiento, validación y prueba:",
                   "medir lo que no vemos"],
     "lleva": "notebooks 03–05 · tarea 2"},
    {"n": 3, "nombre": "Leer el error y regularizar",
     "renglones": ["analizar el error; limitar la",
                   "capacidad con un lagrangeano"],
     "lleva": "notebooks 06–07 · tarea 3"},
    {"n": 4, "nombre": "Clasificación",
     "renglones": ["se entrena con una pérdida y se",
                   "juzga con una métrica; desbalanceo"],
     "lleva": "notebooks 08–09 · tarea 4"},
    {"n": 5, "nombre": "Supuestos y metodología",
     "renglones": ["¿son iid?, fugas, y un orden de",
                   "trabajo que evita casi todo error"],
     "lleva": "notebook 10 · tareas 5a–5c"},
)

MAPA_HILOS = ("el lagrangeano", "siempre contra un benchmark",
              "la muestra enorme: cuánto miente cada cifra")


def ml_u_mapa():
    cuerpo = []
    y = 34
    cuerpo.append(texto(MAPA_X0, y, "La unidad en seis clases", tam=18,
                        peso="700", anclaje="start"))
    y += 21
    cuerpo.append(texto(MAPA_X0, y, "de qué es aprender a trabajar sin engañarse",
                        color=SUAVE, tam=13, anclaje="start"))
    y += 18

    alto_caja = 100
    hueco = 26
    for k, clase in enumerate(MAPA_CLASES):
        top = y
        repaso = clase.get("repaso", False)
        cuerpo.append(caja(MAPA_X0, top, MAPA_W, alto_caja,
                           relleno=PANEL, borde=SUAVE if repaso else LINEA,
                           guiones="6 5" if repaso else None))
        # numero de clase en un circulo a la izquierda
        cx, cy = MAPA_X0 + 26, top + 30
        borde_num = SUAVE if repaso else ACENTO
        cuerpo.append(f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="15" fill="{FONDO}" '
                      f'stroke="{borde_num}" stroke-width="2"/>')
        cuerpo.append(texto(cx, cy + 5.5, str(clase["n"]), tam=16, peso="700",
                            color=borde_num))
        xt = MAPA_X0 + 52
        cuerpo.append(texto(xt, top + 26, f"Clase {clase['n']}", tam=12,
                            color=SUAVE, anclaje="start", peso="700"))
        cuerpo.append(texto(xt, top + 45, clase["nombre"], tam=16, peso="700",
                            anclaje="start"))
        yr = top + 66
        for r in clase["renglones"]:
            cuerpo.append(texto(MAPA_X0 + 14, yr, r, tam=13, anclaje="start"))
            yr += 17
        cuerpo.append(texto(MAPA_X0 + MAPA_W - 12, top + 26, clase["lleva"],
                            tam=12, color=SUAVE, anclaje="end"))
        y = top + alto_caja
        if k < len(MAPA_CLASES) - 1:
            xm = MAPA_X0 + 26
            cuerpo.append(flecha(xm, y + 2, xm, y + hueco - 3))
            y += hueco

    y += 30
    cuerpo.append(texto(MAPA_X0, y, "En todas las clases", tam=14, peso="700",
                        anclaje="start", color=ACENTO))
    y += 6
    for hilo in MAPA_HILOS:
        y += 19
        cuerpo.append(texto(MAPA_X0 + 4, y, f"·  {hilo}", tam=13, anclaje="start",
                            color=TEXTO))
    alto = y + 22

    aria = ("Mapa de la unidad de aprendizaje de máquina: seis clases en orden. "
            + " ".join(
                f"Clase {c['n']}, {c['nombre']}: {c['lleva']}." for c in MAPA_CLASES)
            + " En todas: " + "; ".join(MAPA_HILOS) + ".")
    return svg(MAPA_ANCHO, alto, aria, "La unidad en seis clases", cuerpo)


FIGURAS_U = {
    "ml-u-mapa": ml_u_mapa,
}

# ------------------------------------------------------------ catalogo ---

MODULOS_FIGURAS = [f"figuras_ml_c{n}" for n in range(6)]
CLASES = tuple(range(6))
CLAVE_UNIDAD = "u"


def prefijo(clave):
    return "ml-u-" if clave == CLAVE_UNIDAD else f"ml-c{clave}-"


def unir_catalogos(catalogos):
    """{clave: {id: funcion}} -> {id: funcion}, con las dos reglas del
    contrato §7.1: cada id lleva el prefijo de su catalogo y ningun id se
    repite entre catalogos."""
    todas = {}
    for clave, catalogo in catalogos.items():
        for ident, funcion in catalogo.items():
            if ident in todas:
                raise ValueError(f"{ident}: id repetido entre catalogos")
            if not ident.startswith(prefijo(clave)):
                raise ValueError(
                    f"{ident}: un id del catalogo {clave!r} empieza por {prefijo(clave)!r}")
            if not callable(funcion):
                raise TypeError(f"{ident}: la entrada del catalogo no es una funcion")
            todas[ident] = funcion
    return todas


def cargar_catalogos(modulos=None):
    """Importa los modulos de figuras de clase. Un modulo que falta, o que no
    exporta su FIGURAS_C<N> como dict, es un error."""
    modulos = MODULOS_FIGURAS if modulos is None else modulos
    catalogos = {CLAVE_UNIDAD: FIGURAS_U}
    for nombre in modulos:
        m = re.fullmatch(r"figuras_ml_c(\d)", nombre)
        if not m:
            raise ValueError(f"{nombre}: nombre de modulo de figuras invalido")
        n = int(m.group(1))
        modulo = importlib.import_module(nombre)  # ModuleNotFoundError si falta
        catalogo = getattr(modulo, f"FIGURAS_C{n}", None)
        if not isinstance(catalogo, dict):
            raise TypeError(f"{nombre}: falta FIGURAS_C{n} (un dict id -> funcion)")
        catalogos[n] = catalogo
    return catalogos


@lru_cache(maxsize=None)
def figuras_por_clave():
    """{"u": FIGURAS_U, 0: FIGURAS_C0, ..., 5: FIGURAS_C5}, validado."""
    catalogos = cargar_catalogos()
    unir_catalogos(catalogos)
    return catalogos


def figuras():
    """FIGURAS: la union de los siete catalogos, que comparten el script y las
    pruebas como unica fuente de «que figuras existen»."""
    return unir_catalogos(figuras_por_clave())


def __getattr__(nombre):
    # FIGURAS como atributo del modulo, calculado al pedirlo: los modulos de
    # clase pueden importar este generador (paleta, ROLES, primitivas) sin
    # caer en una importacion circular.
    if nombre == "FIGURAS":
        return figuras()
    raise AttributeError(nombre)


def clave_de(ident):
    m = re.match(r"ml-(u|c(\d))-", ident)
    if not m:
        raise ValueError(f"{ident}: id sin prefijo ml-u- ni ml-c<N>-")
    return CLAVE_UNIDAD if m.group(1) == "u" else int(m.group(2))


# ---------------------------------------------------------------- CLI ---

def parsear_ml_clases(valor):
    """"2" -> [2]; "1,3,u" -> [1, 3, "u"]. Vacio o con un elemento invalido:
    ValueError (mejor fallar que generar todo en una rama de clase)."""
    claves = []
    for parte in valor.split(","):
        parte = parte.strip().lower()
        if parte == CLAVE_UNIDAD:
            clave = CLAVE_UNIDAD
        elif parte.isdigit() and int(parte) in CLASES:
            clave = int(parte)
        else:
            raise ValueError(f"ML_CLASES={valor!r}: {parte!r} no es una clase (0-5) ni «u»")
        if clave not in claves:
            claves.append(clave)
    return claves


def claves_pedidas(argv, entorno):
    """Que catalogos genera una corrida. Los argumentos mandan sobre ML_CLASES;
    sin argumentos ni variable, todos."""
    p = argparse.ArgumentParser(prog="gen_aprendizaje_maquina.py",
                                description="Figuras de la unidad 9.")
    p.add_argument("--clase", type=int, action="append", choices=CLASES,
                   help="genera solo FIGURAS_C<N> (se puede repetir)")
    p.add_argument("--unidad", action="store_true", help="genera solo FIGURAS_U")
    args = p.parse_args(argv)
    if args.clase or args.unidad:
        claves = ([CLAVE_UNIDAD] if args.unidad else []) + list(dict.fromkeys(args.clase or []))
        return claves
    valor = entorno.get("ML_CLASES", "").strip()
    if valor:
        return parsear_ml_clases(valor)
    return [CLAVE_UNIDAD, *CLASES]


def ids_de(claves, catalogos=None):
    catalogos = figuras_por_clave() if catalogos is None else catalogos
    return [ident for clave in claves for ident in catalogos[clave]]


def contenido(ident):
    """El SVG de una figura, sin escribirlo."""
    todas = figuras()
    if ident not in todas:
        raise KeyError(f"figura desconocida: {ident}")
    return todas[ident]()


def escribir(ident, assets=None):
    assets = ASSETS_ML if assets is None else assets
    assets.mkdir(parents=True, exist_ok=True)
    ruta = assets / f"{ident}.svg"
    ruta.write_text(contenido(ident), encoding="utf-8")
    return ruta


def main(argv=None, entorno=None):
    argv = sys.argv[1:] if argv is None else argv
    entorno = os.environ if entorno is None else entorno
    try:
        claves = claves_pedidas(argv, entorno)
    except ValueError as e:
        raise SystemExit(str(e))
    for ident in ids_de(claves):
        print(escribir(ident))


if __name__ == "__main__":
    main()

