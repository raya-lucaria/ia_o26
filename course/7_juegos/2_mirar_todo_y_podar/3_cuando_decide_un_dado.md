---
id: cuando-decide-un-dado
title: Cuando decide un dado
nav_title: Cuando decide un dado
summary: "Un nodo que no decide nadie se valora con un promedio, no con un máximo ni un mínimo. Tratar al azar como un rival, o a un rival como azar, es un error de modelado."
status: ready
estimated_time: 12m
tags: [juegos, azar, expectiminimax]
---

# Cuando decide un dado

**¿Qué cambia si un nodo no lo decide nadie?**

Al terminar tendrás **un tercer tipo de nodo**, el de azar, y sabrás
valorarlo. También sabrás reconocer el error de modelado más común con el
azar.

Hexapawn no tiene azar: cada jugada la elige alguien. En
[[diagnosticar-el-juego|el diagnóstico de la clase 1]], un juego con dado
pedía otro modelo, un árbol con nodos de azar. Para verlo usamos un juego
pequeño, inventado para esta página.

## 1 · Repasar el valor esperado

> **Repaso de valor esperado.** Si un resultado aleatorio vale $x_1,\dots,x_n$
> con probabilidades $\Pr_1,\dots,\Pr_n$, que suman 1, su **valor esperado** es
> $\Pr_1x_1+\cdots+\Pr_nx_n$. Es el promedio ponderado: lo que obtendrías en
> promedio si repitieras la situación muchas veces. Un dado de seis caras
> justo da cada cara con probabilidad $1/6$. Por ejemplo, ganar 6 con
> probabilidad $1/2$ y 0 con $1/2$ vale en promedio 3.

## 2 · Valorar un juego con dado

Tú eres MAX y eliges entre dos acciones:

- **Plantarte:** la partida termina y ganas $+1$ seguro.
- **Tirar** un dado de seis caras. Con 1 o 2 pierdes y la partida termina
  en $-2$. Con 3, 4, 5 o 6 le toca al rival (MIN), que elige entre dos
  finales: $+3$ o $+4$ para ti.

**Piensa: ¿quién decide qué cara sale?**

Nadie. Después de Tirar hay un nodo donde **ni tú ni el rival eligen**: el
resultado lo fija el dado, con probabilidades conocidas. El árbol queda así:

- **Raíz** · decides tú (MAX)
  - **Plantarte** · FINAL, $+1$
  - **Tirar** · decide el dado (AZAR)
    - **1 o 2**, probabilidad $2/6$ · FINAL, $-2$
    - **3 a 6**, probabilidad $4/6$ · decide el rival (MIN)
      - FINAL, $+3$
      - FINAL, $+4$

Valoramos desde los finales, como en minimax:

1. **Nodo del rival:** elige lo peor para ti, $\min\{3,4\}=3$.
2. **Nodo del dado:** no elige nadie, así que **promediamos** con las
   probabilidades:

   $$V(\text{Tirar})=\tfrac{2}{6}(-2)+\tfrac{4}{6}(3)=-\tfrac{2}{3}+2=\tfrac{4}{3}.$$

3. **Raíz:** eliges lo mejor, $\max\{1,\ 4/3\}=4/3$.

**Conviene tirar.** En promedio, tirar vale $4/3\approx1.33$, más que el
$+1$ seguro. No garantiza ganar más en una partida: con probabilidad $1/3$
pierdes.

## 3 · No confundir el azar con un rival

**Piensa: ¿y si fueras prudente y supusieras que el dado siempre cae mal?**

Eso es tratar al dado como un rival que te odia, un nodo MIN:

$$V(\text{Tirar})=\min\{-2,\ 3\}=-2.$$

Con ese modelo te plantarías y te quedarías con $+1$. Pero el dado no
quiere nada: cae en 1 o 2 solo un tercio de las veces. **Tratar al azar como
rival es un error de modelado**, y aquí te hace elegir la acción que vale
menos en promedio.

El error contrario también existe. Si promediaras al rival como si eligiera
al azar entre $+3$ y $+4$, le darías valor $7/2$ y tirar valdría
$\tfrac{2}{6}(-2)+\tfrac{4}{6}\cdot\tfrac{7}{2}=\tfrac{5}{3}$. Ese número
**sobreestima** lo que obtienes: el rival no elige al azar, elige $+3$.

La regla es la del diagnóstico: **quien tiene intereses, optimiza; lo que no
los tiene, se promedia.**

## 4 · Reunir los tres tipos de nodo

::: definition {#jue-c2-nodo-azar title="Nodos MAX, MIN y de azar"}
En un árbol con azar, $P(s)$ puede valer MAX, MIN o AZAR. En un nodo de
azar, cada resultado $a\in A(s)$ ocurre con probabilidad $\Pr(a)$, y esas
probabilidades suman 1. El valor de un estado es:

- en un final, $U(s)$;
- en un nodo MAX, el máximo de los valores de sus hijos;
- en un nodo MIN, el mínimo;
- en un nodo de azar, el promedio ponderado
  $\sum_{a\in A(s)}\Pr(a)\,V\bigl(T(s,a)\bigr)$.
:::

El procedimiento es MINIMAX con un caso más. Se llama **expectiminimax**:

```text
INPUT   un estado s de un juego finito por turnos,
        con P, A, T, los finales, U y las probabilidades Pr.
OUTPUT  V(s), el valor esperado de s en puntos de MAX.

 1  function EXPECTIMINIMAX(s)
 2      if s es final: return U(s)
 3      if P(s) = MAX:  return máximo de EXPECTIMINIMAX(T(s, a)) sobre a in A(s)
 4      if P(s) = MIN:  return mínimo de EXPECTIMINIMAX(T(s, a)) sobre a in A(s)
 5      if P(s) = AZAR: return suma de Pr(a) · EXPECTIMINIMAX(T(s, a)) sobre a in A(s)
```

Las líneas 3 y 4 son MINIMAX abreviado; la 5 es la nueva. El costo crece:
cada nodo de azar multiplica el árbol por el número de resultados posibles,
y no se puede elegir solo uno porque todos cuentan en el promedio.

Con azar importa **cuánto** valen los finales, no solo su orden. Con
minimax bastaba saber qué final es mejor. Aquí, cambia $-2$ por $-20$: el
orden de los finales sigue siendo el mismo, $-20<1<3<4$, pero Tirar pasa a
valer

$$\tfrac{2}{6}(-20)+\tfrac{4}{6}\cdot3=-\tfrac{20}{3}+2=-\tfrac{14}{3}<1,$$

y ahora conviene plantarse. Sin tocar el orden, la decisión cambió.

> [!NOTE]
> Alfa-beta, en la página siguiente, se explica para árboles **sin azar**.
> Con nodos de azar también se puede podar, pero hace falta saber de
> antemano entre qué valores caen las utilidades.

## 5 · Comprobar con otros números

::: exercise {#jue-c2-ej-dado title="Decide si tiras"}
Ahora plantarte vale $+2$ seguro. Si tiras el dado: con 1 pierdes y la
partida termina en $-3$; con 2 a 6 el rival elige entre $+4$ y $+6$ para ti.

1. Calcula el valor de Tirar con fracciones. ¿Te plantas o tiras?
2. ¿Qué harías si trataras al dado como un rival?
3. ¿Cuánto valdría Tirar si promediaras también la elección del rival?
:::

::: answer {#jue-c2-resp-dado of="jue-c2-ej-dado"}
1. El rival elige $\min\{4,6\}=4$. Entonces
   $V(\text{Tirar})=\tfrac{1}{6}(-3)+\tfrac{5}{6}(4)=\tfrac{-3+20}{6}=\tfrac{17}{6}\approx2.83$.
   Como $17/6>2$, **tiras**.
2. Con el dado como MIN, Tirar valdría $\min\{-3,4\}=-3$ y te plantarías
   con $+2$: la decisión equivocada.
3. Promediando al rival, $(4+6)/2=5$ y Tirar valdría
   $\tfrac{1}{6}(-3)+\tfrac{5}{6}(5)=\tfrac{22}{6}=\tfrac{11}{3}$. La decisión
   no cambia, pero el valor está inflado: el rival nunca te dará $+6$.
:::

**Punto de control:** deberías poder valorar un árbol con nodos MAX, MIN y
de azar, y decir para cada nodo si se maximiza, se minimiza o se promedia.

## Lo que hay que llevarse

- Un nodo que no decide nadie se valora con el **promedio ponderado** de
  sus hijos.
- Tratar al azar como rival te hace demasiado prudente; tratar a un rival
  como azar te hace demasiado optimista. Las dos son errores de modelado.
- Expectiminimax es minimax con una línea más; con azar importan las
  distancias entre utilidades, no solo su orden.

Continúa con [[alfa-beta|alfa-beta]].
