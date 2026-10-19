---
id: mkv-ajustar-contando
title: "Ajustar contando"
nav_title: "Ajustar contando"
summary: "Si solo tienes el texto: contar transiciones da la matriz que hace más probable lo observado. El algoritmo trazado en la frase, una simulación que recupera una matriz conocida, qué hacer con lo que nunca se vio y cuánta memoria aguantan los datos del Quijote."
status: ready
estimated_time: 35m
tags: [markov]
---

# Ajustar contando

**Si solo tienes el texto, ¿cómo sacas $\widehat P$, qué garantiza y dónde falla?**

Al terminar tendrás:

- **El algoritmo CONTAR-TRANSICIONES,** en pseudocódigo y en Python, trazado par por par en la frase.
- **Por qué contar es lo correcto:** da la matriz que hace más probable el texto, y no estima las filas sin salidas.
- **Una simulación** en la que contar recupera una matriz conocida, con su error.
- **El suavizado aditivo de conteos (Laplace)** para lo que nunca se vio, y lo que sesga.
- **La memoria del estado como decisión de modelado,** medida en el *Quijote*.

## Lo que traes

- **Probabilidad condicional.** En [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] estimaste $\widehat{\Pr}(A\mid B)$ con frecuencias.
- **La cadena.** En [[mkv-el-problema-de-markov|El problema de Markov]] definiste $(\mathcal S,\mu_0,P)$: estados, distribución inicial y matriz de transición.
- **La matriz.** Las filas indican desde dónde sales; las columnas, hacia dónde vas. Cada entrada está en $[0,1]$ y cada fila suma 1.
- **La trayectoria.** Con propiedad de Markov y homogeneidad, su probabilidad es $\mu_0(s_0)\prod_{j=0}^{t-1}P(s_{j+1}\mid s_j)$.
- **La frase y el muestreo.** En «Con la iglesia hemos dado, Sancho», una vocal siguió a otra 2 de 11 veces; tras consonante, 2 de cada 3. MUESTREAR-FILA simula cada paso con la fila acumulada y un uniforme $u$.

> **Modelo y datos.** El texto es una trayectoria observada. Que lo haya generado una cadena finita y homogénea es una hipótesis útil, no un hecho: $\widehat P$ será la cadena de memoria 1 que mejor explica lo que leímos.

---

## 1 · Pasar del texto a la matriz

**Piensa: ¿qué debes contar para llenar toda la matriz?**

Debes contar cada par (actual, siguiente) y las salidas de cada estado. La frase normalizada, `conlaiglesiahemosdadosancho`, tiene 27 letras:

```text
CVCCVVCCVCVVCVCVCCVCVCVCCCV
```

**A mano.** Hay 26 transiciones: la última letra no tiene siguiente.

::: table {#mkv-c1-tabla-conteos-frase title="Los conteos de la frase"}
| Desde | Hacia V | Hacia C | Salidas |
|---|---:|---:|---:|
| V | 2 | 9 | 11 |
| C | 10 | 5 | 15 |
:::

Divide cada fila entre sus salidas. En el orden V, C:

$$
\widehat P=\begin{pmatrix}2/11 & 9/11\\ 2/3 & 1/3\end{pmatrix}.
$$

La segunda fila simplifica $10/15$ y $5/15$.

::: definition {#mkv-c1-conteos title="Conteos, salidas y matriz estimada"}
**Qué es.** $N(s,s')$ cuenta las transiciones observadas de $s$ a $s'$. Su total, $N(s)=\sum_{s'}N(s,s')$, cuenta las salidas de $s$.

**Cómo se calcula.** Recorre $s_0,\dots,s_T$, una trayectoria de $T$ pasos (la $t$ de la fórmula de la página 2, ahora el largo de los datos), y suma 1 por cada par. Esta $T$ no es la $T(s,a)$ de juegos. Después calcula:

$$
\widehat P(s'\mid s)=\frac{N(s,s')}{N(s)},
\qquad N(s)>0.
$$

**Qué significa.** Cada entrada es una frecuencia observada; el gorro marca una estimación. En la frase, $T=26$: hay 27 observaciones de estado y 26 transiciones. Los estados posibles son V y C: $k=2$.

**Qué no es.** $N(s)$ no cuenta apariciones. Hay 12 vocales, pero la «o» final no tiene sucesor: $N(V)=11$.
:::

> **Dado:** una trayectoria $s_0,\dots,s_T$, con $T\ge1$, sobre $\mathcal S$, un conjunto de $k$ estados.
>
> **Encontrar:** $\widehat P$ (@mkv-c1-conteos), de $k\times k$, estimando únicamente las filas con salidas.

### El mapa de CONTAR-TRANSICIONES

- **Qué calcula:** estima $\widehat P$ fila por fila.
- **Qué guarda:** acumula $N(s,s')$ y $N(s)$; necesita a lo más $k^2+k$ números.
- **Cómo avanza:** procesa una transición y suma 1 al conteo del par y a las salidas.
- **Qué devuelve al terminar:** entrega conteos, salidas y filas estimadas. Si $N(s)=0$, deja esa fila sin estimar.

::: figure {#mkv-c1-flujo-contar title="Contar, en palabras"}
![Diagrama de flujo de contar transiciones, en una pasada por el texto: empieza con todos los conteos en 0; toma el siguiente par (actual, siguiente); suma 1 a N(s, s′) y 1 a N(s); pregunta si quedan pares, y si sí vuelve a tomar el siguiente; si no, divide cada fila entre su total N(s) y devuelve N y P̂. Al pie: una fila con N(s) = 0 queda sin estimar, porque los datos no la fijan](../_assets/mkv-c1-flujo-contar.svg)
:::

::: exercise {#mkv-c1-ej-salidas title="Cuenta las salidas"}
Toma `conla`: C V C C V.

1. **Cuenta los pasos.** ¿Cuánto vale $T$?
2. **Cuenta las salidas.** Escribe $N(V)$, $N(C)$ y los cuatro conteos.
3. **Estima las filas.** ¿Cuáles puedes calcular?
:::

::: hint {#mkv-c1-pista-salidas of="mkv-c1-ej-salidas" title="Cuenta pares, no letras"}
¿Cuántos pares (actual, siguiente) forman cinco letras?
:::

::: answer {#mkv-c1-resp-salidas of="mkv-c1-ej-salidas"}
1. **Hay $T=4$ pasos.** Son C→V, V→C, C→C y C→V.
2. **Los conteos son** $N(C,V)=2$, $N(C,C)=1$, $N(V,C)=1$ y $N(V,V)=0$. Las salidas son $N(C)=3$ y $N(V)=1$.
3. **Se estiman las dos filas.** En el orden V, C, la fila C es $(2/3,\ 1/3)$; la fila V, $(0,\ 1)$. Esta última depende de un solo par.
:::

Ya sabes contar. ¿Por qué estos cocientes y no otros?

---

## 2 · Justificar por qué contar

**Piensa: ¿puede otra matriz hacer más probable la frase observada?**

No, si condicionamos al primer estado y dejamos libres las filas de una cadena finita y homogénea. Para verlo, agrupamos los factores de la trayectoria:

$$
\begin{aligned}
\Pr(s_0,\dots,s_T)
&=\mu_0(s_0)\prod_{j=0}^{T-1}P(s_{j+1}\mid s_j)\\
&=\mu_0(s_0)\prod_{s,s'}P(s'\mid s)^{N(s,s')}.
\end{aligned}
$$

Cada par aparece tantas veces como indica su conteo. Los pares no observados no aportan factores.

::: definition {#mkv-c1-verosimilitud title="La verosimilitud de una matriz"}
**Qué es.** La verosimilitud (*likelihood*) $\mathcal L(P)$ compara matrices mediante la probabilidad de los datos observados. Los datos quedan fijos; cambia $P$.

**Cómo se calcula.** Con propiedad de Markov y homogeneidad, condicionando a $S_0=s_0$:

$$
\mathcal L(P)=\prod_{s,s'}P(s'\mid s)^{N(s,s')}.
$$

**Qué significa.** Una verosimilitud mayor hace más probable esta trayectoria. Condicionar al inicio permite estudiar las transiciones sin ajustar $\mu_0$.

**Qué no es.** No es la probabilidad de que $P$ sea verdadera. Comparamos matrices para los mismos datos.
:::

**En la frase:**

$$
\begin{aligned}
\mathcal L(\widehat P)
&=\left(\tfrac{2}{11}\right)^2
  \left(\tfrac{9}{11}\right)^9
  \left(\tfrac{2}{3}\right)^{10}
  \left(\tfrac{1}{3}\right)^5\\
&\approx3.88\times10^{-7}.
\end{aligned}
$$

- **Filas de ½.** Dan $(1/2)^{26}\approx1.49\times10^{-8}$; $\widehat P$ hace la frase 26 veces más probable.
- **Una matriz cercana.** Con filas $(0.181,\ 0.819)$ y $(0.710,\ 0.290)$ da $\approx3.63\times10^{-7}$; $\widehat P$ alcanza 1.07 veces ese valor.

**A mano, una fila.** La fila V aporta $p^2(1-p)^9$, donde $p=P(V\mid V)$ y $1-p=P(C\mid V)$. El logaritmo conserva el máximo:

$$
\begin{aligned}
\frac{d}{dp}[2\log p+9\log(1-p)]
&=\frac{2}{p}-\frac{9}{1-p}=0\\
\Longrightarrow\quad p&=\frac{2}{11}.
\end{aligned}
$$

Para $0<p<1$ la segunda derivada es negativa, y en los extremos la fila vale 0: $2/11$ es el máximo.

**Con $k$ estados, cada fila se maximiza sola.** La verosimilitud separa sus factores por filas, cada una con $k-1$ números libres. Para una fila fija se maximiza $\sum_{s'}N(s,s')\log P(s'\mid s)$ con la condición de que sume 1. El multiplicador, como en [[el-multiplicador|El multiplicador]], hace las probabilidades proporcionales a los conteos; normalizar da $N(s,s')/N(s)$, y los conteos 0 reciben 0.

::: theorem {#mkv-c1-teo-maximo title="Contar da la matriz más verosímil"}
En una cadena finita y homogénea, condicionamos a $S_0=s_0$. Cada fila de $P$ queda libre, con entradas no negativas que suman 1.

Si $N(s)>0$, su máximo de verosimilitud se alcanza en $P(s'\mid s)=N(s,s')/N(s)$.

Si $N(s)=0$, cualquier fila de probabilidades da el mismo máximo: los datos no la determinan.
:::

La condición sobre el inicio importa. Si su distribución dependiera de $P$ y no condicionáramos, habría otro factor que podría cambiar el máximo.

::: exercise {#mkv-c1-ej-fila-c title="Maximiza la fila C"}
La fila C aporta $p^{10}(1-p)^5$, con $p=P(V\mid C)$. ¿Qué $p$ maximiza ese factor?
:::

::: hint {#mkv-c1-pista-fila-c of="mkv-c1-ej-fila-c" title="Copia la cuenta de la fila V"}
Al derivar el logaritmo, ¿qué números sustituyen al 2 y al 9?
:::

::: answer {#mkv-c1-resp-fila-c of="mkv-c1-ej-fila-c"}
$\frac{10}{p}-\frac{5}{1-p}=0$ da $10(1-p)=5p$. Por tanto, $p=10/15=2/3=N(C,V)/N(C)$.
:::

Falta escribirlo para cualquier texto.

---

## 3 · Contar con un algoritmo

**Piensa: ¿cómo conviertes la cuenta a mano en un procedimiento para todo el corpus?**

Primero acumulas cada par; después divides las filas con salidas.

```text
INPUT   el conjunto de estados 𝒮 y una
        trayectoria s_0, s_1, …, s_T sobre 𝒮,
        con T ≥ 1.
OUTPUT  los conteos N(s, s′), las salidas N(s)
        y la matriz estimada P̂.

 1 function CONTAR-TRANSICIONES(𝒮, s_0, …, s_T)
 2   N(·, ·) ← 0 ; N(·) ← 0    # todo en cero
 3   for j ← 0 to T − 1        # un par por paso
 4     s ← s_j ; s′ ← s_{j+1}  # el par del paso j
 5     N(s, s′) ← N(s, s′) + 1
 6     N(s) ← N(s) + 1         # una salida de s
 7   for each s with N(s) > 0  # filas con datos
 8     for each s′ in 𝒮
 9       P̂(s′ | s) ← N(s, s′) / N(s)
10   return N, N(·), P̂         # N(s) = 0: sin fila
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo. `P_gorro` es $\widehat P$.

```python
from fractions import Fraction

def contar_transiciones(secuencia, estados):  # (1)
    N = {(s, s2): 0 for s in estados         # (2) todo
         for s2 in estados}                   #     en 0
    salidas = {s: 0 for s in estados}         # (2)
    for j in range(len(secuencia) - 1):       # (3)
        s = secuencia[j]                      # (4) actual
        s2 = secuencia[j + 1]                 # (4) siguiente
        N[(s, s2)] += 1                       # (5)
        salidas[s] += 1                       # (6)
    P_gorro = {}                              # P̂
    for s in estados:                         # (7)
        if salidas[s] == 0:                   # (7) sin fila
            continue
        for s2 in estados:                    # (8)
            n = N[(s, s2)]                    # (9)
            P_gorro[(s, s2)] = Fraction(n, salidas[s])
    return N, salidas, P_gorro                # (10)

N, salidas, P_gorro = contar_transiciones(
    "CVCCVVCCVCVVCVCVCCVCVCVCCCV", ("V", "C"))
print(N[("V", "V")], salidas["V"], P_gorro[("V", "V")])
# 2 11 2/11
```

El conjunto de estados se recibe como dato: un estado que no aparece conserva su columna, aunque su fila quede sin estimar.

**Cada pieza, en su línea:**

- **Líneas 3 y 4.** Leen el par $(s_j,s_{j+1})$.
- **Línea 5.** Incrementa $N(s,s')$.
- **Línea 6.** Incrementa $N(s)$; la última letra no aporta una salida.
- **Líneas 7 a 9.** Dividen únicamente las filas con datos.

**Cómo leer la traza.** Cada renglón es un paso $j$ de la línea 3 y muestra los conteos después de procesar su par. El punto «·» separa dos conteos; no indica multiplicación.

- **Desde V.** Muestra $N(V,V)$ y $N(V,C)$, en ese orden.
- **Desde C.** Muestra $N(C,V)$ y $N(C,C)$, en ese orden.

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

- **Paso 0.** «co» suma 1 a $N(C,V)$ y a $N(C)$.
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
- **Pasos 11 a 15.** Solo aumentan $N(V,C)$ y $N(C,V)$.

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
2. **Suma las salidas.** ¿Cuánto valen $N(V)$ y $N(C)$ al terminar?
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

**2. Salidas.** $N(V)=2+9=11$ y $N(C)=10+5=15$; suman 26.

**3. Matriz.** Sus filas son $(2/11,\ 9/11)$ y $(2/3,\ 1/3)$.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** cuenta cada transición una vez y termina al agotar la trayectoria finita. Reordenar la suma de los mismos pares conserva los conteos.
- **Número que da:** devuelve conteos exactos y probabilidades estimadas. Las 26 transiciones dan $N(V)=11$ y $N(C)=15$.
- **Garantía:** bajo las condiciones de @mkv-c1-teo-maximo, maximiza la verosimilitud condicionada a $s_0$. Las filas sin salidas quedan indeterminadas.
- **Costo:** contar requiere tiempo proporcional a $T$; formar la matriz requiere hasta $k^2$ divisiones. Guarda hasta $k^2$ conteos y $k$ salidas; al formar la matriz, hasta $k^2$ probabilidades más.
- **Supuestos:** recibe una trayectoria convertida en estados. La interpretación de máxima verosimilitud supone Markov, homogeneidad y filas libres; el conteo no necesita $\mu_0$.

**Corriendo el algoritmo en el corpus.** Con V y C, las 1 620 532 letras del *Quijote* dan 4 conteos y 2 salidas:

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

El algoritmo maximiza $\mathcal L$. Pero si los datos sí vienen de una cadena, ¿encuentra su matriz?

---

## 4 · Simular una matriz conocida

**Piensa: si los datos proceden de una cadena, ¿contar recupera su matriz?**

Sí, bajo condiciones. Para verlo, comparamos con una $P$ conocida.

- **Matriz generadora.** Usamos la matriz V/C del corpus redondeada a tres decimales: filas $(0.181,\ 0.819)$ y $(0.710,\ 0.290)$.
- **Réplica.** Simulamos una trayectoria independiente de $T$ pasos desde C. Cada paso usa MUESTREAR-FILA con un uniforme nuevo.
- **Error.** Medimos la mayor diferencia entre entradas: $\max_{s,s'}|\widehat P(s'\mid s)-P(s'\mid s)|$.
- **Experimento.** Hacemos $n=200$ réplicas por largo $T$, en pasos: 10, 30, 100, 300, 1 000, 3 000 y 10 000 pasos. Usamos la semilla 2028.

**Una réplica, a mano.** `CVCCVV`, la trayectoria muestreada a mano en la página 2, da filas $(1/2,\ 1/2)$ y $(2/3,\ 1/3)$. La mayor diferencia con la matriz generadora es $|0.5-0.181|=0.319$: ese es el error de esa réplica.

**Un punto es la mediana de los errores para un mismo $T$.** La franja abarca del 5 % al 95 %. Con $T=10$, la mediana es 0.210 y la franja va de 0.069 a 0.319.

::: figure {#mkv-c1-recuperar-p title="Contar recupera una matriz conocida: el error baja al crecer el largo T, en pasos"}
![Error de la matriz estimada contra el largo T de la trayectoria, en pasos, con T en escala logarítmica, en 200 réplicas de una cadena conocida que empiezan en C. La mediana del error baja de 0.210 con T = 10 a 0.006 con T = 10 000. La franja del 5 % al 95 % va de 0.069 a 0.319 con T = 10 y de 0.002 a 0.013 con T = 10 000. Ninguna réplica se quedó sin salidas de un estado](../_assets/mkv-c1-recuperar-p.svg)
:::

- **Trayectorias largas.** Con $T=10\,000$, la mediana es 0.006 y la franja va de 0.002 a 0.013.
- **Variabilidad.** Las franjas de $T=100$ y $T=300$ son 0.025–0.130 y 0.009–0.071. Se traslapan: más pasos no garantizan menos error en cada réplica.
- **Filas sin estimar.** Ninguna réplica quedó sin salidas de algún estado, ni con $T=10$. Si ocurriera, se reportaría aparte.

::: theorem {#mkv-c1-teo-recuperar title="Contar recupera la matriz"}
Si los datos proceden de una cadena finita y homogénea con matriz $P$, y cada $N(s)\to\infty$, entonces $\widehat P\to P$ con probabilidad 1.

Estas condiciones son suficientes. La probabilidad se refiere a las trayectorias que genera la cadena.
:::

**Sin la condición falla.** Si V y C fueran absorbentes —de cada uno solo se vuelve a sí mismo— y empiezas en C, toda trayectoria es solo C: aunque $T$ crezca, $N(V)=0$ y la fila V nunca se recupera.

> [!WARNING]
> **Confundir recuperación con validación.** La simulación comprueba el procedimiento bajo el modelo supuesto. **No demuestra que el texto sea una cadena de memoria 1.** En el *Quijote*, contar da la cadena de memoria 1 que hace más probable el texto, no «la matriz del español».

::: exercise {#mkv-c1-ej-sin-salidas title="Imagina una réplica sin vocales"}
Una réplica de $T=10$ empieza en C y nunca pasa por V.

1. **Identifica las filas estimables.** ¿Cuáles puede calcular CONTAR-TRANSICIONES?
2. **Revisa el código.** ¿Qué hace la línea 7 con V?
:::

::: hint {#mkv-c1-pista-sin-salidas of="mkv-c1-ej-sin-salidas" title="Mira las salidas"}
¿Cuánto vale $N(V)$ si V nunca aparece en los primeros $T$ estados?
:::

::: answer {#mkv-c1-resp-sin-salidas of="mkv-c1-ej-sin-salidas"}
1. **Solo estima C.** Su fila queda $(0,\ 1)$.
2. **Omite V.** Como $N(V)=0$, cualquier fila V da la misma verosimilitud (@mkv-c1-teo-maximo). Esto no ocurrió en las 200 réplicas de cada $T$.
:::

En V/C, cada fila tiene datos de sobra. ¿Y si cada letra es un estado?

---

## 5 · Generalizar a k estados

**Piensa: ¿qué cambia si cada letra es un estado?**

Aumenta el tamaño de la matriz y se reparten los datos entre más filas. La regla sigue siendo $N(s,s')/N(s)$ cuando $N(s)>0$.

**Alfabeto de caracteres.** $\Sigma$ es el conjunto de símbolos posibles. Conservamos 27 letras y el espacio; los espacios consecutivos se reducen a uno: $|\Sigma|=28$.

El espacio cambia qué significa un paso. Sin él, «la iglesia» junta «a» con «i»; conservarlo distingue el límite de palabra.

**Con $k$ estados, la matriz es $k\times k$.** Filas y columnas enumeran los mismos estados. Los conteos suman $N(s)$ por fila; al dividir, cada fila estimable suma 1.

- **Tamaño.** Con $28\times28$ hay 784 entradas posibles.
- **Ceros.** En el corpus, 393 pares tienen conteo 0.
- **Pocos datos.** Hay 433 pares con menos de 5 conteos, incluidos esos ceros.
- **Estado ausente.** La «k» no aparece: los datos no determinan su fila.

El juguete tiene datos en ambas filas y un número libre por fila. Eso no se conserva al aumentar el alfabeto: con 28 símbolos hay 27 números libres por fila.

::: exercise {#mkv-c1-ej-tamanos title="Cuenta las entradas"}
Quita el espacio y conserva solo las 27 letras.

1. **Calcula el tamaño.** ¿Qué dimensiones tiene $\widehat P$?
2. **Cuenta los números libres.** ¿Cuántos tiene cada fila?
:::

::: hint {#mkv-c1-pista-tamanos of="mkv-c1-ej-tamanos" title="Filas por columnas"}
¿Cuántas filas y columnas necesitas? ¿Qué entrada queda fijada cuando las demás se conocen y la fila suma 1?
:::

::: answer {#mkv-c1-resp-tamanos of="mkv-c1-ej-tamanos"}
1. **La matriz es $27\times27$.** Hay una fila y una columna por letra.
2. **Cada fila tiene 26 números libres.** El último se obtiene de la suma 1; en general, hay $k-1$.
:::

Con 784 entradas, muchas quedan en 0. ¿Qué hacer con ellas?

---

## 6 · Tratar lo que nunca se vio

**Piensa: ¿un conteo 0 significa que la transición es imposible?**

No necesariamente: puede faltar evidencia. En una fila con salidas, el conteo 0 produce probabilidad 0 y descarta cualquier trayectoria que use ese par.

- **Cero estructural.** La transición es imposible por las reglas del modelo o la normalización: nunca quedan dos espacios consecutivos.
- **Transición no observada.** La «q» tiene $N(q)=32\,155$ salidas, todas hacia «u». No apareció q→a, aunque podría aparecer en «Qatar».
- **Estado sin observaciones.** No hay salidas, como ocurre con «k». La fila queda indeterminada.

El conteo por sí solo no distingue imposibilidad y falta de observaciones.

**Un arreglo, a mano.** En la fila V de la frase hay 2 y 9 salidas. Suma 1 a cada siguiente: quedan 3 y 10, con total 13. En la frase, los siguientes posibles son V y C: $|\Sigma|=k=2$.

- **Fila V.** $(2/11,\ 9/11)$ pasa a $(3/13,\ 10/13)$.
- **Fila C.** $(10/15,\ 5/15)$ pasa a $(11/17,\ 6/17)$.

Esta operación tiene nombre:

::: definition {#mkv-c1-laplace title="Suavizado aditivo de conteos (Laplace)"}
**Qué es.** El suavizado aditivo de conteos suma 1 por símbolo siguiente antes de dividir. La estimación suavizada se escribe $\widetilde p$.

**Cómo se calcula.** Para el estado actual $s$, cada símbolo siguiente $s'$ recibe:

$$
\widetilde p(s'\mid s)=
\frac{N(s,s')+1}{N(s)+|\Sigma|}.
$$

**Qué significa.** Agrega una observación de cada siguiente posible. Los conteos 0 reciben probabilidad positiva; una fila sin datos queda uniforme.

**Qué no es.** No garantiza maximizar la verosimilitud de los datos originales; puede coincidir con el máximo, por ejemplo cuando los conteos de la fila son iguales. Introduce un sesgo hacia la distribución uniforme.
:::

**En el corpus, el denominador de «q» es $32\,155+28=32\,183$:**

- **q→u.** Baja de 1 a $\frac{32\,156}{32\,183}\approx0.9992$.
- **q→a.** Sube de 0 a $\frac{1}{32\,183}\approx0.00003$.
- **Fila «k».** Cada siguiente recibe $\frac{0+1}{0+28}$.

**Cuánto empuja depende de los datos:** mucho en la fila V de la frase, casi nada en la «q».

> [!WARNING]
> **Suavizar no garantiza mejorar.** Evita descartar una trayectoria por un par no observado, pero acerca las filas a la uniforme. **También asigna probabilidad a ceros estructurales si los incluye entre los siguientes posibles.**

::: exercise {#mkv-c1-ej-laplace title="Suaviza una fila corta"}
En `conla`, $N(V,V)=0$ y $N(V,C)=1$.

1. **Estima sin suavizar.** ¿Cuál es la fila V de $\widehat P$?
2. **Aplica Laplace.** ¿Cuál es su fila de $\widetilde p$, con $|\Sigma|=2$?
:::

::: hint {#mkv-c1-pista-laplace of="mkv-c1-ej-laplace" title="Suma uno arriba y dos abajo"}
Si cada siguiente gana 1, ¿cuánto aumenta el denominador?
:::

::: answer {#mkv-c1-resp-laplace of="mkv-c1-ej-laplace"}
1. **Sin suavizar, queda $(0,\ 1)$.** Solo se observó V→C.
2. **Con Laplace, queda $(1/3,\ 2/3)$.** Las entradas son $\frac{0+1}{1+2}$ y $\frac{1+1}{1+2}$; con un solo dato, el cambio es grande.
:::

Más filas vacías aparecen al meter más pasado en el estado.

---

## 7 · Decidir cuánta memoria lleva el estado

**Piensa: ¿qué puedes cambiar si la letra actual no basta para modelar la siguiente?**

Puedes incluir más pasado en el estado. **Qué es el estado lo decides tú:** es una decisión de modelado, no un dato del texto. En [[escribir-el-juego|Escribir el juego]], el turno entró al estado porque el tablero solo no bastaba.

::: definition {#mkv-c1-memoria title="La memoria de un modelo de texto"}
**Qué es.** La memoria $h$ indica cuántos símbolos forman el contexto usado como estado.

**Cómo se calcula.** Se cuentan pares (contexto, siguiente). Con $h\ge1$, al avanzar el contexto pierde su primer símbolo y agrega el nuevo: «con» pasa a «onl». Con $h=0$, el contexto queda vacío y siempre se usa la misma distribución de símbolos.

**Qué significa.** Memoria 0 usa frecuencias de símbolos: unigrama. Memoria 1 usa pares: bigrama; memoria 2 usa tríos: trigrama.

**Qué no es.** No es la profundidad de búsqueda. Cambia qué información contiene el estado.
:::

Un estado sin observaciones es ahora un contexto sin observaciones.

**La tabla útil tiene $|\Sigma|^h$ filas y $|\Sigma|$ columnas.** Cada fila corresponde a un contexto; cada columna, al símbolo siguiente. Con memoria 2 son 784 contextos por 28 siguientes.

La cadena sobre contextos sí tiene matriz cuadrada. De «la» solo puede pasar a un contexto que empiece con «a».

**Laplace se aplica por símbolo siguiente.** Escribimos $\widetilde p(z\mid s)=\dfrac{N(s,z)+1}{N(s)+|\Sigma|}$, con $s$ el contexto y $z\in\Sigma$ el símbolo siguiente: se suma 1 en cada una de las $|\Sigma|$ columnas. El siguiente contexto $s'$ se obtiene deslizando $s$ y agregando $z$. Sumar 1 a las 784 columnas de contextos permitiría «la»→«de», una transición imposible.

**Para diagnosticar escasez, contamos en la primera mitad del corpus y probamos en la segunda.** Esta aporta cerca de un millón de transiciones (998 563 con memoria 1). Cada barra de @mkv-c1-ceros mide qué fracción de pares (contexto, siguiente) de prueba no apareció al contar.

::: figure {#mkv-c1-ceros title="Lo que nunca se vio, por memoria"}
![Barras horizontales por memoria, con la fracción de transiciones de la segunda mitad del corpus nunca vistas en la primera. Memoria 0: 0 %, 0 de 998 564, contextos vistos 1 de 1. Memoria 1: 0.003 %, 29 de 998 563, contextos vistos 27 de 28. Memoria 2: 0.072 %, 718 de 998 562, contextos vistos 379 de 784. Memoria 3: 0.570 %, 5 694 de 998 561, contextos vistos 3 328 de 21 952. Las barras están a escala de la mayor (memoria 3). Al pie: solo diagnostica escasez, no elige la memoria](../_assets/mkv-c1-ceros.svg)
:::

- **Las fracciones aumentan en este corpus.** Son 0.003 %, 0.072 % y 0.570 % para memorias 1, 2 y 3.
- **Es poca, todavía.** Con memoria 3, menos de una transición de cada 100 es nueva: el *Quijote* es largo.
- **Los contextos crecen rápidamente.** Se observaron 379 de 784 con memoria 2; con memoria 3, 3 328 de 21 952.
- **Algunas ausencias son estructurales.** Tres espacios seguidos no existen tras normalizar.

> [!WARNING]
> **Elegir memoria por los ceros.** Memoria 0 tiene 0 % de transiciones no vistas, pero ignora la letra anterior. **La figura @mkv-c1-ceros diagnostica escasez; no elige la memoria.**

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
2. **Hay 25 transiciones.** Para una trayectoria de $T$ pasos, hay $T-h+1$ pares cuando alcanza para formar el contexto y un siguiente.
:::

Con esto tienes todo para ajustar una cadena por tu cuenta.

---

## Ejercicios

::: exercise {#mkv-c1-ej-tres-simbolos title="Ajusta una cadena de tres símbolos"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Observaste `abacabbcabac`, un texto con símbolos a, b y c. **Cambia una idea:** usa tres estados en lugar de dos, con memoria 1.

1. **Cuenta.** Indica cuántas transiciones hay, construye la tabla $3\times3$ y calcula las salidas de cada símbolo.
2. **Estima.** Escribe $\widehat P$.
3. **Interpreta los ceros.** Señálalos y explica si puedes saber que son estructurales.
4. **Suaviza.** Aplica Laplace a las filas a y c.
:::

::: hint {#mkv-c1-pista-tres-simbolos-1 of="mkv-c1-ej-tres-simbolos" title="Pista 1 · ¿Qué letra no tiene siguiente?"}
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

Las salidas son $N(a)=5$, $N(b)=4$ y $N(c)=2$; suman 11.

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

**4. Laplace.** El alfabeto tiene $|\Sigma|=3$.

- **Fila a.** Las entradas $\frac{0+1}{8}$, $\frac{3+1}{8}$ y $\frac{2+1}{8}$ dan $(1/8,\ 1/2,\ 3/8)$.
- **Fila c.** Las entradas $\frac{2+1}{5}$, $\frac{0+1}{5}$ y $\frac{0+1}{5}$ dan $(3/5,\ 1/5,\ 1/5)$.
:::

::: exercise {#mkv-c1-ej-ceros title="Lee la figura de ceros con menos texto"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Usa @mkv-c1-ceros. **Cambia una idea:** cuenta solo con unas páginas de la primera mitad y conserva la segunda como prueba. Responde 1–3 con la figura, y 4 con esa idea.

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
**1. Memoria 3.** Tiene 0.570 %: menos de una transición de cada 100.

**2. Menos de la mitad.** Se observaron 379 de 784; la mitad sería 392.

**3. Dos ausencias distintas.** Tres espacios seguidos son imposibles tras normalizar. «kia» es un contexto sin observaciones en este corpus, que no contiene «k»; podría aparecer en otro texto.

**4. Las fracciones no pueden bajar.** Quitar datos de conteo no agrega pares vistos; pueden quedar iguales. Lo esperable es que suban, sobre todo con memoria alta: hay 21 952 contextos posibles con memoria 3. Incluso memoria 0 puede dejar de ver algún símbolo.

**5. No basta.** Memoria 0 tiene 0 % de transiciones no vistas, pero ignora la dependencia entre «q» y «u». Elegir requiere evaluar predicciones en datos reservados.
:::

**Punto de control:** deberías poder contar pares, estimar filas con salidas y justificar su máxima verosimilitud condicionada. También, distinguir los tres casos de ausencia, aplicar Laplace y explicar el costo de aumentar la memoria.

---

## Para profundizar

### Elegir la memoria con datos reservados

Ajusta y suaviza cada memoria con la primera mitad. En la segunda, promedia $-\log\widetilde p(z\mid s)$, con $s$ el contexto: es la pérdida logarítmica, con logaritmo natural. Asignar 0.9 al símbolo que salió cuesta ≈0.105; asignar 0.1 cuesta ≈2.303. Un promedio menor indica mejores predicciones sobre esos datos reservados.

- **Suavizado.** Evita que una transición no observada produzca $\log 0$ y una pérdida infinita.
- **Comparación.** Más memoria representa dependencias adicionales, pero no garantiza menor pérdida en datos reservados.

---

## Lo que hay que llevarse

- **A mano y con algoritmo.** Las 26 transiciones dan filas $(2/11,\ 9/11)$ y $(2/3,\ 1/3)$. La regla general es $N(s,s')/N(s)$, solo si $N(s)>0$.
- **Máxima verosimilitud.** Con Markov, homogeneidad, filas libres e inicio condicionado, contar maximiza $\mathcal L$. En la frase da $3.88\times10^{-7}$, frente a $1.49\times10^{-8}$ con filas de ½.
- **Simulación.** En 200 réplicas por longitud, la mediana del error pasa de 0.210 ($T=10$) a 0.006 ($T=10\,000$). Si los datos vienen de esa cadena homogénea y cada $N(s)$ crece sin límite, contar recupera $P$ con probabilidad 1. Estas condiciones son suficientes.
- **Ausencias y suavizado.** Con 28 símbolos hay 784 entradas posibles y 393 conteos 0; «k» queda sin fila estimada. Laplace sesga hacia la uniforme: q→u baja a $\frac{32\,156}{32\,183}$.
- **Memoria.** En el corpus, las transiciones no vistas pasan de 0.003 % a 0.570 % entre memorias 1 y 3. Los contextos posibles llegan a 21 952; la figura diagnostica escasez, sin elegir memoria.

Continúa con [[mkv-predecir|Predecir]].
