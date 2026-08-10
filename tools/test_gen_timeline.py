import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
TRAMOS = ["mitos", "inteligencia", "arco-1", "arco-2", "boom", "actual",
          "raices", "sociedad"]


def test_genera_todos_los_svg():
    subprocess.run([sys.executable, str(RAIZ / "tools/gen_timeline.py")], check=True)
    assert (ASSETS / "v1-panorama.svg").is_file(), "falta el panorama"
    for slug in TRAMOS:
        assert (ASSETS / f"v1-tramo-{slug}.svg").is_file(), f"falta el tramo {slug}"


def test_svg_cumple_convenciones():
    for svg in [ASSETS / "v1-panorama.svg"] + [
        ASSETS / f"v1-tramo-{s}.svg" for s in TRAMOS
    ]:
        texto = svg.read_text(encoding="utf-8")
        assert 'viewBox="' in texto, f"{svg.name} sin viewBox"
        assert "width=" not in texto.split(">")[0], f"{svg.name} fija width en la raiz"
        assert 'fill="#211033"' in texto, f"{svg.name} sin fondo legible en impresion"
        assert 'role="img"' in texto and "aria-label=" in texto


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
