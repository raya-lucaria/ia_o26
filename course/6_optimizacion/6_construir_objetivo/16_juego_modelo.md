---
id: opt-objetivo-juego-modelo
title: Formular cómo elegir una jugada
nav_title: Juego · Modelo general
summary: "Construir un objetivo que tenga en cuenta al rival y revisar qué ocurre cuando contamos fichas en vez de valorar si ganaremos."
status: ready
tags: [optimizacion, modelado, juegos]
---

# Formular cómo elegir una jugada

Esta es una **consulta opcional** que amplía el [[opt-objetivo-juego-practica|ejemplo guiado del juego]].
Vamos a reunir el razonamiento que sirve tanto para el modelo con resultados
finales como para el modelo que cuenta fichas: decidir cómo tener en cuenta
la respuesta rival y qué puntuación usar para comparar jugadas.

En la primera parte del ejemplo guiado conocemos los resultados finales. En la segunda,
revisamos un programa que deja de mirar antes del final y cuenta fichas.
Las acciones permitidas son las mismas; cambia lo que el programa valora.

## 1 · Distinguir lo que elegimos de lo que sabemos

Llamamos $A$ al conjunto de nuestras acciones posibles. Si jugamos $a$,
el rival dispone de las respuestas del conjunto $B(a)$. Estos conjuntos
son finitos y no vacíos; sus elementos describen las jugadas permitidas.

- $A$: Acciones propias permitidas.
- $B(a)$: Respuestas que el rival puede elegir después de $a$.
- $U(a,b)$: Nuestra puntuación final tras esas dos acciones.

**Elegimos $a$; el rival elige $b$ después de observarnos.** Conocer sus
opciones no nos permite elegir su respuesta. Tampoco significa que nos
falte información sobre qué ocurriría con cada una: $U(a,b)$ es un dato
conocido para todas las combinaciones.

A esa puntuación final la llamamos *utilidad*. En el ejemplo guiado vale +1 al
ganar y −1 al perder. En otro juego podría tener más valores, según qué
resultados nos interesara distinguir. Las acciones no tienen unidades
físicas; la utilidad usa la escala de puntos acordada.

Para interpretar correctamente el modelo, necesitamos estos supuestos:

- No hay azar: una misma combinación de acciones produce el mismo resultado.
  Eso significa que el juego es **determinista**.
- La utilidad rival es $-U$. Ambas utilidades suman cero: es un juego de
  **suma cero**, con preferencias opuestas sobre los resultados.
- El rival observa nuestra jugada, conoce sus opciones y sus resultados,
  y elige la respuesta que le da la mayor utilidad a él.

Tener dos jugadores no implica por sí solo que el juego sea de suma cero.
Aquí lo hemos establecido al especificar cómo se relacionan sus utilidades.
También importa que las decisiones sean sucesivas: el modelo no describe
jugadas simultáneas ni respuestas elegidas al azar.

En el ejemplo guiado, los movimientos posteriores son obligatorios. Por eso la
pareja $a,b$ basta para determinar la utilidad final. Si después hubiera
nuevas decisiones, tendríamos que representar también esas elecciones
para valorar cómo continúa el juego.

## 2 · Valorar una acción después de pensar en el rival

Imaginemos que ya elegimos $a$. El rival puede comparar las puntuaciones
que quedan disponibles con cada respuesta $b\in B(a)$.

Como su utilidad es el negativo de la nuestra, conseguir más puntos para
él equivale a dejarnos menos a nosotros. Bajo el comportamiento supuesto,
el valor que debemos atribuir a nuestra acción es:

$$v(a)=\min_{b\in B(a)}U(a,b).$$

El mínimo convierte los resultados posibles de una acción en un solo
número. Ese número se mide en la misma escala que $U$ y se obtiene de los
datos; no lo escogemos libremente.

Ahora comparamos nuestras acciones y buscamos la de mayor valor. El
modelo completo es:

$$
\begin{aligned}
\max_a\quad &\min_{b\in B(a)}U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}
$$

**El máximo representa nuestra elección; el mínimo representa la respuesta
rival.** Escribir una sola maximización sobre $a$ y $b$ nos daría control
sobre ambos jugadores y cambiaría el problema.

Los conjuntos $A$ y $B(a)$ recogen los dominios y todas las reglas sobre
jugadas permitidas. No hacen falta restricciones de recursos adicionales
en el relato del ejemplo guiado.

La combinación de un máximo y un mínimo no demuestra por sí sola que
exista un rival. En el problema de horarios comparábamos molestias sin
suponer que alguien quisiera perjudicarnos. Aquí la interpretación viene
de los intereses y las decisiones del otro jugador.

## 3 · Usar la tabla del juego pequeño

En la primera parte del ejemplo guiado usamos $G$ por Guardar y $S$ por Sacrificar:

$$A=\{G,S\},\qquad B(G)=B(S)=\{I,D\}.$$

La tabla fija nuestras utilidades finales, en puntos. Las columnas I y D
son las respuestas del rival.

| Acción | I | D |
|---|---:|---:|
| Guardar | +1 | −1 |
| Sacrificar | +1 | +1 |

Con estos datos, el modelo es:

$$\max_{a\in\{G,S\}}\min\{U(a,I),U(a,D)\}.$$

Al comprobar qué valor atribuye a cada acción obtenemos:

$$v(G)=\min\{1,-1\}=-1,\qquad v(S)=\min\{1,1\}=1.$$

Así, el modelo elige Sacrificar. Si usáramos el mejor resultado de cada
fila, ambas acciones recibirían un 1. Ese empate ocultaría que Guardar
permite al rival derrotarnos.

**La puntuación y la conducta rival son dos supuestos distintos.** La
puntuación elegida solo distingue ganar de perder; no valora fichas ni
duración. La conducta supuesta dice que el rival siempre elige una
respuesta que nos deja la menor utilidad posible.

Podríamos querer aprovechar los errores de un rival que conocemos. Para
eso necesitaríamos datos sobre cómo responde. Si dispusiéramos de
probabilidades justificadas $\pi(b\mid a)$ —la probabilidad de su respuesta
$b$ después de ver $a$—, podríamos plantear otro modelo:

$$
\begin{aligned}
\max_a\quad &\sum_{b\in B(a)}\pi(b\mid a)U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}
$$

Esas probabilidades serían datos no negativos que suman uno para cada
acción $a$. El objetivo compararía puntuaciones promedio según esa conducta.
La tabla de victorias y derrotas, por sí sola, no proporciona esas
probabilidades: en el ejemplo guiado no podemos justificar ese promedio.

## 4 · Contar fichas cuando dejamos de mirar antes del final

En la segunda parte del ejemplo guiado, el programa examina solo la posición que queda después
de nuestra acción y de la respuesta rival. La llamamos $s(a,b)$.

Una función fija $h(s)$ asigna una puntuación a cada posición. El programa
del ejemplo guiado cuenta nuestras fichas, así que **$h$ se mide en fichas**.
No mide los puntos que obtendremos al ganar o perder.

Para una acción $a$, el programa toma la menor puntuación entre las
posiciones que puede dejar el rival:

$$\min_{b\in B(a)}h(s(a,b)).$$

Después elige la acción con mayor valor. El modelo completo de su
recomendación es:

$$
\begin{aligned}
\max_a\quad &\min_{b\in B(a)}h(s(a,b))\\
\text{sujeto a}\quad &a\in A.
\end{aligned}
$$

Esta fórmula expresa la regla dada al programa. Reemplazar $U$ por $h$
conserva la forma de comparar las respuestas, pero cambia qué intenta
conseguir. Ni la posición ni su puntuación pueden elegirse por separado:
quedan determinadas por las jugadas y por la función fijada.

En el ejercicio conservamos $A=\{G,S\}$ y $B(a)=\{I,D\}$. Las columnas I y D
son las respuestas del rival; los valores se miden en fichas.

| Acción | I | D |
|---|---:|---:|
| Guardar | 3 | 2 |
| Sacrificar | 0 | 0 |

Sustituir estos datos da:

$$\max_{a\in\{G,S\}}\min\{h(s(a,I)),h(s(a,D))\}.$$

Los valores que compara el programa son:

$$\min_{b\in\{I,D\}}h(s(G,b))=\min\{3,2\}=2,$$

$$\min_{b\in\{I,D\}}h(s(S,b))=\min\{0,0\}=0.$$

Recomienda Guardar. Nosotros podemos **auditar esa recomendación**, es decir,
comprobarla usando también la tabla de resultados finales. Esa tabla muestra
que Guardar permite al rival hacernos perder.

El programa aplicó correctamente su regla. El problema es que tener más
fichas no garantiza una victoria. Este ejemplo permite ver la diferencia
porque conocemos los resultados finales; en un juego más grande quizá
no los conoceríamos para hacer una comprobación completa.

## 5 · Distinguir victorias y derrotas inevitables

Podemos ampliar el ejemplo guiado con señales observables que permiten comprobar si una posición
lleva inevitablemente a ganar o a perder. Podemos usarlas para construir
otra puntuación.

En este juego pequeño, una comprobación local certifica llegada inevitable a
la meta tras Guardar–I y tras las dos respuestas a Sacrificar. Tras Guardar–D,
certifica un bloqueo que termina en derrota. Suponemos disponibles esas señales
para esta ampliación; contar fichas por sí solo no las proporciona.

Definimos $W(s)$ y $D(s)$ como indicadores conocidos que toman valores en
$\{0,1\}$:

- $W(s)=1$ cuando la señal certifica una victoria inevitable; vale 0 en
  otro caso.
- $D(s)=1$ cuando la señal certifica una derrota inevitable; vale 0 en
  otro caso.

Ambas señales no pueden estar activas a la vez. Para asignar +1 a una
victoria certificada y −1 a una derrota certificada, usamos:

$$h'(s)=W(s)-D(s).$$

Esta función usa la escala de utilidad, no una cantidad de fichas. El
modelo completo con la nueva puntuación es:

$$\max_{a\in A}\min_{b\in B(a)}h'(s(a,b)).$$

Con los conjuntos $A=\{G,S\}$ y $B(a)=\{I,D\}$, las señales dadas producen
los siguientes valores, en la escala de utilidad. Las columnas I y D son
las respuestas del rival.

| Acción | I | D |
|---|---:|---:|
| Guardar | +1 | −1 |
| Sacrificar | +1 | +1 |

El modelo de esta ampliación queda:

$$\max_{a\in\{G,S\}}\min\{h'(s(a,I)),h'(s(a,D))\}.$$

Ahora recomienda Sacrificar, de acuerdo con los resultados finales. Las
puntuaciones se justifican por las señales y por lo que sabemos que
significan; no basta con cambiarlas hasta que salga la jugada que preferimos.

**Un cero exige cuidado.** Si ninguna señal se activa, tenemos
$W(s)=D(s)=0$ y, por tanto, $h'(s)=0$. Eso indica que no certificamos ni una
victoria ni una derrota. No es un empate demostrado.

En un juego grande, detectar una victoria forzada puede requerir examinar
muchas jugadas posteriores. Si las señales no bastan, necesitaremos mirar
más lejos o justificar una valoración aproximada, también llamada
*heurística*. Esa aproximación no garantiza conservar la decisión que
tomaríamos con todos los resultados finales conocidos.

Para usar otras características de la posición, hay que explicar su
relación con ganar, fijar su escala y buscar casos en que engañen. Los
parámetros de esa valoración deben estar fijados al elegir la jugada:
si pudiéramos ajustarlos libremente junto con ella, podríamos mejorar
la puntuación sin mejorar la posición.

## 6 · Representar más turnos de juego

Si los jugadores vuelven a decidir después de las dos primeras acciones,
necesitamos representar también esos turnos. Podemos dibujar cada posición
como un nodo y cada jugada posible como una arista hacia otra posición.

En nuestros turnos buscamos valores altos; en los del rival, suponemos que
él busca valores bajos para nosotros. Esa alternancia conduce a la
formulación **minimax**. En las posiciones donde el juego ya terminó
conocemos la utilidad; si dejamos de explorar antes, usamos una función
para evaluar la posición.

El [texto de Berkeley sobre minimax y evaluaciones limitadas por profundidad](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html) desarrolla esa distinción.
Más adelante estudiaremos cómo recorrer esos árboles y cuándo la poda
alfa–beta permite omitir ramas.

Por ahora importa saber **qué puntuación estamos comparando y por qué**.
Resolver exactamente el modelo no corrige una puntuación que premia
conservar fichas cuando lo que queríamos era ganar.

[[opt-objetivo-juego-practica|Volver al ejemplo guiado]] · [[opt-construir-objetivo|Volver al banco de práctica]].
