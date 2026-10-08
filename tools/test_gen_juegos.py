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
    """Ancho de la columna y letra minima de 22: el sitio las escala a ~350 px.
    La ventana mide 640, como las figuras de T (ver mas abajo)."""
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    ancho = 640 if nombre == "jue-ab-ventana" else 700
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
             + ["jue-t-ab-pila", "jue-t-azar", "jue-t-corte-d1", "jue-t-corte-d2",
                "jue-t-iterativa"])


def test_estan_todas_las_figuras_del_arbol_t():
    assert len(FIGURAS_T) == 18 and set(FIGURAS_T) <= set(gen.DIAGRAMAS)


@pytest.mark.parametrize("nombre", FIGURAS_T)
def test_las_figuras_de_t_caben_y_cada_numero_lleva_su_letra(nombre):
    svg = _texto(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", svg).group()
    assert 'width="640"' in etiqueta and re.search(r'aria-label="[^"]{120,}"', etiqueta)
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


@pytest.mark.parametrize("nombre", FIGURAS_T + ["jue-ab-ventana"])
def test_nada_se_sale_y_el_titulo_y_el_pie_caben_en_un_telefono(nombre):
    """A 1280 px la columna mide ~640: nada sale del lienzo. A 390 px la
    figura se ve desde la izquierda: lo que va pegado al margen izquierdo
    (titulo, pie, leyenda) cabe en ~340 px. Mide con DejaVu, la letra con que
    el navegador de esta maquina resuelve system-ui; sin ella, se salta."""
    ImageFont = pytest.importorskip("PIL.ImageFont")
    import html
    import os
    if not os.path.isdir(_DEJAVU):
        pytest.skip("sin DejaVu")
    svg = _texto(nombre)
    ancho = float(re.search(r'width="([\d.]+)"', svg).group(1))
    assert ancho <= 640
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
