---
id: mkv-predecir
title: "Predecir"
nav_title: "Predecir"
summary: "Si la cadena empieza en C, ¿qué tan probable es estar en V exactamente t pasos después? A mano con un árbol y con un vector fila por la matriz, con el algoritmo PREDECIR y con 10 000 réplicas simuladas y su error estándar."
status: ready
estimated_time: 30m
tags: [markov]
---

# Predecir

**Si $S_0=C$, ¿cuál es la probabilidad de que $S_3=V$, exactamente tres transiciones después?**

Al terminar tendrás:

- **Una predicción a mano.** Calcularás la probabilidad de cada estado en el paso $t$, con un árbol y un vector fila.
- **La regla de un paso.** Derivarás $\mu_{t+1}=\mu_t\widehat P$ con probabilidad total, propiedad de Markov y homogeneidad.
- **El algoritmo PREDECIR.** Seguirás su pseudocódigo, su Python y su traza; justificarás el costo $t\cdot k^2$.
- **Una comprobación por simulación.** Compararás la cuenta con 10 000 réplicas y su error estándar.
- **El alcance del resultado.** Distinguirás una predicción de la cadena ajustada de una afirmación sobre el idioma.

## Lo que traes

- **Probabilidad total.** En [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] sumaste casos disjuntos que cubren todo. También viste cómo las frecuencias de repeticiones independientes se acercan a su probabilidad.
- **La cadena.** En [[mkv-el-problema-de-markov|El problema de Markov]] definiste $(\mathcal S,\mu_0,P)$. Con propiedad de Markov y homogeneidad, una trayectoria tiene probabilidad $\mu_0(s_0)\prod_{j=0}^{t-1}P(s_{j+1}\mid s_j)$.
- **El muestreo.** MUESTREAR-FILA elige el siguiente estado con un uniforme $u$. Una réplica es una trayectoria simulada, independiente de las demás.
- **Las matrices ajustadas.** En [[mkv-ajustar-contando|Ajustar contando]], la frase dio filas $(2/11,\ 9/11)$ y $(2/3,\ 1/3)$. Las del *Quijote*, redondeadas, son $(0.181,\ 0.819)$ y $(0.710,\ 0.290)$.

> **Modelo y datos.** Trabajamos con cadenas finitas y homogéneas. Todo lo que calcula esta página es lo que haría la cadena ajustada $\widehat P$: una predicción del modelo, no una afirmación sobre el español.

---

## 1 · Predecir a mano con árbol y vector

**Piensa: si empiezas en C, ¿de cuántas maneras puedes estar en V dos pasos después?**

De dos maneras: pasando por V o por C. Con la cadena de la frase, cada trayectoria tiene la probabilidad que resulta de multiplicar sus flechas. El árbol de @mkv-c1-arbol-2-pasos las muestra todas.

::: figure {#mkv-c1-arbol-2-pasos title="Dos pasos desde C: cuatro caminos, dos terminan en V"}
![Árbol de dos pasos desde C con la matriz de la frase. Primer paso: a V con 2/3 y a C con 1/3. Desde V: a V con 2/11 y a C con 9/11; desde C: a V con 2/3 y a C con 1/3. Hojas: C, V, V vale 4/33; C, V, C vale 6/11; C, C, V vale 2/9; C, C, C vale 1/9. Las dos hojas V, con borde grueso, suman Pr(S₂ = V) = 4/33 + 2/9 = 34/99](../_assets/mkv-c1-arbol-2-pasos.svg)
:::

- **Camino C, V, V.** Su probabilidad es $\tfrac{2}{3}\cdot\tfrac{2}{11}=\tfrac{4}{33}$.
- **Camino C, V, C.** Su probabilidad es $\tfrac{2}{3}\cdot\tfrac{9}{11}=\tfrac{6}{11}$.
- **Camino C, C, V.** Su probabilidad es $\tfrac{1}{3}\cdot\tfrac{2}{3}=\tfrac{2}{9}$.
- **Camino C, C, C.** Su probabilidad es $\tfrac{1}{3}\cdot\tfrac{1}{3}=\tfrac{1}{9}$.

Los cuatro caminos son disjuntos y cubren todo. Por probabilidad total, sumamos las hojas que terminan en V:

$$
\Pr(S_2=V\mid S_0=C)=\frac{4}{33}+\frac{2}{9}=\frac{34}{99}.
$$

::: exercise {#mkv-c1-ej-hojas-c title="Suma las otras hojas"}
Con el mismo árbol, calcula $\Pr(S_2=C\mid S_0=C)$. ¿Cuánto suman las cuatro hojas?
:::

::: hint {#mkv-c1-pista-hojas-c of="mkv-c1-ej-hojas-c" title="Mira el último estado"}
¿Qué caminos terminan en C?
:::

::: answer {#mkv-c1-resp-hojas-c of="mkv-c1-ej-hojas-c"}
Terminan en C los caminos C, V, C y C, C, C. Sus probabilidades suman $\tfrac{6}{11}+\tfrac{1}{9}=\tfrac{65}{99}$.

Las cuatro hojas suman $\tfrac{34}{99}+\tfrac{65}{99}=1$: en el paso 2 la cadena está en algún estado.
:::

**El árbol crece demasiado.** Con tres pasos tiene $2^3$ hojas; con $k$ estados y $t$ pasos, hasta $k^t$. Por la propiedad de Markov, los caminos que llegan al mismo estado en el mismo paso comparten sus probabilidades siguientes. Basta guardar cuánta probabilidad llega a cada estado.

**Guardamos un vector fila.** En el orden V, C, empezar en C se escribe $\mu_0=(0,\ 1)$. La matriz conserva ese orden: fila = desde dónde; columna = hacia dónde.

Para obtener cada entrada del paso 1, multiplicamos el renglón por una columna: entrada por entrada, y sumamos.

$$
\begin{aligned}
\mu_1
&=(0,\ 1)\begin{pmatrix}2/11 & 9/11\\ 2/3 & 1/3\end{pmatrix}\\
&=\left(\tfrac{2}{3},\ \tfrac{1}{3}\right).
\end{aligned}
$$

- **Entrada V.** Usa la columna V: $0\cdot\tfrac{2}{11}+1\cdot\tfrac{2}{3}=\tfrac{2}{3}$.
- **Entrada C.** Usa la columna C: $0\cdot\tfrac{9}{11}+1\cdot\tfrac{1}{3}=\tfrac{1}{3}$.

**Desde un estado seguro, el primer paso copia su fila.** Para el paso 2, usamos $\mu_1$:

$$
\begin{aligned}
\mu_2(V)
&=\tfrac{2}{3}\cdot\tfrac{2}{11}+\tfrac{1}{3}\cdot\tfrac{2}{3}\\
&=\tfrac{4}{33}+\tfrac{2}{9}=\tfrac{34}{99},\\
\mu_2(C)
&=\tfrac{2}{3}\cdot\tfrac{9}{11}+\tfrac{1}{3}\cdot\tfrac{1}{3}\\
&=\tfrac{6}{11}+\tfrac{1}{9}=\tfrac{65}{99}.
\end{aligned}
$$

**Da lo mismo que el árbol.** Cada producto corresponde a una hoja; sumamos las que terminan en el mismo estado. Así, $\mu_2=(34/99,\ 65/99)$.

**El paso 3 responde la pregunta.** Multiplicamos $\mu_2$ por cada columna:

$$
\begin{aligned}
\mu_3(V)
&=\tfrac{34}{99}\cdot\tfrac{2}{11}+\tfrac{65}{99}\cdot\tfrac{2}{3}\\
&=\tfrac{1634}{3267},\\
\mu_3(C)
&=\tfrac{34}{99}\cdot\tfrac{9}{11}+\tfrac{65}{99}\cdot\tfrac{1}{3}\\
&=\tfrac{1633}{3267}.
\end{aligned}
$$

Con la cadena de la frase y $S_0=C$, estar en V en el paso 3 tiene probabilidad $1634/3267$. Es casi mitad y mitad.

::: definition {#mkv-c1-distribucion title="La distribución en el paso t"}
**Qué es.** $\mu_t$ es la distribución del estado en el paso $t$. Es un vector fila: $\mu_t(s)=\Pr(S_t=s)$, con entradas no negativas que suman 1.

**Cómo se calcula.** En la cadena finita y homogénea ajustada, multiplicamos $\mu_t$ por cada columna de $\widehat P$:

$$
\mu_{t+1}(s')=\sum_{s\in\mathcal S}\mu_t(s)\,\widehat P(s'\mid s).
$$

**Qué significa.** Describe las probabilidades antes de simular la cadena. Con la matriz de la frase, desde C, $\mu_2=(34/99,\ 65/99)$.

**Qué no es.** Estar en V **en el paso $t$** difiere de pasar por V alguna vez antes. Tampoco es la frecuencia de vocales del texto.
:::

La cuenta funcionó tres veces; falta justificar por qué funciona en cada paso.

---

## 2 · Derivar la regla de un paso

**Piensa: ¿qué permite pasar de $\mu_t$ a $\mu_{t+1}$ usando siempre la misma matriz?**

La propiedad de Markov y la homogeneidad permiten usar una matriz fija. La probabilidad total reúne los casos:

$$
\begin{aligned}
\Pr(S_{t+1}=s')
&=\sum_s\Pr(S_t=s)\,
  \Pr(S_{t+1}=s'\mid S_t=s)\\
&=\sum_s\mu_t(s)\,P(s'\mid s).
\end{aligned}
$$

- **Probabilidad total.** Los eventos $\{S_t=s\}$ son disjuntos y cubren todo. Omitimos los de probabilidad 0: no aportan y su condicional no está definida.
- **Propiedad de Markov.** Dado $S_t=s$, conocer la historia anterior no cambia la probabilidad del siguiente estado.
- **Homogeneidad.** Esa probabilidad es la misma en cada paso: $P(s'\mid s)$.

::: theorem {#mkv-c1-teo-predecir title="La distribución avanza multiplicando por la matriz"}
En una cadena finita y homogénea con matriz $P$, para todo $t\ge0$:

$$
\begin{aligned}
\mu_{t+1}&=\mu_tP,\\
\mu_t&=\mu_0P^t.
\end{aligned}
$$

Estas condiciones son suficientes. $P^t$ es $P$ multiplicada por sí misma $t$ veces; con $t=0$, conservamos $\mu_0$.
:::

**En la frase,** $\mu_3=\mu_0\widehat P^{\,3}$ reproduce la cuenta a mano. El teorema se aplica a la cadena ajustada, cuya matriz es $\widehat P$.

**Sin una fila fija, falla la regla.** En el proceso que repite C C V, las dos C tienen siguientes distintos. Saber «estoy en C» no basta para elegir una fila que describa ambos pasos.

**Con $k$ estados, hacemos la misma cuenta.** $\mu_t$ tiene $k$ entradas y $P$ mide $k\times k$. Cada entrada nueva suma $k$ productos: un paso requiere $k^2$ multiplicaciones. El árbol tiene hasta $k^t$ hojas; el vector conserva $k$ números.

**El vector va a la izquierda.** Aquí usamos vectores fila y multiplicamos $\mu_tP$. Algunos libros usan vectores columna: multiplican $P^{\mathsf T}$ por el vector.

**El atajo de dos estados tiene un límite.** Basta conocer $\Pr(S_t=V)$ porque la otra entrada es su complemento. Con $k$ estados hacen falta $k-1$ números.

> [!WARNING]
> **Confundir la predicción con el idioma.** Desde C, $\mu_3(V)=1634/3267$ corresponde a la cadena ajustada a la frase. **La frecuencia de vocales tres letras después de una consonante se mide en el texto.** El texto no tiene por qué ser una cadena.

::: exercise {#mkv-c1-ej-dos-matrices title="Cambia la matriz a medio camino"}
Imagina que el paso 1 usa $\widehat P$ y el paso 2 usa otra matriz, $P'$. ¿Cómo escribes $\mu_2$? ¿Sigue valiendo $\mu_2=\mu_0\widehat P^{\,2}$?
:::

::: hint {#mkv-c1-pista-dos-matrices of="mkv-c1-ej-dos-matrices" title="Un paso a la vez"}
¿Qué matriz usa la regla para pasar de $\mu_1$ a $\mu_2$?
:::

::: answer {#mkv-c1-resp-dos-matrices of="mkv-c1-ej-dos-matrices"}
Queda $\mu_2=\mu_1P'=\mu_0\widehat P P'$. Si cada paso usa su matriz, conservamos el producto. Sin homogeneidad, la potencia $\mu_0\widehat P^{\,2}$ ya no está garantizada.
:::

La regla ya está justificada; podemos convertirla en un procedimiento para cualquier $k$ y $t$.

---

## 3 · Predecir con un algoritmo

**Piensa: ¿qué tiene que recordar un programa entre un paso y el siguiente?**

Debe conservar el vector actual y la matriz. En la cadena finita y homogénea, el vector resume las probabilidades necesarias para avanzar.

> **Dado:** una cadena finita y homogénea con $k$ estados, matriz $P$ de $k\times k$ y distribución inicial $\mu_0$. El número de pasos $t\ge0$ es entero.
>
> **Encontrar:** $\mu_t$ (@mkv-c1-distribucion), la distribución del estado en el paso $t$.

### El mapa de PREDECIR

- **Qué calcula:** obtiene la distribución $\mu_t=\mu_0P^t$.
- **Qué guarda:** conserva la matriz, el vector actual y espacio para el siguiente.
- **Cómo avanza:** reemplaza $\mu$ por $\mu P$, multiplicando el renglón por cada columna.
- **Qué devuelve al terminar:** entrega $\mu_t$ después de exactamente $t$ multiplicaciones de vector por matriz.

::: figure {#mkv-c1-flujo-predecir title="Predecir, en palabras"}
![Diagrama de flujo de predecir, en palabras: empieza con μ₀, un vector fila; multiplica por P̂, μ ← μ P̂; pregunta si ya van t pasos; si no, vuelve a multiplicar; si sí, devuelve μₜ. Al pie: cada paso cuesta k² productos con k estados](../_assets/mkv-c1-flujo-predecir.svg)
:::

```text
INPUT   los k estados de 𝒮, en un orden fijo
        (V, C en la frase); P, de k×k, con filas
        y columnas en ese orden; μ_0, un vector
        fila de k entradas que suma 1; t ≥ 0.
OUTPUT  μ_t, la distribución en el paso t.

 1 function PREDECIR(P, μ_0, t)
 2   μ ← μ_0                  # el paso 0
 3   for j ← 1 to t           # un paso por vuelta
 4     nuevo ← k ceros        # el μ del paso j
 5     for each s′ in 𝒮       # una columna
 6       for each s in 𝒮      # un renglón
 7         nuevo(s′) ← nuevo(s′) + μ(s)·P(s′ | s)
 8     μ ← nuevo              # ahora μ = μ_j
 9   return μ                 # μ_t
```

**Gemelo Python.** Los comentarios indican la línea del pseudocódigo. Los estados ocupan las posiciones $0,\dots,k-1$, en el orden de las filas de `P`.

```python
from fractions import Fraction

def predecir(P, mu0, t):                  # (1)
    k = len(mu0)          # estados 0, …, k − 1, como en P
    mu = list(mu0)                        # (2) paso 0
    for j in range(1, t + 1):             # (3)
        nuevo = [0] * k                   # (4)
        for s2 in range(k):               # (5) columna s′
            for s in range(k):            # (6) renglón s
                nuevo[s2] += mu[s] * P[s][s2]  # (7)
        mu = nuevo                        # (8) ahora μ_j
    return mu                             # (9) μ_t

P_gorro = [[Fraction(2, 11), Fraction(9, 11)],   # fila V
           [Fraction(2, 3), Fraction(1, 3)]]     # fila C
print(predecir(P_gorro, [0, 1], 3))
# [Fraction(1634, 3267), Fraction(1633, 3267)]
```

**Cada pieza, en su línea:**

- **Línea 2.** Copia $\mu_0$; con $t=0$, devuelve esa distribución.
- **Líneas 4 a 7.** Multiplican el renglón por cada columna. `P[s][s2]` indica fila $s$, columna $s'$.
- **Línea 8.** Sustituye el vector al terminar la vuelta; así evita mezclar $\mu_{j-1}$ con $\mu_j$.

**Cómo leer la traza.** Usamos la matriz de la frase y empezamos en C. El renglón 0 muestra la inicialización; cada renglón siguiente muestra $\mu$ al terminar la vuelta $j$.

| j | μ(V) | μ(C) | Qué pasó |
|---:|---|---|---|
| 0 | 0 | 1 | Línea 2: empieza en C |
| 1 | 2/3 | 1/3 | Copia la fila C |
| 2 | 34/99 | 65/99 | Suma las hojas del árbol |
| 3 | 1634/3267 | 1633/3267 | Responde la pregunta |

- **Paso 1.** El 1 de $\mu_0$ está en C, así que el producto conserva solo esa fila.
- **Paso 3.** Devuelve $(1634/3267,\ 1633/3267)$; las entradas siguen sumando 1.

::: exercise {#mkv-c1-ej-traspuesta title="Encuentra el índice cambiado"}
Alguien escribió la línea 7 con $P(s\mid s')$ en lugar de $P(s'\mid s)$. Corre una vuelta con la matriz de la frase desde $\mu_0=(0,\ 1)$.

1. **Calcula.** ¿Qué vector obtiene?
2. **Diagnostica.** ¿Cómo sabes, sin el resultado correcto, que está mal?
:::

::: hint {#mkv-c1-pista-traspuesta of="mkv-c1-ej-traspuesta" title="Qué entradas sobreviven"}
Con $\mu=(0,\ 1)$, ¿qué entradas de $\widehat P$ se multiplican por 1?
:::

::: answer {#mkv-c1-resp-traspuesta of="mkv-c1-ej-traspuesta"}
1. **Obtiene $(9/11,\ 1/3)$.** Copia la columna C de $\widehat P$.
2. **No suma 1.** $9/11$ y $1/3$ juntos pasan de 1. Las columnas de $P$ no tienen por qué sumar 1.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina tras $t$ vueltas si $t$ es un entero no negativo. Si $\mu_0$ es una distribución y $P$ tiene filas de probabilidades, cada $\mu_j$ sigue siendo una distribución.
- **Número que da:** con la matriz de la frase, desde C y con $t=3$, devuelve $(1634/3267,\ 1633/3267)$.
- **Garantía:** bajo las condiciones de @mkv-c1-teo-predecir, devuelve $\mu_0P^t$. Con fracciones es exacto; con decimales interviene el redondeo.
- **Costo:** ejecuta $k^2$ multiplicaciones por vuelta, para un total de $t\cdot k^2$. Guarda $k^2$ entradas de la matriz y dos vectores de $k$ entradas.
- **Supuestos:** usa la misma $P$ en todos los pasos, con entradas en $[0,1]$ y filas que suman 1. Predice la cadena que recibe.

La cuenta con fracciones es exacta; la simulación permite contrastarla mediante réplicas.

---

## 4 · Simular réplicas para comprobar la cuenta

**Piensa: si no confiaras en la multiplicación, ¿cómo estimarías $\Pr(S_3=V)$?**

Simularías la cadena muchas veces y contarías cuántas réplicas terminan en V en ese paso. Para un paso fijo, la ley de los grandes números permite aproximar su probabilidad con réplicas independientes del mismo modelo.

**El experimento usa la matriz del corpus:**

- **Matriz.** Usamos $\widehat P$ del *Quijote*, con filas $(0.181,\ 0.819)$ y $(0.710,\ 0.290)$.
- **Réplicas.** Simulamos $n=10\,000$ trayectorias independientes de 8 pasos desde C, con semilla 2030; otras 10 000 empiezan en V, con semilla 2029. Cada paso usa MUESTREAR-FILA con un $u$ nuevo.
- **Un punto.** Muestra la fracción de réplicas que están en V en el paso $t$.
- **Una línea.** Muestra la cuenta $\mu_0\widehat P^{\,t}$ de PREDECIR, con la misma matriz e inicio.

**Cuánto ruido esperar.** En un paso fijo, cada réplica está en V con probabilidad $p$. La fracción simulada varía alrededor de $p$.

::: definition {#mkv-c1-error-estandar title="El error estándar de una fracción simulada"}
**Qué es.** El error estándar (*standard error*) mide el tamaño típico de la diferencia entre la fracción simulada y la probabilidad $p$.

**Cómo se calcula.** Para $n$ réplicas independientes, cada una con probabilidad $p$ de estar en V en el paso elegido:

$$
\sqrt{\frac{p(1-p)}{n}}.
$$

**Qué significa.** Con el mismo $p$, cuadruplicar $n$ reduce el error estándar a la mitad. Como $p(1-p)\le1/4$, con $n=10\,000$ el error estándar no supera $0.005$. Diferencias de uno o dos errores estándar son lo esperable.

**Qué no es.** No es una cota para la diferencia observada: puede superar uno o dos errores estándar. Tampoco mide si el modelo describe el texto.
:::

::: figure {#mkv-c1-mu-t title="La cuenta y las réplicas coinciden dentro del error, paso a paso"}
![Probabilidad de estar en V en el paso t, de t = 0 a 8, con la matriz del corpus. Arriba, la cuenta μ₀P̂ᵗ como línea y la fracción de 10 000 réplicas en V como marcas. Desde V: cuenta 1.000, 0.181, 0.615, 0.385, 0.507, 0.442, 0.476, 0.458, 0.468; réplicas 1.000, 0.180, 0.611, 0.392, 0.498, 0.438, 0.476, 0.460, 0.464. Desde C: cuenta 0.000, 0.710, 0.334, 0.533, 0.428, 0.484, 0.454, 0.470, 0.462; réplicas 0.000, 0.712, 0.326, 0.543, 0.424, 0.485, 0.452, 0.467, 0.470. Abajo, réplicas menos cuenta, con una franja de ±2 errores estándar (±0.010); la mayor diferencia es 0.010, unos 2.0 errores estándar](../_assets/mkv-c1-mu-t.svg)
:::

- **Cuenta desde C.** En los pasos 1, 2 y 3 da 0.710, 0.334 y 0.533. Con la cadena del corpus, la respuesta para el paso 3 es 0.533.
- **Réplicas desde C.** Las fracciones son 0.712, 0.326 y 0.543 en esos mismos pasos.
- **Mayor diferencia observada.** Es 0.010, en el paso 3 desde C: unos 2.0 errores estándar. Ningún punto se sale de la franja del panel inferior.
- **Paso 0.** Es exacto porque todas las réplicas de cada grupo empiezan en el mismo estado.

**La simulación se aproxima, no coincide.** En este experimento, las diferencias son del tamaño que anticipa el error estándar.

> [!WARNING]
> **Confundir comprobar la cuenta con validar el modelo.** Las réplicas salen de la misma $\widehat P$ que usa PREDECIR. **La concordancia comprueba el procedimiento; no demuestra que el *Quijote* sea una cadena de memoria 1.**

**En esta matriz las curvas se acercan.** En el paso 8, la cuenta desde V da 0.468; desde C, 0.462. ¿Pasa con cualquier matriz? ¿Hacia qué valor? Estas cuentas dejan abiertas ambas preguntas.

::: exercise {#mkv-c1-ej-paso-cero title="Explica el punto exacto"}
Desde C, el punto del paso 0 vale 0.000 en la cuenta y en las réplicas. ¿Por qué no tiene ruido? ¿Cuánto vale ahí su error estándar?
:::

::: hint {#mkv-c1-pista-paso-cero of="mkv-c1-ej-paso-cero" title="Dónde empieza cada réplica"}
¿Qué $p$ corresponde a V en el paso 0 si $\mu_0=(0,\ 1)$?
:::

::: answer {#mkv-c1-resp-paso-cero of="mkv-c1-ej-paso-cero"}
Todas las réplicas empiezan en C, así que ninguna está en V. Con $p=0$, el error estándar es $\sqrt{0\cdot1/n}=0$.
:::

Ya puedes calcular una predicción y contrastarla con réplicas; toca aplicar ambas ideas a variantes.

---

## Ejercicios

::: exercise {#mkv-c1-ej-tres-estados title="Predice dos pasos con tres estados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una cadena homogénea tiene estados x, y, z, en ese orden. **Cambia una idea:** usa tres estados; el inicio se reparte entre dos de ellos.

$$
P=\begin{pmatrix}
1/2 & 1/4 & 1/4\\
1/3 & 0 & 2/3\\
0 & 1/2 & 1/2
\end{pmatrix},
\qquad
\mu_0=\left(\tfrac12,\ \tfrac12,\ 0\right).
$$

1. **Lee la matriz.** ¿Qué dicen sus dos ceros?
2. **Calcula $\mu_1$.** Haz el renglón por cada columna.
3. **Calcula $\mu_2$.** Comprueba que suma 1.
4. **Generaliza.** Escribe $\mu_t$ para cualquier $t$ y cuántas multiplicaciones cuesta.

:::

::: hint {#mkv-c1-pista-tres-estados-1 of="mkv-c1-ej-tres-estados" title="Pista 1 · ¿Qué renglones cuentan?"}
¿Qué entrada de $\mu_0$ es 0? ¿Qué fila de $P$ deja de aportar por eso en el primer paso?
:::

::: hint {#mkv-c1-pista-tres-estados-2 of="mkv-c1-ej-tres-estados" title="Pista 2 · ¿Usaste el vector correcto?"}
¿Suman 1 tus dos vectores? Para el segundo paso, ¿multiplicaste $\mu_1$ y no $\mu_0$?
:::

::: answer {#mkv-c1-resp-tres-estados of="mkv-c1-ej-tres-estados" title="Respuesta · Dos pasos con tres estados"}
**1. Ceros.** $P(y\mid y)=0$ impide quedarse en y; $P(x\mid z)=0$ impide pasar de z a x. Ambas transiciones son imposibles en el modelo.

**2. Primer paso.** La fila z no aporta porque $\mu_0(z)=0$:

$$
\begin{aligned}
\mu_1(x)&=\tfrac12\cdot\tfrac12+\tfrac12\cdot\tfrac13=\tfrac{5}{12},\\
\mu_1(y)&=\tfrac12\cdot\tfrac14+\tfrac12\cdot0=\tfrac18,\\
\mu_1(z)&=\tfrac12\cdot\tfrac14+\tfrac12\cdot\tfrac23=\tfrac{11}{24}.
\end{aligned}
$$

**3. Segundo paso.** Ahora las tres filas aportan, multiplicadas por sus entradas en $\mu_1$:

$$
\begin{aligned}
\mu_2(x)
&=\tfrac{5}{12}\cdot\tfrac12+\tfrac18\cdot\tfrac13+\tfrac{11}{24}\cdot0\\
&=\tfrac14,\\
\mu_2(y)
&=\tfrac{5}{12}\cdot\tfrac14+\tfrac18\cdot0+\tfrac{11}{24}\cdot\tfrac12\\
&=\tfrac13,\\
\mu_2(z)
&=\tfrac{5}{12}\cdot\tfrac14+\tfrac18\cdot\tfrac23+\tfrac{11}{24}\cdot\tfrac12\\
&=\tfrac{5}{12}.
\end{aligned}
$$

Así, $\mu_2=(1/4,\ 1/3,\ 5/12)$, que suma 1.

**4. General.** Como la cadena es finita y homogénea, $\mu_t=\mu_0P^t$. PREDECIR requiere $k^2=3^2$ multiplicaciones por paso: $t\cdot3^2$ en total.
:::

::: exercise {#mkv-c1-ej-leer-simulacion title="Lee una simulación con pocas réplicas"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Repetiste la simulación desde C con la matriz del corpus. **Cambia una idea:** usaste $n=400$ réplicas independientes en lugar de 10 000, con semilla 2031.

La fracción en V fue 0.693, 0.352 y 0.512 en los pasos 1, 2 y 3. La cuenta da 0.710, 0.334 y 0.533.

1. **Calcula el error estándar.** Usa $p$ igual a la cuenta de cada paso.
2. **Compara.** ¿Cada diferencia cabe en dos errores estándar? ¿En uno?
3. **Explica el tamaño.** ¿Por qué los errores estándar son mayores que con 10 000 réplicas? ¿Cuánto mayores?
4. **Delimita.** ¿Esta concordancia dice algo sobre el *Quijote*?

:::

::: hint {#mkv-c1-pista-leer-simulacion-1 of="mkv-c1-ej-leer-simulacion" title="Pista 1 · ¿Qué va en la fórmula?"}
¿Qué $p$ y qué $n$ usas en cada paso? ¿Contra qué error estándar comparas cada diferencia?
:::

::: hint {#mkv-c1-pista-leer-simulacion-2 of="mkv-c1-ej-leer-simulacion" title="Pista 2 · ¿Tu conclusión depende del texto?"}
¿Qué dato del *Quijote*, que no haya pasado por $\widehat P$, usa tu respuesta a 4?
:::

::: answer {#mkv-c1-resp-leer-simulacion of="mkv-c1-ej-leer-simulacion" title="Respuesta · Dentro del error, con menos precisión"}
**1. Errores estándar.** Con $n=400$ réplicas independientes, dan 0.023, 0.024 y 0.025. En el paso 2, $\sqrt{0.334\cdot(1-0.334)/400}\approx0.024$.

**2. Comparación.** Las tres diferencias caben incluso en un error estándar:

- **Paso 1.** La diferencia cumple $|0.693-0.710|<0.023$.
- **Paso 2.** La diferencia cumple $|0.352-0.334|<0.024$.
- **Paso 3.** La diferencia cumple $|0.512-0.533|<0.025$.

**3. Tamaño.** Para el mismo $p$, el error estándar cambia como $1/\sqrt n$. Con 25 veces menos réplicas, es $\sqrt{25}=5$ veces mayor: de a lo más 0.005 a cerca de 0.025.

**4. Límite.** Las réplicas salen de $\widehat P$. La concordancia comprueba la cuenta y el muestreo; no aporta evidencia independiente sobre el texto.
:::

**Punto de control:** deberías poder predecir con un árbol y un vector fila, y justificar $\mu_{t+1}=\mu_tP$ con sus supuestos. También, correr PREDECIR, dar su costo y comparar una simulación con su error estándar.

---

## Lo que hay que llevarse

- **A mano.** Con la matriz de la frase y desde C, el árbol da $4/33+2/9=34/99$ para V en el paso 2. El vector fila por la matriz suma los mismos caminos.
- **La respuesta.** Desde C, la cadena de la frase da $\mu_3=(1634/3267,\ 1633/3267)$. La cadena del corpus da $\Pr(S_3=V)=0.533$.
- **La regla.** En una cadena finita y homogénea, $\mu_{t+1}=\mu_tP$ y $\mu_t=\mu_0P^t$. La propiedad de Markov y la homogeneidad son condiciones suficientes.
- **El algoritmo.** PREDECIR usa $t\cdot k^2$ multiplicaciones; guarda la matriz y dos vectores de $k$ entradas. El árbol tendría hasta $k^t$ hojas.
- **El tamaño del vector.** Con dos estados basta conocer una probabilidad; con $k$, hacen falta $k-1$.
- **La simulación.** Con 10 000 réplicas independientes por inicio, el error estándar no supera 0.005; la mayor diferencia observada fue 0.010. Son unos 2 errores estándar: la comparación comprueba el procedimiento, no valida el modelo.

Continúa con [[mkv-generar-texto|Generar texto]].
