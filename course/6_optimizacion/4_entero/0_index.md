---
id: optimizacion-entera
title: "Clase 4 · Cuando las piezas no se parten"
nav_title: Entero
summary: "Un taller que fabrica cosas que no se pueden dejar a medias. Qué cambia al escribir el modelo, por qué los métodos anteriores no cierran, y el primer método que sí: mirarlos todos."
status: ready
estimated_time: 50m
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
| 1 | La bitácora | Lee y analiza. Tú escribes el modelo; la página no lo escribe por ti |
| 2 | El modelo | Lo formaliza, lo cambia dos veces, y dice por qué lo anterior no cierra |
| 3 | Enumerar | El primer método que sí funciona, con su costo |

- [[la-bitacora-del-taller|1 · La bitácora del taller]]
- [[el-modelo-del-taller|2 · El modelo, escrito]]
- [[enumerar|3 · Enumerar]]

## Cómo se trabaja esta clase

La página 1 termina pidiéndote que escribas el modelo **antes** de ver el de la
página 2, y plantea dos variantes cuya respuesta está plegada en la página
siguiente. Eso es el trabajo de la clase: no hay forma de aprender a modelar
leyendo modelos ya escritos.

## Qué no cubre

No vas a ver todavía cómo se resuelve esto sin mirar todos los planes —enumerar
funciona con 20 candidatos y no con un millón—, ni variables mixtas, ni los
métodos que usan la relajación para descartar sin probar. Esta clase llega hasta
el método tosco y su factura.

Empieza por [[la-bitacora-del-taller|la bitácora del taller]].
