# Créditos de las imágenes — Modelado y optimización

Los diagramas SVG de esta unidad los produce `tools/gen_optimizacion.py`. No se
editan a mano: se cambia la función del generador y se vuelve a correr. Cuatro de
ellos —`opt-poligono`, `opt-curvas-de-nivel`, `opt-sin-energia` y
`opt-fig-poliedro`— **calculan** su contenido desde los parámetros del episodio,
así que cambiar un dato de la impresora cambia el dibujo solo.
`opt-camino-simplex` calcula además la relación de vecindad y la traza entera
del método, y `opt-fig-precio-sombra` las dos regiones y los tres óptimos que
recorre la recta de las horas. `opt-fig-circulos`
calcula el polígono y el consumo de su punto interior, y `opt-fig-vertice-o-arista`
deriva de cada objetivo cuáles vértices ganan y cuánto pagan: por eso uno de
sus paneles trae un punto y el otro una arista.

Las páginas HTML autocontenidas de `_assets/`, si las hay, no llevan fila aquí:
no son imágenes.

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `opt-la-impresora.svg` | La situación entera: qué se gasta, qué se decide y qué se gana | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-anatomia.svg` | La forma canónica con cada una de sus siete partes señalada | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-lienzo.svg` | Los siete pasos del lienzo de modelado, en dos bloques | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-historia-a-modelo.svg` | Cada frase de la bitácora y la desigualdad que produce | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-poligono.svg` | La región factible de la impresora y sus cinco esquinas | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-curvas-de-nivel.svg` | La familia de curvas de nivel y la que toca el óptimo | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-sin-energia.svg` | Las dos regiones, con y sin la restricción de energía | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-dos-cimas.svg` | Un óptimo local que no es global, en una variable | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-matriz.svg` | El modelo escrito y la misma información como terna, con un renglón y una columna marcados | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-poliedro.svg` | El poliedro de tres piezas en proyección, con sus ocho vértices | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-circulos.svg` | Curvas de nivel circulares sobre el polígono de la clase 1, con el máximo por dentro | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-camino-simplex.svg` | El camino de simplex sobre el polígono de la clase 1: dos pivotes y dos esquinas que nadie miró | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-precio-sombra.svg` | Qué compra una hora más: la recta de las horas en 10, 11 y 12, y el óptimo corriendo por la arista del polímero hasta (6,6) | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
| `opt-fig-vertice-o-arista.svg` | Los dos desenlaces del teorema del vértice: la recta de nivel que toca en un solo vértice y la que se apoya en una arista entera | Generado con `tools/gen_optimizacion.py` | Propio, CC BY-SA 4.0 |
