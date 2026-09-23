---
id: opt-practica-cafe
title: "Comprar café para una mezcla"
nav_title: "Café: práctica"
summary: "Formular una mezcla por kilogramo y su variante con paquetes completos, sin calcular la mejor compra."
status: ready
tags: [optimizacion, modelado, practica]
---

# Comprar café para una mezcla

Una cafetería necesita comprar café de dos orígenes para preparar su mezcla.
Primero podrá pedir las cantidades por kilogramo; después, el proveedor solo
venderá paquetes completos. Los números de ambos problemas son didácticos.

**Tu tarea es escribir el modelo de cada compra.** Explica qué se decide,
qué condiciones debe cumplir la mezcla y cómo se calcula el gasto.
No hace falta encontrar la compra más barata. Intenta cada problema antes de
abrir sus ayudas.

## Problema 1 · Preparar 20 kg comprando a granel

::: exercise {#opt-b-cafe-ej-mezcla title="Una mezcla para la semana"}
Una cafetería necesita preparar **exactamente 20 kg de café** mezclando dos
orígenes, A y B. Compra a granel: puede pedir la cantidad que necesite de cada
origen, incluidas fracciones de kilogramo. Paga únicamente lo que compra.

El proveedor ofrece estas cantidades para los orígenes A y B:

| Dato | A | B |
|---|---:|---:|
| Precio (pesos/kg) | 180 | 120 |
| Disponible (kg) | 12 | 16 |

La receta pide que **al menos el 40 % del peso de la mezcla sea del origen A**.
Todo el café comprado se usa en esta preparación y no se pierde nada al mezclar.

La cafetería quiere cumplir el pedido y **gastar lo menos posible**.
Escribe un modelo que permita elegir cuánto comprar de cada origen:

- Distingue los datos de las decisiones y explica sus unidades.
- Define las variables y los valores que pueden tomar.
- Escribe el objetivo y una restricción por cada condición del relato.

Presenta primero el modelo con parámetros y después sustituye los datos.
:::

### Primero intenta plantearlo

Escribe lo que puedas por tu cuenta. Si te atoras, abre la primera pista y
vuelve a tu intento.

::: hint {#opt-b-cafe-pista-mezcla-datos of="opt-b-cafe-ej-mezcla" title="Pista 1 · Ordena los datos de la compra"}
Las columnas A y B corresponden a los dos orígenes:

| Dato | A | B |
|---|---:|---:|
| Precio (pesos/kg) | 180 | 120 |
| Disponible (kg) | 12 | 16 |

- **Peso total**: Exactamente 20 kg.
- **Participación del origen A**: Al menos 40 % del peso.
- **Cantidades permitidas**: Fracciones de kilogramo.
- **Pérdidas**: Ninguna.
- **Uso del café comprado**: Todo entra en la mezcla.

Debes decidir cuánto comprar de cada origen.
:::

Si todavía no sabes cómo representar la receta, prueba con esta pregunta.

::: hint {#opt-b-cafe-pista-mezcla-guia of="opt-b-cafe-ej-mezcla" title="Pista 2 · ¿De qué es el porcentaje?"}
¿El porcentaje de la receta se refiere al dinero gastado o al peso preparado?
:::

Cuando tengas un planteamiento, abre la respuesta y compáralo paso a paso.

::: answer {#opt-b-cafe-resp-mezcla of="opt-b-cafe-ej-mezcla" title="Respuesta · De los kilogramos al modelo"}
**1. Distinguir las condiciones de la compra.** El pedido fija un peso exacto.
Las existencias ponen un máximo a lo que podemos comprar de cada origen;
la receta exige un mínimo del origen A.

El precio sirve para calcular dinero. Las otras condiciones hablan de
**kilogramos de café**, así que no podemos interpretar el 40 % como una parte
del gasto.

**2. Dar nombre a los datos y a las decisiones.** Primero escribiremos el
modelo con parámetros: símbolos que representan los datos conocidos. Así
podremos reconocer la misma estructura aunque cambien el pedido o los precios.

Llamamos $J$ al conjunto de orígenes disponibles. Dentro de él, $S\subseteq J$
reúne los orígenes cuya participación conjunta tiene un mínimo en la receta.
En este pedido, $J=\{A,B\}$ y $S=\{A\}$: ese mínimo corresponde solo a A.

- $D>0$: Peso total requerido, en kg.
- $c_j\ge0$: Costo del origen $j$, en pesos/kg.
- $s_j\ge0$: Disponibilidad del origen $j$, en kg.
- $\alpha\in[0,1]$: Fracción mínima del peso que debe provenir de $S$.

La variable $x_j$ representa cuántos **kg comprar del origen $j$**. Hay una
variable por origen. Podemos comprar fracciones de kilogramo, pero no cantidades
negativas; por eso elegimos el dominio $x_j\in\mathbb R_{\ge0}$.

**3. Construir el gasto y las restricciones.** Para cualquier compra, el
gasto en un origen se obtiene multiplicando su precio por la cantidad comprada:

$$c_jx_j\quad\text{pesos}.$$

Sumar ese gasto para todos los orígenes da el costo total que queremos minimizar.

**El peso comprado es también el peso preparado.** Esto se cumple porque todo
lo comprado entra en la mezcla y no hay pérdidas. Por eso el pedido se escribe:

$$\sum_{j\in J}x_j=D.$$

Cada origen tiene sus propias existencias. No podemos comprar más de ellas:

$$x_j\le s_j\qquad\text{para cada }j\in J.$$

Por último, la receta exige una fracción $\alpha$ del peso total. Como ese
peso está fijado en $D$ kg, el mínimo requerido es $\alpha D$ kg. Sumamos
lo comprado de los orígenes de $S$ y exigimos que alcance ese mínimo:

$$\sum_{j\in S}x_j\ge\alpha D.$$

El signo incluye la igualdad porque la receta dice «al menos».

**4. Reunir el modelo general.**

$$
\begin{aligned}
\min\quad &\sum_{j\in J}c_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J}x_j=D,\\
&x_j\le s_j &&\text{para cada }j\in J,\\
&\sum_{j\in S}x_j\ge\alpha D,\\
&x_j\in\mathbb R_{\ge0} &&\text{para cada }j\in J.
\end{aligned}
$$

**5. Sustituir los datos, conservando todas las condiciones.**

$$
\begin{aligned}
\min\quad &180x_A+120x_B\\
\text{sujeto a}\quad
&x_A+x_B=20,\\
&x_A\le12,\\
&x_B\le16,\\
&x_A\ge0.40(20),\\
&x_A,x_B\in\mathbb R_{\ge0}.
\end{aligned}
$$

**Comprobación:** comprar menos de lo disponible está permitido; preparar
menos de 20 kg no. Una mezcla con exactamente 40 % de A cumple la receta:
«al menos» incluye la igualdad. No hemos calculado la compra óptima.
:::

## Problema 2 · Preparar la misma mezcla con paquetes completos

::: exercise {#opt-b-cafe-ej-paquetes title="Comprar paquetes completos"}
La cafetería mantiene el mismo pedido, pero el proveedor cambia la forma de
venta. Ahora solo ofrece A en **paquetes completos de 4 kg** y B en
**paquetes completos de 2 kg**. No abre los paquetes para vender una parte.

Todo lo comprado debe entrar en esta mezcla. **No se permite guardar sobrantes
ni desechar café**, y sigue sin haber pérdidas al mezclar.

Estas condiciones del pedido se conservan:

- Preparar exactamente **20 kg**.
- Que al menos **40 % del peso de la mezcla provenga del origen A**.
- Pagar 180 pesos por kg de A y 120 pesos por kg de B.
- Comprar dentro de las existencias: 12 kg de A y 16 kg de B.

Se sigue buscando el menor costo total. Escribe el modelo completo, primero
con parámetros y después con estos datos. Explica qué cuenta cada variable
y por qué los valores que le permites representan las compras que acepta
el proveedor.
:::

### Primero intenta plantearlo

Revisa qué parte de tu modelo anterior necesita cambiar. Abre esta pista
solo si necesitas ordenar los datos.

::: hint {#opt-b-cafe-pista-paquetes-datos of="opt-b-cafe-ej-paquetes" title="Pista 1 · Revisa lo que vende el proveedor"}
Para cada origen, comparamos el precio, las existencias y el peso de cada paquete:

| Dato | A | B |
|---|---:|---:|
| Precio (pesos/kg) | 180 | 120 |
| Disponible (kg) | 12 | 16 |
| Paquete (kg) | 4 | 2 |

Se preparan exactamente 20 kg, al menos 40 % de A. Los paquetes se compran
completos y se usan íntegramente; no hay pérdidas ni sobrantes.
:::

Si sigues atorado, piensa en las compras que permite la nueva presentación.

::: hint {#opt-b-cafe-pista-paquetes-guia of="opt-b-cafe-ej-paquetes" title="Pista 2 · ¿Qué compras rechazaría?"}
¿Qué compras que eran posibles por kilogramo ahora rechazaría el proveedor?
:::

Compara tu propuesta con la respuesta cuando hayas intentado escribirla completa.

::: answer {#opt-b-cafe-resp-paquetes of="opt-b-cafe-ej-paquetes" title="Respuesta · De los paquetes al modelo"}
**1. Identificar el cambio.** Ahora la unidad que podemos contar es el paquete.
Exigir kilogramos enteros no basta: por ejemplo, un kilogramo de A no constituye
un paquete completo.

**2. Definir datos y decisiones.** Conservamos los datos del modelo anterior:
los orígenes $J$, el grupo $S$ exigido por la receta, el pedido $D$, los precios
$c_j$, las existencias $s_j$ y la fracción mínima $\alpha$.

Añadimos un dato: $q_j>0$, los **kg que contiene cada paquete** del origen $j$.
Elegimos $n_j$, el **número de paquetes comprados** de ese origen. Como solo
se venden completos, $n_j\in\mathbb Z_{\ge0}$.

**3. Pasar de paquetes a kilogramos y a pesos.** Cada paquete contiene $q_j$ kg.
Al comprar $n_j$ paquetes recibimos:

$$q_jn_j\quad\text{kg}.$$

Esta cantidad se calcula a partir de la compra; no necesitamos elegir otra
variable para ella. El proveedor sigue cobrando por kilogramo, de modo que
el gasto en ese origen es:

$$c_j(q_jn_j)\quad\text{pesos}.$$

Sumamos esos gastos para obtener el costo total. Las demás condiciones siguen
hablando de kilogramos, así que en todas ellas usamos $q_jn_j$:

- El peso total comprado debe ser exactamente $D$, porque todo entra en la mezcla.
- La cantidad de cada origen no puede superar sus existencias $s_j$.
- Los orígenes de $S$ deben aportar al menos $\alpha D$ kg.

**Cambiar cómo contamos la compra afecta todo el modelo**, aunque el pedido
y sus reglas sean los mismos.

**4. Escribir el modelo general completo.**

$$
\begin{aligned}
\min\quad &\sum_{j\in J}c_jq_jn_j\\
\text{sujeto a}\quad
&\sum_{j\in J}q_jn_j=D,\\
&q_jn_j\le s_j &&\text{para cada }j\in J,\\
&\sum_{j\in S}q_jn_j\ge\alpha D,\\
&n_j\in\mathbb Z_{\ge0} &&\text{para cada }j\in J.
\end{aligned}
$$

**5. Sustituir los datos.**

$$
\begin{aligned}
\min\quad &180(4n_A)+120(2n_B)\\
\text{sujeto a}\quad
&4n_A+2n_B=20,\\
&4n_A\le12,\\
&2n_B\le16,\\
&4n_A\ge0.40(20),\\
&n_A,n_B\in\mathbb Z_{\ge0}.
\end{aligned}
$$

**Comprobación:** contamos paquetes en el dominio, pero comparamos kilogramos
en las restricciones. La igualdad incorpora la obligación de usar todo lo
comprado; permitir sobrantes requeriría otro relato y otro modelo.
:::

Si quieres ampliar lo trabajado, tienes una consulta opcional sobre [[opt-modelo-cafe|la estructura general y su forma estándar]].

Si necesitas ayuda para construir el modelo, vuelve a [[opt-objetivo-salones-practica|el ejemplo guiado de salones]].

[[opt-construir-objetivo|Volver al banco de práctica]].
