---
id: tarea-leer-y-escribir
title: "Tarea de refuerzo · Escribir un juego"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: escribir gato desde unas reglas confusas y cambiar una regla de hexapawn para ver qué parte del modelo cambia."
status: ready
estimated_time: 40m
tags: [juegos, modelado, practica]
---

# Tarea de refuerzo · Escribir un juego

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin
ayuda** lo de la clase: ordenar unas reglas y escribir el modelo completo.

El primer ejercicio es un juego nuevo. El segundo cambia una sola regla de
hexapawn.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

## 1 · Escribir gato desde unas reglas confusas

Alguien te explica gato (tres en raya) por chat:

> **[1]** Se juega en una cuadrícula de 3×3; yo lo juego en una servilleta.
>
> **[2]** Uno pone X y el otro pone O, por turnos, en una casilla vacía.
>
> **[3]** No puedes poner tu marca donde ya hay otra.
>
> **[4]** Gana el que haga tres en línea.
>
> **[5]** Si se llena la cuadrícula y nadie hizo línea, nadie gana.
>
> **[6]** Ganar vale 1 punto, empatar 0 y perder −1.

::: exercise {#jue-tarea-1-ej-gato title="Escribe el modelo de gato"}
1. Ordena el chat: qué mensaje **sobra**, qué **falta**, qué mensaje es
   **ambiguo** y cuál es **redundante**. Anota tus supuestos.
2. Escribe las siete piezas del modelo: $S$, $s_0$, $S_F$, $\mathrm{Pl}$,
   $A$, $T$ y $U$, con $U$ en puntos de X. Para cada función, di su dominio.
   (Aquí X y O son las marcas del gato, no conjuntos.)
3. ¿Hace falta guardar en el estado a quién le toca, o se puede deducir del
   tablero? Justifica tu respuesta.
4. Diagnostica gato con las cuatro preguntas y di qué modelo le toca.
5. ¿Qué tendría más nodos: el árbol de partidas o el grafo de estados?
   Explica por qué sin contar.
6. ¿Con qué método se resolvería y cuánto trabajo costaría, en orden de
   magnitud?
7. Di un límite del modelo: algo que no captura.
:::

::: hint {#jue-tarea-1-pista-gato-a of="jue-tarea-1-ej-gato" title="Pista 1 · Las trampas"}
Pasa cada mensaje por las cuatro preguntas: qué jugadas hay, cómo cambia el
tablero, cuándo termina y cuánto vale. Para lo ambiguo, pregúntate qué
cuenta como «línea». Para lo que falta, intenta hacer la primera jugada.
:::

::: hint {#jue-tarea-1-pista-gato-b of="jue-tarea-1-ej-gato" title="Pista 2 · El turno"}
Cuenta las marcas. Si en el tablero hay tantas X como O, ¿quién jugó la
última vez? ¿Puede haber dos O más que X?
:::

::: answer {#jue-tarea-1-resp-gato of="jue-tarea-1-ej-gato" title="Respuesta · El modelo de gato"}
**1. Separar lo que entra de lo que no.**

- **Sobra** la servilleta del mensaje 1: no cambia jugadas, tablero, final
  ni puntos. La cuadrícula de 3×3 sí entra.
- **Falta** quién empieza. Suponemos que **empieza X** y lo anotamos.
- **Ambiguo** es «tres en línea» del mensaje 4: ¿cuentan las diagonales?
  Decidimos que **sí**: valen las 3 filas, las 3 columnas y las 2 diagonales,
  8 líneas en total.
- **Redundante** es el mensaje 3: «en una casilla vacía», del mensaje 2, ya
  lo dice.

**2. Reunir el modelo.**

| Pieza | En gato |
|---|---|
| $S$ | Pares (cuadrícula, turno) alcanzables desde $s_0$; la cuadrícula es una función de las 9 casillas a $\{X,O,\cdot\}$ |
| $s_0$ | Cuadrícula vacía, le toca a X |
| $S_F$ | Alguien tiene una de las 8 líneas, o la cuadrícula está llena |
| $\mathrm{Pl}$ | $S\setminus S_F\to\{\text{MAX},\text{MIN}\}$: MAX (X) si hay tantas X como O; MIN (O) si hay una X más |
| $A$ | $S\setminus S_F\to$ conjuntos no vacíos de casillas: las casillas vacías |
| $T$ | $\{(s,a): s\notin S_F,\ a\in A(s)\}\to S$: pone la marca del jugador de turno en la casilla $a$ y pasa el turno |
| $U$ | $S_F\to\mathbb{R}$: $+1$ si X hizo línea, $-1$ si la hizo O, $0$ si se llenó sin línea |

**3. Decidir qué guarda el estado.** El turno se deduce. X empieza y se alternan, así que en todo tablero
alcanzable hay tantas X como O, o una X más. Si hay tantas, le toca a X; si
hay una más, a O. El estado puede ser solo la cuadrícula. La computadora lo
comprobó en los 5478 tableros alcanzables. Esto **no** vale en ajedrez,
donde la misma posición puede tocarle a cualquiera: ahí hay que guardar el
turno.

**4. Diagnosticar.** Por turnos, sin azar, todo visible y suma cero: le toca
un **árbol con nodos MAX y MIN**, como a hexapawn.

**5. Comparar árbol y grafo.** El árbol tiene muchos más nodos, porque un
mismo tablero se alcanza poniendo las mismas marcas en distinto orden. Por
ejemplo, X en una esquina, O en el centro y X en la esquina opuesta deja el
mismo tablero que poner primero la esquina opuesta. La computadora cuenta
**549 946 nodos** en el árbol, **255 168 partidas** distintas y solo
**5478 tableros** distintos.

**6. Tipo de modelo, método y costo.** Juego por turnos, finito,
determinista, de información perfecta y suma cero. Se resuelve con minimax,
que verás en la clase 2: recorrer el árbol cuesta del orden de sus 549 946
nodos; recordando tableros ya valorados, del orden de 5478.

**7. Límite.** El modelo supone que los dos juegan lo mejor posible. No dice
cómo aprovechar a un rival que se equivoca seguido.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Cada mensaje del chat tiene una etiqueta: entra, sobra, falta, ambiguo o
  redundante.
- Escribiste tus supuestos como supuestos, no como reglas.
- Tienes las siete piezas, y $U$ está en puntos de X.
- Dijiste por qué el turno se puede o no se puede deducir.

## 2 · Hexapawn donde quedarse sin jugada es empate

Ahora cambiamos una sola regla de hexapawn. Todo lo demás sigue igual:
tablero, peones, cómo se mueven, quién empieza y que ganar vale $+1$ y perder $-1$.

> **La regla nueva.** Si a un jugador le toca y no tiene ninguna jugada, la
> partida termina en **empate**, que vale $0$.

Es la regla del ajedrez, donde quedarse sin jugada sin estar en jaque se
llama *ahogado*.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.
>
> **Lo que cambia en este ejercicio:** «deja al rival sin jugada» ya no es
> victoria; es empate y vale 0.

::: exercise {#jue-tarea-1-ej-empate title="Cambia una regla de hexapawn"}
1. De las siete piezas del modelo, ¿cuáles cambian y cuáles no? Para las que
   cambian, escribe la versión nueva.
2. ¿Cambia el número de estados del juego? ¿Y el número de nodos del árbol?
3. Encuentra un tablero donde la regla nueva cambia el resultado.
4. En el juego original, Negras gana si las dos juegan perfecto (lo
   calcularás en la clase 2; por ahora tómalo como dato). ¿Puedes saber,
   solo leyendo la regla nueva, si eso sigue siendo cierto?
5. ¿Cambia el tipo de modelo o el método para resolverlo?
6. Di un límite de la respuesta del inciso 4.
:::

::: hint {#jue-tarea-1-pista-empate-a of="jue-tarea-1-ej-empate" title="Pista 1 · Qué toca la regla"}
La regla nueva habla de cómo **termina** una partida y de cuánto **vale**
terminar así. ¿Dice algo sobre qué jugadas hay o sobre cómo se mueve un peón?
:::

::: hint {#jue-tarea-1-pista-empate-b of="jue-tarea-1-ej-empate" title="Pista 2 · Un tablero para el inciso 3"}
¿En algún ejercicio de esta clase alguien se quedó sin jugada? Busca en la
página [[escribir-el-juego|Escribir el juego]].
:::

::: answer {#jue-tarea-1-resp-empate of="jue-tarea-1-ej-empate" title="Respuesta · Qué cambia y qué no"}
**1. Separar lo que cambia de lo que no.** No cambian $S$, $s_0$, $S_F$,
$\mathrm{Pl}$, $A$ ni $T$: la partida termina en los mismos estados que
antes, y las jugadas y el movimiento de los peones son los mismos. **Solo
cambia $U$**, en los finales donde la partida acabó porque el jugador de
turno no tenía jugada. Los casos se revisan **en orden**: primero llegar,
luego capturar todo y solo si no pasó nada de eso, quedarse sin jugada.

$$U(s)=\begin{cases}+1 & \text{si Blancas llegó o capturó todo},\\
-1 & \text{si Negras llegó o capturó todo},\\
\phantom{-}0 & \text{si nadie llegó ni capturó todo y al jugador de turno no le queda jugada}.\end{cases}$$

**2. Contar.** Los conteos no cambian. Una partida termina en los mismos
tableros que antes; solo cambia el dato de $U$ en algunos finales. Siguen
siendo 252 nodos y 135 estados. De los 65 estados finales, en 8 nadie llegó
ni capturó todo y el jugador de turno no tiene jugada: esos 8 pasan de
victoria a empate.

**3. Usar los datos en un tablero.** Tras a1-a2, b3-b2 y c1-c2, Negras no puede
mover. Antes ganaba Blancas y valía $+1$; ahora es empate y vale 0.

**4. Recalcular, no adivinar.** No basta con leer la regla. Cambiar el valor de 8 finales puede
cambiar qué jugadas convienen antes, en cualquier parte del árbol. Para
saberlo hay que **recalcular** desde los finales hacia atrás, que es lo que
hace la clase 2. La computadora lo hizo: con la regla nueva, si las dos
juegan perfecto, la partida termina en **empate**, con valor 0.

**5. Tipo de modelo, método y costo.** El mismo: un árbol finito con nodos
MAX y MIN, que se resuelve con minimax recorriendo sus 252 nodos, o 135
estados con memoria. Cambiaron los datos de los finales, no la forma del
juego.

**6. Límite.** El nuevo valor, 0, también supone juego perfecto de las dos.
Si Negras se equivoca, Blancas podría ganar.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Separaste lo que cambia de lo que no, pieza por pieza.
- Escribiste la utilidad nueva con sus tres casos, sin que dos casos se
  contradigan en un mismo final.
- Explicaste por qué los conteos se mantienen o cambian.

**Punto de control:** deberías poder escribir las siete piezas de un juego
nuevo a partir de unas reglas confusas y decir qué piezas cambian si cambia
una regla.

## Lo que hay que llevarse

- Escribir un juego es siempre lo mismo: ordenar las reglas, anotar los
  supuestos y llenar las siete piezas.
- Lo que guarda un estado depende del juego: en gato el turno se deduce del
  tablero; en ajedrez no.
- Cambiar una regla de final cambia los datos, no la forma del modelo. Pero
  saber quién gana obliga a recalcular.

Continúa con [[juegos-mirar-todo-y-podar|la clase 2]], donde calculamos
por primera vez quién gana.
