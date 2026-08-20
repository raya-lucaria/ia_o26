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
PAGINA = RAIZ / "course/2_filosofia_ia/1_aceleracionismo/0_index.md"
TAREA = RAIZ / "course/2_filosofia_ia/_official/tasks/1_leer_cuadernillo.yaml"
VISOR = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_1.html"
LECTURAS_README = MODULO / "README.md"
PUBLICADO = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf"
CONSTRUIDO = MODULO / "lecturas/filosofia_ia_clase_1_cuadernillo.pdf"

# Modulo 2 -- "The Left Takes the Future Back"
MODULO_2 = RAIZ / "lecturas/filosofia_ia/clase_2"
PAGINA_2 = RAIZ / "course/2_filosofia_ia/2_aceleracionismo_de_izquierda/0_index.md"
TAREA_2 = RAIZ / "course/2_filosofia_ia/_official/tasks/2_leer_cuadernillo_modulo_2.yaml"
VISOR_2 = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_2.html"
LECTURAS_README_2 = MODULO_2 / "README.md"
PUBLICADO_2 = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_2_left_future.pdf"
CONSTRUIDO_2 = MODULO_2 / "lecturas/filosofia_ia_clase_2_cuadernillo.pdf"

# Modulo 3 -- "Exit, NRx & Dark Enlightenment"
MODULO_3 = RAIZ / "lecturas/filosofia_ia/clase_3"
PAGINA_3 = RAIZ / "course/2_filosofia_ia/3_aceleracionismo_de_derecha/0_index.md"
TAREA_3 = RAIZ / "course/2_filosofia_ia/_official/tasks/3_leer_cuadernillo_modulo_3.yaml"
VISOR_3 = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_3.html"
LECTURAS_README_3 = MODULO_3 / "README.md"
PUBLICADO_3 = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_3_exit_nrx.pdf"
CONSTRUIDO_3 = MODULO_3 / "lecturas/filosofia_ia_clase_3_cuadernillo.pdf"

# Modulo 4 -- "Moloch, Rationality & the Long Future"
MODULO_4 = RAIZ / "lecturas/filosofia_ia/clase_4"
PAGINA_4 = RAIZ / "course/2_filosofia_ia/4_futuro_largo/0_index.md"
TAREA_4 = RAIZ / "course/2_filosofia_ia/_official/tasks/4_leer_cuadernillo_modulo_4.yaml"
VISOR_4 = RAIZ / "course/2_filosofia_ia/_assets/visor_modulo_4.html"
LECTURAS_README_4 = MODULO_4 / "README.md"
PUBLICADO_4 = RAIZ / "course/2_filosofia_ia/_assets/cuadernillo_modulo_4_long_future.pdf"
CONSTRUIDO_4 = MODULO_4 / "lecturas/filosofia_ia_clase_4_cuadernillo.pdf"

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
    # PDFS con .get: el modulo 3 no tiene ninguna lectura en PDF externo, y
    # con m.PDFS[modulo] este helper reventaria con KeyError al usarlo con el.
    m = _cargar_lecturas()
    return list(m.LECTURAS[modulo]) + list(m.PDFS.get(modulo, []))


@pytest.mark.parametrize("modulo", [
    "filosofia_ia/clase_1", "filosofia_ia/clase_2", "filosofia_ia/clase_3",
    "filosofia_ia/clase_4",
])
def test_toda_lectura_trae_introduccion(modulo):
    for x in _todas_las_lecturas(modulo):
        assert not hasattr(x, "por_que"), f"{x.id}: por_que quedo vivo"
        for apartado in APARTADOS:
            assert apartado in x.introduccion, f"{x.id}: le falta {apartado}"


@pytest.mark.parametrize("modulo,cuantas", [
    ("filosofia_ia/clase_1", 6),
    ("filosofia_ia/clase_2", 4),
    ("filosofia_ia/clase_3", 4),
    ("filosofia_ia/clase_4", 6),
])
def test_el_orden_es_consecutivo_y_unico(modulo, cuantas):
    ordenes = sorted(x.orden for x in _todas_las_lecturas(modulo))
    assert ordenes == list(range(1, cuantas + 1)), (
        f"{modulo}: el orden debe ser 1..{cuantas} sin huecos ni repetidos, y "
        f"es {ordenes}. El intercalado de los PDF externos depende de ello."
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


def test_markdown_basico_convierte_enlace_web_en_ancla():
    m = _cargar_lecturas()
    resultado = m._markdown_basico(
        "[escucha las ocho partes](https://www.youtube.com/watch?v=SeohwQls2GE)"
    )
    assert (
        '<a href="https://www.youtube.com/watch?v=SeohwQls2GE">'
        "escucha las ocho partes</a>"
    ) in resultado


def test_markdown_basico_no_activa_enlaces_http():
    m = _cargar_lecturas()
    resultado = m._markdown_basico("[sitio inseguro](http://example.com)")
    assert "<a " not in resultado
    assert "http://example.com" in resultado


def test_markdown_basico_no_corrompe_asteriscos_en_url_https():
    m = _cargar_lecturas()
    resultado = m._markdown_basico("[ruta](https://example.com/*path*)")
    assert '<a href="https://example.com/*path*">ruta</a>' in resultado
    assert "<em>path</em>" not in resultado


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
    (PUBLICADO_3, CONSTRUIDO_3),
    (PUBLICADO_4, CONSTRUIDO_4),
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
    (PAGINA, "modulo 1 · 0_index.md (resumen)", r"cuadernillo de (\d+) páginas"),
    (PAGINA, "modulo 1 · 0_index.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
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
    (PAGINA_2, "modulo 2 · 0_index.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
    (TAREA_2, "2_leer_cuadernillo_modulo_2.yaml", r"un solo archivo de (\d+) páginas"),
    (VISOR_2, "visor_modulo_2.html", r"Cuatro lecturas · (\d+) páginas ·"),
    (LECTURAS_README_2, "README.md modulo 2 (resumen)", r"Cuatro lecturas, (\d+) páginas,"),
    (LECTURAS_README_2, "README.md modulo 2 (cuadernillo)",
     r"\*\*(\d+) páginas, las cuatro lecturas completas\*\*"),
]


# Igual para el modulo 3 ("Exit, NRx & Dark Enlightenment"). Su README declara
# la cifra tres veces —la tercera comparandola con las 53 del modulo 2—, y las
# tres entran aqui: la comparacion es justo la que se queda vieja al rehacer el
# cuadernillo.
# El modulo 4 es el mas largo de la unidad y se compara contra el 1, que era el
# que lo era antes. Sin "completas" ni "las seis lecturas completas": del
# articulo de Greaves y MacAskill van las secciones 1 a 4 y la 10, no entero.
PATRONES_PAGINAS_TOTALES_MODULO_4 = [
    (PAGINA_4, "modulo 4 · 0_index.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
    (TAREA_4, "4_leer_cuadernillo_modulo_4.yaml", r"un solo archivo de (\d+)\s"),
    (VISOR_4, "visor_modulo_4.html", r"Seis lecturas · (\d+) páginas ·"),
    (LECTURAS_README_4, "README.md modulo 4 (resumen)", r"Seis lecturas, (\d+) páginas,"),
    (LECTURAS_README_4, "README.md modulo 4 (comparación)",
     r"de la unidad: (\d+) páginas frente a las 57"),
    (LECTURAS_README_4, "README.md modulo 4 (cuadernillo)",
     r"\*\*(\d+) páginas, las seis lecturas\*\*"),
]

PATRONES_PAGINAS_TOTALES_MODULO_3 = [
    (PAGINA_3, "modulo 3 · 0_index.md (cuerpo)", r"\*\*(\d+) páginas\*\*, cada lectura"),
    (TAREA_3, "3_leer_cuadernillo_modulo_3.yaml", r"un solo archivo de (\d+)\s"),
    (VISOR_3, "visor_modulo_3.html", r"Cuatro lecturas · (\d+) páginas ·"),
    (LECTURAS_README_3, "README.md modulo 3 (resumen)", r"Cuatro lecturas, (\d+) páginas,"),
    (LECTURAS_README_3, "README.md modulo 3 (comparación)",
     r"la unidad: (\d+) páginas frente a las 53"),
    # Sin "completas", a diferencia de los modulos 1 y 2: de Patchwork va solo
    # la segunda mitad del capitulo, asi que el README no puede decir que las
    # cuatro lecturas esten completas sin contradecir su propia tabla.
    (LECTURAS_README_3, "README.md modulo 3 (cuadernillo)",
     r"\*\*(\d+) páginas, las cuatro lecturas\*\*"),
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


def test_las_paginas_del_cuadernillo_modulo_3_coinciden_en_todos_lados():
    _verificar_cifra_total_de_paginas(PATRONES_PAGINAS_TOTALES_MODULO_3, PUBLICADO_3)


def test_las_paginas_del_cuadernillo_modulo_4_coinciden_en_todos_lados():
    _verificar_cifra_total_de_paginas(PATRONES_PAGINAS_TOTALES_MODULO_4, PUBLICADO_4)


@pytest.mark.parametrize("pdf", [CONSTRUIDO_4, PUBLICADO_4])
def test_el_cuadernillo_modulo_4_enlaza_el_audio_de_moloch(pdf):
    import pypdf

    esperado = "https://www.youtube.com/watch?v=SeohwQls2GE"
    enlaces = []
    for pagina in pypdf.PdfReader(pdf).pages:
        for referencia in pagina.get("/Annots", []):
            anotacion = referencia.get_object()
            uri = anotacion.get("/A", {}).get("/URI")
            if uri:
                enlaces.append(uri)
    assert esperado in enlaces, (
        f"{pdf.name}: la ficha de Moloch debe enlazar el audio completo en YouTube"
    )


# (modulo, PDF publicado) para la guarda de abajo.
MODULOS_CON_CUADERNILLO = [
    ("filosofia_ia/clase_1", PUBLICADO),
    ("filosofia_ia/clase_2", PUBLICADO_2),
    ("filosofia_ia/clase_3", PUBLICADO_3),
    ("filosofia_ia/clase_4", PUBLICADO_4),
]


def _solo_letras(texto: str) -> str:
    """Deja solo letras minusculas, sin acentos ni espacios ni puntuacion.

    Es lo unico que sobrevive intacto al viaje introduccion.md -> WeasyPrint ->
    pdftotext: el PDF justifica, parte palabras con guion suave (U+2010) y mete
    saltos de linea donde el Markdown no los tiene, asi que comparar texto con
    espacios o con guiones da falsos negativos.
    """
    import unicodedata
    plano = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in plano if c.isalpha() and c.isascii())


@pytest.mark.parametrize("modulo,pdf", MODULOS_CON_CUADERNILLO)
def test_el_cuadernillo_publicado_trae_la_introduccion_vigente(modulo, pdf):
    """El PDF publicado tiene que venir del `introduccion.md` de hoy.

    `test_el_pdf_publicado_es_el_que_se_construyo` compara las dos copias del
    PDF entre si, asi que pasa igual de contenta si las dos son viejas. Editar
    `introduccion.md` (o una ficha) y olvidarse de correr `lecturas.py` deja el
    cuadernillo diciendo una cosa y la fuente otra, y nada lo notaba: paso
    exactamente eso al escribir el modulo 3, con «once partes» impreso en el PDF
    despues de que la fuente ya decia «diez». Se comprueba un tramo largo del
    tercer parrafo, no el archivo entero: el PDF reflowea y no reproduce los
    saltos de parrafo del Markdown.
    """
    import pypdf
    intro = (RAIZ / "lecturas" / modulo / "introduccion.md").read_text(encoding="utf-8")
    parrafos = [p for p in intro.split("\n\n")[1:] if len(_solo_letras(p)) > 300]
    assert parrafos, f"{modulo}: introduccion.md no tiene ningun parrafo largo que comprobar"
    texto_pdf = _solo_letras(
        " ".join((p.extract_text() or "") for p in pypdf.PdfReader(pdf).pages)
    )
    for parrafo in parrafos:
        aguja = _solo_letras(parrafo)[:300]
        assert aguja in texto_pdf, (
            f"{pdf.name}: un párrafo de lecturas/{modulo}/introduccion.md no "
            "aparece en el cuadernillo publicado. Se editó la introducción y no "
            f"se reconstruyó el PDF: corre `python3 tools/lecturas.py {modulo}` "
            "y vuelve a copiarlo a _assets/. Párrafo: "
            f"{' '.join(parrafo.split())[:90]!r}"
        )


@pytest.mark.parametrize("modulo,pdf", MODULOS_CON_CUADERNILLO)
def test_el_cuadernillo_publicado_trae_las_fichas_vigentes(modulo, pdf):
    """Lo mismo que la guarda de arriba, pero para las fichas de `LECTURAS`.

    La de arriba solo muestrea `introduccion.md`, y su docstring prometia cubrir
    tambien «una ficha» sin cubrirla: editar el campo `introduccion` de una
    Lectura en tools/lecturas.py y olvidarse de reconstruir dejaba el PDF
    diciendo otra cosa, y las 102 pruebas pasaban. Paso dos veces al agregar la
    cuarta lectura al modulo 3 —«las tres» impreso donde la fuente ya decia «las
    cuatro»—, y por eso existe esta.

    Se comprueban DOS tramos de cada apartado largo -el principio y el final-,
    con la misma normalizacion a solo-letras: el PDF justifica, parte palabras
    con guion suave y reflowea, asi que comparar texto con espacios da falsos
    negativos. Los dos tramos, y no solo el primero, porque la edicion tipica es
    retocar el final de una frase; con un solo tramo al inicio esta guarda ya
    dejo pasar en vivo una ficha editada por la cola.
    """
    import pypdf
    m = _cargar_lecturas()
    texto_pdf = _solo_letras(
        " ".join((p.extract_text() or "") for p in pypdf.PdfReader(pdf).pages)
    )
    comprobados = 0
    for lectura in _todas_las_lecturas(modulo):
        for apartado in lectura.introduccion.split("\n\n"):
            plano = _solo_letras(apartado)
            if len(plano) < 200:
                continue
            comprobados += 1
            for donde, aguja in (("empieza", plano[:150]), ("termina", plano[-150:])):
                assert aguja in texto_pdf, (
                    f"{pdf.name}: el apartado que {donde} asi, en la ficha de "
                    f"«{lectura.id}», no aparece en el cuadernillo publicado. Se "
                    "editó la ficha en tools/lecturas.py y no se reconstruyó el "
                    f"PDF: corre `python3 tools/lecturas.py {modulo}` y vuelve a "
                    f"copiarlo a _assets/. Apartado: "
                    f"{' '.join(apartado.split())[:90]!r}"
                )
    assert comprobados, f"{modulo}: ninguna ficha tiene un apartado largo que comprobar"


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


# (visor, pagina del modulo) por modulo. El visor es HTML a mano dentro de
# _assets/, asi que su boton de vuelta es una URL escrita a dedo: nada la
# reescribe cuando la pagina se mueve.
PARES_VISOR_PAGINA = [
    (VISOR, PAGINA),
    (VISOR_2, PAGINA_2),
    (VISOR_3, PAGINA_3),
    (VISOR_4, PAGINA_4),
]


@pytest.mark.parametrize("visor,pagina", PARES_VISOR_PAGINA)
def test_el_visor_vuelve_a_la_url_publicada_de_su_modulo(visor, pagina):
    """El boton «Volver al modulo» del visor apuntaba al id estable de la
    pagina (`/filosofia-ia/moloch-long-future/`), pero el segmento publicado
    sale del NOMBRE DEL DIRECTORIO del modulo (`4_futuro_largo` ->
    `futuro-largo`). Al anidar la unidad, los cuatro botones se quedaron
    apuntando a un 404 -- y no lo vio ni `raya validate`, que no mira dentro
    de _assets/, ni el resto de la suite. Se descubrio en el sitio desplegado.
    """
    segmento = re.sub(r"^\d+_", "", pagina.parent.name).replace("_", "-")
    esperado = f"filosofia-ia/{segmento}/index.html"
    html = visor.read_text(encoding="utf-8")
    hrefs = re.findall(r'href="([^"]*filosofia-ia/[^"]*)"', html)
    assert hrefs, f"{visor.name}: no enlaza de vuelta a ninguna pagina del curso"
    for href in hrefs:
        assert href.endswith(esperado), (
            f"{visor.name}: enlaza a «{href}», que ya no es la URL publicada "
            f"de {pagina.relative_to(RAIZ)}; deberia terminar en «{esperado}»"
        )
