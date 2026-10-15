---
id: juegos-radiografia
title: Radiografía de los algoritmos
nav_title: Radiografía
summary: "Los siete algoritmos de la unidad en un mismo árbol pequeño: cómo explora cada uno, qué número da, qué jugada entrega y cuánto cuesta. Y cómo elegir el algoritmo para un juego nuevo."
status: ready
estimated_time: 90m
tags: [juegos, busqueda-adversarial, minimax, mcts]
prerequisites: [juegos-cuando-no-cabe]
---

# Radiografía de los algoritmos

**Ya viste cada algoritmo por separado. ¿En qué se parecen y en qué no?**

Esta sección es **de consulta**: vuelve a ella en cualquier momento. Pone
los algoritmos de las clases 2 y 3 sobre el árbol de resultados para
compararlos. Después usa esa comparación para elegir el algoritmo de un
juego. No tiene tarea.

## Lo que traes

- **De la clase 2:** minimax, alfa-beta y expectiminimax, que calculan $V$
  cuando el árbol cabe.
- **De la clase 3:** el corte con EVAL, la quietud, la profundización
  iterativa y los tres Monte Carlo, que estiman cuando no cabe.
- **El árbol de resultados**, con finales $+1$, $0$ y $-1$, donde ya corriste
  cada uno.

## El hilo

Un solo árbol para todos: el de resultados, con 15 nodos. Cada algoritmo
tiene ahí una ficha con el mismo orden, así que las diferencias saltan a la
vista. La segunda página da la vuelta: parte de un juego nuevo y elige.

## Qué vas a poder hacer al terminar

- Leer la ficha de cada algoritmo. Todas siguen el mismo orden: qué valor
  rastrea, cómo obtiene su número, qué juega, propiedades y casos borde.
- Decir si un número es $V$, un valor con corte o una estimación
  $\widehat Q$. Y a qué converge cada Monte Carlo.
- Elegir el algoritmo de un juego nuevo con cuatro preguntas. ¿Cabe el
  árbol? ¿Hay dados? ¿Hay una buena EVAL? ¿Hay reloj?

> [!TIP]
> **▶ [El mismo árbol, todos los algoritmos](../_assets/un_arbol_todos.html).** Elige un algoritmo. Mira qué nodos genera, qué jugada entrega y con qué valor.

## Recorrido

::: table {#jue-ruta-4 title="Las páginas de esta sección"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 60m | **Radiografía: un árbol, todos los algoritmos.** Siete fichas en el árbol de resultados y las tablas que los comparan |
| 2 | 30m | **Elegir el algoritmo.** Cuatro preguntas sobre el juego que deciden qué algoritmo usar, y lo que suponen todos |
:::

1. [[un-arbol-todos-los-algoritmos|Radiografía: un árbol, todos los algoritmos]]
2. [[elegir-el-algoritmo|Elegir el algoritmo]]

Empieza por [[un-arbol-todos-los-algoritmos|la radiografía]].
