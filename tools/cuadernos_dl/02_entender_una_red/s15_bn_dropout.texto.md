### celda: s15-intro

## 15 · Batch normalization y dropout

**Batch normalization** (normalización por batch, o BN) ajusta el centro y la escala de lo que entra a cada ReLU. Puede facilitar la optimización y permitir un *learning rate* (tasa de aprendizaje) mayor. **Dropout** (apagado aleatorio) regulariza la red al apagar activaciones durante el entrenamiento.

Las dos capas cambian de comportamiento entre `train()` (modo de entrenamiento) y `eval()` (modo de evaluación). La función `entrenar` calcula las métricas en `eval()`, incluso las de train.

Primero compara las preactivaciones al inicializar y las curvas con y sin BN. Luego compara el control de la §10 con una red que usa dropout. En ambos casos verás qué pasa al predecir la misma imagen en los dos modos.

### celda: s15-bn-formula

En la §5 restaste la media de train a los píxeles y dividiste entre su desviación estándar. Batch normalization aplica esa idea dentro de la red. Durante el entrenamiento, cada neurona usa las preactivaciones del batch actual.

Para la neurona $i$ de la capa $l$, escribe $z^{(l)}_{k,i}$ para su preactivación en la observación $k$ del batch $\mathcal B$. Omitimos el índice de capa en los parámetros y estadísticas de BN.

- Calcula la media $\mu_{\mathcal B,i}=\frac{1}{|\mathcal B|}\sum_{k\in\mathcal B}z^{(l)}_{k,i}$ y la varianza $\sigma^2_{\mathcal B,i}=\frac{1}{|\mathcal B|}\sum_{k\in\mathcal B}(z^{(l)}_{k,i}-\mu_{\mathcal B,i})^2$.
- Estandariza con $\widetilde z^{(l)}_{k,i}=\frac{z^{(l)}_{k,i}-\mu_{\mathcal B,i}}{\sqrt{\sigma^2_{\mathcal B,i}+\varepsilon}}$. El $\varepsilon>0$ evita dividir entre cero.
- Envía $\gamma_i\widetilde z^{(l)}_{k,i}+\beta_i$ a la ReLU. La escala $\gamma_i$ empieza en $1$ y el desplazamiento $\beta_i$ empieza en $0$. Ambos se ajustan con *backpropagation*, igual que los pesos.

$\mu_{\mathcal B,i}$ es una media del batch. El $\mu$ del lagrangeano de la unidad 9 regula la capacidad. Aquí $\beta_i$ es el desplazamiento de BN. En la unidad 9, $\beta$ nombraba los coeficientes de la regresión.

En la red de la clase 1, la capa lineal entrega $\mathbf z^{(l)}_k=\mathbf W^{(l)}\mathbf a^{(l-1)}_k+\mathbf b^{(l)}$. Al insertar BN, queda $\mathbf a^{(l)}_k=\operatorname{ReLU}(\operatorname{BN}(\mathbf z^{(l)}_k))$. Como el sesgo de cada neurona es igual para todo el batch, se cancela al restar la media. El desplazamiento $\beta_i$ permite volver a ajustar el centro.

Busca el orden `Linear` → `BatchNorm1d` → `ReLU` en los módulos impresos. Cada BN agrega $2d_l$ parámetros aprendidos y guarda dos vectores de estadísticas que se actualizan con los batches.

### celda: s15-preact-explica

Antes de actualizar los pesos, pasa el mismo batch de imágenes de train por dos redes con los mismos pesos iniciales ortogonales. La comparación se hace en `train()` para que BN use la media y la varianza de ese batch.

Un *hook* es una función que PyTorch llama al ejecutar un módulo. Aquí se llama justo antes de cada ReLU. El hook lee su entrada y calcula una media y una desviación estándar por capa, sobre todas las imágenes y neuronas del batch. Al terminar se retiran los hooks.

ReLU pone en cero los valores negativos. Al repetir esa operación capa tras capa, la escala puede cambiar. Como viste en las §§13–14, la profundidad también puede hacer que los gradientes se encojan o crezcan. Antes de correr la celda, predice dónde quedarán las barras con BN.

### celda: s15-preact-lee

A la izquierda está la media de lo que entra a cada ReLU. La línea horizontal marca cero. A la derecha está la desviación estándar, con una línea discontinua en uno. El gris identifica la red sin BN y el morado la red con BN. La tabla impresa da los valores de las barras.

Con BN, las barras deberían quedar cerca de esas referencias por cómo se inicializan $\gamma_i$ y $\beta_i$. Sin BN, fíjate si la escala se va reduciendo con la profundidad y cuánto se aparta la media de cero. La dirección del cambio puede variar por capa. Estas barras son una foto al inicializar. Al aprender $\gamma_i$ y $\beta_i$, la red puede ajustar tanto el centro como la escala.

### celda: s15-apuesta

Entrena la red profunda de la §13 con ReLU y SGD sin momentum. Cruza dos *learning rates* con dos versiones de la red, con y sin BN. Las corridas parten de los mismos pesos en las capas lineales y usan el mismo orden de batches.

**Apuesta.** ¿En qué corrida bajará más rápido la *loss*? ¿Cuál podría divergir? Como en la §8, si la loss de un batch se vuelve no finita, `entrenar` registra el paso y detiene la corrida.

### celda: s15-bn-lee

Compara primero dentro de cada fila. Arriba está el *learning rate* menor y abajo el mayor. La columna izquierda es sin BN y la derecha con BN. El eje horizontal cuenta actualizaciones y los paneles comparten la escala vertical. Los colores distinguen train, validation y test.

Con el paso menor, mira si la loss baja más rápido con BN. Con el paso mayor, busca si alguna curva oscila o se corta con el aviso «DIVERGIÓ». La corrida sin BN también puede terminar. En ese caso, compara la velocidad de descenso y cuánto oscila cada curva. La tabla maestra indica si hubo divergencia y muestra la loss y la accuracy de validation en el punto con menor loss de validation.

Al recalcular las estadísticas en cada batch, BN reduce los cambios de escala que llegan a la ReLU cuando se actualizan las capas anteriores. Eso puede facilitar el uso de un paso mayor.

Mirar test en cada evaluación está mal. Test se usa una sola vez, al final. Aquí se muestra solo para aprender a leer las curvas. La elección del mejor punto de cada corrida usa únicamente validation.

### celda: s15-apuesta-respuesta

Con BN, esperarías que la loss bajara más rápido y que el paso grande fuera más estable. Revisa si ocurrió en las dos filas. Si la corrida sin BN con el paso grande dice «terminó», usa la curva para ver si hubo oscilaciones o un descenso más lento. Si ambas curvas son parecidas, esa también es una respuesta.

Vuelve a la «U» del *learning rate* de la §8. Con BN, la zona de pasos que funcionan bien puede desplazarse hacia valores mayores de $\eta$. La rejilla compara los dos pasos ensayados.

### celda: s15-bn-eval

En `train()`, BN normaliza con la media y la varianza del batch. También actualiza los *running averages* (promedios corridos) de esas estadísticas. Si $r$ es el valor guardado, $v$ la estimación del batch y $m$ el `momentum` de BN, el nuevo valor es $(1-m)r+mv$. Para el promedio corrido de la varianza, PyTorch calcula esa estimación con divisor $|\mathcal B|-1$. En `eval()`, la capa usa los valores guardados.

Al predecir, puede llegarte una sola imagen. Como en la unidad 9, una vez ajustado el modelo, la salida depende solo de la entrada $\mathbf x$. Usar estadísticas guardadas cumple el mismo papel que usar la media y la desviación de train en la §5.

La siguiente celda carga el mejor checkpoint de la corrida con BN y el paso menor. Imprime algunas medias y varianzas guardadas de la primera BN. Después compara los *logits* de la misma imagen sola y acompañada por dos grupos distintos. En `eval()`, espera diferencias cercanas a cero por redondeo. En `train()`, las estadísticas cambian con las imágenes que la acompañan y pueden cambiar sus logits. Para una imagen sola, `BatchNorm1d` en modo de entrenamiento exige más de una observación y lanza un error.

### celda: s15-dropout-que-es

En `train()`, **dropout** pone en cero cada activación oculta con probabilidad $p$. El sorteo es independiente para cada activación y se repite en cada pasada. Las activaciones que quedan se multiplican por $1/(1-p)$. Si $a$ es el valor original y $\widetilde a$ el valor con dropout, su promedio sobre los sorteos es $\mathbb E[\widetilde a]=(1-p)\frac{a}{1-p}=a$. En `eval()` pasan todas las activaciones con su valor original.

Con dropout, apoyarse siempre en la misma combinación de neuronas se vuelve más difícil. Eso puede reducir la varianza, en el sentido del balance sesgo-varianza de la unidad 9. Ridge, con el $\mu$ del lagrangeano, y *weight decay* (§9) también limitan la capacidad efectiva del modelo.

La celda aplica `nn.Dropout` a un vector de unos. En `train()` aparecen ceros y unos multiplicados por el factor que imprime el código. Con un vector más largo, el promedio se acerca a uno. En `eval()` salen puros unos. Al final, fíjate dónde va `Dropout` en la red de la §10. Aparece después de cada ReLU oculta.

### celda: s15-dropout-lee

La comparación retoma el control de la §10. Había pocos ejemplos y parte de las etiquetas de train estaban cambiadas. Las etiquetas de validation y test están limpias. Si el control falta, la celda lo vuelve a entrenar y lo avisa. La otra corrida agrega dropout a la misma configuración. Las dos se miden en `eval()`, con la red completa.

En la primera figura, el control está a la izquierda y dropout a la derecha. Arriba está la loss y abajo la accuracy. Los paneles de cada fila comparten la escala vertical. Cada color corresponde a train, validation o test.

En el control, busca si la loss de validation toca un mínimo y luego sube mientras la de train sigue bajando. Ese patrón de *overfitting* (sobreajuste) aparece cuando la red empieza a memorizar incluso las etiquetas cambiadas. Con dropout, espera que la loss de train baje más despacio y que la de validation suba menos o más tarde. Como en la §6, la accuracy puede cambiar poco aunque la loss suba. Basta con que la red gane confianza en sus errores.

Mirar test en cada epoch está mal. Test se usa una sola vez, al final. Aquí se muestra solo para aprender a leer las curvas. La mejor epoch se elige por la menor loss de validation.

En la segunda figura, la línea continua es el control y la discontinua es dropout. A la izquierda se grafica la loss de validation menos la de train. A la derecha, la accuracy de train menos la de validation. La brecha de accuracy puede empezar en negativo porque train se mide contra las etiquetas alteradas. Puede crecer cuando la red empieza a memorizarlas. Comprueba si las brechas crecen más despacio con dropout. La diferencia puede ser pequeña, incluso si cambia la forma de las curvas.

La primera tabla resume la última epoch, incluida la brecha de accuracy. La columna `repite_falsa` mira solo los ejemplos de train con etiqueta alterada y cuenta qué fracción predice la red con la etiqueta **falsa**, como en la §10. Una brecha menor también podría salir de una red que solo aprende más despacio; esta columna dice si de verdad memorizó menos ruido. La tabla maestra muestra las métricas de la mejor epoch por loss de validation. Una brecha más pequeña al final y una accuracy de validation más alta en el checkpoint elegido pueden aparecer por separado.

En la celda siguiente se carga el último checkpoint de la red con dropout y se repite la misma imagen. Compara la probabilidad que la red asigna al dígito real y la clase que predice en cada modo.

### celda: s15-que-viste

### Qué viste

- **Batch normalization.** Al inicializar, centra y ajusta la escala de lo que entra a cada ReLU. Puede ayudar a usar un paso mayor. En `eval()`, las estadísticas guardadas hacen que la salida sea independiente de las otras imágenes del batch.
- **Dropout.** En `train()`, apaga y reescala activaciones al azar. Por eso la probabilidad de la clase real puede variar al repetir la misma imagen. En `eval()`, la salida se repite. En el experimento con etiquetas alteradas, una brecha que crece más despacio es una señal del efecto regularizador.
- **Al evaluar o predecir**, usa `model.eval()`. Así BN usa las estadísticas guardadas y dropout deja pasar todas las activaciones.
