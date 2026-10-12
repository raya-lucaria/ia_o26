---
id: minimax-con-corte
title: Minimax con corte como algoritmo
nav_title: Minimax con corte
summary: "El cálculo a mano escrito como procedimiento: qué recibe, qué genera, por qué termina, qué se puede afirmar de lo que devuelve, cuánto cuesta y qué preferencia expresa la evaluación."
status: ready
estimated_time: 40m
tags: [juegos, busqueda-adversarial, evaluacion, algoritmos]
---

# Minimax con corte como algoritmo

**¿Cómo se escribe lo que hicimos a mano para cualquier juego, y qué se
puede confiar en lo que devuelve?**

Al terminar tendrás:

- **el pseudocódigo de minimax con corte**, escrito como MINIMAX de la
  clase 2 más una línea;
- una **traza del árbol T cortado**, donde dirás qué línea valora cada
  nodo, la 8 o la 9;
- qué se puede **afirmar** de lo que devuelve, y **cuánto cuesta**;
- qué **preferencia** expresa una función de evaluación.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4. Blancas
> (B) tiene cuatro peones en la fila 1, Negras (N) cuatro en la fila 4, y
> empiezan Blancas. Un peón avanza una casilla si está vacía o captura en
> diagonal hacia delante. Gana quien llega a la fila del rival, captura
> todo o deja al rival sin jugada. ${U=+1}$ si gana Blancas y ${U=-1}$ si gana
> Negras.

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $S_F$ (@jue-c1-finales),
> $\mathrm{Pl}(s)$ (@jue-c1-pl), $A(s)$ (@jue-c1-acciones), $T(s,a)$
> (@jue-c1-transicion) y $U(s)$ (@jue-c1-utilidad). De
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: $\mathrm{EVAL}$
> (@jue-c3-evaluacion), el valor con corte (@jue-c3-valor-con-corte) y el
> orden de los finales (@jue-c3-orden-finales).

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: dos jugadores por turnos,
> sin azar, todo a la vista, toda partida termina, suma cero, y no alcanza
> el tiempo para llegar a los finales.

> [!TIP]
> **Míralo correr: minimax con corte, con d = 1, 2 o 3**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#corte)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 6: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## 1 · Qué recibe y qué genera

**Piensa: ¿qué tuviste que saber para calcular la tabla de profundidades a
mano?**

Las reglas, como en la clase 2, y dos cosas nuevas: cuánto mirar y cómo
juzgar una posición sin terminar.

> **El problema de minimax con corte.**
>
> **Dado (lo que recibe):**
>
> - un estado $s$ donde mueve MAX;
> - ${d\ge1}$, la profundidad: cuántas jugadas puede mirar desde $s$. Es un
>   número, no la columna d del tablero de $\text{d2}$ o $\text{d3}$;
> - las reglas del juego: $S_F$ (@jue-c1-finales), $\mathrm{Pl}$
>   (@jue-c1-pl), $A$ (@jue-c1-acciones), $T$ (@jue-c1-transicion) y $U$
>   (@jue-c1-utilidad);
> - una función de evaluación, $\mathrm{EVAL}$ (@jue-c3-evaluacion).
>
> **Encontrar (lo que devuelve):** una jugada de $A(s)$ cuyo hijo tenga el
> mayor valor con corte (@jue-c3-valor-con-corte), en puntos de MAX.

**Qué genera:** como minimax, no recibe el grafo. Genera los estados con
$A$ y $T$ mientras recorre, pero **solo hasta $d$ jugadas**. Los nodos de
corte sí se generan, porque hay que evaluarlos, pero no se expanden: nadie
calcula sus hijos.

**Estamos aquí:** la posición de la clase, la de
[[cortar-y-evaluar|Cortar y evaluar a mano]]. Mueven Blancas.

::: table {#jue-c3-posicion-corte title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

::: exercise {#jue-c3-ej-genera title="Cuenta qué genera con una sola jugada"}
Con ${d=1}$ en la raíz, en la posición de la tabla:

1. ¿Qué nodos genera minimax con corte? ¿Cuántos son, contando la raíz?
2. ¿Cuál se expande y cuáles se evalúan?
3. Con ${d=2}$ genera 12 nodos. ¿Cuántos de ellos se expanden, y cuántos se
   evalúan?
:::

::: hint {#jue-c3-pista-genera-1 of="jue-c3-ej-genera" title="Cuenta las jugadas"}
¿Cuántas jugadas tiene Blancas en la raíz? Después de una de ellas,
¿cuántas jugadas quedan por mirar?
:::

::: answer {#jue-c3-resp-genera of="jue-c3-ej-genera"}
1. **4 nodos:** la raíz y sus tres hijos, tras
   $\text{a1}\textbf{-}\text{a2}$, $\text{d2}\textbf{-}\text{d3}$ y
   $\text{d2}\textbf{x}\text{c3}$.
2. Solo se expande la raíz. Los tres hijos llegan sin jugadas por mirar y
   no son finales: se evalúan, con 2, 2 y 13.
3. Se expanden **4**: la raíz y sus tres hijos, que ahora llegan con
   ${d=1}$. Los otros **8** son las respuestas de Negras (3, 2 y 3), que
   llegan con ${d=0}$ y se evalúan.
:::

## 2 · El procedimiento

**Piensa: ¿qué línea hay que agregarle a MINIMAX para que se detenga?**

Una sola, la 9. Lo demás es DECIDIR-MINIMAX y MINIMAX de
[[minimax-como-algoritmo|la clase 2]], con $d$ como argumento y ${d-1}$ en
cada hijo:

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
     # ×100: un final pesa más que EVAL
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

El mismo procedimiento en Python, línea por línea; el número entre
paréntesis es la línea del pseudocódigo:

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
    # (8) Un final vale 100 veces su U.
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

Respecto de DECIDIR-MINIMAX y MINIMAX de
[[minimax-como-algoritmo|la clase 2]]:

- **La línea 9 es la nueva:** cuando ya no quedan jugadas por mirar, se
  estima.
- **La línea 8 solo cambia la escala** de $U$, para que un final pese más
  que cualquier estimación. Va antes que la 9.
- **Las demás son las mismas**, con ${d-1}$ en cada llamada (líneas 4, 13
  y 19). Como la 9 es nueva, todo lo que sigue se corre un lugar: las del
  MAX quedan en 10–15 y las del MIN en 16–21, no en 9–14 y 15–20.

Con ${d=1}$, ${d=2}$ y ${d=3}$, los valores $w$ de la línea 4 son las tres
primeras columnas de la tabla de [[cortar-y-evaluar|la página anterior]].

::: exercise {#jue-c3-ej-hoja title="Señala qué línea valora cada estado"}
Para cada estado, di con qué $d$ llega, qué línea devuelve su valor y
cuánto devuelve.

1. Con ${d=2}$ en la raíz: el estado tras $\text{d2}\textbf{x}\text{c3}$ y
   la respuesta $\text{b4}\textbf{x}\text{c3}$.
2. Con ${d=4}$ en la raíz: el estado tras $\text{d2}\textbf{-}\text{d3}$,
   $\text{a4}\textbf{-}\text{a3}$ y $\text{d3}\textbf{-}\text{d4}$.
3. El mismo estado del inciso 2, ahora con ${d=3}$ en la raíz. Si las
   líneas 8 y 9 estuvieran en el orden contrario, ¿cuánto devolvería?
:::

::: hint {#jue-c3-pista-hoja-1 of="jue-c3-ej-hoja" title="Cuenta hacia abajo"}
¿Cuántas jugadas se hicieron desde la raíz hasta ese estado, y cuánto le
quitó cada una a $d$? Después, ¿alguien gana en ese tablero?
:::

::: answer {#jue-c3-resp-hoja of="jue-c3-ej-hoja"}
1. Llega con ${d=0}$ y no es final: lo toma la **línea 9**, que devuelve
   ${\mathrm{EVAL}=0}$.
2. Llega con ${d=1}$. Blancas llegó a la fila 4: es final. Lo toma la
   **línea 8**, que devuelve ${100\cdot(+1)=100}$. La 9 ni se consulta.
3. Llega con ${d=0}$ **y** es final. La línea 8 va primero y devuelve 100.
   Con el orden contrario, la 9 lo evaluaría como un tablero sin terminar:
   tres peones por lado y avance 4 contra 2, así que ${\mathrm{EVAL}=2}$.
   **Una victoria segura se leería como una posición casi pareja.**
:::

## 3 · El corte en el árbol T

**Piensa: si cortas el árbol T a una jugada, ¿con qué valoras I, C y D?**

Con la evaluación, porque ya no queda nada por mirar. Volvemos al árbol T
de [[minimax-como-algoritmo|la clase 2]]: R de MAX; I, C y D de MIN; C1 y
C2 de MAX.

::: figure {#jue-c3-t-arbol title="El árbol T: el problema"}
![Árbol T. Arriba R, donde mueve MAX, con tres flechas: izq hacia I, centro hacia C y der hacia D; en los tres mueve MIN. I tiene dos hojas, 3 y 6. C tiene dos hijos donde mueve MAX: C1 por c1, con hojas 5 y 2, y C2 por c2, con hojas 7 y 8. D tiene dos hojas, 2 y 12. Los nodos internos todavía no tienen valor. Al pie: «Cada hoja es un final: su número es lo que vale ese final.»](../_assets/jue-t-arbol.svg)
:::

**Los números de T son de juguete.** En el 4×4 un final vale ${100\cdot U}$,
o sea ${\pm100}$; aquí las hojas valen entre 2 y 12. T no sirve para ver
quién gana. Sirve para ver **qué línea actúa** en cada nodo.

- Las hojas, de izquierda a derecha: 3 y 6 bajo I; 5 y 2 bajo C1; 7 y 8
  bajo C2; 2 y 12 bajo D. **Hay dos hojas 2**: la de C1 y la de D.
- **Las hojas son finales.** Su número de juguete se toma tal cual, como
  lo que ya devolvió la línea 8.
- Le damos una $\mathrm{EVAL}$ a cada nodo interno. Junto a ella va $V$,
  el valor del juego, calculado en la clase 2:

::: table {#jue-c3-t-eval title="La evaluación de los nodos internos del árbol T"}
| Nodo | $\mathrm{EVAL}$ | $V$ |
|---|---:|---:|
| I | 5 | 3 |
| C | 4 | 5 |
| D | 7 | 2 |
| C1 | 6 | 5 |
| C2 | 9 | 8 |
:::

Con estos números de juguete, T **no cumple** @jue-c3-orden-finales, y a
propósito: la $\mathrm{EVAL}$ de C2, 9, es mayor que la hoja 2 de D, que
es final.

### Con d = 1, der parece la mejor

I, C y D llegan con ${d=0}$ y no son finales: los valora la **línea 9**, con
5, 4 y 7. DECIDIR-CON-CORTE juega der. Es una trampa: D vale 2, porque MIN
responde con la hoja 2 de D, que quedó debajo de la línea de corte.

::: figure {#jue-c3-t-fig-d1 title="Corte con d = 1: der parece valer 7"}
![El árbol T con una línea punteada, la línea de corte, debajo de I, C y D. Arriba de la línea, I, C y D llevan su EVAL: 5, 4 y 7, y R elige der con 7. Debajo de la línea, todo lo que no se genera va en caja o círculo punteado con «?». Al lado: der parece valer 7, su valor real es 2. Se han generado 4 de 14 nodos](../_assets/jue-t-corte-d1.svg)
:::

### Con d = 2, cómo leer la traza

La línea de corte baja un nivel: ahora queda debajo de C1 y C2, y debajo
de las hojas de I y de D.

> **▶ [Recorre esta traza paso a paso](../_assets/traza_arbol_t.html#corte)** — ahí puedes cambiar $d$ entre 1, 2 y 3 y ver cuándo cambia la jugada.

La traza de DECIDIR-CON-CORTE(R, 2) usa el formato de
[[minimax-como-algoritmo|la clase 2]]:

- **Una fila al entrar a un nodo** y una por cada hijo que regresa.
- **Las líneas 8 y 9 corren dentro del hijo**, y el hijo que no se expande
  no tiene fila propia. Su $w$ aparece en la fila del padre: líneas 19–20
  si el padre es de MIN.
- En $w$, una hoja va sola y un nodo lleva su nombre entre paréntesis.
- **En las filas de R, la columna $v$ es mejor_valor.**
- **elige** es mejor_jugada, con «—» mientras vale ninguna.

### Tramo 1 · Centro releva a izq

::: table {#jue-c3-t-traza-d2 title="Traza de DECIDIR-CON-CORTE en el árbol T con d = 2, tramo 1"}
| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›I | +∞ |  | — |
| 3 | 19–⁠20 · R›I | 3 | 3 | — |
| 4 | 19–⁠20 · R›I | 3 | 6 | — |
| 5 | 4–⁠5 · R | 3 | 3 (I) | izq |
| 6 | 17 · R›C | +∞ |  | izq |
| 7 | 19–⁠20 · R›C | 6 | 6 (C1) | izq |
| 8 | 19–⁠20 · R›C | 6 | 9 (C2) | izq |
| 9 | 4–⁠5 · R | 6 | 6 (C) | centro |
:::

- **Filas 3 y 4:** las hojas 3 y 6 son finales. La línea 8 las valora
  dentro del hijo, y su número llega como $w$ a la fila de I.
- **Filas 7 y 8:** C1 y C2 no son finales y llegan con ${d=0}$. La línea 9
  devuelve su $\mathrm{EVAL}$, 6 y 9. Nadie genera sus hojas.
- **Fila 9:** ${6>3}$, así que mejor_jugada pasa de izq a **centro**.

::: figure {#jue-c3-t-fig-d2-tramo-1 title="Tramo 1: C devuelve 6 y R pasa a centro"}
![El árbol T con corte a profundidad 2, al cerrar el tramo 1. I vale 3, con sus hojas 3 y 6. C acaba de devolver 6: C1 y C2 llevan su EVAL, 6 y 9, y sus hojas van en círculo punteado con «?», porque no se generan. D y sus hojas están por mirar. En el recuadro, mejor_jugada = centro y mejor_valor = 6. Se han generado 7 de 14 nodos](../_assets/jue-t-corte-d2-tramo-1.svg)
:::

### Tramo 2 · D no mejora a centro

::: table {#jue-c3-t-traza-d2-tramo-2 title="Traza de DECIDIR-CON-CORTE en el árbol T con d = 2, tramo 2"}
| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 10 | 17 · R›D | +∞ |  | centro |
| 11 | 19–⁠20 · R›D | 2 | 2 | centro |
| 12 | 19–⁠20 · R›D | 2 | 12 | centro |
| 13 | 4–⁠5 · R | 6 | 2 (D) | centro |
| 14 | 6 · R | 6 |  | centro |
:::

- **Filas 11 y 12:** la hoja 2 de D y la hoja 12 son finales, como las de
  I.
- **Fila 13:** ${2>6}$ es falso: mejor_jugada se queda en **centro**, y la
  línea 6 la devuelve.

::: figure {#jue-c3-t-fig-d2-tramo-2 title="Tramo 2: D devuelve 2, que no mejora 6"}
![El árbol T con corte a profundidad 2, al cerrar el tramo 2: la traza está resuelta. I vale 3 y D vale 2, calculados con sus hojas finales; C1 y C2 llevan su EVAL, 6 y 9, y C vale 6. R elige centro con 6. Debajo de la línea de corte, las hojas de C1 y C2 van en círculo punteado con «?»: no se generan. Al lado: centro vale 6, su valor real es 5. Se han generado 10 de 14 nodos](../_assets/jue-t-corte-d2.svg)
:::

### Con d = 3, ya no hay corte

Ningún nodo llega con ${d=0}$ sin ser final: toda hoja la toma la línea 8.
El valor con corte coincide con $V$, y DECIDIR-CON-CORTE juega centro con
5, como en la clase 2.

::: table {#jue-c3-t-por-profundidad title="El árbol T con cada profundidad"}
| $d$ | I · C · D | Juega | Nodos |
|---|---|---|---:|
| 1 | 5 · 4 · 7 | der | 4 |
| 2 | 3 · 6 · 2 | centro | 10 |
| 3 | 3 · 5 · 2 | centro | 14 |
:::

Los nodos generados cuentan la raíz. Con ${d=1}$, der es la trampa. Con
${d=2}$, centro vale 6 y no 5: el 6 es una estimación, pero aquí alcanza
para elegir bien.

::: exercise {#jue-c3-ej-traza-d2 title="Completa la traza con der primero"}
Ahora R prueba sus jugadas en otro orden: **der, izq, centro**. Dentro de
I, C y D el orden no cambia, y la línea 5 sigue con ${>}$ estricto. Llena
los «?» de DECIDIR-CON-CORTE(R, 2).

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›D | +∞ |  | — |
| 3 | 19–⁠20 · R›D | ? | ? | — |
| 4 | 19–⁠20 · R›D | ? | ? | — |
| 5 | 4–⁠5 · R | ? | ? (D) | ? |
| 6 | 17 · R›I | +∞ |  | ? |
| 7 | 19–⁠20 · R›I | ? | ? | ? |
| 8 | 19–⁠20 · R›I | ? | ? | ? |
| 9 | 4–⁠5 · R | ? | ? (I) | ? |
| 10 | 17 · R›C | +∞ |  | ? |
| 11 | 19–⁠20 · R›C | ? | ? (C1) | ? |
| 12 | 19–⁠20 · R›C | ? | ? (C2) | ? |
| 13 | 4–⁠5 · R | ? | ? (C) | ? |
| 14 | 6 · R | ? |  | ? |

1. Llena los «?». ¿En qué filas cambia mejor_jugada, y qué devuelve?
2. En esta traza, ¿qué nodos no los valora ni la línea 8 ni la 9? ¿Qué
   líneas los valoran?
:::

::: hint {#jue-c3-pista-traza-d2-1 of="jue-c3-ej-traza-d2" title="Qué llega a cada fila"}
En cada fila de I, C o D, ¿quién regresa: una hoja o un nodo? ¿Con qué
$d$ llega, y es final? En las filas de R, ¿con qué compara la línea 5?
:::

::: answer {#jue-c3-resp-traza-d2 of="jue-c3-ej-traza-d2"}
En negrita, lo que era «?»; en la columna elige, desde la fila 5 todo
era «?».

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›D | +∞ |  | — |
| 3 | 19–⁠20 · R›D | **2** | **2** | — |
| 4 | 19–⁠20 · R›D | **2** | **12** | — |
| 5 | 4–⁠5 · R | **2** | **2** (D) | der |
| 6 | 17 · R›I | +∞ |  | der |
| 7 | 19–⁠20 · R›I | **3** | **3** | der |
| 8 | 19–⁠20 · R›I | **3** | **6** | der |
| 9 | 4–⁠5 · R | **3** | **3** (I) | izq |
| 10 | 17 · R›C | +∞ |  | izq |
| 11 | 19–⁠20 · R›C | **6** | **6** (C1) | izq |
| 12 | 19–⁠20 · R›C | **6** | **9** (C2) | izq |
| 13 | 4–⁠5 · R | **6** | **6** (C) | centro |
| 14 | 6 · R | **6** |  | centro |

1. mejor_jugada cambia tres veces: a der en la fila 5 (${2>-\infty}$), a
   izq en la 9 (${3>2}$) y a centro en la 13 (${6>3}$). Devuelve
   **centro, con 6**, igual que con el orden de la página.
2. **I, C y D.** Llegan con ${d=1}$ y no son finales, así que pasan de largo
   las líneas 8 y 9 y los valora la rama de MIN, líneas 16–21. R tampoco:
   lo recorre DECIDIR-CON-CORTE, líneas 1–6.
:::

## 4 · Por qué termina y qué se puede afirmar

**Piensa: el algoritmo hace minimax sin errores de cuenta. ¿Por qué
entonces no da el valor del juego?**

Porque lo hace **sobre otro árbol**: el árbol cortado a $d$ jugadas, con
las hojas valoradas por las líneas 8 y 9. Que termine también depende de
ese árbol, y no del juego.

::: remark {#jue-c3-termina title="Minimax con corte termina"}
Si cada estado tiene un número finito de jugadas,
MINIMAX-CON-CORTE$(s,d)$ termina, aunque el juego no termine.

**Por qué:** cada llamada baja $d$ en uno, y la línea 9 ya no llama a
nadie cuando ${d=0}$. La pila nunca pasa de $d$ niveles. A diferencia de
minimax, que termine no depende de que las partidas terminen.
:::

::: remark {#jue-c3-que-afirma title="Qué se puede afirmar de lo que devuelve"}
MINIMAX-CON-CORTE$(s,d)$ devuelve el valor con corte de $s$
(@jue-c3-valor-con-corte), no $V(s)$. Con el mismo argumento de
inducción que minimax, es el minimax del árbol cortado.

En el 4×4, ${|\mathrm{EVAL}|\le36}$ en las posiciones alcanzables que no
son finales. Así, **un 100 solo puede venir de finales ganados**: Blancas
tiene una victoria asegurada dentro de las $d$ jugadas, responda lo que
responda Negras. Lo mismo vale para ${-100}$ y Negras. **Cualquier otro
número es una estimación.**
:::

Si una hoja de corte está mal estimada, el error sube por el árbol, como
la trampa de der con ${d=1}$.

::: exercise {#jue-c3-ej-afirma title="Separa lo seguro de lo estimado"}
Con ${d=3}$ en la raíz de la posición de la clase, MINIMAX-CON-CORTE
devuelve ${-9}$ para $\text{a1}\textbf{-}\text{a2}$, $100$ para
$\text{d2}\textbf{-}\text{d3}$ y $1$ para $\text{d2}\textbf{x}\text{c3}$.

1. ¿Cuál de los tres números es seguro? ¿En cuántas jugadas, a lo más y
   contando la primera, asegura la victoria, y contra cuántas respuestas de
   Negras lo comprobó la búsqueda?
2. Un compañero dice: «con $\text{a1}\textbf{-}\text{a2}$, Blancas pierde
   un peón seguro». ¿Qué se puede afirmar de verdad?
:::

::: hint {#jue-c3-pista-afirma-1 of="jue-c3-ej-afirma" title="Quién pudo dar cada número"}
¿Qué números puede devolver la línea 9 en este juego, y cuáles solo la
línea 8?
:::

::: answer {#jue-c3-resp-afirma of="jue-c3-ej-afirma"}
1. **El 100.** Ninguna evaluación llega a 100, así que viene de finales.
   Blancas gana en a lo más **tres jugadas desde la raíz**, contando
   $\text{d2}\textbf{-}\text{d3}$. La búsqueda lo comprobó contra las
   **dos** respuestas de Negras, $\text{a4}\textbf{-}\text{a3}$ y
   $\text{b4}\textbf{-}\text{b3}$: no hay otras.
2. **Nada seguro.** El ${-9}$ es el minimax de evaluaciones, no de finales.
   Dice que, mirando tres jugadas, la evaluación prefiere poco esa jugada.
:::

## 5 · Cuánto cuesta

**Piensa: si subes $d$ en uno, ¿cuánto más trabajo hay?**

Si cada estado tiene a lo más $b$ jugadas, el árbol cortado tiene a lo más
$b^d$ hojas, y cada hoja cuesta una llamada a $\mathrm{EVAL}$ o a $U$.

::: remark {#jue-c3-costo-corte title="Costo de minimax con corte"}
Con ramificación $b$ y $d$ jugadas por mirar en la raíz,

$$\text{tiempo}=O(b^d).$$

Con alfa-beta y las jugadas bien ordenadas, del orden de $O(b^{d/2})$: en el
mismo tiempo se mira cerca del doble de profundo. El valor en la raíz es el
mismo con o sin poda.
:::

En la posición de la clase, DECIDIR-CON-CORTE genera **4 nodos** con ${d=1}$,
**12** con ${d=2}$ y **33** con ${d=3}$, contando la raíz. Cada nivel multiplica
el trabajo, aunque aquí por menos de ${b=5}$. Ese 5 es el máximo de jugadas
de un nodo que se expande con ${d=3}$: varios estados tienen menos jugadas,
o son finales.

Por eso $d$ se elige según el **tiempo disponible**, no según el juego: es
el tema de [[jugar-contra-el-reloj|Jugar contra el reloj]].

::: exercise {#jue-c3-ej-cota title="Compara la cota con el árbol cortado"}
En el árbol T, ningún nodo tiene más de 3 jugadas: ${b=3}$.

1. Con ${d=2}$, ¿cuántas hojas permite a lo más la cota $b^d$?
2. ¿Cuántas hojas tiene de verdad el árbol cortado, contando nodos de
   corte y finales? ¿Por qué menos?
:::

::: hint {#jue-c3-pista-cota-1 of="jue-c3-ej-cota" title="Dónde termina cada rama"}
Recorre las tres ramas de R. ¿Dónde se detiene cada una con ${d=2}$, y
cuántos hijos tiene cada nodo de MIN?
:::

::: answer {#jue-c3-resp-cota of="jue-c3-ej-cota"}
1. ${3^2=9}$.
2. **6:** las hojas 3 y 6 de I, C1 y C2, y las hojas 2 y 12 de D. Son
   menos porque I, C y D tienen 2 jugadas, no 3. Con la raíz e I, C y D,
   suman los 10 nodos de la tabla.
:::

## 6 · Leer qué preferencia expresa la evaluación

**Piensa: ¿qué dice la suma ${10\cdot\text{material}+\text{avance}}$ sobre
lo que importa?**

$\mathrm{EVAL}$ no viene del reglamento: **la escribimos nosotros**. Es una
decisión de modelado, igual que la medida de comodidad del
[[opt-objetivo-salones-practica|ejemplo de los salones]] en la unidad de
optimización: los pesos dicen cuánto importa cada rasgo. Ésta, leída con
cuidado:

- **Un peón vale lo mismo que diez filas de avance.** La computadora
  revisó las posiciones alcanzables del 4×4 que no son finales. Entre
  posiciones con distinto material, la diferencia de avance nunca
  compensa el peón: **el material decide primero** y el avance desempata.
- **Todos los peones valen igual**, estén donde estén, salvo por su avance.
- **No ve si un peón está bloqueado**, ni si está a punto de ser capturado.
- **No sabe a quién le toca.** La misma posición recibe el mismo número
  mueva quien mueva.

Ninguna de esas omisiones es un error de cuenta. Son **supuestos** del
modelo, y conviene escribirlos como tales.

En ajedrez, la evaluación más conocida es la del **material**: peón 1,
caballo 3, alfil 3, torre 5 y dama 9. Es la misma idea, una suma ponderada
de rasgos, con los mismos huecos.

::: exercise {#jue-c3-ej-rasgo title="Comprueba si un rasgo nuevo arregla el error"}
En la posición de la sección 1, a profundidad 1, la evaluación prefirió
$\text{d2}\textbf{x}\text{c3}$ (13) sobre $\text{a1}\textbf{-}\text{a2}$ y
$\text{d2}\textbf{-}\text{d3}$ (2 cada una), sin ver que Negras recupera
el peón.

1. ¿Cuál de los supuestos de la lista explica ese error?
2. Una compañera propone agregar un rasgo: restar 10 por cada captura que
   Negras tiene disponible y sumar 10 por cada captura que tiene Blancas.
   Calcula la nueva evaluación tras cada una de las tres jugadas. ¿Cambia la
   elección?
3. Otro compañero propone contar solo las capturas de **quien mueve**, que
   tras la jugada de Blancas es Negras: restar 10 por cada una. Calcula otra
   vez. ¿Cambia la elección?
:::

::: hint {#jue-c3-pista-rasgo-1 of="jue-c3-ej-rasgo" title="Cuenta las diagonales"}
Dibuja los tres tableros. En cada uno, cuenta por separado las capturas
de cada color: ¿qué peones tienen un rival en una diagonal de enfrente?
:::

::: answer {#jue-c3-resp-rasgo of="jue-c3-ej-rasgo"}
1. **«No ve si un peón está a punto de ser capturado».**
2. Tras $\text{a1}\textbf{-}\text{a2}$, Negras puede capturar en d2 y
   Blancas en c3: ${2-10+10=2}$. Tras $\text{d2}\textbf{-}\text{d3}$, nadie
   puede capturar: 2. Tras $\text{d2}\textbf{x}\text{c3}$, Negras puede
   capturar en c3, pero el peón de c3 también amenaza a b4: ${13-10+10=13}$.
   **No cambia nada**: las dos amenazas se cancelan, porque el rasgo no
   sabe a quién le toca.
3. Contando solo las de Negras: ${2-10=-8}$, $2$ y ${13-10=3}$. **Sigue
   eligiendo la captura**, por poco: tras la recaptura también cambia el
   avance, y el rasgo no lo ve.

Adivinar las capturas con rasgos es frágil: cada arreglo deja otro hueco.
La [[mas-alla-del-horizonte|página siguiente]] hace otra cosa:
**mirarlas**.
:::

## 7 · Trazar el árbol T por tu cuenta

**Piensa: ¿qué cambia en la decisión si cambia el orden de las jugadas, o
una sola evaluación?**

Antes de empezar, anota tu apuesta: ¿cuál de las dos crees que puede
cambiar la jugada? El ejercicio lo pone a prueba en tres pasos: una traza,
una variante y un costo.

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-corte title="Traza el árbol T con otro orden y otra evaluación"}
Usa el árbol T, sus hojas y las $\mathrm{EVAL}$ de la sección 3. La idea
nueva: **R prueba sus jugadas al revés**, der,
centro, izq. Dentro de I, C y D el orden no cambia, y la línea 5 sigue con
${>}$ estricto.

1. Escribe la traza de DECIDIR-CON-CORTE(R, 2) con ese orden, en el
   formato de la sección 3. ¿Qué jugada devuelve, con qué valor, y en qué
   filas cambia mejor_jugada?
2. Vuelve al orden izq, centro, der y cambia **una** evaluación:
   ${\mathrm{EVAL}(\text{C2})=1}$ en vez de 9. ¿Qué juega con ${d=1}$, ${d=2}$
   y ${d=3}$?
3. ¿Cuántos nodos genera con ${d=1}$, 2 y 3 en la variante del inciso 2? ¿Y
   con el orden del inciso 1? Explica por qué.
:::

::: hint {#jue-c3-pista-final-corte-1 of="jue-c3-ej-final-corte" title="Pista 1 · Qué se mueve de lugar"}
Con R al revés, ¿cambian las filas de dentro de cada hijo, o solo su
lugar en la traza? ¿Qué compara la línea 5 cada vez que un hijo regresa a
R? Para el inciso 2: con cada $d$, ¿qué nodos llegan con ${d=0}$ sin ser
finales?
:::

::: hint {#jue-c3-pista-final-corte-2 of="jue-c3-ej-final-corte" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿Cada nodo que contaste está
arriba de la línea de corte o justo en ella? ¿Cada fila de R compara su
$w$ con el mejor_valor de la fila anterior de R, y no con el último $w$?
:::

::: answer {#jue-c3-resp-final-corte of="jue-c3-ej-final-corte" title="Respuesta · La traza, la variante y el costo"}
**1. La traza con R al revés.**

| # | línea · pila | v | w | elige |
|---:|---|---:|---|---|
| 1 | 2 · R | −∞ |  | — |
| 2 | 17 · R›D | +∞ |  | — |
| 3 | 19–⁠20 · R›D | 2 | 2 | — |
| 4 | 19–⁠20 · R›D | 2 | 12 | — |
| 5 | 4–⁠5 · R | 2 | 2 (D) | der |
| 6 | 17 · R›C | +∞ |  | der |
| 7 | 19–⁠20 · R›C | 6 | 6 (C1) | der |
| 8 | 19–⁠20 · R›C | 6 | 9 (C2) | der |
| 9 | 4–⁠5 · R | 6 | 6 (C) | centro |
| 10 | 17 · R›I | +∞ |  | centro |
| 11 | 19–⁠20 · R›I | 3 | 3 | centro |
| 12 | 19–⁠20 · R›I | 3 | 6 | centro |
| 13 | 4–⁠5 · R | 6 | 3 (I) | centro |
| 14 | 6 · R | 6 |  | centro |

mejor_jugada pasa de ninguna a **der** en la fila 5 (${2>-\infty}$) y a
**centro** en la fila 9 (${6>2}$). En la fila 13, ${3>6}$ es falso. Devuelve
**centro, con 6**, como con el orden de la página.

**2. La variante.** Con ${d=1}$, C2 no se genera: juega der, con 7.
Con ${d=2}$, C2 es nodo de corte y C vale ${\min(6,1)=1}$. R compara izq 3,
centro 1 y der 2, y juega izq, con 3. Con ${d=3}$ no se evalúa ningún
nodo interno: juega centro, con 5. **Una sola evaluación mala cambia la
jugada**, pero solo con la profundidad en que ese nodo es de corte.

**3. El costo.** **4, 10 y 14** nodos en los dos casos. Sin poda, se
genera todo lo que está arriba de la línea de corte, y eso no depende del
orden ni de los números. Con poda, el orden sí importaría.
:::

**Punto de control:** deberías poder

- escribir DECIDIR-CON-CORTE y MINIMAX-CON-CORTE de memoria;
- decir qué recibe y qué genera;
- decir qué línea valora cada nodo: la 8, la 9 o ninguna;
- explicar por qué termina aunque el juego no termine;
- decir qué número de su salida es seguro.

## Lo que hay que llevarse

- DECIDIR-CON-CORTE recibe las reglas, $d$ y $\mathrm{EVAL}$, y devuelve
  una jugada. Genera los estados solo hasta $d$ jugadas y evalúa los nodos
  de corte sin expandirlos.
- Es DECIDIR y MINIMAX con una línea más, la 9. La 8 va antes: un final
  se reconoce aunque llegue con ${d=0}$. Termina siempre, porque $d$ baja en
  cada llamada.
- Elige con el valor con corte, no con $V$: solo los ${\pm100}$ son seguros.
  En el árbol T, ${d=1}$ cae en la trampa de der (7, y vale 2); ${d=2}$ ya
  juega centro, con 6; ${d=3}$ juega centro, con 5. Con ${d=1}$, 2 y 3
  genera **4, 10 y 14** nodos.
- Cuesta $O(b^d)$: en la posición de la clase, **4, 12 y 33** nodos con
  ${d=1}$, 2 y 3.
- $\mathrm{EVAL}$ es un modelo: sus pesos expresan una preferencia y dejan
  cosas fuera.

Las tres palancas de la búsqueda, y lo que se puede justificar de cada
una:

::: table {#jue-c3-que-cambia title="Qué cambia cuando cambia la búsqueda"}
| Cambio | Efecto que se puede justificar |
|---|---|
| Subir $d$ en uno | Hasta $b$ veces más hojas. La decisión puede cambiar en cualquier sentido |
| Una $\mathrm{EVAL}$ con más rasgos | Las mismas hojas, cada una más cara. Ayuda si se acerca a $V$; nada lo asegura |
| Con alfa-beta, un peor orden de jugadas | El mismo valor en la raíz, con menos cortes |
:::

Continúa con [[mas-alla-del-horizonte|más allá del horizonte]].
