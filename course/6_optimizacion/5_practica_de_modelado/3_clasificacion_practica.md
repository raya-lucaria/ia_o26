---
id: opt-objetivo-clasificacion-practica
title: Clasificar mensajes y evaluar probabilidades
nav_title: Clasificación
summary: "Construir dos objetivos para una misma regla y comprobar por qué mejorar las probabilidades no siempre aumenta los aciertos."
status: ready
estimated_time: 20m
tags: [optimizacion, modelado, clasificacion]
---

# Clasificar mensajes y evaluar probabilidades

Un equipo quiere separar mensajes normales de mensajes no deseados.
**Clasificar** consiste aquí en decidir a cuál de esos dos grupos pertenece
cada mensaje. Vamos a construir dos maneras de evaluar la misma regla.

Los datos son ficticios. No necesitamos conocer un algoritmo de
clasificación ni buscar los mejores parámetros para formular el problema.

## 1 · Separar los mensajes de la regla que ajustamos

Tenemos tres mensajes ya revisados. La entrada $x$ cuenta sus enlaces;
la etiqueta correcta $y$ vale 0 para un mensaje normal y 1 para uno no deseado.

| Mensaje | Enlaces | Clase |
|---|---:|---:|
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 1 |

Estos registros no establecen una ley general sobre los mensajes con enlaces.
Son los casos conocidos con los que vamos a comparar reglas.

**¿Qué podemos cambiar: los mensajes, sus etiquetas o la regla?**

Elegimos dos parámetros reales, $a$ y $b$, ambos entre $-4$ y $4$.
Usamos **la misma pareja para los tres mensajes**. La regla asigna a la
clase 1 esta probabilidad:

$$p(x;a,b)=\sigma(ax+b),\qquad \sigma(z)=\frac{1}{1+e^{-z}}.$$

La función $\sigma$, llamada **sigmoide**, transforma cualquier número real
en uno estrictamente entre 0 y 1. A la clase 0 le corresponde la probabilidad
$1-p(x;a,b)$. Entradas, parámetros y probabilidades no tienen unidades físicas.

Llamamos $p_i(a,b)=p(x_i;a,b)$ a la probabilidad del mensaje $i$. Para anunciar
una etiqueta, la regla usa el umbral 0.5; **el empate da clase 1**:

$$\widehat y_i(a,b)=
\begin{cases}1&\text{si }p_i(a,b)\ge0.5,\\0&\text{si }p_i(a,b)<0.5.\end{cases}$$

Probabilidades y etiquetas se calculan a partir de $a,b$. No son decisiones
que podamos elegir por separado para que cada mensaje salga bien.

## 2 · Construir una medida de aciertos

El equipo quiere acertar tantas etiquetas como sea posible y da el mismo
peso a cada mensaje. **¿Cómo contaríamos un acierto y dejaríamos fuera un error?**

Usamos $\mathbf1\{P\}$: vale 1 si la afirmación $P$ es verdadera y 0 si es
falsa. Así, $\mathbf1\{\widehat y_i(a,b)=y_i\}$ cuenta el acierto del mensaje
$i$. Sumamos los tres resultados y dividimos entre 3 para obtener una proporción.

Esa medida se llama **accuracy**. El modelo completo es

$$\begin{aligned}
\max_{a,b}\quad &\frac13\sum_{i=1}^3
\mathbf1\{\widehat y_i(a,b)=y_i\}\\
\text{sujeto a}\quad &-4\le a\le4,\\
&-4\le b\le4,\qquad a,b\in\mathbb R.
\end{aligned}$$

Las entradas de la tabla dan $p_1=\sigma(b)$, $p_2=\sigma(a+b)$ y
$p_3=\sigma(2a+b)$. En el primer mensaje acertamos si $p_1<0.5$; en los
otros dos, si $p_i\ge0.5$. El objetivo está entre 0 y 1 y no tiene unidades.

**¿Distingue un acierto con probabilidad 0.51 de otro con probabilidad 0.99?**

No: ambos cuentan uno si esa es la probabilidad de la clase correcta.
Podemos cambiar los parámetros y las probabilidades sin cambiar ninguna
etiqueta. Mientras eso ocurra, accuracy permanece en una **meseta**: su valor
no cambia. Contar aciertos es fácil, pero ese conteo no informa de pequeñas
mejoras en las probabilidades.

## 3 · Evaluar la probabilidad de la clase correcta

El equipo también quiere distinguir esas probabilidades. Propone usar el
**negativo del logaritmo natural** de la probabilidad asignada a la clase
correcta. Esta medida es la **pérdida logarítmica**, o *log loss*.

Es una elección del modelo: interesarse por las probabilidades no obliga
a usar esta fórmula. Aquí la tomamos como propuesta y examinamos qué mide.

**Si la clase correcta es 0, ¿debemos evaluar $p_i$ o $1-p_i$?**

Usamos $p_i$ cuando $y_i=1$ y $1-p_i$ cuando $y_i=0$. Si llamamos $r$ a
esa probabilidad correcta, $-\ln r$ disminuye cuando $r$ aumenta. Se acerca
a 0 cuando $r$ se acerca a 1 y crece sin límite cuando $r$ se acerca a 0.

El signo negativo permite **minimizar una pérdida** para favorecer
probabilidades altas de la clase correcta. Un error con mucha confianza
en la clase equivocada recibe una penalización grande.

Reunimos los dos casos de etiqueta en una expresión:

$$\ell_i(a,b)=-y_i\ln p_i(a,b)-(1-y_i)\ln(1-p_i(a,b)).$$

Uno de los coeficientes vale 1 y el otro 0. La sigmoide mantiene los dos
argumentos de los logaritmos positivos. Promediando los tres casos obtenemos
este segundo modelo completo:

$$\begin{aligned}
\min_{a,b}\quad &\frac13\sum_{i=1}^3\ell_i(a,b)\\
\text{sujeto a}\quad &-4\le a\le4,\\
&-4\le b\le4,\qquad a,b\in\mathbb R.
\end{aligned}$$

Con las etiquetas 0, 1 y 1, el objetivo es

$$\frac{-\ln(1-p_1(a,b))-\ln p_2(a,b)-\ln p_3(a,b)}3.$$

Se expresa en **nats por ejemplo** porque usamos logaritmos naturales; no
es un porcentaje de errores. En esta familia, varía suavemente con los
parámetros y registra cambios que el umbral puede ocultar.

Sus derivadas pueden orientar cambios de los parámetros para reducir la
pérdida. En cambio, dentro de una meseta de accuracy, las derivadas no
indican cómo mejorar el conteo. Esta diferencia motiva usar un objetivo
sustituto para ajustar; no hace que las dos medidas sean equivalentes.

## 4 · Comprobar si las dos medidas prefieren lo mismo

**¿Una pérdida menor garantiza más aciertos?** Comparemos dos reglas
permitidas con $a=0$. La primera usa $b=\ln9\approx2.197$ y asigna
probabilidad 0.9 a la clase 1 en todos los mensajes. La segunda usa
$b=\ln(0.49/0.51)\approx-0.040$ y asigna 0.49.

La primera anuncia clase 1 siempre y acierta dos veces. La segunda anuncia
clase 0 siempre y acierta una. Sus pérdidas se calculan así:

$$L_1=\frac{-\ln0.1-2\ln0.9}3,\qquad
L_2=\frac{-\ln0.51-2\ln0.49}3.$$

En la tabla, $p$ es la probabilidad de clase 1. Las pérdidas están redondeadas.

| $p$ | Accuracy | Log loss |
|---|---:|---:|
| 0.9 | 2/3 | 0.838 |
| 0.49 | 1/3 | 0.700 |

**La segunda regla tiene menor pérdida y menos aciertos.** La primera
penaliza fuertemente el mensaje normal, al que asigna apenas 0.1 de
probabilidad de pertenecer a su clase correcta.

La comparación refuta que cada reducción de log loss aumente accuracy.
No encontramos los óptimos globales ni demostramos que los mejores
parámetros de ambos problemas sean distintos.

## 5 · Volver al propósito de la clasificación

Si nos interesan las probabilidades, log loss puede ser una medida de
interés por sí misma. Si solo nos interesa acertar etiquetas, usarla para
ajustar significa elegir un **objetivo sustituto**. Después tenemos que
comprobar el resultado con la medida que motivó el trabajo.

Ambos modelos dan el mismo peso a cada mensaje. Representar errores con
costos distintos requeriría esos datos. Para evaluar mensajes nuevos,
además, necesitamos casos que no hayan determinado el ajuste: las cifras
de los tres mensajes usados no garantizan resultados futuros.

Algo parecido ocurre al contar aciertos en una actividad educativa:
responder bien con ayuda no demuestra que después se responderá sin ella.
En [[opt-objetivo-aprendizaje-practica|la práctica de aprendizaje]] revisarás esa diferencia.

Consulta opcional: [[opt-objetivo-clasificacion-modelo|generalizar la regla a varias características]].

Siguiente ejemplo: [[opt-objetivo-juego-practica|elegir una jugada cuando el rival responde]].
