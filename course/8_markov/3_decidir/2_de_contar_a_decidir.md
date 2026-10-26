---
id: mkv-la-escalera
title: "De contar a decidir: la escalera"
nav_title: "La escalera"
summary: "Contar las rutas de una escalera y elegir la más barata con una pasada hacia atrás; por qué falla la codiciosa y qué rompe la pasada: un ciclo."
status: ready
estimated_time: 25m
tags: [markov, decidir, programacion-dinamica, algoritmo]
---

# De contar a decidir: la escalera

**Si en cada escalón eliges cuánto brincar, ¿cuál es la ruta más barata hasta arriba, y cómo se encuentra sin probarlas todas?**

Al terminar tendrás:

- **Dos cuentas hacia atrás.** Contarás las 8 rutas de una escalera y calcularás lo que falta pagar desde cada escalón.
- **El teorema y su condición.** Aplicarás @mkv-c3-teo-hacia-atras: si todo brinco sube, una pasada basta.
- **El algoritmo HACIA-ATRÁS.** Seguirás su pseudocódigo y su Python, y dirás cuánto cuesta.
- **Un contraejemplo.** Verás por qué elegir el escalón más barato de enfrente paga 5 y no 4.
- **El límite.** Dirás qué rompe la pasada: un ciclo, no el azar.

## Lo que traes

- **El máximo y el argmax.** En [[mkv-max-y-punto-fijo|Lo que necesitas: el máximo y el punto fijo]] viste el argmax con empates (@mkv-c3-def-argmax). Aquí se usa el mínimo, que es lo mismo con el signo cambiado.
- **Condicionar en el primer paso.** En [[mkv-absorcion|Cuánto falta para terminar]] el tiempo medio salió de mirar un solo paso (@mkv-c2-teo-primer-paso, @mkv-c2-teo-absorcion).
- **Minimax.** En [[minimax|Minimax a mano]] el valor de un nodo salió del de sus hijos, de abajo hacia arriba (@jue-c2-valor).

> [!NOTE]
> **Por qué empezamos sin azar.** La clase entera trata de decidir muchas veces seguidas. La idea central ya aparece en un problema sin probabilidades: calcular, desde cada lugar, cuánto falta, y decidir con esa cifra. Aquí se ve limpia; en la página siguiente le agregamos azar.

> **Dado:** una escalera de escalones 0 a 5. Estás en 0 y la meta es 5. Desde el escalón $s$ brincas 1 o 2, sin pasarte de 5. Pisar los escalones 1 a 5 cuesta 1, 2, 9, 1 y 1; el 3 está flojo y es caro.
>
> **Encontrar:** cuántas rutas hay de 0 a 5 y cuál cuesta menos.

::: figure {#mkv-c3-fig-escalera title="La escalera: lo que cuesta pisar, lo que falta y la ruta más barata"}
![Seis escalones, de 0 a 5, con la meta en 5. Debajo de cada escalón, lo que cuesta pisarlo: 1, 2, 9, 1 y 1 para los escalones 1 a 5; el 3 está marcado como flojo. Encima, lo que falta pagar desde cada escalón: 4, 4, 2, 1, 1 y 0. Resaltada, la ruta más barata 0 → 2 → 4 → 5, que cuesta 4](../_assets/mkv-c3-escalera.svg)
:::

---

## 1 · Contar las rutas desde arriba

**Piensa: si ya sabes cuántas rutas salen del escalón 3 y cuántas del 4, ¿cuántas salen del 2?**

Su suma. Desde 2 el primer brinco te deja en 3 o en 4, y desde ahí sigue cualquier ruta de ese escalón. Es condicionar en el primer paso, pero contando en lugar de promediar.

$$
\operatorname{rutas}(5)=1,\qquad
\operatorname{rutas}(s)=\sum_{a}\operatorname{rutas}(s+a),
$$

donde la suma va sobre los brincos $a\in\{1,2\}$ con $s+a\le5$.

- **Por qué 1 en la meta.** Desde 5 hay exactamente una ruta: quedarse. Si valiera 0, todo daría 0.
- **El orden.** Cada renglón usa escalones más altos, así que se llena de 5 hacia 0.

| Escalón s | rutas(s) | De dónde sale |
|---:|---:|---|
| 5 | 1 | la meta |
| 4 | 1 | solo cabe brincar 1 |
| 3 | 2 | rutas(4) + rutas(5) = 1 + 1 |
| 2 | 3 | rutas(3) + rutas(4) = 2 + 1 |
| 1 | 5 | rutas(2) + rutas(3) = 3 + 2 |
| 0 | 8 | rutas(1) + rutas(2) = 5 + 3 |

- **Respuesta.** Hay **8 rutas** de 0 a 5. Cada renglón es la suma de los dos de arriba, como en la sucesión de Fibonacci.

::: exercise {#mkv-c3-es-ej-pisan-3 title="Cuenta las rutas que pisan el 3"}
¿Cuántas de las 8 rutas pisan el escalón flojo?
:::

::: hint {#mkv-c3-es-pista-pisan-3 of="mkv-c3-es-ej-pisan-3" title="¿Cómo se parte una ruta que pasa por 3?"}
¿Cuántas maneras hay de llegar de 0 a 3, y cuántas de seguir de 3 a 5?
:::

::: answer {#mkv-c3-es-resp-pisan-3 of="mkv-c3-es-ej-pisan-3"}
De 0 a 3 hay 3 maneras (0→1→2→3, 0→1→3, 0→2→3) y de 3 a 5 hay ${\operatorname{rutas}(3)=2}$. Son ${3\cdot2=6}$ rutas. Solo 2 de las 8 lo evitan: 0→1→2→4→5 y 0→2→4→5.
:::

Contar ya funciona hacia atrás. Falta cambiar la suma por una elección.

---

## 2 · Elegir la más barata hacia atrás

**Piensa: si ya sabes cuánto falta pagar desde 3 y desde 4, ¿cuánto falta desde 2?**

Lo menor entre dos opciones: brincar a 3 y pagar 9 más lo que falta desde 3, o brincar a 4 y pagar 1 más lo que falta desde 4. La regla de contar se queda; la suma se vuelve mínimo.

Llamamos $\operatorname{costo}(s)$ a lo **mínimo que falta pagar** desde el escalón $s$ hasta la meta, y $\text{pisar}(s')$ a lo que cuesta pisar el escalón $s'$.

::: theorem {#mkv-c3-teo-hacia-atras title="Una pasada hacia atrás da el costo mínimo"}
Sea una escalera de escalones $0,\dots,n$ con meta $n$. Desde $s$ se brinca $a$ escalones, con $a$ en un conjunto finito de enteros positivos y ${s+a\le n}$. Pisar el escalón $s'$ cuesta $\text{pisar}(s')$, un número cualquiera.

**Condición.** Todo brinco sube: $a\ge1$. Así ningún escalón se puede volver a pisar.

Entonces, calculando de $n$ hacia 0,

$$
\begin{aligned}
\operatorname{costo}(n)&=0,\\
\operatorname{costo}(s)&=\min_{a}\bigl[\text{pisar}(s+a)+\operatorname{costo}(s+a)\bigr],
\end{aligned}
$$

es el menor costo de una ruta de $s$ a la meta. Seguir desde 0 un brinco que alcanza el mínimo en cada escalón da una ruta óptima.

**Lectura.** Pagas el escalón donde caes y, de ahí, lo mejor que se puede. El mínimo elige el brinco.

**Casos nulos.** En la meta no falta nada. Desde ${n-1}$ solo cabe brincar 1: ${\operatorname{costo}(n-1)=\text{pisar}(n)}$.
:::

::: proof {#mkv-c3-es-dem-hacia-atras of="mkv-c3-teo-hacia-atras"}
Por inducción, de $n$ hacia abajo. En $n$ la única ruta es quedarse y cuesta 0. Sea ${s<n}$ y supón cierto el teorema en todos los escalones arriba de $s$.

Una ruta desde $s$ empieza con un brinco $a$ y sigue con una ruta desde $s+a$. Esa cola cuesta al menos $\operatorname{costo}(s+a)$, así que la ruta cuesta al menos ${\text{pisar}(s+a)+\operatorname{costo}(s+a)}$, y al menos el mínimo sobre $a$. Ese mínimo se alcanza: brinca con el $a$ ganador y sigue la ruta óptima desde $s+a$.
:::

- **La condición sí importa.** Que todo brinco suba garantiza que los escalones de arriba ya están calculados cuando se piden. Sin eso, la sección 5 muestra qué pasa.
- **Ya lo habías visto.** En @mkv-c2-teo-absorcion, ${m(s)=1+\sum_{s'}P_{ss'}m(s')}$: un paso más lo que falta, promediado. Aquí no hay azar y sí hay elección: el promedio se vuelve mínimo.

**En el juguete.** De 5 hacia 0, con los costos de pisar 1, 2, 9, 1 y 1:

| Escalón s | Brinca 1 | Brinca 2 | costo(s) |
|---:|---|---|---:|
| 5 | — | — | 0 |
| 4 | 1 + 0 = 1 | no cabe | 1 |
| 3 | 1 + 1 = 2 | 1 + 0 = 1 | 1 |
| 2 | 9 + 1 = 10 | 1 + 1 = 2 | 2 |
| 1 | 2 + 2 = 4 | 9 + 1 = 10 | 4 |
| 0 | 1 + 4 = 5 | 2 + 2 = 4 | 4 |

- **Respuesta.** Lo mínimo es ${\operatorname{costo}(0)=4}$. El vector completo, de 0 a 5, es ${(4,4,2,1,1,0)}$.
- **La ruta.** El mínimo gana con brincar 2 en 0, brincar 2 en 2 y brincar 1 en 4: **0 → 2 → 4 → 5**, que paga ${2+1+1=4}$. Es la única, porque ningún renglón empata.
- **Qué guarda.** La tabla no solo da el número: guarda en cada escalón qué brinco gana. Esa columna es la decisión.

> [!WARNING]
> **Calcular hacia adelante.** Desde 0, el costo de un brinco depende de lo que falta *después*, que aún no conoces.
> **Se empieza por la meta: cada renglón solo pide escalones ya calculados.**

---

## 3 · Calcular con HACIA-ATRÁS

**Piensa: ¿qué necesita un programa para pasar de los costos de pisar a la ruta más barata?**

Una tabla de lo que falta, otra del brinco que gana, y recorrer los escalones de arriba hacia abajo. Esta forma de resolver, guardando la respuesta de cada subproblema para reusarla, se llama programación dinámica (*dynamic programming*).

### El mapa de HACIA-ATRÁS

- **Qué calcula:** $\operatorname{costo}(s)$ para cada escalón y un brinco ganador $\text{elige}(s)$, por @mkv-c3-teo-hacia-atras.
- **Qué guarda:** dos tablas indexadas por escalón, costo y elige; nada más.
- **Cómo avanza:** de ${n-1}$ a 0; en cada escalón prueba cada brinco que cabe y se queda con el menor.
- **Qué devuelve al terminar:** las dos tablas; seguir elige desde 0 da la ruta.

::: figure {#mkv-c3-fig-flujo-hacia-atras title="HACIA-ATRÁS, en palabras"}
![Diagrama de flujo de HACIA-ATRÁS, en palabras. 1: En la meta no falta nada: costo(n) = 0. 2: Toma el escalón de abajo siguiente, empezando por n − 1. 3: Para cada brinco que cabe, suma lo que cuesta pisar donde caes más lo que falta desde ahí. 4: Guarda el menor como costo(s) y su brinco como elige(s). 5, pregunta: ¿ya llegaste al escalón 0? Si no, vuelve al paso 2. Si sí, 6: devuelve costo y elige; sigue elige desde 0 para leer la ruta](../_assets/mkv-c3-flujo-hacia-atras.svg)
:::

```text
INPUT   n, la meta; pisar(s') para s' = 1..n;
        un conjunto finito de brincos ≥ 1.
OUTPUT  costo(s) y elige(s) para s = 0..n−1.

 1 function HACIA-ATRAS(pisar, n, brincos)
 2   costo(n) ← 0
 3   for s ← n − 1 down to 0
 4     mejor ← ∞
 5     for a in brincos con s + a ≤ n
 6       c ← pisar(s + a) + costo(s + a)
 7       if c < mejor: mejor ← c; elige(s) ← a
 8     costo(s) ← mejor
 9   return costo, elige
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. `rutas` es la cuenta de la sección 1; `seguir` lee la ruta.

```python
PISAR = {1: 1, 2: 2, 3: 9, 4: 1, 5: 1}
BRINCOS = (1, 2)

def rutas(n, brincos):
    cuenta = {n: 1}
    for s in range(n - 1, -1, -1):
        cuenta[s] = sum(cuenta[s + a] for a in brincos
                        if s + a <= n)
    return cuenta

def hacia_atras(pisar, n, brincos):     # (1)
    costo, elige = {n: 0}, {}           # (2)
    for s in range(n - 1, -1, -1):      # (3)
        mejor = float("inf")            # (4)
        for a in brincos:               # (5)
            if s + a > n:
                continue                # te pasarías
            c = pisar[s + a] + costo[s + a]   # (6)
            if c < mejor:               # (7)
                mejor, elige[s] = c, a
        costo[s] = mejor                # (8)
    return costo, elige                 # (9)

def seguir(elige, n):
    s, ruta = 0, [0]
    while s != n:
        s += elige[s]
        ruta.append(s)
    return ruta

print(rutas(5, BRINCOS))
# {5: 1, 4: 1, 3: 2, 2: 3, 1: 5, 0: 8}
costo, elige = hacia_atras(PISAR, 5, BRINCOS)
print(costo)
# {5: 0, 4: 1, 3: 1, 2: 2, 1: 4, 0: 4}
print(seguir(elige, 5))
# [0, 2, 4, 5]
```

**Cada pieza, en su línea:**

- **Línea 5.** El `continue` es el «con ${s+a\le n}$» del pseudocódigo: un brinco que se pasa no se considera.
- **Línea 7.** Con `<` estricto, en un empate se conserva el primer brinco probado. Cualquiera de los empatados es óptimo.
- **`seguir`.** Termina porque cada brinco sube: es la condición del teorema, otra vez.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina siempre, tras $n$ escalones. Cada escalón se calcula una sola vez.
- **Garantía:** por @mkv-c3-teo-hacia-atras, $\operatorname{costo}(0)$ es el menor costo entre todas las rutas, y seguir elige da una que lo alcanza.
- **Costo:** $n$ escalones por a lo más tantos brincos como haya: del orden de ${n\cdot\lvert\text{brincos}\rvert}$ sumas.
- **Supuestos:** todo brinco sube y los costos de pisar son fijos.

**Comprobación: probar las 8.** En una escalera chica se pueden listar todas las rutas y sumar. El mínimo tiene que coincidir con ${\operatorname{costo}(0)=4}$.

| Ruta | Lo que paga |
|---|---:|
| 0 → 1 → 2 → 3 → 4 → 5 | 1 + 2 + 9 + 1 + 1 = 14 |
| 0 → 1 → 2 → 3 → 5 | 1 + 2 + 9 + 1 = 13 |
| 0 → 1 → 2 → 4 → 5 | 1 + 2 + 1 + 1 = 5 |
| 0 → 1 → 3 → 4 → 5 | 1 + 9 + 1 + 1 = 12 |
| 0 → 1 → 3 → 5 | 1 + 9 + 1 = 11 |
| 0 → 2 → 3 → 4 → 5 | 2 + 9 + 1 + 1 = 13 |
| 0 → 2 → 3 → 5 | 2 + 9 + 1 = 12 |
| 0 → 2 → 4 → 5 | 2 + 1 + 1 = 4 |

- **Lectura.** El mínimo es 4 y lo logra solo 0 → 2 → 4 → 5, como dijo la pasada.

::: exercise {#mkv-c3-es-ej-dos-flojos title="Dos escalones caros"}
Ahora el escalón 4 también está flojo y pisarlo cuesta 9. Los demás siguen igual. Calcula la tabla de $\operatorname{costo}$ y la ruta más barata.
:::

::: hint {#mkv-c3-es-pista-dos-flojos of="mkv-c3-es-ej-dos-flojos" title="¿Qué escalones cambian?"}
¿Cambia $\operatorname{costo}(4)$, que no pisa el 4? ¿Desde qué escalón empieza a importar el nuevo costo?
:::

::: answer {#mkv-c3-es-resp-dos-flojos of="mkv-c3-es-ej-dos-flojos"}
De 5 hacia 0: ${\operatorname{costo}(4)=1}$ y ${\operatorname{costo}(3)=1}$ no cambian, porque desde ahí no se pisa el 4. Luego ${\operatorname{costo}(2)=\min(9+1,\ 9+1)=10}$, ${\operatorname{costo}(1)=\min(2+10,\ 9+1)=10}$ y ${\operatorname{costo}(0)=\min(1+10,\ 2+10)=11}$. La ruta es 0 → 1 → 3 → 5, que paga ${1+9+1=11}$: un escalón caro ya es inevitable, y conviene pisar uno solo.
:::

Con la tabla en la mano, vale preguntar si había un atajo más simple.

---

## 4 · Ver por qué no basta lo más barato de enfrente

**Piensa: ¿y si en cada escalón brincas al más barato de los que alcanzas?**

Pagas 5, no 4. Esa regla, que mira solo el siguiente escalón, se llama **codiciosa**:

- **En 0.** El 1 cuesta 1 y el 2 cuesta 2: va al 1.
- **En 1.** El 2 cuesta 2 y el 3 cuesta 9: va al 2.
- **En 2.** El 3 cuesta 9 y el 4 cuesta 1: va al 4, y de ahí a 5.

La ruta 0 → 1 → 2 → 4 → 5 paga ${1+2+1+1=5}$. Ahorró 1 en el primer brinco y lo perdió al tener que pisar el 2 para esquivar el 3. La pasada hacia atrás no se equivoca porque cada brinco se juzga con $\operatorname{costo}$, lo que viene **después** incluido.

**Por qué no probar todas.** Las 8 rutas comparten tramos: la cola 4 → 5 aparece en cinco de ellas. Listarlas recalcula esos tramos cada vez; la pasada calcula cada uno de los 6 escalones **una vez**.

Con más escalones la diferencia crece: cada $\operatorname{rutas}(s)$ es la suma de las dos de arriba, y eso crece como Fibonacci, casi multiplicándose por 1.6 con cada escalón nuevo. Los escalones solo crecen de uno en uno.

::: figure {#mkv-c3-fig-escalera-arbol-vs-grafo title="Las rutas como árbol y como escalera"}
![A la izquierda, el árbol de todas las rutas desde el escalón 0: cada nodo es un escalón y cada rama un brinco de 1 o de 2; tiene 8 hojas, una por ruta, y los escalones 2, 3 y 4 aparecen repetidos en varias ramas. A la derecha, la misma escalera como grafo: 6 nodos, del 0 al 5, con flechas de cada escalón a los que alcanza; cada nodo aparece una sola vez](../_assets/mkv-c3-escalera-arbol-vs-grafo.svg)
:::

**Es minimax sin rival.** En @jue-c2-valor, el valor de un nodo salía del de sus hijos, de abajo hacia arriba, con máximo y mínimo alternados. En la escalera mueve siempre el mismo jugador, que minimiza lo que paga. Y en lugar de un árbol hay un grafo: el escalón 4 se alcanza desde 2 y desde 3, pero se calcula una vez.

---

## 5 · Romper la pasada con un resbalón

**Piensa: ¿qué pasa si un brinco puede fallar y dejarte donde estabas?**

Que $\operatorname{costo}(s)$ depende de sí mismo, y la pasada ya no tiene por dónde empezar. Supón que el escalón 3, además de caro, resbala: desde ahí, cualquier brinco sale bien con probabilidad $1/2$ y con $1/2$ te deja en 3.

- **La ecuación de 3.** Condicionando en el primer paso, como en @mkv-c2-teo-primer-paso, con probabilidad $1/2$ estás de nuevo en 3 y falta otra vez $\operatorname{costo}(3)$. Ese término aparece **a los dos lados** del igual.
- **Lo que se rompe.** La pasada pide en cada renglón solo escalones ya calculados. El renglón de 3 se pide a sí mismo: hay un **ciclo** de 3 a 3, y la condición de @mkv-c3-teo-hacia-atras deja de cumplirse.

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** la escalera de esta página. Todo brinco sube, el grafo no tiene ciclos y una pasada de 5 a 0 basta.
> - **No lo cumple:** la misma escalera con resbalón $1/2$ en el escalón 3. Hay un lazo de 3 a sí mismo y $\operatorname{costo}(3)$ depende de $\operatorname{costo}(3)$.

::: figure {#mkv-c3-fig-ej-hacia-atras title="Lo que necesita la pasada hacia atrás: que nada regrese"}
![Dos escaleras, cada una como grafo con nodos de acción y una matriz por acción debajo. Arriba, la que cumple: escalones 0 a 5, cada brinco de 1 o de 2 sube con probabilidad 1; el grafo no tiene ciclos y una pasada basta. Abajo, la que no: en el escalón 3 cada brinco sube con 1/2 y con 1/2 regresa a 3; el lazo hace que costo(3) dependa de sí mismo](../_assets/mkv-c3-ej-hacia-atras.svg)
:::

- **No es el azar.** Si el brinco desde 3 te mandara con $1/2$ a 4 y con $1/2$ a 5, habría azar sin ciclo. La pasada seguiría funcionando con un promedio dentro del mínimo, como en @mkv-c2-teo-absorcion. **Lo que rompe la pasada hacia atrás es el ciclo, no el azar.**

Con un ciclo, el costo de un escalón queda definido por una ecuación que lo contiene. Eso pide un objeto nuevo: estados, acciones, una matriz por acción y lo que cuesta cada una.

Aplica la pasada a una escalera con otra regla de brinco.

---

## Ejercicios

::: exercise {#mkv-c3-es-ej-brinco-3 title="Permite brincar 3"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

La misma escalera de 0 a 5, con los mismos costos de pisar: 1, 2, 9, 1 y 1. **Cambia una idea:** ahora desde cada escalón puedes brincar 1, 2 o 3, sin pasarte de 5.

1. **Cuenta.** Escribe la regla de $\operatorname{rutas}(s)$ y llena su tabla. ¿Cuántas rutas hay de 0 a 5?
2. **Revisa la condición.** ¿Sigue cumpliéndose la condición de @mkv-c3-teo-hacia-atras?
3. **Pasada hacia atrás.** Llena la tabla de $\operatorname{costo}$ con una columna por brinco. ¿Cuánto vale $\operatorname{costo}(0)$?
4. **Las rutas óptimas.** ¿Cuántas rutas alcanzan el mínimo? ¿Cuál devuelve el Python de la sección 3, y por qué esa?
5. **La codiciosa.** Sigue la regla de la sección 4 con los tres brincos. ¿Acierta ahora? ¿Prueba eso que la regla es correcta?
:::

::: hint {#mkv-c3-es-pista-brinco-3-1 of="mkv-c3-es-ej-brinco-3" title="Pista 1 · ¿Cuántos términos lleva cada renglón?"}
¿Qué brincos caben desde 3, desde 4 y desde los escalones de abajo? ¿Cada renglón suma o minimiza sobre cuántos escalones de arriba?
:::

::: hint {#mkv-c3-es-pista-brinco-3-2 of="mkv-c3-es-ej-brinco-3" title="Pista 2 · ¿Tus números tienen sentido?"}
¿Hay ahora más rutas que 8? ¿Puede $\operatorname{costo}(0)$ ser mayor que 4, si las rutas viejas siguen disponibles? ¿Qué hace la línea 7 cuando dos brincos empatan?
:::

::: answer {#mkv-c3-es-resp-brinco-3 of="mkv-c3-es-ej-brinco-3" title="Respuesta · La escalera con brinco de 3"}
**1. Rutas.** ${\operatorname{rutas}(5)=1}$ y ${\operatorname{rutas}(s)}$ suma los de ${s+1}$, ${s+2}$ y ${s+3}$ que no pasen de 5. De 5 a 0: 1, 1, 2, 4, 7 y **13**.

**2. Condición.** Sí: los tres brincos suben, así que ningún escalón se vuelve a pisar.

**3. Costo.** De 5 hacia 0, con las opciones brinca 1 · brinca 2 · brinca 3:

- **Escalón 4:** ${1+0}$; los demás no caben. ${\operatorname{costo}(4)=1}$.
- **Escalón 3:** ${1+1}$ · ${1+0}$. ${\operatorname{costo}(3)=1}$.
- **Escalón 2:** ${9+1}$ · ${1+1}$ · ${1+0}$. ${\operatorname{costo}(2)=1}$.
- **Escalón 1:** ${2+1}$ · ${9+1}$ · ${1+1}$. ${\operatorname{costo}(1)=2}$.
- **Escalón 0:** ${1+2}$ · ${2+1}$ · ${9+1}$. ${\operatorname{costo}(0)=3}$.

**4. Empate.** En 0, brincar 1 y brincar 2 dan 3. Hay dos rutas óptimas: 0 → 1 → 4 → 5 y 0 → 2 → 5, las dos pagan 3. El Python devuelve la primera, porque con `<` estricto la línea 7 conserva el primer brinco probado. El argmax es un conjunto con dos brincos (@mkv-c3-def-argmax).

**5. Codiciosa.** En 0 va al 1 (cuesta 1); en 1 elige entre 2, 9 y 1 y va al 4; de ahí a 5. Paga ${1+1+1=3}$: acierta. Pero un caso donde acierta no prueba nada; la escalera original es un contraejemplo y basta uno.
:::

**Punto de control:** deberías poder contar rutas y calcular lo que falta pagar con una pasada hacia atrás. También, decir por qué la pasada necesita que ningún brinco regrese, y mostrar con un ejemplo que elegir lo más barato de enfrente puede fallar.

---

## Lo que hay que llevarse

- **Contar.** ${\operatorname{rutas}(s)=\sum_a\operatorname{rutas}(s+a)}$ con ${\operatorname{rutas}(5)=1}$: la escalera tiene **8 rutas**.
- **Decidir.** ${\operatorname{costo}(s)=\min_a[\text{pisar}(s+a)+\operatorname{costo}(s+a)]}$ con ${\operatorname{costo}(5)=0}$ da ${(4,4,2,1,1,0)}$ y la ruta 0 → 2 → 4 → 5, que paga 4 (@mkv-c3-teo-hacia-atras).
- **El algoritmo.** HACIA-ATRÁS calcula cada escalón una vez: del orden de ${n\cdot\lvert\text{brincos}\rvert}$ sumas, contra un número de rutas que crece como Fibonacci.
- **La codiciosa falla.** Brincar al más barato de enfrente paga 5: no ve lo que viene después.
- **El límite.** La pasada pide que todo brinco suba. Un resbalón que te deja donde estabas crea un ciclo: lo que la rompe es el ciclo, no el azar.

¿Y si un brinco puede fallar y dejarte donde estabas? Continúa con [[mkv-el-mdp|El proceso de decisión de Markov]].
