---
id: jugar-contra-el-reloj
title: Jugar contra el reloj
nav_title: Contra el reloj
summary: "Una búsqueda cortada puede no ver la respuesta que deshace su jugada. Buscar un poco más donde hay capturas, profundizar paso a paso y recordar posiciones permiten entregar una jugada a tiempo."
status: ready
estimated_time: 35m
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

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $S_F$ (@jue-c1-finales),
> $\mathrm{Pl}(s)$ (@jue-c1-pl), $A(s)$ (@jue-c1-acciones), $T(s,a)$
> (@jue-c1-transicion) y $U(s)$ (@jue-c1-utilidad), más $\mathrm{EVAL}$
> (@jue-c3-evaluacion).

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]], y uno más: **hay un reloj**.
> El tablero espera a que juegues, pero el tiempo para decidir se acaba.

Seguimos con la posición de [[cortar-y-evaluar|Cortar y evaluar a mano]] y la
misma evaluación, $\mathrm{EVAL}=10\cdot\text{material}+\text{avance}$: el
material es peones blancos menos peones negros, y el avance, avance blanco
menos avance negro. En los finales, $100\cdot U=\pm100$. Como allá, $d$ es **la profundidad que
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

A profundidad 1, $\text{d2}\textbf{x}\text{c3}$ valía 13 y las otras jugadas, 2. El algoritmo vio
**la ganancia**: un peón de más. No vio **la respuesta**: Negras recaptura con
$\text{b4}\textbf{x}\text{c3}$ y el peón de ventaja desaparece. Esa respuesta estaba una jugada más
allá del corte, donde el algoritmo ya no mira.

::: definition {#jue-c3-efecto-horizonte title="Efecto horizonte"}
El **efecto horizonte** ocurre cuando una consecuencia importante de una
jugada queda más allá de la profundidad de corte, y la búsqueda valora mal
la posición porque la evalúa antes de esa consecuencia.
:::

::: figure {#jue-c3-fig-horizonte title="El efecto horizonte"}
![La posición de la clase arriba; la flecha d2xc3 lleva a un nodo de corte con EVAL = 13, un peón de más. Debajo, una línea punteada marca el horizonte, donde se corta con d = 1. Detrás de la línea, en gris, la recaptura b4xc3, que deja EVAL = 0 y que la búsqueda no ve](../_assets/jue-c3-horizonte.svg)
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

::: hint {#jue-c3-pista-quietud of="jue-c3-ej-quietud" title="Negras puede no capturar"}
En la quietud, el jugador de turno elige entre quedarse con la evaluación
de la posición o hacer una captura. Negras es MIN: se queda con el menor de
esos números.
:::

::: answer {#jue-c3-resp-quietud of="jue-c3-ej-quietud"}
1. Tras **$\text{a1}\textbf{-}\text{a2}$**, Negras puede jugar $\text{c3}\textbf{x}\text{d2}$. Tras **$\text{d2}\textbf{x}\text{c3}$**, puede jugar
   $\text{b4}\textbf{x}\text{c3}$. Tras **$\text{d2}\textbf{-}\text{d3}$**, el peón de c3 está bloqueado y no tiene a quién
   capturar: esa posición es quieta.
2. Negras elige entre capturar o no, y escoge lo peor para Blancas:
   $\text{a1}\textbf{-}\text{a2}$ vale $\min(2,-10)=-10$ y $\text{d2}\textbf{x}\text{c3}$ vale $\min(13,0)=0$. Después de esas
   capturas ya no hay más capturas, así que se evalúa. $\text{d2}\textbf{-}\text{d3}$ se queda con su
   $\mathrm{EVAL}=2$. Blancas elige **$\text{d2}\textbf{-}\text{d3}$**, la jugada que gana.
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

> **El problema de la profundización iterativa.**
>
> **Dado:** un estado $s$ donde mueve MAX, las reglas del juego,
> $\mathrm{EVAL}$ y un reloj que nadie sabe cuándo se acaba.
>
> **Encontrar:** una jugada lista para entregar en cualquier momento, tan
> buena como lo permita el tiempo que hubo.

**Estamos aquí:** la posición de la clase, mueven Blancas.

**Pendiente:** ver qué jugada tendría lista el programa después de cada
búsqueda.

| $d$ | Valor de cada jugada | Jugada lista |
|---|---|---|
| 1 | $\text{a1}\textbf{-}\text{a2}$: 2 · $\text{d2}\textbf{-}\text{d3}$: 2 · $\text{d2}\textbf{x}\text{c3}$: 13 | $\text{d2}\textbf{x}\text{c3}$ |
| 2 | $\text{a1}\textbf{-}\text{a2}$: $-10$ · $\text{d2}\textbf{-}\text{d3}$: 1 · $\text{d2}\textbf{x}\text{c3}$: 0 | $\text{d2}\textbf{-}\text{d3}$ |
| 3 | $\text{a1}\textbf{-}\text{a2}$: $-9$ · $\text{d2}\textbf{-}\text{d3}$: 100 · $\text{d2}\textbf{x}\text{c3}$: 1 | $\text{d2}\textbf{-}\text{d3}$ |

::: exercise {#jue-c3-ej-reloj title="Decide qué jugada se entrega"}
**Decide:** para cada caso, ¿qué jugada entrega el programa?

1. El reloj se acaba mientras busca con $d=2$.
2. El reloj se acaba mientras busca con $d=3$.
3. El reloj alcanza para terminar $d=3$.
:::

::: hint {#jue-c3-pista-reloj of="jue-c3-ej-reloj" title="La última completa"}
Una búsqueda que no terminó no cuenta. Para cada caso, pregúntate cuál fue
la última búsqueda que **sí** terminó, y busca su jugada en la tabla.
:::

::: answer {#jue-c3-resp-reloj of="jue-c3-ej-reloj"}
1. La última búsqueda completa es $d=1$: entrega **$\text{d2}\textbf{x}\text{c3}$** y pierde.
2. La última completa es $d=2$: entrega **$\text{d2}\textbf{-}\text{d3}$**, que gana.
3. Entrega **$\text{d2}\textbf{-}\text{d3}$**, y además ya sabe que gana: vale 100.

Una búsqueda a medias no se usa: puede no haber revisado la mejor jugada.
:::

La figura lo dibuja en el tiempo. Cada barra es una búsqueda **sin poda**,
con DECIDIR-CON-CORTE, y su largo, cuántos nodos genera:

::: figure {#jue-c3-fig-profundizacion title="Profundizar mientras haya tiempo"}
![Tres barras seguidas en el tiempo: la búsqueda con d = 1 genera 4 nodos y deja lista d2xc3; la de d = 2 genera 12 y deja lista d2-d3; la de d = 3 genera 33 y deja lista d2-d3, que gana. Dos líneas marcan dos relojes: el reloj 1 se acaba durante d = 2, así que se entrega d2xc3; el reloj 2 se acaba durante d = 3, así que se entrega d2-d3](../_assets/jue-c3-profundizacion.svg)
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
cuando $b$ es grande. En la posición de la clase, sin poda, las búsquedas
con $d=1$ y $d=2$ generan $4+12=16$ nodos, menos de la mitad de los 33 de
$d=3$.

Además, la repetición **ayuda**. La mejor jugada de la búsqueda anterior se
prueba primero en la siguiente. Como viste en [[alfa-beta-como-algoritmo|alfa-beta]], probar
primero una buena jugada produce más cortes. Para aprovecharlo, la búsqueda
de cada iteración tiene que ser alfa-beta y compartir $\alpha$ entre las
jugadas de la raíz; lo escribimos en la sección siguiente.

## 5 · Escribir la profundización iterativa

Qué guarda cada nombre:

- **$s$:** el estado donde le toca jugar a MAX.
- **$d$:** la profundidad que queda en la raíz, la de la búsqueda en curso.
- **$\alpha$:** lo que MAX ya asegura en la raíz durante la búsqueda en
  curso: el `mejor_valor` de DECIDIR.
- **`jugada`:** la mejor de la última búsqueda **completa**: la que se
  entrega.
- **`mejor_jugada`:** la mejor de la búsqueda **en curso**, como en
  DECIDIR.
- **$w$:** lo que devuelve un hijo de la raíz.

PROFUNDIZACIÓN-ITERATIVA hace el papel de DECIDIR: va primero, en las
líneas 1–13. Su auxiliar, ALFA-BETA-CON-CORTE, va en el mismo bloque, en
las líneas 14–32.

```text
INPUT   un estado s donde mueve MAX; las
        reglas S_F, Pl, A, T y U; una
        función EVAL; y un reloj.
        No recibe el grafo.
OUTPUT  una jugada de A(s), la mejor de la
        última búsqueda completa.

 1 function PROFUNDIZACIÓN-ITERATIVA(s)
     # siempre hay algo que entregar
 2   jugada ← cualquier a in A(s)
 3   d ← 1
     # cada vuelta, una búsqueda más honda
 4   while quede tiempo
 5     α ← −∞ ; mejor_jugada ← jugada
       # la anterior primero: α sube pronto
 6     for each a in A(s), jugada primero
 7       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, +∞)
         # a medias no sirve: va la anterior
 8       if el tiempo se acabó: return jugada
 9       if w = 100: return a  # gana seguro
10       if w > α: α ← w ; mejor_jugada ← a
11     jugada ← mejor_jugada   # ya terminó
12     d ← d + 1
13   return jugada

14 function ALFA-BETA-CON-CORTE(s, d, α, β)
15   if s ∈ S_F: return 100 · U(s)
16   if d = 0: return EVAL(s)  # se estima
17   if Pl(s) = MAX
18     v ← −∞
19     for each a in A(s)
20       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, β)
21       v ← max(v, w)
22       if v ≥ β: return v    # corte beta
23       α ← max(α, v)
24     return v
25   else
26     v ← +∞
27     for each a in A(s)
28       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, β)
29       v ← min(v, w)
30       if v ≤ α: return v    # corte alfa
31       β ← min(β, v)
32     return v
```

El mismo procedimiento en Python, línea por línea. El reloj es una
función, `queda_tiempo()`, que dice si sigue habiendo tiempo. El número
entre paréntesis es la línea del pseudocódigo de arriba:

```python
from math import inf

# Las reglas: es_final(s), pl(s), acciones(s),
# transicion(s, a), utilidad(s) y evaluar(s),
# que es EVAL. pl(s) da "MAX" o "MIN".

def profundizacion_iterativa(s):   # (1)
    jugada = acciones(s)[0]        # (2)
    d = 1                          # (3)
    while queda_tiempo():          # (4)
        alfa = -inf                # (5)
        mejor_jugada = jugada
        # (6) La jugada anterior va primero.
        resto = [a for a in acciones(s)
                 if a != jugada]
        for a in [jugada] + resto:
            # (7) Le quedan d - 1 jugadas.
            w = alfa_beta_con_corte(
                transicion(s, a),
                d - 1, alfa, inf)
            # (8) A medias: se descarta.
            if not queda_tiempo():
                return jugada
            # (9) Victoria asegurada.
            if w == 100:
                return a
            # (10) Mejor que lo visto.
            if w > alfa:
                alfa = w
                mejor_jugada = a
        jugada = mejor_jugada      # (11)
        d = d + 1                  # (12)
    return jugada                  # (13)

# (14) El alfa-beta de la clase 2, con d.
def alfa_beta_con_corte(s, d, alfa, beta):
    if es_final(s):                # (15)
        return 100 * utilidad(s)
    if d == 0:                     # (16) EVAL
        return evaluar(s)
    if pl(s) == "MAX":             # (17)
        v = -inf                   # (18)
        for a in acciones(s):      # (19)
            w = alfa_beta_con_corte(  # (20)
                transicion(s, a),
                d - 1, alfa, beta)
            v = max(v, w)          # (21)
            if v >= beta:          # (22) beta
                return v
            alfa = max(alfa, v)    # (23)
        return v                   # (24)
    else:                          # (25)
        v = inf                    # (26)
        for a in acciones(s):      # (27)
            w = alfa_beta_con_corte(  # (28)
                transicion(s, a),
                d - 1, alfa, beta)
            v = min(v, w)          # (29)
            if v <= alfa:          # (30) alfa
                return v
            beta = min(beta, v)    # (31)
        return v                   # (32)
```

**Las líneas 14–32 son el [[alfa-beta-como-algoritmo|ALFA-BETA de la clase 2]]**
(sus líneas 7–24) con lo de [[minimax-con-corte|minimax con corte]]:

- **15** es su línea 8, con la escala $100\cdot U$.
- **16** es la nueva: con $d=0$ se estima. Por ella, las demás quedan
  corridas en uno: el corte beta, su 14, es aquí la 22, y el corte alfa,
  su 22, es aquí la 30.
- **20 y 28** pasan $d-1$ al hijo.

Y en PROFUNDIZACIÓN-ITERATIVA:

- La línea 2 asegura que siempre haya algo que entregar.
- La línea 8 descarta una búsqueda a medias y entrega la de la última
  búsqueda completa. El reloj **solo se revisa ahí**, entre dos hijos de
  la raíz: si un hijo tarda mucho, la búsqueda se pasa del tiempo hasta
  que ese hijo termina. Un programa real lo revisa también por dentro.
- La línea 9 es la salida temprana: como $|\mathrm{EVAL}|\le36$ en las
  posiciones alcanzables que no son finales, un 100 solo viene de finales
  ganados. No hay nada mejor que buscar.
- Las líneas 5, 7, 10 y 11 son DECIDIR-ALFA-BETA: $\alpha$ hace de
  `mejor_valor`, y la línea 10 lo sube entre los hijos de la raíz. Por eso
  importa la línea 6: si la jugada de la búsqueda anterior es buena y se
  prueba primero, $\alpha$ sube pronto y las demás jugadas se podan antes.
- Si ninguna jugada gana, la línea 9 nunca actúa. Cuando $d$ ya alcanza
  todos los finales —en una posición perdida o empatada—, cada vuelta
  repite la misma búsqueda hasta que se acaba el reloj: gasta el tiempo,
  pero no cambia la jugada.

**En el árbol T.** Con la $\mathrm{EVAL}$ de
[[minimax-con-corte|Minimax con corte]] (I 5, C 4, D 7, C1 6, C2 9) y la
jugada inicial izq (línea 2). Como allá, el número de cada hoja de T ya
está en la escala de los finales: es lo que devolvió la línea 15,
$100\cdot U$. T es un árbol de juguete, sin un $U=\pm1$ detrás.

::: figure {#jue-c3-t-fig-iterativa title="Profundización iterativa en el árbol T"}
![Tres copias pequeñas del árbol T, una por búsqueda. Con d = 1, la raíz prueba izq, centro y der, ve sus EVAL 5, 4 y 7, genera 4 nodos y deja lista der. Con d = 2 prueba der primero, luego izq y centro; ve 2, 3 y 6, sin cortes, genera 10 nodos y deja lista centro. Con d = 3 prueba centro primero y ve 5; poda la hoja 8 con un corte beta en C2 y las hojas 6 y 12 con cortes alfa en I y en D; genera 11 nodos y deja lista centro](../_assets/jue-t-iterativa.svg)
:::

::: table {#jue-c3-t-iterativa title="Cada búsqueda de la profundización iterativa en el árbol T"}
| $d$ | orden: $w$ | Lista |
|---|---|---|
| 1 | I 5 · C 4 · D 7 | der |
| 2 | **D** 2 · I 3 · C 6 | centro |
| 3 | **C** 5 · I ≤3 · D ≤2 | centro |
:::

- **Cómo leer la tabla:** «orden: $w$» da los hijos de R en el orden en que
  se prueban, con el $w$ que devuelve cada uno; en negrita, el que va
  primero por ser la jugada lista de la búsqueda anterior. I, C y D son los
  hijos por izq, centro y der.
- **Nodos generados:** 4, 10 y 11. **Cortes:** con $d=1$ y $d=2$, ninguno.
  Con $d=3$, un corte beta en C2 y dos cortes alfa, en I y en D.
- **$d=1$ deja lista la trampa**, der, y por la línea 6 der va primero con
  $d=2$. Ahí ya se ve que vale 2: la búsqueda corrige la jugada.
- **Con $d=3$, centro va primero** y $\alpha$ sube a 5 de entrada. I y D
  llegan con $(5,+\infty)$: su primera hoja, 3 y 2, ya es $\le5$ y cortan.
  En C2, $7\ge5$ corta y la hoja 8 no se genera.
- Los $w$ de I y D con $d=3$ son **techos**, no valores: «I vale a lo más
  3». Bastan para saber que no superan a centro.
- Las tres búsquedas generan $4+10+11=25$ nodos. Sin poda, con
  DECIDIR-CON-CORTE, serían $4+10+14=28$. Con alfa-beta en el orden de
  siempre, la de $d=3$ sola genera 12; con centro primero, 11.

En la posición de la clase, con $d=3$ se prueba primero $\text{d2}\textbf{-}\text{d3}$, la jugada
que dejó lista $d=2$. Vale 100, y la línea 9 la entrega sin mirar las otras
dos: los valores $-9$ y 1 de la tabla de la sección 3 están ahí para
comparar, pero el programa ya no los calcula.

Con todo eso, el procedimiento de esta sección genera **4**, **10** y **9**
nodos con $d=1$, 2 y 3, contra los 4, 12 y 33 de la figura sin poda. La
búsqueda con $d=3$ es la más barata de las tres: empieza por la jugada
ganadora y sale en la línea 9.

::: exercise {#jue-c3-ej-linea title="Decide qué línea actúa"}
1. El reloj se acaba durante la búsqueda con $d=2$, después de valorar
   $\text{d2}\textbf{x}\text{c3}$ y antes de valorar las otras jugadas. ¿Qué línea actúa y qué
   jugada se entrega?
2. ¿Por qué no basta con devolver `mejor_jugada` en ese momento?
:::

::: hint {#jue-c3-pista-linea of="jue-c3-ej-linea" title="Qué guarda cada variable"}
`jugada` es la de la última búsqueda **completa**; `mejor_jugada`, la de la
búsqueda en curso. ¿Cuál de las dos ya vio todas las jugadas?
:::

::: answer {#jue-c3-resp-linea of="jue-c3-ej-linea"}
1. Actúa la **línea 8** y entrega `jugada`, la de la última búsqueda
   completa: con $d=1$ era **$\text{d2}\textbf{x}\text{c3}$**.
2. `mejor_jugada` solo compara las jugadas ya valoradas en esta búsqueda; las que
   faltan podrían ser mejores. En este caso las dos variables dicen lo
   mismo, $\text{d2}\textbf{x}\text{c3}$, porque es la primera que se
   probó, pero `mejor_jugada` no lo sabe: $\text{d2}\textbf{-}\text{d3}$, la
   que gana, estaba sin valorar.
:::

## 6 · Recordar posiciones ya valoradas

**Piensa: si dos órdenes de jugadas llegan al mismo tablero, ¿hace falta
valorarlo dos veces?**

Como en [[minimax-como-algoritmo|minimax]], un estado al que se llega por
varios caminos —una **transposición**— no hace falta valorarlo dos veces: una
**tabla de transposición** guarda cada estado ya valorado. Con corte y con
poda, guardar «el estado y su valor» no basta. Cada entrada guarda tres
cosas:

- **El número** que devolvió la búsqueda.
- **La profundidad que quedaba**, $d$. Un número calculado con $d=1$ no
  sirve a una búsqueda que llega con $d=3$: miró menos. Solo se reutiliza
  si se calculó con al menos la profundidad que queda ahora.
- **Qué clase de número es.** Con alfa-beta, un nodo que cortó no devolvió
  su valor, sino una cota:
  - **exacto**, si no hubo corte;
  - **piso**, si hubo corte beta: el valor es **al menos** ese número;
  - **techo**, si hubo corte alfa: el valor es **a lo más** ese número,
    como I y D con $d=3$ en el árbol T.

Un techo de 3 en I no sirve para decir «I vale 3»; sirve para descartar I
en cualquier búsqueda donde MAX ya asegure 3 o más.

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
- Una tabla de transposición evita valorar dos veces el mismo estado. Con
  corte y poda guarda también la profundidad con que se valoró y si el
  número es exacto, un piso o un techo.

Continúa con [[simular-en-vez-de-evaluar|simular en vez de evaluar]].
