### celda: s06-intro

## 06 · La línea base y cómo leer tres curvas

- La **línea base** usa $784\to128\to10$, ReLU, Adam y $\eta=10^{-3}$.
- Entrena ocho epochs con 50 000 ejemplos estandarizados.
- La sección 7 usa SGD con 4096 imágenes. Allí el color identifica el batch y todas las curvas son de validation.

### celda: s06-aviso-test

> **Aviso.** Mirar test en cada epoch está mal: test se usa una sola vez, al final, para reportar. Aquí lo hacemos solo de manera didáctica, para aprender a leer las tres curvas. Ninguna decisión del notebook usa test.

### celda: s06-referencias

**El azar da dos referencias.**

- Con probabilidad uniforme, la cross-entropy es $-\log(1/10)=\log 10\approx 2.30$.
- Al elegir un dígito al azar, la accuracy esperada es $10\,\%$.
- Predecir las proporciones de train da una loss cercana a $\log 10$ porque MNIST está casi balanceado.

### celda: s06-apuesta

- **Apuesta.** ¿Qué conjunto acabará con menor loss y mayor accuracy?
- ¿Esperas que validation y test queden cerca?

### celda: s06-apuesta-respuesta

**Train obtuvo la menor loss y la mayor accuracy.**

| Conjunto | Qué es | Qué esperar | En la gráfica |
|---|---|---|---|
| Train | Datos de ajuste | Ventaja en ambas métricas | Azul se separa |
| Validation | Datos para elegir el checkpoint | Resultados cercanos a test | Naranja cerca de verde |
| Test | Datos del reporte final | Orden variable por muestreo | Verde cerca de naranja |

### celda: s06-como-leer

1. Arriba, compara el inicio con el azar y ubica el salto de la primera epoch.
2. Abajo, usa el acercamiento para ver cuándo se separan las curvas.
3. **La línea naranja vertical marca la menor loss de validation** y el checkpoint elegido.

### celda: s06-brechas

- **La brecha entre train y validation se abrió.** Un valor positivo favorece a train en ambos paneles.
- En loss, la diferencia test menos validation bajó de forma sostenida al final.
- En accuracy, validation menos test quedó dentro de $\pm2$ errores estándar, compatible con variación de muestreo.
- Para esa diferencia, $EE=\sqrt{p_v(1-p_v)/n_v+p_t(1-p_t)/n_t}$ con muestras independientes.

### celda: s06-confianza-intro

**La loss puede subir con accuracy casi estable.** Por imagen, vale $-\log p$ de la clase correcta.

| Promedio de loss | Qué incluye | Qué esperar | En las salidas |
|---|---|---|---|
| Global | Todas las imágenes | Sube con errores más costosos | Repunte en validation |
| Por error | Solo imágenes mal clasificadas | Penaliza valores bajos de $p$ | Más errores muy confiados en el histograma |

### celda: s06-que-viste

**Qué viste**

- La mayor mejora ocurrió en la primera epoch. Después train se despegó de validation.
- Al final hubo más errores y bajó su probabilidad media para la clase correcta.
- La loss de validation repuntó con accuracy casi estable. En otra corrida puede seguir bajando.
