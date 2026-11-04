"""Pruebas de prosa de la clase 3 (D-003): cada cifra de tools/ml_cifras_c3.py
aparece, en su forma literal («cita»), en la sección de la página que la cita
(clase_3.md §10.2 y §10.7.3); cada figura de FIGURAS_C3 vive en un
`::: figure` con su id en su página; los guiones de los notebooks 06 y 07 no
tienen secciones vacías; el índice del tramo rápido enlaza solo las dos
páginas.

Lee páginas y guiones, así que no es parte de S1: corre en S2 y en el paso 5
de la validación de cada borrador de Codex (C3.T13). Mientras la página no
existe estas pruebas fallan a propósito con «falta la página (la redacta
Codex)».

Anclas por tramo (protocolo p5.2 §7.1): la parte de la tarea (3_tarea.md y
su guion) la agrega la subrama -c al final, tras su bajada (C3.T8p).
"""
import re
from functools import lru_cache
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c3 as c  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/4_leer_el_error"
GUIONES = RAIZ / "tools/cuadernos_ml"


def leer(ruta):
    assert ruta.exists(), f"falta la página {ruta.relative_to(RAIZ)} (la redacta Codex)"
    return ruta.read_text(encoding="utf-8")


def secciones(texto):
    """{n: texto de la sección «## n · …» hasta el siguiente «## »}."""
    salida = {}
    for p in re.split(r"(?m)^## ", texto)[1:]:
        m = re.match(r"(\d+) · ", p)
        if m:
            salida[int(m.group(1))] = p
    return salida


def formas(cifra):
    """Las formas en que la página puede escribir una cifra: un negativo con «−»
    o con «-»; un número con separador de miles con espacio fino, normal o nada."""
    s = str(cifra)
    out = {s}
    if s.startswith("-"):
        out.add("−" + s[1:])
    if " " in s and s.replace(" ", "").isdigit():
        out |= {s.replace(" ", " "), s.replace(" ", " "), s.replace(" ", "")}
    if s.endswith(" %"):
        out.add(s.replace(" %", " %"))
        out.add(s.replace(" %", "%"))
    return out


def comprobar(texto, cifras, donde):
    faltan = [x for x in cifras if not any(f in texto for f in formas(x))]
    assert not faltan, f"{donde}: no cita {faltan}"


P1 = CLASE / "1_leer_el_error.md"
P2 = CLASE / "2_el_lagrangeano_en_accion.md"
INDICE = CLASE / "0_index.md"
NB06 = GUIONES / "06_leer_el_error.texto.md"
NB07 = GUIONES / "07_el_lagrangeano_en_accion.texto.md"


@lru_cache(maxsize=None)
def pagina(ruta):
    return leer(ruta)


# --- tramo rapido ---

def cifras_p1():
    m = c.cifras_c3_mismo_rmse()["cita"]
    e = c.cifras_c3_escala_y()["cita"]
    s = c.cifras_c3_senal_debil()["cita"]
    co = c.cifras_c3_colas()["cita"]
    o = c.cifras_c3_omitida_caso1()["cita"]
    en = c.cifras_c3_endogena()["cita"]
    di = c.cifras_c3_diana()["cita"]
    cl = c.cifras_c3_colineal()["cita"]
    return {
        1: [m["rmse_val"]],
        2: [e["rmse_modelo"], e["rmse_media"], e["rmse_mediana"], e["ybar"],
            e["rmse_sobre_ybar"], e["desv_y_ent"], e["mejora"], e["dif_pareada"], e["ee_dif"],
            s["rmse_media"], s["raiz_piso"], s["mejora"], s["dif_pareada"], s["ee_dif"],
            "16", "20", "3.2"],
        3: [co["normal"], co["pareto"], co["cauchy"], "25.99", "96", "1.49", "34"],
        4: [o["beta1_a"], o["beta1_b"], o["beta_c_x1"], o["beta_c_x2x3"], o["L_val_c"],
            o["piso_visible"], en["media_beta1"], en["cuenta"], en["L_val"], en["piso"],
            di["omitida"], di["endogena"], "3.5"],
        5: [cl["desv_beta1_0"], cl["desv_beta1_99"], cl["desv_y_dentro_99"],
            cl["desv_y_fuera_99"], "0.229", "50"],
    }


def cifras_p2():
    r = c.cifras_c3_recta_apoyo()["cita"]
    g = c.cifras_c3_regiones()["cita"]
    g12 = c.cifras_c3_grado12()["cita"]
    t = c.cifras_c3_trayectorias()["cita"]
    pa = c.cifras_c3_pareja()["cita"]
    rc = c.cifras_c3_ridge_colineal()["cita"]
    es = c.cifras_c3_estandarizar()["cita"]
    eo = c.cifras_c3_escala_objetivo()["cita"]
    mu = c.cifras_c3_mu_cv()["cita"]
    return {
        1: [r["d"], r["mu"]],
        2: [g["l2"]["mu"], g["l2"]["beta1"], g["l2"]["beta2"], g["l1"]["mu"],
            g["elastica"]["mu"], g["elastica"]["beta1"], g["elastica"]["beta2"],
            "0.148", "0.989", "1.022"],
        3: ["1.833", "2.5"],
        4: [g12["mu_medio"], g12["R"]["grande"], g12["R"]["medio"], g12["R"]["chico"],
            g12["R_sin_penalizar"], t["primera_util"], t["ultima_util"], pa["l1"]["x6"],
            rc["sin"]["desv"], rc["ridge"]["desv"]],
        5: [es["sin_x1"], es["con_x1"], es["con_x2"], eo["no_ceros_y"], eo["no_ceros_1000y"]],
        6: [mu["mu_min"], mu["mu_un_ee"], mu["cv_min"], mu["cv_un_ee"], mu["no_ceros_min"],
            mu["no_ceros_un_ee"], mu["R_un_ee"], mu["L_prueba"], mu["dos_ee_prueba"],
            mu["dif_prueba"], mu["ee_dif_prueba"]],
    }


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_p1_cada_seccion_cita_sus_cifras(n):
    s = secciones(pagina(P1))
    assert n in s, f"P1 no tiene la sección «## {n} · …»"
    comprobar(s[n], cifras_p1()[n], f"P1 §{n}")


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_p2_cada_seccion_cita_sus_cifras(n):
    s = secciones(pagina(P2))
    assert n in s, f"P2 no tiene la sección «## {n} · …»"
    comprobar(s[n], cifras_p2()[n], f"P2 §{n}")


FIGURAS_P1 = ["ml-c3-mismo-rmse", "ml-c3-benchmarks", "ml-c3-media-acumulada",
              "ml-c3-fuentes-patologias", "ml-c3-diana-beta", "ml-c3-interaccion-plano",
              "ml-c3-colineal-prediccion"]
FIGURAS_P2 = ["ml-c3-un-coeficiente", "ml-c3-recta-de-apoyo", "ml-c3-elipse-region",
              "ml-c3-encoger-1d", "ml-c3-grado-12-mu", "ml-c3-trayectorias",
              "ml-c3-ridge-colineal", "ml-c3-estandarizar", "ml-c3-mu-cv"]


def test_las_figuras_de_las_paginas_son_las_del_catalogo():
    import figuras_ml_c3 as fig
    assert sorted(FIGURAS_P1 + FIGURAS_P2) == sorted(fig._RAPIDO)


@pytest.mark.parametrize("ruta,ident", [(P1, i) for i in FIGURAS_P1] + [(P2, i) for i in FIGURAS_P2])
def test_cada_figura_vive_en_un_figure_con_su_id(ruta, ident):
    texto = pagina(ruta)
    m = re.search(r"(?ms)^:::\s*figure\s*\{#" + re.escape(ident) + r"\b[^\n]*\n(.*?)^:::\s*$", texto)
    assert m, f"{ruta.name}: no hay ::: figure {{#{ident}}}"
    assert f"_assets/{ident}.svg" in m.group(1), f"{ident}: el figure no enlaza su SVG"


@pytest.mark.parametrize("ruta", [P1, P2])
def test_ninguna_linea_dice_le_gana_con_validacion_cruzada(ruta):
    for linea in pagina(ruta).splitlines():
        if "le gana" in linea:
            assert not re.search(r"\bCV|validación cruzada", linea), linea


def test_p1_el_centro_de_entrenamiento_es_cero():
    assert "0" in secciones(pagina(P1))[1]
    assert abs(c.cifras_c3_centro_entrenamiento()["e_ent"]) < 1e-10


def test_p2_la_nota_unica_de_lambda_esta_y_es_unica():
    texto = pagina(P2)
    assert texto.count("λ") + texto.count(r"\lambda") >= 1
    assert texto.count("`alpha`") == 1


def test_el_indice_del_tramo_enlaza_las_dos_paginas_y_no_la_tarea():
    texto = pagina(INDICE)
    assert "[[ml-leer-el-error|" in texto
    assert "[[ml-lagrangeano-en-accion|" in texto
    assert "ml-tarea-3" not in texto
    assert "{#ml-c3-tab-lo-que-traes" in texto and "{#ml-c3-tab-recorrido" in texto


@pytest.mark.parametrize("ruta", [NB06, NB07])
def test_los_guiones_no_tienen_secciones_vacias(ruta):
    texto = leer(ruta)
    partes = re.split(r"(?m)^### celda: ", texto)[1:]
    assert partes, f"{ruta.name}: sin secciones"
    vacias = [p.splitlines()[0] for p in partes if not "\n".join(p.splitlines()[1:]).strip()]
    assert not vacias, f"{ruta.name}: secciones vacías {vacias}"
# --- fin tramo rapido ---


# --- tramo completo ---
# --- fin tramo completo ---
