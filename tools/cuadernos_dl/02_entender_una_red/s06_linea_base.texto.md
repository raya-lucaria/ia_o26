### celda: s06-intro

## 06 · La línea base y cómo leer tres curvas

La **línea base** reutiliza la red $784\to128\to10$ con ReLU, Adam y $\eta=10^{-3}$.
La configuración completa usa ocho epochs y 50 000 ejemplos estandarizados de train.
Aquí train va en azul, validation en naranja y test en verde.
La sección 7 usa SGD con 4096 imágenes. Allí todas las curvas son de validation y el color identifica el batch.

### celda: s06-aviso-test

> **Aviso.** Mirar test en cada epoch está mal: test se usa una sola vez, al final, para reportar. Aquí lo hacemos solo de manera didáctica, para aprender a leer las tres curvas. Ninguna decisión del notebook usa test.

### celda: s06-referencias

**El azar da dos referencias.**

- Con probabilidad uniforme, la cross-entropy es $-\log(1/10)=\log 10\approx 2.30$.
- Al elegir un dígito al azar, la accuracy esperada es $10\,\%$.
- Predecir siempre las proporciones de train da una loss cercana a $\log 10$ porque MNIST está casi balanceado.

### celda: s06-apuesta

**Apuesta.** Al final, ¿cuál de los tres conjuntos tendrá menor loss y cuál mayor accuracy?
¿Esperas que validation y test queden cerca o se separen?

### celda: s06-apuesta-respuesta

**Train terminó con la menor loss y la mayor accuracy** porque el modelo se ajustó con esos datos.
Validation y test quedaron cerca. En otra corrida su orden puede cambiar por variación de muestreo.

### celda: s06-como-leer

1. Arriba, compara la epoch 0 con las referencias de azar. Ubica el salto de la primera epoch.
2. Abajo, usa el acercamiento para ver cuándo se separan las curvas.
3. **La línea naranja marca la menor loss de validation**. Ahí se guarda el checkpoint elegido.

### celda: s06-brechas

- **La brecha entre train y validation se abrió.** Un valor positivo favorece a train en ambos paneles.
- En loss, la diferencia test menos validation bajó de forma sostenida en el tramo final.
- En accuracy, validation menos test quedó dentro de la banda de $\pm2$ errores estándar, compatible con variación de muestreo.
- Para esa diferencia, $EE=\sqrt{p_v(1-p_v)/n_v+p_t(1-p_t)/n_t}$ con muestras independientes.

### celda: s06-confianza-intro

**La loss puede subir con accuracy casi estable.** Para cada imagen, la loss es $-\log p$ de la clase correcta.
La tabla compara los grupos de errores del mejor checkpoint y del último.
Al final hubo más errores y su probabilidad media para la clase correcta fue menor.
La loss media por error subió. Se calcula promediando $-\log p$ por imagen.

### celda: s06-que-viste

**Qué viste**

- La mayor mejora ocurrió en la primera epoch. Después train se despegó de validation.
- La loss de validation repuntó al final con accuracy casi estable. En otra corrida puede seguir bajando.
- El histograma final mostró más errores con confianza alta en la clase equivocada.
