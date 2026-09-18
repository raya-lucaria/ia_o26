---
id: ramificar-y-acotar
title: Ramificar y acotar
nav_title: Ramificar
summary: "El algoritmo que no mira todos los planes y aun así demuestra que su respuesta es la mejor: parte el problema en dos, y descarta grupos enteros de planes con una sola cuenta."
status: ready
estimated_time: 34m
tags: [optimizacion, entera, algoritmos]
---

# Ramificar y acotar

**¿Cómo descarto un plan que nunca miré?**

Vienes de [[enumerar|enumerar]] · Aquí: el algoritmo que sí escala.

Enumerar encontró el ganador en el candidato 17 de 20 **y siguió tres más**. No
le faltaba suerte: le faltaba un **argumento** para parar. Este algoritmo lo
tiene, y se arma con tres piezas: una cota, un corte, y una manera de llevar la
cuenta.

## 1 · La cota

::: definition {#opt-relajacion title="Relajación lineal"}
La **relajación** de un problema entero es el mismo problema **sin** la línea
$x\in\mathbb{Z}$:

$$\max\; c^{\mathsf T}x \quad\text{s.a.}\quad Ax \le b,\quad l \le x \le u$$

Ya no es un problema entero: es uno lineal, de los de la clase 2, y lo resuelve
simplex.
:::

En el taller, la relajación vale **21**, en el punto $(3,\ 3/2)$.

### Por qué ese número es un techo

Primero la regla, que no es de optimización sino de conjuntos:

> Si $A \subseteq B$, entonces $\max B \ge \max A$. **Agregar opciones nunca baja
> el máximo.**

Con números sueltos: si $A = \{12,\ 19,\ 20\}$ y le agregas el 21, el máximo sube
a 21. Si le agregas el 7, se queda en 20. Lo que no puede hacer es **bajar**.

Ahora, por qué aquí $A \subseteq B$. Un plan entero factible cumple $Ax \le b$ y
$l \le x \le u$. La relajación pide **exactamente eso y nada más** —solo deja de
exigir $x \in \mathbb{Z}$—, así que **ningún plan entero se cae**: todos siguen
estando.

Con $A$ = los 13 planes enteros y $B$ = todos los puntos del polígono:

| Plan | ¿Entero? | ¿Está en la relajación? | Vale |
|---|---|---|---:|
| $(4,\ 0)$ | sí | sí | 20 |
| $(3,\ 1)$ | sí | sí | 19 |
| $(2,\ 2)$ | sí | sí | 18 |
| $(3,\ 3/2)$ | **no**: media sonda | **sí** | **21** |

Los tres primeros están en los dos conjuntos. El cuarto **solo está en el
segundo**, y es el que manda. Por eso

$$z_{\text{relajación}} \;\ge\; z_{\text{entero}}, \qquad\text{y aquí}\quad 21 \ge 20.$$

::: figure {#opt-relajacion-corte title="La cota que da la relajación"}
![El polígono del taller con los trece planes enteros que caben dentro, el óptimo continuo marcado con una cruz sobre el borde y el mejor plan entero resaltado en la esquina de abajo a la derecha](../_assets/opt-relajacion-corte.svg)
:::

::: definition {#opt-cota-relajacion title="Cota superior"}
Una **cota superior** de un problema es un número que **ninguno** de sus planes
enteros puede superar, calculado **sin** conocer el mejor de ellos.

Y sirve para una cosa: si la cota de un problema no supera a una solución que ya
tienes en la mano, **ese problema no hace falta resolverlo**.
:::

> **Cuidado.** La cota **no es la respuesta**. «Tres rovers y media sonda» no
> existe. Lo único que dice el 21 es que nadie va a pasar de ahí.

## 2 · Partir el problema

La relajación contestó $x_2 = 3/2$, que no es un plan. Hay que **obligar a $x_2$
a decidirse**: o es 1 o menos, o es 2 o más. Ésa es la regla general:

$$x_j \le \lfloor \bar x_j \rfloor \qquad\text{y}\qquad x_j \ge \lceil \bar x_j \rceil$$

Aquí, $x_2 \le 1$ y $x_2 \ge 2$.

::: figure {#opt-ramas title="Partir no pierde ninguna solución"}
![El mismo polígono partido en dos por una franja horizontal entre uno y dos, que no contiene ningún punto entero; arriba la mitad de x dos mayor o igual que dos y abajo la de x dos menor o igual que uno](../_assets/opt-ramas.svg)
:::

El dibujo dice dos cosas a la vez:

- **No se pierde ningún plan.** Entre $\lfloor \bar x_j \rfloor$ y
  $\lceil \bar x_j \rceil$ no hay ningún entero, así que la franja que queda
  fuera está vacía. Partir es exhaustivo, no una apuesta.
- **Sí se pierde el punto de la cota.** $(3,\ 3/2)$ no sobrevive a ninguna de las
  dos mitades. Por eso cada corte obliga a la relajación a contestar algo
  distinto, y el método avanza en vez de dar vueltas.

Cada mitad es un problema completo —mismo objetivo, mismas restricciones, cotas
más apretadas—, y tiene nombre:

::: definition {#opt-subproblema title="Subproblema"}
Un **subproblema** es el mismo modelo con las cotas más apretadas: mismo $c$,
misma $A$, mismo $b$, y un $l \le x \le u$ más chico.

Por eso todo lo que sabes del original sigue valiendo dentro de él — incluida su
relajación, que se calcula igual.
:::

### Los subproblemas forman un árbol

Partir uno da dos, y a esos dos se les puede volver a partir. Lo que se va
formando es un árbol binario, y le damos los nombres de siempre. Esto es un
recordatorio, no vocabulario nuevo:

| Palabra | Aquí significa |
|---|---|
| **raíz** | El problema original |
| **nodo** | Un subproblema |
| **hijos** | Los dos subproblemas que salen de partir uno |
| **hoja** | Un nodo que no se partió |
| **rama** | Un nodo **con todo lo que cuelga de él** |
| **abrir** un nodo | Resolver su relajación |

::: figure {#opt-arbol-vocabulario title="Cómo se llama cada parte"}
![Árbol genérico de tres niveles: una raíz arriba, dos hijos debajo, y el hijo de la izquierda con dos hijos propios; un recuadro punteado encierra al hijo de la izquierda con todo lo que cuelga de él](../_assets/opt-arbol-vocabulario.svg)
:::

**Nodo y subproblema son la misma cosa**, con dos nombres: *subproblema* cuando
hablamos del modelo, *nodo* cuando hablamos del dibujo.

## 3 · El algoritmo

Ya está todo lo que hace falta: una cota para descartar, un corte para avanzar y
un árbol donde poner lo que se va abriendo. Falta la contabilidad.

::: definition {#opt-nodos-vivos title="Lista de nodos vivos"}
La **lista de nodos vivos** son los subproblemas ya creados y todavía sin
resolver.

Es el estado del algoritmo, y es lo que lo hace distinto de todo lo anterior:
simplex estaba en un vértice, el gradiente en un punto, enumerar en un
candidato. **Éste no está en un lugar: tiene un conjunto.**
:::

::: definition {#opt-poda title="Cerrar y podar"}
Un nodo se **cierra** cuando ya no hay que abrir nada debajo de él. Hay tres
formas, y solo dos son podas:

| Cierre | Cuándo | ¿Poda? |
|---|---|---|
| Por infactibilidad | La relajación del nodo no tiene ni un punto | sí |
| Por cota | Su cota no supera a la mejor solución que ya tienes | sí |
| Por solución entera | Su relajación salió entera: nada debajo puede ser mejor | no: la resolvió |

**Podar** es cerrar una rama sin abrir lo que cuelga de ella.
:::

El tercer renglón se confunde con una poda y no lo es: ahí el nodo **se terminó
de resolver**, no se descartó.

::: figure {#opt-flujo-ramificar title="Ramificar y acotar, paso a paso"}
![Diagrama de flujo de doce pasos: entrada, inicialización, la lista de nodos vivos, el ciclo que saca un nodo, lo descarta si su relajación es infactible o si su cota no supera a la mejor solución, lo guarda si salió entera y si no lo parte en dos, y la salida cuando la lista se vacía](../_assets/opt-flujo-ramificar.svg)
:::

Las etiquetas `[Ln]` de cada paso son las líneas de aquí abajo:

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

Dos cosas que hay que decir antes de correrlo.

**La línea 6 llama a otro algoritmo.** Es la primera vez que pasa en el curso:
resolver la relajación **es** correr simplex. Ramificar y acotar no sabe resolver
nada por sí mismo; sabe **decidir qué vale la pena resolver**.

**La línea 5 supone la caja finita**, igual que enumerar. Si una variable no
tiene cota superior, la relajación puede salir **no acotada**, que no es lo mismo
que infactible: tratarla como infactible haría que el algoritmo contestara «no
hay factibles» a un problema que sí tiene respuesta.

### Tres decisiones que el pseudocódigo deja abiertas

Sin ellas, el árbol del taller no tiene cinco nodos: tiene los que le toquen.

| Línea | Lo que no dice | Lo que usamos aquí |
|---|---|---|
| 4 | **Cuál** nodo sale de la lista | El último que entró |
| 11 | En qué orden entran los hijos | Primero el del $\le$, para que abra el del $\ge$ |
| 10 | **Cuál** variable fraccionaria | La primera, en el orden en que están escritas |

Y una cuarta que no es de estilo: en la línea 7 la comparación va **antes** de
revisar si $\bar x$ es entera. Al revés, un nodo entero peor que la mejor
solución la sobrescribiría.

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
**Ramificar y acotar** es este ciclo: acotar cada nodo con su relajación,
partirlo por una variable fraccionaria cuando la cota promete, y cerrarlo cuando
no.

Entrega el **óptimo global** y un **certificado**: al terminar, toda rama que no
se abrió tenía una cota peor que la respuesta.
:::

De repaso, qué hace cada pieza del modelo dentro del ciclo:

| Pieza | Sirve para |
|---|---|
| La relajación de un nodo | **Acotar** lo mejor que puede haber en esa rama |
| ¿La solución salió entera? | **Cerrar** el nodo |
| La mejor solución hasta ahora | **Podar** lo que ya no puede ganar |
| Una variable fraccionaria | **Partir** en dos |

## 4 · El árbol del taller, y su factura

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

Las tres hojas **parten la caja entera**, sin solapes y sin huecos. Ojo con la
unidad: aquí se cuentan **celdas de la caja**, las 20, no los 13 planes
factibles:

| Nodo | Qué tapa | Celdas | Se resolvió con |
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

### Los dos factores

$$T \;=\; \underbrace{\text{cuántos nodos se abren}}_{\text{de } 1 \text{ a } 2|X|-1} \;\times\; \underbrace{\text{qué cuesta un nodo}}_{\textbf{un problema lineal completo}}$$

**El primero no tiene fórmula**, y ésa es la diferencia más honda con enumerar.
Allá el conteo salía de las cotas antes de correr nada; aquí depende de la
instancia:

| | Nodos |
|---|---|
| El mejor caso | 1 — la relajación sale entera de una vez |
| Este problema | 5 |
| El peor caso | $2|X|-1$, con $|X|$ la caja de la página 3 — aquí **39** |

**De dónde sale ese tope.** Cada hoja se queda con un pedazo de la caja, los
pedazos no se solapan y ninguno queda vacío: hay a lo más $|X|$ hojas, y un árbol
binario con $L$ hojas tiene $2L-1$ nodos. Con variables **0/1** eso es el
$2^{n+1}-1$ que se suele citar; con enteras generales **no hay tope que dependa
solo de $n$**, porque la misma variable se puede volver a partir más abajo.

Léelo despacio, porque es incómodo: **en el peor caso este algoritmo abre casi el
doble de nodos que candidatos tiene la caja**, y cada nodo cuesta un problema
lineal. Ramificar y acotar puede ser mucho peor que enumerar.

**Podar no cambia la clase de complejidad.** El problema sigue siendo NP-duro, y
existen instancias donde el árbol se abre entero. Lo que cambia es la constante y
la suerte, y en la práctica eso es casi todo.

### El segundo factor es mucho más caro

| Algoritmo | Un paso es | Cuesta |
|---|---|---|
| Enumerar | Revisar un candidato | $(m+1)n$ productos |
| Ramificar | Abrir un nodo | **Un problema lineal completo**: la relajación, con los pivotes de simplex |

> **Cinco nodos contra veinte candidatos no es cuatro veces más rápido.**
> Comparar los conteos mezcla unidades, igual que comparar hojas con nodos. Un
> candidato es un producto punto; un nodo es un algoritmo completo.

**En el taller, enumerar gana en el reloj.** Veinte productos punto valen menos
que cinco llamadas a simplex. Ramificar y acotar no está hecho para 20
candidatos: está hecho para cuando la caja tiene $10^{12}$, y ahí la comparación
se invierte de golpe. Medir los dos en el mismo problema es lo único que zanja la
discusión.

### Qué lo hace crecer

| Si agregas… | Qué le pasa |
|---|---|
| Una variable, $n \to n+1$ | El árbol **puede** duplicarse — pero solo si la poda falla |
| Una restricción, $m \to m+1$ | Cada nodo cuesta un poco más… y suele podar **antes** |
| Una cota más floja (un $M$ grande) | La relajación se aleja del entero, poda menos, y el árbol crece |

El último renglón es el que conecta con la página 2: por eso el enlace del costo
fijo se escribe $x_1 \le 3y$ y no $x_1 \le 1000y$. Los dos modelos son correctos;
**uno se resuelve y el otro no.**

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
  soluciones, porque entre las dos mitades no hay ningún entero.
- Enumerar mira los 20 planes uno por uno y no puede parar; ramificar cierra los
  20 con **cinco relajaciones**. Cada paso suyo cuesta mucho más: por eso gana en
  grande y pierde en chico.
