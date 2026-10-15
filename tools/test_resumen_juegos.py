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
# Las propiedades canónicas de cada ficha (plan de homologación §3.3), en su
# orden: reemplazan a la tabla de siete rasgos de antes; «Garantía» hereda la
# fila «¿Garantiza $V$?».
PROPIEDADES = [
    "Número que da",
    "Usa EVAL",
    "Garantía",
    "Se puede interrumpir",
    "Complejidad",
    "Frente a los demás",
    "Supuestos",
]

# Palabras que delatan a cada algoritmo; una fila anterior no puede usarlas.
DELATORAS = {
    "Alfa-beta": ["Alfa-beta", "alfa", "cota", "\\alpha"],
    "Expectiminimax": ["Expectiminimax", "azar", "dado", "Pr"],
    "Minimax con corte": ["corte", "EVAL", "$d$"],
    "Búsqueda de quietud": ["quiet", "captura"],
    "Profundización iterativa": ["iterativa", "reloj", "última búsqueda"],
    "Monte Carlo plano": ["Monte Carlo", "\\widehat Q", "Q_{\\text{azar}}", "simula", "al azar"],
    "Monte Carlo con actualización minimax": ["actualización", "respaldo", "\\widehat V"],
    "MCTS con UCT": ["MCTS", "UCT", "crece", "bono", "vueltas"],
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


def tramos_de_ficha(lineas, archivo):
    """{nombre: (i_ficha, i_fin)} de cada ficha propia de la página: desde su
    encabezado `### <ficha>` hasta el siguiente `###` o `##`."""
    tramos = {}
    for alg in gen.ALGORITMOS:
        if alg["archivo"] != archivo:
            continue
        cabeza = f"### {alg['ficha']}"
        donde = [i for i, s in enumerate(lineas) if s.rstrip() == cabeza]
        assert len(donde) == 1, f"{archivo}: «{cabeza}» debe aparecer una vez"
        i = donde[0]
        k = next((j for j in range(i + 1, len(lineas))
                  if re.match(r"#{2,3} ", lineas[j])), len(lineas))
        tramos[alg["nombre"]] = (i, k)
    assert tramos, f"{archivo}: la página no tiene fichas"
    return tramos


def fichas(archivo):
    """{nombre del algoritmo: {propiedad: texto}} de la lista de «#### 3 ·
    Propiedades» de cada ficha, con `_orden` = las propiedades en su orden."""
    lineas = texto(archivo).split("\n")
    salida = {}
    for nombre, (i, k) in tramos_de_ficha(lineas, archivo).items():
        tramo = lineas[i:k]
        assert "#### 3 · Propiedades" in tramo, f"{archivo}: {nombre} sin «#### 3 · Propiedades»"
        j = tramo.index("#### 3 · Propiedades") + 1
        props, actual = {}, None
        orden = []
        while j < len(tramo) and not tramo[j].startswith("#"):
            m = re.match(r"- \*\*([^*]+):\*\* ?(.*)", tramo[j])
            if m:
                actual = m.group(1)
                orden.append(actual)
                props[actual] = m.group(2)
            elif actual and tramo[j].strip():   # renglón partido de la viñeta
                props[actual] += " " + tramo[j].strip()
            elif orden and not tramo[j].strip():
                break   # la lista de propiedades termina en su primer renglón en blanco
            j += 1
        props["_orden"] = orden
        salida[nombre] = props
    return salida


@pytest.mark.parametrize("archivo", PAGINAS)
def test_cada_ficha_va_antes_del_cierre_con_sus_siete_propiedades(archivo):
    """Antes: «la ficha va antes del cierre con sus siete rasgos». La tabla de
    rasgos se reemplazó por el mapa y las propiedades canónicas; la prueba
    conserva lo que fijaba: una ficha por algoritmo de la página, en el orden
    del curso, sin LaTeX ni enlaces en su encabezado, sus propiedades en orden,
    y el recuadro después de la última ficha y antes del cierre."""
    lineas = texto(archivo).split("\n")
    tramos = tramos_de_ficha(lineas, archivo)
    i_cierre = lineas.index(gen.CIERRE)
    propios = [a["nombre"] for a in gen.ALGORITMOS if a["archivo"] == archivo]
    assert sorted(tramos, key=lambda n: tramos[n][0]) == propios, (
        "una ficha por algoritmo de la página, en el orden del curso")
    for nombre, (i_ficha, _) in tramos.items():
        assert i_ficha < i_cierre
        assert not re.search(r"\$|\[\[", lineas[i_ficha]), (
            "la ficha no lleva LaTeX ni enlaces en su encabezado")
    ultima = max(i for i, _ in tramos.values())
    lugares = gen.localizar_todos(lineas)
    assert len(lugares) == 1, f"{archivo}: un solo recuadro por página"
    assert ultima < lugares[0][0] < i_cierre, (
        f"{archivo}: el recuadro va después de la última ficha y antes del cierre")
    f = fichas(archivo)
    for nombre, props in f.items():
        assert props["_orden"] == PROPIEDADES, nombre
        assert all(props[p].strip() for p in PROPIEDADES), nombre


@pytest.mark.parametrize("archivo", PAGINAS)
def test_ficha_y_recuadro_dicen_lo_mismo_de_si_garantiza_v(archivo):
    """Una sola convención: la propiedad «Garantía» dice si el algoritmo, por
    cómo funciona, devuelve el valor minimax. Sí: minimax, alfa-beta (en la
    raíz), expectiminimax (el del juego con dado). No: los demás; corte,
    quietud e iterativa con la salvedad de los finales, y los dos que
    convergen (actualización minimax y UCT) con su límite."""
    f = fichas(archivo)
    for alg in gen.ALGORITMOS:
        if alg["archivo"] != archivo:
            continue
        celda = f[alg["nombre"]]["Garantía"]
        assert alg["garantia"] in celda, (alg["nombre"], celda)
        if alg["garantiza"] == "Sí":
            assert alg["numero"].endswith("lo garantiza"), alg["nombre"]
            assert "no garantiza $V$" not in celda, alg["nombre"]
        else:
            assert "no garantiza $V$" in alg["numero"], alg["nombre"]
            assert "salvo si" not in alg["numero"] or "finales" in celda, alg["nombre"]
            assert "converge" not in alg["numero"] or re.search(
                r"converge|tienden", celda), alg["nombre"]


def test_quien_garantiza_v_es_lo_que_dice_la_convencion():
    garantiza = {a["nombre"]: a["garantiza"] for a in gen.ALGORITMOS}
    assert [n for n, g in garantiza.items() if g == "Sí"] == [
        "Minimax", "Alfa-beta", "Expectiminimax"]
    salvedad = [a["nombre"] for a in gen.ALGORITMOS if "salvo si llega a los finales" in a["numero"]]
    assert salvedad == ["Minimax con corte", "Búsqueda de quietud", "Profundización iterativa"]
    convergen = [a["nombre"] for a in gen.ALGORITMOS if "converge" in a["numero"]]
    assert convergen == ["Monte Carlo con actualización minimax", "MCTS con UCT"]
    assert "converge" in gen.ALGORITMOS[-1]["numero"]


def test_el_orden_es_el_de_la_navegacion_y_cada_enlace_lleva_el_titulo_real():
    """R14 de la homologación: el orden de ALGORITMOS es el de las páginas, y
    «Lo que viene» enlaza a una página que existe con el `title` de su
    frontmatter (no a una URL perdida como `mas-alla-del-horizonte`)."""
    import yaml
    assert [a["nombre"] for a in gen.ALGORITMOS] == [
        "Minimax", "Alfa-beta", "Expectiminimax", "Minimax con corte",
        "Búsqueda de quietud", "Profundización iterativa", "Monte Carlo plano",
        "Monte Carlo con actualización minimax", "MCTS con UCT"]
    assert PAGINAS == sorted(PAGINAS), "las páginas van en el orden de navegación"
    titulos = {}
    for ruta in gen.UNIDAD.rglob("*.md"):
        if any(p.startswith("_") for p in ruta.relative_to(gen.UNIDAD).parts):
            continue
        cabeza = yaml.safe_load(ruta.read_text(encoding="utf-8").split("---")[1])
        titulos[cabeza["id"]] = cabeza["title"]
    for a in gen.ALGORITMOS:
        assert titulos.get(a["enlace"]) == a["titulo"], a["nombre"]
    m = re.search(r"\[\[([^|\]]+)\|([^\]]+)\]\]", gen.SIN_PENDIENTES)
    assert titulos.get(m.group(1)) == m.group(2)


def test_ninguna_celda_usa_la_notacion_retirada():
    """Plan §5.1: $\\bar u$, $\\mu$ y $G/N$ salieron de la unidad."""
    for a in gen.ALGORITMOS:
        todo = " ".join(str(v) for v in a.values())
        for vieja in ("\\bar u", "\\mu", "G/N", "ū", "μ"):
            assert vieja not in todo, (a["nombre"], vieja)


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
