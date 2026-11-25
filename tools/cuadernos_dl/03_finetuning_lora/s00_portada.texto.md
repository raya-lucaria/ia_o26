### celda: s00-portada

# Notebook 3 · Fine-tuning generativo con LoRA

- Unidad 10 de *deep learning*, clase 3. **Stable Diffusion 1.5 aprende el estilo «cara de anime»** con LoRA.
- Pregunta: **¿cuánto del modelo hay que mover, y con qué precisión, para que aprenda un estilo nuevo?**
- Se compara fine-tuning completo (no cabe en la GPU), LoRA, QLoRA y varios rangos $r$.

**Cómo correrlo**

- En Colab: «Entorno de ejecución → Cambiar tipo de entorno → **T4 GPU** → Guardar», y luego «Ejecutar todo».
- La primera celda de código fija `MODO`:

| `MODO` | Qué corre | Tiempo en una T4 |
|---|---|---|
| `"corto"` (por omisión) | Lo esencial (✔) | ≈ 30 min |
| `"largo"` | Además, las variantes marcadas ➕ | ≈ 75 min |

- En `MODO = "corto"`, una celda ➕ imprime «(solo en MODO largo)» y el notebook sigue.

**Test, una sola vez.** Todas las decisiones se toman con validation. La loss de test se calcula **solo al final (§13), una vez**, con el modelo ya elegido.

**Sobre las caras.** El dataset reúne caras de personajes de anime cuyos derechos son de sus autores. Se usan solo para estudiar el método. **Se entrena con un único prompt genérico, `"an anime face"`, sin nombres de personajes**: el modelo aprende un estilo, no identidades. El notebook guardado muestra caras *generadas* y, como mucho, una tira de 8 caras reales.

**Mapa**

| § | Sección | Modo |
|---|---|---|
| 01 | Instalar y preparar | ✔ |
| 02 | Datos: caras, partición train / validation / test | ✔ |
| 03 | Cómo aprende un modelo de difusión | ✔ |
| 04 | LoRA y QLoRA en matemáticas | ✔ |
| 05 | La caja de herramientas | ✔ |
| 06 | Antes de entrenar: el modelo base | ✔ |
| 07 | Los cuatro casos: completo, LoRA, QLoRA, rangos | ✔ / ➕ rangos |
| 08 | Dónde poner LoRA | ➕ (corto: solo $\lVert\Delta W\rVert$ por capa) |
| 09 | Learning rate y schedule | ➕ |
| 10 | Cuánto cambia el modelo | ✔ |
| 11 | Memorización | ✔ |
| 12 | ¿Olvidó lo que sabía? | ✔ |
| 13 | Cierre: test una vez, tabla final, receta, tarea | ✔ |
