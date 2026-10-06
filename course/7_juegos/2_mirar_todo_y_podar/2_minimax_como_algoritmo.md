---
id: minimax-como-algoritmo
title: Minimax como algoritmo
nav_title: Minimax como algoritmo
summary: "El cálculo a mano escrito como procedimiento general: qué recibe, qué genera mientras recorre, por qué es correcto, por qué termina, cuánto cuesta y un subárbol nuevo para resolver por tu cuenta."
status: ready
estimated_time: 25m
tags: [juegos, minimax, algoritmos]
---

# Minimax como algoritmo

**¿Cómo se escribe lo que hicimos a mano para que sirva en cualquier juego
finito, y cuánto cuesta?**

Al terminar tendrás **el pseudocódigo de minimax**, sabrás qué recibe y qué
genera, por qué es correcto y cuánto cuesta, y habrás resuelto **un subárbol
nuevo de hexapawn por tu cuenta**.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todos los peones rivales o deja al rival
> sin jugada; ganar vale $+1$ y perder, $-1$.

> **Supuestos de esta página.** Los mismos de
> [[escribir-el-juego|Escribir el juego]]: dos jugadores por turnos, sin
> azar, todo a la vista, toda partida termina y suma cero.

En [[minimax|Minimax a mano]] valoramos los 13 nodos de n1, de los finales
hacia la raíz, y obtuvimos $V(\text{n1})=+1$ con
$\text{c1}\textbf{-}\text{c2}$. Esta página convierte ese cálculo en un
procedimiento que no depende de hexapawn.

## 1 · Qué recibe y qué devuelve

**Piensa: para valorar un nodo, ¿qué tuviste que saber de él?**

Si era final y cuánto valía; si no, quién movía, qué jugadas tenía y a
dónde llevaba cada una. Son las piezas de la clase 1. Nada más.

> **El problema de minimax.**
>
> **Dado (lo que recibe):** un estado $s$ y las reglas del juego, como
> funciones que se pueden evaluar en cualquier estado:
>
> - $S_F$, para preguntar si $s$ es final (@jue-c1-finales);
> - $\mathrm{Pl}$, quién mueve: MAX o MIN (@jue-c1-pl);
> - $A$, las jugadas permitidas (@jue-c1-acciones);
> - $T$, a dónde lleva cada jugada (@jue-c1-transicion);
> - $U$, cuánto vale un final para MAX (@jue-c1-utilidad).
>
> **Encontrar (lo que devuelve):** el valor $V(s)$ de @jue-c2-valor, un
> número en puntos de MAX.

**Lo que no recibe es el grafo.** Nadie le entrega los 13 nodos de n1 ni los
135 estados del juego. Minimax los **genera**: cada vez que necesita los
hijos de un estado, calcula $A(s)$ y, para cada jugada, $T(s,a)$. Es la idea
de [[el-juego-como-grafo|El juego como grafo]]: el grafo es implícito.

## 2 · El procedimiento

**Piensa: para valorar n3 tuvimos que valorar antes n4, n6 y n13. ¿Cómo se
escribe eso en un programa?**

Con una función que se llama a sí misma sobre cada hijo:

```text
INPUT   un estado s y las reglas S_F, Pl, A, T y U de un juego
        finito, por turnos y sin azar. No recibe el grafo.
OUTPUT  V(s), el valor de s en puntos de MAX.

 1  function MINIMAX(s)
 2      if s ∈ S_F: return U(s)
 3      if Pl(s) = MAX
 4          v ← −∞
 5          for each a in A(s)                 ▷ genera los hijos
 6              v ← max(v, MINIMAX(T(s, a)))
 7          return v
 8      else                                   ▷ Pl(s) = MIN
 9          v ← +∞
10          for each a in A(s)
11              v ← min(v, MINIMAX(T(s, a)))
12          return v
```

Cada línea usa una pieza del modelo:

| Línea | Pieza | Qué hace |
|---|---|---|
| 2 | $S_F$ y $U$ | En un final, devuelve su utilidad |
| 3 y 8 | $\mathrm{Pl}$ | Decide si toma el máximo o el mínimo |
| 5 y 10 | $A$ | Recorre las jugadas permitidas |
| 6 y 11 | $T$ | Genera el hijo y lo valora |

$v$ es **el mejor valor visto hasta ahora** entre los hijos. Empieza en
$-\infty$, que es menor que cualquier utilidad, así que el primer hijo
siempre lo reemplaza; $+\infty$ hace lo mismo para MIN.

## 3 · De un número a una jugada

**Piensa: MINIMAX(n1) devuelve $+1$. ¿Con eso ya sabe Blancas qué
jugar?**

No: devuelve un número. Para jugar hace falta una segunda función, que
compara los hijos de la raíz y se queda con una jugada del
$\operatorname{arg\,max}$:

```text
INPUT   un estado s con Pl(s) = MAX, y las mismas reglas.
OUTPUT  una jugada a∗ de A(s) que alcanza V(s).

 1  function DECIDIR(s)
 2      return una jugada a de A(s) con el mayor MINIMAX(T(s, a))
```

En n1: $\mathrm{MINIMAX}(T(\text{n1},\text{c1}\textbf{-}\text{c2}))=+1$ y
$\mathrm{MINIMAX}(T(\text{n1},\text{c1}\textbf{x}\text{b2}))=-1$, así que
DECIDIR devuelve $\text{c1}\textbf{-}\text{c2}$. Si hay empate, cualquier
jugada del $\operatorname{arg\,max}$ sirve; ahí entra un desempate como el
de ganar rápido.

## 4 · Ver cómo genera mientras recorre

**Piensa: a media ejecución, ¿qué tiene minimax en memoria?**

MINIMAX baja por la primera jugada hasta un final, regresa, y solo entonces
prueba la siguiente. Es un recorrido **en profundidad**, y su orden de
visita es justo la numeración: n1, n2, n3, n4, … hasta n13.

La figura congela el momento en que empieza MINIMAX(n8):

::: figure {#jue-c2-genera title="MINIMAX a media ejecución"}
![El subgrafo de n1 cuando empieza MINIMAX(n8). Resaltado, el camino n1, n3, n6, n7, n8: cada nodo espera a sus hijos con el mejor valor visto hasta ahora; n1 y n3 ya tienen v = +1, n6 y n8 tienen −∞ y n7 +∞. n2, n4 y n5 aparecen como cajas punteadas: devolvieron +1 y se olvidaron. n9, n10, n11, n12 y n13 son cajas con signo de interrogación: todavía no existen](../_assets/jue-minimax-genera.svg)
:::

**Cómo leerla:**

- **El camino resaltado es todo lo que hay en memoria.** Cada nodo espera a
  que su hijo actual le devuelva un número.
- **n2, n4 y n5 ya devolvieron $+1$ y se olvidaron.** Su número quedó
  guardado en el $v$ de su padre; sus tableros ya no hacen falta.
- **n9 a n13 todavía no existen.** Se generarán cuando el recorrido llegue a
  ellos, con $A$ y $T$.

::: exercise {#jue-c2-ej-memoria title="Decide qué hay en memoria"}
Ahora empieza MINIMAX(n13), el último nodo que se visita.

1. ¿Qué nodos están en memoria, esperando?
2. ¿Qué $v$ tiene cada uno en ese momento?
3. ¿Cuáles ya se generaron y se olvidaron?
:::

::: hint {#jue-c2-pista-memoria of="jue-c2-ej-memoria" title="Sigue el camino"}
En memoria solo está el camino de n1 a n13. Para el $v$ de cada uno, mira
qué hijos suyos ya devolvieron su valor.
:::

::: answer {#jue-c2-resp-memoria of="jue-c2-ej-memoria"}
1. El camino: n1 y n3, más n13, que se acaba de generar.
2. En n1, $v=+1$: n2 ya devolvió $+1$. En n3, $v=\min\{+1,+1\}=+1$: n4 y n6
   ya devolvieron $+1$. Cuando n13 devuelva $-1$, n3 pasará a $v=-1$.
3. Todos los demás: n2, n4, n5, n6, n7, n8, n9, n10, n11 y n12. Se
   generaron, devolvieron su valor y se olvidaron.
:::

## 5 · Por qué es correcto

**Piensa: ¿cómo sabemos que el $+1$ es lo que Blancas asegura, y no solo
un número que salió de la cuenta?**

Llamamos **altura** de un nodo al número de jugadas de la continuación más
larga desde él hasta un final. Los finales tienen altura 0. Queremos
demostrar:

> MINIMAX($s$) es el valor que MAX puede asegurar desde $s$ si MIN responde
> siempre lo mejor que puede.

Se demuestra **por inducción sobre la altura**, desde los finales:

1. **Altura 0.** En un final no hay nada que decidir. La línea 2 devuelve
   $U(s)$, que es exactamente lo que vale.
2. **Altura mayor.** Todos los hijos tienen menor altura, así que su valor
   es correcto. Si mueve MAX, puede elegir cualquier hijo y asegura el mayor
   de esos valores; no puede asegurar más, porque después de su jugada MIN
   responde bien. Si mueve MIN, el argumento es el mismo con el menor.

Es la misma inducción hacia atrás del
[[opt-objetivo-juego-practica|ejemplo del juego]] de la unidad de
optimización, escrita como procedimiento.

::: exercise {#jue-c2-ej-induccion title="Decide dónde se usa que MIN juega bien"}
1. ¿En qué paso de la inducción se usa que MIN responde lo mejor que puede?
2. Si Negras se equivocara en n3 y jugara $\text{a3}\textbf{x}\text{b2}$,
   ¿Blancas obtendría más o menos que $V(\text{n3})=-1$?
:::

::: hint {#jue-c2-pista-induccion of="jue-c2-ej-induccion" title="Busca los dos lugares"}
Hay dos lugares en el paso de altura mayor: uno en los nodos de MIN y otro
en los de MAX. En los de MAX, fíjate en la frase que dice qué **no** puede
asegurar.
:::

::: answer {#jue-c2-resp-induccion of="jue-c2-ej-induccion"}
1. En el paso de **altura mayor**, en dos lugares. En un nodo de MIN, al
   decir que vale el **menor** de sus hijos. En uno de MAX, al decir que MAX
   no puede asegurar más que el mayor, porque después responde MIN.
2. **Más**: $+1$, el valor de n4. El valor es lo que MAX asegura contra
   cualquier respuesta; contra un rival que se equivoca puede obtener más,
   nunca menos.
:::

## 6 · Por qué termina

**Piensa: ¿podría MINIMAX llamarse a sí mismo para siempre?**

No en un juego **finito**, que es uno de los supuestos. En hexapawn cada
jugada avanza un peón y ningún peón retrocede, así que ninguna partida dura
para siempre: la más larga tiene 7 jugadas. Cada llamada baja un nivel, así
que ninguna cadena de llamadas pasa de 7, y cada nodo del árbol se visita
una sola vez.

## 7 · Cuánto cuesta

**Piensa: si un juego tiene el doble de jugadas por turno, ¿cuesta el doble
resolverlo?**

MINIMAX visita **cada nodo del árbol una vez**: 13 desde n1, 252 desde
$s_0$. Para un juego cualquiera usamos dos números:

- $b$, el **factor de ramificación**: el máximo de jugadas en un estado;
- $m$, la **profundidad máxima**: la partida más larga.

Con $b$ jugadas en cada nivel y $m$ niveles hay a lo más
$1+b+b^2+\cdots+b^m$ nodos.

::: remark {#jue-c2-costo-minimax title="Costo de minimax"}
Con recorrido en profundidad,

$$\text{tiempo}=O(b^m),\qquad \text{memoria}=O(bm).$$

El tiempo es exponencial en la profundidad: cada nivel multiplica el
trabajo por $b$. La memoria es pequeña: solo se guarda el camino actual, de
$m$ niveles, con las jugadas pendientes de cada uno, a lo más $b$ por
nivel. Es lo que muestra la figura de la sección 4.
:::

En hexapawn, $b=4$, aunque en promedio un estado no final tiene unas 2.3
jugadas, y $m=7$. La cota $1+4+\cdots+4^7=21\,845$ queda muy por encima de
los 252 nodos reales: es un techo, no un conteo. En juegos grandes la cota
sí describe bien el crecimiento.

## 8 · Recordar lo que ya se valoró

**Piensa: si el mismo estado aparece por dos caminos, ¿hace falta valorarlo
dos veces?**

En [[el-juego-como-grafo|El juego como grafo]] contamos 252 nodos en el
árbol de partidas y solo **135 estados distintos**: hay transposiciones. Si
MINIMAX guarda el valor de cada estado la primera vez que lo calcula, la
segunda vez solo lo consulta. Esa tabla se llama **tabla de
transposición**: el trabajo baja del árbol al grafo, de 252 nodos a 135
estados. El precio es memoria: un valor por estado, no solo el camino.

**Funciona porque $V(s)$ depende solo de $s$.** $S_F$, $\mathrm{Pl}$, $A$,
$T$ y $U$ leen únicamente el estado $(\tau,\text{turno})$, no el camino que
llevó a él. Si $U$ dependiera de cuántas jugadas van, dos caminos al mismo
tablero podrían valer distinto, y la tabla mezclaría valores ajenos.

::: table {#jue-c2-que-cambia-minimax title="Qué cambia cuando cambia el juego"}
| Cambio en el juego | Efecto en minimax |
|---|---|
| Más jugadas por turno (crece $b$) | Cada nivel multiplica más; el tiempo crece como $b^m$ |
| Partidas más largas (crece $m$) | Cada nivel extra multiplica el tiempo por $b$; la memoria solo crece en $b$ |
| Muchas transposiciones | Una tabla de transposición ahorra mucho, a cambio de memoria |
| Un final cambia de utilidad | Hay que recalcular sus antecesores; el costo no cambia |
:::

## 9 · Resolver un caso por tu cuenta

**Piensa: sin la página anterior abierta, ¿puedes escribir y valorar un
árbol desde cero?**

Llamemos **e1** a la posición que sale tras $\text{b1}\textbf{-}\text{b2}$,
$\text{c3}\textbf{x}\text{b2}$ y $\text{a1}\textbf{x}\text{b2}$. Mueve
**Negras**.

::: table {#jue-c2-e1 title="e1: mueven Negras"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | N | · |
| **2** | · | B | · |
| **1** | · | · | B |
:::

::: exercise {#jue-c2-ej-propio title="Resuelve el subárbol de e1"}
1. Escribe el árbol completo desde e1, con las jugadas en el orden fijo:
   por casilla de salida y, para cada peón, primero avanzar y después
   capturar. Numera los nodos e1, e2, … en el orden en que MINIMAX los
   visita. ¿Cuántos nodos tiene y cuántos son finales?
2. Pon su $U$ a cada final y sube hasta la raíz.
3. ¿Cuánto vale e1 y qué jugada elige Negras?
:::

::: hint {#jue-c2-pista-propio-a of="jue-c2-ej-propio" title="Pista 1 · Las jugadas de Negras"}
Empieza con $A(\text{e1})$. El peón de b3 tiene b2 ocupada enfrente y nada
que capturar. El de a3 puede avanzar o capturar.
:::

::: hint {#jue-c2-pista-propio-b of="jue-c2-ej-propio" title="Pista 2 · Las respuestas de Blancas"}
Tras $\text{a3}\textbf{-}\text{a2}$, el peón blanco de b2 queda bloqueado:
b3 está ocupada y no hay nada que capturar en a3 ni en c3. ¿Qué jugada le
queda a Blancas?
:::

::: answer {#jue-c2-resp-propio of="jue-c2-ej-propio"}
El árbol tiene **11 nodos**: 5 finales y 6 donde alguien decide.

- **e1 · Raíz** · mueve Negras (MIN)
  - **e2 · a3-a2** · mueve Blancas (MAX)
    - **e3 · c1-c2** · mueve Negras (MIN)
      - **e4 · a2-a1** · FINAL: Negras llega a la fila 1, $U=-1$
      - **e5 · b3xc2** · mueve Blancas (MAX)
        - **e6 · b2-b3** · FINAL: Blancas llega a la fila 3, $U=+1$
  - **e7 · a3xb2** · mueve Blancas (MAX)
    - **e8 · c1-c2** · mueve Negras (MIN)
      - **e9 · b2-b1** · FINAL: Negras llega, $U=-1$
      - **e10 · b3xc2** · FINAL: Negras captura todo, $U=-1$
    - **e11 · c1xb2** · FINAL: Negras sin jugada, $U=+1$

| Nodo | Mueve | Hijos y sus valores | Operación | $V$ |
|---|---|---|---|---:|
| e5 | Blancas (MAX) | e6 = +1 | único hijo | +1 |
| e3 | Negras (MIN) | e4 = −1, e5 = +1 | mínimo | −1 |
| e2 | Blancas (MAX) | e3 = −1 | único hijo | −1 |
| e8 | Negras (MIN) | e9 = −1, e10 = −1 | mínimo | −1 |
| e7 | Blancas (MAX) | e8 = −1, e11 = +1 | máximo | +1 |
| e1 | Negras (MIN) | e2 = −1, e7 = +1 | mínimo | **−1** |

e1 vale **$-1$**: gana Negras. Debe jugar **$\text{a3}\textbf{-}\text{a2}$**,
el avance. La captura $\text{a3}\textbf{x}\text{b2}$ parece atractiva, pero
Blancas responde $\text{c1}\textbf{x}\text{b2}$ y deja a Negras sin jugada.
:::

**Punto de control:** deberías poder escribir MINIMAX y DECIDIR de memoria,
decir qué recibe minimax y qué genera, decir en qué paso de la demostración
se usa que el rival juega bien y calcular la cota $O(b^m)$ de un juego dados
$b$ y $m$.

## Lo que hay que llevarse

- Minimax **recibe las reglas** ($S_F$, $\mathrm{Pl}$, $A$, $T$, $U$), **no
  el grafo**. Genera cada estado al expandir a su padre y lo olvida al
  terminar su rama.
- MINIMAX devuelve un número; DECIDIR elige la jugada del
  $\operatorname{arg\,max}$ en la raíz.
- Es correcto por inducción sobre la altura y termina porque el juego es
  finito.
- Cuesta $O(b^m)$ en tiempo y $O(bm)$ en memoria. Una tabla de
  transposición baja el trabajo del árbol al grafo, a cambio de memoria.

Continúa con [[cuando-decide-un-dado|cuando decide un dado]].
