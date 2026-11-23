### celda: s04-intro

## 4 · De la regresión logística a la red

La **regresión softmax** de la unidad 9 es una red con una sola capa de salida.
Calcula diez logits con $\mathbf z_k^{(1)}=\mathbf W^{(1)}\mathbf x_k+\mathbf b^{(1)}$.
Cada fila de $\mathbf W^{(1)}$ reúne los pesos de un dígito. Su sesgo es el intercepto.
La clase predicha tiene el mayor logit. La cross-entropy es $-\log p_{k,y_k}$, con $p$ calculada por softmax.
PyTorch guarda cada imagen en una fila, por eso calcula `x @ W.T + b`.

### celda: s04-logistica-entrena-texto

**Adam actualiza los pesos con cada mini-batch** de train.
La cross-entropy es la misma de la unidad 9, con $\mu=0$.
Una epoch es una pasada por train. La epoch 0 muestra los pesos recién inicializados.

### celda: s04-logistica-mira

Train va en azul, validation en naranja y test en verde.
Si adivinas uniformemente, la loss es $\log 10\approx 2.30$ y la accuracy esperada es $10\,\%$.
La logística mejora de golpe y luego se aplana. Curvas cercanas con error persistente sugieren **underfitting**.
Elige la epoch de menor loss de validation.
Aquí graficamos test para practicar. En un proyecto real se usa una sola vez para el reporte final.

### celda: s04-pesos-texto

Cada fila de $\mathbf W^{(1)}$, vista en una cuadrícula de $28\times28$, es la **plantilla de pesos** de un dígito.
Su logit es $z_i^{(1)}=\sum_j w_{ij}^{(1)}x_j+b_i^{(1)}$.
Si sube un píxel, el rojo indica que sube el logit y el azul que baja.
Busca el centro azul del cero y el trazo vertical rojo del uno.

### celda: s04-neurona

- La neurona calcula $z_i^{(l)}=\sum_j w_{ij}^{(l)}a_j^{(l-1)}+b_i^{(l)}$ y devuelve $a_i^{(l)}=g^{(l)}(z_i^{(l)})$.
- La capa reúne esas neuronas en paralelo. **ReLU introduce no linealidad** con $g(z)=\max(0,z)$.
- Su derivada vale $1$ si $z>0$ y $0$ si $z<0$. En backpropagation usamos $g'(0)=0$.
- Con identidad en ambas capas, todo se reduce a $\mathbf W'=\mathbf W^{(2)}\mathbf W^{(1)}$ y $\mathbf b'=\mathbf W^{(2)}\mathbf b^{(1)}+\mathbf b^{(2)}$.

### celda: s04-apuesta

**Apuesta.** ¿Cuánto mejora la accuracy de validation con $128$ unidades ReLU? (a) Nada, (b) menos de un punto o (c) varios puntos.
¿También se cumple (d), que la red comete menos de la mitad de los errores?
Cada capa tiene $d_l d_{l-1}+d_l$ parámetros. La logística tiene $7\,850$ y la red oculta, $101\,770$.
Ambos puntos de accuracy de la epoch 0 quedan debajo del eje recortado. El $10\,\%$ es la referencia de azar.

### celda: s04-apuesta-respuesta

Se cumplieron (c) y (d). **Ganar pocos puntos puede eliminar muchos errores** cuando el modelo de referencia ya acierta mucho.
Las ReLU permiten fronteras no lineales. En otra corrida puede cambiar la fracción de errores que se elimina.

### celda: s04-que-viste

**Qué viste**

- La loss de la logística cayó en la primera epoch y luego apenas cambió.
- La capa oculta con ReLU redujo la loss de train y los errores de validation.
- Con ReLU se abrió una brecha entre train y validation. En otra corrida puede ser menor.
