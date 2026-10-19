---
id: mkv-ajustar-contando
title: "Ajustar contando"
nav_title: "Ajustar contando"
summary: "Si solo tienes el texto: contar transiciones da la matriz que hace más probable lo observado. El algoritmo trazado en la frase, una simulación que recupera una matriz conocida, qué hacer con lo que nunca se vio y cuánta memoria aguantan los datos del Quijote."
status: ready
estimated_time: 38m
tags: [markov]
---

# Ajustar contando

**Si solo tienes el texto, ¿cómo sacas $\widehat P$, qué garantiza y dónde falla?**

Al terminar tendrás:

- **El algoritmo CONTAR-TRANSICIONES,** en pseudocódigo y en Python, trazado par por par en la frase.
- **La justificación del conteo:** maximiza la verosimilitud condicionada al inicio; las filas sin salidas quedan indeterminadas.
- **Una simulación** en la que contar recupera una matriz conocida, con su error.
- **El suavizado aditivo de conteos (Laplace)** para lo que nunca se vio, y lo que sesga.
- **La memoria del estado como decisión de modelado,** medida en el *Quijote*.

## Lo que traes

- **Probabilidad condicional.** En [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] estimaste ${\widehat{\Pr}(A\mid B)}$ con frecuencias.
- **La cadena.** En [[mkv-cadena-en-general|La cadena, en general]]: ${(\mathcal S,\mu_0,P)}$ (@mkv-c1-cadena), con ${P_{ij}=P(s_j\mid s_i)}$, $P$ de ${k\times k}$ y filas que suman 1. Ahí también está la probabilidad de una trayectoria, que aquí se lee al revés: los datos quedan fijos y $P$ cambia.
- **La frase y el muestreo.** En [[mkv-el-problema-de-markov|El problema de Markov]], «Con la iglesia hemos dado, Sancho»: tras vocal hubo vocal 2 de 11 veces; tras consonante, 2 de cada 3. MUESTREAR-FILA usa la fila acumulada y un uniforme $u$.

> **Modelo y datos.** El texto es una trayectoria observada. Suponer una cadena finita y homogénea permite ajustar una matriz; no demuestra cómo se produjo el texto.

---

## 1 · Pasar del texto a la matriz

**Piensa: ¿qué debes contar para llenar toda la matriz?**

Cada par (actual, siguiente) y las salidas de cada estado.

::: definition {#mkv-c1-conteos title="Conteos, salidas y matriz estimada"}
**Qué es.** Para $\mathcal S=\{s_1,\dots,s_k\}$ y una trayectoria $s_{i_0},\dots,s_{i_T}$, con $T\ge1$, definimos:

$$
\begin{aligned}
N(s_i,s_j)
&=\#\{t\in\{0,\dots,T-1\}:\\
&\qquad i_t=i,\ i_{t+1}=j\},\\
N(s_i)&=\sum_{j=1}^k N(s_i,s_j).
\end{aligned}
$$

$\#$ cuenta elementos; $i,j$ enumeran estados e $i_t$ identifica el visitado en el paso $t$. $T$ cuenta transiciones, no es la $T(s,a)$ de juegos.

**Cómo se calcula.** Suma 1 por cada par y divide cada fila entre sus salidas:

$$
\begin{aligned}
N&=\bigl(N(s_i,s_j)\bigr)\in\mathbb N^{k\times k},\\
\sum_{j=1}^kN(s_i,s_j)&=N(s_i),\\
\sum_{i=1}^k\sum_{j=1}^kN(s_i,s_j)&=T.
\end{aligned}
$$

Aquí $\mathbb N$ incluye el 0. Para ${N(s_i)>0}$:

$$
\begin{aligned}
\widehat P_{ij}
&=\widehat P(s_j\mid s_i)\\
&=\frac{N(s_i,s_j)}{N(s_i)}.
\end{aligned}
$$

**Qué significa.** Es la $P$ de @mkv-c1-cadena, estimada fila por fila con frecuencias; el gorro indica estimación. Cada fila estimada suma 1.

**Qué no es.** ${N(s_i)}$ cuenta salidas, no apariciones: el último estado no tiene sucesor. Si ${N(s_i)=0}$, la fila queda sin estimar.
:::

**En la frase.** `conlaiglesiahemosdadosancho` tiene 27 letras, ${T=26}$ transiciones y ${k=2}$ estados, V y C:

```text
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

::: table {#mkv-c1-tabla-conteos-frase title="Los conteos de la frase"}
| Desde | Hacia V | Hacia C | Salidas |
|---|---:|---:|---:|
| V | 2 | 9 | 11 |
| C | 10 | 5 | 15 |
:::

En el orden V, C:

$$
N=\begin{pmatrix}2&9\\10&5\end{pmatrix},
\qquad
\widehat P=\begin{pmatrix}
2/11&9/11\\
2/3&1/3
\end{pmatrix}.
$$

- **Fila C.** ${10/15}$ y ${5/15}$ se simplifican a ${2/3}$ y ${1/3}$.
- **Fila V.** Hay 12 vocales, pero la «o» final no tiene sucesor: ${N(V)=11}$.

::: exercise {#mkv-c1-ej-salidas title="Cuenta las salidas"}
Toma `conla`: C V C C V.

1. **Cuenta los pasos.** ¿Cuánto vale $T$?
2. **Cuenta las salidas.** Escribe ${N(V)}$, ${N(C)}$ y los cuatro conteos.
3. **Estima las filas.** ¿Cuáles puedes calcular?
:::

::: hint {#mkv-c1-pista-salidas of="mkv-c1-ej-salidas" title="Cuenta pares, no letras"}
¿Cuántos pares (actual, siguiente) forman cinco letras?
:::

::: answer {#mkv-c1-resp-salidas of="mkv-c1-ej-salidas"}
1. **Hay ${T=4}$ pasos.** Son C→V, V→C, C→C y C→V.
2. **Los conteos son** ${N(C,V)=2}$, ${N(C,C)=1}$, ${N(V,C)=1}$ y ${N(V,V)=0}$. Las salidas son ${N(C)=3}$ y ${N(V)=1}$.
3. **Se estiman las dos filas.** En el orden V, C, la fila C es ${(2/3,\ 1/3)}$; la fila V, ${(0,\ 1)}$. Esta última depende de un solo par.
:::

Ya sabes contar. ¿Por qué estos cocientes y no otros?

---

## 2 · Justificar por qué contar

**Piensa: ¿puede otra matriz hacer más probable la frase observada?**

No, bajo Markov y homogeneidad, con filas libres e inicio condicionado.

::: definition {#mkv-c1-verosimilitud title="La verosimilitud de una matriz"}
**Qué es.** La verosimilitud (*likelihood*) ${\mathcal L(P)}$ es la probabilidad de los datos observados, vista como función de $P$.

**Cómo se calcula.** Para $P\in[0,1]^{k\times k}$ estocástica por filas, bajo Markov y homogeneidad, condicionamos a $S_0=s_{i_0}$:

$$
\begin{aligned}
\mathcal L(P)
&=\prod_{t=0}^{T-1}P_{i_ti_{t+1}}\\
&=\prod_{i=1}^k\prod_{j=1}^kP_{ij}^{N(s_i,s_j)}.
\end{aligned}
$$

**Qué significa.** Los datos quedan fijos; cambia $P$. Agrupar transiciones iguales produce los exponentes; condicionar elimina $\mu_0(s_{i_0})$.

**Qué no es.** No es la probabilidad de que $P$ sea verdadera.
:::

El logaritmo conserva el máximo y separa la cuenta por filas:

$$
\log\mathcal L(P)
=\sum_{i=1}^k\sum_{j=1}^kN(s_i,s_j)\log P_{ij}.
$$

Se omiten términos con conteo 0; asignar probabilidad 0 a un par observado da ${\log\mathcal L(P)=-\infty}$.

::: theorem {#mkv-c1-teo-maximo title="Contar da la matriz más verosímil"}
En una cadena finita y homogénea, condicionamos a $S_0=s_{i_0}$ y dejamos libres las filas de $P\in[0,1]^{k\times k}$.

Para cada fila $i$:

$$
\begin{aligned}
\text{maximizar}\quad
&\sum_{j=1}^kN(s_i,s_j)\log P_{ij}\\
\text{sujeto a}\quad
&\sum_{j=1}^kP_{ij}=1,\\
&P_{ij}\ge0,\qquad j=1,\dots,k.
\end{aligned}
$$

Si ${N(s_i)>0}$, la solución es:

$$
P_{ij}=\widehat P_{ij}
=\frac{N(s_i,s_j)}{N(s_i)}.
$$

Si ${N(s_i)=0}$, cualquier fila de probabilidades da el mismo máximo: los datos no la determinan.
:::

**Por qué.** Con $\lambda_i$ el multiplicador de la restricción de suma, como en [[el-multiplicador|El multiplicador]], para los conteos positivos:

$$
\begin{aligned}
\frac{N(s_i,s_j)}{P_{ij}}-\lambda_i&=0,\\
P_{ij}&=\frac{N(s_i,s_j)}{\lambda_i},\\
\sum_jP_{ij}=1
&\ \Longrightarrow\ \lambda_i=N(s_i).
\end{aligned}
$$

- **Conteo 0 con salidas.** Asignarle masa la quita a los pares observados; el máximo le asigna 0.
- **Máximo global.** La suma de logaritmos ponderados es cóncava.
- **Inicio condicionado.** Si la distribución inicial dependiera de $P$ y no condicionáramos, su factor podría cambiar el máximo.

**En la frase:**

$$
\begin{aligned}
\mathcal L(\widehat P)
&=\left(\tfrac{2}{11}\right)^2
  \left(\tfrac{9}{11}\right)^9\\
&\quad\cdot\left(\tfrac{2}{3}\right)^{10}
  \left(\tfrac{1}{3}\right)^5\\
&\approx3.88\times10^{-7}.
\end{aligned}
$$

- **Filas de ½.** Dan ${(1/2)^{26}\approx1.49\times10^{-8}}$; $\widehat P$ hace la frase 26 veces más probable.
- **Matriz cercana.** Con filas ${(0.181,\ 0.819)}$ y ${(0.710,\ 0.290)}$ da ${\approx3.63\times10^{-7}}$. $\widehat P$ alcanza 1.07 veces ese valor.

**A mano, la fila V.** Aporta ${p^2(1-p)^9}$, con ${p=P(V\mid V)}$ y ${1-p=P(C\mid V)}$:

$$
\begin{gathered}
\frac{d}{dp}[2\log p+9\log(1-p)]\\
=\frac{2}{p}-\frac{9}{1-p}=0,\\
\Longrightarrow\quad p=\frac{2}{11}.
\end{gathered}
$$

Para ${0<p<1}$ la segunda derivada es negativa; en los extremos, el factor vale 0.

::: exercise {#mkv-c1-ej-fila-c title="Maximiza la fila C"}
La fila C aporta ${p^{10}(1-p)^5}$, con ${p=P(V\mid C)}$. ¿Qué $p$ maximiza ese factor?
:::

::: hint {#mkv-c1-pista-fila-c of="mkv-c1-ej-fila-c" title="Los exponentes de la fila C"}
Al derivar el logaritmo, ¿qué números sustituyen al 2 y al 9?
:::

::: answer {#mkv-c1-resp-fila-c of="mkv-c1-ej-fila-c"}
$$
\begin{aligned}
\frac{10}{p}-\frac{5}{1-p}&=0\\
10(1-p)&=5p\\
p&=10/15=2/3\\
&=N(C,V)/N(C).
\end{aligned}
$$
:::

Falta escribirlo para cualquier texto.

---

## 3 · Contar con un algoritmo

**Piensa: ¿cómo conviertes la cuenta a mano en un procedimiento para todo el corpus?**

Primero acumulas cada par; después divides las filas con salidas.

> **Dado:** una trayectoria $s_{i_0},\dots,s_{i_T}$, con $T\ge1$, sobre $\mathcal S=\{s_1,\dots,s_k\}$.
>
> **Encontrar:** $\widehat P$ (@mkv-c1-conteos), de $k\times k$, estimando únicamente las filas con salidas.

En el pseudocódigo, $s_j$ abrevia el estado observado $s_{i_j}$: el subíndice $j$ recorre la trayectoria.

### El mapa de CONTAR-TRANSICIONES

- **Qué calcula:** estima $\widehat P$ fila por fila.
- **Qué guarda:** ${N(s,s')}$ y ${N(s)}$, a lo más ${k^2+k}$ números.
- **Cómo avanza:** suma 1 al conteo del par y a las salidas de su origen.
- **Qué devuelve al terminar:** conteos, salidas y filas estimadas; si ${N(s)=0}$, deja la fila sin estimar.

::: figure {#mkv-c1-flujo-contar title="Contar, en palabras"}
![Diagrama de flujo de contar transiciones, en una pasada por el texto: empieza con todos los conteos en 0; toma el siguiente par (actual, siguiente); suma 1 a N(s, s′) y 1 a N(s); pregunta si quedan pares, y si sí vuelve a tomar el siguiente; si no, divide cada fila entre su total N(s) y devuelve N, N(s) y P̂. Al pie: una fila con N(s) = 0 queda sin estimar, porque los datos no la fijan](../_assets/mkv-c1-flujo-contar.svg)
:::

```text
INPUT   estados 𝒮 y trayectoria
        s_0, s_1, …, s_T en 𝒮;
        T ≥ 1.
OUTPUT  N(s, s′), N(s) y P̂;
        filas sin salidas:
        sin estimar.

 1 function CONTAR-TRANSICIONES(
       𝒮, s_0, …, s_T)
 2   N(·, ·) ← 0 ; N(·) ← 0
 3   for j ← 0 to T − 1
 4     s ← s_j ; s′ ← s_{j+1}
 5     N(s, s′) ← N(s, s′) + 1
 6     N(s) ← N(s) + 1
 7   for each s with N(s) > 0
 8     for each s′ in 𝒮
 9       P̂(s′ | s) ←
           N(s, s′) / N(s)
10   return N, N(·), P̂
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo; `P_gorro` es $\widehat P$.

```python
from fractions import Fraction

# (1)
def contar_transiciones(
    secuencia, estados
):
    # (2) Todo en cero.
    N = {
        (s, s2): 0
        for s in estados
        for s2 in estados
    }
    salidas = {
        s: 0 for s in estados
    }
    # (3)
    for j in range(
        len(secuencia) - 1
    ):
        # (4) Actual y siguiente.
        s = secuencia[j]
        s2 = secuencia[j + 1]
        # (5)
        N[(s, s2)] += 1
        # (6)
        salidas[s] += 1
    P_gorro = {}
    # (7)
    for s in estados:
        # (7) Fila sin salidas.
        if salidas[s] == 0:
            continue
        # (8)
        for s2 in estados:
            # (9)
            n = N[(s, s2)]
            P_gorro[(s, s2)] = (
                Fraction(
                    n, salidas[s]
                )
            )
    # (10)
    return N, salidas, P_gorro

(
    N, salidas, P_gorro
) = contar_transiciones(
    "CVCCVVCCVCVVCVCVCCVCVCVCCCV",
    ("V", "C")
)
print(
    N[("V", "V")],
    salidas["V"],
    P_gorro[("V", "V")]
)
# 2 11 2/11
```

**Los estados son un dato.** Un estado ausente conserva su columna, aunque su fila quede sin estimar.

**Cada pieza, en su línea:**

- **Líneas 3 y 4.** Leen el par ${(s_j,s_{j+1})}$.
- **Línea 5.** Incrementa ${N(s,s')}$.
- **Línea 6.** Incrementa ${N(s)}$; la última letra no aporta salida.
- **Líneas 7 a 9.** Dividen únicamente las filas con datos.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** cuenta cada transición una vez y termina al agotar la trayectoria. Reordenar la suma de los mismos pares conserva los conteos.
- **Número que da:** devuelve conteos exactos y probabilidades estimadas.
- **Garantía:** maximiza la verosimilitud condicionada bajo @mkv-c1-teo-maximo; las filas sin salidas quedan indeterminadas.
- **Costo:** una pasada por $T$ pares y hasta ${k^2}$ divisiones:

$$
\begin{aligned}
\text{tiempo}&=O(T+k^2),\\
\text{memoria}&=O(k^2).
\end{aligned}
$$

Guarda hasta ${k^2}$ conteos, $k$ salidas y ${k^2}$ probabilidades.

- **Supuestos:** la interpretación de máxima verosimilitud requiere Markov, homogeneidad y filas libres; contar no necesita $\mu_0$.

**En el corpus.** Las 1 620 532 letras del *Quijote*, convertidas a V/C, dan 4 conteos y 2 salidas:

$$
N=\begin{pmatrix}
135\,916 & 616\,635\\
616\,635 & 251\,345
\end{pmatrix}.
$$

$$
\widehat P\approx\begin{pmatrix}
0.181 & 0.819\\
0.710 & 0.290
\end{pmatrix}.
$$

**En la frase.** Las 26 transiciones dan ${N(V)=11}$ y ${N(C)=15}$.

**Cómo leer la traza.** Cada renglón es un paso $j$ de la línea 3 y muestra los conteos después de procesar su par. El punto «·» separa dos conteos; no indica multiplicación.

- **Desde V.** Muestra ${N(V,V)}$ y ${N(V,C)}$, en ese orden.
- **Desde C.** Muestra ${N(C,V)}$ y ${N(C,C)}$, en ese orden.

**Tramo 1 · Aparecen los cuatro pares**

| j | Letras · par | Desde V | Desde C |
|---:|---|---|---|
| 0 | co · C→V | 0 · 0 | 1 · 0 |
| 1 | on · V→C | 0 · 1 | 1 · 0 |
| 2 | nl · C→C | 0 · 1 | 1 · 1 |
| 3 | la · C→V | 0 · 1 | 2 · 1 |
| 4 | ai · V→V | 1 · 1 | 2 · 1 |
| 5 | ig · V→C | 1 · 2 | 2 · 1 |
| 6 | gl · C→C | 1 · 2 | 2 · 2 |
| 7 | le · C→V | 1 · 2 | 3 · 2 |

- **Paso 0.** «co» suma 1 a ${N(C,V)}$ y a ${N(C)}$.
- **Paso 4.** Quitar el espacio de «la iglesia» junta «a» con «i»: aparece V→V.

**Tramo 2 · El segundo V→V, y luego alternan**

| j | Letras · par | Desde V | Desde C |
|---:|---|---|---|
| 8 | es · V→C | 1 · 3 | 3 · 2 |
| 9 | si · C→V | 1 · 3 | 4 · 2 |
| 10 | ia · V→V | 2 · 3 | 4 · 2 |
| 11 | ah · V→C | 2 · 4 | 4 · 2 |
| 12 | he · C→V | 2 · 4 | 5 · 2 |
| 13 | em · V→C | 2 · 5 | 5 · 2 |
| 14 | mo · C→V | 2 · 5 | 6 · 2 |
| 15 | os · V→C | 2 · 6 | 6 · 2 |

- **Paso 10.** Aparece el segundo y último V→V de la frase.
- **Pasos 11 a 15.** Solo aumentan ${N(V,C)}$ y ${N(C,V)}$.

::: exercise {#mkv-c1-ej-traza title="Termina la traza"}
Completa los pasos 18 a 25. Los pasos 16 a 25 corresponden a «sdadosancho».

**Tramo 3 · «dados» y «sanc»**

| j | Letras · par | Desde V | Desde C |
|---:|---|---|---|
| 16 | sd · C→C | 2 · 6 | 6 · 3 |
| 17 | da · C→V | 2 · 6 | 7 · 3 |
| 18 | ad · ? | 2 · ? | 7 · 3 |
| 19 | do · C→V | ? · ? | ? · ? |
| 20 | os · V→C | ? · ? | ? · ? |
| 21 | sa · ? | ? · ? | ? · ? |
| 22 | an · V→C | ? · ? | ? · ? |
| 23 | nc · ? | ? · ? | ? · ? |

**Tramo 4 · Fin**

| j | Letras · par | Desde V | Desde C |
|---:|---|---|---|
| 24 | ch · ? | ? · ? | ? · ? |
| 25 | ho · ? | ? · ? | ? · ? |

1. **Completa la traza.** Sustituye cada «?».
2. **Suma las salidas.** ¿Cuánto valen ${N(V)}$ y ${N(C)}$ al terminar?
3. **Estima la matriz.** ¿Qué produce la línea 9?
:::

::: hint {#mkv-c1-pista-traza of="mkv-c1-ej-traza" title="Una casilla por paso"}
¿Qué único conteo cambia respecto del renglón anterior?
:::

::: answer {#mkv-c1-resp-traza of="mkv-c1-ej-traza"}
**1. Traza.** En negrita, lo que era «?».

| j | Letras · par | Desde V | Desde C |
|---:|---|---|---|
| 18 | ad · **V→C** | 2 · **7** | 7 · 3 |
| 19 | do · C→V | **2 · 7** | **8 · 3** |
| 20 | os · V→C | **2 · 8** | **8 · 3** |
| 21 | sa · **C→V** | **2 · 8** | **9 · 3** |
| 22 | an · V→C | **2 · 9** | **9 · 3** |
| 23 | nc · **C→C** | **2 · 9** | **9 · 4** |
| 24 | ch · **C→C** | **2 · 9** | **9 · 5** |
| 25 | ho · **C→V** | **2 · 9** | **10 · 5** |

**2. Salidas.** ${N(V)=2+9=11}$ y ${N(C)=10+5=15}$; suman 26.

**3. Matriz.** Sus filas son ${(2/11,\ 9/11)}$ y ${(2/3,\ 1/3)}$.
:::

El algoritmo maximiza ${\mathcal L(P)}$. Si los datos vienen de una cadena, ¿recupera su matriz?

---

## 4 · Simular una matriz conocida

**Piensa: si los datos proceden de una cadena, ¿contar recupera su matriz?**

Sí, si la cadena es homogénea y las salidas de cada estado crecen sin límite.

::: theorem {#mkv-c1-teo-recuperar title="Contar recupera la matriz"}
Los datos proceden de una cadena finita y homogénea con matriz ${P\in[0,1]^{k\times k}}$. Si cada ${N(s)\to\infty}$ al crecer $T$, entonces:

$$
\widehat P\longrightarrow P
\qquad\text{con probabilidad }1.
$$

Son condiciones suficientes. Basta que la cadena finita sea irreducible: desde cada estado se puede llegar a cualquier otro.

La probabilidad se refiere a las trayectorias generadas por la cadena.
:::

**Error.** Cuando todas las filas tienen estimación, medimos la mayor diferencia entre entradas:

$$
\delta
=\max_{1\le i,j\le k}
\lvert\widehat P_{ij}-P_{ij}\rvert.
$$

**Sin salidas no hay recuperación.** Si V y C fueran absorbentes —desde cada uno solo se puede permanecer ahí— y empezaras en C, siempre observarías C. Aunque $T$ creciera, $N(V)=0$.

**El experimento:**

- **Matriz generadora.** La matriz V/C del corpus, redondeada a tres decimales:

$$
P=\begin{pmatrix}
0.181&0.819\\
0.710&0.290
\end{pmatrix}.
$$

- **Réplica.** Una trayectoria independiente de $T$ pasos desde C; cada paso usa MUESTREAR-FILA con un uniforme nuevo.
- **Repeticiones.** ${n=200}$ réplicas por largo. Largos: 10, 30, 100, 300, 1 000, 3 000 y 10 000 pasos. Semilla: 2028.

**Una réplica, a mano.** Usa los uniformes de [[mkv-el-problema-de-markov|El problema de Markov]]: 0.40, 0.75, 0.90, 0.25 y 0.10. Desde C sale `CVCCVV`, con ${T=5}$:

$$
\widehat P=\begin{pmatrix}
1/2&1/2\\
2/3&1/3
\end{pmatrix}.
$$

$$
\delta=|0.5-0.181|=0.319.
$$

**Qué muestra la gráfica.** El eje horizontal mide $T$ en pasos; el vertical, el error. Cada punto es la mediana para un mismo $T$; la franja abarca del 5 % al 95 %.

**Con ${T=10}$.** La mediana es 0.210; la franja, 0.069–0.319. Muchas réplicas no ven V→V y estiman ${\widehat P(V\mid V)=0}$: producen el error más frecuente, 0.181.

::: figure {#mkv-c1-recuperar-p title="Contar recupera una matriz conocida: el error baja al crecer el largo T, en pasos"}
![Error de la matriz estimada contra el largo T de la trayectoria, en pasos, con T en escala logarítmica, en 200 réplicas de una cadena conocida que empiezan en C. La mediana del error baja de 0.210 con T = 10 a 0.006 con T = 10 000. La franja del 5 % al 95 % va de 0.069 a 0.319 con T = 10 y de 0.002 a 0.013 con T = 10 000. Ninguna réplica se quedó sin salidas de un estado](../_assets/mkv-c1-recuperar-p.svg)
:::

- **Trayectorias largas.** Con ${T=10\,000}$, la mediana es 0.006; la franja, 0.002–0.013.
- **Variabilidad.** Las franjas para ${T=100}$ y ${T=300}$ son 0.025–0.130 y 0.009–0.071. Se traslapan: más pasos no garantizan menos error en cada réplica.
- **Filas sin estimar.** Ninguna réplica quedó sin salidas de algún estado, ni con ${T=10}$; si ocurriera, se reportaría aparte.

> [!WARNING]
> **Confundir recuperación con validación.** La simulación comprueba el procedimiento bajo el modelo supuesto. **No demuestra que el texto sea una cadena que solo mira la letra anterior.** El ajuste del *Quijote* no es «la matriz del español».

::: exercise {#mkv-c1-ej-sin-salidas title="Imagina una réplica sin vocales"}
Una réplica de ${T=10}$ empieza en C y nunca pasa por V.

1. **Identifica las filas estimables.** ¿Cuáles puede calcular CONTAR-TRANSICIONES?
2. **Revisa el código.** ¿Qué hace la línea 7 con V?
:::

::: hint {#mkv-c1-pista-sin-salidas of="mkv-c1-ej-sin-salidas" title="Mira las salidas"}
¿Cuánto vale ${N(V)}$ si V nunca aparece en los primeros $T$ estados?
:::

::: answer {#mkv-c1-resp-sin-salidas of="mkv-c1-ej-sin-salidas"}
1. **Solo estima C.** Su fila queda ${(0,\ 1)}$.
2. **Omite V.** Como ${N(V)=0}$, cualquier fila V da la misma verosimilitud (@mkv-c1-teo-maximo). Esto no ocurrió en las 200 réplicas de cada $T$.
:::

En V/C, cada fila tiene datos de sobra. ¿Y si cada letra es un estado?

---

## 5 · Generalizar a todo el alfabeto

**Piensa: ¿qué cambia si cada letra es un estado?**

Aumenta el tamaño de la matriz y los datos se reparten entre más filas.

El ajuste sigue siendo $\widehat P_{ij}=N(s_i,s_j)/N(s_i)$ para $N(s_i)>0$ (@mkv-c1-conteos).

$$
\begin{aligned}
\text{entradas}&=k^2,\\
\text{números libres}&=k(k-1).
\end{aligned}
$$

La suma de cada fila fija su última entrada: quedan $k-1$ números libres por fila.

**En el texto.** $\Sigma$ es el alfabeto de símbolos posibles: conservamos 27 letras y el espacio, con ${|\Sigma|=28}$.

- **Normalización.** Los espacios consecutivos se reducen a uno. Conservar el espacio distingue el límite de palabra: «la iglesia» ya no junta «a» con «i».
- **Tamaño.** ${28\times28}$: 784 entradas posibles y 27 números libres por fila.
- **Ceros.** En el corpus, 393 pares tienen conteo 0.
- **Pocos datos.** Hay 433 pares con menos de 5 conteos, incluidos los ceros.
- **Estado ausente.** La «k» no aparece: los datos no determinan su fila.

El juguete tiene datos en ambas filas y un número libre por fila; eso no se conserva al ampliar el alfabeto.

::: exercise {#mkv-c1-ej-tamanos title="Cuenta las entradas"}
Quita el espacio y conserva solo las 27 letras.

1. **Calcula el tamaño.** ¿Qué dimensiones tiene $\widehat P$?
2. **Cuenta los números libres.** ¿Cuántos tiene cada fila?
:::

::: hint {#mkv-c1-pista-tamanos of="mkv-c1-ej-tamanos" title="Filas por columnas"}
¿Cuántas filas y columnas necesitas? ¿Qué entrada queda fijada cuando las demás se conocen y la fila suma 1?
:::

::: answer {#mkv-c1-resp-tamanos of="mkv-c1-ej-tamanos"}
1. **La matriz es ${27\times27}$.** Hay una fila y una columna por letra.
2. **Cada fila tiene 26 números libres.** El último se obtiene de la suma 1; en general, hay ${k-1}$.
:::

Con 784 entradas, muchas quedan en 0. ¿Qué hacer con ellas?

---

## 6 · Tratar lo que nunca se vio

**Piensa: ¿un conteo 0 significa que la transición es imposible?**

No necesariamente: puede faltar evidencia. Pero en una fila con salidas, un conteo 0 da ${\widehat P_{ij}=0}$ y descarta toda trayectoria que use ese par.

::: definition {#mkv-c1-laplace title="Suavizado aditivo de conteos (Laplace)"}
**Qué es.** Laplace suma 1 por símbolo siguiente antes de dividir; la estimación suavizada se escribe $\widetilde p$.

**Cómo se calcula.** Para el estado actual $s$ y cada símbolo siguiente ${z\in\Sigma}$, con $\Sigma$ finito y no vacío:

$$
\widetilde p(z\mid s)
=\frac{N(s,z)+1}{N(s)+|\Sigma|}.
$$

Aquí cada estado es un símbolo, así que $z$ también es el estado siguiente.

**Qué significa.** Agrega una observación de cada siguiente posible:

$$
\widetilde p(z\mid s)>0,
\qquad
\sum_{z\in\Sigma}\widetilde p(z\mid s)=1.
$$

Los conteos 0 reciben probabilidad positiva; una fila sin datos queda uniforme.

**Qué no es.** No garantiza máxima verosimilitud; puede coincidir con ella si los conteos de la fila son iguales. Introduce sesgo hacia la uniforme.
:::

**Tres ausencias distintas:**

- **Cero estructural.** Imposible por las reglas o la normalización: nunca quedan dos espacios consecutivos.
- **Transición no observada.** «q» tiene ${N(q)=32\,155}$ salidas, todas hacia «u». No apareció q→a, aunque podría aparecer en «Qatar».
- **Estado sin observaciones.** ${N(s)=0}$, como ocurre con «k»: su fila queda indeterminada.

El conteo solo no distingue imposibilidad de falta de datos.

**A mano.** En la frase, ${|\Sigma|=k=2}$. Los conteos de V, 2 y 9, pasan a 3 y 10, con total 13:

$$
\begin{aligned}
\text{fila V:}\quad
&(2/11,\ 9/11)\\
&\longrightarrow(3/13,\ 10/13),\\
\text{fila C:}\quad
&(10/15,\ 5/15)\\
&\longrightarrow(11/17,\ 6/17).
\end{aligned}
$$

**En el corpus**, el denominador de «q» es:

$$
32\,155+28=32\,183.
$$

- **q→u.** Baja de 1 a ${\frac{32\,156}{32\,183}\approx0.9992}$.
- **q→a.** Sube de 0 a ${\frac{1}{32\,183}\approx0.00003}$.
- **Fila «k».** Cada siguiente recibe ${\frac{0+1}{0+28}}$.

El efecto depende de los datos: grande en la fila V de la frase, pequeño en «q».

> [!WARNING]
> **Suavizar no garantiza mejorar.** Evita descartar trayectorias por pares no observados, pero sesga hacia la uniforme. **También asigna probabilidad a ceros estructurales si los incluye entre los siguientes posibles.**

::: exercise {#mkv-c1-ej-laplace title="Suaviza una fila corta"}
En `conla`, ${N(V,V)=0}$ y ${N(V,C)=1}$.

1. **Estima sin suavizar.** ¿Cuál es la fila V de $\widehat P$?
2. **Aplica Laplace.** ¿Cuál es su fila de $\widetilde p$, con ${|\Sigma|=2}$?
:::

::: hint {#mkv-c1-pista-laplace of="mkv-c1-ej-laplace" title="Qué cambia en la cuenta"}
Si cada siguiente gana 1, ¿cuánto aumenta el denominador?
:::

::: answer {#mkv-c1-resp-laplace of="mkv-c1-ej-laplace"}
1. **Sin suavizar, queda ${(0,\ 1)}$.** Solo se observó V→C.
2. **Con Laplace, queda ${(1/3,\ 2/3)}$.** Las entradas son ${\frac{0+1}{1+2}}$ y ${\frac{1+1}{1+2}}$; con un solo dato, el cambio es grande.
:::

Más filas vacías aparecen al meter más pasado en el estado.

---

## 7 · Decidir cuánta memoria lleva el estado

**Piensa: ¿qué puedes cambiar si la letra actual no basta para modelar la siguiente?**

Puedes incluir más pasado en el estado.

::: definition {#mkv-c1-memoria title="La memoria de un modelo de texto"}
**Qué es.** La memoria $h$ indica cuántos símbolos forman el contexto usado como estado.

**Cómo se calcula.** Para símbolos $z_0,\dots,z_T\in\Sigma$, con $1\le h\le T$, el contexto $c_t$ se desliza:

$$
\begin{aligned}
c_t&=(z_{t-h+1},\dots,z_t)\in\Sigma^h,\\
c_{t+1}&=(z_{t-h+2},\dots,z_{t+1}),\\
t&=h-1,\dots,T-1.
\end{aligned}
$$

Se cuentan pares $(c_t,z_{t+1})$:

$$
\begin{aligned}
\text{tabla útil:}\quad&|\Sigma|^h\times|\Sigma|,\\
\text{número de pares:}\quad&T-h+1.
\end{aligned}
$$

Cada fila es un contexto; cada columna, el símbolo siguiente. Con ${h=0}$ no hay contexto: una sola fila cuenta todos los símbolos.

**Qué significa.** Memoria 0 usa frecuencias de símbolos: unigrama. Memoria 1 usa pares: bigrama; memoria 2 usa tríos: trigrama.

**Qué no es.** No es la profundidad de búsqueda: cambia qué información contiene el estado.
:::

Un estado sin observaciones es ahora un contexto sin observaciones.

**El estado es una decisión de modelado.** En [[escribir-el-juego|Escribir el juego]], incluimos el turno porque el tablero solo no bastaba.

**La cadena sobre contextos sí es cuadrada**, de ${|\Sigma|^h\times|\Sigma|^h}$. Sus transiciones deben respetar el deslizamiento.

**Laplace por contexto:** $\widetilde p(z\mid c_t)=[N(c_t,z)+1]/[N(c_t)+|\Sigma|]$ (@mkv-c1-laplace). Se suavizan símbolos siguientes; cada símbolo determina el contexto siguiente.

**En el texto:**

- **Deslizamiento.** Al agregar «l», «con» pasa a «onl».
- **Memoria 2.** Hay ${28^2=784}$ contextos por 28 siguientes: 784 cuenta contextos, no entradas.
- **Transiciones permitidas.** De «la» solo se pasa a contextos que empiezan con «a»: «aa», «ab», «ac», etc.
- **Suavizado incorrecto.** Sumar 1 a las 784 columnas de la matriz de contextos permitiría «la»→«de», que viola el deslizamiento.

**En el corpus.** Contamos en la primera mitad y probamos en la segunda. Esta aporta cerca de un millón de transiciones: 998 563 con memoria 1.

Cada barra mide la fracción de pares (contexto, siguiente) de prueba que no apareció al contar.

::: figure {#mkv-c1-ceros title="Lo que nunca se vio, por memoria"}
![Barras horizontales por memoria, con la fracción de transiciones de la segunda mitad del corpus nunca vistas en la primera. Memoria 0: 0 %, 0 de 998 564, contextos vistos 1 de 1. Memoria 1: 0.003 %, 29 de 998 563, contextos vistos 27 de 28. Memoria 2: 0.072 %, 718 de 998 562, contextos vistos 379 de 784. Memoria 3: 0.570 %, 5 694 de 998 561, contextos vistos 3 328 de 21 952. Las barras están a escala de la mayor (memoria 3). Al pie: solo diagnostica escasez, no elige la memoria](../_assets/mkv-c1-ceros.svg)
:::

- **Fracciones.** Son 0.003 %, 0.072 % y 0.570 % para memorias 1, 2 y 3.
- **Escasez.** Con memoria 3, menos de una transición de cada 100 es nueva: el *Quijote* es largo.
- **Contextos vistos.** Con memoria 2, 379 de 784; con memoria 3, 3 328 de 21 952.
- **Ausencias estructurales.** Tres espacios seguidos no existen tras normalizar.

> [!WARNING]
> **Elegir memoria por los ceros.** Memoria 0 tiene 0 % de transiciones no vistas, pero ignora la letra anterior. **La @mkv-c1-ceros diagnostica escasez; no elige la memoria.**

::: exercise {#mkv-c1-ej-contexto title="Desliza el contexto"}
Recorre `conlaiglesia` con memoria 2.

1. **Forma los pares.** Escribe los tres primeros pares (contexto, siguiente).
2. **Cuenta las transiciones.** ¿Cuántas produce una frase de 27 letras con memoria 2?
:::

::: hint {#mkv-c1-pista-contexto of="mkv-c1-ej-contexto" title="El primer contexto completo"}
Si necesitas dos letras para el contexto, ¿cuál es el primer símbolo siguiente?
:::

::: answer {#mkv-c1-resp-contexto of="mkv-c1-ej-contexto"}
1. **Los pares son (co, n), (on, l) y (nl, a).** Cada contexto pierde su primera letra y agrega la nueva.
2. **Hay 25 transiciones.** Para una trayectoria de $T$ pasos, hay ${T-h+1}$ pares cuando alcanza para formar el contexto y un siguiente.
:::

Con esto tienes todo para ajustar una cadena por tu cuenta.

---

## Ejercicios

::: exercise {#mkv-c1-ej-tres-simbolos title="Ajusta una cadena de tres símbolos"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Observaste `abacabbcabac`, un texto con símbolos a, b y c. **Cambia una idea:** ahora hay tres estados en lugar de dos. El texto es tan corto que alguna fila se apoya en muy pocas salidas.

1. **Cuenta.** Indica cuántas transiciones hay, construye la tabla ${3\times3}$ y calcula las salidas de cada símbolo.
2. **Estima.** Escribe $\widehat P$.
3. **Interpreta los ceros.** Señálalos y explica si puedes saber que son estructurales.
4. **Suaviza.** Aplica Laplace a las filas a y c.
:::

::: hint {#mkv-c1-pista-tres-simbolos-1 of="mkv-c1-ej-tres-simbolos" title="Pista 1 · ¿Cuántos pares salen?"}
¿Qué pares obtienes al recorrer el texto? ¿Qué aparición no aporta una salida?
:::

::: hint {#mkv-c1-pista-tres-simbolos-2 of="mkv-c1-ej-tres-simbolos" title="Pista 2 · ¿Suman lo que deben?"}
¿Los conteos suman las salidas y estas suman las transiciones? ¿Qué denominador corresponde a cada fila al suavizar?
:::

::: answer {#mkv-c1-resp-tres-simbolos of="mkv-c1-ej-tres-simbolos" title="Respuesta · Tres filas, cada una por su lado"}
**1. Conteos.** Doce letras dan 11 transiciones. La «c» aparece 3 veces, pero solo tiene 2 salidas.

| Desde | a | b | c |
|---|---:|---:|---:|
| a | 0 | 3 | 2 |
| b | 2 | 1 | 1 |
| c | 2 | 0 | 0 |

Las salidas son ${N(a)=5}$, ${N(b)=4}$ y ${N(c)=2}$; suman 11.

**2. Matriz.** Dividimos cada fila entre sus salidas, en el orden a, b, c:

$$
\widehat P=
\begin{pmatrix}
0 & 3/5 & 2/5\\
1/2 & 1/4 & 1/4\\
1 & 0 & 0
\end{pmatrix}.
$$

**3. Ceros.** Corresponden a a→a, c→b y c→c. Estos datos no permiten clasificarlos como estructurales; c solo tiene 2 salidas.

**4. Laplace.** El alfabeto tiene ${|\Sigma|=3}$.

- **Fila a.** Las entradas ${\frac{0+1}{8}}$, ${\frac{3+1}{8}}$ y ${\frac{2+1}{8}}$ dan ${(1/8,\ 1/2,\ 3/8)}$.
- **Fila c.** Las entradas ${\frac{2+1}{5}}$, ${\frac{0+1}{5}}$ y ${\frac{0+1}{5}}$ dan ${(3/5,\ 1/5,\ 1/5)}$.
:::

::: exercise {#mkv-c1-ej-ceros title="Lee la figura de ceros con menos texto"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Usa @mkv-c1-ceros. **Cambia una idea:** cuenta solo con unas páginas de la primera mitad y conserva la segunda como prueba. Responde 1–3 y 5 con la figura, y 4 con esa idea.

1. **Lee la fracción.** ¿Qué memoria tiene más transiciones no vistas y qué tan grande es su proporción?
2. **Compara los contextos.** Con memoria 2, ¿se observó más o menos de la mitad de los posibles?
3. **Distingue las ausencias.** Da un contexto de memoria 3 imposible y otro no observado que podría aparecer en otro texto.
4. **Reduce los datos.** ¿Qué cambios esperarías en las barras y por qué?
5. **Delimita el diagnóstico.** ¿La figura basta para elegir memoria? Justifica.
:::

::: hint {#mkv-c1-pista-ceros-1 of="mkv-c1-ej-ceros" title="Pista 1 · ¿Qué mide cada barra?"}
¿De qué mitad salen los pares que se prueban? ¿Qué puede faltar si cuentas con menos texto?
:::

::: hint {#mkv-c1-pista-ceros-2 of="mkv-c1-ej-ceros" title="Pista 2 · ¿Qué no mide?"}
¿Qué tendría que medir una figura para comparar dos memorias? ¿Esta lo mide?
:::

::: answer {#mkv-c1-resp-ceros of="mkv-c1-ej-ceros" title="Respuesta · Escasez sí, elección no"}
**1. Memoria 3.** Tiene 0.570 %: menos de una transición de cada 100.

**2. Menos de la mitad.** Se observaron 379 de 784; la mitad sería 392.

**3. Dos ausencias distintas.** Tres espacios seguidos son imposibles tras normalizar. «kia» es un contexto sin observaciones en este corpus, que no contiene «k»; podría aparecer en otro texto.

**4. Las fracciones no pueden bajar.** Quitar datos de conteo no agrega pares vistos; pueden quedar iguales. Lo esperable es que suban, sobre todo con memoria alta: hay 21 952 contextos posibles con memoria 3. Incluso memoria 0 puede dejar de ver algún símbolo.

**5. No basta.** Memoria 0 tiene 0 % de transiciones no vistas, pero ignora la dependencia entre «q» y «u». Elegir requiere evaluar predicciones en datos reservados.
:::

**Punto de control:** deberías poder contar pares, estimar filas con salidas y justificar su máxima verosimilitud condicionada. También, distinguir los tres casos de ausencia, aplicar Laplace y explicar el costo de aumentar la memoria.

---

## Para profundizar

**Piensa: ¿cómo comparas memorias sin decidir solo por sus ceros?**

Comparas su pérdida promedio en datos reservados: menor pérdida significa mejores predicciones de esos datos.

### Elegir la memoria con datos reservados

La pérdida logarítmica por símbolo observado $z$, dado el contexto $s$, es:

$$
-\log\widetilde p(z\mid s),
\qquad \widetilde p(z\mid s)>0.
$$

Ajusta y suaviza con la primera mitad; promedia esta pérdida en la segunda. Un promedio menor indica mejores predicciones reservadas.

Con logaritmo natural:

$$
\begin{aligned}
-\log 0.9&\approx0.105,\\
-\log 0.1&\approx2.303.
\end{aligned}
$$

- **Suavizado.** Evita ${\log 0}$ y la pérdida infinita por una transición no observada.
- **Comparación.** Más memoria representa dependencias adicionales, pero no garantiza menor pérdida en datos reservados.

---

## Lo que hay que llevarse

- **Conteo por fila.** ${\widehat P_{ij}=N(s_i,s_j)/N(s_i)}$, solo si ${N(s_i)>0}$. Las 26 transiciones de la frase dan filas ${(2/11,\ 9/11)}$ y ${(2/3,\ 1/3)}$.
- **Máxima verosimilitud.** Markov, homogeneidad, filas libres e inicio condicionado justifican el máximo. En la frase: ${3.88\times10^{-7}}$, frente a ${1.49\times10^{-8}}$ con filas de ½.
- **Recuperación.** Con datos de esa cadena homogénea y cada ${N(s)\to\infty}$, ${\widehat P\to P}$ con probabilidad 1; basta irreducibilidad. En 200 réplicas por longitud, la mediana baja de 0.210 ${(T=10)}$ a 0.006 ${(T=10\,000)}$.
- **Ausencias y suavizado.** Con 28 símbolos hay 784 entradas y 393 conteos 0; «k» queda sin fila estimada. Laplace sesga hacia la uniforme: q→u baja a ${\frac{32\,156}{32\,183}}$.
- **Memoria.** La tabla útil es de ${|\Sigma|^h\times|\Sigma|}$. Entre memorias 1 y 3, las transiciones no vistas pasan de 0.003 % a 0.570 %. Los contextos posibles llegan a 21 952. La figura diagnostica escasez, sin elegir memoria.

Continúa con [[mkv-predecir|Predecir]].

