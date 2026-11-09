### celda: portada

# Tarea 5c · Otras familias (opcional)

Duración estimada: 45 minutos.

Al terminar tendrás:

- **Selección:** elegirás la capacidad de un árbol, un bosque y boosting con los mismos pliegues.
- **Comparación:** reunirás errores, dispersión entre pliegues y tiempos de ajuste.
- **Conclusión:** identificarás una victoria y una limitación de cada familia, incluyendo su predicción fuera del rango observado.

Ejecuta primero el arranque. Antes de correr cada bloque, escribe tu predicción en una celda de texto.
Después conserva las salidas y responde lo solicitado en «Entrega».

Se entrega el `.ipynb` por Canvas, con las celdas corridas.
La fecha la da el profesor.

La celda que genera los datos está colapsada y marcada «no la abras hasta entregar».
El repositorio es público; nada depende de que esa celda esté oculta.

### celda: idea

Tres familias, una sola manera de elegir.
Estimarás minutos de entrega para un despliegue con clientes nuevos.
Compararás un árbol, un bosque (*random forest*) y boosting mediante validación cruzada (*cross-validation*, CV).
Mantendrás la misma partición por cliente para todas las familias.

Lo que traes: pliegues por grupo, curvas de capacidad y la regla de un error estándar (EE).
Usarás un punto de comparación (*benchmark*) para interpretar los errores.
La tarea es de regresión de minutos, sin pesos de clase.

### celda: bloque-1-predice

## 1 · Conserva la misma partición

**Predice: «Si cada familia usara sus propios pliegues, ¿podrías decir cuál es mejor?»**

El código está **dado**: corre tal cual.
La celda llama `pliegues(..., como="grupo")` una vez y reutiliza esa partición en las comparaciones siguientes.
Los grupos corresponden a clientes, de acuerdo con el uso previsto.

### celda: bloque-1-mira

Mira la partición por grupos que construye la celda.
Identifica qué clientes quedan para ajustar y cuáles para validar en cada pliegue.
Sigue el uso de esa misma partición al pasar de una familia a otra.

### celda: entrega-1

**Entrega:** por qué la misma

### celda: bloque-2-predice

## 2 · Elige la profundidad del árbol

**Predice: «¿Qué profundidad crees que elige la CV: 2, 5 o 15?»**

El código está **dado**: corre tal cual.
Incluye el ajuste con `ajustar_otro(familia="arbol", profundidad=…)` y la curva de capacidad.

La regla de un EE está **a completar**: escribe la línea marcada `____`.
Usa la curva para aplicar la regla y conserva la profundidad elegida.

### celda: bloque-2-mira

Mira cómo cambia el error de CV al recorrer las profundidades.
Ubica los EE que acompañan la curva y contrasta tu elección con tu predicción inicial.
El bloque 5 usará la profundidad que dé tu regla.

### celda: entrega-2

**Entrega:** profundidad elegida con la regla de un EE

### celda: bloque-3-predice

## 3 · Compara tamaños del bosque

**Predice: «Con 300 árboles en lugar de 10, ¿la CV sube, baja o se queda?»**

El código está **dado**: corre tal cual.
Compara de 10 a 300 árboles con tres semillas del bosque.
En la unidad 6, $B$ era la capacidad de los coeficientes; aquí, el número de árboles.

Al cambiar la semilla del bosque, los datos no cambian.
Cambian el ajuste y su riesgo realizado; las semillas corresponden al bosque, no a nuevas muestras de datos.

### celda: bloque-3-mira

Mira las curvas de CV contra el número de árboles.
Compara cuánto cambia cada curva al aumentar el bosque y cuánto difieren las tres semillas para un mismo tamaño.
Apoya tu lectura de la estabilidad en ambas comparaciones.

### celda: entrega-3

**Entrega:** ¿se estabiliza?, mirando también cuánto difieren las semillas (`ml-c5-obs-bagging`)

### celda: bloque-4-predice

## 4 · Elige las etapas de boosting

**Predice: «Con una tasa $\nu$ diez veces más chica, ¿necesitas más o menos etapas?»**

El código está **dado**: corre tal cual.
Primero recorre el número de etapas con una tasa $\nu$ fija; después compara dos tasas.
Conserva las curvas para justificar tu elección de etapas.

### celda: bloque-4-mira

Mira el error de CV contra el número de etapas para cada tasa.
Localiza dónde elegirías detenerte y compara esa ubicación entre las dos curvas.
Relaciona las etapas elegidas con la tasa usada, sin separar una elección de la otra.

### celda: entrega-4

**Entrega:** etapas elegidas; qué pasa con $\nu$ chico

### celda: bloque-5-predice

## 5 · Compara y extrapola

**Predice: «Para una distancia el doble de la mayor que viste, ¿qué familia se equivoca más?»**

El código es **propio**: tú escribes la celda.
Reúne por familia el error de CV ± EE, el benchmark y el tiempo de ajuste.
Usa los mismos pliegues y el mismo criterio de error.
Añade la predicción fuera del rango de distancias observado, en la distancia indicada por la pregunta.

### celda: bloque-5-mira

Lee la tabla comparando cada familia con el benchmark.
Nombra el conjunto y el criterio de cada error; distingue el tiempo de ajuste de la calidad de la predicción.
El EE entre pliegues es descriptivo: no demuestra que una familia sea superior.

Mira después las predicciones fuera del rango de distancias.
Separa lo que observaste en CV de lo que muestra esta extrapolación.
Usa ambas salidas al describir las ventajas y limitaciones.

### celda: entrega-5

**Entrega:** una victoria y una limitación de cada familia

### celda: taller-intro

## Taller · Examina el proceso visible

La celda visible permite explorar la curva en distancia, la interacción entre lluvia y hora, y el tamaño de muestra $n$.
Cambia un elemento a la vez y conserva las salidas que compares.
Describe qué modificaste antes de atribuirle un cambio en los resultados.

### celda: galeria-intro

## Galería · Examina el caso indicado

Ejecuta `galeria(clase=5, casos=[16])` y lee la situación que presenta.
Conserva la salida y describe lo que observas.

### celda: cierre

Conserva tus predicciones iniciales, las cinco entregas y las salidas que las sustentan.
Revisa que cada comparación identifique su conjunto, su criterio y su benchmark.

Esta tarea es opcional. Cuánto suma a tu calificación lo anuncia tu profesor.
