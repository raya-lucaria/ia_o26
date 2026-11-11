---
id: dl-composicion
title: "La red como composición de funciones"
nav_title: "Composición"
summary: "El pase hacia adelante capa por capa, la red como composición de funciones f_θ, el pase a mano de la red 2–3–2–1 hasta ŷ = 0.546, por qué sin activación apilar capas no agrega nada, y tres activaciones: ReLU, sigmoide e identidad."
status: ready
estimated_time: 30m
tags: [deep-learning, redes-neuronales, pase-hacia-adelante, activacion]
prerequisites: [dl-la-red]
---

# La red como composición de funciones

**Con los pesos ya nombrados, ¿cómo convierte la red una entrada $\mathbf x$ en una predicción $\widehat{\mathbf y}$?**

Al terminar tendrás:

- **El pase hacia adelante:** $\mathbf z^{(l)}$ y $\mathbf a^{(l)}$, capa por capa.
- **Un pase a mano:** la 2–3–2–1 con $\mathbf x=(1,2)$ predice $\widehat y=0.546$.
- **La red como función:** $f_\theta=f^{(L)}\circ\cdots\circ f^{(1)}$.
- **Una demostración:** sin activación, la red entera es una sola capa afín.
- **Tres activaciones:** ReLU, sigmoide e identidad, y cuándo se usa cada una.

> **Lo que traes**
>
> $\mathbf W^{(l)}$ con filas de destino y columnas de origen, y $\mathbf b^{(l)}$ (@dl-def-matriz-pesos), en [[dl-la-red|La red]].
>
> La 2–3–2–1, capa por capa (@dl-tab-dimensiones).
>
> La sigmoide $\sigma(z)=1/(1+e^{-z})$ de [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]].

## 1 · Calcular una capa

**Piensa: la neurona $i$ de la capa $l$ ya tiene su fila de pesos y su sesgo. ¿Qué hace con lo que le llega?**

Dos cosas, en orden.
Primero suma lo que llega, ponderado por sus pesos, más su sesgo.
Después le aplica una función fija, la activación.
Al primer número se le llama preactivación; al segundo, activación.

::: definition {#dl-def-adelante title="El pase hacia adelante"}
Empieza con $\mathbf a^{(0)}=\mathbf x$. Para cada capa $l=1,\dots,L$, en orden:

$$
\begin{aligned}
\mathbf z^{(l)}&=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)},\\
\mathbf a^{(l)}&=g^{(l)}\bigl(\mathbf z^{(l)}\bigr).
\end{aligned}
$$

La predicción es la última activación: $\widehat{\mathbf y}=\mathbf a^{(L)}$.
Neurona por neurona, la capa $l$ calcula

$$
z^{(l)}_i=\sum_{j=1}^{d_{l-1}} w^{(l)}_{ij}\,a^{(l-1)}_j+b^{(l)}_i,\qquad a^{(l)}_i=g^{(l)}\bigl(z^{(l)}_i\bigr).
$$

- $\mathbf z^{(l)}\in\mathbb R^{d_l}$ es la **preactivación**; $\mathbf a^{(l)}\in\mathbb R^{d_l}$, la **activación**.
- $g^{(l)}$ es la **función de activación** de la capa $l$: una función $g:\mathbb R\to\mathbb R$ que se aplica entrada por entrada. Sobre el vector, $g^{(l)}:\mathbb R^{d_l}\to\mathbb R^{d_l}$, componente a componente.
:::

Las dimensiones cuadran: una matriz de $d_l\times d_{l-1}$ por un vector de $d_{l-1}$ da $d_l$ números, y se le suman $d_l$ sesgos.

La $z$ es el mismo puntaje de la logística de la unidad 9: lineal en lo que entra.
Allá, $z_i$ era el puntaje de la observación $i$; aquí $z^{(l)}_i$ es el de la neurona $i$.

**La activación se llama $g$, no $\sigma$.** En el curso, $\sigma$ es la sigmoide; aquí es solo una $g$ posible.
Tampoco es la $g(\beta)\le d$ de las restricciones de la unidad 9.

La 2–3–2–1 usa dos activaciones.
Las capas ocultas usan **ReLU**, $\operatorname{ReLU}(z)=\max(0,z)$: deja pasar lo positivo y vuelve cero lo negativo.
La salida usa la **identidad**, $g(z)=z$, porque predice un número cualquiera.

## 2 · Seguir la 2–3–2–1 a mano

**Piensa: con $\mathbf x=(1,2)$, ¿cuánto vale la primera neurona de la capa 1?**

Su fila de $\mathbf W^{(1)}$ es $(0.5,\ -0.2)$ y su sesgo es $0.1$.
Entonces $z^{(1)}_1=0.5\cdot1+(-0.2)\cdot2+0.1=0.2$, y $\operatorname{ReLU}(0.2)=0.2$.

La capa entera es el mismo cálculo con las tres filas:

$$
\mathbf z^{(1)}=
\begin{array}{c|cc}
 & j=1 & j=2\\ \hline
i=1 & 0.5 & -0.2\\
i=2 & -0.4 & 0.1\\
i=3 & 0.3 & 0.2
\end{array}
\begin{pmatrix}1\\2\end{pmatrix}
+\begin{pmatrix}0.1\\0\\-0.1\end{pmatrix}
=\begin{pmatrix}0.2\\-0.2\\0.6\end{pmatrix},
\qquad
\mathbf a^{(1)}=\begin{pmatrix}0.2\\0\\0.6\end{pmatrix}.
$$

La neurona 2 recibe $z^{(1)}_2=-0.4\cdot1+0.1\cdot2+0=-0.2$, que es negativo.
ReLU la deja en 0: con esta $\mathbf x$, la neurona 2 está **apagada** y no aporta nada a la capa 2.

::: exercise {#dl-ej-adelante title="Termina el pase"}
**Estamos aquí:** $\mathbf a^{(1)}=(0.2,\ 0,\ 0.6)$. Las capas 2 y 3 tienen

$$
\mathbf W^{(2)}=
\begin{array}{c|ccc}
 & j=1 & j=2 & j=3\\ \hline
i=1 & 0.4 & -0.3 & 0.5\\
i=2 & 0.2 & 0.6 & -0.1
\end{array}
\qquad
\mathbf W^{(3)}=
\begin{array}{c|cc}
 & j=1 & j=2\\ \hline
i=1 & 0.7 & -0.5
\end{array}
$$

con $\mathbf b^{(2)}=(0.1,\ 0.2)$ y $\mathbf b^{(3)}=(0.3)$. La capa 2 usa ReLU; la 3, la identidad.

(a) Calcula $\mathbf z^{(2)}$ y $\mathbf a^{(2)}$.

(b) Calcula $\widehat y=a^{(3)}_1$.
:::

::: hint {#dl-pista-adelante-1 of="dl-ej-adelante" title="Pista 1 · Una fila a la vez"}
¿Qué fila de $\mathbf W^{(2)}$ multiplica a $\mathbf a^{(1)}$ para dar $z^{(2)}_1$? ¿Qué término de esa suma se anula por la neurona apagada?
:::

::: answer {#dl-resp-adelante of="dl-ej-adelante" title="Respuesta · La red predice 0.546"}
(a) $z^{(2)}_1=0.4\cdot0.2-0.3\cdot0+0.5\cdot0.6+0.1=0.48$ y $z^{(2)}_2=0.2\cdot0.2+0.6\cdot0-0.1\cdot0.6+0.2=0.18$.
Los dos son positivos, así que $\mathbf a^{(2)}=\mathbf z^{(2)}=(0.48,\ 0.18)$.

(b) $z^{(3)}_1=0.7\cdot0.48-0.5\cdot0.18+0.3=0.546$. Con la identidad, $\widehat y=0.546$.
:::

::: table {#dl-tab-pase title="El pase hacia adelante de la 2–3–2–1 con x = (1, 2)"}
| Capa $l$ | $\mathbf z^{(l)}$ | $g^{(l)}$ | $\mathbf a^{(l)}$ |
|---|---|---|---|
| 0 | — | — | $(1,\ 2)$ |
| 1 | $(0.2,\ -0.2,\ 0.6)$ | ReLU | $(0.2,\ 0,\ 0.6)$ |
| 2 | $(0.48,\ 0.18)$ | ReLU | $(0.48,\ 0.18)$ |
| 3 | $(0.546)$ | identidad | $(0.546)$ |
:::

Cada capa solo necesita la activación de la anterior.
Por eso el cálculo va en un solo sentido, de la entrada a la salida: hacia adelante.

## 3 · Ver la red como una composición

**Piensa: si cada capa recibe un vector y devuelve otro, ¿qué es la red entera?**

Una función que aplica las capas una tras otra: una composición.
Cada capa es una función con sus propios parámetros.

::: definition {#dl-def-composicion title="La capa como función y la red como composición"}
La capa $l$ es la función $f^{(l)}:\mathbb R^{d_{l-1}}\to\mathbb R^{d_l}$,

$$
f^{(l)}(\mathbf u)=g^{(l)}\bigl(\mathbf W^{(l)}\mathbf u+\mathbf b^{(l)}\bigr).
$$

La red es la composición de sus $L$ capas, $f_\theta:\mathbb R^{d_0}\to\mathbb R^{d_L}$:

$$
f_\theta=f^{(L)}\circ\cdots\circ f^{(2)}\circ f^{(1)},\qquad \widehat{\mathbf y}=f_\theta(\mathbf x).
$$

$\theta$ reúne los parámetros de todas las capas, como en @dl-tab-simbolos.
:::

La composición se lee de derecha a izquierda: primero actúa $f^{(1)}$.
Para la 2–3–2–1, $\widehat y=f^{(3)}\bigl(f^{(2)}\bigl(f^{(1)}(\mathbf x)\bigr)\bigr)=0.546$.

::: figure {#dl-composicion title="La red es una cadena de capas"}
![La red como una cadena de funciones: x entra a f⁽¹⁾ y sale a⁽¹⁾; a⁽¹⁾ entra a f⁽²⁾ y sale a⁽²⁾; a⁽²⁾ entra a f⁽³⁾ y sale ŷ; ŷ y la respuesta y entran a la pérdida ℓ. A cada caja f⁽ˡ⁾ le entran sus parámetros W⁽ˡ⁾ y b⁽ˡ⁾. Debajo de cada vector, su espacio: x en ℝ², a⁽¹⁾ en ℝ³, a⁽²⁾ en ℝ² y ŷ en ℝ¹; g⁽¹⁾ y g⁽²⁾ son ReLU y g⁽³⁾ la identidad. Abajo, ŷ = f⁽³⁾(f⁽²⁾(f⁽¹⁾(x))) = f_θ(x), con f⁽ˡ⁾(u) = g⁽ˡ⁾(W⁽ˡ⁾u + b⁽ˡ⁾).](../_assets/dl-composicion.svg)
:::

En la figura, cada caja recibe dos cosas: la activación de la izquierda y sus parámetros.
Debajo de cada flecha está el tamaño del vector que pasa: 2, 3, 2 y 1, los anchos de la red.
La última caja, $\ell$, compara $\widehat y$ con la respuesta $y$: es la pérdida que presenta la página 3.

$f_\theta$ hace el papel de $f_\beta$ en la unidad 9, con una diferencia importante.
Allá el modelo era lineal en $\beta$ (@ml-c1-def-modelo-lineal).
Aquí $\mathbf W^{(1)}$ queda dentro de $g^{(1)}$, y lo que sale se multiplica por $\mathbf W^{(2)}$: la red **no es lineal en $\theta$**.

::: exercise {#dl-ej-composicion title="Escribe la composición"}
Una red 3–4–1 tiene una capa oculta con ReLU y salida identidad.

(a) Escribe $\widehat y$ como composición, con el dominio y el codominio de cada $f^{(l)}$.

(b) Escribe $\widehat y$ en una sola fórmula con $\mathbf W^{(1)}$, $\mathbf b^{(1)}$, $\mathbf W^{(2)}$ y $\mathbf b^{(2)}$.
:::

::: hint {#dl-pista-composicion-1 of="dl-ej-composicion" title="Pista 1 · De adentro hacia afuera"}
¿Qué función actúa primero sobre $\mathbf x$, y de qué tamaño es lo que devuelve?
:::

::: answer {#dl-resp-composicion of="dl-ej-composicion" title="Respuesta · Dos capas, una dentro de la otra"}
(a) $\widehat y=f^{(2)}\bigl(f^{(1)}(\mathbf x)\bigr)$, con $f^{(1)}:\mathbb R^3\to\mathbb R^4$ y $f^{(2)}:\mathbb R^4\to\mathbb R$.

(b) $\widehat y=\mathbf W^{(2)}\operatorname{ReLU}\bigl(\mathbf W^{(1)}\mathbf x+\mathbf b^{(1)}\bigr)+\mathbf b^{(2)}$, con $\mathbf W^{(1)}$ de $4\times3$ y $\mathbf W^{(2)}$ de $1\times4$.
:::

## 4 · Entender por qué hace falta la activación

**Piensa: si todas las $g^{(l)}$ fueran la identidad, ¿ganaría algo la red con cada capa nueva?**

Nada. Dos capas afines seguidas son otra capa afín, así que apilarlas no agrega capacidad.

::: remark {#dl-obs-sin-activacion title="Sin activación, la red es una sola capa afín"}
Con $g^{(1)}$ y $g^{(2)}$ la identidad,

$$
\begin{aligned}
f^{(2)}\bigl(f^{(1)}(\mathbf u)\bigr)&=\mathbf W^{(2)}\bigl(\mathbf W^{(1)}\mathbf u+\mathbf b^{(1)}\bigr)+\mathbf b^{(2)}\\
&=\underbrace{\mathbf W^{(2)}\mathbf W^{(1)}}_{d_2\times d_0}\,\mathbf u+\underbrace{\mathbf W^{(2)}\mathbf b^{(1)}+\mathbf b^{(2)}}_{d_2}.
\end{aligned}
$$

Es una capa afín con matriz $\mathbf W^{(2)}\mathbf W^{(1)}$ y sesgo $\mathbf W^{(2)}\mathbf b^{(1)}+\mathbf b^{(2)}$.
Repitiendo el argumento capa por capa, la red entera es $\mathbf W'\mathbf x+\mathbf b'$, con $\mathbf W'=\mathbf W^{(L)}\cdots\mathbf W^{(1)}$, de $d_L\times d_0$.

- **Filas:** una por neurona $i$ de la capa $L$.
- **Columnas:** una por entrada $x_j$.
- **Entrada $(i,j)$:** $w'_{ij}$.
:::

En la 2–3–2–1 sin activaciones, $\mathbf W'$ sería de $1\times2$.
La red predeciría $w'_{11}x_1+w'_{12}x_2+b'_1$: una regresión lineal con 3 parámetros, aunque $\theta$ tenga 20.

La activación es lo que rompe ese colapso.
Con ReLU, cada neurona se prende o se apaga según la $\mathbf x$, como la neurona 2 de la capa 1 en la sección 2.
Cada patrón de neuronas prendidas da una pieza afín distinta: la red es afín **por pedazos**.

> [!WARNING]
> Lectura equivocada: «Más capas siempre dan una red más flexible».
>
> Lectura correcta: **Más capas dan más flexibilidad solo si entre ellas hay una activación no lineal.**

::: exercise {#dl-ej-colapso title="Colapsa una red sin activaciones"}
Una red 5–8–8–3 usa la identidad en todas sus capas.

(a) ¿De qué tamaño es la matriz $\mathbf W'$ a la que se reduce?

(b) ¿Cuántos parámetros tiene $\theta$, y cuántos tiene el modelo colapsado?
:::

::: hint {#dl-pista-colapso-1 of="dl-ej-colapso" title="Pista 1 · Solo cuentan los extremos"}
En el producto $\mathbf W^{(3)}\mathbf W^{(2)}\mathbf W^{(1)}$, ¿qué tamaño da filas y cuál da columnas?
:::

::: answer {#dl-resp-colapso of="dl-ej-colapso" title="Respuesta · Las capas de en medio desaparecen"}
(a) $\mathbf W'$ es de $3\times5$: filas de la salida, columnas de la entrada.

(b) $\theta$ tiene $8\cdot6+8\cdot9+3\cdot9=48+72+27=147$ parámetros.
El modelo colapsado tiene $3\cdot5$ pesos y 3 sesgos: 18. Los 147 solo describen esas 18 cifras de muchas maneras.
:::

## 5 · Elegir la activación

**Piensa: si la salida es una probabilidad, ¿sirve la identidad en la última capa?**

No: la identidad puede devolver $-3$ o $1.7$, y una probabilidad vive entre 0 y 1.
La activación de la salida se elige por lo que se predice; la de las capas ocultas, por cómo entrena.

::: table {#dl-tab-activaciones title="Tres activaciones y dónde se usan"}
| $g$ | Fórmula | Valores | Uso típico |
|---|---|---|---|
| ReLU | $\max(0,z)$ | $[0,\infty)$ | Capas ocultas |
| Sigmoide $\sigma$ | $1/(1+e^{-z})$ | $(0,1)$ | Salida de clasificación binaria |
| Identidad | $z$ | Todo $\mathbb R$ | Salida de regresión |
:::

La sigmoide es la de la logística de la unidad 9.
La red de una capa de @ml-c5-teo-cybenko la usaba también en la capa oculta; hoy se prefiere ReLU, porque entrena más rápido en redes profundas.

> [!WARNING]
> Lectura equivocada: «$g$ es la sigmoide».
>
> Lectura correcta: **$g^{(l)}$ es la activación de la capa $l$, la que sea; la sigmoide $\sigma$ es solo una opción.**

::: exercise {#dl-ej-elegir-activacion title="Elige la activación de la salida"}
Elige $g^{(L)}$ en cada caso.

(a) Predecir la temperatura de mañana, en °C.

(b) Predecir la probabilidad de que llueva.

(c) ¿Qué falla si usas ReLU en la salida de (a)?
:::

::: hint {#dl-pista-elegir-activacion-1 of="dl-ej-elegir-activacion" title="Pista 1 · Mira los valores posibles"}
¿Qué valores puede tomar lo que predices, y qué columna de @dl-tab-activaciones los cubre?
:::

::: answer {#dl-resp-elegir-activacion of="dl-ej-elegir-activacion" title="Respuesta · La salida manda"}
(a) La identidad: una temperatura puede ser cualquier número real.

(b) La sigmoide: devuelve un número en $(0,1)$.

(c) ReLU nunca devuelve negativos. La red no podría predecir $-5$ °C.
:::

**Punto de control:** deberías poder hacer a mano el pase hacia adelante de una red pequeña y decir qué pasa si quitas las activaciones.

## Lo que hay que llevarse

- **Una capa calcula dos cosas:** $\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$ y $\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$, desde $\mathbf a^{(0)}=\mathbf x$ hasta $\widehat{\mathbf y}=\mathbf a^{(L)}$.
- **El pase de la 2–3–2–1 con $\mathbf x=(1,2)$:** $\mathbf z^{(1)}=(0.2,-0.2,0.6)$ y $\mathbf a^{(1)}=(0.2,0,0.6)$, con la neurona 2 apagada; $\mathbf a^{(2)}=(0.48,0.18)$; $\widehat y=0.546$.
- **La red es una composición:** $f_\theta=f^{(L)}\circ\cdots\circ f^{(1)}$ con $f^{(l)}(\mathbf u)=g^{(l)}(\mathbf W^{(l)}\mathbf u+\mathbf b^{(l)})$. No es lineal en $\theta$.
- **Sin activación no hay profundidad:** las capas afines se colapsan en $\mathbf W'\mathbf x+\mathbf b'$; la 2–3–2–1 quedaría en 3 parámetros efectivos.
- **$g$ no es $\sigma$:** ReLU en las ocultas; identidad o sigmoide en la salida, según lo que se predice.

Continúa con [[dl-perdida-lagrangeano|La pérdida y el lagrangeano]].
