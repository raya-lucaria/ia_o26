# Créditos de las imágenes — Jugar contra alguien que también piensa

Los diagramas SVG de esta unidad los produce `tools/gen_juegos.py`. No se
editan a mano: se cambia la función del generador y se vuelve a correr. Ningún
tablero está dibujado a mano: cada nodo se calcula aplicando las jugadas con
`tools/juegos.py`, así que cambiar una regla cambia el dibujo.

Las cinco vistas previas `jue-anim-*.png` no se dibujan: son capturas de la
animación `traza_arbol_t.html`, tomadas con Chrome sin interfaz por
`tools/gen_vistas_traza.py`. `tools/test_vistas_traza.py` falla si la
animación cambió desde la última captura; entonces se vuelven a tomar.

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
| `jue-ab-ventana.svg` | La ventana (α, β) como banda en la recta: fuera de ella, o en el umbral del rival (v ≥ β en MAX, v ≤ α en MIN), corte beta o corte alfa; igualar el umbral propio no basta; los dos cortes del árbol base | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-fijo-parte-1.svg` | Alfa-beta desde n1 en orden fijo, parte 1: n2 vale +1 y la raíz toma α = +1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-fijo-parte-2.svg` | Alfa-beta desde n1 en orden fijo, parte 2: corte alfa en n3, que devuelve v = +1, una cota | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-1.svg` | Alfa-beta desde n1 en orden invertido, parte 1: n13 vale −1 y n3 toma β = −1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-2.svg` | Alfa-beta desde n1 en orden invertido, parte 2: corte beta en n6 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-ab-invertido-parte-3.svg` | Alfa-beta desde n1 en orden invertido, parte 3: n4, n3 devuelve v = −1, n2 y la raíz v = +1; 8 de 13 nodos | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-arbol.svg` | El árbol base, el problema: R de MAX con izq, centro y der; C con C1 y C2; las ocho hojas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-1.svg` | Minimax en el árbol base, tramo 1: I devuelve 3 y mejor_jugada = izq (fila 5 de la traza) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-2.svg` | Minimax en el árbol base, tramo 2: a media ejecución, pila R›C›C2 con C2 en v = 7 (fila 12) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-3.svg` | Minimax en el árbol base, tramo 3: C devuelve 5 y mejor_jugada = centro (fila 15) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-minimax-4.svg` | Minimax en el árbol base, tramo 4: D devuelve 2 y 2 > 5 es falso; DECIDIR devuelve centro (fila 19) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-1.svg` | Alfa-beta en el árbol reducido, fila 5: I devuelve 3, α = 3 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-2.svg` | Alfa-beta en el árbol reducido, fila 7: D llega con (3, +∞), v = 2 ≤ α = 3, corte alfa; la hoja 12 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t1-ab-3.svg` | Alfa-beta en el árbol reducido, fila 10: el final, 6 de 7 nodos, juega izq | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-1.svg` | Alfa-beta en el árbol base, tramo 1: I devuelve 3, α = 3 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-2.svg` | Alfa-beta en el árbol base, tramo 2: C1 devuelve 5; C compara v = 5 con α = 3, el número del rival, y baja su β a 5 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-3.svg` | Alfa-beta en el árbol base, tramo 3: corte beta en C2, v = 7 ≥ β = 5; la hoja 8 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-4.svg` | Alfa-beta en el árbol base, tramo 4: corte alfa en D, v = 2 ≤ α = 5; la hoja 12 no se genera | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-5.svg` | Alfa-beta en el árbol base, tramo 5: el final, dos podas, 12 de 14 nodos, juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-ab-pila.svg` | ALFA-BETA a media ejecución en el árbol base: la pila R›C›C2 y sus marcos en el instante del corte beta en C2 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-azar.svg` | El árbol base con I, C y D como volados parejos: 9/2, 13/2 y 7; juega der | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-corte-d1.svg` | El árbol de resultados con corte a profundidad 1 (finales en 100·U): EVAL 60, 20 y 10 en I, C y D; izq parece valer 60 y vale −100: la trampa del horizonte; 4 de 15 nodos | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-corte-d2-tramo-1.svg` | El árbol de resultados con corte a profundidad 2, al cerrar el tramo 1: I devolvió −100 y C 10, mejor_jugada = centro con 10; D todavía por mirar | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-corte-d2.svg` | El árbol de resultados con corte a profundidad 2: EVAL 10 y 50 en C1 y C2; izq y der −100, centro 10; juega centro; 11 de 15 nodos | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-iterativa.svg` | Profundización iterativa en el árbol de resultados (alfa-beta con corte, la jugada anterior primero): izq con d = 1, centro desde d = 2; 4, 9 y 12 nodos, 25 en total; las cotas marcadas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-1.svg` | Minimax con corte a profundidad 1 en la posición de la clase 3: la captura parece la mejor | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-2.svg` | Minimax con corte a profundidad 2: las respuestas de Negras y el cambio de decisión | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-corte-prof-3.svg` | Minimax con corte a profundidad 3, solo la rama d2-d3: tras a4-a3 o b4-b3, d3-d4 llega a la fila 4 y la rama vale 100 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-horizonte.svg` | El efecto horizonte: la recaptura queda detrás del corte | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-profundizacion.svg` | La profundización iterativa en el tiempo, con la jugada lista tras cada búsqueda | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcts-pasos.svg` | Una vuelta de UCT (c = 1) en cuatro paneles, cada nodo con N y V̂ desde MAX: selección, expansión, simulación (U = +1) y retropropagación; la raíz pasa de N 4, V̂ 0 a N 5, V̂ +0.2 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-hoeffding.svg` | Hoeffding en la escala ±1 en dos paneles: la cota e^(−N·ε²/2) contra ε con N = 100 (60.65 %, 13.53 %, 0.0335 % en ε = 0.1, 0.2, 0.4) y el margen √(2·ln(1/δ)/N) contra N para δ = 0.05 y 0.005 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-bono.svg` | El bono 2√2·√(ln N(s)/N(s,a)) contra N(s,a) para tres N(s), en la escala de U, y la curva de c = 1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-t-pm-arbol.svg` | El árbol de resultados, el problema de la radiografía: la forma del árbol base con finales en U (+1, 0, −1), tres hojas en D y la captura ix marcada; solo jugadas y finales, sin EVAL | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-minimax.svg` | Radiografía de minimax en el árbol de resultados: genera los 15 nodos, el V de cada uno y juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-alfa-beta.svg` | Radiografía de alfa-beta en el árbol de resultados, orden dado: 12 nodos, c2b, d2 y d3 tachados por el corte β y el corte α, cotas ≥ +1 y ≤ −1 | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-corte.svg` | Radiografía del corte a d = 1 en el árbol de resultados: 4 nodos, la EVAL de I, C y D en insignia, la captura ix detrás del horizonte; juega izq | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-quietud.svg` | Radiografía de la búsqueda de quietud a d = 1 en el árbol de resultados: sigue la captura ix, I pasa de EVAL 60 a −100; juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-iterativa.svg` | Radiografía de la profundización iterativa en el árbol de resultados: tres paneles, d = 1, 2 y 3, con 4, 9 y 12 nodos y los cortes α y β rotulados | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-mc-plano.svg` | Radiografía de Monte Carlo plano en el árbol de resultados (5 partidas por jugada, semilla 0): por dónde pasaron las partidas, que no se guardan, y los contadores de la raíz; juega der | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-uct-12.svg` | Radiografía de UCT en el árbol de resultados (c = 1, semilla 0) tras 12 vueltas: su árbol de 10 nodos con N y V̂, lo que aún no agrega; juega der | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-uct-40.svg` | Radiografía de UCT en el árbol de resultados (c = 1, semilla 0) tras 40 vueltas: su árbol de 15 nodos con N y V̂; juega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-flujo-minimax.svg` | Diagrama de flujo de minimax, en palabras | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-flujo-alfa-beta.svg` | Diagrama de flujo de alfa-beta, en palabras | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-flujo-corte.svg` | Diagrama de flujo del corte por profundidad, en palabras | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-flujo-mc-plano.svg` | Diagrama de flujo de Monte Carlo plano, en palabras | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-flujo-uct.svg` | Diagrama de flujo de UCT: el ciclo de sus cuatro fases y la salida por tiempo | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcg-arbol.svg` | Un árbol de juego grande y abstracto: b jugadas por nodo y m de hondo, con puntos suspensivos | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcg-mc-plano.svg` | Monte Carlo plano en el árbol grande: partidas al azar como caminos quebrados y solo N y Q̂ en la raíz | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcg-uct-fases.svg` | Las cuatro fases de UCT en el árbol grande, y el caso en que la selección llega a un final ya en su árbol | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcg-uct-crece.svg` | Tres instantáneas del árbol de UCT creciendo desigual, con la frontera siguiendo su contorno | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-rx-estado-y-jugada.svg` | El valor de una jugada vive en el hijo al que lleva: Q(s,a) = V(T(s,a)), y qué número guarda ahí cada algoritmo; simbólica, sin cifras | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-mcg-mezcla.svg` | Un promedio que se vuelve un mínimo: el nodo MIN bajo la jugada A con pocas y con muchas vueltas de UCT, Q̂(A) de ≈ 0 a −1; proporciones ilustrativas | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-rx-expectiminimax.svg` | Expectiminimax, otro juego: el árbol de resultados con D como dado parejo (esquinas redondas, ⅓ por hijo); I −1, C 0, D +1/3, R +1/3; juega der | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-rx-flujo-expectiminimax.svg` | Diagrama de flujo de expectiminimax: el de minimax con la rama «¿AZAR? → suma Pr(a\|s)·w» | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-rx-mmmc.svg` | Monte Carlo con actualización minimax en el árbol de resultados tras 10 partidas (semilla 0): V̂ de cada estado guardado, «?» en lo no visitado, los exactos marcados; entrega centro | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-rx-flujo-mmmc.svg` | Diagrama de flujo de la actualización minimax: partida uniforme hasta un final, guarda lo nuevo, V̂(z) = U(z), sube con máximo y mínimo | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-refutacion-tres.svg` | La refutación descubierta tarde en tres paneles con el mismo eje: promedio (10 → 8.67, límite −10/3) y actualización minimax (10 → −30) sobre una secuencia impuesta, y una corrida real de UCT (c = 1, semilla 0, 60 vueltas, pagos ÷30) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-tres-mc.svg` | Los tres Monte Carlo en el árbol de resultados por jugada de la raíz: V y Q_azar exactos; Monte Carlo plano, actualización minimax y UCT con 40 partidas o vueltas (semilla 0) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-c3-min-volteado.svg` | MIN volteado: p, q y r (Q̂ −0.2, +0.25, +0.5; N(s,a) 30, 16, 4; N(s) = 50; c = 2√2; bonos 1.02, 1.40, 2.80) con el bigote del bono a la derecha (si eligiera MAX) y a la izquierda (elige MIN) | Generado con `tools/gen_juegos.py` | Propio, CC BY-SA 4.0 |
| `jue-anim-minimax.png` | Vista previa de la animación de minimax en el árbol base, fila 12: línea 13, pila R›C›C2 | Capturado de `traza_arbol_t.html` con `tools/gen_vistas_traza.py` | Propio, CC BY-SA 4.0 |
| `jue-anim-azar.png` | Vista previa de la animación de expectiminimax en el árbol base, fila 6: C, de azar, empieza a sumar con v ← 0 | Capturado de `traza_arbol_t.html` con `tools/gen_vistas_traza.py` | Propio, CC BY-SA 4.0 |
| `jue-anim-alfa-beta.png` | Vista previa de la animación de alfa-beta en el árbol base, fila 12: el corte beta de C2, con tres marcos en la pila | Capturado de `traza_arbol_t.html` con `tools/gen_vistas_traza.py` | Propio, CC BY-SA 4.0 |
| `jue-anim-corte.png` | Vista previa de la animación de minimax con corte en el árbol de resultados, d = 2, fila 8: C1 y C2 estimados con EVAL | Capturado de `traza_arbol_t.html` con `tools/gen_vistas_traza.py` | Propio, CC BY-SA 4.0 |
| `jue-anim-iterativa.png` | Vista previa de la animación de la profundización iterativa, búsqueda con d = 2: empieza por izq y la ventana de I baja a (−∞, −100) | Capturado de `traza_arbol_t.html` con `tools/gen_vistas_traza.py` | Propio, CC BY-SA 4.0 |
