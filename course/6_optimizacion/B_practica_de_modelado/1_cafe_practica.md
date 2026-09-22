---
id: opt-practica-cafe
title: "Preparar una mezcla de café"
nav_title: "Café: práctica"
summary: "Formular una mezcla por kilogramo y su variante con paquetes completos, sin calcular la mejor compra."
status: ready
tags: [optimizacion, modelado, practica]
---

# Preparar una mezcla de café

**Tu tarea:** escribir dos modelos completos, no encontrar cuánto comprar.
Son situaciones habituales de una cafetería; los números son didácticos.
Intenta cada ejercicio antes de abrir sus ayudas.

## Problema 1 · Comprar por kilogramo

::: exercise {#opt-b-cafe-ej-mezcla title="Una mezcla para la semana"}
Una cafetería prepara **20 kg de café mezclando dos orígenes, A y B**. Puede
comprar fracciones de kilogramo. El origen A cuesta 180 pesos por kg y hay
12 kg disponibles; el B cuesta 120 pesos por kg y hay 16 kg disponibles.

Para conservar el sabor de la receta, **al menos el 40 % del peso de la mezcla
debe ser del origen A**. No hay pérdidas al mezclar: cada kilogramo comprado
se incorpora a la preparación. Se paga únicamente la cantidad comprada.

La cafetería quiere preparar exactamente los 20 kg y gastar lo menos posible.
**Define los datos y las decisiones; escribe el objetivo, todas las
restricciones y el dominio de cada variable.**
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-b-cafe-pista-mezcla-datos of="opt-b-cafe-ej-mezcla" title="PISTA 1 · Solo si te atoraste"}
| Dato | Origen A | Origen B |
|---|---:|---:|
| Costo por kilogramo | 180 pesos | 120 pesos |
| Disponible | 12 kg | 16 kg |

| Condición de la mezcla | Información del relato |
|---|---|
| Peso total | Exactamente 20 kg |
| Participación del origen A | Al menos 40 % del peso |
| Cantidades permitidas | Fracciones de kilogramo |
| Pérdidas | Ninguna |

Debes decidir cuánto comprar de cada origen.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-b-cafe-pista-mezcla-guia of="opt-b-cafe-ej-mezcla" title="PISTA 2 · Solo si te atoraste"}
¿El porcentaje de la receta se refiere al dinero gastado o al peso preparado?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-cafe-resp-mezcla of="opt-b-cafe-ej-mezcla" title="Respuesta · Del relato al modelo"}
**1. Leer las condiciones.** La cantidad preparada es exacta. La disponibilidad
es un máximo; la participación de A es un mínimo. El costo mide dinero, mientras
que la receta y las existencias se refieren a masa.

**2. Separar parámetros y decisiones.** Para escribir una regla que admita más
orígenes, sea $J$ el conjunto de orígenes y $S\subseteq J$ el conjunto cuya
participación mínima exige la receta. Aquí $J=\{A,B\}$ y $S=\{A\}$.

| Parámetro conocido | Significado y unidad |
|---|---|
| $D>0$ | Peso total requerido, en kg |
| $c_j\ge0$ | Costo del origen $j$, en pesos/kg |
| $s_j\ge0$ | Disponibilidad del origen $j$, en kg |
| $\alpha\in[0,1]$ | Fracción mínima del peso que debe provenir de $S$ |

La decisión $x_j$ es cuántos **kg** comprar del origen $j$. Como pueden medirse
fracciones de kilogramo, $x_j\in\mathbb R_{\ge0}$.

**3. Construir cada expresión.** Costo por kilogramo multiplicado por
kilogramos da pesos: $c_jx_j$. Sumamos esos costos para obtener el gasto total.

Sumar las compras da el peso preparado porque no hay pérdidas. El mínimo de
la receta se obtiene multiplicando la fracción requerida por el peso total:
$\alpha D$ kg. La suma de las cantidades de los orígenes de $S$ debe alcanzar
ese mínimo.

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

## Problema 2 · El proveedor cambia la presentación

::: exercise {#opt-b-cafe-ej-paquetes title="Comprar paquetes completos"}
Esta variante conserva la mezcla del problema 1, pero cambia cómo se compra.
El proveedor vende A en **paquetes de 4 kg** y B en **paquetes de 2 kg**. Solo
vende paquetes completos, y **todo lo comprado debe entrar en esta mezcla**:
no se permite guardar sobrantes ni desechar café.

La cafetería necesita exactamente **20 kg**, con **al menos 40 % del peso de A**.
A cuesta 180 pesos por kg y hay 12 kg disponibles; B cuesta 120 pesos por kg y
hay 16 kg disponibles. No hay pérdidas y se busca el menor costo total.

**Escribe el modelo completo de esta variante. Explica qué representa cada
variable y por qué elegiste su dominio.**
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-b-cafe-pista-paquetes-datos of="opt-b-cafe-ej-paquetes" title="PISTA 1 · Solo si te atoraste"}
| Dato | Origen A | Origen B |
|---|---:|---:|
| Costo por kilogramo | 180 pesos | 120 pesos |
| Disponible | 12 kg | 16 kg |
| Presentación de venta | Paquete de 4 kg | Paquete de 2 kg |

Se preparan exactamente 20 kg, al menos 40 % de A. Los paquetes se compran
completos y se usan íntegramente; no hay pérdidas ni sobrantes.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-b-cafe-pista-paquetes-guia of="opt-b-cafe-ej-paquetes" title="PISTA 2 · Solo si te atoraste"}
¿Qué compras que eran posibles por kilogramo ahora rechazaría el proveedor?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-cafe-resp-paquetes of="opt-b-cafe-ej-paquetes" title="Respuesta · Contar paquetes y medir kilogramos"}
**1. Identificar el cambio.** Ahora la unidad que podemos contar es el paquete.
Exigir kilogramos enteros no basta: por ejemplo, un kilogramo de A no constituye
un paquete completo.

**2. Definir datos y decisiones.** Conservamos $J,S,D,c_j,s_j,\alpha$ del modelo
anterior y añadimos el dato $q_j>0$: kg que contiene cada paquete del origen $j$.

Elegimos $n_j$, el número de paquetes comprados del origen $j$, con
$n_j\in\mathbb Z_{\ge0}$. La masa comprada es $q_jn_j$ kg. No necesitamos otra
variable para representarla.

**3. Traducir todas las reglas a sus unidades.** La disponibilidad, la receta y
el peso total se expresan en kg: usamos $q_jn_j$ en cada una. El costo es
$c_jq_jn_j$ pesos, porque el precio dado es por kilogramo, no por paquete.

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

Después de escribir tus intentos, consulta [[opt-modelo-cafe|la estructura general y su forma estándar]].
