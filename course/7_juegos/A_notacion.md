---
id: notacion-juegos
title: Toda la notación, en una hoja
nav_title: Notación
summary: "Cada símbolo y cada término que usa la unidad de juegos, cómo se lee, qué significa y en qué página se presentó."
status: ready
estimated_time: 5m
tags: [juegos, referencia, notacion]
---

# Toda la notación, en una hoja

Todos los símbolos están definidos en su página. Si encuentras uno a media
lectura y no recuerdas qué era, búscalo aquí en vez de retroceder.

**Cómo leer la última columna:** dice en qué página se **presentó** el
símbolo. Si algo te resulta opaco, vuelve a esa página. Un título largo va
sin la parte que sigue a los dos puntos.

**Las tablas van por tema, no en orden de aparición.** Si un renglón usa un
símbolo de otra tabla, búscalo en la suya. Por ejemplo, $s_0$ y $T(s,a)$
están en «Las siete piezas de un juego».

**Dos convenciones valen en toda la unidad.** Todo valor se mide desde
MAX, también en los nodos de MIN. Lo exacto va sin gorro; lo que se estima
con muestras lleva gorro, como $\widehat Q$.

## Conjuntos y funciones

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $x\in X$ | «equis pertenece a equis mayúscula». $x$ es un elemento del conjunto $X$; $x\notin X$, que no lo es | Escribir el juego |
| $\{x,y,z\}$ | «el conjunto equis, ye, zeta». El conjunto formado por esos elementos | Escribir el juego |
| $\{x\in X : P(x)\}$ | «los equis de X tales que pe». Los elementos de $X$ que cumplen la condición $P$ | Escribir el juego |
| $X\subseteq Y$ | «equis contenido en ye». Todo elemento de $X$ está en $Y$ | Escribir el juego |
| $X\setminus Y$ | «equis menos ye». Los elementos de $X$ que no están en $Y$ | Escribir el juego |
| $X\times Y$ | «equis por ye». Los pares $(x,y)$ con $x\in X$ y $y\in Y$. Entre números, $\times$ es multiplicar | Escribir el juego |
| $\mathbb{R}$ | «los reales». Los números reales | Escribir el juego |
| $f: X\to Y$ | «efe de equis en ye». Una función: a cada elemento de su **dominio** $X$ le asigna uno de su **codominio** $Y$ | Escribir el juego |
| $3^9$ | «tres a la nueve». $3$ multiplicado por sí mismo 9 veces | Escribir el juego |
| Llave con renglones | «por casos». Una función que da un valor distinto según qué condición se cumpla | Escribir el juego |

## Grafos

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $G=(\mathcal{N},E)$ | «ge igual a ene caligráfica, e». Un grafo dirigido: nodos $\mathcal{N}$ y aristas $E\subseteq\mathcal{N}\times\mathcal{N}$ | Escribir el juego |
| $(u,v)$ | «u, ve». Una arista: una flecha del nodo $u$ al nodo $v$; $v$ es **hijo** de $u$ | Escribir el juego |
| $G=(S,E)$ | «ge igual a ese, e». El grafo de un juego: un nodo por estado y una arista por jugada, $E=\{(s,a,T(s,a)) : s\notin S_F,\ a\in A(s)\}$. Dos jugadas que llevan al mismo hijo son dos aristas; el dibujo puede abreviarlas | El juego como grafo |
| n1 → n3 | «ene uno y luego ene tres». Un camino en el grafo: de un nodo a su hijo | El juego como grafo |

## Hexapawn

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $C$ | «ce». Las nueve casillas, de $\text{a1}$ a $\text{c3}$: la letra es la columna y el número, la fila | Escribir el juego |
| $B$, $N$, $\cdot$ | «be», «ene», «punto». Lo que hay en una casilla: peón blanco, peón negro o nada. $B$ y $N$ también nombran a los jugadores, Blancas y Negras; como turno, son la etiqueta que guarda el estado | Leer el reglamento y Escribir el juego |
| $\tau: C\to\{B,N,\cdot\}$ | «tau». Un tablero: a cada casilla le asigna lo que hay en ella; $\tau_0$ es el tablero inicial | Escribir el juego |
| $\text{a1}\textbf{-}\text{a2}$, $\text{c1}\textbf{x}\text{b2}$ | «a uno a a dos», «c uno por b dos». Una jugada: casilla de salida, guion **-** si avanza o **x** si captura, casilla de llegada | Escribir el juego |
| «tras $\text{a1}\textbf{-}\text{a2}$» | «tras a uno a dos». El estado $T(s_0,\text{a1}\textbf{-}\text{a2})$ al que se llega con esa jugada | Escribir el juego |
| n1 | «ene uno». El estado tras $\text{a1}\textbf{-}\text{a2}$ y $\text{b3}\textbf{-}\text{b2}$ | Escribir el juego |
| n2, …, n13 | «ene dos». Los demás estados del subgrafo de n1, en el orden en que se recorren | El juego como grafo |

## Las siete piezas de un juego

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $\mathcal{S}$ | «ese caligráfica». El universo: todas las situaciones que se pueden escribir, se alcancen o no | Escribir el juego |
| $S$ | «ese». Los estados: las situaciones que se alcanzan desde $s_0$ | Escribir el juego |
| $s$, $s_0$ | «ese», «ese cero». Un estado cualquiera; el estado inicial del juego. El estado incluye el turno: $s=(\text{tablero},\text{turno})$. En Python, `(tablero, turno)` es el mismo $s$ desarmado | Escribir el juego |
| $s_{\text{raíz}}$ | «ese raíz». La raíz de una búsqueda: el estado donde toca decidir. Solo al empezar la partida es $s_0$ | El juego como grafo |
| $s_1, s_2, \dots$ | «ese uno, ese dos». Los estados de la partida trazada con las piezas, en orden | Escribir el juego |
| $S_F$ | «ese efe». Los estados finales: donde la partida terminó | Escribir el juego |
| $\mathrm{Pl}(s)$ | «pe ele de ese». Quién mueve en un estado no final: **lee el turno guardado en $s$**. Con azar dice quién controla la transición (MAX, MIN o AZAR), y el estado incluye esa fase. En un árbol, la etiqueta MAX, MIN o AZAR del nodo es $\mathrm{Pl}(s)$ | Escribir el juego |
| MAX, MIN | «max», «min». MAX es el jugador desde cuyo lado se miden pagos y valores, y busca que sean altos. Con dos jugadores y suma cero o constante, MIN busca que sean bajos | Escribir el juego |
| $\mathcal{A}$ | «a caligráfica». Todas las jugadas que se pueden escribir en el juego | Escribir el juego |
| $a$ | «a». Una jugada cualquiera (no es la columna a). En un nodo de AZAR, un **resultado**: nadie lo elige | Escribir el juego |
| $A(s)$ | «a de ese». Las jugadas permitidas en un estado no final; nunca está vacío | Escribir el juego |
| $T(s,a)$ | «te de ese, a». El estado al que lleva la jugada $a$ desde $s$; es determinista dado $a$, y el azar, si lo hay, está en $\Pr(a\mid s)$. Dominio: $\{(s,a): s\in S\setminus S_F,\ a\in A(s)\}$ | Escribir el juego |
| $U(s)$ | «u de ese». El **pago terminal que define cada juego, siempre desde MAX**. Hexapawn: $+1$ o $-1$, sin empates; gato y el árbol de resultados suman el $0$ del empate; otros juegos declaran su escala. Con suma cero, para MIN vale $-U(s)$ | Escribir el juego |
| $(U_1,\dots,U_n)$ | «u uno a u ene». Un pago por jugador: hace falta con más de dos jugadores o con suma no constante | Escribir el juego; con $\max^n$, en Diagnosticar el juego |

## Valor y decisión

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $V(s)$ | «ve de ese». El **valor exacto, siempre desde MAX**: el pago para MAX si los dos juegan lo mejor desde $s$. No cambia de signo con el turno | Diagnosticar el juego |
| $Q(s,a)$ | «cu de ese, a». El valor exacto de una jugada: $Q(s,a)=V(T(s,a))$. Las estimaciones llevan gorro, $\widehat Q$ | Diagnosticar el juego |
| $V$ por casos | $V(s)=U(s)$ si $s$ es final; $\max_a Q(s,a)$ si mueve MAX; $\min_a Q(s,a)$ si mueve MIN; $\sum_a\Pr(a\mid s)\,Q(s,a)$ si mueve AZAR | Diagnosticar el juego; el caso de AZAR, en Cuando decide un dado |
| $\max_{a\in A(s)} Q(s,a)$ | «máximo de cu». El número más alto que alcanza $Q(s,a)$ entre las jugadas de $A(s)$; $\min$, el más bajo | Diagnosticar el juego |
| $\operatorname*{arg\,max}_{a\in A(s)} Q(s,a)$ | «arg max de cu». El conjunto de jugadas que alcanzan ese máximo; puede tener varias. MIN usa $\operatorname{arg\,min}$ | Diagnosticar el juego |
| $a^{*}$ | «a estrella». Una jugada elegida del $\operatorname{arg\,max}$; se escribe $a^{*}\in\operatorname{arg\,max}$ porque puede haber varias | Diagnosticar el juego |
| $v$ | «ve». En un procedimiento: un acumulador, el mejor valor visto hasta ahora entre los hijos del nodo actual; en AZAR, una suma ponderada | Minimax como algoritmo |
| $w$ | «doble ve». En un procedimiento: lo que devuelve **un** hijo, recién calculado: un valor, un valor con corte o una **cota**. Luego se compara con $v$ (o, en la raíz, con mejor_valor) | Minimax como algoritmo |
| mejor_valor | En DECIDIR, el mayor $w$ que ha devuelto hasta ahora un hijo de la raíz; empieza en $-\infty$. En DECIDIR-ALFA-BETA hace ese papel $\alpha$ | Minimax como algoritmo |
| mejor_jugada | En DECIDIR, la jugada que dio mejor_valor; empieza en «ninguna». Es lo que el agente entrega | Minimax como algoritmo |
| $-\infty$, $+\infty$ | «menos infinito», «más infinito». Marcas menores y mayores que cualquier pago: el primer hijo siempre las reemplaza | Minimax como algoritmo |
| $\Delta$ | «delta». En la tarea de monedas en fila, los pesos acumulados por MAX menos los del rival; es parte del estado | Tarea de la clase 2 |
| $W(\text{tramo})$ | «doble ve del tramo». En la misma tarea, la diferencia futura que asegura quien mueve, contando solo las monedas restantes. Cambia de perspectiva con el turno; $V$ siempre se mide desde MAX | Tarea de la clase 2 |
| $b$, $m$ | «be», «eme». Factor de ramificación (el máximo de jugadas en un estado) y profundidad máxima (la partida más larga) | Minimax como algoritmo |

## Azar

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| AZAR | «azar». Valor de $\mathrm{Pl}(s)$ donde decide el azar: nadie elige, sale un dado o una moneda | Cuando decide un dado |
| $\Pr(a\mid s)$ | «probabilidad de a dado ese». En un nodo de AZAR, la probabilidad de que salga el resultado $a$; suman 1 sobre $A(s)$ | Cuando decide un dado |
| $E[\cdot]$ | «esperanza de». La esperanza exacta: el promedio de los resultados, cada uno pesado por su probabilidad. Sin gorro | Cuando decide un dado |
| $V_{\text{azar}}(s)$, $Q_{\text{azar}}(s,a)$ | «ve azar», «cu azar». La esperanza exacta de $U$ si **los dos** juegan al azar desde $s$, o tras la jugada $a$. A esto converge Monte Carlo plano. No es $V$ | Simular partidas |

## Alfa-beta

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $\alpha$, $\beta$ | «alfa», «beta». Umbrales heredados del camino: lo que MAX ($\alpha$) y MIN ($\beta$) ya se aseguran con una jugada revisada en un nodo suyo arriba. MAX actualiza $\alpha$ y poda comparando su $v$ con $\beta$; MIN actualiza $\beta$ y poda comparando con $\alpha$ | Alfa-beta a mano |
| $(\alpha,\beta)$ | «la ventana alfa beta». Los valores que todavía importan en un nodo. Se escribe abierta porque igualar el umbral del rival ya poda: $v\le\alpha$ en MIN, $v\ge\beta$ en MAX. Igualar el propio no basta | Alfa-beta a mano |
| $(\alpha_0,\beta_0)$ | «la ventana de entrada». La ventana con que se llamó al nodo. Para lo que devuelve, $w$: si $w\le\alpha_0$, $V\le w$; si $\alpha_0<w<\beta_0$, $V=w$; si $w\ge\beta_0$, $V\ge w$ | Alfa-beta a mano |

## Corte y evaluación

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $d$ | «de». Cuántas decisiones quedan: cuántas jugadas más, de los dos jugadores, se pueden mirar desde el estado actual | Cortar y evaluar |
| $M$ | «eme». La escala reservada a los finales: un final vale $M\cdot U(s)$, y $M$ se elige para que $\lvert\mathrm{EVAL}(s)\rvert<M$. El ejemplo principal usa $M=100$; el ejercicio de la escala prueba $M=30$ a propósito, para ver que no alcanza. Nunca dos $M$ en una traza | Cortar y evaluar |
| $\mathrm{EVAL}(s)$ | «eval de ese». La función de evaluación: **estima $100\cdot V(s)$** (en general, $M\cdot V(s)$) mirando solo $s$. En la clase 3, $10\cdot\text{material}+\text{avance}$. Sin gorro: no es estadística | Cortar y evaluar |
| $M\cdot U(s)$ | «eme por u de ese». El pago de un final en la escala de $\mathrm{EVAL}$; con $M=100$, $100\cdot U(s)$. Una victoria vale más que cualquier estimación, y una derrota, menos | Cortar y evaluar |
| $V_d(s)$ | «ve de ese con de». El valor con corte, por casos: $M\cdot U(s)$ si $s$ es final; $\mathrm{EVAL}(s)$ si $d=0$ y no es final; $\max_a V_{d-1}(T(s,a))$ si mueve MAX; $\min_a$ si mueve MIN. El final se revisa **antes** que $d=0$ | Cortar y evaluar |
| $100\,V(s)$ | Lo que devuelve $V_d$ con $M=100$ si alcanza todos los finales: el valor exacto en la escala de los finales, no $V(s)$ | Cortar y evaluar |

## Simulación y UCT

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $\widehat Q(s,a)$ | «cu gorro». Estimación de una jugada. En Monte Carlo plano y en UCT, el promedio de los pagos de las simulaciones o vueltas que tomaron $a$; en la actualización minimax, $\widehat V(T(s,a))$ | Simular partidas |
| $\widehat V(s)$ | «ve gorro». Estimación de un estado. En la actualización minimax, el máximo (MAX) o el mínimo (MIN) de sus $\widehat Q$; en UCT, el promedio de las vueltas que pasaron por $s$ | Simular partidas |
| $N(s)$, $N(s,a)$ | «ene de ese», «ene de ese, a». Visitas: cuántas vueltas pasaron por el nodo $s$, y cuántas tomaron la arista $a$. Esta $N$ no es Negras | $N(s_{\text{raíz}},a)$, en Simular partidas; en todo el árbol, MCTS con UCT |
| $k$ | «ka». Cuántas simulaciones recibe cada jugada de la raíz en Monte Carlo plano | Simular partidas |
| $n$ | «ene». Simulaciones, o vueltas de UCT, **en total**. En Monte Carlo plano, ${n=\lvert A(s_{\text{raíz}})\rvert\,k}$ | Simular partidas |
| $h$ | «hache». La profundidad que alcanzó el árbol de UCT; a lo más $m$. Una vuelta cuesta $O(bh+m)$ | MCTS con UCT |
| $c$ | «ce». El peso de explorar en la regla UCB; nunca cambia de signo, tampoco en MIN | MCTS con UCT |
| bono | $c\sqrt{\ln N(s)/N(s,a)}$: crece con las visitas del padre y baja con las de la jugada. Solo se calcula con $N(s,a)>0$: una jugada sin visitas se prueba antes | MCTS con UCT |
| Puntaje de exploración | $\widehat Q(s,a)+\text{bono}$ en MAX, que elige el mayor; $\widehat Q(s,a)-\text{bono}$ en MIN, que elige el menor. **No es un pago:** como EVAL, guía la búsqueda; a diferencia de EVAL, no estima ningún valor | MCTS con UCT |
| $\ln$ | «logaritmo natural» | MCTS con UCT |
| $\varepsilon$ | «épsilon». El margen, en la escala de $U$: cuánto puede quedar $\widehat Q$ por debajo de su esperanza (en el lema, $Q_{\text{azar}}$) | De dónde sale el bono |
| $\delta$ | «delta». La probabilidad de fallo que se tolera: que $\widehat Q$ quede $\varepsilon$ o más por debajo de su esperanza. Con $\delta=N(s)^{-4}$ sale la constante de UCB1, $2\sqrt2$ con pagos en $[-1,1]$ | De dónde sale el bono |

## Términos

### Grafos y modelado

| Término | Qué es | Se presenta en |
|---|---|---|
| Hijo, padre | Si hay arista de $u$ a $v$, $v$ es hijo de $u$ y $u$ es padre de $v$ | Escribir el juego |
| Camino | Sucesión de nodos donde cada uno es hijo del anterior | Escribir el juego |
| Hoja | Nodo sin hijos en el árbol que se considera | Escribir el juego |
| Final ≠ hoja | Un final es un estado donde terminó el juego. Una hoja puede no ser final: un nodo de corte o un nodo aún sin expandir | Escribir el juego |
| Raíz | En un árbol, el nodo sin padre, desde el que se alcanzan todos los demás | Escribir el juego |
| Árbol | Grafo con raíz donde la raíz no tiene padre, cada otro nodo tiene exactamente uno y todos se alcanzan desde la raíz | Escribir el juego |
| Ciclo | Camino que vuelve a su primer nodo | Escribir el juego |
| Nodo de MAX, de MIN | Estado con $\mathrm{Pl}(s)=\text{MAX}$, o con $\mathrm{Pl}(s)=\text{MIN}$ | Escribir el juego |
| Expandir | Calcular $A(s)$ y, para cada jugada, $T(s,a)$: así aparecen los hijos | Escribir el juego |
| Posición perdida | Una en la que el rival puede asegurarte la derrota, hagas lo que hagas. «Posición» es el nombre coloquial de un estado | Escribir el juego |
| Jugada, acción | Lo mismo: lo que el jugador de turno elige. En un nodo de AZAR, un resultado | Escribir el juego |
| Tupla | Lista ordenada de piezas | Escribir el juego |
| Por turnos, determinista, información perfecta, finito, dos jugadores, suma cero | Los supuestos de la clase 1: uno mueve a la vez; sin azar; cada uno ve el estado y las jugadas anteriores; cada estado admite un número finito de jugadas y toda partida termina, así que el árbol de partidas es finito; juegan dos; lo que gana uno lo pierde el otro | Escribir el juego |
| Subgrafo de un estado | Los estados que se alcanzan desde él, con sus aristas | El juego como grafo |
| Árbol de partidas, grafo de estados | En el árbol, un nodo por camino; en el grafo, un nodo por estado | El juego como grafo |
| Transposición | Dos caminos distintos que llegan al mismo estado | El juego como grafo |
| Grafo explícito, implícito | Explícito: se generan todos los estados antes y se guardan. Implícito: se generan cuando hacen falta | El juego como grafo |
| Resolver el juego | Ponerle a cada estado su valor: el resultado para MAX si los dos juegan lo mejor | El juego como grafo |
| Análisis hacia atrás | Con el grafo explícito, etiquetar los nodos desde los finales hacia $s_0$; así se construyen las tablas de finales de ajedrez | El juego como grafo |
| Racional | Que elige la jugada que espera le dé más utilidad, dados su función a optimizar, lo que sabe, lo que puede hacer y lo que alcanza a calcular. No quiere decir que gane | Diagnosticar el juego |
| Racionalidad limitada | Elegir lo mejor que se alcanza con el tiempo y la memoria que hay, cuando la jugada perfecta no se puede calcular | Diagnosticar el juego |
| Estrategia | Función que a cada estado donde le toca a un jugador le asigna una jugada de $A(s)$ | Diagnosticar el juego |
| Nodo de azar | Nodo donde no elige un jugador sino un dado; cada flecha lleva su probabilidad | Diagnosticar el juego |
| Tabla de pagos | Filas: jugadas de uno; columnas: jugadas del otro; cada celda: lo que gana cada uno. Es el modelo de las jugadas a la vez, que queda fuera de esta unidad | Diagnosticar el juego |
| El problema de la unidad | Dado el juego, encontrar en cada estado de MAX la jugada que le asegura el mayor pago si los dos juegan lo mejor | Diagnosticar el juego |
| Suma no constante | Lo que gana uno no es lo que pierde el otro: hace falta un pago por jugador, y el segundo maximiza el suyo en vez de minimizar el de MAX | Diagnosticar el juego |
| $\max^n$ | Con más jugadores, quien mueve elige el hijo con su componente más alta y copia el vector de ese hijo, con un desempate fijo. Da un equilibrio, sin la garantía de minimax | Diagnosticar el juego |
| *Paranoid* | Juntar a todos los rivales en una coalición MIN. Recupera alfa-beta, pero resuelve un juego más pesimista | Diagnosticar el juego |

### Árboles de la unidad

| Término | Qué es | Se presenta en |
|---|---|---|
| Árbol base | El árbol de juguete de la clase 2: MAX en la raíz, tres ramas y hojas de puntos, de 2 a 12 | Minimax como algoritmo |
| Árbol reducido | El árbol base sin su rama del centro: siete nodos, para la primera poda | Alfa-beta a mano |
| Árbol de resultados | Finales en $U$ ($+1$, $0$ o $-1$, con un solo empate), una captura de MIN (ix) y D con tres hijos; para el corte se le agrega una $\mathrm{EVAL}$ inventada en los nodos internos. Lo corren todos los algoritmos de la unidad | Minimax como algoritmo |

### Mirar todo y podar

| Término | Qué es | Se presenta en |
|---|---|---|
| Desempate | Una preferencia, como ganar rápido, que elige entre jugadas del $\operatorname{arg\,max}$ sin cambiar el valor | Minimax a mano |
| Minimax | Procedimiento que recibe las reglas y un estado, genera los estados en profundidad y devuelve $V(s)$. Es el auxiliar de DECIDIR-MINIMAX | Minimax como algoritmo |
| DECIDIR-MINIMAX | Lo que el agente corre en su turno: valora cada jugada con MINIMAX y devuelve la **jugada** de mayor valor, no el número. DECIDIR-ALFA-BETA hace lo mismo pasando $\alpha$ a los hijos | Minimax como algoritmo |
| Altura | Jugadas de la continuación más larga desde un nodo hasta un final; un final tiene altura 0 | Minimax como algoritmo |
| Pila | Las llamadas abiertas, de la raíz al nodo activo; se escribe R›C›C2. Es todo lo que el recorrido tiene en memoria | Minimax como algoritmo |
| Tabla de transposición | Guarda el valor de cada estado ya calculado, para no recalcularlo si se llega por otro camino. Con corte y alfa-beta guarda también la $d$ que quedaba y si el número es un valor ($\alpha_0<v<\beta_0$), un piso ($v\ge\beta_0$) o un techo ($v\le\alpha_0$) | Minimax como algoritmo; lo de valor, piso o techo, en Hasta dónde mirar |
| Valor esperado | Promedio de los resultados posibles, cada uno pesado por su probabilidad: $E[\cdot]$ | Cuando decide un dado |
| Utilidad esperada | El valor esperado del pago. Con azar, un jugador racional busca la mayor utilidad esperada | Cuando decide un dado |
| DECIDIR-EXPECTIMINIMAX | DECIDIR-MINIMAX con nodos de AZAR: valora cada jugada con EXPECTIMINIMAX y devuelve la de mayor valor esperado | Cuando decide un dado |
| Expectiminimax | Minimax con un caso más: en un nodo de AZAR, el valor esperado de sus hijos. Si solo hay MAX y AZAR, se llama expectimax | Cuando decide un dado |
| Alfa-beta | Minimax que deja de generar las jugadas que ya no pueden cambiar la decisión de arriba: eso es **podar** | Alfa-beta a mano |
| Poda ≠ corte | **Poda** es lo que hace alfa-beta: no genera lo que ya no importa. **Corte** es dejar de mirar a cierta profundidad y estimar | Cortar y evaluar |
| Corte alfa, corte beta | Los dos tipos de poda. El corte alfa ocurre en un nodo de MIN, cuando $v\le\alpha$; el corte beta, en uno de MAX, cuando $v\ge\beta$. Cada uno se llama como el umbral con que compara | Alfa-beta a mano |
| Cota | Lo que devuelve un nodo cuyo $w$ tocó o salió de su ventana de entrada. Si $w\le\alpha_0$, cota superior: su valor es a lo más $w$. Si $w\ge\beta_0$, cota inferior: al menos $w$ | Alfa-beta a mano |
| Ventana | El intervalo $(\alpha,\beta)$ con que llega un nodo. Empieza en $(-\infty,+\infty)$ en la raíz y al bajar solo se encoge | Alfa-beta a mano |
| Regla del empate en la raíz | Con alfa-beta, la raíz cambia de jugada solo si el $w$ de un hijo supera estrictamente a $\alpha$: un hijo que devolvió una cota no gana un empate | Alfa-beta a mano |
| *Fail-soft* | La versión de alfa-beta que, al podar, devuelve su $v$ tal cual aunque caiga fuera de la ventana, en vez de recortarlo a $\alpha$ o $\beta$ | Alfa-beta como algoritmo |
| Marco de la pila | Lo que guarda la pila por cada llamada abierta: el estado, la jugada por la que va su `for`, su ventana y su $v$. Se pierde cuando la llamada regresa | Alfa-beta como algoritmo |

### Cuando el árbol no cabe

| Término | Qué es | Se presenta en |
|---|---|---|
| Nodo de corte | Estado no final al que se llega con $d=0$: se evalúa con $\mathrm{EVAL}$ y no se expande | Cortar y evaluar |
| Valor con corte | $V_d(s)$: el minimax del árbol cortado a $d$ jugadas, con $\mathrm{EVAL}$ en los nodos de corte y los finales en $M\cdot U$. No es el valor del juego | Cortar y evaluar |
| Material, avance | Peones blancos menos negros; filas avanzadas por los blancos menos las de los negros. Blancas es MAX | Cortar y evaluar |
| DECIDIR-CON-CORTE, MINIMAX-CON-CORTE | DECIDIR-MINIMAX y su auxiliar con una línea más (con $d=0$, un estado no final vale su $\mathrm{EVAL}$) y los finales en la escala $M\cdot U$ | Cortar y evaluar |
| Horizonte | La línea donde la búsqueda se corta: lo que queda debajo no se genera | Hasta dónde mirar |
| Efecto horizonte | Una consecuencia decisiva queda justo detrás del corte, y la búsqueda valora mal la jugada | Hasta dónde mirar |
| Posición quieta, búsqueda de quietud, valor con quietud | Posición sin capturas disponibles; en un nodo de corte que no es quieto, no devolver sin más la $\mathrm{EVAL}$: usarla como opción de quedarse (una aproximación llamada *stand pat*) y compararla con las capturas, cada una seguida hasta un final o una posición quieta. Quedarse no es una jugada legal. El valor con quietud es el número que resulta | Hasta dónde mirar |
| Profundización iterativa | Buscar con $d=1,2,3,\dots$ mientras haya tiempo y entregar la jugada de la última búsqueda completa | Hasta dónde mirar |
| *Anytime* | Que tiene una jugada lista si se le interrumpe | Minimax como algoritmo |
| PROFUNDIZACIÓN-ITERATIVA | La versión completa: alfa-beta con corte en cada $d$, la jugada anterior primero y una jugada lista desde antes de buscar; entrega la de la última búsqueda completa | Hasta dónde mirar |
| PROFUNDIZAR-SIN-PODA | La profundización iterativa en su forma corta: llama a DECIDIR-CON-CORTE con $d=1,2,3,\dots$ y, cuando se acaba el reloj, entrega la jugada de la última búsqueda completa | Hasta dónde mirar |
| ALFA-BETA-CON-CORTE | Alfa-beta con los mismos cambios: con $d=0$ se estima y los finales valen $M\cdot U$ | Hasta dónde mirar |
| Simulación | Recorrido desde un estado hasta un final, con jugadas al azar; su resultado es la $U$ del final. En inglés, *rollout* | Simular partidas |
| Vuelta ≠ simulación ≠ corrida | Una vuelta es una iteración de MCTS; una simulación, el recorrido hasta un final; una corrida, la ejecución completa del algoritmo | MCTS con UCT |
| Monte Carlo plano | Estimar cada jugada de la raíz por el promedio de $k$ simulaciones al azar. Converge a $Q_{\text{azar}}$, no a $Q$ | Simular partidas |
| Monte Carlo con actualización minimax | Simular al azar, guardar los estados descubiertos y subir los resultados con máximo en MAX y mínimo en MIN. En la literatura, MMMC | Simular partidas |
| Jugada desconocida | En la actualización minimax, una jugada que no se ha visitado: no vale cero, no se sabe cuánto vale | Simular partidas |
| Nodo resuelto | Un nodo cuyo valor ya es exacto: sus hijos conocidos bastan para fijar su máximo o su mínimo | Simular partidas |
| MCTS, búsqueda en árbol de Monte Carlo | La familia: construye un árbol con vueltas de selección, expansión, simulación y retropropagación | MCTS con UCT |
| UCT | El miembro de MCTS que selecciona con la regla UCB en cada nodo del árbol. Sube el mismo $U$ y promedia, nunca toma máximo ni mínimo. En un árbol finito, con $c>0$ fija y vueltas sin límite, sus $\widehat Q$ tienden a $Q$, no a $Q_{\text{azar}}$ | MCTS con UCT |
| Explorar, aprovechar | Probar lo poco probado, o elegir lo que ya funcionó; la regla UCB equilibra los dos | MCTS con UCT |
| *Robust child* | La jugada con más visitas: la que se entrega al final, sin bono | MCTS con UCT |
| Bandido | Elegir muchas veces entre unas pocas opciones inciertas, cuya esperanza no se conoce; cada prueba da un resultado al azar. Es la raíz de MCTS sin árbol debajo | MCTS con UCT; a fondo, en De dónde sale el bono |
| Cota optimista | $\widehat Q$ más el margen: lo más que la esperanza podría valer sin que los datos lo desmientan. Que la cota quede en la esperanza o por debajo es fallar, y pasa con probabilidad a lo más $\delta$. Es un puntaje, no un pago. En MIN, $\widehat Q$ menos el margen, y se elige la menor. No es el techo de la tabla de transposición | De dónde sale el bono |
| Regla UCB, UCB1 | Regla UCB: la de la cota optimista en un bandido. UCB1: esa regla con ${c=2\sqrt2}$ para pagos en $[-1,1]$ en el bandido estacionario (Auer, Cesa-Bianchi y Fischer, 2002) | Regla UCB, en MCTS con UCT; UCB1, en De dónde sale el bono |
| A veces al azar | Elegir el mejor promedio, salvo una fracción fija de las veces (10 % aquí), en que se elige al azar | De dónde sale el bono |

## En las figuras

| Marca | Qué significa |
|---|---|
| Borde doble | Estado final, con su $U$ |
| Borde punteado | El estado existe, pero todavía no se expande |
| Borde grueso de color | Lo nuevo de ese paso |
| Flecha resaltada | Una jugada que alcanza el valor de su padre |
| Esquinas redondas | Nodo de azar |
| Caja o círculo punteado con «?» | Estado que el recorrido nunca genera; en la actualización minimax, una jugada desconocida |
| Etiqueta «exacto» bajo el $\widehat V$ de un nodo | En la actualización minimax: su valor ya no cambia, el nodo está resuelto. Sin la etiqueta, el $\widehat V$ todavía puede cambiar |
| Línea punteada de color | Dónde se corta la búsqueda; su pastilla dice el $d$ de la raíz. Desde «Hasta dónde mirar» se llama horizonte |
| Barra bajo un nodo | Ahí hubo una poda (un corte alfa o beta): los hermanos que siguen no se generan |
| Etiqueta «cota» bajo el $v$ de un nodo | Su $v$ tocó o salió de la ventana de entrada: solo garantiza un techo o un piso de su valor (puede coincidir con él, pero no se sabe) |
| Barras en el tiempo, línea del reloj | Cada barra es una búsqueda y su largo, los nodos que genera; la línea marca dónde se acaba el reloj |
| $N$ y $\widehat V$ en un nodo, $\widehat Q$ junto a una arista | En MCTS: visitas y estimación del estado; estimación de la jugada |
| Círculo con número | Orden en que un recorrido visita el nodo |
| Arista gruesa del color de MIN, nombre en negrita con «x» | Una captura: la jugada que la búsqueda de quietud no deja sin mirar |

Cada clase agrega sus símbolos a esta hoja.
