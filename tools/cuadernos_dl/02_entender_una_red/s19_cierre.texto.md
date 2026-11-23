### celda: s19-intro

## 19 · Cierre

Compara las corridas registradas para ver **qué cambios movieron el error de validation**.

### celda: s19-tabla-texto

- **Compara dentro de cada grupo de datos**. Las filas se ordenan por accuracy de validation.
- `presupuesto` indica lo configurado. `pasos` indica cuántas actualizaciones se ejecutaron.
- La tabla reporta las métricas del checkpoint con menor loss de validation. Test queda para el reporte.

### celda: s19-figura-texto

- Izquierda. Compara la accuracy de validation. El eje puede empezar por encima de cero y el rayado marca divergencia.
- Derecha. Una **brecha** positiva, $a_{\text{train}}-a_{\text{validation}}$, puede señalar overfitting.
- Con etiquetas alteradas en train, la brecha puede ser negativa porque validation conserva etiquetas limpias.

### celda: s19-figura-mira

Busca **resultados cercanos** entre las corridas con mayor accuracy.
En las de abajo, ubica casos con learning rates extremos, activaciones saturadas o cuellos angostos.
Compara la CNN con los MLP del mismo grupo. Con otra semilla pueden cambiar las diferencias pequeñas.

### celda: s19-movio-texto

El **rango de accuracy de validation** $a_{\max}-a_{\min}$ compara corridas de la misma sección, datos y presupuesto, con dos excepciones.
Se incluyen dropout frente a su control y CNN frente al MLP elegido.
La gráfica muestra el mayor rango arriba. La tabla empieza por el menor.
La anotación de divergencia cuenta las corridas que quedaron fuera del cálculo.

### celda: s19-que-viste

**Qué viste**

- Con SGD y el mismo learning rate, escalar los píxeles mejoró la accuracy de validation (§5). Estandarizarlos dio la mayor.
- Los cuellos angostos rindieron peor (§12). En redes profundas, ReLU superó a sigmoide y batch normalization mejoró ReLU (§13–15).
- Con etiquetas alteradas, early stopping y su control eligieron el mismo checkpoint (§10). Otras corridas pueden mostrar una brecha distinta.
- CNN y MLP quedaron cerca (§17). Las diferencias entre learning rates fueron mucho mayores (§8).

### celda: s19-protocolo

- Train ajusta los pesos.
- **Decide con validation.** Usa su loss para early stopping y sus métricas para elegir el modelo.
- Mira test una sola vez, al final, para reportar el desempeño. Mostrarlo por epoch aquí fue didáctico.

#### Receta práctica para un MLP

- Empieza con una o dos capas ocultas de ancho fijo o con un embudo suave. Crece solo si validation mejora.
- Prioriza el ancho sobre la profundidad.
- Mantén cada capa al menos tan ancha como el número de clases. Un cuello menor puede perder información. Recuerda el de dos unidades en §12.
- Si sobreajusta, prueba early stopping, weight decay con AdamW o dropout antes de achicar la red.
- Empieza con ReLU o GELU, Adam o AdamW, learning rate $10^{-3}$ y batch de 32 a 256.
- Si la red es profunda, prueba batch normalization. Para imágenes, usa una CNN (§17).
