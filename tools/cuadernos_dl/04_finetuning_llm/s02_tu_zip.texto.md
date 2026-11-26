### celda: s02-intro

## 02 · Tu zip

Empaqueta `datos.jsonl`, `prompts.txt` y `LEEME.md` en la raíz de `texto.zip`. Cada línea de `datos.jsonl` lleva un `prompt`, la entrada al modelo, y un `completion`, la respuesta esperada.

| Dónde está tu zip | Qué haces |
|---|---|
| En tu computadora | Arrástralo al panel **📁 Archivos** de Colab y espera a que termine la carga. |
| En Google Drive | Descomenta las líneas de Drive y ajusta la ruta en `RUTA_ZIP`. |
| Si falla el arrastre | Descomenta la línea con `files.upload()` para abrir el selector de archivos. La ejecución espera a que elijas el zip. |

Con `RUTA_ZIP = ""`, el cuaderno busca primero `texto.zip` en `/content` y en la carpeta actual. También reconoce otros nombres si el zip trae `datos.jsonl` en la raíz. Si tienes varios zips, indica cuál usar en `RUTA_ZIP`. Si encuentra un zip de imágenes como entrada, te dirige al notebook 3.

Si dejas la ruta vacía y la búsqueda no encuentra un zip de texto ni de imágenes, la celda crea `texto_demo.zip` con una muestra de `b-mc2/sql-create-context`. Cada entrada trae el esquema de las tablas y una pregunta. La respuesta esperada es una consulta SQL.

### celda: s02-revisar-explica

`revisar_zip` es la función de la tarea. Comprueba los archivos obligatorios, la cantidad de prompts y ejemplos, las llaves de cada ejemplo y que haya un completion. Si falla, corrige lo que indique el mensaje, vuelve a subir el zip y ejecuta la sección 02.

La celda lee la ficha, muestra ejemplos y resume la longitud de prompts y completions en **caracteres**. Úsala para detectar entradas largas. El recorte en la sección 05 se decide en **tokens** y también cuenta las marcas de la plantilla de chat.

En `prompts.txt`, escribe un prompt por línea. Si un prompt necesita un salto de línea interno, escribe los dos caracteres `\n`. Al leer el archivo, la celda los convierte en un salto de línea.

### celda: s02-split-explica

| Split | Proporción aproximada | Para qué se usa |
|---|---:|---|
| **Train** | 80 % | Calcular los gradientes y actualizar el adaptador. |
| **Validation** | 10 % | Seguir las curvas, comparar respuestas y decidir ajustes. |
| **Test** | 10 % | Medir el resultado final **una sola vez**, en la sección 08. |

El reparto baraja las filas con semilla fija. Con el mismo archivo y orden de filas, se repite el mismo split. Revisa los duplicados antes de empaquetar, porque dos filas iguales pueden quedar en splits distintos.
