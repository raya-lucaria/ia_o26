"""Las vistas previas de la animación de la unidad 7 (tools/gen_vistas_traza.py).

Las capturas no se regeneran aquí: dependen de Chrome y de las fuentes de la
máquina. Lo que esta prueba ata es que no se desfasen de la animación (la
huella de traza_arbol_t.html en tools/vistas_traza.json), que cada una tenga
su crédito, y que cada página que las usa las enlace a la animación en el
mismo paso que muestran: pulsar la imagen abre lo que se ve en ella.
"""
import json
import re

import pytest
from PIL import Image

import gen_vistas_traza as g
from unidades import ASSETS_JUEGOS

UNIDAD = ASSETS_JUEGOS.parent
HUELLA = json.loads(g.HUELLA.read_text(encoding="utf-8"))
MODOS = ("minimax", "azar", "alfa-beta", "corte", "iterativa")
FONDO_PAGINA = (0x12, 0x06, 0x1F)   # --page de la animación (skin eva-cyberpunk)


def _paginas():
    return {p: p.read_text(encoding="utf-8") for p in UNIDAD.rglob("*.md")
            if not any(parte.startswith("_") for parte in p.relative_to(UNIDAD).parts)}


def test_las_capturas_son_de_la_animacion_de_hoy():
    """Si gen_traza_web.py (o una mano) cambió la animación, las capturas
    enseñan otra cosa: hay que volver a correr gen_vistas_traza.py."""
    assert HUELLA["sha256"] == g.huella_html(), (
        "traza_arbol_t.html cambió desde la última captura: corre "
        "`uv run --python 3.12 --with playwright --with pillow python tools/gen_vistas_traza.py`")
    assert [(v["archivo"], v["fragmento"]) for v in HUELLA["vistas"]] == g.VISTAS


def test_una_vista_por_animacion():
    assert sorted(f.split("-fila-")[0] for _, f in g.VISTAS) == sorted(MODOS)
    en_disco = sorted(p.name for p in ASSETS_JUEGOS.glob("jue-anim-*.png"))
    assert en_disco == sorted(a for a, _ in g.VISTAS)


@pytest.mark.parametrize("archivo,fragmento", g.VISTAS)
def test_la_captura_tiene_la_forma_esperada(archivo, fragmento):
    ruta = ASSETS_JUEGOS / archivo
    img = Image.open(ruta)
    assert img.width == g.ANCHO and 600 <= img.height <= g.ALTO
    assert img.mode == "P", "sin reducir a 256 colores pesa el triple"
    assert ruta.stat().st_size < 150_000
    assert img.convert("RGB").getpixel((2, 2)) == FONDO_PAGINA


@pytest.mark.parametrize("archivo,fragmento", g.VISTAS)
def test_la_captura_tiene_credito(archivo, fragmento):
    creditos = (ASSETS_JUEGOS / "CREDITOS.md").read_text(encoding="utf-8")
    fila = next((l for l in creditos.splitlines() if l.startswith(f"| `{archivo}` |")), None)
    assert fila and "gen_vistas_traza.py" in fila


@pytest.mark.parametrize("archivo,fragmento", g.VISTAS)
def test_cada_captura_abre_la_animacion_en_el_paso_que_muestra(archivo, fragmento):
    """Toda aparición de la imagen va dentro de un enlace a la animación con
    su mismo fragmento, y dentro de una figura (numerada, con título)."""
    usos = 0
    for ruta, texto in _paginas().items():
        for m in re.finditer(rf"\[!\[[^\]]+\]\((?:\.\./)?_assets/{re.escape(archivo)}\)\]"
                             r"\((?:\.\./)?_assets/traza_arbol_t\.html#([\w-]+)\)", texto):
            assert m.group(1) == fragmento, (ruta.name, m.group(1))
            antes = texto[:m.start()].rstrip().splitlines()[-1]
            assert antes.startswith("::: figure {#"), ruta.name
            usos += 1
        sueltas = texto.count(archivo) - len(re.findall(rf"_assets/{re.escape(archivo)}\)\]", texto))
        assert sueltas == 0, f"{ruta.name}: {archivo} sin enlace a la animación"
    assert usos >= 2, f"{archivo}: debe estar en su página y en el anexo"


def test_el_anexo_trae_las_cinco_y_lo_enlazan_los_indices():
    anexo = (UNIDAD / "B_animaciones.md").read_text(encoding="utf-8")
    for archivo, _ in g.VISTAS:
        assert f"_assets/{archivo}" in anexo
    for indice in ("0_index.md", "2_mirar_todo_y_podar/0_index.md", "3_cuando_no_cabe/0_index.md"):
        assert "[[animaciones-juegos|" in (UNIDAD / indice).read_text(encoding="utf-8"), indice
