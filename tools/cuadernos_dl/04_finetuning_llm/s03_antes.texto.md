### celda: s03-intro

## 03 · Antes: qué contesta el modelo base

Primero genera con Qwen tal como viene. La celda carga el tokenizer y el modelo, imprime cuántos parámetros tiene y congela sus pesos. Las respuestas del base te servirán de referencia para evaluar qué aporta LoRA.

### celda: s03-plantilla-explica

`formatear(prompt)` usa `apply_chat_template` para convertir tu entrada en una conversación. La celda imprime el primer prompt ya formateado. Busca el mensaje de usuario y la marca que abre el turno del asistente. En entrenamiento, el completion ocupa ese turno. Al generar, el modelo lo escribe token a token a partir del mismo prefijo.

### celda: s03-generar-explica

- **Greedy decoding.** En cada paso, `generar` elige el token más probable. La comparación entre base y LoRA usa la misma entrada y prescinde del azar del *sampling*.
- **Padding.** Al generar por batches, el relleno va a la izquierda y queda enmascarado. La celda decodifica solo los tokens nuevos y omite los tokens especiales.
- **Límite.** `P["max_new"]` acota los tokens nuevos por respuesta. Si una frase queda a medias, revisa ese límite.
- **Base y LoRA.** Una vez instalado el adaptador, `lora=False` lo desactiva temporalmente. Puedes comparar las dos versiones con el mismo modelo cargado.

### celda: s03-lee

**Cómo leer las tablas.** La primera reúne los prompts de `prompts.txt` y guarda las respuestas del base para la sección 08. La segunda compara `base` con `esperado` en tres ejemplos de validation. Fíjate por separado en el contenido y en el formato. Una consulta SQL puede resolver bien la pregunta y venir envuelta en una explicación que la referencia no trae.
