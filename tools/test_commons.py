import csv
from pathlib import Path

from PIL import Image

from unidades import ASSETS_POR_UNIDAD, CELDA_LICENCIA, filas_de_creditos

RAIZ = Path(__file__).resolve().parent.parent
LISTA = RAIZ / "tools/commons.tsv"

LICENCIAS_OK = ("public domain", "cc0", "cc by", "cc-by", "pd-")


def filas():
    with LISTA.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _assets(fila):
    return ASSETS_POR_UNIDAD[fila["unidad"]]


def test_cada_foto_se_descargo():
    for fila in filas():
        assert (_assets(fila) / fila["destino"]).is_file(), f"falta {fila['destino']}"


def test_fotos_recomprimidas():
    for fila in filas():
        with Image.open(_assets(fila) / fila["destino"]) as im:
            assert im.width <= 1400, f"{fila['destino']} mide {im.width}px"


def test_cada_foto_tiene_credito_con_licencia_aceptable():
    for fila in filas():
        filas_creditos = filas_de_creditos(_assets(fila))
        destino = fila["destino"]
        assert destino in filas_creditos, f"{destino} sin fila en CREDITOS.md"
        licencia = filas_creditos[destino][CELDA_LICENCIA].lower()
        assert licencia, f"{destino}: celda de licencia vacia"
        assert any(l in licencia for l in LICENCIAS_OK), (
            f"{destino}: licencia no reconocible: {licencia!r}"
        )
