### celda: s06-intro

## 06 · Ver LoRA por dentro

Para inspeccionar el adaptador entrenado, la celda construye $\Delta W=\frac{\alpha}{r}BA$ en cada capa adaptada. El espectro muestra cuántas direcciones usa esa corrección. La norma relativa dice cuánto pesa frente a $W_0$. La perilla $\lambda$ y el merge permiten comprobar cómo se aplica al generar.

### celda: s06-svd-explica

La SVD descompone una matriz en direcciones ponderadas por sus valores singulares $\sigma_1\ge\sigma_2\ge\dots\ge 0$. El rango exacto cuenta los valores singulares no nulos. Como $\Delta W$ pasa por un espacio de dimensión $r$, puede usar hasta $r$ direcciones.

**Cómo leer la gráfica.** En la capa con mayor cambio relativo, compara $W_0$ (gris) y $\Delta W$ (naranja). Cada curva divide sus valores singulares por su propio $\sigma_1$ y usa escala logarítmica. Si hay valores de $\Delta W$ a la derecha de la línea que marca el corte en $r$, deben quedar cerca de cero. La caída puede empezar antes si se usan menos direcciones. El redondeo deja residuos pequeños y, si $\Delta W=0$, el cociente queda indefinido.

### celda: s06-capas-explica

La razón $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$ compara el tamaño de la corrección con el peso original. La norma de Frobenius $\lVert M\rVert_F=\sqrt{\sum_{i,j}M_{ij}^2}$ reúne las entradas de una matriz en una sola magnitud.

**Cómo leer la gráfica.** Cada grupo corresponde a un bloque del transformer y cada color a una proyección. Una barra alta indica un cambio grande para esa capa. Cuánto afecta a las respuestas depende también de cómo se propaga la corrección. La tabla promedia por tipo de proyección a través de los bloques.

### celda: s06-lambda-explica

Al generar, `escala_lora` aplica $W=W_0+\lambda\,\Delta W$ en cada capa adaptada y restaura la escala al salir.

| $\lambda$ | Qué aplica |
|---|---|
| $0$ | Corrección nula. La celda compara las respuestas con las del adaptador apagado. |
| $0.5$ | La mitad de la corrección entrenada. |
| $1$ | La corrección entrenada. |
| $1.5$ | Una vez y media la corrección entrenada. |

**Cómo leer la tabla.** En cada fila, compara el mismo prompt a distintas escalas. Se usa el primer prompt de `prompts.txt` y el primero de validation, ambos con greedy decoding. Una respuesta puede quedarse igual si se siguen eligiendo los mismos tokens, o cambiar mucho a partir del primer token que sale distinto.

### celda: s06-merge-explica

`merge_and_unload()` suma $\Delta W$ a $W_0$ en una copia del modelo y elimina las capas LoRA de esa copia. La celda cuenta las capas y los parámetros restantes, compara logits y comprueba si coinciden las respuestas de `prompts.txt`.

En aritmética exacta, sumar los pesos o aplicar la corrección en el forward da el mismo resultado lineal. En precisión finita, las dos operaciones redondean en puntos distintos. Lee la diferencia máxima junto con la magnitud de los logits. Incluso una diferencia pequeña puede cambiar el token elegido si dos logits están muy cerca.
