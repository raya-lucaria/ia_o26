"""Pruebas de prosa de la clase 2 (D-003, D-009.5): cada cifra de
tools/ml_cifras_c2.py que cita una pagina o un guion aparece en la seccion
que la cita, y cada figura del catalogo de la clase vive en una pagina
dentro de su `::: figure {#id …}`.

Lee paginas y guiones, asi que no es parte de S1: corre en S2. Mientras una
pagina no existe, sus pruebas fallan a proposito con «falta la pagina».

Anclas por tramo (protocolo p5.2 §7.1): la rama de clase escribe el tramo
rapido; la subrama -m agrega su parte tras su bajada; la -completo, la suya.
"""
import re
from functools import lru_cache
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c2 as c  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/3_separar_los_datos"
GUIONES = RAIZ / "tools/cuadernos_ml"


def leer(ruta):
    assert ruta.exists(), f"falta la pagina {ruta.relative_to(RAIZ)} (la redacta Codex)"
    return ruta.read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def texto(nombre):
    return leer(CLASE / nombre if nombre.endswith(".md") and "/" not in nombre
                else RAIZ / nombre)


def secciones(t):
    """{n: texto de la seccion «## n · …» hasta el siguiente «## »}."""
    salida = {}
    for p in re.split(r"(?m)^## ", t)[1:]:
        m = re.match(r"(\d+) · ", p)
        if m:
            salida[int(m.group(1))] = p
    return salida


def seccion(nombre, n):
    s = secciones(texto(nombre))
    assert n in s, f"{nombre} no tiene la seccion «## {n} · …»"
    return s[n]


def llevarse(nombre):
    t = texto(nombre)
    i = t.find("Lo que hay que llevarse")
    assert i >= 0, f"{nombre} no tiene «Lo que hay que llevarse»"
    return t[i:]


def formas(v, d=1):
    """Un numero como puede escribirlo la pagina: punto decimal, signo «−» o «-»."""
    s = f"{abs(v):.{d}f}"
    return (s,) if v >= 0 else (f"−{s}", f"-{s}", s)


def esta(v, t, d=1):
    return any(f in t for f in formas(v, d))


def figuras_en(nombre):
    return set(re.findall(r"(?m)^:::\s*figure\s*\{#(ml-c2-[a-z0-9-]+)", texto(nombre)))


# --- tramo rapido ---

P1, P2, TAREA = "1_entrenamiento_y_prueba.md", "2_validacion_cruzada.md", "4_tarea.md"
G03 = "tools/cuadernos_ml/03_entrenamiento_y_prueba.texto.md"
G04 = "tools/cuadernos_ml/04_validacion_cruzada.texto.md"


def test_p1_la_prueba_ruidosa_en_su_seccion():
    pr = c.cifras_c2_prueba_ruidosa()
    s3 = seccion(P1, 3)
    for k in ("R", "desv_20", "desv_200"):
        assert esta(pr[k], s3), k


def test_p1_el_engano_de_elegir_con_la_prueba_en_su_seccion():
    op = c.cifras_c2_optimismo()
    s4 = seccion(P1, 4)
    assert esta(op["sesgo_prueba"], s4) and esta(op["ee_prueba"], s4)
    assert f"{100 * op['optimistas_prueba']:.0f} %" in s4
    assert esta(op["sesgo_prueba"], llevarse(P1))


def test_p1_el_reparto_en_su_seccion():
    rp = c.cifras_c2_reparto()
    s6 = seccion(P1, 6)
    for f in (0.1, 0.5):
        assert esta(rp[f]["R"], s6) and esta(rp[f]["desv_error"], s6), f


def test_p2_la_cv_del_hilo_y_el_umbral_en_su_seccion():
    h = c.cifras_c2_hilo()
    s3 = seccion(P2, 3)
    assert esta(h["cv"][h["N_min"]], s3, 2) and esta(h["umbral"], s3, 2)
    assert esta(h["cv"][h["N_min"]], llevarse(P2), 2)


def test_p2_la_estratificada_en_su_seccion():
    e = c.cifras_c2_estratificada()
    assert f"{100 * e['azar']:.0f} %" in seccion(P2, 5)


def test_p2_la_anidada_en_su_seccion():
    an = c.cifras_c2_anidada()
    s6 = seccion(P2, 6)
    for k in ("cv_ganador", "anidada", "R_procedimiento"):
        assert esta(an[k], s6), k


def test_guion_03_cita_las_cifras_de_la_prueba_ruidosa_y_del_engano():
    pr, op = c.cifras_c2_prueba_ruidosa(), c.cifras_c2_optimismo()
    g = texto(G03)
    assert esta(pr["R"], g, 2) and esta(pr["desv_20"], g, 2)
    assert esta(op["sesgo_prueba"], g, 2)


def test_guion_04_cita_la_cv_del_hilo():
    h = c.cifras_c2_hilo()
    assert esta(h["cv"][h["N_min"]], texto(G04), 2)


def test_cada_figura_del_tramo_rapido_vive_en_un_figure_de_p1_o_p2():
    import figuras_ml_c2 as fig
    usadas = figuras_en(P1) | figuras_en(P2)
    assert set(fig._RAPIDO) <= usadas, set(fig._RAPIDO) - usadas


def test_la_tarea_no_lleva_respuestas_ni_explica():
    t = texto(TAREA)
    assert "::: answer" not in t and "-explica" not in t

# --- fin tramo rapido ---


# --- tramo m ---
# --- fin tramo m ---


# --- tramo completo ---
# --- fin tramo completo ---
