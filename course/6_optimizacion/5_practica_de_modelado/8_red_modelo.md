---
id: opt-modelo-red
title: Ajustar una misma regla para todos los clips
nav_title: Red · Modelo general
summary: "Construir la salida y el error de cada clip usando pesos compartidos, y limitar esos pesos sin cambiar el objetivo."
status: ready
tags: [optimizacion, modelado, convexidad]
---

# Ajustar una misma regla para todos los clips

**Primero intenta los [[opt-practica-red|dos problemas de la salida neuronal]].**
Queremos elegir pesos y una constante para que una sola regla aproxime
los puntajes de todos los clips. Las entradas de esa regla ya están
calculadas: las etapas anteriores de la red permanecen fijas.

El criterio también está dado: minimizar la suma de errores cuadrados.
Nuestro trabajo consiste en traducirlo, distinguir las decisiones de los
datos y, en la segunda variante, añadir la condición sobre los pesos.

## 1 · Separar los datos de los ajustes

Cada clip tiene sus propias entradas y su puntaje de referencia. Llamemos
$I$ al conjunto de clips y $J$ al conjunto de entradas de la salida; ambos
son finitos y no vacíos.

**Los datos** son números reales conocidos:

- $h_{ij}$: Entrada $j$ ya calculada para el clip $i$.
- $t_i$: Puntaje de referencia del clip $i$.

**Las decisiones** son los números reales que ajustamos:

- $w_j$: Peso que multiplica la entrada $j$.
- $b$: Constante que se suma a la salida, también llamada sesgo.

Un peso lleva índice $j$, pero no $i$: **usamos el mismo peso en todos los
clips**. La constante $b$ también es única. Si eligiéramos pesos diferentes
para cada clip, tendríamos varias reglas en lugar de la regla compartida
que pide el enunciado.

Los pesos y la constante pueden ser negativos, positivos o cero. Eso se
expresa permitiendo cualquier valor real. Todos los valores están en la
escala sin unidades físicas del ejercicio.

## 2 · Calcular la salida y el error de un clip

Para el clip $i$, multiplicamos cada entrada por su peso y sumamos esos
productos. Después añadimos la constante:

$$\text{salida del clip }i=\sum_{j\in J}h_{ij}w_j+b.$$

Ahora comparamos esa salida con el puntaje de referencia $t_i$. La
diferencia es el error del clip; elevamos esa diferencia al cuadrado,
como pide el criterio del equipo:

$$\text{error cuadrado del clip }i=
\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2.$$

**Calculamos un cuadrado por clip y luego los sumamos.** La suma sobre
$j$ recorre las entradas de un solo clip para obtener su salida. La suma
sobre $i$, que aparecerá en el objetivo, reúne los errores cuadrados de
todos los clips.

El orden importa. Si primero sumáramos los errores y después eleváramos
el total al cuadrado, un error positivo podría cancelar uno negativo.
Esa sería una medida distinta de la que pide el enunciado.

Las salidas y los errores se calculan con los pesos y la constante. No
son nuevas decisiones que podamos escoger libremente. Si quisiéramos
representarlos con variables adicionales, necesitaríamos igualdades que
los vincularan con esa misma regla de salida.

## 3 · Minimizar la suma de errores cuadrados

El problema 7 pide aproximar las referencias. **No exige acertar
exactamente en todos los clips.** Por eso medimos las diferencias en el
objetivo, sin imponer que cada salida sea igual a su referencia.

El modelo general es

$$
\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}
$$

Los dominios completan este modelo. El enunciado no establece límites de
recursos ni pide pesos no negativos o puntajes dentro de un intervalo.
Añadir cualquiera de esas condiciones cambiaría el problema.

Aunque cada clip aporte un término distinto, los términos comparten las
decisiones. Cambiar un peso puede modificar los errores de varios clips a
la vez. Por eso no podemos elegir cada salida por separado.

## 4 · Añadir un límite para los pesos

El problema 8 conserva los datos, las decisiones y el objetivo. Añade un
dato $R>0$ y pide que la suma de cuadrados de los pesos no supere $R^2$:

$$\sum_{j\in J}w_j^2\le R^2.$$

Cada $w_j^2$ cuenta contra **el mismo límite**. El valor de $R$ está dado;
no podemos aumentarlo para hacer que una elección de pesos cumpla la
condición. Tampoco necesitamos nuevas variables.

Al traducir la condición, conservamos estas distinciones:

- **El límite se aplica a la suma**: Una restricción reúne todos los pesos.
- **La constante queda libre**: $b$ no entra en esa suma.
- **Los pesos pueden ser negativos**: Se mantiene su dominio real.
- **El máximo es obligatorio**: Aparece entre las restricciones.

Limitar cada peso por separado no bastaría. Varios pesos podrían respetar
sus límites individuales y, juntos, exceder el total permitido. En la
práctica, dos pesos iguales a 1 suman 2 al elevarlos al cuadrado, aunque
cada uno esté entre $-1$ y 1.

Tampoco basta con sumar los cuadrados de los pesos al objetivo. Eso
penalizaría los valores grandes, pero no impondría el máximo pedido y
cambiaría la medida que minimizamos.

## 5 · Escribir el modelo con el nuevo límite

Para usar la forma estándar convexa del curso, escribimos las
desigualdades con cero del lado derecho. Restamos $R^2$ en ambos lados de
la restricción. **El objetivo permanece igual:**

$$
\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&\sum_{j\in J}w_j^2-R^2\le0,\\
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}
$$

En el ejercicio hay dos pesos y $R=1$, por lo que la condición se convierte
en $w_1^2+w_2^2-1\le0$. La constante $b$ sigue libre.

## 6 · Comprobar por qué el modelo es convexo

La forma estándar convexa que usamos minimiza una función convexa.
Admite desigualdades $g(x)\le0$ con $g$ convexa e igualdades afines, si las
hay. Este modelo cumple esas condiciones.

**En el objetivo**, cada error antes de elevarlo al cuadrado es una
expresión afín en las decisiones. Los valores $h_{ij}$ y $t_i$ son datos:
solo multiplicamos decisiones por números conocidos, sumamos $b$ y
restamos la referencia. No hay productos entre decisiones.

El cuadrado de esa expresión afín es convexo. Al sumar los errores
cuadrados, conservamos la convexidad del objetivo.

**En la restricción**, la suma de cuadrados de los pesos menos el dato
$R^2$ también es una función convexa. Pedir que sea menor o igual que
cero define un conjunto permitido convexo. Los dominios reales de pesos
y constante son convexos, así que el problema es **continuo convexo**.

No es lineal: contiene cuadrados. La forma estándar lineal no obliga a
convertir todo problema en uno lineal, y cambiar signos no elimina esos
cuadrados. Aquí corresponde usar la forma convexa.

## Qué conservar al añadir clips o entradas

**Distingue lo que se calcula para cada clip de lo que se elige para todos.**
Más clips añaden términos al objetivo; más entradas añaden pesos
compartidos. Una condición nueva puede limitar esas decisiones sin crear
variables ni cambiar el objetivo.

Esta explicación depende de que las entradas $h_{ij}$ permanezcan fijas.
Si ajustáramos también las etapas anteriores de la red, esas entradas
dejarían de ser datos y la justificación de convexidad que acabamos de
usar ya no bastaría. Aquí solo ajustamos la combinación final.

[[opt-practica-red|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
