import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
SVG = ASSETS / "v9-computo.svg"


def _cargar_gen_computo():
    """Carga tools/gen_computo.py como modulo para probar sus funciones directamente."""
    spec = importlib.util.spec_from_file_location(
        "gen_computo", RAIZ / "tools/gen_computo.py"
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module", autouse=True)
def _svg_fresco():
    """Regenera el SVG una vez por modulo para que ninguna prueba lea un
    archivo obsoleto si se corre con -k contra un solo test."""
    subprocess.run([sys.executable, str(RAIZ / "tools/gen_computo.py")], check=True)


def test_svg_cumple_convenciones():
    texto = SVG.read_text(encoding="utf-8")
    raiz = texto.split(">")[0]
    assert 'viewBox="' in texto, f"{SVG.name} sin viewBox"
    # Mismo hallazgo que gen_timeline.py (Tarea 18): sin width/height propios
    # en la raiz <svg>, el navegador incrusta el <img> a su tamano por
    # omision (~300x150 CSS px) en vez de llenar el contenedor de la figura.
    assert "width=" in raiz, f"{SVG.name} sin width en la raiz: se vera minusculo en el sitio"
    assert "height=" in raiz, f"{SVG.name} sin height en la raiz: se vera minusculo en el sitio"
    assert 'fill="#211033"' in texto, f"{SVG.name} sin fondo legible"
    assert 'role="img"' in texto and "aria-label=" in texto


def test_svg_referencia_las_cifras_de_computo_json():
    """v9-computo.svg estaba escrito a mano con las mismas seis cifras que
    trae computo.json, sin que ningun script las conectara (H12). Esta
    prueba falla si el SVG y el JSON divergen en modelo, anio o cifra."""
    datos = json.loads((RAIZ / "tools/computo.json").read_text(encoding="utf-8"))
    texto = SVG.read_text(encoding="utf-8")
    for modelo in datos["modelos"]:
        assert modelo["modelo"] in texto, f"{modelo['modelo']} no aparece en el SVG"
        assert modelo["flop_texto"] in texto, f"FLOP de {modelo['modelo']} no aparece en el SVG"
        assert str(modelo["anio"]) in texto, f"anio de {modelo['modelo']} no aparece en el SVG"


def test_regenerar_no_cambia_el_svg_comiteado():
    """Si esto falla, alguien edito v9-computo.svg a mano o cambio
    tools/computo.json sin correr `python3 tools/gen_computo.py`: el archivo
    comiteado y el que produce el generador ya no coinciden, y CREDITOS.md
    vuelve a mentir sobre la procedencia del diagrama."""
    modulo = _cargar_gen_computo()
    datos = json.loads((RAIZ / "tools/computo.json").read_text(encoding="utf-8"))
    esperado = modulo.dibuja(
        datos["modelos"], "El computo de entrenamiento crece exponencialmente",
        datos["fuente"], datos["consultado"],
    )
    assert SVG.read_text(encoding="utf-8") == esperado, (
        "v9-computo.svg no coincide con la salida de gen_computo.py: "
        "corre 'python3 tools/gen_computo.py' y comitea el resultado"
    )


def _elemento_de_texto(texto, contenido):
    """Devuelve (x, y, anchor) del <text> cuyo contenido es exactamente
    `contenido`."""
    patron = re.escape(contenido)
    m = re.search(
        rf'<text x="([-\d.]+)" y="([-\d.]+)"[^>]*text-anchor="(middle|start|end)">{patron}</text>',
        texto,
    )
    assert m, f"no se encontro <text> con contenido {contenido!r}"
    x, y, anchor = m.groups()
    return float(x), float(y), anchor


def _bbox(x, y0, y1, ancho, anchor):
    if anchor == "middle":
        x0, x1 = x - ancho / 2, x + ancho / 2
    elif anchor == "end":
        x0, x1 = x - ancho, x
    else:
        x0, x1 = x, x + ancho
    return (x0, x1, y0, y1)


def _caja_por_modelo(texto, modelo):
    """Caja delimitadora combinada del nombre y el valor FLOP de un modelo
    (dos lineas de la misma etiqueta, que si se traslapan entre si es
    intencional -- estan apiladas a proposito)."""
    nx, ny, na = _elemento_de_texto(texto, modelo["modelo"])
    contenido_valor = f'{modelo["flop_texto"]} FLOP'
    vx, vy, va = _elemento_de_texto(texto, contenido_valor)
    ancho_nombre = len(modelo["modelo"]) * 7.2
    ancho_valor = len(contenido_valor) * 6.2
    n0, n1, _, _ = _bbox(nx, 0, 0, ancho_nombre, na)
    v0, v1, _, _ = _bbox(vx, 0, 0, ancho_valor, va)
    x0, x1 = min(n0, v0), max(n1, v1)
    y0, y1 = min(ny, vy) - 13, max(ny, vy) + 4
    return (x0, x1, y0, y1)


def test_ninguna_etiqueta_de_modelo_se_encima_con_otra():
    """Con text-anchor='middle' fijo para todos los puntos, PaLM 540B y
    GPT-4 se dibujaban encimados en el sitio real (verificado visualmente
    con Chrome sin interfaz, 2026-08-10) porque sus circulos caen a solo 66px
    de distancia en x. gen_computo.py separa las etiquetas que colisionan;
    esta prueba aproxima el bloque de texto (nombre + valor) de cada modelo
    y falla si dos bloques de MODELOS DISTINTOS se traslapan en pantalla."""
    datos = json.loads((RAIZ / "tools/computo.json").read_text(encoding="utf-8"))
    texto = SVG.read_text(encoding="utf-8")
    cajas = [(m["modelo"], _caja_por_modelo(texto, m)) for m in datos["modelos"]]
    for i, (nombre_a, a) in enumerate(cajas):
        for nombre_b, b in cajas[i + 1:]:
            solapa_x = a[0] < b[1] and b[0] < a[1]
            solapa_y = a[2] < b[3] and b[2] < a[3]
            assert not (solapa_x and solapa_y), (
                f"etiquetas encimadas: {nombre_a!r} y {nombre_b!r}"
            )
