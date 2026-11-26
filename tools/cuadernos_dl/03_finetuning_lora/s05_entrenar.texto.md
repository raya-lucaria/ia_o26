### celda: s05-intro

## 05 · Entrenar

El UNet aprende a estimar el ruido añadido a una imagen. El scheduler mezcla su latent limpio $x_0$ con ruido gaussiano $\varepsilon\sim\mathcal N(0,I)$ en un paso $t$ elegido al azar.

$$
x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon.
$$

$\bar\alpha_t$ fija cuánto queda de la señal original. Conforme aumenta $t$, pesa menos la señal y más el ruido. El UNet recibe $x_t$, $t$ y el embedding $c$ del caption, y predice $\hat\varepsilon=\varepsilon_\theta(x_t,t,c)$. La loss es el error cuadrático medio (MSE) entre $\hat\varepsilon$ y el ruido aplicado, promediado sobre todos los elementos del batch.

La celda precalcula los latents y un embedding por caption distinto porque el VAE y el text encoder están congelados. Guarda los latents en CPU y avisa si algún caption se trunca.

### celda: s05-ruido-explica

Para comparar la loss en distintos momentos, la celda fija pares $(t,\varepsilon)$. Espacia los $t$ a lo largo del scheduler y genera el ruido con semilla fija. Cada medición vuelve a emparejar las imágenes del split con los mismos pares en el mismo orden. La primera cifra es la loss de validation del modelo base.

### celda: s05-entrenar-explica

1. Toma un batch de latents de **train** con sus captions y sortea el ruido y el paso $t$.
2. Forma $x_t$, predice el ruido y calcula la MSE.
3. Calcula los gradientes de $A$ y $B$ y actualiza esas matrices. Los pesos base siguen congelados.

| Técnica | Para qué se usa |
|---|---|
| AdamW | Actualiza los parámetros entrenables con el learning rate de `P["lr"]` y aplica *weight decay*. |
| Warmup y cosine schedule | Sube el learning rate al inicio y luego lo reduce siguiendo una curva coseno. |
| Gradient clipping | Limita la norma de los gradientes antes de actualizar. |
| Mixed precision en GPU | Usa `autocast` para el forward y `GradScaler` para proteger gradientes pequeños. $A$ y $B$ se mantienen en fp32. |
| Gradient checkpointing | Ahorra memoria al recalcular activaciones durante el backward. |

La celda imprime la configuración, estima el tiempo a partir de los primeros pasos y reporta cuántas actualizaciones completó. Si `GradScaler` detecta gradientes no finitos, omite la actualización.

### celda: s05-curvas-explica

**Cómo leer la gráfica.**

- **Train, en azul.** Cada batch trae nuevas imágenes o ruido. Sigue la media móvil para ver la tendencia.
- **Validation, en naranja.** Los pares de ruido son fijos. Lee el cambio frente al punto gris del paso inicial, cuando $B=0$ y el modelo equivale al base.
- Una pérdida de validation menor indica mejor predicción del ruido en ese split. La mejora puede ser pequeña si el modelo base ya predice bien. Si train baja y validation sube de forma sostenida, puede haber sobreajuste. Contrasta la tendencia con las mallas y las métricas de la sección 07.
