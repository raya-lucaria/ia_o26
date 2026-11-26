### celda: s04-intro

## 04 · LoRA por dentro

- **Qué vas a ver:** la fórmula de LoRA y, medido en **tu** modelo, cuántos parámetros entrenas y cuánto pesa lo que te llevas.
- Las cuentas de esta sección son exactas; los números los imprime el código.

### celda: s04-mates

**LoRA (Low-Rank Adaptation).** Cada capa lineal elegida cambia así:

$$W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}\,BA,\qquad B\in\mathbb R^{d\times r},\; A\in\mathbb R^{r\times k},\; r\ll\min(d,k).$$

- $W_0\in\mathbb R^{d\times k}$ queda **congelada**; solo se entrenan $A$ y $B$. Aquí $r=8$ y $\alpha=16$, así que $\frac{\alpha}{r}=2$.
- **Forward sin formar $\Delta W$:** $h=W_0x+\frac{\alpha}{r}\,B(Ax)$. Primero $Ax\in\mathbb R^{r}$, luego $B(Ax)\in\mathbb R^{d}$.
- **Inicio:** $A$ al azar y $B=0$ $\Rightarrow$ $\Delta W=0$. El modelo arranca **idéntico** al base; la última celda lo comprueba.
- **Rango:** $\operatorname{rank}(\Delta W)\le r$, porque todo pasa por un espacio de dimensión $r$. En §06 lo ves en los valores singulares.
- **Parámetros:** $dk$ si entrenaras $W$ completa, contra $r(d+k)$ con LoRA.

**Dónde va LoRA en un transformer.** Cada bloque tiene atención y un MLP, y los dos están hechos de lineales:

| Lineal | Dónde | Qué hace |
|---|---|---|
| `q_proj`, `k_proj`, `v_proj` | atención | arman las *queries*, *keys* y *values* |
| `o_proj` | atención | mezcla las cabezas de vuelta al ancho del modelo |
| `gate_proj`, `up_proj`, `down_proj` | MLP | el MLP de cada bloque (solo en `MODO = "largo"`) |

En Qwen2.5, `k_proj` y `v_proj` son **más angostas** que `q_proj`: varias cabezas de *query* comparten una misma *key* y *value* (*grouped-query attention*). Por eso su $d$ sale más chico en la tabla.

### celda: s04-lee

**Cómo leer las tablas**

- `% entrenable` es la fracción del modelo que recibe gradiente. Todo lo demás está congelado y no necesita ni gradiente ni momentos de AdamW: por eso cabe en una T4.
- `MB del adaptador` es lo que descargas en §08. Compáralo con los MB del modelo: tu ajuste viaja en un archivo cientos de veces más chico, y se pone encima del modelo base de cualquiera.
- En la tabla por capa, `%` es $r(d+k)/dk$: cuanto más grande la capa, más ahorra LoRA.
- La diferencia de logits de la última celda tiene que ser **exactamente 0**: con $B=0$, la capa suma cero.
