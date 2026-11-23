### celda: s08-intro

## 08 · El learning rate

![Tres pelotas con distinto learning rate](ilustracion:learning_rate)
*(Ilustración generada con gpt-image-2.)*

En la clase 1 actualizaste los pesos y sesgos con gradient descent (descenso
por gradiente). La regla era $\theta \leftarrow \theta - \eta\,\nabla L(\theta)$.
El negativo del gradiente indica hacia dónde bajar. El learning rate (tasa
de aprendizaje) $\eta$ multiplica ese vector y controla el tamaño del paso.
Hace el papel de $\alpha$ en la unidad 6.

Mira las tres pelotas, cada una en su valle. A la izquierda, con pasos
pequeños, la pelota apenas avanza. En el centro, con pasos intermedios,
llega al fondo. A la derecha, con pasos grandes, rebota entre las paredes
y sale del valle.

Primero veremos cuándo un paso produce avance lento, descenso rápido,
oscilaciones o divergencia en una cuadrática sin datos. Después buscaremos
esos patrones al entrenar en MNIST con SGD y Adam.

### celda: s08-cuadratica-texto

Partimos de $(1,1)$ y queremos llegar al mínimo $(0,0)$ de
$f(x,y)=\tfrac12(x^2+100y^2)$. La curvatura, medida por la segunda derivada,
es $1$ en $x$ y $100$ en $y$. Por eso el valle es largo en $x$ y angosto en $y$.
Las curvas de nivel unen puntos con el mismo valor de $f$ y forman elipses
alargadas en $x$.

El gradiente es $\nabla f(x,y)=(x,100y)$. Cada paso multiplica $x$ por
$1-\eta$ y $y$ por $1-100\eta$. Como ambas coordenadas empiezan fuera de
cero, las dos tienden a cero si y solo si ambos factores tienen valor
absoluto menor que $1$. La dirección más empinada impone el límite de
estabilidad $0<\eta<2/100=0.02$. En ese intervalo, el factor $1-\eta$
queda cerca de $1$, así que el avance en $x$ es lento.

- Con $\eta=0.001$, los factores son $0.999$ en $x$ y $0.9$ en $y$.
  La trayectoria baja hacia el fondo del valle y apenas avanza en $x$.
- Con $\eta=0.01$, el factor en $y$ es $0$. Esa coordenada llega a cero
  en un paso y después $x$ se reduce por un factor de $0.99$ en cada paso.
- Con $\eta=0.018$, el factor en $y$ es $-0.8$. La trayectoria cambia de
  lado en cada paso y el zigzag se va apagando.
- Con $\eta=0.025$, el factor en $y$ es $-1.5$. Cada salto cruza el valle
  y queda más lejos del centro. La trayectoria diverge.

El código imprime los factores y dibuja un panel por $\eta$, con los mismos
ejes. El cuadro negro marca el inicio y la estrella roja, el mínimo. Los
puntos azules marcan los pasos sobre las curvas de nivel grises.

### celda: s08-cuadratica-f-texto

Ahora mira el valor de $f$ en cada paso. El eje vertical está en escala
logarítmica. Si $f$ se multiplica por el mismo factor en cada paso, la curva
se ve como una recta. Baja si el factor es menor que $1$ y sube si es mayor.
La corrida que diverge acaba por salirse por arriba.

Fíjate en cuál termina más abajo. Con $\eta=0.018$, la trayectoria oscila
en $y$ y logra una $f$ final menor que con $\eta=0.01$. Una vez que el
zigzag se apaga, domina la dirección plana. Ahí el factor $0.982$
reduce $x$ más rápido que $0.99$.

El learning rate fijo que minimiza el mayor de los dos factores en valor
absoluto es $\eta=2/101\approx0.0198$. En ese punto ambos factores tienen la
misma magnitud y signos opuestos. El valor queda cerca del límite de
estabilidad. Al final, el código imprime $x$, $y$ y $f$ para cada trayectoria.

### celda: s08-mnist-texto

Pasamos a clasificar los dígitos de MNIST con una red de una capa oculta
con ReLU. Cerca de un mínimo, la loss (pérdida) de una red puede aproximarse
con una cuadrática. Sus direcciones pueden tener curvaturas muy distintas,
como en el valle que acabamos de ver.

Haremos un barrido de $\eta$ con cada optimizer (optimizador). Todas las
corridas arrancan con los mismos pesos y sesgos y recorren los batches en
el mismo orden. El tamaño del batch también se mantiene fijo. Con SGD
(stochastic gradient descent), el paso sigue el gradiente del batch
multiplicado por $-\eta$. Adam ajusta el paso de cada parámetro según sus
gradientes recientes. Por eso la escala de $\eta$ puede ser distinta. La
sección 9 vuelve a Adam con más detalle.

En cada corrida medimos la loss sobre train y validation al inicio y luego
a intervalos. Todas las tasas tienen el mismo presupuesto de pasos, que
se reduce en modo `RAPIDO`. Este tramo corto nos permite comparar el arranque.

Si la loss de un batch llega a infinito o a `NaN` (*Not a Number*), la
función `entrenar` detiene esa corrida y registra el primer paso no finito.
El barrido sigue con las demás tasas.

En una red con ReLU y cross-entropy, un $\eta$ demasiado grande no siempre
produce `NaN`. A menudo la loss da saltos y luego se atasca cerca de
$\log 10$ o más arriba: la red deja de aprender sin que ningún número se
desborde. Por eso el barrido de SGD termina con $\eta=1000$, un valor
absurdo a propósito, para ver un `NaN` de verdad y comprobar que el
notebook no truena. Puede que ninguna corrida de Adam diverja.

### celda: s08-apuesta

**Apuesta.** Antes de ejecutar, mira las tasas en `BARRIDO_LR` y escribe
cuál dará la menor loss final de validation con SGD y cuál con Adam.
¿Esperas que gane la misma tasa en ambos? ¿Cuáles crees que divergirán?

Abre «Respuesta» después de ver la gráfica de la «U».

### celda: s08-rejilla-texto

Cada figura reúne las corridas de un optimizer. Los paneles van de menor
a mayor $\eta$ y comparten los ejes. El horizontal cuenta las actualizaciones
y el vertical muestra la loss de cross-entropy (entropía cruzada). Azul es
train y naranja es validation. La línea punteada marca $\log 10$, la loss
de asignar la misma probabilidad a cada dígito.

Con una tasa baja, la loss puede quedarse cerca de la línea punteada.
Busca tasas que la hagan bajar pronto y compáralas con las que bajan a
saltos o rebotan. Los valores que quedan por encima del panel son peores
que la referencia uniforme; cuando eso pasa, el panel escribe en rojo el
máximo que alcanzó. Si una corrida se detuvo por divergencia,
el panel marca en rojo el primer paso con loss no finita. Las curvas
solo muestran evaluaciones finitas.

En un tramo tan corto, train y validation pueden seguirse de cerca. Mira
qué tan pronto bajan y qué tan estable es el descenso. Si empiezan a
separarse, fíjate en cuál sigue bajando.

### celda: s08-u-texto

Cada marca corresponde a una corrida. El eje horizontal muestra $\eta$
en escala logarítmica. Dos saltos del mismo tamaño en ese eje multiplican
$\eta$ por el mismo factor. El eje vertical muestra la loss de validation
al final de la corrida.

Los círculos morados son de SGD y los cuadrados cafés, de Adam. Una
$\times$ arriba marca una corrida que divergió o terminó con una loss de
validation no finita. Si un valor finito rebasa el rango elegido para la
loss, su marca queda en el techo como un triángulo hueco, con el valor
escrito al lado. La tabla trae todos los valores.

Busca una «U». A la izquierda, los pasos pequeños pueden dejar la loss
alta. En medio, algunas tasas pueden bajarla más. A la derecha pueden
aparecer valores altos o un salto directo a $\times$. También puede haber
un fondo plano con varias tasas casi empatadas.

El código imprime la tasa con menor loss final de validation para cada
optimizer que tenga corridas válidas. La tabla muestra la loss final de
train y validation y la accuracy (proporción de aciertos) de validation.
También indica si cada corrida divergió y el primer paso no finito cuando
se detectó.

### celda: s08-apuesta-respuesta

Compara tu apuesta con el ganador que imprimió el código para cada
optimizer. Mira en la tabla si alguna otra tasa quedó cerca.

En este barrido cabe esperar que la tasa útil de SGD sea mayor que la de
Adam. En SGD, un gradiente pequeño da un paso pequeño para el mismo
$\eta$. Adam divide el promedio reciente del gradiente de cada parámetro
por una estimación de su escala. Así, un mismo $\eta$ puede dar tamaños
de paso distintos con los dos optimizers. Si cambias de optimizer, vuelve
a comparar tasas con validation.

Con SGD, $\eta=1000$ está puesto para divergir. Las tasas grandes que
quedan antes, como $\eta=5$, pueden terminar con una loss finita: mira en
su panel si la loss dio saltos y se quedó alta en lugar de bajar.

### celda: s08-que-viste

- **Paso muy pequeño.** La loss puede quedarse cerca de $\log 10$.
  En la cuadrática, el factor de la dirección plana queda casi en $1$.
- **Paso que funciona bien.** La loss baja pronto y de forma sostenida.
- **Paso grande.** En MNIST puedes ver rebotes en la loss. En la cuadrática,
  un factor negativo hace que la coordenada cambie de signo en cada paso.
- **Divergencia.** En la cuadrática, $|1-100\eta|>1$ hace crecer $|y|$.
  En MNIST, el código detiene la corrida si detecta infinito o `NaN`
  en la loss de un batch. Antes de llegar ahí puede haber una zona donde
  la loss salta y se atasca alta sin volverse `NaN`.

En la sección 7 vimos que un batch más grande da un gradiente menos
ruidoso. Eso puede permitir un learning rate mayor. Si cambias el batch,
vuelve a revisar $\eta$.

El learning rate es un hiperparámetro. Como en la unidad 9, elígelo
con validation y reserva test para reportar el resultado al final.
