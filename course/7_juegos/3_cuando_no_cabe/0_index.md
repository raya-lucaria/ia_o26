---
id: juegos-cuando-no-cabe
title: "Clase 3 · Cuando el árbol no cabe"
nav_title: Cuando no cabe
summary: "Si no se puede llegar a los finales, se corta la búsqueda y se estima cada posición. La jugada que sale ya no es segura, y hay que entregarla antes de que se acabe el tiempo."
status: ready
estimated_time: 75m
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

En esta clase la utilidad cambia: dejamos $10-k$ y usamos $U=\pm1$, porque
en el 4×4 solo importa quién gana y al cortar no sabemos cuántas jugadas
faltan. La primera página lo explica.

## Recorrido

Tres páginas, en orden, y una tarea de refuerzo al final.

::: table {#jue-ruta-3 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Cortar y evaluar | Qué hacer cuando no se puede llegar a los finales | 30m |
| 2 | Jugar contra el reloj | Qué jugada entregar cuando se acaba el tiempo | 30m |
| 3 | Simular en vez de evaluar | La otra respuesta: estimar con partidas al azar, sin escribir una evaluación | 15m |
| 4 | Tarea de refuerzo | Proponer y usar una evaluación de gato, y otra posición de peones | 50m, aparte |
:::

1. [[cortar-y-evaluar|Cortar y evaluar]]
2. [[jugar-contra-el-reloj|Jugar contra el reloj]]
3. [[simular-en-vez-de-evaluar|Simular en vez de evaluar]]
4. [[tarea-cuando-no-cabe|Tarea de refuerzo]]

## Qué no cubre esta clase

La búsqueda de árbol Monte Carlo (MCTS) solo se presenta: su idea, sus
cuatro pasos y su regla de selección, sin calcularla a mano ni escribir su
pseudocódigo. Tampoco desarrollamos AlphaGo ni AlphaZero. Tampoco aprendemos la función
de evaluación a partir de partidas; aquí la escribimos a mano. La búsqueda de
quietud se explica en un párrafo, sin sus detalles de implementación.

Empieza por [[cortar-y-evaluar|cortar y evaluar]].
