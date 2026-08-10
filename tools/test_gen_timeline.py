import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
TRAMOS = ["mitos", "inteligencia", "arco-1", "arco-2", "boom", "actual",
          "raices", "sociedad"]


def _cargar_gen_timeline():
    """Carga tools/gen_timeline.py como modulo para probar sus funciones directamente."""
    spec = importlib.util.spec_from_file_location(
        "gen_timeline", RAIZ / "tools/gen_timeline.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    """Regenera los SVG una vez por modulo para que ninguna prueba lea archivos
    obsoletos si se corre con -k contra un solo test."""
    subprocess.run([sys.executable, str(RAIZ / "tools/gen_timeline.py")], check=True)


def test_genera_todos_los_svg():
    assert (ASSETS / "v1-panorama.svg").is_file(), "falta el panorama"
    for slug in TRAMOS:
        assert (ASSETS / f"v1-tramo-{slug}.svg").is_file(), f"falta el tramo {slug}"


def test_svg_cumple_convenciones():
    for svg in [ASSETS / "v1-panorama.svg"] + [
        ASSETS / f"v1-tramo-{s}.svg" for s in TRAMOS
    ]:
        texto = svg.read_text(encoding="utf-8")
        raiz = texto.split(">")[0]
        assert 'viewBox="' in texto, f"{svg.name} sin viewBox"
        # El sitio incrusta estos SVG con <img src="...svg">, y el CSS del
        # skin solo trae "max-width: 100%; height: auto" (sin "width"). Un
        # <svg> sin width/height propios (solo viewBox) no tiene tamano
        # intrinseco: el navegador cae al tamano por omision de un elemento
        # reemplazado (~300x150 CSS px) en vez de llenar el contenedor de la
        # figura, y el diagrama se ve minusculo e ilegible. Verificado
        # visualmente con Chrome sin interfaz contra el sitio construido
        # (Tarea 18) -- width/height deben estar presentes, no ausentes.
        assert "width=" in raiz, f"{svg.name} sin width en la raiz: se vera minusculo en el sitio"
        assert "height=" in raiz, f"{svg.name} sin height en la raiz: se vera minusculo en el sitio"
        assert 'fill="#211033"' in texto, f"{svg.name} sin fondo legible en impresion"
        assert 'role="img"' in texto and "aria-label=" in texto


def test_envolver_no_trunca_ninguna_etiqueta():
    """hitos.json es la unica fuente de verdad y crecera con las siguientes 9
    tareas; envolver() descarta en silencio las palabras que no caben en dos
    lineas, asi que cualquier etiqueta larga debe fallar aqui, no en el SVG."""
    gen_timeline = _cargar_gen_timeline()
    datos = json.loads((RAIZ / "tools/hitos.json").read_text(encoding="utf-8"))
    for h in datos["hitos"]:
        original = " ".join(h["etiqueta"].split())
        envuelto = " ".join(" ".join(gen_timeline.envolver(h["etiqueta"])).split())
        assert envuelto == original, f"envolver() trunco la etiqueta: {h['etiqueta']!r}"


def test_hitos_tienen_forma_valida():
    datos = json.loads((RAIZ / "tools/hitos.json").read_text(encoding="utf-8"))
    assert len(datos["hitos"]) >= 40
    for h in datos["hitos"]:
        assert set(h) >= {"anio", "etiqueta", "tramo"}
        assert isinstance(h["anio"], int)
        assert h["tramo"] in TRAMOS, f"tramo desconocido: {h['tramo']}"
    for banda in datos["bandas"]:
        assert banda["tipo"] in {"verano", "invierno"}
        assert banda["desde"] < banda["hasta"]


def test_cada_tramo_tiene_hitos():
    datos = json.loads((RAIZ / "tools/hitos.json").read_text(encoding="utf-8"))
    for slug in TRAMOS:
        assert [h for h in datos["hitos"] if h["tramo"] == slug], f"tramo vacio: {slug}"
    assert len([h for h in datos["hitos"] if h.get("ancla")]) >= 5, "faltan anclas"


def test_ningun_tramo_repite_anio():
    """Dos hitos del mismo tramo y del mismo anio caerian en la misma x."""
    datos = json.loads((RAIZ / "tools/hitos.json").read_text(encoding="utf-8"))
    for slug in TRAMOS:
        anios = [h["anio"] for h in datos["hitos"] if h["tramo"] == slug]
        assert len(anios) == len(set(anios)), f"anios repetidos en el tramo {slug}"
