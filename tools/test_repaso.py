"""Guardas de la pagina de repaso del modulo 1 de filosofia.

La pagina lleva citas textuales de seis ensayos a un salon de clases. El riesgo
concreto no es un error de dedo: es una cita plausible que nadie copio de
ningun lado. Por eso cada cita de la pagina tiene que aparecer, literal, en el
registro de verificacion, y cada fila de ese registro tiene que estar marcada
como verificada.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "course/2_filosofia_ia/2_repaso_y_discusion.md"
REGISTRO = RAIZ / "docs/verificacion/filosofia_ia/2_repaso_y_discusion.md"

# Formato fijado por el diseno: cada cita es una linea de blockquote que abre
# con comillas angulares y cierra con la pagina del cuadernillo.
RE_CITA = re.compile(r"^> «(.+?)» — cuadernillo, p\. \d+\s*$", re.MULTILINE)


def test_el_registro_de_verificacion_existe():
    assert REGISTRO.is_file(), f"falta {REGISTRO.relative_to(RAIZ)}"


def test_toda_cita_de_la_pagina_esta_en_el_registro():
    texto = PAGINA.read_text(encoding="utf-8")
    registro = REGISTRO.read_text(encoding="utf-8")
    citas = RE_CITA.findall(texto)
    # Guarda explicita de conteo: sin esto, un cambio de puntuacion en una cita
    # (o una lectura nueva con formato ligeramente distinto) hace que
    # RE_CITA.findall devuelva menos citas -- o cero -- y el for de abajo pasa
    # vacio, sin fallar. Seis lecturas, seis citas; si un dia hay una septima,
    # esta linea obliga a actualizarla a mano en vez de dejar que la cobertura
    # baje en silencio.
    assert len(citas) == 6, (
        f"se esperaban 6 citas con el formato de RE_CITA, se encontraron "
        f"{len(citas)}: revisa si RE_CITA todavia calza con el formato de las "
        "citas de la pagina"
    )
    for cita in citas:
        assert cita in registro, (
            f"cita sin fila en el registro de verificacion: {cita[:60]!r}"
        )


def test_ninguna_cita_quedo_con_el_marcador_de_plantilla():
    texto = PAGINA.read_text(encoding="utf-8")
    assert "<cita literal>" not in texto, (
        "quedo el marcador de plantilla de una cita sin llenar"
    )


def test_toda_fila_del_registro_esta_verificada():
    """Fila por fila, no una busqueda de 'si' en todo el archivo: ese agujero
    de substring-contra-todo-el-archivo ya se cerro dos veces en las guardas
    de la unidad de historia."""
    lineas = [l for l in REGISTRO.read_text(encoding="utf-8").splitlines()
              if l.strip().startswith("|")]
    encabezado, filas = None, []
    for linea in lineas:
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if encabezado is None:
            encabezado = celdas
            continue
        if all(set(c) <= {"-", " ", ":"} for c in celdas):
            continue
        filas.append(celdas)
    assert encabezado and filas, "el registro no tiene tabla de verificacion"
    assert "Verificado" in encabezado, "el registro no tiene columna 'Verificado'"
    columna = encabezado.index("Verificado")
    for fila in filas:
        assert fila[columna].strip().lower().startswith(("sí", "si")), (
            f"fila sin verificar: {fila}"
        )
