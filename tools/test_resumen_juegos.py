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
    "¿Garantiza $V$?",
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


def tramos_de_ficha(lineas):
    """(i_ficha, i_cierre) de cada «## Ficha: …», con el cierre que la sigue.

    Una página que absorbió a otra trae una ficha y un cierre por cada parte;
    cada ficha se mide contra su propio cierre, no contra el primero."""
    tramos = []
    for i, s in enumerate(lineas):
        if s.startswith("## Ficha: "):
            tramos.append((i, lineas.index(gen.CIERRE, i)))
    assert tramos, "la página no tiene «## Ficha: …»"
    return tramos


def fichas(archivo):
    """{nombre del algoritmo: {rasgo: celda}} de cada `::: table {#jue-ficha-…}`
    entre cada «## Ficha: …» y su cierre, en el orden de la página."""
    lineas = texto(archivo).split("\n")
    tramo = "\n\n".join("\n".join(lineas[i:k]) for i, k in tramos_de_ficha(lineas))
    salida = {}
    for m in re.finditer(r"^::: table \{#jue-ficha-[a-z-]+ title=\"[^\"]+\"\}\n(.*?)^:::",
                         tramo, re.M | re.S):
        renglones = [r for r in m.group(1).splitlines() if r.startswith("|")]
        enc = [c.strip() for c in renglones[0].strip("|").split("|")]
        filas = [[c.strip() for c in r.strip("|").split("|")] for r in renglones[2:]]
        assert len(enc) == 2 and enc[0] == "Rasgo", (
            f"{archivo}: cada ficha lleva dos columnas, Rasgo y su algoritmo "
            "(con tres, a 390 px la tercera se esconde tras el scroll)")
        assert all(len(f) == 2 for f in filas)
        salida[enc[1]] = {f[0]: f[1] for f in filas}
        salida[enc[1]]["_orden"] = [f[0] for f in filas]
    return salida


@pytest.mark.parametrize("archivo", PAGINAS)
def test_la_ficha_va_antes_del_cierre_con_sus_siete_rasgos(archivo):
    t = texto(archivo)
    lineas = t.split("\n")
    tramos = tramos_de_ficha(lineas)
    lugares = gen.localizar_todos(lineas)
    for i_ficha, i_cierre in tramos:
        assert i_ficha < i_cierre
        assert not re.search(r"\$|\[\[", lineas[i_ficha]), "la ficha no lleva LaTeX ni enlaces en su encabezado"
        # El recuadro va justo después de la ficha, antes de su cierre.
        assert any(i_ficha < i < i_cierre for i, _ in lugares), (
            f"{archivo}: la ficha de la línea {i_ficha + 1} no lleva su recuadro antes del cierre")
    f = fichas(archivo)
    assert f, f"{archivo}: la ficha no está en un ::: table {{#jue-ficha-…}}"
    propios = [a["nombre"] for a in gen.ALGORITMOS if a["archivo"] == archivo]
    # Una ficha por algoritmo de la página. En una página que absorbió a otra
    # van en el orden de la página (la de «Jugar contra el reloj» trae
    # iterativa y luego quietud); el orden del curso lo fija el recuadro.
    assert sorted(f) == sorted(propios) and len(f) == len(propios), (
        "una ficha por algoritmo de la página")
    if len(tramos) == 1:
        assert list(f) == propios, "una ficha por algoritmo de la página, en el orden del curso"
    for nombre, rasgos in f.items():
        assert rasgos["_orden"] == RASGOS, nombre


@pytest.mark.parametrize("archivo", PAGINAS)
def test_ficha_y_recuadro_dicen_lo_mismo_de_si_garantiza_v(archivo):
    """Una sola convención: «¿Garantiza $V$?» dice si el algoritmo, por cómo
    funciona, devuelve el valor minimax. Sí: minimax, expectiminimax (el del
    juego con dado), alfa-beta (en la raíz). No: los demás; corte, quietud e
    iterativa con la salvedad de los finales."""
    f = fichas(archivo)
    for alg in gen.ALGORITMOS:
        if alg["archivo"] != archivo:
            continue
        celda = f[alg["nombre"]]["¿Garantiza $V$?"]
        assert celda.startswith(alg["garantiza"]), (alg["nombre"], celda)
        if alg["garantiza"] == "Sí":
            assert alg["numero"].endswith("lo garantiza"), alg["nombre"]
        else:
            assert "no garantiza $V$" in alg["numero"], alg["nombre"]
            assert "salvo si" not in alg["numero"] or "salvo si" in celda, alg["nombre"]


def test_quien_garantiza_v_es_lo_que_dice_la_convencion():
    garantiza = {a["nombre"]: a["garantiza"] for a in gen.ALGORITMOS}
    assert [n for n, g in garantiza.items() if g == "Sí"] == [
        "Minimax", "Expectiminimax", "Alfa-beta"]
    salvedad = [a["nombre"] for a in gen.ALGORITMOS if "salvo si llega a los finales" in a["numero"]]
    assert salvedad == ["Minimax con corte", "Búsqueda de quietud", "Profundización iterativa"]
    assert "converge" in gen.ALGORITMOS[-1]["numero"]


def test_la_quietud_y_mcts_dicen_lo_que_hacen():
    """Brief r2 W3: la salvedad de la quietud es «antes de cortar», la misma
    de GARANTIZA_TPM (aun con capturas hasta los finales, quedarse usa EVAL);
    y «Lo que viene» de MCTS dice que construye un árbol, no «lo mismo» que
    Monte Carlo plano."""
    import juegos as j
    por = {a["nombre"]: a for a in gen.ALGORITMOS}
    assert por["Búsqueda de quietud"]["numero"].endswith(
        "salvo si llega a los finales antes de cortar")
    assert j.GARANTIZA_TPM["quietud"] == "No, salvo si llega a los finales antes de cortar"
    assert por["MCTS con UCT"]["viene"] == (
        "construye un árbol: elige por puntaje dentro de él, lo hace crecer, simula desde la "
        "hoja y sube el resultado; manda más partidas a lo que va mejor sin dejar de probar "
        "lo otro")
    assert "menos nodos" not in " ".join(a["viene"] + a["numero"] for a in gen.ALGORITMOS)
