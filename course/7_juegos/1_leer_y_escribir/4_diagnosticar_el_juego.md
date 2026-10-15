---
id: diagnosticar-el-juego
title: Diagnosticar el juego
nav_title: Diagnosticar
summary: "Cuatro preguntas sobre un juego deciden qué modelo le toca: árbol con turnos, árbol con azar o tabla de pagos. Y qué es una respuesta: valor, jugada o estrategia."
status: ready
estimated_time: 20m
tags: [juegos, modelado, diagnostico]
---

# Diagnosticar el juego

**¿Qué tipo de juego es, y qué modelo le toca?**

Al terminar tendrás un **mapa**: para cada tipo de juego, qué modelo se
escribe y en qué clase se resuelve. También sabrás qué tipo de respuesta
buscamos.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

## 1 · Cuatro preguntas sobre el juego

[[diagnosticar-el-entorno|La unidad de agentes]] diagnosticaba un entorno con
siete perillas. Para un juego, cuatro preguntas deciden el modelo; tres
vienen de esas perillas y una es nueva:

::: table {#jue-c1-perillas title="Las cuatro preguntas, y hexapawn"}
| Pregunta | Perilla de la unidad de agentes | Hexapawn |
|---|---|---|
| ¿Se juega por turnos o los dos eligen a la vez? | Ninguna: es nueva, propia de los juegos | Por turnos: cada uno ve la jugada anterior |
| ¿Decide el azar alguna parte? | Determinismo | No: no hay dados ni cartas |
| ¿Cada jugador ve todo lo que importa? | Observabilidad | Sí: es de **información perfecta**, el tablero y las jugadas están a la vista |
| ¿Lo que gana uno lo pierde el otro? | Número de agentes: competitivo | Sí: es de **suma cero** |
:::

Hay una quinta pregunta que no es del juego sino del cómputo: **¿cabe el
árbol?** Hexapawn sí: 252 nodos. El ajedrez, no.

## 2 · Cada diagnóstico pide un modelo

**Piensa: si los dos eligen a la vez, ¿sigue sirviendo un árbol donde uno
mueve y el otro responde?**

Las respuestas a las cuatro preguntas deciden cómo se escribe el juego:

::: table {#jue-c1-mapa title="Del diagnóstico al modelo"}
| Juego | Lo que lo distingue | Modelo | Dónde se resuelve |
|---|---|---|---|
| Hexapawn | Turnos, sin azar, todo visible, suma cero | Árbol con nodos MAX y MIN | Clase 2 |
| Un juego con dado | Además, un dado decide una parte | Árbol con nodos de azar | Clase 2 |
| Ajedrez | Igual que hexapawn, pero el árbol no cabe | Árbol cortado y una estimación | Clase 3 |
| Pares o nones | Los dos eligen a la vez | Tabla de pagos | Clase 4 |
| Dilema del prisionero | A la vez y **no** es suma cero | Tabla con un pago por jugador | Clase 4 |
| Póker | Las cartas del rival están ocultas | Otro modelo | Fuera de esta unidad |
:::

Dos modelos de la tabla son nuevos, y aquí basta una línea de cada uno:

- un **nodo de azar** es un nodo donde no elige ningún jugador, sino un dado:
  cada flecha lleva la probabilidad de que salga;
- una **tabla de pagos** tiene una fila por jugada de un jugador, una columna
  por jugada del otro y, en cada celda, lo que gana cada uno.

Cuando los dos eligen a la vez, ninguno ve la jugada del otro antes de
decidir. Un árbol donde Blancas mueve y luego Negras responde **viéndola**
describiría otro juego. Por eso la clase 4 cambia de modelo.

## 3 · Valor, jugada y estrategia

**Piensa: cuando le pides a un programa «la respuesta», ¿qué esperas que te
dé?**

Hay tres cosas distintas, y conviene no confundirlas:

::: definition {#jue-c1-valor-jugada-estrategia title="Valor, jugada y estrategia"}
- El **valor** $V(s)$ es la utilidad que MAX puede garantizar desde $s$
  suponiendo que MIN siempre responde con lo peor para MAX. Es un número, en
  puntos de MAX; en un final, $V(s)=U(s)$.
- Una **jugada** es una acción $a\in A(s)$: lo que haces ahora.
- Una **estrategia** de MAX es una función que a cada estado $s$ con
  $\mathrm{Pl}(s)=\text{MAX}$ le asigna una jugada de $A(s)$: dice qué hacer
  en **cada** estado donde le toca, no solo en el actual. Lo mismo para MIN.
:::

El valor no es una jugada: dice cuánto vale la posición, no qué hacer. Ya lo
viste en la unidad de optimización. Si $f$ asigna un número a cada jugada
$a\in A(s)$:

- $\max_{a\in A(s)} f(a)$ es **el número** más alto que se alcanza;
- $\operatorname*{arg\,max}_{a\in A(s)} f(a)$ es **el conjunto de jugadas**
  que lo alcanzan. Es un conjunto porque puede haber empates.

Una estrategia es mucho más grande que una jugada. En hexapawn hay **37
estados** donde le toca a Negras y la partida no ha terminado; una estrategia
de Negras elige una jugada en cada uno. Martin Gardner construyó una máquina
que jugaba con Negras usando **24 cajas de cerillos**, una por posición: le
alcanzaron menos de 37 porque muchas posiciones son el reflejo de otra y
basta guardar una. La máquina aprendía qué jugada evitar en cada caja.

**Por qué importa la estrategia:** el rival puede llevarte a estados que no
esperabas. Un plan que solo dice cómo empezar se queda sin respuesta en
cuanto el rival se desvía.

::: exercise {#jue-c1-ej-que-dice-v title="Decide qué dice el valor"}
En la clase 2 calcularemos que $V(s_0)=-1$ en hexapawn. ¿Qué dice ese número
y qué **no** dice?
:::

::: answer {#jue-c1-resp-que-dice-v of="jue-c1-ej-que-dice-v"}
**Dice** que, si las dos juegan lo mejor posible, Blancas pierde: Negras
puede asegurar la victoria, haga lo que haga Blancas.

**No dice** qué jugada hacer en ningún estado. Para eso hace falta comparar
los valores de los hijos y quedarse con una jugada del
$\operatorname{arg\,max}$, o tener una estrategia completa.
Tampoco dice qué pasa si alguno de los dos se equivoca.
:::

## 4 · Tu turno

::: exercise {#jue-c1-ej-diagnostico title="Diagnostica tres juegos"}
Para cada juego, contesta las cuatro preguntas de la sección 1 y di qué
modelo le toca, o por qué no es un juego para esta unidad.

1. **Serpientes y escaleras.** Cada jugador tira un dado y avanza esa
   cantidad de casillas; las escaleras suben y las serpientes bajan.
2. **Batalla naval.** Cada jugador esconde sus barcos en una cuadrícula y,
   por turnos, dispara a una casilla del rival.
3. **Conecta 4.** Por turnos se dejan caer fichas en un tablero vertical de
   7 columnas; gana quien alinea cuatro.
:::

::: hint {#jue-c1-pista-diagnostico of="jue-c1-ej-diagnostico" title="Antes de las cuatro preguntas"}
Para cada juego, pregúntate primero si algún jugador **elige** algo. Si nadie
elige, no hay nada que calcular para un jugador. Después busca qué no ve cada
jugador.
:::

::: answer {#jue-c1-resp-diagnostico of="jue-c1-ej-diagnostico"}
1. **Serpientes y escaleras:** por turnos, con azar, todo visible y suma
   cero. Pero **nadie decide nada**: el dado fija cada movimiento. No hay
   jugada que elegir, así que no hay nada que calcular para un jugador.
2. **Batalla naval:** por turnos y sin azar una vez colocados los barcos,
   pero **no** ves los barcos del rival. Es información oculta, como en el
   póker: queda fuera de esta unidad.
3. **Conecta 4:** por turnos, sin azar, todo visible y suma cero. Le toca un
   **árbol con nodos MAX y MIN**, como a hexapawn. Pero su árbol es enorme:
   para jugarlo se usan las herramientas de la clase 3, como en el ajedrez.
   Con muchísimo cómputo sí se resolvió en 1988: gana quien empieza.
:::

**Punto de control:** deberías poder diagnosticar un juego nuevo con las
cuatro preguntas, decir qué modelo le toca y distinguir su valor de una
jugada y de una estrategia.

## 5 · Jugar bien: qué es ser racional

**Piensa: el problema de la unidad va a pedir que MIN «responda lo mejor
que puede». ¿Lo mejor según quién, y con qué?**

::: definition {#jue-c1-racional title="Jugador racional"}
Un jugador es **racional** si, cada vez que le toca, elige la jugada que
espera que le dé la mayor utilidad, **dado**:

1. **su función a optimizar**: su utilidad, la que está escrita;
2. **lo que sabe**: las reglas y lo que ha visto de la partida;
3. **lo que puede hacer**: sus jugadas, $A(s)$;
4. **lo que alcanza a calcular** con el tiempo y la memoria que tiene.

**Qué significa:** no existe «racional» a secas. Siempre es racional
**respecto a** esas cuatro cosas, y la primera es la que manda: la
racionalidad sale de la función a optimizar, no de ganar ni de parecer
listo.
:::

Es la definición del libro de texto de IA, el de Russell y Norvig: un agente
racional elige la acción que espera que maximice su **medida de desempeño**,
con lo que ha percibido y lo que sabe. Es la misma medida de desempeño de
[[desempeno-en-peas|la unidad de agentes]]. En un juego, esa medida es $U$.

### Racional para MAX y para MIN

- **MAX racional** elige para que $U$ quede lo más alto posible.
- **MIN racional** elige para que **su** utilidad, $-U$, quede lo más alta
  posible. Es decir, para que $U$ quede lo más bajo posible.

Por eso, y **solo** porque es suma cero, «lo mejor para MIN» es «lo peor
para MAX». En la clase 4 aparecen juegos que no son de suma cero, y esa
equivalencia deja de valer.

### No hay racionalidad perfecta

Elegir la jugada perfecta exige calcular todas las continuaciones. En
hexapawn se puede: son 252 nodos. En ajedrez nadie puede, ni la computadora
más grande.

**Eso no vuelve irracional a quien juega ajedrez.** Lo racional, entonces,
es **lo mejor que puedes dado tu objetivo y tus límites**: si tienes un
segundo, la mejor jugada que encuentras en un segundo. Stuart Russell, uno
de los autores de ese libro, lo llamó **racionalidad limitada**; en
economía, Herbert Simon le había llamado racionalidad acotada.

::: table {#jue-c1-racional-limites title="Lo racional depende de lo que tiene el jugador"}
| Lo que tiene el jugador | Lo racional |
|---|---|
| Tiempo para recorrer todo el árbol | La jugada que asegura lo más posible contra cualquier respuesta |
| Un segundo por jugada | La mejor jugada que encuentra en ese segundo |
| Una tabla de 24 cajas | Lo que dice la caja de esa posición |
:::

La jugada perfecta es un ideal que sirve de **regla para medir**, no una
exigencia. Lo que sí se exige es no desperdiciar: si tenías tiempo de ver
que una jugada pierde y la hiciste, eso sí es irracional.

### Lo que racional no quiere decir

::: table {#jue-c1-racional-no title="Cuatro confusiones con «racional»"}
| No es | Por qué no |
|---|---|
| Ganar siempre | En hexapawn, Blancas jugando perfecto pierde; lo calcularemos en la clase 2 |
| Ser inteligente o humano | La máquina de cerillos de Gardner son cajas, y puede ser racional |
| Saberlo todo o calcularlo todo | Elige con lo que sabe y con lo que alcanza a calcular |
| Querer lo que queremos nosotros | Persigue **su** $U$; si $U$ premia otra cosa, persigue esa otra cosa |
:::

La última fila es la importante: **un jugador racional con una utilidad
mal escrita hace mal las cosas con toda eficiencia.** El error está en
$U$, no en el jugador. Por eso la sección 8 insiste en que la utilidad
copia el reglamento.

### Que el rival sea racional es un supuesto

Lo anotamos igual que los supuestos del reglamento. Vuelve en tres clases:

- **Clase 2:** si Negras mueve al azar, lo que Blancas calcula suponiéndola
  racional se sigue cumpliendo como piso, pero puede dejar puntos sobre la
  mesa.
- **Clase 3:** cuando el árbol no cabe, se corta y se estima. Es
  racionalidad limitada en la práctica.
- **Clase 4:** cuando eligen a la vez, cada uno es racional **dado lo que
  hará el otro**.

::: exercise {#jue-c1-ej-racional title="¿Racional o no?"}
Para cada caso, di si el jugador fue racional y, si algo salió mal, dónde
está el error: en el jugador o en la utilidad.

1. En n1, Blancas juega $\text{c1}\textbf{-}\text{c2}$ y gana en esa jugada.
2. Un programa recibe $+1$ por ganar, $-1$ por perder y además $+3$ por
   cada peón que captura. En n1 juega $\text{c1}\textbf{x}\text{b2}$ en vez
   de $\text{c1}\textbf{-}\text{c2}$, y pierde.
3. Blancas juega perfecto desde el inicio y pierde.
4. Un programa juega suponiendo que Negras es racional, pero Negras mueve
   al azar.
5. Con un segundo por jugada, un programa de ajedrez mira 4 jugadas hacia
   delante y elige una que, vista con 20, pierde.
:::

::: hint {#jue-c1-pista-racional of="jue-c1-ej-racional" title="Las cuatro cosas dadas"}
En cada caso pregúntate: ¿qué función optimizaba el jugador, qué sabía y
cuánto podía calcular? Si con eso eligió lo mejor, fue racional, aunque el
resultado haya sido malo.

Para el caso 2, cuenta los puntos de cada jugada con **la utilidad del
programa**, no con la del reglamento. Tras $\text{c1}\textbf{x}\text{b2}$,
Negras gana de inmediato con $\text{c3}\textbf{x}\text{b2}$.
:::

::: answer {#jue-c1-resp-racional of="jue-c1-ej-racional"}
1. **Racional.** Gana en una jugada, y ganar es lo más alto que da $U$.
2. **Racional, con una utilidad mal escrita.** Para el programa,
   $\text{c1}\textbf{-}\text{c2}$ vale $+1$: gana sin capturar. Y
   $\text{c1}\textbf{x}\text{b2}$ vale $-1+3=+2$: pierde, pero capturó un
   peón. Con su utilidad, capturar es mejor. **El error está en $U$:** el
   reglamento no paga por capturar, y el programa hizo con toda eficiencia
   lo que su número le pedía.
3. **Racional.** En hexapawn, Negras puede asegurar la victoria haga lo que
   haga Blancas. Perder no prueba que se jugó mal; ser racional no es
   ganar.
4. **El programa es racional dado lo que supone**, pero el supuesto es
   falso. Lo que calculó lo sigue protegiendo: nunca le irá peor que eso.
   Lo que pierde es la oportunidad de aprovechar los errores de Negras. En
   la clase 2 se calcula cuánto.
5. **Racional.** Eligió lo mejor que encontraba en un segundo, y no tenía
   cómo ver 20 jugadas. Sería irracional solo si tuviera tiempo de mirar
   más y no lo usara.
:::

## 6 · La pregunta que falta: qué jugada elegir

**Piensa: en $s_0$, ¿pudo Blancas evitar perder?**

Una sola partida no lo dice. Para saberlo hay que considerar **todas** las
respuestas de Negras, no solo las que hizo esta vez. Eso es el problema de
la unidad, y se escribe como en la unidad de optimización: qué te dan y qué
tienes que encontrar.

::: definition {#jue-c1-problema title="El problema: elegir la jugada"}
**Dado:** el juego $(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\ T,\ U)$.

**Encontrar:** en cada estado donde le toca a MAX, la jugada de $A(s)$ que
le asegura la mayor utilidad posible, suponiendo que MIN es **racional**
(@jue-c1-racional): responde siempre lo mejor que puede para su utilidad,
$-U$, es decir, lo peor para MAX.
:::

**Por qué en cada estado, y no solo en $s_0$.** El rival puede llevarte a
cualquier estado. Una respuesta que solo dice cómo empezar se queda sin
jugada en cuanto el rival hace algo inesperado.

Dos nombres para esta respuesta llegan en las páginas siguientes:

- el número que MAX puede asegurar desde $s$ será el **valor** $V(s)$, en
  [[el-juego-como-grafo|El juego como grafo]];
- una regla que dice qué jugada hacer en cada estado será una
  **estrategia**, en [[diagnosticar-el-juego|Diagnosticar el juego]].

**Las clases 2 a 4 son maneras distintas de contestar esta pregunta.** La
clase 2 la contesta cuando el juego cabe completo; la clase 3, cuando no
cabe; la clase 4, cuando los dos eligen a la vez y el modelo tiene que
cambiar.

**Punto de control:** para cualquier tablero de hexapawn deberías poder
escribir su estado, decir si es final, quién mueve, cuáles son sus jugadas,
a dónde lleva cada una y, si es final, cuánto vale. Deberías poder escribir
una partida completa con esas piezas, decir qué cambiaría en cada pieza si
el juego fuera ajedrez, decir respecto a qué es racional un jugador y decir
qué pide el problema de la unidad.

## Lo que hay que llevarse

- Cuatro preguntas deciden el modelo: turnos o a la vez, azar, información
  completa y suma cero. Una quinta decide el método: si el árbol cabe.
- Turnos sin azar llevan a un árbol MAX/MIN; con azar, a un árbol con nodos
  de azar; jugadas a la vez, a una tabla de pagos.
- El valor es un número, la jugada es lo que haces ahora y la estrategia es
  un plan para cada estado donde te toca.

Continúa con la [[tarea-leer-y-escribir|tarea de refuerzo]].
