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
- $M>0$: Cota para la magnitud de cada parámetro.

El número de casos es $n=|I|>0$.

**Elegimos un peso $w_j$ para cada atributo y una constante $b$.** Son
números reales, sin unidades físicas, que compartimos entre todos los
casos. Al combinar cada entrada con su peso y sumar la constante, obtenemos
un número al que aplicamos la sigmoide:

$$p_i(w,b)=\sigma\left(\sum_{j\in J}w_jx_{ij}+b\right),
\qquad \sigma(z)=\frac{1}{1+e^{-z}}.$$

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

**Cada parámetro debe estar entre $-M$ y $M$.** Llamamos $\Theta$ al conjunto
de todas las elecciones permitidas:

$$\Theta=\{(w,b):w_j\in\mathbb R,\ -M\le w_j\le M\ (j\in J),
\ b\in\mathbb R,\ -M\le b\le M\}.$$

Estas cotas forman parte del problema planteado. No son una condición
obligatoria de todos los modelos de clasificación.

## 2 · Contar aciertos

Para evaluar un caso, comparamos la etiqueta anunciada $\widehat y_i$ con
la correcta $y_i$. Contamos un acierto cuando coinciden y ninguno cuando
son distintas. Sumamos los aciertos y dividimos entre el número de casos.

Esa proporción se llama **accuracy**. Si todos los casos cuentan lo mismo
y queremos acertar tantas etiquetas como sea posible, el modelo es

$$\begin{aligned}
\max_{w,b}\quad &\frac1n\sum_{i\in I}
\mathbf1\{\widehat y_i(w,b)=y_i\}\\
\text{sujeto a}\quad &(w,b)\in\Theta.
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

$$\ell_i(w,b)=-y_i\ln p_i(w,b)-(1-y_i)\ln(1-p_i(w,b)).$$

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
\text{sujeto a}\quad &(w,b)\in\Theta.
\end{aligned}$$

En esta familia, la pérdida varía suavemente con los parámetros. Puede
registrar cambios en las probabilidades aunque ninguna cruce el umbral
que cambia una etiqueta.

Si nos interesa evaluar esas probabilidades, log loss puede ser una medida
de interés por sí misma. Si al final solo nos importa accuracy, usar log
loss para ajustar significa elegir un **objetivo sustituto**: optimizamos
una medida con la intención de obtener un buen resultado en otra.

En ese segundo uso necesitamos comprobar el resultado con la medida final.
Las dos funciones no se vuelven idénticas por aplicarlas a las mismas
reglas, y mejorar una no garantiza mejorar la otra en cada comparación.

## 4 · Comparar dos reglas permitidas

En el ejemplo guiado hay un atributo, el número de enlaces del mensaje, de modo
que $w_1=a$. La cota es $M=4$; las entradas son 0, 1 y 2. El primer mensaje
es normal y los otros dos son no deseados: sus etiquetas son 0, 1 y 1. Al
sustituir estos datos, la proporción de aciertos es

$$A(a,b)=\frac{\mathbf1\{\sigma(b)<0.5\}
+\mathbf1\{\sigma(a+b)\ge0.5\}
+\mathbf1\{\sigma(2a+b)\ge0.5\}}3.$$

La pérdida logarítmica promedio es

$$L(a,b)=\frac{-\ln(1-\sigma(b))-\ln\sigma(a+b)-\ln\sigma(2a+b)}3.$$

Los dos problemas consisten en maximizar $A(a,b)$ o minimizar $L(a,b)$,
sujetos a $a,b\in[-4,4]$. No necesitamos resolverlos para comprobar si una
mejora de pérdida siempre acompaña a una mejora de accuracy: basta encontrar
una comparación que contradiga esa afirmación.

Tomamos $a=0$, con lo que la probabilidad de clase 1 es la misma en todos
los casos. Las dos parejas siguientes respetan las cotas:

La primera usa $b=\ln9$ y la segunda, $b=\ln(0.49/0.51)$. La tabla
muestra las aproximaciones de $b$ y la probabilidad $p$ de clase 1:

| Regla | $b$ aprox. | $p$ |
|---|---:|---:|
| Primera | 2.197 | 0.9 |
| Segunda | −0.040 | 0.49 |

La primera anuncia clase 1 en los tres casos y acierta dos. La segunda
anuncia clase 0 en los tres y acierta uno. Al calcular también sus pérdidas,
obtenemos estos valores redondeados:

| Regla | Accuracy | Log loss |
|---|---:|---:|
| Primera | 2/3 | 0.838 |
| Segunda | 1/3 | 0.700 |

**La segunda regla reduce la pérdida, pero también reduce los aciertos.**
La primera recibe una penalización considerable por asignar probabilidad
0.1 a la clase correcta del caso cuya etiqueta es 0.

Este contraejemplo basta para rechazar la garantía en cada comparación.
No identifica los mejores parámetros posibles ni demuestra que los óptimos
de ambos problemas sean distintos en este conjunto.

## 5 · Comprobar qué falta evaluar

Los dos modelos dan el mismo peso a todos los casos. Si equivocarse con
una clase costara más que equivocarse con la otra, necesitaríamos datos
sobre esos costos y decidir cómo representarlos. Las medidas anteriores
no hacen esa distinción.

Tampoco basta evaluar los tres casos usados para ajustar la regla si
queremos saber cómo funcionará con casos nuevos. Esa comprobación necesita
otros datos, que no hayan determinado los parámetros.

Al justificar el objetivo, deja claras estas tres decisiones:

- **Qué quieres conseguir:** acertar etiquetas, evaluar probabilidades o ambas cosas.
- **Qué medida vas a optimizar:** qué cuenta y qué diferencias deja fuera.
- **Cómo comprobarás el resultado:** con qué medida y con qué datos juzgarás la regla obtenida.

Un objetivo sustituto necesita tanto una razón para elegirlo como una
comprobación frente al propósito que motivó el ajuste.

[[opt-objetivo-clasificacion-practica|Volver al ejemplo guiado]] · [[opt-construir-objetivo|Volver al banco de práctica]].
