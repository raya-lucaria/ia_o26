### celda: s07-intro

## 07 · Gradient descent y el tamaño del batch

![Una pelota bajando por la superficie de pérdida](ilustracion:pelota)
*(Ilustración generada con gpt-image-2.)*

La pelota baja por la pendiente. El gradiente apunta hacia donde más sube la
loss (pérdida). Gradient descent (descenso por gradiente) da un paso en la
dirección contraria.

En la unidad 6 y en la red que entrenamos a mano en la clase 1, cada paso usaba
todos los ejemplos de train (entrenamiento). Si $\ell_k$ es la loss del ejemplo
$k$, la loss promedio es $L(\theta)=\frac{1}{n}\sum_{k=1}^n\ell_k$. El paso es
$\theta\leftarrow\theta-\eta\,\nabla_\theta L(\theta)$, donde $\theta$ reúne los
pesos y sesgos y $\eta$ es el learning rate (tasa de aprendizaje).

Aquí barajamos los ejemplos al inicio de cada epoch y los dividimos en batches
(lotes). Para un batch $\mathcal B$, promediamos su loss,
$L_{\mathcal B}(\theta)=\frac{1}{\lvert\mathcal B\rvert}
\sum_{k\in\mathcal B}\ell_k$. El paso queda
$\theta\leftarrow\theta-\eta\,\nabla_\theta L_{\mathcal B}(\theta)$.
Llamamos $B$ al tamaño de batch elegido.

- Con $B=n$, cada paso usa todo el subconjunto de train. Es full-batch gradient descent (descenso con el lote completo).
- Con $B=1$, cada paso usa un ejemplo. Es stochastic gradient descent (descenso estocástico por gradiente, o SGD en sentido estricto).
- Con $1<B<n$, cada paso usa un mini-batch (lote de varios ejemplos).

PyTorch usa el mismo optimizer (optimizador), `SGD`, en los tres casos.
Una epoch (pasada completa por train) tiene
$\lceil n/B\rceil$ actualizaciones de $\theta$. Un batch chico da más pasos por
epoch y su gradiente suele variar más de un paso a otro. Un batch grande usa
más ejemplos en cada paso y estima con mayor precisión el gradiente completo.

**El experimento.** Todas las corridas usan los mismos 4096 ejemplos de train:
un subconjunto fijo de MNIST con casi la misma cantidad de cada dígito, para
que el experimento quepa en clase. La red es la de siempre, 784→128→10 con ReLU
(unidad lineal rectificada), con los mismos pesos iniciales y la misma secuencia
de barajado. El optimizer es SGD sin momentum (momento) con $\eta=0.03$.
Medimos sobre todo el conjunto de validation (validación), los 10 000 ejemplos.

- Full-batch, $B=4096$: 80 epochs, es decir, 80 pasos.
- $B=1$: una sola epoch, que ya son 4096 pasos.
- $B\in\{8, 32, 128, 1024\}$: cinco epochs cada uno.

En modo `RAPIDO` (sin GPU) todo esto se recorta a unos pocos pasos: sirve para
comprobar que el código corre, no para comparar.

La primera tabla muestra los tamaños de batch y el presupuesto previsto de
cada corrida. El learning rate se mantiene fijo para estudiar el efecto de
cambiar el batch. El orden de las curvas puede cambiar con otro learning rate.
En la sección 8 veremos por qué conviene ajustar ambos juntos.

### celda: s07-apuesta

**Apuesta.** Escribe tus dos respuestas antes de ejecutar.

1. Tras una epoch, ¿qué corrida esperas que tenga menor loss de validation, la de un ejemplo por batch o la de full-batch?
2. Con el mismo número de pasos al inicio del entrenamiento, ¿cuál esperas que tenga menor loss?

Abre la respuesta plegada después de mirar la gráfica y la tabla.

### celda: s07-ejes

La tabla de arriba muestra cuántos pasos caben en una epoch. Todas las
corridas ven los mismos ejemplos en una pasada. Las de batch chico
actualizan los parámetros más veces. A igual número de pasos, las de batch
grande procesan más ejemplos.

La figura pone las mismas corridas en cuatro paneles. El eje horizontal
cuenta epochs, actualizaciones, ejemplos procesados o segundos de
entrenamiento. El conteo de ejemplos incluye cada visita durante el
entrenamiento y aproxima el trabajo de calcular los gradientes. Una
fracción de epoch indica qué parte de la pasada se ha completado.

El eje vertical muestra la loss de validation y tiene la misma escala en los
cuatro paneles. En la paleta viridis, el batch más chico es oscuro y los más
grandes son claros. La línea negra discontinua es full-batch. La línea
horizontal gris del primer panel marca $\log 10\approx 2.30$, la loss de
asignar la misma probabilidad a cada dígito. El eje vertical se corta en 3:
con este learning rate, batch 1 puede dar saltos bruscos y algunos picos
pueden salirse por arriba.

El eje horizontal es logarítmico para abarcar presupuestos muy distintos. La
evaluación inicial se omite porque sus contadores están en cero y el 0 no cabe
en una escala logarítmica. Cada corrida se evalúa al menos cada 8 pasos; las
que tienen pocas evaluaciones llevan un círculo en cada una, y las que tienen
cientos se dibujan solo como línea. La línea vertical gris marca el
presupuesto máximo al que llegaron **todas** las corridas, y el tramo
sombreado es lo que queda a su izquierda. El código imprime ese límite para
cada eje. Fuera del tramo gris, una curva ya no tiene contra quién
compararse. Dentro de él, no todas las corridas tienen puntos medidos en
todas partes: full-batch, por ejemplo, mide por primera vez al terminar su
primera epoch. Por eso cada panel marca con una estrella ★ la última
medición de cada corrida dentro del presupuesto común. **Compara las
estrellas**: en epochs y en ejemplos vistos caen todas al final de la
primera epoch; en pasos, alguna puede caer un poco antes del límite porque
esa corrida evalúa cada 8 pasos.

### celda: s07-justa

Elige el eje según el recurso que quieras igualar.

- **Epochs o ejemplos vistos.** Con los mismos ejemplos procesados, un batch chico puede bajar más la loss porque actualiza los parámetros más veces.
- **Pasos.** Un batch grande puede bajar más la loss con las mismas actualizaciones, porque cada gradiente promedia más ejemplos. Cada paso requiere más cómputo.
- **Segundos.** Una GPU procesa varios ejemplos en paralelo. Un batch de un solo ejemplo puede aprovechar poco ese paralelismo y pagar muchas veces el costo de lanzar cada paso desde Python. Full-batch puede dar muy pocos pasos en el mismo tiempo. Un tamaño intermedio puede rendir mejor. El orden puede cambiar en CPU o con otra GPU. El reloj de la gráfica mide el entrenamiento y deja fuera el tiempo dedicado a evaluar las métricas.

La siguiente tabla muestra los presupuestos consumidos y las métricas de
validation. Usa «loss val tras 1 epoch» para comparar a igual cantidad de
datos procesados: todas vieron cada ejemplo exactamente una vez. Si una
corrida no completó esa epoch (pasa en modo `RAPIDO`), la columna dice
«sin completar». Las columnas de loss y accuracy
(proporción de aciertos) «al final» describen el punto donde terminó cada
corrida, con sus propios presupuestos: no se comparan entre filas. Decir
«full-batch terminó mejor que batch 1» sin decir que hizo 80 epochs contra
una es una comparación tramposa. Acompaña cualquier comparación con el
presupuesto al que corresponde.

### celda: s07-apuesta-respuesta

**Tras una epoch.** Se espera que el batch de un ejemplo vaya por delante de
full-batch. Con la misma pasada por train, actualiza los parámetros una vez
por ejemplo. Full-batch actualiza una vez por pasada. Comprueba la apuesta en
la tabla si ambas corridas completaron la primera epoch.

**A igual número de pasos.** Una expectativa razonable es que full-batch
avance más al principio. Cada paso usa el gradiente completo, mientras que
uno basado en un ejemplo puede fluctuar mucho con el learning rate elegido.
Míralo en el panel de pasos, dentro del tramo gris. Si el orden sale
distinto al esperado, ese resultado también responde la pregunta: dice cómo
se comportan estos batches con el learning rate de esta corrida.

### celda: s07-ruido-idea

¿Por qué varía el gradiente de un batch chico? Con $\theta$ fijo, el gradiente
$g_{\mathcal B}=\nabla_\theta L_{\mathcal B}(\theta)$ promedia los gradientes
de los ejemplos del batch. Si tomamos batches al azar, ese promedio es un
estimador insesgado del gradiente completo
$g_{\text{completo}}=\nabla_\theta L(\theta)$.
Al cambiar de batch, el estimador fluctúa. Medimos ese ruido como
$\mathbb E\,\lVert g_{\mathcal B}-g_{\text{completo}}\rVert^2$, la distancia
al cuadrado al gradiente completo, promediada sobre el muestreo de batches.

En la unidad 9 vimos la misma idea con un promedio muestral. Si las
observaciones son independientes y tienen varianza $\sigma^2$, la varianza
del promedio es $\sigma^2/B$. Su error estándar baja como $1/\sqrt B$. Por
eso esperamos que el ruido, que aquí es una **distancia al cuadrado**,
baje aproximadamente como $1/B$. En cada batch muestreamos sin reemplazo
entre los $n$ ejemplos. Eso multiplica el ruido esperado por
$(n-B)/(n-1)$. Con $B=n$, el batch contiene todo el conjunto y el ruido
es cero.

El código mantiene fijos los pesos. Calcula el gradiente completo con
backpropagation (retropropagación) y lo compara con el de 32 batches al azar por cada
$B\in\{1, 8, 32, 128, 1024\}$ (8 en modo `RAPIDO`). Repite la medición con la
red recién inicializada y con la red de `s07-b128` al final de sus cinco
epochs. La tabla reporta el ruido
promedio y su cociente con $\lVert g_{\text{completo}}\rVert^2$, que llamamos
la señal. Un cociente mayor que uno indica que, en promedio, la distancia
al cuadrado al gradiente completo supera la magnitud al cuadrado de ese
gradiente.

Ambos ejes de la gráfica están en escala logarítmica. Una ley $1/B$ se ve como
una recta de pendiente $-1$. Las líneas grises discontinuas son referencias
$1/B$ ajustadas a la escala de los datos de cada red. Las punteadas incorporan
la corrección por muestreo sin reemplazo. Las barras muestran el error
estándar de la media de las distancias medidas para cada tamaño.

### celda: s07-que-viste

**Qué viste**

- **El avance depende del presupuesto.** Compara las estrellas ★ de cada panel: busca si los batches chicos avanzan más por ejemplo o por epoch, si los grandes avanzan más por paso y si un tamaño intermedio rinde mejor por segundo en GPU. Algunas diferencias pueden ser pequeñas, y el orden por segundos depende de la máquina.
- **El ruido baja al promediar más ejemplos.** Busca una caída cercana a $1/B$ y fíjate si se acentúa al aumentar la fracción del conjunto que entra en cada batch.
- **La señal también puede cambiar al entrenar.** Compara las dos normas al cuadrado que imprime el código. Si el gradiente completo se hace pequeño, el cociente ruido/señal puede subir, incluso cuando el ruido absoluto baja. Cerca de un mínimo, el ruido de los batches chicos puede dominar el gradiente que queremos estimar. Puede que aquí no se vea. En la sección 14 volveremos a medir gradientes, esta vez por capa.

El tamaño del batch afecta la memoria, los pasos que das por epoch, el
ruido de cada actualización y el tiempo de cómputo. En el resto del notebook
usaremos mini-batches por omisión. El siguiente paso es ver cómo el
learning rate cambia el efecto de cada actualización.
