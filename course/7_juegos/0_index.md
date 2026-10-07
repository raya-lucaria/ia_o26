---
id: juegos
title: Jugar contra alguien que también piensa
nav_title: Juegos
summary: "Cómo decide una IA cuando otro agente también decide: escribir un juego, calcular la mejor jugada, estimarla cuando el juego no cabe y mezclar cuando los dos eligen a la vez."
status: ready
estimated_time: 6h30m
tags: [juegos, busqueda-adversarial, minimax, alfa-beta]
prerequisites: [optimizacion]
---

# Jugar contra alguien que también piensa

**Optimizar era elegir lo mejor entre lo que se puede. Ahora alguien más elige
después de ti, y quiere lo contrario.**

En [[opt-objetivo-juego-practica|el ejemplo del juego]] de la unidad de
optimización ya viste la idea central: en tu turno buscas el valor más alto,
y en el del rival suponemos que él busca el más bajo para ti. Aquel árbol
cabía en media página. Esta unidad pregunta qué pasa cuando el juego crece.

## Por qué esto está en un curso de inteligencia artificial

[[agentes-ambientes|La unidad de agentes]] tenía una perilla para el número
de agentes. Cuando hay un rival, tu acción no basta para saber qué pasará:
también importa lo que él decida. Un agente así tiene que **modelar al otro
agente**, no solo al mundo.

Los juegos son el laboratorio clásico de esa idea. En 1997, Deep Blue venció
al campeón mundial de ajedrez con las herramientas de esta unidad: buscar
hacia delante, descartar ramas sin revisarlas y estimar posiciones que no
puede terminar de calcular. Los sistemas modernos, como AlphaZero, cambian
cómo se estima, pero conservan la pregunta.

## El hilo de la unidad

Usamos un juego pequeño para todo: **hexapawn**, un «ajedrez» con solo
peones en un tablero de 3×3. Martin Gardner lo publicó en 1962 para mostrar
una máquina que aprende a jugar. Sus reglas caben en cuatro líneas y su árbol
completo se puede calcular.

No necesitas saber jugar ajedrez. El ajedrez aparece solo como comparación:
es el juego real que **no** cabe, y por eso los programas que lo juegan
tienen que estimar.

**Cada clase cambia una sola cosa**, y ese cambio obliga a una herramienta
nueva:

| Clase | Qué cambia | Herramienta |
|---|---|---|
| 1 | Pasamos de unas reglas en palabras a un modelo | Las siete piezas de un juego y su grafo |
| 2 | El juego cabe completo | Minimax, nodos de azar y alfa-beta |
| 3 | El juego ya no cabe | Corte de profundidad, función de evaluación y Monte Carlo |
| 4 | Los dos eligen a la vez | Estrategias mixtas y programación lineal |

## Las clases

::: table {#jue-clases title="Las clases de la unidad"}
| Sección | Título | Qué trabaja | Minutos |
|---|---|---|---:|
| 1 | Leer y escribir el juego | Ordenar unas reglas confusas, escribir el juego, construir su grafo y diagnosticarlo | 110m |
| 2 | Mirar todo y podar | Calcular la mejor jugada y descartar ramas sin generarlas | 110m |
| 3 | Cuando el árbol no cabe | Cortar la búsqueda, estimar posiciones, jugar contra el reloj y simular partidas | 90m |
| 4 | Cuando no hay turnos | Mezclar jugadas, escribirlo como programa lineal y reconocer cuándo no es suma cero | 80m |
:::

- [[juegos-leer-y-escribir|Clase 1 · Leer y escribir el juego]]
- [[juegos-mirar-todo-y-podar|Clase 2 · Mirar todo y podar]]
- [[juegos-cuando-no-cabe|Clase 3 · Cuando el árbol no cabe]]
- [[juegos-sin-turnos|Clase 4 · Cuando no hay turnos]]

El recorrido de lectura suma **6 horas y 30 minutos**. Cada clase termina
con una **tarea de refuerzo**: dos ejercicios con pistas y respuestas
plegadas, uno con un juego nuevo y otro que modifica o complementa lo que ya
viste. Las cuatro tareas suman unas **3 horas más**. No se entregan; sirven
para comprobar que puedes hacerlo sin ayuda.

## Antes de empezar: el video

Una clase del MIT sobre juegos, minimax y alfa-beta:

[6. Search: Games, Minimax, and Alpha-Beta](https://www.youtube.com/watch?v=STjW3eH0Cik)
— MIT 6.034, *Artificial Intelligence*, con Patrick Winston. **Menos de una
hora, en inglés**; los subtítulos automáticos ayudan si los necesitas.

**Una de las ideas del título ya la tienes.** El video llama *minimax* a lo
que hiciste en el ejemplo del juego de la unidad de optimización: máximos en
tus turnos y mínimos en los del rival. Lo nuevo es *alfa-beta*, que la clase 2
desarrolla paso a paso, y la *profundización progresiva*, que en la clase 3
llamamos **profundización iterativa**.

No necesitas entenderlo todo la primera vez. Párala cuando reconozcas algo
de la unidad de optimización y anota lo que todavía no tiene nombre para ti.

### Con qué llegas a clase

Pudiendo explicar con tus palabras, sin leerlas:

1. Por qué un programa de ajedrez no puede revisar todas las partidas.
2. Qué hace minimax en un turno tuyo y en uno del rival.
3. Qué idea usa alfa-beta para dejar de revisar una rama.
4. Una cosa del video que **no** esté en estas páginas, y una de estas páginas
   que **no** esté en el video.

No hay cuestionario ni nada que entregar.

Y una hoja de consulta, aparte del recorrido:

- [[notacion-juegos|Toda la notación, en una hoja]]: cada símbolo de la
  unidad, cómo se lee y dónde se presentó.

Empieza por [[juegos-leer-y-escribir|la clase 1]].
