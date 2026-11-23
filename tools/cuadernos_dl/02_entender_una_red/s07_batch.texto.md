### celda: s07-intro

## 07 · Gradient descent y el tamaño del batch

![Una pelota bajando por la superficie de pérdida](ilustracion:pelota)
*(Ilustración generada con gpt-image-2.)*

- Gradient descent da un paso $\theta\leftarrow\theta-\eta\,\nabla_\theta L_{\mathcal B}(\theta)$ en dirección contraria al gradiente.
- La loss del batch es $L_{\mathcal B}(\theta)=\frac{1}{|\mathcal B|}\sum_{k\in\mathcal B}\ell_k$. Con full-batch, el promedio abarca todo train.
- **El tamaño del batch determina cuántos pasos caben en una epoch**, $\lceil n/B\rceil$.
- Todas las corridas usan las mismas 4096 imágenes, la misma inicialización y SGD sin momentum con $\eta=0.03$.

### celda: s07-apuesta

**Apuesta.** Tras una epoch, ¿tendrá menor loss de validation batch 1 o full-batch?
¿Y con el mismo número de pasos al inicio?

### celda: s07-ejes

Los cuatro paneles muestran loss de validation por epoch, paso, ejemplo procesado o segundo de entrenamiento.
El eje horizontal es logarítmico. Cada estrella marca la última medición dentro del presupuesto común.
**Compara al mismo presupuesto.** Fuera del tramo gris aún puedes comparar corridas que alcanzaron el mismo valor.
Aquí se compara con validation. Test se reserva para el reporte final.

### celda: s07-justa

- **Iguala el recurso que quieres comparar.** Por epoch o ejemplos vistos, un batch chico da más pasos.
- A igual número de pasos, un batch grande procesa más ejemplos. Por segundo, importa el paralelismo de la GPU.
- Los batches $8$, $32$, $128$ y $1024$ completaron cinco epochs. Entre ellos, la menor loss final fue la de $8$.

### celda: s07-apuesta-respuesta

**El orden cambió con el eje.** Tras una epoch, batch 1 logró menor loss que full-batch.
A igual número de pasos al inicio, full-batch avanzó más. En otra corrida el learning rate puede cambiar ese orden.

### celda: s07-ruido-idea

- Con $\theta$ fijo, el gradiente de un batch aleatorio estima sin sesgo el gradiente completo. La señal es $\|g_{\text{completo}}\|^2$.
- El ruido es $\mathbb E\,\|g_{\mathcal B}-g_{\text{completo}}\|^2$.
- **El ruido baja aproximadamente como $1/B$**. Muestrear sin reemplazo añade el factor $(n-B)/(n-1)$.
- Compara la red inicial con la entrenada. Las barras muestran el error estándar del ruido medio.

### celda: s07-que-viste

**Qué viste**

- Los batches chicos destacaron por epoch y los grandes por paso. En GPU rindieron mejor los intermedios por segundo.
- El ruido bajó cerca de $1/B$. Para batches grandes, se acercó a la referencia corregida por muestreo sin reemplazo.
- Con batch 8 bajó el ruido absoluto al entrenar. El cociente ruido/señal subió y confirmó que predominaba el ruido.
- En otra máquina puede cambiar el orden por segundo.
