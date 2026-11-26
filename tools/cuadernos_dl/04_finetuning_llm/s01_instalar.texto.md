### celda: s01-intro

## 01 · Instalar y configurar

Elige `MODO` en la primera línea de código. `LARGO` indica si activaste el modo largo. La celda instala los paquetes que faltan y conserva las versiones ya instaladas.

| Paquete | Para qué lo usamos |
|---|---|
| `transformers` | Cargar el LLM, el tokenizer y su plantilla de chat. |
| `peft` | Añadir, activar, desactivar y guardar LoRA. |
| `accelerate` | Apoyar la carga del modelo. |
| `safetensors` | Guardar los pesos del adaptador. |

### celda: s01-gpu-explica

- `DEVICE` indica dónde se ejecuta el modelo. Si Colab avisa que estás en CPU, activa la **T4 GPU** y vuelve a ejecutar todo.
- `DTYPE` indica la precisión de los pesos base. En modo corto, el 0.5B se carga en fp32 (≈ 2 GB), porque Qwen se entrenó en bf16, que la T4 no tiene, y en fp16 puede desbordarse. En modo largo, el 1.5B va en fp16 con `autocast` y `GradScaler` (`AMP = True`), que ocupa la mitad por parámetro. En CPU se usa fp32.
- `RAPIDO=1` fuerza una prueba en CPU con un Qwen diminuto. Sus respuestas y métricas sirven para revisar el flujo.

### celda: s01-constantes-explica

| Modo | Modelo base | Dónde se aplica LoRA |
|---|---|---|
| Corto | `Qwen/Qwen2.5-0.5B-Instruct` | Proyecciones de atención. |
| Largo | `Qwen/Qwen2.5-1.5B-Instruct` | Proyecciones de atención y del MLP. |

Un modelo *Instruct* ya está ajustado para seguir instrucciones. Aquí lo adaptas a la forma de responder que muestran tus ejemplos. El modo largo requiere más memoria. La prueba de merge crea además una copia del modelo.

La celda muestra `P`, la configuración efectiva de tu corrida.

| Claves de `P` | Qué controlan |
|---|---|
| `n_demo` | Tamaño de la muestra del demo. |
| `max_len`, `max_new` | Límite de tokens por ejemplo al preparar la loss y límite de tokens nuevos al generar. `max_new` se fija en la sección 03 con el completion más largo de train y validation. |
| `batch`, `acum` | Ejemplos por batch y batches cuyos gradientes se acumulan antes de actualizar. |
| `pasos`, `lr`, `val_cada` | Actualizaciones programadas, learning rate y frecuencia de evaluación en validation. |
| `n_val_loss`, `n_eval` | Topes de ejemplos por split para medir la loss y evaluar las respuestas generadas. |
| `rango`, `alfa`, `modulos` | Rango, escala y capas del adaptador. |

`semilla(s)` fija el azar de Python, NumPy y PyTorch. En la gráfica de entrenamiento, azul es train y naranja es validation.
