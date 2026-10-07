"""Guardas de los diagramas de la unidad de juegos.

Mismas convenciones que test_gen_optimizacion.py: prefijo, raiz <svg> con
tamano propio, fondo del skin, <title> y <desc>, sin opacidades, XML valido,
sin huerfanos y sin SVG que ninguna pagina use. Ademas, comprueba que lo que
los diagramas dibujan coincide con el juego calculado.

Como alla, el fixture regenera antes de leer: lo que ata el archivo
comiteado a su generador es correr el generador y ver `git status` limpio.
"""
import re
import xml.etree.ElementTree as ET

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
    cota = "≤" if corte == "alfa" else "≥"
    assert f"devuelve {cota} {gen.fmt(visitas[padre][4])}" in svg
    assert padre == (6 if invertir else 3)
    # Bajo de los ~1480 px de antes.
    alto = int(re.search(r'<svg\b[^>]*\bheight="(\d+)"', svg).group(1))
    assert alto < 1000


# ------------------------------------------- alfa-beta por partes ---

NUEVAS_AB = (["jue-ab-arbol-a-paso-%d" % k for k in gen.PASOS_ARBOL_A]
             + ["jue-ab-arbol-b-paso-%d" % k for k in gen.PASOS_ARBOL_B]
             + ["jue-ab-ventana", "jue-ab-fijo-parte-1", "jue-ab-fijo-parte-2",
                "jue-ab-invertido-parte-1", "jue-ab-invertido-parte-2",
                "jue-ab-invertido-parte-3", "jue-ab-a-media-ejecucion", "jue-ab-arbol-c"])


def test_estan_las_catorce_figuras_de_alfa_beta():
    assert len(NUEVAS_AB) == 14
    assert set(NUEVAS_AB) <= set(gen.DIAGRAMAS)


@pytest.mark.parametrize("nombre", NUEVAS_AB)
def test_las_figuras_de_alfa_beta_se_leen_en_un_telefono(nombre):
    """Ancho de la columna y letra minima de 22: el sitio las escala a ~350 px."""
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert 'width="700"' in etiqueta and 'viewBox="0 0 700 ' in etiqueta
    assert re.search(r'aria-label="[^"]{60,}"', etiqueta)
    # Toda la letra, salvo la B y la N de las piezas de los tableros.
    tamanos = [float(t) for t, contenido in
               re.findall(r'font-size="([\d.]+)"[^>]*>([^<]*)</text>', svg)
               if contenido not in ("B", "N")]
    assert min(tamanos) >= 22, (nombre, min(tamanos))


def _arbol(arbol, es_max):
    r = j.alfa_beta_arbol(arbol, es_max=es_max)
    return r, {c: (tipo, a, b, v, corte) for c, tipo, a, b, v, corte in r["traza"]}


def test_el_arbol_a_dibuja_su_traza():
    r, t = _arbol(j.ARBOL_A, True)
    assert (r["valor"], r["generados"], j.contar_nodos(j.ARBOL_A)) == (3, 6, 7)
    p1, p2, p3, p4 = (_texto(f"jue-ab-arbol-a-paso-{k}") for k in gen.PASOS_ARBOL_A)
    assert ">= 3<" in p1 and "min{3, 5}" in p1 and ">por mirar<" in p1
    assert ">α = 3<" in p2
    assert t[(1,)][1] == 3 and "[3, +∞]" in p3 and ">v = 2 ≤ 3<" in p3
    assert ">≤ 2<" in p4 and ">= 3<" in p4 and "corte alfa" in p4
    assert "6 de 7 nodos" in p4 and p4.count(">?<") == 1 and ">no se genera<" in p4
    # Antes del corte, «?» todavia no es un fantasma.
    for svg in (p1, p2, p3):
        assert "no se genera" not in svg and "corte" not in svg


def test_el_arbol_b_dibuja_su_traza():
    r, t = _arbol(j.ARBOL_B, False)
    assert (r["valor"], r["generados"]) == (8, 6) and t[(1,)][4] == "beta"
    p1, p2 = (_texto(f"jue-ab-arbol-b-paso-{k}") for k in gen.PASOS_ARBOL_B)
    assert ">β = 8<" in p1 and ">= 8<" in p1 and "max{8, 6}" in p1
    assert "[−∞, 8]" in p2 and ">9 ≥ 8<" in p2 and ">≥ 9<" in p2 and ">= 8<" in p2
    assert "corte beta" in p2 and "6 de 7 nodos" in p2


def test_la_ventana_marca_los_dos_cortes():
    svg = _texto("jue-ab-ventana")
    for rotulo in ("v ≤ α:", "v ≥ β:", "corte alfa", "corte beta", "aquí el valor",
                   "2 ≤ 3: corte alfa", "9 ≥ 8: corte beta", "α = 3", "β = 8"):
        assert rotulo in svg, rotulo


def test_las_partes_del_orden_fijo_dibujan_su_traza():
    visitas, cortes = gen.traza_n1(False)
    assert cortes == {(3, 6): "alfa"}
    p1, p2 = _texto("jue-ab-fijo-parte-1"), _texto("jue-ab-fijo-parte-2")
    assert ">α = +1<" in p1 and ">por mirar<" in p1 and "corte" not in p1
    _, _, a3, b3, v3 = visitas[3]
    assert (a3, b3, v3) == (1, float("inf"), 1) and gen.valores_n1()[3] == -1
    assert "[+1, +∞]" in p2
    assert ">v = +1 ≤ +1<" in p2 and ">≤ +1 (cota)<" in p2
    assert "corte alfa" in p2 and p2.count(">?<") == 2 and "5 de 13" in p2


def test_las_partes_del_orden_invertido_dibujan_su_traza():
    visitas, cortes = gen.traza_n1(True)
    assert cortes == {(6, 11): "beta"}
    p1, p2, p3 = (_texto(f"jue-ab-invertido-parte-{k}") for k in (1, 2, 3))
    # n13 vale −1, y es lo primero que ve n3: β = −1.
    assert visitas[13][4] == -1 and visitas[6][3] == -1
    assert ">β = −1<" in p1 and ">U = −1<" in p1 and "corte" not in p1
    assert "[−∞, −1]" in p2 and ">+1 ≥ −1<" in p2 and ">≥ +1 (cota)<" in p2
    assert "corte beta" in p2 and p2.count(">?<") == 2
    assert visitas[3][4] == -1 and visitas[2][2:4] == (-1, float("inf"))
    assert ">α = −1<" in p3 and "[−1, +∞]" in p3 and "pero no ahorra" in p3
    assert ">= +1<" in p3 and "8 de 13" in p3


def test_a_media_ejecucion_es_la_pila_del_corte_en_n3():
    svg = _texto("jue-ab-a-media-ejecucion")
    assert ">v = +1 ≤ α<" in svg and ">→ corta<" in svg and ">α = +1<" in svg
    assert svg.count("y se olvidó") == 2 and svg.count(">?<") == 2
    assert svg.count(">[+1, +∞]<") == 2 and ">[−∞, +∞]<" in svg


def test_el_arbol_c_es_el_del_ejercicio():
    svg = _texto("jue-ab-arbol-c")
    hojas = re.findall(r'font-size="26" font-weight="700" text-anchor="middle">(\d)</text>', svg)
    assert hojas == ["3", "5", "6", "9", "2", "4", "7", "1"]
    assert svg.count(">MAX<") == 5 and svg.count(">MIN<") == 2
    assert j.contar_nodos(j.ARBOL_C) == 15
    # Sin marcas: es el enunciado.
    assert "corte" not in svg and "α" not in svg and "β" not in svg


# ------------------------------------------------------------- clase 3 ---

def test_las_figuras_de_corte_dibujan_las_evaluaciones_calculadas():
    p1 = _texto("jue-c3-corte-prof-1")
    for nombre, t, p in gen.hijos4(gen.POSICION_C3, "B"):
        assert f"EVAL = {gen.fmt(gen.ev(t))}" in p1
    assert "con corte: +13" in p1
    p2 = _texto("jue-c3-corte-prof-2")
    minimos = [min(gen.ev(t2) for _, t2, _ in gen.hijos4(t, p))
               for _, t, p in gen.hijos4(gen.POSICION_C3, "B")]
    assert minimos == [-10, 1, 0]
    for v in minimos:
        assert f"mínimo: {gen.fmt(v)}" in p2
    assert "con corte: +1" in p2


def test_el_horizonte_esconde_la_recaptura():
    svg = _texto("jue-c3-horizonte")
    assert "tras d2xc3" in svg and "tras b4xc3" in svg
    assert "EVAL = +13" in svg and "EVAL = 0" in svg


def test_la_profundizacion_dibuja_lo_que_cada_busqueda_deja_listo():
    svg = _texto("jue-c3-profundizacion")
    assert [gen.jugada_lista(d)[0] for d in gen.PROFUNDIDADES_RELOJ] == ["d2xc3", "d2-d3", "d2-d3"]
    assert gen.jugada_lista(3)[1] == 100
    for d, c in zip(gen.PROFUNDIDADES_RELOJ, (4, 12, 33)):
        assert f"d = {d} · {c} nodos" in svg
    assert "entrega d2xc3" in svg and "entrega d2-d3" in svg


def test_mcts_tiene_sus_cuatro_pasos():
    svg = _texto("jue-c3-mcts-pasos")
    for paso in ("Selección", "Expansión", "Simulación", "Retropropagación"):
        assert paso in svg
    assert "5/11" in svg and "U = +1" in svg
