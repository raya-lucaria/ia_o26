### celda: s07-intro

## 07 · Métricas, explicadas

Compara **base y LoRA en validation**. La loss y la perplexity evalúan los completions de referencia que quedaron tras tokenizar y recortar. Exact match y token F1 comparan las respuestas generadas con las referencias completas. La celda imprime cuántos ejemplos usa en cada cálculo.

### celda: s07-loss

**Loss**

En cada posición evaluada, el modelo recibe el prompt y los tokens **de referencia** anteriores (*teacher forcing*). La loss $\mathcal L$ de la sección 05 promedia $-\log p$ para los tokens esperados.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Sorpresa media, en *nats* por token del completion, ante la respuesta esperada. | $[0,\infty)$ | Menor loss sobre los mismos tokens. | Al generar, el modelo sigue sus propios tokens. Una loss baja puede convivir con respuestas que se desvían pronto. |

Si el recorte deja el split sin tokens evaluables, la función devuelve loss cero por cómo protege la división. Revisa el conteo antes de interpretar esa cifra.

**Perplexity**

La perplexity es $e^{\mathcal L}$, el inverso de la media geométrica de las probabilidades asignadas a los tokens esperados.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| La misma sorpresa expresada como número efectivo de opciones equiprobables por token. | $[1,\infty)$ en la definición. | Menor perplexity sobre los mismos tokens. | Ordena los modelos igual que la loss. Depende del tokenizer y de los datos. En cifras extremas la tabla limita el exponente para evitar desbordamientos. |

### celda: s07-em

**Exact match normalizado**

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Porcentaje de respuestas que coinciden por completo tras pasar a minúsculas y colapsar espacios. | De 0 a 100 %. | Un porcentaje alto cuando la tarea pide una forma de respuesta bien definida. | Una consulta equivalente con otro alias o un bloque de código extra puede valer cero. La puntuación y el orden siguen contando. |

### celda: s07-f1

**Token F1 (estilo SQuAD)**

Aquí los tokens son fragmentos separados por espacios tras la misma normalización. Artículos y puntuación se conservan. Sean $n_p$ y $n_r$ las longitudes de la predicción y la referencia, y $m$ el número de tokens que comparten contando repeticiones. Con ambas respuestas no vacías, la *precision* es $m/n_p$ y el *recall* es $m/n_r$. El F1 combina las dos en $F_1=2m/(n_p+n_r)$. Si una respuesta está vacía, el código devuelve cero. Si ambas lo están, devuelve uno.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Solapamiento de tokens, con crédito parcial. Baja si sobran tokens o faltan tokens esperados. | De 0 a 100 % en la tabla resumen. | Un F1 alto cuando importa recuperar el contenido de la referencia. | Ignora el orden. Una respuesta puede tener casi todos los tokens correctos y fallar en un operador que cambia el sentido. |

La celda ilustra la diferencia con `>` y `>=` en SQL. Exact match vale cero, mientras F1 da crédito por los tokens compartidos.

### celda: s07-lee

**Cómo leer las tablas.** Compara base y LoRA por columna. Las cuatro métricas usan las mismas filas; la línea de cobertura dice en cuántas entró la loss y si alguna referencia es más larga que `max_new`, en cuyo caso su exact match es 0 por construcción. Una loss `NaN` significa que ninguna fila conservó su completion. Busca menos loss y perplexity y más exact match y F1, según lo que importe en tu tarea. Abajo, cada fila muestra el prompt, la referencia y ambas respuestas. Los scores por ejemplo van de cero a uno. Si F1 sube y exact match se queda igual, busca qué conserva la respuesta y qué diferencias aún importan. Si la salida se ve cortada en la tabla, recuerda que los scores usan el texto completo que devolvió el generador.
