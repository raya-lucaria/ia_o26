### celda: s01-intro

## 01 · Instalar y configurar

- **Elige el modo en la primera línea de código.** `MODO = "corto"` es el de clase; `MODO = "largo"` entrena más pasos y mide con más muestras.
- La celda instala solo lo que falta. No actualiza lo que Colab ya trae.

| Paquete | Para qué |
|---|---|
| `diffusers` | Stable Diffusion: UNet, VAE, schedulers |
| `transformers` | el text encoder y el modelo CLIP que mide las imágenes |
| `peft` | el adaptador LoRA |
| `accelerate` | carga eficiente de los pesos |

### celda: s01-gpu-explica

- **Necesitas GPU.** Si aparece el aviso, elige T4 GPU en «Cambiar tipo de entorno» y ejecuta todo de nuevo.
- `DTYPE` es fp16 en la GPU: la mitad de memoria que fp32. La T4 no tiene bf16.
- `RAPIDO=1` existe solo para probar el notebook en una computadora sin GPU: usa modelos diminutos y sus imágenes son ruido. En Colab nunca está activo.

### celda: s01-constantes-explica

`P` junta todos los tamaños del modo. Los que más importan:

| Clave | Qué es |
|---|---|
| `res` | lado de las imágenes en px (SD 1.5 trabaja a 512) |
| `max_imagenes` | si tu zip trae más, se toma una muestra con semilla 0 |
| `rango`, `lr` | el rango $r$ del adaptador y el learning rate de AdamW |
| `batch`, `pasos` | imágenes por paso y número de pasos de entrenamiento |
| `val_cada` | cada cuántos pasos se mide la loss de validation |
| `semillas` | las semillas de las mallas: misma semilla ⇒ mismo ruido inicial |
| `n_gen` | cuántas imágenes se generan por conjunto para las métricas |

- `semilla(s)` fija el azar. Con la misma semilla, el modelo base y el adaptado parten del **mismo ruido**: la diferencia entre sus imágenes es efecto del adaptador.
- Colores fijos: azul train, naranja validation, verde test; gris el modelo base y morado el LoRA.
