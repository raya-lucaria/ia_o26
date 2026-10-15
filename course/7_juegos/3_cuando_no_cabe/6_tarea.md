---
id: tarea-cuando-no-cabe
title: "Tarea de refuerzo · Evaluar sin llegar al final"
nav_title: Tarea
summary: "Tres ejercicios para practicar sin ayuda: proponer, usar y criticar una evaluación de gato a profundidad 2; seguir una posición de peones donde mirar más no basta; y comparar Monte Carlo plano, actualización minimax y UCT ante una respuesta final decisiva, distinguiendo la jugada que se selecciona de la que se entrega."
status: ready
estimated_time: 70m
tags: [juegos, evaluacion, monte-carlo, practica]
---

# Tarea de refuerzo · Evaluar sin llegar al final

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin ayuda** lo de la clase:

- **Gato a profundidad 2.** Propones una función de evaluación, calculas minimax con corte a mano y dices qué deja fuera.
- **Otra posición de peones de 4×4.** Sigues la jugada elegida mientras crece la profundidad y nombras el efecto horizonte.
- **Simular partidas.** Comparas qué número calcula cada Monte Carlo cuando aparece una respuesta que derrota a MAX.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

---

## 1 · Evaluar gato a profundidad 2

Gato se juega en una cuadrícula de 3×3. X empieza; por turnos, cada jugador
pone su marca en una casilla vacía. Gana quien completa una de las **8
líneas**: 3 filas, 3 columnas y 2 diagonales. Si se llena la cuadrícula sin
línea, es empate.

- **El estado incluye el turno.** $s=(\text{cuadrícula},\text{turno})$ y $\mathrm{Pl}(s)$ lo lee; una **posición** es un estado.
- **X es MAX y O es MIN.** El pago de un final se mide desde X: $U=+1$ si gana X, $-1$ si gana O y $0$ si empatan.

Supón que X no puede calcular el árbol completo y necesita una función de
evaluación.

::: exercise {#jue-tarea-3-ej-gato title="Propón, usa y critica una evaluación de gato"}
1. Propón una evaluación con dos o tres rasgos y di qué preferencia expresa.
   Escríbela en tu hoja **antes de seguir leyendo**.
2. Ahora usa esta evaluación de referencia:
   $\mathrm{EVAL}(s)=(\text{abiertas para X})-(\text{abiertas para O})$.
   Una línea está **abierta para X** si no tiene ninguna O: X todavía podría
   completarla. Una línea está abierta para O si no tiene ninguna X. Calcula
   $\mathrm{EVAL}$ de la cuadrícula vacía, y después de que X pone en el
   centro.
3. Desde la cuadrícula vacía, X busca con **profundidad 2**: su jugada, la
   respuesta de O y luego evalúa. Por simetría basta con tres tipos de
   primera jugada: **centro**, **esquina** y **borde** (casilla del medio de
   un lado). Para cada una, encuentra la mejor respuesta de O y el valor.
4. ¿Qué jugada elige X?
5. ¿Qué preferencia expresa la evaluación de referencia? Escribe al menos
   dos cosas que deja fuera, y compárala con la tuya.
6. Con juego perfecto, gato termina en empate. ¿Lo sabe la evaluación? ¿Qué
   escala $M$ le darías a los finales, valorados como $M\cdot U$, para que
   la evaluación respete el orden de los finales?
7. ¿Qué tipo de modelo y qué método usaste, y cuántas posiciones evaluaste?
8. Di un límite de la jugada que elegiste: algo que el valor con corte no
   dice.
:::

::: hint {#jue-tarea-3-pista-gato-a of="jue-tarea-3-ej-gato" title="Pista 1 · Cuántas líneas pasan por cada casilla"}
¿Cuántas de las 8 líneas pasan por el centro, por una esquina y por un
borde? Esa cuenta te sirve para elegir rasgos en el inciso 1 y para usar la
evaluación de referencia: una marca de X cierra para O todas las líneas que
pasan por su casilla.
:::

::: hint {#jue-tarea-3-pista-gato-b of="jue-tarea-3-ej-gato" title="Pista 2 · Qué busca O"}
O es MIN: quiere dejar el número más bajo. ¿Dónde cierra **más** líneas de X
una sola marca de O? Con X en el centro, compara a O en una esquina con O en
un borde.
:::

::: answer {#jue-tarea-3-resp-gato of="jue-tarea-3-ej-gato" title="Respuesta · Gato elige el centro"}
**1. Proponer una evaluación.** No hay una sola respuesta correcta. Una
propuesta posible usa dos rasgos: las **amenazas**, líneas con dos marcas
propias y la tercera casilla vacía, y las líneas abiertas:

$$\mathrm{EVAL}_{\text{propia}}(s)=5\cdot\text{amenazas}+\text{abiertas},$$

donde **amenazas** son las de X menos las de O, y **abiertas**, las líneas
abiertas para X menos las abiertas para O.

Expresa que una amenaza vale lo mismo que cinco líneas abiertas: prefiere
estar a una jugada de ganar antes que tener muchas opciones lejanas. Lo que
importa es que tu propuesta diga qué rasgos mira, cómo los pesa y qué
preferencia expresa ese peso.

**2. Contar líneas.** Por el centro pasan 4 líneas: su fila, su columna y
las dos diagonales. Por una esquina pasan 3: fila, columna y una diagonal.
Por un borde pasan 2: fila y columna.

En la cuadrícula vacía, las 8 líneas están abiertas para los dos:
$\mathrm{EVAL}=8-8=0$. Con X en el centro, X conserva 8 líneas abiertas y O
pierde las 4 que pasan por el centro: $\mathrm{EVAL}=8-4=4$.

**3. Profundidad 2.** En cada caso, O pone su marca y se cuentan las líneas:

| Primera de X | Mejor de O | Abiertas X | Abiertas O | Valor |
|---|---|---:|---:|---:|
| Centro | Esquina | $8-3=5$ | $8-4=4$ | **1** |
| Esquina | Centro | $8-4=4$ | $8-3=5$ | $-1$ |
| Borde | Centro | $8-4=4$ | $8-2=6$ | $-2$ |

Con X en el centro, O en un borde dejaría $6-4=2$; la esquina deja menos, así
que O elige esquina. Cada esquina vale $-1$ y cada borde, $-2$.

**4. Elegir la jugada.** X compara $1$, $-1$ y $-2$ y elige el **centro**.

**5. Leer qué deja fuera.** La evaluación de referencia prefiere tener
muchas líneas posibles y quitárselas al rival. Dice que una línea abierta
vale lo mismo esté vacía o casi completa: no ve **amenazas**, porque dos X en
línea con la tercera casilla vacía cuentan igual que una línea sin marcas.
Tampoco distingue **a quién le toca**, aunque el turno está en el estado y una
amenaza vale mucho más si puedes completarla ahora. Y no ve **dobles
amenazas**, que es como se gana en gato. Una propuesta como la del paso 1
cubre las amenazas, pero sigue sin mirar el turno.

**6. Valorar el empate y los finales.** La computadora calcula que gato vale
$V(s_0)=0$: con juego perfecto nadie gana, y comprueba que **cualquier**
primera jugada de X empata. La evaluación dice 1 para el centro y $-1$ para
una esquina, y no sabe que las dos llevan al mismo resultado. Como la
evaluación de referencia queda siempre entre $-8$ y $8$, basta cualquier
$M>8$; con $M=100$, los finales valen $M\cdot U$, es decir, $+100$ si gana X, $-100$ si gana O y
$0$ si empatan, y $|\mathrm{EVAL}|<M$. La evaluación estima $M\cdot V$; un
final se reconoce **antes** de cortar y aporta $M\cdot U$. Con tu propia
evaluación, $M$ tiene que quedar por encima de lo más alto que pueda dar.

**7. Tipo de modelo, método y costo.** Juego por turnos, determinista, de
información perfecta y suma cero, resuelto con **minimax con corte a
profundidad 2** y una evaluación escrita a mano. Mirar todas las parejas de
jugada y respuesta son $9\cdot8=72$ posiciones evaluadas; la simetría lo
reduce a tres casos, cada uno con sus respuestas de O.

**8. Límite.** El valor con corte es el minimax del árbol truncado con
$\mathrm{EVAL}$ en la frontera, no $V$: aquí distingue centro, esquina y
borde, aunque las tres primeras jugadas empatan con juego perfecto. La
preferencia por el centro es un supuesto de la evaluación, no un resultado
del juego.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Tu evaluación va primero.** Escribiste la tuya y su preferencia antes de usar la de referencia.
- **Contaste para los dos.** Las líneas abiertas son de X **y** de O, no solo de X.
- **O minimiza.** En la profundidad 2, O eligió la respuesta **más baja** para X.
- **Lo que falta es un supuesto.** Escribiste qué deja fuera la evaluación como supuestos, no como errores de cuenta.

---

## 2 · Otra posición de peones donde mirar más no basta

Las reglas son las de la clase: tablero de 4×4, gana quien llega a la fila
del rival, captura todo o deja al rival sin jugada. Blancas es MAX; los
finales valen $M\cdot U=\pm100$, con $M=100$. La evaluación es la misma:

$$\mathbf{\mathrm{EVAL}(s)=10\cdot\text{material}+\text{avance}},$$

donde **material** es peones blancos menos peones negros, y **avance** es el
avance blanco menos el avance negro. El avance de un peón blanco es cuántas
filas subió desde la fila 1; el de uno negro, cuántas bajó desde la fila 4.

::: exercise {#jue-tarea-3-ej-peones title="Sigue la decisión al crecer la profundidad"}
Mueven Blancas en esta posición:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | N |
| **2** | B | · | · | B |
| **1** | · | B | B | · |

1. Escribe $A(s)$ y calcula $\mathrm{EVAL}(s)$.
2. Calcula el valor de cada jugada a **profundidad 1**. ¿Cuál elige Blancas?
3. A **profundidad 2**, $\text{b1}\textbf{-}\text{b2}$ y $\text{c1}\textbf{-}\text{c2}$ valen $-11$ cada una. Calcula el valor
   de $\text{a2}\textbf{-}\text{a3}$ y el de $\text{d2}\textbf{x}\text{c3}$, escribiendo cada respuesta de Negras con su
   $\mathrm{EVAL}$. ¿Cuál elige Blancas?
4. La computadora calcula los valores exactos, en la escala de $U$: $\text{b1}\textbf{-}\text{b2}$, $\text{c1}\textbf{-}\text{c2}$ y $\text{d2}\textbf{x}\text{c3}$ valen
   $-1$; **$\text{a2}\textbf{-}\text{a3}$ vale $+1$**. Y a más profundidad da:

   | Jugada | Prof. 3 | Prof. 4 | Prof. 5 |
   |---|---:|---:|---:|
   | $\text{b1}\textbf{-}\text{b2}$ | 1 | $-100$ | $-100$ |
   | $\text{c1}\textbf{-}\text{c2}$ | 1 | $-100$ | $-100$ |
   | $\text{a2}\textbf{-}\text{a3}$ | 0 | $-1$ | 100 |
   | $\text{d2}\textbf{x}\text{c3}$ | 0 | $-1$ | 12 |

   ¿Qué jugadas elige Blancas a cada profundidad, de 1 a 5? ¿Qué te dice eso
   sobre subir la profundidad?
5. ¿En qué profundidades aparece el efecto horizonte? Señala qué respuesta o
   qué final quedó detrás del corte.
6. ¿Qué tipo de modelo y qué método usaste, y cuánto cuesta cada profundidad
   más?
7. Di un límite: ¿subir la profundidad garantiza acercarse a la jugada
   correcta?
:::

::: hint {#jue-tarea-3-pista-peones-a of="jue-tarea-3-ej-peones" title="Pista 1 · Las capturas de Negras"}
Tras cada jugada de Blancas, busca qué peones negros pueden capturar en
diagonal hacia abajo. ¿Cuánto cambia la evaluación cuando desaparece un
peón?
:::

::: hint {#jue-tarea-3-pista-peones-b of="jue-tarea-3-ej-peones" title="Pista 2 · La recaptura"}
Tras $\text{d2}\textbf{x}\text{c3}$, el peón blanco queda en c3. ¿Qué peón negro lo tiene en diagonal?
Tras $\text{a2}\textbf{-}\text{a3}$, ¿qué peón negro lo tiene en diagonal?
:::

::: answer {#jue-tarea-3-resp-peones of="jue-tarea-3-ej-peones" title="Respuesta · La captura engaña a dos profundidades"}
**1. Leer la posición.** $A(s)=\{\text{b1}\textbf{-}\text{b2},\ \text{c1}\textbf{-}\text{c2},\ \text{a2}\textbf{-}\text{a3},\ \text{d2}\textbf{x}\text{c3}\}$.
El peón de d2 tiene d3 ocupada enfrente, pero puede capturar en c3. Cada lado
tiene 4 peones; el avance de Blancas es $1+1=2$ (a2 y d2) y el de Negras,
$1+1=2$ (c3 y d3). $\mathrm{EVAL}=0$.

**2. Mirar a profundidad 1.** Las tres jugadas que avanzan suben el avance
blanco a 3: valen $0+(3-2)=1$. La captura deja 4 peones contra 3, con avance
blanco 3 (a2, y el peón que llegó a c3) y negro 1: $10+(3-1)=12$. Blancas
elige **$\text{d2}\textbf{x}\text{c3}$**.

**3. Mirar a profundidad 2.** Negras elige la respuesta de menor evaluación:

| Jugada | Respuestas de Negras y su $\mathrm{EVAL}$ | Valor |
|---|---|---:|
| $\text{a2}\textbf{-}\text{a3}$ | $\text{c3}\textbf{-}\text{c2}$: 0 · $\text{c3}\textbf{x}\text{d2}$: $-11$ · $\text{b4}\textbf{-}\text{b3}$: 0 · $\text{b4}\textbf{x}\text{a3}$: $-12$ | $-12$ |
| $\text{d2}\textbf{x}\text{c3}$ | $\text{d3}\textbf{-}\text{d2}$: 11 · $\text{a4}\textbf{-}\text{a3}$: 11 · $\text{b4}\textbf{-}\text{b3}$: 11 · $\text{b4}\textbf{x}\text{c3}$: $-1$ | $-1$ |

Con $\text{b1}\textbf{-}\text{b2}$ y $\text{c1}\textbf{-}\text{c2}$ en $-11$, Blancas compara $-11$, $-11$, $-12$ y $-1$, y
**sigue eligiendo $\text{d2}\textbf{x}\text{c3}$**. La recaptura $\text{b4}\textbf{x}\text{c3}$ ya se ve, pero las otras jugadas
también regalan un peón.

**4. Seguir la decisión al crecer la profundidad.** La jugada elegida es un
$a^{∗}\in\operatorname*{arg\,max}_a V_{d-1}(T(s,a))$, así que puede haber empates:

| Profundidad | Mejor valor | Jugadas empatadas |
|---:|---:|---|
| 1 | 12 | $\text{d2}\textbf{x}\text{c3}$ |
| 2 | $-1$ | $\text{d2}\textbf{x}\text{c3}$ |
| 3 | 1 | $\text{b1}\textbf{-}\text{b2}$, $\text{c1}\textbf{-}\text{c2}$ |
| 4 | $-1$ | $\text{a2}\textbf{-}\text{a3}$, $\text{d2}\textbf{x}\text{c3}$ |
| 5 | 100 | $\text{a2}\textbf{-}\text{a3}$ |

Solo $\text{a2}\textbf{-}\text{a3}$ gana, y solo a profundidad 5 la búsqueda la elige sin empate. La
elección cambió **varias veces**: de la captura a dos jugadas perdedoras,
luego a un empate entre la buena y la captura, y por fin a la buena.

**5. Nombrar el efecto horizonte.** Es **efecto horizonte** cada vez que una
consecuencia decisiva queda justo detrás del corte. A profundidad 1, $\text{d2}\textbf{x}\text{c3}$
vale 12 porque la recaptura $\text{b4}\textbf{x}\text{c3}$ queda detrás del horizonte; a profundidad 2
ya se ve y la captura baja a $-1$. A profundidad 3, $\text{b1}\textbf{-}\text{b2}$ y $\text{c1}\textbf{-}\text{c2}$ parecen
valer 1, y a profundidad 4 aparece que pierden ($-100$): esa derrota estaba
detrás del horizonte. Y la victoria de $\text{a2}\textbf{-}\text{a3}$ solo aparece a profundidad 5.

**6. Tipo de modelo, método y costo.** El mismo árbol MAX/MIN de un juego
por turnos, determinista y de suma cero, resuelto con **minimax con corte**:
$d$ cuenta las decisiones que faltan por mirar, y $V_d$ vale $M\cdot U$ en un
final y $\mathrm{EVAL}$ cuando $d=0$. Cuesta $O(b^d)$ con ramificación $b$;
cada profundidad más multiplica el trabajo por hasta $b$. En esta posición, la
computadora cuenta 5, 22, 90, 315 y 1001 nodos con $d=1$ a 5, contando la
raíz: cada nivel multiplica el trabajo por entre 3.2 y 4.4.

**7. Límite.** **Más profundidad no siempre basta**: el valor con corte no se
acerca al exacto de forma ordenada, y a una profundidad dada puede elegir una
jugada que pierde. Solo los valores $\pm100$ son seguros; los demás son
estimaciones de la evaluación.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Las cuatro jugadas.** Encontraste todas, incluida la captura de d2.
- **Todas las respuestas.** A profundidad 2 revisaste **todas** las de Negras, también las capturas.
- **Los empates a la vista.** Los señalaste en lugar de elegir una jugada al azar.
- **El horizonte con nombre.** En cada cambio de decisión, nombraste qué quedó detrás del corte.

---

## 3 · Tres Monte Carlo ante una respuesta certera

Ahora no hay $\mathrm{EVAL}$: se simulan partidas al azar hasta un final. Usa
este árbol pequeño; los pagos están en la escala de $U$, desde MAX:

- **La raíz pertenece a MAX.** Sus jugadas A y B llevan a dos estados donde mueve MIN.
- **Tras A, MIN tiene cuatro finales.** $\text{a1}=\text{a2}=\text{a3}=+1$ y $\text{a4}=-1$: a4 es la respuesta certera.
- **Tras B, MIN tiene dos opciones.** El final $\text{b1}=0$, o el estado E, donde MAX elige entre $\text{e1}=0$ y $\text{e2}=+1$.

Escribimos $Q(\text{A})$ por $Q(s_{\text{raíz}},\text{A})$, y lo mismo con B,
$Q_{\text{azar}}$ y $\widehat Q$. Las simulaciones eligen uniformemente entre
las jugadas legales, como en [[simular-en-vez-de-evaluar|Simular partidas]].

- **Aquí la raíz también se muestrea al azar.** Monte Carlo plano no fija $k$ simulaciones por jugada; usa las mismas partidas que la actualización minimax.
- **Las corridas son reales.** Salen de `tools/juegos.py` con semilla 0; en UCT, $c=1$ y los empates se resuelven por orden.

::: exercise {#jue-tarea-3-ej-simular title="Compara tres Monte Carlo ante una respuesta certera"}
1. **Valores exactos.** Calcula $Q(\text{A})$, $Q(\text{B})$, $Q_{\text{azar}}(\text{A})$ y
   $Q_{\text{azar}}(\text{B})$. ¿Qué jugada es la correcta? ¿Cuál termina prefiriendo
   Monte Carlo plano con muchas simulaciones?
2. **Las mismas 11 partidas.** Una corrida termina, en este orden, en e1, e2,
   e2, a2, b1, a3, a3, a1, e1, e2 y a4. Para Monte Carlo plano y para la
   actualización minimax, escribe $\widehat Q(\text{A})$ y $\widehat Q(\text{B})$
   tras las simulaciones 3, 5, 10 y 11; usa «?» para lo desconocido. ¿Qué
   entrega cada uno tras la 11?
3. **Seleccionar frente a entregar.** Una corrida de UCT con $c=1$ agrega A
   en la vuelta 1, y su simulación cae en a4. Tras la vuelta 15, $N(s_{\text{raíz}})=15$ y:

   | Jugada | $N(s,a)$ | $\widehat Q(s,a)$ |
   |---|---:|---:|
   | A | 4 | $1/2$ |
   | B | 11 | $1/11$ |

   Calcula $\widehat Q+\text{bono}$ de cada jugada. ¿Cuál selecciona la
   vuelta 16? Si el tiempo se acaba ahí, ¿cuál entrega UCT? ¿Por qué no
   entrega la de mayor $\widehat Q$?
4. **Una respuesta no es un voto.** UCT vio a4 en la vuelta 1, y aun así
   $\widehat Q(\text{A})=1/2$ en la 15. Explica por qué. En las vueltas 16, 17
   y 18 la selección baja por A hasta a4: ¿cuánto vale $\widehat Q(\text{A})$
   tras cada una?
5. **A qué converge cada uno.** Con presupuesto sin límite, ¿a qué número se
   acerca $\widehat Q(\text{A})$ en cada método, y qué jugada entrega cada uno?
:::

::: hint {#jue-tarea-3-pista-simular-a of="jue-tarea-3-ej-simular" title="Pista 1 · Quién decide en cada número"}
En $Q$, MIN elige su mejor respuesta en A y en B, y MAX la suya en E. En
$Q_{\text{azar}}$, todos eligen al azar: cada final de A pesa $1/4$; en B,
b1 pesa $1/2$, y e1 y e2 pesan $1/4$ cada uno.
:::

::: hint {#jue-tarea-3-pista-simular-b of="jue-tarea-3-ej-simular" title="Pista 2 · Qué mira cada regla"}
El bono es $c\sqrt{\ln N(s)/N(s,a)}$, con $\ln 15\approx2.708$. Seleccionar
compara $\widehat Q+\text{bono}$; entregar compara solo $N(s,a)$. Al
promediar, cada pago pesa $1/N$, sea cual sea quién lo eligió.
:::

::: answer {#jue-tarea-3-resp-simular of="jue-tarea-3-ej-simular" title="Respuesta · Solo el respaldo minimax cambia en el acto"}
**1. Valores exactos.** MIN responde a4 en A y b1 en B:

$$
Q(\text{A})=\min(1,1,1,-1)=-1,\qquad Q(\text{B})=\min\bigl(0,\max(0,1)\bigr)=0.
$$

La correcta es **B**, con $V=0$. Con todos al azar:

$$
Q_{\text{azar}}(\text{A})=\frac{1+1+1-1}{4}=\frac12,\qquad
Q_{\text{azar}}(\text{B})=\frac{0+\tfrac12}{2}=\frac14.
$$

Monte Carlo plano termina prefiriendo **A**, que pierde contra a4.

**2. Las mismas 11 partidas.** «Plano» promedia el $U$ crudo; «minimax»
respalda máximos y mínimos sobre lo descubierto:

| Tras | Plano A | Plano B | Minimax A | Minimax B |
|---:|---:|---:|---:|---:|
| 3 | ? | $2/3$ | ? | $1$ |
| 5 | $1$ | $1/2$ | $1$ | $0$ ✓ |
| 10 | $1$ | $1/2$ | $1$ | $0$ ✓ |
| 11 | $3/5$ | $1/2$ | $-1$ ✓ | $0$ ✓ |

- **Tras la 3, B vale 1 en minimax.** MIN solo conoce E, y E ya vale $\max(0,1)=1$; el número es provisional.
- **La 5 descubre b1.** B baja a $\min(0,1)=0$ y queda exacto ✓: E y b1 ya se conocen.
- **La 11 descubre a4.** Minimax baja A a $-1$, el menor pago posible, y entrega **B**; el promedio de A solo baja a $3/5$ y sigue entregando **A**.

**3. Seleccionar frente a entregar.** Con $c=1$, el bono de A es
$\sqrt{2.708/4}\approx0.823$ y el de B, $\sqrt{2.708/11}\approx0.496$:

| Jugada | $\widehat Q$ | Bono | $\widehat Q+\text{bono}$ |
|---|---:|---:|---:|
| A | $0.5$ | $0.823$ | $1.323$ |
| B | $0.091$ | $0.496$ | $0.587$ |

- **La vuelta 16 selecciona A.** Su promedio es alto y tiene pocas visitas; el bono sirve para seguir aprendiendo.
- **Si se acaba el tiempo, se entrega B.** Tiene 11 visitas contra 4: se juega la más visitada, sin bono.
- **El mayor $\widehat Q$ engaña aquí.** El $1/2$ de A descansa en cuatro vueltas, y $Q(\text{A})=-1$.

**4. Una respuesta no es un voto.** En la vuelta 1, la simulación desde A
aportó un $-1$ al llegar a a4, pero no agregó a4 al árbol. Las vueltas 13 a
15 agregaron a1, a2 y a3, y cada una aportó $+1$. El promedio es
$(-1+1+1+1)/4=1/2$: la respuesta certera pesa como una observación más.

- **Vuelta 16.** La expansión agrega a4: $\widehat Q(\text{A})=(2-1)/5=1/5$.
- **Vuelta 17.** MIN ya conoce a4 y baja por el menor $\widehat Q-\text{bono}$, que es a4: $\widehat Q(\text{A})=0/6=0$.
- **Vuelta 18.** Otra vez a4: $\widehat Q(\text{A})=-1/7$, y ahora el puntaje de B vuelve a ganar.

El promedio de A baja porque la selección de MIN **concentra** las vueltas en
a4, no porque UCT tome un mínimo. La actualización minimax, con un solo a4,
habría fijado $-1$ en ese mismo respaldo.

**5. A qué converge cada uno.**

- **Monte Carlo plano:** $\widehat Q(\text{A})\to Q_{\text{azar}}(\text{A})=1/2$ y entrega A, que pierde.
- **Actualización minimax:** llega a $-1$ en cuanto descubre a4, y entrega B; aquí la raíz quedó resuelta en la simulación 11. Converge porque el árbol es finito, todas las jugadas legales tienen probabilidad positiva, los finales son reales y lo descubierto se conserva.
- **UCT:** $\widehat Q(\text{A})\to Q(\text{A})=-1$ en un árbol finito, con $c>0$ fija y vueltas sin límite, pero despacio. En la vuelta 1000, A lleva 15 visitas y $\widehat Q(\text{A})=-3/5$; B, 985 visitas, y UCT entrega B desde la vuelta 3.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Dos preguntas distintas.** Separaste $Q$, con MIN eligiendo, de $Q_{\text{azar}}$, con todos al azar.
- **Desconocido no es cero.** En la actualización minimax dejaste «?» donde no había visitas.
- **Exacto contra provisional.** Marcaste qué valores ya no puede cambiar ninguna partida nueva.
- **Dos reglas en UCT.** Para seleccionar usaste el bono; para entregar, solo las visitas.

**Punto de control:** deberías poder proponer una evaluación para un juego
nuevo y decir qué preferencia expresa; seguir a mano cómo cambia la jugada
elegida al subir la profundidad; y decir, para cada Monte Carlo, qué número
estima, qué hace con una respuesta certera y qué jugada entrega.

## Lo que hay que llevarse

- **Una evaluación es un modelo escrito a mano.** Expresa una preferencia y
  deja fuera cosas como las amenazas o quién mueve.
- **Minimax con corte se calcula igual que minimax.** Solo cambia lo que vale
  una hoja de corte: $\mathrm{EVAL}$, o $M\cdot U$ si es un final.
- **Subir la profundidad no garantiza acercarse a la jugada correcta.** La
  elección puede cambiar varias veces, y esos cambios delatan lo que estaba
  detrás del horizonte.
- **Cada Monte Carlo converge a lo que simula.** El promedio plano va a
  $Q_{\text{azar}}$; la actualización minimax fija una respuesta certera en
  cuanto la ve; UCT la alcanza concentrando sus vueltas, y entrega la jugada
  más visitada, no la de mayor puntaje.

Continúa con [[juegos-radiografia|la radiografía de los algoritmos]].
