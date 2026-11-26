### celda: s05-intro

## 05 · Entrenar

- **Qué vas a ver:** un LoRA con $r=8$ que aprende tu dataset, y sus curvas de loss en train y validation.
- **La idea central: la loss solo cuenta en los tokens del completion.** El modelo lee el prompt completo, pero solo se le corrige lo que **contesta**.
- ¿Por qué? Tu dataset no le pide al modelo *escribir preguntas*, sino *responderlas*. Si la loss incluyera el prompt, gastaría capacidad en imitar tus preguntas (y en ejemplos con prompt largo, eso dominaría la loss).

Primero, cada ejemplo se vuelve tokens:

| Pieza | Qué es |
|---|---|
| `ids` | los tokens de `formatear(prompt)` seguidos de los del completion y su marca de fin de turno |
| `labels` | lo mismo, pero con **−100** en cada token del prompt |
| `cortado` | el ejemplo pasaba de `max_len` y se cortó al final |

- **−100** es la marca que `cross_entropy` ignora (`ignore_index=-100`): esos tokens no suman a la loss ni dan gradiente.
- El completion termina con `<|im_end|>`, y ese token **sí** cuenta: así el modelo aprende **cuándo callarse**.
- La tabla dice cuántos ejemplos se cortaron y cuántos se descartaron (el prompt solo ya llenaba `max_len`, así que no quedaba nada que aprender).

### celda: s05-mascara-explica

**La máscara, a la vista.** La celda pinta un ejemplo de train token por token:

- **gris:** prompt y marcas de la plantilla; label −100; no cuentan.
- **verde:** completion y el `<|im_end|>` final; sí cuentan.

La tabla de abajo muestra la frontera: los últimos tokens del prompt (label −100) y los primeros del completion (label = su propio id).

**El corrimiento.** Un modelo causal, en la posición $i$, predice el token $i+1$. Por eso la loss compara los logits de las posiciones $0\ldots n-2$ con los labels de $1\ldots n-1$:

$$\mathcal L=\frac{1}{|C|}\sum_{i\in C}-\log p_\theta\big(x_{i}\mid x_{<i}\big),$$

con $C$ el conjunto de posiciones del completion (todas las de label $\ne -100$) en el batch. Es la **media por token**, no por ejemplo: una respuesta larga pesa más que una corta.

### celda: s05-entrenar-explica

Un paso de entrenamiento:

1. Toma `acum` batches de `batch` ejemplos y rellena a la derecha (padding con label −100, también ignorado).
2. Forward, loss de cada batch, y `backward`. Los gradientes se **acumulan**; la loss se divide entre los tokens de los `acum` batches, así que el resultado es la media sobre todos.
3. Recorta el gradiente a norma 1 y da **un** paso de AdamW.

| Pieza | Por qué |
|---|---|
| modelo fp16, adaptador fp32 | `GradScaler` no sabe desescalar gradientes fp16; $A$ y $B$ son pocos, así que en fp32 cuestan casi nada |
| `autocast` + `GradScaler` | fp16 rápido sin que los gradientes chicos se vuelvan cero; un paso con inf/NaN se salta y no cuenta |
| AdamW, `lr = 2e-4` | el estándar para LoRA en LLMs: diez veces más que en un fine-tuning completo, porque $\Delta W$ arranca en cero |
| warmup 5 % + cosine | el lr sube los primeros pasos y luego baja suave hasta 0 |
| gradient checkpointing | guarda menos activaciones y las recalcula en el backward: menos memoria, más tiempo |
| `lora_dropout = 0.05` | apaga al azar 5 % de la entrada de LoRA al entrenar; un poco de regularización |

`entrenar()` siempre empieza con un adaptador **nuevo**: si vuelves a correr la celda, no sigue entrenando el anterior.

### celda: s05-lee

**Cómo leer la gráfica**

- **Validation** (naranja, gruesa) es la que importa. Su primer punto, en el paso 0, es el **modelo base**: todo lo que baja de ahí es lo que aprendió.
- **Train** (azul, delgada) brinca porque cada punto es un solo batch. Mira su tendencia, no cada punto.
- La unidad es *nats* por token: $-\log p$ promedio. Una loss de $0.7$ quiere decir que el token correcto recibe, en promedio geométrico, probabilidad $e^{-0.7}\approx 0.5$.
- **Si validation sube mientras train baja**, el modelo empezó a memorizar train: menos `pasos` o más datos (ver la receta de §08).
- **Si casi no baja**, puede que el base ya contestara así, o que la tarea sea muy difícil para un modelo de 0.5B. No siempre sale un efecto grande, y eso también es un resultado.
