---
id: juegos-cuando-no-cabe
title: "Clase 3 · Cuando el árbol no cabe"
nav_title: Cuando no cabe
summary: "Si no se puede llegar a los finales, se corta la búsqueda y se estima cada posición. La jugada que sale ya no es segura, y hay que entregarla antes de que se acabe el tiempo."
status: ready
estimated_time: 90m
tags: [juegos, busqueda-adversarial, evaluacion]
prerequisites: [juegos-mirar-todo-y-podar]
---

# Clase 3 · Cuando el árbol no cabe

**En la clase 2 el árbol cabía completo. Aquí deja de caber.** Agrandamos el
tablero de hexapawn a 4×4 y el árbol pasa de cientos de nodos a millones. El
ajedrez está muchísimo más lejos. Ya no se puede llegar a los finales:
hay que detenerse antes y **estimar**.

## Qué vas a poder hacer al terminar esta clase

- Explicar por qué minimax completo no sirve para un juego como el ajedrez.
- Escribir una función de evaluación y decir qué preferencia expresa y qué
  deja fuera.
- Calcular a mano minimax con corte de profundidad en una posición pequeña.
- Distinguir el valor con corte del valor exacto del juego.
- Reconocer el efecto horizonte y explicar qué hace la búsqueda de quietud.
- Explicar la profundización iterativa: qué jugada entregar cuando se acaba
  el tiempo y por qué repetir búsquedas cuesta poco.
- Explicar la idea de la búsqueda de árbol Monte Carlo: estimar una jugada
  simulando partidas al azar, sin función de evaluación.

La utilidad no cambia: sigue siendo la de las clases 1 y 2, $U=+1$ si gana
Blancas y $U=-1$ si gana Negras. Lo nuevo es lo que se hace cuando la
búsqueda se corta antes de llegar a un final.

## El hilo de la clase

Todo pasa en **una posición de peones de 4×4**, la misma en las cuatro
páginas. A profundidad 1 se elige ahí una jugada que pierde; cada página
muestra una manera distinta de no caer en eso.

## Recorrido

Cuatro páginas, en orden, y una tarea de refuerzo al final. Las dos
primeras van en par, como en la clase 2: primero **a mano** y después
**como algoritmo**.

::: table {#jue-ruta-3 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Cortar y evaluar a mano | Cortar la búsqueda y estimar, a profundidad 1, 2 y 3 | 25m |
| 2 | Minimax con corte como algoritmo | Qué recibe, qué genera, qué garantiza y cuánto cuesta | 20m |
| 3 | Jugar contra el reloj | Qué jugada entregar cuando se acaba el tiempo | 25m |
| 4 | Simular en vez de evaluar | Estimar con partidas al azar, sin escribir una evaluación | 20m |
| 5 | Tarea de refuerzo | Proponer y usar una evaluación de gato, y otra posición de peones | 50m, aparte |
:::

1. [[cortar-y-evaluar|Cortar y evaluar a mano]]
2. [[minimax-con-corte|Minimax con corte como algoritmo]]
3. [[jugar-contra-el-reloj|Jugar contra el reloj]]
4. [[simular-en-vez-de-evaluar|Simular en vez de evaluar]]
5. [[tarea-cuando-no-cabe|Tarea de refuerzo]]

## Qué no cubre esta clase

La búsqueda de árbol Monte Carlo (MCTS) solo se presenta: su idea, sus
cuatro pasos y su regla de selección, sin calcularla a mano ni escribir su
pseudocódigo. Tampoco desarrollamos AlphaGo ni AlphaZero. Tampoco aprendemos la función
de evaluación a partir de partidas; aquí la escribimos a mano. La búsqueda de
quietud se explica en un párrafo, sin sus detalles de implementación.

Empieza por [[cortar-y-evaluar|cortar y evaluar a mano]].
