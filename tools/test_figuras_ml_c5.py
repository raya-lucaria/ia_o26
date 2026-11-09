"""Pruebas propias de las figuras de la clase 5 (tools/figuras_ml_c5.py).

Sin prosa (D-003). Las guardas comunes (raíz <svg>, XML, ancho, letra,
opacidad, determinismo, créditos, huérfanos, figura<->página) viven en
tools/test_gen_aprendizaje_maquina.py. Aquí, lo que pide clase_5.md §10.8: el
catálogo de las 16 figuras partido en P1 y P2, cada id en exactamente un dict y
con prefijo ml-c5-, que el texto alternativo nombre las cifras de
tools/ml_cifras_c5.py (forma «cita»), la guarda copiada de la clase 4 (ningún
$R$ junto a MCC, $A_{\\text{bal}}$, $A$ o aciertos), la fila de cada figura en el
bloque «## Clase 5» de CREDITOS.md, y que los diagramas se generen sin ml_lab.
"""
import html
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import figuras_ml_c5 as fig

HERRAMIENTAS = Path(__file__).resolve().parent
CREDITOS = gen.ASSETS_ML / "CREDITOS.md"
CITAS = json.loads((HERRAMIENTAS / "datos" / "citas_c5.json").read_text(encoding="utf-8"))

P1 = ["ml-c5-modelo-exitoso", "ml-c5-bolsas", "ml-c5-particiones", "ml-c5-momento-decision",
      "ml-c5-tuberia", "ml-c5-detectores", "ml-c5-cv-miente", "ml-c5-fugas",
      "ml-c5-imputacion"]
P2 = ["ml-c5-receta", "ml-c5-phi-aprendida", "ml-c5-trampa-dummy", "ml-c5-diagnostico",
      "ml-c5-arbol-escalones", "ml-c5-familias-capacidad", "ml-c5-cybenko"]
FIGURAS = P1 + P2
DIAGRAMAS = ["ml-c5-modelo-exitoso", "ml-c5-bolsas", "ml-c5-particiones",
             "ml-c5-momento-decision", "ml-c5-tuberia", "ml-c5-receta", "ml-c5-phi-aprendida"]


@lru_cache(maxsize=None)
def contenido(ident):
    return gen.contenido(ident)


def aria(ident):
    return html.unescape(re.search(r'aria-label="([^"]*)"', contenido(ident)).group(1))


def textos(ident):
    s = contenido(ident)
    return html.unescape(" ".join(re.findall(r">([^<>]+)<", s) + [aria(ident)]))


def test_el_catalogo_trae_las_dieciseis_partidas_en_p1_y_p2():
    assert set(fig.FIGURAS_C5_P1) == set(P1)
    assert set(fig.FIGURAS_C5_P2) == set(P2)
    assert not set(P1) & set(P2)
    assert fig.FIGURAS_C5 == {**fig.FIGURAS_C5_P1, **fig.FIGURAS_C5_P2}
    assert all(i.startswith("ml-c5-") for i in fig.FIGURAS_C5)
    assert all(f.__name__.startswith("fig_") for f in fig.FIGURAS_C5.values())


def test_importar_las_figuras_no_importa_ml_lab_ni_matplotlib():
    codigo = ("import sys; sys.path.insert(0, %r); import figuras_ml_c5; "
              "print('aprendizaje_maquina' in sys.modules, 'matplotlib' in sys.modules)"
              % str(HERRAMIENTAS))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip() == "False False", r.stdout + r.stderr


@pytest.mark.parametrize("ident", DIAGRAMAS)
def test_el_diagrama_se_genera_sin_ml_lab(ident):
    codigo = ("import sys; sys.path.insert(0, %r); import gen_aprendizaje_maquina as g; "
              "g.contenido(%r); print('aprendizaje_maquina' in sys.modules)"
              % (str(HERRAMIENTAS), ident))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip().endswith("False"), r.stdout + r.stderr


def _bloque_clase_5():
    texto = CREDITOS.read_text(encoding="utf-8")
    return texto[texto.index("## Clase 5"):]


@pytest.mark.parametrize("ident", FIGURAS)
def test_cada_figura_tiene_su_fila_en_el_bloque_clase_5(ident):
    filas = [l for l in _bloque_clase_5().splitlines() if l.startswith(f"| `{ident}.svg`")]
    assert len(filas) == 1, f"{ident}: {len(filas)} filas en el bloque Clase 5"
    assert "CC BY-SA 4.0" in filas[0]


def test_el_bloque_clase_5_tiene_dieciseis_filas():
    assert len(re.findall(r"^\| `ml-c5-", _bloque_clase_5(), re.M)) == 16


@pytest.mark.parametrize("ident", FIGURAS)
def test_raiz_svg_con_viewbox_tamano_y_fondo(ident):
    s = contenido(ident)
    raiz = re.search(r"<svg\b[^>]*>", s).group(0)
    assert "viewBox" in raiz and 'width="' in raiz and 'height="' in raiz
    assert gen.FONDO.lower() in s.lower()


@pytest.mark.parametrize("ident", FIGURAS)
def test_aria_no_vacio_y_sin_dolar(ident):
    a = aria(ident)
    assert a.strip() and "$" not in a


@pytest.mark.parametrize("ident", FIGURAS)
def test_ninguna_r_junto_a_una_metrica(ident):
    """Guarda copiada de la clase 4 (§10.8, r1-18)."""
    t = textos(ident)
    for m in re.finditer(r"(?<![A-Za-zÁ-ú_])R(?![A-Za-zÁ-ú_])", t):
        cerca = t[max(0, m.start() - 50):m.end() + 50]
        assert not re.search(r"MCC|A_bal|aciertos", cerca), f"{ident}: …{cerca}…"


@pytest.mark.parametrize("ident", FIGURAS)
def test_ningun_phi_con_subindice_numerico(ident):
    assert not re.search(r"φ_?\d|\\phi_\d", textos(ident))


CIFRAS_EN_ALT = {
    "ml-c5-cv-miente": ["cifras_c5_cv_miente/c14_clase2/azar", "cifras_c5_cv_miente/c14_clase2/R",
                        "cifras_c5_cv_miente/c13_lineal/azar"],
    "ml-c5-fugas": ["cifras_c5_fugas/posterior/cv", "cifras_c5_fugas/posterior/uso",
                    "cifras_c5_fugas/seleccion_previa/cv"],
    "ml-c5-imputacion": ["cifras_c5_imputacion/L_sin", "cifras_c5_imputacion/L_con",
                         "cifras_c5_imputacion/pendiente_centinela"],
    "ml-c5-detectores": ["cifras_c5_adversarial/nada_bosque/log_loss",
                         "cifras_c5_adversarial/deriva_bosque/log_loss"],
    "ml-c5-trampa-dummy": ["cifras_c5_dummy/rango"],
    "ml-c5-diagnostico": ["cifras_c5_diagnostico/azar", "cifras_c5_diagnostico/grupos"],
    "ml-c5-arbol-escalones": ["cifras_c5_arbol/mcc/1", "cifras_c5_arbol/mcc/6"],
    "ml-c5-familias-capacidad": ["cifras_c5_familias/profundidad", "cifras_c5_familias/etapas"],
    "ml-c5-cybenko": ["cifras_c5_cybenko/error/10", "cifras_c5_cybenko/n_polar",
                      "cifras_c5_cybenko/n_aprendida"],
}


def _cita(ruta):
    v = CITAS
    for k in ruta.split("/"):
        v = v[k]
    return v


@pytest.mark.parametrize("ident", sorted(CIFRAS_EN_ALT))
def test_el_alt_nombra_las_cifras_de_ml_cifras_c5(ident):
    pytest.importorskip("sklearn")
    a = aria(ident)
    for ruta in CIFRAS_EN_ALT[ident]:
        assert str(_cita(ruta)) in a, f"{ident}: falta {ruta} = {_cita(ruta)!r} en el alt"
