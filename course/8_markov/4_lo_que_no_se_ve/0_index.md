---
id: markov-lo-que-no-se-ve
title: "Clase 4 · Lo que no se ve"
nav_title: "Lo que no se ve"
summary: "Cuando el estado no se ve y solo llegan señales: el modelo oculto, filtrar, decodificar con Viterbi, la idea de aprenderlo, un modelo de lenguaje pequeño, y de ahí a decidir con la creencia y al aprendizaje por refuerzo."
status: ready
estimated_time: 206m
tags: [markov, ocultas, hmm, filtrar, viterbi, pomdp]
prerequisites: [markov-decidir]
---

# Clase 4 · Lo que no se ve

**Si el estado de la cadena no se ve y solo llegan señales, ¿qué puedes
saber de él, y cómo decides con eso?** Al terminar sabrás modelar una
cadena oculta y estimar en qué estado estás. También encontrarás la
secuencia más probable y plantearás la decisión cuando no ves el estado.

> [!WARNING]
> **Tarea para el miércoles 4 de noviembre:** ver y entender dos videos,
> uno sobre modelos ocultos de Markov y la lección 3 del curso de
> refuerzo de David Silver. Los enlaces y las preguntas con las que
> llegas están en [[tarea-lo-que-no-se-ve|la tarea de la clase 4]].

## Lo que traes

Esta clase sigue a las tres anteriores. Si un renglón no te suena, vuelve a su página.

- **La cadena que se ve.** En [[mkv-cadena-en-general|La cadena en general]]
  viste $\mu_0$, $P$ y $\mu_{t+1}=\mu_tP$. Aquí la misma $P$ mueve un
  estado que no se ve.
- **Contar para ajustar.** En [[mkv-ajustar-contando|Ajustar contando]]
  estimaste $P$ con conteos. Aquí contar sirve cuando hay etiquetas.
- **A la larga.** En [[mkv-olvida-su-inicio|Olvida su inicio]] viste cuándo
  una cadena deja de recordar de dónde salió.
- **Decidir.** En [[mkv-el-mdp|El proceso de decisión de Markov]] y
  [[mkv-bellman|La ecuación de Bellman]] el agente veía su estado. Aquí
  ya no.

## Qué vas a poder hacer al terminar esta clase

- **Escribir un modelo oculto:** estados, señales, $P$ y $B$, y la
  probabilidad de una trayectoria con sus señales.
- **Filtrar:** calcular la creencia sobre el estado actual, día por día.
- **Decodificar:** encontrar la secuencia de estados más probable con
  Viterbi, y decir en qué se distingue del mejor estado de cada día.
- **Decidir con la creencia** y decir qué falta para llegar al
  aprendizaje por refuerzo.

---

## El hilo de la clase

Un solo juguete: **el paraguas**. Trabajas en un sótano sin ventanas y no
ves el clima; solo ves si tu compañero llega con paraguas. El mismo juguete
sirve para generar, filtrar, decodificar, aprender y decidir. Al final, el
mismo modelo con tres estados gramaticales y unas doce palabras.

## Recorrido

Nueve páginas, en orden; la última resume toda la clase en una sola página.

**Los minutos son de lectura.** Cada página, salvo el resumen, cierra con
un ejercicio final con pistas y respuesta plegadas. Resolverlo toma tiempo
aparte, que no está en la tabla.

::: table {#mkv-ruta-4 title="Las páginas de esta clase"}
| # | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 12m | **Lo que necesitas.** La regla de Bayes y normalizar |
| 2 | 28m | **El modelo oculto.** Estados, señales, $P$ y $B$, la probabilidad conjunta y las preguntas que se le hacen |
| 3 | 28m | **Filtrar y predecir.** La creencia día por día y la señal de mañana |
| 4 | 28m | **Decodificar.** Viterbi, el suavizado y por qué el mejor estado de cada día no da la mejor secuencia |
| 5 | 18m | **Aprender.** Contar con etiquetas y la idea de Baum-Welch sin ellas |
| 6 | 22m | **Un modelo de lenguaje pequeño.** El mismo modelo con tres estados gramaticales y unas doce palabras |
| 7 | 40m | **Decidir sin ver.** De ver el estado a decidir con la creencia, y el valor de mirar |
| 8 | 18m | **Hacia el aprendizaje por refuerzo.** El mapa de dos ejes |
| 9 | 12m | **Resumen: el formulario.** Qué le preguntas a una cadena visible u oculta |
| 10 | 120m, aparte | **Tarea.** Dos videos, para el miércoles 4 de noviembre |
:::

1. [[mkv-bayes-y-normalizar|Lo que necesitas: Bayes y normalizar]]
2. [[mkv-el-modelo-oculto|El modelo oculto]]
3. [[mkv-filtrar|Filtrar y predecir]]
4. [[mkv-decodificar|Decodificar: Viterbi y suavizar]]
5. [[mkv-aprender-lo-oculto|Aprender un modelo oculto]]
6. [[mkv-lenguaje-pequeno|Un modelo de lenguaje pequeño]]
7. [[mkv-decidir-sin-ver|Decidir sin ver el estado]]
8. [[mkv-hacia-refuerzo|Hacia el aprendizaje por refuerzo]]
9. [[mkv-resumen-lo-oculto|Resumen de la clase: el formulario]]

Aparte del recorrido: [[tarea-lo-que-no-se-ve|la tarea de la clase 4, para el miércoles 4 de noviembre]].

## Qué no cubre esta clase

- **Baum-Welch derivado:** solo su idea, sin las fórmulas.
- **Suavizar a fondo:** una sección, la que Viterbi y el aprendizaje necesitan.
- **Aprendizaje por refuerzo:** la clase termina en el mapa de lo que falta.
- **Cadenas de tiempo continuo.**

Empieza por [[mkv-bayes-y-normalizar|Lo que necesitas: Bayes y normalizar]].
