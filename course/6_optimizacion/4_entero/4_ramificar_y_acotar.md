---
id: ramificar-y-acotar
title: Ramificar y acotar
nav_title: Ramificar
summary: "El algoritmo que no mira todos los planes y aun así demuestra que su respuesta es la mejor: parte el problema en dos, y descarta ramas enteras con una cuenta."
status: ready
estimated_time: 34m
tags: [optimizacion, entera, algoritmos]
---

# Ramificar y acotar

**¿Cómo descarto un plan que nunca miré?**

Vienes de [[enumerar|enumerar]] · Aquí: el algoritmo que sí escala.

Enumerar encontró el ganador en el candidato 17 de 20 **y siguió tres más**. No
le faltaba suerte: le faltaba un **argumento** para parar. Este algoritmo lo
tiene.

## 1 · La cota

::: definition {#opt-relajacion title="Relajación lineal"}
La **relajación** de un problema entero es el mismo problema **sin** la línea
$x\in\mathbb{Z}$:

$$\max\; c^{\mathsf T}x \quad\text{s.a.}\quad Ax \le b,\quad l \le x \le u$$

Ya no es un problema entero: es uno lineal, de los de la clase 2, y lo resuelve
simplex.
:::

**Por qué su valor es una cota, argumentado y no afirmado.**

Primero la regla, que no es de optimización sino de conjuntos:

> Si $A \subseteq B$, entonces $\max B \ge \max A$. **Agregar opciones nunca baja
> el máximo.**

Con números sueltos: si $A = \{12,\ 19,\ 20\}$ y le agregas el 21, el máximo sube
a 21. Si le agregas el 7, se queda en 20. Lo que no puede hacer es **bajar**.

Ahora, por qué aquí $A \subseteq B$. Un plan entero factible cumple $Ax \le b$ y
$l \le x \le u$. La relajación pide **exactamente eso y nada más** —solo deja de
exigir $x \in \mathbb{Z}$—, así que **ningún plan entero se cae**: todos siguen
estando.

En el taller, con $A$ = los 13 planes enteros y $B$ = todos los puntos del
polígono:

| Plan | ¿Entero? | ¿Está en la relajación? | Vale |
|---|---|---|---:|
| $(4,\ 0)$ | sí | sí | 20 |
| $(3,\ 1)$ | sí | sí | 19 |
| $(2,\ 2)$ | sí | sí | 18 |
| $(3,\ 3/2)$ | **no**: media sonda | **sí** | **21** |

Los tres primeros están en los dos conjuntos. El cuarto **solo está en el
segundo**, y es el que manda. Por eso

$$z_{\text{relajación}} \;\ge\; z_{\text{entero}}, \qquad\text{y aquí}\quad 21 \ge 20.$$

**Y a veces son iguales.** Si la relajación sale entera, ese punto está en los
dos conjuntos: entonces la cota no es una cota, es **la respuesta**. De eso vive
el algoritmo — es lo que cierra las ramas 2 y 4 del árbol.

::: definition {#opt-cota-relajacion title="Cota superior"}
Una **cota superior** de un subproblema es un número que **ningún** plan entero
suyo puede superar, calculado **sin** conocer ese plan.

Sirve para descartar: si la cota de una rama no supera a lo que ya tienes, esa
rama **no puede ganar**, y no hace falta abrirla.
:::

::: figure {#opt-relajacion-corte title="La cota que da la relajación"}
![El polígono del taller con los trece planes enteros que caben dentro, el óptimo continuo marcado con una cruz sobre el borde y el mejor plan entero resaltado en la esquina de abajo a la derecha](../_assets/opt-relajacion-corte.svg)
:::

En el taller:

| | Plan | Vale |
|---|---|---:|
| Relajación | $(3,\ 3/2)$ | **21** ← la cota |
| Mejor entero | $(4,\ 0)$ | 20 |

> **Cuidado.** La cota **no es la respuesta**. «Tres rovers y media sonda» no
> existe. Lo único que dice el 21 es que nadie va a pasar de ahí.

## 2 · Cómo usa el modelo

Cada pieza hace un trabajo, y solo uno:

| Pieza | Sirve para |
|---|---|
| La relajación de un subproblema | **Acotar** lo mejor que puede haber ahí abajo |
| ¿La solución salió entera? | **Cerrar** la rama |
| La mejor solución hasta ahora | **Podar** lo que ya no puede ganar |
| Una variable fraccionaria | **Partir** en dos |

::: definition {#opt-subproblema title="Subproblema"}
Un **subproblema** es el mismo modelo con las cotas más apretadas: mismo $c$,
misma $A$, mismo $b$, y un $l \le x \le u$ más chico.

Por eso todo lo que sabes del original sigue valiendo dentro de él.
:::

### Partir en dos, sin perder nada

La relajación de la raíz dio $x_2 = 3/2$. Se parte por ahí, con la regla general:

$$x_j \le \lfloor \bar x_j \rfloor \qquad\text{y}\qquad x_j \ge \lceil \bar x_j \rceil$$

Aquí, $x_2 \le 1$ y $x_2 \ge 2$.

::: figure {#opt-ramas title="Partir no pierde ninguna solución"}
![El mismo polígono partido en dos por una franja horizontal entre uno y dos, que no contiene ningún punto entero; arriba la rama de x dos mayor o igual que dos y abajo la de x dos menor o igual que uno](../_assets/opt-ramas.svg)
:::

**Las dos ramas cubren todo.** Entre $\lfloor \bar x_j \rfloor$ y
$\lceil \bar x_j \rceil$ **no hay ningún entero**: la franja que queda fuera está
vacía de soluciones. Por eso partir es exhaustivo y no una apuesta.

Y fíjate en lo que sí se pierde a propósito: el punto $(3,\ 3/2)$ —el de la
cota— **no está en ninguna de las dos ramas**. Ese es el punto: cada corte
obliga a la relajación a dar algo distinto, y por eso el árbol avanza.

::: definition {#opt-nodos-vivos title="Lista de nodos vivos"}
La **lista de nodos vivos** son los subproblemas creados y todavía sin resolver.

Es el estado del algoritmo. Enumerar tenía un punto, el gradiente tenía un
punto, simplex tenía un vértice: **éste tiene un conjunto.**
:::

::: definition {#opt-poda title="Podar"}
**Podar** es cerrar una rama sin abrir lo que cuelga de ella. Hay tres formas de
cerrar, y solo dos son podas:

| Cierre | Cuándo | ¿Poda? |
|---|---|---|
| Por infactibilidad | La relajación no tiene ni un punto | sí |
| Por cota | $\bar z \le$ la mejor solución que ya tienes | sí |
| Por solución entera | La relajación salió entera: no hay nada mejor debajo | no: la resolvió |
:::

El tercer renglón se confunde con una poda y no lo es: ahí la rama **se terminó
de resolver**, no se descartó.

### El algoritmo

::: figure {#opt-flujo-ramificar title="Ramificar y acotar, paso a paso"}
![Diagrama de flujo de doce nodos: entrada, inicialización, la lista de nodos vivos, el ciclo que saca un nodo, lo descarta si su relajación es infactible o si su cota no supera a la mejor solución, lo guarda si salió entera y si no lo parte en dos, y la salida cuando la lista se vacía](../_assets/opt-flujo-ramificar.svg)
:::

Las etiquetas `[Ln]` son las líneas de aquí abajo:

```text
INPUT   max cᵀx  s.a.  Ax ≤ b,  l ≤ x ≤ u,  x entera.
OUTPUT  un óptimo x* y su valor, o «no hay factibles».

 1  mejor ← −∞ ;  x* ← «ninguno»
 2  L ← { el problema original }        ▷ nodos vivos
 3  while L ≠ { }
 4      P ← saca un nodo de L
 5      if la relajación de P no es factible: continue
 6      x̄, z̄ ← óptimo de la relajación de P
 7      if z̄ ≤ mejor: continue                 ▷ poda por cota
 8      if x̄ es entera
 9          mejor ← z̄ ;  x* ← x̄ ;  continue    ▷ cierra
10      elige j con x̄ⱼ fraccionaria
11      mete en L  xⱼ ≤ ⌊x̄ⱼ⌋  y  xⱼ ≥ ⌈x̄ⱼ⌉
12  end while
13  return x*, mejor      ▷ x* = «ninguno» si no hubo factibles
```

**La línea 5 supone la caja finita**, igual que enumerar. Si una variable no
tiene cota superior, la relajación puede salir **no acotada**, que no es lo mismo
que infactible: tratarla como infactible haría que el algoritmo contestara «no
hay factibles» a un problema que sí tiene respuesta.

**La línea 6 llama a otro algoritmo.** Es la primera vez que pasa en el curso:
resolver la relajación **es** correr simplex. Ramificar y acotar no sabe
resolver nada por sí mismo; sabe **decidir qué vale la pena resolver**.

### Dos reglas que el pseudocódigo deja abiertas

Sin ellas el árbol no tiene cinco nodos: tiene los que le toquen.

| Línea | Lo que no dice | Lo que usamos aquí |
|---|---|---|
| 4 | **Cuál** nodo sale de la lista | El último que entró |
| 11 | En qué orden entran los hijos | Primero el del $\le$, para que abra el del $\ge$ |
| 10 | **Cuál** variable fraccionaria | La primera, en el orden en que están escritas |

Y una que no es de estilo: en la línea 7 la comparación va **antes** de revisar
si $\bar x$ es entera. Al revés, un nodo entero peor que la mejor solución la
sobrescribiría.

En Python, el mismo texto:

```python
import numpy as np
from math import floor, ceil
from scipy.optimize import linprog

pila = [(l, u)]                                  # L2
mejor, x_mejor = -np.inf, None                   # L1
while pila:                                      # L3
    lo, hi = pila.pop()                          # L4
    r = linprog(-np.asarray(c), A_ub=A, b_ub=b,
                bounds=list(zip(lo, hi)))
    if not r.success:                            # L5
        continue
    z = -r.fun                                   # L6
    if z <= mejor:                               # L7
        continue
    frac = [j for j in range(len(c))
            if abs(r.x[j] - round(r.x[j])) > 1e-9]
    if not frac:                                 # L8
        mejor, x_mejor = z, r.x.round().astype(int)   # L9
        continue
    j = frac[0]                                  # L10
    baja, sube = list(hi), list(lo)              # L11
    baja[j], sube[j] = floor(r.x[j]), ceil(r.x[j])
    pila.append((lo, baja))                      # el ≤ entra primero
    pila.append((sube, hi))                      # el ≥ sale primero
```

::: definition {#opt-bnb title="Ramificar y acotar"}
**Ramificar y acotar** es este ciclo: acotar cada subproblema con su relajación,
partirlo por una variable fraccionaria cuando la cota promete, y cerrarlo cuando
no.

Entrega el **óptimo global** y un **certificado**: al terminar, toda rama que no
se abrió tenía una cota peor que la respuesta.
:::

## 3 · Los cinco nodos

::: figure {#opt-arbol title="El árbol del taller"}
![Árbol de cinco nodos: la raíz con cota veintiuno se parte en dos ramas; la de la derecha cierra con una solución entera de dieciocho y la de la izquierda se vuelve a partir, y de ahí salen la solución entera de veinte y una poda por cota](../_assets/opt-arbol.svg)
:::

| # | Nodo | Cota | Relajación | Qué pasa |
|---:|---|---:|---|---|
| 1 | raíz | 21 | $(3,\ 3/2)$ | $x_2$ fraccionaria → parte en $x_2\le1$ y $x_2\ge2$ |
| 2 | $x_2 \ge 2$ | 18 | $(2,\ 2)$ | **entera** → mejor = 18 |
| 3 | $x_2 \le 1$ | $62/3 \approx 20.67$ | $(10/3,\ 1)$ | $x_1$ fraccionaria → parte en $x_1\le3$ y $x_1\ge4$ |
| 4 | $x_1 \ge 4$ | 20 | $(4,\ 0)$ | **entera** → mejor = **20** |
| 5 | $x_1 \le 3$ | 19 | $(3,\ 1)$ | $19 \le 20$ → **poda por cota** |

**Respuesta: 4 rovers, ninguna sonda, 20 MB al día** — la misma que enumerar, en
cinco nodos.

**El orden de los números no es de izquierda a derecha.** El 2 está a la derecha
y el 3 a la izquierda porque de la lista sale el último que entró, y el hijo del
$\ge$ entró después.

### Dónde quedaron los veinte planes

Las tres ramas que se cerraron **parten la caja entera**, sin solapes y sin
huecos. Ojo con la unidad: aquí se cuentan **celdas de la caja**, las 20, no los
13 planes factibles —el pie de la figura de las ramas cuenta esos otros—:

| Nodo | Qué tapa | Planes de la caja | Se resolvió con |
|---|---|---:|---|
| 2 | $x_2 \ge 2$ | 10 | una relajación |
| 4 | $x_1 \ge 4$, $x_2 \le 1$ | 2 | una relajación |
| 5 | $x_1 \le 3$, $x_2 \le 1$ | 8 | una relajación |
| | **Total** | **20** | |

Ocho planes enteros cayeron en el nodo 5 y **ninguno se evaluó**: se fueron con
una sola cuenta, porque su cota —19— no alcanzaba. Eso es podar.

> **Lo que este árbol no enseña.** Tiene poda por cota y cierre por solución
> entera, pero **ninguna poda por infactibilidad**: en este problema toda rama
> tiene al menos un punto. Es la tercera forma de cerrar, y aquí no aparece.

## 4 · Qué cuesta

### Los dos factores, otra vez

$$T \;=\; \underbrace{\text{cuántos nodos se abren}}_{\text{de } 1 \text{ a } 2|X|-1} \;\times\; \underbrace{\text{qué cuesta un nodo}}_{\textbf{un problema lineal completo}}$$

### El primer factor no tiene fórmula

Y ésta es la diferencia más honda con enumerar. Allá el conteo salía de las
cotas, antes de correr nada. Aquí **depende de la instancia**:

| | Nodos |
|---|---|
| El mejor caso | 1 — la relajación sale entera de una vez |
| Este problema | 5 |
| El peor caso | $2|X|-1$, con $|X|$ la caja de la página 3 — aquí **39** |

**De dónde sale ese tope.** Cada hoja se queda con un pedazo de la caja, los
pedazos no se solapan, y ninguno queda vacío: hay a lo más $|X|$ hojas, y un
árbol binario con $L$ hojas tiene $2L-1$ nodos. Con variables **0/1** eso es el
$2^{n+1}-1$ que se suele citar; con enteras generales **no hay tope que dependa
solo de $n$**, porque la misma variable se puede volver a partir más abajo.

Léelo despacio, porque es incómodo: **en el peor caso este algoritmo abre casi el
doble de nodos que candidatos tiene la caja**, y cada nodo cuesta un problema
lineal. Ramificar y acotar puede ser mucho peor que enumerar.

**Podar no cambia la clase de complejidad.** El problema sigue siendo NP-duro, y
existen instancias donde el árbol se abre entero. Lo que cambia es la
**constante y la suerte**, y en la práctica eso es casi todo.

### El segundo factor es mucho más caro

| Algoritmo | Un paso es | Cuesta |
|---|---|---|
| Enumerar | Revisar un candidato | $(m+1)n$ productos |
| Ramificar | Resolver un nodo | **Un problema lineal completo**: la relajación, con los pivotes de simplex |

> **Cinco nodos contra veinte candidatos no es cuatro veces más rápido.**
> Comparar los conteos mezcla unidades, igual que comparar hojas con nodos. Un
> candidato es un producto punto; un nodo es un algoritmo completo.

**En el taller, enumerar gana en el reloj.** Veinte productos punto valen menos
que cinco llamadas a simplex. Ramificar y acotar no está hecho para 20
candidatos: está hecho para cuando la caja tiene $10^{12}$, y ahí la
comparación se invierte de golpe. Medir los dos en el mismo problema es lo único
que zanja la discusión.

### Qué lo hace crecer

| Si agregas… | Qué le pasa |
|---|---|
| Una variable, $n \to n+1$ | El árbol **puede** duplicarse — pero solo si la poda falla |
| Una restricción, $m \to m+1$ | Cada nodo cuesta un poco más… y suele podar **antes** |
| Una cota más floja (un $M$ grande) | La relajación se aleja del entero, poda menos, y el árbol crece |

El último renglón es el que conecta con la página 2: por eso el enlace del costo
fijo se escribe $x_1 \le 4y$ y no $x_1 \le 1000y$. Los dos modelos son
correctos; **uno se resuelve y el otro no.**

### Cuándo sí, cuándo no

| Úsalo | Evítalo |
|---|---|
| Cuando la caja no cabe en la memoria ni en el día | Cuando hay diez candidatos: enumerar es más simple y más rápido |
| Cuando necesitas el óptimo **y** su certificado | Cuando te basta una solución buena y tienes prisa |
| Cuando el modelo está bien apretado | Cuando el modelo tiene grandes constantes sueltas |

Y para lo que sigue: **esto es lo que hay dentro de `scipy.optimize.milp`, de
Gurobi y de CPLEX.** Ahí encima le montan cortes, heurísticas y presolve, pero el
esqueleto es el de arriba.

## Lo que hay que llevarse

- La relajación no resuelve el problema: **da una cota**, y la cota es lo único
  que permite descartar sin mirar.
- Partir por $\lfloor \bar x_j\rfloor$ y $\lceil \bar x_j\rceil$ no pierde
  soluciones, porque entre las dos no hay ningún entero.
- Enumerar mira los 20 planes uno por uno y no puede parar; ramificar cierra los
  20 con **cinco relajaciones**, y demuestra que no hacía falta mirarlos. Cada
  paso suyo cuesta mucho más: por eso gana en grande y pierde en chico.
