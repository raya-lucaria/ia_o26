### celda: s05-intro

## 05 · Normalizar la entrada

En MNIST, cada píxel viene como un entero entre $0$ (negro) y $255$ (blanco).
Vamos a comparar tres formas de representar esos valores.

- **Crudo.** Usamos el valor original $x$.
- **Entre $0$ y $1$.** Dividimos el valor entre $255$.
- **Estandarizado.** Centramos y ajustamos la dispersión con
  $x' = (x/255 - \text{MEDIA})/\text{DESV}$.

La sección 2 calculó una sola media y una sola desviación estándar con
todos los píxeles de train (entrenamiento) en la escala $[0,1]$.
Usamos esas mismas dos constantes para validation (validación) y test (prueba).
Si incluyéramos sus píxeles al calcularlas, habría *leakage* (fuga de información):
estaríamos espiando los datos con los que después medimos, y la evaluación
dejaría de ser honesta. Es la misma regla de la unidad 9: estandarizar solo con
entrenamiento.
En producción, esas constantes tienen que estar listas antes de recibir imágenes nuevas.

En la unidad 9, «El lagrangeano en acción», §5 «Estandarizar antes de penalizar»,
pusimos las variables en escalas comparables para que sus unidades no dieran
ventaja a unos coeficientes al penalizarlos. Aquí vamos a ver cómo la escala
cambia el gradiente y qué *learning rate* (tasa de aprendizaje) $\eta$ sirve.

Las tres corridas usan la misma red con una capa oculta con ReLU y el mismo
SGD (*stochastic gradient descent*, descenso estocástico de gradiente) sin
*momentum* (momento). Comparten el learning rate, el tamaño de *batch* (lote),
el presupuesto de *epochs* (pasadas por train), los pesos iniciales y el orden
de los batches. Solo cambia la escala.

**Mira la tabla.** Compara el mínimo, el máximo, la media y la desviación
de cada escala por conjunto. En la escala estandarizada, train tiene media
$0$ y desviación $1$ por construcción. En validation y test, ambas suelen
quedar cerca de esos valores al aplicar las constantes de train.

### celda: s05-histogramas-guia

Los tres paneles usan la misma muestra de imágenes de train. Las
transformaciones son afines. Multiplican y desplazan los valores del eje
horizontal, así que conservan la forma de la distribución y la información
de cada píxel.

Fíjate en la barra alta del fondo y en los valores más claros del trazo.
El eje vertical usa escala logarítmica para que se vean también los
valores poco frecuentes. En el panel estandarizado, el fondo queda por
debajo de cero y el trazo blanco queda por encima. Busca sus extremos
en la tabla.

La línea discontinua marca la media de la muestra. La estandarización fija
la media y la desviación del conjunto de píxeles de train. Cada posición
de la imagen puede tener su propia media.

### celda: s05-gradiente

Recuerda el cálculo de la primera capa de la clase 1. Para una imagen,
la preactivación de la neurona $i$ es
$z^{(1)}_i = \sum_j w^{(1)}_{ij} x_j + b^{(1)}_i$.
Al hacer *backpropagation* (retropropagación), el gradiente del peso es
$\frac{\partial \ell}{\partial w^{(1)}_{ij}} = \delta^{(1)}_i x_j$,
donde $\delta^{(1)}_i = \frac{\partial \ell}{\partial z^{(1)}_i}$.
En el código, cada imagen ocupa una fila de `x`. Por eso el producto es
`x @ W.T`.

Si mantienes fijo $\delta^{(1)}_i$ y multiplicas la entrada por $255$,
ese gradiente también se multiplica por $255$. Ahora imagina un paso de
SGD con una sola imagen. El cambio de los pesos es
$\Delta w^{(1)}_{ij} = -\eta\,\delta^{(1)}_i x_j$.
Al volver a evaluar la misma imagen, el cambio de los pesos aporta
$-\eta\,\delta^{(1)}_i\sum_j x_j^2$ a la preactivación.
Ese efecto crece por un factor de $255^2$ con $\eta$ y $\delta^{(1)}_i$ fijos.
En las corridas también cambian los $\delta$ y se promedian gradientes
de varias imágenes.

Con los mismos pesos iniciales, los píxeles crudos pueden dar
preactivaciones grandes desde el inicio. La segunda capa recibe las
activaciones de la primera. Por eso también pueden crecer los gradientes
de sus pesos, la magnitud de los *logits* (salidas antes de softmax) y la
*loss* (pérdida) inicial.

En la unidad 6, «Bajar la pendiente», §3 «Cuánto avanzar», la distancia
con signo al mínimo se multiplica por $1-2\alpha$ en $x$ y por
$1-8\alpha$ en $y$. La dirección más sensible limita el paso $\alpha$.
Aquí llamamos $\eta$ a ese paso. Cambiar la escala de la entrada puede
cambiar la curvatura de la loss respecto a los pesos y, con ello, el
tamaño de paso que funciona.

**Lee la tabla.** La celda usa el mismo batch y los mismos pesos iniciales
para las tres escalas. Para cada capa muestra la loss inicial, la norma
del gradiente de los pesos y el tamaño relativo de un paso de SGD,
$\eta\lVert\nabla_{\mathbf W^{(l)}} L_{\mathcal B}\rVert_F / \lVert\mathbf W^{(l)}\rVert_F$.
Este cociente mide cuánto movería el paso a la matriz de pesos en relación
con su norma. Las líneas al pie comparan la norma del gradiente de la
primera capa con la de $[0,1]$.

### celda: s05-apuesta

**Apuesta.** Con el mismo $\eta$, ¿qué escala entrenará mejor en el
presupuesto de epochs fijado? ¿Alguna se quedará cerca del azar?
¿Esperas una diferencia clara entre $[0,1]$ y estandarizar?
Escribe tu predicción antes de ejecutar. Después abre la respuesta
plegada al final de la sección.

La celda indica si la loss se volvió infinita o NaN, y en qué paso.
También imprime la epoch de menor loss de validation y su *accuracy*
(proporción de aciertos) en validation. La elección se hace con validation.

### celda: s05-arranque-guia

Las rejillas de arriba muestran la accuracy y la loss por epoch. Dentro de
cada rejilla los paneles comparten ejes. La loss usa escala logarítmica
porque la de los píxeles crudos puede crecer mucho. La línea gris marca
$\log 10$, la loss de asignar la misma probabilidad a cada dígito. Si una
corrida diverge, se detiene y la gráfica omite los valores no finitos.
En ese caso, el último punto de accuracy ya no significa nada: se calculó
con salidas no finitas.

Mirar test en cada epoch es un error en un proyecto real. Test se usa
una sola vez, al final, para reportar. Aquí se muestra solo para aprender
a leer las curvas. Usa solo validation para comparar las corridas.

La primera epoch puede esconder lo que pasó en los primeros pasos.
Ahora repetimos el arranque con los mismos pesos iniciales y el mismo
orden de batches, pero registramos métricas con mayor frecuencia.
La tabla maestra distingue estas corridas por el sufijo `-arranque`.

A la izquierda, mira la loss de train por paso en escala logarítmica.
La referencia gris vuelve a ser $\log 10$. A la derecha, mira la accuracy
de validation por paso. La referencia gris es el $10\%$ de aciertos al
adivinar al azar. Usa la leyenda para identificar cada escala.
¿En cuál baja antes la loss? ¿Alguna se dispara o queda cerca del azar?
¿Desde cuándo se distinguen $[0,1]$ y la escala estandarizada?

### celda: s05-apuesta-respuesta

Con los píxeles crudos, esperamos que el $\eta$ compartido sea demasiado
grande. La loss puede dispararse y provocar una parada, o la accuracy
puede quedarse cerca del azar con una loss finita. Esto último puede
pasar si un salto deja muchas ReLU apagadas para todas las imágenes de
train. Con preactivaciones negativas, esas neuronas dejan de recibir
gradiente. Usa la gráfica y el estado impreso para ver qué pasó en
tu corrida.

En $[0,1]$ y en la escala estandarizada, las entradas son del orden de la
unidad. El mismo $\eta$ suele funcionar en las dos y pueden empatar.
Si la escala estandarizada tiene ventaja, puede verse más en los primeros
pasos que al final. Un empate también es compatible con que ambas escalas
sean adecuadas para este paso.

### celda: s05-pregunta-eta

**Piensa.** Si tuvieras que entrenar con los píxeles crudos, ¿qué
learning rate probarías? ¿Bastaría dividir $\eta$ entre $255^2$?

### celda: s05-pregunta-eta-respuesta

Dividir $\eta$ entre $255^2$ compensa, para una imagen y con el mismo
$\delta^{(1)}_i$, el efecto de actualizar los pesos sobre su preactivación.
El mismo $\eta$ se aplica también a los sesgos. Su gradiente es
$\frac{\partial \ell}{\partial b^{(1)}_i} = \delta^{(1)}_i$, así que
reducir $\eta$ encoge esos pasos sin que haya un factor $x_j$ que compensar.
Además, los logits iniciales pueden ser grandes con los píxeles crudos.
La red los calcula antes del primer paso con $\eta$.

La idea de «Cuánto avanzar» vuelve aquí. La dirección más sensible limita
el paso y el resto puede avanzar muy despacio. Normalizar la entrada
ayuda a usar un paso común. En la sección 9 verás que Adam se adapta en
parte. Para cada parámetro, divide un promedio de sus gradientes por una
estimación de su magnitud típica.

### celda: s05-que-viste

**Qué viste**

- Las tres escalas conservan la información de la imagen. El tamaño del
  gradiente de la primera capa sí depende de la escala.
- Con el mismo $\eta$, los píxeles crudos pueden hacer que la corrida
  diverja o se estanque. $[0,1]$ y la escala estandarizada pueden rendir
  de forma parecida. La gráfica por pasos ayuda a ver cuándo se separan.
- Empieza por fijar una escala de entrada antes de ajustar el learning
  rate o cambiar de *optimizer* (optimizador). Si estandarizas, calcula
  las constantes en train y aplícalas también a validation y test.

La escala estandarizada es el valor por defecto de `Config` en el resto
del notebook. En la sección 8 variamos el learning rate con la escala fija.
