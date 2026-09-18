---
id: el-modelo-del-taller
title: El modelo, escrito
nav_title: El modelo
summary: "Qué sale de la bitácora y qué se queda fuera, el modelo en forma canónica con su dominio declarado, tres variantes que obligan a inventar variables nuevas, y por qué los métodos anteriores dejan de cerrar."
status: ready
estimated_time: 30m
tags: [optimizacion, modelado, entera]
---

# El modelo, escrito

**¿Cómo se escribe esto para que no quede nada a interpretación?**

Vienes de [[la-bitacora-del-taller|leer la bitácora]] · Aquí: el modelo formal ·
Sigue: resolverlo.

**Compara con lo que escribiste.** Si algo no coincide, lo interesante es *dónde*
deja de coincidir, no cuánto.

## 1 · Qué sale de la bitácora

Las cuatro preguntas, contestadas:

| Parte | En la bitácora |
|---|---|
| Lo que decides | Cuántos rovers y cuántas sondas fabricar |
| Lo que te limita | 24 kg de aleación · 6 horas de calibración |
| Lo que mides | MB transmitidos al día, y los quieres al máximo |
| Qué clase de números | **Cantidades completas.** Media sonda no es media respuesta: es nada |

Y las tres que escondía:

| Trampa | Cuál era | Qué se hace con ella |
|---|---|---|
| Un dato que sobra | La electricidad del taller | Fuera: es igual en todos los planes |
| Un dato que falta | **¿Sirve de algo media sonda?** Nadie lo dijo | Preguntar. Respuesta: no transmite |
| Una frase que no aporta | «No más de cuatro rovers» | Fuera: la aleación ya lo impide |

La segunda es la importante. Todo lo que hace distinta a esta clase cuelga de esa
respuesta.

## 2 · El modelo, con cada parte nombrada

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
se escribe $x_B \ge x_A$—. Aquí no lo necesitamos para contar: los rovers se
cuentan.
:::

::: remark {#opt-indicadora title="Variable indicadora"}
Una **indicadora** es una binaria que no cuenta nada: solo dice **si algo
ocurre**. ¿Se enciende la línea? ¿Se usa el lote?

Por sí sola no hace nada. Solo sirve si se **enlaza** con las variables que sí
cuentan, mediante desigualdades que la obliguen a valer 1 cuando eso ocurre.
Cuáles son esas desigualdades es el trabajo de los tres ejercicios de abajo.
:::

## 3 · Tres variantes, y ninguna es un cambio de número

::: exercise {#opt-ej-encender title="Variante 1 — encender cuesta"}
Poner en marcha la línea de rovers gasta **3 horas de calibración**, se fabrique
uno o se fabriquen cuatro. Si no se fabrica ninguno, no se gasta.
:::

::: answer {#opt-resp-encender of="opt-ej-encender"}
Una variable nueva, $y \in \{0,1\}$: ¿se enciende la línea?

$$x_1 + 2x_2 + 3y \le 6 \qquad\text{(calibración)}$$
$$x_1 \le 3y \qquad\text{(enlace)}$$

**Lo difícil es el enlace, y tiene dos sutilezas.**

**De dónde sale el 3.** Es la cota más pequeña que sigue siendo válida, y hay
que buscarla en el renglón que el costo fijo acaba de cambiar: si se enciende,
$y=1$ y la calibración deja $x_1 + 2x_2 \le 3$, así que $x_1 \le 3$. Un número
más grande —el 4 de la aleación, o un 1000— también da un modelo **correcto**,
y más difícil de resolver: usa la más chica que puedas justificar.

Y fíjate en que $x_1 \le 3y$ **no** es una @opt-cota: su lado derecho no es un
número, es otra variable. Es un **enlace**.

**Falta el enlace al revés, y no hace falta.** Nada impide $y=1$ con $x_1=0$,
pero encender cuesta 3 horas y no da nada: ningún plan óptimo lo haría. Si
encender regalara algo, sí habría que escribir $y \le x_1$.
:::

::: exercise {#opt-ej-lote title="Variante 2 — o ninguno, o lote completo"}
Los rovers se calibran en lote: o no fabricas ninguno, o fabricas **al menos
tres**. Cuatro y cinco están bien; uno y dos, no.
:::

::: answer {#opt-resp-lote of="opt-ej-lote"}
Otra vez una indicadora $y \in \{0,1\}$, y esta vez **dos** enlaces:

$$3y \;\le\; x_1 \;\le\; 4y$$

El techo aquí sí es 4 y no 3: en esta variante la calibración no cambió, así que
la cota más apretada vuelve a salir de la aleación, $6x_1 \le 24$.

**Por qué no se puede sin ella.** Los valores permitidos de $x_1$ son
$\{0\} \cup \{3,4\}$, y eso tiene un **hueco**. Una desigualdad sobre $x_1$ sola
solo puede describir un intervalo, y ningún intervalo se salta el 1 y el 2 sin
saltarse también el 0.

**Y por qué $x_1 \ge 3y$ y no $x_1 \ge 3$.** Lo segundo prohibiría no fabricar
ninguno, que es justamente una de las dos opciones que el protocolo permite.
:::

::: exercise {#opt-ej-antena-compartida title="Variante 3 — la antena se comparte"}
Los dos primeros rovers transmiten 5 MB cada uno; del tercero en adelante, solo
**3 MB**. Sin variables nuevas de sí o no.
:::

::: answer {#opt-resp-antena-compartida of="opt-ej-antena-compartida"}
Parte la variable en sus dos tramos: $x_1 = u + v$, con

$$0 \le u \le 2, \qquad 0 \le v \le 2, \qquad u, v \in \mathbb{Z}$$

El objetivo pasa a ser $5u + 3v + 4x_2$, y en las dos restricciones $x_1$ se
sustituye por $u+v$.

**Aquí está el edge case.** Nada en el modelo obliga a llenar $u$ antes que $v$:
el plan «$u=0$, $v=2$» es factible y significaría cobrar el precio del tercer y
el cuarto rover habiendo fabricado dos. Funciona igual **porque el tramo caro va
primero**: como $u$ paga 5 y $v$ paga 3, ningún óptimo abre el segundo tramo sin
haber llenado el primero. Lo hace solo.

**Dale la vuelta y el truco miente.** Si los dos primeros rindieran 3 MB y del
tercero en adelante 5 —rendimiento creciente—, el mismo modelo declara **18 MB**
con $u=0,\ v=2$, y la verdad es **16**. Ahí sí hace falta una indicadora que
obligue a llenar el primer tramo antes de abrir el segundo.

Partir en tramos vale cuando cada tramo rinde **menos** que el anterior. Con
rendimiento creciente, no.
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
- Hay condiciones que **no son un renglón más**: piden una variable nueva, y la
  parte difícil nunca es la variable, es el enlace que la ata a las demás.
- Perdiste la región y ganaste una lista. La página siguiente la lee entera:
  [[enumerar|enumerar]].
