---
id: notacion-deep-learning
title: Toda la notación de redes neuronales, en una hoja
nav_title: Notación
summary: "Cada símbolo de la unidad de aprendizaje profundo, qué es, su dimensión y en qué página se presentó, con los avisos de letras que cambian de sentido respecto a la unidad 9."
status: ready
estimated_time: 10m
tags: [deep-learning, referencia, notacion]
---

# Toda la notación de redes neuronales, en una hoja

Todos los símbolos están definidos en su página. Si encuentras uno a media
lectura y no lo recuerdas, búscalo aquí.

**Cómo leer la flecha:** *→ página* dice dónde se **presentó** el símbolo.

## Convenciones que valen en toda la unidad

- **La capa va arriba, entre paréntesis.** $\mathbf W^{(l)}$, $\mathbf a^{(l)}$, $\mathbf z^{(l)}$: el $(l)$ nombra la capa; la capa 0 es la entrada.
- **Un peso se lee de destino a origen.** $w^{(l)}_{ij}$ va de la neurona $j$ de la capa $l-1$ a la neurona $i$ de la capa $l$. En $\mathbf W^{(l)}$ las filas son destinos y las columnas, orígenes.
- **Gorro para lo predicho,** como en la unidad 9: $\widehat{\mathbf y}$, $\widehat\theta$.
- **Observaciones con $k$.** $\mathbf x_k$, $\mathbf y_k$, con $k=1,\dots,n$.
- **$L$ tiene dos papeles.** Como superíndice o tope del índice de capa, $\mathbf a^{(L)}$ o $l=1,\dots,L$, es el número de capas. En cualquier otro lugar, $L(\theta)$ es la pérdida promedio.
- **$d$ con subíndice es un ancho.** $d_l$ es el ancho de la capa $l$; $d$ sola es la cota de $\Omega$.
- **Derivadas implícitas.** Se escribe $\nabla$; solo se expande lo que la página necesita.

## Avisos de letras que cambian respecto a la unidad 9

::: table {#dl-n-tab-avisos title="Letras que cambian de sentido"}
| Letra | En la unidad 9 | En esta unidad |
|---|---|---|
| $i$ | Índice de observación | Neurona de **destino**; la observación pasa a $k$ |
| $k$ | Número de pliegues | Índice de observación; aquí no hay pliegues |
| $\sigma$ | La sigmoide | Sigue siendo la sigmoide; la activación de una capa se llama $g^{(l)}$ |
| $g$ | La restricción $g(\beta)\le d$ | La activación $g^{(l)}$ |
| $\theta$ | Ángulo polar | Todos los pesos y sesgos; hace el papel de $\beta$ |
| $n$ | Número de observaciones | Igual; el ancho de una capa es $d_l$ |
| $L$ | Pérdida promedio | Igual, $L(\theta)$; como superíndice o tope de $l$, el número de capas |
| $d$ | Cota de la restricción | Igual; el ancho de una capa lleva subíndice, $d_l$ |
| $w$ | El peso de clase $w_y$ | El peso $w^{(l)}_{ij}$ de una conexión |
| $b$ | Las pendientes $b_j$ de mínimos cuadrados | El sesgo $b^{(l)}_i$ de una neurona |
| $\delta$ | La probabilidad de fallar; la cobertura es $1-\delta$ | El error $\delta^{(l)}_i$ de una neurona |
| $B$ | El número de árboles de un bosque | No aparece; $\mathcal B$ caligráfica es un lote |
| $h$ | La unidad $h$ de una red de una capa, con $\gamma_h$ | El paso de las diferencias finitas; aquella unidad es la neurona $i$ de la capa 1 |
| $\eta$ | $\eta(x)=\Pr(y=1\mid x)$ | Tasa de aprendizaje; es el paso $\alpha$ de la unidad 6 |
| $\mathcal L$ | El lagrangeano | Igual: $\mathcal L(\theta,\mu)=L(\theta)+\mu(\Omega(\theta)-d)$ |
:::

## Página 1 · La red

::: table {#dl-n-tab-red title="Símbolos de la red"}
| Símbolo | Qué es | Dimensión |
|---|---|---|
| $L$ | Número de capas con parámetros, como superíndice o tope de $l$ | entero |
| $l$ | Índice de capa, $l=1,\dots,L$ | entero |
| $d_l$ | Ancho de la capa $l$ (número de neuronas) | entero |
| $\mathbf x=\mathbf a^{(0)}$ | Entrada de la red | $d_0\times1$ |
| $\mathbf a^{(l)}$, $a^{(l)}_i$ | Activaciones de la capa $l$ y la de la neurona $i$ | $d_l\times1$ |
| $w^{(l)}_{ij}$ | Peso de la neurona $j$ (capa $l-1$) a la $i$ (capa $l$) | escalar |
| $\mathbf W^{(l)}$ | Matriz de pesos hacia la capa $l$ | $d_l\times d_{l-1}$ |
| $\mathbf b^{(l)}$, $b^{(l)}_i$ | Sesgos de la capa $l$ | $d_l\times1$ |
| $\theta$ | Todos los pesos y sesgos | parámetros |
:::

## Página 2 · La composición

::: table {#dl-n-tab-composicion title="Símbolos de la composición"}
| Símbolo | Qué es | Dimensión |
|---|---|---|
| $\mathbf z^{(l)}$, $z^{(l)}_i$ | Preactivaciones: $\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$ | $d_l\times1$ |
| $g^{(l)}$ | Activación de la capa $l$: una $g:\mathbb R\to\mathbb R$ aplicada a cada componente | $\mathbb R^{d_l}\to\mathbb R^{d_l}$ |
| $\mathrm{ReLU}$ | $\max(0,z)$ | — |
| $f^{(l)}$ | La capa $l$ como función: $g^{(l)}(\mathbf W^{(l)}\mathbf u+\mathbf b^{(l)})$ | — |
| $f_\theta$ | La red: $f^{(L)}\circ\cdots\circ f^{(1)}$ | — |
| $\widehat{\mathbf y}$ | La predicción $f_\theta(\mathbf x)$ | $d_L\times1$ |
| $\mathbf W'$, $\mathbf b'$ | La matriz y el sesgo de una red sin activaciones, colapsada en una capa afín | $d_L\times d_0$, $d_L\times1$ |
:::

## Página 3 · La pérdida y el lagrangeano

::: table {#dl-n-tab-perdida title="Símbolos de la pérdida"}
| Símbolo | Qué es |
|---|---|
| $k$, $n$ | Índice de observación y número de observaciones |
| $\ell(\widehat{\mathbf y},\mathbf y)$ | Pérdida de una observación; en regresión, $(\widehat y-y)^2$ |
| $\ell_k$ | La pérdida de la observación $k$ |
| $L(\theta)$ | Pérdida promedio, $\frac1n\sum_k\ell$; es el MSE en regresión |
| $\mathrm{MSE}$, $\mathrm{RMSE}$ | Como en la unidad 9; $\mathrm{RMSE}=\sqrt{\mathrm{MSE}}$ |
| $\widehat\theta$ | El $\theta$ que minimiza la pérdida |
| $\lVert\mathbf W\rVert_F^2$ | Suma de los cuadrados de las entradas de $\mathbf W$ |
| $\Omega(\theta)$, $d$ | La medida de capacidad (ridge: $\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$) y su cota |
| $\mathcal L(\theta,\mu)$ | El lagrangeano $L(\theta)+\mu(\Omega(\theta)-d)$, con $\mu\ge0$ |
:::

## Página 4 · La retropropagación

::: table {#dl-n-tab-retro title="Símbolos de la retropropagación"}
| Símbolo | Qué es |
|---|---|
| $\mathbf u$, $\mathbf v$, $\mathbf s$ | Tres vectores cualesquiera en cadena: $\mathbf s$ depende de $\mathbf v$ y $\mathbf v$ de $\mathbf u$ |
| $\dim\mathbf u$ | El número de componentes de $\mathbf u$ |
| $\partial\mathbf v/\partial\mathbf u$ | Jacobiana: fila por cada salida, columna por cada entrada; $\dim\mathbf v\times\dim\mathbf u$ |
| $\nabla_{\mathbf u}\ell$ | Gradiente columna de $\ell$ respecto a $\mathbf u$ |
| $\mathbf{δ}^{(l)}$, $\delta^{(l)}_i$ | Error de la capa $l$: $\nabla_{\mathbf z^{(l)}}\ell$ |
| $\odot$ | Producto componente a componente |
| $g^{(l)\prime}$ | Derivada de la activación; en ReLU, por convención, $g'(0)=0$ |
| $h$ | Paso de las diferencias finitas |
:::

## Página 5 · Entrenar

::: table {#dl-n-tab-entrenar title="Símbolos del entrenamiento"}
| Símbolo | Qué es |
|---|---|
| $\eta$ | Tasa de aprendizaje, $\eta>0$ |
| $\mathcal B$, $\lvert\mathcal B\rvert$ | Un lote de observaciones y su tamaño |
| $L_{\mathcal B}$ | La pérdida promedio del lote |
| $\Omega_1$ | La capacidad de lasso, como en la unidad 9: la suma de los $\lvert w^{(l)}_{ij}\rvert$ |
| $\operatorname{sign}(w)$ | El signo de $w$: $+1$, $-1$ o 0, como en la unidad 9 |
:::
