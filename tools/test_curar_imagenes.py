import csv
from pathlib import Path

from PIL import Image

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
