"""Guardas de los diagramas de la unidad de modelado y optimizacion.

Mismo juego que test_gen_complejidad.py, con dos anadidos propios de esta
unidad: <title> y <desc> internos, que ningun SVG del curso llevaba, y la
comprobacion de que los dos diagramas que CALCULAN siguen coincidiendo con la
aritmetica exacta del episodio.

Ojo con lo que estas pruebas NO hacen: el fixture regenera antes de leer, asi
que un SVG editado a mano se sobrescribe en silencio y la suite pasa. Lo que
ata el archivo comiteado a su generador es correr el generador y comprobar que
`git status` queda limpio.
"""
import re
import xml.etree.ElementTree as ET
from fractions import Fraction as F
from itertools import combinations

import pytest

import gen_optimizacion as gen
from unidades import ASSETS_OPTIMIZACION, filas_de_creditos

FONDO = "#211033"


@pytest.fixture(scope="module", autouse=True)
def _svgs_frescos():
    for nombre in gen.DIAGRAMAS:
        gen.escribir(nombre)


def _texto(nombre):
    return (ASSETS_OPTIMIZACION / f"{nombre}.svg").read_text(encoding="utf-8")


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_existe_y_lleva_el_prefijo(nombre):
    assert nombre.startswith("opt-"), (
        f"{nombre}: los ids de objeto numerado son unicos en TODO el curso, "
        "asi que esta unidad prefija con 'opt-'"
    )
    assert (ASSETS_OPTIMIZACION / f"{nombre}.svg").is_file()


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_la_raiz_svg_trae_las_cinco_convenciones(nombre):
    texto = _texto(nombre)
    raiz = re.match(r"<svg\b[^>]*>", texto)
    assert raiz, f"{nombre}: no empieza con la etiqueta <svg>"
    etiqueta = raiz.group()
    for atributo in ('viewBox="', 'role="img"', "aria-label="):
        assert atributo in etiqueta, f"{nombre}: <svg> sin {atributo}"
    assert re.search(r'\bwidth="\d', etiqueta), (
        f"{nombre}: <svg> sin width propio; el sitio lo incrusta con <img> y "
        "sin tamano intrinseco cae a ~300x150 px"
    )
    assert re.search(r'\bheight="\d', etiqueta), f"{nombre}: <svg> sin height propio"
    assert f'fill="{FONDO}"' in texto, f"{nombre}: sin el fondo del skin ({FONDO})"


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_trae_title_y_desc(nombre):
    """Convencion NUEVA de esta unidad: ningun SVG del curso los traia.

    aria-label lo lee un lector de pantalla, pero <title> es lo que muestran
    los visores de SVG y lo que aparece al abrir el archivo suelto.
    """
    texto = _texto(nombre)
    for etiqueta in ("<title>", "<desc>"):
        assert etiqueta in texto, f"{nombre}: sin {etiqueta}"
    titulo = re.search(r"<title>(.*?)</title>", texto).group(1)
    desc = re.search(r"<desc>(.*?)</desc>", texto).group(1)
    assert len(titulo) >= 8, f"{nombre}: <title> demasiado corto"
    assert len(desc) >= 40, f"{nombre}: <desc> no describe lo que se ve"


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ningun_diagrama_usa_fill_opacity(nombre):
    """Se publico una vez un sombreado opaco que tapaba dos curvas.

    mezclar() devuelve el color ya fundido contra el fondo, que se ve igual en
    los renderizadores que ignoran la opacidad.
    """
    assert "fill-opacity" not in _texto(nombre)
    assert "stroke-opacity" not in _texto(nombre)


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_cada_diagrama_parsea_como_xml(nombre):
    ET.fromstring(_texto(nombre))


def test_no_queda_ningun_svg_huerfano():
    en_disco = {p.stem for p in ASSETS_OPTIMIZACION.glob("*.svg")}
    assert en_disco == set(gen.DIAGRAMAS), (
        "sobran o faltan SVG frente al catalogo: "
        f"{en_disco ^ set(gen.DIAGRAMAS)}"
    )


def test_ningun_svg_sin_pagina_que_lo_use():
    """El mapa de huerfanos compara disco contra catalogo, y eso deja pasar un
    diagrama generado, acreditado, y que ninguna pagina enlaza. Historia y
    agentes tienen esta guarda; optimizacion no la tenia.

    Recorre con rglob porque las paginas de la unidad estan anidadas por clase,
    y salta los directorios de soporte: _assets/CREDITOS.md nombra TODOS los
    SVG, asi que incluirlo dejaria pasar justo el caso que esta guarda busca
    —acreditado y sin enlazar—."""
    unidad = ASSETS_OPTIMIZACION.parent
    renderizadas = sorted(
        p for p in unidad.rglob("*.md")
        if not any(parte.startswith("_") for parte in p.relative_to(unidad).parts)
    )
    paginas = "\n".join(p.read_text(encoding="utf-8") for p in renderizadas)
    sin_usar = sorted(
        svg.name for svg in ASSETS_OPTIMIZACION.glob("*.svg")
        if svg.name not in paginas
    )
    assert not sin_usar, f"SVG que ninguna pagina enlaza: {sin_usar}"


def test_cada_svg_tiene_fila_en_creditos():
    filas = filas_de_creditos(ASSETS_OPTIMIZACION)
    for nombre in gen.DIAGRAMAS:
        assert f"{nombre}.svg" in filas, f"{nombre}.svg sin fila en CREDITOS.md"


def test_los_dos_que_calculan_usan_la_geometria_exacta():
    """opt-poligono y opt-curvas-de-nivel no llevan coordenadas a mano.

    Si un parametro del fabricador cambia, el dibujo tiene que cambiar solo.
    Esta prueba fija las cinco esquinas que la aritmetica exacta produce hoy y
    comprueba que los rotulos del SVG las nombran.
    """
    V = gen.vertices()
    assert sorted((int(x), int(y)) for x, y in V) == [
        (0, 0), (0, 9), (2, 8), (8, 2), (9, 0)
    ], f"las esquinas del episodio cambiaron: {V}"
    mejor = max(V, key=gen.valor)
    assert (int(mejor[0]), int(mejor[1])) == (8, 2)
    assert int(gen.valor(mejor)) == 38
    texto = _texto("opt-poligono")
    for x, y in V:
        assert gen.rotulo((x, y)) in texto, (
            f"opt-poligono no rotula la esquina {gen.rotulo((x, y))}"
        )


def test_el_rotulo_de_cada_esquina_esta_declarado():
    """ROTULOS se ajusto a mano mirando el render; si nace una esquina nueva,
    su desplazamiento no existe y el generador reventaria al dibujarla."""
    claves = {(int(x), int(y)) for x, y in gen.vertices()}
    assert claves <= set(gen.ROTULOS), f"esquinas sin desplazamiento: {claves - set(gen.ROTULOS)}"


# --------------------------------------------------------------------------
# Aritmetica exacta del poliedro con sello.
#
# Copiado literal de docs/superpowers/verificacion-optimizacion/clase2.py, que
# es la hoja canonica de la clase. Solo fractions, itertools y math: el job
# `checks` de CI no instala scipy, numpy ni sympy.
#
# `vecinos_por_arista` aterriza aqui aunque esta guarda no lo llame: las
# paginas 3 y 4 tabulan vecinos, y sus guardas lo necesitan. Y decide por
# RANGO n-1, no por conteo: contar activas compartidas declara vecinos a los
# extremos de la diagonal de una cara, y esa version falsa ya se publico una
# vez en el primer borrador del diseno.

def _reducir(M, ncol):
    """Gauss-Jordan sobre fracciones. Devuelve (matriz reducida, columnas pivote)."""
    M = [fila[:] for fila in M]
    piv, r = [], 0
    for col in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        f = M[r][col]
        M[r] = [v / f for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                fa = M[i][col]
                M[i] = [a - fa * b for a, b in zip(M[i], M[r])]
        piv.append(col)
        r += 1
        if r == len(M):
            break
    return M, piv


def rango(filas, n):
    if not filas:
        return 0
    _, piv = _reducir([[F(v) for v in f] for f in filas], n)
    return len(piv)


def resolver_cuadrado(filas, rhs, n):
    """Solucion unica de un sistema n x n, o None si es singular."""
    M, piv = _reducir([[F(v) for v in f] + [F(r)] for f, r in zip(filas, rhs)], n)
    if len(piv) != n:
        return None
    return [M[i][n] for i in range(n)]


def _sistema(A, b, n):
    """Todas las restricciones como (fila, lado derecho), con las no negatividades."""
    filas = [(A[i], b[i]) for i in range(len(A))]
    filas += [([-1 if j == k else 0 for j in range(n)], 0) for k in range(n)]
    return filas


def vertices(A, b, n):
    filas = _sistema(A, b, n)
    V = []
    for idx in combinations(range(len(filas)), n):
        x = resolver_cuadrado([filas[i][0] for i in idx], [filas[i][1] for i in idx], n)
        if x is None or any(v < 0 for v in x):
            continue
        if any(sum(a * xx for a, xx in zip(A[i], x)) > b[i] for i in range(len(A))):
            continue
        if x not in V:
            V.append(x)
    return V


def activas(A, b, n, x):
    filas = _sistema(A, b, n)
    return frozenset(i for i, (a, bb) in enumerate(filas)
                     if sum(ai * xi for ai, xi in zip(a, x)) == bb)


def vecinos_por_arista(A, b, n, v, w):
    """La relacion buena: comparten n-1 activas INDEPENDIENTES."""
    if v == w:
        return False
    filas = _sistema(A, b, n)
    comp = activas(A, b, n, v) & activas(A, b, n, w)
    return rango([filas[i][0] for i in comp], n) == n - 1


def test_el_poliedro_del_sello_tiene_los_ocho_vertices_que_la_pagina_tabula():
    """La pagina 2 tabula ocho vertices con sus restricciones activas, y la
    traza de la pagina 4 se verifica contra esa tabla. Si el poliedro cambia,
    las dos paginas mienten a la vez."""
    A = [[1, 1, 1], [2, 1, 2], [1, 2, 3]]
    b = [10, 18, 18]
    c = [4, 3, 5]
    V = vertices(A, b, 3)
    assert len(V) == 8, f"el poliedro tiene {len(V)} vertices, no 8"
    assert all(len(activas(A, b, 3, v)) == 3 for v in V), "hay un vertice degenerado"
    z = max(sum(ci * xi for ci, xi in zip(c, v)) for v in V)
    arg = [v for v in V if sum(ci * xi for ci, xi in zip(c, v)) == z]
    assert z == 41 and len(arg) == 1, "el optimo no es (5,2,3)=41 unico"
    assert all(sum(A[i][j] * arg[0][j] for j in range(3)) == b[i] for i in range(3)), \
        "el optimo ya no consume los tres recursos exactos, y de eso vive la pagina 5"
    # La pagina tiene que tabular los ocho, y nombrar bien lo que se acaba en
    # cada uno. Esta segunda mitad existe porque la primera version del diseno
    # decia que en (0,9,0) estaba activo el polimero, y no lo esta: 9 de 18.
    # Una tabla de restricciones activas se escribe sola en la cabeza y sale mal.
    texto = (ASSETS_OPTIMIZACION.parent / "2_lineal" /
             "2_cuando_se_acaba_el_dibujo.md").read_text(encoding="utf-8")
    bloque = texto.split("{#opt-ocho-vertices")[1].split(":::")[0]
    filas = [l for l in bloque.splitlines()
             if l.strip().startswith("|") and "---" not in l and "Plan" not in l]
    assert len(filas) == 8, f"la tabla tiene {len(filas)} filas de datos, no 8"
    recursos = {0: "horas", 1: "polimero", 2: "energia"}
    esperado = sorted(
        sorted(recursos[i] for i in activas(A, b, 3, v) if i in recursos)
        for v in V
    )

    def normaliza(s):
        return s.replace("ó", "o").replace("í", "i").replace("é", "e").lower()

    visto = sorted(
        sorted(r for r in recursos.values() if r in normaliza(f.split("|")[3]))
        for f in filas
    )
    assert visto == esperado, f"las restricciones activas no cuadran:\n{visto}\n{esperado}"
