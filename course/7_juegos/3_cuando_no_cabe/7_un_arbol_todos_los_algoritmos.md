---
id: un-arbol-todos-los-algoritmos
title: Un árbol, todos los algoritmos
nav_title: Un árbol, todos los algoritmos
summary: "Todos los algoritmos de la unidad corridos sobre el mismo árbol, T±: qué jugada entrega cada uno, con qué valor y cuántos nodos genera. Los exactos coinciden, el dado cambia la jugada, el corte se deja engañar, Monte Carlo plano elige mal y UCT lo corrige."
status: ready
estimated_time: 25m
tags: [juegos, busqueda-adversarial, comparacion]
---

# Un árbol, todos los algoritmos

**¿Qué hace distinto cada algoritmo con el mismo árbol?**

Al terminar tendrás:

- el árbol **T±**, una variante de T con finales que dicen quién gana, y
  por qué tiene la forma que tiene;
- la jugada, el valor y los nodos de cada algoritmo de la unidad en ese
  árbol, juntos en una tabla;
- el punto donde se separa cada uno: el orden en alfa-beta, el dado en la
  jugada, el horizonte en el corte;
- por qué Monte Carlo plano elige der, que pierde, y cómo UCT vuelve a
  centro.

> [!TIP]
> **Míralo correr: el mismo árbol, todos los algoritmos**
>
> - **▶ [El mismo árbol, todos los algoritmos](../_assets/un_arbol_todos.html)**:
>   elige un algoritmo y mira qué nodos genera, qué jugada entrega y con
>   qué valor. Las corridas al azar ya vienen hechas, con las semillas de
>   esta página.

> **Lo que traes.** El árbol T de [[minimax-como-algoritmo|Minimax como algoritmo]]:
> R, donde mueve MAX, con izq, centro y der hacia I, C y D. El corte a $d$
> jugadas con $\mathrm{EVAL}$, de [[minimax-con-corte|Minimax con corte]].
> La búsqueda de quietud (@jue-c3-quietud), que sigue solo las capturas. La
> profundización iterativa, de [[jugar-contra-el-reloj|Jugar contra el reloj]].
> Monte Carlo plano y MCTS con UCT, de [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].

## 1 · Armar el árbol T±

**Piensa: T ya corrió minimax, el dado, alfa-beta, el corte y la
iterativa. ¿Por qué no sirve para todos?**

Sus hojas van de 2 a 12. Son finales, y una simulación podría
promediarlas, pero no dicen si MAX ganó, empató o perdió. Sin eso no se
ve la regla de dejar de buscar al tener lo más que paga el juego, ni se
cuentan victorias. Ninguna jugada de T es una captura: la quietud no
tendría nada que mirar.

En T, el corte a ${d=1}$ y el límite de Monte Carlo plano (con
simulaciones sin fin) eligen der, la misma jugada equivocada; con los
dados de la clase 2, der es la óptima. Este ejemplo nuevo entra porque **el hilo no muestra la idea**: hace falta un
árbol donde se separen los algoritmos.

**T±** parte de T: conserva sus nodos internos y las jugadas de la raíz,
y cambia estos datos y una rama:

- **Finales en $U$.** Cada hoja vale ${+1}$ si gana MAX, ${-1}$ si gana MIN
  y $0$ si es empate. Hay un solo empate, c1a.
- **Una captura.** ix, la segunda jugada de MIN en I, captura: la x es la
  de $\text{d2}\textbf{x}\text{c3}$.
- **Una $\mathrm{EVAL}$.** Los nodos internos llevan una estimación en la
  escala ${100\cdot U}$: I 60, C 20, D 10, C1 10 y C2 50. I parece ir
  ganando porque la estimación no ve la captura.
- **D con tres hijos**, d1, d2 y d3; en T tenía dos. Con dos, el promedio
  de un ${-1}$ y otro final es $0$ o menos: un dado en D nunca supera a
  centro. Con tres, ${(-1+1+1)/3=1/3}$.

::: figure {#jue-c3-cmp-arbol title="El árbol T±: la forma de T, con finales en U"}
![El árbol T±: la forma del árbol T, con 15 nodos porque D tiene 3 hijos y no 2. La raíz R es de MAX; izq lleva a I, centro a C y der a D, los tres de MIN. I tiene las hojas i1 = +1 y ix = −1; ix es una captura de MIN. C tiene dos hijos de MAX: C1, con c1a = 0 y c1b = −1, y C2, con c2a = +1 y c2b = −1. D tiene las hojas d1 = −1, d2 = +1 y d3 = +1. La EVAL de los nodos internos, en la escala 100·U: I = 60, C = 20, D = 10, C1 = 10, C2 = 50](../_assets/jue-t-pm-arbol.svg)
:::

El árbol está listo. Antes de ver dónde se equivocan los demás, hace falta
saber cuál es la jugada buena.

## 2 · Los exactos: minimax y alfa-beta

**Piensa: ¿qué asegura MAX con cada jugada, si MIN responde lo mejor?**

Lo contesta **minimax**, que mira todo. I vale ${-1}$: MIN captura con ix.
D vale ${-1}$: MIN juega d1. C vale $0$: si MIN manda a C2, MAX gana con
c2a; así que MIN manda a C1, donde lo mejor de MAX es el empate c1a.
Minimax juega **centro**, con ${V=0}$, y genera los 15 nodos.

**Alfa-beta** da la misma jugada y el mismo $0$ con menos nodos. Cuántos
menos depende del orden:

- **En el orden dado**, 12. Poda c2b: tras c2a, C2 ya vale ${+1}$ o más, y
  MIN tiene C1 con $0$. Poda d2 y d3: tras d1, D ya vale ${-1}$ o menos,
  peor que centro.
- **Con todos los hijos al revés**, 14. Solo poda i1: ix llega primero, y
  con ${-1}$ ya basta.

El orden no cambia la respuesta; cambia el trabajo.

::: exercise {#jue-c3-cmp-ej-poda title="Explica una poda"}
En el orden dado, alfa-beta llega a C2 tras resolver C1.

1. ¿Cuánto vale C1, y qué cota le deja a C?
2. ¿Por qué basta ver c2a para no generar c2b?
:::

::: hint {#jue-c3-cmp-pista-poda-1 of="jue-c3-cmp-ej-poda" title="Quién elige en C"}
En C elige MIN. ¿Qué le importa de C2, si ya tiene C1 en la mano?
:::

::: answer {#jue-c3-cmp-resp-poda of="jue-c3-cmp-ej-poda"}
1. C1 vale $0$, el empate c1a: es de MAX, y $0$ supera a ${-1}$. Entonces C
   vale **a lo más** $0$: MIN puede elegir C1.
2. Tras c2a, C2 vale **al menos** ${+1}$, porque ahí elige MAX. MIN nunca
   lo prefiere a C1. Valga lo que valga c2b, C sigue en $0$.
:::

Los dos exactos coinciden porque resuelven el mismo juego. ¿Qué pasa si el
juego es otro?

## 3 · Con dado: cambia la jugada

**Piensa: si en D tira un dado parejo de tres caras en vez de elegir MIN,
¿sigue conviniendo centro?**

No. Con el dado, D vale el promedio de sus hojas,
${(-1+1+1)/3=1/3}$. Es más que el $0$ de centro y que el ${-1}$ de I.
**Expectiminimax** juega **der**, con valor ${1/3}$, y genera los 15
nodos.

El ${1/3}$ es exacto, pero **para otro juego**: uno donde en D decide el
dado. No corrige a minimax. En T±, en D decide MIN, y der vale ${-1}$.
Por eso D tiene tres hijos: con dos, el dado nunca cambiaba la jugada.

::: exercise {#jue-c3-cmp-ej-dado title="Calcula el dado con otra hoja"}
Cambia d3 de ${+1}$ a ${-1}$, con el dado parejo en D.

1. ¿Cuánto vale D?
2. ¿Qué jugada entrega expectiminimax?
:::

::: hint {#jue-c3-cmp-pista-dado-1 of="jue-c3-cmp-ej-dado" title="Cuántas caras pierden"}
¿Cuántas de las tres caras dan ${-1}$ ahora, y cuántas ${+1}$?
:::

::: answer {#jue-c3-cmp-resp-dado of="jue-c3-cmp-ej-dado"}
1. D vale ${(-1+1-1)/3=-1/3}$.
2. **Centro**, con $0$: ${-1/3}$ ya no supera a centro. El dado solo cambia
   la jugada si el promedio de D le gana a lo que MAX asegura en otra
   rama.
:::

El dado cambia el juego. Los que siguen juegan el mismo T±, pero no
alcanzan a mirar hasta los finales. ¿Qué ven en su lugar?

## 4 · Con corte: el horizonte engaña

**Piensa: con ${d=1}$, ¿qué sabe la raíz de cada jugada?**

Solo la $\mathrm{EVAL}$ de I, C y D: 60, 20 y 10. **El corte a ${d=1}$
juega izq**, con 60, y genera 4 nodos. Es el efecto horizonte
(@jue-c3-efecto-horizonte): la captura ix queda detrás del corte, e I vale
de verdad ${-100}$ en esta escala.

El corte no poda: genera todo hasta $d$. Con más profundidad, el engaño
desaparece:

- **${d=2}$** ya ve los finales de I y D, los dos en ${-100}$. En C corta
  en C1 y C2, con 10 y 50. Juega **centro**, con 10, y genera 11 nodos.
- **${d=3}$** llega a todos los finales. Juega centro, con $0$: el valor de
  minimax por 100, con los mismos 15 nodos.

### La quietud arregla la jugada

Con ${d=1}$ y **búsqueda de quietud**, I no es una posición quieta: MIN
tiene la captura ix. MIN elige entre quedarse con 60 o capturar, que da
${-100}$, y captura. C y D no tienen capturas: se quedan en 20 y 10.

La quietud juega **centro**, con 20, y genera 5 nodos: los 4 del corte más
ix. **Arregla la jugada, pero no el valor**: 20 no es el $0$ de minimax. El
20 es la $\mathrm{EVAL}$ de C, que es quieta.

::: exercise {#jue-c3-cmp-ej-quietud title="Señala lo que la quietud no mira"}
La quietud a ${d=1}$ da 20 en C, y el valor de minimax de C es $0$.

1. ¿Por qué la quietud no sigue ninguna jugada bajo C?
2. ¿Qué elección de MIN tendría que mirar para llegar a $0$?
:::

::: hint {#jue-c3-cmp-pista-quietud-1 of="jue-c3-cmp-ej-quietud" title="Qué jugadas sigue"}
En un nodo de corte, ¿qué clase de jugadas sigue la quietud? ¿Hay alguna
bajo C?
:::

::: answer {#jue-c3-cmp-resp-quietud of="jue-c3-cmp-ej-quietud"}
1. Solo sigue capturas, y ni c1 ni c2 lo son: C es quieta y se evalúa ahí.
2. La de C1 contra C2. El error de C no es un intercambio a medias: es que
   MIN puede mandar a C1, donde MAX solo empata. Eso solo lo ve buscar
   más hondo, como ${d=3}$.
:::

### La iterativa entrega algo en cada vuelta

La **profundización iterativa** corre ${d=1}$, 2 y 3, cada una con alfa-beta
y la jugada anterior primero. Cada búsqueda deja una jugada lista:

- **${d=1}$:** izq, con 4 nodos. Si el reloj se acaba aquí, entrega la del
  horizonte.
- **${d=2}$:** centro, con 9, y no 11 como el corte solo: alfa-beta poda.
- **${d=3}$:** centro, con 12, porque prueba centro primero y poda.

Son 25 nodos en total, más que los 15 de minimax. En un árbol tan chico,
repetir cuesta más que mirar todo una vez. Lo que se compra es tener
siempre una jugada.

::: exercise {#jue-c3-cmp-ej-reloj title="Calcula lo que entrega el reloj"}
El reloj alcanza para las dos primeras búsquedas de la iterativa en T±, y
no para la tercera.

1. ¿Qué jugada entrega, y con qué valor?
2. ¿Cuántos nodos generó en total?
:::

::: hint {#jue-c3-cmp-pista-reloj-1 of="jue-c3-cmp-ej-reloj" title="Qué búsqueda manda"}
¿Cuál de las búsquedas terminadas deja la jugada lista? ¿Cuántos nodos
generó cada una?
:::

::: answer {#jue-c3-cmp-resp-reloj of="jue-c3-cmp-ej-reloj"}
1. **Centro, con 10**: la de ${d=2}$, la última búsqueda completa. Es la
   jugada correcta con un valor que todavía no es el de minimax.
2. ${4+9=13}$ nodos.
:::

Todos estos estiman con una $\mathrm{EVAL}$ escrita a mano. ¿Y si no hay
$\mathrm{EVAL}$?

## 5 · Con simulaciones: Monte Carlo plano elige der

**Piensa: si los dos juegan al azar, ¿qué jugada promedia más?**

Monte Carlo plano simula desde cada jugada de la raíz y entrega la de
mayor $\bar u$. En T± hay un empate, así que $\bar u$ es el promedio de
$U$ con el empate contando $0$. La fórmula ${2G/N-1}$ ya no sirve: suponía
que cada partida la gana alguien.

Con infinitas simulaciones, cada $\bar u$ llega a su $\mu$
(@jue-c3-mu), el promedio con **todos** al azar, también MAX:

- **izq:** I elige al azar entre ${+1}$ y ${-1}$: ${\mu=0}$.
- **centro:** C1 al azar da ${(0-1)/2=-1/2}$ y C2, ${(1-1)/2=0}$. Con C
  también al azar, ${\mu=-1/4}$.
- **der:** ${\mu=(-1+1+1)/3=1/3}$.

**Monte Carlo plano elige der, que pierde.** Centro queda último porque, al
azar, MAX juega c1b o c2b la mitad de las veces, y pierde. Ojo con la cuenta que
tienta: con solo MIN al azar, C1 y C2 valdrían $0$ y ${+1}$, C valdría
${1/2}$ y ganaría centro. Pero en una simulación nadie elige.

**La corrida de la página.** Con 5 simulaciones por jugada y la semilla 0,
las sumas de $U$ son ${-3}$, ${-2}$ y ${+3}$. Los promedios, ${-3/5}$,
${-2/5}$ y ${3/5}$: entrega der.

¿Fue suerte? Cada fila de la tabla repite Monte Carlo plano con 1000
semillas distintas; cada semilla es una corrida. «Sims» son las
simulaciones por jugada, y las columnas izq, centro y der cuentan cuántas
corridas entregaron cada jugada. Si dos promedios empatan, entrega la
primera en el orden izq, centro, der.

::: table {#jue-c3-cmp-reparto-mc title="Monte Carlo plano en T±: qué entrega en 1000 corridas"}
| Sims | izq | centro | der |
|---:|---:|---:|---:|
| 5 | 353 | 106 | 541 |
| 10 | 269 | 53 | 678 |
| 50 | 39 | 1 | 960 |
:::

Por empate se decidieron 233, 157 y 15 de esas corridas, fila por fila.

Con pocas simulaciones, el ruido y el desempate reparten las corridas. Con
50, casi todas van a der. **Más simulaciones no lo arreglan**: lo vuelven
más seguro de la jugada equivocada.

::: exercise {#jue-c3-cmp-ej-mas-sims title="Predice con un millón de simulaciones"}
Con un millón de simulaciones por jugada, ¿qué entregaría Monte Carlo
plano en T±, en casi todas las corridas? ¿Qué tendría que cambiar para que
entregara centro?
:::

::: hint {#jue-c3-cmp-pista-mas-sims-1 of="jue-c3-cmp-ej-mas-sims" title="A dónde se acerca cada promedio"}
Con muchas simulaciones, ¿a qué número se acerca el $\bar u$ de cada
jugada? ¿Quién elige al azar en ese número?
:::

::: answer {#jue-c3-cmp-resp-mas-sims of="jue-c3-cmp-ej-mas-sims"}
**Der**: cada $\bar u$ se acerca a su $\mu$, y der tiene el mayor,
${1/3}$. El defecto no es el ruido, es el supuesto: los dos juegan al
azar.

Ningún nodo solo basta para entregar centro: tienen que dejar el azar al
menos dos. Si MAX elige en C1 y en C2, centro vale ${1/2}$, más que el
${1/3}$ de der. Si MIN elige en I y en D, izq y der caen a ${-1}$. Que MIN
elija solo en D no alcanza: der cae, pero izq, con $0$, sigue arriba del
${-1/4}$ de centro.
:::

El defecto es el rival al azar, y también el MAX al azar. ¿Qué cambia si,
donde ya hay árbol, los dos eligen?

## 6 · UCT construye el árbol y vuelve a centro

**Piensa: en D, tras unas cuantas vueltas, ¿seguiría MIN eligiendo al azar
con UCT?**

No. Donde ya hay árbol, UCT elige por puntaje, y en un nodo de MIN baja al
hijo de menor $\bar u$, con bono. Si d2 y d3 le dan victorias a MAX,
MIN baja por d1. Lo mismo hace MAX en C1 y C2. T± tiene 15 nodos: pronto el árbol lo
cubre entero, y nadie juega al azar.

**La corrida de la página**, con ${c=1}$ y la semilla 0. Al final de cada
vuelta, la jugada más simulada de la raíz es:

- **izq**, en las vueltas 1 a 3;
- **centro**, de la 4 a la 7;
- **der**, de la 8 a la 17;
- **centro**, desde la 18. En la 18, centro y der empatan 7 a 7, y gana la
  primera en el orden.

Tras 40 vueltas, centro lleva 26 simulaciones, der 9 e izq 5. UCT entrega
**centro**, con ${\bar u=0}$. Ese $0$ coincide con $V$ **por casualidad**:
es el promedio de 26 partidas, no un valor exacto.

¿Fue suerte la semilla 0? Se repitió con 500 semillas, de 200 vueltas cada
una. Cada semilla es una corrida, y de cada una se anota **la vuelta desde
la que centro queda como la más simulada**, sin soltarlo, hasta la 200:

- con ${c=1}$, las 500 terminan en centro. La vuelta va de 4 a 34. La
  mediana es 18, como la semilla 0; el 10 % llega en la 8 o antes, y el
  90 %, en la 31 o antes;
- con ${c=2\sqrt2}$, también llegan todas, más tarde: la mediana es 29.
  Es la $c$ que sale en [[de-donde-sale-el-bono|De dónde sale el bono]]. En
  la escala ${(U+1)/2}$, de 0 a 1 (victorias más medio empate, entre $N$;
  sin empates es ${G/N}$), se escribe ${c=\sqrt2}$: pasar a la escala de
  ${-1}$ a ${+1}$ dobla los puntajes, y con ellos $c$.

Es lo medido en este árbol, no una garantía. Con tiempo sin límite,
cualquier ${c>0}$ termina en la jugada de minimax; cuánto tarda depende
del árbol y de $c$.

::: exercise {#jue-c3-cmp-ej-uct title="Corta la corrida antes"}
En la corrida de la semilla 0, el tiempo se acaba al terminar la vuelta 12.

1. ¿Qué jugada entrega UCT?
2. ¿Por qué no contradice que UCT corrija a Monte Carlo plano?
:::

::: hint {#jue-c3-cmp-pista-uct-1 of="jue-c3-cmp-ej-uct" title="Qué hay en el árbol a esa altura"}
¿Qué entrega UCT cuando se acaba el tiempo? Con 12 vueltas, ¿cuántos de
los 15 nodos pueden estar en el árbol?
:::

::: answer {#jue-c3-cmp-resp-uct of="jue-c3-cmp-ej-uct"}
1. **Der**: es la más simulada de la vuelta 8 a la 17.
2. Cada vuelta agrega **a lo más** un nodo: una vuelta que baja a un
   final que ya está en el árbol no agrega nada. Tras 12 vueltas hay 10 de
   los 15 nodos, contando R. El árbol todavía no cubre T±, y abajo se sigue
   simulando con los dos al azar. UCT corrige **con
   vueltas**: cuantas más, menos azar queda arriba.
:::

## 7 · Ponerlos todos en una tabla

Ya corrió cada uno. La tabla los junta, en el orden del curso.

::: table {#jue-c3-cmp-resultados title="Todos los algoritmos en T±"}
| Algoritmo | Jugada, valor | Nodos |
|---|---|---:|
| Minimax | centro, 0 | 15 |
| Expecti­minimax, dado en D | der, 1/3 | 15 |
| Alfa-beta, orden dado | centro, 0 | 12 |
| Alfa-beta, al revés | centro, 0 | 14 |
| Corte, d=1 | izq, 60 | 4 |
| Corte, d=2 | centro, 10 | 11 |
| Corte, d=3 | centro, 0 | 15 |
| Quietud, d=1 | centro, 20 | 5 |
| Iterativa, d=1, 2, 3 | centro, 0 | 25 |
| Monte Carlo plano | der, 3/5 | 15 |
| UCT | centro, 0 | 15 |
:::

- **Valor:** en la escala de cada uno. Los de corte usan ${100\cdot U}$,
  como $\mathrm{EVAL}$; los demás, la de $U$.
- **Nodos:** no miden el mismo trabajo en todas las filas. En las
  búsquedas, los generados, contando R; la iterativa suma sus tres
  búsquedas, con repeticiones. En Monte Carlo plano, los nodos distintos
  que tocaron sus simulaciones; en UCT, los que quedaron en su árbol. Las
  dos corridas son las de la semilla 0: Monte Carlo plano jugó 15
  simulaciones, 5 por jugada; UCT, 40, una por vuelta con ${c=1}$.

Tres filas no dicen centro, y cada una por una razón distinta: el dado
cambia el juego, el corte a ${d=1}$ no ve la captura y Monte Carlo plano
supone que los dos juegan al azar. Los otros ocho aciertan.

Acertar la jugada no es lo mismo que garantizar el valor. La segunda
tabla dice, de cada algoritmo, si **por cómo funciona** devuelve $V$, el
valor de minimax.

::: table {#jue-c3-cmp-garantiza title="Qué algoritmo garantiza V"}
| Algoritmo | ¿Garantiza V? |
|---|---|
| Minimax | Sí |
| Expecti­minimax | Sí, el V del juego con dado |
| Alfa-beta | Sí, en la raíz |
| Corte | No, salvo si llega a los finales |
| Quietud | No, salvo si llega a los finales antes de cortar |
| Iterativa | No, salvo si llega a los finales |
| Monte Carlo plano | No |
| UCT | No (con tiempo sin límite converge a él, con cualquier c > 0) |
:::

En T±, tres filas que en general no garantizan $V$ dan el $0$ de
minimax. El corte a ${d=3}$ y la iterativa, porque esta vez llegan a los
finales, y entonces sí es $V$. UCT, por casualidad: su $0$ es un promedio.

::: exercise {#jue-c3-cmp-ej-tabla title="Compara dos filas que dicen 0"}
Minimax y UCT entregan centro con valor $0$.

1. ¿Qué es cada uno de esos dos ceros?
2. Si UCT corriera 1000 vueltas más, ¿podría cambiar su $0$? ¿Y el de
   minimax?
:::

::: hint {#jue-c3-cmp-pista-tabla-1 of="jue-c3-cmp-ej-tabla" title="De dónde sale cada número"}
¿Cuál de los dos sale de mirar todos los finales, y cuál de promediar
partidas?
:::

::: answer {#jue-c3-cmp-resp-tabla of="jue-c3-cmp-ej-tabla"}
1. El de minimax es $V$: lo que MAX asegura contra un MIN que juega
   perfecto. El de UCT es $\bar u$: el promedio de las 26 partidas que
   pasaron por centro.
2. El de UCT sí: cada vuelta suma una partida al promedio. El de minimax
   no: ya miró los 15 nodos y no queda nada que cambie.
:::

Cada algoritmo dio un número distinto. ¿Qué es cada número?

**Punto de control:** deberías poder correr a mano cualquiera de los
algoritmos de la unidad en T±. También, decir por qué el corte a ${d=1}$
y Monte Carlo plano se equivocan, y qué los corrige.

## Lo que hay que llevarse

- **T±** es T con finales en $U$: un empate (c1a), una captura (ix), una
  $\mathrm{EVAL}$ (I 60, C 20, D 10) y tres hijos en D. Minimax juega
  centro con ${V=0}$ y 15 nodos.
- **Alfa-beta** da lo mismo con menos: 12 nodos en el orden dado, 14 al
  revés. El orden cambia el trabajo, no la respuesta.
- **Un dado en D cambia el juego**: expectiminimax juega der por ${1/3}$.
- **El corte a ${d=1}$ se engaña**: izq con 60, sin ver ix. La quietud
  juega centro con 5 nodos, pero su 20 no es el $0$. La iterativa deja izq,
  centro y centro, con 4, 9 y 12 nodos: 25.
- **Monte Carlo plano elige der**: con todos al azar, der promedia ${1/3}$,
  izq $0$ y centro ${-1/4}$. Con 50 simulaciones, der en 960 de 1000
  corridas.
- **UCT vuelve a centro**: en la semilla 0, desde la vuelta 18; tras 40,
  con 26 simulaciones. En 500 semillas con ${c=1}$, todas, con mediana 18.

Continúa con [[que-numero-da-cada-uno|Qué número da cada uno]].
