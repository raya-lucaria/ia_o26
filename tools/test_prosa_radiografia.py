"""La radiografía de la unidad 7 (sección 7.4) y sus páginas hermanas.

«Radiografía: un árbol, todos los algoritmos» (7.4.1) es la versión colapsada
de siete fichas —minimax, alfa-beta, expectiminimax, minimax con corte, Monte
Carlo plano, Monte Carlo con actualización minimax y UCT—, todas sobre el árbol
de resultados y con las etiquetas canónicas del plan de homologación (§3.3):
bloque «Qué valor rastrea / Dónde lo guarda / Cómo sube / A qué converge», las
cuatro partes numeradas y las siete viñetas de propiedades. Sus hermanas a
detalle son «Simular partidas» (7.3.3: Monte Carlo plano y actualización
minimax) y «MCTS con UCT» (7.3.4), que llevan las mismas partes.

Se retiró (homologación, plan §11.2) la comparación literal de la ficha de UCT
contra `.superpowers/unidad/juegos/radiografia/ficha-uct-v4.md`: ese archivo
está gitignorado (en CI la comparación nunca corría) y su notación (ū, G/N)
es la que §5.1 sustituyó por $\\widehat Q$. En su lugar, las anclas de esa
ficha son ahora fórmulas y frases de la ficha homologada. Ninguna prueba de
este archivo depende de un archivo fuera del repositorio.
"""
import re
from pathlib import Path

import juegos as j

UNIDAD = Path(__file__).resolve().parent.parent / "course/7_juegos"
CLASE_3 = UNIDAD / "3_cuando_no_cabe"
CLASE_4 = UNIDAD / "4_radiografia"
RX = CLASE_4 / "1_un_arbol_todos_los_algoritmos.md"
ELEGIR = CLASE_4 / "2_elegir_el_algoritmo.md"
SIMULAR = CLASE_3 / "3_simular_en_vez_de_evaluar.md"
MCG = CLASE_3 / "4_monte_carlo_en_un_arbol_grande.md"

# Sin cursivas en el título: el índice «On this page» imprime los asteriscos.
FICHAS = [
    "Minimax",
    "Alfa-beta",
    "Expectiminimax: otro juego, con un dado en D",
    "Minimax con corte: por nivel o por reloj",
    "Monte Carlo plano",
    "Monte Carlo con actualización minimax",
    "UCT",
]
BLOQUE = ["**Qué valor rastrea:**", "**Dónde lo guarda:**", "**Cómo sube:**",
          "**A qué converge:**"]
PARTES = [
    "#### 1 · Exploración: cómo obtiene su número",
    "#### 2 · Elección: qué jugada juega",
    "#### 3 · Propiedades",
    "#### 4 · Casos borde",
]
PROPIEDADES = ["**Número que da:**", "**Usa EVAL:**", "**Garantía:**",
               "**Se puede interrumpir:**", "**Complejidad:**",
               "**Frente a los demás:**", "**Supuestos:**"]
# Las fichas a detalle de las páginas hermanas: (página, título de la ficha).
FICHAS_A_DETALLE = [(SIMULAR, "Monte Carlo plano"),
                    (SIMULAR, "Monte Carlo con actualización minimax"),
                    (MCG, "UCT")]


def _texto(p):
    return p.read_text(encoding="utf-8")


def _ficha(texto, titulo):
    """Del `### ` de su título al siguiente `## ` o `### `."""
    i = texto.index("### " + titulo + "\n")
    m = re.compile(r"^#{2,3} ", re.M).search(texto, i + 4)
    return texto[i:m.start() if m else len(texto)]


def _fichas(texto):
    return {titulo: _ficha(texto, titulo) for titulo in FICHAS}


# En la radiografía (versión colapsada) las cuatro partes son párrafos en
# negrita, no `####`, para que el índice lateral no tenga 47 entradas (ola 4,
# r1, render #1); las páginas a detalle conservan los `####`.
PARTES_RX = ["**" + p[len("#### "):] + "**" for p in PARTES]


def _revisa_esqueleto(ficha, cual, partes_=PARTES):
    bloque = ficha[:ficha.index(partes_[0])]
    posiciones = [bloque.index(b) for b in BLOQUE]
    assert posiciones == sorted(posiciones), cual
    partes = [ficha.index(p) for p in partes_]
    assert partes == sorted(partes), cual
    propiedades = ficha[ficha.index(partes_[2]):ficha.index(partes_[3])]
    posiciones = [propiedades.index(p) for p in PROPIEDADES]
    assert posiciones == sorted(posiciones), cual
    assert "#####" not in ficha, cual


def test_la_radiografia_conserva_el_id_y_la_url_de_la_que_reemplaza():
    t = _texto(RX)
    assert re.search(r"^id: un-arbol-todos-los-algoritmos$", t, re.M)
    assert 'title: "Radiografía: un árbol, todos los algoritmos"' in t
    assert re.search(r"^id: monte-carlo-en-un-arbol-grande$", _texto(MCG), re.M)
    assert re.search(r"^title: MCTS con UCT$", _texto(MCG), re.M)
    assert re.search(r"^id: simular-en-vez-de-evaluar$", _texto(SIMULAR), re.M)


def test_las_siete_fichas_van_en_orden_con_las_mismas_cuatro_partes_y_siete_propiedades():
    t = _texto(RX)
    posiciones = [t.index("### " + f + "\n") for f in FICHAS]
    assert posiciones == sorted(posiciones)
    assert t.count("\n### ", t.index("## Las siete fichas"),
                   t.index("\n## ", t.index("## Las siete fichas") + 1)) == 7
    for titulo, ficha in _fichas(t).items():
        _revisa_esqueleto(ficha, titulo, PARTES_RX)
        assert "\n#### " not in ficha, titulo


def test_las_fichas_a_detalle_llevan_el_mismo_esqueleto_que_la_radiografia():
    for pagina, titulo in FICHAS_A_DETALLE:
        _revisa_esqueleto(_ficha(_texto(pagina), titulo), (pagina.name, titulo))


def test_cada_ficha_tiene_su_formula_en_negrita():
    f = _fichas(_texto(RX))
    assert r"\mathbf{V(s)=\max_{a\in A(s)} Q(s,a)}" in f[FICHAS[0]]
    assert r"\mathbf{v\ge\beta" in f[FICHAS[1]]
    assert r"\mathbf{V(s)=\sum_{a} \Pr(a\mid s)\,Q(s,a)}" in f[FICHAS[2]]
    assert r"\mathbf{V_0(s)=\mathrm{EVAL}(s)}" in f[FICHAS[3]]
    assert r"\mathbf{V_d(s)=M\cdot U(s)}" in f[FICHAS[3]]
    assert (r"\mathbf{\widehat Q(s_{\text{raíz}},a)=\frac{1}{N(s_{\text{raíz}},a)}\sum U}"
            in f[FICHAS[4]])
    assert r"\mathbf{\widehat V(s)=\max_{a\text{ visitada}}\widehat Q(s,a)}" in f[FICHAS[5]]
    assert r"\mathbf{\widehat V(s)=\min_{a\text{ visitada}}\widehat Q(s,a)}" in f[FICHAS[5]]
    assert r"\mathbf{\widehat Q(s,a)+\text{bono}}" in f[FICHAS[6]]
    assert r"\mathbf{\widehat Q(s,a)-\text{bono}}" in f[FICHAS[6]]
    for p in (RX, SIMULAR, MCG):
        t = _texto(p)
        assert r"\boldsymbol" not in t, p.name
        # Notación vieja que §5.1 eliminó.
        assert r"\bar u" not in t and not re.search(r"\\mu\b", t), p.name


def test_la_ficha_de_uct_dice_su_regla_de_eleccion_y_la_linea_de_min():
    """Anclas de la ficha homologada (antes: comparación literal con la ficha
    aprobada en `.superpowers/`, retirada por §11.2; ver el docstring)."""
    uct = _fichas(_texto(RX))[FICHAS[6]]
    assert r"\text{bono}=c\sqrt{\ln N(s)/N(s,a)}" in uct
    assert "el hijo más visitado (*robust child*)" in uct
    assert "el artículo original elige el mayor promedio" in uct
    assert ("**MIN minimiza $\\widehat Q-\\text{bono}$**, equivalente a maximizar "
            "$-\\widehat Q+\\text{bono}$") in uct
    # La utilidad por casos vive en la página a detalle, junto a «Final del juego».
    mcg = _texto(MCG)
    assert re.search(r"\\mathbf\{U\(s\)\}=\n\\begin\{cases\}\n\+1 & \\text\{si gana MAX\}", mcg)
    assert "(*robust child*)" in _ficha(mcg, "UCT")


def test_la_figura_base_del_arbol_de_resultados_no_lleva_eval_y_va_antes_que_las_fichas():
    t = _texto(RX)
    i = t.index("(../_assets/jue-t-pm-arbol.svg)")
    assert i < t.index("### " + FICHAS[0] + "\n")
    alt = t[t.rindex("![", 0, i):i]
    assert "EVAL" not in alt


def test_cada_ficha_lleva_su_arbol_de_resultados_y_su_diagrama_de_flujo():
    f = _fichas(_texto(RX))
    esperadas = {
        FICHAS[0]: ["jue-c3-rx-minimax", "jue-c3-rx-flujo-minimax"],
        FICHAS[1]: ["jue-c3-rx-alfa-beta", "jue-c3-rx-flujo-alfa-beta"],
        FICHAS[2]: ["jue-rx-expectiminimax", "jue-rx-flujo-expectiminimax"],
        FICHAS[3]: ["jue-c3-rx-corte", "jue-c3-rx-quietud", "jue-c3-rx-iterativa",
                    "jue-c3-rx-flujo-corte"],
        FICHAS[4]: ["jue-c3-rx-mc-plano", "jue-c3-rx-flujo-mc-plano"],
        FICHAS[5]: ["jue-rx-mmmc", "jue-rx-flujo-mmmc"],
        FICHAS[6]: ["jue-c3-rx-uct-12", "jue-c3-rx-uct-40", "jue-c3-rx-flujo-uct"],
    }
    for titulo, svgs in esperadas.items():
        for svg in svgs:
            assert f"(../_assets/{svg}.svg)" in f[titulo], (titulo, svg)


def test_los_titulos_de_las_figuras_dicen_la_jugada_que_calcula_el_codigo():
    t = _texto(RX)
    assert "T±" not in t
    assert j.minimax_tpm()[0] == "centro"
    assert 'title="Minimax en el árbol de resultados: genera los 15 nodos y juega centro"' in t
    ab = j.alfa_beta_tpm()
    assert (ab[2], ab[0]) == (12, "centro")
    assert 'title="Alfa-beta en el árbol de resultados: 12 de 15 nodos, la misma jugada"' in t
    assert j.expectiminimax_tpm()[0] == "der"
    assert ('title="Expectiminimax en el árbol de resultados con un dado en D: juega der"'
            in t)
    assert j.corte_tpm(1)[0] == "izq" and j.corte_tpm(1)[3] == 4
    assert 'title="Corte a d = 1 en el árbol de resultados: 4 nodos, juega izq"' in t
    assert j.mc_plano_tpm(5, 0)[0] == "der"
    assert ('title="Monte Carlo plano en el árbol de resultados: 5 simulaciones por jugada, '
            'juega der"') in t
    m = j.mc_minimax(j.ARBOL_TPM, j.ITERACIONES_MMMC_TPM, j.SEMILLA_TPM)
    assert j.JUGADAS_RAIZ[m["jugada"]] == "centro" and len(m["N"]) == 11
    assert (f'title="Actualización minimax en el árbol de resultados: '
            f'{j.ITERACIONES_MMMC_TPM} partidas, juega centro"') in t
    assert "11 estados guardados" in t


def test_las_paginas_hermanas_traen_sus_figuras_simbolicas_y_los_casos_que_pide_el_spec():
    t = _texto(MCG)
    # El árbol grande y Monte Carlo plano en él viven en «Simular partidas» (destinos.md R2).
    simular = _texto(SIMULAR)
    for svg in ["jue-c3-mcg-arbol", "jue-c3-mcg-mc-plano"]:
        assert f"(../_assets/{svg}.svg)" in simular, svg
    for svg in ["jue-c3-mcg-uct-fases", "jue-c3-mcg-uct-crece", "jue-c3-mcg-mezcla"]:
        assert f"(../_assets/{svg}.svg)" in t, svg
    assert "**Un final que ya está en el árbol.** Si la selección llega a él, solo retropropaga" in t
    assert "Esto es intuición;" in t
    assert ("**UCT no reemplaza el promedio por un mínimo: elige cada vez mejor, "
            "y así las partidas de buen juego dominan los promedios.**") in t
    assert "(*robust child*)" in t


def test_la_radiografia_va_sin_ejercicios_y_ninguna_con_referencias_hacia_adelante():
    """La radiografía es de consulta: sin ejercicios. «MCTS con UCT» y «Simular
    partidas» sí los traen desde que recibieron el recorrido a detalle
    (destinos.md R17): de ellas solo se exige que no remitan hacia adelante."""
    assert "::: exercise" not in _texto(RX)
    for p in (SIMULAR, MCG):
        assert "::: exercise" in _texto(p), p.name
    for p in (RX, SIMULAR, MCG, ELEGIR):
        t = _texto(p)
        assert not re.search(r"(?i)explicad[oa] (abajo|más adelante)|más abajo", t), p.name
        assert "<!--" not in t, p.name


def test_la_navegacion_va_de_simular_a_mcts_al_bono_a_la_tarea_y_a_la_radiografia():
    cierre = lambda p: _texto(p).rstrip().splitlines()[-1]
    assert cierre(SIMULAR) == "Continúa con [[monte-carlo-en-un-arbol-grande|MCTS con UCT]]."
    assert cierre(MCG) == "Continúa con [[de-donde-sale-el-bono|De dónde sale el bono]]."
    assert cierre(CLASE_3 / "5_de_donde_sale_el_bono.md") == (
        "Continúa con la [[tarea-cuando-no-cabe|tarea de la clase]].")
    assert "[[juegos-radiografia|" in cierre(CLASE_3 / "6_tarea.md")
    assert cierre(RX) == "Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]]."
    nombres = sorted(p.name for p in CLASE_3.glob("*.md"))
    assert nombres == ["0_index.md", "1_cortar_y_evaluar.md", "2_jugar_contra_el_reloj.md",
                       "3_simular_en_vez_de_evaluar.md", "4_monte_carlo_en_un_arbol_grande.md",
                       "5_de_donde_sale_el_bono.md", "6_tarea.md"]
    nombres = sorted(p.name for p in CLASE_4.glob("*.md"))
    assert nombres == ["0_index.md", "1_un_arbol_todos_los_algoritmos.md",
                       "2_elegir_el_algoritmo.md"]


def test_ningun_titulo_de_la_radiografia_ni_sus_hermanas_lleva_enfasis():
    """El índice lateral toma el texto crudo del encabezado: «Minimax (*minimax*)»
    se publicaba con los asteriscos (se vio en las capturas a 1280 px)."""
    for p in (RX, SIMULAR, MCG, ELEGIR):
        for linea in _texto(p).splitlines():
            if linea.startswith("#"):
                assert "*" not in linea, (p.name, linea)
