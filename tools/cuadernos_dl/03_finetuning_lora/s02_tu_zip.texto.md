### celda: s02-intro

## 02 · Tu zip

| Dónde está tu zip | Qué haces |
|---|---|
| En tu computadora | Arrástralo al panel **📁 Archivos** de la izquierda y espera a que termine la carga. |
| En Google Drive | Descomenta `drive.mount(...)` y pega la ruta del zip en `RUTA_ZIP`. |
| Si falla el arrastre | Descomenta `files.upload()` para abrir el selector de archivos. |

Con `RUTA_ZIP = ""`, se busca `imagenes*.zip` en `/content` y en la carpeta de trabajo. Si hay varios, se elige el más reciente. Si el tuyo tiene otro nombre, escribe su ruta en `RUTA_ZIP`. Si solo hay coincidencias con `texto*.zip`, la celda te dirige al notebook 4.

### celda: s02-demo-explica

Si dejas la ruta vacía y la búsqueda no encuentra ninguno de los dos tipos de zip, la celda crea `demo/imagenes.zip` con el formato de la tarea. En una corrida normal, toma caras de anime de una versión fija de `ComputerVisionAnimeProject/AnimeFaceColorization`, con muestreo reproducible. En `RAPIDO=1`, dibuja óvalos de colores.

El demo usa el caption `an anime face` para todas las imágenes. Sus prompts piden variaciones de pelo, lentes o edad para explorar cómo responde el modelo. Si aparece un aviso de resolución, las imágenes se ampliaron durante la preparación.

### celda: s02-revisar-explica

`revisar_zip` es la función de la tarea. Comprueba los archivos obligatorios, la cantidad de ejemplos y prompts, las columnas del CSV, los captions y que los archivos de imagen se puedan abrir. Si detecta `datos.jsonl` sin `metadata.csv`, el notebook indica que corresponde a la ruta de texto y muestra el enlace al notebook 4.

Si la revisión falla, usa el mensaje para localizar el problema, corrige el zip y vuelve a ejecutar la sección 02. Empaqueta los archivos de modo que `metadata.csv`, `prompts.txt`, `LEEME.md` y `images/` queden en la raíz.

### celda: s02-cargar-explica

| Paso | Qué hace |
|---|---|
| Descomprimir | Extrae el zip en `datos_zip/` y lee el CSV, los prompts y la ficha. |
| Muestrear | Si el zip supera `P["max_imagenes"]`, toma una muestra con semilla fija. |
| Preparar | Corrige la orientación EXIF, convierte a RGB y hace un recorte cuadrado al centro del tamaño `P["res"]`. |
| Deduplicar | Descarta imágenes con la misma huella al reducirlas. Así evita repartir copias detectadas entre los splits. |
| Partir | Baraja con semilla fija y reparte aproximadamente 80 % para **train**, 10 % para **validation** y 10 % para **test**. |

Cada imagen conserva el caption de la columna `text`. **Train** actualiza el adaptador, **validation** orienta tus decisiones y **test** queda reservado para la evaluación final.

### celda: s02-muestra-explica

**Cómo leer la malla.** Cada imagen de train lleva su caption. Revisa que el recorte conserve el motivo, y que el caption describa lo que quedó en la imagen. Debajo aparecen los prompts de prueba y la ficha de tu dataset.
