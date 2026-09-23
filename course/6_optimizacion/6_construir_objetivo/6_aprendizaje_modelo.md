---
id: opt-objetivo-aprendizaje-modelo
title: "El modelo general de un indicador de aprendizaje"
nav_title: "Aprendizaje: modelo general"
summary: "Separar selección, estimaciones y propósito al construir y revisar una función objetivo educativa."
status: ready
tags: [optimizacion, modelado, practica]
---

# El modelo general de un indicador de aprendizaje

**Primero intenta los [[opt-objetivo-aprendizaje-practica|dos problemas de actividades]].**
La pregunta es: **¿qué actividades elegir y con qué medida compararlas?**
Una formulación puede representar exactamente un indicador y aun así omitir
parte del propósito que motivó la elección.

## 1 · Definir lo que puede elegirse

Sea $K$ el conjunto finito no vacío de temas. Para cada tema $k$, $J_k$
contiene sus actividades posibles. Estos conjuntos son disjuntos: cada
actividad pertenece a un solo tema. Su unión es $J$.

| Dato | Significado |
|---|---|
| $t_j>0$ | Duración de la actividad $j$, en minutos |
| $T>0$ | Tiempo disponible, en minutos |
| $a_j\ge0$ | Aciertos previstos durante la actividad $j$ |
| $b_j\ge0$, cuando se dispone de la estimación | Aciertos previstos después, en el bloque del tema de $j$, al seleccionar esa actividad |

Elegimos $x_j\in\{0,1\}$: uno significa realizar la actividad completa y
cero significa no realizarla. No elegimos los aciertos. Los valores $a_j$
y $b_j$ son estimaciones que el modelo recibe como datos.

## 2 · Construir las obligaciones antes de comparar

Para seleccionar exactamente una actividad de cada tema necesitamos
$\sum_{j\in J_k}x_j=1$ para cada $k$. Una sola igualdad que exigiera
$\sum_{j\in J}x_j=|K|$ contaría actividades, pero permitiría concentrarlas
en algunos temas y omitir otros.

El tiempo consumido es $\sum_{j\in J}t_jx_j$ minutos. Su límite es $T$.
Estas condiciones determinan las selecciones permitidas y se conservan en
las dos variantes de la práctica. Elegir otro indicador no elimina las
obligaciones del relato.

## 3 · Formular el indicador disponible

Si cada actividad conserva su estimación independientemente de las otras,
su aportación durante la sesión es $a_jx_j$. El modelo completo es

$$
\begin{aligned}
\max\quad &\sum_{j\in J}a_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

El objetivo mide aciertos previstos durante las actividades. La suma cuenta
todas las respuestas correctas por igual. En la práctica, cada actividad
tiene diez preguntas; si sus longitudes cambiaran, habría que decidir si
seguir valorando un conteo total o comparar otra medida.

Un sistema que facilita mucho cada pregunta puede elevar esa suma. Eso es
compatible con el objetivo escrito, aunque la persona todavía dependa de
ayudas. El modelo no descubre por sí mismo que nuestra intención era
desempeño posterior autónomo.

## 4 · Revisar la medición con datos pertinentes

La segunda variante usa una prueba posterior común, sin ayuda, dividida en
bloques de preguntas distintos por tema. Se supone que elegir una actividad
afecta únicamente al resultado previsto de su propio bloque. Así podemos
sumar las estimaciones seleccionadas:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}b_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J_k}x_j=1 &&\text{para cada }k\in K,\\
&\sum_{j\in J}t_jx_j\le T,\\
&x_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

La unidad sigue siendo aciertos, pero **cambió qué evaluación se cuenta**.
Esto permite comparar selecciones sobre la misma prueba, realizada después
y sin ayudas. No constituye una garantía de aprendizaje ni demuestra que
las diferencias sean efectos causados por las actividades: las estimaciones
son supuestos dados para formular el ejercicio.

Si existen interacciones entre temas, $\sum_j b_jx_j$ puede dejar de
representar bien la consecuencia. Harían falta datos sobre esas interacciones
y una expresión que las recoja. Escribir $F(x)$ y llamarla “aprendizaje real”
no resuelve la falta de información.

## 5 · Distinguir otro objetivo de una obligación adicional

Puede interesarnos el desempeño posterior y también mantener cierta
experiencia de éxito durante la sesión. Eso introduce una preferencia
adicional que no estaba en el problema 6.

Por ejemplo, **si se adopta explícitamente** un mínimo de $A\ge0$ aciertos
previstos durante la sesión, el modelo revisado es

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
permitido porque suma 12 aciertos previstos en sesión. Las parejas con una
E y una R suman 16 durante la sesión y 9 después. El umbral cambia qué
selecciones se aceptan; no es una conclusión inevitable de querer aprender.
Un mínimo imposible podría dejar el modelo sin solución.

## 6 · Intentar engañar al indicador

Para revisar una propuesta, busca una selección que eleve su puntuación
sin cumplir bien el propósito. En la práctica, las ayudas cuestionan los
aciertos de la sesión; memorizar preguntas conocidas cuestionaría incluso
una prueba posterior sin ayuda.

La revisión debe especificar qué medición nueva se necesita. Evaluar
preguntas nuevas, observar retención más tarde o medir transferencia a
otros problemas puede ser pertinente, pero exige nuevos datos. No hay una
fórmula única que podamos justificar solamente cambiando el nombre de la suma.

## Qué razonamiento puedes reutilizar

**Declara qué mide el objetivo, por qué lo usas y cómo podría puntuar bien
sin lograr el propósito.** Mantén separadas las decisiones, las estimaciones
y las obligaciones. Una revisión útil cambia datos o supuestos explícitos
y vuelve a construir el modelo completo.

[[opt-objetivo-aprendizaje-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
