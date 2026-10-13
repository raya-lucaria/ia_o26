---
id: elegir-el-algoritmo
title: Elegir el algoritmo
nav_title: Elegir el algoritmo
summary: "Dado un juego, unas cuantas preguntas eligen el algoritmo: si el árbol cabe, si hay dados, si hay una buena evaluación y si hay reloj. Con el juego real donde se usó cada uno, y lo que suponen todos: dos jugadores, suma cero, por turnos y todo a la vista."
status: ready
estimated_time: 25m
tags: [juegos, busqueda-adversarial, mcts]
---

# Elegir el algoritmo

**Dado un juego, ¿qué algoritmo uso?**

Al terminar tendrás:

- dos tablas con **cuándo conviene** cada algoritmo de la unidad y qué le
  cuesta, y en qué juego real se usó;
- un **mapa de decisión** de cuatro preguntas, aplicado al árbol T± y a la
  posición de peones de la clase;
- los cuatro **supuestos** que comparten todos, y qué se usa cuando falla
  alguno;
- un juego nuevo, diagnosticado por ti, con su algoritmo justificado.

> **Lo que traes de [[que-numero-da-cada-uno|Qué número da cada uno]].**
> Tres números distintos. $V$ es el valor exacto del juego; con dados,
> promedia el azar del juego con jugadores óptimos. El valor con corte
> estima con $\mathrm{EVAL}$ donde se corta. $\bar u$ promedia
> simulaciones en las que los dos juegan al azar. Solo $V$ es el valor del
> juego.

> **T±, en tres líneas.** La raíz R es de MAX, con izq, centro y der hacia
> I, C y D, de MIN. Los finales valen ${+1}$, ${-1}$ y hay un solo empate,
> 0. Minimax juega centro con ${V=0}$.

> **Supuestos de esta página.** Los cuatro de toda la unidad: dos
> jugadores, suma cero, por turnos y todo a la vista. El azar, solo donde
> hay dados. La sección 3 los revisa uno por uno.

## 1 · Elegir por lo que tiene el juego

La página anterior dijo qué número da cada algoritmo. Falta lo práctico:
cuál conviene, y en qué juego.

**Piensa: Deep Blue y AlphaGo vencieron a campeones humanos. ¿Por qué no
usaron el mismo algoritmo?**

Porque sus juegos no tienen lo mismo. En ajedrez hay una estimación
razonable que se escribe a mano: contar piezas, con su valor. En Go no hay
una cuenta tan sencilla: un grupo de piedras puede valer mucho o nada según
cómo termine la partida. **Lo que el juego ofrece decide el algoritmo.**

En las dos tablas, cada fila es un algoritmo de la unidad. «Conviene
cuando» dice qué tiene que ofrecer el juego; «Le cuesta», qué paga a cambio.
«Cabe» quiere decir que el árbol entero se recorre en el tiempo que hay.

::: table {#jue-c3-cmp-cuando title="Cuándo conviene cada algoritmo"}
| Algoritmo | Conviene cuando |
|---|---|
| Minimax | Cabe y no hay dados |
| Expectiminimax | Cabe y hay dados |
| Alfa-beta | Cabe y no hay dados |
| Corte, quietud e iterativa | No cabe; hay $\mathrm{EVAL}$ buena |
| Monte Carlo plano | No cabe; no hay $\mathrm{EVAL}$ |
| MCTS con UCT | No cabe; no hay $\mathrm{EVAL}$ |
:::

Dónde se usó cada uno, en el mismo orden:

- **Minimax:** gato.
- **Expectiminimax:** ningún juego de dados famoso cabe; en la clase, el
  ejemplo es T± con un dado en D. El backgammon no cabe: TD-Gammon (1992)
  miraba dos jugadas, promediaba los dados y estimaba con una red.
- **Alfa-beta:** Conecta 4, resuelto en 1988.
- **Corte, quietud e iterativa:** ajedrez (Deep Blue, 1997) y damas
  (Chinook, con bases de finales).
- **Monte Carlo plano:** Go, de 1993 a 2005.
- **MCTS con UCT:** Go (MoGo, 2006) y Hex (MoHex).

::: table {#jue-c3-cmp-cuesta title="Qué le cuesta a cada algoritmo"}
| Algoritmo | Le cuesta |
|---|---|
| Minimax | Del orden de $b^m$ nodos |
| Expectiminimax | Cada dado multiplica las ramas |
| Alfa-beta | Hasta $b^m$, menos ordenando bien |
| Corte, quietud e iterativa | Escribir $\mathrm{EVAL}$; el horizonte |
| Monte Carlo plano | Supone rivales al azar |
| MCTS con UCT | Muchas simulaciones; elegir $c$ |
:::

Monte Carlo plano promedia como si los dos jugaran al azar, y por eso puede
elegir mal. La iterativa y MCTS son las que se interrumpen con el reloj.

Tres matices que las tablas no alcanzan a decir:

- **Deep Blue y Chinook no buscaban hasta los finales**: cortaban y
  estimaban, y por eso no están en las filas de minimax y alfa-beta. Las damas sí se
  resolvieron, en 2007: con juego perfecto son tablas. Tampoco fue
  alfa-beta sola: combinó varias búsquedas con bases de finales.
- **La quietud arregla los intercambios a medias, no todo.** Lo que no es
  captura sigue detrás del horizonte, como viste en
  [[mas-alla-del-horizonte|Más allá del horizonte]].
- **UCT tiende a la jugada de minimax con una $c$ suficientemente grande y
  tiempo sin límite.** La ${c=1}$ del curso queda debajo de esa hipótesis:
  funcionó, pero sin la garantía. Lo viste en
  [[de-donde-sale-el-bono|De dónde sale el bono]].

::: exercise {#jue-c3-cmp-ej-tdgammon title="Ubica a TD-Gammon en la tabla"}
TD-Gammon aparece junto a expectiminimax, porque el backgammon tiene
dados, pero no buscaba hasta los finales.

1. ¿Qué fila de la primera tabla describe mejor lo que hacía?
2. ¿Qué número daba su búsqueda: $V$, valor con corte o $\bar u$?
:::

::: hint {#jue-c3-cmp-pista-tdgammon of="jue-c3-cmp-ej-tdgammon" title="Lo que hacía debajo"}
Cuando dejaba de mirar jugadas, ¿con qué valoraba esa posición? ¿Qué fila
de la tabla hace lo mismo?
:::

::: answer {#jue-c3-cmp-resp-tdgammon of="jue-c3-cmp-ej-tdgammon"}
1. La de **corte, quietud e iterativa**, pero con nodos de azar: miraba dos
   jugadas, promediaba los dados como expectiminimax y estimaba debajo del
   corte con su red, que hacía de $\mathrm{EVAL}$.
2. **Valor con corte**, no $V$. Promediar los dados no lo vuelve exacto: lo
   que queda debajo del corte es una estimación.
:::

La tabla se lee de algoritmo a juego. Con un juego nuevo en la mano hace
falta lo contrario: ¿en qué orden se hacen las preguntas?

## 2 · Recorrer el mapa de decisión

**Piensa: de todas las preguntas de la tabla, ¿cuál hay que hacer primero?**

La de si cabe. Si el árbol cabe, la búsqueda es exacta: ninguna estimación
supera a $V$. Solo falta saber si hay dados, para elegir cuál búsqueda
exacta. Las otras preguntas solo se hacen cuando no cabe. En [[diagnosticar-el-juego|Diagnosticar el juego]] ya era la quinta
pregunta, la que decide el método.

El mapa, en orden:

1. **¿Cabe el árbol en el tiempo que hay?** Sí, sin dados: alfa-beta. Da
   $V$ y la jugada de minimax, con menos nodos que minimax. Sí, con dados:
   expectiminimax, que da el $V$ del juego con dado.
2. **No cabe: ¿hay dados?** Sí: corte con nodos de azar, que se promedian,
   como TD-Gammon.
3. **¿Hay una $\mathrm{EVAL}$ buena?** Sí: alfa-beta con corte. Con
   capturas, quietud; con reloj, profundización iterativa, que entrega la
   última búsqueda completa.
4. **¿No la hay?** MCTS con UCT. Solo pide las reglas, para simular. Se
   interrumpe cuando sea y entrega la jugada más simulada.

Monte Carlo plano es la versión sin árbol de la rama 4: más simple, y puede
elegir mal.

**En T±.** Tiene 15 nodos y no tiene dados: cabe, rama 1. Alfa-beta juega centro con
${V=0}$ y genera 12. Los demás habrían pagado por nada, o algo peor: el corte
a ${d=1}$ elige izq, con 60, y Monte Carlo plano elige der. Si D fuera un
dado, seguiría en la rama 1, ahora con dados: expectiminimax juega der, que vale ${1/3}$.

**En la posición de la clase.** La tratamos como si no cupiera, para hacer
las cuentas a mano. No tiene dados, y en la computadora sí cabe, así que es
la rama 1: su árbol completo tiene 389
nodos, y alfa-beta lo resuelve generando 78. Juega
$\text{d2}\textbf{-}\text{d3}$, que gana: ${V=+1}$. El tablero de 4×4
entero, con 4 197 973 nodos, también cabe; así se sabe que gana el
primero.

Si no cupiera, la posición tiene $\mathrm{EVAL}$: sería la rama 3. El corte a
${d=1}$ elige $\text{d2}\textbf{x}\text{c3}$, con 13, que pierde. Con
quietud elige $\text{d2}\textbf{-}\text{d3}$. Sin $\mathrm{EVAL}$, Monte
Carlo plano también acierta: si desde $\text{d2}\textbf{-}\text{d3}$ los dos
juegan al azar hasta el final, $U$ promedia ${8/9}$, lo más alto de las tres
jugadas.

::: exercise {#jue-c3-cmp-ej-mapa title="Corre el mapa en tres juegos"}
Recorre las cuatro preguntas para cada juego y di en qué rama acaba.

1. Hexapawn, con sus 252 nodos.
2. El ajedrez, con reloj de torneo.
3. El backgammon.
:::

::: hint {#jue-c3-cmp-pista-mapa of="jue-c3-cmp-ej-mapa" title="Por dónde empezar"}
¿En cuál de los tres te detienes en la primera pregunta? En los otros dos,
¿qué tiene uno que el otro no?
:::

::: answer {#jue-c3-cmp-resp-mapa of="jue-c3-cmp-ej-mapa"}
1. **Hexapawn: rama 1.** Cabe y no hay dados; alfa-beta da $V$ exacto.
2. **Ajedrez: rama 3.** No cabe, no hay dados y contar piezas es una
   $\mathrm{EVAL}$ razonable. Alfa-beta con corte, quietud por las capturas
   e iterativa por el reloj: lo de Deep Blue.
3. **Backgammon: rama 2.** No cabe y hay dados: corte con nodos de azar,
   y la estimación que haya debajo. TD-Gammon la aprendió con una red.
:::

El mapa da por hecho que hay dos jugadores, que lo que gana uno lo pierde el
otro, y que todo está a la vista. ¿Qué pasa si no?

## 3 · Lo que supone todo esto

**Piensa: MAX maximiza $U$ y MIN lo minimiza. ¿Por qué MIN se conforma con
el número de MAX en vez de tener uno propio?**

Porque en suma cero no le hace falta. Cada final tiene un solo número, y lo
que gana uno lo pierde el otro. El final que para MAX vale ${-1}$ es el
mejor que le puede pasar a MIN: **el ${-1}$ de MAX es el máximo de MIN**.
Minimizar lo de MAX es maximizar lo suyo, como viste en
[[escribir-el-juego|Escribir el juego]].

Alfa-beta poda por lo mismo. Lo que MAX ya tiene asegurado es justo lo que
MIN ya no le puede quitar, porque los dos miden con el mismo número.

**Con tres jugadores eso se rompe.** Un final en el que tú pierdes puede ser
victoria de B o de C, y a B le importa cuál. Un número ya no basta: cada
final necesita uno por jugador, y lo peor para ti deja de ser lo mejor para
cada rival.

**Con dos jugadores también se rompe, si cada uno tiene su propio pago.**
Dos amigos arman por turnos un rompecabezas, y los dos ganan si lo terminan.
Lo que le conviene a uno le conviene al otro. Minimax supondría que el
compañero quiere arruinarlo, y descartaría una jugada buena solo porque él
podría echarla a perder, aunque nunca lo haría.

Los cuatro supuestos de la unidad, y qué los rompe:

- **Dos jugadores.** Con tres o más no hay un MIN: hay varios rivales, cada
  uno con su meta.
- **Suma cero.** Si cada uno tiene su propio pago, suponer que el otro
  quiere dañarte es un error de modelado. La clase 4 lo retoma:
  [[juegos-sin-turnos|Cuando no hay turnos]].
- **Por turnos.** Si eligen a la vez, ya no hay árbol donde uno responde al
  otro. También es la clase 4.
- **Todo a la vista.** En póker no ves las cartas del rival: no sabes en qué
  nodo estás. Es información oculta, y queda fuera de esta unidad.

**Para ubicar.** Lo que se usa cuando falla un supuesto, o cuando se le
pide más a MCTS. Una línea cada uno; no se estudian en el curso.

- **MCTS-Solver** (Winands, Björnsson y Saito, 2008): propaga hacia arriba
  las victorias y derrotas ya demostradas. No demuestra empates.
- **MCTS con evaluación.** AlphaGo (2016) valora cada hoja mezclando una red
  de valor con una simulación; un peso, λ, decide cuánto cuenta la
  simulación. AlphaGo Zero (2017) y AlphaZero ya no simulan: solo la red,
  y seleccionan con PUCT, un puntaje que suma lo que la red sugiere.
- **$\max^n$** (Luckhardt e Irani, 1986): cada final lleva un número por
  jugador y cada jugador maximiza el suyo. Ahí alfa-beta casi no poda
  (Korf, 1991).
- **Paranoico** (Sturtevant y Korf, 2000): supone que todos los rivales se
  aliaron en tu contra. Vuelven a ser dos bandos y alfa-beta poda otra vez,
  a costa de un supuesto falso.
- **MCTS con varios jugadores** (Sturtevant, 2008): cada nodo guarda un
  promedio por jugador. Lo probó, entre otros juegos, en damas chinas.

::: exercise {#jue-c3-cmp-ej-cartas title="Señala qué supuestos rompe"}
Un juego de cartas para tres: cada uno ve solo su mano, se juega por turnos
y quien hace más puntos gana. ¿Qué supuestos de la unidad rompe, y cuál de
ellos lo deja fuera incluso de la lista «para ubicar»?
:::

::: hint {#jue-c3-cmp-pista-cartas of="jue-c3-cmp-ej-cartas" title="Uno por uno"}
Recorre la lista de los cuatro supuestos. ¿Cuántos jugadores hay? ¿Qué no
ve cada uno?
:::

::: answer {#jue-c3-cmp-resp-cartas of="jue-c3-cmp-ej-cartas"}
Rompe **dos jugadores** (son tres) y **todo a la vista** (las manos están
ocultas). Sigue siendo por turnos. Las herramientas de varios jugadores de
la lista suponen todo a la vista; **la información oculta** lo deja fuera,
como el póker.
:::

Con los supuestos y el mapa ya puedes elegir sin ayuda. Pruébalo en un juego
que no está en ninguna tabla.

## 4 · Elegir en un juego nuevo

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-cmp-ej-fronteras title="Elige el algoritmo para Fronteras"}
**Fronteras** se juega en un tablero de 11×11 casillas, vacío al empezar.
Por turnos, Rojo y Azul pintan una casilla vacía de su color; empieza Rojo.
Una casilla pintada no se borra. La partida acaba cuando no queda casilla
vacía, tras 121 jugadas. Gana quien tenga el grupo más grande de casillas de
su color unidas por un lado. Si los dos grupos miden igual, es empate.

Simplificaciones: no hay dados ni cartas, los dos ven el tablero, y cada
jugada tiene 10 segundos de reloj. Los que lo juegan dicen que contar el
grupo más grande a mitad de partida engaña: un grupo chico bien puesto
termina uniendo dos grandes.

Lo nuevo frente a la página: no hay tabla ni árbol dados; el diagnóstico es
tuyo, y una variante tiene tres jugadores.

1. Contesta: ¿cabe el árbol?, ¿hay dados?, ¿hay una $\mathrm{EVAL}$ buena?,
   ¿hay reloj?, ¿es de suma cero entre dos?
2. Recorre el mapa de la sección 2 y di en qué rama acabas.
3. Di qué jugada entrega tu algoritmo al acabarse el reloj, y qué número la
   respalda. ¿Es $V$?
4. Variante: el tablero es de 3×3. ¿Cambia tu elección?
5. Variante: juegan Rojo, Azul y Verde, por turnos. ¿Qué supuesto se rompe,
   y qué buscarías en la lista «para ubicar»?
:::

::: hint {#jue-c3-cmp-pista-fronteras-1 of="jue-c3-cmp-ej-fronteras" title="Pista 1 · Qué dato contesta cada pregunta"}
Para cada pregunta del punto 1, ¿qué frase del enunciado la contesta? ¿Cuál
no se contesta con las reglas, sino con lo que dicen quienes lo juegan?
:::

::: hint {#jue-c3-cmp-pista-fronteras-2 of="jue-c3-cmp-ej-fronteras" title="Pista 2 · Revisa tu elección"}
Comprueba tu propuesta con dos preguntas. ¿Tu algoritmo necesita algo que
el enunciado no te da? Con tres jugadores, ¿quién haría de MIN?
:::

::: answer {#jue-c3-cmp-resp-fronteras of="jue-c3-cmp-ej-fronteras" title="Respuesta · Simular, porque no hay con qué estimar"}
**1. Las cinco respuestas.** No cabe: hay 121 jugadas y la partida siempre
las juega todas, así que hay ${121!}$ órdenes posibles, un número de 201
cifras. No hay dados. No hay $\mathrm{EVAL}$ buena: la obvia, el grupo más
grande, engaña según quienes lo juegan. Hay reloj: 10 segundos. Y sí es
suma cero entre dos: ${U=+1}$, ${-1}$ o 0, y lo que gana uno lo pierde el
otro.

**2. El mapa.** No cabe, no hay dados, no hay $\mathrm{EVAL}$: **rama 4,
MCTS con UCT**. Simular es fácil: se llena al azar lo que queda y se cuentan
los grupos. Toda simulación acaba, a lo más en 121 jugadas. Es el caso de
Go y Hex en la tabla.

**3. Lo que entrega.** Al acabarse los 10 segundos, la jugada **más
simulada**. La respalda $\bar u$, un promedio de simulaciones, no $V$. Con
tiempo sin límite y una $c$ suficientemente grande tendería a la de
minimax; 10 segundos no son tiempo sin límite.

**4. Tablero de 3×3.** Son 9 jugadas: ${9!=}$ 362 880 partidas.
Cabe: rama 1, alfa-beta, y la jugada sale con su $V$ exacto. El tamaño
cambia la primera respuesta del mapa, y con ella todo lo demás.

**5. Tres jugadores.** Se rompe **dos jugadores**: no hay un solo MIN, y
cada final necesita un número por jugador. Como no hay $\mathrm{EVAL}$
buena, lo cercano de la lista es **MCTS con varios jugadores**. $\max^n$ y
el paranoico llegan a los finales si el árbol cabe; aquí tendrían que
cortar y estimar con una $\mathrm{EVAL}$, y no hay con qué.
:::

**Punto de control:** deberías poder decir, para un juego nuevo, si cabe,
si tiene dados, si hay una $\mathrm{EVAL}$ buena y si hay reloj, elegir el
algoritmo con el mapa y decir qué número respalda su jugada. También,
reconocer cuándo un juego rompe los supuestos de la unidad.

## Lo que hay que llevarse

- **Un árbol, todos los algoritmos.** En T±, minimax juega centro con
  ${V=0}$ en 15 nodos, y alfa-beta lo mismo en 12. El corte a ${d=1}$ elige
  izq, con 60, y la quietud lo corrige: centro. Monte Carlo plano elige der;
  UCT vuelve a centro. Con un dado en D, la jugada es der, que vale
  ${1/3}$.
- **Qué número da cada uno.** $V$ es el valor del juego. El valor con corte
  y $\bar u$ lo estiman, cada uno con su supuesto: $\mathrm{EVAL}$ donde se
  corta, o los dos jugando al azar.
- **Cuándo conviene.** Si cabe, alfa-beta, o expectiminimax si hay dados:
  gato, Conecta 4. Si no cabe y hay una $\mathrm{EVAL}$ buena, corte,
  quietud e iterativa: Deep Blue, Chinook. Si no la hay, MCTS con UCT:
  MoGo, MoHex. Sin caber y con dados, corte con nodos de azar: TD-Gammon.
- **El mapa empieza por «¿cabe?».** La posición de la clase sí cabía en la
  computadora: 389 nodos, 78 con alfa-beta, y $\text{d2}\textbf{-}\text{d3}$
  gana. El corte a ${d=1}$ elegía $\text{d2}\textbf{x}\text{c3}$, con 13.
- **Todo supone dos jugadores, suma cero, por turnos y todo a la vista.** En
  suma cero, el ${-1}$ de MAX es el máximo de MIN. Con tres jugadores o
  pagos propios eso se rompe, y entran $\max^n$, el paranoico o MCTS con
  varios jugadores.

Continúa con [[juegos-sin-turnos|la clase 4, cuando no hay turnos]].
