### celda: s07-intro

## 07 · Métricas, explicadas

- **Qué vas a ver:** cuatro números para comparar el base contra tu LoRA, cada uno con lo que mide y **cómo te puede engañar**.
- Todo se mide en **validation**. El test espera a §08.
- Un solo número nunca basta: la loss puede bajar sin que las respuestas mejoren, y una respuesta correcta puede tener exact match 0. Por eso van juntos, y al final de la sección hay una tabla de ejemplos para **leer**.

### celda: s07-loss

**Loss y perplexity (solo en el completion)**

$$\mathcal L=\frac{1}{|C|}\sum_{i\in C}-\log p_\theta(x_i\mid x_{<i}),\qquad \text{perplexity}=e^{\mathcal L}.$$

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| qué tan probable le parece al modelo **la respuesta de tu dataset**, token por token | loss $\ge 0$; perplexity $\ge 1$ | más bajo | mide si el modelo *esperaba* esa respuesta, no si la que **genera** es buena; no se compara entre tokenizers distintos ni entre datasets |

- La perplexity se lee como «entre cuántos tokens duda, en promedio». Perplexity 2 ≈ dudar entre dos opciones en cada token.
- Es la única métrica que no necesita generar: es rápida y suave, por eso es la de las curvas.

### celda: s07-em

**Exact match (normalizado)**

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| la respuesta generada es **idéntica** a la esperada, tras pasar a minúsculas y colapsar espacios | 0 a 100 % | más alto | todo o nada: `age >= 20` contra `age > 20` vale 0, igual que una respuesta absurda; y una respuesta **correcta pero escrita distinto** (otro orden, un alias) también vale 0 |

- Tiene sentido cuando las respuestas son **cortas y tienen una forma canónica**, como el SQL del demo.
- Con poemas, resúmenes o explicaciones va a dar ≈ 0 para cualquier modelo: no la uses ahí.

### celda: s07-f1

**Token F1 (estilo SQuAD)**

Con $p$ las palabras de la respuesta generada y $r$ las de la esperada (como bolsas, contando repeticiones):

$$\text{precision}=\frac{|p\cap r|}{|p|},\qquad \text{recall}=\frac{|p\cap r|}{|r|},\qquad F_1=\frac{2\cdot\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}.$$

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| cuántas **palabras** comparten la respuesta generada y la esperada: crédito parcial | 0 a 100 % | más alto | ignora el orden: `SELECT a FROM b` y `FROM a SELECT b` tienen F1 = 100 %; y premia copiar palabras del prompt aunque la respuesta esté mal |

- «Palabras» aquí son los pedazos separados por espacios, tras normalizar. A diferencia de SQuAD, no se quita la puntuación ni los artículos: en SQL, `>` y `>=` no son lo mismo.
- La celda calcula las dos métricas en un ejemplo a mano: una diferencia mínima da exact match 0 y F1 alto.

El **olvido** (¿perdió lo que ya sabía?) no tiene número: se lee en §08, comparando respuestas a preguntas generales.

### celda: s07-lee

**Cómo leer la tabla**

- Compara cada columna fila contra fila: **base** contra **LoRA**. En la loss y la perplexity, LoRA debe salir más baja; en exact match y F1, más alta.
- Si la loss bajó mucho pero el exact match no se movió, lee los ejemplos: a veces el modelo ya contesta casi bien y falla en un detalle (un espacio, una comilla). Para eso está F1.
- **Si el base ya tenía un F1 alto**, el ajuste tenía poco que ganar en esa métrica; mira la loss y el formato.
- Estos números son de **validation**, que usaste para mirar curvas y la perilla. El número honesto es el de test, en §08.
