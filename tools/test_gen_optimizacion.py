"""Guardas de los diagramas de la unidad de modelado y optimizacion.

Mismo juego que test_gen_complejidad.py, con dos anadidos propios de esta
unidad: <title> y <desc> internos, que ningun SVG del curso llevaba, y la
comprobacion de que los dos diagramas que CALCULAN siguen coincidiendo con la
aritmetica exacta del episodio.

Ojo con lo que estas pruebas NO hacen: el fixture regenera antes de leer, asi
que un SVG editado a mano se sobrescribe en silencio y la suite pasa. Lo que
ata el archivo comiteado a su generador es correr el generador y comprobar que
`git status` queda limpio.
"""
import re
import xml.etree.ElementTree as ET

import pytest

import gen_optimizacion as gen
from unidades import ASSETS_OPTIMIZACION, filas_de_creditos

FONDO = "#211033"


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    for nombre in gen.DIAGRAMAS:
        gen.escribir(nombre)


def _texto(nombre):
    return (ASSETS_OPTIMIZACION / f"{nombre}.svg").read_text(encoding="utf-8")


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_existe_y_lleva_el_prefijo(nombre):
    assert nombre.startswith("opt-"), (
        f"{nombre}: los ids de objeto numerado son unicos en TODO el curso, "
        "asi que esta unidad prefija con 'opt-'"
    )
    assert (ASSETS_OPTIMIZACION / f"{nombre}.svg").is_file()


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_la_raiz_svg_trae_las_cinco_convenciones(nombre):
    texto = _texto(nombre)
    raiz = re.match(r"<svg\b[^>]*>", texto)
    assert raiz, f"{nombre}: no empieza con la etiqueta <svg>"
    etiqueta = raiz.group()
    for atributo in ('viewBox="', 'role="img"', "aria-label="):
        assert atributo in etiqueta, f"{nombre}: <svg> sin {atributo}"
    assert re.search(r'\bwidth="\d', etiqueta), (
        f"{nombre}: <svg> sin width propio; el sitio lo incrusta con <img> y "
        "sin tamano intrinseco cae a ~300x150 px"
    )
    assert re.search(r'\bheight="\d', etiqueta), f"{nombre}: <svg> sin height propio"
    assert f'fill="{FONDO}"' in texto, f"{nombre}: sin el fondo del skin ({FONDO})"


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_trae_title_y_desc(nombre):
    """Convencion NUEVA de esta unidad: ningun SVG del curso los traia.

    aria-label lo lee un lector de pantalla, pero <title> es lo que muestran
    los visores de SVG y lo que aparece al abrir el archivo suelto.
    """
    texto = _texto(nombre)
    for etiqueta in ("<title>", "<desc>"):
        assert etiqueta in texto, f"{nombre}: sin {etiqueta}"
    titulo = re.search(r"<title>(.*?)</title>", texto).group(1)
    desc = re.search(r"<desc>(.*?)</desc>", texto).group(1)
    assert len(titulo) >= 8, f"{nombre}: <title> demasiado corto"
    assert len(desc) >= 40, f"{nombre}: <desc> no describe lo que se ve"


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ningun_diagrama_usa_fill_opacity(nombre):
    """Se publico una vez un sombreado opaco que tapaba dos curvas.

    mezclar() devuelve el color ya fundido contra el fondo, que se ve igual en
    los renderizadores que ignoran la opacidad.
    """
    assert "fill-opacity" not in _texto(nombre)
    assert "stroke-opacity" not in _texto(nombre)


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_parsea_como_xml(nombre):
    ET.fromstring(_texto(nombre))


def test_no_queda_ningun_svg_huerfano():
    en_disco = {p.stem for p in ASSETS_OPTIMIZACION.glob("*.svg")}
    assert en_disco == set(gen.DIAGRAMAS), (
        "sobran o faltan SVG frente al catalogo: "
        f"{en_disco ^ set(gen.DIAGRAMAS)}"
    )


def test_ningun_svg_sin_pagina_que_lo_use():
    """El mapa de huerfanos compara disco contra catalogo, y eso deja pasar un
    diagrama generado, acreditado, y que ninguna pagina enlaza. Historia y
    agentes tienen esta guarda; optimizacion no la tenia.

    Recorre con rglob porque las paginas de la unidad estan anidadas por clase,
    y salta los directorios de soporte: _assets/CREDITOS.md nombra TODOS los
    SVG, asi que incluirlo dejaria pasar justo el caso que esta guarda busca
    —acreditado y sin enlazar—."""
    unidad = ASSETS_OPTIMIZACION.parent
    renderizadas = sorted(
        p for p in unidad.rglob("*.md")
        if not any(parte.startswith("_") for parte in p.relative_to(unidad).parts)
    )
    paginas = "\n".join(p.read_text(encoding="utf-8") for p in renderizadas)
    sin_usar = sorted(
        svg.name for svg in ASSETS_OPTIMIZACION.glob("*.svg")
        if svg.name not in paginas
    )
    assert not sin_usar, f"SVG que ninguna pagina enlaza: {sin_usar}"


def test_cada_svg_tiene_fila_en_creditos():
    filas = filas_de_creditos(ASSETS_OPTIMIZACION)
    for nombre in gen.DIAGRAMAS:
        assert f"{nombre}.svg" in filas, f"{nombre}.svg sin fila en CREDITOS.md"


def test_los_dos_que_calculan_usan_la_geometria_exacta():
    """opt-poligono y opt-curvas-de-nivel no llevan coordenadas a mano.

    Si un parametro del fabricador cambia, el dibujo tiene que cambiar solo.
    Esta prueba fija las cinco esquinas que la aritmetica exacta produce hoy y
    comprueba que los rotulos del SVG las nombran.
    """
    V = gen.vertices()
    assert sorted((int(x), int(y)) for x, y in V) == [
        (0, 0), (0, 9), (2, 8), (8, 2), (9, 0)
    ], f"las esquinas del episodio cambiaron: {V}"
    mejor = max(V, key=gen.valor)
    assert (int(mejor[0]), int(mejor[1])) == (8, 2)
    assert int(gen.valor(mejor)) == 38
    texto = _texto("opt-poligono")
    for x, y in V:
        assert gen.rotulo((x, y)) in texto, (
            f"opt-poligono no rotula la esquina {gen.rotulo((x, y))}"
        )


def test_el_rotulo_de_cada_esquina_esta_declarado():
    """ROTULOS se ajusto a mano mirando el render; si nace una esquina nueva,
    su desplazamiento no existe y el generador reventaria al dibujarla."""
    claves = {(int(x), int(y)) for x, y in gen.vertices()}
    assert claves <= set(gen.ROTULOS), f"esquinas sin desplazamiento: {claves - set(gen.ROTULOS)}"
