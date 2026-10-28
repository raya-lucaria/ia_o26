---
id: mkv-el-modelo-oculto
title: "El modelo oculto"
nav_title: "El modelo oculto"
summary: "El problema de un estado que no se ve, primero en general y luego en el paraguas: estados, señales, P, B, la probabilidad conjunta y las cuatro preguntas que se le hacen."
status: ready
estimated_time: 28m
tags: [markov, ocultas, hmm]
---

# El modelo oculto

**Si la cadena se mueve donde no la ves y solo te llegan señales, ¿qué hay que escribir para razonar sobre ella?**

Al terminar tendrás:

- **El modelo, en general:** estados, señales, $\mu_0$, $P$ y $B$, con una tabla de símbolos.
- **El paraguas, con números:** $P$ y $B$ a mano, revisadas por filas, y una semana simulada.
- **Una cuenta:** la probabilidad conjunta de una trayectoria y sus señales como producto.
- **Un cuidado:** lo que se observa no es, en general, una cadena de Markov; en el paraguas, con la cuenta.
- **Cuatro preguntas:** qué preguntarle al modelo y dónde encontrar las respuestas.

## Lo que traes

- **La cadena.** En [[mkv-cadena-en-general|La cadena, en general]] escribiste $(\mathcal S,\mu_0,P)$. $\mu_0$ da la distribución inicial y cada fila de $P$ suma 1.
- **El producto de una trayectoria.** En [[mkv-el-problema-de-markov|El problema de Markov]] multiplicaste $\mu_0$ por una entrada de $P$ por paso: $\Pr(C,V,C,C,V)=4/33$. También sorteaste con MUESTREAR-FILA.
- **El agente que veía.** En [[mkv-el-mdp|El proceso de decisión de Markov]] el agente conocía su estado $S_t$. Aquí no lo ve.
- **Bayes.** En [[mkv-bayes-y-normalizar|Bayes y normalizar]] pasaste de $\Pr(\text{señal}\mid\text{estado})$ a $\Pr(\text{estado}\mid\text{señal})$.
- **El modelo de esta página.** Usamos $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$. Nadie decide: no hay acciones ni recompensas como en el MDP.

---

## 1 · Plantear el problema en general

**Piensa: si no ves el estado, ¿qué necesitas saber para razonar sobre él?**

Necesitas saber cómo cambia el estado y qué señal produce. Ya sabes escribir la cadena. Una segunda tabla da las probabilidades de las señales según el estado.

::: definition {#mkv-c4-def-hmm title="Modelo oculto de Markov (HMM)"}
$$
\begin{aligned}
&\langle\mathcal S,\ \mathcal O,\ \mu_0,\ P,\ B\rangle,\\
&B(s,o)=\Pr(O_t=o\mid S_t=s).
\end{aligned}
$$

- **Qué es:** cinco piezas.
  - **$\mathcal S$:** un conjunto finito de **estados**. No se ven.
  - **$\mathcal O$:** un conjunto finito de **señales**. Se ven.
  - **$\mu_0$:** la distribución del estado inicial, $\mu_0(s)=\Pr(S_0=s)$.
  - **$P(s'\mid s)$:** la probabilidad de pasar de $s$ a $s'$, como en la clase 1.
  - **$B(s,o)$:** la **emisión**. Es la probabilidad de ver $o$ dado $s$.
- **Cómo se calcula:** $P$ es de $\lvert\mathcal S\rvert\times\lvert\mathcal S\rvert$ y $B$ de $\lvert\mathcal S\rvert\times\lvert\mathcal O\rvert$. Sus entradas son $\ge0$. **Cada fila suma 1**, en $P$ y en $B$.
- **Qué significa:** dos supuestos para toda historia con probabilidad positiva:

$$
\begin{aligned}
&\Pr(S_{t+1}=s'\mid S_{0:t},O_{0:t})=P(s'\mid S_t),\\
&\Pr(O_t=o\mid S_{0:t},O_{0:t-1})=B(S_t,o).
\end{aligned}
$$

  El primero dice que el estado sigue una cadena de Markov. Las señales no cambian sus transiciones. El segundo dice que la señal depende solo del estado actual; en $t=0$, $O_{0:-1}$ es la historia vacía.
- **Qué no es:** $B(s,o)$ no es $\Pr(S_t=s\mid O_t=o)$. $B$ va del estado a la señal; invertirla pide Bayes y depende de $\mu_0$.
:::

- **Aviso de letras.** $O_t$ es la señal aleatoria del paso $t$; $o$, un valor concreto. Igual que $S_t$ y $s$.
- **Aviso de $P$.** Aquí $P(s'\mid s)$ es la matriz de la clase 1, sin acción. No es $P(s'\mid s,a)$ del MDP.
- **En otros textos** verás $A$ por $P$ y $\pi$ por $\mu_0$. Aquí $\pi$ representa la política.

::: table {#mkv-c4-mo-tabla-notacion title="La notación del modelo oculto, pieza por pieza"}
| Símbolo | Se lee | Qué es |
|---|---|---|
| $\mathcal S$ | «ese caligráfica» | Los estados; no se ven |
| $\mathcal O$ | «o caligráfica» | Las señales; se ven |
| $s$, $s'$ | «ese», «ese prima» | Un estado y el siguiente |
| $o$ | «o» | Una señal concreta |
| $S_t$ | «ese sub te» | El estado aleatorio en el paso $t$ |
| $O_t$ | «o sub te» | La señal aleatoria en el paso $t$ |
| $\mu_0$ | «mu cero» | La distribución de $S_0$ |
| $P(s'\mid s)$ | «pe de ese prima dado ese» | Pasar de $s$ a $s'$; cada fila suma 1 |
| $B(s,o)$ | «be de ese, o» | Ver $o$ desde $s$; cada fila suma 1 |
| $T$ | «te mayúscula» | El último paso: hay $T+1$ señales |
| $O_{0:T}$ | «o de cero a te» | Las señales $O_0,\dots,O_T$ |
| $\lvert\mathcal S\rvert$, $\lvert\mathcal O\rvert$ | «tamaño de…» | Cuántos estados y cuántas señales |
:::

- **Lectura:** las cinco piezas definen el modelo. $S_t$ y $O_t$ describen una corrida. Solo ves $O_{0:T}$.

**Anatomía de $B$.** Las filas son estados; las columnas, señales. **No tiene por qué ser cuadrada:** con 2 climas y 3 señales, $B$ es de $2\times3$. En $P$, ambos ejes son estados; en $B$, son distintos. En $B$, cada fila suma 1. Una columna de $B$ reúne probabilidades de una señal bajo distintos estados: no es una distribución.

> **Dado:** un modelo oculto $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ y las señales vistas $o_0,\dots,o_T$.
>
> **Encontrar:** qué puedes decir de los estados ocultos $S_0,\dots,S_T$. La sección 5 plantea cuatro preguntas concretas.

::: exercise {#mkv-c4-mo-ej-tamano title="Cuenta las celdas de B"}
Un modelo tiene 3 estados y 4 señales. ¿De qué tamaño son $P$ y $B$? ¿Cuántas sumas deben dar 1 en $B$?
:::

::: hint {#mkv-c4-mo-pista-tamano of="mkv-c4-mo-ej-tamano" title="¿Qué va en las filas?"}
¿Qué representa cada fila de $B$? ¿Y cada columna?
:::

::: answer {#mkv-c4-mo-resp-tamano of="mkv-c4-mo-ej-tamano"}
$P$ es de $3\times3$ y $B$ de $3\times4$, con 12 celdas. En $B$ deben sumar 1 sus 3 filas, una por estado. Las 4 columnas no tienen esa obligación.
:::

Veamos el modelo con números.

---

## 2 · Llenar el modelo con el paraguas

**Piensa: ¿cómo sabrías si llueve sin ver el cielo?**

Por lo que traen los demás. Usaremos este ejemplo toda la clase; lo adaptamos de Russell y Norvig. Trabajas en un sótano sin ventanas. No ves el clima: solo ves si tu compañero llega con paraguas.

**Estados y señales.** $\mathcal S=\{\text{lluvia},\text{sol}\}$ y $\mathcal O=\{\text{paraguas},\text{sin paraguas}\}$. Los dos tamaños son 2, así que aquí $B$ sí es cuadrada.

**El inicio.** Sin información inicial, usamos $\mu_0=(1/2,\ 1/2)$, en el orden lluvia, sol.

**El clima cambia.** Si hoy llueve, mañana llueve con 7/10 y sale el sol con 3/10. Si hoy hay sol, las probabilidades se invierten. **El clima tiende a seguir igual.**

**El compañero emite.** Con lluvia trae paraguas 9 de cada 10 días. Con sol, 2 de cada 10: es precavido. Filas en orden lluvia, sol. Columnas de $B$: paraguas, sin paraguas.

$$
\begin{aligned}
P&=\begin{pmatrix}7/10&3/10\\3/10&7/10\end{pmatrix},\\
B&=\begin{pmatrix}9/10&1/10\\2/10&8/10\end{pmatrix}.
\end{aligned}
$$

- **Una entrada de $B$:** $B(\text{sol},\text{paraguas})=2/10$. Fila de sol, columna de paraguas.
- **Las filas suman 1:** $9/10+1/10=1$ y $2/10+8/10=1$. Las columnas no: $9/10+2/10=11/10$.

::: figure {#mkv-c4-fig-hmm-grafo title="El paraguas como modelo oculto"}
![Grafo del modelo oculto del paraguas. Arriba, los dos estados ocultos, lluvia y sol, en nodos con borde punteado. Lluvia se queda con 7/10 y pasa a sol con 3/10; sol se queda con 7/10 y pasa a lluvia con 3/10. Abajo, las dos señales que se ven, paraguas y sin paraguas, en nodos con borde sólido. Flechas de emisión hacia abajo: de lluvia a paraguas 9/10 y a sin paraguas 1/10; de sol a paraguas 2/10 y a sin paraguas 8/10. Al pie, μ₀ = (1/2, 1/2).](../_assets/mkv-c4-hmm-grafo.svg)
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** el paraguas. De lluvia salen dos flechas de emisión: a paraguas con 9/10 y a sin paraguas con 1/10; suman 1. De sol salen 2/10 y 8/10; suman 1. Cada fila de $B=\begin{pmatrix}9/10&1/10\\2/10&8/10\end{pmatrix}$ es una distribución.
> - **No lo cumple:** la misma tabla copiada por columnas, $\begin{pmatrix}9/10&2/10\\1/10&8/10\end{pmatrix}$. De lluvia salen 9/10 a paraguas y 2/10 a sin paraguas: suman 11/10. De sol salen 1/10 y 8/10: suman 9/10. Ninguna fila es una distribución.

::: figure {#mkv-c4-fig-ej-modelo title="Ejemplo y contraejemplo: un modelo oculto"}
![Dos paneles con el mismo grafo del paraguas y su matriz B debajo. Arriba, el que cumple: de lluvia salen 9/10 a paraguas y 1/10 a sin paraguas, de sol 2/10 y 8/10; cada fila suma 1. Abajo, el que no: B copiada por columnas, de lluvia salen 9/10 y 2/10, que suman 11/10, y de sol 1/10 y 8/10, que suman 9/10; ninguna fila es una distribución.](../_assets/mkv-c4-ej-modelo.svg)
:::

> [!WARNING]
> **Error típico:** leer $B$ por columnas, como si diera el clima a partir del paraguas. **$B$ se lee por filas: da la probabilidad de cada señal según el clima.** Para invertir la pregunta necesitas Bayes.

**El modelo en Python.** Las cinco piezas van en un diccionario, como el MDP de la clase 3. `P[s][s2]` y `B[s][o]` se consultan por estado, sin acción:

```python
from fractions import Fraction as F

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

for s in paraguas["estados"]:      # cada fila suma 1
    fila_P = sum(paraguas["P"][s].values())
    fila_B = sum(paraguas["B"][s].values())
    print(s, fila_P, fila_B)
```

```text
lluvia 1 1
sol 1 1
```

**Las páginas siguientes usan este diccionario.** Python guarda `F(2, 10)` como `1/5`: es el mismo número.

**Una semana simulada.** Sortea $S_0$ con $\mu_0$ y su señal con la fila correspondiente de $B$. Después, sortea cada estado con su fila de $P$ y luego su señal. Usa MUESTREAR-FILA con un valor uniforme nuevo cada vez:

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

tray, obs = simular(paraguas, 6, semilla=2045)
for t in range(7):
    print(t, tray[t].ljust(6), obs[t])
```

```text
0 sol    sin paraguas
1 sol    sin paraguas
2 lluvia paraguas
3 lluvia paraguas
4 lluvia paraguas
5 lluvia paraguas
6 lluvia sin paraguas
```

- **Dos columnas, una oculta.** El clima está al centro. Solo ves las señales de la derecha.
- **El día 6 engaña.** Llovió y el compañero llegó sin paraguas. Pasa 1 de cada 10 días de lluvia: es $B(\text{lluvia},\text{sin paraguas})=1/10$.

::: exercise {#mkv-c4-mo-ej-tapar title="Adivina con la columna tapada"}
Tapa la columna del clima de la semana simulada. Con solo las señales, ¿qué días dirías que llovió? ¿En cuántos de los 7 aciertas?
:::

::: hint {#mkv-c4-mo-pista-tapar of="mkv-c4-mo-ej-tapar" title="¿Qué fila de B mirar?"}
Día por día, ¿qué clima hace más probable la señal que viste? Luego destapa y compara.
:::

::: answer {#mkv-c4-mo-resp-tapar of="mkv-c4-mo-ej-tapar"}
La regla «paraguas, lluvia; sin paraguas, sol» predice lluvia del día 2 al 5 y sol en 0, 1 y 6. Acierta 6 de 7: falla el día 6. Para mejorar, usa también $P$ y los días vecinos.
:::

Antes que la semana entera, tres días: ¿qué tan probable es un clima con sus señales?

---

## 3 · Calcular la probabilidad conjunta

**Piensa: ¿qué tan probable es que llueva, llueva y salga el sol, y que veas paraguas, paraguas y sin paraguas?**

Multiplica como en la clase 1, con un factor más por día: la probabilidad de la señal.

::: remark {#mkv-c4-obs-conjunta title="La probabilidad conjunta de una trayectoria y sus señales"}
**Condición.** Un modelo como en @mkv-c4-def-hmm, una trayectoria $s_0,\dots,s_T$ y señales $o_0,\dots,o_T$ de igual longitud.

$$
\begin{aligned}
&\Pr(S_{0:T}=s_{0:T},\ O_{0:T}=o_{0:T})\\
&\quad=\mu_0(s_0)B(s_0,o_0)\prod_{t=1}^{T}P(s_t\mid s_{t-1})\,B(s_t,o_t).
\end{aligned}
$$

- **De dónde sale:** aplica la regla del producto a $S_0$, $O_0$, $S_1$, $O_1$… El primer supuesto de @mkv-c4-def-hmm da cada transición con $P$. El segundo da cada señal con $B$.
- **Lectura:** hay $T$ factores de $P$, uno por transición, y $T+1$ de $B$, uno por día.
- **Casos nulos:** si una entrada usada vale 0, el producto vale 0. Esa trayectoria no puede producir esas señales.
:::

**En el ejemplo.** Lluvia, lluvia, sol con paraguas, paraguas, sin paraguas. Un factor por renglón:

::: table {#mkv-c4-mo-tabla-conjunta title="Los factores de lluvia, lluvia, sol con sus señales"}
| Día | Factor | Valor |
|---|---|---:|
| 0 | $\mu_0(\text{lluvia})$ | 1/2 |
| 0 | $B(\text{lluvia},\text{paraguas})$ | 9/10 |
| 1 | $P(\text{lluvia}\mid\text{lluvia})$ | 7/10 |
| 1 | $B(\text{lluvia},\text{paraguas})$ | 9/10 |
| 2 | $P(\text{sol}\mid\text{lluvia})$ | 3/10 |
| 2 | $B(\text{sol},\text{sin paraguas})$ | 8/10 |
:::

$$
\begin{aligned}
&\tfrac12\cdot\tfrac{9}{10}\cdot\tfrac{7}{10}\cdot\tfrac{9}{10}\cdot\tfrac{3}{10}\cdot\tfrac{8}{10}\\
&\quad=\tfrac{1701}{25000}\approx0.068.
\end{aligned}
$$

Calcula el mismo producto en Python. `verosimilitud` suma la conjunta de todas las trayectorias: $2^3=8$ para tres días.

```python
from itertools import product

def probabilidad_conjunta(hmm, tray, obs):
    P, B = hmm["P"], hmm["B"]
    p = hmm["mu0"][tray[0]] * B[tray[0]][obs[0]]
    for t in range(1, len(tray)):
        p *= P[tray[t - 1]][tray[t]] * B[tray[t]][obs[t]]
    return p

con, sin = "paraguas", "sin paraguas"
print(probabilidad_conjunta(paraguas,
      ["lluvia", "lluvia", "sol"], [con, con, sin]))

def verosimilitud(hmm, obs):      # suma sobre trayectorias
    todas = product(hmm["estados"], repeat=len(obs))
    return sum(probabilidad_conjunta(hmm, tr, obs)
               for tr in todas)

print(verosimilitud(paraguas, [con, con, sin]))
```

```text
1701/25000
24089/200000
```

- **Las señales solas.** Las 8 trayectorias cubren todos los casos sin traslaparse. Por probabilidad total, suman $\Pr(O_{0:2}=(\text{paraguas},\text{paraguas},\text{sin paraguas}))=24089/200000\approx0.120$.
- **Una de muchas.** Lluvia, lluvia, sol aporta $0.068$ de esos $0.120$: más de la mitad.

::: exercise {#mkv-c4-mo-ej-dos-dias title="Multiplica dos días"}
Calcula la conjunta de sol, lluvia con las señales sin paraguas, paraguas.
:::

::: hint {#mkv-c4-mo-pista-dos-dias of="mkv-c4-mo-ej-dos-dias" title="¿Cuántos factores?"}
Dos días: ¿cuántos factores de $B$ y cuántos de $P$?
:::

::: answer {#mkv-c4-mo-resp-dos-dias of="mkv-c4-mo-ej-dos-dias"}
Dos factores de $B$, uno de $P$ y el inicio $\mu_0$:

$$
\tfrac12\cdot\tfrac{8}{10}\cdot\tfrac{3}{10}\cdot\tfrac{9}{10}=\tfrac{27}{250}.
$$
:::

La conjunta incluye estados y señales. ¿Las señales solas forman una cadena?

---

## 4 · Revisar si las señales son una cadena

**Piensa: el paraguas de hoy depende del clima, que depende del clima de ayer. ¿Basta el paraguas de ayer para predecir el de hoy?**

No basta. El paraguas de anteayer informa sobre el clima de ayer, que influye en el de hoy. La cuenta va abajo, con fracciones exactas.

En una cadena de Markov, la señal de mañana dependería solo de la de hoy. Mantén hoy paraguas y cambia la señal de ayer:

```python
L = lambda obs: verosimilitud(paraguas, obs)
print(L([con, con, con]) / L([con, con]))
print(L([sin, con, con]) / L([sin, con]))
```

```text
46211/70300
24089/39700
```

Cada renglón divide la probabilidad de las tres señales entre la de las dos primeras. Es una condicional:

$$
\begin{aligned}
&\Pr(O_2=\text{paraguas}\mid\text{paraguas},\text{paraguas})\approx0.657,\\
&\Pr(O_2=\text{paraguas}\mid\text{sin paraguas},\text{paraguas})\approx0.607.
\end{aligned}
$$

Hoy es igual en los dos casos y la probabilidad cambia. **Las señales del paraguas no son una cadena de Markov.**

::: remark {#mkv-c4-obs-no-markov title="Lo que se observa no es, en general, una cadena de Markov"}
El estado $S_t$ sí es una cadena de Markov, por @mkv-c4-def-hmm. Las señales $O_t$, en general, no.

- **En el paraguas no lo son:** $46211/70300\ne24089/39700$.
- **En otros modelos sí:** si las filas de $B$ son iguales, o las de $P$, las $O_t$ son independientes. Si $B$ es la identidad, $O_t$ identifica a $S_t$ uno a uno y las señales copian la cadena.
:::

> [!WARNING]
> **Error típico:** «la señal sale de una cadena, así que también es una cadena». **No en general:** una sola señal no resume la memoria del estado oculto. Ni «nunca» ni «siempre»: depende del modelo completo, $P$ y $B$.

::: exercise {#mkv-c4-mo-ej-filas-iguales title="Iguala las filas de B"}
Cambia $B$ por dos filas iguales, $(1/2,\ 1/2)$. ¿Cuánto valen ahora las dos condicionales de arriba?
:::

::: hint {#mkv-c4-mo-pista-filas-iguales of="mkv-c4-mo-ej-filas-iguales" title="¿Importa el clima?"}
Con esas filas, ¿la probabilidad de ver paraguas cambia si llueve?
:::

::: answer {#mkv-c4-mo-resp-filas-iguales of="mkv-c4-mo-ej-filas-iguales"}
Las dos valen 1/2. La señal es un volado, sin importar el clima ni las señales anteriores. Son independientes, así que forman una cadena de Markov.
:::

Predecir las señales del paraguas requiere considerar el estado oculto. ¿Qué puedes preguntarle al modelo?

---

## 5 · Hacerle cuatro preguntas al modelo

**Piensa: ya tienes las señales de la semana; ¿qué quieres saber del clima que no viste?**

Cuatro, cada una con su algoritmo.

::: table {#mkv-c4-mo-tabla-preguntas title="Las cuatro preguntas a un modelo oculto"}
| Pregunta | Nombre | Qué se calcula |
|---|---|---|
| ¿Qué tan probable es lo que vi? | Verosimilitud | $\Pr(O_{0:T}=o_{0:T})$ |
| ¿En qué estado estoy hoy? | Filtrar | $\Pr(S_T=s\mid O_{0:T}=o_{0:T})$ |
| ¿Cuál fue la secuencia de estados? | Decodificar | La trayectoria con mayor probabilidad conjunta |
| ¿Cómo aprendo $P$ y $B$? | Aprender | $P$ y $B$ a partir de señales |
:::

Dónde se responde:

- **Verosimilitud.** Ya sumaste 8 trayectorias: $24089/200000$. Para muchos días hay demasiadas. El cálculo diario está en [[mkv-filtrar|Filtrar y predecir]].
- **Filtrar.** Estimar la probabilidad de lluvia hoy con las señales hasta hoy, en [[mkv-filtrar|Filtrar y predecir]].
- **Decodificar.** Encontrar la secuencia de climas más probable, en [[mkv-decodificar|Decodificar]].
- **Aprender.** Estimar $P$ y $B$ cuando nadie anotó el clima, en [[mkv-aprender-lo-oculto|Aprender un modelo oculto]].

La clase cierra con una quinta pregunta: **¿qué hago sin ver?** Decidir si llevas paraguas según tus creencias, en [[mkv-decidir-sin-ver|Decidir sin ver el estado]].

::: exercise {#mkv-c4-mo-ej-clasifica title="Clasifica cuatro preguntas"}
Clasifica cada caso entre las cuatro preguntas:

1. Con un año de señales, sin registros del clima, ¿cuánto vale $P(\text{lluvia}\mid\text{sol})$?
2. ¿Qué tan raro es ver paraguas cinco días seguidos?
3. Con lo visto hasta hoy, ¿llueve hoy?
4. ¿Cuál fue la secuencia completa del clima durante la semana?
:::

::: hint {#mkv-c4-mo-pista-clasifica of="mkv-c4-mo-ej-clasifica" title="¿Qué piden?"}
¿Pide la probabilidad de las señales, un estado, una trayectoria o el modelo?
:::

::: answer {#mkv-c4-mo-resp-clasifica of="mkv-c4-mo-ej-clasifica"}
1. Aprender. 2. Verosimilitud. 3. Filtrar. 4. Decodificar.
:::

---

## Ejercicios

::: exercise {#mkv-c4-mo-ej-helado title="Modela el helado"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Buscas el clima de un verano sin registros. Solo tienes un diario de los helados que alguien comió cada día: uno, dos o tres.

**Cambia una idea:** la señal tiene tres valores, no dos. Lo demás funciona como en el paraguas.

- **El clima:** calor o frío. El primer día hay calor con probabilidad 4/5.
- **Cómo cambia:** después de calor, sigue calor con 3/5 o frío con 2/5. Después de frío, cada uno con 1/2.
- **Los helados:** con calor, come uno, dos o tres con probabilidades 1/5, 2/5 y 2/5. Con frío, las probabilidades son 1/2, 2/5 y 1/10.

1. **Modela:** escribe $\mathcal S$, $\mathcal O$, $\mu_0$, $P$ y $B$, con el tamaño de cada matriz.
2. **Revisa:** comprueba que cada fila de $P$ y de $B$ suma 1. ¿Por qué no se pide lo mismo a las columnas de $B$?
3. **Multiplica:** calcula la probabilidad conjunta de calor, frío con tres helados, un helado.
4. **Suma:** calcula la conjunta de las otras trayectorias de dos días con esas señales. Súmalas todas. ¿Cuál de las cuatro preguntas contestaste?
:::

::: hint {#mkv-c4-mo-pista-helado-1 of="mkv-c4-mo-ej-helado" title="Pista 1 · ¿Qué nombra cada fila y cada columna?"}
¿Cuántos climas y cantidades de helado hay? ¿Qué representa cada fila de las matrices? ¿Y cada columna?
:::

::: hint {#mkv-c4-mo-pista-helado-2 of="mkv-c4-mo-ej-helado" title="Pista 2 · ¿Tu producto tiene los factores justos?"}
Para dos días, ¿usaste $\mu_0$ al inicio, un factor de $P$ y dos de $B$? ¿Cuántas trayectorias de dos días puedes formar con dos climas?
:::

::: answer {#mkv-c4-mo-resp-helado of="mkv-c4-mo-ej-helado" title="Respuesta · El helado, pieza por pieza"}
**1. Modela.** $\mathcal S=\{\text{calor},\text{frío}\}$ y $\mathcal O=\{1,2,3\}$ helados. $\mu_0=(4/5,\ 1/5)$. Filas en orden calor, frío:

$$
\begin{aligned}
P&=\begin{pmatrix}3/5&2/5\\1/2&1/2\end{pmatrix},\\
B&=\begin{pmatrix}1/5&2/5&2/5\\1/2&2/5&1/10\end{pmatrix}.
\end{aligned}
$$

$P$ es de $2\times2$ y $B$ de $2\times3$: dos climas, tres señales.

**2. Revisa.** Filas de $P$: $3/5+2/5=1$ y $1/2+1/2=1$. Filas de $B$: $1/5+2/5+2/5=1$ y $1/2+2/5+1/10=1$. Las columnas de $B$ no cumplen: la de un helado suma $7/10$. Cada fila distribuye la probabilidad entre señales dado un clima. Una columna mezcla dos climas.

**3. Multiplica.**

$$
\tfrac45\cdot\tfrac25\cdot\tfrac25\cdot\tfrac12=\tfrac{8}{125}.
$$

**4. Suma.** Calor, calor: $24/625$. Frío, calor: $1/500$. Frío, frío: $1/200$. Al sumar calor, frío:

$$
\tfrac{8}{125}+\tfrac{24}{625}+\tfrac{1}{500}+\tfrac{1}{200}=\tfrac{547}{5000}.
$$

Es $\Pr(O_0=3,\ O_1=1)\approx0.109$: la verosimilitud.
:::

**Punto de control:** debes poder hacer cuatro cosas.

- **Escribir** un modelo oculto como $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$, con filas que suman 1.
- **Calcular** la probabilidad conjunta de una trayectoria y sus señales mediante un producto.
- **Explicar** con una cuenta por qué las señales del paraguas no forman una cadena de Markov.
- **Identificar** cuál de las cuatro preguntas plantea un problema.

---

## Lo que hay que llevarse

- **El modelo oculto:** $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$. El estado cambia según $P$. Produce una señal diaria según su fila de $B$ (@mkv-c4-def-hmm).
- **$B$ se lee por filas:** estados por señales, no necesariamente cuadrada. Cada fila suma 1. Leerla por columnas es el contraejemplo.
- **El paraguas:** el clima sigue igual con 7/10 y cambia con 3/10; el compañero trae paraguas con 9/10 si llueve y con 2/10 si hay sol. Inicio: $\mu_0=(1/2,1/2)$.
- **La conjunta es un producto:** $\mu_0$, luego $P$ y $B$ por día. Lluvia, lluvia, sol con paraguas, paraguas, sin paraguas da $1701/25000\approx0.068$. La suma de las 8 trayectorias da $24089/200000\approx0.120$ (@mkv-c4-obs-conjunta).
- **Las señales no son, en general, una cadena:** depende de $P$ y $B$. En el paraguas, $46211/70300\approx0.657$ frente a $24089/39700\approx0.607$ (@mkv-c4-obs-no-markov).
- **Cuatro preguntas:** verosimilitud, filtrar, decodificar y aprender. Al final, qué hacer sin ver.

Si no veo el clima, ¿cuánto creo que llueve hoy?

Continúa con [[mkv-filtrar|Filtrar y predecir]].
