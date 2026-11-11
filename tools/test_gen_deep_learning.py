"""Guardas del generador de diagramas de la unidad 10 (aprendizaje profundo).

Patron de test_gen_complejidad.py: el fixture regenera antes de leer, asi que
un SVG editado a mano se sobrescribe en silencio; lo que ata el archivo
comiteado a su generador es que `git status` quede limpio tras correrlo.

De la unidad 9 se toman el tope de 600 px de ancho y la letra minima de 12 px.
Y como dl-curvas-rmse dibuja datos, se coteja cada punto de sus curvas y su
marca de minimo contra redes.entrenar_ejemplo(): cambiar el entrenamiento sin
regenerar la figura, o la geometria sin los datos, falla aqui.
"""
import importlib.util
import re
import subprocess
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
TOOLS = RAIZ / "tools"
ASSETS = RAIZ / "course/10_deep_learning/_assets"
NS = "{http://www.w3.org/2000/svg}"

# Ids fijados por el plan de la unidad: las paginas los citan en `::: figure`.
IDS_DEL_PLAN = {
    "dl-red-2-3-2-1", "dl-peso-wij", "dl-matriz-w", "dl-composicion",
    "dl-retropropagacion", "dl-ciclo", "dl-curvas-rmse",
}


def _cargar():
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location(
        "gen_deep_learning", TOOLS / "gen_deep_learning.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


GEN = _cargar()
NOMBRES = sorted(GEN.DIAGRAMAS)


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    subprocess.run([sys.executable, str(TOOLS / "gen_deep_learning.py")],
                   check=True, capture_output=True)


def _leer(nombre):
    return (ASSETS / f"{nombre}.svg").read_text(encoding="utf-8")


def _raiz(texto):
    return re.match(r"<svg\b[^>]*>", texto).group()


# ------------------------------------------------------------ catalogo ---

def test_el_catalogo_es_el_del_plan():
    assert set(GEN.DIAGRAMAS) == IDS_DEL_PLAN


def test_todos_los_diagramas_declarados_existen():
    for nombre in NOMBRES:
        assert nombre.startswith("dl-"), (
            f"{nombre}: los ids de objeto numerado son unicos en TODO el curso; "
            "sin el prefijo 'dl-' pueden chocar con otra unidad")
        assert (ASSETS / f"{nombre}.svg").is_file(), f"falta {nombre}.svg"


def test_ningun_svg_quedo_huerfano_en_assets():
    presentes = {p.name for p in ASSETS.glob("*.svg")}
    huerfanos = sorted(presentes - {f"{n}.svg" for n in NOMBRES})
    assert not huerfanos, (
        f"SVG en _assets que el generador ya no produce: {huerfanos}. "
        "Borralos, o devuelveles su entrada en DIAGRAMAS.")


def test_cada_svg_tiene_fila_en_creditos_con_origen_y_licencia():
    from unidades import CELDA_LICENCIA, CELDA_ORIGEN, filas_de_creditos
    filas = filas_de_creditos(ASSETS)
    for nombre in NOMBRES:
        fila = filas.get(f"{nombre}.svg")
        assert fila, f"{nombre}.svg no tiene fila en CREDITOS.md"
        assert fila[CELDA_ORIGEN] and fila[CELDA_LICENCIA], (
            f"{nombre}.svg: origen o licencia vacios en CREDITOS.md")
        assert "cc by" in fila[CELDA_LICENCIA].lower(), fila[CELDA_LICENCIA]


# ------------------------------------------------- convenciones del SVG ---

@pytest.mark.parametrize("nombre", NOMBRES)
def test_la_raiz_cumple_las_convenciones(nombre):
    texto = _leer(nombre)
    assert texto.startswith("<svg"), f"{nombre}: no empieza con <svg"
    etiqueta = _raiz(texto)
    assert re.search(r'\bwidth="\d', etiqueta), f"{nombre}: <svg> sin width"
    assert re.search(r'\bheight="\d', etiqueta), f"{nombre}: <svg> sin height"
    assert 'viewBox="' in etiqueta, f"{nombre}: sin viewBox"
    assert 'role="img"' in etiqueta, f"{nombre}: sin role=img"
    assert re.search(r'aria-label="[^"]{40,}"', etiqueta), (
        f"{nombre}: aria-label vacio o demasiado corto para describir la figura")
    assert f'fill="{GEN.FONDO}"' in texto, f"{nombre}: sin el fondo {GEN.FONDO}"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_es_xml_bien_formado_y_trae_titulo(nombre):
    try:
        xml.dom.minidom.parseString(_leer(nombre).encode("utf-8"))
    except Exception as error:  # noqa: BLE001 - se re-lanza como fallo legible
        raise AssertionError(f"{nombre} no es XML bien formado: {error}") from error
    raiz = ET.fromstring(_leer(nombre))
    titulo = raiz.find(f"{NS}title")
    assert titulo is not None and titulo.text.strip(), f"{nombre}: sin <title>"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_mide_a_lo_mas_600_y_cuadra_con_su_viewbox(nombre):
    etiqueta = _raiz(_leer(nombre))
    ancho = float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1))
    alto = float(re.search(r'\bheight="([\d.]+)"', etiqueta).group(1))
    _, _, vw, vh = (float(v) for v in
                    re.search(r'viewBox="([^"]+)"', etiqueta).group(1).split())
    assert ancho <= GEN.ANCHO_MAX, f"{nombre}: {ancho} px de ancho"
    assert abs(ancho / alto - vw / vh) < 0.01, f"{nombre}: proporcion distinta"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_la_letra_es_de_12_px_o_mas(nombre):
    tams = [float(t) for t in re.findall(r'font-size="([\d.]+)"', _leer(nombre))]
    assert tams, f"{nombre}: sin texto"
    assert min(tams) >= GEN.LETRA_MIN, f"{nombre}: letra de {min(tams)} px"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ningun_diagrama_usa_opacidad(nombre):
    """El sombreado de cx-o-grande se publico con fill-opacity y tapo dos
    curvas fuera del navegador; aqui todo color translucido se hornea con
    mezclar()."""
    assert "opacity" not in _leer(nombre), (
        f"{nombre}.svg usa opacidad: usa mezclar(color, fraccion)")


def _luminancia(color):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


def _contraste(a, b):
    la, lb = sorted((_luminancia(a), _luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_todo_texto_contrasta_4_5_contra_el_fondo(nombre):
    raiz = ET.fromstring(_leer(nombre))
    colores = set()
    for el in raiz.iter():
        if el.tag in (f"{NS}text", f"{NS}tspan") and el.get("fill"):
            colores.add(el.get("fill"))
    assert colores, f"{nombre}: sin texto"
    for color in colores:
        assert _contraste(color, GEN.FONDO) >= 4.5, (
            f"{nombre}: texto {color} a {_contraste(color, GEN.FONDO):.2f}:1 "
            f"contra {GEN.FONDO}")


@pytest.mark.parametrize("nombre", NOMBRES)
def test_toda_flecha_apunta_a_un_marcador_definido(nombre):
    texto = _leer(nombre)
    definidos = set(re.findall(r'<marker id="([^"]+)"', texto))
    usados = set(re.findall(r'marker-end="url\(#([^)]+)\)"', texto))
    assert usados <= definidos, f"{nombre}: marcadores sin definir {usados - definidos}"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_el_generador_es_determinista(nombre):
    if nombre == "dl-curvas-rmse":
        pytest.skip("entrena dos redes: lo cubre el cotejo de curvas")
    assert GEN.DIAGRAMAS[nombre]() == _leer(nombre)


def test_la_notacion_del_plan_aparece_en_las_figuras():
    """Los simbolos que el plan fija, escritos con Unicode, en la figura
    donde se introducen (un renombre del plan obliga a regenerar)."""
    esperado = {
        "dl-red-2-3-2-1": ["₁₁⁽¹⁾", "₃₂⁽¹⁾", "d</tspan>₀", "ŷ"],
        "dl-peso-wij": ["ᵢⱼ⁽ˡ⁾", "ⱼ⁽ˡ⁻¹⁾", "ᵢ⁽ˡ⁾", "destino", "origen"],
        "dl-matriz-w": ["destino", "origen", "₃₂⁽¹⁾", "ℝ³ˣ²"],
        "dl-composicion": ["f\u200a</tspan>⁽¹⁾", "ŷ", "ℓ", "θ"],
        "dl-retropropagacion": ["δ</tspan>⁽³⁾", "⁽³⁾ᵀ", "⊙", "′", "∇"],
        "dl-ciclo": ["η", "μ", "ℒ", "θ"],
        "dl-curvas-rmse": ["μ", "RMSE", "época"],
    }
    for nombre, piezas in esperado.items():
        texto = _leer(nombre)
        for pieza in piezas:
            assert pieza in texto, f"{nombre}: falta {pieza!r}"


# ----------------------------------------------- curvas contra redes.py ---

def _puntos(d):
    nums = [float(v) for v in re.findall(r"-?[\d.]+", d)]
    return list(zip(nums[0::2], nums[1::2]))


@pytest.fixture(scope="module")
def historias():
    import redes
    return redes, {"sin-mu": redes.entrenar_ejemplo(0.0),
                   "con-mu": redes.entrenar_ejemplo(redes.MU_ENTRENAMIENTO)}


@pytest.mark.parametrize("panel", ["sin-mu", "con-mu"])
@pytest.mark.parametrize("serie", ["entrenamiento", "validacion"])
def test_las_curvas_son_las_de_entrenar_ejemplo(historias, panel, serie):
    redes, hist = historias
    raiz = ET.fromstring(_leer("dl-curvas-rmse"))
    camino = raiz.find(f".//{NS}path[@id='dl-curva-{panel}-{serie}']")
    assert camino is not None, f"falta la curva {panel}-{serie}"
    g = GEN.CURVAS
    arriba, abajo = g["paneles"][panel]
    valores = hist[panel][f"rmse_{serie}"]
    puntos = _puntos(camino.get("d"))
    epocas = [round((x - g["x0"]) / (g["x1"] - g["x0"]) * redes.EPOCAS)
              for x, _ in puntos]
    assert epocas == list(range(1, redes.EPOCAS + 1)), (
        "la curva debe tener un punto por epoca, de la 1 a la ultima")
    leidos = [g["y_min"] + (abajo - y) / (abajo - arriba) * (g["y_max"] - g["y_min"])
              for _, y in puntos]
    error = np.max(np.abs(np.array(leidos) - np.array(valores[1:])))
    # 0.05 px de redondeo en un panel de 176 px son ~1.5e-4 de RMSE
    assert error < 5e-4, f"{panel}-{serie}: la curva se aparta {error:.4f}"


@pytest.mark.parametrize("panel", ["sin-mu", "con-mu"])
def test_el_minimo_marcado_es_el_de_la_validacion(historias, panel):
    redes, hist = historias
    val = np.array(hist[panel]["rmse_validacion"])
    raiz = ET.fromstring(_leer("dl-curvas-rmse"))
    marca = raiz.find(f".//{NS}circle[@id='dl-minimo-{panel}']")
    assert marca is not None, f"falta la marca del minimo en {panel}"
    k = int(val.argmin())
    assert int(marca.get("data-epoca")) == k
    assert abs(float(marca.get("cx")) - GEN.escala_x(k, redes.EPOCAS)) < 0.06
    assert abs(float(marca.get("cy")) - GEN.escala_y(val[k], panel)) < 0.06
    texto = _leer("dl-curvas-rmse")
    assert f"mínimo {val.min():.3f}" in texto
    assert f"en la época {k}" in texto


def test_sin_mu_la_validacion_sube_tras_su_minimo(historias):
    """Lo que la figura existe para enseñar: sin μ la validacion baja y
    luego sube; con μ termina mas cerca de su minimo."""
    _, hist = historias
    sin = np.array(hist["sin-mu"]["rmse_validacion"])
    con = np.array(hist["con-mu"]["rmse_validacion"])
    assert sin[-1] - sin.min() > 0.05
    assert con[-1] - con.min() < sin[-1] - sin.min()
    assert sin.argmin() < len(sin) // 2
