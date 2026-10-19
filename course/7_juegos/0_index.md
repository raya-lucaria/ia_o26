---
id: juegos
title: Jugar contra alguien que también piensa
nav_title: Juegos
summary: "Cómo decide una IA cuando otro agente también decide: escribir un juego, calcular la mejor jugada, estimarla cuando el juego no cabe y comparar todos los algoritmos en un mismo árbol."
status: ready
estimated_time: 11h34m
tags: [juegos, busqueda-adversarial, minimax, alfa-beta]
prerequisites: [optimizacion]
---

# Jugar contra alguien que también piensa

**Optimizar era elegir lo mejor entre lo que se puede. Ahora alguien más elige
después de ti, y quiere lo contrario.**

En [[opt-objetivo-juego-practica|el ejemplo del juego]] de la unidad de
optimización ya viste la idea central. En tu turno buscas el valor más alto.
En el del rival, suponemos que él busca el más bajo para ti. Aquel árbol
cabía en media página; esta unidad pregunta qué pasa cuando el juego crece.

## Por qué esto está en un curso de inteligencia artificial

[[agentes-ambientes|La unidad de agentes]] tenía una perilla para el número
de agentes. Cuando hay un rival, tu acción no basta para saber qué pasará:
también importa lo que él decida. Un agente así tiene que **modelar al otro
agente**, no solo al mundo.

Los juegos son el laboratorio clásico de esa idea. En 1997, Deep Blue venció
al campeón mundial de ajedrez con las herramientas de esta unidad. Buscaba
hacia delante, descartaba ramas sin revisarlas y estimaba las posiciones que
no podía terminar de calcular. Los sistemas modernos, como AlphaZero, cambian
cómo se estima, pero conservan la pregunta.

## El hilo de la unidad

Usamos un juego pequeño para todo: **hexapawn**, un «ajedrez» con solo
peones en un tablero de 3×3. Martin Gardner lo publicó en 1962 para mostrar
una máquina que aprende a jugar. Sus reglas caben en cuatro líneas y su árbol
completo se puede calcular.

Junto a él viven **tres árboles de juguete**, tan chicos que cada línea de un
algoritmo se sigue a mano:

- **El árbol reducido**, de siete nodos, para la primera poda de alfa-beta.
- **El árbol base**, con hojas de puntos del 2 al 12, para minimax, alfa-beta
  y los dados.
- **El árbol de resultados**, con finales $+1$, $0$ y $-1$, para el corte y
  los Monte Carlo; la clase 2 ya lo usa al cerrar cada algoritmo. En la
  radiografía lo corren todos.

No necesitas saber jugar ajedrez. El ajedrez aparece solo como comparación:
es el juego real que **no** cabe. Por eso los programas que lo juegan tienen
que estimar.

**Cada clase cambia una sola cosa**, y ese cambio obliga a una herramienta
nueva. La tabla de la sección siguiente lo resume.

## Las clases

::: table {#jue-clases title="Las clases de la unidad"}
| Sección | Qué cambia | Qué trabaja | Minutos |
|---|---|---|---:|
| 1 | Pasamos de unas reglas en palabras a un modelo | Ordenar unas reglas confusas, escribir el juego, construir su grafo, diagnosticarlo y definir $V$ y $Q$ | 121m |
| 2 | El juego cabe completo | Calcular la mejor jugada con minimax, podar con alfa-beta y promediar dados con expectiminimax | 203m |
| 3 | El juego ya no cabe | Cortar y evaluar, decidir hasta dónde mirar, simular partidas, MCTS con UCT y de dónde sale su bono | 280m |
| 4 | Nada en el juego: se comparan los algoritmos | Los siete algoritmos en un mismo árbol: qué número da cada uno, qué juega y cuánto cuesta; y cómo elegir uno | 90m |
:::

- [[juegos-leer-y-escribir|Clase 1 · Leer y escribir el juego]]
- [[juegos-mirar-todo-y-podar|Clase 2 · Mirar todo y podar]]
- [[juegos-cuando-no-cabe|Clase 3 · Cuando el árbol no cabe]]
- [[juegos-radiografia|Radiografía de los algoritmos]]: **de consulta**,
  para volver a ella en cualquier momento.

El recorrido de lectura suma **11 horas y 34 minutos**.

Las clases 1 a 3 terminan con una **tarea de refuerzo**. Trae ejercicios con
pistas y respuestas plegadas, sobre juegos nuevos y sobre variantes de lo
que ya viste. Las tres tareas suman unas **3 horas más**. No se entregan;
sirven para comprobar que puedes hacerlo sin ayuda.

## Antes de empezar: el video

Una clase del MIT sobre juegos, minimax y alfa-beta:

[6. Search: Games, Minimax, and Alpha-Beta](https://www.youtube.com/watch?v=STjW3eH0Cik)
— MIT 6.034, *Artificial Intelligence*, con Patrick Winston. **Menos de una
hora, en inglés**; los subtítulos automáticos ayudan si los necesitas.

**Una de las ideas del título ya la tienes.** El video llama *minimax* a lo
que hiciste en el ejemplo del juego de la unidad de optimización. Son máximos
en tus turnos y mínimos en los del rival. Lo nuevo es *alfa-beta*, que la
clase 2 desarrolla paso a paso. También la *profundización progresiva*, que
en la clase 3 llamamos **profundización iterativa**.

No necesitas entenderlo todo la primera vez. Párala cuando reconozcas algo
de la unidad de optimización y anota lo que todavía no tiene nombre para ti.

### Con qué llegas a clase

Pudiendo explicar con tus palabras, sin leerlas:

1. Por qué un programa de ajedrez no puede revisar todas las partidas.
2. Qué hace minimax en un turno tuyo y en uno del rival.
3. Qué idea usa alfa-beta para dejar de revisar una rama.
4. Una cosa del video que **no** esté en estas páginas. Y una de estas
   páginas que **no** esté en el video.

No hay cuestionario ni nada que entregar.

## El proyecto de la unidad

La unidad cierra con un proyecto en equipos de 2: un bot que juega
*Breakthrough de combate*, un juego de peones con dados, en una liga contra
los bots del grupo y los nuestros. Qué es, cómo empezar, qué se entrega y
cómo se califica: [[proyecto-torneo-adversarial|el proyecto]].

Y dos hojas de consulta, aparte del recorrido:

- [[notacion-juegos|Toda la notación, en una hoja]]: cada símbolo de la
  unidad, cómo se lee y dónde se presentó.
- [[animaciones-juegos|Las animaciones de la unidad]]: cada algoritmo
  corriendo línea por línea, con el pseudocódigo, la pila y el árbol a la
  vez, y qué mirar en cada una.

Empieza por [[juegos-leer-y-escribir|la clase 1]].
