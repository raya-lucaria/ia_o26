---
id: alfa-beta
title: Alfa-beta
nav_title: Alfa-beta
summary: "Descartar ramas del árbol sin revisarlas y sin cambiar el valor de la raíz: dos recorridos del mismo subárbol de hexapawn, el procedimiento general, por qué sus cortes son seguros y por qué el orden decide cuánto ahorra."
status: ready
estimated_time: 40m
tags: [juegos, alfa-beta, poda, algoritmos]
---

# Alfa-beta

**¿Cómo descartar ramas sin revisarlas y sin cambiar la respuesta?**

Al terminar tendrás **dos recorridos de alfa-beta hechos a mano** sobre el
mismo árbol, uno que revisa 5 nodos y otro que revisa 8, y sabrás explicar
por qué los dos dan el mismo valor.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todo o deja al rival sin jugada; gana
> $10-k$ puntos, donde $k$ es el número de jugadas de la partida, y el otro
> pierde esos mismos puntos.

**Problema activo: el mismo subárbol de [[minimax|minimax a mano]].**
Tras a1-a2 y b3-b2 mueven Blancas, con $k=2$.

::: table {#jue-c2-subarbol-ab title="El problema activo: mueven Blancas, k = 2"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | · | N |
| **2** | B | N | · |
| **1** | · | B | B |
:::

Este es su árbol, en el orden fijo de las jugadas, con los mismos números
n1 a n13 de minimax y el valor de cada final:

- **n1 · Raíz** · B (MAX)
  - **n2 · c1-c2** · final, $U=7$
  - **n3 · c1xb2** · N (MIN)
    - **n4 · a3xb2** · B (MAX)
      - **n5 · a2-a3** · final, $U=5$
    - **n6 · c3-c2** · B (MAX)
      - **n7 · b1xc2** · N (MIN)
        - **n8 · a3xb2** · B (MAX)
          - **n9 · a2-a3** · final, $U=3$
          - **n10 · c2-c3** · final, $U=3$
      - **n11 · b2-b3** · final, $U=5$
      - **n12 · b2xa3** · final, $U=5$
    - **n13 · c3xb2** · final, $U=-6$

Minimax revisó los 13 nodos y obtuvo $V=7$, con la jugada c1-c2.
**Nosotros ya conocemos $V=7$; el algoritmo empezará sin él.** Lo usaremos
al final para comprobar la respuesta.

En [[ramificar-y-acotar|ramificar y acotar]] cerrábamos un subproblema
completo cuando su **cota** no superaba el **mejor** valor ya encontrado.
Alfa-beta hace lo mismo en un árbol de juego, con una diferencia: aquí hay
dos jugadores, y cada uno lleva su propio «mejor».

## 1 · Ver un corte con números

**Piensa: si Blancas ya tiene una jugada que vale 7, ¿necesita saber
exactamente cuánto vale otra?**

Sigamos el recorrido en profundidad, en el orden fijo:

1. Blancas revisa **n2 = c1-c2**: es final y vale 7. Blancas ya tiene
   **asegurado 7**, juegue lo que juegue después.
2. Blancas revisa **n3 = c1xb2**. Ahí manda Negras. Su primera respuesta,
   **n4 = a3xb2**, lleva a un final, n5, que vale 5.
3. Con solo eso, Negras **ya puede dejar a Blancas en 5 o menos** en esta
   rama: le basta con jugar a3xb2. Sus otras respuestas solo podrían bajar
   ese número, nunca subirlo.

Para Blancas, 5 o menos es peor que el 7 que ya tiene. **La rama n3 ya no
puede mejorar a Blancas**, valgan lo que valgan n6 (c3-c2) y n13 (c3xb2).
Esos dos hijos de n3 no se revisan.

Revisamos **5 nodos de 13**: n1, n2, n3, n4 y n5. La respuesta es la
misma: $V=7$, con c1-c2.

**Ojo:** no supimos cuánto vale n3. Solo supimos que vale **a lo más 5**.
Su valor exacto, −6, nunca se calculó, y no hacía falta.

## 2 · Nombrar lo que cada jugador ya tiene asegurado

Para hacer este razonamiento en cualquier nodo, cada llamada lleva dos
números: lo que MAX ya tiene asegurado y lo que MIN ya tiene asegurado en
el camino desde la raíz.

::: definition {#jue-c2-alfa-beta title="Alfa y beta"}
En un nodo del recorrido,

- $\alpha$ es el **mayor valor que MAX ya tiene asegurado** con alguna
  alternativa en el camino desde la raíz hasta ese nodo;
- $\beta$ es el **menor valor que MIN ya tiene asegurado** con alguna
  alternativa en ese mismo camino.

Al empezar no hay nada asegurado: $\alpha=-\infty$ y $\beta=+\infty$. El valor
que importa está entre los dos; lo que cae fuera, alguno de los dos ya lo
evitó.
:::

Con esos dos números, $v$ es el mejor valor visto hasta ahora entre los
hijos del nodo actual, como en minimax. Hay dos cortes:

::: definition {#jue-c2-cortes title="Corte alfa y corte beta"}
- **Corte alfa**, en un nodo MIN: si $v\le\alpha$, MIN ya puede dejar a MAX
  en $v$ o menos, y MAX tiene asegurado $\alpha$ en otra parte. MAX nunca
  entrará aquí: se dejan de revisar los hijos que faltan.
- **Corte beta**, en un nodo MAX: si $v\ge\beta$, MAX ya puede conseguir $v$
  o más, y MIN tiene asegurado $\beta$ en otra parte. MIN nunca dejará llegar
  aquí: se dejan de revisar los hijos que faltan.
:::

El corte de la sección 1 fue un **corte alfa**: en n3 (c1xb2), un nodo
MIN, $v=5\le\alpha=7$.

## 3 · Recorrer el subárbol con alfa y beta

Ahora repetimos el recorrido llevando $\alpha$, $\beta$ y $v$ en cada nodo.
Cada hijo **hereda** el $\alpha$ y el $\beta$ que tiene su padre en ese
momento.

### Paso 1 · La raíz revisa n2

**Estamos aquí:** en n1, la raíz, nodo MAX, con $\alpha=-\infty$,
$\beta=+\infty$ y $v=-\infty$.

n2 (c1-c2) es final y vale 7. Entonces $v=\max\{-\infty,7\}=7$.
¿$7\ge\beta=+\infty$? No: no hay corte. Actualizamos $\alpha=7$.

**Pendiente:** el segundo hijo, n3 (c1xb2), que recibe $\alpha=7$ y
$\beta=+\infty$.

### Paso 2 · Negras responde a3xb2

**Estamos aquí:** en n3, nodo MIN, con $\alpha=7$, $\beta=+\infty$ y
$v=+\infty$. Su primer hijo es n4 (a3xb2), un nodo MAX que hereda
$\alpha=7$, $\beta=+\infty$.

n4 tiene un solo hijo, n5 (a2-a3), que es final y vale 5. n4 devuelve 5.
De vuelta en n3, $v=\min\{+\infty,5\}=5$.

**Decide:** ¿hace falta revisar n6 y n13?

::: exercise {#jue-c2-ej-primer-corte title="Decide si se corta en n3"}
En n3 tienes $\alpha=7$ y $v=5$. Es un nodo MIN. ¿Se cumple la condición
de algún corte? ¿Qué valor devuelve n3 a la raíz, y qué sabemos de su
valor exacto?
:::

::: answer {#jue-c2-resp-primer-corte of="jue-c2-ej-primer-corte"}
Sí: $v=5\le\alpha=7$, un **corte alfa**. n3 devuelve 5 sin revisar n6
(c3-c2) ni n13 (c3xb2). Del valor exacto solo sabemos que es **a lo más
5**; minimax calculó que es −6, pero alfa-beta no lo sabe.
:::

n3 devuelve 5 y deja **2 hijos sin visitar**: n6 y n13, con todo lo que
cuelga de n6.

### Paso 3 · La raíz termina

**Estamos aquí:** de vuelta en n1, con $v=7$. El hijo n3 devolvió 5:
$v=\max\{7,5\}=7$. No quedan hijos.

La raíz devuelve **7**, el mismo valor de minimax, y la jugada que lo
alcanzó es c1-c2.

::: table {#jue-c2-traza-natural title="Alfa-beta con el orden fijo: 5 nodos visitados"}
| Orden | Nodo | Tipo | $\alpha$, $\beta$ al llegar | Devuelve | Qué pasa |
|---:|---|---|---|---:|---|
| 1 | n1 = raíz | MAX | $-\infty$, $+\infty$ | 7 | Revisa sus dos hijos |
| 2 | n2 = c1-c2 | Final | $-\infty$, $+\infty$ | 7 | La raíz pasa a $\alpha=7$ |
| 3 | n3 = c1xb2 | MIN | $7$, $+\infty$ | 5 | **Corte alfa** tras n4 |
| 4 | n4 = c1xb2 → a3xb2 | MAX | $7$, $+\infty$ | 5 | Un solo hijo |
| 5 | n5 = c1xb2 → a3xb2 → a2-a3 | Final | $7$, $+\infty$ | 5 | |
| — | n6 y n13, hijos de n3 | | | | No se visitan |
:::

## 4 · Cambiar el orden de las jugadas

**Piensa: si Blancas hubiera mirado primero la captura, ¿se habría ahorrado
lo mismo?**

Repetimos todo con el orden de las jugadas **invertido en todos los
nodos**: la última jugada de cada lista se revisa primero. El árbol y sus
finales no cambian; los nodos conservan sus números. Así queda el árbol con
los hijos ya en el orden en que se revisan:

- **n1 · Raíz** · B (MAX)
  - **n3 · c1xb2** · N (MIN)
    - **n13 · c3xb2** · final, $U=-6$
    - **n6 · c3-c2** · B (MAX)
      - **n12 · b2xa3** · final, $U=5$
      - **n11 · b2-b3** · final, $U=5$
      - **n7 · b1xc2** · N (MIN)
        - **n8 · a3xb2** · B (MAX)
          - **n10 · c2-c3** · final, $U=3$
          - **n9 · a2-a3** · final, $U=3$
    - **n4 · a3xb2** · B (MAX)
      - **n5 · a2-a3** · final, $U=5$
  - **n2 · c1-c2** · final, $U=7$

### Paso 1 · La raíz empieza por n3

**Estamos aquí:** en n1, MAX, con $\alpha=-\infty$, $\beta=+\infty$. Su
primer hijo ahora es n3 (c1xb2), nodo MIN, que hereda $\alpha=-\infty$,
$\beta=+\infty$.

El primer hijo de n3 es ahora n13 (c3xb2): final, vale −6. En n3,
$v=-6$. ¿$-6\le\alpha=-\infty$? No. Actualizamos $\beta=-6$: **Negras ya
tiene asegurado −6**.

**Pendiente:** n6 (c3-c2), que recibe $\alpha=-\infty$ y $\beta=-6$.

### Paso 2 · Blancas en n6

**Estamos aquí:** en n6, nodo MAX, con $\alpha=-\infty$, $\beta=-6$. Su
primer hijo, en el orden invertido, es n12 (b2xa3): final, vale 5. En n6,
$v=5$.

::: exercise {#jue-c2-ej-corte-beta title="Decide si se corta en n6"}
En n6 tienes $\beta=-6$ y $v=5$. Es un nodo MAX. ¿Se cumple la condición
de algún corte? ¿Qué hijos de n6 se dejan de revisar? ¿Qué sabe el
algoritmo del valor de n6?
:::

::: answer {#jue-c2-resp-corte-beta of="jue-c2-ej-corte-beta"}
Sí: $v=5\ge\beta=-6$, un **corte beta**. Se dejan sin revisar n11 (b2-b3)
y n7 (b1xc2), con todo lo que cuelga de n7. El algoritmo solo sabe que n6
vale **al menos 5**. Su valor exacto es 5, pero eso lo sabemos por
minimax, no por este recorrido.
:::

n6 devuelve 5 y deja **2 hijos sin visitar**: n11 y n7. La razón, en
palabras: Negras ya tiene c3xb2 (n13), que la hace ganar; si entrara en
n6, Blancas conseguiría al menos 5. Negras nunca elegirá c3-c2, y no
importa cuánto más que 5 valga.

### Paso 3 · Negras termina, y la raíz también

**Estamos aquí:** de vuelta en n3, con $v=\min\{-6,5\}=-6$ y $\beta=-6$.
Falta n4 (a3xb2), nodo MAX que recibe $\alpha=-\infty$, $\beta=-6$. Su
único hijo, n5 (a2-a3), vale 5; como $5\ge\beta$, se cumpliría un corte
beta, pero a n4 ya no le quedan hijos que ahorrar. n4 devuelve 5.

n3 queda con $v=\min\{-6,5\}=-6$ y lo devuelve. En n1, $v=-6$ y
$\alpha=-6$. Su segundo hijo es n2 (c1-c2), que vale 7:
$v=\max\{-6,7\}=7$.

La raíz devuelve **7**. Mismo valor, misma jugada.

::: table {#jue-c2-traza-invertida title="Alfa-beta con el orden invertido: 8 nodos visitados"}
| Orden | Nodo | Tipo | $\alpha$, $\beta$ al llegar | Devuelve | Qué pasa |
|---:|---|---|---|---:|---|
| 1 | n1 = raíz | MAX | $-\infty$, $+\infty$ | 7 | Revisa sus dos hijos |
| 2 | n3 = c1xb2 | MIN | $-\infty$, $+\infty$ | −6 | Revisa sus tres hijos |
| 3 | n13 = c1xb2 → c3xb2 | Final | $-\infty$, $+\infty$ | −6 | n3 pasa a $\beta=-6$ |
| 4 | n6 = c1xb2 → c3-c2 | MAX | $-\infty$, $-6$ | 5 | **Corte beta** tras n12 |
| 5 | n12 = c1xb2 → c3-c2 → b2xa3 | Final | $-\infty$, $-6$ | 5 | |
| 6 | n4 = c1xb2 → a3xb2 | MAX | $-\infty$, $-6$ | 5 | Un solo hijo |
| 7 | n5 = c1xb2 → a3xb2 → a2-a3 | Final | $-\infty$, $-6$ | 5 | |
| 8 | n2 = c1-c2 | Final | $-6$, $+\infty$ | 7 | La raíz termina en 7 |
| — | n11 y n7, hijos de n6 | | | | No se visitan |
:::

### Lo que dicen los valores devueltos

En los dos recorridos, la **raíz** devuelve el valor exacto, 7. Los nodos
donde hubo corte, no:

| Nodo | Devolvió | Valor exacto | Lo que el algoritmo sabe |
|---|---:|---:|---|
| n3 = c1xb2, orden fijo | 5 | −6 | A lo más 5 |
| n6 = c1xb2 → c3-c2, orden invertido | 5 | 5 | Al menos 5 |

En el segundo caso el número coincide, pero por suerte: el algoritmo
**no lo sabe**. Un nodo podado da una **cota**, no un valor. Si necesitaras el
valor exacto de n6, tendrías que revisar sus hijos restantes, n11 y n7.

## 5 · Escribir el procedimiento general

**Ya hicimos dos ejecuciones.** Estos son los nombres que usa el
procedimiento:

| Nombre | Qué guarda |
|---|---|
| $s$ | El estado que estamos valorando |
| $P(s)$, $A(s)$, $T(s,a)$, $U(s)$ | Las piezas del modelo, como en minimax |
| $\alpha$ | Lo que MAX ya tiene asegurado en el camino hasta $s$ |
| $\beta$ | Lo que MIN ya tiene asegurado en el camino hasta $s$ |
| $v$ | El mejor valor visto hasta ahora entre los hijos de $s$ |

```text
INPUT   un estado s de un juego finito por turnos y sin azar;
        α y β, lo que MAX y MIN ya aseguran (al empezar, −∞ y +∞).
OUTPUT  el valor de s si queda entre α y β; si no, una cota
        que basta para decidir. En la raíz, siempre el valor exacto.

 1  function ALFA-BETA(s, α, β)
 2      if s es final: return U(s)
 3      if P(s) = MAX
 4          v ← −∞
 5          for each a in A(s)
 6              v ← max(v, ALFA-BETA(T(s, a), α, β))
 7              if v ≥ β: return v                 ▷ corte beta
 8              α ← max(α, v)
 9          return v
10      else                                       ▷ P(s) = MIN
11          v ← +∞
12          for each a in A(s)
13              v ← min(v, ALFA-BETA(T(s, a), α, β))
14              if v ≤ α: return v                 ▷ corte alfa
15              β ← min(β, v)
16          return v
```

Compáralo con MINIMAX: las líneas 7, 8, 14 y 15 son las únicas nuevas. Las
líneas 7 y 14 cortan; las 8 y 15 actualizan lo asegurado. La llamada
inicial es ALFA-BETA($s_0$, $-\infty$, $+\infty$), y la jugada se elige en la
raíz como antes.

La relación con ramificar y acotar es directa:

| Ramificar y acotar | Alfa-beta |
|---|---|
| `mejor`, el valor de un plan que ya tenemos | $\alpha$ para MAX y $\beta$ para MIN |
| La cota de un subproblema | $v$ en un nodo del rival: lo que esa rama, como mucho, puede dar |
| Cerrar si la cota no supera `mejor` | Cortar si $v\le\alpha$ o si $v\ge\beta$ |
| Un nodo cerrado no tiene óptimo calculado | Un nodo podado solo tiene una cota |

### Por qué los cortes son seguros

**Piensa: ¿por qué saltarse n6 y n13 no puede cambiar el 7 de la raíz?**

1. **Corte alfa.** En un nodo MIN con $v\le\alpha$, MIN puede asegurar $v$
   o menos. En algún nodo MAX de más arriba, MAX tiene otra alternativa que
   le asegura $\alpha\ge v$. Revisar los hijos que faltan solo podría bajar
   el valor de este nodo, así que MAX seguiría prefiriendo su alternativa.
   El valor de la raíz no cambia.
2. **Corte beta.** Es el mismo argumento con los papeles cambiados: MAX ya
   puede asegurar $v\ge\beta$, y MIN tiene más arriba una alternativa que le
   asegura $\beta$. MIN nunca dejará que la partida llegue aquí.

Lo que se mantiene en cada llamada es esta propiedad sobre el número $w$
que devuelve ALFA-BETA($s$, $\alpha$, $\beta$):

> Si $w\le\alpha$, el valor exacto de $s$ es a lo más $w$. Si $w\ge\beta$, es
> al menos $w$. Si $w$ queda estrictamente entre $\alpha$ y $\beta$, es el
> valor exacto.

En la raíz, $\alpha=-\infty$ y $\beta=+\infty$, así que cualquier $w$ queda entre
los dos: **el valor de la raíz es exacto**. Los nodos de abajo pueden
devolver solo cotas, como n3 y n6.

### Por qué termina

Alfa-beta recorre el mismo árbol finito que minimax, en el mismo orden en
profundidad, y **nunca visita un nodo que minimax no visitaría**. Lo único
que cambia es que puede terminar antes el `for`. Si minimax termina, alfa-beta también, con a lo
más el mismo número de visitas.

## 6 · Contar el trabajo

**Piensa: ¿de qué depende que alfa-beta ahorre mucho o poco?**

Del **orden**. Mismo árbol, mismos finales, distinto orden:

| Recorrido | Nodos visitados | Corte |
|---|---:|---|
| Minimax | 13 | Ninguno |
| Alfa-beta, orden fijo | 5 | Alfa, en n3 |
| Alfa-beta, orden invertido | 8 | Beta, en n6 |

El orden fijo revisó primero c1-c2, la mejor jugada de Blancas: el 7 quedó
asegurado de entrada y bastó para cortar pronto. **Cuanto antes aparece una
buena jugada, más alto queda $\alpha$ o más bajo queda $\beta$, y más se
corta.**

::: remark {#jue-c2-costo-alfa-beta title="Costo de alfa-beta"}
Con $b$ jugadas por estado y profundidad $m$:

- **Peor caso:** si las jugadas llegan en el peor orden, no se corta nada y
  el tiempo es $O(b^m)$, igual que minimax.
- **Mejor caso:** si en cada nodo la mejor jugada se revisa primero, el
  tiempo baja a $O(b^{m/2})$.
- **Memoria:** $O(bm)$, como minimax; solo se guarda el camino actual.
:::

$O(b^{m/2})$ es lo mismo que $O\bigl((\sqrt b)^m\bigr)$: es como si cada estado
tuviera $\sqrt b$ jugadas en vez de $b$. Con el mismo tiempo, alfa-beta bien
ordenado puede mirar **el doble de profundo** que minimax. Nadie conoce de
antemano la mejor jugada, claro; los programas reales usan reglas para
adivinar un buen orden, como revisar primero las capturas. Eso vuelve en la
clase 3.

::: table {#jue-c2-que-cambia-ab title="Qué cambia cuando cambia el orden o el juego"}
| Cambio | Efecto en alfa-beta |
|---|---|
| La mejor jugada se revisa primero en cada nodo | Más cortes; tiempo cercano a $O(b^{m/2})$ |
| Las jugadas llegan en el peor orden | Ningún corte; el mismo trabajo que minimax |
| Crece $b$ | El ahorro posible crece: se pasa de $b^m$ a $b^{m/2}$ |
| El juego tiene azar | Hace falta otra versión, que conozca entre qué valores caen las utilidades |
:::

::: exercise {#jue-c2-ej-se-corta title="Decide si se corta"}
1. Un nodo MIN recibe $\alpha=4$ y $\beta=9$. Su primer hijo devuelve 6 y el
   segundo, 3; tiene un tercer hijo. ¿Hay corte después del primero? ¿Y
   después del segundo? ¿Cuánto vale $\beta$ tras el primero?
2. En el recorrido invertido, n4 (a3xb2) tenía $\beta=-6$ y su único hijo,
   n5, valía 5. La condición $v\ge\beta$ se cumplía. ¿Ahorró algo?
:::

::: answer {#jue-c2-resp-se-corta of="jue-c2-ej-se-corta"}
1. Tras el primero, $v=6$ y $6\le4$ es falso: no hay corte, y $\beta$ baja a
   $\min\{9,6\}=6$. Tras el segundo, $v=\min\{6,3\}=3\le\alpha=4$: **corte
   alfa**, y el tercer hijo no se revisa. El nodo devuelve 3, que es una
   cota: vale a lo más 3.
2. No. La línea 7 devuelve $v$, pero n4 ya no tenía hijos pendientes
   que saltarse. Un corte ahorra solo cuando quedan hijos por revisar.
:::

**Punto de control:** deberías poder recorrer un árbol de cuatro niveles con
alfa-beta, anotar $\alpha$ y $\beta$ en cada nodo, marcar cada corte como alfa o
beta y decir qué nodos no se visitaron. Si te pierdes, vuelve a la tabla de
la sección 3 y sigue una fila a la vez.

## Lo que hay que llevarse

- $\alpha$ es lo que MAX ya tiene asegurado y $\beta$ lo que MIN ya tiene
  asegurado. Se corta en un nodo MIN cuando $v\le\alpha$ y en uno MAX cuando
  $v\ge\beta$.
- La raíz da el mismo valor que minimax; los nodos podados solo dan una
  cota.
- El orden de las jugadas decide el ahorro: 5 contra 8 nodos en el mismo
  árbol; $O(b^{m/2})$ en el mejor caso y $O(b^m)$ en el peor.

Continúa con la [[tarea-mirar-todo-y-podar|tarea de refuerzo]].
