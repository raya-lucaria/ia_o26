### celda: s09-intro

## 9 · Optimizers

Sea $\mathbf g_t=\nabla_\theta L_{\mathcal B_t}(\theta_t)$ el gradiente del batch y $\eta$ el learning rate.
**Los optimizers difieren en cómo usan los gradientes.** SGD usa el batch actual y momentum acumula gradientes.

$$
\begin{aligned}
\text{SGD}\quad &\theta_{t+1}=\theta_t-\eta\mathbf g_t,\\
\text{Momentum}\quad &\mathbf m_t=\beta\mathbf m_{t-1}+\mathbf g_t,\qquad
\theta_{t+1}=\theta_t-\eta\mathbf m_t.
\end{aligned}
$$

Adam ajusta cada parámetro con promedios del gradiente y de su cuadrado.

$$
\begin{aligned}
\mathbf m_t&=\beta_1\mathbf m_{t-1}+(1-\beta_1)\mathbf g_t,\\
\mathbf v_t&=\beta_2\mathbf v_{t-1}+(1-\beta_2)\mathbf g_t^2,\\
\widehat{\mathbf m}_t&=\frac{\mathbf m_t}{1-\beta_1^t},\qquad
\widehat{\mathbf v}_t=\frac{\mathbf v_t}{1-\beta_2^t},\\
\theta_{t+1}&=\theta_t-
\eta\frac{\widehat{\mathbf m}_t}{\sqrt{\widehat{\mathbf v}_t}+\varepsilon}.
\end{aligned}
$$

Los denominadores $1-\beta_i^t$ corrigen el arranque en cero. $\varepsilon$ evita dividir entre cero.
AdamW añade weight decay por separado. Las cuatro corridas comparten parámetros iniciales, orden de batches y epochs.

### celda: s09-apuesta

**Apuesta.** ¿Quién terminará con menor loss de validation: SGD, SGD con momentum, Adam o AdamW?
La primera figura muestra la loss de train, validation y test por epoch con fines didácticos (§6). Decide con validation y reserva test para el informe final.

### celda: s09-apuesta-respuesta

**SGD con momentum terminó con la menor loss de validation.** Mira el último punto del panel izquierdo de la segunda figura.
Esa figura compara solo validation. Adam y AdamW quedaron cerca y SGD sin momentum quedó atrás.
Con otra semilla, el orden de las curvas cercanas puede cambiar.

### celda: s09-l2-vs-adamw

### Weight decay en Adam + L2 y AdamW

La penalización $\mu\Omega(\theta)$ suma cuadrados de pesos, $\Omega(\theta)=\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$.
**Con L2, la penalización entra en los promedios de Adam.** Su derivada da `weight_decay` igual a $2\mu$.

$$
\mathbf G_t\leftarrow\mathbf G_t+2\mu\mathbf W_t.
$$

En AdamW, $\mathbf D_t$ es el paso de Adam calculado con el gradiente de los datos.

$$
\mathbf W_{t+1}=(1-2\eta\mu)\mathbf W_t-\mathbf D_t.
$$

Prueba ambas reglas desde $(1,2)$ con gradiente de datos y momentos en cero, $\eta=0.1$ y $2\mu=0.1$.
Con L2, la normalización produce un cambio casi igual en ambos pesos. AdamW les aplica el mismo factor.

### celda: s09-paso-que-viste

- Con Adam + L2, los pesos bajaron casi en paralelo y el cociente $w_2/w_1$ creció.
- **AdamW encogió ambos pesos en la misma proporción.** Con gradiente de datos cero, el cociente quedó en $2$.

### celda: s09-mnist-intro

En MNIST, las tres corridas comparten pesos iniciales, learning rate, orden de batches y epochs.
Adam + L2 y AdamW reciben el mismo `weight_decay`. Adam sin decay sirve de control.

**Apuesta.** ¿Cuál terminará con menor norma de los pesos: Adam + L2, AdamW o el control?

### celda: s09-que-viste

### Qué viste

- **El mismo weight decay produjo efectos distintos.** Adam + L2 redujo la norma al inicio y luego la mantuvo baja. Tuvo la mayor loss de validation.
- La norma creció casi igual con AdamW y con el control. El factor $1-2\eta\mu$ estaba cerca de uno.
- Sus curvas de validation quedaron juntas. En otra corrida, el orden de sus losses finales puede cambiar.
