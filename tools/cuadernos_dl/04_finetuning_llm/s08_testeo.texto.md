### celda: s08-intro

## 08 · Testeo, una sola vez

> **Ejecuta la evaluación de test una sola vez**, con la configuración que elegiste en validation. Si cambias el modelo tras ver los resultados de test, necesitarás otro conjunto reservado para evaluar el resultado final.

**Cómo leer las tablas.** Antes de todo, una fila resume los recortes de test, que la sección 05 no mostró para no adelantar el test. La siguiente repite las cuatro métricas de la sección 07 en **test**. La segunda muestra ejemplos con la respuesta esperada, las dos generaciones y sus scores. Compara base y LoRA en el mismo split. Si el resultado difiere de validation, mira cuántos ejemplos entraron en cada medición y qué errores aparecen. Con muestras pequeñas, unas pocas respuestas pueden mover el promedio.

### celda: s08-prompts-explica

**Tus prompts, antes y después.** La tabla recupera las respuestas del base a `prompts.txt` y genera nuevas con LoRA. Estos prompts son ejemplos exploratorios. Úsalos para ver si cambia el formato, si el modelo sigue la instrucción y si el contenido mejora.

### celda: s08-olvido-explica

**Olvido con el adaptador activo**

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Si al activar LoRA se deterioran respuestas en tres tareas generales. | Comparación cualitativa, sin escala numérica. | Mantener el contenido correcto y seguir la instrucción al menos tan bien como el base. | Tres preguntas cubren poco. Una diferencia de estilo puede ser inocua y el base también puede equivocarse. |

**Cómo leer la tabla.** Revisa si se conserva el dato pedido, si la explicación sigue siendo correcta y si se respeta el formato solicitado. Si LoRA impone el formato de tu dataset en otras tareas, anota el fallo de instrucción. Esta prueba compara el comportamiento con el adaptador activo. Al apagarlo, vuelves a usar los pesos base.

### celda: s08-guardar-explica

La celda guarda los pesos del adaptador y su configuración en `mi_lora_texto`. Añade un `LEEME.md` con el modelo base, la configuración, el número de actualizaciones válidas, la ficha del dataset y las métricas de test. Empaqueta la carpeta en `mi_lora_texto.zip` e inicia la descarga en Colab.

Si el navegador bloquea la descarga, abre el panel **📁 Archivos** y elige «Descargar» sobre el zip. Fuera de Colab, el zip queda en la carpeta actual. Para reutilizarlo, descomprime el zip y carga el adaptador con PEFT sobre el mismo modelo base que figura en la ficha.

### celda: s08-receta

Usa esta receta **en validation, antes de abrir test**. Cambia una cosa a la vez y vuelve a ejecutar desde la sección donde se configura.

| Lo que ves | Qué probar |
|---|---|
| Las respuestas apenas cambian y todavía fallan en la tarea. | Revisa si los completions muestran un patrón claro. Prueba más pasos o el modo largo si tienes memoria suficiente. |
| Train baja y validation sube de forma sostenida. | Prueba menos pasos o añade ejemplos variados. |
| Aparecen avisos de gradientes no finitos. | Prueba un learning rate menor y comprueba cuántas actualizaciones se completan. |
| Hay muchos recortes o descartes. | Acorta los ejemplos o aumenta `P["max_len"]` si cabe en memoria. Revisa si se conserva el final de la respuesta. |
| La generación se queda a medias o se repite hasta el límite. | Si falta espacio para terminar, sube `P["max_new"]`. Si hay repeticiones, revisa los finales de tus completions y los recortes de la sección 05. |
| F1 es alto y exact match es bajo. | Lee las respuestas. Distingue cambios de formato aceptables de errores que alteran el sentido. |
| Las respuestas de validation pierden detalles al aplicar LoRA. | Usa la perilla de la sección 06 para explorar una corrección más débil o prueba menos pasos. |
| Se agota la memoria al entrenar. | Reduce `P["batch"]`. Puedes aumentar `P["acum"]` para acercarte al mismo número de ejemplos por actualización. |

### celda: s08-cierre

Conserva el zip junto con la comparación de test. Al presentar el resultado, acompaña las métricas con una respuesta que ilustre qué cambió al activar LoRA y qué le sigue costando al modelo.
