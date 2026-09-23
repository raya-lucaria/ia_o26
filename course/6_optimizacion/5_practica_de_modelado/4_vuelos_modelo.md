---
id: opt-modelo-vuelos
title: "Cómo asignar aviones respetando capacidad y permisos"
nav_title: "Vuelos: modelo general"
summary: "Asignar un recurso completo a cada servicio, con exclusividad, capacidad y autorizaciones, en forma estándar."
status: ready
tags: [optimizacion, modelado, entera, practica]
---

# Cómo asignar aviones respetando capacidad y permisos

Antes de continuar, intenta los [[opt-practica-vuelos|dos problemas de vuelos]].
En ambos elegimos qué avión realizará cada vuelo. La asignación debe cumplir
las condiciones de operación y tener el menor costo posible.

Aquí construiremos esa formulación paso a paso. La misma estructura sirve
para asignar vehículos a recorridos o máquinas a tareas, cuando cada recurso
atiende como máximo un servicio.

## 1 · Decidir qué avión realiza cada vuelo

- $A,V$: Conjuntos finitos no vacíos de aviones y vuelos.
- $s_a\in\mathbb Z_{\ge0}$: Asientos utilizables del avión $a$.
- $d_v\in\mathbb Z_{\ge0}$: Pasajeros que deben viajar en el vuelo $v$.
- $c_{av}\ge0$: Costo total de operar esa pareja, en miles de pesos.

Saber que usamos un avión no dice **en qué vuelo**. Por eso definimos
$x_{av}\in\{0,1\}$: vale $1$ si asignamos el avión $a$ al vuelo $v$, y $0$
si no. Hay una variable por pareja; no representa pasajeros ni asientos.

Imagina una tabla: las filas son aviones y las columnas son vuelos. Cada
casilla contiene una decisión. **Todas las condiciones consultan esa misma tabla.**

## 2 · Calcular el costo y comprobar las condiciones

Una pareja elegida cuesta $c_{av}$; una no elegida aporta cero. El término
$c_{av}x_{av}$ expresa ambos casos. Sumamos todas las parejas:

$$\min\quad \sum_{a\in A}\sum_{v\in V}c_{av}x_{av}.$$

No multiplicamos por pasajeros: $c_{av}$ ya es el costo del vuelo completo.

Para escribir cada restricción, identifica primero **a quién se aplica la regla**.
Podemos comprobar la asignación vuelo por vuelo, avión por avión o pareja por
pareja. El índice de lo que estamos revisando se mantiene fijo.

**Cada vuelo recibe exactamente un avión.** Fijamos un vuelo $v$ y recorremos
su columna: sumamos las decisiones de todos los aviones que podrían atenderlo.
La suma cuenta los aviones asignados a ese vuelo, así que exigimos

$$\sum_{a\in A}x_{av}=1\qquad\text{para cada }v\in V.$$

**Cada avión realiza como máximo un vuelo.** Fijamos un avión $a$ y recorremos
su fila: sumamos las decisiones de todos los vuelos que podría realizar.
Cero significa dejarlo sin usar; uno significa asignarle un vuelo. No permitimos
una cuenta mayor porque los vuelos ocurren en la misma franja:

$$\sum_{v\in V}x_{av}\le1\qquad\text{para cada }a\in A.$$

Estas condiciones relacionan las elecciones. Al poner un uno en una casilla,
ocupamos el avión de su fila y cubrimos el vuelo de su columna. Esa decisión
limita qué podemos elegir en las demás casillas.

**Cada vuelo debe tener suficientes asientos.** El producto $s_ax_{av}$ aporta
los asientos del avión $a$ si lo elegimos para el vuelo $v$. Si no lo elegimos,
aporta cero. Sumando esos términos obtenemos los asientos asignados al vuelo,
que deben alcanzar para sus pasajeros:

$$\sum_{a\in A}s_ax_{av}\ge d_v\qquad\text{para cada }v\in V.$$

Esta interpretación depende de la primera condición: como cada columna tiene
exactamente un uno, contamos los asientos de **un solo avión**. Sin esa
condición, la suma podría reunir asientos de varios aviones para el mismo vuelo.

Tampoco basta comparar la capacidad total de la flota con el total de pasajeros.
Esa cuenta permitiría compensar los asientos que faltan en un vuelo con los que
sobran en otro, aunque los pasajeros no puedan cambiar de vuelo.

## 3 · Respetar las autorizaciones de operación

En el problema 4 conocemos otro dato: $p_{av}\in\{0,1\}$, que indica si la
pareja está autorizada. **El modelo elige la asignación, no el permiso.**
El objetivo y las variables $x_{av}$ permanecen iguales.

Queremos una regla que represente estos dos casos:

- **Sin permiso**, $p_{av}=0$: solo se admite $x_{av}=0$. La restricción debe
  impedir usar la pareja.
- **Con permiso**, $p_{av}=1$: se admite $x_{av}=0$ o $1$. La restricción debe
  permitir elegir la pareja, sin obligar a hacerlo.

Con el dominio binario, ambos casos se escriben como

$$x_{av}\le p_{av}\qquad\text{para cada }a\in A,\ v\in V.$$

Si el permiso es cero, la desigualdad y la no negatividad fuerzan cero.
Si es uno, queda el límite habitual de una variable binaria. Escribir una
igualdad obligaría a usar todas las parejas autorizadas.

Esta restricción **enlaza la decisión con un dato conocido**: los valores que
puede tomar $x_{av}$ dependen del permiso $p_{av}$. Revisar los casos cero y uno
permite comprobar que la condición acepta exactamente las decisiones permitidas.

No hace falta otra variable para «activar» el avión. La asignación ya decide
si se usa, y el relato no incluye un costo adicional por activarlo.

Conservamos la capacidad: tener permiso y tener asientos son requisitos
separados. Para representar el problema 3, tomamos todos los $p_{av}=1$.

## 4 · Reunir el modelo en forma estándar

Para escribir el modelo en forma estándar usaremos un objetivo de maximización,
restricciones con $\le$ y variables no negativas. Podemos llegar a esa escritura
sin cambiar qué asignaciones se permiten ni cuál tiene el menor costo.

Primero hacemos tres transformaciones:

1. **Maximizar el negativo del costo.** Un costo menor tiene un negativo mayor,
   así que esta escritura conserva la preferencia original.
2. **Expresar las condiciones con $\le$.** La cobertura exige a la vez como
   máximo un avión y como mínimo uno. Escribimos ambas desigualdades y cambiamos
   de signo la segunda. También cambiamos de signo ambos lados de la condición
   de capacidad, invirtiendo su sentido.
3. **Expresar el dominio binario.** Una variable entera, no negativa y como máximo
   uno solo puede valer cero o uno. Debemos conservar las tres exigencias.

Estas transformaciones conservan el significado de las condiciones de la
aerolínea. El modelo completo es:

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

Es un modelo de **programación lineal entera**: el objetivo y las restricciones
son lineales, y las variables deben tomar valores enteros.

El límite $x_{av}\le1$ hace explícito el dominio binario, aunque los permisos ya
lo implican. Mantener ambas filas permite reconocer cuál describe el dominio
y cuál viene de las autorizaciones.

## Qué razonamiento puedes reutilizar

**Decide la unidad de asignación; después escribe reglas por recurso, por
servicio y por pareja.** Más aviones o vuelos aumentan el número de variables
y restricciones, pero no cambian esa lógica.

Este modelo supone una sola franja, aviones disponibles en el mismo origen y
costos por pareja sin recargos por combinaciones. No describe conexiones ni
reutilización de aviones durante el día. Si faltan recursos, capacidad o
permisos, puede ser imposible cubrir todos los vuelos.

[[opt-practica-vuelos|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
