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

**Si ${S_0=C}$, ¿cuál es la probabilidad de que ${S_3=V}$, exactamente tres transiciones después?**

Al terminar tendrás:

- **Una predicción a mano.** Calcularás la distribución con un árbol y un vector fila.
- **La regla y sus condiciones.** Aplicarás @mkv-c1-teo-predecir y explicarás por qué una tabla de un paso puede fallar.
- **El algoritmo PREDECIR.** Seguirás pseudocódigo, Python y traza; justificarás el costo ${t\cdot k^2}$.
- **Una comprobación por simulación.** Compararás la cuenta con 10 000 réplicas y su error estándar.
- **El alcance.** Distinguirás una predicción de la cadena ajustada de una afirmación sobre el idioma.

## Lo que traes

- **Probabilidad total.** [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]] presenta @mkv-c1-teo-total y el promedio de repeticiones independientes, @mkv-c1-teo-promedio.
- **La cadena.** [[mkv-cadena-en-general|La cadena de Markov, en general]] define ${(\mathcal S,\mu_0,P)}$ en @mkv-c1-cadena. Una trayectoria tiene probabilidad ${\mu_0(s_0)\prod_{j=0}^{t-1}P(s_{j+1}\mid s_j)}$, bajo Markov y homogeneidad.
- **El muestreo.** MUESTREAR-FILA elige el siguiente estado con un uniforme $u$. Una réplica es una trayectoria simulada, independiente de las demás.
- **Las matrices ajustadas.** [[mkv-ajustar-contando|Ajustar contando]] obtuvo filas ${(2/11,\ 9/11)}$ y ${(2/3,\ 1/3)}$ para la frase. Para el *Quijote*, redondeadas: ${(0.181,\ 0.819)}$ y ${(0.710,\ 0.290)}$.

> **Modelo y datos.** Trabajamos con cadenas finitas y homogéneas. Usamos la matriz estimada $\widehat P$ para predecir lo que haría esa cadena.

---

## 1 · Predecir a mano con árbol y vector

**Piensa: ¿qué cuenta hay que hacer para responder la pregunta guía?**

Una multiplicación por paso. @mkv-c1-teo-predecir lo dice para cualquier cadena finita y homogénea:

$$
\begin{aligned}
\underbrace{\mu_{t+1}}_{1\times k}
&=\underbrace{\mu_t}_{1\times k}\underbrace{P}_{k\times k},\\
\underbrace{\mu_t}_{1\times k}
&=\underbrace{\mu_0}_{1\times k}\underbrace{P^t}_{k\times k}.
\end{aligned}
$$

- **Lectura.** $\mu_t$ (@mkv-c1-distribucion) es una fila; cada paso la multiplica por la misma $P$ y sigue siendo ${1\times k}$.
- **Aquí.** Con la frase, ${k=2}$, $P=\widehat P$ y ${\mu_0=\mathbf e_2}$. Primero lo vemos con un árbol, después con el vector.

### El árbol de la frase

- **Dos pasos desde C.** Puedes terminar en V pasando por V o por C. Cada camino multiplica sus flechas; @mkv-c1-arbol-2-pasos muestra todos.

::: figure {#mkv-c1-arbol-2-pasos title="Dos pasos desde C: cuatro caminos, dos terminan en V"}
![Árbol de dos pasos desde C con la matriz de la frase. Primer paso: a V con 2/3 y a C con 1/3. Desde V: a V con 2/11 y a C con 9/11; desde C: a V con 2/3 y a C con 1/3. Hojas: C, V, V vale 4/33; C, V, C vale 6/11; C, C, V vale 2/9; C, C, C vale 1/9. Las dos hojas V, con borde grueso, suman Pr(S₂ = V) = 4/33 + 2/9 = 34/99](../_assets/mkv-c1-arbol-2-pasos.svg)
:::

$$
\begin{aligned}
\Pr(C,V,V)&=\tfrac{2}{3}\cdot\tfrac{2}{11}=\tfrac{4}{33},\\
\Pr(C,V,C)&=\tfrac{2}{3}\cdot\tfrac{9}{11}=\tfrac{6}{11},\\
\Pr(C,C,V)&=\tfrac{1}{3}\cdot\tfrac{2}{3}=\tfrac{2}{9},\\
\Pr(C,C,C)&=\tfrac{1}{3}\cdot\tfrac{1}{3}=\tfrac{1}{9}.
\end{aligned}
$$

- **Suma de hojas.** Los caminos son disjuntos. Para V, sumamos los que terminan ahí:

$$
\Pr(S_2=V\mid S_0=C)
=\frac{4}{33}+\frac{2}{9}=\frac{34}{99}.
$$

::: exercise {#mkv-c1-ej-hojas-c title="Suma las otras hojas"}
Con el mismo árbol, calcula ${\Pr(S_2=C\mid S_0=C)}$. ¿Cuánto suman las cuatro hojas?
:::

::: hint {#mkv-c1-pista-hojas-c of="mkv-c1-ej-hojas-c" title="Mira el último estado"}
¿Qué caminos terminan en C?
:::

::: answer {#mkv-c1-resp-hojas-c of="mkv-c1-ej-hojas-c"}
Terminan en C los caminos C, V, C y C, C, C. Sus probabilidades suman ${\tfrac{6}{11}+\tfrac{1}{9}=\tfrac{65}{99}}$.

Las cuatro hojas suman ${\tfrac{34}{99}+\tfrac{65}{99}=1}$: en el paso 2 la cadena está en algún estado.
:::

### El mismo cálculo con un vector

- **Agrupar caminos.** Por Markov, los caminos que llegan al mismo estado comparten las probabilidades siguientes. El vector guarda su probabilidad total.
- **Inicio y orden.** En el orden V, C, empezar en C es ${\mu_0=(0,\ 1)=\mathbf e_2}$. Fila = desde dónde; columna = hacia dónde.

$$
\begin{aligned}
\mu_1
&=(0,\ 1)\begin{pmatrix}2/11&9/11\\2/3&1/3\end{pmatrix}\\
&=\left(\tfrac{2}{3},\ \tfrac{1}{3}\right).
\end{aligned}
$$

- **Cada entrada.** Multiplica el vector por una columna; desde un estado seguro, el producto copia su fila:

$$
\begin{aligned}
\mu_1(V)&=0\cdot\tfrac{2}{11}+1\cdot\tfrac{2}{3}=\tfrac{2}{3},\\
\mu_1(C)&=0\cdot\tfrac{9}{11}+1\cdot\tfrac{1}{3}=\tfrac{1}{3}.
\end{aligned}
$$

- **Paso 2.** Los productos vuelven a sumar las hojas del árbol:

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

- **Paso 3.** Multiplicamos ${\mu_2=(34/99,\ 65/99)}$ por cada columna:

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

- **Respuesta.** Desde C, la cadena de la frase está en V en el paso 3 con probabilidad $1634/3267$.
- **Evento preciso.** Estar en V en ese paso difiere de visitarlo alguna vez antes (@mkv-c1-distribucion).
- **Tamaño del árbol.** Tres pasos dan $2^3$ hojas; con $k$ estados y $t$ pasos, hasta $k^t$. El vector guarda solo $k$ números.
- **Lo que no generaliza.** Con dos estados basta ${\mu_t(V)}$, porque ${\mu_t(C)=1-\mu_t(V)}$. Con $k$ estados hacen falta ${k-1}$ números.

---

## 2 · Derivar el contraejemplo

**Piensa: ¿basta una tabla de un paso para predecir con potencias?**

No. La prueba de @mkv-c1-teo-predecir usa, en cada paso $t$, la propiedad de Markov y la homogeneidad:

$$
\begin{aligned}
&\Pr(S_{t+1}=s'\mid S_t=s,\ \text{historia})\\
&\quad=P(s'\mid s).
\end{aligned}
$$

- **Si vale.** Cada paso usa la fila de $s$ y nada más; en la frase, ${\mu_3=\mu_0\widehat P^{\,3}}$ reproduce la cuenta a mano.
- **Contraejemplo.** Un proceso repite C C V sin fin. Empieza en cualquiera de sus dos C, cada una con probabilidad $1/2$.
- **Dos posiciones distintas.** La primera C va a C; la segunda va a V. Su tabla de un paso, en orden V, C, es:

$$
P=\begin{pmatrix}0&1\\1/2&1/2\end{pmatrix},
\qquad \mu_0=(0,\ 1).
$$

- **Si repites esa tabla.** Predice:

$$
\begin{aligned}
\mu_0P&=\left(\tfrac{1}{2},\ \tfrac{1}{2}\right),\\
(\mu_0P^2)(V)
&=\tfrac{1}{2}\cdot0+\tfrac{1}{2}\cdot\tfrac{1}{2}=\tfrac{1}{4}.
\end{aligned}
$$

- **En el proceso.** Solo empezar en la primera C lleva a V dos pasos después:

$$
\Pr(S_2=V)=\tfrac{1}{2}\cdot1+\tfrac{1}{2}\cdot0=\tfrac{1}{2}.
$$

- **Qué falla.** Saber «C» no determina una fila válida para todos los pasos. Tras observar C, C, la siguiente es V.

> [!WARNING]
> **Confundir predicción con idioma.** Desde C, ${\mu_3(V)=1634/3267}$ corresponde a la cadena ajustada a la frase.
> **La frecuencia de vocales tres letras después de una consonante se mide en el texto.** El texto no tiene por qué ser una cadena.

::: exercise {#mkv-c1-ej-dos-matrices title="Cambia la matriz a medio camino"}
Imagina que el paso 1 usa $\widehat P$ y el paso 2 usa otra matriz, $P'$. ¿Cómo escribes $\mu_2$? ¿Sigue valiendo ${\mu_2=\mu_0\widehat P^{\,2}}$?
:::

::: hint {#mkv-c1-pista-dos-matrices of="mkv-c1-ej-dos-matrices" title="Un paso a la vez"}
¿Qué matriz usa la regla para pasar de $\mu_1$ a $\mu_2$?
:::

::: answer {#mkv-c1-resp-dos-matrices of="mkv-c1-ej-dos-matrices"}
$$
\mu_2=\mu_1P'=\mu_0\widehat P P'.
$$

Cada paso conserva su matriz. Sin homogeneidad, la potencia ${\mu_0\widehat P^{\,2}}$ ya no está garantizada.
:::

---

## 3 · Predecir con un algoritmo

**Piensa: ¿qué tiene que recordar un programa entre un paso y el siguiente?**

El vector actual y la matriz. Cada vuelta calcula, entrada por entrada, el vector siguiente completo:

$$
\mu_j(s')
=\sum_{s\in\mathcal S}\mu_{j-1}(s)\,P(s'\mid s),
\qquad s'\in\mathcal S.
$$

- **Por qué completo.** Si sustituyera entradas a medias, mezclaría $\mu_{j-1}$ con $\mu_j$.

> **Dado:** una cadena finita y homogénea, matriz $P$ de ${k\times k}$, distribución fila $\mu_0$ de ${1\times k}$ y entero ${t\ge0}$.
>
> **Encontrar:** $\mu_t$, la distribución del estado en el paso $t$ (@mkv-c1-distribucion).

### El mapa de PREDECIR

- **Qué calcula:** ${\mu_t=\mu_0P^t}$.
- **Qué guarda:** la matriz, el vector actual y espacio para el siguiente.
- **Cómo avanza:** reemplaza $\mu$ por ${\mu P}$, multiplicando por cada columna.
- **Qué devuelve al terminar:** $\mu_t$, tras exactamente $t$ multiplicaciones de vector por matriz.

::: figure {#mkv-c1-flujo-predecir title="Predecir, en palabras"}
![Diagrama de flujo de predecir, en palabras: empieza con μ₀, un vector fila; pregunta si faltan pasos; si sí, multiplica por P̂, μ ← μ P̂, y vuelve a preguntar con otro paso; si no, devuelve μₜ. Con t = 0 devuelve μ₀ sin multiplicar. Al pie: cada paso cuesta k² productos con k estados](../_assets/mkv-c1-flujo-predecir.svg)
:::

```text
INPUT   los k estados de 𝒮, en un
        orden fijo (V, C aquí);
        P, de k×k, con filas y
        columnas en ese orden;
        μ_0, vector fila de k
        entradas que suma 1;
        t ≥ 0 entero.
OUTPUT  μ_t, la distribución del
        estado en el paso t.

 1 function PREDECIR(P, μ_0, t)
 2   μ ← μ_0
 3   for j ← 1 to t
 4     nuevo ← k ceros
 5     for each s′ in 𝒮
 6       for each s in 𝒮
 7         nuevo(s′) ← nuevo(s′)
                 + μ(s)·P(s′ | s)
 8     μ ← nuevo
 9   return μ
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. Las posiciones ${0,\dots,k-1}$ respetan el orden de las filas de `P`.

```python
from fractions import Fraction

def predecir(P, mu0, t):                  # (1)
    k = len(mu0)          # estados 0, …, k − 1, como en P
    mu = list(mu0)                        # (2) paso 0
    for j in range(1, t + 1):             # (3)
        nuevo = [0] * k                   # (4)
        for s2 in range(k):               # (5) columna s′
            for s in range(k):            # (6) fila s
                nuevo[s2] += mu[s] * P[s][s2]  # (7)
        mu = nuevo                        # (8) ahora μ_j
    return mu                             # (9) μ_t

P_gorro = [[Fraction(2, 11), Fraction(9, 11)],   # fila V
           [Fraction(2, 3), Fraction(1, 3)]]     # fila C
print(predecir(P_gorro, [0, 1], 3))
# [Fraction(1634, 3267), Fraction(1633, 3267)]
```

**Cada pieza, en su línea:**

- **Línea 2.** Copia $\mu_0$; con ${t=0}$, devuelve esa distribución.
- **Líneas 4 a 7.** Multiplican por cada columna: `P[s][s2]` indica fila $s$, columna $s'$.
- **Línea 8.** Sustituye el vector completo; evita mezclar $\mu_{j-1}$ con $\mu_j$.

**Cómo leer la traza.** Usamos la matriz de la frase y empezamos en C. El renglón 0 inicializa; cada siguiente muestra $\mu$ tras la vuelta $j$.

**Tramo único · De C al paso 3**

| j | μ(V) | μ(C) |
|---:|---|---|
| 0 | 0 | 1 |
| 1 | 2/3 | 1/3 |
| 2 | 34/99 | 65/99 |
| 3 | 1634/3267 | 1633/3267 |

- **Paso 1.** Copia la fila C.
- **Paso 2.** Suma las hojas de @mkv-c1-arbol-2-pasos.
- **Paso 3.** Devuelve ${(1634/3267,\ 1633/3267)}$; las entradas siguen sumando 1.

::: exercise {#mkv-c1-ej-traspuesta title="Encuentra el índice cambiado"}
Alguien escribió la línea 7 con ${P(s\mid s')}$ en lugar de ${P(s'\mid s)}$. Corre una vuelta con la matriz de la frase desde ${\mu_0=(0,\ 1)}$.

1. **Calcula.** ¿Qué vector obtiene?
2. **Diagnostica.** ¿Cómo sabes, sin el resultado correcto, que está mal?
:::

::: hint {#mkv-c1-pista-traspuesta of="mkv-c1-ej-traspuesta" title="Qué entradas sobreviven"}
Con ${\mu=(0,\ 1)}$, ¿qué entradas de $\widehat P$ se multiplican por 1?
:::

::: answer {#mkv-c1-resp-traspuesta of="mkv-c1-ej-traspuesta"}
1. **Obtiene ${(9/11,\ 1/3)}$.** Copia la columna C de $\widehat P$.
2. **No suma 1.** $9/11$ y $1/3$ juntos pasan de 1. Las columnas de $P$ no tienen por qué sumar 1.
:::

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina tras $t$ vueltas para cualquier entero no negativo. Cada $\mu_j$ sigue siendo una distribución.
- **Número que da:** desde C, con la frase y ${t=3}$, devuelve ${(1634/3267,\ 1633/3267)}$.
- **Garantía:** @mkv-c1-teo-predecir asegura ${\mu_0P^t}$. Con fracciones es exacto; con decimales interviene el redondeo.
- **Costo:** $k^2$ multiplicaciones por vuelta, ${t\cdot k^2}$ en total. Guarda $k^2$ entradas de la matriz y dos vectores de $k$ entradas.
- **Supuestos:** $\mu_0$ es una distribución; $P$ es fija, tiene entradas en ${[0,1]}$ y cada fila suma 1.

---

## 4 · Simular réplicas para comprobar la cuenta

**Piensa: ¿cómo estimas una probabilidad sin repetir la multiplicación?**

Simulando $n$ réplicas independientes y contando cuántas están en $s$ en el paso $t$. Por @mkv-c1-teo-promedio, con probabilidad 1:

$$
\frac{\#\{\text{réplicas en }s\text{ en el paso }t\}}{n}
\xrightarrow[n\to\infty]{}\mu_t(s).
$$

- **Ruido.** Con ${p=\mu_t(s)}$, cada réplica aporta 0 o 1, con dispersión ${\sqrt{p(1-p)}}$. Promediar $n$ réplicas independientes la divide entre ${\sqrt n}$.

::: definition {#mkv-c1-error-estandar title="El error estándar de una fracción simulada"}
- **Qué es.** El error estándar (*standard error*) mide la dispersión de la fracción simulada alrededor de la probabilidad $p$.
- **Cómo se calcula.** Para $n$ réplicas independientes con la misma probabilidad ${p=\mu_t(s)}$:

$$
\text{error estándar}=\sqrt{\frac{p(1-p)}{n}}.
$$

- **Qué significa.** Con el mismo $p$, cuadruplicar $n$ reduce el error estándar a la mitad. La dispersión es nula con ${p=0}$ o ${p=1}$, y máxima con ${p=1/2}$.

$$
p(1-p)\le\tfrac{1}{4}
\quad\Longrightarrow\quad
\sqrt{\frac{p(1-p)}{10\,000}}\le0.005.
$$

- **Ejemplo.** En el paso 3 desde C, el corpus da ${p=0.533}$ redondeado; su error estándar con ${n=10\,000}$ vale ${\approx0.005}$.
- **Qué no es.** No acota la diferencia observada: esta puede superar uno o dos errores estándar. Tampoco mide si el modelo describe el texto.
:::

### El experimento con el corpus

- **Matriz.** Usamos $\widehat P$ del *Quijote*. Sus filas redondeadas son ${(0.181,\ 0.819)}$ y ${(0.710,\ 0.290)}$; cuenta y simulación usan las fracciones exactas.
- **Réplicas.** Son ${n=10\,000}$ trayectorias independientes de 8 pasos desde C, con semilla 2030. Otras 10 000 empiezan en V, con semilla 2029.
- **Sorteos.** Cada réplica gasta un $u$ para sortear $S_0$, incluso con inicio seguro. Cada paso usa MUESTREAR-FILA con un $u$ nuevo.
- **Un punto.** Muestra la fracción de réplicas en V en el paso $t$.
- **Una línea.** Muestra ${\mu_0\widehat P^{\,t}}$ de PREDECIR, con la misma matriz e inicio.
- **Ejes.** El horizontal indica el paso; arriba se comparan probabilidades y fracciones, abajo aparece «réplicas menos cuenta».

::: figure {#mkv-c1-mu-t title="La cuenta y las réplicas coinciden dentro del error, paso a paso"}
![Probabilidad de estar en V en el paso t, de t = 0 a 8, con la matriz del corpus. Arriba, la cuenta μ₀P̂ᵗ como línea y la fracción de 10 000 réplicas en V como marcas. Desde V: cuenta 1.000, 0.181, 0.615, 0.385, 0.507, 0.442, 0.476, 0.458, 0.468; réplicas 1.000, 0.180, 0.611, 0.392, 0.498, 0.438, 0.476, 0.460, 0.464. Desde C: cuenta 0.000, 0.710, 0.334, 0.533, 0.428, 0.484, 0.454, 0.470, 0.462; réplicas 0.000, 0.712, 0.326, 0.543, 0.424, 0.485, 0.452, 0.467, 0.470. Abajo, réplicas menos cuenta, con una franja de ±0.010, dos errores estándar en el peor caso (p = 0.5); la mayor diferencia es 0.010, unos 2.0 errores estándar, en el paso 3 desde C, justo en el borde de la franja](../_assets/mkv-c1-mu-t.svg)
:::

- **Cuenta desde C.** En los pasos 1, 2 y 3 da 0.710, 0.334 y 0.533.
- **Réplicas desde C.** Dan 0.712, 0.326 y 0.543 en esos pasos.
- **Franja.** ±0.010 corresponde a dos errores estándar en el peor caso, ${p=0.5}$. En los demás puntos, el error estándar es menor.
- **Mayor diferencia.** Es 0.010, unos 2.0 errores estándar, en el paso 3 desde C. Queda en el borde; ningún punto sale de la franja.
- **Lectura.** Las diferencias observadas tienen el tamaño que anticipa el error estándar. La franja no garantiza contener todas las diferencias de otra corrida.
- **Acercamiento observado.** En el paso 8, la cuenta desde V da 0.468; desde C, 0.462. Esto no demuestra convergencia para cualquier matriz.

> [!WARNING]
> **Confundir comprobar la cuenta con validar el modelo.** Las réplicas usan la misma $\widehat P$ que PREDECIR.
> **La concordancia comprueba el procedimiento; no demuestra que el *Quijote* sea una cadena de memoria 1.**

::: exercise {#mkv-c1-ej-paso-cero title="Explica el punto exacto"}
Desde C, el punto del paso 0 vale 0.000 en la cuenta y en las réplicas. ¿Por qué no tiene ruido? ¿Cuánto vale ahí su error estándar?
:::

::: hint {#mkv-c1-pista-paso-cero of="mkv-c1-ej-paso-cero" title="Dónde empieza cada réplica"}
¿Qué $p$ corresponde a V en el paso 0 si ${\mu_0=(0,\ 1)}$?
:::

::: answer {#mkv-c1-resp-paso-cero of="mkv-c1-ej-paso-cero"}
Todas las réplicas empiezan en C, así que ninguna está en V. Con ${p=0}$, el error estándar es ${\sqrt{0\cdot1/n}=0}$.
:::

---

## Ejercicios

::: exercise {#mkv-c1-ej-tres-estados title="Predice dos pasos con tres estados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Una cadena homogénea tiene estados 1, 2, 3, en ese orden. **Cambia una idea:** el inicio ya no es seguro; se reparte entre dos estados.

$$
P=\begin{pmatrix}
1/2 & 1/4 & 1/4\\
1/3 & 0 & 2/3\\
0 & 1/2 & 1/2
\end{pmatrix},
$$

$$
\mu_0=\left(\tfrac{1}{2},\ \tfrac{1}{2},\ 0\right).
$$

1. **Lee la matriz.** ¿Qué dicen sus dos ceros?
2. **Calcula $\mu_1$.** Haz el vector fila por cada columna.
3. **Calcula $\mu_2$.** Comprueba que suma 1.
4. **Generaliza.** Escribe $\mu_t$ para cualquier $t$ y cuántas multiplicaciones cuesta.

:::

::: hint {#mkv-c1-pista-tres-estados-1 of="mkv-c1-ej-tres-estados" title="Pista 1 · ¿Qué filas cuentan?"}
¿Qué entrada de $\mu_0$ es 0? ¿Qué fila de $P$ deja de aportar por eso en el primer paso?
:::

::: hint {#mkv-c1-pista-tres-estados-2 of="mkv-c1-ej-tres-estados" title="Pista 2 · ¿Usaste el vector correcto?"}
¿Suman 1 tus dos vectores? Para el segundo paso, ¿multiplicaste $\mu_1$ y no $\mu_0$?
:::

::: answer {#mkv-c1-resp-tres-estados of="mkv-c1-ej-tres-estados" title="Respuesta · Dos pasos con tres estados"}
**1. Ceros.** ${P(2\mid 2)=0}$ impide quedarse en 2; ${P(1\mid 3)=0}$ impide pasar de 3 a 1. Ambas transiciones son imposibles en el modelo.

**2. Primer paso.** La fila 3 no aporta porque ${\mu_0(3)=0}$:

$$
\begin{aligned}
\mu_1(1)&=\tfrac{1}{2}\cdot\tfrac{1}{2}+\tfrac{1}{2}\cdot\tfrac{1}{3}=\tfrac{5}{12},\\
\mu_1(2)&=\tfrac{1}{2}\cdot\tfrac{1}{4}+\tfrac{1}{2}\cdot0=\tfrac{1}{8},\\
\mu_1(3)&=\tfrac{1}{2}\cdot\tfrac{1}{4}+\tfrac{1}{2}\cdot\tfrac{2}{3}=\tfrac{11}{24}.
\end{aligned}
$$

**3. Segundo paso.** Ahora las tres filas aportan, multiplicadas por sus entradas en $\mu_1$:

$$
\begin{aligned}
\mu_2(1)
&=\tfrac{5}{12}\cdot\tfrac{1}{2}+\tfrac{1}{8}\cdot\tfrac{1}{3}+\tfrac{11}{24}\cdot0\\
&=\tfrac{1}{4},\\
\mu_2(2)
&=\tfrac{5}{12}\cdot\tfrac{1}{4}+\tfrac{1}{8}\cdot0+\tfrac{11}{24}\cdot\tfrac{1}{2}\\
&=\tfrac{1}{3},\\
\mu_2(3)
&=\tfrac{5}{12}\cdot\tfrac{1}{4}+\tfrac{1}{8}\cdot\tfrac{2}{3}+\tfrac{11}{24}\cdot\tfrac{1}{2}\\
&=\tfrac{5}{12}.
\end{aligned}
$$

Así, ${\mu_2=(1/4,\ 1/3,\ 5/12)}$, que suma 1.

**4. General.** Como la cadena es finita y homogénea, ${\mu_t=\mu_0P^t}$. PREDECIR requiere ${k^2=3^2}$ multiplicaciones por paso: ${t\cdot3^2}$ en total.
:::

::: exercise {#mkv-c1-ej-leer-simulacion title="Lee una simulación con pocas réplicas"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Repetiste la simulación desde C con la matriz del corpus. **Cambia una idea:** usaste ${n=400}$ réplicas independientes en lugar de 10 000, con semilla 2031.

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
**1. Errores estándar.** Con ${n=400}$ réplicas independientes, dan 0.023, 0.024 y 0.025. En el paso 2:

$$
\sqrt{\frac{0.334\cdot(1-0.334)}{400}}\approx0.024.
$$

**2. Comparación.** Las tres diferencias caben incluso en un error estándar:

- **Paso 1.** La diferencia cumple ${|0.693-0.710|<0.023}$.
- **Paso 2.** La diferencia cumple ${|0.352-0.334|<0.024}$.
- **Paso 3.** La diferencia cumple ${|0.512-0.533|<0.025}$.

**3. Tamaño.** Para el mismo $p$, el error estándar cambia como ${1/\sqrt n}$. Con 25 veces menos réplicas, es ${\sqrt{25}=5}$ veces mayor: de a lo más 0.005 a cerca de 0.025.

**4. Límite.** Las réplicas salen de $\widehat P$. La concordancia comprueba la cuenta y el muestreo; no aporta evidencia independiente sobre el texto.
:::

**Punto de control:** deberías poder predecir con árbol y vector, aplicar ${\mu_{t+1}=\mu_tP}$ con sus condiciones y dar sus dimensiones. También, correr PREDECIR, justificar su costo y comparar réplicas con su error estándar.

---

## Lo que hay que llevarse

- **A mano.** Árbol y vector suman los mismos caminos: ${4/33+2/9=34/99}$ para V en el paso 2 desde C.
- **La respuesta.** La cadena de la frase da ${\mu_3=(1634/3267,\ 1633/3267)}$. La del corpus da ${\Pr(S_3=V)=0.533}$.
- **La regla.** En una cadena finita y homogénea, ${\mu_{t+1}=\mu_tP}$ y ${\mu_t=\mu_0P^t}$, con formas ${(1\times k)(k\times k)=(1\times k)}$ (@mkv-c1-teo-predecir).
- **El algoritmo.** PREDECIR usa ${t\cdot k^2}$ multiplicaciones y guarda la matriz y dos vectores. El árbol tendría hasta $k^t$ hojas.
- **El atajo.** Dos estados requieren una probabilidad; $k$ estados, ${k-1}$.
- **La simulación.** Con 10 000 réplicas, el error estándar no supera 0.005. La mayor diferencia fue 0.010: unos 2 errores estándar, en el borde de ±0.010.
- **El alcance.** La comparación comprueba el procedimiento; no valida el modelo del idioma.

Continúa con [[mkv-generar-texto|Generar texto]].

