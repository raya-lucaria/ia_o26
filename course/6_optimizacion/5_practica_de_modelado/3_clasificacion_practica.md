---
id: opt-objetivo-clasificacion-practica
title: Clasificar mensajes y evaluar probabilidades
nav_title: Clasificación
summary: "Construir una regla para dos clases y comparar contar aciertos con evaluar las probabilidades asignadas."
status: ready
estimated_time: 20m
tags: [optimizacion, modelado, clasificacion]
---

# Clasificar mensajes y evaluar probabilidades

**Clasificar** consiste en decidir a qué grupo pertenece un caso. Aquí
trabajaremos con dos clases, llamadas 0 y 1. Primero construiremos una regla
para asignarlas; después compararemos dos maneras de decidir qué regla es mejor.

## 1 · Distinguir los datos de lo que vamos a elegir

Tenemos $n\ge1$ casos ya revisados. Para cada caso conocemos una entrada
numérica y su clase correcta. Los escribimos como

$$(x_i,y_i),\qquad i=1,\ldots,n.$$

El índice $i$ identifica un caso; $x_i\in\mathbb R$ es su entrada y
$y_i\in\{0,1\}$, su etiqueta. Las entradas pueden tomar muchos valores:
**tener dos clases no significa que la entrada también deba ser binaria**.

Para darles un significado concreto, pensemos en mensajes: $y_i=1$ indica
un mensaje fraudulento y $y_i=0$, uno legítimo. La entrada $x_i$ cuenta
cuántos enlaces contiene. En este ejemplo es un entero no negativo; podría
valer 0, 1, 2 o más.

El número de enlaces puede ser una señal para clasificar, pero por sí solo
no garantiza que un mensaje sea fraudulento. Usaremos los mensajes revisados
para ajustar una regla y comprobar qué consigue con esa información.

**Piensa: ¿podemos cambiar las etiquetas para que nuestra regla acierte más?**

No. Las entradas y las etiquetas son **datos conocidos**. Elegiremos los
parámetros de la regla; no modificaremos los casos para mejorar su puntuación.

## 2 · Convertir una entrada en una probabilidad y una etiqueta

Elegimos dos números reales: $\alpha$, el **intercepto**, y $\beta$, la
**pendiente**. Con ellos calculamos un puntaje para cada caso:

$$z_i(\alpha,\beta)=\alpha+\beta x_i.$$

El intercepto fija el puntaje cuando la entrada vale cero. La pendiente
indica cuánto cambia ese puntaje al aumentar la entrada en una unidad.
Usamos **la misma pareja de parámetros para todos los casos** y permitimos
cualquier valor real:

$$\alpha,\beta\in\mathbb R.$$

**Piensa: el puntaje puede ser negativo o mayor que uno; ¿cómo lo convertiríamos en una probabilidad?**

Aquí proponemos una función concreta, llamada **sigmoide**:

$$\sigma(z)=\frac{1}{1+e^{-z}}.$$

La aplicamos al puntaje para estimar la probabilidad de clase 1:

$$p_i(\alpha,\beta)=\sigma\bigl(z_i(\alpha,\beta)\bigr).$$

La sigmoide transforma cualquier puntaje real en un número estrictamente
entre 0 y 1. A la clase 0 le asignamos el complemento $1-p_i(\alpha,\beta)$.
Esta regla se llama [regresión logística](https://cs229.stanford.edu/notes_archive/cs229-notes-all/cs229-notes1.pdf); aquí tiene una sola entrada.

![La sigmoide transforma el puntaje z en una probabilidad p: pasa por p igual a 0.5 cuando z es cero y se aproxima a 0 y 1 sin alcanzarlos](../_assets/opt-clasificacion-sigmoide.svg)

El eje horizontal de la gráfica es **el puntaje**, no el número de enlaces.
Cuando $\beta$ es positiva, más enlaces elevan el puntaje; cuando es negativa,
lo reducen. Esa relación depende de los parámetros que elijamos.

Que las dos probabilidades sumen 1 permite usarlas como un modelo
probabilístico. No demuestra que estén bien **calibradas**: asignar 0.8 a
ciertos mensajes no garantiza que el 80 % de ellos sean fraudulentos.
Eso tendría que comprobarse con datos.

Para anunciar una etiqueta fijamos el umbral en 0.5. **El empate da clase 1**:

$$
\widehat y_i(\alpha,\beta)=
\begin{cases}
1 &\text{si }p_i(\alpha,\beta)\ge0.5,\\
0 &\text{si }p_i(\alpha,\beta)<0.5.
\end{cases}
$$

Solo elegimos $\alpha$ y $\beta$. El puntaje, la probabilidad y la etiqueta
se calculan a partir de ellos; no podemos escogerlos por separado para
hacer que cada mensaje salga bien.

## 3 · Contar cuántas etiquetas acertamos

Queremos acertar tantas etiquetas como sea posible y damos el mismo peso
a cada caso. **Piensa: ¿cómo contarías un acierto y dejarías fuera un error?**

Usamos un **indicador**, escrito $\mathbf1\{\cdot\}$: vale 1 cuando lo que
está entre llaves es verdadero y 0 cuando es falso. Así,
$\mathbf1\{\widehat y_i(\alpha,\beta)=y_i\}$ cuenta el acierto del caso $i$.
Sumamos los aciertos y dividimos entre el número de casos:

$$A(\alpha,\beta)=\frac1n\sum_{i=1}^n
\mathbf1\{\widehat y_i(\alpha,\beta)=y_i\}.$$

Esta proporción se llama **accuracy**. Toma valores entre 0 y 1 y no tiene
unidades. Nuestro primer problema de optimización es

$$\max_{\alpha,\beta\in\mathbb R}\quad A(\alpha,\beta).$$

**Piensa: si la clase correcta es 1, ¿cuenta distinto acertar con probabilidad 0.51 que con 0.99?**

No: ambos casos cuentan un acierto. Podemos cambiar los parámetros y las
probabilidades sin cambiar ninguna etiqueta. Mientras eso ocurra, accuracy
permanece en una **meseta**: su valor no cambia. Cuando una probabilidad cruza
el umbral, el conteo puede saltar.

Aunque los parámetros sean continuos, este objetivo es, en general,
**discontinuo y no cóncavo**. Maximizarlo no es un problema de optimización
convexa en general. Dentro de una meseta, sus derivadas no señalan cómo
conseguir más aciertos.

## 4 · Valorar la probabilidad de la clase correcta

Podemos evaluar algo que el conteo de aciertos deja fuera: **cuánta
probabilidad recibe la clase correcta**. Proponemos usar el negativo de su
logaritmo natural, una medida llamada **pérdida logarítmica** o *log loss*.

Es una elección del modelo. Interesarse por las probabilidades no obliga
a usar esta fórmula; vamos a examinar qué mide y qué facilita al ajustar.

**Piensa: si la etiqueta correcta es 0, ¿debemos evaluar la probabilidad de clase 1 o su complemento?**

Evaluamos $p_i$ cuando $y_i=1$ y $1-p_i$ cuando $y_i=0$. Las pérdidas de
cada caso son, respectivamente, $-\ln p_i$ y $-\ln(1-p_i)$.

![Pérdida logarítmica frente a la probabilidad p de clase 1: para y igual a 1 disminuye al aumentar p, y para y igual a 0 aumenta; ambas penalizan sin límite la confianza en la clase equivocada](../_assets/opt-clasificacion-log-loss.svg)

La pérdida se acerca a cero cuando la probabilidad de la clase correcta
se acerca a uno. Crece sin límite cuando esa probabilidad se acerca a cero.
Así, **equivocarse con mucha confianza recibe una penalización grande**.

Reunimos los dos casos en una sola expresión:

$$
\begin{aligned}
\ell_i(\alpha,\beta)={}&-y_i\ln p_i(\alpha,\beta)\\
&-(1-y_i)\ln\bigl(1-p_i(\alpha,\beta)\bigr).
\end{aligned}
$$

Como $y_i$ vale 0 o 1, uno de los dos términos desaparece. Para parámetros
finitos, la sigmoide mantiene positivos los argumentos de ambos logaritmos.
Promediamos las pérdidas de los $n$ casos:

$$L(\alpha,\beta)=\frac1n\sum_{i=1}^n\ell_i(\alpha,\beta).$$

El segundo problema de optimización es

$$\min_{\alpha,\beta\in\mathbb R}\quad L(\alpha,\beta).$$

La pérdida promedio se expresa en **nats por caso**, porque usamos
logaritmos naturales. No es un porcentaje de errores.

Con esta regla logística, $L$ es **suave y convexa** en $\alpha,\beta$;
no es una función lineal. Sus derivadas pueden orientar cambios de los
parámetros para reducirla, incluso cuando las etiquetas todavía no cambian.
Esa es una razón para usarla como **objetivo sustituto** al ajustar una regla
con la que queremos acertar etiquetas.

La convexidad no garantiza que aquí exista un mínimo con parámetros finitos.
Si los datos se pueden separar con puntajes estrictamente positivos para
la clase 1 y estrictamente negativos para la clase 0, podemos multiplicar
los parámetros por números cada vez mayores. La pérdida se acerca a cero
sin alcanzarlo. Hemos dejado los parámetros sin límites; en ese caso la
formulación tiene un ínfimo, pero no una pareja finita que lo alcance.

## 5 · Comprobar cuándo coinciden las dos medidas

**Piensa: ¿reducir la pérdida siempre aumenta los aciertos?**

Consideremos un conjunto hipotético donde $n$ es múltiplo de 3 y dos
terceras partes de las etiquetas son 1. La tercera parte restante es 0.
No necesitamos fijar las entradas para comparar reglas **constantes**:
con $\beta=0$, todos los casos reciben la misma probabilidad $p$ de clase 1.
Para obtenerla elegimos

$$\alpha=\ln\frac{p}{1-p},\qquad 0<p<1.$$

Las tres reglas de la tabla pertenecen a nuestra familia. La pérdida
promedio de cada una se calcula con

$$-\frac23\ln p-\frac13\ln(1-p).$$

Las pérdidas están redondeadas y las fracciones de aciertos son exactas.

| $p$ | Aciertos | Pérdida |
|---|---:|---:|
| 0.49 | 1/3 | 0.700 |
| 2/3 | 2/3 | 0.637 |
| 0.9 | 2/3 | 0.838 |

Al pasar de 0.49 a 2/3, **mejoran ambas medidas**: baja la pérdida y sube
la proporción de aciertos. Pasar de 0.9 a 2/3 también reduce la pérdida,
pero conserva las etiquetas y, por tanto, los aciertos.

En cambio, pasar de 0.9 a 0.49 reduce la pérdida **y reduce los aciertos**.
La regla de 0.9 penaliza mucho a los casos de clase 0: les asigna solo 0.1
de probabilidad de pertenecer a su clase correcta.

Estos ejemplos muestran que los criterios pueden coincidir o discrepar.
No hemos encontrado los óptimos globales de los dos problemas ni probado
que sean distintos. Tampoco hay una garantía de que cada mejora de la
pérdida mejore accuracy.

## 6 · Distinguir qué optimizamos de cuánto cuesta hacerlo

**Piensa: ¿un objetivo suave siempre se puede optimizar más rápido que uno con saltos?**

No basta con mirar la forma del objetivo. También importan la familia de
reglas, el algoritmo y la precisión que buscamos. Aquí solo tenemos una
entrada y dos parámetros.

Para una pareja fija $\alpha,\beta$, evaluar accuracy o la pérdida requiere
recorrer los $n$ casos: cuesta $O(n)$ operaciones. En la pérdida logística,
un paso de **descenso por gradiente con todos los datos** también cuesta
$O(n)$: reúne las contribuciones de los casos para ajustar los dos parámetros.
Hacer $T$ iteraciones cuesta $O(Tn)$, bajo el conteo usual de operaciones
aritméticas. El número $T$ no es una constante garantizada: depende de los
datos, del método y de la precisión buscada.

Para accuracy podemos aprovechar una particularidad de este modelo.
Como $p_i\ge0.5$ equivale a $\alpha+\beta x_i\ge0$, una regla no constante
separa las entradas mediante un **corte**: anuncia clase 1 a un lado y
clase 0 al otro.

Podemos ordenar las entradas, mantener juntas las que tengan el mismo valor
y recorrer los cortes en ambas orientaciones. También incluimos las dos
reglas constantes. Ordenar cuesta $O(n\log n)$; actualizar los conteos al
recorrer los cortes cuesta $O(n)$. Así podemos encontrar un máximo exacto
de accuracy en **$O(n\log n)$**, sin buscar todas las parejas reales.

Volver a contar los $n$ casos desde cero para cada corte daría un barrido
innecesario de $O(n^2)$. Mejorar ese algoritmo es distinto de cambiar el
objetivo. **Usar log loss no garantiza resolver más rápido**: facilita
ajustes guiados por derivadas y evalúa probabilidades, pero optimiza otra medida.

Si el propósito es acertar etiquetas, debemos comprobar accuracy después
del ajuste. Para evaluar mensajes nuevos necesitamos además **datos que no
hayan intervenido en ese ajuste**. Ninguno de los dos objetivos garantiza
por sí solo buenos resultados fuera de los casos usados.

## 7 · Resumen de los dos modelos

Los datos son $n\ge1$ pares $(x_i,y_i)$, con $i=1,\ldots,n$,
$x_i\in\mathbb R$ y $y_i\in\{0,1\}$. En el ejemplo, $x_i$ cuenta enlaces
y la clase 1 significa fraude. Ajustamos una sola regla para todos los casos.

| Símbolo | Qué representa |
|---|---|
| $n$ | Número de casos |
| $i$ | Índice de caso |
| $x_i$ | Entrada del caso |
| $y_i$ | Clase correcta |
| $\alpha$ | Intercepto |
| $\beta$ | Pendiente |
| $z_i$ | Puntaje |
| $\sigma$ | Sigmoide |
| $p_i$ | Probabilidad de clase 1 |
| $\widehat y_i$ | Clase anunciada |
| $\mathbf1\{\cdot\}$ | Indicador |
| $A$ | Proporción de aciertos |
| $\ell_i$ | Pérdida del caso |
| $L$ | Pérdida promedio |

**Las decisiones son $\alpha,\beta\in\mathbb R$.** Las entradas y las
etiquetas son datos. Los puntajes $z_i$, las probabilidades $p_i$, las
etiquetas anunciadas $\widehat y_i$ y las medidas se calculan a partir de
los datos y los parámetros elegidos. La sigmoide y el umbral forman parte
de la regla fijada:

$$z_i(\alpha,\beta)=\alpha+\beta x_i.$$

$$\sigma(z)=\frac{1}{1+e^{-z}},\qquad
p_i(\alpha,\beta)=\sigma\bigl(z_i(\alpha,\beta)\bigr).$$

$$
\widehat y_i(\alpha,\beta)=
\begin{cases}
1 &\text{si }p_i(\alpha,\beta)\ge0.5,\\
0 &\text{si }p_i(\alpha,\beta)<0.5.
\end{cases}
$$

El umbral es fijo y el empate da clase 1. La probabilidad de clase 0 es
$1-p_i$; ninguna de las dos probabilidades se elige por separado.

**Modelo 1 · Maximizar los aciertos.** El indicador vale 1 si acertamos
y 0 si nos equivocamos. La formulación completa es

$$
\begin{aligned}
&\max_{\alpha,\beta\in\mathbb R}\quad A(\alpha,\beta),\\
&A(\alpha,\beta)=\frac1n\sum_{i=1}^n
\mathbf1\{\widehat y_i(\alpha,\beta)=y_i\}.
\end{aligned}
$$

Es optimización con parámetros continuos y un objetivo con saltos, no
cóncavo en general. En esta familia de una sola entrada podemos resolverla
exactamente ordenando y recorriendo cortes, en $O(n\log n)$.

**Modelo 2 · Minimizar la pérdida logarítmica promedio.** Para cada caso,
la pérdida evalúa la probabilidad de su clase correcta:

$$
\begin{aligned}
\ell_i(\alpha,\beta)={}&-y_i\ln p_i(\alpha,\beta)\\
&-(1-y_i)\ln\bigl(1-p_i(\alpha,\beta)\bigr).
\end{aligned}
$$

La formulación completa es

$$
\begin{aligned}
&\min_{\alpha,\beta\in\mathbb R}\quad L(\alpha,\beta),\\
&L(\alpha,\beta)=\frac1n\sum_{i=1}^n\ell_i(\alpha,\beta).
\end{aligned}
$$

Es **minimización convexa, suave y no lineal**. Un método posible es descenso
por gradiente con todos los datos: $O(n)$ por iteración, $O(Tn)$ para $T$
iteraciones. Si los datos son separables, puede no haber un mínimo finito.
Reducir esta pérdida no garantiza aumentar la proporción de aciertos.

Algo parecido ocurre al contar aciertos en una actividad educativa:
responder bien con ayuda no demuestra que después se responderá sin ella.
En [[opt-objetivo-aprendizaje-practica|la práctica de aprendizaje]] revisarás esa diferencia.

Consulta opcional: [[opt-objetivo-clasificacion-modelo|generalizar la regla a varias características]].

Siguiente ejemplo: [[opt-objetivo-juego-practica|elegir una jugada cuando el rival responde]].
