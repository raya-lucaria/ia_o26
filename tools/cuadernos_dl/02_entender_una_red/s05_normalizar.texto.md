### celda: s05-intro

## 05 · Normalizar la entrada

- **Calcula la media y la desviación solo en train** y reutilízalas en validation y test para evitar leakage.
- Las corridas comparten red ReLU, SGD sin momentum, learning rate, pesos iniciales y secuencia de batches.

### celda: s05-histogramas-guia

**La forma del histograma se conserva** en las tres escalas.

| Escala | Qué es | Qué esperar | En el histograma |
|---|---|---|---|
| Cruda | $x$ | Rango original | Fondo cerca de cero |
| Reescalada | $x/255$ | Rango $[0,1]$ | Eje horizontal comprimido |
| Estandarizada | $(x/255-\text{MEDIA})/\text{DESV}$ | Media $0$ y desviación $1$ en train | Fondo bajo cero y blanco por encima |

- El eje vertical logarítmico revela píxeles poco frecuentes.
- La línea discontinua marca la media muestral.

### celda: s05-gradiente

- En backpropagation, $\partial\ell/\partial w_{ij}^{(1)}=\delta_i^{(1)}x_j$, con $\delta_i^{(1)}=\partial\ell/\partial z_i^{(1)}$.
- Para una imagen, un paso de SGD cambia su preactivación vía los pesos en $-\eta\,\delta_i^{(1)}\sum_j x_j^2$.
- Con $\delta_i^{(1)}$ fijo, multiplicar $x$ por $255$ amplifica ese efecto por $255^2$.
- Compara el **tamaño del paso respecto a los pesos** con $\eta\lVert\nabla_W L_{\mathcal B}\rVert_F/\lVert W\rVert_F$.

### celda: s05-apuesta

- **Apuesta.** ¿Qué escala dará menor loss de validation con el mismo $\eta$?
- ¿Cuál podría quedarse cerca del azar?

### celda: s05-arranque-guia

- **La vista por paso revela picos** que la vista por epoch puede ocultar.
- Izquierda: loss de train frente a $\log 10$, en escala logarítmica.
- Derecha: accuracy de validation frente al $10\,\%$ de azar.
- Aquí graficamos test para practicar. En un proyecto real se usa una sola vez para el reporte final.

### celda: s05-apuesta-respuesta

- **Estandarizar dio ventaja desde el arranque** frente a $[0,1]$.
- El salto inicial con píxeles crudos pudo apagar muchas ReLU. Para comprobarlo, mide sus activaciones.

### celda: s05-pregunta-eta

**Ajusta el learning rate.** Para píxeles crudos, ¿dividirías $\eta$ entre $255^2$ o probarías otro valor?

### celda: s05-pregunta-eta-respuesta

- Dividir $\eta$ entre $255^2$ compensa el efecto de los pesos sobre una imagen con $\delta_i^{(1)}$ fijo.
- **Reducir $\eta$ también achica el paso del sesgo**, cuyo gradiente es $\partial\ell/\partial b_i^{(1)}=\delta_i^{(1)}$.
- Los logits iniciales dependen de la escala de los píxeles.

### celda: s05-que-viste

**Qué viste**

- Con píxeles crudos, la loss de train se disparó y volvió cerca de $\log 10$ con valores finitos.
- Su accuracy de validation repuntó y acabó cerca del azar. En otra corrida, la loss podría volverse no finita.
- Estandarizar mantuvo una ventaja sobre $[0,1]$, aunque se redujo hacia el final.
