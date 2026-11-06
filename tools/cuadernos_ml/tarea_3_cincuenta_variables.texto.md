<!--
Tipo: guion_notebook_tarea
Etiqueta: codex-red-c3-nbtarea
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_3 (sha256 5b6a9181)
Rama de origen: aprendizaje-maquina-clase-3-c@259fad6
Archivos permitidos: tools/cuadernos_ml/tarea_3_cincuenta_variables.texto.md

## Decisiones del registro que aplican

- D-005: lista negra del linter; se conserva la notación del curso.
- D-008: «Ningún plan, página, notebook, tarea ni objeto oficial lleva fechas de clase o de entrega.»
- D-009.1: se traduce la notación de las presentaciones a la del curso.
- D-009.5: «Toda cifra de una página o un enunciado sale de `ml_lab`/`tools/` y la ata una prueba.» No se anticipan resultados individuales.
- D-012: ejecución autorizada en el worktree; sin fusión ni push.
- D-013c-c3: se respetan la API ratificada y la apertura única de prueba con el procedimiento congelado.
- D-013c-c2: no se citan sus objetos en este guion.
- D-015: se usa la notación aditiva aceptada para la clase 3.

## Anatomía y formato

Las claves siguientes reproducen, en orden, los huecos de texto del código.
Portada presenta entrega y rúbrica; idea fija el problema.
Cada bloque pide predecir, leer una salida y escribir una entrega.
El ejercicio final pide transferencia; cierre recuerda qué entregar.
Las claves de código pertenecen al archivo Python.
Solo portada lleva un título de nivel 1; ninguna celda lleva encabezados de nivel 3.
El generador pone el badge y el arranque. No hay respuestas ni explicaciones desplegables.
-->

### celda: portada

# Tarea 3 · Cincuenta variables y una decisión defendible

Pertenece a [Clase 3 · Leer el error y regularizar](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/).
Duración: ~150 min en casa.

Se entrega el `.ipynb` por Canvas, con las celdas corridas.

Ejecuta primero la celda de arranque. Antes de correr cada bloque, escribe
tu predicción en su celda «Entrega». Después añade tus observaciones sin
borrar la predicción. Guarda las salidas y tus explicaciones en este notebook.
Ejecuta el bloque final solo cuando hayas congelado tu procedimiento.

La rúbrica suma 100 puntos:

| Bloque | Qué se evalúa | Puntos |
|---|---|---|
| 1 | Predicción concreta antes de experimentar | 10 |
| 2 | Benchmarks y diagnóstico con conjuntos identificados | 15 |
| 3 | Elección de regularización y justificación | 25 |
| 4 | Interpretación de coeficientes y gemela | 20 |
| 5 | Comparación de unidades sin estandarizar | 15 |
| 6 | Procedimiento congelado y lectura de prueba | 15 |

### celda: idea

Decidirás con 50 variables: pocas importan, sus escalas difieren y dos son casi idénticas.
Minimizas el objetivo penalizado $L_{\text{ent}}+\mu\,\Omega_1$, con $\mu\ge0$, sobre columnas estandarizadas.
Eliges $\mu$ por validación cruzada (*cross-validation*); abres prueba una sola vez, al final.
Cada número debe nombrar su conjunto. Se califica tu argumento, no acertar las cinco útiles.
Consulta [Leer el error y regularizar](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/).

### celda: bloque-1-predice

**Predice.** Sin estandarizar, ¿qué variables crees que lasso apagará primero, y por qué?

Considera columnas de escala chica, grande o sin un orden por escala.
Nombra variables concretas y registra tu predicción antes de ejecutar.
Escribe en `SEMILLA` los últimos cuatro dígitos de tu clave única.
Conserva esa semilla durante la tarea.

`J` fija 50 variables normales; `COEF` asigna efectos a `x1`…`x5`.
En unidades estándar son 3, −2, 1.5, 1 y 0.5, respectivamente.
La variable `x6` no entra en $f$; es gemela de `x1`, con correlación 0.95.
El ruido normal tiene $\sigma_\varepsilon=1$.

`ESCALAS` multiplica cada columna $x_j$ por `10.0 ** ((j % 10) - 4)`: las escalas van de $10^{-4}$ a $10^5$.
Para `x1` y `x2`, los factores son $10^{-3}$ y $10^{-2}$.
Hay $n=300$ observaciones: 180 de entrenamiento, 60 de validación y 60 de prueba.
La prueba permanece cerrada.

### celda: bloque-1-mira

**Mira.** En la matriz impresa, cada fila es una observación de entrenamiento; las columnas muestran la constante y las cinco variables útiles.
Debajo, compara las desviaciones de las columnas en `ent`: describen su escala observada, no el tamaño de su efecto.

### celda: entrega-1

**Entrega 1.** Escribe dos frases antes de correr el bloque: identifica qué variables esperas que lasso apague primero y justifica tu predicción.
Después añade una frase que cite las escalas observadas para esas variables.
Se califica que la predicción exista y pueda verificarse, no que acierte.

### celda: bloque-2-predice

**Predice.** Con 50 variables y 180 filas de entrenamiento, ¿esperas que $L_{\text{val}}$ de mínimos cuadrados quede cerca de $L_{\text{ent}}$ o muy por encima? ¿Le ganará a la media?

Registra ambas predicciones. Aquí $L$ es la pérdida cuadrática promedio, MSE;
su subíndice identifica el conjunto evaluado.
Los puntos de comparación (*benchmarks*) predicen siempre la media o la mediana calculadas en entrenamiento.
`mc` ajusta mínimos cuadrados con `COLUMNAS`, que incluye las 50 variables.

Aquí `val` todavía no eligió nada: el modelo y los benchmarks se fijaron con `ent`.
Por eso sirve como reserva para esta comparación pareada.
Dejará de serlo en el bloque 3: la validación cruzada usará entrenamiento ∪ validación para elegir.

### celda: bloque-2-mira

**Mira.** Compara `L_ent` con `L_val`; cada punto de los paneles laterales representa una observación de validación, y el histograma cuenta residuales.
El primer panel compara predicción y observación; el tercero, residual y `x1`. Las barras comparan RMSE y MAE en validación.
En la tabla, «cuadratica» es MSE; debajo aparece la diferencia pareada «mínimos cuadrados − media», con su error estándar, EE.

### celda: entrega-2

**Entrega 2.** Conserva tus predicciones y escribe una tabla más cuatro frases de análisis.
Anota $L_{\text{ent}}$, $L_{\text{val}}$ y los valores de ambos benchmarks en validación.
Cada cifra debe llevar el conjunto y la pérdida o métrica correspondiente.

En las frases, reporta la diferencia pareada y su EE en `val`.
Indica si el modelo le gana a la media por más de 2 EE y explica por qué esa reserva sirve aquí.
Propón una hipótesis sobre qué sobra o falta en el modelo, apoyada en las salidas.

### celda: bloque-3-predice

**Predice.** ¿La regla de un EE elegirá una $\mu$ mayor, menor o igual que la del mínimo de $\mathrm{CV}_5$, y con más o menos coeficientes distintos de cero?

Antes de correr, escribe el orden de simplicidad de tus candidatos.
Declara «$\mu$ de mayor a menor» y explica por qué ese es tu orden.
La línea `orden_complejidad=sorted(MUS, reverse=True)` lo comunica a `elegir`.
`MUS` contiene 16 valores entre $10^{-2}$ y $10$, en escala logarítmica.

Elige `REGLA = "minimo"` o `REGLA = "un_ee"` antes de ver la curva.
`PHI` estandariza dentro de cada ajuste de los cinco pliegues.
`sel` guarda la selección; `mu_hat`, el valor correspondiente a tu regla.
La penalización suma magnitudes de pendientes; excluye el intercepto $\beta_0$.

Para contrastar el número de coeficientes activos, usa la salida del bloque 4 con cada regla y `PENALIZACION = "l1"`.
Registra ambas corridas; después restaura tu regla declarada y ejecuta otra vez el bloque 3.
Termina esta comparación antes de abrir la prueba.

### celda: bloque-3-mira

**Mira.** Cada punto de la curva es la pérdida promedio de validación cruzada para una candidata; el eje horizontal muestra $\log_{10}\mu$.
Las barras muestran EE; la horizontal marca «mínimo + 1 EE». Compara el círculo del mínimo con el rombo de un EE.
Esas barras pertenecen a cada candidata: no son EE de diferencias entre modelos en validación cruzada.

### celda: entrega-3

**Entrega 3.** Conserva tu predicción y escribe cinco frases, más el lagrangeano del problema que resolviste, con su $\mu\ge0$.
Reporta las dos elecciones de $\mu$ y contrasta los coeficientes activos observados con tu predicción.
Repite el orden de simplicidad declarado antes de medir y justifícalo.
Indica qué regla usas y por qué; identifica el conjunto usado por $\mathrm{CV}_5$.

Si además comparas con la media mediante `diferencia_por_pliegue`, escribe solo «señal» o «sin señal».
No calcules un EE de esas diferencias ni afirmes que un modelo le gana al otro con CV.
La confirmación requiere una reserva que no haya elegido nada.

### celda: bloque-4-predice

**Predice.** De la pareja x1 y x6 (casi idénticas), ¿cuántas veces de 100 crees que lasso conserva las dos?

Anota una cantidad entre ninguna y todas, y justifica tu expectativa.
Primero ejecuta con `PENALIZACION = "l1"`; después cambia a `"elastica"` para probar la red elástica (*elastic net*).
Conserva `mu_hat` y compara ambas salidas.
Este cambio explora la interpretación; no sustituye el procedimiento lasso guardado en `sel`.

En las réplicas, cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.
El riesgo es la pérdida cuadrática esperada en esa población.

### celda: bloque-4-mira

**Mira.** Cada curva sigue una pendiente al variar $\mu$; la vertical marca `mu_hat` y la horizontal marca cero.
Contrasta «β̂» con «verdadero» y lee las frecuencias de `x1`, `x6` y ambas en 100 réplicas.
`UTILES` también resalta la gemela para compararla: que una curva tenga color no significa que su variable aparezca en $f$.

### celda: entrega-4

**Entrega 4.** Conserva tu predicción y escribe tres frases apoyadas en las salidas.
En la primera, explica por qué un cero estimado no equivale a un coeficiente verdadero cero.
En la segunda, describe qué ocurrió con la gemela y cita las frecuencias observadas.
En la tercera, explica si la red elástica cambió ese comportamiento al conservar la misma $\mu$.

### celda: bloque-5-predice

**Predice.** Si repites todo sin estandarizar, ¿qué útil crees que se apaga primero: la de escala más chica o la de escala más grande?

Elige una opción y nombra la variable que tienes en mente.
`crudos` conserva la rejilla `MUS`, la regla `REGLA` y los cinco pliegues.
Ahora ajusta con `COLUMNAS`, sin `estandarizar`.
`sel_crudo` guarda esa selección y `mu_crudo`, la regularización elegida.
El contraste sigue usando lasso, aunque hayas explorado la red elástica.

### celda: bloque-5-mira

**Mira.** Lee la $\mu$ impresa y compara las filas de «desviación de x», «β̂ en sus unidades» y «¿viva?».
Cada fila corresponde a una variable útil; contrasta sus ceros con el lasso estandarizado, atendiendo a las unidades de cada coeficiente.

### celda: entrega-5

**Entrega 5.** Conserva tu predicción y escribe tres frases más una cuenta de unidades.
Reporta qué cambió en la elección y qué variable útil se apagó, si ocurrió.
Explica cómo la escala de la columna modifica la pendiente necesaria para representar el mismo efecto.

La cuenta debe usar el factor de `ESCALAS` de esa variable y relacionarlo con su contribución a la penalización.
Si tu corrida difiere de la predicción, describe lo observado.

### celda: bloque-6-predice

**Predice.** ¿Tu $L_{\text{prueba}}$ quedará por encima o por debajo de tu $\mathrm{CV}_5$ del elegido, y por qué?

Anota tu expectativa antes de ejecutar. Deja fijados semilla, columnas,
estandarización, penalización, rejilla y regla de selección.
`final = sel.modelo_final` recupera el procedimiento del bloque 3, reajustado con entrenamiento ∪ validación.
El benchmark de la media también queda fijado con esos datos antes de evaluar prueba.

Abre la prueba una sola vez. Los bloques 4 y 5 fueron diagnósticos:
`sel_crudo` y la exploración elástica no sustituyen `sel.modelo_final`.
Después de esta celda no vuelvas a elegir ni ejecutes «correr todo».

### celda: bloque-6-mira

**Mira.** La primera línea imprime `L_prueba` y la media evaluadas en prueba; el margen tras «±» corresponde a 2 EE.
La segunda muestra la diferencia pareada «modelo − media» y su EE en prueba.
La línea rotulada «R» estima $R$ en el despliegue para ese mismo modelo; no es otra pérdida de validación cruzada.

### celda: entrega-6

**Entrega 6.** Conserva tu predicción y escribe cinco frases con cada conjunto identificado.
Declara el procedimiento congelado y reporta $L_{\text{prueba}}\pm\mathrm{EE}$; divide entre dos el margen impreso, rotulado «2 EE».
Reporta la pérdida del benchmark y la diferencia pareada con su EE en prueba.

Indica si el modelo le gana por más de 2 EE y compara $L_{\text{prueba}}$ con $R$ del despliegue.
Termina con una frase sobre qué habría pasado si hubieras elegido con la prueba.
No se vuelve a elegir.

### celda: ejercicio-nueva-regularizacion

Un experto no sabe si importa x1 o su gemela x6, pero está seguro de que, si importan, su efecto es parecido.
Plantea un lagrangeano que sume al de lasso un castigo por la **diferencia** entre los coeficientes de x1 y x6.
No lo resuelvas. Di cuántos multiplicadores y qué hiperparámetros tiene.
Describe qué esperas que pase con la pareja cuando el multiplicador nuevo crece sin límite.

### celda: cierre

Entrega este `.ipynb` corrido, con las predicciones originales, las seis entregas y tu planteamiento del ejercicio final.
Revisa que cada cifra nombre su conjunto y que la decisión congelada quede identificada antes de abrir la prueba.
Conserva sus salidas sin volver a ejecutar esa apertura.

Se entrega el `.ipynb` por Canvas, con las celdas corridas.
