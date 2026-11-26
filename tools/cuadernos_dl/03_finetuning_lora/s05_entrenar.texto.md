### celda: s05-intro

## 05 · Entrenar

**Cómo aprende un modelo de difusión.** Se toma el latent $x_0$ de una imagen de train, se le suma ruido, y el UNet tiene que adivinar **qué ruido** se le sumó:

$$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\qquad \varepsilon\sim\mathcal N(0,I),\quad t\sim\mathcal U\{0,\dots,T-1\},\ T=1000,$$

$$\mathcal L=\big\lVert\varepsilon-\varepsilon_\theta(x_t,t,c)\big\rVert^2\quad\text{(promedio sobre los elementos del latent)}.$$

- $\bar\alpha_t$ baja de ≈ 1 (casi pura señal) a ≈ 0 (casi puro ruido) conforme crece $t$.
- $c$ es el embedding del **caption de esa imagen**. Así el modelo asocia tu estilo con tus textos.
- Es una **MSE**: regresión, como en la unidad 9. Para generar, se parte de ruido puro y se le resta, paso a paso, el ruido que estima el UNet.

**Precomputar una vez.** El VAE y el text encoder no se entrenan, así que sus salidas no cambian. La celda calcula ahora todos los latents y **un embedding por caption distinto** (si todas tus imágenes dicen lo mismo, es uno solo). Cada paso de entrenamiento solo corre el UNet.

### celda: s05-ruido-explica

**Una loss de validation que no tiembla.** Si cada medición sorteara $t$ y $\varepsilon$ nuevos, la curva subiría y bajaría por puro azar. Por eso se fijan $K$ pares $(t,\varepsilon)$ con semilla 0, con los $t$ espaciados de 0 a $T-1$, y **todas** las mediciones usan los mismos.

- La celda imprime la loss de validation del **base**. Es el número a vencer.

### celda: s05-entrenar-explica

**Un paso de entrenamiento**

1. Toma un batch de latents de train, sortea $\varepsilon$ y $t$, y arma $x_t$.
2. El UNet (con el adaptador) predice $\hat\varepsilon$; la loss es la MSE.
3. `backward` llega **solo** a $A$ y $B$: es lo único con `requires_grad`. AdamW los actualiza.

| Pieza | Valor | Por qué |
|---|---|---|
| Optimizador | AdamW, weight decay $10^{-2}$ | el estándar para LoRA |
| Learning rate | `P["lr"]` $=10^{-4}$ | más alto suele romper la imagen; más bajo casi no mueve nada |
| Schedule | warmup (5 % de los pasos) + cosine | sube suave al principio y baja al final |
| Gradiente | recortado a norma 1 | un batch raro no descompone el adaptador |
| Precisión | UNet fp16, $A$ y $B$ fp32, `autocast` + `GradScaler` | rápido en la T4 sin que los gradientes chicos se vuelvan cero |
| Gradient checkpointing | encendido | guarda menos activaciones y las recalcula: menos memoria |

- La celda de abajo mide los primeros 10 pasos e imprime cuánto va a tardar el entrenamiento completo. Es la celda más larga del notebook.
- Si `GradScaler` encuentra inf o NaN, salta ese paso y baja la escala; ese intento no cuenta.

### celda: s05-curvas-explica

**Cómo leer la gráfica.**

- **Train** (azul) brinca muchísimo: cada paso usa otro $t$, y la loss depende sobre todo de $t$. Mira su media móvil, no los puntos.
- **Validation** (naranja) usa siempre los mismos $(t,\varepsilon)$: sus cambios sí son del modelo. El punto gris del paso 0 es el modelo base.
- **Espera cambios chicos.** Una baja pequeña de la loss de validation ya es aprender: buena parte del error de difusión no lo baja ningún modelo, porque el ruido sorteado es azar puro y no hay forma de adivinarlo exacto.
- Si validation **sube** mientras train baja, el adaptador empieza a memorizar train. Con pocos pasos casi nunca pasa; la métrica de memorización de la sección 07 lo mide directo.
- La loss **no es calidad de imagen**. Que baje dice que el modelo predice mejor el ruido de tus imágenes; si las imágenes se ven como tu estilo, lo dicen las mallas y las métricas de CLIP.
