---
id: opt-objetivo-clasificacion-practica
title: Acertar etiquetas y asignar probabilidades
nav_title: Clasificación · Practicar
summary: "Formular accuracy y pérdida logarítmica, y comprobar por qué mejorar una no siempre mejora la otra."
status: ready
tags: [optimizacion, modelado, clasificacion, practica]
---

# Acertar etiquetas y asignar probabilidades

Una misma regla puede evaluarse por las etiquetas que acierta o por las
probabilidades que asigna. Practicaremos cómo construir ambos objetivos.
Los datos son didácticos; no necesitas entrenar un modelo ni conocer un
algoritmo de clasificación.

## Problema 7 · Contar decisiones correctas

::: exercise {#opt-obj-clas-ej-1 title="Ajustar una regla para acertar etiquetas"}
Tenemos tres ejemplos conocidos. Una entrada numérica $x$ resume cada
ejemplo; la etiqueta correcta $y$ vale 0 o 1.

| Ejemplo | Entrada | Etiqueta correcta |
|---|---:|---:|
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 1 |

Elegimos dos números reales, $a$ y $b$, compartidos por los tres ejemplos.
Cada uno debe estar entre $-4$ y $4$. Con ellos, la regla asigna a la clase 1
la probabilidad

$$p(x;a,b)=\frac{1}{1+e^{-(ax+b)}}.$$

Esta transformación, llamada **sigmoide**, convierte cualquier número real
en un valor entre 0 y 1. La probabilidad de la clase 0 es $1-p(x;a,b)$.
Entradas, parámetros y probabilidades no tienen unidades físicas aquí.

La regla anuncia clase 1 cuando su probabilidad es **mayor o igual que
0.5**; anuncia clase 0 en caso contrario. Queremos maximizar la proporción
de etiquetas acertadas, llamada **accuracy**. Cada ejemplo cuenta lo mismo.

Plantea el modelo completo sin buscar los mejores parámetros. Explica qué
información conserva el objetivo y qué información pierde: compara asignar
probabilidad 0.51 o 0.99 a la clase correcta.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SI TODAVÍA NO HAS HECHO UN INTENTO.**

::: hint {#opt-obj-clas-pista-1a of="opt-obj-clas-ej-1" title="PISTA 1 · Solo si te atoraste"}
| Parte del relato | ¿Está dada o se elige? |
|---|---|
| Entradas y etiquetas correctas | Dadas, una pareja por ejemplo |
| Dos parámetros entre −4 y 4 | Se eligen una sola vez |
| Umbral y regla del empate | Dados |
| Probabilidad de cada ejemplo | Se calcula con la regla elegida |

El objetivo cuenta decisiones correctas, no suma directamente probabilidades.
:::

**ABRE LA PISTA 2 SOLO SI SIGUES ATORADO; DESPUÉS VUELVE A TU HOJA.**

::: hint {#opt-obj-clas-pista-1b of="opt-obj-clas-ej-1" title="PISTA 2 · Solo si te atoraste"}
¿Cómo asignarías un 1 a un acierto y un 0 a un error? ¿Qué necesitas hacer
con esos tres números para obtener una proporción?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-clas-resp-1 of="opt-obj-clas-ej-1"}
**Datos y decisiones.** Sean $I$ los ejemplos, $n=|I|>0$, $x_i$ sus entradas
y $y_i\in\{0,1\}$ sus etiquetas. El dato $M>0$ limita los parámetros.
Las decisiones son $a,b\in[-M,M]$, sin unidades físicas.

**Construir probabilidades y etiquetas.** Abreviamos
$p_i(a,b)=1/(1+e^{-(ax_i+b)})$. La etiqueta anunciada es

$$\widehat y_i(a,b)=
\begin{cases}1&\text{si }p_i(a,b)\ge0.5,\\0&\text{si }p_i(a,b)<0.5.\end{cases}$$

Son expresiones derivadas de $a,b$, no decisiones independientes.
La notación $\mathbf 1\{P\}$ vale 1 cuando la proposición $P$ es verdadera
y 0 cuando es falsa. Así, cada ejemplo aporta
$\mathbf 1\{\widehat y_i(a,b)=y_i\}$.

**Modelo general completo:**

$$\begin{aligned}
\max_{a,b}\quad &\frac1n\sum_{i\in I}
\mathbf 1\{\widehat y_i(a,b)=y_i\}\\
\text{sujeto a}\quad &-M\le a\le M,\\
&-M\le b\le M,\qquad a,b\in\mathbb R.
\end{aligned}$$

**Con los datos del ejercicio**, $I=\{1,2,3\}$, $M=4$ y
$(p_1,p_2,p_3)=(\sigma(b),\sigma(a+b),\sigma(2a+b))$, donde
$\sigma(z)=1/(1+e^{-z})$. El modelo queda

$$\begin{aligned}
\max_{a,b}\quad &\frac{
\mathbf 1\{p_1(a,b)<0.5\}+
\mathbf 1\{p_2(a,b)\ge0.5\}+
\mathbf 1\{p_3(a,b)\ge0.5\}}{3}\\
\text{sujeto a}\quad &-4\le a\le4,\quad -4\le b\le4,\quad a,b\in\mathbb R.
\end{aligned}$$

**Qué mide y qué omite.** Es una proporción sin unidades, entre 0 y 1.
Dar el mismo peso a cada acierto supone que todos los errores cuestan lo
mismo. Una probabilidad 0.51 y una 0.99 para la clase correcta producen
el mismo acierto: el objetivo omite cuánta confianza expresa la regla.

Evaluar accuracy es sencillo. Lo que dificulta usarla para orientar pequeños
cambios de parámetros es que permanece constante mientras ninguna etiqueta
cambie; al cruzar ciertos límites, salta. El siguiente problema revisa la
medida para conservar información probabilística. Si el problema real
penalizara más un tipo de error, también habría que representar esos costos.
:::

## Problema 8 · Evaluar la probabilidad de la clase correcta

::: exercise {#opt-obj-clas-ej-2 title="Cambiar el objetivo sin cambiar el predictor"}
Conserva los tres ejemplos, la regla de probabilidad, el umbral, la regla
del empate y las cotas del problema 7. Ahora importa asignar una probabilidad
alta a la clase correcta, además de poder anunciar una etiqueta.

El equipo propone que cada ejemplo aporte **el negativo del logaritmo
natural de la probabilidad asignada a su clase correcta**. Quiere minimizar
el promedio de esas aportaciones; esta medida se llama **pérdida
logarítmica** o **log loss**.

Construye el modelo completo y explica el signo negativo. Después compara
estas dos reglas permitidas: ambas usan $a=0$; una usa $b=\ln9$ y asigna
probabilidad 0.9 a la clase 1 en todos los ejemplos; la otra usa
$b=\ln(0.49/0.51)$ y asigna 0.49. Puedes usar calculadora.

¿Menor log loss implica necesariamente mayor accuracy en este conjunto?
No necesitas calcular el óptimo de ninguno de los dos modelos.
:::

### Primero construye la nueva medida

**NO ABRAS LA PISTA 1 SIN DISTINGUIR LAS DOS CLASES.**

::: hint {#opt-obj-clas-pista-2a of="opt-obj-clas-ej-2" title="PISTA 1 · Solo si te atoraste"}
La probabilidad que produce la regla corresponde siempre a la clase 1.
Las etiquetas correctas de los tres ejemplos siguen siendo 0, 1 y 1.
Los parámetros de las dos reglas propuestas están dentro de las cotas.
:::

**ABRE LA PISTA 2 SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-clas-pista-2b of="opt-obj-clas-ej-2" title="PISTA 2 · Solo si te atoraste"}
Si la etiqueta correcta es 0, ¿qué probabilidad corresponde a un acierto?
¿Qué sucede con el negativo de su logaritmo cuando esa probabilidad se
acerca a 1? ¿Y cuando se acerca a 0?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-clas-resp-2 of="opt-obj-clas-ej-2"}
**Conservamos** los datos $I,x_i,y_i,M$ y las decisiones $a,b$.
Cuando $y_i=1$, la probabilidad correcta es $p_i(a,b)$; cuando $y_i=0$,
es $1-p_i(a,b)$. La expresión

$$\ell_i(a,b)=-y_i\ln p_i(a,b)-(1-y_i)\ln(1-p_i(a,b))$$

elige el término que corresponde a cada etiqueta: uno de sus coeficientes
vale 1 y el otro 0. Las probabilidades de esta familia están estrictamente
entre 0 y 1, de modo que los logaritmos están definidos.

**Modelo general completo:**

$$\begin{aligned}
\min_{a,b}\quad &\frac1n\sum_{i\in I}
\left[-y_i\ln p_i(a,b)-(1-y_i)\ln(1-p_i(a,b))\right]\\
\text{sujeto a}\quad &-M\le a\le M,\\
&-M\le b\le M,\qquad a,b\in\mathbb R.
\end{aligned}$$

**Con los datos del ejercicio**, se sustituyen las etiquetas 0, 1 y 1:

$$\begin{aligned}
\min_{a,b}\quad &\frac{-\ln(1-\sigma(b))-\ln\sigma(a+b)-\ln\sigma(2a+b)}{3}\\
\text{sujeto a}\quad &-4\le a\le4,\quad -4\le b\le4,\quad a,b\in\mathbb R.
\end{aligned}$$

**Sentido y escala.** Para una probabilidad correcta $r\in(0,1)$,
$-\ln r$ es positivo, se aproxima a 0 cuando $r$ se aproxima a 1 y crece
sin límite cuando $r$ se aproxima a 0. Minimizarlo favorece probabilidades
altas para lo que ocurrió y penaliza errores muy confiados. Con logaritmo
natural, la escala se expresa en **nats por ejemplo**; no es porcentaje de
errores. El signo negativo ya forma parte de la pérdida: no se vuelve a negar.

**Comprobación de las dos reglas:**

| Probabilidad de clase 1 | Aciertos | Log loss |
|---|---:|---:|
| 0.9 | 2/3 | 0.838 |
| 0.49 | 1/3 | 0.700 |

Los promedios se calculan como $(-\ln0.1-2\ln0.9)/3$ para la primera
regla y $(-\ln0.51-2\ln0.49)/3$ para la segunda. Los valores de la tabla
están redondeados.

La segunda regla baja la pérdida y acierta menos etiquetas. En la primera,
el error sobre el ejemplo de clase 0 recibe una penalización considerable.
Así queda refutada la garantía de que **cada reducción de log loss** aumente
accuracy. No hemos comparado los óptimos globales de ambos problemas.

**Por qué elegirla y qué deja fuera.** Log loss distingue probabilidades
que accuracy trata igual y, en esta familia, varía suavemente con los
parámetros. Es defendible cuando también queremos evaluar probabilidades;
puede servir como objetivo sustituto cuando la medida final es accuracy.
No garantiza que cada cambio favorezca esa medida final ni incorpora costos
distintos de equivocarse. Para juzgar el resultado conviene conservar ambas
medidas y, al evaluar predicción futura, usar ejemplos que no determinaron
el ajuste. Ninguna de las dos cifras de entrenamiento demuestra por sí sola
cómo se comportará la regla con datos nuevos.
:::

Después de comparar tus modelos, pasa a [[opt-objetivo-clasificacion-modelo|la formulación general de clasificación]].
