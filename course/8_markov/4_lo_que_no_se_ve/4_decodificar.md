---
id: mkv-decodificar
title: "Decodificar: Viterbi y suavizar"
nav_title: "Decodificar"
summary: "La secuencia de estados más probable con Viterbi, el suavizado y por qué el mejor estado de cada día no da la mejor secuencia."
status: ready
estimated_time: 28m
tags: [markov, ocultas, viterbi, suavizar]
---

# Decodificar: Viterbi y suavizar

**Si ya viste todas las señales, ¿cuál es la secuencia de climas más probable?**

Al terminar tendrás:

- **El suavizado:** la probabilidad de cada estado por día, dadas todas las señales. Usaremos las tablas hacia adelante y hacia atrás.
- **El algoritmo VITERBI:** recurrencia, pseudocódigo y versión en Python. También lo seguiremos a mano con el paraguas.
- **Un teorema con su condición:** Viterbi devuelve la trayectoria de mayor probabilidad conjunta si esa probabilidad es positiva.
- **Un contraste con cifras:** elegir el mejor estado diario no garantiza la mejor secuencia. Con sin paraguas, paraguas, sin paraguas, obtenemos $0.332$ frente a $0.402$.

## Lo que traes

- **El modelo.** En [[mkv-el-modelo-oculto|El modelo oculto]] viste $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ (@mkv-c4-def-hmm), el diccionario `paraguas` y la conjunta como producto (@mkv-c4-obs-conjunta). Falta responder «¿cuál fue la secuencia de estados?».
- **Filtrar.** En [[mkv-filtrar|Filtrar y predecir]] calculaste la creencia $b_t(s)=\Pr(S_t=s\mid O_{0:t})$ día por día. Usaste las señales hasta hoy.
- **Normalizar.** En [[mkv-bayes-y-normalizar|Bayes y normalizar]] dividiste los pesos entre su suma, siempre que fuera positiva.
- **Máximo sobre una recurrencia.** En [[mkv-iterar-valores|Iteración de valores]] elegiste el mejor candidato y guardaste solo ese. Viterbi lo hace con caminos.
- **Qué $b$ usamos aquí.** El filtro $b_t$ sirve para comparar. El suavizado $b_{t\mid T}$ usa todas las señales. No hay $V$ porque nadie decide.

---

## 1 · Plantear el problema

**Piensa: con dos climas posibles, ¿cuántas secuencias de una semana pudieron producir las señales que viste?**

Hay $2^7=128$ secuencias, una por cada combinación de climas en los siete días. Con $\lvert\mathcal S\rvert$ estados y $T+1$ días hay $\lvert\mathcal S\rvert^{T+1}$ secuencias. Revisarlas todas resulta impráctico.

> **Dado:** un modelo oculto $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ y las señales observadas $o_0,\dots,o_T$.
>
> **Encontrar:** la trayectoria $s_0,\dots,s_T$ con mayor probabilidad conjunta $\Pr(S_{0:T}=s_{0:T},\ O_{0:T}=o_{0:T})$.

- **Conjunta o posterior, gana la misma.** La posterior de una trayectoria es su conjunta dividida entre $\Pr(O_{0:T}=o_{0:T})$. Todas tienen el mismo divisor, así que gana la misma trayectoria.
- **Ya sabes calcular la conjunta.** Usa el producto de @mkv-c4-obs-conjunta: $\mu_0$, seguido de un factor de $P$ y uno de $B$ por día.

**En el paraguas, por fuerza bruta.** Tomamos tres días: sin paraguas, paraguas, sin paraguas. Hay $2^3=8$ trayectorias. Python las enumera con el diccionario de la página 2:

```python
from fractions import Fraction as F
from itertools import product

paraguas = {
    "estados": ["lluvia", "sol"],              # 𝒮
    "señales": ["paraguas", "sin paraguas"],   # 𝒪
    "mu0": {"lluvia": F(1, 2), "sol": F(1, 2)},
    "P": {"lluvia": {"lluvia": F(7, 10),       # P(s'|s)
                     "sol": F(3, 10)},
          "sol": {"lluvia": F(3, 10),
                  "sol": F(7, 10)}},
    "B": {"lluvia": {"paraguas": F(9, 10),     # B(s, o)
                     "sin paraguas": F(1, 10)},
          "sol": {"paraguas": F(2, 10),
                  "sin paraguas": F(8, 10)}},
}

def conjunta(hmm, tray, obs):
    P, B = hmm["P"], hmm["B"]
    p = hmm["mu0"][tray[0]] * B[tray[0]][obs[0]]
    for t in range(1, len(obs)):
        p *= P[tray[t - 1]][tray[t]] * B[tray[t]][obs[t]]
    return p

C, N = "paraguas", "sin paraguas"
obs = [N, C, N]
todas = {tr: conjunta(paraguas, tr, obs)
         for tr in product(paraguas["estados"], repeat=3)}
for tr in sorted(todas, key=todas.get, reverse=True)[:3]:
    print(", ".join(tr), todas[tr])
```

```text
sol, sol, sol 98/3125
sol, lluvia, sol 81/3125
lluvia, lluvia, sol 189/25000
```

- **Gana sol, sol, sol** con conjunta $98/3125=392/12500\approx0.031$. Le sigue sol, lluvia, sol con $81/3125$.
- **Ninguna vale 0.** En el paraguas, todas las entradas de $P$ y $B$ son positivas. Toda trayectoria es posible, aunque unas son más probables que otras.

::: exercise {#mkv-c4-de-ej-cuantas title="Cuenta las trayectorias"}
Un modelo tiene 3 estados y observas 5 señales. ¿Cuántas trayectorias debes revisar por fuerza bruta? ¿Y con 30 señales?
:::

::: hint {#mkv-c4-de-pista-cuantas of="mkv-c4-de-ej-cuantas" title="¿Cuántas opciones por día?"}
¿Cuántos estados posibles hay por día? ¿Cuántos días hay?
:::

::: answer {#mkv-c4-de-resp-cuantas of="mkv-c4-de-ej-cuantas"}
Con 5 señales hay $3^5=243$ trayectorias. Con 30, hay $3^{30}\approx2.1\times10^{14}$: no podemos revisarlas a mano ni rápidamente.
:::

Calculemos primero la probabilidad de cada estado por día, dadas todas las señales.

---

## 2 · Suavizar con las dos tablas

**Piensa: el paraguas de mañana, ¿dice algo del clima de hoy?**

Sí, porque el clima tiende a mantenerse. El filtro $b_t$ solo usa las señales hasta $t$. El **suavizado** incluye las señales posteriores. Lo comparamos con Viterbi porque ambos usan toda la secuencia.

::: table {#mkv-c4-de-tabla-simbolos title="Los símbolos de esta página"}
| Símbolo | Se lee | Qué es |
|---|---|---|
| $b_{t\mid T}(s)$ | «be de te dado te mayúscula» | $\Pr(S_t=s\mid O_{0:T})$: el suavizado |
| $\operatorname{adelante}_t(s)$ | «adelante en $t$» | $\Pr(S_t=s,\ O_{0:t})$, sin normalizar |
| $\operatorname{atrás}_t(s)$ | «atrás en $t$» | $\Pr(O_{t+1:T}\mid S_t=s)$ |
| $\operatorname{mejor}_t(s)$ | «mejor en $t$» | La mayor conjunta de un camino que acaba en $s$ el día $t$ |
| $\operatorname{de}_t(s)$ | «de dónde viene» | El estado del día $t-1$ que da ese $\operatorname{mejor}_t(s)$ |
:::

- **Sobre el nombre.** Aquí, «suavizar» significa usar señales futuras. Es distinto del suavizado de conteos de la clase 1.
- **Sobre las letras.** Otros textos llaman $\alpha$, $\beta$ y $\delta$ a adelante, atrás y mejor. Aquí esas letras tienen otro significado.

::: remark {#mkv-c4-de-obs-suavizar title="El suavizado es adelante por atrás"}
**Condición.** Tenemos un modelo como en @mkv-c4-def-hmm y señales $o_{0:T}$ con $\Pr(O_{0:T}=o_{0:T})>0$.

$$
\begin{aligned}
&\operatorname{adelante}_t(s)=\sum_{s'}\operatorname{adelante}_{t-1}(s')P(s\mid s')B(s,o_t),\\
&\operatorname{atrás}_t(s)=\sum_{s'}P(s'\mid s)B(s',o_{t+1})\operatorname{atrás}_{t+1}(s'),\\
&b_{t\mid T}(s)=\frac{\operatorname{adelante}_t(s)\operatorname{atrás}_t(s)}{\Pr(O_{0:T}=o_{0:T})}.
\end{aligned}
$$

- **Arranques:** $\operatorname{adelante}_0(s)=\mu_0(s)B(s,o_0)$ y $\operatorname{atrás}_T(s)=1$.
- **De dónde sale:** $\Pr(S_t=s,O_{0:T})$ es el producto del pasado, $\operatorname{adelante}_t(s)$, por el futuro dado $S_t=s$, $\operatorname{atrás}_t(s)$. El futuro depende del pasado solo a través de $S_t$. Esto se debe a los dos supuestos de @mkv-c4-def-hmm.
- **Lectura:** sumar $\operatorname{adelante}_t\cdot\operatorname{atrás}_t$ sobre $s$ da $\Pr(O_{0:T})$ en cualquier día. Al normalizar el producto obtenemos $b_{t\mid T}$.
- **Casos nulos:** si $\Pr(O_{0:T})=0$, no podemos dividir. En el último día, $b_{T\mid T}=b_T$ porque no quedan señales futuras.
:::

**En el paraguas,** con sin paraguas, paraguas, sin paraguas:

::: table {#mkv-c4-de-tabla-suavizar title="Adelante, atrás y el suavizado de lluvia"}
| Día | adelante (lluvia, sol) | atrás (lluvia, sol) | $b_{t\mid 2}(\text{lluvia})$ |
|---|---|---|---:|
| 0 | 1/20, 2/5 | 2307/10000, 1663/10000 | 2307/15611 ≈ 0.148 |
| 1 | 279/2000, 59/1000 | 31/100, 59/100 | 8649/15611 ≈ 0.554 |
| 2 | 2307/200000, 1663/25000 | 1, 1 | 2307/15611 ≈ 0.148 |
:::

- **La suma:** en el día 1, $\tfrac{279}{2000}\cdot\tfrac{31}{100}+\tfrac{59}{1000}\cdot\tfrac{59}{100}=\tfrac{15611}{200000}$. Es la verosimilitud de las tres señales.
- **El más probable de cada día:** sol $\approx0.852$, lluvia $\approx0.554$, sol $\approx0.852$.
- **El futuro corrige al filtro.** El filtro del día 1 asigna a lluvia $279/397\approx0.703$. La señal sin paraguas del día 2 reduce esa probabilidad a $0.554$.

```python
def adelante_atras(hmm, obs):
    E, P, B = hmm["estados"], hmm["P"], hmm["B"]
    a = {s: hmm["mu0"][s] * B[s][obs[0]] for s in E}
    adelante = [a]
    for o in obs[1:]:
        a = {s: sum(a[r] * P[r][s] for r in E) * B[s][o]
             for s in E}
        adelante.append(a)
    z = {s: F(1) for s in E}
    atras = [z]
    for o in reversed(obs[1:]):
        z = {r: sum(P[r][s] * B[s][o] * z[s] for s in E)
             for r in E}
        atras.insert(0, z)
    return adelante, atras

def suavizar(hmm, obs):
    adelante, atras = adelante_atras(hmm, obs)
    L = sum(adelante[-1].values())          # Pr(O_{0:T})
    if L == 0:
        raise ValueError("señal imposible")
    return [{s: a[s] * z[s] / L for s in a}
            for a, z in zip(adelante, atras)]

for b in suavizar(paraguas, obs):
    print(b["lluvia"], b["sol"])
```

```text
2307/15611 13304/15611
8649/15611 6962/15611
2307/15611 13304/15611
```

Aprender un modelo sin etiquetas requiere estas dos tablas. También requiere la probabilidad de cada **par** de estados consecutivos, dada toda la secuencia.

::: exercise {#mkv-c4-de-ej-atras title="Calcula un renglón hacia atrás"}
Con las señales sin paraguas, paraguas, sin paraguas, comprueba que $\operatorname{atrás}_1(\text{sol})=59/100$.
:::

::: hint {#mkv-c4-de-pista-atras of="mkv-c4-de-ej-atras" title="¿Qué señal queda en el futuro?"}
Desde sol el día 1, ¿a qué estados puedes pasar? ¿Con qué probabilidad emite cada estado la señal del día 2?
:::

::: answer {#mkv-c4-de-resp-atras of="mkv-c4-de-ej-atras"}
Solo queda la señal sin paraguas del día 2, y $\operatorname{atrás}_2=1$. Entonces obtenemos $\tfrac{3}{10}\cdot\tfrac{1}{10}+\tfrac{7}{10}\cdot\tfrac{8}{10}=\tfrac{3}{100}+\tfrac{56}{100}=\tfrac{59}{100}$.
:::

Con el suavizado elegimos un estado por día. ¿Cómo encontramos la mejor secuencia completa sin revisar las $\lvert\mathcal S\rvert^{T+1}$?

---

## 3 · Decodificar con VITERBI

**Piensa: si conoces el mejor camino hasta cada estado de ayer, ¿necesitas revisar los caminos anteriores?**

No hace falta. Para terminar hoy en $s$, extendemos un camino que ayer terminó en algún $s'$. El paso adicional vale $P(s\mid s')B(s,o_t)$. No depende de cómo llegamos a $s'$. Basta conservar el mejor camino hasta cada $s'$:

$$
\begin{aligned}
\operatorname{mejor}_t(s)=\max_{s'}\ &\operatorname{mejor}_{t-1}(s')\\
&\cdot P(s\mid s')\,B(s,o_t).
\end{aligned}
$$

- **El arranque:** $\operatorname{mejor}_0(s)=\mu_0(s)B(s,o_0)$, igual que $\operatorname{adelante}_0$.
- **Máximo en vez de suma.** Usamos la recurrencia de $\operatorname{adelante}$ con $\max$ donde había $\sum$.
- **El apuntador** $\operatorname{de}_t(s)$ guarda el $s'$ ganador. Seguimos los apuntadores hacia atrás para reconstruir la trayectoria.

### El mapa de VITERBI

- **Qué calcula:** $\operatorname{mejor}_t(s)$ para cada día y estado, y la trayectoria de mayor conjunta.
- **Qué guarda:** una columna con $\lvert\mathcal S\rvert$ valores $\operatorname{mejor}$ y los apuntadores de todos los días.
- **Cómo avanza:** recorre los días en orden. En cada estado elige el mejor predecesor y multiplica por la emisión.
- **Qué devuelve:** la trayectoria y su conjunta. Sigue los apuntadores hacia atrás desde el mejor estado del último día.

::: figure {#mkv-c4-fig-flujo-viterbi title="VITERBI, en palabras"}
![Diagrama de flujo vertical de Viterbi, en palabras. 1: Para cada estado, mejor del día 0 igual a mu cero por la emisión de la primera señal. 2: Pasa al día siguiente. 3: Para cada estado, prueba cada estado de ayer: su mejor por la transición; guarda el máximo y de dónde vino, y multiplica por la emisión de la señal de hoy. 4, pregunta: ¿quedan días? Si sí, regresa al paso 2. Si no, 5: elige el estado con mayor mejor en el último día; si vale 0, error de señal imposible. 6: Sigue los apuntadores hacia atrás y devuelve la trayectoria y su probabilidad conjunta.](../_assets/mkv-c4-flujo-viterbi.svg)
:::

```text
INPUT   modelo ⟨𝒮, 𝒪, μ₀, P, B⟩;
        señales o_0, …, o_T.
OUTPUT  la trayectoria de mayor
        conjunta y esa conjunta.

 1 function VITERBI(modelo, o)
 2   mejor(s) ← μ₀(s)·B(s,o_0) para todo s
 3   para t de 1 a T:
 4     para cada s en 𝒮:
 5       de_t(s) ← el primer s' de 𝒮 que
                   maximiza mejor(s')·P(s|s')
 6       nuevo(s) ← mejor(de_t(s))
                    ·P(s|de_t(s))·B(s,o_t)
 7     mejor ← nuevo
 8   s_T ← el primer s de 𝒮 con mejor máximo
 9   si mejor(s_T) = 0: error «señal imposible»
10   para t de T a 1: s_{t-1} ← de_t(s_t)
11   return s_0, …, s_T y mejor(s_T)
```

**Versión en Python.** Los comentarios numerados corresponden al pseudocódigo. `max` con `key` devuelve el primer estado que alcanza el máximo. Así resolvemos los empates.

```python
def viterbi(hmm, obs):
    E, P, B = hmm["estados"], hmm["P"], hmm["B"]
    mejor = {s: hmm["mu0"][s] * B[s][obs[0]]
             for s in E}                         # (2)
    apuntadores = []
    for o in obs[1:]:                            # (3)
        de, nuevo = {}, {}
        for s in E:                              # (4)
            paso = lambda r: mejor[r] * P[r][s]
            de[s] = max(E, key=paso)             # (5)
            nuevo[s] = paso(de[s]) * B[s][o]     # (6)
        mejor = nuevo                            # (7)
        apuntadores.append(de)
    s = max(E, key=lambda r: mejor[r])           # (8)
    valor = mejor[s]
    if valor == 0:
        raise ValueError("señal imposible")      # (9)
    tray = [s]
    for de in reversed(apuntadores):             # (10)
        s = de[s]
        tray.append(s)
    return tray[::-1], valor                     # (11)

tray, p = viterbi(paraguas, obs)
print(", ".join(tray), p)
```

```text
sol, sol, sol 98/3125
```

Coincide con la trayectoria y la conjunta obtenidas por fuerza bruta. Veamos los pasos. La retícula tiene una columna por día y un nodo por estado.

::: table {#mkv-c4-de-traza-1 title="Traza de Viterbi, tramo 1: el arranque"}
| # | Nodo | Cuenta | mejor ← de |
|---|---|---|---|
| 1 | día 0, lluvia | $\tfrac12\cdot\tfrac{1}{10}$ | 1/20 ← inicio |
| 2 | día 0, sol | $\tfrac12\cdot\tfrac{8}{10}$ | 2/5 ← inicio |
:::

- **Fila 1:** con la señal sin paraguas, lluvia empieza con $1/20$.
- **Fila 2:** sol empieza con 8 veces ese valor: $2/5$.

::: figure {#mkv-c4-fig-trellis-1 title="Tramo 1: sol arranca adelante"}
![Retícula de Viterbi para sin paraguas, paraguas, sin paraguas: tres columnas, días 0, 1 y 2, con la señal arriba de cada una; dos filas, lluvia arriba y sol abajo. Solo la columna del día 0 está llena, con borde grueso: lluvia 1/20 y sol 2/5. Las columnas de los días 1 y 2 tienen nodos vacíos punteados.](../_assets/mkv-c4-trellis-1.svg)
:::

::: table {#mkv-c4-de-traza-2 title="Traza de Viterbi, tramo 2: el día 1"}
| # | Nodo | Cuenta | mejor ← de |
|---|---|---|---|
| 3 | día 1, lluvia | máx(7/200, 12/100) · 9/10 | 27/250 ← sol |
| 4 | día 1, sol | máx(3/200, 28/100) · 2/10 | 7/125 ← sol |
:::

- **Fila 3:** el mejor camino a lluvia viene de sol: $\tfrac25\cdot\tfrac{3}{10}=\tfrac{12}{100}$ supera a $\tfrac{1}{20}\cdot\tfrac{7}{10}$. La señal paraguas multiplica el valor por $9/10$.
- **Fila 4:** el mejor camino a sol también viene de sol. Emitir paraguas desde sol tiene probabilidad $2/10$.
- **Lluvia toma la delantera.** Si termináramos hoy, ganaría sol, lluvia, con $27/250$ frente a $7/125$.

::: figure {#mkv-c4-fig-trellis-2 title="Tramo 2: en el día 1 lluvia toma la delantera"}
![La misma retícula, nodos en las mismas posiciones. Columna del día 0 llena: lluvia 1/20 y sol 2/5. Columna del día 1 nueva, con borde grueso: lluvia 27/250 con flecha gruesa desde sol del día 0, y sol 7/125 con flecha gruesa desde sol del día 0. Las flechas que perdieron, de lluvia del día 0 a cada nodo del día 1, van delgadas y punteadas. Lluvia del día 1 lleva la marca de mayor valor de su columna. La columna del día 2 sigue vacía.](../_assets/mkv-c4-trellis-2.svg)
:::

::: table {#mkv-c4-de-traza-3 title="Traza de Viterbi, tramo 3: el día 2 y el regreso"}
| # | Nodo | Cuenta | mejor ← de |
|---|---|---|---|
| 5 | día 2, lluvia | máx(189/2500, 42/2500) · 1/10 | 189/25000 ← lluvia |
| 6 | día 2, sol | máx(81/2500, 98/2500) · 8/10 | 98/3125 ← sol |
| 7 | regreso | sol gana el día 2; sigue a sol, luego a sol | sol, sol, sol |
:::

- **Fila 5:** la señal sin paraguas reduce el valor de lluvia con el factor $1/10$.
- **Fila 6:** llegar a sol desde sol da $98/2500$. Desde lluvia da $81/2500$. Volver desde lluvia requiere cambiar de clima, con probabilidad $3/10$.
- **Fila 7:** $98/3125>189/25000$. Los apuntadores llevan de sol a sol y luego a sol. La ventaja de lluvia en el día 1 no sobrevivió.

::: figure {#mkv-c4-fig-trellis-3 title="Tramo 3: gana sol, sol, sol al regresar"}
![La misma retícula completa. Día 0: lluvia 1/20, sol 2/5. Día 1: lluvia 27/250 desde sol, sol 7/125 desde sol. Día 2, nuevo, con borde grueso: lluvia 189/25000 con flecha desde lluvia del día 1, y sol 98/3125 con flecha desde sol del día 1. El camino de regreso sol, sol, sol va resaltado con línea doble gruesa, de sol del día 2 a sol del día 1 y a sol del día 0. Al pie: conjunta 98/3125.](../_assets/mkv-c4-trellis-3.svg)
:::

### Lo que garantiza y cuánto cuesta

::: theorem {#mkv-c4-de-teo-viterbi title="Viterbi devuelve la trayectoria más probable"}
**Condición.** Tenemos un modelo como en @mkv-c4-def-hmm, con $\mathcal S$ finito y ordenado. Las señales $o_{0:T}$ cumplen $\Pr(O_{0:T}=o_{0:T})>0$. Esto equivale a que la mayor conjunta sea positiva. En un empate gana el primer estado de $\mathcal S$.

Usamos $\Pr(s_{0:t},o_{0:t})$ como abreviatura de $\Pr(S_{0:t}=s_{0:t},\ O_{0:t}=o_{0:t})$. Entonces:

$$
\begin{aligned}
\operatorname{mejor}_t(s)&=\max_{s_{0:t-1}}\Pr(s_{0:t-1},s,\ o_{0:t}),\\
\max_s\operatorname{mejor}_T(s)&=\max_{s_{0:T}}\Pr(s_{0:T},\ o_{0:T}).
\end{aligned}
$$

La trayectoria reconstruida con los apuntadores alcanza ese máximo.

**Lectura.** La columna del día $t$ resume los caminos hasta $t$. De los que terminan en $s$, solo necesitamos el mejor.

**Casos nulos.** Con $T=0$ no hay transiciones. Viterbi elige el $s$ con mayor $\mu_0(s)B(s,o_0)$, igual que el filtro $b_0$. Si $\Pr(O_{0:T})=0$, toda la columna final vale 0 y no hay trayectoria que devolver: `ValueError`.
:::

::: proof {#mkv-c4-de-dem-viterbi of="mkv-c4-de-teo-viterbi"}
**Por inducción en $t$.** Con $t=0$, el único camino que termina en $s$ es $s$ mismo. Su conjunta es $\mu_0(s)B(s,o_0)$.

**El paso.** Por @mkv-c4-obs-conjunta, un camino que termina en $s'$ el día $t-1$ y continúa a $s$ tiene conjunta:

$$
\begin{aligned}
&\Pr(s_{0:t-2},s',s,\ o_{0:t})\\
&\quad=\Pr(s_{0:t-2},s',\ o_{0:t-1})\,P(s\mid s')B(s,o_t).
\end{aligned}
$$

El último factor no depende de $s_{0:t-2}$. Por la hipótesis de inducción, maximizar sobre $s_{0:t-2}$ da $\operatorname{mejor}_{t-1}(s')$. Al maximizar sobre $s'$ obtenemos la recurrencia.

**El regreso.** $\operatorname{de}_t(s)$ guarda un $s'$ que alcanza ese máximo. Seguimos los apuntadores desde el mejor $s_T$ y reconstruimos un camino cuyo producto es $\operatorname{mejor}_T(s_T)$. La condición garantiza que ese valor sea positivo y que exista la posterior.
:::

- **Garantía.** La trayectoria devuelta tiene la mayor conjunta y, por tanto, la mayor posterior.
- **Costo.** Cada día prueba $\lvert\mathcal S\rvert$ predecesores por cada uno de $\lvert\mathcal S\rvert$ estados. Requiere del orden de $T\lvert\mathcal S\rvert^2$ productos. Un año del paraguas, con $T=364$, requiere unos $1456$ productos. Por fuerza bruta revisaríamos $2^{365}\approx7.5\times10^{109}$ trayectorias.
- **Memoria.** Una columna de valores y $T\lvert\mathcal S\rvert$ apuntadores.
- **Supuestos.** Conocemos el modelo: $\mu_0$, $P$ y $B$.

> [!TIP]
> **Ejemplo y contraejemplo de la condición.**
>
> - **Lo cumple:** el paraguas con sin paraguas, paraguas, sin paraguas. Las flechas sol → sol con $7/10$ y sol → sin paraguas con $8/10$ son positivas. También lo son todas las de $B=\begin{pmatrix}9/10&1/10\\2/10&8/10\end{pmatrix}$. La mayor conjunta es $98/3125>0$. Viterbi devuelve sol, sol, sol.
> - **No lo cumple:** agregamos la señal «nieve», que ningún estado emite: $B=\begin{pmatrix}9/10&1/10&0\\2/10&8/10&0\end{pmatrix}$. Con sin paraguas, nieve, sin paraguas, las flechas lluvia → nieve y sol → nieve valen 0. La columna del día 1 vale $(0,\ 0)$. La del día 2 también. No hay trayectoria que devolver: «señal imposible».

::: figure {#mkv-c4-fig-ej-decodificar title="Ejemplo y contraejemplo: Viterbi necesita una conjunta positiva"}
![Dos paneles con la misma retícula de tres días, lluvia arriba y sol abajo. Arriba, marcado como cumple: señales sin paraguas, paraguas, sin paraguas; columnas 1/20 y 2/5, 27/250 y 7/125, 189/25000 y 98/3125; camino sol, sol, sol resaltado con línea doble y conjunta 98/3125. Abajo, marcado como no cumple: señales sin paraguas, nieve, sin paraguas, con B de 2 por 3 y la columna de nieve en ceros; día 0 con 1/20 y 2/5, días 1 y 2 con 0 y 0 tachados; sin camino, con el letrero señal imposible.](../_assets/mkv-c4-ej-decodificar.svg)
:::

> [!WARNING]
> **Error típico: llamar a Viterbi un filtro o un suavizado.** El filtro permite elegir un estado diario con las señales hasta ese día. El suavizado usa todas las señales. **Viterbi maximiza la probabilidad de la secuencia completa.**

::: exercise {#mkv-c4-de-ej-dos-paraguas title="Corre Viterbi con dos paraguas"}
Con las señales paraguas, paraguas, corre Viterbi a mano. ¿Qué trayectoria devuelve? ¿Cuál es su conjunta?
:::

::: hint {#mkv-c4-de-pista-dos-paraguas of="mkv-c4-de-ej-dos-paraguas" title="¿Cómo arranca la columna?"}
¿Cuánto vale $\mu_0(s)B(s,\text{paraguas})$ en cada estado? En el día 1, ¿qué predecesor da el mayor producto para cada estado?
:::

::: answer {#mkv-c4-de-resp-dos-paraguas of="mkv-c4-de-ej-dos-paraguas"}
Día 0: lluvia $9/20$, sol $1/10$. Día 1, lluvia: $\max(\tfrac{9}{20}\cdot\tfrac{7}{10},\ \tfrac{1}{10}\cdot\tfrac{3}{10})\cdot\tfrac{9}{10}=\tfrac{567}{2000}$, desde lluvia. Día 1, sol: $\tfrac{9}{20}\cdot\tfrac{3}{10}\cdot\tfrac{2}{10}=\tfrac{27}{1000}$, desde lluvia. Gana lluvia, lluvia, con conjunta $567/2000$.
:::

Viterbi encuentra la mejor secuencia. ¿Coincide con elegir el estado más probable de cada día?

---

## 4 · Comparar con el mejor estado de cada día

**Piensa: si eliges el estado más probable del suavizado cada día, ¿obtienes la secuencia más probable?**

No siempre. **Elegir el mejor estado de cada día no garantiza la mejor secuencia.** Con sin paraguas, paraguas, sin paraguas, el suavizado elige sol, lluvia, sol. Viterbi elige sol, sol, sol.

- **Comparamos con el suavizado.** Viterbi y el suavizado usan todas las señales. El filtro solo usa las señales hasta ese día. Comparar Viterbi con el filtro mezclaría dos diferencias.
- **Qué probabilidad usamos.** No existe una «probabilidad del mejor por día». Usamos la posterior de la **trayectoria** formada con esos estados: su conjunta dividida entre $\Pr(O_{0:T})$.

```python
def por_dia(hmm, obs):
    E = hmm["estados"]
    return [max(E, key=lambda s: b[s])
            for b in suavizar(hmm, obs)]

for obs in ([N, C, N], [N, C, N, C], [C, C, N, C, C]):
    adelante, _ = adelante_atras(paraguas, obs)
    L = sum(adelante[-1].values())
    v, _ = viterbi(paraguas, obs)
    d = por_dia(paraguas, obs)
    print(", ".join(v), conjunta(paraguas, v, obs) / L)
    print(", ".join(d), conjunta(paraguas, d, obs) / L)
```

```text
sol, sol, sol 6272/15611
sol, lluvia, sol 5184/15611
sol, sol, sol, lluvia 169344/704647
sol, lluvia, sol, lluvia 139968/704647
lluvia, lluvia, sol, lluvia, lluvia 23147208/68607401
lluvia, lluvia, sol, lluvia, lluvia 23147208/68607401
```

::: table {#mkv-c4-de-tabla-contraste title="Viterbi frente al mejor estado de cada día, en el paraguas"}
| Señales | Viterbi | Mejor por día | ¿Coinciden? |
|---|---|---|---|
| sin, con, sin | sol, sol, sol: 6272/15611 ≈ 0.4018 | sol, lluvia, sol: 5184/15611 ≈ 0.3321 | no |
| sin, con, sin, con | sol, sol, sol, lluvia: 169344/704647 ≈ 0.2403 | sol, lluvia, sol, lluvia: 139968/704647 ≈ 0.1986 | no |
| con, con, sin, con, con | lluvia, lluvia, sol, lluvia, lluvia | la misma | sí |
:::

- **Por qué difieren.** El $0.554$ de lluvia en el día 1 reúne muchas trayectorias: sol, lluvia, sol; lluvia, lluvia, sol; y otras. Ninguna por separado supera a sol, sol, sol.
- **La marginal suma; Viterbi maximiza.** Un estado puede ser el más probable del día porque muchos caminos pasan por él. La mejor secuencia es un solo camino.
- **La trayectoria es posible.** En el paraguas, sol, lluvia, sol tiene conjunta $81/3125>0$. Es menos probable que sol, sol, sol, con $98/3125$.
- **A veces coinciden.** Con las señales con, con, sin, con, con, ambos dan lluvia, lluvia, sol, lluvia, lluvia. Por eso elegimos el ejemplo con cuidado.

::: exercise {#mkv-c4-de-ej-marginal title="Suma la marginal de lluvia"}
Usa las señales sin paraguas, paraguas, sin paraguas. Suma las conjuntas de las cuatro trayectorias con lluvia el día 1. Divide entre $15611/200000$. ¿Qué obtienes?
:::

::: hint {#mkv-c4-de-pista-marginal of="mkv-c4-de-ej-marginal" title="¿Cuáles son las cuatro?"}
El día 0 y el día 2 pueden ser lluvia o sol. Usa la función `conjunta` o la tabla de factores de la página 2.
:::

::: answer {#mkv-c4-de-resp-marginal of="mkv-c4-de-ej-marginal"}
Las conjuntas son $81/3125$ para sol, lluvia, sol y $189/25000$ para lluvia, lluvia, sol. Siguen $189/25000$ para sol, lluvia, lluvia y $441/200000$ para lluvia, lluvia, lluvia. Suman $8649/200000$. Al dividir obtenemos $8649/15611\approx0.554$: el suavizado de lluvia del día 1.
:::

---

## Ejercicios

::: exercise {#mkv-c4-de-ej-helado title="Decodifica el diario de helados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** la señal tiene tres valores. Además, $P$ no es simétrica. Usamos el helado de Eisner con los números de Jurafsky y Martin. El clima es calor o frío. Cada día alguien come uno, dos o tres helados.

- **El inicio:** $\mu_0=(4/5,\ 1/5)$, en el orden calor, frío.
- **Cómo cambia:** después de calor, sigue calor con $3/5$ o frío con $2/5$. Después de frío, cada estado tiene probabilidad $1/2$.
- **Los helados:** con calor, comer uno, dos o tres tiene probabilidades $1/5$, $2/5$ y $2/5$. Con frío, son $1/2$, $2/5$ y $1/10$.

El diario dice tres, uno, tres helados.

1. **Arranca:** calcula $\operatorname{mejor}_0$ de calor y de frío.
2. **Avanza:** calcula $\operatorname{mejor}_1$ y $\operatorname{mejor}_2$ de cada estado, con su apuntador.
3. **Regresa:** escribe la trayectoria de Viterbi y su conjunta.
4. **Compara:** el suavizado de frío es $905/14281$, $8625/14281$ y $2533/14281$. ¿Qué secuencia obtienes al elegir el mejor estado de cada día? ¿Coincide con Viterbi?
5. **Revisa:** cambia `paraguas` por el helado en la versión en Python y confirma el paso 3.
:::

::: hint {#mkv-c4-de-pista-helado-1 of="mkv-c4-de-ej-helado" title="Pista 1 · ¿Qué fila y qué columna usa cada factor?"}
¿Qué columna de $B$ corresponde a tres helados? En cada nodo del día 1, ¿cuáles son los dos candidatos antes de multiplicar por la emisión?
:::

::: hint {#mkv-c4-de-pista-helado-2 of="mkv-c4-de-ej-helado" title="Pista 2 · ¿Tu regreso sigue los apuntadores?"}
¿Elegiste el estado final usando $\operatorname{mejor}_2$ en lugar del suavizado? ¿El producto de los factores de tu trayectoria coincide con $\operatorname{mejor}_2$?
:::

::: answer {#mkv-c4-de-resp-helado of="mkv-c4-de-ej-helado" title="Respuesta · Calor, frío, calor"}
**1. Arranca.** Calor: $\tfrac45\cdot\tfrac25=\tfrac{8}{25}$. Frío: $\tfrac15\cdot\tfrac{1}{10}=\tfrac{1}{50}$.

**2. Avanza.**

- **Día 1, calor:** $\max(\tfrac{8}{25}\cdot\tfrac35,\ \tfrac{1}{50}\cdot\tfrac12)\cdot\tfrac15=\tfrac{24}{625}$, desde calor.
- **Día 1, frío:** $\max(\tfrac{8}{25}\cdot\tfrac25,\ \tfrac{1}{50}\cdot\tfrac12)\cdot\tfrac12=\tfrac{8}{125}$, desde calor.
- **Día 2, calor:** $\max(\tfrac{24}{625}\cdot\tfrac35,\ \tfrac{8}{125}\cdot\tfrac12)\cdot\tfrac25=\tfrac{8}{625}$, desde frío.
- **Día 2, frío:** $\max(\tfrac{24}{625}\cdot\tfrac25,\ \tfrac{8}{125}\cdot\tfrac12)\cdot\tfrac{1}{10}=\tfrac{2}{625}$, desde frío.

**3. Regresa.** Gana calor el día 2, con $8/625$. Su apuntador lleva a frío. El de frío lleva a calor. Obtenemos calor, frío, calor, con conjunta $8/625$.

**4. Compara.** Frío gana solo el día 1 ($8625/14281>1/2$). El mejor estado por día da calor, frío, calor. Coincide con Viterbi, pero depende de las señales.

**5. Revisa.** Con el helado, `viterbi` imprime calor, frío, calor y `8/625`.
:::

**Punto de control:** calcula el suavizado con las dos tablas y explica por qué usa señales futuras. Corre Viterbi a mano en una retícula chica, con apuntadores, y enuncia su condición. Muestra con cifras por qué elegir el mejor estado diario puede no dar la mejor secuencia.

---

## Lo que hay que llevarse

- **El problema.** Hay $\lvert\mathcal S\rvert^{T+1}$ trayectorias. Maximizar la conjunta equivale a maximizar la posterior.
- **Suavizar.** $b_{t\mid T}\propto\operatorname{adelante}_t\cdot\operatorname{atrás}_t$. Con sin paraguas, paraguas, sin paraguas, lluvia tiene probabilidades $2307/15611$, $8649/15611$ y $2307/15611$. Ganan sol $\approx0.852$, lluvia $\approx0.554$, sol $\approx0.852$ (@mkv-c4-de-obs-suavizar).
- **Viterbi.** Usa la recurrencia de adelante con $\max$ en vez de $\sum$, más apuntadores. Cuesta del orden de $T\lvert\mathcal S\rvert^2$. Devuelve la trayectoria de mayor conjunta si $\Pr(O_{0:T})>0$. Si no, lanza el error «señal imposible» (@mkv-c4-de-teo-viterbi).
- **El contraste.** Viterbi da sol, sol, sol con posterior $6272/15611\approx0.4018$ (conjunta $392/12500$). El mejor por día da sol, lluvia, sol con $5184/15611\approx0.3321$. Con cuatro días, $169344/704647\approx0.2403$ frente a $139968/704647\approx0.1986$.
- **Comparamos con el suavizado, no con el filtro.** En el paraguas, todas las trayectorias son posibles. Algunas son más probables que otras.

Todo esto supone que conoces $P$ y $B$. Si nadie registró el clima, ¿de dónde salen?

Continúa con [[mkv-aprender-lo-oculto|Aprender un modelo oculto]].
