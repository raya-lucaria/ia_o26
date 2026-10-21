---
id: mkv-olvida-su-inicio
title: "¿Olvida su inicio?"
nav_title: "¿Olvida su inicio?"
summary: "La conjetura de la tarea, revisada: cuándo dos inicios distintos acaban en la misma distribución, qué tan rápido se juntan, el algoritmo ITERACIÓN DE POTENCIAS con su tolerancia y su tope de pasos, y una trayectoria larga del Quijote frente a su estacionaria."
status: ready
estimated_time: 27m
tags: [markov, estacionaria, algoritmo]
---

# ¿Olvida su inicio?

**Si dejas correr una cadena desde dos inicios distintos, ¿acaban en la misma distribución? ¿Cuándo, y qué tan rápido?**

Al terminar tendrás:

- **La conjetura, revisada.** Dirás qué condición de @mkv-c2-teo-converge separa la matriz de la frase de la alternante.
- **Una cuenta a mano.** Medirás el ritmo $\lambda$: la distancia a ${\mu=(22/49,\ 27/49)}$ se multiplica por $16/33$ en cada paso.
- **El algoritmo ITERACIÓN DE POTENCIAS.** Seguirás su pseudocódigo y su Python, con tolerancia y tope de pasos.
- **Una trayectoria larga.** Compararás su fracción del tiempo en V con $\mu(V)$, en la frase y en el *Quijote*.
- **El alcance.** Distinguirás comprobar el procedimiento de validar el modelo.

## Lo que traes

- **Tu conjetura.** En el ejercicio @mkv-c1-ej-a-la-larga de la [[tarea-que-es-una-cadena|tarea de la clase 1]] dejaste correr dos matrices y escribiste en qué se distinguen.
- **PREDECIR.** De [[mkv-predecir|Predecir]]: ${\mu_{t+1}=\mu_tP}$, una multiplicación de vector por matriz por paso.
- **Límites y sistemas.** De [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]: la distancia $\lVert x-y\rVert_1$, la tolerancia $\mathrm{tol}$ y cómo resolver ${\mu P=\mu}$ con ${\sum=1}$.
- **Clases y periodo.** De [[mkv-clasificar-estados|Clasificar los estados]]: clase cerrada (@mkv-c2-def-clase-cerrada) y periodo (@mkv-c2-def-periodo).
- **La estacionaria.** De [[mkv-la-estacionaria|La estacionaria y sus cuatro teoremas]]: la definición @mkv-c2-def-estacionaria y los teoremas @mkv-c2-teo-unica, @mkv-c2-teo-converge y @mkv-c2-teo-ergodico.

> **Modelo y datos.** Cadenas finitas y homogéneas. La frase usa ${\widehat P=\begin{pmatrix}2/11&9/11\\2/3&1/3\end{pmatrix}}$ en el orden V, C; el *Quijote*, su $\widehat P$ de la clase 1.

---

## 1 · Revisar la conjetura de la tarea

**Piensa: ¿qué tenía la matriz de la frase que no tenía la alternante?**

Una sola clase cerrada **aperiódica**. @mkv-c2-teo-converge lo dice para cualquier cadena finita de $k$ estados: con una sola clase cerrada y aperiódica, ${\mu_0P^t\to\mu}$ **desde todo** $\mu_0$. El límite es la única estacionaria de @mkv-c2-teo-unica.

- **En palabras.** Olvidar el inicio es que $\mu_t$ deje de depender de $\mu_0$ cuando $t$ crece.
- **Condición exacta.** En una cadena finita, una sola clase cerrada aperiódica es necesaria y suficiente para converger a la misma $\mu$ desde todo $\mu_0$. Desde un inicio particular, $\mu_0P^t$ puede converger sin ella.
- **Lo que no dice.** Cuántos pasos hacen falta.
- **Tres preguntas.** [[mkv-la-estacionaria|La estacionaria]] separó $\mu_t$ en el paso $t$, su límite y la fracción del tiempo. Esta página responde la segunda a mano y con un algoritmo, y la tercera simulando.

**En el juguete.** La tarea dejó dos sucesiones de ${\Pr(S_t=V)}$ con la matriz de la frase:

- **Desde V:** 1.000, 0.182, 0.579, 0.386, 0.479, 0.434, 0.456, 0.446, 0.451.
- **Desde C:** 0.000, 0.667, 0.343, 0.500, 0.424, 0.461, 0.443, 0.452, 0.448.
- **La frase cumple.** V y C se comunican y no hay más clases; el lazo ${P_{VV}=2/11>0}$ la hace aperiódica.
- **La alternante no.** Con estados A, B, sus filas son ${(0,\ 1)}$ y ${(1,\ 0)}$: una clase cerrada de periodo 2. Desde A da 1, 0, 1, 0, … (la tarea la corrió con V y C).

::: figure {#mkv-c2-fig-mu-t-inicios title="Dos inicios que se juntan y uno que no se asienta"}
![Probabilidad de estar en el primer estado en el paso t, de t = 0 a 10. Matriz de la frase (V, C) desde V: 1.000, 0.182, 0.579, 0.386, 0.479, 0.434, 0.456, 0.446, 0.451, 0.448, 0.449. Desde C: 0.000, 0.667, 0.343, 0.500, 0.424, 0.461, 0.443, 0.452, 0.448, 0.450, 0.449. Las dos se juntan en μ(V) = 22/49 ≈ 0.449; la distancia a μ se multiplica por 16/33 en cada paso. Cadena alternante desde A: 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1; alterna entre 1 y 0 y no converge.](../_assets/mkv-c2-mu-t-inicios.svg)
:::

- **Qué es un punto.** Una cuenta exacta, ${\mu_t(V)=(\mu_0P^t)(V)}$; aquí no hay azar ni réplicas.
- **Lo que se ve.** Las dos curvas de la frase quedan a 0.003 en ${t=8}$. La alternante no se acerca a nada.
- **Por qué zigzaguea.** Desde V la cadena pasa a C con $9/11$, y desde C vuelve a V con $2/3$. Cada paso corrige de más, pero cada vez menos.

> [!WARNING]
> **Leer «converge desde todo inicio» como «converge desde algún inicio».** La alternante desde ${(1/2,\ 1/2)}$ no se mueve.
> **Un inicio que ya es estacionario no prueba nada: el teorema pide converger desde todos.**

::: exercise {#mkv-c2-ol-ej-lazo title="Agrega un lazo"}
Cambia la alternante por ${P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}}$, en el orden A, B. ¿Cumple las condiciones de @mkv-c2-teo-converge? ¿Olvida su inicio?
:::

::: hint {#mkv-c2-ol-pista-lazo of="mkv-c2-ol-ej-lazo" title="¿Qué regresos a A son posibles?"}
¿Puede volver a A en un paso? ¿Y en dos?
:::

::: answer {#mkv-c2-ol-resp-lazo of="mkv-c2-ol-ej-lazo"}
Sí. A y B se comunican, así que hay una sola clase y es cerrada. Desde A se regresa en 1 paso (el lazo) o en 2 (A, B, A): el periodo es ${\operatorname{mcd}\{1,2\}=1}$. Por @mkv-c2-teo-converge, $\mu_t$ tiende a la misma $\mu$ desde todo inicio.
:::

El teorema dice que se juntan; con dos estados podemos medir también qué tan rápido.

---

## 2 · Medir a mano cuánto falta

**Piensa: ¿a qué vector se acercan las dos sucesiones, y a qué ritmo?**

Al vector que no cambia al multiplicarlo por $P$. Con $k$ estados, $\mu$ resuelve el sistema de @mkv-c2-def-estacionaria:

$$
\mu P=\mu,\qquad \sum_{s\in\mathcal S}\mu(s)=1,\qquad \mu\ge0.
$$

- **Qué se mide.** La distancia ${\lVert\mu_t-\mu\rVert_1=\sum_s\lvert\mu_t(s)-\mu(s)\rvert}$. Olvidar el inicio es que tienda a 0.

**En el juguete.** El destino ya lo resolviste en [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]: con dos estados, ${\mu=\bigl(b/(a+b),\ a/(a+b)\bigr)}$, y en la frase ${\mu=(22/49,\ 27/49)}$, con ${22/49\approx0.449}$.

- **Comprobación.** ${\tfrac{22}{49}\cdot\tfrac{2}{11}+\tfrac{27}{49}\cdot\tfrac{2}{3}=\tfrac{4}{49}+\tfrac{18}{49}=\tfrac{22}{49}}$: la entrada V no cambia.
- **Lo nuevo.** No es el destino sino el ritmo: cuánto se acorta la distancia en cada paso.

Ahora, el ritmo. Con dos estados basta seguir la entrada V, porque la de C es su complemento.

::: theorem {#mkv-c2-ol-teo-dos-estados title="Con dos estados, la distancia se multiplica por un número fijo"}
Sea una cadena de dos estados con ${P_{12}=a}$, ${P_{21}=b}$ y estacionaria $\mu$. Sea ${\lambda=1-a-b}$. Para todo $\mu_0$ y todo ${t\ge0}$:

$$
\lVert\mu_t-\mu\rVert_1=\lvert\lambda\rvert^t\,\lVert\mu_0-\mu\rVert_1.
$$

- **Condición.** Dos estados y una $\mu$ estacionaria. Si ${a+b>0}$, es la única: ${\mu=\bigl(b/(a+b),\ a/(a+b)\bigr)}$, la de [[mkv-algebra-y-limites|álgebra y límites]].
- **Lectura.** Cada paso multiplica la distancia por $\lvert\lambda\rvert$. Si ${\lambda<0}$, la diferencia cambia de signo: $\mu_t$ zigzaguea alrededor de $\mu$.
- **Casos nulos.** ${\lambda=-1}$ es la alternante: la distancia no baja. ${\lambda=1}$ es la identidad: nada se mueve.
:::

::: proof {#mkv-c2-ol-dem-dos-estados of="mkv-c2-ol-teo-dos-estados"}
Escribe ${x_t=\mu_t(s_1)}$. Un paso de ${\mu_{t+1}=\mu_tP}$ da ${x_{t+1}=x_t(1-a)+(1-x_t)\,b=b+\lambda x_t}$. La estacionaria cumple lo mismo: ${\mu(s_1)=b+\lambda\,\mu(s_1)}$. Restando, ${x_{t+1}-\mu(s_1)=\lambda\,(x_t-\mu(s_1))}$. Con dos estados, ${\lVert\mu_t-\mu\rVert_1=2\lvert x_t-\mu(s_1)\rvert}$; repite $t$ veces.
:::

**En el juguete.** Con la frase, ${\lambda=1-\tfrac{9}{11}-\tfrac{2}{3}=\tfrac{2}{11}-\tfrac{2}{3}=-\tfrac{16}{33}\approx-0.485}$. Las distancias de partida son:

$$
\begin{aligned}
\lVert\mathbf e_1-\mu\rVert_1&=2\cdot\tfrac{27}{49}=\tfrac{54}{49}\approx1.102,\\
\lVert\mathbf e_2-\mu\rVert_1&=2\cdot\tfrac{22}{49}=\tfrac{44}{49}\approx0.898.
\end{aligned}
$$

| t | desde V | desde C |
|---:|---|---|
| 0 | 1.102 | 0.898 |
| 1 | 0.534 | 0.435 |
| 2 | 0.259 | 0.211 |
| 4 | 0.061 | 0.050 |
| 8 | 0.0034 | 0.0027 |
| 10 | 0.0008 | 0.0006 |

- **Menos de la mitad.** ${16/33<1/2}$: por eso la tarea veía la distancia «en menos de la mitad» cada paso.
- **El zigzag.** ${\lambda<0}$ explica que ${\Pr(S_t=V)}$ quede por arriba y por abajo de 0.449, alternando.
- **Las dos sucesiones entre sí.** Su diferencia en V es ${\lvert\lambda\rvert^t}$: 1 en ${t=0}$, 0.003 en ${t=8}$.

::: exercise {#mkv-c2-ol-ej-ritmo title="Calcula el ritmo de otra matriz"}
Una cadena tiene filas ${(1/2,\ 1/2)}$ y ${(1/4,\ 3/4)}$. Calcula $\mu$, $\lambda$ y ${\lVert\mu_3-\mu\rVert_1}$ desde ${\mathbf e_1}$. ¿Zigzaguea?
:::

::: hint {#mkv-c2-ol-pista-ritmo of="mkv-c2-ol-ej-ritmo" title="¿Quiénes son a y b?"}
¿Qué entradas fuera de la diagonal tiene la matriz?
:::

::: answer {#mkv-c2-ol-resp-ritmo of="mkv-c2-ol-ej-ritmo"}
Con ${a=1/2}$ y ${b=1/4}$: ${\mu=(1/3,\ 2/3)}$ y ${\lambda=1/4}$. La distancia inicial es ${2\cdot\tfrac{2}{3}=\tfrac{4}{3}}$, así que ${\lVert\mu_3-\mu\rVert_1=\tfrac{4}{3}\cdot\tfrac{1}{64}=\tfrac{1}{48}}$. Como ${\lambda>0}$, no zigzaguea: se acerca siempre desde arriba.
:::

**El caso grande.** El *Quijote* también tiene dos estados, así que el teorema aplica con su $\widehat P$. Su ${\lambda\approx-0.530}$ queda un poco más cerca de $-1$ que el de la frase.

| t | desde V | desde C |
|---:|---|---|
| 0 | 1.071 | 0.929 |
| 1 | 0.568 | 0.492 |
| 2 | 0.301 | 0.261 |
| 4 | 0.084 | 0.073 |
| 8 | 0.0067 | 0.0058 |
| 10 | 0.0019 | 0.0016 |

- **Más lento.** En ${t=10}$ la frase ya está a 0.0008 desde V; el *Quijote*, a 0.0019. Un $\lvert\lambda\rvert$ mayor deja más distancia cada paso.
- **Su destino.** Sale de la misma fórmula ${b/(a+b)}$:

  $$
  \begin{aligned}
  \mu&=\left(\tfrac{752\,551}{1\,620\,531},\ \tfrac{867\,980}{1\,620\,531}\right)\\
  &\approx(0.4644,\ 0.5356).
  \end{aligned}
  $$

Con $k$ estados no hay un solo $\lambda$ que leer en la matriz; hace falta un procedimiento que itere y sepa parar.

---

## 3 · Iterar hasta que deje de moverse

**Piensa: ¿cómo encuentras $\mu$ con miles de estados, sin resolver el sistema?**

Multiplicando por $P$ hasta que el vector deje de cambiar. Si la cadena cumple @mkv-c2-teo-converge, ${\mu_0P^t\to\mu}$; basta aproximar el límite. Si no lo cumple, el cambio puede no bajar nunca de la tolerancia: por eso lleva un tope.

> **Dado:** una cadena finita y homogénea, matriz $P$ de ${k\times k}$, distribución fila $\mu_0$, una tolerancia ${\mathrm{tol}>0}$ y un tope de pasos.
>
> **Encontrar:** un vector cercano a la estacionaria $\mu$ de @mkv-c2-def-estacionaria y cuántos pasos costó, o el aviso de que no paró.

### El mapa de ITERACIÓN DE POTENCIAS

- **Qué calcula:** ${\mu_0P^t}$ para $t$ creciente, hasta que dos vectores seguidos difieren en a lo más $\mathrm{tol}$.
- **Qué guarda:** la matriz, el vector actual, el siguiente y el contador de pasos.
- **Cómo avanza:** un paso de PREDECIR, ${\mu\leftarrow\mu P}$, y mide ${d=\lVert\mu P-\mu\rVert_1}$.
- **A qué converge y bajo qué condición:** a la única $\mu$, desde todo $\mu_0$, si hay una sola clase cerrada y es aperiódica (@mkv-c2-teo-converge). Sin esa condición, puede no cumplir la tolerancia y terminar por el tope.

::: figure {#mkv-c2-fig-flujo-potencias title="La iteración de potencias, en palabras"}
![Diagrama de flujo de la iteración de potencias, en palabras. 1: Empieza: μ ← μ₀ y pasos = 1. 2: Multiplica: nuevo = μP. 3: Mide d = ‖nuevo − μ‖₁ y avanza: μ ← nuevo. 4, pregunta: ¿d ≤ tol? Si no, sigue abajo. 5, pregunta: ¿pasos llegó al tope? Si no, sigue abajo. 6: Suma 1 a pasos. 7: Devuelve (μ, «no paró»). 8: Devuelve (μ, pasos). Desde el paso 6, si otra vuelta, vuelve al paso 2. Desde el paso 4, si sí, salta al paso 8. Desde el paso 5, si sí, salta al paso 7. «No paró» no prueba que no converja: solo que no cumplió tol a tiempo. Cada vuelta cuesta k² productos.](../_assets/mkv-c2-flujo-potencias.svg)
:::

```text
INPUT   P, de k×k, filas que suman 1;
        μ_0, vector fila que suma 1;
        tol > 0; tope ≥ 1 entero.
OUTPUT  (μ, pasos) si paró;
        (μ, «no paró») si llegó al tope.

 1 function ITERACIÓN-DE-POTENCIAS(
        P, μ_0, tol, tope)
 2   μ ← μ_0
 3   for pasos ← 1 to tope
 4     nuevo ← μ·P        ▷ PREDECIR, t = 1
 5     d ← ‖nuevo − μ‖₁
 6     μ ← nuevo
 7     if d ≤ tol
 8       return (μ, pasos)
 9   return (μ, «no paró»)
```

**Gemelo Python.** Cada comentario numerado remite al pseudocódigo. Usa decimales, como un programa real.

```python
def iteracion_potencias(P, mu0, tol, tope):   # (1)
    k = len(mu0)
    mu = list(mu0)                            # (2)
    for pasos in range(1, tope + 1):          # (3)
        nuevo = [sum(mu[s] * P[s][s2]         # (4)
                     for s in range(k))
                 for s2 in range(k)]
        d = sum(abs(nuevo[i] - mu[i])         # (5)
                for i in range(k))
        mu = nuevo                            # (6)
        if d <= tol:                          # (7)
            return mu, pasos                  # (8)
    return mu, None                           # (9) no paró

frase = [[2 / 11, 9 / 11], [2 / 3, 1 / 3]]
mu, pasos = iteracion_potencias(frase, [0, 1], 1e-6, 1000)
print([round(x, 6) for x in mu], pasos)
# [0.44898, 0.55102] 21
alternante = [[0, 1], [1, 0]]
print(iteracion_potencias(alternante, [1, 0], 1e-6, 1000))
# ([1, 0], None)
```

**Cada pieza, en su línea:**

- **Línea 4.** Es PREDECIR con un solo paso: ${k^2}$ productos.
- **Línea 5.** Mide cuánto se movió el vector, no cuánto le falta: $\mu$ todavía no se conoce.
- **Líneas 7 y 9.** La tolerancia decide si paró; el tope garantiza que el ciclo termina aunque la cadena no converja.
- **«No paró» no es «no converge».** Solo dice que no cumplió la tolerancia dentro del tope; con un tope mayor, una cadena lenta sí pararía.
- **Por qué no siempre el sistema.** Resolver $k$ ecuaciones por eliminación cuesta del orden de $k^3$ operaciones. Iterar cuesta $k^2$ por paso, y menos si casi todas las entradas de $P$ son 0: solo se multiplican las flechas que existen.

**Cómo leer la traza.** La frase desde C, con ${\mathrm{tol}=10^{-2}}$. Cada renglón muestra $\mu(V)$ y $d$ tras el paso indicado.

**Tramo único · De C hasta parar**

| pasos | μ(V) | d |
|---:|---|---|
| 1 | 0.667 | 1.333 |
| 2 | 0.343 | 0.646 |
| 3 | 0.500 | 0.313 |
| 4 | 0.424 | 0.152 |
| 5 | 0.461 | 0.074 |
| 6 | 0.443 | 0.036 |
| 7 | 0.452 | 0.017 |
| 8 | 0.448 | 0.008 |

- **Paso 8.** ${d\approx0.008\le0.01}$: devuelve ${\mu(V)\approx0.448}$ y 8 pasos. Su distancia real a $\mu$ es 0.0027.
- **Con ${\mathrm{tol}=10^{-6}}$.** Desde V o desde C, para en 21 pasos con ${\mu\approx(0.4490,\ 0.5510)}$.

::: exercise {#mkv-c2-ol-ej-traza-alternante title="Traza la alternante"}
Corre ITERACIÓN DE POTENCIAS con la alternante desde ${\mu_0=(1,\ 0)}$, ${\mathrm{tol}=10^{-2}}$ y ${\mathrm{tope}=4}$. Llena los «?»; ¿qué devuelve?

| pasos | μ(A) | d |
|---:|---|---|
| 1 | 0 | ? |
| 2 | ? | ? |
| 3 | ? | ? |
| 4 | ? | ? |
:::

::: hint {#mkv-c2-ol-pista-traza-alternante of="mkv-c2-ol-ej-traza-alternante" title="¿Qué hace el vector en un paso?"}
¿Qué vector sale de multiplicar ${(1,\ 0)}$ por la alternante, y de multiplicar ese por la alternante otra vez?
:::

::: answer {#mkv-c2-ol-resp-traza-alternante of="mkv-c2-ol-ej-traza-alternante"}
En negrita, lo que era «?».

| pasos | μ(A) | d |
|---:|---|---|
| 1 | 0 | **2** |
| 2 | **1** | **2** |
| 3 | **0** | **2** |
| 4 | **1** | **2** |

El vector salta entre ${(1,\ 0)}$ y ${(0,\ 1)}$; cada paso mueve 2. Nunca baja de $\mathrm{tol}$: llega a la línea 9 y devuelve ${((1,\ 0),\ \text{«no paró»})}$. Con cualquier tope pasaría igual.
:::

> [!WARNING]
> **Leer $d\le\mathrm{tol}$ como «estoy a $\mathrm{tol}$ de $\mu$».** $d$ mide cuánto se movió el último paso.
> **Si la cadena se mueve despacio, el vector puede quedar mucho más lejos de $\mu$ que $\mathrm{tol}$.**

Con dos estados y ${a+b>0}$, de modo que ${\lambda<1}$, se puede medir. Sale de la prueba de @mkv-c2-ol-teo-dos-estados, con ${e=x_{t-1}-\mu(s_1)}$ antes del último paso y ${x_t-\mu(s_1)=\lambda e}$ después:

- **Lo que se movió.** ${d=2\lvert x_t-x_{t-1}\rvert=2\lvert\lambda e-e\rvert=2(1-\lambda)\lvert e\rvert}$.
- **Lo que falta.** ${\lVert\mu_t-\mu\rVert_1=2\lvert\lambda\rvert\lvert e\rvert}$. Dividiendo, falta ${d\cdot\lvert\lambda\rvert/(1-\lambda)}$.

Para la identidad, ${\lambda=1}$, no aplica. En la frase, ${16/49}$ de $d$; con ${\lambda=0.999}$, 999 veces $d$.

### Lo que garantiza y cuánto cuesta

- **Propiedades:** termina en a lo más «tope» pasos. Cada vector sigue siendo una distribución.
- **Número que da:** con la frase y ${\mathrm{tol}=10^{-6}}$, ${\mu\approx(0.4490,\ 0.5510)}$ en 21 pasos. Con el *Quijote*, ${\mu\approx(0.4644,\ 0.5356)}$ en 24 pasos, desde V o desde C.
- **Garantía:** con una sola clase cerrada aperiódica, ${\mu_0P^t\to\mu}$. Si el tope alcanza para cumplir la tolerancia, el error del vector devuelto tiende a 0 cuando $\mathrm{tol}$ tiende a 0. Si termina por el tope, no garantiza cercanía. Sin la condición, nada.
- **Costo:** ${k^2}$ productos por paso, ${\text{pasos}\cdot k^2}$ en total. Guarda la matriz y dos vectores.
- **Supuestos:** $P$ fija, filas que suman 1, $\mu_0$ distribución. Decimales: el redondeo se acumula.
- **Lo que no sabe.** Cuántos pasos tardará: lo fija la cadena, no el algoritmo. Con dos estados se predice con $\lambda$; con $k$, no se lee en una entrada.

**El caso grande.** El *Quijote* tarda 24 pasos y no 21: su ${\lvert\lambda\rvert\approx0.530}$ es mayor que ${16/33}$. Con miles de estados, el mismo ciclo sirve sin cambiar una línea; solo crece el costo por paso.

| Ruta | Qué da | Qué pide |
|---|---|---|
| A mano | $\mu$ exacta | Resolver $k$ ecuaciones |
| Iterar | $\mu$ aproximada y los pasos | Una clase cerrada aperiódica |
| Simular | Fracción del tiempo | Una clase cerrada |

- **Tres rutas, un número.** Las tres apuntan a la misma $\mu$ cuando sus condiciones se cumplen. La tercera es la que falta.

El algoritmo calcula $\mu$ multiplicando; una trayectoria la puede estimar contando.

---

## 4 · Simular una trayectoria larga

**Piensa: ¿qué dice $\mu$ de una sola trayectoria, y no de una distribución?**

Cuánto tiempo pasa en cada estado. @mkv-c2-teo-ergodico lo dice para cualquier cadena finita con una sola clase cerrada, periódica o no. Desde cualquier inicio, con probabilidad 1:

$$
\frac{N_T(s)}{T}\xrightarrow[T\to\infty]{}\mu(s),
$$

donde ${N_T(s)}$ cuenta las visitas a $s$ en los pasos ${0,\dots,T-1}$.

- **Otra pregunta.** Ya no es ${\Pr(S_t=s)}$ en un paso, sino la fracción del tiempo de **una** réplica.

**Cómo se simula.** Una sola réplica, larga:

- **Sorteos.** Empieza en el estado dado. Cada paso usa MUESTREAR-FILA con un $u$ nuevo sobre la fila del estado actual.
- **Conteo.** Antes de cada paso suma 1 a la cuenta del estado actual; al final divide entre $T$.
- **Semilla.** Fija la sucesión de uniformes: con la misma, la trayectoria se repite.

**En el juguete.** Una trayectoria de la frase desde C, con ${T=10\,000}$ y semilla 2042, pasa en V una fracción 0.4494. ${\mu(V)=22/49\approx0.4490}$.

- **La alternante.** Desde A, la fracción en A es exactamente $1/2$ con $T$ par. La convergencia de $\mu_t$ falla; la del tiempo no.
- **Dos clases cerradas.** El teorema ya no aplica. El ejercicio siguiente muestra qué pasa entonces.

**El caso grande.** Una trayectoria del *Quijote* desde C, con ${T=100\,000}$ y semilla 2037, pasa en V una fracción 0.46434. ${\mu(V)\approx0.46439}$: difieren en 0.00005.

> [!WARNING]
> **Leer la concordancia como validación del modelo.** La trayectoria se muestreó de la misma $\widehat P$ cuya $\mu$ calculamos.
> **Que coincidan comprueba el procedimiento; no prueba que el *Quijote* sea una cadena de memoria 1.**

- **Sin error estándar.** ${\sqrt{p(1-p)/n}}$ de [[mkv-predecir|Predecir]] pide réplicas independientes. Las visitas de una trayectoria no lo son.
- **Lo que dice.** Una réplica larga pasa en cada estado una fracción cercana a $\mu$, aunque $\mu_t$ oscile, como en la alternante.
- **Lo que no dice.** No da cuántos pasos bastan ni un margen de error. Con dos clases cerradas, ni siquiera da un número fijo.

::: exercise {#mkv-c2-ol-ej-dos-clases title="Explica cinco réplicas que no coinciden"}
Con ${P=\begin{pmatrix}1/2&1/4&1/4\\0&1&0\\0&0&1\end{pmatrix}}$, cinco trayectorias desde $s_1$, de ${T=1000}$ pasos, pasan en $s_2$ las fracciones 0, 0.998, 0, 0 y 0.998. ¿Qué recorridos explican esos valores? ¿Podrían salir otras fracciones en réplicas nuevas? ¿Por qué no contradicen @mkv-c2-teo-ergodico?
:::

::: hint {#mkv-c2-ol-pista-dos-clases of="mkv-c2-ol-ej-dos-clases" title="¿Cuántas clases cerradas hay?"}
Una vez que la trayectoria sale de $s_1$, ¿puede volver?
:::

::: answer {#mkv-c2-ol-resp-dos-clases of="mkv-c2-ol-ej-dos-clases"}
$s_1$ es transitorio y ${\{s_2\}}$, ${\{s_3\}}$ son dos clases cerradas. Cada trayectoria pasa unos pasos en $s_1$ y luego cae en una de ellas para siempre. Si cae en $s_2$, su fracción ahí es casi 1 (0.998: dos de los mil pasos fueron en $s_1$); si cae en $s_3$, es 0.

No son los únicos valores posibles: una réplica que sale hacia $s_2$ en el primer paso da 0.999, y una que sale en el tercero, 0.997. El límite es aleatorio: 1 o 0.

El teorema pide una sola clase cerrada; aquí hay dos, así que no aplica.
:::

Ya puedes revisar la conjetura con matrices que no son de dos estados.

---

## Ejercicios

::: exercise {#mkv-c2-ol-ej-tres-estados title="Itera con tres estados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Un robot visita tres salas, 1, 2 y 3. En cada paso deja la sala donde está y entra a una de las otras dos, cada una con probabilidad $1/2$. Las probabilidades no cambian con el tiempo. **Cambia una idea:** ahora son tres estados, así que no hay una $\lambda$ que leer de una entrada.

$$
P=\begin{pmatrix}
0&1/2&1/2\\
1/2&0&1/2\\
1/2&1/2&0
\end{pmatrix},
\qquad \mu_0=\mathbf e_1.
$$

1. **Revisa las condiciones.** ¿Cumple @mkv-c2-teo-converge? Justifica clase y periodo.
2. **Calcula $\mu$.** Comprueba que ${\mu P=\mu}$.
3. **Traza.** Calcula $\mu_1$, $\mu_2$, $\mu_3$ y sus distancias a $\mu$.
4. **Predice el paro.** ¿En cuántos pasos para ITERACIÓN DE POTENCIAS con ${\mathrm{tol}=10^{-2}}$?
:::

::: hint {#mkv-c2-ol-pista-tres-estados-1 of="mkv-c2-ol-ej-tres-estados" title="Pista 1 · ¿Qué necesitas para cada entregable?"}
Separa tu propuesta en clases, longitudes posibles de regreso a la sala 1 y ecuaciones de la estacionaria. ¿Qué información de la matriz necesitas para cada parte?
:::

::: hint {#mkv-c2-ol-pista-tres-estados-2 of="mkv-c2-ol-ej-tres-estados" title="Pista 2 · ¿Comparaste contra el vector correcto?"}
En el entregable 3, ¿restaste $\mu$? En el 4, ¿restaste el vector anterior, como la línea 5?
:::

::: answer {#mkv-c2-ol-resp-tres-estados of="mkv-c2-ol-ej-tres-estados" title="Respuesta · Tres salas que se juntan"}
**1. Condiciones.** Las tres salas se comunican: una sola clase, cerrada. Se regresa a 1 en 2 pasos (1, 2, 1) y en 3 (1, 2, 3, 1). El periodo es ${\operatorname{mcd}\{2,3\}=1}$: aperiódica. Cumple.

**2. Estacionaria.** Cada columna suma 1, así que ${\mu=(1/3,\ 1/3,\ 1/3)}$ cumple ${\mu P=\mu}$. Por @mkv-c2-teo-unica es la única.

**3. Traza.**

$$
\begin{aligned}
\mu_1&=\left(0,\ \tfrac{1}{2},\ \tfrac{1}{2}\right),\\
\mu_2&=\left(\tfrac{1}{2},\ \tfrac{1}{4},\ \tfrac{1}{4}\right),\\
\mu_3&=\left(\tfrac{1}{4},\ \tfrac{3}{8},\ \tfrac{3}{8}\right).
\end{aligned}
$$

Sus distancias a $\mu$ son $2/3$, $1/3$ y $1/6$.

Desde ${\lVert\mathbf e_1-\mu\rVert_1=4/3}$, cada paso la parte a la mitad. Es un caso simétrico; en general, no hay razón fija.

**4. Paro.** Los movimientos son ${d=2,\ 1,\ 1/2,\ \dots}$: ${d=2\cdot(1/2)^{\text{pasos}-1}}$. Pide ${2^{\text{pasos}-1}\ge200}$: para en 9 pasos, con ${d=1/128\approx0.008}$.
:::

::: exercise {#mkv-c2-ol-ej-cadena-lenta title="Desconfía de una cadena lenta"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Un foco está encendido o apagado, en ese orden. En cada paso cambia de estado con probabilidad $1/100$ y se queda igual con $99/100$. Empieza encendido. **Cambia una idea:** la cadena cumple todas las condiciones, pero se mueve despacio.

$$
P=\begin{pmatrix}99/100&1/100\\1/100&99/100\end{pmatrix},
\qquad \mu_0=\mathbf e_1.
$$

1. **Calcula.** $\mu$, $\lambda$ y ${\lVert\mu_t-\mu\rVert_1}$ como función de $t$.
2. **Mide el paro.** Cuando ITERACIÓN DE POTENCIAS para con ${d\le\mathrm{tol}}$, ¿cuántas veces $d$ puede faltar todavía?
3. **Compara.** La corrida con ${\mathrm{tol}=10^{-6}}$ para en 492 pasos. ¿Su vector está a menos de $10^{-6}$ de $\mu$?
4. **Corrige.** ¿Qué $\mathrm{tol}$ pedirías para quedar a menos de $10^{-6}$? ¿Por qué esa corrección no se traslada a $k$ estados?
:::

::: hint {#mkv-c2-ol-pista-cadena-lenta-1 of="mkv-c2-ol-ej-cadena-lenta" title="Pista 1 · ¿Qué resultado de esta página aplica?"}
¿Cuánto valen $a$ y $b$? ¿Qué relación hay entre lo que se mueve un paso y lo que falta?
:::

::: hint {#mkv-c2-ol-pista-cadena-lenta-2 of="mkv-c2-ol-ej-cadena-lenta" title="Pista 2 · ¿Tu cota tiene sentido con la frase?"}
Si sustituyes ${\lambda=-16/33}$ en tu respuesta al entregable 2, ¿recuperas el ${16/49}$ de la página?
:::

::: answer {#mkv-c2-ol-resp-cadena-lenta of="mkv-c2-ol-ej-cadena-lenta" title="Respuesta · Un paro que se engaña"}
**1. Cuenta.** Con ${a=b=1/100}$: ${\mu=(1/2,\ 1/2)}$ y ${\lambda=98/100}$. La distancia inicial es 1, así que ${\lVert\mu_t-\mu\rVert_1=0.98^t}$.

**2. Paro.** Lo que falta es ${d\cdot\lambda/(1-\lambda)=49\,d}$: hasta 49 veces la tolerancia.

**3. No.** El vector devuelto queda a unos ${4.8\times10^{-5}}$ de $\mu$, casi 50 veces $10^{-6}$. El paro creyó estar cerca porque cada paso se mueve poco.

**4. Corrección.** Con ${\mathrm{tol}=10^{-6}/49}$ se garantiza la distancia. Requiere conocer $\lambda$, que con dos estados se lee en la matriz; con $k$ estados no hay un solo número que leer.
:::

**Punto de control:** deberías poder decir qué condición de @mkv-c2-teo-converge falta en cada contraejemplo y calcular $\mu$ de una cadena de dos estados. También, medir su ritmo con $\lambda$, correr ITERACIÓN DE POTENCIAS con tolerancia y tope, y leer una fracción del tiempo sin confundirla con validar el modelo.

---

## Lo que hay que llevarse

- **La conjetura, con condición.** Una sola clase cerrada aperiódica es necesaria y suficiente para olvidar el inicio desde todo $\mu_0$ (@mkv-c2-teo-converge). La alternante tiene periodo 2: desde A da 1, 0, 1, 0, …
- **El destino.** La frase va a ${\mu=(22/49,\ 27/49)}$, con ${22/49\approx0.449}$, la fórmula $b/(a+b)$ de la página 1.
- **El ritmo con dos estados.** La distancia se multiplica por ${\lvert\lambda\rvert=\lvert1-a-b\rvert}$; en la frase, ${16/33\approx0.485}$. En ${t=8}$, las dos sucesiones distan 0.003.
- **El algoritmo.** ITERACIÓN DE POTENCIAS para cuando ${d\le\mathrm{tol}}$ o al llegar al tope. Con ${\mathrm{tol}=10^{-6}}$: 21 pasos en la frase, 24 en el *Quijote*. La alternante desde A, con ${\mathrm{tol}<2}$, termina por el tope y devuelve «no paró».
- **La tolerancia.** $d$ es lo que se movió el último paso, no lo que falta.
- **Una trayectoria.** En la frase, 0.4494 en 10 000 pasos frente a 0.4490. En el *Quijote*, 0.46434 en 100 000 pasos frente a ${\mu(V)\approx0.46439}$. Con dos clases cerradas, la fracción a ${T=1000}$ depende de la réplica (en las cinco, 0 o 0.998), y su límite es aleatorio: 0 o 1.
- **El alcance.** Simular con la misma $\widehat P$ comprueba el procedimiento; no valida el modelo del idioma.
- **Lo que no generaliza.** Con dos estados el ritmo es un solo número, ${\lvert\lambda\rvert}$. Con $k$ estados, la distancia no se multiplica por lo mismo en cada paso, y el teorema no dice cuántos pasos.

Continúa con [[mkv-absorcion|Cuánto falta para terminar]].
