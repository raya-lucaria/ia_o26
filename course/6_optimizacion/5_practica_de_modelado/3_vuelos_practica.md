---
id: opt-practica-vuelos
title: "Asignar aviones a vuelos"
nav_title: "Vuelos: práctica"
summary: "Dos ejercicios para asignar aviones completos: cubrir vuelos, respetar capacidades y distinguirlas de las autorizaciones."
status: ready
tags: [optimizacion, modelado, entera, practica]
---

# Asignar aviones a vuelos

Una aerolínea debe decidir qué avión realizará cada vuelo. Necesita llevar a
todos los pasajeros, respetar las condiciones de operación y gastar lo menos
posible.

**Tu tarea es escribir los dos modelos completos.** No hace falta encontrar
la asignación más barata. Los números son didácticos, no datos de una empresa real.

## Problema 3 · Elegir un avión para cada vuelo

::: exercise {#opt-b-vuelos-ej-asignar title="Un avión para cada vuelo"}
Una aerolínea tiene tres aviones disponibles en el mismo aeropuerto: A1 tiene
100 asientos utilizables, A2 tiene 150 y A3 tiene 180. Desde allí deben salir
tres vuelos: V1 lleva 70 pasajeros con reservación, V2 lleva 100 y V3 lleva 140.

Todos los pasajeros deben viajar. Al elegir el avión para cada vuelo, hay que
respetar estas condiciones:

- Los tres vuelos ocurren en la misma franja, así que **cada avión puede realizar
  como máximo uno**.
- **Un solo avión llevará a todos los pasajeros de cada vuelo.** No se permite
  cancelar vuelos ni repartir sus pasajeros entre varios aviones.
- El avión elegido debe tener suficientes asientos para los pasajeros de ese vuelo.

El costo total de operar cada pareja avión–vuelo, en **miles de pesos**, es:

| Avión | V1 | V2 | V3 |
|---|---:|---:|---:|
| A1 | 18 | 24 | 30 |
| A2 | 23 | 26 | 35 |
| A3 | 26 | 30 | 33 |

Es el costo del vuelo completo, no por pasajero. Un avión sin asignación no
aporta costo en este modelo. No hay otras restricciones de operación.

La aerolínea quiere realizar los tres vuelos al menor costo total.
**Formula un modelo completo:** define qué se decide, cómo calcular el costo
y qué condiciones debe cumplir la asignación. Incluye los dominios de las
variables y escribe el modelo primero con parámetros y luego con estos datos.
:::

### Primero intenta plantearlo

Antes de abrir las pistas, escribe un primer intento. Identifica qué elige
la aerolínea y qué debe comprobar para aceptar esa elección.

::: hint {#opt-b-vuelos-pista-asignar-datos of="opt-b-vuelos-ej-asignar" title="Pista 1 · Ordenar los datos"}
Cada avión puede hacer como máximo un vuelo en esta franja:

| Avión | Asientos | Vuelos |
|---|---:|---|
| A1 | 100 | 0 o 1 |
| A2 | 150 | 0 o 1 |
| A3 | 180 | 0 o 1 |

Cada vuelo necesita exactamente un avión:

| Vuelo | Pasajeros | Aviones |
|---|---:|---|
| V1 | 70 | 1 |
| V2 | 100 | 1 |
| V3 | 140 | 1 |

La tabla del enunciado da costos **totales por pareja**, en miles de pesos.
:::

Con los datos ordenados, vuelve a tu intento antes de pasar a la segunda pista.

::: hint {#opt-b-vuelos-pista-asignar-guia of="opt-b-vuelos-ej-asignar" title="Pista 2 · Revisar las condiciones"}
¿Qué debes comprobar por separado para cada vuelo y para cada avión?
:::

Antes de leer la respuesta, revisa si tu modelo recoge todas las condiciones
del relato. Después podrás comparar cómo las expresaste.

::: answer {#opt-b-vuelos-resp-asignar of="opt-b-vuelos-ej-asignar" title="Respuesta · Contar aviones, vuelos y asientos"}
**1. Separar datos y decisiones.** Sean $A$ el conjunto de aviones y $V$ el
conjunto de vuelos. La aerolínea ya conoce estos datos:

- $s_a$: Asientos utilizables del avión $a$.
- $d_v$: Pasajeros que deben viajar en el vuelo $v$.
- $c_{av}$: Costo de operar el vuelo $v$ con el avión $a$, en miles de pesos.

Lo que falta decidir es qué avión realiza cada vuelo. Definimos $x_{av}=1$
si asignamos el avión $a$ al vuelo $v$ y $x_{av}=0$ si no lo asignamos.

Cada variable representa una elección de **sí o no**, por eso es binaria.
Necesita dos índices para identificar la pareja avión–vuelo. Su valor no
representa una cantidad de pasajeros ni de asientos.

**2. Construir las condiciones y el costo.** Para comprobar que un vuelo $v$
queda cubierto, sumamos las decisiones que podrían asignarle un avión:

$$\sum_{a\in A}x_{av}.$$

La suma cuenta cuántos aviones recibe ese vuelo. Si vale cero, el vuelo queda
sin atender; si vale dos, le hemos asignado dos aviones. El relato exige
**exactamente uno**, así que esta suma debe valer uno para cada vuelo.

Ahora miramos un avión $a$ y sumamos sus decisiones sobre todos los vuelos:

$$\sum_{v\in V}x_{av}.$$

Esta cuenta indica cuántos vuelos le asignamos al mismo avión. Como ocurren
en la misma franja, no puede superar uno. Sí puede valer cero: se permite
dejar un avión sin usar.

Para comprobar los asientos, el producto $s_ax_{av}$ aporta la capacidad del
avión $a$ cuando lo elegimos para el vuelo $v$; aporta cero cuando no lo elegimos.
Por tanto,

$$\sum_{a\in A}s_ax_{av}$$

cuenta los asientos asignados a ese vuelo. Como elegimos un único avión,
**solo un término corresponde al avión asignado**. Sus asientos deben alcanzar
para los $d_v$ pasajeros.

Hay que comprobar la capacidad vuelo por vuelo. Sumar todos los asientos de
la flota no garantiza que cada pasajero tenga lugar en el vuelo que reservó.

El costo se construye de manera parecida. Cada pareja elegida aporta $c_{av}$
miles de pesos, de modo que $c_{av}x_{av}$ es su contribución al costo total.
Sumamos esas contribuciones sobre todos los aviones y vuelos. No multiplicamos
por pasajeros: el dato ya incluye operar el vuelo completo.

**3. Escribir el modelo general completo.**

$$
\begin{aligned}
\min\quad &\sum_{a\in A}\sum_{v\in V}c_{av}x_{av}\\
\text{sujeto a}\quad
&\sum_{a\in A}x_{av}=1 &&\text{para cada }v\in V,\\
&\sum_{v\in V}x_{av}\le1 &&\text{para cada }a\in A,\\
&\sum_{a\in A}s_ax_{av}\ge d_v &&\text{para cada }v\in V,\\
&x_{av}\in\{0,1\} &&\text{para cada }a\in A,\ v\in V.
\end{aligned}
$$

**4. Sustituir los datos.** En $x_{av}$, el primer número identifica al avión
y el segundo al vuelo; ambos recorren $\{1,2,3\}$.

$$
\begin{aligned}
\min\quad &18x_{11}+24x_{12}+30x_{13}\\
&\quad+23x_{21}+26x_{22}+35x_{23}\\
&\quad+26x_{31}+30x_{32}+33x_{33}\\
\text{sujeto a}\quad
&x_{11}+x_{21}+x_{31}=1,\\
&x_{12}+x_{22}+x_{32}=1,\\
&x_{13}+x_{23}+x_{33}=1,\\
&x_{11}+x_{12}+x_{13}\le1,\\
&x_{21}+x_{22}+x_{23}\le1,\\
&x_{31}+x_{32}+x_{33}\le1,\\
&100x_{11}+150x_{21}+180x_{31}\ge70,\\
&100x_{12}+150x_{22}+180x_{32}\ge100,\\
&100x_{13}+150x_{23}+180x_{33}\ge140,\\
&x_{av}\in\{0,1\} &&a,v\in\{1,2,3\}.
\end{aligned}
$$

**Comprobación:** A1 no puede cubrir V3: sus 100 asientos no alcanzan para
140 pasajeros. Que otro avión tenga asientos libres no cambia esa condición.
:::

## Problema 4 · Asignar aviones con una prohibición

::: exercise {#opt-b-vuelos-ej-autorizaciones title="Espacio disponible no significa permiso"}
La aerolínea debe asignar los mismos aviones a los mismos vuelos del problema 3.
Los aviones A1, A2 y A3 tienen 100, 150 y 180 asientos utilizables. Los vuelos
V1, V2 y V3 tienen 70, 100 y 140 pasajeros con reservación, respectivamente.

Se conservan las condiciones de operación:

- Los aviones están disponibles en el mismo aeropuerto y los vuelos salen de
  allí en una misma franja. Cada avión puede realizar como máximo un vuelo.
- Todos los pasajeros deben viajar. Cada vuelo recibe exactamente un avión
  con suficientes asientos, sin cancelaciones ni pasajeros repartidos.

Ahora hay una condición adicional: **A2 no tiene autorización para realizar V1**.
Todas las demás parejas avión–vuelo están autorizadas, aunque siguen teniendo
que cumplir el requisito de asientos.

Los costos totales por pareja, en **miles de pesos**, siguen siendo:

| Avión | V1 | V2 | V3 |
|---|---:|---:|---:|
| A1 | 18 | 24 | 30 |
| A2 | 23 | 26 | 35 |
| A3 | 26 | 30 | 33 |

Un avión sin asignación no aporta costo y no hay otras condiciones de operación.

**Formula el modelo completo para minimizar el costo total.** Escribe primero
una formulación con parámetros que también sirva para más aviones, vuelos y
parejas sin autorización. Después sustituye los datos de este caso. Conserva
las condiciones anteriores e incluye los dominios de las variables.
:::

### Primero intenta plantearlo

Antes de abrir las pistas, escribe un primer intento. Identifica qué elige
la aerolínea y qué debe comprobar para aceptar esa elección.

::: hint {#opt-b-vuelos-pista-autorizaciones-datos of="opt-b-vuelos-ej-autorizaciones" title="Pista 1 · Ordenar los datos"}
- **Asientos de A1, A2, A3**: 100, 150, 180.
- **Pasajeros de V1, V2, V3**: 70, 100, 140.
- **Por vuelo**: Exactamente un avión.
- **Por avión**: Como máximo un vuelo.
- **Nueva prohibición**: A2 no puede realizar V1.
- **Demás parejas**: Autorizadas; también deben cumplir la capacidad.

Los costos son los de la tabla del enunciado, en miles de pesos por vuelo completo.
:::

Con los datos ordenados, vuelve a tu intento antes de pasar a la segunda pista.

::: hint {#opt-b-vuelos-pista-autorizaciones-guia of="opt-b-vuelos-ej-autorizaciones" title="Pista 2 · Revisar las condiciones"}
¿Tener suficientes asientos garantiza que una pareja avión–vuelo esté permitida?
:::

Antes de leer la respuesta, revisa si tu modelo recoge todas las condiciones
del relato. Después podrás comparar cómo las expresaste.

::: answer {#opt-b-vuelos-resp-autorizaciones of="opt-b-vuelos-ej-autorizaciones" title="Respuesta · Distinguir un permiso de una decisión"}
**1. Nombrar el dato nuevo.** Para los conjuntos de aviones $A$ y vuelos $V$,
conservamos los datos de asientos $s_a$, pasajeros $d_v$ y costos $c_{av}$.
También conservamos la decisión binaria $x_{av}$: asignar o no el avión $a$
al vuelo $v$.

La aerolínea ya sabe cuáles parejas están autorizadas. Representamos esa
información mediante $p_{av}\in\{0,1\}$: vale uno si la pareja está autorizada
y cero si está prohibida. **El permiso es un dato; la asignación es una decisión.**

**2. Traducir el permiso en una condición.** La restricción debe distinguir
dos situaciones:

- Si $p_{av}=0$, no podemos elegir la pareja. Su decisión $x_{av}$ debe valer cero.
- Si $p_{av}=1$, podemos elegirla o descartarla. La autorización permite usar
  ese avión en ese vuelo, pero no obliga a hacerlo.

Con el dominio binario de $x_{av}$, ambos casos se expresan mediante

$$x_{av}\le p_{av}.$$

Cuando el permiso vale cero, solo queda permitido el cero. Cuando vale uno,
se admiten ambos valores de la decisión. Escribir una igualdad obligaría a
usar cada pareja autorizada, que no es lo que pide el relato.

Esta condición se añade a las de cobertura, uso y capacidad. Tener permiso
no garantiza suficientes asientos, y tener asientos no garantiza permiso.
El objetivo sigue sumando el costo de todas las parejas elegidas.

**3. Modelo general completo.**

$$
\begin{aligned}
\min\quad &\sum_{a\in A}\sum_{v\in V}c_{av}x_{av}\\
\text{sujeto a}\quad
&\sum_{a\in A}x_{av}=1 &&\text{para cada }v\in V,\\
&\sum_{v\in V}x_{av}\le1 &&\text{para cada }a\in A,\\
&\sum_{a\in A}s_ax_{av}\ge d_v &&\text{para cada }v\in V,\\
&x_{av}\le p_{av} &&\text{para cada }a\in A,\ v\in V,\\
&x_{av}\in\{0,1\} &&\text{para cada }a\in A,\ v\in V.
\end{aligned}
$$

**4. Sustituir los datos.** La tabla numérica de permisos, con filas para
aviones y columnas para vuelos, es:

$$
P=(p_{av})=
\begin{pmatrix}
1&1&1\\
0&1&1\\
1&1&1
\end{pmatrix}.
$$

La incorporamos al modelo completo; en su penúltima fila se aplica una
restricción por cada entrada de esta tabla:

$$
\begin{aligned}
\min\quad &18x_{11}+24x_{12}+30x_{13}\\
&\quad+23x_{21}+26x_{22}+35x_{23}\\
&\quad+26x_{31}+30x_{32}+33x_{33}\\
\text{sujeto a}\quad
&x_{11}+x_{21}+x_{31}=1,\\
&x_{12}+x_{22}+x_{32}=1,\\
&x_{13}+x_{23}+x_{33}=1,\\
&x_{11}+x_{12}+x_{13}\le1,\\
&x_{21}+x_{22}+x_{23}\le1,\\
&x_{31}+x_{32}+x_{33}\le1,\\
&100x_{11}+150x_{21}+180x_{31}\ge70,\\
&100x_{12}+150x_{22}+180x_{32}\ge100,\\
&100x_{13}+150x_{23}+180x_{33}\ge140,\\
&x_{av}\le p_{av} &&a,v\in\{1,2,3\},\\
&x_{av}\in\{0,1\} &&a,v\in\{1,2,3\}.
\end{aligned}
$$

**Comprobación:** A2 tiene espacio para V1, pero $p_{21}=0$ prohíbe asignarlo.
A1 tiene permiso para V3, pero no suficientes asientos. Son comprobaciones distintas.
:::

Después de tus intentos, consulta [[opt-modelo-vuelos|la estructura general de asignación y su forma estándar]].
