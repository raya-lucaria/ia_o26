"""Pruebas de ml_lab (tools/aprendizaje_maquina.py), unidad 9.

Lo que fijan, en el orden del contrato común (§5):

1. La superficie pública es la de tools/datos/ml_lab_superficie.json para la
   VERSION cargada (§5.2, D-004), con su prueba de mutación, las claves de
   los catálogos, la firma común de las dibujar_* y la regla de requiere().
2. La copia _assets/ml_lab.py es byte-idéntica y las cifras importan la fuente.
3. La semántica numérica de ajustar (§5.7): el problema que minimiza, el
   intercepto sin penalizar, los pesos w_y = n/(K n_y), las conversiones a
   sklearn y las condiciones KKT.
4. Evaluar sin pesos (§5.8), realidad contra despliegue, el piso con lo
   visible, la reproducibilidad por semilla y los adelantos que lanzan.
5. Las Phi, los casos borde de 1.0, las gráficas y la interactividad sin
   ipywidgets.
6. Lo que trae 1.1 (O0b-c1, contrato §5.15 B): repetir, error_por_zona,
   no_free_lunch y sus dos gráficas, el adelanto proceso_clasificacion con la
   prueba de adelantos de §5.2, PROCESOS["recursivo"] y los casos 3, 4 y 5.
7. Lo que trae 1.2 (lote de la clase 2) y 1.3 (lote de la clase 3, clase_3.md
   §10.7.2): piezas de cola larga y heterocedastico con su piso, interacciones,
   estandarizar, mae/rmse/r2, peores_errores, trayectorias, optimo_restringido,
   encoger_1d, beta_repetido, muchas_variables, los casos 6–12 y 24, sus
   gráficas (dibujar_cv y dibujar_diana idénticas a 1.2 sin los argumentos
   nuevos) y el taller de la clase 3.

Corre en menos de un minuto con el venv de S-lab.
"""
import inspect
import io
import json
import os
import re
import subprocess
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

import aprendizaje_maquina as ml  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SUPERFICIE = RAIZ / "tools/datos/ml_lab_superficie.json"
COPIA = RAIZ / "course/9_aprendizaje_maquina/_assets/ml_lab.py"


@pytest.fixture(autouse=True)
def _cerrar_figuras():
    yield
    plt.close("all")


def _sin_avisos(funcion, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        return funcion(*args, **kwargs)


# ---------------------------------------------------------------------------
# 1 · Superficie pública (§5.2, D-004)
# ---------------------------------------------------------------------------


def _entradas():
    return json.loads(SUPERFICIE.read_text(encoding="utf-8"))


def _x_y(version):
    x, y = version.split(".")
    return int(x), int(y)


def _parametros(firma):
    """Parte "(a, b=1, *, c=None, **d)" en parámetros (tipo, nombre, valor por omisión
    como texto o None), respetando paréntesis, comillas y los <function …> del JSON."""
    cuerpo = firma.strip()
    assert cuerpo.startswith("(") and cuerpo.endswith(")"), firma
    cuerpo = cuerpo[1:-1]
    trozos, actual, nivel, comilla = [], "", 0, None
    for ch in cuerpo:
        if comilla:
            actual += ch
            if ch == comilla:
                comilla = None
            continue
        if ch in "'\"":
            comilla = ch
        elif ch in "([{<":
            nivel += 1
        elif ch in ")]}>":
            nivel -= 1
        elif ch == "," and nivel == 0:
            trozos.append(actual.strip())
            actual = ""
            continue
        actual += ch
    if actual.strip():
        trozos.append(actual.strip())
    salida, solo_nombre = [], False
    for t in trozos:
        if t == "*":
            solo_nombre = True
            continue
        if t.startswith("**"):
            salida.append(("**", t[2:], None))
            continue
        if t.startswith("*"):
            salida.append(("*", t[1:], None))
            solo_nombre = True
            continue
        nombre, _, defecto = t.partition("=")
        salida.append(("nombre" if solo_nombre else "posicion", nombre.strip(),
                       defecto.strip() if _ else None))
    return salida


def _firma_compatible(vieja, nueva, nombre):
    """§5.2: la firma nueva conserva cada parámetro viejo (mismo orden posicional,
    mismo nombre, mismo valor por omisión) y solo agrega parámetros con valor por
    omisión: al final de los posicionales, o solo por nombre."""
    v, n = _parametros(vieja), _parametros(nueva)
    pos_v = [p for p in v if p[0] == "posicion"]
    pos_n = [p for p in n if p[0] == "posicion"]
    assert pos_n[:len(pos_v)] == pos_v, f"cambió la firma de {nombre}: {vieja} -> {nueva}"
    otros_n = {p[1]: p for p in n if p[0] != "posicion"}
    for p in v:
        if p[0] != "posicion":
            assert otros_n.get(p[1]) == p, f"cambió {p[1]} en {nombre}: {vieja} -> {nueva}"
    viejos = {p[1] for p in v}
    for p in n:
        if p[1] not in viejos and p[0] in ("posicion", "nombre"):
            assert p[2] is not None, f"{nombre} agregó {p[1]} sin valor por omisión"


def _compatible(vieja, nueva):
    """Cada nombre de la vieja sigue en la nueva con una firma compatible
    parámetro a parámetro (_firma_compatible), métodos incluidos."""
    for nombre, firma in vieja.items():
        if nombre == "__claves__":
            continue
        assert nombre in nueva, f"se quitó {nombre}"
        actual = nueva[nombre]
        if actual == firma:
            continue
        if isinstance(firma, dict) and isinstance(actual, dict):
            for metodo, f in firma.items():
                assert metodo in actual, f"se quitó {nombre}.{metodo}"
                _firma_compatible(f, actual[metodo], f"{nombre}.{metodo}")
            continue
        assert isinstance(firma, str) and isinstance(actual, str), nombre
        assert firma.startswith("(") and actual.startswith("("), f"cambió {nombre}"
        _firma_compatible(firma, actual, nombre)
    for catalogo, claves in vieja.get("__claves__", {}).items():
        faltan = set(map(str, claves)) - set(map(str, nueva["__claves__"][catalogo]))
        assert not faltan, f"{catalogo} perdió {sorted(faltan)}"


def test_la_superficie_publica_es_la_del_contrato():
    entradas = _entradas()
    assert ml.VERSION in entradas, f"falta la entrada {ml.VERSION} en {SUPERFICIE.name}"
    assert ml._superficie() == entradas[ml.VERSION]
    x_actual, y_actual = _x_y(ml.VERSION)
    for version, entrada in entradas.items():
        x, y = _x_y(version)
        if x == x_actual and y < y_actual:
            _compatible(entrada, entradas[ml.VERSION])
    # las entradas ya publicadas en main no cambian
    r = subprocess.run(
        ["git", "-C", str(RAIZ), "show", "main:tools/datos/ml_lab_superficie.json"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        pytest.skip("tools/datos/ml_lab_superficie.json todavía no existe en main")
    en_main = json.loads(r.stdout)
    for version, entrada in en_main.items():
        assert entradas.get(version) == entrada, f"cambió la entrada publicada {version}"


def test_mutacion_de_un_valor_por_omision_rompe_la_superficie(monkeypatch):
    esperado = _entradas()[ml.VERSION]
    original = ml.ajustar.__defaults__
    cambiado = tuple(0.5 if v == 0.0 and not isinstance(v, bool) else v for v in original)
    assert cambiado != original
    monkeypatch.setattr(ml.ajustar, "__defaults__", cambiado)
    assert ml._superficie() != esperado
    monkeypatch.setattr(ml.ajustar, "__defaults__", original)
    assert ml._superficie() == esperado


def test_mutacion_de_una_clave_de_catalogo_rompe_la_superficie(monkeypatch):
    esperado = _entradas()[ml.VERSION]
    procesos = dict(ml.PROCESOS)
    procesos.pop("lluvia")
    monkeypatch.setattr(ml, "PROCESOS", procesos)
    actual = ml._superficie()
    assert actual != esperado
    with pytest.raises(AssertionError):
        _compatible(esperado, actual)


def test_toda_dibujar_termina_en_ax_y_tema():
    nombres = [n for n in ml.__all__ if n.startswith("dibujar_")]
    assert len(nombres) >= 7
    for nombre in nombres:
        params = list(inspect.signature(getattr(ml, nombre)).parameters.values())
        assert [p.name for p in params[-2:]] == ["ax", "tema"], nombre
        assert params[-2].default is None and params[-1].default == "claro", nombre


def test_claves_de_los_catalogos_de_1_0():
    claves_1_0 = _entradas()["1.0"]["__claves__"]
    assert set(claves_1_0["PROCESOS"]) == {
        "entregas", "inverso", "mezcla_logs", "seno", "x1_mas_x2x3", "lluvia",
    }
    assert set(claves_1_0["CASOS_BORDE"]) == {1, 2, 23}
    # 1.1 (O0b-c1) agrega "recursivo" y los casos 3, 4 y 5; 1.2 (clase 2) agrega
    # "entregas_curvas", los casos 13 a 16 y el taller 2; nadie quita nada
    assert set(ml.PROCESOS) == set(claves_1_0["PROCESOS"]) | {"recursivo", "entregas_curvas"}
    assert set(_entradas()["1.2"]["__claves__"]["PROCESOS"]) >= {"entregas_curvas"}
    for prohibida in ("lineal", "ar1", "cola_larga"):
        assert prohibida not in ml.PROCESOS
    # 1.3 (clase 3) agrega los casos 6 a 12 y 24 y el taller 3
    assert set(ml.CASOS_BORDE) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 23, 24}
    assert all(isinstance(k, int) for k in ml.CASOS_BORDE)
    assert set(ml.ANALISIS_TALLER) == {1, 2, 3}
    assert ml.SENTIDO == {
        "cuadratica": "min", "absoluta": "min", "logaritmica": "min", "aciertos": "max",
    }


def test_requiere_misma_x_y_mayor_o_igual():
    ml.requiere("1.0")
    ml.requiere(ml.VERSION)
    with pytest.raises(RuntimeError, match="vuelve a correr la celda de arranque"):
        ml.requiere("1.99")
    with pytest.raises(RuntimeError, match=re.escape(ml.VERSION)):
        ml.requiere("2.0")
    with pytest.raises(RuntimeError):
        ml.requiere("0.9")


def test_version_y_cambios():
    assert ml.VERSION == "1.3"
    assert {"1.0", "1.1", "1.2", "1.3"} <= set(ml.CAMBIOS)
    assert set(_entradas()) == set(ml.CAMBIOS)


def test_copia_en_assets_es_identica():
    if not COPIA.parent.parent.exists():
        pytest.skip("course/9_aprendizaje_maquina/ todavía no existe (U.T1 de integ)")
    assert COPIA.exists() and COPIA.read_bytes() == (RAIZ / "tools/aprendizaje_maquina.py").read_bytes(), (
        "copia tools/aprendizaje_maquina.py a _assets"
    )


def test_las_cifras_importan_la_fuente():
    """Un ml_cifras_c<N>.py o su prueba, si importa ml_lab, lo importa de tools/."""
    archivos = sorted((RAIZ / "tools").glob("ml_cifras_c*.py")) + sorted(
        (RAIZ / "tools").glob("test_ml_cifras_c*.py")
    )
    malos = []
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        if re.search(r"^\s*(import|from)\s+ml_lab\b", texto, re.M) or "_assets/ml_lab" in texto:
            malos.append(archivo.name)
    assert not malos, f"importan la copia de _assets en vez de tools/: {malos}"
    assert Path(ml.__file__).resolve().parent == RAIZ / "tools"


# ---------------------------------------------------------------------------
# 2 · Ajuste: la convención de mu (§5.7)
# ---------------------------------------------------------------------------


def _datos_reg(n=80, q=4, semilla=1, colineal=False):
    rng = np.random.default_rng(semilla)
    X = rng.normal(size=(n, q))
    if colineal:
        X[:, 1] = X[:, 0]
    y = 3 + X @ np.arange(1, q + 1) + rng.normal(size=n)
    df = pd.DataFrame(X, columns=[f"x{j + 1}" for j in range(q)])
    df["y"] = y
    return df, [f"x{j + 1}" for j in range(q)]


def _kkt(Phi, y, w, mu, penalizacion, rho, beta, tarea="regresion"):
    """Máximo residuo de las condiciones KKT de
    (1/n) sum w_i l_i + mu Omega(beta), con el intercepto (columna 0) libre."""
    n = len(y)
    if tarea == "regresion":
        g = -(2.0 / n) * Phi.T @ (w * (y - Phi @ beta))
    else:
        p = 1 / (1 + np.exp(-(Phi @ beta)))
        g = (1.0 / n) * Phi.T @ (w * (p - y))
    r = {"l2": 0.0, "l1": 1.0, "elastica": rho}.get(penalizacion, 0.0)
    if penalizacion is None:
        mu = 0.0
    g = g.copy()
    g[1:] += 2 * mu * (1 - r) * beta[1:]
    peor = abs(g[0])
    for j in range(1, len(beta)):
        if abs(beta[j]) > 1e-12:
            peor = max(peor, abs(g[j] + mu * r * np.sign(beta[j])))
        else:
            peor = max(peor, max(0.0, abs(g[j]) - mu * r))
    return peor


@pytest.mark.parametrize("penalizacion", ["l2", "l1", "elastica"])
@pytest.mark.parametrize("mu", [0.01, 0.3, 2.0])
def test_kkt_regresion(penalizacion, mu):
    df, cols = _datos_reg()
    df.attrs["ml"] = {"columnas_x": cols, "columnas_contexto": [], "tarea": "regresion",
                      "K": None, "clases": None}
    m = ml.ajustar(df, mu=mu, penalizacion=penalizacion, rho=0.3)
    Phi = m.Phi(df).to_numpy()
    assert list(m.Phi(df).columns)[0] == "1"
    assert _kkt(Phi, df["y"].to_numpy(), np.ones(len(df)), mu, penalizacion, 0.3,
                m.beta_gorro.to_numpy()) < 1e-6


def test_el_intercepto_no_se_penaliza():
    df, cols = _datos_reg()
    df["y"] += 1000.0
    m = ml.ajustar(df, mu=1e6, penalizacion="l2", columnas_x=cols, tarea="regresion")
    pendientes = m.beta_gorro.drop("1")
    assert np.all(np.abs(pendientes) < 1e-3)
    assert m.beta_gorro["1"] == pytest.approx(df["y"].mean(), abs=1e-3)


@pytest.mark.parametrize("penalizacion", ["l2", "l1", "elastica"])
def test_kkt_regresion_con_pesos(penalizacion):
    """Los pesos solo entran por el ajuste (adelanto de la clase 4): se prueba el
    resolvedor común que usará ajustar(pesos=...)."""
    df, cols = _datos_reg(n=60)
    rng = np.random.default_rng(5)
    w = rng.uniform(0.2, 3.0, size=len(df))
    Phi = np.column_stack([np.ones(len(df)), df[cols].to_numpy()])
    y = df["y"].to_numpy()
    beta = ml._resolver(Phi, y, w, 0.5, penalizacion, 0.4, "regresion", True)
    assert _kkt(Phi, y, w, 0.5, penalizacion, 0.4, beta) < 1e-6


def test_pesos_balanceados_son_n_sobre_K_por_n_y():
    y = np.array([0] * 90 + [1] * 10)
    w = ml._pesos_balanceados(y, clases=[0, 1])
    assert w == {0: pytest.approx(100 / (2 * 90)), 1: pytest.approx(100 / (2 * 10))}
    assert sum(w[v] for v in y) == pytest.approx(len(y))


def test_ajustar_con_pesos_lanza_hasta_la_clase_4():
    datos = ml.anillos()
    for pesos in ("balanceado", {0: 1.0, 1: 2.0}):
        with pytest.raises(NotImplementedError, match="clase 4"):
            ml.ajustar(datos, tarea="clasificacion", pesos=pesos)


def test_conversiones_a_sklearn():
    from sklearn.linear_model import ElasticNet, Lasso, LogisticRegression

    df, cols = _datos_reg(n=120, q=3)
    X, y = df[cols].to_numpy(), df["y"].to_numpy()
    for mu in (0.05, 0.8):
        m = ml.ajustar(df, mu=mu, penalizacion="l1", columnas_x=cols, tarea="regresion")
        sk = Lasso(alpha=mu / 2, tol=1e-12, max_iter=200_000).fit(X, y)
        assert np.allclose(m.beta_gorro.drop("1"), sk.coef_, atol=1e-5)
        assert m.beta_gorro["1"] == pytest.approx(sk.intercept_, abs=1e-5)
        for rho in (0.25, 0.7):
            m = ml.ajustar(df, mu=mu, penalizacion="elastica", rho=rho, columnas_x=cols,
                           tarea="regresion")
            sk = ElasticNet(alpha=mu * (2 - rho) / 2, l1_ratio=rho / (2 - rho), tol=1e-12,
                            max_iter=200_000).fit(X, y)
            assert np.allclose(m.beta_gorro.drop("1"), sk.coef_, atol=1e-5)
    datos = ml.anillos(n=300)
    ent = datos.ent
    X = ent[["x1", "x2"]].to_numpy()
    for mu in (0.0, 0.01, 0.2):
        m = ml.ajustar(datos, mu=mu, penalizacion="l2" if mu else None, tarea="clasificacion")
        n = len(ent)
        if mu:
            sk = LogisticRegression(C=1 / (2 * mu * n), tol=1e-12, max_iter=10_000)
        else:
            sk = LogisticRegression(penalty=None, tol=1e-12, max_iter=10_000)
        sk.fit(X, ent["y"].to_numpy())
        assert np.allclose(m.beta_gorro.drop("1"), sk.coef_.ravel(), atol=1e-4)
        assert m.beta_gorro["1"] == pytest.approx(sk.intercept_[0], abs=1e-4)


@pytest.mark.parametrize("penalizacion,mu", [(None, 0.0), ("l2", 0.05), ("l1", 0.02),
                                             ("elastica", 0.05)])
def test_kkt_logistica(penalizacion, mu):
    datos = ml.anillos(n=300)
    m = ml.ajustar(datos, phi=ml.polares(), mu=mu, penalizacion=penalizacion, rho=0.5,
                   tarea="clasificacion")
    Phi = m.Phi(datos.ent).to_numpy()
    y = datos.ent["y"].to_numpy().astype(float)
    assert _kkt(Phi, y, np.ones(len(y)), mu, penalizacion, 0.5, m.beta_gorro.to_numpy(),
                tarea="clasificacion") < 1e-6


def test_lasso_con_columnas_duplicadas_compara_el_objetivo():
    df, cols = _datos_reg(colineal=True)
    mu = 0.4
    m = ml.ajustar(df, mu=mu, penalizacion="l1", columnas_x=cols, tarea="regresion")
    b = m.beta_gorro.to_numpy().copy()
    Phi = m.Phi(df).to_numpy()
    y = df["y"].to_numpy()

    def objetivo(beta):
        return np.mean((y - Phi @ beta) ** 2) + mu * np.abs(beta[1:]).sum()

    otro = b.copy()
    otro[1] = otro[2] = (b[1] + b[2]) / 2
    assert objetivo(b) == pytest.approx(objetivo(otro), abs=1e-9)
    assert _kkt(Phi, y, np.ones(len(y)), mu, "l1", 1.0, b) < 1e-6


def test_pseudoinversa_con_mas_parametros_que_datos():
    datos = ml.caso(23)
    with pytest.warns(UserWarning, match="pseudoinversa"):
        m = ml.ajustar(datos, phi=ml.polinomio(12))
    Phi = m.Phi(datos.ent).to_numpy()
    assert np.allclose(m.beta_gorro.to_numpy(), np.linalg.pinv(Phi) @ datos.ent["y"].to_numpy(),
                       atol=1e-6)
    assert ml.L(m, datos.ent) < 1e-10
    assert ml.riesgo(m, datos) > 10 * ml.piso(datos)


def test_separacion_se_avisa_y_el_traslape_no():
    separables = ml.anillos(n=200, grosor=0.05, ruido=0.01)
    with pytest.warns(UserWarning, match="se separan perfectamente"):
        ml.ajustar(separables, phi=ml.polares(incluir=("r",)), tarea="clasificacion")
    _sin_avisos(ml.ajustar, ml.anillos(), phi=ml.polares(), tarea="clasificacion")
    _sin_avisos(ml.ajustar, ml.anillos(), tarea="clasificacion")


def test_la_tarea_nunca_se_infiere():
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [0, 1, 0, 1]})
    with pytest.raises(ValueError, match="tarea"):
        ml.ajustar(df, columnas_x=["x"])
    with pytest.raises(ValueError, match="columnas_x"):
        ml.ajustar(df, tarea="regresion")


# ---------------------------------------------------------------------------
# 3 · Evaluar: sin pesos, realidad contra despliegue, piso (§5.8)
# ---------------------------------------------------------------------------


def test_la_evaluacion_no_lee_los_pesos_del_modelo():
    for nombre in ("evaluar", "L"):
        assert inspect.signature(getattr(ml, nombre)).parameters["pesos"].default is None
    assert inspect.signature(ml.Modelo.L).parameters["pesos"].default is None
    datos = ml.anillos(n=300)
    a = ml.ajustar(datos, tarea="clasificacion")
    b = ml.ajustar(datos, tarea="clasificacion")
    b.pesos = {0: 1.0, 1: 9.0}  # como si se hubiera ajustado con pesos
    for modelo in (a, b):
        p = modelo.predecir_p(datos.val)
        a_mano = ml.perdida(datos.val["y"].to_numpy(), p, "logaritmica").mean()
        assert ml.evaluar(modelo, datos.val) == pytest.approx(a_mano)
        assert ml.L(modelo, datos.val) == pytest.approx(a_mano)
    assert ml.evaluar(a, datos.val) == ml.evaluar(b, datos.val)
    # ponderar la evaluación es explícito e igual para los dos
    assert ml.evaluar(a, datos.val, pesos="balanceado") == ml.evaluar(b, datos.val,
                                                                      pesos="balanceado")


def test_riesgo_solo_perdidas_y_desempeno_las_metricas():
    datos = ml.anillos()
    m = ml.ajustar(datos, phi=ml.polares(), tarea="clasificacion")
    with pytest.raises(ValueError, match="desempeno"):
        ml.riesgo(m, datos, "aciertos")
    assert ml.desempeno(m, datos, "aciertos") == pytest.approx(
        ml.aciertos(datos.despliegue["y"].to_numpy(), m.predecir(datos.despliegue)))
    assert ml.desempeno(m, datos, "logaritmica") == pytest.approx(ml.riesgo(m, datos))
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.desempeno(m, datos, "mcc")


def test_realidad_y_despliegue_son_dos_muestras_de_la_misma_poblacion():
    datos = ml.PROCESOS["entregas"](n=40)
    otra = ml.PROCESOS["entregas"](n=40, semilla=7)
    pd.testing.assert_frame_equal(datos.realidad, otra.realidad)
    pd.testing.assert_frame_equal(datos.despliegue, otra.despliegue)
    assert not datos.realidad["y"].equals(datos.despliegue["y"])
    assert not datos.ent.equals(otra.ent)
    m = ml.ajustar(datos)
    r_real, r_desp = ml.riesgo(m, datos, contra="realidad"), ml.riesgo(m, datos)
    assert r_real != r_desp
    assert abs(r_real - r_desp) < 0.05 * r_desp
    for df in (datos.ent, datos.val, datos.prueba):
        assert not set(df.columns) & {"f", "f_visible", "prob"}
    assert {"f", "f_visible"} <= set(datos.realidad.columns)


def test_reproducibilidad_por_semilla():
    a = ml.proceso(n=50, semilla=3)
    b = ml.proceso(n=50, semilla=3)
    for parte in ("ent", "val", "prueba"):
        pd.testing.assert_frame_equal(getattr(a, parte), getattr(b, parte))
    c = ml.proceso(n=50, semilla=3, fracciones=(0.5, 0.25, 0.25))
    juntas = lambda d: pd.concat([d.ent, d.val, d.prueba]).sort_index()  # noqa: E731
    pd.testing.assert_frame_equal(juntas(a), juntas(c))
    assert not ml.proceso(n=50, semilla=4).ent.equals(a.ent)
    m1 = ml.ajustar(a, phi=ml.polinomio(3))
    m2 = ml.ajustar(b, phi=ml.polinomio(3))
    assert m1.beta_gorro.equals(m2.beta_gorro)


def test_fracciones_con_ceros():
    casos = [ml.proceso(n=30, fracciones=(1, 0, 0)),
             ml.anillos(n=400, fracciones=(1, 0, 0)),
             ml.PROCESOS["entregas"](fracciones=(1, 0, 0))]
    casos += [ml.caso(k) for k in (1, 2, 23)]
    for datos in casos:
        n = len(datos.ent) + len(datos.val) + len(datos.prueba)
        assert len(datos.ent) == n
        assert len(datos.val) == 0 and len(datos.prueba) == 0
        assert list(datos.val.columns) == list(datos.ent.columns)
    assert len(ml.anillos(n=400, fracciones=(1, 0, 0)).ent) == 400
    assert len(ml.PROCESOS["entregas"](fracciones=(1, 0, 0)).ent) == 20
    _sin_avisos(ml.proceso, n=30, fracciones=(1, 0, 0))


def test_adelantos_de_proceso_lanzan_con_la_clase_que_los_trae():
    # 1.2: lo de la clase 2 ya funciona; faltantes sigue lanzando y nombra la clase 4
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.proceso(n=20, faltantes={"x": (0.2, "azar")})
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.proceso(n=20, ruido=ml.ar1(), despliegue="futuro", faltantes={"x": (0.2, "azar")})
    # lo que pide una columna que el proceso no tiene es un ValueError que lo dice
    for kwargs, patron in [({"separar": "tiempo"}, "columna t"),
                           ({"separar": "grupo"}, "columna grupo"),
                           ({"despliegue": "futuro"}, "columna t"),
                           ({"despliegue": "grupos_nuevos"}, "columna grupo")]:
        with pytest.raises(ValueError, match=patron):
            ml.proceso(n=20, con_realidad=False, **kwargs)
    with pytest.raises(ValueError, match="deriva"):
        ml.proceso(n=20, deriva=lambda t: {})
    with pytest.raises(ValueError):
        ml.proceso(n=20, separar="otra")
    with pytest.raises(NotImplementedError, match="clase 5"):
        ml.ajustar_otro(ml.proceso(n=20), familia="arbol")


def test_piso_con_variables_visibles():
    lluvia = ml.caso(2)
    assert ml.piso(lluvia) == pytest.approx(10.0, abs=0.05)
    con_x2 = ml.caso("lluvia", omitir=None)
    assert ml.piso(con_x2) == pytest.approx(1.0, abs=1e-9)
    assert ml.piso(ml.proceso(n=20, ruido=ml.normal(0, 2))) == pytest.approx(4.0)
    assert ml.piso(ml.caso(1)) == pytest.approx(0.86, abs=0.01)
    assert ml.piso(ml.proceso(n=20, ruido=ml.normal(0, 2)), "absoluta") == pytest.approx(
        2 * np.sqrt(2 / np.pi))
    assert ml.piso(ml.anillos(), "logaritmica") > 0


def test_piso_endogeno_y_endogeno_con_omitidas():
    sin_omitidas = ml.proceso(n=50, x={"x1": ml.normal()}, f=lambda d: 1 + 2 * d["x1"],
                              endogeno=0.5)
    assert ml.piso(sin_omitidas) == pytest.approx(0.75, abs=1e-9)
    datos = ml.proceso(n=50, x={"x1": ml.normal(), "x2": ml.normal()},
                       f=lambda d: 1 + 2 * d["x1"] + 3 * d["x2"], endogeno=0.4, omitir=["x2"])
    assert ml.piso(datos) == pytest.approx(9.84, abs=0.05)
    malla = pd.DataFrame({"x1": np.linspace(-2, 2, 9)})
    assert np.allclose(datos.f_visible(malla), 1 + 2.4 * malla["x1"], atol=0.05)
    m = ml.ajustar(ml.proceso(n=20_000, x={"x1": ml.normal(), "x2": ml.normal()},
                              f=lambda d: 1 + 2 * d["x1"] + 3 * d["x2"], endogeno=0.4,
                              omitir=["x2"], con_realidad=False))
    assert m.beta_gorro["x1"] == pytest.approx(2.4, abs=0.1)


def test_piso_infinito_y_desconocido():
    class Pesada(ml.Pieza):
        nombre = "pesada"
        media, varianza = 0.0, float("inf")

        def muestrear(self, n, rng):
            return rng.standard_cauchy(n)

    assert ml.piso(ml.proceso(n=20, ruido=Pesada(), n_realidad=1000)) == float("inf")
    raro = ml.proceso(n=20, x={"x1": ml.normal(), "x2": ml.normal()},
                      f=lambda d: d["x1"] * d["x2"], correlacion={("x1", "x2"): 0.5},
                      omitir=["x2"], n_realidad=2000)
    assert raro.f_visible is None
    with pytest.warns(UserWarning, match="piso desconocido"):
        assert np.isnan(ml.piso(raro))


def test_beta_verdadero_del_caso_1():
    datos = ml.caso(1)
    b = ml.beta_verdadero(datos, None)
    assert b["x1"] == pytest.approx(1.0, abs=1e-2)
    assert set(b.attrs["omitidas"]) == {"x2", "x3"}
    assert b.attrs["exacto"] is False
    lineal = ml.proceso(n=30, x={"x1": ml.normal(), "x2": ml.normal()},
                        f=lambda d: 1 + 2 * d["x1"] - d["x2"], omitir=["x2"])
    b = ml.beta_verdadero(lineal, None)
    assert b.attrs["exacto"] is True
    assert b["x1"] == pytest.approx(2.0, abs=1e-9)
    m = ml.ajustar(datos)
    assert m.beta_gorro["x1"] == pytest.approx(1.8, abs=0.2)


def test_escala_cambia_unidades_no_f():
    base = ml.proceso(n=40, x={"x1": ml.normal(), "x2": ml.uniforme()},
                      f=lambda d: d["x1"] + d["x2"])
    km = ml.proceso(n=40, x={"x1": ml.normal(), "x2": ml.uniforme()},
                    f=lambda d: d["x1"] + d["x2"], escala={"x2": 1000})
    assert np.allclose(km.ent["x2"], 1000 * base.ent["x2"])
    assert np.allclose(km.ent["y"], base.ent["y"])
    yy = ml.proceso(n=40, escala={"y": 10})
    assert yy.sigma2_e == pytest.approx(100.0)
    assert np.allclose(yy.ent["y"], 10 * ml.proceso(n=40).ent["y"])


def test_anillos_prob_contra_frecuencia_por_bandas():
    datos = ml.anillos()
    real = datos.realidad
    r = np.hypot(real["x1"], real["x2"])
    bandas = pd.cut(r, np.arange(0.4, 2.8, 0.2))
    tabla = real.assign(banda=bandas).groupby("banda", observed=True).agg(
        p=("prob", "mean"), y=("y", "mean"), n=("y", "size"))
    tabla = tabla[tabla["n"] > 2000]
    assert len(tabla) >= 6
    assert np.max(np.abs(tabla["p"] - tabla["y"])) < 0.02


# ---------------------------------------------------------------------------
# 4 · Representaciones Phi (§5.6)
# ---------------------------------------------------------------------------


def test_solo_radio_desde_datos_frescos():
    codigo = (
        "import sys, warnings; sys.path.insert(0, %r)\n"
        "import numpy as np, io, contextlib\n"
        "import aprendizaje_maquina as ml\n"
        "datos = ml.anillos()\n"
        "antes = list(datos.ent.columns)\n"
        "m = ml.ajustar(datos, phi=ml.polares(incluir=('r',)), tarea='clasificacion')\n"
        "Phi = m.Phi(datos.ent)\n"
        "assert np.max(np.abs(Phi['r'] - np.hypot(datos.ent.x1, datos.ent.x2))) < 1e-12\n"
        "assert list(datos.ent.columns) == antes\n"
        "s = io.StringIO()\n"
        "with contextlib.redirect_stdout(s): ml.imprimir_Phi(m, datos.ent)\n"
        "assert s.getvalue().split('\\n')[0].split()[:2] == ['1', 'r'], s.getvalue()\n"
        "try:\n"
        "    ml.ajustar(datos, phi=ml.columnas('r'), tarea='clasificacion')\n"
        "except ValueError as e:\n"
        "    assert 'polares(incluir=(\"r\",))' in str(e), e\n"
        "else:\n"
        "    raise SystemExit('columnas(r) no lanzó')\n"
        "print('ok')\n"
    ) % str(RAIZ / "tools")
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True,
                       env={**os.environ, "MPLBACKEND": "Agg"})
    assert r.returncode == 0 and r.stdout.strip().endswith("ok"), r.stderr


def test_polares_valida_incluir():
    for malo in ((), ("radio",), ("theta", "r"), ("r", "r")):
        with pytest.raises(ValueError):
            ml.polares(incluir=malo)


def test_imprimir_Phi_pone_la_columna_1_primero():
    datos = ml.anillos(n=200)
    for phi, esperado in [(None, ["1", "x1", "x2"]), (ml.polares(), ["1", "r", "theta"]),
                          (ml.polares(incluir=("r",)), ["1", "r"])]:
        m = ml.ajustar(datos, phi=phi, tarea="clasificacion")
        s = io.StringIO()
        with redirect_stdout(s):
            ml.imprimir_Phi(m, datos.ent)
        assert s.getvalue().split("\n")[0].split() == esperado
        assert "el mismo ajuste lineal" in s.getvalue()
        assert list(m.Phi(datos.ent).columns) == esperado


def _df_con_categoria(semilla=0, n=120):
    rng = np.random.default_rng(semilla)
    g = rng.choice(["a", "b", "c"], size=n)
    x = rng.uniform(0, 1, size=n)
    efecto = pd.Series(g).map({"a": 0.0, "b": 2.0, "c": -1.0}).to_numpy()
    df = pd.DataFrame({"x": x, "g": g, "y": 1 + 3 * x + efecto + rng.normal(0, 0.1, n)})
    df.attrs["ml"] = {"columnas_x": ["x", "g"], "columnas_contexto": [],
                      "tarea": "regresion", "K": None, "clases": None}
    return df


def test_dummies_base_lanza_con_categoria_nueva():
    df = _df_con_categoria()
    m = ml.ajustar(df, phi=ml.combinar(ml.columnas("x"), ml.dummies("g")))
    nuevo = df.head(3).copy()
    nuevo.loc[nuevo.index[0], "g"] = "zeta"
    with pytest.raises(ValueError, match="zeta") as e:
        m.predecir(nuevo)
    assert "efectos" in str(e.value)


def test_dummies_efectos_da_fila_de_ceros_y_aviso():
    df = _df_con_categoria()
    phi = ml.dummies("g", codificacion="efectos").ajustar(df)
    nuevo = pd.DataFrame({"g": ["zeta", "a"]})
    with pytest.warns(UserWarning, match="grupo promedio"):
        M = phi(nuevo)
    assert np.all(M.iloc[0].to_numpy() == 0)
    assert np.all(phi(pd.DataFrame({"g": ["a"]})).to_numpy() == -1)


def test_dummies_efectos_no_depende_del_orden_de_las_categorias():
    df = _df_con_categoria()
    otro = df.iloc[::-1].copy()
    otro.attrs = df.attrs
    phi = lambda: ml.combinar(ml.columnas("x"), ml.dummies("g", codificacion="efectos"))  # noqa: E731
    a = ml.ajustar(df, phi=phi())
    b = ml.ajustar(otro, phi=phi())
    malla = _df_con_categoria(semilla=9)
    assert np.allclose(a.predecir(malla), b.predecir(malla), atol=1e-9)


def test_dummies_sin_quitar_una_deja_phi_sin_rango_completo():
    df = _df_con_categoria()
    with pytest.warns(UserWarning, match="pseudoinversa"):
        m = ml.ajustar(df, phi=ml.dummies("g", quitar_una=False))
    Phi = m.Phi(df).to_numpy()
    assert np.linalg.matrix_rank(Phi) < Phi.shape[1]
    with pytest.raises(ValueError):
        ml.dummies("g", quitar_una=False, codificacion="efectos")


def test_una_phi_lee_contexto_solo_si_lo_nombra():
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"x": rng.uniform(size=60), "t": np.arange(60.0)})
    df["y"] = df["x"] + 0.1 * df["t"]
    df.attrs["ml"] = {"columnas_x": ["x"], "columnas_contexto": ["t"], "tarea": "regresion",
                      "K": None, "clases": None}
    m = ml.ajustar(df)
    assert list(m.Phi(df).columns) == ["1", "x"]
    m = ml.ajustar(df, phi=ml.columnas("x", "t"))
    assert list(m.Phi(df).columns) == ["1", "x", "t"]
    v = ml.ajustar_otro(df, familia="vecinos", n_vecinos=3)
    assert v.columnas_x == ["x"]
    v = ml.ajustar_otro(df, familia="vecinos", columnas_x=["x", "t"], n_vecinos=3)
    assert v.columnas_x == ["x", "t"]
    with pytest.raises(ValueError, match="n_vecino"):
        ml.ajustar_otro(df, familia="vecinos", vecinos=3)


def test_columnas_parser_seguro():
    df = pd.DataFrame({"x1": [1.0, 2.0], "x2": [4.0, 8.0], "x3": [3.0, 5.0]})
    M = ml.columnas("x1", "1/x2", "x1*x3", "log(x1)").ajustar(df)(df)
    assert list(M.columns) == ["x1", "1/x2", "x1*x3", "log(x1)"]
    assert np.allclose(M["1/x2"], [0.25, 0.125])
    with pytest.raises(ValueError):
        ml.columnas("__import__('os')")


def test_polinomio_escala_a_menos_uno_uno():
    datos = ml.PROCESOS["inverso"]()
    phi = ml.polinomio(3).ajustar(datos.ent)
    M = phi(datos.ent)
    assert M.iloc[:, 0].min() == pytest.approx(-1) and M.iloc[:, 0].max() == pytest.approx(1)
    sin = ml.polinomio(3, escalar=False).ajustar(datos.ent)(datos.ent)
    assert np.allclose(sin.iloc[:, 1], datos.ent["x"] ** 2)


def test_taylor_y_periodicas():
    t = ml.taylor("inverso", centro=1.0, N=3)
    assert t(np.array([1.0]))[0] == pytest.approx(7.0)
    s = ml.taylor("seno", centro=0.5, N=9)
    x = np.linspace(0.3, 0.7, 5)
    assert np.allclose(s(x), 4 + 2 * np.sin(5 * x), atol=1e-3)
    M = ml.periodicas("x", periodo=2.0, armonicos=2).ajustar(pd.DataFrame({"x": [0.5]}))(
        pd.DataFrame({"x": [0.5]}))
    assert M.shape == (1, 4)


# ---------------------------------------------------------------------------
# 5 · Métricas, benchmarks, capacidad
# ---------------------------------------------------------------------------


def test_aciertos_y_perdidas():
    from sklearn.metrics import accuracy_score

    rng = np.random.default_rng(0)
    y, yg = rng.integers(0, 2, 50), rng.integers(0, 2, 50)
    assert ml.aciertos(y, yg) == pytest.approx(accuracy_score(y, yg))
    assert np.allclose(ml.perdida([1, 2], [0, 4], "cuadratica"), [1, 4])
    assert np.allclose(ml.perdida([1, 2], [0, 4], "absoluta"), [1, 2])
    assert np.allclose(ml.perdida([1, 0], [0.8, 0.8], "logaritmica"),
                       [-np.log(0.8), -np.log(0.2)])
    assert ml.mse([1, 2], [0, 4]) == pytest.approx(2.5)


def test_benchmarks():
    datos = ml.PROCESOS["entregas"](n=40)
    tabla = ml.benchmarks(datos, datos.val)
    media = datos.ent["y"].mean()
    assert tabla.loc["media", "cuadratica"] == pytest.approx(
        np.mean((datos.val["y"] - media) ** 2))
    assert set(tabla.index) == {"media", "mediana"}
    anillos = ml.anillos()
    t = ml.benchmarks(anillos, anillos.despliegue)
    assert set(t.index) == {"moda", "proporcion"}
    assert list(t.columns) == ["logaritmica", "aciertos"]
    assert t.loc["moda", "aciertos"] == pytest.approx(0.5, abs=0.02)
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.benchmarks(anillos, anillos.val, criterios=["mcc"])


def test_curva_capacidad():
    datos = ml.PROCESOS["inverso"](n=30)
    candidatos = {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N))) for N in (1, 2, 4)}
    tabla = ml.curva_capacidad(datos, candidatos)
    assert list(tabla.columns) == ["candidato", "conjunto", "L", "ee"]
    assert set(tabla["conjunto"]) == {"ent", "realidad"}
    ent = tabla[tabla.conjunto == "ent"].set_index("candidato")["L"]
    assert ent[4] <= ent[2] <= ent[1]
    cv = ml.curva_capacidad(datos, candidatos, conjuntos=("cv",), k=5)
    for N, construir in candidatos.items():
        r = ml.validacion_cruzada(datos, construir, k=5)
        fila = cv[cv.candidato == N].iloc[0]
        assert fila["L"] == pytest.approx(r.media) and fila["ee"] == pytest.approx(r.ee)


# ---------------------------------------------------------------------------
# 6 · Casos borde de 1.0 y PROCESOS
# ---------------------------------------------------------------------------


def test_casos_de_1_0_se_rompen_a_la_vista():
    c1 = ml.caso(1)
    assert c1.omitidas == ["x2", "x3"] and c1.columnas_x == ["x1"]
    assert ml.caso("omitida_correlacionada").ent.equals(c1.ent)
    c2 = ml.caso(2)
    assert len(c2.ent) == 20
    assert ml.ajustar(c2).beta_gorro["x1"] == pytest.approx(4.0, abs=1.0)
    assert ml.piso(c2) > 9 * ml.piso(ml.caso(2, omitir=None))
    for numero, caso in ml.CASOS_BORDE.items():
        dueña = 2 if 13 <= numero <= 16 else 3 if 6 <= numero <= 12 or numero == 24 else 1
        assert caso.numero == numero and caso.clase == dueña
        assert caso.pregunta.endswith("?") and caso.que_se_ve


def test_procesos_de_1_0():
    e = ml.PROCESOS["entregas"]()
    assert len(e.ent) + len(e.val) + len(e.prueba) == 20 and e.sigma2_e == 1.0
    assert ml.PROCESOS["entregas"](sigma_e=2).sigma2_e == pytest.approx(4.0)
    malla = pd.DataFrame({"x": [1.0, 2.0]})
    assert np.allclose(e.f(malla), [14.0, 18.0])
    assert np.allclose(ml.PROCESOS["inverso"]().f(malla), [7.0, 4.5])
    assert np.allclose(ml.PROCESOS["seno"]().f(malla), 4 + 2 * np.sin(5 * malla["x"]))
    x = malla["x"]
    assert np.allclose(ml.PROCESOS["mezcla_logs"]().f(malla),
                       x + np.log(x) + x * np.log(x) + 1 / x + x ** 1.3)
    assert ml.PROCESOS["lluvia"]().ent.equals(ml.caso(2).ent)


# ---------------------------------------------------------------------------
# 7 · Gráficas e interactividad
# ---------------------------------------------------------------------------


def _curvas(ax):
    return [ln.get_ydata() for ln in ax.get_lines() if ln.get_gid() == "ajuste"]


def test_dibujar_ajuste_tres_formas_mismas_curvas():
    datos = ml.PROCESOS["inverso"]()
    a, b = ml.ajustar(datos, phi=ml.polinomio(1)), ml.ajustar(datos, phi=ml.polinomio(3))
    ax1 = ml.dibujar_ajuste(a, datos)
    ax2 = ml.dibujar_ajuste([a], datos)
    ax3 = ml.dibujar_ajuste({"recta": a}, datos)
    for x, y in zip(_curvas(ax1), _curvas(ax2)):
        assert np.allclose(x, y)
    for x, y in zip(_curvas(ax1), _curvas(ax3)):
        assert np.allclose(x, y)
    ax = ml.dibujar_ajuste({"Taylor": ml.taylor("inverso", 1.0, 3), "cubo": b},
                           ventana=(0.3, 4.0))
    assert len(_curvas(ax)) == 2


def test_dibujar_perdida_1d_marca_el_minimo_en_beta_gorro():
    datos = ml.PROCESOS["entregas"](n=40)
    m = ml.ajustar(datos)
    ax = ml.dibujar_perdida_1d(datos, None, "x", np.linspace(0, 8, 41))
    marca = [ln for ln in ax.get_lines() if ln.get_gid() == "minimo"][0]
    assert marca.get_xdata()[0] == pytest.approx(m.beta_gorro["x"], abs=1e-6)


def test_dibujar_proceso_y_las_demas_corren():
    datos = ml.PROCESOS["entregas"](n=40)
    ax = ml.dibujar_proceso(datos, realizaciones=3, puntos_realidad=50)
    assert len([c for c in ax.collections if c.get_gid() == "muestra"]) == 3
    nuevas = [c for c in ax.collections if c.get_gid() == "observaciones_nuevas"]
    assert len(nuevas) == 1
    with pytest.raises(ValueError):
        ml.dibujar_proceso(datos, color_por="x")
    m = ml.ajustar(datos, phi=ml.polinomio(2))
    fig = ml.dibujar_tres_paneles(m, datos.ent)
    assert len(fig.axes) == 3
    ml.dibujar_piso(datos, {"recta": ml.ajustar(datos), "cuadrática": m})
    ml.dibujar_piso(datos, [m], tema="sitio")
    anillos = ml.anillos(n=200)
    clf = ml.ajustar(anillos, phi=ml.polares(), tarea="clasificacion")
    ml.dibujar_frontera(clf, anillos.ent)
    ml.dibujar_frontera(clf, anillos.ent, vista="polares")
    candidatos = {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N))) for N in (1, 2, 3)}
    tabla = ml.curva_capacidad(datos, candidatos, conjuntos=("ent", "despliegue"))
    ml.dibujar_curva_capacidad(tabla, piso=ml.piso(datos),
                               benchmark=ml.benchmarks(datos, datos.despliegue), marcar=2)
    ml.dibujar_curva_capacidad(tabla, piso=float("inf"), benchmark=(30.0, 1.0))
    ml.tema("sitio")
    ml.tema("claro")
    assert {"entrenamiento", "validacion", "prueba", "realidad", "f", "f_gorro", "piso",
            "observaciones_nuevas", "benchmark"} <= set(ml.ROLES)


def test_laboratorio_sin_widgets_corre_una_vez(monkeypatch):
    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    llamadas = []
    ml.laboratorio(lambda N, ruido, f: llamadas.append((N, ruido, f)),
                   N=ml.deslizador("grado N", 1, 9, 1, 3),
                   ruido=ml.interruptor("con ruido", True),
                   f=ml.selector("función", {"recíproca": "inverso", "seno": "seno"},
                                 valor="seno"))
    assert llamadas == [(3, True, "seno")]


def test_galeria_y_taller(monkeypatch):
    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    s = io.StringIO()
    with redirect_stdout(s):
        ml.galeria(1, casos=[1, 2])
    assert ml.CASOS_BORDE[1].pregunta in s.getvalue()
    s = io.StringIO()
    with redirect_stdout(s):
        ml.galeria(1, casos=["lluvia"])
    assert ml.CASOS_BORDE[2].pregunta in s.getvalue()
    with redirect_stdout(io.StringIO()):
        ml.taller(ml.PROCESOS["inverso"](), 1, N_max=6)
        ml.taller(ml.anillos(n=300), 1, phi=ml.polares())


# ---------------------------------------------------------------------------
# 8 · Revisión adversarial de 1.0 (D-018): cada prueba falló antes del arreglo
# ---------------------------------------------------------------------------


class _Laplace(ml.Pieza):
    """Una pieza del taller, con la plantilla del docstring: su repr no trae b."""

    nombre, media = "laplace", 0.0

    def __init__(self, b):
        self.b = b
        self.varianza = 2 * b * b

    def muestrear(self, n, rng):
        return rng.laplace(0, self.b, n)


def test_la_cache_distingue_piezas_propias_del_mismo_nombre():
    uno = ml.PROCESOS["entregas"](ruido=_Laplace(1))
    cinco = ml.PROCESOS["entregas"](ruido=_Laplace(5))
    assert ml.piso(uno) == pytest.approx(2.0)
    assert ml.piso(cinco) == pytest.approx(50.0)
    real = cinco.realidad
    assert np.var(real["y"] - real["f"]) == pytest.approx(50.0, rel=0.03)


def test_la_cache_ve_una_pieza_o_una_f_que_cambiaron_en_su_lugar():
    pieza = _Laplace(1)
    assert ml.piso(ml.PROCESOS["entregas"](ruido=pieza)) == pytest.approx(2.0)
    pieza.b, pieza.varianza = 3, 18.0
    despues = ml.PROCESOS["entregas"](ruido=pieza)
    assert ml.piso(despues) == pytest.approx(18.0)
    assert np.var(despues.realidad["y"] - despues.realidad["f"]) == pytest.approx(18, rel=0.03)
    k = {"c": 1.0}

    def g(d):
        return k["c"] * d["x"]

    a = ml.proceso(f=g)
    k["c"] = 3.0
    b = ml.proceso(f=g)
    assert np.allclose(b.realidad["f"], 3 * b.realidad["x"])
    assert not np.allclose(a.realidad["f"], b.realidad["f"])


def _avisos(funcion, *args, **kwargs):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        salida = funcion(*args, **kwargs)
    return salida, [str(x.message) for x in w]


def test_potencias_sin_escalar_avisan_mal_condicionamiento_y_no_pseudoinversa():
    """Caso 4 de clase_1.md §10.4: q <= n, rango numérico deficiente por la escala."""
    datos = ml.PROCESOS["inverso"](n=100)
    for N in (15, 20, 25):
        _, avisos = _avisos(ml.ajustar, datos, phi=ml.polinomio(N, escalar=False))
        assert any("mal condicionada" in a for a in avisos), (N, avisos)
        assert not any("pseudoinversa" in a for a in avisos), (N, avisos)
    _, avisos = _avisos(ml.ajustar, datos, phi=ml.polinomio(25))
    assert not any("pseudoinversa" in a for a in avisos)
    # y donde el rango sí falta, sigue la pseudoinversa con la causa correcta
    _, avisos = _avisos(ml.ajustar, ml.caso(23), phi=ml.polinomio(12))
    assert any("pseudoinversa" in a and "más parámetros" in a for a in avisos)
    df, cols = _datos_reg(colineal=True)
    _, avisos = _avisos(ml.ajustar, df, columnas_x=cols, tarea="regresion")
    assert any("pseudoinversa" in a and "repetidas" in a for a in avisos)


def test_ridge_con_escalas_dispares_no_pierde_el_intercepto():
    x = 1e9 * np.array([-2.0, -1, 0, 1, 2])
    df = pd.DataFrame({"x": x, "y": [-1.0, 1, 3, 5, 7]})
    m = ml.ajustar(df, columnas_x=["x"], tarea="regresion", mu=0.1, penalizacion="l2")
    # a mano: con x centrada, b1 = (Σ xc yc / n) / (Σ xc² / n + mu)
    b1 = (np.sum(x * (df["y"] - 3)) / 5) / (np.sum(x ** 2) / 5 + 0.1)
    assert m.beta_gorro["1"] == pytest.approx(3.0, rel=1e-9)
    assert m.beta_gorro["x"] == pytest.approx(b1, rel=1e-9)
    w = np.array([0.5, 2.0, 1.0, 3.0, 1.5])
    Phi = np.column_stack([np.ones(5), x])
    beta = ml._resolver(Phi, df["y"].to_numpy(), w, 0.1, "l2", 0.0, "regresion", True)
    g0 = -(2 / 5) * np.sum(w * (df["y"].to_numpy() - Phi @ beta))
    assert abs(g0) < 1e-9


def test_casos_con_forma_cerrada_la_sueltan_si_cambian_sus_hipotesis():
    assert ml.caso(1).f_visible(pd.DataFrame({"x1": [1.0]}))[0] == pytest.approx(1.8)
    assert ml.caso(1, n=50).f_visible(pd.DataFrame({"x1": [1.0]}))[0] == pytest.approx(1.8)
    assert ml.piso(ml.caso(2, ruido=ml.normal(1, 1))) == pytest.approx(10.0, abs=0.1)
    c2 = ml.caso(2, endogeno=0.5)
    assert ml.piso(c2) == pytest.approx(9.75, abs=0.1)
    assert c2.f_visible(pd.DataFrame({"x1": [0.0]}))[0] == pytest.approx(
        13 - 0.5 * 3 / np.sqrt(3), abs=1e-6)
    c1 = ml.caso(1, endogeno=0.5)
    assert c1.f_visible is None
    with pytest.warns(UserWarning, match="piso desconocido"):
        assert np.isnan(ml.piso(c1))


def test_logistica_cuasiseparada_avisa():
    for x, y in (([0, 1, 2, 3, 3, 4, 5, 6], [0, 0, 0, 0, 1, 1, 1, 1]),
                 ([-1, 0, 0, 1], [0, 0, 1, 1])):
        df = pd.DataFrame({"x": np.asarray(x, float), "y": y})
        with pytest.warns(UserWarning, match="se separan"):
            ml.ajustar(df, columnas_x=["x"], tarea="clasificacion")


def _logistica_fija(beta):
    df = pd.DataFrame({"x": [-1.0, 0.0, 1.0, 2.0], "y": [0, 1, 0, 1]})
    m = ml.ajustar(df, columnas_x=["x"], tarea="clasificacion")
    m.beta_gorro[:] = beta
    return m


def test_predecir_usa_el_umbral_0_5_incluido():
    m = _logistica_fija([0.0, 1.0])
    x = np.array([-1.0, -1e-9, 0.0, 1e-9, 1.0])
    df = pd.DataFrame({"x": x})
    p = m.predecir_p(df)
    assert p[2] == 0.5
    assert list(m.predecir(df)) == [0, 0, 1, 1, 1]
    assert np.array_equal(m.predecir(df) == m.clases[1], p >= 0.5)


def test_la_perdida_logistica_sale_del_puntaje_sin_infinitos():
    m = _logistica_fija([0.0, 78.377])
    df = pd.DataFrame({"x": [1.0, -1.0], "y": [0, 1]})
    assert ml.L(m, df) == pytest.approx(78.377, rel=1e-9)
    datos = ml.anillos(n=100)
    lejos = datos.ent.copy()
    lejos[["x1", "x2"]] *= 1e3
    m = ml.ajustar(datos, phi=ml.polares(incluir=("r",)), tarea="clasificacion")
    assert np.isfinite(ml.L(m, lejos))


def test_un_peso_cero_no_vuelve_nan_la_perdida():
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [0, 0, 1, 1]})
    v = ml.ajustar_otro(df, columnas_x=["x"], tarea="clasificacion", n_vecinos=1)
    nuevo = pd.DataFrame({"x": [0.0, 0.0], "y": [0, 1]})
    assert ml.L(v, nuevo, pesos={0: 1.0, 1: 0.0}) == 0.0


def test_vecinos_multiclase_da_probabilidades_y_perdida():
    df = pd.DataFrame({"x": np.arange(9.0), "y": [0, 0, 0, 1, 1, 1, 2, 2, 2]})
    v = ml.ajustar_otro(df, columnas_x=["x"], tarea="clasificacion", n_vecinos=3)
    P = v.predecir_prob(df)
    assert P.shape == (9, 3) and np.allclose(P.sum(axis=1), 1)
    assert np.allclose(P[0], [1, 0, 0]) and np.allclose(P[4], [0, 1, 0])
    l_i = -np.log(P[np.arange(9), df["y"].to_numpy()])
    assert ml.L(v, df) == pytest.approx(l_i.mean())
    with pytest.raises(ml.NoAplica):
        v.predecir_p(df)


def test_benchmarks_multiclase_y_desempate():
    df = pd.DataFrame({"x": np.arange(9.0), "y": [0, 0, 0, 1, 1, 1, 2, 2, 2]})
    t = ml.benchmarks(df, df, tarea="clasificacion")
    assert t.loc["proporcion", "logaritmica"] == pytest.approx(np.log(3))
    assert t.loc["moda", "aciertos"] == pytest.approx(1 / 3)
    # binario con p = 0.5: moda y proporcion desempatan igual que predecir (p >= 0.5)
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [0, 1, 0, 1]})
    ev = pd.DataFrame({"y": [1, 1, 1, 0]})
    t = ml.benchmarks(df, ev, tarea="clasificacion")
    assert t.loc["moda", "aciertos"] == pytest.approx(0.75)
    assert t.loc["proporcion", "aciertos"] == pytest.approx(0.75)


def test_benchmark_proporcion_usa_la_p_de_ent():
    anillos = ml.anillos(n=200)
    ev = anillos.despliegue.iloc[:500]
    p = float(np.mean(anillos.ent["y"] == 1))
    y = (ev["y"].to_numpy() == 1).astype(float)
    esperado = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    t = ml.benchmarks(anillos, ev)
    assert t.loc["proporcion", "logaritmica"] == pytest.approx(esperado, rel=1e-12)


def test_curva_capacidad_ee_es_desviacion_entre_raiz_de_n():
    datos = ml.PROCESOS["entregas"](n=20)
    tabla = ml.curva_capacidad(datos, {1: lambda df: ml.ajustar(df)}, conjuntos=("ent",))
    m = ml.ajustar(datos)
    l_i = (datos.ent["y"] - m.predecir(datos.ent)) ** 2
    assert tabla["ee"].iloc[0] == pytest.approx(np.std(l_i, ddof=1) / np.sqrt(len(l_i)))


def test_dummies_efectos_categoria_no_vista_es_el_promedio_de_los_grupos():
    df = _df_con_categoria()
    phi = lambda: ml.combinar(ml.columnas("x"), ml.dummies("g", codificacion="efectos"))  # noqa: E731
    m = ml.ajustar(df, phi=phi())
    x0 = 0.4
    grupos = [m.predecir(pd.DataFrame({"x": [x0], "g": [c]}))[0] for c in "abc"]
    with pytest.warns(UserWarning, match="grupo promedio"):
        nuevo = m.predecir(pd.DataFrame({"x": [x0], "g": ["zeta"]}))[0]
    assert nuevo == pytest.approx(np.mean(grupos), abs=1e-9)
    otro = df.copy()
    otro["g"] = otro["g"].map({"a": "c", "b": "b", "c": "a"})
    m2 = ml.ajustar(otro, phi=phi())
    with pytest.warns(UserWarning, match="grupo promedio"):
        nuevo2 = m2.predecir(pd.DataFrame({"x": [x0], "g": ["zeta"]}))[0]
    assert nuevo2 == pytest.approx(nuevo, abs=1e-9)


def test_escala_de_una_omitida_no_toca_f():
    datos = ml.proceso(x={"x1": ml.uniforme(), "x2": ml.uniforme()},
                       f=lambda d: d["x1"] + d["x2"], omitir=["x2"], escala={"x2": 1000})
    real = datos.realidad
    assert np.allclose(datos.f(real), real["f"])


def test_piso_nan_de_una_pieza_sin_varianza_avisa():
    class SinVarianza(ml.Pieza):
        nombre, media = "sin_varianza", 0.0

        def muestrear(self, n, rng):
            return rng.normal(0, 1, n)

    datos = ml.PROCESOS["entregas"](ruido=SinVarianza())
    with pytest.warns(UserWarning, match="piso desconocido"):
        assert np.isnan(ml.piso(datos))


def test_dibujar_ajuste_no_junta_modelos_con_el_mismo_rotulo():
    a = ml.ajustar(ml.PROCESOS["inverso"](semilla=1))
    b = ml.ajustar(ml.PROCESOS["inverso"](semilla=2))
    ax = ml.dibujar_ajuste([a, b], ventana=(0.3, 3.0))
    assert len(_curvas(ax)) == 2


def test_dibujar_proceso_nombra_f_verdadera_solo_si_lo_es():
    def rotulo(datos):
        ax = ml.dibujar_proceso(datos)
        return [ln.get_label() for ln in ax.get_lines() if ln.get_gid() == "f"][0]

    assert rotulo(ml.PROCESOS["entregas"]()) == "f verdadera"
    assert rotulo(ml.PROCESOS["entregas"](endogeno=0.5)) == "E[y | lo visible]"
    assert rotulo(ml.PROCESOS["entregas"](ruido=ml.normal(1, 1))) == "E[y | lo visible]"


@pytest.mark.parametrize("vieja,nueva,compatible", [
    ("(datos, phi)", "(datos, phi, obligatorio)", False),
    ("(x, N=3)", "(x, N=30)", False),
    ("(x, a=1)", "(x, b=2, a=1)", False),
    ("(x, *, a=1)", "(x, *, a=1, b)", False),
    ("(x, **cambios)", "(x)", False),
    ("(x, a=1)", "(x, a=1, b=2)", True),
    ("(x)", "(x, *, b=2)", True),
    ("(x, *, a=1)", "(x, *, a=1, b={'k': (1, 2)})", True),
    ("(x, f=<function _f>)", "(x, f=<function _f>, g=None)", True),
])
def test_la_guarda_de_compatibilidad_compara_parametro_a_parametro(vieja, nueva, compatible):
    if compatible:
        _compatible({"g": vieja}, {"g": nueva})
    else:
        with pytest.raises(AssertionError):
            _compatible({"g": vieja}, {"g": nueva})


# ---------------------------------------------------------------------------
# 9 · Versión 1.1 (O0b-c1, contrato §5.15 B, D-013b)
# ---------------------------------------------------------------------------


def test_las_funciones_nuevas_dicen_desde_cuando():
    for nombre in ("repetir", "error_por_zona", "no_free_lunch", "dibujar_no_free_lunch",
                   "dibujar_elecciones", "proceso_clasificacion"):
        assert "Desde: 1.1 (clase 1)" in getattr(ml, nombre).__doc__, nombre
    assert "Desde: 1.1 (clase 1)" in ml.PROCESOS["recursivo"].__doc__


def test_repetir_es_determinista_y_apila():
    def experimento(semilla):
        rng = np.random.default_rng(semilla)
        return {"media": float(rng.normal(size=10).mean()), "n": 10}

    a = ml.repetir(experimento, repeticiones=7, semilla=3)
    b = ml.repetir(experimento, repeticiones=7, semilla=3)
    assert a.equals(b)
    assert list(a.columns) == ["repeticion", "semilla", "media", "n"]
    assert a["repeticion"].tolist() == list(range(7))
    assert a["semilla"].tolist() == list(range(3, 10))
    assert a.loc[2, "media"] == experimento(5)["media"]
    assert not a.equals(ml.repetir(experimento, repeticiones=7, semilla=4))
    with pytest.raises(TypeError, match="dict"):
        ml.repetir(lambda s: s, repeticiones=2)
    with pytest.raises(ValueError, match="semilla"):
        ml.repetir(lambda s: {"semilla": s}, repeticiones=2)


def test_error_por_zona_contra_la_cuenta_a_mano():
    datos = ml.PROCESOS["entregas"](n=30)
    m = ml.ajustar(datos)
    b0, b1 = m.beta_gorro["1"], m.beta_gorro["x"]
    tabla = ml.error_por_zona(m, datos, {"dentro": (0, 6), "fuera": (6, 9)}, puntos=2001)
    assert list(tabla.columns) == ["zona", "desde", "hasta", "dif2", "var_y_dado_x", "R_zona"]
    assert tabla["zona"].tolist() == ["dentro", "fuera"]
    # (f − f̂)² = (a + c x)² con a = 10 − b0, c = 4 − b1; promedio exacto en [lo, hi]
    a, c = 10 - b0, 4 - b1
    for _, fila in tabla.iterrows():
        lo, hi = fila["desde"], fila["hasta"]
        exacto = a * a + a * c * (lo + hi) + c * c * (lo * lo + lo * hi + hi * hi) / 3
        assert fila["dif2"] == pytest.approx(exacto, rel=1e-3)  # malla de 2001 puntos
        assert fila["R_zona"] == pytest.approx(fila["dif2"] + 1.0, rel=1e-12)
    # la zona de los datos, con x uniforme y despliegue igual, es ≈ R
    assert tabla.loc[0, "R_zona"] == pytest.approx(ml.riesgo(m, datos), rel=0.03)
    with pytest.raises(ValueError, match="una variable"):
        ml.error_por_zona(ml.ajustar(ml.caso(1, omitir=None)), ml.caso(1, omitir=None),
                          {"z": (0, 1)})


def test_no_free_lunch_promedia_exactamente_un_medio():
    from fractions import Fraction

    tabla = ml.no_free_lunch()
    assert list(tabla.columns) == ["funcion", "regla", "aciertos_fuera", "rugosidad"]
    assert tabla["funcion"].nunique() == 256 and len(tabla) == 3 * 256
    assert set(tabla["regla"]) == {"vecino", "mayoria", "siempre_1"}
    for regla, trozo in tabla.groupby("regla"):
        total = sum(Fraction(v) for v in trozo["aciertos_fuera"])
        assert total / len(trozo) == Fraction(1, 2), regla
    siempre = tabla[tabla["regla"] == "siempre_1"]
    for r, trozo in siempre.groupby("rugosidad"):
        assert sum(Fraction(v) for v in trozo["aciertos_fuera"]) / len(trozo) == Fraction(1, 2), r
    assert tabla["rugosidad"].min() == 0 and tabla["rugosidad"].max() == 12
    # desempate de la mayoría: entrenamiento (0, 3, 5, 6) con etiquetas 1, 1, 0, 0 → 1
    funcion = (1 << 0) | (1 << 3)  # f(0) = f(3) = 1, todo lo demás 0
    fila = tabla[(tabla["funcion"] == funcion) & (tabla["regla"] == "mayoria")].iloc[0]
    assert fila["aciertos_fuera"] == 0.0  # predice 1 en 1, 2, 4, 7, donde f vale 0
    # el vecino desempata por el índice menor: el 1 tiene a 0, 3 y 5 a distancia 1 → copia f(0)
    # (1, 2 y 4 tienen al 0 entre sus vecinos a distancia 1; el 7 no: copia f(3) = 0)
    vec = tabla[(tabla["funcion"] == 1) & (tabla["regla"] == "vecino")].iloc[0]
    assert vec["aciertos_fuera"] == 0.25  # falla en 1, 2 y 4 (copia f(0) = 1), acierta en 7
    with pytest.raises(ValueError):
        ml.no_free_lunch(reglas=("adivina",))


def test_dibujar_no_free_lunch_es_el_groupby():
    tabla = ml.no_free_lunch()
    ax = ml.dibujar_no_free_lunch(tabla)
    for regla, trozo in tabla.groupby("regla"):
        medias = trozo.groupby("rugosidad")["aciertos_fuera"].mean().astype(float)
        ln = [ln for ln in ax.get_lines() if ln.get_gid() == f"regla-{regla}"][0]
        assert np.allclose(ln.get_xdata(), medias.index) and np.allclose(ln.get_ydata(), medias)
        assert f"{trozo['aciertos_fuera'].mean():.3f}" in ln.get_label()
    assert any(ln.get_gid() == "medio" for ln in ax.get_lines())


def test_dibujar_elecciones_son_los_value_counts():
    tabla = pd.DataFrame({"N_ent": [15, 15, 15, 14], "N_R": [4, 5, 4, 6]})
    ejes = ml.dibujar_elecciones(tabla)
    assert len(ejes) == 2
    for ax, col in zip(ejes, ("N_ent", "N_R")):
        alturas = {round(b.get_x() + b.get_width() / 2): b.get_height() for b in ax.patches}
        assert alturas == tabla[col].value_counts().to_dict()
    with pytest.raises(ValueError):
        ml.dibujar_elecciones(tabla, columnas=("N_ent", "no_hay"))


def test_proceso_clasificacion_oraculo_es_sigma_del_puntaje():
    datos = ml.proceso_clasificacion(n=500)
    assert datos.tarea == "clasificacion" and datos.K == 2 and list(datos.clases) == [0, 1]
    assert datos.columnas_x == ["x1", "x2"]
    assert len(datos.ent) == 300 and len(datos.val) == 100 and len(datos.prueba) == 100
    real = datos.realidad
    z = 1.5 * real["x1"] + 1.0 * real["x2"]
    assert np.allclose(real["prob"], 1 / (1 + np.exp(-z)))
    # la frecuencia de y = 1 sigue a prob
    bandas = pd.cut(real["prob"], np.linspace(0, 1, 11))
    tabla = real.groupby(bandas, observed=True).agg(p=("prob", "mean"), y=("y", "mean"))
    assert np.allclose(tabla["p"], tabla["y"], atol=0.02)
    assert "prob" not in datos.ent.columns
    # estratificado: la proporción de y = 1 casi igual en los tres conjuntos
    props = [d["y"].mean() for d in (datos.ent, datos.val, datos.prueba)]
    assert max(props) - min(props) < 0.02
    # un puntaje propio, ajustar y el piso logarítmico
    propio = ml.proceso_clasificacion(n=400, x={"a": ml.uniforme(-2, 2)},
                                      puntaje=lambda d: 3 * d["a"], separar="azar")
    m = ml.ajustar(propio, tarea="clasificacion")
    assert m.beta_gorro["a"] == pytest.approx(3, abs=1.2)
    assert 0 < ml.piso(propio, "logaritmica") < ml.riesgo(m, propio, "logaritmica")
    assert ml.proceso_clasificacion(semilla=1).ent.equals(ml.proceso_clasificacion(semilla=1).ent)


@pytest.mark.parametrize("cambio", [
    {"proporcion": 0.1}, {"ruido_etiquetas": 0.1}, {"K": 3},
    {"faltantes": {"x1": (0.2, "azar")}}, {"ruido": ml.normal(0, 1)},
    {"separar": "tiempo"}, {"separar": "grupo"},
])
def test_adelantos_de_proceso_clasificacion_lanzan_con_la_clase_4(cambio):
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.proceso_clasificacion(n=50, con_realidad=False, **cambio)


def test_adelantos_de_proceso_clasificacion_de_la_clase_2_y_errores():
    # 1.2: despliegue y deriva funcionan con la implementación común
    with pytest.raises(ValueError, match="columna t"):
        ml.proceso_clasificacion(n=50, despliegue="futuro", con_realidad=False)
    otra = ml.proceso_clasificacion(n=50, despliegue="otra_poblacion",
                                    deriva=lambda t: {"x1": ml.uniforme(3, 4)})
    assert otra.despliegue["x1"].min() >= 3 and otra.realidad["x1"].min() < 0
    z = 1.5 * otra.despliegue["x1"] + otra.despliegue["x2"]
    assert np.allclose(otra.despliegue["prob"], 1 / (1 + np.exp(-z)))
    concepto = ml.proceso_clasificacion(n=50, despliegue="otra_poblacion",
                                        deriva=lambda t: {"f": lambda d: -d["x1"]})
    assert np.allclose(concepto.despliegue["prob"], 1 / (1 + np.exp(concepto.despliegue["x1"])))
    with pytest.raises(ValueError, match="grupo"):
        ml.proceso_clasificacion(n=50, despliegue="grupos_nuevos", con_realidad=False)
    with pytest.raises(ValueError, match="deriva"):
        ml.proceso_clasificacion(n=50, deriva=lambda t: {}, con_realidad=False)
    with pytest.raises(ValueError):
        ml.proceso_clasificacion(n=50, separar="temporal", con_realidad=False)
    with pytest.raises(ValueError):
        ml.proceso_clasificacion(n=50, K=1, con_realidad=False)


def test_firma_de_proceso_clasificacion_es_la_de_5_5():
    nombres = list(inspect.signature(ml.proceso_clasificacion).parameters)
    assert nombres == [
        "n", "x", "puntaje", "K", "puntajes", "proporcion", "ruido_etiquetas", "separar",
        "fracciones", "despliegue", "deriva", "n_realidad", "semilla", "semilla_realidad",
        "faltantes", "ruido", "con_realidad",
    ]
    defectos = {k: v.default for k, v in inspect.signature(ml.proceso_clasificacion).parameters.items()}
    assert defectos["n"] == 500 and defectos["K"] == 2 and defectos["separar"] == "estratificado"
    assert defectos["faltantes"] is None and defectos["ruido"] is None
    assert defectos["con_realidad"] is True and defectos["ruido_etiquetas"] == 0.0


def test_mutacion_mover_ruido_tras_con_realidad_rompe_la_superficie(monkeypatch):
    esperado = _entradas()[ml.VERSION]

    def movida(n=500, x=None, puntaje=None, K=2, puntajes=None, proporcion=None,
               ruido_etiquetas=0.0, separar="estratificado", fracciones=(0.6, 0.2, 0.2),
               despliegue="igual", deriva=None, n_realidad=100_000, semilla=0,
               semilla_realidad=0, faltantes=None, con_realidad=True, ruido=None):
        return None

    monkeypatch.setattr(ml, "proceso_clasificacion", movida)
    assert ml._superficie() != esperado


def test_recursivo_es_una_serie_que_se_evalua_a_un_paso():
    datos = ml.PROCESOS["recursivo"]()
    assert datos.columnas_x == ["x", "y_anterior"] and datos.columnas_contexto == ["t"]
    assert len(datos.ent) == 60 and len(datos.val) == 0 and len(datos.prueba) == 20
    assert datos.ent["t"].tolist() == list(range(60))
    assert datos.prueba["t"].tolist() == list(range(60, 80))
    serie = pd.concat([datos.ent, datos.prueba])
    assert np.all(np.diff(serie["x"]) > 0)  # x crece con el tiempo
    assert serie["x"].iloc[0] == pytest.approx(1, abs=0.05)
    assert serie["x"].iloc[-1] == pytest.approx(5, abs=0.05)
    # y_anterior es el y observado un paso antes
    assert np.allclose(serie["y_anterior"].iloc[1:].to_numpy(), serie["y"].iloc[:-1].to_numpy())
    # f = 0.8·y_anterior + la mezcla de logaritmos de x; el residuo es el ruido
    x = serie["x"]
    g = x + np.log(x) + x * np.log(x) + 1 / x + x ** 1.3
    assert np.allclose(datos.f(serie), 0.8 * serie["y_anterior"] + g)
    assert datos.sigma2_e == 1.0 and ml.piso(datos) == pytest.approx(1.0)
    # realidad: el tramo de entrenamiento; despliegue: el futuro, a un paso
    assert datos.realidad["t"].max() == 59 and datos.despliegue["t"].min() == 60
    assert datos.despliegue["x"].min() > datos.ent["x"].max() - 0.05
    desp = datos.despliegue
    assert np.mean((desp["y"] - desp["f"]) ** 2) == pytest.approx(1.0, abs=0.03)
    m_tiempo = ml.ajustar(datos, phi=ml.columnas("x", "y_anterior"))
    assert ml.riesgo(m_tiempo, datos) < 1.5
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m_poli = ml.ajustar(datos, phi=ml.polinomio(4))
    assert ml.riesgo(m_poli, datos) > 5 * ml.riesgo(m_tiempo, datos)
    assert ml.PROCESOS["recursivo"](semilla=2).ent.equals(ml.PROCESOS["recursivo"](semilla=2).ent)
    with pytest.raises(ValueError, match="recursivo"):
        ml.PROCESOS["recursivo"](separar="azar")


def test_casos_3_4_y_5_se_rompen_a_la_vista():
    # caso 3: ningún polinomio de grado <= 10 alcanza a (1, 1/x)
    for n in (20, 60):
        datos = ml.caso(3, n=n)
        assert len(datos.ent) == n
        r_buena = ml.riesgo(ml.ajustar(datos, phi=ml.columnas("1/x")), datos)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r_poli = min(ml.riesgo(ml.ajustar(datos, phi=ml.polinomio(N)), datos)
                         for N in range(1, 11))
        assert r_poli >= 1.5 * r_buena, (n, r_poli, r_buena)
    # caso 4: sin escalar, más columnas y L_ent sube, con aviso de mal condicionamiento
    datos = ml.caso(4)
    assert len(datos.ent) == 100
    m25, avisos = _avisos(ml.ajustar, datos, phi=ml.polinomio(25, escalar=False))
    m10 = ml.ajustar(datos, phi=ml.polinomio(10, escalar=False))
    assert ml.L(m25, datos.ent) > ml.L(m10, datos.ent)
    assert any("mal condicionada" in a for a in avisos)
    assert not any("pseudoinversa" in a for a in avisos)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        L_esc = [ml.L(ml.ajustar(datos, phi=ml.polinomio(N)), datos.ent) for N in (10, 15, 20, 25)]
    assert all(b <= a + 1e-9 for a, b in zip(L_esc, L_esc[1:]))
    # caso 5: el seno con N = 7 acierta dentro y falla fuera
    datos = ml.caso(5)
    assert len(datos.ent) == 50
    m = ml.ajustar(datos, phi=ml.polinomio(7))
    tabla = ml.error_por_zona(m, datos, {"dentro": (0, 2), "fuera": (2, 3)}).set_index("zona")
    assert tabla.loc["fuera", "R_zona"] >= 10 * tabla.loc["dentro", "R_zona"]
    for numero in (3, 4, 5):
        cb = ml.CASOS_BORDE[numero]
        assert cb.numero == numero and cb.clase == 1 and cb.pregunta.endswith("?")
    assert ml.caso("seno_extrapolar").ent.equals(ml.caso(5).ent)


def test_galeria_corre_los_casos_nuevos_con_sus_opciones(monkeypatch):
    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    for numero in (3, 4, 5):
        s = io.StringIO()
        with redirect_stdout(s):
            ml.galeria(1, casos=[numero])
        assert ml.CASOS_BORDE[numero].pregunta in s.getvalue()
    s = io.StringIO()
    with redirect_stdout(s):
        ml.galeria(1, casos=[5])
    assert "fuera" in s.getvalue()


# --- Revisión del lote O0b-c1 (codex-rev-lab-O0b-c1): cada prueba falló antes del arreglo ---


class _Prediccion:
    """Un modelo que predice con una función fija de la malla."""

    def __init__(self, funcion):
        self.funcion = funcion

    def predecir(self, df):
        return np.asarray(self.funcion(df), float)


def test_error_por_zona_suma_la_varianza_de_y_dado_lo_visible():
    # caso 2: con 13 + 4·x1 (el óptimo), lo que queda es Var(6·lluvia) + σ² = 36·¼ + 1 = 10
    datos = ml.caso(2)
    tabla = ml.error_por_zona(_Prediccion(lambda d: 13 + 4 * d["x1"]), datos, {"z": (0, 6)},
                              variable="x1")
    assert list(tabla.columns) == ["zona", "desde", "hasta", "dif2", "var_y_dado_x", "R_zona"]
    assert tabla.loc[0, "dif2"] == pytest.approx(0, abs=1e-12)
    assert tabla.loc[0, "var_y_dado_x"] == pytest.approx(10, rel=1e-9)
    assert tabla.loc[0, "R_zona"] == pytest.approx(10, rel=1e-9)
    # endogeno = 0.8 con ruido N(0, 1): Var(ε | x) = 1 − 0.8² = 0.36
    endo = ml.proceso(n=50, endogeno=0.8)
    tabla = ml.error_por_zona(_Prediccion(endo.f_visible), endo, {"z": (0, 1)})
    assert tabla.loc[0, "R_zona"] == pytest.approx(0.36, rel=1e-9)
    # y con el predictor óptimo, la zona de los datos coincide con el piso
    assert tabla.loc[0, "R_zona"] == pytest.approx(ml.piso(endo), rel=0.02)


def test_error_por_zona_rechaza_lo_que_no_sabe_medir():
    # caso 1: las omitidas están correlacionadas con x1; Var(y | x1) no se sabe por fila
    datos = ml.caso(1)
    with pytest.raises(ValueError, match="Var"):
        ml.error_por_zona(_Prediccion(datos.f_visible), datos, {"z": (-1, 1)}, variable="x1")


def test_error_por_zona_distingue_sigma_de_sigma_cuadrada():
    datos = ml.PROCESOS["entregas"](n=30, ruido=ml.normal(0, 2))
    tabla = ml.error_por_zona(ml.ajustar(datos), datos, {"z": (0, 6)})
    assert (tabla["R_zona"] - tabla["dif2"]).tolist() == pytest.approx([4.0], rel=1e-12)


@pytest.mark.parametrize("zonas, puntos, patron", [
    ({"z": (0, 1)}, 0, "puntos"), ({"z": (0, 1)}, 1, "puntos"), ({"z": (0, 1)}, 2.5, "puntos"),
    ({"z": (0, 1)}, True, "puntos"), ({"z": (0, np.inf)}, 10, "finit"),
    ({"z": (np.nan, 1)}, 10, "finit"),
])
def test_error_por_zona_exige_una_malla_que_mida(zonas, puntos, patron):
    datos = ml.PROCESOS["entregas"](n=30)
    with pytest.raises(ValueError, match=patron):
        ml.error_por_zona(ml.ajustar(datos), datos, zonas, puntos=puntos)


def test_error_por_zona_nombra_la_zona_donde_queda_indefinido():
    datos = ml.proceso(n=30, x={"x": ml.uniforme(1, 2)}, f=lambda d: np.log(d["x"]))
    with pytest.raises(ValueError, match="negativa"):
        with np.errstate(all="ignore"):
            ml.error_por_zona(_Prediccion(lambda d: 0 * d["x"]), datos,
                              {"positiva": (1, 2), "negativa": (-2, -1)})


def test_error_por_zona_con_dos_puntos_ya_promedia():
    # f(x) = x, predictor 0, sin ruido: con la malla fina la media de x² en [0, 1] es 1/3
    datos = ml.proceso(n=30, f=lambda d: d["x"], ruido=ml.normal(0, 0))
    tabla = ml.error_por_zona(_Prediccion(lambda d: 0 * d["x"]), datos, {"z": (0, 1)},
                              puntos=20_001)
    assert tabla.loc[0, "R_zona"] == pytest.approx(1 / 3, rel=1e-4)


def test_repetir_con_cero_repeticiones_conserva_las_columnas():
    vacio = ml.repetir(lambda s: {"a": s}, repeticiones=0)
    assert len(vacio) == 0 and list(vacio.columns) == ["repeticion", "semilla"]
    for malo in (-1, 1.9, True, "3"):
        with pytest.raises(ValueError, match="repeticiones"):
            ml.repetir(lambda s: {"a": s}, repeticiones=malo)


def test_no_free_lunch_rugosidad_en_funciones_conocidas():
    tabla = ml.no_free_lunch(reglas=("siempre_1",))
    rug = tabla.set_index("funcion")["rugosidad"]
    paridad = sum(1 << i for i in range(8) if bin(i).count("1") % 2)
    assert rug[0] == 0 and rug[255] == 0  # constantes: ninguna arista cambia
    assert rug[1] == 3 and rug[1 << 7] == 3  # un solo vértice en 1: sus tres aristas
    assert rug[paridad] == 12  # paridad: todas las aristas cambian


def test_no_free_lunch_es_exacto_y_global_pondera_por_funciones():
    from fractions import Fraction

    tabla = ml.no_free_lunch(entrenamiento=(0, 3, 5))  # cinco puntos fuera: quintos
    for regla, trozo in tabla.groupby("regla"):
        assert all(isinstance(v, Fraction) for v in trozo["aciertos_fuera"])
        assert sum(trozo["aciertos_fuera"]) / len(trozo) == Fraction(1, 2), regla
    # aquí la media de medias por rugosidad NO es 1/2 (vecino ≈ 0.528, mayoría 0.535)
    medias = tabla[tabla["regla"] == "vecino"].groupby("rugosidad")["aciertos_fuera"].mean()
    assert abs(float(medias.astype(float).mean()) - 0.5) > 0.02
    ax = ml.dibujar_no_free_lunch(tabla)
    for regla in ("vecino", "mayoria", "siempre_1"):
        ln = [ln for ln in ax.get_lines() if ln.get_gid() == f"regla-{regla}"][0]
        assert "(promedio 0.500)" in ln.get_label(), ln.get_label()
    plt.close("all")


def test_proceso_clasificacion_rechaza_nombres_reservados():
    for nombre in ("prob", "y"):
        with pytest.raises(ValueError, match=nombre):
            ml.proceso_clasificacion(n=50, x={nombre: ml.normal()},
                                     puntaje=lambda d, k=nombre: d[k], con_realidad=False)


def test_proceso_clasificacion_otra_semilla_cambia_la_muestra_entera():
    def todo(s):
        d = ml.proceso_clasificacion(n=200, semilla=s, con_realidad=False)
        return pd.concat([d.ent, d.val, d.prueba]).sort_index()

    a, b = todo(0), todo(1)
    assert a.equals(todo(0))
    assert not np.allclose(a["x1"].to_numpy(), b["x1"].to_numpy())
    # la misma semilla con otras fracciones: mismos datos, otra partición
    c = ml.proceso_clasificacion(n=200, semilla=0, fracciones=(0.5, 0.25, 0.25),
                                 con_realidad=False)
    assert pd.concat([c.ent, c.val, c.prueba]).sort_index().equals(a)


def test_recursivo_otra_semilla_cambia_la_serie():
    a, b = ml.PROCESOS["recursivo"](semilla=0), ml.PROCESOS["recursivo"](semilla=1)
    assert not np.allclose(a.ent["y"].to_numpy(), b.ent["y"].to_numpy())
    assert not np.allclose(a.prueba["x"].to_numpy(), b.prueba["x"].to_numpy())


def test_recursivo_realidad_y_despliegue_son_filas_independientes_de_todo_el_tramo():
    chica = ml.PROCESOS["recursivo"](n_realidad=10, semilla_realidad=3)
    assert chica.despliegue["t"].max() > 70  # no solo los primeros pasos del futuro
    assert chica.realidad["t"].max() > 10
    datos = ml.PROCESOS["recursivo"]()
    for df, (lo, hi) in ((datos.realidad, (0, 60)), (datos.despliegue, (60, 80))):
        cuenta = df["t"].value_counts()
        assert set(cuenta.index) == set(range(lo, hi))
        assert cuenta.max() - cuenta.min() <= 2  # tiempos estratificados: uniformes en el tramo
    # filas de réplicas independientes: y_anterior de una fila no es el y de la previa
    real = datos.realidad
    seguidas = np.isclose(real["y_anterior"].to_numpy()[1:], real["y"].to_numpy()[:-1])
    assert seguidas.mean() < 0.01


# ---------------------------------------------------------------------------
# 10 · Versión 1.2 (lote de la clase 2, contrato §5.15 C, D-013c-c2)
# ---------------------------------------------------------------------------

NUEVAS_1_2 = ("ar1", "efecto_grupo", "entregas_curvas", "separar", "pliegues", "error_estandar",
              "intervalo", "validacion_cruzada", "diferencia_pareada", "diferencia_por_pliegue",
              "elegir", "cv_anidada", "optimismo_por_seleccion", "capacidad_elegida", "reparto",
              "sesgo_varianza", "curva_aprendizaje", "dibujar_pliegues",
              "dibujar_histograma_estimaciones", "dibujar_cv", "dibujar_abanico",
              "dibujar_sesgo_varianza", "dibujar_curva_aprendizaje", "dibujar_cajas_pliegues",
              "dibujar_diana", "dibujar_contratos", "dibujar_reparto")


def _polis(Ns, var="x"):
    return {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N, variable=var))) for N in Ns}


class _Constante(ml.Modelo):
    """Un predictor fijo para las pruebas (tarea regresión)."""

    familia, tarea = "constante", "regresion"

    def __init__(self, valor):
        self.valor = float(valor)

    def predecir(self, df):
        return np.full(len(df), self.valor)


def test_las_funciones_de_1_2_dicen_desde_cuando():
    for nombre in NUEVAS_1_2:
        assert "Desde: 1.2 (clase 2)" in getattr(ml, nombre).__doc__, nombre
    assert "Desde: 1.2 (clase 2)" in ml.Datos.rehacer.__doc__
    assert ml.PROCESOS["entregas_curvas"] is ml.entregas_curvas


def test_ar1_es_estacionario_desde_el_primer_paso():
    a, desv = 0.95, 3.0
    mec = ml.ar1(a, desv)
    assert mec.crea == ["t"] and mec.varianza == pytest.approx(desv ** 2 / (1 - a ** 2))
    rng = np.random.default_rng(0)
    primeros = np.array([mec.muestrear(pd.DataFrame({"t": np.arange(3)}), rng)[0]
                         for _ in range(4000)])
    assert np.var(primeros) == pytest.approx(mec.varianza, rel=0.08)
    serie = mec.muestrear(pd.DataFrame({"t": np.arange(20_000)[::-1]}), rng)[::-1]
    assert np.corrcoef(serie[:-1], serie[1:])[0, 1] == pytest.approx(a, abs=0.02)
    with pytest.raises(ValueError, match="persistencia"):
        ml.ar1(1.0)


def test_efecto_grupo_fija_pacientes_y_crea_nuevos():
    mec = ml.efecto_grupo(24, 4, 1)
    assert mec.crea == ["grupo"] and mec.varianza == pytest.approx(17)
    g = mec.preparar(240, np.random.default_rng(0))["grupo"]
    assert sorted(np.unique(g)) == list(range(24)) and np.all(np.bincount(g) == 10)
    nuevos = mec.preparar_nuevos(100, np.random.default_rng(0))["grupo"]
    assert nuevos.min() >= 24
    # el efecto de un paciente es de la población: no cambia con la semilla
    assert np.allclose(mec._efecto([3, 3, 7]), mec._efecto(np.array([3, 3, 7])))
    d1 = ml.caso(14, semilla=1)
    d2 = ml.caso(14, semilla=2)
    assert d1.sigma2_e == pytest.approx(17)
    assert ml.piso(d1) == pytest.approx(17)
    pd.testing.assert_frame_equal(d1.despliegue, d2.despliegue)


def test_despliegue_futuro():
    """Contrato §5.5 v5: t sigue a la muestra; otra realización estacionaria del ruido."""
    a, desv, n = 0.95, 3.0, 240
    datos = ml.proceso(n=n, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 0 * d["x"],
                       ruido=ml.ar1(a, desv), despliegue="futuro")
    muestra = pd.concat([datos.ent, datos.val, datos.prueba])
    assert sorted(muestra["t"]) == list(range(n))
    t_desp = datos.despliegue["t"].to_numpy()
    assert t_desp.min() == n and t_desp.max() == n + len(t_desp) - 1
    assert t_desp.min() > muestra["t"].max()
    otra = ml.proceso(n=n, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 0 * d["x"],
                      ruido=ml.ar1(a, desv), despliegue="futuro", semilla=9)
    pd.testing.assert_frame_equal(datos.despliegue.reset_index(drop=True),
                                  otra.despliegue.reset_index(drop=True))
    eps = datos.despliegue["y"].to_numpy() - 10
    assert np.var(eps) == pytest.approx(desv ** 2 / (1 - a ** 2), rel=0.05)
    pares = []
    for s in range(200):
        d = ml.proceso(n=40, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 0 * d["x"],
                       ruido=ml.ar1(a, desv), despliegue="futuro", semilla=s,
                       semilla_realidad=s, n_realidad=50)
        m = pd.concat([d.ent, d.val, d.prueba]).sort_values("t")
        pares.append((m["y"].iloc[-1] - 10, d.despliegue.sort_values("t")["y"].iloc[0] - 10))
    pares = np.array(pares)
    assert abs(np.corrcoef(pares[:, 0], pares[:, 1])[0, 1]) < 0.2  # no es continuación
    with pytest.raises(ValueError, match="deriva"):
        ml.proceso(n=40, ruido=ml.ar1(), deriva=lambda t: {})
    with pytest.raises(NotImplementedError, match="clase 4"):
        ml.proceso(n=40, ruido=ml.ar1(), despliegue="futuro", faltantes={"x": (0.1, "azar")})
    for numero in (13, 14, 15):
        ml.caso(numero, n_realidad=2000)


def test_deriva_cambia_x_o_f_en_el_despliegue():
    base = dict(n=60, x={"x": ml.uniforme(0, 6)}, f=lambda d: 2 * d["x"], n_realidad=5000)
    otra = ml.proceso(despliegue="otra_poblacion", deriva=lambda t: {"x": ml.uniforme(4, 9)},
                      **base)
    assert otra.despliegue["x"].min() >= 4 and otra.realidad["x"].max() <= 6
    assert np.allclose(otra.despliegue["f"], 2 * otra.despliegue["x"])
    concepto = ml.proceso(despliegue="otra_poblacion", deriva=lambda t: {"f": lambda d: -d["x"]},
                          **base)
    assert np.allclose(concepto.despliegue["f"], -concepto.despliegue["x"])
    futuro = ml.proceso(ruido=ml.ar1(0.5, 1), despliegue="futuro",
                        deriva=lambda t: {"x": 0.001 * t}, **base)
    assert np.allclose(futuro.despliegue["x"], 0.001 * futuro.despliegue["t"])
    with pytest.raises(ValueError, match="variable"):
        ml.proceso(despliegue="otra_poblacion", deriva=lambda t: {"z": 1}, **base)
    # con f_visible de forma cerrada, la deriva la deja en nan (y el piso es desconocido)
    lluvia = ml.caso(2, despliegue="otra_poblacion", deriva=lambda t: {"x1": ml.uniforme(5, 6)})
    assert lluvia.despliegue["f_visible"].isna().all()


def test_separar_y_proceso_nunca_mezclan_tiempo_ni_grupos():
    t = ml.proceso(n=100, ruido=ml.ar1(), separar="tiempo")
    assert t.ent["t"].max() < t.val["t"].min() and t.val["t"].max() < t.prueba["t"].min()
    g = ml.caso(14, separar="grupo")
    grupos = [set(p["grupo"]) for p in (g.ent, g.val, g.prueba)]
    assert not (grupos[0] & grupos[1] or grupos[0] & grupos[2] or grupos[1] & grupos[2])
    # separar es una función pública con el mismo vocabulario, y conserva attrs
    ent, val, pru = ml.separar(pd.concat([g.ent, g.val, g.prueba]), como="grupo", semilla=3)
    assert ent.attrs["ml"]["tarea"] == "regresion"
    assert not set(ent["grupo"]) & set(pru["grupo"])
    a, b, c = ml.separar(pd.concat([t.ent, t.val, t.prueba]), como="tiempo")
    assert a["t"].max() < c["t"].min()
    with pytest.raises(ValueError, match="temporal"):
        ml.separar(t.ent, como="temporal")
    # estratificado en regresión: deciles de y, las tres partes con todo el rango
    e = ml.proceso(n=200, separar="estratificado")
    assert len(e.ent) == 120 and len(e.val) == 40 and len(e.prueba) == 40
    assert e.prueba["y"].min() < e.ent["y"].quantile(0.2) < e.ent["y"].quantile(0.8) < \
        e.prueba["y"].max()
    # mismas semillas, solo cambia separar: misma muestra y mismo despliegue
    az = ml.caso(14, separar="azar")
    juntas = lambda d: pd.concat([d.ent, d.val, d.prueba]).sort_index()  # noqa: E731
    pd.testing.assert_frame_equal(juntas(az), juntas(g))
    pd.testing.assert_frame_equal(az.despliegue, g.despliegue)


def test_pliegues_cada_fila_valida_una_vez():
    df = ml.entregas_curvas(n=53).ent
    part = ml.pliegues(df, k=5, semilla=2)
    assert len(part) == 5
    validas = np.concatenate([v for _, v in part])
    assert sorted(validas) == list(range(len(df)))
    for ajuste, valida in part:
        assert not set(ajuste) & set(valida) and len(ajuste) + len(valida) == len(df)
    y = pd.DataFrame({"y": np.r_[np.ones(6, int), np.zeros(54, int)]})
    for semilla in range(30):
        est = ml.pliegues(y, k=5, como="estratificado", semilla=semilla)
        assert all(y["y"].iloc[v].sum() > 0 for _, v in est)
    for como in ("grupo", "temporal"):
        with pytest.raises(NotImplementedError, match="clase 5"):
            ml.pliegues(df, como=como)
    with pytest.raises(ValueError):
        ml.pliegues(df, como="azar", estratificar=True)


def test_rehacer_cambia_la_muestra_no_la_poblacion():
    datos = ml.entregas_curvas()
    otra = datos.rehacer(5)
    assert not otra.ent.equals(datos.ent) and otra.realidad is None
    con = datos.rehacer(5, True)
    pd.testing.assert_frame_equal(con.despliegue, datos.despliegue)
    assert con.ent.equals(otra.ent)
    assert ml.caso(13).rehacer(1, True).despliegue.equals(ml.caso(13).despliegue)
    with pytest.raises(ValueError):
        ml.Datos(*[None] * 20).rehacer(1)


def test_entregas_curvas_hilo_de_la_clase_2():
    datos = ml.entregas_curvas()
    assert len(datos.ent) == 36 and datos.sigma2_e == pytest.approx(9)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s = ml.elegir(datos, _polis(range(13)), con="cv")
        m12 = _polis([12])[12](datos.ent)
    assert 3 <= s.elegido <= 6
    assert ml.L(m12, datos.val) / ml.L(m12, datos.ent) >= 2
    x = np.linspace(0, 6, 601)
    f = datos.f(pd.DataFrame({"x": x}))
    fuera = (x < 3) | (x > 4)  # creciente salvo la bajada de la joroba (3.2 a 3.96 km)
    assert np.all(np.diff(f)[fuera[1:]] > 0)
    assert f[0] == pytest.approx(10 + 4 * np.exp(-18))
    assert ml.entregas_curvas(sigma_e=1).sigma2_e == pytest.approx(1)
    plano = ml.entregas_curvas(joroba=0)
    assert np.allclose(plano.f(pd.DataFrame({"x": [3.0]})), 10 + 12 * np.log(4))
    assert "lineal" not in ml.PROCESOS


@pytest.mark.parametrize("numero,cambios", [
    (13, {"persistencia": 0.5, "n": 120}), (13, {"separar": "tiempo"}),
    (14, {"desv_grupo": 2, "n_grupos": 12}), (14, {"separar": "grupo"}),
    (15, {"n": 60}), (16, {"semilla": 3}),
])
def test_casos_13_a_16_existen_corren_y_aceptan_cambios(numero, cambios):
    caso = ml.CASOS_BORDE[numero]
    assert caso.clase == 2 and caso.pregunta.endswith("?") and caso.que_se_ve
    datos = ml.caso(numero, n_realidad=3000, **cambios)
    assert datos.tarea == "regresion" and len(datos.ent) > 0
    assert ml.caso(caso.nombre, n_realidad=3000, **cambios).ent.equals(datos.ent)
    m = ml.ajustar(datos, phi=ml.polinomio(2))
    assert np.isfinite(ml.riesgo(m, datos))
    if numero == 16:
        assert (datos.ent["x"] > 5.5).sum() == 2 and (datos.ent["x"] <= 4).sum() == 48


def test_polinomio_cero_es_la_media():
    datos = ml.entregas_curvas()
    m = ml.ajustar(datos, phi=ml.polinomio(0))
    assert list(m.beta_gorro.index) == ["1"]
    assert m.beta_gorro["1"] == pytest.approx(datos.ent["y"].mean())
    with pytest.raises(ValueError, match="intercepto"):
        ml.ajustar(datos, phi=ml.polinomio(0), intercepto=False)


def test_validacion_cruzada_perdidas_fuera_reproducen_cada_pliegue():
    datos = ml.entregas_curvas()
    r = ml.validacion_cruzada(datos, _polis([4])[4], k=5)
    desarrollo = pd.concat([datos.ent, datos.val])
    assert len(r.perdidas_fuera) == len(desarrollo) and len(r.por_pliegue) == 5
    for (_, valida), valor in zip(r.pliegues, r.por_pliegue):
        assert r.perdidas_fuera[valida].mean() == pytest.approx(valor)
    assert r.media == pytest.approx(np.mean(r.por_pliegue))
    assert r.ee == pytest.approx(np.std(r.por_pliegue, ddof=1) / np.sqrt(5))
    assert r.por_pliegue_estadistico is None
    assert "no se pasan a\n    diferencia_pareada" in ml.validacion_cruzada.__doc__


def test_validacion_cruzada_estadistico_etiquetas_y_nan():
    """Contrato v5 §5.9 (r3-13): etiquetas, nan tal cual, sin fallar."""
    datos = ml.proceso_clasificacion(n=200, separar="azar", fracciones=(1, 0, 0))
    df = datos.ent
    positivos = np.flatnonzero(df["y"].to_numpy() == 1)
    negativos = np.flatnonzero(df["y"].to_numpy() == 0)
    sin_positivos = negativos[:20]
    resto = np.setdiff1d(np.arange(len(df)), sin_positivos)
    trozos = np.array_split(resto, 4)
    part = [(np.setdiff1d(np.arange(len(df)), sin_positivos), sin_positivos)] + [
        (np.setdiff1d(np.arange(len(df)), t), t) for t in trozos]
    assert len(positivos) > 0
    vistos = []

    def estadistico(y, y_gorro):
        vistos.append(np.asarray(y_gorro))
        return float("nan") if not np.any(y == 1) else float(np.mean(y_gorro))

    r = ml.validacion_cruzada(df, lambda d: ml.ajustar(d), particion=lambda d: part,
                              estadistico=estadistico)
    est = r.por_pliegue_estadistico
    assert np.isnan(est[0]) and np.all(np.isfinite(est[1:]))
    assert set(np.unique(np.concatenate(vistos))) <= {0, 1}


def test_diferencia_pareada_y_por_pliegue():
    a = np.array([1.0, 2.0, 4.0])
    assert ml.diferencia_pareada(a, a) == (0.0, 0.0)
    media, ee = ml.diferencia_pareada(a, np.zeros(3))
    assert media == pytest.approx(7 / 3) and ee == pytest.approx(np.std(a, ddof=1) / np.sqrt(3))
    with pytest.raises(ValueError, match="mismo largo"):
        ml.diferencia_pareada(a, a[:2])
    datos = ml.entregas_curvas()
    c = _polis([1, 4])
    r1 = ml.validacion_cruzada(datos, c[1], k=5)
    r4 = ml.validacion_cruzada(datos, c[4], k=5)
    tabla = ml.diferencia_por_pliegue(r4, r1)
    assert list(tabla["pliegue"]) == [1, 2, 3, 4, 5, "media"]
    assert tabla["diferencia"].iloc[-1] == pytest.approx(r4.media - r1.media)
    assert "descriptivo" in tabla.attrs["nota"]
    otra = ml.validacion_cruzada(datos, c[1], k=5, semilla=7)
    with pytest.raises(ValueError, match="misma partición"):
        ml.diferencia_por_pliegue(r4, otra)


def test_contraejemplo_del_ee_pareado_en_cv():
    """Contrato §5.9 / ml-c3-def-benchmark (b): dos respuestas ±1, CV dejando una fuera,
    predictor 0 contra la media de entrenamiento. Las dos diferencias por pliegue son
    siempre iguales (s_d/√2 = 0) y la desviación real de su media es 2."""
    medias = []
    for y1 in (-1.0, 1.0):
        for y2 in (-1.0, 1.0):
            df = pd.DataFrame({"x": [0.0, 1.0], "y": [y1, y2]})
            part = lambda d: [(np.array([1]), np.array([0])), (np.array([0]), np.array([1]))]  # noqa: E731
            cero = ml.validacion_cruzada(df, lambda d: _Constante(0), particion=part)
            media = ml.validacion_cruzada(df, lambda d: _Constante(d["y"].mean()), particion=part)
            tabla = ml.diferencia_por_pliegue(cero, media)
            d = tabla["diferencia"].iloc[:2].to_numpy(float)
            assert d[0] == d[1]
            assert np.std(d, ddof=1) / np.sqrt(2) == 0
            medias.append(tabla["diferencia"].iloc[-1])
    assert sorted(medias) == [-3, -3, 1, 1]
    assert np.std(medias) == pytest.approx(2.0)


def test_elegir_semantica_de_contrato():
    datos = ml.entregas_curvas()
    c = _polis(range(9))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cv = ml.elegir(datos, c, con="cv", k=5)
        val = ml.elegir(datos, c, con="val")
        ent = ml.elegir(datos, c, con="ent")
        un = ml.elegir(datos, c, con="cv", regla="un_ee")
    # tabla, costo y cv
    assert list(cv.tabla.columns) == ["candidato", "valor", "ee"]
    assert cv.costo_ajustes == 9 * 5 + 1 and cv.con == "cv"
    for N in c:
        assert len(cv.cv[N].por_pliegue) == 5
        assert cv.cv[N].media == pytest.approx(cv.tabla.set_index("candidato").loc[N, "valor"])
    # modelo_final: con val reajusta con ent ∪ val; con cv es el mismo objeto
    n_ent, n_val = len(datos.ent), len(datos.val)
    assert cv.modelo_final is cv.modelo
    assert val.modelo is not val.modelo_final and val.cv is None and val.con == "val"
    desarrollo = pd.concat([datos.ent, datos.val])
    esperado = c[val.elegido](desarrollo).beta_gorro
    assert np.allclose(val.modelo_final.beta_gorro, esperado)
    assert np.allclose(val.modelo.beta_gorro, c[val.elegido](datos.ent).beta_gorro)
    assert n_ent + n_val == len(desarrollo)
    # entrenamiento elige el más complejo; la regla de un EE, uno igual o más simple
    assert ent.elegido == 8
    assert un.elegido_un_ee <= un.elegido
    v = un.tabla.set_index("candidato")
    umbral = v.loc[un.elegido, "valor"] + v.loc[un.elegido, "ee"]
    assert v.loc[un.elegido_un_ee, "valor"] <= umbral
    assert all(v.loc[N, "valor"] > umbral for N in c if N < un.elegido_un_ee)
    with pytest.warns(UserWarning, match="prueba"):
        ml.elegir(datos, c, con="prueba")
    with pytest.raises(ValueError, match="un EE"):
        ml.elegir(datos, c, con="val", regla="un_ee")


def test_elegir_empate_al_mas_simple():
    datos = ml.entregas_curvas()
    cands = {"a": lambda df: _Constante(25), "b": lambda df: _Constante(25),
             "c": lambda df: _Constante(100)}
    for con in ("ent", "val", "cv"):
        assert ml.elegir(datos, cands, con=con).elegido == "a"
    orden = ml.elegir(datos, cands, con="cv", orden_complejidad=["b", "a", "c"])
    assert orden.elegido == "b"


def test_cv_anidada_y_optimismo():
    datos = ml.entregas_curvas(n=80)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = ml.cv_anidada(datos, _polis(range(6)), k_externo=4, k_interno=3)
    assert len(r.por_pliegue) == 4 and np.isfinite(r.media)
    assert np.all(np.isfinite(r.perdidas_fuera))
    fab = lambda s: ml.entregas_curvas(semilla=s, con_realidad=False)  # noqa: E731
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        largo = ml.optimismo_por_seleccion(fab, _polis(range(5)), repeticiones=6, detalle=True)
        corto = ml.optimismo_por_seleccion(fab, _polis(range(5)), repeticiones=6)
    assert list(largo.columns) == ["repeticion", "candidato", "L_ent", "L_val", "L_prueba", "R",
                                   "R_final", "L_prueba_final"]
    assert (largo["R_final"] != largo["R"]).any()
    for _, fila in corto.iterrows():
        g = largo[largo.repeticion == fila["repeticion"]]
        assert fila["con_prueba"] == g["L_prueba"].min()
        assert fila["con_val_y_prueba"] == g.loc[g["L_val"].idxmin(), "L_prueba"]
        assert fila["R_real"] == g.loc[g["L_prueba"].idxmin(), "R"]


def test_sesgo_varianza_suma_y_curva_de_aprendizaje():
    datos = ml.entregas_curvas()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sv = ml.sesgo_varianza(datos.rehacer, _polis([1, 4]), repeticiones=20)
    t = sv.tabla.set_index("candidato")
    assert t.loc[1, "ruido"] == pytest.approx(9)
    assert np.allclose(t["total"], t["ruido"] + t["sesgo2"] + t["varianza"])
    P = sv.predicciones[4]
    assert P.shape == (20, len(sv.malla))
    assert t.loc[4, "sesgo2"] + t.loc[4, "varianza"] == pytest.approx(
        np.mean((P - sv.verdad) ** 2))
    assert t.loc[1, "sesgo2"] > t.loc[4, "sesgo2"]
    fab = lambda s: ml.entregas_curvas(n=240, semilla=s, con_realidad=False)  # noqa: E731
    tabla = ml.curva_aprendizaje(fab, _polis([1, 4]), ns=[30, 240], repeticiones=3)
    assert list(tabla.columns) == ["candidato", "n", "repeticion", "L_ent", "R"]
    assert len(tabla) == 2 * 2 * 3
    with pytest.raises(ValueError, match="filas"):
        ml.curva_aprendizaje(fab, _polis([1]), ns=[500], repeticiones=1)


def test_capacidad_elegida_sube_con_n_en_el_hilo():
    fab = lambda s: ml.entregas_curvas(n=960, semilla=s, con_realidad=False)  # noqa: E731
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tabla = ml.capacidad_elegida(fab, _polis(range(11)), ns=[30, 960], repeticiones=8)
    assert list(tabla.columns) == ["n", "repeticion", "elegido"]
    med = tabla.groupby("n")["elegido"].median()
    assert med[960] >= med[30]


def test_reparto_error_es_L_prueba_menos_R():
    fab = lambda s: ml.entregas_curvas(n=120, semilla=s, con_realidad=False)  # noqa: E731
    tabla = ml.reparto(fab, _polis([3])[3], fracciones_prueba=(0.1, 0.5), repeticiones=3)
    assert list(tabla.columns) == ["fraccion", "repeticion", "R", "L_prueba", "error", "ee"]
    assert np.allclose(tabla["error"], tabla["L_prueba"] - tabla["R"])
    fig = ml.dibujar_reparto(tabla, marca=0.1)
    assert len(fig.axes) == 2
    assert any(ln.get_gid() == "marca" for ln in fig.axes[1].get_lines())


# --- gráficas de la clase 2 ---


def _gids(ax):
    return [a.get_gid() for a in ax.get_children() if a.get_gid()]


def test_dibujar_cv_cubre_los_cuatro_con():
    datos = ml.entregas_curvas()
    c = _polis(range(9))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sel = {con: ml.elegir(datos, c, con=con) for con in ("ent", "val", "cv", "prueba")}
    # cv: un umbral horizontal en CV(mín) + EE(mín), marcas sobre los puntos, sin verticales
    ax = ml.dibujar_cv(sel["cv"])
    s = sel["cv"].tabla.set_index("candidato")
    umbral = [ln for ln in ax.get_lines() if ln.get_gid() == "umbral"]
    assert len(umbral) == 1
    assert umbral[0].get_ydata()[0] == pytest.approx(s.loc[sel["cv"].elegido, "valor"]
                                                     + s.loc[sel["cv"].elegido, "ee"])
    for gid, cand in (("elegido", sel["cv"].elegido), ("elegido-un-ee", sel["cv"].elegido_un_ee)):
        ln = next(ln for ln in ax.get_lines() if ln.get_gid() == gid)
        assert ln.get_xdata()[0] == cand and ln.get_ydata()[0] == pytest.approx(s.loc[cand, "valor"])
    assert not any(np.allclose(*ln.get_xdata()[:2]) for ln in ax.get_lines()
                   if len(ln.get_xdata()) == 2 and ln.get_gid() not in ("piso", "benchmark"))
    assert not {"R", "L_ent", "piso", "benchmark"} & set(_gids(ax))
    serie = next(ln for ln in ax.get_lines() if ln.get_gid() == "serie-cv")
    assert serie.get_marker() == "^"
    assert "CV_k" in [t.get_text() for t in ax.get_legend().get_texts()]
    # val: triángulos sin barras ni umbral; ent: círculos y aviso si llega L_ent; prueba: cuadrados
    ax = ml.dibujar_cv(sel["val"])
    serie = next(ln for ln in ax.get_lines() if ln.get_gid() == "serie-val")
    assert serie.get_marker() == "^" and serie.get_label() == "L_val"
    assert "umbral" not in _gids(ax) and not ax.collections
    with pytest.warns(UserWarning, match="L_ent"):
        ax = ml.dibujar_cv(sel["ent"], L_ent={N: 1.0 for N in c})
    assert [ln.get_marker() for ln in ax.get_lines() if ln.get_gid() == "serie-ent"] == ["o"]
    assert "L_ent" not in _gids(ax)
    ax = ml.dibujar_cv(sel["prueba"], R={N: 10.0 for N in c}, piso=9.0, benchmark=(60, 2))
    assert [ln.get_marker() for ln in ax.get_lines() if ln.get_gid() == "serie-prueba"] == ["s"]
    assert {"R", "piso", "benchmark"} <= set(_gids(ax))


def test_dibujar_pliegues_dibuja_la_particion_usada():
    y = pd.DataFrame({"y": np.r_[np.ones(3, int), np.zeros(57, int)]})
    part = ml.pliegues(y, k=5, como="estratificado")
    ax = ml.dibujar_pliegues(60, 5, y=y["y"], particion=part)
    assert "2 de 5" in ax.get_title()  # 3 positivos y 5 pliegues: dos sin ninguno (palomar)
    for m, (_, val) in enumerate(part, start=1):
        barras = [b for b in ax.collections if b.get_gid() == f"valida-{m}"]
        cubiertas = set()
        for b in barras:
            for camino in b.get_paths():
                xs = camino.vertices[:, 0]
                cubiertas |= set(range(int(round(xs.min())), int(round(xs.max()))))
        assert cubiertas == set(int(v) for v in val)
    with pytest.raises(ValueError, match="pliegues"):
        ml.dibujar_pliegues(60, 4, particion=part)
    ml.dibujar_pliegues(48, 5, m_activo=2, prueba=True)


def test_dibujar_histograma_estimaciones_una_o_varias_series():
    rng = np.random.default_rng(0)
    ax = ml.dibujar_histograma_estimaciones({"con prueba": rng.normal(size=200),
                                             "con validación": rng.normal(1, 1, 200)},
                                            verdadero=0, etiqueta="anunciado − real")
    assert [ln.get_gid() for ln in ax.get_lines()].count("verdadero") == 1
    assert {"serie-con prueba", "serie-con validación"} <= set(_gids(ax))
    v = rng.normal(size=100)
    a1 = ml.dibujar_histograma_estimaciones(v, verdadero=0.5, etiqueta="L_prueba")
    a2 = ml.dibujar_histograma_estimaciones({"L_prueba": v}, verdadero=0.5, etiqueta="L_prueba")
    caminos = lambda ax: [p.get_path().vertices.tolist() for p in ax.patches]  # noqa: E731
    assert caminos(a1) == caminos(a2)


def test_dibujar_cajas_pliegues_con_seleccion_y_con_estadistico():
    datos = ml.entregas_curvas()
    sel = ml.elegir(datos, _polis([1, 4]), con="cv")
    ax = ml.dibujar_cajas_pliegues(sel)
    puntos = next(ln for ln in ax.get_lines() if ln.get_gid() == "pliegues-4")
    assert np.allclose(puntos.get_ydata(), sel.cv[4].por_pliegue)
    res = {N: ml.validacion_cruzada(datos, f, estadistico=lambda y, g: float(np.mean(y - g)))
           for N, f in _polis([1, 4]).items()}
    ax = ml.dibujar_cajas_pliegues(res, estadistico=True)
    puntos = next(ln for ln in ax.get_lines() if ln.get_gid() == "pliegues-1")
    assert np.allclose(puntos.get_ydata(), res[1].por_pliegue_estadistico)


def test_dibujar_diana_pone_cada_marca_en_su_valor():
    datos = ml.entregas_curvas()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sv = ml.sesgo_varianza(datos.rehacer, _polis([1, 6]), repeticiones=10)
    ax = ml.dibujar_diana(sv, 5.0, candidatos=[1, 6])
    marcas = [ln for ln in ax.get_lines() if ln.get_gid() == "repeticion"]
    punto = pd.DataFrame({"x": [5.0]})
    for ln, N in zip(marcas, (1, 6)):
        esperado = [_polis([N])[N](datos.rehacer(s).ent).predecir(punto)[0] for s in range(10)]
        esperado[0] = _polis([N])[N](datos.ent).predecir(punto)[0]
        assert np.allclose(ln.get_xdata(), esperado)
    verde = next(ln for ln in ax.get_lines() if ln.get_gid() == "f")
    assert verde.get_xdata()[0] == pytest.approx(datos.f(punto)[0])
    ml.dibujar_abanico(sv, 6)
    ml.dibujar_sesgo_varianza(sv)


def test_dibujar_curva_aprendizaje_media_o_mediana():
    tabla = pd.DataFrame({"candidato": [1] * 6, "n": [30, 30, 30, 60, 60, 60],
                          "repeticion": [0, 1, 2] * 2, "L_ent": [1, 2, 9, 1, 1, 7.0],
                          "R": [3, 4, 30, 2, 2, 20.0]})
    for resumen, f in (("media", np.mean), ("mediana", np.median)):
        ax = ml.dibujar_curva_aprendizaje(tabla, piso=1.0, resumen=resumen)
        R = next(ln for ln in ax.get_lines() if ln.get_gid() == "R-1")
        assert np.allclose(R.get_ydata(), [f([3, 4, 30]), f([2, 2, 20])])
    elegido = pd.DataFrame({"n": [30, 30, 60, 60], "repeticion": [0, 1, 0, 1],
                            "elegido": [2, 3, 4, 6]})
    fig = ml.dibujar_curva_aprendizaje(tabla, elegido=elegido)
    assert len(fig.axes) == 2
    assert inspect.signature(ml.dibujar_curva_aprendizaje).parameters["resumen"].default == "media"


def test_dibujar_contratos_igual_con_estimado_y_un_panel_por_modelo():
    tabla = pd.DataFrame({"contrato": ["igual", "el mes que viene"],
                          "separacion": ["azar", "azar"], "L_prueba": [10.0, 60.0],
                          "R": [11.0, 130.0], "benchmark": [60.0, 140.0]})
    a1 = ml.dibujar_contratos(tabla, resaltar="el mes que viene")
    a2 = ml.dibujar_contratos(tabla.rename(columns={"L_prueba": "estimado"}),
                              resaltar="el mes que viene")
    barras = lambda ax: [(p.get_x(), p.get_height()) for p in ax.patches]  # noqa: E731
    lineas = lambda ax: [(ln.get_gid(), list(ln.get_xydata().ravel())) for ln in ax.get_lines()]  # noqa: E731
    assert barras(a1) == barras(a2) and lineas(a1) == lineas(a2)
    assert [h for _, h in barras(a1)] == [10.0, 60.0]
    assert [ln.get_ydata()[0] for ln in a1.get_lines() if ln.get_gid() == "R"] == [11.0, 130.0]
    doble = pd.concat([tabla.assign(modelo="lineal"), tabla.assign(modelo="vecinos")])
    fig = ml.dibujar_contratos(doble)
    assert len(fig.axes) == 2


def test_taller_y_galeria_de_la_clase_2(monkeypatch):
    import time
    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    s = io.StringIO()
    inicio = time.time()
    with redirect_stdout(s):
        ml.taller(ml.entregas_curvas(), 2, que="elegir")
    assert time.time() - inicio < 10
    texto = s.getvalue()
    for conjunto in ("CV_5 sobre ent ∪ val", "prueba:", "despliegue:"):
        assert conjunto in texto
    with redirect_stdout(io.StringIO()):
        ml.taller(ml.entregas_curvas(), 2, que="descomponer")
    s = io.StringIO()
    with redirect_stdout(s):
        ml.galeria(2)
    assert ml.CASOS_BORDE[13].pregunta in s.getvalue()
    for numero in (14, 15, 16):
        with redirect_stdout(io.StringIO()):
            ml.galeria(2, casos=[numero])


# --- revisión adversarial del lote c2 (codex-rev-lab-c2): cada prueba falló antes ---


def test_efecto_grupo_piso_es_el_de_sus_pacientes():
    uno = ml.proceso(n=40, f=lambda d: 0 * d["x"], ruido=ml.efecto_grupo(1, 4, 0), n_realidad=2000)
    assert np.allclose(uno.realidad["y"], uno.realidad["y"].iloc[0])
    assert ml.piso(uno) == pytest.approx(0)
    mec = ml.efecto_grupo(24, 4, 1)
    efectos = mec._efecto(np.arange(24))
    assert efectos.mean() == pytest.approx(0, abs=1e-12) and efectos.std() == pytest.approx(4)
    d = ml.caso(14, n_realidad=24_000)
    assert d.realidad["y"].sub(d.realidad["f"]).mean() == pytest.approx(0, abs=0.05)


@pytest.mark.parametrize("particion, patron", [
    (lambda d: [([0, 1], [0, 1]), ([2, 3], [2, 3])], "fuga"),
    (lambda d: [([1, 2, 3], [0, 1]), ([0, 2, 3], [1])], "fuga"),
    (lambda d: [([2, 3], [0, 1]), ([0, 3], [1, 2])], "dos pliegues"),
    (lambda d: [([1, 2], []), ([0], [1])], "vacío"),
    (lambda d: [([1, 2, 9], [0])], "fuera"),
])
def test_validacion_cruzada_rechaza_particiones_con_fuga(particion, patron):
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [1.0, 2, 3, 4]})
    with pytest.raises(ValueError, match=patron):
        ml.validacion_cruzada(df, lambda d: _Constante(0), particion=particion)


def test_validacion_cruzada_temporal_deja_nan_en_lo_que_no_valida():
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [1.0, 2, 3, 4]})
    r = ml.validacion_cruzada(df, lambda d: _Constante(0),
                              particion=lambda d: [([0], [1]), ([0, 1], [2, 3])])
    assert np.isnan(r.perdidas_fuera[0]) and np.allclose(r.perdidas_fuera[1:], [4, 9, 16])


def test_sesgo_varianza_no_inventa_el_ruido_con_omitidas_y_contexto():
    fab = lambda s: ml.proceso(n=60, x={"x": ml.normal(), "z": ml.normal()},  # noqa: E731
                               f=lambda d: d["z"], ruido=ml.ar1(0, 1), omitir=["z"],
                               semilla=s, n_realidad=2000)
    with pytest.raises(ValueError, match="Var"):
        ml.sesgo_varianza(fab, _polis([1]), repeticiones=2)


def test_deriva_que_cambia_de_estado_no_sale_de_la_cache():
    estado = {"a": 4.0}
    deriva = lambda t: {"x": ml.uniforme(estado["a"], estado["a"] + 1)}  # noqa: E731
    base = dict(n=20, despliegue="otra_poblacion", deriva=deriva, n_realidad=500)
    assert ml.proceso(**base).despliegue["x"].min() >= 4
    estado["a"] = 10.0
    assert ml.proceso(**base).despliegue["x"].min() >= 10


def test_optimismo_salta_candidatos_sin_valor_finito():
    fab = lambda s: ml.entregas_curvas(semilla=s, n_realidad=2000)  # noqa: E731
    cands = {"nan": lambda df: _Constante(float("nan")), "25": lambda df: _Constante(25)}
    corto = ml.optimismo_por_seleccion(fab, cands, repeticiones=2)
    assert np.isfinite(corto[["con_prueba", "con_val_y_prueba", "R_real", "R_val"]]).all().all()


def test_misma_particion_exige_mismo_ajuste_y_dibujar_pliegues_lo_dibuja_tal_cual():
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [1.0, 2, 3, 4]})
    p1 = lambda d: [([1], [0, 2]), ([0], [1, 3])]  # noqa: E731
    p2 = lambda d: [([1, 3], [0, 2]), ([0, 2], [1, 3])]  # noqa: E731
    a = ml.validacion_cruzada(df, lambda d: _Constante(0), particion=p1)
    b = ml.validacion_cruzada(df, lambda d: _Constante(0), particion=p2)
    with pytest.raises(ValueError, match="misma partición"):
        ml.diferencia_por_pliegue(a, b)
    ax = ml.dibujar_pliegues(4, 2, particion=p1(df), prueba=False)
    cubiertas = set()
    for barra in (b for b in ax.collections if b.get_gid() == "ajuste-1"):
        for camino in barra.get_paths():
            xs = camino.vertices[:, 0]
            cubiertas |= set(range(int(round(xs.min())), int(round(xs.max()))))
    assert cubiertas == {1}


def test_reparto_nunca_deja_el_entrenamiento_vacio():
    fab = lambda s: ml.entregas_curvas(n=10, semilla=s, n_realidad=500)  # noqa: E731
    tabla = ml.reparto(fab, _polis([0])[0], fracciones_prueba=(0.99,), repeticiones=1)
    assert np.isfinite(tabla["R"]).all()


def test_cv_anidada_elige_dentro_de_cada_pliegue_externo():
    datos = ml.entregas_curvas(n=80)
    c = _polis(range(6))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = ml.cv_anidada(datos, c, k_externo=4, k_interno=3)
        df = pd.concat([datos.ent, datos.val])
        df.attrs = datos.ent.attrs
        esperado = []
        for ajuste, valida in ml.pliegues(df, k=4, semilla=0):
            dentro = df.iloc[ajuste].copy()
            dentro.attrs = df.attrs
            s = ml.elegir(dentro, c, con="cv", k=3, semilla=1)
            esperado.append(ml.L(s.modelo, df.iloc[valida]))
            assert len(s.modelo.beta_gorro) == s.elegido + 1
    assert np.allclose(r.por_pliegue, esperado)
    plano = ml.validacion_cruzada(df, c[0], k=4)
    assert not np.allclose(r.por_pliegue, plano.por_pliegue)


# --- revisión adversarial del lote c2, ronda 2 (codex-rev-lab-c2.i2): cada prueba falló antes ---


def test_piso_junta_f_y_efecto_grupo_cuando_f_usa_el_grupo():
    # f = ±4 por grupo y los efectos estandarizados de 2 grupos son ∓4: y = 0 siempre
    d = ml.proceso(n=200, f=lambda d: 4 * (2 * d["grupo"] - 1), ruido=ml.efecto_grupo(2, 4, 0),
                   n_realidad=4000)
    desp = d.despliegue
    assert np.allclose(desp["y"], 0)
    assert ml.piso(d) == pytest.approx(0, abs=1e-12)
    assert np.allclose(desp["f_visible"], 0) and np.allclose(d.f_visible(desp), 0)
    assert np.allclose(d.f_visible(desp[["x"]]), 0)  # sin grupo: el grupo no es visible
    # f que usa x y el grupo: el piso es E[Var_g(f + efecto)] + desv², y es alcanzable
    d = ml.proceso(n=200, f=lambda d: d["x"] + d["grupo"], ruido=ml.efecto_grupo(4, 1, 1),
                   n_realidad=40_000)
    mec = ml.efecto_grupo(4, 1, 1)
    esperado = np.var(np.arange(4) + mec._efecto(np.arange(4))) + 1
    assert ml.piso(d) == pytest.approx(esperado, rel=1e-9)
    L = np.mean((d.despliegue["y"] - d.despliegue["f_visible"]) ** 2)
    assert L == pytest.approx(esperado, rel=0.03)


def test_piso_desconocido_si_f_usa_el_grupo_y_no_se_puede_juntar():
    with pytest.warns(UserWarning, match="piso desconocido"):
        nuevos = ml.proceso(n=200, f=lambda d: d["x"] * d["grupo"], ruido=ml.efecto_grupo(3, 1, 1),
                            despliegue="grupos_nuevos", n_realidad=2000)
        assert np.isnan(ml.piso(nuevos))
    with pytest.warns(UserWarning, match="piso desconocido"):
        omitida = ml.proceso(n=200, x={"x": ml.uniforme(), "z": ml.uniforme()}, omitir=["z"],
                             f=lambda d: d["x"] + d["z"] * d["grupo"],
                             ruido=ml.efecto_grupo(3, 1, 1), n_realidad=2000)
        assert np.isnan(ml.piso(omitida))
    assert np.isnan(omitida.f_visible(omitida.despliegue.head(3))).all()
    # si f no usa el grupo, nada cambia: el caso 14 y el de grupos nuevos
    assert ml.piso(ml.proceso(n=240, ruido=ml.efecto_grupo(24, 4, 1), n_realidad=2000)) == 17


def test_varianza_en_distingue_grupos_propios_de_nuevos():
    mec = ml.efecto_grupo(1, 4, 1)
    v = mec.varianza_en(pd.DataFrame({"grupo": [0, 0, 1, 5]}))
    assert list(v) == [1, 1, 17, 17]
    v24 = ml.efecto_grupo(24, 4, 1).varianza_en(pd.DataFrame({"grupo": [0, 23, 24]}))
    assert list(v24) == [17, 17, 17]
    igual = ml.proceso(n=240, ruido=ml.efecto_grupo(1, 4, 1), n_realidad=2000)
    nuevos = ml.proceso(n=240, ruido=ml.efecto_grupo(1, 4, 1), despliegue="grupos_nuevos",
                        n_realidad=2000)
    assert ml.piso(igual) == pytest.approx(1) and ml.piso(nuevos) == pytest.approx(17)


@pytest.mark.parametrize("particion", [
    lambda d: [([1, 2, 3], [0]), ([0, 2, 3], [1])],      # omite 2 y 3, y no va hacia adelante
    lambda d: [([0], [1]), ([0, 1, 2], [3])],            # la fila 2 no valida y no es de las primeras
    lambda d: [([1], [0]), ([0, 1], [2, 3])],            # el pliegue 1 ajusta con el futuro
])
def test_validacion_cruzada_exige_que_cada_fila_valide_una_vez(particion):
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [0.0, 0, 20, 30]})
    with pytest.raises(ValueError, match="exactamente una vez"):
        ml.validacion_cruzada(df, lambda d: _Constante(0), particion=particion)


def test_validacion_cruzada_hacia_adelante_sigue_el_orden_de_t():
    df = pd.DataFrame({"x": [0.0, 1, 2, 3], "t": [3, 2, 1, 0], "y": [1.0, 2, 3, 4]})
    r = ml.validacion_cruzada(df, lambda d: _Constante(0),
                              particion=lambda d: [([3], [2]), ([3, 2], [1, 0])])
    assert np.isnan(r.perdidas_fuera[3]) and np.allclose(r.perdidas_fuera[:3], [1, 4, 9])
    with pytest.raises(ValueError, match="exactamente una vez"):  # hacia adelante en filas, no en t
        ml.validacion_cruzada(df, lambda d: _Constante(0),
                              particion=lambda d: [([0], [1]), ([0, 1], [2, 3])])


def test_dibujar_cv_prefiere_el_riesgo_de_despliegue():
    tabla = pd.DataFrame({"candidato": [1, 4, 1, 4], "conjunto": ["realidad"] * 2 + ["despliegue"] * 2,
                          "L": [15.15, 9.65, 36.39, 258.25], "ee": [0.1] * 4})
    sel = ml.Seleccion(tabla=pd.DataFrame({"candidato": [1, 4], "valor": [20.0, 12.0],
                                           "ee": [1.0, 1.0]}),
                       elegido=4, elegido_un_ee=4, modelo=None, modelo_final=None,
                       criterio="cuadratica", sentido="min", costo_ajustes=11, cv=None, con="cv")
    ax = ml.dibujar_cv(sel, R=tabla)
    (r,) = [ln for ln in ax.get_lines() if ln.get_gid() == "R"]
    assert list(r.get_ydata()) == [36.39, 258.25]
    ax = ml.dibujar_cv(sel, R=tabla[tabla["conjunto"] == "realidad"])
    (r,) = [ln for ln in ax.get_lines() if ln.get_gid() == "R-origen"]
    assert list(r.get_ydata()) == [15.15, 9.65] and "origen" in r.get_label()


def test_dibujar_pliegues_rechaza_una_particion_de_otro_n():
    df4 = pd.DataFrame({"x": [0.0, 1, 2, 3], "y": [1.0, 2, 3, 4]})
    with pytest.raises(ValueError, match="otro n"):
        ml.dibujar_pliegues(8, 2, particion=ml.pliegues(df4, k=2))
    with pytest.raises(ValueError, match="otro n"):
        ml.dibujar_pliegues(3, 2, particion=ml.pliegues(df4, k=2))
    ml.dibujar_pliegues(4, 2, particion=ml.pliegues(df4, k=2))


# ---------------------------------------------------------------------------
# 1.3 · el lote de la clase 3 (clase_3.md §10.7.2, contrato §5.4–§5.12, §5.15 C)

NUEVAS_1_3 = [
    "t_student", "cauchy", "pareto", "lognormal", "heterocedastico", "muchas_variables",
    "interacciones", "estandarizar", "mae", "rmse", "r2", "peores_errores", "trayectorias",
    "optimo_restringido", "encoger_1d", "beta_repetido", "dibujar_benchmarks",
    "dibujar_media_acumulada", "dibujar_peso_de_filas", "dibujar_residuales_plano",
    "dibujar_beta_repetido", "dibujar_encoger_1d", "dibujar_trayectorias", "dibujar_regiones",
    "dibujar_presupuesto",
]
VERSION_1_2 = "d05c81b"  # el commit de ml_lab 1.2 contra el que se comparan las ampliaciones


def _calla(funcion, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return funcion(*args, **kwargs)


def test_las_funciones_de_1_3_dicen_desde_cuando():
    for nombre in NUEVAS_1_3:
        assert nombre in ml.__all__, nombre
        assert "Desde: 1.3 (clase 3)" in getattr(ml, nombre).__doc__, nombre
    assert "(1.3)" in ml.dibujar_cv.__doc__
    assert set(ml.ANALISIS_TALLER) >= {3}
    assert {6, 7, 8, 9, 10, 11, 12, 24} <= set(ml.CASOS_BORDE)
    for n in (6, 7, 8, 9, 10, 11, 12, 24):
        assert ml.CASOS_BORDE[n].clase == 3


# --- piezas y piso ---------------------------------------------------------

def test_piezas_de_cola_larga_y_sus_momentos():
    t3, t2, c, p, ln = ml.t_student(3), ml.t_student(2), ml.cauchy(), ml.pareto(1.5), ml.lognormal(0, 1)
    assert t3.varianza == pytest.approx(3.0) and t3.media == 0
    assert np.isinf(t2.varianza) and np.isinf(c.varianza) and np.isinf(p.varianza)
    assert ml.pareto(3.0).varianza == pytest.approx(3 / (4 * 1))
    assert np.isnan(c.media) and p.media == 0
    assert ln.media == pytest.approx(np.exp(0.5)) and ln.varianza == pytest.approx((np.e - 1) * np.e)
    rng = np.random.default_rng(0)
    # centrar resta la media: la media muestral de Pareto(3) con 10⁶ filas está cerca de 0
    assert abs(ml.pareto(3.0).muestrear(1_000_000, rng).mean()) < 0.01
    assert np.median(ml.pareto(1.5).muestrear(200_001, rng)) == pytest.approx(2 ** (1 / 1.5) - 3,
                                                                               abs=0.01)
    for pieza in (t3, c, p, ln):
        a = pieza.muestrear(50, np.random.default_rng(4))
        assert np.array_equal(a, pieza.muestrear(50, np.random.default_rng(4)))
        u = np.array([0.1, 0.5, 0.9])
        assert np.all(np.diff(pieza._cuantil(u)) > 0)
    with pytest.raises(ValueError, match="centrar"):
        ml.pareto(0.8)
    assert np.isinf(ml.pareto(0.8, centrar=False).varianza)
    with pytest.raises(ValueError):
        ml.t_student(0)
    with pytest.raises(ValueError, match="centrada"):
        ml.heterocedastico(lambda d: d["x"], base=ml.normal(1, 1))


def test_piso_infinito_con_colas_sin_segundo_momento():
    for ruido in (ml.pareto(1.5), ml.t_student(2), ml.cauchy()):
        assert np.isinf(ml.piso(ml.proceso(n=50, ruido=ruido)))
    assert ml.piso(ml.proceso(n=50, ruido=ml.t_student(3))) == pytest.approx(3.0)
    # absoluta: E|ε| de la pieza simétrica; inf con Cauchy; nan (con aviso) si es asimétrica
    assert ml.piso(ml.proceso(n=50, ruido=ml.t_student(2)), "absoluta") == pytest.approx(np.sqrt(2))
    assert ml.piso(ml.proceso(n=50, ruido=ml.t_student(3)), "absoluta") == pytest.approx(
        2 * np.sqrt(3) / np.pi)
    assert np.isinf(ml.piso(ml.proceso(n=50, ruido=ml.cauchy()), "absoluta"))
    with pytest.warns(UserWarning, match="piso desconocido"):
        assert np.isnan(ml.piso(ml.proceso(n=50, ruido=ml.pareto(1.5)), "absoluta"))


def test_heterocedastico_varianza_por_fila_y_su_piso():
    datos = ml.caso(12)
    assert ml.piso(datos) == pytest.approx(0.04 + 0.3 + 0.75, rel=0.01)  # E[(0.2 + 1.5x)²]
    assert ml.piso(datos, "absoluta") == pytest.approx(0.95 * np.sqrt(2 / np.pi), rel=0.01)
    e = datos.realidad["y"] - datos.realidad["f"]
    x = datos.realidad["x"]
    assert e[x < 0.2].std() == pytest.approx(np.sqrt(((0.2 + 1.5 * np.linspace(0, 0.2, 999)) ** 2).mean()),
                                             rel=0.05)
    assert e[x > 0.8].std() > 4 * e[x < 0.2].std()
    con_cauchy = ml.caso(12, ruido=ml.heterocedastico(lambda d: 0.2 + d["x"], base=ml.cauchy()))
    assert np.isinf(ml.piso(con_cauchy)) and np.isinf(ml.piso(con_cauchy, "absoluta"))


def test_caso_8_piso_endogeno_y_mc_por_encima():
    datos = ml.caso(8)
    assert abs(ml.piso(datos) - 0.75) < 0.01
    grande = ml.caso(8, n=20_000)
    m = ml.ajustar(grande)
    l_i = ml.perdida(grande.val["y"], m.predecir(grande.val))
    assert l_i.mean() >= ml.piso(grande) - 2 * ml.error_estandar(l_i)
    assert m.beta_gorro["x1"] == pytest.approx(2.5, abs=0.03)


# --- representaciones, métricas -------------------------------------------

def test_interacciones_y_estandarizar():
    datos = ml.caso(7)
    phi = ml.combinar(ml.columnas("x1", "x2"), ml.interacciones(("x1", "x2")))
    m = ml.ajustar(datos, phi=phi)
    M = m.Phi(datos.val)
    assert list(M.columns) == ["1", "x1", "x2", "x1*x2"]
    assert np.allclose(M["x1*x2"], datos.val["x1"] * datos.val["x2"])
    columnas_antes = list(datos.ent.columns)
    est = ml.estandarizar(ml.polinomio(3)).ajustar(ml.caso(11).ent)
    E = est(ml.caso(11).ent)
    assert np.allclose(E.mean(), 0, atol=1e-12) and np.allclose(E.std(ddof=0), 1)
    V = est(ml.caso(11).val)  # con la media y la desviación de ent, no de val
    assert not np.allclose(V.mean(), 0, atol=1e-6)
    con_uno = ml.estandarizar(ml.combinar(ml.polinomio(2))).ajustar(datos.ent.assign(x=datos.ent.x1))
    assert np.all(con_uno(datos.ent.assign(x=datos.ent.x1))["1"] == 1.0)
    assert list(datos.ent.columns) == columnas_antes
    with pytest.raises(ValueError):
        ml.interacciones("x1")
    with pytest.raises(ValueError):
        ml.estandarizar("x1")


def test_mae_rmse_r2_y_peores_errores():
    y, g = np.array([0.0, 0, 0, 4]), np.zeros(4)
    assert ml.mae(y, g) == 1.0 and ml.rmse(y, g) == 2.0 and ml.rmse(y, g) != ml.mae(y, g)
    assert ml.r2([1.0, 2, 3], [1.0, 2, 3]) == 1.0
    assert ml.r2([1.0, 2, 3], [2.0, 2, 2]) == pytest.approx(0.0)
    datos = ml.caso(11)
    m = ml.ajustar(datos)
    antes = datos.val.copy()
    t = ml.peores_errores(m, datos.val, k=7)
    assert len(t) == 7 and list(t.columns) == ["x", "y", "y_gorro", "e"]
    assert np.all(np.diff(np.abs(t["e"].to_numpy())) <= 0)
    e = datos.val["y"] - m.predecir(datos.val)
    assert abs(t["e"].iloc[0]) == pytest.approx(np.abs(e).max())
    pd.testing.assert_frame_equal(datos.val, antes)


# --- regularización ----------------------------------------------------------

def test_encoger_1d_contra_el_enunciado_y_kkt():
    b = np.array([-2.0, -0.3, 0.0, 0.2, 1.0, 3.0])
    assert np.allclose(ml.encoger_1d(b, 1.0, "l2"), b / 2)
    assert np.allclose(ml.encoger_1d(b, 1.0, "l1"), np.sign(b) * np.maximum(np.abs(b) - 0.5, 0))
    assert np.allclose(ml.encoger_1d(b, 1.0, "elastica", rho=1.0), ml.encoger_1d(b, 1.0, "l1"))
    assert np.allclose(ml.encoger_1d(b, 1.0, "elastica", rho=0.0), ml.encoger_1d(b, 1.0, "l2"))
    assert ml.encoger_1d(1.0, 1.0, "l1") == 0.5 and ml.encoger_1d(1.0, 0.7, None) == 1.0
    # contra ajustar con un diseño de una columna centrada con (1/n)Σx² = 1
    rng = np.random.default_rng(3)
    x = rng.normal(size=200)
    x = (x - x.mean()) / x.std()
    df = pd.DataFrame({"x": x, "y": 0.8 * x + rng.normal(size=200)})
    b_mc = ml.ajustar(df, columnas_x=["x"], tarea="regresion").beta_gorro["x"]
    for pen in ("l2", "l1", "elastica"):
        for mu in (0.1, 0.9, 3.0):
            m = ml.ajustar(df, mu=mu, penalizacion=pen, rho=0.4, columnas_x=["x"], tarea="regresion")
            assert m.beta_gorro["x"] == pytest.approx(ml.encoger_1d(b_mc, mu, pen, 0.4), abs=1e-9)


def test_trayectorias_solo_pendientes_y_mu_grande():
    datos = ml.muchas_variables(n=200, J=6, utiles=3)
    mus = [0.01, 0.1, 1.0, 1e8]
    for pen in ("l2", "l1", "elastica"):
        t = ml.trayectorias(datos, None, pen, mus)
        assert list(t.columns) == ["mu", "coeficiente", "valor"]
        assert "1" not in set(t["coeficiente"])
        assert set(t["coeficiente"]) == set(datos.columnas_x)
        assert np.all(np.abs(t[t["mu"] == 1e8]["valor"]) < 1e-6)
        m = ml.ajustar(datos, mu=1e8, penalizacion=pen)
        assert m.beta_gorro["1"] == pytest.approx(datos.ent["y"].mean(), abs=1e-6)


def test_optimo_restringido_reajusta_al_mismo_beta():
    datos = ml.caso(9)
    for pen in ("l1", "l2", "elastica"):
        beta, mu = ml.optimo_restringido(datos, None, pen, 0.8, rho=0.5)
        assert mu > 0
        m = ml.ajustar(datos, mu=mu, penalizacion=pen, rho=0.5)
        assert np.allclose(m.beta_gorro.to_numpy(), beta.to_numpy(), atol=1e-4)
        b = beta[["x1", "x2"]].to_numpy()
        omega = {"l1": np.abs(b).sum(), "l2": (b ** 2).sum(),
                 "elastica": 0.5 * np.abs(b).sum() + 0.5 * (b ** 2).sum()}[pen]
        assert omega == pytest.approx(0.8, abs=1e-7)
        # nadie dentro de Ω <= d tiene menor L_ent (comparado con un optimizador aparte)
        X = datos.ent[["x1", "x2"]].to_numpy()
        Xc, yc = X - X.mean(axis=0), datos.ent["y"].to_numpy() - datos.ent["y"].mean()
        from scipy import optimize as opt
        if pen == "l2":
            restr = {"type": "ineq", "fun": lambda v: 0.8 - (v ** 2).sum()}
            r = opt.minimize(lambda v: ((yc - Xc @ v) ** 2).mean(), np.zeros(2), method="SLSQP",
                             constraints=[restr], options={"ftol": 1e-14, "maxiter": 500})
            assert ((yc - Xc @ b) ** 2).mean() <= r.fun + 1e-7
    beta, mu = ml.optimo_restringido(datos, None, "l1", 1e6)
    assert mu == 0.0
    with pytest.raises(ValueError, match="mayor que 0"):
        ml.optimo_restringido(datos, None, "l1", 0.0)
    with pytest.raises(ValueError, match="2 coeficientes"):
        ml.optimo_restringido(ml.muchas_variables(n=60, J=3, utiles=3), None, "l1", 1.0)


def test_beta_repetido_contra_minimos_cuadrados_a_mano():
    datos = ml.caso(9)
    t = ml.beta_repetido(datos.rehacer, None, repeticiones=5, semilla=3)
    assert list(t.index) == [3, 4, 5, 6, 7] and list(t.columns) == ["1", "x1", "x2"]
    for s in (3, 7):
        d = datos.rehacer(s)
        X = np.column_stack([np.ones(len(d.ent)), d.ent[["x1", "x2"]].to_numpy()])
        b = np.linalg.lstsq(X, d.ent["y"].to_numpy(), rcond=None)[0]
        assert np.allclose(t.loc[s].to_numpy(), b, atol=1e-10)
    datos24 = ml.muchas_variables(n=150, J=10, utiles=3)
    lasso = ml.beta_repetido(datos24.rehacer, None, repeticiones=10, mu=0.3, penalizacion="l1")
    assert ((lasso.drop(columns="1") == 0).to_numpy().sum()) > 0
    frecuencia = (lasso != 0).mean()
    assert frecuencia["x1"] == 1.0


def test_muchas_variables():
    datos = ml.muchas_variables(n=200, J=12, utiles=4, gemelas={"x1": 0.9})
    bv = ml.beta_verdadero(datos, None)
    assert np.allclose(bv[[f"x{j}" for j in range(1, 13)]].to_numpy(),
                       [3, -2, 1.5, 1] + [0] * 8, atol=1e-9)
    assert np.corrcoef(datos.realidad["x1"], datos.realidad["x5"])[0, 1] == pytest.approx(0.9, abs=0.03)
    assert abs(np.corrcoef(datos.realidad["x1"], datos.realidad["x6"])[0, 1]) < 0.03
    visto = {}
    real = ml._proceso

    def espia(**kw):
        visto.update(kw)
        return real(**kw)

    import unittest.mock as mock
    with mock.patch.object(ml, "_proceso", espia):
        ml.muchas_variables(n=50, J=3, utiles=2, escala={"x2": 10, "y": 3})
    assert visto["escala"] == {"x2": 10, "y": 3}
    with pytest.raises(ValueError):
        ml.muchas_variables(J=5, utiles=6)


def test_caso_24_mu_escala_con_el_cuadrado_de_y():
    datos, kilos = ml.caso(24), ml.caso(24, escala=None)
    vivos = lambda d, mu: int((ml.ajustar(d, mu=mu, penalizacion="l1").beta_gorro.drop("1") != 0).sum())  # noqa: E731
    assert vivos(datos, 0.3) > vivos(kilos, 0.3)
    b1 = ml.ajustar(datos, mu=300.0, penalizacion="l1").beta_gorro / 1000
    b0 = ml.ajustar(kilos, mu=0.3, penalizacion="l1").beta_gorro
    assert np.abs(b1 - b0).max() < 1e-6
    r1 = ml.ajustar(datos, mu=0.3, penalizacion="l2").beta_gorro / 1000
    assert np.abs(r1 - ml.ajustar(kilos, mu=0.3, penalizacion="l2").beta_gorro).max() < 1e-6


# --- gráficas ----------------------------------------------------------------

def test_dibujar_benchmarks_barras_y_pisos():
    datos = ml.caso(11)
    m = ml.ajustar(datos)
    ax = ml.dibujar_benchmarks(m, datos)
    b = ml.benchmarks(datos, datos.val, criterios=["cuadratica", "absoluta"])
    largo = {p.get_gid(): p.get_width() for p in ax.patches if p.get_gid()}
    assert largo["barra-cuadratica-media"] == pytest.approx(np.sqrt(b.loc["media", "cuadratica"]))
    assert largo["barra-absoluta-mediana"] == pytest.approx(b.loc["mediana", "absoluta"])
    assert largo["barra-cuadratica-modelo"] == pytest.approx(ml.rmse(datos.val.y, m.predecir(datos.val)))
    assert largo["barra-cuadratica-piso"] == pytest.approx(np.sqrt(ml.piso(datos)))
    assert largo["barra-absoluta-piso"] == pytest.approx(ml.piso(datos, "absoluta"))
    assert "RMSE" in " ".join(t.get_text() for t in ax.get_yticklabels())
    with pytest.raises(ValueError, match="no es un criterio"):
        ml.dibujar_benchmarks(m, datos, criterios=("rmse",))
    for ruido in (ml.pareto(1.5), ml.t_student(2), ml.cauchy()):
        d = ml.caso(6, ruido=ruido)
        ax = _calla(ml.dibujar_benchmarks, ml.ajustar(d), d)
        assert "barra-cuadratica-piso" not in [p.get_gid() for p in ax.patches]
        textos = [t.get_text() for t in ax.get_legend().get_texts()]
        assert "piso infinito: todo predictor tiene riesgo cuadrático infinito" in textos
        assert np.isfinite(ax.get_xlim()[1])
    d = ml.proceso(n=200, x={"x1": ml.normal(), "x2": ml.normal()}, correlacion={("x1", "x2"): 0.5},
                   omitir=["x2"], f=lambda d: d["x1"] * d["x2"] ** 2)
    ax = _calla(ml.dibujar_benchmarks, ml.ajustar(d), d)
    assert "piso desconocido" in [t.get_text() for t in ax.get_legend().get_texts()]


def test_dibujar_media_acumulada_determinista_y_normal_estable():
    piezas = {"normal": ml.normal(), "Cauchy": ml.cauchy()}
    fig = ml.dibujar_media_acumulada(piezas, n_max=10_000, trayectorias=20)
    otra = ml.dibujar_media_acumulada(piezas, n_max=10_000, trayectorias=20)
    a, b = fig.axes, otra.axes
    assert len(a) == 2
    finales = []
    for la, lb in zip(a[0].get_lines(), b[0].get_lines()):
        assert np.array_equal(la.get_ydata(), lb.get_ydata())
        if (la.get_gid() or "").startswith("traza-normal"):
            finales.append(la.get_ydata()[-1])
    assert len(finales) == 20
    assert (max(finales) - min(finales)) / np.mean(finales) < 0.10
    cauchy_finales = [ln.get_ydata()[-1] for ln in a[1].get_lines()
                      if (ln.get_gid() or "").startswith("traza-Cauchy")]
    assert max(cauchy_finales) / min(cauchy_finales) > 10
    ax = ml.dibujar_media_acumulada({"normal": ml.normal()}, n_max=100, trayectorias=2)
    assert hasattr(ax, "get_lines")


def test_dibujar_peso_de_filas_con_un_vector_conocido():
    df = pd.DataFrame({"x": np.zeros(100), "y": np.r_[np.ones(99), 50.0]})
    ax = ml.dibujar_peso_de_filas(_Constante(0.0), df)
    lineas = {ln.get_gid(): ln for ln in ax.get_lines()}
    for gid, esperado in (("peso-mse", 2500 / 2599), ("peso-mae", 50 / 149)):
        x, y = lineas[gid].get_xdata(), lineas[gid].get_ydata()
        assert x[1] == pytest.approx(0.01) and y[1] == pytest.approx(esperado)
        assert round(y[1], 3) == {"peso-mse": 0.962, "peso-mae": 0.336}[gid]


def test_dibujar_residuales_plano_marcadores_y_todas_las_filas():
    datos = ml.caso(7)
    m = ml.ajustar(datos)
    ax = ml.dibujar_residuales_plano(m, datos.val, "x1", "x2")
    nubes = {c.get_gid(): c for c in ax.collections}
    assert set(nubes) == {"residuales-positivos", "residuales-negativos"}
    assert sum(len(c.get_offsets()) for c in nubes.values()) == len(datos.val)
    from matplotlib.markers import MarkerStyle
    for gid, marca in (("residuales-positivos", "^"), ("residuales-negativos", "v")):
        ruta = nubes[gid].get_paths()[0]
        assert np.allclose(ruta.vertices, MarkerStyle(marca).get_path().transformed(
            MarkerStyle(marca).get_transform()).vertices)


def test_dibujar_beta_repetido_con_el_trazo_de_la_diana():
    datos = ml.caso(9)
    t = ml.beta_repetido(datos.rehacer, None, repeticiones=40)
    verdadero = ml.beta_verdadero(datos, None)
    ax = ml.dibujar_beta_repetido(t, verdadero, ["x1", "x2"])
    anillos = [p for p in ax.patches if (p.get_gid() or "").startswith("anillo-")]
    assert len(anillos) == 3
    assert all(np.allclose(p.center, verdadero[["x1", "x2"]]) for p in anillos)
    nube = next(ln for ln in ax.get_lines() if ln.get_gid() == "repeticion")
    assert len(nube.get_xdata()) == 40
    # mismos objetos de estilo que dibujar_diana (clase 2)
    sv = ml.sesgo_varianza(ml.entregas_curvas().rehacer, _polis([1]), repeticiones=5)
    diana = ml.dibujar_diana(sv, 3.0)
    rep_d = next(ln for ln in diana.get_lines() if ln.get_gid() == "repeticion")
    for prop in ("get_marker", "get_color", "get_markersize", "get_markeredgewidth", "get_linestyle"):
        assert getattr(nube, prop)() == getattr(rep_d, prop)(), prop
    ver_d = next(ln for ln in diana.get_lines() if ln.get_gid() == "f")
    prom_d = next(ln for ln in diana.get_lines() if (ln.get_gid() or "").startswith("promedio-"))
    ver = next(ln for ln in ax.get_lines() if ln.get_gid() == "verdadero")
    prom = next(ln for ln in ax.get_lines() if ln.get_gid() == "promedio")
    assert ver.get_color() == ver_d.get_color() and prom.get_color() == prom_d.get_color()
    ax1 = ml.dibujar_beta_repetido(t, verdadero, "x1")
    prom1 = next(ln for ln in ax1.get_lines() if ln.get_gid() == "promedio")
    assert prom1.get_linestyle() == prom_d.get_linestyle() == "--"
    assert next(ln for ln in ax1.get_lines() if ln.get_gid() == "verdadero").get_xdata()[0] == \
        pytest.approx(1.0)
    with pytest.raises(ValueError, match="1 o 2"):
        ml.dibujar_beta_repetido(t, verdadero, ["1", "x1", "x2"])


def test_dibujar_encoger_1d_marca_los_minimos_de_encoger_1d():
    for pen in ("l2", "l1", "elastica"):
        ax = ml.dibujar_encoger_1d("objetivo", b=1.3, mus=(0.0, 0.5, 2.0), penalizacion=pen, rho=0.3)
        for mu in (0.0, 0.5, 2.0):
            ln = next(ln for ln in ax.get_lines() if ln.get_gid() == f"minimo-{mu:g}")
            assert ln.get_xdata()[0] == pytest.approx(ml.encoger_1d(1.3, mu, pen, 0.3))
            curva = next(c for c in ax.get_lines() if c.get_gid() == f"objetivo-{mu:g}")
            assert ln.get_ydata()[0] <= curva.get_ydata().min() + 1e-9
    ax = ml.dibujar_encoger_1d()
    assert {"solucion-l2", "solucion-l1", "solucion-elastica", "sin-regularizar"} <= set(_gids(ax))
    with pytest.raises(ValueError, match="penalizacion"):
        ml.dibujar_encoger_1d("objetivo")


def test_dibujar_trayectorias_colores_por_rol():
    datos = ml.muchas_variables(n=150, J=8, utiles=3)
    t = ml.trayectorias(datos, ml.estandarizar(ml.columnas(*datos.columnas_x)), "l1",
                        [0.0] + list(np.logspace(-3, 1, 12)))
    ax = ml.dibujar_trayectorias(t, utiles=["x1", "x2", "x3"], marcar_mu=0.1)
    lineas = {ln.get_gid(): ln for ln in ax.get_lines() if (ln.get_gid() or "").startswith("coef-")}
    assert set(lineas) == {f"coef-x{j}" for j in range(1, 9)}
    grises = {lineas[f"coef-x{j}"].get_color() for j in range(4, 9)}
    assert len(grises) == 1 and grises.isdisjoint({lineas[f"coef-x{j}"].get_color() for j in (1, 2, 3)})
    assert all(len(ln.get_xdata()) == 12 for ln in lineas.values())  # μ = 0 no cabe en log
    assert "marcar-mu" in _gids(ax)


def test_dibujar_regiones_titulo_con_el_mu_de_optimo_restringido():
    datos = ml.caso(9)
    for pen in ("l1", "l2", "elastica"):
        ax = ml.dibujar_regiones(datos, None, pen, 1.0)
        _, mu = ml.optimo_restringido(datos, None, pen, 1.0)
        assert f"μ equivalente = {mu:.4g}" in ax.get_title()
        estrella = next(ln for ln in ax.get_lines() if ln.get_gid() == "beta-restringido")
        beta, _ = ml.optimo_restringido(datos, None, pen, 1.0)
        assert np.allclose([estrella.get_xdata()[0], estrella.get_ydata()[0]], beta[["x1", "x2"]])
    ax = ml.dibujar_regiones(datos, None, "l1", 1.0, mostrar_mu=False)
    assert "μ" not in ax.get_title()


def test_dibujar_presupuesto_convexa_y_su_recta_de_apoyo():
    datos = ml.caso(9)
    ds = np.linspace(0.1, 2.5, 25)
    ax = ml.dibujar_presupuesto(datos, None, "l1", ds, d_marcado=1.0)
    curva = next(ln for ln in ax.get_lines() if ln.get_gid() == "curva-presupuesto")
    v = np.asarray(curva.get_ydata(), float)
    assert np.all(np.diff(v) <= 1e-8)
    assert np.all(v[:-2] - 2 * v[1:-1] + v[2:] >= -1e-8)  # rejilla uniforme
    recta = next(ln for ln in ax.get_lines() if ln.get_gid() == "recta-apoyo")
    _, mu = ml.optimo_restringido(datos, None, "l1", 1.0)
    (x0, x1), (y0, y1) = recta.get_xdata(), recta.get_ydata()
    assert (y1 - y0) / (x1 - x0) == pytest.approx(-mu, abs=1e-4)
    pendiente = (y1 - y0) / (x1 - x0)
    assert np.all(v >= y0 + pendiente * (ds - x0) - 1e-6)
    omega_mc = np.abs(ml.ajustar(datos).beta_gorro[["x1", "x2"]]).sum()
    ax = ml.dibujar_presupuesto(datos, None, "l1", ds, d_marcado=omega_mc + 0.5)
    recta = next(ln for ln in ax.get_lines() if ln.get_gid() == "recta-apoyo")
    assert np.ptp(recta.get_ydata()) == 0.0
    with pytest.raises(ValueError, match="mayor que 0"):
        ml.dibujar_presupuesto(datos, None, "l1", [0.0, 0.5, 1.0])
    # dibujar_frontera conserva su firma (frontera de decisión, clases 1, 4, 5)
    assert list(inspect.signature(ml.dibujar_frontera).parameters) == ["modelo", "df", "vista",
                                                                       "ax", "tema"]


def _modulo_1_2():
    r = subprocess.run(["git", "-C", str(RAIZ), "show", f"{VERSION_1_2}:tools/aprendizaje_maquina.py"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        pytest.skip(f"no está el commit {VERSION_1_2} de ml_lab 1.2")
    import importlib.util
    import tempfile
    ruta = Path(tempfile.mkdtemp()) / "ml_lab_1_2.py"
    ruta.write_text(r.stdout, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("ml_lab_1_2", ruta)
    viejo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(viejo)
    assert viejo.VERSION == "1.2"
    return viejo


def _svg(fig):
    buf = io.StringIO()
    with plt.rc_context({"svg.hashsalt": "ml", "svg.fonttype": "none"}):  # el texto, como texto
        fig.savefig(buf, format="svg", metadata={"Date": None})
    return re.sub(r'id="[^"]*"|xlink:href="#[^"]*"|clip-path="url\(#[^)]*\)"', "", buf.getvalue())


def test_dibujar_cv_y_diana_sin_argumentos_nuevos_son_los_de_1_2():
    viejo = _modulo_1_2()
    datos = ml.entregas_curvas()
    c = _polis(range(7))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for con in ("ent", "val", "cv", "prueba"):
            sel = ml.elegir(datos, c, con=con)
            nuevo = _svg(ml.dibujar_cv(sel, R={N: 1.0 + N for N in c}, piso=0.5, log=False,
                                       anotar=None).figure)
            antes = _svg(viejo.dibujar_cv(sel, R={N: 1.0 + N for N in c}, piso=0.5).figure)
            assert nuevo == antes, con
        mus = [float(m) for m in np.logspace(-3, 0.5, 4)]  # floats largos: el rótulo no cambia
        sel = ml.Seleccion(tabla=pd.DataFrame({"candidato": mus, "valor": [3.0, 2.0, 2.5, 4.0],
                                               "ee": [0.5] * 4}),
                           elegido=mus[1], elegido_un_ee=mus[2], modelo=None, modelo_final=None,
                           criterio="cuadratica", sentido="min", costo_ajustes=21, cv=None, con="cv")
        assert _svg(ml.dibujar_cv(sel).figure) == _svg(viejo.dibujar_cv(sel).figure)
        sv = ml.sesgo_varianza(datos.rehacer, _polis([1, 6]), repeticiones=4)
        assert _svg(ml.dibujar_diana(sv, 3.0).figure) == _svg(viejo.dibujar_diana(sv, 3.0).figure)
    sel = _calla(ml.elegir, datos, c, con="cv")
    with pytest.raises(TypeError):
        ml.dibujar_cv(sel, None, None, None, None, True)
    with pytest.raises(ValueError, match="> 0"):
        ml.dibujar_cv(sel, log=True)  # el candidato 0 no cabe en log


def test_dibujar_cv_log_y_anotar():
    datos = ml.entregas_curvas()
    mus = [0.001, 0.01, 0.1, 1.0, 10.0]
    c = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=ml.estandarizar(ml.polinomio(8)), mu=mu,
                                           penalizacion="l2")) for mu in mus}
    sel = _calla(ml.elegir, datos, c, con="cv", orden_complejidad=sorted(mus, reverse=True))
    ax = ml.dibujar_cv(sel, log=True, anotar={0.01: "A", 10.0: "tú"})
    serie = next(ln for ln in ax.get_children() if getattr(ln, "get_gid", lambda: None)() == "serie-cv")
    assert np.allclose(np.sort(serie.get_xdata()), np.log10(mus))
    textos = {a.get_gid(): a for a in ax.texts}
    assert textos["anotar-0.01"].get_text() == "A" and textos["anotar-10.0"].xy[0] == pytest.approx(1.0)
    assert ax.get_xlabel() == "log₁₀ μ"
    with pytest.raises(ValueError, match="no es un candidato"):
        ml.dibujar_cv(sel, anotar={5.0: "x"})


# --- taller y galería --------------------------------------------------------

def test_senal_es_la_regla_descriptiva():
    assert ml._senal([-2.0, -2.1, -1.9, -2.2, -1.8]) == "señal"
    assert ml._senal([-2.0, 1.5, -0.3, 0.8, -1.0]) == "sin señal"
    assert ml._senal([1.0]) == "sin señal"


def test_taller_3_corre_rapido_sin_tocar_prueba(monkeypatch):
    import time

    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    for numero, opciones in ((7, {}), (12, {}), (24, {"que": "lagrangeano"}),
                             (10, {"que": "lagrangeano"})):
        datos = ml.caso(numero)
        datos.prueba = None  # cualquier lectura de prueba rompería la llamada
        inicio = time.perf_counter()
        buf = io.StringIO()
        with redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ml.taller(datos, 3, **opciones)
        assert time.perf_counter() - inicio < 10, numero
        salida = buf.getvalue()
        plt.close("all")
        if opciones.get("que") == "lagrangeano":
            assert "le gana" not in salida
            linea = next(t for t in salida.splitlines() if t.startswith("Contra la media"))
            assert "EE" not in linea and ("señal" in linea)
            assert "se confirma en una reserva" in salida
        else:
            assert "diferencia" not in salida or "val (no eligió nada" in salida


def test_taller_3_pasa_orden_complejidad(monkeypatch):
    visto = {}
    real = ml.elegir

    def espia(*args, **kwargs):
        visto.update(kwargs)
        return real(*args, **kwargs)

    monkeypatch.setattr(ml, "elegir", espia)
    mus = list(np.logspace(-3, 0.5, 9))
    with redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.taller(ml.caso(24, escala=None), 3, que="lagrangeano", mus=mus)
    assert visto["orden_complejidad"] == sorted(mus, reverse=True)
    sel = _calla(real, ml.caso(24, escala=None),
                 {mu: (lambda df, mu=mu: ml.ajustar(df, phi=ml.estandarizar(ml.columnas(
                     *[f"x{j}" for j in range(1, 11)])), mu=mu, penalizacion="l1")) for mu in mus},
                 con="cv", orden_complejidad=sorted(mus, reverse=True))
    assert sel.elegido_un_ee >= sel.elegido


def test_galeria_3_sin_widgets(monkeypatch):
    monkeypatch.setenv("ML_LAB_PRUEBA", "1")
    buf = io.StringIO()
    with redirect_stdout(buf), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.galeria(3)
    assert "Caso 6" in buf.getvalue()
    with redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.galeria(3, casos=[24])
