---
id: opt-modelo-evento
title: "Cómo modelar la selección y duración de talleres"
nav_title: "Evento · Modelo general"
summary: "Selección binaria y duración continua: parámetros, dependencias, enlaces y dos modelos completos en forma estándar."
status: ready
tags: [optimizacion, modelado, entera, mixta]
---

# Cómo modelar la selección y duración de talleres

**Primero intenta los [[opt-practica-evento|dos ejercicios del evento]].**
Primero decidimos **qué talleres ofrecer**. En la segunda variante también
elegimos **cuánto dura cada uno**. Veremos cómo escribir ambas decisiones
para cualquier número de talleres y cómo impedir que se contradigan.

## 1 · Contar las horas de los talleres elegidos

Todos los talleres se imparten uno después de otro en un solo salón. Podemos
elegir cualquiera de ellos, siempre que respetemos los recursos disponibles
y los requisitos entre talleres.

Llamamos $J$ al conjunto finito no vacío de talleres. Estos son los datos
necesarios para la primera variante:

- $B\ge0$: Presupuesto disponible, en pesos.
- $T\ge0$: Tiempo disponible en el salón, en horas.
- $c_j\ge0$: Precio del taller completo, en pesos.
- $t_j\ge0$: Duración del taller completo, en horas.

La decisión es $y_j\in\{0,1\}$: $1$ si ofrecemos el taller $j$ y $0$ si
no. Su duración ya está dada; todavía no necesitamos decidirla.

**El objetivo cuenta horas de talleres.** Un taller elegido aporta $t_jy_j$
horas: su duración completa si $y_j=1$, y cero si $y_j=0$. Sumamos esas
aportaciones y buscamos el mayor total:

$$\max\quad\sum_{j\in J}t_jy_j.$$

Contar talleres sería otro objetivo: uno largo y uno corto contarían lo mismo.

**El presupuesto limita el gasto.** Solo pagamos los talleres elegidos, de
modo que cada uno cuesta $c_jy_j$ pesos. El total debe caber en el presupuesto:

$$\sum_{j\in J}c_jy_j\le B.$$

**El salón limita el tiempo.** Como los talleres se imparten uno después de
otro, sus duraciones se suman. No pueden superar las horas disponibles:

$$\sum_{j\in J}t_jy_j\le T.$$

La suma de horas aparece como objetivo y como restricción. No sobra ninguna:
el límite establece cuánto está permitido; el objetivo prefiere más horas
entre las elecciones que cumplen todas las condiciones.

## 2 · Traducir «si ofrecemos uno, también el otro»

Puede haber varios requisitos como el de video y fotografía. Los reunimos
en un conjunto de pares $E\subseteq J\times J$: escribir $(p,q)\in E$
significa que ofrecer $q$ exige ofrecer $p$.

Para cada par, revisamos las cuatro combinaciones posibles. En la tabla,
$y_p$ indica si ofrecemos el requerido y $y_q$ si ofrecemos el que lo necesita:

| $y_p$ | $y_q$ | ¿Está permitido? |
|---:|---:|---|
| 0 | 0 | Sí |
| 1 | 0 | Sí |
| 1 | 1 | Sí |
| 0 | 1 | No |

La desigualdad que elimina exactamente la última fila es:

$$y_q\le y_p.$$

No usamos igualdad: ofrecer $p$ sin $q$ sí está permitido. Tampoco necesitamos
otra variable, pues ya tenemos las dos decisiones que queremos relacionar.
Si ofrecemos el taller que tiene el requisito, debemos incluir también el
requerido; no se exige impartirlo antes.

En la forma estándar del curso, escribimos esa condición como $y_q-y_p\le0$.
Para expresar el dominio binario, exigimos que cada $y_j$ sea entero, no
negativo y como máximo uno: los únicos valores que quedan son 0 y 1.

El modelo completo es:

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

Es **lineal entero**: todas las variables son enteras y las expresiones son
sumas de variables multiplicadas por datos conocidos. Cada par de $E$ produce
una restricción con la misma regla; no necesitamos una fórmula distinta para
cada requisito.

## 3 · Decidir también cuánto dura cada taller

En el problema 6, la duración deja de ser un dato fijo. Añadimos $h_j$, las
horas que impartimos del taller $j$. Su dominio es $h_j\in\mathbb R_{\ge0}$,
porque se permiten fracciones de hora.

Conservamos $y_j$ para indicar si ofrecemos el taller. Esa decisión también
determina si debemos pagar su preparación, que se cobra una sola vez.

Los nuevos datos por taller son:

- $f_j\ge0$: Costo fijo de preparación, en pesos, si se ofrece.
- $k_j\ge0$: Tarifa por hora impartida, en pesos/hora.
- $L_j$: Duración mínima contratada, en horas.
- $U_j$: Duración máxima contratada, en horas.

Los límites cumplen $0<L_j\le U_j<\infty$. El mínimo debe ser positivo;
el máximo es finito y no puede ser menor que el mínimo.

**Las dos decisiones deben ser coherentes.** Si solo escribimos sus dominios,
podríamos elegir $y_j=0$ y $h_j>0$: asignar horas a un taller que no ofrecemos.
Necesitamos restricciones que relacionen las dos variables. Las llamaremos
restricciones de enlace.

## 4 · Exigir cero horas a los talleres que no se ofrecen

El contrato pide estas posibilidades. El valor $y_j=0$ significa que el
taller no se ofrece; $y_j=1$ significa que sí se ofrece.

| $y_j$ | Horas permitidas |
|---|---|
| $0$ | $h_j=0$ |
| $1$ | $L_j\le h_j\le U_j$ |

Para construir el límite inferior, buscamos una expresión que valga cero
cuando $y_j=0$ y $L_j$ cuando $y_j=1$. El producto $L_jy_j$ hace eso.
Para el superior usamos $U_jy_j$, que cambia de cero a $U_j$.

Así obtenemos las dos restricciones:

$$
\begin{aligned}
&h_j\ge L_jy_j,\\
&h_j\le U_jy_j.
\end{aligned}
$$

**Comprueba los dos casos.** Si no ofrecemos el taller, $y_j=0$: la cota
superior exige $h_j\le0$ y el dominio impide horas negativas. Por tanto,
necesariamente $h_j=0$.

Si lo ofrecemos, $y_j=1$: ambas desigualdades recuperan el intervalo
contratado, desde $L_j$ hasta $U_j$. Como **$L_j>0$**, no podemos seleccionar
un taller y asignarle cero horas.

La cota superior impide asignar horas a un taller no seleccionado. La inferior
impide ofrecerlo durante menos del mínimo contratado. Juntas aseguran que
ofrecer un taller implica impartir horas y que impartir horas exige ofrecerlo.

Escribir solo $h_j\ge L_j$ obligaría a impartir todos los talleres, incluso
los que queríamos dejar fuera. Los límites vienen del contrato; no son
números grandes elegidos arbitrariamente.

## 5 · Sumar la preparación y las horas impartidas

La preparación cuesta $f_j$ pesos, **una sola vez y solo si ofrecemos el
taller**. Por eso aporta $f_jy_j$ al gasto. Impartir $h_j$ horas a una tarifa
de $k_j$ pesos por hora aporta $k_jh_j$ pesos.

Sumamos esos dos cobros:

$$\text{costo del taller }j=f_jy_j+k_jh_j.$$

Si no se ofrece, $y_j=h_j=0$ y el costo es cero. Si se ofrece, pagamos
la preparación más las horas impartidas. Este cobro **sustituye** al precio
completo $c_j$; no sumamos los dos esquemas de pago.

No hace falta multiplicar $k_jh_j$ por $y_j$: las restricciones anteriores
ya exigen cero horas cuando no ofrecemos el taller. Cada producto que usamos
es un dato por una variable, por lo que el modelo sigue siendo lineal.

**Seguimos buscando el mayor total de horas.** Antes seleccionábamos
duraciones ya fijadas y sumábamos $\sum_j t_jy_j$. Ahora elegimos esas
duraciones, de modo que el objetivo es:

$$\max\quad\sum_j h_j.$$

La suma $\sum_j y_j$ contaría talleres; no representa las horas que pide el relato.

## 6 · Modelo completo con duración flexible

Conservamos las condiciones de presupuesto, tiempo y requisitos entre
talleres. Añadimos las duraciones y las dos restricciones que las relacionan
con la selección.

Para escribir estas últimas con $\le$, pasamos los términos al mismo lado:
$h_j\ge L_jy_j$ se convierte en $L_jy_j-h_j\le0$, y
$h_j\le U_jy_j$ en $h_j-U_jy_j\le0$. El modelo completo queda:

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

Es **lineal mixto**: combina las variables enteras de selección con las
duraciones, que pueden tomar valores reales. Cada grupo de restricciones
tiene una función:

- Los requisitos entre talleres relacionan cuáles se ofrecen.
- Los enlaces relacionan cada taller con su duración.
- El presupuesto y el tiempo limitan los totales del programa.

## Qué razonamiento puedes reutilizar

**Cuando añadas una decisión, pregunta qué debe impedir que contradiga a
las anteriores.** Escribe primero los casos permitidos y luego comprueba
que las desigualdades permiten exactamente esos casos.

Aquí «requiere» significa incluir otro taller, no impartirlo antes.
Sumamos tiempos porque hay un salón y cualquier orden está permitido.
Horarios, varios salones o instructores con disponibilidad parcial pedirían
otras condiciones.

[[opt-practica-evento|Volver a los ejercicios]] · [[opt-practica-modelado|Volver a la guía]].
