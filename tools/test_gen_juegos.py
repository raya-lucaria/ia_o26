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
    assert svg.count("no se genera") == 13 - generados + 1  # mas la leyenda
    assert list(cortes.values()) == [corte] and f"corte {corte}" in svg
    for orden in range(1, generados + 1):
        assert f">{orden}º<" in svg
