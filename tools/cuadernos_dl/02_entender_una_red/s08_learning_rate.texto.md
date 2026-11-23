### celda: s08-intro

## 08 · El learning rate

![Tres pelotas con distinto learning rate](ilustracion:learning_rate)
*(Ilustración generada con gpt-image-2.)*

El **learning rate fija el tamaño del paso** de gradient descent.
$\theta \leftarrow \theta-\eta\,\nabla L(\theta)$, con $\eta$ en el papel de $\alpha$ de la unidad 6.
En el dibujo, la primera pelota apenas avanza, la segunda llega al fondo y la tercera rebota y sale.

### celda: s08-cuadratica-texto

En $f(x,y)=\tfrac12(x^2+100y^2)$ vamos de $(1,1)$ hacia $(0,0)$.
El gradiente $(x,100y)$ da los multiplicadores $1-\eta$ en $x$ y $1-100\eta$ en $y$.
Ambos deben tener magnitud menor que uno. **La dirección más empinada fija el límite** $0<\eta<0.02$.

- $\eta=0.001$ deja un avance lento. Con $\eta=0.01$, $y$ llega a cero en un paso.
- Con $\eta=0.018$, el zigzag se apaga. Con $\eta=0.025$, crece y la trayectoria diverge.

### celda: s08-cuadratica-f-texto

En escala logarítmica, multiplicar $f$ por el mismo factor en cada paso da una recta.
**La dirección plana domina después del zigzag.** Por eso $\eta=0.018$ termina por debajo de $\eta=0.01$.
Con $\eta=2/101\approx0.0198$, los dos multiplicadores tienen igual magnitud y signos opuestos.
Ese valor minimiza la mayor magnitud de los dos.

### celda: s08-mnist-texto

En MNIST, cada corrida parte de los mismos pesos y sesgos y recorre los mismos batches.
**La loss se revisa por bloques.** Con SGD y $\eta=1000$, el primer batch no finito apareció antes de la revisión.
La corrida se detuvo al revisar el bloque. La salida identifica ese primer valor solo como no finito.
La tabla final muestra `NaN`.

### celda: s08-apuesta

**Apuesta.** ¿Qué tasa de `BARRIDO_LR` dará la menor loss final de validation para SGD y para Adam?
¿Cuáles divergirán?

### celda: s08-rejilla-texto

Los paneles comparten ejes y van de menor a mayor $\eta$. Azul es train y naranja es validation.
La línea punteada marca $\log 10$, la cross-entropy de predecir todos los dígitos con igual probabilidad.
**Busca un descenso sostenido.** Las marcas rojas indican máximos fuera de escala o el primer batch con loss no finita.

### celda: s08-u-texto

Cada punto da la loss final de validation. El eje de $\eta$ es logarítmico.
$\times$ señala divergencia o loss final no finita. El triángulo señala un valor finito fuera de escala.
**Busca el fondo de cada U.** Varias tasas cercanas pueden quedar casi empatadas.

### celda: s08-apuesta-respuesta

**Aquí la mejor tasa de SGD fue mayor que la de Adam.**
Adam divide el gradiente suavizado por una escala reciente de cada parámetro.
Con la tasa extrema divergió SGD. Las corridas de Adam terminaron con loss finita.

### celda: s08-que-viste

- **Las tasas intermedias bajaron más la loss.** Con pasos muy chicos, el descenso fue lento.
- Con tasas altas hubo rebotes. Una corrida de SGD se estancó cerca de $\log 10$ con loss finita.
- La tasa extrema de SGD produjo una loss no finita. En otra corrida, Adam también puede divergir con tasas grandes.
- Elige el learning rate con validation y reserva test para el informe final.
