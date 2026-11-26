### celda: s02-intro

## 02 · Tu zip

**Dónde subirlo.** Elige una de tres formas:

| Forma | Cómo | Cuándo |
|---|---|---|
| Panel de archivos | clic en **📁 Archivos** (barra de la izquierda) y **arrastra** tu `imagenes.zip` ahí | lo normal; espera a que termine la barrita de carga |
| Google Drive | quita el `#` de la línea `drive.mount(...)` y escribe la ruta en `RUTA_ZIP` | si tu zip pesa mucho |
| Botón de subir | quita el `#` de la línea `files.upload()` | si el panel no te deja arrastrar |

- Con `RUTA_ZIP = ""` la celda **busca sola** `imagenes*.zip` en `/content` (también `imagenes (1).zip`). Si hay varios, toma el más reciente.
- **Sin zip, el notebook no se detiene:** usa el dataset demo, que la celda siguiente arma en el mismo formato.
- Si encuentra un `texto.zip`, se detiene y te manda al notebook 4, que es el de texto.
- Los archivos subidos al panel **se borran** al cerrar la sesión de Colab. Tu zip original sigue en tu computadora.

### celda: s02-demo-explica

**El demo: caras de anime.** Si no subiste nada, esta celda arma `demo/imagenes.zip` **en el mismo formato que la tarea**, así que todo lo que sigue corre igual que con tu zip.

- Las caras vienen de la colección *moeimouto*, compilada en `ComputerVisionAnimeProject/AnimeFaceColorization` (CC-BY-4.0), en una versión fija del dataset.
- Personajes y caras se eligen con semilla 0. Todas llevan el mismo caption, `"an anime face"`: el modelo aprende un estilo, no identidades. Los derechos de los personajes son de sus autores; aquí solo se estudia el método.
- Las caras miden 252 px, menos que los 512 que pide la tarea: verás el aviso de imágenes chicas, y es cierto.
- Sus `prompts.txt` piden variaciones que no están en el dataset (pelo verde, lentes, un señor mayor).

### celda: s02-revisar-explica

**Revisar antes de usar.** `revisar_zip` es **la misma función** de la página de la tarea, copiada letra por letra. Si ya te dijo `OK` en tu computadora, aquí también.

- Si el zip es de **texto** (trae `datos.jsonl`), la celda se detiene y te da el enlace al notebook 4.
- Si algo falla, el error dice **qué** está mal (una columna, un archivo que falta, una imagen que no abre). Corrige el zip, súbelo otra vez y vuelve a correr desde aquí.
- El error más común: comprimir **la carpeta** en vez de los archivos. Entonces `metadata.csv` queda en `imagenes/metadata.csv` y no en la raíz.

### celda: s02-cargar-explica

**De tu zip a tres conjuntos.**

| Paso | Qué hace | Por qué |
|---|---|---|
| Descomprimir | en `datos_zip/` | leer cada imagen y su caption |
| Muestra | si traes más de `P["max_imagenes"]`, toma una muestra con semilla 0 | que el modo corto quepa en clase |
| Recortar | endereza la foto, recorta un cuadrado **al centro** y lo deja a 512 × 512 | SD 1.5 trabaja a 512 px |
| Deduplicar | hash de la imagen reducida a 16 × 16 | una imagen repetida en train y en test haría que test premie memorizar |
| Partir | 80 % train, 10 % validation, 10 % test, con semilla 0 | misma partición en cada corrida |

- **Train** enseña. **Validation** sirve para mirar y decidir. **Test** se usa una sola vez, en la sección 08.
- Cada imagen conserva **su** caption (columna `text`). Si todas dicen lo mismo, verás «captions distintos = 1».

### celda: s02-muestra-explica

- Hasta ocho imágenes de train, ya recortadas, con su caption encima. **Revisa que el recorte al centro no corte lo importante.**
- Debajo, tus prompts de prueba y tu ficha. Los prompts vuelven en la sección 03 (antes) y en la 08 (después).
