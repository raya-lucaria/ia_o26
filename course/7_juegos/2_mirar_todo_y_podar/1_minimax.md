---
id: minimax
title: Minimax a mano
nav_title: Minimax a mano
summary: "Valorar un árbol de juego desde los finales hacia la raíz: un subárbol de hexapawn a mano, el valor contra la jugada y el resultado del juego completo."
status: ready
estimated_time: 20m
tags: [juegos, minimax]
---

# Minimax a mano

**¿Quién gana si los dos juegan perfecto, y con qué jugada?**

Al terminar tendrás **el valor de una posición de hexapawn calculado a
mano**, la jugada que lo alcanza y la respuesta a por qué gana quien juega
segundo.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todo o deja al rival sin jugada; gana
> $10-k$ puntos, donde $k$ es el número de jugadas de la partida, y el otro
> pierde esos mismos puntos.

**Problema activo: el subárbol tras a1-a2 y b3-b2.** Es la posición del
ejercicio «Decide qué jugadas hay» de [[escribir-el-juego|Escribir el juego]].
Mueven Blancas y ya se hicieron $k=2$ jugadas.

::: table {#jue-c2-subarbol title="El problema activo: mueven Blancas, k = 2"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | N |
| **2** | B | N | · |
| **1** | · | B | B |
:::

Blancas tiene dos jugadas: $A(s)=\{\text{c1-c2},\ \text{c1xb2}\}$. La
pregunta de esta página es cuál conviene y cuántos puntos asegura.

Nosotros ya conocemos el resultado de c1-c2 por la clase 1; el algoritmo
empezará sin él.

> **Recordatorio de [[opt-objetivo-juego-practica|elegir una jugada cuando el rival responde]].**
> En un final, el valor es la utilidad: $V(s)=U(s)$. En el turno de MAX,
> $V(s)$ es el **máximo** de los valores de sus hijos; en el de MIN, el
> **mínimo**. Se calcula **desde los finales hacia atrás**. Aquí MAX es
> Blancas y MIN es Negras, y todo se mide en puntos de Blancas.

## 1 · Escribir el árbol completo

**Piensa: desde esta posición, ¿cuántas partidas distintas pueden pasar?**

Antes de valorar nada, escribimos todas las continuaciones. Las jugadas van
en un **orden fijo**: por casilla de salida (a1, b1, c1, luego la fila 2 y
la 3) y, para cada peón, primero avanzar y después capturar. Ese orden
importará en alfa-beta.

Cada renglón es un estado; la sangría indica quién es hijo de quién. Cada
nodo lleva un **número**, n1 a n13, porque hay nombres de jugada que se
repiten: a3xb2 aparece en n4 y en n8, y a2-a3 en n5 y en n9.

- **n1 · Raíz** · mueven B, $k=2$
  - **n2 · c1-c2** · FINAL: Negras no tiene jugada, $k=3$
  - **n3 · c1xb2** · mueven N, $k=3$
    - **n4 · a3xb2** · mueven B, $k=4$
      - **n5 · a2-a3** · FINAL: Blancas llega a la fila 3, $k=5$
    - **n6 · c3-c2** · mueven B, $k=4$
      - **n7 · b1xc2** · mueven N, $k=5$
        - **n8 · a3xb2** · mueven B, $k=6$
          - **n9 · a2-a3** · FINAL: Blancas llega, $k=7$
          - **n10 · c2-c3** · FINAL: Blancas llega, $k=7$
      - **n11 · b2-b3** · FINAL: Blancas llega, $k=5$
      - **n12 · b2xa3** · FINAL: Blancas llega, $k=5$
    - **n13 · c3xb2** · FINAL: Blancas no tiene jugada, $k=4$

Son **13 nodos**: 7 finales (n2, n5, n9, n10, n11, n12, n13) y 6 donde
alguien decide (n1, n3, n4, n6, n7, n8). El árbol es pequeño porque los
peones se bloquean rápido.

Estos son los tableros de la rama n3, que es la que pide más trabajo:

::: table {#jue-c2-tras-captura title="n3, tras c1xb2: mueven Negras, k = 3"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | N |
| **2** | B | B | · |
| **1** | · | B | · |
:::

Negras tiene tres jugadas: a3xb2 (n4) captura el peón de b2, c3-c2 (n6)
avanza y c3xb2 (n13) captura también en b2.

::: table {#jue-c2-tras-a3xb2 title="n4, tras c1xb2 y a3xb2: mueven Blancas, k = 4"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | · | · | N |
| **2** | B | N | · |
| **1** | · | B | · |
:::

::: table {#jue-c2-tras-c3-c2 title="n6, tras c1xb2 y c3-c2: mueven Blancas, k = 4"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | · |
| **2** | B | B | N |
| **1** | · | B | · |
:::

::: table {#jue-c2-tras-c3xb2 title="n13, tras c1xb2 y c3xb2: mueven Blancas, k = 4"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | · |
| **2** | B | N | · |
| **1** | · | B | · |
:::

En n13, Blancas no puede mover: a2 tiene a3 ocupada enfrente y nada que
capturar en b3; b1 tiene b2 ocupada y nada que capturar en a2 ni en c2.
Por eso es final y gana Negras.

## 2 · Valorar los finales

**Piensa: ¿qué número le corresponde a cada final?**

Los finales son datos: la utilidad la fija el reglamento. Con
$U=\pm(10-k)$:

::: table {#jue-c2-finales title="Los siete finales del subárbol"}
| Nodo | Camino desde la raíz | Qué pasa | $k$ | $U$ |
|---|---|---|---:|---:|
| n2 | c1-c2 | Negras sin jugada: gana Blancas | 3 | 7 |
| n5 | c1xb2, a3xb2, a2-a3 | Blancas llega a la fila 3 | 5 | 5 |
| n9 | c1xb2, c3-c2, b1xc2, a3xb2, a2-a3 | Blancas llega | 7 | 3 |
| n10 | c1xb2, c3-c2, b1xc2, a3xb2, c2-c3 | Blancas llega | 7 | 3 |
| n11 | c1xb2, c3-c2, b2-b3 | Blancas llega | 5 | 5 |
| n12 | c1xb2, c3-c2, b2xa3 | Blancas llega | 5 | 5 |
| n13 | c1xb2, c3xb2 | Blancas sin jugada: gana Negras | 4 | −6 |
:::

Seis de los siete finales los gana Blancas. Eso **no** dice que Blancas
gane: falta saber si Negras puede llevar la partida al séptimo.

## 3 · Subir desde los finales

**Piensa: ¿por qué no se puede valorar n3 antes que n6?**

Valoramos cada nodo cuando ya conocemos a todos sus hijos. Por eso
empezamos por el más profundo.

### Primer paso: la rama más larga

**Estamos aquí:** en n8 (c1xb2 → c3-c2 → b1xc2 → a3xb2). Mueven Blancas
(MAX), $k=6$. Sus dos hijos son finales: n9 y n10 valen 3 y 3.

**Pendiente:** su valor, y el de su padre n7.

$$V(\text{n8})=\max\{3,\ 3\}=3.$$

Su padre, n7 (tras b1xc2), es de Negras y tiene un solo hijo: Negras está
**obligada** a jugar a3xb2. Su valor también es 3. Un nodo con un solo hijo
copia el valor de ese hijo, sea MAX o MIN.

### Segundo paso: el nodo n6

**Estamos aquí:** en n6 (c1xb2 → c3-c2) mueven Blancas (MAX), $k=4$. Ya
conocemos sus tres hijos: n7 vale 3, n11 vale 5 y n12 vale 5.

**Pendiente:** el valor de n6 y qué jugada lo alcanza.

::: exercise {#jue-c2-ej-paso-max title="Decide el valor del nodo n6"}
Calcula el valor de n6, tras c1xb2 y c3-c2. ¿Qué jugadas de Blancas lo
alcanzan? ¿Por qué b1xc2 (n7), que también gana, no es la mejor?
:::

::: answer {#jue-c2-resp-paso-max of="jue-c2-ej-paso-max"}
Es un nodo MAX: $V(\text{n6})=\max\{3,5,5\}=5$. Lo alcanzan **dos**
jugadas, b2-b3 (n11) y b2xa3 (n12): las dos llegan a la fila 3 en la
jugada 5. La captura b1xc2 también termina en victoria, pero dos jugadas
después, en $k=7$, y eso vale 3. Con esta utilidad, ganar antes vale más.
:::

n6 vale **5**. Que dos jugadas empaten es normal; por eso más adelante
escribiremos $a^{∗}\in\operatorname*{arg\,max}$, con pertenencia.

### Tercer paso: el nodo n4

**Estamos aquí:** en n4 (c1xb2 → a3xb2) mueven Blancas, $k=4$. Solo tiene
la jugada a2-a3 (n5), que llega a la fila 3 y vale 5.

**Pendiente:** su valor. Como tiene un solo hijo, n4 vale **5**.

### Cuarto paso: el turno de Negras

**Estamos aquí:** en n3 (tras c1xb2) mueven Negras (MIN), $k=3$. Ya
conocemos sus tres hijos: n4 vale 5, n6 vale 5 y n13 vale −6.

**Pendiente:** el valor de n3 para Blancas.

::: exercise {#jue-c2-ej-paso-min title="Decide qué hace Negras"}
Calcula el valor de n3. ¿Qué jugada elige Negras, y por qué no importa
que dos de sus tres jugadas pierdan?
:::

::: answer {#jue-c2-resp-paso-min of="jue-c2-ej-paso-min"}
Es un nodo MIN: $V(\text{n3})=\min\{5,5,-6\}=-6$. Negras elige **c3xb2**
(n13), que deja a Blancas sin jugada y gana en la jugada 4. Que a3xb2 (n4)
y c3-c2 (n6) pierdan no importa: Negras no está obligada a jugarlas. Al
rival le basta **una** respuesta buena.
:::

Capturar en b2 con c1 vale **−6** para Blancas: Negras responde c3xb2 y
gana. Este es el paso que una lectura optimista se salta.

### Quinto paso: la raíz

**Estamos aquí:** en n1 mueven Blancas (MAX). n2 (c1-c2) vale 7 y n3
(c1xb2) vale −6.

$$V(\text{n1})=\max\{7,\ -6\}=7.$$

::: table {#jue-c2-valores title="Los valores del subárbol, de abajo hacia arriba"}
| Nodo | Turno | Hijos y sus valores | Operación | Valor |
|---|---|---|---|---:|
| n8 = c1xb2 → c3-c2 → b1xc2 → a3xb2 | B (MAX) | n9 = 3, n10 = 3 | máximo | 3 |
| n7 = c1xb2 → c3-c2 → b1xc2 | N (MIN) | n8 = 3 | único hijo | 3 |
| n6 = c1xb2 → c3-c2 | B (MAX) | n7 = 3, n11 = 5, n12 = 5 | máximo | 5 |
| n4 = c1xb2 → a3xb2 | B (MAX) | n5 = 5 | único hijo | 5 |
| n3 = c1xb2 | N (MIN) | n4 = 5, n6 = 5, n13 = −6 | mínimo | −6 |
| n1 = raíz | B (MAX) | n2 = 7, n3 = −6 | máximo | **7** |
:::

## 4 · Separar el valor de la jugada

**Piensa: el número 7, ¿le dice a Blancas qué hacer?**

No directamente. El 7 es el **valor**: los puntos que Blancas asegura. La
**jugada** es la acción que lo alcanza:

$$V(s)=7,\qquad a^{∗}\in\operatorname*{arg\,max}_{a\in A(s)}V\bigl(T(s,a)\bigr)=\{\text{c1-c2}\}.$$

El plan óptimo de Blancas es **c1-c2**: deja a Negras sin jugada y gana ya,
en la jugada 3. Si Blancas capturara en b2, Negras respondería c3xb2 y
Blancas perdería.

Hay otro dato escondido en este cálculo. Tras a1-a2, la computadora valora
la respuesta b3-b2 de Negras en 7, y la respuesta b3xa2 en −6. **Nuestro
problema activo empezó con un error de Negras.**

## 5 · Calcular el juego completo

**Piensa: si minimax resuelve un subárbol de 13 nodos, ¿qué impide
resolver el juego entero?**

Nada: el árbol completo tiene 252 nodos. A mano es tedioso; la computadora
lo hace en un instante con el mismo procedimiento. Estos son los valores de
las tres jugadas iniciales de Blancas:

::: table {#jue-c2-juego-completo title="Hexapawn completo, con U = ±(10 − k)"}
| Primera jugada de Blancas | Valor |
|---|---:|
| a1-a2 | −6 |
| b1-b2 | −4 |
| c1-c2 | −6 |
:::

Las tres son negativas, así que $V(s_0)=\max\{-6,-4,-6\}=-4$. Con juego
perfecto **gana Negras en la jugada 6**: $-(10-6)=-4$. La mejor jugada de
Blancas, b1-b2, solo retrasa la derrota.

Con la utilidad simple, $+1$ si gana Blancas y $-1$ si gana Negras, el
valor del inicio es $-1$. **Quien empieza pierde** si el rival juega
perfecto. Esa es la respuesta a la pregunta de la clase 1: en tus partidas,
si usaron nuestra regla de que quedarse sin jugada pierde, quien jugó
segundo tenía una respuesta ganadora a cada jugada; si
alguna vez ganó quien empezó, alguien se equivocó en el camino, como Negras
con b3-b2.

::: exercise {#jue-c2-ej-mas-menos-uno title="Decide qué se pierde con ±1"}
Recalcula el valor del problema activo con la utilidad simple: $+1$ si
gana Blancas y $-1$ si gana Negras. ¿Sigue siendo c1-c2 una jugada
óptima? ¿Qué información se pierde?
:::

::: answer {#jue-c2-resp-mas-menos-uno of="jue-c2-ej-mas-menos-uno"}
Los finales valen $+1$ salvo n13 (c3xb2), que vale $-1$. Subiendo igual:
n8 y n7 valen 1, n6 vale $\max\{1,1,1\}=1$, n4 vale 1, n3 vale
$\min\{1,1,-1\}=-1$ y la raíz $\max\{1,-1\}=+1$. **c1-c2 sigue siendo
óptima.**

Lo que se pierde está en n6: con $\pm1$ las tres jugadas de Blancas
empatan en 1, y b1xc2 (n7), que gana en la jugada 7, parece tan buena como
b2-b3 (n11), que gana en la 5. Con $\pm1$ no distinguimos ganar en 5 de
ganar en 7.
:::

**Punto de control:** deberías poder tomar un árbol de cuatro o cinco
niveles, numerar sus nodos, valorar sus finales, subir con máximos y
mínimos hasta la raíz y decir qué jugada elige MAX. Si te trabas al subir,
vuelve a la tabla de la sección 3.

## Lo que hay que llevarse

- Minimax valora desde los finales: máximo en el turno de MAX, mínimo en el
  de MIN. Un nodo se valora solo cuando ya se conocen todos sus hijos.
- El valor es un número; la jugada sale del $\operatorname{arg\,max}$ en la
  raíz. En el problema activo, $V=7$ con c1-c2.
- Hexapawn vale $-4$ con juego perfecto: gana Negras, el segundo jugador.

Continúa con [[minimax-como-algoritmo|minimax como algoritmo]].
