"""Guardas de los diagramas de la unidad de juegos.

Mismas convenciones que test_gen_optimizacion.py: prefijo, raiz <svg> con
tamano propio, fondo del skin, <title> y <desc>, sin opacidades, XML valido,
sin huerfanos y sin SVG que ninguna pagina use. Ademas, comprueba que lo que
los diagramas dibujan coincide con el juego calculado.

Como alla, el fixture regenera antes de leer: lo que ata el archivo
comiteado a su generador es correr el generador y ver `git status` limpio.
"""
import re
from collections import Counter
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import pytest

import gen_juegos as gen
import juegos as j
from unidades import ASSETS_JUEGOS

FONDO = "#211033"


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    for nombre in gen.DIAGRAMAS:
        gen.escribir(nombre)


def _texto(nombre):
    return (ASSETS_JUEGOS / f"{nombre}.svg").read_text(encoding="utf-8")


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_existe_y_lleva_el_prefijo(nombre):
    assert nombre.startswith("jue-")
    assert (ASSETS_JUEGOS / f"{nombre}.svg").is_file()


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_la_raiz_svg_trae_sus_convenciones(nombre):
    texto = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", texto).group()
    for atributo in ('viewBox="', 'role="img"', "aria-label="):
        assert atributo in etiqueta
    assert re.search(r'\bwidth="\d', etiqueta) and re.search(r'\bheight="\d', etiqueta)
    assert f'fill="{FONDO}"' in texto
    assert "<title>" in texto and "<desc>" in texto
    assert "fill-opacity" not in texto and "stroke-opacity" not in texto
    ET.fromstring(texto)


def test_no_queda_ningun_svg_huerfano():
    en_disco = {p.stem for p in ASSETS_JUEGOS.glob("*.svg")}
    assert en_disco == set(gen.DIAGRAMAS)


def test_ningun_svg_sin_pagina_que_lo_use():
    unidad = ASSETS_JUEGOS.parent
    paginas = "\n".join(
        p.read_text(encoding="utf-8") for p in unidad.rglob("*.md")
        if not any(parte.startswith("_") for parte in p.relative_to(unidad).parts))
    sin_usar = sorted(s.name for s in ASSETS_JUEGOS.glob("*.svg") if s.name not in paginas)
    assert not sin_usar, f"SVG que ninguna pagina enlaza: {sin_usar}"


def test_cada_svg_tiene_su_fila_en_creditos():
    creditos = (ASSETS_JUEGOS / "CREDITOS.md").read_text(encoding="utf-8")
    for nombre in gen.DIAGRAMAS:
        assert f"`{nombre}.svg`" in creditos


def test_el_subgrafo_dibujado_es_el_del_juego():
    nodos = gen.subgrafo_n1()
    assert len(nodos) == 13 == j.contar_arbol(".BBBN.N.N")[0]
    assert [n for n, (t, p, _, _) in nodos.items() if j.ganador(t, p)] == [
        2, 5, 9, 10, 11, 12, 13]
    assert set(gen.LUGARES_N1) == set(nodos)


def test_la_transposicion_llega_al_mismo_estado():
    a = gen.jugar(j.inicio(), "B", gen.CAMINO_A)
    b = gen.jugar(j.inicio(), "B", gen.CAMINO_B)
    assert a == b
    # Y es el final n2 del subgrafo.
    t, p, _, _ = gen.subgrafo_n1()[2]
    assert a == (t, p)



def test_el_ciclo_nombra_las_siete_piezas_y_resalta_solo_elegir():
    svg = _texto("jue-ciclo-partida")
    for pieza in ("s₀", "un elemento de S", "Pl(s)", "A(s)", "T(s, a)", "U(s)"):
        assert pieza in svg, pieza
    # S_F se escribe con subindice: «S» y luego «F» abajo.
    assert re.search(r"S</tspan><tspan dy=\"[\d.]+\" font-size=\"[\d.]+\">F</tspan>", svg)
    # Una sola caja con el borde grueso de acento: la de elegir la jugada.
    gruesas = re.findall(rf'<rect [^>]*stroke="{gen.ACENTO}" stroke-width="4"', svg)
    assert len(gruesas) == 1
    assert "Elige una jugada" in svg


# ------------------------------------------------------------- clase 2 ---

def test_los_valores_dibujados_son_los_de_minimax():
    valores = gen.valores_n1()
    nodos = gen.subgrafo_n1()
    for n, (t, p, _, _) in nodos.items():
        assert valores[n] == j.valor(t, p)
    assert valores[1] == 1 and valores[3] == -1
    # Las jugadas resaltadas: c1-c2 en n1, c3xb2 en n3 y las tres de n6.
    elegidas = gen.elegidas_n1(valores)
    assert {h for p, h in elegidas if p == 1} == {2}
    assert {h for p, h in elegidas if p == 3} == {13}
    assert {h for p, h in elegidas if p == 6} == {7, 11, 12}
    svg = _texto("jue-minimax-n1")
    for n, (t, p, _, _) in nodos.items():
        if not j.ganador(t, p):
            assert f"V = {gen.fmt(valores[n])}" in svg


@pytest.mark.parametrize("paso", sorted(gen.PASOS_MINIMAX))
def test_cada_paso_de_minimax_escribe_el_valor_de_su_nodo(paso):
    n, _, _ = gen.PASOS_MINIMAX[paso]
    svg = _texto(f"jue-minimax-paso-{paso}")
    t, p, _, _ = gen.subgrafo_n1()[n]
    assert f"V = {gen.fmt(j.valor(t, p))}" in svg
    assert f">n{n}<" in svg


def test_la_memoria_de_minimax_es_un_camino():
    nodos = gen.subgrafo_n1()
    # El camino en la pila baja de padre a hijo, y lo ya devuelto va antes en
    # el orden de visita que lo que todavia no existe.
    for padre, hijo in zip(gen.EN_PILA, gen.EN_PILA[1:]):
        assert nodos[hijo][2] == padre
    assert max(gen.YA_DEVOLVIERON) < gen.EN_PILA[-1] < min(gen.SIN_GENERAR)
    svg = _texto("jue-minimax-genera")
    assert svg.count("aún no existe") == len(gen.SIN_GENERAR)
    assert svg.count("y se olvidó") == len(gen.YA_DEVOLVIERON) + 1  # mas la leyenda


def test_el_nodo_de_azar_promedia():
    svg = _texto("jue-azar-n3")
    assert "V = 1/3" in svg and svg.count(": ⅓") == 3


@pytest.mark.parametrize("invertir,generados,corte", [(False, 5, "alfa"), (True, 8, "beta")])
def test_alfa_beta_dibuja_lo_que_genera(invertir, generados, corte):
    nombre = "jue-alfa-beta-invertido" if invertir else "jue-alfa-beta-fijo"
    svg = _texto(nombre)
    visitas, cortes = gen.traza_n1(invertir)
    assert len(visitas) == generados == j.alfa_beta(".BBBN.N.N", "B", invertir=invertir)[1]
    assert f"{generados} de 13 nodos" in svg
    # Un fantasma por subarbol no generado, no uno por nodo.
    grupos = gen.FANTASMAS_INV if invertir else gen.FANTASMAS_FIJO
    assert sum(len(g) for g in grupos.values()) == 13 - generados
    assert svg.count(">?<") == len(grupos) == 2
    assert svg.count(">cuelga de él<") == 1
    assert list(cortes.values()) == [corte] and f"corte {corte}" in svg
    for orden in range(1, generados + 1):
        assert f">{orden}º<" in svg
    # El nodo que corta devuelve una cota, y la figura lo escribe asi.
    (padre, _), = cortes
    assert f">v = {gen.fmt(visitas[padre][4])} (cota)<" in svg
    assert f"devuelve v = {gen.fmt(visitas[padre][4])}, una cota" in svg
    assert padre == (6 if invertir else 3)
    # Bajo de los ~1480 px de antes.
    alto = int(re.search(r'<svg\b[^>]*\bheight="(\d+)"', svg).group(1))
    assert alto < 1000


# ------------------------------------------- alfa-beta por partes ---

NUEVAS_AB = ["jue-ab-ventana", "jue-ab-fijo-parte-1", "jue-ab-fijo-parte-2",
             "jue-ab-invertido-parte-1", "jue-ab-invertido-parte-2",
             "jue-ab-invertido-parte-3"]


def test_estan_las_figuras_de_alfa_beta_en_n1():
    assert set(NUEVAS_AB) <= set(gen.DIAGRAMAS)
    # Los arboles A, B y C se fueron: los sustituye el arbol T.
    assert not [n for n in gen.DIAGRAMAS if n.startswith(("jue-ab-arbol", "jue-ab-a-media"))]


@pytest.mark.parametrize("nombre", NUEVAS_AB)
def test_las_figuras_de_alfa_beta_se_leen_en_un_telefono(nombre):
    """Ancho de la unidad y letra minima de 22: en un telefono se leen sin
    acercarse."""
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    ancho = gen.ANCHO
    assert f'width="{ancho}"' in etiqueta and f'viewBox="0 0 {ancho} ' in etiqueta
    assert re.search(r'aria-label="[^"]{60,}"', etiqueta)
    # Toda la letra, salvo la B y la N de las piezas de los tableros.
    tamanos = [float(t) for t, contenido in
               re.findall(r'font-size="([\d.]+)"[^>]*>([^<]*)</text>', svg)
               if contenido not in ("B", "N")]
    assert min(tamanos) >= 22, (nombre, min(tamanos))


@pytest.mark.parametrize("nombre", NUEVAS_AB + ["jue-alfa-beta-fijo", "jue-alfa-beta-invertido"])
def test_ninguna_ventana_va_entre_corchetes_ni_un_numero_sin_su_letra(nombre):
    """La ventana es abierta, (α, β), y ningun renglon dice «= 3» a secas."""
    svg = _texto(nombre)
    renglones = re.findall(r">([^<>]+)</text>", svg)
    assert not [r for r in renglones if re.search(r"\[[^\]]*∞", r)], nombre
    assert not [r for r in renglones if re.match(r"\s*[=≤≥] ", r)], nombre


def test_la_ventana_marca_los_dos_cortes_de_t():
    svg = _texto("jue-ab-ventana")
    for rotulo in ("La ventana (α, β)", "v ≤ α:", "v ≥ β:", "corte alfa", "corte beta",
                   "aquí el valor", "D llega con (5, +∞)", "C2 llega con (3, 5)",
                   "2 ≤ 5: corte alfa", "7 ≥ 5: corte beta", "α = 5", "α = 3", "β = 5"):
        assert rotulo in svg, rotulo


def test_las_partes_del_orden_fijo_dibujan_su_traza():
    visitas, cortes = gen.traza_n1(False)
    assert cortes == {(3, 6): "alfa"}
    p1, p2 = _texto("jue-ab-fijo-parte-1"), _texto("jue-ab-fijo-parte-2")
    assert ">α = +1<" in p1 and ">por mirar<" in p1 and "corte" not in p1
    _, _, a3, b3, v3 = visitas[3]
    assert (a3, b3, v3) == (1, float("inf"), 1) and gen.valores_n1()[3] == -1
    assert "(+1, +∞)" in p2
    assert ">v ≤ α: corta<" in p2 and ">v = +1 (cota)<" in p2 and ">v = +1<" in p2
    assert "corte alfa" in p2 and p2.count(">?<") == 2 and "5 de 13" in p2


def test_las_partes_del_orden_invertido_dibujan_su_traza():
    visitas, cortes = gen.traza_n1(True)
    assert cortes == {(6, 11): "beta"}
    p1, p2, p3 = (_texto(f"jue-ab-invertido-parte-{k}") for k in (1, 2, 3))
    # n13 vale −1, y es lo primero que ve n3: β pasa de +∞ a −1.
    assert visitas[13][4] == -1 and visitas[6][3] == -1
    assert ">β: +∞ → −1<" in p1 and ">U = −1<" in p1 and "corte" not in p1
    assert "(−∞, −1)" in p2 and ">v ≥ β: corta<" in p2 and ">v = +1 (cota)<" in p2
    assert "corte beta" in p2 and p2.count(">?<") == 2
    assert visitas[3][4] == -1 and visitas[2][2:4] == (-1, float("inf"))
    # La raiz ya no mete «α = −1» y un «= +1» suelto en la misma caja.
    assert "(−1, +∞)" in p3 and "pero no ahorra" in p3 and ">v = +1<" in p3
    assert ">= +1<" not in p3 and "8 de 13" in p3


# ------------------------------------------------------------ el arbol T ---

FIGURAS_T = (["jue-t-arbol"] + [f"jue-t-minimax-{k}" for k in gen.PASOS_MINIMAX_T]
             + [f"jue-t1-ab-{k}" for k in gen.PASOS_AB_T1]
             + [f"jue-t-ab-{k}" for k in gen.PASOS_AB_T]
             + ["jue-t-ab-pila", "jue-t-azar", "jue-t-corte-d1",
                "jue-t-corte-d2-tramo-1", "jue-t-corte-d2", "jue-t-iterativa"])


def test_estan_todas_las_figuras_del_arbol_t():
    assert len(FIGURAS_T) == 19 and set(FIGURAS_T) <= set(gen.DIAGRAMAS)


@pytest.mark.parametrize("nombre", FIGURAS_T)
def test_las_figuras_de_t_caben_y_cada_numero_lleva_su_letra(nombre):
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert f'width="{gen.ANCHO_T}"' in etiqueta
    assert re.search(r'aria-label="[^"]{120,}"', etiqueta)
    tamanos = [float(t) for t in re.findall(r'font-size="([\d.]+)"', svg)]
    assert min(tamanos) >= 15, (nombre, min(tamanos))
    renglones = re.findall(r">([^<>]+)</text>", svg)
    assert not [r for r in renglones if re.match(r"\s*[=≤≥] ", r)], nombre
    assert not [r for r in renglones if re.search(r"\[[^\]]*,", r)], nombre


def test_la_banda_es_el_pseudocodigo_canonico():
    for k in gen.PASOS_MINIMAX_T:
        svg = _texto(f"jue-t-minimax-{k}")
        fila = j.traza_decidir(j.ARBOL_T)["filas"][gen._pasos_minimax_t()[k][0] - 1]
        for n in gen._lineas_banda(fila, False):
            assert escape(j.PSEUDO_MINIMAX[n]) in svg
    svg = _texto("jue-t-ab-3")
    for n in (12, 13, 14):
        assert escape(j.PSEUDO_ALFA_BETA[n]) in svg


def test_minimax_en_t_dibuja_su_traza():
    p1, p2, p3, p4 = (_texto(f"jue-t-minimax-{k}") for k in gen.PASOS_MINIMAX_T)
    assert ">mejor_jugada = izq<" in p1 and ">mejor_valor = 3<" in p1
    # El momento que describe la pagina: fila 12, pila R›C›C2, C2 con v = 7.
    assert gen._pasos_minimax_t()[2][0] == 12
    assert "la hoja 7 devuelve w = 7" in p2 and ">v = 7<" in p2 and ">C1 · MAX<" in p2
    assert ">mejor_jugada = centro<" in p3 and ">mejor_valor = 5<" in p3
    assert "2 &gt; 5 es falso" in p4 or "2 > 5 es falso" in p4


def test_alfa_beta_en_t1_y_t_dibuja_sus_cortes():
    t1 = [_texto(f"jue-t1-ab-{k}") for k in gen.PASOS_AB_T1]
    assert "v = 2 ≤ α = 3: corte alfa" in t1[1] and "corte alfa" in t1[2]
    assert "6 de 7 nodos" in t1[2] and t1[2].count(">?<") == 1 + 1  # mas la leyenda
    t = [_texto(f"jue-t-ab-{k}") for k in gen.PASOS_AB_T]
    assert ">mejor_jugada = izq<" in t[0] and ">α = 3<" in t[0]
    assert ">β = 5<" in t[1] and "v = 5 ≤ α = 3 es falso: β ← 5" in t[1]
    assert "v = 7 ≥ β = 5: corte beta" in t[2] and "valor exacto es 8" in t[2]
    assert "v = 2 ≤ α = 5: corte alfa" in t[3]
    assert "12 de 14 nodos" in t[4] and t[4].count(">?<") == 2 + 1  # mas la leyenda
    assert ">mejor_jugada = centro<" in t[4] and ">α = 5<" in t[4]


def test_la_pila_de_alfa_beta_es_la_del_corte_en_c2():
    svg = _texto("jue-t-ab-pila")
    for rot in ("R · DECIDIR", "C · MIN", "C2 · MAX", "mejor_jugada = izq", "va en: c2",
                "v ≥ β: corta", "devolvió 3", "devolvió 5", "se perdió al regresar"):
        assert rot in svg, rot
    assert svg.count(">?<") == 1


def test_azar_corte_e_iterativa_en_t():
    azar = _texto("jue-t-azar")
    for rot in ("v = 9/2", "v = 13/2", "v = 7", "mejor_jugada = der"):
        assert rot in azar, rot
    d1, d2 = _texto("jue-t-corte-d1"), _texto("jue-t-corte-d2")
    assert "EVAL = 5" in d1 and "EVAL = 4" in d1 and "EVAL = 7" in d1
    assert "mejor_jugada = der" in d1 and "4 de 14 nodos" in d1
    assert "EVAL = 6" in d2 and "EVAL = 9" in d2 and "mejor_jugada = centro" in d2
    assert "10 de 14 nodos" in d2
    it = _texto("jue-t-iterativa")
    for rot in ("orden: izq, centro, der · 4 nodos", "orden: der, izq, centro · 10 nodos",
                "orden: centro, izq, der · 11 nodos", "En total, 25 nodos"):
        assert rot in it, rot


# ------------------------------------------------------------- clase 3 ---

def test_las_figuras_de_corte_dibujan_las_evaluaciones_calculadas():
    p1 = _texto("jue-c3-corte-prof-1")
    for nombre, t, p in gen.hijos4(gen.POSICION_C3, "B"):
        assert f">EVAL = {gen.fmt_eval(gen.ev(t))}<" in p1
    assert ">con corte: 13<" in p1
    p2 = _texto("jue-c3-corte-prof-2")
    minimos = [min(gen.ev(t2) for _, t2, _ in gen.hijos4(t, p))
               for _, t, p in gen.hijos4(gen.POSICION_C3, "B")]
    assert minimos == [-10, 1, 0]
    for v in minimos:
        assert f">mínimo: {gen.fmt_eval(v)}<" in p2
    assert ">con corte: 1<" in p2
    # Cada EVAL de las hojas, sin signo de mas.
    for _, t, p in gen.hijos4(gen.POSICION_C3, "B"):
        for n2, t2, _ in gen.hijos4(t, p):
            assert f">{gen.fmt_eval(gen.ev(t2))}<" in p2
    assert ">−10<" in p2 and ">12<" in p2


def test_profundidad_3_dibuja_la_rama_d2_d3():
    svg = _texto("jue-c3-corte-prof-3")
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert 'width="520"' in etiqueta
    rama = next(h for h in j.arbol_con_corte(gen.POSICION_C3, "B", 3, 4)["hijos"]
                if h["jugada"] == gen.RAMA_PROF_3)
    for r in rama["hijos"]:
        assert f">{r['jugada']}<" in svg and ">máximo: 100<" in svg
        for h in r["hijos"]:
            assert f">{h['jugada']}<" in svg
    assert svg.count(">100<") == 2 and svg.count(">final<") == 2
    assert svg.count(">2<") == 2 and ">13<" in svg and ">mínimo: 100<" in svg
    assert "La rama tiene 8 nodos" in etiqueta


def test_el_horizonte_esconde_la_recaptura():
    svg = _texto("jue-c3-horizonte")
    assert "tras d2xc3" in svg and "tras b4xc3" in svg
    assert ">EVAL = 13<" in svg and "(EVAL = 0)" in svg
    # La recaptura no se genera: la caja punteada con «?», no un nodo.
    assert ">?<" in svg and ">no se genera<" in svg and "No se ve" not in svg
    assert ">horizonte (d = 1 en la raíz)<" in svg


def test_la_profundizacion_dibuja_lo_que_cada_busqueda_deja_listo():
    svg = _texto("jue-c3-profundizacion")
    assert [gen.jugada_lista(d)[0] for d in gen.PROFUNDIDADES_RELOJ] == ["d2xc3", "d2-d3", "d2-d3"]
    assert gen.jugada_lista(3)[1] == 100
    for d, c in zip(gen.PROFUNDIDADES_RELOJ, (4, 12, 33)):
        assert f"d = {d} · {c} nodos" in svg
    assert "entrega d2xc3" in svg and "entrega d2-d3" in svg
    # Cada reloj se nombra con texto: el circulo con numero es el orden de
    # visita en la leyenda de la unidad.
    assert "<circle" not in svg and ">reloj 1<" in svg and ">reloj 2<" in svg


def test_mcts_tiene_sus_cuatro_pasos():
    svg = _texto("jue-c3-mcts-pasos")
    for paso in ("Selección", "Expansión", "Simulación", "Retropropagación"):
        assert paso in svg
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    # Antes de la vuelta (tres paneles) y despues (uno), cada nodo con su G/N.
    for n, (g, s) in vuelta["antes"].items():
        assert svg.count(f">{g}/{s}<") >= 3, n
    for n in vuelta["camino"] + ["nuevo"]:
        g, s = vuelta["despues"][n]
        assert f">{g}/{s}<" in svg, n
    assert ">0/0<" in svg and "U = +1" in svg and "<circle" not in svg
    assert "la raíz pasa de 2/4 a 3/5" in svg


C3 = ["jue-c3-corte-prof-1", "jue-c3-corte-prof-2", "jue-c3-corte-prof-3",
      "jue-c3-horizonte", "jue-c3-profundizacion", "jue-c3-mcts-pasos",
      "jue-t-corte-d1", "jue-t-corte-d2-tramo-1", "jue-t-corte-d2", "jue-t-iterativa"]


@pytest.mark.parametrize("nombre", C3)
def test_las_marcas_de_la_clase_3(nombre):
    """Las marcas de la clase 3 (lente de consistencia, 2026-10): ningun EVAL
    ni 100·U con «+»; el <title> no corta frases con «. »; y el horizonte
    dice que su d es la de la raiz."""
    svg = _texto(nombre)
    renglones = [r.strip() for r in re.findall(r">([^<>]+)</text>", svg)]
    assert not [r for r in renglones if re.search(r"(EVAL|corte|mínimo|máximo)\D*\+\d", r)]
    assert not [r for r in renglones if re.fullmatch(r"\+\d+", r)], nombre
    titulo = re.search(r"<title>([^<]*)</title>", svg).group(1)
    assert not re.search(r"\. [a-záéíóú]", titulo), titulo
    if nombre.startswith("jue-t-corte"):
        # Se ven en «Minimax con corte», antes de que «Más allá del horizonte»
        # presente la palabra: la línea se llama corte, no horizonte.
        assert re.search(r">corte \(d = \d en la raíz\)<", svg), nombre
        assert "horizonte" not in svg, nombre


@pytest.mark.parametrize("nombre", ["jue-c3-corte-prof-1", "jue-c3-corte-prof-2",
                                    "jue-c3-corte-prof-3", "jue-c3-horizonte"])
def test_en_los_peones_de_la_clase_3_ningun_nodo_lleva_el_borde_de_nuevo(nombre):
    """La eleccion va en la flecha resaltada; el borde grueso de acento es
    «lo nuevo de ese paso», y estas figuras no son pasos de una serie."""
    svg = _texto(nombre)
    assert not re.search(rf'<rect [^>]*stroke="{gen.ACENTO}" stroke-width="3(\.5)?"', svg)


def test_el_tramo_1_de_d_2_es_parcial_y_el_final_resuelto():
    t1, fin = _texto("jue-t-corte-d2-tramo-1"), _texto("jue-t-corte-d2")
    traza = j.traza_decidir(j.ARBOL_T, profundidad=2, evaluar=j.EVAL_T)
    k = gen._fila_tramo_1(traza)
    assert k == 9 and traza["filas"][k - 1]["generados"] == 7
    assert "7 de 14 nodos hasta aquí" in t1 and "10 de 14 nodos" in fin
    assert ">mejor_jugada = centro<" in t1 and ">mejor_valor = 6<" in t1
    assert "Corte con d = 2, tramo 1 · centro sube a 6" in t1
    # D todavia por mirar (punteado, sin «?»); las hojas de C1 y C2, «?».
    assert ">D · MIN<" in t1 and t1.count(">?<") == 4 + 1      # mas la leyenda
    assert fin.count(">?<") == 4 + 1
    assert "D todavía por mirar" in re.match(r"<svg\b[^>]*>", t1).group()
    for svg in (t1, fin):
        assert ">corte (d = 2 en la raíz)<" in svg
    # Misma geometria: el mismo arbol en los mismos lugares.
    xy = lambda s: re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="108"', s)  # noqa: E731
    assert xy(t1) == xy(fin)


# ------------------------------------------ arbol T: ronda 2 de revision ---

def _bordes_de_acento(svg):
    """Cajas de nodo con el borde grueso de acento: la marca de «en la pila»."""
    return re.findall(rf'<rect [^>]*width="{gen.NODO_T_W}" height="{gen.NODO_T_H}"[^>]*'
                      rf'stroke="{gen.ACENTO}" stroke-width="3.5"', svg)


@pytest.mark.parametrize("nombre", ["jue-t-minimax-1", "jue-t-minimax-3", "jue-t-minimax-4",
                                    "jue-t1-ab-1", "jue-t-ab-1"])
def test_el_nodo_que_acaba_de_devolver_ya_no_esta_en_la_pila(nombre):
    """En una fila de R solo R sigue en la pila: el hijo que devolvio ya no
    lleva el borde de acento (lo lleva su flecha, que sube)."""
    assert len(_bordes_de_acento(_texto(nombre))) == 1, nombre


def test_a_c_le_llega_w_no_v():
    for nombre in FIGURAS_T:
        assert "solo le llegó" not in _texto(nombre), nombre
    assert "a C le llegó" in _texto("jue-t-ab-2")
    assert "A C le llegó w = 5" in _texto("jue-t-ab-pila")


def test_el_nodo_que_evalua_su_if_compara_el_numero_del_rival():
    casos = {"jue-t1-ab-2": ("α = 3 ← de MAX: se compara", "β = +∞ · suyo"),
             "jue-t-ab-2": ("α = 3 ← de MAX: se compara", "β = 5 · suyo"),
             "jue-t-ab-3": ("β = 5 ← de MIN: se compara", "α = 3 · suyo"),
             "jue-t-ab-4": ("α = 5 ← de MAX: se compara", "β = +∞ · suyo")}
    for nombre, (rival, propio) in casos.items():
        svg = _texto(nombre)
        assert rival in svg and propio in svg, nombre
        # En la etiqueta del nodo, el renglon del rival va relleno de acento.
        assert re.search(rf'<rect [^>]*fill="{gen.ACENTO}"[^>]*/><text [^>]*fill="{gen.FONDO}"',
                         svg), nombre


def test_la_iterativa_marca_las_cotas_de_d3():
    *_, (d, orden, t) = j.profundizacion_iterativa_t(j.ARBOL_T)
    cotas = sorted(n for n, e in t["filas"][-1]["estado"].items() if e.get("cota"))
    assert d == 3 and cotas == ["C2", "D", "I"]
    assert _texto("jue-t-iterativa").count(">· cota<") == len(cotas)


def test_el_arbol_t_no_dice_que_la_hoja_es_u():
    svg = _texto("jue-t-arbol")
    assert ">su número es lo que vale ese final.<" in svg and "es U" not in svg


_DEJAVU = "/usr/share/fonts/truetype/dejavu/"


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_nada_se_sale_y_el_titulo_y_el_pie_caben_en_un_telefono(nombre):
    """A 1280 px la columna util mide ~614: nada sale del lienzo de 600. A
    390 px la figura se ve desde la izquierda: lo que va pegado al margen
    izquierdo (titulo, pie, leyenda) cabe en ~340 px. Mide con DejaVu, la
    letra con que el navegador de esta maquina resuelve system-ui; sin ella,
    se salta. El texto girado (el carril del ciclo) no entra en la cuenta."""
    ImageFont = pytest.importorskip("PIL.ImageFont")
    import html
    import os
    if not os.path.isdir(_DEJAVU):
        pytest.skip("sin DejaVu")
    svg = _texto(nombre)
    ancho = float(re.search(r'width="([\d.]+)"', svg).group(1))
    assert ancho <= 600
    patron = (r'<text x="([\d.-]+)" y="[\d.-]+"[^>]*font-family="([^"]*)" '
              r'font-size="([\d.]+)" font-weight="(\w+)" text-anchor="(\w+)">([^<]*)</text>')
    for x, familia, tam, peso, anclaje, contenido in re.findall(patron, svg):
        archivo = (("DejaVuSansMono" if "mono" in familia else "DejaVuSans")
                   + ("-Bold" if peso == "700" else "") + ".ttf")
        w = ImageFont.truetype(_DEJAVU + archivo, round(float(tam))).getlength(
            html.unescape(contenido))
        x = float(x)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anclaje]
        assert x0 >= 0 and x0 + w <= ancho, (nombre, contenido)
        if anclaje == "start" and x <= gen.X_PIE + 4:
            assert x0 + w <= 345, (nombre, contenido, round(x0 + w))


# ------------------------------------------ todas caben en la columna ---

@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ninguna_figura_pasa_de_600_de_ancho(nombre):
    """A 1280 px la columna util de una figura mide ~614 px, y por debajo de
    ~1470 px el sitio no encoge los SVG (rich.css fija max-width: none para
    no bajar de letra legible): lo que pase de ahi se corta por la derecha.
    Asi se publicaron las figuras de 640 y 700 («n1…», «no gene…»). El
    viewBox mide lo mismo que el width: la figura no se escala, se rediseña."""
    etiqueta = re.match(r"<svg\b[^>]*>", _texto(nombre)).group()
    ancho = float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1))
    caja = re.search(r'viewBox="0 0 ([\d.]+) ', etiqueta).group(1)
    assert ancho <= 600, (nombre, ancho)
    assert float(caja) == ancho, nombre


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ninguna_letra_baja_de_12(nombre):
    """Minimo legible a escala 1. Salvo la B y la N de las piezas (van dentro
    de su circulo, en los tableros chicos) y los subindices (el F de S_F)."""
    svg = _texto(nombre)
    chicas = [(t, c) for t, c in re.findall(r'<text [^>]*font-size="([\d.]+)"[^>]*>([^<]*)<', svg)
              if float(t) < 12 and c not in ("B", "N")]
    assert not chicas, (nombre, chicas)


def test_las_figuras_de_alfa_beta_en_t_citan_la_fila_de_la_pagina():
    """Las tablas de la pagina numeran tambien las filas ✗ (la hoja podada,
    que solo esta en la traza de minimax); traza_decidir no las tiene. El
    aria-label cita el numero de la pagina, no el de la traza compacta. La
    fila esperada sale de pasos_interactivos, que numera como la pagina, y
    no de fila_pagina: asi las dos cuentas se vigilan una a otra."""
    def fila(variante, pred):
        return next(p["n"] for p in j.pasos_interactivos("alfa-beta", variante)["pasos"]
                    if p["linea"] and pred(p))  # una fila ✗ no tiene linea

    def ultima(variante):
        return j.pasos_interactivos("alfa-beta", variante)["pasos"][-1]["n"]

    raiz_i = lambda p: p["evento"] == "raiz" and p["hijo"] == "I"  # noqa: E731
    esperadas = {
        "jue-t1-ab-1": fila("T1", raiz_i),
        "jue-t1-ab-2": fila("T1", lambda p: p["corta"] == "alfa"),
        "jue-t1-ab-3": ultima("T1"),
        "jue-t-ab-1": fila("T", raiz_i),
        "jue-t-ab-2": fila("T", lambda p: p["nodo"] == "C" and p["hijo"] == "C1"),
        "jue-t-ab-3": fila("T", lambda p: p["corta"] == "beta"),
        "jue-t-ab-4": fila("T", lambda p: p["corta"] == "alfa"),
        "jue-t-ab-5": ultima("T"),
        "jue-t-ab-pila": fila("T", lambda p: p["corta"] == "beta"),
    }
    # Las que cita el texto de la pagina (4_alfa_beta.md): 5, 7, 10 y 5, 10,
    # 12, 17, 20.
    assert [esperadas[f"jue-t-ab-{k}"] for k in range(1, 6)] == [5, 10, 12, 17, 20]
    for nombre, n in esperadas.items():
        etiqueta = re.match(r"<svg\b[^>]*>", _texto(nombre)).group()
        assert re.findall(r"\(fila (\d+)", etiqueta) == [str(n)], nombre


_MUESTRA = re.compile(r'<rect x="([\d.]+)" y="([\d.]+)" width="(24|30)" height="(16|22|20)"')


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ningun_texto_de_leyenda_invade_la_muestra_siguiente(nombre):
    """Las muestras de las leyendas (cajitas de 24x16 o 30x22): ningun texto
    de su renglon puede pisarlas. Se publico «el va[muestra]lor» en
    jue-minimax-n1. Mide con DejaVu, como la prueba de los bordes."""
    ImageFont = pytest.importorskip("PIL.ImageFont")
    import html
    import os
    if not os.path.isdir(_DEJAVU):
        pytest.skip("sin DejaVu")
    svg = _texto(nombre)
    muestras = [(float(x), float(y), float(w), float(h)) for x, y, w, h in _MUESTRA.findall(svg)]
    patron = (r'<text x="([\d.-]+)" y="([\d.-]+)"[^>]*font-family="([^"]*)" '
              r'font-size="([\d.]+)" font-weight="(\w+)" text-anchor="start">([^<]*)</text>')
    for x, y, familia, tam, peso, contenido in re.findall(patron, svg):
        archivo = (("DejaVuSansMono" if "mono" in familia else "DejaVuSans")
                   + ("-Bold" if peso == "700" else "") + ".ttf")
        x, y, t = float(x), float(y), float(tam)
        w = ImageFont.truetype(_DEJAVU + archivo, round(t)).getlength(html.unescape(contenido))
        for mx, my, mw, mh in muestras:
            mismo_renglon = my < y and y - t < my + mh
            if mismo_renglon and mx > x - 1:
                assert x + w + 4 <= mx, (nombre, contenido, round(x + w), mx)


@pytest.mark.parametrize("nombre", FIGURAS_T)
def test_ningun_aria_label_deja_una_frase_vacia(nombre):
    """En la fila final no hay comparacion: «Abajo, la recta numérica: .»
    se publicaba vacia."""
    etiqueta = re.match(r"<svg\b[^>]*>", _texto(nombre)).group()
    assert not re.search(r":\s*\.", etiqueta), nombre


# ------------------------------- clase 3, p6: de donde sale el bono ---

UCB = ["jue-c3-hoeffding", "jue-c3-bono", "jue-c3-pago", "jue-c3-eligiendo-x",
       "jue-c3-bandido-corridas"]


@pytest.mark.parametrize("nombre", UCB)
def test_las_graficas_de_la_p6_nombran_sus_ejes_y_su_escala(nombre):
    """Ejes con nombre, marcas de escala de 14 px o mas, y el eje log dicho
    en el nombre del eje que lo es."""
    svg = _texto(nombre)
    renglones = re.findall(r">([^<>]+)</text>", svg)
    # Los nombres largos van partidos en renglones: las figuras miden 300 px
    # (ver ANCHO_UCB_MAX abajo).
    ejes = {"jue-c3-hoeffding": ("N(s′): simulaciones de la jugada",
                                 "frecuencia de ū(s′) ≤ μ(s′) − ε", "(escala log)"),
            "jue-c3-bono": ("N(s′): simulaciones de la jugada", "bono (en unidades de ū)"),
            "jue-c3-pago": ("N(s): vueltas (escala log)", "pago promedio por vuelta,",
                            "de la vuelta 1 a N(s)"),
            "jue-c3-eligiendo-x": ("N(s): vueltas (escala log)", "elecciones que van a x (%),",
                                   "en esas 10 vueltas"),
            "jue-c3-bandido-corridas": ("fracción de las 10 000 vueltas", "que fueron a x")}[nombre]
    for e in ejes:
        assert escape(e) in renglones, e
    marcas = {"jue-c3-hoeffding": ["0.001", "0.01", "0.1", "1", "0", "50", "200"],
              "jue-c3-bono": ["0", "1", "2", "3", "4", "50", "200"],
              "jue-c3-pago": ["10", "100", "1 000", "10 000", "0.3", "0.4", "0.5", "0.6"],
              "jue-c3-eligiendo-x": ["10", "100", "1 000", "10 000", "40", "55", "70", "85",
                                     "100"],
              "jue-c3-bandido-corridas": ["0", "0.25", "0.5", "0.75", "1"]}[nombre]
    for m in marcas:
        assert m in renglones, m
    assert ANCHO_UCB_MAX >= float(re.search(r'width="([\d.]+)"', svg).group(1))
    assert not re.findall(r'<text [^>]*font-size="(1[0-3](?:\.\d+)?)"', svg)


# A 390 px el sitio no escala los SVG: los pone a su ancho natural con scroll
# propio, y a 520 px jue-c3-bandido-corridas solo mostraba de 0 a ~0.6 (lo
# que importa esta cerca de 1); las otras tres perdian la leyenda o el final
# del eje x. El parrafo de la figura mide 305 px a 390 (medido en el sitio
# construido). Vale para todas las graficas de la p6.
ANCHO_UCB_MAX = 305


def test_hoeffding_dibuja_la_simulacion_y_la_cota():
    svg = _texto("jue-c3-hoeffding")
    pl = gen.plano_hoeffding()
    puntos = gen.puntos_hoeffding(pl)
    t = j.tabla_hoeffding()
    assert len(puntos) == len(j.NS_HOEFFDING) == 200      # ninguna frecuencia es 0
    circulos = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="2.6"', svg)
    # Cada punto es la frecuencia de la fuente (no la cota ni otra cosa)…
    esperados = [(pl.x(n), pl.y(float(t[n][0]))) for n in j.NS_HOEFFDING]
    assert [(float(x), float(y)) for x, y in circulos] == esperados
    assert [(x, y) for _, x, y in puntos] == esperados
    # …y queda bajo la cota (en pixeles: y mayor es mas abajo).
    for n, x, y in puntos:
        assert y >= pl.y(t[n][1]), n
    # La linea de la cota pasa por exp(−n·ε²/2) en cada n.
    linea_cota = re.search(rf'<polyline points="([^"]+)" fill="none" stroke="{gen.COLOR_COTA}"',
                           svg).group(1).split()
    assert linea_cota[99] == f"{pl.x(100)},{pl.y(j.cota_hoeffding(100, 0.2))}"
    # El aria-label cita lo que la pagina puede citar: n = 10, 50, 100.
    aria = re.match(r"<svg\b[^>]*>", svg).group()
    for n in (10, 50, 100):
        assert f"con N(s′) = {n}, {gen._pct(t[n][0])} contra una cota de {gen._pct(t[n][1])}" in aria
    assert "con N(s′) = 10, 24.7 % contra una cota de 81.9 %" in aria


def test_el_bono_dibuja_la_formula():
    svg = _texto("jue-c3-bono")
    pl = gen.plano_bono()
    for n in gen.MARCAS_MICRO_BONO:
        b = j.bono_ucb(100, n)
        assert f'<circle cx="{pl.x(n)}" cy="{pl.y(b)}" r="5"' in svg, n
    assert "el bono vale 1.92, 1.11, 0.78." in svg
    # Cuatro curvas: tres de c = 2√2 y la de c = 1; cada una baja con N(s′).
    curvas = re.findall(r'<polyline points="([^"]+)"', svg)
    assert len(curvas) == 4
    for c in curvas:
        ys = [float(p.split(",")[1]) for p in c.split()]
        assert all(a <= b for a, b in zip(ys, ys[1:]))   # en pixeles, hacia abajo
    # Ninguna curva pasa de N(s′) = N(s): un hijo no lleva mas simulaciones
    # que su padre (la de 100 llegaba a 200; auditoria de la 7.3). Orden de
    # dibujo: c = 1 con N(s) = 100, y luego CURVAS_BONO.
    ultimo_x = [float(c.split()[-1].split(",")[0]) for c in curvas]
    padres = [100, *gen.CURVAS_BONO]
    assert ultimo_x == [pl.x(min(n, pl.xs[1])) for n in padres]
    # Con mas N(s), mas bono: la curva de 10 000 va arriba de la de 100.
    primera = {n: j.bono_ucb(n, 5) for n in gen.CURVAS_BONO}
    assert primera[100] < primera[1000] < primera[10000] < 4


# jue-c3-pago y jue-c3-eligiendo-x reemplazan a jue-c3-bandido (la fraccion
# ACUMULADA en x, promediada sobre 40 corridas, mezclaba el costo de explorar
# con las corridas atoradas; el profesor no la entendio, 2026-10-12).

def _curvas_de(svg, pl, tabla, escala=1):
    for r, d in tabla.items():
        esperado = " ".join(f"{pl.x(m)},{pl.y(float(v * escala))}" for m, v in d.items())
        assert f'<polyline points="{esperado}"' in svg, r


def test_el_pago_dibuja_cada_regla_y_la_referencia():
    svg = _texto("jue-c3-pago")
    pl = gen.plano_pago()
    t = j.tabla_pago()
    assert list(t) == list(gen.ESTILO_REGLA) == list(j.FILAS_BANDIDO)
    _curvas_de(svg, pl, t)
    assert gen.puntos_pago(pl)["ucb"][0] == (10, pl.x(10), pl.y(float(t["ucb"][10])))
    # La referencia «siempre x» en μ(x) = 0.6, y ninguna curva la pasa.
    y_ref = pl.y(0.6)
    assert f'<line x1="{pl.x0}" y1="{y_ref}" x2="{pl.x0 + pl.w}" y2="{y_ref}"' in svg
    renglones = re.findall(r">([^<>]+)</text>", svg)
    assert "siempre x (lo mejor posible)" in renglones
    assert all(y > y_ref for pts in gen.puntos_pago(pl).values() for _, _, y in pts)
    # Lo que es un punto, en el dibujo; la leyenda con el valor final.
    assert "cada punto: promedio de 40 corridas" in renglones
    for fila in ("siempre el mejor promedio: 0.543", "a veces al azar (10 %): 0.564",
                 "UCB, c = 2√2: 0.580", "UCB, c = 1: 0.598"):
        assert fila in renglones, fila
    assert "(34·0.6 + 5·0.3 − 0.2)/40 = 0.5425." in renglones
    aria = re.match(r"<svg\b[^>]*>", svg).group()
    for frase in ("Cada punto es el promedio de 40 corridas",
                  "pago promedio por vuelta, el promedio de los U de las vueltas 1 a N(s)",
                  "Una raya horizontal en 0.6: siempre x, lo mejor posible",
                  "siempre el mejor promedio, 0.400, 0.533, 0.544 y 0.543",
                  "a veces al azar (10 %), 0.385, 0.522, 0.561 y 0.564",
                  "UCB, c = 2√2, 0.295, 0.397, 0.519 y 0.580",
                  "UCB, c = 1, 0.340, 0.514, 0.583 y 0.598",
                  "34 corridas se quedan en x, 5 en y y 1 en z",
                  "(34·0.6 + 5·0.3 − 0.2)/40 = 0.5425; simulado, 0.543"):
        assert frase in aria, frase


def test_eligiendo_x_dibuja_cada_regla_sin_acumular():
    svg = _texto("jue-c3-eligiendo-x")
    pl = gen.plano_eligiendo()
    t = j.tabla_eligiendo_x()
    _curvas_de(svg, pl, t, escala=100)
    renglones = re.findall(r">([^<>]+)</text>", svg)
    # Que es un punto (elecciones, no corridas: lente de correccion r2, H5)
    # y que no es acumulado, en el dibujo.
    for r_ in ("¿Qué tanto se elige x?", "cada punto: 40 corridas × 10 vueltas",
               "(de N(s) − 9 a N(s)), no acumulado", "elecciones que van a x (%),",
               "en esas 10 vueltas"):
        assert r_ in renglones, r_
    assert not [r_ for r_ in renglones if "corridas que eligen" in r_]
    for fila in ("siempre el mejor promedio: 85 %", "a veces al azar (10 %): 92.5 %",
                 "UCB, c = 2√2: 98.8 %", "UCB, c = 1: 100 %"):
        assert fila in renglones, fila
    # Sin bono, y solo ahi, el porcentaje de elecciones es el de corridas.
    assert "Sin bono, 85 % son justo 34 corridas" in renglones
    assert "de 40: entre las vueltas 100 y 10 000," in renglones
    assert "las 6 atoradas no eligen x." in renglones
    assert not [r_ for r_ in renglones if "nunca eligen" in r_]
    assert "0.9 + 0.1/3 = 93.3 %." in renglones
    # La meseta de 85 % es una recta: desde N(s) = 100, la misma y.
    ys = {y for m, _, y in gen.puntos_eligiendo(pl)["mejor_promedio"] if m >= 100}
    assert ys == {pl.y(85)}
    aria = re.match(r"<svg\b[^>]*>", svg).group()
    assert "corridas que eligen" not in aria and "nunca eligen" not in aria
    for frase in ("porcentaje de las elecciones que van a x, no acumulado",
                  "cada punto cuenta 400 elecciones: las vueltas N(s) − 9 a N(s) de cada una "
                  "de las 40 corridas",
                  "siempre el mejor promedio, 61.3 %, 85 %, 85 % y 85 %",
                  "a veces al azar (10 %), 60.3 %, 84 %, 93 % y 92.5 %",
                  "UCB, c = 2√2, 41.8 %, 65 %, 91.8 % y 98.8 %",
                  "UCB, c = 1, 54.5 %, 83.3 %, 99.5 % y 100 %",
                  "se aplana en 85 %, que aquí sí son 34 de 40 corridas: entre las vueltas "
                  "100 y 10 000, las 6 atoradas no eligen x y las otras 34 sí",
                  "0.9 + 0.1/3 = 93.3 %"):
        assert frase in aria, frase


def test_las_reglas_se_distinguen_sin_color():
    """Cada regla con su trazo y su marca: el color no es la unica senal."""
    assert len({(e["guiones"], e["marca"]) for e in gen.ESTILO_REGLA.values()}) == len(gen.ESTILO_REGLA)


def test_las_corridas_dibujan_cada_corrida_y_su_promedio():
    """jue-c3-bandido-corridas: 40 marcas por fila, con la marca de su regla
    y ninguna encima de otra; la raya del promedio en la x del valor final
    de tabla_bandido; el rotulo de atoradas y el de las buenas con sus
    cifras."""
    svg = _texto("jue-c3-bandido-corridas")
    pl = gen.plano_corridas()
    r, t = j.reparto_bandido(), j.tabla_bandido()
    pts = gen.puntos_corridas(pl)
    filas_px = gen.filas_corridas()
    assert list(pts) == list(j.FILAS_BANDIDO)
    for k, (fila, lista) in enumerate(pts.items()):
        e = gen.ESTILO_REGLA[fila]
        top, fondo, alto = filas_px[k]
        assert len(lista) == j.CORRIDAS_BANDIDO == 40
        assert [f for _, f, _, _ in lista] == r[fila]["fracciones"]
        for _, f, x, y in lista:
            assert top < y <= fondo and fondo + 14 <= top + alto, (fila, f)
            assert gen.marca_corrida(x, y, e["marca"], e["color"]) in svg, (fila, f)
        # Ninguna marca encima de otra: a un paso en x o en y.
        lugares = [(x, y) for _, _, x, y in lista]
        assert all(max(abs(a[0] - b[0]), abs(a[1] - b[1])) >= gen.PASO_CORRIDAS - 0.11
                   for i, a in enumerate(lugares) for b in lugares[i + 1:]), fila
        # y el punto (2·R) cabe en el paso con hueco.
        assert 2 * gen.R_CORRIDAS + 0.6 <= gen.PASO_CORRIDAS
        xm = pl.x(t[fila][max(j.MARCAS_BANDIDO)])
        assert f'<line x1="{xm}" y1=' in svg, fila
        assert f"promedio {t[fila][max(j.MARCAS_BANDIDO)]:.2f}" in svg
        assert e["rotulo"] in svg
    # 34 en x: una columna en la x de 1; las 6 atoradas, una columna en 0.
    mejor = pts["mejor_promedio"]
    columnas = Counter(x for _, f, x, _ in mejor if f >= j.UMBRAL_ATORADA)
    assert dict(columnas) == {pl.x(1): 34}
    atoradas = Counter(x for _, f, x, _ in mejor if f < j.UMBRAL_ATORADA)
    assert dict(atoradas) == {pl.x(0): 6}
    # El promedio 0.85 cae en el hueco: lejos de las dos columnas.
    xm = pl.x(r["mejor_promedio"]["promedio"])
    assert pl.x(0) + 20 < xm < pl.x(1) - 20
    renglones = re.findall(r">([^<>]+)</text>", svg)
    assert renglones.count("34 en x, 0.99 o más") == 1
    # Cada fila sin atoradas rotula su rango real (lente r3, H3).
    for r_ in ("de 0.90 a 0.94", "de 0.92 a 0.96", "de 0.96 a 1.00"):
        assert renglones.count(r_) == 1, r_
    # «6 de 40 atoradas: 5 en y, 1 en z» va en dos renglones: en uno llegaba
    # a la raya del promedio 0.85; igual el subtitulo, por el ancho.
    assert ["6 de 40 atoradas:", "5 en y, 1 en z"] == [
        r_ for r_ in renglones if r_.startswith("6 de 40") or r_ == "5 en y, 1 en z"]
    assert renglones.count("0 de 40 atoradas") == 3
    assert "cada punto es una corrida" in renglones and "de 10 000 vueltas" in renglones
    aria = re.match(r"<svg\b[^>]*>", svg).group()
    for frase in ("Cada punto es una corrida de 10 000 vueltas",
                  "La posición horizontal de cada punto es su valor, a ±0.01",
                  "Siempre el mejor promedio: 34 corridas en 0.99 o más y 6 atoradas en "
                  "0.001 o menos (5 en y, 1 en z), promedio 0.85",
                  "A veces al azar (10 %): ninguna atorada, de 0.903 a 0.938, promedio 0.93",
                  "UCB, c = 2√2: ninguna atorada, de 0.923 a 0.959, promedio 0.94",
                  "UCB, c = 1: ninguna atorada, de 0.955 a 0.999, promedio 0.99"):
        assert frase in aria, frase
    assert "corridas de la fila. Una columna junta" in renglones and "las corridas a 0.01 o menos de su x," in renglones


def test_cada_corrida_se_dibuja_en_su_valor():
    """La x de cada punto de jue-c3-bandido-corridas esta a ±0.01 de su
    fraccion (lente r3, H3): el apilado anterior las centraba en la mediana
    del grupo y pintaba de 0.88 filas que empiezan en 0.90. Se mide en el SVG
    publicado, no en puntos_corridas: cada marca, por su color y su y."""
    svg = _texto("jue-c3-bandido-corridas")
    pl = gen.plano_corridas()
    tol = 0.01 * pl.w + 0.1             # 0.01 en pixeles, mas el redondeo
    for fila, lista in gen.puntos_corridas(pl).items():
        e = gen.ESTILO_REGLA[fila]
        for _, f, x, y in lista:
            assert abs(x - (pl.x0 + pl.w * f)) <= tol, (fila, f, x)
            assert gen.marca_corrida(x, y, e["marca"], e["color"]) in svg
        # y la fila ocupa en x lo que su rango, a ±0.01 en cada punta.
        xs = [x for _, _, x, _ in lista]
        d = j.reparto_bandido()[fila]
        assert abs(min(xs) - (pl.x0 + pl.w * d["minimo"])) <= tol
        assert abs(max(xs) - (pl.x0 + pl.w * d["maximo"])) <= tol


# ------------------------- 7.3.7: el arbol T± (un arbol, todos) ---

def test_el_arbol_t_pm_cabe_en_la_columna_de_un_telefono():
    """A 390 px el sitio no escala los SVG y el parrafo mide ~305: la figura
    mide 300 o menos, y ninguna letra baja de 14."""
    svg = _texto("jue-t-pm-arbol")
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1)) <= 300
    tams = [float(t) for t in re.findall(r'<text [^>]*font-size="([\d.]+)"', svg)]
    assert tams and min(tams) >= 14


def test_el_arbol_t_pm_dibuja_el_arbol_de_la_fuente():
    svg = _texto("jue-t-pm-arbol")
    aria = re.search(r'aria-label="([^"]*)"', svg).group(1)
    ids = j.ids_tpm()
    signo = {1: "+1", -1: "−1", 0: "0"}
    for c, nombre in j.nombres_hojas_tpm().items():
        u = signo[j.nodo_en(j.ARBOL_TPM, c)]
        assert f"{nombre} = {u}" in aria, nombre
        assert f">{nombre}<" in svg
    # Sin EVAL (spec de la radiografia, §3.2): el arbol del juego solo tiene
    # jugadas y finales; la EVAL vive en las figuras de corte.
    assert "EVAL" not in svg
    assert f"con {j.contar_nodos(j.ARBOL_TPM)} nodos" in aria
    # Cada hoja con su borde doble: dos circulos por final.
    assert svg.count("<circle") == 2 * len(j.nombres_hojas_tpm())
    for nombre in ("I", "C", "D"):
        assert f">{nombre}<" in svg
    assert svg.count(">MIN<") == 3 and svg.count(">MAX<") == 2 and ">R · MAX<" in svg
    # La captura: su nombre en negritas del color de MIN y un trazo ancho de
    # ese color, uno por captura; el pie lo dice en palabras.
    capturas = [ids[c] for c in j.CAPTURAS_TPM]
    for nombre in capturas:
        assert re.search(rf'fill="{gen.COLOR_CAPTURA}"[^>]*font-weight="700"[^>]*>{nombre}<', svg)
        assert f"{nombre} es una captura de MIN" in aria
    assert svg.count(f'stroke="{gen.COLOR_CAPTURA}" stroke-width="6"') == len(capturas)
    assert ">La x de ix: es una captura de MIN.<" in svg


# ------------------ 7.3.6: radiografia (un arbol, cinco algoritmos) ---

RX_ARBOLES = ["jue-c3-rx-minimax", "jue-c3-rx-alfa-beta", "jue-c3-rx-corte",
              "jue-c3-rx-quietud", "jue-c3-rx-iterativa", "jue-c3-rx-mc-plano",
              "jue-c3-rx-uct-12", "jue-c3-rx-uct-40"]
RX_FLUJOS = [f"jue-c3-rx-flujo-{n}" for n in ("minimax", "alfa-beta", "corte", "mc-plano", "uct")]
MCG = ["jue-c3-mcg-arbol", "jue-c3-mcg-mc-plano", "jue-c3-mcg-uct-fases",
       "jue-c3-mcg-uct-crece"]


def _aria(nombre):
    return re.search(r'aria-label="([^"]*)"', _texto(nombre)).group(1)


def _renglones(nombre):
    import html
    return [html.unescape(r) for r in re.findall(r">([^<>]+)</text>", _texto(nombre))]


def test_estan_las_figuras_de_la_radiografia():
    for nombre in RX_ARBOLES + RX_FLUJOS + MCG:
        assert nombre in gen.DIAGRAMAS, nombre


@pytest.mark.parametrize("nombre", RX_ARBOLES + RX_FLUJOS + MCG)
def test_la_radiografia_cabe_en_un_telefono(nombre):
    """Como jue-t-pm-arbol: a 390 px el parrafo mide ~305 y el sitio no
    escala los SVG, asi que miden 300 o menos; la letra no baja de 12 (las
    hojas 100·U, en su pastilla) y casi todo va a 13 o mas."""
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1)) <= 300
    tams = [float(t) for t in re.findall(r'<text [^>]*font-size="([\d.]+)"', svg)]
    assert min(tams) >= 12
    assert sum(t < 13 for t in tams) <= 12, nombre


@pytest.mark.parametrize("nombre", RX_ARBOLES)
def test_cada_arbol_de_la_radiografia_marca_la_jugada_que_entrega(nombre):
    jugada = {"jue-c3-rx-minimax": j.minimax_tpm()[0],
              "jue-c3-rx-alfa-beta": j.alfa_beta_tpm("dado")[0],
              "jue-c3-rx-corte": j.corte_tpm(1)[0],
              "jue-c3-rx-quietud": j.quietud_tpm(1)[0],
              "jue-c3-rx-iterativa": j.iterativa_tpm()[0][-1][2],
              "jue-c3-rx-mc-plano": j.mc_plano_tpm(5, j.SEMILLA_TPM)[0],
              "jue-c3-rx-uct-12": j.uct_tpm(1, 12, j.SEMILLA_TPM)["mas_simulada"][-1],
              "jue-c3-rx-uct-40": j.uct_tpm(1, 40, j.SEMILLA_TPM)["mas_simulada"][-1]}[nombre]
    assert f"juega {jugada}" in _renglones(nombre)
    assert f"Juega {jugada}" in _aria(nombre) or f"juega {jugada}" in _aria(nombre)


def test_la_radiografia_dibuja_los_numeros_de_juegos():
    """Los datos de §7.1 del spec, leidos de juegos.py y buscados en cada
    figura: nodos, valores, cotas, podas, sumas y visitas."""
    jm, v, raiz, n = j.minimax_tpm()
    assert (jm, v, n) == ("centro", 0, 15)
    r = _renglones("jue-c3-rx-minimax")
    assert f"genera los {n} nodos" in r and not [x for x in r if "EVAL" in x and "Sin" not in x]

    ja, va, na, pod = j.alfa_beta_tpm("dado")
    r = _renglones("jue-c3-rx-alfa-beta")
    assert f"orden dado: {na} de {n} nodos" in r and na == 12
    assert "≥ +1" in r and "≤ −1" in r and "poda α" in r and "poda β" in r
    assert "C2: v = +1 ≥ β = 0, poda β." in r and "D: v = −1 ≤ α = 0, poda α." in r
    # cada hoja podada lleva su tachado (dos lineas de acento) y no su U
    assert _texto("jue-c3-rx-alfa-beta").count(f'stroke="{gen.ACENTO}" stroke-width="2.5"') \
        >= 2 * len(pod)

    jc, vc, ws, nc = j.corte_tpm(1)
    r = _renglones("jue-c3-rx-corte")
    assert (jc, vc, nc) == ("izq", 60, 4) and f"genera {nc} nodos y estima" in r
    for nombre in ("I", "C", "D"):
        assert f"EVAL {j.EVAL_TPM[nombre]}" in r
    assert "corte d = 1" in r and "−100" in r     # ix, detras del horizonte

    jq, vq, wq, nq, _ = j.quietud_tpm(1)
    r = _renglones("jue-c3-rx-quietud")
    assert (jq, vq, nq) == ("centro", 20, 5) and f"{nq} nodos: sigue la captura" in r
    assert "quedarse (EVAL 60) con" in r and "el menor, −100." in r

    filas, total = j.iterativa_tpm()
    r = _renglones("jue-c3-rx-iterativa")
    assert [f[2] for f in filas] == ["izq", "centro", "centro"] and total == 25
    for d, _, _, _, g in filas:
        assert f"d = {d} · {g} nodos" in r
    assert "4 + 9 + 12 = 25 nodos en total." in r
    assert "orden en la raíz: centro, izq, der" in r and "≥ 100" in r

    jp, sumas = j.mc_plano_tpm(5, j.SEMILLA_TPM)
    r = _renglones("jue-c3-rx-mc-plano")
    assert "izq −3, centro −2, der +3." in r and jp == "der"
    assert r.count("N 5") == 3 and {"ū −0.6", "ū −0.4", "ū +0.6"} <= set(r)
    sims = j.simulaciones_mc_plano_tpm(5, j.SEMILLA_TPM)
    assert sum(int(x[1:]) for x in r if re.fullmatch(r"×\d+", x)) == len(sims) == 15

    for vueltas, (nodos, ns, jugada) in {12: (10, (1, 4, 7), "der"),
                                        40: (15, (5, 26, 9), "centro")}.items():
        u = j.uct_tpm(1, vueltas, j.SEMILLA_TPM)
        assert len(u["N"]) == nodos and tuple(u["N"][(i,)] for i in range(3)) == ns
        r = _renglones(f"jue-c3-rx-uct-{vueltas}")
        assert f"c = 1, semilla 0: {nodos} nodos" in r and f"juega {jugada}" in r
        assert f"izq {ns[0]}, centro {ns[1]}, der {ns[2]}." in r
        # lo que aun no entra a su arbol va rayado: uno por nodo que falta
        faltan = 15 - nodos
        assert _texto(f"jue-c3-rx-uct-{vueltas}").count('stroke-dasharray="6 5"') >= 2 * faltan


def test_las_hojas_del_corte_van_en_100_u_sin_mas():
    """Las de corte cuentan los finales como 100·U, sin «+» (la convencion de
    las figuras de la clase 3), y las de U llevan su signo."""
    for nombre in ("jue-c3-rx-corte", "jue-c3-rx-quietud", "jue-c3-rx-iterativa"):
        r = _renglones(nombre)
        assert not [x for x in r if re.fullmatch(r"[≥≤]? ?\+\d+", x)], nombre
        assert not [x for x in r if re.search(r"EVAL \+", x)], nombre
    assert "+1" in _renglones("jue-c3-rx-minimax")


@pytest.mark.parametrize("nombre", RX_FLUJOS)
def test_cada_flujo_tiene_de_3_a_6_cajas_y_acaba_en_la_jugada(nombre):
    f = gen.FLUJOS[nombre.removeprefix("jue-c3-rx-flujo-")]
    cajas = [p for p in f["pasos"] if "caja" in p]
    assert 3 <= len(cajas) <= 6 and len(f["pasos"]) <= 7
    assert f["pasos"][-1].get("fin") and f["pasos"][-1]["caja"][0].startswith("Juega")
    r = _renglones(nombre)
    for p in f["pasos"]:
        for x in p.get("caja", p.get("rombo")):
            assert x in r, x


def test_el_flujo_de_uct_es_un_ciclo_de_cuatro_fases():
    r = _renglones("jue-c3-rx-flujo-uct")
    for fase in ("1 · Selección", "2 · Expansión", "3 · Simulación", "4 · Retropropagación"):
        assert fase in r
    assert "el tiempo?" in r and "no: otra vuelta" in r and "de la raíz más visitada" in r


def test_las_figuras_del_arbol_grande_no_llevan_cifras():
    """§9.5: simbolicas. Ningun digito en lo que se ve, salvo los de los
    numeros de fase («1 · Selección»)."""
    for nombre in MCG:
        r = [x for x in _renglones(nombre) if not re.match(r"\d · ", x)]
        assert not [x for x in r if re.search(r"\d", x)], nombre


def test_uct_en_el_arbol_grande_trae_el_caso_del_final():
    r = _renglones("jue-c3-mcg-uct-fases")
    assert "a un final ya en su árbol:" in r and "solo retropropaga su U" in r
    assert "frontera" in r


def test_la_frontera_de_uct_sigue_el_contorno_de_su_arbol():
    """No es una linea pareja: en las dos instantaneas con mas vueltas la
    frontera baja mas en una rama que en otra."""
    svg = _texto("jue-c3-mcg-uct-crece")
    lineas = re.findall(r'<polyline points="([^"]+)" fill="none" stroke="'
                        + gen.ACENTO + r'" stroke-width="2.5" stroke-dasharray="7 4"/>', svg)
    assert len(lineas) == len(gen.CRECE_UCT)
    alturas = [len({p.split(",")[1] for p in l.split()}) for l in lineas]
    assert alturas[0] == 1 and all(a >= 3 for a in alturas[1:]), alturas
