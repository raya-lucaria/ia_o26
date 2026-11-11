"""Genera el notebook de la clase 1 de aprendizaje profundo para Colab.

Escribe course/10_deep_learning/_assets/01_red_desde_cero.ipynb, guardado sin
salidas: la red 2–3–2–1 del hilo (pesos, pase hacia adelante, pérdida,
retropropagación y su comprobación por diferencias finitas, un paso de
descenso), el entrenamiento de la página 5 sin μ y con μ, y tres «apuesta y
luego corre».

Colab no tiene el repositorio, así que el notebook no importa redes.py: cada
celda «fuente» es un tramo de renglones de tools/redes.py, copiado tal cual
(de la primera a la última definición que nombra TRAMOS). La prosa, la celda
de arranque y las celdas que corren viven en este archivo; los parámetros que
cita la prosa (η, μ, épocas, lote…) se leen de redes.py, no se escriben aquí.

Correrlo después de cambiar redes.py o algo de aquí:
`python3 tools/gen_cuaderno_redes.py`. Es idempotente, y
test_cuaderno_redes.py falla si el notebook comiteado no es el que este
generador produce hoy.
"""
import ast
import json
import sys
from pathlib import Path

import redes

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "tools" / "redes.py"
RUTA = "course/10_deep_learning/_assets/01_red_desde_cero.ipynb"
URL = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
       "blob/main/" + RUTA)
URL_CLASE = ("https://raya-lucaria.github.io/ia_o26/deep-learning/"
             "redes-neuronales/")
CELDAS = []

# Valores que cita la prosa: salen de redes.py.
VALORES = {
    "ETA_EJEMPLO": redes.ETA_EJEMPLO,
    "MU_EJEMPLO": redes.MU_EJEMPLO,
    "ETA": redes.ETA_ENTRENAMIENTO,
    "MU": redes.MU_ENTRENAMIENTO,
    "EPOCAS": redes.EPOCAS,
    "LOTE": redes.LOTE,
    "PASOS": redes.N_ENTRENAMIENTO // redes.LOTE,
    "N_ENT": redes.N_ENTRENAMIENTO,
    "N_VAL": redes.N_VALIDACION,
    "RUIDO": redes.RUIDO,
    "ANCHOS": "–".join(str(d) for d in redes.ANCHOS_ENTRENAMIENTO),
}
# Las tres apuestas: lo que cambia respecto al entrenamiento de la sección 6.
ETA_APUESTA, EPOCAS_APUESTA_ETA = 0.5, 300
MU_APUESTA = 0.03
ANCHOS_APUESTA = (2, 4, 4, 1)


def md(texto):
    for clave, valor in VALORES.items():
        texto = texto.replace(f"@{clave}@", str(valor))
    assert "@" not in texto.replace("@title", ""), texto
    CELDAS.append({"cell_type": "markdown", "metadata": {},
                   "source": texto.strip("\n")})


def code(texto, *tags, oculta=False):
    meta = {}
    if oculta:
        meta["cellView"] = "form"
    if tags:
        meta["tags"] = list(tags)
    CELDAS.append({"cell_type": "code", "execution_count": None,
                   "metadata": meta, "outputs": [],
                   "source": texto.strip("\n")})


# --- Las celdas «fuente» son tramos literales de redes.py ------------------
def definiciones(texto):
    """{nombre: (primer renglón, último renglón)} de cada def y asignación
    de primer nivel, contando desde 1."""
    res = {}
    for nodo in ast.parse(texto).body:
        inicio = min([nodo.lineno] + [d.lineno for d in
                                      getattr(nodo, "decorator_list", [])])
        if isinstance(nodo, ast.FunctionDef):
            res[nodo.name] = (inicio, nodo.end_lineno)
        elif isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                res[t.id] = (inicio, nodo.end_lineno)
    return res


def tramo(primero, ultimo):
    texto = FUENTE.read_text(encoding="utf-8")
    renglones, defs = texto.split("\n"), definiciones(texto)
    return "\n".join(renglones[defs[primero][0] - 1:defs[ultimo][1]])


def fuente(primero, ultimo=None):
    code(tramo(primero, ultimo or primero), "fuente")


# ================================================================ 0 ===
md(f"""
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({URL})

# Notebook 1 · Una red desde cero

Acompaña la [Clase 1 · Redes neuronales]({URL_CLASE}). Solo usa numpy y
matplotlib, que Colab ya trae.

- Primero: **Entorno de ejecución → Ejecutar todas** (`Ctrl + F9`), o corre
  la celda «▶ Corre esta celda primero» y sigue de arriba abajo.
- Las celdas con funciones son el código de la página, copiado tal cual: no
  hace falta nada más.
- Al final hay tres **apuestas**: escribe tu predicción *antes* de correr.
""")

code(r'''
#@title ▶ Corre esta celda primero
import copy

import matplotlib.pyplot as plt
import numpy as np

plt.style.use("default")                     # fondo claro
plt.rcParams.update({"figure.facecolor": "white", "axes.grid": True,
                     "grid.alpha": 0.3, "font.size": 11})


def fmt(v):
    """Un número o un vector con 3 decimales: 0.546, [0.200, 0.000]."""
    v = np.round(np.asarray(v, dtype=float), 3) + 0.0
    if v.ndim == 0:
        return f"{v:.3f}"
    return "[" + ", ".join(f"{t:.3f}" for t in v) + "]"


def mostrar(nombre, M):
    """Una matriz con sus ejes: filas = destino i, columnas = origen j."""
    filas, columnas = M.shape
    print(f"{nombre}: {filas} × {columnas}  (filas = destino i, "
          "columnas = origen j)")
    print("       " + "".join(f"   j = {j}" for j in range(1, columnas + 1)))
    for i in range(filas):
        valores = np.round(M[i], 3) + 0.0
        print(f"i = {i + 1}  " + "".join(f"{t:8.3f}" for t in valores))


print("Listo: numpy", np.__version__)
''', "arranque", oculta=True)

# ================================================================ 1 ===
md(r"""
## 1 · La red 2–3–2–1

La capa 0 es la entrada $\mathbf x$; las capas $l = 1, \dots, L$ tienen
parámetros. La capa $l$ tiene $d_l$ neuronas. Aquí $L = 3$ y
$d_0, d_1, d_2, d_3 = 2, 3, 2, 1$.

- $w^{(l)}_{ij}$ es el peso que va de la neurona $j$ de la capa $l-1$
  (**origen**) a la neurona $i$ de la capa $l$ (**destino**).
- $\mathbf W^{(l)} \in \mathbb R^{d_l \times d_{l-1}}$ junta esos pesos:
  filas = destino $i$, columnas = origen $j$.
- $\mathbf b^{(l)} \in \mathbb R^{d_l}$ es el sesgo de la capa $l$.

**Aviso.** Aquí $i$ y $j$ numeran **neuronas**. Las observaciones llevan el
índice $k$: $(\mathbf x_k, \mathbf y_k)$, con $k = 1, \dots, n$.

En el código, `red["W"][l]` es $\mathbf W^{(l)}$ y `red["W"][l][i-1, j-1]` es
$w^{(l)}_{ij}$ (Python cuenta desde 0). La posición 0 de cada lista vale
`None`: la entrada no tiene parámetros.
""")

fuente("ejemplo", "capas")

code("""
red, x, y = ejemplo()
L = capas(red)
anchos = [len(x)] + [len(b) for b in red["b"][1:]]
print("anchos d_0, ..., d_L:", anchos, "  L =", L, "\\n")
for l in range(1, L + 1):
    mostrar(f"W^({l})", red["W"][l])
    print(f"b^({l}) = {fmt(red['b'][l])}   g^({l}) = {red['g'][l]}\\n")
""")

md(r"""
Cuenta los parámetros: $\mathbf W^{(l)}$ tiene $d_l \cdot d_{l-1}$ entradas y
$\mathbf b^{(l)}$ tiene $d_l$. Todos juntos son $\theta$.
""")

code("""
for l in range(1, L + 1):
    print(f"capa {l}: {red['W'][l].size} pesos + {red['b'][l].size} sesgos")
print("total de parámetros en θ:",
      sum(red["W"][l].size + red["b"][l].size for l in range(1, L + 1)))
""")

# ================================================================ 2 ===
md(r"""
## 2 · Hacia adelante

Cada capa hace dos cosas:

$$\mathbf z^{(l)} = \mathbf W^{(l)} \mathbf a^{(l-1)} + \mathbf b^{(l)},
\qquad \mathbf a^{(l)} = g^{(l)}\bigl(\mathbf z^{(l)}\bigr),
\qquad \mathbf a^{(0)} = \mathbf x .$$

$\mathbf z^{(l)}$ es la preactivación y $\mathbf a^{(l)}$ la activación. La
red es la composición $f_\theta = f^{(L)} \circ \cdots \circ f^{(1)}$, con
$f^{(l)}(\mathbf u) = g^{(l)}(\mathbf W^{(l)} \mathbf u + \mathbf b^{(l)})$, y
la predicción es $\widehat{\mathbf y} = f_\theta(\mathbf x) = \mathbf a^{(L)}$.

**Aviso.** La activación se llama $g^{(l)}$, no $\sigma$: en la unidad 9,
$\sigma$ es la sigmoide. Aquí la sigmoide es una $g$ posible; las ocultas
usan ReLU, $g(z) = \max(0, z)$, y la salida usa la identidad.
""")

fuente("relu", "ACTIVACIONES")

md(r"""
La pérdida de **una** observación es $\ell(\widehat{\mathbf y}, \mathbf y) =
\sum (\widehat y - y)^2$, sin $\tfrac12$ (igual que el MSE de la unidad 9).
""")

fuente("adelante", "perdida")

code("""
z, a, y_gorro = adelante(red, x)
print(f"a^(0) = x = {fmt(x)}")
for l in range(1, L + 1):
    print(f"capa {l}: z^({l}) = {fmt(z[l])}  →  a^({l}) = {fmt(a[l])}")
print(f"\\nŷ = {fmt(y_gorro[0])}   y = {fmt(y[0])}")
print(f"ℓ(ŷ, y) = (ŷ − y)² = {fmt(perdida(y_gorro, y))}")
""")

md(r"""
**Mira.** En la capa 1, $z^{(1)}_2$ es negativa: ReLU la vuelve 0 y esa
neurona no pasa nada hacia adelante. En la sección 4 vas a ver que tampoco
recibe nada hacia atrás.
""")

# ================================================================ 3 ===
md(r"""
## 3 · La pérdida de un conjunto y el lagrangeano

Con $n$ observaciones, la pérdida es el promedio, como en la unidad 9:

$$L(\theta) = \frac1n \sum_{k=1}^{n}
\ell\bigl(f_\theta(\mathbf x_k), \mathbf y_k\bigr) = \mathrm{MSE},
\qquad \mathrm{RMSE} = \sqrt{\mathrm{MSE}} .$$

Para que la red generalice, se limita su capacidad: minimizar $L(\theta)$
sujeto a $\Omega(\theta) \le d$, con $\Omega(\theta) = \sum_l
\lVert \mathbf W^{(l)} \rVert_F^2$ (ridge; los sesgos no se penalizan). El
lagrangeano junta las dos cosas, con $\mu \ge 0$:

$$\mathcal L(\theta, \mu) = L(\theta) + \mu\,\bigl(\Omega(\theta) - d\bigr).$$

En el código, `X` y `Y` llevan **una columna por observación** $k$. Un
vector suelto cuenta como una sola columna. Con $\mu$ fijo, $d$ no cambia
dónde está el mínimo; por eso el código usa $d = 0$ si no se le da otro.
""")

fuente("_columnas", "lagrangeano")

code("""
print(f"Ω(θ) = Σ_l ‖W^(l)‖² = {fmt(omega(red))}")
print(f"L(θ) con la única observación = {fmt(perdida_promedio(red, x, y))}")
print(f"RMSE = √L = {fmt(rmse(red, x, y))}")
for mu in (0.0, MU_EJEMPLO):
    print(f"𝓛(θ, μ = {mu}) = {fmt(lagrangeano(red, x, y, mu))}")
""")

# ================================================================ 4 ===
md(r"""
## 4 · Retropropagación

El error retropropagado de la capa $l$ es $\boldsymbol\delta^{(l)} :=
\nabla_{\mathbf z^{(l)}} \ell$, de **una** observación. Se calcula de la
salida hacia la entrada:

$$\boldsymbol\delta^{(L)} = \nabla_{\mathbf a^{(L)}} \ell \odot
g^{(L)\prime}\bigl(\mathbf z^{(L)}\bigr), \qquad
\boldsymbol\delta^{(l)} = \bigl(\mathbf W^{(l+1)\mathsf T}
\boldsymbol\delta^{(l+1)}\bigr) \odot g^{(l)\prime}\bigl(\mathbf z^{(l)}\bigr).$$

Con $\ell = (\widehat y - y)^2$, $\nabla_{\mathbf a^{(L)}} \ell =
2(\widehat{\mathbf y} - \mathbf y)$. Y los gradientes salen de $\boldsymbol
\delta$:

$$\nabla_{\mathbf W^{(l)}} \ell = \boldsymbol\delta^{(l)}
\mathbf a^{(l-1)\mathsf T}, \qquad \nabla_{\mathbf b^{(l)}} \ell =
\boldsymbol\delta^{(l)}, \qquad \frac{\partial \ell}{\partial w^{(l)}_{ij}}
= \delta^{(l)}_i\, a^{(l-1)}_j .$$

Error del destino por activación del origen. En ReLU se toma
$g'(0) = 0$.
""")

fuente("atras")

code("""
delta, grad_W, grad_b = atras(red, x, y)
for l in range(L, 0, -1):
    print(f"δ^({l}) = {fmt(delta[l])}")
    mostrar(f"∇_{{W^({l})}} ℓ = δ^({l}) a^({l - 1})ᵀ", grad_W[l])
    print(f"∇_{{b^({l})}} ℓ = δ^({l}) = {fmt(grad_b[l])}\\n")
""")

md(r"""
**Mira.** $\delta^{(1)}_2 = 0$: la neurona apagada tiene $g' = 0$, así que
toda la fila 2 de $\nabla_{\mathbf W^{(1)}} \ell$ es cero. Y cada entrada es
«error del destino × activación del origen»:
""")

code("""
i, j = 1, 2                          # el peso w^(1)_12 (índices desde 1)
print(f"δ^(1)_{i} · a^(0)_{j} = {fmt(delta[1][i - 1] * x[j - 1])}")
print(f"∂ℓ/∂w^(1)_{i}{j}      = {fmt(grad_W[1][i - 1, j - 1])}")
""")

md(r"""
**¿Está bien?** Se comprueba sin derivar: se mueve un solo parámetro un
poquito, $h$, hacia arriba y hacia abajo, y se mide el cambio de la pérdida:

$$\frac{\mathcal L(\theta + h\,\mathbf e) - \mathcal L(\theta - h\,\mathbf e)}
{2h} .$$

`gradiente` es la retropropagación de un **lote** (columnas = observaciones):
promedia los gradientes de $\ell$ y suma $2\mu\mathbf W^{(l)}$ a cada
$\mathbf W^{(l)}$. Con una sola observación y $\mu = 0$ da lo mismo que
`atras`. El error relativo compara los dos:
$\lVert a - n \rVert / (\lVert a \rVert + \lVert n \rVert)$.
""")

fuente("gradiente")
fuente("gradiente_numerico", "comprobar_gradiente")

code("""
grad_W_num, grad_b_num = gradiente_numerico(red, x, y)
mostrar("∇_{W^(1)} ℓ por diferencias finitas", grad_W_num[1])
error = comprobar_gradiente(red, x, y)
error_mu = comprobar_gradiente(red, x, y, MU_EJEMPLO)
print(f"\\nerror relativo máximo, μ = 0:    {error:.1e}")
print(f"error relativo máximo, μ = {MU_EJEMPLO}: {error_mu:.1e}")
print("¿coinciden?", error < 1e-6 and error_mu < 1e-6)
""")

# ================================================================ 5 ===
md(r"""
## 5 · Un paso de descenso

Se mueve $\theta$ contra el gradiente, con una tasa de aprendizaje
$\eta > 0$ (una letra nueva: en la unidad 9 no aparece):

$$\theta \leftarrow \theta - \eta\, \nabla_\theta \mathcal L, \qquad
\mathbf W^{(l)} \leftarrow \mathbf W^{(l)} - \eta\bigl(\nabla_{\mathbf
W^{(l)}} L + 2\mu \mathbf W^{(l)}\bigr).$$

El término $2\mu\mathbf W^{(l)}$ encoge cada peso un poco en cada paso: es
el **decaimiento de pesos**. Aquí $\eta = @ETA_EJEMPLO@$ y $\mu = @MU_EJEMPLO@$.
""")

fuente("paso")

code("""
nueva = paso(red, x, y, ETA_EJEMPLO)
y_nueva = adelante(nueva, x)[2]
print(f"η = {ETA_EJEMPLO}")
print(f"antes:   ŷ = {fmt(y_gorro[0])}   ℓ = {fmt(perdida(y_gorro, y))}"
      f"   Ω = {fmt(omega(red))}")
print(f"después: ŷ = {fmt(y_nueva[0])}   ℓ = {fmt(perdida(y_nueva, y))}"
      f"   Ω = {fmt(omega(nueva))}")
nueva_mu = paso(red, x, y, ETA_EJEMPLO, MU_EJEMPLO)
y_mu = adelante(nueva_mu, x)[2]
print(f"con μ = {MU_EJEMPLO}: ŷ = {fmt(y_mu[0])}   ℓ = {fmt(perdida(y_mu, y))}"
      f"   Ω = {fmt(omega(nueva_mu))}")
""")

md(r"""
Un paso basta para que $\ell$ baje mucho. Con $\mu > 0$, $\Omega$ crece
menos: el decaimiento frena a los pesos. Ahora cinco pasos seguidos:
""")

code("""
red_t = red
for t in range(6):
    print(f"paso {t}: ℓ = {fmt(perdida(adelante(red_t, x)[2], y))}")
    red_t = paso(red_t, x, y, ETA_EJEMPLO)
""")

# ================================================================ 6 ===
md(r"""
## 6 · Entrenar sin μ y con μ

Ahora una red de verdad, $@ANCHOS@$ con ReLU, sobre datos sintéticos:
$y = \sin(\pi x_1)\cos(\pi x_2 / 2)$ más ruido normal de desviación
$@RUIDO@$, con $@N_ENT@$ observaciones de entrenamiento y $@N_VAL@$ de
validación.

- Pesos iniciales normales escalados por $\sqrt{2 / d_{l-1}}$; sesgos en 0.
- **Minibatch**: en cada época se barajan las observaciones y se da un paso
  por lote de $@LOTE@$ ($@PASOS@$ pasos por época), promediando los
  gradientes del lote.
- $\eta = @ETA@$ y $@EPOCAS@$ épocas, sin $\mu$ y con $\mu = @MU@$: los
  mismos pesos iniciales y el mismo barajado en las dos corridas.
""")

fuente("SEMILLAS", "datos_ejemplo")

code("""
X, Y, X_val, Y_val = datos_ejemplo()
print("X:", X.shape, "  Y:", Y.shape, "  (columnas = observaciones k)")
print("X_val:", X_val.shape, "  Y_val:", Y_val.shape)
""")

fuente("red_inicial", "entrenar")
fuente("entrenar_ejemplo")

code("""
sin_mu = entrenar_ejemplo(0.0)                     # unos segundos
con_mu = entrenar_ejemplo(MU_ENTRENAMIENTO)
for nombre, h in (("sin μ", sin_mu), (f"μ = {MU_ENTRENAMIENTO}", con_mu)):
    ent, val = h["rmse_entrenamiento"], np.array(h["rmse_validacion"])
    print(f"{nombre}: RMSE final ent. = {fmt(ent[-1])}, "
          f"val. = {fmt(val[-1])}; mejor val. = {fmt(val.min())} "
          f"en la época {val.argmin()}")
""")

code("""
fig, ejes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
titulos = ("Sin μ", f"Con μ = {MU_ENTRENAMIENTO}")
for eje, h, titulo in zip(ejes, (sin_mu, con_mu), titulos):
    eje.plot(h["rmse_entrenamiento"], label="entrenamiento")
    eje.plot(h["rmse_validacion"], label="validación")
    eje.axhline(RUIDO, color="gray", ls="--", label="ruido")
    eje.set(title=titulo, xlabel="época", ylabel="RMSE", ylim=(0, 0.9))
    eje.legend()
fig.suptitle("RMSE por época, red " + "–".join(map(str, ANCHOS_ENTRENAMIENTO)))
plt.show()
""")

md(r"""
**Lee las curvas.** Sin $\mu$, la RMSE de entrenamiento sigue bajando, pero
la de validación toca fondo y vuelve a subir: la red empieza a memorizar el
ruido. Con $\mu$, el entrenamiento baja menos y la validación termina más
abajo. Ninguna puede bajar mucho del ruido (la línea punteada) en
validación: ese error no se puede aprender.
""")

# ================================================================ 7 ===
md(r"""
## 7 · Apuesta y luego corre

Tres cambios de un número. Para cada uno: lee la pregunta, **escribe tu
apuesta** y solo después corre la celda. Las tres usan esta función, que
entrena con los mismos datos y el mismo arranque de la sección 6.
""")

code("""
def apuesta(eta=ETA_ENTRENAMIENTO, mu=0.0, anchos=ANCHOS_ENTRENAMIENTO,
            epocas=EPOCAS):
    red_0 = red_inicial(anchos, ACTIVACIONES_ENTRENAMIENTO)
    red_f, h = entrenar(red_0, X, Y, X_val, Y_val, eta, mu, epocas, LOTE)
    print(f"η = {eta}, μ = {mu}, red {'–'.join(map(str, anchos))}: "
          f"RMSE final ent. = {fmt(h['rmse_entrenamiento'][-1])}, "
          f"val. = {fmt(h['rmse_validacion'][-1])}")
    return red_f, h
""", "apuesta")

md(f"""
**Apuesta 1 · η.** Con $\\eta = {redes.ETA_ENTRENAMIENTO}$ la red aprende.
¿Qué pasa con $\\eta = {ETA_APUESTA}$?

- (a) aprende más rápido y termina mejor;
- (b) termina igual, pero llega antes;
- (c) se descompone y deja de aprender.
""")

code(f"""
red_eta, h_eta = apuesta(eta={ETA_APUESTA}, epocas={EPOCAS_APUESTA_ETA})
for t in (0, 1, 2, 10, {EPOCAS_APUESTA_ETA}):
    print(f"época {{t:>3}}:  η = {{ETA_ENTRENAMIENTO}} → "
          f"{{fmt(sin_mu['rmse_entrenamiento'][t])}}   "
          f"η = {ETA_APUESTA} → {{fmt(h_eta['rmse_entrenamiento'][t])}}")
y_eta = adelante(red_eta, X)[2]
print(f"\\nŷ va de {{fmt(y_eta.min())}} a {{fmt(y_eta.max())}}; "
      f"desviación estándar de y: {{fmt(Y.std())}}")
""", "apuesta")

md("""
<details><summary>Respuesta</summary>

**(c).** En la época 1 la RMSE salta a más de mil: el paso es tan largo
que se pasa del mínimo. Después, todas las $z$ de las ocultas quedan
negativas y ReLU las apaga ($g' = 0$): las $\\boldsymbol\\delta$ de las
ocultas valen cero y solo se mueve el sesgo de la salida. La red predice la
misma $\\widehat y$ para todo, y su RMSE es la desviación estándar de $y$ (lo
mejor que hace una constante). Una $\\eta$ grande no es «aprender más
rápido».

</details>
""")

md(f"""
**Apuesta 2 · μ.** Con $\\mu = {redes.MU_ENTRENAMIENTO}$ la validación
terminó mejor que sin $\\mu$. Con $\\mu$ diez veces mayor,
$\\mu = {MU_APUESTA}$, ¿la RMSE final de validación baja todavía más, o
sube? ¿Y la de entrenamiento?
""")

code(f"""
_, h_mu = apuesta(mu={MU_APUESTA})
for nombre, h in (("μ = 0", sin_mu), (f"μ = {{MU_ENTRENAMIENTO}}", con_mu),
                  ("μ = {MU_APUESTA}", h_mu)):
    print(f"{{nombre:>9}}: ent. = {{fmt(h['rmse_entrenamiento'][-1])}}, "
          f"val. = {{fmt(h['rmse_validacion'][-1])}}")
""", "apuesta")

md("""
<details><summary>Respuesta</summary>

**Suben las dos.** Con $\\mu$ grande, $\\Omega$ pesa más que $L$ en
$\\mathcal L$: los pesos quedan tan chicos que la red ya no alcanza a seguir
la curva. Antes sobraba capacidad; ahora falta. Por eso $\\mu$ se elige con
validación, como en la unidad 9: ni cero ni lo más grande posible.

</details>
""")

anchos_apuesta = "–".join(map(str, ANCHOS_APUESTA))
md(f"""
**Apuesta 3 · el ancho.** Sin $\\mu$, la red $@ANCHOS@$ terminó con mucha
distancia entre entrenamiento y validación. Con solo 4 neuronas por capa
oculta, $({anchos_apuesta})$ y sin $\\mu$, ¿esa distancia crece o se
achica? ¿Cuál termina mejor en validación?
""")

code(f"""
_, h_ancho = apuesta(anchos={ANCHOS_APUESTA})
for nombre, h in (("@ANCHOS@", sin_mu), ("{anchos_apuesta}", h_ancho)):
    ent, val = h["rmse_entrenamiento"][-1], h["rmse_validacion"][-1]
    print(f"{{nombre:>9}}: ent. = {{fmt(ent)}}, val. = {{fmt(val)}}, "
          f"distancia = {{fmt(val - ent)}}")
""".replace("@ANCHOS@", VALORES["ANCHOS"]), "apuesta")

md("""
<details><summary>Respuesta</summary>

**Se achica.** La red angosta tiene muchos menos parámetros: no le alcanza
para memorizar el ruido, así que su RMSE de entrenamiento sube y la de
validación baja. Quitar neuronas es otra forma de limitar la capacidad,
igual que $\\mu$: las dos acercan las curvas.

</details>

**Para cerrar.** Todo el entrenamiento es el mismo ciclo: hacia adelante
($\\mathbf z$, $\\mathbf a$, $\\widehat{\\mathbf y}$), la pérdida, hacia atrás
($\\boldsymbol\\delta$ y los gradientes) y un paso de descenso. Lo demás
(η, μ, el ancho) decide qué tan bien generaliza.
""")


def contenido():
    """El .ipynb como texto: nbformat 4, sin salidas."""
    celdas = []
    for c in CELDAS:
        lineas = c["source"].split("\n")
        fuente_ = [r + "\n" for r in lineas[:-1]] + [lineas[-1]]
        celdas.append(dict(c, source=fuente_))
    nb = {"cells": celdas,
          "metadata": {"colab": {"provenance": [], "toc_visible": True},
                       "kernelspec": {"display_name": "Python 3",
                                      "name": "python3"},
                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 0}
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


def main(argv):
    destino = RAIZ / RUTA
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido(), encoding="utf-8")
    print(f"escrito {destino.relative_to(RAIZ)}: {len(CELDAS)} celdas")


if __name__ == "__main__":
    main(sys.argv)
