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

def test_el_tramo_m_trae_abanico_y_diana_y_nada_del_completo():
    assert list(fig._M) == ["ml-c2-abanico", "ml-c2-diana"]
    assert not {"ml-c2-sesgo-varianza", "ml-c2-curva-aprendizaje",
                "ml-c2-diagnostico"} & set(fig._M)


def test_la_diana_es_el_id_congelado_y_nombra_sesgo_y_desviacion():
    import ml_cifras_c2 as c
    s, t = c.cifras_c2_sesgo_varianza(), aria("ml-c2-diana")
    for N in (1, 12):
        assert fig._num(s[f"diana_{N}"]["desv"]) in t
    assert fig._num(s["f_x0"]) in t and "ninguna predicción queda fuera" in t


def test_cada_cruz_de_la_diana_queda_donde_esta_su_prediccion():
    # figuras.md: «un punto queda donde está su valor»; eje fijo, sin recorte.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import aprendizaje_maquina as ml
    import ml_cifras_c2 as c
    sv = c.sesgo_varianza_hilo()
    fig_, ax = plt.subplots()
    ml.dibujar_diana(sv, c.X0, candidatos=[1, 12], ax=ax, tema="sitio")
    for fila, N in enumerate((1, 12)):
        esperado = np.sort(c._predicciones_en(sv, c.X0, N))
        dibujado = [ln for ln in ax.lines if ln.get_gid() == "repeticion"
                    and abs(np.mean(ln.get_ydata()) - fila) < 0.5]
        assert len(dibujado) == 1
        assert np.allclose(np.sort(dibujado[0].get_xdata()), esperado)
        assert esperado.min() >= c.EJE_DIANA[0] and esperado.max() <= c.EJE_DIANA[1]
    plt.close(fig_)


def test_el_abanico_no_usa_opacidad_para_informar():
    assert "opacity" not in contenido("ml-c2-abanico")
    t = aria("ml-c2-abanico")
    assert "Grado 1" in t and "Grado 12" in t

# --- fin tramo m ---


# --- tramo completo ---

def test_el_tramo_completo_trae_sus_tres_figuras():
    assert list(fig._COMPLETO) == ["ml-c2-sesgo-varianza", "ml-c2-curva-aprendizaje",
                                   "ml-c2-diagnostico"]


def test_el_aria_de_sesgo_y_varianza_nombra_la_estrella_y_el_desglose():
    import ml_cifras_c2 as c
    s, t = c.cifras_c2_sesgo_varianza(), aria("ml-c2-sesgo-varianza")
    N0 = s["N_estrella"]
    assert f"N⋆ = {N0}" in t and fig._num(s[N0]["total"], 2) in t
    assert fig._num(s[0]["ruido"]) in t


def test_cada_punto_de_la_curva_de_aprendizaje_es_su_mediana():
    # «un punto queda donde está su valor»: la ordenada de R en 30, 480 y 960
    # es la mediana de cifras_c2_curva_aprendizaje (si alguien quita
    # resumen="mediana", esta prueba se pone roja)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import aprendizaje_maquina as ml
    import ml_cifras_c2 as c
    a = c.cifras_c2_curva_aprendizaje()
    fig_, ejes = plt.subplots(2, 1)
    ml.dibujar_curva_aprendizaje(c.tabla_curva_aprendizaje(), piso=a["piso"],
                                 elegido=c.tabla_capacidad_elegida(), resumen="mediana",
                                 ax=list(ejes), tema="sitio")
    for N in c.GRADOS_CURVA:
        ln = [x for x in ejes[0].lines if x.get_gid() == f"R-{N}"][0]
        pares = dict(zip(np.asarray(ln.get_xdata(), float), np.asarray(ln.get_ydata(), float)))
        for n in (30, 480, 960):
            assert np.isclose(pares[n], a["R"][(N, n)])
    el = [x for x in ejes[1].lines if x.get_gid() == "elegido"][0]
    pares = dict(zip(np.asarray(el.get_xdata(), float), np.asarray(el.get_ydata(), float)))
    assert pares[30] == a["elegido"][30] and pares[960] == a["elegido"][960]
    plt.close(fig_)
    assert 'resumen="mediana"' in __import__("inspect").getsource(fig.ml_c2_curva_aprendizaje)


def test_el_aria_de_la_curva_nombra_las_medianas_citadas():
    import ml_cifras_c2 as c
    a, t = c.cifras_c2_curva_aprendizaje(), aria("ml-c2-curva-aprendizaje")
    for k in ((1, 30), (1, 480), (1, 960), (10, 480), (10, 960)):
        assert fig._num(a["R"][k]) in t
    assert fig._num(a["R"][(10, 30)]) not in t   # inestable entre semillas: no se cita


def test_el_diagnostico_tiene_las_cinco_hojas_y_las_cuatro_preguntas():
    t = contenido("ml-c2-diagnostico")
    for hoja in ("sobreajuste", "no aprende", "subajuste", "listo", "rehacer la separación"):
        assert hoja in t
    for k in ("1 ·", "2 ·", "3 ·", "4 ·"):
        assert k in t
    assert "falta evidencia" in t and "heurística" in t

# --- fin tramo completo ---
