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

Queda abierto de dónde sale exactamente la forma del bono y cuánto debe valer $c$: lo contesta [[de-donde-sale-el-bono|De dónde sale el bono]].
