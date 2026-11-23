### celda: s12-intro

## 12 · La forma de la red

![Una red en forma de embudo](ilustracion:embudo)
*(Ilustración generada con gpt-image-2.)*

En la sección 11 variamos el ancho y la profundidad para cambiar el tamaño de la red. Ahora damos a cada red casi el mismo presupuesto, alrededor de 102 mil parámetros. ¿Qué cambia si los repartimos de otra manera entre las capas? La ilustración muestra un embudo que se estrecha capa a capa.

Cada lista empieza con los 784 píxeles de entrada y termina con las 10 salidas, una por dígito. Los números intermedios son los anchos de las capas ocultas.

- **Embudo** `[784, 124, 32, 10]`
- **Embudo invertido** `[784, 96, 248, 10]`
- **Cuello de 2** `[784, 128, 2, 128, 10]`
- **Rectangular** `[784, 112, 112, 10]`
- **Una capa oculta** `[784, 128, 10]`

Como en la red que hicimos a mano, si la capa $l$ tiene ancho $d_l$, su matriz $\mathbf W^{(l)}$ tiene $d_l$ filas (neuronas de destino) y $d_{l-1}$ columnas (entradas de la capa). El vector $\mathbf b^{(l)}$ añade un sesgo por neurona. Al sumar pesos y sesgos de todas las capas obtenemos $\sum_{l=1}^{L} d_l\,(d_{l-1}+1)$ parámetros.

Por ejemplo, la red con una sola capa oculta tiene $128\cdot785 + 10\cdot129 = 100\,480 + 1\,290 = 101\,770$ parámetros. El código imprime los cinco conteos, término por término, y comprueba que coincidan con los de PyTorch. Luego dibuja las cinco redes. En el dibujo de arriba, una capa ancha se abrevia con «⋮» y su ancho real va debajo. Por eso abajo va también la silueta a escala de las capas ocultas y la salida: ahí se ven el embudo, el embudo invertido y el cuello. Fíjate en la primera capa oculta. Cada neurona recibe los 784 píxeles, así que esa capa concentra la mayor parte de los parámetros en las cinco redes.

En la unidad 9 variamos la capacidad del modelo con el grado del polinomio o con la penalización asociada a $\mu$ en el lagrangeano. Aquí veremos cómo dos redes con casi el mismo número de parámetros pueden tener distinta capacidad según dónde los coloquemos.

### celda: s12-apuesta

**Apuesta.** Antes de entrenar, escribe qué forma crees que tendrá la mayor *accuracy* (proporción de aciertos) de validation y cuál tendrá la menor. Justifica tu apuesta en una frase.

En la red con cuello, las capas posteriores reciben solo dos números para distinguir qué dígito había en la imagen. ¿Qué información necesitarían conservar esos números?

### celda: s12-entrenar-explica

Las cinco redes usan Adam con el mismo learning rate $\eta$, el mismo tamaño de batch y el mismo número de epochs. Todas usan ReLU en las capas ocultas e inicialización de He, que ajusta la escala de los pesos iniciales al ancho de entrada de cada capa. También fijamos las semillas de inicialización y del orden de los batches.

Usamos el mismo subconjunto estratificado de train que en la sección 11. Así mantenemos representados todos los dígitos. Evaluamos con validation y test completos. Al mantener la receta de entrenamiento fija, podemos estudiar el efecto de la forma con un presupuesto casi constante.

Otra semilla podría cambiar el orden entre formas con resultados parecidos. Es posible que varias rindan casi igual. Con estas corridas podemos describir las diferencias que veamos.

Por cada corrida, `entrenar` imprime una línea con sus parámetros, sus pasos, su mejor epoch y su accuracy de validation en esa mejor epoch, que es la de menor loss de validation, no necesariamente la última. También imprime cuánto tardó. La tabla maestra registra las cinco corridas con los IDs `s12-embudo`, `s12-invertido`, `s12-cuello`, `s12-rectangular` y `s12-una-capa`.

### celda: s12-curvas-lee

Hay una rejilla de *loss* (pérdida) y otra de accuracy. Cada panel corresponde a una forma. Dentro de cada rejilla, todos los paneles comparten la escala vertical. Puedes comparar alturas para la misma epoch. Azul es train, naranja es validation y verde es test.

Primero compara las curvas naranjas. ¿Quedan cerca las cuatro formas sin cuello? Luego mira el cuello de 2. Busca si tiene mayor loss y menor accuracy también en train. Un ajuste pobre desde train es una señal de *underfitting* (subajuste), como cuando un polinomio de grado bajo tenía demasiado sesgo en la unidad 9. Dentro de cada panel, fíjate también en cuánto se separan las curvas de train y validation.

Mirar test en cada epoch está mal. Test se usa una sola vez, al final, para reportar. Aquí lo graficamos solo para aprender a leer las curvas. Para elegir la mejor epoch y comparar modelos usamos validation.

### celda: s12-apuesta-respuesta

Esperamos que el embudo, el embudo invertido, la red rectangular y la de una sola capa oculta queden cerca en validation. El orden entre ellas puede cambiar con la semilla. Esperamos que la red con cuello tenga más dificultades tanto en train como en validation.

Cada imagen debe pasar por las dos activaciones del cuello. ReLU puede llevar una o ambas a cero. Si dos imágenes de dígitos distintos quedan representadas por el mismo par de números, todas las capas siguientes reciben la misma entrada y producen la misma predicción. Recuerda la gráfica de la sección 11. Allí cada punto representaba una imagen mediante dos activaciones. Busca las zonas donde se mezclan los colores de distintos dígitos.

Un matiz: el cuello no solo es angosto, también es más profundo, con tres capas ocultas en vez de una o dos. Si queda abajo, parte puede deberse a que es más difícil de optimizar, no solo a la información que se pierde; estas curvas solas no separan las dos causas. Si el cuello quedó cerca de las demás formas en tu corrida, registra esa observación. La gráfica muestra cuánto se distinguieron con esta receta y esta semilla.

### celda: s12-que-viste

Para leer las barras, ubica primero la epoch que se eligió con validation en cada corrida. La barra naranja muestra la accuracy de validation en esa epoch y su escala empieza en cero. La barra gris muestra la brecha de accuracy en la misma epoch, train menos validation, en puntos porcentuales. Los valores aparecen en las etiquetas y en la tabla.

Compara con tu apuesta. ¿Quedaron cerca las barras de accuracy y de brecha de las cuatro formas sin cuello? Si el cuello quedó abajo tanto en train como en validation, el patrón apunta a underfitting. Una brecha pequeña también puede darse cuando ambos conjuntos tienen pocos aciertos.

Para estos MLP en MNIST, la accuracy de validation y la brecha pueden variar poco entre las formas sin cuello. Compara esas diferencias con las que viste al cambiar el tamaño de la red o la receta de entrenamiento. Un cuello estrecho puede dificultar el ajuste aunque el presupuesto total sea parecido: el número de parámetros no lo dice todo, importa también por dónde tiene que pasar la información. Si dos formas quedaron casi empatadas, habría que repetir con varias semillas para saber si la diferencia se sostiene.
