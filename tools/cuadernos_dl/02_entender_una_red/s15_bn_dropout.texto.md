### celda: s15-intro

## 15 · Batch normalization y dropout

**El modo de la red cambia el comportamiento de ambas capas.**
Batch normalization (BN) ajusta el centro y la escala de las preactivaciones. Dropout apaga activaciones al azar durante train.
Las métricas se calculan en `eval()`, incluidas las de train.

### celda: s15-bn-formula

- Para cada neurona, BN usa la media $\mu_{\mathcal B,i}$ y la varianza $\sigma^2_{\mathcal B,i}$ del batch.
- **Estandariza la preactivación** con $\widetilde z_{k,i}=(z_{k,i}-\mu_{\mathcal B,i})/\sqrt{\sigma^2_{\mathcal B,i}+\varepsilon}$. El $\varepsilon$ evita dividir entre cero.
- Pasa $\gamma_i\widetilde z_{k,i}+\beta_i$ a la ReLU. Se aprenden $\gamma_i$ y $\beta_i$, que empiezan en $1$ y $0$.
- El orden es `Linear` → `BatchNorm1d` → `ReLU`. Cada BN agrega $2d_l$ parámetros aprendidos.

### celda: s15-preact-explica

Las redes comparten los pesos iniciales y el batch de train. En `train()`, BN usa las estadísticas de ese batch.
Un hook mide la media y la desviación estándar **justo antes de cada ReLU**.
Predice cómo cambiará la escala entre capas con BN y sin ella.

### celda: s15-preact-lee

**Con BN, la media queda cerca de cero y la desviación estándar, cerca de uno** al inicializar.
Sin BN, la desviación estándar disminuye con la profundidad.
Al aprender $\gamma_i$ y $\beta_i$, cada neurona puede ajustar su escala y su centro.

### celda: s15-apuesta

**Apuesta.** ¿Con qué combinación bajará más rápido la loss? ¿Alguna podría divergir?
Elige entre learning rate bajo o alto, con o sin BN. Todas usan SGD sin momentum.

### celda: s15-bn-lee

**Compara con y sin BN dentro de cada fila.** Arriba está el learning rate menor y abajo el mayor.
Sigue el descenso de la loss de validation y busca oscilaciones.
Test se reporta una sola vez, al final. Aquí se grafica para practicar. El checkpoint se elige con validation.

### celda: s15-apuesta-respuesta

**Con el learning rate mayor, la loss bajó más rápido con BN.**
Con el paso menor, las dos curvas bajaron a ritmos parecidos.
Las cuatro corridas terminaron. En otra corrida, la red sin BN puede oscilar más o divergir con un paso grande.

### celda: s15-bn-eval

**En `eval()`, BN usa las estadísticas guardadas.** En `train()`, usa las del batch y actualiza sus running averages.
La actualización es $r\leftarrow(1-m)r+mv$, con $m$ el momentum de BN y $v$ la estimación del batch.
Con el mismo checkpoint, compara los logits de una imagen al cambiar las imágenes que la acompañan.
En `train()`, `BatchNorm1d` exige más de una observación para esta entrada.

### celda: s15-dropout-que-es

En `train()`, **dropout apaga cada activación con probabilidad $p$** y multiplica las restantes por $1/(1-p)$.
Así conserva su valor esperado, $\mathbb E[\widetilde a]=(1-p)\frac{a}{1-p}=a$.
En `eval()`, las activaciones pasan intactas. En esta red, `Dropout` va después de cada ReLU oculta.

### celda: s15-dropout-lee

- Ambas redes entrenan 80 epochs con un 20 % de etiquetas alteradas en train.
- **La loss de validation del control subió tras su mínimo.** Con dropout, el repunte fue posterior y menor.
- Al final, `repite_falsa` fue mayor en el control. Mide la fracción de etiquetas alteradas que reproduce cada red.
- La comparación de etiquetas ocurre al final y deja abierto cuándo empezó la memorización.

### celda: s15-que-viste

- En `train()`, con BN cambiaron los logits al cambiar las imágenes acompañantes. Con dropout varió la probabilidad del dígito real.
- **`model.eval()` hizo repetibles los logits y las probabilidades.** BN usó estadísticas guardadas y dropout dejó pasar todas las activaciones.
- Con dropout, las brechas finales de loss y accuracy fueron menores. En otra corrida, la diferencia puede ser más pequeña.
