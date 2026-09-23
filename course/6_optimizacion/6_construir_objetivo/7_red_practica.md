---
id: opt-practica-red
title: Ajustar puntajes de claridad con una red
nav_title: Red · Practicar
summary: "Ajustar una regla compartida para aproximar cuatro puntajes y añadir un límite para sus pesos."
status: ready
tags: [optimizacion, modelado, convexidad, practica]
---

# Ajustar puntajes de claridad con una red

Una red neuronal puede transformar un audio en varios números y usarlos
para producir un puntaje. Aquí **solo ajustaremos la última combinación
de esos números**: multiplicar cada uno por un peso y sumar una constante.
Las etapas anteriores ya están construidas y permanecen fijas.

No necesitas conocer redes neuronales para plantear estos problemas.
Los datos son didácticos; no hay azar ni cálculo de probabilidades.
Queremos escribir un modelo a partir de cuatro clips que ya conocemos.

## Problema 7 · Ajustar los puntajes de cuatro clips

::: exercise {#opt-b-red-ej-1 title="Ajustar los puntajes de cuatro clips"}
Una aplicación asigna un **puntaje de claridad** a clips de audio. Un número
mayor representa un audio más claro. Una etapa ya construida convierte
cada clip en dos características numéricas: **ambas están dadas y no se
modifican** durante el ajuste.

Tenemos cuatro clips que un equipo de revisión ya escuchó y calificó.
Queremos que la aplicación produzca puntajes cercanos a esas referencias.

| Clip | Entradas | Referencia |
|---|---|---:|
| 1 | (0, 0) | 0 |
| 2 | (1, 0) | 1 |
| 3 | (0, 1) | 1 |
| 4 | (1, 1) | 3 |

**Cómo se calcula el puntaje.** La salida multiplica la primera entrada
por un peso, la segunda por otro y suma una constante. Usamos **los mismos
dos pesos y la misma constante en los cuatro clips**.

Podemos elegir valores positivos, negativos o cero para esos tres ajustes.
Todos los números del ejercicio están en una escala sin unidades físicas.
No se pide limitar el puntaje producido a un intervalo.

**Cómo se evalúa el ajuste.** Para cada clip, restamos el puntaje de
referencia al producido y elevamos esa diferencia al cuadrado. Después
sumamos los cuatro resultados. Queremos que esa suma sea lo más pequeña
posible.

Plantea el modelo completo: identifica los datos de cada clip, las
decisiones compartidas, sus valores permitidos y el objetivo. No calcules
los mejores pesos.
:::

### Intenta escribir una regla para los cuatro clips

Escribe tu propuesta antes de abrir las pistas. Si no encuentras por dónde
empezar, usa la primera para ordenar la información.

::: hint {#opt-b-red-pista-1a of="opt-b-red-ej-1" title="Pista 1 · Datos de cada clip y ajustes compartidos"}

- **Entradas**: Dos números ya calculados para cada clip.
- **Referencia**: Un puntaje conocido para cada clip.
- **Ajustes**: Dos pesos y una constante, iguales para todos los clips.
- **Valores permitidos**: Los ajustes pueden ser positivos, negativos o cero.

La tabla del enunciado contiene los datos de los cuatro clips. Elegir los
ajustes no modifica esos datos.
:::

Si todavía no sabes cómo usar una sola regla, abre la segunda pista y
vuelve a tu hoja.

::: hint {#opt-b-red-pista-1b of="opt-b-red-ej-1" title="Pista 2 · Qué cambia entre clips"}
¿Qué cantidades cambian cuando pasas de un clip a otro? ¿Cuáles deben
seguir siendo las mismas para que exista una sola regla de salida?
:::

Antes de abrir la respuesta, revisa tu modelo. Después compara cómo
representaste los datos, los ajustes y el error.

::: answer {#opt-b-red-resp-1 of="opt-b-red-ej-1" title="Construir el error de una regla compartida"}
**Separamos datos y decisiones.** Llamemos $I$ al conjunto de clips y $J$
al conjunto de entradas de la salida. Ambos son finitos y no vacíos.
Para cada clip conocemos las entradas y el puntaje de referencia.

- $h_{ij}$: Entrada $j$ ya calculada para el clip $i$; es un dato real.
- $t_i$: Puntaje de referencia del clip $i$; es un dato real.
- $w_j$: Peso de la entrada $j$; es una decisión real.
- $b$: Constante que se suma a la salida; es una decisión real.

Elegimos una sola lista de pesos y una sola constante para todos los clips.
Por eso $w_j$ lleva el índice de la entrada, pero no el del clip. Tanto los
datos como las decisiones usan la escala sin unidades físicas del enunciado.

**Calculamos la salida de un clip.** Multiplicamos cada entrada por su peso,
sumamos los productos y añadimos $b$:

$$\text{puntaje producido para el clip }i=\sum_{j\in J}h_{ij}w_j+b.$$

Cada $h_{ij}$ es un dato fijo: ninguna decisión multiplica otra decisión.
La expresión es **afín** en los ajustes; es una suma de múltiplos conocidos
de las decisiones. Aquí $b$ también se elige, aunque se sume de la misma
manera en todos los clips.

**Calculamos el error de ese clip.** Restamos el puntaje de referencia al
producido. Elevamos esa diferencia al cuadrado, como pide el enunciado:

$$\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2.$$

Repetimos el cálculo para cada clip y sumamos los resultados. En todos los
términos usamos los mismos pesos y la misma constante. No exigimos que cada
error sea cero: buscamos aproximar las referencias lo mejor posible según
esta suma.

**El modelo general** queda así:

$$\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}$$

**Ahora sustituimos los datos.** Tenemos cuatro clips y dos entradas:
$I=\{1,2,3,4\}$ y $J=\{1,2\}$. La misma regla produce estas salidas:

| Clip | Salida | Referencia |
|---|---|---:|
| 1 | $b$ | 0 |
| 2 | $w_1+b$ | 1 |
| 3 | $w_2+b$ | 1 |
| 4 | $w_1+w_2+b$ | 3 |

Restamos cada referencia, elevamos cada diferencia al cuadrado y sumamos:

$$\begin{aligned}
\min_{w_1,w_2,b}\quad
&b^2+(w_1+b-1)^2\\
&\quad +(w_2+b-1)^2+(w_1+w_2+b-3)^2\\
\text{sujeto a}\quad
&w_1,w_2,b\in\mathbb R.
\end{aligned}$$

**Comprobamos el primer término.** El primer clip tiene ambas entradas en
cero, de modo que su salida es $b$. Su referencia es 0 y el error cuadrado
es $b^2$. Cada clip aporta un término, pero ninguno recibe pesos propios.

El dominio real permite los valores negativos que admite el enunciado.
No añadimos condiciones de no negatividad ni límites al puntaje.

Este es un problema **continuo convexo**: el error de cada clip es afín en
las decisiones y su cuadrado es convexo. La suma conserva esa propiedad.
No es un problema lineal, porque el objetivo contiene cuadrados.
:::

## Problema 8 · Ajustar la red con un límite para los pesos

::: exercise {#opt-b-red-ej-2 title="Ajustar la red con un límite para los pesos"}
Volvemos a los cuatro clips del problema 7. Todavía tenemos que elegir los
pesos y la constante; no hemos fijado sus valores.

**Conservamos:**

- Las entradas (0, 0), (1, 0), (0, 1) y (1, 1), que permanecen fijas.
- Los puntajes de referencia 0, 1, 1 y 3, respectivamente.
- La misma regla de salida para todos los clips.
- El objetivo de minimizar la suma de errores cuadrados.

**Añadimos una condición.** Para evitar pesos demasiado grandes, el equipo
establece que **la suma de los cuadrados de los dos pesos no puede superar
1**. Los pesos todavía pueden ser negativos.

La constante que se suma a la salida, también llamada **sesgo**, queda
fuera de ese límite. Sigue siendo un número real libre.

Escribe el modelo completo con la nueva condición como restricción.
Para la versión general, usa el dato $R>0$: el límite de la suma será
$R^2$. En este ejercicio, $R=1$. No busques los mejores parámetros.
:::

### Intenta escribir la condición nueva

Conserva tu objetivo del problema anterior y escribe la condición que
ahora deben cumplir los pesos. Usa las pistas si necesitas revisar esa
traducción.

::: hint {#opt-b-red-pista-2a of="opt-b-red-ej-2" title="Pista 1 · Qué cambia con el límite"}

- **Entradas y referencias**: Se conservan los datos de los cuatro clips.
- **Medida que se minimiza**: Sigue siendo la suma de errores cuadrados.
- **Pesos**: Admiten valores negativos; sus cuadrados suman como máximo 1.
- **Constante de salida**: Sigue libre y queda fuera del nuevo límite.

El dato $R$ fija el límite. No es otro ajuste que podamos elegir.
:::

Si todavía no sabes qué debe reunir la restricción, abre la segunda pista.

::: hint {#opt-b-red-pista-2b of="opt-b-red-ej-2" title="Pista 2 · Una suma para todos los pesos"}
¿El enunciado exige limitar cada peso por separado o una cantidad que
depende de todos ellos juntos?
:::

Antes de abrir la respuesta, comprueba qué hiciste con la constante.
Después compara tu restricción con la formulación propuesta.

::: answer {#opt-b-red-resp-2 of="opt-b-red-ej-2" title="Añadir el límite sin cambiar el objetivo"}
**Se mantienen los datos y las decisiones.** Las entradas $h_{ij}$ y las
referencias $t_i$ siguen fijas. Elegimos los mismos tipos de ajustes: los
pesos compartidos $w_j$ y la constante $b$. El nuevo dato es $R>0$.

**Construimos la condición sobre los pesos.** Cada peso aporta su cuadrado,
$w_j^2$. Sumamos esas aportaciones y comparamos el total con $R^2$:

$$\sum_{j\in J}w_j^2\le R^2.$$

El límite se aplica a todos los pesos juntos. La constante $b$ no aparece
en esta suma porque el enunciado la deja libre. Para escribir la condición
con cero del lado derecho, restamos $R^2$ en ambos lados.

**El modelo general** conserva el objetivo y añade la restricción:

$$\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&\sum_{j\in J}w_j^2-R^2\le0,\\
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}$$

**Ahora sustituimos los datos.** Usamos las cuatro referencias y las dos
entradas por clip del problema anterior. Con $R=1$, obtenemos

$$\begin{aligned}
\min_{w_1,w_2,b}\quad
&b^2+(w_1+b-1)^2\\
&\quad +(w_2+b-1)^2+(w_1+w_2+b-3)^2\\
\text{sujeto a}\quad
&w_1^2+w_2^2-1\le0,\\
&w_1,w_2,b\in\mathbb R.
\end{aligned}$$

**Comprobamos qué impone el límite.** Si ambos pesos valieran 1, sus
cuadrados sumarían 2 y violarían la condición. Por eso no basta con pedir
que cada peso esté entre $-1$ y 1. Un peso negativo sí está permitido,
siempre que se respete la suma de cuadrados.

El objetivo sigue siendo convexo. En la nueva restricción, la suma de
cuadrados menos el dato $R^2$ también es una función convexa. Al exigir
que sea menor o igual que cero, obtenemos un conjunto permitido convexo.

**El límite es obligatorio.** Por eso aparece entre las restricciones.
Sumar los cuadrados de los pesos al objetivo cambiaría lo que minimizamos
y no obligaría a respetar el máximo pedido.
:::

Si quieres ampliar lo trabajado, tienes una consulta opcional sobre [[opt-modelo-red|la forma general de esta salida]].

Si necesitas ayuda para construir el modelo, vuelve a [[opt-objetivo-clasificacion-practica|el ejemplo guiado de clasificación]].

[[opt-construir-objetivo|Volver al banco de práctica]].
