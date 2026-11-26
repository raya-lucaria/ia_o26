### celda: s03-intro

## 03 · Antes: el modelo base

Primero genera con Stable Diffusion tal como viene. Estas imágenes serán tu referencia para juzgar el efecto del adaptador.

| Pieza | Qué hace |
|---|---|
| VAE | Codifica una imagen en un latent $x_0$ y convierte un latent generado en píxeles. |
| Text encoder (CLIP) | Convierte el prompt en los embeddings $c$ que condicionan al UNet. |
| UNet | Estima el ruido a partir del latent ruidoso $x_t$, el paso $t$ y los embeddings $c$. |

La celda carga el pipeline e imprime cuántos parámetros tiene cada pieza. Los pesos base quedan congelados y el adaptador se añadirá al **UNet**. El pipeline se carga con el *safety checker* desactivado.

### celda: s03-generar-explica

`combinar(prompts, semillas)` empareja cada prompt con cada semilla. `generar` produce una imagen por pareja. Usa `lora=False` para el modelo base y, después del entrenamiento, `lora=True` para activar el adaptador. El argumento `escala` controla su intensidad.

Al comparar dos salidas con el mismo prompt y la misma semilla, ambas parten del mismo ruido inicial.

### celda: s03-prompts-explica

**Cómo leer la malla.** Cada fila corresponde a un prompt de `prompts.txt` y cada columna a una semilla. Mira qué elementos del prompt aparecen y cómo se ven el color, la textura y el encuadre. En la sección 08 volverás a ver estas imágenes junto a las de LoRA.

### celda: s03-validation-explica

**Cómo leer la malla.** Arriba tienes ejemplos reales de validation. Debajo de cada uno ves lo que genera el modelo base con su caption. Si el caption es amplio, muchas imágenes distintas pueden corresponderle. Compara rasgos de tema y estilo entre las filas.
