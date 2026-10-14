---
id: cortar-y-evaluar
title: Cortar y evaluar a mano
nav_title: Cortar y evaluar a mano
summary: "Cuando no se puede llegar a los finales, se corta la búsqueda a cierta profundidad y se estima cada posición con una función de evaluación. A mano, en una posición de 4×4: a profundidad 1 se elige una jugada que pierde."
status: ready
estimated_time: 30m
tags: [juegos, busqueda-adversarial, evaluacion]
---

# Cortar y evaluar a mano

**¿Qué hacemos si no podemos llegar a los finales?**

Al terminar tendrás:

- una **función de evaluación** para peones, calculada a mano en tres
  tableros de 4×4;
- el **minimax con corte** de las tres jugadas de una posición, a
  profundidad 1 y 2, y una de sus ramas a profundidad 3;
- un caso concreto en el que **cortar se equivoca**: a profundidad 1 se
  elige la jugada que pierde.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4. Blancas
> (B) empieza con cuatro peones en la fila 1, y Negras (N) con cuatro en la
> 4. Empiezan Blancas. Un peón avanza una casilla si está vacía o
> captura en diagonal hacia delante. Gana quien llega a la fila del rival,
> captura todo o deja al rival sin jugada: ${U=+1}$ si gana Blancas y ${U=-1}$
> si gana Negras.

> **Las piezas que usa esta página.** Las siete de
> [[escribir-el-juego|Escribir el juego]]: $S$ y $s_0$ (@jue-c1-estado),
> $S_F$ (@jue-c1-finales), $\mathrm{Pl}$ (@jue-c1-pl), $A$
> (@jue-c1-acciones), $T$ (@jue-c1-transicion) y $U$ (@jue-c1-utilidad).
> Y el valor $V$ de [[minimax|Minimax a mano]] (@jue-c2-valor).

> **Supuestos de esta página.** Los mismos de
> [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin
> azar, todo a la vista, toda partida termina y suma cero. Uno nuevo: **no
> nos alcanza el tiempo para llegar a los finales**.

## 1 · Pasar el mismo juego a un tablero más grande

**Piensa: de las siete piezas de hexapawn, ¿cuáles cambian si el tablero
pasa a 4×4?**

Casi ninguna. Las reglas son las de la clase 1 con una fila y una columna
más:

- **Cambian $S$ y $s_0$.** Un estado sigue siendo un par (tablero, turno),
  ahora con 16 casillas. Al empezar hay cuatro peones por lado y mueve
  Blancas.
- **Las reglas que definen $S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$ no
  cambian**: se llega a la fila del rival, se captura todo o se deja al
  rival sin jugada; $\mathrm{Pl}$ lee el turno guardado; ${U=\pm1}$.

Hay un detalle que la clase 1 dejó anunciado. En el 3×3, el turno se
podía deducir del tablero, aunque lo guardábamos por principio. **En el 4×4
ya no:** la computadora encontró 2925 tableros que se alcanzan con los dos
turnos. Guardar el turno en el estado era necesario.

::: table {#jue-c3-octapawn-inicio title="El tablero de 4×4 al empezar"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | N | N |
| **3** | · | · | · | · |
| **2** | · | · | · | · |
| **1** | B | B | B | B |
:::

::: exercise {#jue-c3-ej-inicio title="Escribe las jugadas tras dos avances"}
Desde el inicio se jugó $\text{b1}\textbf{-}\text{b2}$ y
$\text{c4}\textbf{-}\text{c3}$. Mueven Blancas:

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
Para cada peón blanco, ¿qué casilla tiene enfrente y cuáles en diagonal
hacia delante? ¿Quién ocupa cada una?
:::

::: answer {#jue-c3-resp-inicio of="jue-c3-ej-inicio"}
1. Cinco: $\text{a1}\textbf{-}\text{a2}$, $\text{b2}\textbf{-}\text{b3}$,
   $\text{b2}\textbf{x}\text{c3}$, $\text{c1}\textbf{-}\text{c2}$ y
   $\text{d1}\textbf{-}\text{d2}$.
2. Una: $\text{b2}\textbf{x}\text{c3}$. El peón de b2 tiene al de c3 en
   una diagonal de enfrente. Los demás peones blancos no tienen ningún peón
   negro en diagonal: solo avanzan.
:::

## 2 · Medir cuánto crece el árbol

**Piensa: si el tablero pasa de 3×3 a 4×4, ¿el árbol crece al doble, al
triple o más?**

Mucho más. La computadora contó los dos árboles completos:

::: table {#jue-c3-crecimiento title="Del tablero de 3×3 al ajedrez"}
| Tablero | Nodos | Estados |
|---|---:|---:|
| 3×3 | 252 | 135 |
| 4×4 | 4 197 973 | 20 286 |
| Ajedrez | — | ${\approx10^{44}}$ |
:::

**Nodos** cuenta los del árbol completo, que no junta estados repetidos:
cada nodo guarda el camino por el que llegó, así que un mismo tablero con el
mismo turno aparece una vez por cada orden de jugadas que lo alcanza.
**Estados** cuenta los del grafo de la clase 1, que guarda cada uno una sola
vez.

Con juego perfecto, en el 3×3 (hexapawn) gana
el segundo y en el 4×4 gana el primero. En el ajedrez nadie lo sabe.

::: exercise {#jue-c3-ej-crecimiento title="Compara los dos árboles"}
1. ¿Cuántas veces más nodos tiene el árbol del 4×4 que el de hexapawn?
2. ¿Cuántos nodos hay por cada estado, en promedio, en cada tablero? ¿En
   cuál se repiten más los estados?
:::

::: hint {#jue-c3-pista-crecimiento-1 of="jue-c3-ej-crecimiento" title="Qué es un nodo"}
Divide los nodos entre los estados de cada fila de la tabla
@jue-c3-crecimiento.
:::

::: answer {#jue-c3-resp-crecimiento of="jue-c3-ej-crecimiento"}
1. ${4\,197\,973/252\approx16\,659}$: **más de 16 000 veces**, por una fila y
   una columna más.
2. En el 3×3, ${252/135\approx1.9}$ nodos por estado; en el 4×4,
   ${4\,197\,973/20\,286\approx207}$. Se repiten mucho más en el 4×4: con
   más jugadas hay muchos más órdenes distintos que llegan al mismo estado.
:::

El 4×4 todavía lo resuelve una computadora, pero ya no una persona con
lápiz.

El ajedrez está en otra escala. Tromp y Österlund estimaron en 2021 que
tiene cerca de ${4.8\times10^{44}}$ posiciones legales, y Claude Shannon
estimó en 1950 que hay unas $10^{120}$ partidas. **Ni recordando cada
posición cabe**: no hay memoria para $10^{44}$ estados, y menos tiempo para
recorrerlos.

## 3 · Plantear el problema cuando no cabe

**Piensa: si no se puede llegar a los finales, ¿qué puede pedirse?**

Algo más modesto que la jugada óptima:

> **El problema de esta clase.**
>
> **Dado:** el juego, un estado $s$ donde mueve MAX y un presupuesto: cuántas
> jugadas hacia delante se pueden mirar.
>
> **Encontrar:** una jugada para $s$, lo mejor posible con ese presupuesto.

::: exercise {#jue-c3-ej-problema title="Compara con el problema de la unidad"}
Pon este problema junto al de la unidad (@jue-c1-problema).

1. ¿Qué dato nuevo recibe?
2. ¿Qué pedía el de la unidad que éste ya no pide, y por qué?
:::

::: hint {#jue-c3-pista-problema-1 of="jue-c3-ej-problema" title="Renglón por renglón"}
Compara primero los dos «Dado» y luego los dos «Encontrar». ¿Qué hace
falta para saber qué jugada asegura la mayor utilidad?
:::

::: answer {#jue-c3-resp-problema of="jue-c3-ej-problema"}
1. El **presupuesto**: cuántas jugadas se pueden mirar.
2. La jugada que **asegura** la mayor utilidad. Para saber cuál es hay que
   llegar a los finales, y eso es justo lo que ya no cabe.
:::

La respuesta ya no viene con garantía. Esta página muestra qué tan bien, y
qué tan mal, puede salir.

## 4 · Cortar la búsqueda y estimar

**Piensa: si solo te alcanza para ver dos jugadas hacia delante, ¿qué haces
con las posiciones donde te detienes?**

Una persona que juega ajedrez no calcula hasta el final. Mira unas jugadas,
se detiene y **juzga** la posición: «tengo un peón de más». Minimax con
corte hace lo mismo, con dos cambios:

1. Lleva la cuenta de **la profundidad que queda**, $d$: cuántas jugadas
   más, contando las de los dos jugadores, puede mirar. En la raíz, $d$ es
   el presupuesto; cada jugada la baja en uno.
2. Donde llega a ${d=0}$, en lugar de la utilidad $U(s)$, que no conoce, usa
   una **estimación** $\mathrm{EVAL}(s)$.

Ojo con la letra: $d$, en cursiva, es siempre esta profundidad. No tiene
nada que ver con la columna d del tablero, la de
$\text{d2}\textbf{-}\text{d3}$.

::: definition {#jue-c3-evaluacion title="Función de evaluación"}
Una **función de evaluación** $\mathrm{EVAL}(s)$ asigna a un estado $s$ un
número que estima qué tan bueno es $s$ para MAX. Se calcula **mirando solo
$s$**, sin buscar hacia delante.

**Qué significa:** es un juicio rápido, como «tengo un peón de más».

**Qué no es:** no es $V(s)$. No viene del reglamento: la escribimos
nosotros, y puede equivocarse.
:::

Los finales que aparezcan antes de llegar a ${d=0}$, o justo en ${d=0}$, se
siguen valorando con su utilidad: ahí no hay nada que estimar.

::: exercise {#jue-c3-ej-presupuesto title="Sigue la profundidad que queda"}
El presupuesto es ${d=3}$ en la raíz, donde mueve Blancas.

1. ¿Cuánto vale $d$ tras la primera jugada de Blancas, tras la respuesta
   de Negras y tras la segunda jugada de Blancas?
2. ¿En cuál de esos niveles se usa $\mathrm{EVAL}$?
3. Si la primera jugada de Blancas llegara a la fila 4, ¿con qué número
   se valoraría ese nodo?
:::

::: hint {#jue-c3-pista-presupuesto-1 of="jue-c3-ej-presupuesto" title="Un renglón por jugada"}
Escribe la raíz con su $d$ y baja un renglón por cada jugada. ¿Importa
de quién es la jugada para lo que le pasa a $d$?
:::

::: answer {#jue-c3-resp-presupuesto of="jue-c3-ej-presupuesto"}
1. ${d=2}$, luego ${d=1}$, luego ${d=0}$: cada jugada la baja en uno, sea de
   quien sea.
2. Tras la segunda jugada de Blancas, donde ${d=0}$.
3. Con su utilidad, ${U=+1}$ (en la escala de la sección 6, 100): ese nodo
   es un final, y no se estima aunque le queden dos jugadas por mirar.
:::

## 5 · Escribir una evaluación para los peones

**Piensa: mirando solo un tablero de peones, ¿qué te dice quién va
mejor?**

Dos cosas saltan a la vista: **cuántos peones** tiene cada uno y **cuánto
han avanzado**. Un peón avanzado está más cerca de la fila del rival, que
es una forma de ganar. El avance de un peón blanco es cuántas filas subió
desde la fila 1; el de uno negro, cuántas bajó desde la fila 4.

$$\mathrm{EVAL}(s)=10\cdot\text{material}+\text{avance},$$

donde **material** es peones blancos menos peones negros, y **avance** es el
avance blanco menos el avance negro.

Los dos rasgos se restan porque lo que es bueno para Negras es malo para
Blancas: la evaluación, igual que $U$, se mide en puntos de MAX.

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

::: exercise {#jue-c3-ej-eval title="Calcula dos evaluaciones"}
Desde el inicio se jugó $\text{b1}\textbf{-}\text{b2}$,
$\text{c4}\textbf{-}\text{c3}$ y $\text{b2}\textbf{x}\text{c3}$, la
captura del primer ejercicio. Ahora mueven Negras:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | N |
| **3** | · | · | B | · |
| **2** | · | · | · | · |
| **1** | B | · | B | B |

1. Calcula $\mathrm{EVAL}(s_0)$, el tablero de 4×4 al empezar.
2. Calcula el $\mathrm{EVAL}$ del tablero de arriba. ¿Cambiaría si
   movieran Blancas?
:::

::: hint {#jue-c3-pista-eval-1 of="jue-c3-ej-eval" title="Dos rasgos"}
Para cada lado, ¿cuántos peones hay y cuántas filas avanzó cada uno desde
su fila de salida? ¿Qué parte de la fórmula mira el turno?
:::

::: answer {#jue-c3-resp-eval of="jue-c3-ej-eval"}
1. Cuatro peones por lado, ninguno avanzado:
   ${\mathrm{EVAL}(s_0)=10\cdot0+0=0}$.
2. Blancas tiene a1, c1, d1 y c3: **4** peones, con avance 2 (el de c3).
   Negras tiene a4, b4 y d4: **3**, con avance 0. Entonces
   ${\mathrm{EVAL}=10\cdot1+2=12}$. No cambiaría: $\mathrm{EVAL}$ mira solo
   el tablero, no a quién le toca.
:::

## 6 · Pesar los finales más que cualquier estimación

**Piensa: si una victoria valiera ${+1}$ y un peón de más valiera $10$,
¿qué preferiría el algoritmo?**

El peón. Por eso hay que poner $U$ en la **misma escala** que
$\mathrm{EVAL}$. En los finales usamos ${100\cdot U(s)}$: **100** si gana
Blancas y **${-100}$** si gana Negras.

Multiplicar por 100 solo cambia la escala; el orden entre finales es el
mismo que con $U$. Y 100 es mayor que cualquier evaluación: la computadora
comprobó que, en las posiciones alcanzables del 4×4 que no son finales,
$\mathrm{EVAL}$ nunca pasa de 36 en valor absoluto.

::: remark {#jue-c3-orden-finales title="La evaluación tiene que respetar el orden de los finales"}
Una función de evaluación puede equivocarse en las posiciones sin terminar,
pero no debe contradecir lo que ya se sabe: **ganar vale más que cualquier
estimación, y perder, menos**. Si no lo cumple, el programa puede preferir
una posición «buena» a una victoria segura.
:::

::: exercise {#jue-c3-ej-escala title="Encuentra una escala que no alcanza"}
Alguien propone usar ${30\cdot U}$ en los finales en vez de ${100\cdot U}$.
¿Respeta el orden de los finales? Usa la cifra de arriba.
:::

::: hint {#jue-c3-pista-escala-1 of="jue-c3-ej-escala" title="Compara dos números"}
¿Cuánto puede valer, como mucho, la $\mathrm{EVAL}$ de una posición sin
terminar? ¿Y una victoria con esa escala?
:::

::: answer {#jue-c3-resp-escala of="jue-c3-ej-escala"}
No. Una posición sin terminar puede tener ${\mathrm{EVAL}=36}$, más que los
30 de una victoria. El programa podría preferir esa posición a ganar. Con
100, ninguna estimación alcanza a un final.
:::

## 7 · Profundidad 1: mirar una jugada y evaluar

**Piensa: si Blancas solo mira su propia jugada, ¿qué le conviene más,
avanzar o capturar?**

Lo que diga $\mathrm{EVAL}$ justo después. **Estamos aquí:** la posición de
la clase, con ${\mathrm{EVAL}=1}$. Blancas tiene tres jugadas:
$\text{a1}\textbf{-}\text{a2}$, $\text{d2}\textbf{-}\text{d3}$ y
$\text{d2}\textbf{x}\text{c3}$. El peón de c2 no puede moverse: tiene c3
enfrente y nada que capturar en b3 ni en d3.

Con ${d=1}$ en la raíz, cada jugada de Blancas deja ${d=0}$: sin esperar la
respuesta de Negras, se evalúa.

Esos tres hijos son **nodos de corte**: estados no finales a los que se
llega con ${d=0}$. Ahí la búsqueda se detiene y estima. En las figuras llevan
el borde punteado de la clase 1, el de un estado que existe pero no se
expande.

::: exercise {#jue-c3-ej-prof-1 title="Calcula la jugada a profundidad 1"}
1. Calcula $\mathrm{EVAL}$ después de cada una de las tres jugadas.
2. ¿Qué jugada elige Blancas a profundidad 1?
:::

::: hint {#jue-c3-pista-prof-1-1 of="jue-c3-ej-prof-1" title="Rasgo por rasgo"}
En cada jugada, ¿cambia el número de peones de alguno de los dos lados?
¿Cuántas filas sube el peón que se mueve?
:::

::: answer {#jue-c3-resp-prof-1 of="jue-c3-ej-prof-1"}
1. $\text{a1}\textbf{-}\text{a2}$ y $\text{d2}\textbf{-}\text{d3}$:
   ${10\cdot0+(3-1)=2}$. $\text{d2}\textbf{x}\text{c3}$: quedan 3 peones
   blancos contra 2 negros, con avance $3$ contra $0$:
   ${10\cdot1+(3-0)=13}$.
2. **$\text{d2}\textbf{x}\text{c3}$**, con 13: gana un peón.
:::

::: figure {#jue-c3-fig-prof-1 title="Profundidad 1: la captura parece ganar un peón"}
![La posición de la clase arriba, donde mueve Blancas. Sus tres jugadas llevan a nodos de corte, con borde punteado porque ahí la búsqueda se detiene: a1-a2 da EVAL = 2; d2-d3 da EVAL = 2; d2xc3 da EVAL = 13. Blancas toma el máximo, 13: la flecha de d2xc3 va resaltada](../_assets/jue-c3-corte-prof-1.svg)
:::

A profundidad 1, Blancas **captura**. Parece obvio: un peón de más.

## 8 · Profundidad 2: mirar también la respuesta

**Piensa: si Blancas mira también la respuesta de Negras, ¿cuál de sus
respuestas supone?**

La peor para Blancas. Con ${d=2}$ en la raíz, miramos la jugada de Blancas,
**todas las respuestas de Negras**, y evaluamos. Negras es MIN: de sus
respuestas, elige la de menor $\mathrm{EVAL}$.

- **$\text{a1}\textbf{-}\text{a2}$.** Negras puede responder
  $\text{c3}\textbf{x}\text{d2}$ (${-10}$), $\text{a4}\textbf{-}\text{a3}$
  (1) o $\text{b4}\textbf{-}\text{b3}$ (1). Lo peor para Blancas: ${-10}$.
- **$\text{d2}\textbf{-}\text{d3}$.** El peón de c3 queda bloqueado por c2 y
  sin nada que capturar. Negras puede responder
  $\text{a4}\textbf{-}\text{a3}$ o $\text{b4}\textbf{-}\text{b3}$, las dos
  con 1. Lo peor para Blancas: 1.
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
3. ¿Cuánto vale la captura a profundidad 2? ¿Qué jugada elige Blancas
   ahora?
:::

::: hint {#jue-c3-pista-prof-2-1 of="jue-c3-ej-prof-2" title="Peón por peón"}
Recorre los peones negros uno por uno. Para cada uno, ¿qué casilla tiene
enfrente, qué casillas tiene en sus dos diagonales hacia abajo, y quién
ocupa cada una?
:::

::: answer {#jue-c3-resp-prof-2 of="jue-c3-ej-prof-2"}
1. $\text{a4}\textbf{-}\text{a3}$, $\text{b4}\textbf{-}\text{b3}$ y
   **$\text{b4}\textbf{x}\text{c3}$**: el peón de b4 captura en diagonal.
2. Tras un avance: ${10\cdot(3-2)+(3-1)=12}$. Tras
   $\text{b4}\textbf{x}\text{c3}$ quedan dos peones por lado, con avance 1
   cada uno: ${\mathrm{EVAL}=0}$.
3. Negras recaptura, así que la captura vale **0**. Blancas compara ${-10}$,
   1 y 0 y elige **$\text{d2}\textbf{-}\text{d3}$**.
:::

::: figure {#jue-c3-fig-prof-2 title="Profundidad 2: Negras recaptura y Blancas elige d2-d3"}
![La posición de la clase, sus tres jugadas y todas las respuestas de Negras, que son nodos de corte con su EVAL. Tras a1-a2, Negras puede c3xd2 (−10), a4-a3 (1), b4-b3 (1): el mínimo es −10. Tras d2-d3, Negras puede a4-a3 (1), b4-b3 (1): el mínimo es 1. Tras d2xc3, Negras puede a4-a3 (12), b4-b3 (12), b4xc3 (0): el mínimo es 0. Blancas toma el máximo, 1, con d2-d3: las flechas resaltadas](../_assets/jue-c3-corte-prof-2.svg)
:::

**Mirar una jugada más cambió la decisión.** La captura ganaba un peón,
pero Negras lo recupera enseguida.

## 9 · Profundidad 3: mirar la segunda jugada de Blancas

**Piensa: a profundidad 3, ¿dónde quedan los nodos de corte?**

Tras la segunda jugada de Blancas: se mira jugada de Blancas, respuesta de
Negras y otra jugada de Blancas. El árbol completo ya tiene 33 nodos. Aquí haces a mano
solo la rama de $\text{d2}\textbf{-}\text{d3}$, la que eligió la
profundidad 2.

::: exercise {#jue-c3-ej-prof-3 title="Calcula la rama d2-d3 a profundidad 3"}
Tras $\text{d2}\textbf{-}\text{d3}$, el tablero es éste y mueven Negras,
con ${d=2}$:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | B |
| **2** | · | · | B | · |
| **1** | B | · | · | · |

1. Escribe las respuestas de Negras y, bajo cada una, todas las jugadas
   de Blancas.
2. Valora cada hoja.
3. ¿Cuánto vale $\text{d2}\textbf{-}\text{d3}$ a profundidad 3? ¿Cuántos
   nodos tiene la rama, contando el de $\text{d2}\textbf{-}\text{d3}$?
:::

::: hint {#jue-c3-pista-prof-3-1 of="jue-c3-ej-prof-3" title="Dos niveles"}
Primero las respuestas de Negras; luego, bajo cada una, los peones
blancos uno por uno, con su avance y sus dos diagonales. Antes de aplicar
$\mathrm{EVAL}$ a una hoja, ¿qué hay que revisar?
:::

::: answer {#jue-c3-resp-prof-3 of="jue-c3-ej-prof-3"}
1. Negras solo tiene $\text{a4}\textbf{-}\text{a3}$ y
   $\text{b4}\textbf{-}\text{b3}$. Tras $\text{a4}\textbf{-}\text{a3}$,
   Blancas tiene $\text{a1}\textbf{-}\text{a2}$ y
   $\text{d3}\textbf{-}\text{d4}$. Tras $\text{b4}\textbf{-}\text{b3}$,
   tiene además $\text{c2}\textbf{x}\text{b3}$.
2. $\text{d3}\textbf{-}\text{d4}$ llega a la fila 4: es un **final**, vale
   100 y no se estima. $\text{a1}\textbf{-}\text{a2}$ da 2 en los dos casos;
   $\text{c2}\textbf{x}\text{b3}$ da 13.
3. Blancas toma 100 bajo cada respuesta, y Negras, el mínimo de 100 y 100:
   la rama vale **100**. Tiene **8** nodos: 1 + 2 respuestas + 2 + 3
   jugadas.
:::

::: figure {#jue-c3-fig-prof-3 title="Profundidad 3: d3-d4 llega a la fila 4 y d2-d3 vale 100"}
![Solo la rama d2-d3 del árbol con d = 3 en la raíz. Tras d2-d3 mueve Negras, que tiene 2 respuestas. Tras a4-a3, Blancas puede a1-a2 (2, EVAL) o d3-d4 (100, final: gana Blancas): el máximo es 100. Tras b4-b3, Blancas puede a1-a2 (2, EVAL), c2xb3 (13, EVAL) o d3-d4 (100, final: gana Blancas): el máximo es 100. Negras toma el mínimo, 100: d2-d3 vale 100. La rama tiene 8 nodos](../_assets/jue-c3-corte-prof-3.svg)
:::

A profundidad 3 el algoritmo ya ve la victoria. Hagas lo que hagas Negras,
Blancas llega a la fila 4.

## 10 · Comparar con el valor exacto

**Piensa: ¿alguna de estas profundidades garantiza la jugada correcta?**

Ninguna lo garantiza en general; aquí la 3 sí, porque su 100 sale de
finales: lo verás en la página siguiente.

Para saber cuál es la correcta,
la computadora recorrió el árbol del 4×4 hasta los finales: eso da el
**valor exacto**, $V$. Las otras dos ramas de la profundidad 3 también
las hizo la computadora. En la tabla, P1, P2 y P3 son las profundidades 1, 2 y 3, y la
última columna pone $V$ por 100, en la escala de las demás.

::: table {#jue-c3-profundidades title="Las tres jugadas a profundidad 1, 2 y 3, y su valor exacto"}
| Jugada | P1 | P2 | P3 | ${100\cdot V}$ |
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
En cada columna de profundidad, ¿qué jugada tiene el máximo? ¿Cuánto vale
esa jugada en la última columna?
:::

::: answer {#jue-c3-resp-exacto of="jue-c3-ej-exacto"}
1. Con profundidad 2 y 3: las dos eligen $\text{d2}\textbf{-}\text{d3}$,
   que vale 100.
2. Con profundidad 1: elige $\text{d2}\textbf{x}\text{c3}$ con 13, y esa
   jugada vale ${-100}$. La sobreestima en **113 puntos**, ${13-(-100)}$.
   **Capturar pierde y $\text{d2}\textbf{-}\text{d3}$ gana.**
:::

La profundidad 2 acierta sin ver la victoria: solo vio que capturar salía
mal. El número que calcula la
búsqueda cortada tiene nombre propio.

::: definition {#jue-c3-valor-con-corte title="Valor con corte"}
El **valor con corte** de un estado, cuando quedan $d$ jugadas por mirar,
es el minimax del árbol cortado a $d$ jugadas, con $\mathrm{EVAL}$ en los
nodos de corte y ${100\cdot U}$ en los finales.

**Qué significa:** es **el minimax de la evaluación**.

**Qué no es:** no es $V(s)$, el valor del juego, y puede equivocarse.
:::

**Punto de control:** deberías poder calcular a mano el valor con corte de
cada jugada a profundidad 1, 2 y 3 en una posición de peones de 4×4, y
decir por qué puede no coincidir con el valor exacto.

## Lo que hay que llevarse

- El 4×4 es el mismo juego con más casillas: cambian $S$ y $s_0$, y ahora
  sí hace falta guardar el turno. Su árbol tiene 4 197 973 nodos: ya no se
  recorre a mano.
- Si el árbol no cabe, se corta cuando la profundidad que queda llega a
  ${d=0}$ y se usa ${\mathrm{EVAL}=10\cdot\text{material}+\text{avance}}$ en ese
  nodo de corte. Los finales valen ${100\cdot U}$, que gana a cualquier
  estimación (nunca pasa de 36).
- El valor con corte es el minimax de $\mathrm{EVAL}$, no el del juego. En
  la posición de la clase, la captura vale **13** a profundidad 1 y **0** a
  profundidad 2; $\text{d2}\textbf{-}\text{d3}$ vale **100** a profundidad
  3, y es la que gana.

Continúa con [[minimax-con-corte|minimax con corte como algoritmo]].
