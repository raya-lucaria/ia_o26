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
from fractions import Fraction as F
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
    assert ">v ≤ α: poda<" in p2 and ">v = +1 (cota)<" in p2 and ">v = +1<" in p2
    assert "corte alfa" in p2 and p2.count(">?<") == 2 and "5 de 13" in p2


def test_las_partes_del_orden_invertido_dibujan_su_traza():
    visitas, cortes = gen.traza_n1(True)
    assert cortes == {(6, 11): "beta"}
    p1, p2, p3 = (_texto(f"jue-ab-invertido-parte-{k}") for k in (1, 2, 3))
    # n13 vale −1, y es lo primero que ve n3: β pasa de +∞ a −1.
    assert visitas[13][4] == -1 and visitas[6][3] == -1
    assert ">β: +∞ → −1<" in p1 and ">U = −1<" in p1 and "corte" not in p1
    assert "(−∞, −1)" in p2 and ">v ≥ β: poda<" in p2 and ">v = +1 (cota)<" in p2
    assert "corte beta" in p2 and p2.count(">?<") == 2
    assert visitas[3][4] == -1 and visitas[2][2:4] == (-1, float("inf"))
    # La raiz ya no mete «α = −1» y un «= +1» suelto en la misma caja.
    assert "(−1, +∞)" in p3 and "pero no ahorra" in p3 and ">v = +1<" in p3
    assert ">= +1<" not in p3 and "8 de 13" in p3


# ------------------------------------------------------------ el arbol T ---

def _aria_de(svg):
    return re.match(r"<svg\b[^>]*>", svg).group()


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
                "v ≥ β: poda", "devolvió 3", "devolvió 5", "se perdió al regresar"):
        assert rot in svg, rot
    assert svg.count(">?<") == 1


def test_azar_corte_e_iterativa_en_t():
    azar = _texto("jue-t-azar")
    for rot in ("v = 9/2", "v = 13/2", "v = 7", "mejor_jugada = der"):
        assert rot in azar, rot
    # El corte y la iterativa, sobre el árbol de resultados (destinos §E.3):
    # finales en 100·U y EVAL de EVAL_TPM; cifras de juegos.corte_tpm.
    d1, d2 = _texto("jue-t-corte-d1"), _texto("jue-t-corte-d2")
    total = j.contar_nodos(j.ARBOL_TPM)
    for d, svg in ((1, d1), (2, d2)):
        jugada, valor, ws, gen_ = j.corte_tpm(d)
        assert f">mejor_jugada = {jugada}<" in svg and f">mejor_valor = {gen._fmt_t(valor)}<" in svg
        assert f"{gen_} de {total} nodos" in svg
        for a, w in ws.items():
            assert f"{j.JUGADA_A_NOMBRE[a]} vale {gen._fmt_t(w)}" in _aria_de(svg), (d, a)
    for n in ("I", "C", "D"):
        assert f">EVAL = {j.EVAL_TPM[n]}<" in d1
    for n in ("C1", "C2"):
        assert f">EVAL = {j.EVAL_TPM[n]}<" in d2
    assert (j.corte_tpm(1)[:2], j.corte_tpm(2)[:2]) == (("izq", 60), ("centro", 10))
    assert "4 de 15 nodos" in d1 and "11 de 15 nodos" in d2
    assert "izq parece valer 60" in d1 and "su valor real es −100: la captura" in d1
    assert ">−100<" in d2 and "-100" not in d2          # signo menos tipografico
    it = _texto("jue-t-iterativa")
    filas, total_it = j.iterativa_tpm()
    for d, orden, jugada, _, n in filas:
        assert f"orden: {', '.join(orden)} · {n} nodos" in it, d
        assert f"d = {d} · lista: {jugada}" in it, d
    assert total_it == 25 and f"En total, {total_it} nodos" in it
    assert "izq con d = 1," in it and "centro desde d = 2" in it
    for svg in (d1, d2, it):
        assert "Finales en la escala 100·U." in svg and "árbol de resultados" in svg


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
    """Rehecha (destinos §E.1 #9): N y V̂ en cada nodo, sin G/N; raíz N 4,
    V̂ 0 → N 5, V̂ +0.2. Cifras de juegos.mcts_vuelta y mcts_nv."""
    svg = _texto("jue-c3-mcts-pasos")
    for paso in ("1 · Selección", "2 · Expansión", "3 · Simulación", "4 · Retropropagación"):
        assert f">{paso}<" in svg
    vuelta = j.mcts_vuelta(j.MCTS_ARBOL, c=1, u=1)
    antes, despues = j.mcts_nv(vuelta["antes"]), j.mcts_nv(vuelta["despues"])
    renglones = re.findall(r">([^<>]+)</text>", svg)
    # Antes de la vuelta (tres paneles) y despues (uno), cada nodo con N y V̂.
    for n, (k, v) in antes.items():
        assert renglones.count(f"N {k}") >= 3 and f"V̂ {gen._dec_txt(v)}" in renglones, n
    for n in vuelta["camino"] + ["nuevo"]:
        k, v = despues[n]
        assert f"N {k}" in renglones and f"V̂ {gen._dec_txt(v)}" in renglones, n
    assert "N 0" in renglones and "V̂ ?" in renglones and "U = +1:" in renglones
    assert (antes["r"], despues["r"]) == ((4, 0), (5, F(1, 5)))
    titulo = re.search(r"<title>([^<]*)</title>", svg).group(1)
    assert "la raíz pasa de N 4, V̂ 0 a N 5, V̂ +0.2" in titulo
    assert f"{vuelta['puntajes']['r']['a']:.2f}" in renglones
    # MAX y MIN marcados por nivel, con su color
    assert re.search(rf'fill="{gen.COLOR_MAX}"[^>]*>MAX<', svg)
    assert re.search(rf'fill="{gen.COLOR_MIN}"[^>]*>MIN<', svg)
    assert "G/N" not in svg and not re.search(r">\d+/\d+<", svg)
    # nodos rotulados (lo pide la prosa de 3.4): R, a, b, a1, a2 y «nuevo»
    for nombre in ("R", "a", "b", "a1", "a2", "nuevo"):
        assert renglones.count(nombre) >= 3, nombre
    assert (antes["a"], antes["b"], antes["a1"], antes["a2"]) == (
        (3, F(1, 3)), (1, -1), (1, 1), (1, -1))
    assert (despues["a2"], despues["nuevo"]) == ((2, 0), (1, 1))

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
    traza = j.traza_decidir(j.ARBOL_TPM_100, profundidad=2, evaluar=j.EVAL_TPM)
    k = gen._fila_tramo_1(traza)
    assert traza["filas"][k - 1]["generados"] == 7 and traza["generados"] == 11
    assert "7 de 15 nodos hasta aquí" in t1 and "11 de 15 nodos" in fin
    assert ">mejor_jugada = centro<" in t1 and ">mejor_valor = 10<" in t1
    assert "Corte con d = 2, tramo 1 · centro sube a 10" in t1
    # el tramo se corta donde cambia la jugada: de izq a centro
    assert traza["filas"][k - 2]["mejor_jugada"] == "izq"
    assert "Corte con d = 2, tramo 2 · D devuelve −100: sigue centro" in fin
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
    corridas = j.profundizacion_iterativa_t(j.ARBOL_TPM_100, (1, 2, 3), j.EVAL_TPM)
    cotas = [sorted(n for n, e in t["filas"][-1]["estado"].items() if e.get("cota"))
             for _, _, t in corridas]
    assert cotas == [[], ["D"], ["C2", "D"]]
    assert _texto("jue-t-iterativa").count(">· cota<") == sum(map(len, cotas))


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

UCB = ["jue-c3-hoeffding", "jue-c3-bono"]


@pytest.mark.parametrize("nombre", UCB)
def test_las_graficas_de_la_p6_nombran_sus_ejes_y_su_escala(nombre):
    """Ejes con nombre, marcas de escala de 14 px o mas, y el eje log dicho
    en el nombre del eje que lo es."""
    svg = _texto(nombre)
    renglones = re.findall(r">([^<>]+)</text>", svg)
    # Los nombres largos van partidos en renglones: las figuras miden 300 px
    # (ver ANCHO_UCB_MAX abajo).
    ejes = {"jue-c3-hoeffding": ("ε: el margen pedido", "cota de la probabilidad de",
                                 "que Q̂ quede ε o más abajo", "N: muestras de la jugada",
                                 "ε: el margen que falla", "con prob. ≤ δ"),
            "jue-c3-bono": ("N(s,a): visitas de la jugada", "bono, en la escala de U",
                            "(de −1 a +1)")}[nombre]
    for e in ejes:
        assert escape(e) in renglones, e
    marcas = {"jue-c3-hoeffding": ["0", "0.1", "0.2", "0.4", "0.5", "1", "50", "200", "1.2"],
              "jue-c3-bono": ["0", "1", "2", "3", "4", "50", "200"]}[nombre]
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


def test_hoeffding_dibuja_la_cota_contra_eps_y_el_margen_contra_n():
    """Rehecha (destinos §E.1 #8): (A) la cota e^(−N·ε²/2) contra ε con
    N = 100, sus tres puntos 60.65 / 13.53 / 0.0335 %; (B) el margen
    contra N para dos δ. Cifras de juegos."""
    svg = _texto("jue-c3-hoeffding")
    renglones = re.findall(r">([^<>]+)</text>", svg)
    tabla = j.tabla_hoeffding_epsilon()
    assert [gen._pct_h(p) for _, p in tabla] == ["60.65 %", "13.53 %", "0.0335 %"]
    for _, p in tabla:
        assert gen._pct_h(p) in renglones
    assert ">A · La cota contra ε<" in svg and ">B · El margen contra N<" in svg
    assert f"con N = {j.N_HOEFFDING_HOMOLOGACION} muestras" in renglones
    # cada punto de A, sobre la curva, en (ε, cota)
    y_a = float(re.search(r'<text x="12" y="([\d.]+)"[^>]*>A · La cota', svg).group(1))
    pl = gen.plano_hoeffding_a(y_a - 40 + 128)
    for e, p in tabla:
        assert f'<circle cx="{pl.x(e)}" cy="{pl.y(p / 100)}" r="5"' in svg, e
    # B: una curva por δ, con su valor en N = 100
    d1, d2 = j.DELTAS_HOEFFDING_HOMOLOGACION
    for d in (d1, d2):
        assert f"δ = {d:g}" in renglones
        assert gen._dos(j.margen_hoeffding(d, 100)) in renglones
    assert "0.24" in renglones and "0.33" in renglones
    assert svg.count("<polyline") == 3
    aria = _aria_de(svg)
    assert "con ε = 0.1, 60.65 %, con ε = 0.2, 13.53 %, con ε = 0.4, 0.0335 %" in aria
    assert "regla de continuación fija" in aria and "1.33 veces" in aria
    assert "Es una cota, no una tasa." in aria

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
    # «árbol base» es el de la 7.2, no este: el subtitulo no lo nombra
    assert "árbol base" not in "".join(_renglones("jue-t-pm-arbol"))
    assert "finales en U" in _renglones("jue-t-pm-arbol")
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
       "jue-c3-mcg-uct-crece", "jue-c3-mcg-mezcla"]
# Figuras simbolicas sueltas de la radiografia: sin arbol T± ni jugada que marcar.
RX_SIMBOLICAS = ["jue-c3-rx-estado-y-jugada"]


def _aria(nombre):
    return re.search(r'aria-label="([^"]*)"', _texto(nombre)).group(1)


def _renglones(nombre):
    import html
    return [html.unescape(r) for r in re.findall(r">([^<>]+)</text>", _texto(nombre))]


def test_estan_las_figuras_de_la_radiografia():
    for nombre in RX_ARBOLES + RX_FLUJOS + MCG + RX_SIMBOLICAS:
        assert nombre in gen.DIAGRAMAS, nombre
        assert (gen.ASSETS / f"{nombre}.svg").exists(), nombre


@pytest.mark.parametrize("nombre", RX_ARBOLES + RX_FLUJOS + MCG + RX_SIMBOLICAS)
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
    assert r.count("N 5") == 3 and {"Q̂ −0.6", "Q̂ −0.4", "Q̂ +0.6"} <= set(r)
    assert not [x for x in r if "ū" in x or "T±" in x]
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
    """§7.2 pide 3 a 6 cajas «y, si hace falta, un rombo». Los tres de la
    familia minimax son recursivos y necesitan mas de un rombo (¿final?,
    ¿quedan hijos?, y ¿d = 0? o ¿v ≥ β?) para que siguiendo las flechas se
    vea el descenso y el regreso al padre; por eso el tope es de pasos de la
    columna, cajas + rombos ≤ 8 (las cajas del lado de un rombo no cuentan:
    son su salida «sí»)."""
    f = gen.FLUJOS[nombre.removeprefix("jue-c3-rx-flujo-")]
    cajas = [p for p in f["pasos"] if "caja" in p]
    assert 3 <= len(cajas) <= 6 and len(f["pasos"]) <= 8
    assert f["pasos"][-1].get("fin") and f["pasos"][-1]["caja"][0].startswith("Juega")
    r = _renglones(nombre)
    for p in f["pasos"]:
        for x in p.get("caja", p.get("rombo")):
            assert x in r, x


@pytest.mark.parametrize("nombre", ["minimax", "alfa-beta", "corte"])
def test_en_los_flujos_recursivos_todo_valor_vuelve_al_padre(nombre):
    """Antes «vale U» quedaba sin salida y «¿Es un final? —no→ Sube su
    valor» se saltaba el descenso. Toda caja de valor (las del lado de un
    rombo y «Vuelve al padre») regresa a la unica caja «Al volver…», y hay
    una vuelta de «Baja al siguiente hijo» al primer rombo."""
    f = gen.FLUJOS[nombre]
    pasos = f["pasos"]
    assert [p.get("destino", False) for p in pasos].count(True) == 1
    for p in pasos:
        if "lado" in p and p["lado"][1][0] in ("vale", "poda:"):
            assert p.get("regresa"), p
    # «Vuelve al padre» lleva su condición: la raíz no tiene padre, y ahí se juega.
    assert any(p.get("regresa") and p.get("caja", [""])[:2] == ["Si no es la raíz:", "vuelve al padre"]
               for p in pasos)
    assert any(p.get("fin") and p.get("tenue") == "si es la raíz" for p in pasos)
    baja = next(k for k, p in enumerate(pasos) if p.get("caja", [""])[0].startswith("Baja"))
    assert (baja, 0) in [(d, h) for d, h, _ in f["vueltas"]]
    r = _renglones(f"jue-c3-rx-flujo-{nombre}")
    assert "vuelve al padre" in r and "Empieza en la raíz" in r


def test_el_flujo_de_uct_es_un_ciclo_de_cuatro_fases():
    r = _renglones("jue-c3-rx-flujo-uct")
    for fase in ("1 · Selección", "2 · Expansión", "3 · Simulación", "4 · Retropropagación"):
        assert fase in r
    assert "el tiempo?" in r and "no: otra vuelta" in r and "de la raíz más visitada" in r
    # Q̂ es un promedio: no se le «suma» U
    assert "actualiza su promedio" in r and "Q̂ con la U" in r
    assert not [x for x in r if "U a Q̂" in x or "ū" in x]


def test_las_figuras_del_arbol_grande_no_llevan_cifras():
    """§9.5: simbolicas. Ningun digito en lo que se ve, salvo los de los
    numeros de fase («1 · Selección»). La mezcla es la excepcion acotada:
    dibuja dos finales y el promedio de sus U, y +1, −1 y 0 son la escala de
    utilidades, no datos de una corrida; ahi se borran solo esas tres
    (como numeros sueltos) antes de buscar digitos, asi que cualquier otra
    cifra (un conteo, un 0.6) sigue fallando. La figura de estado y jugada
    va sin ninguna."""
    for nombre in MCG + RX_SIMBOLICAS:
        r = [x for x in _renglones(nombre) if not re.match(r"\d · ", x)]
        if nombre == "jue-c3-mcg-mezcla":
            r = [re.sub(r"(?<![\d.,])(?:[+−]1|0)(?![\d.,])", "", x) for x in r]
        assert not [x for x in r if re.search(r"\d", x)], nombre


def test_el_valor_de_una_jugada_vive_en_el_hijo():
    r = _renglones("jue-c3-rx-estado-y-jugada")
    for clave in ("jugada A", "jugada B", "T(s, A)", "T(s, B)", "número de A", "número de B",
                  "valor de la jugada = valor del hijo:", "Q(s,a) = V(T(s,a))", "s", "MAX"):
        assert clave in r, clave
    # La leyenda: que numero guarda cada algoritmo (los siete), en el orden de la pagina.
    for alg, sigue in [("minimax", ["V"]), ("alfa-beta", ["V o cota"]),
                       ("expectiminimax", ["E[·]", "V del juego con azar"]),
                       ("corte", ["valor con corte", "o cota"]),
                       ("actualización minimax", ["Q̂ → Q, bajo su contrato"]),
                       ("UCT", ["Q̂ → Q"])]:
        i = r.index(alg)
        assert r[i + 1:i + 1 + len(sigue)] == sigue, alg
    assert "Q̂ estima V" not in r
    assert [a for a, *_ in gen.NUMERO_EN_EL_HIJO] == [
        "minimax", "alfa-beta", "expectiminimax", "corte", "Monte Carlo plano",
        "actualización minimax", "UCT"]
    # el de Monte Carlo plano lleva Q_azar con subindice (notacion §5.1, sin ū ni μ)
    assert ("<tspan>Q̂ estima </tspan><tspan>Q</tspan><tspan dy=\"4.5\" font-size=\"10.8\">"
            "azar</tspan>") in _texto("jue-c3-rx-estado-y-jugada")
    assert r.index("Monte Carlo plano") < r.index("UCT")
    assert "ū" not in _texto("jue-c3-rx-estado-y-jugada") and "μ" not in _texto(
        "jue-c3-rx-estado-y-jugada")
    assert "EVAL" not in _texto("jue-c3-rx-estado-y-jugada")
    assert "Q(s, a) = V(T(s, a))" in _aria("jue-c3-rx-estado-y-jugada")


def test_la_mezcla_pasa_de_mitad_y_mitad_a_casi_todas_a_menos_uno():
    r = _renglones("jue-c3-mcg-mezcla")
    for clave in ("Pocas vueltas", "Muchas vueltas", "Q̂(A) ≈ 0", "Q̂(A) → −1", "+1", "−1",
                  "jugada A", "MIN", "Proporciones ilustrativas:"):
        assert clave in r, clave
    assert "≈ mitad" in r and "casi todas" in r and "a −1" in r
    assert r.index("Pocas vueltas") < r.index("Q̂(A) ≈ 0") < r.index("Muchas vueltas") \
        < r.index("Q̂(A) → −1")
    # El grosor dice las visitas: parejo con pocas vueltas, la rama a −1
    # mucho mas gruesa con muchas.
    grosores = [float(g) for g in re.findall(r'stroke-width="([\d.]+)" stroke-linecap="round"',
                                             _texto("jue-c3-mcg-mezcla"))]
    assert len(grosores) == 4
    pocas_mas, pocas_menos, muchas_mas, muchas_menos = grosores
    assert abs(pocas_mas - pocas_menos) <= 1
    assert muchas_menos >= 4 * muchas_mas


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


# ------------------ 7.3.6: la animacion de las radiografias (spec §7.3) ---

RX_ANIMADAS = sorted(gen.ORDEN_ANIMA_RX)
_CAPA_RX = re.compile(r'<g class="rx-anima".*?</g></g>', re.S)


def _pasos_animados(nombre):
    """[(inicio en fraccion del ciclo, tipo, nodo)] de la capa, por inicio."""
    raiz = ET.fromstring(_texto(nombre))
    ns = "{http://www.w3.org/2000/svg}"
    (capa,) = [g for g in raiz.iter(f"{ns}g") if g.get("class") == gen.CLASE_ANIMA_RX]
    pasos, durs, begins = [], set(), set()
    for k, g in enumerate(capa.findall(f"{ns}g")):
        assert g.get("opacity") == "0" and g.get("data-paso") == str(k)
        (a,) = g.findall(f"{ns}animate")
        valores = a.get("values").split(";")
        tiempos = [float(x) for x in a.get("keyTimes").split(";")]
        assert a.get("calcMode") == "discrete" and a.get("repeatCount") == "indefinite"
        # un solo reloj: misma duración y mismo arranque en todos los pasos, para
        # que comparar keyTimes sea comparar tiempos reales
        durs.add(a.get("dur")); begins.add(a.get("begin", "0s"))
        assert a.get("attributeName") == "opacity"
        assert len(valores) == len(tiempos) and tiempos == sorted(tiempos)
        # opacidad 0 al empezar y al acabar el ciclo: en t = 0 se ve la estatica
        assert tiempos[0] == 0 and valores[0] == valores[-1] == "0" and tiempos[1] > 0
        assert tiempos[-1] < 1 and valores[1] == "1"
        pasos.append((tiempos[1], g.get("data-tipo"), g.get("data-nodo")))
    assert [p[0] for p in pasos] == sorted(p[0] for p in pasos)
    assert len(durs) == 1 and len(begins) == 1, (nombre, durs, begins)
    return pasos


def test_las_radiografias_animadas_son_las_de_orden_determinista():
    assert RX_ANIMADAS == sorted(["jue-c3-rx-minimax", "jue-c3-rx-alfa-beta",
                                  "jue-c3-rx-corte", "jue-c3-rx-quietud",
                                  "jue-c3-rx-iterativa"])
    for nombre in RX_ARBOLES + RX_FLUJOS + MCG + RX_SIMBOLICAS:
        if nombre not in RX_ANIMADAS:
            assert "<animate" not in _texto(nombre) and "rx-anima" not in _texto(nombre)


@pytest.mark.parametrize("nombre", RX_ANIMADAS)
def test_la_animacion_recorre_el_orden_de_juegos_y_acaba_en_la_jugada(nombre):
    ids = j.ids_tpm()
    algoritmo = gen.ORDEN_ANIMA_RX[nombre]
    if algoritmo == "iterativa":
        tramos = [(f"d={d}:", o, f[2]) for d, o, f in
                  zip((1, 2, 3), j.orden_generados_tpm("iterativa"), j.iterativa_tpm()[0])]
    else:
        jugada = {"minimax": j.minimax_tpm()[0], "alfa-beta": j.alfa_beta_tpm("dado")[0],
                  "corte": j.corte_tpm(1)[0], "quietud": j.quietud_tpm(1)[0]}[algoritmo]
        tramos = [("", j.orden_generados_tpm(algoritmo), jugada)]
    esperado = []
    for prefijo, orden, jugada in tramos:
        esperado += [("nodo", prefijo + ids[c]) for c in orden]
        esperado.append(("jugada", prefijo + ids[(j.JUGADAS_RAIZ.index(jugada),)]))
    pasos = _pasos_animados(nombre)
    assert [(t, n) for _, t, n in pasos] == esperado
    # el ultimo paso marca la jugada que juega la figura (la de su pastilla)
    _, tipo, nodo = pasos[-1]
    jugada = tramos[-1][2]
    assert tipo == "jugada" and nodo.split(":")[-1] == "ICD"[j.JUGADAS_RAIZ.index(jugada)]
    assert f"juega {jugada}" in _renglones(nombre)


@pytest.mark.parametrize("nombre", RX_ANIMADAS)
def test_sin_la_capa_animada_la_figura_es_la_estatica(nombre):
    """La animacion es una capa aislada: quitarla deja byte a byte lo que
    dibuja la funcion con animar=False, y la capa no trae texto (no tapa
    ni agrega nada que se lea) y respeta prefers-reduced-motion."""
    svg = _texto(nombre)
    capas = _CAPA_RX.findall(svg)
    assert len(capas) == 1
    estatica = {"jue-c3-rx-minimax": gen.jue_c3_rx_minimax,
                "jue-c3-rx-alfa-beta": gen.jue_c3_rx_alfa_beta,
                "jue-c3-rx-corte": gen.jue_c3_rx_corte,
                "jue-c3-rx-quietud": gen.jue_c3_rx_quietud,
                "jue-c3-rx-iterativa": gen.jue_c3_rx_iterativa}[nombre](animar=False)
    assert _CAPA_RX.sub("", svg) == estatica
    assert "<animate" not in estatica and "<text" not in capas[0]
    assert "prefers-reduced-motion: reduce" in capas[0] and 'aria-hidden="true"' in capas[0]
    # la capa va detras del arbol: antes del primer nodo dibujado
    assert svg.index(capas[0]) < svg.index("R · MAX")


# ------------------------------ homologacion (Ola 1): figuras nuevas ---

HOMOLOGACION_300 = ["jue-rx-expectiminimax", "jue-rx-flujo-expectiminimax", "jue-rx-mmmc",
                    "jue-rx-flujo-mmmc", "jue-c3-refutacion-tres", "jue-c3-tres-mc",
                    "jue-c3-min-volteado", "jue-c3-hoeffding", "jue-c3-mcts-pasos"]


def test_la_lista_cerrada_de_300_es_la_del_generador():
    assert list(gen.HOMOLOGACION_300) == HOMOLOGACION_300
    assert gen.ANCHO == 600 and gen.ANCHO_HOMOLOGACION == 300


@pytest.mark.parametrize("nombre", HOMOLOGACION_300)
def test_las_figuras_nuevas_miden_300_y_hablan_espanol(nombre):
    """destinos §E.1: las nuevas a 300 px exactos (ANCHO = 600 no se toca),
    aria-label en español y notación §5.1: nada de ū, μ, G/N ni T±."""
    assert nombre in gen.DIAGRAMAS and (gen.ASSETS / f"{nombre}.svg").exists()
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert re.search(r'\bwidth="300"', etiqueta) and 'viewBox="0 0 300 ' in etiqueta
    aria = _aria(nombre)
    assert len(aria) > 150 and re.search(r"\b(el|la|de|en|y)\b", aria)
    for viejo in ("ū", "μ", "G/N", "T±", "N(s′)"):
        assert viejo not in svg, (nombre, viejo)
    tams = [float(t) for t in re.findall(r'<text [^>]*font-size="([\d.]+)"', svg)]
    assert min(tams) >= 13


def test_expectiminimax_dibuja_el_dado_en_d():
    jugada, valores = j.expectiminimax_tpm()
    assert jugada == "der" and valores["D"] == F(1, 3) == valores["R"]
    r = _renglones("jue-rx-expectiminimax")
    assert "otro juego: dado en D" in r and "AZAR" in r and r.count("⅓") == 3
    assert "juega der" in r and "+1/3" in r and "Q en la raíz: izq −1," in r
    assert f"jugaría {j.minimax_tpm()[0]}." in r
    for n in ("I", "C", "C1", "C2"):
        assert gen._u_txt(valores[n]) in r
    # el nodo de AZAR: esquinas redondas (rx 22) con el color del azar
    assert re.search(rf'rx="22" fill="[^"]+" stroke="{gen.COLOR_AZAR}"', _texto("jue-rx-expectiminimax"))
    assert "juega der" in _aria("jue-rx-expectiminimax")


def test_el_flujo_de_expectiminimax_es_el_de_minimax_con_la_rama_de_azar():
    f = gen.FLUJO_EXPECTIMINIMAX
    r = _renglones("jue-rx-flujo-expectiminimax")
    for p in f["pasos"]:
        for x in p.get("caja", p.get("rombo")):
            assert x in r, x
    assert "¿AZAR?" in r and "Pr(a|s)·w" in r and "vuelve al padre" in r
    assert f["pasos"][-1].get("fin") and [p.get("destino") for p in f["pasos"]].count(True) == 1
    # la rama de azar entra en «¿Quedan hijos?»
    azar = next(p for p in f["pasos"] if p.get("rombo") == ["¿AZAR?"])
    assert f["pasos"][azar["une"]]["rombo"] == ["¿Quedan", "hijos?"]


def test_la_actualizacion_minimax_dibuja_su_corrida():
    m = j.mc_minimax(j.ARBOL_TPM, j.ITERACIONES_MMMC_TPM, j.SEMILLA_TPM)
    r = _renglones("jue-rx-mmmc")
    ids = j.ids_tpm()
    assert f"{j.ITERACIONES_MMMC_TPM} partidas, semilla {j.SEMILLA_TPM}" in r
    jugada = j.JUGADAS_RAIZ[m["jugada"]]
    assert f"juega {jugada}" in r and jugada == "centro"
    qs = ", ".join(f"{a} {'?' if q is None else gen._u_txt(q)}"
                   for a, q in zip(j.JUGADAS_RAIZ, m["Q"]))
    assert qs + "." in r and "izq ?" in qs
    exactos = [c for c in m["V"] if c and m["exacto"][c] and isinstance(j.nodo_en(j.ARBOL_TPM, c), tuple)]
    assert r.count("exacto") == len(exactos) + (1 if m["exacto"][()] else 0) >= 2
    for c in m["V"]:
        if c and isinstance(j.nodo_en(j.ARBOL_TPM, c), tuple):
            assert f"V̂ {gen._u_txt(m['V'][c])}" in r, ids[c]
    # una «?» por jugada sin visitar cuyo padre ya esta guardado
    frontera = [c for c in ids if c and c not in m["V"] and c[:-1] in m["V"]]
    assert r.count("?") == len(frontera) and len(frontera) == 2
    assert "desconocida" in _aria("jue-rx-mmmc")


def test_el_flujo_de_la_actualizacion_minimax_sube_max_y_min():
    r = _renglones("jue-rx-flujo-mmmc")
    for x in ("V̂(z) = U(z), exacto", "Q̂(s,a) = V̂(T(s,a));", "V̂(s): máximo en MAX,",
              "mínimo en MIN, solo", "no: otra partida", "de la raíz con mayor Q̂",
              "desconocida, nunca cero."):
        assert x in r, x
    assert not [x for x in r if "promedi" in x]


def test_la_refutacion_dibuja_los_tres_operadores():
    o = j.operadores_ante_la_refutacion()
    u = j.uct_refutacion()
    s = gen.series_refutacion()
    assert (s["promedio"]["A"][-2], s["promedio"]["A"][-1]) == (o["promedio_antes"],
                                                                o["promedio_despues"])
    assert (s["minimax"]["A"][-2], s["minimax"]["A"][-1]) == (o["minimax_antes"],
                                                              o["minimax_despues"])
    assert s["uct"]["descubre"] == u["descubre"] and s["uct"]["jugada"] == u["mas_visitada"][-1]
    assert all(x == s["uct"]["jugada"] for x in u["mas_visitada"][s["uct"]["desde"] - 1:])
    assert u["mas_visitada"][s["uct"]["desde"] - 2] != s["uct"]["jugada"]
    r = _renglones("jue-c3-refutacion-tres")
    assert "Q̂(A) baja de 10 a 8.67:" in r and "sigue en A. Entrega A." in r
    assert "Q̂(A) salta de 10 a −30:" in r and "cambia. Entrega B." in r
    assert f"Entrega {u['mas_visitada'][-1]}, la más visitada," in r
    assert f"c = {j.C_REFUTACION}, semilla {j.SEMILLA_REFUTACION}, {j.VUELTAS_REFUTACION} vueltas;" in r
    assert f"corre con los pagos ÷{j.ESCALA_REFUTACION}" in r
    assert (f"<tspan dy=\"-4.2\">(A) = {gen._u_txt(j.q_azar_arbol(j.ARBOL_REFUTACION)[0])}"
            "</tspan>") in _texto("jue-c3-refutacion-tres")
    assert "−10/3" in _aria("jue-c3-refutacion-tres")
    # tres paneles, cada uno con Q̂(A) y Q̂(B)
    assert _texto("jue-c3-refutacion-tres").count("<polyline") == 6


def test_los_tres_monte_carlo_dibujan_sus_limites():
    filas = gen.filas_tres_mc()
    assert [f[0] for f in filas] == ["V", "Q_azar", "plano", "minimax", "uct"]
    assert filas[0][1] == j.q_minimax_arbol(j.ARBOL_TPM) == [-1, 0, -1]
    assert filas[1][1] == j.q_azar_arbol(j.ARBOL_TPM) == [0, F(-1, 4), F(1, 3)]
    u = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)
    assert filas[4][2] == [u["N"][(a,)] for a in range(3)] == [5, 26, 9]
    assert filas[3][1] == [-1, 0, -1]          # la actualizacion minimax ya llego a V
    r = _renglones("jue-c3-tres-mc")
    for clave, vals, ns, i in filas:
        fmt = gen._u_txt if clave in ("V", "Q_azar") else gen._dec_txt
        for q in vals:
            assert fmt(q) in r, (clave, q)
        for n in ns or ():
            assert f"N {n}" in r
    assert "tiende a Q" in r and "juego óptimo" in r and "los dos al azar" in r
    # la fila exacta es Q(s_raiz, a), no V
    assert "Q" in r and "V" not in r and "tiende a V" not in r
    assert f"{j.VUELTAS_PAGINA_TPM} partidas; la raíz también al azar" in r
    aria = _aria("jue-c3-tres-mc")
    assert "entrega izq" in aria and "entrega centro" in aria


# ------------------------------ homologacion (Ola 2): figuras nuevas ---

def test_min_volteado_dibuja_el_bono_a_los_dos_lados():
    """destinos §E.1 #7: p, q, r con Q̂ −0.2, 0.25, 0.5; N(s,a) 30, 16, 4;
    N(s) = 50; c = 2√2; bonos 1.02, 1.40, 2.80. MAX miraría Q̂ + bono; MIN
    mira Q̂ − bono. Cifras de juegos.min_volteado."""
    m = j.min_volteado()
    f = m["filas"]
    svg = _texto("jue-c3-min-volteado")
    r = _renglones("jue-c3-min-volteado")
    assert f"N(s) = {m['N_padre']}, c = 2√2. Bajo s mueve MIN." in r
    for k, d in f.items():
        assert (f"{k}: Q̂ {gen._dec_txt(d['Q'])} · N(s,a) {d['N']} · bono "
                f"{gen._dos_s(d['bono'])}") in r
        for lado in ("arriba", "abajo"):
            assert gen._dos_s(d[lado]) in r, (k, lado)
            # el bigote acaba en Q̂ ± bono
            assert f'x1="{gen._x_vol(d[lado])}"' in svg or f'x2="{gen._x_vol(d[lado])}"' in svg
    assert [gen._dos_s(f[k]["bono"]) for k in "pqr"] == ["1.02", "1.40", "2.80"]
    assert f"elige el mayor: {m['max']}, {gen._dos_s(f[m['max']]['arriba'])}" in r
    assert f"elige el menor: {m['min']}, {gen._dos_s(f[m['min']]['abajo'])}" in r
    assert "Si eligiera MAX: Q̂ + bono" in r and "Elige MIN: Q̂ − bono" in r
    assert "MIN no cambia el signo de c:" in r
    aria = _aria("jue-c3-min-volteado")
    assert "elige el menor, r" in aria and "elegiría el mayor, r" in aria
    assert "MIN no les cambia el signo" in aria


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ninguna_figura_usa_la_notacion_retirada(nombre):
    """plan §5.1 y destinos §E.4: ni ū, μ, G/N, N(s′) ni T± en ninguna figura;
    los árboles de juguete se nombran «árbol base», «árbol reducido» y
    «árbol de resultados» (la T queda solo para T(s, a))."""
    svg = _texto(nombre)
    for viejo in ("ū", "μ", "G/N", "T±", "N(s′)", "árbol T", "unidades de ū"):
        assert viejo not in svg, (nombre, viejo)
    visibles = " ".join(re.findall(r">([^<>]+)<", svg)) + " " + _aria(nombre)
    assert not re.findall(r"(?<![\w(])T1?(?![\w(])", visibles.replace("A y T sirven", "")), nombre


def test_las_figuras_quitadas_no_vuelven():
    """destinos §E.2: sus conclusiones quedan en juegos.py para las tablas."""
    for n in ("jue-c3-bandido-corridas", "jue-c3-pago", "jue-c3-eligiendo-x"):
        assert n not in gen.DIAGRAMAS and not (ASSETS_JUEGOS / f"{n}.svg").exists()
    reparto = j.reparto_bandido()
    sin_bono = reparto["mejor_promedio"]
    assert (sin_bono["n"] - sin_bono["atoradas"], sin_bono["en"]["y"], sin_bono["en"]["z"]) == (
        34, 5, 1)
    assert j.tabla_eligiendo_x()["mejor_promedio"][10000] == F(17, 20)


def test_las_figuras_del_arbol_base_y_del_reducido_se_nombran():
    for nombre in FIGURAS_T:
        aria = _aria(nombre)
        if nombre.startswith("jue-t1-"):
            assert "árbol reducido" in aria, nombre
        elif nombre.startswith(("jue-t-corte", "jue-t-iterativa")):
            assert "árbol de resultados" in aria, nombre
        else:
            assert "árbol base" in aria, nombre


@pytest.mark.parametrize("nombre", [n for n in sorted(gen.DIAGRAMAS)
                                    if n.startswith(("jue-ab-", "jue-alfa-beta-", "jue-t-ab",
                                                     "jue-t1-ab"))])
def test_en_alfa_beta_la_operacion_se_llama_poda(nombre):
    """plan §2.5 y §5.2: «poda» para la operación de alfa-beta; «corte alfa» y
    «corte beta» solo como nombres. Ningún «corta» en lo visible ni en el alt."""
    svg = _texto(nombre)
    visibles = " ".join(re.findall(r">([^<>]+)<", svg)) + " " + _aria(nombre)
    assert not re.search(r"\bcorta\b", visibles), nombre
    assert "árbol T" not in visibles
