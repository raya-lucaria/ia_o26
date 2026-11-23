### celda: s09-intro

## 9 · Optimizers

- Sea $\mathbf g_t=\nabla_\theta L_{\mathcal B_t}(\theta_t)$ el gradiente del batch y $\eta$ el learning rate.
- **Los optimizers difieren en cómo usan los gradientes.** Comparten pesos iniciales, batches y epochs.

| Optimizer | Qué hace | Qué buscar en la loss |
| --- | --- | --- |
| SGD | Usa el gradiente del batch | Ritmo de descenso |
| Momentum | Acumula gradientes | Si acelera el descenso |
| Adam | Promedia el gradiente y su cuadrado por parámetro | Si baja pronto |
| AdamW | Separa el weight decay | Cuánto se aparta de Adam |

$$
\begin{aligned}
\text{SGD}\quad &\theta_{t+1}=\theta_t-\eta\mathbf g_t,\\
\text{Momentum}\quad &\mathbf m_t=\beta\mathbf m_{t-1}+\mathbf g_t,\qquad
\theta_{t+1}=\theta_t-\eta\mathbf m_t.
\end{aligned}
$$

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

- Los factores $1-\beta_i^t$ corrigen el arranque en cero.
- $\varepsilon$ evita dividir entre cero.

### celda: s09-apuesta

- **Apuesta.** ¿Menor loss final de validation: SGD, momentum, Adam o AdamW?
- La primera figura incluye test con fines didácticos (§6). Decide con validation y reserva test para el informe final.

### celda: s09-apuesta-respuesta

- **Momentum terminó con la menor loss de validation.** Mira el último punto del panel izquierdo.
- SGD quedó atrás. Adam y AdamW casi empataron. Otra semilla puede invertirlos.

### celda: s09-l2-vs-adamw

### Weight decay en Adam + L2 y AdamW

- **Con L2, la penalización entra en los promedios de Adam.** Su derivada da `weight_decay` igual a $2\mu$.
- La penalización es $\mu\Omega(\theta)$, con $\Omega(\theta)=\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$.

$$
\mathbf G_t\leftarrow\mathbf G_t+2\mu\mathbf W_t.
$$

En AdamW, $\mathbf D_t$ es el paso de Adam calculado con el gradiente de los datos.

$$
\mathbf W_{t+1}=(1-2\eta\mu)\mathbf W_t-\mathbf D_t.
$$

Prueba ambas desde $(1,2)$ con gradiente de datos y momentos en cero, $\eta=0.1$ y $2\mu=0.1$.

### celda: s09-paso-que-viste

**El decay cambia la proporción entre pesos según cómo se aplique.**

| Regla | Qué esperar sin gradiente de datos | Qué se ve |
| --- | --- | --- |
| Adam + L2 | Restas casi iguales | Pesos casi paralelos y $w_2/w_1$ creciente |
| AdamW | Mismo factor para ambos pesos | $w_2/w_1$ constante |

### celda: s09-mnist-intro

- Mismos pesos iniciales, learning rate, batches y epochs.
- Mismo `weight_decay` para Adam + L2 y AdamW. Control con Adam sin decay.
- **Apuesta.** ¿Cuál terminará con menor norma de los pesos?

### celda: s09-que-viste

### Qué viste

- **Con L2, la norma cayó al inicio y se mantuvo baja.**
- AdamW quedó cerca del control. Su factor $1-2\eta\mu$ estaba cerca de uno.
- En otra corrida pueden intercambiar posiciones.

| Variante | Qué aplica | Norma y loss de validation |
| --- | --- | --- |
| Adam + L2 | L2 en el gradiente | Norma baja y loss más alta |
| AdamW | Decay separado | Norma creciente y loss cercana al control |
| Adam | Sin decay | Norma creciente y loss cercana a AdamW |
