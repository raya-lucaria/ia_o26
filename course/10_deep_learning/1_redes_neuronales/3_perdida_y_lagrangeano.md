---
id: dl-perdida-lagrangeano
title: "La pérdida y el lagrangeano"
nav_title: "Pérdida y lagrangeano"
summary: "Cómo se mide el error de la red y qué significa entrenarla: la pérdida de una observación, su promedio L(θ), MSE y RMSE, entrenar como minimizar, y el lagrangeano con la capacidad de ridge, que en una red se llama decaimiento de pesos."
status: ready
estimated_time: 25m
tags: [deep-learning, redes-neuronales, perdida, lagrangeano, ridge]
prerequisites: [dl-composicion]
---

# La pérdida y el lagrangeano

**La red ya predice. ¿Cómo medimos qué tan mal lo hace, y qué significa entrenarla?**

Al terminar tendrás:

- **Dos pérdidas:** $\ell$ de una observación y su promedio $L(\theta)$; en el ejemplo, $\ell=0.206$.
- **Las cifras que se reportan:** MSE y RMSE de una red de regresión.
- **Una definición de entrenar:** elegir $\theta$ que minimice $L(\theta)$.
- **Un lagrangeano:** $\mathcal L(\theta,\mu)=L(\theta)+\mu\,(\Omega(\theta)-d)$, con la $\Omega$ de ridge, y por qué se llama decaimiento de pesos.

> **Lo que traes**
>
> El pase hacia adelante (@dl-def-adelante) y $\widehat y=0.546$ en la 2–3–2–1, en [[dl-composicion|La red como composición]].
>
> La pérdida promedio en un conjunto (@ml-c1-def-perdida-en-conjunto) y el lagrangeano de la capacidad (@ml-c3-def-lagrangeano-capacidad), de la unidad 9.

## 1 · Medir el error de una observación

**Piensa: para $\mathbf x=(1,2)$ la red predice $\widehat y=0.546$, y la respuesta observada es $y=1$. ¿Cuánto se equivocó?**

Por $0.546-1=-0.454$: se quedó corta.
Para no distinguir errores por arriba y por abajo, se eleva al cuadrado: $(-0.454)^2\approx0.206$.

Los datos son $n$ pares $(\mathbf x_k,\mathbf y_k)$, con $k=1,\dots,n$.
**La observación se indexa con $k$**, porque $i$ y $j$ ya son neuronas.
En la unidad 9, $k$ era el número de pliegues; aquí no hay pliegues.

::: definition {#dl-def-perdida title="Pérdida de una observación y pérdida promedio"}
La **pérdida** $\ell(\widehat{\mathbf y},\mathbf y)\ge0$ mide qué tan lejos queda la predicción de la respuesta. Para regresión,

$$
\ell(\widehat{\mathbf y},\mathbf y)=\sum_{i=1}^{d_L}\bigl(\widehat y_i-y_i\bigr)^2,
$$

que con una sola salida es $(\widehat y-y)^2$. La **pérdida promedio** de la red en sus $n$ observaciones es

$$
L(\theta)=\frac1n\sum_{k=1}^{n}\ell\bigl(f_\theta(\mathbf x_k),\mathbf y_k\bigr).
$$

Con la pérdida cuadrática, $L$ es el $\mathrm{MSE}$, y se reporta $\mathrm{RMSE}=\sqrt{\mathrm{MSE}}$, en las unidades de $y$.
:::

Es la misma $\ell$ cuadrática de la unidad 9, que se escribía $(y-\widehat y)^2$; el cuadrado no depende del orden.
Va sin el $\tfrac12$ que ponen algunos textos.

**$L$ tiene dos papeles.** Como superíndice o tope del índice de capa, $f^{(L)}$ o $l=1,\dots,L$, es el número de capas; en cualquier otro lugar, $L(\theta)$ es la pérdida promedio.
$L(\theta)$ se calcula con el conjunto de entrenamiento: es la $L_{\text{ent}}$ de la unidad 9.
La misma fórmula, en el conjunto de validación, mide lo que importa.

Con la única observación del ejemplo, $\mathrm{MSE}=\ell=0.206$ y $\mathrm{RMSE}=\lvert\widehat y-y\rvert=0.454$.

::: exercise {#dl-ej-mse title="Calcula MSE y RMSE"}
Una red de una salida ve dos observaciones, $k=1,2$.
Escribe $\widehat y_k$ y $y_k$ para la predicción y la respuesta de la observación $k$, y $\ell_k=(\widehat y_k-y_k)^2$ para su pérdida.
Con una sola salida, el subíndice de $\widehat y_k$ es la observación, no la componente $i$ de arriba.
La red predice $\widehat y_1=3$ y $\widehat y_2=5$; las respuestas son $y_1=2$ y $y_2=5$.

(a) ¿Cuánto valen $\ell_1$, $\ell_2$ y $L$?

(b) ¿Cuánto vale el RMSE?
:::

::: hint {#dl-pista-mse-1 of="dl-ej-mse" title="Pista 1 · Primero cada una"}
¿Cuál es el error de cada observación antes de elevarlo al cuadrado? ¿Entre cuánto divides la suma?
:::

::: answer {#dl-resp-mse of="dl-ej-mse" title="Respuesta · Un error de 1 en dos observaciones"}
(a) $\ell_1=(3-2)^2=1$ y $\ell_2=(5-5)^2=0$. Entonces $L=(1+0)/2=0.5$.

(b) $\mathrm{RMSE}=\sqrt{0.5}\approx0.707$.
:::

## 2 · Entrenar es minimizar

**Piensa: si los datos y la arquitectura están fijos, ¿qué puede cambiar para que $L$ baje?**

Solo $\theta$: los pesos y los sesgos.
Entrenar la red es buscar los $\theta$ con la menor pérdida promedio:

$$
\widehat\theta\in\operatorname*{arg\,min}_{\theta}\ L(\theta).
$$

Lleva gorro por la misma razón que $\widehat\beta$ en la unidad 9: depende de la muestra.

La diferencia con la unidad 9 está en cómo se busca.
Allá, con $\beta$ lineal, mínimos cuadrados tenía fórmula cerrada.
Aquí $f_\theta$ no es lineal en $\theta$, y $L$ en general no es convexa: puede tener varios mínimos.

Así que no se despeja $\widehat\theta$: se busca bajando por la pendiente de $L$.
Esa pendiente es el gradiente $\nabla_\theta L$, el vector con la derivada de $L$ respecto a cada parámetro.
En la 2–3–2–1 tiene 20 entradas.

Aquí lo dejamos indicado.
Cómo se calcula es la [[dl-retropropagacion|retropropagación]]; cómo se usa para bajar, [[dl-entrenar|el descenso de gradiente]].

::: exercise {#dl-ej-lineal-en-theta title="Encuentra dónde la red es lineal"}
Fija todas las capas de la 2–3–2–1 menos la última, cuya activación es la identidad.

(a) ¿Es $\widehat y$ lineal en $\mathbf W^{(3)}$ y $\mathbf b^{(3)}$?

(b) ¿Es lineal en $\mathbf W^{(1)}$?
:::

::: hint {#dl-pista-lineal-en-theta-1 of="dl-ej-lineal-en-theta" title="Pista 1 · Mira qué se calcula antes"}
Con las capas 1 y 2 fijas, ¿se puede calcular $\mathbf a^{(2)}$ sin conocer $\mathbf W^{(3)}$? ¿Y $\mathbf a^{(1)}$ sin conocer $\mathbf W^{(1)}$?
:::

::: answer {#dl-resp-lineal-en-theta of="dl-ej-lineal-en-theta" title="Respuesta · Lineal al final, no al principio"}
(a) Sí. $\widehat y=\mathbf W^{(3)}\mathbf a^{(2)}+\mathbf b^{(3)}$, y $\mathbf a^{(2)}$ ya está calculado: es un modelo lineal con $\phi(\mathbf x)=\mathbf a^{(2)}$.
Es lo que dijo la unidad 9: la red es una regresión lineal sobre variables aprendidas.

(b) No. $\mathbf W^{(1)}$ queda dentro de ReLU, y lo que sale se multiplica por $\mathbf W^{(2)}$ y $\mathbf W^{(3)}$.
:::

## 3 · Restringir la capacidad con un lagrangeano

**Piensa: con muchos parámetros y pocos datos, ¿qué hace minimizar $L$ sin ningún freno?**

Persigue cada punto, ruido incluido: baja $L$ en entrenamiento y sube el error en datos nuevos.
Es el sobreajuste de la unidad 9, y se trata igual: con una restricción sobre la capacidad.

::: definition {#dl-def-lagrangeano-red title="El lagrangeano de la red"}
Entrenar con capacidad limitada es resolver

$$
\min_\theta\ L(\theta)\quad\text{s.a.}\quad\Omega(\theta)\le d,
$$

cuyo lagrangeano, con el multiplicador $\mu\ge0$, es

$$
\mathcal L(\theta,\mu)=L(\theta)+\mu\,\bigl(\Omega(\theta)-d\bigr).
$$

Con $\mu$ fijo, el término $-\mu d$ no depende de $\theta$: se minimiza $L(\theta)+\mu\,\Omega(\theta)$.
La $\Omega$ más usada es la de **ridge**, la suma de los cuadrados de todos los pesos:

$$
\Omega(\theta)=\sum_{l=1}^{L}\lVert\mathbf W^{(l)}\rVert_F^2=\sum_{l=1}^{L}\sum_{i=1}^{d_l}\sum_{j=1}^{d_{l-1}}\bigl(w^{(l)}_{ij}\bigr)^2 .
$$

Los sesgos no se penalizan, igual que el intercepto $\beta_0$. Otras $\Omega$, como la de lasso, entran igual.
:::

$\lVert\mathbf W\rVert_F^2$, la norma de Frobenius al cuadrado, es la suma de los cuadrados de las entradas de la matriz.
Es la versión para matrices de $\lVert\beta\rVert_2^2$.
En la 2–3–2–1, $\Omega$ suma los cuadrados de sus 14 pesos; el ejercicio de esta sección la calcula.

Tres avisos de letras:

- **$\mathcal L$ es el lagrangeano,** no la pérdida. Algunos textos llaman $\mathcal L$ o $J$ a la pérdida; aquí es $L$.
- **$d$ sola es la cota de $\Omega$;** con subíndice, $d_l$ es el ancho de una capa.
- **$\mu$ es el multiplicador de la unidad 9,** con $\mu\ge0$. Los libros lo escriben con lambda.

¿Por qué se llama **decaimiento de pesos** (*weight decay*)?
El término de ridge suma al gradiente de cada matriz

$$
\nabla_{\mathbf W^{(l)}}\bigl(\mu\,\Omega\bigr)=2\mu\,\mathbf W^{(l)} .
$$

Bajar por el gradiente resta un múltiplo de $\mathbf W^{(l)}$ en cada paso.
Cada peso se encoge hacia cero, en proporción a su tamaño: decae.
El resto del gradiente, $\nabla_\theta L$, no cambia; la página 4 lo calcula.

::: exercise {#dl-ej-penalizacion title="Calcula la penalización"}
Usa las matrices de la 2–3–2–1: $\mathbf W^{(1)}$ de [[dl-la-red|La red]], y $\mathbf W^{(2)}$ y $\mathbf W^{(3)}$ del ejercicio «Termina el pase» de [[dl-composicion|La composición]].

(a) Calcula $\lVert\mathbf W^{(1)}\rVert_F^2$, $\lVert\mathbf W^{(2)}\rVert_F^2$, $\lVert\mathbf W^{(3)}\rVert_F^2$ y $\Omega(\theta)$.

(b) Con $\mu=0.01$, ¿cuánto suma el término $\mu\,\Omega(\theta)$?

(c) ¿Cuántos de los 20 parámetros no entran en $\Omega$, y cuáles son?
:::

::: hint {#dl-pista-penalizacion-1 of="dl-ej-penalizacion" title="Pista 1 · Una matriz a la vez"}
¿Cuántas entradas tiene cada $\mathbf W^{(l)}$? Eleva cada una al cuadrado y suma; ¿qué parte de $\theta$ no aparece en la definición de $\Omega$?
:::

::: answer {#dl-resp-penalizacion of="dl-ej-penalizacion" title="Respuesta · Solo cuentan los pesos"}
(a) $\lVert\mathbf W^{(1)}\rVert_F^2=0.25+0.04+0.16+0.01+0.09+0.04=0.59$.
$\lVert\mathbf W^{(2)}\rVert_F^2=0.16+0.09+0.25+0.04+0.36+0.01=0.91$.
$\lVert\mathbf W^{(3)}\rVert_F^2=0.49+0.25=0.74$.
Entonces $\Omega=0.59+0.91+0.74=2.24$.

(b) $\mu\,\Omega=0.01\cdot2.24=0.0224$.

(c) Seis: los sesgos $\mathbf b^{(1)}$, $\mathbf b^{(2)}$ y $\mathbf b^{(3)}$, con 3, 2 y 1 entradas.
:::

## 4 · Reconocer el lagrangeano de la unidad 9

**Piensa: ¿hay algo en este lagrangeano que no hayas visto ya?**

Casi nada: cambian los nombres, y la manera de minimizar.

::: table {#dl-tab-unidad-9 title="Del lagrangeano de la unidad 9 al de la red"}
| Pieza | Unidad 9 | Red |
|---|---|---|
| Parámetros | $\beta$ | $\theta$: pesos y sesgos |
| Modelo | $f_\beta$, lineal en $\beta$ | $f_\theta$, composición de capas |
| Pérdida que se minimiza | $L_{\text{ent}}(\beta)$ | $L(\theta)$ |
| Capacidad de ridge | $\sum_{j\ge1}\beta_j^2$ | $\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$ |
| Lo que no se penaliza | El intercepto $\beta_0$ | Los sesgos |
| Cómo se minimiza | Fórmula cerrada (mínimos cuadrados, ridge) | Descenso de gradiente |
:::

Lo demás se queda igual.
$\mu$ es un hiperparámetro (@ml-c1-def-param-hiper): no se elige minimizando $L$, sino con datos de validación.
$\mu$ grande equivale a $d$ chica, y a poca capacidad.
Todo eso está en [[ml-lagrangeano-en-accion|El lagrangeano en acción]]; la página 5 lo ve en las curvas de RMSE de una red.

**Punto de control:** deberías poder escribir $\mathcal L(\theta,\mu)$ de una red, decir qué parámetros entran en $\Omega$ y explicar por qué ridge encoge los pesos.

## Lo que hay que llevarse

- **Pérdida de una observación:** $\ell(\widehat{\mathbf y},\mathbf y)=\sum_i(\widehat y_i-y_i)^2$. En el ejemplo, $\widehat y=0.546$ contra $y=1$ da $\ell=0.206$.
- **Pérdida promedio:** $L(\theta)=\frac1n\sum_k\ell(f_\theta(\mathbf x_k),\mathbf y_k)$, con $k$ para las observaciones. Es el MSE; se reporta $\mathrm{RMSE}=\sqrt{\mathrm{MSE}}$, que en el ejemplo es 0.454.
- **Entrenar es minimizar:** $\widehat\theta\in\operatorname*{arg\,min}_\theta L(\theta)$. Sin fórmula cerrada: se baja con $\nabla_\theta L$.
- **El lagrangeano:** $\mathcal L(\theta,\mu)=L(\theta)+\mu\,(\Omega(\theta)-d)$, $\mu\ge0$. Con ridge, $\Omega$ suma los cuadrados de los pesos, sin sesgos: 2.24 en el ejemplo.
- **Decaimiento de pesos:** ridge suma $2\mu\,\mathbf W^{(l)}$ al gradiente, y cada paso encoge los pesos hacia cero.

Continúa con [[dl-retropropagacion|La retropropagación]].
