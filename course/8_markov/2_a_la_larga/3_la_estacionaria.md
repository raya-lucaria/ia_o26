---
id: mkv-la-estacionaria
title: "La estacionaria y sus cuatro teoremas"
nav_title: "La estacionaria"
summary: "Tres preguntas sobre el largo plazo, la distribución que no cambia al dar un paso y los cuatro teoremas que dicen cuándo existe, cuándo es única, cuándo se llega a ella y cuándo mide la fracción del tiempo."
status: ready
estimated_time: 39m
tags: [markov, estacionaria, convergencia, ergodico]
---

# La estacionaria y sus cuatro teoremas

**¿Qué distribución deja quieta a la cadena, y cuándo describe lo que pasa a la larga?**

Al terminar tendrás:

- **Tres preguntas separadas:** en el paso $t$, en el límite y en fracción del tiempo.
- **Una definición:** la distribución estacionaria, $\mu P=\mu$, y cómo se calcula con un sistema lineal.
- **Cuatro teoremas con su condición exacta:** existe, es única, se llega a ella, mide el tiempo.
- **Un contraejemplo por teorema:** una cadena pequeña que muestra qué se rompe sin la condición.
- **Una tabla para consultar** las cuatro condiciones de un vistazo.

## Lo que traes

De [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]:

- **Sistema lineal:** puede tener una, ninguna o infinitas soluciones (@mkv-c2-def-sistema).
- **Límite de una sucesión de vectores:** la distancia $\lVert\mu_t-\nu\rVert_1$ tiende a cero (@mkv-c2-def-limite).
- **Alcanzar:** hay un camino de flechas positivas de $s$ a $s'$ (@mkv-c2-def-alcanzar).
- **Dos estados:** con $a=P_{12}$, $b=P_{21}$ y $a+b>0$, la fila fija es $igl(b/(a+b),\ a/(a+b)igr)$; en la frase, $(22/49,\ 27/49)$ (sección 1 de esa página).

De [[mkv-clasificar-estados|Clasificar los estados]]:

- **Clases:** los estados que se comunican forman una clase (@mkv-c2-def-comunican).
- **Clase cerrada:** de ella no sale ninguna flecha (@mkv-c2-def-clase-cerrada).
- **Transitorio:** un estado al que la cadena puede no regresar (@mkv-c2-def-transitorio); en cadenas finitas, recurrente equivale a estar en una clase cerrada (@mkv-c2-teo-recurrente-cerrada).
- **Periodo:** $d(s)$, el máximo común divisor de los pasos en que se puede regresar a $s$ (@mkv-c2-def-periodo); toda la clase lo comparte (@mkv-c2-cl-teo-periodo-clase).
- **Siempre hay dónde quedarse:** toda cadena finita tiene una clase cerrada (@mkv-c2-cl-teo-hay-cerrada).

De la clase 1: $\mu_{t+1}=\mu_tP$ (@mkv-c1-teo-predecir) y la ley de los grandes números para repeticiones independientes (@mkv-c1-teo-promedio).

De [[de-donde-sale-el-bono|De dónde sale el bono]], en la unidad de juegos: la cota de Hoeffding (@jue-c3-teo-hoeffding), el margen de error del promedio de repeticiones **independientes**.

**Página formal:** todo se enuncia para una cadena de $k$ estados. Los juguetes son de dos o tres estados, con ceros y unos, para seguirlos a mano.

---

## 1 · Separar tres preguntas

**Piensa: ¿qué significa «qué pasa a la larga» con una cadena?**

Significa tres cosas distintas, y pueden tener respuestas distintas. Sea $N_T(s)$ el número de visitas a $s$ en los pasos ${0,\dots,T-1}$ de una trayectoria.

$$
\begin{aligned}
&\text{En el paso }t:&&\mu_t(s)=\Pr(S_t=s),\\
&\text{En el límite:}&&\lim_{t\to\infty}\mu_t,\\
&\text{Fracción del tiempo:}&&\frac{N_T(s)}{T},\quad T\to\infty.
\end{aligned}
$$

- **En el paso $t$:** un número fijo para cada $t$; lo calcula $\mu_0P^t$ sin azar.
- **En el límite:** un vector fijo, si existe; alternar entre dos vectores distintos impide tener límite (@mkv-c2-def-limite).
- **Fracción del tiempo:** cuenta sobre **una** trayectoria, así que es aleatoria. Su límite, si existe, puede seguir siendo aleatorio.

**En el juguete.** La cadena que alterna, con estados A y B, siempre cambia de estado. Empieza en A.

$$
\begin{aligned}
P&=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad \mu_0=(1,0),\\
\mu_t&=\begin{cases}(1,0),&t\text{ par},\\(0,1),&t\text{ impar},\end{cases}\\
\frac{N_T(A)}{T}&=\frac{\lceil T/2\rceil}{T}\longrightarrow\frac12.
\end{aligned}
$$

- **En el paso $t$:** 1 o 0, según la paridad.
- **En el límite:** no existe; $\mu_t$ salta entre dos vectores.
- **Fracción del tiempo:** tiende a $1/2$, sin azar, porque la trayectoria es A, B, A, B, …
- **El techo:** $\lceil x\rceil$ es el menor entero mayor o igual que $x$. Aquí cuenta los pasos pares entre $0$ y $T-1$, incluido el inicial: con $T=5$, A está en $0,2,4$ y $\lceil5/2\rceil=3$.

La figura dibuja tres de los cuatro contraejemplos de la página, los que se usan en las secciones 4 a 6. El cuarto, $i\to i+1$, tiene infinitos estados y aparece en la sección 3.

::: figure {#mkv-c2-fig-contraejemplos title="Tres cadenas pequeñas que rompen algo"}
![Tres cadenas apiladas, cada una con lo que cumple y lo que rompe. Primera, alternante: A va a B con 1 y B a A con 1; una clase cerrada de periodo 2. Sí: μ = (1/2, 1/2) es única y la fracción del tiempo tiende a 1/2. No: desde A, μₜ alterna 1, 0, 1 y no converge; lo rompe el periodo 2. Segunda, identidad: s1 y s2 se quedan con 1; dos clases cerradas. Sí: μₜ converge, porque nunca cambia. No: toda distribución es estacionaria y cada inicio se queda con su límite. Tercera: s1 se queda con 1/2 y va a s2 con 1/4 y a s3 con 1/4; s2 y s3 se quedan con 1; s1 es transitorio (marco punteado). Sí: μₜ converge, a un límite que depende del inicio; desde s1, a (0, 1/2, 1/2). No: (0, p, 1 − p) es estacionaria para todo p, y una sola trayectoria pasa 1 o 0 del tiempo en s2, nunca 1/2.](../_assets/mkv-c2-grafo-contraejemplos.svg)
:::

**Qué rompe cada una.** Las tres contestan distinto a las tres preguntas:

- **Alternante, una clase cerrada de periodo 2.** $\mu$ es única y la fracción del tiempo tiende a ½. Pero desde A, $\mu_t$ alterna 1, 0, 1, … sin límite. Rompe la **convergencia**: a la clase le falta ser aperiódica.
- **Identidad, dos clases cerradas.** $\mu_t$ converge, porque nunca cambia, pero toda distribución es estacionaria. Rompe la **unicidad**: cada inicio se queda con su límite.
- **Transitorio entre dos cerradas.** $\mu_t$ converge, pero a un límite que depende del inicio; desde $s_1$, a $(0,\tfrac12,\tfrac12)$. Rompe la **unicidad** y el **ergódico**: muchas réplicas en un mismo paso dan ½ en $s_2$, pero una sola trayectoria pasa ahí 1 o 0 del tiempo.
- **Si conectas $s_2$ y $s_3$** con lazos (cada uno se queda con ½ y pasa al otro con ½), queda una sola clase cerrada aperiódica. Se cumplen los cuatro teoremas: $\mu=(0,\tfrac12,\tfrac12)$ es única, $\mu_t$ llega a ella desde cualquier inicio y cada trayectoria pasa la mitad del tiempo en cada una.


::: exercise {#mkv-c2-es-ej-tres-preguntas title="Responde las tres preguntas en la identidad"}
En la cadena identidad de la figura, ${P=I_2}$, empieza con $\mu_0=(1/2,1/2)$. Da $\mu_t$, su límite y los valores posibles de $N_T(s_1)/T$.
:::

::: hint {#mkv-c2-es-pista-tres-preguntas of="mkv-c2-es-ej-tres-preguntas" title="¿Se mueve alguna vez la trayectoria?"}
Una vez sorteado $S_0$, ¿qué estados visita la cadena después?
:::

::: answer {#mkv-c2-es-resp-tres-preguntas of="mkv-c2-es-ej-tres-preguntas"}
- **En el paso $t$:** $\mu_t=\mu_0I_2^t=(1/2,1/2)$ para todo $t$.
- **En el límite:** $(1/2,1/2)$.
- **Fracción del tiempo:** la trayectoria se queda en $S_0$. Vale 1 con probabilidad $1/2$ y 0 con probabilidad $1/2$; nunca $1/2$.

El límite de $\mu_t$ existe y aun así no coincide con la fracción del tiempo de ninguna trayectoria.
:::

Las tres preguntas se separan. ¿Hay alguna distribución que las ponga de acuerdo?

---

## 2 · Definir la estacionaria: μP = μ

**Piensa: si $\mu_t$ tiene límite, ¿qué ecuación cumple ese límite?**

La de un punto fijo: dar un paso no lo cambia. A esa distribución se le llama estacionaria.

::: definition {#mkv-c2-def-estacionaria title="Distribución estacionaria"}
Para una cadena con matriz $P\in\mathbb R^{k\times k}$:

$$
\begin{aligned}
&\mu\in\mathbb R^{1\times k},\\
&\mu P=\mu,\qquad \mu\mathbf 1=1,\qquad \mu(s)\ge0.
\end{aligned}
$$

- **Qué es:** una distribución sobre los estados que no cambia al multiplicarla por $P$.
- **Cómo se calcula:** resolviendo el sistema lineal $\mu(P-I_k)=\mathbf 0$ con la ecuación $\mu\mathbf 1=1$ en lugar de una de las $k$ ecuaciones, que es redundante (@mkv-c2-def-sistema), y conservando solo las soluciones sin entradas negativas. En la identidad $I_2$, $(2,-1)$ cumple el sistema y no es una distribución.
- **Qué significa:** si $\mu_0=\mu$, entonces $\mu_t=\mu$ en todo paso. Arrancas en ella y te quedas en ella.
- **Qué no es:** un estado donde la cadena se detiene. La trayectoria sigue saltando; lo que no cambia son las probabilidades.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $s_1\xrightarrow{1/2}s_2$, $s_2\xrightarrow{1}s_1$, lazo $s_1\xrightarrow{1/2}s_1$, con $\mu=(2/3,1/3)$. Matriz: $P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}$. $\mu P=(\tfrac23\cdot\tfrac12+\tfrac13\cdot1,\ \tfrac23\cdot\tfrac12)=(2/3,1/3)=\mu$; suma 1, sin negativos.
> - **No lo cumple:** la misma cadena, $s_1\xrightarrow{1/2}s_2$, $s_2\xrightarrow{1}s_1$, lazo $s_1\xrightarrow{1/2}s_1$, con $\mu=(1/2,1/2)$. Matriz: $P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}$. $\mu P=(\tfrac14+\tfrac12,\ \tfrac14)=(3/4,1/4)\neq\mu$: es distribución, pero un paso la cambia.

- **Por qué te quedas:** por inducción con @mkv-c1-teo-predecir, $\mu_{t+1}=\mu_tP=\mu P=\mu$.
- **Por qué sobra una ecuación:** cada fila de $P-I_k$ suma cero, ${(P-I_k)\mathbf 1=\mathbf 0}$. Las $k$ columnas del sistema son dependientes.
- **Aviso de letras:** en libros de cadenas verás $\pi$ para la estacionaria. Aquí $\pi$ queda para la política de un agente, como en la unidad de agentes.

::: theorem {#mkv-c2-es-teo-limite title="Si la distribución tiene límite, ese límite es estacionario"}
**Condición.** Cadena finita; para cierto $\mu_0$, la sucesión $\mu_t=\mu_0P^t$ tiene límite $\nu$.

$$
\nu P=\nu,\qquad \nu\mathbf 1=1,\qquad \nu(s)\ge0.
$$

**Lectura.** Si la cadena se asienta, se asienta en una estacionaria.

**Casos nulos.** Si $\mu_t$ no tiene límite, como en la cadena que alterna desde A, el teorema no dice nada.
:::

::: proof {#mkv-c2-es-dem-limite of="mkv-c2-es-teo-limite"}
La sucesión recorrida desde un paso después, $\mu_{t+1}$, tiene el mismo límite $\nu$. Cada entrada de $\mu_tP$ es una suma **finita** de $k$ términos:

$$
\begin{aligned}
\nu(s_j)&=\lim_{t\to\infty}\mu_{t+1}(s_j)\\
&=\lim_{t\to\infty}\sum_{i=1}^k\mu_t(s_i)P_{ij}\\
&=\sum_{i=1}^k\nu(s_i)P_{ij}.
\end{aligned}
$$

- **No negativa:** cada $\nu(s)$ es límite de números $\ge0$.
- **Suma uno:** $\nu\mathbf 1=\lim\mu_t\mathbf 1=1$, otra vez porque la suma es finita.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** lazo $s_1\xrightarrow{1/2}s_1$, $s_1\xrightarrow{1/2}s_2$, $s_2\xrightarrow{1}s_1$. Matriz: $P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}$. Desde $s_1$, $\mu_t\to\nu=(2/3,1/3)$, y $\nu P=\nu$: el límite es estacionario.
> - **No lo cumple:** $A\xrightarrow{1}B$, $B\xrightarrow{1}A$. Matriz: $P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$. Desde A, $\mu_t$ alterna $(1,0),(0,1),\dots$ sin límite; el teorema no dice nada.

- **Dónde se usa que es finita:** con infinitos estados, la suma de los límites puede perder masa. En ${\{0,1,2,\dots\}}$ con $i\to i+1$, $\mu_t=\mathbf e_t$ tiende a cero entrada por entrada, y el vector cero no es una distribución.

**Dos estados, ya resuelto.** El sistema de dos estados se resolvió en la sección 1 de [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]: con $a=P_{12}$, $b=P_{21}$ y $a+b>0$, la única estacionaria es $\bigl(b/(a+b),\ a/(a+b)\bigr)$. Su primera ecuación se lee como un balance:

$$
\mu(s_1)\,a=\mu(s_2)\,b.
$$

- **Lectura de la ecuación:** la probabilidad que sale de $s_1$ en un paso es igual a la que entra.

**En el juguete.** En la frase, $a=P_{VC}=9/11$ y $b=P_{CV}=2/3$ dan $\mu=(22/49,\ 27/49)$. Comprueba el balance: $\tfrac{22}{49}\cdot\tfrac{9}{11}=\tfrac{18}{49}=\tfrac{27}{49}\cdot\tfrac23$.

- **Lectura:** $\mu(V)=22/49\approx0.449$, el número al que se acercaban las dos sucesiones de [[tarea-que-es-una-cadena|la tarea de la clase 1]].
- **La cadena que alterna:** $a=b=1$ da $\mu=(1/2,1/2)$.

> [!WARNING]
> **Error típico:** «en la estacionaria la cadena se queda quieta». **Lo que se queda quieto es la distribución, no el estado:** con $\mu=(1/2,1/2)$, la cadena que alterna sigue saltando en cada paso.

::: exercise {#mkv-c2-es-ej-a-cero title="Usa la fórmula donde se rompe"}
En el ejemplo de dos estados, toma $a=b=0$. ¿Qué matriz es? ¿Qué distribuciones cumplen $\mu P=\mu$?
:::

::: hint {#mkv-c2-es-pista-a-cero of="mkv-c2-es-ej-a-cero" title="¿Qué le pasa al denominador?"}
¿Puedes dividir entre $a+b$? Si no, regresa a la ecuación $\mu(s_1)a=\mu(s_2)b$.
:::

::: answer {#mkv-c2-es-resp-a-cero of="mkv-c2-es-ej-a-cero"}
Es la identidad $I_2$. La ecuación queda $0=0$ y solo sobrevive $\mu\mathbf 1=1$: **toda** distribución $(c,1-c)$, con $0\le c\le1$, es estacionaria. El sistema tiene infinitas soluciones.
:::

La identidad tiene infinitas estacionarias, y la frase una sola. ¿Siempre hay al menos una?

---

## 3 · Existe: basta que la cadena sea finita

**Piensa: ¿puede una cadena no tener ninguna estacionaria?**

Sí, si tiene infinitos estados. Con finitos, siempre hay al menos una.

::: theorem {#mkv-c2-teo-existe title="Existencia de una estacionaria"}
**Condición.** La cadena es finita: $k=\lvert\mathcal S\rvert<\infty$.

$$
\exists\,\mu\in\mathbb R^{1\times k}:\quad
\mu P=\mu,\quad\mu\mathbf 1=1,\quad\mu\ge0.
$$

**Lectura.** Toda matriz de transición finita deja quieta al menos una distribución.

**Casos nulos.** El teorema no dice cuántas hay ni que $\mu_t$ llegue a alguna.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $s_1\xrightarrow{1/2}s_2$, $s_2\xrightarrow{1}s_1$, lazo $s_1\xrightarrow{1/2}s_1$. Matriz: $P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}$. Es finita (dos estados) y $\mu=(\tfrac23,\tfrac13)$ cumple $\mu P=\mu$, $\mu\mathbf 1=1$.
> - **No lo cumple:** $0\xrightarrow{1}1$, $1\xrightarrow{1}2$, $2\xrightarrow{1}3$, $\dots$ Matriz: $P=\begin{pmatrix}0&1&0&0&\cdots\\0&0&1&0&\cdots\\0&0&0&1&\cdots\\\vdots&&&&\ddots\end{pmatrix}$. Infinitos estados: $\mu P=\mu$ obliga $\mu(0)=0$ y $\mu(i+1)=\mu(i)$, así que $\mu=\mathbf 0$.

**De dónde sale.** No lo demostramos; se arma en tres piezas.

- **Hay una clase cerrada:** es @mkv-c2-cl-teo-hay-cerrada. Su prueba da algo más: desde cualquier estado, siguiendo flechas, se llega a una clase cerrada.
- **Dentro de esa clase:** la matriz restringida a ella es de transición y todos sus estados se comunican. Para esas matrices, el teorema de Frobenius (1912) da una estacionaria positiva. Esta es la pieza que se cita.
- **Fuera de ella:** pon $\mu(s)=0$. Como de la clase no sale nada, $\mu P=\mu$ se sigue cumpliendo.

**Contraejemplo: infinitos estados.** En ${\mathcal S=\{0,1,2,\dots\}}$, con $P_{i,i+1}=1$, la cadena avanza un lugar en cada paso.

$$
\begin{aligned}
(\mu P)(0)&=0\ \Longrightarrow\ \mu(0)=0,\\
(\mu P)(i+1)&=\mu(i)\ \Longrightarrow\ \mu(i+1)=\mu(i),\\
&\Longrightarrow\ \mu=\mathbf 0,\ \ \mu\mathbf 1=0\ne1.
\end{aligned}
$$

- **Qué se rompe:** la probabilidad se escapa hacia estados cada vez más lejanos y no queda en ningún lado.

**En el juguete.** La frase, la cadena que alterna, la identidad y la de dos clases cerradas son finitas: todas tienen al menos una estacionaria.

::: exercise {#mkv-c2-es-ej-infinita-con title="Encuentra una infinita que sí tenga"}
En ${\{0,1,2,\dots\}}$, cada estado va a $0$ con probabilidad 1. ¿Tiene estacionaria? ¿Qué dice eso de la condición de finitud?
:::

::: hint {#mkv-c2-es-pista-infinita-con of="mkv-c2-es-ej-infinita-con" title="¿Dónde está la cadena después del primer paso?"}
Prueba con una distribución que ponga toda la probabilidad en un solo estado.
:::

::: answer {#mkv-c2-es-resp-infinita-con of="mkv-c2-es-ej-infinita-con"}
**Sí:** $\mu=\mathbf e_0$. Llega a $0$ toda la probabilidad, $(\mu P)(0)=\sum_i\mu(i)=1$, y a ningún otro estado. La finitud es **suficiente, no necesaria**: hay cadenas infinitas con estacionaria.
:::

Ya sabemos que hay al menos una. La identidad mostró que puede haber muchas: ¿cuándo hay solo una?

---

## 4 · Única: una sola clase cerrada

**Piensa: ¿qué tiene la identidad que no tiene la frase?**

Dos clases cerradas, $\{s_1\}$ y $\{s_2\}$. Cada clase cerrada aporta su propia estacionaria, y cualquier mezcla de ellas también lo es.

::: theorem {#mkv-c2-teo-unica title="Unicidad: una sola clase cerrada"}
**Condición.** Cadena finita con clases cerradas $\mathcal C_1,\dots,\mathcal C_r$, $r\ge1$.

1. Toda estacionaria vale $0$ fuera de ${\mathcal C_1\cup\dots\cup\mathcal C_r}$.
2. Cada $\mathcal C_i$ tiene exactamente una estacionaria $\mu^{(i)}$ que vale $0$ fuera de $\mathcal C_i$; es positiva en todo $\mathcal C_i$.
3. Las estacionarias son exactamente las mezclas:

$$
\begin{aligned}
\mu&=\lambda_1\mu^{(1)}+\dots+\lambda_r\mu^{(r)},\\
\lambda_i&\ge0,\qquad \lambda_1+\dots+\lambda_r=1.
\end{aligned}
$$

**Lectura.** La estacionaria es única **si y solo si** hay una sola clase cerrada, $r=1$.

**Casos nulos.** Con $r\ge2$ hay infinitas, una por cada elección de los pesos $\lambda_i$.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $s_1\xrightarrow{1}s_2$, $s_2\xrightarrow{1/2}s_1$, lazo $s_2\xrightarrow{1/2}s_2$, $s_3\xrightarrow{1/2}s_1$, lazo $s_3\xrightarrow{1/2}s_3$. Matriz: $P=\begin{pmatrix}0&1&0\\1/2&1/2&0\\1/2&0&1/2\end{pmatrix}$. Una sola clase cerrada, $\{s_1,s_2\}$: única estacionaria $\mu=(1/3,\,2/3,\,0)$, cero en el transitorio $s_3$.
> - **No lo cumple:** lazos $s_1\xrightarrow{1}s_1$, $s_2\xrightarrow{1}s_2$; $s_3\xrightarrow{1/2}s_1$, $s_3\xrightarrow{1/2}s_2$. Matriz: $P=\begin{pmatrix}1&0&0\\0&1&0\\1/2&1/2&0\end{pmatrix}$. Dos clases cerradas, $r=2$: toda mezcla $(\lambda,\,1-\lambda,\,0)$ es estacionaria; hay infinitas.

- **Transitorios:** el punto 1 dice que ninguna estacionaria pone probabilidad en un estado transitorio, haya una o muchas.
- **Lo que se cita:** el punto 2 es otra vez Frobenius, dentro de cada clase. El punto 3 sale de 1 y 2; la prueba lo arma.

::: proof {#mkv-c2-es-dem-unica of="mkv-c2-teo-unica"}
**Punto 1.** Sea $\mathcal U$ el conjunto de estados fuera de las clases cerradas. Si $\mathcal U=\varnothing$, el punto 1 es inmediato; supón $\mathcal U\ne\varnothing$. Desde cada $s\in\mathcal U$ se alcanza alguna clase cerrada (la prueba de @mkv-c2-cl-teo-hay-cerrada) por un camino de menos de $k$ pasos, y ya no se sale. Entonces, con $\Pr_s$ la probabilidad empezando en $s$:

$$
\eta=\min_{s\in\mathcal U}\Pr_s(S_k\notin\mathcal U)>0.
$$

Arranca en una estacionaria $\mu$; entonces $\mu_k=\mu$. Escribimos $\mu(\mathcal U)=\sum_{s\in\mathcal U}\mu(s)$, la probabilidad total que $\mu$ pone en el conjunto $\mathcal U$. Desde una clase cerrada no se vuelve a $\mathcal U$:

$$
\begin{aligned}
\mu(\mathcal U)&=\Pr(S_k\in\mathcal U)\\
&=\sum_{s\in\mathcal U}\mu(s)\Pr_s(S_k\in\mathcal U)\\
&\le(1-\eta)\,\mu(\mathcal U).
\end{aligned}
$$

Como $\eta>0$, queda $\mu(\mathcal U)=0$.

**Dos clases cerradas dan infinitas.** Si $\mu^{(1)}P=\mu^{(1)}$ y $\mu^{(2)}P=\mu^{(2)}$, para $0\le\lambda\le1$:

$$
\begin{aligned}
&\bigl(\lambda\mu^{(1)}+(1-\lambda)\mu^{(2)}\bigr)P\\
&\quad=\lambda\mu^{(1)}+(1-\lambda)\mu^{(2)}.
\end{aligned}
$$

La mezcla es no negativa y suma uno. Como $\mu^{(1)}\ne\mu^{(2)}$ (viven en clases distintas), cada $\lambda$ da una distinta.

**Toda estacionaria es una mezcla.** Sea $\mu$ estacionaria y $s\in\mathcal C_i$. En $(\mu P)(s)=\sum_j\mu(j)P_{js}$ solo cuentan los $j\in\mathcal C_i$: fuera de las clases cerradas $\mu(j)=0$ (punto 1), y desde otra clase cerrada $P_{js}=0$. Así, $\mu$ restringida a $\mathcal C_i$ queda quieta bajo la matriz de $\mathcal C_i$, y por el punto 2 es $\lambda_i\mu^{(i)}$ con $\lambda_i=\mu(\mathcal C_i)\ge0$. Por el punto 1, $\lambda_1+\dots+\lambda_r=1$.
:::

**Contraejemplo: la identidad.** Clases cerradas $\{s_1\}$ y $\{s_2\}$, con $\mu^{(1)}=(1,0)$ y $\mu^{(2)}=(0,1)$. Las mezclas son todas las $(c,1-c)$, como en el ejercicio de la sección 2.

**Contraejemplo: dos clases cerradas con un transitorio.** Es la cadena de abajo en @mkv-c2-fig-contraejemplos.

$$
\begin{aligned}
P&=\begin{pmatrix}1/2&1/4&1/4\\0&1&0\\0&0&1\end{pmatrix},\\
\mu&=(0,\ c,\ 1-c),\qquad 0\le c\le1.
\end{aligned}
$$

- **Transitorio:** $s_1$ pierde probabilidad y nadie se la devuelve; por eso $\mu(s_1)=0$.
- **Clases cerradas:** $\{s_2\}$ y $\{s_3\}$, cada una absorbente; de ahí las infinitas.

**En el juguete.** En la frase, V y C se comunican: una sola clase, cerrada. La estacionaria $(22/49,27/49)$ es la única. La cadena que alterna también tiene una sola clase cerrada: $(1/2,1/2)$ es única aunque sea periódica.

> [!WARNING]
> **Error típico:** «la estacionaria es única solo si todos los estados se comunican». **Basta una sola clase cerrada; los transitorios no estorban.** Que todo se comunique es suficiente, no necesario.

::: exercise {#mkv-c2-es-ej-quitar-clase title="Quita una clase cerrada"}
En la cadena de dos clases cerradas, cambia la fila de $s_3$ por $(0,1,0)$. ¿Cuántas clases cerradas quedan? ¿Cuál es la estacionaria?
:::

::: hint {#mkv-c2-es-pista-quitar-clase of="mkv-c2-es-ej-quitar-clase" title="¿Desde dónde se sale ahora?"}
¿Sigue siendo cerrada $\{s_3\}$? ¿Qué estados quedan fuera de toda clase cerrada?
:::

::: answer {#mkv-c2-es-resp-quitar-clase of="mkv-c2-es-ej-quitar-clase"}
Ahora $s_3$ va a $s_2$: $\{s_3\}$ deja de ser cerrada y $s_1$, $s_3$ son transitorios. Queda una sola clase cerrada, $\{s_2\}$. Por @mkv-c2-teo-unica la estacionaria es única: $\mu=(0,1,0)$. Comprueba: $(0,1,0)P$ es la fila de $s_2$.
:::

Única no quiere decir que la cadena llegue a ella. La cadena que alterna tiene una sola estacionaria y, desde A, nunca se asienta.

---

## 5 · Converge: una clase cerrada y aperiódica

**Piensa: ¿qué le falta a la cadena que alterna para olvidar dónde empezó?**

Poder romper el ritmo. Su clase cerrada tiene periodo 2: solo se regresa a A en pasos pares.

::: theorem {#mkv-c2-teo-converge title="Convergencia desde cualquier inicio"}
**Condición.** Cadena finita con **una sola clase cerrada** $\mathcal C$, y $\mathcal C$ **aperiódica**: $d(s)=1$ para un $s\in\mathcal C$, y entonces para todos los de $\mathcal C$ (@mkv-c2-cl-teo-periodo-clase).

$$
\lim_{t\to\infty}\mu_0P^t=\mu
\quad\text{para todo }\mu_0,
$$

donde $\mu$ es la única estacionaria de @mkv-c2-teo-unica. Equivale a que cada fila de $P^t$ tienda a $\mu$.

**Lectura.** Desde donde sea que empiece, la cadena olvida su inicio: $\mu_t$ se acerca a $\mu$. La condición es **necesaria y suficiente** para que $\mu_0P^t$ tienda a una misma $\mu$ desde todo $\mu_0$.

**Casos nulos.** Los transitorios pueden tener cualquier periodo; solo cuenta el de la clase cerrada.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $s_1\xrightarrow{1/2}s_2$, $s_2\xrightarrow{1}s_1$, lazo $s_1\xrightarrow{1/2}s_1$. Matriz: $P=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}$. Una clase cerrada; el lazo da $d(s_1)=1$. Desde $s_1$ o $s_2$, $\mu_t\to\mu=(2/3,1/3)$.
> - **No lo cumple:** $s_1\xrightarrow{1}s_2$, $s_2\xrightarrow{1/2}s_1$, $s_2\xrightarrow{1/2}s_3$, $s_3\xrightarrow{1}s_2$. Matriz: $P=\begin{pmatrix}0&1&0\\1/2&0&1/2\\0&1&0\end{pmatrix}$. Periodo 2: desde $s_1$, $\mu_t$ alterna entre $(0,1,0)$ y $(1/2,0,1/2)$; nunca llega a $\mu=(1/4,1/2,1/4)$.

- **Prueba:** no la damos aquí; usa la aperiodicidad para que alguna potencia de $P$ tenga una columna, de un estado de $\mathcal C$, con todas sus entradas positivas.
- **Necesaria y suficiente desde todo inicio:** la observación siguiente muestra que ninguna condición sobra. Desde un inicio **particular**, en cambio, se puede converger sin ella: la cadena que alterna, desde $(1/2,1/2)$, ya está en su estacionaria y no se mueve.

::: remark {#mkv-c2-es-obs-no-sobra title="Ninguna de las dos condiciones sobra"}
Si falla cualquiera, hay algún inicio desde el que $\mu_t$ no tiende a $\mu$:

- **Dos clases cerradas:** arrancar en $\mu^{(1)}$ deja $\mu_t=\mu^{(1)}$, y arrancar en $\mu^{(2)}$ deja $\mu_t=\mu^{(2)}$. No hay un límite común.
- **Periodo $d\ge2$:** desde $s\in\mathcal C$, $(P^t)_{ss}=0$ cuando $d$ no divide a $t$. Pero $\mu(s)>0$ (@mkv-c2-teo-unica), así que $\mu_t(s)$ no puede tender a $\mu(s)$.
:::

**Contraejemplo: la cadena que alterna, desde A.** Una sola clase cerrada, periodo 2: $\mu_t$ salta entre $(1,0)$ y $(0,1)$ sin límite (sección 1).

**En el juguete.** En la frase, $P_{VV}=2/11>0$: un lazo basta para que la clase sea aperiódica. Desde V y desde C, $\mu_t(V)$ tiende a $22/49\approx0.449$.

| $t$ | Desde V | Desde C |
|---:|---:|---:|
| 0 | 1.000 | 0.000 |
| 1 | 0.182 | 0.667 |
| 2 | 0.579 | 0.343 |
| 4 | 0.479 | 0.424 |
| 8 | 0.451 | 0.448 |

> [!WARNING]
> **Error típico:** «si la estacionaria es única, $\mu_t$ llega a ella». **Única no implica converge:** la cadena que alterna tiene una sola estacionaria y, desde A, alterna para siempre entre $(1,0)$ y $(0,1)$.

> [!WARNING]
> **Error típico:** «si todas las clases cerradas son aperiódicas, olvida su inicio». **Hace falta además que sea una sola:** en la cadena de dos clases cerradas, desde $s_1$, $\mu_t\to(0,1/2,1/2)$, y desde $s_2$, $\mu_t=(0,1,0)$. Converge, pero a límites distintos.

::: exercise {#mkv-c2-es-ej-romper-ritmo title="Rompe el ritmo con un lazo"}
Cambia la cadena que alterna a ${P=\begin{pmatrix}0&1\\1/2&1/2\end{pmatrix}}$. ¿Se cumple la condición de @mkv-c2-teo-converge? ¿A qué tiende $\mu_t$ desde A?
:::

::: hint {#mkv-c2-es-pista-romper-ritmo of="mkv-c2-es-ej-romper-ritmo" title="¿En qué pasos se puede regresar a B?"}
¿Hay algún lazo? Para el límite, ¿qué valen $a$ y $b$ en la fórmula de dos estados?
:::

::: answer {#mkv-c2-es-resp-romper-ritmo of="mkv-c2-es-ej-romper-ritmo"}
**Sí.** A y B se comunican: una sola clase, cerrada. El lazo $P_{BB}=1/2>0$ la hace aperiódica. Con $a=1$ y $b=1/2$:

$$
\mu=\left(\frac{1/2}{3/2},\ \frac{1}{3/2}\right)=\left(\frac13,\ \frac23\right).
$$

Desde A, y desde cualquier inicio, $\mu_t\to(1/3,2/3)$.
:::

Desde A, la cadena que alterna no converge. Pero su fracción del tiempo en A sí tendía a $1/2$. ¿Cuándo pasa eso?

---

## 6 · Ergódico: la fracción del tiempo

**Piensa: ¿una sola trayectoria larga basta para conocer $\mu$?**

Sí, con una sola clase cerrada, aunque sea periódica. Es el **teorema ergódico** (*ergodic theorem*).

::: theorem {#mkv-c2-teo-ergodico title="Teorema ergódico: la fracción del tiempo tiende a la estacionaria"}
**Condición.** Cadena finita con **una sola clase cerrada**; puede ser periódica. Sea $\mu$ su única estacionaria.

$$
\begin{aligned}
&\Pr\!\left(\lim_{T\to\infty}\frac{N_T(s)}{T}=\mu(s)\right)=1\\
&\quad\text{para todo }s\in\mathcal S\text{ y todo }\mu_0.
\end{aligned}
$$

**Lectura.** Con probabilidad 1, la fracción del tiempo que una trayectoria pasa en $s$ tiende a $\mu(s)$, empiece donde empiece. Una sola clase cerrada es **necesaria y suficiente** para que haya ese mismo límite $\mu(s)$ desde todo inicio.

**Casos nulos.** Si $s$ es transitorio, $\mu(s)=0$: la trayectoria lo visita un número finito de veces.
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** la alternante, $A\xrightarrow{1}B$, $B\xrightarrow{1}A$. Matriz: $P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$. Una sola clase cerrada, periódica con $d(A)=2$; aun así $N_T(A)/T\to1/2=\mu(A)$ desde cualquier inicio.
> - **No lo cumple:** lazo $s_1\xrightarrow{1/2}s_1$, $s_1\xrightarrow{1/4}s_2$, $s_1\xrightarrow{1/4}s_3$, lazos $s_2\xrightarrow{1}s_2$, $s_3\xrightarrow{1}s_3$. Matriz: $P=\begin{pmatrix}1/2&1/4&1/4\\0&1&0\\0&0&1\end{pmatrix}$. Dos clases cerradas: desde $s_1$, $N_T(s_2)/T$ tiende a 1 o a 0, cada uno con probabilidad $1/2$.

- **Prueba:** no la damos. La idea: la trayectoria entra a la clase cerrada en un tiempo finito y, dentro, los regresos a $s$ se repiten como ciclos independientes.
- **Necesaria y suficiente desde todo inicio:** con dos clases cerradas, empezar dentro de cada una da límites distintos, y empezar en un transitorio puede dar un límite aleatorio, como en el contraejemplo.

**Contraejemplo: dos clases cerradas con un transitorio.** Empieza en $s_1$. Cuando sale, cae en $s_2$ o en $s_3$, cada uno con probabilidad $1/2$, y se queda.

$$
\lim_{T\to\infty}\frac{N_T(s_2)}{T}=
\begin{cases}
1,&\text{si cae en }s_2,\\
0,&\text{si cae en }s_3.
\end{cases}
$$

- **Qué se rompe:** el límite existe, pero es **aleatorio**. Ningún número fijo $\mu(s_2)$ lo describe.

**En el juguete.** La cadena que alterna es periódica y aun así cumple el teorema: $N_T(A)/T\to1/2=\mu(A)$. En la frase, la fracción del tiempo en V tiende a $22/49$.

> [!WARNING]
> **Error típico:** «las visitas de una trayectoria son una muestra; aplica Hoeffding». **Las visitas dependen unas de otras:** @jue-c3-teo-hoeffding y @mkv-c1-teo-promedio piden repeticiones independientes. El teorema ergódico es la ley de los grandes números para cadenas, y no trae el margen de error de Hoeffding.

**Un poco de historia.** Si la ley de los grandes números vale sin independencia es la pregunta de [[mkv-el-problema-de-markov|El problema de Markov]]. Nekrásov sostenía que la ley de los grandes números necesitaba independencia. Markov (1906) la demostró para variables dependientes encadenadas, en cadenas finitas y homogéneas. El teorema ergódico tal como lo enunciamos es una síntesis posterior, de los años treinta (Kolmogorov, Doeblin); no sale de un solo artículo.

**El nombre viene de otro lado.** Los teoremas ergódicos generales son de Birkhoff (1931, el *puntual*) y von Neumann (1932, el *medio*).

- **Qué dicen:** en un sistema que se mueve sin crear ni destruir probabilidad, el promedio en el tiempo de una cantidad iguala su promedio sobre los estados.
- **Dónde entra la cadena:** si arranca en $\mu$ y tiene una sola clase cerrada, correr la trayectoria un paso no cambia ninguna probabilidad.
- **El caso nuestro:** con la cantidad «estar en $s$», el promedio en el tiempo es $N_T(s)/T$ y el de los estados, $\mu(s)$. @mkv-c2-teo-ergodico es ese caso, probado desde cualquier inicio.

::: exercise {#mkv-c2-es-ej-entrada-periodica title="Visita una cadena con entrada"}
Tres estados: $s_1\to s_2$ con probabilidad 1, y $s_2$, $s_3$ alternan. Empieza en $s_1$. ¿A qué tiende $N_T(s_1)/T$? ¿Y $N_T(s_2)/T$? ¿Converge $\mu_t$?
:::

::: hint {#mkv-c2-es-pista-entrada-periodica of="mkv-c2-es-ej-entrada-periodica" title="¿Cuántas veces se visita s₁?"}
¿Cuáles son las clases y cuál es cerrada? ¿Qué periodo tiene?
:::

::: answer {#mkv-c2-es-resp-entrada-periodica of="mkv-c2-es-ej-entrada-periodica"}
- **Clases:** $\{s_1\}$ transitoria; $\{s_2,s_3\}$ cerrada, de periodo 2. La estacionaria única es $(0,1/2,1/2)$.
- **Fracción del tiempo:** $s_1$ se visita solo en $t=0$, así que $N_T(s_1)/T=1/T\to0$; y $N_T(s_2)/T\to1/2$.
- **En el límite:** no. La trayectoria es $s_1,s_2,s_3,s_2,\dots$ sin azar, y $\mu_t(s_2)$ alterna entre 1 y 0.
:::

Ya están los cuatro. Conviene verlos juntos, con su condición y su contraejemplo.

---

## 7 · Reunir los cuatro teoremas

**Piensa: ¿qué condición pide cada uno?**

Cada teorema pide un poco más que el anterior, salvo el ergódico, que no pide aperiodicidad.

::: table {#mkv-c2-tabla-cuatro title="Los cuatro teoremas, en cadenas finitas"}
| Resultado | Condición | Contraejemplo |
|---|---|---|
| Existe | Cadena finita (basta) | $i\to i+1$ |
| Es única | Una clase cerrada (si y solo si) | Identidad |
| Converge a $\mu$ desde todo inicio | Una clase cerrada y aperiódica (si y solo si) | Alterna, desde A |
| Fracción del tiempo $\to\mu(s)$ | Una clase cerrada, aunque sea periódica (si y solo si) | Dos clases cerradas |
:::

- **Contraejemplos:** $i\to i+1$ en $\{0,1,2,\dots\}$, ninguna; identidad, varias; alterna desde A, sin límite; dos clases cerradas, límite aleatorio.
- **Fuera de las clases cerradas:** toda estacionaria vale cero.
- **Cómo se calcula $\mu$:** con el sistema lineal de la sección 2; cuando @mkv-c2-teo-converge aplica, también multiplicando $\mu_tP$ hasta que deje de cambiar.
- **Lo que no se lee en la tabla:** la convergencia y el ergódico responden preguntas distintas. La cadena que alterna cumple el cuarto renglón y no el tercero.

---

## Ejercicios

::: exercise {#mkv-c2-es-ej-cinco-estados title="Una cadena que rompe tres teoremas a la vez"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Usa la cadena de cinco estados de [[mkv-clasificar-estados|Clasificar los estados]]: $s_1$ va a $s_2$ o a $s_4$, con $1/2$ cada uno; $s_2$ y $s_3$ alternan; $s_4$ se queda con $1/2$ o va a $s_5$; $s_5$ va a $s_4$.

**Cambia una idea:** en lugar de un contraejemplo por teorema, una sola cadena que mezcla una clase periódica, una aperiódica y un transitorio. Empieza en $s_1$.

1. **Clasifica:** ¿qué dicen @mkv-c2-teo-existe y @mkv-c2-teo-unica de esta cadena?
2. **Encuentra:** escribe todas sus estacionarias.
3. **Sigue la distribución:** ¿converge $\mu_t$? Da $\mu_t(s_2)$ para $t\ge1$.
4. **Sigue una trayectoria:** ¿qué valores puede tomar el límite de $N_T(s_4)/T$, y con qué probabilidad?
:::

::: hint {#mkv-c2-es-pista-cinco-estados-1 of="mkv-c2-es-ej-cinco-estados" title="Pista 1 · ¿Qué pasa después del primer paso?"}
Desde $s_1$, ¿en qué clase puede entrar la cadena en el primer paso? ¿Puede salir después de esa clase? ¿Qué filas de $P$ describen lo que ocurre dentro de cada una?
:::

::: hint {#mkv-c2-es-pista-cinco-estados-2 of="mkv-c2-es-ej-cinco-estados" title="Pista 2 · ¿Cumplen tus vectores las tres condiciones?"}
¿Cada vector que propones suma 1, no tiene entradas negativas y cumple $\mu P=\mu$ columna por columna? En el entregable 4, ¿tus probabilidades suman 1?
:::

::: answer {#mkv-c2-es-resp-cinco-estados of="mkv-c2-es-ej-cinco-estados" title="Respuesta · Dos cadenas pequeñas y una moneda al inicio"}
**1. Clasifica.** Es finita: existe al menos una. Clases cerradas: $\{s_2,s_3\}$, de periodo 2, y $\{s_4,s_5\}$, aperiódica por el lazo en $s_4$. Son dos, así que **no** es única. $\{s_1\}$ es transitoria.

**2. Encuentra.** En $\{s_2,s_3\}$, la que alterna: $(1/2,1/2)$. En $\{s_4,s_5\}$, con $a=1/2$ y $b=1$: $(2/3,1/3)$. Por @mkv-c2-teo-unica, todas son mezclas, con $0\le\lambda\le1$:

$$
\mu=\left(0,\ \tfrac{\lambda}{2},\ \tfrac{\lambda}{2},\ \tfrac{2(1-\lambda)}{3},\ \tfrac{1-\lambda}{3}\right).
$$

**3. Sigue la distribución.** No converge. La mitad que entra a $\{s_2,s_3\}$ alterna:

$$
\mu_t(s_2)=\begin{cases}1/2,&t\text{ impar},\\0,&t\text{ par}.\end{cases}
$$

La otra mitad sí se asienta: $\mu_t(s_4)\to\tfrac12\cdot\tfrac23=\tfrac13$.

**4. Sigue una trayectoria.** En el primer paso cae en una de las dos clases, con probabilidad $1/2$ cada una, y no sale. Dentro de cada clase aplica @mkv-c2-teo-ergodico. El límite de $N_T(s_4)/T$ vale $0$ con probabilidad $1/2$ y $2/3$ con probabilidad $1/2$: es aleatorio.

**Qué rompe.** La unicidad (dos clases cerradas), la convergencia (la clase $\{s_2,s_3\}$ es periódica) y el ergódico (el límite es aleatorio). Solo la existencia se cumple.
:::

**Punto de control:** deberías poder separar las tres preguntas, calcular una estacionaria con el sistema lineal y, para cualquier cadena finita, decir cuáles de los cuatro teoremas aplican. Revisa siempre la condición antes de usar la conclusión: cuántas clases cerradas, y de qué periodo.

---

## Lo que hay que llevarse

- **Tres preguntas:** $\mu_t$ en el paso $t$, $\lim\mu_t$ en el límite, $N_T(s)/T$ en fracción del tiempo. Pueden diferir.
- **Estacionaria:** $\mu P=\mu$, $\mu\mathbf 1=1$, $\mu\ge0$. Si $\mu_t$ tiene límite, es estacionaria.
- **Existe:** si la cadena es finita (suficiente; $i\to i+1$ no tiene).
- **Única:** si y solo si hay una sola clase cerrada. Fuera de las clases cerradas, $\mu=0$.
- **Converge a la misma $\mu$ desde todo inicio:** si y solo si hay una sola clase cerrada y es aperiódica. La que alterna, desde A, no tiene límite.
- **Ergódico:** con probabilidad 1, $N_T(s)/T\to\mu(s)$ desde todo inicio si y solo si hay una sola clase cerrada, aunque sea periódica.
- **La frase:** $\mu=(22/49,\ 27/49)$, $\mu(V)\approx0.449$; cumple los cuatro.
- **Consulta:** @mkv-c2-tabla-cuatro.

Continúa con [[mkv-olvida-su-inicio|¿Olvida su inicio?]]
