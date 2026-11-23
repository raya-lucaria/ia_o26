### celda: s14-intro

## 14 · El gradiente por capa (avanzado)

Esta sección es opcional en una primera lectura. Puedes seguir con la §15.

Durante el entrenamiento, **batch normalization** (normalización por batch) usa la media y la desviación estándar del batch para dejar la preactivación de cada neurona oculta con media cero y varianza cercana a uno. Después aplica una escala y un desplazamiento aprendidos por neurona. Todo esto ocurre antes de la activación. En la §15 veremos cómo funciona.

Partimos de la misma arquitectura profunda de la §13, con inicialización ortogonal, sesgos iniciales en cero y el mismo learning rate $\eta$ para SGD. Comparamos sigmoide, ReLU y ReLU con batch normalization. Una cuarta corrida, sigmoide con Adam, aparece solo al final, en el cambio relativo de los pesos. ¿Cuánto gradiente recibe cada capa? ¿Qué pasa con el gradiente conforme baja la loss? ¿Cuánto cambian los pesos en cada paso respecto a su tamaño?

Retoma el cálculo de backpropagation de la clase 1. Sin batch normalization, para pasar el error a la capa anterior usamos $\mathbf{δ}^{(l)} = \bigl((\mathbf W^{(l+1)})^\top \mathbf{δ}^{(l+1)}\bigr)\odot g^{(l)\prime}(\mathbf z^{(l)})$. La matriz de pesos mezcla los errores de la capa siguiente y $\odot$ aplica la derivada de la activación componente a componente. Con la sigmoide, esa derivada vale a lo sumo $1/4$. El efecto se acumula capa tras capa.

### celda: s14-que-medimos

En un paso de SGD usamos la loss promedio $L_{\mathcal B}$ del mini-batch $\mathcal B$. El gradiente $\nabla_{\mathbf W^{(l)}}L_{\mathcal B}$ tiene la misma forma que la matriz de pesos $\mathbf W^{(l)}$: $d_l$ filas para las neuronas de destino y $d_{l-1}$ columnas para las de origen.

Para resumir el gradiente de la capa usamos su norma de Frobenius. Elevamos al cuadrado cada entrada, sumamos y sacamos la raíz: $\lVert\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\rVert_F = \sqrt{\sum_{i,j}\bigl(\partial L_{\mathcal B}/\partial w^{(l)}_{ij}\bigr)^2}$. Es un solo número que mide la magnitud del gradiente de los pesos de la capa.

Con `medir_por_paso=True`, `entrenar` guarda en `corrida.por_paso` el paso, la capa, la norma del gradiente y el cambio relativo de los pesos. Medir en cada paso añade trabajo al entrenamiento. La primera capa está junto a la entrada. La última produce los logits que usa la loss.

La primera celda entrena las cuatro corridas y muestra sus filas en la tabla maestra. La segunda grafica la loss de train y validation contra el número de actualizaciones. Mira cuánto baja la loss antes de comparar los gradientes. La línea punteada marca $\log 10$, la cross-entropy de asignar la misma probabilidad a cada dígito.

### celda: s14-apuesta

**Apuesta.** En la red con sigmoide, ¿en qué capa esperas ver el gradiente más chico: en la primera, junto a la entrada, o en la última, junto a la salida? ¿Qué esperas con ReLU?

Escribe tu predicción y una razón antes de abrir la respuesta y correr la gráfica.

### celda: s14-apuesta-respuesta

Con sigmoide esperamos un gradiente mucho más chico en la primera capa. Al retroceder por cada capa oculta, la derivada de la sigmoide aporta un factor de a lo sumo $1/4$. Aplicar esa reducción varias veces puede dejar un gradiente diminuto cerca de la entrada. A esto se le llama *vanishing gradient* (desvanecimiento del gradiente).

Con ReLU la derivada vale $0$ o $1$. Las componentes que pasan por una ReLU activa conservan su escala en ese paso. La inicialización ortogonal también ayuda a conservar la escala al multiplicar por las matrices de pesos. Esperamos normas más parejas con ReLU, tanto con batch normalization como sin ella. Comprueba en la gráfica si ocurre.

### celda: s14-leer-norma

Cada panel corresponde a una de las tres corridas con SGD. El eje horizontal cuenta las actualizaciones. Los tres paneles comparten un eje vertical logarítmico. Una separación de una potencia de diez equivale a un factor de diez.

Cada color identifica una capa. La primera es la más oscura y la de salida, la más clara. La línea tenue muestra los valores de cada paso. Pueden saltar al cambiar de mini-batch. La línea gruesa muestra una media móvil centrada, calculada sobre el logaritmo y convertida de vuelta a la escala original. La figura usa los valores positivos y finitos.

Primero compara la primera capa con la de salida dentro de cada panel. Si la primera queda varios órdenes de magnitud por debajo, el gradiente se ha atenuado al retroceder por la red. Luego sigue las líneas hacia la derecha y compara su evolución entre corridas. Para leer los valores, usa la tabla de medianas de todo el entrenamiento. Las filas son capas y las columnas son corridas.

### celda: s14-norma-que-viste

Con sigmoide, busca si las primeras capas quedan muy por debajo de la salida y si la loss se mantiene cerca de la referencia uniforme. Con el mismo $\eta$, un gradiente chico produce un cambio chico en los pesos en cada paso de SGD.

Con ReLU, busca capas más parejas y una caída más clara de la loss. Con batch normalization, busca si las normas quedan mucho más juntas que con la sigmoide. El orden puede cambiar: puede que las primeras capas reciban incluso más gradiente que la salida. Al reescalar las preactivaciones, batch normalization cambia la escala de los gradientes durante backpropagation.

Las dos variantes con ReLU pueden verse muy parecidas. Con inicialización ortogonal y la profundidad de este experimento, ReLU puede funcionar bien por sí sola. En la §15 probaremos un learning rate mayor. Fíjate también si alguna norma sube al principio mientras la loss baja. Es común: al inicio la red predice casi lo mismo para todo, y cuando empieza a separar los dígitos el gradiente crece. La norma puede subir y bajar durante el entrenamiento.

### celda: s14-va-a-cero

Cuando baja la loss, ¿el gradiente se acerca a cero? En los ejemplos de gradient descent de la unidad 9 y la clase 1 calculábamos el gradiente de la loss completa. En un mínimo interior donde la loss es diferenciable, ese gradiente vale cero. Aquí SGD calcula un gradiente con cada mini-batch.

Para los mismos parámetros $\theta$ podemos calcular el gradiente completo $\mathbf g_{\text{completo}}=\nabla_\theta L(\theta)$ sobre todo train y el gradiente $\mathbf g_{\mathcal B}=\nabla_\theta L_{\mathcal B}(\theta)$ sobre un mini-batch. Ambos son vectores que juntan las derivadas respecto a todos los pesos y sesgos. Como en la §7, con pesos fijos y batches tomados al azar de train, el gradiente de mini-batch coincide en promedio con el completo. Su diferencia en un batch particular es el ruido del gradiente.

Volvemos a entrenar la red de `s14-relu` con la misma configuración y los mismos pesos iniciales. El loop de esta celda puede recorrer los batches en otro orden. Guarda copias de los parámetros al inicio, a la mitad y al final. En cada copia congelamos los parámetros y calculamos el gradiente de todo el conjunto de train usado en la corrida y los de una colección de mini-batches. Reutilizamos los mismos mini-batches en los tres momentos. Usamos ReLU sin batch normalization porque, con ella, el gradiente aportado por cada ejemplo depende de qué otros ejemplos están en el batch.

La función `gradiente` limpia `.grad` al empezar. Para cada bloque, suma las pérdidas y divide entre $n$, el número total de ejemplos del conjunto que se está midiendo. Cada llamada a `backward()` acumula su aporte en `.grad`. La suma da el gradiente de la loss promedio y permite calcularlo por bloques.

### celda: s14-cero-que-viste

En el panel izquierdo, el eje vertical está en escala logarítmica. En cada momento, el rombo azul marca $\lVert\mathbf g_{\text{completo}}\rVert$ y la cruz negra marca la mediana de $\lVert\mathbf g_{\mathcal B}-\mathbf g_{\text{completo}}\rVert$, nuestra medida del ruido. La caja gris abarca la mitad central de las normas $\lVert\mathbf g_{\mathcal B}\rVert$. La raya marca su mediana. Los valores más alejados de la caja aparecen como puntos fuera de los bigotes.

A la derecha está la loss de train para los mismos parámetros congelados. La tabla reúne esa loss, la norma del gradiente completo y las medianas de las normas del gradiente de mini-batch y del ruido.

No esperes que las normas bajen desde el inicio. Al principio la loss está cerca de $\log 10$ y la red apenas empieza a moverse; cuando aprende rápido, el gradiente puede crecer. Lo que suele verse es que los dos gradientes suben primero y bajan después, mientras la loss baja todo el tiempo. Compara la mitad con el final: ahí los dos bajan. Si el rombo queda por debajo de la caja y la cruz queda cerca de ella, la variación entre mini-batches domina el gradiente típico de un mini-batch. Con un learning rate fijo, SGD puede seguir dando pasos apreciables aun cuando el gradiente completo sea pequeño.

Ninguno de los dos tiene garantizado llegar a cero. El de mini-batch, además, queda dominado por el ruido: aunque la señal $\mathbf g_{\text{completo}}$ se haga chica, el ruido entre batches puede seguir ahí, y por eso $\lVert\mathbf g_{\mathcal B}\rVert$ no llega a cero. Una red puede pasar por zonas planas de la loss. Con cross-entropy también puede seguir bajando la loss al dar más probabilidad a las clases correctas, aun con un gradiente pequeño. Para decidir cuándo parar con *early stopping*, seguimos la loss de validation, como en la §10.

### celda: s14-cociente

Ahora mide cuánto cambian los pesos de la capa $l$ en el paso $t$ en proporción a su tamaño. El cociente es $\lVert\mathbf W^{(l)}_{t+1}-\mathbf W^{(l)}_t\rVert_F / \lVert\mathbf W^{(l)}_t\rVert_F$. Está en la columna `cociente_actualizacion` de `corrida.por_paso`.

Con el SGD sin momentum de estas corridas, la diferencia de pesos es $-\eta\,\nabla_{\mathbf W^{(l)}}L_{\mathcal B}$, calculada antes de actualizar. Así, el numerador es la norma del gradiente multiplicada por $\eta$. Adam usa promedios de gradientes pasados y reescala la actualización de cada parámetro. En ese caso, medir la diferencia real de pesos captura el paso que dio el optimizer. Por eso la figura trae un cuarto panel: la misma red con sigmoide, entrenada con Adam ($\eta = 10^{-3}$). Su gradiente se desvanece igual que con SGD, pero Adam divide el paso de cada peso entre la escala típica de su propio gradiente.

Un cociente pequeño indica que los pesos cambian poco en ese paso. Uno grande indica un cambio fuerte respecto al tamaño de los pesos y puede acompañar un entrenamiento inestable. La línea gris discontinua en $10^{-3}$ marca una milésima. Es una regla práctica de la comunidad para orientarte, no una ley: no decide nada por sí sola.

Lee la figura como la de normas. Los cuatro paneles comparten la escala logarítmica. Cada capa tiene su serie tenue por paso y su media móvil gruesa.

### celda: s14-que-viste

Vuelve a comparar las primeras capas con la de salida. Con sigmoide, espera que las primeras cambien órdenes de magnitud menos que la salida, aun con el mismo learning rate. Con las dos variantes de ReLU, busca cambios relativos más parejos y mira si también se acercan a la referencia gris. En el panel de Adam, compara las primeras capas con las del panel de sigmoide con SGD: si quedan mucho más cerca de la salida, Adam está compensando el gradiente diminuto. Que se muevan no garantiza que la red aprenda: revisa su loss en la gráfica de curvas.

Relaciona esa figura con las anteriores. La gráfica de normas muestra dónde se atenúa el gradiente. El cociente muestra cuánto se mueven los pesos. Los parámetros congelados permiten ver cuánto se desvía el gradiente de mini-batch del completo a medida que baja la loss. Si tus gráficas muestran otra tendencia, describe lo que ves y apóyate en la tabla correspondiente.
