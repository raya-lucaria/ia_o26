---
id: markov-decidir
title: "Clase 3 · Decidir"
nav_title: Decidir
summary: "Cuando en cada estado puedes elegir: de la pasada hacia atrás en una escalera al proceso de decisión de Markov, el valor de una política, la ecuación de Bellman y tres maneras de resolverla: iterar valores, iterar políticas y un programa lineal."
status: ready
estimated_time: 226m
tags: [markov, decidir, mdp, bellman, programacion-dinamica]
prerequisites: [markov-a-la-larga]
---

# Clase 3 · Decidir

**Si en cada estado puedes elegir qué matriz usar, ¿cuál conviene elegir,
y cómo se calcula?** Al final tendrás una ecuación que caracteriza la mejor
elección, su condición exacta y tres algoritmos que la resuelven.

## Lo que traes

Esta clase sigue a la clase 2. Si un renglón no te suena, vuelve a su página.

- **Condicionar en el primer paso.** En
  [[mkv-absorcion|Cuánto falta para terminar]] el tiempo medio de llegada
  salió de un sistema lineal; aquí el mismo truco da el valor de una
  política.
- **El MDP de agentes.** En
  [[de-consecuencias-a-refuerzo|De consecuencias a refuerzo]] viste la
  tupla de un proceso de decisión de Markov; aquí se resuelve.
- **El árbol de juegos.** En [[minimax|Minimax a mano]], el máximo se eligió
  hacia atrás en un árbol. Aquí no hay rival, pero hay azar y ciclos.

## Qué vas a poder hacer al terminar esta clase

- **Plantear un problema de decisión** como MDP: estados, acciones, una
  matriz por acción y recompensas.
- **Evaluar una política** con un sistema lineal, y decir cuándo tiene
  solución única.
- **Escribir la ecuación de Bellman** y su condición, y reconocer cuándo
  falla.
- **Resolverla de tres maneras:** iteración de valores, iteración de
  políticas y programa lineal, y decir qué garantiza cada una.

---

## El hilo de la clase

Dos juguetes. **La escalera** no tiene azar ni ciclos: se decide con una
sola pasada hacia atrás. **El robot en el pasillo mojado** tiene azar y
un ciclo: correr es rápido, pero puede resbalar y quedarse donde estaba.
Cada idea se calcula a mano en el pasillo de dos casillas y se corre en
uno de 200.

## Recorrido

Nueve páginas, en orden; la última resume toda la clase en una sola página.

**Los minutos son de lectura.** Cada página, salvo el resumen, cierra con
un ejercicio final con pistas y respuesta plegadas: resolverlo toma tiempo aparte, que no
está en la tabla.

::: table {#mkv-ruta-3 title="Las páginas de esta clase"}
| # | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 19m | **Lo que necesitas.** El máximo y el argmax, condicionar en el primer paso y el punto fijo de una función |
| 2 | 25m | **La escalera.** Contar rutas, elegir la más barata hacia atrás y por qué falla la codiciosa |
| 3 | 36m | **El MDP.** El pasillo mojado: acciones, una matriz por acción, políticas, retorno y valor |
| 4 | 28m | **Evaluar una política.** Un sistema lineal, a mano, con un algoritmo y simulando |
| 5 | 32m | **La ecuación de Bellman.** El valor óptimo, su condición exacta y la política codiciosa |
| 6 | 30m | **Iteración de valores.** Aplicar el máximo ronda tras ronda, cuándo parar y un pasillo de 200 casillas |
| 7 | 23m | **Iteración de políticas.** Evaluar y mejorar: termina en rondas finitas |
| 8 | 18m | **Como programa lineal.** Bellman con desigualdades y `linprog` |
| 9 | 15m | **Resumen: el formulario.** Definiciones, teoremas, los tres algoritmos y lo que más se confunde |
:::

1. [[mkv-max-y-punto-fijo|Lo que necesitas: el máximo y el punto fijo]]
2. [[mkv-la-escalera|De contar a decidir: la escalera]]
3. [[mkv-el-mdp|El proceso de decisión de Markov]]
4. [[mkv-evaluar-politica|Evaluar una política]]
5. [[mkv-bellman|La ecuación de Bellman]]
6. [[mkv-iterar-valores|Iteración de valores]]
7. [[mkv-iterar-politicas|Iteración de políticas]]
8. [[mkv-mdp-lineal|El MDP como programa lineal]]
9. [[mkv-resumen-decidir|Resumen de la clase: el formulario]]

## Qué no cubre esta clase

- **Descuento** solo en un recuadro: aquí las recompensas se suman tal
  cual.
- **Aprender sin conocer las matrices** (aprendizaje por refuerzo): aquí
  las matrices y las recompensas se conocen.
- **Estados que no se ven** tampoco están aquí.

Empieza por [[mkv-max-y-punto-fijo|Lo que necesitas: el máximo y el punto fijo]].
