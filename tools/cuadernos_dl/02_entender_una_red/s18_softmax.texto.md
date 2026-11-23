### celda: s18-intro

## 18 · Softmax y la loss

La última capa lineal entrega un logit por dígito, $\mathbf z=\mathbf W^{(L)}\mathbf a^{(L-1)}+\mathbf b^{(L)}$.
**Softmax convierte logits en probabilidades** que suman $1$.

$$\widehat y_c=\frac{e^{z_c}}{\sum_{j=0}^{9}e^{z_j}}.$$

Sumar la misma constante a todos los logits deja intactas las probabilidades.
Usamos el checkpoint elegido en §16. Si falta, recurrimos a la línea base de §4.

### celda: s18-un-digito-mira

**El argmax se conserva**. La barra más alta en cada panel corresponde a la misma clase.
El naranja marca la clase real. El ejemplo busca un acierto con confianza entre $0.5$ y $0.9$.
El cociente entre probabilidades es $e^{z_c-z_j}$. Una diferencia pequeña entre logits puede producir probabilidades muy distintas.

### celda: s18-apuesta

La temperatura $T>0$ divide los logits antes de aplicar softmax. Con $T=1$ recuperas las probabilidades originales.

$$\widehat y_c(T)=\frac{e^{z_c/T}}{\sum_{j=0}^{9}e^{z_j/T}}.$$

**Apuesta.** Al subir $T$, ¿la confianza y la loss suben, bajan o quedan iguales?
¿Cambian la clase predicha y la accuracy de validation, o se mantienen?

### celda: s18-apuesta-respuesta

**La predicción se conserva** al dividir por $T>0$. La accuracy queda igual.
Al subir $T$, baja la confianza y sube la loss de este acierto. Si hay error, lee $\widehat y_y$.
Con igual número de aciertos, la loss puede subir. En §6 aumentaron tanto los errores como su confianza media.

### celda: s18-cross-entropy-texto

La **cross-entropy** mide $-\log\widehat y_y$, con logaritmo natural y $y$ como clase verdadera.
La loss crece sin límite cuando $\widehat y_y$ se acerca a cero. Con probabilidades uniformes vale $\log 10\approx2.30$.

$$L(\theta)=\frac{1}{n}\sum_{k=1}^{n}-\log\widehat y_{k,y_k}.$$

Con etiquetas enteras, este promedio es la negative log-likelihood por ejemplo.
`CrossEntropyLoss` recibe logits y combina `log_softmax` con `NLLLoss`.

### celda: s18-cross-entropy-mira

**La loss penaliza mucho los errores confiados**. A la izquierda, la loss se dispara cuando $\widehat y_y$ cae hacia cero.
A la derecha, la mayoría de ejemplos tiene poca loss y unos pocos forman una cola de loss alta.
El eje de conteos es logarítmico. La línea punteada señala la referencia $\log 10$.
La loss puede subir con igual número de aciertos. En §6 aumentaron tanto los errores como su confianza media.

### celda: s18-estabilidad-texto

En `float32`, $e^{-1000}$ se redondea a cero por underflow y $e^{89}$ desborda a infinito por overflow.
Para logits $(0,-1000)$ y clase real $1$, la loss exacta es $1000+\log(1+e^{-1000})\approx1000$.
**Apuesta.** ¿Qué filas de la tabla darán resultados finitos y cuáles darán infinitos?

### celda: s18-estabilidad-mira

Softmax por separado redondeó la probabilidad real a cero. Su logaritmo dio $-\infty$.
**Log-sum-exp** resta $m=\max_j z_j$ antes de calcular las exponenciales.

$$\log\widehat y_c=z_c-m-\log\sum_j e^{z_j-m}.$$

La exponencial mayor vale $1$, así que la suma es finita y vale al menos $1$ para logits finitos.
Usa `log_softmax` para log-probabilidades y pasa los logits directamente a `CrossEntropyLoss` para la loss.

### celda: s18-arquitectura-texto

A la izquierda ves el ancho de la entrada, las capas ocultas y la salida.
En el modelo impreso puedes localizar la normalización y la activación de cada capa oculta.
A la derecha, **los logits se convierten en probabilidades**. El naranja marca la clase real.

### celda: s18-que-viste

**Qué viste**

- Softmax conservó el orden de los logits. La barra ganadora destacó más en probabilidades.
- Al subir la temperatura, la distribución se aplanó y la loss del acierto subió con la misma predicción.
- La loss de validation se concentró cerca de cero, con una cola de ejemplos costosos.
- El cálculo directo produjo infinitos o NaN con logits extremos. Log-sum-exp dio resultados finitos en ambos ejemplos.
