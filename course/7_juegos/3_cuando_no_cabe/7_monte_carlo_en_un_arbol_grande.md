---
id: monte-carlo-en-un-arbol-grande
title: Monte Carlo y UCT en un árbol grande
nav_title: Monte Carlo y UCT en un árbol grande
summary: "En un árbol que no cabe, Monte Carlo plano simula caminos al azar y guarda solo contadores en la raíz, y por eso estima el promedio con los dos al azar. UCT construye su propio árbol, elige con el puntaje dentro de él y al azar solo debajo de su frontera, y crece hondo en lo prometedor."
status: ready
estimated_time: 25m
tags: [juegos, mcts, comparacion]
---

# Monte Carlo y UCT en un árbol grande

## Un árbol que no cabe

T± tiene 15 nodos: cabe en un dibujo y permite calcular minimax completo. Es demasiado chico para ver cómo trabajan Monte Carlo plano y UCT con un presupuesto limitado; para eso hace falta un árbol que **no** quepa.

Este es un árbol abstracto. En la raíz mueve MAX y los niveles alternan MAX y MIN. Cada nodo tiene hasta $b$ jugadas, y ninguna partida pasa de $m$ jugadas. Los «…» dicen que el dibujo sigue a lo ancho y a lo hondo. Los finales quedan muy abajo, cada uno con su $U$.

::: figure {#jue-c3-mcg-fig-arbol title="Un árbol de juego grande"}
![Árbol abstracto grande: b jugadas a lo ancho y m niveles a lo hondo, con puntos suspensivos en las dos direcciones y los finales al fondo](../_assets/jue-c3-mcg-arbol.svg)
:::

## Por qué no basta con lo anterior

Los métodos de la unidad ya tienen respuesta para un árbol así, y cada una pide algo que aquí falta:

- **Minimax** genera todo el árbol: del orden de $b^m$ nodos.
- **Alfa-beta**, con el orden perfecto de los hijos, baja a cerca de $b^{m/2}$. Sigue creciendo exponencialmente: con $m$ grande, tampoco cabe.
- **El corte** se detiene a profundidad $d$, pero necesita una **EVAL buena**. Si la EVAL se equivoca, el valor con corte se equivoca con ella.

Sin una EVAL confiable queda una pieza que siempre está: **las reglas**. Con ellas se puede jugar una partida hasta un final, al azar, y ver quién gana. Explorar todas las continuaciones es imposible, pero jugar **una** cuesta del orden de $m$ jugadas, no de $b^m$. Eso es simular, y aquí se supone que caben suficientes partidas en el presupuesto.

## Monte Carlo plano en el árbol grande

### Cómo explora

Monte Carlo plano (*flat Monte Carlo*) no construye árbol. Desde cada jugada de la raíz juega $k$ simulaciones (*rollouts* o *playouts*): partidas en las que **los dos** eligen al azar, entre sus jugadas permitidas, hasta un final.

- **Cada simulación es un camino, no un subárbol.** Baja eligiendo una jugada al azar en cada nivel, hasta un final lejano, y anota su $U$.
- **En la raíz guarda solo dos números por jugada:** cuántas simulaciones recibió, $N$, y la suma de sus $U$.
- **Debajo de la raíz no guarda nada.** Al terminar una simulación, los estados de su camino se olvidan; solo queda su $U$ sumado al contador.
- **Dos simulaciones pueden repetir camino.** Qué tan seguido pasa depende de la probabilidad de cada camino, no solo del tamaño del árbol.

Con esos dos números saca el promedio de cada jugada:

$$
\mathbf{\bar u=\frac{1}{N}\sum U}
$$

- **La suma recorre las $N$ simulaciones de esa jugada.** Cada una aporta $+1$ si gana MAX, $-1$ si gana MIN y $0$ si empatan.
- **El promedio se mide desde MAX:** entre más alto, mejor le fue a MAX en esas partidas.

::: figure {#jue-c3-mcg-fig-mc-plano title="Monte Carlo plano en un árbol grande"}
![Monte Carlo plano en el árbol grande: desde cada jugada de la raíz bajan simulaciones como caminos quebrados hasta finales lejanos; en la raíz solo hay N y ū por jugada, y debajo no se guarda nada](../_assets/jue-c3-mcg-mc-plano.svg)
:::

### Hacia dónde va su promedio

El **promedio límite** $\mu$ es el promedio de $U$ si los dos juegan al azar desde ahí. Pide una condición: que las simulaciones de una jugada sean **independientes** y sigan **siempre la misma regla al azar**. Entonces su $\bar u$ converge a $\mu$ con probabilidad 1 cuando $N$ crece. Con esa misma condición, la **intuición de Hoeffding** dice cuánto se puede fiar uno de un promedio antes de llegar al límite:

- **El promedio cae cerca de $\mu$, con alta probabilidad.** Para un número de simulaciones fijado de antemano, hay un margen alrededor de $\mu$ donde el promedio cae casi siempre.
- **Ese margen se encoge como $1/\sqrt N$.** Con cuatro veces más simulaciones, la mitad de margen.
- **No mejora en cada simulación.** Una partida de suerte puede alejar el promedio. Lo que se achica es el margen probable, no cada error.
- **Con pocas simulaciones, puede engañar.** El margen todavía es ancho, y una jugada mediocre puede ir arriba por suerte.

### Qué juega, y por qué puede fallar

Al terminar, Monte Carlo plano juega la jugada de la raíz con **mayor $\bar u$**; ante un empate, la primera en el orden dado. Con simulaciones independientes y cada vez más, la probabilidad de que esa sea la jugada de mayor $\mu$ tiende a 1. Pero $\mu$ supone que **MIN también juega al azar**, y un rival que piensa no lo hace.

Un ejemplo mínimo: MAX tiene dos jugadas, y tras cualquiera de ellas la respuesta de MIN termina la partida.

| Jugada | Finales tras MIN | $\mu$ | $V$ |
|---|---|---|---|
| $a$ | $+1$, $+1$, $-1$ | $1/3$ | $-1$ |
| $b$ | $0$, $0$ | $0$ | $0$ |

- **En $a$, MIN tiene una refutación:** de sus tres respuestas, una le gana. Al azar la elige una vez de cada tres, así que $\mu=(1+1-1)/3=1/3$. Pero un MIN que piensa siempre la juega, y $V=-1$.
- **En $b$, el empate es seguro:** $\mu=V=0$.
- **Con muchas simulaciones, Monte Carlo plano juega $a$ casi siempre, y entonces pierde** contra la mejor respuesta. Minimax jugaría $b$. Con pocas, el azar también puede llevarlo a $b$.
- **Con más respuestas buenas para MAX y una sola refutación, la distancia crece:** $\mu$ se acerca a $+1$ mientras $V$ sigue en $-1$.

Más simulaciones no lo arreglan. El promedio converge, pero **al número equivocado**: estima cada vez mejor lo que pasaría si el rival jugara al azar.

## UCT en el árbol grande

UCT corrige justo eso. Construye **su propio árbol de búsqueda: una parte del árbol del juego**, que empieza con solo la raíz. Dentro de ese árbol, también MIN elige por puntaje, no al azar; solo fuera de él se juega al azar.

Antes de las fases, tres cosas que no hay que confundir:

- **Hoja de su árbol:** un nodo guardado sin hijos agregados todavía. Puede tener muchas jugadas permitidas pendientes.
- **Final del juego:** ya tiene su $U$, dado por las reglas.
- **Frontera:** las jugadas permitidas que salen de nodos guardados y todavía no se han agregado. No es un nivel parejo: sigue el contorno irregular del árbol.

### Una vuelta, en el árbol grande

Cada vuelta (*iteration*) tiene cuatro fases:

1. **Selección (*selection*).** Desde la raíz, baja por los nodos guardados. En un nodo con todos sus hijos agregados, elige uno con el puntaje UCT. Se detiene en el primer nodo que todavía tiene una jugada sin agregar —una jugada de la frontera— o al llegar a un final.
2. **Expansión (*expansion*).** Si encontró una jugada pendiente, agrega la primera, en el orden dado, como **un hijo nuevo**: a lo más un nodo por vuelta. Si llegó a un final, no agrega nada y pasa directo a la retropropagación.
3. **Simulación (*rollout* o *playout*).** Desde el hijo nuevo, juega al azar, para los dos, hasta un final. Es un camino como los de Monte Carlo plano, y tampoco se guarda. Si el hijo nuevo ya es un final, toma su $U$ sin simular.
4. **Retropropagación (*backpropagation*).** Sube ese $U$ por el camino hasta la raíz. Cada nodo del camino suma una visita a $N(s)$ y mete el resultado en su promedio $\bar u(s)$. **El signo no cambia al subir:** todo se mide desde MAX.

**El puntaje de la selección.** En un nodo $s$ de MAX, el puntaje de cada hijo $s'$ es

$$
\mathbf{\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}}
$$

y MAX baja al de mayor puntaje. El primer término es lo que ya se vio de ese hijo; el segundo, el **bono**, premia lo poco visitado. En un nodo de MIN, se baja al de menor $\bar u(s')-\text{bono}$; el promedio guardado sigue medido desde MAX. La fórmula nunca se calcula con $N(s')=0$: una jugada sin visitas se atiende en la expansión.

::: figure {#jue-c3-mcg-fig-uct-fases title="Las fases de UCT en un árbol grande"}
![Las cuatro fases de UCT en el árbol grande: selección por el árbol guardado hasta la frontera, expansión de un hijo nuevo, simulación al azar hasta un final y retropropagación por el mismo camino; y el caso en que la selección llega a un final ya guardado, que solo retropropaga](../_assets/jue-c3-mcg-uct-fases.svg)
:::

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

Así se arregla el ejemplo de la refutación. Bajo la jugada $a$, el árbol de UCT agrega las respuestas de MIN. La refutación junta resultados de $-1$ y, por el puntaje, MIN la elige cada vez más: ya no depende de que el azar la encuentre. Con suficientes vueltas, el promedio de $a$ deja de parecerse a $\mu$ y baja hacia $V=-1$.

**Esa convergencia tiene condiciones:** un árbol finito, $c>0$ fija y vueltas sin límite. Con esas condiciones, los promedios se acercan a $V$. Con un presupuesto fijo, una refutación todavía puede pasar inadvertida.

### Por qué el bono hace natural explorar

El bono es ${c\sqrt{\ln N(s)/N(s')}}$, y cada parte tiene una razón:

- **$\sqrt{1/N(s')}$ tiene la forma del margen de un promedio.** Es la misma forma que en Monte Carlo plano: con pocas visitas, $\bar u(s')$ todavía puede estar lejos de lo que valdría con muchas. El bono le da a cada hijo el beneficio de la duda, en proporción a esa duda.
- **$\ln N(s)$ hace crecer el bono de un hijo olvidado.** Si un hijo deja de recibir visitas mientras su padre sigue recibiéndolas, su bono **crece**, despacio. Tarde o temprano supera al de los demás y el hijo vuelve a probarse.
- **$c$ fija cuánto pesa esa duda** frente al promedio.

En un árbol finito, con vueltas sin límite, **ninguna jugada se abandona para siempre**. Las que van mal se prueban cada vez con menos frecuencia, pero se siguen probando.

**Esto es intuición, no garantía.** El margen de Monte Carlo plano pedía simulaciones independientes con una regla fija. En UCT no se cumple:

- **Lo que se juega debajo de un nodo cambia mientras se mide.** Su árbol crece y su selección se mueve, así que el blanco del promedio se desplaza.
- **Cuántas visitas recibe cada hijo depende de los resultados.** La selección decide la vuelta siguiente según lo que ya salió.

El bono sigue la forma del margen, pero ese margen, aquí, no se aplica directo.

### Por qué juega la más visitada

Al acabarse el tiempo o las vueltas, UCT juega la jugada de la raíz con **más visitas $N(s')$**: la regla del **hijo más visitado (*robust child*)**. Ante un empate, juega la primera en el orden dado.

- **Las visitas resumen la búsqueda.** La selección manda una vuelta a un hijo solo si su puntaje es el mayor. Que lo haga muchas veces quiere decir que se probó mucho y siguió viéndose bien.
- **Un promedio alto con pocas visitas puede ser suerte.** Su margen todavía es ancho.
- **Más visitas no demuestran más valor.** También influyen el bono, el orden y los primeros resultados. Con poco presupuesto, la regla puede equivocarse.

| Jugada | Visitas | Promedio |
|---|---|---|
| $a$ | $80$ | $0.5$ |
| $b$ | $20$ | $0.6$ |

UCT juega $a$. El promedio de $b$ descansa en pocas partidas; $b$ podría ser mejor, pero la búsqueda todavía no lo mostró. Si hay una sola jugada óptima y se cumplen las condiciones de convergencia, con suficientes vueltas las dos reglas, por visitas y por promedio, terminan eligiéndola. Elegir por visitas es la convención del curso; el artículo original de UCT usa el mayor promedio.

Queda abierto de dónde sale exactamente la forma del bono y cuánto debe valer $c$: lo contesta [[de-donde-sale-el-bono|De dónde sale el bono]].
