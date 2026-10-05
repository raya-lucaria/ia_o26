---
id: minimax-como-algoritmo
title: Minimax como algoritmo
nav_title: Minimax como algoritmo
summary: "El cálculo a mano escrito como procedimiento general: pseudocódigo, por qué es correcto, por qué termina, cuánto cuesta en tiempo y memoria, y un subárbol nuevo para resolver por tu cuenta."
status: ready
estimated_time: 25m
tags: [juegos, minimax, algoritmos]
---

# Minimax como algoritmo

**¿Cómo se escribe lo que hicimos a mano para que sirva en cualquier juego
finito, y cuánto cuesta?**

Al terminar tendrás **el pseudocódigo de minimax**, la demostración de que
devuelve el valor correcto, su costo en tiempo y memoria, y **un subárbol
nuevo de hexapawn resuelto por tu cuenta**.

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la
> fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas. Un peón avanza
> una casilla si está vacía o captura en diagonal hacia delante. Gana quien
> llega a la fila del rival, captura todo o deja al rival sin jugada; gana
> $10-k$ puntos, donde $k$ es el número de jugadas de la partida, y el otro
> pierde esos mismos puntos.

En [[minimax|minimax a mano]] valoramos los 13 nodos del subárbol desde los
finales hacia n1, y obtuvimos $V=7$ con c1-c2. Esta página convierte ese recorrido
en un procedimiento que no depende de hexapawn.

## 1 · Nombrar las piezas

**Piensa: ¿qué tuviste que saber de cada nodo para valorarlo?**

Para cada nodo necesitamos saber si es final, a quién le toca, qué jugadas
hay y a dónde lleva cada una. Son las piezas del modelo de la clase 1, más
un número que vamos actualizando:

| Nombre | Qué guarda |
|---|---|
| $s$ | El estado que estamos valorando |
| $P(s)$ | A quién le toca en $s$: MAX o MIN |
| $A(s)$ | Las jugadas permitidas en $s$ |
| $T(s,a)$ | El estado al que lleva la jugada $a$ |
| $U(s)$ | La utilidad de un final, en puntos de MAX |
| $v$ | El mejor valor encontrado hasta ahora entre los hijos de $s$ |

La marca $-\infty$ es menor que cualquier utilidad: el primer hijo que se
revise siempre la reemplaza. $+\infty$ hace lo mismo para MIN.

## 2 · Escribir el procedimiento

**Piensa: para valorar n3 tuvimos que valorar antes n4, n6 y n13. ¿Cómo
se escribe eso en un programa?**

```text
INPUT   un estado s de un juego finito por turnos y sin azar,
        con P, A, T, los finales y U.
OUTPUT  V(s), el valor de s en puntos de MAX.

 1  function MINIMAX(s)
 2      if s es final: return U(s)
 3      if P(s) = MAX
 4          v ← −∞
 5          for each a in A(s)
 6              v ← max(v, MINIMAX(T(s, a)))
 7          return v
 8      else                              ▷ P(s) = MIN
 9          v ← +∞
10          for each a in A(s)
11              v ← min(v, MINIMAX(T(s, a)))
12          return v
```

La función se **llama a sí misma** en las líneas 6 y 11: para valorar un
estado, primero valora a cada hijo. Por eso el recorrido es **en
profundidad**: baja por la primera jugada hasta un final, regresa, y solo
entonces prueba la siguiente. En el subárbol, el orden de visita es n1, n2,
n3, n4, n5, n6, … hasta n13: el de la numeración.

MINIMAX devuelve un **número**, no una jugada. Para jugar, en la raíz se
calcula el valor de cada hijo y se elige una jugada del
$\operatorname{arg\,max}$, como hicimos con c1-c2.

## 3 · Demostrar que es correcto

**Piensa: ¿cómo sabemos que el 7 es lo que Blancas asegura, y no solo un
número que salió de la cuenta?**

Llamamos **altura** de un nodo al número de jugadas de la continuación más
larga desde él hasta un final. Los finales tienen altura 0. La propiedad que
queremos es:

> MINIMAX(s) es el valor que MAX puede asegurar desde $s$ si los dos juegan
> lo mejor posible.

Se demuestra **por inducción sobre la altura**, desde los finales:

1. **Altura 0.** En un final no hay nada que decidir; la línea 2 devuelve
   $U(s)$, que es exactamente lo que vale.
2. **Altura mayor.** Todos los hijos tienen menor altura, así que por la
   hipótesis su valor es correcto. Si le toca a MAX, puede elegir cualquier
   hijo y asegura el mayor de esos valores; no puede asegurar más, porque
   después de su jugada MIN juega bien. Si le toca a MIN, el razonamiento es
   el mismo con el menor.

Es la misma inducción hacia atrás de la unidad de optimización, escrita
como un procedimiento.

::: exercise {#jue-c2-ej-induccion title="Decide dónde se usa que MIN juega bien"}
¿En qué paso de la inducción se usa que MIN juega bien? Si Negras se
equivocara en n3 y jugara a3xb2, ¿Blancas obtendría más o menos que
$V(\text{n3})=-6$?
:::

::: answer {#jue-c2-resp-induccion of="jue-c2-ej-induccion"}
En el paso de **altura mayor**, en dos lugares: en un nodo MIN, al decir
que vale el **menor** de sus hijos; en un nodo MAX, al decir que MAX no
puede asegurar más que el mayor, porque después responde MIN. Si Negras
jugara a3xb2 en n3, Blancas obtendría 5, **más** que −6. El valor es lo que
MAX asegura contra cualquier respuesta; contra un rival que se equivoca
puede obtener más, nunca menos.
:::

## 4 · Comprobar que termina

**Piensa: ¿podría MINIMAX llamarse a sí mismo para siempre?**

No en hexapawn. El árbol es **finito**: cada jugada hace avanzar un peón
una fila y ningún peón retrocede, así que ninguna partida dura para
siempre; la más larga tiene 7 jugadas. Cada llamada baja un nivel, así que
ninguna cadena de llamadas pasa de 7 de profundidad. Cada nodo se visita
una sola vez, y hay un número finito de nodos.

## 5 · Contar el trabajo

**Piensa: si un juego tiene el doble de jugadas por turno, ¿cuesta el
doble calcularlo?**

MINIMAX visita **cada nodo una vez**. En el subárbol fueron 13; en el juego
completo, 252. Para un juego cualquiera usamos dos números:

- $b$, el **factor de ramificación**: el máximo de jugadas en un estado;
- $m$, la **profundidad máxima**: la partida más larga.

Con $b$ jugadas en cada nivel y $m$ niveles hay a lo más
$1+b+b^2+\cdots+b^m$ nodos.

::: remark {#jue-c2-costo-minimax title="Costo de minimax"}
Con recorrido en profundidad,

$$T_{\mathrm{minimax}}=O(b^m),\qquad \text{memoria}=O(bm).$$

El tiempo es exponencial en la profundidad: cada nivel multiplica el
trabajo por $b$. La memoria es pequeña: en cada momento solo se guarda el
camino actual, de $m$ niveles, y las jugadas pendientes de cada uno, a lo
más $b$ por nivel.
:::

En hexapawn, el máximo es $b=4$ y un estado no final tiene en promedio unas
2.3 jugadas; $m=7$. La cota $1+4+\cdots+4^7=21\,845$ (del orden de $4^7$)
queda muy por encima de los 252 nodos reales: es un techo, no un conteo.
En juegos grandes la cota sí describe bien el crecimiento.

## 6 · Recordar lo que ya se valoró

**Piensa: si el mismo tablero aparece por dos caminos, ¿hace falta
valorarlo dos veces?**

En [[escribir-el-juego|la clase 1]] contamos 252 nodos en el árbol y **135
estados distintos**: el mismo tablero aparece por varios caminos. Si
MINIMAX guarda el valor de cada estado la primera vez que lo calcula, la
segunda vez solo lo consulta. Esa tabla se llama **tabla de
transposición**, y con ella el trabajo baja del árbol al grafo: 135
estados en vez de 252 nodos. El precio es memoria: ahora se guarda un
valor por estado, no solo el camino actual.

::: table {#jue-c2-que-cambia-minimax title="Qué cambia cuando cambia el juego"}
| Cambio en el juego | Efecto en minimax |
|---|---|
| Más jugadas por turno (crece $b$) | Cada nivel multiplica más; el tiempo crece como $b^m$ |
| Partidas más largas (crece $m$) | Cada nivel extra multiplica el tiempo por $b$; la memoria solo crece en $b$ |
| Muchas transposiciones (mismo estado por varios caminos) | Una tabla de transposición ahorra mucho, a cambio de memoria |
| Un final cambia de utilidad | Hay que recalcular sus antecesores; el costo no cambia |
:::

## 7 · Resolver un caso por tu cuenta

**Piensa: sin la página anterior abierta, ¿puedes escribir y valorar un
árbol desde cero?**

Esta posición sale tras b1-b2, c3xb2 y a1xb2. Mueven **Negras** y ya se
hicieron $k=3$ jugadas.

::: exercise {#jue-c2-ej-propio title="Resuelve un subárbol de hexapawn"}
| | a | b | c |
|---|:---:|:---:|:---:|
| **3** | N | N | · |
| **2** | · | B | · |
| **1** | · | · | B |

1. Escribe el árbol completo desde esta posición, en el orden fijo de las
   jugadas. Numera los nodos e1, e2, … en el orden en que MINIMAX los
   visita. ¿Cuántos nodos tiene y cuántos son finales?
2. Valora cada final con $U=\pm(10-k)$ y sube hasta la raíz.
3. ¿Cuánto vale la posición y qué jugada elige Negras?
:::

::: answer {#jue-c2-resp-propio of="jue-c2-ej-propio"}
El árbol tiene **11 nodos**: 5 finales y 6 donde alguien decide.

- **e1 · Raíz** · mueven N, $k=3$
  - **e2 · a3-a2** · mueven B, $k=4$
    - **e3 · c1-c2** · mueven N, $k=5$
      - **e4 · a2-a1** · FINAL: Negras llega a la fila 1, $k=6$, $U=-4$
      - **e5 · b3xc2** · mueven B, $k=6$
        - **e6 · b2-b3** · FINAL: Blancas llega a la fila 3, $k=7$, $U=3$
  - **e7 · a3xb2** · mueven B, $k=4$
    - **e8 · c1-c2** · mueven N, $k=5$
      - **e9 · b2-b1** · FINAL: Negras llega, $k=6$, $U=-4$
      - **e10 · b3xc2** · FINAL: Negras captura todo, $k=6$, $U=-4$
    - **e11 · c1xb2** · FINAL: Negras sin jugada, $k=5$, $U=5$

En e2, el peón de b2 no puede moverse: b3 está ocupada y no hay nada que
capturar en a3 ni en c3. Por eso Blancas solo tiene c1-c2.

| Nodo | Turno | Hijos y sus valores | Operación | Valor |
|---|---|---|---|---:|
| e5 = a3-a2 → c1-c2 → b3xc2 | B (MAX) | e6 = 3 | único hijo | 3 |
| e3 = a3-a2 → c1-c2 | N (MIN) | e4 = −4, e5 = 3 | mínimo | −4 |
| e2 = a3-a2 | B (MAX) | e3 = −4 | único hijo | −4 |
| e8 = a3xb2 → c1-c2 | N (MIN) | e9 = −4, e10 = −4 | mínimo | −4 |
| e7 = a3xb2 | B (MAX) | e8 = −4, e11 = 5 | máximo | 5 |
| e1 = raíz | N (MIN) | e2 = −4, e7 = 5 | mínimo | **−4** |

La posición vale **−4**: gana Negras en la jugada 6. Negras debe jugar
**a3-a2**, el avance. La captura a3xb2 parece atractiva, pero Blancas
responde c1xb2 y deja a Negras sin jugada.
:::

**Punto de control:** deberías poder escribir el pseudocódigo de MINIMAX de
memoria, decir en qué paso de la demostración se usa que el rival juega bien y calcular el
costo $O(b^m)$ de un juego dados $b$ y $m$.

## Lo que hay que llevarse

- MINIMAX se llama a sí mismo sobre cada hijo y devuelve un número; la
  jugada se elige en la raíz con el $\operatorname{arg\,max}$.
- Es correcto por inducción sobre la altura, y termina porque el árbol es
  finito.
- Cuesta $O(b^m)$ en tiempo y $O(bm)$ en memoria; una tabla de
  transposición baja el trabajo del árbol al grafo a cambio de memoria.

Continúa con [[cuando-decide-un-dado|cuando decide un dado]].
