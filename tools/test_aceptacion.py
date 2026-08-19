"""Verifica los criterios de aceptacion del spec 2026-08-09-historia-ia-design.md, S10.

Cada test_1..test_10 corresponde, en orden, a uno de los diez criterios de esa
seccion. test_extra_avisos_generadas verifica un criterio adicional que el diseno
exige (S6.2: "Cada ilustracion generada se identifica como tal en el pie de
figura") pero que el brief original no cubria.

Notas frente al brief original de la Tarea 18:
- El tope de peso del repositorio es 21 MB, no 10: subio a 16 porque 53
  imagenes ya ocupaban 8.9 MB antes de las ilustraciones generadas, y a 21 al
  publicarse el cuadernillo del modulo 2. Ver TOPE_REPOSITORIO.
- navigation.json es una lista PLANA en "items"; "children" contiene ids en
  texto, no objetos anidados. No hay que recorrer recursivamente.
"""

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

from unidades import ASSETS_POR_UNIDAD

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = RAIZ / "course/1_introduccion/2_historia_ia"
ASSETS = UNIDAD / "_assets"
ARTEFACTO = RAIZ / "artifact"
RAYA_LUCARIA = Path(os.environ.get("RAYA_LUCARIA", "/home/uumami/itam/raya_lucaria"))

# Los criterios 1 y 2 necesitan el CLI `raya`, que vive en un repositorio
# hermano y no existe en CI. Alli se saltan: el workflow de GitHub ya valida y
# construye el curso por su cuenta, asi que la cobertura no se pierde.
sin_cli = pytest.mark.skipif(
    not (RAYA_LUCARIA / "pyproject.toml").is_file(),
    reason=f"El CLI raya no esta en {RAYA_LUCARIA}; CI lo cubre por su cuenta",
)

# artifact/ es salida generada y esta en .gitignore, asi que no existe en un
# clon nuevo. Los criterios que lo inspeccionan se saltan si no se construyo.
sin_artefacto = pytest.mark.skipif(
    not (ARTEFACTO / "manifest.json").is_file(),
    reason="No hay artifact/ construido; corre `raya build` primero",
)

PAGINAS = [
    "0_index.md", "1_imaginar_la_maquina.md", "2_que_es_inteligencia.md",
    "3_arco_historico.md", "4_por_que_el_boom.md", "5_estado_actual.md",
    "6_otras_raices.md", "7_ia_y_sociedad.md", "8_material_adicional.md",
]

PAGINAS_UNIDAD_EN_ORDEN = [
    "imaginar-la-maquina", "que-es-inteligencia", "arco-historico",
    "por-que-el-boom", "estado-actual", "otras-raices", "ia-y-sociedad",
    "material-adicional",
]

# Apellidos/nombres de personas reales retratadas en foto-*.jpg (Capa B). Ninguno
# debe aparecer en la fila de CREDITOS.md de una ilustracion generada (Capa C),
# ni en el nombre de archivo de una ilustracion generada.
PERSONAS_REALES = [
    "turing", "lovelace", "babbage", "rosenblatt", "shannon", "von neumann",
    "nash", "wiener", "pitts", "hinton", "lecun", "bengio", "schmidhuber",
    "pearl", "hopfield", "fei-fei li", "weizenbaum", "mccarthy", "minsky",
    "selfridge", "kasparov",
]


def _run_raya(*args):
    return subprocess.run(
        ["uv", "run", "--offline", "raya", *args, str(RAIZ)],
        cwd=RAYA_LUCARIA,
        env={**os.environ, "UV_PROJECT_ENVIRONMENT": ".venv-local"},
        capture_output=True, text=True,
    )


@sin_cli
def test_1_raya_validate_pasa_sin_errores_ni_advertencias():
    salida = _run_raya("validate")
    assert "ERROR |" not in salida.stdout, salida.stdout
    assert "WARN |" not in salida.stdout, salida.stdout
    assert "Course validation passed" in salida.stdout, salida.stdout


@sin_cli
@sin_artefacto
def test_2_build_genera_artefacto_y_preview_serviria_sin_enlaces_rotos():
    build = _run_raya("build")
    assert "ERROR |" not in build.stdout, build.stdout
    assert "Course artifact build passed" in build.stdout, build.stdout
    assert (ARTEFACTO / "site/index.html").is_file()
    assert (ARTEFACTO / "manifest.json").is_file()

    dry_run = subprocess.run(
        ["uv", "run", "--offline", "raya", "preview", str(RAIZ), "--dry-run"],
        cwd=RAYA_LUCARIA,
        env={**os.environ, "UV_PROJECT_ENVIRONMENT": ".venv-local"},
        capture_output=True, text=True,
    )
    assert "ERROR |" not in dry_run.stdout, dry_run.stdout
    assert "would_serve=true" in dry_run.stdout, dry_run.stdout


@sin_artefacto
def test_3_las_ocho_paginas_aparecen_en_navegacion_en_orden_bajo_introduccion():
    nav = json.loads((ARTEFACTO / "data/navigation.json").read_text())
    items = {it["id"]: it for it in nav["items"]}

    historia = items["historia-ia"]
    assert historia["parent"] == "intro-unidad"
    assert items["intro-unidad"]["nav_title"] == "Introducción"
    assert historia["children"] == PAGINAS_UNIDAD_EN_ORDEN, (
        f"orden inesperado: {historia['children']}"
    )
    for id_pagina in PAGINAS_UNIDAD_EN_ORDEN:
        assert id_pagina in items, f"falta en navegacion: {id_pagina}"


@sin_artefacto
def test_4_objetos_oficiales_con_scope_correctamente_inferido():
    objetos = json.loads((ARTEFACTO / "data/official.json").read_text())["objects"]
    de_unidad = [o for o in objetos if o["scope"]["quantum"] == "historia-ia"]

    tipos = {o["type"] for o in de_unidad}
    assert {"card", "quiz", "prompt", "task"} <= tipos, f"tipos presentes: {tipos}"

    tareas = [o for o in de_unidad if o["type"] == "task"]
    assert len(tareas) == 1, "la unidad debe tener exactamente una tarea: estudiar"
    assert len([o for o in de_unidad if o["type"] == "card"]) >= 20
    assert len([o for o in de_unidad if o["type"] == "quiz"]) >= 1
    assert len([o for o in de_unidad if o["type"] == "prompt"]) >= 5

    # scope.quantum inferido correctamente: nada de esta unidad quedo asignado
    # al curso completo, y viceversa.
    de_curso = [o for o in objetos if o["scope"]["quantum"] == "course-root"]
    ids_unidad = {o["id"] for o in de_unidad}
    ids_curso = {o["id"] for o in de_curso}
    assert ids_unidad.isdisjoint(ids_curso)


def test_5_toda_imagen_tiene_credito_y_las_generadas_estan_marcadas():
    creditos_texto = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8")
    creditos = creditos_texto.lower()

    for img in ASSETS.iterdir():
        if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".gif"}:
            assert img.name.lower() in creditos, f"{img.name} sin credito"

    generadas = sorted(
        p for p in ASSETS.iterdir()
        if p.stem.startswith("ilus-") and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    assert generadas, "no se encontraron ilustraciones generadas (ilus-*)"
    for img in generadas:
        fila = [l for l in creditos_texto.splitlines() if img.name.lower() in l.lower()]
        assert fila, f"{img.name} sin fila en CREDITOS.md"
        assert "generad" in fila[0].lower(), f"{img.name} sin marca de generada"


def test_5b_toda_imagen_en_assets_esta_referenciada_por_alguna_pagina():
    """Lo inverso de test_5: que toda imagen tenga credito no evita que se
    quede sin usar. Esto es exactamente lo que dejo pasar 23 de 74 recursos
    comiteados y acreditados (4.4 MB) sin que ninguna pagina los
    mencionara (hallazgo H7 de la revision final). CREDITOS.md no cuenta
    como pagina -- una fila de creditos no es un uso."""
    texto_paginas = " ".join(
        (UNIDAD / p).read_text(encoding="utf-8")
        for p in PAGINAS if (UNIDAD / p).is_file()
    )
    extensiones = {".png", ".jpg", ".jpeg", ".svg", ".gif"}
    huerfanas = sorted(
        img.name for img in ASSETS.iterdir()
        if img.suffix.lower() in extensiones and img.name not in texto_paginas
    )
    assert not huerfanas, f"imagenes en _assets/ sin usar en ninguna pagina: {huerfanas}"


def test_6_ninguna_generada_representa_persona_real_o_evento_documentado():
    creditos_texto = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8")
    filas_generadas = [
        linea for linea in creditos_texto.splitlines()
        if re.match(r"\|\s*ilus-", linea, re.I)
    ]
    assert filas_generadas, "no hay filas de ilustraciones generadas en CREDITOS.md"

    for fila in filas_generadas:
        fila_baja = fila.lower()
        for persona in PERSONAS_REALES:
            assert persona not in fila_baja, (
                f"una ilustracion generada menciona a una persona real ({persona}): {fila}"
            )

    for img in ASSETS.glob("ilus-*"):
        nombre = img.name.lower()
        for persona in PERSONAS_REALES:
            assert persona.replace(" ", "-") not in nombre, (
                f"nombre de archivo generado sugiere una persona real: {img.name}"
            )


def _filas_de_tabla(texto):
    """Devuelve (encabezado, filas) de la primera tabla Markdown del texto,
    como listas de celdas. Omite la fila separadora ("|---|---|...")."""
    lineas = [l for l in texto.splitlines() if l.strip().startswith("|")]
    encabezado, filas = None, []
    for linea in lineas:
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if encabezado is None:
            encabezado = celdas
            continue
        if all(set(c) <= {"-", " ", ":"} for c in celdas):
            continue  # fila separadora
        filas.append(celdas)
    return encabezado, filas


def test_7_toda_fecha_y_atribucion_tiene_fuente_verificada():
    """Cada FILA de afirmacion debe tener su propia celda de verificacion
    marcada -- no basta con que el archivo contenga un "si" en algun lugar.
    (`re.search` contra el texto completo daba un solo "si" por bueno para
    toda la pagina; el mismo agujero de substring-contra-todo-el-archivo que
    ya se cerro dos veces en las pruebas de creditos.)

    8_material_adicional.md no tiene columna "Verificado" con si/no: verifica
    enlaces por codigo HTTP en una columna "Código HTTP", y ahi se exige 200
    en cada fila en vez de "si"."""
    for pagina in PAGINAS:
        registro = RAIZ / "docs/verificacion" / pagina
        assert registro.is_file(), f"falta {registro.relative_to(RAIZ)}"
        texto = registro.read_text(encoding="utf-8")
        encabezado, filas = _filas_de_tabla(texto)
        assert encabezado and filas, f"{pagina}: no se encontro tabla de verificacion"

        if "Código HTTP" in encabezado:
            columna = encabezado.index("Código HTTP")
            for fila in filas:
                assert fila[columna].strip() == "200", (
                    f"{pagina}: fila sin codigo 200 en 'Código HTTP': {fila}"
                )
        else:
            assert "Verificado" in encabezado, f"{pagina}: tabla sin columna 'Verificado'"
            columna = encabezado.index("Verificado")
            for fila in filas:
                celda = fila[columna].strip().lower()
                # La celda puede ser exacta ("sí") o una frase que empieza
                # con "Sí" seguida de evidencia ("Sí. ACM anuncio..."; "sí —
                # corrige..."). Ambas cuentan como verificado; cualquier otra
                # cosa (vacio, "no", "pendiente") no.
                assert re.match(r"^s[ií]\b", celda), (
                    f"{pagina}: fila sin verificar en la columna 'Verificado': {fila}"
                )


# El tope subio de 10 a 16 MB cuando las 53 imagenes de la unidad de historia
# ya ocupaban 8.9 MB, y de 16 a 21 MB al publicarse el cuadernillo del modulo 2.
# Cada modulo de lecturas cuesta unos 2.8 MB, y la mitad de eso es duplicacion
# deliberada: el PDF vive en lecturas/ y copiado en _assets/, con una guarda que
# exige que sean identicos byte a byte. Medido en agosto de 2026, tras las dos
# paginas de repaso del modulo 2 y sus ocho imagenes: 17.9 MB, o sea 3.1 MB de
# margen. El modulo 3 costo mucho menos que los dos anteriores —0.74 MB, y el
# total quedo en 18.7 MB— porque ninguna de sus cuatro lecturas llega como PDF
# escaneado: el cuadernillo es texto y pesa 182 KB por copia, frente al megabyte
# largo de los otros dos. Quedan 2.3 MB. La cuarta lectura, agregada en
# agosto de 2026, costo 0.19 MB entre las dos copias del PDF y la fuente.
# Otro modulo de solo texto cabe; uno con lecturas en PDF, no. Cuando el
# siguiente vuelva a chocar contra el tope, la decision ya no es subirlo otra
# vez. Generar los cuadernillos en CI NO es la salida: el pipeline necesita
# weasyprint y pypdf, que CI no instala, y sobre todo los PDF en derechos de
# fuentes/, que estan en .gitignore y nunca van a estar en un runner. Las dos
# salidas que si existen son sacar los PDF construidos del arbol de git a Git
# LFS, o dejar de versionarlos y publicarlos como adjuntos de un release de
# GitHub, enlazados desde la pagina del curso.
TOPE_REPOSITORIO = 21_000_000


def test_8_el_repositorio_pesa_menos_del_tope():
    salida = subprocess.run(
        ["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True
    )
    total = sum(
        (RAIZ / n).stat().st_size
        for n in salida.stdout.split("\0") if n and (RAIZ / n).is_file()
    )
    assert total < TOPE_REPOSITORIO, (
        f"el repositorio pesa {total / 1e6:.1f} MB "
        f"(tope: {TOPE_REPOSITORIO / 1e6:.0f} MB)"
    )


def test_9_los_diagramas_svg_son_legibles_sobre_el_fondo_oscuro_del_skin():
    # Recorre las dos unidades con figuras propias: la guarda nacio cuando solo
    # existia la de historia, y un SVG ilegible en filosofia se publicaba sin
    # que nada lo notara. El "assert svgs" es por unidad, no global: un
    # "assert svgs" global pasaria aunque _assets de filosofia se quedara sin
    # ningun SVG propio, mientras los veinte de historia sigan ahi.
    svgs = []
    for unidad, assets in ASSETS_POR_UNIDAD.items():
        svgs_unidad = sorted(assets.glob("*.svg"))
        assert svgs_unidad, f"{unidad}: no hay SVG propios en _assets"
        svgs.extend(svgs_unidad)
    for svg in svgs:
        texto = svg.read_text(encoding="utf-8")
        assert 'viewBox="' in texto, f"{svg.name} sin viewBox"
        assert 'fill="#211033"' in texto, f"{svg.name} sin fondo legible ({'#211033'})"
        assert "aria-label=" in texto, f"{svg.name} sin aria-label"

        # Regresion: el sitio incrusta estos SVG con <img src="...svg">, y el
        # CSS del skin solo trae "max-width: 100%; height: auto" (sin
        # "width"). Un <svg> sin atributos width/height propios (solo
        # viewBox) no tiene tamano intrinseco, y el navegador cae al tamano
        # por omision de un elemento reemplazado (~300x150 CSS px) en vez de
        # llenar el contenedor de la figura: el diagrama se ve minusculo e
        # ilegible aunque el SVG en si sea correcto. Verificado visualmente
        # con Chrome sin interfaz contra el sitio construido (Tarea 18).
        etiqueta_svg = re.match(r"<svg\b[^>]*>", texto)
        assert etiqueta_svg, f"{svg.name}: no se encontro la etiqueta <svg>"
        assert re.search(r'\bwidth="\d', etiqueta_svg.group()), (
            f"{svg.name}: <svg> sin atributo width propio -> se renderiza "
            "minusculo en el sitio (solo tiene viewBox)"
        )
        assert re.search(r'\bheight="\d', etiqueta_svg.group()), (
            f"{svg.name}: <svg> sin atributo height propio -> se renderiza "
            "minusculo en el sitio (solo tiene viewBox)"
        )


def test_10_env_esta_ignorado_por_git():
    salida = subprocess.run(
        ["git", "check-ignore", ".env"], cwd=RAIZ, capture_output=True, text=True
    )
    assert salida.returncode == 0, ".env no esta ignorado por git"


def test_extra_ninguna_ilustracion_generada_aparece_sin_su_aviso_visible():
    """S6.2 del diseno: "Cada ilustracion generada se identifica como tal en el
    pie de figura [...]". El aviso es una linea en cursivas justo despues del
    bloque de figura -- no el texto alternativo de la imagen, que no todo
    lector ve.
    """
    patron_aviso = re.compile(
        r"^\*\(.*ilustraci[oó]n generada.*\)\*\s*$", re.IGNORECASE | re.MULTILINE
    )
    total_usos = 0
    # Un nombre de archivo fijo se rompe en silencio si la pagina se renumera
    # (CLAUDE.md promete que los prefijos numericos son orden de autoria, no
    # identidad estable): con rglob("*.md"), renombrar 2_repaso_y_discusion.md
    # a 3_repaso_y_discusion.md sigue cubierto.
    #
    # rglob y no glob: al partir la unidad de filosofia en un directorio por
    # modulo, un glob("*.md") plano dejo de ver las nueve paginas de repaso y
    # esta guarda paso a cubrir cero ilustraciones sin fallar. La unica pagina
    # que rglob agrega de mas es _assets/CREDITOS.md, que no enlaza figuras.
    PAGINAS_CON_ILUSTRACIONES = [UNIDAD / p for p in PAGINAS] + sorted(
        p for p in (RAIZ / "course/2_filosofia_ia").rglob("*.md")
        if "_assets" not in p.parts
    )
    usos_por_unidad = {"historia": 0, "filosofia": 0}
    for ruta in PAGINAS_CON_ILUSTRACIONES:
        if not ruta.is_file():
            continue
        pagina = ruta.name
        unidad = "filosofia" if "2_filosofia_ia" in ruta.parts else "historia"
        texto = ruta.read_text(encoding="utf-8")
        # El "../" es opcional a proposito: las paginas de historia enlazan a
        # su _assets/ hermano y las de filosofia, desde su directorio de
        # modulo, al _assets/ de la unidad. Sin la alternativa, el patron dejo
        # de calzar con las de filosofia en cuanto se anidaron -- otra vez sin
        # fallar, porque un finditer vacio no falla.
        for match in re.finditer(r"]\((?:\.\./)?_assets/(ilus-[\w-]+\.\w+)\)", texto):
            total_usos += 1
            usos_por_unidad[unidad] += 1
            archivo = match.group(1)
            resto = texto[match.end():match.end() + 400]
            assert patron_aviso.search(resto), (
                f"{pagina}: {archivo} no tiene aviso visible en cursivas "
                "justo despues de su bloque de figura"
            )
    assert total_usos > 0, "no se encontro ningun uso de ilus-* en las paginas"
    # Por unidad, no en total: con una sola cifra global, que las paginas de
    # filosofia dejaran de calzar con el patron no se notaba -- las de historia
    # solas mantenian el total por encima de cero.
    for unidad, usos in usos_por_unidad.items():
        assert usos > 0, f"ningun uso de ilus-* en las paginas de {unidad}"


def test_extra_ningun_wikilink_queda_partido_por_un_salto_de_linea():
    """Un wikilink con un salto de linea dentro no lo reconoce el parser: se
    publica crudo, con los corchetes a la vista, y `raya validate` no lo ve
    porque para el no es un enlace. Paso exactamente eso en las paginas de los
    modulos 3 y 4 de filosofia, y se descubrio mirando el sitio ya desplegado.

    Solo mira el cuerpo, no el frontmatter: `prerequisites` y `aliases` son
    listas YAML y no llevan wikilinks.
    """
    partidos = []
    for ruta in sorted((RAIZ / "course").rglob("*.md")):
        if "_assets" in ruta.parts:
            continue
        texto = ruta.read_text(encoding="utf-8")
        for match in re.finditer(r"\[\[[^\]]*\n[^\]]*\]\]", texto):
            linea = texto[: match.start()].count("\n") + 1
            crudo = " ".join(match.group(0).split())
            partidos.append(f"{ruta.relative_to(RAIZ)}:{linea}: {crudo}")
    assert not partidos, (
        "wikilinks partidos por un salto de linea (se publican crudos):\n"
        + "\n".join(partidos)
    )


def test_extra_ningun_encabezado_lleva_un_enlace_dentro():
    """El indice «On This Page» toma el texto crudo del encabezado: un enlace
    dentro de un H2/H3 se imprime ahi con su sintaxis Markdown a la vista
    («[Modulo 1](raya:accelerate-what) — ¿acelerar que?») y ensucia el ancla.
    Paso al reescribir el recorrido de la unidad de filosofia con los modulos
    como encabezados enlazados; se vio en el sitio desplegado, no en local.
    """
    con_enlace = []
    for ruta in sorted((RAIZ / "course").rglob("*.md")):
        if "_assets" in ruta.parts:
            continue
        for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            if not linea.startswith("#"):
                continue
            if re.search(r"\[\[.+?\]\]|\]\(", linea):
                con_enlace.append(f"{ruta.relative_to(RAIZ)}:{numero}: {linea.strip()}")
    assert not con_enlace, (
        "encabezados con un enlace dentro (el indice de la pagina los imprime "
        "en crudo):\n" + "\n".join(con_enlace)
    )


def test_extra_ningun_wikilink_va_sin_etiqueta():
    """Raya rotula un `[[id]]` sin etiqueta con el id crudo, no con el titulo
    de la pagina: en la prosa se leia «En ia-y-sociedad aparecieron como una
    posicion del mapa». No es un enlace roto —resuelve bien— asi que
    `raya validate` lo da por bueno; se vio mirando el sitio desplegado.
    """
    desnudos = []
    for ruta in sorted((RAIZ / "course").rglob("*.md")):
        if "_assets" in ruta.parts:
            continue
        texto = ruta.read_text(encoding="utf-8")
        for match in re.finditer(r"\[\[([^\]|\n]+)\]\]", texto):
            linea = texto[: match.start()].count("\n") + 1
            desnudos.append(f"{ruta.relative_to(RAIZ)}:{linea}: {match.group(0)}")
    assert not desnudos, (
        "wikilinks sin etiqueta (se publican mostrando el id crudo):\n"
        + "\n".join(desnudos)
    )
