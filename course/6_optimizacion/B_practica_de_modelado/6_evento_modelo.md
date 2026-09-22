---
id: opt-modelo-evento
title: "Evento: de elegir actividades a decidir cantidades"
nav_title: "Evento · Modelo general"
summary: "Selección binaria y duración continua: parámetros, dependencias, enlaces y dos modelos completos en forma estándar."
status: ready
tags: [optimizacion, modelado, entera, mixta]
---

# Evento: de elegir actividades a decidir cantidades

**Primero intenta los [[opt-practica-evento|dos ejercicios del evento]].**
La pregunta inicial es **qué talleres ofrecer**. En la variante también
decidimos **cuánto dura cada uno**. Ese cambio explica por qué necesitamos
otra familia de variables y restricciones que las relacionen.

## 1 · Elegir talleres completos

| Dato conocido | Significado |
|---|---|
| $J$ | Conjunto finito no vacío de talleres |
| $B,T\ge0$ | Presupuesto en pesos y tiempo disponible en horas |
| $c_j,t_j\ge0$ | Precio en pesos y duración en horas del taller completo |
| $E\subseteq J\times J$ | Pares de talleres $(p,q)$ donde ofrecer $q$ requiere ofrecer $p$ |

La decisión es $y_j\in\{0,1\}$: $1$ si ofrecemos el taller $j$ y $0$ si
no. Su duración ya está dada; todavía no necesitamos decidirla.

**Objetivo.** Queremos horas, no número de talleres. Cada taller elegido
aporta $t_jy_j$ horas, así que maximizamos $\sum_{j\in J}t_jy_j$.

**Recursos.** Las mismas elecciones generan dos consumos distintos:

| Obligación | Restricción | Origen |
|---|---|---|
| Respetar el presupuesto | $\sum_{j\in J}c_jy_j\le B$ | Solo pagamos los talleres elegidos |
| Respetar el tiempo del salón | $\sum_{j\in J}t_jy_j\le T$ | Se imparten uno después de otro |

La suma de horas aparece como objetivo y como restricción. No sobra ninguna:
el límite establece cuánto está permitido; el objetivo prefiere más horas
entre las elecciones que cumplen todas las condiciones.

## 2 · Traducir «si ofrecemos uno, también el otro»

Para $(p,q)\in E$, $p$ es el requerido y $q$ el que lo necesita. Primero
identificamos qué combinación prohíbe el relato:

| Ofrecer el requerido: $y_p$ | Ofrecer el dependiente: $y_q$ | ¿Cumple la dependencia? |
|---:|---:|---|
| 0 | 0 | Sí |
| 1 | 0 | Sí |
| 1 | 1 | Sí |
| 0 | 1 | No |

La desigualdad $y_q\le y_p$ elimina exactamente la última fila. Por eso no
usamos igualdad: ofrecer $p$ sin $q$ sí está permitido. Tampoco necesitamos
otra variable: ya tenemos las dos decisiones que queremos relacionar.

Pasamos a la forma estándar con $y_q-y_p\le0$. Escribimos el dominio binario
como entero, no negativo y como máximo uno. El modelo completo es:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}t_jy_j\\
\text{sujeto a}\quad
&\sum_{j\in J}c_jy_j\le B,\\
&\sum_{j\in J}t_jy_j\le T,\\
&y_q-y_p\le0 &&\text{para cada }(p,q)\in E,\\
&y_j\le1 &&\text{para cada }j\in J,\\
&y_j\ge0,\quad y_j\in\mathbb Z &&\text{para cada }j\in J.
\end{aligned}
$$

Es **lineal entero**. Cada par de $E$ produce una restricción con la misma
regla; no tenemos que inventar una fórmula distinta para cada dependencia.

## 3 · Añadir la duración como decisión

En el problema 6, la duración deja de ser un dato fijo. Añadimos
$h_j\in\mathbb R_{\ge0}$: horas que impartimos del taller $j$. Conservamos
$y_j$ para indicar si lo ofrecemos y cobrar su preparación una sola vez.

Los nuevos datos por taller son:

| Dato | Significado |
|---|---|
| $f_j\ge0$ | Costo fijo de preparación, en pesos, si se ofrece |
| $k_j\ge0$ | Tarifa por hora impartida, en pesos/hora |
| $L_j,U_j$ | Duración mínima y máxima contratadas, en horas; $0<L_j\le U_j<\infty$ |

**Dos variables no deben permitir dos relatos incompatibles.** Si solo
escribiéramos sus dominios, sería posible elegir $y_j=0$ y $h_j>0$: impartir
horas de un taller que supuestamente no ofrecemos. Faltan los enlaces.

## 4 · Construir los enlaces por casos

El contrato pide estas posibilidades:

| Elección | Duración permitida |
|---|---|
| No ofrecer: $y_j=0$ | $h_j=0$ |
| Ofrecer: $y_j=1$ | $L_j\le h_j\le U_j$ |

El límite inferior debe valer cero al no ofrecer y $L_j$ al ofrecer:
lo representa $L_jy_j$. El superior debe valer cero o $U_j$:
lo representa $U_jy_j$. Así construimos las dos restricciones:

$$
\begin{aligned}
&h_j\ge L_jy_j,\\
&h_j\le U_jy_j.
\end{aligned}
$$

**Compruébalas juntas.** Con $y_j=0$, fuerzan $h_j=0$. Con $y_j=1$,
recuperan el intervalo contratado. Como $L_j>0$, abrir implica impartir
una duración positiva; cualquier duración positiva también exige abrir.

El límite superior impide horas sin apertura. El inferior impide abrir con
menos horas que el mínimo. Escribir solo $h_j\ge L_j$ obligaría a abrir todos
los talleres. Los límites vienen del contrato: no son números grandes arbitrarios.

## 5 · Actualizar el costo y el objetivo

El costo de cada taller se construye por separado de las horas que queremos maximizar:

$$\text{costo del taller }j=f_jy_j+k_jh_j.$$

Si no se ofrece, $y_j=h_j=0$ y el costo es cero. Si se ofrece, pagamos
$f_j$ una sola vez más $k_j$ por cada hora. Este cobro **sustituye** al precio
completo $c_j$; no sumamos ambos esquemas.

No multiplicamos $k_jh_j$ por $y_j$: los enlaces ya anulan las horas cuando
no se abre. Cada producto que usamos es un dato por una variable, por lo que
el modelo sigue siendo lineal.

**El objetivo conserva su significado, pero cambia su expresión:** antes
sumábamos duraciones fijas elegidas, $\sum_j t_jy_j$; ahora sumamos duraciones
decididas, $\sum_j h_j$. No usamos $\sum_j y_j$, que contaría talleres.

## 6 · Modelo completo con duración flexible

Conservamos presupuesto, tiempo y dependencias. Agregamos las duraciones y
sus dos enlaces, escritos con $\le$ para la forma estándar:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}h_j\\
\text{sujeto a}\quad
&\sum_{j\in J}(f_jy_j+k_jh_j)\le B,\\
&\sum_{j\in J}h_j\le T,\\
&y_q-y_p\le0 &&\text{para cada }(p,q)\in E,\\
&L_jy_j-h_j\le0 &&\text{para cada }j\in J,\\
&h_j-U_jy_j\le0 &&\text{para cada }j\in J,\\
&y_j\le1 &&\text{para cada }j\in J,\\
&h_j\in\mathbb R_{\ge0},\quad y_j\ge0 &&\text{para cada }j\in J,\\
&y_j\in\mathbb Z &&\text{para cada }j\in J.
\end{aligned}
$$

Es **lineal mixto**: elegimos conjuntamente aperturas enteras y duraciones
continuas. La dependencia conecta aperturas entre talleres; los enlaces
conectan cada apertura con su duración; presupuesto y tiempo reúnen a todos.

## Qué razonamiento puedes reutilizar

**Cuando añadas una decisión, pregunta qué debe impedir que contradiga a
las anteriores.** Escribe primero los casos permitidos y luego comprueba
que las desigualdades permiten exactamente esos casos.

Aquí «requiere» significa incluir otro taller, no impartirlo antes.
Sumamos tiempos porque hay un salón y cualquier orden está permitido.
Horarios, varios salones o instructores con disponibilidad parcial pedirían
otras condiciones.

[[opt-practica-evento|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
