---
id: dl-la-red
title: "La red: capas, pesos y sesgos"
nav_title: "La red"
summary: "Qué números guarda una red neuronal y cómo se nombran: capas y anchos, el peso de la neurona j a la neurona i, la matriz de pesos de cada capa con filas de destino y columnas de origen, y cuántos parámetros tiene la red 2–3–2–1."
status: ready
estimated_time: 35m
tags: [deep-learning, redes-neuronales, notacion, pesos]
prerequisites: [ml-la-metodologia]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 01 · Una red desde cero.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)
>
> **[👉 Abrir `01_red_desde_cero.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)**

# La red: capas, pesos y sesgos

**¿Qué números guarda una red neuronal, y cómo se nombra cada uno sin perderse entre capas?**

Al terminar tendrás:

- **Una red con nombre:** sus capas, de la 0 a la $L$, y el ancho $d_l$ de cada una.
- **Un peso bien leído:** $w^{(l)}_{ij}$ llega a la neurona $i$ de la capa $l$ y sale de la neurona $j$ de la capa $l-1$.
- **Una matriz por capa:** $\mathbf W^{(l)}$, de $d_l\times d_{l-1}$, con filas de destino y columnas de origen.
- **Una cuenta:** la red 2–3–2–1 tiene 20 parámetros.

> **Lo que traes**
>
> Neuronas, pesos y sesgos, de los videos de la [[dl-tarea-1|tarea de la clase 1]].
>
> La red de una capa de [[ml-la-metodologia|La metodología]] (@ml-c5-teo-cybenko): unidades sigmoides que aprenden su propia $\phi$.
>
> El modelo lineal $f_\beta(x)=\beta^{\mathsf T}\phi(x)$ (@ml-c1-def-modelo-lineal).

## 1 · Contar capas y neuronas

**Piensa: la red de la unidad 9 tenía una sola capa de unidades sigmoides. ¿Qué cambia si apilas varias?**

Cada capa hace lo mismo que aquella: combina lo que recibe y lo transforma.
Lo nuevo es que la salida de una capa es la entrada de la siguiente.
Con varias capas, cada número necesita un nombre que diga en qué capa vive.

::: figure {#dl-red-2-3-2-1 title="La red 2–3–2–1, el ejemplo de toda la clase"}
![La red 2–3–2–1 en cuatro columnas de neuronas, de izquierda a derecha: la capa 0 de entrada con x₁ y x₂ (d₀ = 2), la capa 1 oculta con tres neuronas (d₁ = 3), la capa 2 oculta con dos (d₂ = 2) y la capa 3 de salida con una (d₃ = 1), que es ŷ. Cada neurona se llama aᵢ⁽ˡ⁾. Cada flecha entre capas vecinas es un peso; se rotulan dos de la capa 1: w₁₁⁽¹⁾, de x₁ a a₁⁽¹⁾, y w₃₂⁽¹⁾, de x₂ a a₃⁽¹⁾. Abajo, los tamaños: W⁽¹⁾ es 3×2, W⁽²⁾ es 2×3 y W⁽³⁾ es 1×2.](../_assets/dl-red-2-3-2-1.svg)
:::

En la figura, la información fluye de izquierda a derecha.
Cada flecha une una neurona con una de la capa siguiente; no hay flechas dentro de una capa.

::: definition {#dl-def-capas title="Capas, anchos y activaciones"}
Una red tiene capas numeradas $l=0,1,\dots,L$.

- La **capa 0** es la entrada $\mathbf x$. No tiene parámetros.
- Las capas $1,\dots,L$ sí tienen parámetros. La capa $L$ es la **salida**; las de en medio son **ocultas**.
- El **ancho** $d_l$ es el número de neuronas de la capa $l$. La arquitectura se escribe con sus anchos: $d_0$–$d_1$–$\cdots$–$d_L$.
- La neurona $i$ de la capa $l$ guarda un número, su **activación** $a^{(l)}_i$. Las de la capa forman el vector $\mathbf a^{(l)}\in\mathbb R^{d_l}$, y $\mathbf a^{(0)}=\mathbf x$.
:::

En la 2–3–2–1, $L=3$ y los anchos son $d_0=2$, $d_1=3$, $d_2=2$ y $d_3=1$.
La entrada tiene dos variables, $\mathbf x=(x_1,x_2)$; la salida es un solo número.
Las dos capas ocultas son la 1 y la 2.

Cuatro avisos de notación, porque la unidad 9 usaba algunas de estas letras para otra cosa:

- **$d_l$, no $n_l$:** $n$ sigue siendo el número de observaciones.
- **$i$ y $j$ son neuronas.** En la unidad 9, $i$ era la observación y $j$ la variable. Aquí la observación usa $k$, desde la página 3.
- **El superíndice entre paréntesis es la capa,** no una potencia: $\mathbf a^{(2)}$ es la activación de la capa 2.
- **Negritas para vectores y matrices:** $\mathbf x$, $\mathbf a^{(l)}$; en cursiva, un número suelto como $a^{(l)}_i$.

**$L$ tiene dos papeles.** Como superíndice o tope del índice de capa, $\mathbf a^{(L)}$ o $l=1,\dots,L$, es el número de capas.
En cualquier otro lugar, $L(\theta)$ es la pérdida promedio de la unidad 9, que llega en la página 3.

Un aviso más, para el video 4 de la tarea.
Ahí el peso se escribe $w^{(L)}_{jk}$: $j$ es la neurona de destino, $k$ la de origen y $C_0$ el costo de una observación.
Aquí el destino es $i$, el origen es $j$, y $k$ es la observación.

::: exercise {#dl-ej-anchos title="Lee una arquitectura"}
Una red es 4–5–5–3.

(a) ¿Cuánto valen $L$, $d_0$ y $d_2$?

(b) ¿Cuántas capas ocultas tiene, y cuántos números devuelve?
:::

::: hint {#dl-pista-anchos-1 of="dl-ej-anchos" title="Pista 1 · Empieza a contar en cero"}
¿Qué número de capa le toca a la entrada, y cuenta la entrada como capa con parámetros?
:::

::: answer {#dl-resp-anchos of="dl-ej-anchos" title="Respuesta · Cuatro anchos, tres capas con parámetros"}
(a) Hay cuatro anchos, de la capa 0 a la 3: $L=3$, $d_0=4$ y $d_2=5$.

(b) Tiene dos capas ocultas, la 1 y la 2. Devuelve $d_3=3$ números.
:::

## 2 · Nombrar un peso

**Piensa: una flecha une dos neuronas de capas vecinas. ¿Qué datos necesita el nombre de su peso para no confundirse con ningún otro?**

Tres: la capa a la que llega, la neurona a la que llega y la neurona de la que sale.
La capa de salida no hace falta: siempre es la anterior.

::: figure {#dl-peso-wij title="Una sola conexión, de cerca"}
![Una sola conexión vista de cerca. A la izquierda, la neurona de origen j en la capa l − 1, con su activación aⱼ⁽ˡ⁻¹⁾; a la derecha, la neurona de destino i en la capa l, con su preactivación zᵢ⁽ˡ⁾. La flecha entre ellas es el peso wᵢⱼ⁽ˡ⁾ y aporta wᵢⱼ⁽ˡ⁾ · aⱼ⁽ˡ⁻¹⁾ a zᵢ⁽ˡ⁾. Abajo, la suma zᵢ⁽ˡ⁾ = Σⱼ wᵢⱼ⁽ˡ⁾ aⱼ⁽ˡ⁻¹⁾ + bᵢ⁽ˡ⁾ y la lectura de los índices: el primero, i, es el destino; el segundo, j, el origen; (l) es la capa a la que llega.](../_assets/dl-peso-wij.svg)
:::

La figura ya muestra a dónde va el producto: a una suma en la neurona de destino, que la página 2 llama $z^{(l)}_i$.

::: definition {#dl-def-peso title="El peso de una conexión y el sesgo de una neurona"}
$w^{(l)}_{ij}$ es el número que multiplica la activación $a^{(l-1)}_j$ cuando llega a la neurona $i$ de la capa $l$.

- El superíndice $(l)$ es la **capa de destino**.
- El primer subíndice, $i$, es la **neurona de destino**, en la capa $l$.
- El segundo, $j$, es la **neurona de origen**, en la capa $l-1$.

Cada neurona $i$ de la capa $l$ tiene además un **sesgo** $b^{(l)}_i$: un número que se suma a lo que llega y que no viene de ninguna neurona.

**Qué no es:** $w^{(l)}_{ij}$ no va «de $i$ a $j$». Se lee al revés de la flecha: primero a dónde llega, luego de dónde sale.
:::

El orden destino–origen parece incómodo. La sección 3 muestra por qué conviene.

En la 2–3–2–1, $w^{(1)}_{12}=-0.2$: llega a la neurona 1 de la capa 1 y sale de la neurona 2 de la capa 0, que es $x_2$.

> [!WARNING]
> Lectura equivocada: «$w^{(1)}_{12}$ va de la neurona 1 a la neurona 2».
>
> Lectura correcta: **$w^{(1)}_{12}$ llega a la neurona 1 de la capa 1 y sale de la neurona 2 de la capa 0.**

Dos letras de la unidad 9 cambian de sentido aquí.
Esta $w$ no es el peso de clase $w_y$; esta $b$ no son las pendientes $b_j$ de mínimos cuadrados.

::: exercise {#dl-ej-leer-peso title="Señala la flecha"}
En la capa 2 de la 2–3–2–1:

(a) ¿Qué flecha es $w^{(2)}_{21}$?

(b) ¿Cómo se llama el peso de la flecha que sale de la neurona 3 de la capa 1 y llega a la neurona 1 de la capa 2?
:::

::: hint {#dl-pista-leer-peso-1 of="dl-ej-leer-peso" title="Pista 1 · Ordena los índices"}
¿Cuál de los dos subíndices dice a dónde llega la flecha?
:::

::: answer {#dl-resp-leer-peso of="dl-ej-leer-peso" title="Respuesta · Primero el destino"}
(a) Llega a la neurona 2 de la capa 2 y sale de la neurona 1 de la capa 1.

(b) Es $w^{(2)}_{13}$: destino 1, origen 3, capa 2.
:::

## 3 · Juntar los pesos de una capa en una matriz

**Piensa: la capa 1 de la 2–3–2–1 tiene $3\times2=6$ pesos. ¿Cómo conviene acomodarlos?**

En una matriz, con una fila por neurona de destino y una columna por neurona de origen.
Así, la fila $i$ reúne todo lo que llega a la neurona $i$.

::: definition {#dl-def-matriz-pesos title="La matriz de pesos y el vector de sesgos de la capa l"}
Los pesos de la capa $l$ forman la matriz $\mathbf W^{(l)}\in\mathbb R^{d_l\times d_{l-1}}$, cuya entrada $(i,j)$ es $w^{(l)}_{ij}$:

$$
\mathbf W^{(l)}=
\begin{array}{c|cccc}
 & j=1 & j=2 & \cdots & j=d_{l-1}\\ \hline
i=1 & w^{(l)}_{11} & w^{(l)}_{12} & \cdots & w^{(l)}_{1\,d_{l-1}}\\
i=2 & w^{(l)}_{21} & w^{(l)}_{22} & \cdots & w^{(l)}_{2\,d_{l-1}}\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
i=d_l & w^{(l)}_{d_l\,1} & w^{(l)}_{d_l\,2} & \cdots & w^{(l)}_{d_l\,d_{l-1}}
\end{array}
$$

- **Filas:** una por neurona de **destino** $i$ de la capa $l$; hay $d_l$.
- **Columnas:** una por neurona de **origen** $j$ de la capa $l-1$; hay $d_{l-1}$.
- **Tamaño:** $d_l\times d_{l-1}$, «llegan por salen».
- **Sesgos:** $\mathbf b^{(l)}=(b^{(l)}_1,\dots,b^{(l)}_{d_l})\in\mathbb R^{d_l}$, uno por fila.
:::

En la 2–3–2–1, la capa 1 tiene 3 destinos y 2 orígenes:

$$
\mathbf W^{(1)}=
\begin{array}{c|cc}
 & j=1 & j=2\\ \hline
i=1 & 0.5 & -0.2\\
i=2 & -0.4 & 0.1\\
i=3 & 0.3 & 0.2
\end{array}
\qquad
\mathbf b^{(1)}=
\begin{array}{c|c}
i=1 & 0.1\\
i=2 & 0\\
i=3 & -0.1
\end{array}
$$

::: figure {#dl-matriz-w title="Cada entrada de W⁽¹⁾ es una flecha de la red"}
![La matriz W⁽¹⁾ en forma general, de 3 filas por 2 columnas, con entradas w₁₁⁽¹⁾ a w₃₂⁽¹⁾. Las filas se rotulan destino i = 1, 2, 3 (las neuronas a₁⁽¹⁾, a₂⁽¹⁾ y a₃⁽¹⁾ de la capa 1) y las columnas origen j = 1, 2 (las entradas x₁ y x₂). Se destacan la fila 3, que son las flechas que llegan a a₃⁽¹⁾; la columna 2, que son las flechas que salen de x₂; y su cruce w₃₂⁽¹⁾, que es la flecha de x₂ a a₃⁽¹⁾ en la red dibujada a la derecha. W⁽¹⁾ está en ℝ³ˣ²: d₁ = 3 filas y d₀ = 2 columnas.](../_assets/dl-matriz-w.svg)
:::

Ahora se ve por qué el destino va primero.
La fila $i$ multiplicada por $\mathbf a^{(l-1)}$ junta, en una suma, todo lo que llega a la neurona $i$:

$$
\sum_{j=1}^{d_{l-1}} w^{(l)}_{ij}\,a^{(l-1)}_j+b^{(l)}_i .
$$

Para toda la capa a la vez, eso es $\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$: un vector de $d_l$ números, uno por neurona.
La página 2 lo nombra y lo calcula con la 2–3–2–1.

La red de una capa de la unidad 9 (@ml-c5-teo-cybenko) es un caso de esta notación.
Su unidad $h$ usaba $\gamma_h$ y $\gamma_{0,h}$: son la fila $i=h$ de $\mathbf W^{(1)}$ y el sesgo $b^{(1)}_i$.
Aquí esa unidad es la neurona $i$ de la capa 1; la página 4 usa $h$ para otra cosa.
Las pendientes $\beta_h$ forman $\mathbf W^{(2)}$, de una sola fila, y $\beta_0$ es $b^{(2)}_1$.

::: exercise {#dl-ej-tamanos title="Da el tamaño de cada pieza"}
En la 2–3–2–1:

(a) ¿De qué tamaño son $\mathbf W^{(2)}$, $\mathbf W^{(3)}$ y $\mathbf b^{(2)}$?

(b) ¿Qué peso está en la fila 2, columna 3, de $\mathbf W^{(2)}$?
:::

::: hint {#dl-pista-tamanos-1 of="dl-ej-tamanos" title="Pista 1 · Llegan por salen"}
¿Cuántas neuronas tiene la capa a la que llegan las flechas, y cuántas la capa de la que salen?
:::

::: answer {#dl-resp-tamanos of="dl-ej-tamanos" title="Respuesta · Filas de la capa, columnas de la anterior"}
(a) $\mathbf W^{(2)}$ es de $2\times3$: llegan a 2 neuronas desde 3. $\mathbf W^{(3)}$ es de $1\times2$. $\mathbf b^{(2)}$ tiene 2 entradas, una por neurona de la capa 2.

(b) Es $w^{(2)}_{23}$: llega a la neurona 2 de la capa 2 desde la neurona 3 de la capa 1.
:::

## 4 · Reunir los símbolos y contar parámetros

**Piensa: si entrenar es elegir números, ¿cuántos números elige el entrenamiento de la 2–3–2–1?**

Todos los pesos y todos los sesgos: esos son los parámetros.
La entrada y las activaciones no se eligen; se calculan.

::: table {#dl-tab-simbolos title="Los símbolos de la red, con su tamaño"}
| Símbolo | Se lee | Qué es | Tamaño |
|---|---|---|---|
| $L$ | «ele» | El número de capas con parámetros | Un entero |
| $d_l$ | «de sub ele» | El ancho de la capa $l$ | Un entero |
| $\mathbf x=\mathbf a^{(0)}$ | «equis» | La entrada | $d_0$ |
| $\mathbf a^{(l)}$ | «a super ele» | Las activaciones de la capa $l$ | $d_l$ |
| $a^{(l)}_i$ | «a sub i super ele» | La activación de la neurona $i$ | Un número |
| $w^{(l)}_{ij}$ | «doble ve sub i jota» | El peso de $j$ (capa $l-1$) a $i$ (capa $l$) | Un número |
| $\mathbf W^{(l)}$ | «doble ve mayúscula» | Los pesos de la capa $l$ | $d_l\times d_{l-1}$ |
| $\mathbf b^{(l)}$ | «be super ele» | Los sesgos de la capa $l$ | $d_l$ |
| $\theta$ | «teta» | Todos los pesos y sesgos de la red | Todos los parámetros |
:::

$\theta=\bigl(\mathbf W^{(1)},\mathbf b^{(1)},\dots,\mathbf W^{(L)},\mathbf b^{(L)}\bigr)$ hace el papel que hacía $\beta$ en la unidad 9.
Esta $\theta$ no es el ángulo polar de los anillos.

La capa $l$ tiene $d_l\,d_{l-1}$ pesos y $d_l$ sesgos. En total, $d_l\,(d_{l-1}+1)$ parámetros.

::: table {#dl-tab-dimensiones title="La 2–3–2–1, capa por capa"}
| Capa $l$ | $d_l$ | $\mathbf W^{(l)}$ | $\mathbf b^{(l)}$ | Papel |
|---|---:|---|---|---|
| 0 | 2 | — | — | Entrada |
| 1 | 3 | $3\times2$ | 3 | Oculta |
| 2 | 2 | $2\times3$ | 2 | Oculta |
| 3 | 1 | $1\times2$ | 1 | Salida |
:::

::: exercise {#dl-ej-contar-parametros title="Cuenta los parámetros"}
(a) ¿Cuántos parámetros tiene la 2–3–2–1? Separa pesos y sesgos.

(b) La red del primer video de la tarea es 784–16–16–10. ¿Cuántos tiene?
:::

::: hint {#dl-pista-contar-parametros-1 of="dl-ej-contar-parametros" title="Pista 1 · Capa por capa"}
¿Cuántas entradas tiene cada $\mathbf W^{(l)}$ de la tabla, y cuántas cada $\mathbf b^{(l)}$?
:::

::: hint {#dl-pista-contar-parametros-2 of="dl-ej-contar-parametros" title="Pista 2 · Revisa la regla"}
¿Tu cuenta de cada capa coincide con $d_l\,(d_{l-1}+1)$? ¿Contaste la capa 0, que no tiene parámetros?
:::

::: answer {#dl-resp-contar-parametros of="dl-ej-contar-parametros" title="Respuesta · Veinte, y trece mil dos"}
(a) Por capa, $3\cdot3=9$, $2\cdot4=8$ y $1\cdot3=3$: son **20 parámetros**. Hay $6+6+2=14$ pesos y $3+2+1=6$ sesgos.

(b) Por capa, $16\cdot785=12\,560$, $16\cdot17=272$ y $10\cdot17=170$: son 13 002 parámetros, la cifra del video.
:::

**Punto de control:** deberías poder decir, sin mirar, de qué tamaño es $\mathbf W^{(l)}$ y qué significa su entrada $(i,j)$.

## Lo que hay que llevarse

- **Capas y anchos:** la capa 0 es la entrada; las capas 1 a $L$ tienen parámetros; $d_l$ es el ancho. El ejemplo es la 2–3–2–1, con $L=3$.
- **El peso se lee destino–origen:** $w^{(l)}_{ij}$ llega a la neurona $i$ de la capa $l$ desde la neurona $j$ de la capa $l-1$. Por ejemplo, $w^{(1)}_{12}=-0.2$ sale de $x_2$.
- **Una matriz por capa:** $\mathbf W^{(l)}\in\mathbb R^{d_l\times d_{l-1}}$, filas de destino y columnas de origen, más $\mathbf b^{(l)}\in\mathbb R^{d_l}$. La fila $i$ junta lo que llega a la neurona $i$.
- **$\theta$ son todos los parámetros:** $d_l\,(d_{l-1}+1)$ por capa; 20 en la 2–3–2–1, de ellos 14 pesos y 6 sesgos.

Continúa con [[dl-composicion|La red como composición de funciones]].
