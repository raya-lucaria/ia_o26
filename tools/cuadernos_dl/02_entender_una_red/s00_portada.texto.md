### celda: s00-portada

# Notebook 2 · Entender una red entrenándola

Unidad 10 de *deep learning* (aprendizaje profundo), clase 2. En el
notebook 01, «Una red desde cero», construiste una red 2–3–2–1 a mano en
NumPy. Aquí vas a entrenar una red con PyTorch para reconocer dígitos
escritos a mano del conjunto MNIST.

**Cómo ejecutarlo.** Abre el notebook en Colab. Elige **Entorno de ejecución
→ Cambiar tipo de entorno → T4 GPU → Guardar**. Luego selecciona **Entorno
de ejecución → Ejecutar todo**. En una T4, la ejecución completa está
estimada en unos 20 minutos. Puedes leer de arriba hacia abajo mientras
corre. Si Colab arranca sin GPU, verás un aviso y se activará el modo
`RAPIDO`. Sus gráficas salen de una prueba con menos datos y menos pasos.

- Separa los datos y lee el código que vas a usar para entrenar.
- Pasa de la regresión logística a una red con capas ocultas. Compara
  escalas de entrada y aprende a leer las tres curvas.
- Prueba cómo cambia el *gradient descent* (descenso de gradiente) con el
  tamaño del *batch* (lote), el *learning rate* (tasa de aprendizaje) y el
  *optimizer* (optimizador). Usa *early stopping* (parada temprana) para
  detener el entrenamiento cuando deja de mejorar en validación.
- Cambia el tamaño, la forma y las activaciones de la red. Mira el gradiente
  en cada capa y prueba *batch normalization* (normalización por lote) y
  *dropout* (desactivación aleatoria de unidades).
- Examina los errores y prueba una red convolucional. Después, mira cómo
  *softmax* (normalización exponencial) convierte las salidas en
  probabilidades y cómo se calcula la *loss* (pérdida). La tabla maestra
  reúne las corridas al final.

Como en la unidad 9, ajusta los parámetros con *train* (entrenamiento) y
toma las decisiones con *validation* (validación). En un proyecto, usa
*test* (prueba) una sola vez, al final. Aquí verás su curva en cada *epoch*
(época, una pasada por los datos de entrenamiento) solo para practicar la
lectura de las tres curvas.

Busca «Qué viste» para comprobar cómo leer las salidas. En las secciones
con una apuesta, escribe tu predicción antes de correr la celda. Luego
abre la respuesta plegada y compárala con lo que observaste.
