---
id: opt-objetivo-juego-modelo
title: Del resultado final a la evaluación de posiciones
nav_title: Juego · Modelo general
summary: "Justificar max–min y distinguir la utilidad terminal de una valoración aproximada al limitar la exploración."
status: ready
tags: [optimizacion, modelado, juegos]
---

# Del resultado final a la evaluación de posiciones

**Primero intenta los [[opt-objetivo-juego-practica|dos problemas del juego]].**
Hay dos decisiones de modelado: cómo representar la respuesta del rival
y qué valor asignar a cada consecuencia que podemos examinar.

## 1 · Decisiones propias y respuestas ajenas

| Símbolo | Significado | Papel |
|---|---|---|
| $A$ | Acciones propias, conjunto finito no vacío | Dato |
| $B(a)$ | Respuestas permitidas tras $a$, conjunto finito no vacío | Dato |
| $U(a,b)$ | Utilidad final propia tras ambas acciones | Dato conocido |
| $a$ | Primera acción propia | Decisión que buscamos |
| $b$ | Respuesta elegida después por el rival | Decisión ajena |

Suponemos un juego determinista de suma cero: la utilidad rival es $-U$.
El rival observa $a$, conoce sus alternativas y busca minimizar $U$.
Todas las condiciones importan para interpretar el mínimo como respuesta
adversaria. No describimos decisiones simultáneas ni incertidumbre aleatoria.

En la práctica, los movimientos que siguen a $a,b$ están forzados; por eso
la tabla ya puede dar su utilidad final. Si hubiera nuevas elecciones,
el valor de la continuación tendría que representarlas también.

## 2 · Construir el criterio frente al rival

Para cada acción propia, el menor resultado disponible al rival es

$$v(a)=\min_{b\in B(a)}U(a,b).$$

Luego elegimos el mayor de esos valores:

$$\begin{aligned}
\max_a\quad &\min_{b\in B(a)}U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

Este orden expresa que elegimos primero y el rival responde después de
observarnos. No podemos reemplazarlo por una maximización conjunta sobre
$a,b$: eso nos daría control sobre ambos jugadores.

El valor usa la escala de $U$. En la práctica es +1 al ganar y −1 al perder,
y ninguna ficha otorga utilidad por sí misma. Minimizar una carga máxima
en un horario también puede combinar extremos, pero allí no aparece por
eso otro agente que elija una respuesta. La interpretación depende del relato.

## 3 · Sustituir las reglas del juego pequeño

Tomamos $A=\{G,S\}$ para Guardar y Sacrificar, y $B(a)=\{I,D\}$ en ambos
casos. La tabla final determina

$$v(G)=\min\{1,-1\}=-1,\qquad v(S)=\min\{1,1\}=1.$$

El modelo $\max_{a\in\{G,S\}}v(a)$ elige Sacrificar. En cambio, el mejor
resultado posible de cada fila vale 1: compararlos deja empate y omite
que Guardar permite una derrota. No hay probabilidades con las cuales
justificar un promedio de columnas.

El supuesto adversarial puede ser demasiado conservador para otros fines.
Si quisiéramos modelar errores frecuentes del rival, necesitaríamos datos
sobre ellos. Con probabilidades justificadas $\pi(b\mid a)$, otro objetivo
posible sería maximizar $\sum_{b\in B(a)}\pi(b\mid a)U(a,b)$ sobre $a\in A$.
Ese sería otro modelo de conducta, no una consecuencia de la tabla sola.

## 4 · Detenerse antes del desenlace

Sea $s(a,b)$ la posición alcanzada tras ambas acciones y sea $h(s)$ una
valoración fija de esa posición. Cuando no usamos el desenlace final,
el modelo de la recomendación limitada es

$$\begin{aligned}
\max_a\quad &\min_{b\in B(a)}h(s(a,b))\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

Aquí $h$ cuenta fichas propias. Por tanto, sus valores tienen unidades de
fichas y no de utilidad terminal. Para el problema 10:

$$\min_{b\in\{I,D\}}h(s(G,b))=\min\{3,2\}=2,$$

$$\min_{b\in\{I,D\}}h(s(S,b))=\min\{0,0\}=0.$$

El modelo recomienda Guardar. La auditoría conserva la tabla terminal
conocida y comprueba que esa recomendación permite perder. El agente no
ha incumplido su modelo: la valoración intermedia ordena las decisiones
de una manera distinta al propósito final.

En problemas mayores puede que no conozcamos los desenlaces para hacer
esta comparación completa. El juego pequeño permite aislar el defecto
de la valoración antes de sumar esa dificultad.

## 5 · Revisar la valoración con información disponible

En la práctica hay señales locales que certifican victoria o derrota
inevitables. Con indicadores $W(s),D(s)\in\{0,1\}$ para esas dos señales,
y sin que ambas puedan activarse a la vez, definimos

$$h'(s)=W(s)-D(s).$$

Las señales dadas producen valores $(1,-1)$ para las posiciones de Guardar
y $(1,1)$ para las de Sacrificar. El modelo completo revisado es

$$\max_{a\in A}\min_{b\in B(a)}h'(s(a,b)),$$

con los mismos conjuntos $A=\{G,S\}$ y $B(a)=\{I,D\}$. Recomienda
Sacrificar, de acuerdo con los resultados finales. La nueva función usa
hechos observables relacionados con el objetivo; no basta con cambiar
puntuaciones hasta que gane nuestra acción favorita.

En un juego grande, detectar una victoria forzada puede exigir examinar
muchas continuaciones. Si ninguna señal se activa, el cero de $h'$ indica
ausencia de certificación, **no empate demostrado**. Para usar otras
características habría que explicar su relación con ganar, fijar su escala
y comprobar casos donde engañen. Los parámetros de esa valoración deben
estar fijados al elegir la jugada: optimizarlos libremente junto con ella
permitiría mejorar la puntuación sin mejorar la posición.

## 6 · El puente hacia árboles de juegos

Cuando los jugadores vuelven a decidir, cada posición puede representarse
como un nodo y cada acción como una arista hacia otra posición. Los turnos
propios buscan valores altos y los adversarios, bajos. Esta alternancia
conduce a la formulación **minimax**. En las hojas terminales conocemos la
utilidad; si detenemos la exploración antes, usamos una función de evaluación.
La distinción se desarrolla en el
[texto de Berkeley sobre minimax y evaluaciones limitadas por profundidad](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html).

Más adelante estudiaremos cómo recorrer esos árboles y cuándo la poda
alfa–beta permite omitir ramas. Aquí la pregunta previa es **qué valor
estamos propagando y qué supuestos lo justifican**. Resolver exactamente
un modelo con una mala valoración no corrige lo que esa valoración omite.

[[opt-objetivo-juego-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
