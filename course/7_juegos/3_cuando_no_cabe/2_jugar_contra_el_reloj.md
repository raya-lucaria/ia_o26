---
id: jugar-contra-el-reloj
title: Jugar contra el reloj
nav_title: Contra el reloj
summary: "Una búsqueda cortada puede no ver la respuesta que deshace su jugada. Buscar un poco más donde hay capturas, profundizar paso a paso y recordar posiciones permiten entregar una jugada a tiempo."
status: ready
estimated_time: 30m
tags: [juegos, busqueda-adversarial, evaluacion]
---

# Jugar contra el reloj

**¿Qué jugada entregamos si se acaba el tiempo?**

Al terminar tendrás **la profundización iterativa**: buscar a profundidad 1,
luego 2, luego 3, y entregar lo mejor de la última búsqueda completa. Antes
verás por qué una búsqueda cortada puede caer en una trampa que estaba una
jugada más allá.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Empiezan Blancas. Un peón avanza una casilla si está vacía o
> captura en diagonal hacia delante. Gana quien llega a la fila del rival,
> captura todo o deja al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$
> si gana Negras.

Seguimos con la posición de [[cortar-y-evaluar|la página anterior]] y la
misma evaluación: $\mathrm{EVAL}=10\cdot(\text{peones blancos}-\text{peones negros})+(\text{avance blanco}-\text{avance negro})$,
y $100\cdot U=\pm100$ en los finales. Como allá, $d$ es **la profundidad que
queda**: en la raíz, la profundidad de toda la búsqueda.

::: table {#jue-c3-horizonte-reloj title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

## 1 · Reconocer el efecto horizonte

**Piensa: a profundidad 1, ¿qué no alcanzó a ver Blancas cuando eligió
capturar?**

A profundidad 1, d2xc3 valía 13 y las otras jugadas, 2. El algoritmo vio
**la ganancia**: un peón de más. No vio **la respuesta**: Negras recaptura con
b4xc3 y el peón de ventaja desaparece. Esa respuesta estaba una jugada más
allá del corte, donde el algoritmo ya no mira.

::: definition {#jue-c3-efecto-horizonte title="Efecto horizonte"}
El **efecto horizonte** ocurre cuando una consecuencia importante de una
jugada queda más allá de la profundidad de corte, y la búsqueda valora mal
la posición porque la evalúa antes de esa consecuencia.
:::

Al corte se le llama **horizonte** porque el algoritmo no ve nada detrás.
En su forma clásica, el efecto horizonte es una **pérdida inevitable** que el
programa no ve porque hay jugadas que la retrasan y la empujan más allá del
horizonte: el programa las juega y cree que evitó la pérdida. El ejemplo de
esta página es la forma más simple: **una sola respuesta, la recaptura,
queda detrás del horizonte**.

En ajedrez el caso simple es el mismo: una pieza captura un peón defendido,
y el corte cae antes de la recaptura. El programa cree que ganó material.

Subir la profundidad no elimina el problema: lo mueve. A cualquier
profundidad fija puede quedar una jugada importante justo detrás del
horizonte.

## 2 · Buscar un poco más donde hay capturas

**Piensa: ¿en qué posiciones es peligroso detenerse a evaluar?**

Una evaluación que cuenta peones se equivoca sobre todo cuando hay
**capturas pendientes**: el número cambiará en la jugada siguiente. Una
posición sin capturas disponibles se llama **quieta**; en ella la evaluación
es más confiable.

La **búsqueda de quietud** no evalúa en un nodo de corte que no sea quieto:
sigue mirando solo las capturas, hasta llegar a posiciones quietas, y evalúa
ahí. En cada paso, el jugador de turno también puede no capturar y quedarse
con la evaluación de la posición. Así el corte deja de caer en medio de un
intercambio.

::: exercise {#jue-c3-ej-quietud title="Decide dónde seguir buscando"}
A profundidad 1, Blancas evalúa la posición tras cada una de sus tres
jugadas, y en las tres mueven Negras.

1. ¿Tras cuáles de las tres jugadas Negras tiene una captura disponible?
2. Si en esas posiciones se mira la captura de Negras antes de evaluar, ¿qué
   valor recibe cada jugada y cuál elige Blancas?
:::

::: answer {#jue-c3-resp-quietud of="jue-c3-ej-quietud"}
1. Tras **a1-a2**, Negras puede jugar c3xd2. Tras **d2xc3**, puede jugar
   b4xc3. Tras **d2-d3**, el peón de c3 está bloqueado y no tiene a quién
   capturar: esa posición es quieta.
2. Negras elige entre capturar o no, y escoge lo peor para Blancas:
   a1-a2 vale $\min(2,-10)=-10$ y d2xc3 vale $\min(13,0)=0$. Después de esas
   capturas ya no hay más capturas, así que se evalúa. d2-d3 se queda con su
   $\mathrm{EVAL}=2$. Blancas elige **d2-d3**, la jugada que gana.
:::

Con solo mirar las capturas, la profundidad 1 dejó de elegir la jugada
perdedora. Buscar las capturas suele costar poco, porque en muchas
posiciones hay pocas capturas disponibles.

**Punto de control:** deberías poder señalar, en una posición de peones, qué
respuesta queda detrás del horizonte y si la posición donde se corta es
quieta.

## 3 · Profundizar poco a poco

**Piensa: si no sabes cuánto tiempo te queda, ¿con qué profundidad buscas?**

En un torneo hay reloj. En el vocabulario de [[diagnosticar-el-entorno|las perillas del entorno]], este juego es **semidinámico**: el tablero espera, el reloj no. Si
eliges $d$ demasiado grande, el tiempo se acaba a mitad de la búsqueda y no
tienes ninguna jugada. Si lo eliges pequeño, desperdicias tiempo y juegas
peor.

La salida es no elegir: **buscar con $d=1$, luego con $d=2$, luego con
$d=3$**, y así mientras haya tiempo. Cuando el reloj se acaba, se juega la
mejor jugada de la **última búsqueda completa**.

**Estamos aquí:** la posición de la clase, mueven Blancas.

**Pendiente:** ver qué jugada tendría lista el programa después de cada
búsqueda.

| Búsqueda | Valores | Jugada lista |
|---|---|---|
| $d=1$ | a1-a2: 2 · d2-d3: 2 · d2xc3: 13 | d2xc3 |
| $d=2$ | a1-a2: $-10$ · d2-d3: 1 · d2xc3: 0 | d2-d3 |
| $d=3$ | a1-a2: $-9$ · d2-d3: 100 · d2xc3: 1 | d2-d3 |

::: exercise {#jue-c3-ej-reloj title="Decide qué jugada se entrega"}
**Decide:** para cada caso, ¿qué jugada entrega el programa?

1. El reloj se acaba mientras busca con $d=2$.
2. El reloj se acaba mientras busca con $d=3$.
3. El reloj alcanza para terminar $d=3$.
:::

::: answer {#jue-c3-resp-reloj of="jue-c3-ej-reloj"}
1. La última búsqueda completa es $d=1$: entrega **d2xc3** y pierde.
2. La última completa es $d=2$: entrega **d2-d3**, que gana.
3. Entrega **d2-d3**, y además ya sabe que gana: vale 100.

Una búsqueda a medias no se usa: puede no haber revisado la mejor jugada.
:::

El reloj decide la calidad de la jugada. **Si el tiempo solo alcanza para
$d=1$, el programa captura y pierde.**

## 4 · Contar lo que cuesta repetir

**Piensa: buscar con $d=1$, luego con $d=2$ y luego con $d=3$, ¿no es
trabajar tres veces?**

Sí se repite trabajo, pero poco. Con ramificación $b$ —a lo más $b$ jugadas
por estado—, la búsqueda con $d$ en la raíz tiene del orden de $b^d$ hojas.
Todas las búsquedas anteriores juntas suman

$$b+b^2+\dots+b^{d-1}=\frac{b^d-b}{b-1}<\frac{b^d}{b-1}.$$

::: remark {#jue-c3-costo-iterativa title="Costo de la profundización iterativa"}
Si la última búsqueda completa llega a $d$ en la raíz, las anteriores juntas
cuestan cerca de $1/(b-1)$ de esa última. El total es

$$T=O\!\left(b^d\cdot\frac{b}{b-1}\right)=O(b^d),$$

el mismo orden que una sola búsqueda a profundidad $d$. Con $b=10$, repetir
añade cerca de una novena parte; con $b=2$, las anteriores cuestan casi lo
mismo que la última, y el total es cerca del doble.
:::

La última búsqueda domina el costo, y repetir las otras es casi gratis
cuando $b$ es grande.

Además, la repetición **ayuda**. La mejor jugada de la búsqueda anterior se
prueba primero en la siguiente. Como viste en [[alfa-beta-como-algoritmo|alfa-beta]], probar
primero una buena jugada produce más cortes. Para aprovecharlo, la búsqueda
de cada iteración tiene que ser alfa-beta y compartir $\alpha$ entre las
jugadas de la raíz; lo escribimos en la sección siguiente.

## 5 · Escribir la profundización iterativa

| Nombre | Qué guarda |
|---|---|
| $s$ | Estado donde le toca jugar a MAX |
| $d$ | La profundidad que queda en la raíz: la de la búsqueda en curso |
| $\alpha$ | Lo que MAX ya asegura en la raíz durante la búsqueda en curso |
| `jugada` | Mejor jugada de la última búsqueda completa |
| `mejor` | Mejor jugada de la búsqueda en curso |

`ALFA-BETA-CON-CORTE(s, d, α, β)` es el [[alfa-beta-como-algoritmo|alfa-beta de la clase 2]] con la línea del corte de minimax con corte: devuelve $100\cdot U(s)$ si $s$ es final y $\mathrm{EVAL}(s)$ si $d=0$, y en lo demás poda igual.

```text
INPUT   un estado s donde mueve MAX, y un reloj
OUTPUT  una jugada de A(s)

 1  function PROFUNDIZACIÓN-ITERATIVA(s)
 2      jugada ← cualquier a in A(s)
 3      d ← 1
 4      while quede tiempo
 5          α ← −∞ ;  mejor ← jugada
 6          for each a in A(s), empezando por jugada
 7              v ← ALFA-BETA-CON-CORTE(T(s, a), d − 1, α, +∞)
 8              if el tiempo se acabó: return jugada   ▷ búsqueda a medias: se descarta
 9              if v = 100: return a                   ▷ victoria asegurada
10              if v > α: α ← v ;  mejor ← a
11          jugada ← mejor
12          d ← d + 1
13      return jugada
```

- La línea 2 asegura que siempre haya algo que entregar.
- La línea 8 descarta una búsqueda a medias y entrega la de la última
  búsqueda completa.
- La línea 9 es la salida temprana: como $|\mathrm{EVAL}|\le36$ en las
  posiciones alcanzables que no son finales, un 100 solo viene de finales
  ganados. No hay nada mejor que buscar.
- La línea 10 actualiza $\alpha$ entre los hijos de la raíz. Por eso importa
  la línea 6: si la jugada de la búsqueda anterior es buena y se prueba
  primero, $\alpha$ sube pronto y las demás jugadas se podan antes.

En la posición de la clase, con $d=3$ se prueba primero d2-d3, la jugada
que dejó lista $d=2$. Vale 100, y la línea 9 la entrega sin mirar las otras
dos: los valores $-9$ y 1 de la tabla de la sección 3 están ahí para
comparar, pero el programa ya no los calcula.

::: exercise {#jue-c3-ej-linea title="Decide qué línea actúa"}
1. El reloj se acaba durante la búsqueda con $d=2$, después de valorar
   d2xc3 y antes de valorar las otras jugadas. ¿Qué línea actúa y qué
   jugada se entrega?
2. ¿Por qué no basta con devolver `mejor` en ese momento?
:::

::: answer {#jue-c3-resp-linea of="jue-c3-ej-linea"}
1. Actúa la **línea 8** y entrega `jugada`, la de la última búsqueda
   completa: con $d=1$ era **d2xc3**.
2. `mejor` solo compara las jugadas ya valoradas en esta búsqueda; las que
   faltan podrían ser mejores. En este caso, d2-d3 estaba sin valorar.
:::

## 6 · Recordar posiciones ya valoradas

**Piensa: si dos órdenes de jugadas llegan al mismo tablero, ¿hace falta
valorarlo dos veces?**

Como en [[minimax-como-algoritmo|minimax]], un estado al que se llega por
varios caminos —una **transposición**— no hace falta valorarlo dos veces: una
**tabla de transposición** guarda cada estado ya valorado con su valor.

Lo nuevo con corte es que también hay que guardar **la profundidad que
quedaba** cuando se valoró. Un valor calculado con $d=1$ no sirve para una
búsqueda que llega a ese estado con $d=3$: miró menos. Solo se reutiliza si
se calculó con al menos la profundidad que queda ahora.

**Punto de control:** deberías poder explicar, con la posición de la clase,
qué jugada entrega un programa según cuándo se acaba el reloj, y por qué
repetir las búsquedas cuesta poco.

## 7 · Ver el panorama

Estas son las herramientas con las que juegan los programas reales, a escala
mucho mayor.

- **Deep Blue venció a Kasparov en 1997** con búsqueda alfa-beta y una
  función de evaluación escrita por expertos en ajedrez. Es lo de esta clase
  y la anterior: buscar, podar, cortar y estimar.
- **AlphaZero (2017)** cambió las dos piezas. **Aprende** su evaluación
  jugando contra sí mismo, sin que nadie le escriba los pesos, y busca con
  otro método: la **búsqueda de árbol Monte Carlo**, que explora más las
  jugadas que parecen prometedoras en lugar de revisar todas hasta una
  profundidad fija. La [[simular-en-vez-de-evaluar|página siguiente]] la
  presenta.

La pregunta sigue siendo la misma de esta unidad: **qué hará el rival**. Lo
que cambia es cómo se estima lo que no se alcanza a calcular.

## Lo que hay que llevarse

- El efecto horizonte: la búsqueda cortada no ve lo que queda detrás del
  corte, como la recaptura. La búsqueda de quietud sigue mirando capturas
  antes de evaluar.
- La profundización iterativa busca con $d=1,2,3,\dots$ con alfa-beta y
  entrega lo mejor de la última búsqueda completa. Repetir cuesta cerca de
  $1/(b-1)$ de la última y deja la mejor jugada primero para podar más.
- Una tabla de transposición evita valorar dos veces el mismo estado, y con
  corte guarda también la profundidad con que se valoró.

Continúa con [[simular-en-vez-de-evaluar|simular en vez de evaluar]].
