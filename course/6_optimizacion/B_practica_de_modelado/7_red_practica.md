---
id: opt-practica-red
title: Ajustar la salida de una red neuronal
nav_title: Red · Practicar
summary: "Dos ejercicios de optimización continua con una regla de salida y datos fijos. Plantear el error y una condición sobre los pesos."
status: ready
tags: [optimizacion, modelado, convexidad, practica]
---

# Ajustar la salida de una red neuronal

**Solo ajustaremos la última salida.** No necesitas conocer redes neuronales.
Piensa en una regla que recibe números, multiplica cada uno por un peso y
suma una constante. Los pesos y la constante son los ajustes que elegimos.
Las etapas anteriores de la red permanecen fijas.

Los datos son didácticos. Aquí no hay azar ni cálculo de probabilidades:
queremos escribir un problema a partir de ejemplos que ya tenemos.

## Problema 7 · Un puntaje de claridad para clips de audio

::: exercise {#opt-b-red-ej-1 title="Ajustar una regla a ejemplos conocidos"}
Una aplicación asigna un **puntaje de claridad** a clips de audio: un número
mayor representa un audio más claro. Una etapa ya construida convierte cada
clip en dos características numéricas. **Esos dos números están dados y no
se modifican** durante este ajuste.

La salida multiplica el primer número por un peso, el segundo por otro y
suma una constante común a todos los clips. Tanto los pesos como la constante
pueden ser positivos, negativos o cero. Todos los números de este ejercicio
están en una escala sin unidades físicas; no se exige limitar el puntaje a
un intervalo.

Tenemos cuatro clips de referencia. Sus pares de entrada son **(0, 0),
(1, 0), (0, 1) y (1, 1)**. El equipo de revisión ya les asignó los puntajes
de claridad **0, 1, 1 y 3**, respectivamente. Esos son los valores de
referencia que queremos aproximar.

Para evaluar un ajuste, en cada clip restamos el puntaje de referencia al
puntaje producido, elevamos esa diferencia al cuadrado y sumamos los cuatro
resultados. Queremos que esa suma sea lo más pequeña posible.

**Plantea el modelo completo.** Define qué datos corresponden a cada clip y
qué decisiones se comparten entre todos. No calcules los mejores pesos.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SI TODAVÍA NO HAS HECHO UN INTENTO.**

::: hint {#opt-b-red-pista-1a of="opt-b-red-ej-1" title="PISTA 1 · Solo si te atoraste"}
Esta tabla solo ordena los datos del relato:

| Clip | Primera entrada fija | Segunda entrada fija | Puntaje de referencia |
|---|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 1 | 3 |

El mismo ajuste se utiliza para los cuatro clips. El relato permite valores
negativos en sus pesos y en su constante.
:::

**ABRE LA PISTA 2 SOLO SI SIGUES ATORADO; DESPUÉS VUELVE A TU HOJA.**

::: hint {#opt-b-red-pista-1b of="opt-b-red-ej-1" title="PISTA 2 · Solo si te atoraste"}
¿Qué cantidades cambian cuando pasas de un clip a otro y cuáles deben seguir
siendo las mismas para que exista una sola regla de salida?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-red-resp-1 of="opt-b-red-ej-1"}
**Datos y decisiones.** Llamamos $I$ al conjunto de clips y $J$ al conjunto
de entradas de la salida. Ambos son finitos y no vacíos.

| Símbolo | Qué representa | Tipo |
|---|---|---|
| $h_{ij}$ | Entrada $j$ ya calculada para el clip $i$ | Dato real |
| $t_i$ | Puntaje de referencia del clip $i$ | Dato real |
| $w_j$ | Peso que multiplica la entrada $j$ en todos los clips | Decisión real |
| $b$ | Constante que se suma en todos los clips | Decisión real |

**Construir la salida.** Para el clip $i$, la regla produce
$\sum_{j\in J}h_{ij}w_j+b$. Los $h_{ij}$ son datos, así que esta expresión
es afín en las decisiones: suma productos de datos por variables y el
término $b$, una variable compartida por todos los clips.

**Construir el error.** Restamos $t_i$, elevamos al cuadrado y sumamos sobre
los clips. La misma lista de pesos y el mismo $b$ aparecen en cada término.
No imponemos que cada error sea cero: el relato pide aproximar.

**Modelo general completo:**

$$\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}$$

**Con los datos del ejercicio**, $I=\{1,2,3,4\}$ y $J=\{1,2\}$:

$$\begin{aligned}
\min_{w_1,w_2,b}\quad
&b^2+(w_1+b-1)^2\\
&\quad +(w_2+b-1)^2+(w_1+w_2+b-3)^2\\
\text{sujeto a}\quad
&w_1,w_2,b\in\mathbb R.
\end{aligned}$$

**Comprobación:** el primer clip tiene ambas entradas en cero; por eso su
salida es $b$ y su error cuadrado es $b^2$. Cada clip aporta un término, pero
no recibe pesos propios. No agregamos no negatividad ni límites de salida
que el enunciado no pide.

Es un problema continuo convexo: cada término es el cuadrado de una expresión
afín. No es un problema lineal, porque el objetivo contiene cuadrados.
:::

## Problema 8 · Limitar los pesos de la salida

::: exercise {#opt-b-red-ej-2 title="Conservar el ajuste y agregar una condición"}
Parte del **problema 7 · Un puntaje de claridad para clips de audio**. Conserva las
entradas (0, 0), (1, 0), (0, 1), (1, 1), los puntajes de referencia 0, 1,
1, 3 y el objetivo de minimizar la suma de errores cuadrados.

Ahora el equipo quiere evitar pesos demasiado grandes. Establece esta regla:
**la suma de los cuadrados de los dos pesos no puede superar 1**. La constante
que se suma a la salida no entra en ese límite y sigue siendo libre. Los
pesos todavía pueden ser negativos.

Escribe el modelo completo. Para la versión general, llama $R>0$ al dato
que fija el límite $R^2$; en este ejercicio $R=1$. Conserva el objetivo y
agrega la condición pedida como restricción.
:::

### Primero escribe tu restricción

**NO ABRAS LA PISTA 1 SIN INTENTAR TRADUCIR LA NUEVA CONDICIÓN.**

::: hint {#opt-b-red-pista-2a of="opt-b-red-ej-2" title="PISTA 1 · Solo si te atoraste"}
| Parte del relato | Condición |
|---|---|
| Entradas de los cuatro clips | (0, 0), (1, 0), (0, 1), (1, 1), fijas |
| Puntajes de referencia | 0, 1, 1, 3 |
| Medida que se minimiza | Suma de errores cuadrados |
| Pesos | Pueden ser negativos; sus cuadrados suman como máximo 1 |
| Constante de salida | Libre; queda fuera del nuevo límite |
:::

**ABRE LA PISTA 2 SOLO SI LA CONDICIÓN TODAVÍA NO TE QUEDA CLARA.**

::: hint {#opt-b-red-pista-2b of="opt-b-red-ej-2" title="PISTA 2 · Solo si te atoraste"}
¿El relato exige limitar cada peso por separado o una cantidad que depende
de todos ellos juntos?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-red-resp-2 of="opt-b-red-ej-2"}
**Conservamos** los datos $h_{ij},t_i$ y las decisiones compartidas $w_j,b$
del problema 7. El nuevo parámetro es $R>0$. La condición suma $w_j^2$ para
todos los pesos, y deja fuera a $b$.

**Modelo general completo:**

$$\begin{aligned}
\min_{w,b}\quad
&\sum_{i\in I}\left(\sum_{j\in J}h_{ij}w_j+b-t_i\right)^2\\
\text{sujeto a}\quad
&\sum_{j\in J}w_j^2-R^2\le0,\\
&w_j\in\mathbb R &&(j\in J),\\
&b\in\mathbb R.
\end{aligned}$$

**Modelo con los datos del ejercicio:**

$$\begin{aligned}
\min_{w_1,w_2,b}\quad
&b^2+(w_1+b-1)^2\\
&\quad +(w_2+b-1)^2+(w_1+w_2+b-3)^2\\
\text{sujeto a}\quad
&w_1^2+w_2^2-1\le0,\\
&w_1,w_2,b\in\mathbb R.
\end{aligned}$$

**Comprobación:** dos pesos de valor 1 violan la regla porque sus cuadrados
suman 2. Limitar cada uno a un intervalo entre $-1$ y 1 no bastaría. Un peso
negativo es válido si se respeta la suma de cuadrados.

El objetivo sigue siendo convexo. La nueva restricción tiene una función
convexa del lado izquierdo y está escrita con $\le0$: su región es convexa.
El límite es obligatorio: debe aparecer entre las restricciones. Sumar los
cuadrados de los pesos al objetivo no impondría ese máximo y cambiaría el
criterio que queremos minimizar.
:::

Después de comparar tus dos planteamientos, pasa a [[opt-modelo-red|la forma general de esta salida]].
