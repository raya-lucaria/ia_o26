---
id: opt-objetivo-aprendizaje-modelo
title: "Cómo comparar actividades para aprender"
nav_title: "Aprendizaje: modelo general"
summary: "Separar selección, estimaciones y propósito al construir y revisar una función objetivo educativa."
status: ready
tags: [optimizacion, modelado, practica]
---

# Cómo comparar actividades para aprender

**Primero intenta los [[opt-objetivo-aprendizaje-practica|dos problemas de actividades]].**
Queremos elegir actividades que ayuden a responder preguntas después sin
ayuda. Para compararlas usamos los aciertos previstos, pero necesitamos
precisar **en qué momento y con qué ayudas se responde**.

El modelo puede contar correctamente los aciertos y aun así dejar fuera
algo importante del aprendizaje. Vamos a separar las reglas de la sesión
de la medida que usamos para preferir unas actividades sobre otras.

## 1 · Elegir una actividad por tema

Empezamos por organizar las opciones. Llamamos $K$ al conjunto finito y no
vacío de temas. Para cada tema $k$, el conjunto $J_k$ contiene sus actividades
posibles, y $J$ reúne todas las actividades.

Cada actividad pertenece a un solo tema. Por eso los conjuntos $J_k$ son
**disjuntos**: ninguna actividad aparece en dos de ellos. La información
que recibimos sobre las actividades es la siguiente:

- $t_j>0$: Duración de $j$, en minutos.
- $T>0$: Tiempo disponible, en minutos.
- $a_j\ge0$: Aciertos previstos al realizar $j$.
- $b_j\ge0$: Aciertos previstos después, en el bloque del tema preparado con $j$.

El dato $b_j$ solo está disponible cuando contamos con estimaciones para una
prueba posterior, como en el problema 10. No se obtiene de $a_j$: saber
cuántas preguntas se responderán bien durante la práctica no basta para
predecir lo que ocurrirá después.

La decisión se expresa con $x_j\in\{0,1\}$. Uno significa realizar la
actividad completa y cero significa dejarla fuera. **Elegimos actividades;
los aciertos son estimaciones que recibimos como datos.**

## 2 · Respetar los temas y el tiempo disponible

Dentro de cada tema, sumar las variables de selección cuenta cuántas
actividades realizamos. Como necesitamos exactamente una, escribimos:

$$
\sum_{j\in J_k}x_j=1\qquad\text{para cada }k\in K.
$$

No basta con pedir tantas actividades como temas. La igualdad
$\sum_{j\in J}x_j=|K|$ permitiría, por ejemplo, elegir las dos actividades
de un tema y ninguna del otro en la práctica. La cantidad sería correcta,
pero faltaría cubrir un tema.

También debemos contar los minutos. La actividad $j$ consume $t_jx_j$
minutos: su duración completa si se elige, y cero si se deja fuera. Al sumar
el tiempo de todas las actividades seleccionadas, no podemos superar el
presupuesto:

$$
\sum_{j\in J}t_jx_j\le T.
$$

Estas reglas determinan qué selecciones están permitidas. **Cambiar la
manera de compararlas no cambia los temas ni el tiempo disponible.** Por
eso ambas restricciones aparecen en los dos modelos de la práctica.

## 3 · Contar los aciertos durante la práctica

Una primera propuesta consiste en preferir las actividades con las que el
estudiante responda bien más preguntas durante la sesión. Para traducirla,
contamos los $a_j$ aciertos previstos de cada actividad elegida y cero por
las que se dejan fuera. Eso es lo que expresa $a_jx_j$.

Suponemos que elegir una actividad no modifica los aciertos previstos en
las demás. Con ese supuesto, sumamos las aportaciones y buscamos que el
total sea lo más grande posible:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}a_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

El objetivo se mide en **aciertos previstos durante las actividades**.
Cuenta todas las respuestas correctas por igual. En la práctica, cada
actividad tiene diez preguntas; si unas tuvieran más preguntas que otras,
habría que decidir si todavía queremos comparar el conteo total o usar
otra medida.

Este conteo puede servir para valorar lo que se responde bien durante la
sesión. Sin embargo, una actividad que facilite mucho cada pregunta puede
puntuar alto aunque el estudiante todavía dependa de las ayudas. La fórmula
no puede decirnos, con esos datos, si después responderá sin ellas.

## 4 · Contar los aciertos en la prueba posterior

Para acercarnos a lo que queremos saber, la segunda variante mira una
**prueba posterior común, sin ayuda**. Todas las personas responden las
mismas preguntas, aunque hayan realizado actividades diferentes. La prueba
contiene un bloque de preguntas distinto para cada tema.

La estimación $b_j$ dice cuántos aciertos se prevén en el bloque del tema de
$j$ si elegimos esa actividad. Solo una actividad se selecciona por tema;
al sumar $b_jx_j$, contamos su estimación y dejamos fuera las alternativas.

Suponemos que elegir una actividad solo afecta al resultado previsto de su
propio bloque. Como los bloques tienen preguntas distintas, podemos sumar
sus aciertos para comparar el total de la prueba:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}b_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

La unidad sigue siendo aciertos, pero **ahora contamos respuestas en otro
momento y sin ayudas**. Eso acerca la medida al propósito de la sesión.
Aun así, las estimaciones no garantizan lo que ocurrirá ni demuestran que
las actividades causen las diferencias: son datos inventados para formular
el ejercicio.

También importa el supuesto sobre los temas. Si estudiar uno cambiara el
resultado en otro, $\sum_j b_jx_j$ podría dejar de representar bien el total
previsto. Necesitaríamos datos sobre esa relación y una expresión que la
recogiera. Escribir $F(x)$ y llamarla “aprendizaje real” no aporta la
información que falta.

## 5 · Pedir también un mínimo de aciertos durante la práctica

Podemos querer que el estudiante responda bien después y, además, que durante
la sesión consiga cierto número de aciertos. Esta segunda petición agrega
una condición que **no estaba en el problema 10**. Tiene que ser una decisión
explícita de quien prepara la sesión.

Llamemos $A\ge0$ al mínimo exigido de aciertos previstos durante la práctica.
Ya sabemos calcular ese conteo con $\sum_j a_jx_j$; ahora pedimos que sea al
menos $A$. El objetivo sigue siendo conseguir tantos aciertos como sea
posible en la prueba posterior:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}b_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&\sum_{j\in J}a_jx_j\ge A,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

Con $A=14$ y los datos de la práctica, seleccionar R1 y R2 deja de estar
permitido: solo suma 12 aciertos previstos durante la sesión. Las parejas
con una E y una R sí cumplen el mínimo, pues suman 16 durante la sesión;
sus aciertos previstos después son 9.

El mínimo cambia qué selecciones aceptamos. No se deduce automáticamente
del deseo de aprender, y uno demasiado alto podría dejar el modelo sin
ninguna selección admisible.

## 6 · ¿Qué nos dicen esos aciertos?

Una forma de revisar el objetivo es imaginar cómo se podría puntuar alto
sin lograr lo que buscábamos. En el primer problema, las ayudas permiten
acumular aciertos sin demostrar que el estudiante pueda responder por su
cuenta. En el segundo, alguien podría memorizar las preguntas de la prueba
y aun así fallar ante preguntas nuevas.

Cada objeción pide información concreta. Podríamos usar preguntas nuevas,
comprobar qué recuerda el estudiante más adelante o ver si puede aplicar lo
aprendido a otros problemas. Cualquiera de esas revisiones necesitaría sus
propios datos; no podemos justificarlas cambiando únicamente el nombre de
la suma.

## Qué razonamiento puedes reutilizar

**Explica qué cuenta tu objetivo y por qué ese conteo ayuda a elegir.**
Después busca un caso que puntúe bien sin cumplir el propósito. Esa
comparación permite ver qué información falta.

Al revisar el modelo, distingue las actividades que puedes elegir, las
estimaciones que recibes y las reglas que debes respetar. Si cambias un
dato o un supuesto, explica cuál y vuelve a escribir el modelo completo.

[[opt-objetivo-aprendizaje-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver al banco de práctica]].
