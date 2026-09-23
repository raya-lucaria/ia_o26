---
id: opt-objetivo-panaderia-practica
title: Decidir cuánto pan producir antes de conocer la demanda
nav_title: "Panadería: ejemplo guiado"
summary: "Construir ventas, ingresos y ganancia para comparar una producción por su promedio o por su peor resultado."
status: ready
estimated_time: 25m
tags: [optimizacion, modelado, incertidumbre]
---

# Decidir cuánto pan producir antes de conocer la demanda

En salones, cada asignación tenía una molestia conocida. En la panadería,
una misma producción puede dejar ganancias distintas según cuántas piezas
se vendan. **Primero construiremos la ganancia; después decidiremos cómo
compararla cuando no conocemos la demanda.**

## 1 · Decidir esta noche para vender mañana

La panadería puede producir entre **0 y 100 piezas enteras**. Debe elegir
la cantidad esta noche y no puede ajustarla después de conocer la demanda.
Los datos de este ejemplo son didácticos.

| Por cada pieza | Pesos |
|---|---:|
| Precio de venta | 8 |
| Costo de producción | 2 |

El costo se paga por todas las piezas producidas, incluidas las que no se
venden. Los sobrantes no tienen valor de recuperación. Se vende toda la
cantidad que permitan la producción y la demanda, sin otros costos ni ingresos.

Para mañana se consideran estos dos escenarios:

| Demanda | Probabilidad |
|---|---:|
| 20 piezas | 0.8 |
| 80 piezas | 0.2 |

Suponemos que las probabilidades describen adecuadamente la incertidumbre.
La responsable propone elegir la producción con mayor ganancia promedio.

**Piensa: ¿podemos elegir una producción para cada demanda?**

No: elegimos una sola cantidad antes de conocer cuál demanda ocurrirá.
Llamaremos $q$ a las piezas producidas. Para formular con parámetros,
usaremos los siguientes datos:

- $Q\in\mathbb Z_{\ge0}$: capacidad de producción, en piezas.
- $S$: conjunto finito no vacío de escenarios.
- $d_s\in\mathbb Z_{\ge0}$: demanda del escenario $s$, en piezas.
- $v$ y $c$: precio de venta y costo de producción, en pesos por pieza;
  en este relato, $v>c>0$.
- $p_s$: probabilidad del escenario $s$, con $p_s\ge0$ y $\sum_{s\in S}p_s=1$.

Las condiciones sobre la decisión son

$$0\le q\le Q,\qquad q\in\mathbb Z.$$

Ni la demanda ni su probabilidad se pueden elegir para mejorar el resultado.

## 2 · De las piezas al dinero ganado

**Piensa: si producimos más de lo que se pide, ¿qué limita las ventas? ¿Y si producimos menos?**

Cuando sobra pan, vendemos la cantidad que se pide. Cuando falta, vendemos
todo lo producido. La cantidad vendida es la menor de las dos:

$$\text{piezas vendidas en el escenario }s=\min(q,d_s).$$

El ingreso corresponde a las piezas **vendidas**. El costo corresponde a
todas las piezas **producidas**, incluso si algunas sobran:

$$I(q,d_s)=v\min(q,d_s),\qquad C(q)=cq.$$

Multiplicar pesos por pieza por piezas da pesos en ambas expresiones.
La ganancia es el dinero que queda del ingreso después de pagar la producción:

$$\Pi(q,d_s)=v\min(q,d_s)-cq.$$

Puede ser negativa si no vendemos lo suficiente para cubrir el costo.
Las ventas y la ganancia quedan determinadas por $q$ y la demanda; no son
otras decisiones que podamos escoger por separado.

## 3 · Construir la ganancia promedio

**Piensa: ¿deberían pesar igual los dos resultados si sus probabilidades son distintas?**

Para calcular el promedio propuesto, multiplicamos la ganancia de cada
escenario por su probabilidad y sumamos. Así obtenemos la **ganancia esperada**,
medida en pesos. El modelo completo es

$$
\begin{aligned}
\max\quad &\sum_{s\in S}p_s\bigl[v\min(q,d_s)-cq\bigr]\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Al sustituir $Q=100$, $v=8$, $c=2$ y los dos escenarios, queda

$$
\begin{aligned}
\max\quad &0.8\bigl[8\min(q,20)-2q\bigr]\\
&\quad+0.2\bigl[8\min(q,80)-2q\bigr]\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

**Las probabilidades permiten calcular ese promedio; no obligan a preferirlo.**
La responsable eligió ese criterio. Podría considerar inaceptable un resultado
muy bajo, aunque quedara compensado por una ganancia alta en otro escenario.

## 4 · Comprobar qué cuenta el objetivo

**Piensa: ¿recibir más dinero por ventas siempre significa ganar más?**

Comparemos dos producciones permitidas, sin buscar la mejor entre todas.
Las columnas corresponden a producir 20 y 65 piezas; los resultados están en pesos.

| Resultado | 20 | 65 |
|---|---:|---:|
| Ingreso esperado | 160 | 232 |
| Costo de producción | 40 | 130 |
| Ganancia esperada | 120 | 102 |

Para 65 piezas, los ingresos son 160 pesos si se piden 20 y 520 pesos si
se piden 80. El ingreso esperado se calcula así:

$$
\begin{aligned}
&0.8(160)+0.2(520)\\
&=232\text{ pesos}.
\end{aligned}
$$

Producir 65 da más ingreso esperado, pero el aumento del costo es mayor
que el del ingreso. Por eso deja menos ganancia esperada.

Minimizar solo el costo tampoco expresa ganar más: producir cero cuesta
cero y deja ganancia cero. Producir 20 cuesta 40 pesos y deja una ganancia
de 120 pesos en cualquiera de los dos escenarios.

Maximizar ingresos equivale a maximizar ganancia si el costo es el mismo
en todas las decisiones comparadas. Minimizar costos equivale a maximizar
ganancia si el ingreso es el mismo. Aquí no se cumplen esas condiciones
para el conjunto de producciones permitidas.

## 5 · Cambiar la prioridad ante la incertidumbre

**Piensa: ¿esperar una ganancia de 102 pesos garantiza ganar al menos esa cantidad mañana?**

No. Al producir 65 piezas, las ganancias son 30 pesos si se piden 20 y
390 pesos si se piden 80. Su promedio es $0.8(30)+0.2(390)=102$ pesos;
no es una ganancia mínima garantizada ni una predicción exacta de mañana.

Ahora imaginemos que conocemos las mismas demandas posibles, pero **ya no
contamos con probabilidades justificadas**. No podemos usar 0.8 y 0.2 para
comparar decisiones. Tampoco podemos asignar probabilidades iguales como
si desconocerlas significara que los escenarios son igualmente probables.

Una prioridad posible es que la menor ganancia entre los escenarios sea
lo más alta posible. Para cada producción tomamos su menor ganancia y
buscamos aumentar ese valor. El modelo es

$$
\begin{aligned}
\max\quad &\min_{s\in S}\Pi(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Con los datos conocidos, su objetivo compara las dos ganancias siguientes;
las condiciones siguen exigiendo una producción entera entre 0 y 100:

$$
\begin{aligned}
\max\quad &\min\{8\min(q,20)-2q,\\
&\qquad 8\min(q,80)-2q\}\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

Este criterio protege la ganancia mínima **entre los escenarios incluidos**.
No afirma que el peor vaya a ocurrir ni considera con qué frecuencia ocurre.
Desconocer las probabilidades no obliga a elegirlo; también podríamos
adoptarlo con probabilidades conocidas si esa protección fuera nuestra prioridad.

Tanto el promedio como el peor caso dependen de los escenarios considerados.
Ninguno garantiza protección frente a cualquier demanda omitida. Cambiar
las demandas posibles o añadir costos requeriría revisar la formulación.

Continúa con [[opt-objetivo-clasificacion-practica|cómo comparar aciertos y probabilidades al clasificar mensajes]].

Para practicar después: [[opt-practica-riesgo|comparar la ganancia con lo que habríamos ganado conociendo la demanda]]. La [[opt-objetivo-panaderia-modelo|consulta opcional de panadería]] desarrolla esos criterios con más detalle.
