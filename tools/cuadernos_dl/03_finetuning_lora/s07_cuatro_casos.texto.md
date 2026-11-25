### celda: s07-intro

## 07 · Los cuatro casos

| Caso | Qué se actualiza | Precisión de los pesos base del UNet |
|---|---|---|
| Completo | Todo el UNet (solo se intenta un paso) | fp32 |
| LoRA $r=8$ | $A$ y $B$ de las proyecciones de atención | fp16 en GPU |
| QLoRA $r=8$ | $A$ y $B$ de las mismas proyecciones | NF4 en las capas lineales |
| ➕ LoRA $r=1$ y $r=64$ | $A$ y $B$ con otro rango | fp16 en GPU |

Con AdamW en fp32, cada parámetro entrenable requiere cuatro valores de 4 bytes.

$$
\underbrace{4}_{W}+\underbrace{4}_{\nabla W}
+\underbrace{4}_{m}+\underbrace{4}_{v}=16\ \text{bytes}.
$$

Para el UNet de Stable Diffusion 1.5, la cuenta da aproximadamente 13.8 GB (12.8 GiB) antes de activaciones y temporales. En una T4 (~15 GiB) esperamos OOM. El subproceso registra si logró dar un paso o qué error encontró.

- **Raro posible:** en una GPU grande (L4, A100) el completo puede caber. No contradice la cuenta: 12.8 GiB más activaciones caben en 22 o 40 GiB.
- **Apuesta.** ¿QLoRA dará caras peores que LoRA?

### celda: s07-lora

- LoRA $r=8$ sirve de referencia. Si termina, se muestran los segundos por paso y el tiempo estimado para este modo.
- QLoRA puede ahorrar memoria al guardar los pesos lineales en NF4. Descuantizarlos durante el cálculo puede alargar cada paso. La comparación de tiempos aparece si ambas corridas terminan.
- ➕ Al variar $r$ cambia la capacidad del adaptador y se mantiene $\alpha/r=1$. **Apuesta.** ¿Se verá alguna diferencia entre $r=1$, $r=8$ y $r=64$?

### celda: s07-tabla-idea

- **Cómo leer la tabla.** Una fila por corrida registrada. Compara memoria pico, segundos por paso y tamaño del adaptador guardado. La columna de error explica las corridas fallidas.
- Debajo aparece la fracción de parámetros entrenables respecto al UNet y su costo estimado con 16 bytes por parámetro. En modo `RAPIDO` se usa un modelo diminuto para probar el flujo.

### celda: s07-curvas-idea

- Si $\varepsilon_j$ es el ruido real, $\varepsilon_{\theta,j}(x_t,t,c)$ es la predicción y $D$ es el número de elementos, la loss es la MSE, $\frac{1}{D}\sum_{j=1}^{D}(\varepsilon_j-\varepsilon_{\theta,j}(x_t,t,c))^2$.
- **Cómo leer las curvas.** Un color por corrida exitosa, línea delgada para train y gruesa para validation. En train se sortean $t$ y $\varepsilon$. En validation se reutilizan para facilitar la comparación.

### celda: s07-malla-idea

- **Cómo leer la malla.** El prompt es fijo. Arriba está el modelo base y debajo las corridas exitosas. Cada columna comparte la semilla con s06.
- La fila de QLoRA se genera con el adaptador sobre el UNet **fp16**, no sobre el cuantizado (así lo hace la caja, s05).
- Con pocos pasos puede haber cambios pequeños. El adaptador arranca con $\Delta W=0$.
- Debajo se imprime la diferencia absoluta media de píxeles respecto al base, en una escala de 0 a 255. Úsala para medir cuánto cambió la imagen y mira la malla para describir el cambio.

### celda: s07-que-mirar

**Qué mirar**

| Qué | Qué esperar | Qué puede salir raro, y por qué |
|---|---|---|
| Completo | OOM en una T4 | Cabe en una GPU grande; la cuenta de 16 B/param sigue siendo cierta |
| Memoria pico | QLoRA < LoRA | Ahorra menos de lo que sugieren los 4 bits: las convoluciones y las activaciones no se cuantizan |
| Segundos por paso | QLoRA más lento | Descuantizar $W_0$ en cada matmul cuesta: ahorra memoria, no tiempo |
| Calidad (loss y malla) | QLoRA ≈ LoRA | Las curvas de validation pueden quedar cerca aunque cambien estilo, rasgos o fondo; la malla es el mejor juez |
| Rango ➕ | poca diferencia | $r=1$ ya mueve el estilo; $r=64$ tiene más capacidad, pero con pocos pasos puede no usarla |
| Cambio vs base | caras más anime | Con pocos pasos las imágenes pueden cambiar poco: el adaptador arranca en $\Delta W=0$ |

- Si una corrida dijo «no corrió» (sin GPU, sin `bitsandbytes`), falta en la tabla y en la malla. El resto del notebook usa `lora_r8`.
