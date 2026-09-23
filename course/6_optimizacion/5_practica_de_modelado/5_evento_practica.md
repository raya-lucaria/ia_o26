---
id: opt-practica-evento
title: "Evento: elegir talleres y su duración"
nav_title: "Evento · Práctica"
summary: "Dos ejercicios para decidir qué talleres ofrecer y después cuánto dura cada uno, con presupuesto y condiciones de apertura."
status: ready
tags: [optimizacion, modelado, entera]
---

# Evento: elegir talleres y su duración

**Tu tarea es escribir el modelo completo, no encontrar la mejor programación.**
El contexto es una jornada universitaria de creación de contenido. Los números
son didácticos; no son cotizaciones de proveedores reales.

## Problema 5 · Elegir talleres completos

::: exercise {#opt-b-evento-elegir title="Una tarde de fotografía, podcast y video"}
Una asociación estudiantil dispone de un salón durante cinco horas efectivas
y de 3000 pesos para ofrecer talleres. Puede contratar fotografía por 1200
pesos durante dos horas, podcast por 2000 pesos durante tres horas y video por
1500 pesos durante dos horas. Cada precio cubre todo el taller.

Cada taller se ofrece una vez completo o no se ofrece. Se imparten uno después
de otro; los instructores están disponibles durante toda la tarde. Los
cambios de equipo ocurren fuera de las cinco horas efectivas.

La asociación exige que, si ofrece video, también ofrezca fotografía: quiere
que ambos temas formen parte del programa. Fotografía sí puede ofrecerse sin
video. No hay otras condiciones de orden o selección.

Quiere ofrecer **el mayor número total de horas de talleres**, sin exceder el
presupuesto ni el tiempo del salón. Escribe el modelo completo.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 A MENOS QUE TE HAYAS ATORADO AL ORGANIZAR EL RELATO.**

::: hint {#opt-b-evento-elegir-pista-1 of="opt-b-evento-elegir" title="PISTA 1 · Solo si te atoraste"}
| Taller | Precio completo | Duración completa |
|---|---:|---:|
| Fotografía | 1200 pesos | 2 horas |
| Podcast | 2000 pesos | 3 horas |
| Video | 1500 pesos | 2 horas |

Disponibles: 3000 pesos y 5 horas. Cada taller se ofrece completo o no se
ofrece. Video requiere que fotografía esté en el programa.
:::

**NO ABRAS LA PISTA 2 SI TODAVÍA PUEDES AVANZAR CON TU INTENTO.**

::: hint {#opt-b-evento-elegir-pista-2 of="opt-b-evento-elegir" title="PISTA 2 · Solo si te atoraste"}
¿Cuál combinación de decisiones prohíbe exactamente la frase «si ofrece
video, también ofrece fotografía»?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-evento-elegir-respuesta of="opt-b-evento-elegir" title="Respuesta · Decisiones de sí o no"}
**1. Separar datos y decisiones.** Sea $J$ el conjunto de talleres. Para cada
$j$, conocemos su costo completo $c_j$ y duración $t_j$. El presupuesto $B$ y
el tiempo $T$ también son datos. Decidimos $y_j=1$ si ofrecemos el taller y
$y_j=0$ si no: $y_j\in\{0,1\}$.

**2. Contar únicamente lo que elegimos.** El taller aporta $t_jy_j$ horas y
cuesta $c_jy_j$ pesos: ambos términos valen cero si no se ofrece. Sumamos por
separado horas y pesos; no son unidades intercambiables.

**3. Traducir la dependencia.** Llamemos $p$ al taller requerido y $q$ al que
lo necesita. La condición $y_q\le y_p$ excluye solamente el caso
$y_q=1,y_p=0$. Permite ofrecer ambos, solo el requerido o ninguno.

El modelo general completo es:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}t_jy_j\\
\text{sujeto a}\quad
&\sum_{j\in J}c_jy_j\le B,\\
&\sum_{j\in J}t_jy_j\le T,\\
&y_q\le y_p,\\
&y_j\in\{0,1\} &&\text{para cada }j\in J.
\end{aligned}
$$

**4. Sustituir los datos.** Numeramos fotografía, podcast y video como
$1,2,3$. Aquí $p=1$ y $q=3$:

$$
\begin{aligned}
\max\quad &2y_1+3y_2+2y_3\\
\text{sujeto a}\quad
&1200y_1+2000y_2+1500y_3\le3000,\\
&2y_1+3y_2+2y_3\le5,\\
&y_3\le y_1,\\
&y_1,y_2,y_3\in\{0,1\}.
\end{aligned}
$$

**Comprobación:** ofrecer fotografía sin video está permitido por la
dependencia. Escribir $y_3=y_1$ lo prohibiría y cambiaría el relato.
:::

## Problema 6 · Elegir también las duraciones

::: exercise {#opt-b-evento-duracion title="Talleres con duración flexible"}
Modificamos **Elegir talleres completos**: ahora los instructores permiten
ajustar la duración, incluyendo fracciones de hora, y cobran una preparación
fija más una tarifa por hora impartida.

Fotografía cuesta 600 pesos de preparación más 300 por hora; si se ofrece,
dura entre una y dos horas. Podcast cuesta 800 de preparación más 400 por
hora; dura entre una y tres horas. Video cuesta 700 de preparación más 400
por hora; dura entre una y dos horas. Esos mínimos y máximos vienen de los
acuerdos con los instructores.

Si un taller no se ofrece, dura cero horas y no se paga nada por él. Cada uno
puede ofrecerse una sola vez. Se mantienen los 3000 pesos, las cinco horas
efectivas en un salón, la disponibilidad de los instructores y la condición:
si se ofrece video, también se ofrece fotografía. Los cambios de equipo no
consumen esas cinco horas y no hay otras condiciones de orden.

Escribe el modelo completo para **maximizar las horas totales impartidas**.
Los nuevos cobros sustituyen los precios completos del ejercicio anterior.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 A MENOS QUE TE HAYAS ATORADO AL ORGANIZAR EL RELATO.**

::: hint {#opt-b-evento-duracion-pista-1 of="opt-b-evento-duracion" title="PISTA 1 · Solo si te atoraste"}
| Taller | Preparación si se ofrece | Por hora impartida | Duración si se ofrece |
|---|---:|---:|---:|
| Fotografía | 600 pesos | 300 pesos/hora | De 1 a 2 horas |
| Podcast | 800 pesos | 400 pesos/hora | De 1 a 3 horas |
| Video | 700 pesos | 400 pesos/hora | De 1 a 2 horas |

Si no se ofrece: cero horas y cero pago. Disponibles: 3000 pesos y 5 horas.
Video requiere fotografía. Se admiten fracciones de hora.
:::

**NO ABRAS LA PISTA 2 SI TODAVÍA PUEDES AVANZAR CON TU INTENTO.**

::: hint {#opt-b-evento-duracion-pista-2 of="opt-b-evento-duracion" title="PISTA 2 · Solo si te atoraste"}
¿Tu descripción permite tanto cancelar un taller como ofrecerlo durante una
hora, pero impide ofrecerlo durante media hora?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-b-evento-duracion-respuesta of="opt-b-evento-duracion" title="Respuesta · Apertura y cantidad continua"}
**1. Añadir la decisión que cambió.** Conservamos $y_j$, que indica si
ofrecemos el taller. Añadimos $h_j\ge0$, su duración en horas; es real porque
se permiten fracciones. Son decisiones distintas: abrir y cuánto impartir.

Los datos por taller son costo fijo $f_j$, tarifa horaria $k_j$ y duraciones
mínima $L_j$ y máxima $U_j$, con $0<L_j\le U_j<\infty$.

**2. Construir los límites por casos.**

| Decisión | Menor duración permitida | Mayor duración permitida |
|---|---:|---:|
| No ofrecer: $y_j=0$ | $0$ | $0$ |
| Ofrecer: $y_j=1$ | $L_j$ | $U_j$ |

El mínimo pasa de $0$ a $L_j$ según la decisión: se escribe $L_jy_j$.
El máximo pasa de $0$ a $U_j$: se escribe $U_jy_j$. Por eso exigimos
$h_j\ge L_jy_j$ y $h_j\le U_jy_j$. Los límites vienen del contrato, no de
haber resuelto otro problema.

**3. Contar el costo.** La preparación cuesta $f_jy_j$ una sola vez; impartir
$h_j$ horas cuesta $k_jh_j$. No multiplicamos este último término por $y_j$:
los enlaces ya obligan a que un taller cancelado tenga duración cero.

Con $J,B,T,p,q$ definidos como antes, el modelo general completo es:

$$
\begin{aligned}
\max\quad &\sum_{j\in J}h_j\\
\text{sujeto a}\quad
&\sum_{j\in J}(f_jy_j+k_jh_j)\le B,\\
&\sum_{j\in J}h_j\le T,\\
&y_q\le y_p,\\
&h_j\ge L_jy_j &&\text{para cada }j\in J,\\
&h_j\le U_jy_j &&\text{para cada }j\in J,\\
&h_j\in\mathbb R_{\ge0},\quad y_j\in\{0,1\}
&&\text{para cada }j\in J.
\end{aligned}
$$

Sustituimos fotografía, podcast y video en ese orden:

$$
\begin{aligned}
\max\quad &h_1+h_2+h_3\\
\text{sujeto a}\quad
&600y_1+800y_2+700y_3\\
&\qquad+300h_1+400h_2+400h_3\le3000,\\
&h_1+h_2+h_3\le5,\\
&y_3\le y_1,\\
&h_1\ge y_1,\\
&h_2\ge y_2,\\
&h_3\ge y_3,\\
&h_1\le2y_1,\\
&h_2\le3y_2,\\
&h_3\le2y_3,\\
&h_1,h_2,h_3\in\mathbb R_{\ge0},\\
&y_1,y_2,y_3\in\{0,1\}.
\end{aligned}
$$

**Comprobación:** si $y_j=0$, ambos límites fuerzan $h_j=0$. Si $y_j=1$,
exigen el intervalo contratado. Escribir $h_j\ge L_j$ sin la decisión de
apertura obligaría a impartir todos los talleres.
:::

Después de comparar ambos intentos, revisa [[opt-modelo-evento|la estructura general y su forma estándar]].
