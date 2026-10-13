"""El recuadro «Lo que ya viste» y la ficha de cada página de algoritmo de juegos.

El recuadro lo escribe `gen_resumen_juegos.py` desde una sola lista,
`ALGORITMOS`. Estas pruebas comparan sin escribir: si alguien edita el bloque
a mano o cambia la lista sin correr el generador, fallan con «corre el
generador». Además fijan lo que el recuadro promete al alumno: que muestra
solo lo ya visto, en orden, y que nada de lo que nombra viene de más adelante.
"""
import re

import pytest

import gen_resumen_juegos as gen

PAGINAS = gen.PAGINAS
RASGOS = [
    "Hasta dónde mira",
    "¿Genera todo el árbol?",
    "¿Da $V$ exacto?",
    "Con qué estima",
    "¿Quién tira dados?",
    "Qué entrega, y si se puede interrumpir",
    "Cuándo conviene",
]

# Palabras que delatan a cada algoritmo; una fila anterior no puede usarlas.
DELATORAS = {
    "Expectiminimax": ["Expectiminimax", "azar", "Pr"],
    "Alfa-beta": ["Alfa-beta", "alfa", "cota", "\\alpha"],
    "Minimax con corte": ["corte", "EVAL", "$d$"],
    "Búsqueda de quietud": ["quiet", "captura"],
    "Profundización iterativa": ["iterativa", "reloj", "última búsqueda"],
    "Monte Carlo plano": ["Monte Carlo", "\\bar u", "simula", "al azar"],
    "MCTS con UCT": ["MCTS", "UCT", "crece"],
}


def texto(archivo):
    return (gen.UNIDAD / archivo).read_text(encoding="utf-8")


def bloque_actual(archivo):
    lineas = texto(archivo).split("\n")
    lugar = gen.localizar(lineas)
    assert lugar, f"{archivo}: no tiene el recuadro «Lo que ya viste»"
    return lineas[lugar[0]:lugar[1]]


def filas_del_recuadro(archivo):
    renglones = [s[2:] for s in bloque_actual(archivo) if s.startswith("> |")]
    assert renglones[0] == gen.ENCABEZADO
    return [[c.strip() for c in r.strip("|").split("|")] for r in renglones[2:]]


@pytest.mark.parametrize("archivo", PAGINAS)
def test_el_recuadro_es_el_que_produce_el_generador(archivo):
    actual = texto(archivo)
    assert gen.contenido(archivo, actual) == actual, (
        f"{archivo}: el recuadro no es el de gen_resumen_juegos.py; "
        "corre el generador (python3 tools/gen_resumen_juegos.py)")


@pytest.mark.parametrize("archivo", PAGINAS)
def test_correr_el_generador_dos_veces_no_cambia_nada(archivo):
    una = gen.contenido(archivo, texto(archivo))
    assert gen.contenido(archivo, una) == una


@pytest.mark.parametrize("archivo", PAGINAS)
def test_el_recuadro_muestra_un_prefijo_que_termina_en_su_algoritmo(archivo):
    filas = filas_del_recuadro(archivo)
    nombres = [re.sub(r"\*\*|\s*\(estás aquí\)", "", f[0]) for f in filas]
    orden = [a["nombre"] for a in gen.ALGORITMOS]
    assert nombres == orden[: len(nombres)], "las filas no siguen el orden del curso"
    propios = [a["nombre"] for a in gen.ALGORITMOS if a["archivo"] == archivo]
    assert nombres[-1] == propios[-1], "el recuadro no termina en el algoritmo de la página"
    for fila, nombre in zip(filas, nombres):
        aqui = "(estás aquí)" in fila[0]
        assert aqui == (nombre in propios)
        if aqui:
            assert all(c.startswith("**") and c.endswith("**") for c in fila), (
                f"{nombre}: la fila de esta página va toda en negrita")


@pytest.mark.parametrize("archivo", PAGINAS)
def test_ninguna_fila_nombra_un_algoritmo_posterior(archivo):
    filas = filas_del_recuadro(archivo)
    orden = [a["nombre"] for a in gen.ALGORITMOS]
    for i, fila in enumerate(filas):
        celdas = " ".join(fila)
        for posterior in orden[i + 1:]:
            for palabra in DELATORAS.get(posterior, []):
                assert palabra not in celdas, (
                    f"{archivo}: la fila de {orden[i]} usa «{palabra}», de {posterior}")


@pytest.mark.parametrize("archivo", PAGINAS)
def test_lo_que_viene_va_en_palabras_llanas_y_solo_trae_lo_que_falta(archivo):
    bloque = bloque_actual(archivo)
    k = bloque.index("> **Lo que viene.**")
    viene = [s for s in bloque[k + 1:] if s.startswith("> - ")]
    pendientes = gen.pendientes(archivo)
    assert len(viene) == len(pendientes)
    for linea, alg in zip(viene, pendientes):
        assert linea.startswith(f"> - **{alg['nombre']}**")
        assert "$" not in linea, f"«Lo que viene» usa un símbolo: {linea}"
    if not pendientes:
        assert any(gen.SIN_PENDIENTES in s for s in bloque[k + 1:])


@pytest.mark.parametrize("archivo", PAGINAS)
def test_la_ficha_va_antes_del_cierre_con_sus_siete_rasgos(archivo):
    t = texto(archivo)
    lineas = t.split("\n")
    i_ficha = next(i for i, s in enumerate(lineas) if s.startswith("## Ficha: "))
    i_cierre = lineas.index(gen.CIERRE)
    assert i_ficha < i_cierre
    assert not re.search(r"\$|\[\[", lineas[i_ficha]), "la ficha no lleva LaTeX ni enlaces en su encabezado"
    m = re.search(r"^::: table \{#jue-ficha-[a-z-]+ title=\"[^\"]+\"\}\n(.*?)^:::",
                  "\n".join(lineas[i_ficha:i_cierre]), re.M | re.S)
    assert m, f"{archivo}: la ficha no está en un ::: table {{#jue-ficha-…}}"
    renglones = [r for r in m.group(1).splitlines() if r.startswith("|")]
    encabezado = [c.strip() for c in renglones[0].strip("|").split("|")]
    propios = [a["nombre"] for a in gen.ALGORITMOS if a["archivo"] == archivo]
    assert encabezado == ["Rasgo", *propios]
    filas = [[c.strip() for c in r.strip("|").split("|")] for r in renglones[2:]]
    assert [f[0] for f in filas] == RASGOS
    assert all(len(f) == len(encabezado) for f in filas)
    # El recuadro va justo después de la ficha.
    lugar = gen.localizar(lineas)
    assert lugar and i_ficha < lugar[0] < i_cierre
