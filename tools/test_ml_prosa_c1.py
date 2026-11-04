"""Pruebas de prosa de la clase 1 (D-003): cada cifra de tools/ml_cifras_c1.py
aparece en la seccion de la pagina que la cita, y las frases fijas de las
rondas 2 y 3 del plan estan donde deben (clase_1.md §10.7).

Lee paginas y guiones, asi que no es parte de S1: corre en S2. Mientras la
pagina no existe (antes de C1.T6) estas pruebas fallan a proposito con
«falta la pagina»: el paso 5 de la validacion de O2 las corre contra el
borrador de Codex antes de aceptarlo.

Anclas por tramo (protocolo p5.2 §7.1): la parte 1b (pagina 2) la agrega la
subrama -b tras su bajada (C1.T13b), antes del «fin» de su tramo.
"""
import re
from functools import lru_cache
from pathlib import Path

import pytest

import ml_cifras_c1 as c

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/2_el_problema"
GUIONES = RAIZ / "tools/cuadernos_ml"


def leer(ruta):
    assert ruta.exists(), f"falta la pagina {ruta.relative_to(RAIZ)} (la redacta Codex)"
    return ruta.read_text(encoding="utf-8")


def secciones(texto):
    """{n: texto de la seccion «## n · …» hasta el siguiente «## »}."""
    partes = re.split(r"(?m)^## ", texto)
    salida = {}
    for p in partes[1:]:
        m = re.match(r"(\d+) · ", p)
        if m:
            salida[int(m.group(1))] = p
    return salida


def bloque(texto, ident):
    """El cuerpo de la directiva ::: … {#ident …} hasta su «:::» de cierre."""
    m = re.search(r"(?ms)^:::[^\n]*\{#" + re.escape(ident) + r"\b[^\n]*\n(.*?)^:::\s*$", texto)
    assert m, f"no hay bloque {{#{ident}}}"
    return m


def parrafo_antes(texto, inicio):
    previo = texto[:inicio].rstrip()
    return previo.split("\n\n")[-1]


def parrafo_despues(texto, fin):
    resto = texto[fin:].lstrip()
    return resto.split("\n\n")[0]


def menos(v, d=1):
    """La forma de un negativo en la pagina: con «−» o con «-»."""
    s = f"{abs(v):.{d}f}"
    return (f"−{s}", f"-{s}")


def alguna(texto, formas):
    return any(f in texto for f in formas)


# --- tramo 1a ---

P1 = CLASE / "1_que_es_f.md"
NB01 = GUIONES / "01_que_es_f.texto.md"


@lru_cache(maxsize=None)
def p1():
    return leer(P1)


@lru_cache(maxsize=None)
def s1():
    return secciones(p1())


def cierre_p1():
    texto = p1()
    i = texto.find("Lo que hay que llevarse")
    assert i >= 0, "P1 no tiene «Lo que hay que llevarse»"
    return texto[i:]


def test_p1_tiene_las_ocho_secciones_del_brief():
    assert sorted(s1()) == list(range(1, 9))


# ---- cifras, una aserción por fila de §10.7 (tramo 1a) ----

def test_p1_s1_cita_el_ganador_a_7_km():
    g = c.cifras_c1_ganador()
    sec = s1()[1]
    assert f"{g['prediccion'][7.0][0]:.1f}" in sec  # 37.4
    assert alguna(sec, menos(g["prediccion"][7.0][1], 0) + menos(g["prediccion"][7.0][1], 1))


def test_p1_s1_micro_cita_las_predicciones_a_35_y_0_km():
    g = c.cifras_c1_ganador()
    sec = s1()[1]
    for km in (3.5, 0.0):
        for v in g["prediccion"][km]:
            assert f"{v:.1f}" in sec, (km, v)


def test_p1_s3_cita_el_mse_de_la_recta_y_el_de_la_recta_fija():
    g = c.cifras_c1_ganador()
    sec = s1()[3]
    assert f"{g['mse_1']:.3f}" in sec       # 0.914
    assert f"{g['rmse_1']:.3f}" in sec      # 0.956


def test_p1_s3_cita_el_error_de_aproximacion_de_la_muestra_enorme():
    p = c.cifras_c1_piso()
    sec = s1()[3]
    ee = p[1.0]["ee_oraculo"]
    assert alguna(sec, (f"{ee:.4f}", f"{ee:.3f}")), "falta el error de aproximación (0.0045 / 0.005)"
    assert "100 000" in sec or "100\\,000" in sec


def test_p1_s4_cita_los_dos_pisos():
    p = c.cifras_c1_piso()
    sec = s1()[4]
    assert "cuadruplica" in sec
    for s in (1.0, 2.0):
        assert re.search(rf"(?<![\d.]){p[s]['piso']:g}(?!\.?\d)", sec), s


def test_p1_s5_cita_el_piso_de_la_lluvia_10_y_1():
    ll = c.cifras_c1_lluvia()
    sec = s1()[5]
    assert re.search(rf"(?<![\d.]){ll['piso_sin_x2']:.0f}(?!\.?\d)", sec)   # 10
    assert re.search(r"10\s*(→|a)\s*1(?!\.?\d)|de 10 a 1(?!\.?\d)", sec), "falta «de 10 a 1»"


def test_p1_s7_cita_los_aciertos_de_los_anillos():
    a = c.cifras_c1_anillos()
    sec = s1()[7]
    assert f"{round(100 * a['polares']['aciertos'])}" in sec          # 75
    assert f"{round(100 * a['bayes'])}" in sec                         # 76
    assert alguna(sec, (f"{round(100 * a['moda'])}", f"{round(100 * a['cartesianas']['aciertos'])}"))
    assert alguna(sec, menos(a["polares"]["beta"]["theta"], 2))       # −0.07


def test_p1_s7_llama_aciertos_a_los_aciertos_nunca_R():
    sec = s1()[7]
    assert "aciertos en el despliegue" in sec
    assert not re.search(r"\$R\$\s*(de|en)\s*(los\s*)?aciertos|aciertos\s*\(\$R\$\)", sec)


def test_p1_cierre_cita_las_cifras_que_hay_que_llevarse():
    g, a = c.cifras_c1_ganador(), c.cifras_c1_anillos()
    cierre = cierre_p1()
    assert f"{g['prediccion'][7.0][0]:.1f}" in cierre
    assert alguna(cierre, menos(g["prediccion"][7.0][1], 0) + menos(g["prediccion"][7.0][1], 1))
    assert f"{round(100 * a['polares']['aciertos'])}" in cierre
    assert "cuadruplica" in cierre


# ---- frases fijas de las rondas 2 y 3 ----

def test_p1_s3_la_frase_del_nombre_va_justo_antes_del_riesgo_y_sin_arroba():
    texto = p1()
    m = bloque(texto, "ml-c1-def-riesgo")
    parrafo = parrafo_antes(texto, m.start())
    for ancla in ("clase 0", "nombre", "riesgo"):
        assert ancla in parrafo, ancla
    assert "@" not in parrafo


def test_p1_s3_la_frase_del_mae_va_justo_despues_del_riesgo():
    texto = p1()
    m = bloque(texto, "ml-c1-def-riesgo")
    parrafo = parrafo_despues(texto, m.end())
    for ancla in ("MAE", "clase 0", "cuadrática"):
        assert ancla in parrafo, ancla


def test_p1_s3_las_dos_estrellas_son_gorro():
    texto = p1()
    m = bloque(texto, "ml-c1-def-estimacion")
    zona = m.group(1) + parrafo_despues(texto, m.end())
    assert "\\beta^\\star" in zona and "\\widehat\\beta" in zona
    assert "(11,\\ 3.6)" in zona or "(11, 3.6)" in zona


def test_p1_avisa_los_subindices_de_x_en_s2_y_en_s8():
    for n in (2, 8):
        sec = s1()[n]
        assert "con la letra $i$" in sec, n
        assert "$x_{ij}$ es la variable $j$ de la observación $i$" in sec, n


def test_p1_ninguna_phi_omite_la_constante():
    for m in re.finditer(r"\\phi(?:_N)?(?:\(x\))?\s*=\s*\(\s*([^,)\s]+)", p1()):
        assert m.group(1) == "1", f"φ sin la constante: {m.group(0)}"


def test_p1_no_cita_ids_de_la_pagina_2_en_la_variante_1a():
    propios = set(re.findall(r"\{#(ml-c1-[a-z0-9-]+)", p1()))
    citados = set(re.findall(r"@(ml-c1-[a-z0-9-]+)", p1()))
    assert citados <= propios, f"@ a ids de la página 2: {sorted(citados - propios)}"


def test_p1_la_optimizacion_no_es_cuarta_ni_quinta_fuente():
    assert not re.search(r"(cuarta|quinta) fuente", p1())


# ---- guion de NB01 ----

@lru_cache(maxsize=None)
def nb01():
    return leer(NB01)


def celda(clave):
    m = re.search(r"(?ms)^### celda: " + re.escape(clave) + r"\s*$(.*?)(?=^### celda: |\Z)",
                  nb01())
    assert m, f"falta la celda {clave}"
    return m.group(1)


def test_nb01_la_frase_de_la_semilla_es_la_del_contrato():
    texto = " ".join(" ".join(celda(k).split()) for k in
                     ("bloque-1-predice", "bloque-1-mira", "bloque-1-explica"))
    assert ("cambia la semilla: la población y $f$ se quedan; cambian los datos, el "
            "ajuste y, con él, su riesgo $R(\\widehat\\beta)$") in texto


def test_nb01_los_puntos_de_realidad_son_observaciones_nuevas():
    assert "observaciones nuevas" in celda("bloque-1-mira")
    assert "prueba" not in celda("bloque-1-mira").lower()


def test_nb01_el_bloque_4_cita_los_aciertos_y_no_los_llama_R():
    a = c.cifras_c1_anillos()
    texto = celda("bloque-4-explica")
    assert f"{round(100 * a['polares']['aciertos'])}" in texto
    assert "aciertos" in texto


def test_nb01_el_ejercicio_del_piso_da_un_cuarto():
    assert "0.25" in celda("ejercicio-piso-respuesta")


def test_nb01_no_lleva_arrobas_ni_wikilinks():
    assert not re.search(r"@ml-|\[\[", nb01())

# --- fin tramo 1a ---


# --- tramo 1b ---
# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---
