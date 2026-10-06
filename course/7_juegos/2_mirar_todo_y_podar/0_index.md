---
id: juegos-mirar-todo-y-podar
title: "Clase 2 · Mirar todo y podar"
nav_title: Mirar todo y podar
summary: "Calcular quién gana un juego que cabe completo: minimax desde los finales, nodos de azar que promedian y alfa-beta para no generar ramas que no cambian la respuesta."
status: ready
estimated_time: 110m
tags: [juegos, minimax, alfa-beta, algoritmos]
prerequisites: [juegos-leer-y-escribir]
---

# Clase 2 · Mirar todo y podar

**En la clase 1 jugaste tres partidas de hexapawn. Revísalas: ¿quién ganó?
¿Podía haber ganado el otro? Con nuestras reglas (quedarse sin jugada
pierde), ¿por qué quien juega segundo puede ganar siempre?** Al final de la
primera página tendrás la respuesta calculada, no adivinada.

La clase 1 escribió el juego; esta lo resuelve. Hexapawn cabe completo en la
memoria de una computadora, así que podemos **mirar todo** el árbol. Después
aprenderemos a **podar**: dejar ramas sin generar sin cambiar la respuesta.

## Qué vas a poder hacer al terminar esta clase

- Calcular a mano el valor de un árbol pequeño, desde los finales hacia la
  raíz, y separar el valor de la jugada que lo alcanza.
- Decir qué **recibe** y qué **genera** minimax: recibe las reglas
  ($S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$), no el grafo, y genera los
  estados mientras recorre.
- Explicar por qué minimax es correcto, por qué termina y cuánto cuesta.
- Valorar un árbol con nodos de azar y decir cuándo tratar el azar como un
  rival, o a un rival como azar, es un error de modelado.
- Ejecutar alfa-beta a mano, marcar cada corte y decir qué nodos nunca se
  generan.
- Explicar por qué los cortes son seguros y por qué el orden de las jugadas
  decide cuánto ahorra alfa-beta.

## El hilo de la clase

Todo pasa en el subgrafo de **n1**, el que dibujaste en
[[el-juego-como-grafo|El juego como grafo]]: trece estados, numerados en el
orden en que los visita minimax. La utilidad es la de la clase 1, $+1$ si
gana Blancas y $-1$ si gana Negras: aquí no cambia ninguna regla.

## Recorrido

Cinco páginas, en orden, y una tarea de refuerzo al final. Las cuatro de
algoritmos van en pares: primero **a mano**, con números, y después **como
algoritmo**, en general.

::: table {#jue-ruta-2 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Minimax a mano | Valorar n1 desde los finales y saber quién gana hexapawn | 25m |
| 2 | Minimax como algoritmo | Qué recibe, qué genera, por qué es correcto y cuánto cuesta | 25m |
| 3 | Cuando decide un dado | Qué cambia si un nodo no lo decide nadie | 15m |
| 4 | Alfa-beta a mano | Dos recorridos de n1 que no generan todos los nodos | 25m |
| 5 | Alfa-beta como algoritmo | Por qué los cortes son seguros y por qué el orden importa | 20m |
| 6 | Tarea de refuerzo | Resolver monedas en fila y hexapawn con empate | 45m, aparte |
:::

1. [[minimax|Minimax a mano]]
2. [[minimax-como-algoritmo|Minimax como algoritmo]]
3. [[cuando-decide-un-dado|Cuando decide un dado]]
4. [[alfa-beta|Alfa-beta a mano]]
5. [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]]
6. [[tarea-mirar-todo-y-podar|Tarea de refuerzo]]

## Qué no cubre esta clase

Aquí el árbol siempre cabe: llegamos a todos los finales. Qué hacer cuando
no se puede, como en el ajedrez, es la clase 3. Tampoco hay jugadas
simultáneas ni juegos donde los dos puedan ganar a la vez: eso es la
clase 4.

Empieza por [[minimax|minimax a mano]].
