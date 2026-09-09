---
id: optimizacion
title: Modelado y optimización
nav_title: Optimización
summary: "Antes de resolver hay que plantear. Esta unidad enseña a leer un problema en palabras y escribirlo como matemáticas, y después a resolverlo."
status: ready
estimated_time: 3h05m
tags: [optimizacion, modelado, programacion-lineal]
---

# Modelado y optimización

**Optimizar es elegir la mejor opción entre las que se pueden.** Las dos mitades
de esa frase pesan lo mismo: hay que saber **cuáles se pueden**, y hay que saber
**qué significa mejor**. Escribir esas dos cosas con precisión es modelar, y es
lo más difícil del asunto.

[[agentes-ambientes|La unidad anterior]] enseñó a dibujar una decisión: quién
decide, qué observa, qué puede hacer y cómo se juzgan las consecuencias. Y cerró
con siete propiedades para diagnosticar el entorno. Ésta empieza cuando esas
siete salen en su combinación más simple —lo ves todo, no hay azar, nada se mueve
mientras piensas— porque entonces la decisión deja de ser un problema de agentes
y se vuelve uno de **cuentas**.

Cuentas que no se pueden hacer probando todas las opciones: eso lo cerró
[[complejidad|la unidad de complejidad]]. Si no puedes enumerar, tienes que
**describir** —el conjunto de opciones y el criterio— y dejar que un método
recorra esa descripción por ti. La descripción es el modelo.

::: figure {#opt-lienzo title="Las siete preguntas, en dos bloques"}
![Siete cajas numeradas en dos bloques: cuatro para construir el modelo y tres para revisarlo, con una flecha de regreso](_assets/opt-lienzo.svg)
:::

## Por qué esto está en un curso de inteligencia artificial

Porque es el paso que casi nadie enseña y todos necesitan. Un agente que decide
qué hacer está resolviendo un problema de optimización, lo diga o no: el espacio
de acciones de su [[entorno-en-peas|especificación PEAS]] es el conjunto
factible, y su medida de desempeño es la función objetivo. Esta unidad les pone
nombre y método.

La parte que se estudia normalmente es el método —cómo buscar rápido—. La parte
que decide si el resultado sirve es la otra: **si el modelo dice lo que creías
que decía**. Un modelo mal planteado se resuelve perfectamente y da una respuesta
que nadie firmaría. Esta unidad pasa la mayor parte del tiempo ahí.

## La nave

Todo pasa en la misma nave, en un viaje largo, y cada clase es un episodio. La
tripulación decide qué fabricar, cómo repartir la potencia del reactor y qué
subir al módulo de descenso. Son tres problemas distintos y el mismo método:
leer, escribir, resolver, dudar de la respuesta.

## Las clases

Cada clase vive en su propio directorio, con su portada, sus páginas y su
tiempo estimado.

::: table {#opt-clases title="Las clases de la unidad"}
| Clase | Título | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Leer y escribir | Leer un problema real, escribirlo como matemáticas y dibujar la respuesta | 77m |
| 2 | Resolver sin dibujar | Escribir el modelo como matriz y resolverlo con simplex sin dibujarlo | 108m |
:::

Las clases 3 y 4 —el caso continuo y los problemas con variables enteras— están
en preparación.

- [[leer-y-escribir|Clase 1 · Leer y escribir]]
- [[optimizacion-lineal|Clase 2 · Resolver sin dibujar]]

Empieza por [[leer-y-escribir|la clase 1]].
