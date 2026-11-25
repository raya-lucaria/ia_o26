### celda: s05-intro

## 05 · La caja de herramientas

Todas las secciones que siguen usan estas funciones **tal como están**. Así, dos corridas solo difieren en lo que cambias en su `Corrida`.

| Función | Qué hace |
|---|---|
| `Corrida(nombre, …)` | Configura un experimento: método, rango $r$, $\alpha$, módulos, lr, pasos, schedule, semilla, datos |
| `entrenar(c)` | Entrena el adaptador, mide y lo guarda; queda en `CORRIDAS[c.nombre]` |
| `perdida_val(unet, latents)` | MSE del ruido con $(t,\varepsilon)$ fijos |
| `generar(nombre, prompts, semillas, escala)` | Imágenes del base (`None`) o con un adaptador |
| `malla`, `curvas` | Ver imágenes y curvas de loss |
| `delta_w`, `norma_relativa` | Abrir el adaptador: $\Delta W$ y su tamaño frente a $W_0$ |
| `embeddings_clip`, `clip_score` | Medir imágenes con CLIP |
| `tabla`, `liberar`, `completo_en_subproceso` | Resumen, memoria, y el fine-tuning completo que no cabe |

Si `entrenar` ya vio una corrida con el mismo nombre y la misma configuración, y no falló, **la reutiliza** sin reentrenar.

### celda: s05-unet-explica

- **LoRA:** el UNet se carga en fp16 y se congela; solo el adaptador entrena.
- **QLoRA:** las lineales del UNet se cargan en **NF4** (4 bits) con bitsandbytes. La celda cuenta los módulos `Linear4bit` para comprobar que la cuantización ocurrió. Sin GPU, la corrida queda con `error` y el notebook sigue.
- `modulos` es una tupla de nombres: sufijos (`"to_q"`) o nombres completos de capa. Una tupla con **una sola regex** (con `*`, `(` o `|`) se pasa a peft como regex.
- `perdida_val` es la loss de difusión
$$L=\frac{1}{n}\big\lVert \varepsilon-\hat\varepsilon_\theta(x_t,t,c)\big\rVert^2,\qquad x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,$$
con $n$ el número de elementos. Usa siempre los mismos $(t,\varepsilon)$ de `RUIDO_VAL`: la evaluación $i$ toma el latent $i \bmod N$ y el par $i \bmod K$. Por eso dos corridas se miden con la misma vara.

### celda: s05-entrenar-explica

Un paso de entrenamiento:

1. Toma un batch de latents $x_0$, sortea $\varepsilon\sim\mathcal N(0,I)$ y $t$ uniforme, y arma $x_t$.
2. El UNet predice $\hat\varepsilon$; la loss es la MSE.
3. `backward` llega **solo** a $A$ y $B$; AdamW (weight decay $10^{-2}$) los actualiza. El gradiente se recorta a norma 1.

Detalles que importan en la T4:

| Pieza | Por qué |
|---|---|
| UNet fp16, adaptador fp32 (`cast_training_params`) | `GradScaler` no sabe desescalar gradientes fp16 |
| `autocast` + `GradScaler` | fp16 rápido sin que los gradientes chicos se vuelvan cero |
| warmup + cosine (o constante) | el lr sube los primeros pasos (5 % por defecto) y luego baja |
| gradient checkpointing | guarda menos activaciones y las recalcula en el backward: menos memoria, más tiempo |
| paso con inf/NaN | `GradScaler` lo salta y baja la escala; ese intento no cuenta como paso |
| `mem_pico_gb` | memoria pico de la GPU durante la corrida (antes se suelta el pipeline; GB = $10^9$ bytes) |
| `seg_por_paso` | promedio de los pasos 5–15, tras sincronizar la GPU |

Al final guarda solo $A$ y $B$ en `adaptadores/<nombre>.safetensors` y reporta sus MB.

### celda: s05-generar-explica

- `generar` usa **un solo** pipeline base (fp16, `DPMSolverMultistepScheduler`, 20 pasos), en caché, y genera de 2 en 2 semillas. `entrenar` lo suelta; la siguiente llamada lo vuelve a cargar.
- Con un adaptador, lo carga encima del UNet base y lo activa; con `None` los apaga todos.
- `escala` es $\lambda$ en $W = W_0 + \lambda\,\frac{\alpha}{r}BA$: con $\lambda=0$ sale el base, con $\lambda=1$ el adaptado.
- **Un adaptador QLoRA se aplica sobre el UNet fp16**, no sobre el cuantizado en que se entrenó. La diferencia NF4 → fp16 es pequeña, pero existe.
- Misma semilla ⇒ mismo ruido inicial: la diferencia entre dos imágenes con igual semilla es efecto del adaptador.

### celda: s05-ver-explica

- `malla(imagenes, filas, titulo, etiquetas)`: las imágenes en filas (reducidas a 256 px). `etiquetas` puede traer una por imagen o una por fila.
- `curvas(nombres, titulo)`: loss contra paso. **Train** es delgada y tenue (cada paso usa otro $t$, por eso brinca); **validation** es gruesa con puntos.

**Cómo leer las curvas:** compara las gruesas entre corridas; la delgada solo da la tendencia.

### celda: s05-medir-explica

- `delta_w(nombre)`: por cada capa adaptada, $\Delta W=\frac{\alpha}{r}BA$, de forma $[d_{\text{out}}, d_{\text{in}}]$ y rango $\le r$.
- `norma_relativa(nombre)`: $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$ por capa. Dice **cuánto** se movió cada capa respecto a su tamaño.
- `embeddings_clip(imagenes)`: vectores de CLIP con norma 1; el coseno entre dos imágenes es su producto punto.
- `clip_score(imagenes, prompt)`: $100\cdot\cos(\text{imagen},\text{texto})$ promediado. Más alto = la imagen se parece más al texto según CLIP.

### celda: s05-tabla-explica

- `tabla()` junta todas las corridas: lo configurado (método, rango, módulos, lr, pasos) y lo medido (loss de validation final, memoria, s/paso, MB, parámetros entrenables, error).
- `liberar()` suelta el pipeline y CLIP de la memoria; la siguiente llamada a `generar` los vuelve a cargar.

### celda: s05-completo-explica

- El fine-tuning **completo** entrena los ~$8.6\cdot10^8$ pesos del UNet en fp32 con AdamW: pesos + gradientes + dos momentos ≈ 16 bytes por peso, antes de activaciones.
- Se intenta en **otro proceso**: un paso con batch 1, hasta el primer `optimizer.step()`. Si se queda sin memoria (OOM), el proceso muere y la GPU del notebook queda intacta.
- Devuelve `{"ok", "error", "mem_pico_gb"}`. Sin GPU devuelve `error="sin GPU"`.
