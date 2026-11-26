### celda: s06-intro

## 06 · Ver LoRA por dentro

El adaptador ya está entrenado. Antes de medir si sirve, abrimos la caja: en cada capa adaptada armamos $\Delta W=\frac{\alpha}{r}BA$ con sus $A$ y $B$ reales y lo comparamos con $W_0$.

| Qué miramos | Qué esperamos | Por qué es LoRA y no otra cosa |
|---|---|---|
| (a) valores singulares de $\Delta W$ | caen a ≈ 0 después del $r$-ésimo | $\operatorname{rank}(BA)\le r$ |
| (b) $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$ por capa | números chicos, desiguales entre capas | el adaptador corrige, no reemplaza |
| (c) la perilla $\lambda$ | $\lambda=0$ da **exactamente** el base | $W_0$ nunca se tocó |

- $\lVert M\rVert_F=\sqrt{\sum_{ij}M_{ij}^2}$ es la norma de Frobenius: el «tamaño» de una matriz.

### celda: s06-svd-explica

**(a) El rango, a la vista.** La SVD escribe $\Delta W=\sum_i\sigma_i u_i v_i^\top$ con $\sigma_1\ge\sigma_2\ge\dots\ge0$. Una matriz de rango $r$ tiene exactamente $r$ valores singulares distintos de cero.

**Cómo leer la gráfica.** El eje vertical es $\sigma_i/\sigma_1$ en escala logarítmica, para la capa que más se movió (➕ en modo largo, también la que más se movió de cada zona). La línea punteada marca $r$. A la izquierda, $r$ valores de tamaño comparable; a la derecha, un salto de muchos órdenes de magnitud hasta el nivel del redondeo de la computadora.

- Aunque $\Delta W$ es una matriz de cientos × cientos, solo vive en $r$ direcciones. Eso es «rango bajo».

### celda: s06-barras-explica

**(b) Qué capas cambiaron más.**

- `down` son los bloques que bajan de resolución, `mid` el centro del UNet y `up` los que vuelven a subir.
- **Self-attention** (`attn1`) mezcla partes de la imagen entre sí; **cross-attention** (`attn2`) es donde la imagen mira al texto.

**Cómo leer la gráfica.** Una barra por capa adaptada, en el orden del UNet, coloreada por zona. A la derecha, el promedio por zona y tipo. La tabla lista las cinco capas que más se movieron.

- Todos los cocientes son chicos: el adaptador **corrige** a $W_0$, no lo reemplaza.
- Qué zona gana depende de tu dataset. Un estilo de color y textura suele mover más los bloques de alta resolución; no hay garantía, así que mira tu gráfica.

### celda: s06-perilla-explica

**(c) La perilla $\lambda$.** Al generar se usa $W=W_0+\lambda\,\Delta W$ con el mismo prompt y las mismas semillas:

| $\lambda$ | Qué se aplica |
|---|---|
| 0 | nada: el modelo base |
| 0.5 | la mitad de la corrección |
| 1 | la corrección tal como se entrenó |
| 1.5 | una vez y media: el estilo exagerado |

**Cómo leer la malla.** Una fila por $\lambda$, una columna por semilla. Lee cada columna de arriba abajo: es la misma imagen inicial, cada vez con más adaptador.

- La celda compara $\lambda=0$ con el base (adaptador apagado), píxel por píxel. Debe dar 0 o casi: con $\lambda=0$ el término LoRA vale cero.
- Si entre $\lambda=0$ y $\lambda=1$ casi no hay diferencia, el adaptador aprendió poco. $\lambda=1.5$ muestra hacia dónde iba: es un buen diagnóstico antes de entrenar más.
- Un adaptador también se puede **fusionar** en $W_0$ (`fuse_lora` en diffusers): queda una sola matriz por capa y generar cuesta lo mismo que con el base.
