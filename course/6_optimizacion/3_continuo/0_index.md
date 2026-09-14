---
id: optimizacion-continua
title: "Clase 3 · Cuando ya no es una recta"
nav_title: Continuo
summary: "El reactor no rinde en línea recta: cada unidad extra de potencia sirve menos que la anterior. Qué se rompe, qué se salva, y cómo se reconoce el mejor reparto sin probarlos todos."
status: ready
estimated_time: 118m
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

El reactor reparte su potencia entre **escudos, motores y soporte vital**. Los
tres rinden cada vez menos por cada unidad extra, la potencia se reparte entera,
y el soporte vital tiene un tope. Lo que le presta a la bodega para la impresora
va aparte y no se discute aquí.

::: table {#opt-el-reactor title="El reparto del reactor, con 15 unidades de potencia por turno"}
| Sistema | Rinde | Lo que paga su primera unidad |
|---|---|---:|
| Escudos | $6p_1 - \tfrac12 p_1^2$ | 6 |
| Motores | $8p_2 - \tfrac12 p_2^2$ | 8 |
| Soporte vital | $10p_3 - \tfrac12 p_3^2$ | 10 |
:::

**Y cada unidad que le pones a un sistema rinde uno menos que la anterior.** Ésa
es toda la diferencia con las clases 1 y 2, y alcanza para cambiar el método
entero.

## Recorrido

Cinco páginas, en orden. Cada una se sostiene sola y declara cuánto toma leerla;
el total de esta clase suma **118 minutos**.

::: table {#opt-ruta-continua title="Las cinco páginas de esta clase"}
| | Página | Qué resuelve | |
|---|---|---|---:|
| 1 | El rendimiento que decrece | Escribir el modelo del reactor, y qué se rompe cuando el objetivo se dobla | 26m |
| 2 | Sustituir y derivar | El primer método: quitar la restricción y derivar | 16m |
| 3 | El multiplicador | Encontrar el óptimo sin despejar, y qué mide el número de más | 24m |
| 4 | Los signos del lagrangeano | Cómo se escribe cada restricción y qué signo le toca | 32m |
| 5 | Bajar la pendiente | Cuando no se puede resolver: dar pasos contra la pendiente | 20m |
:::

- [[el-rendimiento-que-decrece|1 · El rendimiento que decrece]]
- [[sustituir-y-derivar|2 · Sustituir y derivar]]
- [[el-multiplicador|3 · El multiplicador]]
- [[los-signos-del-lagrangeano|4 · Los signos del lagrangeano]]
- [[bajar-la-pendiente|5 · Bajar la pendiente]]

**Si vas con poco tiempo**, las imprescindibles son la 1 y la 4: la primera es la
que sostiene todo lo demás, y la cuarta es la que se usa en la práctica y la que
más se equivoca.

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

**Cuándo.** Después de leer las cinco páginas.

## Qué no cubre esta clase

No vas a ver dualidad como teoría, ni condiciones de segundo orden, ni métodos
que usan la curvatura —Newton aparece en un renglón y nada más—, ni optimización
convexa con restricciones que no sean rectas y planos. Tampoco métodos que sí
respetan restricciones: el descenso de gradiente de aquí no las respeta, y la
página lo dice con todas sus letras.

Empieza por [[el-rendimiento-que-decrece|el rendimiento que decrece]].
