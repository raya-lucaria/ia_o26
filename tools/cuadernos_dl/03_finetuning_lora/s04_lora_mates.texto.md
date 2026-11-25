### celda: s04-intro

## 04 · LoRA y QLoRA en matemáticas

- **Qué vas a ver:** por qué el fine-tuning completo no cabe en una T4, y cómo LoRA y QLoRA mueven muy pocos números.
- Las cifras de esta sección (parámetros, bytes) son cuentas exactas; los números de entrenamiento los imprime el código.

### celda: s04-lora

**LoRA (Low-Rank Adaptation).** Cada capa lineal adaptada cambia así:

$$W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}\,BA,\qquad B\in\mathbb R^{d\times r},\; A\in\mathbb R^{r\times k},\; r\ll\min(d,k).$$

- $W_0\in\mathbb R^{d\times k}$ queda **congelada**; solo se entrenan $A$ y $B$. Escribimos $s=\alpha/r$.
- **Forward sin formar $\Delta W$:** $h=W_0x+s\,B(Ax)$. Primero $Ax\in\mathbb R^{r}$, luego $B(Ax)\in\mathbb R^{d}$.
- **Inicio:** $A$ aleatoria y $B=0$ $\Rightarrow$ $\Delta W=0$: el modelo arranca idéntico al base.
- **Gradientes**, con $g=\partial\mathcal L/\partial h$:

$$\frac{\partial\mathcal L}{\partial B}=s\,g\,(Ax)^\top,\qquad \frac{\partial\mathcal L}{\partial A}=s\,B^\top g\,x^\top.$$

- En el primer backward $B=0$, así que $\partial\mathcal L/\partial A=0$: **solo $B$ se mueve**. (AdamW con weight decay sí mueve $A$ un poco desde el primer paso.)
- **Rango:** $\operatorname{rank}(\Delta W)\le r$, porque $\Delta W$ pasa por un espacio de dimensión $r$.
- **Parámetros:** $dk$ contra $r(d+k)$. Con $d=k=768$ y $r=8$: $589{,}824$ contra $12{,}288$ (≈ 2.1 %).
- **Inferencia:** $W=W_0+\lambda\,s\,BA$ se fusiona en una sola matriz, sin costo extra; $\lambda=0$ recupera el base (§10 mueve $\lambda$).

La celda siguiente construye `LoraLineal` a mano y comprueba el inicio, el primer gradiente, el rango y el conteo.

### celda: s04-memoria

**Memoria del fine-tuning completo con AdamW (fp32)**

| Qué se guarda por parámetro entrenable | Bytes |
|---|---:|
| Peso | 4 |
| Gradiente | 4 |
| Primer momento $m$ | 4 |
| Segundo momento $v$ | 4 |
| **Total** | **16** |

- UNet de SD 1.5, $P\approx 8.6\times10^8$: $16P\approx 13.8$ GB $=12.8$ GiB, **antes** de activaciones y temporales $\Rightarrow$ no cabe en una T4 de 16 GB.
- Con LoRA, los 16 bytes se pagan solo por los $r(d+k)$ de cada capa adaptada; $W_0$ congelada en fp16 cuesta 2 bytes por parámetro.

### celda: s04-qlora

**QLoRA: LoRA sobre un $W_0$ en 4 bits**

- $W_0$ se guarda en **NF4** por bloques de 64 pesos: $W_0\approx c_b\,q$, con $q$ en 16 niveles (cuantiles de $\mathcal N(0,1)$) y $c_b$ la escala del bloque $b$.
- En cada matmul el bloque se **descuantiza a fp16**; los gradientes solo van a $A$ y $B$, que siguen en fp32.

| | $W_0$ por parámetro | Entrena |
|---|---:|---|
| Completo | 16 bytes (fp32 + AdamW) | todo |
| LoRA | 2 bytes (fp16) | $A,B$ |
| QLoRA | ≈ 0.5 byte (NF4) + escalas | $A,B$ |

- En SD solo se cuantizan las capas **lineales**; las convoluciones quedan en fp16.
- QLoRA **ahorra memoria, no tiempo**: descuantizar cuesta, y en una T4 suele ser más lento que LoRA.
- Con QLoRA, $\lambda=0$ recupera el base **cuantizado**, no el original.
