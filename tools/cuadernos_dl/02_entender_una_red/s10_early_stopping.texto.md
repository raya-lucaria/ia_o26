### celda: s10-intro

## 10 · Early stopping

La red tiene dos capas ocultas de 256 neuronas y entrena 80 epochs con 2000 imágenes.
Cambiamos al azar el 20 % de las etiquetas de train para observar si la red las memoriza.
Validation y test conservan las etiquetas verdaderas.
**Early stopping usa la loss de validation para decidir cuándo parar.** Cada nuevo mínimo guarda un checkpoint.

![Parar a tiempo](ilustracion:parar_a_tiempo)
*(Ilustración generada con gpt-image-2.)*

### celda: s10-apuesta

**Apuesta.** ¿La loss de train bajará siempre o tendrá repuntes? ¿La de validation seguirá bajando o volverá a subir?
Al final, ¿la red repetirá pocas, muchas o todas las etiquetas falsas de train?

### celda: s10-apuesta-respuesta

Al principio mejoró la clasificación en validation. Después, su loss subió mientras la de train seguía bajando, con repuntes.
**La red terminó repitiendo todas las etiquetas falsas de train.**
En otra corrida podría memorizar solo parte de ellas.

### celda: s10-paciencia-explica

La simulación cuenta evaluaciones consecutivas sin bajar la loss de validation. Un empate cuenta como falta de mejora.
**Al agotar la paciencia, se recupera el mejor checkpoint hasta la parada.**
Aquí ese checkpoint también fue el mejor de las 80 epochs del control.
En otra corrida puede aparecer un mínimo posterior a la parada.

### celda: s10-memoriza-explica

La línea negra marca el mínimo de validation y la roja, la parada simulada. La sombra indica las epochs ahorradas.
**La barra de etiquetas falsas mide memorización.** Compara cuánto crece del mejor checkpoint al último.
Entre las imágenes con etiquetas alteradas, fíjate también en cuántas reciben su etiqueta verdadera.

### celda: s10-restaurar-explica

**El mejor checkpoint se elige por loss de validation.** Compara sus métricas con las del último.
Train usa las etiquetas vistas al entrenar. Validation y test usan las verdaderas.
Aquí test se muestra con fines didácticos (§6). En un proyecto se usa una vez al final para reportar.

### celda: s10-corrida-paciencia-explica

Repetimos la corrida con paciencia de seis evaluaciones y las mismas semillas.
**La parada real coincidió con la simulada.** Ambas recuperaron el mejor checkpoint del control.
Pequeñas diferencias numéricas en GPU pueden cambiar la parada.

### celda: s10-que-viste

- **El overfitting separó las curvas.** La loss de train siguió bajando y la de validation subió tras su mínimo.
- El último checkpoint repitió más etiquetas falsas y acertó menos en validation.
- Early stopping recuperó el checkpoint previo a ese deterioro. En §15 compararemos cuánto ruido memoriza la red con dropout.
