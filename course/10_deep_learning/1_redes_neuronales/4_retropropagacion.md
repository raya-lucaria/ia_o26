---
id: dl-retropropagacion
title: "Retropropagación: la regla de la cadena hacia atrás"
nav_title: "Retropropagación"
summary: "La regla de la cadena con jacobianas, el error δ de cada capa, los gradientes de pesos y sesgos como error del destino por activación del origen, la red 2–3–2–1 retropropagada a mano y su comprobación por diferencias finitas."
status: ready
estimated_time: 50m
tags: [deep-learning, retropropagacion, regla-de-la-cadena, gradiente, jacobiana]
prerequisites: [dl-perdida-lagrangeano]
---

# Retropropagación: la regla de la cadena hacia atrás

**Un peso de la capa 1 está a tres capas de la pérdida. ¿Cómo sabes cuánto cambia la pérdida si lo mueves un poco?**

Al terminar tendrás:

- **La operación fundamental:** pasar un gradiente hacia atrás es multiplicar por una jacobiana traspuesta.
- **El error de cada capa:** $\mathbf{δ}^{(l)}$, con su fórmula de salida y su fórmula de ocultas.
- **Los gradientes:** cada peso recibe el error del destino por la activación del origen.
- **El ejemplo a mano:** la red 2–3–2–1 retropropagada, de $\delta^{(3)}=-0.908$ hasta $\nabla_{\mathbf W^{(1)}}\ell$.
- **Una comprobación:** las diferencias finitas confirman cada número.

> **Lo que traes**
>
> De [[dl-la-red|la red]]: $w^{(l)}_{ij}$ va de la neurona $j$ de la capa $l-1$ (origen) a la neurona $i$ de la capa $l$ (destino), y $\mathbf W^{(l)}$ es de $d_l\times d_{l-1}$.
>
> De [[dl-composicion|la composición]]: $\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$, $\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$, $\mathbf a^{(0)}=\mathbf x$.
>
> De [[dl-perdida-lagrangeano|la pérdida y el lagrangeano]]: $\ell=(\widehat y-y)^2$ por observación, su promedio $L(\theta)$ y $\mathcal L(\theta,\mu)=L(\theta)+\mu(\Omega(\theta)-d)$.
>
> **El hilo, en cuatro líneas.** Red 2–3–2–1: ocultas ReLU, salida identidad.
> Una observación: $\mathbf x=(1,\ 2)$, $y=1$.
> El pase hacia adelante dio $\mathbf z^{(1)}=(0.2,\ -0.2,\ 0.6)$, $\mathbf a^{(1)}=(0.2,\ 0,\ 0.6)$ y $\mathbf a^{(2)}=(0.48,\ 0.18)$.
> La salida es $\widehat y=0.546$ y la pérdida, $\ell=0.206$.

## 1 · Plantear qué hay que derivar

**Piensa: ¿cuántas derivadas necesitas para mover todos los parámetros de la red del hilo?**

Una por parámetro. $\mathbf W^{(1)}$ tiene 6 pesos, $\mathbf W^{(2)}$ 6 y $\mathbf W^{(3)}$ 2; los sesgos suman 3, 2 y 1.
En total son 20 derivadas parciales.

Basta derivar la pérdida de **una** observación.
$L(\theta)$ es un promedio de las $\ell$, así que su gradiente es el promedio de los gradientes.
El lagrangeano solo agrega $\mu\nabla_\theta\Omega$, que se suma al final (sección 4).

> **Dado:** la red, una observación $(\mathbf x,y)$ y el pase hacia adelante con todos sus $\mathbf z^{(l)}$ y $\mathbf a^{(l)}$ guardados.
>
> **Encontrar:** $\partial\ell/\partial w^{(l)}_{ij}$ y $\partial\ell/\partial b^{(l)}_i$ para toda capa $l$, todo destino $i$ y todo origen $j$.

Podrías mover cada parámetro un poco y volver a correr la red: 20 parámetros, 20 pases o más.
Una red real tiene millones.
La retropropagación las saca todas con **un pase hacia adelante y uno hacia atrás**.
El truco es la regla de la cadena, escrita con matrices.

## 2 · Encadenar derivadas con matrices

**Piensa: si $\mathbf u$ cambia a $\mathbf v$ y $\mathbf v$ cambia a $\mathbf s$, ¿cómo se combinan las dos sensibilidades?**

Multiplicando matrices. Cada sensibilidad es una jacobiana.
En esta sección, $\mathbf u$, $\mathbf v$ y $\mathbf s$ son tres vectores cualesquiera en cadena, y $\dim\mathbf u$ es el número de componentes de $\mathbf u$.

::: definition {#dl-def-jacobiana title="Jacobiana"}
Si $\mathbf v$ depende de $\mathbf u$, su jacobiana $\partial\mathbf v/\partial\mathbf u$ es la matriz de $\dim\mathbf v\times\dim\mathbf u$ con todas las derivadas parciales.
La fila $i$ es la componente $v_i$ de la salida; la columna $j$, la componente $u_j$ de la entrada:

$$
\frac{\partial\mathbf v}{\partial\mathbf u}=
\begin{array}{c|ccc}
 & u_1 & \cdots & u_{\dim\mathbf u}\\\hline
v_1 & \partial v_1/\partial u_1 & \cdots & \partial v_1/\partial u_{\dim\mathbf u}\\
\vdots & \vdots & & \vdots\\
v_{\dim\mathbf v} & \partial v_{\dim\mathbf v}/\partial u_1 & \cdots & \partial v_{\dim\mathbf v}/\partial u_{\dim\mathbf u}
\end{array}
$$

La entrada $(i,j)$ dice cuánto se mueve $v_i$ por unidad de $u_j$.
:::

Es la misma convención que $\mathbf W^{(l)}$: filas = destino $i$, columnas = origen $j$.

Si $\mathbf s$ depende de $\mathbf v$ y $\mathbf v$ de $\mathbf u$, la regla de la cadena es un producto de jacobianas:

$$
\frac{\partial\mathbf s}{\partial\mathbf u}=\frac{\partial\mathbf s}{\partial\mathbf v}\,\frac{\partial\mathbf v}{\partial\mathbf u},
\qquad (\dim\mathbf s\times\dim\mathbf v)(\dim\mathbf v\times\dim\mathbf u)=\dim\mathbf s\times\dim\mathbf u .
$$

Al final de la cadena siempre está $\ell$, un número.
Su gradiente $\nabla_{\mathbf u}\ell$ es la **columna** de $\dim\mathbf u$ entradas $\partial\ell/\partial u_j$.
La jacobiana de $\ell$ respecto de $\mathbf v$ es una fila: $(\nabla_{\mathbf v}\ell)^{\mathsf T}$, de $1\times\dim\mathbf v$.

::: theorem {#dl-teo-operacion-fundamental title="La operación fundamental"}
Si $\ell$ depende de $\mathbf u$ solo a través de $\mathbf v$,

$$
\nabla_{\mathbf u}\ell=\Bigl(\frac{\partial\mathbf v}{\partial\mathbf u}\Bigr)^{\mathsf T}\nabla_{\mathbf v}\ell .
$$

Pasar el gradiente un eslabón hacia atrás es multiplicarlo por la jacobiana de ese eslabón, traspuesta.
:::

::: proof {#dl-dem-operacion-fundamental of="dl-teo-operacion-fundamental"}
1. La regla de la cadena con $\mathbf s=\ell$ da $(\nabla_{\mathbf u}\ell)^{\mathsf T}=(\nabla_{\mathbf v}\ell)^{\mathsf T}\,\partial\mathbf v/\partial\mathbf u$, de $1\times\dim\mathbf u$.
2. Traspón los dos lados: la traspuesta de un producto invierte el orden.
:::

Una capa tiene solo dos eslabones, y sus jacobianas son sencillas.

- **El eslabón lineal**, $\mathbf z=\mathbf W\mathbf a+\mathbf b$. Como $z_i=\sum_j w_{ij}a_j+b_i$, la derivada $\partial z_i/\partial a_j$ es $w_{ij}$. La jacobiana **es** $\mathbf W$, y entonces $\nabla_{\mathbf a}\ell=\mathbf W^{\mathsf T}\nabla_{\mathbf z}\ell$.
- **El eslabón de activación**, $\mathbf a=g(\mathbf z)$, componente por componente. $a_i$ depende solo de $z_i$: la jacobiana es diagonal, con $g'(z_i)$ en la diagonal.

$$
\frac{\partial\mathbf a}{\partial\mathbf z}=
\begin{array}{c|cccc}
 & z_1 & z_2 & \cdots & z_{\dim\mathbf z}\\\hline
a_1 & g'(z_1) & 0 & \cdots & 0\\
a_2 & 0 & g'(z_2) & \cdots & 0\\
\vdots & \vdots & & \ddots & \vdots\\
a_{\dim\mathbf z} & 0 & 0 & \cdots & g'(z_{\dim\mathbf z})
\end{array}
$$

- **Filas:** una por salida $a_i$; **columnas:** una por entrada $z_j$, tantas como filas.
- **Entrada $(i,j)$:** $g'(z_i)$ si $i=j$, y cero fuera de la diagonal.

Multiplicar por una diagonal es multiplicar entrada por entrada.
Eso se escribe $\odot$: $(\mathbf u\odot\mathbf v)_i=u_iv_i$, el producto componente a componente.
Así, $\nabla_{\mathbf z}\ell=\nabla_{\mathbf a}\ell\odot g'(\mathbf z)$.

Las derivadas de las tres $g$ de la clase, en una línea cada una:

- **ReLU:** $g'(z)=1$ si $z>0$ y $0$ si $z<0$. En $z=0$ no hay derivada; por convención tomamos 0.
- **Identidad:** $g'(z)=1$.
- **Sigmoide:** $\sigma'(z)=\sigma(z)\bigl(1-\sigma(z)\bigr)$.

::: exercise {#dl-ej-jacobiana-capa title="Escribe una jacobiana de activación"}
En la red del hilo, la capa 1 usa ReLU y $\mathbf z^{(1)}=(0.2,\ -0.2,\ 0.6)$.

(a) ¿De qué tamaño es $\partial\mathbf a^{(1)}/\partial\mathbf z^{(1)}$? Escríbela con sus filas y columnas rotuladas.

(b) Si llegara $\nabla_{\mathbf a^{(1)}}\ell=(v_1,\ v_2,\ v_3)$, ¿cuánto valdría $\nabla_{\mathbf z^{(1)}}\ell$?
:::

::: hint {#dl-pista-jacobiana-capa-1 of="dl-ej-jacobiana-capa" title="Pista 1 · Una componente a la vez"}
¿De qué componentes de $\mathbf z^{(1)}$ depende $a^{(1)}_1$? ¿Qué signo tiene cada $z^{(1)}_j$?
:::

::: answer {#dl-resp-jacobiana-capa of="dl-ej-jacobiana-capa" title="Respuesta · Una diagonal con un cero"}
(a) Es de $3\times3$. Fuera de la diagonal todo es cero, porque $a^{(1)}_i$ solo depende de $z^{(1)}_i$.
En la diagonal va $\operatorname{ReLU}'(z^{(1)}_i)$: 1, 0 y 1, porque $z^{(1)}_2<0$.

$$
\frac{\partial\mathbf a^{(1)}}{\partial\mathbf z^{(1)}}=
\begin{array}{c|ccc}
 & z^{(1)}_1 & z^{(1)}_2 & z^{(1)}_3\\\hline
a^{(1)}_1 & 1 & 0 & 0\\
a^{(1)}_2 & 0 & 0 & 0\\
a^{(1)}_3 & 0 & 0 & 1
\end{array}
$$

(b) La traspuesta es la misma matriz, así que $\nabla_{\mathbf z^{(1)}}\ell=(v_1,\ 0,\ v_3)$: la componente 2 se corta.
:::

## 3 · Definir el error de cada capa

**Piensa: al bajar de la salida a la capa 1, ¿qué cantidad conviene guardar para no repetir cuentas?**

La derivada de $\ell$ respecto de cada preactivación.
Todo peso de la capa $l$ entra a $\ell$ a través de $\mathbf z^{(l)}$; si ya la tienes, cada peso sale en una multiplicación.

::: definition {#dl-def-delta title="El error de la capa l"}
Para una observación, el error de la capa $l$ es el gradiente de su pérdida respecto de las preactivaciones de esa capa:

$$
\mathbf{δ}^{(l)}:=\nabla_{\mathbf z^{(l)}}\ell\in\mathbb R^{d_l},
\qquad \delta^{(l)}_i=\frac{\partial\ell}{\partial z^{(l)}_i}.
$$

$\delta^{(l)}_i$ dice cuánto sube la pérdida por unidad que suba $z^{(l)}_i$, la preactivación de la neurona $i$ de la capa $l$.
:::

«Error» es el nombre de costumbre. No es el residual $e=y-\widehat y$ de la unidad 9, aunque en la salida se le parece: con salida identidad, $\delta^{(L)}=2(\widehat y-y)=-2e$, como se ve abajo.
Tampoco es la $\delta$ de la unidad 9, la probabilidad de fallar de la predicción conformal.

::: theorem {#dl-teo-dos-ecuaciones title="Las dos ecuaciones de la retropropagación"}
En la capa de salida, con $\mathbf a^{(L)}=\widehat{\mathbf y}$:

$$
\mathbf{δ}^{(L)}=\nabla_{\mathbf a^{(L)}}\ell\odot g^{(L)\prime}(\mathbf z^{(L)}).
$$

En cada capa oculta, de $l=L-1$ hasta $l=1$:

$$
\mathbf{δ}^{(l)}=\bigl(\mathbf W^{(l+1)\mathsf T}\mathbf{δ}^{(l+1)}\bigr)\odot g^{(l)\prime}(\mathbf z^{(l)}).
$$
:::

::: proof {#dl-dem-dos-ecuaciones of="dl-teo-dos-ecuaciones"}
1. Salida: $\mathbf z^{(L)}\to\mathbf a^{(L)}$ es un eslabón de activación; se multiplica por $g^{(L)\prime}$ componente a componente.
2. Ocultas: de $\mathbf z^{(l)}$ a $\ell$ el camino pasa por $\mathbf a^{(l)}$ y luego por $\mathbf z^{(l+1)}$.
3. El eslabón lineal da $\nabla_{\mathbf a^{(l)}}\ell=\mathbf W^{(l+1)\mathsf T}\mathbf{δ}^{(l+1)}$.
4. El de activación multiplica por $g^{(l)\prime}(\mathbf z^{(l)})$ componente a componente.
:::

Con $\ell=(\widehat y-y)^2$, el primer factor es $\nabla_{\widehat y}\ell=2(\widehat y-y)$.
Con salida identidad, $g^{(L)\prime}=1$ y queda $\delta^{(L)}=2(\widehat y-y)$.

Es la cuenta del video 4 de la tarea, con una neurona por capa y $g=\sigma$:

$$
\frac{\partial C_0}{\partial w^{(L)}}=a^{(L-1)}\,\sigma'\bigl(z^{(L)}\bigr)\,2\bigl(a^{(L)}-y\bigr).
$$

Los dos últimos factores, $\sigma'(z^{(L)})\cdot2(a^{(L)}-y)$, son $\delta^{(L)}$.
El primero, $a^{(L-1)}$, es la activación del origen.
El gradiente del peso es $\delta\cdot a$: la regla de la sección 4.

**Las dimensiones cuadran.** $\mathbf W^{(l+1)}$ es de $d_{l+1}\times d_l$, así que su traspuesta es de $d_l\times d_{l+1}$:

$$
\underbrace{\mathbf W^{(l+1)\mathsf T}}_{d_l\times d_{l+1}}\ \underbrace{\mathbf{δ}^{(l+1)}}_{d_{l+1}\times1}\ =\ \text{un vector de }d_l\times1,
$$

del tamaño de $\mathbf z^{(l)}$, y el $\odot$ con $g^{(l)\prime}(\mathbf z^{(l)})$ conserva ese tamaño.

La traspuesta cambia el papel de los ejes. En $\mathbf W^{(l+1)}$ las filas eran destinos; en $\mathbf W^{(l+1)\mathsf T}$ son orígenes:

$$
\mathbf W^{(l+1)\mathsf T}=
\begin{array}{c|ccc}
 & i=1 & \cdots & i=d_{l+1}\\\hline
j=1 & w^{(l+1)}_{11} & \cdots & w^{(l+1)}_{d_{l+1}\,1}\\
\vdots & \vdots & & \vdots\\
j=d_l & w^{(l+1)}_{1\,d_l} & \cdots & w^{(l+1)}_{d_{l+1}\,d_l}
\end{array}
$$

- **Filas:** una por neurona de **origen** $j$, en la capa $l$; hay $d_l$.
- **Columnas:** una por neurona de **destino** $i$, en la capa $l+1$; hay $d_{l+1}$.
- **Entrada $(j,i)$:** el mismo peso $w^{(l+1)}_{ij}$ de siempre; solo cambió de lugar.

En componentes, para la neurona $j$ de la capa $l$:

$$
\delta^{(l)}_j=g^{(l)\prime}\bigl(z^{(l)}_j\bigr)\sum_{i=1}^{d_{l+1}}w^{(l+1)}_{ij}\,\delta^{(l+1)}_i .
$$

La neurona $j$ es **origen** de los pesos $w^{(l+1)}_{ij}$.
Recoge el error de cada destino $i$ al que manda, pesado con el mismo peso que usó hacia adelante.
Por eso aparece la columna $j$ de $\mathbf W^{(l+1)}$, que es la fila $j$ de su traspuesta.

La figura dibuja la red como la cadena de [[dl-composicion|la composición]].
Arriba va el pase hacia adelante; abajo, los errores que regresan.

::: figure {#dl-retropropagacion title="El error regresa por la misma cadena"}
![Arriba y en tenue, la cadena de capas recorrida hacia adelante, de x a la pérdida ℓ. Debajo, punteado, el pase hacia atrás: de ℓ nace δ(3) = 2(ŷ − y) ⊙ g(3) prima; de δ(3) se pasa a δ(2) multiplicando por W(3) traspuesta y luego ⊙ g(2) prima; de δ(2) a δ(1) multiplicando por W(2) traspuesta y luego ⊙ g(1) prima. Cada δ(l) queda bajo su capa f(l) y da sus gradientes: el de W(l) es δ(l) por a(l−1) traspuesta y el de b(l) es δ(l).](../_assets/dl-retropropagacion.svg)
:::

Cada flecha de abajo es una aplicación de @dl-teo-operacion-fundamental: una $\mathbf W^{\mathsf T}$ y un $\odot g'$ por capa.

> [!WARNING]
> Lectura equivocada: «El error regresa multiplicando por $\mathbf W$».
>
> Lectura correcta: **regresa por $\mathbf W^{\mathsf T}$: hacia adelante, la fila $i$ junta lo que llega al destino $i$; hacia atrás, la columna $j$ junta lo que sale del origen $j$.**

::: exercise {#dl-ej-por-que-traspuesta title="Encuentra el error de la propuesta"}
Alguien propone $\mathbf{δ}^{(1)}=\bigl(\mathbf W^{(2)}\mathbf{δ}^{(2)}\bigr)\odot g^{(1)\prime}(\mathbf z^{(1)})$ para la red del hilo.

(a) ¿Se puede calcular?

(b) Si las dos capas tuvieran el mismo ancho, ¿sería correcta?
:::

::: hint {#dl-pista-por-que-traspuesta-1 of="dl-ej-por-que-traspuesta" title="Pista 1 · Revisa tamaños y papeles"}
¿De qué tamaño son $\mathbf W^{(2)}$ y $\mathbf{δ}^{(2)}$? Y en $w^{(2)}_{ij}$, ¿qué índice es la neurona de la capa 1?
:::

::: answer {#dl-resp-por-que-traspuesta of="dl-ej-por-que-traspuesta" title="Respuesta · La traspuesta no es opcional"}
(a) No. $\mathbf W^{(2)}$ es de $2\times3$ y $\mathbf{δ}^{(2)}$ de $2\times1$: el producto no está definido.

(b) Tampoco. El producto existiría, pero la neurona $j$ de la capa 1 recibiría $\sum_i w^{(2)}_{ji}\delta^{(2)}_i$.
Esos son los pesos que llegan a la neurona $j$ de la capa 2, no los que salen de la neurona $j$ de la capa 1.
La neurona necesita los pesos por los que mandó su activación: la columna $j$ de $\mathbf W^{(2)}$.
:::

## 4 · Sacar los gradientes de pesos y sesgos

**Piensa: con $\mathbf{δ}^{(l)}$ en la mano, ¿cuánto cambia la pérdida si mueves $w^{(l)}_{ij}$?**

El peso $w^{(l)}_{ij}$ solo aparece en una preactivación: $z^{(l)}_i=\sum_j w^{(l)}_{ij}a^{(l-1)}_j+b^{(l)}_i$.
Ahí lo multiplica $a^{(l-1)}_j$. La cadena tiene un solo eslabón más.

::: theorem {#dl-teo-gradientes title="Gradientes de pesos y sesgos"}
Para una observación,

$$
\frac{\partial\ell}{\partial w^{(l)}_{ij}}=\delta^{(l)}_i\,a^{(l-1)}_j,
\qquad
\frac{\partial\ell}{\partial b^{(l)}_i}=\delta^{(l)}_i .
$$

En matrices,

$$
\nabla_{\mathbf W^{(l)}}\ell=\mathbf{δ}^{(l)}\,\mathbf a^{(l-1)\mathsf T},
\qquad
\nabla_{\mathbf b^{(l)}}\ell=\mathbf{δ}^{(l)} .
$$
:::

**Error del destino × activación del origen.** Esa es la regla de cada peso.

$\nabla_{\mathbf W^{(l)}}\ell$ tiene la forma de $\mathbf W^{(l)}$, con los mismos rótulos:

$$
\underbrace{\mathbf{δ}^{(l)}}_{d_l\times1}\ \underbrace{\mathbf a^{(l-1)\mathsf T}}_{1\times d_{l-1}}=
\begin{array}{c|ccc}
 & a^{(l-1)}_1 & \cdots & a^{(l-1)}_{d_{l-1}}\\\hline
\delta^{(l)}_1 & \delta^{(l)}_1a^{(l-1)}_1 & \cdots & \delta^{(l)}_1a^{(l-1)}_{d_{l-1}}\\
\vdots & \vdots & & \vdots\\
\delta^{(l)}_{d_l} & \delta^{(l)}_{d_l}a^{(l-1)}_1 & \cdots & \delta^{(l)}_{d_l}a^{(l-1)}_{d_{l-1}}
\end{array}
$$

Las filas son los destinos $i$ y las columnas los orígenes $j$, como en $\mathbf W^{(l)}$.
Dos consecuencias se leen en la tabla:

- Si $a^{(l-1)}_j=0$, **toda la columna $j$** del gradiente es cero: un origen apagado no mueve sus pesos de salida.
- Si $\delta^{(l)}_i=0$, **toda la fila $i$** y el sesgo $b^{(l)}_i$ quedan en cero: ese destino no aprende de esta observación.

**De una observación al conjunto.** Con $n$ observaciones $(\mathbf x_k,\mathbf y_k)$, el gradiente de $L(\theta)$ es el promedio:

$$
\nabla_{\mathbf W^{(l)}}L=\frac1n\sum_{k=1}^{n}\mathbf{δ}^{(l)}_k\,\mathbf a^{(l-1)\mathsf T}_k ,
$$

con $\mathbf{δ}^{(l)}_k$ y $\mathbf a^{(l-1)}_k$ los de la observación $k$.
Lo mismo con un lote de observaciones, en la página siguiente.
Aquí la observación lleva índice $k$, no $i$ como en la unidad 9: $i$ ya es la neurona destino.

**Y el lagrangeano.** $\mathcal L=L+\mu(\Omega-d)$ solo agrega el gradiente del castigo:

$$
\nabla_{\mathbf W^{(l)}}\mathcal L=\nabla_{\mathbf W^{(l)}}L+\mu\,\nabla_{\mathbf W^{(l)}}\Omega,
\qquad
\nabla_{\mathbf b^{(l)}}\mathcal L=\nabla_{\mathbf b^{(l)}}L .
$$

Con ridge, $\Omega=\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$ y el término es $2\mu\mathbf W^{(l)}$.
Los sesgos no se penalizan. Con otra $\Omega$ se cambia solo ese término; la retropropagación no se toca.

## 5 · Retropropagar el ejemplo a mano

**Piensa: en el hilo, $\widehat y=0.546$ y $y=1$. ¿Qué signo esperas en $\delta^{(3)}$?**

Negativo: la salida quedó corta.
Subir $z^{(3)}$ acerca $\widehat y$ a 1 y baja la pérdida.

Lo único que se necesita del pase hacia adelante son las $\mathbf z^{(l)}$ y las $\mathbf a^{(l)}$ que ya guardaste.
Las matrices de pesos son las de [[dl-la-red|la red]]; aquí se usan dos, con filas destino $i$ y columnas origen $j$:

$$
\mathbf W^{(3)}=
\begin{array}{c|cc}
 & j=1 & j=2\\\hline
i=1 & 0.7 & -0.5
\end{array}
$$

$$
\mathbf W^{(2)}=
\begin{array}{c|ccc}
 & j=1 & j=2 & j=3\\\hline
i=1 & 0.4 & -0.3 & 0.5\\
i=2 & 0.2 & 0.6 & -0.1
\end{array}
$$

### Capa 3 · la salida

La salida es identidad, así que $g^{(3)\prime}=1$:

$$
\delta^{(3)}=2(\widehat y-y)=2(0.546-1)=-0.908 .
$$

Su gradiente es $\delta^{(3)}\,\mathbf a^{(2)\mathsf T}$, con $\mathbf a^{(2)}=(0.48,\ 0.18)$:

$$
\nabla_{\mathbf W^{(3)}}\ell=
\begin{array}{c|cc}
 & j=1 & j=2\\\hline
i=1 & -0.908\cdot0.48 & -0.908\cdot0.18
\end{array}
=
\begin{array}{c|cc}
 & j=1 & j=2\\\hline
i=1 & -0.436 & -0.163
\end{array}
$$

El sesgo recibe $\nabla_{b^{(3)}_1}\ell=\delta^{(3)}=-0.908$.

Todas las cifras van redondeadas a tres decimales.
Si multiplicas las ya redondeadas, la última cifra puede salirte distinta en uno.

### Capa 2 · la primera oculta desde arriba

El error baja por $\mathbf W^{(3)\mathsf T}$, con filas origen $j$ (capa 2) y una columna destino $i$ (capa 3):

$$
\mathbf W^{(3)\mathsf T}\delta^{(3)}=
\begin{array}{c|c}
 & i=1\\\hline
j=1 & 0.7\\
j=2 & -0.5
\end{array}
\,(-0.908)=
\begin{array}{c|c}
j=1 & -0.636\\
j=2 & 0.454
\end{array}
$$

Las dos preactivaciones, $\mathbf z^{(2)}=(0.48,\ 0.18)$, son positivas: ReLU deja pasar todo, $g^{(2)\prime}=(1,\ 1)$.
Entonces $\mathbf{δ}^{(2)}=(-0.636,\ 0.454)$.

Con $\mathbf a^{(1)}=(0.2,\ 0,\ 0.6)$:

$$
\nabla_{\mathbf W^{(2)}}\ell=
\begin{array}{c|ccc}
 & j=1 & j=2 & j=3\\\hline
i=1 & -0.127 & 0 & -0.381\\
i=2 & 0.091 & 0 & 0.272
\end{array}
$$

La columna $j=2$ es cero porque $a^{(1)}_2=0$. El sesgo recibe $\nabla_{\mathbf b^{(2)}}\ell=\mathbf{δ}^{(2)}$.

### Capa 1 · tu turno

::: exercise {#dl-ej-delta-capa-1 title="Calcula el error de la capa 1"}
Con $\mathbf W^{(2)}$, $\mathbf{δ}^{(2)}=(-0.636,\ 0.454)$ y $\mathbf z^{(1)}=(0.2,\ -0.2,\ 0.6)$:

(a) Calcula $\mathbf W^{(2)\mathsf T}\mathbf{δ}^{(2)}$.

(b) Calcula $\mathbf{δ}^{(1)}$.

(c) Calcula $\nabla_{\mathbf W^{(1)}}\ell$, con $\mathbf a^{(0)}=\mathbf x=(1,\ 2)$.
:::

::: hint {#dl-pista-delta-capa-1-1 of="dl-ej-delta-capa-1" title="Pista 1 · Usa columnas"}
La entrada $j$ de $\mathbf W^{(2)\mathsf T}\mathbf{δ}^{(2)}$ usa la columna $j$ de $\mathbf W^{(2)}$. ¿Qué vale $g^{(1)\prime}$ en cada una de las tres preactivaciones?
:::

::: answer {#dl-resp-delta-capa-1 of="dl-ej-delta-capa-1" title="Respuesta · Una neurona no recibe nada"}
(a) Columna por columna:
$0.4(-0.636)+0.2(0.454)\approx-0.163$,
$-0.3(-0.636)+0.6(0.454)\approx0.463$ y
$0.5(-0.636)-0.1(0.454)\approx-0.363$.
Con los valores sin redondear, la primera da $-0.163$; con los redondeados, $-0.164$.

(b) $g^{(1)\prime}(\mathbf z^{(1)})=(1,\ 0,\ 1)$, porque $z^{(1)}_2=-0.2<0$.
Así $\mathbf{δ}^{(1)}=(-0.163,\ 0,\ -0.363)$.

(c) $\mathbf{δ}^{(1)}\mathbf x^{\mathsf T}$, con filas destino $i$ y columnas origen $j$:

$$
\begin{array}{c|cc}
 & j=1 & j=2\\\hline
i=1 & -0.163 & -0.327\\
i=2 & 0 & 0\\
i=3 & -0.363 & -0.726
\end{array}
$$
:::

::: exercise {#dl-ej-relu-inactiva title="Explica una fila de ceros"}
La neurona 2 de la capa 1 recibió $0.463$ desde arriba, pero su fila de $\nabla_{\mathbf W^{(1)}}\ell$ y su sesgo quedaron en cero.

(a) ¿Por qué?

(b) Si cambiaras $y$ a cualquier otro valor, ¿esa fila dejaría de ser cero?
:::

::: hint {#dl-pista-relu-inactiva-1 of="dl-ej-relu-inactiva" title="Pista 1 · Escribe la componente 2"}
Escribe $\delta^{(1)}_2$ como el producto de las dos piezas de la segunda ecuación de @dl-teo-dos-ecuaciones. ¿Cuánto vale cada pieza en el hilo?
:::

::: answer {#dl-resp-relu-inactiva of="dl-ej-relu-inactiva" title="Respuesta · La neurona apagada no aprende"}
(a) $z^{(1)}_2=-0.2<0$, así que ReLU tiene derivada 0 y $\delta^{(1)}_2=0.463\cdot0=0$.
Su fila del gradiente es $\delta^{(1)}_2\,\mathbf x^{\mathsf T}=\mathbf 0$ y su sesgo recibe $\delta^{(1)}_2=0$.

(b) No. $y$ cambia lo que llega desde arriba, pero el factor $g^{(1)\prime}(z^{(1)}_2)=0$ depende solo de $\mathbf z^{(1)}$, que no usa $y$.
Mientras su preactivación sea negativa, esa neurona no aprende de esta observación.
Con sigmoide no pasa: $\sigma'$ nunca vale cero.
:::

### Lo que dicen los signos

Todos los números del hilo, juntos:

::: table {#dl-tab-retro-hilo title="La retropropagación del hilo, capa por capa"}
| Capa | $\mathbf{δ}^{(l)}$ | Activación del origen | Gradiente de los pesos |
|---|---|---|---|
| 3 | $(-0.908)$ | $\mathbf a^{(2)}=(0.48,\ 0.18)$ | $(-0.436,\ -0.163)$ |
| 2 | $(-0.636,\ 0.454)$ | $\mathbf a^{(1)}=(0.2,\ 0,\ 0.6)$ | columna 2 en cero |
| 1 | $(-0.163,\ 0,\ -0.363)$ | $\mathbf x=(1,\ 2)$ | fila 2 en cero |
:::

Un gradiente negativo dice que **subir ese peso baja la pérdida**.
Por ejemplo, $\partial\ell/\partial w^{(3)}_{11}=-0.436$: conviene subir $w^{(3)}_{11}=0.7$.
La página siguiente da ese paso.

## 6 · Comprobar con diferencias finitas

**Piensa: tu código de retropropagación da números. ¿Cómo sabes que son los correctos?**

Comparándolos con una derivada aproximada, que no usa la regla de la cadena.
Para un parámetro $w$ cualquiera, con $h$ pequeño:

$$
\frac{\partial\ell}{\partial w}\approx\frac{\ell(w+h)-\ell(w-h)}{2h}.
$$

Aquí $h$ es solo ese número pequeño, $10^{-6}$ en `redes.py`.
Cada parámetro pide dos pases hacia adelante: 40 pases para los 20 del hilo.
Por eso sirve para **comprobar**, no para entrenar.

Los dos gradientes se comparan por bloque ($\mathbf W^{(l)}$ o $\mathbf b^{(l)}$) con el error relativo:

$$
\frac{\lVert\text{retro}-\text{difer}\rVert}{\lVert\text{retro}\rVert+\lVert\text{difer}\rVert},
$$

donde «retro» es el bloque que dio la retropropagación y «difer» el de diferencias finitas.
Dividir entre las normas hace comparables bloques grandes y chicos.

En el hilo, el peor bloque da un error relativo menor que $10^{-10}$: los 20 números coinciden.
Un error en el código, en cambio, deja la cifra lejos de cero.

::: exercise {#dl-ej-olvidar-el-dos title="Calcula el error relativo de un descuido"}
Tu código escribe $\delta^{(L)}=\widehat y-y$ y olvida el 2.
¿Qué error relativo da la comprobación en cada bloque?
:::

::: hint {#dl-pista-olvidar-el-dos-1 of="dl-ej-olvidar-el-dos" title="Pista 1 · Sigue el factor"}
Si $\delta^{(L)}$ sale a la mitad, ¿qué pasa con cada $\mathbf{δ}^{(l)}$ y cada gradiente? Escribe «retro» en términos de «difer».
:::

::: answer {#dl-resp-olvidar-el-dos of="dl-ej-olvidar-el-dos" title="Respuesta · Un tercio en todos los bloques"}
Las dos ecuaciones son lineales en $\mathbf{δ}^{(L)}$, así que todo sale a la mitad: retro $=\tfrac12$ difer.
El error relativo es $\dfrac{\tfrac12\lVert\text{difer}\rVert}{\tfrac32\lVert\text{difer}\rVert}=\tfrac13$, muy lejos de $10^{-10}$.
:::

## Ejercicio final

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#dl-ej-final-retropropagacion title="Retropropaga una red con dos salidas"}
Una red 3–4–2 tiene la capa oculta con sigmoide y la salida identidad.
La idea nueva: la salida tiene **dos** componentes y la pérdida es $\ell=(\widehat y_1-y_1)^2+(\widehat y_2-y_2)^2$, donde el subíndice en cursiva es la componente de $\widehat{\mathbf y}$, no una observación.
No hay números: todo se escribe en general.

1. Da el tamaño de $\mathbf W^{(1)}$, $\mathbf b^{(1)}$, $\mathbf W^{(2)}$, $\mathbf b^{(2)}$, $\mathbf{δ}^{(1)}$ y $\mathbf{δ}^{(2)}$.
2. Escribe $\mathbf{δ}^{(2)}$ y $\mathbf{δ}^{(1)}$.
3. Escribe $\nabla_{\mathbf W^{(1)}}\ell$ y comprueba su tamaño.
4. Di si alguna fila de $\nabla_{\mathbf W^{(1)}}\ell$ puede quedar en cero por la activación, como en el hilo.
5. ¿Cuántos pases hacia adelante pide la comprobación por diferencias finitas?
:::

::: hint {#dl-pista-final-retropropagacion-1 of="dl-ej-final-retropropagacion" title="Pista 1 · Ordena las piezas"}
¿Cuánto vale $d_0$, $d_1$ y $d_2$? ¿Qué es $\nabla_{\widehat{\mathbf y}}\ell$ cuando hay dos salidas: un número o un vector?
:::

::: hint {#dl-pista-final-retropropagacion-2 of="dl-ej-final-retropropagacion" title="Pista 2 · Revisa tu propuesta"}
Comprueba con dos preguntas: ¿tu $\mathbf W^{(2)\mathsf T}\mathbf{δ}^{(2)}$ tiene el tamaño de $\mathbf z^{(1)}$? ¿Puede valer cero $\sigma(z)(1-\sigma(z))$?
:::

::: answer {#dl-resp-final-retropropagacion of="dl-ej-final-retropropagacion" title="Respuesta · Las mismas dos ecuaciones"}
**1. Tamaños.** $d_0=3$, $d_1=4$, $d_2=2$.
$\mathbf W^{(1)}$ es de $4\times3$, $\mathbf b^{(1)}$ y $\mathbf{δ}^{(1)}$ tienen 4 entradas.
$\mathbf W^{(2)}$ es de $2\times4$, $\mathbf b^{(2)}$ y $\mathbf{δ}^{(2)}$ tienen 2.

**2. Errores.** El gradiente de la pérdida es ahora un vector, $\nabla_{\widehat{\mathbf y}}\ell=2(\widehat{\mathbf y}-\mathbf y)$, y la identidad tiene derivada 1:

$$
\mathbf{δ}^{(2)}=2(\widehat{\mathbf y}-\mathbf y),
\qquad
\mathbf{δ}^{(1)}=\bigl(\mathbf W^{(2)\mathsf T}\mathbf{δ}^{(2)}\bigr)\odot\sigma(\mathbf z^{(1)})\odot\bigl(1-\sigma(\mathbf z^{(1)})\bigr).
$$

El $1-\sigma(\mathbf z^{(1)})$ se calcula componente a componente.

$\mathbf W^{(2)\mathsf T}$ es de $4\times2$ y $\mathbf{δ}^{(2)}$ de $2\times1$: el producto tiene 4 entradas, como $\mathbf z^{(1)}$.
Cada neurona oculta recoge el error de las **dos** salidas.

**3. Gradiente.** $\nabla_{\mathbf W^{(1)}}\ell=\mathbf{δ}^{(1)}\mathbf x^{\mathsf T}$: $(4\times1)(1\times3)=4\times3$, la forma de $\mathbf W^{(1)}$.

**4. Filas en cero.** No por la activación: $\sigma(z)$ está entre 0 y 1 sin tocarlos, y su derivada nunca vale cero.
Una fila puede anularse solo si $\mathbf W^{(2)\mathsf T}\mathbf{δ}^{(2)}$ tiene un cero en esa entrada.
Una columna puede anularse si una entrada $x_j$ vale cero.

**5. Comprobación.** Hay $12+4+8+2=26$ parámetros; con dos pases cada uno, 52 pases.
:::

**Punto de control:** deberías poder escribir las dos ecuaciones de $\mathbf{δ}$, explicar la $\mathbf W^{\mathsf T}$ y sacar un gradiente como error del destino por activación del origen.

## Lo que hay que llevarse

- **La operación fundamental:** $\nabla_{\mathbf u}\ell=(\partial\mathbf v/\partial\mathbf u)^{\mathsf T}\nabla_{\mathbf v}\ell$. Por una capa: $\mathbf W^{\mathsf T}$ y luego $\odot g'$.
- **El error de cada capa:** $\mathbf{δ}^{(L)}=\nabla_{\mathbf a^{(L)}}\ell\odot g^{(L)\prime}(\mathbf z^{(L)})$ y $\mathbf{δ}^{(l)}=(\mathbf W^{(l+1)\mathsf T}\mathbf{δ}^{(l+1)})\odot g^{(l)\prime}(\mathbf z^{(l)})$, de $(d_l\times d_{l+1})(d_{l+1}\times1)$.
- **Los gradientes:** $\partial\ell/\partial w^{(l)}_{ij}=\delta^{(l)}_ia^{(l-1)}_j$, o sea $\nabla_{\mathbf W^{(l)}}\ell=\mathbf{δ}^{(l)}\mathbf a^{(l-1)\mathsf T}$ y $\nabla_{\mathbf b^{(l)}}\ell=\mathbf{δ}^{(l)}$. El lagrangeano suma $2\mu\mathbf W^{(l)}$ con ridge.
- **En el hilo:** $\delta^{(3)}=-0.908$, $\mathbf{δ}^{(2)}=(-0.636,\ 0.454)$ y $\mathbf{δ}^{(1)}=(-0.163,\ 0,\ -0.363)$. La neurona 2 de la capa 1, apagada, no aprende.
- **La comprobación:** diferencias finitas con 40 pases para 20 parámetros; error relativo menor que $10^{-10}$.

Continúa con [[dl-entrenar|Entrenar la red]].
