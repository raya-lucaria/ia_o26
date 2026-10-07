---
id: juegos-leer-y-escribir
title: "Clase 1 · Leer y escribir el juego"
nav_title: Leer y escribir
summary: "Antes de calcular una jugada hay que escribir el juego: quién mueve, qué puede hacer, cómo cambia el tablero, cuándo termina y cuánto vale terminar así."
status: ready
estimated_time: 110m
tags: [juegos, modelado]
prerequisites: [juegos]
---

# Clase 1 · Leer y escribir el juego

**En esta clase no se calcula ninguna jugada.** Se leen unas reglas
explicadas con prisa, se ordenan y se escriben como un modelo que una
computadora podría recorrer. Calcular la mejor jugada empieza en la clase 2.

## Qué vas a poder hacer al terminar esta clase

- Separar en unas reglas lo que sobra, lo que falta, lo ambiguo y lo que
  se repite.
- Escribir cualquier juego por turnos con siete piezas, cada una con su
  dominio: estados, estado inicial, finales, jugador de turno, acciones,
  transición y utilidad.
- Decidir qué tiene que guardar un estado, y comprobar que no falta nada.
- Construir el grafo de un juego a partir de esas piezas y leer en él una
  partida.
- Distinguir el árbol de partidas del grafo de estados, y explicar qué
  recibe un algoritmo: el grafo dibujado o las reglas para generarlo.
- Diagnosticar un juego y decir qué modelo le corresponde.
- Decir qué significa que un jugador sea racional, respecto a qué, y qué
  no significa.
- Distinguir un valor, una jugada y una estrategia.

## Antes de leer: juega

Busca a alguien, dibuja un tablero de 3×3 y pon tres monedas de un tipo en
la fila de abajo y tres de otro en la de arriba. Cada moneda es un peón: en
su turno, un jugador avanza un peón una casilla hacia el rival si está
vacía, o lo mueve una casilla en diagonal hacia delante para capturar uno
rival. Gana quien llega a la fila del otro.

Antes de empezar, **decidan entre ustedes** quién empieza y qué pasa si a
alguien le toca y no puede mover. Anótenlo y jueguen **tres partidas**.

Anota quién empezó y quién ganó cada vez. Esas decisiones y esos resultados
vuelven en la primera página y en la clase 2.

## Recorrido

Cuatro páginas, en orden, y una tarea de refuerzo al final.

::: table {#jue-ruta-1 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Leer el reglamento | Qué dicen de verdad unas reglas explicadas con prisa | 15m |
| 2 | Escribir el juego | Las siete piezas de cualquier juego por turnos, una partida escrita con ellas, qué es ser racional y el problema de la unidad | 45m |
| 3 | El juego como grafo | El grafo completo, árbol contra grafo y qué recibe y qué genera cada método | 30m |
| 4 | Diagnosticar el juego | Qué tipo de juego es y qué modelo le toca | 20m |
| 5 | Tarea de refuerzo | Escribir gato desde cero y cambiar una regla de hexapawn | 40m, aparte |
:::

1. [[leer-el-reglamento|Leer el reglamento]]
2. [[escribir-el-juego|Escribir el juego]]
3. [[el-juego-como-grafo|El juego como grafo]]
4. [[diagnosticar-el-juego|Diagnosticar el juego]]
5. [[tarea-leer-y-escribir|Tarea de refuerzo]]

## Qué no cubre esta clase

No calculamos el valor de ninguna posición ni decimos quién gana con juego
perfecto. Tampoco aparecen todavía juegos con azar o con jugadas
simultáneas: la página 4 solo los diagnostica y dice en qué clase se
resuelven.

Empieza por [[leer-el-reglamento|leer el reglamento]].
