### celda: s01-intro

## 01 · Instalar y configurar

- **Elige el modo en la primera línea de código.** `MODO = "corto"` tarda ≈ 20–25 min en una T4; `MODO = "largo"` usa un modelo tres veces más grande y entrena más (≈ 45–60 min).
- La celda instala solo lo que falta. No actualiza lo que Colab ya trae.

| Paquete | Para qué |
|---|---|
| `transformers` | el LLM, su tokenizer y su plantilla de chat |
| `peft` | los adaptadores LoRA |
| `accelerate` | carga eficiente del modelo en la GPU |
| `safetensors` | guardar el adaptador en un archivo seguro |

### celda: s01-gpu-explica

- **Necesitas GPU.** Si aparece el aviso, elige T4 GPU en «Cambiar tipo de entorno» y ejecuta todo de nuevo.
- `DTYPE` es **fp16** en la GPU: 2 bytes por peso, la mitad que fp32. La T4 no tiene bf16, el formato con el que se entrenó Qwen; fp16 funciona, pero tiene menos rango, y por eso en §05 hay un `GradScaler`.
- `RAPIDO=1` es solo para la prueba local: usa un Qwen **diminuto** con pesos al azar, en CPU. Sus respuestas son basura; sirve para ver que el código corre.

### celda: s01-constantes-explica

| Modo | Modelo | Parámetros | Capas con LoRA |
|---|---|---:|---|
| corto | `Qwen/Qwen2.5-0.5B-Instruct` | ≈ 0.5 mil millones | atención: `q_proj`, `k_proj`, `v_proj`, `o_proj` |
| largo | `Qwen/Qwen2.5-1.5B-Instruct` | ≈ 1.5 mil millones | atención + MLP: `gate_proj`, `up_proj`, `down_proj` |

- **Instruct** quiere decir que el modelo ya fue ajustado para conversar: le das un mensaje y contesta. Tú vas a ajustarlo **otra vez**, a tu tarea.
- `P` junta los tamaños del modo:
  - `max_len`: tokens máximos por ejemplo; lo que pase de ahí se corta y **no se aprende**.
  - `batch` × `acum`: ejemplos por paso. Se procesan `batch` a la vez y se acumulan `acum` gradientes antes de actualizar: así cabe en la memoria un batch efectivo de 8.
  - `pasos`, `lr`, `val_cada`: cuántas actualizaciones, con qué learning rate y cada cuántas se mide validation.
  - `n_val_loss`, `n_eval`: cuántos ejemplos de validation (y de test) se usan para la loss y para generar.
  - `max_new`: tope de tokens que el modelo puede generar por respuesta.
  - `rango`, `alfa`, `modulos`: la configuración de LoRA ($r=8$, $\alpha=16$), explicada en §04.
- En `MODO = "largo"` el pico de memoria **sí sube**: el modelo de 1.5B ocupa ≈ 3 GB en fp16, contra ≈ 1 GB del de 0.5B. Cabe en la T4.
- Colores: azul es train, naranja es validation y verde es test.
