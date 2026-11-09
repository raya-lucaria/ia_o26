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
    """Un numero como puede escribirlo la pagina: punto decimal, signo «−» o «-».
    Un negativo exige su signo (revision r1: aceptar el valor absoluto dejaba
    pasar un sesgo con el signo cambiado)."""
    s = f"{abs(v):.{d}f}"
    return (s,) if v >= 0 else (f"−{s}", f"-{s}")


def esta(v, t, d=1):
    """El numero aparece entero: ni pegado a otra cifra (51.2 no esta en 951.2 ni
    1.15 en 999.15) ni, si es positivo, precedido de un signo menos (revision r1:
    cuatro mutaciones de cifras pasaban las 20 pruebas por subcadena)."""
    for f in formas(v, d):
        antes = r"(?<![\d.])" if f[0] in "−-" else r"(?<![\d.−-])"
        if re.search(antes + re.escape(f) + r"(?![\d])", t):
            return True
    return False


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
    # el cierre da la media con su signo y lo dice con palabras («menos error»);
    # revision r3: con la mediana de cada panel al lado
    assert esta(op["sesgo_prueba"], llevarse(P1)) and "menos error" in llevarse(P1)


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

def test_ningun_recuadro_lleva_texto_en_la_linea_del_marcador():
    """«> [!TIP] **titulo**» publica el marcador «[!TIP]» como texto: Raya solo
    reconoce el recuadro si el marcador va solo en su linea (se vio en el build)."""
    malos = [f"{r.name}:{i}" for r in sorted(CLASE.glob("*.md"))
             for i, linea in enumerate(r.read_text(encoding="utf-8").splitlines(), 1)
             if re.match(r"^>\s*\[![A-Z]+\]\s*\S", linea)]
    assert not malos, malos

# --- fin tramo rapido ---


# --- tramo m ---

P3 = "3_sesgo_y_varianza.md"
G05 = "tools/cuadernos_ml/05_sesgo_y_varianza.texto.md"


def test_p3_la_dispersion_de_la_diana_en_la_seccion_1():
    sv = c.cifras_c2_sesgo_varianza()
    s1 = seccion(P3, 1)
    assert esta(sv["diana_12"]["desv"], s1) and esta(sv["diana_1"]["desv"], s1)


def test_p3_el_sesgo_en_x0_y_el_piso_en_la_seccion_2():
    sv = c.cifras_c2_sesgo_varianza()
    s2 = seccion(P3, 2)
    assert esta(sv["f_x0"], s2)
    assert esta(sv["diana_1"]["sesgo"], s2) and esta(sv["diana_12"]["sesgo"], s2)
    assert esta(sv["sigma2_e"], s2)
    assert all(sv[f"diana_{N}"]["fuera_eje"] == 0 for N in (1, 12))
    assert "Ninguna predicción queda fuera" in s2


def test_cada_figura_del_tramo_m_vive_en_un_figure_de_p3():
    import figuras_ml_c2 as fig
    assert set(fig._M) <= figuras_en(P3), set(fig._M) - figuras_en(P3)

# --- fin tramo m ---


# --- tramo completo ---


def test_p3_la_u_calculada_en_la_seccion_3_y_al_llevarse():
    sv = c.cifras_c2_sesgo_varianza()
    N = sv["N_estrella"]
    s3 = seccion(P3, 3)
    assert f"N^\\star={N}" in s3
    for k in ("sesgo2", "varianza", "total"):
        assert esta(sv[N][k], s3, 2), k
        assert esta(sv[N][k], llevarse(P3), 2), k
    assert esta(sv[N]["ruido"], s3)
    # la CV de una sola muestra (el hilo de P2) elige otro grado
    assert f"\\widehat N={c.cifras_c2_hilo()['N_min']}" in s3


def test_p3_las_curvas_de_aprendizaje_en_la_seccion_4():
    cu = c.cifras_c2_curva_aprendizaje()
    s4 = seccion(P3, 4)
    for clave in ((1, 30), (1, 480), (1, 960), (10, 480), (10, 960)):
        assert esta(cu["R"][clave], s4), clave
    assert esta(cu["piso"], s4)
    # la mediana del grado 10 con 30 entregas no se cita (DECISION prog-c2-9.1)
    assert not esta(cu["R"][(10, 30)], s4)
    assert f"{cu['elegido'][30]:.0f} con 30" in s4 and f"{cu['elegido'][960]:.0f} con 960" in s4
    assert esta(cu["R"][(1, 960)], llevarse(P3)) and esta(cu["R"][(10, 960)], llevarse(P3))


def test_p3_el_diagnostico_de_los_cuatro_procesos_en_la_seccion_5():
    dg = c.cifras_c2_diagnostico()
    s5 = seccion(P3, 5)
    for nombre, r in dg.items():
        for k in ("L_ent", "CV", "EE", "benchmark", "benchmark_ee", "dif_val",
                  "dif_val_ee", "dif_cv"):
            assert esta(r[k], s5), (nombre, k)
        assert esta(min(r["dif_por_pliegue"]), s5) and esta(max(r["dif_por_pliegue"]), s5)
        if r["mejor_mas_flexible"] is not None:
            assert f"{r['mejor_mas_flexible']}: " in s5, nombre
    hojas = {"A": "subajuste", "B": "sobreajuste", "C": "no aprende", "D": "listo"}
    assert {n: r["hoja"] for n, r in dg.items()} == hojas
    for nombre, hoja in hojas.items():
        assert f"**{nombre}: {hoja}" in s5, nombre


def test_p3_el_ejercicio_final_cita_al_consultor():
    fi = c.cifras_c2_diagnostico_final()
    t = texto(P3)
    i, j = t.find("## Ejercicio final"), t.find("## Para profundizar")
    assert 0 <= i < j
    ej = t[i:j]
    for nombre in ("A", "B"):
        for n in c.N_CONSULTOR:
            assert esta(fi[nombre][n]["L_ent"], ej) and esta(fi[nombre][n]["CV"], ej), (nombre, n)
    assert fi["A"]["mejora"] > 0.2 and abs(fi["B"]["mejora"]) < 0.01


def test_guion_05_cita_la_diana_las_curvas_y_el_diagnostico():
    sv, cu, dg = (c.cifras_c2_sesgo_varianza(), c.cifras_c2_curva_aprendizaje(),
                  c.cifras_c2_diagnostico())
    g = texto(G05)
    assert esta(sv["f_x0"], g) and esta(sv["diana_12"]["desv"], g)
    assert esta(sv["diana_1"]["sesgo"], g) and esta(sv["diana_12"]["sesgo"], g)
    for clave in ((1, 30), (1, 480), (10, 480), (10, 960)):
        assert esta(cu["R"][clave], g), clave
    assert esta(dg["A"]["CV"], g) and esta(dg["B"]["CV"], g) and esta(dg["B"]["L_ent"], g)
    assert esta(dg["C"]["dif_val"], g) and esta(dg["C"]["dif_val_ee"], g)


def test_cada_figura_del_tramo_completo_vive_en_un_figure_de_p3():
    import figuras_ml_c2 as fig
    usadas = figuras_en(P3)
    assert set(fig._COMPLETO) <= usadas, set(fig._COMPLETO) - usadas

# --- fin tramo completo ---


# --- ronda 1 de revision ---

G_TAREA = "tools/cuadernos_ml/tarea_2_separar_y_elegir.texto.md"
LITERAL_BENCHMARK = "la media de entrenamiento como punto de comparación; la clase 3 lo define"


def test_r1_p1_la_cobertura_con_200_y_el_benchmark_que_le_gana_al_modelo():
    pr, im = c.cifras_c2_prueba_ruidosa(), c.cifras_c2_imitar()
    assert f"{100 * pr['cobertura_200']:.0f} %" in seccion(P1, 3)
    s5 = seccion(P1, 5)
    for contrato in ("el mes que viene", "otra ciudad"):
        a = im[contrato]["azar"]
        assert a["R"] > a["benchmark"], contrato     # el modelo pierde con la media
        assert esta(a["R"], s5) and esta(a["benchmark"], s5), contrato
    assert "“" not in texto(P1) and "”" not in texto(P1)


def test_r1_p1_el_teorema_no_regala_el_ejercicio_del_ee():
    t = texto(P1)
    i = t.find("::: theorem {#ml-c2-teo-prueba-insesgada")
    j = t.find(":::", t.find("\n", i) + 1)
    assert "1,1,4,4" not in t[i:j]


def test_r1_p2_el_reporte_de_prueba_en_el_cuerpo_del_seccion_3():
    h = c.cifras_c2_hilo()
    s3 = seccion(P2, 3)
    assert esta(h["L_prueba_un_ee"], s3) and esta(2 * h["ee_prueba_un_ee"], s3)
    assert esta(h["benchmark_prueba"], s3) and esta(2 * h["ee_benchmark_prueba"], s3)
    assert esta(h["dif_prueba"], s3) and esta(h["ee_dif_prueba"], s3)
    assert h["dif_prueba"] > 0                       # el elegido no le gana en prueba
    assert esta(h["R_por_N"][4], s3) and "48 entregas de desarrollo" in s3


def test_r1_p3_el_sesgo_no_baja_siempre():
    sv = c.cifras_c2_sesgo_varianza()
    s3 = seccion(P3, 3)
    assert "aumentar el grado reduce el sesgo y aumenta la varianza" not in s3
    assert esta(sv[9]["sesgo2"], s3) and esta(sv[12]["sesgo2"], s3)
    tope = max(sv["sesgo2_interior"][N] for N in range(6, 13))
    assert f"{tope:.2f}" in s3


def test_r1_p3_cada_ejercicio_lleva_titulo():
    sin = re.findall(r"(?m)^::: exercise \{#(ml-c2-[a-z0-9-]+)\}", texto(P3))
    assert not sin, sin


def test_r1_el_literal_del_benchmark_sin_arranque_repetido():
    for nombre in (P1, P2, P3, TAREA, G03, G_TAREA):
        t = texto(nombre)
        assert LITERAL_BENCHMARK in t, nombre
        assert "comparación (*benchmark*): la media" not in t, nombre
        assert "será la media de entrenamiento como punto" not in t, nombre


def test_r1_guion_03_la_prueba_de_200_y_el_taller():
    pr, h = c.cifras_c2_prueba_ruidosa(), c.cifras_c2_hilo()
    g = texto(G03)
    assert esta(pr["desv_200"], g, 2) and f"{100 * pr['cobertura_200']:.0f} %" in g
    assert esta(h["L_prueba_un_ee"], g, 2) and esta(h["benchmark_prueba"], g, 2)
    assert "“" not in g and "”" not in g


def test_r1_guion_05_avisa_del_sesgo_del_taller():
    t = c.cifras_c2_taller_descomponer()
    assert f"{t[12]['sesgo2']:.0f}" in texto(G05)

# --- fin ronda 1 ---


# --- ronda 2 de revision ---
# H4 (D-009.5): buscar por seccion o por archivo deja que una copia correcta
# (un texto alternativo, otra frase) encubra otra falsa. Cada copia publicada
# se lee en SU parrafo, sin textos alternativos, con su papel; y cada una
# tiene su mutacion en memoria.

def sin_alt(t):
    return re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)


def parrafo_de(t, ancla):
    """El unico parrafo (bloque entre lineas en blanco, sin textos
    alternativos) que contiene `ancla`."""
    ps = [p for p in re.split(r"\n\s*\n", sin_alt(t)) if ancla in p]
    assert len(ps) == 1, (ancla, len(ps))
    return ps[0]


def fila_de(t, prefijo):
    """La unica fila de tabla que empieza con `prefijo`."""
    fs = [r for r in t.splitlines() if r.startswith(prefijo)]
    assert len(fs) == 1, (prefijo, len(fs))
    return fs[0]


def celda_s5(columna):
    """Una celda de la tabla del diagnostico: fila buscada solo en la seccion 5
    (el ejercicio final tiene filas que empiezan igual) y leida por columna,
    para que una cifra repetida en otra columna no encubra la falsa."""
    def buscar(t, prefijo):
        return fila_de(secciones(t)[5], prefijo).split("|")[columna]
    buscar.columna = columna
    return buscar


def _copias():
    """(archivo, ancla, papel, valor, decimales, buscar): las cifras publicadas
    que tienen guarda por parrafo (o fila), con el parrafo donde viven. No son
    todas: varias cuentas de ejercicios solo se fijan en la fuente
    (test_ml_cifras_c2); revision r3, R2-H4."""
    pr, op, h = c.cifras_c2_prueba_ruidosa(), c.cifras_c2_optimismo(), c.cifras_c2_hilo()
    an, pa, dg = c.cifras_c2_anidada(), c.cifras_c2_pliegue_anomalo(), c.cifras_c2_diagnostico()
    cv, pm = c.cifras_c2_cv_vs_val(), op["sesgo_prueba_por_M"]
    P, F = parrafo_de, celda_s5
    cp = [
        (P1, "Ninguna tiene que estar mal", "desv con 20", pr["desv_20"], 1, P),
        (P1, "Ninguna tiene que estar mal", "desv con 200", pr["desv_200"], 1, P),
        (P1, "las medias de entrenamiento, validación y prueba", "L_ent medio",
         op["media_L_ent"], 1, P),
        (P1, "las medias de entrenamiento, validación y prueba", "L_val medio",
         op["media_L_val"], 1, P),
        (P1, "las medias de entrenamiento, validación y prueba", "L_prueba medio",
         op["media_L_prueba"], 1, P),
        (P2, "Con el grado 6 fijado", "L_prueba del final", h["L_prueba_un_ee"], 1, P),
        (P2, "Con el grado 6 fijado", "2 EE del final", 2 * h["ee_prueba_un_ee"], 1, P),
        (P2, "Con el grado 6 fijado", "benchmark en prueba", h["benchmark_prueba"], 1, P),
        (P2, "Con el grado 6 fijado", "2 EE del benchmark",
         2 * h["ee_benchmark_prueba"], 1, P),
        (P2, "Con el grado 6 fijado", "diferencia pareada", h["dif_prueba"], 1, P),
        (P2, "Con el grado 6 fijado", "EE de la diferencia", h["ee_dif_prueba"], 1, P),
        (P2, "Una sola entrega del borde", "perdida maxima", h["perdida_max_prueba"], 1, P),
        (P2, "Una sola entrega del borde", "R del final", h["R_un_ee"], 1, P),
        (P2, "Una sola entrega del borde", "R del benchmark", h["benchmark_despliegue"], 1, P),
        (P2, "En el caso 16, grado 1 da", "cociente grado 1", pa[1]["cociente"], 2, P),
        (G03, "Con los valores iniciales, $R=", "R congelado", pr["R"], 2, P),
        (G03, "Con los valores iniciales, $R=", "desv con 20", pr["desv_20"], 2, P),
        (G03, "elegir con la prueba da una media de", "sesgo con prueba",
         op["sesgo_prueba"], 2, P),
        (G03, "elegir con la prueba da una media de", "EE del sesgo", op["ee_prueba"], 2, P),
        (G03, "el taller imprime", "L_prueba del final", h["L_prueba_un_ee"], 2, P),
        (G03, "el taller imprime", "margen de 2 EE", 2 * h["ee_prueba_un_ee"], 2, P),
        (G03, "el taller imprime", "benchmark en prueba", h["benchmark_prueba"], 2, P),
        (G03, "el taller imprime", "diferencia pareada", h["dif_prueba"], 1, P),
        (G04, "la CV del ganador", "CV del ganador", an["cv_ganador"], 2, P),
        (G04, "la CV del ganador", "anidada", an["anidada"], 2, P),
        (G04, "la CV del ganador", "R del procedimiento", an["R_procedimiento"], 2, P),
        (G04, "la CV del ganador", "R del final", an["R_final"], 2, P),
        (G04, "pérdidas por pliegue entre", "minimo grado 1", min(pa[1]["por_pliegue"]), 2, P),
        (G04, "pérdidas por pliegue entre", "maximo grado 1", max(pa[1]["por_pliegue"]), 2, P),
        # revision r3 (R2-H4): G04 bloque 3 y G03 bloque del numero de candidatos
        (G04, "la desviación real es", "desv de validacion", cv["desv_val"], 2, P),
        (G04, "la desviación real es", "desv de CV", cv["desv_cv"], 2, P),
        (G04, "la desviación real es", "EE medio de validacion", cv["ee_val_medio"], 2, P),
        (G04, "la desviación real es", "EE medio de CV", cv["ee_cv_medio"], 2, P),
        (G03, "el primer cruce ocurre con", "media con M=7", pm[7], 2, P),
        (G03, "el primer cruce ocurre con", "media con M=6", pm[6], 2, P),
        (G03, "La tabla tampoco baja", "media con M=11", pm[11], 2, P),
        (G03, "La tabla tampoco baja", "media con M=12", pm[12], 2, P),
    ]
    for n, r in dg.items():
        fila = f"| {n} ({r['grado']}) |"
        cp.append((P3, fila, "L_ent", r["L_ent"], 1, F(2)))
        cp.append((P3, fila, "CV", r["CV"], 1, F(3)))
        cp.append((P3, fila, "EE", r["EE"], 1, F(3)))
        if r["mejor_mas_flexible"] is not None:
            cp.append((P3, fila, "CV del mas flexible", r["CV_mejor_mas_flexible"], 1, F(4)))
        cp.append((P3, f"| {n} | ", "benchmark", r["benchmark"], 1, F(2)))
        cp.append((P3, f"| {n} | ", "benchmark_ee", r["benchmark_ee"], 1, F(2)))
        cp.append((P3, f"| {n} | ", "dif_val", r["dif_val"], 1, F(3)))
        cp.append((P3, f"| {n} | ", "dif_val_ee", r["dif_val_ee"], 1, F(3)))
        cp.append((P3, f"| {n} | ", "dif_cv", r["dif_cv"], 1, F(4)))
        for v in (min(r["dif_por_pliegue"]), max(r["dif_por_pliegue"])):
            cp.append((P3, f"| {n} | ", "rango por pliegue", v, 1, F(4)))
    return cp


def _lista(valores, d):
    return "$" + ",".join(formas(v, d)[0] for v in valores) + "$"


def test_r2_p2_las_perdidas_por_pliegue_completas_y_en_orden():
    """Las cinco perdidas por pliegue del caso 16 como lista exacta: una cifra
    suelta («8», «5») se confunde con «grado 8» o con otro numero del parrafo."""
    pa = c.cifras_c2_pliegue_anomalo()
    parr = parrafo_de(texto(P2), "En el caso 16, grado 1 da")
    l1, l8 = _lista(pa[1]["por_pliegue"], 1), _lista(pa[8]["por_pliegue"], 0)
    assert l1 in parr and l8 in parr, (l1, l8)
    for lista in (l1, l8):                      # mutacion: un pliegue cambiado
        assert lista not in parr.replace(lista, lista.replace(",", ",9", 1))


COPIAS = _copias()
IDS_COPIAS = [f"{a.split('/')[-1]}·{b[:18]}·{p}·{i}" for i, (a, b, p, *_r) in enumerate(COPIAS)]


@pytest.mark.parametrize("copia", COPIAS, ids=IDS_COPIAS)
def test_r2_cada_copia_en_su_parrafo(copia):
    nombre, ancla, papel, v, d, buscar = copia
    assert esta(v, buscar(texto(nombre), ancla), d), (nombre, ancla, papel)


def _mutar(t, ancla, v, d, buscar):
    """Cambia la copia de `v` dentro del parrafo o fila de `ancla`, en memoria."""
    trozo = buscar(t, ancla)
    for f in formas(v, d):
        antes = r"(?<![\d.])" if f[0] in "−-" else r"(?<![\d.−-])"
        m = re.search(antes + re.escape(f) + r"(?![\d])", trozo)
        if m:
            nuevo = trozo[:m.start()] + "9" + f.lstrip("−-") + "9" + trozo[m.end():]
            if hasattr(buscar, "columna"):        # una celda: se cambia dentro de su fila
                fila = fila_de(secciones(t)[5], ancla)
                partes = fila.split("|")
                partes[buscar.columna] = nuevo
                trozo, nuevo = fila, "|".join(partes)
            assert t.count(trozo) == 1, ancla
            return t.replace(trozo, nuevo, 1)
    raise AssertionError((ancla, v))


@pytest.mark.parametrize("copia", COPIAS, ids=IDS_COPIAS)
def test_r2_mutar_una_copia_la_pone_en_rojo(copia):
    nombre, ancla, papel, v, d, buscar = copia
    malo = _mutar(sin_alt(texto(nombre)), ancla, v, d, buscar)
    assert not esta(v, buscar(malo, ancla), d), (nombre, ancla, papel)


def test_r2_p1_el_r_medio_del_elegido_junto_a_la_igualdad_de_esperanzas():
    op = c.cifras_c2_optimismo()
    s4 = sin_alt(seccion(P1, 4))
    assert esta(op["media_R"], s4) and esta(op["sesgo_validacion"], s4)
    assert esta(op["ee_validacion"], s4)
    # la diferencia de medias queda a menos de dos EE de cero: igualdad de esperanzas
    assert abs(op["sesgo_validacion"]) < 2 * op["ee_validacion"]
    assert op["media_R"] > 3 * op["media_L_prueba"]
    assert "esperanzas" in s4


def test_r2_p2_el_pliegue_2_interpola_y_el_3_extrapola():
    pa = c.cifras_c2_pliegue_anomalo()
    flags = {p: pa["extrapola_por_pliegue"][p - 1] for p in pa["pliegues_con_lejana"]}
    assert flags == {2: False, 3: True}
    s4 = seccion(P2, 4)
    assert "el pliegue 2 interpola y el 3 extrapola" in s4
    assert "extrapola y falla en ambos" not in s4
    g = texto(G04)
    assert "el pliegue 2 interpola y el 3 extrapola" in g
    assert "obligan a extrapolar" not in g


def test_r2_p3_la_brecha_grande_tiene_criterio_y_c_no_la_tiene():
    dg = c.cifras_c2_diagnostico()
    assert c.UMBRAL_BRECHA == 2.0
    s5 = seccion(P3, 5)
    assert "del doble de $L_{\\text{ent}}$" in s5
    C = dg["C"]
    vineta = next(r for r in s5.splitlines() if r.startswith("- **C: "))
    assert esta(C["CV"] - C["L_ent"], vineta) and esta(C["L_ent"], vineta)
    assert C["CV"] <= c.UMBRAL_BRECHA * C["L_ent"]
    # su brecha en minutos² es mayor que las de A y D: por eso hace falta el criterio
    assert C["CV"] - C["L_ent"] > max(dg[n]["CV"] - dg[n]["L_ent"] for n in "AD")


def test_r2_p3_el_sesgo_del_grado_12_no_se_niega():
    s3 = seccion(P3, 3)
    assert "tenga sesgo" not in s3 and "entrenamientos completos" not in s3
    for n in ("36", "48"):
        assert re.search(rf"(?<![\d.]){n}(?![\d])", s3), n


def test_r2_cada_tabla_numerada_lleva_titulo():
    sin = [f"{r.name}: {m}" for r in sorted(CLASE.glob("*.md"))
           for m in re.findall(r"(?m)^::: table \{#([a-z0-9-]+)\}", r.read_text(encoding="utf-8"))]
    assert not sin, sin
    assert "::: table {#ml-c2-tab-benchmark-contratos" in seccion(P1, 5)


def test_r2_guiones_sin_fragmento_suelto_de_la_semilla():
    for g in (G03, G04):
        malas = [r for r in texto(g).splitlines() if r.startswith("cambia la semilla:")]
        assert not malas, g

# --- fin ronda 2 ---


# --- ronda 3 de revision ---
# R2-H4: una cifra presente no basta; cada una va con su papel.

def _f(v, d):
    return formas(v, d)[0]


def test_r3_p1_cada_media_de_la_cadena_va_con_su_conjunto():
    op = c.cifras_c2_optimismo()
    parr = parrafo_de(texto(P1), "las medias de entrenamiento, validación y prueba")
    e, v, p = (_f(op[f"media_{k}"], 1) for k in ("L_ent", "L_val", "L_prueba"))
    frase = f"entrenamiento, validación y prueba son {e}, {v} y {p}"
    assert frase in parr, frase
    # mutacion del revisor: intercambiar entrenamiento y prueba
    malo = parr.replace(f"{e}, {v} y {p}", f"{p}, {v} y {e}")
    assert frase not in malo


def test_r3_g04_cada_desviacion_va_con_su_estimador():
    cv = c.cifras_c2_cv_vs_val()
    parr = parrafo_de(texto(G04), "la desviación real es")
    frase1 = f"{_f(cv['desv_val'], 2)} para validación y {_f(cv['desv_cv'], 2)}"
    frase2 = f"{_f(cv['ee_val_medio'], 2)} y {_f(cv['ee_cv_medio'], 2)}"
    assert frase1 in parr and frase2 in parr
    malo = parr.replace(_f(cv["desv_val"], 2), "9" + _f(cv["desv_val"], 2))  # 4.85 -> 94.85
    assert not esta(cv["desv_val"], malo, 2)
    assert cv["desv_cv"] < cv["desv_val"]          # «Aquí CV varía menos»


def test_r3_g03_el_primer_cruce_es_el_de_la_fuente():
    pm = c.cifras_c2_optimismo()["sesgo_prueba_por_M"]
    primero = min(M for M in pm if pm[M] < -2)
    assert primero == 7 and pm[6] >= -2
    parr = parrafo_de(texto(G03), "el primer cruce ocurre con")
    assert f"$M={primero}$: la media es {_f(pm[primero], 2)}" in parr
    assert f"Con $M={primero - 1}$ era {_f(pm[primero - 1], 2)}" in parr
    t = parrafo_de(texto(G03), "La tabla tampoco baja")
    assert f"pasa de {_f(pm[11], 2)} con $M=11$ a {_f(pm[12], 2)} con $M=12$" in t
    assert pm[12] > pm[11]



def test_r3_p1_los_dos_paneles_con_el_mismo_estadistico():
    """H4 de r3: arriba la media y abajo la mediana invitaba a leer mal; cada
    par (medianas, medias con EE) va en una misma frase, en §4 y al cierre."""
    op = c.cifras_c2_optimismo()
    medianas = (op["mediana_prueba"], op["mediana_validacion"])
    medias = (op["sesgo_prueba"], op["sesgo_validacion"])
    for t in (sin_alt(seccion(P1, 4)), llevarse(P1)):
        frases = re.split(r"(?<=[.;])\s+(?=[A-ZÁÉÍÓÚ])", t)
        assert any(all(esta(v, f) for v in medianas) and "median" in f for f in frases)
        assert any(all(esta(v, f) for v in medias) and esta(op["ee_validacion"], f)
                   and "media" in f for f in frases)
    assert op["mediana_prueba"] < op["mediana_validacion"] < 0
    # la media con la prueba a mas de cuatro EE bajo cero; la de validacion, a menos de dos
    assert -op["sesgo_prueba"] > 4 * op["ee_prueba"]
    assert "más de cuatro EE" in sin_alt(seccion(P1, 4)) and "más de cuatro EE" in llevarse(P1)


def test_r3_p1_la_frecuencia_no_se_vende_como_teorema():
    s4 = sin_alt(seccion(P1, 4))
    assert "casi siempre" not in s4
    assert "optimista en promedio" in s4
    assert "no una consecuencia del teorema" in s4


def test_r3_p3_el_sesgo_interior_es_un_promedio():
    sv = c.cifras_c2_sesgo_varianza()
    parr = parrafo_de(texto(P3), "En el tramo interior")
    assert "promediado sobre las entradas del tramo" in parr
    assert all(sv["sesgo2_interior"][N] <= 0.25 for N in range(6, 13))


def test_r3_p3_minutos_cuadrados_y_el_diagnostico_de_a():
    s5 = seccion(P3, 5)
    vineta = next(r for r in s5.splitlines() if r.startswith("- **C: "))
    assert "minutos²" in vineta
    fi = c.cifras_c2_diagnostico_final()
    a = fi["A"][min(c.N_CONSULTOR)]
    assert a["CV"] <= c.UMBRAL_BRECHA * a["L_ent"]          # A no cruza la pregunta 1
    t = texto(P3)
    resp = t[t.find("{#ml-c2-resp-final-sesgo-y-varianza"):]
    resp = resp[:resp.find("\n:::")]
    assert "sobreajusta" not in resp
    assert "no cruza el umbral de la pregunta 1" in resp


def test_r3_los_guiones_no_nombran_colores_del_tema_oscuro():
    for g in (G03, G04, G05):
        t = texto(g)
        assert "crema" not in t and "rosa" not in t, g
