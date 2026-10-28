---
id: mkv-lenguaje-pequeno
title: "Un modelo de lenguaje pequeño"
nav_title: "Lenguaje pequeño"
summary: "El mismo modelo con tres estados gramaticales y unas doce palabras: generar, predecir la siguiente palabra y cuánto ahorra frente a la tabla de palabras."
status: ready
estimated_time: 22m
tags: [markov, ocultas, lenguaje]
---

# Un modelo de lenguaje pequeño

**¿El mismo modelo sirve para decir qué palabra sigue, si los estados son categorías gramaticales que nadie ve?**

Al terminar tendrás:

- **Un modelo de lenguaje pequeño:** tres categorías y doce palabras, en tablas y en un grafo.
- **Frases generadas** con la `simular` del paraguas, y lo que el modelo no sabe.
- **La siguiente palabra** con $b_tPB$, y «casa», que cambia de categoría según el contexto.
- **Secuencias imposibles:** el mejor estado de cada palabra puede armar una frase de probabilidad 0; Viterbi no.
- **Una cuenta de parámetros** frente a la tabla de palabras, y lo que no compara.

## Lo que traes

- **El modelo.** En [[mkv-el-modelo-oculto|El modelo oculto]] escribiste $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ (@mkv-c4-def-hmm) y programaste `simular`, `probabilidad_conjunta` y `verosimilitud`. Aquí se copian tal cual.
- **La creencia.** En [[mkv-filtrar|Filtrar y predecir]] calculaste $b_t$ y la señal de mañana con $b_tPB$.
- **Decodificar.** En [[mkv-decodificar|Decodificar]] viste Viterbi, el suavizado y el mejor estado de cada día.
- **La tabla de palabras.** En [[mkv-generar-texto|Generar texto]], con memoria 1, la palabra siguiente salía de la fila de la palabra anterior.
- **Qué usa esta página:** la creencia $b_t$ sobre tres categorías gramaticales, después de leer $t+1$ palabras.

---

## 1 · Plantear el modelo con categorías

**Piensa: ¿qué necesitas saber para adivinar qué clase de palabra sigue?**

La categoría de la última palabra. Después de «la» viene un sustantivo; después de un sustantivo, casi siempre un verbo. Las categorías no se ven: son estados ocultos.

**En general.** Los estados $\mathcal S$ son categorías gramaticales. Las señales $\mathcal O$, las palabras. $P$ dice qué categoría sigue a cuál; $B$, qué palabra produce cada una. Es @mkv-c4-def-hmm sin cambios. En la clase 1 el vocabulario se llamaba $\Sigma$; aquí es $\mathcal O$, porque las palabras son las señales.

**El juguete.** Tres categorías: determinante, sustantivo y verbo. Doce palabras, $\lvert\mathcal O\rvert=12$, pocas, para trazar a mano. Es un modelo de lenguaje **pequeño**, no un modelo grande en miniatura.

- **La palabra ambigua.** «casa» es sustantivo («la casa») y verbo, de casar («casa a mi gata»: búscale pareja). Es la única con dos categorías.
- **El inicio.** $\mu_0=(1/2,\ 1/4,\ 1/4)$, en el orden determinante, sustantivo, verbo.

::: table {#mkv-c4-le-tabla-P title="Qué categoría sigue a cuál, P"}
| Desde | Determinante | Sustantivo | Verbo |
|---|---:|---:|---:|
| Determinante | 0 | 1 | 0 |
| Sustantivo | 1/4 | 0 | 3/4 |
| Verbo | 1/2 | 1/2 | 0 |
:::

- **Cuatro ceros en $P$.** Prohíben repetir categoría y pasar de determinante a verbo. Son reglas del modelo, no datos que faltan.

$B$, de $3\times12$, no cabe: va por estado, con las palabras de probabilidad positiva.

::: table {#mkv-c4-le-tabla-B title="Qué palabra produce cada categoría, B"}
| Estado | Palabras | $B(s,o)$ |
|---|---|---|
| Determinante | la, una, esta, mi | 1/2, 1/4, 1/8, 1/8 |
| Sustantivo | niña, gata, casa, sopa, luna | 1/4, 1/4, 1/4, 1/8, 1/8 |
| Verbo | come, ve, duerme, casa | 1/4, 1/4, 1/4, 1/4 |
:::

::: figure {#mkv-c4-fig-lenguaje-grafo title="El modelo de lenguaje pequeño como modelo oculto"}
![Grafo de tres estados ocultos con borde punteado: determinante, sustantivo y verbo. Flechas: de determinante a sustantivo 1; de sustantivo a determinante 1/4 y a verbo 3/4; de verbo a determinante 1/2 y a sustantivo 1/2. Los cuatro ceros son líneas punteadas sin punta, con una cruz y un 0: lazos punteados en determinante, sustantivo y verbo, y una línea entre determinante y verbo. Debajo, las palabras que emite cada estado, en columnas: determinante la 1/2, una 1/4, esta 1/8, mi 1/8; verbo casa, come, ve y duerme 1/4; sustantivo niña, gata y casa 1/4, sopa y luna 1/8. Las dos apariciones de casa van en un recuadro. Al pie, μ₀ = (1/2, 1/4, 1/4).](../_assets/mkv-c4-lenguaje-grafo.svg)
:::

**En Python**, el mismo diccionario que el paraguas, con las mismas claves:

```python
from fractions import Fraction as F

DET, SUS, VER = "determinante", "sustantivo", "verbo"
palabras = ["la", "una", "esta", "mi", "niña", "gata",
            "casa", "sopa", "luna", "come", "ve", "duerme"]

def fila(pesos):           # las palabras ausentes valen 0
    return {w: pesos.get(w, F(0)) for w in palabras}

lenguaje = {
    "estados": [DET, SUS, VER],
    "señales": palabras,
    "mu0": {DET: F(1, 2), SUS: F(1, 4), VER: F(1, 4)},
    "P": {DET: {DET: F(0), SUS: F(1), VER: F(0)},
          SUS: {DET: F(1, 4), SUS: F(0), VER: F(3, 4)},
          VER: {DET: F(1, 2), SUS: F(1, 2), VER: F(0)}},
    "B": {DET: fila({"la": F(1, 2), "una": F(1, 4),
                     "esta": F(1, 8), "mi": F(1, 8)}),
          SUS: fila({"niña": F(1, 4), "gata": F(1, 4),
                     "casa": F(1, 4), "sopa": F(1, 8),
                     "luna": F(1, 8)}),
          VER: fila({"come": F(1, 4), "ve": F(1, 4),
                     "duerme": F(1, 4), "casa": F(1, 4)})},
}

for s in lenguaje["estados"]:      # cada fila suma 1
    print(s, sum(lenguaje["P"][s].values()),
          sum(lenguaje["B"][s].values()))
```

```text
determinante 1 1
sustantivo 1 1
verbo 1 1
```

::: exercise {#mkv-c4-le-ej-mi title="Encuentra qué sigue a «mi»"}
Si la palabra de hoy es «mi», ¿qué palabras pueden venir mañana y con qué probabilidad?
:::

::: hint {#mkv-c4-le-pista-mi of="mkv-c4-le-ej-mi" title="¿Qué categoría produce «mi»?"}
¿Cuántas categorías pueden producir «mi»? ¿Qué dice su fila de $P$?
:::

::: answer {#mkv-c4-le-resp-mi of="mkv-c4-le-ej-mi"}
Solo el determinante produce «mi», y tras él viene un sustantivo con probabilidad 1. Mañana sale niña, gata o casa con 1/4 cada una, y sopa o luna con 1/8.
:::

---

## 2 · Generar frases

**Piensa: si sorteas categorías con $P$ y palabras con $B$, ¿salen frases?**

Tienen forma, pero no sentido. Copiamos `simular` de [[mkv-el-modelo-oculto|El modelo oculto]]; solo cambia el diccionario.

```python
import random

def muestrear_fila(fila, u):       # de la clase 1
    suma = 0
    for i, p in enumerate(fila):
        suma += p
        if u < suma:
            return i
    return max(i for i, p in enumerate(fila) if p > 0)

def simular(hmm, T, semilla):
    azar = random.Random(semilla)

    def sortear(fila, nombres):
        pesos = [fila[k] for k in nombres]
        return nombres[muestrear_fila(pesos, azar.random())]

    s = sortear(hmm["mu0"], hmm["estados"])      # S_0
    tray = [s]
    obs = [sortear(hmm["B"][s], hmm["señales"])]  # O_0
    for t in range(1, T + 1):
        s = sortear(hmm["P"][s], hmm["estados"])  # S_t
        tray.append(s)
        obs.append(sortear(hmm["B"][s], hmm["señales"]))
    return tray, obs

tray, obs = simular(lenguaje, 7, semilla=2046)
for t in range(8):
    print(t, tray[t].ljust(12), obs[t])
```

```text
0 sustantivo   casa
1 verbo        casa
2 determinante la
3 sustantivo   gata
4 verbo        come
5 sustantivo   niña
6 verbo        duerme
7 determinante esta
```

- **Se lee:** «casa casa la gata come niña duerme esta». Las categorías respetan $P$: nunca hay dos sustantivos ni dos verbos seguidos.
- **«casa» dos veces:** primero sustantivo, luego verbo. La diferencia está en la columna oculta.

**Lo que el modelo no sabe.** Solo recuerda una categoría.

- **Sentido:** «mi luna come la casa» tiene probabilidad positiva.
- **Objeto del verbo:** «duerme esta» sale igual que «come esta».
- **Concordancia:** no la maneja. Sustantivos y determinantes con género son femeninos y singulares, y eso lo esconde; con «el» saldría «el gata».
- **Fin de frase:** no hay punto; la cadena sigue.

::: exercise {#mkv-c4-le-ej-luna title="Calcula una frase absurda"}
Calcula la probabilidad conjunta de «mi luna come la casa» con las categorías determinante, sustantivo, verbo, determinante, sustantivo.
:::

::: hint {#mkv-c4-le-pista-luna of="mkv-c4-le-ej-luna" title="¿Cuántos factores lleva?"}
Cinco palabras: ¿cuántos factores de $B$, cuántos de $P$ y cuál de $\mu_0$?
:::

::: answer {#mkv-c4-le-resp-luna of="mkv-c4-le-ej-luna"}
$\mu_0$, cinco de $B$ y cuatro de $P$:

$$
\begin{aligned}
&\tfrac12\cdot\tfrac18\cdot1\cdot\tfrac18\cdot\tfrac34\cdot\tfrac14\\
&\quad\cdot\tfrac12\cdot\tfrac12\cdot1\cdot\tfrac14=\tfrac{3}{32768}.
\end{aligned}
$$

Es pequeña, pero no es 0: el modelo acepta la frase.
:::

---

## 3 · Predecir la siguiente palabra

**Piensa: después de «la gata», ¿qué palabra esperas?**

Un verbo, casi siempre. Es la señal de mañana de [[mkv-filtrar|Filtrar y predecir]]: filtra lo leído, avanza con $P$ y reparte con $B$.

**En general.** Si $\Pr(O_{0:t}=o_{0:t})>0$, existe $b_t$ y la siguiente palabra se predice así:

$$
\begin{aligned}
&\Pr(O_{t+1}=o\mid O_{0:t}=o_{0:t})\\
&\quad=\sum_{s,s'}b_t(s)\,P(s'\mid s)\,B(s',o).
\end{aligned}
$$

**Tras «la gata».** «la» solo es determinante y «gata» solo sustantivo, así que $b_1(\text{sustantivo})=1$. La fila de sustantivo en $P$ da $(1/4,\ 0,\ 3/4)$. Con $B$:

::: table {#mkv-c4-le-tabla-siguiente title="La siguiente palabra después de «la gata»"}
| Palabras | Categoría | Probabilidad de cada una |
|---|---|---|
| come, ve, duerme, casa | verbo | 3/16 |
| la | determinante | 1/8 |
| una | determinante | 1/16 |
| esta, mi | determinante | 1/32 |
:::

- **Los verbos suman 3/4** y los determinantes 1/4. Ningún sustantivo sigue: es el cero de sustantivo a sustantivo.

**«casa» según el contexto.** La creencia sobre el último «casa» depende de lo anterior:

::: table {#mkv-c4-le-tabla-casa title="La creencia sobre el último «casa», según lo leído"}
| Lo leído | Sustantivo | Verbo |
|---|---:|---:|
| casa | 1/2 | 1/2 |
| la casa | 1 | 0 |
| la gata casa | 0 | 1 |
| casa casa | 2/5 | 3/5 |
:::

- **Sola**, «casa» empata: $\mu_0$ da 1/4 a cada categoría y las dos producen «casa» con 1/4.
- **Tras «la»** solo puede ser sustantivo; **tras «la gata»**, solo verbo.
- **Tras otro «casa»**, se inclina al verbo: sustantivo pasa a verbo con 3/4.

El filtro de [[mkv-filtrar|Filtrar y predecir]], copiado: predecir, corregir, normalizar.

```python
def normalizar(d):
    total = sum(d.values())
    if total == 0:
        raise ValueError(
            "señal imposible: no se puede normalizar")
    return {s: p / total for s, p in d.items()}

def avanzar(hmm, b):               # b·P
    E = hmm["estados"]
    return {s2: sum(b[s] * hmm["P"][s][s2] for s in E)
            for s2 in E}

def filtrar(hmm, obs):             # b_0, ..., b_T
    E, B = hmm["estados"], hmm["B"]
    b = normalizar({s: hmm["mu0"][s] * B[s][obs[0]]
                    for s in E})
    creencias = [b]
    for o in obs[1:]:
        pred = avanzar(hmm, b)
        b = normalizar({s: pred[s] * B[s][o] for s in E})
        creencias.append(b)
    return creencias

def siguiente(hmm, b):             # b·P·B
    pred = avanzar(hmm, b)
    return {o: sum(pred[s] * hmm["B"][s][o]
                   for s in hmm["estados"])
            for o in hmm["señales"]}

for frase in ["casa", "la casa", "la gata casa", "casa casa"]:
    b = filtrar(lenguaje, frase.split())[-1]
    print(frase.ljust(13), b[SUS], b[VER])

b = filtrar(lenguaje, ["la", "gata"])[-1]
print(siguiente(lenguaje, b)["come"])
```

```text
casa          1/2 1/2
la casa       1 0
la gata casa  0 1
casa casa     2/5 3/5
3/16
```

**Con toda la frase.** «casa mi gata» tiene dos lecturas: «casa (a) mi gata», con «casa» verbo, o «casa» suelta y luego «mi gata…», con «casa» sustantivo. El filtro lee «casa» antes de ver «mi». Viterbi ve todo y elige verbo, determinante, sustantivo. Copiamos las dos funciones de [[mkv-el-modelo-oculto|El modelo oculto]]:

```python
from itertools import product

def probabilidad_conjunta(hmm, tray, obs):
    P, B = hmm["P"], hmm["B"]
    p = hmm["mu0"][tray[0]] * B[tray[0]][obs[0]]
    for t in range(1, len(tray)):
        p *= P[tray[t - 1]][tray[t]] * B[tray[t]][obs[t]]
    return p

def verosimilitud(hmm, obs):      # suma sobre trayectorias
    todas = product(hmm["estados"], repeat=len(obs))
    return sum(probabilidad_conjunta(hmm, tr, obs)
               for tr in todas)

frase = ["casa", "mi", "gata"]
L = verosimilitud(lenguaje, frase)
for tr in ([VER, DET, SUS], [SUS, DET, SUS]):
    p = probabilidad_conjunta(lenguaje, tr, frase)
    print(tr[0], p, p / L)
```

```text
verbo 1/1024 2/3
sustantivo 1/2048 1/3
```

- **Gana la lectura de verbo**, con posterior 2/3 frente a 1/3. Pesa más porque el verbo pasa a determinante con 1/2, y el sustantivo solo con 1/4.
- **«la gata casa casa» tiene una sola lectura:** determinante, sustantivo, verbo, sustantivo, con probabilidad posterior 1. El contexto resuelve los dos «casa».

::: exercise {#mkv-c4-le-ej-tras-casa title="Predice después de «la gata casa»"}
Después de «la gata casa», ¿qué palabras pueden seguir y con qué probabilidad?
:::

::: hint {#mkv-c4-le-pista-tras-casa of="mkv-c4-le-ej-tras-casa" title="¿Qué creencia tienes?"}
Usa la tabla de «casa»: ¿en qué categoría estás con certeza? ¿Qué dice su fila de $P$?
:::

::: answer {#mkv-c4-le-resp-tras-casa of="mkv-c4-le-ej-tras-casa"}
La creencia es verbo con 1, y la fila de verbo da $(1/2,\ 1/2,\ 0)$. Determinantes: la 1/4, una 1/8, esta 1/16, mi 1/16. Sustantivos: niña, gata y casa 1/8 cada una; sopa y luna 1/16.
:::

---

## 4 · Encontrar secuencias imposibles

**Piensa: si eliges la mejor categoría de cada palabra por separado, ¿la frase que armas puede ser imposible?**

Sí, si hay ceros. En el paraguas no pasaba: todas las entradas de $P$ y $B$ son positivas.

::: remark {#mkv-c4-le-obs-imposible title="Ceros en P o en B: trayectorias y señales imposibles"}
**Condición.** Un modelo como en @mkv-c4-def-hmm con alguna entrada de $P$ o de $B$ igual a 0.

- **Trayectorias imposibles.** Si una trayectoria usa una entrada nula, su probabilidad conjunta vale 0, por los casos nulos de @mkv-c4-obs-conjunta.
- **Viterbi no las elige.** Si $\Pr(O_{0:T}=o_{0:T})>0$, alguna trayectoria tiene conjunta positiva, y el máximo también.
- **El mejor de cada día sí puede.** Cada día se elige solo; nada revisa las transiciones entre días.
- **Señales imposibles.** Si $\Pr(O_{0:T}=o_{0:T})=0$, no hay creencia: el denominador vale 0 y no se puede normalizar.
:::

**«casa casa casa».** El suavizado da 1/2 y 1/2 a sustantivo y verbo en las tres palabras. **El caso depende de un empate:** en cada día gana el primer estado de la lista. El mejor de cada día arma sustantivo, sustantivo, sustantivo, que usa dos veces el cero de sustantivo a sustantivo: su probabilidad es 0.

Viterbi da sustantivo, verbo, sustantivo, con conjunta 3/2048. Empata con verbo, sustantivo, verbo, y gana por el mismo orden. En este modelo no hay frase de hasta ocho palabras que caiga en lo imposible sin empate; el ejercicio final rompe el empate.

**Una señal imposible.** «la la» pide dos determinantes seguidos, que están prohibidos: solo ellos producen «la». La verosimilitud vale 0 y el filtro no puede normalizar:

```python
frase = ["casa", "casa", "casa"]
print(probabilidad_conjunta(lenguaje, [SUS] * 3, frase))
print(probabilidad_conjunta(lenguaje, [SUS, VER, SUS], frase))
print(verosimilitud(lenguaje, ["la", "la"]))
try:
    filtrar(lenguaje, ["la", "la"])
except ValueError as e:
    print(e)
```

```text
0
3/2048
0
señal imposible: no se puede normalizar
```

En [[mkv-decodificar|Decodificar]], el mejor de cada día y Viterbi diferían, pero ambos eran posibles. Aquí el mejor de cada día da una trayectoria prohibida.

::: exercise {#mkv-c4-le-ej-la-come title="Revisa «la come»"}
¿Cuánto vale la verosimilitud de «la come»? ¿Qué hace `filtrar` con esa frase?
:::

::: hint {#mkv-c4-le-pista-la-come of="mkv-c4-le-ej-la-come" title="¿Quién dice cada palabra?"}
¿Qué categorías producen «la» y «come»? ¿Puede la primera pasar a la segunda?
:::

::: answer {#mkv-c4-le-resp-la-come of="mkv-c4-le-ej-la-come"}
«la» solo la produce el determinante y «come» solo el verbo, y $P(\text{verbo}\mid\text{determinante})=0$. La verosimilitud vale 0. `filtrar` calcula $b_0$ y lanza `ValueError` en la segunda palabra.
:::

---

## 5 · Contar los parámetros

**Piensa: ¿cuántos números necesita este modelo, y cuántos la tabla de palabras de la clase 1?**

Muchos menos, si cuentas igual. Una celda es una entrada de una tabla. Un parámetro libre es una celda que puedes elegir; la última de cada fila queda fija, porque la fila suma 1.

**Sin distribución inicial y sin descontar ceros.** El modelo oculto tiene $P$, de $\lvert\mathcal S\rvert\times\lvert\mathcal S\rvert$, y $B$, de $\lvert\mathcal S\rvert\times\lvert\mathcal O\rvert$. La tabla de palabras con memoria 1 es de $\lvert\mathcal O\rvert\times\lvert\mathcal O\rvert$.

::: table {#mkv-c4-le-tabla-parametros title="Celdas y parámetros libres, sin distribución inicial"}
| Modelo | Celdas | Libres |
|---|---|---|
| Oculto | $3^2+3\cdot12=45$ | $3\cdot2+3\cdot11=39$ |
| Tabla de palabras | $12^2=144$ | $12\cdot11=132$ |
:::

**Con distribución inicial.** Sumamos $\mu_0$ al oculto y la distribución de la primera palabra a la tabla: 48 celdas y 41 libres, frente a 156 y 143.

**Con ceros, sin distribución inicial.** Los ceros son reglas: no se estiman. Las filas de $P$ tienen 1, 2 y 2 celdas posibles: 2 libres en vez de 6. Si solo fijamos los ceros de $P$ y dejamos $B$ densa, quedan 35. Si también fijamos los de $B$ (4, 5 y 4 palabras por estado: 3, 4 y 3 libres), quedan 12.

**Lo que no se compara.** Las familias no tienen la misma capacidad: menos parámetros no significa «mejor».

- **El oculto no puede representar cualquier tabla de palabras.** «la» y «mi» comparten estado, así que predicen lo mismo. Una tabla de palabras puede darles filas distintas.
- **La tabla no ve más atrás de la palabra anterior.** Tras «casa» tiene una sola fila. El oculto da «la» con 3/16 tras «casa» y con 1/4 tras «la gata casa».

::: exercise {#mkv-c4-le-ej-veinte title="Cuenta con veinte palabras"}
Agrega 8 palabras, 20 en total, sin cambiar las tres categorías. Sin distribución inicial y sin descontar ceros, ¿cuántas celdas y libres tiene cada modelo?
:::

::: hint {#mkv-c4-le-pista-veinte of="mkv-c4-le-ej-veinte" title="¿Qué tamaño cambia?"}
¿Cambia $\lvert\mathcal S\rvert$ o $\lvert\mathcal O\rvert$? ¿Qué matrices crecen?
:::

::: answer {#mkv-c4-le-resp-veinte of="mkv-c4-le-ej-veinte"}
Oculto: $9+3\cdot20=69$ celdas y $6+3\cdot19=63$ libres. Tabla de palabras: $20^2=400$ celdas y $20\cdot19=380$ libres. El oculto crece en línea con el vocabulario; la tabla, con su cuadrado.
:::

---

## 6 · Distinguir este modelo de un transformer

**Piensa: ¿un modelo de lenguaje grande es un modelo oculto gigante?**

No. Comparten la pregunta, qué palabra sigue dado lo leído, pero guardan lo leído de otra forma.

> [!NOTE]
> **Un transformer no es un modelo oculto de Markov.**
>
> - **El modelo oculto** resume lo leído en la creencia $b_t$. Con cada palabra la actualiza: predecir con $P$, corregir con $B$, normalizar.
> - **Un transformer** (Vaswani et al., 2017, que lo presentaron como traductor de codificador–decodificador) genera un símbolo a la vez, atendiendo directamente a los anteriores. No tiene un estado oculto que salte con $P$ y emita con $B$, ni una creencia que se actualice.
> - **Con una ventana de contexto fija** de $h$ palabras, la siguiente depende solo de la ventana. El estado es la ventana, que se ve, como la memoria $h$ de la clase 1.
> - **Este modelo pequeño no explica uno grande.** Solo muestra, con números a mano, qué es predecir la siguiente palabra.

::: exercise {#mkv-c4-le-ej-memoria title="Compara qué se guarda"}
Tras «la gata casa», ¿qué guarda de lo leído el modelo oculto? ¿Y la tabla de palabras de la clase 1?
:::

::: hint {#mkv-c4-le-pista-memoria of="mkv-c4-le-ej-memoria" title="¿Qué usa cada uno para la fila siguiente?"}
¿Qué información necesita cada modelo para calcular la distribución de la siguiente palabra?
:::

::: answer {#mkv-c4-le-resp-memoria of="mkv-c4-le-ej-memoria"}
El oculto guarda la creencia: verbo con 1, que depende de «la gata». La tabla guarda solo la palabra «casa», sin saber si fue verbo o sustantivo.
:::

---

## Ejercicios

::: exercise {#mkv-c4-le-ej-cero title="Cambia un cero de P"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** un verbo ya puede seguir a otro. La fila de verbo en $P$ pasa de $(1/2,\ 1/2,\ 0)$ a $(9/20,\ 9/20,\ 1/10)$. Todo lo demás queda igual. Puedes usar el Python de esta página.

1. **Revisa:** comprueba que la fila nueva suma 1. ¿Cuántos ceros de $P$ quedan?
2. **Cuenta:** ¿cuántos parámetros libres reales tiene ahora el modelo, sin distribución inicial y con $B$ completa?
3. **Prueba:** ¿cuánto vale ahora la verosimilitud de «come ve»? ¿Cuánto valía antes?
4. **Decodifica:** para «casa casa casa», ¿qué dan Viterbi y el mejor de cada día? ¿Sigue siendo imposible la trayectoria del mejor de cada día?
5. **Juzga:** en una frase, ¿qué gana y qué pierde el modelo con este cambio?
:::

::: hint {#mkv-c4-le-pista-cero-1 of="mkv-c4-le-ej-cero" title="Pista 1 · ¿Qué fila tocas y qué trayectorias aparecen?"}
¿Cuántas celdas posibles tiene ahora la fila de verbo? Con «casa» tres veces, ¿qué trayectorias con dos verbos seguidos dejan de valer 0?
:::

::: hint {#mkv-c4-le-pista-cero-2 of="mkv-c4-le-ej-cero" title="Pista 2 · ¿Tu cuenta de «casa casa casa» cuadra?"}
¿Las conjuntas positivas que encontraste suman la verosimilitud? ¿La trayectoria del mejor de cada día está entre ellas?
:::

::: answer {#mkv-c4-le-resp-cero of="mkv-c4-le-ej-cero" title="Respuesta · Un cero menos"}
**1. Revisa.** $9/20+9/20+1/10=1$. Quedan tres ceros: determinante a determinante, determinante a verbo y sustantivo a sustantivo.

**2. Cuenta.** Las filas de $P$ tienen 1, 2 y 3 celdas posibles: $0+1+2=3$ libres. Con los 33 de $B$ densa, son 36, uno más que 35.

**3. Prueba.** Antes valía 0. Ahora:

$$
\tfrac14\cdot\tfrac14\cdot\tfrac1{10}\cdot\tfrac14=\tfrac{1}{640}.
$$

**4. Decodifica.** La verosimilitud es $161/51200$. Viterbi sigue dando sustantivo, verbo, sustantivo: conjunta $27/20480$, posterior $135/322\approx0.419$. El suavizado rompe el empate y el mejor de cada día da sustantivo, verbo, verbo. Ya es posible: conjunta $3/10240$, posterior $15/161\approx0.093$. Sigue siendo distinta de Viterbi y menos probable.

**5. Juzga.** Gana frases que antes no podía decir, y pierde una regla: ahora acepta «come ve», que no es español.
:::

**Punto de control:** debes poder hacer cuatro cosas.

- **Escribir** un modelo de lenguaje pequeño como modelo oculto, con categorías como estados y palabras como señales.
- **Predecir** la siguiente palabra con $b_tPB$, y decir cómo cambia la creencia sobre «casa» con el contexto.
- **Mostrar** con «casa casa casa» que el mejor de cada día puede dar una trayectoria de probabilidad 0, y Viterbi no.
- **Contar** celdas y libres en una sola convención, y decir qué no compara esa cuenta.

---

## Lo que hay que llevarse

- **El mismo modelo:** categorías como estados ocultos y palabras como señales; @mkv-c4-def-hmm no cambia. Aquí: 3 categorías, 12 palabras, $\mu_0=(1/2,1/4,1/4)$ y cuatro ceros en $P$.
- **Generar:** `simular`, copiada del paraguas, con semilla 2046 da «casa casa la gata come niña duerme esta». Respeta las categorías; no sabe de sentido, de objetos ni de concordancia.
- **Predecir:** tras «la gata», cada verbo sale con 3/16. «casa» es sustantivo y verbo con 1/2 cada uno; es solo verbo tras «la gata» y verbo con 3/5 tras otro «casa».
- **Con toda la frase:** en «casa mi gata», Viterbi lee verbo, determinante, sustantivo, con posterior 2/3 frente a 1/3. «la gata casa casa» tiene una sola lectura.
- **Los ceros:** en «casa casa casa», con empate en cada día, el mejor de cada día da sustantivo, sustantivo, sustantivo, de probabilidad 0; Viterbi da sustantivo, verbo, sustantivo, con 3/2048 (@mkv-c4-le-obs-imposible). «la la» tiene verosimilitud 0, y filtrar no puede normalizar.
- **Parámetros:** sin distribución inicial, 45 celdas y 39 libres frente a 144 y 132; con ella, 48 y 41 frente a 156 y 143; 35 libres si fijamos los ceros de $P$ con $B$ densa, y 12 si también los de $B$. Las familias no tienen la misma capacidad.
- **Un transformer no es un modelo oculto:** comparten la pregunta de qué sigue, no la forma de guardar lo leído.

Ya sabes qué crees del estado que no ves. Con esa creencia, ¿cómo decides qué hacer?

Continúa con [[mkv-decidir-sin-ver|Decidir sin ver el estado]].
