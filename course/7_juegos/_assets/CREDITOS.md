# Créditos de las imágenes — Jugar contra alguien que también piensa

Los diagramas SVG de esta unidad los produce `tools/gen_juegos.py`. No se
editan a mano: se cambia la función del generador y se vuelve a correr. Ningún
tablero está dibujado a mano: cada nodo se calcula aplicando las jugadas con
`tools/juegos.py`, así que cambiar una regla cambia el dibujo.

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `jue-ciclo-partida.svg` | Una partida como ciclo: las siete piezas son sus cajas y elegir la jugada es la única que no dan las reglas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-grafo-paso-1.svg` | El grafo de hexapawn con un solo nodo: el estado inicial | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-grafo-paso-2.svg` | Las tres jugadas de Blancas y los estados a los que llevan | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-grafo-paso-3.svg` | Las respuestas de Negras a a1-a2 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-grafo-paso-4.svg` | Un camino hasta el primer final, con su utilidad | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-subgrafo-n1.svg` | El grafo completo desde n1, con sus 13 estados | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-transposicion.svg` | Dos órdenes de jugadas que llegan al mismo estado: árbol contra grafo | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-minimax-paso-1.svg` | Minimax a mano: valorar n6, donde las tres jugadas de Blancas empatan | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-minimax-paso-2.svg` | Minimax a mano: valorar n3, donde Negras toma el mínimo | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-minimax-paso-3.svg` | Minimax a mano: valorar n1 y elegir c1-c2 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-minimax-n1.svg` | El subgrafo de n1 con el valor de cada nodo y las jugadas que lo alcanzan | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-minimax-genera.svg` | Lo que MINIMAX tiene en memoria a media ejecución: el camino, lo ya olvidado y lo que aún no existe | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-azar-n3.svg` | n3 como nodo de azar: una Negras que elige al azar vale 1/3 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-alfa-beta-fijo.svg` | Alfa-beta desde n1 con el orden fijo: 5 estados generados, un corte alfa y n3 con la cota v = +1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-alfa-beta-invertido.svg` | Alfa-beta desde n1 con el orden invertido: 8 estados generados y un corte beta | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-ventana.svg` | La ventana (α, β) como banda en la recta: en un extremo o fuera, corte alfa o corte beta; los dos cortes del árbol T | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-fijo-parte-1.svg` | Alfa-beta desde n1 en orden fijo, parte 1: n2 vale +1 y la raíz toma α = +1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-fijo-parte-2.svg` | Alfa-beta desde n1 en orden fijo, parte 2: corte alfa en n3, que devuelve v = +1, una cota | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-1.svg` | Alfa-beta desde n1 en orden invertido, parte 1: n13 vale −1 y n3 toma β = −1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-2.svg` | Alfa-beta desde n1 en orden invertido, parte 2: corte beta en n6 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-3.svg` | Alfa-beta desde n1 en orden invertido, parte 3: n4, n3 devuelve v = −1, n2 y la raíz v = +1; 8 de 13 nodos | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-arbol.svg` | El árbol T, el problema: R de MAX con izq, centro y der; C con C1 y C2; las ocho hojas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-1.svg` | Minimax en T, paso 1: I devuelve 3 y mejor_jugada = izq (fila 5 de la traza) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-2.svg` | Minimax en T, paso 2: a media ejecución, pila R›C›C2 con C2 en v = 7 (fila 12) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-3.svg` | Minimax en T, paso 3: C devuelve 5 y mejor_jugada = centro (fila 15) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-4.svg` | Minimax en T, paso 4: D devuelve 2 y 2 > 5 es falso; DECIDIR devuelve centro (fila 19) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-1.svg` | Alfa-beta en T1, paso 1: I devuelve 3, α = 3 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-2.svg` | Alfa-beta en T1, paso 2: D llega con (3, +∞), v = 2 ≤ α = 3, corte alfa; la hoja 12 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-3.svg` | Alfa-beta en T1, paso 3: el final, 6 de 7 nodos, juega izq | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-1.svg` | Alfa-beta en T, paso 1: I devuelve 3, α = 3 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-2.svg` | Alfa-beta en T, paso 2: C1 devuelve 5; C compara v = 5 con α = 3, el número del rival, y baja su β a 5 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-3.svg` | Alfa-beta en T, paso 3: corte beta en C2, v = 7 ≥ β = 5; la hoja 8 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-4.svg` | Alfa-beta en T, paso 4: corte alfa en D, v = 2 ≤ α = 5; la hoja 12 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-5.svg` | Alfa-beta en T, paso 5: el final, 12 de 14 nodos, juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-pila.svg` | ALFA-BETA a media ejecución en T: la pila R›C›C2 y sus marcos en el instante del corte beta en C2 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-azar.svg` | T con I, C y D como volados parejos: 9/2, 13/2 y 7; juega der | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-corte-d1.svg` | T con corte a profundidad 1: EVAL en I, C y D; juega der, la trampa del horizonte | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-corte-d2.svg` | T con corte a profundidad 2: EVAL en C1 y C2; juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-iterativa.svg` | Profundización iterativa en T: d = 1, 2, 3 con la jugada anterior primero; 4, 10 y 11 nodos; en d = 3, I, D y C2 devuelven cotas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-1.svg` | Minimax con corte a profundidad 1 en la posición de la clase 3: la captura parece la mejor | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-2.svg` | Minimax con corte a profundidad 2: las respuestas de Negras y el cambio de decisión | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-horizonte.svg` | El efecto horizonte: la recaptura queda detrás del corte | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-profundizacion.svg` | La profundización iterativa en el tiempo, con la jugada lista tras cada búsqueda | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcts-pasos.svg` | Una vuelta de MCTS: selección, expansión, simulación y retropropagación | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
