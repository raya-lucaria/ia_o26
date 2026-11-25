### celda: s01-intro

## 01 · Instalar y preparar

- **Elige el modo en la primera línea de código.** `MODO = "corto"` tarda ≈ 30 min en una T4; `MODO = "largo"` agrega las variantes marcadas ➕ (≈ 75 min).
- La celda instala solo lo que falta (`diffusers`, `peft`, `accelerate`, `bitsandbytes`). No actualiza lo que Colab ya trae.

| Paquete | Para qué |
|---|---|
| `diffusers` | Stable Diffusion: UNet, VAE, schedulers |
| `transformers` | el text encoder de CLIP |
| `peft` | los adapters LoRA |
| `bitsandbytes` | pesos en 4 bits (QLoRA); solo con GPU |

### celda: s01-gpu-explica

- **Necesitas GPU.** Si aparece el aviso, elige T4 GPU en «Cambiar tipo de entorno» y ejecuta todo de nuevo.
- `DTYPE` es fp16 en la GPU: la mitad de memoria que fp32. La T4 no tiene bf16.
- `RAPIDO=1` es solo para la prueba local: usa un Stable Diffusion diminuto en CPU. Sus imágenes son ruido.
- Guarda las versiones que imprime la celda si quieres reproducir una corrida.

### celda: s01-constantes-explica

- **Un solo caption para todas las caras:** `PROMPT = "an anime face"`. Sin nombres de personajes, el modelo aprende un estilo y no identidades.
- `P` junta los tamaños del modo: personajes, caras por personaje, resolución, batch, pasos de entrenamiento y cada cuántos pasos se mide validation.
- `semilla(s)` fija el azar. Misma semilla ⇒ mismo ruido inicial ⇒ imágenes comparables entre métodos.
- Colores: azul es train, naranja es validation y verde es test.
