"""Guardas de las paginas de repaso del modulo 1 de filosofia.

Las tres paginas llevan citas textuales de seis ensayos, y afirmaciones sobre
personas vivas, a un salon de clases. El riesgo concreto no es un error de
dedo: es una cita plausible que nadie copio de ningun lado. Por eso cada cita
de cada pagina tiene que aparecer, literal, en el registro de verificacion de
esa pagina, y cada fila de cada registro tiene que estar marcada como
verificada.

El repaso empezo siendo una sola pagina y se partio en tres. Al partirlo, dos
de las citas se mudaron a 2_las_ideas.md y la cobertura de esta guarda se
quedo apuntando solo a 3_las_seis_lecturas.md. De ahi que las tres paginas
esten aqui parametrizadas con su cifra esperada de citas: si una cita se muda
otra vez, el conteo falla en las dos paginas y hay que decidir a mano, en vez
de perder la cobertura en silencio.
"""
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent

# (pagina, registro, citas esperadas). 4_para_discutir.md no cita textualmente
# —discute las seis lecturas ya citadas en las otras dos— y su registro lo
# dice en vez de traer tabla; TABLA lo marca.
PAGINAS = [
    ("2_las_ideas.md", 2, True),
    ("3_las_seis_lecturas.md", 6, True),
    ("4_para_discutir.md", 0, False),
]

# Frase con la que el registro sin tabla declara que no la necesita. Si alguien
# le agrega citas a esa pagina y borra la frase, la guarda de abajo lo exige.
SIN_TABLA = "no hay, por tanto, una tabla de verificación propia"

# Formato fijado por el diseno: cada cita es una linea de blockquote que abre
# con comillas angulares y cierra con la pagina del cuadernillo.
RE_CITA = re.compile(r"^> «(.+?)» — cuadernillo, p\. \d+\s*$", re.MULTILINE)

# Separador de celdas de una tabla Markdown: barra sin escapar.
RE_CELDA = re.compile(r"(?<!\\)\|")


def _pagina(nombre: str) -> Path:
    return RAIZ / "course/2_filosofia_ia" / nombre


def _registro(nombre: str) -> Path:
    return RAIZ / "docs/verificacion/filosofia_ia" / nombre


@pytest.mark.parametrize("nombre,esperadas,tabla", PAGINAS)
def test_el_registro_de_verificacion_existe(nombre, esperadas, tabla):
    registro = _registro(nombre)
    assert registro.is_file(), f"falta {registro.relative_to(RAIZ)}"


@pytest.mark.parametrize("nombre,esperadas,tabla", PAGINAS)
def test_toda_cita_de_la_pagina_esta_en_el_registro(nombre, esperadas, tabla):
    texto = _pagina(nombre).read_text(encoding="utf-8")
    registro = _registro(nombre).read_text(encoding="utf-8")
    citas = RE_CITA.findall(texto)
    # Guarda explicita de conteo: sin esto, un cambio de puntuacion en una cita
    # (o una lectura nueva con formato ligeramente distinto) hace que
    # RE_CITA.findall devuelva menos citas -- o cero -- y el for de abajo pasa
    # vacio, sin fallar. Si un dia una cita se muda de pagina, esta linea
    # obliga a actualizar PAGINAS a mano en vez de dejar que la cobertura baje.
    assert len(citas) == esperadas, (
        f"{nombre}: se esperaban {esperadas} citas con el formato de RE_CITA, "
        f"se encontraron {len(citas)}: revisa si RE_CITA todavia calza con el "
        "formato de las citas de la pagina, o si una cita cambio de pagina"
    )
    for cita in citas:
        assert cita in registro, (
            f"{nombre}: cita sin fila en el registro de verificacion: "
            f"{cita[:60]!r}"
        )


@pytest.mark.parametrize("nombre,esperadas,tabla", PAGINAS)
def test_ninguna_cita_quedo_con_el_marcador_de_plantilla(nombre, esperadas, tabla):
    texto = _pagina(nombre).read_text(encoding="utf-8")
    assert "<cita literal>" not in texto, (
        f"{nombre}: quedo el marcador de plantilla de una cita sin llenar"
    )


@pytest.mark.parametrize("nombre,esperadas,tabla", PAGINAS)
def test_toda_fila_del_registro_esta_verificada(nombre, esperadas, tabla):
    """Fila por fila, no una busqueda de 'si' en todo el archivo: ese agujero
    de substring-contra-todo-el-archivo ya se cerro dos veces en las guardas
    de la unidad de historia."""
    crudo = _registro(nombre).read_text(encoding="utf-8")
    lineas = [l for l in crudo.splitlines() if l.strip().startswith("|")]
    encabezado, filas = None, []
    for linea in lineas:
        # Split por barra NO escapada: las celdas de 2_las_ideas.md citan
        # tuberias de shell (`pdftotext … \| grep …`), y partir por "|" a secas
        # mete una celda de mas y corre la columna 'Verificado' de sitio.
        celdas = [c.strip() for c in RE_CELDA.split(linea.strip().strip("|"))]
        if encabezado is None:
            encabezado = celdas
            continue
        if all(set(c) <= {"-", " ", ":"} for c in celdas):
            continue
        filas.append(celdas)
    if not tabla:
        assert not filas, (
            f"{nombre}: el registro trae tabla y PAGINAS dice que no; "
            "actualiza PAGINAS"
        )
        assert SIN_TABLA in " ".join(crudo.lower().split()), (
            f"{nombre}: el registro no tiene tabla ni dice por que no la tiene"
        )
        return
    assert encabezado and filas, f"{nombre}: el registro no tiene tabla de verificacion"
    assert "Verificado" in encabezado, f"{nombre}: el registro no tiene columna 'Verificado'"
    columna = encabezado.index("Verificado")
    for fila in filas:
        assert fila[columna].strip().lower().startswith(("sí", "si")), (
            f"{nombre}: fila sin verificar: {fila}"
        )
