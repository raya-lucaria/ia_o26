### celda: s00-portada

# Notebook 3 · Fine-tuning de imágenes con LoRA: tu dataset

Vas a enseñarle a **Stable Diffusion 1.5** el estilo de **tus imágenes** con un adaptador **LoRA**, y a medir con honestidad qué aprendió.

- **Entra:** tu `imagenes.zip`, en el formato de la tarea (`metadata.csv` + `images/` + `prompts.txt` + `LEEME.md`).
- **Sale:** imágenes antes y después, curvas de loss, cinco métricas explicadas, el examen en test y tu adaptador descargado (unos MB).
- **Sin zip también corre:** arma un dataset demo de caras de anime en el mismo formato y lo usa.

**Tres pasos**

1. «Entorno de ejecución → Cambiar tipo de entorno → **T4 GPU** → Guardar».
2. Arrastra tu `imagenes.zip` al panel **📁 Archivos** de la izquierda (detalles en la sección 02).
3. «Entorno de ejecución → **Ejecutar todo**».

**Cuánto tarda.** La primera celda de código fija `MODO`:

| `MODO` | Qué cambia | Tiempo en una T4 |
|---|---|---|
| `"corto"` (por omisión) | lo esencial | ≈ 20–25 min |
| `"largo"` | más pasos, más imágenes y más muestras para las métricas (lo marcado ➕) | ≈ 50–60 min |

**Test, una sola vez.** Todo lo que se mira para decidir usa **validation**. El conjunto de **test** se toca **una vez**, en la sección 08, con el adaptador ya entrenado.

**Mapa**

| § | Sección | Qué haces |
|---|---|---|
| 01 | Instalar y configurar | `MODO`, GPU, semillas, tamaños |
| 02 | Tu zip | subirlo, revisarlo, verlo, partirlo 80 / 10 / 10 |
| 03 | Antes | el modelo base con tus `prompts.txt` |
| 04 | LoRA por dentro | la fórmula y cuántos parámetros entrenas de verdad |
| 05 | Entrenar | un LoRA $r=8$ y sus curvas de train y validation |
| 06 | Ver LoRA | el rango de $\Delta W$, qué capas cambiaron, la perilla $\lambda$ |
| 07 | Métricas | qué mide cada una, su trampa, y su valor en validation |
| 08 | Testeo | test una vez, olvido, descargar el adaptador, qué mover si salió mal |
