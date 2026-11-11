"""Las cifras de la clase 1 de aprendizaje profundo salen de redes.py.

1. Cada cifra con su assert: lo que calcula redes.py contra el valor escrito a
   mano aquí (cambiar el ejemplo o una regla sin tocar la prosa rompe la suite).
2. La retropropagación coincide con las diferencias finitas (error relativo
   < 1e-6) en el ejemplo 2–3–2–1, en una red más ancha con varias
   observaciones, con sigmoide e identidad, y con μ > 0.
3. Propiedades que la prosa afirma: un paso con η pequeña baja la pérdida; μ
   cambia el gradiente de cada W exactamente en 2μW y no toca los sesgos; el
   entrenamiento es determinista y cuenta la historia de la página 5.

Las cifras aún no se buscan en las páginas: las escriben los escritores
después de este archivo (la búsqueda en la prosa la agrega el orquestador).
"""
import numpy as np
import pytest

import redes as r

TOL_GRADIENTE = 1e-6

# Cifras del ejemplo 2–3–2–1 (x = (1, 2), y = 1), escritas a mano.
ESPERADAS = {
    "x": [1.0, 2.0],
    "y": [1.0],
    "z1": [0.2, -0.2, 0.6],
    "a1": [0.2, 0.0, 0.6],
    "z2": [0.48, 0.18],
    "a2": [0.48, 0.18],
    "z3": [0.546],
    "a3": [0.546],
    "y_gorro": 0.546,
    "perdida": 0.206,
    "delta3": [-0.908],
    "delta2": [-0.636, 0.454],
    "delta1": [-0.163, 0.0, -0.363],
    "grad_W3": [[-0.436, -0.163]],
    "grad_b3": [-0.908],
    "grad_W2": [[-0.127, 0.0, -0.381],
                [0.091, 0.0, 0.272]],
    "grad_b2": [-0.636, 0.454],
    "grad_W1": [[-0.163, -0.327],
                [0.0, 0.0],
                [-0.363, -0.726]],
    "grad_b1": [-0.163, 0.0, -0.363],
    "omega": 2.24,
    "omega_por_capa": [0.59, 0.91, 0.74],
    "eta": 0.1,
    "y_gorro_tras_paso": 0.879,
    "perdida_tras_paso": 0.015,
    "mu": 0.01,
    "perdida_tras_paso_mu": 0.015,
    "omega_tras_paso": 2.401,
    "omega_tras_paso_mu": 2.392,
    # Entrenamiento de la página 5 (2–32–32–1, 1500 épocas, lote 20).
    "rmse_entrenamiento_final_sin_mu": 0.196,
    "rmse_validacion_final_sin_mu": 0.418,
    "rmse_validacion_min_sin_mu": 0.328,
    "epoca_validacion_min_sin_mu": 285,
    "rmse_entrenamiento_final_con_mu": 0.247,
    "rmse_validacion_final_con_mu": 0.316,
    "rmse_validacion_min_con_mu": 0.31,
    "epoca_validacion_min_con_mu": 894,
    "mu_entrenamiento": 0.003,
    "epocas": 1500,
    # RMSE de la observación del ejemplo (= |ŷ − y|) y parámetros d_l (d_{l-1} + 1) por capa
    "rmse": 0.454,
    "Wt_delta2": [-0.163, 0.463, -0.363],
    "w3_11_tras_paso": 0.744,
    "w3_11_tras_paso_mu": 0.742,
    "b3_tras_paso": 0.391,
    "error_comprobacion_menor_que_1e_10": True,
    "n_parametros": 20,
    "n_parametros_784_16_16_10": 13002,
    "n_parametros_5_8_8_3": 147,
    "n_parametros_5_3_colapsada": 18,
}


@pytest.fixture(scope="module")
def cifras():
    return r.cifras()


def test_cifras_no_tiene_claves_de_mas_ni_de_menos(cifras):
    assert set(cifras) == set(ESPERADAS)


@pytest.mark.parametrize("clave", sorted(ESPERADAS))
def test_cada_cifra(cifras, clave):
    assert cifras[clave] == ESPERADAS[clave]


# ------------------------------------------------------- el ejemplo 2–3–2–1 ---

def test_ejemplo_tiene_la_forma_2_3_2_1():
    red, x, y = r.ejemplo()
    anchos = [len(x)] + [len(b) for b in red["b"][1:]]
    assert anchos == [2, 3, 2, 1]
    for l in range(1, 4):
        assert red["W"][l].shape == (anchos[l], anchos[l - 1])
    assert red["g"] == [None, "relu", "relu", "identidad"]
    assert y.shape == (1,)


def test_ejemplo_tiene_una_neurona_inactiva_en_la_capa_1():
    """g' = 0 en la neurona 2 de la capa 1 y g' = 1 en todas las demás."""
    red, x, _ = r.ejemplo()
    z, _, _ = r.adelante(red, x)
    assert r.relu_prima(z[1]).tolist() == [1.0, 0.0, 1.0]
    assert r.relu_prima(z[2]).tolist() == [1.0, 1.0]
    assert z[1][1] < 0


def test_pesos_del_ejemplo_son_decimales_cortos():
    red, x, y = r.ejemplo()
    for v in [*red["W"][1:], *red["b"][1:], x, y]:
        assert np.allclose(v, np.round(v, 1))


def test_derivada_por_peso_es_error_del_destino_por_activacion_del_origen():
    red, x, y = r.ejemplo()
    _, a, _ = r.adelante(red, x)
    delta, grad_W, _ = r.atras(red, x, y)
    for l in range(1, 4):
        for i in range(grad_W[l].shape[0]):
            for j in range(grad_W[l].shape[1]):
                assert grad_W[l][i, j] == pytest.approx(
                    delta[l][i] * a[l - 1][j])


def test_relu_prima_en_cero_vale_cero():
    assert r.relu_prima(np.array([0.0]))[0] == 0.0


# ------------------------------------------- retropropagación contra numérico ---

def test_backprop_coincide_con_diferencias_finitas_en_el_ejemplo():
    red, x, y = r.ejemplo()
    assert r.comprobar_gradiente(red, x, y) < TOL_GRADIENTE


def test_gradiente_de_lote_con_una_observacion_es_atras():
    red, x, y = r.ejemplo()
    _, grad_W, grad_b = r.atras(red, x, y)
    lote_W, lote_b = r.gradiente(red, x, y)
    for l in range(1, 4):
        assert np.allclose(lote_W[l], grad_W[l])
        assert np.allclose(lote_b[l], grad_b[l])


def _red_aleatoria(anchos, activaciones, semilla):
    rng = np.random.default_rng(semilla)
    red = r.red_inicial(anchos, activaciones, semilla)
    red["b"] = [None] + [0.1 * rng.standard_normal(d) for d in anchos[1:]]
    X = rng.standard_normal((anchos[0], 7))
    Y = rng.standard_normal((anchos[-1], 7))
    return red, X, Y


@pytest.mark.parametrize("activaciones", [
    ("relu", "relu", "identidad"),
    ("sigmoide", "sigmoide", "identidad"),
    ("sigmoide", "relu", "sigmoide"),
    ("identidad", "identidad", "identidad"),
])
@pytest.mark.parametrize("mu", [0.0, 0.05])
def test_backprop_coincide_con_diferencias_finitas_en_red_ancha(activaciones,
                                                                 mu):
    red, X, Y = _red_aleatoria((4, 6, 5, 2), activaciones, semilla=11)
    assert r.comprobar_gradiente(red, X, Y, mu) < TOL_GRADIENTE


def test_comprobar_gradiente_detecta_un_gradiente_equivocado(monkeypatch):
    """Si la retropropagación olvida el factor 2 de ℓ, la comprobación lo ve."""
    red, x, y = r.ejemplo()
    original = r.gradiente

    def mitad(red, X, Y, mu=0.0):
        gW, gb = original(red, X, Y, mu)
        return ([None] + [G / 2 for G in gW[1:]],
                [None] + [g / 2 for g in gb[1:]])

    monkeypatch.setattr(r, "gradiente", mitad)
    assert r.comprobar_gradiente(red, x, y) > 0.1


# ------------------------------------------------------- paso y lagrangeano ---

def test_un_paso_con_eta_pequena_baja_la_perdida_del_ejemplo():
    red, x, y = r.ejemplo()
    antes = r.perdida(r.adelante(red, x)[2], y)
    for eta in (0.001, 0.01, r.ETA_EJEMPLO):
        nueva = r.paso(red, x, y, eta)
        assert r.perdida(r.adelante(nueva, x)[2], y) < antes


def test_un_paso_con_eta_pequena_baja_la_perdida_de_un_lote():
    red, X, Y = _red_aleatoria((4, 6, 5, 2), ("relu", "relu", "identidad"),
                               semilla=11)
    for mu in (0.0, 0.05):
        antes = r.lagrangeano(red, X, Y, mu)
        assert r.lagrangeano(r.paso(red, X, Y, 1e-3, mu), X, Y, mu) < antes


def test_paso_no_modifica_la_red_que_recibe():
    red, x, y = r.ejemplo()
    W1 = red["W"][1].copy()
    r.paso(red, x, y, r.ETA_EJEMPLO, r.MU_EJEMPLO)
    assert np.array_equal(red["W"][1], W1)


def test_mu_cambia_el_gradiente_de_cada_W_justo_en_2_mu_W():
    red, X, Y = _red_aleatoria((4, 6, 5, 2), ("relu", "relu", "identidad"),
                               semilla=11)
    mu = 0.05
    gW0, gb0 = r.gradiente(red, X, Y, 0.0)
    gWmu, gbmu = r.gradiente(red, X, Y, mu)
    for l in range(1, r.capas(red) + 1):
        assert np.allclose(gWmu[l] - gW0[l], 2 * mu * red["W"][l],
                           rtol=0, atol=1e-12)
        assert np.array_equal(gbmu[l], gb0[l])        # sesgos sin penalizar


def test_omega_suma_los_cuadrados_de_los_pesos_y_no_los_sesgos():
    red, _, _ = r.ejemplo()
    a_mano = sum(float((W ** 2).sum()) for W in red["W"][1:])
    assert r.omega(red) == pytest.approx(a_mano)
    red["b"][1] = red["b"][1] + 100
    assert r.omega(red) == pytest.approx(a_mano)


def test_d_del_lagrangeano_solo_desplaza_una_constante():
    red, x, y = r.ejemplo()
    mu = 0.3
    assert (r.lagrangeano(red, x, y, mu, d=0.0)
            - r.lagrangeano(red, x, y, mu, d=1.0)) == pytest.approx(mu)


def test_perdida_promedio_de_una_observacion_es_su_perdida():
    red, x, y = r.ejemplo()
    assert r.perdida_promedio(red, x, y) == pytest.approx(
        r.perdida(r.adelante(red, x)[2], y))
    assert r.rmse(red, x, y) == pytest.approx(
        np.sqrt(r.perdida_promedio(red, x, y)))


# ------------------------------------------------------------ entrenamiento ---

def test_datos_ejemplo_tienen_80_y_200_observaciones_en_columnas():
    X, Y, X_val, Y_val = r.datos_ejemplo()
    assert X.shape == (2, 80) and Y.shape == (1, 80)
    assert X_val.shape == (2, 200) and Y_val.shape == (1, 200)


def test_entrenar_ejemplo_es_determinista():
    h1 = r.entrenar_ejemplo(r.MU_ENTRENAMIENTO, epocas=20)
    h2 = r.entrenar_ejemplo(r.MU_ENTRENAMIENTO, epocas=20)
    assert h1 == h2
    assert len(h1["rmse_entrenamiento"]) == len(h1["rmse_validacion"]) == 21


def test_misma_red_inicial_con_y_sin_mu():
    sin_mu, con_mu = r._historias()
    assert sin_mu["rmse_validacion"][0] == con_mu["rmse_validacion"][0]
    assert len(sin_mu["rmse_validacion"]) == r.EPOCAS + 1


def test_la_historia_sin_mu_sobreajusta_y_con_mu_no():
    """Lo que la página 5 cuenta: sin μ el RMSE de entrenamiento sigue bajando
    mientras el de validación baja y luego sube; con μ la validación queda
    mejor al final y casi plana tras su mínimo."""
    sin_mu, con_mu = r._historias()
    v0 = np.array(sin_mu["rmse_validacion"])
    v1 = np.array(con_mu["rmse_validacion"])
    t0 = np.array(sin_mu["rmse_entrenamiento"])
    t1 = np.array(con_mu["rmse_entrenamiento"])
    # sin μ: mínimo de validación temprano y subida clara después
    assert v0.argmin() < r.EPOCAS / 4
    assert v0[-1] - v0.min() > 0.05
    # sin μ ajusta mejor el entrenamiento y peor la validación
    assert t0[-1] < t1[-1]
    assert v1[-1] < v0[-1] - 0.05
    # con μ: la validación al final no se aleja de su mínimo
    assert v1[-1] - v1.min() < 0.01
    # sin μ el hueco entre validación y entrenamiento crece mucho más
    assert (v0[-1] - t0[-1]) > 2 * (v1[-1] - t1[-1])
