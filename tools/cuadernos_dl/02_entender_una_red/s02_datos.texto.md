### celda: s02-intro

## 02 · Los datos

MNIST reúne 70 000 imágenes de dígitos escritos a mano. Cada imagen tiene
$28 \times 28$ píxeles en escala de grises, con intensidades de 0 a 255.
Su etiqueta es un entero del 0 al 9. Torchvision descarga los archivos si
hace falta y reutiliza la copia local en las siguientes ejecuciones.

MNIST trae 60 000 imágenes de train y 10 000 de test. Creamos validation
con las últimas 10 000 imágenes del train original, siguiendo la
partición del libro de Nielsen. Quedan 50 000 para train, 10 000 para
validation y 10 000 para test. Usamos este split train/validation/test
ya establecido tal cual: por la rapidez de la clase no validamos si es el
mejor. Es una regla reproducible, no una conclusión. `ORIGEN` guarda los índices de cada
conjunto dentro de su archivo.

Recuerda el reparto de tareas de la unidad 9. Train ajusta los pesos y
sesgos. Validation sirve para elegir el modelo, la epoch o los
hiperparámetros, como el learning rate. Test se reserva para reportar
el desempeño del modelo elegido.

### celda: s02-pruebas-explica

Los `assert` son comprobaciones que detienen la celda si fallan. Aquí
verifican los tres tamaños y que train y validation tengan índices
disjuntos dentro del archivo que comparten.

Dos imágenes de índices distintos pueden tener los mismos píxeles.
Por eso también se calcula un *hash* (huella digital) de cada imagen.
La celda cuenta repeticiones dentro de cada conjunto y huellas comunes
entre cada par. Si aparecen coincidencias, se reportan y se conserva la
partición original para los ejercicios.

En la tabla y en la gráfica, compara las tres barras de un mismo dígito.
Si tienen alturas parecidas, ese dígito ocupa una proporción similar en
los tres conjuntos. La línea punteada marca el 10 % que tendría cada
clase en un reparto parejo. Adivinar uniformemente entre las diez clases
da un 10 % de *accuracy* (proporción de aciertos) en promedio. Con clases
casi parejas, predecir siempre el mismo dígito también queda cerca de
esa referencia.

### celda: s02-muestra-explica

Mira las dos primeras imágenes de train de cada dígito. Compara sus
trazos aunque tengan la misma etiqueta. Cada imagen es una cuadrícula de
$28 \times 28$. El *multilayer perceptron* (perceptrón multicapa, MLP)
recibe sus $784$ intensidades en una fila. La posición de cada píxel en
la fila se conserva. En la sección 17, la red convolucional usa la
cuadrícula para procesar píxeles vecinos juntos.

### celda: s02-gpu-explica

`DATOS[escala][conjunto]` guarda el par `(X, y)` en tres escalas.

- `"crudo"` conserva las intensidades de 0 a 255.
- `"01"` divide cada intensidad entre 255.
- `"estandar"` parte de `"01"`, resta `MEDIA` y divide entre `DESV`.

Se calcula una sola media y una sola desviación estándar con todos los
píxeles de train en `"01"`. Esas dos cifras se aplican también a validation
y test, como en la unidad 9. En la sección 5 compararás las tres escalas.

`X` tiene forma `[n, 784]`, con una imagen por **fila**. `y` tiene forma
`[n]` y guarda un entero `int64` por imagen. Los conjuntos caben en la
memoria de una T4. Con `.to(DEVICE)` preparamos los tensores una sola vez
en el dispositivo elegido. Cuando usamos la GPU, los batches se toman
por índice allí mismo y se evita copiar uno desde la CPU en cada paso.

`RAPIDO` toma una muestra con cantidades parecidas de cada dígito en los
tres conjuntos. La celda imprime los tamaños reducidos. `IMAGENES_TEST`
conserva las imágenes en la CPU como cuadrículas en $[0,1]$ para las
galerías de errores de más adelante.

### celda: s02-subconjunto-explica

Algunas corridas usan un subconjunto de train para ahorrar tiempo.
`subconjunto(n)` devuelve índices estratificados, con cerca de $n/10$
ejemplos por dígito. Para los mismos datos, el mismo tamaño y la misma
semilla, devuelve los mismos índices. Fíjate en el conteo por dígito que
imprime la celda.

El subconjunto de una corrida afecta solo a train. Validation y test se
evalúan completos en el modo normal. En `RAPIDO` se evalúa todo lo que
quedó en cada conjunto tras el recorte.

### celda: s02-que-viste

**Qué viste.** Los `assert` comprobaron los tamaños y la separación por
índice. Las huellas de los píxeles permitieron contar imágenes idénticas.
Las barras muestran qué tan parecida es la mezcla de dígitos en los
tres conjuntos. Los tensores ya están en `DEVICE`. Puedes elegir
cualquiera de las tres escalas al entrenar.
