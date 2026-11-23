### celda: s03-intro

## 03 · La caja de herramientas

Vamos a seguir un dígito desde los píxeles hasta la predicción. Luego
haremos un paso de entrenamiento como en el notebook 01. Las funciones
de esta sección quedan a la vista para que puedas seguir qué se calcula
en cada experimento.

`construir_red(capas, ...)` encadena las capas con `nn.Sequential`.
La lista empieza con $784$ entradas y acaba con $10$ salidas, una por
dígito. Los números intermedios indican cuántas neuronas hay en cada capa
oculta. Con `[784, 10]` obtienes la versión multiclase de la regresión
logística de la unidad 9.

Cada capa oculta empieza con `nn.Linear`, que multiplica por los pesos
y suma los sesgos. Luego viene la activación $g^{(l)}$, por ejemplo
*ReLU* (unidad lineal rectificada), que aplica $\max(0,z)$ a cada
componente. Si se activan las opciones de la sección 15, el orden es
`nn.Linear`, batch normalization (ajustar la escala de las señales con
estadísticas del lote), activación y dropout (poner a cero al azar
algunas activaciones durante el entrenamiento). La última capa es
`nn.Linear` y entrega directamente los *logits* (puntajes antes de
convertirlos en probabilidades).

Con `init="defecto"` se usan los pesos y sesgos iniciales de PyTorch.
`"he"` parte de pesos con varianza $2/d_{l-1}$, como en el notebook 01.
Aquí $d_{l-1}$ es el ancho de la capa anterior. `"ortogonal"` usa una
inicialización ortogonal. En estas dos últimas opciones los sesgos
arrancan en cero.

### celda: s03-punta-a-punta-explica

Sigue la primera fila de `xb` en las formas que imprime la celda. La red
procesa varios dígitos juntos. En `[B, 784]`, $B$ es el tamaño del batch
y cada fila contiene los píxeles de un dígito.

En el notebook 01 cada observación ocupaba una **columna**, y la primera
capa calculaba $\mathbf z^{(1)} = \mathbf W^{(1)}\mathbf x + \mathbf b^{(1)}$.
En PyTorch cada observación ocupa una **fila**. Se conservan los ejes de
$\mathbf W^{(1)}$, con filas para las neuronas de destino y columnas para las
entradas de origen. En esta red, eso da `[128, 784]`. La transpuesta
permite escribir `xb @ W.T + b`, que produce `[B, 128]`. El `assert`
comprueba que da lo mismo que llamar a la primera capa de PyTorch.

1. La red devuelve `[B, 10]`. Cada fila contiene un logit por dígito.
   La posición de cada logit corresponde a una clase del 0 al 9.
2. La etiqueta $y_k$ es un entero que indica la posición correcta para
   la observación $k$. `nn.CrossEntropyLoss` recibe los logits y esas
   etiquetas. La *cross-entropy* (entropía cruzada) equivale a aplicar
   softmax y promediar $-\log \widehat p_{k,y_k}$, donde
   $\widehat p_{k,y_k}$ es la probabilidad asignada a la clase correcta.
   Es la *negative log-likelihood* (log-verosimilitud negativa)
   promedio de la regresión logística multiclase.
3. `argmax(dim=1)` busca la posición del logit mayor en cada fila.
   Esa posición es el dígito predicho $\widehat y_k$. Compara el primer
   valor de «predicción» con el primero de «real».

Si la red asignara la misma probabilidad a los diez dígitos, la loss
sería $\log 10$. La loss inicial puede quedar cerca de esa referencia.
En la sección 18 verás cómo calcula PyTorch la cross-entropy a partir
de los logits.

### celda: s03-loop-explica

En `paso()` del notebook 01 calculaste el gradiente y actualizaste los
parámetros. Aquí cada paso usa un *mini-batch* (lote pequeño)
$\mathcal B$ de train para calcular un gradiente y hacer **una**
actualización.

1. `optimizer.zero_grad()` borra los gradientes anteriores. PyTorch
   acumula gradientes cada vez que llamas a `backward()`.
2. `red(X[idx])` hace el *forward pass* (pasada hacia adelante). Pasa
   de las imágenes del batch `[B, 784]` a los logits `[B, 10]`.
3. `perdida_fn(logits, y[idx])` calcula $L_{\mathcal B}$, la
   cross-entropy promedio sobre ese batch.
4. `perdida.backward()` hace la backpropagation. Deja en `p.grad` el
   gradiente de cada parámetro $p$. En el notebook 01 lo calculaste
   a mano y lo comprobaste con diferencias finitas.
5. `optimizer.step()` actualiza los parámetros. Con *SGD* (descenso de
   gradiente estocástico), la regla de esta celda es
   $p \leftarrow p - \eta\,\nabla_p L_{\mathcal B}$, con learning rate
   $\eta$. Al final la celda calcula el mismo paso a mano y compara
   ambos resultados.

En el notebook 01 el gradiente usaba todos los datos en cada paso.
Eso se llama *full-batch gradient descent* (descenso de gradiente con
el lote completo). Al trabajar con mini-batches, una epoch completa
cubre los $n$ ejemplos de train en $\lceil n/B\rceil$ pasos, contando
un último lote más chico si sobra algún ejemplo.

En esta demostración los índices se sortean con reemplazo. Un ejemplo
puede salir más de una vez, incluso en el mismo lote. En `entrenar`,
cada epoch empieza con una permutación de train y recorre los lotes
en ese orden.

### celda: s03-config-explica

`Config` describe una corrida. `id` y `seccion` son los campos
obligatorios. Los demás tienen valores iniciales que puedes cambiar.

- **Red.** Anchos, activación e inicialización. Puedes activar batch
  normalization o dropout, o pasar una función que construya otro modelo.
- **Actualizaciones.** Optimizer, learning rate $\eta$, tamaño del
  batch y presupuesto en epochs o pasos. El *weight decay*
  (decaimiento de pesos) favorece pesos de menor magnitud durante el ajuste.
- **Datos y evaluación.** Elige la escala, un subconjunto de train
  o una fracción de etiquetas que se cambiarán en train. También
  puedes fijar la frecuencia de evaluación y la paciencia para
  early stopping, es decir, cuántas evaluaciones seguidas se esperan
  sin mejora en validation.
- **Azar.** `semilla_init` fija la inicialización y `semilla_orden`
  fija el orden de los batches. Puedes empezar dos corridas con los
  mismos pesos y comparar distintos órdenes.

`config_profunda` prepara la red con varias capas ocultas de las
secciones 13 a 15. Usa SGD, inicialización ortogonal y sesgos en cero.
Puedes sobrescribir los campos al llamarla.

`Corrida` guarda la configuración usada, una fila por evaluación en el
historial, el conteo de parámetros y si se detectó divergencia. También
guarda dos *checkpoints* (copias del estado del modelo), uno para la
mejor evaluación por loss de validation y otro para la última.
`CORRIDAS` guarda cada resultado por su `id`. Si repites una celda con
el mismo ID, el resultado nuevo reemplaza al anterior.

### celda: s03-evaluar-explica

`medir(modelo, X, y)` recorre por bloques todos los ejemplos que recibe.
Devuelve la loss promedio y la accuracy. `evaluar(modelo, escala,
conjunto)` le pasa el conjunto completo que está en `DATOS`.

Para medir, el código apaga el cálculo de gradientes y pone la red en
modo `eval()`. Dropout queda desactivado y batch normalization usa
sus estadísticas acumuladas durante el entrenamiento. Al terminar,
`medir` devuelve la red al modo en el que estaba. En la sección 15
verás por qué importa distinguir `train()` de `eval()`.

`crear_optimizer` arma la regla que actualiza los parámetros. Aplica
weight decay a las matrices y filtros y deja
los sesgos y los parámetros de batch normalization fuera de esa
penalización. Con `adam_l2`, la penalización L2 se suma al gradiente,
como el término con $\mu$ del lagrangeano del notebook 01. Con `adamw`,
el decaimiento se aplica por separado. La sección 9 compara ambas reglas.
`norma_pesos` mide el tamaño conjunto de esas matrices y filtros.

`cargar(corrida, "mejor")` reconstruye la red a partir de la
configuración, recupera el checkpoint elegido con validation y la deja
lista para evaluar en `DEVICE`. También puedes pedir `"ultima"`.

### celda: s03-entrenar-explica

`entrenar(cfg)` reúne las piezas en este orden.

1. Prepara train en la escala elegida y toma el subconjunto si se pidió.
   Si `ruido_etiquetas` es positivo, cambia una fracción de sus etiquetas
   a otros dígitos con una semilla fija. Luego construye la red y su
   optimizer.
2. Mide en la epoch 0, con la red recién inicializada. A partir de ahí,
   baraja los índices al comenzar cada epoch y actualiza por batch.
   Con batch normalization, un último lote de un solo ejemplo se une al
   anterior, porque no se puede normalizar un solo valor.
3. Mide de nuevo al terminar cada epoch o con la frecuencia fijada
   en `eval_cada_pasos`. Usa todos los ejemplos del train de la
   corrida y todo lo disponible en validation y test. Registra loss,
   accuracy, pasos, ejemplos vistos, segundos y norma de los pesos.
4. Guarda en CPU el estado con la menor loss de validation y el último
   estado. Eso incluye las estadísticas acumuladas de batch normalization
   cuando se usa. Si se configuró `paciencia`, el entrenamiento se
   detiene cuando pasan esas evaluaciones seguidas sin mejora.

La caja comprueba por grupos las losses de los pasos para evitar una
espera a la GPU en cada uno. Si encuentra un infinito o un `NaN`
(resultado no numérico), registra el primer paso con loss no finita,
marca `divergio` y detiene la corrida. En la sección 8 verás qué curvas
aparecen cuando esto sucede.

El reloj cuenta el tiempo de entrenamiento. En GPU,
`torch.cuda.synchronize()` espera a que termine el trabajo antes de
leer el reloj. El tiempo dedicado a evaluar queda fuera de ese conteo.

Con `medir_por_paso` también se guardan, para cada capa lineal o
convolucional y cada paso, la norma del gradiente y el cambio relativo
de sus pesos, $\lVert \mathbf W_{t+1}-\mathbf W_t\rVert /
\lVert \mathbf W_t\rVert$. Lo usaremos en las secciones 13 y 14.

Al cerrar, la función registra la `Corrida`, imprime un resumen y
devuelve el historial y los checkpoints como parte de ese resultado.
El modelo y el optimizer de la corrida se descartan al salir de la
función. Con `RAPIDO` se recorta el presupuesto de epochs y pasos.

### celda: s03-graficas-explica

- `curvas` dibuja loss o accuracy en el eje vertical. Puedes poner en
  el horizontal epochs, pasos, ejemplos vistos o segundos. El color
  identifica el conjunto y el estilo de línea identifica la corrida.
  Si graficas varias corridas de un solo conjunto, el color pasa a
  identificar la corrida. La función omite los valores no finitos.
- `rejilla` dibuja un panel por corrida con el eje horizontal compartido.
  Por defecto, también comparte la escala vertical.
- `tabla_maestra` reúne una fila por corrida. Toma loss y accuracy en
  la mejor evaluación según la loss de validation. La brecha es
  accuracy de train menos accuracy de validation en esa evaluación.
  La fila también muestra el tiempo total de entrenamiento y si hubo
  divergencia. Si una misma corrida quedó guardada con dos nombres,
  cuenta una sola vez; `experimentos_unicos()` da cuántas corridas
  distintas hay. En la sección 19 verás la tabla completa.
- `dibujar_red` muestra una columna de nodos por capa, desde los
  píxeles hasta los logits. La altura de cada columna crece con el
  logaritmo de su ancho, así que un embudo se ve como embudo. Si una
  capa es ancha, «⋮» marca los nodos omitidos. Su ancho real aparece
  debajo.

### celda: s03-demo-explica

`s03-demo` es una corrida corta con un subconjunto de train. Lee la
línea de resumen y sigue la loss desde la epoch 0 en el panel izquierdo.
Busca si la línea azul baja al entrenar. En el panel derecho, ubica
la capa oculta entre la entrada de píxeles y la salida de logits.
La tabla debajo reúne las métricas de la mejor evaluación por loss
de validation.

**Mirar test en cada epoch está mal.** Test se usa una sola vez, al
final. Aquí lo graficamos solo para aprender a leer las tres curvas.
Todas las decisiones se toman con validation.

### celda: s03-que-viste

**Qué viste.** Seguiste un dígito desde su fila de píxeles hasta sus
logits, su contribución a la loss y la clase elegida por `argmax`.
Las cinco líneas del paso de entrenamiento hacen en PyTorch el
cálculo que escribiste a mano en el notebook 01.

En la demo, compara la loss de train antes y después de actualizar los
pesos. Si baja, la red empieza a ajustarse a esos ejemplos. Las curvas
de validation y test muestran cómo evolucionó la loss en los otros
conjuntos. A partir de aquí, usa `Config` para cambiar lo que quieres
estudiar y compara las corridas.
