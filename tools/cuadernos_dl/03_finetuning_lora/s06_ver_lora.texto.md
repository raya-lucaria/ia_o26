### celda: s06-intro

## 06 · Ver LoRA por dentro

Para inspeccionar el adaptador entrenado, la celda sí construye $\Delta W=\frac{\alpha}{r}BA$ para cada capa adaptada. El espectro muestra cuántas direcciones usa la corrección. La norma relativa muestra cuánto pesa frente a $W_0$. La perilla $\lambda$ muestra cómo influye en las imágenes.

### celda: s06-svd-explica

**Valores singulares.** La SVD descompone $\Delta W=\sum_i\sigma_i u_i v_i^\top$, con $\sigma_1\ge\sigma_2\ge\dots\ge0$. El rango exacto es la cantidad de $\sigma_i$ no nulos. Como la actualización pasa por un espacio de dimensión $r$, puede usar hasta $r$ direcciones.

**Cómo leer la gráfica.** Busca valores próximos a cero después de la línea punteada que marca $r$. El eje vertical muestra $\sigma_i/\sigma_1$ en escala logarítmica. La caída puede empezar antes si el adaptador usa menos direcciones. El redondeo puede dejar residuos a la derecha, y una corrección nula deja el cociente sin definir. Se grafica la capa con el mayor cambio relativo y, en modo largo, también la mayor de cada zona disponible.

### celda: s06-barras-explica

La razón $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$ compara el tamaño de la actualización con el del peso original. La norma de Frobenius $\lVert M\rVert_F=\sqrt{\sum_{i,j} M_{ij}^{\,2}}$ reúne todas las entradas de la matriz en una sola magnitud.

- **Zona.** `down` baja la resolución, `mid` es el centro del UNet y `up` vuelve a subirla.
- **Tipo.** *Self-attention* relaciona posiciones del latent entre sí. *Cross-attention* las relaciona con los tokens del texto.

**Cómo leer la gráfica.** A la izquierda hay una barra por capa adaptada, agrupada por zona. A la derecha están los promedios por zona y tipo de atención. La tabla muestra las capas con mayor cambio relativo. Una barra alta indica una corrección grande frente al peso base de esa capa. El efecto visual también depende de cómo se propague esa corrección por el UNet.

### celda: s06-perilla-explica

Al generar, la perilla aplica $W=W_0+\lambda\,\Delta W$.

| $\lambda$ | Qué aplica |
|---|---|
| $0$ | Ninguna corrección. |
| $0.5$ | La mitad de la corrección entrenada. |
| $1$ | La corrección entrenada. |
| $1.5$ | Una vez y media la corrección entrenada. |

**Cómo leer la malla.** Cada fila cambia $\lambda$. Dentro de una columna, el primer prompt y el ruido inicial se mantienen fijos. Una corrección más intensa puede hacer visible un cambio sutil o producir artefactos. La imagen se obtiene en varios pasos de denoising, así que el cambio visual puede ser no lineal.

La celda también compara, píxel por píxel, $\lambda=0$ con el adaptador apagado. Como la corrección se anula, se espera una diferencia nula o cercana a cero.
