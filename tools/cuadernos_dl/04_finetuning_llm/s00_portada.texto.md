### celda: s00-portada

# Notebook 4 · Fine-tuning de un LLM con LoRA: tu dataset

Vas a adaptar **Qwen2.5-Instruct** a tu tarea de texto con **LoRA**. Compararás las respuestas antes y después del fine-tuning, verás qué cambió en el modelo y descargarás tu adaptador.

1. En Colab, abre «Entorno de ejecución → Cambiar tipo de entorno», elige **T4 GPU** y guarda.
2. Arrastra tu `texto.zip` al panel **📁 Archivos** de la izquierda y espera a que termine la carga. Si no tienes un zip, el cuaderno usa un demo de preguntas que se responden con SQL.
3. Selecciona «Entorno de ejecución → **Ejecutar todo**». Si vas a probar ajustes, ejecuta hasta la sección 07 y reserva la 08 para tu configuración final.

Usa `MODO = "corto"` en clase. El modo `"largo"` usa un modelo más grande, ajusta también el MLP y dedica más pasos al entrenamiento. La duración depende del entorno, las descargas y los datos.

| Sección | Qué haces |
|---|---|
| 01 · Configuración | Eliges el modo y compruebas la GPU. |
| 02 · Tu zip | Revisas los datos y los repartes en tres splits. |
| 03 · Antes | Lees las respuestas del modelo base. |
| 04 · LoRA por dentro | Descompones la actualización y cuentas sus parámetros. |
| 05 · Entrenamiento | Ajustas el adaptador con loss solo en el completion. |
| 06 · Inspección | Mides el cambio por capa, ajustas su escala y pruebas el merge. |
| 07 · Métricas | Comparas base y LoRA en **validation**. |
| 08 · Testeo | Evalúas en **test una sola vez** y descargas el adaptador. |
