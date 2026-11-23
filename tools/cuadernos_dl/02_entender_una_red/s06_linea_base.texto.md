### celda: s06-intro

## 06 · La línea base y cómo leer tres curvas

Una **línea base** (*baseline*) es una configuración de referencia. En las
siguientes secciones cambiaremos un factor a la vez y compararemos el
resultado con esta corrida.

Usamos la red de la sección 4, $784 \to 128 \to 10$, con una capa oculta de
128 neuronas y activación ReLU. El optimizer es Adam y el learning rate es
$\eta = 10^{-3}$. La configuración completa usa ocho epochs y los 50 000
ejemplos estandarizados de train. La celda reutiliza la corrida
`s04-oculta`. Si falta, avisa y la entrena con la misma configuración.

En la unidad 9 comparaste los errores de regresión en train, validation y
test para distintos grados del polinomio. Aquí leerás la loss y la accuracy
de los tres conjuntos después de cada epoch. La epoch 0 muestra la red
recién inicializada, antes del primer paso de entrenamiento.

En todo el notebook, train va en **azul**, validation en **naranja** y test
en **verde**.

### celda: s06-aviso-test

> **Aviso.** Mirar test en cada epoch está mal: test se usa una sola vez, al final, para reportar. Aquí lo hacemos solo de manera didáctica, para aprender a leer las tres curvas. Ninguna decisión del notebook usa test.

En «Entrenamiento y prueba», en la unidad 9, viste que usar test para elegir
vuelve optimista el resultado que reportas. Volver a mirar test después de
cada cambio guía la elección una decisión a la vez, así que aquí elegimos la
epoch, el modelo y el learning rate $\eta$ con validation.

### celda: s06-referencias

Antes de mirar las curvas, calcula qué esperas de una red que solo adivina.

- **Loss de adivinar uniforme.** Si asigna probabilidad $1/10$ a cada
  dígito, la cross-entropy de cualquier ejemplo es
  $-\log(1/10) = \log 10 \approx 2.30$. La cross-entropy es el negativo del
  logaritmo de la probabilidad asignada a la clase correcta. Es la
  negative log-likelihood (log-verosimilitud negativa) de la regresión
  logística de la unidad 9, ahora con diez clases.
- **Accuracy de azar.** Si eliges un dígito al azar con igual probabilidad
  para todos, esperas acertar el 10 % de las veces.

La celda calcula otra referencia. Si para cualquier imagen predices la
proporción de cada dígito en train, la loss promedio en train es la
entropía de esas proporciones. Sale cerca de $\log 10$ porque MNIST está
casi balanceado.

Con pesos aleatorios pequeños, los logits de la epoch 0 suelen ser
parecidos. El softmax les asigna probabilidades cercanas a $1/10$. Espera
una loss cerca de $\log 10$ y una accuracy cerca del 10 %, con algo de
variación por la inicialización. Una loss inicial muy por encima de
$\log 10$ sugeriría que la red ya asigna probabilidades altas a clases
equivocadas.

Busca una loss por debajo de su referencia y una accuracy por encima de la
suya. Así ves si la red empieza a superar al azar en cada métrica.

### celda: s06-apuesta

**Apuesta.** Escribe tu predicción antes de correr la celda. Al final del
entrenamiento, ¿qué curva tendrá la loss más baja? ¿Cuál tendrá la accuracy
más alta? ¿Qué tan cerca quedarán validation y test?

La figura tiene cuatro paneles. Arriba está la vista completa, con la
epoch 0 y las referencias en gris punteado ($\log 10$ y 10 %). Abajo hay un
acercamiento desde la primera epoch para distinguir las curvas que se
enciman arriba. La línea vertical naranja discontinua marca la epoch
elegida con validation. La curva de test se muestra para la lectura de la
figura.

### celda: s06-apuesta-respuesta

Lo esperable es que train termine con la loss más baja y la accuracy más
alta. La red ajustó sus parámetros con esos datos. En la unidad 9 viste
ese mismo optimismo en el error de entrenamiento.

Validation y test suelen quedar cerca. Para una epoch dada, ambos estiman
cómo le va al mismo modelo con ejemplos de la misma distribución que
quedaron fuera del ajuste de los pesos. Cada conjunto usa una muestra
distinta, así que las curvas pueden quedar a distinta altura por azar de
muestreo. El orden que veas en esta corrida puede cambiar en otra. Si
apostaste por una separación grande, mira el acercamiento y comprueba tu
apuesta. Enseguida pondremos el tamaño de esa diferencia en contexto.

### celda: s06-como-leer

1. **Epoch 0.** Busca las tres curvas cerca de las referencias. Como los
   pesos acaban de inicializarse, train todavía carece de la ventaja que
   le dará el ajuste.
2. **Primera epoch.** Fíjate cuánto cae la loss desde $\log 10$. La mayor
   parte de la caída suele ocurrir aquí. Mira el acercamiento para
   distinguir los cambios posteriores.
3. **Epochs siguientes.** Busca si la loss de train sigue bajando mientras
   las de validation y test bajan más despacio, se aplanan o suben. Ahí se
   abre la brecha.
4. **Las dos métricas.** La accuracy cuenta cuántas veces acierta el
   `argmax`, que elige la clase de mayor probabilidad. La loss también
   responde a la probabilidad asignada a la clase correcta. Por eso las
   dos métricas pueden moverse de forma distinta.

La línea vertical marca la epoch con la menor loss de validation. Esa es
la que guardamos como la mejor. La loss de train puede seguir bajando
porque la red se ajusta con esos datos.

Puede que la loss de validation apenas suba o siga bajando. Si su mínimo
está en la última epoch, esta corrida termina sin mostrar un deterioro
final de la loss de validation.

### celda: s06-brechas

La celda muestra una tabla con una fila por epoch y una figura con un
panel para cada métrica. Fíjate en estas dos diferencias.

- **Train y validation.** En loss se resta validation menos train. En
  accuracy se resta train menos validation. En ambos casos, una brecha
  positiva indica que a la red le va mejor en train. Es el optimismo que
  viste en la unidad 9, $R(\widehat\beta) - L_{\text{ent}}(\widehat\beta)$.
  Aquí, la loss de validation estima $R$, la loss esperada en datos
  nuevos. Si train mejora y la brecha crece, la red puede estar
  aprendiendo detalles de train que se generalizan mal. En «Sesgo y
  varianza», esto corresponde a la varianza y apunta a *overfitting*
  (sobreajuste). Si la brecha es chica y el error sigue alto en ambos
  conjuntos, el patrón apunta a sesgo y *underfitting* (ajuste
  insuficiente).
- **Validation y test.** En loss se resta test menos validation. En
  accuracy se resta validation menos test. Para una epoch fijada de
  antemano, los dos conjuntos estiman el mismo desempeño con muestras
  distintas. En la corrida completa, cada muestra tiene 10 000 ejemplos.
  Como en la unidad 9, una proporción de aciertos $p$ en $n$ ejemplos
  tiene error estándar aproximado $\sqrt{p(1-p)/n}$. La diferencia de dos
  accuracies medidas en muestras independientes suma las dos varianzas:
  su error estándar es
  $\sqrt{p_{\text{val}}(1-p_{\text{val}})/n_{\text{val}} + p_{\text{test}}(1-p_{\text{test}})/n_{\text{test}}}$.
  La celda lo calcula en cada epoch y pinta la banda gris de $\pm 2$
  errores estándar alrededor de cero. La banda sirve solo para la
  diferencia validation − test. Una diferencia dentro de la banda es
  compatible con el ruido de muestreo.

Al elegir la epoch con la menor loss de validation, esa loss puede quedar
algo optimista. El mínimo favorece las estimaciones que salieron bajas por
azar. Test queda fuera de esa elección.

Busca una brecha train–validation que se amplíe y una diferencia entre
validation y test que fluctúe cerca de cero, sin una tendencia clara.

### celda: s06-confianza-intro

¿Cómo puede subir la loss de validation mientras su accuracy se queda casi
igual?

La accuracy cuenta aciertos. La loss promedia $-\log p$ con la probabilidad
$p$ asignada a la clase correcta de cada ejemplo. Imagina dos predicciones
equivocadas. Si una asigna $0.4$ a la clase correcta, cuesta
$-\log(0.4) \approx 0.9$. Si la otra le asigna $0.001$, cuesta
$-\log(0.001) \approx 6.9$. Al seguir entrenando pasan dos cosas a la vez:
los aciertos se vuelven más seguros y cuestan un poco menos, y los errores
que quedan le dan cada vez menos probabilidad a la clase correcta y cuestan
más. Si lo que suben los errores pesa más que lo que bajan los aciertos, la
loss promedio sube, aun con el mismo número de aciertos. Esto conecta con la calibración de la unidad 9. Una probabilidad
predicha debería reflejar la frecuencia con que se cumple lo predicho.

La tabla compara en validation dos *checkpoints* (estados guardados) de la
misma corrida. Uno corresponde a la menor loss de validation y el otro a
la última epoch. Para cada uno muestra:

- La accuracy, la loss promedio y el número de errores.
- En los errores, la probabilidad media de la clase elegida y la
  probabilidad media de la clase correcta. La primera mide la confianza
  con que la red se equivocó; la segunda es la que decide la loss.
- La loss media de un error y la de un acierto. También muestra cuánto
  aporta cada grupo al promedio sobre todos los ejemplos. Los dos aportes
  suman la loss total. Compara los dos aportes entre columnas: ahí se ve
  cuál de los dos movimientos ganó.

El histograma compara la confianza en los errores de los dos checkpoints.
Fíjate si en la última epoch aparecen más errores de confianza alta. Los
errores de un checkpoint y del otro no son exactamente las mismas imágenes,
así que el histograma da la forma general; la tabla da la cuenta. Si la
mejor epoch es la última, la celda avisa que ambas columnas corresponden
al mismo modelo. En ese caso, los histogramas coinciden.

### celda: s06-que-viste

**Qué viste**

- Las tres curvas suelen arrancar juntas cerca de $\log 10$ en loss y del
  10 % en accuracy. El salto mayor suele llegar en la primera epoch.
- Train suele quedar abajo en loss y arriba en accuracy. Es el optimismo
  que viste en la unidad 9.
- Validation y test suelen ir juntas. Usa la banda para ver si la
  diferencia en accuracy cabe en la escala del ruido de muestreo.
- Si la brecha train–validation se abre, busca qué mejora en train
  mientras validation deja de mejorar. Es una señal de varianza.
- Si al final subió la loss de validation con accuracy casi estable,
  revisa si los errores ganaron confianza y aportaron más al promedio. Si
  la loss siguió bajando, la corrida termina con una mejora en validation.
- La mejor epoch se eligió con validation. Test se miró solo para aprender
  a leer las curvas; no decidió nada.

Esta corrida es la referencia de lo que sigue, y la forma de leerla vale
para todas las curvas del notebook. Varias secciones arman su propio
control (con otro subconjunto de datos u otro optimizer) para poder mover
un factor a la vez: el batch, el learning rate, el optimizer, el tamaño de
la red o la activación. En todas, las tres curvas se leen como aquí.
