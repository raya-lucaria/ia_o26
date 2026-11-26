### celda: s06-intro

## 06 · Ver LoRA por dentro

- **Qué vas a ver:** cuatro cosas que solo tiene LoRA, medidas en el adaptador que acabas de entrenar.

| | Qué | Qué esperar |
|---|---|---|
| (a) | valores singulares de $\Delta W$ | caen a cero después del $r$-ésimo |
| (b) | $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$ por capa | cambios **chicos**; unas capas más que otras |
| (c) | la perilla $\lambda$ | $\lambda=0$ es el base; $\lambda$ grande exagera el ajuste |
| (d) | `merge_and_unload` | misma salida que el adaptador, sin capas extra |

La primera celda calcula, para cada capa con LoRA, $\Delta W=\frac{\alpha}{r}BA$ y su tamaño relativo a $W_0$.

### celda: s06-svd-explica

**(a) El rango de $\Delta W$.** Una matriz $d\times k$ cualquiera tiene hasta $\min(d,k)$ valores singulares distintos de cero. $\Delta W=\frac{\alpha}{r}BA$ pasa por un cuello de ancho $r$, así que **a lo más $r$**.

- La gráfica divide cada $\sigma_i$ entre el mayor, $\sigma_1$, y usa escala logarítmica.
- **Gris, $W_0$:** decae poco a poco; la matriz original usa muchas direcciones.
- **Naranja, $\Delta W$:** $r$ valores y luego un **precipicio** hasta $\approx 10^{-7}$, el cero de la aritmética fp32.

**Cómo leer la gráfica:** todo lo que aprendió esta capa vive en $r=8$ direcciones. Eso es lo «low-rank» de LoRA.

### celda: s06-capas-explica

**(b) Qué capas cambiaron más.** Para cada lineal con LoRA, $\lVert\Delta W\rVert_F/\lVert W_0\rVert_F$: cuánto se movió respecto a su propio tamaño.

**Cómo leer la gráfica**

- Una barra por lineal en cada bloque; el eje x va de la entrada (bloque 0) a la salida del modelo.
- Los valores suelen ser **chicos** (del orden de centésimas o menos): LoRA retoca, no reescribe.
- Que unas lineales cambien más que otras depende de tu tarea y de la escala de cada $W_0$. No hay un patrón que *deba* salir; compara la tabla de promedios entre lineales.

### celda: s06-lambda-explica

**(c) La perilla $\lambda$.** Al generar, cada capa calcula

$$h=W_0x+\lambda\,\frac{\alpha}{r}\,B(Ax).$$

- $\lambda=0$: el modelo **base** (la celda lo comprueba contra `lora=False`).
- $\lambda=1$: el adaptador tal como se entrenó.
- $\lambda=0.5$: medio ajuste. $\lambda=1.5$: el ajuste **exagerado**.
- `escala_lora(λ)` multiplica el `scaling` que peft guarda en cada capa (el $\frac{\alpha}{r}$) y lo restaura al salir.

**Cómo leer la tabla:** cada columna es la misma entrada con otro $\lambda$. Busca en qué $\lambda$ aparece el formato de tu dataset. Con $\lambda=1.5$ a veces sale igual que con 1 y a veces se descompone (repite, o se corta): el adaptador se entrenó para $\lambda=1$.

### celda: s06-merge-explica

**(d) Fusionar.** `merge_and_unload()` calcula $W=W_0+\frac{\alpha}{r}BA$ una vez y deja un modelo **normal**, sin capas LoRA: misma forma y mismos parámetros que el base, y ningún costo extra al generar.

- Se hace sobre una **copia**: fusionar destruye el adaptador, y lo necesitas en §07 y §08.
- Los logits no salen idénticos al bit: $W_0$ está en fp16, y al sumarle $\Delta W$ el resultado se **redondea** a fp16. Compara la diferencia con la escala de los logits: es ruido de redondeo.
- Las respuestas greedy casi siempre coinciden. Si alguna difiere, fue un empate casi perfecto entre dos tokens que el redondeo rompió hacia el otro lado.
