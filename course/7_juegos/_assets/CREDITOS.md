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
