---
id: opt-modelo-cafe
title: "Cómo escribir el modelo de una mezcla"
nav_title: "Café: modelo general"
summary: "Reconocer los datos, dominios y restricciones de una mezcla y expresarlos en la forma estándar del curso."
status: ready
tags: [optimizacion, modelado, practica]
---

# Cómo escribir el modelo de una mezcla

**Primero intenta los [[opt-practica-cafe|dos problemas de café]].** Aquí veremos
cómo escribir esa misma compra cuando haya más ingredientes. También pondremos
los dos modelos en la forma estándar que usamos en el curso.

La pregunta sigue siendo: **¿cuánto comprar de cada ingrediente para cumplir
la receta al menor costo?**

## 1 · Nombrar los datos y la compra

El pedido exige un peso exacto. Todo lo comprado entra en la mezcla y no se
pierde nada al prepararla. Por eso podemos usar la misma cantidad para hablar
del café que compramos y del que lleva la mezcla.

Llamamos $J$ al conjunto de ingredientes disponibles; debe ser finito y tener
al menos un elemento. Dentro de $J$, el conjunto $S$ reúne los ingredientes
cuya aportación conjunta debe alcanzar la proporción mínima de la receta.
En la práctica solo A tenía ese requisito; aquí podemos agrupar varios.

- $D>0$: Masa total requerida, en kg.
- $c_j\ge0$: Precio constante del ingrediente $j$, en pesos/kg.
- $s_j\ge0$: Disponibilidad del ingrediente $j$, en kg.
- $\alpha\in[0,1]$: Fracción mínima de masa procedente de $S$.

Para cada ingrediente $j\in J$, elegimos $x_j$: los **kg que compramos de ese
ingrediente**. Como se permiten fracciones de kilogramo y no cantidades
negativas, su dominio es:

$$x_j\in\mathbb R_{\ge0}\qquad\text{para cada }j\in J.$$

No elegimos el precio, la disponibilidad ni la receta. Cambiar sus datos
describe otro pedido; cambiar $x_j$ describe otra compra para el mismo pedido.

## 2 · Escribir el gasto y las reglas de la receta

Para comparar compras, necesitamos calcular cuánto cuesta **cualquier compra
permitida**. Multiplicar el precio $c_j$, en pesos por kg, por la cantidad
$x_j$, en kg, da un gasto de $c_jx_j$ pesos.

Sumamos los gastos de todos los ingredientes y pedimos el menor total:

$$\min\quad \sum_{j\in J}c_jx_j.$$

Ahora escribimos cada obligación del pedido.

**Preparar el peso exacto.** La suma de las compras es el peso de la mezcla,
porque usamos todo y no hay pérdidas. Debe coincidir con el pedido:

$$\sum_{j\in J}x_j=D.$$

**Respetar las existencias.** Cada ingrediente tiene su propio límite.
Escribimos una condición para cada uno:

$$x_j\le s_j\qquad\text{para cada }j\in J.$$

**Cumplir la proporción mínima.** La fracción requerida es $\alpha$ y el
peso total es $D$ kg. Por eso los ingredientes de $S$, sumados, deben aportar
al menos $\alpha D$ kg:

$$\sum_{j\in S}x_j\ge\alpha D.$$

Ese mínimo sale de la receta y del peso fijado en el pedido; no necesitamos
resolver el problema para conocerlo. Si el total no estuviera fijado, no
podríamos usar $D$ de esta manera.

**Las mismas variables aparecen en el gasto y en todas las condiciones.**
Al cambiar una cantidad $x_j$, cambiamos cuánto cuesta, cuánto pesa y, si el
ingrediente pertenece a $S$, cuánto aporta a la proporción exigida.

## 3 · Escribir el mismo modelo en forma estándar

Ya tenemos el objetivo, las restricciones y los dominios. Para reunirlos en
la **forma estándar lineal del curso**, escribiremos una maximización,
restricciones con $\le$ y variables no negativas.

Hacemos tres cambios de escritura que conservan las compras permitidas y
cuáles son las mejores:

- **Objetivo:** minimizar el costo equivale a maximizar su negativo. Se
  conservan las mejores compras; el valor del objetivo cambia de signo.
- **Peso exacto:** exigimos tanto «no más de $D$» como «no menos de $D$».
  Juntas, esas condiciones obligan a comprar exactamente $D$ kg. Para escribir
  la segunda con $\le$, multiplicamos sus dos lados por $-1$.
- **Mínimo de receta:** también multiplicamos sus dos lados por $-1$.
  Al hacerlo, el signo $\ge$ se convierte en $\le$.

No agregamos variables ni condiciones nuevas al pedido. El modelo completo es:

$$
\begin{aligned}
\max\quad &-\sum_{j\in J}c_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J}x_j\le D,\\
&-\sum_{j\in J}x_j\le-D,\\
&x_j\le s_j &&\text{para cada }j\in J,\\
&-\sum_{j\in S}x_j\le-\alpha D,\\
&x_j\in\mathbb R_{\ge0} &&\text{para cada }j\in J.
\end{aligned}
$$

Las dos primeras restricciones juntas representan el peso exacto. Las otras
conservan las existencias y la proporción de la receta.

Este modelo es **lineal**: las variables se multiplican por datos conocidos
y se suman; no se multiplican entre sí.

## 4 · Qué cambia al comprar paquetes completos

Al pasar al problema 2, el pedido y la receta se conservan. Lo que cambia es
la venta: solo se pueden comprar paquetes completos. Añadimos el **dato**
$q_j>0$, que dice cuántos kg contiene un paquete del ingrediente $j$.

Ahora elegimos $n_j$, el número de paquetes de ese ingrediente, con dominio
$n_j\in\mathbb Z_{\ge0}$. Pedir un número entero de kg no bastaría: la cantidad
comprada debe ser un múltiplo del peso de cada paquete.

Para pasar de paquetes a kilogramos, multiplicamos:

$$\underbrace{x_j}_{\text{kg}}=
\underbrace{q_j}_{\text{kg por paquete}}\,
\underbrace{n_j}_{\text{paquetes}}.$$

**Una vez elegidos los paquetes, los kilogramos quedan determinados.**
En el siguiente modelo usamos $n_j$ y calculamos la masa como $q_jn_j$;
ya no necesitamos elegir $x_j$ por separado.

Si quisiéramos conservar ambas variables, tendríamos que agregar la igualdad
$x_j=q_jn_j$. Así representarían la misma compra.

- **Objetivo**: Sigue midiendo costo; cada paquete cuesta $c_jq_j$ pesos.
- **Restricciones de masa**: Sustituimos cada $x_j$ por $q_jn_j$, siempre en kg.
- **Dominio**: Contamos paquetes enteros; no permitimos fracciones de paquete.

La obligación de usar todo lo comprado sigue siendo esencial: los kilogramos
de los paquetes son los que deben completar el pedido, sin guardar sobrantes
ni desechar café. Con esa condición, obtenemos el modelo completo en la misma
forma estándar:

$$
\begin{aligned}
\max\quad &-\sum_{j\in J}c_jq_jn_j\\
\text{sujeto a}\quad
&\sum_{j\in J}q_jn_j\le D,\\
&-\sum_{j\in J}q_jn_j\le-D,\\
&q_jn_j\le s_j &&\text{para cada }j\in J,\\
&-\sum_{j\in S}q_jn_j\le-\alpha D,\\
&n_j\in\mathbb Z_{\ge0} &&\text{para cada }j\in J.
\end{aligned}
$$

Es **lineal entero**. Los precios $c_j$ y los tamaños $q_j$ son datos, así que
$c_jq_j$ es un coeficiente conocido: multiplicarlo por $n_j$ conserva la
linealidad. El dominio exige que el número de paquetes sea entero.

La nueva presentación puede hacer imposible un pedido exacto. Formular
correctamente el problema no garantiza que haya una compra que cumpla
todas sus condiciones.

## Qué razonamiento puedes reutilizar

**Primero elige qué cuenta cada variable; después revisa las unidades en
todas sus apariciones.** Un cambio de unidad de compra afecta tanto al
objetivo como a las restricciones. Si hubiera sobrantes o pérdidas,
comprar y usar ya no serían necesariamente la misma cantidad.

[[opt-practica-cafe|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
