import csv
from pathlib import Path

from PIL import Image

CELDA_NOMBRE = 0
CELDA_ORIGEN = 2
CELDA_LICENCIA = 3

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
INVENTARIO = RAIZ / "tools/imagenes_heredadas.tsv"
ANCHO_MAX = 1400


def filas():
    with INVENTARIO.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_inventario_bien_formado():
    for fila in filas():
        assert fila["decision"] in {"conservar", "descartar"}
        if fila["decision"] == "conservar":
            assert fila["destino"].startswith("legacy-")
            assert fila["descripcion"].strip()


def test_conservadas_existen_y_estan_recomprimidas():
    for fila in filas():
        if fila["decision"] != "conservar":
            continue
        destino = ASSETS / fila["destino"]
        assert destino.is_file(), f"falta {destino.name}"
        with Image.open(destino) as im:
            assert im.width <= ANCHO_MAX, f"{destino.name} mide {im.width}px"


def test_peso_total_razonable():
    total = sum(p.stat().st_size for p in ASSETS.glob("legacy-*"))
    assert total < 6_000_000, f"las imagenes heredadas pesan {total/1e6:.1f} MB"


def filas_de_creditos():
    """Parsea las filas de datos de la tabla de CREDITOS.md: {archivo: [celdas]}."""
    lineas = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8").splitlines()
    filas = {}
    for linea in lineas:
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) < 4:
            continue
        if set(celdas[0]) <= {"-", " "}:  # fila separadora |---|---|---|---|
            continue
        nombre = celdas[CELDA_NOMBRE].strip("`")
        if nombre == "Archivo":  # fila de encabezado
            continue
        filas[nombre] = celdas
    return filas


def test_toda_imagen_tiene_fila_en_creditos():
    filas = filas_de_creditos()
    extensiones = {".png", ".jpg", ".jpeg", ".svg", ".gif"}
    imagenes = sorted(p.name for p in ASSETS.iterdir() if p.suffix.lower() in extensiones)
    sin_fila = [n for n in imagenes if n not in filas]
    assert not sin_fila, f"imagenes sin fila en CREDITOS.md: {sin_fila}"
    incompletas = [
        n for n in imagenes
        if not filas[n][CELDA_ORIGEN] or not filas[n][CELDA_LICENCIA]
    ]
    assert not incompletas, f"filas con origen o licencia vacios: {incompletas}"
