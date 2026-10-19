---
id: markov
title: Cadenas de Markov
nav_title: Markov
summary: "Un modelo de qué sigue que solo mira el estado actual: qué es una cadena de Markov, cómo se ajusta contando en un texto, cómo predice y cómo genera."
status: ready
estimated_time: 160m
tags: [markov, probabilidad, cadenas]
prerequisites: [juegos]
---

# Cadenas de Markov

**En español, después de una «q» casi siempre viene una «u». ¿Cuánto de un
texto se explica mirando solo la letra anterior, y qué se puede hacer con
eso?**

En [[cuando-decide-un-dado|Cuando decide un dado]] ya usaste una
probabilidad dentro de un modelo. Ahí, $\Pr(a\mid s)$ decía qué tan probable
era cada resultado del dado en el estado $s$. Y en
[[de-consecuencias-a-refuerzo|De consecuencias a refuerzo]] apareció una $P$
que decía a qué estado lleva el ambiente. Esta unidad toma esa $P$ y la
estudia sola: **qué sigue, si lo único que importa es dónde estás ahora**.

## Por qué esto está en un curso de inteligencia artificial

Un agente que vive en un ambiente con azar necesita un modelo de **qué
pasará después**. El más sencillo es una cadena de Markov. Es una tabla:
para cada estado, con qué probabilidad sigue cada otro. Con ella se
predice, se simula y se genera.

Y es una de las ideas más viejas para estudiar el lenguaje con números. En
1913, Andréi Markov contó a mano vocales y consonantes en un poema ruso.
Quería mostrar que cada letra depende de la anterior. En 1948, Claude
Shannon usó la misma idea para escribir texto «parecido al inglés».

## El hilo de la unidad

El hilo es **texto**: el *Quijote* completo, con 1 620 532 letras. Para
seguir cada cuenta a mano usamos una frase suya, **«Con la iglesia hemos
dado, Sancho»**. Tiene solo dos estados: vocal y consonante.

El juguete existe para trazar. Cada idea se dice después en general, con
$k$ estados y cualquier alfabeto. Y se corre en el libro completo.

## Las clases

::: table {#mkv-clases title="Las clases de la unidad"}
| Sección | Qué cambia | Qué trabaja | Minutos |
|---|---|---|---:|
| 1 | La cadena se ve | Probabilidad que se necesita, el problema de Markov, ajustar contando, predecir y generar texto | 160m |
:::

- [[markov-que-es-una-cadena|Clase 1 · Qué es una cadena]]

El recorrido de lectura suma **2 horas y 40 minutos**.

Y una hoja de consulta, aparte del recorrido:

- [[notacion-markov|Toda la notación, en una hoja]]: cada símbolo de la
  unidad, cómo se lee y dónde se presentó.

Empieza por [[markov-que-es-una-cadena|la clase 1]].
