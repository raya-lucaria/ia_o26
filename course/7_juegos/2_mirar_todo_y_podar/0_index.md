---
id: juegos-mirar-todo-y-podar
title: "Clase 2 · Mirar todo y podar"
nav_title: Mirar todo y podar
summary: "Calcular quién gana un juego que cabe completo: minimax desde los finales, nodos de azar que promedian y alfa-beta para descartar ramas sin revisarlas."
status: ready
estimated_time: 97m
tags: [juegos, minimax, alfa-beta, algoritmos]
prerequisites: [juegos-leer-y-escribir]
---

# Clase 2 · Mirar todo y podar

**En la clase 1 jugaste tres partidas de hexapawn. Revisa tus tres
partidas: ¿quién ganó? ¿Podía haber ganado el otro? Con nuestras reglas
(quedarse sin jugada pierde), ¿por qué quien juega segundo puede ganar
siempre?** Al final de la primera página tendrás la
respuesta calculada, no adivinada.

La clase 1 escribió el juego; esta lo resuelve. Hexapawn cabe completo en la
memoria de una computadora, así que podemos **mirar todo** el árbol. Después
aprenderemos a **podar**: dejar ramas sin revisar sin cambiar la respuesta.

## Qué vas a poder hacer al terminar esta clase

- Calcular a mano el valor minimax de un árbol pequeño, desde los finales
  hacia la raíz.
- Distinguir el valor de una posición de la jugada que lo alcanza.
- Explicar por qué minimax es correcto y cuánto cuesta en tiempo y memoria.
- Valorar un árbol con nodos de azar, y decir cuándo tratar el azar como un
  rival es un error de modelado.
- Ejecutar alfa-beta a mano, señalar cada corte y justificar por qué es
  seguro.
- Explicar por qué el orden de las jugadas decide cuánto ahorra alfa-beta.

## Recorrido

Cuatro páginas, en orden, y una tarea de refuerzo al final.

::: table {#jue-ruta-2 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Minimax a mano | Cómo se calcula el valor de un árbol finito y quién gana hexapawn | 20m |
| 2 | Minimax como algoritmo | El procedimiento general, por qué es correcto y cuánto cuesta, con un caso para resolver solo | 25m |
| 3 | Cuando decide un dado | Qué cambia si un nodo no lo decide nadie | 12m |
| 4 | Alfa-beta | Cómo descartar ramas sin revisarlas y sin cambiar la respuesta | 40m |
| 5 | Tarea de refuerzo | Resolver monedas en fila y un juego de dado | 45m, aparte |
:::

1. [[minimax|Minimax a mano]]
2. [[minimax-como-algoritmo|Minimax como algoritmo]]
3. [[cuando-decide-un-dado|Cuando decide un dado]]
4. [[alfa-beta|Alfa-beta]]
5. [[tarea-mirar-todo-y-podar|Tarea de refuerzo]]

## Qué no cubre esta clase

Aquí el árbol siempre cabe: llegamos a todos los finales. Qué hacer cuando
no se puede, como en el ajedrez, es la clase 3. Tampoco hay jugadas
simultáneas ni juegos donde los dos puedan ganar a la vez: eso es la
clase 4.

Empieza por [[minimax|minimax a mano]].
