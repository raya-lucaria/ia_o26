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
| `jue-alfa-beta-fijo.svg` | Alfa-beta desde n1 con el orden fijo: 5 estados generados y un corte alfa | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-alfa-beta-invertido.svg` | Alfa-beta desde n1 con el orden invertido: 8 estados generados y un corte beta | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-1.svg` | Minimax con corte a profundidad 1 en la posición de la clase 3: la captura parece la mejor | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-2.svg` | Minimax con corte a profundidad 2: las respuestas de Negras y el cambio de decisión | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-horizonte.svg` | El efecto horizonte: la recaptura queda detrás del corte | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-profundizacion.svg` | La profundización iterativa en el tiempo, con la jugada lista tras cada búsqueda | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcts-pasos.svg` | Una vuelta de MCTS: selección, expansión, simulación y retropropagación | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
