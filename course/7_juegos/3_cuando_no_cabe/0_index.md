---
id: juegos-cuando-no-cabe
title: "Clase 3 · Cuando el árbol no cabe"
nav_title: Cuando no cabe
summary: "Si no se puede llegar a los finales, se corta la búsqueda y se estima cada posición. La jugada que sale ya no es segura, y hay que entregarla antes de que se acabe el tiempo."
status: ready
estimated_time: 145m
tags: [juegos, busqueda-adversarial, evaluacion]
prerequisites: [juegos-mirar-todo-y-podar]
---

# Clase 3 · Cuando el árbol no cabe

**En la clase 2, alfa-beta resolvió hexapawn completo. ¿Cuántos nodos
tendría el árbol si el tablero fuera de 4×4? ¿Y en ajedrez?** En la primera
página verás que ya no se puede llegar a los finales: hay que detenerse
antes y **estimar**.

> [!TIP]
> **Esta clase tiene animaciones y un notebook.** Minimax con corte y profundización iterativa, corriendo en el árbol T:
>
> - **▶ Animaciones paso a paso:** [corte](../_assets/traza_arbol_t.html#corte) · [iterativa](../_assets/traza_arbol_t.html#iterativa). Cada página de
>   algoritmo abre la suya en un recuadro como éste.
> - **Notebook en Colab:** el mismo Python de las páginas, con el árbol dibujado en cada paso.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## Lo que traes de la clase 2

Todo lo que usa esta clase, en una tabla. Si un renglón no te suena, vuelve
a su página.

::: table {#jue-c3-repaso title="Lo que se usa de la clase 2"}
| | Qué es | Dónde se vio |
|---|---|---|
| $V(s)$ | El valor: lo que MAX asegura desde $s$ si MIN es racional | Minimax a mano |
| DECIDIR-MINIMAX | Elige la jugada de la raíz con el máximo de $V$ | Minimax como algoritmo |
| Árbol T | Juguete: R de MAX; I, C, D de MIN; C1 y C2 de MAX; hojas 3, 6 · 5, 2 · 7, 8 · 2, 12 | Minimax como algoritmo |
| $b$, $m$ | Ramificación y profundidad máxima; minimax genera del orden de $b^m$ nodos | Minimax como algoritmo |
| $\alpha$, $\beta$ | Lo que MAX y MIN ya tienen asegurado en el camino | Alfa-beta a mano |
| Corte | Dejar de generar hermanos que no cambian la respuesta | Alfa-beta a mano |
| Cota | Lo que devuelve un nodo que cortó: «al menos» o «a lo más», no su valor | Alfa-beta a mano |
| DECIDIR-ALFA-BETA | Minimax con cortes; el orden de las jugadas cambia cuántos nodos genera | Alfa-beta como algoritmo |
:::

Las páginas de la clase 2:
[[minimax|Minimax a mano]] ·
[[minimax-como-algoritmo|Minimax como algoritmo]] ·
[[alfa-beta|Alfa-beta a mano]] ·
[[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]].

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

Dos ejemplos, cada uno con su papel:

- **Una posición de peones de 4×4**, para las ideas. A profundidad 1 se
  elige ahí una jugada que pierde, y cada página muestra una manera
  distinta de no caer en eso.
- **El árbol T de la clase 2**, para los algoritmos: es tan chico que cada
  línea del pseudocódigo se sigue a mano.

## Recorrido

Cinco páginas, en orden. Las dos primeras van en par, como en la clase 2:
primero **a mano** y después **como algoritmo**.

::: table {#jue-ruta-3 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Cortar y evaluar a mano | Cortar la búsqueda y estimar, a profundidad 1, 2 y 3 | 30m |
| 2 | Minimax con corte como algoritmo | Qué recibe, qué jugada devuelve, qué garantiza y cuánto cuesta | 40m |
| 3 | Más allá del horizonte | Por qué un corte fijo engaña, y buscar más donde hay capturas | 20m |
| 4 | Jugar contra el reloj | Qué jugada entregar cuando se acaba el tiempo | 35m |
| 5 | Simular en vez de evaluar | Estimar con partidas al azar, sin escribir una evaluación | 20m |
| 6 | Tarea de refuerzo | Proponer y usar una evaluación de gato, y otra posición de peones | 50m, aparte |
:::

1. [[cortar-y-evaluar|Cortar y evaluar a mano]]
2. [[minimax-con-corte|Minimax con corte como algoritmo]]
3. [[mas-alla-del-horizonte|Más allá del horizonte]]
4. [[jugar-contra-el-reloj|Jugar contra el reloj]]
5. [[simular-en-vez-de-evaluar|Simular en vez de evaluar]]

## Las animaciones y el notebook

Los mismos de la clase 2, con dos secciones más: minimax con corte y
profundización iterativa, en el árbol T. No se cuentan en el tiempo de la
clase.

- [La animación con corte](../_assets/traza_arbol_t.html#corte): cambia $d$ entre
  1, 2 y 3.
- [La animación de la profundización iterativa](../_assets/traza_arbol_t.html#iterativa): las
  tres búsquedas seguidas.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

*Se abre en Google Colab, en otra pestaña. Las secciones 6 y 7 son las de esta
clase.*

## Qué no cubre esta clase

- **MCTS** solo se presenta: su idea, sus cuatro pasos y su regla de
  selección, que calculas una vez con números. No escribimos su
  pseudocódigo.
- **AlphaGo y AlphaZero** se mencionan, no se desarrollan.
- **La evaluación** la escribimos a mano; no la aprendemos de partidas.
- **La búsqueda de quietud** se explica con un ejemplo, sin sus detalles
  de implementación.

Empieza por [[cortar-y-evaluar|cortar y evaluar a mano]].
