# Créditos de imágenes

Procedencia y licencia de cada imagen de la unidad de complejidad. Toda imagen
del directorio debe tener una fila aquí, **los diagramas SVG incluidos**:
`test_toda_imagen_tiene_fila_en_creditos` no distingue entre una fotografía y un
diagrama generado, y lee el origen y la licencia como celdas obligatorias.

Los diagramas se producen con `tools/gen_complejidad.py` y **no se editan a
mano**: `tools/test_gen_complejidad.py` los regenera antes de compararlos, así
que una edición manual falla la suite.

Las siete ilustraciones de esta unidad usan un registro visual propio —anime de
ciencia ficción, no el grabado editorial de las otras tres unidades—, declarado
en `estilo_anime_fondo_plano` dentro de `tools/ilustraciones.json`. Ninguna cita
obra ni personaje existente y en ninguna el rostro es reconocible: es una
restricción del catálogo, no una casualidad de la generación.

`carrera_de_crecimiento.html` no lleva fila porque no es una imagen; es una
página interactiva escrita a mano, como el simulador de la unidad anterior.

| Archivo | Descripción | Autor / origen | Licencia |
|---|---|---|---|
| `cx-que-es-n.svg` | Tres maneras de medir la misma entrada: una lista, un grafo (que mide dos números) y un entero (que mide sus dígitos, no su valor) | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-peor-caso.svg` | La nube de entradas de tamaño n, con el peor caso, el caso promedio y el mejor caso marcados | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-o-grande.svg` | La definición de O grande dibujada: f por encima de c·g antes de n₀, y por debajo desde n₀ en adelante | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-familia-asintotica.svg` | O, Omega, Theta y o pequeña en cuatro paneles, cada uno con su definición por límites | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-escalera.svg` | Los cuatro algoritmos de la página como escalones, y qué le pasa a cada uno al duplicar n | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-matrices.svg` | De dónde sale el n³ de multiplicar matrices: una fila, una columna y la única celda que producen | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-crecimiento.svg` | Las cinco curvas de crecimiento en escala logarítmica, con los cruces de 2ⁿ marcados en tiempo de reloj | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-frontera.svg` | Qué tamaño de entrada se gana al duplicar la velocidad de la máquina, por tipo de crecimiento | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-dijkstra-vs-tsp.svg` | El mismo grafo con dos preguntas: camino mínimo (en P) y tour más corto (NP-completo) | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-espacio-se-reusa.svg` | La asimetría entre tiempo y memoria: el paso se gasta, la celda se reescribe | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-memoria-logaritmica.svg` | Qué cabe en O(log n) de memoria: una libreta con dos índices, contra una entrada de solo lectura que no cuenta | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-no-determinista.svg` | Una máquina determinista como una línea de configuraciones, y una no determinista como un árbol que se abre | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-verificar-vs-buscar.svg` | La misma fórmula, buscada entre 2ⁿ asignaciones o comprobada sobre el certificado que te entregan | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-tres-clases.svg` | P, NP y EXP anidadas, con habitantes concretos y con el borde que no se sabe cerrar dibujado punteado | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-monte-carlo.svg` | La máquina probabilista: entrada fija, monedas propias, y la brecha entre dos tercios y un tercio | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-miller-rabin.svg` | Las dos cadenas de cuadrados: la de 97, que toca −1, y la de 561, que llega al 1 desde 67 y se delata | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-error-se-desploma.svg` | Cómo cae el error de Miller-Rabin con el número de rondas, de uno en cuatro a uno en 10²⁴ | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-reduccion.svg` | Una reducción polinomial como un traductor entre instancias, con sus dos lecturas escritas | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-duro-vs-completo.svg` | NP-duro y NP-completo enfrentados, y el problema de la parada fuera del óvalo de NP | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-sat-a-3sat.svg` | Una cláusula de cinco literales partida en tres de tres, encadenadas por dos variables nuevas | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-arbol-de-karp.svg` | El árbol de reducciones desde SAT y 3-SAT hasta clique, hamiltoniano, coloreo y mochila | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-mapa.svg` | La cadena L ⊆ P ⊆ NP ⊆ PSPACE ⊆ EXP con el estado de cada contención | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `cx-dos-mundos.svg` | Qué cambiaría si P = NP y qué implica que P ≠ NP, en dos columnas | Diagrama propio, generado con `tools/gen_complejidad.py` | Material del curso |
| `ilus-portada-complejidad.png` | Figura solitaria ante una ciudad nocturna cuyas torres no terminan — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-explosion-combinatoria.png` | Figura pequeña al pie de una estructura que se duplica en cada nivel — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-dos-caminos.png` | Bifurcación entre un sendero corto e iluminado y un laberinto sin fondo — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-el-arbol-que-se-abre.png` | Un corredor que se abre en miles de corredores idénticos a la vez — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-la-llave-y-los-cerrojos.png` | Una sola llave luminosa frente a un muro de cerraduras idénticas — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-la-moneda.png` | Una moneda girando suspendida en una sala de servidores oscura — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
| `ilus-la-frontera.png` | Un territorio partido por una línea de luz: mapa de un lado, blanco del otro — ilustración generada | Ilustración **generada** con `gpt-image-2` desde `tools/ilustraciones.json` | Material del curso |
