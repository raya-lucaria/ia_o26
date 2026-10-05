---
id: maximin-como-programa-lineal
title: Maximin como programa lineal
nav_title: Maximin lineal
summary: "Elegir la mezcla que más asegura es un programa lineal. Con dos acciones se resuelve con un dibujo; con más, con simplex. Y lo que asegura uno coincide con lo que el otro impide."
status: ready
estimated_time: 35m
tags: [juegos, estrategias-mixtas, programacion-lineal]
---

# Maximin como programa lineal

**¿Cómo se elige la mezcla que más asegura?**

Al terminar tendrás **el programa lineal** de cualquier juego simultáneo de
suma cero, lo habrás resuelto con un dibujo para unos penales y sabrás por qué
el valor que aseguras tú es el mismo que el rival te impide superar.

## 1 · Separar datos y decisiones

**Piensa: en la garantía $g(p)$ hay un mínimo, y un programa lineal no admite
mínimos en el objetivo. ¿Cómo se quita?**

Igual que en la unidad de optimización, primero se separa lo que está dado de
lo que se elige. Las filas son $i=1,\dots,I$ y las columnas, $j=1,\dots,J$:

| Símbolo | Qué representa | ¿Dato o decisión? |
|---|---|---|
| $U(i,j)$ | Tu pago si juegas la fila $i$ y el rival la columna $j$ | Dato |
| $p_i$ | Probabilidad con la que juegas la fila $i$ | Decisión |
| $v$ | Un número que vas a poder asegurar | Decisión |

La idea es pedir directamente lo que quieres: **un número $v$ tan alto como
se pueda, que tu mezcla asegure contra todas las columnas**. Eso se escribe
así:

$$\begin{aligned}
\max_{p,\,v}\quad & v\\
\text{sujeto a}\quad & \sum_i p_i\,U(i,j)\ \ge\ v \quad \text{para cada columna } j,\\
& \sum_i p_i = 1,\\
& p_i \ge 0 \quad \text{para cada fila } i,\\
& v \text{ libre}.
\end{aligned}$$

Cada renglón dice una cosa en palabras:

- **El objetivo:** quiero que el número que aseguro sea lo más alto posible.
- **Una restricción por columna:** mi pago esperado contra **cada** respuesta
  pura del rival es al menos $v$.
- **La suma igual a 1 y $p\ge0$:** $p$ es de verdad una lista de
  probabilidades.
- **$v$ libre:** $v$ puede ser negativo. En pares o nones, jugar fijo asegura
  −1, y ese $v$ también es válido.

Al maximizar, $v$ sube hasta tocar el peor pago esperado: en el óptimo,
$v=g(p)$. El mínimo desapareció del objetivo y quedó repartido en una
restricción por columna, todas lineales en $p$ y $v$.

La mezcla óptima se escribe con pertenencia, porque puede haber empates:

$$p^{∗}\in\operatorname*{arg\,max}_{p}\ g(p).$$

Que el programa tenga una restricción por cada columna **pura**, y no por
cada mezcla del rival, se justifica en la sección 5, cuando ya tengas un
ejemplo con números.

## 2 · Plantear los penales

**Piensa: si el portero sabe hacia dónde tiras siempre, ¿qué hace?**

Ahora un ejemplo con números que no son simétricos. Eres el **tirador** de un
penal, y por lo tanto MAX. Tiras a la izquierda o a la derecha; el portero se
lanza a la izquierda o a la derecha, al mismo tiempo, sin ver tu tiro. Los
pagos son la **probabilidad de gol, en porcentaje**:

::: table {#jue-c4-penales title="Penales: probabilidad de gol, en %"}
| Tirador ↓ · Portero → | Se lanza a la izquierda | Se lanza a la derecha |
|---|:---:|:---:|
| **Tira a la izquierda** | 40 | 90 |
| **Tira a la derecha** | 80 | 50 |
:::

Aunque el portero adivine, a veces es gol; aunque falle, a veces el tiro se
va fuera. Lo que el portero gana es lo que tú pierdes en probabilidad de gol,
así que lo tratamos como suma cero.

Con un tiro fijo: a la izquierda, el peor caso es 40; a la derecha, 50. El
**maximin puro es 50**, tirando siempre a la derecha. Del lado del portero,
las columnas tienen máximos 80 y 90, así que el **minimax puro es 80**. Como
$50\ne80$, **no hay punto de silla**.

Con dos acciones, la mezcla se describe con un solo número: escribimos $p$
para la probabilidad de la primera fila, así que la mezcla es $(p,1-p)$.
Aquí $p$ es la probabilidad de tirar a la **izquierda**. El programa queda:

$$\begin{aligned}
\max_{p,\,v}\quad & v\\
\text{sujeto a}\quad & 40p+80(1-p)\ \ge\ v \quad \text{(portero a la izquierda)},\\
& 90p+50(1-p)\ \ge\ v \quad \text{(portero a la derecha)},\\
& 0\le p\le 1,\\
& v \text{ libre}.
\end{aligned}$$

Simplificando, las dos restricciones son $80-40p\ge v$ y $50+40p\ge v$.

## 3 · Dibujar la garantía

**Estamos aquí:** el programa de los penales tiene dos decisiones, $p$ y $v$,
y dos restricciones de columna. **Pendiente:** encontrar $p$ y $v$.

Con dos variables, el modelo se dibuja, como en [[el-dibujo|el dibujo]] de la
unidad de optimización. El eje horizontal es $p$, de 0 a 1. El vertical es el
pago esperado. Cada columna del portero es una **recta**:

| Portero | Tu pago esperado | En $p=0$ | En $p=1$ |
|---|---|---:|---:|
| Se lanza a la izquierda | $80-40p$ | 80 | 40 |
| Se lanza a la derecha | $50+40p$ | 50 | 90 |

La primera recta baja de 80 a 40; la segunda sube de 50 a 90. Dibújalas en
tu hoja antes de seguir.

Para cada $p$, la garantía es la **más baja** de las dos rectas en ese punto.
Esa línea quebrada, que va por debajo de las dos, se llama **envolvente
inferior**. Aquí primero sube, siguiendo la recta del portero a la derecha, y
después baja, siguiendo la otra.

**Decide:** antes de abrir la respuesta, encuentra el máximo en tu dibujo.

::: exercise {#jue-c4-ej-cruce title="Decide dónde está el máximo de la envolvente"}
¿En qué punto de la envolvente inferior está el máximo? Calcula $p$ y $v$.
:::

::: answer {#jue-c4-resp-cruce of="jue-c4-ej-cruce" title="Respuesta · Donde se cruzan las rectas"}
El máximo está donde la envolvente deja de subir y empieza a bajar: donde las
dos rectas se cruzan.

$$80-40p=50+40p\ \Longrightarrow\ 30=80p\ \Longrightarrow\ p=\tfrac38.$$

En ese punto, $v=80-40\cdot\tfrac38=80-15=65$.
:::

**Idea visible:** en los penales, el máximo de la envolvente está en el
**cruce** de las dos rectas. Se encuentra igualándolas: $80-40p=50+40p$ da
$p=3/8$, y entonces $v=65$.

El mismo dibujo, leído como en la unidad de optimización: en el plano
$(p,v)$, cada restricción deja los puntos **debajo** de su recta. La región
factible no tiene piso, porque $v$ es libre, pero por arriba está acotada, y
eso basta para maximizar $v$. Sus vértices de arriba son:

::: table {#jue-c4-esquinas title="Los vértices de arriba de la región"}
| Vértice | Qué lo forma | $v$ |
|---|---|---:|
| $p=0$ | Borde $p=0$ con la recta del portero a la derecha | 50 |
| $p=\tfrac38$ | Cruce de las dos rectas | **65** |
| $p=1$ | Borde $p=1$ con la recta del portero a la izquierda | 40 |
:::

Como en el polígono de la unidad 6, el óptimo está en un vértice de la
envolvente: en un cruce de rectas o en $p=0$ o $p=1$. En los penales, sin
punto de silla, es el cruce. Los otros dos vértices son los tiros fijos:
$p=0$ es tirar siempre a la derecha, con su 50, y $p=1$ es tirar siempre a
la izquierda, con su 40.

**La respuesta:** tira a la izquierda con probabilidad $3/8$ y a la derecha
con $5/8$. Así aseguras **65 %** de gol, pase lo que pase. Es 15 puntos más
que el mejor tiro fijo.

Tiras **más** a la derecha, aunque tu mejor número de la tabla, el 90, sea un
tiro a la izquierda. La mezcla no persigue el mejor caso; empareja las dos
rectas para que al portero le dé igual lanzarse a cualquier lado.

::: exercise {#jue-c4-ej-mitad title="Decide qué asegura la mitad y mitad"}
Un tirador decide tirar a cada lado con probabilidad $1/2$. ¿Cuánto asegura?
¿Contra qué lado del portero le va peor, y por qué eso confirma que $p=1/2$
no es el óptimo?
:::

::: answer {#jue-c4-resp-mitad of="jue-c4-ej-mitad"}
Con $p=\tfrac12$: contra el portero a la izquierda, $80-20=60$; contra el
portero a la derecha, $50+20=70$. Asegura **60 %**, menos que 65.

Le va peor contra el portero que se lanza a la izquierda. Que las dos rectas
den números distintos dice que el tirador no está en el cruce: un portero que
conozca la mezcla se lanzará siempre a la izquierda.
:::

## 4 · Mirar desde el portero

**Piensa: tú aseguras 65 %. ¿Podría el portero dejarte en menos?**

El portero resuelve su propio programa, con la misma convención: escribimos
$q$ para la probabilidad de su primera columna, así que su mezcla es
$(q,1-q)$. Aquí $q$ es la probabilidad de lanzarse a la **izquierda**. Él
quiere el número $w$ más **bajo** tal que tu pago esperado no pase de $w$,
tires a donde tires:

$$\begin{aligned}
\min_{q,\,w}\quad & w\\
\text{sujeto a}\quad & 40q+90(1-q)\ \le\ w \quad \text{(tiro a la izquierda)},\\
& 80q+50(1-q)\ \le\ w \quad \text{(tiro a la derecha)},\\
& 0\le q\le 1,\\
& w \text{ libre}.
\end{aligned}$$

Simplificando, sus dos rectas son $90-50q$ y $50+30q$. Ahora él busca el
punto más **bajo** de la envolvente **superior**, la más alta de las dos
rectas para cada $q$. La primera baja de 90 a 40 y la segunda sube de 50 a
80, así que ese punto está en el cruce:

$$90-50q=50+30q\ \Longrightarrow\ 40=80q\ \Longrightarrow\ q=\tfrac12.$$

Compruébalo en la tabla:

| Tiras a | Probabilidad de gol con $q=\tfrac12$ |
|---|---|
| La izquierda | $\tfrac12\cdot40+\tfrac12\cdot90=65$ |
| La derecha | $\tfrac12\cdot80+\tfrac12\cdot50=65$ |

Con esa mezcla, el portero asegura que **no pases de 65 %**. Tú aseguras al
menos 65; él asegura que no más de 65. Los dos números coinciden, y a ese
número común se le llama el **valor del juego**.

::: remark {#jue-c4-teorema-minimax title="El teorema minimax"}
En todo juego de suma cero con un número finito de acciones, lo más que puede
asegurar el jugador de las filas mezclando es igual a lo menos a lo que el de
las columnas puede limitarlo mezclando. Lo demostró John von Neumann en 1928.

En programación lineal, es un caso de **dualidad**: el programa del portero es
el dual del programa del tirador, y los dos tienen el mismo valor óptimo. Esta
unidad no lo demuestra, y la unidad de optimización tampoco cubrió la dualidad
como teoría.
:::

En la práctica: sin punto de silla, las jugadas puras dejan un hueco entre
50 y 80. **Mezclar cierra el hueco**, y lo cierra en el mismo punto para los
dos jugadores.

## 5 · Revisar solo las columnas puras

**Piensa: el portero acaba de mezclar con $q=\tfrac12$. ¿Por qué tu programa
solo tenía una restricción por columna pura?**

Toma un tirador que juega $p=\tfrac12$. Ya calculaste que saca 60 contra el
portero a la izquierda y 70 contra el portero a la derecha. Si el portero se
lanza a la izquierda con probabilidad $q$, el pago esperado del tirador es

$$q\cdot60+(1-q)\cdot70,$$

un **promedio** de 60 y 70, con pesos $q$ y $1-q$. Un promedio nunca queda
por debajo del menor de los números que promedia: dé lo que dé $q$, el
resultado está entre 60 y 70, nunca debajo de 60.

En general, si el rival juega la columna $j$ con probabilidad $q_j$, tu pago
esperado es

$$\sum_j q_j\Bigl(\sum_i p_i\,U(i,j)\Bigr),$$

el promedio, con pesos $q_j$, de tus pagos contra cada columna pura. Por eso,
si tu mezcla asegura al menos $v$ contra cada columna pura, también lo
asegura contra cualquier mezcla del rival. Basta una restricción por columna,
y el programa tiene un número finito de restricciones.

## 6 · Resolver sin dibujo

**Piensa: con tres acciones, ¿cuántas variables tiene el programa?**

Con más de dos acciones ya no se dibuja. En piedra, papel o tijera hay tres
probabilidades y $v$: cuatro variables. El programa, con las columnas de
[[jugar-a-la-vez|la página anterior]], es:

$$\begin{aligned}
\max_{p,\,v}\quad & v\\
\text{sujeto a}\quad & p_2-p_3\ \ge\ v \quad \text{(rival saca piedra)},\\
& -p_1+p_3\ \ge\ v \quad \text{(rival saca papel)},\\
& p_1-p_2\ \ge\ v \quad \text{(rival saca tijera)},\\
& p_1+p_2+p_3=1,\\
& p_1,p_2,p_3\ge0,\quad v \text{ libre}.
\end{aligned}$$

Aquí $p_1$, $p_2$ y $p_3$ son las probabilidades de piedra, papel y tijera.

Es un programa lineal como los de la unidad de optimización, y se resuelve con
[[de-esquina-en-esquina|simplex]], que camina de vértice en vértice sin
dibujo. Si lo resuelves con `linprog`, cuida tres cosas de
[[patrones-lineales|los patrones lineales]]:

1. `linprog` **minimiza**. Para maximizar $v$, el objetivo es $-v$, y al
   final hay que cambiar el signo del valor que devuelve.
2. Las restricciones $\ge$ se pasan a $\le$ cambiando el signo de los dos
   lados.
3. $v$ necesita la cota `(None, None)`, porque por omisión `linprog` obliga a
   las variables a ser no negativas.

**Comprobar una respuesta sin resolver.** Con $p=(1/3,1/3,1/3)$ y $v=0$, las
tres restricciones de columna dan $0\ge0$, la suma da 1 y nada es negativo:
el punto es **factible**, así que aseguras 0.

¿Se puede asegurar más de 0? No: si el rival juega la misma mezcla uniforme,
**cada una de tus filas** le da un pago esperado de 0. Contra esa mezcla,
ninguna estrategia tuya pasa de 0. El valor del juego es 0 y la mezcla
uniforme es óptima para los dos.

::: exercise {#jue-c4-ej-ppt-v title="Decide el mejor v para una mezcla fija"}
En el programa de piedra, papel o tijera, fija $p=(1/2,1/2,0)$.

1. ¿Es factible el punto con $v=0$? ¿Qué restricción falla?
2. ¿Cuál es el $v$ más alto que hace factible ese $p$? Compáralo con lo que
   calculaste en la página anterior.
:::

::: answer {#jue-c4-resp-ppt-v of="jue-c4-ej-ppt-v"}
1. No. La restricción de papel da $-\tfrac12+0=-\tfrac12$, y
   $-\tfrac12\ge0$ es falso. Las de piedra, $\tfrac12\ge0$, y tijera,
   $0\ge0$, sí se cumplen.
2. El $v$ más alto es el menor de los tres lados izquierdos:
   $\min\{\tfrac12,-\tfrac12,0\}=-\tfrac12$. Es la garantía $g(p)=-\tfrac12$
   de la página anterior: para una $p$ fija, el mejor $v$ es justo su
   garantía.
:::

**Qué modelo es.** Es un programa **lineal continuo**. Con $I$ filas y $J$
columnas tiene $I+1$ variables ($p_1,\ldots,p_I$ y $v$), $J$ restricciones
de columna, una igualdad y las cotas de $p$. Se resuelve con simplex; el
dibujo solo sirve cuando $I=2$.

**Punto de control:** deberías poder escribir el programa lineal de
cualquier tabla de suma cero, explicar cada renglón en palabras y resolver un
caso de 2×2 con las dos rectas, desde los dos jugadores. Si no te sale el
dibujo, vuelve a las secciones 3 y 4.

## Lo que hay que llevarse

- Elegir la mejor mezcla es un programa lineal: maximizar $v$ con una
  restricción por cada columna pura del rival, con $v$ libre.
- Con dos acciones se dibuja: la garantía es la envolvente inferior de las
  rectas y el óptimo está en un vértice de la envolvente: en un cruce de
  rectas o en $p=0$ o $p=1$. En los penales, sin punto de silla, es el cruce.
- Lo que tú aseguras mezclando es igual a lo que el rival te impide superar
  mezclando: el teorema minimax, un caso de dualidad.

Continúa con [[cuando-no-es-suma-cero|cuando no es suma cero]].
