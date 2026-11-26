### celda: s01-intro

## 01 · Instalar y configurar

Elige `MODO` en la primera línea de código. `LARGO` indica si activaste el modo largo. La celda instala los paquetes que faltan y conserva las versiones ya instaladas.

| Paquete | Para qué lo usamos |
|---|---|
| `diffusers` | Cargar Stable Diffusion y sus schedulers de difusión. |
| `transformers` | Procesar captions y obtener embeddings de CLIP. |
| `peft` | Insertar el adaptador LoRA en el UNet. |
| `accelerate` | Apoyar la carga de los pesos. |

### celda: s01-gpu-explica

- `DEVICE` indica dónde se ejecuta el modelo. Si Colab avisa que estás en CPU, activa la **T4 GPU** y vuelve a ejecutar todo.
- `DTYPE` indica la precisión de los pesos base. En GPU se cargan en fp16, que ocupa la mitad por parámetro que fp32. En CPU se usa fp32.
- `RAPIDO=1` es una prueba de ejecución en CPU con modelos diminutos. Sus imágenes y métricas sirven para revisar el flujo.

### celda: s01-constantes-explica

La celda muestra `P`, la configuración efectiva de tu corrida.

| Claves de `P` | Qué controlan |
|---|---|
| `res`, `max_imagenes` | Resolución y tope de imágenes tomadas del zip. |
| `rango`, `lr` | Rango del adaptador y learning rate. |
| `batch`, `pasos` | Imágenes por batch y actualizaciones programadas. |
| `val_cada`, `n_val_ruido` | Frecuencia de evaluación y cantidad de pares de ruido fijos. |
| `semillas`, `pasos_inferencia` | Semillas de las mallas y pasos para generar cada imagen. |
| `n_gen` | Imágenes generadas por modelo para evaluar los captions de cada split. |

`semilla(s)` fija el azar de Python, NumPy y PyTorch. Al generar, cada pareja de prompt y semilla fija el punto de partida de la comparación entre base y LoRA.
