### celda: s02-intro

## 02 · Tu zip

**Dónde subirlo.** El zip es el de la tarea (`texto.zip`: `datos.jsonl`, `prompts.txt`, `LEEME.md` en la raíz).

1. Abre el panel 📁 **Archivos**, a la izquierda de Colab.
2. **Arrastra** tu `texto.zip` adentro y espera a que termine de subir (el círculo de abajo se llena).
3. Ejecuta. La celda lo encuentra sola en `/content`.

Si pesa mucho, súbelo a tu Drive y quita los `#` de las líneas de Drive en la celda. Si tu zip se llama distinto, escribe su ruta en `RUTA_ZIP`.

**Sin zip no pasa nada:** la celda arma `texto_demo.zip` en el mismo formato, con `P["n_demo"]` ejemplos de `b-mc2/sql-create-context` (1,000 en modo corto, 3,000 en largo) (una tabla y una pregunta → la consulta SQL). Es una buena tarea para ver el cambio: las respuestas son cortas y se pueden comparar letra por letra.

**Si subes un zip de imágenes** a este notebook, la celda se detiene y te da el enlace al notebook 3.

### celda: s02-revisar-explica

- Esta es **la misma función** de la página de la tarea, copiada sin cambios. Imprime `OK` o se detiene diciendo qué está mal: arréglalo en tu zip, vuelve a subirlo y ejecuta otra vez.
- Después se leen los tres archivos: la ficha `LEEME.md`, los ejemplos y los prompts de prueba.
- **Saltos de línea en `prompts.txt`:** cada línea es un prompt. Si tu prompt lleva saltos de línea (como el demo: `Tablas: …` y luego `Pregunta: …`), escríbelos como `\n`, con dos caracteres; el notebook los convierte.

**Cómo leer la tabla de largos:** si el máximo de `prompt` + `completion` pasa de ≈ 2,000 caracteres (≈ 500 tokens), esos ejemplos se cortan en §05 y su final no se aprende.

### celda: s02-split-explica

| Parte | Cuánto | Para qué |
|---|---:|---|
| train | 80 % | lo único que ve el entrenamiento |
| validation | 10 % | medir mientras decides: curvas, métricas, la perilla $\lambda$ |
| test | 10 % | **una sola vez**, al final (§08) |

- La semilla 0 fija qué ejemplo cae en cada parte. Si vuelves a correr, los conjuntos son los mismos.
- **¿Por qué el test una sola vez?** Cada vez que miras el test y cambias algo por lo que viste, el test se vuelve parte del entrenamiento y deja de medir lo que el modelo hace con datos nuevos.
