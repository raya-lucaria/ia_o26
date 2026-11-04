"""Arma los notebooks de la unidad 9 (aprendizaje de máquina) para Colab.

Cada notebook sale de dos archivos con dueño distinto (contrato §6.1):

    tools/cuadernos_ml/<stem>.py        orden de celdas y código (prog-cN)
    tools/cuadernos_ml/<stem>.texto.md  todo el texto visible, el guion

`<stem>.py` va en formato «percent»: cada celda abre con un marcador
`# %% [codigo] <clave>`, `# %% [codigo-visible] <clave>` o
`# %% [texto] <clave>` (este último con el cuerpo vacío). El guion trae un
`### celda: <clave>` por cada celda de texto. El generador recorre el `.py`,
pone en cada hueco de texto su sección del guion, agrega el badge de Colab a
la portada y, como segunda celda, la de arranque: colapsada, carga `ml_lab`
(copia local, la del repositorio o el respaldo incrustado, en ese orden) y
llama `ml.requiere(...)` con la versión con que se generó.

El respaldo va **incrustado completo** (zlib + base64 del texto de
tools/aprendizaje_maquina.py): DECISIÓN prog-lab-cuadernos-1 sobre D-006.

Uso:
    python3 tools/gen_cuadernos_ml.py                 # todos (o los de ML_CLASES)
    python3 tools/gen_cuadernos_ml.py --clase 2       # solo los de la clase 2
    python3 tools/gen_cuadernos_ml.py 03_entrenamiento_y_prueba   # uno
    python3 tools/gen_cuadernos_ml.py --solo-codigo 01_que_es_f   # sin guion, a /tmp
    python3 tools/gen_cuadernos_ml.py _humo           # el de humo, a /tmp

Sin argumentos lee `ML_CLASES` (números de clase separados por comas): con
la variable puesta genera solo esas clases; un argumento explícito manda
sobre ella. Escribe en course/9_aprendizaje_maquina/_assets/<stem>.ipynb,
sin salidas, de forma determinista; test_cuadernos_ml.py compara sin
escribir. Los stems que empiezan con `_` (el de humo) son de tools/ y nunca
se publican: se escriben en un directorio temporal, como `--solo-codigo`.
"""
import argparse
import base64
import json
import os
import re
import sys
import tempfile
import zlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "tools" / "cuadernos_ml"
ASSETS_ML = RAIZ / "course/9_aprendizaje_maquina/_assets"
LAB = RAIZ / "tools" / "aprendizaje_maquina.py"

# Contrato §1.5: qué notebooks lleva cada clase (la clase 0 no lleva).
CUADERNOS = {
    1: ["01_que_es_f", "02_polinomios_y_capacidad", "tarea_1_proponer_phi"],
    2: ["03_entrenamiento_y_prueba", "04_validacion_cruzada",
        "05_sesgo_y_varianza", "tarea_2_separar_y_elegir"],
    3: ["06_leer_el_error", "07_el_lagrangeano_en_accion",
        "tarea_3_cincuenta_variables"],
    4: ["08_perdida_metrica_y_desbalanceo", "09_calibracion_y_conformal",
        "tarea_4_desbalanceo_multiclase"],
    5: ["10_son_iid_y_fugas", "tarea_5a_series_de_tiempo", "tarea_5b_fugas",
        "tarea_5c_otras_familias"],
}
# Notebooks de tools/ que nunca se publican, con la clase cuya notación usan.
CUADERNOS_HERRAMIENTA = {"_humo": 1}

URL_COLAB = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
             "blob/main/course/9_aprendizaje_maquina/_assets/{stem}.ipynb")
# Badge grande a propósito: el profesor lo pidió visible desde lejos al proyectar.
BADGE = ('<a href="{url}" target="_blank"><img src="https://colab.research.google.com/'
         'assets/colab-badge.svg" alt="Abrir en Colab" width="300"></a>')
URL_LAB = ("https://raw.githubusercontent.com/raya-lucaria/ia_o26/main/"
           "course/9_aprendizaje_maquina/_assets/ml_lab.py")

MARCADOR = re.compile(r"^# %% \[(codigo|codigo-visible|texto)\] ([a-z0-9-]+)\s*$")
SECCION = re.compile(r"^### celda: ([a-z0-9-]+)\s*$")


def clase_de(stem):
    """La clase dueña de un stem (los de tools/ dicen la de su notación)."""
    if stem in CUADERNOS_HERRAMIENTA:
        return CUADERNOS_HERRAMIENTA[stem]
    for clase, stems in CUADERNOS.items():
        if stem in stems:
            return clase
    raise KeyError(f"{stem}: no está en CUADERNOS (contrato §1.5)")


def es_tarea(stem):
    return stem.startswith("tarea_")


def es_herramienta(stem):
    return stem.startswith("_")


# --- Lectura de las dos fuentes -------------------------------------------

def leer_celdas(texto, nombre="<stem>.py"):
    """Las celdas de un `.py` percent: [(tipo, clave, cuerpo)], en orden."""
    celdas, actual = [], None
    for n, linea in enumerate(texto.split("\n"), 1):
        m = MARCADOR.match(linea)
        if m:
            actual = [m.group(1), m.group(2), []]
            celdas.append(actual)
        elif linea.startswith("# %%"):
            raise ValueError(f"{nombre}:{n}: marcador mal formado: {linea!r}")
        elif actual is None:
            if linea.strip() and not linea.startswith("#"):
                raise ValueError(f"{nombre}:{n}: código antes del primer "
                                 "marcador")
        else:
            actual[2].append(linea)
    salida = []
    for tipo, clave, lineas in celdas:
        cuerpo = "\n".join(lineas).strip("\n")
        if tipo == "texto" and cuerpo.strip():
            raise ValueError(f"{nombre}: la celda [texto] {clave} lleva cuerpo; "
                             "el texto va en el guion")
        salida.append((tipo, clave, cuerpo))
    return salida


def leer_guion(texto, nombre="<stem>.texto.md"):
    """Las secciones del guion: [(clave, markdown)], en orden.

    Antes del primer `### celda:` solo valen líneas vacías o comentarios
    HTML (una nota para quien redacta); dentro de una sección no hay `###`.
    """
    secciones, actual, preambulo = [], None, []
    for linea in texto.split("\n"):
        m = SECCION.match(linea)
        if m:
            actual = [m.group(1), []]
            secciones.append(actual)
        elif actual is None:
            preambulo.append(linea)
        else:
            actual[1].append(linea)
    resto = re.sub(r"<!--.*?-->", "", "\n".join(preambulo), flags=re.S)
    if resto.strip():
        raise ValueError(f"{nombre}: texto antes del primer «### celda:»")
    return [(clave, "\n".join(lineas).strip("\n")) for clave, lineas in secciones]


def fuente_py(stem, fuentes=None):
    return (Path(fuentes or FUENTES) / f"{stem}.py").read_text(encoding="utf-8")


def fuente_guion(stem, fuentes=None):
    return (Path(fuentes or FUENTES) / f"{stem}.texto.md").read_text(encoding="utf-8")


# --- La celda de arranque (contrato §6.2) ----------------------------------

def version_de(texto_lab):
    m = re.search(r'^VERSION\s*=\s*"(\d+\.\d+)"', texto_lab, re.M)
    if not m:
        raise ValueError("el ml_lab no declara VERSION = \"X.Y\"")
    return m.group(1)


def respaldo(texto_lab):
    """El texto de ml_lab comprimido con zlib (nivel 9) y en base64."""
    datos = zlib.compress(texto_lab.encode("utf-8"), 9)
    return base64.b64encode(datos).decode("ascii")


def celda_arranque(texto_lab):
    requiere = version_de(texto_lab)
    return f'''#@title ▶ Corre esta celda primero
import os, sys, glob, base64, zlib, importlib, urllib.request
URL = os.environ.get("ML_LAB_URL",
      "{URL_LAB[:62]}"
      "{URL_LAB[62:]}")
REQUIERE = "{requiere}"                     # la versión con que se generó este notebook
_RESPALDO = "{respaldo(texto_lab)}"

def _v(texto): return tuple(int(p) for p in texto.split("."))

def _sirve(version):                 # misma X y una Y mayor o igual
    (x, y), (x0, y0) = _v(version), _v(REQUIERE)
    return x == x0 and y >= y0

def _cargar():                       # importa ml_lab DE CERO (sin la copia en memoria)
    sys.modules.pop("ml_lab", None)
    for viejo in glob.glob("__pycache__/ml_lab.*.pyc"):
        os.remove(viejo)             # un .pyc de la copia vieja taparía la nueva
    importlib.invalidate_caches()
    import ml_lab
    return ml_lab if _sirve(ml_lab.VERSION) else None

ml = None
if os.path.exists("ml_lab.py"):      # 1) la copia local, si ya es nueva
    try: ml = _cargar()
    except Exception: ml = None
if ml is None:                       # 2) la del repositorio
    try:
        urllib.request.urlretrieve(URL, "ml_lab.py"); ml = _cargar()
    except Exception: ml = None
if ml is None:                       # 3) el respaldo: sin red o repo aún sin esta versión
    with open("ml_lab.py", "wb") as archivo:
        archivo.write(zlib.decompress(base64.b64decode(_RESPALDO)))
    ml = _cargar()
ml.requiere(REQUIERE)
ml.tema("claro")
from ml_lab import *
print(f"Listo: ml_lab {{ml.VERSION}}")'''


# --- Armado ----------------------------------------------------------------

ABRE_PRUEBA = re.compile(r"^# abre-prueba: \S")


def titulo_primero(cuerpo):
    """`# abre-prueba:` va justo tras el marcador en el `.py` (§6.6 regla 8),
    pero Colab solo pliega la celda si `#@title` es su primera línea: en el
    notebook las dos líneas se intercambian."""
    lineas = cuerpo.split("\n")
    if (len(lineas) > 1 and ABRE_PRUEBA.match(lineas[0])
            and lineas[1].startswith("#@title")):
        lineas[0], lineas[1] = lineas[1], lineas[0]
    return "\n".join(lineas)


def _md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto}


def _codigo(texto, colapsada):
    meta = {"cellView": "form"} if colapsada else {}
    return {"cell_type": "code", "execution_count": None, "metadata": meta,
            "outputs": [], "source": texto}


def _lineas(texto):
    partes = texto.split("\n")
    return [p + "\n" for p in partes[:-1]] + [partes[-1]]


def cuaderno(stem, *, solo_codigo=False, fuentes=None, lab=None):
    """El notebook de `stem` como dict nbformat 4, sin salidas.

    `solo_codigo=True` deja cada hueco de texto con solo su clave (S1, antes
    de que exista el guion). `fuentes` y `lab` existen para las pruebas.
    """
    celdas_py = leer_celdas(fuente_py(stem, fuentes), f"{stem}.py")
    guion = {} if solo_codigo else dict(
        leer_guion(fuente_guion(stem, fuentes), f"{stem}.texto.md"))
    lab = Path(lab or LAB)
    if not lab.exists():
        raise FileNotFoundError(f"falta {lab}: el respaldo incrustado es el "
                                "texto de ml_lab (U.T2a)")
    texto_lab = lab.read_text(encoding="utf-8")
    celdas = []
    for tipo, clave, cuerpo in celdas_py:
        if tipo == "texto":
            if solo_codigo:
                md = f"`{clave}`"
            elif clave not in guion:
                raise KeyError(f"{stem}: el guion no trae «### celda: {clave}»")
            else:
                md = guion[clave]
            if clave == "portada":
                url = URL_COLAB.format(stem=stem)
                md = BADGE.format(url=url) + "\n\n" + md
            celdas.append(_md(md))
            if clave == "portada":
                celdas.append(_codigo(celda_arranque(texto_lab), True))
        else:
            cuerpo = titulo_primero(cuerpo)
            colapsada = cuerpo.startswith("#@title")
            celdas.append(_codigo(cuerpo, colapsada))
    for c in celdas:
        c["source"] = _lineas(c["source"])
    return {"cells": celdas,
            "metadata": {"colab": {"provenance": [], "toc_visible": True},
                         "kernelspec": {"display_name": "Python 3",
                                        "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 0}


def serializar(nb):
    return json.dumps(nb, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# --- Qué generar -----------------------------------------------------------

def clases_de_entorno(valor):
    """`ML_CLASES` → conjunto de clases (None si no está puesta)."""
    if valor is None or not valor.strip():
        return None
    clases = set()
    for parte in valor.split(","):
        parte = parte.strip()
        if parte.isdigit():
            clases.add(int(parte))
        elif parte != "u":           # `u` es de las figuras de la unidad
            raise ValueError(f"ML_CLASES: «{parte}» no es un número de clase")
    return clases


def stems_existentes(fuentes=None):
    """Los stems publicables que ya tienen su `<stem>.py`, en orden de clase."""
    return [s for clase in sorted(CUADERNOS) for s in CUADERNOS[clase]
            if (Path(fuentes or FUENTES) / f"{s}.py").exists()]


def seleccion(clases=None, existentes=None):
    """Los stems a generar: todos los existentes, o solo los de `clases`."""
    existentes = stems_existentes() if existentes is None else existentes
    if clases is None:
        return list(existentes)
    return [s for s in existentes if clase_de(s) in clases]


def destino(stem):
    return ASSETS_ML / f"{stem}.ipynb"


def escribir(stem, ruta, **kw):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(serializar(cuaderno(stem, **kw)), encoding="utf-8")
    return ruta


def main(argv=None, entorno=None):
    entorno = os.environ if entorno is None else entorno
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("stems", nargs="*", help="stems a generar")
    p.add_argument("--clase", type=int, action="append",
                   help="solo los notebooks de esta clase (repetible)")
    p.add_argument("--solo-codigo", metavar="STEM",
                   help="arma STEM sin guion, fuera de _assets/")
    p.add_argument("--destino", help="directorio de salida para --solo-codigo "
                   "y los stems de tools/ (por omisión, uno temporal)")
    a = p.parse_args(argv)

    if a.solo_codigo:
        base = Path(a.destino or tempfile.mkdtemp(prefix="cuaderno_ml_"))
        ruta = escribir(a.solo_codigo, base / f"{a.solo_codigo}.ipynb",
                        solo_codigo=True)
        print(f"escrito (sin guion, no se comitea) {ruta}")
        return 0
    if a.stems:
        stems = a.stems
    elif a.clase:
        stems = seleccion(set(a.clase))
    else:
        stems = seleccion(clases_de_entorno(entorno.get("ML_CLASES")))
    for stem in stems:
        clase_de(stem)
        if es_herramienta(stem):
            base = Path(a.destino or tempfile.mkdtemp(prefix="cuaderno_ml_"))
            ruta = escribir(stem, base / f"{stem}.ipynb")
            print(f"escrito (de tools/, no se publica) {ruta}")
        else:
            ruta = escribir(stem, destino(stem))
            print(f"escrito {ruta.relative_to(RAIZ)}")
    if not stems:
        print("ningún notebook que generar (no hay tools/cuadernos_ml/<stem>.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
