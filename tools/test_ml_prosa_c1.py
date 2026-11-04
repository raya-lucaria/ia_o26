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
P2_RUTA = CLASE / "2_polinomios_y_capacidad.md"


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


def test_p1_solo_cita_ids_de_la_clase_1_que_existen():
    # Variante 1a: ningun @ a la pagina 2. Desde el nucleo 1b (C1.T13b) la
    # remision de §6 cita @ml-c1-obs-capacidad-efectiva: vale cualquier id de
    # P1 o P2 que exista.
    paginas = p1() + (P2_RUTA.read_text(encoding="utf-8") if P2_RUTA.exists() else "")
    propios = set(re.findall(r"\{#(ml-c1-[a-z0-9-]+)", paginas))
    citados = set(re.findall(r"@(ml-c1-[a-z0-9-]+)", p1()))
    assert citados <= propios, f"@ a ids que no existen: {sorted(citados - propios)}"


def test_p1_la_optimizacion_no_es_cuarta_ni_quinta_fuente():
    assert not re.search(r"(cuarta|quinta) fuente", p1())


# ---- cifras atadas a su frase (revision r1 del tramo 1a, D-009.5) ----

def _tfrac(fr):
    """Una fraccion como la escribe P1: 73, \\tfrac{280}{3}, con su signo aparte."""
    a = abs(fr)
    return str(a.numerator) if a.denominator == 1 else f"\\tfrac{{{a.numerator}}}{{{a.denominator}}}"


def test_p1_s1_da_la_recta_y_el_polinomio_de_grado_5_con_fracciones_exactas():
    g = c.cifras_c1_ganador()
    sec = s1()[1]
    pend = g["pendiente_recta_fraccion"]
    assert f"${g['intercepto_recta']:.1f}+({pend.numerator}/{pend.denominator})x$" in sec
    fr = g["coeficientes_grado_5_fracciones"]          # de x^5 a la constante
    terminos = []
    for k, a in enumerate(reversed(fr)):               # constante primero
        signo = "-" if a < 0 else "+"
        cuerpo = _tfrac(a) + ("" if k == 0 else "x" if k == 1 else f"x^{k}")
        terminos.append(cuerpo if k == 0 else signo + cuerpo)
    assert "".join(terminos) in sec.replace(" ", "")


def test_p1_s1_el_ejercicio_no_trae_su_respuesta_en_la_prosa():
    sec = s1()[1]
    prosa = re.sub(r"(?ms)^::: figure.*?^:::\s*$", "", sec[:sec.index("::: exercise")])
    assert "24.0" not in prosa, "la prosa de §1 ya resuelve (a) del ejercicio"
    resp = bloque(p1(), "ml-c1-resp-ganador").group(1)
    g = c.cifras_c1_ganador()
    assert f"{g['prediccion'][0.0][0]:.1f} y {g['prediccion'][0.0][1]:.1f}" in resp
    assert "término constante" in resp


def test_p1_s3_cifras_en_su_frase():
    g, p = c.cifras_c1_ganador(), c.cifras_c1_piso()[1.0]
    sec = s1()[3]
    assert f"pérdida mínima en entrenamiento vale {p['L_ent_recta']:.2f}" in sec
    assert f"«El error es {g['rmse_1']:.2f} minutos»" in sec
    assert f"en ellas su MSE es {g['mse_fija']:g}" in sec
    assert f"MSE de {g['mse_1']:.3f} < 1" in sec
    assert f"${g['rmse_1']:.3f}=\\sqrt{{{g['mse_1']:.3f}}}$" in sec
    assert f"$\\sigma_\\varepsilon=1$ es {p['ee_oraculo']:.4f}" in sec


def test_p1_s1_los_rmse_de_la_unidad_6_en_su_frase():
    g = c.cifras_c1_ganador()
    assert (f"RMSE de {g['rmse_1']:.3f} para la recta y {g['rmse_5']:.3f} "
            "para el grado 5") in s1()[1]


def test_p1_s1_la_respuesta_da_las_dos_predicciones_a_35_km():
    g = c.cifras_c1_ganador()
    recta, grado5 = g["prediccion"][3.5]
    assert f"{recta:.1f}" == f"{grado5:.1f}", "la respuesta (a) dice que coinciden"
    resp = bloque(p1(), "ml-c1-resp-ganador").group(1)
    assert f"A 3.5 km, la recta y el polinomio predicen {recta:.1f} minutos" in resp


def test_p1_el_cierre_condiciona_el_cuadruplo_del_piso():
    # Con la lluvia sin medir el piso es 9 + σ_ε²: duplicar σ_ε lo lleva de
    # 10 a 13, no a 40 (revision r2). El cierre solo afirma el cuadruplo
    # cuando el piso es σ_ε².
    cierre = cierre_p1()
    assert "Duplicar $\\sigma_\\varepsilon$ cuadruplica" not in cierre
    assert "cuadruplica" not in cierre or "solo $\\sigma_\\varepsilon^2$" in cierre


def test_p1_s4_las_barras_del_oraculo_en_su_frase():
    p = c.cifras_c1_piso()
    sec = s1()[4]
    assert (f"Las barras aproximan riesgos: {p[1.0]['R_oraculo']:.2f} y "
            f"{p[2.0]['R_oraculo']:.2f} no contradicen") in sec


def test_p1_s7_cifras_en_su_frase():
    a = c.cifras_c1_anillos()
    sec = s1()[7]
    assert (f"En cartesianas hay {round(100 * a['cartesianas']['aciertos'])} % de aciertos "
            f"en el despliegue, cerca del {round(100 * a['moda'])} % de la moda; en polares, "
            f"{round(100 * a['polares']['aciertos'])} %") in sec
    assert f"la ideal $r={a['radio_bayes']:.2f}$ es horizontal" in sec
    assert f"con coeficiente {menos(a['polares']['beta']['theta'], 2)[0]}" in sec
    assert f"alcanza solo {round(100 * a['bayes'])} % de aciertos" in sec


def test_p1_la_lectura_cabe_en_su_presupuesto():
    # 80 palabras por minuto sin pistas ni respuestas (contrato §9), contra
    # los ~30 min de lectura que declara la pagina (el resto es el notebook)
    # y los 5 min de §3 del brief, con un margen de 10 %.
    import contrato_unidad as cu
    palabras = {}
    for n, texto in s1().items():
        pag = cu.parsear("## " + texto)
        palabras[n] = sum(cu.palabras(u.texto) for u in pag.unidades
                          if not u.excluida and not (set(u.contexto) & cu.DIRECTIVAS_FUERA_DE_TIEMPO))
    assert "~30 min de lectura" in p1()
    assert sum(palabras.values()) <= 30 * 80 * 1.1, palabras
    assert palabras[3] <= 5 * 80 * 1.1, palabras[3]


# ---- forma que validate no ve (revision r1 del tramo 1a) ----

def paginas_c1():
    return sorted(CLASE.glob("*.md"))


def test_ningun_aviso_lleva_texto_en_la_linea_del_marcador():
    # Raya solo reconoce «> [!TIP]» solo en su renglon
    # (raya_static/rendering.py); con texto detras publica «[!TIP]» literal.
    for ruta in paginas_c1():
        for n, renglon in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            assert not re.match(r"^\s{0,3}>\s*\[!(NOTE|TIP|WARNING|CAUTION)\]\s*\S", renglon), \
                f"{ruta.name}:{n}: el marcador del aviso va solo en su renglon"


def test_ningun_titulo_de_directiva_lleva_matematicas():
    # Raya no renderiza $…$ dentro de title=: el sitio publico
    # «Compara con $\\beta$ fijo» literal (revision r2 del tramo 1a). Recorre
    # toda la unidad, no solo la clase 1: es una guarda comun.
    unidad = CLASE.parent
    for ruta in sorted(unidad.rglob("*.md")):
        for n, renglon in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            if renglon.lstrip().startswith(":::"):
                for titulo in re.findall(r'title="([^"]*)"', renglon):
                    assert "$" not in titulo and "\\" not in titulo, \
                        f"{ruta.relative_to(RAIZ)}:{n}: title= con matemáticas: {titulo}"


def test_ninguna_lista_usa_el_parentesis_como_marcador():
    # «1) …» es lista ordenada en Markdown: la prueba del mejor predictor se
    # publico como dos renglones de lista con 3) y 4) metidos en el segundo
    # (revision r2 del tramo 1a). Las listas van con «1.»; los incisos, «(a)».
    for ruta in paginas_c1():
        for n, renglon in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            assert not re.match(r"^\s{0,3}\d+\)\s", renglon), \
                f"{ruta.name}:{n}: lista con «N)»; usa «N.» o prosa"


def test_p1_el_alt_de_cada_figura_es_el_aria_label_de_su_svg():
    import html
    assets = CLASE.parent / "_assets"
    figuras = re.findall(r"!\[([^\]]*)\]\(\.\./_assets/(ml-c1-[a-z0-9-]+)\.svg\)", p1())
    assert len(figuras) == 9
    for alt, ident in figuras:
        svg = (assets / f"{ident}.svg").read_text(encoding="utf-8")
        aria = html.unescape(re.search(r'aria-label="([^"]*)"', svg).group(1))
        assert alt == aria, ident


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


def test_nb01_cifras_de_los_bloques_en_su_celda():
    b1, p, ll = c.cifras_c1_bloque_1(), c.cifras_c1_piso()[1.0], c.cifras_c1_lluvia_grados()
    a = c.cifras_c1_anillos()
    t1 = " ".join(celda("bloque-1-explica").split())
    assert f"$L_{{\\text{{ent}}}}={b1['L_ent_recta']:.3f}$" in t1
    assert f"riesgo aproximado {b1['R_recta']:.3f} en el despliegue, frente a {b1['R_media']:.3f}" in t1
    t2 = " ".join(celda("bloque-2-explica").split())
    assert f"riesgo aproximado de {p['R_oraculo']:.3f}" in t2
    assert f"$L_{{\\text{{ent}}}}={p['L_ent_oraculo']:.3f}$" in t2
    t3 = " ".join(celda("bloque-3-explica").split())
    assert f"con grado 1 es {ll[False][1]:.2f}" in t3
    assert f"el riesgo sube de {ll[False][1]:.2f} a {ll[False][5]:.2f}" in t3
    assert "casi no" not in t3
    assert f"$r={a['radio_bayes']:.2f}$" in celda("bloque-4-mira")
    t4 = " ".join(celda("bloque-4-explica").split())
    assert f"logra {round(100 * a['cartesianas']['aciertos'])} % de aciertos" in t4
    assert f"frente al {round(100 * a['moda'])} % de la moda" in t4
    assert f"Polares sí: logra {round(100 * a['polares']['aciertos'])} %" in t4
    assert f"solo radio también logra {round(100 * a['solo radio']['aciertos'])} %" in t4
    assert f"{round(100 * a['bayes'])} %" in t4
    assert "techo de Bayes es" not in t4, "los aciertos del oráculo en la muestra no son el techo"
    assert "aciertos del oráculo" in t4


def test_nb01_la_reciproca_tiene_riesgo_infinito_por_este_ajuste_no_por_la_familia():
    t5 = " ".join(celda("bloque-5-explica").split())
    assert "este ajuste tiene riesgo verdadero infinito" in t5
    assert "coeficiente de $1/x_1$ no es cero" in t5


def test_nb01_no_lleva_arrobas_ni_wikilinks():
    assert not re.search(r"@ml-|\[\[", nb01())

# ---- cifras atadas a su bloque (revision r3, D-009.5) ----

def _g(v):
    return f"{v:g}"


def test_p1_s2_el_ejercicio_del_residual_cuenta_con_sus_datos():
    r = c.cifras_c1_residual()
    ej = bloque(p1(), "ml-c1-ej-residual").group(1)
    assert (f"$f({r['x']})={_g(r['f'])}$, observaste $y={_g(r['y'])}$ y tu ajuste dice "
            f"$\\widehat f({r['x']})={_g(r['f_gorro'])}$") in ej
    resp = bloque(p1(), "ml-c1-resp-residual").group(1)
    assert f"$\\varepsilon={_g(r['y'])}-{_g(r['f'])}={_g(r['ruido'])}$" in resp
    assert (f"$f-\\widehat f={_g(r['f'])}-{_g(r['f_gorro'])}={_g(r['reducible'])}$"
            in resp)
    assert f"${_g(r['y'])}-{_g(r['f_gorro'])}={_g(r['residual'])}$" in resp


def test_p1_s4_el_ejercicio_del_piso_da_sigma_cuadrada():
    e = c.cifras_c1_ej_piso()
    assert e["piso"] == e["sigma2"]
    ej = bloque(p1(), "ml-c1-ej-piso").group(1)
    assert f"$\\sigma_\\varepsilon^2={_g(e['sigma2'])}$" in ej
    assert f"muestra de {e['n_muestra']}" in ej
    resp = bloque(p1(), "ml-c1-resp-piso").group(1)
    assert f"su promedio poblacional es {_g(e['piso'])}." in resp
    assert f"En {e['n_muestra']} observaciones no tiene por qué dar {_g(e['piso'])}" in resp


def test_p1_s5_el_ejemplo_de_la_lluvia_cuenta_dentro_de_su_bloque():
    ll = c.cifras_c1_lluvia()
    ejm = bloque(p1(), "ml-c1-ejm-lluvia").group(1)
    assert (f"$E[y\\mid x_1]={ll['intercepto_sin_x2']:g}+{ll['pendiente_sin_x2']:g}x_1$"
            in ejm)
    assert (f"$R_{{\\text{{Bayes}}}}=1+6^2\\cdot\\tfrac14={ll['piso_sin_x2_exacto']:g}$"
            in ejm)
    assert f"Si mide $x_2$, $R_{{\\text{{Bayes}}}}={ll['piso_con_x2_exacto']:g}$." in ejm
    assert round(ll["piso_sin_x2"], 6) == ll["piso_sin_x2_exacto"]
    assert round(ll["piso_con_x2"], 6) == ll["piso_con_x2_exacto"]


def test_p1_s5_de_10_a_1_en_cada_oracion_que_lo_dice():
    ll = c.cifras_c1_lluvia()
    de_a = f"de {ll['piso_sin_x2']:.0f} a {ll['piso_con_x2']:.0f}"
    sec = s1()[5]
    assert f"medir la lluvia baja el piso {de_a}." in sec
    resp = bloque(p1(), "ml-c1-resp-intervencion").group(1)
    assert f"Medir $x_2$ baja el piso {de_a}." in resp
    assert f"**El piso depende de lo visible:** medir la lluvia lo baja {de_a}." in cierre_p1()


def test_p1_s7_arriba_y_abajo_solo_con_el_radio_queda_en_50():
    a = c.cifras_c1_arriba_abajo()
    assert abs(a["aciertos"] - a["bayes_solo_r"]) < 0.02
    resp = bloque(p1(), "ml-c1-resp-representacion").group(1)
    assert f"los aciertos quedan cerca de {round(100 * a['aciertos'])} %." in resp
    assert round(100 * a["aciertos"]) == round(100 * a["bayes_solo_r"])


def test_p1_s7_el_aviso_no_promete_que_el_piso_sube_sin_nombrar_la_perdida():
    # Con aciertos, descartar θ puede dejar igual el mejor desempeño (Pr(1|θ) =
    # 0.6 y 0.8 equiprobables: 0.30 de error con y sin θ). Revision r3.
    sec = s1()[7]
    assert "el piso sube" not in sec
    assert "los aciertos del mejor clasificador posible pueden bajar" in sec


def test_p1_s8_no_cita_ecuaciones_normales_que_nadie_presento():
    assert "ecuaciones normales" not in p1()
    assert "el mismo problema de mínimos cuadrados" in s1()[8]


def test_p1_la_pista_final_suma_por_clase():
    pista = bloque(p1(), "ml-c1-pista-final-que-es-f-2").group(1)
    assert "cuatro puntos" not in pista
    assert "dos desigualdades de cada clase" in pista


def test_p1_el_alt_del_ganador_no_da_la_respuesta_del_ejercicio():
    fig = bloque(p1(), "ml-c1-ganador-imposible").group(1)
    assert "3.5 km" not in fig and "24.0" not in fig


def test_nb01_la_galeria_no_promete_cifras_que_no_imprime():
    t = " ".join(celda("galeria-intro").split())
    assert "cifras que imprime." not in t
    assert "el caso 2 la celda no imprime cifras" in t
    assert "vuelve a las cifras que imprime el bloque 3" in t
    assert "ignora por ahora la curva de capacidad" in t

# --- fin tramo 1a ---


# --- tramo 1b ---

P2 = CLASE / "2_polinomios_y_capacidad.md"
NB02 = GUIONES / "02_polinomios_y_capacidad.texto.md"


@lru_cache(maxsize=None)
def p2():
    return leer(P2)


@lru_cache(maxsize=None)
def s2():
    return secciones(p2())


def cierre_p2():
    return p2().split("## 8 · ", 1)[1].split("\n## ", 1)[1]


def plano(texto):
    """El texto con los espacios colapsados (las frases cruzan renglones)."""
    return " ".join(texto.split())


def test_p2_tiene_las_ocho_secciones_del_brief():
    assert sorted(s2()) == list(range(1, 9))


# ---- cifras, una aserción por fila de §10.7 (tramo 1b) ----

def test_p2_s1_cita_el_error_de_taylor_en_2_5():
    t = c.cifras_c1_taylor()
    sec = s2()[1]
    assert f"{t['taylor_3'][2.5]:.1f}" in sec and f"{t['taylor_9'][2.5]:.1f}" in sec


def test_p2_s1_el_micro_de_taylor_da_medio():
    m = bloque(p2(), "ml-c1-resp-taylor")
    assert "0.5" in m.group(1) or "1/2" in m.group(1) or "\\tfrac12" in m.group(1)


def test_p2_s2_cita_los_errores_maximos_de_weierstrass():
    w = c.cifras_c1_weierstrass()
    sec = s2()[2]
    for N in c.WEIERSTRASS_GRADOS:
        assert f"{w[N]['error_maximo']:.3f}" in sec, N


def test_p2_s3_cita_L_ent_y_R_de_los_tres_ajustes():
    t = c.cifras_c1_tres_ajustes()
    sec = s2()[3]
    for N in c.TRES_GRADOS:
        assert f"{t[N]['L_ent']:.2f}" in sec, N


def test_p2_s4_cita_el_minimo_de_la_u_y_el_bajo_el_piso():
    k = c.cifras_c1_capacidad()[20]
    sec = plano(s2()[4])
    assert f"N={k['N_menor_R']}" in sec.replace(" ", "")
    m = bloque(p2(), "ml-c1-ej-bajo-el-piso")
    assert f"{k['L_ent'][15]:.3f}" in m.group(1) and "0.25" in m.group(1)


def test_p2_s4_cita_el_optimismo_en_500_muestras():
    o = c.cifras_c1_optimismo()
    sec = s2()[4]
    assert "500" in sec
    for clave in ("R_fijo", "media_L_ent_gorro", "media_R_gorro"):
        assert f"{o[clave]:.2f}" in sec, clave


def test_p2_s5_cita_las_200_elecciones():
    e = c.cifras_c1_elegir()
    sec = plano(s2()[5])
    assert f"{e['veces_N_max_ent']} de {e['repeticiones']}" in sec


def test_p2_s6_cita_el_inverso_y_las_columnas():
    i = c.cifras_c1_inverso()
    sec = s2()[6]
    assert f"{i['R_inverso']:.2f}" in sec and f"{i['R_10']:.2f}" in sec
    col = c.cifras_c1_columnas()
    resp = bloque(p2(), "ml-c1-resp-columnas").group(1)
    assert str(col[5]) in resp and str(col[20]) in resp


def test_p2_s7_cita_el_recursivo_y_el_seno():
    e = c.cifras_c1_extrapolar()
    sec = s2()[7]
    assert f"{e['seno']['grado_7']['fuera']:.0f}" in sec
    assert f"{e['recursivo']['sin_anterior']['futuro']:.1f}" in sec
    assert f"{e['recursivo']['con_anterior']['futuro']:.2f}" in sec


def test_p2_s8_cita_las_256_funciones_y_la_mitad():
    sec = s2()[8]
    assert "256" in sec
    assert alguna(sec, ("\\tfrac12", "\\frac12", "\\frac{1}{2}", "1/2", "0.5"))


def test_p2_el_ejercicio_final_cita_el_polinomio_en_9_y_10():
    pi = c.cifras_c1_par_impar()
    resp = bloque(p2(), "ml-c1-resp-final-polinomios-y-capacidad").group(1)
    assert str(pi["grado_7"][9]) in resp and str(pi["grado_7"][10]) in resp


def test_p2_cierre_cita_las_cifras_que_hay_que_llevarse():
    k, e, i = c.cifras_c1_capacidad()[20], c.cifras_c1_elegir(), c.cifras_c1_inverso()
    cierre = plano(cierre_p2())
    assert f"N={k['N_menor_R']}" in cierre.replace(" ", "")
    assert str(e["veces_N_max_ent"]) in cierre
    assert f"{i['R_inverso']:.2f}" in cierre and f"{i['R_10']:.2f}" in cierre


# ---- frases y objetos fijos ----

def test_p2_la_capacidad_efectiva_es_optimizacion_y_no_cuarta_fuente():
    cuerpo = bloque(p2(), "ml-c1-obs-capacidad-efectiva").group(1)
    assert "optimización" in cuerpo
    assert "cuarta fuente" not in cuerpo
    assert not re.search(r"(cuarta|quinta) fuente", p2())


def test_p2_memorizar_es_el_vecino_junto_al_no_parametrico():
    m = bloque(p2(), "ml-c1-obs-no-parametrico")
    cerca = plano(p2()[max(0, m.start() - 600):m.end() + 600])
    assert ("La regla “memorizar” de la clase 0 (@ml-c0-memorizar-contra-ajustar) es el "
            "vecino más cercano: por eso tenía cero en lo visto") in cerca


def test_p2_s2_aproximar_no_es_aprender():
    assert "aproximar no es aprender" in plano(s2()[2]).lower()


def test_p2_los_objetos_que_cita_la_clase_2_existen():
    for ident in ("ml-c1-def-capacidad", "ml-c1-def-brecha", "ml-c1-teo-optimismo-entrenamiento",
                  "ml-c1-dem-optimismo-entrenamiento", "ml-c1-def-capacidad-como-restriccion",
                  "ml-c1-def-param-hiper"):
        bloque(p2(), ident)


def test_p2_la_brecha_es_solo_la_formula():
    cuerpo = bloque(p2(), "ml-c1-def-brecha").group(1)
    assert "R(\\widehat\\beta)-L_{\\text{ent}}(\\widehat\\beta)" in cuerpo.replace(" ", "")
    assert "suele" not in cuerpo and "crece" not in cuerpo


def test_p2_el_teorema_del_optimismo_usa_argmin():
    assert "arg\\,min" in bloque(p2(), "ml-c1-teo-optimismo-entrenamiento").group(1)


def test_p2_no_free_lunch_en_cuatro_pasos():
    cuerpo = bloque(p2(), "ml-c1-dem-no-free-lunch").group(1)
    pasos = re.findall(r"(?m)^\s*(\d+)\.\s", cuerpo)
    assert pasos == ["1", "2", "3", "4"], pasos


def test_p2_un_modelo_exitoso_va_en_nota():
    assert re.search(r"(?m)^> \[!NOTE\]\s*$\n> \*\*Un modelo exitoso", p2())


def test_p2_la_ultima_linea_de_lo_que_hay_que_llevarse_es_la_pregunta_de_la_clase_2():
    seccion = p2().split("## Lo que hay que llevarse", 1)[1].split("\n## ", 1)[0]
    ultimo = [r for r in seccion.strip().split("\n\n") if r.strip()][-1]
    assert "¿Cómo medimos $R$ sin la muestra enorme" in plano(ultimo)


def test_p2_no_cita_ids_de_las_clases_2_a_5():
    assert not re.search(r"@ml-c[2-5]-", p2())


def test_p2_ninguna_phi_omite_la_constante():
    for m in re.finditer(r"\\phi(?:_N)?(?:\(x\))?\s*=\s*\(\s*([^,)\s]+)", p2()):
        assert m.group(1) == "1", f"φ sin la constante: {m.group(0)}"


def test_p2_la_tendencia_de_la_brecha_es_observacion_en_prosa():
    # Entre la definicion y el teorema: «suele» (no es ley) y la cita al teorema.
    d = bloque(p2(), "ml-c1-def-brecha")
    t = bloque(p2(), "ml-c1-teo-optimismo-entrenamiento")
    entre = plano(p2()[d.end():t.start()])
    assert "suele" in entre and "@ml-c1-teo-optimismo-entrenamiento" in entre


def test_p2_el_alt_de_cada_figura_es_el_aria_label_de_su_svg():
    import html
    assets = CLASE.parent / "_assets"
    figuras = re.findall(r"!\[([^\]]*)\]\(\.\./_assets/(ml-c1-[a-z0-9-]+)\.svg\)", p2())
    assert len(figuras) == 8
    for alt, ident in figuras:
        svg = (assets / f"{ident}.svg").read_text(encoding="utf-8")
        aria = html.unescape(re.search(r'aria-label="([^"]*)"', svg).group(1))
        assert alt == aria, ident


def test_p2_la_lectura_cabe_en_su_presupuesto():
    import contrato_unidad as cu
    palabras = {}
    for n, texto in s2().items():
        pag = cu.parsear("## " + texto)
        palabras[n] = sum(cu.palabras(u.texto) for u in pag.unidades
                          if not u.excluida and not (set(u.contexto) & cu.DIRECTIVAS_FUERA_DE_TIEMPO))
    assert "~35 min de lectura" in p2()
    assert sum(palabras.values()) <= 35 * 80 * 1.1, palabras


def test_p1_s6_remite_a_la_capacidad_efectiva_de_la_pagina_2():
    # Arreglo mecanico de C1.T15: la remision de §6 de P1 deja de ir en palabras.
    assert "@ml-c1-obs-capacidad-efectiva" in s1()[6]


# ---- guion de NB02 ----

@lru_cache(maxsize=None)
def nb02():
    return leer(NB02)


def celda02(clave):
    m = re.search(r"(?ms)^### celda: " + re.escape(clave) + r"\s*$(.*?)(?=^### celda: |\Z)",
                  nb02())
    assert m, f"falta la celda {clave}"
    return m.group(1)


def test_nb02_tu_eliges_N_el_ajuste_elige_beta():
    assert "Tú eliges $N$; el ajuste elige $\\widehat\\beta$" in plano(celda02("bloque-3-mira"))


def test_nb02_la_parte_b_no_demuestra_el_teorema():
    assert "no demuestra" in plano(celda02("bloque-6-explica"))


def test_nb02_no_lleva_arrobas_ni_wikilinks():
    assert not re.search(r"@ml-|\[\[", nb02())


def test_nb02_cifras_de_los_bloques_en_su_celda():
    k, e = c.cifras_c1_capacidad()[20], c.cifras_c1_elegir()
    b2 = celda02("bloque-2-mira") + celda02("bloque-2-explica")
    assert f"{k['R'][4]:.3f}" in b2 or f"N = {k['N_menor_R']}" in b2 or \
        f"N={k['N_menor_R']}" in b2.replace(" ", "")
    b3 = celda02("bloque-3-mira") + celda02("bloque-3-explica")
    assert str(e["veces_N_max_ent"]) in b3

# --- fin tramo 1b ---


# --- tramo tarea ---
# --- fin tramo tarea ---
