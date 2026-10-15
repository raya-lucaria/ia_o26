---
id: monte-carlo-en-un-arbol-grande
title: Monte Carlo y UCT en un árbol grande
nav_title: Monte Carlo y UCT en un árbol grande
summary: "En un árbol que no cabe, Monte Carlo plano simula caminos al azar y guarda solo contadores en la raíz, y por eso estima el promedio con los dos al azar. UCT construye su propio árbol, elige con el puntaje dentro de él y al azar solo debajo de su frontera, y crece hondo en lo prometedor."
status: ready
estimated_time: 30m
tags: [juegos, mcts, comparacion]
---

# Monte Carlo y UCT en un árbol grande

## UCT en el árbol grande

UCT corrige justo eso. Construye **su propio árbol de búsqueda: una parte del árbol del juego**, que empieza con solo la raíz. Dentro de ese árbol, también MIN elige por puntaje, no al azar; solo fuera de él se juega al azar.

- **Qué rastrea:** en **cada nodo** $s$ de su árbol, sus visitas $N(s)$ y su promedio $\bar u(s)$. El valor de una jugada $a$ desde $s$ es el del hijo al que lleva, $T(s,a)$. En un juego sin azar, cada jugada lleva a un solo hijo. 
- **Otra notación:** otros textos guardan esos números en la jugada. Escriben las visitas $N(s,a)=N(T(s,a))$ y llaman $Q(s,a)$ al promedio, aunque es una estimación. Aquí $Q(s,a)$ es el valor exacto, y el promedio, $\bar u$.
- **Cómo sube:** el **mismo $U$** de cada vuelta sube por todo el camino, desde abajo hasta la raíz. Cada nodo del camino lo mete en su promedio. Promedia; no toma máximos ni mínimos.
- **A qué converge:** cada promedio $\bar u(s)$, al valor de minimax $V(s)$, en un árbol finito, con $c>0$ fija y vueltas sin límite. Con un presupuesto fijo, no hay garantía.

### Tres cosas que no hay que confundir

Antes de las fases, tres palabras que se parecen:

- **Hoja de su árbol:** un nodo guardado sin hijos agregados todavía. Puede tener muchas jugadas permitidas pendientes.
- **Final del juego:** ya tiene su $U$, dado por las reglas.
- **Frontera:** las jugadas permitidas que salen de nodos guardados y todavía no se han agregado. No es un nivel parejo: sigue el contorno irregular del árbol.

El $U$ que sube por el árbol es el mismo de siempre, y solo un final lo tiene:

$$
\mathbf{U(s)}=\begin{cases}+1 & \text{si gana MAX}\\-1 & \text{si gana MIN}\\0 & \text{si empatan}\end{cases}
$$

### Una vuelta, en el árbol grande

Cada vuelta (*iteration*) tiene cuatro fases:

1. **Selección (*selection*).** Desde la raíz, baja por los nodos guardados. En un nodo con todos sus hijos agregados, elige uno con el puntaje UCT. Se detiene en el primer nodo que todavía tiene una jugada sin agregar —una jugada de la frontera— o al llegar a un final.
2. **Expansión (*expansion*).** Si encontró una jugada pendiente, agrega la primera, en el orden dado, como **un hijo nuevo**: a lo más un nodo por vuelta. Si llegó a un final, no agrega nada y pasa directo a la retropropagación.
3. **Simulación (*rollout* o *playout*).** Desde el hijo nuevo, juega al azar, para los dos, hasta un final. Es un camino como los de Monte Carlo plano, y tampoco se guarda. Si el hijo nuevo ya es un final, toma su $U$ sin simular.
4. **Retropropagación (*backpropagation*).** Sube ese $U$ por el camino hasta la raíz. Cada nodo del camino suma una visita a $N(s)$ y mete el resultado en su promedio $\bar u(s)$. **El signo no cambia al subir:** todo se mide desde MAX.

#### El puntaje de la selección

En un nodo $s$ de MAX, el puntaje de cada hijo $s'$ es

$$
\mathbf{\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}}
$$

y MAX baja al de mayor puntaje. El primer término es lo que ya se vio de ese hijo; el segundo, el **bono**, premia lo poco visitado. En un nodo de MIN, se baja al de menor $\bar u(s')-\text{bono}$; el promedio guardado sigue medido desde MAX. La fórmula nunca se calcula con $N(s')=0$: una jugada sin visitas se atiende en la expansión.

> [!NOTE]
> **Con esta sola función, el ciclo de UCT hace nacer solas la búsqueda, la información y la estimación.** El puntaje decide a qué hijo bajar: eso es la búsqueda. La simulación y la retropropagación suman una visita en $N$ a cada nodo del camino: eso es la información, cuánto se ha probado.
>
> Cada vuelta deja también un resultado que se promedia en $\bar u$: eso es la estimación. El bono cierra el círculo: donde falta información, es grande y atrae la búsqueda.

::: figure {#jue-c3-mcg-fig-uct-fases title="Las fases de UCT en un árbol grande"}
![Las cuatro fases de UCT en el árbol grande: selección por el árbol guardado hasta la frontera, expansión de un hijo nuevo, simulación al azar hasta un final y retropropagación por el mismo camino; y el caso en que la selección llega a un final ya guardado, que solo retropropaga](../_assets/jue-c3-mcg-uct-fases.svg)
:::

#### Un final que ya está en el árbol

**Cuando la selección llega a un final que ya está en el árbol, solo retropropaga.** Al principio pasa poco; con muchas vueltas, cada vez más, en las ramas donde el árbol ya llegó hasta los finales.

- **No expande:** ese final ya es parte de su árbol.
- **No simula:** las reglas ya dan su $U$; no hay nada que estimar.
- **Sí cuenta como vuelta:** sube ese $U$ por el camino, y cada nodo suma una visita y actualiza su promedio, igual que en una vuelta normal.

### Cómo crece el árbol

Vuelta tras vuelta, el árbol de UCT crece **desigual**: hondo por las jugadas que van bien, delgado por las demás. Las jugadas malas no desaparecen; reciben pocas vueltas.

- **Arriba de la frontera se elige con el puntaje.** Ahí, MAX y MIN eligen según lo que ya vieron, más el bono: aprovechan (*exploitation*) y exploran (*exploration*).
- **Debajo de la frontera se juega al azar.** Es el tramo de la simulación.
- **La frontera baja de forma desigual.** Donde el árbol se hace hondo, una parte mayor de cada camino se elige con el puntaje, y el tramo al azar se acorta.

::: figure {#jue-c3-mcg-fig-uct-crece title="El árbol de UCT crece desigual"}
![Tres instantáneas del árbol de UCT: con pocas vueltas, ramas parejas; con más, una rama más honda; con muchas, la rama prometedora muy honda y gruesa. La frontera, punteada, sigue el contorno del árbol: arriba se elige con el puntaje y abajo se juega al azar](../_assets/jue-c3-mcg-uct-crece.svg)
:::

#### La refutación, otra vez

**Así se arregla el ejemplo de la refutación.** Bajo la jugada $a$, el árbol de UCT agrega las respuestas de MIN. La refutación junta resultados de $-1$ y, por el puntaje, MIN la elige cada vez más: ya no depende de que el azar la encuentre. Con suficientes vueltas, el promedio de $a$ deja de parecerse a $\mu$ y baja hacia $V=-1$.

**Esa convergencia tiene condiciones:** un árbol finito, $c>0$ fija y vueltas sin límite. Con esas condiciones, los promedios se acercan a $V$. Con un presupuesto fijo, una refutación todavía puede pasar inadvertida.

### Cómo un promedio llega a parecerse a un mínimo

Minimax sube valores con máximos y mínimos; UCT solo promedia. Aun así, sus promedios se acercan a $V$.

Un ejemplo abstracto muestra cómo: MAX elige entre las jugadas $A$ y $B$. Tras $A$, MIN elige entre un final de $+1$ y uno de $-1$. La jugada $B$ lleva a un final de $-0.2$.

Para este ejemplo, deja que un final valga cualquier número entre $-1$ y $+1$; en los juegos de la unidad, $U$ solo toma $+1$, $-1$ o $0$, y nada de lo que sigue depende de eso.

- **Minimax juega $B$.** $V(A)=\min(+1,-1)=-1$ y $V(B)=-0.2$, así que $B$ es mejor para MAX.
- **Al principio, las respuestas de MIN bajo $A$ van casi parejas**, cerca de 50 % y 50 %. Entonces $\bar u(A)\approx 0$, y $A$ parece mejor que $B$.
- **Después, UCT favorece la respuesta buena para MIN.** El $-1$ tiene el promedio más bajo, y la selección de MIN lo elige cada vez más. Cada $-1$ sube también al promedio de $A$. Con proporciones ilustrativas, no medidas: si de 1000 vueltas por $A$ solo 10 fueron al $+1$, entonces $\bar u(A)=\frac{10(+1)+990(-1)}{1000}=-0.98$.
- **Lo viejo sigue en el promedio, pero pesa cada vez menos.** Las vueltas de cuando MIN repartía parejo no se borran; las nuevas las diluyen, y $\bar u(A)$ se acerca a $-1$.
- **MAX elige $A$ cada vez menos.** Con $\bar u(A)$ por debajo de $-0.2$, la raíz manda casi todas las vueltas a $B$. El bono sigue probando $A$ de vez en cuando. El promedio de la raíz tiende a $-0.2$, que es $V$.
- **Lo mismo ocurre en cada nivel.** En un árbol hondo, el efecto sube desde los finales hacia la raíz. Cuando los promedios de los hijos se acercan a sus valores de minimax, las jugadas mejores para quien mueve, juntas, se llevan casi todas las visitas. Entonces el promedio del padre se acerca al suyo.

::: figure {#jue-c3-mcg-fig-mezcla title="Un promedio que se vuelve un mínimo"}
![Un nodo de MIN bajo la jugada A, con sus dos respuestas, +1 y −1. Con pocas vueltas, las dos ramas tienen grosor parecido y el promedio de A queda cerca de 0. Con muchas, casi todas las visitas van a −1 y el promedio de A se acerca a −1. Proporciones ilustrativas](../_assets/jue-c3-mcg-mezcla.svg)
:::

**UCT no reemplaza el promedio por un máximo o un mínimo: elige cada vez mejor, y así las partidas de buen juego dominan los promedios.**

**El promedio del padre y los promedios de los hijos.**

- **El padre mezcla:** el $\bar u(s)$ de un nodo junta los resultados de las jugadas que ya eligió desde ahí. Cada una pesa según cuántas veces la eligió. Incluye también la simulación de cuando era nuevo.
- **La selección no usa esa mezcla:** en un nodo de MAX, compara cada hijo por su promedio más su bono.
- **La mezcla sigue a las elecciones:** al mejorar las elecciones, el promedio del padre se acerca al de su mejor hijo.
- **La jugada final tampoco sale de ese promedio:** es la de la raíz con más visitas.

### Por qué el bono hace natural explorar

El bono es ${c\sqrt{\ln N(s)/N(s')}}$, y cada parte tiene una razón:

- **$\sqrt{1/N(s')}$ tiene la forma del margen de un promedio.** Es la misma forma que en Monte Carlo plano: con pocas visitas, $\bar u(s')$ todavía puede estar lejos de lo que valdría con muchas. El bono le da a cada hijo el beneficio de la duda, en proporción a esa duda.
- **$\ln N(s)$ hace crecer el bono de un hijo olvidado.** Si un hijo deja de recibir visitas mientras su padre sigue recibiéndolas, su bono **crece**, despacio. Tarde o temprano supera al de los demás y el hijo vuelve a probarse.
- **$c$ fija cuánto pesa esa duda** frente al promedio.

En un árbol finito, con vueltas sin límite, **ninguna jugada se abandona para siempre**. Las que van mal se prueban cada vez con menos frecuencia, pero se siguen probando.

#### Por qué es solo intuición

**Esto es intuición, no garantía.** El margen de Monte Carlo plano pedía simulaciones independientes con una regla fija. En UCT no se cumple:

- **Lo que se juega debajo de un nodo cambia mientras se mide.** Su árbol crece y su selección se mueve, así que el blanco del promedio se desplaza.
- **Cuántas visitas recibe cada hijo depende de los resultados.** La selección decide la vuelta siguiente según lo que ya salió.

El bono sigue la forma del margen, pero ese margen, aquí, no se aplica directo.

### Por qué juega la más visitada

Al acabarse el tiempo o las vueltas, UCT juega la jugada de la raíz con **más visitas $N(s')$**: la regla del **hijo más visitado (*robust child*)**. Ante un empate, juega la primera en el orden dado.

- **Las visitas resumen la búsqueda.** La selección manda una vuelta a un hijo solo si su puntaje es el mayor. Que lo haga muchas veces quiere decir que se probó mucho y siguió viéndose bien.
- **Un promedio alto con pocas visitas puede ser suerte.** Su margen todavía es ancho.
- **Más visitas no demuestran más valor.** También influyen el bono, el orden y los primeros resultados. Con poco presupuesto, la regla puede equivocarse.

#### Un ejemplo: visitas contra promedio

| Jugada | Visitas | Promedio |
|---|---|---|
| $a$ | $80$ | $0.5$ |
| $b$ | $20$ | $0.6$ |

**UCT juega $a$.** El promedio de $b$ descansa en pocas partidas; $b$ podría ser mejor, pero la búsqueda todavía no lo mostró. Si hay una sola jugada óptima y se cumplen las condiciones de convergencia, con suficientes vueltas las dos reglas, por visitas y por promedio, terminan eligiéndola. Elegir por visitas es la convención del curso; el artículo original de UCT usa el mayor promedio.

---

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

---

## 7 · Seleccionar no es entregar

**Piensa: cuando se acaba el tiempo, ¿se entrega la jugada de mayor
puntaje?**

No. Al terminar, el bono **se quita**:

::: table {#jue-c3-tabla-seleccionar title="Seleccionar no es entregar"}
| | Selección | Entrega |
|---|---|---|
| Cuándo | Cada vuelta | Al final |
| Mira | Puntaje | $N(s')$ |
| Bono | Sí | No |
| Busca | Qué probar | Lo más probado |
:::

El bono premia la ignorancia, y eso sirve para aprender. Para jugar de
verdad se quiere evidencia: aquí, la jugada con más simulaciones. Es una
convención, la más usada, no la única: otras versiones entregan la de mayor
promedio, sin bono, y esa es la que analizan Kocsis y Szepesvári (sección 8).
Elegimos la más simulada porque un promedio de pocas partidas puede ir alto
por suerte.

::: exercise {#jue-c3-ej-entregar title="Señala qué se entrega"}
En el ejercicio de MCTS, x tenía ${N=60}$ y ${\bar u=0.5}$; y, ${N=30}$ y
${0.6}$; z, ${N=10}$ y ${0.2}$. Con ${c=2\sqrt2}$ la selección iba a z. Se
acaba el tiempo.

1. ¿Qué jugada se entrega?
2. y tiene el mejor promedio. ¿Por qué no se entrega y?
:::

::: hint {#jue-c3-pista-entregar-1 of="jue-c3-ej-entregar" title="Promedio y evidencia"}
¿Qué cambia entre seleccionar y entregar: qué número mira cada uno?
:::

::: answer {#jue-c3-resp-entregar of="jue-c3-ej-entregar"}
1. **x**, la de más simulaciones, 60. Ni z, la que seleccionaba, ni y.
2. El 0.6 de y descansa en 30 simulaciones, la mitad que x: su margen es
   mayor y su promedio, menos confiable. Además, la selección manda más
   vueltas a lo que parece mejor, así que la más simulada es la que la
   búsqueda confirmó más veces.
:::

Todo esto pasó en un solo nodo, la raíz. ¿Qué cambia cuando hay árbol
debajo?

Queda abierto de dónde sale exactamente la forma del bono y cuánto debe valer $c$: lo contesta [[de-donde-sale-el-bono|De dónde sale el bono]].
