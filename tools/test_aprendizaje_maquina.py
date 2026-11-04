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


def _compatible(vieja, nueva):
    """Cada nombre de la vieja sigue en la nueva con la misma firma, o con
    argumentos con valor por omisión agregados al final."""
    for nombre, firma in vieja.items():
        if nombre == "__claves__":
            continue
        assert nombre in nueva, f"se quitó {nombre}"
        actual = nueva[nombre]
        if actual == firma:
            continue
        if isinstance(firma, dict) and isinstance(actual, dict):
            for metodo, f in firma.items():
                assert actual.get(metodo) == f, f"cambió {nombre}.{metodo}"
            continue
        assert isinstance(firma, str) and isinstance(actual, str), nombre
        # solo se agregan parámetros con valor por omisión al final
        assert actual.startswith(firma.rstrip(")")), f"cambió la firma de {nombre}"
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
    assert set(ml.PROCESOS) == {
        "entregas", "inverso", "mezcla_logs", "seno", "x1_mas_x2x3", "lluvia",
    }
    for prohibida in ("lineal", "ar1", "cola_larga"):
        assert prohibida not in ml.PROCESOS
    assert set(ml.CASOS_BORDE) == {1, 2, 23}
    assert all(isinstance(k, int) for k in ml.CASOS_BORDE)
    assert set(ml.ANALISIS_TALLER) == {1}
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
    assert ml.VERSION == "1.0"
    assert ml.VERSION in ml.CAMBIOS


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
    for kwargs, clase in [({"separar": "tiempo"}, "clase 2"), ({"separar": "grupo"}, "clase 2"),
                          ({"separar": "estratificado"}, "clase 2"),
                          ({"despliegue": "futuro"}, "clase 2"),
                          ({"despliegue": "grupos_nuevos"}, "clase 2"),
                          ({"despliegue": "otra_poblacion"}, "clase 2"),
                          ({"despliegue": "futuro", "deriva": lambda t: {}}, "clase 2"),
                          ({"faltantes": {"x": (0.2, "azar")}}, "clase 4")]:
        with pytest.raises(NotImplementedError, match=clase):
            ml.proceso(n=20, **kwargs)
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
    with pytest.raises(NotImplementedError, match="clase 2"):
        ml.curva_capacidad(datos, candidatos, conjuntos=("cv",), k=5)


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
        assert caso.numero == numero and caso.clase == 1
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
