---
id: opt-modelo-vuelos
title: "El modelo general de asignación"
nav_title: "Vuelos: modelo general"
summary: "Asignar un recurso completo a cada servicio, con exclusividad, capacidad y autorizaciones, en forma estándar."
status: ready
tags: [optimizacion, modelado, entera, practica]
---

# El modelo general de asignación

**Primero intenta los [[opt-practica-vuelos|dos problemas de vuelos]].**
La pregunta es: **¿qué avión atiende cada vuelo, cumpliendo las condiciones
al menor costo?** La misma estructura sirve para asignar vehículos a
recorridos o máquinas a tareas, cuando cada recurso atiende como máximo un servicio.

## 1 · Una decisión necesita dos índices

| Dato conocido | Significado |
|---|---|
| $A,V$ | Conjuntos finitos no vacíos de aviones y vuelos |
| $s_a\in\mathbb Z_{\ge0}$ | Asientos utilizables del avión $a$ |
| $d_v\in\mathbb Z_{\ge0}$ | Pasajeros que deben viajar en el vuelo $v$ |
| $c_{av}\ge0$ | Costo total de operar esa pareja, en miles de pesos |

Saber que usamos un avión no dice **en qué vuelo**. Por eso definimos
$x_{av}\in\{0,1\}$: vale $1$ si asignamos el avión $a$ al vuelo $v$, y $0$
si no. Hay una variable por pareja; no representa pasajeros ni asientos.

Imagina una tabla: las filas son aviones y las columnas son vuelos. Cada
casilla contiene una decisión. **Todas las condiciones consultan esa misma tabla.**

## 2 · Sumar costos y traducir cada obligación

Una pareja elegida cuesta $c_{av}$; una no elegida aporta cero. El término
$c_{av}x_{av}$ expresa ambos casos. Sumamos todas las parejas:

$$\min\quad \sum_{a\in A}\sum_{v\in V}c_{av}x_{av}.$$

No multiplicamos por pasajeros: $c_{av}$ ya es el costo del vuelo completo.

Para escribir las restricciones, identifica primero **a quién se aplica la
regla**. Ese índice se mantiene fijo; sumamos sobre las alternativas:

| Regla | Qué fijamos y qué sumamos | Restricción |
|---|---|---|
| Un avión por vuelo | Fijamos $v$ y recorremos los aviones de su columna | $\sum_{a\in A}x_{av}=1$ para cada $v$ |
| Como máximo un vuelo por avión | Fijamos $a$ y recorremos los vuelos de su fila | $\sum_{v\in V}x_{av}\le1$ para cada $a$ |
| Asientos suficientes en cada vuelo | Fijamos $v$ y contamos los asientos asignados | $\sum_{a\in A}s_ax_{av}\ge d_v$ para cada $v$ |

Las dos primeras condiciones **relacionan las elecciones**. Una casilla con
valor $1$ ocupa el avión de su fila y cubre el vuelo de su columna. No podemos
elegir las casillas de manera independiente.

La capacidad también depende de la cobertura: como cada columna tiene
exactamente un $1$, la suma de asientos corresponde a **un solo avión**.
Sin esa condición, podríamos sumar asientos de varios aviones para un vuelo.
Una capacidad total para todos los vuelos tampoco garantizaría espacio en cada uno.

## 3 · Añadir permisos sin añadir decisiones

En el problema 4 conocemos otro dato: $p_{av}\in\{0,1\}$, que indica si la
pareja está autorizada. **El modelo elige la asignación, no el permiso.**
El objetivo y las variables $x_{av}$ permanecen iguales.

Queremos una regla que represente estos dos casos:

| Permiso conocido | Asignaciones permitidas | Qué debe exigir la restricción |
|---|---|---|
| $p_{av}=0$ | Solo $x_{av}=0$ | Impedir usar la pareja |
| $p_{av}=1$ | $x_{av}=0$ o $1$ | Permitir elegirla, sin obligar a hacerlo |

Con el dominio binario, ambos casos se escriben como

$$x_{av}\le p_{av}\qquad\text{para cada }a\in A,\ v\in V.$$

Si el permiso es cero, la desigualdad y la no negatividad fuerzan cero.
Si es uno, queda el límite habitual de una variable binaria. Escribir una
igualdad obligaría a usar todas las parejas autorizadas.

**Esta es la idea del enlace:** una condición sobre una decisión debe
reflejar exactamente los casos permitidos. Aquí enlazamos una decisión con
un dato conocido. No hace falta otra variable para «activar» el avión:
la asignación ya decide si se usa, y no hay un costo adicional por activarlo.

Conservamos la capacidad: tener permiso y tener asientos son requisitos
separados. Para representar el problema 3, tomamos todos los $p_{av}=1$.

## 4 · Reunir el modelo en forma estándar

Hacemos tres cambios de escritura, sin cambiar las asignaciones permitidas:

- Maximizamos el **negativo** del costo para conservar la preferencia por el menor costo.
- Separamos la igualdad de cobertura en dos desigualdades; negamos la de capacidad para usar $\le$.
- Escribimos «binaria» como entero, no negativo y como máximo uno.

No son nuevas decisiones ni nuevas exigencias de la aerolínea. El modelo completo es:

$$
\begin{aligned}
\max\quad &-\sum_{a\in A}\sum_{v\in V}c_{av}x_{av}\\
\text{sujeto a}\quad
&\sum_{a\in A}x_{av}\le1 &&\text{para cada }v\in V,\\
&-\sum_{a\in A}x_{av}\le-1 &&\text{para cada }v\in V,\\
&\sum_{v\in V}x_{av}\le1 &&\text{para cada }a\in A,\\
&-\sum_{a\in A}s_ax_{av}\le-d_v &&\text{para cada }v\in V,\\
&x_{av}\le p_{av} &&\text{para cada }a\in A,\ v\in V,\\
&x_{av}\le1 &&\text{para cada }a\in A,\ v\in V,\\
&x_{av}\ge0,\quad x_{av}\in\mathbb Z
&&\text{para cada }a\in A,\ v\in V.
\end{aligned}
$$

Es **programación lineal entera**. El límite $x_{av}\le1$ hace explícito el
dominio binario, aunque los permisos ya lo implican. Mantener ambas filas
permite reconocer cuál describe el dominio y cuál viene de las autorizaciones.

## Qué razonamiento puedes reutilizar

**Decide la unidad de asignación; después escribe reglas por recurso, por
servicio y por pareja.** Más aviones o vuelos aumentan el número de variables
y restricciones, pero no cambian esa lógica.

Este modelo supone una sola franja, aviones disponibles en el mismo origen y
costos por pareja sin recargos por combinaciones. No describe conexiones ni
reutilización de aviones durante el día. Si faltan recursos, capacidad o
permisos, puede ser imposible cubrir todos los vuelos.

[[opt-practica-vuelos|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
