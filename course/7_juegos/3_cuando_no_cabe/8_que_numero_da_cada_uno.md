---
id: que-numero-da-cada-uno
title: Qué número da cada uno
nav_title: Qué número da cada uno
summary: "Minimax da V, el corte da un valor con corte y las simulaciones dan ū: tres números que no miden lo mismo. Cómo leer cada uno en T±, qué supone cada uno sobre los jugadores, y cuándo un número permite dejar de buscar."
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
- qué **supone** cada número, y por qué eso decide si un algoritmo
  **garantiza** $V$;
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

El valor con corte se garantiza exacto cuando todo lo que suma viene de
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
juegan como si cada jugador tirara uno. En MCTS, solo debajo del árbol.

**Qué no es:** el $\bar u$ de Monte Carlo plano no es $V$, ni con muchas
simulaciones. Su límite $\mu$ supone jugadores al azar. El de MCTS, que
dentro del árbol elige por puntaje, tiende a $V$ conforme crecen las
vueltas.

En der, $V$ con dado y el $\mu$ de Monte Carlo plano dan $1/3$ por la
misma cuenta. Pero uno es el valor de un juego con dado, y el otro, el de un MIN
que juega al azar en un juego sin dado, donde ${V(\text{der})=-1}$.
:::

::: exercise {#jue-c3-cmp-ej-cambia-hoja title="Cambia una hoja y mira quién se mueve"}
En T±, cambia una sola hoja: ahora ${\text{d2}=-1}$, y las demás quedan
igual.

1. ¿Cambia $V$? ¿Por qué jugada?
2. Con D como dado, ¿cuánto vale D, y qué juega MAX? Sale lo mismo que en
   @jue-c3-cmp-ej-dado, donde cambiabas d3. ¿Por qué, si cambiaste otra
   hoja?
3. ¿Qué elige Monte Carlo plano con muchas simulaciones? ¿Cuánto vale esa
   jugada para un MIN racional?
:::

::: hint {#jue-c3-cmp-pista-cambia-hoja of="jue-c3-cmp-ej-cambia-hoja" title="Una pregunta por número"}
¿Qué hoja elegía MIN en D antes del cambio? Para el dado, cuenta las
hojas de D en ${-1}$, aquí y con d3 cambiada. Para Monte Carlo plano,
compara los tres $\mu$: ¿cuáles no tocan D?
:::

::: answer {#jue-c3-cmp-resp-cambia-hoja of="jue-c3-cmp-ej-cambia-hoja"}
1. **No: ${V=0}$ por centro.** MIN ya respondía d1 en D, así que der
   seguía valiendo ${-1}$.
2. **Porque un promedio no mira cuál hoja es cuál.** Con d2 o con d3 en
   ${-1}$, D tiene dos hojas en ${-1}$ y una en ${+1}$: vale
   ${(-1-1+1)/3=-1/3}$. Ahora der queda debajo del 0 de centro, y MAX
   juega centro con ${V=0}$. Coincide con el $V$ sin dado porque MAX vuelve
   a centro, donde no hay dado.
3. **Izq.** Su ${\mu=0}$ no cambia, centro sigue en ${-1/4}$ y der baja a
   ${-1/3}$. Pero izq vale ${-1}$: MIN responde ix. Monte Carlo plano
   cambió de jugada y sigue eligiendo una que pierde.
:::

Tres números, tres preguntas. Falta ponerlos junto a la forma en que cada
algoritmo busca, porque de ahí sale qué número puede dar.

## 2 · Poner los algoritmos lado a lado

**Piensa: ¿qué tiene que hacer un algoritmo para que su número sea $V$?**

Llegar a los finales, o probar que lo que no mira no cambia nada, y no
cambiar las decisiones de los jugadores por jugadas al azar. Hasta dónde
mira cada algoritmo, quién tira dados y qué
entrega ya están en su ficha:

- [[minimax-como-algoritmo|Minimax como algoritmo]];
- [[cuando-decide-un-dado|Cuando decide un dado]], para expectiminimax;
- [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]];
- [[minimax-con-corte|Minimax con corte como algoritmo]];
- [[mas-alla-del-horizonte|Más allá del horizonte]], para la quietud;
- [[jugar-contra-el-reloj|Jugar contra el reloj]], para la iterativa;
- [[simular-en-vez-de-evaluar|Simular en vez de evaluar]], para Monte
  Carlo plano y MCTS.

Y si cada uno **garantiza** $V$ está en la @jue-c3-cmp-garantiza, de
[[un-arbol-todos-los-algoritmos|Un árbol, todos los algoritmos]]. Lo que
ninguna de esas tablas junta es qué supone cada número sobre los jugadores.

$V$ lo dan minimax, expectiminimax y alfa-beta. El valor con corte lo
dan el corte, la quietud y la iterativa. Y $\bar u$, Monte Carlo plano y
MCTS. La quietud da una variante del valor con corte: el valor con
quietud.

::: table {#jue-c3-cmp-num-supone title="Qué supone cada número"}
| Número | Supone que |
|---|---|
| $V$ | Todos eligen lo mejor |
| Valor con corte | $\mathrm{EVAL}$ acierta en el corte |
| $\bar u$ | Se juega al azar (en MCTS, solo debajo del árbol) |
:::

Un matiz en la fila de $V$: en expectiminimax, el dado del juego no
elige, se promedia.

Por eso garantiza $V$ quien supone que todos eligen lo mejor y llega a los
finales, o prueba que lo que no mira no cambia nada. Un corte trae $\mathrm{EVAL}$, y un dado del algoritmo trae
$\bar u$.

::: exercise {#jue-c3-cmp-ej-ponle-nombre title="Ponle nombre a cada número"}
Cinco números que salieron de T±. Para cada uno, di cuál de los tres es:
$V$, valor con corte o $\bar u$, y si es el $V$ del juego sin dado.

1. 0, de alfa-beta con los hijos al revés.
2. 60, del corte a ${d=1}$.
3. 0, de la profundización iterativa con ${d=1,2,3}$.
4. $1/3$, de expectiminimax con D como dado.
5. 0, el $\bar u$ de centro tras 40 vueltas de UCT.
:::

::: hint {#jue-c3-cmp-pista-ponle-nombre-1 of="jue-c3-cmp-ej-ponle-nombre" title="Qué algoritmo lo dio"}
¿Qué número da ese algoritmo, según la tabla de qué supone cada número?
¿Llegó a los finales esa vez? ¿En qué escala está su número?
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
PROFUNDIZACIÓN-ITERATIVA, `if w = 100: return a`.

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
sin llevar la ventana: ${+1}$ es lo más para MAX, ${-1}$ lo más para MIN.

Pero la regla poda algo que alfa-beta, tal como la escribimos, no poda.
Se ve en I. Supón que ix fuera la primera hoja de I. I es el primer hijo
de la raíz, así que llega con la ventana inicial, ${(-\infty,+\infty)}$.
Con esa ventana, alfa-beta generaría i1 igual. La regla no: **en I, MIN ve
${\text{ix}=-1}$ y ya no necesita mirar i1**.

Abrir la ventana en los límites de $U$, ${(-1,+1)}$, incluye la regla:
con esa ventana, alfa-beta hace esta misma poda, y además poda por las
cotas que hereda. Por eso la regla pide utilidad acotada: sin un máximo
conocido, no hay límites donde abrir la ventana.

Eso cubre la regla dentro de la búsqueda. En la raíz falta una salida:
cuando $\alpha$ llega a ${+1}$, se deja de buscar. Si no, se siguen
buscando hijos con la ventana cerrada, ${(+1,+1)}$, sin nada que ganar.

Una trampa al abrirla ahí. La raíz cambia de jugada solo si un hijo
devuelve **más** que $\alpha$. Si $\alpha$ empieza en ${-1}$ y todas las
jugadas pierden, ninguna lo supera, y la raíz se queda sin jugada. Por eso
`mejor_jugada` empieza con la primera jugada, no con ninguna.

Para MIN, la regla lee su tope en el número de MAX, y eso supone **suma
cero**: lo mejor para MIN es lo peor para MAX. Si no lo es, MIN tiene que
seguir mirando; la página siguiente dice por qué.

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

::: hint {#jue-c3-cmp-pista-puede-salir-1 of="jue-c3-cmp-ej-puede-salir" title="Dos preguntas por caso"}
¿El número es lo más que puede pagar el juego a quien mueve? ¿Salió de
finales, o es una estimación o un promedio? Y en el caso 4: ¿quién mueve
en D?
:::

::: answer {#jue-c3-cmp-resp-puede-salir of="jue-c3-cmp-ej-puede-salir"}
1. **No.** Es un promedio de 3 partidas al azar: no demuestra nada. Así
   se atoraba x con una sola simulación.
2. **No.** 36 es una estimación, y está debajo de 100: otra jugada puede
   llevar a un final ganado.
3. **Sí.** Si ${+1}$ supera a $\alpha$, ese hijo no cortó: si hubiera
   cortado, devolvería algo ${\le\alpha}$. Entonces ${+1}$ es su valor,
   sale de finales y es lo más que paga el juego. Si $\alpha$ ya era
   ${+1}$, este ${+1}$ puede ser solo una cota. Pero entonces una jugada
   anterior ya ganaba, y desde ella se podía dejar de buscar.
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
- **El $\bar u$ de Monte Carlo plano supone a todos al azar.** Su límite
  en der es ${1/3}$, y ${V(\text{der})=-1}$. UCT elige por puntaje dentro
  del árbol y al azar solo debajo; su ${\bar u=0}$ en centro coincide con
  $V$ por casualidad.
- **Qué número da depende de cómo busca.** Hasta los finales y sin dados
  del algoritmo, $V$; con $d$, $\mathrm{EVAL}$; con simulaciones, $\bar u$.
- **Se deja de buscar con lo máximo posible**, si la utilidad es acotada,
  el número salió de finales y, para que MIN pare con un ${-1}$, el juego es
  de suma cero. La línea 9 de la iterativa sale con 100; en
  I, ix basta. Un ${\bar u=-1}$ no basta: x valía 0.6.

Todo esto supone cosas del juego. ¿Cuáles, y qué uso en cada caso?

Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]].
