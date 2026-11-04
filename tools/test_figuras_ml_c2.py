"""Pruebas propias de las figuras de la clase 2 (tools/figuras_ml_c2.py).

Sin prosa (D-003). Las guardas comunes (test_9, XML, ancho, letra, opacidad,
determinismo, creditos, huerfanos, figura<->pagina) viven en
tools/test_gen_aprendizaje_maquina.py. Aqui: el catalogo de la clase por
tramos, los roles de la leyenda unica (contrato §7.3), que cada figura de
datos dibuje las cifras de tools/ml_cifras_c2.py y que el texto alternativo
las nombre.

Anclas por tramo (protocolo p5.2 §7.1, clase_2.md §10.11): cada rama agrega
sus pruebas solo dentro del ancla de su tramo.
"""
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import figuras_ml_c2 as fig

HERRAMIENTAS = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def contenido(ident):
    return gen.contenido(ident)


def aria(ident):
    return re.search(r'aria-label="([^"]*)"', contenido(ident)).group(1)


def colores(ident):
    return {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", contenido(ident))}


def test_el_catalogo_es_la_suma_de_los_tramos():
    assert fig.FIGURAS_C2 == {**fig._RAPIDO, **fig._M, **fig._COMPLETO}


def test_ningun_id_empieza_por_una_palabra_de_tipo():
    for ident in fig.FIGURAS_C2:
        assert ident.startswith("ml-c2-")
        assert not re.match(r"ml-c2-(fig|figura|diagrama|grafica)-", ident)


def test_importar_las_figuras_no_importa_ml_lab_ni_matplotlib():
    codigo = ("import sys; sys.path.insert(0, %r); import figuras_ml_c2; "
              "print('aprendizaje_maquina' in sys.modules, 'matplotlib' in sys.modules)"
              % str(HERRAMIENTAS))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip() == "False False", r.stdout + r.stderr


# --- tramo rapido ---

DIAGRAMAS_RAPIDO = ["ml-c2-dos-niveles", "ml-c2-tres-conjuntos", "ml-c2-simulacro",
                    "ml-c2-pliegues", "ml-c2-costo-cv", "ml-c2-anidada"]
DATOS_RAPIDO = ["ml-c2-ajustes-con-prueba", "ml-c2-prueba-ruidosa", "ml-c2-optimismo",
                "ml-c2-prueba-miente", "ml-c2-reparto", "ml-c2-cv-capacidad",
                "ml-c2-pliegue-anomalo", "ml-c2-estratificada"]


def test_el_tramo_rapido_no_trae_figuras_de_la_pagina_3():
    p3 = {"ml-c2-abanico", "ml-c2-diana", "ml-c2-sesgo-varianza",
          "ml-c2-curva-aprendizaje", "ml-c2-diagnostico"}
    assert not p3 & set(fig._RAPIDO)


def test_los_diagramas_del_tramo_rapido_estan_en_el_catalogo():
    assert set(DIAGRAMAS_RAPIDO) <= set(fig._RAPIDO)


@pytest.mark.parametrize("ident", DIAGRAMAS_RAPIDO)
def test_los_diagramas_se_generan_sin_ml_lab(ident):
    codigo = ("import sys; sys.path.insert(0, %r); import gen_aprendizaje_maquina as g; "
              "g.contenido(%r); print('aprendizaje_maquina' in sys.modules)"
              % (str(HERRAMIENTAS), ident))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip().endswith("False"), r.stdout + r.stderr


@pytest.mark.parametrize("ident", ["ml-c2-dos-niveles", "ml-c2-tres-conjuntos",
                                   "ml-c2-pliegues", "ml-c2-anidada"])
def test_validacion_va_en_oro_y_entrenamiento_en_cian(ident):
    c = colores(ident)
    assert gen.color_rol("validacion").lower() in c
    assert gen.color_rol("entrenamiento").lower() in c


@pytest.mark.parametrize("ident", ["ml-c2-tres-conjuntos", "ml-c2-simulacro",
                                   "ml-c2-pliegues"])
def test_la_prueba_va_en_rosa_con_cuadrado(ident):
    assert gen.color_rol("prueba").lower() in colores(ident)
    assert re.search(r'<rect [^>]*fill="%s"' % gen.color_rol("prueba"), contenido(ident))


def test_la_prueba_de_los_pliegues_esta_cerrada_y_aparte():
    a = aria("ml-c2-pliegues")
    assert "cerrada" in a and "exactamente una vez" in a


def test_el_costo_cuenta_m_por_k_mas_uno():
    t = contenido("ml-c2-costo-cv")
    assert "3·5 + 1 = 16" in t and "13·5 + 1 = 66" in t
    assert "66 ajustes" in aria("ml-c2-costo-cv")


def test_el_simulacro_trae_los_cuatro_contratos_en_orden():
    a = aria("ml-c2-simulacro")
    pos = [a.index(c) for c in ("Más de lo mismo", "El mes que viene", "Pacientes nuevos",
                                "Otra ciudad")]
    assert pos == sorted(pos)
    assert "declara el alcance" in a


def test_la_anidada_dice_quien_estima_y_quien_elige():
    t = contenido("ml-c2-anidada")
    assert "Afuera se estima; adentro se elige" in t
    assert "no ve el pliegue externo" in t

# --- fin tramo rapido ---


# --- tramo m ---
# --- fin tramo m ---


# --- tramo completo ---
# --- fin tramo completo ---
