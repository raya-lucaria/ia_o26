### celda: s01-intro

## 01 · Arranque

- **PyTorch automatiza la backpropagation** que programaste a mano en el notebook 01.
- Torchvision carga MNIST. NumPy maneja arreglos, pandas arma tablas y Matplotlib dibuja gráficas.

### celda: s01-gpu-explica

- Una GPU acelera las multiplicaciones de matrices al hacerlas en paralelo. `DEVICE` indica dónde se hacen.
- **Si Colab avisa que falta la GPU**, elige T4 GPU en «Cambiar tipo de entorno» y vuelve a ejecutar todo.
- `RAPIDO` usa CPU, recorta los datos y limita el entrenamiento. Para activarlo localmente, fija `RAPIDO=1`.
- Guarda las versiones que imprime la celda si necesitas reproducir una corrida.

### celda: s01-semillas-explica

- **Dos semillas controlan decisiones distintas.** `semilla_init` fija los pesos iniciales y `semilla_orden` fija el orden de los batches.
- Con las mismas semillas, aún puede haber variaciones en GPU. Compara las tendencias.
- En las gráficas, azul es train, naranja es validation y verde es test.
