### celda: s09-intro

## 09 · Learning rate y schedule

- En el notebook 2 (§08) el learning rate fijaba el tamaño del paso, $\theta\leftarrow\theta-\eta\,\nabla L$; aquí lo nuevo es que $\eta$ **cambia con el paso**: warmup + cosine.
- **Warmup:** $\eta$ sube linealmente de 0 al máximo en los primeros $w$ pasos, para no dar pasos grandes con AdamW aún sin estadísticas ($m$, $v$).
- **Cosine:** después baja suave hasta 0 en el paso final $T$:

$$\eta_t=\eta_{\max}\cdot\tfrac12\Big(1+\cos\big(\pi\,\tfrac{t-w}{T-w}\big)\Big),\qquad w\le t\le T$$

- **Constante:** tras el warmup, $\eta_t=\eta_{\max}$ hasta el final.

**Cómo leer la gráfica.** El learning rate de cada paso para los dos schedules; la línea punteada marca el fin del warmup.

### celda: s09-variantes

**➕ Tres corridas nuevas** (todo lo demás igual a `lora_r8`: lr $10^{-4}$, warmup + cosine):

| Corrida | Cambio | Qué se esperaría en la curva | Qué se esperaría en la malla |
|---|---|---|---|
| `s09_lr_1e-5` | lr 10× menor | baja poco y despacio | casi el modelo base |
| `lora_r8` | — | la referencia | el estilo de §07 |
| `s09_lr_1e-3` | lr 10× mayor | baja rápido al inicio; puede saltar o quedar más alta | más estilo, o artefactos y colores saturados |
| `s09_constante` | sin cosine | parecida al inicio; más ruidosa al final | parecida a `lora_r8` |

- Son tendencias, no promesas. LoRA suele tolerar learning rates más altos que el fine-tuning completo ($B$ empieza en 0 y hay pocos parámetros): **si 1e-3 sale bien, no es raro**.
- La loss de difusión depende mucho del $t$ sorteado, así que la curva de train es ruidosa; mira la de validation, que usa $(t,\varepsilon)$ fijos.
- Con pocos pasos, cosine y constante pueden quedar casi iguales: la diferencia está en el tramo final, donde cosine ya casi no mueve los pesos.

### celda: s09-que-mirar

**Qué mirar**

| Dónde | Pregunta |
|---|---|
| Curvas de lr | ¿Cuál baja más rápido? ¿Alguna sube o salta? |
| Curvas de schedule | ¿Se separan solo al final? |
| Malla | ¿1e-5 se parece al base? ¿1e-3 trae artefactos? |

- Elige con validation y con la malla a la vez: la loss de difusión mide qué tan bien se predice el ruido, no qué tan buena se ve la cara.
