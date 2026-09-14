---
id: el-rendimiento-que-decrece
title: El rendimiento que decrece
nav_title: El reactor
summary: "Segundo episodio: repartir la potencia del reactor entre tres sistemas que rinden cada vez menos. Qué se rompe cuando el objetivo deja de ser una recta, y qué se salva."
status: ready
estimated_time: 22m
tags: [optimizacion, convexidad, concavidad]
---

# El rendimiento que decrece

**¿Qué se rompe si el objetivo deja de ser una recta?**

La impresora quedó resuelta. Empieza el segundo episodio, y esta vez lo que
falla no es el dibujo: es la línea recta.

> **Bitácora del reactor.** El turno de noche lo dejo apuntado porque mañana hay
> que decidirlo. El reactor reparte entre tres sistemas: escudos, motores y
> soporte vital. Lo que le presta a la bodega para la impresora ya está aparte y
> no se toca.
>
> El problema es que ninguno rinde parejo. La primera unidad de potencia que le
> das a los escudos vale muchísimo; la décima, casi nada. Con los motores pasa
> igual pero tardan más en saturarse, y el soporte vital es el que más aguanta:
> sigue pagando cuando los otros dos ya no.
>
> La ingeniera lo tiene medido: por cada unidad que le pones a un sistema, lo que
> ganas baja en uno respecto de la unidad anterior. Empieza en 6 para escudos, en
> 8 para motores y en 10 para soporte vital.
>
> Repártela toda entre los tres. Y ojo, que el soporte vital no aguanta mucho más
> de cinco.
>
> Los turnos siguen como estaban: Vega entra a las cuatro.

## 1 · La bitácora, otra vez con sus tres trampas

Lo mismo que en el primer episodio, y conviene notarlo: la forma de las trampas
no cambia porque cambie la matemática.

::: table {#opt-trampas-reactor title="Las tres trampas de la bitácora del reactor"}
| Trampa | Dónde está | Qué se hace |
|---|---|---|
| Sobra | «Vega entra a las cuatro» | Fuera: no entra en ninguna restricción |
| Falta | Cuánta potencia da el reactor en total | Suponer **y anotarlo**: 15 unidades por turno |
| Ambiguo | «Repártela toda» · «no aguanta mucho más de cinco» | Decidir: la primera es igualdad; la segunda se deja para después |
:::

**La primera ambigüedad es la que cambia el modelo.** «Repártela toda» se puede
leer como que la potencia sobrante se pierde —y entonces es una **igualdad**— o
como que se puede guardar —y entonces sería $\le$—. Un reactor que no acumula no
deja guardar nada, así que se escribe con igualdad, y de ahí sale todo lo demás
de esta clase.

La segunda —el tope del soporte vital— se anota y se deja pendiente:
[[los-signos-del-lagrangeano|entra en la página 4]], que es donde hay con qué
tratarla.

## 2 · El modelo

$p_i$ es la potencia que recibe el sistema $i$, en unidades. Lo que rinde cada
sistema es

$$u_i(p_i) = b_i\,p_i - \tfrac{1}{2}p_i^2, \qquad b = (6,\,8,\,10),$$

que es exactamente «cada unidad rinde uno menos que la anterior»: la ganancia de
pasar de $p$ a $p+1$ es $b_i - p - \tfrac12$.

$$\begin{aligned}
\max\; &\sum_{i=1}^{3}\left(b_i p_i - \tfrac12 p_i^2\right) \\
\text{s.a.}\;\; &p_1+p_2+p_3 = 15,\qquad p \ge 0.
\end{aligned}$$

> [!NOTE]
> **Qué sigue igual y qué no.** Las variables siguen siendo continuas y la
> restricción sigue siendo una recta —un plano, con tres variables—. Lo único
> que cambió es el **objetivo**, que dejó de ser $c\cdot x$. Y con eso se cae el
> teorema del vértice: [[cuando-se-acaba-el-dibujo|su demostración]] usaba que
> el valor de una mezcla es la mezcla de los valores, y eso solo vale para una
> función lineal.

## 3 · Cóncava: la prueba de la cuerda

::: definition {#opt-conjunto-convexo title="Conjunto convexo"}
Un conjunto es **convexo** si, tomando dos puntos cualesquiera de él, todo el
segmento que los une también está en el conjunto. Sin huecos, sin entrantes y
sin puntos sueltos.

Todo poliedro lo es —por eso el término venía usándose desde la clase 1—, y el
conjunto de repartos que suman exactamente 15 también.
:::

::: definition {#opt-funcion-concava title="Función cóncava, y la prueba de la cuerda"}
Una función es **cóncava** si entre dos puntos cualesquiera la **curva nunca
queda por debajo de la cuerda** que los une:

$$f\bigl(t\,a + (1-t)\,c\bigr)\;\ge\; t\,f(a) + (1-t)\,f(c) \qquad
\text{para todo } t\in[0,1].$$

Es **convexa** si pasa lo contrario: la curva nunca queda por encima de la
cuerda. Una función lineal cumple las dos con igualdad, y por eso todo lo de las
clases 1 y 2 era los dos casos a la vez.
:::

::: figure {#opt-cuerda title="La cuerda del rendimiento, entre p = 2 y p = 7"}
![La curva de rendimiento de un sistema con una cuerda trazada entre dos de sus puntos; la cuerda queda por debajo de la curva en todo el tramo](../_assets/opt-cuerda.svg)
:::

En el reactor eso se lee directo: repartir cinco unidades entre dos momentos
distintos rinde menos que ponerlas juntas en el punto medio. **Rendimiento
decreciente y concavidad son la misma frase**, dicha en dos idiomas.

## 4 · Y por qué cóncava y convexa son el mismo problema

::: remark {#opt-concava-y-convexa title="Maximizar una cóncava es minimizar una convexa"}
$f$ es cóncava exactamente cuando $-f$ es convexa, y las dos tienen sus óptimos
en el mismo punto. Así que **maximizar una función cóncava y minimizar una
convexa son el mismo problema**, y todo teorema sobre uno vale para el otro sin
demostrarlo dos veces.

Esta unidad maximiza, porque los tres episodios maximizan. Los libros suelen
minimizar. No hay nada que traducir más que el signo.
:::

::: figure {#opt-concava-convexa title="La misma curva, y su reflejo"}
![Dos paneles con la misma curva reflejada: a la izquierda una función cóncava con su máximo señalado, a la derecha su negativo, una función convexa con su mínimo en la misma potencia](../_assets/opt-concava-convexa.svg)
:::

## 5 · Lo que se salva: local sigue siendo global

::: definition {#opt-problema-convexo title="Problema convexo"}
Un problema es **convexo** cuando se cumplen **las dos** cosas:

1. el conjunto factible es convexo, **y**
2. se minimiza una función convexa, o se maximiza una cóncava.

Definirlo solo por la función deja fuera la mitad, y la mitad que falta es la que
hace falta en el teorema de abajo.
:::

::: theorem {#opt-teo-local-global title="En un problema convexo, todo óptimo local es global"}
Sea el conjunto factible **convexo**. Si $f$ es cóncava y se maximiza —o convexa
y se minimiza—, entonces todo óptimo local es óptimo global.
:::

::: proof {#opt-dem-local-global of="opt-teo-local-global"}
Para el caso de máximo; el de mínimo es el mismo con $-f$.

Sea $x^\ast$ un óptimo local y supón que existe un punto factible $y$ con
$f(y) > f(x^\ast)$. Para cada $t\in(0,1]$ mira el punto

$$z_t = (1-t)\,x^\ast + t\,y.$$

**Es factible**, porque el conjunto es convexo y $z_t$ está en el segmento entre
dos puntos factibles. Y por concavidad,

$$f(z_t)\;\ge\;(1-t)f(x^\ast) + t\,f(y)\;>\;f(x^\ast)\quad\text{para todo } t>0,$$

donde la desigualdad estricta es porque $f(y)$ es estrictamente mayor. Ahora haz
$t$ tan chico como quieras: $z_t$ se acerca a $x^\ast$ tanto como se quiera y
**siempre vale más**. Eso contradice que $x^\ast$ gane en su vecindario.

Las dos hipótesis se gastaron en un renglón cada una: la convexidad del conjunto
para que $z_t$ sea factible, la concavidad para la desigualdad.
:::

Esto es lo que [[de-esquina-en-esquina|simplex]] usaba sin demostrar. Una
función lineal es cóncava, un poliedro es convexo, y por eso parar cuando ningún
vecino mejora era correcto. **El teorema no es de programación lineal: es de
convexidad, y la lineal era un caso.**

> [!WARNING]
> **Hacen falta las dos hipótesis, y cada una falla sola.** Maximiza $x^2$ sobre
> $[-2,1]$: el conjunto es convexo, pero la función es convexa y se está
> maximizando, y $x=1$ es un máximo local que no es global. Ahora minimiza
> $(x-2)^2$ sobre $\{0\}\cup[1,3]$: la función es convexa y se minimiza, pero el
> conjunto **no** es convexo, y $x=0$ es un mínimo local aislado que vale 4
> cuando el global vale 0.

## Lo que hay que llevarse

- El rendimiento decreciente rompe la linealidad, y con ella el vértice: el
  mejor reparto ya no está en una esquina.
- Lo que sobrevive es la convexidad, y con ella la garantía que de verdad
  importaba: **mirar alrededor basta**.
- Cóncava y convexa no son dos teorías: son la misma cambiada de signo.

Falta encontrar ese punto:
[[sustituir-y-derivar|la página siguiente]].
