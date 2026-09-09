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


def test_la_traza_de_simplex_en_dos_variables_es_la_que_la_pagina_imprime():
    """La pagina 3 tabula tres filas con los vecinos de cada vertice y su valor,
    y opt-camino-simplex dibuja esa misma traza.

    Si el poligono cambia, la tabla deja de ser comprobable con el dibujo, que
    es la unica razon de que el ejemplo a mano sea de dos variables. La
    vecindad se decide por RANGO n-1, no contando activas: contar declara
    vecinos a los extremos de la diagonal de una cara, y clase2.py trae el
    contraejemplo en cuatro dimensiones.
    """
    A = [[1, 1], [2, 1], [1, 2]]
    b = [10, 18, 18]
    c = [4, 3]
    V = vertices(A, b, 2)
    val = lambda v: sum(ci * xi for ci, xi in zip(c, v))
    camino = [[F(0), F(0)]]
    while True:
        mej = [w for w in V
               if vecinos_por_arista(A, b, 2, camino[-1], w) and val(w) > val(camino[-1])]
        if not mej:
            break
        camino.append(max(mej, key=val))
    assert [[int(x) for x in v] for v in camino] == [[0, 0], [9, 0], [8, 2]], camino
    assert val(camino[-1]) == 38
    assert len(camino) == 3 and len(V) == 5, "ya no visita 3 de 5"

    # Y el generador tiene que llegar a la misma traza por su propia cuenta:
    # el dibujo la calcula, no la transcribe.
    assert [gen.rotulo(p) for p in gen.camino_simplex()] == ["(0, 0)", "(9, 0)", "(8, 2)"]

    # Las tres filas de la tabla publicada, con sus vecinos y sus valores.
    texto = (ASSETS_OPTIMIZACION.parent / "2_lineal" /
             "3_de_esquina_en_esquina.md").read_text(encoding="utf-8")
    bloque = texto.split("{#opt-traza-simplex")[1].split(":::")[0]
    filas = [l for l in bloque.splitlines()
             if l.strip().startswith("|") and "---" not in l and "Estoy en" not in l]
    assert len(filas) == 3, f"la tabla tiene {len(filas)} filas de datos, no 3"
    for fila, v in zip(filas, camino):
        celdas = [c.strip() for c in fila.strip().strip("|").split("|")]
        rot = "$(%d,%d)$" % (int(v[0]), int(v[1]))
        assert celdas[0] == rot, f"la fila dice {celdas[0]}, no {rot}"
        assert celdas[1].strip("*") == str(int(val(v))), f"{rot}: valor mal en la tabla"
        esperados = sorted(w for w in V if vecinos_por_arista(A, b, 2, v, w))
        for w in esperados:
            marca = "$(%d,%d)=%d$" % (int(w[0]), int(w[1]), int(val(w)))
            assert marca in celdas[2], f"{rot}: falta el vecino {marca}"
        assert celdas[2].count("$(") == len(esperados), (
            f"{rot}: la celda de vecinos lista {celdas[2].count('$(')} y son "
            f"{len(esperados)}"
        )


def test_la_traza_con_sello_pasa_por_la_parada_fraccionaria():
    """Tres pivotes, cuatro vertices de ocho, y la parada intermedia tiene
    coordenadas partidas: la pagina la nombra en vez de esconderla, y de ahi
    sale el enganche con la clase 4.

    La pagina 4 no tiene diagrama: su figura es la tabla de los ocho de la
    pagina 2, asi que lo unico que ata su traza a la aritmetica es esta guarda.
    """
    A, b, c = [[1, 1, 1], [2, 1, 2], [1, 2, 3]], [10, 18, 18], [4, 3, 5]
    V = vertices(A, b, 3)
    val = lambda v: sum(ci * xi for ci, xi in zip(c, v))
    camino = [[F(0)] * 3]
    while True:
        mej = [w for w in V
               if vecinos_por_arista(A, b, 3, camino[-1], w) and val(w) > val(camino[-1])]
        if not mej:
            break
        camino.append(max(mej, key=val))
    assert len(camino) == 4 and val(camino[-1]) == 41
    assert len(V) == 8, "ya no visita 4 de 8"
    assert camino[2] == [F(9, 2), F(0), F(9, 2)]
    assert camino[2][0].denominator == 2, "la parada fraccionaria desaparecio"

    # El paso que la elige le gana a (8,2,0) por DOS CREDITOS Y MEDIO, no por
    # medio: el spec y la etiqueta de clase2.py decian "medio credito" y
    # 81/2 - 38 = 5/2. La pagina imprime el margen, asi que va pineado aqui.
    assert val(camino[2]) - val([F(8), F(2), F(0)]) == F(5, 2)

    # Las cuatro filas publicadas, con sus tres vecinos y sus valores.
    def rotulo(v):
        partes = []
        for q in v:
            partes.append(str(q.numerator) if q.denominator == 1
                          else r"\tfrac%d%d" % (q.numerator, q.denominator))
        return "(" + ",".join(partes) + ")"

    def valor(v):
        z = F(val(v))
        return (str(z.numerator) if z.denominator == 1
                else r"\tfrac{%d}{%d}" % (z.numerator, z.denominator))

    texto = (ASSETS_OPTIMIZACION.parent / "2_lineal" /
             "4_sin_dibujo.md").read_text(encoding="utf-8")
    bloque = texto.split("{#opt-traza-sello")[1].split(":::")[0]
    filas = [l for l in bloque.splitlines()
             if l.strip().startswith("|") and "---" not in l and "Estoy en" not in l]
    assert len(filas) == 4, f"la tabla tiene {len(filas)} filas de datos, no 4"
    for fila, v in zip(filas, camino):
        celdas = [x.strip() for x in fila.strip().strip("|").split("|")]
        rot = f"${rotulo(v)}$"
        assert celdas[0] == rot, f"la fila dice {celdas[0]}, no {rot}"
        assert celdas[1].strip("*$") == valor(v), f"{rot}: valor mal en la tabla"
        esperados = [w for w in V if vecinos_por_arista(A, b, 3, v, w)]
        assert len(esperados) == 3, f"{rot}: {len(esperados)} vecinos, no 3"
        for w in esperados:
            marca = f"${rotulo(w)}={valor(w)}$"
            assert marca in celdas[2], f"{rot}: falta el vecino {marca}"
        assert celdas[2].count("$(") == 3, (
            f"{rot}: la celda de vecinos lista {celdas[2].count('$(')} y son 3"
        )


def _pagina_5():
    return (ASSETS_OPTIMIZACION.parent / "2_lineal" /
            "5_cuanto_vale_una_hora_mas.md").read_text(encoding="utf-8")


def _filas_publicadas(texto, id_tabla, cabecera):
    bloque = texto.split("{#" + id_tabla)[1].split(":::")[0]
    return [l for l in bloque.splitlines()
            if l.strip().startswith("|") and "---" not in l and cabecera not in l]


def test_la_serie_de_horas_y_su_fila_de_diferencias():
    """La fila que la pagina imprime es lo que gano ESA hora respecto de la
    anterior. La version anterior la rotulo "lo que gana la hora siguiente" con
    estos mismos numeros, y entonces dos celdas eran falsas: la fila hacia
    adelante tiene SEIS entradas y empieza en 4, 2, no en 4, 4.

    Por eso la guarda afirma las dos filas y ademas lee el rotulo publicado.
    """
    A, c = [[1, 1], [2, 1], [1, 2]], [4, 3]
    z = lambda h: max(sum(ci * xi for ci, xi in zip(c, v))
                      for v in vertices(A, [h, 18, 18], 2))
    serie = [z(h) for h in range(8, 15)]
    assert serie == [32, 36, 38, 40, 42, 42, 42]
    gano_esa_hora = [serie[0] - z(7)] + [serie[i] - serie[i - 1] for i in range(1, 7)]
    assert gano_esa_hora == [4, 4, 2, 2, 2, 0, 0]
    assert [serie[i + 1] - serie[i] for i in range(6)] == [4, 2, 2, 2, 0, 0], \
        "la fila hacia adelante es OTRA y tiene seis entradas, no siete"

    # Los dos codos: la hora vale 2 entre 9 y 12, y el rango tiene DOS extremos.
    assert gano_esa_hora[1] == 4 and gano_esa_hora[2] == 2, "el codo de abajo, en 9"
    assert gano_esa_hora[4] == 2 and gano_esa_hora[5] == 0, "el codo de arriba, en 12"

    texto = _pagina_5()
    assert "ganó esa hora" in texto, (
        "el rotulo de la tercera columna es 'lo que gano ESA hora'; con "
        "'la hora siguiente' dos celdas de la tabla son falsas"
    )
    assert "hora siguiente" not in texto.split("{#opt-valor-por-hora")[1].split(":::")[0]
    filas = _filas_publicadas(texto, "opt-valor-por-hora", "Horas disponibles")
    assert len(filas) == 7, f"la tabla tiene {len(filas)} filas de datos, no 7"
    for fila, h, zz, d in zip(filas, range(8, 15), serie, gano_esa_hora):
        celdas = [x.strip().strip("*") for x in fila.strip().strip("|").split("|")]
        assert len(celdas) == 3, "la tabla va transpuesta: tres columnas, siete filas"
        assert celdas[0] == str(h), f"{celdas[0]}: la primera columna son las horas"
        assert celdas[1] == str(zz), f"h={h}: el optimo publicado no es {zz}"
        assert int(celdas[2].replace("+", "")) == d, f"h={h}: gano {d}, no {celdas[2]}"


def test_los_tres_numeros_del_certificado_son_los_precios_sombra():
    """El enganche entero de la pagina. Si dejan de coincidir, la revelacion
    es falsa y hay que reescribir la seccion, no ajustar el numero."""
    A, b, c = [[1, 1], [2, 1], [1, 2]], [10, 18, 18], [4, 3]
    z = lambda bb: max(sum(ci * xi for ci, xi in zip(c, v)) for v in vertices(A, bb, 2))
    base = z(b)
    y = [z([b[i] + (1 if k == i else 0) for i in range(3)]) - base for k in range(3)]
    assert y == [2, 1, 0], y
    assert base == 38 and sum(y[i] * b[i] for i in range(3)) == 38
    assert y[2] == 0, "el recurso que sobra tiene que tener precio cero"

    # Y la tabla de holguras que la pagina publica al lado, que es de donde
    # sale que el cero cae justo en el recurso que sobra.
    optimo = max(vertices(A, b, 2), key=lambda v: sum(ci * xi for ci, xi in zip(c, v)))
    holguras = [b[i] - sum(A[i][j] * optimo[j] for j in range(2)) for i in range(3)]
    assert holguras == [0, 0, 6], holguras
    filas = _filas_publicadas(_pagina_5(), "opt-estado-recursos", "Recurso")
    assert len(filas) == 3, f"la tabla tiene {len(filas)} filas de datos, no 3"
    for fila, i in zip(filas, range(3)):
        celdas = [x.strip().strip("*") for x in fila.strip().strip("|").split("|")]
        gasta = b[i] - holguras[i]
        assert [celdas[1], celdas[2], celdas[3]] == [str(b[i]), str(gasta),
                                                     str(holguras[i])], celdas


def test_el_diagrama_del_precio_sombra_calcula_sus_tres_optimos():
    """opt-fig-precio-sombra no lleva coordenadas a mano: los tres optimos y
    las dos regiones salen de recortar el episodio con 10, 11 y 12 horas.

    Fija ademas la concurrencia, que es lo que el dibujo tiene que ensenar: con
    12 horas la region pierde una esquina porque las tres rectas de recurso
    pasan por (6, 6).
    """
    # Las tres posiciones de la recta no son tres numeros elegidos a mano: la
    # primera es lo que hay, y la ultima es el codo de arriba, el primer h en el
    # que una hora mas ya no mueve el optimo. Sin esto, dibujar 13 en vez de 12
    # pasaba la guarda, porque con 13 el optimo sigue siendo (6, 6).
    assert gen.HORAS[0] == gen.B[0], "la primera posicion es lo disponible hoy"
    assert list(gen.HORAS) == [gen.HORAS[0] + k for k in range(3)], "van de una en una"
    codo = next(h for h in range(gen.B[0], 40)
                if gen.optimo_con_horas(h) == gen.optimo_con_horas(h + 1))
    assert gen.HORAS[-1] == codo, f"el codo de arriba esta en {codo}, no en {gen.HORAS[-1]}"

    esperados = ["(8, 2)", "(7, 4)", "(6, 6)"]
    optimos = [gen.optimo_con_horas(h) for h in gen.HORAS]
    assert [gen.rotulo(p) for p in optimos] == esperados, optimos
    assert [int(gen.valor(p)) for p in optimos] == [38, 40, 42]
    # los tres caen sobre la arista del polimero, 2x1 + x2 = 18
    assert all(2 * p[0] + p[1] == 18 for p in optimos), "ya no corren por esa arista"
    # el 12 se deriva de HORAS y de B, no se clava: con una hora menos la region
    # tiene cinco esquinas, y es perder una lo que dice que hay concurrencia
    ultimo = [gen.HORAS[-1]] + gen.B[1:]
    assert len(gen._region(gen.A, ultimo)) == 4, (
        f"con {gen.HORAS[-1]} horas la region tiene cuatro esquinas: en "
        f"{gen.rotulo(optimos[-1])} concurren las tres rectas de recurso"
    )
    assert len(gen._region(gen.A, [gen.HORAS[-2]] + gen.B[1:])) == 5, (
        "una hora antes todavia son cinco: la esquina se pierde en el codo"
    )
    texto = _texto("opt-fig-precio-sombra")
    for rot, valor in zip(esperados, (38, 40, 42)):
        assert f"{rot} = {valor}" in texto, f"el diagrama no rotula {rot} = {valor}"


# --------------------------------------------------------------------------
# Guarda de rotulos: ningun trazo parte un rotulo de vertice.
#
# Nace de tres defectos reales de esta rama que el ojo no vio a tamano normal:
# el rotulo (2,8,0) de opt-fig-poliedro partido por la arista punteada de x2, y
# el rotulo (0,9) de opt-poligono con la recta de las horas metida por el
# parentesis de apertura. Se ven ampliando el render a 4x, o midiendo.
#
# Esta ESTRECHADA a proposito, en vez de aflojar un umbral hasta que no muerda:
#
#   - Solo segmentos de linea RECTOS (<line>).
#
#     ESTO DEJA UN HUECO DE COBERTURA, y hay que nombrarlo entero: **ningun
#     trazo que no sea <line> se comprueba**. Quedan fuera, aunque lleven
#     informacion: el contorno del poligono (un <path>, a grosor 2 en
#     opt-camino-simplex y a 2.5 en opt-fig-circulos), las curvas de nivel
#     circulares (<circle>, a grosor 3 la de dentro y 2 las otras tres), **los
#     aros huecos de los vertices, que tambien son <circle> y van a grosor
#     2.5** —el de la parada de opt-camino-simplex, el de sus dos esquinas sin
#     visitar, el de (8,2,0) en opt-fig-poliedro y el de (6,6) en
#     opt-fig-precio-sombra—, los trazos de opt-fig-matriz, y **todas las
#     puntas de flecha, porque son <marker> y no <line>**. Hoy ninguno de esos
#     cruza un rotulo de vertice —medido—, asi que no hay defecto vivo
#     escondido detras del hueco; pero un rotulo partido por una punta de
#     flecha o por el borde del poligono pasaria esta guarda.
#
#     Se aceptan fuera por dos razones distintas. Los <path> y <circle> que
#     rotulan curvas llevan placa de fondo debajo —el arreglo publicado en
#     opt-fig-circulos—, asi que una guarda geometrica los marcaria aunque
#     esten bien. Y los <marker> no tienen geometria propia en el documento:
#     habria que reconstruir el triangulo desde el extremo y la orientacion de
#     su linea, que es una segunda guarda, no un umbral de esta.
#   - Solo trazos de grosor >= 1.5. La rejilla de _plano va a grosor 1 y al 40%
#     del color de linea: pasa por detras de un rotulo sin partir ningun glifo,
#     y ademas es inevitable —la rejilla va cada 68 px y un rotulo con valor
#     mide casi 80—. Todo trazo que lleva informacion (ejes, rectas, aristas,
#     flechas) va a 1.6 o mas.
#   - Solo ROTULOS DE VERTICE: los que empiezan con un parentesis y un digito,
#     «(0, 9)», «(8, 2) = 38», «(5, 2, 3) = 41». Son los que van pegados al
#     dibujo y no pueden llevar placa.
#
# La caja de cada rotulo es una ESTIMACION (0.55 em por caracter), no la
# metrica real de la fuente: para el ancho de glifos latinos en una sans del
# sistema se queda corta antes que larga, que es el lado seguro para no
# inventar defectos.

_ROTULO_DE_VERTICE = re.compile(r"^\(\s*-?\d")


def _caja_de_texto(t):
    x, y = float(t.get("x")), float(t.get("y"))
    tam = float(t.get("font-size"))
    ancho = len(t.text or "") * tam * 0.55
    anclaje = t.get("text-anchor", "start")
    x0 = x if anclaje == "start" else (x - ancho if anclaje == "end" else x - ancho / 2)
    return (x0, y - tam * 0.78, x0 + ancho, y + tam * 0.22)


def _trazos_rectos(raiz, grosor_minimo=1.5):
    fuera = []
    for e in raiz.iter():
        if e.tag.split("}")[-1] != "line":
            continue
        if e.get("stroke") in (None, "none"):
            continue
        if float(e.get("stroke-width", 1)) < grosor_minimo:
            continue
        fuera.append(tuple(float(e.get(k)) for k in ("x1", "y1", "x2", "y2")))
    return fuera


def _atraviesa(seg, caja, pasos=200):
    x1, y1, x2, y2 = seg
    izq, arr, der, aba = caja
    for k in range(pasos + 1):
        x = x1 + (x2 - x1) * k / pasos
        y = y1 + (y2 - y1) * k / pasos
        if izq <= x <= der and arr <= y <= aba:
            return True
    return False


def rotulos_partidos(svg):
    """Los rotulos de vertice que un trazo recto atraviesa, con su trazo."""
    raiz = ET.fromstring(svg)
    trazos = _trazos_rectos(raiz)
    malos = []
    for t in raiz.iter():
        if t.tag.split("}")[-1] != "text":
            continue
        if not _ROTULO_DE_VERTICE.match((t.text or "").strip()):
            continue
        caja = _caja_de_texto(t)
        for seg in trazos:
            if _atraviesa(seg, caja):
                malos.append((t.text, tuple(round(v, 1) for v in seg)))
                break
    return malos


@pytest.mark.parametrize("nombre", sorted(gen.DIAGRAMAS))
def test_ningun_rotulo_de_vertice_queda_partido_por_un_trazo(nombre):
    malos = rotulos_partidos(_texto(nombre))
    assert not malos, (
        f"{nombre}: un trazo atraviesa el rotulo de un vertice "
        "(se ve ampliando el render a 4x, no a tamano normal):\n"
        + "\n".join(f"   {t!r} lo cruza {s}" for t, s in malos)
    )


def test_la_guarda_de_rotulos_si_puede_fallar():
    """Una guarda que no puede fallar es peor que ninguna.

    Los dos escenarios son los dos defectos historicos: un rotulo encima de un
    trazo, y un trazo que le pasa por encima a un rotulo que estaba limpio.
    """
    cabeza = ('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" '
              'viewBox="0 0 200 100">')
    rotulo = '<text x="60" y="50" font-size="13" text-anchor="start">(8, 2) = 38</text>'
    limpio = cabeza + '<line x1="0" y1="90" x2="200" y2="90" stroke="#fff" ' \
                      'stroke-width="2"/>' + rotulo + "</svg>"
    assert rotulos_partidos(limpio) == [], "la guarda marca un SVG que esta bien"

    encima = cabeza + '<line x1="0" y1="46" x2="200" y2="46" stroke="#fff" ' \
                      'stroke-width="2"/>' + rotulo + "</svg>"
    assert rotulos_partidos(encima), "la guarda no vio un trazo sobre el rotulo"

    # Y la rejilla, a grosor 1, se queda fuera a proposito: pasa por detras.
    rejilla = cabeza + '<line x1="0" y1="46" x2="200" y2="46" stroke="#fff" ' \
                       'stroke-width="1"/>' + rotulo + "</svg>"
    assert rotulos_partidos(rejilla) == [], "la rejilla no deberia contar"
