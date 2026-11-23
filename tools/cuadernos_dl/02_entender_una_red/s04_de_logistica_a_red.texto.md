### celda: s04-intro

## 4 · De la regresión logística a la red

- La **regresión softmax** de la unidad 9 es una red con una sola capa de salida.
- Calcula diez logits con $\mathbf z_k^{(1)}=\mathbf W^{(1)}\mathbf x_k+\mathbf b^{(1)}$.
- Cada fila de $\mathbf W^{(1)}$ reúne los pesos de un dígito. Su sesgo es el intercepto.
- La clase predicha tiene el mayor logit. La cross-entropy es $-\log p_{k,y_k}$, con $p$ calculada por softmax.
- PyTorch guarda cada imagen en una fila, por eso calcula `x @ W.T + b`.

### celda: s04-logistica-entrena-texto

- **Adam actualiza los pesos con cada mini-batch** de train.
- La cross-entropy es la misma de la unidad 9, con $\mu=0$.
- Una epoch es una pasada por train. La epoch 0 muestra los pesos recién inicializados.

### celda: s04-logistica-mira

- Train va en azul, validation en naranja y test en verde.
- Si adivinas uniformemente, la loss es $\log 10\approx 2.30$ y la accuracy esperada es $10\,\%$.
- Las curvas cercanas con error persistente sugieren **underfitting**.
- Elige la epoch de menor loss de validation.
- Graficamos test para practicar. En un proyecto, úsalo una vez al final.

### celda: s04-pesos-texto

- Cada fila de $\mathbf W^{(1)}$, vista en una cuadrícula de $28\times28$, es la **plantilla de pesos** de un dígito.
- Su logit es $z_i^{(1)}=\sum_j w_{ij}^{(1)}x_j+b_i^{(1)}$.
- Si sube un píxel, el rojo indica que sube el logit y el azul que baja.
- Busca el centro azul del cero y el trazo vertical rojo del uno.

### celda: s04-neurona

- Cada neurona calcula $z_i^{(l)}=\sum_j w_{ij}^{(l)}a_j^{(l-1)}+b_i^{(l)}$ y devuelve $a_i^{(l)}=g^{(l)}(z_i^{(l)})$.
- Con identidad en ambas capas, $\mathbf W'=\mathbf W^{(2)}\mathbf W^{(1)}$ y $\mathbf b'=\mathbf W^{(2)}\mathbf b^{(1)}+\mathbf b^{(2)}$.

| Activación | Qué es | Qué esperar | En la gráfica |
|---|---|---|---|
| Identidad | $g(z)=z$ | Composición afín | Diagonal |
| ReLU | $g(z)=\max(0,z)$ | **No linealidad** | Plana hasta cero, diagonal después |

- En backpropagation, ReLU usa $g'(z)=0$ para $z\le 0$ y $1$ para $z>0$.

### celda: s04-apuesta

**Apuesta.** ¿Cuánto mejora la accuracy de validation con $128$ unidades ReLU? (a) Nada, (b) menos de un punto o (c) varios puntos.
¿También se cumple (d), que la red comete menos de la mitad de los errores?

- Cada capa tiene $d_l d_{l-1}+d_l$ parámetros.
- La accuracy inicial queda debajo del eje recortado. La referencia de azar es $10\,\%$.

### celda: s04-apuesta-respuesta

- Se cumplieron (c) y (d). **Ganar pocos puntos puede eliminar muchos errores** cuando el modelo de referencia ya acierta mucho.
- En otra corrida puede cambiar la fracción de errores que se elimina.

### celda: s04-que-viste

**Qué viste**

| Red | Qué es | Qué esperar | En la gráfica |
|---|---|---|---|
| Logística | Solo salida, $7\,850$ parámetros | Fronteras lineales | La loss cae al inicio y se aplana |
| Capa oculta | Unidades ReLU, $101\,770$ parámetros | Fronteras no lineales | Menor loss de train y mayor accuracy de validation |

- Train y validation quedan cerca en la logística.
- Con ReLU se abrió una brecha entre train y validation. En otra corrida puede ser menor.
