---
id: juegos-sin-turnos
title: "Clase 4 · Cuando no hay turnos"
nav_title: Sin turnos
summary: "Cuando los dos eligen a la vez, ninguna jugada fija es segura: hay que mezclar. Elegir la mejor mezcla es un programa lineal, y deja de servir cuando el juego no es de suma cero."
status: ready
estimated_time: 80m
tags: [juegos, estrategias-mixtas, programacion-lineal]
prerequisites: [juegos-cuando-no-cabe]
---

# Clase 4 · Cuando no hay turnos

**Aquí se deja el tablero.** En hexapawn cada jugador veía la jugada del otro
antes de mover. En esta clase los dos eligen **a la vez**, y esa sola
diferencia rompe el árbol: ya no hay un turno de MAX seguido de uno de MIN.

El modelo nuevo es una tabla de pagos, y la herramienta para resolverla ya la
conoces: un programa lineal como los de la unidad de optimización. Al final
de la clase verás también cuándo esa herramienta deja de ser la adecuada.

## Qué vas a poder hacer al terminar esta clase

- Escribir un juego simultáneo como una tabla de pagos y calcular qué
  asegura cada jugada fija.
- Reconocer cuándo una tabla tiene punto de silla y cuándo hay que mezclar.
- Calcular qué garantiza una estrategia mixta.
- Escribir la mejor mezcla como programa lineal, resolverla con un dibujo si
  hay dos acciones y explicar por qué con más acciones se usa simplex.
- Encontrar mejores respuestas y equilibrios de Nash puros en una tabla que
  no es de suma cero.
- Explicar por qué suponer un rival hostil es un error de modelado cuando sus
  intereses no son los opuestos de los tuyos.

## Recorrido

Tres páginas, en orden, y una tarea de refuerzo al final.

::: table {#jue-ruta-4 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Jugar a la vez | Qué cambia si el rival no ve tu jugada, y por qué conviene mezclar | 25m |
| 2 | Maximin como programa lineal | Cómo se elige la mejor mezcla, con dibujo y sin él | 35m |
| 3 | Cuando no es suma cero | Qué pasa si lo que gana uno no es lo que pierde el otro | 20m |
| 4 | Tarea de refuerzo | Modelar el saque en tenis y diagnosticar el juego de la gallina | 50m, aparte |
:::

1. [[jugar-a-la-vez|Jugar a la vez]]
2. [[maximin-como-programa-lineal|Maximin como programa lineal]]
3. [[cuando-no-es-suma-cero|Cuando no es suma cero]]
4. [[tarea-sin-turnos|Tarea de refuerzo]]

## Qué no cubre esta clase

No aprenderás a calcular equilibrios en general: solo los puros de tablas
pequeñas, y las mezclas de juegos de suma cero. Tampoco aparecen juegos que
se repiten muchas veces, juegos con información oculta, como el póker, ni
juegos de más de dos jugadores. Cada uno de esos temas pide otro modelo.

Empieza por [[jugar-a-la-vez|jugar a la vez]].
