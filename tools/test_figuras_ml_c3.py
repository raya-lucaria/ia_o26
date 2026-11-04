"""Pruebas propias de las figuras de la clase 3 (tools/figuras_ml_c3.py).

Sin prosa (D-003). Las guardas comunes (test_9, XML, ancho, letra, opacidad,
determinismo, créditos, huérfanos, figura<->página) viven en
tools/test_gen_aprendizaje_maquina.py. Aquí: el catálogo de la clase, que el
texto alternativo nombre las cifras que salen de tools/ml_cifras_c3.py (la
forma «cita»), que cada figura tenga su fila en el bloque «## Clase 3» de
CREDITOS.md y que el diagrama se genere sin ml_lab.

Anclas por tramo (protocolo p5.2 §7.1): la rama de clase agrega solo antes
del «fin tramo rapido».
"""
import html
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import figuras_ml_c3 as fig

HERRAMIENTAS = Path(__file__).resolve().parent
CREDITOS = gen.ASSETS_ML / "CREDITOS.md"


@lru_cache(maxsize=None)
def contenido(ident):
    return gen.contenido(ident)


def aria(ident):
    return html.unescape(re.search(r'aria-label="([^"]*)"', contenido(ident)).group(1))


def _cif():
    pytest.importorskip("sklearn")
    import ml_cifras_c3 as cif
    return cif


# --- tramo rapido ---

RAPIDO = ["ml-c3-mismo-rmse", "ml-c3-benchmarks", "ml-c3-media-acumulada",
          "ml-c3-fuentes-patologias", "ml-c3-diana-beta", "ml-c3-interaccion-plano",
          "ml-c3-colineal-prediccion", "ml-c3-un-coeficiente", "ml-c3-elipse-region",
          "ml-c3-encoger-1d", "ml-c3-grado-12-mu", "ml-c3-trayectorias",
          "ml-c3-ridge-colineal", "ml-c3-estandarizar", "ml-c3-mu-cv",
          "ml-c3-recta-de-apoyo"]
DIAGRAMAS = ["ml-c3-fuentes-patologias"]


def test_el_tramo_rapido_trae_las_dieciseis_figuras_en_orden():
    assert list(fig._RAPIDO) == RAPIDO


def test_el_catalogo_es_la_suma_de_los_tramos():
    assert fig.FIGURAS_C3 == {**fig._RAPIDO, **fig._COMPLETO}


def test_importar_las_figuras_no_importa_ml_lab_ni_matplotlib():
    codigo = ("import sys; sys.path.insert(0, %r); import figuras_ml_c3; "
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


def test_el_diagrama_usa_los_nombres_de_las_fuentes_de_la_clase_1():
    a = aria("ml-c3-fuentes-patologias")
    for nombre in ("azar", "variables que no medimos", "familia equivocada", "pocos datos"):
        assert nombre in a
    assert "aproximación" not in a and "irreducible" not in a


def _bloque_clase_3():
    texto = CREDITOS.read_text(encoding="utf-8")
    inicio = texto.index("## Clase 3")
    fin = texto.index("## Clase 4")
    return texto[inicio:fin]


@pytest.mark.parametrize("ident", RAPIDO)
def test_cada_figura_tiene_su_fila_en_el_bloque_clase_3(ident):
    filas = [l for l in _bloque_clase_3().splitlines() if l.startswith(f"| `{ident}.svg`")]
    assert len(filas) == 1, f"{ident}: {len(filas)} filas en el bloque Clase 3"
    assert "CC BY-SA 4.0" in filas[0]


# Cada figura de datos nombra en su texto alternativo las cifras de su función
# de ml_cifras_c3 (con la forma «cita»): si la cifra cambia, el alt también.
def _cifras_esperadas(ident):
    cif = _cif()
    q = lambda f: f()["cita"]
    if ident == "ml-c3-mismo-rmse":
        return [q(cif.cifras_c3_mismo_rmse)["rmse_val"]]
    if ident == "ml-c3-benchmarks":
        e, s = q(cif.cifras_c3_escala_y), q(cif.cifras_c3_senal_debil)
        return [e["rmse_modelo"], e["rmse_media"], e["rmse_sobre_ybar"], e["mejora"],
                s["rmse_modelo"], s["raiz_piso"], s["rmse_media"]]
    if ident == "ml-c3-media-acumulada":
        c = q(cif.cifras_c3_colas)
        return [c["normal"], c["pareto"], c["cauchy"]]
    if ident == "ml-c3-diana-beta":
        c = q(cif.cifras_c3_diana)
        return [c["omitida"], c["endogena"]]
    if ident == "ml-c3-colineal-prediccion":
        c = q(cif.cifras_c3_colineal)
        return [c["desv_beta1_0"], c["desv_beta1_99"], c["desv_y_dentro_99"], c["desv_y_fuera_99"]]
    if ident == "ml-c3-elipse-region":
        c = q(cif.cifras_c3_regiones)
        return [c["l2"]["beta1"], c["l2"]["beta2"], c["elastica"]["beta1"], c["elastica"]["beta2"]]
    if ident == "ml-c3-grado-12-mu":
        c = q(cif.cifras_c3_grado12)
        return [c["mu_medio"], c["R"]["grande"], c["R"]["medio"], c["R"]["chico"]]
    if ident == "ml-c3-trayectorias":
        c = q(cif.cifras_c3_trayectorias)
        return [c["primera_util"], c["ultima_util"]]
    if ident == "ml-c3-ridge-colineal":
        c = q(cif.cifras_c3_ridge_colineal)
        return [c["sin"]["desv"], c["ridge"]["desv"]]
    if ident == "ml-c3-estandarizar":
        c = q(cif.cifras_c3_estandarizar)
        return [c["sin_x1"], c["sin_x2"], c["con_x1"], c["con_x2"]]
    if ident == "ml-c3-mu-cv":
        c = q(cif.cifras_c3_mu_cv)
        return [c["mu_min"], c["no_ceros_min"], c["mu_un_ee"], c["no_ceros_un_ee"], c["R_un_ee"]]
    if ident == "ml-c3-recta-de-apoyo":
        c = q(cif.cifras_c3_recta_apoyo)
        return [c["d"], c["mu"]]
    return []


@pytest.mark.parametrize("ident", [i for i in RAPIDO if i not in DIAGRAMAS])
def test_el_alt_nombra_las_cifras_de_ml_cifras_c3(ident):
    esperadas = _cifras_esperadas(ident)
    a = aria(ident)
    for cifra in esperadas:
        assert cifra in a, f"{ident}: el alt no dice {cifra!r}"


def test_el_alt_de_f10_y_f8_dice_el_umbral_de_lasso():
    assert "entre −0.5 y 0.5" in aria("ml-c3-encoger-1d")
    assert "desde μ = 2" in aria("ml-c3-un-coeficiente")


def test_f16_solo_dibuja_presupuestos_positivos():
    cif = _cif()
    assert min(cif.rejilla_presupuesto()) > 0 and cif.D_MARCADO > 0
# --- fin tramo rapido ---


# --- tramo completo ---
# --- fin tramo completo ---
