### celda: s16-intro

## 16 · Análisis del error

Hasta aquí comparamos corridas por sus curvas de *loss* (pérdida) y *accuracy*
(proporción de aciertos). Ahora abrimos una sola corrida. Queremos saber qué
dígitos confunde, cuánta confianza tiene cuando falla y si esa confianza
corresponde a la frecuencia con que acierta.

Buscamos en `CORRIDAS` las corridas de §4 a §15 hechas con `construir_red`,
con al menos una capa oculta (la regresión logística de §4 no es un MLP), que
terminaron sin divergir y usaron todo el conjunto de *train* disponible, con etiquetas
originales (`50k-limpio`). Como en la unidad 9, para comparar el efecto de una
configuración conviene mantener fijos los datos de train. Las corridas sobre
subconjuntos o con etiquetas alteradas, como las de §10, responden a otras
preguntas. Si saltaste secciones y faltan candidatos, la celda anuncia y
entrena la línea base `s04-oculta`.

La elección tiene dos pasos. Para cada corrida, la caja guardó el *checkpoint*
(copia del estado del modelo) de la *epoch* con menor loss de *validation*.
Entre esos checkpoints gana el de mayor accuracy de validation. Lo
restauramos con `cargar(…, "mejor")`, igual que al recuperar el mejor estado
en *early stopping* (§10). Validation decide la elección completa.

Usamos validation para explorar los errores y reservamos el diagnóstico en
*test* para el reporte final. Las secciones 17 y 18 recuperan la corrida
ganadora de `CORRIDAS["s16-elegido"]`. Su ID original queda en `ELEGIDO_ID`.

### celda: s16-apuesta

**Apuesta.** Escribe dos pares de dígitos que esperas ver entre las
confusiones más frecuentes. Anótalos en el orden real → predicho. Piensa en
los trazos que se parecen cuando alguien escribe a mano.

¿Esperas una matriz simétrica? Por ejemplo, ¿crees que confundir un 4 con un
9 será igual de frecuente que confundir un 9 con un 4?

### celda: s16-confusion-texto

La **matriz de confusión** de la unidad 9 tenía dos filas y dos columnas para
contar VP, FP, FN y VN. Aquí hay una fila y una columna por dígito. En ambas
gráficas, las **filas son la clase real** $i$ y las **columnas son la clase
predicha** $j$. La entrada $C_{ij}$ cuenta las imágenes de la clase $i$
que el modelo clasificó como $j$.

La predicción es el `argmax`, el dígito con mayor probabilidad anunciada.
En la unidad 9, la regla binaria aplicaba un umbral a la probabilidad de la
clase positiva. Aquí cada imagen toma la etiqueta de su probabilidad mayor.

- **Izquierda.** La diagonal cuenta los aciertos. Busca los errores fuera
  de la diagonal, incluso en celdas claras. La suma de una fila da el número
  de imágenes de ese dígito. La celda imprime la suma de toda la matriz,
  que es el tamaño de validation.
- **Derecha.** Dividimos cada fila entre su suma y la mostramos en
  porcentaje, con un decimal. Ahora cada fila suma $100\,\%$.
  En la fila del 4 puedes leer qué fracción de los 4 reales terminó en cada
  columna. Esto permite comparar fracciones entre dígitos con distinto
  número de ejemplos. En la diagonal queda el **recall**
  (sensibilidad) de cada dígito, en porcentaje.

### celda: s16-apuesta-respuesta

Compara tu apuesta con la tabla de los pares más confundidos, debajo de las
métricas por dígito. El orden sigue el número de casos. La tabla también
indica qué porcentaje de la clase real representa cada par.

En MNIST suelen confundirse dígitos con trazos parecidos, como 4 y 9 o 3 y 5.
Tu corrida puede mostrar otros pares. Compara las celdas $C_{4,9}$ y
$C_{9,4}$ para revisar tu apuesta sobre la simetría. Cada dirección cuenta
un error distinto y es común que sus frecuencias difieran.

### celda: s16-metricas-texto

En el recuadro de la unidad 9 sobre la matriz de confusión, **precision**
(precisión) es $\mathrm{VP}/(\mathrm{VP}+\mathrm{FP})$ y recall es
$\mathrm{VP}/(\mathrm{VP}+\mathrm{FN})$. Para usar las mismas definiciones
con diez clases, tomamos un dígito $j$ como positivo y al resto como
negativo.

- La **precision** de $j$ es $C_{jj}/\sum_i C_{ij}$. De todo lo que el modelo
  puso en la **columna** $j$, ¿qué fracción era realmente $j$? Una
  precision baja indica que a esa columna llegan muchos ejemplos de otros
  dígitos.
- El **recall** de $j$ es $C_{jj}/\sum_i C_{ji}$. De todos los ejemplos de la
  **fila** $j$, ¿qué fracción encontró el modelo? Un recall bajo indica
  que muchos ejemplos de ese dígito acabaron en otras columnas.

**F1** combina las dos métricas con la media armónica
$F_1=2\,\frac{\mathrm{precision}\cdot\mathrm{recall}}{\mathrm{precision}+\mathrm{recall}}$.
Basta que una de las dos sea baja para que baje F1. La columna `soporte`
cuenta los ejemplos reales de cada dígito.

Mira el punto de partida del eje vertical antes de comparar las barras.
La gráfica recorta el eje cuando los valores lo permiten. El recorte
agranda diferencias pequeñas. Busca si los dígitos con menor precision
son también los de menor recall.

### celda: s16-galeria-texto

La *softmax* da una probabilidad anunciada $\widehat p_j(x)$ por dígito para
la imagen $x$. Las diez probabilidades suman $1$. Llamamos **confianza** a
la mayor, $\max_j \widehat p_j(x)$, que corresponde a la clase predicha.
En §18 veremos cómo se calcula la softmax.

La galería muestra hasta dieciséis errores de validation, de mayor a menor
confianza. Cada imagen lleva su clase real, su predicción y su
confianza. Busca trazos poco habituales o imágenes cuya etiqueta tú también
dudarías en asignar. Es una forma de pensar en el ruido irreducible de la
unidad 9. En una imagen ambigua, los píxeles pueden aportar información
insuficiente para recuperar la etiqueta.

Un error con confianza cercana a $1$ deja muy poca probabilidad para el
dígito real. La *cross-entropy* penaliza mucho ese caso. Así puede subir la
loss de validation con la misma accuracy, como vimos en §6.

### celda: s16-confianza-texto

El histograma de validation muestra la confianza de los aciertos en gris y
la de los errores en rojo. Cada grupo se dibuja como **densidad** y sus
barras tienen área total $1$. Así puedes comparar la forma de los dos
grupos aunque tengan tamaños distintos. La leyenda da los conteos y la
celda imprime las medianas.

Como hay diez probabilidades que suman $1$, la mayor vale al menos $1/10$.
Ahí empieza el primer intervalo del histograma.

Busca si los aciertos se concentran cerca de $1$ y si los errores están
más dispersos. Fíjate también dónde se solapan las barras. La galería
muestra por qué una confianza alta puede acompañar a un error.

### celda: s16-calibracion-texto

En la unidad 9, una regla binaria está **calibrada** si cada probabilidad
anunciada coincide con la frecuencia del evento entre los casos que
reciben ese anuncio. Si anuncia $0.8$, el evento debería ocurrir ocho de
cada diez veces en ese grupo. La **curva de confiabilidad** compara la
probabilidad promedio anunciada con la frecuencia observada.

Aquí el evento es **acertar la clase predicha**. Juntamos las imágenes de
todos los dígitos y las agrupamos por su confianza, la probabilidad de su
clase predicha (*top label*). En la unidad 9 los grupos tenían el mismo
número de casos. Aquí usamos diez intervalos de igual ancho en $[0,1]$,
así que sus tamaños pueden variar.

- **Arriba.** Cada intervalo con casos da un punto. El eje horizontal
  muestra la confianza promedio y el vertical, la fracción de aciertos.
  La diagonal discontinua marca la calibración perfecta. Debajo de ella,
  el modelo anuncia más confianza de la que respaldan sus aciertos.
  Encima de ella, acierta más de lo que anuncia.
- **Abajo.** Las barras dan el número de casos por intervalo en escala
  logarítmica. Ese mismo conteo aparece como `n=` junto a cada punto y
  también en la tabla. Con pocos casos, una sola imagen cambia mucho la
  fracción de aciertos. Empieza por los intervalos con más casos, que
  suelen quedar hacia la derecha.

El checkpoint elegido puede quedar cerca de la diagonal o mostrar
sobreconfianza. Usa la figura para decidir qué ves en esta corrida. La
unidad 9 muestra cómo ajustar una recalibración con datos de validation
y comprobarla en una reserva aparte. Esta celda mide la confiabilidad en
validation.

### celda: s16-test-texto

Con el modelo ya elegido, esta celda obtiene sus predicciones en test una
vez para el reporte final. Mirar test en cada epoch es un error de
protocolo. Las curvas de secciones anteriores lo mostraron como recurso
didáctico para aprender a leerlas. Si esta sección tuvo que entrenar la
línea base de respaldo, `entrenar` también evaluó test en cada epoch, con el
mismo fin didáctico. Las decisiones se tomaron con validation.

La celda imprime la accuracy de validation y la de test. También muestra
las matrices de confusión de test, en conteos y normalizada por fila, y la
tabla de precision, recall y F1 por dígito. Las filas siguen siendo la
clase real y las columnas, la clase predicha. La suma de los conteos es el
número de imágenes de test y aparece impresa.

Las dos accuracies pueden quedar cerca. La de validation puede ser
optimista porque la usamos para elegir entre varias corridas, como en la
unidad 9. Mantén fijo el modelo sea cual sea el resultado. Si eligieras
otra corrida con ese resultado, test pasaría a ser otra validation.

### celda: s16-tabla-texto

La tabla maestra reúne las corridas hasta esta sección en bloques según
la columna `datos`. Lee las comparaciones dentro de cada bloque. Dentro de
un bloque, las filas van ordenadas por presupuesto: `pasos_total` y
`ejemplos_total` dicen cuántas actualizaciones hizo y cuántos ejemplos vio
cada corrida en todo su entrenamiento. Compara con más cuidado corridas
con presupuestos muy distintos.

La tabla indica el número de parámetros y la mejor epoch por loss de
validation. Para esa epoch muestra loss y accuracy de train, validation
y test, y la brecha de accuracy entre train y validation. También
registra la duración y si la corrida divergió. Las columnas de test
quedan como registro didáctico. Validation guio las decisiones.

`CORRIDAS["s16-elegido"]` es la misma corrida ganadora con otro nombre, así
que la tabla la muestra una sola vez, con su ID original (`ELEGIDO_ID`).

### celda: s16-que-viste

**Qué viste**

- La diagonal muestra de un vistazo los aciertos. Fuera de ella puedes
  ver si los errores se concentran en unos cuantos pares con trazos
  parecidos. Lee cada par en su dirección, de real a predicho.
- Precision y recall muestran qué le pasa a cada dígito. Una accuracy
  global alta puede ocultar un dígito difícil de encontrar o uno que el
  modelo predice de más.
- La galería y el histograma permiten ver si hay errores de confianza
  alta. La curva de confiabilidad te dice si la confianza media
  corresponde a la fracción de aciertos. Lee primero los puntos con más casos.
- Exploraste en validation y reservaste la evaluación detallada de test
  para reportar el desempeño del modelo ya elegido.

En §17 veremos si una red convolucional entrenada con los mismos datos
cambia la matriz de confusión. En §18 abriremos la softmax para ver de dónde
salen las probabilidades y la confianza.
