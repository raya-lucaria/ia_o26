---
id: optimizacion-continua
title: "Clase 3 · Cuando ya no es una recta"
nav_title: Continuo
summary: "El reactor no rinde en línea recta: cada unidad extra de potencia sirve menos que la anterior. Qué se rompe, qué se salva, y cómo se reconoce el mejor reparto sin probarlos todos."
status: ready
estimated_time: 144m
tags: [optimizacion, convexidad, lagrange, kkt, gradiente]
prerequisites: [optimizacion-lineal]
---

# Clase 3 · Cuando ya no es una recta

Las dos primeras clases vivieron de una suposición que nadie nombró: que el
objetivo era una **recta**. Cuatro créditos por filtro, siempre cuatro, el
primero y el número ochenta. Casi nada en el mundo se comporta así.

Este episodio es el reactor, y ahí no hay recta que valga: la primera unidad de
potencia que recibe un sistema vale mucho, la décima casi nada. Con eso se cae el
teorema del vértice —el mejor reparto deja de estar en una esquina— y hay que
reconocer el óptimo por otra cosa.

Lo que **no** se cae es la garantía que de verdad importaba, la de que mirar
alrededor basta. Pero ya no se sostiene en la linealidad: se sostiene en la
**convexidad**, que es lo que esta clase nombra, define y demuestra.

## El episodio

El reactor reparte su potencia entre **escudos, motores y soporte vital**, y los
tres rinden cada vez menos por cada unidad extra. Cuánta potencia hay en total,
si se reparte entera o puede sobrar, y qué hacer con el tope del soporte vital
son **decisiones de modelado**: la bitácora no las deja cerradas, y la página 1
las toma una por una. Lo que el reactor le presta a la bodega para la impresora
va aparte y no se discute aquí.

::: table {#opt-el-reactor title="Los tres sistemas del reactor, y lo que rinde cada uno"}
| Sistema | Rinde | Su parámetro $b_i$ |
|---|---|---:|
| Escudos | $6p_1 - \tfrac12 p_1^2$ | 6 |
| Motores | $8p_2 - \tfrac12 p_2^2$ | 8 |
| Soporte vital | $10p_3 - \tfrac12 p_3^2$ | 10 |
:::

**Y cada unidad que le pones a un sistema rinde uno menos que la anterior.** Ésa
es toda la diferencia con las clases 1 y 2, y alcanza para cambiar el método
entero. (El $b_i$ de la tabla es la pendiente en cero, no lo que paga la primera
unidad: la página 1 explica la diferencia, que resulta importar.)

## Recorrido

Seis páginas, en orden. Cada una se sostiene sola y declara cuánto toma leerla;
el total de esta clase suma **144 minutos**.

::: table {#opt-ruta-continua title="Las seis páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | El rendimiento que decrece | Escribir el modelo del reactor, y qué se rompe cuando el objetivo se dobla | 26m |
| 2 | Sustituir y derivar | El primer método: quitar la restricción y derivar | 18m |
| 3 | El multiplicador | Encontrar el óptimo sin despejar, y qué mide el número de más | 28m |
| 4 | Los signos del lagrangeano | Cómo se escribe cada restricción y qué signo le toca | 28m |
| 5 | Resolver, paso a paso | El procedimiento completo, y el reactor resuelto con sus dos casos | 24m |
| 6 | Bajar la pendiente | Cuando no se puede resolver: dar pasos contra la pendiente | 20m |
:::

- [[el-rendimiento-que-decrece|1 · El rendimiento que decrece]]
- [[sustituir-y-derivar|2 · Sustituir y derivar]]
- [[el-multiplicador|3 · El multiplicador]]
- [[los-signos-del-lagrangeano|4 · Los signos del lagrangeano]]
- [[resolver-paso-a-paso|5 · Resolver, paso a paso]]
- [[bajar-la-pendiente|6 · Bajar la pendiente]]

**Si vas con poco tiempo**, las imprescindibles son la 1, la 4 y la 5: la primera
sostiene todo lo demás, la cuarta es la que más se equivoca, y la quinta es la que
de verdad se usa cuando te sientas a resolver algo.

## La tarea de esta clase

Son dos cosas, y las dos se entregan por **Canvas** antes de la sesión del
**lunes 21 de septiembre** (el miércoles 16 es descanso obligatorio y no hay
clase). En el sistema los grupos están separados, así que **cada quien entrega en
el suyo**:

- **COM-23101-003** → [entrega en Canvas](https://itam.instructure.com/courses/17744/assignments/228362)
- **COM-11308-003** → [entrega en Canvas](https://itam.instructure.com/courses/17950/assignments/228363)

### 1 · La unidad de Khan Academy sobre multiplicadores de Lagrange

Ve los videos y **haz los ejercicios** de la unidad de optimización con
restricciones:

[Multiplicadores de Lagrange y optimización con restricciones](https://es.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/lagrange-multipliers-and-constrained-optimization/v/constrained-optimization-introduction)
— Khan Academy, en español.

Cubre lo mismo que las páginas 3 y 4 por otro camino y con otra notación, que es
justo lo que conviene: si reconoces la misma idea escrita distinto, la
entendiste.

**Hay que tomarla y subir evidencia de haberla hecho.** Vale el certificado de
la unidad, una captura del progreso, una foto de la pantalla — lo que tengas. No
se evalúa la forma de la evidencia: se evalúa que la hiciste.

Si algo no te cuadra con lo que dice esta clase, anótalo y tráelo. La diferencia
casi siempre va a ser de **convención de signos**, y ya sabes exactamente dónde
mirar.

### 2 · Cómo se hace descenso de gradiente con restricciones

[[bajar-la-pendiente|La página 6]] cierra diciendo que el método **no respeta
restricciones**, y ahí se queda. Investiga por tu cuenta cómo se arregla en su
**versión más sencilla**, y súbelo a Canvas en media cuartilla: qué se le hace al
paso para que el punto no se salga del conjunto factible, cómo se llama eso, y
qué hace falta saber del conjunto para poder aplicarlo.

No tiene que ser exhaustivo ni formal. Tiene que estar entendido: con un dibujo
de dos variables y tres renglones alcanza.

## El notebook de la clase 3

Comprueba con `scipy` lo que las páginas calculan a mano: resuelve el reactor con
y sin la cota, construye $\lambda$ y $\mu_3$ desde la estacionariedad y verifica
las otras tres condiciones, contrasta el multiplicador contra la derivada
numérica del valor óptimo, y corre el descenso de gradiente con los tres tamaños
de paso, incluido el que oscila.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/6_optimizacion/_assets/03_reactor_continuo.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Dónde vive.** El archivo está en este repositorio, en
`course/6_optimizacion/_assets/03_reactor_continuo.ipynb`. Si prefieres correrlo
en tu máquina, necesitas `numpy`, `scipy` y `matplotlib`.

**Cuándo.** Después de leer las seis páginas.

## Qué no cubre esta clase

No vas a ver dualidad como teoría, ni condiciones de segundo orden, ni métodos
que usan la curvatura —Newton aparece en un renglón y nada más—, ni optimización
convexa con restricciones que no sean rectas y planos. Tampoco métodos que sí
respetan restricciones: el descenso de gradiente de aquí no las respeta, y la
página lo dice con todas sus letras.

Empieza por [[el-rendimiento-que-decrece|el rendimiento que decrece]].
