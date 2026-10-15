---
id: alfa-beta-como-algoritmo
title: Alfa-beta como algoritmo
nav_title: Alfa-beta como algoritmo
summary: "DECIDIR-ALFA-BETA línea por línea: qué cambia respecto a minimax, qué guarda la pila a media ejecución en el árbol base, cómo el orden decide el ahorro (n1 al revés, 8 de 13), qué asegura cada número que devuelve y por qué las podas son seguras."
status: ready
estimated_time: 55m
tags: [juegos, alfa-beta, poda, algoritmos]
---

# Alfa-beta como algoritmo

**¿Cómo se escribe alfa-beta para cualquier juego de esta clase, de modo
que devuelva la jugada?**

Al terminar tendrás:

- **DECIDIR-ALFA-BETA**, que devuelve la jugada, y **ALFA-BETA**, su
  recursión, explicadas **línea por línea**;
- **qué líneas cambian** respecto a DECIDIR-MINIMAX y MINIMAX;
- **qué hay en memoria** a media ejecución: el paso por C en el árbol base,
  una fila por línea, con la pila;
- **por qué el orden decide el ahorro** (n1 al revés genera 8 de 13) y
  **qué asegura cada número** que devuelve una llamada.

## Lo que traes

- **Las reglas generan el juego.** $S_F$ reconoce finales
  (@jue-c1-finales); $\mathrm{Pl}(s)$ lee quién mueve (@jue-c1-pl); $A(s)$
  enumera jugadas (@jue-c1-acciones); $T(s,a)$ produce el siguiente estado
  (@jue-c1-transicion); $U$ paga los finales, siempre desde MAX
  (@jue-c1-utilidad).
- **El valor se mide desde MAX.** $V(s)$ es el pago para MAX si los dos
  juegan lo mejor, y $Q(s,a)=V(T(s,a))$. MAX elige el mayor $Q$ y MIN, el
  menor (@jue-c2-valor).
- **De [[alfa-beta|Alfa-beta a mano]]:** $\alpha$ y $\beta$
  (@jue-c2-alfa-beta), lo que **MAX** y lo que **MIN** ya tienen asegurado
  en el camino desde la raíz; el par $(\alpha,\beta)$ es la **ventana**. Y
  la regla de alfa-beta (@jue-c2-t-regla).
- **Dos números que no se mezclan.** $v$ es lo mejor que ha visto **este**
  nodo entre sus hijos; $w$ es lo que **devuelve un hijo**, en el momento
  en que regresa.
- **El árbol base.** Raíz R de MAX; sus hijos I, C y D, de MIN; C tiene dos
  hijos de MAX, C1 y C2. Hojas: I (3, 6), C1 (5, 2), C2 (7, 8), D (2, 12).
- **n1:** la posición de hexapawn, con Blancas (MAX) por mover; sus pagos
  son $+1$ y $-1$.
- **Supuestos:** dos jugadores por turnos, sin azar, todo a la vista, toda
  partida termina y suma cero. Ésa es la clase de juegos de esta página.

> **Dado:** un estado no final $s_{\text{raíz}}$ donde mueve MAX y las
> reglas $S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$.
>
> **Encontrar:** una jugada que alcance $V(s_{\text{raíz}})$, la misma que
> entregaría DECIDIR-MINIMAX, generando menos estados cuando se pueda.

> [!TIP]
> **Míralo correr: alfa-beta en el árbol base**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#alfa-beta)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 5: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

---

## 1 · Qué cambia respecto a minimax

**Piensa: ¿qué líneas de DECIDIR-MINIMAX y MINIMAX hay que tocar para
podar?**

Pocas. Como viste en [[alfa-beta|Alfa-beta a mano]], hay **cuatro
nuevas**; por eso las de `return` se recorren. Así se alinean con las de
minimax:

| Alfa-beta | Minimax | Qué cambia |
|---|---|---|
| 1–6 | 1–6 | `mejor_valor` se llama $\alpha$ y la 4 pasa $(\alpha,+\infty)$ |
| 7–13 | 7–13 | Recibe $\alpha$ y $\beta$; la 12 se los pasa al hijo |
| $\textbf{14–15}$ | — | **Nuevas:** corte beta; sube $\alpha$ |
| 16 | 14 | Igual: `return v` |
| 17–21 | 15–19 | Iguales; la 20 pasa $\alpha$ y $\beta$ |
| $\textbf{22–23}$ | — | **Nuevas:** corte alfa; baja $\beta$ |
| 24 | 20 | Igual: `return v` |

Las cuatro nuevas son la regla de @jue-c2-t-regla: **14 y 22 leen** el
número del rival; **15 y 23 actualizan** el propio.

---

## 2 · El algoritmo, de principio a fin

### Alfa-beta

**Alfa-beta es minimax con poda:** deja de generar los hijos que faltan
en cuanto sabe que el nodo no cambia la decisión de arriba.

- **Qué valor rastrea:** el mismo $V$ que minimax. Un nodo que poda, o que
  recibe una cota, devuelve solo una cota: «al menos» o «a lo más».
- **Dónde lo guarda:** en la $v$ de cada llamada abierta, junto con su
  ventana $(\alpha,\beta)$; en la raíz, $\alpha$ hace de `mejor_valor`.
- **Cómo sube:** con el máximo en MAX y el mínimo en MIN, como minimax. Al
  padre solo sube $v$; la ventana que el hijo cambió se pierde.
- **A qué converge:** no necesita converger. Al terminar, la raíz tiene su
  $V$ exacto y una jugada que lo alcanza.

::: figure {#jue-c2-fig-flujo-alfa-beta title="Alfa-beta, en palabras"}
![Flujo de alfa-beta: el de minimax con una pregunta más; si v ≥ beta, poda los hijos restantes](../_assets/jue-c3-rx-flujo-alfa-beta.svg)
:::

#### 1 · Exploración: cómo obtiene su número

**Los pasos.** El recorrido es el de minimax, **en profundidad** y en el
orden de $A(s)$, con la ventana a cuestas:

1. **Bajar con la ventana.** Cada hijo hereda el $(\alpha,\beta)$ que su
   padre tiene en ese momento.
2. **Valorar el final.** Un final vale su $U$, como en minimax.
3. **Subir y comparar.** El padre toma el máximo o el mínimo y compara su
   $v$ con el número del rival. Si lo alcanza, **poda** los hijos que le
   faltan.
4. **Si no poda, actualiza el suyo** y baja por la siguiente jugada.

**La regla**, con $v$ lo mejor que ha devuelto un hijo de este nodo:

| Mueve | Poda si | Nombre | Si no poda |
|---|---|---|---|
| MAX | $\mathbf{v\ge\beta}$ | Corte beta | $\alpha\leftarrow\max(\alpha,v)$ |
| MIN | $\mathbf{v\le\alpha}$ | Corte alfa | $\beta\leftarrow\min(\beta,v)$ |

- **Cuando un nodo de MAX llega a $v\ge\beta$, vale al menos $v$**, sin
  importar lo que haya en los hijos que faltan.
- **Antes de eso, $v$ no es un valor asegurado.** Puede venir de la cota
  superior que devolvió un hijo podado: «a lo más».
- **La raíz es de MAX y no tiene rival arriba:** su $\beta$ es $+\infty$,
  así que **revisa todos sus hijos**. Las podas ocurren dentro de sus
  ramas.

**El código.**

**Piensa: ¿por qué la raíz llama a sus hijos con su $\alpha$, y no con
$-\infty$?**

Porque con su $\alpha$ el hijo sabe qué número tiene que superar, y puede
podar en cuanto ve que no lo logra.

```text
INPUT   un estado s donde mueve MAX, y las
        reglas S_F, Pl, A, T y U de un juego
        finito, por turnos y sin azar.
OUTPUT  una jugada de A(s) que alcanza V(s).

 1 function DECIDIR-ALFA-BETA(s)
     # α hace de mejor_valor
 2   α ← −∞ ; mejor_jugada ← ninguna
 3   for each a in A(s)
       # sin rival arriba de la raíz: β = +∞
 4     w ← ALFA-BETA(T(s, a), α, +∞)
       # estricto: un empate puede ser cota
 5     if w > α: α ← w ; mejor_jugada ← a
 6   return mejor_jugada        # la jugada

 7 function ALFA-BETA(s, α, β)  # devuelve v
 8   if s ∈ S_F: return U(s)
 9   if Pl(s) = MAX
10     v ← −∞
11     for each a in A(s)
12       w ← ALFA-BETA(T(s, a), α, β)
13       v ← max(v, w)
         # compara v con β, el número de MIN
14       if v ≥ β: return v     # corte beta
15       α ← max(α, v)          # sube su α
16     return v                 # valor o cota
17   else                       # Pl(s) = MIN
18     v ← +∞
19     for each a in A(s)
20       w ← ALFA-BETA(T(s, a), α, β)
21       v ← min(v, w)
         # compara v con α, el número de MAX
22       if v ≤ α: return v     # corte alfa
23       β ← min(β, v)          # baja su β
24     return v                 # valor o cota
```

El mismo código en Python; el número entre paréntesis es la línea del
pseudocódigo:

```python
from math import inf

# Las reglas ya existen como funciones:
# es_final(s), pl(s) ("MAX" o "MIN"),
# acciones(s), transicion(s, a) y
# utilidad(s).

def decidir_alfa_beta(s):     # (1)
    # (2) alfa hace de mejor_valor
    alfa = -inf
    mejor_jugada = None
    for a in acciones(s):     # (3)
        # (4) pasa su alfa; beta: inf
        hijo = transicion(s, a)
        w = alfa_beta(hijo, alfa, inf)
        # (5) estricto: una cota que empata
        # con alfa puede valer menos
        if w > alfa:
            alfa = w
            mejor_jugada = a
    return mejor_jugada       # (6)

def alfa_beta(s, alfa, beta): # (7)
    if es_final(s):           # (8)
        return utilidad(s)
    if pl(s) == "MAX":        # (9)
        v = -inf              # (10)
        for a in acciones(s): # (11)
            # (12) hereda la ventana
            hijo = transicion(s, a)
            w = alfa_beta(hijo, alfa, beta)
            v = max(v, w)     # (13)
            # (14) lee el del rival
            if v >= beta:
                return v
            # (15) actualiza el suyo
            alfa = max(alfa, v)
        return v              # (16)
    else:                     # (17)
        v = inf               # (18)
        for a in acciones(s): # (19)
            # (20) hereda la ventana
            hijo = transicion(s, a)
            w = alfa_beta(hijo, alfa, beta)
            v = min(v, w)     # (21)
            # (22) lee el del rival
            if v <= alfa:
                return v
            # (23) actualiza el suyo
            beta = min(beta, v)
        return v              # (24)
```

**Lo que hay que ver en el código:**

- **Línea 4.** La raíz es un nodo de MAX: su $\alpha$ es lo que ya tiene
  con las jugadas revisadas. Pasarlo deja que el hijo pode en cuanto sabe
  que no lo supera. Con $-\infty$ la jugada sería la misma, pero en el
  árbol base D ya no podaría: 13 nodos en vez de 12.
- **Línea 5, estricta.** Un hijo que devuelve $w>\alpha$ cayó dentro de su
  ventana $(\alpha,+\infty)$: **su valor es exacto**. Uno que devuelve
  $w\le\alpha$ puede venir de una poda y solo promete «a lo más $w$».
  En n1, orden fijo, $\text{c1}\textbf{x}\text{b2}$ devuelve $+1$ por una
  poda y vale $-1$; con $\ge$ la raíz la elegiría y perdería. En el árbol
  base lo muestra @jue-c2-t-ej-empate-raiz.
- **La raíz no poda.** DECIDIR no tiene línea 14: revisa todas sus
  jugadas. Podan los nodos de abajo, con el $\alpha$ que ella les pasa.
- **Una poda ahorra de verdad.** Los hijos que faltan nunca llegan a la
  línea 12 o 20: su $T(s,a)$ no se calcula.
- **Raíz de MIN**, si mueven Negras: se invierte. $\beta\leftarrow+\infty$,
  la línea 4 llama con $(-\infty,\beta)$ y la 5 guarda si $w<\beta$.

> **Si lees Russell y Norvig, 4.ª ed.** Su ALPHA-BETA-SEARCH también
> devuelve la jugada, como DECIDIR. Pero la jugada viaja por la recursión:
> MAX-VALUE y MIN-VALUE devuelven el par $(v,\text{jugada})$, y la raíz es
> una llamada más a MAX-VALUE con $(-\infty,+\infty)$.
>
> Además actualizan $\alpha$ **antes** del `if` de la poda. Es
> equivalente. Cuando $v\ge\beta$ el nodo regresa de inmediato, así que da
> igual si $\alpha$ ya subió; la jugada que sale de la raíz es la misma.

---

**El recorrido: lo que hay en memoria.**

> **▶ [Ve la pila en el corte beta de C2](../_assets/traza_arbol_t.html#alfa-beta-fila-12)** — abre la traza del árbol base justo en ese paso.
>
> **▶ [Ve C y C1 a la vez en la pila](../_assets/traza_arbol_t.html#alfa-beta-fila-8)** — el paso en que C1 sube su α en la línea 15.

**Piensa: en la línea 15 de C1, ¿qué ve la pila que C no ve?**

Ve dos $\alpha$: el de C1, que acaba de subir, y el de C, que no se
enteró. La traza de [[alfa-beta|Alfa-beta a mano]] tiene una fila por
hijo. Aquí el paso por C, sus filas 6 a 15, se abre en **una fila por
línea**, con la pila. Las ramas I y D no se repiten: están en aquella
traza.

- **línea:** qué líneas corren. Al entrar a un nodo corren 7, 8 («¿es
  final?», no) y 9 («¿mueve MAX?»); en uno de MIN, también la 17.
- **pila:** las llamadas abiertas; la última es la que ejecuta.
- **queda:** lo que cambió en la memoria de ese nodo.

Cada llamada abierta ocupa un **marco** de la pila (*stack frame*): los
datos de esa llamada mientras espera a sus hijos.

**Tramo a · C1: su α nace heredado y sube**

| línea | pila | ejecuta | queda |
|---|---|---|---|
| 3–4 | R | centro: llama C(3,+∞) |  |
| 7–9, 17–18 | R›C | MIN; llega con $(3,+\infty)$ | $v$ = $+\infty$ |
| 19–20 | R›C | c1: llama C1(3,+∞) |  |
| 7–10 | R›C›C1 | MAX; llega con $(3,+\infty)$ | $v$ = $-\infty$ |
| 11–12 | R›C›C1 | hoja 5 | $w$ = 5 |
| 13 | R›C›C1 | $v$ ← max(−∞, $5)$ | $v$ = 5 |
| 14 | R›C›C1 | $5\ge +\infty$ no |  |
| 15 | R›C›C1 | α ← max(3, $5)$ | α = 5 |

- **La línea 4 pasa el $\alpha=3$ de la raíz.** Por eso C, y luego C1,
  llegan con $(3,+\infty)$.
- **En la línea 15, la pila guarda dos $\alpha$:** el de C1, que sube a 5,
  y el de C, que sigue en 3. C1 es de MAX: el $\alpha$ es **suyo**, aunque
  empezó heredado.

**Tramo b · C1 revisa su segunda hoja y regresa**

| línea | pila | ejecuta | queda |
|---|---|---|---|
| 11–12 | R›C›C1 | hoja 2 | $w$ = 2 |
| 13 | R›C›C1 | $v$ ← max(5, $2)$ | $v$ = 5 |
| 14 | R›C›C1 | $5\ge +\infty$ no |  |
| 15 | R›C›C1 | α ← max(5, $5)$ | α = 5 |
| 16 | R›C›C1 | devuelve 5 |  |

**Tramo c · C actualiza su β**

| línea | pila | ejecuta | queda |
|---|---|---|---|
| 20 | R›C | C1 regresa | $w$ = 5 |
| 21 | R›C | $v$ ← min(+∞, $5)$ | $v$ = 5 |
| 22 | R›C | $5\le 3$ no |  |
| 23 | R›C | β ← min(+∞, $5)$ | β = 5 |

::: figure {#jue-c2-t-c1-regresa title="C1 regresó: en C, α = 3 y β = 5"}
![Árbol base. C, de MIN, en la pila con la ventana (3, 5). C1 ya devolvió v = 5 tras revisar sus hojas 5 y 2. C2 y D siguen punteados. Abajo, la recta con la ventana (3, 5) sombreada](../_assets/jue-t-ab-2.svg)
:::

- **Al regresar C1, a C solo le llega $w=5$.** El $\alpha=5$ de C1 se
  perdió con su marco. C es de MIN: compara 5 con **su** $\alpha=3$ (línea
  22, «5≤3 no») y baja **su** $\beta$ a 5 (línea 23).

**Tramo d · C2 poda**

| línea | pila | ejecuta | queda |
|---|---|---|---|
| 19–20 | R›C | c2: llama C2(3,5) |  |
| 7–10 | R›C›C2 | MAX; llega con $(3,5)$ | $v$ = $-\infty$ |
| 11–12 | R›C›C2 | hoja 7 | $w$ = 7 |
| 13 | R›C›C2 | $v$ ← max(−∞, $7)$ | $v$ = 7 |
| 14 | R›C›C2 | $7\ge 5$ sí: devuelve 7 | hoja 8: no |

- **Corte beta en C2.** C2 llega con $(3,5)$ y su primera hoja da
  $v=7\ge\beta=5$: la línea 14 regresa y **la hoja 8 no se genera**.

::: figure {#jue-c2-t-ab-pila title="ALFA-BETA a media ejecución en el árbol base"}
![El árbol base en el instante del corte beta en C2 (línea 14). Resaltado, el camino R, C, C2; I y C1 aparecen tenues, con «devolvió 3» y «devolvió 5»: ya regresaron y sus marcos no existen. La hoja 7 acaba de devolver w = 7; la hoja 8 es un círculo punteado con «?»: no se generará. D y sus hojas siguen por mirar. Abajo, la pila de llamadas, tres marcos: R, con α = 3 y mejor_jugada = izq, va en centro; C, con α = 3, β = 5 y v = 5, va en c2; C2, con α = 3, β = 5 y v = 7: v ≥ β, poda. El α = 5 que C1 alcanzó se perdió al regresar; a C solo le llegó w = 5](../_assets/jue-t-ab-pila.svg)
:::

**Qué guarda cada marco** en el instante del corte beta:

- **el estado** $s$ y la jugada por la que va su `for`;
- **su ventana** $(\alpha,\beta)$, que pudo encogerse desde que llegó;
- **su $v$**, lo mejor visto entre sus hijos.

**La memoria sigue siendo $O(bm)$**, como en minimax: hasta $m$ marcos
abiertos, cada uno con a lo más $b$ jugadas pendientes. Nunca se guarda el
árbol entero.

**Tramo e · C devuelve 5 y la raíz cambia de jugada**

| línea | pila | ejecuta | queda |
|---|---|---|---|
| 20 | R›C | C2 regresa | $w$ = 7 |
| 21 | R›C | $v$ ← min(5, $7)$ | $v$ = 5 |
| 22 | R›C | $5\le 3$ no |  |
| 23 | R›C | β ← min(5, $5)$ | β = 5 |
| 24 | R›C | devuelve 5 |  |
| 4 | R | C regresa | $w$ = 5 |
| 5 | R | $5>3$ sí | α = 5; centro |

- **C2 devolvió 7, una cota**: «al menos 7»; su valor exacto es 8. A C le
  basta: $\min(5,7)=5$.
- **En la línea 5, $5>3$:** la raíz guarda centro con $\alpha=5$. Lo que
  sigue, D y su corte alfa, está en la traza por hijo.

---

**El orden decide el ahorro.**

**Piensa: si la mejor jugada llega al final, ¿con qué $\alpha$ trabajan
los primeros hijos?**

Con uno bajo, que poda poco. En [[alfa-beta|Alfa-beta a mano]], n1 con el
orden fijo generó 5 de sus 13 estados. Ahora, **el orden invertido**: la
última jugada de cada lista se revisa primero; los nodos conservan sus
números y los dibujos van reflejados.

::: figure {#jue-c2-ab-inv-1 title="Orden invertido, parte 1: n3 baja β a −1"}
![n1, con su tablero, arriba. Su primer hijo ahora es n3, tras c1xb2: mueve Negras (MIN). El primer hijo de n3, n13, tras c3xb2, va resaltado: final, vale −1. En n3, β pasa de +∞ a −1](../_assets/jue-ab-invertido-parte-1.svg)
:::

::: figure {#jue-c2-ab-inv-2 title="Orden invertido, parte 2: el corte beta en n6"}
![n6, de MAX, con la ventana (−∞, −1). Su primer hijo, n12, tras b2xa3, va resaltado: final, vale +1. n6 muestra v = +1 y «+1 ≥ −1: corte beta». Sus otros dos hijos, n11 tras b2-b3 y n7 tras b1xc2, son cajas punteadas con «?»: no se generan](../_assets/jue-ab-invertido-parte-2.svg)
:::

::: figure {#jue-c2-ab-inv-3 title="Orden invertido, parte 3: Negras termina, y la raíz también"}
![De vuelta en n3, falta n4, de MAX, con (−∞, −1); su único hijo, n5, vale +1, y bajo n5 va la nota «en n4, +1 ≥ −1: poda, pero no ahorra». n3 devuelve v = −1. En la raíz, α pasa a −1. Su último hijo, n2, llega con (−1, +∞) y vale +1. La raíz devuelve +1](../_assets/jue-ab-invertido-parte-3.svg)
:::

- **n3 empieza por n13, que vale $-1$.** Como es de MIN, compara su
  $v=-1$ con $\alpha=-\infty$, el número de MAX que heredó. Como
  $-1\le-\infty$ es falso, no poda y baja $\beta$ a $-1$ (línea 23).
- **n6 es de MAX: compara su $v=+1$ con $\beta=-1$, el número de MIN que
  heredó; $+1\ge-1$ → corte beta, línea 14.** Su $v$ viene de n12, su
  primer hijo, y su ventana, de n3. No se generan n11, n7 ni lo que cuelga
  de n7; n6 devuelve $+1$: «al menos $+1$».
- **n4 también cumple $+1\ge-1$** en la línea 14, pero no le quedan hijos:
  **una poda solo ahorra si quedan hermanos por generar**.
- **n3 revisó todos sus hijos:** devuelve $-1$, **su valor exacto**.
- **En la raíz, primero** $-1>-\infty$: $\alpha$ sube a $-1$ y
  `mejor_jugada` ← $\text{c1}\textbf{x}\text{b2}$, la única que conoce.
  **Después** n2 llega con $(-1,+\infty)$ y vale $+1$; $+1>-1$, así que
  $\alpha$ sube a $+1$ y la jugada pasa a $\text{c1}\textbf{-}\text{c2}$.

::: figure {#jue-c2-ab-invertido title="Alfa-beta con el orden invertido"}
![El subgrafo de n1, reflejado, recorrido por alfa-beta con el orden invertido. Primero n1; segundo n3 (α −∞, β +∞, MIN, devuelve −1); tercero n13, final −1; cuarto n6 (α −∞, β −1, MAX, devuelve ≥ +1, una cota); quinto n12, final +1; sexto n4 (α −∞, β −1, MAX, devuelve +1); séptimo n5, final +1; octavo n2, final +1. Una barra de acento debajo de n6 marca el corte beta sobre las jugadas b2-b3 y b1xc2. Cajas punteadas con signo de interrogación marcan n11 y n7, con lo que cuelga de n7: no se generan](../_assets/jue-alfa-beta-invertido.svg)
:::

**Los dos órdenes dan $+1$ con $\text{c1}\textbf{-}\text{c2}$**, como
minimax: **5** estados con el orden fijo, **8** con el invertido. Con el
invertido, mientras se revisa n3 la raíz solo tiene $\alpha=-\infty$: n3
no puede podar contra nada.

::: table {#jue-c2-ahorro title="Nodos generados por cada recorrido"}
| Recorrido | Árbol base | n1 | Hexapawn |
|---|---:|---:|---:|
| Minimax | 14 | 13 | 252 |
| Alfa-beta, orden dado | 12 | 5 | 82 |
| Alfa-beta, orden invertido | 14 | 8 | 72 |
:::

- **Cuanto antes aparece una buena jugada, más se poda.** En el árbol base
  y en n1 gana el orden dado; en el juego completo, el invertido. Ningún
  orden es el mejor siempre.
- **Nadie conoce de antemano la mejor jugada:** los programas reales
  **adivinan un buen orden**, por ejemplo, capturas primero.

**En el árbol de resultados.** El mismo código, en el árbol de resultados
de [[minimax-como-algoritmo|Minimax como algoritmo]], genera 12 de sus 15
nodos y juega centro, como minimax.

::: figure {#jue-c2-fig-resultados-alfa-beta title="Alfa-beta en el árbol de resultados: 12 de 15 nodos, la misma jugada"}
![Alfa-beta con el orden dado genera 12 de 15 nodos: poda c2b porque C2 ya vale al menos +1 ≥ beta = 0, y d2 y d3 porque D vale a lo más −1 ≤ alfa = 0. Juega centro](../_assets/jue-c3-rx-alfa-beta.svg)
:::

#### 2 · Elección: qué jugada juega

**Cuando la raíz revisó todas sus jugadas**, juega la que guardó en
`mejor_jugada`: la primera, en el orden de $A(s)$, que alcanza el mayor
$Q$.

::: table {#jue-c2-tab-eleccion-alfa-beta title="Podar y jugar con alfa-beta"}
| Decisión | Compara | Regla |
|---|---|---|
| Podar en MAX | $v$ con $\beta$ | $\mathbf{v\ge\beta}$ |
| Podar en MIN | $v$ con $\alpha$ | $\mathbf{v\le\alpha}$ |
| Jugar, en la raíz | $w$ con $\alpha$ | $\mathbf{w>\alpha}$ |
:::

- **El igual poda abajo, pero no gana arriba.** Un $w$ que empata con
  $\alpha$ puede ser solo una cota superior; esa jugada podría valer menos
  y no debe desplazar a la elegida.
- **La jugada guardada trae su $Q$ exacto.** Las descartadas pueden traer
  su valor o solo una cota, suficiente para saber que no la superan.

#### 3 · Propiedades

- **Número que da:** el $V$ exacto de la raíz y el $Q$ exacto de la jugada
  elegida; de las descartadas, a veces solo una cota.
- **Usa EVAL:** no. Solo lee la $U$ de los finales, como minimax.
- **Garantía:** el mismo $V$ que minimax y, con el mismo orden y
  desempate, la misma jugada. Cada número que devuelve una llamada se lee
  contra su ventana de entrada (@jue-c2-invariante).
- **Se puede interrumpir:** no; un algoritmo que sí, se llama *anytime*.
  Tras cerrar el primer hijo de la raíz tiene una jugada legal con su $Q$
  exacto; las que no la mejoran solo traen cotas. Nada garantiza que sea la
  óptima; antes del primer hijo, ni eso.
- **Complejidad:** depende del orden; tiempo entre $O(b^{m/2})$ y
  $O(b^m)$, memoria $O(bm)$ (@jue-c2-costo-alfa-beta).
- **Frente a los demás:** da el resultado de minimax con trabajo menor o
  igual. **Con el mismo orden, nunca genera más nodos**; con buen orden,
  muchos menos. Conviene siempre que minimax sirva: gato, hexapawn. En
  ajedrez y damas es la base de los programas, que además dejan de mirar a
  cierta profundidad.
- **Supuestos:** los de minimax. La poda usa que lo bueno para MIN es lo
  malo para MAX: con más jugadores deja de valer (casos borde).

**Qué asegura cada número que devuelve una llamada.**

::: remark {#jue-c2-invariante title="Qué devuelve ALFA-BETA: el invariante"}
Una llamada ALFA-BETA($s$, $\alpha_0$, $\beta_0$) llega con su **ventana
de entrada** $(\alpha_0,\beta_0)$, $\alpha_0<\beta_0$. Lo que devuelve, y
su padre recibe como $w$, cumple siempre:

| Si $w$ cae… | Entonces $V(s)$ es… |
|---|---|
| $w\le\alpha_0$ | a lo más $w$ |
| $\alpha_0<w<\beta_0$ | exactamente $w$ |
| $w\ge\beta_0$ | al menos $w$ |

Se compara con la ventana con la que **llegó**, no con la que tiene al
regresar. Dentro del nodo, su $\alpha$ o su $\beta$ ya se movieron.
:::

- **La lectura es lo que se garantiza; el número puede ser exacto.** En el
  árbol base, D devuelve $2\le\alpha=5$: el invariante solo promete «a lo
  más 2», y vale exactamente 2, pero el algoritmo no lo sabe. En el orden
  invertido, I devuelve $3\le5$ habiendo visto a todos sus hijos: también
  es exacto. C2, en cambio, devuelve 7 y vale 8.
- **En la raíz,** con $(-\infty,+\infty)$, cualquier $w$ cae dentro: **el
  valor de la raíz es exacto**.
- **No podar en un nodo no garantiza que su número sea exacto:** una poda
  más abajo pudo dejarle solo una cota. Los dos casos de la tabla visitan
  todos sus hijos y aun así devuelven una cota.

| Llamada | Debajo | Devuelve | $V$ |
|---|---|---:|---:|
| MAX con $(10,+\infty)$ | un MIN con hojas 5 y 1 | 5 | 1 |
| MIN con $(-\infty,4)$ | un MAX con hojas 5 y 9 | 5 | 9 |

- **En la primera fila, el MIN de abajo poda:** $5\le10$. MAX recibe 5 y
  lo devuelve; frente a $\alpha_0=10$ solo asegura «a lo más 5».
- **En la segunda, el MAX de abajo poda:** $5\ge4$. MIN recibe 5 y lo
  devuelve; frente a $\beta_0=4$ solo asegura «al menos 5».

**El tipo de cota lo decide la ventana de entrada, no que el nodo sea de
MAX o de MIN.**

- ***Fail-soft* y *fail-hard*.** Esta versión es *fail-soft*: al podar
  devuelve su $v$ tal cual, aunque salga de la ventana. La *fail-hard*
  devolvería $\alpha$ o $\beta$ en su lugar. La raíz da lo mismo.

::: remark {#jue-c2-costo-alfa-beta title="Costo de alfa-beta"}
Con $b\ge2$ jugadas por estado y profundidad $m$:

- **Peor caso:** sin podas, $O(b^m)$, como minimax.
- **Mejor caso:** con un árbol aproximadamente uniforme y **orden
  perfecto**, la mejor jugada primero en cada nodo,
  $O(b^{m/2})=O\bigl((\sqrt b)^m\bigr)$: con el mismo tiempo, **el doble
  de profundidad**.
- **Memoria:** $O(bm)$, solo el camino actual.
:::

#### 4 · Casos borde

- **Empate en la raíz:** el $>$ estricto de la línea 5 conserva la primera
  jugada empatada, como minimax (@jue-c2-t-ej-empate-raiz).
- **El igual poda:** $v\ge\beta$ y $v\le\alpha$. Sin el igual, el valor no
  cambia, pero se poda mucho menos (@jue-c2-ej-igualdad).
- **Una sola jugada:** queda forzada y $V(s)=Q(s,a)$; DECIDIR igual la
  valora con su llamada.
- **Una poda sin hermanos pendientes** no ahorra nada, como la de n4.
- **Un final entre los primeros hijos** puede provocar la poda de
  inmediato, si su $U$ alcanza la ventana: n2 en la ventana más chica.
- **La raíz ya es final:** como en minimax, DECIDIR no tiene jugada que
  devolver; hay que revisar $S_F$ antes de llamarlo.
- **El orden:** con mal orden genera los mismos nodos que minimax. Cambiar
  el orden no cambia $V$, pero puede cambiar cuál de las jugadas empatadas
  se entrega.
- **Finales a distintas profundidades:** no prefiere ganar pronto ni perder
  tarde, salvo que $U$ lo codifique.
- **Con tabla de transposición** hay que guardar si el número es un valor
  exacto, una cota «al menos» o una «a lo más». Guardar una cota como
  exacta es un error clásico.
- **Sin suma cero, o con más de dos jugadores,** la poda ordinaria deja de
  valer. Con $\max^n$ solo queda una **poda superficial**, con cotas por
  jugador y sobre la suma (Korf, 1991), sin el ahorro de alfa-beta.
- **El paranoico (*Paranoid*)** junta a los demás en una coalición MIN y recupera
  alfa-beta, pero resuelve un juego más pesimista.
- **Con nodos de azar** solo se puede podar si se conocen cotas de $U$:
  es la idea de \*-minimax (Ballard, 1983).

---

#### Intuición

**Por qué las podas son seguras.**

- **Corte alfa,** en un nodo de MIN con $v\le\alpha$: MIN ya puede dejar a
  MAX en $v$ o menos aquí. Más arriba, MAX tiene otra alternativa que le
  da $\alpha\ge v$. Los hijos que faltan solo podrían **bajar** este nodo:
  MAX seguiría prefiriendo su alternativa.
- **Corte beta,** en un nodo de MAX con $v\ge\beta$: lo mismo con los
  papeles cambiados. MIN nunca deja que la partida llegue aquí.
- **Termina** por la misma razón que minimax: recorre el mismo árbol
  finito y solo puede salir antes de un `for`.

**La misma idea que ramificar y acotar.** Alfa-beta es
[[ramificar-y-acotar|ramificar y acotar]] con dos jugadores:

- **`mejor`, el valor de un plan que ya tenemos** → $\alpha$ para MAX y
  $\beta$ para MIN.
- **La cota de un subproblema** → lo que devuelve un nodo, leído contra su
  ventana de entrada (@jue-c2-invariante). Su $v$ a medio camino no es
  cota de nada todavía.
- **Cerrar si la cota no supera `mejor`** → podar si $v\le\alpha$ o si
  $v\ge\beta$.
- **Un nodo cerrado no tiene su óptimo calculado** → un nodo que podó solo
  tiene una cota.

**Una ventana más chica.** En hexapawn, $U$ solo vale $+1$ o $-1$, así que
nada sale de $[-1,+1]$. Si solo se quiere **el valor** de n1, no la
jugada, se puede llamar directamente a la recursión, ALFA-BETA(n1, $-1$,
$+1$). Ahí n1 es un nodo de MAX como cualquier otro, con su línea 14:

- **Orden dado: 2 estados.** n2 vale $+1\ge\beta=+1$: corte beta en n1.
  Nada es mejor que ganar.
- **Orden invertido: 4 estados.** n3 poda en su primer hijo, porque
  $-1\le\alpha=-1$, y devuelve $-1$; después n2 da $+1$.
- **Todo el juego:** 82 → **49** en orden dado y 72 → **53** en invertido.

Lo devuelto puede ser una cota, pero aquí es segura: «al menos $+1$» y «a
lo más $-1$» ya son exactas.

**DECIDIR-ALFA-BETA no tiene línea 14.** Para aprovechar lo mismo y
entregar la jugada, su `for` tendría que terminar en cuanto un $w$ vale
$+1$. Así lo hace la línea 9 de PROFUNDIZACIÓN-ITERATIVA, en
[[jugar-contra-el-reloj|Hasta dónde mirar]]. La misma idea, conocer las
cotas de $U$, es la que permite podar en árboles con azar.

---

#### Ejercicios

::: exercise {#jue-c2-t-ej-invertido title="Llena la traza con el orden invertido"}
Recorre el árbol base con **cada lista de hijos al revés**. La raíz revisa
der, centro, izq; D ve 12 y luego 2; C ve C2 y luego C1. C2 ve 8 y luego
7; C1, 2 y luego 5; I, 6 y luego 3. La tabla es la de la traza por hijo de
[[alfa-beta|Alfa-beta a mano]]. Llena los «?».

| # | línea · pila | $(\alpha ,\beta )$ | $v$ | $w$ | poda | jugada |
|---|---|---|---|---|---|---|
| 1 | 2 · R | $(-\infty,+\infty)$ | $-\infty$ |  |  | — |
| 2 | 18 · R›D | $(-\infty,+\infty)$ | $+\infty$ |  |  | — |
| 3 | 20–23 · R›D | $(-\infty,12)$ | 12 | 12 | $12\le -\infty$ no | — |
| 4 | 20–23 · R›D | $(-\infty,2)$ | 2 | 2 | $2\le -\infty$ no | — |
| 5 | 4–5 · R | ? | ? | ? | ? | ? |
| 6 | 18 · R›C | ? | $+\infty$ |  |  | ? |
| 7 | 10 · R›C›C2 | ? | $-\infty$ |  |  | ? |
| 8 | ? · R›C›C2 | ? | ? | 8 | ? | ? |
| 9 | ? · R›C›C2 | ? | ? | 7 | ? | ? |
| 10 | ? · R›C | ? | ? | ? | ? | ? |
| 11 | 10 · R›C›C1 | ? | $-\infty$ |  |  | ? |
| 12 | ? · R›C›C1 | ? | ? | 2 | ? | ? |
| 13 | ? · R›C›C1 | ? | ? | 5 | ? | ? |
| 14 | ? · R›C | ? | ? | ? | ? | ? |
| 15 | 4–5 · R | ? | ? | ? | ? | ? |
| 16 | 18 · R›I | ? | $+\infty$ |  |  | ? |
| 17 | ? · R›I | ? | ? | 6 | ? | ? |
| 18 | ? · R›I | ? | ? | 3 | ? | ? |
| 19 | 4–5 · R | ? | ? | ? | ? | ? |
| 20 | 6 · R | ? | ? |  |  | ? |

1. ¿Cuántos de los 14 nodos se generan?
2. ¿En qué fila se cumple una condición de poda, y qué ahorra?
3. ¿Qué jugada devuelve? ¿Por qué se poda menos que en el orden dado?
:::

::: hint {#jue-c2-t-pista-invertido of="jue-c2-t-ej-invertido" title="Lo que sube y lo que no"}
Después de la fila 5, $\alpha$ de R vale 2. En la fila 10, C solo recibe
el $w$ de C2: el $\alpha$ que C2 subió no viaja. En las filas 17 y 18,
decide si la línea 22 regresa o la 23 baja $\beta$.
:::

::: answer {#jue-c2-t-resp-invertido of="jue-c2-t-ej-invertido"}
| # | línea · pila | $(\alpha ,\beta )$ | $v$ | $w$ | poda | jugada |
|---|---|---|---|---|---|---|
| 1 | 2 · R | $(-\infty,+\infty)$ | $-\infty$ |  |  | — |
| 2 | 18 · R›D | $(-\infty,+\infty)$ | $+\infty$ |  |  | — |
| 3 | 20–23 · R›D | $(-\infty,12)$ | 12 | 12 | $12\le -\infty$ no | — |
| 4 | 20–23 · R›D | $(-\infty,2)$ | 2 | 2 | $2\le -\infty$ no | — |
| 5 | 4–5 · R | $(2,+\infty)$ | 2 | 2 (D) | $2>-\infty$ sí | der |
| 6 | 18 · R›C | $(2,+\infty)$ | $+\infty$ |  |  | der |
| 7 | 10 · R›C›C2 | $(2,+\infty)$ | $-\infty$ |  |  | der |
| 8 | 12–15 · R›C›C2 | $(8,+\infty)$ | 8 | 8 | $8\ge +\infty$ no | der |
| 9 | 12–15 · R›C›C2 | $(8,+\infty)$ | 8 | 7 | $8\ge +\infty$ no | der |
| 10 | 20–23 · R›C | $(2,8)$ | 8 | 8 (C2) | $8\le 2$ no | der |
| 11 | 10 · R›C›C1 | $(2,8)$ | $-\infty$ |  |  | der |
| 12 | 12–15 · R›C›C1 | $(2,8)$ | 2 | 2 | $2\ge 8$ no | der |
| 13 | 12–15 · R›C›C1 | $(5,8)$ | 5 | 5 | $5\ge 8$ no | der |
| 14 | 20–23 · R›C | $(2,5)$ | 5 | 5 (C1) | $5\le 2$ no | der |
| 15 | 4–5 · R | $(5,+\infty)$ | 5 | 5 (C) | $5>2$ sí | centro |
| 16 | 18 · R›I | $(5,+\infty)$ | $+\infty$ |  |  | centro |
| 17 | 20–23 · R›I | $(5,6)$ | 6 | 6 | $6\le 5$ no | centro |
| 18 | 20–22 · R›I | $(5,6)$ | 3 | 3 | $3\le 5$ sí | centro |
| 19 | 4–5 · R | $(5,+\infty)$ | 5 | 3 (I) | $3>5$ no | centro |
| 20 | 6 · R | $(5,+\infty)$ | 5 |  |  | centro |

1. **Los 14.** Ninguna poda deja hermanos sin generar.
2. **Fila 18:** en I, $v=3\le\alpha=5$ y la línea 22 regresa, pero I ya
   no tenía hijos pendientes: **no ahorra nada**. En la fila 12, C1 ve 2
   con $\beta=8$: $2\ge8$ es falso.
3. **Centro**, la misma que en el orden dado: en la fila 19, $3>5$ es
   falso. Se poda menos porque **la mejor jugada llega en medio**.
   Mientras se revisa C, la raíz solo tiene $\alpha=2$; dentro de C, los
   valores altos (8) llegan antes que los bajos.
:::

::: exercise {#jue-c2-ej-se-corta title="Decide si se poda"}
1. Un nodo de MIN recibe $\alpha=4$ y $\beta=9$. Su primer hijo devuelve 6,
   el segundo 3, y tiene un tercer hijo. ¿Hay poda después del primero?
   ¿Cuánto vale $\beta$ entonces? ¿Hay poda después del segundo?
2. En el recorrido invertido de n1, n4 tenía $\beta=-1$ y su único hijo
   valía $+1$. La condición $v\ge\beta$ se cumplía. ¿Ahorró algo?
:::

::: hint {#jue-c2-pista-se-corta of="jue-c2-ej-se-corta" title="La línea 22, y después la 23"}
Para el inciso 1, sigue las líneas 21, 22 y 23 una vez por hijo. Para el
inciso 2, pregúntate qué deja sin generar una poda.
:::

::: answer {#jue-c2-resp-se-corta of="jue-c2-ej-se-corta"}
1. Tras el primero, $v=6$ y $6\le4$ es falso: no hay poda, y $\beta$ baja a
   $\min\{9,6\}=6$. Tras el segundo, $v=\min\{6,3\}=3\le\alpha=4$: **corte
   alfa**, y el tercer hijo no se genera. El nodo devuelve 3, que es una
   cota: vale a lo más 3.
2. No. La línea 14 regresa, pero n4 ya no tenía hijos pendientes. Una poda
   ahorra solo cuando quedan hijos por generar.
:::

::: exercise {#jue-c2-ej-igualdad title="Decide si importa el igual"}
Cambia la línea 22 por `if v < α` y la 14 por `if v > β`. Recorre otra vez
n1 con el orden fijo.

1. ¿Se poda en n3?
2. ¿Cuántos estados se generan?
3. ¿Cambia el valor de la raíz?
:::

::: hint {#jue-c2-pista-igualdad of="jue-c2-ej-igualdad" title="Revisa n3 y n6"}
Usa el subgrafo de n1, @jue-c2-subgrafo. En n3, $v=+1$ y $\alpha=+1$. ¿Es
$+1<+1$? Si n3 no poda, sus otros hijos se generan: revisa si alguno de
ellos poda con las condiciones estrictas.
:::

::: answer {#jue-c2-resp-igualdad of="jue-c2-ej-igualdad"}
1. No: $+1<+1$ es falso.
2. Los **13**. Sin la poda en n3, el recorrido genera n6 y n13, y ninguna
   otra condición estricta deja hijos sin generar.
3. No: la raíz sigue dando $+1$. Pero con pagos $\pm1$ los empates son la
   regla. En el juego completo, sin el igual, alfa-beta genera **228**
   estados en orden fijo y **171** en invertido, contra 82 y 72.
:::

**Punto de control:** deberías poder escribir DECIDIR-ALFA-BETA y
ALFA-BETA de memoria y decir qué líneas los distinguen de minimax. También,
decir qué guarda cada marco de la pila y llenar la traza del árbol base en
cualquier orden. Y leer cada número devuelto contra su ventana de entrada.


> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | **Alfa-beta (estás aquí)** | **$V$ en la raíz; lo garantiza** |
>
> **Lo que viene.**
>
> - **Minimax con corte**: mirar unas cuantas jugadas y estimar a ojo lo que queda debajo, para cuando el árbol no cabe. Clase 3, [[cortar-y-evaluar|Cortar y evaluar a mano]].
> - **Búsqueda de quietud**: no detenerse a estimar a mitad de un intercambio de capturas. Clase 3, [[mas-alla-del-horizonte|Más allá del horizonte]].
> - **Profundización iterativa**: buscar cada vez un poco más hondo, con una jugada siempre lista para cuando se acabe el tiempo. Clase 3, [[jugar-contra-el-reloj|Jugar contra el reloj]].
> - **Monte Carlo plano**: estimar cada jugada jugando muchas partidas al azar hasta el final, sin escribir ninguna estimación. Clase 3, [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].
> - **MCTS con UCT**: construye un árbol: elige por puntaje dentro de él, lo hace crecer, simula desde la hoja y sube el resultado; manda más partidas a lo que va mejor sin dejar de probar lo otro. Clase 3, [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].

## Lo que hay que llevarse

- **DECIDIR-ALFA-BETA devuelve la jugada.** Es DECIDIR-MINIMAX con
  `mejor_valor` llamado $\alpha$, que la raíz pasa a sus hijos (línea 4).
- **Cuatro líneas nuevas** en la recursión: 14 y 22 leen el número del
  rival y podan; 15 y 23 actualizan el propio. Además cambian las que
  reciben o pasan $\alpha$ y $\beta$ (2, 4, 5, 7, 12 y 20).
- **La pila** guarda, por marco, el estado, la ventana y $v$; lo que un
  hijo cambió se pierde al regresar. Memoria $O(bm)$.
- **Lo que devuelve una llamada se lee contra su ventana de entrada:** a lo
  más, exacto o al menos. Un nodo que no podó también puede devolver una
  cota; por eso la línea 5 es estricta.
- **El orden decide el ahorro:** 12 de 14 en el árbol base, 5 u 8 de 13 en
  n1; $O(b^{m/2})$ con orden perfecto.

Continúa con la [[tarea-mirar-todo-y-podar|tarea de refuerzo]].
