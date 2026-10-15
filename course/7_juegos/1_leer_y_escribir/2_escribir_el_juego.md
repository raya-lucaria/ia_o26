---
id: escribir-el-juego
title: Escribir el juego
nav_title: Escribir el juego
summary: "Las siete piezas con las que se escribe cualquier juego de esta clase (dos jugadores, por turnos, determinista, de información perfecta, finito y de suma cero), cada una con su definición, su dominio y su ejemplo en hexapawn, mientras el grafo del juego crece."
status: ready
estimated_time: 40m
tags: [juegos, modelado, grafos]
---

# Escribir el juego

**¿Qué necesita saber una computadora para jugar un juego por turnos?**

Necesita siete datos que fija el reglamento. Al terminar tendrás:

- **Las siete piezas** de cualquier juego de esta clase, cada una con su
  definición, su dominio y su ejemplo en hexapawn.
- **El grafo del juego** dibujado pieza por pieza: nodos, etiquetas, flechas
  y números.
- **Una partida completa** escrita solo con las piezas, sin mirar el
  reglamento.

Usamos hexapawn porque es pequeño, pero ninguna pieza depende de él: las
mismas siete sirven para gato o ajedrez.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

> **Supuestos de esta página.** Definen la **clase de juegos** que escribimos
> aquí. Cada uno tiene nombre para poder revisarlo uno por uno:
>
> - **dos jugadores, por turnos:** mueven uno a la vez;
> - **determinista:** no hay azar;
> - **información perfecta:** cada jugador ve el estado completo y todas las
>   jugadas anteriores;
> - **finito:** cada estado admite un número finito de jugadas y toda
>   partida termina, así que el árbol de partidas tiene un número finito de
>   nodos;
> - **suma cero:** lo que gana uno lo pierde el otro.
>
> En [[diagnosticar-el-juego|Diagnosticar el juego]] se revisa qué cambia
> cuando alguno no se cumple.

> **Notación de conjuntos.** La página la usa toda; si alguna te es nueva,
> aquí está en una línea. También está en la
> [[notacion-juegos|hoja de notación]].
>
> - $x\in X$: $x$ es un elemento de $X$; $x\notin X$: no lo es.
> - $X\subseteq Y$: todo elemento de $X$ está en $Y$.
> - $X\setminus Y$: los elementos de $X$ que no están en $Y$.
> - $X\times Y$: los pares $(x,y)$ con $x\in X$ y $y\in Y$.
> - $\{x,y,z\}$: el conjunto formado por esos elementos.
> - $\{x\in X : P(x)\}$: los elementos de $X$ que cumplen la condición
>   $P$; los dos puntos se leen «tales que».
> - $\mathbb{R}$: los números reales.
> - $f: X\to Y$: una función que a cada elemento de $X$, su **dominio**, le
>   asigna uno de $Y$, su **codominio**.

---

## 1 · Una partida, vuelta por vuelta

**Piensa: cuando te toca jugar, ¿qué tienes que saber antes de mover?**

Tienes que saber si la partida sigue, a quién le toca y qué puedes hacer.
Toda partida repite esa misma vuelta hasta que termina, y la figura la
dibuja. Los símbolos se definen más abajo; por ahora basta con leer las
preguntas.

::: figure {#jue-c1-ciclo title="Una partida, vuelta por vuelta"}
![Diagrama de flujo. Se entra con el estado inicial s0. Primera pregunta: ¿terminó?, es decir, ¿s está en S_F? Si sí, la partida sale con U(s), cuánto vale. Si no: ¿a quién le toca?, Pl(s); ¿qué puede hacer?, A(s); el jugador elige una jugada a, la única caja resaltada; ¿a dónde lleva?, el nuevo estado T(s, a), con el que se da otra vuelta](../_assets/jue-ciclo-partida.svg)
:::

**Cómo leerla:**

- **Se entra arriba**, con el estado inicial $s_0$.
- **Cada vuelta pregunta primero si la partida terminó.** Si terminó, sale
  por la derecha con un número: cuánto vale el resultado.
- **Si no terminó**, pregunta a quién le toca y qué puede hacer. Quien mueve
  elige una jugada, y eso da el estado nuevo para la siguiente vuelta.

**Las siete piezas son las cajas de esta figura.** $S$ es lo que puede
ir en la caja «Estado»; $s_0$, por dónde se entra; $S_F$, $\mathrm{Pl}$, $A$,
$T$ y $U$ contestan las preguntas. El resto de la página define cada una.
Al final de cada sección, un recuadro, «El juego hasta ahora», muestra
las piezas ya escritas para hexapawn; las que faltan llevan «?».

**Una caja es distinta: «Elige una jugada».** Ninguna regla la contesta. Las
reglas dicen qué jugadas hay, no cuál conviene. Decidir esa jugada es el
problema que resuelve el resto de la unidad.

---

## 2 · La idea: el juego es un grafo

**Piensa: mientras juegas, ¿qué cambia de una jugada a la siguiente?**

Cambia la situación. Si dibujamos cada situación como un punto y cada jugada
como una flecha de la situación de antes a la de después, el juego entero se
vuelve un dibujo de puntos y flechas. Ese dibujo es un **grafo**.

::: definition {#jue-c1-grafo title="Grafo dirigido"}
Un **grafo dirigido** es un par $G=(\mathcal{N},E)$:

- $\mathcal{N}$ es un conjunto de **nodos**;
- $E\subseteq \mathcal{N}\times \mathcal{N}$ es un conjunto de **aristas**: pares ordenados
  $(u,v)$ que se dibujan como una flecha de $u$ a $v$.

Si $(u,v)\in E$, decimos que $v$ es **hijo** de $u$ y $u$ es **padre** de $v$.

- **Camino:** una sucesión de nodos donde cada uno es hijo del anterior.
- **Ciclo:** un camino que vuelve a su primer nodo.
- **Hoja:** un nodo sin hijos.
- **Árbol:** un grafo con un nodo distinguido, la **raíz**, que no tiene
  padre. Cada otro nodo tiene exactamente un padre, y todos se alcanzan por
  un camino desde la raíz.

*Ejemplo:* con $\mathcal{N}=\{x,y,z\}$ y $E=\{(x,y),(x,z)\}$, de $x$ salen dos flechas;
$y$ y $z$ son hojas.
:::

En esta página construimos el grafo de hexapawn **pieza por pieza**. Cada
pieza del modelo le agrega algo al dibujo: primero un nodo, luego etiquetas,
luego flechas y al final números.

---

## 3 · Los estados: qué es cada nodo

**Piensa: ¿basta con mirar el tablero para seguir jugando?**

No siempre. **El principio general:** un estado reúne lo suficiente para
contestar las preguntas de [[leer-el-reglamento|la página anterior]] sin
mirar la historia de la partida. Son cómo empieza y qué jugadas hay, quién
mueve, cómo cambia todo con cada jugada, si terminó y cuánto vale.

::: definition {#jue-c1-estado title="Estados y estado inicial"}
- $\mathcal{S}$ es el **universo de situaciones**: todo lo que se puede
  escribir con la descripción del estado, se alcance o no jugando.
- $s_0\in\mathcal{S}$ es el **estado inicial**: la situación antes de la
  primera jugada.
- $S\subseteq\mathcal{S}$ es el **conjunto de estados** del juego: las
  situaciones que se alcanzan desde $s_0$ aplicando las reglas. Lo
  calcularemos al final de la página.

**Las reglas que siguen, en una línea cada una.** Cada una tiene más abajo
su sección, con su definición, su dominio, su codominio y un ejemplo:

- $S_F$: los estados donde la partida ya terminó;
- $\mathrm{Pl}(s)$: quién mueve en $s$;
- $A(s)$: las jugadas permitidas en $s$;
- $T(s,a)$: el estado al que se llega al hacer la jugada $a$ en $s$;
- $U(s)$: cuánto vale el resultado en un estado $s$ donde la partida terminó.

**Primero sobre $\mathcal{S}$, luego sobre $S$.** Las cuatro primeras reglas
se pueden aplicar a cualquier situación bien escrita de $\mathcal{S}$. $S$ es
lo que se alcanza desde $s_0$ aplicándolas una y otra vez. Ya con $S$, cada
pieza se restringe a sus estados: así aparecen en las definiciones de abajo.
$U$ no hace falta para encontrar $S$: solo le pone un número a cada final.

**Qué significa:** cada estado será un nodo del grafo, y $s_0$ será el nodo
de donde parte todo.

**Qué no es:** un estado no es una partida ni una lista de jugadas. Es una
foto del momento con todo lo que hace falta para seguir.
:::

**En hexapawn.** Un estado tiene dos partes.

1. **El tablero.** Llamemos $C=\{a1,b1,c1,a2,b2,c2,a3,b3,c3\}$ a las nueve
   casillas: la letra es la columna y el número, la fila. En cada casilla
   puede haber una de tres cosas, y cada una tiene su símbolo:

   - $B$: un peón **blanco**;
   - $N$: un peón **negro**;
   - $\cdot$: nada, la casilla está **vacía**.

   Un tablero es una función $\tau: C\to\{B,N,\cdot\}$: a cada casilla le
   asigna lo que hay en ella. Por ejemplo, al empezar, $\tau(a1)=B$, $\tau(a3)=N$
   y $\tau(a2)=\cdot$.
2. **El turno:** $B$ si mueve Blancas y $N$ si mueve Negras. Es un elemento
   de $\{B,N\}$, guardado en el estado junto al tablero.

Un estado es el par $s=(\tau,\ \text{turno})$. El universo $\mathcal{S}$ son
todos los pares que se pueden escribir así: cualquier tablero con cualquier
turno. Como cada una de las 9 casillas tiene 3 opciones, hay $3^9$ tableros
($3$ multiplicado por sí mismo 9 veces), y con 2 turnos, $2\times 3^9$
pares. El inicial es:

$$s_0=(\tau_0,\ B),$$

donde $\tau_0$ es el tablero inicial:

$$\tau_0(x)=\begin{cases}B & \text{si } x\in\{a1,b1,c1\},\\
N & \text{si } x\in\{a3,b3,c3\},\\ \cdot & \text{en las demás}.\end{cases}$$

**Estado, tablero y posición.** El tablero es solo $\tau$, sin turno; el
estado es el par completo. En ajedrez al estado se le dice **posición**, y
aquí las dos palabras significan lo mismo.

**Por qué guardamos el turno.** En general el tablero solo no basta: en
ajedrez el mismo tablero puede tocarle a cualquiera de los dos, y quien
mueve cambia qué jugadas hay. En el hexapawn de 3×3 resulta que el turno sí
se podría deducir del tablero, pero eso solo se sabe después de generar
todos los estados. El principio general es guardarlo.

> **Palabras de ajedrez que usamos.** No hace falta saber jugarlo.
>
> - **Jaque:** el rey está atacado.
> - **Mate:** jaque sin jugada que lo evite; pierde quien lo sufre.
> - **Ahogado:** quien mueve no tiene jugada y su rey no está en jaque; es
>   empate.
> - **Tablas:** empate.
> - **Enroque y captura al paso:** dos jugadas especiales que solo se
>   permiten según lo que pasó antes en la partida.

**El mismo principio, en ajedrez.** Además del tablero y el turno, un estado
de ajedrez guarda tres cosas que no se ven en el tablero:

- **Para las jugadas especiales:** si cada rey y cada torre ya se movieron
  (enroque) y si se puede capturar al paso.
- **Para la regla de las 50 jugadas:** cuántas jugadas de cada jugador van
  sin captura ni movimiento de peón; cualquiera de las dos reinicia la cuenta.
- **Para las tablas por repetición:** qué posiciones ya ocurrieron y cuántas
  veces. Se comparan tablero, turno, enroques y captura al paso, no los
  contadores.

Nada de eso se ve en el tablero, pero decide qué jugadas hay o cómo termina.

> **El juego hasta ahora · 2 de 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | ? |
> | $\mathrm{Pl}$ | ? |
> | $A$ | ? |
> | $T$ | ? |
> | $U$ | ? |

---

## 4 · Los finales: dónde se acaba el grafo

**Piensa: ¿en qué estados ya no mueve nadie?**

En los que terminan la partida. Ahí lo único que importa es el resultado.

::: definition {#jue-c1-finales title="Estados finales"}
$S_F\subseteq S$ es el **conjunto de estados finales**: aquellos en los que
la partida ya terminó.

**Qué significa:** en el grafo, los finales serán **hojas**: nunca sale una
flecha de un final. Al revés no siempre: en un dibujo a medias, una hoja
puede ser un estado que todavía no se expande.

**Qué no es:** un final no es un estado perdido. Un estado está **perdido**
para un jugador si el rival puede asegurarle la derrota, haga lo que haga.
Puede estarlo sin haber terminado, y el perdedor todavía tiene que mover.
:::

**Una regla general.** Todo estado donde quien mueve no tenga ninguna jugada
permitida tiene que estar en $S_F$: el reglamento debe decir qué pasa ahí.
En ajedrez son el mate y el ahogado. Por eso, en un estado que no es final,
siempre hay al menos una jugada.

**Pasar también es una jugada.** Si un reglamento permite pasar, pasar es
una jugada legal: el estado no es final y esa jugada está entre las
permitidas.

**En hexapawn.** Un estado $s=(\tau,\text{turno})$ es final si se cumple
cualquiera de estas tres condiciones:

1. hay un peón blanco en la fila 3 o uno negro en la fila 1;
2. a uno de los dos ya no le quedan peones;
3. a quien mueve no le queda ninguna jugada según cómo se mueven los
   peones: no puede avanzar ni capturar con ninguno.

> **El juego hasta ahora · 3 de 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | Un peón llegó a la fila rival, un lado se quedó sin peones o quien mueve no tiene jugada |
> | $\mathrm{Pl}$ | ? |
> | $A$ | ? |
> | $T$ | ? |
> | $U$ | ? |

---

## 5 · Quién mueve: la etiqueta de cada nodo

**Piensa: en un estado que no es final, ¿quién decide la siguiente jugada?**

Lo dice el propio estado: el turno viene guardado en él.

::: definition {#jue-c1-pl title="Quién mueve"}
$\mathrm{Pl}: S\setminus S_F\to\{\text{MAX},\text{MIN}\}$ dice, en cada estado
no final, **quién mueve** ahí (Pl, de *player*).

**Dominio:** solo los estados no finales; en un final nadie mueve.
**Codominio:** los dos jugadores. MAX es el jugador desde cuyo lado
mediremos el resultado (sección 8): busca que sea alto. Como el juego es de
suma cero, MIN busca que sea bajo.

**Cómo se calcula:** no se calcula. **Quién mueve es parte del estado**, y
$\mathrm{Pl}(s)$ solo lee el turno guardado en $s$.

**Qué no es:** la etiqueta no dice quién va ganando; solo quién elige la
siguiente jugada.

**Qué significa:** en el grafo, cada nodo que no es final lleva la etiqueta
MAX o MIN, aunque todavía no se haya expandido. «Nodo de MAX», «mueve MAX» y «$\mathrm{Pl}(s)=\text{MAX}$» dicen
lo mismo.
:::

**En hexapawn.** Blancas es MAX y Negras es MIN. $\mathrm{Pl}(s)$ lee el
**turno guardado en el estado** (sección 3):

$$
\mathrm{Pl}(\tau,\ \text{turno})=
\begin{cases}
\text{MAX} & \text{si turno} = B,\\
\text{MIN} & \text{si turno} = N.
\end{cases}
$$

Por ejemplo, en $s_0$ el turno es $B$, así que $\mathrm{Pl}(s_0)=\text{MAX}$.

**La alternancia es de hexapawn, no del modelo.** Si un reglamento da un
turno extra, la jugada deja el mismo turno guardado, y $\mathrm{Pl}$ del
estado nuevo lo dice. **Si hubiera dados**, la tirada sería otro valor de
$\mathrm{Pl}$, AZAR; con los supuestos de esta página no aparece.

Con esto ya podemos dibujar el primer nodo del grafo.

::: figure {#jue-c1-paso-1 title="Paso 1: un nodo, el estado inicial"}
![El estado inicial s0 en grande, con tres anotaciones: el nombre del nodo, el tablero con tres peones blancos en la fila 1 y tres negros en la fila 3, y el turno de Blancas, que hace que Pl(s0) sea MAX. El borde es punteado porque todavía no se calculan sus jugadas](../_assets/jue-grafo-paso-1.svg)
:::

Cada parte del nodo es una pieza del modelo: el tablero y el turno forman
el estado, y el turno da $\mathrm{Pl}(s_0)$. El borde está punteado porque
todavía no sabemos qué sale de él. Para eso hacen falta las dos piezas
siguientes.

> **El juego hasta ahora · 4 de 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | Un peón llegó a la fila rival, un lado se quedó sin peones o quien mueve no tiene jugada |
> | $\mathrm{Pl}$ | Turno de Blancas: MAX. Turno de Negras: MIN |
> | $A$ | ? |
> | $T$ | ? |
> | $U$ | ? |

---

## 6 · Las acciones: cuántas flechas salen

**Piensa: al empezar, ¿cuántas jugadas tiene Blancas?**

Tres: cada peón puede avanzar y ninguno puede capturar.

::: definition {#jue-c1-acciones title="Acciones permitidas"}
Llamemos $\mathcal{A}$ al conjunto de todas las jugadas que se pueden
escribir en el juego, y $a$ a una jugada cualquiera. Para cada estado no
final $s$, $A(s)\subseteq\mathcal{A}$ es el conjunto de **jugadas
permitidas** en $s$, y nunca está vacío.

**Dominio:** los estados no finales, $S\setminus S_F$. **Codominio:** los
subconjuntos no vacíos de $\mathcal{A}$.

**Qué significa:** en el grafo, de cada nodo no final sale **una flecha por
cada jugada** de $A(s)$, rotulada con su jugada. Si dos jugadas llevaran al
mismo estado, serían dos flechas distintas.

**Qué no es:** $A(s)$ no dice qué jugada conviene. Solo dice cuáles respetan
las reglas.
:::

**En hexapawn.** Una jugada se escribe en tres partes:
**casilla de salida + símbolo + casilla de llegada**. El símbolo dice qué
hace el peón:

| Símbolo | Qué hace el peón | Ejemplo |
|:---:|---|:---:|
| **-** (guion) | **Avanza** a la casilla de enfrente, que está vacía | $\text{b1}\textbf{-}\text{b2}$ |
| **x** | **Captura** el peón rival de una diagonal de enfrente | $\text{c1}\textbf{x}\text{b2}$ |

**Al empezar, ningún peón puede capturar:** los peones negros están en la
fila 3, y la diagonal de enfrente de un peón blanco está en la fila 2. Por
eso las tres jugadas iniciales son avances:

$$A(s_0)=\{\text{a1-a2},\ \text{b1-b2},\ \text{c1-c2}\}.$$

¿Y si a un jugador no le queda ninguna jugada? Por la regla general de la
sección 4, ese estado es final, así que nunca hace falta un $A(s)$ vacío.

> **El juego hasta ahora · 5 de 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | Un peón llegó a la fila rival, un lado se quedó sin peones o quien mueve no tiene jugada |
> | $\mathrm{Pl}$ | Turno de Blancas: MAX. Turno de Negras: MIN |
> | $A$ | Avanzar a la casilla vacía de enfrente o capturar en diagonal hacia delante |
> | $T$ | ? |
> | $U$ | ? |

---

## 7 · La transición: a dónde llega cada flecha

**Piensa: si sabes el estado y la jugada, ¿sabes a dónde llegas?**

Sí. Las reglas dicen exactamente qué pasa al hacer cada jugada.

::: definition {#jue-c1-transicion title="Función de transición"}
$T(s,a)$ es el estado al que se llega al hacer la jugada $a$ en el estado
$s$:

$$T:\ \{(s,a)\ :\ s\in S\setminus S_F,\ a\in A(s)\}\ \to\ S.$$

**Dominio:** los pares de un estado no final y una de sus jugadas.
**Codominio:** los estados.

**Qué significa:** en el grafo, la flecha de la jugada $a$ va de $s$ a
$T(s,a)$ y lleva escrita la jugada $a$.

**Que sea una función** quiere decir que $T$ es **determinista dado $a$**:
la misma jugada desde el mismo estado lleva **siempre** al mismo estado. Si
un juego tuviera azar, el azar estaría en qué $a$ ocurre, no en $T$.
:::

**En hexapawn.** $T(s,a)$ mueve el peón, quita el peón capturado si lo hay y
cambia el turno. Por ejemplo, $T(s_0,\text{b1-b2})$ es:

::: table {#jue-c1-tras-b2 title="El estado T(s₀, b1-b2): mueven Negras"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | N | N |
| **2** | · | B | · |
| **1** | B | · | B |
:::

Con $A$ y $T$, el nodo inicial se **expande**: le salen sus flechas y
aparecen sus hijos. **Expandir** un nodo es calcular $A(s)$ y, para cada
jugada, $T(s,a)$.

::: figure {#jue-c1-paso-2 title="Paso 2: expandir s₀, una flecha por jugada"}
![El nodo s0 arriba con tres flechas, a1-a2, b1-b2 y c1-c2, que llegan a tres estados nuevos rotulados T(s0, a1-a2), T(s0, b1-b2) y T(s0, c1-c2); en los tres mueve Negras (MIN) y todavía no se expanden](../_assets/jue-grafo-paso-2.svg)
:::

Cada hijo es $T(s_0,a)$ para una jugada $a$, y en los tres mueve **MIN**:
$T$ guardó el turno de Negras. Ahora expandimos uno de ellos, el que sale de
a1-a2. Para no llenar la figura, desde aquí cada paso muestra solo el nodo
que se expande y sus hijos, con el camino que lleva a él.

::: figure {#jue-c1-paso-3 title="Paso 3: expandir un nodo de MIN"}
![El estado tras a1-a2, donde mueve Negras, arriba; tres flechas de Negras, b3-b2, b3xa2 y c3-c2, llevan a tres estados donde vuelve a mover Blancas. El primero, tras b3-b2, se llama n1](../_assets/jue-grafo-paso-3.svg)
:::

Las mismas dos funciones sirven para los nodos de Negras: $A$ da sus jugadas
y $T$ las aplica. En las figuras, «tras a1-a2» abrevia $T(s_0,\text{a1-a2})$,
el estado al que se llega con esa jugada. Al estado tras a1-a2 y b3-b2 lo
llamaremos **n1**; lo usaremos toda la unidad.

::: exercise {#jue-c1-ej-acciones title="Decide qué jugadas hay en n1"}
Este es n1. Mueven Blancas.

| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | N |
| **2** | B | N | · |
| **1** | · | B | B |

1. Escribe $A(\text{n1})$.
2. Escribe $T(\text{n1},\text{c1-c2})$. ¿Es final? ¿Por qué condición?
:::

::: hint {#jue-c1-pista-acciones of="jue-c1-ej-acciones" title="Peón por peón"}
Revisa cada peón blanco: ¿la casilla de enfrente está vacía? ¿Hay un peón
negro en alguna diagonal de enfrente?
:::

::: answer {#jue-c1-resp-acciones of="jue-c1-ej-acciones"}
1. $A(\text{n1})=\{\text{c1-c2},\ \text{c1xb2}\}$. El peón de a2 no puede
   avanzar porque a3 está ocupada, y no tiene a quién capturar en b3. El de b1
   tiene b2 ocupada enfrente y nada que capturar en a2 ni en c2.
2. $T(\text{n1},\text{c1-c2})$, con turno de Negras:

   | | a | b | c |
   |---|:---:|:---:|:---:|
   | **3** | N | · | N |
   | **2** | B | N | B |
   | **1** | · | B | · |

   Es **final por la condición 3**: Negras no tiene jugada. a3 y c3 tienen
   enfrente un peón blanco y en diagonal un peón propio; b2 tiene enfrente a
   b1 y nada que capturar. Gana Blancas.
:::

> **El juego hasta ahora · 6 de 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | Un peón llegó a la fila rival, un lado se quedó sin peones o quien mueve no tiene jugada |
> | $\mathrm{Pl}$ | Turno de Blancas: MAX. Turno de Negras: MIN |
> | $A$ | Avanzar a la casilla vacía de enfrente o capturar en diagonal hacia delante |
> | $T$ | Mover el peón, quitar el capturado si lo hay y cambiar el turno |
> | $U$ | ? |

---

## 8 · La utilidad: el número de cada final

**Piensa: cuando la partida termina, ¿qué número debería recibir la
computadora para saber si le fue bien?**

El que dice el reglamento, medido siempre desde el mismo lado: el de MAX.

::: definition {#jue-c1-utilidad title="Utilidad"}
$U: S_F\to\mathbb{R}$ asigna a cada estado final un número, su **utilidad**
o **pago**: **lo que vale ese resultado para MAX**.

**Dominio:** solo los finales; un estado a medio juego no tiene utilidad.
**Codominio:** los números reales.

**Qué significa:** en el grafo, cada final lleva escrito su $U$. No cambia
con quién movió último: $+1$ siempre favorece a MAX.

**Por qué basta un número:** como el juego es de suma cero, para MIN ese
final vale $-U(s)$. Si fuera de suma constante, basta restar la mitad de esa
constante a cada pago para que sume cero.
:::

**Aviso: un número no siempre basta.** Con más de dos jugadores, o si lo
que gana uno no es lo que pierde el otro, cada final necesita un número por
jugador: un vector $(U_1,\dots,U_n)$. Queda fuera de esta clase de juegos.

### Qué número poner en un final

La utilidad **copia lo que el reglamento dice que vale el resultado**. No le
agregamos preferencias que el reglamento no tiene. Según el juego, hay varias
opciones:

| Opción | Qué mide | Cuándo se usa |
|---|---|---|
| $+1$ ganar, $0$ empatar, $-1$ perder | Solo el resultado | Cualquier juego que termina en ganar, empatar o perder: ajedrez, gato, hexapawn |
| Los puntos del reglamento | El marcador final | Juegos que cuentan puntos, como el Go o el backgammon |
| Premiar ganar rápido | El resultado y lo que tardó | Tentador, pero exige saber cuánto puede durar una partida y mezcla una preferencia nuestra con el resultado |

**Cambiar la escala está permitido; cambiar el orden, no.** En un torneo de
ajedrez se dan 1, ½ y 0 puntos. Si a cada número le restas ½ y lo
multiplicas por 2, quedan $+1$, $0$ y $-1$: el orden entre resultados es el
mismo, así que convienen las mismas jugadas, y ahora lo que gana uno lo
pierde el otro.

La tercera opción no es parte del juego. Cuando un programa de ajedrez
prefiere el mate más corto, lo usa para **desempatar** entre jugadas que
ganan las dos; no cambia la utilidad.

**En hexapawn** el reglamento solo dice quién gana, así que usamos la
primera opción. No hay empates, porque quedarse sin jugada es derrota.

Para que $U$ sea una función del estado, quién ganó se tiene que poder leer
de $s=(\tau,\text{turno})$:

- **ganó Blancas** si hay un B en la fila 3, si no quedan N, o si el turno es
  de Negras y Negras no tiene jugada;
- **ganó Negras** en los tres casos simétricos.

Cuando quien mueve no puede mover, gana **el otro**. Entonces:

$$U(s)=\begin{cases}+1 & \text{si en } s \text{ ganó Blancas},\\
-1 & \text{si en } s \text{ ganó Negras}.\end{cases}$$

Con la utilidad, el primer final del grafo recibe su número.

::: figure {#jue-c1-paso-4 title="Paso 4: llegar a un final y escribir su U"}
![El nodo n1, al que se llega por a1-a2 y b3-b2, arriba; dos flechas, c1-c2 y c1xb2. El hijo n2 es final, con borde doble: Negras no tiene jugada, gana Blancas y U = +1. El hijo n3, donde mueve Negras, queda punteado porque todavía no se expande](../_assets/jue-grafo-paso-4.svg)
:::

El hijo n2 es final y recibe $U=+1$. El hijo n3 no es final: su borde
punteado solo dice que todavía no se expande.

> **El juego hasta ahora · las 7 piezas**
>
> | Pieza | En hexapawn |
> |---|---|
> | $S$ | Pares (tablero, turno) que se alcanzan desde $s_0$ |
> | $s_0$ | B en a1, b1 y c1; N en a3, b3 y c3; mueve Blancas |
> | $S_F$ | Un peón llegó a la fila rival, un lado se quedó sin peones o quien mueve no tiene jugada |
> | $\mathrm{Pl}$ | Turno de Blancas: MAX. Turno de Negras: MIN |
> | $A$ | Avanzar a la casilla vacía de enfrente o capturar en diagonal hacia delante |
> | $T$ | Mover el peón, quitar el capturado si lo hay y cambiar el turno |
> | $U$ | $+1$ si gana Blancas; $-1$ si gana Negras |

---

## 9 · Reunir el juego

Las siete piezas juntas son el **modelo** del juego. Un aviso de palabras:

- **Jugada y acción** son lo mismo.
- **Estado y posición** también: «posición» es como se dice en ajedrez.
- **El turno** ($B$ o $N$) es el dato guardado en el estado; $\mathrm{Pl}$
  lo lee y dice MAX o MIN.

Todas las piezas son **datos**: las fija el reglamento, no el jugador.

::: definition {#jue-c1-juego title="Juego por turnos"}
Un **juego de esta clase** (dos jugadores, por turnos, determinista, de
información perfecta, finito y de suma cero) es la **tupla**, es decir, la
lista ordenada de piezas,

$$\bigl(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\ T,\ U\bigr).$$

Quien mueve elige $a\in A(s)$. Todo lo demás lo deciden las reglas: a dónde
lleva la jugada, cuándo termina y cuánto vale.
:::

::: table {#jue-c1-piezas title="Las siete piezas, en general"}
| Pieza | De dónde a dónde | Qué significa |
|---|---|---|
| $S$ | Subconjunto de $\mathcal{S}$ | Las situaciones alcanzables |
| $s_0$ | Elemento de $S$ | Cómo empieza |
| $S_F$ | Subconjunto de $S$ | Dónde termina |
| $\mathrm{Pl}$ | $S\setminus S_F\to\{\text{MAX},\text{MIN}\}$ | Quién mueve |
| $A$ | $S\setminus S_F\to$ conjuntos no vacíos de jugadas | Qué se puede hacer |
| $T$ | $\{(s,a): s\in S\setminus S_F,\ a\in A(s)\}\to S$ | Qué pasa al hacerlo |
| $U$ | $S_F\to\mathbb{R}$ | Cuánto vale para MAX |
:::

::: table {#jue-c1-piezas-ejemplos title="Las siete piezas, en hexapawn y en ajedrez"}
| Pieza | En hexapawn | En ajedrez |
|---|---|---|
| $S$ | Pares (tablero, turno) | Tablero, turno, enroques, al paso, contador de jugadas, posiciones ya vistas |
| $s_0$ | Tres peones por lado, mueve Blancas | La posición inicial, mueven blancas |
| $S_F$ | Llegar, capturar todo o dejar sin jugada | Mate, ahogado, material insuficiente, quíntuple repetición, 75 jugadas |
| $\mathrm{Pl}$ | El turno guardado | El turno guardado |
| $A$ | Avanzar o capturar | Jugadas legales, sin dejar el rey en jaque |
| $T$ | Mover, capturar y cambiar el turno | Mover y actualizar enroques, al paso, contador e historial |
| $U$ | $+1$ o $-1$ | $+1$, $0$ o $-1$ |
:::

**Una simplificación en la tabla.** La triple repetición y las 50 jugadas
no terminan la partida solas: dan a un jugador el derecho de **reclamar**
tablas. Las que terminan sin reclamo son la quíntuple repetición y las 75
jugadas (Leyes del Ajedrez de la FIDE, artículo 9). Para modelar el
reclamo, reclamar tablas sería una jugada más.

**Cuántos estados hay.** Ya con $A$ y $T$ podemos generar $S$: partir de
$s_0$ y aplicar todas las jugadas posibles hasta que no aparezcan estados
nuevos. En hexapawn, de los $3^9\cdot 2$ pares del universo, solo **135** se
alcanzan. En ajedrez nadie puede hacer esa cuenta: hay del orden de $10^{44}$
posiciones legales, y eso sin contar los contadores ni el historial.

---

## 10 · Una partida completa, escrita con las piezas

**Piensa: con las siete piezas, ¿puedes jugar una partida sin mirar el
reglamento?**

Sí. Cada vuelta de la figura del ciclo, en la sección 1, es un renglón:
¿está en $S_F$?, $\mathrm{Pl}$, $A$, una jugada elegida y $T$. Llamemos
$s_1, s_2, \dots$ a los estados de esta partida, en orden.

Primero, los cinco estados. En cada celda van las casillas a, b y c de esa
fila del tablero.

| Estado | Fila 3 | Fila 2 | Fila 1 | Turno |
|---|:---:|:---:|:---:|:---:|
| $s_0$ | N N N | · · · | B B B | B |
| $s_1$ | N N N | B · · | · B B | N |
| $s_2$ | N · N | N · · | · B B | B |
| $s_3$ | N · N | N B · | · · B | N |
| $s_4$ | N · N | · B · | N · B | B |

Ahora, la partida, vuelta por vuelta:

1. **$s_0$**: no está en $S_F$; $\mathrm{Pl}(s_0)=\text{MAX}$;
   $A(s_0)=\{\text{a1-a2},\ \text{b1-b2},\ \text{c1-c2}\}$.
   **Se elige a1-a2**, y $T$ lleva a $s_1$.
2. **$s_1$**: no está en $S_F$; $\mathrm{Pl}(s_1)=\text{MIN}$;
   $A(s_1)=\{\text{b3-b2},\ \text{b3xa2},\ \text{c3-c2}\}$.
   **Se elige b3xa2**, y $T$ lleva a $s_2$.
3. **$s_2$**: no está en $S_F$; $\mathrm{Pl}(s_2)=\text{MAX}$;
   $A(s_2)=\{\text{b1-b2},\ \text{b1xa2},\ \text{c1-c2}\}$.
   **Se elige b1-b2**, y $T$ lleva a $s_3$.
4. **$s_3$**: no está en $S_F$; $\mathrm{Pl}(s_3)=\text{MIN}$;
   $A(s_3)=\{\text{a2-a1},\ \text{a3xb2},\ \text{c3-c2},\ \text{c3xb2}\}$.
   **Se elige a2-a1**, y $T$ lleva a $s_4$.
5. **$s_4$**: **sí** está en $S_F$. La partida terminó.

$s_4$ es final por la condición 1: hay un peón negro en la fila 1. Ganó
Negras, así que

$$U(s_4)=-1.$$

**Fíjate en lo que «se elige» en cada vuelta.** Es lo único que no salió de
las piezas: lo demás lo calcula cualquiera con las reglas. Esas jugadas las
escogimos nosotros, sin ningún criterio.

**Punto de control:** deberías poder escribir las siete piezas de un juego
de esta clase, con su dominio, y trazar una partida vuelta por vuelta con
ellas.

---

## Lo que hay que llevarse

- **Siete piezas escriben el juego:** $S$, $s_0$, $S_F$, $\mathrm{Pl}$, $A$,
  $T$ y $U$. Cada una tiene dominio y significado, y sirve para cualquier
  juego de esta clase.
- **Cada pieza dibuja algo del grafo:** los estados son los nodos,
  $\mathrm{Pl}$ los etiqueta, $A$ y $T$ trazan las flechas y $U$ pone
  números en los finales.
- **Quién mueve es parte del estado:** $s=(\tau,\text{turno})$ y
  $\mathrm{Pl}(s)$ solo lee el turno.
- **La utilidad copia el reglamento y se mide desde MAX.** En hexapawn,
  $+1$ o $-1$; cambiar la escala está permitido, cambiar el orden no.
- **Una partida es una vuelta que se repite:** ¿terminó?, ¿a quién le toca?,
  ¿qué puede hacer?, elegir y ¿a dónde lleva? Las reglas contestan todo
  menos elegir.

Continúa con [[el-juego-como-grafo|el juego como grafo]].
