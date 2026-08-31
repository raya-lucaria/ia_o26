"""Guardas del generador de diagramas de la unidad de complejidad.

Copia deliberada de test_gen_computabilidad.py: regenera antes de comparar, para
que correr pytest certifique que lo comiteado coincide con lo que el generador
produce hoy, y no solo que el archivo existe. Editar un SVG a mano falla aqui.

Las convenciones de la raiz <svg> no son cosmeticas: test_9 de test_aceptacion.py
las exige para toda unidad con imagenes propias, y sin width/height propios el
sitio incrusta el diagrama a ~300x150 CSS px.
"""
import importlib.util
import re
import subprocess
import sys
import xml.dom.minidom
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/4_complejidad/_assets"


def _cargar():
    spec = importlib.util.spec_from_file_location(
        "gen_complejidad", RAIZ / "tools/gen_complejidad.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    subprocess.run([sys.executable, str(RAIZ / "tools/gen_complejidad.py")], check=True)


def test_todos_los_diagramas_declarados_existen():
    modulo = _cargar()
    assert modulo.DIAGRAMAS, "el catalogo DIAGRAMAS esta vacio"
    for nombre in modulo.DIAGRAMAS:
        assert nombre.startswith("cx-"), (
            f"{nombre}: los ids de objeto numerado son unicos en TODO el curso, "
            "no por pagina; sin el prefijo 'cx-' pueden chocar con los 'comp-' "
            "de computabilidad, que cubren varios de los mismos temas"
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


def test_cada_svg_es_xml_bien_formado():
    modulo = _cargar()
    for nombre in modulo.DIAGRAMAS:
        ruta = ASSETS / f"{nombre}.svg"
        try:
            xml.dom.minidom.parse(str(ruta))
        except Exception as error:  # noqa: BLE001 - se re-lanza como fallo legible
            raise AssertionError(f"{ruta.name} no es XML bien formado: {error}") from error


def test_ningun_svg_quedo_huerfano_en_assets():
    modulo = _cargar()
    declarados = {f"{n}.svg" for n in modulo.DIAGRAMAS}
    presentes = {p.name for p in ASSETS.glob("cx-*.svg")}
    huerfanos = sorted(presentes - declarados)
    assert not huerfanos, (
        f"SVG en _assets que el generador ya no produce: {huerfanos}. "
        "Borralos, o devuelveles su entrada en DIAGRAMAS."
    )


def test_cada_svg_tiene_fila_en_creditos():
    modulo = _cargar()
    creditos = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8")
    for nombre in modulo.DIAGRAMAS:
        assert f"`{nombre}.svg`" in creditos, (
            f"{nombre}.svg no tiene fila en CREDITOS.md; agregar una fila con "
            "origen y licencia no vacios al agregar el diagrama"
        )


def test_ningun_diagrama_usa_opacidad_para_informacion():
    """El sombreado de cx-o-grande se pinto una vez con fill-opacity y tapo las
    dos curvas al renderizarse fuera del navegador (ImageMagick ignora la
    opacidad). Se arreglo mezclando el color contra el fondo con mezclar(); esta
    guarda impide que la solucion se pierda al agregar un diagrama nuevo.

    Las barras de las tablas si pueden llevar opacity: se leen igual opacas.
    """
    modulo = _cargar()
    for nombre in modulo.DIAGRAMAS:
        texto = (ASSETS / f"{nombre}.svg").read_text(encoding="utf-8")
        assert "fill-opacity" not in texto, (
            f"{nombre}.svg usa fill-opacity: usa mezclar(color, fraccion) para "
            "obtener el color ya mezclado contra el fondo"
        )


def test_las_cadenas_de_miller_rabin_son_las_de_verdad():
    """El diagrama calcula sus propios numeros con pow(); esta guarda comprueba
    que el ejemplo elegido sigue diciendo lo que la pagina afirma que dice: que
    561 engaña a Fermat (su cadena termina en 1) y que Miller-Rabin lo caza
    igual (llega al 1 desde algo que no es ni 1 ni -1)."""
    modulo = _cargar()
    s, d, cadena = modulo._cadena_mr(561, 2)
    assert (s, d) == (4, 35), f"561 - 1 no se descompuso como 2^4 * 35: {(s, d)}"
    assert cadena[-1] == 1, "561 dejaria de engañar al test de Fermat"
    i = cadena.index(1)
    assert cadena[i - 1] not in (1, 560), (
        "561 ya no llega al 1 desde una raiz no trivial: el ejemplo dejo de "
        "demostrar lo que la pagina dice"
    )

    s, d, cadena = modulo._cadena_mr(97, 2)
    assert 96 in cadena, "la cadena de 97 ya no toca -1, que es lo que la figura enseña"
