### celda: s11-intro

## 11 · El tamaño de la red

¿Qué pasa con la accuracy (proporción de aciertos) de validation si hacemos la red más ancha o más profunda? En la unidad 9, aumentar el grado $N$ de un polinomio le daba más capacidad para ajustar los datos. Aquí cambiamos el ancho $d_l$, que es el número de neuronas de la capa $l$, y la profundidad, que aquí cuenta las capas ocultas. En cada red, todas las capas ocultas tienen el mismo ancho $d$. La arquitectura es $[784,d,\ldots,d,10]$.

Como en la red 2–3–2–1 de la clase pasada, la capa $l$ tiene $d_l d_{l-1}$ pesos en $\mathbf W^{(l)}$ y $d_l$ sesgos en $\mathbf b^{(l)}$. En total hay $\sum_{l=1}^{L}(d_{l-1}+1)d_l$ parámetros, incluida la salida. Por ejemplo, $[784,2,10]$ tiene $785\cdot 2+3\cdot 10=1600$ parámetros. La primera celda muestra el conteo de toda la rejilla y lo comprueba con PyTorch para una de las redes.

Cruzamos los anchos 2, 16, 64, 256 y 1024 con 1, 2, 4 y 8 capas ocultas. Todas las redes usan el mismo subconjunto fijo de train, con el mismo número de imágenes de cada dígito, y se evalúan sobre toda validation. Todas usan ReLU, el optimizer Adam con learning rate $\eta=10^{-3}$, batch de 128 y cinco epochs. El subconjunto es de 20 000 imágenes de train, menos que las 50 000 disponibles, para que las 20 redes quepan en el tiempo de la clase.

Con la inicialización He, los pesos de la capa $l$ se sortean con varianza $2/d_{l-1}$. Para ReLU, esa escala ayuda a que la señal conserve su magnitud al inicio, algo especialmente importante cuando atraviesa varias capas.

Comparamos el rendimiento al final del mismo presupuesto de epochs. Con más entrenamiento, las redes podrían rendir de otra manera. El modo rápido recorta los datos y el entrenamiento.

### celda: s11-apuesta

Escribe tu apuesta antes de ejecutar la celda siguiente.

1. ¿Qué combinación de ancho y profundidad tendrá la menor accuracy de validation?
2. ¿Subirá siempre la accuracy de validation al pasar de ancho 256 a 1024 o de 4 a 8 capas?
3. ¿Tendrá la red más grande, de ancho 1024 y 8 capas ocultas, la mayor brecha entre train y validation?

La celda entrena las 20 redes de la rejilla y puede tardar unos minutos en la T4.

### celda: s11-mapas-lee

Cada fila corresponde a una profundidad y cada columna a un ancho. Cada casilla muestra el último valor registrado para esa red.

- **Izquierda.** El color más claro indica mayor accuracy de validation. Empieza por la columna de ancho 2. Luego recorre una fila de izquierda a derecha y busca dónde empiezan a parecerse los colores.
- **Derecha.** La brecha se calcula restando la accuracy de validation a la de train. En rojo, la red acierta más en los ejemplos que usó para entrenar. En azul, acierta más en validation. El blanco indica una brecha cercana a cero.

Como en la unidad 9, una brecha positiva grande puede ser señal de overfitting (sobreajuste). Compara si la brecha crece con el ancho o la profundidad. Con un entrenamiento corto, puede ser pequeña en toda la rejilla.

### celda: s11-apuesta-respuesta

1. Busca las accuracies más bajas en la columna de ancho 2. La red de 8 capas puede tener más dificultades. Si una ReLU queda en cero para casi todos los ejemplos, por esa neurona tampoco pasa el gradiente para esos ejemplos. En una red estrecha, eso deja pocas rutas para la señal y el gradiente.
2. Es común que, a partir de cierto tamaño, añadir neuronas o capas cambie poco la accuracy de validation. Comprueba si aparece esa meseta. Con una sola corrida por red, otra semilla podría invertir el orden entre casillas cercanas.
3. La brecha puede crecer con el tamaño, aunque también puede seguir pequeña con este presupuesto. Con más epochs podría aumentar.

### celda: s11-parametros-lee

Cada punto es una red. Su altura indica la accuracy de validation y el número junto al punto indica el ancho. Cada línea reúne las redes con la misma profundidad. El eje horizontal usa escala logarítmica. Entre marcas consecutivas de potencias de diez, el conteo se multiplica por diez. Así se ven juntos conteos de miles y de millones de parámetros.

Busca si la accuracy sube al salir del ancho 2 y en qué tramo se aplana. Una línea casi horizontal indica que añadir muchos parámetros apenas cambió el resultado con este presupuesto. Compara también puntos de distintas líneas que queden cerca en el eje horizontal. Su altura muestra cómo rindieron redes de forma distinta con conteos parecidos.

### celda: s11-dibujos-lee

Una accuracy baja admite dos explicaciones. La red puede tener poca capacidad para representar lo que distingue a los dígitos. También puede ser difícil ajustar sus pesos con el presupuesto disponible. En una red profunda y estrecha, el gradiente tiene que atravesar muchas capas y una ReLU en cero puede cortarle el paso. El mapa reúne ambos efectos. En las secciones 13 y 14 miraremos el gradiente por capa para entender mejor la parte de optimización.

Los dibujos muestran cuatro redes de la rejilla. Sus pares de ancho y profundidad son $(2,1)$, $(64,2)$, $(1024,1)$ y $(64,8)$. Cada columna de nodos es una capa. Los puntos suspensivos indican que solo se dibujaron algunas neuronas. Debajo aparece el tamaño real de la capa. El título da el conteo de parámetros y la accuracy de validation. Ubica en la gráfica anterior la red más ancha y la de ocho capas. Compara sus conteos y sus accuracies.

### celda: s11-cuello-intro

En $[784,2,10]$, toda la información de una imagen de 784 píxeles pasa por dos neuronas antes de que la salida decida entre los diez dígitos. Sus dos activaciones forman las coordenadas de un punto. Podemos dibujar un punto por cada imagen de validation y colorearlo por su dígito verdadero.

Reutilizamos esa red de la rejilla y entrenamos $[784,256,2,10]$ con los mismos datos y el mismo presupuesto. La capa de 256 neuronas puede aprender rasgos de la imagen antes de comprimirla en el cuello.

Cada fila muestra una red. A la izquierda están las dos preactivaciones $\mathbf z$, calculadas con los pesos y sesgos del cuello. A la derecha están las activaciones $\mathbf a=\operatorname{ReLU}(\mathbf z)$, los dos valores que recibe la capa de salida. La ReLU convierte los valores negativos en cero. Por eso pueden acumularse puntos en los ejes o en el origen. Si una neurona queda en cero para casi todas las imágenes, la salida depende casi siempre de la otra. La celda imprime la fracción de validation con cada neurona en cero y con ambas en cero, y cuántas imágenes de cada dígito caen en el origen. Los puntos se dibujan en orden aleatorio para que ningún dígito tape siempre a los demás; aun así, en el origen los puntos se enciman y esa cuenta dice qué hay debajo.

### celda: s11-cuello-lee

Si los colores ocupan regiones separadas, la salida tiene más información para distinguir esos dígitos. Si dos imágenes de dígitos distintos llegan al mismo punto en $\mathbf a$, reciben la misma predicción. Donde los colores se mezclan, distinguirlos puede ser más difícil.

Compara los paneles de $\mathbf z$ y $\mathbf a$. Dos puntos separados por un valor negativo pueden acabar en el mismo lugar cuando la ReLU pone ese valor en cero. Mira si la capa de 256 neuronas ayuda a separar los colores después de la ReLU. También puede haber acumulación en los ejes. Usa las fracciones de ceros para comprobar cuánto ocurre. Si casi todas las imágenes caen en el origen, la capa de salida recibe lo mismo para todas y la accuracy se queda cerca del 10 % del azar. Además, una ReLU en cero no deja pasar gradiente, así que esa red ya no puede salir de ahí: es una falla de optimización, no solo de capacidad.

El cuello ayuda a interpretar la columna de ancho 2 del mapa. En esas redes, cada capa oculta debe transmitir lo que sabe sobre la imagen en solo dos valores. La sección 12 pone un cuello similar entre dos capas anchas.

### celda: s11-que-viste

Vuelve a tu apuesta. ¿En qué tramo ayudó agrandar la red? ¿Observaste algún tramo casi horizontal, donde agrandar ya no cambió la accuracy de validation? ¿Creció también la brecha con train? Con una sola semilla por arquitectura, toma las diferencias pequeñas como resultados de esta corrida. El cuello muestra qué información llega a la salida. La rejilla por sí sola deja abierta la pregunta de si una accuracy baja se debe a la capacidad o a la optimización.

La tabla reúne los parámetros, las accuracies finales de train y validation, la brecha y los segundos de entrenamiento. También indica si una corrida divergió. Son 21 filas: las 20 de la rejilla y la red $[784,256,2,10]$ del cuello. Debajo de la tabla se imprime el tiempo total de la sección.

En la sección 12 cambiaremos la forma de la red con un número de parámetros parecido.
