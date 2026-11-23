### celda: s14-intro

## 14 · El gradiente por capa (avanzado)

- Lectura opcional. Puedes seguir con la §15.
- Con la red profunda de §13, comparamos **gradientes y cambios de pesos por capa**.
- Adam con sigmoide aparece en la tabla inicial y en los paneles de loss y cambio relativo.

### celda: s14-que-medimos

- La **norma de Frobenius** mide la magnitud del gradiente de los pesos en cada capa.
- $\|\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\|_F=\sqrt{\sum_{i,j}(\partial L_{\mathcal B}/\partial w_{ij}^{(l)})^2}$, donde $L_{\mathcal B}$ es la loss promedio del mini-batch.
- En las curvas de loss, $\log 10$ marca la referencia uniforme.

### celda: s14-apuesta

- **Apuesta.** ¿Dónde será menor el gradiente con sigmoide, en la primera capa o en la salida?
- Elige también una capa para ReLU o apuesta por normas parecidas.

### celda: s14-apuesta-respuesta

- **Con sigmoide, el gradiente es menor cerca de la entrada.** Cada pendiente aporta un factor de hasta $\tfrac14$.
- Con ReLU, las neuronas activas dejan pasar su componente del gradiente y las normas quedan más parejas.

### celda: s14-leer-norma

- **Compara la primera capa con la salida** en los tres paneles de SGD.
- En escala logarítmica, la línea tenue muestra cada paso y la gruesa, la media móvil del logaritmo.

### celda: s14-norma-que-viste

| Configuración con SGD | Qué esperar | En las curvas |
|---|---|---|
| Sigmoide | **Gradiente que se desvanece hacia la entrada** | Capas separadas y loss cerca de $\log 10$ |
| ReLU sin BN | Gradientes más parejos | Normas suben al inicio y loss baja |
| ReLU con BN | BN antes de ReLU | Normas bajan y la primera capa queda arriba |

### celda: s14-va-a-cero

**Pesos congelados** al inicio, a la mitad y al final, con los mismos mini-batches.

| Gradiente | Qué mide | En la gráfica |
|---|---|---|
| $\mathbf g_{\mathrm{completo}}=\nabla_\theta L(\theta)$ | Todo train | Rombo |
| $\mathbf g_{\mathcal B}=\nabla_\theta L_{\mathcal B}(\theta)$ | Un mini-batch | Cajas de normas |
| $\mathbf g_{\mathcal B}-\mathbf g_{\mathrm{completo}}$ | Ruido | Cruz para la norma mediana |

Con ReLU sin BN, el aporte de cada ejemplo es independiente de sus acompañantes.

### celda: s14-cero-que-viste

- La loss de train fue menor en cada una de las tres mediciones.
- La norma del gradiente completo y la mediana de las normas de mini-batch subieron primero y luego bajaron.
- **El ruido fue comparable al gradiente completo.** Su norma mediana fue mayor al inicio y al final, y menor a mitad.

### celda: s14-cociente

- El **cambio relativo de los pesos** es $\|\mathbf W^{(l)}_{t+1}-\mathbf W^{(l)}_t\|_F/\|\mathbf W^{(l)}_t\|_F$.
- Las dos redes con sigmoide parten de los mismos pesos.
- La línea gris en $10^{-3}$ sirve de referencia práctica.

### celda: s14-que-viste

| Optimizer con sigmoide | Qué mide el numerador | En las curvas |
|---|---|---|
| SGD sin momentum | $\eta\|\nabla_{\mathbf W^{(l)}}L_{\mathcal B}\|_F$ | Poco cambio cerca de la entrada y loss cerca de $\log 10$ |
| Adam | Paso efectivo reescalado por parámetro | **Mayor cambio relativo en la primera capa que con SGD** al final y loss descendente |

Con ReLU y SGD, los cambios entre capas fueron más parejos.
