### celda: portada

# Tarea 5a · Series de tiempo

Duración aproximada: 75 minutos.

Antes de correr cada bloque, escribe tu predicción en una celda de texto.
Después conserva las salidas y escribe lo solicitado en «Entrega».
Compararás la validación cruzada (*cross-validation*, CV) al azar y la temporal.
Tu punto de comparación (*benchmark*) será «el valor de ayer».

Se entrega el `.ipynb` por Canvas, con las celdas corridas.

La celda que genera los datos está colapsada y marcada «no la abras hasta entregar».
El repositorio es público; nada depende de que esa celda esté oculta.
Los controles visibles del proceso se trabajan en el bloque 5 y en el taller.

### celda: idea

El experimento queda fijo antes de mirar los datos; cada bloque lo usa tal cual.

- **Unidad y serie.** Un día; $y_t$ son los minutos promedio de entrega del
  día $t$. Una **sola serie** de 720 días: los días 1–600 son la historia
  del alumno y los días 601–720 son el despliegue, la continuación de la
  misma serie (no otra muestra).
- **Horizonte y momento.** Al cierre del día $t$ se emite la predicción de
  $y_{t+1}$: un día adelante.
- **Qué se conoce al emitir.** El día de la semana de $t+1$ (calendario).
  La lluvia **del día $t$**, ya observada; la de mañana no se conoce.
  $y_t$ y los anteriores, porque la entrega de hoy se conoce al cierre.
  Nada más de $t+1$.
- **Actualización.** Los parámetros se ajustan en cada corte (al inicio de
  cada bloque de validación y, para el despliegue, al cierre del día 600) y
  quedan fijos dentro del bloque; las entradas (lluvia de hoy, $y_t$) sí se
  actualizan cada día. Es un origen móvil con reajuste por bloque, igual en
  validación y en despliegue.
- **Las dos CV.** Temporal: 5 cortes con bloques de 60 días, hueco 0 (las
  entradas no tienen promedios móviles; si el alumno agrega uno en B5, el
  hueco es su ventana). Al azar: los mismos 600 días en 5 pliegues al azar,
  con las mismas entradas: es el error que se quiere medir.
- **Candidatos.** Lineal en $x$ (día de la semana con dummies y lluvia de
  hoy); vecinos sobre $(x,t)$; bosque sobre $(x,t)$. **Benchmark:** «el
  valor de ayer», $\widehat y_{t+1}=y_t$, que el alumno escribe con
  `shift(1)` y evalúa con el mismo protocolo.

### celda: bloque-1-predice

## 1 · Identifica qué se conoce al emitir

**Predice:** «Vas a comparar la CV al azar con la temporal en los tres candidatos. ¿Cuál crees que promete menos error del que tendrá en los días 601–720, y por cuánto: casi igual, el doble o más?»

La tabla vacía es dada. Llenarla es trabajo propio: escribe la celda con tu clasificación de las columnas de la serie.
Usa los encabezados «columna» y «¿se conoce al emitir?».

### celda: bloque-1-mira

Mira las columnas de la serie y tu tabla.
Contrasta cada fila con el momento de emisión fijado en el experimento.
Revisa a qué día corresponde cada dato antes de clasificarlo.

### celda: entrega-1

la tabla y su predicción

### celda: bloque-2-predice

## 2 · Dibuja los cortes

**Predice:** «En la CV al azar, ¿qué fracción de los días de validación tiene a su día anterior en el entrenamiento?»

El código para dibujar ambas particiones está dado: corre tal cual.
Usa `dibujar_pliegues(600, 5, particion=pliegues(serie, k=5, como="azar"))` y lo mismo con `como="temporal"`.
La gráfica recibe la partición ya calculada mediante `particion`; `como` pertenece a `pliegues`.

El conteo de la fracción está a completar: falta una línea marcada `____`.
Aquí `k` cuenta pliegues; en la unidad 6 era el índice de clase.

### celda: bloque-2-mira

Mira las posiciones de entrenamiento y validación en cada iteración de las gráficas.
Ubica los días de validación y sus días anteriores.
Después lee la fracción que produjo tu conteo y contrástala con tu predicción.

### celda: entrega-2

qué días ve cada iteración y la fracción contada

### celda: bloque-3-predice

## 3 · Compara las promesas

**Predice:** «¿El valor de ayer le gana a algún candidato en la CV temporal?»

El código de `validacion_cruzada` para los tres candidatos está dado, con `particion="azar"` y `particion="temporal"`.
El benchmark está a completar: escribe «el valor de ayer» con `shift(1)` y evalúalo con el mismo protocolo.

### celda: bloque-3-mira

Mira los errores de validación de los candidatos y del benchmark bajo cada partición.
Lee cada cifra junto con el conjunto donde se midió.
La comparación en CV es descriptiva: un error estándar calculado allí no demuestra que una opción gane.

### celda: entrega-3

tabla 4 × 2, cada número con su conjunto y el benchmark

### celda: bloque-4-predice

## 4 · Elige con el pasado, mide con el futuro

**Predice:** «El candidato que gana con la CV al azar, ¿es el mismo que gana con la temporal?»

La elección está a completar: llena `particion=____` en `elegir(con="cv", particion=____)`.
Haz la elección con los días 1–600, antes de evaluar en los días 601–720.

La evaluación con `evaluar` está dada y usa `Seleccion.modelo_final`.
Con `con="cv"`, es el mismo objeto que `modelo`, reajustado con los días 1–600.
Se evalúa en los días 601–720 con el protocolo del experimento.
Conserva el rótulo «error en los días 601–720».

### celda: bloque-4-mira

Mira qué candidato elige cada partición.
Luego compara, para cada candidato, los errores de ambas CV con el error en los días 601–720.
Expresa la relación en veces y deja claro qué cantidad comparas con cuál.
Conserva los nombres de los conjuntos junto a las cifras.

### celda: entrega-4

cuánto mentía cada CV, en veces, para cada candidato

### celda: bloque-5-predice

## 5 · Examina cuándo no miente

**Predice:** «Si apagas la memoria del ruido, ¿la mentira de vecinos crece, se queda o desaparece? ¿Y si enciendes la deriva con la memoria apagada?»

El código de los interruptores está dado en la celda visible de proceso.
Cambia `persistencia` entre 0.9 y 0, y `deriva` entre apagada y encendida.
El código de residuales contra $t$ y de `autocorrelacion` también está dado.

### celda: bloque-5-mira

Mira los residuales contra el tiempo y la gráfica de autocorrelación en cada configuración.
Relaciona esas salidas con las comparaciones de errores.
Anota qué interruptores estaban activos junto a cada resultado que conserves.
Revisa también el caso en que la diferencia es chica.

### celda: entrega-5

qué parte de la mentira viene de la memoria y cuál de la deriva, incluido el caso en que es chica

### celda: taller-intro

## Taller · Cambia los controles del proceso

La celda de proceso que sigue es visible y editable.
Las líneas `persistencia`, `deriva` y `n` son los controles para cambiar.
Conserva la configuración junto con sus salidas para que puedas reconstruir cada comparación.
Mantén identificados los resultados del experimento fijado al inicio.

### celda: galeria-intro

## Galería · Explora la memoria y el pliegue raro

Ejecuta `galeria(clase=5, casos=[13, 16])`.
Examina los casos de la memoria y el pliegue raro.
Relaciona sus particiones con las que dibujaste y con lo que conoce el modelo al emitir.

### celda: cierre

## Revisa tu entrega

Conserva tus predicciones, las salidas y las entregas de cada bloque.
Comprueba que cada número nombre su conjunto y que aparezca el benchmark.

| Bloque | Peso |
|---|---:|
| B1 | 10 % |
| B2 | 10 % |
| B3 | 25 % |
| B4 | 25 % |
| B5 | 30 % |

Se califica que expliques cuándo y por qué miente, no un número exacto.
