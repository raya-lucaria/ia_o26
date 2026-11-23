### celda: s14-intro

## 14 · El gradiente por capa (avanzado)

Lectura opcional. Puedes seguir con la §15.
Con la red profunda de §13, comparamos **cómo cambian los gradientes y los pesos por capa**.
Con SGD probamos sigmoide, ReLU y ReLU con batch normalization (BN).
La sigmoide con Adam aparece en la tabla inicial y en los paneles de loss y cambio relativo.

### celda: s14-que-medimos

La **norma de Frobenius** mide la magnitud del gradiente de los pesos en cada capa.
$\|\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\|_F=\sqrt{\sum_{i,j}(\partial L_{\mathcal B}/\partial w_{ij}^{(l)})^2}$, donde $L_{\mathcal B}$ es la loss promedio del mini-batch.
En las curvas de loss, $\log 10$ marca la referencia uniforme.

### celda: s14-apuesta

**Apuesta.** ¿Dónde será menor el gradiente con sigmoide, en la primera capa o en la salida?
Elige también una capa para ReLU o apuesta por normas parecidas.

### celda: s14-apuesta-respuesta

**Con sigmoide, el gradiente es menor cerca de la entrada.** Cada pendiente aporta un factor de hasta $\tfrac14$.
Con ReLU, las neuronas activas dejan pasar su componente del gradiente y las normas quedan más parejas.

### celda: s14-leer-norma

**Compara la primera capa con la salida** en los tres paneles de SGD.
La escala es logarítmica. La línea tenue muestra cada paso y la gruesa, una media móvil en escala logarítmica.
Sigue las líneas para ver cómo cambian las normas durante la corrida.

### celda: s14-norma-que-viste

- **Con sigmoide, el gradiente se desvanece hacia la entrada** y la loss sigue cerca de $\log 10$.
- Con ReLU sin BN, las normas suben al principio mientras baja la loss.
- Con ReLU y BN, las normas bajan desde el inicio. La primera capa queda por encima de la salida.

### celda: s14-va-a-cero

Con **los pesos congelados**, medimos los gradientes al inicio, a la mitad y al final.
$\mathbf g_{\mathrm{completo}}=\nabla_\theta L(\theta)$ usa todo train y $\mathbf g_{\mathcal B}=\nabla_\theta L_{\mathcal B}(\theta)$ usa un mini-batch.
La diferencia $\mathbf g_{\mathcal B}-\mathbf g_{\mathrm{completo}}$ es el ruido del gradiente.
Reutilizamos los mismos mini-batches. Con ReLU sin BN, el aporte de cada ejemplo es independiente de sus acompañantes.

### celda: s14-cero-que-viste

- La loss de train fue menor en cada una de las tres mediciones.
- La norma del gradiente completo y la mediana de las normas de mini-batch subieron primero y luego bajaron.
- **El ruido fue comparable al gradiente completo.** Su norma mediana fue mayor al inicio y al final, y menor a mitad.

### celda: s14-cociente

El **cambio relativo de los pesos** es $\|\mathbf W^{(l)}_{t+1}-\mathbf W^{(l)}_t\|_F/\|\mathbf W^{(l)}_t\|_F$.
En SGD sin momentum, el numerador es $\eta\|\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\|_F$. Adam reescala el paso por parámetro.
Las dos redes con sigmoide parten de los mismos pesos. En Adam, el panel mide el paso efectivo del optimizer.
La línea gris en $10^{-3}$ sirve de referencia práctica.

### celda: s14-que-viste

- Con sigmoide y SGD, las primeras capas cambian mucho menos que la salida. Con ReLU, los cambios son más parejos.
- Hacia el final, **Adam mueve mucho más la primera capa de la sigmoide** que SGD en proporción a sus pesos.
- Con Adam también baja la loss de la sigmoide. Con SGD se queda cerca de la referencia uniforme.
