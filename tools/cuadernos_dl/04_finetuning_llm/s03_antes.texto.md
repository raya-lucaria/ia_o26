### celda: s03-intro

## 03 · Antes: qué contesta el modelo base

- **Qué vas a ver:** las respuestas del modelo **sin entrenar** a tus prompts de prueba y a tres ejemplos de validation.
- Es la fila de referencia: en §06 y §08 vuelven estos mismos prompts, ya con LoRA.
- La celda descarga el modelo (≈ 1 GB en modo corto, ≈ 3 GB en largo) y lo congela: ningún peso de $W_0$ se va a mover.

### celda: s03-plantilla-explica

**La plantilla de chat.** Un modelo *Instruct* no ve tu prompt tal cual: lo ve dentro de una conversación con marcas especiales.

- `<|im_start|>system`: instrucciones generales (Qwen pone una por omisión).
- `<|im_start|>user`: lo que escribe la persona; aquí va **tu `prompt`**.
- `<|im_start|>assistant`: aquí empieza a contestar el modelo; aquí va **tu `completion`**.
- `<|im_end|>`: fin de un turno. Cuando el modelo lo genera, deja de hablar.

- `formatear(prompt)` arma ese texto con `apply_chat_template`, la plantilla que trae el propio tokenizer.
- Se usa **la misma** al entrenar y al generar. Si cambiaras la plantilla entre una cosa y otra, el modelo vería un formato que nunca practicó.

### celda: s03-generar-explica

- `generar(prompts, lora)` contesta con **greedy decoding**: en cada paso toma el token más probable. Sin azar, así que la misma entrada da siempre la misma salida y las comparaciones son justas. Qwen viene configurado para muestrear al azar (*temperature*, *top-p*); la celda de carga lo apaga.
- `max_new` (por omisión `P["max_new"]`) acota cuántos tokens puede escribir. Si la respuesta se ve cortada a media frase, es ese tope, no el modelo.
- Genera en lotes de 16; el relleno (*padding*) va a la **izquierda** para que todas las respuestas empiecen justo después de su prompt.
- `lora=False` apaga el adaptador: con **un solo modelo en la memoria** se obtienen el base y el ajustado.

### celda: s03-lee

**Cómo leer las tablas**

- Con el demo SQL, el base suele **saber** SQL, pero contesta a su manera: con un bloque de código, una explicación, a veces otra sintaxis. Lo correcto no es lo mismo que lo que tu dataset pide.
- Compara la columna `base` con `esperado`: la diferencia de **formato** es lo primero que aprende un fine-tuning.
- Con `RAPIDO=1` el modelo es diminuto y aleatorio: sus respuestas no significan nada.
