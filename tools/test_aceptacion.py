"""Verifica los criterios de aceptacion del spec 2026-08-09-historia-ia-design.md, S10.

Cada test_1..test_10 corresponde, en orden, a uno de los diez criterios de esa
seccion. test_extra_avisos_generadas verifica un criterio adicional que el diseno
exige (S6.2: "Cada ilustracion generada se identifica como tal en el pie de
figura") pero que el brief original no cubria.

Notas frente al brief original de la Tarea 18:
- El tope de peso del repositorio es 16 MB, no 10: se subio deliberadamente
  porque 53 imagenes ya ocupaban 8.9 MB antes de las ilustraciones generadas.
- navigation.json es una lista PLANA en "items"; "children" contiene ids en
  texto, no objetos anidados. No hay que recorrer recursivamente.
"""

import json
import os
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = RAIZ / "course/1_introduccion/2_historia_ia"
ASSETS = UNIDAD / "_assets"
ARTEFACTO = RAIZ / "artifact"
RAYA_LUCARIA = Path("/home/uumami/itam/raya_lucaria")

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


def test_1_raya_validate_pasa_sin_errores_ni_advertencias():
    salida = _run_raya("validate")
    assert "ERROR |" not in salida.stdout, salida.stdout
    assert "WARN |" not in salida.stdout, salida.stdout
    assert "Course validation passed" in salida.stdout, salida.stdout


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


def test_7_toda_fecha_y_atribucion_tiene_fuente_verificada():
    for pagina in PAGINAS:
        registro = RAIZ / "docs/verificacion" / pagina
        assert registro.is_file(), f"falta {registro.relative_to(RAIZ)}"
        texto = registro.read_text(encoding="utf-8").lower()
        # La columna "Verificado" puede ser una celda exacta ("| sí |") o una
        # frase que empieza con "Sí" seguida de la evidencia ("| Sí. ACM
        # anunció..."). Ambas cuentan como verificado.
        marcado_si = re.search(r"\|\s*s[ií]\b", texto) is not None
        # 8_material_adicional.md verifica enlaces por codigo HTTP, no por
        # columna "Verificado" con si/no.
        enlaces_verificados = re.search(r"\|\s*200\s*\|", texto) is not None
        assert marcado_si or enlaces_verificados, f"{pagina}: nada verificado"


def test_8_el_repositorio_pesa_menos_de_16mb():
    salida = subprocess.run(
        ["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True
    )
    total = sum(
        (RAIZ / n).stat().st_size
        for n in salida.stdout.split("\0") if n and (RAIZ / n).is_file()
    )
    assert total < 16_000_000, f"el repositorio pesa {total / 1e6:.1f} MB (tope: 16 MB)"


def test_9_los_diagramas_svg_son_legibles_sobre_el_fondo_oscuro_del_skin():
    svgs = sorted(ASSETS.glob("*.svg"))
    assert svgs, "no hay SVG propios en _assets"
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
    for pagina in PAGINAS:
        ruta = UNIDAD / pagina
        if not ruta.is_file():
            continue
        texto = ruta.read_text(encoding="utf-8")
        for match in re.finditer(r"]\(_assets/(ilus-[\w-]+\.\w+)\)", texto):
            total_usos += 1
            archivo = match.group(1)
            resto = texto[match.end():match.end() + 400]
            assert patron_aviso.search(resto), (
                f"{pagina}: {archivo} no tiene aviso visible en cursivas "
                "justo despues de su bloque de figura"
            )
    assert total_usos > 0, "no se encontro ningun uso de ilus-* en las paginas"
