---
id: jugar-a-la-vez
title: Jugar a la vez
nav_title: Jugar a la vez
summary: "Si el rival no ve tu jugada, el árbol ya no sirve: el juego se escribe como una tabla de pagos, una jugada fija puede castigarse y conviene mezclar."
status: ready
estimated_time: 25m
tags: [juegos, modelado, estrategias-mixtas]
---

# Jugar a la vez

**¿Qué cambia si el rival no ve tu jugada antes de elegir la suya?**

Al terminar tendrás **una tabla de pagos** para dos juegos simultáneos, sabrás
calcular qué asegura cada jugada fija y qué asegura una **mezcla** de jugadas.

## 1 · Recordar la tabla donde el rival miraba

**Piensa: en el ejemplo del juego de la unidad de optimización, ¿por qué
bastaba con mirar el peor valor de cada fila?**

En [[opt-objetivo-juego-practica|el ejemplo del juego]] elegías Guardar o
Sacrificar, y el rival respondía I o D **después de ver tu fila**:

| Acción | I | D |
|---|---:|---:|
| Guardar | +1 | −1 |
| Sacrificar | +1 | +1 |

Como el rival veía tu fila, podía escoger en ella la peor columna para ti.
Por eso el valor de una fila era su mínimo, y elegías la fila con el mejor
mínimo: Sacrificar, que asegura +1.

Ahora cambia una sola cosa: **el rival elige sin ver tu jugada**. Los dos
deciden al mismo tiempo, o cada uno en secreto.

## 2 · Escribir una tabla de pagos

**Piensa: si nadie mueve primero, ¿qué queda del árbol?**

Juegas **pares o nones** y tú vas con pares. A la cuenta de tres, cada uno
muestra **1 o 2 dedos**. Si la suma es par, ganas 1 punto; si es impar,
pierdes 1 punto. Lo que tú ganas lo pierde el otro: es un juego de **suma
cero**.

No hay árbol que recorrer, porque ninguna jugada ocurre antes que la otra.
Lo que hay es una tabla con **una fila por cada acción tuya** y **una columna
por cada acción del rival**:

::: table {#jue-c4-pares title="Pares o nones, en tus puntos"}
| Tú ↓ · Rival → | 1 dedo | 2 dedos |
|---|:---:|:---:|
| **1 dedo** | +1 | −1 |
| **2 dedos** | −1 | +1 |
:::

Con 1 y 1 la suma es 2, par: ganas. Con 1 y 2 la suma es 3, impar: pierdes.

::: definition {#jue-c4-tabla-pagos title="Tabla de pagos"}
En un juego simultáneo de dos jugadores y suma cero, tus acciones son las
filas $i=1,\dots,I$ y las del rival, las columnas $j=1,\dots,J$. $U(i,j)$ es
**tu** pago cuando tú juegas $i$ y el rival juega $j$. El rival recibe
$-U(i,j)$.

La tabla completa es un **dato**: la fijan las reglas. Lo que decide cada
jugador es solo qué fila o qué columna juega.
:::

Seguimos midiendo todo en puntos tuyos, igual que $U(s)$ se medía en puntos
de MAX en hexapawn. Tú eres MAX: quieres que $U$ sea alto. El rival es MIN.

## 3 · Buscar una jugada segura

**Piensa: si tuvieras que anunciar tu jugada en voz alta, ¿cuál elegirías?**

Antes de poner nombres, un aviso, porque los nombres se parecen y significan
cosas distintas:

> **Ojo con los nombres.** El algoritmo [[minimax|minimax]] de la clase 2 calculaba un *máximo de mínimos*, porque MIN respondía viendo tu jugada. En una tabla, ese número se llama **maximin**. El **minimax puro** es lo contrario: el rival elige primero su columna y tú respondes viéndola.

Una jugada fija es una fila que juegas siempre. Lo que **asegura** es el peor
pago de esa fila, porque el rival podría elegir justo esa columna:

| Tu jugada fija | Peor caso |
|---|---:|
| Siempre 1 dedo | −1 |
| Siempre 2 dedos | −1 |

El mejor de esos peores casos es −1: es el **maximin puro**. Con una jugada
fija solo puedes asegurar perder.

Ahora mira la tabla desde el rival. Si él juega siempre la misma columna, lo
peor que le puede pasar es el **mayor** pago de esa columna para ti: +1 en
las dos. El menor de esos máximos, +1, es el **minimax puro**. Con una
columna fija, el rival solo puede asegurar que no ganes **más** de +1.

::: definition {#jue-c4-punto-silla title="Maximin puro, minimax puro y punto de silla"}
- El **maximin puro** es $\max_i \min_j U(i,j)$: lo que aseguras jugando
  siempre la misma fila, si el rival ve tu fila antes de elegir.
- El **minimax puro** es $\min_j \max_i U(i,j)$: el tope que el rival te
  impone jugando siempre la misma columna, si tú ves su columna antes de
  elegir.

El maximin puro nunca pasa del minimax puro, porque mover segundo nunca
perjudica: si ves la columna del rival antes de elegir, no puedes asegurar
menos que si él ve tu fila. Cuando los dos números **coinciden**, la tabla
tiene un **punto de silla**: una fila y una columna que ninguno quiere
cambiar aunque el otro anuncie la suya.
:::

En el ejemplo de Guardar y Sacrificar había punto de silla: Sacrificar asegura
+1, y +1 es lo más que se puede ganar. En pares o nones, el maximin puro es
−1 y el minimax puro es +1. **No hay punto de silla.**

En palabras: **si eres predecible, pierdes**. Si el rival sabe que siempre
muestras 1 dedo, muestra 2. Y lo mismo le pasa a él.

::: exercise {#jue-c4-ej-silla title="Decide si hay punto de silla"}
En esta tabla, tus filas son A y B, y las columnas del rival, X e Y:

| Tú ↓ · Rival → | X | Y |
|---|:---:|:---:|
| **A** | 3 | 5 |
| **B** | 1 | 4 |

Calcula el maximin puro y el minimax puro. ¿Hay punto de silla?
:::

::: answer {#jue-c4-resp-silla of="jue-c4-ej-silla"}
Los peores casos de las filas son 3 y 1: el maximin puro es **3**, jugando A.
Los mayores de las columnas son 3 y 5: el minimax puro es **3**, jugando X.
Coinciden, así que (A, X) es un **punto de silla**: aunque anuncies A, el
rival no puede bajarte de 3, y aunque anuncie X, tú no puedes pasar de 3.
:::

## 4 · Mezclar las jugadas

**Piensa: ¿qué pasa si ni tú sabes qué vas a mostrar hasta el último
momento?**

Supón que lanzas una moneda en secreto: águila, 1 dedo; sol, 2 dedos. El
rival puede saber que usas una moneda; lo que no puede saber es **cómo
cayó**. Tu pago ya no es un número fijo sino un **valor esperado**, como en
los nodos de azar de la clase 2.

Contra cada columna del rival, tu pago esperado es:

| Rival juega | Pago esperado |
|---|---|
| 1 dedo | $\tfrac12(+1)+\tfrac12(-1)=0$ |
| 2 dedos | $\tfrac12(-1)+\tfrac12(+1)=0$ |

Haga lo que haga el rival, tu pago esperado es 0. Con una jugada fija
asegurabas −1; con la moneda aseguras 0.

::: definition {#jue-c4-mixta title="Estrategia mixta y su garantía"}
Una **estrategia mixta** es un vector $p=(p_1,\ldots,p_I)$, donde $p_i$ es la
probabilidad de jugar la fila $i$. Cumple $p_i\ge0$ y $\sum_i p_i=1$. Una
jugada fija es el caso en que un $p_i$ vale 1 y los demás, 0: se llama
**estrategia pura**.

Contra la columna $j$, el pago esperado de $p$ es $\sum_i p_i\,U(i,j)$. La
**garantía** de $p$ es el peor de esos pagos esperados:

$$g(p)=\min_j \sum_i p_i\,U(i,j).$$
:::

Una estrategia mixta es **una sola decisión**: elegir el vector $p$ antes de
jugar. El sorteo viene después y no lo controla nadie.

En la página siguiente verás por qué basta revisar las columnas puras del
rival, aunque él también pueda mezclar.

::: exercise {#jue-c4-ej-tres-cuartos title="Decide qué garantiza una moneda cargada"}
En pares o nones, usas una moneda cargada: muestras 1 dedo con probabilidad
$3/4$ y 2 dedos con probabilidad $1/4$, es decir, $p=(3/4,1/4)$.

1. Calcula tu pago esperado contra cada columna del rival.
2. ¿Cuál es la garantía $g(p)$? ¿Es mejor o peor que la moneda justa?
:::

::: answer {#jue-c4-resp-tres-cuartos of="jue-c4-ej-tres-cuartos"}
1. Contra 1 dedo: $\tfrac34(+1)+\tfrac14(-1)=\tfrac12$. Contra 2 dedos:
   $\tfrac34(-1)+\tfrac14(+1)=-\tfrac12$.
2. $g(p)=\min\{\tfrac12,-\tfrac12\}=-\tfrac12$. Es **peor** que la moneda
   justa, que asegura 0. Una moneda cargada vuelve a hacerte algo
   predecible: el rival que la conoce muestra 2 dedos.
:::

Mezclar no basta: **hay que mezclar en la proporción correcta**. Encontrar
esa proporción es el tema de la página siguiente.

## 5 · Probar con tres acciones

**Piensa: en piedra, papel o tijera, ¿hay alguna jugada que nunca pierda?**

Ahora cada uno tiene tres acciones. Piedra gana a tijera, tijera gana a papel
y papel gana a piedra. Ganar vale +1, perder −1 y empatar 0:

::: table {#jue-c4-ppt title="Piedra, papel o tijera, en tus puntos"}
| Tú ↓ · Rival → | Piedra | Papel | Tijera |
|---|:---:|:---:|:---:|
| **Piedra** | 0 | −1 | +1 |
| **Papel** | +1 | 0 | −1 |
| **Tijera** | −1 | +1 | 0 |
:::

Cada fila tiene un −1: en este juego, toda jugada fija pierde contra alguna
respuesta. El maximin puro es −1 y, por el mismo argumento con las columnas,
el minimax puro es +1. Tampoco hay punto de silla.

Con $p=(1/3,1/3,1/3)$, contra cualquier columna sumas un tercio de +1, un
tercio de −1 y un tercio de 0. El pago esperado es 0 contra las tres: **la
mezcla uniforme asegura 0**.

::: exercise {#jue-c4-ej-sin-tijera title="Decide qué pasa si nunca sacas tijera"}
Juegas piedra o papel con probabilidad $1/2$ cada uno, y nunca tijera:
$p=(1/2,1/2,0)$. Calcula el pago esperado contra cada columna y la
garantía $g(p)$. ¿Qué columna elegiría un rival que conoce tu mezcla?
:::

::: answer {#jue-c4-resp-sin-tijera of="jue-c4-ej-sin-tijera"}
Contra piedra: $\tfrac12(0)+\tfrac12(+1)=\tfrac12$. Contra papel:
$\tfrac12(-1)+\tfrac12(0)=-\tfrac12$. Contra tijera:
$\tfrac12(+1)+\tfrac12(-1)=0$.

La garantía es $g(p)=-\tfrac12$. El rival elegiría **papel**, que empata con
tu papel y le gana a tu piedra. Dejar fuera una acción le regala al rival una
respuesta que no tiene castigo.
:::

**Punto de control:** deberías poder escribir la tabla de un juego simultáneo
pequeño, decir si tiene punto de silla y calcular la garantía de cualquier
mezcla $p$. Si alguna de las tres te falta, vuelve a las secciones 2, 3 o 4.

## Lo que hay que llevarse

- Si los dos eligen a la vez, el juego se escribe como una **tabla de pagos**
  $U(i,j)$, no como un árbol.
- Sin punto de silla, al menos uno de los dos jugadores puede ser castigado
  en cualquier jugada fija; en pares o nones y en piedra, papel o tijera, los
  dos.
- Una estrategia mixta $p$ asegura $g(p)$, el peor pago esperado contra las
  columnas del rival; no cualquier mezcla sirve.

Continúa con [[maximin-como-programa-lineal|maximin como programa lineal]].
