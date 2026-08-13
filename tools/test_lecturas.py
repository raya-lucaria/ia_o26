"""Guardas del cuadernillo de lecturas.

Aqui no se construye ningun PDF: WeasyPrint y los PDF con derechos no estan
disponibles en CI. Se prueban funciones puras y archivos versionados.
"""
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
MODULO = RAIZ / "lecturas/filosofia_ia/clase_1"
INTRO = MODULO / "introduccion.md"
PAGINA = RAIZ / "course/2_filosofia_ia/1_accelerate_what.md"
TAREA = RAIZ / "course/2_filosofia_ia/_official/tasks/1_leer_cuadernillo.yaml"
VISOR = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_1.html"
LECTURAS_README = MODULO / "README.md"
PUBLICADO = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf"
CONSTRUIDO = MODULO / "lecturas/filosofia_ia_clase_1_cuadernillo.pdf"

# Modulo 2 -- "The Left Takes the Future Back"
MODULO_2 = RAIZ / "lecturas/filosofia_ia/clase_2"
PAGINA_2 = RAIZ / "course/2_filosofia_ia/5_left_takes_future.md"
TAREA_2 = RAIZ / "course/2_filosofia_ia/_official/tasks/2_leer_cuadernillo_modulo_2.yaml"
VISOR_2 = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_2.html"
LECTURAS_README_2 = MODULO_2 / "README.md"
PUBLICADO_2 = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_2_left_future.pdf"
CONSTRUIDO_2 = MODULO_2 / "lecturas/filosofia_ia_clase_2_cuadernillo.pdf"

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


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


# (publicado en _assets/, construido por el pipeline en lecturas/) por modulo.
PARES_PDF_PUBLICADO_CONSTRUIDO = [
    (PUBLICADO, CONSTRUIDO),
    (PUBLICADO_2, CONSTRUIDO_2),
]


@pytest.mark.parametrize("publicado,construido", PARES_PDF_PUBLICADO_CONSTRUIDO)
def test_el_pdf_publicado_es_el_que_se_construyo(publicado, construido):
    """El cuadernillo publicado en course/2_filosofia_ia/_assets/ se copia a
    mano desde lecturas/.../lecturas/<modulo>_cuadernillo.pdf; no hay paso
    mecanico que los mantenga sincronizados. Esta guarda compara los SHA-256
    de las dos copias YA VERSIONADAS en git, no contra una reconstruccion
    fresca: pypdf escribe metadatos internos (fechas, IDs) que cambian de una
    corrida a otra aunque el contenido de las paginas sea identico, asi que
    comparar contra un rebuild fallaria en falso incluso cuando el copiado a
    mano se hizo bien. Comparar las dos copias versionadas es lo unico que
    detecta de verdad "se reconstruyo y no se volvio a copiar".
    """
    assert _sha256(publicado) == _sha256(construido), (
        f"{publicado.relative_to(RAIZ)} no coincide (SHA-256 distinto) con "
        f"{construido.relative_to(RAIZ)}: se reconstruyo el cuadernillo y no "
        "se copio el resultado al asset publicado (o viceversa)."
    )


# Cada entrada busca, en un archivo, la frase exacta donde se declara la
# cifra TOTAL de paginas del cuadernillo (no las subcifras de una lectura
# suelta, como las 12 paginas del extracto de Fisher o las 7 del original de
# Swarmachines). Si el patron deja de encontrarse porque alguien reescribio
# la frase, la prueba tambien debe fallar: por eso el assert exige el match.
PATRONES_PAGINAS_TOTALES = [
    (PAGINA, "1_accelerate_what.md (resumen)", r"cuadernillo de (\d+) páginas"),
    (PAGINA, "1_accelerate_what.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
    (TAREA, "1_leer_cuadernillo.yaml", r"un solo archivo de (\d+) páginas"),
    (VISOR, "visor_modulo_1.html", r"Seis lecturas · (\d+) páginas ·"),
    (LECTURAS_README, "README.md (resumen)", r"Seis lecturas, (\d+) páginas,"),
    (LECTURAS_README, "README.md (cuadernillo)",
     r"\*\*(\d+) páginas, las seis lecturas completas\*\*"),
]


# Mismas frases-ancla que PATRONES_PAGINAS_TOTALES, pero para el modulo 2
# ("The Left Takes the Future Back", 53 paginas). Lista aparte porque la
# cifra de un modulo no tiene por que coincidir con la del otro; mezclarlas
# en una sola lista haria que test_las_paginas_del_cuadernillo_coinciden_...
# fallara siempre (57 != 53) aunque cada modulo este internamente consistente.
PATRONES_PAGINAS_TOTALES_MODULO_2 = [
    (PAGINA_2, "5_left_takes_future.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
    (TAREA_2, "2_leer_cuadernillo_modulo_2.yaml", r"un solo archivo de (\d+) páginas"),
    (VISOR_2, "visor_modulo_2.html", r"Cuatro lecturas · (\d+) páginas ·"),
    (LECTURAS_README_2, "README.md modulo 2 (resumen)", r"Cuatro lecturas, (\d+) páginas,"),
    (LECTURAS_README_2, "README.md modulo 2 (cuadernillo)",
     r"\*\*(\d+) páginas, las cuatro lecturas completas\*\*"),
]


def _verificar_cifra_total_de_paginas(patrones, pdf):
    vistas = []
    for ruta, etiqueta, patron in patrones:
        texto = ruta.read_text(encoding="utf-8")
        m = re.search(patron, texto)
        assert m, (
            f"{etiqueta}: no se encontró la frase que declara la cifra total "
            f"de páginas (se buscó {patron!r})"
        )
        vistas.append((etiqueta, int(m.group(1))))

    # El PDF publicado es la sexta voz de la comparacion, y la unica que no se
    # escribe a mano. Sin ella las cinco frases pueden estar de acuerdo entre
    # si y equivocadas todas: un cuadernillo reconstruido sin los PDF en
    # derechos sale mas corto y ninguna de las cinco lo nota.
    import pypdf
    vistas.append((f"{pdf.name} (PDF)", len(pypdf.PdfReader(pdf).pages)))

    cifras = {n for _, n in vistas}
    assert len(cifras) == 1, (
        "la cifra total de páginas del cuadernillo no coincide entre "
        "archivos: " + ", ".join(f"{etiqueta}={n}" for etiqueta, n in vistas)
    )


def test_las_paginas_del_cuadernillo_coinciden_en_todos_lados():
    _verificar_cifra_total_de_paginas(PATRONES_PAGINAS_TOTALES, PUBLICADO)


def test_las_paginas_del_cuadernillo_modulo_2_coinciden_en_todos_lados():
    _verificar_cifra_total_de_paginas(PATRONES_PAGINAS_TOTALES_MODULO_2, PUBLICADO_2)


def test_toda_lectura_en_pdf_declara_que_debe_contener():
    """La via de PDF tiene que ser tan fail-loud como la de descarga.

    `bajar_lecturas.py` verifica cada texto descargado contra su
    `debe_contener`; sin esta guarda, una LecturaPDF nueva podria entrar sin
    frase que verificar y su recorte pasaria sin comprobacion alguna.
    """
    m = _cargar_lecturas()
    for modulo, lecturas in m.PDFS.items():
        for lp in lecturas:
            assert getattr(lp, "debe_contener", "").strip(), (
                f"{modulo}/{lp.id}: no declara debe_contener"
            )


@pytest.mark.parametrize("modulo,ids", [
    ("filosofia_ia/clase_1", ["deleuze-guattari-antiedipo", "fisher-terminator-avatar"]),
    ("filosofia_ia/clase_2", ["fisher-capitalist-realism-cap4", "srnicek-williams-post-work"]),
])
def test_toda_lectura_en_pdf_tiene_enlace_a_su_edicion(modulo, ids):
    """Si el PDF fuente no esta —y no esta en ningun clon nuevo: `.gitignore`
    lo excluye—, el cuadernillo se construye sin esa lectura. ENLACES es lo
    que hace que la omision se vea en la portadilla en vez de pasar callada,
    y el filtro de construir() empareja por el apellido del autor."""
    m = _cargar_lecturas()
    enlaces = m.ENLACES.get(modulo, [])
    for lp in m.PDFS[modulo]:
        assert lp.id in ids
        apellido = lp.autor.split()[-1]
        assert any(apellido in e["cita"] for e in enlaces), (
            f"{modulo}/{lp.id}: ninguna entrada de ENLACES menciona "
            f"«{apellido}», así que si falta el PDF la lectura se omite sin "
            "aviso en el cuadernillo"
        )
