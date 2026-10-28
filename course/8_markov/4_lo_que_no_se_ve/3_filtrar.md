---
id: mkv-filtrar
title: "Filtrar y predecir"
nav_title: "Filtrar"
summary: "Predecir con P, corregir con Bayes y normalizar: la creencia día por día, y la señal de mañana."
status: ready
estimated_time: 28m
tags: [markov, ocultas, filtrar, creencia]
---

# Filtrar y predecir

**Si no veo el clima, ¿cuánto creo que llueve hoy?**

Al terminar tendrás:

- **La creencia, en general:** $b_t(s)=\Pr(S_t=s\mid O_{0:t})$, un estado de información y no el clima.
- **Un paso del filtro:** predecir con $P$, corregir con Bayes y normalizar. El teorema indica cuándo.
- **El algoritmo FILTRAR:** pseudocódigo, versión en Python y una traza con $b_0(\text{lluvia})=9/11$ y $b_1(\text{lluvia})=621/703$.
- **La señal de mañana y la verosimilitud:** $703/1100$ de probabilidad de ver paraguas; $24089/200000$ como producto de evidencias.
- **Un cuidado:** en el modelo del paraguas, la creencia olvida su inicio. No ocurre en cualquier modelo.

## Lo que traes

- **Avanzar una distribución.** En [[mkv-cadena-en-general|La cadena en general]] viste $\mu_{t+1}=\mu_tP$ (@mkv-c1-teo-predecir). Ese producto permite predecir.
- **Bayes y normalizar.** En [[mkv-bayes-y-normalizar|Bayes y normalizar]] multiplicaste prior por verosimilitud y dividiste entre la suma (@mkv-c4-teo-bayes, @mkv-c4-def-normalizar). Con paraguas y prior $(1/2,1/2)$ obtuviste $9/11$.
- **El modelo.** En [[mkv-el-modelo-oculto|El modelo oculto]] definiste $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ (@mkv-c4-def-hmm) y el diccionario `paraguas`. Calculaste la verosimilitud $24089/200000$ al sumar 8 trayectorias.
- **Olvidar el inicio.** En [[mkv-olvida-su-inicio|Olvida su inicio]] la distribución de una cadena dejó de depender de $\mu_0$.
- **Qué $b$ usa esta página.** $b_t$ es la creencia del día $t$ dadas las señales recibidas. $b_{t+1\mid t}$ es la predicción antes de ver la señal $t+1$.

---

## 1 · Plantear el problema en general

**Piensa: si solo ves señales, ¿cómo describes lo que sabes del estado de hoy?**

Con una distribución sobre los estados, dadas las señales. Asigna una probabilidad a cada estado posible.

::: definition {#mkv-c4-def-creencia title="La creencia"}
$$
\begin{aligned}
&b_t(s)=\Pr(S_t=s\mid O_{0:t}=o_{0:t}),\\
&\textstyle\sum_{s\in\mathcal S}b_t(s)=1,\qquad t=0,1,\dots,T.
\end{aligned}
$$

- **Qué es:** un vector fila con una entrada por estado, como $\mu_0$. Sus entradas son $\ge0$ y suman 1.
- **Cómo se calcula:** con el modelo y las señales $o_0,\dots,o_t$. Esa secuencia debe tener probabilidad positiva.
- **Qué significa:** lo que sabes del estado de hoy dadas las señales. $t$ empieza en 0: por eso $b_0$ ya usa la primera señal.
- **Qué no es:** el estado físico. Es un **estado de información**. En la semana simulada de [[mkv-el-modelo-oculto|El modelo oculto]], el día 6 llovió. Con las siete señales, $b_6(\text{lluvia})\approx0.194$.
:::

- **Aviso de letra.** $b$ es la creencia. $B$ es la matriz de emisión. $b_t$ suma 1; una columna de $B$ no tiene por qué hacerlo.
- **Aviso de índice.** $b_{t+1\mid t}$ predice el estado del día $t+1$ con señales hasta el día $t$. Aún no usa $o_{t+1}$.

::: table {#mkv-c4-fi-tabla-notacion title="Los símbolos del filtro"}
| Símbolo | Se lee | Qué es |
|---|---|---|
| $O_{0:t}$ | «o de cero a te» | Las señales $O_0,\dots,O_t$ |
| $b_t(s)$ | «be sub te de ese» | La creencia del día $t$; en el paraguas, $b_0(\text{lluvia})=9/11$ |
| $b_{t+1\mid t}(s)$ | «be de te más uno dado te» | La predicción $b_tP$, sin la señal nueva; $b_{1\mid0}(\text{lluvia})=69/110$ |
| $w_t(s)$ | «doble u sub te de ese» | El peso antes de normalizar, como en @mkv-c4-def-normalizar |
| $\operatorname{ev}_t$ | «evidencia sub te» | La suma de los pesos $w_t$; en el paraguas, $\operatorname{ev}_0=11/20$ |
:::

> **Dado:** un modelo $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ y las señales $o_0,\dots,o_T$, que llegan una por día.
>
> **Encontrar:** $b_t$ para cada $t$, con $b_{t-1}$ y la señal nueva. Sin revisar todo el pasado.

> [!TIP]
> **Ejemplo y contraejemplo de la creencia.**
>
> - **Lo cumple:** con paraguas el día 0, $b_0=\begin{pmatrix}9/11&2/11\end{pmatrix}$. Divide los pesos $9/20$ y $2/20$ entre $11/20$. El resultado suma 1.
> - **No lo cumple:** el clima real del día 6 de la semana simulada, $\begin{pmatrix}1&0\end{pmatrix}$: llovió. Un $(1,0)$ puede ser una creencia, pero no es la que dan las siete señales de esa semana: esa es $\approx\begin{pmatrix}0.194&0.806\end{pmatrix}$.

::: figure {#mkv-c4-fig-ej-creencia title="Ejemplo y contraejemplo: una creencia"}
![Dos paneles con barras de lluvia y sol. Arriba, el que cumple: la creencia del día 0 tras ver paraguas, lluvia 9/11 ≈ 0.818 y sol 2/11 ≈ 0.182; las barras suman 1 y salen de μ₀ y de la señal. Abajo, el que no: el clima real del día 6 de la semana simulada, lluvia 1 y sol 0, en barras con borde punteado y marcado como oculto; debajo, en gris, la creencia de ese día con las siete señales, lluvia ≈ 0.194 y sol ≈ 0.806.](../_assets/mkv-c4-ej-creencia.svg)
:::

::: exercise {#mkv-c4-fi-ej-sumas title="Suma la creencia y la columna"}
Con paraguas el día 0, ¿cuánto suman $b_0(\text{lluvia})+b_0(\text{sol})$? ¿Y $B(\text{lluvia},\text{paraguas})+B(\text{sol},\text{paraguas})$?
:::

::: hint {#mkv-c4-fi-pista-sumas of="mkv-c4-fi-ej-sumas" title="¿Qué suma cada una?"}
¿Cuál es una distribución y cuál reúne probabilidades condicionadas a estados distintos?
:::

::: answer {#mkv-c4-fi-resp-sumas of="mkv-c4-fi-ej-sumas"}
La creencia suma $9/11+2/11=1$. Reparte probabilidad entre estados. La columna suma $9/10+2/10=11/10$. Reúne entradas de dos filas de $B$, una por clima.
:::

¿Cómo pasas de $b_t$ a $b_{t+1}$ cuando llega una señal nueva?

---

## 2 · Avanzar un paso: predecir y corregir

**Piensa: mañana el clima puede cambiar y llegará otra señal. ¿Qué haces primero?**

Primero predices con $P$. Luego corriges con Bayes al ver la señal nueva. Ya conoces estas dos herramientas.

- **Predecir.** $b_{t+1\mid t}=b_tP$. Aplicas $\mu_{t+1}=\mu_tP$, de la clase 1, con $b_t$ en lugar de $\mu_t$.
- **Corregir.** La predicción es el prior. Multiplica por la verosimilitud $B(s,o_{t+1})$ y normaliza los pesos.

::: theorem {#mkv-c4-teo-filtrar title="El filtrado recursivo"}
**Condición.** Usa un modelo como en @mkv-c4-def-hmm y señales $o_0,\dots,o_T$ con $\Pr(O_{0:T}=o_{0:T})>0$. Esto equivale a exigir que cada evidencia $\operatorname{ev}_t$ sea positiva.

$$
\begin{aligned}
b_0(s)&=\mu_0(s)\,B(s,o_0)\,/\,\operatorname{ev}_0,\\
b_{t+1\mid t}(s')&=\textstyle\sum_{s}b_t(s)\,P(s'\mid s),\\
b_{t+1}(s')&=b_{t+1\mid t}(s')\,B(s',o_{t+1})\,/\,\operatorname{ev}_{t+1}.
\end{aligned}
$$

Cada $\operatorname{ev}_t$ suma los pesos del día: $\operatorname{ev}_t=\sum_s w_t(s)$.

**Lectura.** Predice, corrige y normaliza. El costo por día no aumenta con el tiempo.

**Casos nulos.** Un estado con $b_{t+1\mid t}(s')=0$ conserva probabilidad 0 tras corregir. Si $\operatorname{ev}_{t+1}=0$, el modelo considera imposible la señal. No puedes normalizar. La creencia no está definida y la verosimilitud de las señales vale 0.
:::

::: proof {#mkv-c4-dem-filtrar of="mkv-c4-teo-filtrar"}
**Predecir.** Aplica probabilidad total sobre $S_t$, dado $O_{0:t}$. El primer supuesto de @mkv-c4-def-hmm permite usar $P$ para la transición:

$$
\begin{aligned}
&\Pr(S_{t+1}=s'\mid O_{0:t})\\
&\quad=\textstyle\sum_s\Pr(S_t=s\mid O_{0:t})\,P(s'\mid s).
\end{aligned}
$$

**Corregir.** Aplica Bayes (@mkv-c4-teo-bayes), dado $O_{0:t}$. El prior es $b_{t+1\mid t}$. El segundo supuesto de @mkv-c4-def-hmm da la verosimilitud $B(s',o_{t+1})$. Divide entre $\operatorname{ev}_{t+1}$, que debe ser positivo. El día 0 usa el prior $\mu_0$.
:::

**En el paraguas.** Con paraguas el día 0, $b_0(\text{lluvia})=9/11$. Es el Bayes de la página 1. Ahora predice el clima:

$$
\begin{aligned}
b_{1\mid0}(\text{lluvia})&=\tfrac{9}{11}\cdot\tfrac{7}{10}+\tfrac{2}{11}\cdot\tfrac{3}{10}=\tfrac{69}{110},\\
b_{1\mid0}(\text{sol})&=\tfrac{41}{110}.
\end{aligned}
$$

- **Predecir modera.** La probabilidad de lluvia baja de $9/11\approx0.818$ a $69/110\approx0.627$. En este modelo, $P$ acerca la creencia a $(1/2,1/2)$.
- **Corregir con paraguas sube.** Con paraguas el día 1, los pesos son $\tfrac{69}{110}\cdot\tfrac{9}{10}$ y $\tfrac{41}{110}\cdot\tfrac{2}{10}$. Al normalizar obtienes $b_1(\text{lluvia})=621/703\approx0.883$.

> [!TIP]
> **Ejemplo y contraejemplo de la condición.**
>
> - **Lo cumple:** el modelo del paraguas con (paraguas, paraguas). Lluvia → lluvia 7/10, lluvia → paraguas 9/10, sol → paraguas 2/10. Con $P=\begin{pmatrix}7/10&3/10\\3/10&7/10\end{pmatrix}$, las evidencias son $\operatorname{ev}_0=11/20$ y $\operatorname{ev}_1=703/1100$. Las dos son positivas.
> - **No lo cumple:** un clima fijo con señales que lo revelan. Lluvia → lluvia 1, sol → sol 1; lluvia → paraguas 1, sol → sin paraguas 1. Con $P=B=\begin{pmatrix}1&0\\0&1\end{pmatrix}$ y (paraguas, sin paraguas), obtienes $b_0=(1,0)$ y $b_{1\mid0}=(1,0)$. Los pesos del día 1 son $(1\cdot0,\ 0\cdot1)=(0,0)$. Entonces $\operatorname{ev}_1=0$ y no puedes normalizar.

::: figure {#mkv-c4-fig-ej-filtrar title="Ejemplo y contraejemplo: el filtrado recursivo"}
![Dos paneles, cada uno con dos días: barras de la creencia, la flecha predecir y la flecha corregir. Arriba, el que cumple, el paraguas con paraguas y paraguas: día 0 con ev₀ = 11/20 y lluvia 9/11 ≈ 0.818, predecir la baja a 69/110 ≈ 0.627 y corregir, con ev₁ = 703/1100, la sube a 621/703 ≈ 0.883. Abajo, el que no, P = B = I con señales paraguas, sin paraguas: día 0 con ev₀ = 1/2 y lluvia 1, predecir la deja en 1, y sobre la flecha corregir se lee «ev₁ = 0»; la barra final aparece tachada con el letrero «señal imposible». Pie: la barra es Pr(lluvia); tachada, no se puede normalizar.](../_assets/mkv-c4-ej-filtrar.svg)
:::

> [!WARNING]
> **Error típico: predecir antes del día 0.** El día 0 usa $\mu_0$ como prior de $S_0$. **Predecir es para pasar de un día al siguiente.** Aquí el error no se nota: $\mu_0$ uniforme por esta $P$, cuyas columnas también suman 1, vuelve a dar $\mu_0$. En otro modelo, sí cambia.

::: exercise {#mkv-c4-fi-ej-otra-senal title="Corrige con la otra señal"}
Partes de $b_0(\text{lluvia})=9/11$. El día 1 tu compañero llega **sin** paraguas. ¿Cuánto vale $b_1(\text{lluvia})$?
:::

::: hint {#mkv-c4-fi-pista-otra-senal of="mkv-c4-fi-ej-otra-senal" title="¿Cambia la predicción?"}
¿La predicción $69/110$ depende de la señal del día 1? ¿Qué columna de $B$ usas ahora?
:::

::: answer {#mkv-c4-fi-resp-otra-senal of="mkv-c4-fi-ej-otra-senal"}
La predicción sigue siendo $(69/110,\ 41/110)$. Los pesos son $\tfrac{69}{110}\cdot\tfrac{1}{10}=\tfrac{69}{1100}$ y $\tfrac{41}{110}\cdot\tfrac{8}{10}=\tfrac{328}{1100}$. Al normalizar, $b_1(\text{lluvia})=69/397\approx0.174$.
:::

Ya sabes dar un paso. ¿Cómo lo repites día tras día sin perder la cuenta?

---

## 3 · Calcular con FILTRAR

**Piensa: si aplicas el filtro durante un mes, ¿qué debes guardar entre días?**

Solo la creencia de ayer. Con ella y la señal nueva calculas la de hoy. FILTRAR repite ese paso.

> **Dado:** un modelo $\langle\mathcal S,\mathcal O,\mu_0,P,B\rangle$ y las señales $o_0,\dots,o_T$.
>
> **Encontrar:** las creencias $b_0,\dots,b_T$ y las evidencias $\operatorname{ev}_0,\dots,\operatorname{ev}_T$.

### El mapa de FILTRAR

- **Qué calcula:** las creencias $b_0,\dots,b_T$, una por día, con @mkv-c4-teo-filtrar.
- **Qué guarda:** la creencia del día anterior, `b`; la predicción, `pred`; los pesos `w` y su suma `ev`.
- **Cómo avanza:** procesa un día por vuelta: predice, corrige y normaliza. El día 0 toma $\mu_0$ como predicción.
- **Qué devuelve:** las listas de creencias y evidencias. La última creencia da la probabilidad de lluvia hoy.
- **Garantía:** cada $b_t$ es exacta si toda $\operatorname{ev}_t>0$. Si una evidencia vale 0, se detiene con «señal imposible».
- **Costo:** cada día posterior al 0 hace $\lvert\mathcal S\rvert^2$ productos al predecir; todos hacen $\lvert\mathcal S\rvert$ al corregir. No aumenta con el tiempo.
- **Supuestos:** conoces el modelo: $\mu_0$, $P$ y $B$.

::: figure {#mkv-c4-fig-flujo-filtrar title="FILTRAR, en palabras"}
![Diagrama de flujo vertical de FILTRAR, en palabras. 1: Toma el primer día; la predicción es μ₀. 2: Corrige: multiplica la predicción de cada estado por la probabilidad de la señal de hoy en ese estado. 3: Suma los pesos; esa suma es la evidencia del día. 4, pregunta: ¿la evidencia es 0? Si sí, para con «señal imposible». Si no, 5: normaliza, divide cada peso entre la evidencia, y guarda la creencia de hoy. 6, pregunta: ¿quedan días? Si no, devuelve las creencias y las evidencias. Si sí, 7: predice, mueve la creencia con P, y regresa al paso 2 con la señal del día siguiente.](../_assets/mkv-c4-flujo-filtrar.svg)
:::

```text
INPUT   modelo ⟨𝒮, 𝒪, μ₀, P, B⟩; señales
        o_0, …, o_T.
OUTPUT  creencias b_0, …, b_T y
        evidencias ev_0, …, ev_T.

 1 function FILTRAR(modelo, o_0..o_T)
 2   creencias ← [ ], evidencias ← [ ]
 3   para t = 0, 1, …, T:
 4     si t = 0: pred(s) ← μ₀(s)
 5     si no: pred(s') ← Σ_s b(s) P(s'|s)
 6     w(s) ← pred(s) · B(s, o_t)
 7     ev ← Σ_s w(s)
 8     si ev = 0: error «señal imposible»
 9     b(s) ← w(s) / ev
10     agrega b a creencias y ev a evidencias
11   return creencias, evidencias
```

**Gemelo Python.** Usamos el diccionario `paraguas` de [[mkv-el-modelo-oculto|El modelo oculto]]. Cada `# (n)` indica la línea del pseudocódigo.

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

def filtrar(hmm, obs):
    E, P, B = hmm["estados"], hmm["P"], hmm["B"]
    creencias, evidencias = [], []                   # (2)
    for t, o in enumerate(obs):                      # (3)
        if t == 0:
            pred = dict(hmm["mu0"])                  # (4)
        else:
            pred = {s2: sum(b[s] * P[s][s2] for s in E)
                    for s2 in E}                     # (5)
        w = {s: pred[s] * B[s][o] for s in E}        # (6)
        ev = sum(w.values())                         # (7)
        if ev == 0:
            raise ValueError("señal imposible")      # (8)
        b = {s: w[s] / ev for s in E}                # (9)
        creencias.append(b)                          # (10)
        evidencias.append(ev)
    return creencias, evidencias                     # (11)

con, sin = "paraguas", "sin paraguas"
creencias, evidencias = filtrar(paraguas, [con, con, sin])
for t in range(3):
    print(t, creencias[t]["lluvia"], evidencias[t])
```

```text
0 9/11 11/20
1 621/703 703/1100
2 4593/24089 24089/70300
```

- **Líneas 4 y 5.** El día 0 copia $\mu_0$. Los demás días multiplica por $P$. Así el día 0 no se predice dos veces.
- **Línea 8.** Con el clima fijo del contraejemplo, el filtro se detiene el día 1:

```python
uno, cero = F(1), F(0)
fijo = {"estados": ["lluvia", "sol"],
        "señales": ["paraguas", "sin paraguas"],
        "mu0": {"lluvia": F(1, 2), "sol": F(1, 2)},
        "P": {"lluvia": {"lluvia": uno, "sol": cero},
              "sol": {"lluvia": cero, "sol": uno}},
        "B": {"lluvia": {"paraguas": uno, "sin paraguas": cero},
              "sol": {"paraguas": cero, "sin paraguas": uno}}}
try:
    filtrar(fijo, [con, sin])
except ValueError as e:
    print(e)
```

```text
señal imposible
```

**La traza, primer tramo: dos días con paraguas.** Cada fila representa un día. «Antes» muestra la predicción. «Después» muestra la creencia.

::: table {#mkv-c4-fi-tabla-traza-1 title="Traza de FILTRAR hasta el segundo paraguas"}
| # | Señal | Antes: lluvia | Después: $b_t(\text{lluvia})$ |
|---|---|---:|---:|
| 0 | paraguas | $1/2$, de $\mu_0$ | $9/11\approx0.818$ |
| 1 | paraguas | $69/110\approx0.627$ | $621/703\approx0.883$ |
:::

- **Fila 0:** «antes» es $\mu_0$. Corriges con Bayes, como en la página 1.
- **Fila 1:** al predecir, la probabilidad de lluvia baja a $0.627$. El segundo paraguas la sube a $0.883$, más que el primero. Aquí, dos señales iguales seguidas pesan más que una.

**Segundo tramo: llega un día sin paraguas.**

::: table {#mkv-c4-fi-tabla-traza-2 title="Traza de FILTRAR tras el primer día sin paraguas"}
| # | Señal | Antes: lluvia | Después: $b_t(\text{lluvia})$ |
|---|---|---:|---:|
| 2 | sin paraguas | $4593/7030\approx0.653$ | $4593/24089\approx0.191$ |
:::

- **Fila 2:** la predicción favorece la lluvia con $0.653$. La probabilidad de llegar sin paraguas es $1/10$ con lluvia y $8/10$ con sol. Al corregir, la lluvia baja a $0.191$.

::: figure {#mkv-c4-fig-filtrar-traza title="La creencia de lluvia, día por día"}
![Gráfica de la creencia de lluvia contra el día, 0 a 2, con las señales paraguas, paraguas y sin paraguas al pie. Para cada día, un punto hueco con la predicción y un punto lleno con la creencia, unidos por una flecha. Día 0: de 1/2 a 9/11 ≈ 0.818. Día 1: de 69/110 ≈ 0.627 a 621/703 ≈ 0.883. Día 2: de 4593/7030 ≈ 0.653 a 4593/24089 ≈ 0.191. Una línea punteada horizontal marca 1/2.](../_assets/mkv-c4-filtrar-traza.svg)
:::

La gráfica muestra el cambio en la probabilidad de lluvia. Los puntos huecos van antes de corregir. Los llenos, después.

::: exercise {#mkv-c4-fi-ej-costo title="Cuenta las multiplicaciones"}
¿Cuántos productos hace FILTRAR por día en el modelo del paraguas? ¿Cuántos hace en $T+1=30$ días? Compara con sumar todas las trayectorias, como en la página 2.
:::

::: hint {#mkv-c4-fi-pista-costo of="mkv-c4-fi-ej-costo" title="¿Qué líneas multiplican?"}
¿Cuántos productos hacen las líneas 5 y 6 con $\lvert\mathcal S\rvert=2$?
:::

::: answer {#mkv-c4-fi-resp-costo of="mkv-c4-fi-ej-costo"}
La línea 5 hace $2\cdot2=4$ productos y la línea 6 hace 2: son 6 por día. En 30 días son $2+29\cdot6=176$: el día 0 no predice. Hay $2^{30}\approx1.07\times10^{9}$ trayectorias, cada una con su propio producto.
:::

Ya tienes la creencia de hoy. ¿Qué dice de la señal de mañana?

---

## 4 · Predecir la señal de mañana

**Piensa: con lo que crees hoy, ¿qué tan probable es que mañana tu compañero llegue con paraguas?**

Predice la distribución del clima de mañana y multiplícala por $B$. Aplicas probabilidad total sobre los estados posibles.

$$
\begin{aligned}
&\Pr(O_{t+1}=o\mid O_{0:t})\\
&\quad=\textstyle\sum_{s'}b_{t+1\mid t}(s')\,B(s',o)=(b_tPB)(o).
\end{aligned}
$$

- **Desde $b_0$.** Con $b_{1\mid0}=(69/110,\ 41/110)$, la probabilidad de paraguas es $\tfrac{69}{110}\cdot\tfrac{9}{10}+\tfrac{41}{110}\cdot\tfrac{2}{10}=\tfrac{703}{1100}\approx0.639$. Sin paraguas, $397/1100$.
- **Es la evidencia de mañana.** La suma coincide con $\operatorname{ev}_1=703/1100$ en la traza. Es la probabilidad de la señal observada, dadas las anteriores.

**Por eso las evidencias dan la verosimilitud.** Por la regla del producto, multiplica la probabilidad de la primera señal por la de la segunda dada la primera. Continúa así con las demás:

::: remark {#mkv-c4-obs-verosimilitud title="La verosimilitud es el producto de las evidencias"}
**Condición.** Un modelo como en @mkv-c4-def-hmm y señales con $\Pr(O_{0:T}=o_{0:T})>0$.

$$
\begin{aligned}
&\Pr(O_{0:T}=o_{0:T})\\
&\quad=\textstyle\prod_{t=0}^{T}\Pr(O_t=o_t\mid O_{0:t-1})=\prod_{t=0}^{T}\operatorname{ev}_t.
\end{aligned}
$$

- **Lectura:** FILTRAR ya calcula cada factor. Para obtener la verosimilitud, solo faltan $T$ multiplicaciones.
- **Casos nulos:** si $\Pr(O_{0:T}=o_{0:T})=0$, hay un primer día $t$ con $\operatorname{ev}_t=0$. Ahí la verosimilitud ya vale 0 y los factores siguientes no existen: FILTRAR se detiene.
:::

Para las señales (paraguas, paraguas, sin paraguas):

$$
\begin{aligned}
&\tfrac{11}{20}\cdot\tfrac{703}{1100}\cdot\tfrac{24089}{70300}\\
&\quad=\tfrac{24089}{200000}\approx0.120.
\end{aligned}
$$

En la página 2 sumaste 8 trayectorias; aquí bastan tres factores:

```python
from math import prod

def predecir_señal(hmm, b):
    E, P, B = hmm["estados"], hmm["P"], hmm["B"]
    pred = {s2: sum(b[s] * P[s][s2] for s in E) for s2 in E}
    return {o: sum(pred[s] * B[s][o] for s in E)
            for o in hmm["señales"]}

b0 = filtrar(paraguas, [con])[0][0]
for o, p in predecir_señal(paraguas, b0).items():
    print(o, p)
print(prod(filtrar(paraguas, [con, con, sin])[1]))
```

```text
paraguas 703/1100
sin paraguas 397/1100
24089/200000
```

::: exercise {#mkv-c4-fi-ej-producto title="Multiplica las evidencias"}
Calcula $\Pr(\text{sin paraguas},\ \text{paraguas})$ como producto de dos evidencias.
:::

::: hint {#mkv-c4-fi-pista-producto of="mkv-c4-fi-ej-producto" title="¿Qué creencia deja el día 0?"}
¿Cuánto vale $b_0(\text{lluvia})$ sin paraguas? Predice y usa la columna de paraguas.
:::

::: answer {#mkv-c4-fi-resp-producto of="mkv-c4-fi-ej-producto"}
$\operatorname{ev}_0=\tfrac12\cdot\tfrac1{10}+\tfrac12\cdot\tfrac8{10}=\tfrac{9}{20}$ y $b_0(\text{lluvia})=1/9$. La predicción de lluvia es $31/90$. Entonces $\operatorname{ev}_1=\tfrac{31}{90}\cdot\tfrac{9}{10}+\tfrac{59}{90}\cdot\tfrac{2}{10}=\tfrac{397}{900}$. El producto es $\tfrac{9}{20}\cdot\tfrac{397}{900}=\tfrac{397}{2000}$.
:::

Partimos de $\mu_0=(1/2,1/2)$. ¿Qué cambia si usas otro inicio?

---

## 5 · Comparar dos inicios

**Piensa: tú empiezas seguro de que llueve y alguien más, de que hay sol. ¿Siguen en desacuerdo tras recibir las mismas señales?**

En el modelo del paraguas, la diferencia disminuye cada día.

Dos filtros reciben las señales paraguas, paraguas, sin paraguas, paraguas, paraguas. Uno parte de $\mu_0=(1,0)$ y el otro de $\mu_0=(0,1)$.

::: table {#mkv-c4-fi-tabla-inicios title="La creencia de lluvia desde dos inicios opuestos"}
| # | Señal | Desde lluvia | Desde sol |
|---|---|---:|---:|
| 0 | paraguas | $1$ | $0$ |
| 1 | paraguas | $21/23\approx0.913$ | $27/41\approx0.659$ |
| 2 | sin paraguas | $\approx0.199$ | $\approx0.139$ |
| 3 | paraguas | $\approx0.734$ | $\approx0.713$ |
| 4 | paraguas | $\approx0.868$ | $\approx0.864$ |
:::

- **Fila 0:** un prior de 1 no cambia con Bayes: cada filtro conserva su certeza.
- **Fila 1:** la predicción asigna probabilidad a los dos climas porque $P$ no tiene ceros. Las señales acercan las dos creencias.
- **Fila 4:** la diferencia bajó de 1 a $\approx0.004$.

**La condición, solo para el paraguas.** Todas las entradas de $P$ y de $B$ son positivas: la predicción mezcla los climas y ninguna señal descarta uno.

> [!WARNING]
> **Error típico: generalizarlo.** La tabla lo muestra con números; no lo demuestra. Y no pasa siempre: si $P$ es la identidad y las filas de $B$ son iguales, $b_t=\mu_0$ para siempre, porque $P$ no mezcla los climas. **Hay teoremas de estabilidad del filtro, y cada uno pide condiciones distintas.** En [[mkv-olvida-su-inicio|Olvida su inicio]] no había señales.

::: exercise {#mkv-c4-fi-ej-tercer-inicio title="Encuentra el tercer inicio"}
Con las mismas cinco señales y $\mu_0=(1/2,1/2)$, ¿dónde quedará $b_4(\text{lluvia})$ respecto a $0.864$ y $0.868$?
:::

::: hint {#mkv-c4-fi-pista-tercer-inicio of="mkv-c4-fi-ej-tercer-inicio" title="¿Qué pasa si condicionas en el día 0?"}
Con $\mu_0=(1/2,1/2)$, ¿cómo escribes $b_4(\text{lluvia})$ por probabilidad total sobre el clima del día 0?
:::

::: answer {#mkv-c4-fi-resp-tercer-inicio of="mkv-c4-fi-ej-tercer-inicio"}
Entre los dos. Por probabilidad total sobre $S_0$, $b_4$ es un promedio de las dos columnas, con pesos $\Pr(S_0=s\mid O_{0:4})$. FILTRAR da $b_4(\text{lluvia})\approx0.867$.
:::

---

## Ejercicios

::: exercise {#mkv-c4-fi-ej-tres-climas title="Filtra con tres climas"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** ahora hay tres climas: entre sol y lluvia está nublado. Como el nublado cubre los días grises, el sol trae paraguas con $1/10$ y no con $2/10$. Las señales siguen siendo paraguas y sin paraguas. Usa el orden (sol, nublado, lluvia):

- **El inicio:** $\mu_0=(1/3,\ 1/3,\ 1/3)$.
- **Cómo cambia:** desde sol, $(3/5,\ 3/10,\ 1/10)$. Desde nublado, $(1/4,\ 1/2,\ 1/4)$. Desde lluvia, $(1/10,\ 3/10,\ 3/5)$.
- **El paraguas:** con sol, $1/10$; con nublado, $1/2$; con lluvia, $9/10$.

Observas dos días con paraguas.

1. **Corrige el día 0:** escribe los pesos, $\operatorname{ev}_0$ y $b_0$.
2. **Predice:** calcula $b_{1\mid0}$.
3. **Corrige el día 1:** escribe los pesos, $\operatorname{ev}_1$ y $b_1$.
4. **Multiplica:** calcula $\Pr(\text{paraguas},\ \text{paraguas})$ con las evidencias.
5. **Compara:** contrasta $b_1(\text{lluvia})$ con el $621/703$ de dos climas. ¿Qué clima recibió parte de esa probabilidad?
:::

::: hint {#mkv-c4-fi-pista-tres-climas-1 of="mkv-c4-fi-ej-tres-climas" title="Pista 1 · ¿Cuántos términos tiene cada suma?"}
Con tres climas, ¿cuántos términos sumas en cada entrada de la predicción? ¿Cuántos pesos sumas para obtener la evidencia?
:::

::: hint {#mkv-c4-fi-pista-tres-climas-2 of="mkv-c4-fi-ej-tres-climas" title="Pista 2 · ¿Tus vectores suman lo que deben?"}
¿Suman 1 las entradas de $b_0$, de tu predicción y de $b_1$? ¿Tu $\operatorname{ev}_1$ queda entre las probabilidades de paraguas con sol y con lluvia?
:::

::: answer {#mkv-c4-fi-resp-tres-climas of="mkv-c4-fi-ej-tres-climas" title="Respuesta · Nublado se lleva una parte"}
**1. Corrige el día 0.** Los pesos son $\tfrac13\cdot\tfrac1{10}=\tfrac1{30}$, $\tfrac13\cdot\tfrac12=\tfrac16$ y $\tfrac13\cdot\tfrac9{10}=\tfrac3{10}$. Suman $\operatorname{ev}_0=1/2$. Entonces $b_0=(1/15,\ 1/3,\ 3/5)$.

**2. Predice.** Calcula con cada columna de $P$:

$$
\begin{aligned}
b_{1\mid0}(\text{sol})&=\tfrac1{25}+\tfrac1{12}+\tfrac3{50}=\tfrac{11}{60},\\
b_{1\mid0}(\text{nublado})&=\tfrac1{50}+\tfrac16+\tfrac9{50}=\tfrac{11}{30},\\
b_{1\mid0}(\text{lluvia})&=\tfrac1{150}+\tfrac1{12}+\tfrac9{25}=\tfrac{9}{20}.
\end{aligned}
$$

Las entradas suman $11/60+22/60+27/60=1$.

**3. Corrige el día 1.** Los pesos son $\tfrac{11}{600}$, $\tfrac{110}{600}$ y $\tfrac{243}{600}$. Suman $\operatorname{ev}_1=364/600=91/150$. Entonces $b_1=(11/364,\ 55/182,\ 243/364)\approx(0.030,\ 0.302,\ 0.668)$.

**4. Multiplica.** $\tfrac12\cdot\tfrac{91}{150}=\tfrac{91}{300}\approx0.303$.

**5. Compara.** La probabilidad de lluvia baja de $621/703\approx0.883$ a $243/364\approx0.668$. Nublado recibe $0.302$: produce paraguas la mitad de las veces. La comparación junta tres cambios: el estado nublado, $B(\text{sol},\text{paraguas})$ de $2/10$ a $1/10$ y seguir con lluvia de $7/10$ a $3/5$.
:::

**Punto de control:** comprueba estas cuatro habilidades.

- **Definir** la creencia $b_t$ y decir por qué no es el estado físico.
- **Dar un paso** del filtro: predecir con $P$, corregir con $B$ y normalizar si la evidencia es positiva.
- **Trazar** FILTRAR a mano en un modelo chico y reconocer una señal imposible.
- **Obtener** la distribución de la señal de mañana y la verosimilitud como producto de evidencias.

---

## Lo que hay que llevarse

- **La creencia** $b_t(s)=\Pr(S_t=s\mid O_{0:t})$ describe tu información. El día 6 de la semana simulada llovió, aunque $b_6(\text{lluvia})\approx0.194$ (@mkv-c4-def-creencia).
- **Un paso:** predice $b_{t+1\mid t}=b_tP$, corrige con $B(s,o_{t+1})$ y normaliza. El día 0 corriges $\mu_0$. Si la evidencia vale 0, la señal es imposible (@mkv-c4-teo-filtrar).
- **La traza:** con paraguas, paraguas, obtienes $b_0(\text{lluvia})=9/11$, $b_{1\mid0}=(69/110,\ 41/110)$ y $b_1(\text{lluvia})=621/703\approx0.883$. Sin paraguas al día siguiente, baja a $\approx0.191$.
- **La señal de mañana:** desde $b_0$, las probabilidades son $703/1100$ para paraguas y $397/1100$ para sin paraguas.
- **La verosimilitud:** multiplica las evidencias. $\tfrac{11}{20}\cdot\tfrac{703}{1100}\cdot\tfrac{24089}{70300}=24089/200000$. No necesitas enumerar trayectorias (@mkv-c4-obs-verosimilitud).
- **El inicio se olvida en el paraguas,** porque $P$ y $B$ no tienen ceros. No ocurre en todo modelo.

El filtro resume lo que sabes de cada día con las señales recibidas hasta entonces. ¿Cuál fue la secuencia completa de climas más probable?

Continúa con [[mkv-decodificar|Decodificar: Viterbi y suavizar]].
