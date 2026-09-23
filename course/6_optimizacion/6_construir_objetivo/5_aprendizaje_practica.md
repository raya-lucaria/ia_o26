---
id: opt-objetivo-aprendizaje-practica
title: "Elegir actividades para aprender"
nav_title: "Aprendizaje: práctica"
summary: "Formular con un indicador observable, detectar cómo puede fallar y revisar el objetivo con nuevos datos."
status: ready
tags: [optimizacion, modelado, practica]
---

# Elegir actividades para aprender

**Tu tarea:** formular dos maneras de elegir actividades y explicar qué
permiten afirmar sus objetivos. El propósito es que una persona pueda
resolver después preguntas de dos temas sin ayuda. Los valores siguientes
son estimaciones didácticas inventadas, no resultados de un estudio.
Intenta cada ejercicio antes de abrir sus ayudas.

## Problema 5 · Lo que podemos medir durante la sesión

::: exercise {#opt-obj-apr-ej-sesion title="Elegir una actividad por tema"}
Una sesión dura **20 minutos** y debe cubrir dos temas. Hay que elegir
**exactamente una actividad del tema 1 y exactamente una del tema 2**.
Cada actividad dura 10 minutos y contiene 10 preguntas. No se pueden repetir
actividades ni dividirlas.

Las actividades E incluyen ayudas abundantes; las R requieren responder
sin ayuda. Estas son las estimaciones disponibles:

| Actividad | Tema | Duración | Aciertos previstos durante la actividad |
|---|---:|---:|---:|
| E1 | 1 | 10 min | 10 de 10 |
| E2 | 2 | 10 min | 10 de 10 |
| R1 | 1 | 10 min | 6 de 10 |
| R2 | 2 | 10 min | 6 de 10 |

Se propone elegir las actividades con **mayor número total de aciertos
previstos durante la sesión**. Para este modelo, las estimaciones de una
actividad no cambian según qué actividad se elija para el otro tema.

Escribe datos, decisiones, objetivo, restricciones y dominios. Después
propón una selección admisible que puntúe alto y explica cómo podría
lograrlo sin demostrar que la persona responderá después sin ayuda.
¿Qué mide el objetivo y qué deja fuera? No inventes datos sobre esa
evaluación posterior.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-obj-apr-pista-sesion-datos of="opt-obj-apr-ej-sesion" title="PISTA 1 · Solo si te atoraste"}
Agrupa las opciones por tema: E1 y R1 son alternativas entre sí; E2 y R2
también. Los minutos y aciertos previstos son datos. Lo que eliges es qué
actividad se realiza en cada tema.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-apr-pista-sesion-guia of="opt-obj-apr-ej-sesion" title="PISTA 2 · Solo si te atoraste"}
¿Cómo harías que una actividad no elegida aportara cero al total, y una
elegida aportara su estimación completa?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-apr-resp-sesion of="opt-obj-apr-ej-sesion" title="Respuesta · Un indicador no es el propósito completo"}
**1. Separar propósito e indicador.** Queremos desempeño posterior sin ayuda.
Por ahora comparamos aciertos durante actividades que pueden incluir ayudas.
Ambas cosas pueden relacionarse, pero no son la misma medición.

**2. Definir parámetros y decisiones.** Sea $K$ el conjunto de temas y $J_k$
el conjunto de actividades del tema $k$. Cada actividad pertenece a un solo
tema y $J$ reúne todas las actividades.

| Parámetro | Significado y unidad |
|---|---|
| $t_j>0$ | Duración de la actividad $j$, en minutos |
| $T>0$ | Tiempo disponible, en minutos |
| $a_j\ge0$ | Aciertos previstos durante la actividad $j$ si se selecciona |

La decisión $x_j\in\{0,1\}$ vale uno si seleccionamos la actividad $j$ y
cero si no. Es un indicador de selección, sin unidad física.

**3. Construir expresiones.** La actividad aporta $a_jx_j$ aciertos
previstos y consume $t_jx_j$ minutos. Sumamos aportaciones porque el ejercicio
supone que la elección del otro tema no modifica esas estimaciones.
Para cada tema, sumar las selecciones debe dar exactamente uno.

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

El objetivo mide un número previsto de aciertos durante la sesión. Es
defendible para priorizar ese desempeño inmediato. Si se usa para representar
aprendizaje posterior, hace falta justificar la relación entre ambos.

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

**Comprobación y caso límite.** E1 y E2 obtienen 20 aciertos previstos;
R1 y R2, 12. El objetivo favorece la primera pareja. Pero esos 20 aciertos
pueden depender de las ayudas: por sí solos no demuestran que la persona
resolverá preguntas después sin ellas. Tampoco podemos concluir con estos
datos que las R produzcan más aprendizaje.

Para revisar el modelo necesitamos información alineada con el propósito,
por ejemplo desempeño posterior en una prueba común sin ayuda. Cambiar el
nombre del objetivo a “aprendizaje” no aporta esa información.
:::

## Problema 6 · Incorporar una evaluación posterior

::: exercise {#opt-obj-apr-ej-diferida title="Cambiar el indicador con nuevos datos"}
Conserva las cuatro actividades, sus duraciones de 10 minutos, el presupuesto
de 20 minutos y la obligación de seleccionar exactamente una actividad por
tema. También se conservan los aciertos previstos durante la sesión.

Ahora hay estimaciones adicionales para una **prueba común posterior, sin
ayuda**, de 20 preguntas: 10 del tema 1 y 10 del tema 2. Todas las personas
responden la misma prueba, cualquiera que haya sido su selección.

| Actividad seleccionada para un tema | Aciertos previstos en el bloque posterior de ese tema |
|---|---:|
| E1 | 2 de 10 del tema 1 |
| E2 | 2 de 10 del tema 2 |
| R1 | 7 de 10 del tema 1 |
| R2 | 7 de 10 del tema 2 |

Para este ejercicio, el resultado previsto de cada tema depende únicamente
de su actividad seleccionada: no hay interacción entre temas. Los dos
bloques tienen preguntas distintas y sus aciertos se suman. Son supuestos
didácticos del modelo, no evidencia de que una actividad cause esos resultados.

Se propone maximizar el total de aciertos previstos en esa prueba posterior.
Escribe el modelo completo y explica qué cambió respecto del problema 5,
por qué el nuevo objetivo está más cerca del propósito y qué sigue sin medir.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-obj-apr-pista-diferida-datos of="opt-obj-apr-ej-diferida" title="PISTA 1 · Solo si te atoraste"}
Tenemos dos mediciones por actividad: aciertos durante la sesión y aciertos
previstos después en el bloque de su tema. Las actividades posibles y las
reglas de selección se conservan; la prueba posterior es común.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-apr-pista-diferida-guia of="opt-obj-apr-ej-diferida" title="PISTA 2 · Solo si te atoraste"}
¿Qué datos corresponden al momento y a las condiciones del desempeño que
ahora quieres valorar? ¿Cambiar esa medición modifica por sí solo el tiempo
disponible o la obligación de cubrir ambos temas?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-apr-resp-diferida of="opt-obj-apr-ej-diferida" title="Respuesta · Revisar el indicador y conservar las obligaciones"}
**1. Identificar el cambio.** Sustituimos el desempeño durante actividades
por el desempeño previsto después, sin ayudas. La selección sigue siendo
una decisión previa: las estimaciones no son resultados garantizados.

**2. Definir el dato nuevo.** Conservamos $K,J_k,J,t_j,T$ y las variables
binarias $x_j$. Sea $b_j\ge0$ el número previsto de aciertos en el bloque
posterior del tema de $j$ si seleccionamos esa actividad.

**3. Construir la nueva expresión.** Una sola actividad está seleccionada
por tema. Por ello $\sum_{j\in J_k}b_jx_j$ toma la estimación de esa actividad,
sin contar también su alternativa. Sumamos los temas porque sus preguntas
son distintas y el supuesto excluye efectos entre ellos.

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
compara el desempeño sin ayuda y en un momento posterior, como pedía el
propósito. Sigue suponiendo que esa prueba y esas estimaciones son adecuadas.

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

**Comprobación y límite.** Las mismas selecciones reciben ahora otra valoración:

| Selección válida | Aciertos previstos en sesión | Aciertos previstos después |
|---|---:|---:|
| E1 y E2 | 20 | 4 |
| E1 y R2 | 16 | 9 |
| R1 y E2 | 16 | 9 |
| R1 y R2 | 12 | 14 |

La pareja que más puntuaba durante la sesión puntúa menos en la evaluación
posterior. Estos datos permiten mostrar la diferencia que antes solo
podíamos señalar como posibilidad.

El nuevo indicador tampoco equivale a todo el aprendizaje. Si alguien
memoriza las 20 preguntas y falla ante preguntas nuevas, puede obtener una
puntuación alta sin poder transferir lo aprendido. Revisaríamos la prueba
para incluir preguntas nuevas y necesitaríamos estimaciones correspondientes:
no podemos reutilizar los mismos $b_j$ sin justificarlos. También habría
que revisar la suma si estudiar un tema cambiara el desempeño en el otro.
:::

Después de tus intentos, consulta [[opt-objetivo-aprendizaje-modelo|el modelo general de selección e indicadores]].
