"""Pruebas propias de las figuras de la clase 1 (tools/figuras_ml_c1.py).

Sin prosa (D-003). Las guardas comunes (test_9, XML, ancho, letra, opacidad,
determinismo, creditos, huerfanos, figura<->pagina) viven en
tools/test_gen_aprendizaje_maquina.py. Aqui: el catalogo de la clase, los
roles de la leyenda unica (contrato §7.3) y que el texto alternativo nombre
las cifras que salen de tools/ml_cifras_c1.py.

Anclas por tramo (protocolo p5.2 §7.1): cada rama agrega sus pruebas solo
antes del «fin» de su tramo.
"""
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import figuras_ml_c1 as fig

HERRAMIENTAS = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def contenido(ident):
    return gen.contenido(ident)


def aria(ident):
    return re.search(r'aria-label="([^"]*)"', contenido(ident)).group(1)


def colores(ident):
    return {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", contenido(ident))}


# --- tramo 1a ---

TRAMO_1A = ["ml-c1-ganador-imposible", "ml-c1-mismo-mundo", "ml-c1-reducible",
            "ml-c1-aprender-es-minimizar", "ml-c1-piso", "ml-c1-dos-franjas",
            "ml-c1-cuatro-fuentes", "ml-c1-anillos-polares", "ml-c1-matriz-phi"]
DIAGRAMAS_1A = ["ml-c1-reducible", "ml-c1-cuatro-fuentes", "ml-c1-matriz-phi"]
DATOS_1A = [i for i in TRAMO_1A if i not in DIAGRAMAS_1A]


def test_el_tramo_1a_trae_las_nueve_figuras_de_p1_en_orden():
    assert list(fig._TRAMO_1A) == TRAMO_1A


def test_el_catalogo_es_la_suma_de_los_tramos():
    assert fig.FIGURAS_C1 == {**fig._TRAMO_1A, **fig._TRAMO_1B, **fig._TRAMO_TAREA}


def test_importar_las_figuras_no_importa_ml_lab_ni_matplotlib():
    codigo = ("import sys; sys.path.insert(0, %r); import figuras_ml_c1; "
              "print('aprendizaje_maquina' in sys.modules, 'matplotlib' in sys.modules)"
              % str(HERRAMIENTAS))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip() == "False False", r.stdout + r.stderr


@pytest.mark.parametrize("ident", DIAGRAMAS_1A)
def test_los_diagramas_se_generan_sin_ml_lab(ident):
    codigo = ("import sys; sys.path.insert(0, %r); import gen_aprendizaje_maquina as g; "
              "g.contenido(%r); print('aprendizaje_maquina' in sys.modules)"
              % (str(HERRAMIENTAS), ident))
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    assert r.stdout.strip().endswith("False"), r.stdout + r.stderr


@pytest.mark.parametrize("ident", TRAMO_1A)
def test_ninguna_figura_de_la_clase_1_usa_el_rosa_de_prueba(ident):
    # La prueba no existe hasta la clase 2 (contrato §7.3, r1-02).
    assert gen.color_rol("prueba").lower() not in colores(ident)


@pytest.mark.parametrize("ident", TRAMO_1A)
def test_ninguna_figura_de_la_clase_1_usa_el_oro_de_validacion(ident):
    # Tampoco hay validacion en la clase 1; dibujar_frontera pinta y = 1 con
    # el rol de validacion y la figura lo restila (revision codex-rev-codigo-c1-r1).
    assert gen.color_rol("validacion").lower() not in colores(ident)


@pytest.mark.parametrize("ident", ["ml-c1-mismo-mundo"])
def test_los_casos_no_vistos_llevan_el_rol_observaciones_nuevas(ident):
    texto = contenido(ident)
    assert gen.color_rol("observaciones_nuevas").lower() in colores(ident)
    assert "observaciones nuevas" in texto


def test_el_piso_lleva_el_rol_piso_y_la_media_el_rol_benchmark():
    c = colores("ml-c1-piso")
    assert gen.color_rol("piso_bayes").lower() in c
    assert gen.color_rol("benchmark").lower() in c
    assert "benchmark" in contenido("ml-c1-piso")


@pytest.mark.parametrize("ident", ["ml-c1-mismo-mundo", "ml-c1-dos-franjas",
                                   "ml-c1-reducible", "ml-c1-cuatro-fuentes"])
def test_f_verdadera_va_en_verde_grueso(ident):
    assert gen.color_rol("f_verdadera").lower() in colores(ident)


@pytest.mark.parametrize("ident", DATOS_1A)
def test_las_graficas_de_datos_marcan_el_entrenamiento_en_cian(ident):
    assert gen.color_rol("entrenamiento").lower() in colores(ident)


def test_el_aria_del_ganador_nombra_las_cifras():
    import ml_cifras_c1 as c
    g = c.cifras_c1_ganador()
    a = aria("ml-c1-ganador-imposible")
    assert f"{g['prediccion'][7.0][0]:.1f}" in a and "37.4" in a
    assert "−25.0" in a
    # Sin la respuesta del ejercicio ml-c1-ej-ganador (a): un lector de pantalla
    # lee el alt antes de que el alumno lo intente (revision r3).
    assert "24.0" not in a and "3.5 km" not in a


def test_la_matriz_phi_dice_que_es_cada_dimension():
    t = contenido("ml-c1-matriz-phi")
    assert " por 2<" not in t and " por 3<" not in t
    assert t.count("entradas") >= 3 and t.count("una por entrega") >= 3


def test_el_aria_del_piso_nombra_las_cifras():
    import ml_cifras_c1 as c
    p = c.cifras_c1_piso()
    a = aria("ml-c1-piso")
    for s in (1.0, 2.0):
        assert f"{p[s]['R_oraculo']:.2f}" in a
        assert f"{p[s]['R_recta']:.2f}" in a
        assert f"{p[s]['R_media']:.1f}" in a


def test_el_aria_de_los_anillos_nombra_las_cifras():
    import ml_cifras_c1 as c
    an = c.cifras_c1_anillos()
    a = aria("ml-c1-anillos-polares")
    for v in (an["cartesianas"]["aciertos"], an["polares"]["aciertos"], an["moda"],
              an["bayes"]):
        assert f"{round(100 * v)} %" in a
    assert f"{an['radio_bayes']:.2f}" in a
    assert "−0.07" in a
    # Aciertos, nunca R (contrato §4.8, r1-23).
    assert "riesgo" not in a.lower()


def test_el_aria_del_piso_no_dice_que_la_estimacion_nunca_baja_del_piso():
    a = aria("ml-c1-piso")
    assert "ni el oráculo baja" not in a
    assert "un poco abajo" in a


def test_el_aria_de_la_lluvia_nombra_los_dos_pisos():
    a = aria("ml-c1-dos-franjas")
    assert "piso es 10" in a and "baja a 1" in a


def test_el_aria_de_aprender_es_minimizar_nombra_la_pendiente():
    import aprendizaje_maquina as ml
    import ml_cifras_c1 as c
    m = ml.ajustar(c.datos_entregas())
    assert f"{float(m.beta_gorro['x']):.2f}" in aria("ml-c1-aprender-es-minimizar")


def test_la_matriz_phi_trae_las_tres_phi_con_la_columna_de_unos():
    t = contenido("ml-c1-matriz-phi")
    for v in ("1/6", "36", "x²", "q = 2", "q = 3"):
        assert v in t
    assert t.count(">1<") >= 18  # seis unos por cada una de las tres Φ


def test_el_sin_opacidad_hornea_contra_el_panel():
    entrada = '<rect style="fill: #ffffff; fill-opacity: 0.5"/><path style="fill: #000000; opacity: 0.25; stroke: #ffffff"/>'
    salida = fig._sin_opacidad(entrada)
    assert "opacity" not in salida
    assert gen.mezclar("#ffffff", 0.5, gen.PANEL) in salida
    assert gen.mezclar("#000000", 0.25, gen.PANEL) in salida
    assert gen.mezclar("#ffffff", 0.25, gen.PANEL) in salida

# --- fin tramo 1a ---


# --- tramo 1b ---

TRAMO_1B = ["ml-c1-taylor-vs-mco", "ml-c1-weierstrass", "ml-c1-tres-ajustes",
            "ml-c1-capacidad-brecha", "ml-c1-elegir-con-entrenamiento",
            "ml-c1-inverso-vs-potencias", "ml-c1-extrapolar", "ml-c1-no-free-lunch"]


def test_el_tramo_1b_trae_las_ocho_figuras_de_p2_en_orden():
    assert list(fig._TRAMO_1B) == TRAMO_1B


@pytest.mark.parametrize("ident", TRAMO_1B)
def test_ninguna_figura_1b_usa_el_rosa_de_prueba_ni_el_oro_de_validacion(ident):
    c = colores(ident)
    assert gen.color_rol("prueba").lower() not in c
    assert gen.color_rol("validacion").lower() not in c


@pytest.mark.parametrize("ident", [i for i in TRAMO_1B if i != "ml-c1-no-free-lunch"])
def test_las_figuras_1b_de_regresion_traen_la_f_verdadera_o_el_entrenamiento(ident):
    c = colores(ident)
    assert gen.color_rol("f_verdadera").lower() in c or \
        gen.color_rol("entrenamiento").lower() in c


def test_tres_ajustes_dibuja_observaciones_nuevas_con_su_rol():
    assert gen.color_rol("observaciones_nuevas").lower() in colores("ml-c1-tres-ajustes")
    assert "observaciones nuevas" in contenido("ml-c1-tres-ajustes")


@pytest.mark.parametrize("ident", ["ml-c1-capacidad-brecha", "ml-c1-inverso-vs-potencias"])
def test_capacidad_e_inverso_llevan_piso_y_benchmark_con_sus_roles(ident):
    c = colores(ident)
    assert gen.color_rol("piso_bayes").lower() in c
    assert gen.color_rol("benchmark").lower() in c
    assert "benchmark" in contenido(ident)


def test_el_aria_de_taylor_nombra_el_error_en_2_5():
    import ml_cifras_c1 as cif
    t = cif.cifras_c1_taylor()
    a = aria("ml-c1-taylor-vs-mco")
    assert f"{t['taylor_3'][2.5]:.1f}" in a and f"{t['taylor_9'][2.5]:.1f}" in a


def test_el_aria_de_weierstrass_nombra_los_tres_errores():
    import ml_cifras_c1 as cif
    w = cif.cifras_c1_weierstrass()
    a = aria("ml-c1-weierstrass")
    assert all(f"{w[N]['error_maximo']:.3f}" in a for N in (2, 6, 14))


def test_el_aria_de_la_capacidad_nombra_el_optimo_y_el_contraste():
    import ml_cifras_c1 as cif
    k = cif.cifras_c1_capacidad()
    a = aria("ml-c1-capacidad-brecha")
    assert f"grado {k[20]['N_menor_R']}" in a
    assert f"{k[20]['R'][15]:.0f}" in a and "200 datos" in a
    assert "no una ley" in a


def test_el_aria_de_elegir_nombra_las_200_y_el_maximo():
    import ml_cifras_c1 as cif
    e = cif.cifras_c1_elegir()
    a = aria("ml-c1-elegir-con-entrenamiento")
    assert f"{e['veces_N_max_ent']} de {e['repeticiones']}" in a


def test_el_aria_del_inverso_nombra_los_cuatro_riesgos():
    import ml_cifras_c1 as cif
    i = cif.cifras_c1_inverso()
    a = aria("ml-c1-inverso-vs-potencias")
    for clave, d in (("R_1", 1), ("R_4", 1), ("R_10", 2), ("R_inverso", 2)):
        assert f"{i[clave]:.{d}f}" in a, clave


def test_el_aria_de_extrapolar_nombra_el_recursivo():
    import ml_cifras_c1 as cif
    r = cif.cifras_c1_extrapolar()["recursivo"]
    a = aria("ml-c1-extrapolar")
    assert f"{r['sin_anterior']['futuro']:.1f}" in a
    assert f"{r['con_anterior']['futuro']:.2f}" in a


def test_el_aria_de_no_free_lunch_dice_la_mitad_exacta():
    a = aria("ml-c1-no-free-lunch")
    assert "256" in a and "exactamente la mitad" in a

# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---


def test_r2_extrapolar_solo_el_modelo_con_el_anterior_va_a_un_paso():
    # La recta en x no usa el valor anterior: «a un paso» no le aplica (r2 1b).
    a = aria("ml-c1-extrapolar")
    assert "recta en x, a un paso" not in contenido("ml-c1-extrapolar")
    assert "y en el futuro, " in a and "como columna, a un paso, queda en" in a


def test_r2_inverso_nombra_los_datos_fuera_del_cuadro():
    import ml_cifras_c1 as cif
    altos = cif.cifras_c1_inverso()["fuera_del_cuadro"]
    assert f"con y de {altos[0]:.0f} y {altos[1]:.0f}, quedan arriba del cuadro" in aria(
        "ml-c1-inverso-vs-potencias")


def test_r3_taylor_y_tres_ajustes_no_dejan_puntos_fuera_del_cuadro():
    # Con tope 16 quedaban fuera, sin marca, dos datos de entrenamiento y 6 de
    # las 200 observaciones nuevas (r3 del tramo 1b).
    import ml_cifras_c1 as cif
    datos = cif.datos_inverso()
    nuevas = datos.realidad.iloc[:200]
    assert max(datos.ent.y.max(), nuevas.y.max()) < cif.P2_YTOPE
    assert min(datos.ent.y.min(), nuevas.y.min()) > 0
    fuente = (HERRAMIENTAS / "figuras_ml_c1.py").read_text(encoding="utf-8")
    assert "ax.set_ylim(0, cif.P2_YTOPE)" in fuente and "tope = cif.P2_YTOPE" in fuente
    assert "set_ylim(0, 16)" not in fuente and "tope = 16" not in fuente
