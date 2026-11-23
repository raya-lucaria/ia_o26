### celda: s05-intro

## 05 · Normalizar la entrada

Compara el píxel crudo $x$, el reescalado $x/255$ y el estandarizado $(x/255-\text{MEDIA})/\text{DESV}$.
**Calcula la media y la desviación solo en train** y reutilízalas en validation y test para evitar leakage.
La estandarización deja media $0$ y desviación $1$ para el conjunto de píxeles de train.
Las corridas comparten red ReLU, SGD sin momentum, learning rate, pesos iniciales y secuencia de batches.

### celda: s05-histogramas-guia

**La forma del histograma se conserva** al desplazar o reescalar el eje de píxeles.
En la escala estandarizada, el fondo queda debajo de cero y el blanco por encima.
El eje vertical logarítmico hace visibles los valores poco frecuentes. La línea discontinua marca la media muestral.

### celda: s05-gradiente

En backpropagation, $\partial\ell/\partial w_{ij}^{(1)}=\delta_i^{(1)}x_j$, con $\delta_i^{(1)}=\partial\ell/\partial z_i^{(1)}$.
Para una imagen, un paso de SGD cambia su preactivación vía los pesos en $-\eta\,\delta_i^{(1)}\sum_j x_j^2$.
Con $\delta_i^{(1)}$ fijo, multiplicar $x$ por $255$ amplifica ese efecto por $255^2$.
Compara el **tamaño del paso respecto a los pesos** con $\eta\lVert\nabla_W L_{\mathcal B}\rVert_F/\lVert W\rVert_F$.

### celda: s05-apuesta

**Apuesta.** Con el mismo $\eta$, ¿cuál dará menor loss de validation entre la escala cruda, $[0,1]$ y la estandarizada?
¿Cuál podría quedarse cerca del azar?

### celda: s05-arranque-guia

**La vista por paso muestra picos que la vista por epoch puede ocultar**.
A la izquierda, compara la loss de train con $\log 10$ en escala logarítmica.
A la derecha, compara la accuracy de validation con el $10\,\%$ de azar.
Aquí graficamos test para practicar. En un proyecto real se usa una sola vez para el reporte final.

### celda: s05-apuesta-respuesta

**Estandarizar dio ventaja desde el arranque** frente a $[0,1]$. La ventaja se redujo y persistió.
Con píxeles crudos, el paso inicial fue grande respecto a los pesos. La loss se disparó, pero la corrida terminó.
Una hipótesis es que el salto apagó muchas ReLU. Haría falta medir sus activaciones.

### celda: s05-pregunta-eta

**Ajusta el learning rate.** Para píxeles crudos, ¿dividirías $\eta$ entre $255^2$ o probarías otro valor?

### celda: s05-pregunta-eta-respuesta

Dividir $\eta$ entre $255^2$ compensa el efecto de los pesos sobre una imagen con $\delta_i^{(1)}$ fijo.
Para el sesgo, $\partial\ell/\partial b_i^{(1)}=\delta_i^{(1)}$. **Reducir $\eta$ también achica el paso del sesgo**.
Los logits iniciales dependen de la escala de los píxeles desde antes del primer paso.

### celda: s05-que-viste

**Qué viste**

- Con píxeles crudos, la loss de train se disparó y volvió cerca de $\log 10$. La corrida terminó con valores finitos.
- Su accuracy de validation repuntó al inicio y acabó cerca del azar. En otra corrida, la loss podría volverse no finita.
- Estandarizar aventajó a $[0,1]$ desde el arranque. La ventaja se redujo hacia el final.
