---
id: simular-en-vez-de-evaluar
title: Simular en vez de evaluar
nav_title: Simular en vez de evaluar
summary: "La otra respuesta cuando el árbol no cabe: estimar cuánto vale una jugada jugando muchas partidas al azar hasta el final y promediando, que es Monte Carlo plano. La búsqueda de árbol Monte Carlo, la base de AlphaGo, construye además un árbol: dentro de él elige por puntaje, y solo debajo simula al azar."
status: ready
estimated_time: 31m
tags: [juegos, busqueda-adversarial, monte-carlo]
---

# Simular en vez de evaluar

**¿Se puede estimar una posición sin escribir una función de evaluación?**

Al terminar tendrás:

- el **promedio de simulaciones** de una jugada, leído como probabilidad
  de ganar, y por qué no es su valor $V$;
- las cuentas de una **vuelta de MCTS** en sus cuatro pasos, cuando gana
  MAX y cuando pierde;
- el **puntaje UCT** de tres jugadas con ${c=1}$, y por qué la que se explora
  no es la que se entrega;
- el recorrido de la clase en tres programas: Deep Blue, AlphaGo y
  AlphaZero.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N), en la fila 4.
> Empiezan Blancas. Un peón avanza una casilla si está vacía o
> captura en diagonal hacia delante. Gana quien llega a la fila del rival,
> captura todo o deja al rival sin jugada. ${U=+1}$ si gana Blancas y ${U=-1}$
> si gana Negras.

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $S_F$ (@jue-c1-finales),
> $\mathrm{Pl}(s)$ (@jue-c1-pl), $A(s)$ (@jue-c1-acciones), $T(s,a)$
> (@jue-c1-transicion) y $U(s)$, ${+1}$ si gana MAX y ${-1}$ si gana MIN
> (@jue-c1-utilidad).

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: no se puede llegar a los
> finales con minimax. Pero sí se puede jugar **una** partida hasta el final,
> eligiendo cada jugada al azar: eso es barato.

> **El problema de esta página.**
>
> **Dado:** un estado $s$ donde mueve MAX y las reglas del juego. **Sin**
> función de evaluación.
>
> **Encontrar:** una jugada para $s$, lo mejor posible con el tiempo que
> haya.

Esta página es un adelanto de la **búsqueda de árbol Monte Carlo**, o
**MCTS** (del inglés *Monte Carlo tree search*). La ves funcionar en números
pequeños, sin calcularla entera a mano.

## 1 · Jugar al azar y promediar

**Piensa: si no sabes cuánto vale una posición, ¿cómo lo averiguarías sin
escribir ninguna regla sobre el juego?**

Jugando. Desde esa posición, juega muchas partidas eligiendo cada jugada al
azar, hasta el final. Anota la $U$ de cada una y promedia.

Esta idea se llama **Monte Carlo plano**: simula desde cada jugada, sin
construir ningún árbol. Las secciones 1 a 3 son eso. Desde la sección 4,
MCTS lo mejora construyendo un árbol.

::: definition {#jue-c3-simulacion title="Simulación"}
Una **simulación** desde un estado $s$ es una partida que empieza en $s$ y
sigue hasta un final, eligiendo en cada estado una jugada al azar de
$A(s)$. Su resultado es la $U$ del final al que llega.

**Qué significa:** el promedio de muchas simulaciones, $\bar u$, estima qué
tan buena es $s$ para MAX, en la escala de $U$: entre ${-1}$ y ${+1}$.

**Qué no es:** no es el valor $V(s)$. Un rival al azar no es un rival que
piensa. Una posición puede ganarse en casi todas las simulaciones y
perderse contra quien encuentra la única respuesta buena.
:::

Por ejemplo, supón que de 10 simulaciones desde $s$ MAX gana 7 y pierde 3.
El promedio es

$$\bar u=\frac{7\cdot(+1)+3\cdot(-1)}{10}=0.4.$$

::: exercise {#jue-c3-ej-cinco title="Calcula dos promedios"}
Desde un estado se juegan 5 simulaciones.

1. Si MAX gana 3 y pierde 2, ¿cuánto vale $\bar u$?
2. ¿Y si gana 2 y pierde 3?
:::

::: hint {#jue-c3-pista-cinco-1 of="jue-c3-ej-cinco" title="Qué suma cada partida"}
¿Cuánto aporta a la suma una partida ganada, y cuánto una perdida?
:::

::: answer {#jue-c3-resp-cinco of="jue-c3-ej-cinco"}
1. ${\bar u=(3-2)/5=0.2}$.
2. ${\bar u=(2-3)/5=-0.2}$. Una sola partida que cambia de lado mueve el
   promedio $0.4$: con pocas simulaciones, el número todavía brinca mucho.
:::

Un promedio así no pide saber nada del juego. ¿Elige bien en la posición
de la clase?

## 2 · Simular en la posición de la clase

**Piensa: en la posición de la clase, ¿qué jugada parecería mejor si solo
promediaras partidas al azar?**

Con muchísimas simulaciones, el promedio de cada jugada se acerca a un
número fijo: su **promedio límite**. La computadora puede calcularlo sin
simular. Es el promedio de $U$ sobre todas las partidas posibles, cada una
con su probabilidad, si **los dos** eligen al azar.

La tabla lo pone junto a lo que ya conoces. La columna «Azar» es ese
promedio límite. «Corte» es el valor con corte a profundidad 1, en la escala
de $\mathrm{EVAL}$. «$V$» es el valor del juego. «Azar» y «$V$» van en la
escala de $U$, entre ${-1}$ y ${+1}$. En [[cortar-y-evaluar|Cortar y evaluar]]
escribimos $V$ multiplicado por 100; aquí va sin multiplicar.

::: table {#jue-c3-simulaciones title="Promedio de infinitas simulaciones en la posición de la clase"}
| Jugada | Azar | Corte | $V$ |
|---|---:|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 0.21 | 2 | −1 |
| $\text{d2}\textbf{-}\text{d3}$ | **0.89** | 2 | +1 |
| $\text{d2}\textbf{x}\text{c3}$ | 0.15 | **13** | −1 |
:::

**Aquí simular acierta.** La jugada con mejor promedio es
$\text{d2}\textbf{-}\text{d3}$, la que gana, y la captura queda última. Sin
que nadie le escriba una evaluación, la simulación «ve» que el peón de más
se pierde. En las partidas al azar, Negras recaptura muchas veces.

**Pero un promedio no es el valor.** En hexapawn, las tres aperturas de
Blancas valen ${-1}$: Negras gana si juega bien. Sus promedios de simulación
son los tres **positivos**.

Ojo con un número que ya viste. En
[[cuando-decide-un-dado|Cuando decide un dado]] solo Negras jugaba al azar
y Blancas elegía lo mejor: ahí $\text{b1}\textbf{-}\text{b2}$ valía ${3/4}$.
Aquí juegan al azar los dos, y vale ${5/24}$. En la tabla, «Ambos» es el
promedio límite con los dos al azar y «Solo Negras», con solo Negras al azar.

::: table {#jue-c3-hexapawn-azar title="Hexapawn: las aperturas con uno o con los dos al azar"}
| Apertura | Ambos | Solo Negras |
|---|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 7/36 | 5/9 |
| $\text{b1}\textbf{-}\text{b2}$ | 5/24 | 3/4 |
| $\text{c1}\textbf{-}\text{c2}$ | 7/36 | 5/9 |
:::

::: exercise {#jue-c3-ej-promedio title="Traduce un promedio a partidas ganadas"}
Con ${U=\pm1}$, un promedio $\bar u$ y la probabilidad $p$ de que gane MAX
cumplen ${p=(\bar u+1)/2}$, como en
[[cuando-decide-un-dado|Cuando decide un dado]].

1. ¿Con qué probabilidad gana Blancas las partidas al azar que empiezan con
   $\text{d2}\textbf{-}\text{d3}$, si el promedio es ${8/9}$?
2. Las de hexapawn que empiezan con $\text{b1}\textbf{-}\text{b2}$ tienen
   promedio ${5/24}$. ¿Cuántas gana Blancas? ¿Por qué no contradice que
   $\text{b1}\textbf{-}\text{b2}$ valga ${-1}$?
:::

::: hint {#jue-c3-pista-promedio-1 of="jue-c3-ej-promedio" title="Qué supone cada número"}
Para el inciso 2: cada uno de los tres números de la fila de
$\text{b1}\textbf{-}\text{b2}$ responde a una pregunta distinta. ¿Cómo
elige sus jugadas cada jugador en cada una?
:::

::: answer {#jue-c3-resp-promedio of="jue-c3-ej-promedio"}
1. ${p=(8/9+1)/2=17/18}$: Blancas gana 17 de cada 18 partidas al azar.
2. ${p=(5/24+1)/2=29/48}$: un poco más de 6 de cada 10. No lo contradice:
   en las simulaciones, Negras juega al azar y se equivoca seguido; ${V=-1}$
   supone que Negras juega perfecto. Tampoco es el ${3/4}$ de la clase 2:
   ahí Blancas jugaba lo mejor y solo Negras al azar. Son tres supuestos
   sobre los jugadores, y tres números.
:::

El promedio se equivoca cuando el rival al azar no se parece al rival de
verdad. ¿Qué se gana a cambio de ese defecto?

## 3 · Qué cambia respecto de la evaluación

**Piensa: ¿qué necesita saber del juego este método, además de las
reglas?**

Nada. Esa es la diferencia con [[cortar-y-evaluar|cortar y evaluar]]:

::: table {#jue-c3-eval-contra-mcts title="Cortar y evaluar contra Monte Carlo plano"}
| | Cortar y evaluar | Monte Carlo plano |
|---|---|---|
| Pide | $\mathrm{EVAL}$ a mano | Solo las reglas: $A$, $T$, $S_F$ y $U$ |
| Para | En $d$ | En los finales |
| Da | Minimax de $\mathrm{EVAL}$ | Promedio de $U$ |
| Mejora con | Más $d$, mejor $\mathrm{EVAL}$ | Más simulaciones |
:::

Por eso sirve en juegos donde nadie sabe escribir una buena evaluación.
El ejemplo clásico es el **Go**.

::: exercise {#jue-c3-ej-cambio title="Señala qué método hay que rehacer"}
Cambias una regla del 4×4: ahora un peón también puede avanzar dos
casillas en su primera jugada.

1. ¿Cuál de los dos métodos sigue funcionando tal cual?
2. ¿Qué tendrías que revisar en el otro, y por qué?
:::

::: hint {#jue-c3-pista-cambio-1 of="jue-c3-ej-cambio" title="Quién escribió cada pieza"}
En cada método, ¿qué pieza sale de las reglas y cuál la escribió una
persona pensando en las reglas viejas?
:::

::: answer {#jue-c3-resp-cambio of="jue-c3-ej-cambio"}
1. **Monte Carlo plano.** Solo usa las reglas ($A$, $T$, $S_F$ y $U$), y esas
   ya son las nuevas:
   las simulaciones juegan el juego nuevo sin que nadie las toque.
2. **La $\mathrm{EVAL}$ de cortar y evaluar.** Se escribió a mano para el
   juego viejo: con peones más rápidos, cuánto vale avanzar puede cambiar.
   Minimax y el corte no cambian; la estimación sí hay que revisarla.
:::

Monte Carlo plano solo pide las reglas. Pero, tal como va, reparte las
simulaciones a ciegas y deja que el rival juegue al azar. MCTS, en
las dos secciones que siguen, ataca las dos cosas.

## 4 · Dar una vuelta de MCTS

**Piensa: si tienes tiempo para 1000 simulaciones y tres jugadas, ¿las
repartirías por igual?**

No conviene: simular solo desde la raíz reparte igual las partidas entre
jugadas buenas y malas. MCTS **construye un árbol poco a poco** y manda más
simulaciones a las jugadas que van mejor.

Cada nodo $s'$ del árbol guarda dos números. $N(s')$ cuenta las
simulaciones que pasaron por él; aquí $N$ no es Negras. $G(s')$ cuenta en
cuántas de ellas ganó MAX, sea quien sea el que mueve en $s'$; aquí $G$ no
es el grafo de la clase 1.

De esos dos números sale el promedio de $U$. En este juego no hay
empates: cada simulación la gana MAX, con ${U=+1}$, o la gana MIN, con
${U=-1}$. De las $N(s')$ partidas, MAX ganó $G(s')$ y MIN las otras
${N(s')-G(s')}$. La suma de las $U$ es victorias menos derrotas: la misma
cuenta que el ${7\cdot(+1)+3\cdot(-1)}$ de la sección 1. Entre $N(s')$, da
el promedio:

$$\begin{aligned}
\bar u(s')&=\frac{G(s')-\bigl(N(s')-G(s')\bigr)}{N(s')}\\
&=\frac{2G(s')-N(s')}{N(s')}=2\,\frac{G(s')}{N(s')}-1.
\end{aligned}$$

En palabras: ${G/N}$ es la fracción de partidas que ganó MAX, y $\bar u$
la pasa a la escala de $U$. Es la relación ${p=(\bar u+1)/2}$ de la
sección 2, despejada, con $p$ medida en vez de calculada. $\bar u$ se mide
**siempre desde MAX**, también donde mueve MIN. En la raíz de la figura de
abajo, ${G/N=2/4}$: MAX ganó la mitad, y ${\bar u=2\cdot\tfrac24-1=0}$.

Cada vuelta tiene cuatro pasos:

1. **Selección.** Desde la raíz, baja por el árbol ya construido y para en
   el **primer nodo al que le falta algún hijo**: una jugada que todavía no
   está en el árbol. Por ahora, MAX baja al hijo de mayor $\bar u$ y MIN al
   de menor; la sección 5 cambia esta regla.
2. **Expansión.** Agrega al árbol un hijo nuevo bajo el nodo donde paró la
   selección: $T(s,a)$, con $s$ ese nodo y $a$ la primera de las jugadas
   que faltaban, en un orden fijo.
3. **Simulación.** Desde el hijo nuevo, juega una partida al azar hasta un
   final y anota su $U$. Es la primera simulación del hijo: cada nodo nace
   con la suya.
4. **Retropropagación.** Sube por el camino recorrido hasta la raíz. Cada
   nodo del camino, incluido el nuevo, suma 1 a sus simulaciones y, si
   ganó MAX, 1 a sus victorias. Eso vale también en los nodos de MIN.

Si la selección llega a un final, no hay nada que expandir ni simular: su
$U$ es el resultado de la vuelta, y cuenta como una simulación más.

Así, cada vuelta aporta un resultado, y decimos que esa simulación «pasó
por» cada nodo del camino. Pero solo el tramo debajo del hijo nuevo se
jugó al azar: arriba, el camino lo eligió la selección.

En la figura, cada caja dice ${G/N}$. La raíz y el ${2/3}$ ya tienen todas
sus jugadas en el árbol, dos cada uno, así que la selección pasa por ellos.
El ${0/1}$ al que baja MIN no tiene ningún hijo todavía: ahí para, y bajo
él nace el ${0/0}$.

Las cuentas salen de cómo nace cada nodo. La raíz es el estado de partida:
no nació en una expansión y no simula. Sus cuentas suman las de sus hijos,
${2/4=2/3+0/1}$. Cada otro nodo suma la suya y las de sus hijos: el
${2/3}$ es su simulación, que ganó MAX (${1/1}$), más ${1/1}$ y ${0/1}$.
Ahí mueve MIN, y su 2 cuenta igual victorias de MAX.

::: figure {#jue-c3-fig-mcts title="Una vuelta de MCTS: la raíz pasa de 2/4 a 3/5"}
![Cuatro paneles con el mismo árbol; cada caja dice G/N, victorias de MAX entre simulaciones que pasaron por ella. 1, selección: desde la raíz, 2/4, donde mueve MAX, se baja a 2/3; ahí mueve MIN y baja a 0/1, donde MAX ganó menos. 2, expansión: aparece un hijo nuevo, 0/0, bajo ese 0/1. 3, simulación: desde el hijo nuevo, una línea quebrada llega a un final con U = +1. 4, retropropagación: cada nodo del camino suma una simulación y una victoria; 2/4 pasa a 3/5, 2/3 a 3/4, 0/1 a 1/2 y 0/0 a 1/1. Los nodos fuera del camino, 1/1 y el otro 0/1, no cambian](../_assets/jue-c3-mcts-pasos.svg)
:::

Las vueltas se repiten mientras haya tiempo. Al final, en esta versión, se
juega la jugada de la raíz **por la que pasaron más simulaciones**, no la de
mejor promedio. Un promedio de pocas partidas puede ir alto por suerte; el
de la más simulada es el que tiene más evidencia detrás.

Es la convención
más común, no la única: otras versiones entregan la de mayor promedio.
Como la profundización
iterativa de [[jugar-contra-el-reloj|Jugar contra el reloj]], siempre tiene
una jugada lista.

::: exercise {#jue-c3-ej-retro title="Completa la vuelta con una derrota"}
Repite la vuelta de la figura con el mismo camino y el mismo hijo nuevo,
pero la simulación termina en ${U=-1}$: gana MIN.

1. ¿Qué ${G/N}$ quedan en los cuatro nodos del camino, de la raíz al nuevo?
2. ¿Cambia algún nodo fuera del camino?
3. ¿Cuánto vale ahora $\bar u$ en la raíz?
:::

::: hint {#jue-c3-pista-retro-1 of="jue-c3-ej-retro" title="Qué cuenta cada número"}
De los dos números de cada caja, ¿cuál cuenta todas las partidas que
pasaron por ahí y cuál solo algunas?
:::

::: answer {#jue-c3-resp-retro of="jue-c3-ej-retro"}
1. La raíz pasa de ${2/4}$ a ${2/5}$; el ${2/3}$, a ${2/4}$; el ${0/1}$ del camino,
   a ${0/2}$; el nuevo, de ${0/0}$ a ${0/1}$. Todos suman una simulación y
   ninguna victoria: un ${U=-1}$ no resta, solo deja de sumar.
2. No: el ${1/1}$ y el otro ${0/1}$ no estaban en el camino.
3. ${\bar u=(2\cdot2-5)/5=-0.2}$. Antes de la vuelta valía $0$.
:::

La regla provisional de la selección tiene un hueco. En la figura, el
${0/1}$ que cuelga de la raíz lleva ${\bar u=-1}$ tras **una sola**
partida. Bajando siempre por el mayor $\bar u$, MAX no vuelve a él nunca:
el ${2/3}$ ya ganó dos, y su $\bar u$ no puede bajar a ${-1}$. Una mala
suerte en su primera simulación lo condena. ¿Cómo darle otra oportunidad
sin repartir las vueltas a ciegas?

## 5 · Explorar o aprovechar

**Piensa: ¿conviene seguir probando la jugada que va mejor, o darle otra
oportunidad a una que casi no se ha probado?**

Las dos cosas. **Aprovechar** es elegir lo que ya funcionó; **explorar** es
probar lo poco probado, por si es mejor. La regla más usada se llama
**UCT** (del inglés *upper confidence bounds applied to trees*). Le suma a
cada promedio un bono que crece si la jugada se ha probado poco:

$$\text{puntaje}(s')=\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

- $s$ es el nodo donde se elige y $s'$, uno de sus hijos. Aquí $s$ ya no es
  solo la raíz del problema: es cualquier nodo por el que baja la selección.
- $\bar u(s')$ es el de la sección 4: el promedio de $U$ de las simulaciones
  que pasaron por $s'$, siempre desde MAX.
- $N(s)$ y $N(s')$ cuentan las simulaciones que pasaron por cada nodo.
- $\ln$ es el logaritmo natural; aquí solo importa que crece muy despacio.
- $c$ es un número positivo que elegimos: más grande, más exploración. En
  esta página, ${c=1}$.

Así escrito es el puntaje de MAX, que quiere $\bar u$ alto. MIN lo quiere
bajo, así que en un nodo de MIN el primer término es $-\bar u(s')$:

$$\text{puntaje}(s')=-\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

Elegir el mayor de estos es elegir el hijo de ${\bar u-\text{bono}}$ más
bajo. El bono suma en los dos casos: explorar no tiene lado.

El primer término aprovecha; el segundo explora y se encoge con muchas
simulaciones. Un hijo con ${N(s')=0}$ tendría bono infinito, pero en el
árbol no los hay: cada nodo nace con su simulación. ${N=0}$ es una jugada
aún no expandida. Por eso la selección para en el primer nodo al que le
falta un hijo: ese hijo ganaría a cualquiera.

En la figura, MIN elige en el ${2/3}$, con ${N(s)=3}$, entre el ${1/1}$
(${\bar u=+1}$) y el ${0/1}$ (${\bar u=-1}$). Los dos llevan una
simulación, así que su bono es el mismo, ${\sqrt{\ln 3}\approx1.05}$. Sus
puntajes son ${-1+1.05=0.05}$ y ${+1+1.05=2.05}$: MIN baja al ${0/1}$.

Así corrige MCTS el defecto de la sección 2, el **rival al azar**. Donde ya
construyó árbol, MIN elige por puntaje, no al azar: lo que parece mejor para
él, más un bono para lo poco probado. Con suficientes vueltas se concentra
en su mejor respuesta. Solo la simulación, debajo del árbol, sigue jugando
al azar.

**La idea del bono viene del bandido:** elegir una y otra vez entre
jugadas que pagan al azar, sin árbol debajo. Ahí el bono es un margen de
error del promedio: cuánto podría errar una jugada con pocas partidas, del
lado que le importa a quien elige (abajo para MAX, arriba para MIN).

Por eso se encoge al crecer $N(s')$. Crece despacio con ${\ln N(s)}$: conforme
avanza la búsqueda, se pide más confianza antes de dar una jugada por mala.
Y $c$ fija cuánta.

[[de-donde-sale-el-bono|De dónde sale el bono]] dice de dónde sale $c$. En corto: si $N(s')$ se
fijara antes de ver los resultados, $\delta$ acotaría la probabilidad de
que el promedio quedara por debajo de su promedio límite en más que el
bono. Esa $\delta$ baja conforme crece $N(s)$, y $c$ fija qué tan rápido.
Nuestra ${c=1}$ pide ${\delta=1/\sqrt{N(s)}}$: 10 % con ${N(s)=100}$.

En la regla UCB, $N(s')$ depende de lo que salió: $\delta$ guía la
elección de $c$, pero no es una probabilidad garantizada. En UCT, además,
el blanco cambia: lo que se juega debajo de cada nodo va cambiando, y el
promedio no tiene un blanco fijo.

Muchos textos usan la fracción de victorias ${G/N}$ en vez de $\bar u$.
Como ${\bar u=2\,G/N-1}$, el puntaje es

$$\begin{aligned}
&\bar u+c\sqrt{\ln N(s)/N(s')}\\
&\quad=2\,\bigl(G/N+\tfrac c2\sqrt{\ln N(s)/N(s')}\bigr)-1.
\end{aligned}$$

Usar ${G/N}$ con la misma $c$ equivale a duplicar $c$: la ${c=\sqrt2}$ de
esos textos, con ${G/N}$, es ${c=2\sqrt2}$ con $\bar u$.

::: exercise {#jue-c3-ej-mcts title="Calcula qué se explora y qué se entrega"}
Tras 100 vueltas, las tres jugadas de la raíz, donde mueve MAX, tienen:

- **x:** ${N=60}$ simulaciones, promedio ${\bar u=0.5}$;
- **y:** ${N=30}$ simulaciones, promedio ${\bar u=0.6}$;
- **z:** ${N=10}$ simulaciones, promedio ${\bar u=0.2}$.

1. Si el tiempo se acaba ahora, ¿qué jugada se entrega?
2. Si queda tiempo para una vuelta más, calcula el puntaje de cada una con
   ${c=1}$ y ${\ln 100\approx4.61}$. ¿Por cuál baja la selección?
3. ¿Coinciden las dos respuestas? Explica por qué no hay contradicción.
:::

::: hint {#jue-c3-pista-mcts-1 of="jue-c3-ej-mcts" title="Cuándo se usa cada regla"}
¿Qué regla se aplica cuando el tiempo ya se acabó, y cuál mientras todavía
quedan vueltas? ¿Qué número de la lista mira cada una?
:::

::: answer {#jue-c3-resp-mcts of="jue-c3-ej-mcts"}
1. **x:** al final se entrega la jugada con más simulaciones, y x tiene 60.
2. Los puntajes son

   $$\begin{aligned}
   x&:\ 0.5+\sqrt{4.61/60}\\
   &\approx0.5+0.28=0.78,\\[4pt]
   y&:\ 0.6+\sqrt{4.61/30}\\
   &\approx0.6+0.39=0.99,\\[4pt]
   z&:\ 0.2+\sqrt{4.61/10}\\
   &\approx0.2+0.68=0.88.
   \end{aligned}$$

   La selección baja por **y**. La z recibe el bono más grande, pero su
   promedio bajo la deja segunda.
3. **No coinciden, y está bien.** Entregar busca la jugada más confiable:
   60 partidas pesan más que 30. Seleccionar decide dónde gastar la vuelta
   que sigue, y y todavía tiene poca evidencia para lo bien que va. Con
   ${G/N}$ o con ${c=\sqrt2}$ la selección iría a z: las dos le dan más
   peso al bono que nuestra ${c=1}$ (con ${G/N}$ es como usar ${c=2}$), y el
   bono favorece a z.
:::

Queda abierta la pregunta que esta sección pasó de largo: **¿de dónde sale
ese bono, y cuánto debe valer $c$?** La contesta
[[de-donde-sale-el-bono|De dónde sale el bono]].

## 6 · Ubicar MCTS en la historia

**Piensa: Deep Blue y AlphaGo ganaron con búsqueda. ¿Qué pieza cambió de
uno a otro?**

La que estima lo que no se alcanza a calcular:

- **Deep Blue venció a Kasparov en 1997.** Buscaba con alfa-beta y una
  función de evaluación compleja, ajustada en su mayoría a mano: cortar y
  evaluar.
- **Desde 2006**, cuando Rémi Coulom le dio nombre al método, los programas
  de Go más fuertes usan MCTS: simular en vez de evaluar.
- **En marzo de 2016, AlphaGo**, de DeepMind, venció 4 a 1 a Lee Sedol, uno
  de los mejores jugadores de Go del mundo. Combinaba MCTS con **redes
  neuronales**: una sugería qué jugadas explorar y otra estimaba cuánto
  valía una posición. Al valorar un nodo nuevo, AlphaGo mezclaba esa
  estimación, mitad y mitad (${\lambda=0.5}$), con el resultado de una
  simulación rápida guiada por una política rápida y sencilla.
- **AlphaGo Zero y AlphaZero, en 2017, quitaron las partidas simuladas
  hasta el final** (en inglés, *rollouts*): una red que aprende jugando
  contra sí misma sugiere jugadas y valora posiciones.

¿Sigue siendo MCTS sin esas partidas? Sí: sigue dando vueltas de MCTS, con
el árbol, las cuentas y la selección por puntaje. Lo que más cambia es el
paso 3: la red valora el hijo nuevo, sin jugar desde él una partida al
azar. También guía la selección y la expansión:
su puntaje no es el UCT, porque suma un término que premia la jugada que la
red sugiere.

**Punto de control:** deberías poder dar una vuelta de MCTS a mano, con
${G/N}$ en cada nodo y cualquier resultado. También, calcular el puntaje UCT
de un hijo y decir por qué un promedio de simulaciones no es $V$.

## Ficha: Monte Carlo plano y MCTS con UCT

Antes de cerrar, dos fichas, una debajo de la otra. **Monte Carlo plano** es lo de las secciones 1 a 3: simular desde cada jugada de la raíz, sin construir árbol.

::: table {#jue-ficha-mc-plano title="Monte Carlo plano en siete rasgos"}
| Rasgo | Monte Carlo plano |
|---|---|
| Hasta dónde mira | Hasta los finales, jugando al azar |
| ¿Genera todo el árbol? | No: solo las partidas que simula |
| ¿Garantiza $V$? | No: $\bar u$ se acerca al promedio con los dos al azar, no a $V$ |
| Con qué estima | Con $\bar u$ de simulaciones |
| ¿Quién tira dados? | El algoritmo, en cada simulación |
| Qué entrega, y si se puede interrumpir | La jugada de mayor $\bar u$. Sí se puede interrumpir |
| Cuándo conviene | Sin $\mathrm{EVAL}$ confiable: Go experimental, de 1993 a 2005 (Brügmann, 1993) |
:::

**MCTS con UCT** es lo de las secciones 4 y 5: el mismo $\bar u$, pero con un árbol que reparte las partidas.

::: table {#jue-ficha-uct title="MCTS con UCT en siete rasgos"}
| Rasgo | MCTS con UCT |
|---|---|
| Hasta dónde mira | Un árbol que crece hacia lo que va mejor; debajo, partidas al azar hasta los finales |
| ¿Genera todo el árbol? | No necesita: agrega a lo más un nodo por vuelta, más su partida. Con suficientes vueltas expande todo un árbol finito (el árbol T± de «Radiografía: un árbol, cinco algoritmos», de 15 nodos, con 40) |
| ¿Garantiza $V$? | No. Con tiempo sin límite converge a él, con cualquier $c>0$ |
| Con qué estima | Con $\bar u$ de simulaciones |
| ¿Quién tira dados? | El algoritmo, en las simulaciones. Esta versión expande y desempata en orden fijo, así que dentro del árbol no sortea; otras sí |
| Qué entrega, y si se puede interrumpir | Aquí, la jugada más simulada, no la de mayor puntaje; otras versiones entregan la de mayor promedio. Sí se puede interrumpir |
| Cuándo conviene | Sin $\mathrm{EVAL}$ confiable y con árboles enormes: Go (MoGo, 2006), Hex (MoHex) |
:::

> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | Alfa-beta | $V$ en la raíz; lo garantiza |
> | Minimax con corte | Valor con corte; no garantiza $V$, salvo si llega a los finales |
> | Búsqueda de quietud | Valor con quietud; no garantiza $V$, salvo si llega a los finales antes de cortar |
> | Profundización iterativa | Valor con corte de la última búsqueda; no garantiza $V$, salvo si llega a los finales |
> | **Monte Carlo plano (estás aquí)** | **$\bar u$; no garantiza $V$** |
> | **MCTS con UCT (estás aquí)** | **$\bar u$; no garantiza $V$ (con tiempo sin límite converge a él, con cualquier $c>0$)** |
>
> **Lo que viene.**
>
> Ya viste todos los algoritmos de la clase. [[un-arbol-todos-los-algoritmos|Radiografía: un árbol, cinco algoritmos]] los pone lado a lado.

## Lo que hay que llevarse

- **Monte Carlo plano** estima una jugada simulando partidas al azar hasta
  el final y promediando su $U$. No necesita $\mathrm{EVAL}$: solo las
  reglas.
- Ese promedio no es $V$: supone que **los dos** juegan al
  azar. En la posición de la clase acierta ($\text{d2}\textbf{-}\text{d3}$,
  ${8/9}$, 17 de cada 18 partidas). En hexapawn, $\text{b1}\textbf{-}\text{b2}$
  promedia ${5/24}$ aunque vale ${-1}$; con solo Negras al azar valía ${3/4}$.
- **MCTS** construye un árbol: dentro de él cada jugador elige por puntaje,
  y solo debajo se simula al azar. Por eso su $\bar u$ no es ese promedio
  con los dos al azar; con UCT y más vueltas, se acerca a $V$.
- Cada vuelta tiene cuatro pasos: selección, expansión, simulación y
  retropropagación. Cada nodo guarda ${G/N}$, y ${\bar u=2\,G/N-1}$ desde
  MAX: victorias menos derrotas entre $N$. La retropropagación suma 1 a
  $N$ siempre y 1 a $G$ solo si gana MAX: la raíz pasa de ${2/4}$ a ${3/5}$, o
  a ${2/5}$ si pierde.
- El puntaje UCT, ${\bar u+c\sqrt{\ln N(s)/N(s')}}$, equilibra aprovechar y
  explorar; MIN usa $-\bar u$. El bono viene del margen de error de un
  promedio en el bandido.
  Con x, y, z y ${c=1}$, la selección va a y, que puntúa 0.99; la
  entrega, a x, que tiene 60 simulaciones.
- Deep Blue (1997) cortó y evaluó; AlphaGo (2016) combinó MCTS con redes;
  AlphaGo Zero y AlphaZero (2017) cambiaron la partida simulada hasta el
  final por una red que valora la hoja, y que además guía la selección.

Continúa con [[un-arbol-todos-los-algoritmos|Radiografía: un árbol, cinco algoritmos]].
