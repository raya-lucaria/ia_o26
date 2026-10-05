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

## Lo que hay que llevarse

- Cuatro preguntas deciden el modelo: turnos o a la vez, azar, información
  completa y suma cero. Una quinta decide el método: si el árbol cabe.
- Turnos sin azar llevan a un árbol MAX/MIN; con azar, a un árbol con nodos
  de azar; jugadas a la vez, a una tabla de pagos.
- El valor es un número, la jugada es lo que haces ahora y la estrategia es
  un plan para cada estado donde te toca.

Continúa con la [[tarea-leer-y-escribir|tarea de refuerzo]].
