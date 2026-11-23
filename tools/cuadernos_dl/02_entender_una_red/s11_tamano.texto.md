### celda: s11-intro

## 11 · El tamaño de la red

**Ancho y profundidad cambian la forma y el tamaño de la red.** Usamos capas ocultas del mismo ancho.
El conteo incluye pesos y sesgos, $\sum_{l=1}^{L}(d_{l-1}+1)d_l$. En $[784,2,10]$ suma $1600$ parámetros.
Cada red usa ReLU y entrena cinco epochs con los mismos 20 000 ejemplos de train.
Todas usan Adam con $\eta=10^{-3}$ y batch de 128.
La inicialización He usa varianza $2/d_{l-1}$ para conservar la escala de la señal con ReLU.

### celda: s11-apuesta

**Apuesta.** ¿Cuál quedará última en validation: la más estrecha y profunda, la más ancha y profunda u otra?
¿Aumentar ancho o profundidad siempre ayuda? ¿La red más grande tendrá la mayor brecha?

### celda: s11-mapas-lee

Lee el ancho por columna y la profundidad por fila. A la izquierda, un color más claro indica mayor accuracy.
**La brecha es accuracy de train menos accuracy de validation.** A la derecha, rojo indica brecha positiva y azul, negativa.
Una brecha positiva grande puede señalar overfitting.

### celda: s11-apuesta-respuesta

**La red más estrecha y profunda quedó última.** Su accuracy terminó cerca del azar.
Aumentar ancho o profundidad no siempre ayudó. La mayor brecha no fue de la red más grande.
En otra corrida, las redes cercanas pueden cambiar de orden.

### celda: s11-parametros-lee

Cada punto es una red. El número indica su ancho y la línea agrupa redes de igual profundidad.
El eje de parámetros es logarítmico. **La accuracy se aplanó tras salir de los anchos más chicos.**
Compara redes con conteos parecidos y distinta forma.

### celda: s11-dibujos-lee

Los dibujos comparan cuatro redes. Los puntos suspensivos indican neuronas omitidas.
**Una accuracy cercana al azar admite dos explicaciones.** En el mapa, ese fue el resultado de la red más estrecha y profunda.
Puede faltarle capacidad o puede ser difícil ajustar sus pesos en cinco epochs.
En §13 y §14 miraremos el gradiente por capa.

### celda: s11-cuello-intro

Comparamos $[784,2,10]$ y $[784,256,2,10]$ con los mismos datos y presupuesto de epochs.
Cada punto representa una imagen de validation y su color indica el dígito verdadero.
**La salida recibe solo dos activaciones.** A la izquierda ves $\mathbf z$ y a la derecha $\mathbf a=\operatorname{ReLU}(\mathbf z)$.
ReLU convierte los valores negativos en cero. Los puntos pueden acumularse en los ejes o el origen.

### celda: s11-cuello-lee

**El colapso fue parcial.** En ambas redes, muchas imágenes cayeron en el origen y recibieron la misma predicción.
Con la capa de 256, más imágenes cayeron en el origen. La segunda neurona quedó en cero.
La primera aún distinguió parte de las imágenes.
En otra corrida podrían quedar activas ambas neuronas. Haría falta entrenar más para saber si el colapso persiste.

### celda: s11-que-viste

- **Aumentar el ancho ayudó sobre todo al salir del cuello estrecho.** Más adelante, añadir parámetros cambió poco la accuracy.
- La brecha tendió a crecer con el ancho y siguió siendo pequeña.
- Las activaciones mostraron un colapso parcial en las redes con cuello. En otra corrida puede cambiar cuántos ejemplos lo sufren.
- Compara arquitecturas con validation y reserva test para el informe final.
