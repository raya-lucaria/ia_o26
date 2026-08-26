"""Guardas del generador de diagramas de la unidad de computabilidad.

Regenera antes de comparar (igual que test_gen_computo.py) para que correr
pytest certifique que lo comiteado coincide con lo que el generador produce
hoy, y no solo que el archivo existe. Editar un SVG a mano falla aqui.

Las convenciones de la raiz <svg> no son cosmeticas: test_9 de
test_aceptacion.py las exige para toda unidad con imagenes propias, y sin
width/height propios el sitio incrusta el diagrama a ~300x150 CSS px.
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/3_computabilidad/_assets"


def _cargar():
    spec = importlib.util.spec_from_file_location(
        "gen_computabilidad", RAIZ / "tools/gen_computabilidad.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    subprocess.run(
        [sys.executable, str(RAIZ / "tools/gen_computabilidad.py")], check=True
    )


def test_todos_los_diagramas_declarados_existen():
    modulo = _cargar()
    assert modulo.DIAGRAMAS, "el catalogo DIAGRAMAS esta vacio"
    for nombre in modulo.DIAGRAMAS:
        assert nombre.startswith("comp-"), (
            f"{nombre}: los ids de objeto numerado son unicos en TODO el curso, "
            "no por pagina; sin el prefijo 'comp-' pueden chocar "
            "(p. ej. 'computo' ya lo ocupa una figura de historia)"
        )
        assert (ASSETS / f"{nombre}.svg").is_file(), f"falta {nombre}.svg"


def test_cada_svg_cumple_las_cinco_convenciones_de_la_raiz():
    modulo = _cargar()
    for nombre in modulo.DIAGRAMAS:
        ruta = ASSETS / f"{nombre}.svg"
        texto = ruta.read_text(encoding="utf-8")
        raiz = re.match(r"<svg\b[^>]*>", texto)
        assert raiz, f"{ruta.name}: no se encontro la etiqueta <svg>"
        etiqueta = raiz.group()
        assert re.search(r'\bwidth="\d', etiqueta), (
            f"{ruta.name}: <svg> sin width propio -> se renderiza minusculo en el sitio"
        )
        assert re.search(r'\bheight="\d', etiqueta), (
            f"{ruta.name}: <svg> sin height propio -> se renderiza minusculo en el sitio"
        )
        assert 'viewBox="' in etiqueta, f"{ruta.name} sin viewBox"
        assert 'role="img"' in etiqueta, f"{ruta.name} sin role=img"
        assert "aria-label=" in etiqueta, f"{ruta.name} sin aria-label"
        assert f'fill="{modulo.FONDO}"' in texto, (
            f"{ruta.name} sin el fondo {modulo.FONDO} del skin"
        )


def test_ningun_svg_quedo_huerfano_en_assets():
    """Un SVG que el generador ya no produce se queda en el directorio y sigue
    pesando contra TOPE_REPOSITORIO sin que nada lo note. Falla para que se
    borre a mano, que es la decision correcta."""
    modulo = _cargar()
    declarados = {f"{n}.svg" for n in modulo.DIAGRAMAS}
    presentes = {p.name for p in ASSETS.glob("comp-*.svg")}
    huerfanos = sorted(presentes - declarados)
    assert not huerfanos, (
        f"SVG en _assets que el generador ya no produce: {huerfanos}. "
        "Borralos, o devuelveles su entrada en DIAGRAMAS."
    )


def test_cada_svg_tiene_fila_en_creditos():
    """Duplica a proposito lo que test_curar_imagenes ya comprueba para todas
    las unidades: aqui el mensaje nombra al generador, que es donde esta el
    arreglo cuando el que falta es un diagrama recien agregado."""
    modulo = _cargar()
    creditos = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8")
    for nombre in modulo.DIAGRAMAS:
        assert f"`{nombre}.svg`" in creditos, (
            f"{nombre}.svg no tiene fila en CREDITOS.md; agregar una fila con "
            "origen y licencia no vacios al agregar el diagrama"
        )
