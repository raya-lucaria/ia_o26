"""El notebook de la clase 1 de aprendizaje profundo dice lo mismo que redes.py.

course/10_deep_learning/_assets/01_red_desde_cero.ipynb corre en Colab, sin
el repositorio: no puede importar tools/redes.py, así que trae su propia copia
de cada función. Esta prueba es lo que ata esa copia a la fuente:

- el notebook comiteado es, byte a byte, el que tools/gen_cuaderno_redes.py
  produce hoy (se compara, no se sobrescribe);
- nbformat 4 sin salidas; la primera celda lleva el badge de Colab con la URL
  de su propia ruta en main, y la segunda es «▶ Corre esta celda primero»;
- cada celda «fuente» es un tramo de renglones consecutivos de redes.py, tal
  cual; entre todas cubren cada función y constante de redes.py (salvo las
  de FUERA) una sola vez, y ninguna otra celda las redefine ni importa redes;
- celdas cortas: 79 columnas siempre, 15 renglones (36 en una «fuente»);
- todas las celdas corren con python (exec, matplotlib Agg), y lo que
  imprimen son las cifras de redes.cifras(), sección por sección;
- las tres apuestas cumplen lo que dicen sus respuestas plegadas.
"""
import ast
import contextlib
import io
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pytest

import redes as r

REPO = Path(__file__).resolve().parent.parent
RUTA = "course/10_deep_learning/_assets/01_red_desde_cero.ipynb"
CUADERNO = REPO / RUTA
FUENTE = REPO / "tools" / "redes.py"
URL = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
       "blob/main/" + RUTA)
MAX_LINEAS, FUENTE_MAX, MAX_ANCHO = 15, 36, 79
# Lo de redes.py que el notebook no necesita: el caché y las cifras.
FUERA = {"_historias", "_r", "cifras"}
SECCIONES = ["La red 2–3–2–1", "Hacia adelante",
             "La pérdida de un conjunto y el lagrangeano", "Retropropagación",
             "Un paso de descenso", "Entrenar sin μ y con μ",
             "Apuesta y luego corre"]


@pytest.fixture(scope="module")
def nb():
    return json.loads(CUADERNO.read_text(encoding="utf-8"))


def fuente(celda):
    s = celda["source"]
    return "".join(s) if isinstance(s, list) else s


def tags(celda):
    return celda.get("metadata", {}).get("tags", [])


def celdas(nb, tag=None, tipo="code"):
    return [c for c in nb["cells"] if c["cell_type"] == tipo
            and (tag is None or tag in tags(c))]


def nombres_definidos(texto):
    """Los nombres que un bloque define en su primer nivel."""
    res = []
    for nodo in ast.parse(texto).body:
        if isinstance(nodo, ast.FunctionDef):
            res.append(nodo.name)
        elif isinstance(nodo, ast.Assign):
            res += [t.id for t in nodo.targets if isinstance(t, ast.Name)]
    return res


# ------------------------------------------------------------- la forma ---

def test_el_cuaderno_es_el_que_produce_el_generador():
    import gen_cuaderno_redes as gen
    assert CUADERNO.read_text(encoding="utf-8") == gen.contenido(), (
        "el notebook no es el que produce el generador: corre "
        "python3 tools/gen_cuaderno_redes.py y revisa el diff")


def test_es_nbformat_4_sin_salidas(nb):
    assert nb["nbformat"] == 4
    assert nb["metadata"]["kernelspec"]["name"] == "python3"
    for c in nb["cells"]:
        assert c["cell_type"] in ("markdown", "code")
        if c["cell_type"] == "code":
            assert c["outputs"] == [], fuente(c)[:60]
            assert c["execution_count"] is None, fuente(c)[:60]


def test_la_primera_celda_abre_este_cuaderno_en_colab(nb):
    primera = nb["cells"][0]
    assert primera["cell_type"] == "markdown"
    assert "colab-badge.svg" in fuente(primera)
    assert f"]({URL})" in fuente(primera)
    assert "# Notebook 1 · Una red desde cero" in fuente(primera)


def test_la_segunda_celda_se_corre_primero(nb):
    arranque = nb["cells"][1]
    assert arranque["cell_type"] == "code"
    assert "arranque" in tags(arranque)
    assert arranque["metadata"].get("cellView") == "form"
    assert fuente(arranque).startswith("#@title ▶ Corre esta celda primero")
    assert celdas(nb, "arranque") == [arranque]


def test_cada_celda_de_codigo_es_corta(nb):
    for c in celdas(nb):
        lineas = fuente(c).split("\n")
        for renglon in lineas:
            assert len(renglon) <= MAX_ANCHO, renglon
        if "arranque" in tags(c):
            continue
        tope = FUENTE_MAX if "fuente" in tags(c) else MAX_LINEAS
        assert len(lineas) <= tope, (len(lineas), lineas[0])


def test_las_secciones_van_en_orden(nb):
    titulos = [re.match(r"## (\d+) · (.*)", fuente(c)).groups()
               for c in celdas(nb, tipo="markdown")
               if re.match(r"## \d+ · ", fuente(c))]
    assert [int(n) for n, _ in titulos] == list(range(1, len(SECCIONES) + 1))
    assert [t for _, t in titulos] == SECCIONES


def test_cada_apuesta_tiene_su_respuesta_plegada(nb):
    cs = nb["cells"]
    apuestas = [k for k, c in enumerate(cs) if c["cell_type"] == "markdown"
                and re.match(r"\*\*Apuesta \d · ", fuente(c))]
    assert len(apuestas) == 3
    for k in apuestas:
        corre, respuesta = cs[k + 1], cs[k + 2]
        assert corre["cell_type"] == "code" and "apuesta" in tags(corre)
        assert fuente(respuesta).startswith(
            "<details><summary>Respuesta</summary>")


# ------------------------------------------------- la copia literal ---

def test_cada_celda_fuente_es_un_tramo_literal_de_redes(nb):
    renglones = FUENTE.read_text(encoding="utf-8").split("\n")
    for c in celdas(nb, "fuente"):
        mios = fuente(c).split("\n")
        inicios = [k for k in range(len(renglones) - len(mios) + 1)
                   if renglones[k:k + len(mios)] == mios]
        assert inicios, ("la celda no es copia literal de redes.py; corre "
                         "python3 tools/gen_cuaderno_redes.py", mios[0])


def test_toda_definicion_de_redes_va_embebida_una_sola_vez(nb):
    de_redes = set(nombres_definidos(FUENTE.read_text(encoding="utf-8")))
    embebidos = [n for c in celdas(nb, "fuente")
                 for n in nombres_definidos(fuente(c))]
    assert len(embebidos) == len(set(embebidos)), embebidos
    assert set(embebidos) == de_redes - FUERA, (
        sorted(de_redes - FUERA - set(embebidos)),
        sorted(set(embebidos) - de_redes))


def test_ninguna_otra_celda_redefine_ni_importa_redes(nb):
    de_redes = set(nombres_definidos(FUENTE.read_text(encoding="utf-8")))
    for c in celdas(nb):
        texto = fuente(c)
        assert not re.search(r"^\s*(import|from)\s+redes\b", texto, re.M)
        if "fuente" not in tags(c):
            assert not set(nombres_definidos(texto)) & de_redes, texto[:60]


# ------------------------------------------------ correr de punta a punta ---

@pytest.fixture(scope="module")
def corrida(nb):
    """Corre todas las celdas en orden. Devuelve el espacio de nombres y lo
    que imprimió cada sección (0 = antes de la sección 1)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # La celda inicial del notebook fija plt.style y rcParams (fondo claro,
    # rejilla con alfa 0.3). Eso es estado global del proceso: sin restaurarlo,
    # test_gen_aprendizaje_maquina falla ("opacity" en su SVG) solo cuando
    # corre despues de este archivo, y pasa si corre solo.
    rc_antes = matplotlib.rcParams.copy()
    espacio = {"__name__": "cuaderno"}
    salidas, seccion = {0: ""}, 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)    # plt.show() en Agg
        warnings.simplefilter("error", RuntimeWarning)  # nada de overflow
        for k, c in enumerate(nb["cells"]):
            m = re.match(r"## (\d+) · ", fuente(c))
            if c["cell_type"] == "markdown" and m:
                seccion = int(m.group(1))
                salidas[seccion] = ""
            if c["cell_type"] != "code":
                continue
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(fuente(c), f"<celda {k}>", "exec"), espacio)
            salidas[seccion] += buf.getvalue()
    figuras = [plt.figure(n) for n in plt.get_fignums()]
    yield espacio, salidas, figuras
    plt.close("all")
    matplotlib.rcParams.update(rc_antes)


@pytest.fixture(scope="module")
def c():
    return r.cifras()


def fmt(v):
    """El formato del notebook (su fmt), escrito aquí aparte."""
    v = np.round(np.asarray(v, dtype=float), 3) + 0.0
    if v.ndim == 0:
        return f"{v:.3f}"
    return "[" + ", ".join(f"{t:.3f}" for t in v) + "]"


def filas(M):
    """Los renglones que imprime mostrar() para la matriz M."""
    return [f"i = {i + 1}  " + "".join(f"{t:8.3f}" for t in
                                       np.round(np.asarray(fila), 3) + 0.0)
            for i, fila in enumerate(M)]


def test_el_fmt_del_cuaderno_es_el_de_la_prueba(corrida):
    ns, _, _ = corrida
    for v in (0.5465, -0.0001, [0.2, -0.2, 0.6], [-1e-9, 2.0]):
        assert ns["fmt"](v) == fmt(v)


def test_el_ejemplo_del_cuaderno_es_el_de_redes(corrida):
    ns, _, _ = corrida
    red, x, y = r.ejemplo()
    z, a, y_gorro = r.adelante(red, x)
    delta, grad_W, grad_b = r.atras(red, x, y)
    for l in range(1, 4):
        assert np.array_equal(ns["red"]["W"][l], red["W"][l])
        assert np.array_equal(ns["red"]["b"][l], red["b"][l])
        assert np.allclose(ns["z"][l], z[l]) and np.allclose(ns["a"][l], a[l])
        assert np.allclose(ns["delta"][l], delta[l])
        assert np.allclose(ns["grad_W"][l], grad_W[l])
        assert np.allclose(ns["grad_b"][l], grad_b[l])
        assert np.allclose(ns["grad_W_num"][l], grad_W[l], atol=1e-8)
    assert ns["error"] == r.comprobar_gradiente(red, x, y) < 1e-6
    assert ns["error_mu"] == r.comprobar_gradiente(red, x, y, r.MU_EJEMPLO)
    assert ns["sin_mu"] == r._historias()[0]
    assert ns["con_mu"] == r._historias()[1]


def test_seccion_1_imprime_la_red(corrida):
    _, s, _ = corrida
    red, _, _ = r.ejemplo()
    assert "anchos d_0, ..., d_L: [2, 3, 2, 1]   L = 3" in s[1]
    for l in range(1, 4):
        d_l, d_ant = red["W"][l].shape
        assert (f"W^({l}): {d_l} × {d_ant}  (filas = destino i, "
                "columnas = origen j)") in s[1]
        for renglon in filas(red["W"][l]):
            assert renglon in s[1], renglon
        assert f"b^({l}) = {fmt(red['b'][l])}" in s[1]
    assert "total de parámetros en θ: 20" in s[1]


def test_seccion_2_imprime_el_pase_hacia_adelante(corrida, c):
    _, s, _ = corrida
    assert f"a^(0) = x = {fmt(c['x'])}" in s[2]
    for l in (1, 2, 3):
        assert (f"capa {l}: z^({l}) = {fmt(c[f'z{l}'])}  →  "
                f"a^({l}) = {fmt(c[f'a{l}'])}") in s[2]
    assert f"ŷ = {fmt(c['y_gorro'])}   y = {fmt(c['y'][0])}" in s[2]
    assert f"ℓ(ŷ, y) = (ŷ − y)² = {fmt(c['perdida'])}" in s[2]


def test_seccion_3_imprime_omega_y_el_lagrangeano(corrida, c):
    _, s, _ = corrida
    red, x, y = r.ejemplo()
    assert f"Ω(θ) = Σ_l ‖W^(l)‖² = {fmt(c['omega'])}" in s[3]
    assert f"L(θ) con la única observación = {fmt(c['perdida'])}" in s[3]
    assert f"RMSE = √L = {fmt(r.rmse(red, x, y))}" in s[3]
    lag = r.lagrangeano(red, x, y, r.MU_EJEMPLO)
    assert f"𝓛(θ, μ = {r.MU_EJEMPLO}) = {fmt(lag)}" in s[3]


def test_seccion_4_imprime_deltas_y_gradientes(corrida, c):
    _, s, _ = corrida
    for l in (1, 2, 3):
        assert f"δ^({l}) = {fmt(c[f'delta{l}'])}" in s[4]
        assert f"∇_{{b^({l})}} ℓ = δ^({l}) = {fmt(c[f'grad_b{l}'])}" in s[4]
        for renglon in filas(c[f"grad_W{l}"]):
            assert renglon in s[4], (l, renglon)
    assert f"∂ℓ/∂w^(1)_12      = {fmt(c['grad_W1'][0][1])}" in s[4]
    assert "¿coinciden? True" in s[4]


def test_seccion_5_imprime_el_paso(corrida, c):
    _, s, _ = corrida
    assert f"η = {c['eta']}\n" in s[5]
    assert (f"después: ŷ = {fmt(c['y_gorro_tras_paso'])}   "
            f"ℓ = {fmt(c['perdida_tras_paso'])}   "
            f"Ω = {fmt(c['omega_tras_paso'])}") in s[5]
    assert f"con μ = {c['mu']}: " in s[5]
    assert (f"ℓ = {fmt(c['perdida_tras_paso_mu'])}   "
            f"Ω = {fmt(c['omega_tras_paso_mu'])}") in s[5]
    red, x, y = r.ejemplo()
    for t in range(6):
        assert f"paso {t}: ℓ = {fmt(r.perdida(r.adelante(red, x)[2], y))}" \
            in s[5]
        red = r.paso(red, x, y, r.ETA_EJEMPLO)


def test_seccion_6_imprime_el_entrenamiento(corrida, c):
    _, s, _ = corrida
    for nombre, clave in (("sin μ", "sin_mu"),
                          (f"μ = {c['mu_entrenamiento']}", "con_mu")):
        assert (f"{nombre}: RMSE final ent. = "
                f"{fmt(c[f'rmse_entrenamiento_final_{clave}'])}, "
                f"val. = {fmt(c[f'rmse_validacion_final_{clave}'])}; "
                f"mejor val. = {fmt(c[f'rmse_validacion_min_{clave}'])} "
                f"en la época {c[f'epoca_validacion_min_{clave}']}") in s[6]


def test_la_grafica_es_clara_y_en_espanol(corrida):
    _, _, figuras = corrida
    assert len(figuras) == 1
    fig = figuras[0]
    assert fig.get_facecolor()[:3] == (1.0, 1.0, 1.0)
    ejes = fig.get_axes()
    assert [e.get_title() for e in ejes] == [
        "Sin μ", f"Con μ = {r.MU_ENTRENAMIENTO}"]
    for e in ejes:
        assert e.get_xlabel() == "época" and e.get_ylabel() == "RMSE"
        assert e.get_facecolor()[:3] == (1.0, 1.0, 1.0)
        assert len(e.get_lines()[0].get_ydata()) == r.EPOCAS + 1
        etiquetas = [t.get_text() for t in e.get_legend().get_texts()]
        assert etiquetas == ["entrenamiento", "validación", "ruido"]


# ---------------------------------------------------------- las apuestas ---

def test_apuesta_eta_se_descompone_como_dice_la_respuesta(corrida):
    ns, s, _ = corrida
    import gen_cuaderno_redes as gen
    X, Y, X_val, Y_val = r.datos_ejemplo()
    red, h = r.entrenar(
        r.red_inicial(r.ANCHOS_ENTRENAMIENTO, r.ACTIVACIONES_ENTRENAMIENTO),
        X, Y, X_val, Y_val, gen.ETA_APUESTA, 0.0, gen.EPOCAS_APUESTA_ETA,
        r.LOTE)
    assert ns["h_eta"] == h
    ent = h["rmse_entrenamiento"]
    assert ent[1] > 1000                         # «salta a más de mil»
    _, a, y_gorro = r.adelante(red, X)
    assert not a[1].any() and not a[2].any()     # las ocultas, apagadas
    assert np.ptp(y_gorro) == 0                  # la misma ŷ para todo
    assert abs(ent[-1] - Y.std()) < 1e-3         # RMSE ≈ desviación de y
    assert f"η = {gen.ETA_APUESTA} → {fmt(ent[1])}" in s[7]
    assert f"desviación estándar de y: {fmt(Y.std())}" in s[7]


def test_apuesta_mu_sube_las_dos(corrida):
    ns, _, _ = corrida
    grande, chica = ns["h_mu"], ns["con_mu"]
    for clave in ("rmse_entrenamiento", "rmse_validacion"):
        assert grande[clave][-1] > chica[clave][-1], clave


def test_apuesta_ancho_achica_la_distancia(corrida):
    ns, _, _ = corrida
    angosta, ancha = ns["h_ancho"], ns["sin_mu"]

    def distancia(h):
        return h["rmse_validacion"][-1] - h["rmse_entrenamiento"][-1]
    assert distancia(angosta) < distancia(ancha)
    assert angosta["rmse_entrenamiento"][-1] > ancha["rmse_entrenamiento"][-1]
    assert angosta["rmse_validacion"][-1] < ancha["rmse_validacion"][-1]
