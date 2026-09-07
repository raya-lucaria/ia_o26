---
id: patrones-lineales
title: Patrones lineales
nav_title: Patrones
summary: "Casi toda frase de un problema real cae en uno de tres moldes. Ésta es la tabla de traducción, y la trampa de signos que espera al pasar al código."
status: ready
estimated_time: 15m
tags: [optimizacion, modelado, restricciones, signos]
---

# Patrones lineales

**¿Cómo se escribe como desigualdad una frase que no habla de un recurso?**

El problema de la impresora ya está modelado, resuelto y certificado. Pero se
modeló con una ventaja que no vas a volver a tener: **sus tres restricciones eran
del mismo tipo**, las tres decían «hay tanto de esto y cada pieza gasta tanto».

Los problemas de verdad mezclan tipos. Aparecen frases que no hablan de ningún
recurso —«al menos tres», «a lo más cuatro», «por cada uno de éstos, dos de
aquéllos»— y hay que saber en qué se convierten sin pensarlo mucho.

Son **tres moldes**, y casi todo cae en uno de ellos.

## 1 · Los tres moldes

::: definition {#opt-recurso title="Restricción de recurso"}
Una **restricción de recurso** dice que algo **se consume y se agota**: cada
unidad de cada variable gasta una cantidad fija, y el total no puede pasar de lo
que hay.

Su forma es una suma de consumos a la izquierda y la disponibilidad a la derecha,
con $\le$. Las 3 del problema de la impresora son de este tipo.
:::

::: definition {#opt-cota title="Cota sobre una variable"}
Una **cota** es un piso o un techo **directo sobre una sola variable**: «al menos
3 filtros», «a lo más 4 celdas».

Se distingue del recurso en que no hay nada que se reparta entre las variables:
la desigualdad menciona una sola.
:::

::: definition {#opt-proporcion title="Restricción de proporción"}
Una **restricción de proporción** compara **una variable con otra**: «por cada
celda, al menos 2 filtros».

Casi siempre llega escrita con las variables en lados distintos, y hay que
juntarlas de un solo lado para que quede en forma estándar.
:::

::: table {#opt-patrones title="La frase, la desigualdad y el molde"}
| Frase | Desigualdad | Molde |
|---|---|---|
| «cada pieza se lleva 1 hora y quedan 10» | $x_1 + x_2 \le 10$ | recurso |
| «el filtro se lleva 2 kg, la celda 1, y hay 18» | $2x_1 + x_2 \le 18$ | recurso |
| «al menos 3 filtros» | $x_1 \ge 3$ | cota |
| «a lo más 4 celdas» | $x_2 \le 4$ | cota |
| «por cada celda, al menos 2 filtros» | $x_1 - 2x_2 \ge 0$ | proporción |
:::

Las cinco filas se reproducen desde la frase sola: **cada frase dice lo que
consume cada pieza**, no solo una. Una frase como «cada filtro consume 2 kg y hay
18» daría $2x_1 \le 18$, y el término de las celdas tendría que salir de otro
lado.

## 2 · La trampa de los signos

Es la fuente número uno de errores al pasar del papel al código. Un **solver** es
un programa que recibe el modelo escrito como números y devuelve la respuesta; el
de esta unidad es `linprog`, de la biblioteca `scipy`.

::: definition {#opt-signos title="La convención de signos"}
| Dónde | Convención |
|---|---|
| Estas notas | La constante va a la derecha. Se admiten $\le$, $\ge$ y $=$ |
| Para entregárselo a un solver | Todo se pasa a $\le$: una $a\cdot x \ge b$ se escribe $-a\cdot x \le -b$ |
| `linprog` | **Minimiza.** Un máximo se resuelve con $-c$, **y al valor que devuelve hay que cambiarle el signo otra vez** |
| Cotas simples sobre una variable | Van en `bounds`, no como restricción extra. En `linprog` la cota por omisión **ya es** $(0,\infty)$ |
:::

> [!WARNING]
> La fila del signo de vuelta no es adorno. Al resolver este modelo con
> `linprog` y el objetivo negado, el resultado trae `fun = -38.0`. Quien copie
> solo «se minimiza $-f$» y compare contra 38 va a ver reventar su comprobación.

## 3 · Tu turno

::: exercise {#opt-ej-cota title="Una restricción más"}
La ingeniera pide una cosa más: «esta vez quiero **al menos 4 celdas**».

Tradúcela, di si cambia la respuesta, y compárala con las **tres últimas filas**
de la tabla de patrones, que son las que no están ya en el modelo.
:::

::: hint {#opt-pista-cota of="opt-ej-cota" title="Por dónde empezar"}
«Al menos» y «a lo más» son la misma clase de frase con el signo al revés.

Y para saber si cambia algo, no resuelvas: mira primero si el óptimo que ya
tienes, $(8,2)$, la cumple.
:::

::: answer {#opt-resp-cota of="opt-ej-cota"}
Es $x_2 \ge 4$, una **cota**.

Y **sí cambia**: $(8,2)$ hace 2 celdas, así que no la cumple. El óptimo se mueve
a $(6,4)$, con 36 créditos en vez de 38. Las 2 celdas extra cuestan 2
créditos.

Las tres últimas filas de la tabla son $x_1\ge3$, $x_1-2x_2\ge0$ y $x_2\le4$, y
$(8,2)$ **las cumple las tres con holgura**, así que ninguna mueve el óptimo. Pero
**las tres sí mueven el polígono**, que es distinto:

| Se añade | Óptimo | Esquinas | Qué le pasa al polígono |
|---|---|---:|---|
| $x_1 \ge 3$ | $(8,2)$, 38 | 4 | mueren $(0,0)$, $(0,9)$ y $(2,8)$; nacen $(3,0)$ y $(3,7)$ |
| $x_1 - 2x_2 \ge 0$ | $(8,2)$, 38 | 4 | mueren $(0,9)$ y $(2,8)$; nace $(20/3,\,10/3)$ |
| $x_2 \le 4$ | $(8,2)$, 38 | 5 | mueren $(0,9)$ y $(2,8)$; nacen $(0,4)$ y $(6,4)$ |

Y ojo con la cuarta fila de la tabla de patrones: es $x_2 \le 4$, y el ejercicio
pide $x_2 \ge 4$. Puestas las dos, obligan a $x_2 = 4$ exacto. Es el mismo número
visto desde los dos lados.
:::

> [!WARNING]
> «Al menos el 40 % de las piezas son filtros» **no** es $x_1 \ge 0.4$.
>
> Escrita como cociente, $\dfrac{x_1}{x_1+x_2} \ge 0.4$, **no es lineal**: hay una
> variable dividiendo. Se arregla multiplicando los dos lados por $x_1+x_2$, que
> es positivo mientras se fabrique algo, y queda $x_1 \ge 0.4(x_1+x_2)$, o sea
> $0.6x_1 - 0.4x_2 \ge 0$. Si no se fabrica nada, la condición se cumple sola y no
> hay nada que dividir.

## Lo que hay que llevarse

- Casi toda restricción que no habla de un recurso es una **cota** sobre una
  variable o una **proporción** entre dos.
- Una restricción que tu solución ya cumple no mueve el óptimo hoy, pero **sí
  mueve el polígono**, y mañana puede morder.
- Las desigualdades se le entregan al solver todas con $\le$, y al máximo hay que
  cambiarle el signo **dos veces**: al entrar y al salir.

## Y ahora, el notebook

Con esto ya puedes leer un problema, escribirlo, dibujarlo y traducir sus frases.
Toca hacerlo con las manos.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/6_optimizacion/_assets/01_impresora_lineal.ipynb)

*Se abre en Google Colab. Si quieres conservar esta página, ábrelo en otra
pestaña: **ctrl + clic** en Windows y Linux, **cmd + clic** en Mac.*

El notebook resuelve este problema con código y **cierra con una bitácora nueva,
del invernadero, que no está resuelta en ninguna página**. Ése es el ejercicio de
la clase. No hay nada que entregar.

El archivo vive en este repositorio, en
`course/6_optimizacion/_assets/01_impresora_lineal.ipynb`.

Lo que falta después es resolver **sin dibujar**, que es lo que hace falta en
cuanto hay más de dos variables.
