---
id: el-modelo-del-taller
title: El modelo, escrito
nav_title: El modelo
summary: "El modelo del taller en forma canónica y con su dominio declarado, dos variantes para ver qué mueve cada cambio, y por qué los métodos anteriores dejan de cerrar."
status: ready
estimated_time: 18m
tags: [optimizacion, modelado, entera]
---

# El modelo, escrito

**¿Cómo se escribe esto para que no quede nada a interpretación?**

Vienes de [[la-bitacora-del-taller|leer la bitácora]] · Aquí: el modelo formal ·
Sigue: resolverlo.

## 1 · El modelo completo

$$\max\; 5x_1 + 4x_2$$

$$6x_1 + 4x_2 \le 24 \quad \text{(aleación, kg)}$$

$$x_1 + 2x_2 \le 6 \quad \text{(calibración, horas)}$$

$$x_1, x_2 \ge 0, \qquad x_1, x_2 \in \mathbb{Z}$$

Renglón por renglón, contra la bitácora:

| Frase | Renglón |
|---|---|
| «cuántos rovers y cuántas sondas» | $x_1$ = rovers, $x_2$ = sondas |
| «transmite 5 MB / 4 MB al día» | $5x_1 + 4x_2$, y se maximiza |
| «24 kg; 6 kg y 4 kg cada uno» | $6x_1 + 4x_2 \le 24$ |
| «6 horas; 1 h y 2 h cada uno» | $x_1 + 2x_2 \le 6$ |
| «media sonda no transmite» | $x \in \mathbb{Z}$ |
| «la electricidad del taller» | nada |
| «no más de cuatro rovers» | nada: $6x_1 \le 24$ ya da $x_1 \le 4$ |

## 2 · Cada parte, con su nombre

::: definition {#opt-entera title="Variable entera"}
Una variable de decisión es **entera** cuando su valor solo tiene sentido en
$\mathbb{Z}$: 0, 1, 2, 3… y nunca $3/2$.

No es una restricción más. Es parte del **dominio**: lo que la variable puede
ser antes de mirar ninguna desigualdad.
:::

En el taller, $x_2 = 3/2$ no es «una sonda a medias». Es una sonda que no
transmite, y un plan que no existe.

::: definition {#opt-problema-entero title="Problema lineal entero"}
Un problema lineal con todas sus variables enteras:

$$\max\; c^{\mathsf T}x \quad\text{s.a.}\quad Ax \le b,\quad x \ge 0,\quad x \in \mathbb{Z}^n$$

Su **conjunto factible** es $F = \{\,x \in \mathbb{Z}^n_{\ge 0} : Ax \le b\,\}$.
:::

Todo lo de la clase 2 sigue igual salvo la última línea, y esa última línea lo
cambia todo: $F$ ya no es una región, es un **conjunto de puntos sueltos**.

::: remark {#opt-binaria title="El caso binario"}
Si además $x \le 1$, cada variable solo vale 0 o 1: **binaria**. Es el caso de
«lo llevo o no lo llevo», y es donde viven las frases lógicas —«si A entonces B»
se escribe $x_B \ge x_A$—. Aquí no lo necesitamos: los rovers se cuentan.
:::

## 3 · Dos variantes

::: exercise {#opt-ej-cargamento title="Variante 1 — llega un cargamento"}
Ahora hay **30 kg** de aleación. Escribe el modelo nuevo y di qué se movió.
:::

::: answer {#opt-resp-cargamento of="opt-ej-cargamento"}
Cambia **un número y nada más**: $6x_1 + 4x_2 \le 30$.

$c$ igual, $A$ igual, dominio igual. Los datos viven en $b$; la forma del modelo
no se entera. Lo único que sí crece es cuántos planes hay que considerar: ahora
$x_1$ puede llegar a 5.
:::

::: exercise {#opt-ej-antenas title="Variante 2 — solo hay tres antenas"}
Cada rover necesita su propia antena y solo hay 3. Escribe el modelo nuevo.
:::

::: answer {#opt-resp-antenas of="opt-ej-antenas"}
Un renglón nuevo: $x_1 \le 3$.

Y fíjate en qué **tipo** de renglón es. No es un recurso: no hay nada que se
reparta entre las dos variables, la desigualdad menciona una sola. Es una
@opt-cota, de las que definiste en la clase 1.

Con esto, la frase del comandante sí habría sido una restricción — pero decía 4,
y la aleación ya daba 4. Una cota que repite lo que ya sabías no agrega nada;
una que dice menos, sí.
:::

## 4 · Por qué lo que ya sabes no cierra

Breve, porque la respuesta larga es la página siguiente.

| Lo que sabes | Por qué se queda corto |
|---|---|
| Dibujar la región | La región es la misma. Pero ahora **solo cuentan los puntos** de la retícula, y el mejor punto no tiene por qué estar en una esquina |
| Simplex | Te entrega una esquina, y una esquina puede no ser un punto: aquí da $x_2 = 3/2$ |
| Redondear esa esquina | El vecino de abajo transmite menos, y el de arriba no cabe en la nave |
| El gradiente | Necesita pendiente. Entre «2 sondas» y «3 sondas» no hay nada por donde bajar |

Lo que se rompió tiene nombre: **el conjunto factible dejó de ser convexo.** Ya
no puedes caminar dentro de él, porque no hay dentro.

> **Cuidado.** $x \in \mathbb{Z}$ no reemplaza a $x \ge 0$. Los enteros incluyen
> los negativos, y $-2$ rovers pasa todas las restricciones de recurso.

## Lo que hay que llevarse

- El modelo entero es el lineal más una línea: $x \in \mathbb{Z}^n$.
- Un dato que cambia mueve $b$; una frase nueva agrega un renglón; el tipo de
  número mueve el dominio. Son tres sitios distintos.
- Perdiste la región y ganaste una lista. La página siguiente la lee entera:
  [[enumerar|enumerar]].
