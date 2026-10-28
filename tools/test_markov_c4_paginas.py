"""Las paginas de la clase 4 de Markov (course/8_markov/4_lo_que_no_se_ve/)
contra tools/markov.py: el Python de cada pagina corre e imprime lo que dice,
el modelo oculto es UN diccionario, y cada cifra clave esta en SU seccion.

Cierra dos defectos de la clase 3. (1) La guarda de cifras buscaba en la
pagina entera: una cifra correcta en otra seccion tapaba una erronea en la
que la cita. Aqui cada cifra se busca en el texto de su `## N · …` o de
«Lo que hay que llevarse», y su valor se recalcula con markov.py. (2) El
Python de las paginas no se ejecutaba: aqui corre cada bloque en orden, en un
espacio de nombres por pagina, y se compara con su ```text.

Ademas: los pares (trayectoria, probabilidad) de Viterbi frente al mejor por
dia van juntos y no cruzados (el plan los escribio cruzados), una prueba de
mutaciones demuestra que estas guardas fallan con cinco errores plausibles,
los ids `mkv-c4-` son unicos en todo course/, y no aparecen las letras que el
brief prohibe.

Las paginas que aun son esqueleto («Esqueleto:» o un hueco ⟦…⟧) se omiten.
"""
import ast
import re
from fractions import Fraction as F
from pathlib import Path

import pytest

import markov as m

RAIZ = Path(__file__).resolve().parent.parent
CURSO = RAIZ / "course"
CLASE = CURSO / "8_markov/4_lo_que_no_se_ve"

P1, P2 = "1_bayes_y_normalizar.md", "2_el_modelo_oculto.md"
P3, P4 = "3_filtrar.md", "4_decodificar.md"
P5, P6 = "5_aprender_lo_oculto.md", "6_lenguaje_pequeno.md"
P7, P8 = "7_decidir_sin_ver.md", "8_hacia_refuerzo.md"
PAGINAS = [P1, P2, P3, P4, P5, P6, P7, P8]
LLEVARSE = "Lo que hay que llevarse"

LL, SOL = "lluvia", "sol"
C, N = "paraguas", "sin paraguas"
DET, SUS, VER = "determinante", "sustantivo", "verbo"
CALOR, FRIO = "calor", "frío"
UNO, TRES = "un helado", "tres helados"


# ------------------------------------------------------- acceso a markov ---
# El calculista aun agrega funciones: si una falta, la prueba se omite en
# lugar de romper la coleccion.

def _f(nombre):
    fn = getattr(m, nombre, None)
    if fn is None:
        pytest.skip(f"markov.{nombre} aun no existe")
    return fn


def _H(mu0=None):
    h = _f("paraguas")()
    if mu0 is not None:
        h = dict(h, mu0={LL: F(mu0[0]), SOL: F(mu0[1])})
    return h


def _fil(obs, hmm=None):
    return _f("filtrar")(hmm or _H(), obs)


def _vero(obs, hmm=None):
    return _f("verosimilitud_hmm")(hmm or _H(), obs)


def _con(tr, obs, hmm=None):
    return _f("probabilidad_conjunta")(hmm or _H(), list(tr), obs)


def _suav(obs, hmm=None):
    return _f("suavizar")(hmm or _H(), obs)


def _vit(obs, hmm=None):
    return _f("viterbi")(hmm or _H(), obs)


def _post(tr, obs, hmm=None):
    return _f("posterior_trayectoria")(hmm or _H(), list(tr), obs)


def _semana():
    return _f("simular_hmm")(_H(), 6, m.SEMILLAS["c4-simular-semana"])


def _corr(prior, señal):
    return _f("corregir")(_H(), {LL: F(prior[0]), SOL: F(prior[1])}, señal)


def _L():
    return _f("lenguaje_pequeno")()


def _L_mod():
    """El ejercicio final de la pagina 6: un verbo ya puede seguir a otro."""
    h = _L()
    return dict(h, P=dict(h["P"], **{VER: {DET: F(9, 20), SUS: F(9, 20), VER: F(1, 10)}}))


def _helado():
    return _f("helado_eisner")()


def _paso_em():
    nuevo, _ = _f("paso_em")(_H(), [[C, N]])
    return nuevo


def _par():
    return _f("parametros_lenguaje")()


def _costo(b, a):
    return _f("costos_dia")(F(b))[a]


# ------------------------------------------------------------- limpiador ---

def _limpio(s):
    """El de la clase 3, mas \\tfrac12 / \\tfrac9{11} (un digito sin llaves)."""
    s = s.replace("\u2212", "-").replace("\u2060", "")
    s = re.sub(r"\\[tdc]?frac\s*(\{[^{}]*\}|\d)\s*(\{[^{}]*\}|\d)",
               lambda g: g.group(1).strip("{}") + "/" + g.group(2).strip("{}"), s)
    for fino in ("\u202f", "\u2009", "\u00a0", "\\,", "\\;", "\\ ", "~"):
        s = s.replace(fino, " ")
    s = re.sub(r"\\(?:text|textbf|mathrm|mathbf|operatorname)\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\times", "×").replace("**", "").replace("$", "").replace("`", "")
    return re.sub(r"\s+", " ", s)


def _esta(cifra, texto):
    return re.search(r"(?<![\d./])" + re.escape(cifra) + r"(?![\d/]|\.\d)", texto) is not None


def _texto(nombre):
    return (CLASE / nombre).read_text(encoding="utf-8")


def _es_esqueleto(nombre):
    ruta = CLASE / nombre
    if not ruta.is_file():
        return True
    texto = ruta.read_text(encoding="utf-8")
    return "Esqueleto:" in texto or "⟦" in texto


def _saltar_si_esqueleto(nombre):
    if _es_esqueleto(nombre):
        pytest.skip(f"{nombre} aun es esqueleto o tiene huecos ⟦…⟧")


def seccion(texto, titulo):
    """El texto bajo el `## ` que empieza por `titulo`, hasta el siguiente `## `."""
    g = re.search(r"^## " + re.escape(titulo) + r".*?$\n(.*?)(?=^## |\Z)", texto, re.M | re.S)
    return g.group(1) if g else None


# ================================== 1. el Python de cada pagina corre ===

RE_BLOQUE = re.compile(r"^```python\n(.*?)^```\n(?:\n```text\n(.*?)^```)?", re.S | re.M)
MODULOS_PERMITIDOS = {"fractions", "random", "itertools", "math"}


def _bloques(nombre):
    return RE_BLOQUE.findall(_texto(nombre))


def _esperado(codigo, texto):
    """La salida que promete la pagina: el ```text que sigue al codigo o, si
    no hay, los renglones `# …` pegados al margen."""
    if texto:
        return texto.rstrip("\n").splitlines()
    return [l[2:] for l in codigo.splitlines() if l.startswith("# ")]


def _correr(nombre, capsys):
    """Corre los bloques en orden en un solo espacio de nombres; devuelve
    (ns, [(codigo, esperado, salida)])."""
    ns = {"__name__": "pagina"}
    salidas = []
    for codigo, texto in _bloques(nombre):
        exec(compile(codigo, nombre, "exec"), ns)
        salida = capsys.readouterr().out.rstrip("\n").splitlines()
        salidas.append((codigo, _esperado(codigo, texto), salida))
    return ns, salidas


PAGINAS_CON_CODIGO = [p for p in PAGINAS if p != P8]


@pytest.mark.parametrize("pagina", PAGINAS_CON_CODIGO)
def test_el_python_de_la_pagina_imprime_lo_que_dice(pagina, capsys):
    _saltar_si_esqueleto(pagina)
    assert _bloques(pagina), f"{pagina}: no tiene ningun bloque ```python"
    _, salidas = _correr(pagina, capsys)
    for i, (codigo, esperado, salida) in enumerate(salidas, 1):
        primera = codigo.strip().splitlines()[0]
        assert salida == esperado, (
            f"{pagina}, bloque {i} («{primera}»): imprime {salida}, la pagina dice {esperado}")


@pytest.mark.parametrize("pagina", PAGINAS_CON_CODIGO)
def test_el_python_de_la_pagina_solo_importa_la_biblioteca_estandar(pagina):
    _saltar_si_esqueleto(pagina)
    for codigo, _ in _bloques(pagina):
        for nodo in ast.walk(ast.parse(codigo)):
            if isinstance(nodo, ast.Import):
                raices = [a.name.split(".")[0] for a in nodo.names]
            elif isinstance(nodo, ast.ImportFrom):
                raices = [(nodo.module or "").split(".")[0]]
            else:
                continue
            fuera = set(raices) - MODULOS_PERMITIDOS
            assert not fuera, f"{pagina}: importa {fuera} (solo {sorted(MODULOS_PERMITIDOS)})"


# ================================================= 2. un solo diccionario ===

@pytest.mark.parametrize("pagina", PAGINAS_CON_CODIGO)
def test_el_paraguas_y_el_lenguaje_son_el_mismo_diccionario(pagina, capsys):
    _saltar_si_esqueleto(pagina)
    ns, _ = _correr(pagina, capsys)
    if "paraguas" in ns and isinstance(ns["paraguas"], dict):
        assert ns["paraguas"] == _H(), f"{pagina}: `paraguas` no es markov.paraguas()"
    if "lenguaje" in ns and isinstance(ns["lenguaje"], dict):
        assert ns["lenguaje"] == _L(), f"{pagina}: `lenguaje` no es markov.lenguaje_pequeno()"
    if "costo" in ns and isinstance(ns["costo"], dict):     # pagina 7
        for (s, a), v in ns["costo"].items():
            esperado = _f("costos_dia")(1 if s == LL else 0)[a]
            assert v == esperado, f"{pagina}: costo({s}, {a}) = {v}, markov dice {esperado}"
        assert ns["PRECIO"] == m.COSTO_MIRAR, pagina


def test_las_paginas_que_definen_el_paraguas_son_las_esperadas(capsys):
    """Que la prueba de arriba no pase en vacio: el paraguas se arma en la 2
    y se copia en la 3, 4 y 5; el lenguaje en la 6; los costos en la 7."""
    esperado = {P2: "paraguas", P3: "paraguas", P4: "paraguas", P5: "paraguas",
                P6: "lenguaje", P7: "costo"}
    for pagina, nombre in esperado.items():
        if _es_esqueleto(pagina):
            continue
        ns, _ = _correr(pagina, capsys)
        assert nombre in ns, f"{pagina}: ya no define `{nombre}`"


def _sorteo_impreso(pagina):
    """Los renglones `t estado señal` del bloque que llama a simular(…)."""
    for codigo, texto in _bloques(pagina):
        if "simular(" in codigo and texto:
            filas = [l.split(None, 2) for l in texto.strip().splitlines()]
            return [f[1] for f in filas], [f[2] for f in filas]
    raise AssertionError(f"{pagina}: no hay bloque que simule")


def test_la_semana_simulada_de_la_pagina_2_es_la_de_markov():
    _saltar_si_esqueleto(P2)
    assert _sorteo_impreso(P2) == tuple(_semana())


def test_la_frase_generada_de_la_pagina_6_es_la_de_markov():
    _saltar_si_esqueleto(P6)
    tray, obs = _f("simular_hmm")(_L(), 7, m.SEMILLAS["c4-generar-frase"])
    assert _sorteo_impreso(P6) == (tray, obs)


# =========================================== 3. cifras ancladas por seccion ===
# {pagina: {seccion: [(como la escribe la pagina, valor segun markov.py)]}}.
# Una fraccion o entero se compara exacto; un decimal, redondeado a sus cifras.

CIFRAS = {
    P1: {
        "1 · Invertir": [
            ("9/11", lambda: _corr((F(1, 2), F(1, 2)), C)[LL]),
            ("11/20", lambda: _vero([C])),
            ("9/20", lambda: _con([LL], [C])),
            ("1/9", lambda: _corr((F(1, 2), F(1, 2)), N)[LL]),
        ],
        "2 · Normalizar": [
            ("9/11", lambda: _corr((F(1, 2), F(1, 2)), C)[LL]),
            ("2/11", lambda: _corr((F(1, 2), F(1, 2)), C)[SOL]),
            ("27/29", lambda: _corr((F(3, 4), F(1, 4)), C)[LL]),
            ("0.931", lambda: _corr((F(3, 4), F(1, 4)), C)[LL]),
            ("1/3", lambda: _corr((F(1, 10), F(9, 10)), C)[LL]),
        ],
        LLEVARSE: [
            ("9/11", lambda: _corr((F(1, 2), F(1, 2)), C)[LL]),
            ("11/20", lambda: _vero([C])),
            ("27/29", lambda: _corr((F(3, 4), F(1, 4)), C)[LL]),
        ],
    },
    P2: {
        "3 · Calcular": [
            ("1701/25000", lambda: _con([LL, LL, SOL], [C, C, N])),
            ("24089/200000", lambda: _vero([C, C, N])),
            ("27/250", lambda: _con([SOL, LL], [N, C])),
        ],
        "4 · Revisar": [
            ("46211/70300", lambda: _f("no_markov_paraguas")()[0]),
            ("24089/39700", lambda: _f("no_markov_paraguas")()[1]),
            ("0.657", lambda: _f("no_markov_paraguas")()[0]),
            ("0.607", lambda: _f("no_markov_paraguas")()[1]),
        ],
        "5 · Hacerle": [
            ("24089/200000", lambda: _vero([C, C, N])),
        ],
        "Ejercicios": [
            ("8/125", lambda: _con([CALOR, FRIO], [TRES, UNO], _helado())),
            ("24/625", lambda: _con([CALOR, CALOR], [TRES, UNO], _helado())),
            ("547/5000", lambda: _vero([TRES, UNO], _helado())),
        ],
        LLEVARSE: [
            ("1701/25000", lambda: _con([LL, LL, SOL], [C, C, N])),
            ("24089/200000", lambda: _vero([C, C, N])),
            ("46211/70300", lambda: _f("no_markov_paraguas")()[0]),
            ("24089/39700", lambda: _f("no_markov_paraguas")()[1]),
        ],
    },
    P3: {
        "1 · Plantear": [
            ("9/11", lambda: _fil([C])[0][LL]),
            ("69/110", lambda: _f("predecir_estado")(_H(), _fil([C])[0])[LL]),
            ("0.194", lambda: _fil(_semana()[1])[6][LL]),
        ],
        "2 · Avanzar": [
            ("9/11", lambda: _fil([C])[0][LL]),
            ("69/110", lambda: _f("predecir_estado")(_H(), _fil([C])[0])[LL]),
            ("41/110", lambda: _f("predecir_estado")(_H(), _fil([C])[0])[SOL]),
            ("621/703", lambda: _fil([C, C])[1][LL]),
            ("703/1100", lambda: _vero([C, C]) / _vero([C])),
            ("69/397", lambda: _fil([C, N])[1][LL]),
        ],
        "3 · Calcular": [
            ("9/11", lambda: _fil([C, C, N])[0][LL]),
            ("621/703", lambda: _fil([C, C, N])[1][LL]),
            ("4593/24089", lambda: _fil([C, C, N])[2][LL]),
            ("24089/70300", lambda: _vero([C, C, N]) / _vero([C, C])),
            ("4593/7030", lambda: _f("predecir_estado")(_H(), _fil([C, C])[1])[LL]),
        ],
        "4 · Predecir": [
            ("703/1100", lambda: _f("predecir_señal")(_H(), _fil([C])[0])[C]),
            ("397/1100", lambda: _f("predecir_señal")(_H(), _fil([C])[0])[N]),
            ("24089/200000", lambda: _vero([C, C, N])),
            ("397/2000", lambda: _vero([N, C])),
        ],
        "5 · Comparar": [
            ("21/23", lambda: _fil([C, C], _H((1, 0)))[1][LL]),
            ("27/41", lambda: _fil([C, C], _H((0, 1)))[1][LL]),
            ("0.868", lambda: _fil([C, C, N, C, C], _H((1, 0)))[4][LL]),
            ("0.864", lambda: _fil([C, C, N, C, C], _H((0, 1)))[4][LL]),
            ("0.867", lambda: _fil([C, C, N, C, C])[4][LL]),
        ],
        "Ejercicios": [
            ("243/364", lambda: _fil([C, C], _f("hmm_tres_estados")())[1][LL]),
            ("91/300", lambda: _vero([C, C], _f("hmm_tres_estados")())),
        ],
        LLEVARSE: [
            ("9/11", lambda: _fil([C])[0][LL]),
            ("69/110", lambda: _f("predecir_estado")(_H(), _fil([C])[0])[LL]),
            ("621/703", lambda: _fil([C, C])[1][LL]),
            ("0.191", lambda: _fil([C, C, N])[2][LL]),
            ("703/1100", lambda: _f("predecir_señal")(_H(), _fil([C])[0])[C]),
            ("397/1100", lambda: _f("predecir_señal")(_H(), _fil([C])[0])[N]),
            ("24089/200000", lambda: _vero([C, C, N])),
            ("0.194", lambda: _fil(_semana()[1])[6][LL]),
        ],
    },
    P4: {
        "1 · Plantear": [
            ("98/3125", lambda: _vit([N, C, N])[1]),
            ("81/3125", lambda: _con([SOL, LL, SOL], [N, C, N])),
            ("189/25000", lambda: _con([LL, LL, SOL], [N, C, N])),
        ],
        "2 · Suavizar": [
            ("2307/15611", lambda: _suav([N, C, N])[0][LL]),
            ("8649/15611", lambda: _suav([N, C, N])[1][LL]),
            ("15611/200000", lambda: _vero([N, C, N])),
            ("279/397", lambda: _fil([N, C])[1][LL]),
            ("0.852", lambda: _suav([N, C, N])[0][SOL]),
        ],
        "3 · Decodificar": [
            ("98/3125", lambda: _vit([N, C, N])[1]),
            ("27/250", lambda: _vit([N, C])[1]),
            ("7/125", lambda: _con([SOL, SOL], [N, C])),
            ("189/25000", lambda: _con([LL, LL, SOL], [N, C, N])),
            ("567/2000", lambda: _vit([C, C])[1]),
        ],
        "4 · Comparar": [
            ("6272/15611", lambda: _vit([N, C, N])[1] / _vero([N, C, N])),
            ("5184/15611", lambda: _post(_f("mejor_por_dia")(_H(), [N, C, N]), [N, C, N])),
            ("169344/704647", lambda: _vit([N, C, N, C])[1] / _vero([N, C, N, C])),
            ("139968/704647",
             lambda: _post(_f("mejor_por_dia")(_H(), [N, C, N, C]), [N, C, N, C])),
            ("23147208/68607401",
             lambda: _vit([C, C, N, C, C])[1] / _vero([C, C, N, C, C])),
            ("8649/15611", lambda: _suav([N, C, N])[1][LL]),
        ],
        "Ejercicios": [
            ("8/625", lambda: _vit([TRES, UNO, TRES], _helado())[1]),
            ("905/14281", lambda: _suav([TRES, UNO, TRES], _helado())[0][FRIO]),
            ("8625/14281", lambda: _suav([TRES, UNO, TRES], _helado())[1][FRIO]),
            ("2533/14281", lambda: _suav([TRES, UNO, TRES], _helado())[2][FRIO]),
        ],
        LLEVARSE: [
            ("2307/15611", lambda: _suav([N, C, N])[0][LL]),
            ("8649/15611", lambda: _suav([N, C, N])[1][LL]),
            ("6272/15611", lambda: _vit([N, C, N])[1] / _vero([N, C, N])),
            ("392/12500", lambda: _vit([N, C, N])[1]),
            ("5184/15611", lambda: _post(_f("mejor_por_dia")(_H(), [N, C, N]), [N, C, N])),
            ("169344/704647", lambda: _vit([N, C, N, C])[1] / _vero([N, C, N, C])),
            ("139968/704647",
             lambda: _post(_f("mejor_por_dia")(_H(), [N, C, N, C]), [N, C, N, C])),
        ],
    },
    P5: {
        "1 · Contar": [
            ("4/5", lambda: _f("contar_con_etiquetas")([LL, SOL], [C, N], *_semana())[1][LL][C]),
            ("1/5", lambda: _f("contar_con_etiquetas")([LL, SOL], [C, N], *_semana())[1][LL][N]),
            ("1/2", lambda: _f("contar_con_etiquetas")([LL, SOL], [C, N], *_semana())[0][SOL][SOL]),
            ("2/3", lambda: _f("contar_con_etiquetas")(
                [LL, SOL], [C, N], [LL, LL, SOL, SOL, SOL, LL], [C, C, N, C, N, C])[0][SOL][SOL]),
        ],
        "2 · Aprender": [
            ("397/2000", lambda: _vero([C, N])),
            ("279/397", lambda: _suav([C, N])[0][LL]),
            ("69/397", lambda: _suav([C, N])[1][LL]),
            ("7/31", lambda: _paso_em()["P"][LL][LL]),
            ("24/31", lambda: _paso_em()["P"][LL][SOL]),
            ("3/59", lambda: _paso_em()["P"][SOL][LL]),
            ("93/116", lambda: _paso_em()["B"][LL][C]),
            ("59/223", lambda: _paso_em()["B"][SOL][C]),
            ("268802881/669153424", lambda: _vero([C, N], _paso_em())),
        ],
        LLEVARSE: [
            ("279/397", lambda: _suav([C, N])[0][LL]),
            ("7/31", lambda: _paso_em()["P"][LL][LL]),
            ("24/31", lambda: _paso_em()["P"][LL][SOL]),
            ("397/2000", lambda: _vero([C, N])),
            ("0.402", lambda: _vero([C, N], _paso_em())),
            ("4/5", lambda: _f("contar_con_etiquetas")([LL, SOL], [C, N], *_semana())[1][LL][C]),
        ],
    },
    P6: {
        "2 · Generar": [
            ("3/32768", lambda: _con([DET, SUS, VER, DET, SUS],
                                     ["mi", "luna", "come", "la", "casa"], _L())),
        ],
        "3 · Predecir": [
            ("3/16", lambda: _f("predecir_señal")(_L(), _fil(["la", "gata"], _L())[-1])["come"]),
            ("2/5", lambda: _fil(["casa", "casa"], _L())[-1][SUS]),
            ("3/5", lambda: _fil(["casa", "casa"], _L())[-1][VER]),
            ("1/512", lambda: _con([VER, DET, SUS], ["casa", "la", "sopa"], _L())),
            ("2/3", lambda: _post([VER, DET, SUS], ["casa", "la", "sopa"], _L())),
        ],
        "4 · Encontrar": [
            ("3/2048", lambda: _vit(["casa"] * 3, _L())[1]),
        ],
        "5 · Contar": [
            ("45", lambda: _par()["celdas_hmm"]),
            ("39", lambda: _par()["libres_hmm"]),
            ("144", lambda: _par()["celdas_bigramas"]),
            ("132", lambda: _par()["libres_bigramas"]),
            ("48", lambda: _par()["celdas_hmm_con_inicial"]),
            ("41", lambda: _par()["libres_hmm_con_inicial"]),
            ("156", lambda: _par()["celdas_bigramas_con_inicial"]),
            ("143", lambda: _par()["libres_bigramas_con_inicial"]),
            ("35", lambda: _par()["libres_hmm_con_ceros"]),
        ],
        "Ejercicios": [
            ("1/640", lambda: _vero(["come", "ve"], _L_mod())),
            ("161/51200", lambda: _vero(["casa"] * 3, _L_mod())),
            ("27/20480", lambda: _vit(["casa"] * 3, _L_mod())[1]),
            ("135/322", lambda: _vit(["casa"] * 3, _L_mod())[1] / _vero(["casa"] * 3, _L_mod())),
            ("3/10240", lambda: _con(_f("mejor_por_dia")(_L_mod(), ["casa"] * 3),
                                     ["casa"] * 3, _L_mod())),
            ("15/161", lambda: _post(_f("mejor_por_dia")(_L_mod(), ["casa"] * 3),
                                     ["casa"] * 3, _L_mod())),
        ],
        LLEVARSE: [
            ("2046", lambda: m.SEMILLAS["c4-generar-frase"]),
            ("3/16", lambda: _f("predecir_señal")(_L(), _fil(["la", "gata"], _L())[-1])["come"]),
            ("3/5", lambda: _fil(["casa", "casa"], _L())[-1][VER]),
            ("2/3", lambda: _post([VER, DET, SUS], ["casa", "la", "sopa"], _L())),
            ("3/2048", lambda: _vit(["casa"] * 3, _L())[1]),
            ("45", lambda: _par()["celdas_hmm"]),
            ("39", lambda: _par()["libres_hmm"]),
            ("144", lambda: _par()["celdas_bigramas"]),
            ("132", lambda: _par()["libres_bigramas"]),
            ("48", lambda: _par()["celdas_hmm_con_inicial"]),
            ("41", lambda: _par()["libres_hmm_con_inicial"]),
            ("156", lambda: _par()["celdas_bigramas_con_inicial"]),
            ("143", lambda: _par()["libres_bigramas_con_inicial"]),
            ("35", lambda: _par()["libres_hmm_con_ceros"]),
        ],
    },
    P7: {
        "1 · Repasar": [
            ("2", lambda: _costo(F(1, 2), "no llevar")),
            ("1/2", lambda: _f("valor_informacion")(F(1, 2))),
            ("4/3", lambda: _costo(F(1, 3), "no llevar")),
            ("2/3", lambda: _f("valor_informacion")(F(1, 3))),
        ],
        "3 · Decidir": [
            ("1/4", lambda: _f("umbral_paraguas")()),
            ("9/11", lambda: _fil([C])[0][LL]),
            ("36/11", lambda: _costo(F(9, 11), "no llevar")),
            ("4/9", lambda: _costo(F(1, 9), "no llevar")),
            ("69/397", lambda: _fil([C, N])[1][LL]),
            ("276/397", lambda: _costo(F(69, 397), "no llevar")),
        ],
        "4 · Pagar": [
            ("1/6", lambda: _f("rango_mirar")()[0]),
            ("1/2", lambda: _f("rango_mirar")()[1]),
            ("2/3", lambda: _f("costo_mirar")(F(1, 6))),
            ("3/4", lambda: _f("costo_mirar")(F(1, 4))),
            ("29/22", lambda: _f("costo_mirar")(F(9, 11))),
            ("535/794", lambda: _f("costo_mirar")(F(69, 397))),
            ("11/18", lambda: _f("costo_mirar")(F(1, 9))),
            ("5/6", lambda: _f("costo_mirar")(F(1, 3))),
            ("7/10", lambda: _f("costo_mirar")(F(1, 5))),
            ("3/5", lambda: _f("valor_informacion")(F(1, 5))),
        ],
        "5 · Tomar": [
            ("621/703", lambda: _fil([C, C])[1][LL]),
            ("31/503", lambda: _fil([N, N])[1][LL]),
            ("279/397", lambda: _fil([N, C])[1][LL]),
        ],
        LLEVARSE: [
            ("1/4", lambda: _f("umbral_paraguas")()),
            ("1/6", lambda: _f("rango_mirar")()[0]),
            ("1/2", lambda: _f("rango_mirar")()[1]),
            ("2/3", lambda: _f("costo_mirar")(F(1, 6))),
            ("3/4", lambda: _f("costo_mirar")(F(1, 4))),
            ("9/11", lambda: _fil([C])[0][LL]),
        ],
    },
    P8: {
        "2 · Separar": [
            ("9/11", lambda: _fil([C])[0][LL]),
            ("621/703", lambda: _fil([C, C])[1][LL]),
            ("1/6", lambda: _f("rango_mirar")()[0]),
            ("1/2", lambda: _f("rango_mirar")()[1]),
        ],
        "3 · Elegir": [
            ("-5", lambda: m.evaluar_politica(m.pasillo(), m.POLITICAS_J2["caminar–correr"])[1]),
            ("-2", lambda: m.evaluar_politica(m.pasillo(), m.POLITICAS_J2["caminar–correr"])[2]),
        ],
        LLEVARSE: [
            ("9/11", lambda: _fil([C])[0][LL]),
            ("621/703", lambda: _fil([C, C])[1][LL]),
            ("1/6", lambda: _f("rango_mirar")()[0]),
            ("1/2", lambda: _f("rango_mirar")()[1]),
        ],
    },
}

CASOS_CIFRA = [(p, s, c) for p, secs in CIFRAS.items() for s, lista in secs.items()
               for c, _ in lista]


def _vale(texto, valor):
    """¿El numero escrito `texto` es el `valor` que calcula markov.py?"""
    if "." in texto:
        decimales = len(texto.split(".")[1])
        return f"{float(valor):.{decimales}f}" == texto
    return F(texto) == F(valor)


@pytest.mark.parametrize("pagina,sec,cifra", CASOS_CIFRA,
                         ids=[f"{p[:2]}{s[:3]}{c}" for p, s, c in CASOS_CIFRA])
def test_cada_cifra_es_la_que_calcula_markov(pagina, sec, cifra):
    fn = dict(CIFRAS[pagina][sec])[cifra]
    valor = fn()
    assert _vale(cifra, valor), f"{pagina} «{sec}»: escribe {cifra}, markov da {valor}"


def _fallas_cifras(pagina, texto):
    """[(seccion, cifra)] que faltan en SU seccion (o la seccion falta)."""
    fallas = []
    for sec, lista in CIFRAS[pagina].items():
        cuerpo = seccion(texto, sec)
        if cuerpo is None:
            fallas.append((sec, "<falta la seccion>"))
            continue
        cuerpo = _limpio(cuerpo)
        fallas += [(sec, c) for c, _ in lista if not _esta(c, cuerpo)]
    return fallas


@pytest.mark.parametrize("pagina", PAGINAS)
def test_cada_cifra_esta_en_su_seccion(pagina):
    _saltar_si_esqueleto(pagina)
    fallas = _fallas_cifras(pagina, _texto(pagina))
    assert not fallas, f"{pagina}: faltan {fallas}"


def test_el_limpiador_lee_los_formatos():
    assert _esta("9/11", _limpio(r"$\frac{9}{11}$"))
    assert _esta("1/2", _limpio(r"$\tfrac12$"))
    assert _esta("9/11", _limpio(r"$\tfrac9{11}$"))
    assert _esta("-5", _limpio("$\u22125$"))
    assert not _esta("1/2", _limpio("11/20")) and not _esta("1/2", _limpio("1/20"))
    assert not _esta("0.4", _limpio("0.4018"))


# Frases-ancla: condiciones que no se pueden perder al reescribir.
FRASES_ANCLA = {
    P2: {"4 · Revisar": ["no son una cadena de Markov"]},
    P3: {"5 · Comparar": ["solo para el paraguas"],
         LLEVARSE: ["No ocurre en todo modelo"]},
    P4: {"4 · Comparar": ["no garantiza la mejor secuencia"]},
    P6: {"6 · Distinguir": ["no es un modelo oculto de Markov"]},
    P7: {"4 · Pagar": ["Mirar conviene estrictamente"],
         "5 · Tomar": ["no garantiza una solución única"]},
}


def _fallas_frases(pagina, texto):
    fallas = []
    for sec, frases in FRASES_ANCLA.get(pagina, {}).items():
        cuerpo = _limpio(seccion(texto, sec) or "")
        fallas += [(sec, f) for f in frases if f not in cuerpo]
    return fallas


@pytest.mark.parametrize("pagina", sorted(FRASES_ANCLA))
def test_las_condiciones_siguen_escritas(pagina):
    _saltar_si_esqueleto(pagina)
    fallas = _fallas_frases(pagina, _texto(pagina))
    assert not fallas, f"{pagina}: falta {fallas}"


# ============================ 4. pares trayectoria–probabilidad, sin cruzar ===
# Cada probabilidad rastreada debe tener, como trayectoria mas cercana ANTES
# de ella en su renglon y frase, la suya. Si hay otra trayectoria pegada, el
# par esta cruzado; si no hay ninguna, no se juzga (la cifra va sola).

ESTADOS_NOMBRE = "sol|lluvia|determinante|sustantivo|verbo"
RE_TRAY = re.compile(rf"(?:{ESTADOS_NOMBRE})(?:, (?:{ESTADOS_NOMBRE}))+")


def _unidades(texto):
    for renglon in texto.splitlines():
        yield from re.split(r"(?<=[.;])\s+", _limpio(renglon))


def _pares():
    """[(trayectoria, probabilidad)] como se escriben: de markov.py."""
    t3, t4 = [N, C, N], [N, C, N, C]
    md = _f("mejor_por_dia")
    pares = []
    for obs in (t3, t4):
        v, conj = _vit(obs)
        pares.append((v, conj / _vero(obs)))
        d = md(_H(), obs)
        pares.append((d, _post(d, obs)))
    v3 = _vit(t3)[0]
    pares.append((v3, _con(v3, t3)))
    pares.append(([SOL, LL, SOL], _con([SOL, LL, SOL], t3)))
    vl, pl = _vit(["casa"] * 3, _L())
    pares.append((vl, pl))
    return [(", ".join(t), f"{p.numerator}/{p.denominator}") for t, p in pares]


def _fallas_pares(texto, pares, requeridos=()):
    """Cruces en `texto` y pares requeridos que nunca aparecen juntos."""
    fallas, vistos = [], set()
    for u in _unidades(texto):
        trays = [(g.end(), g.group(0)) for g in RE_TRAY.finditer(u)]
        for tray, prob in pares:
            for g in re.finditer(r"(?<![\d./])" + re.escape(prob) + r"(?![\d/]|\.\d)", u):
                antes = [t for fin, t in trays if fin <= g.start()]
                if not antes:
                    continue
                if antes[-1] == tray:
                    vistos.add((tray, prob))
                else:
                    fallas.append(f"cruzado: «{antes[-1]}» junto a {prob} (es de «{tray}»): {u}")
    fallas += [f"falta el par «{t}» con {p}" for t, p in requeridos if (t, p) not in vistos]
    return fallas


def _requeridos(pares, cuales):
    return [pares[i] for i in cuales]


# Indices de _pares(): 0 Viterbi-3, 1 por dia-3, 2 Viterbi-4, 3 por dia-4,
# 4 conjunta sol-sol-sol, 5 conjunta sol-lluvia-sol, 6 lenguaje Viterbi.
PARES_REQUERIDOS = {
    (P4, "1 · Plantear"): [4, 5],
    (P4, "4 · Comparar"): [0, 1, 2, 3],
    (P4, LLEVARSE): [0, 1],
    (P6, "4 · Encontrar"): [6],
    (P6, LLEVARSE): [6],
}


def test_los_pares_de_markov_son_los_del_brief():
    """El plan los cruzo; el brief §3b y test_markov_c4 los fijan asi."""
    pares = _pares()
    assert pares[:4] == [("sol, sol, sol", "6272/15611"), ("sol, lluvia, sol", "5184/15611"),
                         ("sol, sol, sol, lluvia", "169344/704647"),
                         ("sol, lluvia, sol, lluvia", "139968/704647")]
    assert pares[6] == ("sustantivo, verbo, sustantivo", "3/2048")


@pytest.mark.parametrize("pagina,sec", sorted(PARES_REQUERIDOS))
def test_cada_trayectoria_va_con_su_probabilidad(pagina, sec):
    _saltar_si_esqueleto(pagina)
    pares = _pares()
    cuerpo = seccion(_texto(pagina), sec)
    assert cuerpo is not None, f"{pagina}: falta «{sec}»"
    fallas = _fallas_pares(cuerpo, pares, _requeridos(pares, PARES_REQUERIDOS[(pagina, sec)]))
    assert not fallas, f"{pagina} «{sec}»:\n" + "\n".join(fallas)


@pytest.mark.parametrize("pagina", [P4, P6])
def test_ningun_par_esta_cruzado_en_toda_la_pagina(pagina):
    _saltar_si_esqueleto(pagina)
    fallas = _fallas_pares(_texto(pagina), _pares())
    assert not fallas, f"{pagina}:\n" + "\n".join(fallas)


# ================================================== 5. mutaciones ===
# Cada mutacion cambia, en memoria, una sola seccion de una pagina real; la
# cifra cambiada sigue apareciendo en otras secciones, asi que una guarda por
# pagina entera pasaria. Las guardas de arriba tienen que fallar.

def _mutar_seccion(texto, sec, viejo, nuevo):
    cuerpo = seccion(texto, sec)
    assert cuerpo is not None and viejo in cuerpo, (sec, viejo)
    return texto.replace(cuerpo, cuerpo.replace(viejo, nuevo))


def _todas_las_fallas(pagina, texto):
    fallas = _fallas_cifras(pagina, texto) + _fallas_frases(pagina, texto)
    pares = _pares()
    for (p, sec), cuales in PARES_REQUERIDOS.items():
        if p == pagina:
            cuerpo = seccion(texto, sec) or ""
            fallas += _fallas_pares(cuerpo, pares, _requeridos(pares, cuales))
    return fallas


MUTACIONES = [
    # una cifra clave cambia solo en «Lo que hay que llevarse»
    ("cifra-621-703", P3, LLEVARSE, "621/703", "621/702"),
    # el par del contraste, cruzado en la tabla
    ("par-cruzado-tabla", P4, "4 · Comparar",
     "sol, sol, sol: 6272/15611", "sol, sol, sol: 5184/15611"),
    # el par cruzado en el resumen
    ("par-cruzado-llevarse", P4, LLEVARSE,
     "Viterbi da sol, sol, sol con", "Viterbi da sol, lluvia, sol con"),
    # el umbral 1/4 cambia por 1/3 en su seccion
    ("umbral-1-3", P7, "3 · Decidir", "1/4", "1/3"),
    # 45 celdas por 54
    ("celdas-54", P6, "5 · Contar", "=45", "=54"),
    # se borra la condicion «solo para el paraguas»
    ("sin-condicion", P3, "5 · Comparar", "solo para el paraguas", "en general"),
]


@pytest.mark.parametrize("nombre,pagina,sec,viejo,nuevo", MUTACIONES,
                         ids=[x[0] for x in MUTACIONES])
def test_las_guardas_atrapan_la_mutacion(nombre, pagina, sec, viejo, nuevo):
    _saltar_si_esqueleto(pagina)
    texto = _texto(pagina)
    assert not _todas_las_fallas(pagina, texto), f"{pagina} ya falla sin mutar"
    mutado = _mutar_seccion(texto, sec, viejo, nuevo)
    assert mutado != texto
    assert _todas_las_fallas(pagina, mutado), f"{nombre}: la mutacion pasa en silencio"


# ======================================================= 6. ids y objetos ===

RE_DIRECTIVA = re.compile(r"^::: (\w+) \{([^}]*)\}\s*$", re.M)
RE_ID = re.compile(r"\{#([\w-]+)")
RE_ATRIBUTO = re.compile(r'(\w+)="([^"]*)"')


def _ids_definidos(texto):
    return RE_ID.findall(texto)


def test_los_ids_mkv_c4_son_unicos_en_todo_el_curso():
    cuenta = {}
    for md in CURSO.rglob("*.md"):
        for i in _ids_definidos(md.read_text(encoding="utf-8")):
            cuenta.setdefault(i, []).append(md.relative_to(CURSO).as_posix())
    propios = [i for p in PAGINAS if not _es_esqueleto(p)
               for i in _ids_definidos(_texto(p))]
    assert propios, "las paginas no definen ningun id"
    repetidos = {i: cuenta[i] for i in propios if len(cuenta[i]) > 1}
    assert not repetidos, repetidos
    sin_prefijo = [i for i in propios if not i.startswith("mkv-c4-")]
    assert not sin_prefijo, f"ids sin prefijo mkv-c4-: {sin_prefijo}"


@pytest.mark.parametrize("pagina", PAGINAS)
def test_las_figuras_llevan_el_prefijo_de_figura(pagina):
    _saltar_si_esqueleto(pagina)
    for fam, attrs in RE_DIRECTIVA.findall(_texto(pagina)):
        if fam == "figure":
            i = RE_ID.search("{" + attrs).group(1)
            assert i.startswith("mkv-c4-fig-"), f"{pagina}: figura {i}"


@pytest.mark.parametrize("pagina", PAGINAS)
def test_cada_ejercicio_tiene_pistas_y_una_respuesta_contiguas(pagina):
    """test_markov_estructura mide solo el ejercicio final de «## Ejercicios»;
    esta mide tambien los micro de cada seccion: tras el ejercicio, una o
    mas pistas y una sola respuesta, todas con `of=` del ejercicio."""
    _saltar_si_esqueleto(pagina)
    objetos = []
    for fam, attrs in RE_DIRECTIVA.findall(_texto(pagina)):
        if fam in {"exercise", "hint", "answer"}:
            a = dict(RE_ATRIBUTO.findall(attrs))
            a["id"] = RE_ID.search("{" + attrs).group(1)
            objetos.append((fam, a))
    for i, (fam, a) in enumerate(objetos):
        if fam != "exercise":
            continue
        j = i + 1
        while j < len(objetos) and objetos[j][0] == "hint":
            j += 1
        pistas = objetos[i + 1:j]
        assert pistas, f"{pagina}: {a['id']} sin pista"
        assert j < len(objetos) and objetos[j][0] == "answer", f"{pagina}: {a['id']} sin respuesta"
        assert j + 1 == len(objetos) or objetos[j + 1][0] == "exercise", (
            f"{pagina}: {a['id']} tiene mas de una respuesta")
        for _, b in pistas + [objetos[j]]:
            assert b.get("of") == a["id"], f"{pagina}: {b['id']} no es de {a['id']}"


def test_cada_cita_mkv_c4_apunta_a_un_id_de_la_clase():
    definidos = {i for p in CLASE.glob("*.md") for i in _ids_definidos(p.read_text(encoding="utf-8"))}
    for p in PAGINAS:
        if _es_esqueleto(p):
            continue
        citas = set(re.findall(r"@(mkv-c4-[\w-]*\w)", _texto(p)))
        assert citas <= definidos, f"{p}: cita ids que no existen: {citas - definidos}"


# ================================================== 7. letras prohibidas ===
# Brief §3: π no es la distribucion inicial (es la politica), \boldsymbol
# rompe el sitio, y los estados y señales van en palabras, no R/S/U/N.

PROHIBIDAS = [
    (r"\\pi_\{?0\b|π₀|π_0", "π como distribución inicial: se escribe μ₀"),
    (r"\\boldsymbol", "\\boldsymbol rompe el render: \\mathbf"),
    (r"\\text\{[RSUN]\}", "estado o señal con letra suelta"),
    (r"\b[BP]\(\s*[RSUN]\s*[,)]", "B(R, …) o P(S) con letra de estado"),
    (r"\\mid\s*[RSUN]\s*\)", "condicional sobre una letra de estado"),
    (r"P\(\s*u\s*\\mid", "P(u|R): la emisión es B(s,o)"),
]


@pytest.mark.parametrize("pagina", sorted(p.name for p in CLASE.glob("*.md")))
def test_no_hay_letras_prohibidas(pagina):
    texto = _texto(pagina)
    hallazgos = [(motivo, g.group(0), texto.count("\n", 0, g.start()) + 1)
                 for patron, motivo in PROHIBIDAS for g in re.finditer(patron, texto)]
    assert not hallazgos, f"{pagina}: {hallazgos}"


def test_las_letras_prohibidas_se_detectan():
    muestras = [r"$\pi_0=(1/2,1/2)$", r"$\boldsymbol{b}$", r"$\text{R}$",
                r"$B(R,u)$", r"$\Pr(O\mid R)$", r"$P(u\mid R)$"]
    for s in muestras:
        assert any(re.search(p, s) for p, _ in PROHIBIDAS), s
    legales = [r"$\Pr(O=o\mid S=s)$", r"$\pi(s)$", r"$P(s'\mid s)$", r"$B(s,o)$", r"$S_t$"]
    for s in legales:
        assert not any(re.search(p, s) for p, _ in PROHIBIDAS), s
