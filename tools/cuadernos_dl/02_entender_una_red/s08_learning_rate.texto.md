### celda: s08-intro

## 08 · El learning rate

![Tres pelotas con distinto learning rate](ilustracion:learning_rate)
*(Ilustración generada con gpt-image-2.)*

- El **learning rate fija el tamaño del paso** de gradient descent.
- $\theta \leftarrow \theta-\eta\,\nabla L(\theta)$, con $\eta$ en el papel de $\alpha$ de la unidad 6.

### celda: s08-cuadratica-texto

- En $f(x,y)=\tfrac12(x^2+100y^2)$ partimos de $(1,1)$ hacia $(0,0)$.
- El gradiente $(x,100y)$ da los multiplicadores $1-\eta$ y $1-100\eta$.
- **La dirección más empinada fija el límite** $0<\eta<0.02$.

| Tasa | Qué esperar | En la trayectoria |
|---|---|---|
| $\eta=0.001$ | Paso muy chico | Avance lento |
| $\eta=0.01$ | Anula $y$ en un paso | Caída directa al eje $x$ |
| $\eta=0.018$ | Oscila y converge | Zigzag cada vez menor |
| $\eta=0.025$ | Diverge | Zigzag creciente |

### celda: s08-cuadratica-f-texto

- En escala logarítmica, multiplicar $f$ por el mismo factor en cada paso da una recta.
- **La dirección plana domina al final.** Así, $\eta=0.018$ acaba por debajo de $\eta=0.01$.
- $\eta=2/101\approx0.0198$ minimiza la mayor magnitud de ambos multiplicadores.

### celda: s08-mnist-texto

- Las corridas comparten pesos y sesgos iniciales y secuencia de batches.
- **La loss se revisa por bloques.** La corrida extrema de SGD se detuvo al revisar el bloque con la primera loss no finita.

### celda: s08-apuesta

- **Apuesta.** ¿Qué tasa de `BARRIDO_LR` dará la menor loss final de validation para SGD y para Adam?
- ¿Cuáles divergirán?

### celda: s08-rejilla-texto

- Los paneles comparten ejes y van de menor a mayor $\eta$. Azul es train y naranja es validation.
- La línea punteada marca $\log 10$, la cross-entropy de adivinar uniforme.
- Las marcas rojas indican máximos fuera de escala o la primera loss no finita.

**Las tasas intermedias bajaron más la loss.**

| Tasa | Qué esperar | En la gráfica |
|---|---|---|
| Baja | Pasos cortos | Descenso lento |
| Intermedia | Avance sostenido | Descenso más pronunciado |
| Alta | Saltos grandes | Rebotes o divergencia |

### celda: s08-u-texto

- Cada punto da la loss final de validation. El eje de $\eta$ es logarítmico.
- La $\times$ marca divergencia o loss final no finita. El triángulo marca una loss finita fuera de escala.
- **Busca el fondo de cada U.** Tasas cercanas pueden quedar casi empatadas.

### celda: s08-apuesta-respuesta

**SGD obtuvo su mejor resultado con una tasa mayor que Adam.**

| Optimizer | Qué hace | Qué esperar | En esta gráfica |
|---|---|---|---|
| SGD | Usa el gradiente del batch | Pasos grandes pueden desestabilizarlo | La tasa extrema acabó en $\times$ |
| Adam | Reescala el gradiente suavizado por parámetro | Puede funcionar con tasas menores | Mínimo más a la izquierda, loss final finita |

### celda: s08-que-viste

- Con una tasa alta, **SGD se estancó cerca de $\log 10$** con loss finita.
- En otra corrida, Adam también puede divergir con tasas grandes.
- Elige el learning rate con validation y reserva test para el informe final.
