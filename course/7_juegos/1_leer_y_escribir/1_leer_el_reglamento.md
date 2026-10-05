---
id: leer-el-reglamento
title: Leer el reglamento
nav_title: Leer el reglamento
summary: "Unas reglas nunca llegan ordenadas: llegan con frases de más, huecos, ambigüedades y repeticiones. Esta página solo las lee y las ordena."
status: ready
estimated_time: 15m
tags: [juegos, modelado]
---

# Leer el reglamento

**¿Qué dicen de verdad estas reglas?**

Aquí no se juega ni se calcula nada: se lee y se ordena. Al terminar tendrás
**las reglas de hexapawn en limpio**, con cada supuesto anotado.

## Las reglas, como llegan

Hexapawn se juega en un tablero pequeño, con tres peones por lado. Alguien
que ya juega te lo explica por chat, con prisa, antes de un torneo de la
facultad:

> **[1]** Es como ajedrez, pero solo con peones y en un tablero de 3×3.
>
> **[2]** Cada quien pone sus tres peones en su primera fila.
>
> **[3]** El peón avanza una casilla si está libre. Para comer va en
> diagonal, una casilla hacia delante.
>
> **[4]** Ah, y los peones nunca se mueven hacia atrás.
>
> **[5]** Ganas si llegas a la fila del otro o si te comes todos sus peones.
>
> **[6]** Si a alguien le toca y no puede mover, ahí se acaba.
>
> **[7]** En el torneo, ganar te da un punto y perder te lo quita.
>
> **[8]** El que pierde invita los cafés.

Para hablar de los dos jugadores, llamamos **Blancas** (B) al que empieza
abajo y **Negras** (N) al de arriba.

Léelo otra vez y fíjate en tres cosas.

- **El orden no ayuda.** Lo que hace terminar una partida aparece en dos
  mensajes separados, el 5 y el 6.
- **Hay mensajes que no cambian el juego.** Alguno se puede borrar sin que
  cambie una sola partida.
- **Falta algo.** Con lo que dice el chat no se puede hacer la primera
  jugada.

## 1 · Cuatro preguntas para decidir si una frase entra

**Piensa: ¿qué tiene que decir una frase para que cambie el juego?**

Una frase entra al modelo solo si contesta una de estas cuatro preguntas:

1. ¿Qué **jugadas** se permiten?
2. ¿Cómo **cambia el tablero** después de una jugada?
3. ¿**Cuándo termina** la partida y quién gana?
4. ¿**Cuánto vale** terminar así?

Las tres primeras describen el juego; la cuarta dice qué quiere cada
jugador. En la unidad de optimización, la cuarta era la función objetivo.
Aquí se llama **utilidad**.

## 2 · Las cuatro trampas

Unas reglas reales tienen los mismos tres defectos que
[[leer-la-bitacora|la bitácora de la nave]], y uno más: la regla redundante.

::: table {#jue-c1-trampas title="Lo que una explicación con prisa le hace a quien la lee"}
| Trampa | Qué es | Qué se hace |
|---|---|---|
| **Sobra** | Una frase que no contesta ninguna de las cuatro preguntas | Se descarta, diciendo por qué |
| **Falta** | Algo sin lo cual no se puede jugar | Se supone y **se anota el supuesto** |
| **Ambigua** | Una frase que dos personas pueden leer distinto y las dos tener razón | Se decide una lectura y se justifica |
| **Redundante** | Una regla que ya está implicada por otra | Se nota y no se escribe dos veces |
:::

La redundante no es un error grave, pero escribirla dos veces es peligroso:
si un día cambias una copia y no la otra, el modelo se contradice.

## 3 · Tu turno

::: exercise {#jue-c1-ej-reglamento title="Ordena el chat"}
Usa las cuatro preguntas de la sección 1 con cada mensaje del chat.

1. Escribe **qué mensaje sobra** y por qué.
2. Escribe **qué falta** para poder empezar una partida, y qué supones.
3. Encuentra **al menos un mensaje ambiguo**: escribe las dos lecturas
   posibles y cuál eliges.
4. Escribe **qué mensaje es redundante** y qué otro mensaje ya lo implica.
5. Escribe la **utilidad** del mensaje 7 para una partida que gana Blancas
   y para otra que gana Negras, medida desde el lado de Blancas. ¿Importa
   cuántas jugadas duró la partida?
:::

::: hint {#jue-c1-pista-reglamento of="jue-c1-ej-reglamento" title="Un método por pregunta"}
**Para lo que sobra:** pasa cada mensaje por las cuatro preguntas. El que no
contesta ninguna, sobra.

**Para lo que falta:** intenta hacer la primera jugada con lo que dice el
chat. ¿Qué no sabes todavía?

**Para lo ambiguo:** busca un mensaje con el que dos personas podrían jugar
distinto. Fíjate en los que no dicen quién gana, y en los que dicen «como»
otra cosa.

**Para lo redundante:** busca un mensaje que ya se sigue de cómo se mueve un
peón.
:::

::: answer {#jue-c1-resp-reglamento of="jue-c1-ej-reglamento"}
1. **Sobra el mensaje 8.** Invitar los cafés no cambia ninguna jugada, ni el
   tablero, ni el final, ni los puntos del torneo.
2. **Falta quién empieza.** Sin eso no se puede hacer la primera jugada.
   Supondremos que **empiezan Blancas**, como en ajedrez, y lo anotamos como
   supuesto.
3. **Hay dos mensajes ambiguos.**
   - **El 6:** «ahí se acaba» puede leerse como **derrota** de quien no puede
     mover o como **empate**. En ajedrez, quedarse sin jugada sin estar en
     jaque es empate. Elegimos **derrota**, que es la regla de Martin Gardner,
     quien inventó el juego, y lo anotamos.
   - **El 1:** sí entra, porque es el único que fija el tablero de 3×3. Pero
     «es como ajedrez» puede traer reglas del ajedrez que el chat no dice,
     como avanzar dos casillas en la primera jugada. Decidimos que **solo
     valen las reglas escritas**: el peón avanza siempre una casilla.
4. **El mensaje 4 es redundante.** El mensaje 3 ya dice que el peón solo
   avanza o captura hacia delante; moverse hacia atrás no está entre las
   jugadas permitidas.
5. **Utilidad.** Si gana Blancas, recibe $+1$; si gana Negras, Blancas
   recibe $-1$. Lo que gana uno lo pierde el otro. **La duración no importa:**
   el mensaje 7 no dice nada de ella. Premiar ganar rápido sería agregar una
   preferencia que el reglamento no tiene.
:::

> [!WARNING]
> Que un mensaje sea corto no lo hace prescindible. El 4 sobra porque ya
> está dicho; el 8, porque no contesta ninguna de las cuatro preguntas. Son
> motivos distintos, y conviene escribir cuál aplica.

## 4 · El juego, en limpio

Con los supuestos anotados, las reglas quedan así. Ésta es la versión que
usaremos en toda la unidad.

::: table {#jue-c1-hexapawn-inicio title="Hexapawn al empezar"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | N | N |
| **2** | · | · | · |
| **1** | B | B | B |
:::

**Blancas** (B) empieza en la fila 1 y **Negras** (N), en la fila 3. Las
columnas se llaman a, b y c; un punto (·) es una casilla vacía.

1. Juegan por turnos y **empiezan Blancas**. En cada turno se mueve un peón
   propio.
2. Un peón **avanza** una casilla hacia el rival si esa casilla está vacía.
3. Un peón **captura** en diagonal, una casilla hacia delante, si ahí hay un
   peón rival. El peón capturado sale del tablero.
4. Gana quien **llega a la fila del rival**, quien **captura todos** sus
   peones o quien **deja al rival sin jugada** cuando le toca.
5. Ganar vale $+1$ y perder, $-1$.

Y el juego entero cabe en cinco renglones:

::: table {#jue-c1-cinco-renglones title="El juego, en cinco renglones"}
| | En hexapawn |
|---|---|
| **Quién juega** | Blancas y Negras, por turnos; empiezan Blancas |
| **Qué ve cada uno** | El tablero completo; nada está oculto |
| **Qué puede hacer** | Mover uno de sus peones: avanzar o capturar |
| **Cuándo termina** | Cuando alguien llega, captura todo o deja al rival sin jugada |
| **Qué quiere cada uno** | Ganar; lo que gana uno lo pierde el otro |
:::

**Punto de control:** deberías poder tomar cualquier frase de un reglamento
y decir si entra, sobra, falta, es ambigua o es redundante, con la pregunta
que lo decide.

## Lo que hay que llevarse

- Unas reglas reales llegan con frases de más, huecos, ambigüedades y
  repeticiones. Es lo normal.
- Suponer está permitido; **suponer en silencio, no**. Nuestros supuestos:
  empiezan Blancas, quedarse sin jugada es derrota y no hay reglas de ajedrez
  que el chat no diga.
- Una frase entra al modelo solo si dice qué jugadas hay, cómo cambia el
  tablero, cuándo termina o cuánto vale terminar así.

Continúa con [[escribir-el-juego|escribir el juego]].
