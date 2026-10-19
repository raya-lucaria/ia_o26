"""Guardas de los diagramas de la unidad de cadenas de Markov.

Clase de prueba «compara sin escribir» (.claude/skills/unidad/referencias/
codigo.md § 3): contenido(nombre) se compara byte a byte con el SVG
comiteado, sin escribirlo. Si alguien edita un SVG a mano, o cambia
markov.py sin volver a correr el generador, la prueba falla con «corre el
generador».

Ademas, las convenciones de test_gen_juegos.py con ANCHO = 300: prefijo,
raiz <svg> con viewBox/width/height/aria-label, fondo del skin, <title> y
<desc>, sin opacidades, XML valido, sin huerfanos, sin SVG que ninguna pagina
use, letra de 12 px o mas, nada fuera del lienzo y ningun rotulo encimado
sobre otro. Y que lo dibujado salga de markov.py.
"""
import html
import os
import re
import xml.etree.ElementTree as ET
from functools import lru_cache

import pytest

import gen_markov as gen
import markov as m

FONDO = "#211033"
ANCHO = 300
UNIDAD = gen.ASSETS.parent
NOMBRES = sorted(gen.DIAGRAMAS)
_DEJAVU = "/usr/share/fonts/truetype/dejavu/"


@lru_cache(maxsize=None)
def _svg(nombre):
    return gen.contenido(nombre)


def _aria(nombre):
    return html.unescape(re.search(r'aria-label="([^"]*)"', _svg(nombre)).group(1))


def _renglones(nombre):
    return [html.unescape(t) for t in re.findall(r">([^<>]+)</text>", _svg(nombre))]


# ------------------------------------------------------ el archivo ---

@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_es_el_que_produce_el_generador(nombre):
    archivo = gen.ASSETS / f"{nombre}.svg"
    assert archivo.is_file(), f"falta {archivo.name}: corre python3 tools/gen_markov.py"
    assert archivo.read_text(encoding="utf-8") == _svg(nombre), (
        f"{archivo.name} no es el que produce el generador: corre "
        "python3 tools/gen_markov.py y revisa el diff")


def test_cada_diagrama_lleva_el_prefijo_de_la_clase():
    assert all(n.startswith("mkv-c1-") for n in NOMBRES)


def test_estan_las_figuras_de_prioridad_1_y_la_de_rachas():
    assert set(NOMBRES) == {
        "mkv-c1-flujo-muestrear", "mkv-c1-flujo-contar", "mkv-c1-flujo-predecir",
        "mkv-c1-flujo-generar", "mkv-c1-grafo-vc", "mkv-c1-arbol-2-pasos",
        "mkv-c1-mu-t", "mkv-c1-recuperar-p", "mkv-c1-ceros", "mkv-c1-rachas"}


@pytest.mark.parametrize("nombre", NOMBRES)
def test_la_raiz_svg_trae_sus_convenciones(nombre):
    texto = _svg(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", texto).group()
    for atributo in ('viewBox="', 'role="img"', "aria-label="):
        assert atributo in etiqueta, (nombre, atributo)
    assert re.search(r'\bwidth="\d', etiqueta) and re.search(r'\bheight="\d', etiqueta)
    assert f'fill="{FONDO}"' in texto
    assert "<title>" in texto and "<desc>" in texto
    assert "fill-opacity" not in texto and "stroke-opacity" not in texto
    ET.fromstring(texto)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_todas_miden_300_de_ancho(nombre):
    """Plan de unidad §6: 300 px caben en un telefono de 390 sin deslizar."""
    etiqueta = re.match(r"<svg\b[^>]*>", _svg(nombre)).group()
    ancho = float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1))
    caja = re.search(r'viewBox="0 0 ([\d.]+) ', etiqueta).group(1)
    assert ancho == ANCHO == float(caja), nombre


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ninguna_letra_baja_de_12(nombre):
    chicas = [(t, c) for t, c in re.findall(
        r'<text [^>]*font-size="([\d.]+)"[^>]*>([^<]*)<', _svg(nombre)) if float(t) < 12]
    assert not chicas, (nombre, chicas)


def test_no_queda_ningun_svg_huerfano():
    en_disco = {p.stem for p in gen.ASSETS.glob("mkv-*.svg")}
    assert en_disco == set(gen.DIAGRAMAS)


def test_ningun_svg_sin_pagina_que_lo_use():
    paginas = "\n".join(
        p.read_text(encoding="utf-8") for p in UNIDAD.rglob("*.md")
        if not any(parte.startswith("_") for parte in p.relative_to(UNIDAD).parts))
    sin_usar = sorted(f"{n}.svg" for n in gen.DIAGRAMAS if f"{n}.svg" not in paginas)
    assert not sin_usar, f"SVG que ninguna pagina enlaza: {sin_usar}"


# ------------------------------------------------- nada se encima ---

_PATRON_TEXTO = (r'<text x="([\d.-]+)" y="([\d.-]+)"[^>]*font-family="([^"]*)" '
                 r'font-size="([\d.]+)" font-weight="(\w+)" text-anchor="(\w+)">([^<]*)</text>')


def _cajas_de_texto(nombre):
    """(x0, y0, x1, y1, texto) de cada <text> sin girar, medido con DejaVu (la
    letra con que el navegador de esta maquina resuelve system-ui)."""
    ImageFont = pytest.importorskip("PIL.ImageFont")
    if not os.path.isdir(_DEJAVU):
        pytest.skip("sin DejaVu")
    cajas = []
    for x, y, familia, tam, peso, anclaje, contenido in re.findall(_PATRON_TEXTO, _svg(nombre)):
        archivo = (("DejaVuSansMono" if "mono" in familia else "DejaVuSans")
                   + ("-Bold" if peso == "700" else "") + ".ttf")
        t = float(tam)
        s = html.unescape(contenido)
        w = ImageFont.truetype(_DEJAVU + archivo, round(t)).getlength(s)
        x, y = float(x), float(y)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anclaje]
        cajas.append((x0, y - 0.75 * t, x0 + w, y + 0.22 * t, s))
    return cajas


@pytest.mark.parametrize("nombre", NOMBRES)
def test_nada_se_sale_del_lienzo(nombre):
    alto = float(re.search(r'height="([\d.]+)"', _svg(nombre)).group(1))
    for x0, y0, x1, y1, s in _cajas_de_texto(nombre):
        assert 4 <= x0 and x1 <= ANCHO - 4, (nombre, s, round(x0), round(x1))
        assert 0 <= y0 and y1 <= alto, (nombre, s)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ningun_rotulo_se_encima_sobre_otro(nombre):
    """Se publico «el va▮lor» en juegos (defecto 6): aqui ningun par de
    rotulos sin girar comparte un pixel."""
    cajas = _cajas_de_texto(nombre)
    for i, a in enumerate(cajas):
        for b in cajas[i + 1:]:
            se_tocan = (a[0] < b[2] - 0.5 and b[0] < a[2] - 0.5
                        and a[1] < b[3] - 0.5 and b[1] < a[3] - 0.5)
            assert not se_tocan, (nombre, a[4], b[4])


# ------------------------------------- lo dibujado sale de markov.py ---

def _fr(x):
    return gen.fr(x)


def test_el_grafo_dibuja_la_matriz_de_la_frase():
    P = m.matriz_estimada(m.frase_vc())
    assert [[_fr(x) for x in f] for f in P] == [["2/11", "9/11"], ["2/3", "1/3"]]
    renglones = _renglones("mkv-c1-grafo-vc")
    for rot in ("2/11", "9/11", "2/3", "1/3"):
        assert rot in renglones, rot
    aria = _aria("mkv-c1-grafo-vc")
    assert "a V con 2/11" in aria and "a C con 9/11" in aria
    assert "a V con 2/3" in aria and "a C con 1/3" in aria


def test_el_arbol_dibuja_los_cuatro_caminos_y_su_suma():
    renglones = _renglones("mkv-c1-arbol-2-pasos")
    for hoja in ("4/33", "6/11", "2/9", "1/9"):
        assert hoja in renglones, hoja
    assert "4/33 + 2/9 = 34/99." in renglones
    assert "Pr(S₂ = V) = 4/33 + 2/9 = 34/99." in _aria("mkv-c1-arbol-2-pasos")


def test_mu_t_dibuja_la_cuenta_y_la_simulacion():
    datos = m.mu_t_corpus()
    aria = _aria("mkv-c1-mu-t")
    assert "10 000 réplicas" in aria
    # la cuenta desde C, a mano: 0, 0.710, 0.334, 0.533…
    assert "Desde C: cuenta 0.000, 0.710, 0.334, 0.533, 0.428, 0.484, 0.454, 0.470, 0.462" \
        in aria
    assert "Desde V: cuenta 1.000, 0.181, 0.615, 0.385, 0.507, 0.442, 0.476, 0.458, 0.468" \
        in aria
    for d in datos.values():
        assert ", ".join(gen.dec(p) for p in d["simulada"]) in aria
    assert "la mayor diferencia es 0.010, unos 2.0 errores estándar" in aria
    # una marca por paso y por inicio en cada panel: 9 x 2 x 2
    svg = _svg("mkv-c1-mu-t")
    assert svg.count("<circle") == 9 * 2 + 1 and svg.count('<rect x="') >= 9 * 2


def test_recuperar_p_dibuja_las_siete_longitudes():
    aria = _aria("mkv-c1-recuperar-p")
    for T in ("10", "30", "100", "300", "1 000", "3 000", "10 000"):
        assert f"T = {T}: mediana" in aria, T
    assert "T = 10: mediana 0.210, del 5 % al 95 % entre 0.069 y 0.319" in aria
    assert "T = 10 000: mediana 0.006, del 5 % al 95 % entre 0.002 y 0.013" in aria
    assert "Réplicas con un estado sin salidas: 0." in aria


def test_ceros_dibuja_las_cuatro_memorias():
    aria = _aria("mkv-c1-ceros")
    assert "memoria 0: 0 % (0 de 998 564)" in aria
    assert "memoria 1: 0.003 % (29 de 998 563), contextos vistos 27 de 28" in aria
    assert "memoria 2: 0.072 % (718 de 998 562), contextos vistos 379 de 784" in aria
    assert "memoria 3: 0.570 % (5 694 de 998 561), contextos vistos 3 328 de 21 952" in aria


def test_rachas_dibuja_reales_y_los_dos_modelos():
    aria = _aria("mkv-c1-rachas")
    assert "q = 0.290 (círculos)" in aria and "q = 0.536 (cuadrados)" in aria
    assert "ℓ = 1: reales 384 971" in aria
    assert "ℓ = 4: reales 323" in aria and "ℓ = 5: reales 3," in aria
    reales = m.rachas_corpus()
    sim = m.rachas_simuladas("markov")
    for ell in range(1, 6):
        assert f"ℓ = {ell}: reales {gen.miles(reales.get(ell, 0))}, cadena " \
               f"{gen.miles(sim[ell][0])}" in aria
    # marcas distintas, no solo color: circulo (cadena) y cuadro (independientes)
    svg = _svg("mkv-c1-rachas")
    assert svg.count("<circle") == 5 + 1


@pytest.mark.parametrize("clave", sorted(gen.FLUJOS))
def test_cada_flujo_tiene_rombo_y_salida_explicita(clave):
    """Cajas con verbos cortos, una decision por rombo, una sola salida (la
    caja de borde de acento) y al menos una vuelta."""
    f = gen.FLUJOS[clave]
    cajas = [p for p in f["pasos"] if "caja" in p]
    rombos = [p for p in f["pasos"] if "rombo" in p]
    assert 3 <= len(cajas) <= 6 and rombos and f["vueltas"]
    assert [p.get("fin") for p in f["pasos"]].count(True) == 1
    assert f["pasos"][-1].get("fin")
    svg = gen.contenido(f"mkv-c1-flujo-{clave}")
    assert svg.count("<polygon") == len(rombos)
