---
id: alfa-beta-como-algoritmo
title: Alfa-beta como algoritmo
nav_title: Alfa-beta como algoritmo
summary: "Los dos recorridos a mano escritos como procedimiento: qué recibe, qué deja sin generar, por qué sus cortes son seguros y por qué el orden de las jugadas decide cuánto ahorra."
status: ready
estimated_time: 20m
tags: [juegos, alfa-beta, poda, algoritmos]
---

# Alfa-beta como algoritmo

**¿Cómo se escribe alfa-beta para cualquier juego, y por qué nunca se
equivoca?**

Al terminar tendrás **el pseudocódigo de alfa-beta**, sabrás por qué sus
cortes no cambian el valor de la raíz y por qué el orden de las jugadas
decide cuánto ahorra.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

> **Supuestos de esta página.** Los mismos de
> [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin
> azar, todo a la vista, toda partida termina y suma cero.

> **Las piezas que usa esta página.** Vienen de
> [[escribir-el-juego|Escribir el juego]]: $S_F$, los finales
> (@jue-c1-finales); $\mathrm{Pl}(s)$, quién mueve, leído del turno guardado
> (@jue-c1-pl); $A(s)$, las jugadas permitidas (@jue-c1-acciones); $T(s,a)$,
> a dónde lleva cada una (@jue-c1-transicion); y $U(s)$, $+1$ si gana
> Blancas y $-1$ si gana Negras (@jue-c1-utilidad).

## 1 · Qué recibe y qué genera

**Piensa: ¿qué tiene alfa-beta que no tenga minimax?**

Dos números más en cada llamada. Todo lo demás es igual.

> **El problema de alfa-beta.**
>
> **Dado (lo que recibe):** un estado $s$, las mismas reglas que minimax
> ($S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$) y dos números, $\alpha$ y $\beta$,
> lo que MAX y MIN ya tienen asegurado (@jue-c2-alfa-beta).
>
> **Encontrar (lo que devuelve):** el valor $V(s)$ si queda estrictamente
> entre $\alpha$ y $\beta$. Si no, una cota que basta para decidir.

**Qué genera:** solo los estados que no poda. Como minimax, recibe las
reglas y no el grafo, y **por eso** la poda ahorra: lo que no se genera no
cuesta nada. Si alguien le hubiera entregado el grafo dibujado, ese trabajo
ya estaría hecho, como se dijo en
[[el-juego-como-grafo|El juego como grafo]].

## 2 · El procedimiento

**Piensa: ¿qué líneas de MINIMAX hay que tocar para cortar?**

```text
INPUT   un estado s; las reglas S_F, Pl, A, T y U de un juego finito,
        por turnos y sin azar; α y β (al empezar, −∞ y +∞).
OUTPUT  V(s) si queda estrictamente entre α y β; si no, una cota que basta para
        decidir. En la raíz, con −∞ y +∞, siempre el valor exacto.

 1  function ALFA-BETA(s, α, β)
 2      if s ∈ S_F: return U(s)
 3      if Pl(s) = MAX
 4          v ← −∞
 5          for each a in A(s)
 6              v ← max(v, ALFA-BETA(T(s, a), α, β))
 7              if v ≥ β: return v                 ▷ corte beta
 8              α ← max(α, v)
 9          return v
10      else                                       ▷ Pl(s) = MIN
11          v ← +∞
12          for each a in A(s)
13              v ← min(v, ALFA-BETA(T(s, a), α, β))
14              if v ≤ α: return v                 ▷ corte alfa
15              β ← min(β, v)
16          return v
```

Compáralo con el MINIMAX de [[minimax-como-algoritmo|la página 2]]: las
líneas 7, 8, 14 y 15 son nuevas, y las 1, 6 y 13 solo pasan $\alpha$ y
$\beta$.

- **Las líneas 7 y 14 cortan.** Salen del `for` antes de tiempo: las
  jugadas que faltan nunca llegan a la línea 6 o 13, así que su $T(s,a)$
  nunca se calcula.
- **Las líneas 8 y 15 actualizan lo asegurado**, que heredan los hijos
  siguientes.

La llamada inicial es ALFA-BETA($s$, $-\infty$, $+\infty$), y la jugada se
elige en la raíz como en DECIDIR.

**Es la misma idea de [[ramificar-y-acotar|ramificar y acotar]],** con dos
jugadores:

| Ramificar y acotar | Alfa-beta |
|---|---|
| `mejor`, el valor de un plan que ya tenemos | $\alpha$ para MAX y $\beta$ para MIN |
| La cota de un subproblema | $v$ en un nodo del rival: lo que esa rama puede dar, como mucho |
| Cerrar si la cota no supera `mejor` | Cortar si $v\le\alpha$ o si $v\ge\beta$ |
| Un nodo cerrado no tiene su óptimo calculado | Un nodo donde se cortó solo tiene una cota |

## 3 · Por qué los cortes son seguros

**Piensa: ¿por qué no generar n6 ni n13 no puede cambiar el $+1$ de la
raíz?**

1. **Corte alfa.** En un nodo de MIN con $v\le\alpha$, MIN puede asegurar
   $v$ o menos. Más arriba, MAX tiene otra alternativa que le asegura
   $\alpha\ge v$. Generar los hijos que faltan solo podría **bajar** el
   valor de este nodo, y MAX seguiría prefiriendo su alternativa. La raíz no
   cambia.
2. **Corte beta.** Es el mismo argumento con los papeles cambiados: MAX ya
   puede asegurar $v\ge\beta$, y MIN tiene más arriba una alternativa que le
   asegura $\beta$. MIN nunca dejará que la partida llegue aquí.

Lo que se mantiene en cada llamada es esta propiedad sobre el número $w$
que devuelve ALFA-BETA($s$, $\alpha$, $\beta$):

> Si $w\le\alpha$, el valor exacto de $s$ es a lo más $w$. Si $w\ge\beta$,
> es al menos $w$. Si $w$ queda estrictamente entre $\alpha$ y $\beta$, es
> el valor exacto.

En la raíz, $\alpha=-\infty$ y $\beta=+\infty$, así que cualquier $w$ queda
entre los dos: **el valor de la raíz es exacto**. Los nodos de abajo pueden
devolver solo cotas, como n3 y n6 en [[alfa-beta|Alfa-beta a mano]].

**Y termina** por la misma razón que minimax: recorre el mismo árbol finito,
en el mismo orden, y nunca genera un estado que minimax no generaría. Solo
puede salir antes de un `for`.

## 4 · El orden decide cuánto ahorra

**Piensa: ¿de qué depende que alfa-beta ahorre mucho o poco?**

Del **orden** en que se revisan las jugadas. Mismo árbol, mismos finales:

::: table {#jue-c2-ahorro title="Nodos generados por cada recorrido"}
| Recorrido | Desde n1 | Desde $s_0$, todo el juego |
|---|---:|---:|
| Minimax | 13 | 252 |
| Alfa-beta, orden fijo | 5 | 82 |
| Alfa-beta, orden invertido | 8 | 72 |
:::

En n1, el orden fijo revisó primero $\text{c1}\textbf{-}\text{c2}$, la
mejor jugada de Blancas: el $+1$ quedó asegurado de entrada y bastó para
cortar pronto. En el juego completo gana el orden invertido. Ningún orden
es el mejor siempre. **Cuanto antes aparece una buena jugada, más alto
queda $\alpha$ o más bajo queda $\beta$, y más se corta.**

::: remark {#jue-c2-costo-alfa-beta title="Costo de alfa-beta"}
Con $b$ jugadas por estado y profundidad $m$:

- **Peor caso:** si las jugadas llegan en el peor orden, no se corta nada y
  el tiempo es $O(b^m)$, igual que minimax.
- **Mejor caso:** si en cada nodo la mejor jugada se revisa primero, el
  tiempo baja a $O(b^{m/2})$.
- **Memoria:** $O(bm)$, como minimax: solo el camino actual.
:::

$O(b^{m/2})$ es lo mismo que $O\bigl((\sqrt b)^m\bigr)$: es como si cada
estado tuviera $\sqrt b$ jugadas en vez de $b$. Con el mismo tiempo,
alfa-beta bien ordenado puede mirar **el doble de profundo** que minimax.
Nadie conoce de antemano la mejor jugada, claro; los programas reales usan
reglas para adivinar un buen orden, como revisar primero las capturas. Eso
vuelve en la clase 3.

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
2. Los **13**. Sin el corte en n3, el recorrido genera n6 y n13, y en este
   árbol ninguna otra condición estricta se cumple.
3. No: la raíz sigue dando $+1$. El igual no cambia la respuesta, pero en
   un juego con utilidades $\pm1$ los empates son la regla, y sin él se
   pierde casi toda la poda.
:::

## 5 · Si sabes entre qué valores cae la utilidad

**Piensa: en hexapawn, $U$ solo vale $+1$ o $-1$. ¿Puede aprovecharlo
alfa-beta?**

Sí. Empezar con $\alpha=-\infty$ y $\beta=+\infty$ dice «no sé nada». Pero
sí sabemos algo: ningún valor baja de $-1$ ni sube de $+1$. Llamar
ALFA-BETA(n1, $-1$, $+1$) lo usa:

- n2 vale $+1$, y en la raíz $v=+1\ge\beta=+1$: **corte beta en la raíz**.
- Se generan **2 estados**, n1 y n2. Blancas ya ganó: nada puede ser mejor
  que ganar.

En el juego completo, con esa ventana, alfa-beta genera **49** estados con
el orden fijo y **53** con el invertido, contra 82 y 72. Con la ventana la
raíz puede devolver una cota en vez del valor, pero aquí no importa: una
cota de «al menos $+1$» o «a lo más $-1$» ya es exacta, porque $U$ no sale
de $[-1,+1]$.

Esta misma idea, conocer las cotas de $U$, es la que permite podar también
en árboles con nodos de azar.

::: table {#jue-c2-que-cambia-ab title="Qué cambia cuando cambia el orden o el juego"}
| Cambio | Efecto en alfa-beta |
|---|---|
| La mejor jugada se revisa primero en cada nodo | Más cortes; tiempo cercano a $O(b^{m/2})$ |
| Las jugadas llegan en el peor orden | Ningún corte; el mismo trabajo que minimax |
| Crece $b$ | El ahorro posible crece: se pasa de $b^m$ a $b^{m/2}$ |
| Se conocen las cotas de $U$ | Se puede empezar con una ventana más chica y cortar más |
| El juego tiene azar | Hace falta otra versión, que use las cotas de $U$ |
:::

**Punto de control:** deberías poder escribir ALFA-BETA de memoria, decir
qué líneas lo distinguen de MINIMAX, explicar con el corte alfa y el corte
beta por qué la raíz no cambia y decir qué decide cuánto se ahorra.

## Lo que hay que llevarse

- Alfa-beta recibe las mismas reglas que minimax, más $\alpha$ y $\beta$.
  Ahorra justo lo que no genera.
- Cuatro líneas nuevas: dos cortan, dos actualizan lo asegurado. Los cortes
  son seguros porque lo que falta ya no puede cambiar la decisión de arriba.
- La raíz da el valor exacto; un nodo donde se cortó, solo una cota.
- El orden decide el ahorro: $O(b^m)$ en el peor caso y $O(b^{m/2})$ en el
  mejor. En hexapawn, 82 o 72 estados en vez de 252.

Continúa con la [[tarea-mirar-todo-y-podar|tarea de refuerzo]].
