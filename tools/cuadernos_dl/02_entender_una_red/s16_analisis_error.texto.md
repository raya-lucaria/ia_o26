### celda: s16-intro

## 16 · Análisis del error

Comparamos MLP de §4–15 que terminaron sin divergir, configurados con los 50 000 ejemplos de train y etiquetas originales.
Algunos agotaron el presupuesto antes de completar la primera epoch.
**Gana el checkpoint con mayor accuracy de validation** entre los elegidos por menor loss de validation en cada corrida.
Si faltan candidatos, entrenamos la línea base de §4. El ganador queda en `CORRIDAS["s16-elegido"]`.
Explora los errores en validation y reserva test para el reporte final.

### celda: s16-apuesta

**Apuesta.** Anota dos confusiones frecuentes que esperas ver (real → predicho).
¿Esperas la misma frecuencia para 4 → 9 y 9 → 4, o frecuencias distintas?

### celda: s16-confusion-texto

En la matriz, **fila real, columna predicha**. La casilla $C_{ij}$ cuenta las imágenes de $i$ predichas como $j$.
- Izquierda. La diagonal cuenta aciertos. Fuera de ella están los errores.
- Derecha. Cada fila suma $100\,\%$ antes de redondear. La suma visible puede quedar un poco arriba o abajo.
- La diagonal de la matriz normalizada da el recall por dígito.

### celda: s16-apuesta-respuesta

**Las confusiones tienen dirección.** Predominó 3 → 5 y fue más común 9 → 4 que 4 → 9.
En otra corrida pueden destacar otros pares. Compara las dos direcciones en la tabla debajo de las métricas.

### celda: s16-metricas-texto

**Cada dígito se compara con el resto**, como en la unidad 9.
- Precision es la fracción correcta de la columna $j$, $C_{jj}/\sum_i C_{ij}$.
- Recall es la fracción correcta de la fila $j$, $C_{jj}/\sum_i C_{ji}$.
- F1 combina ambas, $F_1=2\,\frac{\mathrm{precision}\cdot\mathrm{recall}}{\mathrm{precision}+\mathrm{recall}}$.
- El soporte cuenta los ejemplos reales. Revisa dónde empieza el eje antes de comparar las barras.

### celda: s16-galeria-texto

La **confianza** es la mayor probabilidad anunciada, $\max_j \widehat p_j(x)$.
La galería ordena los errores por confianza. Busca trazos que tú también clasificarías con duda.
Un error muy confiado deja poca probabilidad para la clase real y aporta mucha cross-entropy.
La loss puede subir con el mismo número de aciertos. En §6 aumentaron tanto los errores como su confianza media.

### celda: s16-confianza-texto

Cada grupo se muestra como **densidad** de área $1$. Así puedes comparar sus formas aunque tengan tamaños distintos.
Gris indica aciertos y rojo, errores. Busca dónde se solapan.
La confianza mínima posible es $1/10$, pues las diez probabilidades suman $1$.

### celda: s16-calibracion-texto

Hay **buena calibración** cuando la confianza anunciada coincide con la frecuencia de aciertos.
- Arriba. Cada punto compara ambas cantidades en uno de diez intervalos de igual ancho. Debajo de la diagonal hay sobreconfianza.
- Abajo. Las barras cuentan los casos por intervalo en escala logarítmica. Lee primero los puntos con más casos.

### celda: s16-test-texto

**Evalúa test una vez, con el modelo ya elegido**. Las curvas por epoch de secciones anteriores son un recurso didáctico.
Lee la matriz y las métricas por dígito igual que en validation.
La accuracy de validation puede ser optimista porque sirvió para elegir el modelo.

### celda: s16-tabla-texto

**Compara dentro de cada bloque de datos**. Las filas se ordenan por pasos ejecutados (`pasos_total`) y, si empatan, por sección.
Contrasta también los ejemplos procesados. La tabla conserva el identificador original de `s16-elegido`.
Test queda como registro didáctico. Validation guio la selección.

### celda: s16-que-viste

**Qué viste**

- Predominaron confusiones entre trazos parecidos. Cambiar la dirección del par cambió el conteo.
- El dígito con menor precision fue distinto del de menor recall.
- Los aciertos se concentraron cerca de confianza máxima. Los errores se dispersaron e incluyeron casos muy confiados.
- Hubo ligera sobreconfianza donde se agrupó la mayoría de ejemplos. En otra corrida ese intervalo puede ajustarse a la diagonal.
