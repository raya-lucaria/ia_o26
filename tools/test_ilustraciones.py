import json
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
CATALOGO = RAIZ / "tools/ilustraciones.json"
CREDITOS = ASSETS / "CREDITOS.md"

PROHIBIDOS = ["turing", "lovelace", "hinton", "astroboy", "atomu", "minsky", "shannon"]


def nombres():
    return list(json.loads(CATALOGO.read_text(encoding="utf-8"))["ilustraciones"])


def test_todas_generadas():
    for nombre in nombres():
        assert (ASSETS / f"ilus-{nombre}.jpg").is_file(), f"falta ilus-{nombre}.jpg"


def test_dimensiones_y_peso():
    for nombre in nombres():
        ruta = ASSETS / f"ilus-{nombre}.jpg"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < 400_000, f"{ruta.name} pesa demasiado"


def test_ningun_prompt_pide_persona_real_o_personaje_protegido():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    texto = json.dumps(catalogo, ensure_ascii=False).lower()
    for termino in PROHIBIDOS:
        assert termino not in texto, f"el catalogo menciona '{termino}'"


def test_creditos_marcan_las_generadas():
    creditos = CREDITOS.read_text(encoding="utf-8").lower()
    for nombre in nombres():
        assert f"ilus-{nombre}.jpg" in creditos, f"ilus-{nombre}.jpg sin credito"
    assert "generada" in creditos


def test_no_queda_png_de_ilustracion_huerfano():
    huerfanos = sorted(p.name for p in ASSETS.glob("ilus-*.png"))
    assert not huerfanos, f"PNGs de ilustracion sin reemplazar por jpg: {huerfanos}"
