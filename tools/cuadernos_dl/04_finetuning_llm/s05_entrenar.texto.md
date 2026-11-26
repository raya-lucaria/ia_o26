### celda: s05-intro

## 05 · Entrenar

**La loss solo cuenta en el completion.** El prompt le dice al modelo qué responder. Al dejarlo como contexto y asignarle peso cero en la loss, entrenamos al modelo para que produzca la respuesta dada la pregunta. Si también puntuáramos los tokens del prompt, parte de la señal premiaría predecir la pregunta y las marcas de chat. Un prompt largo podría dominar la loss.

| Campo | Qué contiene |
|---|---|
| `ids` | Tokens del prompt formateado, seguidos del completion y su marca de fin. Todo entra al modelo hasta el límite de contexto de esta preparación. |
| `labels` | `-100` para el prefijo de chat y el id de cada token del completion que se conserva. La marca de fin también cuenta si cabe, así el modelo aprende cuándo terminar. |
| `cortado` | Indica si el ejemplo superó `P["max_len"]` y perdió tokens al final. |

La tabla cuenta los recortes por split. Si el prompt llena el espacio y no queda ningún token del completion, el ejemplo se descarta para el cálculo de la loss.

### celda: s05-mascara-explica

**Cómo leer la máscara.** La celda muestra un tramo de un ejemplo de train. En gris están el prompt y las marcas del prefijo, con label `-100`. En verde están los tokens que sirven de objetivo. La tabla amplía la frontera entre ambos.

Un modelo causal usa los logits de la posición anterior para predecir $x_i$. Después de alinear logits y labels, `cross_entropy` ignora el label `-100`. Si $C$ reúne las posiciones del completion que cuentan en el batch, la loss es

$$
\mathcal L=\frac{1}{\lvert C\rvert}\sum_{i\in C}-\log p_\theta(x_i\mid x_{<i}).
$$

El prefijo sigue en $x_{<i}$ y condiciona la respuesta. El promedio da el mismo peso a cada token evaluado, de modo que los completions largos aportan más términos.

### celda: s05-entrenar-explica

1. Toma `P["acum"]` batches de train y rellena a la derecha. La máscara de atención marca el *padding* y su label `-100` lo excluye de la loss.
2. Hace el forward y el backward por batch. Divide cada suma de loss por el total de tokens evaluados de **todos** los batches de ese paso. Así los gradientes acumulados corresponden al promedio por token del paso completo.
3. Aplica *gradient clipping* para limitar la norma del gradiente y actualiza $A$ y $B$. Los pesos base siguen congelados.

| Técnica | Para qué se usa |
|---|---|
| AdamW | Actualiza el adaptador con el learning rate de `P["lr"]`. |
| Warmup y cosine schedule | Sube el learning rate al inicio y luego lo reduce siguiendo una curva coseno. |
| Mixed precision en GPU | Usa `autocast` y `GradScaler` para reducir el riesgo de perder gradientes pequeños. Los pesos de $A$ y $B$ se mantienen en fp32. |
| Gradient checkpointing | Ahorra memoria al recalcular activaciones durante el backward. |
| LoRA dropout | Enmascara al azar parte de la entrada a la rama LoRA durante el entrenamiento. |

`entrenar()` crea un adaptador nuevo cada vez. Si `GradScaler` detecta gradientes no finitos, se salta la actualización y el scheduler no avanza. Si se agotan los intentos, la celda avisa cuántas actualizaciones válidas hizo.

### celda: s05-lee

**Cómo leer la gráfica.** Sigue la tendencia azul de **train**, que registra la loss de los batches de cada paso. En naranja, **validation** vuelve a medir los mismos ejemplos tokenizados. Su punto inicial corresponde a la salida del base, porque $B=0$.

La loss está en *nats* por token. Cuanto menor es, mayor es la media geométrica de las probabilidades asignadas a los tokens esperados, $e^{-\mathcal L}$. Si train baja y validation sube de forma sostenida, puede haber sobreajuste. La mejora puede ser pequeña si el base ya resuelve la tarea o si los ejemplos muestran patrones difíciles de aprender con esta configuración. Contrasta las curvas con las respuestas de la sección 07.
