---
id: mkv-aprender-lo-oculto
title: "Aprender un modelo oculto"
nav_title: "Aprender"
summary: "Con etiquetas se cuenta, como en la clase 1; sin etiquetas, la idea de Baum-Welch: contar con fracciones y repetir."
status: ready
estimated_time: 18m
tags: [markov, ocultas, baum-welch]
---

# Aprender un modelo oculto

**¿Cómo se aprenden $P$ y $B$ de unas señales, si nadie anotó el clima?**

Al terminar tendrás:

- **Contar con etiquetas:** estimar $\widehat P$ y $\widehat B$ de una semana anotada, cumpliendo la condición de cada fila.
- **Explicar Baum-Welch:** repartir cada día entre estados, contar con fracciones y repetir.
- **Hacer un paso a mano:** comparar la verosimilitud antes y después con dos días del paraguas.
- **Lo que no se garantiza:** el mejor modelo, los nombres de los estados y la independencia del inicio.

## Lo que traes

- **Contar.** En [[mkv-ajustar-contando|Ajustar contando]] usaste $N(s,s')$ y $N(s)$: $\widehat P(s'\mid s)=N(s,s')/N(s)$ (@mkv-c1-conteos). Con $N(s)=0$, no estimas esa fila.
- **El modelo oculto.** En [[mkv-el-modelo-oculto|El modelo oculto]] usaste $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$, el diccionario `paraguas` y una semana simulada.
- **Suavizar.** En [[mkv-decodificar|Decodificar]] calculaste $b_{t\mid T}(s)=\Pr(S_t=s\mid O_{0:T})$ con **todas** las señales.
- **Aquí usamos:** el paraguas y $b_{t\mid T}$, no la creencia filtrada $b_t$ ni valores $V$.

---

## 1 · Contar con etiquetas

**Piensa: si alguien anotó el clima de cada día junto a la señal, ¿qué cuentas?**

Cuentas transiciones, como en la clase 1, y pares (estado, señal). La primera tabla estima $P$; la segunda, $B$.

::: definition {#mkv-c4-def-contar title="Estimar P y B contando"}
$$
\begin{aligned}
\widehat P(s'\mid s)&=\frac{N(s,s')}{N(s)},\\
\widehat B(s,o)&=\frac{N(s,o)}{\sum_{o'\in\mathcal O}N(s,o')}.
\end{aligned}
$$

- **Qué es:** dada la trayectoria $s_0,\dots,s_T$ y las señales $o_0,\dots,o_T$, $N(s,s')$ cuenta los pasos $t\in\{0,\dots,T-1\}$ con $s_t=s$ y $s_{t+1}=s'$. $N(s)=\sum_{s'}N(s,s')$ cuenta las salidas de $s$. $N(s,o)$ cuenta los días $t\in\{0,\dots,T\}$ con $s_t=s$ y $o_t=o$.
- **Cómo se calcula:** recorre los datos y divide cada fila entre su total. La fila $s$ de $\widehat P$ requiere $N(s)>0$. La fila $s$ de $\widehat B$ requiere que $s$ aparezca.
- **Qué significa:** la conjunta separa los factores de $P$ y de $B$. Maximiza cada producto contando, como en @mkv-c1-teo-maximo. Así obtienes los $P$ y $B$ que hacen más probables los datos.
- **Qué no es:** el denominador de $\widehat B$ no es $N(s)$. $N(s)$ cuenta salidas; el último día no tiene. $N(s,o)$ cuenta días; el último sí tiene señal.
:::

- **Ojo con la notación.** $N$ tiene dos usos según su segundo argumento: estado para transiciones, señal para emisiones.

**En la semana simulada.** Usamos la semana de la página 2, con el clima anotado. Los días 0 y 1 son sol sin paraguas. Del 2 al 5 llueve con paraguas. El día 6 llueve sin paraguas.

::: table {#mkv-c4-ap-tabla-conteos title="Los conteos de la semana anotada"}
| Desde | Hacia lluvia | Hacia sol | $N(s)$ |
|---|---:|---:|---:|
| lluvia | 4 | 0 | 4 |
| sol | 1 | 1 | 2 |
:::

::: table {#mkv-c4-ap-tabla-emisiones title="Las señales de cada clima en la semana anotada"}
| Estado | Paraguas | Sin paraguas | Días |
|---|---:|---:|---:|
| lluvia | 4 | 1 | 5 |
| sol | 0 | 2 | 2 |
:::

Ordena los estados como lluvia, sol. Las columnas de $\widehat B$ son paraguas, sin paraguas:

$$
\begin{aligned}
\widehat P&=\begin{pmatrix}1&0\\1/2&1/2\end{pmatrix},\\
\widehat B&=\begin{pmatrix}4/5&1/5\\0&1\end{pmatrix}.
\end{aligned}
$$

- **Seis salidas, siete días.** Hay $T=6$ transiciones y 7 señales. La lluvia tiene 4 salidas y aparece 5 días.
- **Ceros por pocos datos.** $\widehat P(\text{sol}\mid\text{lluvia})=0$ y $\widehat B(\text{sol},\text{paraguas})=0$. El modelo original tiene $3/10$ y $2/10$.

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** la semana completa tiene sol→sol, sol→lluvia y cuatro veces lluvia→lluvia. $N(\text{lluvia})=4$ y $N(\text{sol})=2$: puedes estimar las dos filas de $\widehat P=\begin{pmatrix}1&0\\1/2&1/2\end{pmatrix}$.
> - **No lo cumple:** los días 2 a 6, cinco días de lluvia. Hay lluvia→lluvia cuatro veces, sin salidas de sol: $N(\text{sol})=0$. El código deja esa fila en ceros: $\widehat P=\begin{pmatrix}1&0\\0&0\end{pmatrix}$. La fila $(0,\ 0)$ no es una distribución. Tampoco estimas la fila de sol de $\widehat B$.

::: figure {#mkv-c4-fig-ej-aprender title="Ejemplo y contraejemplo: cada estado tiene que salir"}
![Dos paneles con la tira de días anotados y la matriz estimada debajo. Arriba, el que cumple: los siete días sol, sol, lluvia, lluvia, lluvia, lluvia, lluvia; lluvia sale 4 veces y sol 2; P gorro con filas (1, 0) y (1/2, 1/2). Abajo, el que no: solo los cinco días de lluvia; sol sale 0 veces; P gorro con filas (1, 0) y (0, 0), y la fila de sol marcada como sin estimar.](../_assets/mkv-c4-ej-aprender.svg)
:::

**En Python.** Agrega una segunda tabla a CONTAR-TRANSICIONES de la clase 1:

```python
from fractions import Fraction as F

def contar(estados, señales, tray, obs):
    NP = {s: {s2: 0 for s2 in estados} for s in estados}
    NB = {s: {o: 0 for o in señales} for s in estados}
    for s, s2 in zip(tray, tray[1:]):   # T pares
        NP[s][s2] += 1
    for s, o in zip(tray, obs):         # T + 1 días
        NB[s][o] += 1

    def filas(N):                       # sin datos: ceros
        out = {}
        for s, f in N.items():
            tot = sum(f.values())
            out[s] = {k: F(n, tot) if tot else F(0)
                      for k, n in f.items()}
        return out
    return filas(NP), filas(NB)

C, N = "paraguas", "sin paraguas"
tray = ["sol", "sol"] + ["lluvia"] * 5
obs = [N, N, C, C, C, C, N]
P_g, B_g = contar(["lluvia", "sol"], [C, N], tray, obs)
for s in ["lluvia", "sol"]:
    print(s, *P_g[s].values(), "|", *B_g[s].values())
```

```text
lluvia 1 0 | 4/5 1/5
sol 1/2 1/2 | 0 1
```

::: exercise {#mkv-c4-ap-ej-contar title="Cuenta seis días"}
Anotaste lluvia, lluvia, sol, sol, sol, lluvia, con paraguas, paraguas, sin paraguas, paraguas, sin paraguas, paraguas. Calcula $\widehat P$ y $\widehat B$.
:::

::: hint {#mkv-c4-ap-pista-contar of="mkv-c4-ap-ej-contar" title="¿Pares o días?"}
¿Cuántos pares de días seguidos hay? ¿Cuántos días usas para $\widehat B$?
:::

::: answer {#mkv-c4-ap-resp-contar of="mkv-c4-ap-ej-contar"}
Cinco pares: $N(\text{lluvia})=2$ y $N(\text{sol})=3$. Filas de $\widehat P$: lluvia $(1/2,\ 1/2)$, sol $(1/3,\ 2/3)$. Seis días: lluvia en 3, siempre con paraguas; sol en 3, una vez con paraguas. Filas de $\widehat B$: lluvia $(1,\ 0)$, sol $(1/3,\ 2/3)$.
:::

Necesitas el clima para contar. ¿Y si nadie lo anotó?

---

## 2 · Aprender sin etiquetas

**Piensa: si no sabes qué clima hubo cada día, ¿qué cuentas?**

Cuentas con fracciones. Cada día reparte su unidad entre los estados, según cuánto crees que estuvo en cada uno. Esa es la idea de **Baum-Welch**.

> **Dado:** señales $o_0,\dots,o_T$ y un modelo inicial. **Encontrar:** $P$, $B$, $\mu_0$ que hagan más probables esas señales.

El ciclo tiene cuatro pasos:

- **Arranca con un modelo.** Elígelo como estimación inicial.
- **Reparte cada día.** El suavizado $b_{t\mid T}$ da la probabilidad de cada estado. Calcula también la de cada par de estados en días seguidos. Usa **toda** la secuencia, no solo hasta $t$.
- **Vuelve a contar.** Suma fracciones: son **conteos esperados**. Divide cada fila entre su total (@mkv-c4-def-contar).
- **Repite** con el modelo nuevo.

::: figure {#mkv-c4-fig-flujo-aprender title="El ciclo de Baum-Welch, en palabras"}
![Diagrama de flujo vertical de Baum-Welch. Arriba, «modelo de hoy: μ₀, P, B». Flecha a «reparte cada día y cada par de días entre los estados, con toda la secuencia». Flecha a «conteos esperados: fracciones en lugar de enteros». Flecha a «cuenta: cada fila entre su total». Flecha a «modelo nuevo». Un rombo pregunta si la verosimilitud dejó de subir; si no, una flecha regresa al modelo de hoy; si sí, termina. Al pie: cada vuelta no baja la verosimilitud, pero puede parar en un modelo que no es el mejor.](../_assets/mkv-c4-flujo-aprender.svg)
:::

**Un paso a mano.** Dos días: paraguas y luego sin paraguas. Fingimos no conocer el modelo y arrancamos con el de la página 2. Con dos días hay cuatro trayectorias. Su conjunta es el producto de la página 2. Cada peso es la conjunta entre la suma, $397/2000$:

::: table {#mkv-c4-ap-tabla-paso title="Las cuatro trayectorias de paraguas, sin paraguas"}
| # | Trayectoria | Conjunta | Peso |
|---|---|---:|---:|
| 1 | lluvia, lluvia | 63/2000 | 63/397 |
| 2 | lluvia, sol | 216/2000 | 216/397 |
| 3 | sol, lluvia | 6/2000 | 6/397 |
| 4 | sol, sol | 112/2000 | 112/397 |
:::

- **Fila 2:** $\tfrac12\cdot\tfrac9{10}\cdot\tfrac3{10}\cdot\tfrac8{10}=216/2000$. Es la trayectoria más probable dadas las dos señales.
- **Día 0, con toda la secuencia:** las filas 1 y 2 dan $b_{0\mid1}(\text{lluvia})=279/397\approx0.703$. El filtro daba $9/11\approx0.818$. «Sin paraguas» del día 1 reduce la probabilidad de lluvia del día 0.
- **El día 1:** filas 1 y 3 dan lluvia $69/397$; filas 2 y 4, sol $328/397$.

**Vuelve a contar.** Lluvia→lluvia aporta $63/397$ y lluvia→sol, $216/397$. Total de salidas: $279/397$. Los $397$ se cancelan:

$$
\begin{aligned}
\widehat P(\cdot\mid\text{lluvia})&=\left(\tfrac{63}{279},\ \tfrac{216}{279}\right)=\left(\tfrac{7}{31},\ \tfrac{24}{31}\right),\\
\widehat P(\cdot\mid\text{sol})&=\left(\tfrac{6}{118},\ \tfrac{112}{118}\right)=\left(\tfrac{3}{59},\ \tfrac{56}{59}\right).
\end{aligned}
$$

Para $\widehat B$, cuenta lluvia con paraguas: $279/397$; sin paraguas: $69/397$. Para sol: $118/397$ y $328/397$:

$$
\begin{aligned}
\widehat B(\text{lluvia},\cdot)&=\left(\tfrac{93}{116},\ \tfrac{23}{116}\right),\\
\widehat B(\text{sol},\cdot)&=\left(\tfrac{59}{223},\ \tfrac{164}{223}\right).
\end{aligned}
$$

El nuevo inicio es el reparto del día 0: $(279/397,\ 118/397)$.

**La verosimilitud sube.** Pasa de $\Pr(O_{0:1})=397/2000\approx0.199$ a $268802881/669153424\approx0.402$. Su logaritmo pasa de $-1.617$ a $-0.912$.

**En Python.** Con pocos días se puede sumar sobre todas las trayectorias. Sumar los pesos de las que pasan por $s$ el día $t$ da $b_{t\mid T}(s)$. Con muchos días, eso se calcula con el suavizado de la página 4.

```python
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

def conjunta(hmm, tr, obs):
    P, B = hmm["P"], hmm["B"]
    p = hmm["mu0"][tr[0]] * B[tr[0]][obs[0]]
    for t in range(1, len(tr)):
        p *= P[tr[t - 1]][tr[t]] * B[tr[t]][obs[t]]
    return p

def paso(hmm, obs):
    E, O = hmm["estados"], hmm["señales"]
    todas = list(product(E, repeat=len(obs)))
    vero = sum(conjunta(hmm, tr, obs) for tr in todas)
    ini = {s: F(0) for s in E}
    NP = {s: {s2: F(0) for s2 in E} for s in E}
    NB = {s: {o: F(0) for o in O} for s in E}
    for tr in todas:
        w = conjunta(hmm, tr, obs) / vero  # peso
        ini[tr[0]] += w
        for s, s2 in zip(tr, tr[1:]):
            NP[s][s2] += w                 # pares
        for s, o in zip(tr, obs):
            NB[s][o] += w                  # días
    nuevo = dict(hmm, mu0=ini)
    nuevo["P"] = {s: {k: n / sum(f.values())
                      for k, n in f.items()}
                  for s, f in NP.items()}
    nuevo["B"] = {s: {k: n / sum(f.values())
                      for k, n in f.items()}
                  for s, f in NB.items()}
    return nuevo, vero

nuevo, antes = paso(paraguas, [C, N])
_, despues = paso(nuevo, [C, N])
for s in ["lluvia", "sol"]:
    print(s, *nuevo["P"][s].values(), "|",
          *nuevo["B"][s].values())
print(antes, despues)
```

```text
lluvia 7/31 24/31 | 93/116 23/116
sol 3/59 56/59 | 59/223 164/223
397/2000 268802881/669153424
```

::: remark {#mkv-c4-obs-baum-welch title="Lo que garantiza Baum-Welch y lo que no"}
**Condición.** El modelo inicial da verosimilitud positiva a las señales.

- **Sí garantiza:** la verosimilitud no baja (Baum, Petrie, Soules y Weiss, 1970). Al repetir con los mismos dos días, sube a $0.666$, $0.943$ y $0.999$.
- **No garantiza el mejor modelo:** puede terminar en un máximo local o un punto fijo que no sea óptimo.
- **No garantiza los nombres:** intercambiar las filas iniciales de $B$ en el paraguas intercambia lluvia y sol en el resultado. El nombre «lluvia» no asegura que llueva.
- **Depende del inicio:** dos inicios pueden dar modelos distintos.
:::

- **Memorizar dos días.** Acercarse a 1 indica ajuste a dos señales, no que recuperaste el clima. Con pocos datos, puedes sobreajustar.
- **De dónde viene el nombre.** Lleva el nombre de Leonard Baum y Lloyd Welch, del Institute for Defense Analyses (IDA) de Princeton. Welch no firma los artículos de 1966 a 1972. Es un caso del algoritmo EM (*expectation–maximization*, esperanza–maximización) de Dempster, Laird y Rubin (1977), que llegó después y lo generalizó.
- **Vocales sin etiquetas.** En 1980, Cave y Neuwirth, en actas internas del IDA, ajustaron un modelo de dos estados a texto en inglés sin decirle qué era vocal. Un estado salió con las vocales y el otro con las consonantes. Su texto abre citando a Markov, que en 1913 había contado esas clases a mano en el *Oneguin*.

::: exercise {#mkv-c4-ap-ej-filas-iguales title="Arranca con filas iguales"}
En el paraguas, haz las dos filas de $B$ iguales a $(1/2,\ 1/2)$. Observas paraguas, sin paraguas. ¿Qué pesos tienen las cuatro trayectorias? ¿Qué modelo obtienes tras el paso?
:::

::: hint {#mkv-c4-ap-pista-filas-iguales of="mkv-c4-ap-ej-filas-iguales" title="¿Distingue algo la señal?"}
Con las dos filas de $B$ iguales, ¿qué factor de la conjunta depende del clima?
:::

::: answer {#mkv-c4-ap-resp-filas-iguales of="mkv-c4-ap-ej-filas-iguales"}
Cada conjunta es $\tfrac12\cdot\tfrac12\cdot P(s'\mid s)\cdot\tfrac12$; suman $1/4$. Los pesos son $7/20$, $3/20$, $3/20$ y $7/20$. El día 0 queda en $(1/2,\ 1/2)$, igual que el día 1. Obtienes **el mismo modelo**, con verosimilitud $1/4$. Desde el paraguas, un paso dio $0.402$. El inicio importa.
:::

---

## Ejercicios

::: exercise {#mkv-c4-ap-ej-helado title="Cuenta los helados anotados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** hay tres señales posibles; $\widehat B$ es de $2\times3$. El registro es inventado.

Un diario registra seis días. Clima: calor, calor, frío, frío, calor, calor. Helados: tres, dos, uno, dos, tres, tres.

1. **Cuenta transiciones:** escribe $N(s,s')$ y $N(s)$ para calor y frío.
2. **Cuenta emisiones:** escribe $N(s,o)$ y cuántos días aparece cada clima.
3. **Estima:** calcula $\widehat P$ y $\widehat B$, en el orden calor, frío y uno, dos, tres helados.
4. **Revisa los ceros:** ¿qué celdas valen 0? ¿Indican imposibilidad o falta de datos?
5. **Recorta:** usa calor, calor, calor, frío y dos, tres, tres, uno helados. ¿Qué fila no puedes estimar? ¿Puedes estimar la de frío de $\widehat B$?
:::

::: hint {#mkv-c4-ap-pista-helado-1 of="mkv-c4-ap-ej-helado" title="Pista 1 · ¿Qué recorres para cada tabla?"}
¿Cuentas pares de días seguidos o días sueltos? ¿Cuántos hay de cada uno en seis días?
:::

::: hint {#mkv-c4-ap-pista-helado-2 of="mkv-c4-ap-ej-helado" title="Pista 2 · ¿Tus filas suman 1?"}
¿Cada fila estimada suma 1? En el registro recortado, ¿cuántas salidas tiene el último clima?
:::

::: answer {#mkv-c4-ap-resp-helado of="mkv-c4-ap-ej-helado" title="Respuesta · Dos tablas de conteo con tres señales"}
**1. Cuenta transiciones.** Cinco pares: calor→calor 2, calor→frío 1, frío→frío 1, frío→calor 1. $N(\text{calor})=3$ y $N(\text{frío})=2$.

**2. Cuenta emisiones.** Calor, 4 días: uno 0, dos 1, tres 3. Frío, 2 días: uno 1, dos 1, tres 0.

**3. Estima.**

$$
\begin{aligned}
\widehat P&=\begin{pmatrix}2/3&1/3\\1/2&1/2\end{pmatrix},\\
\widehat B&=\begin{pmatrix}0&1/4&3/4\\1/2&1/2&0\end{pmatrix}.
\end{aligned}
$$

**4. Revisa los ceros.** $\widehat B(\text{calor},\text{un helado})=0$ y $\widehat B(\text{frío},\text{tres helados})=0$. Solo dicen que en seis días no se vio. Un modelo con esos ceros declara imposible un día de calor con un helado.

**5. Recorta.** Frío aparece al final: $N(\text{frío})=0$. No puedes estimar su fila de $\widehat P$. La de calor es $(2/3,\ 1/3)$. Sí estimas la fila de frío de $\widehat B$: $(1,\ 0,\ 0)$. Para $\widehat B$ basta aparecer; para $\widehat P$ necesitas salidas.
:::

**Punto de control:** debes poder hacer cuatro cosas.

- **Estimar** $\widehat P$ y $\widehat B$ contando, bajo la condición de cada fila.
- **Explicar** por qué $\widehat B$ divide entre días y $\widehat P$ entre salidas.
- **Dar un paso** de Baum-Welch con dos días: pesos, conteos esperados y modelo nuevo.
- **Decir** qué no garantiza Baum-Welch.

---

## Lo que hay que llevarse

- **Con etiquetas se cuenta** (@mkv-c4-def-contar). $\widehat P$ usa pares; $\widehat B$, días. En la semana: $\widehat P$ tiene filas $(1,0)$ y $(1/2,1/2)$; $\widehat B$, $(4/5,1/5)$ y $(0,1)$.
- **Cada fila necesita datos.** Sin salidas, no estimas la fila de $\widehat P$. El código deja ceros.
- **Sin etiquetas, Baum-Welch:** suaviza, cuenta fracciones y repite. En dos días, la probabilidad de lluvia del día 0 pasa a $279/397\approx0.703$, y $\widehat P(\cdot\mid\text{lluvia})=(7/31,\ 24/31)$.
- **La verosimilitud no baja:** pasa de $397/2000\approx0.199$ a $\approx0.402$ (@mkv-c4-obs-baum-welch).
- **El mejor modelo no está garantizado:** hay máximos locales, nombres intercambiados y dependencia del inicio. Con filas iguales en $B$, el modelo queda igual.

Si los estados son clases de palabras y las señales son palabras, ¿qué genera y predice este modelo?

Continúa con [[mkv-lenguaje-pequeno|Un modelo de lenguaje pequeño]].
