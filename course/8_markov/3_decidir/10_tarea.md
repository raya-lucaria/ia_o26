---
id: tarea-decidir
title: "Tarea de la clase 3 · Ver la clase de David Silver sobre MDP"
nav_title: Tarea
summary: "Para el miércoles 28 de octubre: ver y entender la clase 2 del curso de aprendizaje por refuerzo de David Silver, sobre procesos de decisión de Markov, y llegar con cuatro preguntas contestadas."
status: ready
estimated_time: 120m
tags: [markov, tarea, video, mdp, bellman]
---

# Tarea de la clase 3 · Ver la clase de David Silver sobre MDP

> [!WARNING]
> **Tarea para el miércoles 28 de octubre.** Ver y entender un video de una
> hora y 42 minutos. No hay nada que entregar: llegas a clase pudiendo
> contestar las cuatro preguntas de abajo con tus palabras.

---

## 1 · Ver el video

**[RL Course by David Silver — Lecture 2: Markov Decision Process](https://www.youtube.com/watch?v=lfHX2hHRMVQ)**
— Google DeepMind, una hora y 42 minutos, en inglés. Los subtítulos
automáticos ayudan si los necesitas.

Es la segunda clase del curso de aprendizaje por refuerzo que David Silver
dio en University College London. Recorre lo mismo que esta clase, en el
mismo orden, y un poco más:

1. **Procesos de Markov:** la cadena de las clases 1 y 2.
2. **Procesos de Markov con recompensa:** una cadena que además paga. Su
   valor sale de un sistema lineal, como en
   [[mkv-evaluar-politica|Evaluar una política]].
3. **Procesos de decisión de Markov:** acciones, políticas, $V_\pi$ y
   $Q_\pi$, y la ecuación de Bellman del óptimo, como en
   [[mkv-el-mdp|El MDP]] y [[mkv-bellman|La ecuación de Bellman]].
4. **Extensiones:** estados que no se ven y horizontes sin fin. Esto la
   clase no lo cubre.

**La condición no es verlo: es entenderlo.** Páralo, regrésate y vuelve a
correr un trozo si hace falta. Cuando reconozcas algo de la clase, busca la
página que lo hizo con el pasillo.

### Su notación y la nuestra

Silver escribe las mismas ideas con otras letras. Antes de empezar, ten a
mano esta tabla:

::: table {#mkv-c3-tarea-tabla-notacion title="La notación del video y la de la clase"}
| En el video | En la clase | Qué es |
|---|---|---|
| $\mathcal P^a_{ss'}$ | $P(s'\mid s,a)$ | La probabilidad de ir de $s$ a $s'$ usando $a$ |
| $\mathcal R^a_s$ | $r(s,a)$ | La recompensa esperada de usar $a$ en $s$ |
| $v_\pi(s)$ | $V_\pi(s)$ | El valor de $s$ siguiendo la política $\pi$ |
| $q_\pi(s,a)$ | $Q_\pi(s,a)$ | Usar $a$ una vez y después seguir $\pi$ |
| $v_*(s)$, $q_*(s,a)$ | $V^*(s)$, $Q^*(s,a)$ | Los valores óptimos |
| $\pi(a\mid s)$ | $\pi(a\mid s)$ | La política: igual en los dos |
| $\gamma$ | no hay (vale 1) | El descuento |
:::

> [!WARNING]
> **El video descuenta y la clase no.** Silver suma
> $G_t=R_{t+1}+\gamma R_{t+2}+\gamma^2R_{t+3}+\dots$ con $0\le\gamma\le1$.
> En la clase las recompensas se suman tal cual: es su fórmula con
> $\gamma=1$, y por eso la clase pide que la política termine. Cuando él
> escribe $v=\mathcal R+\gamma\mathcal P v$, piensa en
> $V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi$ del pasillo.

---

## 2 · Con qué llegas a clase

Pudiendo explicar con tus palabras, sin leerlas:

1. **Qué agrega cada paso** de proceso de Markov a proceso con recompensa,
   y de ahí a proceso de decisión.
2. **La diferencia entre $V_\pi$ y $Q_\pi$,** y cómo se obtiene una de la
   otra.
3. **Por qué la ecuación de $V_\pi$ se resuelve con un sistema lineal y la
   de $V^*$ no:** qué le hace el máximo.
4. **Para qué sirve $\gamma$** en el video, y qué pide la clase a cambio de
   no usarlo.

---

**Punto de control:** si puedes contestar las cuatro sin abrir el video, la
tarea está hecha.

Regresa al [[markov-decidir|índice de la clase]].
