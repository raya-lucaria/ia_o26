import csv
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
LISTA = RAIZ / "tools/commons.tsv"
CREDITOS = ASSETS / "CREDITOS.md"

LICENCIAS_OK = ("public domain", "cc0", "cc by", "cc-by", "pd-")


def filas():
    with LISTA.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_cada_foto_se_descargo():
    for fila in filas():
        assert (ASSETS / fila["destino"]).is_file(), f"falta {fila['destino']}"


def test_fotos_recomprimidas():
    for fila in filas():
        with Image.open(ASSETS / fila["destino"]) as im:
            assert im.width <= 1400, f"{fila['destino']} mide {im.width}px"


def test_cada_foto_tiene_credito_con_licencia_aceptable():
    creditos = CREDITOS.read_text(encoding="utf-8").lower()
    for fila in filas():
        assert fila["destino"].lower() in creditos, f"{fila['destino']} sin credito"
    assert any(l in creditos for l in LICENCIAS_OK), "ninguna licencia reconocible"
