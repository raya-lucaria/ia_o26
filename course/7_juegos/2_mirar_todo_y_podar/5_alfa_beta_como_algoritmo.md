---
id: alfa-beta-como-algoritmo
title: Alfa-beta como algoritmo
nav_title: Alfa-beta como algoritmo
summary: "Los recorridos a mano escritos como procedimiento: qué devuelve, cómo elige la jugada en la raíz, por qué sus cortes son seguros y por qué el orden de las jugadas decide cuánto ahorra."
status: ready
estimated_time: 20m
tags: [juegos, alfa-beta, poda, algoritmos]
---

# Alfa-beta como algoritmo

**¿Cómo se escribe alfa-beta para cualquier juego, y por qué nunca se
equivoca?**

Al terminar tendrás:

- **el pseudocódigo de alfa-beta**, y el de la función que elige la jugada;
- la razón por la que **sus cortes no cambian el valor de la raíz**;
- la razón por la que **el orden de las jugadas** decide cuánto ahorra.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

> **Supuestos de esta página.** Los mismos de
> [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin
> azar, todo a la vista, toda partida termina y suma cero.

> **Las piezas que usa esta página.** Vienen de
> [[escribir-el-juego|Escribir el juego]]:
>
> - $S_F$, los finales (@jue-c1-finales);
> - $\mathrm{Pl}(s)$, quién mueve, leído del turno guardado (@jue-c1-pl);
> - $A(s)$, las jugadas permitidas (@jue-c1-acciones);
> - $T(s,a)$, a dónde lleva cada una (@jue-c1-transicion);
> - $U(s)$, $+1$ si gana Blancas y $-1$ si gana Negras (@jue-c1-utilidad);
> - $\alpha$ y $\beta$, lo que MAX y MIN ya tienen asegurado
>   (@jue-c2-alfa-beta).

Los dos recorridos de n1 ya los hiciste en
[[alfa-beta|Alfa-beta a mano]]. Aquí no se repiten: se escriben como
procedimiento.

## 1 · Qué recibe y qué devuelve

**Piensa: ¿qué tiene alfa-beta que no tenga minimax?**

**Dos números más en cada llamada**, $\alpha$ y $\beta$. Lo demás es igual.

> **El problema de alfa-beta.**
>
> **Dado (lo que recibe):** un estado $s$, las mismas reglas que minimax
> ($S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$) y la ventana $[\alpha,\beta]$
> de @jue-c2-ab-ventana.
>
> **Encontrar (lo que devuelve):** un número $w$.
>
> - Si $\alpha<w<\beta$, **$w$ es el valor exacto** $V(s)$.
> - Si $w\le\alpha$, es una **cota superior**: $V(s)$ es a lo más $w$.
> - Si $w\ge\beta$, es una **cota inferior**: $V(s)$ es al menos $w$.

Esta versión se llama **fail-soft**: al cortar devuelve su $v$ tal cual,
aunque caiga fuera de la ventana. Otra versión, *fail-hard*, devolvería
$\alpha$ o $\beta$ en vez de $v$; el valor de la raíz es el mismo.

**Qué genera:** solo los estados que no poda.

- Como minimax, **recibe las reglas, no el grafo**.
- **Por eso la poda ahorra:** lo que no se genera no cuesta nada.
- Con el grafo ya dibujado, ese trabajo estaría hecho, como se dijo en
  [[el-juego-como-grafo|El juego como grafo]].

## 2 · El procedimiento

**Piensa: ¿qué líneas de MINIMAX hay que tocar para cortar?**

```text
INPUT   un estado s; las reglas S_F, Pl, A, T y U
        de un juego finito, por turnos y sin azar;
        α y β (al empezar, −∞ y +∞).
OUTPUT  un número w. Si α < w < β, w = V(s).
        Si w ≤ α, cota superior: V(s) ≤ w.
        Si w ≥ β, cota inferior: V(s) ≥ w.
        En la raíz, con −∞ y +∞, siempre V(s).

 1  function ALFA-BETA(s, α, β)
        ▷ Caso base: un final ya vale su utilidad.
 2      if s ∈ S_F: return U(s)
        ▷ Mueve MAX: busca el hijo más alto.
 3      if Pl(s) = MAX
 4          v ← −∞                    ▷ menor que todo
 5          for each a in A(s)        ▷ un hijo por vuelta
                ▷ valora el hijo con lo asegurado hasta ahora
 6              v ← max(v, ALFA-BETA(T(s, a), α, β))
                ▷ arriba, MIN ya tiene algo igual o mejor
 7              if v ≥ β: return v    ▷ corte beta
 8              α ← max(α, v)         ▷ MAX ya asegura v
 9          return v                  ▷ valor o cota
10      else                          ▷ Pl(s) = MIN
            ▷ Mueve MIN: busca el hijo más bajo.
11          v ← +∞                    ▷ mayor que todo
12          for each a in A(s)        ▷ un hijo por vuelta
                ▷ valora el hijo con lo asegurado hasta ahora
13              v ← min(v, ALFA-BETA(T(s, a), α, β))
                ▷ arriba, MAX ya tiene algo igual o mejor
14              if v ≤ α: return v    ▷ corte alfa
15              β ← min(β, v)         ▷ MIN ya asegura v
16          return v                  ▷ valor o cota
```

El mismo procedimiento en Python, línea por línea; el número entre
paréntesis es la línea del pseudocódigo:

```python
from math import inf

# Las reglas: es_final(s), pl(s), acciones(s),
# transicion(s, a) y utilidad(s). pl(s) da "MAX" o "MIN".
# Se llama como alfa_beta(s, -inf, inf).

def alfa_beta(s, alfa, beta):         # (1)
    # (2) Caso base: un final ya vale su utilidad.
    if es_final(s):
        return utilidad(s)
    if pl(s) == "MAX":                # (3) mueve MAX
        v = -inf                      # (4) menor que todo
        for a in acciones(s):         # (5) un hijo por vuelta
            # (6) valora el hijo con alfa y beta actuales
            h = alfa_beta(transicion(s, a), alfa, beta)
            v = max(v, h)
            # (7) Corte beta: las demás no se generan.
            if v >= beta:
                return v
            alfa = max(alfa, v)       # (8) MAX ya asegura v
        return v                      # (9) valor o cota
    else:                             # (10) mueve MIN
        v = inf                       # (11) mayor que todo
        for a in acciones(s):         # (12) un hijo por vuelta
            # (13) valora el hijo con alfa y beta actuales
            h = alfa_beta(transicion(s, a), alfa, beta)
            v = min(v, h)
            # (14) Corte alfa: las demás no se generan.
            if v <= alfa:
                return v
            beta = min(beta, v)       # (15) MIN ya asegura v
        return v                      # (16) valor o cota
```

Compáralo con el MINIMAX de [[minimax-como-algoritmo|la página 2]]:

| Línea | Qué hace |
|---|---|
| 1 | Recibe $\alpha$ y $\beta$, además de $s$ |
| 6 y 13 | Pasan $\alpha$ y $\beta$ al hijo |
| **7 y 14** | **Cortan**: salen del `for` antes de tiempo |
| **8 y 15** | **Encogen la ventana**: lo asegurado sube o baja |
| 9 y 16 | Devuelven $v$: un valor o una cota |
| 2, 3, 4, 5, 10, 11 y 12 | Lo mismo que en MINIMAX |

- **Un corte ahorra de verdad.** Las jugadas que faltan nunca llegan a la
  línea 6 o 13, así que su $T(s,a)$ nunca se calcula.
- **La ventana encogida se hereda.** Los hijos siguientes reciben el
  $\alpha$ o el $\beta$ nuevos.

### De un número a una jugada

**Piensa: en orden fijo, n2 devolvió $+1$ y n3 también. ¿Da igual cuál
jugar?**

**No.** n2 vale $+1$ exacto. n3 devolvió $+1$ por un corte: es una cota,
«a lo más $+1$». Su valor exacto es $-1$. Si la raíz elige «cualquier
jugada con el mayor número», puede quedarse con
$\text{c1}\textbf{x}\text{b2}$, que **pierde**.

> **La regla del empate en la raíz.** La jugada se guarda **solo cuando
> $v$ mejora estrictamente** lo que la raíz ya tenía. Un hijo que devolvió
> una cota no desplaza a la jugada guardada en un empate.

```text
INPUT   un estado s con Pl(s) = MAX, y las mismas reglas.
OUTPUT  una jugada a∗ de A(s) que alcanza V(s).

 1  function DECIDIR-ALFA-BETA(s)
 2      α ← −∞; mejor ← ninguna
 3      for each a in A(s)            ▷ un hijo por vuelta
            ▷ valora el hijo con lo que la raíz ya asegura
 4          v ← ALFA-BETA(T(s, a), α, +∞)
            ▷ guarda la jugada solo si mejora estrictamente
 5          if v > α: α ← v; mejor ← a
 6      return mejor                  ▷ la jugada, no el número
```

En Python, con la función `alfa_beta` de arriba:

```python
def decidir_alfa_beta(s):             # (1)
    alfa, mejor = -inf, None          # (2)
    for a in acciones(s):             # (3) un hijo por vuelta
        # (4) valora el hijo con lo que la raíz ya asegura
        v = alfa_beta(transicion(s, a), alfa, inf)
        # (5) Solo si mejora estrictamente: una cota que
        # empata no desplaza a la jugada guardada.
        if v > alfa:
            alfa, mejor = v, a
    return mejor                      # (6) la jugada
```

**Por qué basta el $>$ de la línea 5:**

- Un hijo que devuelve $v>\alpha$ cae estrictamente dentro de su ventana,
  que va de $\alpha$ a $+\infty$: **su valor es exacto**.
- Un hijo que devuelve $v\le\alpha$ solo promete «a lo más $v$»: no puede
  ser mejor que la jugada guardada.
- En n1, orden fijo: $\text{c1}\textbf{-}\text{c2}$ entra con $+1$;
  $\text{c1}\textbf{x}\text{b2}$ devuelve $+1$, y $+1>+1$ es falso. **Queda
  $\text{c1}\textbf{-}\text{c2}$.**
- En orden invertido: $\text{c1}\textbf{x}\text{b2}$ entra con $-1$ exacto
  y $\text{c1}\textbf{-}\text{c2}$ la desplaza con $+1>-1$.

DECIDIR-ALFA-BETA genera los mismos estados que ALFA-BETA en la raíz: 5 en
orden fijo y 8 en invertido.

## 3 · A media ejecución

**Piensa: en el instante del corte en n3, ¿qué tiene alfa-beta en
memoria?**

Lo mismo que minimax, **más dos números por marco**. La figura es la gemela
de @jue-c2-genera, en orden fijo:

::: figure {#jue-c2-ab-a-media title="ALFA-BETA a media ejecución"}
![La pila de llamadas de alfa-beta en orden fijo, en el instante del corte en n3. Resaltado, el camino n1, n3, n4. Cada marco muestra la ventana con la que llegó y su v: n1 llegó con menos infinito y más infinito, ya tiene v = +1 y alfa = +1; n3 llegó con +1 y más infinito y tiene v = +1, que no supera alfa: ahí corta; n4 llegó con +1 y más infinito y devolvió +1. n2 y n5 aparecen tenues: ya devolvieron +1. n6 y n13 son cajas punteadas con signo de interrogación: no se generarán](../_assets/jue-ab-a-media-ejecucion.svg)
:::

**Qué guarda cada marco:**

- **el estado** $s$ y la jugada por la que va su `for`;
- **la ventana** $[\alpha,\beta]$, que pudo encogerse desde que llegó;
- **$v$**, el mejor valor visto entre sus hijos.

La memoria sigue siendo $O(bm)$: solo el camino actual.

## 4 · Por qué los cortes son seguros

**Piensa: ¿por qué saltarse n6 y n13 no cambia el $+1$ de la raíz?**

**Corte alfa,** en un nodo de MIN con $v\le\alpha$:

- MIN ya puede asegurar $v$ o menos aquí.
- Más arriba, MAX tiene otra alternativa que le asegura $\alpha\ge v$.
- Los hijos que faltan solo podrían **bajar** este nodo.
- MAX seguiría prefiriendo su alternativa: la raíz no cambia.

**Corte beta,** en un nodo de MAX con $v\ge\beta$: el mismo argumento con
los papeles cambiados. **MIN nunca dejará que la partida llegue aquí.**

**El invariante.** Cada llamada ALFA-BETA($s$, $\alpha$, $\beta$) cumple
esto sobre el número $w$ que devuelve:

| Si $w$ cae… | Entonces $V(s)$ es… |
|---|---|
| $w\le\alpha$ | a lo más $w$ |
| $w\ge\beta$ | al menos $w$ |
| $\alpha<w<\beta$ | exactamente $w$ |

- **En la raíz,** $\alpha=-\infty$ y $\beta=+\infty$: cualquier $w$ cae
  dentro. **El valor de la raíz es exacto.**
- **Abajo,** un nodo puede devolver solo una cota, como n3 y n6 en
  [[alfa-beta|Alfa-beta a mano]].
- **Y termina** por la misma razón que minimax: recorre el mismo árbol
  finito y nunca genera un estado que minimax no generaría. Solo puede
  salir antes de un `for`.

## 5 · El orden decide cuánto ahorra

**Piensa: ¿de qué depende que alfa-beta ahorre mucho o poco?**

Del **orden** en que se revisan las jugadas. Mismo árbol, mismos finales:

::: table {#jue-c2-ahorro title="Nodos generados por cada recorrido"}
| Recorrido | Desde n1 | Desde $s_0$, todo el juego |
|---|---:|---:|
| Minimax | 13 | 252 |
| Alfa-beta, orden fijo | 5 | 82 |
| Alfa-beta, orden invertido | 8 | 72 |
:::

- **En n1 gana el orden fijo.** Revisa primero
  $\text{c1}\textbf{-}\text{c2}$, la mejor jugada de Blancas: el $+1$ queda
  asegurado de entrada y corta pronto.
- **En el juego completo gana el invertido.** Ningún orden es el mejor
  siempre.
- **La regla:** cuanto antes aparece una buena jugada, más sube $\alpha$ o
  más baja $\beta$, y **más se corta**.

::: remark {#jue-c2-costo-alfa-beta title="Costo de alfa-beta"}
Con $b$ jugadas por estado y profundidad $m$:

- **Peor caso:** si las jugadas llegan en el peor orden, no se corta nada y
  el tiempo es $O(b^m)$, igual que minimax.
- **Mejor caso:** si en cada nodo la mejor jugada se revisa primero, el
  tiempo baja a $O(b^{m/2})$.
- **Memoria:** $O(bm)$, como minimax: solo el camino actual.
:::

Qué quiere decir $O(b^{m/2})$:

- Es lo mismo que $O\bigl((\sqrt b)^m\bigr)$: **como si cada estado
  tuviera $\sqrt b$ jugadas** en vez de $b$.
- Con el mismo tiempo, alfa-beta bien ordenado mira **el doble de
  profundo** que minimax.
- Nadie conoce de antemano la mejor jugada. Los programas reales
  **adivinan un buen orden**, por ejemplo capturas primero. Eso vuelve en
  la clase 3.

::: figure {#jue-c2-ab-arbol-c title="El árbol C"}
![El árbol C, de tres niveles y 15 nodos. La raíz es de MAX y tiene dos hijos de MIN. El MIN izquierdo tiene dos hijos de MAX, con hojas 3 y 5 el primero, y 6 y 9 el segundo. El MIN derecho tiene dos hijos de MAX, con hojas 2 y 4 el primero, y 7 y 1 el segundo. Sin marcas: es el enunciado del ejercicio](../_assets/jue-ab-arbol-c.svg)
:::

::: exercise {#jue-c2-ej-arbol-c title="Recorre el árbol C"}
Aplica ALFA-BETA a la raíz del árbol C, con $[-\infty,+\infty]$.

1. Con los hijos en el orden dibujado, ¿cuántos de los 15 nodos se
   generan? ¿Dónde se corta, y qué se poda?
2. ¿Cuánto vale la raíz?
3. Invierte la lista de hijos de **cada** nodo y recorre otra vez. ¿Cuántos
   nodos se generan?
:::

::: hint {#jue-c2-pista-arbol-c of="jue-c2-ej-arbol-c" title="Escribe la ventana al llegar"}
Anota $[\alpha,\beta]$ junto a cada nodo en cuanto lo generas. El MAX con
hojas 6 y 9 llega cuando su padre MIN ya vio un 5. Recuerda que **el igual
también corta**.
:::

::: answer {#jue-c2-resp-arbol-c of="jue-c2-ej-arbol-c"}
1. **11 de 15.** Dos cortes:
   - **Corte beta en el MAX (6, 9).** Llega con $[-\infty,5]$, porque su
     hermano MAX (3, 5) valió 5. Su primera hoja da $6\ge5$: **el 9 no se
     genera**. Devuelve 6, «al menos 6».
   - **Corte alfa en el MIN derecho.** Llega con $[5,+\infty]$, porque el
     MIN izquierdo devolvió 5. Su primer hijo, MAX (2, 4), devuelve 4, y
     $4\le5$: **el MAX (7, 1) y sus dos hojas no se generan**, 3 nodos.
     Devuelve 4, «a lo más 4».
2. **5**, lo mismo que minimax: el MIN izquierdo vale
   $\min\{5,9\}=5$ y el derecho $\min\{4,7\}=4$.
3. **15 de 15, ningún corte.** El MIN derecho va primero y solo asegura
   $\alpha=4$. Dentro del izquierdo, el MAX (9, 6) da 9 y el MAX (5, 3) da
   5: ninguno toca la ventana. La mejor jugada llega al final.
:::

::: exercise {#jue-c2-ej-se-corta title="Decide si se corta"}
1. Un nodo de MIN recibe $\alpha=4$ y $\beta=9$. Su primer hijo devuelve 6,
   el segundo 3, y tiene un tercer hijo. ¿Hay corte después del primero?
   ¿Cuánto vale $\beta$ entonces? ¿Hay corte después del segundo?
2. En el recorrido invertido, n4 tenía $\beta=-1$ y su único hijo valía
   $+1$. La condición $v\ge\beta$ se cumplía. ¿Ahorró algo?
:::

::: hint {#jue-c2-pista-se-corta of="jue-c2-ej-se-corta" title="La línea 14, y después la 15"}
Para el inciso 1, sigue las líneas 13, 14 y 15 una vez por hijo. Para el
inciso 2, pregúntate qué deja sin generar un corte.
:::

::: answer {#jue-c2-resp-se-corta of="jue-c2-ej-se-corta"}
1. Tras el primero, $v=6$ y $6\le4$ es falso: no hay corte, y $\beta$ baja a
   $\min\{9,6\}=6$. Tras el segundo, $v=\min\{6,3\}=3\le\alpha=4$: **corte
   alfa**, y el tercer hijo no se genera. El nodo devuelve 3, que es una
   cota: vale a lo más 3.
2. No. La línea 7 devuelve $v$, pero n4 ya no tenía hijos pendientes. Un
   corte ahorra solo cuando quedan hijos por generar.
:::

::: exercise {#jue-c2-ej-igualdad title="Decide si importa el igual"}
Cambia la línea 14 por `if v < α` y la 7 por `if v > β`. Recorre otra vez
n1 con el orden fijo.

1. ¿Se corta en n3?
2. ¿Cuántos estados se generan?
3. ¿Cambia el valor de la raíz?
:::

::: hint {#jue-c2-pista-igualdad of="jue-c2-ej-igualdad" title="Revisa n3 y n6"}
En n3, $v=+1$ y $\alpha=+1$. ¿Es $+1<+1$? Si n3 no corta, sus otros hijos se
generan: revisa si alguno de ellos corta con las condiciones estrictas.
:::

::: answer {#jue-c2-resp-igualdad of="jue-c2-ej-igualdad"}
1. No: $+1<+1$ es falso.
2. Los **13**. Sin el corte en n3, el recorrido genera n6 y n13, y ninguna
   otra condición estricta deja hijos sin generar: en n3, tras n13,
   $-1<+1$ se cumple, pero ya no quedan hijos.
3. No: la raíz sigue dando $+1$. El igual no cambia la respuesta, pero en
   un juego con utilidades $\pm1$ los empates son la regla. En el juego
   completo, sin el igual, alfa-beta genera **228** estados en orden fijo y
   **171** en invertido, contra 82 y 72: se pierde casi toda la poda.
:::

## 6 · Para ir más lejos

**Piensa: en hexapawn, $U$ solo vale $+1$ o $-1$. ¿Puede aprovecharlo
alfa-beta?**

### Una ventana más chica

**Sí.** Empezar con $[-\infty,+\infty]$ dice «no sé nada». Pero ningún
valor baja de $-1$ ni sube de $+1$. Llamar ALFA-BETA(n1, $-1$, $+1$) lo
usa:

- n2 vale $+1$, y en la raíz $v=+1\ge\beta=+1$: **corte beta en la raíz**.
- Se generan **2 estados**, n1 y n2. Blancas ya ganó: nada es mejor que
  ganar.

En el juego completo:

| Recorrido | Ventana $[-\infty,+\infty]$ → $[-1,+1]$ |
|---|---|
| Orden fijo | 82 → **49** estados |
| Orden invertido | 72 → **53** estados |

- **La raíz puede devolver una cota**, no el valor exacto: n1 cortó en la
  raíz.
- **Aquí es segura.** «Al menos $+1$» o «a lo más $-1$» ya son exactas,
  porque $U$ no sale de $[-1,+1]$.
- **La misma idea**, conocer las cotas de $U$, permite podar también en
  árboles con nodos de azar.

::: table {#jue-c2-que-cambia-ab title="Qué cambia cuando cambia el orden o el juego"}
| Cambio | Efecto en alfa-beta |
|---|---|
| La mejor jugada se revisa primero en cada nodo | Más cortes; tiempo cercano a $O(b^{m/2})$ |
| Las jugadas llegan en el peor orden | Ningún corte; el mismo trabajo que minimax |
| Crece $b$ | El ahorro posible crece: se pasa de $b^m$ a $b^{m/2}$ |
| Se conocen las cotas de $U$ | Se puede empezar con una ventana más chica y cortar más |
| El juego tiene azar | Hace falta otra versión, que use las cotas de $U$ |
:::

### La misma idea que ramificar y acotar

Alfa-beta es [[ramificar-y-acotar|ramificar y acotar]] con dos jugadores:

| Ramificar y acotar | Alfa-beta |
|---|---|
| `mejor`, el valor de un plan que ya tenemos | $\alpha$ para MAX y $\beta$ para MIN |
| La cota de un subproblema | $v$ en un nodo del rival: lo que esa rama puede dar, como mucho |
| Cerrar si la cota no supera `mejor` | Cortar si $v\le\alpha$ o si $v\ge\beta$ |
| Un nodo cerrado no tiene su óptimo calculado | Un nodo donde se cortó solo tiene una cota |

**Punto de control:** deberías poder escribir ALFA-BETA y DECIDIR-ALFA-BETA
de memoria, decir qué líneas lo distinguen de MINIMAX, explicar con el
invariante por qué la raíz no cambia, y recorrer el árbol C contando nodos
en los dos órdenes.

## Lo que hay que llevarse

- Alfa-beta recibe las mismas reglas que minimax, **más $\alpha$ y
  $\beta$**. Ahorra justo lo que no genera.
- **Cuatro líneas nuevas:** dos cortan y dos encogen la ventana.
- Devuelve **el valor si cae estrictamente entre** $\alpha$ y $\beta$; si
  no, **una cota**: superior si $w\le\alpha$, inferior si $w\ge\beta$.
- **En la raíz, la jugada cambia solo si $v$ mejora estrictamente:** una
  cota que empata no gana.
- **El orden decide el ahorro:** $O(b^m)$ en el peor caso y $O(b^{m/2})$
  en el mejor. En hexapawn, 82 o 72 estados en vez de 252.

Continúa con la [[tarea-mirar-todo-y-podar|tarea de refuerzo]].
