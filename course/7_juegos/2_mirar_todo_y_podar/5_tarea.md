---
id: tarea-mirar-todo-y-podar
title: "Tarea de refuerzo · Calcular y podar"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: resolver monedas en fila con minimax y alfa-beta, y decidir cuándo dejar de tirar el dado en un juego de azar."
status: ready
estimated_time: 45m
tags: [juegos, minimax, alfa-beta, azar, practica]
---

# Tarea de refuerzo · Calcular y podar

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin
ayuda** lo de la clase: escribir un juego, calcular su valor y su jugada
óptima, podar con alfa-beta y valorar nodos de azar.

El primer ejercicio es un juego nuevo, sin azar. El segundo es un juego de
dado, donde no hay rival.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

## 1 · Resolver monedas en fila

> **Monedas en fila.** Hay cuatro monedas en fila, con valores
> $(2,1,5,3)$ de izquierda a derecha. Dos jugadores se turnan; en cada
> turno, el jugador toma **una moneda de un extremo**: la de la izquierda o
> la de la derecha. Cuando no quedan monedas, gana quien suma más.

Quien empieza es MAX. Su utilidad es la **diferencia** $\Delta$: sus
puntos menos los del rival. Cuando queda una sola moneda, hay una sola
jugada: tomarla.

Puedes medir desde el punto de vista de quien mueve: lo que tomas menos lo
que el rival asegura después.

::: exercise {#jue-tarea-2-ej-monedas title="Resuelve monedas en fila"}
1. Escribe el modelo: qué guarda un estado, $P(s)$, $A(s)$, $T(s,a)$, los
   finales y $U(s)$.
2. ¿Cuántos nodos tiene el árbol completo y cuántos son finales?
3. Calcula con minimax el valor de la raíz. ¿Qué moneda debe tomar MAX
   primero? ¿Con cuántos puntos termina cada jugador?
4. La regla codiciosa dice «toma siempre la moneda mayor». Si MAX la sigue
   en todos sus turnos y el rival juega perfecto, ¿cómo termina?
5. ¿Cuántas situaciones distintas hay si solo importa qué monedas quedan?
   ¿Por qué basta con eso para reutilizar valores?
6. Si recorres el árbol con alfa-beta, ¿esperas ahorrar mucho? Explica qué
   decide el ahorro.
:::

::: hint {#jue-tarea-2-pista-monedas-a of="jue-tarea-2-ej-monedas" title="Pista 1 · Qué guarda el estado"}
Las monedas que quedan siempre forman un tramo seguido de la fila original:
basta con dos índices, el primero y el último que quedan. Pero la utilidad
depende también de quién tomó qué. ¿Qué número tienes que llevar para
calcular $\Delta$ al final?
:::

::: hint {#jue-tarea-2-pista-monedas-b of="jue-tarea-2-ej-monedas" title="Pista 2 · Empieza por las filas cortas"}
Para cada tramo que quede, calcula la diferencia que puede asegurar **quien
mueve** desde ahí. Con una moneda, la toma. Con dos, ¿cuál toma? Con tres,
prueba los dos extremos y usa los tramos de dos que ya calculaste.
:::

::: answer {#jue-tarea-2-resp-monedas of="jue-tarea-2-ej-monedas" title="Respuesta · Monedas en fila"}
**1. El modelo.** Un estado guarda el tramo que queda, de la moneda $i$ a
la $j$; a quién le toca; y $\Delta$, los puntos de MAX menos los del rival
hasta ahora. Al inicio, $s_0=(1,4,\text{MAX},0)$.

| Pieza | En monedas en fila |
|---|---|
| $s_0$ | Las cuatro monedas, le toca a MAX, $\Delta=0$ |
| $P(s)$ | Se alternan; con 4 monedas, MAX mueve cuando queda un número par |
| $A(s)$ | $\{$izquierda, derecha$\}$; con una sola moneda, solo tomarla |
| $T(s,a)$ | Quita la moneda de ese extremo, la suma a $\Delta$ si movió MAX o la resta si movió el rival, y cambia el turno |
| Finales | No quedan monedas |
| $U(s)$ | $\Delta$: los puntos de MAX menos los del rival |

Como en hexapawn con $k$, el estado guarda $\Delta$ porque la utilidad
depende de él y no se ve en las monedas que quedan.

**2. El árbol.** Toda partida dura 4 jugadas. Con dos o más monedas hay dos
hijos; con una, uno solo. Por niveles: $1+2+4+8+8=$ **23 nodos**, de los
cuales **8 son finales**.

**3. Minimax.** Para cada tramo, $W$ es la diferencia que asegura **quien
mueve** con las monedas que quedan. Lo que tomas cuenta a tu favor y lo que
el rival asegura después cuenta en contra:

$$W(\text{tramo})=\max\{\text{izquierda}-W(\text{lo que queda}),\ \text{derecha}-W(\text{lo que queda})\}.$$

| Tramo | Cuenta | $W$ |
|---|---|---:|
| $(2)$, $(1)$, $(5)$, $(3)$ | Se toma la única moneda | 2, 1, 5, 3 |
| $(2,1)$ | $\max\{2-1,\ 1-2\}$ | 1 |
| $(1,5)$ | $\max\{1-5,\ 5-1\}$ | 4 |
| $(5,3)$ | $\max\{5-3,\ 3-5\}$ | 2 |
| $(2,1,5)$ | $\max\{2-4,\ 5-1\}$ | 4 |
| $(1,5,3)$ | $\max\{1-2,\ 3-4\}$ | −1 |
| $(2,1,5,3)$ | $\max\{2-(-1),\ 3-4\}$ | **3** |

El valor de la raíz es **+3** y la jugada óptima es **tomar el 2**, la
moneda menor. Tras el 2, al rival le queda $(1,5,3)$ y las dos jugadas le
dan −1: tome lo que tome, MAX toma después el 5. MAX termina con **7**
puntos y el rival con **4**.

**4. La trampa codiciosa.** Tomar el 3 deja $(2,1,5)$ al rival, que asegura
4 tomando el 5. Después MAX toma el 2 y el rival el 1: MAX suma **5**, el
rival **6**, y la diferencia es **−1**. Tomar la mayor le regaló al rival la
moneda de 5.

**5. El grafo.** Lo que se puede conseguir **desde aquí** solo depende del
tramo que queda; $\Delta$ se suma al final y no cambia qué conviene. Hay
$4+3+2+1=10$ tramos con monedas más el vacío: **11 situaciones**, contra 23
nodos. La tabla del paso 3 es exactamente minimax sobre ese grafo.

**6. Alfa-beta.** Con el árbol de 23 nodos, alfa-beta visita los **23** si
revisa primero la izquierda y **21** si revisa primero la derecha. Ahorra
poco: el árbol es pequeño, cada nodo tiene solo dos hijos y los valores de
los hermanos están cerca. Alfa-beta nunca empeora a minimax, pero **no
siempre ahorra mucho**; lo decide el orden y la forma del árbol.

**7. Tipo de modelo, método y costo.** Juego por turnos, finito, sin azar,
de información completa y suma cero: un árbol MAX/MIN. Se resuelve con
minimax. Con $n$ monedas, el árbol tiene del orden de $2^n$ nodos; con
memoria sobre los tramos hay $n(n+1)/2+1$ situaciones y cada una cuesta dos
restas y un máximo, así que el costo baja a $O(n^2)$.

**8. Límite.** El $+3$ supone que el rival juega perfecto: es lo que MAX
**asegura**, no lo que obtendrá contra un rival que se equivoca, que puede
ser más. Y $\Delta$ mide por cuánto se gana; si solo importara ganar,
jugadas con diferencias distintas podrían valer lo mismo.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Tu estado permite calcular la utilidad al final sin mirar la historia.
- Valoraste los tramos cortos antes que los largos.
- Distinguiste el valor (+3) de la jugada (tomar el 2).
- Comparaste la regla codiciosa contra un rival que juega perfecto, no
  contra uno que también es codicioso.

**Lo que deja este ejercicio.** Midiendo desde quien mueve, una sola
fórmula sirve para los dos jugadores: $W$ es lo que tomas menos el $W$ del
rival en el tramo que te deja. Y aunque el estado completo necesita $\Delta$
para calcular la utilidad, **para reutilizar valores no hace falta**: lo
que se gana desde aquí solo depende del tramo, y $\Delta$ se suma al final.

## 2 · Decidir cuándo dejar de tirar

> **Cerdo reducido.** Tienes 3 puntos **sin asegurar**. En tu turno puedes
> **plantarte**, y los 3 puntos quedan asegurados, o **tirar** un dado de
> seis caras. Si sale 1, pierdes todo lo no asegurado y terminas con 0. Si
> sale 2, 3, 4, 5 o 6, sumas esa cara a tus puntos sin asegurar.

Es una versión pequeña de un juego de dados llamado *Pig*. Aquí no hay
rival: solo tú y el dado. Quieres el mayor número de puntos asegurados en
promedio.

::: exercise {#jue-tarea-2-ej-cerdo title="Decide si tiras otra vez"}
1. Dibuja el árbol si solo puedes tirar **una vez**. ¿Qué tipo es cada
   nodo? ¿Cuánto vale tirar? ¿Te plantas o tiras?
2. Con una sola tirada y $x$ puntos sin asegurar, ¿hasta qué $x$ conviene
   tirar?
3. Ahora puedes tirar **hasta dos veces**, decidiendo después de la primera.
   ¿Cuánto vale empezar desde 3 puntos? ¿Conviene siempre tirar la segunda?
4. **Extra:** ¿qué harías desde 3 puntos si el dado lo controlara un rival
   que quiere que pierdas?
:::

::: hint {#jue-tarea-2-pista-cerdo-a of="jue-tarea-2-ej-cerdo" title="Pista 1 · Qué tipo de nodo es cada uno"}
Hay nodos donde decides tú y nodos donde decide el dado. No hay nodos MIN.
¿Qué operación corresponde a cada uno de los dos tipos?
:::

::: hint {#jue-tarea-2-pista-cerdo-b of="jue-tarea-2-ej-cerdo" title="Pista 2 · La cuenta de una tirada"}
Cada cara pesa $1/6$; la cara 1 deja 0.
:::

::: answer {#jue-tarea-2-resp-cerdo of="jue-tarea-2-ej-cerdo" title="Respuesta · Cerdo reducido"}
**1. Una tirada.** La raíz es tuya (MAX): plantarte vale 3. Tirar lleva a
un nodo de **azar** con seis resultados, cada uno con probabilidad $1/6$.
Todos son finales, porque ya no quedan tiradas: 0 si sale 1, y 5, 6, 7, 8
o 9 si sale 2 a 6.

$$V(\text{tirar})=\tfrac16\cdot0+\tfrac16(5+6+7+8+9)=\tfrac{35}{6}\approx5.83.$$

Como $35/6>3$, **conviene tirar**.

**2. Hasta cuánto conviene.** Con $x$ puntos,

$$V(\text{tirar})=\tfrac16\cdot0+\tfrac16\bigl[(x+2)+(x+3)+(x+4)+(x+5)+(x+6)\bigr]=\tfrac{5x+20}{6}.$$

Es mayor o igual que $x$ cuando $5x+20\ge6x$, es decir, cuando $x\le20$.
**Con una tirada, tirar conviene mientras tengas a lo más 20 puntos.** En 20
empatan: tirar también vale 20.

**3. Dos tiradas.** Valoramos desde abajo. Tras la primera tirada exitosa
tienes entre 5 y 9 puntos y te queda una tirada. Como $5\le x\le9\le20$,
por el paso 2 **siempre conviene tirar la segunda**, y vale $(5x+20)/6$:

| Puntos tras la primera | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|
| Valor de tirar otra vez | $15/2$ | $25/3$ | $55/6$ | $10$ | $65/6$ |

La primera tirada promedia esos cinco valores, más 0 si sale 1:

$$V=\tfrac16\cdot0+\tfrac16\Bigl(\tfrac{45}{6}+\tfrac{50}{6}+\tfrac{55}{6}+\tfrac{60}{6}+\tfrac{65}{6}\Bigr)=\tfrac{275}{36}\approx7.64.$$

Desde 3 puntos, con hasta dos tiradas, el valor óptimo es $275/36$: tirar
y, si no sale 1, volver a tirar.

**4. Si el dado fuera un rival.** Sería un nodo MIN: siempre saldría 1 y
tirar valdría 0. Te plantarías con 3. Es el error de la página
[[cuando-decide-un-dado|Cuando decide un dado]]: con un dado justo, esa
prudencia te cuesta en promedio $35/6-3$ puntos con una sola tirada.

**5. Tipo de modelo, método y costo.** Juego de un solo jugador contra el
azar, finito, con nodos MAX y de azar, sin nodos MIN. Se resuelve con
expectiminimax, desde la última tirada hacia la primera. Cada tirada
permitida añade un nodo de azar con seis resultados, y cinco de ellos
siguen jugando, así que con $t$ tiradas el árbol crece como $5^t$; aquí,
con $t\le2$, la cuenta cabe en una hoja.

**6. Límite.** El modelo maximiza el **promedio**: no le importa el riesgo
de terminar en 0, que con dos tiradas existe aunque tirar convenga. Y el
*Pig* real tiene un rival y una meta de puntos, no un número fijo de
tiradas; ahí lo que conviene depende también del marcador del otro.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Cada nodo de tu árbol dice si lo decides tú o el dado.
- En los nodos de azar promediaste con $1/6$, incluido el 0 del 1.
- En el inciso 3 valoraste primero la segunda tirada y después la primera.

**Punto de control:** deberías poder escribir el modelo de un juego pequeño,
decir qué tipo es cada nodo, valorarlo con minimax o expectiminimax y
separar lo que el estado necesita para la utilidad de lo que basta para
reutilizar valores.

## Lo que hay que llevarse

- El estado guarda lo necesario para la utilidad: $k$ en hexapawn, $\Delta$
  en monedas. Para reutilizar valores basta lo que decide el futuro: el
  tramo que queda.
- La jugada codiciosa puede perder: minimax compara contra la mejor
  respuesta del rival, no contra la que esperas.
- Con azar se promedia; con rival se minimiza. Confundirlos cambia la
  decisión.

Continúa con [[juegos-cuando-no-cabe|la clase 3]], donde el árbol ya no cabe.
