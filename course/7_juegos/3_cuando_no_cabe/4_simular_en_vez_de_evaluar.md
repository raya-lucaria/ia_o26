---
id: simular-en-vez-de-evaluar
title: Simular en vez de evaluar
nav_title: Simular
summary: "La otra respuesta cuando el árbol no cabe: estimar cuánto vale una jugada jugando muchas partidas al azar hasta el final y promediando. Es la búsqueda de árbol Monte Carlo, la base de AlphaGo."
status: ready
estimated_time: 20m
tags: [juegos, busqueda-adversarial, monte-carlo]
---

# Simular en vez de evaluar

**¿Se puede estimar una posición sin escribir una función de evaluación?**

Sí. Al terminar conocerás la **búsqueda de árbol Monte Carlo**, o **MCTS**
(del inglés *Monte Carlo tree search*): su idea, sus cuatro pasos y en qué
se distingue de cortar y evaluar. Es un adelanto: no la calculamos a mano.

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: no se puede llegar a los
> finales con minimax. Pero sí se puede jugar **una** partida hasta el final,
> eligiendo cada jugada al azar: eso es barato.

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $S_F$ (@jue-c1-finales),
> $\mathrm{Pl}(s)$ (@jue-c1-pl), $A(s)$ (@jue-c1-acciones), $T(s,a)$
> (@jue-c1-transicion) y $U(s)$, $+1$ si gana MAX y $-1$ si gana MIN
> (@jue-c1-utilidad).

> **El problema de esta página.**
>
> **Dado:** un estado $s$ donde mueve MAX y las reglas del juego. **Sin**
> función de evaluación.
>
> **Encontrar:** una jugada para $s$, lo mejor posible con el tiempo que
> haya.

## 1 · Jugar al azar y promediar

**Piensa: si no sabes cuánto vale una posición, ¿cómo lo averiguarías sin
escribir ninguna regla sobre el juego?**

Jugando. Desde esa posición, juega muchas partidas eligiendo cada jugada al
azar, hasta el final. Anota la $U$ de cada una y promedia.

::: definition {#jue-c3-simulacion title="Simulación"}
Una **simulación** desde un estado $s$ es una partida que empieza en $s$ y
sigue hasta un final, eligiendo en cada estado una jugada al azar de
$A(s)$. Su resultado es la $U$ del final al que llega.

**Qué significa:** el promedio de muchas simulaciones estima qué tan buena
es $s$ para MAX, en la escala de $U$: entre $-1$ y $+1$.

**Qué no es:** no es el valor $V(s)$. Un rival al azar no es un rival que
piensa: una posición puede ganarse en casi todas las simulaciones y
perderse contra quien encuentra la única respuesta buena.
:::

Por ejemplo, supón que de 10 simulaciones desde $s$ MAX gana 7 y pierde 3.
El promedio es

$$\frac{7\cdot(+1)+3\cdot(-1)}{10}=0.4.$$

## 2 · Simular en la posición de la clase

**Piensa: en la posición de la clase, ¿qué jugada parecería mejor si solo
promediaras partidas al azar?**

Con muchísimas simulaciones, el promedio de cada jugada se acerca a un
número fijo. La computadora puede calcular ese número exacto: el promedio
de $U$ sobre todas las partidas posibles, si los dos jugadores eligen cada
jugada al azar.

::: table {#jue-c3-simulaciones title="Promedio de infinitas simulaciones en la posición de la clase"}
| Jugada | Promedio de las simulaciones | Profundidad 1 | Exacto |
|---|---:|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 0.21 | 2 | $-1$ |
| $\text{d2}\textbf{-}\text{d3}$ | **0.89** | 2 | $+1$ |
| $\text{d2}\textbf{x}\text{c3}$ | 0.15 | **13** | $-1$ |
:::

**Aquí simular acierta.** La jugada con mejor promedio es
$\text{d2}\textbf{-}\text{d3}$, la que gana, y la captura queda última. Sin
que nadie le escriba una evaluación, la simulación «ve» que el peón de más
se pierde: en las partidas al azar, Negras recaptura muchas veces.

**Pero un promedio no es el valor.** En hexapawn, las tres aperturas de
Blancas valen $-1$: Negras gana si juega bien. Sus promedios de simulación
son $7/36$, $5/24$ y $7/36$, los tres **positivos**. Contra un rival que
juega al azar, empezar parece bueno.

::: exercise {#jue-c3-ej-promedio title="Decide qué dice un promedio"}
Con $U=\pm1$, un promedio $\bar u$ y la probabilidad $p$ de que gane MAX
cumplen $p=(\bar u+1)/2$, como en
[[cuando-decide-un-dado|Cuando decide un dado]].

1. ¿Con qué probabilidad gana Blancas las partidas al azar que empiezan con
   $\text{d2}\textbf{-}\text{d3}$, si el promedio es $8/9$?
2. Las de hexapawn que empiezan con $\text{b1}\textbf{-}\text{b2}$ tienen
   promedio $5/24$. ¿Cuántas gana Blancas? ¿Por qué no contradice que
   $\text{b1}\textbf{-}\text{b2}$ valga $-1$?
:::

::: hint {#jue-c3-pista-promedio of="jue-c3-ej-promedio" title="Quién juega en las simulaciones"}
Sustituye en la fórmula. Para el inciso 2, piensa en quién elige las
jugadas de Negras durante una simulación, y en qué supone $V$ sobre Negras.
:::

::: answer {#jue-c3-resp-promedio of="jue-c3-ej-promedio"}
1. $p=(8/9+1)/2=17/18$: Blancas gana 17 de cada 18 partidas al azar.
2. $p=(5/24+1)/2=29/48$: un poco más de 6 de cada 10. No lo contradice:
   en las simulaciones, Negras juega al azar y se equivoca seguido; $V=-1$
   supone que Negras juega perfecto. Es la confusión de rival y azar de
   [[cuando-decide-un-dado|Cuando decide un dado]]. MCTS la corrige con su
   árbol: donde ya construyó nodos, elige con el puntaje en lugar de al
   azar.
:::

## 3 · Qué cambia respecto de la evaluación

**Piensa: ¿qué necesita saber del juego este método, además de las
reglas?**

Nada. Esa es la diferencia con [[cortar-y-evaluar|cortar y evaluar]]:

::: table {#jue-c3-eval-contra-mcts title="Cortar y evaluar contra Monte Carlo"}
| | Cortar y evaluar | Monte Carlo |
|---|---|---|
| Qué necesita, además de las reglas | Una $\mathrm{EVAL}$ escrita a mano | Nada: solo jugar con $A$ y $T$ hasta un final |
| Dónde se detiene | En la profundidad de corte | En los finales, dentro de cada simulación |
| Qué número da | El minimax de $\mathrm{EVAL}$ | Un promedio de $U$ |
| Cómo mejora | Más profundidad o una $\mathrm{EVAL}$ mejor | Más simulaciones |
:::

Por eso sirve en juegos donde nadie sabe escribir una buena evaluación.
El ejemplo clásico es el **Go**.

## 4 · Los cuatro pasos

Simular solo desde la raíz desperdicia tiempo: reparte igual las partidas
entre jugadas buenas y malas. MCTS **construye un árbol poco a poco** y
manda más simulaciones a las jugadas que van mejor.

Cada nodo del árbol guarda dos números: cuántas simulaciones pasaron por
él y cuántas de ellas ganó MAX. Con ellos se calcula su promedio: si de
$n$ simulaciones MAX ganó $w$, el promedio de $U$ es $(2w-n)/n$.

Cada vuelta tiene cuatro pasos:

1. **Selección.** Desde la raíz, baja por el árbol ya construido. En cada
   nodo elige al hijo con mejor puntaje (sección 5), hasta llegar a un
   nodo con alguna jugada que todavía no está en el árbol.
2. **Expansión.** Agrega al árbol un hijo nuevo: $T(s,a)$ para una de esas
   jugadas $a$.
3. **Simulación.** Desde ese hijo, juega una partida al azar hasta un final
   y anota su $U$.
4. **Retropropagación.** Sube por el camino recorrido hasta la raíz. En cada
   nodo, suma 1 a sus simulaciones y suma el resultado a su total.

Si la selección llega a un final, no hay nada que expandir ni simular: su
$U$ es el resultado de la vuelta.

::: figure {#jue-c3-fig-mcts title="Una vuelta de MCTS, en cuatro pasos"}
![Cuatro paneles con el mismo árbol; cada nodo dice victorias de MAX entre simulaciones. Selección: se baja por el camino resaltado, de 4/10 a 3/6, donde mueve MIN, y de ahí a 0/2, el hijo donde MAX ganó menos. Expansión: aparece un hijo nuevo, 0/0. Simulación: desde ese hijo, una línea quebrada llega a un final con U = +1. Retropropagación: los nodos del camino pasan a 5/11, 4/7, 1/3 y 1/1](../_assets/jue-c3-mcts-pasos.svg)
:::

Las vueltas se repiten mientras haya tiempo. Al final se juega la jugada de
la raíz **por la que pasaron más simulaciones**. Como la profundización
iterativa de [[jugar-contra-el-reloj|la página anterior]], siempre tiene una
jugada lista.

## 5 · Explorar o aprovechar

**Piensa: ¿conviene seguir probando la jugada que va mejor, o darle otra
oportunidad a una que casi no se ha probado?**

Las dos cosas. **Aprovechar** es elegir lo que ya funcionó; **explorar** es
probar lo poco probado, por si es mejor. La regla más usada, llamada
**UCT**, le suma a cada promedio un bono que crece si la jugada se ha
probado poco:

$$\text{puntaje}(s')=\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

- $s$ es el nodo donde se elige y $s'$, uno de sus hijos.
- $\bar u(s')$ es el promedio de las simulaciones que pasaron por $s'$,
  visto desde el jugador $\mathrm{Pl}(s)$: si es MIN, se le cambia el signo.
- $N(s)$ y $N(s')$ cuentan las simulaciones que pasaron por cada nodo.
- $\ln$ es el logaritmo natural; aquí solo importa que crece muy despacio.
- $c$ es un número positivo que elegimos: más grande, más exploración.

El primer término aprovecha; el segundo explora. Un hijo que nunca se ha
probado tiene $N(s')=0$ y se prueba antes que los demás. Con muchas
simulaciones el bono se encoge y manda el promedio.

::: exercise {#jue-c3-ej-mcts title="Decide qué jugada entrega MCTS"}
Tras 100 vueltas, las tres jugadas de la raíz, donde mueve MAX, tienen:

| Jugada | Simulaciones | Promedio |
|---|---:|---:|
| x | 60 | 0.5 |
| y | 30 | 0.6 |
| z | 10 | 0.2 |

1. Si el tiempo se acaba ahora, ¿qué jugada se entrega?
2. ¿Cuál de las tres recibe el bono de exploración más grande?
:::

::: hint {#jue-c3-pista-mcts of="jue-c3-ej-mcts" title="Dos reglas distintas"}
Al terminar, la regla es la de la sección 4: la jugada con más
simulaciones. Para el bono, mira qué número va abajo en la raíz cuadrada.
:::

::: answer {#jue-c3-resp-mcts of="jue-c3-ej-mcts"}
1. **x**: es la que tiene más simulaciones, aunque y promedie un poco más.
   Con solo 30 partidas, el 0.6 de y es menos confiable.
2. **z**: el bono tiene $N(s')$ abajo, y z es la menos probada.
:::

## 6 · El ancla: AlphaGo

- **Desde 2006**, cuando Rémi Coulom le dio nombre al método, los programas
  de Go más fuertes usan MCTS.
- **En marzo de 2016, AlphaGo**, de DeepMind, venció 4 a 1 a Lee Sedol, uno
  de los mejores jugadores de Go del mundo. Combinaba MCTS con **redes
  neuronales**: una sugería qué jugadas explorar y otra estimaba cuánto
  valía una posición.
- **AlphaZero, en 2017**, quitó las simulaciones al azar y se quedó con el
  árbol y las redes, que aprende jugando contra sí mismo.

La pregunta es la de toda la unidad: qué hará el rival. Lo que cambia es
cómo se estima lo que no se alcanza a calcular.

**Punto de control:** deberías poder decir los cuatro pasos de MCTS, en qué
se distingue de cortar y evaluar y qué papel tienen los dos términos del
puntaje.

## Lo que hay que llevarse

- MCTS estima una jugada simulando partidas al azar hasta el final y
  promediando su $U$. No necesita $\mathrm{EVAL}$: solo las reglas.
- Cada vuelta tiene cuatro pasos: selección, expansión, simulación y
  retropropagación. Al final se juega la jugada más simulada.
- Un promedio de simulaciones no es $V$: supone un rival que juega al azar.
  En la posición de la clase acierta; en hexapawn, las aperturas perdedoras
  promedian positivo.
- El puntaje equilibra aprovechar lo que va bien y explorar lo poco
  probado.
- AlphaGo (2016) combinó MCTS con redes neuronales y venció a Lee Sedol.

Continúa con [[tarea-cuando-no-cabe|la tarea de refuerzo]].
