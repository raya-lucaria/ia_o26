---
id: minimax-con-corte
title: Minimax con corte como algoritmo
nav_title: Minimax con corte
summary: "El cálculo a mano escrito como procedimiento: qué recibe, qué genera, por qué termina, qué se puede afirmar de lo que devuelve, cuánto cuesta y qué preferencia expresa la evaluación."
status: ready
estimated_time: 20m
tags: [juegos, busqueda-adversarial, evaluacion, algoritmos]
---

# Minimax con corte como algoritmo

**¿Cómo se escribe lo que hicimos a mano para cualquier juego, y qué se
puede confiar en lo que devuelve?**

Al terminar tendrás **el pseudocódigo de minimax con corte**, sabrás qué
recibe y qué genera, qué garantiza y qué no, y cuánto cuesta. También
sabrás leer qué preferencia expresa una función de evaluación.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Empiezan Blancas. Un peón avanza una casilla si está vacía o
> captura en diagonal hacia delante. Gana quien llega a la fila del rival,
> captura todo o deja al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$
> si gana Negras.

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: dos jugadores por turnos,
> sin azar, todo a la vista, toda partida termina, suma cero, y no alcanza
> el tiempo para llegar a los finales.

## 1 · Qué recibe y qué genera

**Piensa: ¿qué tuviste que saber para calcular la tabla de profundidades a
mano?**

Las reglas, como en la clase 2, y dos cosas nuevas: cuánto mirar y cómo
juzgar una posición sin terminar.

> **El problema de minimax con corte.**
>
> **Dado (lo que recibe):**
>
> - un estado $s$;
> - $d$, la profundidad que queda: cuántas jugadas más puede mirar;
> - las reglas del juego: $S_F$ (@jue-c1-finales), $\mathrm{Pl}$
>   (@jue-c1-pl), $A$ (@jue-c1-acciones), $T$ (@jue-c1-transicion) y $U$
>   (@jue-c1-utilidad);
> - una función de evaluación, $\mathrm{EVAL}$ (@jue-c3-evaluacion).
>
> **Encontrar (lo que devuelve):** el valor con corte de $s$
> (@jue-c3-valor-con-corte), en puntos de MAX.

**Qué genera:** como minimax, no recibe el grafo. Genera los estados con
$A$ y $T$ mientras recorre, pero **solo hasta $d$ jugadas**. Los nodos de
corte sí se generan, porque hay que evaluarlos, pero no se expanden: nadie
calcula sus hijos.

## 2 · El procedimiento

**Piensa: ¿qué línea hay que agregarle a MINIMAX para que se detenga?**

Una sola.

```text
INPUT   un estado s; la profundidad que queda, d ≥ 0; las reglas
        S_F, Pl, A, T y U; y una función EVAL. No recibe el grafo.
OUTPUT  el valor con corte de s, en puntos de MAX.

 1  function MINIMAX-CON-CORTE(s, d)
        ▷ Un final vale su utilidad, en otra escala:
        ▷ 100 pesa más que cualquier estimación.
 2      if s ∈ S_F: return 100 · U(s)
        ▷ Ya no quedan jugadas por mirar: se estima.
 3      if d = 0: return EVAL(s)      ▷ nodo de corte
        ▷ De aquí abajo, MINIMAX con d − 1 en cada hijo.
 4      if Pl(s) = MAX
 5          v ← −∞                    ▷ menor que todo
 6          for each a in A(s)        ▷ genera los hijos
                ▷ al hijo le queda una jugada menos
 7              v ← max(v, MINIMAX-CON-CORTE(T(s, a), d − 1))
 8          return v                  ▷ lo mejor para MAX
 9      else                          ▷ Pl(s) = MIN
10          v ← +∞                    ▷ mayor que todo
11          for each a in A(s)        ▷ genera los hijos
                ▷ al hijo le queda una jugada menos
12              v ← min(v, MINIMAX-CON-CORTE(T(s, a), d − 1))
13          return v                  ▷ lo mejor para MIN
```

El mismo procedimiento en Python, línea por línea; el número entre
paréntesis es la línea del pseudocódigo:

```python
from math import inf

# Las reglas: es_final(s), pl(s), acciones(s),
# transicion(s, a), utilidad(s) y evaluar(s), que es EVAL.
# pl(s) da "MAX" o "MIN".

def minimax_con_corte(s, d):          # (1)
    # (2) Un final vale 100 veces su utilidad.
    if es_final(s):
        return 100 * utilidad(s)
    # (3) Nodo de corte: no se expande, se estima.
    if d == 0:
        return evaluar(s)
    if pl(s) == "MAX":                # (4) mueve MAX
        v = -inf                      # (5) menor que todo
        for a in acciones(s):         # (6) genera los hijos
            # (7) valora el hijo con una jugada menos
            h = minimax_con_corte(transicion(s, a), d - 1)
            v = max(v, h)
        return v                      # (8) lo mejor para MAX
    else:                             # (9) mueve MIN
        v = inf                       # (10) mayor que todo
        for a in acciones(s):         # (11) genera los hijos
            # (12) valora el hijo con una jugada menos
            h = minimax_con_corte(transicion(s, a), d - 1)
            v = min(v, h)
        return v                      # (13) lo mejor para MIN
```

Respecto del MINIMAX de [[minimax-como-algoritmo|la clase 2]]:

- **La línea 3 es la nueva:** cuando ya no quedan jugadas por mirar, se
  estima.
- **La línea 2 solo cambia la escala** de $U$, para que un final pese más
  que cualquier estimación.
- **Las demás son las mismas**, con $d-1$ en cada llamada.

Para **elegir la jugada** en la raíz se hace lo de DECIDIR: se llama con
$d-1$ a cada hijo y se toma una jugada del $\operatorname{arg\,max}$. Con
$d=1$, $d=2$ y $d=3$ en la raíz salen las tres primeras columnas de la
tabla de [[cortar-y-evaluar|la página anterior]].

::: exercise {#jue-c3-ej-hoja title="Decide qué devuelve cada línea"}
1. Con $d=2$ en la raíz, la llamada para $\text{d2}\textbf{x}\text{c3}$
   baja a la respuesta $\text{b4}\textbf{x}\text{c3}$, y ahí queda $d=0$.
   ¿Qué línea devuelve el valor de ese estado, y cuánto?
2. Con $d=3$ en la raíz, la llamada para $\text{d2}\textbf{-}\text{d3}$
   baja por $\text{a4}\textbf{-}\text{a3}$ y $\text{d3}\textbf{-}\text{d4}$.
   ¿Qué línea devuelve el valor de ese estado, y cuánto?
:::

::: hint {#jue-c3-pista-hoja of="jue-c3-ej-hoja" title="El orden de las líneas importa"}
La línea 2 se revisa antes que la 3. Pregúntate primero si el estado es
final; solo si no lo es, mira cuánto vale $d$.
:::

::: answer {#jue-c3-resp-hoja of="jue-c3-ej-hoja"}
1. El estado tras $\text{b4}\textbf{x}\text{c3}$ no es final, así que la
   línea 2 no lo toma. Como $d=0$, lo toma la **línea 3**: devuelve
   $\mathrm{EVAL}=0$.
2. Blancas llegó a la fila 4: es final. La **línea 2** devuelve
   $100\cdot(+1)=100$, sin importar cuánto valga $d$.
:::

## 3 · Por qué termina

**Piensa: si el juego fuera infinito, ¿terminaría MINIMAX-CON-CORTE?**

Sí. Cada llamada baja $d$ en uno, y la línea 3 no hace más llamadas cuando
$d=0$. El algoritmo **nunca baja más de $d$ niveles**, así que termina
aunque el árbol completo fuera enorme o infinito. A diferencia de minimax,
que termine no depende de que el juego termine.

## 4 · Qué se puede afirmar de lo que devuelve

**Piensa: el algoritmo hace un minimax exacto. ¿Por qué entonces no da el
valor del juego?**

Porque lo hace **sobre otro árbol**: el árbol cortado a $d$ jugadas, con las
hojas valoradas por las líneas 2 y 3. Con el mismo argumento de inducción
que minimax, el resultado es el minimax exacto de ese árbol. Si una hoja de
corte está mal estimada, el error sube por el árbol.

Hay una afirmación que sí vale en este juego. Como $|\mathrm{EVAL}|\le36$ en
las posiciones alcanzables que no son finales, **un 100 solo puede venir de
finales ganados**: si la búsqueda devuelve 100, Blancas tiene una victoria
asegurada dentro de las $d$ jugadas, responda lo que responda Negras. Lo
mismo vale para $-100$ y Negras. **Cualquier otro número es una
estimación.**

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

En la posición de la clase, minimax con corte genera **4 nodos** con $d=1$,
**12** con $d=2$ y **33** con $d=3$, contando la raíz. Cada nivel multiplica
el trabajo, aunque aquí por menos de $b=5$, el máximo de jugadas en este
árbol: varios estados tienen pocas jugadas o son finales.

Por eso $d$ se elige según el **tiempo disponible**, no según el juego: es
el tema de [[jugar-contra-el-reloj|Jugar contra el reloj]].

## 6 · Leer qué preferencia expresa la evaluación

**Piensa: ¿qué dice la suma $10\cdot\text{material}+\text{avance}$ sobre
lo que importa?**

$\mathrm{EVAL}$ no viene del reglamento: **la escribimos nosotros**. Es una
decisión de modelado, igual que la medida de comodidad del
[[opt-objetivo-salones-practica|ejemplo de los salones]] en la unidad de
optimización: los pesos dicen cuánto importa cada rasgo. Ésta, leída con
cuidado:

- **Un peón vale lo mismo que diez filas de avance.** En las posiciones
  alcanzables del 4×4 que no son finales, la computadora comprobó que la
  diferencia de avance entre dos posiciones nunca compensa un peón, así que
  **el material decide primero** y el avance solo desempata.
- **Todos los peones valen igual**, estén donde estén, salvo por su avance.
- **No ve si un peón está bloqueado**, ni si está a punto de ser capturado.
- **No sabe a quién le toca.** La misma posición recibe el mismo número
  mueva quien mueva.

Ninguna de esas omisiones es un error de cuenta. Son **supuestos** del
modelo, y conviene escribirlos como tales.

En ajedrez, la evaluación más conocida es la del **material**: peón 1,
caballo 3, alfil 3, torre 5 y dama 9. Es la misma idea, una suma ponderada
de rasgos, con los mismos huecos.

::: exercise {#jue-c3-ej-rasgo title="Decide si un rasgo nuevo arregla el error"}
A profundidad 1, la evaluación prefirió $\text{d2}\textbf{x}\text{c3}$
(13) sobre $\text{a1}\textbf{-}\text{a2}$ y $\text{d2}\textbf{-}\text{d3}$
(2 cada una), sin ver que Negras recupera el peón.

1. ¿Cuál de los supuestos de la lista explica ese error?
2. Una compañera propone agregar un rasgo: restar 10 por cada captura que
   Negras tiene disponible y sumar 10 por cada captura que tiene Blancas.
   Calcula la nueva evaluación tras cada una de las tres jugadas. ¿Cambia la
   elección?
3. Otro compañero propone contar solo las capturas de **quien mueve**, que
   tras la jugada de Blancas es Negras: restar 10 por cada una. Calcula otra
   vez. ¿Cambia la elección?
:::

::: hint {#jue-c3-pista-rasgo of="jue-c3-ej-rasgo" title="Cuenta las diagonales"}
Tras cada jugada, revisa qué peones negros tienen un peón blanco en una
diagonal de enfrente (hacia abajo), y qué peones blancos tienen uno negro
(hacia arriba). Tras la captura, mira también lo que amenaza el peón que
llegó a c3.
:::

::: answer {#jue-c3-resp-rasgo of="jue-c3-ej-rasgo"}
1. **«No ve si un peón está a punto de ser capturado».**
2. Tras $\text{a1}\textbf{-}\text{a2}$, Negras puede capturar en d2 y
   Blancas en c3: $2-10+10=2$. Tras $\text{d2}\textbf{-}\text{d3}$, nadie
   puede capturar: 2. Tras $\text{d2}\textbf{x}\text{c3}$, Negras puede
   capturar en c3, pero el peón de c3 también amenaza a b4: $13-10+10=13$.
   **No cambia nada**: las dos amenazas se cancelan, porque el rasgo no
   sabe a quién le toca.
3. Contando solo las de Negras: $2-10=-8$, $2$ y $13-10=3$. **Sigue
   eligiendo la captura**, por poco: tras la recaptura también cambia el
   avance, y el rasgo no lo ve.

Adivinar las capturas con rasgos es frágil: cada arreglo deja otro hueco.
La [[jugar-contra-el-reloj|página siguiente]] hace otra cosa, **mirarlas**:
la búsqueda de quietud.
:::

::: table {#jue-c3-que-cambia title="Qué cambia cuando cambia la búsqueda"}
| Cambio | Efecto que se puede justificar |
|---|---|
| Subir $d$ en uno | Multiplica las hojas por hasta $b$. La decisión puede cambiar en cualquier sentido |
| Una $\mathrm{EVAL}$ con más rasgos | Las mismas hojas, pero cada una cuesta más. Si se acerca al valor exacto, ayuda; nada lo asegura |
| Peor orden de jugadas, con alfa-beta | El mismo valor en la raíz, pero menos cortes |
:::

**Punto de control:** deberías poder escribir MINIMAX-CON-CORTE de memoria,
decir qué recibe y qué genera, explicar por qué termina aunque el juego no
termine y decir qué número de su salida es seguro.

## Lo que hay que llevarse

- Minimax con corte recibe las reglas, $d$ y $\mathrm{EVAL}$. Genera los
  estados solo hasta $d$ jugadas y evalúa los nodos de corte sin
  expandirlos.
- Es minimax con una línea más, la 3. Termina siempre, porque $d$ baja en
  cada llamada.
- Devuelve el minimax exacto del árbol cortado, no el del juego: solo los
  $\pm100$ son seguros. Cuesta $O(b^d)$.
- $\mathrm{EVAL}$ es un modelo: sus pesos expresan una preferencia y dejan
  cosas fuera.

Continúa con [[jugar-contra-el-reloj|jugar contra el reloj]].
