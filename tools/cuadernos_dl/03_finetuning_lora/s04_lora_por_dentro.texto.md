### celda: s04-intro

## 04 · LoRA por dentro

**La idea.** No movemos los pesos del modelo. A cada capa lineal elegida le sumamos una corrección de **rango bajo**:

$$W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}\,BA,\qquad B\in\mathbb R^{d\times r},\quad A\in\mathbb R^{r\times k},\quad r\ll\min(d,k).$$

| Pieza | Qué es | Se entrena |
|---|---|---|
| $W_0\in\mathbb R^{d\times k}$ | el peso original de la capa | no: congelado |
| $A$, $B$ | las dos matrices delgadas del adaptador | **sí** |
| $r$ | el rango; aquí $r=8$ | — |
| $\alpha$ | una escala; aquí $\alpha=r$, así que $\frac{\alpha}{r}=1$ | — |

- **Empieza sin cambiar nada.** $A$ arranca aleatoria y $B=0$, así que $\Delta W=0$: en el paso 0 el modelo es **exactamente** el base.
- **Rango ≤ $r$.** $\Delta W=BA$ pasa por un espacio de dimensión $r$, así que $\operatorname{rank}(\Delta W)\le r$. Lo verás en la sección 06.
- **Pocos parámetros.** Una capa completa tiene $dk$ números; su adaptador, $r(d+k)$. Con $d=k=768$ y $r=8$: $589{,}824$ contra $12{,}288$, el 2.1 %.
- **Forward barato.** $h=W_0x+\frac{\alpha}{r}B(Ax)$: primero $Ax\in\mathbb R^r$, luego $B(Ax)\in\mathbb R^d$. Nunca se arma la matriz $d\times k$.
- **Perilla.** Al generar se puede usar $W_0+\lambda\,\Delta W$: con $\lambda=0$ vuelve el base, con $\lambda=1$ el adaptado.

**Dónde va en Stable Diffusion.** En las cuatro lineales de cada capa de atención del UNet: `to_q`, `to_k`, `to_v` (las proyecciones de query, key y value) y `to_out.0` (la salida). La celda recorre **tu** UNet, encuentra esas capas y hace la cuenta $dk$ contra $r(d+k)$ con sus tamaños reales.

**Cómo leer la tabla.** Compara la última fila con la segunda: lo que entrenas contra lo que pesa el UNet. Los MB del modelo están en fp16 (2 bytes por número); los del adaptador, en fp32 (4 bytes), como se guarda al final.
