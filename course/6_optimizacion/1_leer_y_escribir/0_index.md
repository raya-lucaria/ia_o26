---
id: leer-y-escribir
title: "Clase 1 · Leer y escribir"
nav_title: Leer y escribir
summary: "Cómo se lee un problema real en palabras y se escribe como matemáticas, y qué clase de respuesta te entrega el dibujo."
status: ready
estimated_time: 77m
tags: [optimizacion, modelado]
prerequisites: [optimizacion]
---

# Clase 1 · Leer y escribir

Esta clase hace tres cosas, en orden: lee un problema real escrito con ruido,
huecos y frases ambiguas · lo escribe como matemáticas, con variables, función
objetivo y restricciones · y lo dibuja, para ver dónde vive la respuesta y por
qué cae siempre en una esquina. Termina viendo qué clase de cosa te entrega un
método, y cómo se traducen las frases que no hablan de un recurso.

## Qué vas a poder hacer al terminar esta clase

- Sacar una tabla de datos limpia de un texto con ruido, huecos y frases
  ambiguas, y **decir cuál es cuál**.
- Escribir un problema de optimización completo: variables con su dominio,
  función objetivo, restricciones.
- Dibujar la región factible de un problema de dos variables y encontrar la
  respuesta empujando una recta.
- Explicar **por qué** la respuesta está en una esquina, en vez de repetirlo.
- Distinguir un óptimo de una solución factible, de una cota y de un
  certificado.
- Traducir «al menos», «a lo más» y «por cada» sin equivocarte de signo.

## Recorrido

Cinco páginas, en orden. Cada una se sostiene sola y declara cuánto toma leerla;
el total de esta clase ronda los **77 minutos**, más la hoja de práctica del
final.

::: table {#opt-ruta title="Las cinco páginas de esta clase"}
| | Página | Qué resuelve | |
|---|---|---|---:|
| 1 | Leer la bitácora | Qué dice de verdad este problema | 15m |
| 2 | Escribir el modelo | Cómo se convierte una tabla en matemáticas | 18m |
| 3 | El dibujo | Dónde está la respuesta, y por qué en una esquina | 15m |
| 4 | Qué es una respuesta | Qué clase de cosa te entrega un método | 14m |
| 5 | Patrones lineales | Cómo se traduce una frase que no habla de un recurso | 15m |
:::

- [[leer-la-bitacora|1 · Leer la bitácora]]
- [[escribir-el-modelo|2 · Escribir el modelo]]
- [[el-dibujo|3 · El dibujo]]
- [[que-es-una-respuesta|4 · Qué es una respuesta]]
- [[patrones-lineales|5 · Patrones lineales]]

Y una hoja de práctica, aparte del recorrido:

- [[tres-bitacoras|Tres bitácoras para practicar]] — tres historias nuevas sin
  resolver, una por cada patrón, con la solución plegada. Unos 30 minutos.

## El notebook de la clase 1

Las páginas se leen; el notebook se corre. Trae el problema de la impresora resuelto con
código, el mismo dibujo hecho por la computadora, y **al final una historia nueva
para que la modeles tú**. No hay nada que entregar.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/6_optimizacion/_assets/01_impresora_lineal.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Dónde vive.** El archivo está en este repositorio, en
`course/6_optimizacion/_assets/01_impresora_lineal.ipynb`. El botón de arriba lo
abre en Google Colab, que lo ejecuta en el navegador sin instalar nada. Si
prefieres correrlo en tu máquina, necesitas `numpy`, `scipy` y `matplotlib`.

**Cuándo.** Después de leer las cinco páginas. La última celda da por sabidas
todas.

## Qué no cubre esta clase

Nada de esta clase resuelve un problema **sin dibujarlo**, y el dibujo solo
funciona con dos variables. Tampoco aparecen aquí los problemas donde las
variables no se pueden partir, ni aquéllos donde el objetivo deja de ser una
recta. El primero de los tres llega en la clase 2; los otros dos, después. Los
tres se apoyan en lo que se plantea aquí.

Empieza por [[leer-la-bitacora|leer la bitácora]].
