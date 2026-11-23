### celda: s10-intro

## 10 · Early stopping

- Dos capas ocultas de 256 neuronas, 2000 imágenes y 80 epochs.
- Cambiamos al azar el 20 % de etiquetas de train. Validation y test conservan las verdaderas.
- **Early stopping vigila la loss de validation.** Cada nuevo mínimo guarda un checkpoint.

![Parar a tiempo](ilustracion:parar_a_tiempo)
*(Ilustración generada con gpt-image-2.)*

### celda: s10-apuesta

- **Apuesta.** ¿Bajará la loss de train sin repuntes? ¿La de validation seguirá bajando o volverá a subir?
- ¿La red repetirá pocas, muchas o todas las etiquetas falsas?

### celda: s10-apuesta-respuesta

- La loss de validation bajó y volvió a subir. La de train siguió bajando, con repuntes.
- **La red acabó repitiendo todas las etiquetas falsas.** En otra corrida podría memorizar solo parte.

### celda: s10-paciencia-explica

- La paciencia cuenta evaluaciones consecutivas sin un nuevo mínimo de loss de validation, incluidos los empates.
- **Al agotar la paciencia, se recupera el mejor checkpoint hasta la parada.**
- Aquí coincidió con el mejor del control. En otra corrida puede haber un mínimo posterior a la parada.

### celda: s10-memoriza-explica

- Línea negra para el mínimo de validation, roja para la parada y sombra para las epochs ahorradas.
- **La barra de etiquetas falsas mide memorización.** Compara el mejor checkpoint con el último.
- En las imágenes con etiquetas alteradas, compara también los aciertos de la etiqueta verdadera.

### celda: s10-restaurar-explica

- **El checkpoint se elige por loss de validation.**
- Train se evalúa con las etiquetas usadas al entrenar. Validation y test usan las verdaderas.
- Test se muestra con fines didácticos (§6) y se reserva para el informe final.

### celda: s10-corrida-paciencia-explica

- **La parada real coincidió con la simulada.** Diferencias numéricas en GPU pueden moverla.

| Corrida | Qué hace | Qué se ve en validation |
| --- | --- | --- |
| Control | Agota las epochs | La curva sube tras el mínimo |
| Con paciencia | Para tras seis evaluaciones sin mejora | La curva acaba en la línea roja |

### celda: s10-que-viste

- **El overfitting separó las curvas.** La loss siguió bajando en train y repuntó en validation.
- El último checkpoint repitió más etiquetas falsas y acertó menos en validation.
- Early stopping recuperó el mejor checkpoint del control. En §15 compararemos cuánto ruido memoriza la red con dropout.
