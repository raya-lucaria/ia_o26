---
id: opt-objetivo-clasificacion-practica
title: Clasificar casos y comparar probabilidades
nav_title: Clasificación · Practicar
summary: "Construir una medida de aciertos y otra de probabilidades, y comprobar qué cambia al elegir entre ellas."
status: ready
tags: [optimizacion, modelado, clasificacion, practica]
---

# Clasificar casos y comparar probabilidades

**Clasificar** es decidir a cuál de varios grupos pertenece un caso. Aquí
vamos a separar mensajes normales de mensajes no deseados. Una regla
asignará probabilidades a ambos grupos y, a partir de ellas, anunciará
a cuál pertenece cada mensaje.

Vamos a comparar reglas usando casos cuya clase correcta ya conocemos.
Primero contaremos aciertos; después evaluaremos las probabilidades que
asigna cada regla. Los datos son ficticios: no necesitas entrenar un modelo
ni conocer un algoritmo de clasificación.

## Problema 7 · Contar cuántas etiquetas acierta una regla

::: exercise {#opt-obj-clas-ej-1 title="Contar cuántas etiquetas acierta una regla"}
Un equipo quiere ajustar una regla que separe mensajes normales de
mensajes no deseados. Para ponerla a prueba, tiene **tres mensajes ya
revisados**. Son datos ficticios para este ejercicio.

De cada mensaje conoce el número de enlaces que contiene, que será la
entrada $x$. La etiqueta correcta $y$ vale **0 para un mensaje normal** y
**1 para uno no deseado**.

| Mensaje | Enlaces | Clase |
|---|---:|---:|
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 1 |

El número de enlaces es un conteo, sin unidades físicas. Los tres
registros son los datos disponibles; no establecen una regla general
sobre qué mensajes son no deseados.

**La regla que podemos ajustar.** Elegimos dos números reales, $a$ y $b$.
Cada uno debe estar entre $-4$ y $4$, y usamos la misma pareja para los tres
mensajes. La probabilidad que la regla asigna a la clase 1 está dada por

$$p(x;a,b)=\frac{1}{1+e^{-(ax+b)}}.$$

La transformación del número $ax+b$ mediante esta fórmula se llama
**sigmoide**. Su resultado está estrictamente entre 0 y 1. La probabilidad
de la clase 0 es $1-p(x;a,b)$; los parámetros y las probabilidades tampoco
tienen unidades físicas.

**Cómo anuncia una clase.** La regla marca el mensaje como no deseado
(clase 1) cuando su probabilidad es **mayor o igual que 0.5**. En caso
contrario, lo marca como normal (clase 0). Así queda
resuelto también el empate entre las dos probabilidades.

**Qué quiere el equipo.** Al comparar reglas, cada mensaje cuenta lo mismo:
el equipo prefiere la que tenga una mayor proporción de etiquetas
acertadas. Esa proporción se conoce como **accuracy**.

Plantea el modelo completo, sin buscar los mejores parámetros. Tu propuesta
debe indicar qué se elige, qué valores se permiten y cómo se calcula la
proporción que quieres maximizar.

Explica también qué información conserva esa medida y cuál pierde.
Para hacerlo, compara asignar probabilidad 0.51 o 0.99 a la clase correcta.
:::

### Intenta escribir el modelo

Haz un primer intento en tu hoja. Si no encuentras cómo empezar, abre la
primera pista; después vuelve a tu propuesta.

::: hint {#opt-obj-clas-pista-1a of="opt-obj-clas-ej-1" title="Pista 1 · Qué eliges y qué calculas"}
Organiza lo que dice el enunciado antes de escribir el objetivo.

- **Mensajes que conocemos**: Número de enlaces y etiqueta correcta de cada uno.
- **Números que ajustamos**: Una pareja de parámetros, ambos entre −4 y 4.
- **Regla para anunciar la clase**: Usa la probabilidad de clase 1 y el umbral 0.5; el empate da clase 1.

Al elegir los dos parámetros, ya puedes calcular la probabilidad y la
etiqueta anunciada para cada caso.
:::

Si todavía no logras expresar la proporción, usa la segunda pista.

::: hint {#opt-obj-clas-pista-1b of="opt-obj-clas-ej-1" title="Pista 2 · Cómo contar los aciertos"}
¿Cómo asignarías un 1 a un acierto y un 0 a un error? ¿Qué necesitas hacer
con esos tres números para obtener una proporción?
:::

Antes de abrir la respuesta, revisa tu propuesta. Después compara ambas
y localiza los pasos que planteaste de otra manera.

::: answer {#opt-obj-clas-resp-1 of="opt-obj-clas-ej-1" title="Construir la proporción de aciertos"}
**Los datos y los números que elegimos.** Llamemos $I$ al conjunto de casos
y $n=|I|>0$ a su cantidad. Para cada caso conocemos su entrada $x_i$ y su
etiqueta correcta $y_i\in\{0,1\}$. También conocemos una cota $M>0$ para
los parámetros.

Elegimos únicamente $a$ y $b$, ambos reales en el intervalo $[-M,M]$.
Esta pareja se usa en todos los casos. Las entradas y los parámetros no
tienen unidades físicas.

**De los parámetros a la etiqueta.** Primero calculamos la probabilidad
de clase 1 para cada caso:

$$p_i(a,b)=\frac{1}{1+e^{-(ax_i+b)}}.$$

Después aplicamos la regla del umbral. La etiqueta anunciada, que escribimos
como $\widehat y_i$, es

$$\widehat y_i(a,b)=
\begin{cases}1&\text{si }p_i(a,b)\ge0.5,\\0&\text{si }p_i(a,b)<0.5.\end{cases}$$

**No elegimos las probabilidades ni las etiquetas por separado.** Una vez
fijados $a$ y $b$, estas expresiones determinan ambas.

**De la etiqueta al acierto.** Comparamos la etiqueta anunciada con la
correcta. El símbolo $\mathbf 1\{P\}$ vale 1 cuando la afirmación $P$ es
verdadera y 0 cuando es falsa. Por eso,

$$\mathbf 1\{\widehat y_i(a,b)=y_i\}$$

aporta un 1 si acertamos en el caso $i$ y un 0 si fallamos. Sumamos esas
aportaciones para contar los aciertos y dividimos entre $n$ para obtener
su proporción. El resultado no tiene unidades y está entre 0 y 1.

**El modelo general** busca la mayor proporción posible:

$$\begin{aligned}
\max_{a,b}\quad &\frac1n\sum_{i\in I}
\mathbf 1\{\widehat y_i(a,b)=y_i\}\\
\text{sujeto a}\quad &-M\le a\le M,\\
&-M\le b\le M,\qquad a,b\in\mathbb R.
\end{aligned}$$

**Ahora sustituimos los datos.** Los tres casos son los mensajes del
enunciado: $I=\{1,2,3\}$ y $M=4$.
Para abreviar la sigmoide escribimos $\sigma(z)=1/(1+e^{-z})$. Las entradas
0, 1 y 2 dan las probabilidades

$$(p_1,p_2,p_3)=(\sigma(b),\sigma(a+b),\sigma(2a+b)).$$

La primera etiqueta correcta es 0; las otras dos son 1. Por tanto, el modelo
concreto es

$$\begin{aligned}
\max_{a,b}\quad &\frac{
\mathbf 1\{p_1(a,b)<0.5\}+
\mathbf 1\{p_2(a,b)\ge0.5\}+
\mathbf 1\{p_3(a,b)\ge0.5\}}{3}\\
\text{sujeto a}\quad &-4\le a\le4,\quad -4\le b\le4,\quad a,b\in\mathbb R.
\end{aligned}$$

**Lo que cuenta y lo que deja fuera.** Dar el mismo peso a cada acierto
supone que todos los errores cuestan lo mismo. Asignar probabilidad 0.51 o
0.99 a la clase correcta produce el mismo acierto. Accuracy registra la
etiqueta final, pero pierde esa diferencia entre probabilidades.

Contar aciertos es sencillo. Sin embargo, podemos cambiar un poco los
parámetros y obtener las mismas etiquetas: mientras eso ocurra, el objetivo
permanece igual. El conteo puede saltar cuando cambian las etiquetas.

El siguiente problema considera una medida que conserva diferencias entre
probabilidades. Si un error de clasificación costara más que otro, harían
falta además datos sobre esos costos para representarlos en el modelo.
:::

## Problema 8 · Evaluar las probabilidades de una regla

::: exercise {#opt-obj-clas-ej-2 title="Evaluar las probabilidades de una regla"}
El equipo también quiere evaluar las probabilidades que asigna la regla
a cada mensaje. La etiqueta anunciada no muestra toda esa información: distintas
probabilidades pueden producir la misma etiqueta.

**Se conserva lo siguiente:**

- Los tres mensajes, con sus números de enlaces y sus etiquetas correctas.
- La fórmula que calcula probabilidades a partir de $a$ y $b$.
- Las cotas entre $-4$ y $4$ para ambos parámetros.
- El umbral 0.5 y la regla que anuncia clase 1 en caso de empate.

**Cambia la medida con la que se ajusta la regla.** Para cada caso, el
equipo propone tomar la probabilidad asignada a su clase correcta y
calcular el **negativo de su logaritmo natural**. Después quiere minimizar
el promedio de los tres valores. Esta medida se llama **pérdida
logarítmica** o **log loss**.

Esta es una propuesta concreta del equipo. Querer probabilidades altas
para la clase correcta no obliga, por sí solo, a elegir esta medida.

Construye el modelo completo y explica para qué sirve el signo negativo.
Después compara estas dos reglas permitidas, que usan $a=0$:

La primera usa $b=\ln9$ y la segunda, $b=\ln(0.49/0.51)$. En la tabla,
$p$ es la probabilidad de clase 1 en cada mensaje.

| Regla | $p$ |
|---|---:|
| Primera | 0.9 |
| Segunda | 0.49 |

Calcula la pérdida logarítmica y la proporción de aciertos de cada regla.
Puedes usar calculadora. A partir de la comparación, responde: ¿tener menor
log loss implica necesariamente tener mayor accuracy en este conjunto?

No necesitas encontrar los mejores parámetros de ninguno de los dos modelos.
:::

### Intenta construir la nueva medida

Antes de abrir las pistas, identifica qué probabilidad corresponde a la
clase correcta en cada caso y escribe una propuesta de objetivo.

::: hint {#opt-obj-clas-pista-2a of="opt-obj-clas-ej-2" title="Pista 1 · Qué clase estás evaluando"}
Ordena los datos que necesitas para evaluar cada regla.

- **Probabilidad que entrega la fórmula**: Corresponde siempre a la clase 1.
- **Etiquetas correctas**: Son 0, 1 y 1, en ese orden.
- **Dos reglas para comparar**: Sus parámetros están dentro de las cotas.

La medida propuesta usa la probabilidad de la **clase correcta de cada
caso**, que puede ser distinta de la clase anunciada.
:::

Si todavía no sabes cómo escribir esa medida, abre la segunda pista y
vuelve a tu hoja.

::: hint {#opt-obj-clas-pista-2b of="opt-obj-clas-ej-2" title="Pista 2 · Qué probabilidad recibe esa clase"}
Si la etiqueta correcta es 0, ¿qué probabilidad le asigna la regla a esa
clase? ¿Qué sucede con el negativo de su logaritmo cuando esa probabilidad
se acerca a 1? ¿Y cuando se acerca a 0?
:::

Antes de abrir la respuesta, revisa tu modelo y tus cálculos. Después
compara los resultados y la explicación de cada medida.

::: answer {#opt-obj-clas-resp-2 of="opt-obj-clas-ej-2" title="Construir y comparar la pérdida logarítmica"}
**Primero elegimos qué probabilidad evaluar.** Conservamos los datos
$I,x_i,y_i,M$ y las decisiones $a,b$ del problema anterior. La probabilidad
asignada a la clase correcta depende de su etiqueta:

- Si $y_i=1$, usamos $p_i(a,b)$.
- Si $y_i=0$, usamos $1-p_i(a,b)$.

**Después calculamos la pérdida.** Llamemos $r$ a esa probabilidad correcta.
Para $0<r<1$, el logaritmo natural $\ln r$ es negativo. Por eso $-\ln r$
es positivo y disminuye cuando $r$ aumenta.

Cuando $r$ se acerca a 1, la pérdida se acerca a 0. Cuando $r$ se acerca a
0, la pérdida crece sin límite: asignar una probabilidad muy baja a la
clase correcta recibe una penalización grande. Así se penalizan los errores
en los que la regla expresa mucha confianza en la clase equivocada.

Con logaritmo natural, la escala se expresa en **nats por ejemplo**. No es
un porcentaje de errores. El signo negativo ya está incluido en la
pérdida; al minimizarla no volvemos a cambiarle el signo.

**Reunimos las dos etiquetas en una expresión.** La pérdida del caso $i$ es

$$\ell_i(a,b)=-y_i\ln p_i(a,b)-(1-y_i)\ln(1-p_i(a,b)).$$

Si $y_i=1$, el primer coeficiente vale 1 y el segundo vale 0. Si $y_i=0$,
sucede lo contrario. La fórmula conserva así el término que corresponde
a la clase correcta.

La sigmoide produce probabilidades estrictamente entre 0 y 1 con estos
parámetros finitos. Por eso ambos logaritmos están definidos.

**El modelo general** minimiza el promedio de las pérdidas:

$$\begin{aligned}
\min_{a,b}\quad &\frac1n\sum_{i\in I}
\left[-y_i\ln p_i(a,b)-(1-y_i)\ln(1-p_i(a,b))\right]\\
\text{sujeto a}\quad &-M\le a\le M,\\
&-M\le b\le M,\qquad a,b\in\mathbb R.
\end{aligned}$$

**Ahora sustituimos los datos.** Las etiquetas son 0, 1 y 1, y usamos las
mismas probabilidades del problema anterior. El modelo queda

$$\begin{aligned}
\min_{a,b}\quad &\frac{-\ln(1-\sigma(b))-\ln\sigma(a+b)-\ln\sigma(2a+b)}{3}\\
\text{sujeto a}\quad &-4\le a\le4,\quad -4\le b\le4,\quad a,b\in\mathbb R.
\end{aligned}$$

**Comparamos las dos reglas.** La primera asigna 0.9 a la clase 1, por lo
que anuncia esa clase en los tres casos. Acierta dos veces. La segunda
asigna 0.49 a la clase 1, anuncia clase 0 en todos los casos y acierta una
vez.

Para calcular la pérdida usamos la probabilidad de la clase correcta,
incluso cuando la regla anuncia otra clase. Los promedios son

$$\frac{-\ln0.1-2\ln0.9}{3}\quad\text{para la primera regla},$$

$$\frac{-\ln0.51-2\ln0.49}{3}\quad\text{para la segunda regla}.$$

La columna $p$ muestra la probabilidad de clase 1; accuracy es la proporción
de aciertos.

| $p$ | Accuracy | Log loss |
|---|---:|---:|
| 0.9 | 2/3 | 0.838 |
| 0.49 | 1/3 | 0.700 |

Los valores de pérdida están redondeados. **La segunda regla tiene menor
pérdida y menos aciertos.** La primera recibe una penalización considerable
por asignar apenas 0.1 a la clase correcta del primer caso.

Este ejemplo refuta que cada reducción de log loss tenga que aumentar
accuracy. Comparamos dos reglas permitidas; **no comparamos los mejores
valores posibles** de los dos problemas ni probamos que sus parámetros
óptimos sean distintos.

**Cuándo tiene sentido elegir esta medida.** Log loss distingue
probabilidades que accuracy trata igual. En esta familia, además, varía
suavemente cuando cambian los parámetros.

Si nos interesa evaluar probabilidades, esa información justifica
considerarla. Si lo que finalmente importa es accuracy, podemos usar log
loss como **objetivo sustituto**: ajustamos con una medida y después
comprobamos los resultados con la otra. El contraejemplo muestra por qué
no debemos suponer que cada cambio mejora ambas.

Ambas medidas siguen dando el mismo peso a cada caso; ninguna representa
costos distintos de equivocarse. También necesitamos casos que no se hayan
usado para ajustar los parámetros si queremos evaluar predicciones nuevas.
Ninguna de las dos cifras obtenidas en los casos de ajuste demuestra, por
sí sola, cómo funcionará la regla con datos nuevos.
:::

Después de comparar tus modelos, pasa a [[opt-objetivo-clasificacion-modelo|la formulación general de clasificación]].
