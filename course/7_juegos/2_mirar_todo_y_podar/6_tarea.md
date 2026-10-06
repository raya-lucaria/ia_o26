---
id: tarea-mirar-todo-y-podar
title: "Tarea de refuerzo · Calcular y podar"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: escribir y resolver monedas en fila con minimax y alfa-beta, y resolver n1 en el hexapawn donde quedarse sin jugada es empate."
status: ready
estimated_time: 45m
tags: [juegos, minimax, alfa-beta, practica]
---

# Tarea de refuerzo · Calcular y podar

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin
ayuda** lo de la clase: escribir un juego, calcular su valor y su jugada,
y podar con alfa-beta.

El primer ejercicio es un juego nuevo. El segundo cambia una sola regla de
hexapawn, la misma que cambiaste en la
[[tarea-leer-y-escribir|tarea de la clase 1]].

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

## 1 · Resolver monedas en fila

> **Monedas en fila.** Hay cuatro monedas en fila, de $2$, $1$, $5$ y $3$
> pesos, de izquierda a derecha. Dos jugadores se turnan, y en cada turno el
> de turno toma **una moneda de un extremo**: la de la izquierda o la de la
> derecha. Cuando no quedan monedas, cada quien se queda con lo que tomó. El
> marcador de la partida es la **diferencia**: lo que sumas menos lo que
> suma el rival.

Quien empieza es MAX.

::: exercise {#jue-tarea-2-ej-monedas title="Escribe y resuelve monedas en fila"}
1. Escribe las siete piezas: qué guarda un estado ($S$), $s_0$, $S_F$,
   $\mathrm{Pl}$, $A$, $T$ y $U$.
2. Escribe el problema: qué es lo **dado** y qué hay que **encontrar**.
3. ¿Cuántos nodos tiene el árbol completo y cuántos son finales?
4. Calcula con minimax el valor de la raíz. ¿Qué moneda debe tomar MAX
   primero? ¿Con cuántos pesos termina cada jugador?
5. La regla codiciosa dice «toma siempre la moneda mayor». Si MAX la sigue
   en todos sus turnos y el rival juega perfecto, ¿cómo termina?
6. ¿Cuántas situaciones distintas hay si solo importa qué monedas quedan?
   ¿Por qué basta con eso para reutilizar valores?
7. Si recorres el árbol con alfa-beta, ¿esperas ahorrar mucho? Explica qué
   decide el ahorro.
8. Di un límite del valor que calculaste: algo que no dice.
:::

::: hint {#jue-tarea-2-pista-monedas-a of="jue-tarea-2-ej-monedas" title="Pista 1 · Qué guarda el estado"}
Las monedas que quedan siempre forman un tramo seguido de la fila original:
basta con dos índices, el primero y el último que quedan. Pero la utilidad
depende también de quién tomó qué. ¿Qué número tienes que llevar para
escribir $U$ al final sin mirar la historia?
:::

::: hint {#jue-tarea-2-pista-monedas-b of="jue-tarea-2-ej-monedas" title="Pista 2 · Empieza por los tramos cortos"}
Para cada tramo que quede, calcula la diferencia que puede asegurar **quien
mueve** desde ahí. Con una moneda, la toma. Con dos, ¿cuál toma? Con tres,
prueba los dos extremos y usa los tramos de dos que ya calculaste.
:::

::: answer {#jue-tarea-2-resp-monedas of="jue-tarea-2-ej-monedas" title="Respuesta · Monedas en fila"}
**1. Las siete piezas.** Un estado guarda el tramo que queda, de la moneda
$i$ a la $j$; el turno; y $\Delta$, los pesos de MAX menos los del rival
hasta ahora. $U$ necesita $\Delta$, y $\Delta$ no se ve en las monedas que
quedan: por eso va en el estado.

| Pieza | En monedas en fila |
|---|---|
| $S$ | Las cuádruplas (primera moneda, última moneda, turno, $\Delta$) que se alcanzan desde $s_0$ |
| $s_0$ | Las cuatro monedas, mueve MAX, $\Delta=0$ |
| $S_F$ | Los estados sin monedas |
| $\mathrm{Pl}$ | Se lee del turno guardado: MAX o MIN |
| $A$ | $\{$izquierda, derecha$\}$; con una sola moneda, solo tomarla |
| $T$ | Quita la moneda de ese extremo, la suma a $\Delta$ si movió MAX o la resta si movió MIN, y cambia el turno |
| $U$ | $\Delta$, el marcador final en pesos de MAX |

$U$ no es $\pm1$: aquí el reglamento **sí cuenta puntos**, y la utilidad
copia el marcador. Es la segunda opción de la tabla de
[[escribir-el-juego|Escribir el juego]].

**2. El problema.** **Dado:** las siete piezas. **Encontrar:** en cada
estado donde mueve MAX, la moneda que le asegura la mayor diferencia si MIN
responde lo mejor que puede.

**3. El árbol.** Toda partida dura 4 jugadas. Con dos o más monedas hay dos
hijos; con una, uno solo. Por niveles, $1+2+4+8+8=$ **23 nodos**, de los
cuales **8 son finales**.

**4. Minimax.** Para cada tramo, $W$ es la diferencia que asegura **quien
mueve** con las monedas que quedan: lo que tomas cuenta a tu favor, y lo que
el rival asegura después, en contra. $W(\text{tramo})$ es el mayor de dos
números:

- tomar la izquierda: $\text{izquierda}-W(\text{lo que queda})$;
- tomar la derecha: $\text{derecha}-W(\text{lo que queda})$.

| Tramo | Cuenta | $W$ |
|---|---|---:|
| $(2)$, $(1)$, $(5)$, $(3)$ | Se toma la única moneda | 2, 1, 5, 3 |
| $(2,1)$ | $\max\{2-1,\ 1-2\}$ | 1 |
| $(1,5)$ | $\max\{1-5,\ 5-1\}$ | 4 |
| $(5,3)$ | $\max\{5-3,\ 3-5\}$ | 2 |
| $(2,1,5)$ | $\max\{2-4,\ 5-1\}$ | 4 |
| $(1,5,3)$ | $\max\{1-2,\ 3-4\}$ | −1 |
| $(2,1,5,3)$ | $\max\{2-(-1),\ 3-4\}$ | **3** |

El valor de la raíz es **$+3$** y la jugada es **tomar el 2**, la moneda
menor. Tras el 2, al rival le queda $(1,5,3)$, y tome lo que tome, MAX
toma después el 5. MAX termina con **7** pesos y el rival con **4**.

**5. La trampa codiciosa.** Tomar el 3 deja $(2,1,5)$ al rival, que toma el
5. Después MAX toma el 2 y el rival el 1: MAX suma **5**, el rival **6**, y
la diferencia es **$-1$**. Tomar la mayor le regaló al rival la moneda de 5.

**6. El grafo.** Lo que se puede conseguir **desde aquí** solo depende del
tramo que queda; $\Delta$ se suma al final y no cambia qué conviene. Hay
$4+3+2+1=10$ tramos con monedas más el vacío: **11 situaciones**, contra 23
nodos. La tabla del inciso 4 es justo minimax sobre ese grafo.

**7. Alfa-beta.** En el árbol de 23 nodos, alfa-beta genera los **23** si
revisa primero la izquierda y **21** si revisa primero la derecha. Ahorra
poco: el árbol es chico, cada nodo tiene a lo más dos hijos y los valores de
los hermanos están cerca. Alfa-beta nunca genera más que minimax, pero **no
siempre ahorra mucho**: lo deciden el orden y la forma del árbol.

**8. Límite.** El $+3$ supone que el rival juega perfecto: es lo que MAX
**asegura**, no lo que obtendrá contra un rival que se equivoca, que puede
ser más.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Tu estado permite escribir $U$ al final sin mirar la historia.
- Escribiste el problema con «dado» y «encontrar».
- Valoraste los tramos cortos antes que los largos.
- Distinguiste el valor ($+3$) de la jugada (tomar el 2).
- Comparaste la regla codiciosa contra un rival que juega perfecto, no
  contra uno que también es codicioso.

## 2 · Resolver n1 cuando quedarse sin jugada es empate

Volvemos a la regla de la [[tarea-leer-y-escribir|tarea de la clase 1]]:
todo sigue igual, salvo que quien no tiene jugada **empata**, y empatar
vale 0.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival o captura todos los peones rivales; ganar vale
> $+1$ y perder, $-1$.
>
> **Lo que cambia en este ejercicio:** si al jugador de turno no le queda
> jugada, la partida termina en **empate**, que vale 0.

Usa el subgrafo de n1 de [[minimax|Minimax a mano]], con la misma
numeración y el mismo orden de jugadas.

::: exercise {#jue-tarea-2-ej-empate title="Resuelve n1 con la regla del empate"}
1. ¿Qué finales del subgrafo de n1 cambian de $U$, y a cuánto?
2. Valora el subgrafo con minimax. ¿Cuánto valen n3 y n1? ¿Qué jugadas
   alcanzan el valor de n1?
3. Recorre n1 con alfa-beta y el orden fijo. ¿Cuántos estados se generan?
   ¿Dónde se corta, y de qué tipo es cada corte?
4. Repite con el orden invertido.
5. Con el orden fijo, en el juego original se generaban 5 estados. ¿Por qué
   ahora se generan más?
6. Las dos jugadas de n1 valen lo mismo. Si Negras pudiera equivocarse,
   ¿cuál jugarías? Justifícalo.
:::

::: hint {#jue-tarea-2-pista-empate-a of="jue-tarea-2-ej-empate" title="Pista 1 · Qué finales cambian"}
Solo cambian los finales donde alguien se quedó **sin jugada**. En el
subgrafo de n1 hay dos: uno lo gana Blancas y otro Negras con la regla
original.
:::

::: hint {#jue-tarea-2-pista-empate-b of="jue-tarea-2-ej-empate" title="Pista 2 · El primer α"}
Con el orden fijo, ¿cuánto vale n2 ahora? Ése es el $\alpha$ con el que llega
n3. Compáralo con lo que devuelve el primer hijo de n3.
:::

::: answer {#jue-tarea-2-resp-empate of="jue-tarea-2-ej-empate" title="Respuesta · n1 con empate"}
**1. Los finales.** Cambian dos: **n2**, donde Negras no tiene jugada, y
**n13**, donde no la tiene Blancas. Los dos pasan a valer **0**. Los otros
cinco son llegadas a la fila 3 y siguen valiendo $+1$.

**2. Minimax.** Las ramas de n4 y n6 no cambian: siguen valiendo $+1$.

$$V(\text{n3})=\min\{+1,\ +1,\ 0\}=0,$$

$$V(\text{n1})=\max\{0,\ 0\}=0.$$

Las **dos** jugadas de n1 alcanzan el 0: $\text{c1}\textbf{-}\text{c2}$ y
$\text{c1}\textbf{x}\text{b2}$.

**3. Orden fijo: 10 estados.** n2 vale 0, así que n3 llega con $\alpha=0$.
Su primer hijo, n4, devuelve $+1$: no hay corte, y $\beta$ baja a $+1$. n6
llega con $\alpha=0$ y $\beta=+1$, y lo hereda n8, más abajo:

- en n8, n9 vale $+1\ge\beta=+1$: **corte beta**, n10 no se genera;
- en n6, n7 devuelve $+1\ge\beta=+1$: **corte beta**, n11 y n12 no se
  generan.

Después n13 vale 0, n3 devuelve 0 y la raíz, 0. Se generan n1, n2, n3, n4,
n5, n6, n7, n8, n9 y n13.

**4. Orden invertido: 8 estados.** n3 va primero y su primer hijo, n13,
vale 0: $\beta=0$. En n6, n12 vale $+1\ge\beta=0$: **corte beta**, y n11 y
n7 no se generan. n4 y n5 devuelven $+1$, n3 devuelve 0, y n2 también vale
0. Se generan n1, n3, n13, n6, n12, n4, n5 y n2.

**5. Por qué ahora se poda menos.** En el original, n2 valía $+1$ y la raíz
llegaba a n3 con $\alpha=+1$: el primer hijo de n3 ya bastaba para cortar.
Ahora n2 solo asegura 0, y el primer hijo de n3 vale $+1$, más que eso: con
lo visto hasta ahí, n3 todavía podría ser mejor para Blancas. **Un $\alpha$
más bajo corta menos.**

**6. Cuál jugar.** Con juego perfecto las dos empatan. Pero
$\text{c1}\textbf{-}\text{c2}$ empata **ya**, mientras que
$\text{c1}\textbf{x}\text{b2}$ empata solo si Negras responde
$\text{c3}\textbf{x}\text{b2}$. Si Negras juega otra cosa, Blancas gana.
Conviene $\text{c1}\textbf{x}\text{b2}$: en el peor caso da lo mismo, y le
deja a Negras dos maneras de equivocarse. Es un desempate dentro del
$\operatorname{arg\,max}$, como el de ganar rápido: no cambia ningún valor.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Cambiaste solo los finales donde alguien se quedó sin jugada.
- Anotaste $\alpha$ y $\beta$ al llegar a cada nodo, no solo los cortes.
- Marcaste cada corte como alfa o beta y dijiste qué estados no se
  generaron.
- Separaste el valor de n1 de la jugada que elegirías.

**Punto de control:** deberías poder escribir el modelo de un juego
pequeño, resolverlo con minimax, recorrerlo con alfa-beta en dos órdenes
distintos y explicar por qué el ahorro cambió.

## Lo que hay que llevarse

- El estado guarda lo que la utilidad necesita: $\Delta$ en monedas. Para
  reutilizar valores basta lo que decide el futuro: el tramo que queda.
- La jugada codiciosa puede perder: minimax compara contra la mejor
  respuesta del rival, no contra la que esperas.
- Cambiar los finales cambia lo que poda alfa-beta: un $\alpha$ más bajo
  corta menos.
- Entre jugadas que empatan, se puede desempatar sin tocar la utilidad.

Continúa con [[juegos-cuando-no-cabe|la clase 3]], donde el árbol ya no cabe.
