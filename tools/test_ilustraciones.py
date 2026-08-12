import json
from pathlib import Path

from PIL import Image

from unidades import ASSETS_FILOSOFIA, ASSETS_HISTORIA

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = ASSETS_HISTORIA          # el conjunto original no cambia de sitio
CATALOGO = RAIZ / "tools/ilustraciones.json"
CREDITOS = ASSETS / "CREDITOS.md"
CREDITOS_FILOSOFIA = ASSETS_FILOSOFIA / "CREDITOS.md"

# Un PNG con fondo horneado pesa mas que un JPEG al 85: el tope no puede ser
# el mismo. Medidos tras cuantizar a 128 colores: 165, 315, 229 y 172 KB. El
# tope queda en 400 KB, un escalon arriba del mayor, para que un PNG que se
# dispare al doble se detecte, sin fallar por la variacion normal entre
# generaciones.
PESO_MAX_PNG = 400_000

# tokens.color.surface del skin: el color exacto de la columna de contenido
# de la pagina, medido en pixeles sobre una captura del sitio construido
# (no deducido del CSS). Las cuatro ilustraciones de filosofia hornean su
# fondo a este color en vez de dejarlo transparente.
FONDO_OBJETIVO = (33, 16, 51)

# "nick land" y no "land": "land" sola pega en palabras inocentes (landscape)
# y volveria la guarda inutilizable a fuerza de falsos positivos.
PROHIBIDOS = [
    "turing", "lovelace", "hinton", "astroboy", "atomu", "minsky", "shannon",
    "marx", "deleuze", "guattari", "nick land", "fisher", "barbrook", "cameron",
]


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


def nombres_filosofia():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    return list(catalogo["ilustraciones_filosofia"])


def test_filosofia_fondo_horneado_al_color_exacto():
    """El fondo no es transparente: es el mismo violeta solido de la columna
    de contenido de la pagina (#211033), horneado en el PNG. Si el modelo
    devuelve un fondo que no se pudo hornear al color exacto -- porque salio
    con gradiente, vineta o textura -- las esquinas no dan (33, 16, 51) y esta
    prueba lo agarra aqui, no en el navegador. Es una prueba mas estricta que
    "hay canal alfa": tambien detecta un horneado al color equivocado."""
    for nombre in nombres_filosofia():
        ruta = ASSETS_FILOSOFIA / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"
        with Image.open(ruta) as im:
            im = im.convert("RGB")
            esquinas = [
                im.getpixel((0, 0)),
                im.getpixel((im.width - 1, 0)),
                im.getpixel((0, im.height - 1)),
                im.getpixel((im.width - 1, im.height - 1)),
            ]
            assert all(p == FONDO_OBJETIVO for p in esquinas), (
                f"{ruta.name}: las esquinas no son {FONDO_OBJETIVO} exacto ({esquinas})"
            )


def test_filosofia_dimensiones_y_peso():
    for nombre in nombres_filosofia():
        ruta = ASSETS_FILOSOFIA / f"ilus-{nombre}.png"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < PESO_MAX_PNG, (
            f"{ruta.name} pesa {ruta.stat().st_size/1000:.0f} KB"
        )


def test_filosofia_acreditadas_como_generadas():
    creditos = CREDITOS_FILOSOFIA.read_text(encoding="utf-8").lower()
    for nombre in nombres_filosofia():
        assert f"ilus-{nombre}.png" in creditos, f"ilus-{nombre}.png sin credito"
    assert "generada" in creditos
