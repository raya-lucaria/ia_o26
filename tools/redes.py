"""Cálculos de la unidad 10 (aprendizaje profundo), clase 1: redes neuronales.

Única fuente de los números que citan las páginas de
course/10_deep_learning/1_redes_neuronales/, de las figuras de
gen_deep_learning.py y del notebook 01_red_desde_cero.ipynb. Nada se copia a
mano: test_redes.py fija cada cifra con su valor escrito a mano.

Notación (plan de la unidad, la misma de las páginas)
-----------------------------------------------------
Una red es un dict con tres listas indexadas por la capa l = 1..L; la posición
0 vale None porque la capa 0 es la entrada y no tiene parámetros:

- red["W"][l]  = W^(l), matriz d_l × d_{l-1} (filas = destino i, columnas =
  origen j): red["W"][l][i-1, j-1] es el peso w^(l)_ij.
- red["b"][l]  = b^(l), vector de d_l sesgos.
- red["g"][l]  = nombre de la activación g^(l): "relu", "sigmoide" o
  "identidad" (ACTIVACIONES).

Una observación es x (vector de d_0) y y (vector de d_L). Las funciones de lote
reciben X (d_0 × m) y Y (d_L × m): una COLUMNA por observación k.

Qué calcula cada función (símbolo de la página entre paréntesis)
-----------------------------------------------------------------
- ejemplo()            la red 2–3–2–1 del hilo y su observación (x, y).
- adelante(red, x)     pase hacia adelante: z^(l) = W^(l) a^(l-1) + b^(l),
                       a^(l) = g^(l)(z^(l)), a^(0) = x; devuelve (z, a, ŷ).
- perdida(y_gorro, y)  ℓ(ŷ, y) = Σ (ŷ − y)², sin ½.
- atras(red, x, y)     retropropagación de UNA observación: δ^(l) = ∇_{z^(l)} ℓ
                       y los gradientes ∇_{W^(l)} ℓ = δ^(l) a^(l-1)ᵀ,
                       ∇_{b^(l)} ℓ = δ^(l); devuelve (delta, grad_W, grad_b).
- perdida_promedio(red, X, Y)  L(θ) = (1/n) Σ_k ℓ(f_θ(x_k), y_k) = MSE.
- rmse(red, X, Y)      RMSE = √MSE.
- omega(red)           Ω(θ) = Σ_l ‖W^(l)‖_F² (ridge; sesgos sin penalizar).
- lagrangeano(red, X, Y, mu, d)  𝓛(θ, μ) = L(θ) + μ (Ω(θ) − d).
- gradiente(red, X, Y, mu)       ∇_θ 𝓛 de un lote: promedio de δ a^(l-1)ᵀ
                       sobre las columnas, más 2 μ W^(l) en cada W.
- gradiente_numerico(red, X, Y, mu, h)  lo mismo por diferencias finitas
                       centradas: (𝓛(θ + h e) − 𝓛(θ − h e)) / (2h).
- comprobar_gradiente(red, X, Y, mu, h) error relativo máximo entre los dos,
                       ‖a − n‖ / (‖a‖ + ‖n‖) por bloque W^(l), b^(l).
- paso(red, X, Y, eta, mu)  un paso de descenso: θ ← θ − η ∇_θ 𝓛.
- red_inicial(anchos, activaciones, semilla)  pesos He (normal · √(2/d_{l-1})),
                       sesgos en cero.
- datos_ejemplo()      los datos sintéticos del entrenamiento de la página 5.
- entrenar(...)        descenso por minibatch; historia de RMSE por época.
- entrenar_ejemplo(mu) el entrenamiento de la página 5, sin (μ = 0) o con μ.
- cifras()             diccionario con TODAS las cifras citadas, a 3 decimales.

Convención de ReLU: g'(0) = 0 (la neurona en z = 0 cuenta como inactiva).
Todo lo aleatorio usa np.random.default_rng con las semillas de SEMILLAS
(numpy fijado en tools/requirements-regresion.txt).
"""
import copy
from functools import lru_cache

import numpy as np


# ------------------------------------------------------------ activaciones ---

def relu(z):
    return np.maximum(z, 0.0)


def relu_prima(z):
    return (z > 0).astype(float)


def sigmoide(z):
    return 1.0 / (1.0 + np.exp(-z))


def sigmoide_prima(z):
    s = sigmoide(z)
    return s * (1.0 - s)


def identidad(z):
    return z


def identidad_prima(z):
    return np.ones_like(z)


ACTIVACIONES = {
    "relu": (relu, relu_prima),
    "sigmoide": (sigmoide, sigmoide_prima),
    "identidad": (identidad, identidad_prima),
}


# ----------------------------------------------------------------- ejemplo ---

def ejemplo():
    """La red 2–3–2–1 del hilo: ocultas ReLU, salida identidad, y (x, y).

    Elegida para que la capa 1 tenga una neurona inactiva (z^(1)_2 < 0,
    g' = 0) y las otras dos activas, y la capa 2 ambas activas (g' = 1).
    """
    red = {
        "W": [None,
              np.array([[0.5, -0.2],
                        [-0.4, 0.1],
                        [0.3, 0.2]]),            # W^(1): 3 × 2
              np.array([[0.4, -0.3, 0.5],
                        [0.2, 0.6, -0.1]]),      # W^(2): 2 × 3
              np.array([[0.7, -0.5]])],          # W^(3): 1 × 2
        "b": [None,
              np.array([0.1, 0.0, -0.1]),        # b^(1)
              np.array([0.1, 0.2]),              # b^(2)
              np.array([0.3])],                  # b^(3)
        "g": [None, "relu", "relu", "identidad"],
    }
    x = np.array([1.0, 2.0])
    y = np.array([1.0])
    return red, x, y


ETA_EJEMPLO = 0.1      # η del paso de la página 5
MU_EJEMPLO = 0.01      # μ del paso con decaimiento de pesos


def capas(red):
    """L: el número de capas con parámetros."""
    return len(red["W"]) - 1


# -------------------------------------------------------------- adelante ---

def adelante(red, x):
    """Pase hacia adelante. x es un vector, o una matriz d_0 × m (columnas =
    observaciones). Devuelve las listas z (z[0] = None) y a (a[0] = x) y ŷ."""
    z, a = [None], [x]
    for l in range(1, capas(red) + 1):
        b = red["b"][l] if x.ndim == 1 else red["b"][l][:, None]
        g, _ = ACTIVACIONES[red["g"][l]]
        z.append(red["W"][l] @ a[l - 1] + b)
        a.append(g(z[l]))
    return z, a, a[-1]


def perdida(y_gorro, y):
    """ℓ(ŷ, y) = Σ (ŷ − y)² de UNA observación."""
    return float(np.sum((y_gorro - y) ** 2))


# ----------------------------------------------------------------- atrás ---

def atras(red, x, y):
    """Retropropagación de una observación (x, y).

    δ^(L) = 2(ŷ − y) ⊙ g^(L)'(z^(L));
    δ^(l) = (W^(l+1)ᵀ δ^(l+1)) ⊙ g^(l)'(z^(l));
    ∇_{W^(l)} ℓ = δ^(l) a^(l-1)ᵀ;  ∇_{b^(l)} ℓ = δ^(l).
    """
    z, a, y_gorro = adelante(red, x)
    L = capas(red)
    delta = [None] * (L + 1)
    grad_W, grad_b = [None] * (L + 1), [None] * (L + 1)
    for l in range(L, 0, -1):
        _, g_prima = ACTIVACIONES[red["g"][l]]
        if l == L:
            arriba = 2 * (y_gorro - y)                 # ∇_{a^(L)} ℓ
        else:
            arriba = red["W"][l + 1].T @ delta[l + 1]
        delta[l] = arriba * g_prima(z[l])
        grad_W[l] = np.outer(delta[l], a[l - 1])
        grad_b[l] = delta[l].copy()
    return delta, grad_W, grad_b


# ------------------------------------------------- pérdida de un conjunto ---

def _columnas(v):
    """Un vector suelto es una sola observación: una columna."""
    return v[:, None] if v.ndim == 1 else v


def perdida_promedio(red, X, Y):
    """L(θ) = (1/n) Σ_k ℓ(f_θ(x_k), y_k); para regresión es el MSE."""
    X, Y = _columnas(X), _columnas(Y)
    _, _, Y_gorro = adelante(red, X)
    return float(np.mean(np.sum((Y_gorro - Y) ** 2, axis=0)))


def rmse(red, X, Y):
    """RMSE = √MSE."""
    return float(np.sqrt(perdida_promedio(red, X, Y)))


def omega(red):
    """Ω(θ) = Σ_l ‖W^(l)‖_F²: suma de los cuadrados de todos los pesos."""
    return float(sum(np.sum(W ** 2) for W in red["W"][1:]))


def lagrangeano(red, X, Y, mu=0.0, d=0.0):
    """𝓛(θ, μ) = L(θ) + μ (Ω(θ) − d)."""
    return perdida_promedio(red, X, Y) + mu * (omega(red) - d)


# -------------------------------------------------------------- gradiente ---

def gradiente(red, X, Y, mu=0.0):
    """∇_θ 𝓛 de un lote (columnas = observaciones): los gradientes de ℓ se
    promedian sobre el lote y a cada W^(l) se le suma 2 μ W^(l)."""
    X, Y = _columnas(X), _columnas(Y)
    z, a, Y_gorro = adelante(red, X)
    L, m = capas(red), X.shape[1]
    grad_W, grad_b = [None] * (L + 1), [None] * (L + 1)
    for l in range(L, 0, -1):
        _, g_prima = ACTIVACIONES[red["g"][l]]
        if l == L:
            arriba = 2 * (Y_gorro - Y)
        else:
            arriba = red["W"][l + 1].T @ delta
        delta = arriba * g_prima(z[l])                   # d_l × m
        grad_W[l] = delta @ a[l - 1].T / m + 2 * mu * red["W"][l]
        grad_b[l] = delta.mean(axis=1)
    return grad_W, grad_b


def gradiente_numerico(red, X, Y, mu=0.0, h=1e-6):
    """∇_θ 𝓛 por diferencias finitas centradas, una entrada a la vez."""
    grad = {"W": [None], "b": [None]}
    for nombre in ("W", "b"):
        for l in range(1, capas(red) + 1):
            G = np.zeros_like(red[nombre][l])
            for idx in np.ndindex(G.shape):
                mas, menos = copy.deepcopy(red), copy.deepcopy(red)
                mas[nombre][l][idx] += h
                menos[nombre][l][idx] -= h
                G[idx] = (lagrangeano(mas, X, Y, mu)
                          - lagrangeano(menos, X, Y, mu)) / (2 * h)
            grad[nombre].append(G)
    return grad["W"], grad["b"]


def comprobar_gradiente(red, X, Y, mu=0.0, h=1e-6):
    """Error relativo máximo, por bloque W^(l) y b^(l), entre la
    retropropagación y las diferencias finitas: ‖a − n‖ / (‖a‖ + ‖n‖)."""
    analitico = gradiente(red, X, Y, mu)
    numerico = gradiente_numerico(red, X, Y, mu, h)
    peor = 0.0
    for A_bloques, N_bloques in zip(analitico, numerico):
        for A, N in zip(A_bloques[1:], N_bloques[1:]):
            escala = np.linalg.norm(A) + np.linalg.norm(N)
            if escala > 0:
                peor = max(peor, np.linalg.norm(A - N) / escala)
    return float(peor)


# ------------------------------------------------------------------- paso ---

def paso(red, X, Y, eta, mu=0.0):
    """Un paso de descenso: W ← W − η(∇_W L + 2μW), b ← b − η ∇_b L.
    Devuelve una red nueva; no toca la que recibe."""
    grad_W, grad_b = gradiente(red, X, Y, mu)
    nueva = {"W": [None], "b": [None], "g": list(red["g"])}
    for l in range(1, capas(red) + 1):
        nueva["W"].append(red["W"][l] - eta * grad_W[l])
        nueva["b"].append(red["b"][l] - eta * grad_b[l])
    return nueva


# ------------------------------------------------------------ entrenamiento ---

SEMILLAS = {"datos": 4, "pesos": 3, "lotes": 103}

ANCHOS_ENTRENAMIENTO = (2, 32, 32, 1)
ACTIVACIONES_ENTRENAMIENTO = ("relu", "relu", "identidad")
N_ENTRENAMIENTO = 80
N_VALIDACION = 200
RUIDO = 0.3            # desviación estándar del ruido normal
ETA_ENTRENAMIENTO = 0.03
LOTE = 20              # 80 / 20 = 4 pasos por época
EPOCAS = 1500
MU_ENTRENAMIENTO = 0.003


def funcion_verdadera(X):
    """f(x₁, x₂) = sin(π x₁) · cos(π x₂ / 2), la curva que los datos siguen."""
    return np.sin(np.pi * X[0]) * np.cos(np.pi * X[1] / 2)


def datos_ejemplo(semilla=SEMILLAS["datos"]):
    """x uniforme en [−1, 1]², y = f(x) + ruido normal de desviación RUIDO.
    Devuelve X, Y (entrenamiento) y X_val, Y_val (validación), en columnas."""
    rng = np.random.default_rng(semilla)
    X = rng.uniform(-1, 1, (2, N_ENTRENAMIENTO))
    X_val = rng.uniform(-1, 1, (2, N_VALIDACION))
    Y = funcion_verdadera(X) + RUIDO * rng.standard_normal(N_ENTRENAMIENTO)
    Y_val = (funcion_verdadera(X_val)
             + RUIDO * rng.standard_normal(N_VALIDACION))
    return X, Y[None, :], X_val, Y_val[None, :]


def red_inicial(anchos, activaciones, semilla=SEMILLAS["pesos"]):
    """Pesos normales escalados por √(2 / d_{l-1}) (He); sesgos en cero."""
    rng = np.random.default_rng(semilla)
    red = {"W": [None], "b": [None], "g": [None, *activaciones]}
    for l in range(1, len(anchos)):
        escala = np.sqrt(2 / anchos[l - 1])
        red["W"].append(rng.standard_normal((anchos[l], anchos[l - 1]))
                        * escala)
        red["b"].append(np.zeros(anchos[l]))
    return red


def entrenar(red, X, Y, X_val, Y_val, eta, mu, epocas, lote,
             semilla=SEMILLAS["lotes"]):
    """Descenso por minibatch. En cada época se barajan las observaciones y
    se da un paso por lote. Historia: RMSE de entrenamiento y de validación
    antes de entrenar (época 0) y al final de cada época."""
    rng = np.random.default_rng(semilla)
    historia = {"rmse_entrenamiento": [rmse(red, X, Y)],
                "rmse_validacion": [rmse(red, X_val, Y_val)]}
    for _ in range(epocas):
        orden = rng.permutation(X.shape[1])
        for inicio in range(0, len(orden), lote):
            k = orden[inicio:inicio + lote]
            red = paso(red, X[:, k], Y[:, k], eta, mu)
        historia["rmse_entrenamiento"].append(rmse(red, X, Y))
        historia["rmse_validacion"].append(rmse(red, X_val, Y_val))
    return red, historia


def entrenar_ejemplo(mu=0.0, epocas=EPOCAS):
    """El entrenamiento de la página 5: red 2–32–32–1 ReLU sobre los datos de
    datos_ejemplo(), mismos pesos iniciales y mismo barajado para todo μ.
    Devuelve la historia {rmse_entrenamiento, rmse_validacion}, cada una con
    epocas + 1 valores (el primero es antes de entrenar)."""
    X, Y, X_val, Y_val = datos_ejemplo()
    red = red_inicial(ANCHOS_ENTRENAMIENTO, ACTIVACIONES_ENTRENAMIENTO)
    _, historia = entrenar(red, X, Y, X_val, Y_val, ETA_ENTRENAMIENTO, mu,
                           epocas, LOTE)
    return historia


@lru_cache(maxsize=None)
def _historias():
    return entrenar_ejemplo(0.0), entrenar_ejemplo(MU_ENTRENAMIENTO)


# ------------------------------------------------------------------ cifras ---

def _r(v):
    """Redondea a 3 decimales; un escalar sale float, un arreglo, lista de
    listas. Suma 0.0 para que nunca salga -0.0."""
    return (np.round(np.asarray(v, dtype=float), 3) + 0.0).tolist()


def cifras():
    """Todas las cifras que citan las páginas, redondeadas a 3 decimales.

    Claves del ejemplo 2–3–2–1 (l = 1, 2, 3): z1..z3, a1..a3, y_gorro,
    perdida, delta1..delta3, grad_W1..grad_W3, grad_b1..grad_b3, omega y
    omega_por_capa (la norma de Frobenius al cuadrado de cada W);
    el paso: eta, perdida_tras_paso, y con μ: mu, perdida_tras_paso_mu;
    el entrenamiento (sin_mu / con_mu): rmse finales de entrenamiento y
    validación, el mínimo de validación sin μ y su época.
    """
    red, x, y = ejemplo()
    z, a, y_gorro = adelante(red, x)
    delta, grad_W, grad_b = atras(red, x, y)
    c = {"x": _r(x), "y": _r(y)}
    for l in (1, 2, 3):
        c[f"z{l}"] = _r(z[l])
        c[f"a{l}"] = _r(a[l])
        c[f"delta{l}"] = _r(delta[l])
        c[f"grad_W{l}"] = _r(grad_W[l])
        c[f"grad_b{l}"] = _r(grad_b[l])
    c["y_gorro"] = _r(y_gorro[0])
    c["perdida"] = _r(perdida(y_gorro, y))
    c["omega"] = _r(omega(red))
    c["omega_por_capa"] = _r([np.sum(W ** 2) for W in red["W"][1:]])
    c["rmse"] = _r(rmse(red, _columnas(x), _columnas(y)))
    # Parámetros de una red de anchos d_0..d_L: Σ_l d_l (d_{l-1} + 1).
    def parametros(anchos):
        return sum(d1 * (d0 + 1) for d0, d1 in zip(anchos[:-1], anchos[1:]))
    c["n_parametros"] = parametros([2, 3, 2, 1])
    c["n_parametros_784_16_16_10"] = parametros([784, 16, 16, 10])
    c["n_parametros_5_8_8_3"] = parametros([5, 8, 8, 3])
    c["n_parametros_5_3_colapsada"] = parametros([5, 3])
    c["eta"] = ETA_EJEMPLO
    nueva = paso(red, x, y, ETA_EJEMPLO)
    c["y_gorro_tras_paso"] = _r(adelante(nueva, x)[2][0])
    c["perdida_tras_paso"] = _r(perdida(adelante(nueva, x)[2], y))
    c["mu"] = MU_EJEMPLO
    nueva_mu = paso(red, x, y, ETA_EJEMPLO, MU_EJEMPLO)
    c["perdida_tras_paso_mu"] = _r(perdida(adelante(nueva_mu, x)[2], y))
    c["Wt_delta2"] = _r(red["W"][2].T @ delta[2])
    c["w3_11_tras_paso"] = _r(nueva["W"][3][0, 0])
    c["w3_11_tras_paso_mu"] = _r(nueva_mu["W"][3][0, 0])
    c["b3_tras_paso"] = _r(nueva["b"][3][0])
    c["error_comprobacion_menor_que_1e_10"] = bool(
        comprobar_gradiente(red, _columnas(x), _columnas(y)) < 1e-10)
    c["omega_tras_paso"] = _r(omega(nueva))
    c["omega_tras_paso_mu"] = _r(omega(nueva_mu))

    sin_mu, con_mu = _historias()
    for nombre, h in (("sin_mu", sin_mu), ("con_mu", con_mu)):
        c[f"rmse_entrenamiento_final_{nombre}"] = _r(h["rmse_entrenamiento"][-1])
        c[f"rmse_validacion_final_{nombre}"] = _r(h["rmse_validacion"][-1])
        val = np.array(h["rmse_validacion"])
        c[f"rmse_validacion_min_{nombre}"] = _r(val.min())
        c[f"epoca_validacion_min_{nombre}"] = int(val.argmin())
    c["mu_entrenamiento"] = MU_ENTRENAMIENTO
    c["epocas"] = EPOCAS
    return c


if __name__ == "__main__":
    for clave, valor in cifras().items():
        print(f"{clave:38s} {valor}")
