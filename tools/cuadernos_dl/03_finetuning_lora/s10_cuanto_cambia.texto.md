### celda: s10-intro

## 10 · Cuánto cambia el modelo

- $\Delta W=\frac{\alpha}{r}BA$ tiene rango a lo sumo $r$ porque $A$ tiene $r$ filas y $B$, $r$ columnas.
- La SVD escribe $\Delta W=\sum_i\sigma_i u_i v_i^\top$ con $\sigma_1\ge\sigma_2\ge\dots\ge0$. La **energía** de la dirección $i$ es $\sigma_i^2$; las primeras $k$ direcciones concentran la fracción $E_k=\frac{\sum_{i=1}^k\sigma_i^2}{\lVert\Delta W\rVert_F^2}$, donde $\lVert\Delta W\rVert_F^2=\sum_i\sigma_i^2$.
- **Rango efectivo al 90 %** es el menor $k$ con $E_k\ge0.9$.

**Cómo leer la gráfica.** Cada curva muestra $\sigma_i/\sigma_1$ para una capa, en escala logarítmica. La línea punteada marca $r$. Para $i>r$, los valores caen al nivel del redondeo o al mínimo del eje. En modo largo se repite el análisis con `lora_r64`.

### celda: s10-perilla

En inferencia, la perilla $\lambda$ escala el término LoRA en $W=W_0+\lambda\Delta W$.

| $\lambda$ | Actualización aplicada |
|---|---|
| 0 | Base ($W_0$) |
| 0.5 | Mitad de $\Delta W$ |
| 1 | $\Delta W$ tal como se entrenó |
| 1.5 | Una vez y media $\Delta W$ |

**Cómo leer la malla.** Cada fila cambia $\lambda$. Cada columna conserva la semilla y el ruido inicial.

### celda: s10-que-viste

**Qué viste**

- Un rango efectivo muy por debajo de $r$ indica que la energía se concentra en pocas direcciones.
- Para $\lambda=0$, la celda imprime la diferencia absoluta media y máxima de píxeles frente al base. Deberían quedar cerca de cero porque $W_0$ se mantuvo congelada.
