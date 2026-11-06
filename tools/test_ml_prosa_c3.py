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
    it = c.cifras_c3_interaccion()["cita"]
    return {
        1: [m["rmse_val"]],
        2: [e["rmse_modelo"], e["rmse_media"], e["rmse_mediana"], e["ybar"],
            e["rmse_sobre_ybar"], e["desv_y_ent"], e["mejora"], e["dif_pareada"], e["ee_dif"],
            s["rmse_media"], s["raiz_piso"], s["mejora"], s["dif_pareada"], s["ee_dif"],
            "16", "20", "3.2"],
        3: [co["normal"], co["pareto"], co["cauchy"], "25.99", "96", "1.49", "34"],
        4: [o["beta1_a"], o["beta1_b"], o["beta_c_x1"], o["beta_c_x2x3"], o["L_val_c"],
            o["piso_visible"], en["media_beta1"], en["cuenta"], en["L_val"], en["piso"],
            di["omitida"], di["endogena"], it["L_val_sin"], it["L_val_con"], "3.5"],
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
    """Revisión c3 r2 (R1-H8): la cifra va atada a la frase que la cita, no a
    que aparezca un «0» en la sección."""
    frase = _unidad(pagina(P1), "La simulación confirma")
    assert r"$\bar e_{\text{ent}}=0$ a 10 decimales" in frase, frase
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
# Revisión c3 r1 (D-009.5): cada cifra atada a la FRASE que la cita, no solo a
# su sección. El ancla es un fragmento literal que aparece una sola vez en la
# página; la cifra tiene que estar en su párrafo (o en su renglón, si el ancla
# es una fila de tabla).
def _unidad(texto, ancla):
    assert texto.count(ancla) == 1, f"el ancla {ancla!r} aparece {texto.count(ancla)} veces"
    renglones = texto.splitlines()
    i = next(k for k, r in enumerate(renglones) if ancla in r)
    if renglones[i].lstrip().startswith("|"):
        return renglones[i]
    a = i
    while a > 0 and renglones[a - 1].strip():
        a -= 1
    b = i
    while b + 1 < len(renglones) and renglones[b + 1].strip():
        b += 1
    return "\n".join(renglones[a:b + 1])


def frases_p1():
    m = c.cifras_c3_mismo_rmse()["cita"]
    e = c.cifras_c3_escala_y()["cita"]
    s = c.cifras_c3_senal_debil()["cita"]
    co = c.cifras_c3_colas()["cita"]
    o = c.cifras_c3_omitida_caso1()["cita"]
    en = c.cifras_c3_endogena()["cita"]
    di = c.cifras_c3_diana()["cita"]
    cl = c.cifras_c3_colineal()["cita"]
    it = c.cifras_c3_interaccion()["cita"]
    ej = c.cifras_c3_ejercicios()
    return [
        ("Ambas tienen RMSE de validación", [m["rmse_val"]]),
        ("todo está en el ancho", [f"{ej['cancelan']['L']:g}"]),
        ("RMSE/desviación vale", [e["rmse_media"], e["rmse_mediana"], e["desv_y_ent"],
                                  e["rmse_sobre_desv"], e["mejora"]]),
        ("Caso 11: diferencia pareada", [e["dif_pareada"], e["ee_dif"], e["n_val"]]),
        ("Con señal débil, $f=0.75x$", [s["rmse_modelo"], s["rmse_media"], s["raiz_piso"],
                                       s["mejora"], s["dif_pareada"], s["ee_dif"]]),
        ("el cociente máximo/mínimo", [co["normal"], co["pareto"], co["cauchy"]]),
        ("La omitida centra", [di["omitida"], di["endogena"]]),
        ("la simulación da $", [o["beta1_a"]]),
        ("sin el producto,", [o["beta1_b"]]),
        ("el coeficiente de $x_2x_3", [o["beta_c_x1"], o["beta_c_x2x3"], o["L_val_c"]]),
        ("el piso con lo visible es", [o["piso_visible"]]),
        ("elimina la silla", [it["L_val_sin"], it["L_val_con"]]),
        ("La cuenta da 2.5", [en["cuenta"], en["media_beta1"], en["L_val"], en["piso"]]),
        ("Todas las $x$ son normales estándar", [di["corr_omitida"], di["endogeno"],
                                                 di["cuenta_omitida"], di["cuenta_endogena"],
                                                 di["omitida"], di["endogena"]]),
        ("La desviación de $\\widehat y$ es", [cl["desv_y_dentro_99"], cl["desv_y_fuera_99"],
                                              cl["desv_beta1_0"], cl["desv_beta1_99"]]),
        ("veces mayor", [f"{ej['colineal']['razon']:.1f}", f"{ej['colineal']['desv_09']:.3f}"]),
    ]


def frases_p2():
    r = c.cifras_c3_recta_apoyo()["cita"]
    g = c.cifras_c3_regiones()["cita"]
    g12 = c.cifras_c3_grado12()["cita"]
    v = c.cifras_c3_grado12_vistas()["cita"]
    pa = c.cifras_c3_pareja()["cita"]
    rc = c.cifras_c3_ridge_colineal()["cita"]
    es = c.cifras_c3_estandarizar()["cita"]
    mu = c.cifras_c3_mu_cv()["cita"]
    k = ("grande", "medio", "chico")
    sin_x2 = es["sin_x2"].replace(" × 10^", "\\times10^")
    return [
        ("la recta de pendiente", [r["d"], "-" + r["mu"]]),
        ("ridge llega a", [g["l2"]["beta1"], g["l2"]["beta2"], g["l2"]["mu"], g["l1"]["mu"],
                           g["elastica"]["beta1"], g["elastica"]["beta2"], g["elastica"]["mu"]]),
        ("| $L_{\\text{val}}$, en 12 filas", [g12["L_val"][x] for x in k]),
        ("| $R$, muestra enorme", [g12["R"][x] for x in k]),
        ("| Centro de residuales", [v[x]["centro"] for x in k]),
        ("| Ancho de residuales", [v[x]["ancho"] for x in k]),
        ("El $R$ de B,", [g12["R"]["medio"]]),
        ("no ve ese tope", [g12["n_desarrollo"]]),
        ("lasso conserva $x_1$", [pa["l1"]["x1"], pa["l1"]["x6"]]),
        ("La elástica conserva ambas", [pa["elastica"]["x1"]]),
        ("su media pasa de", [rc["sin"]["desv"], rc["ridge"]["desv"], rc["sin"]["media"],
                              rc["ridge"]["media"]]),
        ("fuera de la figura", [sin_x2]),
        ("| Mínimo |", [mu["mu_min"], mu["cv_min"], mu["ee_min"], mu["no_ceros_min"]]),
        ("| Un EE |", [mu["mu_un_ee"], mu["cv_un_ee"], mu["ee_un_ee"], mu["no_ceros_un_ee"]]),
        ("Sus riesgos son", [mu["R_min"], mu["R_un_ee"]]),
        ("Los conteos y $R$ son del reajuste", [str(c.curvas_mu_cv()["filas"])]),
        ("Al abrir la prueba una vez", [mu["L_prueba"], mu["dos_ee_prueba"]]),
        ("La diferencia pareada modelo − media es", [mu["dif_prueba"], mu["ee_dif_prueba"]]),
    ]


@pytest.mark.parametrize("ruta,frases", [(P1, "frases_p1"), (P2, "frases_p2")])
def test_cada_cifra_esta_en_la_frase_que_la_cita(ruta, frases):
    texto = pagina(ruta)
    for ancla, cifras in globals()[frases]():
        comprobar(_unidad(texto, ancla), cifras, f"{ruta.name} «{ancla}»")




# Revisión c3 r3 (R1-H8, tercera vuelta): una fila de tabla se compara columna
# por columna (intercambiar 48.3 y 203.1 en la fila de R tiene que fallar), y
# las respuestas, viñetas de cierre y guiones de nb06 y nb07 atan sus cuentas.
def _celdas(fila):
    return [x.strip() for x in fila.strip().strip("|").split("|")]


def _es(celda, cifras):
    """La celda dice exactamente la cifra, o (con varias) las trae en orden."""
    if len(cifras) == 1:
        return celda in formas(cifras[0])
    i = 0
    for x in cifras:
        hallado = [celda.find(f, i) for f in formas(x) if celda.find(f, i) >= 0]
        if not hallado:
            return False
        i = min(hallado) + 1
    return True


def filas_p2():
    g12 = c.cifras_c3_grado12()["cita"]
    v = c.cifras_c3_grado12_vistas()["cita"]
    mu = c.cifras_c3_mu_cv()["cita"]
    k = ("grande", "medio", "chico")
    return [
        ("| $L_{\\text{val}}$, en 12 filas", [[g12["L_val"][x]] for x in k]),
        ("| $R$, muestra enorme", [[g12["R"][x]] for x in k]),
        ("| Centro de residuales", [[v[x]["centro"]] for x in k]),
        ("| Ancho de residuales", [[v[x]["ancho"]] for x in k]),
        ("| Mínimo |", [[mu["mu_min"]], [mu["cv_min"], mu["ee_min"]], [mu["no_ceros_min"]]]),
        ("| Un EE |", [[mu["mu_un_ee"]], [mu["cv_un_ee"], mu["ee_un_ee"]],
                       [mu["no_ceros_un_ee"]]]),
    ]


def test_p2_las_filas_de_tabla_van_columna_por_columna():
    texto = pagina(P2)
    for ancla, columnas in filas_p2():
        celdas = _celdas(_unidad(texto, ancla))[1:]
        assert len(celdas) == len(columnas), (ancla, celdas)
        malas = [(cel, cif) for cel, cif in zip(celdas, columnas) if not _es(cel, cif)]
        assert not malas, f"{ancla}: {malas}"


def _g(x):
    return f"{x:g}"


def _par(t):
    return f"({_g(round(t[0], 3))},\\ {_g(round(t[1], 3))})"


def frases_respuestas():
    ej = c.cifras_c3_ejercicios()
    k, co, cl = ej["constante"], ej["cola"], ej["colineal"]
    cero, esq = ej["cero_a_mano"], ej["esquina"]
    return {P1: [
        ("Elevar al cuadrado hace costoso", [_g(k["mse_media"]), _g(k["mse_mediana"])]),
        ("«Mejor» depende de la pérdida", [_g(k["mae_media"]), _g(k["mae_mediana"])]),
        ("La fila aporta", [_g(co["mse"]), f"{100 * co['frac_mse']:.0f}"]),
        ("El cuadrado aumenta mucho su peso", [_g(co["mae"]), f"{100 * co['frac_mae']:.0f}"]),
        ("**(a)** $2+3", [_g(ej["pendiente"])]),
        ("Toma la raíz de la varianza", [f"{cl['desv_09']:.3f}", f"{cl['razon']:.1f}"]),
        ("el factor $1/(1-0.99^2)", [f"{ej['factor_099']:.0f}"]),
        ("- **Cola larga:**", [f"{100 * co['frac_mse']:.0f}"]),
        ("- **Lo que falta:**", [_g(ej["pendiente"])]),
    ], P2: [
        ("Ninguna pendiente vale cero", [_par(esq["ridge"]), f"{esq['mu_ridge']:.3f}"]),
        ("Lasso resta el umbral sin cruzar cero", [_par(cero["l1"])]),
        ("el umbral es la mitad del de lasso", [_par(cero["elastica"])]),
    ]}


@pytest.mark.parametrize("ruta", [P1, P2])
def test_cada_respuesta_ata_sus_cuentas(ruta):
    texto = pagina(ruta)
    for ancla, cifras in frases_respuestas()[ruta]:
        comprobar(_unidad(texto, ancla), cifras, f"{ruta.name} «{ancla}»")


def _defecto(py, etiqueta):
    """El valor inicial de un deslizador del .py del notebook: la prosa lo cita."""
    m = re.search(re.escape(f'"{etiqueta}"') + r",\s*[-\d.]+,\s*[-\d.]+,\s*[-\d.]+,"
                  r"\s*([-\d.]+)\)", py)
    assert m, f"no hay deslizador «{etiqueta}» en el .py"
    return float(m.group(1))


def test_los_guiones_de_nb06_y_nb07_atan_sus_cuentas_al_codigo():
    import ml_cifras_c3 as cc
    ml = cc._ml()
    py6 = (GUIONES / "06_leer_el_error.py").read_text(encoding="utf-8")
    py7 = (GUIONES / "07_el_lagrangeano_en_accion.py").read_text(encoding="utf-8")
    t6, t7 = leer(NB06), leer(NB07)
    # nb06 B4: f = 1 + 2·x1 + 3·x2; el control empieza en corr = 0.3
    assert "f=lambda d: 1 + 2 * d.x1 + 3 * d.x2" in py6
    corr = _defecto(py6, "corr(x1, x2)")
    centro = _g(round(2 + 3 * corr, 6))
    comprobar(_unidad(t6, "¿dónde se centra el histograma"), [_g(corr), centro, "2", "5"],
              "nb06 bloque-4-predice")
    comprobar(_unidad(t6, "Se centra en"), [_g(corr), centro], "nb06 bloque-4-explica")
    comprobar(_unidad(t6, "Deja «qué no ve el modelo» en «x2»"), [_g(corr)],
              "nb06 bloque-4-predice, controles")
    # nb07 B2: b = 0.4 y μ = 1 por omisión; la cuenta sale de encoger_1d
    b, mu = _defecto(py7, "b: pendiente sin penalizar"), _defecto(py7, "μ")
    assert ml.encoger_1d(b, mu, "l1") == 0
    comprobar(_unidad(t7, "¿sobrevive a lasso"), [_g(b), _g(mu)], "nb07 bloque-2-predice")
    comprobar(_unidad(t7, "No sobrevive:"), [_g(b), _g(mu / 2)], "nb07 bloque-2-explica")
    comprobar(_unidad(t7, "Ridge divide entre $1+\\mu$: aquí"),
              [_g(b), _g(ml.encoger_1d(b, mu, "l2"))], "nb07 bloque-2-explica, ridge")
    # nb07 B4: 100 réplicas con μ = 0.3 y gemela a 0.95
    assert "ml.beta_repetido(fab, PHI_50, 100, mu=0.3," in py7
    assert 'gemelas={"x1": 0.95}' in py7
    comprobar(_unidad(t7, "El conteo usa"), ["100", "0.3", "0.95"], "nb07 bloque-4-explica")
    # nb07, ejercicio del cero a mano: b = (3, 0.4), μ = 1
    cero = c.cifras_c3_ejercicios()["cero_a_mano"]
    comprobar(_unidad(t7, "Lasso resta $\\mu/2=0.5$"),
              [f"({_g(cero['l1'][0])},{_g(cero['l1'][1])})",
               f"({_g(cero['l2'][0])},{_g(round(cero['l2'][1], 6))})"],
              "nb07 ejercicio-cero-a-mano-respuesta")

def _bloque(texto, ident):
    i = texto.index("{#" + ident)
    return texto[i:texto.index("\n:::", i)]


def test_p1_h1_del_ejercicio_final_fija_el_ruido_independiente():
    """Revisión c3 r1: «el ruido crece con |x1|» no basta para que el signo de e
    no siga a x2 (ε = σ(x1)·signo(x1x2)·U cumple H1 y da la silla de H2). H1 tiene
    que decir ε = σ(x1)·Z con Z independiente de las entradas."""
    ej = _bloque(pagina(P1), "ml-c3-ej-final-leer-el-error")
    assert r"\sigma_\varepsilon(x_1)" in ej and "independiente de $x_1$ y $x_2$" in ej, ej
    assert r"\sigma(x_1)" not in ej, "σ sola es la sigmoide (revisión c3 r2)"


def test_el_intercepto_solo_garantiza_el_centro_en_entrenamiento():
    """Revisión c3 r1: con semilla 0 los centros de validación del grado 12 son
    −0.17, −0.52 y 3.56; el intercepto libre solo fija ē = 0 en entrenamiento."""
    for ruta in (P2, GUIONES / "07_el_lagrangeano_en_accion.texto.md"):
        texto = pagina(ruta)
        assert "mantiene el centro" not in texto, ruta.name
        assert "en entrenamiento" in texto, ruta.name


def test_p1_h1_habla_del_error_ideal_no_del_residual():
    """Revisión c3 r2: e = σ_ε(x1)Z + f − f̂; con semilla 0, 3 de 120 residuales
    de validación tienen signo distinto al del ruido. El signo de Z es el del
    error ideal, no el de e."""
    resp = _bloque(pagina(P1), "ml-c3-resp-final-leer-el-error")
    assert "el signo de $e$ es el de $Z$" not in resp
    assert "error ideal" in resp and "sistemático" in resp, resp


def test_p1_el_piso_normal_conjunto_se_limita_al_caso_8():
    """Revisión c3 r2: Var(ε)(1 − corr²) no vale con otras entradas visibles
    (ε = 0.5x1 + 0.5x2 + √0.5·Z: la fórmula da 0.75 y el piso es 0.50)."""
    obs = _bloque(pagina(P1), "ml-c3-obs-endogeneidad")
    assert "Si no falta ninguna variable" not in obs
    assert "única entrada" in obs and "Con más entradas visibles" in obs, obs
    assert "no de la predicción" not in obs


def test_p1_bengio_grandvalet_excluye_un_estimador_universal():
    obs = _bloque(pagina(P1), "ml-c3-obs-cv-no-es-reserva")
    assert "insesgado universal" in obs, obs


def test_p2_con_mu_enorme_lasso_llega_a_una_meseta():
    """Revisión c3 r2: con μ = 10, 100 y 1000, CV₅ = 16.3050 y R = 17.5321; la
    página no puede decir que siguen subiendo."""
    cur = c.curvas_mu_cv()
    grandes = sorted(cur["R"])[-3:]
    assert len({round(cur["R"][m], 9) for m in grandes}) == 1
    texto = pagina(P2)
    assert r"con $\mu\to\infty$ llegas al benchmark" not in texto
    resp = _bloque(texto, "ml-c3-resp-sube-mu")
    assert "meseta" in resp and "permanecen iguales" in resp, resp
    seis = secciones(texto)[6]
    assert "meseta del predictor constante, el benchmark" in seis


def test_los_guiones_de_nb07_no_hablan_de_la_linea_crema():
    """Revisión c3 r2: con el tema claro del notebook, R es negra discontinua."""
    texto = leer(GUIONES / "07_el_lagrangeano_en_accion.texto.md")
    assert "crema" not in texto and texto.count("la línea discontinua es $R$") == 2


def test_la_monotonia_en_mu_admite_empates():
    """Revisión c3 r1: las desigualdades del teorema son no estrictas."""
    teo = _bloque(pagina(P2), "ml-c3-teo-monotonia-mu")
    assert "siempre prefiere" not in teo and "empates" in teo, teo


# --- fin tramo rapido ---


# --- tramo completo ---
TAREA = CLASE / "3_tarea.md"
NBTAREA = GUIONES / "tarea_3_cincuenta_variables.texto.md"
ENTREGA = "Se entrega el `.ipynb` por Canvas, con las celdas corridas"


def test_tarea_cita_el_montaje_y_la_rubrica():
    texto = pagina(TAREA)
    t = c.cifras_c3_tarea()["cita"]
    comprobar(_unidad(texto, "Tienes 50 variables"), [t["J"], t["utiles"], t["corr_gemela"]],
              "3_tarea.md «Tienes 50 variables»")
    comprobar(_unidad(texto, "Tendrás 300 observaciones"), [t["n"], t["n_ent"]],
              "3_tarea.md «Tendrás 300 observaciones»")
    s = secciones(texto)
    assert set(s) >= {1, 2, 3, 4, 5}, f"3_tarea.md: secciones {sorted(s)}"
    puntos = [int(x) for x in re.findall(r"\|\s*(\d{1,3})\s*\|", s[4])]
    assert sorted(puntos) == sorted([10, 15, 25, 20, 15, 15]) and sum(puntos) == 100, puntos


def test_tarea_sin_respuestas_ni_fechas_y_con_la_frase_de_entrega():
    texto = pagina(TAREA)
    assert ENTREGA in texto
    assert "La fecha la da el profesor en clase" in texto
    assert not re.search(r"^:::\s*(answer|hint|exercise)\b", texto, re.M)
    assert "tarea_3_cincuenta_variables.ipynb" in texto


def test_el_guion_de_la_tarea_no_da_respuestas_y_cita_el_montaje():
    texto = leer(NBTAREA)
    partes = re.split(r"(?m)^### celda: ", texto)[1:]
    claves = [p.splitlines()[0].strip() for p in partes]
    assert not any(k.endswith(("-explica", "-respuesta")) for k in claves), claves
    assert "<details" not in texto
    vacias = [p.splitlines()[0] for p in partes if not "\n".join(p.splitlines()[1:]).strip()]
    assert not vacias, f"secciones vacías {vacias}"
    assert ENTREGA in texto
    t = c.cifras_c3_tarea()["cita"]
    comprobar(_unidad(texto, "`J` fija"), [t["J"]], "guion «`J` fija»")
    comprobar(_unidad(texto, "es gemela de `x1`"), [t["corr_gemela"]], "guion «gemela»")
    comprobar(_unidad(texto, "Hay $n=300$ observaciones"), [t["n"], t["n_ent"]],
              "guion «Hay n=300 observaciones»")


def test_el_indice_completo_lleva_la_fila_de_la_tarea_sin_enlazarla():
    texto = pagina(INDICE)
    tabla = texto.split("{#ml-c3-tab-recorrido", 1)[1].split("\n:::", 1)[0]
    assert "Tarea 3" in tabla and "aparte" in tabla
    assert "tarea_3_cincuenta_variables" in texto

# --- fin tramo completo ---
