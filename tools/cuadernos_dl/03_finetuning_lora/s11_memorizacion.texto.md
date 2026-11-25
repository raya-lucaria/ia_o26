### celda: s11-intro

## 11 · Memorización

**Memorizar es el overfitting de un modelo generativo:** en vez de aprender la distribución de caras, reproduce caras de train. Buscamos posibles copias. Para cada imagen $g$, medimos su mayor similitud con una cara $x_i$ de train.

$$\text{nn}(g)=\max_i \cos\big(\phi(g),\phi(x_i)\big),\qquad x_i\in\text{train}.$$

| $\phi$ | Un coseno alto indica |
|---|---|
| Embedding de imagen de CLIP | Parecido semántico (tipo de cara, estilo, pose) |
| Píxeles RGB a $64\times64$, centrados por imagen | Copia literal |

- **Referencia.** Las caras reales de validation muestran cuánto se parecen a train otras caras del mismo dominio.
- **Control.** Entrena con menos caras y más pasos que `lora_r8` para favorecer la memorización. Si aún no reproduce caras, sus similitudes pueden quedar cerca de validation.
- **Curvas.** El overfitting del control puede no verse en validation: la loss de difusión es ruidosa porque cada medición mezcla muchos $t$.

### celda: s11-como-leer

**Cómo leer la gráfica.** Cada punto es una imagen y su altura es el mayor coseno frente a train. Compara `base`, `lora_r8` y `control` con «validation (reales)» en ambos paneles.

### celda: s11-que-viste

**Qué viste**

- Usa las medianas para comparar grupos y los máximos para detectar posibles copias aisladas.
- Para buscar copias, revisa los pares del control con mayor similitud en píxeles. La imagen generada va arriba y su vecina de train abajo. Si son casi idénticas, hay evidencia de memorización.
