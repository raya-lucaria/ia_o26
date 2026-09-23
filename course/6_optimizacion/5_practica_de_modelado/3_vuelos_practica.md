---
id: opt-practica-vuelos
title: "Asignar aviones a vuelos"
nav_title: "Vuelos: práctica"
summary: "Dos ejercicios para asignar aviones completos: cubrir vuelos, respetar capacidades y distinguirlas de las autorizaciones."
status: ready
tags: [optimizacion, modelado, entera, practica]
---

# Asignar aviones a vuelos

**Tu tarea:** escribir dos modelos completos, sin buscar la asignación más
barata. El contexto es una aerolínea; los números son didácticos, no datos de
una empresa real.

## Problema 3 · Cubrir tres vuelos

::: exercise {#opt-b-vuelos-ej-asignar title="Un avión para cada vuelo"}
Una aerolínea tiene tres aviones disponibles en el mismo aeropuerto. A1 tiene
100 asientos utilizables, A2 tiene 150 y A3 tiene 180.

Debe realizar tres vuelos desde ese aeropuerto: V1 tiene 70 pasajeros con
reservación, V2 tiene 100 y V3 tiene 140. Todos deben viajar. Los vuelos
ocurren en la misma franja: **cada avión puede realizar como máximo uno**.
Cada vuelo necesita **exactamente un avión**; no se permite cancelarlo ni
repartir a sus pasajeros entre varios aviones.

El costo total de operar cada pareja avión–vuelo, en **miles de pesos**, es:

| Avión | V1 | V2 | V3 |
|---|---:|---:|---:|
| A1 | 18 | 24 | 30 |
| A2 | 23 | 26 | 35 |
| A3 | 26 | 30 | 33 |

Es el costo del vuelo completo, no por pasajero. Un avión sin asignación no
aporta costo en este modelo. No hay otras restricciones de operación.

La aerolínea quiere cubrir los vuelos al menor costo total. **Define las
decisiones y escribe el objetivo, todas las restricciones y sus dominios.**
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-b-vuelos-pista-asignar-datos of="opt-b-vuelos-ej-asignar" title="PISTA 1 · Solo si te atoraste"}
| Avión disponible | Asientos utilizables | Vuelos que puede realizar en la franja |
|---|---:|---|
| A1 | 100 | Como máximo uno |
| A2 | 150 | Como máximo uno |
| A3 | 180 | Como máximo uno |

| Vuelo | Pasajeros que deben viajar | Aviones requeridos |
|---|---:|---|
| V1 | 70 | Exactamente uno |
| V2 | 100 | Exactamente uno |
| V3 | 140 | Exactamente uno |

La tabla del enunciado da costos **totales por pareja**, en miles de pesos.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-b-vuelos-pista-asignar-guia of="opt-b-vuelos-ej-asignar" title="PISTA 2 · Solo si te atoraste"}
¿Qué debes comprobar por separado para cada vuelo y para cada avión?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-vuelos-resp-asignar of="opt-b-vuelos-ej-asignar" title="Respuesta · Dos índices, dos tipos de cobertura"}
**1. Separar datos y decisiones.** Sean $A$ los aviones y $V$ los vuelos.
Los datos son $s_a$, asientos del avión $a$; $d_v$, pasajeros del vuelo $v$;
y $c_{av}$, costo total de usar ese avión en ese vuelo.

Definimos $x_{av}=1$ si asignamos el avión $a$ al vuelo $v$ y $0$ si no.
La variable es binaria, no un número de pasajeros. Necesita dos índices
porque identifica una pareja.

**2. Construir las condiciones.** Fijamos primero un vuelo $v$ y sumamos
sus decisiones sobre todos los aviones: debe haber exactamente un $1$.
Después fijamos un avión $a$ y sumamos sobre los vuelos: puede haber como
máximo un $1$. La desigualdad permite aviones sin uso.

Para cada vuelo, $\sum_a s_ax_{av}$ cuenta los asientos del avión elegido:
**solo uno de los términos está activo**. Deben alcanzar para sus $d_v$
pasajeros. No sustituimos esta condición por una suma global de asientos:
los pasajeros necesitan espacio en su propio vuelo.

Cada pareja elegida aporta $c_{av}$ al costo. No multiplicamos por pasajeros,
porque la tarifa dada ya cubre operar el vuelo completo.

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

## Problema 4 · Una asignación no está autorizada

::: exercise {#opt-b-vuelos-ej-autorizaciones title="Espacio disponible no significa permiso"}
Conservamos el problema 3 y añadimos una condición: por una autorización de
operación, **A2 no puede realizar V1**. Todas las demás parejas están
autorizadas. Los requisitos de asientos siguen vigentes.

A1, A2 y A3 tienen 100, 150 y 180 asientos utilizables. V1, V2 y V3 tienen
70, 100 y 140 pasajeros con reservación, respectivamente; todos deben viajar.
Los aviones están disponibles en el mismo aeropuerto y los vuelos salen de
él en una misma franja. Cada avión realiza como máximo un vuelo y cada vuelo
recibe exactamente un avión, sin cancelaciones ni pasajeros repartidos.

Los costos totales por pareja, en **miles de pesos**, siguen siendo:

| Avión | V1 | V2 | V3 |
|---|---:|---:|---:|
| A1 | 18 | 24 | 30 |
| A2 | 23 | 26 | 35 |
| A3 | 26 | 30 | 33 |

Un avión sin asignación no aporta costo y no hay otras condiciones de operación.
**Escribe el modelo completo para minimizar el costo.** Debe poder representar
más aviones, vuelos y parejas sin autorización.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-b-vuelos-pista-autorizaciones-datos of="opt-b-vuelos-ej-autorizaciones" title="PISTA 1 · Solo si te atoraste"}
| Dato | Información del relato |
|---|---|
| Asientos de A1, A2, A3 | 100, 150, 180 |
| Pasajeros de V1, V2, V3 | 70, 100, 140 |
| Por vuelo | Exactamente un avión |
| Por avión | Como máximo un vuelo |
| Nueva prohibición | A2 no puede realizar V1 |
| Demás parejas | Autorizadas; también deben cumplir la capacidad |

Los costos son los de la tabla del enunciado, en miles de pesos por vuelo completo.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-b-vuelos-pista-autorizaciones-guia of="opt-b-vuelos-ej-autorizaciones" title="PISTA 2 · Solo si te atoraste"}
¿Tener suficientes asientos garantiza que una pareja avión–vuelo esté permitida?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-vuelos-resp-autorizaciones of="opt-b-vuelos-ej-autorizaciones" title="Respuesta · Distinguir un permiso de una decisión"}
**1. Nombrar el dato nuevo.** Para aviones $A$ y vuelos $V$, conservamos
asientos $s_a$, pasajeros $d_v$, costos $c_{av}$ y decisiones binarias $x_{av}$.
Añadimos $p_{av}\in\{0,1\}$: vale $1$ si la pareja está autorizada y $0$ si
está prohibida. **El permiso es un dato; la asignación es una decisión.**

**2. Traducir ambos casos.** Si $p_{av}=0$, queremos obligar a $x_{av}=0$.
Si $p_{av}=1$, queremos permitir cualquiera de sus valores binarios.
La condición $x_{av}\le p_{av}$ representa exactamente esos dos casos.

Las autorizaciones no cuentan asientos. Conservamos las condiciones de
cobertura, uso y capacidad, además del costo de todas las parejas elegidas.

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
