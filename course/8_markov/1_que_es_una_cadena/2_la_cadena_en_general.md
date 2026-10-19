---
id: mkv-cadena-en-general
title: "La cadena de Markov, en general"
nav_title: "La cadena, en general"
summary: "Estados, matriz de transición, distribuciones fila y potencias para describir una cadena finita y homogénea y calcular cómo se mueve."
status: ready
estimated_time: 30m
tags: [markov, matrices, probabilidad]
---

# La cadena de Markov, en general

**¿Qué es una cadena de Markov con cualquier número de estados y cómo se mueve?**

Al terminar tendrás:

- **Una definición general:** estados, distribución inicial, propiedad de Markov y homogeneidad.
- **Una matriz bien orientada:** filas de salida, columnas de llegada y dimensiones explícitas.
- **La cuenta de uno y varios pasos:** multiplicación, potencias y sus justificaciones.
- **Dos objetos distintos:** la distribución de probabilidades y una trayectoria aleatoria.

## Lo que traes

De [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]]:

- **Evento:** un conjunto de resultados del experimento, como estar en cierto estado (@mkv-c1-experimento).
- **Variable aleatoria:** $S_t$ nombra el estado todavía aleatorio; sus valores son estados concretos (@mkv-c1-variable-aleatoria).
- **Condicional:** exige que el evento dado tenga probabilidad positiva (@mkv-c1-prob-condicional).
- **Independencia condicional:** dado el presente, otra información puede dejar de modificar una probabilidad (@mkv-c1-independencia-condicional).
- **Probabilidad total:** combina casos disjuntos con sus probabilidades (@mkv-c1-teo-total).
- **Promedio de repeticiones:** requiere repetir independientemente el mismo experimento (@mkv-c1-teo-promedio).

**Página de concepto:** sin simulación, código ni algoritmo; todo va en letras, para $k$ estados cualesquiera.

---

## 1 · Leer los estados y la matriz

**Piensa: ¿cómo organizas las probabilidades de pasar entre estados?**

En una matriz cuadrada: cada fila fija el origen y cada columna, el destino.

::: definition {#mkv-c1-matriz-transicion title="Matriz de transición estocástica por filas"}
$$
\begin{aligned}
\mathcal S&=\{s_1,\dots,s_k\},\qquad k\ge1,\\
P&=(P_{ij})\in\mathbb R^{k\times k},\\
P_{ij}&=P(s_j\mid s_i),\\
P_{ij}&\ge0,\qquad
\sum_{j=1}^kP_{ij}=1
\quad(1\le i\le k).
\end{aligned}
$$

Para una transición regida por $P$:

$$
\begin{aligned}
P_{ij}
&=\Pr(S_{t+1}=s_j\mid S_t=s_i),\\
&\hspace{1em}\text{si }\Pr(S_t=s_i)>0.
\end{aligned}
$$

- **Qué es:** una matriz cuadrada de probabilidades; los mismos estados aparecen como salidas y llegadas.
- **Cómo se calcula:** la fila $i$ reúne las probabilidades de cada destino desde $s_i$.
- **Qué significa:** $P_{ij}$ se lee «desde $s_i$, hacia $s_j$, en un paso».
- **Qué no es:** una columna no es, en general, una distribución; sus entradas pueden sumar algo distinto de uno.
:::

- **Cuadrada:** $k$ filas (de dónde sales) y $k$ columnas (a dónde llegas), porque los estados son los mismos.
- **Estados sin probabilidad actual:** su fila sigue especificada por el modelo, aunque esa condicional no esté definida.
- **Notación:** $P$ nombra la matriz, como en agentes; aquí no nombra la clase P de complejidad.

$$
\begin{aligned}
P_{ij}=0
&\Longrightarrow
\text{transición imposible en el modelo},\\
P_{ii}
&=P(s_i\mid s_i),\\
s_i\longrightarrow s_j
&\Longleftrightarrow P_{ij}>0.
\end{aligned}
$$

- **Diagonal:** sus entradas dan las probabilidades de quedarse.
- **Grafo:** un nodo por estado; cada flecha lleva el peso de su entrada positiva.

Con el vector columna de unos:

$$
\begin{aligned}
\mathbf 1&=
\begin{pmatrix}1\\ \vdots\\1\end{pmatrix}
\in\mathbb R^{k\times1},\\
P\mathbf 1&=\mathbf 1.
\end{aligned}
$$

- **Lectura:** multiplicar por esa columna suma cada fila.

**Ejemplo abstracto: tres estados.** Escribimos $p_{ij}=P_{ij}$ para las entradas de esta matriz simbólica.

$$
\begin{aligned}
\mathcal S&=\{s_1,s_2,s_3\},\\
P&=
\begin{pmatrix}
p_{11}&p_{12}&p_{13}\\
p_{21}&p_{22}&p_{23}\\
p_{31}&p_{32}&p_{33}
\end{pmatrix}
\in\mathbb R^{3\times3},\\
p_{ij}&\ge0,\\
p_{i1}+p_{i2}+p_{i3}&=1
\quad(i=1,2,3).
\end{aligned}
$$

- **Fila 2:** sale de $s_2$; columna 3: reúne las probabilidades de llegar a $s_3$ desde cada origen.
- **Grafo en palabras:** desde cada $s_i$ hay flecha hacia cada $s_j$ cuyo $p_{ij}$ sea positivo.

**Contraejemplo simbólico:** sea $\varepsilon>0$ y sea $P$ la matriz anterior.

$$
\begin{aligned}
M&=
\begin{pmatrix}
p_{11}+\varepsilon&p_{12}&p_{13}\\
p_{21}&p_{22}&p_{23}\\
p_{31}&p_{32}&p_{33}
\end{pmatrix},\\
\sum_{j=1}^3M_{1j}&=1+\varepsilon\ne1.
\end{aligned}
$$

- **Falla:** $M$ no es matriz de transición; su primera fila reparte más probabilidad de la disponible.

::: exercise {#mkv-c1-ej-leer-entrada title="Interpreta una entrada y su inversa"}
En la matriz de tres estados, ¿qué significa $p_{31}$? Si vale cero, ¿también debe valer cero $p_{13}$?
:::

::: hint {#mkv-c1-pista-leer-entrada of="mkv-c1-ej-leer-entrada" title="¿Cuál índice fija la salida?"}
¿Qué origen y qué destino señala cada índice?
:::

::: answer {#mkv-c1-resp-leer-entrada of="mkv-c1-ej-leer-entrada"}
- **Entrada:** $p_{31}$ es la probabilidad de pasar de $s_3$ a $s_1$.
- **Sentido contrario:** $p_{13}$ puede ser positivo; las dos flechas tienen probabilidades distintas.
:::

La matriz describe las transiciones; falta precisar cómo gobierna una sucesión de estados.

---

## 2 · Definir la cadena

**Piensa: ¿qué falta, además de la matriz, para definir una cadena?**

Faltan la distribución inicial y las condiciones que permiten usar la misma fila después de cualquier historia.

::: definition {#mkv-c1-cadena title="Cadena de Markov finita y homogénea"}
$$
\begin{aligned}
&S_0,S_1,\dots\in\mathcal S=\{s_1,\dots,s_k\},\\
&(\mathcal S,\mu_0,P),\\
&\mu_0\in\mathbb R^{1\times k},
\qquad P\in\mathbb R^{k\times k},\\
&\mu_0(s_i)=\Pr(S_0=s_i)\ge0,\\
&\sum_{i=1}^k\mu_0(s_i)=1,\\
&P_{ij}=P(s_j\mid s_i)\ge0,
\qquad\sum_{j=1}^kP_{ij}=1.
\end{aligned}
$$

Para todo paso entero $t\ge0$, define la historia:

$$
H_t=\{S_0=s_{i_0},\dots,S_t=s_{i_t}\}.
$$

Para toda historia con $\Pr(H_t)>0$ y todo destino $s_j$:

$$
\begin{aligned}
&\Pr(S_{t+1}=s_j\mid H_t)\\
&\quad=\Pr(S_{t+1}=s_j\mid S_t=s_{i_t})\\
&\quad=P_{i_tj}.
\end{aligned}
$$

- **Qué es:** una sucesión de estados aleatorios descrita por estados posibles, distribución inicial y matriz de transición.
- **Cómo se calcula:** la primera igualdad elimina la historia anterior al presente; es la propiedad de Markov.
- **Qué significa:** la segunda igualdad usa la misma $P$ en todo paso; eso es homogeneidad.
- **Qué no es:** «sin memoria» significa independencia condicional del pasado dado el presente (@mkv-c1-independencia-condicional), no independencia entre estados consecutivos.
:::

- **Índices:** $s_i$ enumera estados; $t$ enumera pasos. La trayectoria puede repetir el mismo estado.
- **Inicio:** $\mu_0$, «mu cero», reparte la probabilidad inicial; no es el multiplicador de KKT.

**Ejemplo abstracto: tres estados.** Si la historia indicada tiene probabilidad positiva:

$$
\begin{aligned}
&\Pr(S_2=s_3\mid S_0=s_1,\ S_1=s_2)\\
&\quad=\Pr(S_2=s_3\mid S_1=s_2)\\
&\quad=p_{23}.
\end{aligned}
$$

- **Lo que basta:** saber que el presente es $s_2$.
- **Dependencia permitida:** $p_{13}$ y $p_{23}$ pueden diferir; cambiar el presente puede cambiar la predicción.

::: exercise {#mkv-c1-ej-historias-mismo-final title="Compara dos historias"}
Dos historias de probabilidad positiva terminan en $s_2$, en el mismo paso. ¿Pueden dar probabilidades distintas de ir después a $s_3$?
:::

::: hint {#mkv-c1-pista-historias-mismo-final of="mkv-c1-ej-historias-mismo-final" title="¿Qué conserva la condición?"}
Después de aplicar la propiedad de Markov, ¿qué información de cada historia permanece?
:::

::: answer {#mkv-c1-resp-historias-mismo-final of="mkv-c1-ej-historias-mismo-final"}
**No:** ambas probabilidades valen $p_{23}$. Una diferencia violaría la propiedad de Markov para esos estados.
:::

La cadena ya está definida; representemos la incertidumbre sobre su estado en cada paso.

---

## 3 · Escribir distribuciones como filas

**Piensa: ¿cómo describes dónde puede estar la cadena en un paso?**

Con un vector fila que asigna una probabilidad a cada estado.

::: definition {#mkv-c1-distribucion title="La distribución en el paso t"}
$$
\begin{aligned}
\mu_t(s_i)&=\Pr(S_t=s_i),\\
\mu_t&=
\begin{pmatrix}
\mu_t(s_1)&\cdots&\mu_t(s_k)
\end{pmatrix}
\in\mathbb R^{1\times k},\\
\mu_t(s_i)&\ge0,\qquad
\sum_{i=1}^k\mu_t(s_i)=1.
\end{aligned}
$$

- **Qué es:** el vector fila de probabilidades del estado en el paso $t$.
- **Cómo se calcula:** reúne una probabilidad por estado, en el mismo orden que las filas y columnas de $P$.
- **Qué significa:** describe dónde puede estar la cadena en ese paso.
- **Qué no es:** estar en un estado en el paso $t$ difiere de haberlo visitado alguna vez antes.
:::

$$
\begin{aligned}
\mu_0=\mathbf e_i
&\Longleftrightarrow \Pr(S_0=s_i)=1,\\
(\mathbf e_i)_j
&=
\begin{cases}
1,&j=i,\\
0,&j\ne i,
\end{cases}\\
\mathbf e_i&\in\mathbb R^{1\times k}.
\end{aligned}
$$

- **Inicio fijo:** $\mathbf e_i$, «e sub i», es la fila $i$ de la matriz identidad.
- **Inicio al azar:** cualquier fila no negativa que sume uno puede ser $\mu_0$.
- **Orientación:** elegimos filas porque $P$ organiza las salidas por fila; la distribución se multiplica a su izquierda.

**Ejemplo abstracto: tres estados.**

$$
\begin{aligned}
\mu_0&=\begin{pmatrix}a&b&c\end{pmatrix}
\in\mathbb R^{1\times3},\\
a,b,c&\ge0,\qquad a+b+c=1,\\
\Pr(S_0=s_2)=1
&\Longleftrightarrow
\mu_0=\begin{pmatrix}0&1&0\end{pmatrix}.
\end{aligned}
$$

- **Lectura:** $a$, $b$ y $c$ son las probabilidades iniciales, no entradas de la matriz de transición.

::: exercise {#mkv-c1-ej-inicio-dos-estados title="Escribe un inicio incierto"}
La cadena empieza en $s_1$ con probabilidad $a$ y en $s_3$ con probabilidad $1-a$, con $0<a<1$. Escribe $\mu_0$ y su forma.
:::

::: hint {#mkv-c1-pista-inicio-dos-estados of="mkv-c1-ej-inicio-dos-estados" title="¿Qué lugar corresponde al estado ausente?"}
En el orden $s_1,s_2,s_3$, ¿qué probabilidad debe ocupar la segunda entrada?
:::

::: answer {#mkv-c1-resp-inicio-dos-estados of="mkv-c1-ej-inicio-dos-estados"}
$$
\mu_0=\begin{pmatrix}a&0&1-a\end{pmatrix}
\in\mathbb R^{1\times3}.
$$
:::

Con la distribución escrita como fila, podemos calcular cómo cambia al dar un paso.

---

## 4 · Avanzar un paso multiplicando

**Piensa: ¿cómo obtienes la distribución del paso siguiente?**

Multiplicas la distribución actual por la matriz de transición, con la fila a la izquierda.

::: theorem {#mkv-c1-teo-predecir title="La distribución avanza multiplicando por la matriz"}
En una cadena finita y homogénea de @mkv-c1-cadena, para todo entero $t\ge0$:

$$
\begin{aligned}
\mu_{t+1}&=\mu_tP,\\
\mu_{t+1}(s_j)&=\sum_{i=1}^k\mu_t(s_i)P_{ij},\\
\mu_t&=\mu_0P^t,\\
(1\times k)(k\times k)&=(1\times k).
\end{aligned}
$$

Aquí $P^t$ multiplica $P$ por sí misma $t$ veces; $P^0=I_k$, la identidad de tamaño $k\times k$.
:::

- **Lectura:** a $s_j$ se llega desde cada $s_i$; cada posibilidad pesa la probabilidad de estar en su origen.
- **Producto:** la entrada $j$ combina la fila $\mu_t$ con la columna $j$ de $P$.

::: proof {#mkv-c1-dem-predecir of="mkv-c1-teo-predecir"}
**Probabilidad total.** Los eventos $\{S_t=s_i\}$ forman una partición (@mkv-c1-teo-total). Conserva primero solo los de probabilidad positiva:

$$
J_t=\{i:\mu_t(s_i)>0\}.
$$

$$
\begin{aligned}
\mu_{t+1}(s_j)
&=\sum_{i\in J_t}\mu_t(s_i)\\
&\quad{}\cdot\Pr(S_{t+1}=s_j\mid S_t=s_i)\\
&=\sum_{i\in J_t}\mu_t(s_i)P_{ij}\\
&=\sum_{i=1}^k\mu_t(s_i)P_{ij}.
\end{aligned}
$$

- **Markov:** dado el presente, conocer la historia anterior no cambia la distribución del siguiente estado.
- **Homogeneidad:** esa condicional usa la misma entrada $P_{ij}$ en cada paso.
- **Casos omitidos:** reincorporarlos aporta cero mediante $\mu_t(s_i)P_{ij}$, sin evaluar condicionales indefinidas.

**Inducción sobre el paso.**

$$
\begin{aligned}
t=0:\quad&\mu_0=\mu_0I_k=\mu_0P^0,\\
\mu_t=\mu_0P^t
\quad&\Longrightarrow\\
\mu_{t+1}
&=\mu_tP\\
&=\mu_0P^tP=\mu_0P^{t+1}.
\end{aligned}
$$
:::

**El resultado sigue siendo una distribución.**

$$
\begin{aligned}
\mu_{t+1}(s_j)&\ge0,\\
\mu_{t+1}\mathbf 1
&=(\mu_tP)\mathbf 1\\
&=\mu_t(P\mathbf 1)\\
&=\mu_t\mathbf 1=1.
\end{aligned}
$$

**El orden importa.** Para $k>1$:

$$
\underbrace{P}_{k\times k}
\underbrace{\mu_t}_{1\times k}
\quad\text{no está definido}.
$$

- **Motivo:** las dimensiones interiores no coinciden. Con un solo estado, ambas matrices son $1\times1$.
- **Otra convención:** el superíndice $\mathsf T$ indica trasposición: intercambia filas y columnas. Con distribuciones columna, el producto se escribe:

$$
\begin{aligned}
\mu_{t+1}^{\mathsf T}&=P^{\mathsf T}\mu_t^{\mathsf T},\\
(k\times k)(k\times1)&=(k\times1).
\end{aligned}
$$

**Ejemplo abstracto: tres estados.** Con la matriz simbólica de la sección 1:

$$
\begin{aligned}
\mu_0&=\begin{pmatrix}a&b&c\end{pmatrix},\\
\mu_1&=
\begin{pmatrix}
\mu_1(s_1)&\mu_1(s_2)&\mu_1(s_3)
\end{pmatrix},\\
\mu_1(s_1)&=ap_{11}+bp_{21}+cp_{31},\\
\mu_1(s_2)&=ap_{12}+bp_{22}+cp_{32},\\
\mu_1(s_3)&=ap_{13}+bp_{23}+cp_{33}.
\end{aligned}
$$

Desde un estado fijo:

$$
\mathbf e_2P=
\begin{pmatrix}p_{21}&p_{22}&p_{23}\end{pmatrix}.
$$

- **Selección de fila:** en general, $\mathbf e_iP$ es exactamente la fila $i$ de $P$.

::: exercise {#mkv-c1-ej-completar-un-paso title="Completa una llegada"}
Con el siguiente inicio, escribe $\mu_1(s_2)$ usando $p_{ij}$:

$$
\mu_0=\begin{pmatrix}a&0&1-a\end{pmatrix},
\qquad 0\le a\le1.
$$
:::

::: hint {#mkv-c1-pista-completar-un-paso of="mkv-c1-ej-completar-un-paso" title="¿Desde cuáles orígenes llega probabilidad?"}
¿Qué términos desaparecen al pesar cada origen por su probabilidad inicial?
:::

::: answer {#mkv-c1-resp-completar-un-paso of="mkv-c1-ej-completar-un-paso"}
$$
\mu_1(s_2)=ap_{12}+(1-a)p_{32}.
$$

**Llegadas:** una desde $s_1$ y otra desde $s_3$; el origen $s_2$ tiene peso cero.
:::

Repetir el producto de un paso lleva a las potencias de la matriz.

---

## 5 · Avanzar varios pasos con potencias

**Piensa: ¿cómo reúnes varias transiciones en una sola matriz?**

Con una potencia de la matriz de transición.

::: theorem {#mkv-c1-teo-potencias title="Las potencias describen transiciones de varios pasos"}
Para una cadena finita y homogénea y enteros $t,t_1,t_2\ge0$:

$$
\begin{aligned}
P^t&\in\mathbb R^{k\times k},\\
(P^t)_{ij}&\ge0,\qquad P^t\mathbf 1=\mathbf 1,\\
\mu_t&=\mu_0P^t,\\
P^{t_1+t_2}&=P^{t_1}P^{t_2},\\
(P^{t_1+t_2})_{ij}
&=\sum_{l=1}^k(P^{t_1})_{il}(P^{t_2})_{lj}.
\end{aligned}
$$

Si $\Pr(S_0=s_i)>0$:

$$
(P^t)_{ij}=\Pr(S_t=s_j\mid S_0=s_i).
$$

Con inicio fijo $\mu_0=\mathbf e_i$, $\mu_t$ es la fila $i$ de $P^t$.
:::

- **Lectura:** la potencia cuenta exactamente $t$ transiciones; no la probabilidad de haber llegado antes.
- **Estado intermedio:** la suma separa los caminos según el estado $s_l$ en que están tras $t_1$ pasos.

::: proof {#mkv-c1-dem-potencias of="mkv-c1-teo-potencias"}
**Filas que suman 1.** Inducción sobre $t$; los productos de entradas no negativas son no negativos.

$$
\begin{aligned}
P^0\mathbf 1&=I_k\mathbf 1=\mathbf 1,\\
P^{t+1}\mathbf 1
&=P^t(P\mathbf 1)
=P^t\mathbf 1=\mathbf 1.
\end{aligned}
$$

**Potencias.** $P^{t_1+t_2}$ es el producto de $t_1+t_2$ factores $P$; agruparlos en dos bloques da $P^{t_1}P^{t_2}$.

**Lectura condicional.** Condicionar en $S_0=s_i$ es empezar con $\mu_0=\mathbf e_i$. Por @mkv-c1-teo-predecir:

$$
\begin{aligned}
\Pr(S_t=s_j\mid S_0=s_i)
&=(\mathbf e_iP^t)_j\\
&=(P^t)_{ij}.
\end{aligned}
$$
:::

**Ejemplo abstracto: tres estados.**

$$
\begin{aligned}
(P^2)_{ij}&=\sum_{l=1}^3p_{il}p_{lj},\\
(P^2)_{13}
&=p_{11}p_{13}\\
&\quad+p_{12}p_{23}\\
&\quad+p_{13}p_{33}.
\end{aligned}
$$

- **Caminos:** de $s_1$ a $s_3$ pasando por $s_1$, por $s_2$ o por $s_3$.
- **No es elevar cada entrada al cuadrado:** se multiplican probabilidades sobre caminos y se suman alternativas.

::: exercise {#mkv-c1-ej-cero-dos-pasos title="Distingue un paso de dos"}
Si $p_{13}=0$ y $p_{12}p_{23}>0$, ¿puede llegarse de $s_1$ a $s_3$ en dos pasos?
:::

::: hint {#mkv-c1-pista-cero-dos-pasos of="mkv-c1-ej-cero-dos-pasos" title="¿Qué camino permanece?"}
¿Cuál de los tres términos sobrevive al sustituir el cero?
:::

::: answer {#mkv-c1-resp-cero-dos-pasos of="mkv-c1-ej-cero-dos-pasos"}
$$
(P^2)_{13}=p_{12}p_{23}>0.
$$

**Sí:** el camino pasa por $s_2$, aunque la transición directa sea imposible.
:::

Las potencias reúnen caminos posibles; distingamos esa distribución de un camino realizado.

---

## 6 · Distinguir distribución y trayectoria

**Piensa: ¿calcular la distribución produce un camino de la cadena?**

No: la distribución reúne probabilidades; una trayectoria elige un estado en cada paso.

Para la cadena de @mkv-c1-cadena y una secuencia de índices $i_0,\dots,i_t$:

$$
\begin{aligned}
\mu_t&=\mu_0P^t\in\mathbb R^{1\times k},\\
&\Pr(S_0=s_{i_0},\dots,S_t=s_{i_t})\\
&\quad=\mu_0(s_{i_0})
\prod_{j=0}^{t-1}P_{i_ji_{j+1}}.
\end{aligned}
$$

- **Distribución:** fijados $\mu_0$ y $P$, multiplicar determina sus probabilidades sin azar adicional.
- **Trayectoria:** una realización elige un estado inicial y después un destino con las probabilidades de la fila actual.

**De dónde sale:** la regla del producto (@mkv-c1-teo-producto) encadena condicionales; Markov y homogeneidad las convierten en entradas de $P$.

- **Secuencia imposible:** si algún prefijo tiene probabilidad cero, la trayectoria completa y el producto valen cero.
- **Paso cero:** el producto sin factores vale uno y queda la probabilidad inicial.

Para $n$ réplicas independientes con los mismos $\mu_0$ y $P$, fija el paso $t$ y el estado $s_j$:

$$
\frac{\#\{\text{réplicas en }s_j\text{ en el paso }t\}}{n}
\longrightarrow\mu_t(s_j).
$$

- **Condición:** la convergencia tiene probabilidad uno cuando $n$ crece, por @mkv-c1-teo-promedio.
- **Qué se repite:** la trayectoria completa; dentro de cada trayectoria, los estados pueden depender unos de otros.
- **Qué se cuenta:** un mismo paso entre réplicas, no distintos pasos de una sola trayectoria.
- **Muestreo:** cómo se elige el destino con un uniforme, MUESTREAR-FILA, está en [[mkv-el-problema-de-markov|El problema de Markov]].

**Ejemplo abstracto: tres estados.** Desde $s_1$:

$$
\begin{aligned}
\mu_0&=\mathbf e_1,\\
&\Pr(S_0=s_1,S_1=s_2,S_2=s_3)\\
&\quad=p_{12}p_{23},\\
\mu_2(s_3)
&=p_{11}p_{13}+p_{12}p_{23}\\
&\quad+p_{13}p_{33}.
\end{aligned}
$$

- **Un camino:** el producto exige pasar por $s_2$.
- **Una llegada:** la distribución reúne todos los caminos que terminan en $s_3$.

::: exercise {#mkv-c1-ej-trayectoria-y-marginal title="Compara el camino con la llegada"}
¿Puede la probabilidad del camino $s_1\to s_2\to s_3$ superar $\mu_2(s_3)$, con inicio fijo en $s_1$? Justifica.
:::

::: hint {#mkv-c1-pista-trayectoria-y-marginal of="mkv-c1-ej-trayectoria-y-marginal" title="¿Qué signos tienen las otras contribuciones?"}
Al quitar la contribución de ese camino, ¿puede quedar una cantidad negativa?
:::

::: answer {#mkv-c1-resp-trayectoria-y-marginal of="mkv-c1-ej-trayectoria-y-marginal"}
$$
p_{12}p_{23}\le\mu_2(s_3).
$$

**No:** ese camino es una de las posibilidades de llegada. Las demás contribuciones son no negativas.
:::

Todos estos objetos tienen una forma fija; revisarla detecta un producto mal escrito.

---

## 7 · Comprobar las dimensiones

**Piensa: ¿cómo compruebas que cada producto tiene sentido?**

Revisas que coincidan las dimensiones interiores y que todos los objetos usen el mismo orden de estados.

Para una cadena finita y homogénea, con el mismo orden de estados en todos los objetos:

$$
\begin{aligned}
P,P^t&\in\mathbb R^{k\times k},\\
\mu_t,\mathbf e_i,\mu_tP&\in\mathbb R^{1\times k},\\
\mathbf 1&\in\mathbb R^{k\times1},\\
\mu_tP\mathbf 1&=1.
\end{aligned}
$$

- **Lectura:** las dimensiones determinan qué productos existen.
- **Normalización:** sumar uno tiene sentido sobre una distribución completa, no sobre cualquier columna o entrada aislada.

::: table {#mkv-c1-tabla-dimensiones title="Forma y lectura de los objetos de la cadena"}
| Objeto | Forma | Qué suma 1 | Cómo se lee |
|---|---|---|---|
| $P$ | $k\times k$ | Cada fila | Transiciones de un paso |
| $P_{ij}$ | Escalar ($1\times1$) | Nada exigido | De $s_i$ a $s_j$ |
| Fila $i$ de $P$ | $1\times k$ | Sus entradas | Destinos desde $s_i$ |
| Columna $j$ de $P$ | $k\times1$ | Nada exigido | Llegada a $s_j$, por origen |
| $\mu_t$ | $1\times k$ | Sus entradas | Estado en el paso $t$ |
| $\mu_0=\mathbf e_i$ | $1\times k$ | Sus entradas | Inicio fijo en $s_i$ |
| $\mu_tP$ | $1\times k$ | Sus entradas | Estado un paso después |
| $P^t$ | $k\times k$ | Cada fila | Transiciones de $t$ pasos |
:::

**Ejemplo abstracto: tres estados.**

$$
\begin{aligned}
\text{fila 2 de }P
&=\begin{pmatrix}p_{21}&p_{22}&p_{23}\end{pmatrix}\\
&\in\mathbb R^{1\times3},\\
\text{columna 2 de }P
&=\begin{pmatrix}p_{12}\\p_{22}\\p_{32}\end{pmatrix}\\
&\in\mathbb R^{3\times1},\\
p_{21}+p_{22}+p_{23}&=1.
\end{aligned}
$$

- **Columna 2:** ninguna condición obliga a que sus entradas sumen uno.

::: exercise {#mkv-c1-ej-forma-producto-final title="Reconoce la forma del resultado"}
Con tres estados, ¿qué forma tiene $\mu_tP^2$? ¿Y $\mu_tP^2\mathbf 1$?
:::

::: hint {#mkv-c1-pista-forma-producto-final of="mkv-c1-ej-forma-producto-final" title="¿Qué dimensiones quedan afuera?"}
Tras comprobar las dimensiones interiores, ¿cuáles determinan la forma de cada resultado?
:::

::: answer {#mkv-c1-resp-forma-producto-final of="mkv-c1-ej-forma-producto-final"}
$$
\begin{aligned}
\mu_tP^2&:\quad1\times3,\\
\mu_tP^2\mathbf 1&:\quad1\times1,\\
\mu_tP^2\mathbf 1&=1.
\end{aligned}
$$
:::

Con estas formas puedes comprobar los productos de los ejercicios siguientes.

---

## Ejercicios

::: exercise {#mkv-c1-ej-dos-pasos-simbolicos title="Calcula una distribución completa a dos pasos"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Usa la matriz simbólica de tres estados de la sección 1.

**Cambia una idea:** empieza con certeza en $s_1$, en lugar del inicio general de la sección 4.

1. **Calcula:** escribe las tres entradas de $\mu_2$, desarrolladas con $p_{ij}$.
2. **Comprueba:** demuestra que son no negativas y suman uno.
3. **Dimensiona:** da la forma de $\mu_0$, $P^2$, $\mu_2$ y $\mu_2\mathbf 1$.
:::

::: hint {#mkv-c1-pista-dos-pasos-simbolicos-1 of="mkv-c1-ej-dos-pasos-simbolicos" title="Pista 1 · ¿Qué destinos intermedios debes considerar?"}
Para cada estado final, ¿por cuáles estados pudo pasar la cadena después de la primera transición?
:::

::: hint {#mkv-c1-pista-dos-pasos-simbolicos-2 of="mkv-c1-ej-dos-pasos-simbolicos" title="Pista 2 · ¿Qué ocurre al reunir todos los destinos?"}
¿Puedes agrupar tu suma por el estado intermedio y reconocer una condición de la matriz?
:::

::: answer {#mkv-c1-resp-dos-pasos-simbolicos of="mkv-c1-ej-dos-pasos-simbolicos" title="Respuesta · La fila inicial después de dos transiciones"}
**1. Calcula.**

$$
\begin{aligned}
\mu_0&=\mathbf e_1,\\
\mu_2&=\mathbf e_1P^2,\\
\mu_2(s_1)
&=p_{11}p_{11}+p_{12}p_{21}\\
&\quad+p_{13}p_{31},\\
\mu_2(s_2)
&=p_{11}p_{12}+p_{12}p_{22}\\
&\quad+p_{13}p_{32},\\
\mu_2(s_3)
&=p_{11}p_{13}+p_{12}p_{23}\\
&\quad+p_{13}p_{33}.
\end{aligned}
$$

**2. Comprueba.** Cada sumando es producto de entradas no negativas.

$$
\begin{aligned}
\sum_{j=1}^3\mu_2(s_j)
&=\sum_{j=1}^3\sum_{l=1}^3p_{1l}p_{lj}\\
&=\sum_{l=1}^3p_{1l}
\left(\sum_{j=1}^3p_{lj}\right)\\
&=\sum_{l=1}^3p_{1l}=1.
\end{aligned}
$$

**3. Dimensiona.**

$$
\begin{aligned}
\mu_0&:\quad1\times3,\\
P^2&:\quad3\times3,\\
\mu_2&:\quad1\times3,\\
\mu_2\mathbf 1&:\quad1\times1.
\end{aligned}
$$
:::

::: exercise {#mkv-c1-ej-convencion-columna title="Corrige la orientación de la distribución"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** guarda ahora la distribución como columna, para una cadena con $k\ge2$ estados. Conserva la matriz $P$ original.

1. **Diagnostica:** ¿está definido $P\mu_t^{\mathsf T}$? ¿Calcula en general las probabilidades del siguiente paso?
2. **Corrige:** escribe el producto correcto y sus dimensiones.
3. **Comprueba:** demuestra que el resultado correcto conserva la suma uno y tiene entradas no negativas.
:::

::: hint {#mkv-c1-pista-convencion-columna-1 of="mkv-c1-ej-convencion-columna" title="Pista 1 · ¿Qué entrada representa la llegada?"}
En la probabilidad del destino $s_j$, ¿qué índice de $P$ debe quedar fijo y cuál debe recorrerse?
:::

::: hint {#mkv-c1-pista-convencion-columna-2 of="mkv-c1-ej-convencion-columna" title="Pista 2 · ¿Coinciden las cuentas entrada por entrada?"}
¿Tu propuesta reproduce la fórmula escalar del paso siguiente? ¿Al sumar todas sus entradas recuperas uno?
:::

::: answer {#mkv-c1-resp-convencion-columna of="mkv-c1-ej-convencion-columna" title="Respuesta · Trasponer el producto completo"}
**1. Diagnostica.** El producto existe:

$$
(k\times k)(k\times1)=(k\times1).
$$

Pero su entrada $j$ intercambia el papel del origen y el destino:

$$
\begin{aligned}
(P\mu_t^{\mathsf T})_j
&=\sum_{i=1}^kP_{ji}\mu_t(s_i),\\
\mu_{t+1}(s_j)
&=\sum_{i=1}^kP_{ij}\mu_t(s_i).
\end{aligned}
$$

**2. Corrige.** Al trasponer un producto se invierte el orden de sus factores:

$$
\begin{aligned}
\mu_{t+1}^{\mathsf T}
&=(\mu_tP)^{\mathsf T}\\
&=P^{\mathsf T}\mu_t^{\mathsf T},\\
(k\times k)(k\times1)&=(k\times1).
\end{aligned}
$$

**3. Comprueba.** Todas las entradas son sumas de productos no negativos. La fila $\mathbf 1^{\mathsf T}$ suma la columna resultante:

$$
\begin{aligned}
\mathbf 1^{\mathsf T}
P^{\mathsf T}\mu_t^{\mathsf T}
&=(P\mathbf 1)^{\mathsf T}\mu_t^{\mathsf T}\\
&=\mathbf 1^{\mathsf T}\mu_t^{\mathsf T}\\
&=\mu_t\mathbf 1=1.
\end{aligned}
$$
:::

**Punto de control:** deberías poder orientar cada objeto, justificar la multiplicación y distinguir una trayectoria de una distribución. Comprueba las condiciones antes de interpretar cualquier probabilidad condicional.

---

## Lo que hay que llevarse

- **Matriz:** entradas no negativas y una distribución por fila.

$$
P\in\mathbb R^{k\times k},\qquad P\mathbf 1=\mathbf 1.
$$

- **Un paso:** suma las llegadas desde todos los orígenes.

$$
\mu_{t+1}=\mu_tP.
$$

- **Varios pasos:** desde un inicio fijo se selecciona una fila de la potencia.

$$
\mu_t=\mu_0P^t,\qquad \mathbf e_iP^t=\text{fila }i\text{ de }P^t.
$$

- **Un camino:** multiplica la probabilidad inicial por las transiciones que recorre.

$$
\begin{aligned}
&\Pr(S_0=s_{i_0},\dots,S_t=s_{i_t})\\
&\quad=\mu_0(s_{i_0})\prod_{j=0}^{t-1}P_{i_ji_{j+1}}.
\end{aligned}
$$

- **Formas:** fila $1\times k$, matriz $k\times k$, columna de unos $k\times1$; consulta @mkv-c1-tabla-dimensiones.

Continúa con [[mkv-el-problema-de-markov|El problema de Markov]].
