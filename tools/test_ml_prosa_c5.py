"""Pruebas de prosa de la clase 5 (D-003; clase_5.md §10.7, §10.11).

Cada cifra de tools/ml_cifras_c5.py que una página cita aparece en esa página
con su forma literal («cita»; la tabla de qué cifra va en qué página es
PAGINA_DE); cada figura de FIGURAS_C5 vive en un `::: figure` de la clase; los
guiones de los cuatro notebooks no tienen secciones vacías; las cantidades de
escenario (ml_cifras_c5.ESCENARIOS) aparecen en el enunciado que las usa; y las
guardas de frase del plan: ningún $R$ junto a MCC, ninguna fecha (D-008),
ninguna cifra de los insumos (D-009.6), la línea literal de conformal con grupos.

Lee páginas y guiones, así que no es parte de S1: corre en S2 y en la
validación de cada borrador de Codex (C5.T12). Mientras una página no existe,
sus pruebas fallan a propósito con «falta … (la redacta Codex)».
"""
import json
import re
from functools import lru_cache
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

from figuras_ml_c5 import FIGURAS_C5  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/6_supuestos_y_metodologia"
GUIONES = RAIZ / "tools/cuadernos_ml"
CITAS = json.loads((RAIZ / "tools/datos/citas_c5.json").read_text(encoding="utf-8"))

P1 = CLASE / "1_son_iid_y_fugas.md"
P2 = CLASE / "2_la_metodologia.md"
TAREA = CLASE / "3_tarea.md"
INDICE = CLASE / "0_index.md"
STEMS = ("10_son_iid_y_fugas", "tarea_5a_series_de_tiempo", "tarea_5b_fugas",
         "tarea_5c_otras_familias")

# Qué cifras cita cada página (rutas dentro de CITAS: función/clave/subclave).
PAGINA_DE = {
    P1: ["cifras_c5_ks_a_mano/ks", "cifras_c5_autocorrelacion/alterna",
         "cifras_c5_cv_miente/c14_clase2/azar", "cifras_c5_cv_miente/c14_clase2/R",
         "cifras_c5_cv_miente/c14_lineal/azar", "cifras_c5_cv_miente/c14_lineal/R",
         "cifras_c5_fugas/posterior/cv", "cifras_c5_fugas/posterior/uso",
         "cifras_c5_fugas/seleccion_previa/cv", "cifras_c5_fugas/seleccion_previa/uso",
         "cifras_c5_imputacion/L_sin", "cifras_c5_imputacion/L_con"],
    P2: ["cifras_c5_depurar/mse_recta", "cifras_c5_arbol/mcc/1", "cifras_c5_arbol/mcc/6",
         "cifras_c5_familias/profundidad", "cifras_c5_cybenko/n_polar",
         "cifras_c5_cybenko/n_aprendida"],
}


@lru_cache(maxsize=None)
def leer(ruta):
    assert ruta.exists(), f"falta {ruta.relative_to(RAIZ)} (la redacta Codex)"
    return ruta.read_text(encoding="utf-8")


def cita(ruta):
    v = CITAS
    for k in ruta.split("/"):
        v = v[k]
    return v


def formas(cifra):
    s = str(cifra)
    out = {s, s.replace("−", "-"), s.replace("-", "−")}
    if s.endswith(" %"):
        out |= {s.replace(" %", " %"), s.replace(" %", "%")}
    return out


CASOS = [(p, r) for p, rutas in PAGINA_DE.items() for r in rutas]


@pytest.mark.parametrize("pagina,ruta", CASOS, ids=[f"{p.stem}:{r}" for p, r in CASOS])
def test_cada_cifra_citada_aparece_en_su_pagina(pagina, ruta):
    texto = leer(pagina)
    assert any(f in texto for f in formas(cita(ruta))), (
        f"{pagina.name} no cita {ruta} = {cita(ruta)!r}")


@pytest.mark.parametrize("ident", list(FIGURAS_C5))
def test_cada_figura_vive_en_un_figure_de_la_clase(ident):
    textos = "\n".join(leer(p) for p in (P1, P2))
    assert re.search(r"(?m)^:::\s*figure\s*\{#" + re.escape(ident) + r"\b", textos), (
        f"{ident} no está en ningún ::: figure de la clase")


@pytest.mark.parametrize("stem", STEMS)
def test_cada_guion_existe_y_no_tiene_secciones_vacias(stem):
    texto = leer(GUIONES / f"{stem}.texto.md")
    partes = re.split(r"(?m)^### celda: [a-z0-9-]+\s*$", texto)[1:]
    assert partes and all(p.strip() for p in partes)


def test_escenarios_del_final_de_p1():
    t = leer(P1)
    for cifra in ("ocho semanas", "3 000", "400 clientes", "60"):
        assert cifra in t


def test_escenarios_del_final_de_p2():
    t = leer(P2)
    assert "2 000 pedidos" in t and "300 clientes" in t


def test_ningun_r_junto_a_mcc():
    for p in (P1, P2):
        for linea in leer(p).splitlines():
            if "MCC" in linea:
                assert not re.search(r"\$R\$|\bR \(despliegue\)", linea), linea


def test_sin_fechas_ni_cifras_de_los_insumos():
    for p in (P1, P2, TAREA, INDICE):
        t = leer(p)
        assert not re.search(r"\b(lunes|martes|miércoles|jueves|viernes|noviembre|"
                             r"diciembre)\b", t, re.I)
        for prohibida in ("162", "331", "Lending Club", "AutoGluon"):
            assert prohibida not in t


def test_conformal_con_grupos_literal():
    t = leer(P1)
    assert ("Con grupos, apartar la calibración por grupos es necesario, pero no basta"
            in re.sub(r"\s+", " ", t))


def test_la_tarea_dice_quien_da_la_fecha():
    assert "la fecha la da el profesor" in leer(TAREA)
