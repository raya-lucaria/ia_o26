---
id: resultados-torneo-adversarial
title: "Resultados del torneo: Breakthrough de combate"
nav_title: Resultados
summary: "La tabla final de la liga de Breakthrough de combate: 29 bots, todos contra todos, 16 240 partidas jugadas del 17 al 18 de noviembre de 2026."
status: ready
estimated_time: 3m
tags: [juegos, proyecto, torneo, resultados]
---

# Resultados del torneo

**Anexo** · la tabla final de la liga

La liga del [[proyecto-torneo-adversarial|proyecto de la unidad]] se jugó
completa del 17 al 18 de noviembre de 2026, en una sola máquina y con los
límites oficiales: cada bot corrió aislado en Docker con 1 núcleo y 1 GB, y
con 30 s de reloj por partida (escala oficial 1.1).

Jugaron **29 bots**: 16 equipos de alumnos y 13 bots de referencia
(`random`, `montecarlo` y los `tier_*`). Fue todos contra todos, con **40
partidas por pareja**: 20 juegos de dados, cada uno con blancas y con negras.
La tabla junta 7 corridas completas con semillas distintas, así que cada bot
jugó **1 120 partidas** y la liga entera **16 240**. Ninguna partida se perdió
por reloj y ninguna pareja quedó fuera por fallas.

**Cómo se lee.** En este juego no hay empates: los puntos son las partidas
ganadas. Si dos bots empatan en puntos, decide primero el resultado entre
ellos, luego el **SB** (la suma de los puntos de los rivales a los que
venciste) y al final los peones anotados (columna «Peones»). «%» es el
porcentaje de victorias. Los equipos de alumnos van en
negritas; los demás son los bots de referencia.

| Lugar | Equipo | Ganadas | % | SB | Peones |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | **`torneo_breakthrough`** | 875 | 78,1 % | 453 939 | 2 917 |
| 2 | **`frea`** | 815 | 72,8 % | 409 034 | 2 897 |
| 3 | **`alondra_bernardo`** | 802 | 71,6 % | 410 603 | 2 808 |
| 4 | **`pamplinotas`** | 791 | 70,6 % | 401 092 | 2 803 |
| 5 | **`equipo_gg`** | 791 | 70,6 % | 395 380 | 2 841 |
| 6 | `tier_5` | 774 | 69,1 % | 385 163 | 2 734 |
| 7 | `tier_halcon` | 752 | 67,1 % | 371 892 | 2 686 |
| 8 | **`maquinas_del_trabajo`** | 733 | 65,4 % | 361 972 | 2 752 |
| 9 | `tier_colibri` | 719 | 64,2 % | 356 234 | 2 613 |
| 10 | `tier_4` | 698 | 62,3 % | 340 035 | 2 644 |
| 11 | `tier_3` | 649 | 57,9 % | 310 203 | 2 472 |
| 12 | **`iacasitegano`** | 634 | 56,6 % | 299 081 | 2 571 |
| 13 | `tier_2` | 633 | 56,5 % | 296 975 | 2 644 |
| 14 | `tier_buho` | 629 | 56,2 % | 293 116 | 2 631 |
| 15 | **`liszt_breakthrough2`** | 619 | 55,3 % | 297 587 | 2 534 |
| 16 | **`t_regex`** | 566 | 50,5 % | 261 120 | 2 479 |
| 17 | `tier_1` | 530 | 47,3 % | 238 599 | 1 961 |
| 18 | `tier_lince` | 521 | 46,5 % | 234 848 | 1 941 |
| 19 | **`primer_lugar`** | 518 | 46,2 % | 231 939 | 2 119 |
| 20 | **`fperez_mnava`** | 484 | 43,2 % | 212 852 | 2 311 |
| 21 | **`limon_armando`** | 479 | 42,8 % | 212 303 | 2 042 |
| 22 | **`frame_perfect_push`** | 467 | 41,7 % | 204 331 | 2 021 |
| 23 | **`nan`** | 419 | 37,4 % | 179 134 | 1 733 |
| 24 | **`potential_man`** | 411 | 36,7 % | 176 317 | 1 910 |
| 25 | **`mc_aprendiz`** | 396 | 35,4 % | 164 093 | 2 039 |
| 26 | `montecarlo` | 382 | 34,1 % | 156 320 | 1 736 |
| 27 | `tier_tortuga` | 92 | 8,2 % | 8 999 | 588 |
| 28 | `tier_cuervo` | 58 | 5,2 % | 9 684 | 542 |
| 29 | `random` | 3 | 0,3 % | 991 | 90 |

## Tres cosas que dice la tabla

- **Los cinco primeros equipos de alumnos quedaron por encima de `tier_5`**,
  el más fuerte de los tiers numerados, y `torneo_breakthrough` ganó la liga
  con 78,1 % de victorias.
- **Los tiers 1 a 5 quedaron en orden**: `tier_5` 6.º, `tier_4` 10.º,
  `tier_3` 11.º, `tier_2` 13.º y `tier_1` 17.º. Con 1 120 partidas por bot,
  la escala de fuerza se notó tal como estaba pensada.
- **`pamplinotas` y `equipo_gg` empataron con 791 puntos** y los separó el
  SB: 401 092 contra 395 380. Ganarle a rivales fuertes pesa más que ganarle
  a los débiles.

Y una más: los 16 equipos de alumnos quedaron por encima de `montecarlo`.

Las reglas y el motor siguen en el
[repositorio del torneo](https://github.com/raya-lucaria/ia_o26_torneo_adversarial).

Regresa a [[proyecto-torneo-adversarial|el proyecto]] o a [[juegos|la unidad]].
