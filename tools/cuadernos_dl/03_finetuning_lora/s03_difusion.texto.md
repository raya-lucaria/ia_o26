### celda: s03-intro

## 03 · Cómo aprende un modelo de difusión

Stable Diffusion tiene tres piezas. **Solo el UNet se entrena** en este notebook.

| Pieza | Entrada → salida | En este notebook |
|---|---|---|
| VAE | imagen 512×512×3 ↔ latent 64×64×4 | congelado; se usa una vez |
| Text encoder (CLIP) | prompt → embedding $c$ de 77 tokens | congelado; se usa una vez |
| UNet $\varepsilon_\theta$ | $(x_t, t, c)$ → ruido estimado | **se entrena** (completo, LoRA o QLoRA) |

**Ensuciar** (forward, DDPM). Con $x_0$ el latent de una cara y $\bar\alpha_t$ una constante que baja de ≈ 1 a ≈ 0:

$$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\qquad \varepsilon\sim\mathcal N(0,I),\quad t\sim\mathcal U\{1,\dots,T\},\ T=1000.$$

**Aprender** (ε-prediction). El UNet adivina qué ruido se le sumó:

$$\mathcal L(\theta)=\mathbb E_{x_0,t,\varepsilon}\Big[\big\lVert\varepsilon-\varepsilon_\theta(x_t,t,c)\big\rVert_2^2\Big].$$

- Es un **MSE**: regresión, como en la unidad 9. La MSE promedia sobre todos los elementos del latent.
- Para generar, se parte de ruido puro y se le resta, paso a paso, el ruido que estima el UNet.
- Aquí $x_0$ es el latent **ya multiplicado** por `scaling_factor` (0.18215), para que tenga varianza ≈ 1.

### celda: s03-precomputar-explica

- **Precomputar una vez.** El VAE y el text encoder no se entrenan, así que sus salidas no cambian. Calculamos todos los latents y el embedding del prompt ahora.
- Después los sacamos de la GPU: cada paso de entrenamiento solo corre el UNet. Por eso cada corrida tarda minutos y no horas.
- Un latent tiene 48 veces menos números que la imagen. El UNet trabaja en ese espacio chico.

### celda: s03-ruido-explica

- **La loss de validation necesita ruido fijo.** Si cada medición sorteara $t$ y $\varepsilon$ nuevos, la curva temblaría por puro azar.
- Fijamos $K$ pares $(t,\varepsilon)$ con semilla 0, con $t$ espaciados de 0 a $T-1$. Todas las corridas se miden con los mismos pares.
- Cómo leer la tabla: con $t$ chico casi todo es señal; con $t$ cerca de $T$ casi todo es ruido.

### celda: s03-ver-explica

- Arriba: una cara de train y los 4 canales de su latent. El latent todavía conserva la silueta de la cara.
- Abajo: $x_t$ decodificado para tres valores de $t$. Con $t$ chico se ve la cara; con $t$ grande, casi solo ruido.
- Al final, la celda libera el VAE y el text encoder de la GPU.
