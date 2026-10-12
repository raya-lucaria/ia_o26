---
id: jugar-contra-el-reloj
title: Jugar contra el reloj
nav_title: Contra el reloj
summary: "Si no sabes cuánto tiempo queda, buscas con d = 1, luego con 2, luego con 3, y entregas lo de la última búsqueda completa. Primero sin poda; después con alfa-beta, la jugada anterior primero y una tabla que recuerda exacto, piso o techo."
status: ready
estimated_time: 35m
tags: [juegos, busqueda-adversarial, evaluacion, algoritmos]
---

# Jugar contra el reloj

**¿Qué jugada entregamos si se acaba el tiempo?**

Al terminar tendrás:

- decir, en la posición de la clase, **qué jugada entrega** un programa
  según cuándo se acaba el reloj;
- **la profundización iterativa** en dos versiones: una corta sin poda, y
  la completa con alfa-beta, línea por línea lo que cambia entre ellas;
- la **traza de la búsqueda con $d=3$** en el árbol T: qué se poda, dónde
  y por qué;
- la regla para guardar un número en una **tabla de transposición**:
  exacto, piso o techo, según la ventana.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Un peón avanza una casilla si está vacía o captura en diagonal
> hacia delante. Gana quien llega a la fila del rival, captura todo o deja
> al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$ si gana Negras.

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $S_F$ (@jue-c1-finales),
> $\mathrm{Pl}(s)$ (@jue-c1-pl), $A(s)$ (@jue-c1-acciones), $T(s,a)$
> (@jue-c1-transicion) y $U(s)$ (@jue-c1-utilidad). $\mathrm{EVAL}$
> (@jue-c3-evaluacion) y DECIDIR-CON-CORTE, de
> [[minimax-con-corte|Minimax con corte]]. Y ALFA-BETA, de
> [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]].

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]], y uno más: **hay un reloj**.
> El tablero espera a que juegues, pero el tiempo para decidir se acaba.

Seguimos con la posición de [[cortar-y-evaluar|Cortar y evaluar a mano]] y la
misma evaluación, $\mathrm{EVAL}=10\cdot\text{material}+\text{avance}$. En
los finales, $100\cdot U=\pm100$. Como allá, $d$ es **la profundidad que
queda**: en la raíz, la de toda la búsqueda.

::: table {#jue-c3-horizonte-reloj title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

> [!TIP]
> **Míralo correr: profundización iterativa en el árbol T**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#iterativa)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 7: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## 1 · Profundizar poco a poco

**Piensa: si no sabes cuánto tiempo te queda, ¿con qué profundidad buscas?**

En [[mas-alla-del-horizonte|Más allá del horizonte]] viste que una
profundidad fija puede dejar la respuesta decisiva detrás del corte. Mirar
más hondo ayuda, pero cuesta tiempo.

En un torneo hay reloj. En el vocabulario de [[diagnosticar-el-entorno|las perillas del entorno]], este juego es **semidinámico**: el tablero espera, el reloj no.
Si eliges $d$ demasiado grande, el tiempo se acaba a mitad de la búsqueda y
no tienes jugada. Si lo eliges pequeño, desperdicias tiempo y juegas peor.

La salida es no elegir: **buscar con $d=1$, luego con $d=2$, luego con
$d=3$**, mientras haya tiempo. Cuando el reloj se acaba, se juega la mejor
jugada de la **última búsqueda completa**.

> **El problema de la profundización iterativa.**
>
> **Dado:** un estado $s$ donde mueve MAX, las reglas del juego
> (@jue-c1-finales, @jue-c1-pl, @jue-c1-acciones, @jue-c1-transicion,
> @jue-c1-utilidad), $\mathrm{EVAL}$ (@jue-c3-evaluacion) y un reloj que
> nadie sabe cuándo se acaba.
>
> **Encontrar:** una jugada lista para entregar en cualquier momento, tan
> buena como lo permita el tiempo que hubo.

::: definition {#jue-c3-profundizacion-iterativa title="Profundización iterativa"}
La **profundización iterativa** repite la búsqueda con corte con
$d=1,2,3,\dots$ mientras quede tiempo. Guarda la mejor jugada de cada
búsqueda que termina, y al acabarse el reloj entrega la de la última
búsqueda completa.
:::

**Estamos aquí:** la posición de la clase, mueven Blancas. La tabla da el
valor con corte de cada jugada en las tres primeras búsquedas.

::: table {#jue-c3-reloj-por-d title="Valor de cada jugada de Blancas en cada búsqueda"}
| $d$ | $\text{a1}\textbf{-}\text{a2}$ | $\text{d2}\textbf{-}\text{d3}$ | $\text{d2}\textbf{x}\text{c3}$ |
|---|---:|---:|---:|
| 1 | 2 | 2 | 13 |
| 2 | $-10$ | 1 | 0 |
| 3 | $-9$ | 100 | 1 |
:::

::: exercise {#jue-c3-ej-reloj title="Encuentra la jugada que se entrega"}
Para cada caso, ¿qué jugada entrega el programa?

1. El reloj se acaba mientras busca con $d=2$.
2. El reloj se acaba mientras busca con $d=3$.
3. El reloj alcanza para terminar $d=3$.
:::

::: hint {#jue-c3-pista-reloj-1 of="jue-c3-ej-reloj" title="Fila por fila"}
En cada caso, ¿cuáles búsquedas terminaron antes de que sonara el reloj?
De la última de ellas, ¿qué columna tiene el número mayor?
:::

::: answer {#jue-c3-resp-reloj of="jue-c3-ej-reloj"}
1. La última búsqueda completa es $d=1$, y su mayor número es 13:
   entrega **$\text{d2}\textbf{x}\text{c3}$**, que pierde.
2. La última completa es $d=2$, con 1: entrega
   **$\text{d2}\textbf{-}\text{d3}$**, que gana.
3. Entrega **$\text{d2}\textbf{-}\text{d3}$**, y además ya sabe que gana:
   vale 100.

Una búsqueda a medias no se usa: puede no haber revisado la mejor jugada.
:::

La figura lo dibuja en el tiempo. Cada barra es una búsqueda **sin poda**,
con DECIDIR-CON-CORTE, y su largo es cuántos nodos genera.

::: figure {#jue-c3-fig-profundizacion title="El reloj decide qué jugada se entrega"}
![Tres barras seguidas en el tiempo, una por búsqueda sin poda sobre la posición de la clase. La de d = 1 genera 4 nodos y deja lista d2xc3, con 13; la de d = 2 genera 12 y deja lista d2-d3, con 1; la de d = 3 genera 33 y deja lista d2-d3, con 100. Dos líneas punteadas, reloj 1 y reloj 2, marcan dos momentos en que se acaba el tiempo: el reloj 1 cae durante d = 2 y se entrega d2xc3; el reloj 2 cae durante d = 3 y se entrega d2-d3](../_assets/jue-c3-profundizacion.svg)
:::

El reloj decide la calidad de la jugada. **Si el tiempo solo alcanza para
$d=1$, el programa captura y pierde.**

## 2 · Contar lo que cuesta repetir

**Piensa: buscar con $d=1$, luego con $d=2$ y luego con $d=3$, ¿no es
trabajar tres veces?**

Sí se repite trabajo, pero poco. Con ramificación $b$ —a lo más $b$ jugadas
por estado—, la búsqueda con $d$ en la raíz tiene del orden de $b^d$ hojas.
Todas las búsquedas anteriores juntas suman

$$b+b^2+\dots+b^{d-1}=\frac{b^d-b}{b-1}<\frac{b^d}{b-1}.$$

::: remark {#jue-c3-costo-iterativa title="Costo de la profundización iterativa"}
Si la última búsqueda completa llega a $d$ en la raíz, las anteriores juntas
cuestan cerca de $1/(b-1)$ de esa última. El tiempo total es

$$\text{tiempo}=O\!\left(b^d\cdot\frac{b}{b-1}\right)=O(b^d),$$

el mismo orden que una sola búsqueda a profundidad $d$. Con $b=10$, repetir
añade cerca de una novena parte. Con $b=2$, las anteriores cuestan casi lo
mismo que la última, y el total es cerca del doble.
:::

La última búsqueda domina el costo. Repetir las otras es casi gratis cuando
$b$ es grande.

::: exercise {#jue-c3-ej-costo title="Calcula lo que se repite"}
Usa las barras de la figura: 4, 12 y 33 nodos.

1. ¿Cuántos nodos genera en total profundizar hasta terminar $d=3$?
2. ¿Cuántos de ellos son repetición? ¿Es más o menos que la mitad de la
   última búsqueda?
:::

::: hint {#jue-c3-pista-costo-1 of="jue-c3-ej-costo" title="Qué se habría hecho igual"}
Un programa que supiera de antemano que llega a $d=3$, ¿qué búsquedas
habría hecho? Lo demás es lo que se repite.
:::

::: answer {#jue-c3-resp-costo of="jue-c3-ej-costo"}
1. $4+12+33=$ **49** nodos.
2. Se repiten las búsquedas con $d=1$ y $d=2$: $4+12=$ **16** nodos,
   **menos de la mitad** de los 33 de la última. Aquí $b$ no es fijo
   —ninguna posición tiene más de 5 jugadas—, así que la cuenta de
   $1/(b-1)$ es una guía, no una igualdad.
:::

## 3 · Escribir la versión sin poda

**Piensa: ¿qué le falta a DECIDIR-CON-CORTE para jugar contra un reloj?**

Solo un ciclo alrededor: llamarla con $d=1,2,3,\dots$ y recordar la jugada
de la última búsqueda que terminó. Qué guarda cada nombre:

- **$s$:** el estado donde le toca jugar a MAX.
- **$d$:** la profundidad de la búsqueda en curso.
- **`jugada`:** la mejor de la última búsqueda **completa**: la que se
  entrega.
- **`nueva`:** lo que devuelve la búsqueda en curso cuando termina.

```text
INPUT   un estado s donde mueve MAX; las
        reglas S_F, Pl, A, T y U; una
        función EVAL; y un reloj.
OUTPUT  una jugada de A(s), la mejor de la
        última búsqueda completa.

 1 function PROFUNDIZAR-SIN-PODA(s)
     # siempre hay algo que entregar
 2   jugada ← cualquier a in A(s)
 3   d ← 1
     # cada vuelta, una búsqueda más honda
 4   while quede tiempo
       # la de la página anterior, entera
 5     nueva ← DECIDIR-CON-CORTE(s, d)
       # se acabó mientras corría: no cuenta
 6     if el tiempo se acabó: return jugada
 7     jugada ← nueva       # ya terminó
 8     d ← d + 1
 9   return jugada
```

- La línea 2 asegura que siempre haya algo que entregar.
- La línea 5 es la búsqueda de [[minimax-con-corte|Minimax con corte]],
  sin cambiar nada.
- La línea 6 mira el reloj **solo al terminar** cada búsqueda. Si se acabó
  mientras corría, esa búsqueda no cuenta y se entrega la anterior.

**En el árbol T.** Con la $\mathrm{EVAL}$ de
[[minimax-con-corte|Minimax con corte]]: I 5, C 4, D 7, C1 6 y C2 9. Las
hojas de T son números de juguete: valen como lo que devolvería la línea
de los finales. R prueba sus hijos en el orden izq, centro, der.

::: table {#jue-c3-t-sin-poda title="PROFUNDIZAR-SIN-PODA en el árbol T"}
| $d$ | I · C · D | Lista | Nodos |
|---|---|---|---:|
| 1 | 5 · 4 · 7 | der | 4 |
| 2 | 3 · 6 · 2 | centro | 10 |
| 3 | 3 · 5 · 2 | centro | 14 |
:::

- **$d=1$ deja lista la trampa:** der parece valer 7, pero con $d=2$ vale
  2.
- **$d=2$ corrige la jugada:** centro, con 6. Con $d=3$ sigue centro, con
  5.
- Las tres búsquedas generan $4+10+14=28$ nodos. Si el reloj se acaba
  durante $d=2$, se entrega der; durante $d=3$, centro.

::: exercise {#jue-c3-ej-orden-sin-poda title="Comprueba si el orden importa"}
Cambia el orden en que R prueba sus hijos: en cada búsqueda va primero la
jugada lista de la anterior. Con $d=2$, R prueba der, izq, centro; con
$d=3$, centro, izq, der.

1. ¿Cambia la jugada lista de alguna búsqueda?
2. ¿Cambia el número de nodos?
:::

::: hint {#jue-c3-pista-orden-sin-poda-1 of="jue-c3-ej-orden-sin-poda" title="Qué línea podría notarlo"}
¿Hay alguna línea de DECIDIR-CON-CORTE o de MINIMAX-CON-CORTE que deje de
generar un hijo? ¿Y cuándo podría cambiar el ganador de `w > mejor_valor`?
:::

::: answer {#jue-c3-resp-orden-sin-poda of="jue-c3-ej-orden-sin-poda"}
1. **No.** El `>` estricto solo distingue el orden cuando hay empate, y en
   ninguna fila de la tabla hay dos valores iguales. Las listas siguen
   siendo der, centro y centro.
2. **No.** Sin poda, cada búsqueda genera todos los hijos, en el orden que
   sea: 4, 10 y 14.

Poner primero la jugada lista solo sirve si la búsqueda puede saltarse
algo. Eso es lo que trae alfa-beta.
:::

## 4 · Pasar a alfa-beta

**Piensa: si la búsqueda nueva ya sabe cuál fue la mejor jugada de la
anterior, ¿cómo puede ahorrar trabajo?**

Con alfa-beta, una buena jugada probada primero **sube $\alpha$ pronto** y
las demás se podan antes; lo viste en
[[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]]. Para aprovecharlo,
hay que abrir la línea 5 de la versión corta y tocar cuatro cosas entre dos
hijos de la raíz:

- **Alfa-beta que comparte $\alpha$** (líneas 7 y 14–32): cada hijo de la
  raíz se valora con ALFA-BETA-CON-CORTE y recibe el $\alpha$ que la raíz
  ya asegura.
- **La jugada anterior primero** (línea 6).
- **El reloj entre dos hijos** (línea 8): la versión corta solo lo miraba al
  terminar cada búsqueda.
- **La salida con 100** (línea 9): si un hijo gana seguro, no hay nada
  mejor que buscar.

Los nombres nuevos:

- **$\alpha$:** lo que MAX ya asegura en la raíz durante la búsqueda en
  curso: hace de `mejor_valor`.
- **`mejor_jugada`:** la mejor de la búsqueda **en curso**, como en
  DECIDIR.
- **$w$:** lo que devuelve un hijo de la raíz.

PROFUNDIZACIÓN-ITERATIVA va primero, en las líneas 1–13. Su auxiliar,
ALFA-BETA-CON-CORTE, va en el mismo bloque, en las líneas 14–32.

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

**Lo que cambia respecto de PROFUNDIZAR-SIN-PODA:**

- **Se quedan igual** las líneas 2, 3, 4, 12 y 13: son las 2, 3, 4, 8 y 9
  de la versión corta. La 11, `jugada ← mejor_jugada`, es su línea 7.
- **Las líneas 5, 7 y 10 son DECIDIR-ALFA-BETA** (sus líneas 2, 4 y 5):
  $\alpha$ hace de `mejor_valor`, y la línea 10 lo sube entre los hijos de
  la raíz. La 6 es su línea 3 con otro orden.
- **La línea 6** prueba primero la jugada de la búsqueda anterior. Si es
  buena, $\alpha$ sube pronto y las demás jugadas se podan antes.
- **La línea 8** es la línea 6 de la versión corta, ahora entre dos hijos
  de la raíz. Si un hijo tarda mucho, la búsqueda se pasa del tiempo hasta
  que ese hijo termina. Un programa real lo revisa también por dentro.
- **La línea 9** es la salida temprana. Como $|\mathrm{EVAL}|\le36$ en las
  posiciones alcanzables que no son finales, un 100 solo viene de finales
  ganados.

**Las líneas 14–32 son el [[alfa-beta-como-algoritmo|ALFA-BETA de la clase 2]]**
(sus líneas 7–24) con lo de [[minimax-con-corte|minimax con corte]]:

- **15** es su línea 8, con la escala $100\cdot U$.
- **16** es la nueva: con $d=0$ se estima. Por ella, las demás quedan
  corridas en uno: el corte beta, su 14, es aquí la 22, y el corte alfa,
  su 22, es aquí la 30.
- **20 y 28** pasan $d-1$ al hijo.

::: remark {#jue-c3-entrega-iterativa title="Qué entrega y cuándo termina"}
PROFUNDIZACIÓN-ITERATIVA siempre devuelve una jugada de $A(s)$: la línea 2
la pone antes de buscar. Lo que devuelve es la jugada de la última búsqueda
completa, con el mayor valor con corte de esa $d$, o una jugada que gana
seguro (línea 9).

Termina cuando un hijo gana seguro (línea 9) o cuando se
acaba el reloj (línea 8 o 4). Si ninguna jugada gana, la 9 nunca actúa.
Cuando $d$ ya alcanza todos los finales, cada vuelta repite la misma
búsqueda: gasta el tiempo, pero no cambia la jugada.
:::

::: exercise {#jue-c3-ej-linea title="Señala qué línea actúa"}
En la posición de la clase, el reloj se acaba durante la búsqueda con
$d=2$. Ya se valoró $\text{d2}\textbf{x}\text{c3}$, que va primero, y
faltan las otras dos jugadas.

1. ¿Qué línea actúa y qué jugada se entrega?
2. ¿Por qué no basta con devolver `mejor_jugada` en ese momento?
:::

::: hint {#jue-c3-pista-linea-1 of="jue-c3-ej-linea" title="Sigue las líneas en orden"}
Tras la línea 7, ¿cuál es la primera que mira el reloj? Para la parte 2:
¿en qué línea recibe su valor cada una de las dos variables, y cuántas
jugadas se habían valorado cuando eso pasó?
:::

::: answer {#jue-c3-resp-linea of="jue-c3-ej-linea"}
1. Actúa la **línea 8** y entrega `jugada`, la de la última búsqueda
   completa: con $d=1$ era **$\text{d2}\textbf{x}\text{c3}$**.
2. `mejor_jugada` solo compara las jugadas ya valoradas en esta búsqueda;
   las que faltan podrían ser mejores. Aquí las dos variables dicen lo
   mismo, $\text{d2}\textbf{x}\text{c3}$, porque es la primera que se
   probó. Pero `mejor_jugada` no lo sabe: $\text{d2}\textbf{-}\text{d3}$,
   la que gana, estaba sin valorar.
:::

## 5 · Trazar la tercera búsqueda en T

**Piensa: con $d=3$, centro va primero. ¿Qué podan I y D con lo que centro
ya aseguró?**

Las dos primeras búsquedas dan lo mismo que sin poda. Con $d=1$, R ve 5, 4
y 7: deja lista der con 4 nodos. Con $d=2$ prueba der primero, luego izq y
centro; ve 2, 3 y 6 sin cortes y deja lista centro con 10 nodos.

La tercera búsqueda prueba centro primero. Cómo leer su traza:

- **línea · pila:** la línea que corre y el camino desde R al nodo activo.
- **$(\alpha,\beta)$:** la ventana del nodo activo **al terminar** la
  fila, como en la clase 2.
- **$v$:** el de ese nodo. En las filas de R, su $\alpha$, que hace de
  `mejor_valor`.
- **$w$:** lo que acaba de devolver un hijo; entre paréntesis, cuál.
- **corta:** la comparación de la fila: $v\ge\beta$ en un nodo de MAX,
  $v\le\alpha$ en uno de MIN, $w>\alpha$ en R.

::: exercise {#jue-c3-ej-traza-d3 title="Completa la búsqueda con d = 3"}
ALFA-BETA-CON-CORTE en T, con $d=3$ en la raíz y R probando centro, izq,
der. Dentro de C, primero C1.

| # | línea · pila | $(\alpha,\beta)$ | $v$ | $w$ | corta | `mejor_jugada` |
|---|---|---|---|---|---|---|
| 1 | 5 · R | $(-\infty,+\infty)$ | $-\infty$ |  |  | ? |
| 2 | 26 · R›C | ? | $+\infty$ |  |  | centro |
| 3 | 18 · R›C›C1 | $(-\infty,+\infty)$ | $-\infty$ |  |  | centro |
| 4 | 20–23 · R›C›C1 | ? | 5 | 5 | ? | centro |
| 5 | 20–23 · R›C›C1 | $(5,+\infty)$ | 5 | 2 | $5\ge+\infty$ no | centro |
| 6 | 28–31 · R›C | ? | 5 | 5 (C1) | $5\le-\infty$ no | centro |
| 7 | 18 · R›C›C2 | ? | $-\infty$ |  |  | centro |
| 8 | 20–22 · R›C›C2 | $(-\infty,5)$ | 7 | 7 | ? | centro |
| 9 | 28–31 · R›C | $(-\infty,5)$ | 5 | 7 (C2) | $5\le-\infty$ no | centro |
| 10 | 7–10 · R | ? | 5 | 5 (C) | ? | centro |
| 11 | 26 · R›I | $(5,+\infty)$ | $+\infty$ |  |  | centro |
| 12 | 28–30 · R›I | $(5,+\infty)$ | ? | 3 | ? | centro |
| 13 | 7–10 · R | $(5,+\infty)$ | 5 | 3 (I) | ? | centro |
| 14 | 26 · R›D | $(5,+\infty)$ | $+\infty$ |  |  | centro |
| 15 | 28–30 · R›D | $(5,+\infty)$ | 2 | 2 | ? | centro |
| 16 | 7–10 · R | $(5,+\infty)$ | ? | 2 (D) | $2>5$ no | centro |
| 17 | 11–12 · R | $(5,+\infty)$ | 5 |  |  | centro |

1. Llena los «?».
2. ¿Qué hojas no se generan? ¿Cuántos nodos genera la búsqueda?
3. ¿Qué devuelven I y D: su valor, o un número que solo lo acota?
:::

::: hint {#jue-c3-pista-traza-d3-1 of="jue-c3-ej-traza-d3" title="Una fila de corta"}
En cada fila de corta, di de quién es el nodo, con qué número del rival
compara y en qué línea. Y en la fila 1: ¿qué asigna la línea 5 a
`mejor_jugada`?
:::

::: answer {#jue-c3-resp-traza-d3 of="jue-c3-ej-traza-d3"}
En negrita, lo que era «?».

| # | línea · pila | $(\alpha,\beta)$ | $v$ | $w$ | corta | `mejor_jugada` |
|---|---|---|---|---|---|---|
| 1 | 5 · R | $(-\infty,+\infty)$ | $-\infty$ |  |  | **centro** |
| 2 | 26 · R›C | $\mathbf{(-\infty,+\infty)}$ | $+\infty$ |  |  | centro |
| 3 | 18 · R›C›C1 | $(-\infty,+\infty)$ | $-\infty$ |  |  | centro |
| 4 | 20–23 · R›C›C1 | $\mathbf{(5,+\infty)}$ | 5 | 5 | **5≥+∞ no** | centro |
| 5 | 20–23 · R›C›C1 | $(5,+\infty)$ | 5 | 2 | $5\ge+\infty$ no | centro |
| 6 | 28–31 · R›C | $\mathbf{(-\infty,5)}$ | 5 | 5 (C1) | $5\le-\infty$ no | centro |
| 7 | 18 · R›C›C2 | $\mathbf{(-\infty,5)}$ | $-\infty$ |  |  | centro |
| 8 | 20–22 · R›C›C2 | $(-\infty,5)$ | 7 | 7 | **7≥5 sí** | centro |
| 9 | 28–31 · R›C | $(-\infty,5)$ | 5 | 7 (C2) | $5\le-\infty$ no | centro |
| 10 | 7–10 · R | $\mathbf{(5,+\infty)}$ | 5 | 5 (C) | **5>−∞ sí** | centro |
| 11 | 26 · R›I | $(5,+\infty)$ | $+\infty$ |  |  | centro |
| 12 | 28–30 · R›I | $(5,+\infty)$ | **3** | 3 | **3≤5 sí** | centro |
| 13 | 7–10 · R | $(5,+\infty)$ | 5 | 3 (I) | **3>5 no** | centro |
| 14 | 26 · R›D | $(5,+\infty)$ | $+\infty$ |  |  | centro |
| 15 | 28–30 · R›D | $(5,+\infty)$ | 2 | 2 | **2≤5 sí** | centro |
| 16 | 7–10 · R | $(5,+\infty)$ | **5** | 2 (D) | $2>5$ no | centro |
| 17 | 11–12 · R | $(5,+\infty)$ | 5 |  |  | centro |

1. La línea 5 pone `mejor_jugada ← jugada`: centro, la lista de $d=2$.
2. **C2 es de MAX:** $7\ge5$ → corte beta, línea 22; la hoja 8 no se
   genera. **I y D son de MIN:** $3\le5$ y $2\le5$ → corte alfa, línea
   30; las hojas 6 y 12 no se generan. Se generan **11** nodos: R, C, C1,
   5, 2, C2, 7, I, 3, D y 2.
3. **Cotas.** I devuelve 3 y D devuelve 2, pero solo se sabe que valen
   **a lo más** eso. Basta para saber que no superan a centro.
:::

> **▶ [Recorre las tres búsquedas paso a paso](../_assets/traza_arbol_t.html#iterativa)** — $d=1$, 2 y 3 seguidas, con la jugada anterior primero.

La tabla resume las tres búsquedas.

::: table {#jue-c3-t-iterativa title="Cada búsqueda de la profundización iterativa en el árbol T"}
| $d$ | orden: $w$ | Lista |
|---|---|---|
| 1 | I 5 · C 4 · D 7 | der |
| 2 | **D** 2 · I 3 · C 6 | centro |
| 3 | **C** 5 · I ≤3 · D ≤2 | centro |
:::

- **Cómo leer la tabla:** «orden: $w$» da los hijos de R en el orden en que
  se prueban, con el $w$ que devuelve cada uno. En negrita, el que va
  primero por ser la jugada lista de la búsqueda anterior.
- **Nodos generados:** 4, 10 y 11, en total $4+10+11=25$. Sin poda eran
  $4+10+14=28$.
- **Cortes:** con $d=1$ y $d=2$, ninguno. Con $d=3$, un corte beta en C2
  y dos cortes alfa, en I y en D.
- **$d=1$ deja lista la trampa**, der, y por la línea 6 der va primero con
  $d=2$. Ahí ya se ve que vale 2: la búsqueda corrige la jugada.

::: figure {#jue-c3-t-fig-iterativa title="Profundización iterativa en T: der con d = 1, centro desde d = 2"}
![Tres copias pequeñas del árbol T, una por búsqueda. Con d = 1, la raíz prueba izq, centro y der, ve sus EVAL 5, 4 y 7, genera 4 nodos y deja lista der, con 7. Con d = 2 prueba der primero, luego izq y centro; ve 2, 3 y 6, sin cortes, genera 10 nodos y deja lista centro, con 6. Con d = 3 prueba centro primero y ve 5; poda la hoja 8 con un corte beta en C2 y las hojas 6 y 12 con cortes alfa en I y en D, que devuelven una cota; las hojas podadas son círculos punteados con «?». Genera 11 nodos y deja lista centro, con 5. En total, 25 nodos](../_assets/jue-t-iterativa.svg)
:::

**En la posición de la clase.** Con $d=3$ se prueba primero
$\text{d2}\textbf{-}\text{d3}$, la jugada que dejó lista $d=2$. Vale 100,
y la línea 9 la entrega sin mirar las otras dos. Los valores $-9$ y 1 de la
@jue-c3-reloj-por-d están ahí para comparar, pero el programa ya no los
calcula.

La tabla junta todas las cuentas de nodos de la clase. En T, el orden fijo
es izq, centro, der. En la posición de la clase, el orden fijo va por
casilla de origen: $\text{a1}\textbf{-}\text{a2}$,
$\text{d2}\textbf{-}\text{d3}$, $\text{d2}\textbf{x}\text{c3}$. La
iterativa pone primero la jugada lista y sale con 100 (línea 9).

::: table {#jue-c3-nodos-generados title="Nodos generados por búsqueda, en T y en la posición de la clase"}
| Árbol · algoritmo | $d=1$ | $d=2$ | $d=3$ | Total |
|---|---:|---:|---:|---:|
| T · sin poda | 4 | 10 | 14 | 28 |
| T · alfa-beta, orden fijo | 4 | 9 | 12 | 25 |
| T · iterativa | 4 | 10 | 11 | 25 |
| 4×4 · sin poda | 4 | 12 | 33 | 49 |
| 4×4 · alfa-beta, orden fijo, sin salida en 100 | 4 | 12 | 22 | 38 |
| 4×4 · iterativa | 4 | 10 | 9 | 23 |
:::

- **En T, la iterativa no ahorra frente a alfa-beta con orden fijo:** los
  dos suman 25. Gana uno con $d=3$ (11 contra 12), pero pierde uno con
  $d=2$, porque prueba primero la trampa der (10 contra 9).
- **En la posición de la clase sí ahorra:** 23 contra 38. Casi todo el
  ahorro está en $d=3$, 9 contra 22: la jugada que va primero gana, y la
  línea 9 sale sin mirar más.

## 6 · Recordar posiciones ya valoradas

**Piensa: si dos órdenes de jugadas llegan al mismo tablero, ¿hace falta
valorarlo dos veces?**

Como en [[minimax-como-algoritmo|minimax]], un estado al que se llega por
varios caminos —una **transposición**— no hace falta valorarlo dos veces.
Una **tabla de transposición** guarda cada estado ya valorado. Con corte y
con poda, guardar «el estado y su valor» no basta. Cada entrada guarda tres
cosas:

- **El número** que devolvió la búsqueda.
- **La profundidad que quedaba**, $d$. Un número calculado con $d=1$ no
  sirve a una búsqueda que llega con $d=3$: miró menos. Solo se reutiliza
  si se calculó con al menos la profundidad que queda ahora.
- **Qué clase de número es**, según la ventana $(\alpha,\beta)$ con que se
  llamó al nodo y el $v$ que devolvió:
  - **exacto**, si $\alpha<v<\beta$: es su valor con corte;
  - **piso**, si $v\ge\beta$: el valor es **al menos** $v$;
  - **techo**, si $v\le\alpha$: el valor es **a lo más** $v$.

La clase se lee de la ventana, no de si el nodo cortó. Un nodo puede
devolver una cota sin haber cortado él: basta con que corten sus hijos y
le devuelvan cotas.

::: table {#jue-c3-transposicion-iterativa title="Clase de cada número en la búsqueda con d = 3, centro primero"}
| Nodo | Ventana al llegar | $v$ | Clase |
|---|---|---:|---|
| C | $(-\infty,+\infty)$ | 5 | exacto |
| C1 | $(-\infty,+\infty)$ | 5 | exacto |
| C2 | $(-\infty,5)$ | 7 | piso |
| I | $(5,+\infty)$ | 3 | techo |
| D | $(5,+\infty)$ | 2 | techo |
:::

Un techo de 3 en I no sirve para decir «I vale 3». Sirve para descartar I
en cualquier búsqueda donde MAX ya asegure 3 o más.

::: exercise {#jue-c3-ej-clase title="Clasifica lo que se guarda"}
Ahora alfa-beta con $d=3$ y el orden fijo: R prueba izq, centro, der.
I llega con $(-\infty,+\infty)$ y devuelve 3. C2 llega con $(3,5)$ y
devuelve 7. D llega con $(5,+\infty)$ y devuelve 2.

1. ¿Qué clase de número guarda la tabla para I, para C2 y para D?
2. Compara I con la tabla de arriba. ¿Por qué cambia su clase?
:::

::: hint {#jue-c3-pista-clase-1 of="jue-c3-ej-clase" title="Con cuál extremo"}
Para cada nodo, ¿su $v$ cae dentro de la ventana, o toca o pasa uno de los
extremos? ¿Cuál?
:::

::: answer {#jue-c3-resp-clase of="jue-c3-ej-clase"}
1. **I: exacto**, porque $-\infty<3<+\infty$. **C2: piso**, porque
   $7\ge5$. **D: techo**, porque $2\le5$.
2. Con el orden fijo, I va primero y llega sin nada asegurado: su 3 es su
   valor. Con centro primero, I llega con $\alpha=5$, corta tras la hoja 3
   y su 3 solo es un techo. **El mismo nodo cambia de clase porque cambió
   la ventana con que se llamó.**
:::

## 7 · Resolver un caso por tu cuenta

**Piensa: si cambias el orden inicial de las jugadas, ¿qué cambia, la
jugada que se entrega o lo que cuesta llegar a ella?**

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-reloj title="Corre la iterativa con otro orden y un reloj"}
Mismo árbol T y misma $\mathrm{EVAL}$ (I 5, C 4, D 7, C1 6, C2 9). Lo que
cambia es el orden de $A(R)$: **der, centro, izq**. Así la línea 2 deja
$\text{jugada}=\text{der}$. Dentro de C, primero C1, como siempre.

Dos simplificaciones. El reloj se mide en **nodos generados**, contando
las tres búsquedas seguidas, raíz incluida en cada una. Y se mira solo en
las líneas 4 y 8: se acaba cuando la cuenta llega al tope.

1. Corre PROFUNDIZACIÓN-ITERATIVA con $d=1$, 2 y 3. Para cada búsqueda, da
   el orden en que R prueba sus hijos, la jugada lista y los nodos
   generados.
2. ¿Dónde se poda con $d=2$? ¿Por qué con el orden de la página no se
   podaba?
3. ¿Cuántos nodos suman las tres búsquedas? Compáralo con los 25 de la
   página.
4. Con un reloj de 10 nodos, ¿qué línea actúa y qué jugada se entrega? ¿Y
   con uno de 20?
:::

::: hint {#jue-c3-pista-final-reloj-1 of="jue-c3-ej-final-reloj" title="Pista 1 · Qué va primero"}
Antes de cada búsqueda, ¿qué jugada está lista y dónde la pone la línea
6? Después, para cada hijo de R, ¿con qué $\alpha$ llega?
:::

::: hint {#jue-c3-pista-final-reloj-2 of="jue-c3-ej-final-reloj" title="Pista 2 · Revisa la cuenta del reloj"}
Comprueba tu respuesta con dos preguntas. ¿Cuántos nodos llevas en total
cada vez que un hijo de R devuelve su $w$? Cuando la cuenta llega al tope,
¿la búsqueda en curso ya había terminado?
:::

::: answer {#jue-c3-resp-final-reloj of="jue-c3-ej-final-reloj"}
**1. Las tres búsquedas.**

| $d$ | Orden de R | Lista | Nodos |
|---|---|---|---:|
| 1 | der, centro, izq | der | 4 |
| 2 | der, centro, izq | centro | 9 |
| 3 | centro, der, izq | centro | 11 |

Con $d=1$, R ve 7, 4 y 5: queda der, la trampa. Con $d=2$, der va primero
y vale 2; centro vale 6. Con $d=3$, centro va primero y vale 5; der e izq
se cortan tras su primera hoja.

**2. La poda con $d=2$.** I llega con $\alpha=6$, porque centro ya se
valoró. Su primera hoja es 3, y $3\le6$: corte alfa, la hoja 6 no se
genera. Con el orden de la página, I iba segunda, con $\alpha=2$, y
$3\le2$ es falso.

**3. El total.** $4+9+11=$ **24** nodos, uno menos que los 25 de la
página. La jugada entregada es la misma, centro.

**4. El reloj.** Con 10 nodos: la primera búsqueda termina en 4. La
segunda llega a 8 tras der, y a 11 tras centro. La línea 8 ve el reloj
agotado y entrega **der**, de $d=1$: la trampa. Con 20 nodos: la segunda
búsqueda termina en 13. La tercera llega a 20 tras centro, y la línea 8
entrega **centro**, de $d=2$.

El orden cambió lo que cuesta, no la jugada final. Pero con poco tiempo
decide qué se entrega: con este orden, un reloj corto entrega la trampa.
:::

**Punto de control:** deberías poder decir qué entrega
PROFUNDIZACIÓN-ITERATIVA si el reloj se acaba entre dos hijos de la raíz
(línea 8) y si un hijo devuelve 100 (línea 9). También, por qué la jugada
lista va primero, y si un número guardado es exacto, piso o techo según su
ventana.

## Para profundizar

**Deep Blue venció a Kasparov en 1997** con estas mismas piezas, a escala
mucho mayor. Buscaba con alfa-beta, en paralelo y con hardware propio, y
evaluaba con una función compleja ajustada casi toda a mano.

## Lo que hay que llevarse

- La profundización iterativa busca con $d=1,2,3,\dots$ y entrega lo mejor
  de la **última búsqueda completa**. En la posición de la clase, un reloj
  que se acaba durante $d=2$ entrega $\text{d2}\textbf{x}\text{c3}$, que
  pierde; durante $d=3$, $\text{d2}\textbf{-}\text{d3}$, que gana.
- Repetir cuesta cerca de $1/(b-1)$ de la última búsqueda: 16 nodos
  contra 33 en la posición de la clase, sin poda.
- La versión corta llama entera a DECIDIR-CON-CORTE. La completa usa
  alfa-beta con $\alpha$ compartido (7), prueba primero la jugada anterior
  (6), mira el reloj entre hijos (8) y sale con 100 (9).
- En T: 28 nodos sin poda, 25 con la iterativa (4 + 10 + 11), igual que
  alfa-beta con orden fijo. En la posición de la clase: 49, 38 y 23.
- La tabla de transposición guarda número, profundidad y clase: exacto si
  $\alpha<v<\beta$, piso si $v\ge\beta$, techo si $v\le\alpha$, según la
  ventana con que se llamó.

Continúa con [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].
