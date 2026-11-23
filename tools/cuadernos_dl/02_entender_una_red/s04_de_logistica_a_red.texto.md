### celda: s04-intro

## 4 · De la regresión logística a la red

En «Pasar a más de dos clases» de la unidad 9 viste la regresión softmax.
Cada clase $y$ tiene un intercepto $\beta_{0,y}$ y un vector de pesos $\beta_y$.
Si usamos los píxeles como entrada, el puntaje para la imagen $i$ es
$z_{i,y}=\beta_{0,y}+\beta_y^{\mathsf T}x_i$.
Softmax (normalización exponencial) convierte los puntajes en probabilidades
$p_{i,y}$. La pérdida de esa imagen es $-\ln p_{i,y_i}$, donde $y_i$ es su clase
correcta. La figura de la unidad 9 ya mostraba este modelo como una red de
una sola capa. Aquí la construimos.

En la notación de la unidad 10, $k$ identifica la imagen e $i$ el dígito de salida.
La red $[784,10]$ lee los $784$ píxeles de $\mathbf x_k$ y calcula
$\mathbf z_k^{(1)}=\mathbf W^{(1)}\mathbf x_k+\mathbf b^{(1)}$.
En $\mathbf W^{(1)}$, de $10\times784$, cada fila $i$ corresponde al dígito
destino y cada columna $j$ al píxel de origen. La fila $i$ es
$\beta_y^{\mathsf T}$ para $y=i$. El sesgo $b_i^{(1)}$ de
$\mathbf b^{(1)}$, de $10\times1$, es el intercepto $\beta_{0,y}$ de esa clase.

La salida usa la identidad. Sus diez valores son los **logits** (puntajes
sin normalizar). El dígito predicho $\widehat y_k$ es el de mayor logit.
`CrossEntropyLoss` recibe los logits y calcula la cross-entropy (entropía
cruzada). Para cada imagen, equivale a aplicar softmax y tomar el negativo del
logaritmo de la probabilidad de la clase correcta. En la sección 18 veremos
softmax a fondo.

En las fórmulas, una imagen es una columna. En PyTorch, cada imagen ocupa
una fila de la entrada de forma `[B, 784]`, donde `B` es el número de
imágenes. Por eso la operación en código es `x @ W.T + b`.

La celda siguiente construye y dibuja la red sin entrenar. Imprime las formas
de los pesos y los sesgos, y cuenta $10\cdot784+10=7\,850$ parámetros.
También pasa tres imágenes por la red para mostrar el cambio de forma de
`[3, 784]` a `[3, 10]`.

### celda: s04-logistica-entrena-texto

Entrena la logística con `Config` y `entrenar`, de la sección 3. Cada
actualización usa un mini-batch (lote pequeño) de train (entrenamiento).
Adam es el optimizer (optimizador) que ajusta el paso de cada parámetro.
En la sección 9 veremos cómo lo hace.

En la unidad 9, el optimizer buscaba converger y el objetivo podía incluir
una penalización con $\mu$ en el lagrangeano. Aquí ajustamos el mismo modelo
con la misma cross-entropy, sin penalización ($\mu=0$). Hacemos actualizaciones
por mini-batches durante un número fijo de epochs (pasadas por train).

Verás dos gráficas, una de loss (pérdida) y otra de accuracy (proporción de
aciertos). Cada una muestra train, validation (validación) y test (prueba).
La tabla reúne las mediciones por epoch. La fila de la epoch 0 corresponde
a la red antes de entrenar.

### celda: s04-logistica-mira

Lee la epoch en el eje horizontal. Train va en azul, validation en naranja
y test en verde. La epoch 0 parte de pesos aleatorios. Como referencia, si
das la misma probabilidad a cada dígito, la loss es $\ln(10)\approx 2.30$.
Si eliges un dígito al azar con esa misma distribución, la accuracy
esperada es $10\,\%$.

Busca una caída rápida de la loss en la primera epoch y una curva más plana
después. Si train y validation quedan cerca y ambas se estancan, el patrón
sugiere underfitting (subajuste). Los logits dependen de una combinación
lineal de píxeles más un sesgo. Esa capacidad limitada puede dejar un error
por sesgo que apenas cambie con más epochs.

La «mejor epoch» es la de menor loss en validation. Mirar test en cada
epoch está mal en un proyecto real. Test se usa una sola vez, al final,
para reportar. Aquí lo mostramos en cada epoch solo para aprender a leer
las tres curvas. Las decisiones de selección se toman con validation.

### celda: s04-pesos-texto

La siguiente figura toma los pesos de la mejor epoch según validation.
Cada fila $i$ de $\mathbf W^{(1)}$ tiene un peso $w_{ij}^{(1)}$ por píxel.
Al reorganizar la fila en una cuadrícula de $28\times28$, ves la plantilla
de pesos del dígito $i$. Su logit es
$z_i^{(1)}=\sum_j w_{ij}^{(1)}x_j+b_i^{(1)}$.

Hay un panel por dígito. El eje horizontal es la columna del píxel y el
vertical, su renglón. Al aplanar la imagen, el píxel $j$ viene del renglón
$\lfloor j/28\rfloor$ y la columna $j\bmod 28$. La escala de color es la
misma en todos los paneles y es simétrica alrededor de cero. Si aumentas un
píxel y mantienes los demás fijos, un peso rojo sube el logit de ese dígito
y uno azul lo baja. El blanco corresponde a un peso cero.

Busca un anillo rojo con centro azul en el cero o un trazo vertical en el
uno. Son formas que podrían aparecer. Los bordes pueden verse irregulares.
Allí muchos píxeles cambian poco entre imágenes, así que sus pesos pueden
conservar parte de la inicialización aleatoria. Como la entrada está
estandarizada, un píxel apagado toma un valor negativo. Lee los colores como
contrastes de pesos entre posiciones.

### celda: s04-neurona

Agreguemos una **capa oculta**, como en la red que construiste a mano en la
clase 1. La red $[784,128,10]$ calcula $128$ activaciones ocultas y las
combina para producir los diez logits de salida.

- **Neurona.** La neurona $i$ de la capa $l$ calcula una preactivación,
  $z_i^{(l)}=\sum_j w_{ij}^{(l)}a_j^{(l-1)}+b_i^{(l)}$.
  Luego aplica una función de activación y devuelve
  $a_i^{(l)}=g^{(l)}(z_i^{(l)})$. Si eliges la sigmoide $\sigma$, recuperas
  la forma de la regresión logística binaria de la unidad 9.
- **Capa.** Las $d_l$ neuronas leen la misma entrada en paralelo, cada una
  con sus propios pesos. Juntas calculan
  $\mathbf a^{(l)}=g^{(l)}(\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)})$,
  con $\mathbf W^{(l)}$ de $d_l\times d_{l-1}$. Una capa oculta está entre
  la entrada y la salida. Sus activaciones son valores intermedios que la
  red aprende a calcular al ajustar sus salidas a las etiquetas.
- **ReLU** (unidad lineal rectificada). La capa oculta usa
  $g^{(1)}(z)=\max(0,z)$. Deja pasar los valores positivos y convierte
  los negativos en cero. Su derivada vale cero para $z<0$ y uno para $z>0$.
  En $z=0$ hay un quiebre. Para backpropagation (retropropagación) usamos
  $g^{(1)\prime}(0)=0$ por convención, como en la clase 1.
  La siguiente celda dibuja ReLU junto a la identidad y muestra la derivada
  de ReLU.

Con la identidad en las dos capas, la composición se reduce a una sola
transformación afín. Sus parámetros son
$\mathbf W'=\mathbf W^{(2)}\mathbf W^{(1)}$ y
$\mathbf b'=\mathbf W^{(2)}\mathbf b^{(1)}+\mathbf b^{(2)}$.
Con esos logits y la cross-entropy recuperamos la familia de modelos de la
logística. El código compara los logits de las dos formas de calcularlos
en las mismas imágenes. `True` indica que coinciden dentro de la tolerancia
numérica. Con ReLU, la contribución de una neurona depende de si su
preactivación es positiva. Eso permite construir fronteras de clasificación
más flexibles.

### celda: s04-apuesta

**Apuesta.** La logística suele acertar la gran mayoría de los dígitos.
¿Qué pasará con la accuracy de validation al agregar $128$ neuronas ReLU
en una capa oculta? Las dos redes usan el mismo optimizer, el mismo
learning rate (tasa de aprendizaje) $\eta$, el mismo tamaño de batch
(lote) y el mismo número de epochs.

- (a) Las dos redes empatan.
- (b) La red con capa oculta gana menos de un punto porcentual.
- (c) Gana unos pocos puntos porcentuales.
- (d) Se equivoca menos de la mitad de las veces que la logística.

Escribe tu apuesta antes de ejecutar. Puedes elegir más de una opción.
La capa oculta permite combinar los píxeles de manera no lineal. También
multiplica el número de parámetros.

La tabla que sigue cuenta $d_l d_{l-1}+d_l$ parámetros por capa y los
dibujos muestran ambas redes lado a lado. La logística tiene $7\,850$
parámetros. La red con ReLU tiene $784\cdot128+128=100\,480$ en la capa
oculta y $128\cdot10+10=1\,290$ en la salida. Suma $101\,770$, unas trece
veces el total de la logística.

Luego se entrena `s04-oculta`, la línea base del notebook. La sección 6
retoma sus curvas y la sección 16 incluye esta corrida entre las candidatas.
Las gráficas de abajo ponen una red por columna, con los mismos ejes en
cada renglón para comparar epoch por epoch. La línea punteada gris marca la
mejor epoch de cada red según validation. En accuracy, el eje empieza cerca
de los valores de la epoch 1 en adelante: la epoch 0, cerca del $10\,\%$,
queda debajo y no aparece. La tabla muestra las métricas en esa mejor epoch.

### celda: s04-apuesta-respuesta

Mira el cambio en puntos porcentuales de accuracy que reportó la celda
anterior. Luego mira el cociente entre la proporción de errores de la
logística y la de la red con capa oculta, ambos en validation. La última
línea resuelve la opción (d) con un «sí» o un «no».

Cerca del $100\,\%$ de accuracy quedan pocos errores. Ganar unos pocos
puntos puede eliminar una fracción grande de esos errores. En MNIST, la
red con ReLU suele mostrar ese patrón. Las apuestas (c) y (d) pueden
cumplirse a la vez. Si el cociente pasa de 2, en esta ejecución la red se equivocó
menos de la mitad de las veces que la logística.

La logística compara puntajes afines y separa clases con fronteras lineales
en el espacio de píxeles. Las neuronas ocultas pueden aprender rasgos de la
imagen y la salida puede combinar esos rasgos para formar fronteras no
lineales. Esa flexibilidad puede reducir el sesgo. También aumenta el
margen para el overfitting (sobreajuste). Busca si la red con ReLU abre una
brecha mayor entre train y validation. Puede ser pequeña o apenas empezar
a verse.

### celda: s04-que-viste

**Qué viste**

- La regresión softmax de la unidad 9 es una red $[784,10]$ con salida
  identidad y cross-entropy. Sus filas de pesos se leen como plantillas de
  los dígitos.
- Cada neurona calcula una preactivación y aplica una activación. Una capa
  reúne neuronas en paralelo. Con la identidad, dos capas se pueden
  reemplazar por una sola transformación afín.
- Con la capa oculta ReLU, busca una loss de train más baja y menos errores
  en validation. Compara también la brecha entre las dos curvas. Una
  mejora en validation puede coexistir con una brecha mayor.

En la tabla maestra, cada fila es una corrida. Busca `s04-logistica` y
`s04-oculta`. Sus métricas corresponden a la mejor epoch de cada corrida
según validation. Las curvas de test se mostraron en cada epoch solo para
practicar su lectura. La elección de epoch se hizo con validation.

En la sección 5 cambiamos la escala de la entrada. En la sección 6 volvemos
a la línea base `s04-oculta` para leer a fondo las tres curvas.
