### celda: s00-portada

# Notebook 3 · Fine-tuning de imágenes con LoRA: tu dataset

Vas a adaptar **Stable Diffusion 1.5** a tus imágenes con **LoRA**. Compararás el modelo base con el adaptado, verás qué cambió en sus capas y descargarás tu adaptador.

1. En Colab, abre «Entorno de ejecución → Cambiar tipo de entorno», elige **T4 GPU** y guarda.
2. Arrastra tu `imagenes.zip` al panel **📁 Archivos** de la izquierda y espera a que termine la carga.
3. Selecciona «Entorno de ejecución → **Ejecutar todo**». Puedes seguir el mismo recorrido sin subir un zip, con el demo de caras de anime.

Elige `MODO = "corto"` para clase. En una T4, reserva unos 20–25 minutos para la ejecución completa, incluidas las descargas. El tiempo es orientativo. El modo `"largo"` permite usar más datos y dedica más pasos al entrenamiento y más muestras a la evaluación.

| Sección | Qué haces |
|---|---|
| 01 · Configuración | Eliges el modo y compruebas la GPU. |
| 02 · Tu zip | Revisas y preparas los datos. |
| 03 · Antes | Generas imágenes con el modelo base. |
| 04 · LoRA por dentro | Descompones la actualización y cuentas sus parámetros. |
| 05 · Entrenamiento | Ajustas el adaptador y lees las curvas de loss. |
| 06 · Inspección | Ves el rango de la actualización, las capas y el efecto de cambiar su escala. |
| 07 · Métricas | Comparas base y LoRA en **validation**. |
| 08 · Testeo | Evalúas en **test una sola vez**, al final, y guardas el adaptador. |
