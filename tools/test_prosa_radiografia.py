"""Las dos páginas de la radiografía de la clase 7.3.

«Radiografía: un árbol, cinco algoritmos» (7.3.6) y «Monte Carlo y UCT en
un árbol grande» (7.3.7) reemplazaron a las tres páginas de comparación
(ahora en `_drafts/`). Estas guardas fijan lo que el profesor aprobó: cinco
fichas con las mismas tres partes, la ficha de UCT tal cual, la fórmula de
cada una, la figura base sin EVAL y la navegación 5 → 6 → 7 → 8 → tarea.
"""
import re
from pathlib import Path

import juegos as j

CLASE_3 = Path(__file__).resolve().parent.parent / "course/7_juegos/3_cuando_no_cabe"
P6 = CLASE_3.parent / "4_radiografia" / "1_un_arbol_todos_los_algoritmos.md"
P7 = CLASE_3 / "4_monte_carlo_en_un_arbol_grande.md"
FICHA_UCT = Path("/home/uumami/itam/ia_o26/.superpowers/unidad/juegos/radiografia/ficha-uct-v4.md")

# Sin cursivas en el título: el índice «On this page» imprime los asteriscos.
FICHAS = [
    "Minimax (minimax)",
    "Alfa-beta (alpha-beta pruning)",
    "Corte por nivel o por reloj (depth-limited search, iterative deepening)",
    "Monte Carlo plano (flat Monte Carlo)",
    "UCT (Upper Confidence bounds applied to Trees)",
]
PARTES = [
    "#### 1 · Exploración: cómo construye su estimación",
    "#### 2 · Elección: qué jugada juega",
    "#### 3 · Propiedades",
]
PROPIEDADES = ["**Número que da:**", "**Usa EVAL:**", "**Garantía:**",
               "**Se puede interrumpir (*anytime*):**", "**Complejidad"]


def _texto(p):
    return p.read_text(encoding="utf-8")


def _fichas(texto):
    """Cada ficha: del `### ` de su título al siguiente `## ` o `### `."""
    trozos = {}
    for titulo in FICHAS:
        i = texto.index("### " + titulo)
        m = re.compile(r"^#{2,3} ", re.M).search(texto, i + 4)
        trozos[titulo] = texto[i:m.start() if m else len(texto)]
    return trozos


def test_la_pagina_6_conserva_el_id_y_la_url_de_la_que_reemplaza():
    t = _texto(P6)
    assert re.search(r"^id: un-arbol-todos-los-algoritmos$", t, re.M)
    assert 'title: "Radiografía: un árbol, cinco algoritmos"' in t
    assert re.search(r"^id: monte-carlo-en-un-arbol-grande$", _texto(P7), re.M)


def test_las_cinco_fichas_van_en_orden_con_las_mismas_tres_partes_y_seis_propiedades():
    t = _texto(P6)
    posiciones = [t.index("### " + f) for f in FICHAS]
    assert posiciones == sorted(posiciones)
    for titulo, ficha in _fichas(t).items():
        partes = [ficha.index(p) for p in PARTES]
        assert partes == sorted(partes), titulo
        propiedades = ficha[ficha.index(PARTES[2]):]
        for prop in PROPIEDADES:
            assert prop in propiedades, (titulo, prop)
        assert "**Frente a" in propiedades, titulo


def test_cada_ficha_tiene_su_formula_en_negrita():
    f = _fichas(_texto(P6))
    assert r"\mathbf{V(s)=\max_{a\in A(s)} V(T(s,a))}" in f[FICHAS[0]]
    assert r"\mathbf{v\ge\beta" in f[FICHAS[1]]
    assert r"\mathbf{\mathrm{EVAL}(s)}" in f[FICHAS[2]]
    assert r"\mathbf{\bar u(s')=\frac{1}{N(s')}\sum U}" in f[FICHAS[3]]
    assert r"\mathbf{\bar u(s')+\text{bono}}" in f[FICHAS[4]]
    assert r"\boldsymbol" not in _texto(P6) + _texto(P7)


def test_la_ficha_de_uct_va_tal_cual_la_aprobo_el_profesor_mas_la_linea_de_min():
    """La ficha aprobada vive fuera del repo (`.superpowers/`, gitignorada):
    en un clon limpio esta parte se salta sola y quedan las anclas literales.

    El 2026-10-14 el profesor pidió, por legibilidad, la utilidad $U$ escrita
    como fórmula por casos junto a «Final del juego» (con su frase de entrada),
    subtítulos `#####` dentro de la exploración y un separador `---` entre
    fichas. Ese mismo día pidió además, al inicio de cada ficha, la lista de
    tres puntos «Qué valor rastrea / Dónde lo guarda / Cómo sube y a qué
    converge», igual en las cinco para comparar. La comparación literal quita
    esas cuatro cosas y nada más: el resto de la ficha tiene que seguir siendo,
    palabra por palabra, la aprobada."""
    uct = _fichas(_texto(P6))[FICHAS[4]]
    assert r"\mathbf{U(s)=\begin{cases}+1 & \text{si gana MAX}" in uct
    assert "la regla del **hijo más visitado (*robust child*)**" in uct
    assert "el artículo original usa la de mayor promedio" in uct
    assert ("Elegir el menor $\\bar u(s')-\\text{bono}$ equivale a elegir el mayor "
            "$-\\bar u(s')+\\text{bono}$") in uct
    if FICHA_UCT.exists():
        aprobada = FICHA_UCT.read_text(encoding="utf-8").strip().replace(
            "### UCT (*Upper Confidence bounds applied to Trees*)", "### " + FICHAS[4])
        sin_figuras = re.sub(r"\n*::: figure.*?\n:::", "", uct, flags=re.S).strip()
        sin_linea = re.sub(r" Elegir el menor .*?\]\]\.", "", sin_figuras)
        sin_formula_u = re.sub(
            r"\n\n\*\*Lo que promedia UCT es esa utilidad\*\*[^\n]*\n\n\$\$\n.*?\n\$\$", "",
            sin_linea, flags=re.S)
        sin_bloque = re.sub(
            r"\n\n- \*\*Qué valor rastrea:\*\*[^\n]*\n- \*\*Dónde lo guarda:\*\*[^\n]*"
            r"\n- \*\*Cómo sube y a qué converge:\*\*[^\n]*", "", sin_formula_u)
        sin_subtitulos = re.sub(r"\n\n##### [^\n]*", "", sin_bloque)
        sin_separador = re.sub(r"\n+---\s*$", "", sin_subtitulos)
        assert sin_separador == aprobada


def test_la_figura_base_de_t_mas_menos_no_lleva_eval_y_va_antes_que_las_fichas():
    t = _texto(P6)
    i = t.index("(../_assets/jue-t-pm-arbol.svg)")
    assert i < t.index("### " + FICHAS[0])
    alt = t[t.rindex("![", 0, i):i]
    assert "EVAL" not in alt


def test_cada_ficha_lleva_su_arbol_en_t_mas_menos_y_su_diagrama_de_flujo():
    f = _fichas(_texto(P6))
    esperadas = {
        FICHAS[0]: ["jue-c3-rx-minimax", "jue-c3-rx-flujo-minimax"],
        FICHAS[1]: ["jue-c3-rx-alfa-beta", "jue-c3-rx-flujo-alfa-beta"],
        FICHAS[2]: ["jue-c3-rx-corte", "jue-c3-rx-quietud", "jue-c3-rx-iterativa",
                    "jue-c3-rx-flujo-corte"],
        FICHAS[3]: ["jue-c3-rx-mc-plano", "jue-c3-rx-flujo-mc-plano"],
        FICHAS[4]: ["jue-c3-rx-uct-12", "jue-c3-rx-uct-40", "jue-c3-rx-flujo-uct"],
    }
    for titulo, svgs in esperadas.items():
        for svg in svgs:
            assert f"(../_assets/{svg}.svg)" in f[titulo], (titulo, svg)


def test_los_titulos_de_las_figuras_dicen_la_jugada_que_calcula_el_codigo():
    t = _texto(P6)
    assert j.minimax_tpm()[0] == "centro"
    assert 'title="Minimax en T±: genera los 15 nodos y juega centro"' in t
    ab = j.alfa_beta_tpm()
    assert (ab[2], ab[0]) == (12, "centro")
    assert 'title="Alfa-beta en T±: 12 de 15 nodos, la misma jugada"' in t
    assert j.corte_tpm(1)[0] == "izq" and j.corte_tpm(1)[3] == 4
    assert 'title="Corte a d = 1 en T±: 4 nodos, juega izq"' in t
    assert j.mc_plano_tpm(5, 0)[0] == "der"
    assert 'title="Monte Carlo plano en T±: 5 simulaciones por jugada, juega der"' in t


def test_la_pagina_7_trae_sus_figuras_simbolicas_y_los_casos_que_pide_el_spec():
    t = _texto(P7)
    # El árbol grande y Monte Carlo plano en él pasaron a «Simular partidas» (destinos.md R2).
    simular = _texto(P7.parent / "3_simular_en_vez_de_evaluar.md")
    for svg in ["jue-c3-mcg-arbol", "jue-c3-mcg-mc-plano"]:
        assert f"(../_assets/{svg}.svg)" in simular, svg
    for svg in ["jue-c3-mcg-uct-fases", "jue-c3-mcg-uct-crece"]:
        assert f"(../_assets/{svg}.svg)" in t, svg
    assert "**Cuando la selección llega a un final que ya está en el árbol, solo retropropaga.**" in t
    assert "**Esto es intuición, no garantía.**" in t
    assert "(*robust child*)" in t


def test_las_dos_paginas_van_sin_ejercicios_ni_referencias_hacia_adelante():
    for p in (P6, P7):
        t = _texto(p)
        assert "::: exercise" not in t, p.name
        assert not re.search(r"(?i)explicad[oa] (abajo|más adelante)|más abajo", t), p.name
        assert "<!--" not in t, p.name


def test_la_navegacion_va_de_la_5_a_la_6_a_la_7_al_bono_a_la_tarea():
    cierre = lambda p: _texto(p).rstrip().splitlines()[-1]
    assert cierre(CLASE_3 / "3_simular_en_vez_de_evaluar.md") == (
        "Continúa con [[un-arbol-todos-los-algoritmos|Radiografía: un árbol, cinco algoritmos]].")
    assert cierre(P6) == (
        "Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]].")
    assert "[[de-donde-sale-el-bono|De dónde sale el bono]]" in cierre(P7)
    assert cierre(CLASE_3 / "5_de_donde_sale_el_bono.md") == (
        "Continúa con la [[tarea-cuando-no-cabe|tarea de la clase]].")
    nombres = sorted(p.name for p in CLASE_3.glob("*.md"))
    assert nombres == ["0_index.md", "1_cortar_y_evaluar.md", "2_jugar_contra_el_reloj.md",
                       "3_simular_en_vez_de_evaluar.md", "4_monte_carlo_en_un_arbol_grande.md",
                       "5_de_donde_sale_el_bono.md", "6_tarea.md"]


def test_ningun_titulo_de_las_dos_paginas_lleva_enfasis():
    """El índice lateral toma el texto crudo del encabezado: «Minimax (*minimax*)»
    se publicaba con los asteriscos (se vio en las capturas a 1280 px)."""
    for p in (P6, P7):
        for linea in _texto(p).splitlines():
            if linea.startswith("#"):
                assert "*" not in linea, (p.name, linea)
