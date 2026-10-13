---
id: que-numero-da-cada-uno
title: Qué número da cada uno
nav_title: Qué número da cada uno
summary: "Minimax da V, el corte da un valor con corte y las simulaciones dan ū: tres números que no miden lo mismo. Cómo leer cada uno en T±, dos tablas para comparar los algoritmos, y cuándo un número permite dejar de buscar."
status: ready
estimated_time: 20m
tags: [juegos, busqueda-adversarial, comparacion]
---

# Qué número da cada uno

**¿Qué significa el número que devuelve cada algoritmo?**

Al terminar tendrás:

- los **tres números** de la unidad, $V$, el valor con corte y $\bar u$, y
  de qué jugadores habla cada uno;
- por qué en T± el 0, el 60 y los dos $1/3$ no se contradicen;
- dos tablas para poner los algoritmos lado a lado: **cómo busca** cada uno
  y **qué número da**;
- la regla para **dejar de buscar** al ver lo mejor posible, y cuándo no se
  vale.

> **Lo que traes de [[un-arbol-todos-los-algoritmos|Un árbol, todos los algoritmos]].**
> Ahí corriste cada algoritmo de la unidad sobre el mismo árbol, T±, y cada
> uno entregó una jugada y un número. La página cerró con una pregunta:
> ¿qué es cada número? Esta página la contesta.

> **T± en cuatro líneas.** La raíz R es de MAX: izq lleva a I, centro a C y
> der a D, los tres de MIN. Bajo I, ${\text{i1}=+1}$ y la captura
> ${\text{ix}=-1}$. Bajo C, dos nodos de MAX: C1 con ${\text{c1a}=0}$ y
> ${\text{c1b}=-1}$; C2 con ${\text{c2a}=+1}$ y ${\text{c2b}=-1}$. Bajo D,
> ${\text{d1}=-1}$, ${\text{d2}=+1}$ y ${\text{d3}=+1}$.

::: figure {#jue-c3-cmp-num-arbol title="El árbol T±, otra vez"}
![El árbol T±: la forma del árbol T, con 15 nodos porque D tiene 3 hijos y no 2. La raíz R es de MAX; izq lleva a I, centro a C y der a D, los tres de MIN. I tiene las hojas i1 = +1 y ix = −1; ix es una captura de MIN. C tiene dos hijos de MAX: C1, con c1a = 0 y c1b = −1, y C2, con c2a = +1 y c2b = −1. D tiene las hojas d1 = −1, d2 = +1 y d3 = +1. La EVAL de los nodos internos, en la escala 100·U: I = 60, C = 20, D = 10, C1 = 10, C2 = 50](../_assets/jue-t-pm-arbol.svg)
:::

## 1 · Leer los tres números

**Piensa: minimax dice 0 y expectiminimax dice $1/3$. ¿Cuál tiene razón?**

Los dos. Cada número contesta una pregunta distinta, y la unidad ya les
puso nombre. Son tres.

### El valor V

Minimax y alfa-beta dan $V$: lo que MAX **asegura** si los dos juegan lo
mejor posible. En T±, ${V=0}$ por centro. MIN responde c1, y MAX empata
con c1a. Por izq o por der, MIN gana con ix o con d1.

Expectiminimax también da $V$, pero **de otro juego**: uno donde D es un
dado parejo entre d1, d2 y d3. Nadie elige ahí, así que D vale el promedio:
${(-1+1+1)/3=1/3}$. Con ese dado, MAX juega der y ${V=1/3}$. El promedio
es del azar **del juego**; los jugadores siguen eligiendo lo mejor en cada
nodo suyo.

### El valor con corte

El corte a ${d=1}$ eligió izq con 60. Ese 60 no es una utilidad: es
$\mathrm{EVAL}(\text{I})$, una estimación en la escala ${100\cdot U}$. Debajo
de I está ix, y en realidad izq vale ${-1}$, o ${-100}$ en esa escala.

El valor con corte se vuelve exacto solo cuando todo lo que suma viene de
finales. Con ${d=2}$ da 10; con ${d=3}$ ya llega a todos los finales y da
0, que es ${100\cdot V}$. La quietud con ${d=1}$ elige centro, la jugada
buena, pero con 20: **arregla la jugada, no el valor**.

### El promedio de simulaciones

Monte Carlo plano da $\bar u$, y $\bar u$ se acerca a $\mu$: el promedio si
**todos** juegan al azar, también MAX en C1 y C2. En T±,
${\mu(\text{izq})=0}$, ${\mu(\text{centro})=-1/4}$ y
${\mu(\text{der})=1/3}$. Con muchas simulaciones elige der. Pero
${V(\text{der})=-1}$: un MIN racional juega d1.

Con UCT, la política cambia: dentro del árbol ya no se elige al azar sino
por puntaje. Su $\bar u$ mezcla partidas de las dos clases. En la corrida
de la página anterior, a las 40 vueltas centro tiene ${N=26}$ y
${\bar u=0}$. Coincide con ${V=0}$ **por casualidad**: a la vuelta 100 es
${1/83}$.

::: remark {#jue-c3-cmp-v-no-es-u title="V con dado y ū promedian azares distintos"}
**Qué es cada uno.** $V$ con dado promedia el azar **del juego**: el dado
existe, y los jugadores eligen lo mejor en sus nodos. $\bar u$ promedia el
azar **del algoritmo**: el juego no tiene dado, pero las simulaciones
juegan como si cada jugador tirara uno.

**Qué no es:** $\bar u$ no es $V$, ni con muchas simulaciones. Su límite
$\mu$ supone jugadores al azar. En der, los dos dan $1/3$ por la misma
cuenta. Pero uno es el valor de un juego con dado, y el otro, el de un MIN
que juega al azar en un juego sin dado, donde ${V(\text{der})=-1}$.
:::

::: exercise {#jue-c3-cmp-ej-rival-al-azar title="Calcula con solo el rival al azar"}
Un error común al leer $\mu$: creer que solo el **rival** juega al azar.
Supón que en T± MIN elige al azar en I, C y D, y MAX sigue eligiendo lo
mejor en C1 y C2.

1. ¿Cuánto vale centro así?
2. ¿Qué jugada elegiría MAX en la raíz? ¿Coincide con lo que elige Monte
   Carlo plano con muchas simulaciones?
:::

::: hint {#jue-c3-cmp-pista-rival-al-azar-1 of="jue-c3-cmp-ej-rival-al-azar" title="Pista 1 · De abajo hacia arriba"}
¿Cuánto vale C1 si MAX elige ahí? ¿Y C2? ¿Qué hace luego MIN en C, si tira
un volado entre los dos?
:::

::: answer {#jue-c3-cmp-resp-rival-al-azar of="jue-c3-cmp-ej-rival-al-azar"}
1. **Centro vale $1/2$.** MAX elige c1a en C1, que vale 0, y c2a en C2,
   que vale ${+1}$. El volado de MIN en C da ${(0+1)/2=1/2}$.
2. **Centro**, porque izq vale 0 y der ${1/3}$. Monte Carlo plano elige
   der: también MAX juega al azar en C1 y C2, y por eso centro baja a
   ${-1/4}$. El límite de $\bar u$ es «todos al azar», no «el rival al
   azar».
:::

Tres números, tres preguntas. Falta ponerlos junto a la forma en que cada
algoritmo busca, porque de ahí sale qué número puede dar.

## 2 · Poner los algoritmos lado a lado

**Piensa: ¿qué tiene que hacer un algoritmo para que su número sea $V$?**

Llegar a los finales, o probar que lo que no mira no cambia nada, y no
tirar dados. La primera tabla dice cómo busca cada uno. Repite filas de
las fichas de cada página, ahora juntas.

::: table {#jue-c3-cmp-como-busca title="Cómo busca cada algoritmo"}
| Algoritmo | Hasta dónde mira | ¿Genera todo? | ¿Quién tira dados? |
|---|---|---|---|
| Minimax | Los finales | Sí | Nadie |
| Expectiminimax | Los finales | Sí | El juego |
| Alfa-beta | Los finales, sin las ramas que ya no deciden | No | Nadie |
| Minimax con corte | $d$ jugadas | Solo arriba del corte | Nadie |
| Búsqueda de quietud | $d$ jugadas, luego solo capturas | No | Nadie |
| Profundización iterativa | $d=1,2,3,\dots$ mientras haya reloj | No | Nadie |
| Monte Carlo plano | Los finales, jugando al azar; sin árbol | Solo lo que simula | El algoritmo |
| MCTS con UCT | Un árbol que crece; debajo, partidas al azar | No | El algoritmo, al simular |
:::

La segunda dice qué número sale de esa búsqueda, si es $V$, y qué
entrega el algoritmo al final.

::: table {#jue-c3-cmp-que-numero title="Qué número da cada algoritmo"}
| Algoritmo | Número | ¿Es V? | Qué entrega |
|---|---|---|---|
| Minimax | $V$ | Sí | Una jugada de mayor $V$ |
| Expectiminimax | $V$ con dado | Sí, el del juego con dado | Una jugada de mayor utilidad esperada |
| Alfa-beta | $V$ en la raíz; abajo, valor o cota | Sí, en la raíz | Lo mismo que minimax |
| Minimax con corte | Valor con corte | No, salvo si viene de finales | Una jugada de mayor valor con corte |
| Búsqueda de quietud | Valor con corte, en posiciones quietas | No | Una jugada de mayor valor con corte |
| Profundización iterativa | Valor con corte de la última búsqueda completa | No | La jugada de esa búsqueda |
| Monte Carlo plano | $\bar u$, que se acerca a $\mu$ | No | La jugada de mayor $\bar u$ |
| MCTS con UCT | $\bar u$ de cada nodo | No | La jugada más simulada |
:::

Las dos tablas se leen juntas. Donde la primera mira hasta los finales y
el algoritmo no tira dados, la segunda dice $V$. Un $d$ trae
$\mathrm{EVAL}$, y un dado del algoritmo trae $\bar u$.

::: exercise {#jue-c3-cmp-ej-ponle-nombre title="Ponle nombre a cada número"}
Cinco números que salieron de T±. Para cada uno, di cuál de los tres es
($V$, valor con corte o $\bar u$) y si es el $V$ del juego sin dado.

1. 0, de alfa-beta con los hijos al revés.
2. 60, del corte a ${d=1}$.
3. 0, de la profundización iterativa con ${d=1,2,3}$.
4. $1/3$, de expectiminimax con D como dado.
5. 0, el $\bar u$ de centro tras 40 vueltas de UCT.
:::

::: hint {#jue-c3-cmp-pista-ponle-nombre-1 of="jue-c3-cmp-ej-ponle-nombre" title="Pista 1 · Las dos columnas de en medio"}
En la tabla de cómo busca, ¿hasta dónde miró cada uno y quién tiró
dados? ¿En qué escala está su número?
:::

::: answer {#jue-c3-cmp-resp-ponle-nombre of="jue-c3-cmp-ej-ponle-nombre"}
1. **$V$, y sí es el del juego.** Alfa-beta da en la raíz el mismo $V$
   que minimax, en cualquier orden.
2. **Valor con corte; no.** Es $\mathrm{EVAL}(\text{I})$ en la escala
   ${100\cdot U}$; izq vale ${-1}$.
3. **Valor con corte; sí, esta vez.** Con ${d=3}$ todo lo que suma viene
   de finales: ${0=100\cdot V}$.
4. **$V$, pero de otro juego**: el que tiene un dado en D. Sin dado,
   ${V=0}$.
5. **$\bar u$; no.** Coincide con $V$ por casualidad: a la vuelta 100 ya
   es ${1/83}$.
:::

El 0 de la iterativa fue exacto porque vino de finales. Un número así
sirve para algo más que valorar: puede decir que ya no hace falta buscar.

## 3 · Cuándo dejar de buscar

**Piensa: la profundización iterativa sale en cuanto un hijo de la raíz
devuelve 100. ¿Por qué no se pierde nada?**

En [[jugar-contra-el-reloj|Jugar contra el reloj]] lo hace la línea 9 de
PROFUNDIZACIÓN-ITERATIVA:

```text
 9       if w = 100: return a  # gana seguro
```

Ningún final paga más que ${100\cdot U=100}$. Si una jugada ya lo
asegura, ninguna otra puede superarla. Es una regla general: **quien mueve
deja de buscar cuando ya tiene lo más que puede pagarle el juego**. Para
MAX es ${+1}$; para MIN, que busca lo más bajo, es ${-1}$.

La regla pide dos condiciones.

- **Utilidad acotada.** Tiene que existir un máximo conocido. En T±, $U$
  vale ${-1}$, 0 o ${+1}$.
- **Que el número sea un final, o venga de finales.** Una estimación no
  sirve: en T± la $\mathrm{EVAL}$ más alta es 60, y en la posición de la
  clase nunca pasa de 36. Un promedio tampoco. En
  [[de-donde-sale-el-bono|De dónde sale el bono]], x tenía ${\bar u=-1}$
  tras una simulación, y su $\mu$ era 0.6.

En T± con el orden dado, alfa-beta ya se ahorra c2b, d2 y d3. Ahí lo hace
la ventana: C2 ve ${\text{c2a}=+1}$ cuando C ya asegura 0, y D ve
${\text{d1}=-1}$ cuando la raíz ya asegura 0. La regla llega a lo mismo
sin mirar la ventana: ${+1}$ es lo más para MAX, ${-1}$ lo más para MIN.

La diferencia se ve en I. Con los hijos al revés, alfa-beta poda i1 y
genera 14 nodos. Pero lo poda porque la raíz ya asegura 0. Con el orden
dado, I es el primer hijo de la raíz y llega con la ventana abierta. Si ix
fuera su primera hoja, alfa-beta generaría i1 igual. La regla no: **en I,
MIN ve ${\text{ix}=-1}$ y ya no necesita mirar i1**.

Esta regla supone **suma cero**: lo mejor para MIN es lo peor para MAX.
La página siguiente lo pone en duda.

::: exercise {#jue-c3-cmp-ej-puede-salir title="Señala dónde se puede dejar de buscar"}
En cada caso, ¿puede quien mueve dejar de mirar sus otras jugadas? Di por
qué.

1. MCTS: en la raíz, una jugada lleva 3 simulaciones, todas ganadas, y
   ${\bar u=+1}$.
2. Minimax con corte: un hijo de la raíz devuelve 36, la
   $\mathrm{EVAL}$ más alta de la posición de la clase.
3. Alfa-beta sin corte: un hijo de la raíz devuelve ${+1}$.
4. T± con D como dado: en D sale primero ${\text{d1}=-1}$.
:::

::: hint {#jue-c3-cmp-pista-puede-salir-1 of="jue-c3-cmp-ej-puede-salir" title="Pista 1 · Dos preguntas por caso"}
¿El número es lo más que puede pagar el juego a quien mueve? ¿Salió de
finales, o es una estimación o un promedio? Y en el caso 4: ¿quién mueve
en D?
:::

::: answer {#jue-c3-cmp-resp-puede-salir of="jue-c3-cmp-ej-puede-salir"}
1. **No.** Es un promedio de 3 partidas al azar: no demuestra nada. Así
   se atoraba x con una sola simulación.
2. **No.** 36 es una estimación, y está debajo de 100: otra jugada puede
   llevar a un final ganado.
3. **Sí.** Alfa-beta sin corte da valores de finales, y ${+1}$ es lo más
   que paga el juego.
4. **No.** En D no mueve nadie: decide el dado. Su valor es el promedio
   de las tres hojas, y hacen falta todas.
:::

**Punto de control:** deberías poder decir, de un número que devuelve un
algoritmo, si es $V$, un valor con corte o un $\bar u$, y si con él se
puede dejar de buscar.

## Lo que hay que llevarse

- **Tres números, tres preguntas.** $V$ supone a los dos jugando lo mejor;
  en T±, ${V=0}$ por centro. Con un dado en D es otro juego, y ${V=1/3}$
  por der.
- **El valor con corte estima.** El corte a ${d=1}$ da 60 por izq, que
  vale ${-1}$. Con ${d=3}$ llega a los finales y da 0. La quietud elige
  centro con 20: arregla la jugada, no el valor.
- **$\bar u$ supone a todos al azar.** Su límite en der es ${1/3}$, y
  ${V(\text{der})=-1}$. El ${\bar u=0}$ de UCT en centro coincide con $V$
  por casualidad.
- **Qué número da depende de cómo busca.** Hasta los finales y sin dados
  del algoritmo, $V$; con $d$, $\mathrm{EVAL}$; con simulaciones, $\bar u$.
- **Se deja de buscar con lo máximo posible**, si la utilidad es acotada y
  el número salió de finales. La línea 9 de la iterativa sale con 100; en
  I, ix basta. Un ${\bar u=-1}$ no basta: x valía 0.6.

Todo esto supone cosas del juego. ¿Cuáles, y qué uso en cada caso?

Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]].
