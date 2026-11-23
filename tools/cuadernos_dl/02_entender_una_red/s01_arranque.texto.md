### celda: s01-intro

## 01 · Arranque

Aquí preparamos las bibliotecas, el dispositivo, las semillas y las gráficas.
El entrenamiento empieza más adelante.

- PyTorch, que importamos como `torch`, trabaja con tensores (arreglos de
  números). Calcula el gradiente de la loss respecto a los parámetros.
  Hace automáticamente la *backpropagation* (retropropagación) que
  programaste a mano en el notebook 01.
- Torchvision proporciona MNIST.
- Como en la unidad 9, usamos NumPy para operaciones con arreglos, pandas
  para tablas y Matplotlib para gráficas.

### celda: s01-gpu-explica

Entrenar una red implica multiplicar matrices una y otra vez. Una GPU
(unidad de procesamiento gráfico) puede hacer muchas de esas operaciones
en paralelo. `DEVICE` indica dónde se guardan y se operan los tensores.
`cuda` indica una GPU de NVIDIA y `cpu`, el procesador de propósito general.

**Si aparece «ESTE ENTORNO NO TIENE GPU»**, en Colab elige **Entorno de
ejecución → Cambiar tipo de entorno → T4 GPU → Guardar** y vuelve a
seleccionar **Ejecutar todo**. Sin GPU, el notebook sigue en CPU con
`RAPIDO`. Ese modo recorta los datos y limita el entrenamiento, así que
sus curvas pueden verse distintas de las de clase. Para hacer la misma
prueba local, puedes fijar la variable de entorno `RAPIDO=1`. El modo
rápido usa CPU aunque detecte una GPU.

Si está disponible, `nvidia-smi` muestra el modelo de GPU y su memoria.
La salida también identifica qué versión de PyTorch se está usando, con
qué versión de CUDA se compiló y qué versión de cuDNN detecta si hay GPU.
Guarda esa información si necesitas reproducir una corrida o reportar
un problema.

### celda: s01-semillas-explica

Una semilla fija el punto de partida del azar, como en la unidad 9. La
caja separa dos decisiones. `semilla_init` fija los pesos iniciales y
`semilla_orden` fija el orden de los batches. Así puedes conservar los
mismos pesos de partida y cambiar el orden de los datos. Algunas operaciones
en GPU pueden variar un poco entre ejecuciones aunque fijes las semillas.
Al comparar corridas, fíjate en las tendencias de las curvas.

Las gráficas usan fondo claro y rejilla suave, como en el notebook 01.
`COLORES` asigna azul a train, naranja a validation y verde a test.
