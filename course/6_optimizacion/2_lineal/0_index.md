---
id: optimizacion-lineal
title: "Clase 2 · Resolver sin dibujar"
nav_title: Lineal
summary: "El dibujo se acaba en cuanto hay tres productos. Esta clase escribe el modelo como matriz y enseña el método que llega a la esquina correcta sin verla."
status: draft
estimated_time: 85m
tags: [optimizacion, programacion-lineal, simplex]
prerequisites: [leer-y-escribir]
---

# Clase 2 · Resolver sin dibujar

El dibujo se acaba en cuanto hay tres productos. La clase 1 resolvió todo
mirando un polígono; aquí el depósito agrega un tercer producto, el polígono se
vuelve poliedro, y con veinte productos nadie ha visto jamás la figura. Esta
clase escribe el modelo como una matriz, para que no le importe cuántas
columnas tenga, y enseña el método que llega a la esquina correcta
preguntándole solo a sus vecinos, sin necesidad de verla.

## El tercer producto

Este viaje, además de filtros y celdas, el depósito también compra **sellos de
vacío**: la impresora tiene un tercer molde cargado. El sello gasta lo mismo
que un filtro en horas de impresora y en polímero, pero el triple de energía —
y ese detalle es el que rompe el dibujo.

::: table {#opt-tres-piezas title="Los tres productos del viaje, con un renglón por recurso"}
| Recurso | Por filtro | Por celda | Por sello |
|---|---:|---:|---:|
| Horas de impresora | 1 | 1 | 1 |
| Polímero (kg) | 2 | 1 | 2 |
| Energía (kWh) | 1 | 2 | 3 |
| **Créditos que abona el depósito** | **4** | **3** | **5** |
:::

## Recorrido

Cinco páginas, en orden. Cada una se sostiene sola y declara cuánto toma
leerla; el total de esta clase ronda los **85 minutos**.

::: table {#opt-ruta-lineal title="Las cinco páginas de esta clase"}
| | Página | Qué resuelve | |
|---|---|---|---:|
| 1 | El modelo como matriz | Cómo se escribe el modelo sin que dependa de dos variables | 16m |
| 2 | Cuando se acaba el dibujo | Qué es un vértice cuando ya no hay dibujo que ver | 20m |
| 3 | De esquina en esquina | El primer método: caminar de vecino en vecino | 20m |
| 4 | Sin dibujo | El mismo método sobre un poliedro de tres dimensiones | 12m |
| 5 | Cuánto vale una hora más | Qué dice el óptimo sobre cada recurso | 17m |
:::

- [[el-modelo-como-matriz|1 · El modelo como matriz]]
- [[cuando-se-acaba-el-dibujo|2 · Cuando se acaba el dibujo]]
- [[de-esquina-en-esquina|3 · De esquina en esquina]]
- [[sin-dibujo|4 · Sin dibujo]]
- [[cuanto-vale-una-hora-mas|5 · Cuánto vale una hora más]]

## Qué no cubre esta clase

No vas a ver el cuadro de cálculo con que se enseña simplex a mano —aquí el
método camina por esquinas, que es la misma idea sin la contabilidad—, ni la
dualidad como teoría, ni qué hacer cuando el método se atora en un empate. Nada
de eso hace falta para lo que sigue.

Empieza por [[el-modelo-como-matriz|el modelo como matriz]].
