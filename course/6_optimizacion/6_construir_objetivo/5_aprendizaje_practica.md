---
id: opt-objetivo-aprendizaje-practica
title: "Elegir actividades para aprender"
nav_title: "Aprendizaje: práctica"
summary: "Formular con un indicador observable, detectar cómo puede fallar y revisar el objetivo con nuevos datos."
status: ready
tags: [optimizacion, modelado, practica]
---

# Elegir actividades para aprender

Como tutor, vas a preparar una sesión para que un estudiante pueda
**resolver después preguntas de dos temas sin ayuda**. Puedes elegir las
actividades que realizará, pero necesitas decidir cómo comparar las opciones. ¿Basta con contar lo que
responde bien mientras practica?

En estos dos problemas vas a formular una propuesta y después revisarla con
información nueva. Los valores son **estimaciones didácticas inventadas**,
no resultados de un estudio. Intenta cada ejercicio antes de abrir sus ayudas.

## Problema 5 · Preparar una sesión para dos temas

::: exercise {#opt-obj-apr-ej-sesion title="Elegir una actividad por tema"}
Dispones de **20 minutos** para la sesión con el estudiante. Para cada
tema puedes elegir entre una actividad E, con ayudas abundantes, y una
actividad R, que requiere responder sin ayuda.

Todas las actividades duran **10 minutos** y contienen **10 preguntas**.
La sesión debe cumplir estas condiciones:

- Elegir exactamente una actividad del tema 1 y una del tema 2.
- Realizar completas las actividades elegidas, sin dividirlas ni repetirlas.
- Terminar dentro de los 20 minutos disponibles.

La tabla muestra cuántos aciertos se prevén durante cada actividad:

| Actividad | Tema | Aciertos |
|---|---:|---:|
| E1 | 1 | 10 |
| E2 | 2 | 10 |
| R1 | 1 | 6 |
| R2 | 2 | 6 |

Un colega te propone usar esos aciertos para comparar las opciones: le
parece conveniente que el estudiante responda correctamente tantas
preguntas como sea posible durante la práctica. Para este ejercicio, la
estimación de una actividad no cambia al elegir otra para el segundo tema.

**Tu tarea es formular y examinar esa propuesta:**

1. Identifica los datos y las decisiones. Escribe el objetivo, las
   restricciones y los dominios de las variables.
2. Construye una selección admisible que puntúe alto. Explica cómo podría
   lograrlo sin demostrar que el estudiante responderá después sin ayuda.
3. Distingue qué mide el objetivo y qué deja fuera del propósito de aprender.

No tenemos datos sobre una evaluación posterior. Tu explicación debe
respetar ese límite, sin inventar resultados para esa evaluación.
:::

### Primero intenta plantearlo

Antes de abrir la primera pista, intenta separar lo que sabes de lo que puedes elegir.

::: hint {#opt-obj-apr-pista-sesion-datos of="opt-obj-apr-ej-sesion" title="Pista 1 · Separar datos y decisiones"}
Agrupa las opciones por tema: E1 y R1 son alternativas entre sí; E2 y R2
también. Los minutos y aciertos previstos son datos. Lo que eliges es qué
actividad se realiza en cada tema.
:::

Si todavía no encuentras cómo expresarlo, la segunda pista puede ayudarte.

::: hint {#opt-obj-apr-pista-sesion-guia of="opt-obj-apr-ej-sesion" title="Pista 2 · Construir la expresión"}
¿Cómo harías que una actividad no elegida aportara cero al total, y una
elegida aportara su estimación completa?
:::

Cuando tengas un planteamiento, compáralo con la respuesta.

::: answer {#opt-obj-apr-resp-sesion of="opt-obj-apr-ej-sesion" title="Respuesta · Contar aciertos y preguntar qué demuestran"}
**1. Distinguir lo que queremos de lo que contamos.** Queremos que el estudiante
responda después sin ayuda. Por ahora solo tenemos estimaciones de aciertos
durante las actividades, algunas de las cuales ofrecen ayudas abundantes.

Ese conteo es un **indicador**: una medida concreta que usamos para valorar
una selección. Puede relacionarse con el propósito, pero la relación necesita
justificarse; no basta con llamar “aprendizaje” a los aciertos.

**2. Definir parámetros y decisiones.** Sea $K$ el conjunto de temas y $J_k$
el conjunto de actividades del tema $k$. Cada actividad pertenece a un solo
tema y $J$ reúne todas las actividades.

- $t_j>0$: Duración de $j$, en minutos.
- $T>0$: Tiempo disponible, en minutos.
- $a_j\ge0$: Aciertos previstos al realizar $j$.

Para cada actividad definimos una variable $x_j\in\{0,1\}$. Vale uno si
seleccionamos la actividad completa y cero si la dejamos fuera; no tiene
unidad física. **Elegimos actividades, no sus aciertos**: las estimaciones
ya vienen dadas.

**3. Construir lo que vamos a contar.** Si seleccionamos la actividad $j$,
contamos sus $a_j$ aciertos previstos; si la dejamos fuera, contamos cero.
El producto $a_jx_j$ expresa esas dos posibilidades. Al sumar obtenemos:

$$
\text{aciertos previstos durante la sesión}=\sum_{j\in J}a_jx_j.
$$

La suma se mide en aciertos. Podemos usarla porque el ejercicio supone que
seleccionar una actividad no cambia la estimación de la elegida para el otro
tema.

Para el tiempo hacemos lo mismo: $t_jx_j$ cuenta los minutos de una actividad
solo cuando se realiza. La suma de esos minutos debe caber en $T$. Además,
al sumar las variables de las actividades de un mismo tema, el resultado
debe ser uno: así elegimos una y dejamos fuera las demás.

**4. Reunir el modelo general.**

$$
\begin{aligned}
\max\quad &\sum_{j\in J}a_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

El objetivo mide un número previsto de aciertos durante la sesión. Sirve
para preferir las actividades con más respuestas correctas en ese momento.
Si queremos usarlo para valorar lo que se aprenderá, todavía necesitamos
justificar esa relación.

**5. Sustituir los datos.** Aquí $J_1=\{E1,R1\}$ y $J_2=\{E2,R2\}$:

$$
\begin{aligned}
\max\quad &10x_{E1}+10x_{E2}+6x_{R1}+6x_{R2}\\
\text{sujeto a}\quad
&x_{E1}+x_{R1}=1,\\
&x_{E2}+x_{R2}=1,\\
&10x_{E1}+10x_{E2}+10x_{R1}+10x_{R2}\le20,\\
&x_{E1},x_{E2},x_{R1},x_{R2}\in\{0,1\}.
\end{aligned}
$$

El tiempo se cumple automáticamente con estos datos y una actividad por tema;
mantener la condición permite reconocer el presupuesto del relato.

**6. Poner a prueba el indicador.** La selección E1 y E2 cumple las reglas y
suma 20 aciertos previstos. R1 y R2 también es admisible, pero suma 12. El
objetivo favorece la primera pareja.

Podemos imaginar que el estudiante responde bien gracias a las ayudas y aún
necesita esas ayudas al terminar. Eso basta para mostrar el límite del
indicador: **una puntuación alta durante la sesión no demuestra que el
estudiante pueda responder después sin ayuda**. Tampoco podemos concluir con estos datos que las R produzcan
más aprendizaje.

Para saber más necesitamos observar lo que el estudiante puede responder
después, por ejemplo en una prueba común sin ayuda. Cambiar el nombre del
objetivo a “aprendizaje” no aporta esa información.
:::

## Problema 6 · Responder después sin ayuda

::: exercise {#opt-obj-apr-ej-diferida title="Preparar al estudiante para una prueba sin ayuda"}
Seguimos preparando la misma sesión, pero queremos mirar lo que el estudiante
podrá responder **después, sin ayuda**. Para eso disponemos ahora de
estimaciones sobre una evaluación posterior.

**Las condiciones de la sesión se conservan:**

- Las mismas cuatro actividades, completas y sin repeticiones, de 10 minutos
  cada una.
- Un presupuesto de 20 minutos y exactamente una actividad por tema.
- Los mismos aciertos previstos durante la sesión.

**La información nueva** corresponde a una prueba común de 20 preguntas:
10 del tema 1 y 10 del tema 2. Todas las personas responden la misma prueba
sin ayuda, cualquiera que haya sido su selección de actividades.

Cada fila indica los aciertos previstos en el bloque de un tema si se
selecciona esa actividad para prepararlo:

| Actividad | Tema | Aciertos |
|---|---:|---:|
| E1 | 1 | 2 |
| E2 | 2 | 2 |
| R1 | 1 | 7 |
| R2 | 2 | 7 |

Suponemos que el resultado previsto de cada tema depende únicamente de la
actividad elegida para ese tema: **no hay interacción entre temas**. Los
bloques contienen preguntas distintas y sus aciertos se suman. Estos son
supuestos didácticos; no son evidencia de que las actividades causen esos
resultados.

Con esta información, tu colega propone elegir las actividades con las que
se prevean más aciertos en la prueba posterior. Examina esta nueva propuesta:

1. Escribe el modelo completo y explica qué cambia respecto del problema 5.
2. Explica por qué esta evaluación está más cerca del propósito de aprender.
3. Describe una situación en la que se obtenga una puntuación alta y aun así
   quede fuera algo importante del aprendizaje. ¿Qué habría que observar
   para revisar ese límite?
:::

### Primero intenta plantearlo

Antes de abrir la primera pista, intenta separar lo que sabes de lo que puedes elegir.

::: hint {#opt-obj-apr-pista-diferida-datos of="opt-obj-apr-ej-diferida" title="Pista 1 · Separar datos y decisiones"}
Tenemos dos estimaciones de aciertos por actividad: durante la sesión y
después, en el bloque de su tema. Las actividades posibles y las
reglas de selección se conservan; la prueba posterior es común.
:::

Si todavía no encuentras cómo expresarlo, la segunda pista puede ayudarte.

::: hint {#opt-obj-apr-pista-diferida-guia of="opt-obj-apr-ej-diferida" title="Pista 2 · Construir la expresión"}
¿Qué datos te dicen cuántas preguntas podría responder bien el estudiante
cuando ya no tenga ayuda? Al usar esos datos, ¿cambian el tiempo disponible
o la obligación de cubrir ambos temas?
:::

Cuando tengas un planteamiento, compáralo con la respuesta.

::: answer {#opt-obj-apr-resp-diferida of="opt-obj-apr-ej-diferida" title="Respuesta · Cambiar los aciertos que contamos"}
**1. Identificar el cambio.** Antes contábamos aciertos durante las
actividades; ahora contamos los previstos en una prueba posterior sin
ayuda. Las actividades se eligen antes de conocer esos resultados: las
estimaciones no garantizan lo que ocurrirá.

**2. Definir el dato nuevo.** Los conjuntos de temas y actividades
($K,J_k,J$), las duraciones $t_j$, el tiempo disponible $T$ y las variables
binarias $x_j$ conservan su significado.

Llamamos $b_j\ge0$ al número previsto de aciertos en el bloque posterior del
tema de $j$ si seleccionamos esa actividad. Esta estimación es un dato nuevo:
no podemos deducirla de los aciertos durante la sesión ni de nuestro deseo
de que el estudiante aprenda.

**3. Contar los aciertos de cada bloque.** Para un mismo tema hay varias
actividades posibles, pero realizamos solo una. Multiplicar $b_j$ por $x_j$
permite contar la estimación de la actividad elegida y dejar en cero las de
sus alternativas:

$$
\text{aciertos previstos en el bloque del tema }k
=\sum_{j\in J_k}b_jx_j.
$$

Después sumamos los bloques para obtener el total de la prueba. Las
preguntas de un bloque son distintas de las del otro, así que no contamos
un mismo acierto dos veces. Además, el supuesto de ausencia de interacción
permite conservar la estimación de un bloque al elegir la actividad del otro.

**4. Reunir el modelo general completo.**

$$
\begin{aligned}
\max\quad &\sum_{j\in J}b_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

El objetivo se mide en aciertos previstos en la prueba posterior. Ahora
comparamos lo que el estudiante respondería después y sin ayuda, como pedía
el propósito. Aún necesitamos confiar en que la prueba evalúa lo que nos
interesa y en que las estimaciones son adecuadas.

**5. Sustituir los datos.**

$$
\begin{aligned}
\max\quad &2x_{E1}+2x_{E2}+7x_{R1}+7x_{R2}\\
\text{sujeto a}\quad
&x_{E1}+x_{R1}=1,\\
&x_{E2}+x_{R2}=1,\\
&10x_{E1}+10x_{E2}+10x_{R1}+10x_{R2}\le20,\\
&x_{E1},x_{E2},x_{R1},x_{R2}\in\{0,1\}.
\end{aligned}
$$

**6. Comparar las dos valoraciones.** Las selecciones admisibles no han
cambiado. Para cada una, esta tabla compara los aciertos previstos en los
dos momentos:

En la tabla, «Prueba» corresponde a la evaluación posterior.

| Selección | Sesión | Prueba |
|---|---:|---:|
| E1 y E2 | 20 | 4 |
| E1 y R2 | 16 | 9 |
| R1 y E2 | 16 | 9 |
| R1 y R2 | 12 | 14 |

La pareja que más puntuaba durante la sesión puntúa menos en la evaluación
posterior. Estos datos permiten mostrar la diferencia que antes solo
podíamos señalar como posibilidad.

**7. Buscar lo que todavía queda fuera.** Si alguien memoriza las 20
preguntas de la prueba y falla ante preguntas nuevas, puede obtener una
puntuación alta sin poder usar lo aprendido en otra situación. El nuevo
indicador está más cerca del propósito, pero tampoco equivale a todo el
aprendizaje.

Para examinar ese límite, podríamos incluir preguntas nuevas en la prueba.
Necesitaríamos estimaciones correspondientes a esa evaluación: **no podemos
reutilizar los mismos $b_j$ sin justificarlos**. También habría que revisar
la suma si estudiar un tema cambiara el desempeño en el otro.
:::

Después de tus intentos, consulta [[opt-objetivo-aprendizaje-modelo|el modelo general de selección e indicadores]].
