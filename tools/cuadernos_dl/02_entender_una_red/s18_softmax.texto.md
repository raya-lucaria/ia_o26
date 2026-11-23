### celda: s18-intro

## 18 · Softmax y la loss

- La última capa lineal entrega un logit por dígito, $\mathbf z=\mathbf W^{(L)}\mathbf a^{(L-1)}+\mathbf b^{(L)}$.
- **Softmax convierte logits en probabilidades** que suman $1$.

$$\widehat y_c=\frac{e^{z_c}}{\sum_{j=0}^{9}e^{z_j}}.$$

- Sumar la misma constante a todos los logits conserva las probabilidades.
- Usamos el checkpoint de §16 o, si falta, la línea base de §4.

### celda: s18-un-digito-mira

- **El argmax se conserva** entre paneles.
- El naranja marca la clase real de un acierto con confianza entre $0.5$ y $0.9$.
- El cociente $e^{z_c-z_j}$ amplifica las diferencias entre logits.

### celda: s18-apuesta

La temperatura $T>0$ divide los logits antes de aplicar softmax.

$$\widehat y_c(T)=\frac{e^{z_c/T}}{\sum_{j=0}^{9}e^{z_j/T}}.$$

**Apuesta.** Al subir $T$, ¿la confianza y la loss suben, bajan o quedan iguales?
¿Cambian la clase predicha y la accuracy de validation, o se mantienen?

### celda: s18-apuesta-respuesta

- **La predicción y la accuracy se conservan** para $T>0$.
- Al subir $T$, baja la confianza y sube la loss de este acierto.
- Para un error, sigue la probabilidad de la clase real, $\widehat y_y$.

### celda: s18-cross-entropy-texto

- La **cross-entropy** mide $-\log\widehat y_y$ con logaritmo natural y clase real $y$.
- La loss crece sin límite si $\widehat y_y$ tiende a cero.
- Con probabilidades uniformes vale $\log 10\approx2.30$.

$$L(\theta)=\frac{1}{n}\sum_{k=1}^{n}-\log\widehat y_{k,y_k}.$$

Con etiquetas enteras, el promedio es la negative log-likelihood por ejemplo.

### celda: s18-cross-entropy-mira

- **Los errores confiados encarecen la loss**. La curva se dispara al acercarse $\widehat y_y$ a cero.
- El histograma usa conteos logarítmicos. La línea punteada marca $\log 10$.
- La loss puede subir con igual número de aciertos. En §6 aumentaron los errores y su confianza media.

| Cálculo | Qué hace | Qué se ve en la gráfica |
|---|---|---|
| A mano | Promedia $-\log\widehat y_y$ | Línea discontinua del promedio |
| `CrossEntropyLoss` / `evaluar` | Calcula la loss desde logits | Mismo promedio |
| `NLLLoss` | Promedia desde `log_softmax` | Mismo promedio |

### celda: s18-estabilidad-texto

- En `float32`, $e^{-1000}$ cae a cero por underflow y $e^{89}$ desborda a infinito.
- Para logits $(0,-1000)$ y clase real $1$, la loss es $1000+\log(1+e^{-1000})\approx1000$.
- **Apuesta.** ¿Qué filas de la tabla darán resultados finitos y cuáles darán infinitos?

### celda: s18-estabilidad-mira

**Log-sum-exp** resta $m=\max_j z_j$ para que la mayor exponencial valga $1$.

$$\log\widehat y_c=z_c-m-\log\sum_j e^{z_j-m}.$$

| Cálculo | Qué hace | Qué se ve en la tabla |
|---|---|---|
| `softmax` → `log` → `NLLLoss` | Redondea la probabilidad real a cero | Log-probabilidad $-\infty$, loss infinita |
| `log_softmax` → `NLLLoss` | Calcula log-probabilidades con log-sum-exp | Loss finita |
| `CrossEntropyLoss` | Recibe logits y combina ambos pasos | Misma loss finita |

### celda: s18-arquitectura-texto

- A la izquierda, compara el ancho de la entrada, las capas ocultas y la salida.
- El modelo impreso identifica la normalización y la activación de cada capa oculta.
- A la derecha, **los logits se convierten en probabilidades**. El naranja marca la clase real.

### celda: s18-que-viste

**Qué viste**

- Softmax mantuvo la clase ganadora y acentuó su ventaja.
- La loss de validation concentró muchos ejemplos cerca de cero y pocos en la cola.
- Con logits extremos, el cálculo directo dio infinitos o NaN y log-sum-exp dio valores finitos.

| Temperatura | Qué hace | Qué esperar en este acierto | Cómo se ve |
|---|---|---|---|
| $T<1$ | Amplía diferencias entre logits | Más confianza, menor loss | Barra ganadora más alta |
| $T=1$ | Conserva los logits | Probabilidades originales | Panel de referencia |
| $T>1$ | Reduce diferencias entre logits | Menos confianza, mayor loss | Barras más parejas |
