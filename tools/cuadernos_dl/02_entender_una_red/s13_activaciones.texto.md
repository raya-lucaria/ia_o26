### celda: s13-intro

## 13 · Activaciones

Cada capa oculta calcula $\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$ y luego $\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$.
La **activación no lineal** evita que toda la red se reduzca a una transformación afín.
Compara ReLU $\max(0,z)$, sigmoide $1/(1+e^{-z})$, $\tanh(z)$ y GELU $z\Phi(z)$, con $\Phi$ la distribución acumulada normal estándar.
Las redes comparten seis capas ocultas de 128 neuronas, pesos ortogonales iniciales y sesgos en cero.

### celda: s13-derivadas-lectura

- Para la sigmoide, $\sigma'(z)=\sigma(z)(1-\sigma(z))$. **Su pendiente máxima es $\tfrac14$** en $z=0$.
- Para tanh, $1-\tanh^2(z)$ alcanza $1$ en cero. Ambas pendientes se acercan a cero lejos del centro.
- La pendiente de ReLU es $1$ para $z>0$ y $0$ para $z<0$. PyTorch usa $0$ en el origen.
- La pendiente de GELU varía suavemente. Es negativa en parte del lado negativo y supera $1$ en parte del positivo.

### celda: s13-atenuacion

En backpropagation, $\boldsymbol\delta^{(l)}=\nabla_{\mathbf z^{(l)}}\ell$ es el error que llega a la preactivación.
$$
\boldsymbol\delta^{(l)}
=\bigl((\mathbf W^{(l+1)})^\top\boldsymbol\delta^{(l+1)}\bigr)
\odot g^{(l)\prime}(\mathbf z^{(l)}).
$$
Las matrices iniciales tienen norma espectral unitaria. Para la sigmoide, **las pendientes atenúan la señal capa a capa**.
Así, $\|\boldsymbol\delta^{(1)}\|_2\le(\tfrac14)^6\|\boldsymbol\delta^{(7)}\|_2$ al inicio.
El gradiente de los pesos también depende de la entrada, según $\nabla_{\mathbf W^{(l)}}\ell=\boldsymbol\delta^{(l)}(\mathbf a^{(l-1)})^\top$.

### celda: s13-apuesta

**Apuesta.** ¿Cuál tendrá el menor gradiente inicial de los pesos de la primera capa? ¿Cuál tendrá mayor loss final de validation?
Elige entre ReLU, sigmoide, tanh y GELU para cada pregunta.

### celda: s13-gradiente-texto

Usamos el mismo batch antes de actualizar los pesos. `retain_grad()` conserva el gradiente de cada preactivación.
**Medimos dos normas de Frobenius.** Una resume el gradiente de los pesos y la otra, `z.grad`.
Cada fila de `z.grad` contiene el error de una imagen dividido entre el tamaño del batch.

### celda: s13-lee-gradiente

**Sigue las barras de la salida a la entrada** en escala logarítmica.
El panel derecho muestra el error de preactivación. La línea discontinua marca la cota de la sigmoide.
El panel izquierdo mide el gradiente de los pesos, que también depende de las activaciones anteriores.

### celda: s13-lee-histogramas

**Compara la dispersión al aumentar la profundidad.** Cada histograma reúne las activaciones de una capa en el mismo batch inicial.
La sigmoide concentra salidas cerca de $\tfrac12$ y tanh alrededor de cero.
ReLU acumula valores en cero. GELU admite valores negativos pequeños.

### celda: s13-entrenar-texto

**Mismo presupuesto con SGD sin momentum.** Las redes comparten learning rate y orden de batches.
La referencia uniforme da cross-entropy $\log 10$ y accuracy esperada del $10\,\%$.
Test se reporta una sola vez, al final. Aquí se grafica para practicar. Compara las redes con validation.

### celda: s13-lee-durante

**Compara la primera capa con la salida** en la misma escala logarítmica.
Busca si el gradiente de la sigmoide sigue bajo en la primera capa.
Cada batch puede producir picos. Fíjate en el nivel general de la curva.

### celda: s13-apuesta-respuesta

**Sigmoide en ambas.** Tuvo el menor gradiente inicial en los pesos de la primera capa y la mayor loss final de validation.
La cota $(\tfrac14)^6$ corresponde a la señal inicial de preactivación.

### celda: s13-que-viste

- **La sigmoide se estancó.** Su loss llegó pronto a $\log 10$ y permaneció cerca. Su accuracy quedó cerca del azar.
- El gradiente de la primera capa de la sigmoide se mantuvo pequeño durante la corrida.
- ReLU, tanh y GELU llegaron a resultados similares. En otra corrida puede cambiar su orden.
