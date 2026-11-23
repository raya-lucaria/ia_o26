### celda: s13-intro

## 13 · Activaciones

En la red 2–3–2–1 de la clase 1, cada capa oculta hacía dos operaciones.
Primero calculaba la preactivación
$\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$.
Luego aplicaba $g^{(l)}$ a cada componente para obtener
$\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$. Sin esas funciones no lineales,
toda la red se reduciría a una sola transformación afín.

- **ReLU**, la de las capas ocultas de la clase 1, es $g(z)=\max(0,z)$.
- **Sigmoide**, la de la regresión logística de la unidad 9, es
  $\sigma(z)=1/(1+e^{-z})$.
- **tanh** es $g(z)=\tanh(z)=(e^z-e^{-z})/(e^z+e^{-z})$.
- **GELU** es $g(z)=z\,\Phi(z)$, donde $\Phi$ es la función de distribución
  acumulada de la normal estándar. Se parece a una ReLU suave.

Las cuatro redes reciben los 784 píxeles, tienen seis capas ocultas de 128
neuronas y entregan diez logits. Empiezan con los mismos pesos, inicializados
con matrices ortogonales, y sesgos en cero. Cambia la activación de las capas
ocultas. Usaremos esta arquitectura también en §14 y §15.

Primero mira las funciones y sus derivadas. Después compara los gradientes y
las activaciones al inicio. Al final, compara cómo arrancan las curvas de
entrenamiento.

### celda: s13-derivadas-lectura

Cada columna muestra una activación. Arriba está $g(z)$ y abajo, su pendiente
$g'(z)$. PyTorch calcula las pendientes con autograd, el mismo mecanismo que
usa para backpropagation. El código imprime el máximo que encuentra entre los
puntos graficados.

- **Sigmoide.** Si $p=\sigma(z)$, entonces $\sigma'(z)=p(1-p)$. El producto
  alcanza su máximo en $p=\tfrac12$, cuando $z=0$. Vale $\tfrac14$, el nivel de
  la línea punteada. Lejos de cero la curva se aplana y la pendiente se acerca
  a cero. A esto le llamamos saturación.
- **tanh.** También se satura lejos de cero. Su curva es simétrica respecto
  al origen. La pendiente $1-\tanh^2(z)$ llega a $1$ en $z=0$.
- **ReLU.** La pendiente vale $0$ si $z<0$ y $1$ si $z>0$. PyTorch toma
  $g'(0)=0$. Una neurona activa, con $z>0$, deja pasar el gradiente con su
  pendiente de $1$.
- **GELU.** Su pendiente cambia suavemente. En parte del lado negativo es
  un poco menor que cero. En parte del lado positivo supera $1$.

### celda: s13-atenuacion

Recuerda la regla de la cadena de la clase 1. Para una observación,
$\mathbf{δ}^{(l)}=\nabla_{\mathbf z^{(l)}}\ell$ es el error que llega a la
preactivación de la capa $l$. En una capa oculta se calcula así.

$$
\mathbf{δ}^{(l)}
=\bigl((\mathbf W^{(l+1)})^\top\mathbf{δ}^{(l+1)}\bigr)
\odot g^{(l)\prime}(\mathbf z^{(l)}).
$$

Primero la matriz transpuesta lleva la señal a la capa anterior. Después
$\odot$ multiplica cada componente por la pendiente de su activación. Con la
sigmoide, este segundo paso deja como máximo una cuarta parte de la norma de
la señal que entregó la matriz.

Al inicio, las matrices de esta red tienen filas ortonormales, incluso
las rectangulares. Así, la transpuesta de cada una conserva la norma del
vector que recibe. La norma espectral $\lVert\mathbf W^{(l)}\rVert_2$ mide
cuánto puede amplificar un vector la matriz o su transpuesta. El código
imprime esas normas y las usa al calcular la cota.

Al pasar hacia atrás por seis capas ocultas con sigmoide, la cota al inicio
es $\lVert\mathbf{δ}^{(1)}\rVert_2\le(\tfrac14)^6
\lVert\mathbf{δ}^{(7)}\rVert_2$, con normas espectrales unitarias. La
atenuación puede ser mayor si las pendientes están por debajo de
$\tfrac14$. Esto es *vanishing gradient* (desvanecimiento del gradiente).
ReLU y tanh también pueden atenuar la señal, aunque su pendiente máxima de
$1$ permite que pase entera en algunas componentes.

El gradiente de los pesos también incluye la activación que entra a la capa.
Para una observación,
$\nabla_{\mathbf W^{(l)}}\ell=\mathbf{δ}^{(l)}(\mathbf a^{(l-1)})^\top$.
Con un mismo learning rate $\eta$, un gradiente de pesos pequeño produce
un cambio pequeño en esos pesos.

### celda: s13-apuesta

Escribe tus dos apuestas antes de seguir.

1. Antes del primer paso, ¿qué activación dará el menor gradiente de los pesos
   en la capa 1, la más cercana a la entrada?
2. Al terminar el presupuesto de pasos, ¿qué activación tendrá la mayor loss
   de validation?

Abre la respuesta plegada después de ver las gráficas y la tabla.

### celda: s13-gradiente-texto

Tomamos un batch fijo de train y pasamos las mismas imágenes por las cuatro
redes. En el forward, `retain_grad()` le pide a PyTorch que conserve el
gradiente de cada preactivación. Calculamos la cross-entropy promedio del
batch, $L_{\mathcal B}$, y llamamos una vez a `backward()` por red. Los pesos
siguen en sus valores iniciales.

En el notebook 01, cada observación era una columna. En PyTorch es una fila.
En una capa oculta, `z.grad` tiene una fila por imagen y una columna por
neurona. Cada fila contiene el $\mathbf{δ}^{(l)}_k$ de esa imagen,
multiplicado por $1/\lvert\mathcal B\rvert$ porque la loss es un promedio.

Medimos dos normas por capa.

- $\lVert\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\rVert_F$ resume el tamaño del
  gradiente que usaría el optimizer para actualizar los pesos.
- La norma de Frobenius de `z.grad` mide el tamaño de la señal que pasa
  hacia atrás en todo el batch.

La tabla muestra la primera norma. Las filas son las capas, de la 1 junto a
la entrada a la 7 de salida. Las columnas son las cuatro activaciones.

### celda: s13-lee-gradiente

En cada panel, sigue las barras de un mismo color de derecha a izquierda,
de la salida a la entrada. La escala vertical es logarítmica. Bajar una
potencia de diez significa dividir la norma entre diez.

En el panel derecho, la línea negra discontinua parte del error medido a
la salida de la red con sigmoide. Por cada capa hacia la entrada, multiplica
por $\tfrac14$ y por la norma espectral de la matriz transpuesta. Las barras
moradas quedan en esa cota o por debajo, salvo redondeo. Busca una caída más
pronunciada para la sigmoide. El código imprime, para cada activación, la
razón entre las normas del error en la capa 1 y en la salida. Compara la
razón de la sigmoide con $(\tfrac14)^6$. La cota también vale para las
normas del batch.

El panel izquierdo muestra los gradientes de los pesos. Ahí también
intervienen las activaciones de la capa anterior. Usa el panel derecho para
comprobar la cota.

### celda: s13-lee-histogramas

Cada fila usa una función de activación. Cada columna corresponde a una
capa oculta. Un histograma reúne los valores de todas las neuronas de esa
capa para el mismo batch de train, antes del primer paso. Compara la
desviación estándar impresa de izquierda a derecha para ver si la
dispersión se reduce o se mantiene.

- **Sigmoide.** Busca salidas positivas agrupadas cerca de $\tfrac12$.
  Allí la pendiente está cerca de su máximo y aun así vale a lo sumo
  $\tfrac14$.
- **tanh.** Mira si las salidas se agrupan alrededor de cero y cómo cambia
  su dispersión.
- **ReLU.** Busca el pico en cero. Ahí caen las neuronas apagadas, que
  tienen pendiente cero.
- **GELU.** Busca también valores negativos pequeños. La transición
  alrededor de cero es suave.

Las preactivaciones determinan en qué tramo de $g$ cae cada neurona y cuánta
señal deja pasar su pendiente. En §15 veremos *batch normalization*
(normalización por batch), que usa estadísticas del batch para centrar y
reescalar preactivaciones durante el entrenamiento.

### celda: s13-entrenar-texto

Ahora entrenamos las cuatro redes con `config_profunda`. Usamos SGD sin
momentum, con el mismo learning rate, el mismo orden de batches y el mismo
presupuesto de pasos. En modo normal, el presupuesto cubre poco más de una
epoch. La pregunta es cuál empieza a aprender en ese tramo. El código
imprime cuántos pasos completó cada corrida y guarda la norma del gradiente
de cada capa en cada paso; la usamos después de las curvas.

Los paneles de `s13-relu`, `s13-sigmoide`, `s13-tanh` y `s13-gelu`
comparten ejes. El eje horizontal cuenta pasos de SGD. Al inicio y conforme
avanza el entrenamiento, el código evalúa train, validation y test sobre
todos los ejemplos cargados de cada conjunto. La línea punteada marca
$\log 10$ en la gráfica de loss, el valor de asignar probabilidad uniforme
a los diez dígitos. En accuracy, marca el $10\,\%$ esperado al adivinar
al azar.

Mirar test en cada evaluación está mal. En un proyecto, test se usa una
sola vez, al final. Aquí lo mostramos solo para aprender a leer las curvas.
Todas las comparaciones de desempeño para decidir usan validation.

Puede que una red se quede cerca de la referencia del azar durante toda
la corrida. También puede que ReLU, tanh y GELU queden cerca entre sí. Para
la segunda apuesta, consulta la columna de loss de validation final.

### celda: s13-lee-durante

Las barras de antes eran una foto de la red recién creada. Estas curvas
siguen la norma del gradiente de los pesos en cada paso del entrenamiento:
a la izquierda la capa 1, junto a la entrada; a la derecha la de salida.
El eje vertical es logarítmico y los dos paneles comparten escala.

Compara la distancia vertical entre la sigmoide y las demás en el panel
izquierdo con la del panel derecho. Si en la capa 1 la curva de la sigmoide
sigue muy por debajo de las otras mientras en la salida están cerca, la
atenuación no fue un accidente del primer paso: se mantiene mientras se
entrena. Las curvas son ruidosas porque cada paso usa un batch distinto;
fíjate en el nivel, no en cada pico. §14 estudia este gradiente por capa
con más detalle.

### celda: s13-apuesta-respuesta

1. **Al inicio, esperamos que sea la sigmoide.** Las seis pendientes
   limitan la señal que llega a la primera capa. Con las normas iniciales
   unitarias, el error de esa capa mide como máximo $(\tfrac14)^6$ veces
   el de salida. Comprueba la apuesta sobre los pesos en la primera fila
   de la tabla de gradientes.
2. **Al final, también esperamos que sea la sigmoide.** Si sus primeras
   capas reciben gradientes pequeños, cambian poco con el mismo learning
   rate. La respuesta observada está en la columna de loss de validation
   final. Si el orden difiere de tu apuesta, usa el que muestra la tabla.
   La cota se aplica al error inicial por capa.

### celda: s13-que-viste

La pendiente de la sigmoide alcanza como máximo $\tfrac14$, incluso cerca
del centro de su curva. En los histogramas, ese tramo corresponde a
activaciones cercanas a $\tfrac12$. Al retroceder por las capas, las
pendientes se multiplican con los pesos transpuestos. El panel del error
muestra cuánta señal logra llegar a la primera capa al inicio.

En las curvas, fíjate en qué redes se alejan de la referencia del azar y
cuáles tardan más. Si la sigmoide se queda cerca de esa línea, relaciona ese
arranque lento con el tamaño de sus gradientes iniciales. Las curvas
también permiten ver si varias activaciones arrancan a un ritmo parecido.

ReLU y GELU son opciones habituales en capas ocultas profundas. La sigmoide
sigue sirviendo en regresión logística binaria para convertir un logit en
probabilidad. En §14 seguiremos el gradiente por capa durante el
entrenamiento, con sigmoide, ReLU y ReLU con batch normalization. En §15
veremos cómo batch normalization cambia la escala de las señales.
