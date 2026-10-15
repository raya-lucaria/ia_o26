---
id: juegos-leer-y-escribir
title: "Clase 1 · Leer y escribir el juego"
nav_title: Leer y escribir
summary: "Antes de calcular una jugada hay que escribir el juego: quién mueve, qué puede hacer, cómo cambia el tablero, cuándo termina y cuánto vale terminar así. Y decir qué se busca: el valor V de un estado y el Q de una jugada."
status: ready
estimated_time: 121m
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
- Escribir cualquier juego por turnos con **siete piezas**, cada una con su
  dominio. Son los estados, el estado inicial, los finales, quién mueve, las
  acciones, la transición y la utilidad.
- Decidir qué tiene que guardar un estado, incluido **a quién le toca**, y
  comprobar que no falta nada.
- Construir el grafo de un juego a partir de esas piezas y leer en él una
  partida.
- Distinguir el árbol de partidas del grafo de estados. Y explicar qué
  recibe una búsqueda: las reglas para generar el grafo, no el grafo dibujado.
- Diagnosticar un juego, decir qué modelo le corresponde y qué queda fuera
  de esta unidad.
- Decir qué significa que un jugador sea racional, respecto a qué, y qué
  no significa.
- Distinguir el **valor de un estado**, $V(s)$, el **valor de una jugada**,
  $Q(s,a)$, la jugada y la estrategia. Los dos valores se miden siempre desde
  MAX.

---

## Antes de leer: juega

Busca a alguien y dibuja un tablero de 3×3. Pon tres monedas de un tipo en
la fila de abajo y tres de otro en la de arriba. Cada moneda es un peón.

En su turno, un jugador avanza un peón una casilla hacia el rival, si está
vacía. O lo mueve una casilla en diagonal hacia delante para capturar uno
rival. Gana quien llega a la fila del otro.

Antes de empezar, **decidan entre ustedes** quién empieza y qué pasa si a
alguien le toca y no puede mover. Anótenlo y jueguen **tres partidas**.

Anota quién empezó y quién ganó cada vez. Esas decisiones y esos resultados
vuelven en la primera página y en la clase 2.

---

## Recorrido

Cuatro páginas, en orden, y una tarea de refuerzo al final.

::: table {#jue-ruta-1 title="Las páginas de esta clase"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 16m | **Leer el reglamento.** Qué dicen de verdad unas reglas explicadas con prisa |
| 2 | 40m | **Escribir el juego.** Las siete piezas de cualquier juego por turnos y una partida escrita con ellas |
| 3 | 30m | **El juego como grafo.** El grafo completo, árbol contra grafo y qué recibe una búsqueda |
| 4 | 35m | **Diagnosticar el juego.** Qué tipo de juego es, qué modelo le toca, qué es ser racional, $V$ y $Q$, y el problema de la unidad |
| 5 | 40m, aparte | **Tarea de refuerzo.** Escribir gato desde cero y cambiar una regla de hexapawn |
:::

1. [[leer-el-reglamento|Leer el reglamento]]
2. [[escribir-el-juego|Escribir el juego]]
3. [[el-juego-como-grafo|El juego como grafo]]
4. [[diagnosticar-el-juego|Diagnosticar el juego]]
5. [[tarea-leer-y-escribir|Tarea de refuerzo]]

## Qué no cubre esta clase

- **No se calcula ningún valor.** $V$ y $Q$ se definen aquí; calcularlos y
  saber quién gana con juego perfecto es la clase 2.
- **Azar, jugadas simultáneas y más jugadores** solo se diagnostican. La
  página 4 dice qué modelo pediría cada uno y cuáles quedan fuera de la
  unidad.

Empieza por [[leer-el-reglamento|leer el reglamento]].
