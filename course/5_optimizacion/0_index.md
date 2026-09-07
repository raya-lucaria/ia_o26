---
id: optimizacion
title: Modelado y optimización
nav_title: Optimización
summary: "Antes de resolver hay que plantear. Esta unidad enseña a leer un problema en palabras y escribirlo como matemáticas, y después a resolverlo."
status: ready
estimated_time: 1h17m
tags: [optimizacion, modelado, programacion-lineal]
---

# Modelado y optimización

**Optimizar es elegir la mejor opción entre las que se pueden.** Las dos mitades
de esa frase pesan lo mismo: hay que saber **cuáles se pueden**, y hay que saber
**qué significa mejor**. Escribir esas dos cosas con precisión es modelar, y es
lo más difícil del asunto.

[[complejidad|La unidad anterior]] terminó explicando por qué casi ningún problema
interesante se resuelve probando todas las opciones. Ésta empieza donde aquélla
dejó: si no puedes enumerar, tienes que **describir** —el conjunto de opciones y
el criterio— y dejar que un método recorra esa descripción por ti. La descripción
es el modelo.

::: figure {#opt-lienzo title="Las siete preguntas, en dos bloques"}
![Siete cajas numeradas en dos bloques: cuatro para construir el modelo y tres para revisarlo, con una flecha de regreso](_assets/opt-lienzo.svg)
:::

## Por qué esto está en un curso de inteligencia artificial

Porque es el paso que casi nadie enseña y todos necesitan. Un agente que decide
qué hacer está resolviendo un problema de optimización, lo diga o no: tiene un
conjunto de acciones posibles y un criterio para preferir unas sobre otras.

La parte que se estudia normalmente es el método —cómo buscar rápido—. La parte
que decide si el resultado sirve es la otra: **si el modelo dice lo que creías
que decía**. Un modelo mal planteado se resuelve perfectamente y da una respuesta
que nadie firmaría. Esta unidad pasa la mayor parte del tiempo ahí.

## La nave

Todo pasa en la misma nave, en un viaje largo, y cada clase es un episodio. La
tripulación decide qué fabricar, cómo repartir la potencia del reactor y qué
subir al módulo de descenso. Son tres problemas distintos y el mismo método:
leer, escribir, resolver, dudar de la respuesta.

## Qué vas a poder hacer al terminar la primera clase

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
el total de la primera clase ronda los **77 minutos**.

::: table {#opt-ruta title="Las cinco páginas de la primera clase"}
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

## Qué no cubre esta clase

Nada de esta clase resuelve un problema **sin dibujarlo**, y el dibujo solo
funciona con dos variables. Tampoco aparecen aquí los problemas donde las
variables no se pueden partir, ni aquéllos donde el objetivo deja de ser una
recta. Los tres casos llegan después, y los tres se apoyan en lo que se plantea
aquí.

Empieza por [[leer-la-bitacora|leer la bitácora]].
