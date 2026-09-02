"""Guardas del generador de diagramas de agentes y ambientes."""

import importlib.util
import re
import subprocess
import sys
import xml.dom.minidom
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/5_agentes_ambientes/_assets"


def cargar():
    spec = importlib.util.spec_from_file_location(
        "gen_agentes_ambientes", RAIZ / "tools/gen_agentes_ambientes.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module", autouse=True)
def svgs_frescos():
    subprocess.run([sys.executable, str(RAIZ / "tools/gen_agentes_ambientes.py")], check=True)


def test_catalogo_de_siete_diagramas_con_prefijo_aa():
    modulo = cargar()
    assert len(modulo.DIAGRAMAS) == 7
    assert all(nombre.startswith("aa-") for nombre in modulo.DIAGRAMAS)
    for nombre in modulo.DIAGRAMAS:
        assert (ASSETS / f"{nombre}.svg").is_file(), f"falta {nombre}.svg"


def test_raices_y_xml_de_los_diagramas():
    modulo = cargar()
    for nombre in modulo.DIAGRAMAS:
        ruta = ASSETS / f"{nombre}.svg"
        texto = ruta.read_text(encoding="utf-8")
        raiz = re.match(r"<svg\b[^>]*>", texto)
        assert raiz, f"{ruta.name}: falta raiz svg"
        etiqueta = raiz.group()
        for atributo in ('width="', 'height="', 'viewBox="', 'role="img"', 'aria-label="'):
            assert atributo in etiqueta, f"{ruta.name}: falta {atributo}"
        assert "<title>" in texto and "<desc>" in texto
        assert f'fill="{modulo.FONDO}"' in texto
        xml.dom.minidom.parse(str(ruta))


def test_catalogo_y_creditos_no_dejan_diagramas_huerfanos():
    modulo = cargar()
    declarados = {f"{nombre}.svg" for nombre in modulo.DIAGRAMAS}
    presentes = {ruta.name for ruta in ASSETS.glob("aa-*.svg")}
    assert presentes == declarados
    creditos = (ASSETS / "CREDITOS.md").read_text(encoding="utf-8")
    for nombre in modulo.DIAGRAMAS:
        assert f"{nombre}.svg" in creditos
