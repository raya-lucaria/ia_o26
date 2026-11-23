### celda: s02-intro

## 02 · Los datos

Cada imagen de MNIST tiene $28 \times 28$ píxeles en gris y una etiqueta del 0 al 9.
La partición de Nielsen deja las últimas 10 000 imágenes del train original para validation. `ORIGEN` conserva sus índices.
**Train ajusta los parámetros y validation guía las decisiones.** Usa test una vez al final para reportar el desempeño.

### celda: s02-pruebas-explica

**Índices distintos pueden contener los mismos píxeles.** Los `assert` verifican tamaños e índices. Los *hashes* detectan imágenes idénticas.
Compara las tres barras de cada dígito. La línea punteada marca el 10 % de un reparto uniforme.
Adivinar al azar con igual probabilidad para cada dígito da un 10 % de accuracy en promedio.

### celda: s02-muestra-explica

Compara los trazos de las dos imágenes de cada dígito.
**El MLP aplana cada cuadrícula** en una fila de $784$ intensidades. La red convolucional de la sección 17 conserva la cuadrícula.

### celda: s02-gpu-explica

- `DATOS[escala][conjunto]` guarda `(X, y)` en `DEVICE`. `X` tiene una imagen por fila e `y` una etiqueta entera por imagen.
- `"crudo"` conserva las intensidades de 0 a 255. `"01"` las divide entre 255.
- `"estandar"` aplica $(x-\mathrm{MEDIA})/\mathrm{DESV}$ a la escala `"01"`, con **media y desviación calculadas solo en train**.
- `RAPIDO` recorta los tres conjuntos por dígito. `IMAGENES_TEST` guarda cuadrículas de test en CPU para las galerías de errores.

### celda: s02-subconjunto-explica

`subconjunto(n)` toma **cerca de $n/10$ ejemplos de train por dígito**. Con los mismos datos, tamaño y semilla, devuelve los mismos índices.
Validation y test se evalúan con todos los ejemplos disponibles en el modo elegido.

### celda: s02-que-viste

Qué viste

- **La mezcla de dígitos es parecida en los tres conjuntos.** El 1 supera la referencia uniforme. El 5 queda por debajo.
- Las huellas no detectaron imágenes idénticas dentro de los conjuntos ni entre ellos.
