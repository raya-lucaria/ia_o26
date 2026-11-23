### celda: s15-intro

## 15 · Batch normalization y dropout

- **El modo de la red cambia el comportamiento de ambas capas.**
- Batch normalization (BN) ajusta centro y escala. Dropout apaga activaciones al azar durante train.
- Calculamos las métricas en `eval()`, incluidas las de train.

### celda: s15-bn-formula

- Para cada neurona, BN usa la media $\mu_{\mathcal B,i}$ y la varianza $\sigma^2_{\mathcal B,i}$ del batch.
- **Estandariza la preactivación** con $\widetilde z_{k,i}=(z_{k,i}-\mu_{\mathcal B,i})/\sqrt{\sigma^2_{\mathcal B,i}+\varepsilon}$. El $\varepsilon$ evita dividir entre cero.
- Pasa $\gamma_i\widetilde z_{k,i}+\beta_i$ a la ReLU. Se aprenden $\gamma_i$ y $\beta_i$, que empiezan en $1$ y $0$.
- El orden es `Linear` → `BatchNorm1d` → `ReLU`. Cada BN agrega $2d_l$ parámetros aprendidos.

### celda: s15-preact-explica

- Las redes comparten los pesos iniciales y el batch de train. En `train()`, BN usa las estadísticas de ese batch.
- Un hook mide la media y la desviación estándar **justo antes de cada ReLU**.
- Predice cómo cambiará la escala entre capas con BN y sin ella.

### celda: s15-preact-lee

| Variante | Qué esperar al inicializar | En las barras por capa |
|---|---|---|
| Con BN | **Centro cerca de cero y escala cerca de uno** | Media cerca de cero y desviación estable |
| Sin BN | Escala dependiente de la profundidad | Desviación decreciente |

Cada neurona aprende su escala y centro con $\gamma_i$ y $\beta_i$.

### celda: s15-apuesta

- **Apuesta.** ¿Con qué combinación bajará más rápido la loss? ¿Alguna podría divergir?
- Elige entre learning rate bajo o alto, con o sin BN. Todas usan SGD sin momentum.

### celda: s15-bn-lee

- **Compara la loss de validation** sin BN a la izquierda y con BN a la derecha.
- Reporta test solo al final y elige el checkpoint con validation. Aquí se grafica test para practicar.

### celda: s15-apuesta-respuesta

| Learning rate | Qué esperar | Sin BN · izquierda | Con BN · derecha |
|---|---|---|---|
| Menor · arriba | Pasos pequeños | Descenso parecido | Descenso parecido |
| Mayor · abajo | Pasos grandes | Oscilación inicial | **Descenso más rápido** |

- Las cuatro corridas terminaron.
- En otra corrida, un paso grande sin BN puede producir más oscilaciones o divergencia.

### celda: s15-bn-eval

- **En `eval()`, BN usa las estadísticas guardadas.** En `train()`, usa las del batch y actualiza sus running averages.
- La actualización es $r\leftarrow(1-m)r+mv$, con $m$ el momentum de BN y $v$ la estimación del batch.
- Con el mismo checkpoint, compara los logits de una imagen al cambiar las imágenes que la acompañan.
- En `train()`, `BatchNorm1d` exige más de una observación para esta entrada.

### celda: s15-dropout-que-es

- En `train()`, **dropout apaga cada activación con probabilidad $p$** y multiplica las restantes por $1/(1-p)$.
- Así conserva su valor esperado, $\mathbb E[\widetilde a]=(1-p)\frac{a}{1-p}=a$.
- En `eval()`, las activaciones pasan intactas. En esta red, `Dropout` va después de cada ReLU oculta.

### celda: s15-dropout-lee

Ambas redes entrenan 80 epochs con un 20 % de etiquetas alteradas en train.

| Variante | Qué esperar | En las curvas de validation y las brechas |
|---|---|---|
| Control | Más memorización | La loss repunta antes y las brechas finales son mayores |
| Con dropout | **Menos memorización** | Repunte más tardío y menor, con brechas finales menores |

`repite_falsa`, la fracción de etiquetas alteradas reproducidas al final, fue mayor en el control.

### celda: s15-que-viste

- En `train()`, los logits con BN cambiaron al variar las imágenes acompañantes.
- Con dropout, la probabilidad del dígito real varió entre evaluaciones de la misma imagen en `train()`.
- **`model.eval()` dio los mismos logits y probabilidades salvo redondeo.**
- En otra corrida, dropout puede reducir menos las brechas de loss y accuracy.
