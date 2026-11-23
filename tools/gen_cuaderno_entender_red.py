"""Arma el notebook 02 de deep learning, «Entender una red», para Colab con GPU.

Las fuentes viven en tools/cuadernos_dl/02_entender_una_red/, un par por
sección (NN = 00…19):

    sNN_<slug>.py        orden de celdas y código, formato «percent»
    sNN_<slug>.texto.md  el texto de cada celda de markdown

En el `.py` cada celda abre con `# %% [codigo] sNN-<clave>`,
`# %% [texto] sNN-<clave>` (cuerpo vacío) o `# %% [plegada] sNN-<clave>`
(cuerpo vacío; su texto sale envuelto en un <details> «Respuesta»). El
`.texto.md` trae un `### celda: sNN-<clave>` por cada celda de texto o
plegada. Una ilustración se escribe `![alt](ilustracion:<nombre>)` y la
siguiente línea no vacía tiene que ser el aviso
`*(Ilustración generada con gpt-image-2.)*`; el generador la incrusta como
data URI desde ilustraciones/<nombre>.png.

Uso:
    python3 tools/gen_cuaderno_entender_red.py                  # el .ipynb, sin salidas
    python3 tools/gen_cuaderno_entender_red.py --script /tmp/humo.py \\
        --borrador --secciones 1,2,3,7                          # código plano
    python3 tools/gen_cuaderno_entender_red.py --integrar descarga.ipynb

`--borrador` admite «NOTA PARA SOL» y sustituye por un marcador la
ilustración que aún no existe. `--secciones` filtra; la sección 0 (portada)
siempre entra al notebook y nunca al script. `--fuentes DIR` y `--salida
RUTA` existen para las pruebas. `--integrar` exige que cada celda de código
de la descarga sea idéntica a la generada (el markdown puede diferir: gana
el del generador), conserva sus salidas y borra la metadata de la cuenta.
"""
import argparse
import base64
import copy
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = RAIZ / "tools" / "cuadernos_dl" / "02_entender_una_red"
RUTA_NB = "course/10_deep_learning/_assets/02_entender_una_red.ipynb"
DESTINO = RAIZ / RUTA_NB
URL_COLAB = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
             "blob/main/" + RUTA_NB)
BADGE = ("[![Abrir en Colab](https://colab.research.google.com/assets/"
         f"colab-badge.svg)]({URL_COLAB})")
AVISO = "*(Ilustración generada con gpt-image-2.)*"
NOTA = "NOTA PARA SOL"
METADATA = {
    "accelerator": "GPU",
    "colab": {"provenance": [], "toc_visible": True, "gpuType": "T4"},
    "kernelspec": {"display_name": "Python 3", "name": "python3"},
    "language_info": {"name": "python"},
}

ARCHIVO = re.compile(r"^s(\d\d)_([a-z0-9_]+)\.py$")
ARCHIVO_MD = re.compile(r"^s(\d\d)_([a-z0-9_]+)\.texto\.md$")
MARCADOR = re.compile(r"^# %% \[(codigo|texto|plegada)\] ([a-z0-9-]+)\s*$")
SECCION = re.compile(r"^### celda: ([a-z0-9-]+)\s*$")
IMAGEN = re.compile(r"!\[([^\]]*)\]\(ilustracion:([A-Za-z0-9_-]+)\)")
# Claves de metadata que delatan la cuenta de Colab (se borran al integrar).
CUENTA = {"outputid", "authorship_tag", "executioninfo"}

# Preámbulo del script plano: lo que Colab da gratis y python no.
PREAMBULO = '''\
# Generado por tools/gen_cuaderno_entender_red.py --script. No editar.
import sys as _sys
try:
    from IPython.display import display
except ImportError:                       # python sin IPython
    display = print


def _fin_de_celda():
    """Como el backend inline: cada celda cierra sus figuras."""
    if "matplotlib.pyplot" in _sys.modules:
        _sys.modules["matplotlib.pyplot"].close("all")

'''


def falla(mensaje):
    raise SystemExit(f"gen_cuaderno_entender_red: {mensaje}")


# --- Lectura de las fuentes --------------------------------------------------

def leer_celdas(texto, nombre):
    """Las celdas de un `.py` percent: [(tipo, clave, cuerpo)], en orden."""
    celdas, actual = [], None
    for n, linea in enumerate(texto.split("\n"), 1):
        m = MARCADOR.match(linea)
        if m:
            actual = [m.group(1), m.group(2), []]
            celdas.append(actual)
        elif linea.startswith("# %%"):
            falla(f"{nombre}:{n}: marcador mal formado {linea!r} (se espera "
                  "«# %% [codigo|texto|plegada] sNN-<clave>»)")
        elif actual is None:
            if linea.strip() and not linea.lstrip().startswith("#"):
                falla(f"{nombre}:{n}: código antes del primer marcador «# %%»")
        else:
            actual[2].append(linea)
    salida = []
    for tipo, clave, lineas in celdas:
        cuerpo = "\n".join(lineas).strip("\n")
        if tipo != "codigo" and cuerpo.strip():
            falla(f"{nombre}: la celda [{tipo}] {clave} lleva cuerpo; su "
                  "texto va en el .texto.md")
        salida.append((tipo, clave, cuerpo))
    return salida


def leer_guion(texto, nombre):
    """Las secciones del guion: [(clave, markdown)], en orden."""
    secciones, actual, preambulo = [], None, []
    for linea in texto.split("\n"):
        m = SECCION.match(linea)
        if m:
            actual = [m.group(1), []]
            secciones.append(actual)
        elif linea.startswith("### celda:"):
            falla(f"{nombre}: encabezado mal formado {linea!r}")
        elif actual is None:
            preambulo.append(linea)
        else:
            actual[1].append(linea)
    resto = re.sub(r"<!--.*?-->", "", "\n".join(preambulo), flags=re.S)
    if resto.strip():
        falla(f"{nombre}: texto antes del primer «### celda:»")
    return [(c, "\n".join(ls).strip("\n")) for c, ls in secciones]


def pares(fuentes=None):
    """{NN: (ruta .py, ruta .texto.md o None)} de las fuentes, por número."""
    base = Path(fuentes or FUENTES)
    if not base.is_dir():
        falla(f"no existe el directorio de fuentes {base}")
    pys, mds = {}, {}
    for ruta in sorted(base.iterdir()):
        m, mm = ARCHIVO.match(ruta.name), ARCHIVO_MD.match(ruta.name)
        if m:
            nn = int(m.group(1))
            if nn in pys:
                falla(f"dos fuentes para la sección {nn:02d}: "
                      f"{pys[nn].name} y {ruta.name}")
            pys[nn] = ruta
        elif mm:
            nn = int(mm.group(1))
            if nn in mds:
                falla(f"dos guiones para la sección {nn:02d}: "
                      f"{mds[nn].name} y {ruta.name}")
            mds[nn] = ruta
    for nn, md in mds.items():
        if nn not in pys:
            falla(f"{md.name}: guion sobrante, no hay s{nn:02d}_*.py")
        if md.name[:-len(".texto.md")] != pys[nn].stem:
            falla(f"{md.name} no se llama como {pys[nn].name} (.texto.md)")
    return {nn: (pys[nn], mds.get(nn)) for nn in sorted(pys)}


def celdas_de_seccion(nn, py, md, vistas):
    """[(tipo, clave, contenido)] de una sección, con claves validadas.

    `vistas` acumula {clave: archivo} para detectar duplicadas entre
    secciones. El contenido de [texto]/[plegada] es el markdown del guion.
    """
    celdas = leer_celdas(py.read_text(encoding="utf-8"), py.name)
    prefijo = f"s{nn:02d}-"
    for _, clave, _ in celdas:
        if not clave.startswith(prefijo):
            falla(f"{py.name}: la clave {clave!r} no empieza con {prefijo!r}")
        if clave in vistas:
            falla(f"clave duplicada {clave!r}: en {vistas[clave]} y {py.name}")
        vistas[clave] = py.name
    guion = []
    if md is not None:
        guion = leer_guion(md.read_text(encoding="utf-8"), md.name)
    textos, nombre_md = {}, md.name if md else f"{py.stem}.texto.md"
    for clave, texto in guion:
        if clave in textos:
            falla(f"{nombre_md}: clave duplicada {clave!r}")
        textos[clave] = texto
    de_texto = {c for t, c, _ in celdas if t != "codigo"}
    for clave in [c for t, c, _ in celdas if t != "codigo"]:
        if clave not in textos:
            falla(f"{nombre_md}: falta «### celda: {clave}» (la pide {py.name})")
    for clave in textos:
        if clave not in de_texto:
            falla(f"{nombre_md}: clave sobrante {clave!r}: {py.name} no tiene "
                  "una celda [texto] o [plegada] con ella")
    return [(t, c, cuerpo if t == "codigo" else textos[c])
            for t, c, cuerpo in celdas]


# --- Markdown: notas, ilustraciones, plegadas ---------------------------------

def ilustraciones(md, clave, fuentes, borrador):
    """Sustituye cada `ilustracion:<nombre>` por su PNG como data URI."""
    lineas = md.split("\n")
    for i, linea in enumerate(lineas):
        for m in IMAGEN.finditer(linea):
            siguiente = next((l for l in lineas[i + 1:] if l.strip()), None)
            if siguiente is None or siguiente.strip() != AVISO:
                falla(f"{clave}: la ilustración {m.group(2)!r} no va seguida "
                      f"de la línea {AVISO!r}")

    def sustituir(m):
        alt, nombre = m.group(1), m.group(2)
        png = Path(fuentes or FUENTES) / "ilustraciones" / f"{nombre}.png"
        if not png.exists():
            if borrador:
                return f"*[ilustración pendiente: {nombre}]*"
            falla(f"{clave}: falta la ilustración {png}")
        datos = base64.b64encode(png.read_bytes()).decode("ascii")
        return f"![{alt}](data:image/png;base64,{datos})"

    return IMAGEN.sub(sustituir, md)


def markdown(tipo, clave, md, fuentes, borrador):
    if NOTA in md and not borrador:
        falla(f"{clave}: queda «{NOTA}» (usa --borrador mientras sol no "
              "redacta)")
    md = ilustraciones(md, clave, fuentes, borrador)
    if tipo == "plegada":
        md = f"<details><summary>Respuesta</summary>\n\n{md}\n\n</details>"
    return md


# --- Armar ---------------------------------------------------------------------

def celdas(fuentes=None, secciones=None, borrador=False, portada=True):
    """[(tipo, clave, fuente)] ya listas; tipo ∈ {"code", "markdown"}."""
    todas, vistas, salida = pares(fuentes), {}, []
    if secciones is not None:
        faltan = sorted(set(secciones) - set(todas))
        if faltan:
            falla("no hay fuentes para las secciones "
                  + ", ".join(f"{n:02d}" for n in faltan))
    for nn, (py, md) in todas.items():
        quiere = secciones is None or nn in secciones or (nn == 0 and portada)
        if nn == 0 and not portada:
            quiere = False
        if not quiere:
            continue
        for tipo, clave, cont in celdas_de_seccion(nn, py, md, vistas):
            if tipo == "codigo":
                salida.append(("code", clave, cont))
            else:
                salida.append(("markdown", clave,
                               markdown(tipo, clave, cont, fuentes, borrador)))
    return salida


def _lineas(texto):
    partes = texto.split("\n")
    return [p + "\n" for p in partes[:-1]] + [partes[-1]]


def _celda(tipo, clave, texto):
    c = {"cell_type": tipo, "metadata": {"id": clave}, "source": _lineas(texto)}
    if tipo == "code":
        c.update(execution_count=None, outputs=[])
    return c


def cuaderno(fuentes=None, secciones=None, borrador=False):
    """El notebook como dict nbformat 4, sin salidas."""
    lista = celdas(fuentes, secciones, borrador, portada=True)
    if not lista:
        falla("no hay celdas: ninguna fuente sNN_*.py")
    if lista[0][0] == "markdown":
        tipo, clave, texto = lista[0]
        lista[0] = (tipo, clave, BADGE + "\n\n" + texto)
    else:
        lista.insert(0, ("markdown", "badge", BADGE))
    return {"cells": [_celda(*c) for c in lista],
            "metadata": copy.deepcopy(METADATA),
            "nbformat": 4, "nbformat_minor": 0}


def script(fuentes=None, secciones=None, borrador=False):
    """Todo el código (sin la portada) concatenado como un .py plano."""
    partes = [PREAMBULO]
    for tipo, clave, texto in celdas(fuentes, secciones, borrador,
                                     portada=False):
        if tipo == "code":
            partes.append(f"# ==== {clave} ====\n{texto}\n_fin_de_celda()\n\n")
    return "".join(partes)


def serializar(nb):
    return json.dumps(nb, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# --- Integrar la corrida de Colab -----------------------------------------------

def fuente(celda):
    s = celda.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def _normal(texto):
    return "\n".join(l.rstrip() for l in texto.split("\n")).strip("\n")


def limpiar(obj):
    """Copia sin las claves de cuenta: outputId, authorship_tag, executionInfo,
    y toda clave que mencione email o user."""
    if isinstance(obj, dict):
        return {k: limpiar(v) for k, v in obj.items()
                if k.lower() not in CUENTA
                and "email" not in k.lower() and "user" not in k.lower()}
    if isinstance(obj, list):
        return [limpiar(v) for v in obj]
    return obj


def integrar(generado, descarga):
    """El notebook generado con las salidas de código de `descarga`."""
    a, b = generado["cells"], descarga.get("cells", [])
    if len(a) != len(b):
        falla(f"la descarga tiene {len(b)} celdas y el generador {len(a)}: "
              "reejecuta en Colab el notebook generado hoy")
    nb = copy.deepcopy(generado)
    for i, (g, d) in enumerate(zip(nb["cells"], b)):
        clave = g["metadata"]["id"]
        if g["cell_type"] != d.get("cell_type"):
            falla(f"celda {i} ({clave}): tipo {d.get('cell_type')!r} en la "
                  f"descarga, {g['cell_type']!r} en el generador")
        if g["cell_type"] != "code":
            continue                      # el markdown puede cambiar: gana el nuestro
        if _normal(fuente(g)) != _normal(fuente(d)):
            falla(f"celda {i} ({clave}): el código difiere del generador; un "
                  "cambio de código obliga a reejecutar en Colab")
        g["outputs"] = limpiar(d.get("outputs", []))
        g["execution_count"] = d.get("execution_count")
    return nb


# --- CLI -------------------------------------------------------------------------

def _secciones(valor):
    try:
        return {int(p) for p in valor.split(",") if p.strip()}
    except ValueError:
        raise argparse.ArgumentTypeError(f"--secciones: {valor!r} no es una "
                                         "lista de números (p. ej. 1,2,3,7)")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--script", metavar="RUTA",
                   help="escribe el código concatenado como .py plano")
    p.add_argument("--integrar", metavar="DESCARGA",
                   help="integra un .ipynb ejecutado en Colab")
    p.add_argument("--borrador", action="store_true",
                   help="admite NOTA PARA SOL e ilustraciones faltantes")
    p.add_argument("--secciones", type=_secciones,
                   help="solo estas secciones, p. ej. 1,2,3,7")
    p.add_argument("--fuentes", help="directorio de fuentes (pruebas)")
    p.add_argument("--salida", help=f"ruta del notebook (por omisión {RUTA_NB})")
    a = p.parse_args(argv)
    if a.script and a.integrar:
        p.error("--script e --integrar son excluyentes")

    if a.script:
        ruta = Path(a.script)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(script(a.fuentes, a.secciones, a.borrador),
                        encoding="utf-8")
        print(f"escrito {ruta}")
        return 0
    nb = cuaderno(a.fuentes, a.secciones, a.borrador)
    if a.integrar:
        if a.borrador or a.secciones:
            p.error("--integrar va sin --borrador ni --secciones")
        descarga = json.loads(Path(a.integrar).read_text(encoding="utf-8"))
        nb = integrar(nb, descarga)
    ruta = Path(a.salida) if a.salida else DESTINO
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(serializar(nb), encoding="utf-8")
    print(f"escrito {ruta} ({len(nb['cells'])} celdas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
