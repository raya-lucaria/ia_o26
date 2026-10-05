# Verificación — Jugar contra alguien que también piensa

Registro de fuentes de `course/7_juegos/`. Como en optimización, **un solo
archivo cubre la unidad**. Lo que hay que respaldar son de dos tipos:

- **Números de los juegos de la unidad** (hexapawn, octapawn, gato, monedas,
  el dado, los juegos simultáneos). No se citan de ninguna fuente: se
  **calculan** por fuerza bruta o con fracciones exactas en `tools/juegos.py`,
  y `tools/test_juegos.py` comprueba cada número que la prosa cita.
- **Hechos externos** (ajedrez, Gardner, Deep Blue, AlphaZero, MCTS, AlphaGo), con su fuente
  abajo.

Las fuentes se consultaron el **1 de octubre de 2026**.

## Números calculados

| Afirmación | Dónde se calcula | Prueba |
|---|---|---|
| Hexapawn 3×3: 252 nodos, 135 estados; partida más larga de 7 jugadas | `contar_arbol`, `partida_mas_larga` | `test_clase_1_hexapawn` |
| La partida trazada en «Escribir el juego»: a1-a2, b3xa2, b1-b2, a2-a1; las $A(s)$ de cada paso, el final $s_4$ y $U(s_4)=-1$ | `jugadas`, `mover`, `ganador` | `test_clase_1_partida_trazada_con_las_piezas` |
| En 3×3 el tablero determina el turno y $k$; en 4×4, 2925 tableros se alcanzan con los dos turnos | `tableros_con_dos_turnos`, `tableros_con_dos_contadores` | `test_clase_1_hexapawn` |
| 33 estados no finales con Blancas al turno, 37 con Negras, 65 finales (8 por falta de jugada) | `contar_estados` | `test_clase_1_hexapawn` |
| Con juego perfecto gana Negras (valor −1; −4 con puntos de torneo); con «sin jugada = empate», valor 0 | `valor` | `test_clase_1_tarea`, `test_clase_2_minimax_y_alfa_beta` |
| Gato: 255 168 partidas, 549 946 nodos, 5478 tableros; el turno se deduce; valor 0 | `gato_conteos`, `gato_turno_se_deduce`, `gato_valor` | `test_clase_1_tarea`, `test_clase_3_tarea_gato` |
| Subárbol de la clase 2: 13 nodos, valor 7; alfa-beta visita 5 (corte alfa) u 8 con el orden invertido (corte beta) | `alfa_beta` | `test_clase_2_minimax_y_alfa_beta` |
| Octapawn 4×4: 4 197 973 nodos, 20 286 estados, gana el primero | `contar_arbol`, `valor` | `test_clase_3_no_cabe_y_horizonte` |
| Posiciones de horizonte de la clase 3 y su tarea | `minimax_limitado`, `evaluar_peones` | `test_clase_3_no_cabe_y_horizonte` |
| Monedas (2,1,5,3), dado, cerdo reducido | `monedas_*`, `dado_ejemplo`, `cerdo*` | `test_clase_2_dado_y_tarea` |
| Pares o nones, piedra-papel-tijera, penales, gallina, prisionero | `mezcla_2x2`, `punto_de_silla`, `equilibrios_puros` | `test_clase_4_*` |

## Hechos externos

| # | Afirmación | Fuente | Verificado |
|---|---|---|---|
| 1 | Hexapawn lo publicó Martin Gardner en su columna «Mathematical Games» de *Scientific American*, marzo de 1962, para construir una máquina que aprende con cajas de cerillos | Wikipedia, «Hexapawn» (https://en.wikipedia.org/wiki/Hexapawn); Marx et al., *Using Matchboxes to Teach the Basics of Machine Learning*, PMLR 170 (2022) | Sí |
| 2 | La máquina de Gardner (HER) juega con Negras y usa 24 cajas de cerillos. Contando una vez cada par de posiciones reflejas, las posiciones no finales de Negras son 19; ese 19 es un cálculo nuestro (`test_clase_1_posiciones_de_negras_por_simetria`), no la cifra de Gardner | Wikipedia, «Hexapawn»; Marx et al., PMLR 170 (2022); M. Scroggs, «Building MENACEs for other games» (https://www.mscroggs.co.uk/blog/52) | Sí |
| 2b | Conecta 4 se resolvió en 1988 (Allen; Allis, de forma independiente): gana quien empieza | Wikipedia, «Connect Four» | Sí |
| 3 | Con juego perfecto gana el segundo jugador | Las mismas fuentes; además lo recalcula `valor` | Sí |
| 4 | Posiciones legales de ajedrez ≈ 4.8×10^44 (Tromp y Österlund, 2021, por muestreo) | J. Tromp, «John's Chess Playground» (https://tromp.github.io/chess/chess.html); Chess Programming Wiki, «John Tromp» | Sí |
| 5 | Shannon (1950) estimó del orden de 10^120 partidas de ajedrez | Wikipedia, «Shannon number» (https://en.wikipedia.org/wiki/Shannon_number) | Sí |
| 6 | Deep Blue venció a Kasparov en un match en 1997 | Hecho histórico ampliamente documentado; la unidad de historia lo cita | Sí |
| 7 | Clase del MIT: 6.034 *Artificial Intelligence* (otoño 2010), lección 6, «Search: Games, Minimax, and Alpha-Beta», Patrick Winston | MIT OCW y YouTube (https://www.youtube.com/watch?v=STjW3eH0Cik) | Sí |
| 8 | MCTS: cada vuelta tiene cuatro pasos (selección, expansión, simulación, retropropagación); Rémi Coulom le dio nombre en 2006; desde 2006 los programas de Go más fuertes la usan; al final se juega la jugada con más simulaciones | Wikipedia, «Monte Carlo tree search» (https://en.wikipedia.org/wiki/Monte_Carlo_tree_search); R. Coulom, *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*, CG 2006. Consultado el 5 de octubre de 2026 | Sí |
| 9 | La regla UCT, $\bar u+c\sqrt{\ln N(s)/N(s')}$, es de Kocsis y Szepesvári (2006) | L. Kocsis y C. Szepesvári, *Bandit Based Monte-Carlo Planning*, ECML 2006; Wikipedia, «Monte Carlo tree search». Consultado el 5 de octubre de 2026 | Sí |
| 10 | AlphaGo venció 4 a 1 a Lee Sedol en Seúl, del 9 al 15 de marzo de 2016, combinando MCTS con una red que sugiere jugadas y otra que estima posiciones | Wikipedia, «AlphaGo versus Lee Sedol» (https://en.wikipedia.org/wiki/AlphaGo_versus_Lee_Sedol); D. Silver et al., «Mastering the game of Go with deep neural networks and tree search», *Nature* 529 (2016). Consultado el 5 de octubre de 2026 | Sí |
| 11 | AlphaZero (2017) deja las simulaciones al azar: valora las hojas con su red, que aprende jugando contra sí misma | D. Silver et al., «A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play», *Science* 362 (2018; preprint de 2017) | Sí |
