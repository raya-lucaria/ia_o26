### celda: s17-intro

## 17 · Una red convolucional, breve

Hasta aquí usamos MLP (*multilayer perceptrons*, redes de capas densas). Un MLP recibe cada dígito como una lista de $784$ píxeles. Si aplicas la misma permutación a todas las imágenes, basta con reordenar las columnas de la primera matriz de pesos para representar la misma función. Para el MLP, la vecindad entre píxeles queda por aprender.

Una CNN (*convolutional neural network*, red convolucional) aprovecha esa vecindad con dos ideas.

- **Localidad.** En la primera convolución, cada valor de salida depende de una ventana de $3\times3$ píxeles vecinos.
- **Pesos compartidos.** Los mismos pesos recorren toda la imagen. Un filtro puede responder al mismo trazo arriba, abajo o en medio.

En la regresión logística de §4, cada fila de $\mathbf W$ era una plantilla del tamaño de la imagen para un dígito. Aquí un filtro es una plantilla pequeña que se aplica en cada posición.

![Un filtro recorriendo un dígito](ilustracion:filtro)
*(Ilustración generada con gpt-image-2.)*

Primero aplicaremos un filtro hecho a mano a un dígito de validation. Verás la entrada, el filtro y su mapa de salida. Después entrenaremos una CNN para mirar qué filtros aprende y medir su accuracy frente al MLP elegido en §16.

### celda: s17-filtro-lee

A la izquierda está el $4$ de validation con dos ventanas marcadas. En el centro están los pesos $w_{uv}$ del filtro, con el renglón $u$ y la columna $v$ rotulados. La columna izquierda vale $-1$, la central vale $0$ y la derecha vale $+1$. A la derecha está el mapa de salida. Los recuadros rojo y morado marcan el máximo y el mínimo, respectivamente. Cada color enlaza la ventana con la posición que le corresponde en la salida. El código imprime la suma de productos junto al valor del mapa para comprobar que coinciden.

Para calcular la salida en el renglón $r$ y la columna $c$, multiplica cada píxel de la ventana por su peso y suma los productos.

$z_{rc}=\sum_{u=-1}^{1}\sum_{v=-1}^{1} w_{uv}\,x_{r+u,c+v}+b$

Es la misma operación de una neurona de §4, aplicada a nueve píxeles vecinos y con los mismos pesos en todos los centros $(r,c)$. En este ejemplo, $b=0$. En la fórmula, $u$ y $v$ son desplazamientos desde el centro. La figura numera los renglones y las columnas del filtro de $0$ a $2$. Con `padding=1`, PyTorch añade un marco de ceros de un píxel. Así el mapa conserva el tamaño de la entrada, $28\times28$.

El filtro suma la tinta de la columna derecha y le resta la de la izquierda. En la entrada, la tinta toma valores cercanos a $1$ y se dibuja oscura. Si hay más tinta a la derecha de la ventana, la salida es positiva y aparece en rojo. Si hay más a la izquierda, la salida es negativa y aparece en azul. Por eso el filtro resalta bordes verticales. Cuando ambas columnas suman casi lo mismo, la salida queda cerca de cero y aparece blanca.

En términos matemáticos, la operación de `conv2d` es una *cross-correlation* (correlación cruzada). PyTorch aplica el filtro tal como está escrito. En la CNN, los pesos y los sesgos de cada filtro se aprenden con backpropagation, igual que los de la red de la clase 1.

### celda: s17-arquitectura-lee

Lee el dibujo de izquierda a derecha. En los bloques de imagen y de mapas, la forma indica canales, alto y ancho. La tabla sigue el mismo recorrido e incluye la dimensión del batch de prueba.

1. **`Unflatten`.** Recupera la cuadrícula de $28\times28$ a partir de los $784$ píxeles de cada imagen. La imagen tiene un canal de entrada porque está en escala de grises.
2. **Primera convolución.** Aplica $16$ filtros de $3\times3$ y produce un mapa por filtro. Esos mapas son los $16$ canales de salida. Cada filtro tiene nueve pesos y un sesgo compartido por todas las posiciones. En total son $16(9+1)=160$ parámetros.
3. **ReLU y max-pooling.** ReLU pone en cero los valores negativos. Luego, *max-pooling* (agrupación por máximo) divide cada mapa en cuadros de $2\times2$ y se queda con el máximo de cada cuadro. El mapa pasa de $28\times28$ a $14\times14$. Si la respuesta más alta se desplaza dentro del mismo cuadro, el máximo puede quedar igual.
4. **Segunda convolución, ReLU y max-pooling.** Cada uno de los $32$ filtros combina una ventana de $3\times3$ de los $16$ canales. Tiene $16\cdot3\cdot3$ pesos y un sesgo, para un total de $32(16\cdot3\cdot3+1)=4\,640$ parámetros en la capa. Después de ReLU y max-pooling, quedan $32$ mapas de $7\times7$.
5. **`Flatten` y `Linear`.** `Flatten` reúne los mapas en una lista de $32\cdot7\cdot7=1\,568$ rasgos. Sobre ellos, la capa densa calcula un logit por dígito, como en §4. Tiene $10(1\,568+1)=15\,690$ parámetros. La loss sigue siendo `CrossEntropyLoss`.

Las dos convoluciones y la capa densa suman $20\,490$ parámetros. La tabla desglosa el conteo por capa. ReLU, max-pooling y los cambios de forma tienen cero parámetros.

### celda: s17-apuesta

**Apuesta.** Esta CNN usa cerca de una quinta parte de los parámetros de la línea base con una capa oculta de $128$ unidades. El MLP elegido en §16 puede tener otro tamaño. Con el mismo conjunto de train y el mismo tamaño de batch, ¿esperas que la CNN gane, empate o pierda en accuracy de validation? ¿Qué red tendrá la mayor brecha entre train y validation hacia el final?

La CNN toma del MLP la escala de entrada, el tamaño de batch y el número de epochs configuradas. También copia el tope de pasos y la frecuencia de evaluación, si están configurados. La CNN usa Adam sin weight decay, con el learning rate que fija el código.

Si saltaste §16, el código busca el MLP disponible con mayor accuracy de validation entre las corridas con los datos completos de train y etiquetas limpias. Si no encuentra uno, avisa y entrena la línea base `s04-oculta`.

Al final de la sección puedes abrir la respuesta y contrastar tu apuesta con las cifras de tu corrida.

### celda: s17-curvas-lee

Arriba está la loss y abajo la accuracy. A la izquierda está el MLP elegido y a la derecha la CNN. Los dos paneles de cada fila comparten la escala vertical. Train va en azul, validation en naranja y test en verde.

**Mirar test en cada epoch está mal.** En un proyecto real, test se usa una sola vez, al final, para reportar. Aquí se grafica solo para aprender a leer las curvas. Las decisiones se toman con validation.

Compara la caída inicial de la loss de validation. Luego mira la brecha entre train y validation hacia el final. Si la loss de train sigue bajando mientras la de validation empieza a subir, tienes una señal de overfitting. Como en la unidad 9, restringir la familia de modelos puede reducir la varianza. Allí podías hacerlo con una penalización controlada por $\mu$. Aquí la arquitectura restringe las conexiones y comparte los pesos.

Para cada red, la tabla usa la epoch de menor loss de validation. En esa epoch reporta la loss, la accuracy y los errores de validation. También muestra el número de parámetros y el tiempo total de entrenamiento. Revisa el optimizer, el learning rate $\eta$ y el weight decay de cada corrida. Si difieren, la comparación recoge también esas diferencias de entrenamiento. Debajo aparecen la diferencia de accuracy en puntos porcentuales y el cociente entre los números de parámetros.

La comparación usa una sola semilla. Una diferencia pequeña podría cambiar con otra. Una CNN puede tardar más por epoch que un MLP pequeño. Usa el tiempo de la tabla para ver qué ocurrió en tu corrida.

### celda: s17-filtros-lee

La primera figura muestra los $16$ filtros de la primera capa en el checkpoint de menor loss de validation. Los ejes indican el renglón $u$ y la columna $v$. Todos los filtros usan la misma escala de color. Rojo indica un peso positivo, azul uno negativo y blanco un peso cercano a cero.

Busca una columna roja junto a una azul. Ese patrón puede responder a un borde vertical, como el filtro hecho a mano. Otros filtros pueden responder a bordes horizontales o diagonales. Algunos pueden verse como manchas y ser difíciles de interpretar. Los pesos se ajustaron para clasificar dígitos.

La segunda figura muestra los *activation maps* (mapas de activación) para el mismo $4$. Cada mapa de $28\times28$ es la respuesta de un filtro después de ReLU, antes de max-pooling. Los tonos claros marcan valores mayores dentro de ese mapa. Como cada mapa tiene su propia escala, compara dónde aparece la respuesta y qué forma dibuja. Si todos los valores de un mapa son cero, ReLU apagó todas las respuestas del filtro a ese dígito.

Fíjate si algún mapa resalta un borde o una parte del trazo. La imagen de referencia se muestra con píxeles entre $0$ y $1$. La CNN recibe el mismo dígito en la escala con la que entrenó. Si esa escala es la estandarizada, el fondo tiene un valor distinto de cero y también puede activar un filtro. Tras max-pooling, la segunda convolución combina la información de todos esos canales.

### celda: s17-que-viste

Las dos matrices de confusión se calculan en validation con el mejor checkpoint de cada red. A la izquierda está el MLP y a la derecha la CNN. **Las filas son las clases reales y las columnas son las clases predichas.** Cada casilla muestra un conteo. Los aciertos se leen en gris en la diagonal. El rojo destaca los errores y usa la misma escala en ambas matrices.

Compara los totales de error en los títulos. Luego elige una casilla roja y busca la misma fila y columna en la otra matriz. Por ejemplo, la fila del $4$ y la columna del $9$ cuentan los cuatros predichos como nueves. Revisa también la confusión en sentido inverso. Fíjate si la CNN reduce los errores en los mismos pares o si disminuyen en unos y aumentan en otros. En la tabla por clase real, una diferencia CNN $-$ MLP negativa indica que la CNN se equivocó menos en ese dígito.

La CNN incorpora una suposición sobre los datos. Los píxeles cercanos forman rasgos y un mismo rasgo puede servir en distintos lugares. Si esa suposición encaja, restringir la arquitectura puede reducir la varianza sin aumentar mucho el sesgo. Medimos el resultado en validation con una sola semilla. En §19, la CNN aparecerá en la tabla maestra con las demás corridas.

### celda: s17-apuesta-respuesta

La respuesta sale de tu corrida. En la tabla de curvas, una diferencia de accuracy positiva favorece a la CNN y una negativa favorece al MLP. Para la segunda parte de la apuesta, compara la distancia entre train y validation en los paneles de accuracy hacia el final. Las matrices muestran qué confusiones cambiaron.

En MNIST es razonable esperar que esta CNN iguale o supere la accuracy del MLP y que su brecha sea menor. Con una sola semilla, pocas epochs y un MLP fuerte, la diferencia puede ser pequeña o favorecer al MLP. La proporción impresa te dice cuánto cambia el número de parámetros frente al MLP que se usó.

El conteo de parámetros dice cuántos valores se ajustan. La arquitectura determina cómo se combinan. Al compartir los pesos, la CNN puede reaprovechar en toda la imagen un rasgo que aprendió a reconocer en una ventana.
