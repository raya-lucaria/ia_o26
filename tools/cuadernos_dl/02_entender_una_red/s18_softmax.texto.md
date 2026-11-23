### celda: s18-intro

## 18 · Softmax y la loss

Hasta aquí entrenamos con `CrossEntropyLoss`. ¿Qué recibe esa función y qué
mide la loss (pérdida)? Empecemos con la salida de la red para un solo dígito.

La última capa lineal entrega diez **logits** (puntajes), uno por cada clase
$c=0,\dots,9$. Con la notación de la clase 1, son las preactivaciones de la
última capa, $\mathbf z = \mathbf W^{(L)}\mathbf a^{(L-1)}+\mathbf b^{(L)}$.
La red entrega ese vector directamente, sin aplicar una activación final.
Los logits pueden ser negativos y su suma puede tomar cualquier valor.

**Softmax** convierte esos puntajes en probabilidades. Eleva $e$ a cada
logit y divide cada resultado entre la suma de todos.

$$\widehat y_c = \frac{e^{z_c}}{\sum_{j=0}^{9} e^{z_j}}.$$

En aritmética exacta, cada probabilidad queda entre 0 y 1, sin incluir los
extremos, y todas suman 1. La exponencial conserva el orden y el denominador
es común a todas las clases. Sumar la misma constante a todos los logits
multiplica el numerador y el denominador por el mismo factor, así que las
probabilidades quedan iguales.

Es el mismo softmax de la regresión logística multiclase de la unidad 9.
En §4 vimos esa regresión como una red sin capas ocultas. Las capas ocultas
cambian cómo se calculan los logits. La fórmula que los convierte en
probabilidades sigue siendo la misma.

Cargamos el checkpoint de la mejor epoch del modelo elegido en §16 por
validation (validación). Si esa corrida falta, usamos la línea base de §4 y
la entrenamos si hace falta. La celda indica qué modelo usó y comprueba con
un `assert` que sus capas no incluyen `nn.Softmax`. Veremos los logits de
un dígito real, cómo la temperatura modifica sus probabilidades y cómo
calcular la loss de forma estable. Al final, el dibujo ubica cada paso.

### celda: s18-un-digito-mira

A la izquierda está el dígito de validation. En el centro están sus logits.
La línea negra marca el cero. A la derecha están las probabilidades del
softmax. En ambos paneles de barras, el naranja señala la clase verdadera $y$.

El código busca el primer acierto con una probabilidad máxima mayor que
$0.5$ y menor que $0.9$. Así podemos ver un caso en que el modelo acierta
con algo de duda. Si no encuentra un ejemplo así, muestra el acierto con
la confianza más baja.

Compara las barras más altas. Ambas corresponden a la misma clase. Una
diferencia de pocos puntos entre logits puede producir una gran diferencia
entre probabilidades, porque su cociente es $e^{z_c-z_j}$ para las clases
$c$ y $j$. Hasta un logit negativo aporta una cantidad positiva en la
fórmula.

La tabla muestra la cuenta para cada clase. Sigue $z_c$, luego $e^{z_c}$ y
por último $\widehat y_c$, que es la altura de la barra de la derecha.
Debajo se imprimen la suma de las probabilidades y los dos `argmax`
(índices del máximo). Para predecir la clase basta con el `argmax` de
los logits.

### celda: s18-apuesta

La **temperatura** $T>0$ divide todos los logits entre el mismo número antes
de aplicar softmax. Con $T=1$ recuperamos las probabilidades del modelo
tal cual.

$$\widehat y_c(T)=\frac{e^{z_c/T}}{\sum_{j=0}^{9}e^{z_j/T}}.$$

La confianza es la probabilidad más alta. Como vimos en la unidad 9, un
modelo puede acertar mucho y aun así estar mal calibrado. Por ejemplo,
puede acertar con menos frecuencia de la que su confianza sugiere. La
temperatura se puede usar para ajustar esa confianza. En modelos de
lenguaje también se usa para ajustar las probabilidades al muestrear.

**Apuesta antes de correr.** Para el mismo dígito y
$T\in\{0.5,1,2,5\}$, ¿cambia la clase predicha? ¿Qué le pasa a la barra
más alta al subir o bajar $T$? ¿Cambia la loss de ese ejemplo,
$-\log\widehat y_y(T)$? Si aplicaras la misma $T$ a todo validation,
¿cambiaría la accuracy (proporción de aciertos)?

Los cuatro paneles comparten eje vertical. La tabla muestra para cada $T$
el `argmax`, la confianza, la probabilidad de la clase verdadera y la
loss del dígito.

### celda: s18-apuesta-respuesta

- **Clase predicha.** Dividir entre $T>0$ conserva el orden de los logits.
  El `assert` comprueba que el `argmax` del dígito se mantiene.
- **Confianza.** Bajar $T$ ensancha las diferencias entre logits. La barra
  más alta crece. Cuando $T\to 0$, la probabilidad se concentra en la clase
  ganadora o se reparte entre las clases empatadas en el máximo. Subir $T$
  reduce las diferencias y baja la barra más alta. Cuando $T\to\infty$,
  cada clase se acerca a $1/10$.
- **Loss del dígito.** Depende de la barra naranja. Si la clase verdadera
  tiene el logit más alto, al bajar $T$ su probabilidad sube y su loss baja.
  Si el modelo no acertara ningún ejemplo de validation, el respaldo sería
  un error; entonces lee el cambio directamente en la columna
  $\widehat y_y$ de la tabla. Una
  probabilidad menor para la clase verdadera implica una loss mayor.
- **Accuracy de validation.** En aritmética exacta, cada predicción se
  conserva, así que la accuracy queda igual. La loss promedio sí puede
  cambiar. En §6 vimos cómo los errores más confiados pueden elevar la
  loss de validation con la misma accuracy.

Ajustar $T$ en validation para calibrar el modelo se llama *temperature
scaling*. Aquí solo probamos temperaturas fijas en este dígito.

### celda: s18-cross-entropy-texto

La **cross-entropy** (entropía cruzada) de un ejemplo con etiqueta entera
$y$ es $\ell=-\log\widehat y_y$. Tomamos la probabilidad asignada a la clase
verdadera y le aplicamos el logaritmo natural, $\ln$ en la unidad 9, con
signo menos. Con $\widehat y_y=1$ la loss vale cero. Cuando $\widehat y_y$
se acerca a cero, la loss crece sin límite. Si das la misma probabilidad
a los diez dígitos, la loss es $\log 10\approx 2.30$, la referencia de §6.

Es la pérdida logarítmica de la regresión logística de la unidad 9. Para
$n$ observaciones independientes, la verosimilitud de las etiquetas
observadas es el producto $\prod_{k=1}^{n}\widehat y_{k,y_k}$. El logaritmo
del producto es una suma. Al cambiarle el signo y dividir entre $n$ queda

$$L(\theta) = \frac{1}{n}\sum_{k=1}^{n} -\log\widehat y_{k,y_k}.$$

Aquí la cross-entropy es la **negative log-likelihood** (menos
log-verosimilitud) por ejemplo, promediada sobre el conjunto. Minimizarla
equivale a maximizar la verosimilitud.

En PyTorch, `nn.CrossEntropyLoss()(logits, y)` da lo mismo que
`nn.NLLLoss()(torch.log_softmax(logits, dim=1), y)`. Las dos llamadas usan
etiquetas enteras del 0 al 9. `log_softmax` calcula las
log-probabilidades por fila. `NLLLoss` recibe esos logaritmos, toma el
de cada clase verdadera, cambia su signo y promedia. `CrossEntropyLoss`
recibe los logits y combina ambos pasos.

La celda compara primero la cuenta del dígito con `F.cross_entropy`.
Después muestra cuatro cálculos de la loss de validation. Compara
el promedio explícito de las pérdidas por ejemplo con
`CrossEntropyLoss`, `NLLLoss` sobre `log_softmax` y `evaluar` de la
caja. Un `assert` verifica que los cuatro coincidan dentro de una
tolerancia.

### celda: s18-cross-entropy-mira

La tabla comprueba cómo se calcula la loss de las curvas. En cada conjunto
se promedia $-\log\widehat y_y$ sobre sus ejemplos.

En la gráfica izquierda, el eje horizontal es la probabilidad de la clase
verdadera y el vertical es su loss. El punto gris marca la referencia
uniforme $\log 10$. El naranja es el dígito que acabamos de ver. Cerca de 1,
aumentar la probabilidad ahorra poca loss. Cerca de 0, una probabilidad
todavía menor cuesta mucho.

A la derecha, cada barra cuenta ejemplos de validation en un intervalo de
loss. El eje vertical está en escala logarítmica. Busca una concentración
de ejemplos con poca loss y fíjate si aparece una cola de ejemplos con
loss alta. La línea discontinua marca el promedio y la punteada marca
$\log 10$. Los errores confiados que viste en §16 pueden contribuir mucho
al promedio. Si se vuelven más confiados, la loss puede subir aunque la
cantidad de aciertos siga igual, como en §6.

### celda: s18-estabilidad-texto

¿Por qué conviene juntar softmax y el logaritmo en el cálculo de la loss?
El notebook entrena en `float32`, un formato con un rango limitado.
El menor positivo normal es aproximadamente $1.2\times10^{-38}$. Incluso
el menor positivo representable, contando los subnormales, es de apenas
$1.4\times10^{-45}$. Un valor tan pequeño como $e^{-1000}$ se redondea a
cero. Eso es *underflow*. En el otro extremo, $e^{89}$ supera el máximo
representable y produce `inf`. Eso es *overflow*.

Probemos con dos clases, logits $\mathbf z=(0,-1000)$ y etiqueta verdadera
$y=1$. La clase verdadera recibe una probabilidad diminuta. Su
log-probabilidad exacta es $-1000-\log(1+e^{-1000})\approx-1000$.
La loss es enorme y finita, aproximadamente $1000$.

La tabla pone el valor de referencia al lado de cada resultado en
`float32`. La primera fila muestra la log-probabilidad de la clase 1 con
`softmax(z).log()`. Las otras tres muestran la loss calculada con
`NLLLoss(softmax(z).log())`, `NLLLoss(log_softmax(z))` y
`CrossEntropyLoss(z)`. **Antes de correr, predice qué filas darán un
resultado finito.**

### celda: s18-estabilidad-mira

En la tabla, `softmax(z)` produjo $(1,0)$ por *underflow*. Tomar el
logaritmo de la probabilidad de la clase 1 dio $-\infty$. Al cambiarle el
signo, `NLLLoss` devolvió $+\infty$. Un solo ejemplo así puede volver
infinita la loss del batch y producir gradientes `NaN`. Los cálculos
con `log_softmax` y `CrossEntropyLoss` devolvieron $1000$.

El truco **log-sum-exp** usa que desplazar todos los logits por la misma
constante deja el softmax igual. Toma $m=\max_j z_j$ y escribe

$$\log\widehat y_c
= z_c-\log\sum_j e^{z_j}
= z_c-m-\log\sum_j e^{z_j-m}.$$

Ahora la exponencial más grande es $e^0=1$. Las demás pueden redondearse
a cero, pero la suma siempre vale al menos 1. Para $(0,-1000)$, esa suma
se redondea a 1 en `float32`. Su logaritmo es cero y el término $z_1-m$
da directamente $-1000$.

La segunda celda contrasta el cálculo directo con el estable en ambos
extremos. Con $(1000,0)$, el softmax ingenuo intenta dividir
$\infty/\infty$ y aparece `nan`. La versión a mano con log-sum-exp y
`torch.log_softmax` dan resultados finitos para ambos pares. Un `assert`
verifica que las dos versiones estables coincidan, dentro de la tolerancia,
en los logits de todo validation.

Para obtener log-probabilidades, usa `log_softmax`. Para calcular la
cross-entropy, pasa los logits directamente a `CrossEntropyLoss`.

### celda: s18-arquitectura-texto

El dibujo reúne la arquitectura del modelo cargado y el cálculo de softmax
para el mismo dígito. A la izquierda, `dibujar_red` muestra las capas del
MLP. A la derecha, sigue los diez logits hasta sus diez probabilidades.
La barra naranja vuelve a marcar la clase verdadera.

La última capa lineal del `nn.Sequential` entrega los diez logits.
Durante el entrenamiento, `CrossEntropyLoss` calcula log-softmax de
forma estable y aplica la negative log-likelihood. Para predecir la clase
basta el `argmax` de los logits. Aplica softmax explícitamente cuando
quieras ver probabilidades, como en el análisis de confianza y calibración
de §16.

### celda: s18-que-viste

**Qué viste**

- La red entrega logits. Softmax conserva su orden y los convierte en
  probabilidades que suman 1.
- La temperatura cambia la confianza y puede cambiar la loss. Conserva el
  `argmax` de cada ejemplo y, por tanto, la accuracy.
- La cross-entropy de un ejemplo es $-\log\widehat y_y$. Su promedio es la
  loss de las curvas del notebook.
- Con etiquetas enteras, ese promedio es la negative log-likelihood por
  ejemplo, como en la regresión logística de la unidad 9.
- En `float32`, hacer softmax y luego tomar el logaritmo puede producir
  infinitos o `NaN`. Log-sum-exp permite calcular directamente las
  log-probabilidades de forma estable.

Negative log-likelihood y cross-entropy son la misma cantidad; la
diferencia está en cómo se calcula. Por eso los modelos del notebook
terminan en logits y el entrenamiento los entrega directamente a
`CrossEntropyLoss`, que hace log-softmax y la negative log-likelihood en un
solo paso estable.
