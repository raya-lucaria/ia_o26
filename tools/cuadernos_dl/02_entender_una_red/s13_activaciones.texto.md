### celda: s13-intro

## 13 · Activaciones

- Cada capa oculta calcula $\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$ y $\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$.
- La **activación no lineal** evita que la red se reduzca a una transformación afín.
- Las redes usan seis capas ocultas de 128 neuronas, pesos ortogonales iniciales y sesgos en cero.

### celda: s13-derivadas-lectura

| Activación | Qué esperar de la pendiente | En la gráfica de $g'$ |
|---|---|---|
| ReLU $\max(0,z)$ | Cero para $z\le0$ en PyTorch | Escalón de $0$ a $1$ |
| Sigmoide $\sigma(z)=1/(1+e^{-z})$ | $\sigma(z)(1-\sigma(z))$ se acerca a cero en los extremos | **Pico de $\tfrac14$** en cero |
| $\tanh(z)$ | $1-\tanh^2(z)$ se acerca a cero en los extremos | Pico de $1$ en cero |
| GELU $z\Phi(z)$, con $\Phi$ la acumulada normal estándar | Pendiente suave | Tramo negativo a la izquierda y pico por encima de $1$ |

### celda: s13-atenuacion

- En backpropagation, $\boldsymbol\delta^{(l)}=\nabla_{\mathbf z^{(l)}}\ell$ es el error que llega a la preactivación.

$$
\boldsymbol\delta^{(l)}
=\bigl((\mathbf W^{(l+1)})^\top\boldsymbol\delta^{(l+1)}\bigr)
\odot g^{(l)\prime}(\mathbf z^{(l)}).
$$

- Con matrices iniciales de norma espectral unitaria, **la sigmoide atenúa la señal capa a capa**.
- Al inicio, $\|\boldsymbol\delta^{(1)}\|_2\le(\tfrac14)^6\|\boldsymbol\delta^{(7)}\|_2$.
- El gradiente de los pesos también depende de la entrada, $\nabla_{\mathbf W^{(l)}}\ell=\boldsymbol\delta^{(l)}(\mathbf a^{(l-1)})^\top$.

### celda: s13-apuesta

- **Apuesta.** ¿Qué activación tendrá el menor gradiente inicial de los pesos en la primera capa?
- ¿Cuál tendrá mayor loss final de validation? Elige entre ReLU, sigmoide, tanh y GELU.

### celda: s13-gradiente-texto

- Usamos el mismo batch antes de actualizar los pesos. `retain_grad()` conserva el gradiente de cada preactivación.
- **Normas de Frobenius** del gradiente de los pesos y de `z.grad`.
- Cada fila de `z.grad` contiene el error de una imagen dividido entre el tamaño del batch.

### celda: s13-lee-gradiente

- **Sigue las barras de la salida a la entrada** en escala logarítmica.
- El panel derecho muestra el error de preactivación. La línea discontinua marca la cota de la sigmoide.
- El panel izquierdo mide el gradiente de los pesos, que también depende de las activaciones anteriores.

### celda: s13-lee-histogramas

**Compara la dispersión entre capas** en el mismo batch inicial.

| Activación | Qué esperar | En el histograma |
|---|---|---|
| Sigmoide | Salidas entre $0$ y $1$ | Valores cerca de $\tfrac12$ |
| tanh | Salidas centradas en cero | Distribución más estrecha con la profundidad |
| ReLU | Recorte del lado negativo | Pico en cero |
| GELU | Negativos pequeños | Pico cerca de cero con cola positiva |

### celda: s13-entrenar-texto

- **Mismo presupuesto con SGD sin momentum**, mismo learning rate y orden de batches.
- La referencia uniforme da cross-entropy $\log 10$ y accuracy esperada del $10\,\%$.
- Reporta test solo al final y usa validation para comparar. Aquí se grafica test para practicar.

### celda: s13-lee-durante

- **Compara la primera capa con la salida** en la misma escala logarítmica.
- Busca si el gradiente de la sigmoide sigue bajo en la primera capa.
- Cada batch puede producir picos. Fíjate en el nivel general de la curva.

### celda: s13-apuesta-respuesta

- **Sigmoide en ambas** por su menor gradiente inicial en la primera capa y su mayor loss final de validation.
- La cota $(\tfrac14)^6$ corresponde a la señal inicial de preactivación.

### celda: s13-que-viste

- **La sigmoide se estancó.** Su loss llegó pronto a $\log 10$ y permaneció cerca. Su accuracy quedó cerca del azar.
- El gradiente de la primera capa de la sigmoide se mantuvo pequeño durante la corrida.
- ReLU, tanh y GELU llegaron a resultados similares. En otra corrida puede cambiar su orden.
