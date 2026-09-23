---
id: opt-practica-evento
title: "Organizar una tarde de talleres"
nav_title: "Evento · Práctica"
summary: "Dos ejercicios para decidir qué talleres ofrecer y después cuánto dura cada uno, con presupuesto y requisitos entre talleres."
status: ready
tags: [optimizacion, modelado, entera]
---

# Organizar una tarde de talleres

Una asociación estudiantil prepara una tarde de talleres de creación de
contenido. Primero elegirá entre talleres con duración fija; después podrá
negociar cuánto dura cada uno. Los números son didácticos, no cotizaciones
de proveedores reales.

**Tu tarea es escribir los dos modelos completos.** Explica qué se elige,
cómo se cuentan las horas y cuánto se paga. No hace falta encontrar la mejor
programación. Intenta cada problema antes de abrir sus ayudas.

## Problema 5 · Elegir qué talleres ofrecer

::: exercise {#opt-b-evento-elegir title="Una tarde de fotografía, podcast y video"}
La asociación tiene **3000 pesos** y un salón disponible durante **cinco horas
efectivas**. Puede contratar estos talleres; cada precio cubre el taller completo:

| Taller | Pesos | Horas |
|---|---:|---:|
| Fotografía | 1200 | 2 |
| Podcast | 2000 | 3 |
| Video | 1500 | 2 |

Cada taller se ofrece **una vez completo o no se ofrece**. Se imparten uno
después de otro, y los instructores están disponibles durante toda la tarde.
Los cambios de equipo ocurren fuera de las cinco horas efectivas.

La asociación exige que, si ofrece video, también ofrezca fotografía: quiere
que ambos temas formen parte del programa. Fotografía sí puede ofrecerse sin
video. No hay otras condiciones de orden o selección.

La asociación quiere ofrecer **el mayor número total de horas de talleres**,
sin exceder el presupuesto ni el tiempo del salón.

Escribe un modelo que permita elegir el programa. Distingue los datos de las
decisiones, explica qué representa cada variable y los valores que puede tomar.
Incluye el objetivo y todas las condiciones, primero con parámetros y después
con los datos de esta tarde.
:::

### Primero intenta plantearlo

Escribe un primer intento. Si te atoras al separar los datos de las decisiones,
abre esta pista y vuelve a tu hoja.

::: hint {#opt-b-evento-elegir-pista-1 of="opt-b-evento-elegir" title="Pista 1 · ¿Qué está fijado y qué puedes elegir?"}
Cada fila describe el precio y la duración del taller completo:

| Taller | Pesos | Horas |
|---|---:|---:|
| Fotografía | 1200 | 2 |
| Podcast | 2000 | 3 |
| Video | 1500 | 2 |

El precio y la duración de cada taller ya están fijados. La asociación decide
cuáles contratar; cada uno se ofrece completo o no se ofrece.

Hay 3000 pesos y 5 horas disponibles. Video requiere que fotografía esté
en el programa.
:::

Si la condición sobre video y fotografía te detiene, considera esta pregunta.

::: hint {#opt-b-evento-elegir-pista-2 of="opt-b-evento-elegir" title="Pista 2 · ¿Qué combinación está prohibida?"}
¿Cuál combinación de decisiones prohíbe exactamente la frase «si ofrece
video, también ofrece fotografía»?
:::

Cuando tengas una propuesta, compárala con la respuesta paso a paso.

::: answer {#opt-b-evento-elegir-respuesta of="opt-b-evento-elegir" title="Respuesta · Contar las horas y el costo de los talleres elegidos"}
**1. Separar los datos de las decisiones.** Llamamos $J$ al conjunto de
talleres que podemos contratar. Para escribir el modelo antes de sustituir
los números, damos nombre a los datos:

- $c_j$: Precio del taller completo $j$, en pesos.
- $t_j$: Duración del taller completo $j$, en horas.
- $B$: Presupuesto disponible, en pesos.
- $T$: Tiempo disponible en el salón, en horas.

De cada taller debemos decidir **si lo ofrecemos o no**. La variable $y_j$
vale 1 cuando lo ofrecemos y 0 cuando no. Su dominio es $y_j\in\{0,1\}$;
no tiene unidades físicas y no permite contratar una fracción del taller.

**2. Contar las horas y el gasto de lo elegido.** Queremos que un taller
aporte su duración completa cuando se ofrece, y cero cuando no. Multiplicar
su duración por la decisión consigue eso:

$$t_jy_j\quad\text{horas}.$$

La suma de esas aportaciones es el total de horas que queremos maximizar.
También debe caber en las $T$ horas disponibles: los talleres se imparten
uno después de otro en un solo salón.

El precio funciona de la misma manera:

$$c_jy_j\quad\text{pesos}.$$

Sumamos esos gastos y exigimos que no superen $B$. **Horas y pesos se suman
por separado**: cada total responde a una condición distinta del relato.

**3. Representar el requisito entre talleres.** Llamamos $p$ al taller que
debe estar incluido y $q$ al que lo requiere. Queremos prohibir un único caso:
ofrecer $q$ sin ofrecer $p$, es decir, $y_q=1$ y $y_p=0$.

La condición que necesitamos es:

$$y_q\le y_p.$$

Si elegimos $q$, el lado izquierdo vale 1 y obliga a que $y_p$ también valga 1.
Si no elegimos $q$, podemos ofrecer $p$ o dejarlo fuera. Así se permiten ambos,
solo el requerido o ninguno. No estamos imponiendo un orden para impartirlos.

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
condición del programa. Escribir $y_3=y_1$ lo prohibiría y cambiaría el relato.
:::

## Problema 6 · Decidir cuánto dura cada taller

::: exercise {#opt-b-evento-duracion title="Talleres con duración flexible"}
Los instructores cambian su oferta: ahora permiten decidir cuánto dura cada
taller, **incluidas fracciones de hora**. Si se contrata un taller, cobran
una preparación fija una sola vez, más una tarifa por cada hora impartida.

**Estos cobros sustituyen los precios completos del problema 5.** La tabla
muestra el cobro fijo de preparación y el cobro por cada hora, ambos en pesos:

| Taller | Fijo | Por hora |
|---|---:|---:|
| Fotografía | 600 | 300 |
| Podcast | 800 | 400 |
| Video | 700 | 400 |

Los acuerdos con los instructores fijan estas duraciones, en horas, para
cada taller que sí se ofrece:

| Taller | Mínimo | Máximo |
|---|---:|---:|
| Fotografía | 1 | 2 |
| Podcast | 1 | 3 |
| Video | 1 | 2 |

Si un taller no se ofrece, dura cero horas y **no se paga nada por él**, ni
siquiera la preparación. Cada taller puede ofrecerse una sola vez.

El resto de la organización se conserva:

- Hay **3000 pesos** y **cinco horas efectivas** en un solo salón.
- Los talleres se imparten uno después de otro; los instructores están
  disponibles durante toda la tarde.
- Los cambios de equipo quedan fuera de esas cinco horas.
- Si se ofrece video, también se ofrece fotografía. Fotografía puede
  ofrecerse sin video; no hay otras condiciones de orden o selección.

Escribe el modelo completo para **maximizar las horas totales impartidas**.
Explica qué debes decidir ahora y cómo representas tanto los talleres que se
ofrecen como los que quedan fuera. Presenta primero el modelo con parámetros
y después sustituye los datos.
:::

### Primero intenta plantearlo

Intenta adaptar tu modelo anterior. Abre esta pista si necesitas distinguir
lo que cambia de lo que sigue igual.

::: hint {#opt-b-evento-duracion-pista-1 of="opt-b-evento-duracion" title="Pista 1 · Distingue los dos cobros"}
Las tablas del enunciado dan dos cobros distintos: uno por preparar el taller
y otro por cada hora que se imparte. También dan una duración mínima y una
máxima, que solo se exigen si el taller se ofrece.

Sigue habiendo 3000 pesos y 5 horas. Video requiere fotografía, y cada taller
puede ofrecerse una sola vez. Ahora se admiten fracciones de hora; si no se
ofrece un taller, tanto sus horas como su pago son cero.
:::

Si todavía te cuesta representar la duración permitida, revisa estos casos.

::: hint {#opt-b-evento-duracion-pista-2 of="opt-b-evento-duracion" title="Pista 2 · ¿Qué duraciones permite el contrato?"}
¿Tu descripción permite tanto cancelar un taller como ofrecerlo durante una
hora, pero impide ofrecerlo durante media hora?
:::

Antes de abrir la respuesta, comprueba que tu propuesta describe también
un taller que no se ofrece.

::: answer {#opt-b-evento-duracion-respuesta of="opt-b-evento-duracion" title="Respuesta · Relacionar cada taller con su duración"}
**1. Añadir la decisión que cambió.** Conservamos $y_j\in\{0,1\}$, que
indica si ofrecemos el taller. Pero elegirlo ya no determina cuántas horas
dura. Para eso añadimos $h_j$, su duración en horas.

Como se admiten fracciones de hora, $h_j\in\mathbb R_{\ge0}$. Tenemos dos
decisiones por taller: **si se ofrece y cuánto dura**. Los nuevos datos son:

- $f_j$: Preparación del taller, en pesos, si se ofrece.
- $k_j$: Tarifa en pesos por hora impartida.
- $L_j$: Duración mínima contratada, en horas.
- $U_j$: Duración máxima contratada, en horas.

Los límites cumplen $0<L_j\le U_j<\infty$: el mínimo es positivo y no supera
al máximo, que es finito. Los cobros nuevos reemplazan el precio completo
del problema anterior.

**2. Construir los límites por casos.** Primero anotamos las duraciones
permitidas, en horas. Recuerda: $y_j=0$ significa no ofrecer el taller y
$y_j=1$ significa ofrecerlo.

| $y_j$ | Mínimo | Máximo |
|---|---:|---:|
| $0$ | $0$ | $0$ |
| $1$ | $L_j$ | $U_j$ |

El límite inferior debe ser cero si no ofrecemos el taller y $L_j$ si lo
ofrecemos. Podemos escribir ambos casos multiplicando por $y_j$:

$$h_j\ge L_jy_j.$$

El límite superior cambia de cero a $U_j$ de la misma manera:

$$h_j\le U_jy_j.$$

Juntas, estas condiciones relacionan las dos decisiones. Si $y_j=0$, obligan
a que $h_j=0$; si $y_j=1$, exigen una duración entre $L_j$ y $U_j$.
Como el mínimo es positivo, no podemos declarar que ofrecemos un taller
y asignarle cero horas. Los límites vienen del contrato, no de resolver el modelo.

**3. Contar el costo.** La preparación se paga **una sola vez y únicamente
si se ofrece el taller**. Su costo es $f_jy_j$ pesos. A eso sumamos la tarifa
$k_j$ multiplicada por las horas impartidas:

$$f_jy_j+k_jh_j\quad\text{pesos}.$$

Si no ofrecemos el taller, sus horas deben ser cero. Las restricciones
anteriores ya se encargan de exigirlo, así que $k_jh_j$ también vale cero.
No hace falta multiplicar ese término otra vez por $y_j$.

**4. Reunir el modelo.** Sumamos las horas decididas para escribir el objetivo
y el límite de tiempo. Sumamos los costos para respetar el presupuesto.
La condición entre video y fotografía sigue relacionando las decisiones
de ofrecerlos.

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

**5. Sustituir los datos.** Numeramos fotografía, podcast y video como
$1,2,3$, igual que en el primer problema:

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
ofrecer el taller obligaría a impartirlos todos.
:::

Después de comparar ambos intentos, revisa [[opt-modelo-evento|la estructura general y su forma estándar]].
