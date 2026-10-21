---
id: markov-a-la-larga
title: "Clase 2 · Qué pasa a la larga"
nav_title: Qué pasa a la larga
summary: "Qué hace una cadena de Markov si la dejas correr: clasificar sus estados, la distribución estacionaria y los cuatro teoremas que dicen cuándo olvida su inicio, el tiempo medio para terminar una partida de serpientes y escaleras, y PageRank."
status: ready
estimated_time: 181m
tags: [markov, probabilidad, cadenas, estacionaria, pagerank]
prerequisites: [markov-que-es-una-cadena]
---

# Clase 2 · Qué pasa a la larga

**Si dejas correr una cadena mucho tiempo, ¿qué puede pasar? ¿Y cuándo deja
de importar dónde empezó?** Al final tendrás cuatro teoremas que lo dicen.
Cada uno trae su condición y un ejemplo de qué se rompe sin ella. Y dos
usos: cuánto dura una partida de serpientes y escaleras, y cómo ordena
páginas PageRank.

## Lo que traes

Esta clase sigue a la clase 1. Si un renglón no te suena, vuelve a su página.

- **La matriz y los vectores.** En
  [[mkv-cadena-en-general|La cadena de Markov, en general]] la matriz $P$
  era $k\times k$, la distribución $\mu_t$ un vector fila, y
  $\mu_t=\mu_0P^t$.
- **Predecir paso a paso.** En [[mkv-predecir|Predecir]] viste que, en la
  matriz de la frase, $\mu_t$ desde V y desde C casi coincidían en el paso
  8. Ahí solo se observó; aquí se demuestra cuándo pasa.
- **La conjetura de la tarea.** El ejercicio que adelantaba esta clase
  comparó esa matriz con la que siempre cambia de estado. Una olvidaba su
  inicio y la otra no. La clase dice por qué.

## Qué vas a poder hacer al terminar esta clase

- **Clasificar los estados** de una cadena: clases, clases cerradas,
  transitorios y periodo.
- **Calcular la distribución estacionaria** resolviendo un sistema lineal o
  iterando, y decir cuándo es única.
- **Distinguir tres preguntas** que suenan igual: la probabilidad en el paso
  $t$, el límite y la fracción del tiempo. Y decir qué condición contesta
  cada una.
- **Calcular cuánto falta** para llegar a un conjunto de estados, en
  promedio, con un sistema lineal.
- **Explicar PageRank** como la estacionaria de una cadena arreglada para
  que los teoremas apliquen.

---

## El hilo de la clase

**Las páginas 1 a 3 son de conceptos,** sin simulación. La 1 da el álgebra
y los límites que faltan. La 2 clasifica estados. La 3 define la
estacionaria y enuncia los cuatro teoremas. Cada condición trae un
contraejemplo de dos o tres estados.

**Las páginas 4 a 6 los usan.** Cada idea se resuelve a mano en un juguete,
con un algoritmo que sirve para cualquier tamaño, y simulando. Los casos
grandes son el *Quijote*, un tablero de 100 casillas y los enlaces de
este curso.

## Recorrido

Seis páginas, en orden.

**Los minutos son de lectura.** Cada página cierra con uno o dos
ejercicios finales con pistas y respuesta plegadas: resolverlos toma
tiempo aparte, que no está en la tabla.

::: table {#mkv-ruta-2 title="Las páginas de esta clase"}
| # | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 31m | **Lo que necesitas de álgebra y límites.** Sistemas lineales, límites y tolerancia, valor esperado condicionando en el primer paso, y alcanzar en un grafo |
| 2 | 29m | **Clasificar los estados.** Comunicar, clases cerradas, transitorios, recurrentes y periodo |
| 3 | 34m | **La estacionaria y sus cuatro teoremas.** Las tres preguntas; cuándo existe, cuándo es única, cuándo converge y qué dice la fracción del tiempo |
| 4 | 27m | **¿Olvida su inicio?** La conjetura de la tarea resuelta: a mano, con la iteración de potencias y simulando, en la frase y en el *Quijote* |
| 5 | 28m | **Cuánto falta para terminar.** El tiempo medio de llegada con un sistema lineal, en serpientes y escaleras |
| 6 | 32m | **PageRank.** El navegante al azar, las páginas sin salida y el salto, en una web de cuatro páginas y en la de este curso |
:::

1. [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]
2. [[mkv-clasificar-estados|Clasificar los estados]]
3. [[mkv-la-estacionaria|La estacionaria y sus cuatro teoremas]]
4. [[mkv-olvida-su-inicio|¿Olvida su inicio?]]
5. [[mkv-absorcion|Cuánto falta para terminar]]
6. [[mkv-pagerank|PageRank: el navegante al azar]]

## Qué no cubre esta clase

- **Cadenas infinitas** salvo como contraejemplo: ahí los teoremas cambian.
- **Qué tan rápido** se olvida el inicio en general: solo se mide en los
  ejemplos.
- **Decidir** entre varias matrices y **estados que no se ven** tampoco
  están aquí.

Empieza por [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]].
