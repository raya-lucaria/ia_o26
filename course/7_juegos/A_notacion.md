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
símbolo. Si algo te resulta opaco, vuelve a esa página.

**Las tablas van por tema, no en orden de aparición.** Si un renglón usa un
símbolo de otra tabla, como $s_0$ o $T(s,a)$ en «Grafos» y «Hexapawn»,
búscalo en la suya: esos dos están en «Las siete piezas de un juego».

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
| $G=(S,E)$ | «ge igual a ese, e». El grafo de un juego: un nodo por estado y una arista por jugada, $E=\{(s,T(s,a))\}$ | El juego como grafo |
| n1 → n3 | «ene uno y luego ene tres». Un camino en el grafo: de un nodo a su hijo | El juego como grafo |

## Hexapawn

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $C$ | «ce». Las nueve casillas, de $a1$ a $c3$: la letra es la columna y el número, la fila | Escribir el juego |
| $B$, $N$, $\cdot$ | «be», «ene», «punto». Lo que hay en una casilla: peón blanco, peón negro o nada. $B$ y $N$ también nombran el turno y a los jugadores, Blancas y Negras | Leer el reglamento y Escribir el juego |
| $\tau: C\to\{B,N,\cdot\}$ | «tau». Un tablero: a cada casilla le asigna lo que hay en ella; $\tau_0$ es el tablero inicial | Escribir el juego |
| a1-a2, c1xb2 | «a uno a a dos», «c uno por b dos». Una jugada: casilla de salida, guion **-** si avanza o **x** si captura, casilla de llegada | Escribir el juego |
| «tras a1-a2» | «tras a uno a dos». El estado $T(s_0,\text{a1-a2})$ al que se llega con esa jugada | Escribir el juego |
| n1 | «ene uno». El estado tras a1-a2 y b3-b2 | Escribir el juego |
| n2, …, n13 | «ene dos». Los demás estados del subgrafo de n1, en el orden en que se recorren | El juego como grafo |

## Las siete piezas de un juego

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $\mathcal{S}$ | «ese caligráfica». El universo: todas las situaciones que se pueden escribir, se alcancen o no | Escribir el juego |
| $S$ | «ese». Los estados: las situaciones que se alcanzan desde $s_0$ | Escribir el juego |
| $s$, $s_0$ | «ese», «ese cero». Un estado cualquiera; el estado inicial | Escribir el juego |
| $s_1, s_2, \dots$ | «ese uno, ese dos». Los estados de la partida trazada con las piezas, en orden | Escribir el juego |
| $S_F$ | «ese efe». Los estados finales: donde la partida terminó | Escribir el juego |
| $\mathrm{Pl}(s)$ | «pe ele de ese». El jugador que mueve en un estado no final: MAX o MIN. Traduce el turno guardado. En un juego con azar también puede valer AZAR | Escribir el juego |
| MAX, MIN | «max», «min». MAX es el jugador desde cuyo lado se mide la utilidad y busca que sea alta; MIN busca que sea baja | Escribir el juego |
| $\mathcal{A}$ | «a caligráfica». Todas las jugadas que se pueden escribir en el juego | Escribir el juego |
| $a$ | «a». Una jugada cualquiera (no es la columna a) | Escribir el juego |
| $A(s)$ | «a de ese». Las jugadas permitidas en un estado no final; nunca está vacío | Escribir el juego |
| $T(s,a)$ | «te de ese, a». El estado al que lleva la jugada $a$ desde $s$. Dominio: $\{(s,a): s\in S\setminus S_F,\ a\in A(s)\}$ | Escribir el juego |
| $U(s)$ | «u de ese». Lo que vale un final para MAX; para MIN vale $-U(s)$ | Escribir el juego |

## Resolver

| Símbolo | Cómo se lee y qué es | Se presenta en |
|---|---|---|
| $V(s)$ | «ve de ese». El valor: la utilidad que MAX puede garantizar desde $s$ si MIN responde siempre con lo peor para MAX. En un final, $V(s)=U(s)$; en un nodo de MAX, el máximo de sus hijos; en uno de MIN, el mínimo | El juego como grafo y Minimax a mano |
| $\max_{a\in A(s)} f(a)$ | «máximo de efe». El número más alto que alcanza $f$ entre las jugadas de $A(s)$ | Diagnosticar el juego |
| $\operatorname*{arg\,max}_{a\in A(s)} f(a)$ | «arg max de efe». El conjunto de jugadas que alcanzan ese máximo; puede tener varias | Diagnosticar el juego |
| $a^{∗}$ | «a estrella». Una jugada elegida del $\operatorname{arg\,max}$; se escribe $a^{∗}\in\operatorname{arg\,max}$ porque puede haber varias | Minimax a mano |
| $v$ | «ve». En un procedimiento: el mejor valor visto hasta ahora entre los hijos del nodo actual | Minimax como algoritmo |
| $-\infty$, $+\infty$ | «menos infinito», «más infinito». Marcas menores y mayores que cualquier utilidad: el primer hijo siempre las reemplaza | Minimax como algoritmo |
| $b$, $m$ | «be», «eme». Factor de ramificación (el máximo de jugadas en un estado) y profundidad máxima (la partida más larga) | Minimax como algoritmo |
| AZAR | «azar». Valor de $\mathrm{Pl}(s)$ en un nodo donde nadie elige: decide un dado o una moneda | Cuando decide un dado |
| $\Pr(a)$ | «probabilidad de a». En un nodo de azar, la probabilidad de que salga el resultado $a$; suman 1 | Cuando decide un dado |
| $\alpha$, $\beta$ | «alfa», «beta». Lo que MAX y lo que MIN ya tienen asegurado con alguna alternativa en el camino desde la raíz | Alfa-beta a mano |
| $d$ | «de». La profundidad que queda: cuántas jugadas más, de los dos jugadores, se pueden mirar desde el estado actual | Cortar y evaluar a mano |
| $\mathrm{EVAL}(s)$ | «eval de ese». La función de evaluación: estima qué tan bueno es $s$ para MAX mirando solo $s$. En la clase 3, $10\cdot\text{material}+\text{avance}$ | Cortar y evaluar a mano |
| $100\cdot U(s)$ | «cien por u de ese». La utilidad de un final en la escala de $\mathrm{EVAL}$: pesa más que cualquier estimación | Cortar y evaluar a mano |
| $\bar u(s')$, $N(s')$ | «u barra», «ene». En MCTS: promedio de las simulaciones que pasaron por $s'$ y cuántas fueron | Simular en vez de evaluar |

## Términos

| Término | Qué es | Se presenta en |
|---|---|---|
| Hijo, padre | Si hay arista de $u$ a $v$, $v$ es hijo de $u$ y $u$ es padre de $v$ | Escribir el juego |
| Camino | Sucesión de nodos donde cada uno es hijo del anterior | Escribir el juego |
| Hoja | Nodo sin hijos | Escribir el juego |
| Raíz | Nodo desde el que hay un camino a todos los demás | Escribir el juego |
| Árbol | Grafo con raíz donde cada nodo, salvo la raíz, tiene un solo padre | Escribir el juego |
| Ciclo | Camino que vuelve a su primer nodo | Escribir el juego |
| Nodo de MAX, de MIN | Estado con $\mathrm{Pl}(s)=\text{MAX}$, o con $\mathrm{Pl}(s)=\text{MIN}$ | Escribir el juego |
| Expandir | Calcular $A(s)$ y, para cada jugada, $T(s,a)$: así aparecen los hijos | Escribir el juego |
| Posición perdida | Una en la que el rival puede asegurarte la derrota, hagas lo que hagas | Escribir el juego |
| Jugada, acción | Lo mismo: lo que el jugador de turno elige | Escribir el juego |
| Tupla | Lista ordenada de piezas | Escribir el juego |
| Racional | Que elige la jugada que espera le dé más utilidad, dados su función a optimizar, lo que sabe, lo que puede hacer y lo que alcanza a calcular. No quiere decir que gane | Escribir el juego |
| Racionalidad limitada | Elegir lo mejor que se alcanza con el tiempo y la memoria que hay, cuando la jugada perfecta no se puede calcular | Escribir el juego |
| Por turnos, determinista, información perfecta, finito, suma cero | Los supuestos de la clase 1: uno mueve a la vez; sin azar; cada uno ve el estado y las jugadas anteriores; toda partida termina; lo que gana uno lo pierde el otro | Escribir el juego |
| Subgrafo de un estado | Los estados que se alcanzan desde él, con sus aristas | El juego como grafo |
| Árbol de partidas, grafo de estados | En el árbol, un nodo por camino; en el grafo, un nodo por estado | El juego como grafo |
| Transposición | Dos caminos distintos que llegan al mismo estado | El juego como grafo |
| Grafo explícito, implícito | Explícito: se generan todos los estados antes y se guardan. Implícito: se generan cuando hacen falta | El juego como grafo |
| Resolver el juego | Ponerle a cada nodo su valor $V(s)$ | El juego como grafo |
| Desempate | Una preferencia, como ganar rápido, que elige entre jugadas del $\operatorname{arg\,max}$ sin cambiar la utilidad | Minimax a mano |
| Minimax | Procedimiento que recibe las reglas, genera los estados en profundidad y devuelve $V(s)$ | Minimax como algoritmo |
| Altura | Jugadas de la continuación más larga desde un nodo hasta un final; un final tiene altura 0 | Minimax como algoritmo |
| Tabla de transposición | Tabla que guarda el valor de cada estado ya calculado, para no recalcularlo si se llega por otro camino | Minimax como algoritmo |
| Valor esperado | Promedio de los resultados posibles, cada uno pesado por su probabilidad | Cuando decide un dado |
| Expectiminimax | Minimax con un caso más: en un nodo de azar, el valor esperado de sus hijos | Cuando decide un dado |
| Alfa-beta | Minimax que deja de generar las jugadas que ya no pueden cambiar la decisión de arriba | Alfa-beta a mano |
| Corte alfa, corte beta | En un nodo de MIN, dejar de generar hijos cuando $v\le\alpha$; en uno de MAX, cuando $v\ge\beta$ | Alfa-beta a mano |
| Cota | Lo que devuelve un nodo donde se cortó: su valor es a lo más, o al menos, ese número | Alfa-beta a mano |
| Estrategia | Función que a cada estado donde le toca a un jugador le asigna una jugada de $A(s)$ | Diagnosticar el juego |
| Nodo de azar | Nodo donde no elige un jugador sino un dado; cada flecha lleva su probabilidad | Diagnosticar el juego |
| Tabla de pagos | Filas: jugadas de uno; columnas: jugadas del otro; cada celda: lo que gana cada uno | Diagnosticar el juego |
| El problema de la unidad | Dado el juego, encontrar en cada estado de MAX la jugada que le asegura la mayor utilidad si MIN es racional y responde lo mejor que puede | Escribir el juego |
| Análisis hacia atrás | Con el grafo explícito, etiquetar los nodos desde los finales hacia $s_0$; así se construyen las tablas de finales de ajedrez | El juego como grafo |
| Nodo de corte | Estado no final al que se llega con $d=0$: se evalúa con $\mathrm{EVAL}$ y no se expande | Cortar y evaluar a mano |
| Valor con corte | El minimax del árbol cortado a $d$ jugadas, con $\mathrm{EVAL}$ en los nodos de corte; no es el valor del juego | Cortar y evaluar a mano |
| Material, avance | Peones blancos menos negros; filas avanzadas por los blancos menos las de los negros | Cortar y evaluar a mano |
| Efecto horizonte | Una consecuencia decisiva queda justo detrás del corte, y la búsqueda valora mal la jugada | Jugar contra el reloj |
| Posición quieta, búsqueda de quietud | Posición sin capturas disponibles; en un nodo de corte que no es quieto, seguir mirando solo capturas antes de evaluar | Jugar contra el reloj |
| Profundización iterativa | Buscar con $d=1,2,3,\dots$ mientras haya tiempo y entregar la jugada de la última búsqueda completa | Jugar contra el reloj |
| Simulación | Partida desde un estado hasta un final, con jugadas al azar; su resultado es la $U$ del final | Simular en vez de evaluar |
| MCTS, búsqueda de árbol Monte Carlo | Construye un árbol con vueltas de selección, expansión, simulación y retropropagación, y estima cada jugada por el promedio de sus simulaciones | Simular en vez de evaluar |
| Explorar, aprovechar | Probar lo poco probado, o elegir lo que ya funcionó; la regla UCT equilibra los dos | Simular en vez de evaluar |

## En las figuras

| Marca | Qué significa |
|---|---|
| Borde doble | Estado final, con su $U$ |
| Borde punteado | El estado existe, pero todavía no se expande |
| Borde grueso de color | Lo nuevo de ese paso |
| Flecha resaltada | Una jugada que alcanza el valor de su padre |
| Esquinas redondas | Nodo de azar |
| Caja punteada con «?» | Estado que el recorrido nunca genera |
| Círculo con número | Orden en que un recorrido visita el nodo |

Cada clase agrega sus símbolos a esta hoja.
