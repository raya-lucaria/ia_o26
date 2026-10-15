---
id: cortar-y-evaluar
title: Cortar y evaluar
nav_title: Cortar y evaluar
summary: "Cuando no se puede llegar a los finales, minimax se detiene a cierta profundidad y estima cada posición con una función de evaluación, EVAL, que aproxima 100·V. Los finales valen 100·U y se reconocen antes de cortar. A mano en una posición de 4×4 y como algoritmo en el árbol de resultados: a profundidad 1 elige una jugada que pierde."
status: ready
estimated_time: 72m
tags: [juegos, busqueda-adversarial, evaluacion]
aliases: [minimax-con-corte]
---

# Cortar y evaluar

**¿Qué hacemos si no podemos llegar a los finales?**

Miramos unas cuantas jugadas, nos detenemos y estimamos. El número que resulta es útil, pero ya no es el valor del juego.

Al terminar tendrás:

- **una función de evaluación** para peones, calculada a mano en tableros de 4×4;
- **el minimax con corte** de las tres jugadas de una posición, a profundidad 1, 2 y 3, y un caso en el que **cortar se equivoca**;
- **el pseudocódigo y el Python** de minimax con corte, que es MINIMAX más una línea;
- **una traza en el árbol de resultados**, y qué se puede **afirmar** de lo que devuelve y **cuánto cuesta**.

## Lo que traes

- **Las reglas generan el juego.** $S$ y $s_0$ (@jue-c1-estado); $S_F$ reconoce finales (@jue-c1-finales); $\mathrm{Pl}(s)$ lee quién mueve (@jue-c1-pl); $A(s)$ enumera jugadas (@jue-c1-acciones); $T(s,a)$ produce el siguiente estado (@jue-c1-transicion); $U$ paga los finales (@jue-c1-utilidad).
- **El valor se mide desde MAX.** $V(s)$ es el pago para MAX si los dos juegan lo mejor (@jue-c2-valor); $Q(s,a)=V(T(s,a))$ valora una jugada (@jue-c1-valor-jugada-estrategia).
- **Minimax ya está escrito.** DECIDIR-MINIMAX y MINIMAX de [[minimax-como-algoritmo|Minimax como algoritmo]] recorren todo hasta los finales.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4. Blancas (B, MAX) empieza con cuatro peones en la fila 1, y Negras (N, MIN) con cuatro en la 4. Empiezan Blancas.
>
> Un peón avanza una casilla si está vacía o captura en diagonal hacia delante. Gana quien llega a la fila del rival, captura todo o deja al rival sin jugada: ${U=+1}$ si gana Blancas y ${U=-1}$ si gana Negras. En el 4×4 no hay empates.

> **Supuestos de esta página.** Los de [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin azar, todo a la vista, toda partida termina y suma cero (o constante). Uno nuevo: **no nos alcanza el tiempo para llegar a los finales**.

> [!TIP]
> **Míralo correr: minimax con corte, con d = 1, 2 o 3**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#corte)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 6: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

---

## 1 · Un juego que no cabe

### El mismo juego en 4×4

**Piensa: de las siete piezas de hexapawn, ¿cuáles cambian si el tablero pasa a 4×4?**

Casi ninguna. Las reglas son las de la clase 1 con una fila y una columna más:

- **Cambian $S$ y $s_0$.** Un estado sigue siendo un par (tablero, turno), ahora con 16 casillas. Al empezar hay cuatro peones por lado y mueve Blancas.
- **Las reglas que definen $S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$ no cambian.** Se llega a la fila del rival, se captura todo o se deja al rival sin jugada; $\mathrm{Pl}$ lee el turno guardado; ${U=\pm1}$.

La clase 1 dijo que en el 3×3 el turno se podía deducir del tablero, aunque lo guardábamos por principio. **En el 4×4 ya no:** la computadora encontró 2925 tableros que se alcanzan con los dos turnos. Guardar el turno en el estado era necesario.

::: table {#jue-c3-octapawn-inicio title="El tablero de 4×4 al empezar"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | N | N |
| **3** | · | · | · | · |
| **2** | · | · | · | · |
| **1** | B | B | B | B |
:::

### Cuánto crece el árbol

**Piensa: si el tablero pasa de 3×3 a 4×4, ¿el árbol crece al doble, al triple o más?**

Mucho más. La computadora contó los dos árboles completos:

::: table {#jue-c3-crecimiento title="Del tablero de 3×3 al ajedrez"}
| Tablero | Nodos | Estados |
|---|---:|---:|
| 3×3 | 252 | 135 |
| 4×4 | 4 197 973 | 20 286 |
| Ajedrez | — | ${\approx10^{44}}$ |
:::

- **Nodos** cuenta los del árbol completo, que no junta estados repetidos. Un mismo tablero con el mismo turno aparece una vez por cada orden de jugadas que lo alcanza.
- **Estados** cuenta los del grafo de la clase 1, que guarda cada uno una sola vez.

Con juego perfecto, en el 3×3 (hexapawn) gana el segundo y en el 4×4 gana el primero. En el ajedrez nadie lo sabe.

::: exercise {#jue-c3-ej-crecimiento title="Compara los dos árboles"}
1. ¿Cuántas veces más nodos tiene el árbol del 4×4 que el de hexapawn?
2. ¿Cuántos nodos hay por cada estado, en promedio, en cada tablero? ¿En cuál se repiten más los estados?
:::

::: hint {#jue-c3-pista-crecimiento-1 of="jue-c3-ej-crecimiento" title="Qué es un nodo"}
Divide los nodos entre los estados de cada fila de la tabla @jue-c3-crecimiento.
:::

::: answer {#jue-c3-resp-crecimiento of="jue-c3-ej-crecimiento"}
1. ${4\,197\,973/252\approx16\,659}$: **más de 16 000 veces**, por una fila y una columna más.
2. En el 3×3, ${252/135\approx1.9}$ nodos por estado; en el 4×4, ${4\,197\,973/20\,286\approx207}$. Se repiten mucho más en el 4×4: con más jugadas hay muchos más órdenes distintos que llegan al mismo estado.
:::

El 4×4 todavía lo resuelve una computadora, pero ya no una persona con lápiz.

El ajedrez está en otra escala. Tromp y Österlund estimaron en 2021 que tiene cerca de ${4.8\times10^{44}}$ posiciones legales, y Claude Shannon estimó en 1950 que hay unas $10^{120}$ partidas. **Ni recordando cada posición cabe**: no hay memoria para $10^{44}$ estados, y menos tiempo para recorrerlos.

### El problema

**Piensa: si no se puede llegar a los finales, ¿qué puede pedirse?**

Algo más modesto que la jugada óptima:

> **Dado:** las reglas del juego, un estado $s$ donde mueve MAX y un presupuesto: ${d\ge1}$, cuántas jugadas se pueden mirar desde $s$.
>
> **Encontrar:** una jugada de $A(s)$, lo mejor posible con ese presupuesto.

::: exercise {#jue-c3-ej-problema title="Compara con el problema de la unidad"}
Pon este problema junto al de la unidad (@jue-c1-problema).

1. ¿Qué dato nuevo recibe?
2. ¿Qué pedía el de la unidad que éste ya no pide, y por qué?
:::

::: hint {#jue-c3-pista-problema-1 of="jue-c3-ej-problema" title="Renglón por renglón"}
Compara primero los dos «Dado» y luego los dos «Encontrar». ¿Qué hace falta para saber qué jugada asegura la mayor utilidad?
:::

::: answer {#jue-c3-resp-problema of="jue-c3-ej-problema"}
1. El **presupuesto**: cuántas jugadas se pueden mirar.
2. La jugada que **asegura** la mayor utilidad. Para saber cuál es hay que llegar a los finales, y eso es justo lo que ya no cabe.
:::

La respuesta ya no viene con garantía. Esta página muestra qué tan bien, y qué tan mal, puede salir.

---

## 2 · Cortar y estimar

### Lo que queremos y lo que cuesta

**Piensa: ¿qué número querríamos para cada jugada, si el tiempo alcanzara?**

Su $Q$: el pago que MAX se asegura con esa jugada si los dos juegan lo mejor. MAX juega la de mayor $Q$, y $V(s)$ es ese máximo.

::: table {#jue-c3-tab-q-a-b title="V y Q en un árbol mínimo"}
| Jugada de MAX | Finales que elige MIN | $Q(s,a)$ |
|---|---|---:|
| $a$ | $+1$ o $-1$ | $-1$ |
| $b$ | $0$ o $0$ | $\mathbf{0}$ |
:::

- **El número de una jugada vive en su hijo.** $Q(s,a)$ es el $V$ del estado al que lleva $a$: tras $a$, MIN elige $-1$.
- **MAX elige el mayor $Q$.** Aquí $V(s)=\max(-1,0)=0$, con $b$.
- **Calcularlo exige llegar a los finales.** En el 4×4 eso son millones de nodos; en el ajedrez, imposible.

### Dos cambios a minimax

**Piensa: si solo te alcanza para ver dos jugadas hacia delante, ¿qué haces con las posiciones donde te detienes?**

Las **juzgas**. Una persona que juega ajedrez no calcula hasta el final: mira unas jugadas, se detiene y dice «tengo un peón de más». Minimax con corte hace lo mismo, con dos cambios:

1. **Lleva la cuenta de la profundidad que queda, $d$:** cuántas jugadas más, contando las de los dos jugadores, puede mirar. En la raíz, $d$ es el presupuesto; cada jugada la baja en uno.
2. **Donde llega a ${d=0}$ usa una estimación $\mathrm{EVAL}(s)$**, en lugar de $V(s)$, que exigiría recorrer todo lo de abajo.

Ojo con la letra: $d$, en cursiva, es siempre esta profundidad. Es un número, no la columna d del tablero, la de $\text{d2}\textbf{-}\text{d3}$.

Ojo también con la palabra: **corte** es dejar de mirar a cierta profundidad y estimar; lo que hace alfa-beta se llama **poda**.

::: definition {#jue-c3-evaluacion title="Función de evaluación"}
**Qué es.** Una **función de evaluación** $\mathrm{EVAL}(s)$ asigna a un estado no final $s$ un número que estima $100\cdot V(s)$, siempre desde MAX.

**Cómo se calcula.** **Mirando solo $s$**, sin buscar hacia delante. No es un estimador estadístico: no promedia muestras, y por eso no lleva gorro.

**Qué significa.** Es un juicio rápido, como «tengo un peón de más».

**Qué no es.** No es $V(s)$. No viene del reglamento: la escribimos nosotros, y puede equivocarse.
:::

### Una evaluación para los peones

**Piensa: mirando solo un tablero de peones, ¿qué te dice quién va mejor?**

Dos cosas saltan a la vista: **cuántos peones** tiene cada uno y **cuánto han avanzado**. Un peón avanzado está más cerca de la fila del rival, que es una forma de ganar. El avance de un peón blanco es cuántas filas subió desde la fila 1; el de uno negro, cuántas bajó desde la fila 4.

$$\mathbf{\mathrm{EVAL}(s)=10\cdot\text{material}+\text{avance}},$$

donde **material** es peones blancos menos peones negros, y **avance** es el avance blanco menos el avance negro.

Los dos rasgos se restan porque lo que es bueno para Negras es malo para Blancas: la evaluación, igual que $U$, se mide en puntos de MAX.

Ésta es la posición que usaremos en toda la clase. Mueven Blancas.

::: table {#jue-c3-posicion title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

::: table {#jue-c3-posicion-eval title="La evaluación de la posición de la clase, por rasgo"}
| | Blancas | Negras |
|---|---|---|
| Peones | a1, c2, d2: **3** | a4, b4, c3: **3** |
| Avance | ${0+1+1=}$ **2** | ${0+0+1=}$ **1** |
:::

$$\mathrm{EVAL}=10\cdot(3-3)+(2-1)=1.$$

Van parejos en peones, y Blancas está un poco más avanzada.

### Pesar los finales más que cualquier estimación

**Piensa: si una victoria valiera ${+1}$ y un peón de más valiera $10$, ¿qué preferiría el algoritmo?**

El peón. Por eso hay que poner $U$ en la **misma escala** que $\mathrm{EVAL}$. En los finales usamos ${100\cdot U(s)}$: **100** si gana Blancas y **${-100}$** si gana Negras.

- **Multiplicar por 100 solo cambia la escala.** El orden entre finales es el mismo que con $U$; un empate, en los juegos que lo tienen, sigue valiendo 0.
- **100 es mayor que cualquier evaluación.** La computadora comprobó que, en las posiciones alcanzables del 4×4 que no son finales, $\mathrm{EVAL}$ nunca pasa de 36 en valor absoluto.
- **En general, la escala se llama $M$.** Hace falta ${|\mathrm{EVAL}|<M}$ en todo estado no final; en esta página, ${M=100}$.

::: remark {#jue-c3-orden-finales title="La evaluación tiene que respetar el orden de los finales"}
Una función de evaluación puede equivocarse en las posiciones sin terminar, pero no debe contradecir lo que ya se sabe: **ganar vale más que cualquier estimación, y perder, menos**. Si no lo cumple, el programa puede preferir una posición «buena» a una victoria segura.
:::

::: exercise {#jue-c3-ej-escala title="Encuentra una escala que no alcanza"}
Alguien propone usar ${30\cdot U}$ en los finales en vez de ${100\cdot U}$. ¿Respeta el orden de los finales? Usa la cifra de arriba.
:::

::: hint {#jue-c3-pista-escala-1 of="jue-c3-ej-escala" title="Compara dos números"}
¿Cuánto puede valer, como mucho, la $\mathrm{EVAL}$ de una posición sin terminar? ¿Y una victoria con esa escala?
:::

::: answer {#jue-c3-resp-escala of="jue-c3-ej-escala"}
No. Una posición sin terminar puede tener ${\mathrm{EVAL}=36}$, más que los 30 de una victoria. El programa podría preferir esa posición a ganar. Con 100, ninguna estimación alcanza a un final.
:::

Los finales que aparezcan antes de llegar a ${d=0}$, o justo en ${d=0}$, se siguen valorando con ${100\cdot U}$: ahí no hay nada que estimar.

::: exercise {#jue-c3-ej-presupuesto title="Sigue la profundidad que queda"}
El presupuesto es ${d=3}$ en la raíz, donde mueve Blancas.

1. ¿Cuánto vale $d$ tras la primera jugada de Blancas, tras la respuesta de Negras y tras la segunda jugada de Blancas?
2. ¿En cuál de esos niveles se usa $\mathrm{EVAL}$?
3. Si la primera jugada de Blancas llegara a la fila 4, ¿con qué número se valoraría ese nodo?
:::

::: hint {#jue-c3-pista-presupuesto-1 of="jue-c3-ej-presupuesto" title="Un renglón por jugada"}
Escribe la raíz con su $d$ y baja un renglón por cada jugada. ¿Importa de quién es la jugada para lo que le pasa a $d$?
:::

::: answer {#jue-c3-resp-presupuesto of="jue-c3-ej-presupuesto"}
1. ${d=2}$, luego ${d=1}$, luego ${d=0}$: cada jugada la baja en uno, sea de quien sea.
2. Tras la segunda jugada de Blancas, donde ${d=0}$.
3. Con ${100\cdot U=100}$: ese nodo es un final, y no se estima aunque le queden dos jugadas por mirar.
:::

---

## 3 · El algoritmo

Una sola ficha: minimax con corte **por nivel**, con $d$ fijo antes de buscar.

### Minimax con corte

**Piensa: ¿qué número obtienes si haces minimax sobre un árbol que se detiene en $d$?**

El minimax de ese árbol cortado. Se llama **valor con corte**, y es lo que este algoritmo calcula exactamente.

- **Qué valor rastrea:** $V_d(s)$, el valor con corte del estado $s$ cuando quedan $d$ jugadas por mirar. Estima $100\cdot V(s)$; el de una jugada es el de su hijo.
- **Dónde lo guarda:** cada llamada abierta guarda su $v$ en su marco de la pila (los datos de una llamada abierta). Al terminar lo devuelve y lo olvida: no guarda el árbol.
- **Cómo sube:** con el máximo de los hijos en MAX y el mínimo en MIN, desde $\mathrm{EVAL}$ en los nodos de corte y ${100\cdot U}$ en los finales.
- **A qué converge:** no promedia ni itera: da un número exacto del árbol cortado. Si alcanza todos los finales, devuelve $100\,V(s)$.

::: figure {#jue-c3-fig-flujo-corte title="Minimax con corte, en palabras"}
![Diagrama de flujo del corte. En cada nodo: ¿es final? Si sí, vale 100·U y vuelve al padre. Si no, ¿d = 0? Si sí, vale EVAL y vuelve al padre. Si no, baja a cada hijo con d − 1; al volver, MAX se queda con el mayor y MIN con el menor. Cuando no quedan hijos, vuelve al padre con su valor; en la raíz, juega la jugada de mayor valor](../_assets/jue-c3-rx-flujo-corte.svg)
:::

::: definition {#jue-c3-valor-con-corte title="Valor con corte"}
**Qué es.** El **valor con corte** $V_d(s)$ es el minimax del árbol cortado a $d$ jugadas, con $\mathrm{EVAL}$ en los nodos de corte y ${M\cdot U}$ en los finales.

**Cómo se calcula.** Con los casos en este orden; el final se revisa **antes** que ${d=0}$:

$$
\mathbf{
\begin{aligned}
&V_d(s)=\\
&\begin{cases}
M\cdot U(s) & \text{si } s\in S_F,\\
\mathrm{EVAL}(s) & \text{si } d=0,\\
\max_{a\in A(s)} V_{d-1}(T(s,a)) & \text{si } \mathrm{Pl}(s)=\text{MAX},\\
\min_{a\in A(s)} V_{d-1}(T(s,a)) & \text{si } \mathrm{Pl}(s)=\text{MIN}.
\end{cases}
\end{aligned}}
$$

**Qué significa.** Es **el minimax de la evaluación**. No lleva gorro: no es una estadística, sino una cuenta exacta sobre otro árbol.

**Qué no es.** No es $V(s)$, el valor del juego, y puede equivocarse. Si alcanza todos los finales, devuelve $100\,V(s)$, no $V(s)$.
:::

#### 1 · Exploración: cómo obtiene su número

**La regla.** Recorre el árbol en profundidad, en el orden dado, y en cada nodo revisa:

1. **¿Es final? (*terminal test*)** Devuelve ${100\cdot U}$, aunque ya no quede profundidad.
2. **¿Se acabó la profundidad?** Si no es final y ${d=0}$, es un **nodo de corte** (*cutoff*): devuelve su $\mathrm{EVAL}$ y no genera hijos.
3. **Si queda profundidad, expande.** Valora cada hijo con ${d-1}$; MAX se queda con el mayor y MIN con el menor.

- **Cada jugada consume un nivel**, sea de quien sea. Con ${d=1}$ en la raíz, sus hijos ya llegan con ${d=0}$.
- **El invariante conserva la perspectiva.** Todo número mide el pago de MAX; cambia dónde se detiene la búsqueda, no la regla de minimax.

**Ejemplo mínimo:** un nodo de MAX con ${d=1}$ y dos hijos.

| Hijo | Tipo | Valor |
|---|---|---|
| $a$ | No final | EVAL $40$ |
| $b$ | Final: gana MAX | $100$ |

- **Con el orden correcto elige $b$.** El final se reconoce antes de evaluar y vale 100.
- **Con los pasos 1 y 2 al revés**, ese final se evaluaría como un tablero sin terminar, por ejemplo con 30. Elegiría $a$ y dejaría pasar una victoria.

**Una EVAL es una estimación, no un resultado.** El 40 de $a$ podría ocultar una derrota detrás del corte.

---

**Recorrido: la posición de la clase, a mano.**

**Profundidad 1: mirar una jugada y evaluar.**

**Piensa: si Blancas solo mira su propia jugada, ¿qué le conviene más, avanzar o capturar?**

Lo que diga $\mathrm{EVAL}$ justo después. **Estamos aquí:** la posición de la clase, con ${\mathrm{EVAL}=1}$. Blancas tiene tres jugadas: $\text{a1}\textbf{-}\text{a2}$, $\text{d2}\textbf{-}\text{d3}$ y $\text{d2}\textbf{x}\text{c3}$. El peón de c2 no puede moverse: tiene c3 enfrente y nada que capturar en b3 ni en d3.

Con ${d=1}$ en la raíz, cada jugada de Blancas deja ${d=0}$: sin esperar la respuesta de Negras, se evalúa.

Esos tres hijos son **nodos de corte**: estados no finales a los que se llega con ${d=0}$. En las figuras llevan el borde punteado de la clase 1, el de un estado que existe pero no se expande.

::: exercise {#jue-c3-ej-prof-1 title="Calcula la jugada a profundidad 1"}
1. Calcula $\mathrm{EVAL}$ después de cada una de las tres jugadas.
2. ¿Qué jugada elige Blancas a profundidad 1?
:::

::: hint {#jue-c3-pista-prof-1-1 of="jue-c3-ej-prof-1" title="Rasgo por rasgo"}
En cada jugada, ¿cambia el número de peones de alguno de los dos lados? ¿Cuántas filas sube el peón que se mueve?
:::

::: answer {#jue-c3-resp-prof-1 of="jue-c3-ej-prof-1"}
1. $\text{a1}\textbf{-}\text{a2}$ y $\text{d2}\textbf{-}\text{d3}$: ${10\cdot0+(3-1)=2}$. $\text{d2}\textbf{x}\text{c3}$: quedan 3 peones blancos contra 2 negros, con avance $3$ contra $0$: ${10\cdot1+(3-0)=13}$.
2. **$\text{d2}\textbf{x}\text{c3}$**, con 13: gana un peón.
:::

::: figure {#jue-c3-fig-prof-1 title="Profundidad 1: la captura parece ganar un peón"}
![La posición de la clase arriba, donde mueve Blancas. Sus tres jugadas llevan a nodos de corte, con borde punteado porque ahí la búsqueda se detiene: a1-a2 da EVAL = 2; d2-d3 da EVAL = 2; d2xc3 da EVAL = 13. Blancas toma el máximo, 13: la flecha de d2xc3 va resaltada](../_assets/jue-c3-corte-prof-1.svg)
:::

A profundidad 1, Blancas **captura**. Parece obvio: un peón de más.

**Profundidad 2: mirar también la respuesta.**

**Piensa: si Blancas mira también la respuesta de Negras, ¿cuál de sus respuestas supone?**

La peor para Blancas. Con ${d=2}$ en la raíz, miramos la jugada de Blancas, **todas las respuestas de Negras**, y evaluamos. Negras es MIN: de sus respuestas, elige la de menor $\mathrm{EVAL}$.

- **$\text{a1}\textbf{-}\text{a2}$.** Negras puede responder $\text{c3}\textbf{x}\text{d2}$ (${-10}$), $\text{a4}\textbf{-}\text{a3}$ (1) o $\text{b4}\textbf{-}\text{b3}$ (1). Lo peor para Blancas: ${-10}$.
- **$\text{d2}\textbf{-}\text{d3}$.** El peón de c3 queda bloqueado por c2 y sin nada que capturar. Negras puede responder $\text{a4}\textbf{-}\text{a3}$ o $\text{b4}\textbf{-}\text{b3}$, las dos con 1. Lo peor para Blancas: 1.
- **$\text{d2}\textbf{x}\text{c3}$.** Es el ejercicio que sigue.

::: exercise {#jue-c3-ej-prof-2 title="Encuentra el valor de la captura a profundidad 2"}
Tras $\text{d2}\textbf{x}\text{c3}$, el tablero es éste y mueven Negras:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | B | · |
| **2** | · | · | B | · |
| **1** | B | · | · | · |

1. Escribe las jugadas de Negras.
2. Calcula $\mathrm{EVAL}$ después de cada una.
3. ¿Cuánto vale la captura a profundidad 2? ¿Qué jugada elige Blancas ahora?
:::

::: hint {#jue-c3-pista-prof-2-1 of="jue-c3-ej-prof-2" title="Peón por peón"}
Recorre los peones negros uno por uno. Para cada uno, ¿qué casilla tiene enfrente, qué casillas tiene en sus dos diagonales hacia abajo, y quién ocupa cada una?
:::

::: answer {#jue-c3-resp-prof-2 of="jue-c3-ej-prof-2"}
1. $\text{a4}\textbf{-}\text{a3}$, $\text{b4}\textbf{-}\text{b3}$ y **$\text{b4}\textbf{x}\text{c3}$**: el peón de b4 captura en diagonal.
2. Tras un avance: ${10\cdot(3-2)+(3-1)=12}$. Tras $\text{b4}\textbf{x}\text{c3}$ quedan dos peones por lado, con avance 1 cada uno: ${\mathrm{EVAL}=0}$.
3. Negras recaptura, así que la captura vale **0**. Blancas compara ${-10}$, 1 y 0 y elige **$\text{d2}\textbf{-}\text{d3}$**.
:::

::: figure {#jue-c3-fig-prof-2 title="Profundidad 2: Negras recaptura y Blancas elige d2-d3"}
![La posición de la clase, sus tres jugadas y todas las respuestas de Negras, que son nodos de corte con su EVAL. Tras a1-a2, Negras puede c3xd2 (−10), a4-a3 (1), b4-b3 (1): el mínimo es −10. Tras d2-d3, Negras puede a4-a3 (1), b4-b3 (1): el mínimo es 1. Tras d2xc3, Negras puede a4-a3 (12), b4-b3 (12), b4xc3 (0): el mínimo es 0. Blancas toma el máximo, 1, con d2-d3: las flechas resaltadas](../_assets/jue-c3-corte-prof-2.svg)
:::

**Mirar una jugada más cambió la decisión.** La captura ganaba un peón, pero Negras lo recupera enseguida.

**Profundidad 3: mirar la segunda jugada de Blancas.**

**Piensa: a profundidad 3, ¿dónde quedan los nodos de corte?**

Tras la segunda jugada de Blancas: se mira jugada de Blancas, respuesta de Negras y otra jugada de Blancas. El árbol completo ya tiene 33 nodos. Aquí haces a mano solo la rama de $\text{d2}\textbf{-}\text{d3}$, la que eligió la profundidad 2.

::: exercise {#jue-c3-ej-prof-3 title="Calcula la rama d2-d3 a profundidad 3"}
Tras $\text{d2}\textbf{-}\text{d3}$, el tablero es éste y mueven Negras, con ${d=2}$:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | B |
| **2** | · | · | B | · |
| **1** | B | · | · | · |

1. Escribe las respuestas de Negras y, bajo cada una, todas las jugadas de Blancas.
2. Valora cada hoja.
3. ¿Cuánto vale $\text{d2}\textbf{-}\text{d3}$ a profundidad 3? ¿Cuántos nodos tiene la rama, contando el de $\text{d2}\textbf{-}\text{d3}$?
:::

::: hint {#jue-c3-pista-prof-3-1 of="jue-c3-ej-prof-3" title="Dos niveles"}
Primero las respuestas de Negras; luego, bajo cada una, los peones blancos uno por uno, con su avance y sus dos diagonales. Antes de aplicar $\mathrm{EVAL}$ a una hoja, ¿qué hay que revisar?
:::

::: answer {#jue-c3-resp-prof-3 of="jue-c3-ej-prof-3"}
1. Negras solo tiene $\text{a4}\textbf{-}\text{a3}$ y $\text{b4}\textbf{-}\text{b3}$. Tras $\text{a4}\textbf{-}\text{a3}$, Blancas tiene $\text{a1}\textbf{-}\text{a2}$ y $\text{d3}\textbf{-}\text{d4}$. Tras $\text{b4}\textbf{-}\text{b3}$, tiene además $\text{c2}\textbf{x}\text{b3}$.
2. $\text{d3}\textbf{-}\text{d4}$ llega a la fila 4: es un **final**, vale 100 y no se estima. $\text{a1}\textbf{-}\text{a2}$ da 2 en los dos casos; $\text{c2}\textbf{x}\text{b3}$ da 13.
3. Blancas toma 100 bajo cada respuesta, y Negras, el mínimo de 100 y 100: la rama vale **100**. Tiene **8** nodos: 1 + 2 respuestas + 2 + 3 jugadas.
:::

::: figure {#jue-c3-fig-prof-3 title="Profundidad 3: d3-d4 llega a la fila 4 y d2-d3 vale 100"}
![Solo la rama d2-d3 del árbol con d = 3 en la raíz. Tras d2-d3 mueve Negras, que tiene 2 respuestas. Tras a4-a3, Blancas puede a1-a2 (2, EVAL) o d3-d4 (100, final: gana Blancas): el máximo es 100. Tras b4-b3, Blancas puede a1-a2 (2, EVAL), c2xb3 (13, EVAL) o d3-d4 (100, final: gana Blancas): el máximo es 100. Negras toma el mínimo, 100: d2-d3 vale 100. La rama tiene 8 nodos](../_assets/jue-c3-corte-prof-3.svg)
:::

A profundidad 3 el algoritmo ya ve la victoria. Hagas lo que hagas Negras, Blancas llega a la fila 4.

**Comparar con el valor exacto.**

**Piensa: ¿alguna de estas profundidades garantiza la jugada correcta?**

Ninguna lo garantiza en general. Aquí la 3 sí: su 100 solo puede venir de finales, porque ninguna $\mathrm{EVAL}$ llega a 100.

Para saber cuál es la correcta, la computadora recorrió el árbol del 4×4 hasta los finales: eso da el **valor exacto** de cada jugada, $Q(s_{\text{raíz}},a)$. Las otras dos ramas de la profundidad 3 también las hizo la computadora. En la tabla, P1, P2 y P3 son las profundidades 1, 2 y 3, y la última columna pone $Q$ por 100, en la escala de las demás.

::: table {#jue-c3-profundidades title="Las tres jugadas a profundidad 1, 2 y 3, y su valor exacto"}
| Jugada | P1 | P2 | P3 | ${100\,Q(s_{\text{raíz}},a)}$ |
|---|---:|---:|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 2 | −10 | −9 | −100 |
| $\text{d2}\textbf{-}\text{d3}$ | 2 | **1** | **100** | **100** |
| $\text{d2}\textbf{x}\text{c3}$ | **13** | 0 | 1 | −100 |
:::

En negrita, el máximo de cada columna: la jugada que elige Blancas.

::: exercise {#jue-c3-ej-exacto title="Señala qué profundidad acierta"}
1. ¿Con qué profundidades elige Blancas una jugada que gana?
2. ¿Con cuál elige una que pierde, y cuánto la sobreestima?
:::

::: hint {#jue-c3-pista-exacto-1 of="jue-c3-ej-exacto" title="Columna contra columna"}
En cada columna de profundidad, ¿qué jugada tiene el máximo? ¿Cuánto vale esa jugada en la última columna?
:::

::: answer {#jue-c3-resp-exacto of="jue-c3-ej-exacto"}
1. Con profundidad 2 y 3: las dos eligen $\text{d2}\textbf{-}\text{d3}$, que vale 100.
2. Con profundidad 1: elige $\text{d2}\textbf{x}\text{c3}$ con 13, y esa jugada vale ${-100}$. La sobreestima en **113 puntos**, ${13-(-100)}$. **Capturar pierde y $\text{d2}\textbf{-}\text{d3}$ gana.**
:::

**La profundidad 2 acierta sin ver la victoria:** solo vio que capturar salía mal. Su 1 es una estimación que, aquí, alcanzó para elegir bien.

---

**El procedimiento.**

**Piensa: ¿qué línea hay que agregarle a MINIMAX para que se detenga?**

Una sola, la 9. Lo demás es DECIDIR-MINIMAX y MINIMAX de [[minimax-como-algoritmo|Minimax como algoritmo]], con $d$ como argumento y ${d-1}$ en cada hijo.

**Qué recibe y qué genera.** Además de las reglas y $d$, recibe $\mathrm{EVAL}$ (@jue-c3-evaluacion) y devuelve una jugada de mayor valor con corte (@jue-c3-valor-con-corte). Como minimax, no recibe el grafo: genera los estados con $A$ y $T$ mientras recorre, **pero solo hasta $d$ jugadas**. Los nodos de corte sí se generan, porque hay que evaluarlos, pero no se expanden.

```text
INPUT   un estado s donde mueve MAX; la
        profundidad d ≥ 1; las reglas S_F,
        Pl, A, T y U; y una función EVAL.
        No recibe el grafo.
OUTPUT  una jugada de A(s) con el mayor
        valor con corte.

 1 function DECIDIR-CON-CORTE(s, d)
 2   mejor_valor ← −∞ ; mejor_jugada ← ninguna
 3   for each a in A(s)
       # ya se gastó una jugada: d − 1
 4     w ← MINIMAX-CON-CORTE(T(s, a), d − 1)
       # estricto: un empate deja la primera
 5     if w > mejor_valor:
         mejor_valor ← w ; mejor_jugada ← a
 6   return mejor_jugada       # la jugada, no w

   # d: las jugadas que quedan por mirar
 7 function MINIMAX-CON-CORTE(s, d)
     # ×100 supera a EVAL: pide |EVAL| < 100
 8   if s ∈ S_F: return 100 · U(s)
 9   if d = 0: return EVAL(s)  # se estima
10   if Pl(s) = MAX
11     v ← −∞                  # menor que todo
12     for each a in A(s)
13       w ← MINIMAX-CON-CORTE(T(s, a), d − 1)
14       v ← max(v, w)         # el mayor
15     return v
16   else                      # Pl(s) = MIN
17     v ← +∞                  # mayor que todo
18     for each a in A(s)
19       w ← MINIMAX-CON-CORTE(T(s, a), d − 1)
20       v ← min(v, w)         # el menor
21     return v
```

El mismo procedimiento en Python, línea por línea; el número entre paréntesis es la línea del pseudocódigo:

```python
from math import inf

# Las reglas: es_final(s), pl(s), acciones(s),
# transicion(s, a), utilidad(s) y evaluar(s),
# que es EVAL. pl(s) da "MAX" o "MIN".

def decidir_con_corte(s, d):    # (1)
    # (2) Aún no ha visto ninguna jugada.
    mejor_valor = -inf
    mejor_jugada = None
    for a in acciones(s):       # (3)
        # (4) Valora el hijo con una jugada
        # menos.
        w = minimax_con_corte(
            transicion(s, a), d - 1)
        # (5) Solo si mejora estrictamente.
        if w > mejor_valor:
            mejor_valor = w
            mejor_jugada = a
    return mejor_jugada         # (6) jugada

def minimax_con_corte(s, d):    # (7)
    # (8) 100·U supera a EVAL si |EVAL| < 100.
    if es_final(s):
        return 100 * utilidad(s)
    # (9) Nodo de corte: se estima.
    if d == 0:
        return evaluar(s)
    if pl(s) == "MAX":          # (10)
        v = -inf                # (11)
        for a in acciones(s):   # (12)
            # (13) una jugada menos
            w = minimax_con_corte(
                transicion(s, a), d - 1)
            v = max(v, w)       # (14) mayor
        return v                # (15)
    else:                       # (16) MIN
        v = inf                 # (17)
        for a in acciones(s):   # (18)
            # (19) una jugada menos
            w = minimax_con_corte(
                transicion(s, a), d - 1)
            v = min(v, w)       # (20) menor
        return v                # (21)
```

Respecto de DECIDIR-MINIMAX y MINIMAX:

- **La línea 9 es la nueva:** cuando ya no quedan jugadas por mirar, se estima.
- **La línea 8 solo cambia la escala** de $U$, para que un final pese más que cualquier estimación. Va antes que la 9 y pide ${|\mathrm{EVAL}|<100}$ en todo estado que no es final; con otra $\mathrm{EVAL}$, el 100 se cambia por un $M$ con ${|\mathrm{EVAL}|<M}$.
- **Las demás son las mismas**, con ${d-1}$ en cada llamada (líneas 4, 13 y 19). Como la 9 es nueva, las del MAX quedan en 10–15 y las del MIN en 16–21, no en 9–14 y 15–20.

Con ${d=1}$, ${d=2}$ y ${d=3}$, los valores $w$ de la línea 4 son las tres primeras columnas de la tabla @jue-c3-profundidades.

::: exercise {#jue-c3-ej-hoja title="Señala qué línea valora cada estado"}
Para cada estado, di con qué $d$ llega, qué línea devuelve su valor y cuánto devuelve.

1. Con ${d=2}$ en la raíz: el estado tras $\text{d2}\textbf{x}\text{c3}$ y la respuesta $\text{b4}\textbf{x}\text{c3}$.
2. Con ${d=4}$ en la raíz: el estado tras $\text{d2}\textbf{-}\text{d3}$, $\text{a4}\textbf{-}\text{a3}$ y $\text{d3}\textbf{-}\text{d4}$.
3. El mismo estado del inciso 2, ahora con ${d=3}$ en la raíz. Si las líneas 8 y 9 estuvieran en el orden contrario, ¿cuánto devolvería?
:::

::: hint {#jue-c3-pista-hoja-1 of="jue-c3-ej-hoja" title="Cuenta hacia abajo"}
¿Cuántas jugadas se hicieron desde la raíz hasta ese estado, y cuánto le quitó cada una a $d$? Después, ¿alguien gana en ese tablero?
:::

::: answer {#jue-c3-resp-hoja of="jue-c3-ej-hoja"}
1. Llega con ${d=0}$ y no es final: lo toma la **línea 9**, que devuelve ${\mathrm{EVAL}=0}$.
2. Llega con ${d=1}$. Blancas llegó a la fila 4: es final. Lo toma la **línea 8**, que devuelve ${100\cdot(+1)=100}$. La 9 ni se consulta.
3. Llega con ${d=0}$ **y** es final. La línea 8 va primero y devuelve 100. Con el orden contrario, la 9 lo evaluaría como un tablero sin terminar: tres peones por lado y avance 4 contra 2, así que ${\mathrm{EVAL}=2}$. **Una victoria segura se leería como una posición casi pareja.**
:::

::: exercise {#jue-c3-ej-genera title="Cuenta qué genera con una sola jugada"}
Con ${d=1}$ en la raíz, en la posición de la clase:

1. ¿Qué nodos genera minimax con corte? ¿Cuántos son, contando la raíz?
2. ¿Cuál se expande y cuáles se evalúan?
3. Con ${d=2}$ genera 12 nodos. ¿Cuántos de ellos se expanden, y cuántos se evalúan?
:::

::: hint {#jue-c3-pista-genera-1 of="jue-c3-ej-genera" title="Cuenta las jugadas"}
¿Cuántas jugadas tiene Blancas en la raíz? Después de una de ellas, ¿cuántas jugadas quedan por mirar?
:::

::: answer {#jue-c3-resp-genera of="jue-c3-ej-genera"}
1. **4 nodos:** la raíz y sus tres hijos, tras $\text{a1}\textbf{-}\text{a2}$, $\text{d2}\textbf{-}\text{d3}$ y $\text{d2}\textbf{x}\text{c3}$.
2. Solo se expande la raíz. Los tres hijos llegan sin jugadas por mirar y no son finales: se evalúan, con 2, 2 y 13.
3. Se expanden **4**: la raíz y sus tres hijos, que ahora llegan con ${d=1}$. Los otros **8** son las respuestas de Negras (3, 2 y 3), que llegan con ${d=0}$ y se evalúan.
:::

---

**Recorrido: el árbol de resultados.**

**Piensa: si cortas el árbol de resultados a una jugada, ¿con qué valoras I, C y D?**

Con la evaluación, porque ya no queda nada por mirar. El **árbol de resultados** tiene la forma del árbol base de [[minimax-como-algoritmo|Minimax como algoritmo]], salvo que D tiene tres hijos, y sus finales dicen quién gana:

- **R es de MAX.** Sus jugadas izq, centro y der llevan a I, C y D, donde mueve MIN.
- **I tiene dos finales:** $\text{i1}=+1$ e $\text{ix}=-1$. La segunda, ix, es una captura de MIN.
- **C tiene dos hijos de MAX:** C1, con $\text{c1a}=0$ y $\text{c1b}=-1$, y C2, con $\text{c2a}=+1$ y $\text{c2b}=-1$.
- **D tiene tres finales:** $\text{d1}=-1$, $\text{d2}=+1$ y $\text{d3}=+1$. En total, 15 nodos.

::: figure {#jue-c3-t-arbol title="El árbol de resultados: el problema"}
![El árbol de resultados, 15 nodos. R, de MAX, con tres flechas: izq hacia I, centro hacia C y der hacia D, los tres de MIN. I tiene los finales i1 = +1 e ix = −1; ix es una captura de MIN. C tiene dos hijos de MAX: C1, con c1a = 0 y c1b = −1, y C2, con c2a = +1 y c2b = −1. D tiene los finales d1 = −1, d2 = +1 y d3 = +1. Cada hoja es un final con su U](../_assets/jue-t-pm-arbol.svg)
:::

En la búsqueda con corte, cada final vale ${100\cdot U}$: ${+100}$, $0$ o ${-100}$. Le damos una $\mathrm{EVAL}$ a cada nodo interno; junto a ella va ${100\,V}$, lo que debería estimar:

::: table {#jue-c3-t-eval title="La evaluación de los nodos internos del árbol de resultados"}
| Nodo | $\mathrm{EVAL}$ | ${100\,V}$ |
|---|---:|---:|
| I | 60 | −100 |
| C | 20 | 0 |
| D | 10 | −100 |
| C1 | 10 | 0 |
| C2 | 50 | 100 |
:::

- **Ahora @jue-c3-orden-finales sí se aplica.** Ninguna $\mathrm{EVAL}$ llega a 100: una victoria queda arriba de toda estimación y una derrota, abajo. El empate c1a sigue valiendo 0.
- **La de I es mala a propósito.** Da 60 a un nodo que vale ${-100}$, porque no ve la captura ix.

**Con d = 1, izq parece la mejor.**

I, C y D llegan con ${d=0}$ y no son finales: los valora la **línea 9**, con 60, 20 y 10. DECIDIR-CON-CORTE juega izq. Es una trampa: I vale ${-100}$, porque MIN responde con la captura ix, que quedó debajo de la línea de corte.

::: figure {#jue-c3-t-fig-d1 title="Corte con d = 1: izq parece valer 60"}
![El árbol de resultados con una línea punteada, la línea de corte, debajo de I, C y D. Arriba de la línea, I, C y D llevan su EVAL: 60, 20 y 10, y R elige izq con 60. Debajo de la línea, todo lo que no se genera va en caja o círculo punteado con «?»; ahí está la captura ix. Al lado: izq parece valer 60, su valor real es −100. Se han generado 4 de 15 nodos](../_assets/jue-t-corte-d1.svg)
:::

**Con d = 2, cómo leer la traza.**

La línea de corte baja un nivel: ahora queda debajo de C1 y C2, y debajo de los finales de I y de D.

> **▶ [Recorre esta traza paso a paso](../_assets/traza_arbol_t.html#corte)** — ahí puedes cambiar $d$ entre 1, 2 y 3 y ver cuándo cambia la jugada.

La traza de DECIDIR-CON-CORTE(R, 2) usa el formato de [[minimax-como-algoritmo|Minimax como algoritmo]]:

- **Una fila al entrar a un nodo** y una por cada hijo que regresa.
- **Las líneas 8 y 9 corren dentro del hijo**, y el hijo que no se expande no tiene fila propia. Su $w$ aparece en la fila del padre: líneas 19–20 si el padre es de MIN.
- **En $w$, un final va solo** y un nodo lleva su nombre entre paréntesis.
- **En las filas de R, la columna $v$ es mejor_valor.**
- **La columna elige es mejor_jugada**, con «—» mientras vale ninguna.

**Tramo 1, filas 1 a 5 · I deja izq como primera candidata.**

::: table {#jue-c3-t-traza-d2 title="Traza de DECIDIR-CON-CORTE en el árbol de resultados con d = 2, tramo 1, filas 1 a 5"}
| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›I | +∞ |  | — |
| 3 | 19–⁠20 · R›I | 100 | 100 | — |
| 4 | 19–⁠20 · R›I | −100 | −100 | — |
| 5 | 4–⁠5 · R | −100 | −100 (I) | izq |
:::

- **Filas 3 y 4:** i1 e ix son finales. La línea 8 los valora dentro del hijo con ${100\cdot U}$, 100 y ${-100}$, y MIN se queda con ${-100}$.
- **Fila 5:** ${-100>-\infty}$, así que mejor_jugada pasa a izq, aunque vale lo peor posible.

**Tramo 1, filas 6 a 9 · Centro releva a izq.**

::: table {#jue-c3-t-traza-d2-tramo-1b title="Traza de DECIDIR-CON-CORTE en el árbol de resultados con d = 2, tramo 1, filas 6 a 9"}
| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 6 | 17 · R›C | +∞ |  | izq |
| 7 | 19–⁠20 · R›C | 10 | 10 (C1) | izq |
| 8 | 19–⁠20 · R›C | 10 | 50 (C2) | izq |
| 9 | 4–⁠5 · R | 10 | 10 (C) | centro |
:::

- **Filas 7 y 8:** C1 y C2 no son finales y llegan con ${d=0}$. La línea 9 devuelve su $\mathrm{EVAL}$, 10 y 50. Nadie genera sus hijos.
- **Fila 9:** ${10>-100}$, así que mejor_jugada pasa de izq a **centro**.

::: figure {#jue-c3-t-fig-d2-tramo-1 title="Tramo 1: C devuelve 10 y R pasa a centro"}
![El árbol de resultados con corte a profundidad 2, al cerrar el tramo 1. I vale −100, con sus finales i1 = 100 e ix = −100. C acaba de devolver 10: C1 y C2 llevan su EVAL, 10 y 50, y sus hijos van en círculo punteado con «?», porque no se generan. D y sus finales están por mirar. En el recuadro, mejor_jugada = centro y mejor_valor = 10. Se han generado 7 de 15 nodos](../_assets/jue-t-corte-d2-tramo-1.svg)
:::

**Tramo 2 · D no mejora a centro.**

::: table {#jue-c3-t-traza-d2-tramo-2 title="Traza de DECIDIR-CON-CORTE en el árbol de resultados con d = 2, tramo 2"}
| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 10 | 17 · R›D | +∞ |  | centro |
| 11 | 19–⁠20 · R›D | −100 | −100 | centro |
| 12 | 19–⁠20 · R›D | −100 | 100 | centro |
| 13 | 19–⁠20 · R›D | −100 | 100 | centro |
| 14 | 4–⁠5 · R | 10 | −100 (D) | centro |
| 15 | 6 · R | 10 |  | centro |
:::

- **Filas 11 a 13:** d1, d2 y d3 son finales, como los de I. Los dos 100 no mejoran el mínimo de MIN.
- **Fila 14:** ${-100>10}$ es falso: mejor_jugada se queda en **centro**, y la línea 6 la devuelve.

::: figure {#jue-c3-t-fig-d2-tramo-2 title="Tramo 2: D devuelve −100, que no mejora 10"}
![El árbol de resultados con corte a profundidad 2, al cerrar el tramo 2: la traza está resuelta. I vale −100 y D vale −100, calculados con sus finales; C1 y C2 llevan su EVAL, 10 y 50, y C vale 10. R elige centro con 10. Debajo de la línea de corte, los hijos de C1 y C2 van en círculo punteado con «?»: no se generan. Al lado: centro vale 10, su valor real es 0. Se han generado 11 de 15 nodos](../_assets/jue-t-corte-d2.svg)
:::

**Con d = 3, ya no hay corte.**

Ningún nodo llega con ${d=0}$ sin ser final: toda hoja la toma la línea 8. DECIDIR-CON-CORTE juega centro con 0. **Si alcanza todos los finales devuelve $100\,V(s)$, no $V(s)$:** aquí ${V=0}$, y por eso coinciden los dos números.

::: table {#jue-c3-t-por-profundidad title="El árbol de resultados con cada profundidad"}
| $d$ | I · C · D | Juega | Nodos |
|---|---|---|---:|
| 1 | 60 · 20 · 10 | izq | 4 |
| 2 | −100 · 10 · −100 | centro | 11 |
| 3 | −100 · 0 · −100 | centro | 15 |
:::

- **Los nodos generados cuentan la raíz.** Con ${d=3}$ se genera el árbol completo.
- **Con ${d=1}$, izq es la trampa.** Con ${d=2}$, la captura ix ya queda arriba de la línea de corte.
- **Con ${d=2}$, centro vale 10 y no 0.** El 10 es una estimación, pero aquí alcanza para elegir bien.

---

#### 2 · Elección: qué jugada juega

DECIDIR-CON-CORTE explora y elige; MINIMAX-CON-CORTE solo valora.

::: table {#jue-c3-tab-eleccion-corte title="Explorar y jugar con minimax con corte"}
| Decisión | Qué compara | Cuándo |
|---|---|---|
| Explorar | Valora todas las jugadas hasta $d$ | Antes de decidir |
| Jugar | Elige el mayor valor con corte | Al terminar |
:::

- **Un empate conserva el orden.** La línea 5 usa ${>}$ estricto: se queda la primera jugada que alcanzó el mejor valor.
- **No elige por $V$.** Elige por el valor con corte, que puede ser una estimación equivocada, como izq con ${d=1}$.

#### 3 · Propiedades

- **Número que da:** el valor con corte de cada jugada, $V_{d-1}(T(s,a))$, que estima ${100\cdot Q(s,a)}$. En el 4×4, mientras la búsqueda no llegue a todos los finales, solo los ${\pm100}$ son seguros.
- **Usa EVAL:** sí, en los nodos de corte. Los finales valen ${100\cdot U}$, con ${|\mathrm{EVAL}|<100}$.
- **Garantía:** con ramificación finita, termina siempre y devuelve el minimax del árbol cortado. Si alcanza todos los finales, devuelve $100\,V$ y una jugada óptima; si no, nada asegura la jugada.
- **Se puede interrumpir:** no (no es *anytime*). $d$ se fija antes de buscar, y una búsqueda a medias no ha comparado todas las jugadas.
- **Complejidad:** tiempo $O(b^d)$. Memoria $O(bd)$: a lo más $d$ llamadas abiertas, cada una con sus hasta $b$ jugadas.
- **Frente a los demás:** es minimax con una línea más. Con poda es alfa-beta con corte: el mismo valor en la raíz y, con el mismo orden, nunca más nodos. Así juegan Deep Blue (ajedrez) y Chinook (damas, que además usa tablas de finales); con dados, TD-Gammon (backgammon), con una $\mathrm{EVAL}$ aprendida por una red.
- **Supuestos:** con dos jugadores y suma cero o constante, un número desde MAX basta y MIN minimiza lo de MAX. Con suma no constante o más jugadores, pagos y $\mathrm{EVAL}$ son vectores $(U_1,\dots,U_n)$, y la regla para subir valores pasa a $\max^n$.

En $\max^n$, quien mueve maximiza su componente y copia el vector elegido, con un desempate fijo. En un árbol finito resuelto hasta los finales da un equilibrio, sin la garantía escalar de minimax; con $\mathrm{EVAL}$, solo del árbol cortado.

**Por qué termina y qué se puede afirmar.**

**Piensa: el algoritmo hace minimax sin errores de cuenta. ¿Por qué entonces no da el valor del juego?**

Porque lo hace **sobre otro árbol**: el árbol cortado a $d$ jugadas, con las hojas valoradas por las líneas 8 y 9. Que termine también depende de ese árbol, y no del juego.

::: remark {#jue-c3-termina title="Minimax con corte termina"}
Si cada estado tiene un número finito de jugadas, MINIMAX-CON-CORTE$(s,d)$ termina, aunque el juego no termine.

**Por qué:** cada llamada baja $d$ en uno, y la línea 9 ya no llama a nadie cuando ${d=0}$. La recursión baja a lo más $d$ niveles por debajo de $s$. A diferencia de minimax, que termine no depende de que las partidas terminen.
:::

::: remark {#jue-c3-que-afirma title="Qué se puede afirmar de lo que devuelve"}
MINIMAX-CON-CORTE$(s,d)$ devuelve el valor con corte de $s$ (@jue-c3-valor-con-corte), no $V(s)$. Con el mismo argumento de inducción que minimax, es el minimax del árbol cortado.

En el 4×4, ${|\mathrm{EVAL}|\le36}$ en las posiciones alcanzables que no son finales. Así, **un 100 solo puede venir de finales ganados**: Blancas tiene una victoria asegurada dentro de las $d$ jugadas, responda lo que responda Negras. Lo mismo vale para ${-100}$ y Negras. **Cualquier otro número es una estimación.**
:::

Si una hoja de corte está mal estimada, el error puede subir por el árbol hasta la raíz, como la trampa de izq con ${d=1}$.

**Cuánto cuesta.**

**Piensa: si subes $d$ en uno, ¿cuánto más trabajo hay?**

Si cada estado tiene a lo más $b$ jugadas, el árbol cortado tiene a lo más $b^d$ hojas, y cada hoja cuesta una llamada a $\mathrm{EVAL}$ o a $U$.

::: remark {#jue-c3-costo-corte title="Costo de minimax con corte"}
Con ramificación $b$ y $d$ jugadas por mirar en la raíz,

$$\text{tiempo}=O(b^d).$$

Con alfa-beta y las jugadas bien ordenadas, del orden de $O(b^{d/2})$: en el mismo tiempo se mira cerca del doble de profundo. El valor en la raíz es el mismo con o sin poda.
:::

En la posición de la clase, DECIDIR-CON-CORTE genera **4 nodos** con ${d=1}$, **12** con ${d=2}$ y **33** con ${d=3}$, contando la raíz. Cada nivel multiplica el trabajo, aunque aquí por menos de ${b=5}$. Ese 5 es el máximo de jugadas de un nodo que se expande con ${d=3}$: varios estados tienen menos jugadas, o son finales.

Por eso $d$ se elige según el **tiempo disponible**, no según el juego.

#### 4 · Casos borde

- **Un final que llega con ${d=0}$.** La línea 8 va antes que la 9: vale ${100\cdot U}$, no su $\mathrm{EVAL}$ (@jue-c3-ej-hoja).
- **Un final antes del corte.** Vale ${100\cdot U}$ aunque le queden jugadas por mirar: con ${d=4}$ en la raíz, $\text{d3}\textbf{-}\text{d4}$ llega con ${d=1}$ (@jue-c3-ej-hoja).
- **Una escala que no alcanza.** Con ${30\cdot U}$, una $\mathrm{EVAL}$ de 36 supera a una victoria (@jue-c3-ej-escala).
- **Una $\mathrm{EVAL}$ contra un final.** Un hijo con EVAL 40 pierde contra un final que vale 100; evaluar ese final dejaría pasar la victoria.
- **Un error que sube.** Una hoja de corte mal estimada puede subir por máximos y mínimos hasta la raíz, como el 60 de I; otras veces un hermano la descarta.
- **Un empate en la raíz.** Decide el orden: con ${>}$ estricto, gana la primera jugada que alcanzó el valor.
- **Una $\mathrm{EVAL}$ que no mira el turno.** El mismo tablero recibe el mismo número mueva quien mueva, aunque a mitad de un intercambio de capturas eso importe mucho.
- **Una sola jugada.** Ya está decidida; la búsqueda solo estima cuánto vale.
- **Un estado sin jugadas.** En el 4×4 siempre es un final: quien no puede mover pierde, y la línea 8 lo valora. Un estado **no final** sin jugadas rompería las reglas: las líneas 11 y 17 devolverían ${\mp\infty}$ y DECIDIR-CON-CORTE, «ninguna».
- **Finales a distintas profundidades.** El que cae antes del corte vale ${100\cdot U}$; el que queda detrás no se ve. El algoritmo no prefiere ganar pronto, salvo que $U$ lo indique.

---

#### Intuición

**Qué preferencia expresa la evaluación.**

**Piensa: ¿qué dice la suma ${10\cdot\text{material}+\text{avance}}$ sobre lo que importa?**

$\mathrm{EVAL}$ no viene del reglamento: **la escribimos nosotros**. Es una decisión de modelado, igual que la medida de comodidad del [[opt-objetivo-salones-practica|ejemplo de los salones]] en la unidad de optimización: los pesos dicen cuánto importa cada rasgo. Ésta, leída con cuidado:

- **Un peón vale lo mismo que diez filas de avance.** La computadora revisó las posiciones alcanzables del 4×4 que no son finales. Entre posiciones con distinto material, la diferencia de avance nunca compensa el peón: **el material decide primero** y el avance desempata.
- **Todos los peones valen igual**, estén donde estén, salvo por su avance.
- **No ve si un peón está bloqueado**, ni si está a punto de ser capturado.
- **No sabe a quién le toca.** La misma posición recibe el mismo número mueva quien mueva.

Ninguna de esas omisiones es un error de cuenta. Son **supuestos** del modelo, y conviene escribirlos como tales.

En ajedrez, la evaluación más conocida es la del **material**: peón 1, caballo 3, alfil 3, torre 5 y dama 9. Es la misma idea, una suma ponderada de rasgos, con los mismos huecos.

**Las tres palancas de la búsqueda.** Lo que se puede justificar de cada una:

::: table {#jue-c3-que-cambia title="Qué cambia cuando cambia la búsqueda"}
| Cambio | Efecto que se puede justificar |
|---|---|
| Subir $d$ en uno | Hasta $b$ veces más hojas. La decisión puede cambiar en cualquier sentido |
| Una $\mathrm{EVAL}$ con más rasgos | Las mismas hojas, cada una más cara. Ayuda si se acerca a ${100\cdot V}$; nada lo asegura |
| Con alfa-beta, un peor orden de jugadas | El mismo valor en la raíz, con menos podas |
:::

**Cortar cambia la pregunta:** el algoritmo responde con exactitud cuánto vale el árbol cortado, no cuánto vale el juego.

---

#### Ejercicios

::: exercise {#jue-c3-ej-inicio title="Escribe las jugadas tras dos avances"}
Desde el inicio se jugó $\text{b1}\textbf{-}\text{b2}$ y $\text{c4}\textbf{-}\text{c3}$. Mueven Blancas:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | N |
| **3** | · | · | N | · |
| **2** | · | B | · | · |
| **1** | B | · | B | B |

1. Escribe $A(s)$: todas las jugadas de Blancas en este tablero.
2. ¿Alguna es una captura?
:::

::: hint {#jue-c3-pista-inicio-1 of="jue-c3-ej-inicio" title="Peón por peón"}
Para cada peón blanco, ¿qué casilla tiene enfrente y cuáles en diagonal hacia delante? ¿Quién ocupa cada una?
:::

::: answer {#jue-c3-resp-inicio of="jue-c3-ej-inicio"}
1. Cinco: $\text{a1}\textbf{-}\text{a2}$, $\text{b2}\textbf{-}\text{b3}$, $\text{b2}\textbf{x}\text{c3}$, $\text{c1}\textbf{-}\text{c2}$ y $\text{d1}\textbf{-}\text{d2}$.
2. Una: $\text{b2}\textbf{x}\text{c3}$. El peón de b2 tiene al de c3 en una diagonal de enfrente. Los demás peones blancos no tienen ningún peón negro en diagonal: solo avanzan.
:::

::: exercise {#jue-c3-ej-eval title="Calcula dos evaluaciones"}
Desde el inicio se jugó $\text{b1}\textbf{-}\text{b2}$, $\text{c4}\textbf{-}\text{c3}$ y $\text{b2}\textbf{x}\text{c3}$, la captura del ejercicio anterior. Ahora mueven Negras:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | N |
| **3** | · | · | B | · |
| **2** | · | · | · | · |
| **1** | B | · | B | B |

1. Calcula $\mathrm{EVAL}(s_0)$, el tablero de 4×4 al empezar.
2. Calcula el $\mathrm{EVAL}$ del tablero de arriba. ¿Cambiaría si movieran Blancas?
:::

::: hint {#jue-c3-pista-eval-1 of="jue-c3-ej-eval" title="Dos rasgos"}
Para cada lado, ¿cuántos peones hay y cuántas filas avanzó cada uno desde su fila de salida? ¿Qué parte de la fórmula mira el turno?
:::

::: answer {#jue-c3-resp-eval of="jue-c3-ej-eval"}
1. Cuatro peones por lado, ninguno avanzado: ${\mathrm{EVAL}(s_0)=10\cdot0+0=0}$.
2. Blancas tiene a1, c1, d1 y c3: **4** peones, con avance 2 (el de c3). Negras tiene a4, b4 y d4: **3**, con avance 0. Entonces ${\mathrm{EVAL}=10\cdot1+2=12}$. No cambiaría: $\mathrm{EVAL}$ mira solo el tablero, no a quién le toca.
:::

::: exercise {#jue-c3-ej-afirma title="Separa lo seguro de lo estimado"}
Con ${d=3}$ en la raíz de la posición de la clase, MINIMAX-CON-CORTE devuelve ${-9}$ para $\text{a1}\textbf{-}\text{a2}$, $100$ para $\text{d2}\textbf{-}\text{d3}$ y $1$ para $\text{d2}\textbf{x}\text{c3}$.

1. ¿Cuál de los tres números es seguro? ¿En cuántas jugadas, a lo más y contando la primera, asegura la victoria, y contra cuántas respuestas de Negras lo comprobó la búsqueda?
2. Un compañero dice: «con $\text{a1}\textbf{-}\text{a2}$, Blancas pierde un peón seguro». ¿Qué se puede afirmar de verdad?
:::

::: hint {#jue-c3-pista-afirma-1 of="jue-c3-ej-afirma" title="Quién pudo dar cada número"}
¿Qué números puede devolver la línea 9 en este juego, y cuáles solo la línea 8?
:::

::: answer {#jue-c3-resp-afirma of="jue-c3-ej-afirma"}
1. **El 100.** Ninguna evaluación llega a 100, así que viene de finales. Blancas gana en a lo más **tres jugadas desde la raíz**, contando $\text{d2}\textbf{-}\text{d3}$. La búsqueda lo comprobó contra las **dos** respuestas de Negras, $\text{a4}\textbf{-}\text{a3}$ y $\text{b4}\textbf{-}\text{b3}$: no hay otras.
2. **Que lo pierde dentro del horizonte, no qué tanto importa.** La búsqueda sí ve que Negras responde $\text{c3}\textbf{x}\text{d2}$, gana un peón y lo conserva tras las dos respuestas de Blancas, $\text{a2}\textbf{-}\text{a3}$ y $\text{c2}\textbf{-}\text{c3}$: las dos valen ${-9}$. Lo que no es seguro es cuánto vale esa ventaja para el resultado: el ${-9}$ es el minimax de evaluaciones, no de finales, y no dice quién gana.
:::

::: exercise {#jue-c3-ej-cota title="Compara la cota con el árbol cortado"}
En el árbol de resultados, ningún nodo tiene más de 3 jugadas: ${b=3}$.

1. Con ${d=2}$, ¿cuántas hojas permite a lo más la cota $b^d$?
2. ¿Cuántas hojas tiene de verdad el árbol cortado, contando nodos de corte y finales? ¿Por qué menos?
:::

::: hint {#jue-c3-pista-cota-1 of="jue-c3-ej-cota" title="Dónde termina cada rama"}
Recorre las tres ramas de R. ¿Dónde se detiene cada una con ${d=2}$, y cuántos hijos tiene cada nodo de MIN?
:::

::: answer {#jue-c3-resp-cota of="jue-c3-ej-cota"}
1. ${3^2=9}$.
2. **7:** los finales i1 e ix de I, los nodos de corte C1 y C2, y los finales d1, d2 y d3 de D. Son menos porque I y C tienen 2 jugadas, no 3. Con la raíz e I, C y D, suman los 11 nodos de la tabla @jue-c3-t-por-profundidad.
:::

::: exercise {#jue-c3-ej-rasgo title="Comprueba si un rasgo nuevo arregla el error"}
En la posición de la clase, a profundidad 1, la evaluación prefirió $\text{d2}\textbf{x}\text{c3}$ (13) sobre $\text{a1}\textbf{-}\text{a2}$ y $\text{d2}\textbf{-}\text{d3}$ (2 cada una), sin ver que Negras recupera el peón.

1. ¿Cuál de los supuestos de la lista de la intuición explica ese error?
2. Una compañera propone agregar un rasgo: restar 10 por cada captura que Negras tiene disponible y sumar 10 por cada captura que tiene Blancas. Calcula la nueva evaluación tras cada una de las tres jugadas. ¿Cambia la elección?
3. Otro compañero propone contar solo las capturas de **quien mueve**, que tras la jugada de Blancas es Negras: restar 10 por cada una. Calcula otra vez. ¿Cambia la elección?
:::

::: hint {#jue-c3-pista-rasgo-1 of="jue-c3-ej-rasgo" title="Cuenta las diagonales"}
Dibuja los tres tableros. En cada uno, cuenta por separado las capturas de cada color: ¿qué peones tienen un rival en una diagonal de enfrente?
:::

::: answer {#jue-c3-resp-rasgo of="jue-c3-ej-rasgo"}
1. **«No ve si un peón está a punto de ser capturado».**
2. Tras $\text{a1}\textbf{-}\text{a2}$, Negras puede capturar en d2 y Blancas en c3: ${2-10+10=2}$. Tras $\text{d2}\textbf{-}\text{d3}$, nadie puede capturar: 2. Tras $\text{d2}\textbf{x}\text{c3}$, Negras puede capturar en c3, pero el peón de c3 también amenaza a b4: ${13-10+10=13}$. **No cambia nada**: las dos amenazas se cancelan, porque el rasgo no sabe a quién le toca.
3. Contando solo las de Negras: ${2-10=-8}$, $2$ y ${13-10=3}$. **Sigue eligiendo la captura**, por poco: tras la recaptura también cambia el avance, y el rasgo no lo ve.

Adivinar las capturas con rasgos es frágil: cada arreglo deja otro hueco. La alternativa es **mirarlas**.
:::

::: exercise {#jue-c3-ej-traza-d2 title="Completa la traza con der primero"}
Ahora R prueba sus jugadas en otro orden: **der, izq, centro**. Dentro de I, C y D el orden no cambia, y la línea 5 sigue con ${>}$ estricto. Llena los «?» de DECIDIR-CON-CORTE(R, 2) en el árbol de resultados.

**Tramo 1 · D, filas 1 a 6.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›D | +∞ |  | — |
| 3 | 19–⁠20 · R›D | ? | ? | — |
| 4 | 19–⁠20 · R›D | ? | ? | — |
| 5 | 19–⁠20 · R›D | ? | ? | — |
| 6 | 4–⁠5 · R | ? | ? (D) | ? |

**Tramo 2 · I, filas 7 a 10.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 7 | 17 · R›I | +∞ |  | ? |
| 8 | 19–⁠20 · R›I | ? | ? | ? |
| 9 | 19–⁠20 · R›I | ? | ? | ? |
| 10 | 4–⁠5 · R | ? | ? (I) | ? |

**Tramo 3 · C y la salida, filas 11 a 15.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 11 | 17 · R›C | +∞ |  | ? |
| 12 | 19–⁠20 · R›C | ? | ? (C1) | ? |
| 13 | 19–⁠20 · R›C | ? | ? (C2) | ? |
| 14 | 4–⁠5 · R | ? | ? (C) | ? |
| 15 | 6 · R | ? |  | ? |

1. Llena los «?». ¿En qué filas cambia mejor_jugada, por qué no cambia en la fila 10, y qué devuelve?
2. En esta traza, ¿qué nodos no los valora ni la línea 8 ni la 9? ¿Qué líneas los valoran?
:::

::: hint {#jue-c3-pista-traza-d2-1 of="jue-c3-ej-traza-d2" title="Qué llega a cada fila"}
En cada fila de I, C o D, ¿quién regresa: un final o un nodo? ¿Con qué $d$ llega, y es final? En las filas de R, ¿con qué compara la línea 5?
:::

::: answer {#jue-c3-resp-traza-d2 of="jue-c3-ej-traza-d2"}
En negrita, lo que era «?»; en la columna elige, desde la fila 6 todo era «?».

**Tramo 1 · D deja der como primera candidata.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›D | +∞ |  | — |
| 3 | 19–⁠20 · R›D | **−100** | **−100** | — |
| 4 | 19–⁠20 · R›D | **−100** | **100** | — |
| 5 | 19–⁠20 · R›D | **−100** | **100** | — |
| 6 | 4–⁠5 · R | **−100** | **−100** (D) | der |

**Tramo 2 · I empata y conserva der.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 7 | 17 · R›I | +∞ |  | der |
| 8 | 19–⁠20 · R›I | **100** | **100** | der |
| 9 | 19–⁠20 · R›I | **−100** | **−100** | der |
| 10 | 4–⁠5 · R | **−100** | **−100** (I) | der |

**Tramo 3 · C mejora el valor y cambia a centro.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 11 | 17 · R›C | +∞ |  | der |
| 12 | 19–⁠20 · R›C | **10** | **10** (C1) | der |
| 13 | 19–⁠20 · R›C | **10** | **50** (C2) | der |
| 14 | 4–⁠5 · R | **10** | **10** (C) | centro |
| 15 | 6 · R | **10** |  | centro |

1. mejor_jugada cambia dos veces: a der en la fila 6 ${(-100>-\infty)}$ y a centro en la 14 ${(10>-100)}$. En la fila 10, ${-100>-100}$ es falso: izq empata con der y se queda la primera. Devuelve **centro, con 10**, igual que con el orden de la página.
2. **R, I, C y D.** I, C y D llegan con ${d=1}$ y no son finales, así que pasan de largo las líneas 8 y 9 y los valora la rama de MIN, líneas 16–21. R lo recorre DECIDIR-CON-CORTE, líneas 1–6.
:::

**Trazar el árbol de resultados por tu cuenta.**

**Piensa: ¿qué cambia en la decisión si cambia el orden de las jugadas, o una sola evaluación?**

Antes de empezar, anota tu apuesta: ¿cuál de las dos crees que puede cambiar la jugada? El ejercicio lo pone a prueba en tres pasos: un empate, una variante y un costo.

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-corte title="Traza el árbol de resultados con un empate y otra evaluación"}
Usa el árbol de resultados, sus finales en ${100\cdot U}$ y las $\mathrm{EVAL}$ de @jue-c3-t-eval. Dentro de I, C y D el orden no cambia, y la línea 5 sigue con ${>}$ estricto.

1. **Un empate en la raíz.** Cambia ${\mathrm{EVAL}(\text{C})=60}$ en vez de 20. Con ${d=1}$ y el orden izq, centro, der, ¿qué juega, y con qué valor? Escribe después la traza de DECIDIR-CON-CORTE(R, 1) con R al revés: der, centro, izq. ¿Qué jugada devuelve, con qué valor, y en qué filas cambia mejor_jugada?
2. **Otra evaluación.** Vuelve a ${\mathrm{EVAL}(\text{C})=20}$ y cambia ${\mathrm{EVAL}(\text{I})=0}$ en vez de 60: una evaluación menos optimista frente a la captura ix. ¿Qué juega con ${d=1}$, ${d=2}$ y ${d=3}$?
3. **El costo.** ¿Cuántos nodos genera con ${d=1}$, 2 y 3 en la variante del inciso 2? ¿Y con la evaluación del inciso 1 y R al revés? Explica por qué.
:::

::: hint {#jue-c3-pista-final-corte-1 of="jue-c3-ej-final-corte" title="Pista 1 · Qué se mueve de lugar"}
Con ${d=1}$, ¿cuánto valen I, C y D con ${\mathrm{EVAL}(\text{C})=60}$? Con R al revés, ¿qué compara la línea 5 cuando un hijo regresa con el mismo número que mejor_valor? Para el inciso 2: con cada $d$, ¿qué nodos llegan con ${d=0}$ sin ser finales?
:::

::: hint {#jue-c3-pista-final-corte-2 of="jue-c3-ej-final-corte" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿Cada nodo que contaste está arriba de la línea de corte o justo en ella? ¿Cada fila de R compara su $w$ con el mejor_valor de la fila anterior de R, y no con el último $w$?
:::

::: answer {#jue-c3-resp-final-corte of="jue-c3-ej-final-corte" title="Respuesta · El empate, la variante y el costo"}
**1. El empate.** Con ${d=1}$, I y C valen 60 y D vale 10. Con el orden de la página, izq llega primero con 60; en la fila de C, ${60>60}$ es falso, y juega **izq, con 60**. Con R al revés:

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 4–⁠5 · R | 10 | 10 (D) | der |
| 3 | 4–⁠5 · R | 60 | 60 (C) | centro |
| 4 | 4–⁠5 · R | 60 | 60 (I) | centro |
| 5 | 6 · R | 60 |  | centro |

mejor_jugada pasa de ninguna a **der** en la fila 2 ${(10>-\infty)}$ y a **centro** en la fila 3 ${(60>10)}$. En la fila 4, ${60>60}$ es falso. Devuelve **centro, con 60**. Con un empate, el orden decide la jugada: con ${>}$ estricto se queda la primera que alcanzó el valor. Aquí el orden salva a MAX por suerte: izq vale ${-100}$ y centro, 0.

**2. La variante.** Con ${d=1}$, I vale 0: juega **centro, con 20**. Con ${d=2}$, I ya no es nodo de corte, porque sus hijos son finales: juega centro, con 10, como antes. Con ${d=3}$ no se evalúa ningún nodo interno: juega centro, con 0. **Una sola evaluación cambia la jugada**, pero solo con la profundidad en que ese nodo es de corte.

**3. El costo.** **4, 11 y 15** nodos en los dos casos. Sin poda, se genera todo lo que está arriba de la línea de corte, y eso no depende del orden ni de los números. Con poda, el orden sí importaría.
:::

**Punto de control:** deberías poder

- calcular a mano el valor con corte de cada jugada a profundidad 1, 2 y 3 en una posición de peones de 4×4, y decir por qué puede no coincidir con el valor exacto;
- escribir DECIDIR-CON-CORTE y MINIMAX-CON-CORTE de memoria, y decir qué recibe y qué genera;
- decir qué línea valora cada nodo: la 8, la 9 o ninguna;
- explicar por qué termina aunque el juego no termine, y qué número de su salida es seguro.

> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Alfa-beta | $V$ en la raíz; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | **Minimax con corte (estás aquí)** | **Valor con corte; no garantiza $V$. Con todos los finales, da $M\cdot V$** |

## Lo que hay que llevarse

- **El 4×4 es el mismo juego con más casillas:** cambian $S$ y $s_0$, y ahora sí hace falta guardar el turno. Su árbol tiene 4 197 973 nodos: ya no se recorre a mano.
- **Si el árbol no cabe, se corta** cuando la profundidad que queda llega a ${d=0}$, y se usa ${\mathrm{EVAL}=10\cdot\text{material}+\text{avance}}$ en ese nodo de corte. $\mathrm{EVAL}$ estima ${100\cdot V}$. Los finales valen ${100\cdot U}$, que gana a cualquier estimación (nunca pasa de 36).
- **El valor con corte es el minimax de $\mathrm{EVAL}$, no el del juego.** En la posición de la clase, la captura vale **13** a profundidad 1 y **0** a profundidad 2; $\text{d2}\textbf{-}\text{d3}$ vale **100** a profundidad 3, y es la que gana.
- **DECIDIR-CON-CORTE es DECIDIR y MINIMAX con una línea más, la 9.** La 8 va antes: un final se reconoce aunque llegue con ${d=0}$. Termina siempre, porque $d$ baja en cada llamada.
- **Solo los ${\pm100}$ son seguros** mientras la búsqueda no llegue a todos los finales. En el árbol de resultados, ${d=1}$ cae en la trampa de izq (60, y vale ${-100}$); ${d=2}$ ya juega centro, con 10; ${d=3}$ llega a todos los finales y devuelve $100\,V$, que aquí es 0. Con ${d=1}$, 2 y 3 genera **4, 11 y 15** nodos.
- **Cuesta $O(b^d)$:** en la posición de la clase, **4, 12 y 33** nodos con ${d=1}$, 2 y 3.
- **$\mathrm{EVAL}$ es un modelo:** sus pesos expresan una preferencia y dejan cosas fuera, como las capturas que vienen.

Adivinar esas capturas con rasgos es frágil; la siguiente página las mira, y elige $d$ según el reloj. Continúa con [[jugar-contra-el-reloj|Hasta dónde mirar]].
