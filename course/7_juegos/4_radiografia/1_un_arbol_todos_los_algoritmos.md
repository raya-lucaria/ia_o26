---
id: un-arbol-todos-los-algoritmos
title: "Radiografía: un árbol, todos los algoritmos"
nav_title: "Radiografía: un árbol, todos los algoritmos"
summary: "Minimax, alfa-beta, expectiminimax, el corte por nivel o por reloj, Monte Carlo plano, Monte Carlo con actualización minimax y UCT, cada uno en una ficha con el mismo orden: qué valor rastrea, cómo explora, qué jugada juega, sus propiedades y sus casos borde. Los siete corren sobre el árbol de resultados y al final se comparan en tablas cortas."
status: ready
estimated_time: 105m
tags: [juegos, busqueda-adversarial, comparacion]
---

# Radiografía: un árbol, todos los algoritmos

Esta página pone lado a lado los siete algoritmos de búsqueda de la unidad. Cada uno tiene una ficha con las mismas partes, **qué valor rastrea, cómo explora, qué jugada juega, sus propiedades y sus casos borde**, y sus figuras sobre el mismo árbol.

**Al final del día, lo que se busca es el valor $V(s)$:** el pago para MAX si los dos juegan lo mejor desde $s$. **Sobre todo, el $Q(s_{\text{raíz}},a)$ de cada jugada de la raíz**, para jugar la mejor. Cada algoritmo trata de **obtenerlo, acotarlo o estimarlo**, y dos terminan con otro número:

- **Minimax** lo calcula exacto.
- **Alfa-beta** lo calcula exacto para la jugada que elige, con menos trabajo; de las demás puede dar solo cotas.
- **Expectiminimax** lo calcula exacto, pero **de otro juego**: uno en el que en D decide un dado.
- **El corte** lo estima: donde se detiene, pone la EVAL.
- **Monte Carlo plano** estima otro número, $Q_{\text{azar}}$: el pago esperado si los dos juegan al azar.
- **Monte Carlo con actualización minimax** simula al azar, pero sube máximos y mínimos; en un árbol finito, converge a $V$.
- **UCT** promedia, pero elige cada vez mejor; en un árbol finito y con vueltas sin límite, se acerca a $V$.

> [!TIP]
> **Míralo correr**
>
> - **▶ [El mismo árbol, todos los algoritmos](../_assets/un_arbol_todos.html)**: elige un algoritmo y mira qué nodos genera, qué jugada entrega y con qué valor.
> - **Las figuras de minimax, alfa-beta, el corte, la quietud y la profundización iterativa se animan:** un halo recorre los nodos en el orden en que el algoritmo los genera y termina en la jugada que juega.

---

## La notación de esta página

Todos los símbolos ya aparecieron en la unidad y están también en [[notacion-juegos|la hoja de notación]].

**El juego**

::: table {#jue-c3-rx-tab-notacion-juego title="Notación: el juego"}
| Símbolo | Qué es |
|---|---|
| $S$, $s$ | Los estados del juego; cada uno incluye el turno |
| $s_0$ | El estado inicial del juego |
| $s_{\text{raíz}}$ | Donde MAX decide: la **raíz** de la búsqueda |
| $\mathrm{Pl}(s)$ | Quién mueve en $s$: MAX, MIN o AZAR |
| $A(s)$ | Las jugadas permitidas en un estado no final |
| $T(s,a)$ | Adonde lleva la jugada $a$: un **hijo** $s'$ |
| $U(s)$ | Pago de un final, desde MAX. Solo en finales |
| $V(s)$ | Pago para MAX si los dos juegan lo mejor desde $s$ |
| $Q(s,a)$ | Lo mismo, si en $s$ se juega $a$ |
| $\Pr(a\mid s)$ | Probabilidad de cada resultado de un nodo AZAR |
| $b$ | El máximo de jugadas permitidas en un estado |
| $m$ | El largo máximo de una partida, en jugadas |
:::

**El pago terminal lo define cada juego, siempre desde MAX.** En este árbol, $U=+1$ si gana MAX, $-1$ si gana MIN y $0$ si empatan; en un final, $V(s)=U(s)$.

**La búsqueda con corte y poda**

::: table {#jue-c3-rx-tab-notacion-busqueda title="Notación: corte y poda"}
| Símbolo | Qué es |
|---|---|
| $\mathrm{EVAL}(s)$ | Estimación de $M\cdot V(s)$ que mira solo $s$ |
| $M$ | Escala de los finales; aquí $M=100$ y $\lvert\mathrm{EVAL}\rvert<M$ |
| $d$ | Las decisiones que quedan, de los dos jugadores |
| $V_d(s)$ | El valor con corte de $s$ cuando quedan $d$ |
| $(\alpha,\beta)$ | La **ventana**: lo que MAX y MIN ya aseguran en el camino |
:::

**La simulación**

::: table {#jue-c3-rx-tab-notacion-simulacion title="Notación: simulación"}
| Símbolo | Qué es |
|---|---|
| $N(s)$ | Cuántas simulaciones o vueltas pasaron por $s$ |
| $N(s,a)$ | Cuántas tomaron la jugada $a$ en $s$ |
| $\widehat Q(s,a)$ | Estimación de $Q(s,a)$, siempre desde MAX |
| $\widehat V(s)$ | Estimación de $V(s)$ |
| $Q_{\text{azar}}$ | Pago esperado si **los dos** juegan al azar; en general no es $Q$ |
| $k$ | Simulaciones por jugada de la raíz, en Monte Carlo plano |
| $n$ | Simulaciones, iteraciones o vueltas **en total** |
| $c>0$ | El peso de explorar en el puntaje de UCT |
| $h$ | La profundidad que alcanzó el árbol de UCT; a lo más $m$ |
:::

**El gorro marca una estimación hecha con partidas simuladas.** Lo que estima depende del algoritmo: en Monte Carlo plano, $Q_{\text{azar}}$; en los otros dos, $Q$. Sin gorro, $V$, $Q$ y $Q_{\text{azar}}$ son valores exactos.

---

## Valor de un estado y valor de una jugada

Como en [[diagnosticar-el-juego|Diagnosticar el juego]] y en [[minimax|Minimax]], dos números se parecen y conviene no confundirlos. **Los dos se miden siempre desde MAX**, mueva quien mueva:

- **El valor de un estado, $V(s)$, es lo que vale estar en $s$:** el pago para MAX si los dos juegan lo mejor desde ahí.
- **El valor de una jugada, $Q(s,a)$, es lo que vale elegir $a$ en $s$**, si después los dos juegan lo mejor.

**Sin azar, el valor de una jugada es el del estado hijo al que lleva**, no el del estado desde donde se elige:

$$
\mathbf{Q(s,a)=V(T(s,a))}
$$

- **Una jugada lleva a un solo hijo**, $T(s,a)$. Elegirla es pasar a ese hijo, así que la jugada vale lo que vale el hijo.
- **El estado vale lo que su mejor jugada para quien mueve.** MAX elige el mayor $Q$ y MIN el menor: $\mathbf{V(s)=\max_{a\in A(s)}Q(s,a)}$ si $\mathrm{Pl}(s)=$ MAX, y el mínimo si es MIN.
- **Una jugada puede valer menos que el estado** desde donde se elige: basta que exista otra mejor.
- **Si decide el azar, el estado promedia.** Con $\mathrm{Pl}(s)=$ AZAR, $V(s)=\sum_a \Pr(a\mid s)\,Q(s,a)$; dibujado el azar como un nodo hijo, la igualdad $Q(s,a)=V(T(s,a))$ sigue valiendo.
- **Dos jugadas que llevan al mismo estado sí valen lo mismo.** Pero un árbol que junte ese estado en un solo nodo mezclaría las visitas de las dos; por eso las estadísticas se guardan por jugada, en la arista.

**Dónde se dibuja el número.** Los cuatro que calculan lo guardan en el nodo hijo mientras lo recorren. Los Monte Carlo lo asocian a la jugada: UCT guarda $N(s,a)$ y $\widehat Q(s,a)$ **por arista**.

**En este árbol cada hijo tiene un solo padre.** Dibujar los datos de una arista junto a $s'=T(s,a)$ es una representación, no otra definición.

**Lo que cambia es qué número pone cada algoritmo en ese lugar.** Minimax guarda $V$; alfa-beta, $V$ o una cota; expectiminimax, el $V$ del juego con dado; el corte, $V_d$ o una cota; los Monte Carlo, una estimación $\widehat Q$. El lugar es el mismo; el significado del número, no.

::: figure {#jue-c3-rx-fig-estado-y-jugada title="El valor de una jugada vive en el hijo al que lleva"}
![Raíz de MAX con dos jugadas, A y B, como aristas hacia sus hijos; el número de cada jugada está dibujado junto al nodo hijo, con la nota «valor de la jugada = valor del hijo». Debajo, cada algoritmo pone ahí un número distinto: V, una cota, el valor con corte o una estimación Q̂](../_assets/jue-c3-rx-estado-y-jugada.svg)
:::

::: table {#jue-c3-rx-tab-que-guarda title="Qué guarda cada algoritmo, dónde y cómo sube"}
| Algoritmo | Qué guarda | Dónde | Cómo sube |
|---|---|---|---|
| Minimax | $V$ | Cada nodo, al recorrerlo | Máximo o mínimo |
| Alfa-beta | $V$ o una cota | Cada nodo, al recorrerlo | Máximo o mínimo, con poda |
| Expectiminimax | $V$ del juego con dado | Cada nodo, al recorrerlo | Máximo, mínimo o suma con $\Pr$ |
| Corte | $V_d$, con quietud, o cota | Cada nodo, al recorrerlo | Máximo o mínimo; EVAL al cortar |
| Monte Carlo plano | $N$ y suma | Jugadas de la raíz | No sube |
| Actualización minimax | $\widehat Q(s,a)=\widehat V(T(s,a))$ | Cada estado descubierto | Máximo o mínimo de lo visitado |
| UCT | $N(s,a)$, $\widehat Q(s,a)$; $N(s)$ | Cada arista de su árbol | Promedio del mismo $U$ |
:::

- **Los cuatro primeros calculan:** el valor de un nodo sale de sus hijos, según quién mueve. Parten de los finales; el corte, además, de la EVAL donde se detiene.
- **Solo expectiminimax promedia entre ellos, y solo donde decide el dado.** Donde decide un jugador, los cuatro toman el máximo o el mínimo.
- **Los tres Monte Carlo usan partidas simuladas hasta un final.** Difieren en qué guardan y en cómo suben lo que vieron.

**Converge a lo que simulas.** Las tres formas de usar simulaciones llegan a números distintos:

::: table {#jue-rx-tab-converge title="Los tres Monte Carlo: a qué converge cada uno"}
| Algoritmo | Qué guarda | Cómo sube | A qué converge |
|---|---|---|---|
| Monte Carlo plano | $N$ y suma por jugada de la raíz | No sube | $Q_{\text{azar}}$ |
| Actualización minimax | $\widehat Q(s,a)$ en cada estado guardado | Máximo o mínimo | $V$ |
| UCT | $N(s,a)$ y $\widehat Q(s,a)$ por arista; $N(s)$ | Promedio del mismo $U$ | $V$ |
:::

- **Monte Carlo plano converge al pago de jugar al azar.** Con simulaciones independientes, la misma regla al azar y sin límite, $\widehat Q$ converge a $Q_{\text{azar}}$: el expectiminimax del juego en que los dos son dados.
- **La actualización minimax converge a $V$ porque sube máximos y mínimos.** Simula igual de al azar, pero en un árbol finito y determinista acaba descubriéndolo todo, y su respaldo es el de minimax.
- **Promediar y después tomar el máximo no basta.** Un promedio del $U$ crudo por jugada sigue estimando $Q_{\text{azar}}$, aunque luego se elija el mayor.
- **UCT converge a $V$ porque elige cada vez mejor, no porque promedie un máximo.** En un árbol finito, con $c>0$ fija y vueltas sin límite, las jugadas peores para quien mueve reciben una fracción de visitas que tiende a cero.
- **Con un presupuesto fijo, ninguno de los tres garantiza $V$.** Las tres convergencias son límites.

::: figure {#jue-rx-fig-tres-mc title="Los tres Monte Carlo en el árbol de resultados"}
![Para cada jugada de la raíz del árbol de resultados, izq, centro y der: su valor exacto V, que es −1, 0 y −1, y su pago con los dos al azar, Q_azar, que es 0, −1/4 y 1/3. Debajo, las estimaciones Q̂ de los tres Monte Carlo con 40 partidas o vueltas y semilla 0: Monte Carlo plano entrega izq y tiende a Q_azar; la actualización minimax y UCT entregan centro y tienden a V](../_assets/jue-c3-tres-mc.svg)
:::

---

## El problema: un juego, dos dibujos

Seis de los siete algoritmos resuelven el mismo problema. **Dado** un estado $s_{\text{raíz}}$ donde mueve MAX y las reglas del juego, **encontrar** una jugada de $A(s_{\text{raíz}})$, lo mejor posible con el tiempo que haya. Expectiminimax resuelve ese problema en otro juego, con un dado en D.

**El primer dibujo es el de cualquier juego.** MAX y MIN se turnan, un nivel cada uno; cada estado tiene a lo más $b$ jugadas, y ninguna partida pasa de $m$. Las hojas son los finales, con su $U$.

::: figure {#jue-c3-rx-arbol-abstracto title="Un juego cualquiera, en abstracto"}
![Árbol abstracto de un juego: la raíz es de MAX, los niveles alternan MAX y MIN, cada nodo tiene hasta b jugadas y las partidas tienen a lo más m jugadas; los puntos suspensivos indican que sigue a lo ancho y a lo hondo, y al fondo están los finales con su U](../_assets/jue-c3-mcg-arbol.svg)
:::

**El segundo dibujo es un juego concreto, el árbol de resultados.** Tiene la forma del árbol base de [[minimax-como-algoritmo|Minimax como algoritmo]]. En la raíz R mueve MAX, con tres jugadas: izq, centro y der. Llevan a I, C y D, donde mueve MIN. Cambia en tres cosas:

- **Sus finales dicen quién gana.** Cada hoja vale $+1$, $-1$ o $0$, y hay un solo empate.
- **Tiene una captura.** La segunda respuesta de MIN en I, ix, captura una pieza; eso importa para la búsqueda de quietud.
- **D tiene tres hijos**, no dos. En total, el árbol tiene 15 nodos.

**Este dibujo no lleva EVAL:** solo las jugadas y los finales en $U$. De los siete algoritmos, solo el corte la necesita, y sus valores van en las figuras de su ficha.

::: figure {#jue-c3-rx-arbol-tpm title="El árbol de resultados: jugadas y finales en U, sin EVAL"}
![El árbol de resultados, con 15 nodos. La raíz R es de MAX; izq lleva a I, centro a C y der a D, los tres de MIN. I tiene los finales i1 = +1 y ix = −1, y ix es una captura. C tiene dos hijos de MAX: C1, con c1a = 0 y c1b = −1, y C2, con c2a = +1 y c2b = −1. D tiene los finales d1 = −1, d2 = +1 y d3 = +1](../_assets/jue-t-pm-arbol.svg)
:::

---

## La EVAL

**Cuando el árbol no cabe, la búsqueda se corta** a cierta profundidad. En cada estado no final donde se detiene, estima su valor con la EVAL, que da $M\cdot V$ aproximado sin mirar debajo; aquí $M=100$.

- **Si un algoritmo usa EVAL, cuenta los finales como $\mathbf{M\cdot U}$.** Una victoria vale $100$, más que cualquier EVAL; una derrota vale $-100$, menos que cualquiera; un empate vale $0$.
- **Funciona porque la EVAL nunca llega a $M$** en valor absoluto: $|\mathrm{EVAL}|<M$.
- **Un final se reconoce antes de cortar.** Aunque ya no quede profundidad, un final vale su $M\cdot U$; nunca se estima.
- **Si un algoritmo no usa EVAL, trabaja directo con $U$**, entre $-1$ y $+1$.

---

## Explorar contra jugar

Los siete hacen lo mismo **en dos tiempos**:

1. **Exploran.** Recorren o construyen una parte del árbol para ponerle **un número a cada jugada de la raíz**.
2. **Juegan.** Con esos números eligen **una sola** jugada de la raíz, y la juegan. Cuando el rival responde, vuelven a empezar desde el estado nuevo.

**Cambia cómo exploran, qué número sale y con qué regla eligen.** El número puede ser $V$ exacto, una cota, el valor con corte o una estimación $\widehat Q$. Por eso cada ficha separa «1 · Exploración» de «2 · Elección».

**Explorar una jugada no obliga a jugarla:** un algoritmo puede gastar trabajo en una jugada poco probada y al final jugar otra.

**El orden y los empates.** Cuando los hijos se recorren en un orden, es el dado, de izquierda a derecha, salvo que la ficha diga otro. Un empate en la raíz lo gana la primera jugada en el orden que usó esa búsqueda.

---

## Lo que suponen: dos jugadores y suma cero

**Todas las fichas suponen dos jugadores, suma cero o constante, turnos y todo a la vista.** La nota dice qué cambia si no; cada ficha cierra sus propiedades con una línea de supuestos.

::: remark {#jue-rx-nota-suma-cero title="Suma cero, suma no constante y más jugadores"}
**«MIN minimiza lo de MAX» solo vale con dos jugadores y suma cero o constante.** Entonces cada final tiene un solo número, y el $-1$ de MAX es el mejor final para MIN.

- **Dos jugadores, suma no constante.** Cada final lleva un vector $(U_1,U_2)$. El segundo jugador maximiza $U_2$, que no necesariamente es minimizar $U_1$.
- **Más jugadores: max$^n$** (Luckhardt e Irani, 1986). Cada final lleva $(U_1,\dots,U_n)$; quien mueve elige el hijo con su componente más alta y copia el vector completo.
- **Lo que da max$^n$.** En árboles finitos, por turnos y con todo a la vista, da un equilibrio, con una regla de desempate fija. No da la garantía escalar de minimax.
- **Alfa-beta ordinaria no se traslada.** Con cotas por jugador y sobre la suma solo queda una **poda superficial** (Korf, 1991), sin el ahorro asintótico.
- ***Paranoid*, el paranoico** (Sturtevant y Korf, 2000), junta a los rivales en una coalición MIN y recupera alfa-beta. A cambio, resuelve un juego más pesimista que el real.
- **UCT con vectores** guarda un promedio por jugador, y cada quien selecciona por el suyo. Puede dar equilibrios mixtos (Sturtevant, 2008, con sus condiciones).
:::

---

## Las siete fichas

### Minimax

Es la búsqueda exacta para juegos de dos jugadores por turnos, de suma cero, sin azar, con todo a la vista y con árbol finito. **Recorre el árbol completo hasta los finales y sube los resultados**: cada nodo vale lo que MAX puede asegurar desde ahí.

- **Qué valor rastrea:** el de cada estado, $V(s)$. El de una jugada es el de su hijo: $Q(s,a)=V(T(s,a))$.
- **Dónde lo guarda:** en cada nodo, mientras lo recorre. Al cerrarlo, entrega el número a su padre y lo descarta.
- **Cómo sube:** con el máximo o el mínimo de los hijos, según quién mueve; nunca con un promedio.
- **A qué converge:** no necesita converger. En un árbol finito, al terminar, cada número es exacto.

#### 1 · Exploración: cómo construye su estimación

Minimax no estima: **calcula el valor exacto de cada jugada de la raíz** con el árbol del juego entero. Antes de recorrerlo conviene separar dos números:

- **El pago de un final, $U(s)$, lo dan las reglas:** aquí $U=+1$ si gana MAX, $-1$ si gana MIN y $0$ si empatan.
- **El valor de un nodo, $V(s)$, es lo que MAX puede asegurar desde $s$** si MIN responde siempre lo peor para MAX. Si MIN se equivoca, MAX puede obtener más; nunca menos.

##### Los pasos

El recorrido es **en profundidad** (*depth-first search*), con los hijos en el orden dado, de izquierda a derecha:

1. **Bajar.** Desde la raíz, genera las jugadas legales del nodo y baja por la primera. Repite en cada nodo nuevo hasta llegar a un final del juego.
2. **Valorar el final.** Un final no se calcula: su valor es su pago, $V(s)=U(s)$.
3. **Subir el valor (*backup*).** Regresa al padre con el valor del hijo y lo compara con lo mejor que llevaba. Si al padre le quedan jugadas sin revisar, baja por la siguiente.
4. **Cerrar el nodo.** Con todos sus hijos revisados, el valor del padre queda fijo y sube a su propio padre. **Ningún nodo se valora antes de conocer todos sus hijos.**

##### La regla

**La regla para valorar un nodo.** Los finales dan el punto de partida; los demás nodos toman su valor de sus jugadas, con $Q(s,a)=V(T(s,a))$:

| Nodo | Su valor |
|---|---|
| Final | $\mathbf{V(s)=U(s)}$ |
| $\mathrm{Pl}(s)=$ MAX | $\mathbf{V(s)=\max_{a\in A(s)} Q(s,a)}$ |
| $\mathrm{Pl}(s)=$ MIN | $\mathbf{V(s)=\min_{a\in A(s)} Q(s,a)}$ |

Donde mueve MIN se toma el mínimo: es la respuesta más desfavorable para MAX.

Cada parte tiene su papel:

- **El pago $U(s)$ detiene la cuenta:** al llegar a un final ya no hay nada que calcular.
- **El máximo es la decisión de MAX:** se queda con la jugada que más le asegura, después de revisar **todas** las de $A(s)$.
- **El valor del hijo ya incluye las respuestas que vienen después:** no basta con que haya un final favorable debajo de una jugada.
- **$V$ aparece a los dos lados del igual:** la regla se usa a sí misma, y por eso se calcula de abajo hacia arriba. **El signo no cambia al subir:** todo se mide desde MAX.

##### Ejemplo

**Ejemplo en un nodo de MAX.** Tiene dos hijos de MIN, cada uno con dos finales debajo.

| Jugada de MAX | Finales debajo | $Q$ de la jugada |
|---|---|---|
| $a$ | $+1$ y $-1$ | $-1$ |
| $b$ | $0$ y $0$ | $0$ |

MAX juega $b$ y asegura el empate, aunque debajo de $a$ haya una victoria: MIN nunca lo dejaría llegar a ella. Los dos pares de finales promedian $0$, y aun así sus valores son distintos. Si los finales de $a$ fueran $+1$ y $+1$, $a$ valdría $+1$ y MAX jugaría $a$. **Decide lo que MAX puede asegurar, no el mejor final que hay debajo ni el promedio.**

##### Al terminar

Al terminar el recorrido, minimax generó **todos los nodos del árbol** y la raíz conoce el valor exacto de cada una de sus jugadas. No tuvo que conservar el árbol entero en memoria: cada nodo cerrado se descarta en cuanto entrega su valor.

#### 2 · Elección: qué jugada juega

**Cuando la raíz cerró todas sus jugadas**, juega la de **mayor $Q$**. Si varias empatan, juega **la primera en el orden dado**: solo cambia de jugada cuando otra vale estrictamente más.

| Decisión | Qué compara | Cuándo |
|---|---|---|
| Exploración: valorar cada nodo | $Q$ de sus jugadas | Durante el recorrido |
| Elección: qué jugar | $Q$ de cada jugada de la raíz | Al cerrar la raíz |

Aquí explorar y elegir usan **el mismo número**. La elección es la regla del máximo aplicada una vez más, en la raíz, guardando además qué jugada lo alcanzó.

#### 3 · Propiedades

- **Número que da:** el valor exacto $Q$ de **cada** jugada de la raíz. No es una estimación ni una cota.
- **Usa EVAL:** no. Siempre llega a los finales, así que le basta $U$. Trabaja en la escala de $U$, sin la $M$.
- **Garantía:** sí. Entrega el $V$ de la raíz y una jugada que lo alcanza: contra un MIN que juega bien obtiene exactamente $V$, y contra cualquier otro, al menos $V$.
- **Se puede interrumpir (*anytime*):** no. Hasta cerrar la raíz no tiene una jugada fiable: una jugada que aún no revisó puede valer más que todas las anteriores.
- **Complejidad en tiempo:** sean $b$ las jugadas máximas por nodo y $m$ el largo máximo de una partida. Genera hasta $1+b+b^2+\dots+b^m$ nodos: tiempo $O(b^m)$.
- **Complejidad en memoria:** solo guarda el camino de la raíz al nodo actual, a lo más $m$ niveles con hasta $b$ jugadas pendientes cada uno: $O(bm)$.
- **Frente a los demás:** es la referencia, y su costo exponencial es lo que obliga a buscar otros. Otro algoritmo puede conservar su $V$ con menos trabajo, estimarlo, o estimar un número distinto.
- **Supuestos:** dos jugadores, suma cero o constante, sin azar. Con más jugadores, el análogo es max$^n$ (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Empate:** todas las jugadas empatadas son óptimas; juega la primera en el orden dado.
- **Una sola jugada:** queda forzada, y $V(s)=Q(s,a)$.
- **Final ya en el árbol, o la raíz misma final:** vale su $U$ y no genera hijos.
- **Finales a distintas profundidades:** no prefiere ganar pronto ni perder tarde, salvo que $U$ lo codifique.

::: figure {#jue-c3-rx-fig-minimax title="Minimax en el árbol de resultados: genera los 15 nodos y juega centro"}
![Minimax en el árbol de resultados: genera los 15 nodos; I vale −1, C vale 0 y D vale −1, así que la raíz vale 0 y juega centro](../_assets/jue-c3-rx-minimax.svg)
:::

::: figure {#jue-c3-rx-fig-flujo-minimax title="Minimax, en palabras"}
![Diagrama de flujo de minimax: baja un nivel; si es final, vale U; si quedan jugadas, baja por la siguiente; al subir, MAX toma el mayor; al final juega la jugada de mayor valor](../_assets/jue-c3-rx-flujo-minimax.svg)
:::

---

### Alfa-beta

Es minimax con poda (*alpha-beta pruning*). **Hace el mismo recorrido, pero deja de generar una rama** en cuanto lo ya revisado basta para saber que no cambia la jugada de la raíz. Con el mismo orden y desempate, entrega la misma jugada y el mismo $V$ que minimax, y puede generar menos nodos.

- **Qué valor rastrea:** el mismo $V(s)$ que minimax, con $Q(s,a)=V(T(s,a))$. Un nodo afectado por una poda devuelve solo una cota: «al menos» o «a lo más».
- **Dónde lo guarda:** en cada nodo que genera, mientras lo recorre, junto con la ventana $(\alpha,\beta)$ del camino.
- **Cómo sube:** con el máximo o el mínimo de los hijos, como minimax, pero deja de generar hijos que ya no pueden cambiar la jugada de la raíz.
- **A qué converge:** no necesita converger. Al terminar, la jugada elegida trae su $V$ exacto.

#### 1 · Exploración: cómo construye su estimación

Alfa-beta recorre el árbol del juego **en profundidad, hijo por hijo y en el orden dado**, como minimax. Cuando llega a un final del juego, devuelve su $U$.

##### La ventana

**Cada nodo lleva dos números de lo que ya pasó arriba**, en el camino desde la raíz. Los dos se miden desde MAX, como $U$:

- **$\alpha$ («alfa») es un piso:** lo mejor que **MAX ya tiene asegurado** en algún nodo suyo del camino, con una jugada ya revisada.
- **$\beta$ («beta») es un techo:** lo mejor que **MIN ya tiene asegurado** en algún nodo suyo del camino. MIN puede evitar cualquier cosa mejor para MAX.

El par $(\alpha,\beta)$ se llama **ventana**. En la raíz empieza en $(-\infty,+\infty)$: todavía no hay nada asegurado.

**La ventana resume alternativas del camino; no acota por sí sola el valor del nodo actual.** Lo que asegura el número que devuelve un nodo se lee contra la ventana con la que entró.

##### Los pasos

En cada nodo de MAX que no es final, el recorrido sigue estos pasos:

1. **Empezar.** Recibe la ventana que tiene su padre en ese momento y empieza con $v=-\infty$. En $v$ guardará el mayor número que le devuelvan sus hijos.
2. **Bajar al siguiente hijo.** Lo genera, lo explora con la ventana actual y recibe el número $w$ que devuelve. Actualiza $v$ con $\max(v,w)$.
3. **Podar.** Compara $v$ con $\beta$. Si $v\ge\beta$, **deja de generar sus hijos restantes** y devuelve $v$.
4. **Subir el piso.** Si no poda, sube $\alpha$ a $\max(\alpha,v)$ y pasa al siguiente hijo. Su $\beta$ no cambia.
5. **Regresar.** Al terminar sus hijos, devuelve $v$. **Al padre solo sube ese número:** la ventana que el nodo modificó se pierde, y el padre sigue con la suya.

##### La regla

**La regla de poda en un nodo de MAX:**

$$
\mathbf{v\ge\beta\;\Rightarrow\;\text{no genera sus hijos restantes}}
$$

- **$v$ es el mayor número que le han devuelto sus hijos revisados.** Cuando llega a $v\ge\beta$, el nodo vale **al menos $v$**, sin importar los hijos que faltan.
- **Antes de eso, $v$ no es todavía un valor asegurado:** puede venir de la cota superior de un hijo afectado por una poda.
- **$\beta$ es lo que MIN ya tiene asegurado más arriba, con otra jugada.** Si este nodo ya vale $v\ge\beta$, MIN nunca dejaría que la partida llegara aquí.
- **Los hijos que faltan no cambian eso:** solo podrían subir $v$, y un $v$ más alto le da a MIN todavía más razones para no venir.
- **El igual también poda:** con $v=\beta$, a MIN le da lo mismo, así que esta rama tampoco cambia la jugada de arriba.

Éste es el **corte beta**: se llama como el número que lo provoca. En MIN, $v$ empieza en $+\infty$, guarda el menor número recibido y la regla cambia de papeles:

| Mueve | Poda si | Nombre | Si no poda |
|---|---|---|---|
| MAX | $\mathbf{v\ge\beta}$ | Corte beta | $\alpha\leftarrow\max(\alpha,v)$ |
| MIN | $\mathbf{v\le\alpha}$ | Corte alfa | $\beta\leftarrow\min(\beta,v)$ |

**Lo podado no se genera:** ni sus estados ni sus jugadas legales. De ahí sale el ahorro.

##### Qué significa lo que devuelve

**El número $w$ que devuelve un nodo se lee contra la ventana con la que entró**, $(\alpha_0,\beta_0)$, con $\alpha_0<\beta_0$:

| Lo que devuelve | Qué asegura |
|---|---|
| $w\le\alpha_0$ | $V\le w$: «a lo más» |
| $\alpha_0<w<\beta_0$ | $V=w$: exacto |
| $w\ge\beta_0$ | $V\ge w$: «al menos» |

**No podar en un nodo no garantiza que su número sea exacto:** una poda en un descendiente pudo dejarle solo una cota. Lo que decide es dónde cae $w$ respecto de la ventana de entrada.

##### Ejemplo

**Ejemplo en un nodo de MAX, con pagos cualquiera** (un juego cuyo $U$ va de $0$ a $10$). Llega con $\beta=4$: más arriba, MIN ya tiene una jugada que le da $4$.

| Caso | 1.er hijo | ¿Poda? | Devuelve |
|---|---|---|---|
| $a$ | $6$ | Sí: $6\ge 4$ | $6$: «$\ge 6$» |
| $b$ | $4$ | Sí: $4\ge 4$ | $4$: «$\ge 4$» |
| $c$ | $3$ | No: $3<4$ | Sigue con el segundo |

- **En el caso $a$, el segundo hijo no se genera.** Podría valer mucho más y a MAX le encantaría, pero MIN ya escogió no venir aquí.
- **El $6$ que sube no es el valor exacto del nodo, es una cota inferior:** el nodo vale al menos $6$. Al padre de MIN le basta, porque se queda con su $4$ de todos modos.
- **En el caso $c$ todavía no se sabe:** el segundo hijo podría subir $v$ hasta $4$ o más.

**Decide la comparación con $\beta$, no qué tan grande es el número.**

##### Qué se repite

**Al repetir, unas ramas quedan sin generar** y otras se revisan hasta los finales. Los cortes beta devuelven cotas inferiores («al menos»); los cortes alfa, cotas superiores («a lo más»).

**La raíz es de MAX y no tiene rival arriba:** su $\beta$ es $+\infty$, así que **revisa todos sus hijos**. Las podas ocurren dentro de sus ramas, y su $\alpha$ sube cada vez que encuentra una jugada mejor.

#### 2 · Elección: qué jugada juega

**Al terminar el recorrido**, juega la jugada de la raíz con **el mayor número devuelto**, igual que minimax. La raíz cambia de jugada solo cuando el número $w$ de un hijo supera estrictamente a su $\alpha$: **$w>\alpha$**. Ante un empate, conserva la primera en el orden dado.

| Decisión | Compara | Regla |
|---|---|---|
| Poda en un nodo de MAX | $v$ con $\beta$ | $\mathbf{v\ge\beta}$ |
| Elección en la raíz | $w$ con $\alpha$ | $\mathbf{w>\alpha}$ |

**La comparación estricta también protege la elección:** un número que empata con $\alpha$ puede ser solo una cota superior. Esa jugada podría valer menos de lo que devolvió, y no debe desplazar a la elegida.

**La jugada elegida trae su $V$ exacto.** Las demás pueden traer su valor exacto o solo una cota superior, suficiente para saber que no la superan. Con el mismo orden y desempate, la jugada coincide con la de minimax: la poda quita trabajo, no cambia la respuesta.

#### 3 · Propiedades

- **Número que da:** el $Q$ exacto **de la jugada elegida**. De las demás jugadas de la raíz puede dar solo cotas («a lo más $w$»), suficientes para descartarlas.
- **Usa EVAL:** no. Llega hasta los finales y trabaja en la escala de $U$, sin la $M$.
- **Garantía:** sí, en la raíz. En un árbol finito, al terminar da el mismo $V$ y la misma jugada que minimax, con el mismo orden y desempate.
- **Se puede interrumpir (*anytime*):** no. Si se interrumpe a medio recorrido no garantiza haber visto la mejor jugada.
- **Complejidad:** **con el mismo orden, nunca genera más nodos que minimax, pero puede generar los mismos.** El tiempo va de $O(b^{m/2})$ con **orden perfecto** —la mejor jugada para quien mueve siempre primero— a $O(b^m)$ con el peor orden.
- **Memoria:** $O(bm)$. Guarda el camino actual y las jugadas de sus nodos, igual que minimax.
- **Frente a minimax:** la misma respuesta, con menos trabajo o, en el peor caso, el mismo. Con orden perfecto revisa del orden de $b^{m/2}$ nodos en lugar de $b^m$; con corte, eso permite mirar cerca del doble de hondo en el mismo tiempo.
- **Supuestos:** los de minimax. Con más jugadores no se traslada; solo queda una poda superficial (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Empate en la raíz:** la regla estricta $w>\alpha$ conserva la primera jugada empatada, como minimax.
- **El igual en un nodo interno poda:** $v=\beta$ ya no cambia la jugada de arriba.
- **Un final entre los primeros hijos** puede provocar la poda de inmediato, si su $U$ alcanza la ventana.
- **El orden decide el ahorro, no la respuesta:** con el peor orden genera los mismos nodos que minimax.

::: figure {#jue-c3-rx-fig-alfa-beta title="Alfa-beta en el árbol de resultados: 12 de 15 nodos, la misma jugada"}
![Alfa-beta en el árbol de resultados con el orden dado: genera 12 de 15 nodos. Poda c2b porque C2 ya vale al menos +1, que es mayor o igual que beta = 0, y poda d2 y d3 porque D ya vale a lo más −1, que es menor o igual que alfa = 0. Juega centro, como minimax](../_assets/jue-c3-rx-alfa-beta.svg)
:::

::: figure {#jue-c3-rx-fig-flujo-alfa-beta title="Alfa-beta, en palabras"}
![Diagrama de flujo de alfa-beta: el de minimax con una pregunta más, si v es mayor o igual que beta; si lo es, poda y no genera los hijos restantes](../_assets/jue-c3-rx-flujo-alfa-beta.svg)
:::

---

### Expectiminimax: otro juego, con un dado en D

**Esta ficha resuelve otro juego:** el árbol de resultados con un dado parejo de tres caras en D, en vez de MIN. Las otras seis no tienen azar. Expectiminimax es minimax con nodos AZAR: **donde decide un jugador, toma el máximo o el mínimo; donde decide el dado, promedia** con las probabilidades del juego.

- **Qué valor rastrea:** el $V(s)$ del juego con dado: el pago esperado para MAX si los dos juegan lo mejor. Sigue valiendo $Q(s,a)=V(T(s,a))$.
- **Dónde lo guarda:** en cada nodo, mientras lo recorre, como minimax.
- **Cómo sube:** con el máximo en MAX, el mínimo en MIN y la suma pesada por $\Pr(a\mid s)$ en AZAR.
- **A qué converge:** no necesita converger. Es una esperanza exacta, calculada con las probabilidades del juego, no un promedio de muestras.

#### 1 · Exploración: cómo construye su estimación

**Recorre el árbol entero en profundidad, como minimax.** La única diferencia está en los nodos donde decide el azar.

##### Los pasos

1. **Bajar.** Genera las jugadas del nodo y baja por la primera, hasta un final.
2. **Valorar el final.** Su valor es su pago, $V(s)=U(s)$.
3. **Subir el valor.** En MAX y en MIN, compara con lo mejor que llevaba, como minimax. En AZAR, suma el valor del hijo multiplicado por su probabilidad.
4. **Cerrar el nodo.** Un nodo AZAR necesita **todos** sus hijos: falta cualquiera y la suma puede cambiar.

##### La regla

| Nodo | Su valor |
|---|---|
| Final | $\mathbf{V(s)=U(s)}$ |
| $\mathrm{Pl}(s)=$ MAX | $\mathbf{V(s)=\max_{a} Q(s,a)}$ |
| $\mathrm{Pl}(s)=$ MIN | $\mathbf{V(s)=\min_{a} Q(s,a)}$ |
| $\mathrm{Pl}(s)=$ AZAR | $\mathbf{V(s)=\sum_{a} \Pr(a\mid s)\,Q(s,a)}$ |

- **$\Pr(a\mid s)$ la dan las reglas:** es la probabilidad de cada cara del dado. No son negativas y suman $1$.
- **La suma es una esperanza, $E[\cdot]$:** el pago promedio que MAX puede esperar si en ese nodo decide el dado.
- **Los jugadores siguen eligiendo:** el máximo y el mínimo no cambian.

##### Ejemplo

**Ejemplo: el mismo par de finales, $+1$ y $-1$, debajo de dos nodos distintos.**

| Quién decide | Su valor |
|---|---|
| MIN | $-1$ |
| Un volado parejo | $(+1-1)/2=0$ |

MIN elige la derrota de MAX; el volado no elige, se promedia. **Donde decide un rival se toma el mínimo; donde decide el azar, el promedio.**

#### 2 · Elección: qué jugada juega

**Al cerrar la raíz**, juega la jugada de **mayor $Q$**, ahora un pago esperado. Ante un empate, la primera en el orden dado.

| Decisión | Qué compara | Cuándo |
|---|---|---|
| Exploración: valorar cada nodo | $Q$, o su suma pesada en AZAR | Durante el recorrido |
| Elección: qué jugar | $Q$ esperado de cada jugada | Al cerrar la raíz |

**En el árbol de resultados con dado, D vale $(-1+1+1)/3=1/3$.** Es más que el $0$ de centro y que el $-1$ de I, así que expectiminimax juega **der**, con valor $1/3$, y genera los 15 nodos.

**El $1/3$ es exacto, pero de otro juego.** No corrige a minimax: en el árbol de resultados decide MIN en D, y der vale $-1$. Por eso D tiene tres hijos: con dos, el dado nunca cambiaba la jugada.

#### 3 · Propiedades

- **Número que da:** el valor **esperado** exacto de cada jugada de la raíz, calculado con las $\Pr$ del juego. No es una estimación.
- **Usa EVAL:** no. Trabaja en la escala de $U$, y **aquí la escala importa**: solo un cambio afín positivo de $U$, como $2U+1$, conserva siempre la jugada.
- **Garantía:** el mayor pago esperado contra un MIN que juega lo mejor y un dado con esas $\Pr$. No garantiza el resultado de una partida.
- **Se puede interrumpir (*anytime*):** no. Como minimax, necesita cerrar la raíz.
- **Complejidad:** tiempo $O(b^m)$, donde $b$ cuenta también los resultados del azar y $m$, las tiradas; memoria $O(bm)$. Sin cotas conocidas de $U$, en un nodo AZAR no se poda: falta un hijo y el promedio puede moverse.
- **Frente a minimax:** si todas las $\Pr$ valen $0$ o $1$, es minimax.
- **Frente a Monte Carlo plano:** Monte Carlo plano estima por muestreo el expectiminimax de un juego donde **todos** son azar: eso es $Q_{\text{azar}}$.
- **Supuestos:** dos jugadores de suma cero, más el azar con probabilidades conocidas (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Un dado con una sola cara** es una jugada forzada: su nodo AZAR vale lo que su único hijo.
- **Probabilidades que no suman $1$** no describen un dado: la suma deja de ser una esperanza.
- **Un cambio de escala no afín** puede cambiar la jugada, aunque conserve el orden de los finales. Aquí, con pagos $\pm1$ y $0$, elevar al cubo no cambia nada; en un juego con otros pagos, sí puede.
- **Empate y finales a distintas profundidades:** como en minimax.

::: figure {#jue-rx-fig-expectiminimax title="Expectiminimax en el árbol de resultados con un dado en D: juega der"}
![El árbol de resultados con D como nodo de azar, con esquinas redondas y probabilidad 1/3 en cada hijo. I vale −1, C vale 0 y D vale el promedio (−1 + 1 + 1)/3 = 1/3, así que la raíz vale 1/3 y juega der](../_assets/jue-rx-expectiminimax.svg)
:::

::: figure {#jue-rx-fig-flujo-expectiminimax title="Expectiminimax, en palabras"}
![Diagrama de flujo de expectiminimax: el de minimax con una pregunta más, si el nodo es de azar; si lo es, suma la probabilidad de cada hijo por su valor](../_assets/jue-rx-flujo-expectiminimax.svg)
:::

---

### Minimax con corte: por nivel o por reloj

Es minimax que deja de bajar al agotarse la profundidad y **usa EVAL para estimar donde se detiene**. Por nivel, fija cuánto mirar; por reloj, repite búsquedas cada vez más profundas mientras quede tiempo.

- **Qué valor rastrea:** el valor con corte $V_d(s)$: el de minimax en el árbol cortado, con EVAL donde se detiene. Con quietud, el valor con quietud; con poda, algunos son solo cotas.
- **Dónde lo guarda:** en cada nodo, mientras lo recorre, hasta la profundidad del corte. Solo la búsqueda de quietud, que sigue capturas, puede pasar de ahí.
- **Cómo sube:** con el máximo o el mínimo de los hijos, como minimax; en los nodos de corte, el número de partida es la EVAL.
- **A qué converge:** no es un promedio que converja. Es exacto para el árbol cortado, y coincide con $M\cdot V$ si la profundidad alcanza los finales sin aplicar EVAL ni activar la quietud.

#### 1 · Exploración: cómo construye su estimación

Recorre el árbol en profundidad y distingue dos clases de hojas:

- **Final del juego:** ya tiene pago. Vale $M\cdot U$: con $M=100$, $+100$ si gana MAX, $-100$ si gana MIN y $0$ si empatan.
- **Nodo de corte (*cutoff*):** no es final, pero ya no queda profundidad. Vale su EVAL, que estima $M\cdot V$ mirando la posición, sin generar sus hijos.

Como $|\mathrm{EVAL}|<M$, una victoria confirmada vale más que cualquier estimación y una derrota confirmada vale menos.

##### Por nivel

**Por nivel (*depth-limited search*).** La raíz empieza con una profundidad fija $d\ge1$. En cada nodo sigue estos pasos:

1. **Comprobar el final (*terminal test*).** Primero revisa si la partida terminó. Si terminó, devuelve $M\cdot U$, aunque ya no quede profundidad.
2. **Aplicar el corte.** Si el nodo no es final y $d=0$, devuelve EVAL y no genera hijos.
3. **Expandir.** Si queda profundidad, genera y valora los hijos en el orden dado. Cada hijo recibe $d-1$.
4. **Subir el valor.** Al terminar de valorar los hijos, un nodo de MAX devuelve el mayor valor.

##### La regla

**La regla del corte.** $V_d(s)$ es el **valor con corte** de $s$ cuando quedan $d$ decisiones: el de minimax en el árbol cortado, con EVAL en sus hojas no finales. Los casos se revisan en este orden:

| Nodo | Valor con corte |
|---|---|
| Final | $\mathbf{V_d(s)=M\cdot U(s)}$ |
| No final, $d=0$ | $\mathbf{V_0(s)=\mathrm{EVAL}(s)}$ |
| MAX, $d\ge1$ | $\mathbf{V_d(s)=\max_{a\in A(s)}V_{d-1}(T(s,a))}$ |
| MIN, $d\ge1$ | $\mathbf{V_d(s)=\min_{a\in A(s)}V_{d-1}(T(s,a))}$ |

Cada parte tiene su papel:

- **La profundidad cuenta lo que queda.** Cada jugada consume un nivel, sea de quien sea; con $d=1$ en la raíz, sus hijos ya llegan con $d=0$.
- **La transición lleva al hijo.** $T(s,a)$ es la posición que deja la jugada $a$; se valora con un nivel menos.
- **El máximo y el mínimo conservan la regla de minimax.** Cambia dónde se detiene la búsqueda, pero todos los valores siguen medidos desde MAX.
- **Si alcanza todos los finales, devuelve $M\cdot V(s)$**, no $V(s)$: la escala es la de la EVAL.

##### Ejemplo

**Ejemplo en un nodo de MAX con $d=1$.**

| Hijo | Tipo | Valor |
|---|---|---|
| $a$ | No final | EVAL $40$ |
| $b$ | Final: gana MAX | $100$ |

Elige $b$. Si revisara primero la profundidad y evaluara ese final con $30$, elegiría $a$ y dejaría pasar una victoria. Además, el $40$ de $a$ podría ocultar una derrota detrás del corte. **Un final se reconoce antes de evaluar; una EVAL es una estimación, no un resultado.**

##### Con poda

**Con poda es alfa-beta con corte.** Aplica las mismas cotas $\alpha$ y $\beta$ al árbol cortado y da el mismo valor en la raíz. Con el mismo orden de hijos, nunca genera más nodos que minimax con corte, aunque puede generar los mismos.

##### Por reloj

**Por reloj: profundización iterativa (*iterative deepening*).** Repite búsquedas de alfa-beta con corte con $d=1,2,3,\dots$:

1. **Guardar un respaldo.** Antes de buscar, guarda la primera jugada legal. Así tiene algo que entregar si no alcanza a terminar la primera búsqueda.
2. **Buscar con la profundidad actual.** Empieza desde la raíz y prueba primero la jugada guardada; después, las demás en el orden dado. Si la primera es buena, sube $\alpha$ pronto y permite podar más.
3. **Revisar el reloj.** Lo revisa antes de cada búsqueda y después de valorar cada hijo de la raíz, **sin interrumpir la exploración de ese hijo**. Si se acabó, descarta la búsqueda en curso y entrega la jugada guardada.
4. **Reconocer una victoria.** Si un hijo devuelve $+M$, entrega esa jugada de inmediato: ninguna EVAL alcanza $M$, así que demuestra una victoria dentro de la profundidad buscada.
5. **Guardar y profundizar.** Si termina la búsqueda, guarda su mejor jugada, aumenta $d$ en uno y vuelve a empezar.

**El límite de tiempo no es estricto:** si el subárbol de un hijo tarda, la respuesta llega después del plazo.

##### Horizonte y quietud

- **Efecto horizonte (*horizon effect*): una consecuencia decisiva queda justo detrás del corte y la estimación engaña.** Aumentar $d$ mueve el horizonte, pero no elimina el problema.
- **Búsqueda de quietud (*quiescence search*): prolonga la búsqueda desde los nodos de corte que todavía tienen capturas.** Una posición es quieta si quien mueve no tiene capturas.
- **En cada posición no quieta, MAX compara quedarse con su EVAL contra seguir cada captura.** Solo genera capturas, hasta posiciones quietas o finales; en MIN se toma el menor valor, medido desde MAX.
- **Quedarse se llama *stand pat*:** es una aproximación, no una jugada legal.

**Por ejemplo, con EVAL $20$.** Si una captura llega a una posición quieta con EVAL $50$, MAX la sigue y el nodo vale $50$. Si la única captura lleva a $-10$, MAX se planta y el nodo vale $20$.

**Ese $20$ supone que MAX tiene alguna jugada sin captura que lo conserve.** Si todas las que tiene pierden, el $20$ es demasiado optimista.

**El resultado es el valor con quietud.** Solo garantiza $M\cdot V$ si la búsqueda llega a los finales antes de activar la quietud: aun si todas las capturas llegan a finales, quedarse puede alterar el resultado. Además, ya no está limitada a $d$; una cadena de capturas puede alcanzar el final de la partida.

#### 2 · Elección: qué jugada juega

**Por nivel**, al terminar juega la jugada de la raíz con **mayor valor con corte**.

**Por reloj**, al vencer el plazo juega la de la **última búsqueda completa**; si no terminó ninguna, entrega el respaldo.

| Versión | Qué jugada entrega | Cuándo |
|---|---|---|
| Por nivel | Mayor valor con corte | Al terminar |
| Por reloj | Última búsqueda completa | Al vencer el plazo |
| Por reloj, con $+M$ | Esa jugada | Al encontrarla |

En ambos casos, ante empate conserva la primera jugada **en el orden de esa búsqueda**: solo cambia si otra devuelve un valor estrictamente mayor. Por reloj, la mejor anterior va primero y conserva los empates.

**La salida con $+M$ no rompe la regla:** ya demostró una victoria, y ninguna otra jugada puede superarla.

#### 3 · Propiedades

- **Número que da:** sin poda, el valor con corte de cada jugada de la raíz: exacto para el árbol cortado, estimación de $M\cdot V$ del juego completo. Con alfa-beta, el de la jugada elegida es exacto para ese árbol; los demás pueden ser cotas.
- **Usa EVAL:** sí, en los nodos de corte. Los finales se valoran con $M\cdot U$, en la misma escala.
- **Garantía:** en general no garantiza $V$. Si la profundidad alcanza los finales sin aplicar EVAL, el valor con corte coincide con $M\cdot V$; por reloj, cuenta la profundidad de la última búsqueda completa.
- **Se puede interrumpir (*anytime*):** por nivel, no. Por reloj, sí: tiene un respaldo legal desde el principio y una jugada respaldada por una búsqueda completa desde que termina $d=1$.
- **Complejidad:** sin quietud, el tiempo es $O(b^d)$ sin poda, y con alfa-beta va de $O(b^{d/2})$ con orden perfecto a $O(b^d)$. La memoria es $O(bd)$, sin tabla de transposición.
- **Complejidad por reloj:** si cada búsqueda cuesta $B>1$ veces la anterior, todas juntas cuestan aproximadamente $B/(B-1)$ veces la última. Con $B=10$, repetir añade cerca de un 11 %; con $B=2$, casi el doble; se suma lo gastado en la búsqueda descartada.
- **Complejidad con quietud:** el peor caso alcanza tiempo $O(b^m)$ y memoria $O(bm)$.
- **Frente a minimax y alfa-beta sin corte:** permite buscar cuando no alcanza para llegar a los finales. A cambio, la decisión depende de la calidad de EVAL y de la profundidad alcanzada.
- **Supuestos:** los de minimax. Con más jugadores harían falta pagos y EVAL vectoriales (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Un final con $d=0$:** vale $M\cdot U$, no su EVAL; por eso el final se revisa primero.
- **Finales a distintas profundidades:** el que cae antes del corte vale $M\cdot U$; el que queda detrás, no se ve.
- **El reloj vence antes de terminar $d=1$:** entrega el respaldo, la primera jugada legal.
- **El *stand pat* con jugada obligada:** si quien mueve está obligado a capturar, quedarse puede ocultar su única jugada legal.

**En las figuras de esta ficha, el árbol de resultados lleva una EVAL inventada:** I $60$, C $20$ y D $10$; con $d=2$, también C1 $10$ y C2 $50$. La de I es mala a propósito: no ve que la captura ix pierde.

::: figure {#jue-c3-rx-fig-corte title="Corte a d = 1 en el árbol de resultados: 4 nodos, juega izq"}
![Minimax con corte a profundidad 1 en el árbol de resultados: genera la raíz y sus tres hijos, que valen su EVAL, 60, 20 y 10; juega izq, aunque detrás del horizonte está la captura ix, que pierde](../_assets/jue-c3-rx-corte.svg)
:::

::: figure {#jue-c3-rx-fig-quietud title="Búsqueda de quietud a d = 1 en el árbol de resultados: juega centro"}
![Búsqueda de quietud a profundidad 1 en el árbol de resultados: I no es quieto, así que MIN compara su EVAL, 60, con la captura ix, que vale −100, y toma el menor, −100; genera 5 nodos y juega centro, con 20](../_assets/jue-c3-rx-quietud.svg)
:::

::: figure {#jue-c3-rx-fig-iterativa title="Profundización iterativa en el árbol de resultados: d = 1, 2, 3"}
![Profundización iterativa en el árbol de resultados, con alfa-beta con corte y la jugada anterior primero: con d = 1 genera 4 nodos y deja lista izq; con d = 2, 9 nodos y centro; con d = 3, 12 nodos y centro](../_assets/jue-c3-rx-iterativa.svg)
:::

::: figure {#jue-c3-rx-fig-flujo-corte title="El corte, en palabras"}
![Diagrama de flujo del corte: baja un nivel; si es final, vale M·U; si se acabó d, vale EVAL; al subir, MAX toma el mayor; juega la mejor de la raíz](../_assets/jue-c3-rx-flujo-corte.svg)
:::

---

### Monte Carlo plano

Estima cada jugada de la raíz (*flat Monte Carlo*) **jugando muchas partidas al azar desde ella y promediando sus pagos**. No construye un árbol de búsqueda: conserva solo un contador y una suma por jugada de la raíz.

- **Qué valor rastrea:** una estimación $\widehat Q(s_{\text{raíz}},a)$ por jugada. Pero no estima $Q$: estima $Q_{\text{azar}}$, el pago esperado si los dos juegan al azar.
- **Dónde lo guarda:** solo en las jugadas de la raíz: un contador $N(s_{\text{raíz}},a)$ y una suma. Los estados que cruza una simulación no guardan nada.
- **Cómo sube:** no sube. El $U$ de cada simulación va directo a la suma de la jugada donde empezó.
- **A qué converge:** con simulaciones independientes, la misma regla al azar y simulaciones sin límite, a $Q_{\text{azar}}$ con probabilidad 1, no a $Q$.

#### 1 · Exploración: cómo construye su estimación

Monte Carlo plano recorre **caminos del árbol del juego hasta los finales**, sin guardarlos. Antes de empezar, fija un número entero de simulaciones por jugada, $k\ge 1$.

##### Los pasos

Para cada jugada $a$ de la raíz, en el orden dado, llama $s'=T(s_{\text{raíz}},a)$ al estado que resulta y completa estos pasos:

1. **Simular (*rollout*).** Desde $s'$, elige jugadas legales **al azar, con la misma probabilidad cada una, para los dos jugadores, hasta un final**. Toma su pago $U$; si $s'$ ya es final, toma directamente su $U$.
2. **Actualizar.** Agrega ese $U$ a la suma de la jugada y una simulación a su contador. Los estados recorridos no se conservan.
3. **Repetir.** Vuelve a simular desde el mismo $s'$ hasta completar $k$ partidas. Después pasa a la siguiente jugada de la raíz.

**No usa EVAL:** el resultado sale de terminar la partida. El total de simulaciones es:

$$
\mathbf{n=|A(s_{\text{raíz}})|\,k\le b\,k}
$$

Aquí, $|A(s_{\text{raíz}})|$ es la cantidad de jugadas legales en la raíz y $b$ es el máximo de jugadas legales en cualquier estado.

##### La regla

**Lo que se promedia es el pago $U$ de cada final**, siempre desde MAX y solo definido en los finales:

$$
\mathbf{U(s)=\begin{cases}+1 & \text{si gana MAX}\\-1 & \text{si gana MIN}\\0 & \text{si empatan}\end{cases}}
$$

**El número de cada jugada.** Al terminar, calcula su promedio:

$$
\mathbf{\widehat Q(s_{\text{raíz}},a)=\frac{1}{N(s_{\text{raíz}},a)}\sum U}
$$

- **La suma reúne los pagos** de las simulaciones que empezaron con la jugada $a$. Cada una aporta el $U$ de su final.
- **El contador dice cuántas partidas se promediaron.** Al completar el presupuesto, cada jugada tiene $N(s_{\text{raíz}},a)=k$.
- **El promedio se mide siempre desde MAX.** Una victoria aporta $+1$; una derrota, $-1$; un empate, $0$.

##### Lo que estima

**$Q_{\text{azar}}(s_{\text{raíz}},a)$ es el pago esperado de la jugada si después los dos eligen al azar**, cada partida posible con su probabilidad.

- **Elegir uniformemente en cada estado no hace igual de probables todas las hojas.** Cada camino pesa el producto de $1/|A(s)|$ en cada estado que cruza.
- **Por eso $Q_{\text{azar}}$ no es, en general, el promedio simple de las hojas.** Tampoco es $Q$, que supone que ambos eligen lo mejor para sí.
- **Cuánto confiar en el promedio:** con simulaciones independientes y pagos en $[-1,1]$, el margen alrededor de $Q_{\text{azar}}$ se encoge como $1/\sqrt{N}$. La cota de Hoeffding está en [[de-donde-sale-el-bono|De dónde sale el bono]].

##### Ejemplo

**Ejemplo: dos jugadas de MAX.** Después de cada jugada, una respuesta de MIN termina la partida. Cada número de la segunda columna corresponde a una respuesta distinta.

| Jugada | Pagos finales | $Q_{\text{azar}}$ | $Q$ |
|---|---|---|---|
| $a$ | $+1,\ +1,\ -1$ | $1/3$ | $-1$ |
| $b$ | $0,\ 0$ | $0$ | $0$ |

Con respuestas al azar, MAX gana en dos de las tres continuaciones de $a$, mientras que con $b$ siempre empata. Por eso, al crecer las simulaciones, Monte Carlo plano termina prefiriendo $a$ con probabilidad 1. Pero MIN puede elegir la única respuesta que derrota a MAX: **$a$ pierde contra la mejor respuesta y $b$ asegura el empate**.

**Más simulaciones no corrigen esa decisión.** El promedio de $a$ se acerca a $1/3$, no a $-1$: se está estimando el pago contra un rival al azar.

##### Qué se repite

**Al repetir, el reparto sigue siendo uniforme:** una jugada que parece mala recibe tantas simulaciones como una que parece buena. **Solo quedan las sumas y los contadores de la raíz; los caminos simulados se descartan.**

#### 2 · Elección: qué jugada juega

**Al terminar las simulaciones**, juega la jugada de la raíz con **mayor $\widehat Q$**. En un empate, elige la primera en el orden dado. Como todas recibieron las mismas $k$ simulaciones, comparar promedios equivale a comparar sumas.

| Decisión | Regla | Usa los resultados |
|---|---|---|
| Exploración: qué simular | $k$ por jugada | No |
| Elección: qué jugar | Mayor $\widehat Q$ | Sí |

**El reparto se fija antes de ver los resultados**; la elección usa los promedios obtenidos. Si se interrumpe con cantidades distintas por jugada, hay que comparar **promedios**, porque las sumas ya no son equivalentes.

#### 3 · Propiedades

- **Número que da:** para cada jugada de la raíz, su promedio $\widehat Q$. Estima $Q_{\text{azar}}$, no el valor de minimax en general.
- **Usa EVAL:** no la necesita. Le bastan las reglas para generar jugadas, reconocer finales y obtener su pago. Trabaja en la escala de $U$, sin la $M$.
- **Garantía:** no garantiza $V$. Con independencia y regla fija, cuando $k\to\infty$ cada $\widehat Q$ converge con probabilidad 1 a su $Q_{\text{azar}}$, que puede favorecer una jugada equivocada.
- **Se puede interrumpir (*anytime*):** cuando todas las jugadas de la raíz tienen al menos una simulación. Con el reparto por bloques descrito, eso ocurre al completar la primera simulación de la última jugada.
- **Complejidad:** con una jugada al azar de costo $O(1)$, cada simulación cuesta $O(m)$ y las $n$ simulaciones, $O(nm)$. Guarda un contador y una suma por jugada de la raíz y la partida en curso: memoria $O(b)$, si cada estado ocupa espacio constante.
- **Frente a minimax y el corte:** como minimax, toma sus pagos de finales, y a diferencia del corte no necesita EVAL. Pero minimax supone que cada jugador elige lo mejor; Monte Carlo plano, que los dos eligen al azar. Por eso le basta $O(nm)$ en vez de $O(b^m)$, y por eso puede elegir mal.
- **Supuestos:** puede promediar vectores de pagos, pero entonces estima el pago contra rivales al azar, no max$^n$ (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Una jugada que lleva directo a un final:** cada simulación da el mismo $U$, así que su $\widehat Q$ es exacta desde la primera.
- **Una sola jugada:** no hay nada que decidir, aunque se puede seguir estimando.
- **Empate de promedios:** juega la primera en el orden dado.
- **Finales a distintas profundidades:** el mismo número de simulaciones no cuesta lo mismo en todas las jugadas.
- **Una respuesta certera descubierta tarde:** en el promedio pesa solo $1/N$, y no cambia hacia dónde converge.

::: figure {#jue-c3-rx-fig-mc-plano title="Monte Carlo plano en el árbol de resultados: 5 simulaciones por jugada, juega der"}
![Monte Carlo plano en el árbol de resultados con 5 simulaciones por jugada y semilla 0: las simulaciones bajan al azar hasta finales y no se guardan; las sumas son −3 para izq, −2 para centro y +3 para der, así que Q̂ vale −3/5, −2/5 y 3/5 y juega der, que con un MIN que piensa pierde](../_assets/jue-c3-rx-mc-plano.svg)
:::

::: figure {#jue-c3-rx-fig-flujo-mc-plano title="Monte Carlo plano, en palabras"}
![Diagrama de flujo de Monte Carlo plano: para cada jugada de la raíz, juega k partidas al azar hasta un final, promedia su U y al final juega la de mayor Q̂](../_assets/jue-c3-rx-flujo-mc-plano.svg)
:::

---

### Monte Carlo con actualización minimax

Simula partidas al azar, como Monte Carlo plano, pero **guarda los estados que descubre y sube máximos y mínimos, no promedios**. En la literatura se llama MMMC (*Monte-Carlo search with minimax value update*; Kocsis, Szepesvári y Willemson, 2006).

- **Qué valor rastrea:** una estimación $\widehat Q(s,a)=\widehat V(T(s,a))$ de cada jugada visitada. No es un promedio: es el minimax de lo descubierto hasta ahora.
- **Dónde lo guarda:** en cada estado descubierto, que se agrega al árbol guardado y no se borra.
- **Cómo sube:** con el máximo en MAX y el mínimo en MIN, solo sobre las jugadas visitadas.
- **A qué converge:** casi seguramente a $V$, en un árbol de juego finito, determinista y de ramificación finita, con las condiciones de sus propiedades.

#### 1 · Exploración: cómo construye su estimación

**Cada iteración es una partida al azar que deja huella.** Lo que descubre se queda, y lo que se sabe de un final sube de inmediato hasta la raíz.

##### Los pasos

1. **Simular.** Desde la raíz, elige jugadas legales **uniformemente, para los dos jugadores, hasta un final real**.
2. **Agregar lo descubierto.** Los estados de esa partida que no estaban en el árbol guardado se agregan.
3. **Valorar el final.** En el final $z$, $\widehat V(z)=U(z)$: exacto, sin ruido ni promedio.
4. **Subir el valor.** Por el camino, de abajo hacia arriba, cada arista toma $\widehat Q(s,a)=\widehat V(T(s,a))$ y cada estado recalcula su $\widehat V(s)$ con la regla.

##### La regla

| Estado | Su estimación |
|---|---|
| Final descubierto | $\mathbf{\widehat V(z)=U(z)}$ |
| $\mathrm{Pl}(s)=$ MAX | $\mathbf{\widehat V(s)=\max_{a\text{ visitada}}\widehat Q(s,a)}$ |
| $\mathrm{Pl}(s)=$ MIN | $\mathbf{\widehat V(s)=\min_{a\text{ visitada}}\widehat Q(s,a)}$ |

- **Una jugada no visitada es desconocida, nunca cero.** El máximo o el mínimo se toma solo sobre las visitadas, y por eso es **provisional**.
- **Un final vuelve exacta la $\widehat Q$ de la jugada que lleva a él.** Su $U$ no tiene ruido: sale de las reglas.
- **Un antecesor queda resuelto** cuando sus hijos conocidos bastan para fijar el máximo o el mínimo. Por ejemplo, un nodo de MIN que ya vio un $-1$, el peor pago posible para MAX.
- **No se promedia el $U$ crudo por jugada.** Promediar y después tomar el máximo seguiría estimando $Q_{\text{azar}}$.

##### Ejemplo

**Ejemplo: las mismas dos jugadas de Monte Carlo plano.** Bajo $a$, MIN tiene respuestas que dan $+1$, $+1$ y $-1$; $b$ da $0$. Supón que $b$ ya fue visitada y que la respuesta $-1$ aparece hasta la tercera visita a $a$:

| Lo visto bajo $a$ | Promedio de $U$ | Actualización minimax |
|---|---|---|
| $+1$, $+1$ | $1$ | $1$, provisional |
| $+1$, $+1$, $-1$ | $1/3$ | $-1$, exacto |

**La actualización minimax cambia a $b$ en el mismo respaldo en que aparece el $-1$.** El promedio sigue prefiriendo $a$ y, con más simulaciones, tiende a $Q_{\text{azar}}=1/3$. Si las tres respuestas fueran $+1$, las dos coincidirían en $a$.

**Un final malo descubierto tarde baja el mínimo de golpe; en un promedio pesa solo $1/N$.** La refutación de [[simular-en-vez-de-evaluar|Simular partidas]] lo muestra con una secuencia impuesta, no una corrida: 29 resultados $+10$ por A y luego un $-30$.

**El promedio de A baja apenas de $10$ a $8.67$ y sigue ganándole a B, que vale $-10$.** La actualización minimax salta a $-30$ y cambia a B en ese mismo respaldo.

##### Qué se repite

**Al repetir, el árbol guardado crece y cada vez más nodos quedan resueltos.** El muestreo nunca cambia: sigue siendo uniforme, sin preferir lo que se ve mejor.

#### 2 · Elección: qué jugada juega

**Al acabarse el presupuesto**, juega la jugada de la raíz con **mayor $\widehat Q$** disponible. Ante un empate, la primera en el orden dado; sin muestras, la primera jugada legal.

| Decisión | Qué compara | Usa los resultados |
|---|---|---|
| Exploración: qué simular | Nada: uniforme | No |
| Elección: qué jugar | $\widehat Q$ de cada jugada visitada | Sí |

**Una jugada sin visitar no compite con cero:** no tiene $\widehat Q$, así que no entra en la comparación.

#### 3 · Propiedades

- **Número que da:** una $\widehat Q$ provisional por jugada visitada, que es exacta si su subárbol quedó resuelto.
- **Usa EVAL:** no. Si se sustituye para siempre la frontera por EVAL, converge al minimax del árbol cortado, no a $V$.
- **Garantía:** converge casi seguramente a $V$ si `acciones(s)` enumera todas las jugadas, cada una con probabilidad positiva, y cada simulación llega a un final real. Además, los pagos son exactos y se conserva todo lo descubierto.
- **Con presupuesto fijo, ninguna.** En el peor caso, garantizar $V$ exige descubrir todo el árbol; con ciclos hace falta una regla de terminación que lo vuelva finito.
- **Se puede interrumpir (*anytime*):** sí; desde la primera iteración entrega la mejor $\widehat Q$ disponible.
- **Complejidad:** una iteración simula $O(m)$ jugadas y recalcula, en cada nivel del camino, el máximo o mínimo de hasta $b$ hijos: $O(bm)$. Guarda a lo más $m+1$ estados nuevos por iteración: memoria $O(nm)$, nunca más que el árbol.
- **Frente a Monte Carlo plano:** las mismas partidas al azar, otro operador al subir; por eso converge a $V$ y no a $Q_{\text{azar}}$. Con presupuesto corto puede jugar peor que Monte Carlo plano (Kocsis, Szepesvári y Willemson, 2006).
- **Frente a UCT:** UCT cambia **la selección** y promedia; la actualización minimax muestrea uniforme y cambia **el respaldo**.
- **Supuestos:** los de minimax. Con más jugadores, su extensión natural sube vectores con max$^n$ (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Final directo:** la $\widehat Q$ de esa jugada es su $U$, exacta desde que se descubre.
- **Jugada no visitada:** desconocida, no cero. Si se tomara como cero, un máximo provisional podría preferirla sin haberla visto.
- **Respuesta certera descubierta tarde:** cambia el valor del antecesor en el mismo respaldo.
- **Empates:** $\widehat V$ puede converger aunque la jugada entregada alterne entre varias óptimas.
- **Una sola jugada:** su valor sube sin que el máximo o el mínimo decidan nada.

**En la figura, una corrida de 10 partidas con semilla 0.** D queda resuelto en $-1$ desde la cuarta, cuando aparece d1; C vale $0$, todavía provisional. Izq sigue sin visitar: desconocida, no cero, y la raíz juega centro.

::: figure {#jue-rx-fig-mmmc title="Actualización minimax en el árbol de resultados: 10 partidas, juega centro"}
![La actualización minimax en el árbol de resultados tras 10 partidas al azar con semilla 0: guarda 11 estados; D vale −1, exacto, y C vale 0, provisional; I y sus finales siguen sin visitar, así que la Q̂ de izq es desconocida, no cero. Juega centro, la mayor Q̂ disponible](../_assets/jue-rx-mmmc.svg)
:::

::: figure {#jue-rx-fig-flujo-mmmc title="Actualización minimax, en palabras"}
![Diagrama de flujo de la actualización minimax: juega al azar hasta un final; agrega los estados nuevos; el final vale su U; sube por el camino tomando el máximo en MAX y el mínimo en MIN; al acabarse el presupuesto, juega la jugada de mayor Q̂](../_assets/jue-rx-flujo-mmmc.svg)
:::

---

### UCT

UCT (*Upper Confidence bounds applied to Trees*) es el miembro de la familia MCTS, la búsqueda en árbol de Monte Carlo (*Monte Carlo Tree Search*), que selecciona con la regla UCB. Aquí simula al azar hasta un final del juego y elige la jugada por número de visitas.

- **Qué valor rastrea:** una estimación $\widehat Q(s,a)$ de cada jugada de su árbol: el promedio de los pagos de las vueltas que tomaron esa jugada, medido desde MAX. Con pocas visitas puede estar lejos de $Q(s,a)$.
- **Dónde lo guarda:** **por arista**: $N(s,a)$ y $\widehat Q(s,a)$, más las visitas $N(s)$ de cada estado. Los estados que cruza la simulación al azar no guardan nada.
- **Cómo sube:** sube el mismo $U$ por el camino y cada arista lo promedia; nunca toma el máximo ni el mínimo de los hijos.
- **A qué converge:** en un árbol finito, con $c>0$ fija y vueltas sin límite, a $Q$. La selección elige cada vez mejor, y las partidas bien jugadas pesan casi todo.

#### 1 · Exploración: cómo construye su estimación

UCT construye **su propio árbol de búsqueda: una parte del árbol del juego**, que empieza con solo la raíz.

- **Hoja de su árbol:** todavía no tiene hijos agregados, pero puede tener jugadas legales pendientes.
- **Final del juego:** ya tiene pago, el $U$ que define el juego; aquí $+1$, $-1$ o $0$.

##### Los pasos

Cada **vuelta** tiene cuatro fases:

1. **Selección (*selection*).** Desde la raíz, baja por los nodos que ya están en su árbol, eligiendo en cada uno una jugada con el puntaje UCT. Se detiene en una jugada todavía sin agregar —la **frontera** de su árbol— o en un final.
2. **Expansión (*expansion*).** Si hay una jugada sin agregar, la agrega como **un hijo nuevo**. Si llegó a un final, no agrega nada: toma su $U$ y pasa directo a la retropropagación.
3. **Simulación (*rollout*).** Desde el hijo nuevo, elige jugadas legales **al azar, para los dos jugadores, hasta un final**. Los nodos de esa partida no se agregan; **no usa EVAL**.
4. **Retropropagación (*backpropagation*).** Sube ese mismo $U$ hasta la raíz. Cada arista del camino suma una visita a $N(s,a)$ y mete $U$ en su promedio $\widehat Q(s,a)$; cada estado suma una a $N(s)$.

**El signo no cambia al subir:** todos los promedios se miden desde MAX.

##### La regla

**El puntaje de la selección.** En cada nodo $s$, UCT combina el promedio de cada jugada con un bono que premia explorar:

$$
\text{bono}=c\sqrt{\frac{\ln N(s)}{N(s,a)}}
$$

MAX elige **el mayor puntaje**; la regla se ajusta según **quién mueve en ese nodo**:

| Quién mueve | Elige | Puntaje |
|---|---|---|
| MAX | El mayor | $\mathbf{\widehat Q(s,a)+\text{bono}}$ |
| MIN | El menor | $\mathbf{\widehat Q(s,a)-\text{bono}}$ |

En MIN solo cambia la cuenta de la selección; el promedio guardado sigue medido desde MAX. Elegir el menor $\widehat Q(s,a)-\text{bono}$ equivale a elegir el mayor $-\widehat Q(s,a)+\text{bono}$: **$c$ no cambia de signo**.

Las dos partes hacen cosas distintas:

- **El promedio aprovecha (*exploitation*):** resume lo que ya pasó al tomar esa jugada. Un promedio alto indica que a MAX le ha ido bien.
- **El bono explora (*exploration*):** es mayor para la jugada menos visitada. Si deja de recibir visitas mientras su padre sigue recibiéndolas, su bono crece hasta que vuelve a ser atractiva.
- **La constante $c>0$ regula el balance:** con $c$ grande pesa más explorar; con $c$ chica, el promedio. La fórmula nunca se calcula con $N(s,a)=0$: una jugada sin visitas se atiende primero en la expansión.
- **El puntaje no es un pago.** Como la EVAL, guía la búsqueda; a diferencia de ella, no estima ningún valor. De dónde sale el bono está en [[de-donde-sale-el-bono|De dónde sale el bono]].

##### Ejemplo

**Ejemplo en un nodo de MAX.**

| Jugada | Promedio | Bono | Puntaje |
|---|---|---|---|
| $a$ | $0.5$ | $0.1$ | $0.6$ |
| $b$ | $0.2$ | $0.3$ | $0.5$ |

Elige $a$, aunque $b$ tenga más bono. Si el bono de $b$ fuera $0.6$, sumaría $0.8$ y elegiría $b$, aunque el promedio de $a$ siga siendo mayor. **Decide la suma de las dos partes.**

##### Qué se repite

**Al repetir, UCT concentra vueltas en lo que se ve mejor** según el puntaje de cada nodo, sin dejar de revisar lo demás. Su árbol crece desigual: dentro, se elige con el puntaje; desde la frontera hacia abajo, al azar.

- **Así un promedio llega a parecerse a un mínimo.** En un nodo de MIN, la respuesta que más le conviene a MIN acumula casi todas las visitas, y el promedio del padre se acerca al de ella. La versión a detalle está en [[monte-carlo-en-un-arbol-grande|MCTS con UCT]].
- **El promedio de un estado no es el de sus jugadas.** Si se dibuja $\widehat V(s)$, es el promedio de todas las vueltas que pasaron por $s$, no el máximo ni el mínimo de sus $\widehat Q(s,a)$.

#### 2 · Elección: qué jugada juega

**Al acabarse el tiempo o las vueltas**, juega la jugada de la raíz con **más visitas $N(s_{\text{raíz}},a)$**: la regla del **hijo más visitado (*robust child*)**. Es la convención de este curso; el artículo original usa la de mayor promedio.

| Decisión | Qué compara | Usa bono |
|---|---|---|
| Selección: dónde gastar otra vuelta | Puntajes UCT | Sí |
| Elección: qué jugar | Visitas $N(s_{\text{raíz}},a)$ | No |

**Seleccionar no es entregar.** Elegir por visitas evita fiarse de un promedio alto que salió de pocas partidas, aunque con pocas vueltas también puede equivocarse.

#### 3 · Propiedades

- **Número que da:** para cada jugada, sus visitas y su promedio $\widehat Q$. Estima el valor de minimax; no es exacto.
- **Usa EVAL:** no. Le bastan las reglas para generar jugadas, reconocer finales y saber quién ganó. Trabaja en la escala de $U$, sin la $M$.
- **Garantía:** con presupuesto fijo, ninguna. En un árbol finito, con cualquier $c>0$ fija, los promedios convergen a los de minimax, aunque puede tardar mucho.
- **Se puede interrumpir (*anytime*):** desde la primera vuelta tiene una jugada que recomendar.
- **Complejidad:** sea $h$ la profundidad que alcanzó su árbol. Una vuelta cuesta $O(bh+m)$; $n$ vueltas, $O(n(bh+m))$. Guarda a lo más $n+1$ nodos: memoria $O(n)$.
- **Frente a Monte Carlo plano:** Monte Carlo plano supone que los dos juegan al azar en toda la partida; UCT, solo debajo de su frontera. Por eso su promedio puede acercarse a $Q$, y no a $Q_{\text{azar}}$.
- **Frente a la actualización minimax:** las dos convergen a $V$, por caminos opuestos. UCT mejora la selección y promedia; la otra muestrea uniforme y sube máximos y mínimos.
- **Supuestos:** dos jugadores de suma cero. Con vectores, cada quien selecciona por su promedio y puede dar equilibrios mixtos (@jue-rx-nota-suma-cero).

#### 4 · Casos borde

- **Final ya en su árbol:** no se expande ni se simula desde ahí; se retropropaga su $U$ exacto.
- **Jugada no visitada:** no tiene puntaje; la expansión la atiende antes de cualquier comparación.
- **Respuesta certera descubierta tarde:** entra como una observación más y mueve el promedio en proporción a $1/N$. La corrección es gradual, conforme la selección se concentra en ella.
- **Empates:** los promedios pueden converger sin una jugada única, y la más visitada puede alternar.
- **Una sola jugada:** queda forzada; sigue acumulando evidencia en su subárbol.

**En la figura de 12 vueltas, d1 ya dio $-1$ cuatro veces.** Aun así, $\widehat Q(s_{\text{raíz}},\text{der})=-1/7$ y der es la más visitada: el $-1$ certero de MIN pesa como un pago más.

::: figure {#jue-c3-rx-fig-uct-12 title="UCT en el árbol de resultados tras 12 vueltas: todavía juega der"}
![UCT en el árbol de resultados con c = 1 y semilla 0, tras 12 vueltas: su árbol tiene 10 nodos y las visitas de izq, centro y der son 1, 4 y 7; juega der, la más visitada, aunque d1 ya dio −1 cuatro veces](../_assets/jue-c3-rx-uct-12.svg)
:::

::: figure {#jue-c3-rx-fig-uct-40 title="UCT en el árbol de resultados tras 40 vueltas: ya juega centro"}
![UCT en el árbol de resultados con c = 1 y semilla 0, tras 40 vueltas: su árbol tiene los 15 nodos y las visitas de izq, centro y der son 5, 26 y 9; juega centro, la jugada de minimax](../_assets/jue-c3-rx-uct-40.svg)
:::

::: figure {#jue-c3-rx-fig-flujo-uct title="UCT, en palabras"}
![Diagrama de flujo de UCT: un ciclo de selección, expansión, simulación y retropropagación; cuando se acaba el tiempo, juega la jugada más visitada](../_assets/jue-c3-rx-flujo-uct.svg)
:::

---

## Comparación

Las siete fichas, lado a lado. «Corte» es por nivel o por reloj. **Expectiminimax va marcado: resuelve otro juego, con un dado en D.**

### Lo que entrega cada uno en el árbol de resultados

::: table {#jue-c3-cmp-resultados title="Todos los algoritmos en el árbol de resultados"}
| Algoritmo | Jugada, valor | Nodos |
|---|---|---:|
| Minimax | centro, 0 | 15 |
| Alfa-beta, orden dado | centro, 0 | 12 |
| Alfa-beta, al revés | centro, 0 | 14 |
| Expecti­minimax, dado en D | der, 1/3 | 15 |
| Corte, d=1 | izq, 60 | 4 |
| Corte, d=2 | centro, 10 | 11 |
| Corte, d=3 | centro, 0 | 15 |
| Quietud, d=1 | centro, 20 | 5 |
| Iterativa, d=1, 2, 3 | centro, 0 | 25 |
| Monte Carlo plano | der, 3/5 | 15 |
| Actualización minimax | centro, 0 | 11 |
| UCT | centro, 0 | 15 |
:::

- **Valor:** en la escala de cada uno. Los de corte usan $M\cdot U$, como la EVAL; los demás, la de $U$.
- **Nodos en las búsquedas:** los generados, contando R. La iterativa suma sus tres búsquedas, con repeticiones.
- **Nodos en los Monte Carlo:** en Monte Carlo plano, los nodos distintos que tocaron sus simulaciones; en la actualización minimax y en UCT, los que quedaron en su árbol.
- **Las corridas son las de la semilla 0:** Monte Carlo plano jugó 15 simulaciones, 5 por jugada; la actualización minimax, 10 partidas; UCT, 40 vueltas con $c=1$.

**Tres filas no dicen centro, cada una por una razón distinta:** el dado cambia el juego, el corte a $d=1$ no ve la captura y Monte Carlo plano supone que los dos juegan al azar. Las otras nueve aciertan, pero coincidir en la jugada no da a sus números el mismo significado.

### Qué hace cada uno

::: table {#jue-c3-rx-tab-numero title="Qué número da cada uno y si usa EVAL"}
| Algoritmo | Usa EVAL | Número que da |
|---|---|---|
| Minimax | No | $Q$ de cada jugada |
| Alfa-beta | No | $Q$ de la elegida; cotas |
| Expectiminimax (dado en D) | No | $Q$ esperado, de otro juego |
| Corte | Sí | Valor con corte $V_d$ |
| Monte Carlo plano | No | $\widehat Q$, hacia $Q_{\text{azar}}$ |
| Actualización minimax | No | $\widehat Q$ por máximo o mínimo |
| UCT | No | $N$ y promedio $\widehat Q$ |
:::

::: table {#jue-c3-rx-tab-juega title="Qué jugada juega cada uno y si garantiza V"}
| Algoritmo | Juega | Garantiza $V$ |
|---|---|---|
| Minimax | La de mayor $Q$ | Sí |
| Alfa-beta | La de minimax | Sí, en la raíz |
| Expectiminimax (dado en D) | La de mayor $Q$ esperado | El del juego con dado |
| Corte | La de mayor $V_d$ | Si llega a finales |
| Monte Carlo plano | La de mayor $\widehat Q$ | No |
| Actualización minimax | La de mayor $\widehat Q$ | No; converge a $V$ |
| UCT | La más visitada | No; converge a $V$ |
:::

- **En el corte por reloj**, la jugada es la de la **última búsqueda completa**; la búsqueda que el reloj interrumpe se descarta.
- **En Monte Carlo plano**, con simulaciones independientes y la misma regla al azar, $\widehat Q$ se acerca a $Q_{\text{azar}}$, y no a $Q$.
- **En la actualización minimax**, la convergencia pide un árbol finito y determinista, todas las jugadas con probabilidad positiva y lo descubierto conservado.
- **En UCT**, en un árbol finito, con $c>0$ fija y vueltas sin límite, los promedios se acercan a $Q$. Con un presupuesto fijo no hay garantía.

### Cuánto cuesta y cuándo conviene

El costo cuenta una unidad por nodo generado o por jugada simulada, con recorrido en profundidad y sin tabla de transposición.

::: table {#jue-c3-rx-tab-costo title="Cuánto cuesta cada uno"}
| Algoritmo | Tiempo | Memoria |
|---|---|---|
| Minimax | $O(b^m)$ | $O(bm)$ |
| Alfa-beta | $O(b^{m/2})$ a $O(b^m)$ | $O(bm)$ |
| Expectiminimax | $O(b^m)$, con $b$ del azar | $O(bm)$ |
| Corte | $O(b^d)$ sin poda | $O(bd)$ |
| Monte Carlo plano | $O(nm)$ | $O(b)$ |
| Actualización minimax | $O(nbm)$ | $O(nm)$ |
| UCT | $O(n(bh+m))$ | $O(n)$ |
:::

::: table {#jue-c3-rx-tab-cuando title="Cuándo se puede interrumpir y cuándo conviene"}
| Algoritmo | *Anytime* | Conviene si |
|---|---|---|
| Minimax | No | Cabe todo el árbol |
| Alfa-beta | No | Cabe todo, con poda |
| Expectiminimax | No | Hay dados y cabe |
| Corte | Por reloj, sí | Hay buena EVAL |
| Monte Carlo plano | Tras simular cada jugada | Sin EVAL, como base |
| Actualización minimax | Desde la primera iteración | Sin EVAL, si cabe en memoria |
| UCT | Desde la primera vuelta | Sin EVAL, árbol enorme |
:::

- **En alfa-beta**, $O(b^{m/2})$ es con el **orden perfecto** de los hijos y $O(b^m)$, con el peor. Con el mismo orden, nunca genera más nodos que minimax, pero puede generar los mismos.
- **En el corte con alfa-beta** y orden perfecto, el tiempo baja a $O(b^{d/2})$. Por reloj, si cada búsqueda cuesta $B>1$ veces la anterior, todas juntas cuestan aproximadamente $B/(B-1)$ veces la última.
- **En Monte Carlo plano**, $n=|A(s_{\text{raíz}})|\,k\le b\,k$: cada jugada de la raíz recibe $k$ simulaciones.
- **Las filas del corte no incluyen la quietud.** Con ella, el peor caso cuesta $O(b^m)$ en tiempo y $O(bm)$ en memoria, y la garantía exige llegar a los finales antes de activarla.
- **Poder interrumpir no es garantizar.** Un algoritmo *anytime* siempre tiene una jugada que entregar, pero con poco tiempo puede ser mala.

### Qué garantiza y qué supone cada número

**Acertar la jugada no es lo mismo que garantizar el valor.** La tabla dice si cada algoritmo, **por cómo funciona**, devuelve $V$:

::: table {#jue-c3-cmp-garantiza title="Qué algoritmo garantiza V"}
| Algoritmo | ¿Garantiza $V$? |
|---|---|
| Minimax | Sí |
| Alfa-beta | Sí, en la raíz |
| Expecti­minimax | Sí, el $V$ del juego con dado |
| Corte | No, salvo si llega a los finales |
| Quietud | No, salvo si llega a los finales antes de cortar |
| Iterativa | No, salvo si llega a los finales |
| Monte Carlo plano | No |
| Actualización minimax | No; converge a él en un árbol finito |
| UCT | No; converge a él con cualquier $c>0$ |
:::

**En el árbol de resultados, cuatro filas que en general no garantizan $V$ dan el $0$ de minimax.** El corte a $d=3$ y la iterativa, porque esta vez llegan a los finales. La actualización minimax, con un $0$ todavía provisional: C no está resuelto. UCT, por casualidad: su $0$ es un promedio.

**Cada número supone algo distinto sobre los jugadores:**

::: table {#jue-c3-cmp-num-supone title="Qué supone cada número"}
| Número | Supone que |
|---|---|
| $V$ | Todos eligen lo mejor |
| Valor con corte | La EVAL acierta en el corte |
| $\widehat Q$ de Monte Carlo plano | Se juega al azar |
| $\widehat Q$ de la actualización minimax | Se elige lo mejor; se estima muestreando |
| $\widehat Q$ de UCT | Al azar solo debajo de su árbol |
:::

- **Un matiz en la fila de $V$:** en expectiminimax, el dado del juego no elige, se promedia.
- **Garantiza $V$ quien supone que todos eligen lo mejor y llega a los finales**, o prueba que lo que no mira no cambia nada.
- **Un corte trae la EVAL, y un dado del algoritmo trae una estimación.** Lo que el número supone decide hacia dónde puede converger.

**La EVAL no es lo que decide entre alfa-beta y MCTS:** se pueden combinar. Un MCTS puede valorar el hijo nuevo con una estimación en lugar de simular, o junto con la simulación, como hacía AlphaGo.

**Los siete buscan el mismo $V$; lo que los separa es qué número ponen en cada jugada y qué suponen para ponerlo.**

Continúa con [[elegir-el-algoritmo|Elegir el algoritmo]].
