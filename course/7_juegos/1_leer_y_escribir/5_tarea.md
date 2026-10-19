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

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin ayuda** lo de la clase: ordenar unas reglas, escribir el modelo completo y diagnosticarlo.

- **El primer ejercicio** pide escribir el modelo de gato.
- **El segundo ejercicio** cambia una sola regla de hexapawn.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

---

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
Aquí X y O son las marcas del gato, no conjuntos; X será MAX y O será MIN.

1. **Ordena las reglas.** Identifica qué sobra, qué falta, qué es ambiguo y qué es redundante; anota tus supuestos.
2. **Escribe las siete piezas.** Define $S$, $s_0$, $S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$, con el dominio de cada función y $U$ en puntos de X (MAX).
3. **Revisa el turno.** El estado lo guarda; explica si un programa podría recuperarlo contando marcas y por qué conservamos el par en el modelo.
4. **Diagnostica el juego.** Contesta las cuatro preguntas de [[diagnosticar-el-juego|Diagnosticar el juego]] y di qué modelo le toca.
5. **Compara árbol y grafo.** Explica cuál tiene más nodos y por qué, sin hacer cuentas.
6. **Revisa si cabe.** Toma como dato que su árbol tiene 549 946 nodos y explica por qué cabe completo.
7. **Reconoce un límite.** Di algo que este análisis del juego no captura.
:::

::: hint {#jue-tarea-1-pista-gato-a of="jue-tarea-1-ej-gato" title="Pista 1 · Las trampas"}
**Revisa qué aporta cada mensaje.** Usa las cuatro preguntas de [[leer-el-reglamento|Leer el reglamento]]: cómo empieza y qué jugadas hay, cómo cambia el tablero, cuándo termina y cuánto vale.

- **Para encontrar la ambigüedad**, pregúntate qué cuenta como «línea».
- **Para encontrar lo que falta**, intenta hacer la primera jugada.
:::

::: hint {#jue-tarea-1-pista-gato-b of="jue-tarea-1-ej-gato" title="Pista 2 · El turno"}
**Cuenta las marcas suponiendo que empieza X.** Si se alternan, ¿qué turno corresponde cuando hay tantas X como O, y puede haber dos O más que X?
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Cada mensaje del chat** tiene una etiqueta: entra, sobra, falta, ambiguo o redundante.
- **Tus supuestos** están escritos como supuestos, no como reglas.
- **Las siete piezas** están completas y $U$ está en puntos de X (MAX).
- **El turno** está en el estado, y dijiste cómo podría recuperarse contando marcas.

::: answer {#jue-tarea-1-resp-gato of="jue-tarea-1-ej-gato" title="Respuesta · El modelo de gato"}
**1 · Ordenar las reglas.**

- **Sobra la servilleta del mensaje 1.** No cambia jugadas, tablero, final ni puntos; la cuadrícula de 3×3 sí entra.
- **Falta quién empieza.** Suponemos que empieza X y lo anotamos.
- **Es ambiguo «tres en línea», del mensaje 4.** Suponemos que cuentan las 3 filas, las 3 columnas y las 2 diagonales: 8 líneas en total.
- **Es redundante el mensaje 3.** «En una casilla vacía», del mensaje 2, ya impide poner una marca sobre otra.

**2 · Reunir el modelo.**

**X es MAX y O es MIN.** El estado es $\mathbf{s=(\text{cuadrícula},\text{turno})}$: la cuadrícula da a cada una de las 9 casillas X, O o · (vacía), y el turno es X u O.

| Pieza | Dominio | En gato |
|---|---|---|
| $S$ | — | Pares alcanzables desde $s_0$ |
| $s_0$ | — | Vacía, turno de X |
| $S_F$ | — | Hay línea o está llena |
| $\mathrm{Pl}$ | $S\setminus S_F$ | Lee el turno: X es MAX, O es MIN |
| $A$ | $S\setminus S_F$ | Las casillas vacías |
| $T$ | $s\notin S_F$, $a\in A(s)$ | Pone en $a$ la marca del turno y lo pasa |
| $U$ | $S_F$ | $+1$ si X hizo línea, $-1$ si O, $0$ si se llenó sin línea |

**3 · Guardar el turno.**

- **El modelo conserva el par.** Como en [[escribir-el-juego|Escribir el juego]], el estado guarda el turno y $\mathrm{Pl}(s)$ lo lee.
- **Contar marcas es una compresión posible.** Como empieza X y se alternan, el turno guardado es X cuando hay tantas X como O, y O cuando hay una X más.
- **La computadora lo comprobó en los 5478 tableros alcanzables.** Un programa podría recuperar el turno contando, pero el modelo sigue siendo el par.
- **La compresión no sirve para todos los juegos.** En ajedrez, el mismo tablero puede corresponder a distintos turnos; hace falta guardar quién mueve.

**4 · Diagnosticar el juego.**

| Pregunta | Gato |
|---|---|
| ¿Por turnos o a la vez? | Por turnos |
| ¿Decide el azar algo? | No |
| ¿Cada uno ve todo? | Sí |
| ¿Son dos y uno pierde lo que gana el otro? | Sí: suma cero |

Le toca un **árbol con nodos MAX y MIN**, como a hexapawn.

**5 · Comparar árbol y grafo.**

**El árbol tiene más nodos**, porque distintos órdenes llegan al mismo estado. X en una esquina, O al centro y X en la esquina opuesta deja lo mismo que poner primero la esquina opuesta.

La computadora cuenta:

| Qué se cuenta | Total |
|---|---:|
| Nodos del árbol | 549 946 |
| Partidas completas | 255 168 |
| Tableros distintos | 5478 |

Cada tablero alcanzable tiene un único turno compatible con las reglas, así que esos 5478 tableros corresponden también a los estados del grafo.

**6 · Ver si cabe.**

**Sí cabe.** Cada jugada llena una casilla, así que ninguna partida dura más de 9 jugadas. Medio millón de nodos, y menos de 6000 estados en el grafo, caben completos en una computadora; el árbol del ajedrez, no.

**7 · Reconocer un límite.**

**El valor $V$ supone juego óptimo de ambos.** No dice cómo aprovechar a un rival que se equivoca seguido.
:::

---

## 2 · Hexapawn donde quedarse sin jugada es empate

Ahora cambiamos una sola regla de hexapawn; todo lo demás sigue igual.

> **Las reglas originales.** El tablero es de 3×3; Blancas (B, MAX) empieza en la fila 1 y Negras (N, MIN), en la fila 3. Empiezan Blancas.
>
> Un peón avanza una casilla si está vacía o captura en diagonal hacia delante. Gana quien llega a la fila rival, captura todos los peones rivales o deja al rival sin jugada.
>
> **El pago se mide desde MAX:** $U=+1$ si gana Blancas y $U=-1$ si gana Negras.

> **La regla nueva.** Si nadie llegó ni capturó todos los peones rivales y al jugador de turno no le queda ninguna jugada, la partida termina en **empate**, con $U=0$.
>
> **Lo que cambia:** dejar al rival sin jugada ya no da la victoria.

En ajedrez, quedarse sin jugada legal sin estar en jaque se llama *ahogado* y también es empate.

::: exercise {#jue-tarea-1-ej-empate title="Cambia una regla de hexapawn"}
1. **Revisa las siete piezas.** Separa cuáles cambian y cuáles se conservan; escribe la nueva versión de las que cambian.
2. **Compara los tamaños.** Explica si cambian el número de estados del juego y el número de nodos del árbol.
3. **Busca un ejemplo.** Encuentra un tablero donde la nueva regla cambie el resultado.
4. **Interpreta el valor.** Toma como dato que en el juego original $V(s_0)=-1$, por lo que MAX pierde bajo juego óptimo de ambos; ¿basta leer la regla nueva para saber si ese valor se conserva?
5. **Diagnostica la variante.** Explica si cambia el modelo que le toca y por qué el árbol sigue cabiendo completo.
6. **Reconoce un límite.** Di qué no permite concluir la respuesta al inciso 4.
:::

::: hint {#jue-tarea-1-pista-empate-a of="jue-tarea-1-ej-empate" title="Pista 1 · Qué toca la regla"}
**La regla habla de cómo termina una partida y de cuánto vale.** ¿Dice algo sobre qué jugadas hay o cómo se mueve un peón?
:::

::: hint {#jue-tarea-1-pista-empate-b of="jue-tarea-1-ej-empate" title="Pista 2 · Un tablero para el inciso 3"}
**Busca un caso donde alguien se quede sin jugada.** Revisa los ejercicios de [[escribir-el-juego|Escribir el juego]].
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Lo que cambia y lo que se conserva** está separado pieza por pieza.
- **El nuevo pago terminal** tiene tres casos que no se contradicen en un mismo final.
- **Los conteos** tienen una justificación: explicaste por qué se mantienen o cambian.

::: answer {#jue-tarea-1-resp-empate of="jue-tarea-1-ej-empate" title="Respuesta · Qué cambia y qué no"}
**1 · Separar lo que cambia.**

- **Se conservan $S$, $s_0$, $S_F$, $\mathrm{Pl}$, $A$ y $T$.** Las jugadas, el movimiento de los peones y los estados donde termina la partida son los mismos.
- **Solo cambia $U$**, en los finales donde el jugador de turno no tenía jugada.
- **Los casos se revisan en orden.** Primero llegar, luego capturar todo y, solo si no pasó nada de eso, quedarse sin jugada.

**El nuevo pago, siempre desde MAX.**

- **MAX gana:** $\mathbf{U(s)=+1}$ si Blancas llegó o capturó todo.
- **MAX pierde:** $\mathbf{U(s)=-1}$ si Negras llegó o capturó todo.
- **Hay empate:** $\mathbf{U(s)=0}$ si nadie llegó ni capturó todo y al jugador de turno no le queda jugada.

**2 · Comparar los tamaños.**

**Los conteos no cambian:** siguen siendo **252 nodos y 135 estados**. La partida se detiene en los mismos estados; solo cambia el pago de algunos finales.

De los **65 estados finales, en 8 nadie llegó** ni capturó todos los peones rivales y el jugador de turno no tiene jugada. Esos 8 pasan de victoria a empate.

**3 · Mostrar un tablero.**

**Tras a1-a2, b3-b2 y c1-c2, Negras no puede mover.** El tablero queda así:

| Fila | a | b | c |
|---|:---:|:---:|:---:|
| 3 | N | · | N |
| 2 | B | N | B |
| 1 | · | B | · |

**Antes ganaba MAX; ahora empata.** El pago para Blancas pasa de $+1$ a $0$.

**4 · Recalcular, no adivinar.**

**Leer la regla no basta para conocer el nuevo valor.** Cambiar el pago de 8 finales puede cambiar qué jugadas convienen en los estados anteriores.

Hay que **recalcular desde los finales hacia atrás**. La computadora lo hizo:

| Regla | Valor inicial |
|---|---:|
| Sin jugada, pierde. | $\mathbf{V(s_0)=-1}$ |
| Sin jugada, empata. | $\mathbf{V(s_0)=0}$ |

Con la regla nueva, **MAX empata si ambos juegan lo mejor posible**.

**5 · Diagnosticar la variante.**

**Le toca el mismo árbol finito con nodos MAX y MIN**, y sigue cabiendo con sus 252 nodos y 135 estados. Cambiaron los datos de los finales, no la forma del juego.

**6 · Reconocer un límite.**

**El valor 0 supone juego óptimo de ambos.** No predice todas las partidas: si Negras se equivoca, Blancas podría ganar.
:::

---

**Punto de control:** deberías poder escribir las siete piezas de un juego nuevo a partir de unas reglas confusas, diagnosticarlo y decir qué piezas cambian al modificar una regla.

## Lo que hay que llevarse

- **Escribir un juego es siempre lo mismo:** ordenar las reglas, anotar los supuestos y llenar las siete piezas.
- **El estado guarda el turno y $\mathrm{Pl}(s)$ lo lee.** En gato se podría recuperar contando marcas; en ajedrez, no.
- **Diagnosticar dice qué modelo toca y si cabe.** Gato y hexapawn piden un árbol con nodos MAX y MIN, y los dos caben completos.
- **Cambiar una regla de final cambia los datos, no la forma del modelo.** Pero saber quién gana obliga a recalcular: en hexapawn, $V(s_0)$ pasa de $-1$ a $0$.

Continúa con [[juegos-mirar-todo-y-podar|la clase 2]].
