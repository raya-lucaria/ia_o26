---
id: cuando-no-es-suma-cero
title: Cuando no es suma cero
nav_title: No suma cero
summary: "Si cada jugador tiene su propio pago, suponer que el otro quiere dañarte es un error de modelado. Se buscan mejores respuestas y equilibrios de Nash, con el dilema del prisionero como ejemplo."
status: ready
estimated_time: 20m
tags: [juegos, modelado, equilibrio-de-nash]
---

# Cuando no es suma cero

**¿Y si lo que gana uno no es lo que pierde el otro?**

Al terminar tendrás **una tabla con dos pagos por casilla**, sabrás encontrar
las mejores respuestas y los equilibrios de Nash puros, y podrás explicar por
qué el maximin deja de ser la herramienta adecuada.

## 1 · Escribir una tabla con dos pagos

**Piensa: si la policía ofrece un trato a dos detenidos por separado, ¿lo que
gana uno es exactamente lo que pierde el otro?**

Dos personas detenidas por el mismo delito están en cuartos separados. A cada
una, por separado, le ofrecen lo mismo: **Callar** o **Delatar** al otro.
Deciden sin saber qué hace el otro, así que es un juego simultáneo. Las
condenas son:

- Si los dos callan, cada uno pasa 1 año en la cárcel.
- Si uno delata y el otro calla, el que delata sale libre y el que calla pasa
  10 años.
- Si los dos delatan, cada uno pasa 5 años.

Cada jugador quiere pasar **menos** años en la cárcel. Para que más sea
mejor, como en todo el curso, escribimos los años con signo negativo.

::: definition {#jue-c4-dos-pagos title="Utilidad de cada jugador"}
En un juego que no es de suma cero, cada jugador tiene su propia utilidad.
$U_1(i,j)$ es el pago del jugador 1 (las filas) y $U_2(i,j)$, el del jugador 2
(las columnas), cuando el 1 juega $i$ y el 2 juega $j$. Cada casilla de la
tabla lleva el par $(U_1,U_2)$.
:::

::: table {#jue-c4-prisionero title="Dilema del prisionero: (pago del 1, pago del 2), en años con signo negativo"}
| Jugador 1 ↓ · Jugador 2 → | Callar | Delatar |
|---|:---:|:---:|
| **Callar** | (−1, −1) | (−10, 0) |
| **Delatar** | (0, −10) | (−5, −5) |
:::

Los pagos de una casilla **no suman cero**, ni siempre lo mismo: suman −2 si
los dos callan y −10 si los dos delatan. Hay casillas que son mejores para
los dos a la vez. Eso no pasaba en pares o nones ni en los penales.

## 2 · Buscar la mejor respuesta

**Piensa: si supieras que el otro va a callar, ¿qué harías tú?**

Una pregunta más sencilla que «¿qué hago?» es: «si el otro hiciera esto, ¿qué
me conviene?».

::: definition {#jue-c4-mejor-respuesta title="Mejor respuesta"}
Una **mejor respuesta** del jugador 1 a la acción $j$ del jugador 2 es una
fila $i$ que maximiza $U_1(i,j)$ con $j$ fija. Para el jugador 2 es igual,
con las columnas y $U_2$.
:::

Para el jugador 1, comparando dentro de cada columna:

| Si el jugador 2… | Callar le da al 1 | Delatar le da al 1 | Mejor respuesta del 1 |
|---|---:|---:|---|
| Calla | −1 | 0 | Delatar |
| Delata | −10 | −5 | Delatar |

**Haga lo que haga el otro, delatar te da más**: $0>-1$ y $-5>-10$. El juego
es simétrico, así que al jugador 2 le pasa exactamente lo mismo.

## 3 · Encontrar el equilibrio

**Piensa: ¿hay alguna casilla de la que ninguno de los dos quiera moverse?**

::: definition {#jue-c4-nash title="Equilibrio de Nash"}
Un par de jugadas $(i,j)$ es un **equilibrio de Nash** si ninguno de los dos
gana cambiando **solo** su jugada: $i$ es mejor respuesta a $j$, y $j$ es
mejor respuesta a $i$. Lleva el nombre de John Nash.
:::

Se comprueba casilla por casilla. En (Delatar, Delatar), si el jugador 1 cambia
solo a Callar, pasa de −5 a −10: empeora. Al jugador 2 le pasa lo mismo.
Ninguno quiere cambiar: es un equilibrio.

Al revisar las cuatro casillas, **el único equilibrio es (Delatar,
Delatar)**, con pagos $(-5,-5)$. Y aquí está el dilema: (Callar, Callar) da
$(-1,-1)$, **mejor para los dos**. Cada uno, buscando lo mejor para sí, llega
a un resultado que los dos consideran peor.

::: exercise {#jue-c4-ej-callar title="Decide si callar los dos es equilibrio"}
1. Comprueba que (Callar, Callar) **no** es un equilibrio de Nash: ¿quién
   gana cambiando solo su jugada, y cuánto?
2. Comprueba que (Callar, Delatar) tampoco lo es.
:::

::: answer {#jue-c4-resp-callar of="jue-c4-ej-callar"}
1. En (Callar, Callar) el jugador 1 recibe −1. Si cambia solo a Delatar,
   llega a (Delatar, Callar) y recibe 0: gana 1 año. Basta con que uno quiera
   cambiar para que no sea equilibrio. (Al jugador 2 le pasa lo mismo.)
2. En (Callar, Delatar) el jugador 1 recibe −10. Si cambia solo a Delatar,
   llega a (Delatar, Delatar) y recibe −5: gana 5 años. No es equilibrio.
:::

Un equilibrio no es «lo mejor para todos»: es una situación **estable**,
donde nadie se arrepiente de su jugada viendo la del otro. Un equilibrio no
necesita un acuerdo para sostenerse: nadie gana rompiéndolo solo. En el
dilema se llega sin coordinarse porque delatar conviene haga lo que haga el
otro; con varios equilibrios, como en el juego de la gallina de la tarea,
llegar a uno sí puede requerir coordinación. La tabla no dice cómo se llega.

## 4 · Reconocer cuándo maximin es un error

**Piensa: en los penales suponíamos que el portero quería lo peor para ti.
¿Por qué ahí era razonable?**

En un juego de suma cero, **dañarte y ayudarse son la misma cosa**: cada
punto de gol que el portero te quita es un punto que él gana. Suponer que el
rival busca lo peor para ti es simplemente suponer que busca lo mejor para
sí. Por eso el maximin era la herramienta correcta.

Fuera de la suma cero, eso deja de ser cierto. El otro detenido no quiere que
pases 10 años en la cárcel; quiere pasar **él** pocos años. Modelarlo como
alguien que elige su columna para dañarte es atribuirle una utilidad que no
tiene. Es un **error de modelado**, no un error de cálculo: la cuenta puede
estar bien hecha sobre un modelo equivocado.

[[diagnosticar-el-entorno|La unidad de agentes]] ya tenía la perilla para
esto: multiagente **competitivo** o **cooperativo**, y advertía que casi
siempre es mixto. El dilema del prisionero es mixto: los dos prefieren
(Callar, Callar) a (Delatar, Delatar), que es la parte cooperativa, pero cada
uno gana delatando por su cuenta, que es la parte competitiva.

::: table {#jue-c4-herramientas title="Qué herramienta le toca a cada diagnóstico"}
| Diagnóstico | Qué supones del otro | Herramienta |
|---|---|---|
| Por turnos y suma cero | Elige lo peor para ti, porque es lo mejor para él | Árbol MAX/MIN: minimax y alfa-beta |
| A la vez y suma cero | Lo mismo, pero sin ver tu jugada | Estrategia mixta: programa lineal |
| A la vez y no suma cero | Busca su propio pago $U_2$ | Mejores respuestas y equilibrios de Nash |
:::

En esta clase solo buscamos equilibrios **puros** en tablas pequeñas,
revisando casilla por casilla. Calcular equilibrios en general, con mezclas y
muchas acciones, es un problema más difícil que no cubrimos.

**Punto de control:** deberías poder escribir una tabla con dos pagos,
marcar las mejores respuestas de cada jugador y decir qué casillas son
equilibrios de Nash puros. Si te falta alguno de los tres pasos, vuelve a las
secciones 1, 2 o 3.

## Lo que hay que llevarse

- Si los pagos no suman cero, cada jugador tiene su propia utilidad y la
  tabla lleva un par $(U_1,U_2)$ en cada casilla.
- Un equilibrio de Nash es un par de jugadas del que nadie quiere salir
  solo; en el dilema del prisionero es (Delatar, Delatar), aunque callar los
  dos sería mejor para ambos.
- Suponer que el otro quiere dañarte solo es correcto en suma cero; fuera de
  ella es un error de modelado.

Continúa con la [[tarea-sin-turnos|tarea de refuerzo]].
