### celda: s08-intro

## 08 · Testeo, una sola vez

> **Ejecuta la evaluación de test una sola vez**, con el adaptador y la configuración ya elegidos en validation. Si usas el resultado de test para ajustar el modelo, necesitarías otro conjunto reservado para medir el resultado final.

La primera tabla repite las cinco métricas con el split de **test** para la loss, el CLIP score, el parecido al estilo y el vecino en train. El olvido se mide con los mismos prompts ajenos y nuevas semillas. Las generaciones con captions de test también usan semillas nuevas. La segunda tabla compara las cifras de LoRA en validation y test, sin el olvido: sus prompts ajenos son los mismos en los dos casos y solo cambian las semillas, así que no dice nada de generalizar a test.

### celda: s08-tabla-leer

**Cómo leer las tablas.** En test, compara base y LoRA en cada fila y mira las referencias. Para estilo, son las imágenes reales de train frente al centroide de test. Para el vecino, son las imágenes reales de test frente a sus vecinos en train. Una brecha entre validation y test puede deberse a diferencias entre sus ejemplos o a la variabilidad de una muestra pequeña. Reporta lo observado junto con las mallas.

| Malla | Cómo leerla |
|---|---|
| **Test** | Cada columna muestra una imagen real y dos generaciones con su caption. Base y LoRA comparten el ruido inicial. |
| **Tus prompts** | Cada prompt tiene una fila «antes», recuperada de la sección 03, y una «después». Compara la misma columna para mantener fija la semilla. |

### celda: s08-olvido-explica

**Cómo leer la malla.** Por cada prompt ajeno hay una fila del base y otra de LoRA. Compara dentro de la misma columna. Distingue entre un cambio de estilo y un caso en que desaparece el objeto o la escena que pediste.

La tabla muestra el CLIP score por prompt. Una diferencia «LoRA − base» negativa indica menor correspondencia según CLIP. Revisa la imagen para interpretar la caída. Esta prueba mide el comportamiento con el adaptador activo. Al apagarlo, vuelves a usar los pesos base.

### celda: s08-guardar-explica

La celda guarda los pesos del adaptador en `mi_lora/pytorch_lora_weights.safetensors`, en formato diffusers. Imprime el tamaño real del archivo junto a la estimación de la sección 04 y los MB del UNet en fp16.

En Colab se inicia la descarga. Si el navegador la bloquea, abre la carpeta `mi_lora` en el panel **📁 Archivos** y selecciona «Descargar» sobre el archivo. Fuera de Colab, la celda imprime la ruta donde quedó. Conserva el adaptador junto con el nombre del modelo base que usaste para entrenarlo.

### celda: s08-receta

Usa esta receta **durante la revisión en validation**, antes de abrir test. Cambia una cosa a la vez y vuelve a ejecutar desde la sección que la configura.

| Lo que ves | Qué probar |
|---|---|
| El estilo apenas cambia y se siguen respetando los captions. | Prueba más pasos. Usa la perilla para ver si al amplificar la corrección aparece el cambio que buscabas. |
| Aparecen artefactos y sube la loss de validation. | Prueba un learning rate menor. |
| El vecino en train queda muy por encima de la referencia y ves ejemplos casi repetidos. | Prueba menos pasos o añade imágenes variadas. |
| Las salidas pierden detalles que pediste en el prompt. | Revisa si los captions de train describen esos detalles. Prueba captions más específicos. |
| Los prompts ajenos pierden el objeto o la escena. | Prueba una escala $\lambda$ menor al generar o menos pasos de entrenamiento. |
| Baja la loss, pero el estilo sigue lejos. | Revisa los recortes, la coherencia del dataset y los captions. Juzga el estilo con las mallas y el parecido al estilo. |
| Se agota la memoria durante el entrenamiento. | Reduce `P["batch"]`. Reinicia el entorno para liberar memoria y vuelve a ejecutar. |
