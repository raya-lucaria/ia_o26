### celda: s11-intro

## 11 · El tamaño de la red

- **Ancho y profundidad determinan el tamaño de la red.** Las capas ocultas de cada red tienen el mismo ancho.
- Pesos y sesgos suman $\sum_{l=1}^{L}(d_{l-1}+1)d_l$. En $[784,2,10]$ son $1600$ parámetros.
- ReLU, Adam con $\eta=10^{-3}$, batch de 128 y cinco epochs sobre los mismos 20 000 ejemplos.
- La inicialización He usa varianza $2/d_{l-1}$ para conservar la escala de la señal con ReLU.

### celda: s11-apuesta

- **Apuesta.** ¿Quedará última la más estrecha y profunda, la más ancha y profunda u otra?
- ¿Añadir ancho o profundidad siempre ayuda? ¿La red más grande tendrá la mayor brecha?

### celda: s11-mapas-lee

**La brecha es accuracy de train menos accuracy de validation.**

| Mapa | Qué buscar | Cómo se ve |
| --- | --- | --- |
| Accuracy de validation | Mejora al variar ancho o profundidad | Claro indica mayor accuracy |
| Brecha | Una brecha positiva grande sugiere overfitting | Rojo positivo, azul negativo |

Lee el ancho por columna y la profundidad por fila.

### celda: s11-apuesta-respuesta

- **La más estrecha y profunda quedó cerca del azar.**
- Añadir ancho o profundidad no siempre ayudó. La mayor brecha apareció fuera de la red más grande.
- En otra corrida, las redes cercanas pueden cambiar de orden.

### celda: s11-parametros-lee

- Cada punto es una red. El número indica su ancho y la línea agrupa redes de igual profundidad.
- El eje de parámetros es logarítmico. **La accuracy se aplanó tras salir de los anchos más chicos.**
- Compara redes de forma distinta con conteos parecidos.

### celda: s11-dibujos-lee

- Los dibujos comparan cuatro redes. Los puntos suspensivos indican neuronas omitidas.
- **Una accuracy cercana al azar admite dos explicaciones.** Puede faltar capacidad o ser difícil optimizar en cinco epochs.
- En §13 y §14 miraremos el gradiente por capa.

### celda: s11-cuello-intro

- Mismos datos y epochs para $[784,2,10]$ y $[784,256,2,10]$.
- Cada punto es una imagen de validation y su color indica el dígito verdadero.
- **La salida recibe dos activaciones.** Izquierda, $\mathbf z$. Derecha, $\mathbf a=\operatorname{ReLU}(\mathbf z)$.
- ReLU lleva los negativos a cero. Los puntos pueden juntarse en los ejes o en el origen.

### celda: s11-cuello-lee

- **El colapso fue parcial.** Las imágenes que caen en el origen reciben la misma predicción.

| Red | Qué cambia | Qué se ve tras ReLU |
| --- | --- | --- |
| $[784,2,10]$ | Cuello directo | Acumulación en origen y ambos ejes |
| $[784,256,2,10]$ | Capa ancha antes del cuello | Más puntos en el origen y segunda neurona en cero |

En otra corrida podrían quedar activas ambas neuronas.

### celda: s11-que-viste

- **Aumentar el ancho ayudó sobre todo al salir del cuello estrecho.** Después, sumar parámetros cambió poco la accuracy.
- La brecha tendió a crecer con el ancho y siguió siendo pequeña.
- Compara arquitecturas con validation y reserva test para el informe final.
