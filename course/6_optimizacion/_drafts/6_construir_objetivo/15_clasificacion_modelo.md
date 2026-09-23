---
id: opt-objetivo-clasificacion-modelo
title: Dos formas de evaluar una regla de clasificación
nav_title: Clasificación · Modelo general
summary: "Contar etiquetas acertadas o evaluar probabilidades, y explicar por qué elegir una medida cambia el ajuste."
status: ready
tags: [optimizacion, modelado, clasificacion]
---

# Dos formas de evaluar una regla de clasificación

Esta es una **consulta opcional** que amplía el [[opt-objetivo-clasificacion-practica|ejemplo guiado de clasificación]].
Tanto al maximizar los aciertos como al minimizar la pérdida logarítmica,
queremos ajustar una regla que distinga entre las clases 0 y 1.
Usamos los mismos casos y ajustamos los mismos parámetros, pero cambiamos
la medida que decide qué ajuste preferimos.

Esa elección exige precisar el propósito. Si nos interesa acertar etiquetas,
podemos contar los aciertos. Si también nos interesan las probabilidades,
necesitamos una medida que distinga entre reglas que anuncian las mismas
etiquetas con probabilidades diferentes.

La pérdida logarítmica es una propuesta para ese segundo propósito. A
continuación construimos ambos modelos y revisamos qué podemos concluir
al compararlos.

## 1 · Calcular probabilidades y anunciar etiquetas

En el ejemplo guiado usamos el número de enlaces de cada mensaje como única
entrada. Ahora permitimos varias características o **atributos** por caso: el dato $x_{ij}$ es el valor del
atributo $j$ en el caso $i$. Todas las entradas se expresan en escalas
numéricas sin unidades físicas, como antes.

**Estos son los datos conocidos:**

- $I$: Conjunto finito, no vacío, de casos.
- $J$: Conjunto finito, no vacío, de atributos.
- $n$: Cantidad de casos.
- $x_{ij}$: Valor real del atributo $j$ en el caso $i$.
- $y_i$: Etiqueta correcta del caso $i$, igual a 0 o 1.

El número de casos es $n=|I|>0$.

**Elegimos un peso $w_j$ para cada atributo y una constante $b$.** Son
números reales, sin unidades físicas, que compartimos entre todos los
casos. En el ejemplo guiado hay una sola entrada: $w_1=\beta$ y
$b=\alpha$. Al combinar cada entrada con su peso y sumar la constante,
obtenemos un número al que aplicamos la sigmoide:

$$p_i(w,b)=\sigma\left(\sum_{j\in J}w_jx_{ij}+b\right).$$

$$\sigma(z)=\frac{1}{1+e^{-z}}.$$

Esta fórmula define la familia de reglas que estamos considerando. Su
resultado $p_i$ es la probabilidad asignada a la clase 1; a la clase 0 le
corresponde $1-p_i$.

Las probabilidades se calculan a partir de los parámetros. Si las
eligiéramos libremente para cada caso, ya no estaríamos ajustando una regla
compartida de esta familia.

**Para anunciar la etiqueta**, comparamos $p_i$ con 0.5. El empate da
clase 1, igual que en el ejemplo guiado:

$$\widehat y_i(w,b)=\mathbf1\{p_i(w,b)\ge0.5\}.$$

El símbolo $\mathbf1\{P\}$ vale 1 cuando la afirmación $P$ es verdadera
y 0 cuando es falsa. La etiqueta anunciada tampoco es una decisión
independiente: queda determinada por los parámetros.

Permitimos cualquier peso real y cualquier intercepto real:

$$w_j\in\mathbb R\quad(j\in J),\qquad b\in\mathbb R.$$

No imponemos cotas adicionales a los parámetros.

## 2 · Contar aciertos

Para evaluar un caso, comparamos la etiqueta anunciada $\widehat y_i$ con
la correcta $y_i$. Contamos un acierto cuando coinciden y ninguno cuando
son distintas. Sumamos los aciertos y dividimos entre el número de casos.

Esa proporción se llama **accuracy**. Si todos los casos cuentan lo mismo
y queremos acertar tantas etiquetas como sea posible, el modelo es

$$\begin{aligned}
\max_{w,b}\quad &\frac1n\sum_{i\in I}
\mathbf1\{\widehat y_i(w,b)=y_i\}\\
\text{sujeto a}\quad &w_j\in\mathbb R\quad(j\in J),\qquad b\in\mathbb R.
\end{aligned}$$

El objetivo no tiene unidades y toma valores entre 0 y 1. Acertar en un
caso compensa fallar en otro por la misma cantidad. No registra si la
probabilidad asignada a la clase correcta era 0.51 o 0.99: ambas producen
un acierto.

**El conteo puede permanecer igual aunque cambien las probabilidades.**
Si una modificación de los parámetros conserva todas las etiquetas,
también conserva accuracy. Por eso esta función es constante en regiones
del espacio de parámetros y salta cuando cambia el conteo de aciertos.

Esto limita la información disponible para orientar pequeños ajustes con
derivadas o gradientes: dentro de una región donde el objetivo no cambia,
no indica cómo mejorar. No significa que contar aciertos sea difícil.
Aquí formulamos el problema, sin elegir un algoritmo para resolverlo.

## 3 · Evaluar probabilidades

Podemos interesarnos también por la probabilidad que la regla asigna a la
clase correcta. Para el caso $i$, llamemos $r_i$ a esa probabilidad:

- Si la etiqueta correcta es 1, usamos $r_i=p_i$.
- Si la etiqueta correcta es 0, usamos $r_i=1-p_i$.

La **pérdida logarítmica** propone evaluar cada caso mediante $-\ln r_i$.
El signo negativo hace que la pérdida sea positiva y que disminuya cuando
la probabilidad correcta aumenta. Se acerca a 0 cuando esa probabilidad
se acerca a 1 y crece sin límite cuando se acerca a 0.

Elegir esta pérdida es una decisión del modelo. Querer probabilidades
altas para la clase correcta explica el propósito, pero no determina una
única fórmula para medirlo.

**Una expresión reúne las dos etiquetas:**

$$
\begin{aligned}
\ell_i(w,b)={}&-y_i\ln p_i(w,b)\\
&-(1-y_i)\ln\bigl(1-p_i(w,b)\bigr).
\end{aligned}
$$

Cuando $y_i=1$, solo queda el primer término. Cuando $y_i=0$, solo queda
el segundo. Así usamos en cada caso la probabilidad de su clase correcta.

Con parámetros finitos, la sigmoide mantiene $0<p_i<1$ y ambos logaritmos
están definidos. Como usamos logaritmos naturales, el promedio se expresa
en **nats por ejemplo**, no como porcentaje de errores. Esta es la
[pérdida logarítmica binaria documentada por scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html).

**El modelo minimiza el promedio de las pérdidas** y conserva exactamente
las mismas decisiones permitidas:

$$\begin{aligned}
\min_{w,b}\quad &\frac1n\sum_{i\in I}\ell_i(w,b)\\
\text{sujeto a}\quad &w_j\in\mathbb R\quad(j\in J),\qquad b\in\mathbb R.
\end{aligned}$$

En esta familia, la pérdida es suave y convexa en los parámetros. Puede
registrar cambios en las probabilidades aunque ninguna cruce el umbral
que cambia una etiqueta.

La convexidad no garantiza un mínimo finito: si podemos dar puntajes
estrictamente positivos a todos los casos de clase 1 y estrictamente
negativos a los de clase 0, escalar los parámetros acerca la pérdida a cero
sin alcanzarlo. No hemos impuesto cotas que impidan ese crecimiento.

Si nos interesa evaluar esas probabilidades, log loss puede ser una medida
de interés por sí misma. Si al final solo nos importa accuracy, usar log
loss para ajustar significa elegir un **objetivo sustituto**: optimizamos
una medida con la intención de obtener un buen resultado en otra.

En ese segundo uso necesitamos comprobar el resultado con la medida final.
Las dos funciones no se vuelven idénticas por aplicarlas a las mismas
reglas, y mejorar una no garantiza mejorar la otra en cada comparación.

## 4 · Comparar reglas constantes

El ejemplo guiado compara un conjunto hipotético con $n$ múltiplo de 3:
dos terceras partes de las etiquetas son 1 y la tercera parte restante es 0.
Podemos reproducir la comparación con cualquier número de atributos,
fijando todos los pesos en cero. Así, cada caso recibe la misma probabilidad
$p$ de clase 1. Para cualquier $p$ entre 0 y 1, sin incluir los extremos,
fijamos

$$w_j=0\qquad(j\in J).$$

$$b=\ln\frac{p}{1-p}.$$

En la notación del ejemplo guiado, esto corresponde a $\beta=0$ y
$\alpha=\ln(p/(1-p))$. Todos estos parámetros son reales y están permitidos.
Las entradas no afectan a una regla constante.

Si $p\ge0.5$, anunciamos clase 1 para todos y acertamos dos terceras partes
de los casos. Si $p<0.5$, anunciamos clase 0 y acertamos una tercera parte.
La pérdida promedio es

$$-\frac23\ln p-\frac13\ln(1-p).$$

Estas son tres comparaciones permitidas; las pérdidas están redondeadas:

| $p$ | Aciertos | Pérdida |
|---|---:|---:|
| 0.49 | 1/3 | 0.700 |
| 2/3 | 2/3 | 0.637 |
| 0.9 | 2/3 | 0.838 |

Pasar de 0.49 a 2/3 mejora ambas medidas. Pasar de 0.9 a 2/3 reduce la
pérdida sin cambiar las etiquetas. Pero pasar de 0.9 a 0.49 reduce la pérdida
**y también reduce los aciertos**: la regla de 0.9 penaliza mucho los casos
de clase 0, a los que asigna solo 0.1 de probabilidad de su clase correcta.

Este último contraejemplo basta para rechazar que cada reducción de la
pérdida aumente accuracy. No identifica los mejores parámetros posibles
ni demuestra que los óptimos de ambos problemas sean distintos.

## 5 · Comprobar qué falta evaluar

Los dos modelos dan el mismo peso a todos los casos. Si equivocarse con
una clase costara más que equivocarse con la otra, necesitaríamos datos
sobre esos costos y decidir cómo representarlos. Las medidas anteriores
no hacen esa distinción.

Tampoco basta evaluar los casos usados para ajustar la regla si
queremos saber cómo funcionará con casos nuevos. Esa comprobación necesita
otros datos, que no hayan determinado los parámetros.

Al justificar el objetivo, deja claras estas tres decisiones:

- **Qué quieres conseguir:** acertar etiquetas, evaluar probabilidades o ambas cosas.
- **Qué medida vas a optimizar:** qué cuenta y qué diferencias deja fuera.
- **Cómo comprobarás el resultado:** con qué medida y con qué datos juzgarás la regla obtenida.

Un objetivo sustituto necesita tanto una razón para elegirlo como una
comprobación frente al propósito que motivó el ajuste.

[[opt-objetivo-clasificacion-practica|Volver al ejemplo guiado]] · [[opt-construir-objetivo|Volver al banco de práctica]].
