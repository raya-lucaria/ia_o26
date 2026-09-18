---
id: optimizacion-entera
title: "Clase 4 · Cuando las piezas no se parten"
nav_title: Entero
summary: "Un taller que fabrica cosas que no se pueden dejar a medias. Qué cambia al escribir el modelo, por qué los métodos anteriores no cierran, y el primer método que sí: mirarlos todos."
status: ready
estimated_time: 100m
tags: [optimizacion, modelado, entera]
prerequisites: [optimizacion-lineal]
---

# Clase 4 · Cuando las piezas no se parten

Las tres clases anteriores se apoyaron en una licencia que nadie discutió: que
una fracción de pieza significa algo. Media hora de trabajo, medio filtro a
medio armar. En la impresora era razonable.

Aquí no. Media sonda no es media respuesta: es una sonda que no transmite. El
modelo cambia en **una sola línea** —el dominio— y con esa línea se cae casi todo
el instrumental de las clases 2 y 3.

## El episodio

El taller de la nave fabrica **rovers** y **sondas de superficie** con lo que
queda de aleación y de horas de calibración. Dos variables, dos restricciones, y
la regla de que las cosas se fabrican enteras o no se fabrican.

::: table {#opt-el-taller title="Lo que consume y lo que da cada equipo"}
| Equipo | Aleación (kg) | Calibración (h) | Transmite (MB/día) |
|---|---:|---:|---:|
| Rover | 6 | 1 | 5 |
| Sonda | 4 | 2 | 4 |
| **Disponible** | **24** | **6** | maximizar |
:::

## Las páginas

| # | Página | Qué hace |
|---|---|---|
| 1 | La bitácora | Las preguntas que hay que hacerle, y cómo se contesta cada una. **El modelo lo escribes tú** |
| 2 | El modelo | Contesta la lectura, formaliza, y **tres variantes que obligan a inventar variables nuevas** |
| 3 | Enumerar | El primer método que sí funciona, con su costo |
| 4 | Ramificar y acotar | El algoritmo que descarta planes que nunca miró, y prueba que puede |

- [[la-bitacora-del-taller|1 · La bitácora del taller]]
- [[el-modelo-del-taller|2 · El modelo, escrito]]
- [[enumerar|3 · Enumerar]]
- [[ramificar-y-acotar|4 · Ramificar y acotar]]

## Cómo se trabaja esta clase

La página 1 **no escribe el modelo**: da las preguntas, dice cómo se contesta
cada una —el dominio con más detalle, porque es la nueva— y te pide el tuyo en
papel antes de pasar de página. Las respuestas, incluidas las de sus tres
variantes, están en la página 2. Eso es el trabajo de la clase: no hay forma de
aprender a modelar leyendo modelos ya escritos.

## El notebook de la clase 4

La función `enumerar` es el pseudocódigo de la página 3, línea por línea, y
recibe cualquier modelo entero: le pasas `c`, `A`, `b` y las cotas, y te
devuelve el óptimo con cuántos candidatos miró. Trae resueltos el taller y las
**tres variantes** de la página 2, las contrasta contra `scipy.optimize.milp`, y
cierra midiendo cómo crece el costo al mover $n$ y al mover $m$ por separado.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/6_optimizacion/_assets/04_taller_entero.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Dónde vive.** El archivo está en este repositorio, en
`course/6_optimizacion/_assets/04_taller_entero.ipynb`. Si prefieres correrlo en
tu máquina, necesitas `numpy`, `scipy` y `matplotlib`.

**Cuándo.** Después de leer las tres páginas. La última celda te pide modelar una
bitácora nueva y comprueba tu respuesta sola.

## Qué no cubre

No vas a ver variables mixtas —unas enteras y otras continuas—, ni planos de
corte, ni las heurísticas que los solucionadores usan para encontrar pronto una
solución buena. Tampoco el mapa de qué algoritmo le toca a cada familia, que
cierra la unidad y todavía no está escrito.

Empieza por [[la-bitacora-del-taller|la bitácora del taller]].
