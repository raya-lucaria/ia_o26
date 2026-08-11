"""Guardas del cuadernillo de lecturas.

Aqui no se construye ningun PDF: WeasyPrint y los PDF con derechos no estan
disponibles en CI. Se prueban funciones puras y archivos versionados.
"""
import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODULO = RAIZ / "lecturas/filosofia_ia/clase_1"
INTRO = MODULO / "introduccion.md"
PAGINA = RAIZ / "course/2_filosofia_ia/1_accelerate_what.md"

MARCADORES = re.compile(
    r"^## Cómo leer este cuadernillo$(.*?)(?=^## El cuadernillo$)",
    re.S | re.M,
)


def _cargar_lecturas():
    """Carga tools/lecturas.py como modulo para probar sus funciones directamente."""
    spec = importlib.util.spec_from_file_location(
        "lecturas", RAIZ / "tools/lecturas.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    # Necesario para que `from __future__ import annotations` en lecturas.py
    # resuelva sus anotaciones de dataclass: dataclasses._is_type busca el
    # modulo en sys.modules por nombre al procesar la clase.
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _normalizar(texto: str) -> str:
    """Colapsa todo espacio en blanco a uno solo.

    Tolera que alguien reacomode los saltos de linea al editar cualquiera de
    los dos archivos, y sigue detectando cualquier cambio de palabra.
    """
    return " ".join(texto.split())


def test_la_introduccion_no_ha_derivado():
    fuente = INTRO.read_text(encoding="utf-8").split("\n", 1)[1]
    m = MARCADORES.search(PAGINA.read_text(encoding="utf-8"))
    assert m, (
        "la pagina del curso debe traer la seccion "
        "'Como leer este cuadernillo' terminada por '## El cuadernillo'"
    )
    assert _normalizar(m.group(1)) == _normalizar(fuente), (
        "la introduccion de la pagina del curso ya no coincide con "
        "lecturas/filosofia_ia/clase_1/introduccion.md"
    )


APARTADOS = (
    "**Qué vas a leer.**",
    "**Palabras clave.**",
    "**Qué retener.**",
    "**Es difícil, y está bien.**",
)


def _todas_las_lecturas(modulo="filosofia_ia/clase_1"):
    m = _cargar_lecturas()
    return list(m.LECTURAS[modulo]) + list(m.PDFS[modulo])


def test_toda_lectura_trae_introduccion():
    for x in _todas_las_lecturas():
        assert not hasattr(x, "por_que"), f"{x.id}: por_que quedo vivo"
        for apartado in APARTADOS:
            assert apartado in x.introduccion, f"{x.id}: le falta {apartado}"


def test_el_orden_es_consecutivo_y_unico():
    ordenes = sorted(x.orden for x in _todas_las_lecturas())
    assert ordenes == [1, 2, 3, 4, 5, 6], (
        f"el orden debe ser 1..6 sin huecos ni repetidos, y es {ordenes}. "
        "El intercalado de los PDF externos depende de ello."
    )


def test_el_orden_es_el_acordado():
    xs = sorted(_todas_las_lecturas(), key=lambda x: x.orden)
    assert [x.id for x in xs] == [
        "marx-fragmento-maquinas",
        "deleuze-guattari-antiedipo",
        "land-meltdown",
        "fisher-terminator-avatar",
        "ccru-swarmachines",
        "barbrook-cameron-californian",
    ]


def test_inline_convierte_negritas_y_cursivas():
    m = _cargar_lecturas()
    assert m._inline("**Qué retener.** el *capital*") == (
        "<strong>Qué retener.</strong> el <em>capital</em>"
    )


def test_inline_escapa_el_html():
    m = _cargar_lecturas()
    assert m._inline("a < b & c") == "a &lt; b &amp; c"


def test_markdown_basico_arma_parrafos_encabezado_y_lista():
    m = _cargar_lecturas()
    html = m._markdown_basico(
        "## Título\n\nUn párrafo.\n\n- **uno** primero\n  y su continuación\n- dos\n"
    )
    assert "<h2>Título</h2>" in html
    assert "<p>Un párrafo.</p>" in html
    assert "<li><strong>uno</strong> primero y su continuación</li>" in html
    assert "<li>dos</li>" in html


def test_markdown_basico_borra_los_wikilinks():
    m = _cargar_lecturas()
    assert "[[" not in m._markdown_basico("ver [[ia-y-sociedad]] y [[x|el mapa]]")
    assert "el mapa" in m._markdown_basico("ver [[x|el mapa]]")
    assert "ia-y-sociedad" in m._markdown_basico("ver [[ia-y-sociedad]]")


def test_la_introduccion_del_modulo_se_lee_del_archivo():
    m = _cargar_lecturas()
    assert m._introduccion("filosofia_ia/clase_1").startswith("## Cómo leer")


def test_se_emite_un_hueco_por_pagina_externa():
    m = _cargar_lecturas()
    fisher = next(x for x in m.PDFS["filosofia_ia/clase_1"]
                  if x.id == "fisher-terminator-avatar")
    html = m._seccion_externa(fisher)
    esperadas = fisher.paginas[1] - fisher.paginas[0] + 1   # 12
    assert len(m.RE_MARCA.findall(html)) == esperadas
    assert "##HUECO:fisher-terminator-avatar:0##" in html
    assert f"##HUECO:fisher-terminator-avatar:{esperadas - 1}##" in html


def test_las_secciones_salen_en_el_orden_acordado():
    m = _cargar_lecturas()
    modulo = "filosofia_ia/clase_1"
    lecturas = m.LECTURAS[modulo]
    textos = {l.id: "palabra " * 120 for l in lecturas}
    doc = m.construir_html(
        modulo, lecturas, textos, [], m.PDFS[modulo], m._introduccion(modulo)
    )
    titulos = ["Fragmento sobre las máquinas", "El Anti-Edipo",
               "Meltdown", "Terminator vs Avatar", "Swarmachines",
               "La ideología californiana"]
    posiciones = [doc.index(f"<h2>{t}") for t in titulos]
    assert posiciones == sorted(posiciones), (
        "las secciones no salen en el orden acordado: " + str(posiciones)
    )


def test_la_introduccion_va_antes_de_la_primera_lectura():
    m = _cargar_lecturas()
    modulo = "filosofia_ia/clase_1"
    lecturas = m.LECTURAS[modulo]
    doc = m.construir_html(
        modulo, lecturas, {l.id: "palabra " * 120 for l in lecturas},
        [], m.PDFS[modulo], m._introduccion(modulo)
    )
    assert doc.index("Cómo leer este cuadernillo") < doc.index("<h2>Fragmento")
