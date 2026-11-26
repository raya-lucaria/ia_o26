### celda: s03-intro

## 03 · Antes: el modelo base

Antes de entrenar, mira qué hace Stable Diffusion **sin** tus datos. Sin este «antes» no hay forma de saber qué cambió.

Stable Diffusion tiene tres piezas, y **solo el UNet recibirá el adaptador**:

| Pieza | Entrada → salida | En este notebook |
|---|---|---|
| VAE | imagen 512 × 512 × 3 ↔ latent 64 × 64 × 4 | congelado |
| Text encoder (CLIP) | caption → embedding $c$ de 77 tokens | congelado |
| UNet $\varepsilon_\theta$ | $(x_t, t, c)$ → ruido estimado | congelado, **más el adaptador LoRA** |

- La celda baja el modelo (≈ 4 GB, uno o dos minutos la primera vez) y cuenta los parámetros de cada pieza.
- El *safety checker* va apagado para ahorrar memoria; tus datos y prompts son tu responsabilidad (lo que no se vale está en la página de la tarea).

### celda: s03-generar-explica

`generar(pares, lora, escala)` produce una imagen por pareja `(prompt, semilla)`:

- `lora=False` es el modelo base; `lora=True` usa el adaptador, que existirá después de la sección 05.
- `escala` es la perilla $\lambda$ de la sección 06.
- **Misma semilla ⇒ mismo ruido inicial.** Si el base y el LoRA usan la misma pareja, la diferencia entre las dos imágenes es efecto del adaptador y no del azar.
- `combinar(prompts, semillas)` arma todas las parejas: cada prompt con cada semilla.

### celda: s03-prompts-explica

**Cómo leer la malla.** Una fila por prompt de tu `prompts.txt`, una columna por semilla. Esta es la referencia «antes»: en la sección 08 se repite con las **mismas** parejas y el adaptador puesto.

- Fíjate en el estilo, los colores, el encuadre y el fondo. Eso es lo que esperas que cambie.

### celda: s03-validation-explica

- Arriba, tres imágenes **reales** de validation; abajo, lo que el base genera con **el mismo caption**.
- La distancia entre las dos filas es lo que el fine-tuning intenta cerrar. Si ya se parecen mucho, el cambio después será sutil, porque el base ya sabía hacer tu estilo.
