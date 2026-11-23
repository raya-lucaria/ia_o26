### celda: s07-intro

## 07 · Gradient descent y el tamaño del batch

![Una pelota bajando por la superficie de pérdida](ilustracion:pelota)
*(Ilustración generada con gpt-image-2.)*

- Gradient descent actualiza $\theta\leftarrow\theta-\eta\,\nabla_\theta L_{\mathcal B}(\theta)$.
- La loss del batch es $L_{\mathcal B}(\theta)=\frac{1}{|\mathcal B|}\sum_{k\in\mathcal B}\ell_k$.
- **El tamaño del batch determina cuántos pasos caben en una epoch**, $\lceil n/B\rceil$.
- Todas las corridas comparten 4096 imágenes, inicialización y SGD sin momentum con $\eta=0.03$.

### celda: s07-apuesta

- **Apuesta.** Tras una epoch, ¿tendrá menor loss de validation batch 1 o full-batch?
- ¿Y con el mismo número de pasos al inicio?

### celda: s07-ejes

- Los paneles muestran loss de validation por epoch, paso, ejemplo procesado o segundo.
- El eje horizontal es logarítmico. Cada estrella marca la última medición dentro del presupuesto común.
- **Compara al mismo presupuesto.** Fuera del tramo gris puedes comparar corridas que alcanzaron el mismo valor.
- Aquí se compara con validation. Test se reserva para el reporte final.

### celda: s07-justa

**La ventaja depende del presupuesto.**

| Batch | Qué es | Qué esperar | En la gráfica |
|---|---|---|---|
| Chico | Pocos ejemplos por paso | Más pasos por epoch | Menor loss a igual epoch |
| Intermedio | Varios ejemplos por paso | Aprovecha el paralelismo de la GPU | Menor loss por segundo |
| Full-batch | Todo train por paso | Más ejemplos por actualización | Mayor avance por paso inicial |

### celda: s07-apuesta-respuesta

- **El orden cambió con el eje.** Batch 1 ganó por epoch y full-batch por paso al inicio.
- En otra corrida, el learning rate puede cambiar ese orden.

### celda: s07-ruido-idea

- Con $\theta$ fijo, el gradiente de un batch aleatorio estima sin sesgo el gradiente completo.
- La señal es $\|g_{\text{completo}}\|^2$ y el ruido es $\mathbb E\,\|g_{\mathcal B}-g_{\text{completo}}\|^2$.
- **El ruido baja aproximadamente como $1/B$**. Muestrear sin reemplazo añade el factor $(n-B)/(n-1)$.
- Las barras muestran el error estándar del ruido medio.

### celda: s07-que-viste

**Qué viste**

- Entre batches con el mismo presupuesto final de ejemplos, el menor batch obtuvo la menor loss.
- Para batches grandes, el ruido se acercó a la referencia corregida por muestreo sin reemplazo.
- Con batch 8, al entrenar bajó el ruido absoluto y subió el cociente ruido/señal.
- En otra máquina puede cambiar el orden por segundo.
