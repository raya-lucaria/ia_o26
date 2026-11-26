### celda: s04-intro

## 04 · LoRA por dentro

LoRA (*Low-Rank Adaptation*) congela el peso original $W_0$ y aprende una actualización $\Delta W$ como producto de dos matrices delgadas.

$$
W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}BA.
$$

| Símbolo | Forma | Papel |
|---|---|---|
| $W_0$ | $d\times k$ | Peso congelado de una capa con $k$ entradas y $d$ salidas. |
| $A$ | $r\times k$ | Proyección entrenable de la entrada a $r$ coordenadas. |
| $B$ | $d\times r$ | Proyección entrenable de esas coordenadas a la salida. |
| $r$, $\alpha$ | Escalares | $r$ limita el rango de la corrección. $\alpha/r$ ajusta su escala y aquí vale uno porque $\alpha=r$. |

- **Inicio.** $A$ se inicializa con valores aleatorios y $B=0$. Por eso al comienzo $\Delta W=0$ y la capa equivale a la original.
- **Forward.** Para una entrada $x$, la parte lineal de la salida es $W_0x+\frac{\alpha}{r}B(Ax)$. La corrección se calcula en dos proyecciones, sin construir la matriz completa $BA$.
- **Rango y parámetros.** Como $Ax$ tiene $r$ coordenadas, $\operatorname{rank}(\Delta W)\le r$. Entrenas $r(d+k)$ parámetros del adaptador en lugar de los $dk$ del peso completo.

La celda cuenta las capas lineales de atención del UNet que recibirán LoRA. `to_q`, `to_k` y `to_v` calculan las proyecciones de *query*, *key* y *value*. `to_out.0` proyecta la salida de la atención.

**Cómo leer la tabla.** Compara la fila de LoRA con la del UNet para ver qué fracción de sus parámetros vas a entrenar. La fila de los pesos $W_0$ seleccionados cuenta solo los pesos de las capas elegidas. Los MB estiman el tamaño de los pesos en fp16 para el modelo base y en fp32 para el adaptador.
