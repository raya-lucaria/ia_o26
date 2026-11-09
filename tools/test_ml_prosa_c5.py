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


# Cada cifra citada, atada a la frase que la cita. La prueba de arriba solo busca
# la cifra en algún lugar de la página: «0.21» o «3» aparecen en muchas frases, así
# que cambiar un número en una tabla o intercambiar ganador y perdedor pasaba. Aquí
# cada plantilla es la frase literal con {función/clave/...} en lugar de la cifra;
# se compara sin espacios, porque Markdown parte las frases donde quiere.
ANCLAS = {
    P1: [
        "Con$\\bar o={cifras_c5_adversarial/o_bar}$",
        "contra la entropía {cifras_c5_adversarial/benchmark_formula}:",
        "|Sin deriva|{cifras_c5_adversarial/nada_bosque/log_loss}|Sin señal|",
        "|Con deriva|{cifras_c5_adversarial/deriva_bosque/log_loss}|Señal|",
        "|Mismas marginales|{cifras_c5_adversarial/control/mcc_05}"
        "|{cifras_c5_adversarial/control/mcc_obar}|",
        "|Deriva fuerte|{cifras_c5_adversarial/control/deriva_mcc_05}"
        "|{cifras_c5_adversarial/control/deriva_mcc_obar}|",
        "(pérdida logarítmica {cifras_c5_adversarial/nada_bosque/log_loss} contra "
        "{cifras_c5_adversarial/benchmark_formula}, sin señal)",
        "(rezago 1: {cifras_c5_autocorrelacion/rezago1_sin})",
        "la adversarial baja a {cifras_c5_adversarial/deriva_bosque/log_loss} (señal)",
        "(rezago 1: {cifras_c5_autocorrelacion/rezago1_con})",
        "da ${cifras_c5_autocorrelacion/alterna}$, frente a "
        "${cifras_c5_autocorrelacion/pearson}$ de Pearson",
        "las escaleras valen ${cifras_c5_ks_a_mano/Fa}$ y ${cifras_c5_ks_a_mano/Fb}$",
        "La mayor diferencia es ${cifras_c5_ks_a_mano/ks}$",
        "la CV al azar promete {cifras_c5_cv_miente/c14_clase2/azar} con clientes que "
        "repiten y los clientes nuevos dan {cifras_c5_cv_miente/c14_clase2/R}; en días "
        "seguidos, {cifras_c5_cv_miente/c13_clase2/azar} contra "
        "{cifras_c5_cv_miente/c13_clase2/R}. Con el lineal en x, "
        "{cifras_c5_cv_miente/c14_lineal/azar} contra {cifras_c5_cv_miente/c14_lineal/R} "
        "y {cifras_c5_cv_miente/c13_lineal/azar} contra {cifras_c5_cv_miente/c13_lineal/R}",
        "|Clientes nuevos|Polinomio y dummies del cliente|"
        "{cifras_c5_cv_miente/c14_clase2/azar}|{cifras_c5_cv_miente/c14_clase2/R}|",
        "|Clientes nuevos|Lineal en $x$|{cifras_c5_cv_miente/c14_lineal/azar}|"
        "{cifras_c5_cv_miente/c14_lineal/R}|",
        "|Días futuros|Vecinos sobre $(x,t)$|{cifras_c5_cv_miente/c13_clase2/azar}|"
        "{cifras_c5_cv_miente/c13_clase2/R}|",
        "|Días futuros|Lineal en $x$|{cifras_c5_cv_miente/c13_lineal/azar}|"
        "{cifras_c5_cv_miente/c13_lineal/R}|",
        "Sin fuga, la CV promete un MCC de {cifras_c5_fugas/ninguna/cv} y en el "
        "despliegue da {cifras_c5_fugas/ninguna/uso}. Con la calificación la CV promete "
        "{cifras_c5_fugas/posterior/cv} y en el despliegue da "
        "{cifras_c5_fugas/posterior/uso}; escalar e imputar antes, "
        "{cifras_c5_fugas/preprocesar_antes/cv} contra "
        "{cifras_c5_fugas/preprocesar_antes/uso}; pedidos duplicados, "
        "{cifras_c5_fugas/duplicados/cv} contra {cifras_c5_fugas/duplicados/uso}; elegir "
        "variables antes (500 columnas de ruido, 100 pedidos), "
        "{cifras_c5_fugas/seleccion_previa/cv} contra {cifras_c5_fugas/seleccion_previa/uso}",
        "mejora aparente en {cifras_c5_fugas/caso20/optimistas} semillas; diferencia "
        "mediana {cifras_c5_fugas/caso20/mediana_dif}",
        "Imputar con la mediana ({cifras_c5_imputacion/mediana} km) deja un pico con el "
        "{cifras_c5_imputacion/pico} de las filas; con la indicadora, el error en "
        "validación baja de {cifras_c5_imputacion/L_sin} a {cifras_c5_imputacion/L_con}",
        "tuerce la pendiente de distancia a {cifras_c5_imputacion/pendiente_centinela}, "
        "contra {cifras_c5_imputacion/pendiente_mediana} con la mediana",
        "|Seleccionar variables|{cifras_c5_tuberia/seleccion/sin}|"
        "{cifras_c5_tuberia/seleccion/con}|{cifras_c5_tuberia/seleccion/uso}|",
        "|Escalar e imputar|{cifras_c5_tuberia/preprocesar/sin}|"
        "{cifras_c5_tuberia/preprocesar/con}|{cifras_c5_tuberia/preprocesar/uso}|",
        "La adversarial da pérdida {cifras_c5_adversarial/nada_bosque/log_loss} sin "
        "deriva y {cifras_c5_adversarial/deriva_bosque/log_loss} con deriva, frente a "
        "{cifras_c5_adversarial/benchmark_formula}",
        "clientes que repiten dan {cifras_c5_cv_miente/c14_clase2/azar} en CV al azar y "
        "{cifras_c5_cv_miente/c14_clase2/R} en clientes nuevos; el lineal, "
        "{cifras_c5_cv_miente/c14_lineal/azar} y {cifras_c5_cv_miente/c14_lineal/R}",
        "Calificación posterior: MCC {cifras_c5_fugas/posterior/cv} en CV y "
        "{cifras_c5_fugas/posterior/uso} en despliegue; duplicados: "
        "{cifras_c5_fugas/duplicados/cv} y {cifras_c5_fugas/duplicados/uso}",
        "La selección previa pasa de {cifras_c5_tuberia/seleccion/sin} a "
        "{cifras_c5_tuberia/seleccion/con} en CV",
    ],
    P2: [
        "rango {cifras_c5_dummy/rango}",
        "el intercepto puede pasar de {cifras_c5_dummy/b1/0} a {cifras_c5_dummy/b2/0} sin "
        "cambiar las predicciones",
        "una predicción de {cifras_c5_dummy/yh/0} minutos",
        "error cuadrático de entrenamiento {cifras_c5_diagnostico/L_ent}, CV al azar "
        "{cifras_c5_diagnostico/azar} y CV por grupos {cifras_c5_diagnostico/grupos}",
        "La CV al azar da {cifras_c5_diagnostico/azar} minutos cuadrados; por grupos da "
        "{cifras_c5_diagnostico/grupos}",
        "no baja de {cifras_c5_depurar/mse_recta} de error cuadrático medio",
        "MCC en validación de {cifras_c5_arbol/mcc/1}, {cifras_c5_arbol/mcc/3} y "
        "{cifras_c5_arbol/mcc/6}. La logística lineal obtiene {cifras_c5_arbol/logistica}",
        "mejora su MCC de {cifras_c5_arbol/mcc/1} a {cifras_c5_arbol/mcc/6}. La logística "
        "obtiene {cifras_c5_arbol/logistica}",
        "la fórmula da {cifras_c5_bagging/formula} y la varianza medida del promedio, "
        "{cifras_c5_bagging/simulada}",
        "La CV elige profundidad {cifras_c5_familias/profundidad} y "
        "{cifras_c5_familias/etapas} etapas. Con 10 y 200 árboles, el bosque da medianas "
        "de {cifras_c5_familias/bosque_10} y {cifras_c5_familias/bosque_200}; el rango "
        "entre semillas baja de {cifras_c5_familias/rango_10} a "
        "{cifras_c5_familias/rango_200}",
        "la CV elige profundidad {cifras_c5_familias/profundidad} y "
        "{cifras_c5_familias/etapas} etapas de boosting",
        "cambia la mediana de {cifras_c5_familias/bosque_10} a "
        "{cifras_c5_familias/bosque_200} minutos cuadrados. El rango entre semillas baja "
        "de {cifras_c5_familias/rango_10} a {cifras_c5_familias/rango_200}",
        "dan errores máximos de {cifras_c5_cybenko/error/1}, {cifras_c5_cybenko/error/3} "
        "y {cifras_c5_cybenko/error/10}",
        "con {cifras_c5_cybenko/n_polar} filas; diez unidades aprendidas, con "
        "{cifras_c5_cybenko/n_aprendida}. El piso es {cifras_c5_cybenko/piso}",
        "los errores máximos con 1, 3 y 10 unidades son {cifras_c5_cybenko/error/1}, "
        "{cifras_c5_cybenko/error/3} y {cifras_c5_cybenko/error/10}",
        "el piso de pérdida logarítmica es {cifras_c5_cybenko/piso}",
        "del piso con {cifras_c5_cybenko/n_polar} filas; la aprendida, con "
        "{cifras_c5_cybenko/n_aprendida}",
        "$L_{\\text{ent}}$ es {cifras_c5_final_metodologia/L_ent} minutos",
        "|Bosque sin tope|Al azar|{cifras_c5_final_metodologia/bosque_azar}|",
        "|Bosque sin tope|Por grupos|{cifras_c5_final_metodologia/bosque_grupo}|",
        "|Lineal|Al azar|{cifras_c5_final_metodologia/lineal_azar}|",
        "|Lineal|Por grupos|{cifras_c5_final_metodologia/lineal_grupo}|",
        "El benchmark de la media, con CV por grupos, da "
        "{cifras_c5_final_metodologia/benchmark} minutos",
        "el rango queda en {cifras_c5_dummy/rango}",
        "La recta sobre $y=x^2$ no baja de {cifras_c5_depurar/mse_recta}",
        "Aquí la CV eligió profundidad {cifras_c5_familias/profundidad} y "
        "{cifras_c5_familias/etapas} etapas; pasar de 10 a 200 árboles redujo el rango "
        "entre semillas de {cifras_c5_familias/rango_10} a {cifras_c5_familias/rango_200}",
        "las polares necesitaron {cifras_c5_cybenko/n_polar} filas y la representación "
        "aprendida {cifras_c5_cybenko/n_aprendida}",
    ],
}


def _llenar(plantilla):
    def valor(m):
        v = CITAS
        for k in m.group(1).split("/"):
            v = v[int(k)] if isinstance(v, list) else v[k]
        return str(v)
    return re.sub(r"\{(cifras_c5_[^{}]+)\}", valor, plantilla)


def _sin_espacios(s):
    return re.sub(r"\s+", "", s.replace("−", "-"))


ANCLADAS = [(p, a) for p, lista in ANCLAS.items() for a in lista]


@pytest.mark.parametrize("pagina,plantilla", ANCLADAS,
                         ids=[f"{p.stem}:{i}" for i, (p, _) in enumerate(ANCLADAS)])
def test_cada_cifra_citada_esta_en_su_frase(pagina, plantilla):
    frase = _llenar(plantilla)
    assert _sin_espacios(frase) in _sin_espacios(leer(pagina)), (
        f"{pagina.name} no trae la frase «{frase}»")
