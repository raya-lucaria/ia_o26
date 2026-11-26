### celda: s04-intro

## 04 · LoRA por dentro

LoRA (*Low-Rank Adaptation*) congela los pesos base y aprende una corrección en las capas lineales elegidas. En esta sección instalas el adaptador, cuentas sus parámetros y compruebas cómo se comporta antes del primer paso.

### celda: s04-mates

$$
W=W_0+\Delta W,\qquad \Delta W=\frac{\alpha}{r}BA.
$$

| Símbolo | Forma | Papel |
|---|---|---|
| $W_0$ | $d\times k$ | Matriz congelada de una capa con $k$ entradas y $d$ salidas. |
| $A$ | $r\times k$ | Proyección entrenable de la entrada a $r$ coordenadas. |
| $B$ | $d\times r$ | Proyección entrenable de esas coordenadas a la salida. |
| $r$, $\alpha$ | Escalares | $r$ limita el rango de la corrección y $\alpha/r$ fija su escala. |

- **Forward.** Para una entrada $x$, la parte lineal es $W_0x+\frac{\alpha}{r}B(Ax)$. Las dos proyecciones calculan la corrección sin construir la matriz completa $BA$. Durante el entrenamiento se aplica *dropout* a la entrada de la rama LoRA.
- **Inicio.** $A$ se inicializa al azar y $B=0$. Así $\Delta W=0$ y la capa empieza con la misma salida que la original.
- **Rango y parámetros.** La corrección pasa por $r$ coordenadas, así que $\operatorname{rank}(\Delta W)\le r$. Cuando $r$ es pequeño frente a $d$ y $k$, bastan $r(d+k)$ parámetros para el adaptador frente a los $dk$ de la matriz completa.

| Proyecciones | Qué hacen |
|---|---|
| `q_proj`, `k_proj`, `v_proj` | Construyen las *queries*, *keys* y *values* de la atención. |
| `o_proj` | Proyecta la salida de las cabezas de atención al ancho del modelo. |
| `gate_proj`, `up_proj`, `down_proj` | Transforman la representación de cada token en el MLP. Reciben LoRA en modo largo. |

### celda: s04-lee

**Cómo leer las tablas.** El porcentaje global divide los parámetros de $A$ y $B$ entre todos los parámetros del modelo con LoRA. En la tabla del primer bloque, cada porcentaje compara $r(d+k)$ con $dk$ para esa proyección. Solo los parámetros entrenables necesitan estados del optimizador. La memoria de entrenamiento también incluye las activaciones.

Compara los MB de los pesos congelados con el tamaño del adaptador guardado en disco. Por último, lee la diferencia máxima entre los logits con el adaptador recién inicializado y con el adaptador apagado. Con $B=0$, se espera que sea cero.
