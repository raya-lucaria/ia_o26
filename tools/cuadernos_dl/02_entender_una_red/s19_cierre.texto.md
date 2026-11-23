### celda: s19-intro

## 19 · Cierre

En la unidad 9 comparamos modelos con el error de validation. Aquí hacemos lo mismo con todas las corridas registradas, desde la demo de la caja hasta la CNN de §17. La tabla maestra y la figura ayudan a ver qué cambios movieron el error y cuáles dieron resultados parecidos. El cierre solo resume lo que hay en `CORRIDAS`. Si saltaste secciones, verás solo las corridas registradas. Si el registro está vacío, la celda te avisa.

### celda: s19-tabla-texto

La tabla se divide por `datos`. Compara filas dentro del mismo grupo. Hay corridas con todo train limpio, con subconjuntos y con etiquetas alteradas. Al alterar etiquetas, la red recibe ejemplos con respuestas incorrectas. Ese ruido recuerda al ruido irreducible de la unidad 9 y cambia las condiciones del ajuste.

- `parametros` cuenta los pesos y sesgos entrenables. `presupuesto` es lo que pidió la `Config` (epochs, o un tope de pasos) y `pasos` las actualizaciones que dio de verdad. `mejor_epoch` indica dónde fue menor la loss de validation en esa corrida.
- Las columnas `loss_` y `acc_` muestran la loss y la accuracy de train, validation y test en esa epoch. Dentro de cada grupo, la tabla ordena las filas de mayor a menor `acc_validation`. Test aparece solo para reportar.
- `brecha` es la accuracy de train menos la de validation. `segundos` mide el tiempo acumulado al final de la corrida. `divergio` indica si apareció una loss no finita durante el entrenamiento.

Incluso dentro del mismo grupo, el presupuesto de entrenamiento puede variar. Por ejemplo, cambiar el tamaño del batch en §7 cambia cuántas actualizaciones caben en una epoch. Lee el orden de la tabla junto con las columnas `presupuesto` y `pasos`.

### celda: s19-figura-texto

Cada grupo de datos ocupa una fila de paneles. A la izquierda, cada barra horizontal muestra la accuracy de validation en la mejor epoch de una corrida. La accuracy más alta queda arriba. El color indica la sección de origen, según la leyenda. Las corridas que divergieron llevan un rayado en esa barra y la marca «✕ divergió» junto al nombre.

El eje de accuracy puede empezar por encima de cero. El título indica el inicio del eje. Un eje recortado hace más visibles las diferencias pequeñas y puede hacer que parezcan grandes. Para medirlas, lee los valores junto a las barras. Si una accuracy cae por debajo del inicio del eje, el valor lleva la marca «fuera del eje».

A la derecha está la brecha de cada corrida, $a_{\text{train}} - a_{\text{validation}}$, donde $a$ es la accuracy en esa misma epoch. Una brecha positiva indica que la red acierta más en train y puede señalar overfitting. Cerca de cero, esta medida da poca señal de overfitting. Con etiquetas alteradas, la brecha puede ser negativa. Ahí train se evalúa con las etiquetas alteradas y validation con etiquetas limpias.

### celda: s19-figura-mira

**Qué mirar.** ¿Se amontonan las barras cerca del tope? Una vez que el entrenamiento funciona, varios cambios pueden dar casi la misma accuracy. Entre las barras de abajo, busca corridas con un learning rate que dejó el ajuste estancado o redes con un cuello muy angosto. Las redes con activaciones que saturan también pueden quedar abajo si tuvieron pocos pasos para aprender. Ubica la CNN de §17 y compárala con los MLP de su mismo grupo de datos.

En el grupo con etiquetas alteradas, busca una brecha más visible. Puede variar con la semilla y con el presupuesto de entrenamiento, igual que las posiciones en la figura. Diferencias pequeñas pueden deberse al azar de una corrida.

### celda: s19-movio-texto

**Qué movió de verdad el error y qué no movió nada.** Una comparación junta corridas de la misma sección, con los mismos datos y el mismo presupuesto pedido. Entre las que terminaron sin divergir, la gráfica calcula el rango de accuracy de validation, $a_{\max} - a_{\min}$, la mayor accuracy menos la menor. Se agregan dos comparaciones que cruzan secciones, si ambas corridas existen: dropout de §15 contra su control de §10, y la CNN de §17 contra el MLP elegido en §16. Las barras se ordenan de menor a mayor rango. Si hubo divergencias, la anotación «(+… divergieron)» cuenta las corridas cuyo entrenamiento se interrumpió por una loss no finita.

Un rango pequeño indica que los valores probados dieron errores parecidos. Uno grande indica que el error varió más entre las corridas. El rango depende de los valores probados y del presupuesto. Solo aparece una barra cuando hay al menos dos corridas comparables. Si todas menos una divergieron, la barra queda en cero y la anotación lo dice.

### celda: s19-que-viste

**Qué viste.** Estas son tendencias para buscar. Pueden aparecer solo algunas en tu ejecución.

- Dar con un learning rate que permita avanzar suele cambiar más el error que cambiar de optimizer o retocar la forma de la red. Normalizar la entrada cambia qué learning rate funciona (§5).
- Cuando la red ya tiene capacidad suficiente, añadir parámetros puede aportar poco (§11). Con tamaños similares, varias formas pueden empatar. Un cuello muy angosto sí puede dificultar la tarea (§12).
- En redes profundas, activaciones que saturan, como la sigmoide, pueden dejar gradientes pequeños y hacer lento el aprendizaje. Batch normalization puede facilitar el entrenamiento de una red profunda (§13–15).
- Con etiquetas alteradas, busca el overfitting en las curvas. La loss de train puede seguir bajando mientras la de validation sube. Early stopping conserva el checkpoint elegido con la loss de validation (§10).
- La CNN usa la estructura espacial de la imagen. Su ventaja, si aparece, se ve al compararla con los MLP del mismo grupo (§17).

Muchas decisiones de diseño pueden acabar en empate. Eso también es un resultado.

### celda: s19-protocolo

**Cómo separar train, validation y test.**

1. **Train** ajusta los pesos y sesgos.
2. **Validation** guía todas las decisiones de selección. Usa su loss para elegir la mejor epoch y aplicar early stopping. Usa validation también para comparar learning rates, optimizers, tamaños y formas de red, y para elegir el modelo final. En este notebook, `mejor_epoch` se elige por loss de validation. La selección de `s16-elegido` y el orden de la tabla usan accuracy de validation.
3. **Test** se mira una sola vez, al final, con el modelo ya elegido. Sirve para reportar una estimación del error en datos nuevos.

Aquí mostramos test en cada epoch solo para aprender a leer las tres curvas. Ninguna decisión del notebook usó test. En un proyecto real, mirar test en cada epoch está mal. Si consultas test repetidamente y eliges lo que mejor se ve, conviertes test en otra validation. Como vimos con el conjunto de prueba en la unidad 9, su error puede quedar sesgado a la baja.

La última celda imprime el ID de cada corrida, una vez, y al final cuántos experimentos distintos hay. `s16-elegido` no cuenta aparte: §16 guarda el MLP elegido con un segundo nombre, que apunta a la misma corrida. La celda lista ese alias por separado.
