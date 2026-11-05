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
import math
import os
import re
import subprocess
import sys
import warnings
from contextlib import redirect_stdout
from types import SimpleNamespace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgba  # noqa: E402
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
    # 1.4 (clase 4) agrega los procesos hilo "fraude" y "mensajes3"
    assert set(ml.PROCESOS) == set(claves_1_0["PROCESOS"]) | {"recursivo", "entregas_curvas",
                                                             "fraude", "mensajes3"}
    assert set(_entradas()["1.2"]["__claves__"]["PROCESOS"]) >= {"entregas_curvas"}
    for prohibida in ("lineal", "ar1", "cola_larga"):
        assert prohibida not in ml.PROCESOS
    # 1.3 (clase 3) agrega los casos 6 a 12 y 24 y el taller 3; 1.5 (clase 4), 17, 18, 22,
    # 25 y el taller 4; 1.6 (clase 5), 19, 20, 21, 26, 27, 28 y el taller 5
    assert set(ml.CASOS_BORDE) == {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                   19, 20, 21, 22, 23, 24, 25, 26, 27, 28}
    assert all(isinstance(k, int) for k in ml.CASOS_BORDE)
    assert set(ml.ANALISIS_TALLER) == {1, 2, 3, 4, 5}
    # 1.4 agrega las métricas de la clase 4
    assert ml.SENTIDO == {
        "cuadratica": "min", "absoluta": "min", "logaritmica": "min", "aciertos": "max",
        "mcc": "max", "aciertos_balanceados": "max", "brier": "min",
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
    assert ml.VERSION == "1.6"
    assert {"1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"} <= set(ml.CAMBIOS)
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


def test_ajustar_con_pesos_desde_la_clase_4():
    """1.4: pesos solo en clasificación, y modelo.pesos guarda los que se usaron."""
    datos = ml.anillos()
    m = ml.ajustar(datos, tarea="clasificacion", pesos={0: 1.0, 1: 2.0})
    assert m.pesos == {0: 1.0, 1: 2.0}
    assert ml.ajustar(datos, pesos="balanceado").pesos == pytest.approx(
        ml._pesos_balanceados(datos.ent["y"], [0, 1]))
    with pytest.raises(ValueError, match="clasificación"):
        ml.ajustar(ml.PROCESOS["entregas"](), pesos="balanceado")
    with pytest.raises(ValueError, match="clases"):
        ml.ajustar(datos, pesos={0: 1.0})


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
    assert ml.desempeno(m, datos, "mcc") == pytest.approx(
        ml.mcc(datos.despliegue["y"], m.predecir(datos.despliegue), clases=[0, 1]))


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
    # 1.4: faltantes ya funciona (clase 4)
    assert ml.proceso(n=20, faltantes={"x": (0.2, "azar")}).ent["x"].isna().any()
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
    ml.ajustar_otro(ml.proceso(n=20), familia="arbol")  # desde 1.6 (clase 5)


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
    assert ml.benchmarks(anillos, anillos.val, criterios=["mcc"]).loc["moda", "mcc"] == 0.0


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
        dueña = (2 if 13 <= numero <= 16 else 3 if 6 <= numero <= 12 or numero == 24
                 else 4 if numero in (17, 18, 22, 25)
                 else 5 if numero in (19, 20, 21, 26, 27, 28) else 1)
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
def test_adelantos_de_proceso_clasificacion_ya_no_lanzan_en_la_clase_4(cambio):
    """1.4 los trae: ninguno lanza NotImplementedError (separar tiempo/grupo sin la
    columna que piden es ValueError, en español)."""
    if cambio.get("K") == 3:
        cambio = {**cambio, "puntajes": [lambda d: 0 * d.x1, lambda d: d.x1, lambda d: d.x2]}
    if "separar" in cambio:
        with pytest.raises(ValueError, match="columna"):
            ml.proceso_clasificacion(n=50, con_realidad=False, **cambio)
        return
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
    assert len(ml.pliegues(df, como="temporal")) == 5  # desde 1.6 (clase 5)
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
    # la desviación de las diferencias, no su error estándar: aquí el EE daría «señal»
    assert ml._senal([-1.0, -1.0, 0.0, 0.0, 0.0]) == "sin señal"
    # ddof=1: |media| = 1.1 queda entre la desviación con ddof=0 (0.9) y con ddof=1 (1.27)
    assert ml._senal([0.2, 2.0]) == "sin señal"


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


def test_taller_3_no_evalua_el_modelo_final_en_val(monkeypatch):
    datos = ml.caso(24, escala=None)
    real = ml.elegir

    def espia(*args, **kwargs):
        s = real(*args, **kwargs)
        original = s.modelo_final.predecir

        def predecir(df):
            assert not (len(df) == len(datos.val) and df.index.equals(datos.val.index)
                        and df["y"].equals(datos.val["y"])), "evaluó el modelo final en val"
            return original(df)

        s.modelo_final.predecir = predecir
        return s

    monkeypatch.setattr(ml, "elegir", espia)
    with redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.taller(datos, 3, que="lagrangeano")
        with pytest.raises(AssertionError, match="final en val"):  # la espía sí ve una evaluación
            s = ml.elegir(datos, {1.0: lambda df: ml.ajustar(df, mu=1.0, penalizacion="l1")}, con="cv")
            ml.L(s.modelo_final, datos.val)
    with pytest.raises(ValueError, match="en el taller los μ son > 0"):
        ml.taller(datos, 3, que="lagrangeano", mus=[0.0, 0.1, 1.0])


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


# --- lo que encontró la revisión del lote c3 ----------------------------------

def test_estandarizar_columna_constante_no_amplifica_el_redondeo():
    df = pd.DataFrame({"x": np.full(100, 0.1), "y": np.full(100, 2.0)})
    est = ml.estandarizar(ml.columnas("x")).ajustar(df)
    assert np.allclose(est(df)["x"], 0.0)
    m = ml.ajustar(df, phi=ml.estandarizar(ml.columnas("x")), columnas_x=["x"], tarea="regresion")
    assert abs(m.predecir(pd.DataFrame({"x": [0.11]}))[0] - 2.0) < 1e-6


def test_heterocedastico_sin_ruido_tiene_piso_cero():
    d = ml.proceso(n=50, ruido=ml.heterocedastico(lambda d: 0.0 * d["x"], base=ml.cauchy()))
    assert ml.piso(d) == 0.0 and ml.piso(d, "absoluta") == 0.0
    assert np.allclose(d.ent["y"], d.ent["x"] * 0 + ml._f_por_omision(d.ent))


def test_caso_10_se_rompe_en_8_de_10_semillas():
    """A μ = 2: sin estandarizar x1 ya se apagó y x2 no; estandarizando, viven las dos."""
    est = ml.estandarizar(ml.columnas("x1", "x2"))
    ok = []
    for s in range(10):
        d = ml.caso(10, semilla=s)
        crudo = ml.ajustar(d, mu=2.0, penalizacion="l1").beta_gorro
        estd = ml.ajustar(d, phi=est, mu=2.0, penalizacion="l1").beta_gorro
        ok.append(crudo["x1"] == 0 and crudo["x2"] != 0 and estd["x1"] != 0 and estd["x2"] != 0)
    assert ok[0] and sum(ok) >= 8


def test_optimo_restringido_con_mu_diminuto():
    datos = ml.muchas_variables(n=100, J=2, utiles=2, escala={"x1": 1e-8, "x2": 1e-8})
    mc = ml.ajustar(datos).beta_gorro[["x1", "x2"]]
    d = 0.5 * float((mc ** 2).sum())
    beta, mu = ml.optimo_restringido(datos, None, "l2", d)
    assert 0 < mu < 1e-10
    assert float((beta[["x1", "x2"]] ** 2).sum()) == pytest.approx(d, rel=1e-6)
    m = ml.ajustar(datos, mu=mu, penalizacion="l2")
    assert np.allclose(m.beta_gorro, beta, rtol=1e-4)


def test_dibujar_regiones_siempre_trae_curvas_de_nivel_visibles():
    for datos, d in ((ml.caso(10), 1.0), (ml.caso(9), 100.0), (ml.caso(9), 1.0)):
        ax = ml.dibujar_regiones(datos, None, "l1", d)
        (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
        curvas = [ln for ln in ax.get_lines() if (ln.get_gid() or "").startswith("curva-nivel")]
        assert curvas
        dentro = sum(np.any((ln.get_xdata() >= x0) & (ln.get_xdata() <= x1)
                            & (ln.get_ydata() >= y0) & (ln.get_ydata() <= y1)) for ln in curvas)
        assert dentro >= 2


def test_dibujar_media_acumulada_distingue_infinito_de_no_calculado():
    ax = ml.dibujar_media_acumulada({"L": ml.lognormal()}, n_max=200, trayectorias=2,
                                    estadistico="absoluto")
    esperado = next(ln for ln in ax.get_lines() if ln.get_gid() == "esperado-L")
    assert esperado.get_ydata()[0] == pytest.approx(np.exp(0.5))
    ax = ml.dibujar_media_acumulada({"P": ml.pareto(1.5)}, n_max=200, trayectorias=2,
                                    estadistico="absoluto")
    assert any((ln.get_gid() or "") == "esperado-P" for ln in ax.get_lines())
    ax = ml.dibujar_media_acumulada({"P": ml.pareto(1.5)}, n_max=200, trayectorias=2)
    assert "valor esperado infinito" in [t.get_text() for t in ax.get_legend().get_texts()]
    rng = np.random.default_rng(0)
    assert ml._esperado(ml.pareto(1.5), "absoluto") == pytest.approx(
        np.abs(ml.pareto(1.5).muestrear(4_000_000, rng)).mean(), rel=0.03)


def test_segunda_ronda_c3():
    # estandarizar: variación real en unidades diminutas no es «constante»
    df = pd.DataFrame({"x": [0, 1e-13, 2e-13, 3e-13], "y": [0.0, 1, 2, 3]})
    E = ml.estandarizar(ml.columnas("x")).ajustar(df)(df)
    assert np.allclose(E["x"].std(ddof=0), 1.0)
    # elipses con escalas muy distintas pero rango completo
    ax = ml.dibujar_regiones(ml.caso(10, escala={"x2": 1e7}), None, "l1", 0.4)
    assert sum(1 for ln in ax.get_lines() if (ln.get_gid() or "").startswith("curva-nivel-")) == 6
    # piso infinito con base Cauchy aunque haya omitidas; 0 sin ruido con cualquier base
    d = ml.caso(9, omitir=["x2"], ruido=ml.heterocedastico(lambda _: 1.0, base=ml.cauchy()))
    assert np.isinf(ml.piso(d))
    d = ml.proceso(n=40, ruido=ml.heterocedastico(lambda d: 0.0 * d["x"], base=ml.pareto(1.5)))
    assert ml.piso(d, "absoluta") == 0.0 and ml.piso(d) == 0.0


def test_taller_3_cuenta_las_pendientes_del_modelo_final(monkeypatch):
    datos = ml.caso(24, escala=None)
    visto = {}
    real = ml.elegir

    def espia(*args, **kwargs):
        visto["s"] = real(*args, **kwargs)
        return visto["s"]

    monkeypatch.setattr(ml, "elegir", espia)
    buf = io.StringIO()
    with redirect_stdout(buf), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.taller(datos, 3, que="lagrangeano")
    s = visto["s"]
    vivas = int((s.modelo_final.beta_gorro.drop("1") != 0).sum())
    assert f"({vivas} pendientes distintas de 0" in buf.getvalue()


# --- tercera ronda de la revisión del lote c3 -----------------------------------

def _L_ent_en(datos, phi, B):
    """L_ent con el intercepto en su mejor valor, en cada columna de B (2 × m)."""
    M = ml.ajustar(datos, phi=phi).Phi(datos.ent)
    pend = [c for c in M.columns if c != "1"]
    Mc = M[pend].to_numpy(float)
    Mc = Mc - Mc.mean(axis=0)
    y = datos.ent["y"].to_numpy(float)
    return (((y - y.mean())[:, None] - Mc @ B) ** 2).mean(axis=0)


@pytest.mark.parametrize("pesada", [ml.cauchy(), ml.t_student(2), ml.pareto(1.5)])
def test_piso_con_omitida_de_cola_pesada_no_es_un_monte_carlo_finito(pesada):
    x = {"x1": ml.normal(), "x2": pesada}
    d = ml.proceso(n=40, x=x, f=lambda d: d["x1"] + d["x2"], omitir=["x2"],
                   ruido=ml.normal(0, 0), n_realidad=2000)
    assert ml.piso(d) == float("inf")
    d = ml.proceso(n=40, x=x, f=lambda d: d["x1"] + np.tanh(d["x2"]), omitir=["x2"],
                   ruido=ml.normal(0, 0), n_realidad=2000)
    with pytest.warns(UserWarning, match="piso desconocido"):
        assert np.isnan(ml.piso(d))
    d = ml.proceso(n=40, x=x, f=lambda d: d["x1"] + 0 * d["x2"], omitir=["x2"],
                   ruido=ml.normal(0, 1), n_realidad=2000)
    assert ml.piso(d) == pytest.approx(1.0, rel=0.1)


def test_estandarizar_constante_grande_no_depende_de_las_unidades():
    c = 1e9 + 0.1
    for k in (1.0, 1e-9):
        df = pd.DataFrame({"x": np.full(100, c * k), "y": np.full(100, 2.0)})
        m = ml.ajustar(df, phi=ml.estandarizar(ml.columnas("x")), columnas_x=["x"],
                       tarea="regresion")
        assert np.all(m.Phi(df)["x"].to_numpy() == 0.0)
        assert m.predecir(pd.DataFrame({"x": [1.1 * c * k]}))[0] == pytest.approx(2.0)


@pytest.mark.parametrize("ruido", [ml.cauchy(), ml.t_student(2), ml.pareto(1.5)])
def test_endogeno_pide_un_ruido_con_varianza_finita(ruido):
    with pytest.raises(ValueError, match="endogeno"):
        ml.proceso(n=40, ruido=ruido, endogeno=0.5, n_realidad=500)
    with pytest.raises(ValueError, match="endogeno"):
        ml.proceso(n=40, x={"x1": ruido}, ruido=ml.normal(), f=lambda d: d["x1"],
                   endogeno=0.5, n_realidad=500)


def test_piso_con_condicionamiento_gaussiano_conjunto():
    x = {"x1": ml.normal(), "x2": ml.normal()}
    d = ml.proceso(n=40, x=x, f=lambda d: d["x1"] + d["x2"], ruido=ml.normal(), endogeno=0.5,
                   omitir=["x1"], n_realidad=2000)
    assert ml.piso(d) == pytest.approx(2.25 + 0.75, abs=1e-12)
    desp = d.despliegue
    assert np.allclose(d.f_visible(desp), desp["x2"]) and np.allclose(desp["f_visible"], desp["x2"])
    # x2 omitida y correlacionada 0.6 con x1: E[y | x1] = 2.2·x1, piso 4·(1 − 0.36) + 1
    d = ml.proceso(n=40, x=x, correlacion={("x1", "x2"): 0.6}, f=lambda d: d["x1"] + 2 * d["x2"],
                   omitir=["x2"], escala={"y": 10.0}, n_realidad=200_000)
    assert ml.piso(d) == pytest.approx(100 * 3.56, abs=1e-9)
    desp = d.despliegue
    assert np.allclose(desp["f_visible"], 22 * desp["x1"])
    assert np.mean((desp["y"] - desp["f_visible"]) ** 2) == pytest.approx(356, rel=0.02)


def test_region_elastica_cerca_de_lasso_no_pierde_la_frontera():
    for rho in (1 - 1e-16, 1 - 1e-12, 0.5, 0.0):
        bx, by = ml._region("elastica", 0.4, rho)
        pen = (1 - rho) * (bx ** 2 + by ** 2) + rho * (np.abs(bx) + np.abs(by))
        assert np.allclose(pen, 0.4, rtol=1e-12)


def test_dibujar_regiones_rango_uno_traza_rectas_en_su_nivel():
    datos = ml.proceso(n=80, x={"x": ml.normal()}, f=lambda d: 2 * d["x"], ruido=ml.normal(0, 0.5))
    phi = ml.columnas("x", "10000000*x")
    ax = ml.dibujar_regiones(datos, phi, "l1", 0.4)
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    niveles = {}
    for ln in ax.get_lines():
        gid = ln.get_gid() or ""
        if gid.startswith("curva-nivel-"):
            B = np.vstack([ln.get_xdata(), ln.get_ydata()])
            Ls = _L_ent_en(datos, phi, B)
            assert Ls.max() - Ls.min() <= 1e-9 * Ls.max()
            dentro = (B[0] >= x0) & (B[0] <= x1) & (B[1] >= y0) & (B[1] <= y1)
            assert dentro.sum() >= 2
            niveles.setdefault(gid.rstrip("b"), []).append(Ls.mean())
    assert len(niveles) == 6 and all(len(v) == 2 for v in niveles.values())
    assert len({round(v[0], 9) for v in niveles.values()}) == 6


@pytest.mark.parametrize("datos, d", [(ml.caso(10), 0.4), (ml.caso(10, escala={"x2": 1e7}), 0.4),
                                      (ml.caso(9), 1.0)])
def test_dibujar_regiones_el_optimo_restringido_toca_su_curva(datos, d):
    """La curva gruesa (nivel 2) es la de L en el óptimo restringido, y las seis siguen
    los múltiplos 0.25, 0.5, 1, 2, 3.5, 5.5 del incremento de pérdida."""
    ax = ml.dibujar_regiones(datos, None, "l1", d)
    beta_r, _ = ml.optimo_restringido(datos, None, "l1", d)
    pend = [c for c in beta_r.index if c != "1"]
    L_r = _L_ent_en(datos, None, beta_r[pend].to_numpy(float)[:, None])[0]
    L_mc = _L_ent_en(datos, None, ml.ajustar(datos).beta_gorro[pend].to_numpy(float)[:, None])[0]
    assert L_r - L_mc > 1e-6 * L_mc  # el óptimo restringido está en la frontera
    curvas = {ln.get_gid(): ln for ln in ax.get_lines()
              if (ln.get_gid() or "").startswith("curva-nivel-")}
    for k, mult in enumerate((0.25, 0.5, 1.0, 2.0, 3.5, 5.5)):
        ln = curvas[f"curva-nivel-{k}"]
        Ls = _L_ent_en(datos, None, np.vstack([ln.get_xdata(), ln.get_ydata()]))
        assert np.allclose(Ls - L_mc, mult * (L_r - L_mc), rtol=1e-6, atol=1e-12 * L_mc)


# ---------------------------------------------------------------------------
# 8 · Lo que trae 1.4 (primer tramo del lote de la clase 4, clase_4.md §10.3 y §10.7)
# ---------------------------------------------------------------------------


def _avisos(funcion, *args, **kwargs):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        salida = funcion(*args, **kwargs)
    return salida, [str(a.message) for a in w]


def test_firmas_de_los_procesos_hilo():
    for clave, n in (("fraude", 600), ("mensajes3", 10_000)):
        params = list(inspect.signature(ml.PROCESOS[clave]).parameters.values())
        assert [p.name for p in params[:2]] == ["n", "semilla"]
        assert params[0].default == n and params[1].default == 0
        assert params[2].kind is params[2].KEYWORD_ONLY and params[2].name == "proporcion"
    assert inspect.signature(ml.PROCESOS["mensajes3"]).parameters["separar"].default == "azar"
    with pytest.raises(ValueError, match=r"proporcion=0\.05"):
        ml.PROCESOS["fraude"](0.05)
    with pytest.raises(TypeError):
        ml.PROCESOS["fraude"](600, 0, 0.05)  # la proporción solo va por nombre


def test_fraude_criterios_de_clase_4_10_3():
    """Con 0.1, la logística sin pesos tiene MCC > 0.2 en el despliegue y la moda 0. Con
    0.01 (la construcción del caso 18, n = 1000), la logística sin pesos queda a menos de
    0.1 de la moda y por debajo de la que usa pesos balanceados."""
    d = ml.PROCESOS["fraude"](proporcion=0.1)
    m = ml.ajustar(d)
    assert ml.desempeno(m, d, "mcc") > 0.2
    assert ml.benchmarks(d, d.despliegue, criterios=("mcc",)).loc["moda", "mcc"] == 0.0
    d = ml.PROCESOS["fraude"](n=1000, proporcion=0.01)
    sin = ml.desempeno(ml.ajustar(d), d, "mcc")
    con = ml.desempeno(ml.ajustar(d, pesos="balanceado"), d, "mcc")
    assert abs(sin - 0.0) < 0.1
    assert sin < con


def test_mensajes3_criterio_a_aciertos_dentro_del_fraude():
    d = ml.PROCESOS["mensajes3"]()
    y = d.despliegue["y"].to_numpy()
    for pesos, condicion in ((None, lambda a: a < 0.3), ("balanceado", lambda a: a > 0.6)):
        m = ml.ajustar(d, pesos=pesos)
        a = ml.por_clase("aciertos", y, m.predecir(d.despliegue), clases=[0, 1, 2])[2]
        assert condicion(a), (pesos, a)


def test_mensajes3_criterio_b_conformal_marginal_y_por_clase():
    """Marginal con δ = 0.1: cobertura del fraude <= 0.6 en despliegue. Por clase, en
    promedio sobre calibraciones repetidas e independientes: >= 0.9 − 2 EE."""
    d = ml.PROCESOS["mensajes3"]()
    cal, _ = ml.partir(d.val, 1 / 3, como="azar", semilla=0)
    m = ml.ajustar(d)
    marginal = ml.conformal(m, cal, delta=0.1)
    assert marginal.cobertura_por_clase(d.despliegue)[2] <= 0.6
    coberturas = []
    for s in range(1, 21):
        otra = ml.PROCESOS["mensajes3"](semilla=s, con_realidad=False)
        cal_s, _ = ml.partir(otra.val, 1 / 3, como="azar", semilla=s)
        cf = ml.conformal(m, cal_s, delta=0.1, por_clase=True)
        coberturas.append(cf.cobertura_por_clase(d.despliegue)[2])
    c = np.array(coberturas)
    assert c.mean() >= 0.9 - 2 * c.std(ddof=1) / math.sqrt(len(c))


def test_proporcion_fija_el_intercepto_en_la_poblacion():
    d = ml.proceso_clasificacion(n=200, proporcion=0.05, n_realidad=100_000)
    assert d.realidad["prob"].mean() == pytest.approx(0.05, abs=0.002)
    d3 = ml.PROCESOS["mensajes3"](n=300, proporcion=(0.7, 0.2, 0.1))
    medias = d3.realidad[["prob_0", "prob_1", "prob_2"]].mean().to_numpy()
    assert medias == pytest.approx([0.7, 0.2, 0.1], abs=0.002)
    assert d3.clases.tolist() == [0, 1, 2] and d3.K == 3
    with pytest.raises(ValueError, match="proporcion"):
        ml.proceso_clasificacion(n=50, proporcion=1.2, con_realidad=False)


def test_ruido_etiquetas_mezcla_la_prob_y_fija_el_techo():
    d = ml.proceso_clasificacion(n=400, puntaje=lambda d: 1000 * d["x1"], ruido_etiquetas=0.5)
    p = d.despliegue["prob"].to_numpy()
    assert p.min() == pytest.approx(0.25) and p.max() == pytest.approx(0.75)
    m = ml.ajustar(d)
    techo = 1 - 0.5 / 2
    a = ml.desempeno(m, d, "aciertos")
    assert a <= techo + 2 * math.sqrt(techo * (1 - techo) / len(d.despliegue))


@pytest.mark.parametrize("ruido", [ml.normal(0, 1.5), ml.efecto_grupo(10, 1.5, 0.5),
                                   ml.ar1(0.7, 1.0), ml.t_student(5)])
def test_oraculo_con_ruido_promedia_el_ruido(ruido):
    """prob es Pr(y=1 | x visibles): en realidad, dentro de grupos de prob parecida, la
    frecuencia de y = 1 coincide con la prob media (Monte Carlo, ±4 EE)."""
    d = ml.proceso_clasificacion(n=200, ruido=ruido, n_realidad=100_000, separar="azar")
    tab = ml.calibracion(d.realidad["prob"], d.realidad["y"], bins=10)
    assert np.all(np.abs(tab["frecuencia"] - tab["p_media"]) <= 4 * tab["ee"] + 1e-3)
    sin = ml.proceso_clasificacion(n=200, n_realidad=100_000)
    # el ruido aplana la probabilidad: menos casos extremos que sin ruido
    assert d.realidad["prob"].std() < sin.realidad["prob"].std()


def test_proceso_clasificacion_faltantes():
    d = ml.proceso_clasificacion(n=2000, faltantes={"x1": (0.2, "azar")})
    for parte in (d.ent, d.val, d.prueba):
        assert parte["x1"].isna().mean() == pytest.approx(0.2, abs=0.06)
        assert parte["x2"].notna().all()
    assert d.realidad["prob"].notna().all() and d.realidad["x1"].notna().all()
    dep = ml.proceso_clasificacion(n=4000, faltantes={"x1": (0.3, "depende_x")},
                                   con_realidad=False)
    todo = pd.concat([dep.ent, dep.val, dep.prueba])
    falta = todo["x1"].isna()
    assert falta.mean() == pytest.approx(0.3, abs=0.03)
    assert todo.loc[falta, "x2"].mean() > todo.loc[~falta, "x2"].mean() + 0.3
    with pytest.raises(ValueError, match="visible"):
        ml.proceso_clasificacion(n=50, faltantes={"z": (0.2, "azar")}, con_realidad=False)


def test_proceso_faltantes():
    d = ml.proceso(n=3000, faltantes={"x": (0.2, "azar")})
    for parte in (d.ent, d.val, d.prueba):
        assert parte["x"].isna().mean() == pytest.approx(0.2, abs=0.05)
    assert d.realidad["x"].notna().all() and d.despliegue["x"].notna().all()
    y = ml.proceso(n=3000, faltantes={"x": (0.3, "depende_y")}, con_realidad=False)
    todo = pd.concat([y.ent, y.val, y.prueba])
    assert todo.loc[todo["x"].isna(), "y"].mean() > todo.loc[todo["x"].notna(), "y"].mean()


def test_proceso_clasificacion_grupo():
    d = ml.proceso_clasificacion(n=600, ruido=ml.efecto_grupo(30, 1.0, 0.5), separar="grupo")
    assert "grupo" in d.ent.columns and "grupo" in d.columnas_contexto
    g = [set(p["grupo"]) for p in (d.ent, d.val, d.prueba)]
    assert not (g[0] & g[1]) and not (g[0] & g[2]) and not (g[1] & g[2])
    nuevos = ml.proceso_clasificacion(n=300, ruido=ml.efecto_grupo(30, 1.0, 0.5),
                                      separar="grupo", despliegue="grupos_nuevos")
    assert nuevos.despliegue["grupo"].min() >= 30


def test_proceso_clasificacion_tiempo():
    d = ml.proceso_clasificacion(n=400, ruido=ml.ar1(0.8, 1.0), separar="tiempo")
    assert d.val["t"].min() > d.ent["t"].max()
    assert d.prueba["t"].min() > d.val["t"].max()


def test_proceso_clasificacion_separar_sin_columna():
    with pytest.raises(ValueError, match="grupo"):
        ml.proceso_clasificacion(n=50, separar="grupo", con_realidad=False)
    with pytest.raises(ValueError, match="columna t"):
        ml.proceso_clasificacion(n=50, separar="tiempo", con_realidad=False)


def test_proceso_clasificacion_binaria_sin_novedades_no_cambio():
    """La muestra y el oráculo de una binaria sin lo nuevo son los de 1.3 (D-004)."""
    d = ml.proceso_clasificacion(n=300)
    pob = d._pob
    assert np.array_equal(d.realidad["prob"].to_numpy(),
                          1 / (1 + np.exp(-(1.5 * d.realidad["x1"] + d.realidad["x2"]))))
    assert pob.b.tolist() == [0.0, 0.0]
    import hashlib
    h = hashlib.sha256(pd.util.hash_pandas_object(d.ent).values.tobytes()).hexdigest()[:16]
    assert h == _HUELLA_BINARIA_1_3


# Huella de proceso_clasificacion(n=300).ent en 1.3 (fcb8ee7), para fijar que 1.4 no la mueve.
_HUELLA_BINARIA_1_3 = "9f9b3f5bbf03a7c8"


def test_partir_conserva_y_respeta_el_vocabulario():
    d = ml.PROCESOS["fraude"](n=1200, proporcion=0.1)
    cal, resto = ml.partir(d.val, 1 / 3)
    assert set(cal.index).isdisjoint(resto.index)
    assert sorted(cal.index.tolist() + resto.index.tolist()) == sorted(d.val.index.tolist())
    assert cal.attrs["ml"] == d.val.attrs["ml"]
    for parte, total in ((cal, 1 / 3), (resto, 2 / 3)):
        for c in (0, 1):
            esperado = (d.val["y"] == c).sum() * total
            assert abs((parte["y"] == c).sum() - esperado) <= 1
    g = ml.proceso_clasificacion(n=600, ruido=ml.efecto_grupo(30, 1, 0.5), separar="grupo")
    a, b = ml.partir(g.val.pipe(lambda v: pd.concat([g.ent, v])), 0.5, como="grupo")
    assert set(a["grupo"]).isdisjoint(b["grupo"])
    t = ml.proceso_clasificacion(n=400, ruido=ml.ar1(), separar="tiempo")
    viejo, nuevo = ml.partir(t.ent, 0.5, como="tiempo")
    assert nuevo["t"].min() > viejo["t"].max()
    with pytest.raises(ValueError, match="temporal"):
        ml.partir(d.val, 0.5, como="temporal")
    with pytest.raises(ValueError, match="grupo"):
        ml.partir(d.val, 0.5, como="grupo")


def test_mcc_gorodkin_contra_sklearn_y_contra_covarianzas():
    from sklearn.metrics import matthews_corrcoef

    rng = np.random.default_rng(0)
    for K in (2, 3, 5):
        y = rng.integers(0, K, 300)
        g = np.where(rng.uniform(size=300) < 0.6, y, rng.integers(0, K, 300))
        assert ml.mcc(y, g, clases=list(range(K))) == pytest.approx(matthews_corrcoef(y, g))
        U = np.eye(K)[y]
        V = np.eye(K)[g]
        cov = sum(np.cov(U[:, k], V[:, k], bias=True)[0, 1] for k in range(K))
        den = math.sqrt(U.var(axis=0).sum() * V.var(axis=0).sum())
        assert ml.mcc(y, g, clases=list(range(K))) == pytest.approx(cov / den)
    # binaria = correlación de las etiquetas 0/1; regla constante: 0 por convención
    y, g = np.array([0, 0, 1, 1, 1]), np.array([0, 1, 1, 1, 0])
    assert ml.mcc(y, g, clases=[0, 1]) == pytest.approx(np.corrcoef(y, g)[0, 1])
    assert ml.mcc([0, 0, 0, 1], [0, 0, 0, 0], clases=[0, 1]) == 0.0
    assert ml.mcc([0, 0, 0, 0], [0, 0, 0, 0], clases=[0, 1]) == 0.0


def test_soporte_nulo_y_clases_explicitas():
    assert ml.aciertos_balanceados([0, 0, 1, 1], [0, 0, 1, 1], clases=[0, 1]) == 1
    v, avisos = _avisos(ml.aciertos_balanceados, [0, 0, 1, 1], [0, 0, 1, 1], clases=[0, 1, 2])
    assert math.isnan(v) and any("falta la clase 2" in a for a in avisos)
    assert ml.aciertos_balanceados([0, 0, 1, 1], [0, 0, 1, 1]) == 1
    v, avisos = _avisos(ml.aciertos_balanceados, [0, 0, 0], [0, 0, 0])
    assert math.isnan(v) and any("pasa `clases=`" in a for a in avisos)
    with pytest.raises(ValueError, match="fuera"):
        ml.mcc([0, 1, 2], [0, 1, 1], clases=[0, 1])
    # la regla constante en un conjunto sin positivos: A_bal nan (no 1), MCC 0
    y0, g0 = [0] * 20, [0] * 20
    v, _ = _avisos(ml.aciertos_balanceados, y0, g0, clases=[0, 1])
    assert math.isnan(v)
    assert ml.mcc(y0, g0, clases=[0, 1]) == 0.0
    s, avisos = _avisos(ml.por_clase, "aciertos", y0, g0, clases=[0, 1])
    assert s[0] == 1 and math.isnan(s[1])
    assert any("no tiene casos en este conjunto" in a for a in avisos)
    m, _ = _avisos(ml.promediar, "aciertos", y0, g0, "macro", clases=[0, 1])
    assert math.isnan(m)
    assert ml.promediar("aciertos", y0, g0, "ponderado", clases=[0, 1]) == 1.0


def test_identidades_de_promediar():
    rng = np.random.default_rng(1)
    y = rng.choice(3, 500, p=[0.8, 0.15, 0.05])
    g = np.where(rng.uniform(size=500) < 0.7, y, rng.integers(0, 3, 500))
    cl = [0, 1, 2]
    assert ml.promediar("aciertos", y, g, "macro", clases=cl) == pytest.approx(
        ml.aciertos_balanceados(y, g, clases=cl))
    assert ml.promediar("aciertos", y, g, "ponderado", clases=cl) == pytest.approx(
        ml.aciertos(y, g))
    s = ml.por_clase("precision", y, g, clases=cl)
    assert list(s.index) == cl


def test_con_clases_en_cv_guarda_nan_en_el_pliegue_sin_positivos():
    est = ml.con_clases(ml.aciertos_balanceados, [0, 1])
    assert est.__name__ == "aciertos_balanceados" and est.__doc__ == ml.aciertos_balanceados.__doc__
    df = pd.DataFrame({"x1": np.linspace(-1, 1, 40), "y": [0] * 38 + [1, 1]})
    df.attrs["ml"] = {"columnas_x": ["x1"], "columnas_contexto": [], "tarea": "clasificacion",
                      "K": 2, "clases": [0, 1]}

    def contiguos(d):
        idx = np.arange(len(d))
        return [(np.setdiff1d(idx, b), b) for b in np.array_split(idx, 4)]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = ml.validacion_cruzada(df, lambda d: ml.ajustar(d, mu=1.0, penalizacion="l2"),
                                  particion=contiguos, estadistico=est)
    assert np.isnan(r.por_pliegue_estadistico[:3]).all()


def test_criterios_nuevos_en_evaluar_benchmarks_y_cv():
    d = ml.PROCESOS["fraude"](n=800, proporcion=0.2)
    m = ml.ajustar(d)
    val = d.val
    assert ml.evaluar(m, val, "mcc") == pytest.approx(ml.mcc(val["y"], m.predecir(val),
                                                             clases=[0, 1]))
    assert ml.evaluar(m, val, "brier") == pytest.approx(ml.brier(val["y"], m.predecir_p(val)))
    with pytest.raises(ValueError, match="riesgo"):
        ml.riesgo(m, d, "mcc")
    with pytest.raises(ValueError, match="pondera"):
        ml.evaluar(m, val, "mcc", pesos="balanceado")
    cv = ml.validacion_cruzada(d, lambda df: ml.ajustar(df), criterio="mcc",
                               particion="estratificado")
    assert len(cv.por_pliegue) == 5 and np.isnan(cv.perdidas_fuera).all()
    s = ml.elegir(d, {"x1": lambda df: ml.ajustar(df, phi=ml.columnas("x1")),
                      "x1 y x2": lambda df: ml.ajustar(df)}, con="val", criterio="mcc")
    assert s.elegido == "x1 y x2" and s.sentido == "max"
    with pytest.raises(ValueError, match="binario"):
        ml.benchmarks(ml.PROCESOS["mensajes3"](n=300), ml.PROCESOS["mensajes3"](n=300).val,
                      criterios=("brier",))


def test_benchmarks_de_clasificacion_contra_las_formulas():
    """Ajustados en ent, evaluados en el conjunto: con ȳ_ent = 0.05 y ȳ_D = 0.10, el Brier
    de la proporción es 0.10·0.95² + 0.90·0.05² = 0.0925; la logarítmica, su fórmula."""
    meta = {"columnas_x": ["x1"], "columnas_contexto": [], "tarea": "clasificacion", "K": 2,
            "clases": [0, 1]}
    ent = pd.DataFrame({"x1": 0.0, "y": [1] * 5 + [0] * 95})
    ent.attrs["ml"] = meta
    ev = pd.DataFrame({"x1": 0.0, "y": [1] * 10 + [0] * 90})
    t = ml.benchmarks(ent, ev, criterios=("brier", "logaritmica", "mcc", "aciertos_balanceados",
                                          "aciertos"))
    assert t.loc["proporcion", "brier"] == pytest.approx(0.0925)
    assert t.loc["proporcion", "logaritmica"] == pytest.approx(
        -0.10 * math.log(0.05) - 0.90 * math.log(0.95))
    assert t.loc["moda", "mcc"] == 0.0 and t.loc["moda", "aciertos_balanceados"] == 0.5
    assert list(ml.benchmarks(ent, ev).columns) == ["logaritmica", "aciertos"]


def test_pesos_de_clase():
    y = np.array([0] * 950 + [1] * 50)
    w = ml.pesos_de_clase(y)
    assert w[0] == pytest.approx(1000 / (2 * 950)) and w[1] == pytest.approx(10)
    w = ml.pesos_de_clase(y, como="razon", razon=9)
    assert w[1] / w[0] == pytest.approx(9)
    assert np.mean([w[v] for v in y]) == pytest.approx(1)
    with pytest.raises(ValueError, match="razón"):
        ml.pesos_de_clase(y, como="razon")
    w, avisos = _avisos(ml.pesos_de_clase, y, como="balanceado", razon=3)
    assert w[1] == pytest.approx(10) and avisos


def test_pesos_mueven_el_intercepto_y_no_las_pendientes():
    """Con el proceso bien especificado y n grande: β̂0(razón) − β̂0(1) ≈ ln(razón) y las
    pendientes casi no cambian (la equivalencia con el umbral de clase_4.md §10.7)."""
    d = ml.PROCESOS["fraude"](n=20_000, proporcion=0.1, con_realidad=False)
    sin = ml.ajustar(d)
    con = ml.ajustar(d, pesos={0: 1.0, 1: 9.0})
    salto = con.beta_gorro["1"] - sin.beta_gorro["1"]
    assert salto == pytest.approx(math.log(9), abs=0.15)
    assert con.beta_gorro[["x1", "x2"]].to_numpy() == pytest.approx(
        sin.beta_gorro[["x1", "x2"]].to_numpy(), abs=0.15)


def test_softmax_con_K_2_coincide_con_la_logistica():
    """Con K = 2 puntajes libres y μ, la diferencia de coeficientes es la logística con μ/2."""
    d = ml.PROCESOS["fraude"](n=500, proporcion=0.3, con_realidad=False)
    ent = d.ent
    phi = ml.estandarizar(ml.columnas("x1", "x2"))
    log = ml.ajustar(ent, phi=phi, mu=0.05, penalizacion="l2")
    M = phi.ajustar(ent)(ent).to_numpy()
    A = np.column_stack([np.ones(len(M)), M])
    Y = np.eye(2)[ent["y"].to_numpy()]
    B = ml._softmax(A, Y, np.ones(len(A)), 0.1, 0.0, np.array([False, True, True]))
    assert (B[1] - B[0]) == pytest.approx(log.beta_gorro.to_numpy(), abs=1e-5)


def test_softmax_tres_clases_kkt_y_predicciones():
    d = ml.PROCESOS["mensajes3"](n=2000, con_realidad=False)
    m = ml.ajustar(d)
    assert m.familia == "softmax" and m.beta_gorro.shape == (3, 3)
    assert list(m.beta_gorro["1"].index) == [0, 1, 2]
    P = m.predecir_prob(d.ent)
    assert P.sum(axis=1) == pytest.approx(1)
    Y = np.eye(3)[d.ent["y"].to_numpy()]
    A = m.Phi(d.ent).to_numpy()
    assert np.abs(A.T @ (P - Y) / len(A)).max() < 1e-6  # gradiente 0 sin penalizar
    assert m.beta_gorro.sum(axis=0).abs().max() < 1e-6  # Σ_k β_kj = 0
    assert ml.L(m, d.val) == pytest.approx(ml.log_loss(d.val["y"], m.predecir_prob(d.val)))
    m1 = ml.ajustar(d, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=0.05, penalizacion="l1")
    assert (m1.beta_gorro.drop(columns="1").to_numpy() == 0).any()


def test_rango_conformal_exacto():
    for (n, delta), k in (((8, 1 / 3), 6), ((9, 0.1), 9), ((5, 1 / 6), 5), ((5, 1 / 3), 4)):
        assert ml._rango_conformal(n, delta) == k
    assert ml._corte([0.1, 0.2], 0.1) == float("inf")  # índice 3 > n_cal = 2
    assert ml._corte([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 0.1) == 0.5  # empates


def test_conformal_cobertura_promedio_sobre_calibraciones():
    """La garantía promedia sobre la calibración: con R calibraciones independientes, la
    cobertura media cae en [1 − δ − 3 EE, 1 − δ + 1/(n_cal + 1) + 3 EE]."""
    d = ml.PROCESOS["fraude"](n=600, proporcion=0.3)
    m = ml.ajustar(d)
    cob, n_cal = [], None
    for s in range(1, 41):
        otra = ml.PROCESOS["fraude"](n=600, proporcion=0.3, semilla=s, con_realidad=False)
        cf = ml.conformal(m, otra.val, delta=0.1)
        n_cal = cf.n_cal
        cob.append(cf.cobertura(d.despliegue))
    c = np.array(cob)
    ee = c.std(ddof=1) / math.sqrt(len(c))
    assert 0.9 - 3 * ee <= c.mean() <= 0.9 + 1 / (n_cal + 1) + 3 * ee
    cf = ml.conformal(m, d.val, delta=0.1)
    assert cf.puntajes.shape == (len(d.val),)
    assert 0 < cf.tamano_medio(d.despliegue) <= 2
    assert set(cf.tamano_por_clase(d.despliegue).index) == {0, 1}
    conj = cf.predecir_conjunto(d.val.head(3))
    assert all(isinstance(c_, set) for c_ in conj)
    reg = ml.PROCESOS["entregas"](n=200)
    mr = ml.ajustar(reg)
    cr = ml.conformal(mr, reg.val, delta=0.2)
    lo, hi = cr.predecir_conjunto(reg.despliegue)
    assert np.all(hi - lo == pytest.approx(2 * cr.c_gorro))


def test_conformal_por_clase_avisa_si_una_clase_no_alcanza():
    d = ml.PROCESOS["fraude"](n=200, proporcion=0.05)
    m = ml.ajustar(d)
    cf, avisos = _avisos(ml.conformal, m, d.val, delta=0.1, por_clase=True)
    assert cf.c_gorro[1] == float("inf") and any("∞" in a for a in avisos)


def test_calibracion_y_recalibrar_con_platt():
    d = ml.PROCESOS["fraude"](n=4000, proporcion=0.1)
    con = ml.ajustar(d, pesos="balanceado")
    tab = ml.calibracion(con.predecir_p(d.val), d.val["y"], bins=10)
    assert list(tab.columns) == ["grupo", "p_media", "frecuencia", "n", "ee"]
    assert tab["n"].sum() == len(d.val) and tab["n"].max() - tab["n"].min() <= 1
    u = ml.calibracion(con.predecir_p(d.val), d.val["y"], bins=10, estrategia="uniforme")
    assert u["n"].sum() == len(d.val)
    # los pesos descalibran: la probabilidad media anunciada pasa de la tasa real
    assert con.predecir_p(d.despliegue).mean() > d.despliegue["y"].mean() + 0.1
    val_a, val_b = ml.partir(d.val, 0.5)
    rc = ml.recalibrar(con, val_a)
    b0, b1 = rc.hiperparametros["beta_cal"]
    assert b0 == pytest.approx(-math.log(con.pesos[1] / con.pesos[0]), abs=0.5)
    assert b1 == pytest.approx(1, abs=0.25)
    assert ml.desempeno(rc, d, "brier") < ml.desempeno(con, d, "brier")
    assert ml.L(rc, d.despliegue) < ml.L(con, d.despliegue)
    d3 = ml.PROCESOS["mensajes3"](n=3000)
    c3 = ml.ajustar(d3, pesos="balanceado")
    r3 = ml.recalibrar(c3, d3.val)
    assert ml.L(r3, d3.despliegue) < ml.L(c3, d3.despliegue)
    assert set(r3.hiperparametros["beta_cal"]) == {"pendiente", "desplazamientos"}


def test_elegir_umbral():
    d = ml.PROCESOS["fraude"](n=2000, proporcion=0.05)
    m = ml.ajustar(d)
    tau = ml.elegir_umbral(m, d.val)
    p, y = m.predecir_p(d.val), d.val["y"].to_numpy()
    mejor = max(ml.mcc(y, (p >= t).astype(int), clases=[0, 1]) for t in np.arange(0.01, 1, 0.01))
    assert ml.mcc(y, (p >= tau).astype(int), clases=[0, 1]) == pytest.approx(mejor)
    assert ml.mcc(y, (p >= tau).astype(int), clases=[0, 1]) > ml.mcc(y, m.predecir(d.val),
                                                                      clases=[0, 1])
    rej = np.array([0.3, 0.5, 0.7])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t = ml.elegir_umbral(m, d.val.assign(y=0), "aciertos", rejilla=rej)
    assert t == 0.7 or t == 0.5  # empate entre los que no predicen positivos: el más cercano a 0.5
    with pytest.raises(ValueError, match="umbral"):
        ml.elegir_umbral(m, d.val, "brier")


def _regla_constante(etiqueta, clases=(0, 1)):
    class _Constante(ml.Modelo):
        tarea, familia = "clasificacion", "constante"

        def predecir(self, df):
            return np.full(len(df), etiqueta)

    m = _Constante()
    m.clases, m.K = np.asarray(clases), len(clases)
    return m


def test_incertidumbre_esquemas():
    df = pd.DataFrame({"x1": 0.0, "y": [0] * 90 + [1] * 10})
    m = _regla_constante(0)
    est = ml.incertidumbre(m, df, "aciertos", estratificar=True, repeticiones=300)
    assert est.ee == 0 and est.intervalo == (0.9, 0.9) and est.esquema == "estratificado por clase"
    filas = ml.incertidumbre(m, df, "aciertos", repeticiones=2000)
    assert filas.ee == pytest.approx(math.sqrt(0.9 * 0.1 / 100), rel=0.15)
    assert filas.esquema == "por filas"
    d = ml.PROCESOS["fraude"](n=1500, proporcion=0.3)
    mod = ml.ajustar(d)
    inc = ml.incertidumbre(mod, d.val, "aciertos", repeticiones=2000)
    l_i = (mod.predecir(d.val) == d.val["y"].to_numpy()).astype(float)
    assert inc.ee == pytest.approx(ml.error_estandar(l_i), rel=0.1)
    assert ml.incertidumbre(mod, d.val, "mcc", contra=mod, repeticiones=50).ee == 0
    with pytest.raises(ValueError, match="esquemas"):
        ml.incertidumbre(mod, d.val, estratificar=True, grupo="grupo")
    a = ml.incertidumbre(mod, d.val, "mcc", repeticiones=200, semilla=3)
    b = ml.incertidumbre(mod, d.val, "mcc", repeticiones=200, semilla=3)
    assert a == b
    g = d.val.assign(grupo=np.arange(len(d.val)))
    por_g = ml.incertidumbre(mod, g, "aciertos", grupo="grupo", repeticiones=2000)
    assert por_g.ee == pytest.approx(inc.ee, rel=0.1) and por_g.esquema == "por grupos (grupo)"
    # estratificado en un caso no degenerado: sqrt(Σ (n_y/n)² a_y(1−a_y)/n_y)
    y = d.val["y"].to_numpy()
    acierta = mod.predecir(d.val) == y
    teo = math.sqrt(sum((np.mean(y == c)) ** 2 * acierta[y == c].mean()
                        * (1 - acierta[y == c].mean()) / np.sum(y == c) for c in (0, 1)))
    e = ml.incertidumbre(mod, d.val, "aciertos", estratificar=True, repeticiones=3000)
    assert e.ee == pytest.approx(teo, rel=0.1)


def test_dibujar_metrica_por_pliegue_marca_nan_y_convencion():
    tabla = pd.DataFrame({
        "k": [3] * 6 + [10] * 4,
        "pliegue": [0, 1, 2, 0, 1, 2, 0, 1, 0, 1],
        "metrica": ["mcc"] * 3 + ["aciertos_balanceados"] * 3 + ["mcc"] * 2
                   + ["aciertos_balanceados"] * 2,
        "valor": [0.4, 0.0, 0.5, 0.7, np.nan, 0.8, 0.3, 0.0, 0.6, np.nan],
        "raros": [2, 0, 3, 2, 0, 3, 1, 0, 1, 0],
    })
    ax = ml.dibujar_metrica_por_pliegue(tabla, k=3)
    gids = {c.get_gid(): c for c in ax.collections}
    assert len(gids["no-estimable-k3"].get_offsets()) == 1
    assert len(gids["no-estimable-k10"].get_offsets()) == 1
    assert len(gids["cero-por-convencion-k3"].get_offsets()) == 1
    raya = [ln for ln in ax.lines if ln.get_gid() == "media-aciertos_balanceados-k3"][0]
    assert raya.get_ydata()[0] == pytest.approx(0.75)
    assert "sin los nan" in ax.get_title()
    with pytest.raises(ValueError, match="k=5"):
        ml.dibujar_metrica_por_pliegue(tabla, k=5)
    ml.dibujar_metrica_por_pliegue(tabla, tema="sitio")


def test_dibujar_calibracion_humo():
    d = ml.PROCESOS["fraude"](n=1500, proporcion=0.2)
    m = ml.ajustar(d)
    tab = ml.calibracion(m.predecir_p(d.val), d.val["y"])
    ver = ml.calibracion(d.realidad["prob"], d.realidad["y"])
    ax = ml.dibujar_calibracion({"sin pesos": tab}, verdadera=ver)
    assert {ln.get_gid() for ln in ax.lines} >= {"diagonal", "verdadera", "calibracion-0"}
    ml.dibujar_calibracion(tab, histograma=False, tema="sitio")


# ---------------------------------------------------------------------------
# 9 · Lo que trae 1.5 (segundo tramo del lote de la clase 4)
# ---------------------------------------------------------------------------


def _fraude_1d(n=300, semilla=0, ruido=False):
    """Una variable: separable (puntaje 1000·x) o con ruido (puntaje 2·x)."""
    f = (lambda d: 2.0 * d["x"]) if ruido else (lambda d: 1000.0 * d["x"])
    return ml.proceso_clasificacion(n=n, x={"x": ml._DosUniformes(0.2, 1.0)}, puntaje=f,
                                    semilla=semilla, n_realidad=2000)


def test_ajustes_por_mu_es_trayectorias_y_nunca_reajusta(monkeypatch):
    d = _fraude_1d()
    phi = ml.estandarizar(ml.columnas("x"))
    mus = [1e-3, 1e-2, 1e-1]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        aj = ml.ajustes_por_mu(d, phi, "l2", mus)
        tr = ml.trayectorias(d, phi, "l2", mus)
    pd.testing.assert_frame_equal(aj.tabla, tr)
    assert aj.mus == tuple(mus)
    for mu in mus:
        assert aj.interceptos[mu] == aj.modelos[mu].beta_gorro["1"]
    # la Φ guardada es la aprendida con ent: transformar val con ella da lo mismo
    m = aj.modelo(1e-2)
    eta = m.Phi(d.val).to_numpy() @ m.beta_gorro.to_numpy()
    assert 1 / (1 + np.exp(-eta)) == pytest.approx(m.predecir_p(d.val))
    assert m.phi.centro["x"] == pytest.approx(d.ent["x"].mean())
    assert m.phi.escala["x"] == pytest.approx(d.ent["x"].std(ddof=0))

    def prohibido(*a, **k):
        raise AssertionError("no debe ajustar")

    monkeypatch.setattr(ml, "ajustar", prohibido)
    monkeypatch.setattr(ml, "ajustar_otro", prohibido)
    aj.modelo(1e-2).predecir_prob(d.val)
    with pytest.raises(ValueError, match="rejilla precalculada"):
        aj.modelo(0.5)
    fig = ml.dibujar_separable({"separable": aj}, mu=1e-2, datos={"separable": d})
    der = fig.axes[1]
    punto = [ln for ln in der.lines if ln.get_gid() == "separable-punto-0"][0]
    norma = float(np.sqrt((aj.tabla.loc[np.isclose(aj.tabla["mu"], 1e-2), "valor"] ** 2).sum()))
    assert punto.get_ydata()[0] == pytest.approx(norma)
    assert der.get_yscale() == "linear"
    with pytest.raises(ValueError, match="rejilla precalculada"):
        ml.dibujar_separable({"separable": aj}, mu=0.5)
    ml.dibujar_separable({"separable": aj}, mu=[1e-3, 1e-1], tema="sitio")


def test_ajustes_por_mu_en_softmax_y_con_pesos():
    d = ml.PROCESOS["mensajes3"](n=900, con_realidad=False)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        aj = ml.ajustes_por_mu(d, ml.estandarizar(ml.columnas("x1", "x2")), "l2", [0.01, 1.0],
                               pesos="balanceado")
    assert aj.modelos[0.01].pesos is not None
    for mu in (0.01, 1.0):  # .interceptos[mu] también en softmax
        pd.testing.assert_series_equal(aj.interceptos[mu], aj.modelos[mu].beta_gorro["1"])
    assert aj.tabla["coeficiente"].str.contains("clase").all()
    norma = aj.tabla.groupby("mu")["valor"].apply(lambda v: np.sqrt((v ** 2).sum()))
    assert norma[1.0] < norma[0.01]


def test_separable_la_norma_sube_por_decada_sin_explotar():
    d = _fraude_1d(n=40)
    con = _fraude_1d(n=200, ruido=True)
    phi = ml.estandarizar(ml.columnas("x"))
    mus = [1e-6, 1e-5, 1e-4, 1e-3]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sep = ml.ajustes_por_mu(d, phi, "l2", mus).tabla.set_index("mu")["valor"].abs()
        ruido = ml.ajustes_por_mu(con, phi, "l2", mus).tabla.set_index("mu")["valor"].abs()
    subidas = -np.diff(sep.to_numpy())  # de μ chica a grande la norma baja
    assert np.all(subidas > 0.3)
    assert np.all(sep.to_numpy()[:-1] / sep.to_numpy()[1:] < 5)  # nunca ×10 por década
    assert abs(ruido.iloc[0] - ruido.iloc[1]) < 0.05


def test_perfil_en_beta_convexo_y_a_escalones():
    d = ml.PROCESOS["fraude"](n=200, proporcion=0.3, con_realidad=False)
    t = ml.perfil_en_beta(d.ent, "x1", np.linspace(-1, 4, 61))
    perdida = t[t["criterio"] == "logaritmica"]["valor"].to_numpy()
    assert np.all(np.diff(perdida, 2) > -1e-9)
    assert set(t.columns) == {"beta1", "criterio", "valor"}
    # cada fila contra una cuenta independiente: β0 que anula la derivada, y sus métricas
    from scipy import optimize as opt, special as sp
    x, y = d.ent["x1"].to_numpy(), d.ent["y"].to_numpy()
    for b1 in (-0.5, 1.0, 2.5):
        b0 = opt.brentq(lambda b: np.mean(sp.expit(b + b1 * x) - y), -50, 50, xtol=1e-14)
        p = sp.expit(b0 + b1 * x)
        g = (p >= 0.5).astype(int)
        fila = t[np.isclose(t["beta1"], b1)].set_index("criterio")["valor"]
        assert fila["logaritmica"] == pytest.approx(np.mean(-(y * np.log(p) + (1 - y) * np.log(1 - p))))
        assert fila["aciertos"] == pytest.approx(np.mean(g == y))
        assert fila["mcc"] == pytest.approx(ml.mcc(y, g, clases=[0, 1]))
    # intercepto lejos de ±60 y una sola clase
    lejos = pd.DataFrame({"x": [100.0, 100.0], "y": [0, 1]})
    assert ml.perfil_en_beta(lejos, "x", [1.0], criterios=("logaritmica",))["valor"][0] == \
        pytest.approx(math.log(2))
    una = pd.DataFrame({"x": [0.0, 1.0], "y": [1, 1]})
    assert ml.perfil_en_beta(una, "x", [1.0], criterios=("logaritmica",))["valor"][0] == 0.0


def test_contribucion_por_clase_suma_y_pesos_balanceados():
    d = ml.PROCESOS["fraude"](n=1000, proporcion=0.05, con_realidad=False)
    m = ml.ajustar(d)
    for pesos in (None, "balanceado"):
        t = ml.contribucion_por_clase(m, d.ent, pesos=pesos)
        assert t["contribucion"].sum() == pytest.approx(m.L(d.ent, pesos=pesos))
    t = ml.contribucion_por_clase(m, d.ent, pesos="balanceado")
    assert t["fraccion_peso"].to_numpy() == pytest.approx([0.5, 0.5])
    assert t["fraccion_casos"].sum() == pytest.approx(1)


def test_efecto_de_pesos_a_los_dos_lados_del_maximo():
    d = ml.PROCESOS["fraude"](n=20_000, proporcion=0.05)
    razones = [1, 2, 3, 5, 8, 12, 19, 30, 50, 100]
    t = ml.efecto_de_pesos(d, razones)
    salto = t["beta0"] - t["beta0"].iloc[0]
    assert salto.to_numpy() == pytest.approx(t["ln_razon"].to_numpy(), abs=0.2)
    imax = int(t["mcc_tau05"].idxmax())
    assert 0 < imax < len(t) - 1
    assert t["mcc_tau05"].max() - t["mcc_tau05"].iloc[-1] > 0.1
    balanceada = (1 - 0.05) / 0.05
    jbal = int(t["aciertos_balanceados_tau05"].idxmax())
    cerca = int(np.argmin(np.abs(np.log(t["razon"]) - math.log(balanceada))))
    assert abs(jbal - cerca) <= 1
    assert np.all(np.diff(t["aciertos_tau05"].to_numpy()) <= 1e-9)


def test_metricas_vs_proporcion_dispersion_no_depende_de_repeticiones():
    def corre(rep):
        return ml.metricas_vs_proporcion([0.01], pesos=("balanceado",), metricas=("mcc",),
                                         contra=("despliegue", "val"), repeticiones=rep,
                                         tamanos_val=(120, 3000), repeticiones_val=150)
    for rep in (1, 2):
        t = corre(rep)
        v = t[(t["conjunto"] == "val") & (t["modelo"] == "balanceado")].set_index("tamano")
        assert v.loc[120, "desv"] > 3 * v.loc[3000, "desv"]
    desp = t[(t["conjunto"] == "despliegue") & (t["modelo"] == "balanceado")]
    assert np.isfinite(desp["ee"]).all() and np.isfinite(desp["desv_entre_modelos"]).all()
    assert set(t["modelo"]) == {"balanceado", "moda"}


def test_metricas_vs_proporcion_pesos_contra_sin_pesos_a_1_por_ciento():
    t = ml.metricas_vs_proporcion([0.01], n=2000, repeticiones=3)
    d = t[t["conjunto"] == "despliegue"].set_index(["modelo", "metrica"])["media"]
    # (el MCC no: con pesos balanceados a 1 % puede quedar igual o abajo; lo mide cifras_c4)
    assert d["balanceado", "aciertos_balanceados"] > d["sin pesos", "aciertos_balanceados"]
    assert d["balanceado", "aciertos"] < d["sin pesos", "aciertos"]
    assert d["moda", "mcc"] == 0.0


def test_casos_de_la_clase_4():
    assert {17, 18, 22, 25} <= set(ml.CASOS_BORDE)
    assert all(ml.CASOS_BORDE[k].clase == 4 for k in (17, 18, 22, 25))
    a, b = ml.caso(18), ml.PROCESOS["fraude"](n=1000, proporcion=0.01)
    for parte in ("ent", "val", "prueba"):
        pd.testing.assert_frame_equal(getattr(a, parte), getattr(b, parte))
    t = ml.benchmarks(a, a.despliegue, criterios=("aciertos", "mcc"))
    assert t.loc["moda", "aciertos"] == pytest.approx((a.despliegue["y"] == 0).mean())
    assert t.loc["moda", "mcc"] == 0.0
    v25, n25 = ml.caso(25), ml.caso("rara_en_el_centro")
    pd.testing.assert_frame_equal(v25.ent, n25.ent)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lin = ml.ajustar(v25, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=1e-4,
                         penalizacion="l2", pesos="balanceado")
        cua = ml.ajustar(v25, phi=ml.estandarizar(ml._phi_taller_c4("cuadratica", ["x1", "x2"])),
                         mu=1e-4, penalizacion="l2", pesos="balanceado")
    assert ml.desempeno(lin, v25, "mcc") < 0.15 < 0.5 < ml.desempeno(cua, v25, "mcc")
    # poblacional: la regla óptima para aciertos > 0.75 y la balanceada > 0.7
    real = v25.realidad
    y = real["y"].to_numpy()
    assert ml.mcc(y, (real["prob"] >= 0.5).astype(int), clases=[0, 1]) > 0.75
    assert ml.mcc(y, (real["prob"] >= 0.1).astype(int), clases=[0, 1]) > 0.7
    d22 = ml.caso(22)
    m22 = ml.ajustar(d22)
    a22 = ml.desempeno(m22, d22, "aciertos")
    assert a22 <= 0.75 + 2 * math.sqrt(0.75 * 0.25 / len(d22.despliegue))
    d17 = ml.caso(17)
    with pytest.warns(UserWarning, match="separan"):
        m17 = ml.ajustar(d17)
    assert ml.aciertos(d17.ent["y"], m17.predecir(d17.ent)) == 1.0


def test_taller_4_mapa_de_reservas(monkeypatch):
    d = ml.PROCESOS["fraude"](n=900, proporcion=0.2)
    vistos = {"benchmarks": [], "elegir": [], "recalibrar": [], "evaluar": [],
              "incertidumbre": [], "conformal": []}
    for nombre in vistos:
        original = getattr(ml, nombre)

        def espia(*a, _n=nombre, _o=original, **k):
            vistos[_n].append((a, k))
            return _o(*a, **k)

        monkeypatch.setattr(ml, nombre, espia)
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        salida = io.StringIO()
        with redirect_stdout(salida):
            ml.taller(d, 4)
    texto = salida.getvalue()
    assert "por clase" in texto  # separación estratificada
    (cal_a, _), = [(a, k) for a, k in vistos["conformal"]]
    cal = cal_a[1]
    i_cal = set(cal.index)
    assert i_cal <= set(d.val.index) and not (i_cal & set(d.ent.index))
    for nombre in ("benchmarks", "elegir", "recalibrar", "evaluar", "incertidumbre"):
        for a, k in vistos[nombre]:
            for x in list(a) + list(k.values()):
                if isinstance(x, pd.DataFrame):
                    assert not (set(x.index) & i_cal), nombre
                    assert not (set(x.index) & set(d.prueba.index)), nombre
    (ba, bk), = vistos["benchmarks"]
    assert bk["criterios"] == ("mcc", "aciertos_balanceados", "aciertos", "logaritmica")
    val_b = ba[1]
    assert set(val_b.index) <= set(d.val.index) and not (set(val_b.index) & i_cal)
    assert not [a for a in avisos if "estratificada fija" in str(a.message)]


def test_taller_4_avisos_por_clase_k_grupo_y_tiempo():
    d = ml.PROCESOS["fraude"](n=900, proporcion=0.2)
    with pytest.warns(UserWarning, match="estratificada fija"):
        with redirect_stdout(io.StringIO()):
            ml.taller(d, 4, pesos=(None,), por_clase=False)
    pocos = ml.PROCESOS["fraude"](n=300, proporcion=0.0167, semilla=3)
    raros = int((pocos.ent["y"] == 1).sum())
    if 2 <= raros < 5:
        with pytest.warns(UserWarning, match=f"k = {raros}"):
            with redirect_stdout(io.StringIO()):
                ml.taller(pocos, 4, pesos=(None,))
    g = ml.proceso_clasificacion(n=900, ruido=ml.efecto_grupo(40, 1.0, 0.5), separar="grupo",
                                 proporcion=0.3)
    with pytest.warns(UserWarning, match="no hay garantía por filas"):
        with redirect_stdout(io.StringIO()):
            ml.taller(g, 4, pesos=(None,), mu=0.01)
    t = ml.proceso_clasificacion(n=600, ruido=ml.ar1(0.5, 0.5), separar="tiempo",
                                 proporcion=0.3)
    with pytest.warns(UserWarning, match="no se sostiene"):
        with redirect_stdout(io.StringIO()):
            ml.taller(t, 4, pesos=(None,), mu=0.01)
    cal, resto = ml.partir(g.val, 1 / 3, como="grupo", semilla=g.semilla + 4)
    a, b = ml.partir(resto, 0.5, como="grupo", semilla=g.semilla + 5)
    for otra in (g.ent, a, b):
        assert set(cal["grupo"]).isdisjoint(otra["grupo"])


def test_galeria_4_sin_widgets():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with redirect_stdout(io.StringIO()) as salida:
            ml.galeria(4)
    assert "Caso 17" in salida.getvalue()


# --- 9b · Las gráficas de la clase 4 (1.5; redactadas por Codex, revisadas aquí) ---


@pytest.fixture(scope="module")
def binario():
    datos = ml.PROCESOS["fraude"](n=600, proporcion=0.2)
    modelo = ml.ajustar(datos)
    return datos, modelo, ml.conformal(modelo, datos.val, delta=0.1)


@pytest.fixture(scope="module")
def multiclase():
    datos = ml.PROCESOS["mensajes3"](n=3000)
    modelo = ml.ajustar(datos)
    return datos, modelo, ml.conformal(modelo, datos.val, delta=0.1, por_clase=True)


@pytest.fixture(scope="module")
def regresion():
    datos = ml.PROCESOS["entregas"](n=300)
    modelo = ml.ajustar(datos)
    return datos, modelo, ml.conformal(modelo, datos.val, delta=0.1)


@pytest.fixture
def perfil():
    return pd.DataFrame([
        {"beta1": b, "criterio": criterio, "valor": valor}
        for b in [2., -1., 0., 1.]
        for criterio, valor in [("logaritmica", (b - 0.5) ** 2 + 0.3),
                                ("aciertos", 0.6 + b * 0.05), ("mcc", b * 0.1)]
    ], columns=["beta1", "criterio", "valor"])


@pytest.fixture
def contribuciones():
    return {"sin pesos": pd.Series([19., 1.], index=[0, 1]),
            "balanceado": pd.Series([3., 7.], index=[0, 1])}


@pytest.fixture
def pesos():
    razones = np.array([0.25, 1., 4., 16.])
    return pd.DataFrame({
        "razon": razones, "ln_razon": np.log(razones),
        "beta0": -1.4 + 0.95 * np.log(razones),
        "pendientes": [np.array([1., -0.7])] * 4,
        "p_promedio": razones / (4 + razones), "prob_real": 0.2,
        "mcc_tau05": [0.3, 0.5, 0.6, 0.4],
        "mcc_umbral_equivalente": [0.31, 0.5, 0.61, 0.41],
        "aciertos_balanceados_tau05": [0.6, 0.7, 0.8, 0.7],
        "aciertos_tau05": [0.83, 0.86, 0.8, 0.65],
        "mcc_moda": 0., "aciertos_balanceados_moda": 0.5,
        "aciertos_moda": 0.8, "coincidencia": [0.99, 1., 0.99, 0.98],
    })


@pytest.fixture
def proporciones():
    filas = []
    for metrica in ("mcc", "aciertos_balanceados", "aciertos", "logaritmica"):
        for p in (0.01, 0.1, 0.5):
            referencia = "proporcion" if metrica == "logaritmica" else "moda"
            for modelo in ("sin pesos", "balanceado", referencia):
                filas.append(dict(proporcion=p, modelo=modelo, metrica=metrica,
                                  conjunto="despliegue", tamano=np.nan, media=0.6 + p / 10,
                                  ee=0.01, desv=np.nan, desv_entre_modelos=0.03))
            if metrica != "logaritmica":
                for n in (50, 500):
                    filas.append(dict(proporcion=p, modelo="balanceado", metrica=metrica,
                                      conjunto="val", tamano=n, media=0.65 + p / 10,
                                      ee=np.nan, desv=0.1 if n == 50 else 0.02,
                                      desv_entre_modelos=np.nan))
    return pd.DataFrame(filas, columns=["proporcion", "modelo", "metrica", "conjunto", "tamano",
                                        "media", "ee", "desv", "desv_entre_modelos"])


def artista(fig, gid):
    encontrados = fig.findobj(lambda a: a.get_gid() == gid)
    assert len(encontrados) == 1, (gid, len(encontrados))
    return encontrados[0]


NOMBRES = ["umbral", "perfil_en_beta", "contribucion_por_clase", "efecto_de_pesos",
           "promedios", "cobertura_por_clase", "metricas_vs_proporcion", "confusion",
           "conformal", "roc_pr"]


@pytest.mark.parametrize("tema", ["claro", "sitio"])
@pytest.mark.parametrize("nombre", NOMBRES)
def test_humo_temas_y_ejes(nombre, tema, binario, perfil, contribuciones, pesos, proporciones,
                          monkeypatch):
    datos, m, cf = binario
    df = datos.prueba
    y, g = df["y"], m.predecir(df)
    serie = ml.por_clase("aciertos", y, g, clases=list(m.clases))
    argumentos = {
        "umbral": (m, df), "perfil_en_beta": (perfil,),
        "contribucion_por_clase": (contribuciones,), "efecto_de_pesos": (pesos,),
        "promedios": (serie, y.value_counts()), "cobertura_por_clase": (cf, df),
        "metricas_vs_proporcion": (proporciones,),
        "confusion": (ml.matriz_confusion(y, g),), "conformal": (cf, df),
        "roc_pr": (m.predecir_p(df), y),
    }
    def no_ajustar(*args, **kwargs):
        pytest.fail("este dibujo no debe ajustar modelos")
    monkeypatch.setattr(ml, "ajustar", no_ajustar)
    n = {"umbral": 2, "efecto_de_pesos": 2, "metricas_vs_proporcion": 4, "roc_pr": 2}.get(nombre, 1)
    fig, ejes = plt.subplots(1, n)
    resultado = getattr(ml, f"dibujar_{nombre}")(*argumentos[nombre], ax=ejes, tema=tema)
    assert resultado is (fig if n > 1 else ejes)
    assert fig.get_facecolor() == to_rgba(ml._TEMAS[tema]["fondo"])
    for a in fig.axes:
        assert a.get_facecolor() == to_rgba(ml._TEMAS[tema]["panel"])
        assert a.xaxis.label.get_color() == ml._TEMAS[tema]["texto"]
    fig.canvas.draw()


@pytest.mark.parametrize("nombre", NOMBRES)
def test_firma_y_docstring(nombre):
    funcion = getattr(ml, f"dibujar_{nombre}")
    parametros = list(inspect.signature(funcion).parameters.values())
    assert [(p.name, p.default) for p in parametros[-2:]] == [("ax", None), ("tema", "claro")]
    assert "Desde: 1.5 (clase 4)." in funcion.__doc__
    assert "Ejemplo:" in funcion.__doc__
    assert len(funcion.__doc__.splitlines()) <= 8


def test_umbral_perdida_invariante_metricas_y_disposicion(binario):
    datos, m, _ = binario
    df = datos.prueba
    fig = ml.dibujar_umbral(m, df, tau=0.237, tau_elegido=0.41)
    otro = ml.dibujar_umbral(m, df, tau=0.9)
    assert fig.axes[0].get_title() == otro.axes[0].get_title()
    assert fig.axes[0].get_title() == f"pérdida logarítmica: {ml.L(m, df):.3f} (no depende de τ)"
    assert fig.axes[0].get_position().y0 > fig.axes[1].get_position().y1
    assert artista(fig, "umbral-elegido").get_xdata() == [0.41, 0.41]
    p, y = m.predecir_p(df), df["y"]
    for nombre, funcion in (("mcc", ml.mcc), ("a_bal", ml.aciertos_balanceados),
                            ("aciertos", ml.aciertos)):
        curva = artista(fig, f"curva-{nombre}")
        np.testing.assert_allclose(curva.get_xdata(), np.arange(1, 100) / 100)
        def evaluar(tau):
            g = np.where(p >= tau, m.clases[1], m.clases[0])
            return funcion(y, g) if nombre == "aciertos" else funcion(y, g, clases=list(m.clases))
        np.testing.assert_allclose(curva.get_ydata(), [evaluar(t) for t in curva.get_xdata()])
        punto = artista(fig, f"actual-{nombre}")
        np.testing.assert_allclose(punto.get_data(), [[0.237], [evaluar(0.237)]])
    for c in m.clases:
        barras = fig.findobj(lambda a: a.get_gid() == f"histograma-clase-{c}")
        assert sum(b.get_height() for b in barras) == (y == c).sum()


def test_umbral_perdida_sin_pesos(binario):
    datos, _, _ = binario
    m = ml.ajustar(datos, pesos={0: 1., 1: 4.})
    fig = ml.dibujar_umbral(m, datos.prueba)
    perdida = ml.log_loss(datos.prueba["y"], m.predecir_p(datos.prueba))
    assert f"{perdida:.3f}" in fig.axes[0].get_title()


def test_perfil_ordena_y_separa_perdida(perfil):
    ax = ml.dibujar_perfil_en_beta(perfil)
    for criterio, filas in perfil.groupby("criterio"):
        curva = artista(ax.figure, f"perfil-{criterio}")
        filas = filas.sort_values("beta1")
        np.testing.assert_allclose(curva.get_xdata(), filas["beta1"])
        np.testing.assert_allclose(curva.get_ydata(), filas["valor"])
        assert curva.axes is ax  # las tres curvas en un solo eje (contrato §5.11)
    assert len(ax.figure.axes) == 1


def test_contribuciones_normalizacion_y_porcentajes(contribuciones):
    contribuciones["pequeño"] = pd.Series([96., 4.], index=[0, 1])
    ax = ml.dibujar_contribucion_por_clase(contribuciones)
    for i, s in enumerate(contribuciones.values()):
        base = 0
        for c, fraccion in (s / s.sum()).items():
            barra = artista(ax.figure, f"contribucion-{i}-clase-{c}")
            assert barra.get_height() == pytest.approx(fraccion)
            assert barra.get_y() == pytest.approx(base)
            base += fraccion
        assert base == pytest.approx(1)
    assert len(ax.texts) == 5  # el tramo de exactamente 4 % no lleva texto
    assert ax.get_ylabel() == "fracción de L_ent"


def test_contribuciones_alinea_clases_ausentes():
    ax = ml.dibujar_contribucion_por_clase({"a": pd.Series([1., 3.], index=[0, 1]),
                                           "b": pd.Series([2.], index=[1])})
    assert artista(ax.figure, "contribucion-1-clase-0").get_height() == 0
    assert artista(ax.figure, "contribucion-1-clase-1").get_height() == 1


def test_efecto_pesos_escalas_y_referencias(pesos):
    fig = ml.dibujar_efecto_de_pesos(pesos, razon=4)
    np.testing.assert_allclose(artista(fig, "cambio-intercepto").get_ydata(), 0.95 * pesos["ln_razon"])
    referencia = artista(fig, "recta-pendiente-uno")
    np.testing.assert_allclose(referencia.get_xdata(), referencia.get_ydata())
    assert referencia.get_color() == ml._color("realidad", "claro")
    assert referencia.get_label() == "recta de pendiente 1"
    promedio = artista(fig, "probabilidad-promedio")
    np.testing.assert_allclose(promedio.get_xdata(), pesos["razon"])
    np.testing.assert_allclose(promedio.get_ydata(), pesos["p_promedio"])
    np.testing.assert_allclose(artista(fig, "probabilidad-real").get_ydata(), [0.2, 0.2])
    assert promedio.axes.get_xscale() == "log"
    for metrica in ("mcc", "aciertos_balanceados", "aciertos"):
        np.testing.assert_allclose(artista(fig, f"pesos-{metrica}").get_ydata(), pesos[f"{metrica}_tau05"])
        linea = artista(fig, f"moda-{metrica}")
        assert linea.get_linestyle() == ":"
        assert linea.get_color() == ml._color("benchmark", "claro")
        np.testing.assert_allclose(linea.get_ydata(), pesos[f"{metrica}_moda"].iloc[0])
    marcas = fig.findobj(lambda a: a.get_gid() == "razon-elegida")
    np.testing.assert_allclose(sorted(a.get_xdata()[0] for a in marcas), [np.log(4), 4, 4])


@pytest.mark.parametrize("tema", ["claro", "sitio"])
def test_efecto_pesos_fronteras_ajustes_y_umbrales(pesos, binario, tema, monkeypatch):
    datos, _, _ = binario
    original, llamadas, modelos = ml.ajustar, [], []
    def ajustar(*args, **kwargs):
        llamadas.append((args, kwargs))
        modelo = original(*args, **kwargs)
        modelos.append(modelo)
        return modelo
    monkeypatch.setattr(ml, "ajustar", ajustar)
    fig = ml.dibujar_efecto_de_pesos(pesos, razon=4, datos=datos, tema=tema)
    assert len(llamadas) == 2
    assert llamadas[0][0][0] is datos
    ybar = float((datos.ent["y"] == 1).mean())
    w0 = 1 / ((1 - ybar) + 4 * ybar)  # normalizados como en efecto_de_pesos (promedio 1)
    assert llamadas[0][1] == {"pesos": {0: w0, 1: 4 * w0}}
    assert llamadas[1][1] == {}
    for m, gid, tau in zip(modelos, ["frontera-pesos", "frontera-equivalente"], [0.5, 0.2]):
        contorno = artista(fig, gid)
        vertices = np.concatenate([p.vertices for p in contorno.get_paths()])
        assert len(vertices) > 10
        np.testing.assert_allclose(m.predecir_p(pd.DataFrame(vertices, columns=["x1", "x2"])),
                                   tau, atol=0.002)
    fig.canvas.draw()


def test_promedios_identidades_y_soporte(binario):
    datos, m, _ = binario
    y, g = datos.prueba["y"], m.predecir(datos.prueba)
    serie = ml.por_clase("aciertos", y, g, clases=list(m.clases))
    soporte = y.value_counts().iloc[::-1]
    ax = ml.dibujar_promedios(serie, soporte)
    for como in ("macro", "ponderado"):
        valor = ml.promediar("aciertos", y, g, como, clases=list(m.clases))
        np.testing.assert_allclose(artista(ax.figure, f"promedio-{como}").get_xdata(), valor)
    alturas = np.array([b.get_height() for b in ax.patches])
    np.testing.assert_allclose(alturas, 0.15 + 0.7 * soporte.reindex(serie.index) / soporte.max())
    assert np.all((alturas >= 0.15) & (alturas <= 0.85))


def test_promedios_clase_sin_soporte():
    y, g, clases = [0, 0, 0], [0, 1, 0], [0, 1]
    with pytest.warns(UserWarning, match="no tiene casos"):
        serie = ml.por_clase("aciertos", y, g, clases=clases)
    ax = ml.dibujar_promedios(serie, pd.Series([3, 0], index=clases))
    assert not ax.figure.findobj(lambda a: a.get_gid() == "promedio-macro")
    assert "macro: no estimable" in [t.get_text() for t in ax.get_legend().get_texts()]
    esperado = ml.promediar("aciertos", y, g, "ponderado", clases=clases)
    np.testing.assert_allclose(artista(ax.figure, "promedio-ponderado").get_xdata(), esperado)


@pytest.mark.parametrize("caso", ["binario", "multiclase"])
@pytest.mark.parametrize("tema", ["claro", "sitio"])
def test_cobertura_global_identidad_y_tamanos(caso, tema, request):
    datos, m, cf = request.getfixturevalue(caso)
    df = datos.prueba
    ax = ml.dibujar_cobertura_por_clase(cf, df, tema=tema)
    por_clase = cf.cobertura_por_clase(df)
    soporte = df["y"].value_counts().reindex(por_clase.index, fill_value=0)
    global_esperada = (por_clase * soporte).sum() / soporte.sum()
    np.testing.assert_allclose(artista(ax.figure, "cobertura-global").get_ydata(), global_esperada)
    np.testing.assert_allclose(global_esperada, cf.cobertura(df))
    np.testing.assert_allclose(artista(ax.figure, "cobertura-objetivo").get_ydata(), 0.9)
    for i, c in enumerate(m.clases):
        assert artista(ax.figure, f"cobertura-clase-{i}").get_height() == por_clase[c]
        assert f"{cf.tamano_por_clase(df)[c]:.2f}" in artista(ax.figure, f"tamano-clase-{i}").get_text()
    assert ax.get_title() == ("por clase" if cf.por_clase else "marginal")
    ax.figure.canvas.draw()


def test_metricas_bandas_errores_referencias_y_orden(proporciones):
    fig = ml.dibujar_metricas_vs_proporcion(proporciones)
    assert [a.get_title() for a in fig.axes] == ["MCC", "A_bal", "aciertos", "pérdida logarítmica"]
    bandas = fig.findobj(lambda a: (a.get_gid() or "").startswith("banda-"))
    assert len(bandas) == proporciones.loc[proporciones["conjunto"] == "val", "metrica"].nunique()
    for metrica in proporciones["metrica"].unique():
        referencia = artista(fig, f"referencia-{metrica}")
        assert referencia.get_label() == ("proporción" if metrica == "logaritmica" else "moda")
        assert referencia.get_linestyle() == ":"
        assert referencia.get_color() == ml._color("benchmark", "claro")
        assert referencia.axes.get_xscale() == "log"
        assert referencia.axes.get_legend().get_title().get_text() == (
            "puntos: despliegue ± 2 EE Monte Carlo; banda: dispersión entre validaciones")
        cont = referencia.axes.containers[0]
        puntos = cont.lines[0]
        for segmento, x, y in zip(cont.lines[2][0].get_segments(), puntos.get_xdata(), puntos.get_ydata()):
            np.testing.assert_allclose(segmento, [[x, y - 0.02], [x, y + 0.02]])
        if metrica != "logaritmica":
            banda = artista(fig, f"banda-{metrica}")
            assert banda.get_label() == "validación de n = 50, ±2 desv"
            vertices = banda.get_paths()[0].vertices
            for p in (0.01, 0.1, 0.5):
                limites = vertices[np.isclose(vertices[:, 0], p), 1]
                assert limites.min() == pytest.approx(0.65 + p / 10 - 0.2)
                assert limites.max() == pytest.approx(0.65 + p / 10 + 0.2)


def test_metricas_un_panel_acepta_secuencia_y_sin_banda(proporciones):
    tabla = proporciones[proporciones["metrica"] == "logaritmica"]
    fig, ax = plt.subplots()
    assert ml.dibujar_metricas_vs_proporcion(tabla, ax=[ax]) is fig
    assert len(fig.axes) == 1
    assert not fig.findobj(lambda a: (a.get_gid() or "").startswith("banda-"))
    assert len(ml.dibujar_metricas_vs_proporcion(tabla).axes) == 1


def test_confusion_conteos_y_orientacion():
    matriz = ml.matriz_confusion([0, 0, 0, 1, 1], [0, 1, 1, 1, 1])
    ax = ml.dibujar_confusion(matriz)
    np.testing.assert_array_equal(artista(ax.figure, "mapa-confusion").get_array(), matriz)
    for i in range(2):
        for j in range(2):
            texto = artista(ax.figure, f"conteo-{i}-{j}")
            assert texto.get_text() == str(matriz.iloc[i, j])
            assert texto.get_position() == (j, i)
    assert (ax.get_xlabel(), ax.get_ylabel()) == ("predicha", "real")


@pytest.mark.parametrize("caso", ["binario", "multiclase"])
@pytest.mark.parametrize("tema", ["claro", "sitio"])
def test_conformal_conjuntos_y_titulo_global(caso, tema, request):
    datos, m, cf = request.getfixturevalue(caso)
    df = datos.prueba
    ax = ml.dibujar_conformal(cf, df, tema=tema)
    celdas = artista(ax.figure, "conjuntos-conformales").get_offsets()
    esperado = [(list(m.clases).index(c), i)
                for i, conjunto in enumerate(cf.predecir_conjunto(df.iloc[:40])) for c in conjunto]
    assert set(map(tuple, celdas)) == set(esperado)
    reales = artista(ax.figure, "clases-reales").get_offsets()
    assert len(reales) == 40
    np.testing.assert_array_equal(reales[:, 0], df.iloc[:40]["y"])
    assert f"cobertura: {cf.cobertura(df):.3f}" in ax.get_title()
    assert f"tamaño medio: {cf.tamano_medio(df):.3f}" in ax.get_title()
    ax.figure.canvas.draw()


@pytest.mark.parametrize("tema", ["claro", "sitio"])
def test_conformal_regresion_intervalos_y_exclusiones(regresion, tema):
    datos, m, cf = regresion
    df = datos.prueba.copy()
    df.loc[df.index[0], "y"] = 1e9  # garantiza un caso fuera
    ax = ml.dibujar_conformal(cf, df, tema=tema)
    ordenado = df.sort_values(m.columnas_x[0])
    x = ordenado[m.columnas_x[0]].to_numpy()
    pred = m.predecir(ordenado)
    np.testing.assert_allclose(artista(ax.figure, "prediccion-conformal").get_data(), [x, pred])
    vertices = artista(ax.figure, "banda-conformal").get_paths()[0].vertices
    for xx, yy in zip(x, pred):
        limites = vertices[np.isclose(vertices[:, 0], xx, rtol=0, atol=1e-12), 1]
        assert limites.min() == pytest.approx(yy - cf.c_gorro)
        assert limites.max() == pytest.approx(yy + cf.c_gorro)
    fuera = np.abs(ordenado["y"].to_numpy() - pred) > cf.c_gorro
    np.testing.assert_allclose(artista(ax.figure, "casos-fuera").get_offsets(),
                               np.column_stack([x[fuera], ordenado["y"].to_numpy()[fuera]]))
    assert ax.get_title() == f"cobertura: {cf.cobertura(df):.3f}"
    ax.figure.canvas.draw()


def area_titulo(ax):
    return float(re.search(r"área: ([0-9.]+)", ax.get_title())[1])


def test_roc_perfecta_azar_y_base_positivos():
    fig = ml.dibujar_roc_pr([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1])
    assert [area_titulo(a) for a in fig.axes] == [1., 1.]
    rng = np.random.default_rng(211)
    y = rng.binomial(1, 0.3, 20000)
    fig = ml.dibujar_roc_pr(rng.random(len(y)), y)
    assert area_titulo(fig.axes[0]) == pytest.approx(0.5, abs=0.02)
    assert area_titulo(fig.axes[1]) == pytest.approx(y.mean(), abs=0.02)
    np.testing.assert_allclose(artista(fig, "proporcion-positivos").get_ydata(), y.mean())


def test_roc_empates_no_dependen_del_orden():
    uno = ml.dibujar_roc_pr([0.5] * 4, [0, 0, 1, 1])
    dos = ml.dibujar_roc_pr([0.5] * 4, [1, 0, 1, 0])
    assert area_titulo(uno.axes[0]) == 0.5
    np.testing.assert_allclose(artista(uno, "curva-roc").get_data(), [[0, 1], [0, 1]])
    for gid in ("curva-roc", "curva-precision-sensibilidad"):
        np.testing.assert_array_equal(artista(uno, gid).get_data(), artista(dos, gid).get_data())


@pytest.mark.parametrize("nombre,tabla", [("perfil_en_beta", "perfil"),
                                          ("efecto_de_pesos", "pesos"),
                                          ("metricas_vs_proporcion", "proporciones")])
def test_tablas_validan_todas_las_columnas(nombre, tabla, request):
    tabla = request.getfixturevalue(tabla)
    funcion = getattr(ml, f"dibujar_{nombre}")
    for columna in tabla:
        with pytest.raises(ValueError, match="faltan las columnas"):
            funcion(tabla.drop(columns=columna))
    with pytest.raises(ValueError, match="vacía"):
        funcion(tabla.iloc[:0])


def test_validacion_modelos_y_datos(binario, multiclase, regresion, pesos):
    datos, m, cf = binario
    with pytest.raises(ValueError, match="binaria"):
        ml.dibujar_umbral(multiclase[1], multiclase[0].prueba)
    with pytest.raises(ValueError, match="umbrales"):
        ml.dibujar_umbral(m, datos.prueba, tau=-0.1)
    with pytest.raises(ValueError, match="faltan las columnas"):
        ml.dibujar_umbral(m, datos.prueba.drop(columns="y"))
    with pytest.raises(ValueError, match="largos distintos"):
        ml.dibujar_umbral(SimpleNamespace(K=2, columnas_x=m.columnas_x,
                                         predecir_p=lambda df: np.zeros(3)), datos.prueba)
    with pytest.raises(ValueError, match="necesita razon"):
        ml.dibujar_efecto_de_pesos(pesos, datos=datos)
    with pytest.raises(ValueError, match="binaria"):
        ml.dibujar_efecto_de_pesos(pesos, razon=4, datos=multiclase[0])
    with pytest.raises(ValueError, match="razón = 1"):
        ml.dibujar_efecto_de_pesos(pesos[pesos["razon"] != 1])
    with pytest.raises(ValueError, match="clasificación"):
        ml.dibujar_cobertura_por_clase(regresion[2], regresion[0].prueba)
    for funcion in (ml.dibujar_conformal, ml.dibujar_cobertura_por_clase):
        with pytest.raises(ValueError, match="faltan las columnas"):
            funcion(cf, datos.prueba.drop(columns="y"))
        with pytest.raises(ValueError, match="fuera de clases"):
            funcion(cf, datos.prueba.assign(y=7))


@pytest.mark.parametrize("prob,y,mensaje", [([0.2], [0, 1], "mismo largo"),
                                           ([0.1, 0.2], [0, 0], "ambas clases"),
                                           ([0.1, 0.2], [0, 2], "ambas clases"),
                                           ([np.nan, 0.2], [0, 1], "probabilidades"),
                                           ([-0.1, 1.2], [0, 1], "probabilidades")])
def test_roc_valida(prob, y, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        ml.dibujar_roc_pr(prob, y)


def test_series_y_matrices_invalidas():
    with pytest.raises(ValueError, match="mismo largo"):
        ml.dibujar_promedios(pd.Series([1., 2.]), pd.Series([1.]))
    with pytest.raises(ValueError, match="mismas clases"):
        ml.dibujar_promedios(pd.Series([1.], index=[0]), pd.Series([1.], index=[1]))
    with pytest.raises(ValueError, match="no negativo"):
        ml.dibujar_promedios(pd.Series([1.]), pd.Series([-1.]))
    for valores in ([0., 0.], [-1., 2.], [np.inf, 1.]):
        with pytest.raises(ValueError, match="total positivo"):
            ml.dibujar_contribucion_por_clase({"a": pd.Series(valores)})
    with pytest.raises(ValueError, match="desconocidas"):
        ml.dibujar_contribucion_por_clase({"a": pd.Series([np.nan])})
    with pytest.raises(ValueError, match="cuadrada"):
        ml.dibujar_confusion(pd.DataFrame([[1, 2]]))
    with pytest.raises(ValueError, match="conteos enteros"):
        ml.dibujar_confusion(pd.DataFrame([[0.5]]))


def test_numero_de_ejes_invalido(binario, pesos, proporciones):
    datos, m, _ = binario
    _, ax = plt.subplots()
    for funcion, args in [(ml.dibujar_umbral, (m, datos.prueba)),
                           (ml.dibujar_roc_pr, ([0.1, 0.9], [0, 1])),
                           (ml.dibujar_efecto_de_pesos, (pesos,)),
                           (ml.dibujar_metricas_vs_proporcion, (proporciones,))]:
        with pytest.raises(ValueError, match="ejes"):
            funcion(*args, ax=[ax])


# --- 9c · Arreglos de la revisión adversarial de 1.4 (codex-rev-lab-c4.i1) ---


def test_oraculo_con_ruido_normal_ancho_converge():
    """Con ruido N(0, 30²), la prob anunciada coincide con la integral independiente
    (24 nodos de Gauss–Hermite daban 0.620 donde se pedía 0.6)."""
    from scipy import integrate, special, stats

    d = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=lambda d: 0 * d["x1"],
                                 ruido=ml.normal(0, 30), proporcion=0.6, n_realidad=2000)
    b = d._pob.b[1]
    ref = integrate.quad(lambda e: special.expit(b + e) * stats.norm.pdf(e, 0, 30),
                         -400, 400, points=[-b], limit=500)[0]
    assert d.realidad["prob"].iloc[0] == pytest.approx(ref, abs=1e-6)
    assert ref == pytest.approx(0.6, abs=1e-4)
    for s in (0.5, 3.0, 300.0):
        regla = ml._normal_mezcla([0.3], [1.0], s)
        for z in (-9.0, 0.0, 4.0):
            r = integrate.quad(lambda e: special.expit(z + e) * stats.norm.pdf(e, 0.3, s),
                               0.3 - 12 * s, 0.3 + 12 * s, points=[-z], limit=1000)[0]
            assert ml._p1_binaria(np.array([z]), regla)[0] == pytest.approx(r, abs=1e-6)


def test_oraculo_de_una_pieza_sin_cuantiles_usa_sorteos_fijos():
    class Cero(ml.Pieza):
        nombre, media, varianza = "cero", 0.0, 0.0

        def muestrear(self, n, rng):
            return np.zeros(n)

    d = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=lambda d: 0 * d["x1"],
                                 ruido=Cero(), n_realidad=1000)
    assert d.realidad["prob"].to_numpy() == pytest.approx(0.5)
    assert ml.piso(d, "logaritmica") == pytest.approx(math.log(2))


def test_interceptos_lejanos_y_cache_sin_redondeo():
    d = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=lambda d: 100 + 0 * d["x1"],
                                 proporcion=0.1, n_realidad=1000)
    assert d._pob.b[1] == pytest.approx(math.log(0.1 / 0.9) - 100, abs=1e-6)
    f = lambda d: 0 * d["x1"]  # noqa: E731
    a = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=f, proporcion=1e-16,
                                 con_realidad=False)._pob.b[1]
    b = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=f, proporcion=1e-20,
                                 con_realidad=False)._pob.b[1]
    assert b < a - 5
    u = ml.proceso_clasificacion(n=50, ruido_etiquetas=1.0, proporcion=0.5, con_realidad=False)
    assert u._pob.b.tolist() == [0.0, 0.0]


def test_faltantes_leen_los_datos_completos_y_topan_la_fraccion():
    d = ml.proceso_clasificacion(n=20_000, faltantes={"x1": (0.2, "azar"),
                                                      "x2": (0.2, "depende_x")},
                                 con_realidad=False, fracciones=(1, 0, 0))
    assert d.ent["x1"].isna().mean() == pytest.approx(0.2, abs=0.01)
    assert d.ent["x2"].isna().mean() == pytest.approx(0.2, abs=0.01)
    with pytest.raises(ValueError, match="0.5"):
        ml.proceso_clasificacion(n=50, faltantes={"x1": (0.8, "depende_x")}, con_realidad=False)


def test_politica_de_una_sola_clase_en_por_clase_y_promediar():
    s, avisos = _avisos(ml.por_clase, "aciertos", [0, 0], [0, 0])
    assert s.isna().all() and any("pasa `clases=`" in a for a in avisos)
    v, avisos = _avisos(ml.promediar, "aciertos", [0, 0], [0, 0])
    assert math.isnan(v) and avisos


def test_etiquetas_fuera_de_las_clases_lanzan_en_brier_y_recalibrar():
    d = ml.PROCESOS["fraude"](n=400, proporcion=0.3)
    m = ml.ajustar(d)
    mala = d.val.assign(y=2)
    with pytest.raises(ValueError, match="fuera"):
        ml.recalibrar(m, mala)
    with pytest.raises(ValueError, match="fuera"):
        ml.evaluar(m, mala, "brier")


def test_calibracion_por_cuantiles_no_parte_empates():
    t = ml.calibracion([0.5] * 100, [0] * 50 + [1] * 50)
    assert len(t) == 1 and t["frecuencia"].iloc[0] == 0.5
    p = np.r_[np.full(60, 0.2), np.linspace(0.3, 0.9, 40)]
    y = (np.random.default_rng(0).uniform(size=100) < p).astype(int)
    orden = np.random.default_rng(1).permutation(100)
    pd.testing.assert_frame_equal(ml.calibracion(p, y), ml.calibracion(p[orden], y[orden]))


def test_pesos_que_suman_cero_lanzan():
    d = ml.PROCESOS["mensajes3"](n=100, con_realidad=False)
    with pytest.raises(ValueError, match="suman 0"):
        ml.ajustar(d, pesos={0: 0, 1: 0, 2: 0}, mu=0.1, penalizacion="l2")


def test_conformal_en_un_conjunto_vacio():
    d = ml.PROCESOS["fraude"](n=400, proporcion=0.3)
    cf = ml.conformal(ml.ajustar(d), d.val)
    assert math.isnan(cf.cobertura(d.val.iloc[:0]))
    assert cf.cobertura_por_clase(d.val.iloc[:0]).isna().all()


def test_softmax_l1_cumple_kkt():
    """Lasso y elástica en softmax: gradiente 0 en los interceptos; |g| <= μρ en los ceros;
    g + μρ·signo + 2μ(1−ρ)β = 0 en los activos (mata «todo en cero»)."""
    d = ml.PROCESOS["mensajes3"](n=1500, con_realidad=False)
    for pen, rho in (("l1", 1.0), ("elastica", 0.5)):
        mu = 0.02
        m = ml.ajustar(d, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=mu, penalizacion=pen,
                       rho=0.5)
        A = m.Phi(d.ent).to_numpy()
        Y = np.eye(3)[d.ent["y"].to_numpy()]
        G = ((m.predecir_prob(d.ent) - Y).T @ A) / len(A)
        B = m.beta_gorro.to_numpy()
        assert np.abs(G[:, 0]).max() < 1e-6
        activos = B[:, 1:] != 0
        assert activos.any()
        g, b = G[:, 1:], B[:, 1:]
        r = 1.0 if pen == "l1" else 0.5
        assert np.abs(g[~activos]).max(initial=0) <= mu * r + 1e-6
        resto = g + mu * r * np.sign(b) + 2 * mu * (1 - r) * b
        assert np.abs(resto[activos]).max() < 1e-5


def test_conformal_por_clase_es_el_estadistico_de_orden_de_cada_clase():
    d = ml.PROCESOS["mensajes3"](n=6000)
    m = ml.ajustar(d)
    cf = ml.conformal(m, d.val, delta=0.1, por_clase=True)
    P = m.predecir_prob(d.val)
    y = d.val["y"].to_numpy()
    for c in (0, 1, 2):
        ci = np.sort(1 - P[y == c, c])
        k = ml._rango_conformal(len(ci), 0.1)
        assert k <= len(ci)
        assert cf.c_gorro[c] == ci[k - 1] and np.isfinite(cf.c_gorro[c])


def test_dibujar_pliegues_dibuja_la_particion_recibida():
    """codex-rev-c4-6: el conteo de pliegues sin raros del título es el de la partición que
    se pasa, y cambia cuando cambia la partición (40 casos, 3 raros)."""
    df = pd.DataFrame({"x1": np.arange(40.0), "y": [0] * 37 + [1] * 3})
    df.attrs["ml"] = {"columnas_x": ["x1"], "columnas_contexto": [], "tarea": "clasificacion",
                      "K": 2, "clases": [0, 1]}
    y = df["y"].to_numpy()
    cuentas = []
    for como in ("azar", "estratificado"):
        part = ml.pliegues(df, 5, como=como)
        vacios = sum(not np.any(y[v] == 1) for _, v in part)
        ax = ml.dibujar_pliegues(40, 5, y=y, particion=part)
        assert f"{vacios} de 5 pliegues" in ax.get_title()
        cuentas.append(vacios)
    assert cuentas[0] != cuentas[1] and cuentas[1] == 2


def test_validaciones_frescas_son_iid_del_proceso():
    """codex-rev-lab-c4.i2: con n_realidad = 100 y tamaño 100, submuestrear realidad sin
    reemplazo daba siempre los mismos casos (desv ≈ 0); con validaciones frescas, la desv
    de los aciertos es la binomial."""
    t = ml.metricas_vs_proporcion(
        [0.3], pesos=(None,), metricas=("aciertos",), contra=("despliegue", "val"),
        tamanos_val=(100,), repeticiones_val=200,
        fabrica_por_proporcion=lambda p, s: ml.PROCESOS["fraude"](n=200, semilla=s, proporcion=p,
                                                               n_realidad=100))
    v = t[t["conjunto"] == "val"].iloc[0]
    assert v["desv"] == pytest.approx(math.sqrt(v["media"] * (1 - v["media"]) / 100), rel=0.25)
    fig = ml.dibujar_metricas_vs_proporcion(ml.metricas_vs_proporcion([0.1], metricas=("mcc",)))
    assert fig is not None  # repeticiones=1: ee nan, punto sin barra


def test_efecto_de_pesos_dibuja_con_la_phi_de_la_tabla():
    d = ml.caso(25, n_realidad=4000)
    phi = ml.estandarizar(ml._phi_taller_c4("cuadratica", ["x1", "x2"]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        t = ml.efecto_de_pesos(d, [1, 9], mu=1e-4, phi=phi)
        llamadas = []
        original = ml.ajustar

        def espia(*a, **k):
            llamadas.append(k)
            return original(*a, **k)

        ml.ajustar = espia
        try:
            ml.dibujar_efecto_de_pesos(t, razon=9, datos=d)
        finally:
            ml.ajustar = original
    assert llamadas and all(repr(k.get("phi")) == repr(phi) and k.get("mu") == 1e-4
                            for k in llamadas)
    ybar = float((d.ent["y"] == 1).mean())
    w0 = 1 / ((1 - ybar) + 9 * ybar)
    con_pesos = [k["pesos"] for k in llamadas if k.get("pesos")]
    assert con_pesos == [{0: w0, 1: 9 * w0}]  # los mismos pesos normalizados de la tabla


def test_softmax_con_ruido_ancho_es_exacto():
    """Con el ruido común a z_1…z_{K−1}, K > 2 se reduce a una integral binaria exacta."""
    from scipy import integrate, special, stats

    c = 21 - math.log(2)
    d = ml.proceso_clasificacion(n=30, K=3, x={"x1": ml.normal()},
                                 puntajes=[lambda q: 0 * q["x1"], lambda q: c + 0 * q["x1"],
                                           lambda q: c + 0 * q["x1"]],
                                 ruido=ml.normal(0, 300), n_realidad=500, separar="azar")
    ref = integrate.quad(lambda e: (1 - special.expit(e + 21)) * stats.norm.pdf(e, 0, 300),
                         -4000, 4000, points=[-21], limit=1000)[0]
    assert d.realidad["prob_0"].iloc[0] == pytest.approx(ref, abs=1e-6)
    assert d.realidad["prob_1"].iloc[0] == pytest.approx((1 - ref) / 2, abs=1e-6)
    p3 = ml.PROCESOS["mensajes3"](n=300, ruido=ml.normal(0, 3), n_realidad=20_000)
    medias = p3.realidad[["prob_0", "prob_1", "prob_2"]].mean().to_numpy()
    assert medias == pytest.approx([0.90, 0.08, 0.02], abs=0.003)


def test_taller_4_imprime_intervalos_y_calibra_con_k_3():
    d = ml.PROCESOS["mensajes3"](n=1500, n_realidad=3000)
    llamadas = []
    original = ml.recalibrar

    def espia(*a, **k):
        llamadas.append(a)
        return original(*a, **k)

    ml.recalibrar = espia
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with redirect_stdout(io.StringIO()) as salida:
                ml.taller(d, 4, pesos=(None,), mu=0.01)
    finally:
        ml.recalibrar = original
    assert llamadas
    assert "percentiles 2.5–97.5" in salida.getvalue() and "MCC" in salida.getvalue()


def test_interceptos_k3_con_puntajes_lejanos():
    """codex-rev-lab-c4.i3: con puntajes constantes [0, 10, 0] el arranque log(p/p0) dejaba
    al solver sin converger; el arranque convexo lo resuelve."""
    d = ml.proceso_clasificacion(n=50, K=3, x={"x1": ml.normal()},
                                 puntajes=[lambda q: 0 * q["x1"], lambda q: 10 + 0 * q["x1"],
                                           lambda q: 0 * q["x1"]],
                                 proporcion=[0.8, 0.15, 0.05], n_realidad=500, separar="azar")
    assert d._pob.b[1:] == pytest.approx([-11.67397643, -2.77258872], abs=1e-6)


# ---------------------------------------------------------------------------
# 10 · Revisión c4 de 1.5: cachés, cuadratura, etiquetas ajenas y conformal exacto


class _ConstanteRuido(ml.Pieza):
    """Pieza del taller con el repr heredado «constante()»: su repr no dice v."""
    nombre = "constante"

    def __init__(self, v):
        self.v = float(v)

    def muestrear(self, n, rng):
        return np.full(n, self.v)


def _cero(d):
    return 0.0 * d["x1"]


def test_cache_de_poblacion_distingue_ruidos_con_el_mismo_repr():
    a = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                 ruido=_ConstanteRuido(0), n_realidad=2000)
    b = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                 ruido=_ConstanteRuido(10), n_realidad=2000)
    assert a.realidad["prob"].to_numpy() == pytest.approx(0.5, abs=1e-12)
    assert b.realidad["prob"].to_numpy() == pytest.approx(special_expit(10), abs=1e-9)
    c = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                 ruido=_ConstanteRuido(0), proporcion=0.5, n_realidad=2000)
    d = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                 ruido=_ConstanteRuido(10), proporcion=0.5, n_realidad=2000)
    assert c.realidad["prob"].to_numpy() == pytest.approx(0.5, abs=1e-9)
    assert d.realidad["prob"].to_numpy() == pytest.approx(0.5, abs=1e-9)


def special_expit(z):
    from scipy import special
    return float(special.expit(z))


def test_oraculo_integra_ruidos_discretos_y_uniformes_anchos_exactos():
    disc = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                    ruido=ml.categorica([-100, 100], [0.494, 0.506]),
                                    n_realidad=2000)
    assert disc.realidad["prob"].to_numpy() == pytest.approx(0.506, abs=1e-9)
    prop = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=_cero,
                                    ruido=ml.categorica([-100, 100], [0.494, 0.506]),
                                    proporcion=0.5, n_realidad=2000)
    assert prop.realidad["prob"].mean() == pytest.approx(0.5, abs=1e-6)

    def diez(d):
        return 10.0 + 0.0 * d["x1"]

    ancho = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=diez,
                                     ruido=ml.uniforme(-1000, 1000), n_realidad=2000)
    assert ancho.realidad["prob"].to_numpy() == pytest.approx(0.505, abs=1e-9)
    # una pieza continua con cuantiles (t de 1 gl, escala enorme) converge a la cuenta exacta
    t = ml.proceso_clasificacion(n=50, x={"x1": ml.normal()}, puntaje=diez,
                                 ruido=ml.t_student(1, 1000), n_realidad=2000)
    from scipy import integrate, stats as st
    exacto = integrate.quad(lambda e: special_expit(10 + e) * st.t.pdf(e, 1, scale=1000),
                            -np.inf, np.inf, limit=500)[0]
    assert t.realidad["prob"].to_numpy() == pytest.approx(exacto, abs=1e-6)


def test_proporcion_con_categorica_de_texto():
    d = ml.proceso_clasificacion(n=50, x={"tipo": ml.categorica(["a", "b"])},
                                 puntaje=lambda d: (d.tipo == "b").astype(float),
                                 proporcion=0.2, con_realidad=False)
    assert len(d.ent) > 0


def test_rango_conformal_conserva_fracciones_exactas():
    from fractions import Fraction
    assert ml._rango_conformal(9, Fraction(9999999, 100000000)) == 10
    assert ml._rango_conformal(9, 0.09999999) == 10
    assert ml._rango_conformal(9, 0.3) == 7      # 0.3 en flotante no sube a 8
    assert ml._rango_conformal(9, 0.1) == 9
    assert ml._rango_conformal(10, 1e-8) == 11
    assert ml._corte(np.arange(1, 10), 0.09999999) == float("inf")


def test_etiquetas_ajenas_al_problema_lanzan():
    with pytest.raises(ValueError, match="y"):
        ml.log_loss([2], [0.9])
    ent = pd.DataFrame({"y": [0, 1, 0, 1]})
    ent.attrs["ml"] = {"tarea": "clasificacion", "clases": [0, 1]}
    with pytest.raises(ValueError, match="clase"):
        ml.benchmarks(ent, pd.DataFrame({"y": [2, 2]}), criterios=("brier",))
    d = ml.PROCESOS["fraude"](n=600, proporcion=0.3, con_realidad=False)
    m = ml.ajustar(d)
    with pytest.raises(ValueError, match="clase"):
        ml.contribucion_por_clase(m, d.ent.assign(y=2))


def test_incertidumbre_por_grupos_remuestrea_grupos_completos():
    df = pd.DataFrame({"x1": 0.0, "grupo": np.repeat(np.arange(10), 10),
                       "y": np.repeat([0] * 5 + [1] * 5, 10)})
    m = _regla_constante(0)
    g = ml.incertidumbre(m, df, "aciertos", grupo="grupo", repeticiones=3000)
    f = ml.incertidumbre(m, df, "aciertos", repeticiones=3000)
    assert g.ee == pytest.approx(math.sqrt(0.25 / 10), rel=0.1)   # 0.158
    assert f.ee == pytest.approx(math.sqrt(0.25 / 100), rel=0.1)  # 0.050


def test_por_clase_precision_valores_y_clase_sin_predicciones():
    s = ml.por_clase("precision", [0, 0, 1, 1], [0, 0, 0, 1], clases=[0, 1])
    assert s.to_numpy() == pytest.approx([2 / 3, 1.0])
    s, avisos = _avisos(ml.por_clase, "precision", [0, 0, 1, 1], [0, 0, 0, 0], clases=[0, 1])
    assert s.iloc[0] == pytest.approx(0.5) and math.isnan(s.iloc[1])
    assert avisos


def test_elegir_umbral_desempata_hacia_medio():
    class _Fija(ml.Modelo):
        tarea, familia = "clasificacion", "constante"

        def predecir_p(self, df):
            return np.full(len(df), 0.1)

    m = _Fija()
    m.clases, m.K = np.asarray([0, 1]), 2
    df = pd.DataFrame({"x1": 0.0, "y": [0, 0, 1, 1]})
    for metrica in ("aciertos", "mcc", "aciertos_balanceados"):
        assert ml.elegir_umbral(m, df, metrica, rejilla=[0.3, 0.5, 0.7]) == 0.5


def test_efecto_de_pesos_coincidencia_poblacional():
    """Contrato: con n grande la regla con pesos y la sin pesos con τ = w0/(w0 + w1)
    coinciden en más del 99 % de despliegue (con n = 20 000 la razón 100 da 0.989)."""
    d = ml.PROCESOS["fraude"](n=500_000, proporcion=0.05)
    t = ml.efecto_de_pesos(d, [1, 3, 12, 30, 100])
    assert (t["coincidencia"] > 0.99).all()


# === Lote de la clase 5 (1.6): clase_5.md §10.7 «Pide nuevo», contrato §5.10–§5.11 ===


def _llego_tarde(**cambios):
    return ml._llego_tarde(**cambios)


def test_pliegues_temporales_solo_validan_hacia_adelante():
    df = pd.DataFrame({"t": np.arange(60)[::-1].astype(float), "y": np.arange(60.0)})
    part = ml.pliegues(df, k=5, como="temporal")
    assert len(part) == 5
    t = df["t"].to_numpy()
    for ajuste, valida in part:
        assert t[ajuste].max() < t[valida].min()
    validas = np.concatenate([v for _, v in part])
    assert len(set(validas)) == len(validas) == 50  # el primer bloque nunca valida
    cv = ml.validacion_cruzada(df.assign(x=1.0), lambda d: ml.ajustar(d, columnas_x=["x"],
                                                                      tarea="regresion"),
                               particion="temporal")
    assert np.isnan(cv.perdidas_fuera).sum() == 10
    ml.dibujar_pliegues(60, 5, particion=part)


def test_pliegues_por_grupo_nunca_parten_un_grupo():
    d = ml.proceso(n=240, ruido=ml.efecto_grupo(24), con_realidad=False)
    df = d.ent
    part = ml.pliegues(df, k=5, como="grupo", semilla=3)
    for ajuste, valida in part:
        assert not set(df["grupo"].iloc[ajuste]) & set(df["grupo"].iloc[valida])
    assert sorted(np.concatenate([v for _, v in part])) == list(range(len(df)))
    with pytest.raises(ValueError, match="grupo"):
        ml.pliegues(df.drop(columns="grupo"), como="grupo")


def test_grupo_estratificado_balancea_positivos():
    rng = np.random.default_rng(0)
    grupo = np.repeat(np.arange(60), 5)
    y = (rng.random(300) < np.repeat(rng.choice([0.05, 0.6], 60), 5)).astype(int)
    df = pd.DataFrame({"grupo": grupo, "y": y})
    df.attrs["ml"] = {"columnas_x": [], "columnas_contexto": ["grupo"],
                      "tarea": "clasificacion", "K": 2, "clases": [0, 1]}
    est = ml.pliegues(df, k=5, como="grupo", estratificar=True, semilla=0)
    sin = ml.pliegues(df, k=5, como="grupo", semilla=0)
    for ajuste, valida in est:
        assert not set(grupo[ajuste]) & set(grupo[valida])
    rango = lambda part: np.ptp([y[v].mean() for _, v in part])  # noqa: E731
    assert rango(est) < rango(sin)
    assert rango(est) < 0.2


def test_estratificar_sin_grupo_lanza():
    df = pd.DataFrame({"y": [0, 1] * 20})
    for como in ("azar", "estratificado", "temporal"):
        with pytest.raises(ValueError, match='como="grupo"'):
            ml.pliegues(df, como=como, estratificar=True)


@pytest.mark.parametrize("familia", ["arbol", "bosque", "boosting"])
def test_ajustar_otro_familias_de_la_clase_5(familia):
    reg = ml.PROCESOS["entregas_curvas"](n=120)
    m = ml.ajustar_otro(reg, familia=familia)
    assert m.familia == familia and m.tarea == "regresion"
    assert ml.L(m, reg.val) < ml.benchmarks(reg, reg.val).loc["media", "cuadratica"]
    clf = _llego_tarde(n=400)
    m = ml.ajustar_otro(clf, familia=familia, profundidad=2)
    assert m.predecir_prob(clf.val).shape == (len(clf.val), 2)
    assert np.allclose(m.predecir_prob(clf.val).sum(axis=1), 1)
    assert ml.evaluar(m, clf.val, "logaritmica") < np.inf
    with pytest.raises(ValueError):
        ml.ajustar_otro(reg, familia=familia, profundidad=0)


def test_ajustar_otro_boosting_nombra_tasa_y_etapas():
    reg = ml.PROCESOS["entregas_curvas"](n=120)
    m = ml.ajustar_otro(reg, familia="boosting", etapas=7, tasa=0.3, profundidad=1)
    assert m.hiperparametros == {"etapas": 7, "tasa": 0.3, "profundidad": 1}
    assert m._est.n_estimators == 7 and m._est.learning_rate == 0.3
    with pytest.raises(ValueError, match="tasa"):
        ml.ajustar_otro(reg, familia="boosting", tasa=1.5)


def test_seleccionar_solo_mira_entrenamiento():
    d = ml.sembrar_fuga(_llego_tarde(n=200), "seleccion_previa", n_ruido=40, k=5)
    phi = ml.seleccionar(k=5).ajustar(d.ent)
    otra_val = d.val.copy()
    otra_val["y"] = 1 - otra_val["y"]
    otra_val[d.columnas_universo] = otra_val[d.columnas_universo].to_numpy()[::-1]
    phi2 = ml.seleccionar(k=5).ajustar(d.ent)
    assert phi.nombres == phi2.nombres
    # y la lista es la de mayor |corr| en ent
    r = ml._abs_corr_con_y(d.ent, d.columnas_universo)
    assert set(phi.nombres) == {d.columnas_universo[i] for i in np.argsort(-r)[:5]}
    assert ml.estandarizar(ml.seleccionar(k=5)).ajustar(d.ent).nombres == phi.nombres


def test_seleccionar_lee_el_universo():
    d = ml.caso(26)
    assert len(d.columnas_universo) == 503 and len(d.columnas_x) == 10
    assert set(d.columnas_universo) <= set(d.ent.columns)
    assert d.ent.attrs["ml"]["columnas_universo"] == d.columnas_universo
    assert ml.ajustar(d).Phi(d.ent).shape[1] == 11  # 10 columnas y la constante
    phi = ml.seleccionar(10).ajustar(d.ent)
    r = ml._abs_corr_con_y(d.ent, d.columnas_universo)
    assert set(phi.nombres) == {d.columnas_universo[i] for i in np.argsort(-r)[:10]}
    assert set(phi.nombres) != set(d.columnas_x)  # eligió entre las 503, no entre las 10
    with pytest.raises(ValueError, match="contexto|constante"):
        ml.seleccionar(1, columnas=["y"]).ajustar(d.ent)


def test_seleccion_previa_infla_y_la_limpia_recupera():
    d = ml.caso(26)
    logistica = lambda df: ml.ajustar(df, pesos="balanceado")  # noqa: E731
    limpia = ml.tuberia(ml.seleccionar(10), modelo={"familia": "logistica",
                                                    "pesos": "balanceado"})
    mutada = ml.tuberia(ml.seleccionar(10, columnas=d.columnas_x),
                        modelo={"familia": "logistica", "pesos": "balanceado"})
    cv = lambda c: ml.validacion_cruzada(d, c, particion="estratificado",  # noqa: E731
                                         criterio="mcc").media
    assert cv(logistica) > 0.3
    assert abs(cv(limpia)) < 0.1
    assert abs(ml.desempeno(limpia(ml._desarrollo(d)), d, "mcc")) < 0.1
    assert cv(mutada) > 0.3  # reseleccionar desde columnas_x ya reducidas no recupera


def test_tuberia_caso_26_recupera():
    d = ml.caso(26)
    limpia = ml.tuberia(ml.seleccionar(10), modelo={"familia": "logistica",
                                                    "pesos": "balanceado"})
    cv = ml.validacion_cruzada(d, limpia, particion="estratificado", criterio="mcc")
    assert abs(cv.media) < 0.1


def test_imputador_aprende_en_ent_y_agrega_indicadoras():
    d = _llego_tarde(n=300, faltantes={"distancia": (0.3, "azar")})
    imp = ml.imputar_simple(d.ent)
    assert imp.indicadoras == ["distancia"]
    assert imp.valores["distancia"] == pytest.approx(d.ent["distancia"].median())
    val = imp.transformar(d.val)
    assert not val["distancia"].isna().any()
    assert (val["distancia_falta"] == d.val["distancia"].isna().astype(float)).all()
    assert val.attrs["ml"]["columnas_x"] == ["distancia", "hora", "lluvia", "distancia_falta"]
    assert d.val.attrs["ml"]["columnas_x"] == ["distancia", "hora", "lluvia"]  # no muta
    assert repr(ml.imputador()) == "imputador()"
    with pytest.raises(ValueError, match="no está ajustado"):
        ml.imputador().transformar(d.val)
    with pytest.raises(ValueError, match="contexto|y"):
        ml.imputar_simple(d.ent, columnas=["y"])


def test_tuberia_acepta_imputador_sin_ajustar():
    d = _llego_tarde(n=300, faltantes={"distancia": (0.3, "azar")})
    vistos = []
    base = ml.tuberia(ml.imputador(), modelo={"familia": "logistica"})

    def construir(df):
        m = base(df)
        vistos.append((m._imputadores[0].valores["distancia"], df["distancia"].median()))
        return m

    ml.validacion_cruzada(d, construir, k=5)
    assert len(vistos) == 5
    for aprendido, del_pliegue in vistos:
        assert aprendido == pytest.approx(del_pliegue)
    assert len({round(a, 12) for a, _ in vistos}) > 1  # cada pliegue la suya


def test_tuberia_un_solo_intercepto():
    d = _llego_tarde(n=300, faltantes={"distancia": (0.3, "azar")})
    for phi in (ml.estandarizar(ml.seleccionar(k=2)),
                ml.combinar(ml.columnas("distancia"), ml.columnas("hora")),
                ml.estandarizar(ml.combinar(ml.columnas("distancia"), ml.dummies("lluvia")))):
        m = ml.tuberia(ml.imputador(), phi, modelo={"familia": "logistica"})(d.ent)
        assert list(m.Phi(d.val).columns).count("1") == 1
    m = ml.tuberia(ml.imputador(), modelo={"familia": "logistica"})(d.ent)
    assert list(m.Phi(d.val).columns) == ["1", "distancia", "hora", "lluvia", "distancia_falta"]


def test_tuberia_dos_phi_lanza():
    with pytest.raises(ValueError, match="a lo sumo una Φ"):
        ml.tuberia(ml.seleccionar(3), ml.estandarizar(ml.columnas("x")), modelo={})
    with pytest.raises(ValueError, match="antes de la Φ"):
        ml.tuberia(ml.seleccionar(3), ml.imputador(), modelo={})
    with pytest.raises(ValueError, match="paso"):
        ml.tuberia("estandarizar", modelo={})
    with pytest.raises(ValueError, match="Φ va como paso"):
        ml.tuberia(modelo={"phi": ml.polinomio(2)})
    with pytest.raises(ValueError, match="pesos"):
        ml.tuberia(modelo={"familia": "vecinos", "pesos": "balanceado"})


def test_tuberia_pesos_por_pliegue():
    d = _llego_tarde(n=500)
    dev = ml._desarrollo(d)
    y = dev["y"].to_numpy()
    orden = np.argsort(-y, kind="stable")  # positivos primero: los pliegues difieren
    trozos = np.array_split(orden, 4)
    part = [(np.sort(np.concatenate([t for j, t in enumerate(trozos) if j != m])),
             np.sort(trozos[m])) for m in range(4)]
    vistos = []
    base = ml.tuberia(modelo={"familia": "logistica", "pesos": "balanceado"})

    def construir(df):
        m = base(df)
        vistos.append((m.pesos, df["y"].to_numpy()))
        return m

    ml.validacion_cruzada(dev, construir, particion=lambda df: part)
    total = {c: len(y) / (2 * np.sum(y == c)) for c in (0, 1)}
    distintos = 0
    for pesos, y_m in vistos:
        for c in (0, 1):
            assert pesos[c] == pytest.approx(len(y_m) / (2 * np.sum(y_m == c)))
        distintos += any(not math.isclose(pesos[c], total[c]) for c in (0, 1))
    assert distintos == len(vistos)  # contarlos con todo el desarrollo daría otros


def test_tuberia_con_familias_de_ajustar_otro():
    d = _llego_tarde(n=300, faltantes={"distancia": (0.3, "azar")})
    for fam, extra in (("vecinos", {"n_vecinos": 7}), ("arbol", {"profundidad": 2})):
        m = ml.tuberia(ml.imputador(), ml.estandarizar(ml.columnas("distancia", "hora")),
                       modelo={"familia": fam, **extra})(d.ent)
        assert m.familia == fam and len(m.predecir(d.val)) == len(d.val)
        assert m.columnas_x == ["distancia", "hora", "lluvia"]
    with pytest.raises(ValueError, match="regresion|clasificacion"):
        ml.tuberia(modelo={"familia": "lineal"})(d.ent)


@pytest.mark.parametrize("tipo", ["posterior", "preprocesar_antes", "duplicados",
                                  "seleccion_previa"])
def test_sembrar_fuga_conserva_el_proceso(tipo):
    d = _llego_tarde(n=300, faltantes={"distancia": (0.2, "azar")})
    f = ml.sembrar_fuga(d, tipo, n_ruido=30, k=4)
    assert f.tarea == d.tarea and list(f.clases) == list(d.clases)
    for parte in (f.ent, f.val, f.prueba, f.despliegue):
        assert parte.attrs["ml"]["columnas_x"] == f.columnas_x
        assert set(f.columnas_x) <= set(parte.columns)
    assert d.ent.attrs["ml"]["columnas_x"] == ["distancia", "hora", "lluvia"]  # no muta
    otra = f.rehacer(5)
    assert otra.columnas_x == f.columnas_x or tipo == "seleccion_previa"
    if tipo == "posterior":
        assert f.columnas_x[-1] == "calificacion"
        assert f.despliegue["calificacion"].nunique() == 1
        assert f.ent.groupby("y")["calificacion"].mean().diff().iloc[-1] < -1.5
    if tipo == "duplicados":
        assert sum(map(len, (f.ent, f.val, f.prueba))) == 300 + 90
    if tipo == "preprocesar_antes":
        todo = pd.concat([f.ent, f.val, f.prueba])
        assert todo["hora"].mean() == pytest.approx(0, abs=1e-12)
        assert "distancia_falta" in f.columnas_x
    if tipo == "seleccion_previa":
        assert len(f.columnas_universo) == 33 and len(f.columnas_x) == 4
        assert len(f.despliegue) == 10_000
    with pytest.raises(ValueError, match="imputar_simple"):
        ml.sembrar_fuga(d, "imputar_en_prueba")


def test_medir_fugas_no_tiene_columna_R():
    d = _llego_tarde(n=300)
    tabla = ml.medir_fugas(d, lambda df: ml.ajustar(df), tipos=("posterior",), criterio="mcc")
    assert list(tabla.columns) == ["tipo", "intensidad", "estimado", "en_uso", "inflado"]
    assert "R" not in tabla.columns and tabla.attrs["criterio"] == "mcc"
    fila = tabla.iloc[0]
    assert fila["inflado"] == pytest.approx(fila["estimado"] - fila["en_uso"])
    assert fila["estimado"] > 0.8 and fila["inflado"] > 0.3
    ax = ml.dibujar_fugas(tabla)
    rotulos = [t.get_text() for t in ax.get_legend().get_texts()]
    assert "MCC de la CV" in rotulos and "MCC en el despliegue" in rotulos
    assert not any(r.startswith("R") for r in rotulos)


def test_medir_fugas_ninguna_no_infla():
    d = _llego_tarde(n=600)
    tabla = ml.medir_fugas(d, lambda df: ml.ajustar(df), tipos=("ninguna",), criterio="mcc")
    assert abs(tabla["inflado"].iloc[0]) < 2 * tabla.attrs["ee"][0]
    perdida = ml.medir_fugas(d, lambda df: ml.ajustar(df), tipos=("ninguna",))
    assert perdida.attrs["criterio"] == "logaritmica"
    assert perdida["inflado"].iloc[0] == pytest.approx(
        perdida["en_uso"].iloc[0] - perdida["estimado"].iloc[0])


def test_importancia_de_ruido_cerca_de_cero():
    d = ml.sembrar_fuga(_llego_tarde(n=800), "seleccion_previa", n_ruido=3, k=6)
    m = ml.ajustar(d)
    imp = ml.importancia(m, d.val, "logaritmica", repeticiones=10)
    assert list(imp.index) == d.columnas_x and imp.name == "importancia"
    ruido = imp[[c for c in imp.index if c.startswith("ruido_")]]
    assert ruido.abs().max() < 0.02
    assert imp["distancia"] > 0.05
    ml.dibujar_importancia(imp)


def _dos_tablas(desplaza=0.0, n_a=600, n_b=150, semilla=0, corr=None):
    rng = np.random.default_rng(semilla)
    a = pd.DataFrame(rng.standard_normal((n_a, 2)), columns=["x1", "x2"])
    z = rng.standard_normal((n_b, 2))
    if corr is not None:
        z[:, 1] = corr * z[:, 0] + math.sqrt(1 - corr ** 2) * z[:, 1]
    b = pd.DataFrame(z, columns=["x1", "x2"])
    b["x1"] += desplaza
    return a, b


def test_adversarial_senal_nada_y_deriva():
    a, b = _dos_tablas()
    nada = ml.validacion_adversarial(a, b)
    assert nada.senal == "sin señal"
    assert abs(nada.log_loss - nada.log_loss_benchmark) < 0.02
    assert np.mean(nada.diferencias_por_pliegue) == pytest.approx(
        nada.log_loss - nada.log_loss_benchmark)
    a, b = _dos_tablas(desplaza=1.0)
    deriva = ml.validacion_adversarial(a, b)
    assert deriva.senal == "señal" and deriva.log_loss < deriva.log_loss_benchmark - 0.05
    assert len(deriva.diferencias_por_pliegue) == 5
    assert deriva.importancia.idxmax() == "x1"
    ml.dibujar_adversarial(deriva)


def test_adversarial_mcc_con_origen_desbalanceado():
    a, b = _dos_tablas(desplaza=0.4)
    r = ml.validacion_adversarial(a, b)
    assert r.o_bar == pytest.approx(0.2) and r.senal == "señal"
    assert r.mcc > 0.15
    con_05 = ml.mcc(r.origen, (r.prob >= 0.5).astype(int), clases=[0, 1])
    assert abs(con_05) < 0.05  # mutación: cortar en 0.5 nunca dice «origen 1»


def test_adversarial_sin_doble_correccion():
    a, b = _dos_tablas(desplaza=0.8)
    r = ml.validacion_adversarial(a, b)
    X = np.r_[a.to_numpy(), b.to_numpy()]
    o = r.origen

    def replica(pesos):
        pred = np.zeros(len(o), int)
        for ajuste, valida in r.pliegues:
            est = ml._clasificador_adversarial("bosque", 0, pesos).fit(X[ajuste], o[ajuste])
            pred[valida] = est.predict_proba(X[valida])[:, 1] >= o[ajuste].mean()
        return ml.mcc(o, pred, clases=[0, 1])

    assert replica(None) == pytest.approx(r.mcc)  # la réplica es la función
    assert replica("balanced") != pytest.approx(r.mcc, abs=1e-3)  # doble corrección


def test_adversarial_firma_sin_pesos():
    firma = inspect.signature(ml.validacion_adversarial)
    assert list(firma.parameters) == ["df_a", "df_b", "columnas", "k", "semilla", "particion",
                                      "familia"]
    assert "Sin pesos" in ml.validacion_adversarial.__doc__ or \
        "SIN pesos" in ml.validacion_adversarial.__doc__


def test_adversarial_ve_correlacion_con_bosque():
    a, b = _dos_tablas(corr=0.95, n_b=600)
    bosque = ml.validacion_adversarial(a, b)
    logistica = ml.validacion_adversarial(a, b, familia="logistica")
    assert bosque.senal == "señal" and bosque.log_loss < bosque.log_loss_benchmark - 0.03
    assert abs(logistica.log_loss - logistica.log_loss_benchmark) < 0.01
    ks = ml.ks_por_variable(a, b)
    assert (ks["estadistico"] < 0.1).all()  # las marginales son las mismas
    ml.dibujar_ks(ks)


def test_adversarial_por_grupos_no_detecta_clientes():
    rng = np.random.default_rng(0)
    filas = []
    for origen, clientes in ((0, range(0, 30)), (1, range(30, 60))):
        for cliente in clientes:
            centro = rng.normal(0, 1, 2)
            for _ in range(10):
                filas.append((origen, cliente, *(centro + rng.normal(0, 0.05, 2))))
    t = pd.DataFrame(filas, columns=["o", "grupo", "x1", "x2"])
    a, b = t[t["o"] == 0], t[t["o"] == 1]
    azar = ml.validacion_adversarial(a, b, columnas=["x1", "x2"])
    grupos = ml.validacion_adversarial(a, b, columnas=["x1", "x2"], particion="grupo")
    assert azar.senal == "señal"
    assert grupos.senal == "sin señal"
    for ajuste, valida in grupos.pliegues:
        assert not set(t["grupo"].to_numpy()[ajuste]) & set(t["grupo"].to_numpy()[valida])
    with pytest.raises(ValueError, match="nunca usa"):
        ml.validacion_adversarial(a, b, columnas=["x1", "grupo"])


def test_ks_a_mano_es_un_tercio():
    a = pd.DataFrame({"x": [0.0, 1.0, 2.0]})
    b = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    assert ml.ks_por_variable(a, b)["estadistico"].iloc[0] == pytest.approx(1 / 3)


def test_autocorrelacion_denominador_comun():
    r = ml.autocorrelacion([1, -1, 1, -1, 1, -1], rezagos=1)
    assert r[0] == pytest.approx(-5 / 6)
    assert "denominador común" in ml.autocorrelacion.__doc__
    e = np.random.default_rng(0).standard_normal(400)
    assert np.mean(np.abs(ml.autocorrelacion(e, 10)) < 2 / 20) >= 0.8
    with pytest.raises(ValueError):
        ml.autocorrelacion([1.0, 2.0], rezagos=2)


def test_dibujar_residual_tiempo_con_memoria():
    d = ml.proceso(n=200, ruido=ml.ar1(0.9), separar="tiempo", con_realidad=False)
    m = ml.ajustar(d)
    ax = ml.dibujar_residual_tiempo(m, d.ent)
    assert any(l.get_gid() == "residual-tiempo" for l in ax.lines)
    with pytest.raises(ValueError, match="t"):
        ml.dibujar_residual_tiempo(m, d.ent.drop(columns="t"))


def test_sellada_cuenta_aperturas():
    df = pd.DataFrame({"x": [1.0, 2.0], "y": [0, 1]})
    s = ml.sellar(df)
    assert s.aperturas == 0 and len(s) == 2 and "Sellada" in repr(s)
    assert not any(isinstance(v, pd.DataFrame) for k, v in vars(s).items()
                   if not k.startswith("_Sellada"))
    abierta = s.abrir()
    abierta.loc[0, "x"] = 99.0
    assert s.abrir()["x"].iloc[0] == 1.0
    assert s.aperturas == 2


def test_dibujar_sigmoides_una_curva_por_q():
    f = np.sin
    ajustes = {1: lambda x: 0.5 * x, 3: lambda x: x - x ** 3 / 6, 10: np.sin}
    ax = ml.dibujar_sigmoides(f, ajustes, datos=(np.linspace(0, 3, 30), np.sin(np.linspace(0, 3, 30))))
    gids = [l.get_gid() for l in ax.lines]
    assert gids == ["curva-verdadera", "ajuste-1", "ajuste-3", "ajuste-10"]
    rotulos = [t.get_text() for t in ax.get_legend().get_texts()]
    assert {"1 unidad", "3 unidades", "10 unidades"} <= set(rotulos)
    assert not any("R" == r or "q" in r.split() for r in rotulos)
    with pytest.raises(ValueError):
        ml.dibujar_sigmoides(f, {"uno": f})


def test_casos_de_la_clase_5_se_construyen_por_nombre():
    for numero, nombre in ((19, "variable_posterior"), (20, "preprocesar_antes"),
                           (21, "duplicados"), (26, "seleccion_previa"),
                           (27, "categoria_nueva"), (28, "cambio_de_concepto")):
        cb = ml.CASOS_BORDE[numero]
        assert cb.numero == numero and cb.nombre == nombre and cb.clase == 5
    d = ml.caso("categoria_nueva")
    assert "sur" not in set(d.ent["zona"]) | set(d.val["zona"])
    assert "sur" in set(d.prueba["zona"]) and "sur" in set(d.despliegue["zona"])
    phi = ml.combinar(ml.columnas("distancia"), ml.dummies("zona"))
    with pytest.raises(ValueError, match="sur"):
        ml.ajustar(d, phi=phi).predecir(d.prueba)
    efectos = ml.ajustar(d, phi=ml.combinar(ml.columnas("distancia"),
                                            ml.dummies("zona", codificacion="efectos")))
    with pytest.warns(UserWarning, match="sur"):
        pred = efectos.predecir(d.prueba)
    e = (d.prueba["y"] - pred) ** 2
    sur = d.prueba["zona"].to_numpy() == "sur"
    assert e[sur].mean() > 5 * e[~sur].mean()
    c28 = ml.caso(28)
    m = ml.ajustar(c28)
    assert ml.riesgo(m, c28) > 5 * ml.L(m, c28.prueba)


def test_caso_19_y_21_rompen_la_cv():
    vecinos = lambda df: ml.tuberia(  # noqa: E731
        ml.estandarizar(ml.columnas(*df.attrs["ml"]["columnas_x"])),
        modelo={"familia": "vecinos"})(df)
    d19 = ml.caso(19)
    assert ml.validacion_cruzada(d19, vecinos, criterio="mcc").media >= 0.9
    limpio = ml._llego_tarde()
    assert (ml.desempeno(vecinos(ml._desarrollo(d19)), d19, "mcc")
            <= ml.desempeno(vecinos(ml._desarrollo(limpio)), limpio, "mcc"))
    d21 = ml.caso(21)
    uno = lambda df: ml.ajustar_otro(df, familia="vecinos", n_vecinos=1)  # noqa: E731
    log = lambda df: ml.ajustar(df, pesos="balanceado")  # noqa: E731
    infla = {}
    for nombre, c in (("vecinos", uno), ("logistica", log)):
        cv = ml.validacion_cruzada(d21, c, criterio="mcc").media
        infla[nombre] = cv - ml.desempeno(c(ml._desarrollo(d21)), d21, "mcc")
    assert infla["vecinos"] >= 0.1
    assert abs(infla["logistica"]) < 0.5 * infla["vecinos"]


def test_taller_y_galeria_de_la_clase_5_corren(monkeypatch):
    monkeypatch.setattr(ml, "_widgets", lambda: None)
    monkeypatch.setattr(ml, "_mostrar", lambda: None)
    salida = io.StringIO()
    with redirect_stdout(salida), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ml.taller(ml.proceso(n=200, ruido=ml.ar1(0.9), despliegue="futuro"), clase=5)
        ml.taller(_llego_tarde(n=300), clase=5)
        ml.galeria(5, casos=[28])
    texto = salida.getvalue()
    for marca in ("(1) Validación adversarial", "(2) KS_j", "(3) Residuales contra t",
                  "(4) CV", "(5) Alarma de fuga", "MCC en el despliegue", "largo plazo"):
        assert marca in texto
    assert 5 in ml.ANALISIS_TALLER
