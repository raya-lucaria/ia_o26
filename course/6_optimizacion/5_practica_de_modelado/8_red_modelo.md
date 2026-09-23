---
id: opt-modelo-red
title: Una regla de salida con muchos ejemplos
nav_title: Red · Modelo general
summary: "Separar las entradas fijas de los pesos que ajustamos y escribir un modelo convexo completo."
status: ready
tags: [optimizacion, modelado, convexidad]
---

# Una regla de salida con muchos ejemplos

**Primero intenta los [[opt-practica-red|dos problemas de la salida neuronal]].**
La pregunta es: **¿qué pesos y qué constante producen una sola regla que
aproxime los puntajes de todos los clips?** Solo ajustamos esa salida; las
entradas ya están calculadas.

## 1 · Distinguir datos por ejemplo y decisiones compartidas

| Símbolo | Significado | ¿Se elige? |
|---|---|---|
| $I,J$ | Conjuntos finitos no vacíos de clips y entradas | No |
| $h_{ij}\in\mathbb R$ | Entrada $j$ ya calculada para el clip $i$ | No |
| $t_i\in\mathbb R$ | Puntaje de referencia del clip $i$ | No |
| $w_j\in\mathbb R$ | Peso de la entrada $j$ en todos los clips | Sí |
| $b\in\mathbb R$ | Constante que se suma en todos los clips | Sí |

Un peso lleva índice $j$, pero no $i$: **el mismo peso se usa en todos los
clips**. La constante $b$ también es única. Si diéramos pesos distintos a
cada clip, estaríamos ajustando reglas distintas, no la regla compartida del relato.

Pesos y constante pueden ser negativos, positivos o cero. El dominio real
traduce esa libertad; imponer no negatividad agregaría una condición que
el problema no pide. Todos los valores usan la escala numérica sin unidades
físicas establecida en el ejercicio.

## 2 · Construir la función objetivo desde el relato

Primero escribimos qué produce la regla para **un** clip $i$:

$$\text{salida del clip }i=\sum_{j\in J}h_{ij}w_j+b.$$

Después restamos su referencia y elevamos la diferencia al cuadrado:

$$\text{error cuadrado del clip }i=
\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2.$$

Por último, sumamos sobre $i\in I$. La suma interior recorre las entradas
de un clip; la exterior reúne los errores de todos los clips.
**No elevamos al cuadrado la suma de errores:** errores positivos y negativos
podrían cancelarse antes de elevarla. El relato pide un cuadrado por clip.

Las salidas y errores son expresiones calculadas con $w_j,b$, no nuevas
decisiones libres. Escribirlas directamente evita variables adicionales y
las igualdades que harían falta para vincularlas con los pesos.

## 3 · Modelo completo del ajuste básico

El problema 7 pide aproximar las referencias lo mejor posible, no acertar
exactamente en todas. Por eso no imponemos una igualdad entre salida y
referencia: medimos la diferencia en el objetivo.

$$
\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}
$$

No faltan restricciones de recursos: el relato básico no las establece.
Los dominios completan el modelo. Los términos del objetivo están relacionados
porque comparten decisiones: modificar un peso puede cambiar los errores de
varios clips a la vez. No podemos elegir cada salida independientemente.

## 4 · Añadir un límite conjunto a los pesos

El problema 8 conserva las decisiones y el objetivo. Añade el **dato** $R>0$
y exige que la suma de cuadrados de los pesos sea como máximo $R^2$:

$$\sum_{j\in J}w_j^2\le R^2.$$

$R$ no es algo que podamos aumentar para evitar la condición. No añadimos
variables. La restricción relaciona todos los pesos: lo que aporta cada
$w_j^2$ cuenta contra **un mismo límite**.

| Pregunta al traducir el relato | Consecuencia en el modelo |
|---|---|
| ¿Se limita cada peso o la suma? | Una restricción conjunta para todos los pesos |
| ¿Entra la constante? | No: $b$ queda fuera de esa suma |
| ¿Se permiten pesos negativos? | Sí: conservamos $w_j\in\mathbb R$ |
| ¿El límite es obligatorio o una preferencia? | Obligatorio: va entre las restricciones |

Limitar cada $w_j^2$ por separado no bastaría: varios pesos podrían cumplir
su límite individual y superar la suma permitida. Tampoco añadimos esa suma
al objetivo; eso cambiaría la medida que minimizamos y no impondría el máximo pedido.

## 5 · Modelo completo y forma estándar convexa

La convención convexa del curso minimiza una función convexa, con
restricciones convexas escritas como $g(x)\le0$ e igualdades afines, si las hay.
Aquí solo trasladamos $R^2$ al lado izquierdo; **el objetivo no cambia**.

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

Es un modelo **continuo convexo**. Cada error antes de elevarlo al cuadrado
es una expresión afín en las decisiones, porque $h_{ij},t_i$ son datos.
Su cuadrado es convexo y la suma conserva esa propiedad. La función de la
desigualdad también es convexa; el dominio real es convexo.

La presencia de cuadrados impide llamarlo lineal. La forma estándar lineal
no exige que transformemos todo problema en uno lineal: cambiar signos no
elimina esos cuadrados. Aquí corresponde la forma convexa.

## Qué razonamiento puedes reutilizar

**Distingue lo que se calcula por ejemplo de lo que se decide para todos.**
Más clips añaden términos al objetivo; más entradas añaden pesos compartidos.
Una condición nueva puede restringir las decisiones existentes sin crear
variables ni modificar el objetivo.

No estamos ajustando una red completa. Si las etapas que producen $h_{ij}$
también cambiaran, esas entradas dejarían de ser datos y esta justificación
de convexidad ya no bastaría.

[[opt-practica-red|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
