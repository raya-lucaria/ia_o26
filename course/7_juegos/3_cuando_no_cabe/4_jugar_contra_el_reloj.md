---
id: jugar-contra-el-reloj
title: Jugar contra el reloj
nav_title: Jugar contra el reloj
summary: "Si no sabes cuánto tiempo queda, buscas con d = 1, luego con 2, luego con 3, y entregas lo de la última búsqueda completa. Primero sin poda; después con alfa-beta, la jugada anterior primero y una tabla que guarda si cada número es un valor, un piso o un techo."
status: ready
estimated_time: 37m
tags: [juegos, busqueda-adversarial, evaluacion, algoritmos]
---

# Jugar contra el reloj

**¿Qué jugada entregamos si se acaba el tiempo?**

Al terminar tendrás:

- decir, en la posición de la clase, **qué jugada entrega** un programa
  según cuándo se acaba el reloj;
- **la profundización iterativa** en dos versiones: una corta sin poda, y
  la completa con alfa-beta, línea por línea lo que cambia entre ellas;
- la **traza de la búsqueda con ${d=3}$** en el árbol T: qué se poda, dónde
  y por qué;
- la regla para guardar un número en una **tabla de transposición**:
  un valor dentro de la ventana, un piso o un techo.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Un peón avanza una casilla si está vacía o captura en diagonal
> hacia delante. Gana quien llega a la fila del rival, captura todo o deja
> al rival sin jugada. ${U=+1}$ si gana Blancas y ${U=-1}$ si gana Negras.

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

> [!TIP]
> **Míralo correr: profundización iterativa en el árbol T**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#iterativa)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 7: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

Seguimos con la posición de [[cortar-y-evaluar|Cortar y evaluar a mano]] y la
misma evaluación, ${\mathrm{EVAL}=10\cdot\text{material}+\text{avance}}$. En
los finales, ${100\cdot U=\pm100}$. Como allá, $d$ es **la profundidad que
queda**: en la raíz, la de toda la búsqueda.

::: table {#jue-c3-posicion-reloj title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

## 1 · Profundizar poco a poco

**Piensa: si no sabes cuánto tiempo te queda, ¿con qué profundidad buscas?**

En [[mas-alla-del-horizonte|Más allá del horizonte]] viste que una
profundidad fija puede dejar la respuesta decisiva detrás del corte. Mirar
más hondo ayuda, pero cuesta tiempo.

En un torneo hay reloj: el tablero espera, el reloj no. Si eliges $d$
demasiado grande, el tiempo se acaba a mitad de la búsqueda y no tienes
jugada. Si lo eliges pequeño, desperdicias tiempo y juegas peor.

La salida es no elegir: **buscar con ${d=1}$, luego con ${d=2}$, luego con
${d=3}$**, mientras haya tiempo. Cuando el reloj se acaba, se juega la mejor
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
${d=1,2,3,\dots}$ mientras quede tiempo. Guarda la mejor jugada de cada
búsqueda que termina, y al acabarse el reloj entrega la de la última
búsqueda completa.
:::

**Estamos aquí:** la posición de la clase, mueven Blancas. La tabla da el
valor con corte de cada jugada en las tres primeras búsquedas.

::: table {#jue-c3-reloj-por-d title="Valor de cada jugada de Blancas en cada búsqueda"}
| $d$ | $\text{a1}\textbf{-}\text{a2}$ | $\text{d2}\textbf{-}\text{d3}$ | $\text{d2}\textbf{x}\text{c3}$ |
|---|---:|---:|---:|
| 1 | 2 | 2 | 13 |
| 2 | −10 | 1 | 0 |
| 3 | −9 | 100 | 1 |
:::

::: exercise {#jue-c3-ej-reloj title="Encuentra la jugada que se entrega"}
Para cada caso, ¿qué jugada entrega el programa?

1. El reloj se acaba mientras busca con ${d=2}$.
2. El reloj se acaba mientras busca con ${d=3}$.
3. El reloj alcanza para terminar ${d=3}$.
:::

::: hint {#jue-c3-pista-reloj-1 of="jue-c3-ej-reloj" title="Fila por fila"}
En cada caso, ¿cuáles búsquedas terminaron antes de que sonara el reloj?
De la última de ellas, ¿qué columna tiene el número mayor?
:::

::: answer {#jue-c3-resp-reloj of="jue-c3-ej-reloj"}
1. La última búsqueda completa es ${d=1}$, y su mayor número es 13:
   entrega **$\text{d2}\textbf{x}\text{c3}$**, que pierde.
2. La última completa es ${d=2}$, con 1: entrega
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
${d=1}$, el programa captura y pierde.**

## 2 · Contar lo que cuesta repetir

**Piensa: buscar con ${d=1}$, luego con ${d=2}$ y luego con ${d=3}$, ¿no es
trabajar tres veces?**

Sí se repite trabajo, pero poco. Con ramificación $b$ —a lo más $b$ jugadas
por estado—, la búsqueda con $d$ en la raíz tiene del orden de $b^d$ hojas.
Todas las búsquedas anteriores juntas suman

$$b+b^2+\dots+b^{d-1}=\frac{b^d-b}{b-1}<\frac{b^d}{b-1}.$$

::: remark {#jue-c3-costo-iterativa title="Costo de la profundización iterativa"}
Si la última búsqueda completa llega a $d$ en la raíz, las anteriores juntas
cuestan cerca de ${1/(b-1)}$ de esa última. El tiempo total es

$$\text{tiempo}=O\!\left(b^d\cdot\frac{b}{b-1}\right)=O(b^d),$$

el mismo orden que una sola búsqueda a profundidad $d$. Con ${b=10}$, repetir
añade cerca de una novena parte. Con ${b=2}$, las anteriores cuestan casi lo
mismo que la última, y el total es cerca del doble.
:::

La última búsqueda domina el costo. Repetir las otras es casi gratis cuando
$b$ es grande.

::: exercise {#jue-c3-ej-costo title="Calcula lo que se repite"}
Usa las barras de la figura: 4, 12 y 33 nodos.

1. ¿Cuántos nodos genera en total profundizar hasta terminar ${d=3}$?
2. ¿Cuántos de ellos son repetición? ¿Es más o menos que la mitad de la
   última búsqueda?
:::

::: hint {#jue-c3-pista-costo-1 of="jue-c3-ej-costo" title="Qué se habría hecho igual"}
Un programa que supiera de antemano que llega a ${d=3}$, ¿qué búsquedas
habría hecho? Lo demás es lo que se repite.
:::

::: answer {#jue-c3-resp-costo of="jue-c3-ej-costo"}
1. ${4+12+33=}$ **49** nodos.
2. Se repiten las búsquedas con ${d=1}$ y ${d=2}$: ${4+12=}$ **16** nodos,
   **menos de la mitad** de los 33 de la última. Aquí $b$ no es fijo
   —ningún nodo de estas búsquedas tiene más de 5 jugadas—, así que la
   cuenta de ${1/(b-1)}$ es una guía, no una igualdad.
:::

## 3 · Escribir la versión sin poda

**Piensa: ¿qué le falta a DECIDIR-CON-CORTE para jugar contra un reloj?**

Solo un ciclo alrededor: llamarla con ${d=1,2,3,\dots}$ y recordar la jugada
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

- **${d=1}$ deja lista la trampa:** der parece valer 7, pero con ${d=2}$ vale
  2.
- **${d=2}$ corrige la jugada:** centro, con 6. Con ${d=3}$ sigue centro, con
  5.
- Las tres búsquedas generan ${4+10+14=28}$ nodos. Si el reloj se acaba
  durante ${d=2}$, se entrega der; durante ${d=3}$, centro.

::: exercise {#jue-c3-ej-orden-sin-poda title="Comprueba si el orden importa"}
Cambia el orden en que R prueba sus hijos: en cada búsqueda va primero la
jugada lista de la anterior. Con ${d=2}$, R prueba der, izq, centro; con
${d=3}$, centro, izq, der.

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
[[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]].

Para aprovecharlo, se abre la línea 5 de la versión corta: en vez de una
sola llamada a DECIDIR-CON-CORTE, el ciclo sobre los hijos de la raíz
queda a la vista. Ahí entran cuatro cambios, y los números de línea son
los del bloque completo.

Los nombres nuevos:

- **$\alpha$:** lo que MAX ya asegura en la raíz durante la búsqueda en
  curso: hace de `mejor_valor`.
- **`mejor_jugada`:** la mejor de la búsqueda **en curso**, como en
  DECIDIR.
- **$w$:** lo que devuelve un hijo de la raíz.

El bloque completo va primero: PROFUNDIZACIÓN-ITERATIVA, en las líneas
1–13, y su auxiliar, ALFA-BETA-CON-CORTE, en las líneas 14–32. Debajo, los
cuatro cambios lo recorren de uno en uno.

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

**Cambio 1 · Valorar cada hijo con alfa-beta.** La raíz recorre sus hijos
como DECIDIR-ALFA-BETA. La línea 5 pone ${\alpha=-\infty}$. La línea 7
valora cada hijo con ALFA-BETA-CON-CORTE y le pasa la ventana
${(\alpha,+\infty)}$: el hijo recibe lo que la raíz ya asegura. Si ${w>\alpha}$,
la línea 10 sube $\alpha$ y anota la jugada en `mejor_jugada`.

**Cambio 2 · La jugada anterior primero.** La línea 6 recorre $A(s)$
empezando por `jugada`, la que dejó lista la búsqueda anterior. Sin poda,
el orden no cambiaba nada. Con alfa-beta, si esa jugada es buena, $\alpha$
sube con el primer hijo y los demás se podan antes.

**Cambio 3 · El reloj entre dos hijos.** La versión corta miraba el reloj
solo al terminar cada búsqueda. La línea 8 lo mira tras cada hijo de la
raíz. Si se acabó, la búsqueda en curso no cuenta y se entrega `jugada`.

**Cambio 4 · La salida con 100.** Si un hijo devuelve 100, gana seguro y
no hay nada mejor que buscar: la línea 9 lo entrega en ese momento.

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

**Lo que queda igual y lo que viene de otro lado:**

- **Se quedan igual** las líneas 2, 3, 4, 12 y 13: son las 2, 3, 4, 8 y 9
  de la versión corta. La 11, `jugada ← mejor_jugada`, es su línea 7.
- **Las líneas 5, 7 y 10 son DECIDIR-ALFA-BETA** (sus líneas 2, 4 y 5), y
  la 6 es su línea 3 con otro orden.
- **La línea 8 se pasa del tiempo** si un hijo tarda mucho: espera a que
  ese hijo termine. Un programa real mira el reloj también por dentro.
- **La línea 9 no se confunde con una estimación.** Como
  ${|\mathrm{EVAL}|\le36}$ en las posiciones alcanzables que no son
  finales, un 100 solo viene de finales ganados.

Las líneas 14–32 son el
[[alfa-beta-como-algoritmo|ALFA-BETA de la clase 2]] con lo de
[[minimax-con-corte|minimax con corte]]. La tabla pone cada línea junto a
la suya:

::: table {#jue-c3-lineas-alfa-beta title="ALFA-BETA-CON-CORTE contra el ALFA-BETA de la clase 2"}
| Aquí | Clase 2 | Qué cambia |
|---|---|---|
| 14 | 7 | recibe $d$ |
| 15 | 8 | el final vale ${100\cdot U}$ |
| 16 | — | nueva: con ${d=0}$ se estima |
| 17–⁠32 | 9–⁠24 | nada, salvo ${d-1}$ en 20 y 28 |
:::

- **Por la línea 16, todo queda corrido en uno:** el corte beta, su 14, es
  aquí la 22; el corte alfa, su 22, es aquí la 30.

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
${d=2}$. Ya se valoró $\text{d2}\textbf{x}\text{c3}$, que va primero, y
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
   completa: con ${d=1}$ era **$\text{d2}\textbf{x}\text{c3}$**.
2. `mejor_jugada` solo compara las jugadas ya valoradas en esta búsqueda;
   las que faltan podrían ser mejores. Aquí las dos variables dicen lo
   mismo, $\text{d2}\textbf{x}\text{c3}$, porque es la primera que se
   probó. Pero `mejor_jugada` no lo sabe: $\text{d2}\textbf{-}\text{d3}$,
   la que gana, estaba sin valorar.
:::

## 5 · Trazar la tercera búsqueda en T

**Piensa: con ${d=3}$, centro va primero. ¿Qué podan I y D con lo que centro
ya aseguró?**

Las dos primeras búsquedas dan lo mismo que sin poda. Con ${d=1}$, R ve
5, 4 y 7: deja lista der con 4 nodos. Con ${d=2}$ prueba der primero,
luego izq y centro; ve 2, 3 y 6 sin cortes y deja lista centro con 10
nodos.

La tercera búsqueda prueba centro primero, luego izq y der. Dentro de C,
primero C1. Cada tramo va en dos tablas con el mismo número de fila: dónde
está la búsqueda y qué números maneja.

- **línea · pila:** la línea que corre y el camino desde R al nodo activo.
- **$(\alpha,\beta)$:** la ventana del nodo activo **al terminar** la
  fila, como en la clase 2.
- **$v$:** el de ese nodo. En las filas de R, su $\alpha$, que hace de
  `mejor_valor`.
- **$w$:** lo que acaba de devolver un hijo; entre paréntesis, cuál.
- **compara:** la comparación de la fila. En un nodo de MAX,
  ${v\ge\beta}$, y un «sí» es un corte beta. En uno de MIN,
  ${v\le\alpha}$, y un «sí» es un corte alfa. En R, ${w>\alpha}$ de
  la línea 10: un «sí» no corta nada, solo sube $\alpha$.
- **`mejor_jugada`** vale centro en las 17 filas: la línea 5 la pone así y
  ningún hijo la supera.

### Tramo 1 · Centro asegura 5

::: table {#jue-c3-t-traza-d3-donde title="Búsqueda con d = 3, tramo 1: dónde está"}
| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 1 | 5 · R | (−∞,+∞) |
| 2 | 26 · R›C | (−∞,+∞) |
| 3 | 18 · R›C›C1 | (−∞,+∞) |
| 4 | 20–23 · R›C›C1 | (5,+∞) |
| 5 | 20–23 · R›C›C1 | (5,+∞) |
| 6 | 28–31 · R›C | (−∞,5) |
| 7 | 18 · R›C›C2 | (−∞,5) |
| 8 | 20–22 · R›C›C2 | (−∞,5) |
| 9 | 28–31 · R›C | (−∞,5) |
| 10 | 7–10 · R | (5,+∞) |
:::

::: table {#jue-c3-t-traza-d3-numeros title="Búsqueda con d = 3, tramo 1: qué números maneja"}
| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 1 | −∞ |  |  |
| 2 | +∞ |  |  |
| 3 | −∞ |  |  |
| 4 | 5 | 5 | 5≥+∞: no |
| 5 | 5 | 2 | 5≥+∞: no |
| 6 | 5 | 5 (C1) | 5≤−∞: no |
| 7 | −∞ |  |  |
| 8 | 7 | 7 | 7≥5: sí |
| 9 | 5 | 7 (C2) | 5≤−∞: no |
| 10 | 5 | 5 (C) | 5>−∞: sí |
:::

- **Fila 1:** la línea 5 pone ${\alpha=-\infty}$ y
  `mejor_jugada ← jugada`: centro, la que dejó lista ${d=2}$.
- **Fila 6:** C es de MIN y recibe 5 de C1. Su $\beta$ baja a 5: la
  ventana de C pasa a ser ${(-\infty,5)}$, y con ella llama a C2.
- **Fila 8:** C2 es de MAX y su primera hoja vale 7. Como ${7\ge5}$,
  corta en la línea 22: la hoja 8 no se genera. C2 devuelve 7, y C se
  queda con 5.
- **Fila 10:** ${5>-\infty}$, así que la línea 10 sube $\alpha$ a 5.

Al cerrar el tramo 1, C vale 5, C1 vale 5 y C2 devolvió 7, con la hoja 8
podada.

### Tramo 2 · Izq y der, con alfa en 5

::: exercise {#jue-c3-ej-traza-d3 title="Completa el tramo 2 de la búsqueda con d = 3"}
Sigue la misma búsqueda desde la fila 11: R prueba izq y luego der.

| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 11 | 26 · R›I | ? |
| 12 | 28–30 · R›I | ? |
| 13 | 7–10 · R | (5,+∞) |
| 14 | 26 · R›D | ? |
| 15 | 28–30 · R›D | ? |
| 16 | 7–10 · R | (5,+∞) |
| 17 | 11–12 · R | ? |

| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 11 | +∞ |  |  |
| 12 | ? | 3 | ? |
| 13 | 5 | 3 (I) | ? |
| 14 | +∞ |  |  |
| 15 | 2 | 2 | ? |
| 16 | ? | 2 (D) | ? |
| 17 | ? |  |  |

1. Llena los «?».
2. ¿Qué hojas de I y de D no se generan? Contando el tramo 1, ¿cuántos
   nodos genera la búsqueda?
3. ¿Qué devuelven I y D: su valor, o un número que solo lo acota?
:::

::: hint {#jue-c3-pista-traza-d3-1 of="jue-c3-ej-traza-d3" title="Qué compara cada fila"}
En cada fila de compara, ¿de quién es el nodo: de MAX, de MIN o es R? ¿Con
qué número compara su $v$ o su $w$, y en qué línea?
:::

::: answer {#jue-c3-resp-traza-d3 of="jue-c3-ej-traza-d3"}
En negrita, lo que era «?».

| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 11 | 26 · R›I | **(5,+∞)** |
| 12 | 28–30 · R›I | **(5,+∞)** |
| 13 | 7–10 · R | (5,+∞) |
| 14 | 26 · R›D | **(5,+∞)** |
| 15 | 28–30 · R›D | **(5,+∞)** |
| 16 | 7–10 · R | (5,+∞) |
| 17 | 11–12 · R | **(5,+∞)** |

| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 11 | +∞ |  |  |
| 12 | **3** | 3 | **3≤5: sí** |
| 13 | 5 | 3 (I) | **3>5: no** |
| 14 | +∞ |  |  |
| 15 | 2 | 2 | **2≤5: sí** |
| 16 | **5** | 2 (D) | **2>5: no** |
| 17 | **5** |  |  |

1. **I y D son de MIN** y llegan con ${\alpha=5}$. Su primera hoja, 3
   y 2, ya cumple ${v\le\alpha}$: corte alfa en la línea 30. En R, ni
   3 ni 2 superan 5, así que $\alpha$ y `mejor_jugada` no cambian.
2. No se generan las hojas 6 (de I) y 12 (de D); en el tramo 1 tampoco
   se generó la 8. Se generan **11** nodos: R, C, C1, 5, 2, C2, 7, I, 3,
   D y 2.
3. **Cotas.** I devuelve 3 y D devuelve 2, pero solo se sabe que valen
   **a lo más** eso. Basta para saber que no superan a centro.
:::

> **▶ [Recorre las tres búsquedas paso a paso](../_assets/traza_arbol_t.html#iterativa)** — ${d=1}$, 2 y 3 seguidas, con la jugada anterior primero.

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
- **Nodos generados:** 4, 10 y 11, que suman 25. Sin poda eran 28 (4, 10
  y 14).
- **Cortes:** con ${d=1}$ y ${d=2}$, ninguno. Con ${d=3}$, un corte beta en C2
  y dos cortes alfa, en I y en D.
- **${d=1}$ deja lista la trampa**, der, y por la línea 6 der va primero con
  ${d=2}$. Ahí ya se ve que vale 2: la búsqueda corrige la jugada.

::: figure {#jue-c3-t-fig-iterativa title="Profundización iterativa en T: der con d = 1, centro desde d = 2"}
![Tres copias pequeñas del árbol T, una por búsqueda. Con d = 1, la raíz prueba izq, centro y der, ve sus EVAL 5, 4 y 7, genera 4 nodos y deja lista der, con 7. Con d = 2 prueba der primero, luego izq y centro; ve 2, 3 y 6, sin cortes, genera 10 nodos y deja lista centro, con 6. Con d = 3 prueba centro primero y ve 5; poda la hoja 8 con un corte beta en C2 y las hojas 6 y 12 con cortes alfa en I y en D, que devuelven una cota; las hojas podadas son círculos punteados con «?». Genera 11 nodos y deja lista centro, con 5. En total, 25 nodos](../_assets/jue-t-iterativa.svg)
:::

**En la posición de la clase.** Con ${d=3}$ se prueba primero
$\text{d2}\textbf{-}\text{d3}$, la jugada que dejó lista ${d=2}$. Vale 100,
y la línea 9 la entrega sin mirar las otras dos. Los valores $-9$ y 1 de la
@jue-c3-reloj-por-d están ahí para comparar, pero el programa ya no los
calcula.

Las dos tablas juntan todas las cuentas de nodos de la clase. En T, el orden fijo
es izq, centro, der.

En la posición de la clase, el orden fijo va por la fila de la casilla de
origen, de la 1 a la 4, y dentro de la fila por columna, de a a d. En cada
peón va primero el avance y luego las capturas. Para Blancas da $\text{a1}\textbf{-}\text{a2}$,
$\text{d2}\textbf{-}\text{d3}$, $\text{d2}\textbf{x}\text{c3}$. La
iterativa pone primero la jugada lista y sale con 100 (línea 9).

::: table {#jue-c3-nodos-generados title="Nodos generados en el árbol T, por búsqueda"}
| $d$ | sin poda | α-β fijo | iterativa |
|---|---:|---:|---:|
| 1 | 4 | 4 | 4 |
| 2 | 10 | 9 | 10 |
| 3 | 14 | 12 | 11 |
| Total | 28 | 25 | 25 |
:::

::: table {#jue-c3-nodos-generados-posicion title="Nodos generados en la posición de la clase, por búsqueda"}
| $d$ | sin poda | α-β fijo | iterativa |
|---|---:|---:|---:|
| 1 | 4 | 4 | 4 |
| 2 | 12 | 12 | 10 |
| 3 | 33 | 22 | 9 |
| Total | 49 | 38 | 23 |
:::

«α-β fijo» es alfa-beta con el orden fijo y sin la salida en 100.

- **En T, la iterativa no ahorra frente a alfa-beta con orden fijo:** los
  dos suman 25. Gana uno con ${d=3}$ (11 contra 12), pero pierde uno con
  ${d=2}$, porque prueba primero la trampa der (10 contra 9).
- **En la posición de la clase sí ahorra:** 23 contra 38. Casi todo el
  ahorro está en ${d=3}$, 9 contra 22: la jugada que va primero gana, y la
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
- **La profundidad que quedaba**, $d$. Un número calculado con ${d=1}$ no
  sirve a una búsqueda que llega con ${d=3}$: miró menos. Solo se reutiliza
  si se calculó con al menos la profundidad que queda ahora.
- **Qué tipo de número es**, según la ventana $(\alpha,\beta)$ con que se
  llamó al nodo y el $v$ que devolvió:
  - **valor**, si ${\alpha<v<\beta}$: cae dentro de la ventana y es su
    valor con corte;
  - **piso**, si ${v\ge\beta}$: el valor es **al menos** $v$;
  - **techo**, si ${v\le\alpha}$: el valor es **a lo más** $v$.

Ojo con los nombres: en [[alfa-beta|Alfa-beta a mano]], $\alpha$ era un
piso y $\beta$ un techo. Aquí piso y techo describen el número guardado,
no la ventana: tocar $\beta$ deja un piso.

El tipo se lee de la ventana, no de si el nodo cortó. Un nodo puede
devolver una cota sin haber cortado él: basta con que corten sus hijos y
le devuelvan cotas.

::: table {#jue-c3-transposicion-iterativa title="Tipo de cada número en la búsqueda con d = 3, centro primero"}
| Nodo | Ventana al llegar | $v$ | Tipo |
|---|---|---:|---|
| C | (−∞,+∞) | 5 | valor |
| C1 | (−∞,+∞) | 5 | valor |
| C2 | (−∞,5) | 7 | piso |
| I | (5,+∞) | 3 | techo |
| D | (5,+∞) | 2 | techo |
:::

Un techo de 3 en I no sirve para decir «I vale 3». Sirve para descartar I
en cualquier búsqueda donde MAX ya asegure 3 o más.

::: exercise {#jue-c3-ej-clase title="Clasifica lo que se guarda"}
Ahora alfa-beta con ${d=3}$ y el orden fijo: R prueba izq, centro, der.
I llega con ${(-\infty,+\infty)}$ y devuelve 3. C2 llega con $(3,5)$ y
devuelve 7. D llega con ${(5,+\infty)}$ y devuelve 2.

1. ¿Qué tipo de número guarda la tabla para I, para C2 y para D?
2. Compara I con la tabla de arriba. ¿Por qué cambia su tipo?
:::

::: hint {#jue-c3-pista-clase-1 of="jue-c3-ej-clase" title="Con cuál extremo"}
Para cada nodo, ¿su $v$ cae dentro de la ventana, o toca o pasa uno de los
extremos? ¿Cuál?
:::

::: answer {#jue-c3-resp-clase of="jue-c3-ej-clase"}
1. **I: valor**, porque 3 cae dentro de ${(-\infty,+\infty)}$. **C2:
   piso**, porque ${7\ge5}$. **D: techo**, porque ${2\le5}$.
2. Con el orden fijo, I va primero y llega sin nada asegurado: su 3 es su
   valor. Con centro primero, I llega con ${\alpha=5}$, corta tras la
   hoja 3 y su 3 solo es un techo. **El mismo nodo cambia de tipo porque
   cambió la ventana con que se llamó.**
:::

## 7 · Resolver un caso por tu cuenta

**Piensa: si cambias el orden inicial de las jugadas, ¿qué cambia, la
jugada que se entrega o lo que cuesta llegar a ella?**

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-reloj title="Corre la iterativa con otro orden y un reloj"}
Mismo árbol T y misma $\mathrm{EVAL}$ (I 5, C 4, D 7, C1 6, C2 9). Lo que
cambia es el orden de $A(R)$: **der, centro, izq**. Así la línea 2 deja
${\text{jugada}=\text{der}}$. Dentro de C, primero C1, como siempre.

Dos simplificaciones. El reloj se mide en **nodos generados**, contando
las tres búsquedas seguidas, raíz incluida en cada una. Y se mira solo en
las líneas 4 y 8: se acaba cuando la cuenta llega al tope.

1. Corre PROFUNDIZACIÓN-ITERATIVA con ${d=1}$, 2 y 3. Para cada búsqueda, da
   el orden en que R prueba sus hijos, la jugada lista y los nodos
   generados.
2. ¿Dónde se poda con ${d=2}$? ¿Por qué con el orden de la página no se
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

::: hint {#jue-c3-pista-final-reloj-2 of="jue-c3-ej-final-reloj" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿Cuántos nodos llevas en total
cada vez que un hijo de R devuelve su $w$? Cuando la cuenta llega al tope,
¿la búsqueda en curso ya había terminado?
:::

::: answer {#jue-c3-resp-final-reloj of="jue-c3-ej-final-reloj" title="Respuesta · Las tres búsquedas y los dos relojes"}
**1. Las tres búsquedas.**

| $d$ | Orden de R | Lista | Nodos |
|---|---|---|---:|
| 1 | der, centro, izq | der | 4 |
| 2 | der, centro, izq | centro | 9 |
| 3 | centro, der, izq | centro | 11 |

Con ${d=1}$, R ve 7, 4 y 5: queda der, la trampa. Con ${d=2}$, der va primero
y vale 2; centro vale 6. Con ${d=3}$, centro va primero y vale 5; der e izq
se cortan tras su primera hoja.

**2. La poda con ${d=2}$.** I llega con ${\alpha=6}$, porque centro ya
se valoró. Su primera hoja es 3, y ${3\le6}$: corte alfa, la hoja 6 no
se genera. Con el orden de la página, I iba segunda, con ${\alpha=2}$, y
${3\le2}$ es falso.

**3. El total.** **24** nodos (4, 9 y 11), uno menos que los 25 de la
página. La jugada entregada es la misma, centro.

**4. El reloj.** Con 10 nodos: la primera búsqueda termina en 4. La
segunda llega a 8 tras der, y a 11 tras centro. La línea 8 ve el reloj
agotado y entrega **der**, de ${d=1}$: la trampa. Con 20 nodos: la segunda
búsqueda termina en 13. La tercera llega a 20 tras centro, y la línea 8
entrega **centro**, de ${d=2}$.

El orden cambió lo que cuesta, no la jugada final. Pero con poco tiempo
decide qué se entrega: con este orden, un reloj corto entrega la trampa.
:::

**Punto de control:** deberías poder decir qué entrega
PROFUNDIZACIÓN-ITERATIVA si el reloj se acaba entre dos hijos de la raíz
(línea 8) y si un hijo devuelve 100 (línea 9). También, por qué la jugada
lista va primero, y si un número guardado es un valor, un piso o un techo
según su ventana.

## Ficha: profundización iterativa

Antes de cerrar, la ficha de la profundización iterativa. Es la primera que cambia la sexta fila: siempre tiene una jugada para entregar.

::: table {#jue-ficha-iterativa title="Profundización iterativa en siete rasgos"}
| Rasgo | Profundización iterativa |
|---|---|
| Hasta dónde mira | $d=1$, luego 2, luego 3, mientras haya reloj |
| ¿Genera todo el árbol? | No: repite lo de arriba en cada búsqueda y, con alfa-beta, poda |
| ¿Garantiza $V$? | No, salvo si la última búsqueda llega a los finales. Da su valor con corte |
| Con qué estima | Con $\mathrm{EVAL}$, en los nodos de corte |
| ¿Quién tira dados? | Nadie |
| Qué entrega, y si se puede interrumpir | La jugada de la última búsqueda completa. Sí se puede interrumpir: siempre hay una lista |
| Cuándo conviene | Cuando hay reloj y no se sabe hasta qué $d$ alcanza: ajedrez de torneo (Deep Blue) |
:::

> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | Alfa-beta | $V$ en la raíz; lo garantiza |
> | Minimax con corte | Valor con corte; no garantiza $V$, salvo si llega a los finales |
> | Búsqueda de quietud | Valor con corte en posiciones quietas; no garantiza $V$, salvo si llega a los finales |
> | **Profundización iterativa (estás aquí)** | **Valor con corte de la última búsqueda; no garantiza $V$, salvo si llega a los finales** |
>
> **Lo que viene.**
>
> - **Monte Carlo plano**: estimar cada jugada jugando muchas partidas al azar hasta el final, sin escribir ninguna estimación. Clase 3, [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].
> - **MCTS con UCT**: lo mismo, pero mandando más partidas a las jugadas que van mejor, sin dejar de probar las otras. Clase 3, [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].

## Lo que hay que llevarse

- La profundización iterativa busca con ${d=1,2,3,\dots}$ y entrega lo mejor
  de la **última búsqueda completa**. En la posición de la clase, un reloj
  que se acaba durante ${d=2}$ entrega $\text{d2}\textbf{x}\text{c3}$, que
  pierde; durante ${d=3}$, $\text{d2}\textbf{-}\text{d3}$, que gana.
- Repetir cuesta poco frente a la última búsqueda: del orden de
  ${1/(b-1)}$ de ella si $b$ es fijo. En la posición de la clase, sin poda,
  16 nodos contra 33, porque ahí $b$ no es fijo.
- La versión corta llama entera a DECIDIR-CON-CORTE. La completa usa
  alfa-beta con $\alpha$ compartido (7), prueba primero la jugada anterior
  (6), mira el reloj entre hijos (8) y sale con 100 (9).
- En T: 28 nodos sin poda, 25 con la iterativa (4, 10 y 11), igual que
  alfa-beta con orden fijo. En la posición de la clase: 49, 38 y 23.
- La tabla de transposición guarda número, profundidad y tipo, según la
  ventana con que se llamó: valor si ${\alpha<v<\beta}$, piso si
  ${v\ge\beta}$, techo si ${v\le\alpha}$.

Continúa con [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].
