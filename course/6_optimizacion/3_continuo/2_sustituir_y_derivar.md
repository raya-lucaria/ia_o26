---
id: sustituir-y-derivar
title: Sustituir y derivar
nav_title: Sin restricción
summary: "El primer método para el reparto: quitar la restricción sustituyéndola, derivar, e igualar a cero. Funciona, da el reparto exacto, y deja de servir en cuanto no se puede despejar."
status: ready
estimated_time: 16m
tags: [optimizacion, gradiente, derivada]
---

# Sustituir y derivar

**¿Dónde está el mejor reparto, si ya no hay esquinas que mirar?**

El modelo del reactor está escrito y se sabe que su óptimo local es global. Falta
encontrarlo.

## 1 · Lo mínimo de derivadas

::: definition {#opt-gradiente title="Derivada parcial y gradiente"}
La **derivada parcial** $\partial f/\partial x_j$ es la derivada de $f$ mirando
solo la variable $x_j$ y tratando a las demás como constantes: cuánto cambia el
valor si mueves esa perilla y dejas quietas las otras.

El **gradiente** es el vector que las junta:

$$\nabla f(x) = \left(\frac{\partial f}{\partial x_1},\;\dots,\;
\frac{\partial f}{\partial x_n}\right).$$

Apunta en la dirección en que $f$ crece más rápido, y su tamaño dice qué tan
empinada está la subida.
:::

En el reactor, $\partial/\partial p_i$ de $\sum_j (b_j p_j - \tfrac12 p_j^2)$ es
$b_i - p_i$: **lo que paga la siguiente unidad de potencia en ese sistema**. Con
$b=(6,8,10)$, el gradiente en el reparto parejo $(5,5,5)$ es $(1,3,5)$.

## 2 · Por qué no basta con igualar el gradiente a cero

::: definition {#opt-estacionario title="Punto estacionario"}
Un punto es **estacionario** si $\nabla f = 0$: ninguna perilla, movida sola,
cambia el valor a primer orden.

En un problema **sin restricciones** y con $f$ cóncava y diferenciable, eso es
exactamente el máximo. Con restricciones, casi nunca: el óptimo suele estar
pegado a la frontera, donde la pendiente **no** es cero.
:::

Aquí se ve de inmediato. $\nabla f = 0$ pide $b_i - p_i = 0$, o sea
$p = (6,8,10)$: veinticuatro unidades de potencia. **Hay quince.** El punto
estacionario del objetivo ni siquiera es factible, y el óptimo del problema está
en otro lado.

::: table {#opt-dos-puntos title="El estacionario contra el factible"}
| Reparto | ¿Suma 15? | ¿Gradiente cero? | Rinde |
|---|---|---|---:|
| $(6,8,10)$ | no: suma 24 | sí | 100 |
| $(5,5,5)$ | sí | no: $(1,3,5)$ | 82.5 |
| $(3,5,7)$ | sí | no: $(3,3,3)$ | **86.5** |
:::

El primero es inalcanzable. El segundo es factible y mejorable. El tercero es el
que esta página va a encontrar, y conviene fijarse desde ahora en su gradiente:
**las tres componentes son iguales**.

## 3 · Sustituir la restricción, y que deje de haberla

::: remark {#opt-sustituir title="Sustituir y derivar"}
Si de la restricción se puede **despejar** una variable, se sustituye en el
objetivo y queda un problema sin restricciones, con una variable menos. Entonces
sí: derivar, igualar a cero, resolver.
:::

De $p_1+p_2+p_3=15$ sale $p_3 = 15 - p_1 - p_2$. Sustituyendo,

$$\begin{aligned}
g(p_1,p_2) = \;&\left(6p_1 - \tfrac{p_1^2}{2}\right)
+ \left(8p_2 - \tfrac{p_2^2}{2}\right) \\
+\;&\left(10(15-p_1-p_2) - \tfrac{(15-p_1-p_2)^2}{2}\right).
\end{aligned}$$

Las dos derivadas parciales quedan lineales:

$$\frac{\partial g}{\partial p_1} = 11 - 2p_1 - p_2 = 0,
\qquad
\frac{\partial g}{\partial p_2} = 13 - p_1 - 2p_2 = 0.$$

Dos ecuaciones, dos incógnitas: $p_1 = 3$, $p_2 = 5$, y de la restricción
$p_3 = 7$. **El reparto óptimo es $(3,5,7)$ y rinde 86.5.**

Y es el máximo global, no solo un punto donde la pendiente se anula: el objetivo
es cóncavo, el conjunto factible es convexo, y
[[el-rendimiento-que-decrece|el teorema de la página anterior]] hace el resto.

## 4 · El patrón que deja a la vista

En el óptimo, $b_i - p_i$ vale **3 en los tres sistemas**:

::: table {#opt-reparto-optimo title="El reparto óptimo, y lo que paga la siguiente unidad en cada sistema"}
| Sistema | $b_i$ | $p_i$ | $b_i - p_i$ |
|---|---:|---:|---:|
| Escudos | 6 | 3 | 3 |
| Motores | 8 | 5 | 3 |
| Soporte vital | 10 | 7 | 3 |
:::

Y tiene que ser así. Si a un sistema le pagara más que a otro la siguiente
unidad, convendría quitarle una al segundo y dársela al primero: el reparto no
sería óptimo. **En el mejor reparto, la última unidad de potencia rinde lo mismo
donde sea que la pongas.** Ese número común es 3, y la página siguiente muestra
que no es un detalle del ejemplo: tiene nombre, y ya lo conoces de otra clase.

> [!WARNING]
> **Sustituir tiene fecha de caducidad.** Aquí se pudo porque la restricción era
> una suma y despejar era de un renglón. Con $p_1^2 + p_2 p_3 = 15$ no se despeja
> limpio; con veinte variables y ocho restricciones, no se despeja en absoluto. El
> método de la página siguiente hace lo mismo **sin despejar nada**, y por eso es
> el que se queda.

## Lo que hay que llevarse

- El gradiente es la lista de lo que paga mover cada perilla por separado.
- Con restricciones, el óptimo casi nunca está donde el gradiente se anula: aquí
  ese punto ni siquiera era alcanzable.
- En el óptimo, lo que paga la siguiente unidad es **igual en todos los
  sistemas**. Ese número es la pista de todo lo que sigue.

De dónde sale ese 3: [[el-multiplicador|la página siguiente]].
