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

def test_los_datos_del_tramo_rapido_estan_en_el_catalogo():
    assert set(DATOS_RAPIDO) <= set(fig._RAPIDO)
    assert len(fig._RAPIDO) == 14


@pytest.mark.parametrize("ident", ["ml-c2-prueba-miente", "ml-c2-cv-capacidad",
                                   "ml-c2-estratificada"])
def test_los_ids_congelados_existen_tal_cual(ident):
    # contrato §2.3: los cita otra clase (5, 3 y 4); no se renombran
    assert ident in fig._RAPIDO


@pytest.mark.parametrize("ident", ["ml-c2-ajustes-con-prueba", "ml-c2-prueba-ruidosa",
                                   "ml-c2-optimismo", "ml-c2-prueba-miente", "ml-c2-reparto"])
def test_las_graficas_de_prueba_usan_el_rosa_de_prueba(ident):
    assert gen.color_rol("prueba").lower() in colores(ident)


def test_la_cv_lleva_oro_entrenamiento_cian_benchmark_magenta_y_piso():
    c = colores("ml-c2-cv-capacidad")
    for rol in ("validacion", "entrenamiento", "benchmark"):
        assert gen.color_rol(rol).lower() in c, rol
    assert "solo en el simulador" in contenido("ml-c2-cv-capacidad")


def test_el_aria_de_los_ajustes_nombra_las_cifras():
    import ml_cifras_c2 as c
    a, t = c.cifras_c2_ajustes_con_prueba(), aria("ml-c2-ajustes-con-prueba")
    for N in (1, 4):
        assert fig._num(a[N]["L_ent"]) in t and fig._num(a[N]["L_prueba"]) in t
    assert fig._num(a[12]["L_prueba"], 0) in t


def test_el_aria_de_la_prueba_ruidosa_nombra_desviaciones_y_coberturas():
    import ml_cifras_c2 as c
    p, t = c.cifras_c2_prueba_ruidosa(), aria("ml-c2-prueba-ruidosa")
    for n in (20, 200):
        assert fig._num(p[f"desv_{n}"]) in t and fig._pct(p[f"cobertura_{n}"]) in t
    assert fig._num(p["R"]) in t


def test_el_aria_del_optimismo_nombra_el_sesgo_y_los_porcentajes():
    import ml_cifras_c2 as c
    o, t = c.cifras_c2_optimismo(), aria("ml-c2-optimismo")
    assert fig._num(o["sesgo_prueba"]) in t
    assert fig._pct(o["optimistas_prueba"]) in t and fig._pct(o["optimistas_validacion"]) in t
    assert "sin reajuste" in contenido("ml-c2-optimismo")


def test_la_figura_de_contratos_dibuja_las_cifras_de_imitar():
    import ml_cifras_c2 as c
    t = fig.tabla_contratos()
    i = c.cifras_c2_imitar()
    fila = t[(t["contrato"] == "el mes que viene") & (t["separacion"] == "al azar")].iloc[0]
    assert fila["L_prueba"] == i["el mes que viene"]["azar"]["L_prueba"]
    assert list(dict.fromkeys(t["contrato"])) == list(c.CONTRATOS)
    a = aria("ml-c2-prueba-miente")
    for ct in c.CONTRATOS:
        assert fig._num(i[ct]["azar"]["R"]) in a


def test_el_aria_del_reparto_nombra_los_tres_extremos():
    import ml_cifras_c2 as c
    r, t = c.cifras_c2_reparto(), aria("ml-c2-reparto")
    for f in (0.1, 0.2, 0.5):
        assert fig._num(r[f]["R"]) in t and fig._num(r[f]["desv_error"]) in t


def test_el_aria_de_la_cv_nombra_los_elegidos_y_el_umbral():
    import ml_cifras_c2 as c
    h, t = c.cifras_c2_hilo(), aria("ml-c2-cv-capacidad")
    assert f"N = {h['N_min']}" in t and fig._num(h["umbral"], 2) in t
    assert fig._num(h["cv"][h["N_min"]], 2) in t


def test_el_pliegue_anomalo_rotula_un_pliegue_con_entrega_lejana():
    import ml_cifras_c2 as c
    p = c.cifras_c2_pliegue_anomalo()
    assert f"pliegue {p[8]['pliegue_max']}" in contenido("ml-c2-pliegue-anomalo")


def test_la_estratificada_nombra_las_dos_fracciones():
    import ml_cifras_c2 as c
    e, t = c.cifras_c2_estratificada(), aria("ml-c2-estratificada")
    assert fig._pct(e["azar"]) in t and fig._pct(e["estratificada"]) in t

# --- fin tramo rapido ---


# --- tramo m ---
# --- fin tramo m ---


# --- tramo completo ---
# --- fin tramo completo ---
