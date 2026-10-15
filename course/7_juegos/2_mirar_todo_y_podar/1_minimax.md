---
id: minimax
title: Minimax a mano
nav_title: Minimax a mano
summary: "Calcular a mano V y Q desde MAX, distinguir el valor de la jugada que lo alcanza y resolver n1 y hexapawn con juego óptimo."
status: ready
estimated_time: 30m
tags: [juegos, minimax]
---

# Minimax a mano

**¿Quién gana si los dos juegan lo mejor, y con qué jugada?**

Lo decide el valor de cada estado, calculado desde los finales hacia arriba. Al terminar tendrás:

- **El valor de n1, calculado a mano**, nodo por nodo.
- **La jugada que lo alcanza**, separada del número.
- **La respuesta a por qué gana quien juega segundo** en hexapawn.

## Lo que traes

- **El estado incluye el turno.** $S_F$ reconoce los finales (@jue-c1-finales); $\mathrm{Pl}(s)$ lee del estado quién mueve: Blancas es MAX y Negras es MIN (@jue-c1-pl).
- **Las jugadas y adónde llevan.** $A(s)$ son las jugadas permitidas (@jue-c1-acciones) y $T(s,a)$ el estado al que lleva $a$ (@jue-c1-transicion).
- **El pago de un final.** Cada juego define $U(s)$ desde MAX (@jue-c1-utilidad). Solo existe en los finales.
- **El valor y la jugada.** $V(s)$ y $Q(s,a)$ se definieron con palabras en @jue-c1-valor-jugada-estrategia; esta página da la regla para calcularlos.

La tabla completa, con el problema escrito, está en [[juegos-mirar-todo-y-podar|la página de la clase]].

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas.
>
> Un peón avanza una casilla si está vacía o captura en diagonal hacia delante. Gana quien llega a la fila del rival, captura todos los peones rivales o deja al rival sin jugada.
>
> **El pago, desde MAX:** $U=+1$ si gana Blancas y $U=-1$ si gana Negras. Hexapawn no tiene empates.

> **Supuestos de esta página.** Los mismos de [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin azar, todo a la vista, toda partida termina y suma cero.

---

## El mapa de minimax

- **Qué valor rastrea:** $V(s)$ en cada estado y $Q(s,a)=V(T(s,a))$ en cada jugada, siempre desde MAX.
- **Dónde lo guarda:** en cada nodo, hasta entregarlo a su padre.
- **Cómo sube:** con el máximo en los nodos de MAX y el mínimo en los de MIN; nunca con un promedio.

**Ejemplo mínimo.** Un nodo de MAX tiene dos hijos de MIN, cada uno con dos finales debajo.

::: table {#jue-c2-tab-abstracto-minimax title="Un nodo de MAX con dos jugadas"}
| Jugada de MAX | Finales debajo | $Q$ de la jugada |
|---|---|---|
| $a$ | $+1$ y $-1$ | $-1$ |
| $b$ | $0$ y $0$ | $0$ |
:::

- **MAX juega $b$ y asegura el empate.** Bajo $a$ hay una victoria, pero MIN nunca lo dejaría llegar a ella.
- **Los dos pares promedian $0$ y aun así valen distinto.** Decide lo que MAX puede asegurar, no el mejor final que hay debajo ni el promedio.

---

## 1 · El problema, en n1

**Piensa: ¿qué pedía el problema de la unidad?**

En cada estado de MAX, la jugada que le asegura más si los dos juegan lo mejor (@jue-c1-problema). Esta página lo resuelve en un solo estado, **n1**: el que se alcanza con $\text{a1}\textbf{-}\text{a2}$ y $\text{b3}\textbf{-}\text{b2}$.

::: table {#jue-c2-n1 title="n1: mueven Blancas"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | N |
| **2** | B | N | · |
| **1** | · | B | B |
:::

> **El problema de esta página.**
>
> **Dado:** el juego de hexapawn, con sus siete piezas, y el estado n1.
>
> **Encontrar:** cuánto asegura Blancas desde n1, $V(\text{n1})$, y con cuál de sus dos jugadas, $\text{c1}\textbf{-}\text{c2}$ o $\text{c1}\textbf{x}\text{b2}$. Es decir, una jugada $a^{∗}\in\operatorname*{arg\,max}_{a\in A(\text{n1})} Q(\text{n1},a)$.

El subgrafo entero de n1 ya lo dibujaste en [[el-juego-como-grafo|El juego como grafo]]. Aquí está otra vez:

::: figure {#jue-c2-subgrafo title="El subgrafo de n1, como lo dejó la clase 1"}
![Trece nodos numerados n1 a n13. De n1 (MAX) salen c1-c2 hacia n2, final con U = +1, y c1xb2 hacia n3 (MIN). De n3 salen a3xb2 hacia n4, c3-c2 hacia n6 y c3xb2 hacia n13, final con U = −1. n4 lleva a n5, final +1. n6 lleva a n7, n11 y n12; n11 y n12 son finales +1. n7 lleva a n8, y n8 a n9 y n10, finales +1](../_assets/jue-subgrafo-n1.svg)
:::

Las hojas ya tienen su número, $U$. Los nodos de en medio todavía no. Esta página les pone uno a cada uno.

---

## 2 · La regla: máximo, mínimo y pago

**Piensa: si sabes cuánto vale cada hijo de un nodo, ¿cuánto vale el nodo?**

Depende de quién mueve. Si mueve MAX, elige el hijo que más vale; si mueve MIN, el que menos. Y un final ya tiene su número.

::: definition {#jue-c2-valor title="Valor minimax"}
**Qué es:** el **valor** $V(s)$ es el pago para MAX si los dos juegan lo mejor desde $s$. Ya lo definimos con palabras en @jue-c1-valor-jugada-estrategia; aquí va **cómo se calcula**.

**Cómo se calcula.** Primero la jugada: vale lo que vale el hijo al que lleva,

$$\mathbf{Q(s,a)=V\bigl(T(s,a)\bigr)}.$$

Después el estado, según quién mueve:

$$\mathbf{V(s)=\begin{cases}U(s) & \text{si } s\in S_F,\\[2pt] \max_{a\in A(s)} Q(s,a) & \text{si } \mathrm{Pl}(s)=\text{MAX},\\[2pt] \min_{a\in A(s)} Q(s,a) & \text{si } \mathrm{Pl}(s)=\text{MIN}.\end{cases}}$$

**MAX elige el mayor $Q$ y MIN el menor.** Los dos números se miden desde MAX: el signo no cambia al subir.

**La fórmula se usa a sí misma:** $V$ aparece a los dos lados del igual, a través de $Q$. El valor de un nodo se calcula con el de sus **hijos**, y los **finales** detienen la cuenta, porque su valor ya lo da $U$.

**Qué significa:** si MAX elige así en cada turno, obtiene exactamente $V(s)$ contra un MIN que juega óptimamente.

**Qué no es:** no es lo que pasará en una partida real. Si MIN se equivoca, MAX puede obtener más; nunca menos, **si MAX sigue eligiendo óptimamente**. Y «MIN minimiza la $U$ de MAX» solo vale con dos jugadores y suma cero o constante (@jue-c1-nota-jugadores).
:::

**En n1 ya hay un $Q$ que se lee directo.** $\text{c1}\textbf{-}\text{c2}$ lleva a n2, que es final: $Q(\text{n1},\text{c1}\textbf{-}\text{c2})=V(\text{n2})=U(\text{n2})=+1$. El otro, $Q(\text{n1},\text{c1}\textbf{x}\text{b2})=V(\text{n3})$, espera a que se conozca n3.

Por eso se calcula **de abajo hacia arriba**: un nodo se valora solo cuando ya se conocen todos sus hijos.

---

## 3 · Empezar por los finales

**Piensa: ¿qué número le toca a cada hoja?**

Ninguno se calcula: los da $U$. En el subgrafo hay 7 finales.

- **Valen $+1$**, porque gana Blancas: n2, n5, n9, n10, n11 y n12.
- **Vale $-1$**, porque gana Negras: n13. Ahí Blancas no tiene jugada.

Seis de siete finales los gana Blancas. Eso **no** dice que Blancas gane: falta saber si Negras puede llevar la partida al séptimo.

---

## 4 · Subir por la rama más honda

**Piensa: ¿cuál es el primer nodo que puedes valorar?**

Uno cuyos hijos sean todos finales. El más hondo es **n8**: mueve Blancas (MAX) y sus dos jugadas llevan a n9 y n10, que valen $+1$.

$$V(\text{n8})=\max\{+1,\ +1\}=+1.$$

Su padre, **n7**, es de Negras y tiene un solo hijo: Negras está **obligada** a jugar $\text{a3}\textbf{x}\text{b2}$. Un nodo con un solo hijo copia el valor de ese hijo, sea MAX o MIN: $V(\text{n7})=+1$.

Lo mismo pasa con **n4**: mueve Blancas, su única jugada es $\text{a2}\textbf{-}\text{a3}$ y lleva a n5, que vale $+1$. Entonces $V(\text{n4})=+1$.

---

## 5 · Valorar n6: el turno de Blancas

**Estamos aquí:** en n6, al que se llega con $\text{c1}\textbf{x}\text{b2}$ y $\text{c3}\textbf{-}\text{c2}$. Mueve Blancas. Ya conocemos sus tres hijos: n7, n11 y n12.

::: exercise {#jue-c2-ej-paso-max title="Decide el valor de n6"}
1. Calcula $V(\text{n6})$.
2. ¿Qué jugadas de Blancas lo alcanzan?
:::

::: hint {#jue-c2-pista-paso-max of="jue-c2-ej-paso-max" title="Qué operación toca"}
Mira quién mueve en n6: eso decide si tomas el máximo o el mínimo de los $Q$. Cada $Q$ es el valor de un hijo, y los de n7, n11 y n12 ya están arriba.
:::

::: answer {#jue-c2-resp-paso-max of="jue-c2-ej-paso-max"}
1. Mueve Blancas, así que es el máximo: $V(\text{n6})=\max\{+1,\ +1,\ +1\}=+1$.
2. **Las tres**: $\text{b1}\textbf{x}\text{c2}$ (n7), $\text{b2}\textbf{-}\text{b3}$ (n11) y $\text{b2}\textbf{x}\text{a3}$ (n12). Empatan, y que varias jugadas empaten es normal.
:::

::: figure {#jue-c2-paso-1 title="Paso 1: valorar n6"}
![n6 arriba, donde mueve Blancas (MAX), con V = +1 resaltado. Abajo sus tres hijos: n7, donde mueve Negras, con V = +1; n11 y n12, finales que gana Blancas con U = +1. Las tres flechas, b1xc2, b2-b3 y b2xa3, van resaltadas porque las tres alcanzan el máximo](../_assets/jue-minimax-paso-1.svg)
:::

---

## 6 · Valorar n3: el turno de Negras

**Estamos aquí:** en n3, tras $\text{c1}\textbf{x}\text{b2}$. Mueve Negras. Sus hijos son n4, n6 y n13, y ya sabes cuánto vale cada uno.

::: exercise {#jue-c2-ej-paso-min title="Decide qué hace Negras"}
1. Calcula $V(\text{n3})$.
2. ¿Qué jugada elige Negras?
3. Dos de sus tres jugadas pierden. ¿Por qué no importa?
:::

::: hint {#jue-c2-pista-paso-min of="jue-c2-ej-paso-min" title="Desde el lado de Negras"}
El valor está en puntos de Blancas. Negras quiere que sea **bajo**. ¿Cuál de sus tres hijos es el peor para Blancas?
:::

::: answer {#jue-c2-resp-paso-min of="jue-c2-ej-paso-min"}
1. Mueve Negras, así que es el mínimo: $V(\text{n3})=\min\{+1,\ +1,\ -1\}=-1$.
2. **$\text{c3}\textbf{x}\text{b2}$**, que lleva a n13: Blancas se queda sin jugada y gana Negras.
3. Porque Negras no está obligada a jugarlas. Al rival le basta **una** respuesta buena.
:::

::: figure {#jue-c2-paso-2 title="Paso 2: valorar n3"}
![n3 arriba, donde mueve Negras (MIN), con V = −1 resaltado. Abajo sus tres hijos: n4 y n6, donde mueve Blancas, con V = +1, y n13, final que gana Negras con U = −1. Solo la flecha c3xb2 va resaltada: es la que alcanza el mínimo](../_assets/jue-minimax-paso-2.svg)
:::

**La respuesta de Negras vale $Q(\text{n3},\text{c3}\textbf{x}\text{b2})=-1$.** Es el valor óptimo para quien mueve, MIN, medido todavía desde MAX.

**Entonces capturar en b2 vale $-1$ para Blancas:** $Q(\text{n1},\text{c1}\textbf{x}\text{b2})=V(\text{n3})=-1$, porque Negras responde $\text{c3}\textbf{x}\text{b2}$ y gana. Éste es el paso que una lectura optimista se salta.

---

## 7 · Valorar n1 y elegir la jugada

**Piensa: el número $V(\text{n1})$, ¿le dice a Blancas qué hacer?**

No: dice cuánto asegura. Primero, los $Q$ de sus dos jugadas, que ya conoces:

::: table {#jue-c2-q-n1 title="Lo que vale cada jugada de Blancas en n1"}
| Jugada $a$ | Lleva a | $Q(\text{n1},a)$ |
|---|---|---:|
| $\text{c1}\textbf{-}\text{c2}$ | n2, final | $+1$ |
| $\text{c1}\textbf{x}\text{b2}$ | n3, de MIN | $-1$ |
:::

En n1 mueve Blancas, así que toma el mayor:

$$V(\text{n1})=\max_{a\in A(\text{n1})} Q(\text{n1},a)=\max\{+1,\ -1\}=+1.$$

::: figure {#jue-c2-paso-3 title="Paso 3: valorar n1"}
![n1 arriba, donde mueve Blancas (MAX), con V = +1 resaltado. Abajo sus dos hijos: n2, final que gana Blancas con U = +1, y n3, donde mueve Negras, con V = −1. La flecha c1-c2 va resaltada](../_assets/jue-minimax-paso-3.svg)
:::

El $+1$ **no** es una jugada: es lo que Blancas asegura. La jugada es la que lo alcanza. Se escribe con el $\operatorname{arg\,max}$ de [[diagnosticar-el-juego|Diagnosticar el juego]], el conjunto de jugadas que dan el máximo:

$$a^{∗}\in\operatorname*{arg\,max}_{a\in A(\text{n1})} Q(\text{n1},a)=\{\text{c1}\textbf{-}\text{c2}\}.$$

La estrella marca la jugada elegida, y se escribe $\in$ porque podría haber varias. Aquí hay una sola: **Blancas debe jugar $\text{c1}\textbf{-}\text{c2}$**. Deja a Negras sin jugada y gana en ese momento.

**MIN elige con el $\operatorname{arg\,min}$.** En n3, $\operatorname*{arg\,min}_{a\in A(\text{n3})} Q(\text{n3},a)=\{\text{c3}\textbf{x}\text{b2}\}$: la única jugada que da el mínimo.

Así queda el subgrafo con todos sus valores. Las flechas resaltadas son las jugadas que alcanzan el valor de su padre:

::: figure {#jue-c2-resuelto title="El subgrafo de n1, resuelto"}
![El subgrafo de n1 con un valor en cada nodo: n1, n4, n6, n7 y n8 valen +1; n3 vale −1. Los finales conservan su U: n13 vale −1 y los demás +1. Van resaltadas c1-c2 en n1, c3xb2 en n3 y las tres jugadas de n6, que empatan; también las jugadas únicas de n4 y n7, y las dos de n8](../_assets/jue-minimax-n1.svg)
:::

Los mismos valores, en el orden en que los calculamos:

1. **n8**, mueve Blancas: el máximo de n9 = +1 y n10 = +1 da **+1**.
2. **n7**, mueve Negras: su único hijo, n8, da **+1**.
3. **n4**, mueve Blancas: su único hijo, n5, da **+1**.
4. **n6**, mueve Blancas: el máximo de n7, n11 y n12, los tres +1, da **+1**.
5. **n3**, mueve Negras: el mínimo de n4 = +1, n6 = +1 y n13 = −1 da **−1**.
6. **n1**, mueve Blancas: el máximo de n2 = +1 y n3 = −1 da **+1**.

---

## 8 · Cuando dos jugadas empatan

**Piensa: en n6, las tres jugadas valen $+1$. ¿Da igual cuál jugar?**

Para el valor, sí: las tres ganan. Pero no ganan igual de rápido. Contando desde n6:

- **$\text{b2}\textbf{-}\text{b3}$ y $\text{b2}\textbf{x}\text{a3}$** llegan a la fila 3 en la primera jugada.
- **$\text{b1}\textbf{x}\text{c2}$** gana en la tercera jugada, contando las de los dos: Negras responde $\text{a3}\textbf{x}\text{b2}$ y Blancas todavía tiene que avanzar.

Preferir ganar rápido es razonable, pero **no está en el reglamento**: el pago solo dice quién gana (@jue-c1-utilidad). Por eso no lo cambiamos. Lo usamos solo para **desempatar** dentro del $\operatorname{arg\,max}$, como hacen los programas de ajedrez con el mate más corto. La justificación es práctica: una partida más corta deja menos jugadas en las que equivocarse.

> [!WARNING]
> Meter «ganar rápido» en el pago, por ejemplo con $U=\pm(10-k)$ donde $k$ cuenta las jugadas, tiene tres costos.
>
> - **$U$ dejaría de leerse del estado** $(\text{tablero},\text{turno})$: habría que guardar también $k$.
> - **El problema cambiaría:** ya no preguntaría quién gana, sino cuánto tarda.
> - **La constante tiene que superar la duración máxima.** Con $k\ge 10$, ganar valdría $0$ o menos y perder, $0$ o más. En hexapawn no pasa: ninguna partida dura más de 7 jugadas.
>
> El desempate da la misma preferencia sin tocar el modelo.

---

## 9 · El juego completo

**Piensa: si minimax resuelve 13 nodos, ¿qué impide resolver los 252?**

Nada: es el mismo procedimiento, y la computadora lo hace en un instante. Estos son los valores de las tres primeras jugadas de Blancas:

::: table {#jue-c2-juego-completo title="Hexapawn completo: las tres aperturas"}
| Primera jugada $a$ | $Q(s_0,a)$ |
|---|---:|
| $\text{a1}\textbf{-}\text{a2}$ | −1 |
| $\text{b1}\textbf{-}\text{b2}$ | −1 |
| $\text{c1}\textbf{-}\text{c2}$ | −1 |
:::

Las tres valen $-1$, así que $V(s_0)=-1$: **quien empieza pierde** si el rival juega perfecto. Ésa es la respuesta a la pregunta de la clase. En tus partidas, quien jugó segundo tenía desde el inicio una respuesta ganadora. Si alguna vez ganó quien empezó, alguien se equivocó en el camino.

Y n1 viene justo de una equivocación. Tras $\text{a1}\textbf{-}\text{a2}$, Negras tenía tres respuestas:

::: table {#jue-c2-respuestas-negras title="Tras a1-a2: las tres respuestas de Negras"}
| Respuesta de Negras | $Q$, desde Blancas |
|---|---:|
| $\text{b3}\textbf{-}\text{b2}$, que lleva a n1 | +1 |
| $\text{b3}\textbf{x}\text{a2}$ | −1 |
| $\text{c3}\textbf{-}\text{c2}$ | +1 |
:::

Solo la captura gana para Negras. **Nuestro problema empezó con un error de Negras**, y por eso Blancas gana desde n1.

::: exercise {#jue-c2-ej-que-asegura title="Decide qué dice cada número"}
1. $V(\text{n1})=+1$ y $V(s_0)=-1$. ¿Se contradicen? Blancas mueve en los dos.
2. Si en n3 Negras jugara $\text{a3}\textbf{x}\text{b2}$, ¿cuánto obtendría Blancas? ¿Contradice eso que $V(\text{n3})=-1$?
:::

::: hint {#jue-c2-pista-que-asegura of="jue-c2-ej-que-asegura" title="Qué mide V"}
$V(s)$ habla de lo que se puede **asegurar desde $s$**. ¿Desde qué estado habla cada número? ¿Y qué supone sobre el rival?
:::

::: answer {#jue-c2-resp-que-asegura of="jue-c2-ej-que-asegura"}
1. No. Hablan de estados distintos. Desde $s_0$, Negras puede asegurar la victoria. Desde n1 ya no: para llegar ahí, Negras jugó $\text{b3}\textbf{-}\text{b2}$ en vez de la captura.
2. $+1$: esa jugada lleva a n4, que vale $+1$. No lo contradice. $V(\text{n3})=-1$ es lo que Blancas obtiene si Negras juega **bien**. Contra un error, Blancas puede obtener más, nunca menos, si sigue eligiendo óptimamente.
:::

**Punto de control:** deberías poder tomar un árbol de cuatro o cinco niveles y valorar sus finales con $U$. Luego, subir con máximos y mínimos de los $Q$ hasta la raíz y decir qué jugada elige MAX. Si te trabas al subir, vuelve a la lista de la sección 7.

---

## Lo que hay que llevarse

- **$V(s)$ se calcula desde los finales hacia la raíz.** Es $U(s)$ en un final, el mayor $Q$ si mueve MAX y el menor si mueve MIN; siempre medido desde MAX.
- **Una jugada vale lo que su hijo:** $Q(s,a)=V(T(s,a))$. En n1, $Q=+1$ con $\text{c1}\textbf{-}\text{c2}$ y $Q=-1$ con $\text{c1}\textbf{x}\text{b2}$.
- **El valor es un número; la jugada sale del $\operatorname{arg\,max}$** (o del $\operatorname{arg\,min}$, si mueve MIN). En n1, $V=+1$ con $\text{c1}\textbf{-}\text{c2}$.
- **El pago sigue siendo $\pm1$.** Preferir ganar rápido es un desempate dentro del $\operatorname{arg\,max}$, no un cambio de $U$.
- **Hexapawn vale $-1$:** con juego perfecto gana Negras, la que juega segundo.

Continúa con [[minimax-como-algoritmo|minimax como algoritmo]].
