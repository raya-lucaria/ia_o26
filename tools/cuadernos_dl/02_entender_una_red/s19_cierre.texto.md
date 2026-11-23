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

**Las diferencias pequeñas** pueden cambiar con otra semilla.

| Cambio | Qué es | Qué esperar | Cómo se ve |
|---|---|---|---|
| Escala (§5) | Píxeles crudos, reescalados o estandarizados | Estandarizar mejoró la accuracy con SGD | Barra más larga |
| Forma (§12) | Ancho fijo, embudo o cuello | El cuello angosto rindió peor | Barra más corta |
| Activación (§13) | ReLU frente a sigmoide | ReLU rindió mejor en redes profundas | Barras de ReLU más largas |
| Batch normalization (§15) | ReLU con o sin normalización | Con BN subió la accuracy | Barras con BN algo más largas |

### celda: s19-movio-texto

- El **rango de accuracy de validation** $a_{\max}-a_{\min}$ agrupa por sección, datos y presupuesto.
- Incluye dropout frente a su control y CNN frente al MLP elegido.
- Los rangos mayores van arriba.

| Cambio | Qué se ajusta | Qué esperar | Cómo se ve |
|---|---|---|---|
| Learning rate (§8) | Tamaño del paso | Un extremo puede divergir | Barra larga y divergencias anotadas |
| Optimizer (§9) | Regla de actualización | Diferencias menores aquí | Barras cortas |
| Dropout (§15) | Apaga activaciones al azar en train | Mejoró frente al control | Barra corta |

### celda: s19-que-viste

**Qué viste**

- Cambiar learning rate o activación movió mucho la accuracy.
- La CNN y el MLP quedaron cerca.
- Con etiquetas alteradas, early stopping y su control eligieron el mismo checkpoint (§10). El rango puede variar en otra corrida.

### celda: s19-protocolo

- Train ajusta los pesos.
- **Decide con validation**. Usa su loss para early stopping y sus métricas para elegir el modelo.
- Mira test una vez al final para reportar el desempeño. Mostrarlo por epoch fue didáctico.

#### Receta práctica para un MLP

- Empieza con una o dos capas ocultas de ancho fijo o con un embudo suave.
- Prioriza el ancho sobre la profundidad. Crece solo si validation mejora.
- Mantén cada capa al menos tan ancha como el número de clases (§12).
- Si sobreajusta, prueba early stopping, weight decay con AdamW o dropout.
- Empieza con ReLU o GELU, Adam o AdamW, learning rate $10^{-3}$ y batch de 32 a 256.
- Para redes profundas, prueba batch normalization. Para imágenes, usa una CNN (§17).
