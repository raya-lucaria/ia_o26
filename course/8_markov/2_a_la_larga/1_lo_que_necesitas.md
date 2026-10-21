---
id: mkv-algebra-y-limites
title: "Lo que necesitas de álgebra y límites"
nav_title: "Lo que necesitas"
summary: "Sistemas lineales y cuántas soluciones tienen, límite de una sucesión y criterio de paro, valor esperado y la regla de condicionar en el primer paso, y alcanzar un estado en un grafo: las herramientas para preguntar qué hace una cadena a la larga."
status: ready
estimated_time: 25m
tags: [markov, algebra-lineal, limites, probabilidad]
---

# Lo que necesitas de álgebra y límites

**¿Qué herramientas faltan para decir si una cadena olvida dónde empezó?**

Al terminar tendrás:

- **Un sistema lineal bien planteado:** con incógnita fila o columna, y cuántas soluciones puede tener.
- **Una sucesión con o sin límite:** de números y de distribuciones, con su tolerancia de paro.
- **Un valor esperado:** su definición y la regla de condicionar en el primer paso.
- **Una prueba de alcance:** cuándo un estado lleva a otro, leída en las potencias de $P$.

## Lo que traes

De la clase 1, [[markov-que-es-una-cadena|Qué es una cadena de Markov]]:

- **La distribución de cada paso:** $\mu_t$ es una fila $1\times k$ que suma 1 (@mkv-c1-distribucion).
- **Avanzar:** $\mu_{t+1}=\mu_tP$ y $\mu_t=\mu_0P^t$ (@mkv-c1-teo-predecir).
- **Las potencias:** $(P^t)_{ij}$ reúne los caminos de $t$ pasos de $s_i$ a $s_j$ (@mkv-c1-teo-potencias).
- **Probabilidad total:** suma por casos de una partición (@mkv-c1-teo-total).
- **Las rachas:** $\Pr(L=\ell)=(1-q)q^{\ell-1}$, con $q<1$, en [[mkv-el-problema-de-markov|El problema de Markov]].

De [[bajar-la-pendiente|Bajar la pendiente]], en optimización:

- **Tolerancia:** un método iterativo para cuando el cambio es menor que una tolerancia (@opt-tolerancia).

**La pregunta abierta.** En [[tarea-que-es-una-cadena|la tarea de la clase 1]] dejaste correr dos cadenas. Con la matriz de la frase, $\mu_t(V)$ desde V y desde C se acercaban a $22/49\approx0.449$. Con la que alterna A↔B, desde A, saltaba 1, 0, 1, 0… sin asentarse.

Para explicar esa diferencia faltan cuatro herramientas:

- **Un sistema lineal,** para encontrar la fila que no cambia al multiplicar por $P$.
- **Un límite,** para decir con precisión qué es «acercarse».
- **Un valor esperado,** para preguntar cuánto tarda algo en promedio.
- **Alcanzar,** para saber qué estados pueden llevar a cuáles.

**Página de concepto:** sin simulación; un solo bloque de Python.

---

## 1 · Plantear un sistema lineal

**Piensa: ¿qué fila $x$ cumple $xP=x$?**

Es una incógnita que aparece en $k$ ecuaciones lineales a la vez: un sistema lineal.

::: definition {#mkv-c2-def-sistema title="Sistema lineal, con incógnita columna o fila"}
$$
\begin{aligned}
&A\in\mathbb R^{k\times k},\qquad
x^{\mathsf T},b^{\mathsf T}\in\mathbb R^{k\times1},\\
&Ax^{\mathsf T}=b^{\mathsf T}
\quad(\text{incógnita columna}),\\
&xA=b
\iff A^{\mathsf T}x^{\mathsf T}=b^{\mathsf T}
\quad(\text{incógnita fila}).
\end{aligned}
$$

- **Qué es:** $k$ ecuaciones lineales con $k$ incógnitas, $x=(x_1,\dots,x_k)$; una **solución** es una $x$ que las cumple todas.
- **Cómo se calcula:** se despeja una incógnita y se sustituye en las demás (eliminación), o se usa una biblioteca.
- **Qué significa:** en la forma fila, cada columna de $A$ da una ecuación.
- **Qué no es:** $xA$ no es $Ax^{\mathsf T}$; para pasar de fila a columna se traspone **y** se invierte el orden.
:::

- **Trasponer:** $(xA)^{\mathsf T}=A^{\mathsf T}x^{\mathsf T}$, como en [[mkv-cadena-en-general|La cadena, en general]].

::: theorem {#mkv-c2-al-teo-soluciones title="Ninguna, una o infinitas"}
Sea $A\in\mathbb R^{k\times k}$ y $b$ cualquier lado derecho.

- **Una sola:** si la única solución de $Ax^{\mathsf T}=0$ es $x=0$, entonces $Ax^{\mathsf T}=b^{\mathsf T}$ tiene exactamente una solución.
- **Si no:** $Ax^{\mathsf T}=b^{\mathsf T}$ no tiene ninguna o tiene infinitas. Nunca exactamente dos.

**Condición.** Matriz cuadrada; para la forma fila, aplica lo mismo a $A^{\mathsf T}$.

**Lectura.** Con $k=2$, la solución es única si y solo si $a_{11}a_{22}-a_{12}a_{21}\ne0$ (el **determinante**).

**Casos nulos.** Si $b=0$, $x=0$ siempre es solución: «ninguna» no puede ocurrir.
:::

::: proof {#mkv-c2-al-dem-soluciones of="mkv-c2-al-teo-soluciones"}
Solo la parte «nunca dos». Si $y\ne z$ son soluciones, para todo número real $\lambda$:

$$
\begin{aligned}
A\bigl(y+\lambda(z-y)\bigr)^{\mathsf T}
&=b^{\mathsf T}+\lambda\,(b-b)^{\mathsf T}\\
&=b^{\mathsf T}.
\end{aligned}
$$

Cada $\lambda$ da una solución distinta: son infinitas. La parte «una sola» es un resultado estándar de álgebra lineal que citamos.
:::

**En general: la fila que no cambia.** Para una matriz de transición $P$ de $k\times k$:

$$
\begin{aligned}
xP=x
&\iff x(P-I_k)=0\\
&\iff (P^{\mathsf T}-I_k)\,x^{\mathsf T}=0.
\end{aligned}
$$

- **Siempre tiene la solución $x=0$:** el lado derecho es cero. Si hay otra, hay infinitas.
- **Una ecuación sobra.** Al sumar las $k$ ecuaciones, cada $x_i$ queda multiplicada por su fila de $P$ menos 1, que da cero.

$$
\begin{aligned}
&\sum_{j=1}^k\sum_{i=1}^k x_i(P_{ij}-\delta_{ij})\\
&\quad=\sum_{i=1}^k x_i\Bigl(\sum_{j=1}^kP_{ij}-1\Bigr)=0.
\end{aligned}
$$

- **Lectura:** $\delta_{ij}$ vale 1 si $i=j$ y 0 si no; son las entradas de $I_k$.
- **El arreglo:** se **cambia una ecuación** por $x_1+\dots+x_k=1$. La redundante no aporta y la nueva descarta $x=0$.

**En el juguete.** Toda cadena de dos estados se escribe con dos números, $a,b\in[0,1]$:

$$
\begin{aligned}
P&=\begin{pmatrix}1-a&a\\ b&1-b\end{pmatrix},\\
xP=x&\iff
\begin{cases}
-a\,x_1+b\,x_2=0,\\
\phantom{-}a\,x_1-b\,x_2=0.
\end{cases}
\end{aligned}
$$

La segunda ecuación es la primera por $-1$. Se cambia por la suma:

$$
\begin{aligned}
&\begin{cases}
-a\,x_1+b\,x_2=0,\\
\phantom{-a\,}x_1+\phantom{b\,}x_2=1,
\end{cases}\\
&\text{determinante}=-a-b,\\
&x=\Bigl(\frac{b}{a+b},\ \frac{a}{a+b}\Bigr)
\quad\text{si }a+b>0.
\end{aligned}
$$

- **La frase:** $a=9/11$ (de V a C) y $b=2/3$ (de C a V) dan $x=(22/49,\ 27/49)$, el número de la tarea.
- **La identidad:** $a=b=0$ anula el determinante. Toda $x$ que sume 1 cumple $xI_2=x$: infinitas soluciones.

**Con la biblioteca.** `numpy.linalg.solve` resuelve la forma columna; la función traspone y cambia la última ecuación:

```python
import numpy as np

def fila_fija(P):
    """Resuelve x P = x con x 1 = 1."""
    k = P.shape[0]
    A = P.T - np.eye(k)   # (P^T - I) x^T = 0
    b = np.zeros(k)
    A[-1, :] = 1.0        # cambia la última ecuación
    b[-1] = 1.0           # por x_1 + ... + x_k = 1
    return np.linalg.solve(A, b)

P = np.array([[2/11, 9/11],
              [2/3, 1/3]])
x = fila_fija(P)
print(np.round(x, 4))      # la fila
print(np.round(x @ P, 4))  # no cambia
print(round(22/49, 4), round(27/49, 4))

try:
    fila_fija(np.eye(2))   # identidad: infinitas
except np.linalg.LinAlgError as error:
    print("sin solución única:", error)
```

```text
[0.449 0.551]
[0.449 0.551]
0.449 0.551
sin solución única: Singular matrix
```

- **Con $k$ estados:** la misma función sirve; solo crece $A$.
- **Cuando falla:** con infinitas soluciones, `solve` avisa que la matriz es singular.

> [!WARNING]
> **Error típico: resolver $Px^{\mathsf T}=x^{\mathsf T}$.** Esa cuenta usa las filas de $P$ como ecuaciones y responde otra pregunta. **La lectura correcta: la incógnita es fila, así que se traspone, $(P^{\mathsf T}-I_k)\,x^{\mathsf T}=0$.**

::: exercise {#mkv-c2-al-ej-alternante title="Resuelve la cadena que alterna"}
Para la cadena A↔B, con $P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, ¿cuántas filas $x$ cumplen $xP=x$ y $x_1+x_2=1$? ¿Cuáles?
:::

::: hint {#mkv-c2-al-pista-alternante of="mkv-c2-al-ej-alternante" title="¿Qué valen a y b aquí?"}
¿Es positivo $a+b$ en esta matriz?
:::

::: answer {#mkv-c2-al-resp-alternante of="mkv-c2-al-ej-alternante"}
**Una sola:** $a=b=1$, así que $a+b=2>0$ y $x=(1/2,\ 1/2)$. Comprueba: $(1/2,\ 1/2)P=(1/2,\ 1/2)$.
:::

La alternante sí tiene su fila fija, y aun así desde A no se acercaba a ella. Falta definir «acercarse».

---

## 2 · Decidir si una sucesión tiene límite

**Piensa: ¿qué significa que $\mu_t$ «se acerque» a una fila?**

Que la distancia entre ambas se vuelva tan chica como quieras y **se quede** así desde algún paso.

::: definition {#mkv-c2-def-limite title="Límite de una sucesión de números o de filas"}
$$
\begin{aligned}
&\lVert x-y\rVert_1=\sum_{i=1}^k\lvert x_i-y_i\rvert,
\qquad x,y\in\mathbb R^{1\times k},\\
&\lim_{t\to\infty}x_t=x\iff\\
&\quad\text{para todo }\mathrm{tol}>0\text{ hay un }t_0\text{ con}\\
&\quad\lVert x_t-x\rVert_1<\mathrm{tol}
\text{ para todo }t\ge t_0.
\end{aligned}
$$

- **Qué es:** $x$ es el **límite** de $x_0,x_1,\dots$ si la distancia a $x$ acaba por debajo de cualquier tolerancia.
- **Cómo se calcula:** se acota $\lVert x_t-x\rVert_1$ con una expresión en $t$ que tienda a cero.
- **Qué significa:** pasado $t_0$, todos los términos están a menos de $\mathrm{tol}$ de $x$, no solo alguno.
- **Qué no es:** pasar cerca una vez. Con $k=1$, la distancia es el valor absoluto $\lvert x_t-x\rvert$.
:::

- **Notación:** $\lVert\cdot\rVert_1$ se lee «norma uno».
- **Entre distribuciones:** la distancia va de 0 a 2.
- **Entrada por entrada:** con $k$ finito, la fila converge si y solo si converge cada entrada.
- **Por qué $\mathrm{tol}$:** en optimización se escribía $\varepsilon$; aquí $\varepsilon$ ya fue el contraejemplo de la clase 1.

::: theorem {#mkv-c2-al-teo-oscila title="Una sucesión que oscila no tiene límite"}
La sucesión $1,0,1,0,\dots$ no tiene límite.

**Condición.** Los términos pares valen 1 y los impares 0, para siempre.

**Lectura.** No hay un número al que se quede cerca: siempre vuelve a saltar 1.
:::

::: proof {#mkv-c2-al-dem-oscila of="mkv-c2-al-teo-oscila"}
Supón un límite $x$ y toma $\mathrm{tol}=1/2$. Pasado $t_0$ hay un término 1 y otro 0, ambos a menos de $1/2$ de $x$:

$$
1=\lvert1-0\rvert\le\lvert1-x\rvert+\lvert x-0\rvert<\tfrac12+\tfrac12=1.
$$

Es una contradicción: no hay límite.
:::

**En el juguete.** Con $x=(22/49,\ 27/49)$, la fila de la sección 1:

- **La frase, desde V:** $\lVert\mu_t-x\rVert_1$ baja de $54/49\approx1.102$ en $t=0$ a $0.0034$ en $t=8$.
- **La frase, desde C:** baja de $44/49\approx0.898$ a $0.0027$ en $t=8$.
- **La alternante, desde A:** $\mu_t(A)$ es $1,0,1,0,\dots$ Por el teorema, $\mu_t$ no tiene límite.
- **La alternante, desde $(1/2,\ 1/2)$:** $\mu_t$ no cambia; una sucesión constante converge a su valor.

**El criterio de paro.** Una computadora no espera a $t=\infty$. Un método iterativo para cuando el cambio es pequeño:

$$
\lVert x_{t+1}-x_t\rVert_1<\mathrm{tol}.
$$

- **Lo que no garantiza:** cambio chico no es estar cerca del límite. Las sumas $1+\tfrac12+\dots+\tfrac1t$ avanzan cada vez menos y no tienen límite.
- **Tope de pasos:** hace falta, porque una sucesión que oscila nunca cumple el criterio.

> [!WARNING]
> **Error típico: «paró, entonces convergió».** El criterio solo mide el último cambio. **La lectura correcta: parar dice que el cambio fue chico; que exista el límite y qué tan cerca estás requiere un teorema aparte.**

::: exercise {#mkv-c2-al-ej-cambio-alternante title="Mide el cambio en la alternante"}
Desde A, ¿cuánto vale $\lVert\mu_{t+1}-\mu_t\rVert_1$ en la cadena A↔B? ¿Con qué $\mathrm{tol}$ pararía el criterio?
:::

::: hint {#mkv-c2-al-pista-cambio-alternante of="mkv-c2-al-ej-cambio-alternante" title="¿Cuáles son dos filas seguidas?"}
¿Qué filas son $\mu_0$ y $\mu_1$, y cambia esa diferencia con $t$?
:::

::: answer {#mkv-c2-al-resp-cambio-alternante of="mkv-c2-al-ej-cambio-alternante"}
$$
\lVert(0,1)-(1,0)\rVert_1=1+1=2\quad\text{en todo paso}.
$$

**Solo con $\mathrm{tol}>2$,** que no sirve: dos distribuciones nunca distan más de 2. Sin tope de pasos, el método no para.
:::

Falta otra clase de pregunta: cuánto tarda algo, en promedio.

---

## 3 · Promediar con el valor esperado

**Piensa: ¿cuánto mide, en promedio, una racha de consonantes?**

Se responde con el **valor esperado** del largo $L$: cada largo posible, pesado por su probabilidad.

::: definition {#mkv-c2-def-esperanza title="Valor esperado de una variable discreta"}
$$
\begin{aligned}
&X\in\{x_1,x_2,\dots\}\quad(\text{finitos o numerables}),\\
&E[X]=\sum_j x_j\Pr(X=x_j),\\
&E[X\mid B]=\sum_j x_j\Pr(X=x_j\mid B),
\quad\Pr(B)>0,\\
&E_s[X]=E[X\mid S_0=s],
\qquad\Pr_s(\cdot)=\Pr(\cdot\mid S_0=s).
\end{aligned}
$$

- **Qué es:** el promedio de los valores de $X$, cada uno pesado por su probabilidad.
- **Cómo se calcula:** la suma de arriba; está definida si $X\ge0$ (puede valer $+\infty$) o si $\sum_j\lvert x_j\rvert\Pr(X=x_j)<\infty$.
- **Qué significa:** con muchas repeticiones independientes, el promedio observado de $X$ se acerca a $E[X]$.
- **Qué no es:** el valor más probable, ni un valor que $X$ tenga que tomar: un largo promedio de $3/2$ no es un largo.
:::

- **Notación:** $E_s$ y $\Pr_s$ se leen «empezando en $s$»; equivalen a tomar $\mu_0=\mathbf e_s$, la fila con 1 en $s$.
- **Indicadora:** si $X$ vale 1 cuando ocurre $A$ y 0 si no, $E[X]=\Pr(A)$. Una probabilidad es un valor esperado.

**En el juguete.** En la frase, $q=\widehat P(C\mid C)=1/3$:

$$
\begin{aligned}
E[L]&=\sum_{\ell=1}^\infty\ell\cdot\tfrac23\bigl(\tfrac13\bigr)^{\ell-1}\\
&=1\cdot\tfrac23+2\cdot\tfrac29+3\cdot\tfrac2{27}+\cdots
\end{aligned}
$$

- **Sumas parciales:** $0.667$, $1.111$, $1.333$… Sumarla a mano exige otra herramienta.

::: exercise {#mkv-c2-al-ej-indicadora title="Calcula una esperanza de un paso"}
En la frase, $X$ vale 1 si la siguiente letra es vocal y 0 si no. ¿Cuánto vale $E_C[X]$?
:::

::: hint {#mkv-c2-al-pista-indicadora of="mkv-c2-al-ej-indicadora" title="¿Qué probabilidad pesa al valor 1?"}
¿Qué entrada de $\widehat P$ da la probabilidad de vocal estando en C?
:::

::: answer {#mkv-c2-al-resp-indicadora of="mkv-c2-al-ej-indicadora"}
$$
E_C[X]=1\cdot\tfrac23+0\cdot\tfrac13=\tfrac23.
$$

**Es una probabilidad:** la de la fila C, columna V.
:::

¿Hay forma de obtener su suma sin sumar término por término?

---

## 4 · Condicionar en el primer paso

**Piensa: ¿y si partes la cuenta según lo que pasa en el primer paso?**

Promedias dentro de cada caso de $S_1$ y pesas cada promedio por su probabilidad.

::: theorem {#mkv-c2-teo-primer-paso title="Condicionar en el primer paso"}
$$
E[X]=\sum_{s:\ \Pr(S_1=s)>0}\Pr(S_1=s)\;E[X\mid S_1=s].
$$

**Condición.** $X$ es discreta y $E[X]$ está definida: $X\ge0$, o $\sum_j\lvert x_j\rvert\Pr(X=x_j)<\infty$. Los eventos $\{S_1=s\}$ forman una partición.

**Lectura.** Es probabilidad total (@mkv-c1-teo-total) aplicada a promedios.

**Casos nulos.** Los $s$ con $\Pr(S_1=s)=0$ se omiten: su condicional no está definida y no aportan.
:::

::: proof {#mkv-c2-al-dem-primer-paso of="mkv-c2-teo-primer-paso"}
Aplica probabilidad total a cada $\Pr(X=x_j)$ y cambia el orden de las sumas:

$$
\begin{aligned}
E[X]
&=\sum_j x_j\sum_s\Pr(X=x_j\mid S_1=s)\Pr(S_1=s)\\
&=\sum_s\Pr(S_1=s)\sum_jx_j\Pr(X=x_j\mid S_1=s)\\
&=\sum_s\Pr(S_1=s)\,E[X\mid S_1=s].
\end{aligned}
$$

Reordenar es válido porque los términos son no negativos, o la suma converge absolutamente: eso pide la condición.
:::

**En una cadena.** Empezando en $s$, el primer paso va a $s'$ con probabilidad $P_{ss'}$:

$$
E_s[X]=\sum_{s':\ P_{ss'}>0}P_{ss'}\;E_s[X\mid S_1=s'].
$$

- **Markov y homogeneidad:** dado $S_1=s'$, lo que sigue es una cadena que empieza en $s'$ (@mkv-c1-cadena).
- **El truco:** si $X$ cuenta pasos hasta un evento, el condicional es «1 más el mismo problema desde $s'$».

**En el juguete.** Empieza una racha: $S_0=C$. Si $S_1=V$, la racha midió 1. Si $S_1=C$, midió 1 más una racha que vuelve a empezar en C:

$$
\begin{aligned}
E[L]&=(1-q)\cdot1+q\,\bigl(1+E[L]\bigr),\\
E[L]&=\frac1{1-q}\quad\text{si }E[L]<\infty.
\end{aligned}
$$

- **La frase:** $q=1/3$ da $E[L]=3/2$, la suma de la serie de la sección 3, sin sumarla.
- **El *Quijote*:** $q\approx0.290$ da $E[L]\approx1.408$.
- **Los datos:** las 616 634 rachas reales suman 867 979 consonantes; su promedio es también $\approx1.408$.
- **Lo que no basta:** coincide la media, no la forma (@mkv-c1-tabla-rachas).
- **Con $k$ estados:** queda una ecuación por estado de partida, todas a la vez: un sistema lineal como el de la sección 1.

> [!WARNING]
> **Error típico: despejar sin revisar que la esperanza es finita.** Con $q=1$ la racha nunca termina: $E[L]=+\infty$ y la ecuación es $E=1+E$, sin solución finita. **La lectura correcta: primero asegura $E[L]<\infty$ (aquí, $q<1$); después despeja.**

::: exercise {#mkv-c2-al-ej-racha-v title="Mide una racha de vocales"}
En la frase, $\widehat P(V\mid V)=2/11$. Una racha de vocales empieza en V y termina al llegar una C. ¿Cuánto mide en promedio?
:::

::: hint {#mkv-c2-al-pista-racha-v of="mkv-c2-al-ej-racha-v" title="¿Qué papel juega ahora q?"}
¿Cuál es la probabilidad de seguir en la racha, y es menor que 1?
:::

::: answer {#mkv-c2-al-resp-racha-v of="mkv-c2-al-ej-racha-v"}
$$
E=\frac1{1-2/11}=\frac{11}9\approx1.222.
$$

**Mismo argumento:** seguir en V cuesta 1 paso más y vuelve a empezar. Es finita porque $2/11<1$.
:::

Promediar respondió «cuánto tarda». Falta una pregunta previa: si un estado puede llevar a otro.

---

## 5 · Alcanzar un estado en el grafo

**Piensa: desde $s$, ¿puede la cadena llegar alguna vez a $s'$?**

Puede si hay un camino de flechas positivas de $s$ a $s'$, por improbable que sea.

::: definition {#mkv-c2-def-alcanzar title="Camino y alcanzar en un grafo dirigido"}
$$
\begin{aligned}
&\text{camino de }t\text{ pasos de }s_i\text{ a }s_j:\
s_i=s_{i_0},s_{i_1},\dots,s_{i_t}=s_j,\\
&\hspace{4em}P_{i_mi_{m+1}}>0\quad(0\le m<t),\\
&s_i\to s_j\iff
\text{hay un camino de algún }t\ge0\text{ pasos}.
\end{aligned}
$$

- **Qué es:** $s_i\to s_j$, «$s_i$ alcanza a $s_j$», dice que existe una sucesión de flechas del grafo de $s_i$ a $s_j$.
- **Cómo se calcula:** se recorre el grafo desde $s_i$ siguiendo flechas, o se revisan las potencias de $P$.
- **Qué significa:** la cadena puede, con probabilidad positiva, pasar por $s_j$ si empieza en $s_i$.
- **Qué no es:** simétrico. $s_i\to s_j$ no implica $s_j\to s_i$.
:::

- **Paso cero:** sin flechas, todo estado se alcanza a sí mismo.
- **La flecha:** en la clase 1 era un paso; ahora $s\to s'$ admite caminos de cualquier largo.

::: theorem {#mkv-c2-al-teo-caminos title="Las potencias detectan caminos"}
Para toda matriz de transición $P$ y todo $t\ge0$:

$$
(P^t)_{ij}>0
\iff
\text{hay un camino de }t\text{ pasos de }s_i\text{ a }s_j.
$$

**Condición.** Entradas de $P$ no negativas, como en toda matriz de transición.

**Lectura.** $s_i\to s_j$ si y solo si $(P^t)_{ij}>0$ para algún $t\ge0$; con $s_i\ne s_j$ basta revisar $t\le k-1$.
:::

::: proof {#mkv-c2-al-dem-caminos of="mkv-c2-al-teo-caminos"}
Desarrolla la potencia con @mkv-c1-teo-potencias, un estado intermedio a la vez:

$$
(P^t)_{ij}=\sum_{i_1,\dots,i_{t-1}}P_{ii_1}P_{i_1i_2}\cdots P_{i_{t-1}j}.
$$

Cada sumando es no negativo, así que la suma es positiva si y solo si algún sumando lo es. Un sumando es positivo si y solo si todos sus factores lo son: es un camino. Con $t=0$, $P^0=I_k$ y $(I_k)_{ii}=1$.

**El tope $k-1$:** un camino que repite un estado contiene un ciclo; quitarlo da otro camino, más corto. Sin repetir, hay a lo más $k$ estados y $k-1$ pasos.
:::

**En el juguete.** En la alternante, $P^2=I_2$:

- **Regresar a A:** $(P^t)_{AA}>0$ solo con $t$ par. A se alcanza a sí misma, pero no en cualquier número de pasos.
- **Ir a B:** $(P^1)_{AB}=1$; así que $A\to B$ y $B\to A$.
- **En la identidad:** $P^t=I_2$ para todo $t$; $s_1$ no alcanza a $s_2$ ni al revés.

::: exercise {#mkv-c2-al-ej-pasos-impares title="Encuentra los pasos de ida"}
En la cadena A↔B, ¿para qué valores de $t$ es $(P^t)_{AB}>0$?
:::

::: hint {#mkv-c2-al-pista-pasos-impares of="mkv-c2-al-ej-pasos-impares" title="¿Dónde está la cadena tras un número par de pasos?"}
Si $P^2=I_2$, ¿cuánto vale $P^t$ según la paridad de $t$?
:::

::: answer {#mkv-c2-al-resp-pasos-impares of="mkv-c2-al-ej-pasos-impares"}
**Solo con $t$ impar.** Con $t$ par, $P^t=I_2$ y la entrada $AB$ es 0; con $t$ impar, $P^t=P$ y vale 1.
:::

Con estas cuatro herramientas ya se puede preguntar qué pasa a la larga. Antes, practícalas.

---

## Ejercicios

::: exercise {#mkv-c2-al-ej-tres-estados title="Resuelve la fila fija de tres estados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Una cadena tiene tres estados, $s_1,s_2,s_3$. Desde $s_1$ y desde $s_3$ siempre va a $s_2$; desde $s_2$ va a $s_1$ o a $s_3$ con probabilidad $1/2$ cada uno.

**Cambia una idea:** tres estados en lugar de dos, así que la fórmula $b/(a+b)$ ya no aplica.

1. **Escribe $P$** y el sistema $xP=x$, ecuación por ecuación.
2. **Encuentra la redundante:** muestra que la suma de las tres ecuaciones da $0=0$.
3. **Resuelve:** cambia una ecuación por $x_1+x_2+x_3=1$ y encuentra $x$.
4. **Revisa el alcance:** ¿cada estado alcanza a cada otro? Di con cuántos pasos basta.
:::

::: hint {#mkv-c2-al-pista-tres-estados-1 of="mkv-c2-al-ej-tres-estados" title="Pista 1 · ¿Qué columna de P da cada ecuación?"}
En $xP=x$, la entrada $j$ del lado izquierdo, ¿qué columna de $P$ combina con $x$? ¿Qué orígenes llegan a cada estado?
:::

::: hint {#mkv-c2-al-pista-tres-estados-2 of="mkv-c2-al-ej-tres-estados" title="Pista 2 · ¿Tu fila pasa las dos pruebas?"}
¿Tus tres números son no negativos y suman 1? ¿Al multiplicar tu fila por $P$ obtienes la misma fila?
:::

::: answer {#mkv-c2-al-resp-tres-estados of="mkv-c2-al-ej-tres-estados" title="Respuesta · Una fila fija con el doble en el centro"}
**1. Escribe $P$.**

$$
\begin{aligned}
P&=\begin{pmatrix}0&1&0\\ \tfrac12&0&\tfrac12\\ 0&1&0\end{pmatrix},\\
xP=x&\iff
\begin{cases}
\tfrac12x_2=x_1,\\
x_1+x_3=x_2,\\
\tfrac12x_2=x_3.
\end{cases}
\end{aligned}
$$

**2. Encuentra la redundante.** Pasa todo a la izquierda y suma: $(\tfrac12x_2-x_1)+(x_1+x_3-x_2)+(\tfrac12x_2-x_3)=0$, sin importar $x$. Cualquiera de las tres se deduce de las otras dos.

**3. Resuelve.** Cambia la segunda por la suma:

$$
\begin{aligned}
x_1=x_3=\tfrac12x_2,\qquad
\tfrac12x_2+x_2+\tfrac12x_2=1,\\
x_2=\tfrac12,\qquad
x=\bigl(\tfrac14,\ \tfrac12,\ \tfrac14\bigr).
\end{aligned}
$$

Comprueba: $xP=(\tfrac14,\ \tfrac14+\tfrac14,\ \tfrac14)=x$.

**4. Revisa el alcance.** Sí: $s_1\to s_2\to s_3$ y $s_3\to s_2\to s_1$. Bastan $k-1=2$ pasos, como dice @mkv-c2-al-teo-caminos.
:::

::: exercise {#mkv-c2-al-ej-llegar title="Calcula cuánto tarda en llegar"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Usa la cadena de tres estados del ejercicio anterior. Sea $X$ el número de pasos hasta estar en $s_3$ por primera vez; si ya empiezas en $s_3$, $X=0$.

**Cambia una idea:** en las rachas había un solo estado de partida; aquí hay dos, $s_1$ y $s_2$, y sus promedios dependen uno del otro.

1. **Plantea:** con condicionar en el primer paso, escribe $E_{s_1}[X]$ y $E_{s_2}[X]$ en términos de ellos mismos.
2. **Justifica la finitud:** explica por qué ambos son finitos antes de despejar.
3. **Resuelve** el sistema de dos ecuaciones.
4. **Interpreta:** ¿por qué tarda más desde $s_1$ que desde $s_2$?
:::

::: hint {#mkv-c2-al-pista-llegar-1 of="mkv-c2-al-ej-llegar" title="Pista 1 · ¿Qué queda pendiente tras el primer paso?"}
Desde cada estado, ¿a dónde puede ir en un paso, y cuánto falta en cada caso? ¿Cuánto falta si el paso cae en $s_3$?
:::

::: hint {#mkv-c2-al-pista-llegar-2 of="mkv-c2-al-ej-llegar" title="Pista 2 · ¿Cómo compruebas tus dos números?"}
¿Satisfacen tus valores las dos ecuaciones al sustituirlos? ¿Qué probabilidad hay de no haber llegado tras cada par de pasos?
:::

::: answer {#mkv-c2-al-resp-llegar of="mkv-c2-al-ej-llegar" title="Respuesta · Dos promedios que se llaman entre sí"}
**1. Plantea.** Escribe $m_1=E_{s_1}[X]$ y $m_2=E_{s_2}[X]$. Desde $s_1$ el paso va a $s_2$; desde $s_2$, mitad a $s_1$ y mitad a $s_3$, donde ya no falta nada:

$$
\begin{aligned}
m_1&=1+m_2,\\
m_2&=1+\tfrac12m_1+\tfrac12\cdot0.
\end{aligned}
$$

**2. Justifica la finitud.** Desde $s_1$ o $s_2$, en a lo más dos pasos se llega a $s_3$ con probabilidad $\ge\tfrac12$. No llegar en $2r$ pasos tiene probabilidad $\le(\tfrac12)^r$, así que $E[X]\le\sum_r 2(r+1)(\tfrac12)^r<\infty$.

**3. Resuelve.**

$$
\begin{aligned}
m_2&=1+\tfrac12(1+m_2)
\Rightarrow\tfrac12m_2=\tfrac32,\\
m_2&=3,\qquad m_1=4.
\end{aligned}
$$

**4. Interpreta.** Desde $s_1$ el primer paso es obligado a $s_2$: cuesta 1 y deja el problema de $s_2$. Por eso $m_1=1+m_2$.
:::

---

**Punto de control:** deberías poder plantear $xP=x$ con una ecuación cambiada por la suma. También, decir si una sucesión de filas tiene límite y qué promete un criterio de paro. Y condicionar en el primer paso con la esperanza finita, y leer en $P^t$ si un estado alcanza a otro.

---

## Lo que hay que llevarse

- **Sistema lineal:** ninguna, una o infinitas soluciones, nunca dos. La incógnita fila se traspone.

$$
\begin{aligned}
&xP=x,\quad x\mathbf 1=1\iff\\
&(P^{\mathsf T}-I_k)\,x^{\mathsf T}=0,\
\text{con una ecuación}\\
&\text{cambiada por la suma.}
\end{aligned}
$$

- **Dos estados:** $x=\bigl(b/(a+b),\ a/(a+b)\bigr)$; la frase da $(22/49,\ 27/49)\approx(0.449,\ 0.551)$.
- **Límite:** la distancia $\lVert x_t-x\rVert_1$ queda bajo toda $\mathrm{tol}$. La frase baja a $0.0034$ y $0.0027$ en $t=8$; la alternante desde A oscila y no tiene límite.
- **Criterio de paro:** cambio menor que $\mathrm{tol}$, con tope de pasos. Parar no prueba convergencia.
- **Valor esperado y primer paso:** $E[X]=\sum_s\Pr(S_1=s)E[X\mid S_1=s]$. Rachas: $E[L]=1/(1-q)$, $3/2$ en la frase y $\approx1.408$ en el *Quijote*, si $q<1$.
- **Alcanzar:** $s_i\to s_j$ si y solo si $(P^t)_{ij}>0$ para algún $t$, con $t\le k-1$ si $s_i\ne s_j$.

Continúa con [[mkv-clasificar-estados|Clasificar los estados]].
