---
id: tarea-lo-que-no-se-ve
title: "Tarea de la clase 4 · Dos videos"
nav_title: Tarea
summary: "Para el miércoles 4 de noviembre: ver y entender un video sobre modelos ocultos de Markov y la lección 3 del curso de refuerzo de David Silver, sobre programación dinámica, y llegar con cuatro preguntas contestadas."
status: ready
estimated_time: 120m
tags: [markov, tarea, video, ocultas, programacion-dinamica]
---

# Tarea de la clase 4 · Dos videos

> [!WARNING]
> **Tarea para el miércoles 4 de noviembre.** Ver y entender dos videos:
> uno de unos 14 minutos y otro de una hora y 39 minutos. No hay nada que
> entregar: llegas a clase pudiendo contestar las cuatro preguntas de abajo
> con tus palabras.

---

## 1 · Ver los videos

**Primero, el modelo oculto.**
[Hidden Markov Model: Data Science Concepts](https://www.youtube.com/watch?v=fX5bYmnHqqE)
— ritvikmath, unos 14 minutos, en inglés. Es el mismo autor de dos de los
videos de [[tarea-que-es-una-cadena|la tarea de la clase 1]]. Presenta el
modelo oculto de Markov, el tema de [[mkv-el-modelo-oculto|El modelo oculto]].

**Después, planificar con programación dinámica.**
[RL Course by David Silver — Lecture 3: Planning by Dynamic Programming](https://www.youtube.com/watch?v=Nd1-UUMVfz4)
— Google DeepMind, una hora y 39 minutos, en inglés. Los subtítulos
automáticos ayudan si los necesitas.

Según sus diapositivas, la lección recorre seis temas, en este orden:

1. **Introducción:** qué pide un problema para resolverse con programación
   dinámica.
2. **Evaluación de políticas,** como en
   [[mkv-evaluar-politica|Evaluar una política]].
3. **Iteración de políticas,** como en
   [[mkv-iterar-politicas|Iteración de políticas]].
4. **Iteración de valores,** como en
   [[mkv-iterar-valores|Iteración de valores]].
5. **Extensiones:** actualizar los estados en otro orden, con muestras o de
   forma aproximada. Esto la clase no lo cubre.
6. **Contracción:** por qué estas iteraciones convergen. Tampoco lo cubre la
   clase.

**La condición no es verlos: es entenderlos.** Páralos, regrésate y vuelve a
correr un trozo si hace falta. Cuando reconozcas algo de la clase 3, busca la
página que lo hizo con el pasillo.

### Su notación y la nuestra

Silver escribe las mismas ideas con otras letras. Es la misma tabla de
[[tarea-decidir|la tarea de la clase 3]], con una fila más:

::: table {#mkv-c4-tarea-tabla-notacion title="La notación de la lección y la de la clase"}
| En el video | En la clase | Qué es |
|---|---|---|
| $\mathcal P^a_{ss'}$ | $P(s'\mid s,a)$ | La probabilidad de ir de $s$ a $s'$ usando $a$ |
| $\mathcal R^a_s$ | $r(s,a)$ | La recompensa esperada de usar $a$ en $s$ |
| $v_\pi(s)$ | $V_\pi(s)$ | El valor de $s$ siguiendo la política $\pi$ |
| $v_*(s)$ | $V^*(s)$ | El valor óptimo |
| $v_k$, iteración $k$ | $V^{(k)}$, ronda $k$ | La aproximación después de $k$ rondas |
| *backup* | actualizar | Recalcular el valor de un estado con el de sus sucesores |
| $\gamma$ | no hay (vale 1) | El descuento |
:::

> [!WARNING]
> **El video descuenta y la clase no.** Silver suma con $0\le\gamma\le1$. En
> la clase las recompensas se suman tal cual: es su fórmula con $\gamma=1$, y
> por eso la clase pide que la política termine.

---

## 2 · Con qué llegas a clase

Pudiendo explicar con tus palabras, sin leerlas:

1. **El estado oculto y la señal.** En el ejemplo del primer video, ¿qué es
   lo que no se ve y qué es lo que sí? Escríbelos con las letras de la
   clase: $\mathcal S$, $\mathcal O$, $P$ y $B$.
2. **Las preguntas que se le hacen al modelo.** ¿Qué le pregunta el video al
   modelo oculto? Clasifica cada pregunta entre las cuatro de
   [[mkv-el-modelo-oculto|El modelo oculto]]: verosimilitud, filtrar,
   decodificar y aprender.
3. **Evaluar, mejorar y las dos iteraciones.** En la lección de Silver, ¿qué
   hace la evaluación de una política y qué hace su mejora? ¿Qué cambia
   entre iterar políticas e iterar valores?
4. **Qué pide la programación dinámica.** La lección dice que un problema
   necesita dos propiedades para resolverse así, y enumera otros usos. Uno de
   ellos, en la diapositiva 6, es el algoritmo de Viterbi. ¿Cuáles son las
   dos propiedades?

---

**Punto de control:** si puedes contestar las cuatro sin abrir los videos, la
tarea está hecha.

Regresa al [[markov-lo-que-no-se-ve|índice de la clase]].
