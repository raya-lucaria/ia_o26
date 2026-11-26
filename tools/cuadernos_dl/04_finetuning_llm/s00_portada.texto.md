### celda: s00-portada

# Notebook 4 · Fine-tuning de un LLM con LoRA: tu dataset

- Unidad 10 de *deep learning*, clase 3. Un **LLM chico** (Qwen2.5, 0.5 mil millones de parámetros) aprende **tu** dataset de texto con LoRA.
- Pregunta: **¿qué aprende un modelo de lenguaje de unos cientos de ejemplos, y cómo lo sabes sin engañarte?**
- Es el gemelo del notebook 3: las mismas secciones, pero con texto en vez de imágenes.

**Tres pasos**

1. En Colab: «Entorno de ejecución → Cambiar tipo de entorno → **T4 GPU** → Guardar».
2. Arrastra tu `texto.zip` (el de la tarea) al panel 📁 **Archivos** de la izquierda. Si no tienes zip, no pasa nada: el notebook arma uno de demostración (texto → SQL).
3. «Entorno de ejecución → **Ejecutar todo**».

| `MODO` | Modelo | Qué corre | Tiempo en una T4 |
|---|---|---|---|
| `"corto"` (por omisión) | Qwen2.5-0.5B-Instruct | un LoRA en atención, lo esencial | ≈ 20–25 min |
| `"largo"` | Qwen2.5-1.5B-Instruct | más pasos, más datos, LoRA también en el MLP | ≈ 45–60 min |

**Test, una sola vez.** Todo se decide con *validation*. El *test* se usa **solo al final (§08), una vez**, con el modelo ya entrenado.

**Mapa**

| § | Sección | Qué te llevas |
|---|---|---|
| 01 | Instalar y configurar | `MODO`, GPU, modelo |
| 02 | Tu zip | revisar el formato, ver ejemplos, partir 80/10/10 |
| 03 | Antes | qué contesta el modelo base |
| 04 | LoRA por dentro | las matemáticas y cuántos parámetros entrenas de verdad |
| 05 | Entrenar | la loss solo en el *completion*, curvas train / validation |
| 06 | Ver LoRA | rango de $\Delta W$, qué capas cambiaron, la perilla $\lambda$, *merge* |
| 07 | Métricas | qué mide cada número y cuál es su trampa |
| 08 | Testeo | test una vez, olvido, descargar tu adaptador, qué mover si salió mal |
