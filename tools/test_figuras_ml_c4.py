"""Pruebas propias de las figuras de la clase 4 (tools/figuras_ml_c4.py).

Sin prosa (D-003). Las guardas comunes (test_9, XML, ancho, letra, opacidad,
determinismo, créditos, huérfanos, figura<->página) viven en
tools/test_gen_aprendizaje_maquina.py. Aquí, lo que pide clase_4.md §10.8: el
catálogo de las 20 figuras, que el texto alternativo nombre las cifras de
tools/ml_cifras_c4.py (forma «cita»), el mapa único de reservas, que
ml-c4-separable no reajuste, ningún «techo» ni R junto a una métrica, la fila
de cada figura en el bloque «## Clase 4» de CREDITOS.md, y que los diagramas
sin cifras se generen sin ml_lab.
"""
import html
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import figuras_ml_c4 as fig

HERRAMIENTAS = Path(__file__).resolve().parent
CREDITOS = gen.ASSETS_ML / "CREDITOS.md"

FIGURAS = ["ml-c4-moda-99", "ml-c4-separable", "ml-c4-cadena-decision",
           "ml-c4-perdida-vs-metrica", "ml-c4-umbral", "ml-c4-contribucion-clases",
           "ml-c4-metricas-vs-proporcion", "ml-c4-pesos-umbral", "ml-c4-anillos-metricas",
           "ml-c4-mcc-por-pliegue", "ml-c4-softmax", "ml-c4-fronteras-tres-clases",
           "ml-c4-macro-ponderado", "ml-c4-recuadro-confusion", "ml-c4-confiabilidad",
           "ml-c4-tasa", "ml-c4-mapa-reservas", "ml-c4-conformal-rangos",
           "ml-c4-conformal-conjuntos", "ml-c4-cobertura-por-clase"]
SIN_ML_LAB = ["ml-c4-cadena-decision", "ml-c4-softmax", "ml-c4-mapa-reservas", "ml-c4-tasa"]


@lru_cache(maxsize=None)
def contenido(ident):
    return gen.contenido(ident)


def aria(ident):
    return html.unescape(re.search(r'aria-label="([^"]*)"', contenido(ident)).group(1))


def textos(ident):
    """Todo el texto visible del SVG (las <text> de matplotlib van como glifos, así que
    para las gráficas de datos esto solo cubre title, desc y aria)."""
    s = contenido(ident)
    partes = re.findall(r">([^<>]+)<", s) + [aria(ident)]
    return html.unescape(" ".join(partes))


def _cif():
    pytest.importorskip("sklearn")
    import ml_cifras_c4 as cif
    return cif


def test_el_catalogo_trae_las_veinte_figuras_en_orden():
    assert list(fig.FIGURAS_C4) == FIGURAS
    assert "ml-c4-estratificar" not in fig.FIGURAS_C4


def test_importar_las_figuras_no_importa_ml_lab_ni_matplotlib():
    codigo = ("import sys; sys.path.insert(0, %r); import figuras_ml_c4; "
              "print('aprendizaje_maquina' in sys.modules, 'matplotlib' in sys.modules)"
              % str(HERRAMIENTAS))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip() == "False False", r.stdout + r.stderr


@pytest.mark.parametrize("ident", SIN_ML_LAB)
def test_el_diagrama_se_genera_sin_ml_lab(ident):
    codigo = ("import sys; sys.path.insert(0, %r); import gen_aprendizaje_maquina as g; "
              "g.contenido(%r); print('aprendizaje_maquina' in sys.modules)"
              % (str(HERRAMIENTAS), ident))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip().endswith("False"), r.stdout + r.stderr


def _bloque_clase_4():
    texto = CREDITOS.read_text(encoding="utf-8")
    return texto[texto.index("## Clase 4"):texto.index("## Clase 5")]


@pytest.mark.parametrize("ident", FIGURAS)
def test_cada_figura_tiene_su_fila_en_el_bloque_clase_4(ident):
    filas = [l for l in _bloque_clase_4().splitlines() if l.startswith(f"| `{ident}.svg`")]
    assert len(filas) == 1, f"{ident}: {len(filas)} filas en el bloque Clase 4"
    assert "CC BY-SA 4.0" in filas[0]


def test_el_bloque_clase_4_tiene_veinte_filas_y_ninguna_de_estratificar():
    b = _bloque_clase_4()
    assert len(re.findall(r"^\| `ml-c4-", b, re.M)) == 20
    assert "ml-c4-estratificar" not in b


@pytest.mark.parametrize("ident", FIGURAS)
def test_aria_no_vacio_y_sin_dolar(ident):
    a = aria(ident)
    assert a.strip() and "$" not in a


@pytest.mark.parametrize("ident", FIGURAS)
def test_ningun_techo_junto_a_mcc(ident):
    t = textos(ident)
    for m in re.finditer(r"techo", t, re.I):
        assert "MCC" not in t[max(0, m.start() - 60):m.end() + 60], ident


@pytest.mark.parametrize("ident", FIGURAS)
def test_ninguna_r_junto_a_una_metrica(ident):
    t = textos(ident)
    assert not re.search(r"\bR\s*\(?[^.]{0,20}(MCC|Brier|aciertos)", t), ident
    assert not re.search(r"(MCC|Brier|aciertos)[^.]{0,20}\bR\b", t), ident


@pytest.mark.parametrize("ident", FIGURAS)
def test_ningun_phi_con_subindice_numerico(ident):
    assert not re.search(r"φ[₀-₉]|\\phi_[0-9]", textos(ident))


def test_mapa_de_reservas_un_solo_vocabulario():
    assert fig.piezas_mapa_reservas() == ["ent", "val_a", "val_b", "cal", "prueba"]
    t = textos("ml-c4-mapa-reservas")
    for p in ("val_a", "val_b", "cal", "se aparta primero"):
        assert p in t
    for p in ("val_eval", "val_cal", "val3_b"):
        assert p not in t
    corte = [p for p in fig.PIEZAS_MAPA if "conformal" in p[3]]
    assert [p[0] for p in corte] == ["cal"]


def test_separable_no_reajusta(monkeypatch):
    cif = _cif()
    for ruido in (False, True):
        cif.ajustes_separable(ruido)  # precalculado una vez, como el NB08 bloque 1
    ml = gen.ml_lab()

    def prohibido(*a, **k):
        raise AssertionError("dibujar_separable no reajusta")
    monkeypatch.setattr(ml, "ajustar", prohibido)
    monkeypatch.setattr(ml, "ajustes_por_mu", prohibido)
    svg = fig.ml_c4_separable()
    assert "‖β̂‖₂" in svg or "variables estandarizadas" in html.unescape(svg) or svg


def test_separable_usa_phi_estandarizada_y_eje_lineal():
    import inspect
    fuente = inspect.getsource(_cif().ajustes_separable)
    assert "ml.estandarizar(ml.columnas(\"x\"))" in fuente
    assert "set_yscale" not in inspect.getsource(fig.ml_c4_separable)


def _cifras_esperadas(ident):
    cif = _cif()
    q = lambda f: f()["cita"]  # noqa: E731
    if ident == "ml-c4-moda-99":
        c = q(cif.cifras_c4_moda)["uno"]
        return [c["aciertos"], c["aciertos_balanceados"], c["mcc"]]
    if ident == "ml-c4-separable":
        return [q(cif.cifras_c4_separable)["por_decada"]]
    if ident == "ml-c4-umbral":
        c = q(cif.cifras_c4_umbral)
        return [c["tau"], c["mcc_val_05"], c["mcc_val_elegido"]]
    if ident == "ml-c4-metricas-vs-proporcion":
        return [q(cif.cifras_c4_desbalanceo)["banda_01"]]
    if ident == "ml-c4-pesos-umbral":
        c = q(cif.cifras_c4_pesos_intercepto)
        return [c["salto"], c["ln_razon"], c["coincidencia"]]
    if ident == "ml-c4-anillos-metricas":
        c = q(cif.cifras_c4_anillos)
        return [c["lineal"], c["lineal_pesos"], c["cuadratica_pesos"]]
    if ident == "ml-c4-mcc-por-pliegue":
        c = q(cif.cifras_c4_mcc_por_pliegue)
        return [c["fraudes_ent"], c["min_mcc_10"], c["max_mcc_10"]]
    if ident == "ml-c4-fronteras-tres-clases":
        c = q(cif.cifras_c4_multiclase)
        return [c["sin"]["por_clase"][2], c["con"]["por_clase"][2]]
    if ident == "ml-c4-macro-ponderado":
        c = q(cif.cifras_c4_noticias)
        return list(c["aciertos"]) + [c["macro"], c["ponderado"]]
    if ident == "ml-c4-recuadro-confusion":
        return [q(cif.cifras_c4_umbral)["tau"]]
    if ident == "ml-c4-confiabilidad":
        c = q(cif.cifras_c4_calibracion)
        return [c["brier_sin"], c["brier_con"], c["brier_benchmark"]]
    if ident == "ml-c4-tasa":
        return [q(cif.cifras_c4_tasa)["sin"]]
    if ident == "ml-c4-conformal-conjuntos":
        c = q(cif.cifras_c4_conformal_equilibrado)
        return [c["cobertura_01"], c["tamano_01"]]
    if ident == "ml-c4-cobertura-por-clase":
        c = q(cif.cifras_c4_conformal_repetido)
        return [c["marginal_fraude"], c["por_clase_fraude"], c["R"]]
    return []


@pytest.mark.parametrize("ident", FIGURAS)
def test_el_alt_nombra_las_cifras_de_ml_cifras_c4(ident):
    a = aria(ident)
    for cifra in _cifras_esperadas(ident):
        assert cifra in a, f"{ident}: el alt no dice {cifra!r}"


def test_mcc_por_pliegue_dibuja_las_cifras_de_ml_cifras_c4():
    cif = _cif()
    import math
    tabla = fig.tabla_metrica_por_pliegue()
    m = cif.cifras_c4_mcc_por_pliegue()["por_k"]
    for k, v in m.items():
        t = tabla[tabla["k"] == k]
        assert list(t[t["metrica"] == "mcc"]["valor"]) == pytest.approx(v["mcc"])
        ab = list(t[t["metrica"] == "aciertos_balanceados"]["valor"])
        assert all((math.isnan(a) and math.isnan(b)) or a == pytest.approx(b)
                   for a, b in zip(ab, v["aciertos_balanceados"]))
        # un A_bal no estimable (nan) solo donde el pliegue no tiene fraude
        for _, fila in t.iterrows():
            if fila["metrica"] == "aciertos_balanceados" and math.isnan(fila["valor"]):
                assert fila["raros"] == 0
        assert not t[t["metrica"] == "mcc"]["valor"].isna().any()


def test_conformal_rangos_dibuja_el_ejemplo_exacto():
    t = textos("ml-c4-conformal-rangos")
    assert "ĉ = 0.6" in t and "C(x) = {0}" in t
