---
id: cortar-y-evaluar
title: Cortar y evaluar
nav_title: Cortar y evaluar
summary: "Cuando no se puede llegar a los finales, se corta la búsqueda a cierta profundidad y se estima cada posición con una función de evaluación. El valor que sale ya no es el del juego."
status: ready
estimated_time: 30m
tags: [juegos, busqueda-adversarial, evaluacion, modelado]
---

# Cortar y evaluar

**¿Qué hacemos si no podemos llegar a los finales?**

Al terminar tendrás **minimax con corte**: un algoritmo que mira unas pocas
jugadas hacia delante y estima las posiciones donde se detiene. Lo calcularás
a mano en una posición de peones y verás que puede equivocarse.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Empiezan Blancas. Un peón avanza una casilla si está vacía o
> captura en diagonal hacia delante. Gana quien llega a la fila del rival,
> captura todo o deja al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$
> si gana Negras.

> **Cambio respecto de las clases 1 y 2:** dejamos $10-k$. En el 4×4 solo
> nos importa quién gana, y al cortar la búsqueda no sabemos cuántas jugadas
> faltan; usamos $U=\pm1$, y el estado ya no necesita guardar $k$.

## 1 · Medir cuánto crece el árbol

**Piensa: si el tablero pasa de 3×3 a 4×4, ¿el árbol crece al doble, al
triple o más?**

Este es el tablero de 4×4 al empezar. Se le llama a veces *octapawn*, por sus
ocho peones.

::: table {#jue-c3-octapawn-inicio title="El tablero de 4×4 al empezar"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | N | N |
| **3** | · | · | · | · |
| **2** | · | · | · | · |
| **1** | B | B | B | B |
:::

Con una fila y una columna más, el árbol no crece al doble: crece miles de
veces. La computadora contó los dos tableros completos:

::: table {#jue-c3-crecimiento title="Del tablero de 3×3 al ajedrez"}
| Juego | Nodos del árbol | Situaciones distintas | Con juego perfecto |
|---|---:|---:|---|
| Hexapawn, 3×3 | 252 | 135 | Gana el segundo jugador |
| Peones en 4×4 | 4 197 973 | 20 286 | Gana el primero |
| Ajedrez | — | del orden de $10^{44}$ | Nadie lo sabe |
:::

El 4×4 todavía lo resuelve una computadora, pero ya no una persona con
lápiz. Con $U=\pm1$, el valor exacto de la posición inicial es $+1$:
Blancas gana si juega bien.

El ajedrez está en otra escala. Tromp y Österlund estimaron en
2021 que tiene cerca de $4.8\times10^{44}$ posiciones legales. Claude Shannon
estimó en 1950 que hay unas $10^{120}$ partidas. **Ni recordando cada posición
cabe**: no hay memoria para $10^{44}$ estados, y menos tiempo para recorrerlos.

## 2 · Cortar la búsqueda y estimar

**Piensa: si solo te alcanza para ver dos jugadas hacia delante, ¿qué haces
con las posiciones donde te detienes?**

Una persona que juega ajedrez no calcula hasta el final. Mira unas jugadas,
se detiene y **juzga** la posición: «tengo un peón de más», «mi rey está
expuesto». Minimax con corte hace lo mismo, con dos cambios:

1. Lleva la cuenta de **la profundidad que queda**, $d$: cuántas jugadas más,
   contando las de los dos jugadores, puede mirar desde el estado actual. En
   la raíz, $d$ es la profundidad de toda la búsqueda; cada jugada la baja en
   uno, y al llegar a $d=0$ deja de bajar.
2. En las posiciones donde se detiene, en lugar de la utilidad $U(s)$, que
   no conoce, usa una **estimación** $\mathrm{EVAL}(s)$.

En toda la página, $d$ significa solo eso: la profundidad que queda.

::: definition {#jue-c3-evaluacion title="Función de evaluación"}
Una **función de evaluación** $\mathrm{EVAL}(s)$ asigna a cualquier estado
$s$, terminado o no, un número que estima qué tan bueno es $s$ para MAX. Se
calcula **mirando solo $s$**, sin buscar hacia delante.
:::

Un **nodo de corte** es un estado no final al que se llega con $d=0$: ahí
la búsqueda se detiene y estima. Los finales que aparezcan antes del corte
se siguen valorando con su utilidad real.

## 3 · Escribir una evaluación para los peones

**Piensa: mirando solo un tablero de peones, ¿qué te dice quién va mejor?**

Dos cosas saltan a la vista: **cuántos peones** tiene cada uno y **cuánto han
avanzado**. Un peón avanzado está más cerca de la fila del rival, que es una
forma de ganar.

Para medir el avance, el de un peón blanco es cuántas filas subió desde la
fila 1; el de un peón negro, cuántas bajó desde la fila 4. La evaluación de
esta clase es:

$$\mathrm{EVAL}(s)=10\cdot(\text{peones blancos}-\text{peones negros})+(\text{avance blanco}-\text{avance negro}).$$

Los dos rasgos se restan porque lo que es bueno para Negras es malo para
Blancas: la evaluación, igual que $U$, se mide en puntos de MAX.

Esta es la posición que usaremos en toda la clase. Mueven Blancas.

::: table {#jue-c3-horizonte title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

Calculemos su evaluación paso a paso:

| | Blancas | Negras |
|---|---|---|
| Peones | a1, c2, d2: **3** | a4, b4, c3: **3** |
| Avance | $0+1+1=$ **2** | $0+0+1=$ **1** |

$$\mathrm{EVAL}=10\cdot(3-3)+(2-1)=1.$$

Van parejos en peones, y Blancas está un poco más avanzada.

### Los finales pesan más que cualquier estimación

En un final no hace falta estimar: sabemos quién ganó. Pero hay que poner $U$
en la **misma escala** que $\mathrm{EVAL}$. $\mathrm{EVAL}$ cuenta en
unidades de «un peón vale 10». Si una victoria valiera $U=+1$, el algoritmo
preferiría ganar un peón ($+10$) a ganar la partida.

Por eso, en los finales usamos $100\cdot U(s)$: **$+100$** si gana Blancas y
**$-100$** si gana Negras. Multiplicar por 100 solo cambia la escala: entre
dos finales, el orden de preferencia es el mismo que con $U$. El 100 se eligió
mayor que cualquier evaluación: la computadora comprobó que, en las
posiciones alcanzables del 4×4 que no son finales, $\mathrm{EVAL}$ nunca pasa
de 36 en valor absoluto. Una victoria vale más que cualquier posición sin
terminar, y una derrota, menos.

::: remark {#jue-c3-orden-finales title="La evaluación tiene que respetar el orden de los finales"}
Una función de evaluación puede equivocarse en las posiciones sin terminar,
pero no debe contradecir lo que ya se sabe: **ganar vale más que cualquier
estimación, y perder, menos**. Si no lo cumple, el programa puede preferir
una posición «buena» a una victoria segura.
:::

## 4 · Leer qué preferencia expresa la suma

**Piensa: ¿qué preferencia expresa esta suma?**

$\mathrm{EVAL}$ no viene del reglamento: **la escribimos nosotros**. Es una
decisión de modelado, igual que la medida de comodidad de
[[opt-objetivo-salones-practica|el ejemplo de los salones]] en la unidad de optimización.
Ahí, sumar las molestias de los grupos aceptaba que uno sufriera más si el
total bajaba; aquí, los pesos dicen cuánto importa cada rasgo.

Lo que esta suma dice, leída con cuidado:

- **Un peón vale lo mismo que diez filas de avance.** En las posiciones
  alcanzables del 4×4 que no son finales, la diferencia de avance nunca pasa
  de 6 en valor absoluto, así que **el material decide primero** y el avance
  solo desempata.
- **Todos los peones valen igual**, estén donde estén. Un peón a punto de
  llegar cuenta como uno recién salido, salvo por su avance.
- **No ve si un peón está bloqueado** por otro que tiene enfrente, ni si está
  a punto de ser capturado.
- **No sabe a quién le toca.** La misma posición recibe el mismo número
  mueva quien mueva, aunque eso pueda decidir la partida.

Ninguna de esas omisiones es un error de cuenta. Son **supuestos** del
modelo, y conviene escribirlos como tales.

En ajedrez, la evaluación más conocida es la del **material**: peón 1,
caballo 3, alfil 3, torre 5 y dama 9. Es la misma idea, una suma ponderada
de rasgos, y tiene los mismos huecos: no ve si el rey está expuesto ni si
una pieza está atrapada. Los programas reales suman muchos más rasgos.

**Punto de control:** deberías poder calcular $\mathrm{EVAL}$ de un tablero
de 4×4 y decir dos cosas que esa suma no ve.

## 5 · Mirar una jugada y evaluar

**Estamos aquí:** la posición de la clase, mueven Blancas, con
$\mathrm{EVAL}=1$. Sus jugadas son a1-a2, d2-d3 y d2xc3. El peón de c2 no
puede moverse: tiene a c3 enfrente y nada que capturar en b3 ni en d3.

**Pendiente:** elegir jugada con $d=1$ en la raíz: cada jugada de Blancas
deja $d=0$, así que, sin esperar la respuesta, se evalúa.

| Jugada | Qué cambia | $\mathrm{EVAL}$ después |
|---|---|---:|
| a1-a2 | El peón de a sube una fila | $0+(3-1)=2$ |
| d2-d3 | El peón de d sube una fila | $0+(3-1)=2$ |
| d2xc3 | Captura el peón de c3 y sube a c3 | $10\cdot(3-2)+(3-0)=13$ |

::: exercise {#jue-c3-ej-prof-1 title="Decide la jugada a profundidad 1"}
**Decide:** con estos tres números, ¿qué jugada elige Blancas a
profundidad 1?
:::

::: answer {#jue-c3-resp-prof-1 of="jue-c3-ej-prof-1"}
Elige **d2xc3**, con 13: gana un peón. Las otras dos solo avanzan y valen 2.
:::

Con profundidad 1, Blancas **captura**. Parece obvio: un peón de más.

## 6 · Mirar la respuesta del rival

**Piensa: después de capturar en c3, ¿qué puede hacer Negras?**

**Estamos aquí:** misma posición, mismas tres jugadas.

**Pendiente:** ahora $d=2$ en la raíz. Miramos la jugada de Blancas, **todas
las respuestas de Negras**, y evaluamos. Negras es MIN: de sus respuestas,
elige la de menor $\mathrm{EVAL}$.

| Jugada de Blancas | Respuestas de Negras y su $\mathrm{EVAL}$ | Peor para Blancas |
|---|---|---:|
| a1-a2 | c3xd2: $-10$ · a4-a3: $1$ · b4-b3: $1$ | $-10$ |
| d2-d3 | a4-a3: $1$ · b4-b3: $1$ | $1$ |
| d2xc3 | ? | ? |

Tras a1-a2, Negras captura en d2 con el peón de c3. Tras d2-d3, el peón de c3
queda bloqueado por c2 y ya no tiene a quién capturar.

::: exercise {#jue-c3-ej-prof-2 title="Decide el valor de la captura a profundidad 2"}
Tras d2xc3, el tablero es este y mueven Negras:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | B | · |
| **2** | · | · | B | · |
| **1** | B | · | · | · |

1. Escribe las jugadas de Negras.
2. Calcula $\mathrm{EVAL}$ después de cada una.
3. ¿Cuánto vale d2xc3 a profundidad 2? ¿Qué jugada elige Blancas ahora?
:::

::: answer {#jue-c3-resp-prof-2 of="jue-c3-ej-prof-2"}
1. Negras tiene a4-a3, b4-b3 y **b4xc3**: el peón de b4 captura en diagonal
   hacia abajo.
2. Tras a4-a3 o b4-b3: $10\cdot(3-2)+(3-1)=12$. Tras b4xc3, cada lado queda
   con dos peones: Blancas a1 y c2, con avance 1; Negras a4 y c3, con avance
   1. $\mathrm{EVAL}=0+(1-1)=0$.
3. Negras elige b4xc3, así que d2xc3 vale **0**. Blancas compara $-10$, $1$
   y $0$ y elige **d2-d3**.
:::

La tabla completa a profundidad 2 queda así:

| Jugada | Profundidad 1 | Profundidad 2 |
|---|---:|---:|
| a1-a2 | 2 | $-10$ |
| d2-d3 | 2 | **1** |
| d2xc3 | **13** | 0 |

**Mirar una jugada más cambió la decisión.** La captura ganaba un peón, pero
Negras lo recupera enseguida en b4xc3.

## 7 · Comparar con el valor exacto

**Piensa: si con profundidad 2 la decisión cambió, ¿cambiará otra vez con
profundidad 3?**

A profundidad 3 se mira jugada de Blancas, respuesta de Negras y otra jugada
de Blancas. La computadora da:

| Jugada | Prof. 1 | Prof. 2 | Prof. 3 | Exacto, en la escala de los cortes (±100) |
|---|---:|---:|---:|---:|
| a1-a2 | 2 | $-10$ | $-9$ | $-100$ |
| d2-d3 | 2 | 1 | **100** | $+100$ |
| d2xc3 | **13** | 0 | 1 | $-100$ |

El 100 de d2-d3 sale de un final: tras d2-d3, Negras solo puede jugar a4-a3 o
b4-b3, y en los dos casos Blancas juega **d3-d4** y llega a la fila 4. A
profundidad 3 el algoritmo ya ve esa victoria.

La última columna es el **valor exacto**: el minimax del juego completo,
calculado por la computadora hasta los finales con $U=\pm1$ y multiplicado
por 100 para compararlo con las otras columnas. **Capturar pierde y d2-d3
gana.** Con profundidad 1 el programa habría elegido la jugada perdedora.

::: definition {#jue-c3-valor-con-corte title="Valor con corte"}
El **valor con corte** de un estado, cuando quedan $d$ jugadas por mirar, es
el minimax del árbol cortado a $d$ jugadas, con $\mathrm{EVAL}$ en los nodos
de corte y $100\cdot U$ en los finales. Es **el minimax de la evaluación**,
no el valor del juego, y puede equivocarse.
:::

Coinciden con seguridad (salvo el factor 100) cuando todas las ramas llegan a
finales antes del corte, o cuando $\mathrm{EVAL}$ da en cada nodo de corte
100 veces su valor exacto; fuera de esos casos pueden coincidir o no, y nada
lo garantiza.

**Punto de control:** deberías poder calcular a mano el valor con corte de
cada jugada a profundidad 1 y 2 en una posición de peones de 4×4, y explicar
por qué puede no coincidir con el valor exacto.

## 8 · Escribir el procedimiento general

Reunimos lo que hicimos a mano. Necesitamos estos nombres:

| Nombre | Qué guarda |
|---|---|
| $s$ | Estado que se está valorando |
| $d$ | La profundidad que queda: jugadas que todavía se pueden mirar desde $s$ |
| $P(s)$ | Jugador de turno: MAX o MIN |
| $A(s)$, $T(s,a)$ | Jugadas permitidas y estado al que lleva cada una |
| $U(s)$ | Utilidad de un final: $+1$ o $-1$ |
| $\mathrm{EVAL}(s)$ | Estimación de un estado sin terminar |

```text
INPUT   un estado s y la profundidad que queda, d ≥ 0
OUTPUT  el valor con corte de s, en puntos de MAX

 1  function MINIMAX-CON-CORTE(s, d)
 2      if s es final: return 100 · U(s)
 3      if d = 0: return EVAL(s)                   ▷ nodo de corte
 4      if P(s) = MAX
 5          v ← −∞
 6          for each a in A(s)
 7              v ← max(v, MINIMAX-CON-CORTE(T(s, a), d − 1))
 8          return v
 9      else                                       ▷ P(s) = MIN
10          v ← +∞
11          for each a in A(s)
12              v ← min(v, MINIMAX-CON-CORTE(T(s, a), d − 1))
13          return v
```

Respecto del minimax de [[minimax-como-algoritmo|la clase 2]], la línea nueva
es la **3**: cuando ya no quedan jugadas por mirar, se estima. La línea 2 solo
cambia la escala de $U$. Las demás son las mismas, con $d-1$ en cada llamada.

Para **elegir la jugada** en la raíz se llama con $d-1$ a cada hijo y se toma
$a^{∗}\in\operatorname*{arg\,max}$ de esos valores, como en la clase 2. Con
$d=1$, $d=2$ y $d=3$ en la raíz salen las tres primeras columnas de la
sección anterior.

::: exercise {#jue-c3-ej-hoja title="Decide qué devuelve cada línea"}
En la posición de la clase, con $d=2$ en la raíz, la llamada para d2xc3 baja
a la respuesta b4xc3 y ahí queda $d=0$.

1. ¿Qué línea del pseudocódigo devuelve el valor en ese estado, y cuánto?
2. Con $d=3$ en la raíz, la llamada para d2-d3 baja por a4-a3 y d3-d4. ¿Qué
   línea devuelve el valor en ese estado, y cuánto?
:::

::: answer {#jue-c3-resp-hoja of="jue-c3-ej-hoja"}
1. La posición tras b4xc3 no es final, así que no la toma la línea 2. Como
   $d=0$, la toma la **línea 3**: devuelve $\mathrm{EVAL}=0$.
2. Blancas llegó a la fila 4: es final. La **línea 2** devuelve
   $100\cdot(+1)=100$, sin importar cuánto valga $d$.
:::

### Por qué termina

Cada llamada recursiva baja $d$ en uno, y la línea 3 no hace más llamadas
cuando $d=0$. Así, el algoritmo **nunca baja más de $d$ niveles** y termina
aunque el árbol completo del juego fuera enorme o infinito. Que termine no
depende de que el juego termine.

### Por qué no es exacto, y qué sí se puede afirmar

Lo que el algoritmo calcula **sí es exacto, pero para otro árbol**: con el
mismo argumento que minimax en la clase 2, devuelve el minimax del árbol
cortado a $d$ jugadas, con las hojas valoradas por las líneas 2 y 3. Si una
hoja de corte está mal estimada, ese error sube por el árbol: por eso no es
el valor del juego.

Hay una afirmación que sí vale en este juego. Como $|\mathrm{EVAL}|\le36$ en
las posiciones alcanzables que no son finales, **un valor de 100 solo puede
venir de finales ganados**: si la búsqueda devuelve 100, Blancas tiene una
victoria asegurada dentro de las $d$ jugadas, responda lo que responda
Negras. Lo mismo vale para $-100$ y Negras. Cualquier otro número es una
estimación.

### Contar el trabajo

Si cada estado tiene a lo más $b$ jugadas —la **ramificación**—, el árbol
cortado tiene a lo más $b^d$ hojas, y cada hoja cuesta una llamada a
$\mathrm{EVAL}$ o a $U$.

::: remark {#jue-c3-costo-corte title="Costo de minimax con corte"}
Con ramificación $b$ y $d$ jugadas por mirar en la raíz, contando cada
llamada como una unidad,

$$T=O(b^d).$$

Con alfa-beta y las jugadas bien ordenadas —la mejor primero en cada nodo—,
el número de nodos visitados es del orden de $O(b^{d/2})$: en el mismo tiempo
se puede mirar cerca del doble de profundidad. El valor que devuelve en la
raíz es el mismo con o sin poda.
:::

Por eso $d$ se elige según el tiempo disponible, no según el juego: es el
tema de [[jugar-contra-el-reloj|la página siguiente]].

::: table {#jue-c3-que-cambia title="Qué cambia cuando cambia la búsqueda"}
| Cambio | Efecto que podemos justificar |
|---|---|
| Subir $d$ en uno | Multiplica las hojas por hasta $b$. La decisión puede cambiar, en cualquier sentido: en la sección 7 pasó de la jugada perdedora a la ganadora |
| Una $\mathrm{EVAL}$ mejor, con más rasgos | Mismas hojas, pero cada una cuesta más. Si diera 100 veces el valor exacto en cada nodo de corte, la decisión sería correcta; si solo se acerca, nada lo asegura |
| Peor orden de jugadas, con alfa-beta | El mismo valor en la raíz, pero menos cortes: en el peor orden se visitan tantos nodos como sin poda, $O(b^d)$ |
:::

## Lo que hay que llevarse

- Si el árbol no cabe, se corta cuando la profundidad que queda llega a
  $d=0$ y se usa $\mathrm{EVAL}(s)$ en ese nodo de corte. Los finales valen
  $100\cdot U$, una escala que gana a cualquier estimación.
- $\mathrm{EVAL}$ es un modelo: los pesos expresan una preferencia y dejan
  cosas fuera. Escribe qué supone.
- El valor con corte es el minimax exacto del árbol cortado, no el valor del
  juego; cuesta $O(b^d)$. En la posición de la clase, la profundidad 1 elige
  una jugada que pierde.

Continúa con [[jugar-contra-el-reloj|jugar contra el reloj]].
