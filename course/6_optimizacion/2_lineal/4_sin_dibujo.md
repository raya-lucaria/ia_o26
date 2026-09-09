---
id: sin-dibujo
title: Sin dibujo
nav_title: En tres variables
summary: "El mismo método sobre el poliedro de tres piezas, donde nadie puede ver la figura. Qué entrega, y qué cuesta."
status: ready
estimated_time: 12m
tags: [optimizacion, simplex, costo]
---

# Sin dibujo

**¿Y si el poliedro tiene tres dimensiones y nadie lo puede ver?**

Simplex ya está descrito, y comprobado donde había dibujo. Ahora se suelta donde
no lo hay.

## 1 · El mismo método, con el sello

Nada cambia, y esa es la noticia. Los vecinos de cada vértice salen de la tabla
de los ocho de [[cuando-se-acaba-el-dibujo|Cuando se acaba el dibujo]]: son los
que comparten con él **dos restricciones activas**.

::: table {#opt-traza-sello title="Simplex sobre el poliedro con sello, desde el origen"}
| Estoy en | Vale | Vecinos, y lo que valen | Me voy a |
|---|---:|---|---|
| $(0,0,0)$ | 0 | $(9,0,0)=36$ · $(0,0,6)=30$ · $(0,9,0)=27$ | $(9,0,0)$ |
| $(9,0,0)$ | 36 | $(\tfrac92,0,\tfrac92)=\tfrac{81}{2}$ · $(8,2,0)=38$ · $(0,0,0)=0$ | $(\tfrac92,0,\tfrac92)$ |
| $(\tfrac92,0,\tfrac92)$ | $\tfrac{81}{2}$ | $(5,2,3)=41$ · $(9,0,0)=36$ · $(0,0,6)=30$ | $(5,2,3)$ |
| $(5,2,3)$ | **41** | $(\tfrac92,0,\tfrac92)=\tfrac{81}{2}$ · $(8,2,0)=38$ · $(2,8,0)=32$ | — |
:::

Tres pivotes, cuatro vértices de ocho, y ni un dibujo. Cada renglón se revisa
comparando qué se acaba en cada vértice, que es lo único que hizo falta.

Que en el segundo paso gane $(\tfrac92,0,\tfrac92)$ a $(8,2,0)$ por dos
créditos y medio es lo que hace que el método valga: a ojo nadie hubiera
apostado por el plan de coordenadas partidas. Y ese paso es un plan de **cuatro
filtros y medio y cuatro sellos y medio**. No es la respuesta: es una parada del
camino, y aquí las piezas se pueden partir porque el modelo lo permite. Cuándo
no se puede es el asunto de la clase 4.

Las cuatro preguntas anotadas al margen del pseudocódigo quedan contestadas de
un tirón:

| Dónde estoy | Hacia dónde | Cuánto avanzo | ¿Paro? |
|---|---|---|---|
| En un vértice | Hacia los vecinos que mejoran | Hasta el mejor de ellos | Cuando ninguno mejora |

## 2 · Qué entrega, y qué cuesta

Entrega un óptimo **global y exacto**, no una aproximación, y de regalo la
información para construir su certificado. De eso vive la página siguiente.

**Un paso** cuesta mirar sus vecinos —$n$ exactos si ningún vértice es
degenerado, como aquí; más si los hay— y cada vecino es resolver un sistema de
$n$ ecuaciones con $n$ incógnitas. **Cuántos pasos** es la pregunta abierta:
pocos en la práctica, y hay problemas construidos a propósito para que sean
exponencialmente muchos.

Y ahí se termina, porque el resto ya está publicado: la unidad de complejidad
cuenta que [[las-clases|la programación lineal está en P aunque el simplex no sea polinomial]], y el [[zoologico-de-problemas|zoológico de problemas]] lleva su fila.

## 3 · Tu turno

::: exercise {#opt-ej-sello title="Escríbelo y da un paso"}
1. Escribe la terna $(c, A, b)$ del modelo con sello, de memoria si puedes.
2. Arranca simplex en $(0,0,6)$ —seis sellos y nada más— y da **un** paso. ¿A
   dónde llegas?
:::

::: hint {#opt-pista-sello of="opt-ej-sello" title="Por dónde empezar"}
Para la primera, no inventes el orden: la tabla de las tres piezas de
[[cuando-se-acaba-el-dibujo|Cuando se acaba el dibujo]] ya está puesta como
$A$, un renglón por recurso y una columna por pieza. El renglón de créditos es
$c$, y $b$ son las cantidades disponibles.

Para la segunda no hace falta calcular nada. Empieza por localizar qué se acaba
en $(0,0,6)$, busca en la tabla de los ocho los vértices que compartan dos de
esas tres cosas, y hasta entonces compara valores.
:::

::: answer {#opt-resp-sello of="opt-ej-sello"}
$$c=(4,3,5),\quad A=\begin{pmatrix}1&1&1\\2&1&2\\1&2&3\end{pmatrix},\quad b=\begin{pmatrix}10\\18\\18\end{pmatrix}$$

En $(0,0,6)$ están activas la energía, $x_1=0$ y $x_2=0$. Comparten dos de esas
tres $(0,0,0)$ con 0, $(0,9,0)$ con 27 y $(\tfrac92,0,\tfrac92)$ con
$\tfrac{81}{2}$: son los tres vecinos.

Donde estoy vale 30, así que el único que mejora es $(\tfrac92,0,\tfrac92)$, y
el paso lleva ahí. Es la misma parada de coordenadas partidas por la que pasa la
traza que empieza en el origen, llegando por otro lado.
:::

## Lo que hay que llevarse

- El método no necesitó ver la figura: le bastó saber quién es vecino de quién,
  y eso se lee en una tabla.
- Da el óptimo exacto y no una aproximación; lo que no promete es cuántos
  vértices va a recorrer para llegar a él.
- Un vértice puede tener coordenadas partidas, y eso no es un fallo del método:
  es lo que el modelo le permitió.

Falta cobrar lo que el óptimo dice de cada recurso:
[[cuanto-vale-una-hora-mas|la página siguiente]].
