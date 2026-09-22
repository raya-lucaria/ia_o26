---
id: opt-modelo-cafe
title: "El modelo general de una mezcla"
nav_title: "Café: modelo general"
summary: "Reconocer los datos, dominios y restricciones de una mezcla y expresarlos en la forma estándar del curso."
status: ready
tags: [optimizacion, modelado, practica]
---

# El modelo general de una mezcla

**Primero intenta los [[opt-practica-cafe|dos problemas de café]].** Aquí
reconstruimos el razonamiento para cualquier número de ingredientes.
La pregunta es: **¿cuánto comprar de cada uno para cumplir la receta al menor costo?**

## 1 · Separar lo conocido de lo que elegimos

El relato fija una mezcla de peso exacto, sin pérdidas, y exige usar todo lo
comprado. Esas condiciones determinan cómo relacionamos compras y mezcla.

| Dato conocido | Significado |
|---|---|
| $J$ | Conjunto finito no vacío de ingredientes |
| $S\subseteq J$ | Ingredientes cuya participación conjunta tiene un mínimo |
| $D>0$ | Masa total requerida, en kg |
| $c_j\ge0$ | Precio constante del ingrediente $j$, en pesos/kg |
| $s_j\ge0$ | Disponibilidad del ingrediente $j$, en kg |
| $\alpha\in[0,1]$ | Fracción mínima de masa procedente de $S$ |

Elegimos $x_j$: **kg comprados del ingrediente $j$**. Hay una variable por
ingrediente. Como se permiten fracciones y no compras negativas,
$x_j\in\mathbb R_{\ge0}$.

No elegimos el precio, la disponibilidad ni la receta. Cambiar sus datos
describe otro pedido; cambiar $x_j$ describe otra compra para el mismo pedido.

## 2 · Construir el objetivo y las condiciones

Para gastar lo menos posible, primero escribimos cuánto cuesta **cualquier**
compra. Precio por cantidad da $c_jx_j$ pesos; sumamos todos los ingredientes:

$$\min\quad \sum_{j\in J}c_jx_j.$$

Ahora traducimos cada obligación sin buscar todavía la mejor compra:

| Condición del relato | Traducción | Por qué |
|---|---|---|
| Preparar exactamente el pedido | $\sum_{j\in J}x_j=D$ | Toda la compra entra en la mezcla, sin pérdidas |
| No comprar más de lo disponible | $x_j\le s_j$ para cada $j$ | Cada ingrediente tiene su propia existencia |
| Cumplir la proporción mínima | $\sum_{j\in S}x_j\ge\alpha D$ | El grupo requerido debe aportar esa fracción del peso total |

**Son las mismas cantidades en todas las filas.** No elegimos una compra
para el costo y otra para la receta. Al cambiar $x_j$, cambian simultáneamente
su costo, su aportación al peso y, si $j\in S$, su aportación a la proporción.

El mínimo $\alpha D$ no es una cota descubierta resolviendo el ejemplo:
proviene del porcentaje pedido y del total fijo. Si el total no estuviera
fijado, no podríamos usar $D$ de esta manera.

## 3 · Pasar a la forma estándar sin cambiar el pedido

En el curso, la forma estándar lineal **maximiza**, usa $\le$ y declara
variables no negativas. Adaptamos la escritura:

- **Objetivo:** minimizar el costo equivale a maximizar su negativo. Se
  conservan las mejores compras; el valor del objetivo cambia de signo.
- **Peso exacto:** escribimos tanto «no más de $D$» como «no menos de $D$».
- **Mínimo de receta:** multiplicamos ambos lados por $-1$ e invertimos el signo.

No agregamos variables ni nuevas condiciones al pedido. El modelo completo es:

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

Las dos primeras filas juntas representan la igualdad. Las demás conservan
la disponibilidad y la receta. Este modelo es **lineal**.

## 4 · Qué cambia al comprar paquetes completos

En el problema 2 cambia la unidad de compra. Añadimos el **dato** $q_j>0$:
kg que contiene un paquete del ingrediente $j$.

Elegimos ahora $n_j\in\mathbb Z_{\ge0}$, el número de paquetes. Un número
entero de kg no bastaría: debe comprarse un múltiplo del tamaño del paquete.
La relación entre las dos maneras de contar es

$$\underbrace{x_j}_{\text{kg}}=
\underbrace{q_j}_{\text{kg por paquete}}\,
\underbrace{n_j}_{\text{paquetes}}.$$

**Reemplazamos las variables de masa por variables de paquetes.** En el
modelo siguiente no elegimos $x_j$ y $n_j$ por separado: la masa queda
calculada como $q_jn_j$. Si decidiéramos conservar ambas, tendríamos que
agregar la igualdad $x_j=q_jn_j$ para enlazarlas.

| Parte | Qué cambia y qué se conserva |
|---|---|
| Objetivo | Sigue midiendo costo; cada paquete cuesta $c_jq_j$ pesos |
| Restricciones de masa | Sustituimos cada $x_j$ por $q_jn_j$, siempre en kg |
| Dominio | Contamos paquetes enteros; no permitimos fracciones de paquete |

Así obtenemos el modelo completo, en la misma forma estándar:

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

Es **lineal entero**: $c_j$ y $q_j$ son datos, así que sus productos con $n_j$
siguen siendo lineales. La nueva presentación puede hacer imposible el
pedido exacto; formular correctamente no garantiza que exista una compra válida.

## Qué razonamiento puedes reutilizar

**Primero elige qué cuenta cada variable; después revisa las unidades en
todas sus apariciones.** Un cambio de unidad de compra afecta tanto al
objetivo como a las restricciones. Si hubiera sobrantes o pérdidas,
comprar y usar ya no serían necesariamente la misma cantidad.

[[opt-practica-cafe|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
