### celda: portada

# Tarea 4 · Tres desenlaces y uno que importa

**¿Cómo evaluarás un modelo de crédito cuando el impago es poco frecuente?**

Al terminar tendrás:

- **Procedimiento:** justificarás tus métricas y dibujarás las reservas.
- **Comparación:** contrastarás representaciones y pesos con un punto de comparación (*benchmark*).
- **Diagnóstico:** relacionarás los aciertos por clase y la calibración con una decisión de crédito.
- **Conclusión:** reportarás la evaluación final con incertidumbre.

Consulta la [página de la tarea](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/clasificacion/tarea/).
Ejecuta primero el arranque. Antes de correr cada bloque, escribe tu predicción en una celda de texto.
Después conserva las salidas y escribe lo solicitado en «Entrega».

Se entrega el `.ipynb` por Canvas, con las celdas corridas.
Sobre la entrega: la fecha la da el profesor.

### celda: idea

Trabajas con crédito sintético y tres desenlaces: al corriente (0), atraso (1) e impago (2).
El uso previsto son los clientes del próximo trimestre, provenientes del mismo proceso.
Cada fila describe un cliente mediante `uso`, `atrasos_previos` e `ingreso`.
La celda inicial escribe las distribuciones y los puntajes que generan las etiquetas.

Lo que traes: softmax, pérdida logarítmica, aciertos, aciertos balanceados y MCC; también pesos de clase, calibración y predicción conformal.
Usarás validación cruzada (*cross-validation*) para seleccionar dentro del entrenamiento.
Distingue el objetivo que minimiza el ajuste, el criterio que selecciona candidatos y las cifras de evaluación.

### celda: bloque-1-predice

## 1 · Separa los usos de los datos

**Predice: ¿la clase más numerosa será la misma en todas las reservas visibles?**

Anota si esperas coincidencia en todas o alguna diferencia.
Fija `SEMILLA` y `CRITERIO` antes de ejecutar; conserva esa semilla durante la tarea.
Elige tu métrica principal y dos compañeras. Justifica su relación con el uso previsto antes de mirar resultados.

La primera celda construye las cinco reservas del mapa único de la página acompañante.
Primero aparta `cal` de `datos.val`; después divide el resto entre `val_a` y `val_b`.
Apartar `cal` desde el inicio impide que sus etiquetas orienten la selección o la decisión de recalibrar.
Su único uso posterior será fijar los cortes conformales, con el modelo congelado.

| Reserva | Uso autorizado | Límite |
|---|---|---|
| `datos.ent` | Ajusta parámetros y estandarización; selecciona representación, pesos y regularización mediante CV interna. | No incorpora validación ni prueba. |
| `cal` | Fija los cortes conformales por clase al final. | No participa en selección, benchmark ni diagnóstico. |
| `val_a` | Ajusta la recalibración y, si la modificas, la regla de decisión. | No evalúa la recalibración que ajustó. |
| `val_b` | Evalúa el benchmark, el diagnóstico por clase y las curvas de confiabilidad; permite decidir si recalibras. | No ajusta parámetros. |
| `datos.prueba` | Evalúa el procedimiento congelado una sola vez. | No decide ningún cambio. |

### celda: bloque-1-mira

Mira las barras horizontales: cada barra es una reserva visible y cada segmento cuenta clientes de una clase.
La prueba no aparece en la gráfica.
La celda colapsada imprime tamaños y conteos de `ent`, `cal`, `val_a` y `val_b`.
También comprueba que esas cuatro reservas no comparten índices; de la prueba solo informa el tamaño, sin abrirla.

Esta inspección inicial de la separación no autoriza a usar `cal` para comparar modelos.
Dibuja tu mapa con las cinco reservas y las operaciones que recibe cada una.

### celda: entrega-1

Escribe en **hasta 6 renglones** tu métrica principal y las dos compañeras, con su justificación.
Nombra por separado el objetivo de ajuste, el criterio de selección y la evaluación.
Añade el mapa de las cinco reservas, a mano e incorporado al notebook si lo prefieres.
Conserva también tu predicción inicial.

### celda: bloque-2-predice

## 2 · Establece el benchmark

**Predice: ¿moda y proporción quedarán ordenadas igual bajo los cuatro criterios?**

Anota si esperas el mismo orden, empates o diferencias según el criterio.
La celda ajusta ambos benchmarks en `datos.ent` y los evalúa **en `val_b`**, nunca en toda la validación.

La llamada declara los cuatro criterios: `"mcc"`, `"aciertos_balanceados"`, `"aciertos"` y `"logaritmica"`.
Son MCC, aciertos balanceados, aciertos y pérdida logarítmica.
El registro `USADOS["benchmarks"]` conserva el conjunto utilizado.

### celda: bloque-2-mira

Lee la tabla bajo «benchmark en val_b».
Localiza la moda y la proporción; identifica el criterio asociado a cada cifra antes de compararlas.
Para MCC, aciertos balanceados y aciertos, mayor es mejor; para pérdida logarítmica, menor es mejor.
Conserva la tabla para acompañar las comparaciones posteriores con el nombre del conjunto evaluado.

### celda: entrega-2

Entrega una tabla del benchmark en `val_b` con MCC, $A_{\text{bal}}$ —aciertos balanceados—, $A$ —aciertos— y pérdida logarítmica.
Pon los criterios en filas y los benchmarks en columnas.
Indica dónde se ajustaron y dónde se evaluaron.

### celda: bloque-3-predice

## 3 · Selecciona dentro del entrenamiento

**Predice: ¿cambiar `FORMA` modificará la combinación elegida de pesos y regularización?**

Anota si esperas que cambien los pesos, la regularización, ambos o ninguno.
Ejecuta con `FORMA = "lineal"` y conserva la tabla.
Cambia únicamente esa línea a `FORMA = "cuadrática"`, vuelve a ejecutar y conserva la segunda tabla.

Cada ejecución compara los cinco valores de `MUS`, sin pesos y con pesos balanceados, mediante CV estratificada con cinco pliegues.
`PHI` se estandariza dentro de cada pliegue.
La selección recibe `datos.ent`: pasar `datos` incorporaría las reservas de validación al ajuste.

Aquí $\mu$ es la fuerza de regularización, asociada al multiplicador de KKT; no es una distribución de Markov.
Aquí $k$ cuenta pliegues, no clases como en la unidad 6.
Los pesos de clase $w_y$ no son la cadena de computabilidad ni el valor de un hijo en juegos.

### celda: bloque-3-mira

Cada fila de la tabla corresponde a una combinación de pesos y `MU` para la `FORMA` indicada en el título.
Compara las dos tablas usando `CRITERIO`.
Lee la cifra de CV y su dispersión entre pliegues como descripción de esta partición.
La columna `ee` no demuestra que una opción gane; si quedan cerca, reconoce que falta evidencia.

Conserva ambas tablas en tu entrega. Vuelve a ejecutar el bloque con la forma que elijas antes de continuar.
Así `PHI`, `PESOS`, `MU` y `modelo` corresponderán a esa elección.
Declara cómo resolviste cualquier empate y conserva el orden de candidatos usado por la celda.

### celda: entrega-3

Escribe la representación, los pesos y `MU` elegidos, junto con `CRITERIO` y tu regla de desempate.
Reporta la cifra de CV y la dispersión que imprime la tabla, con su lectura descriptiva.
Apoya la elección en las dos tablas conservadas; identifica entrenamiento como la única reserva usada para seleccionar.

### celda: bloque-4-predice

## 4 · Compara los aciertos por clase

**Predice: ¿los pesos balanceados moverán los aciertos de todas las clases en la misma dirección?**

Anota si esperas aumentos comunes, descensos comunes o cambios distintos por clase.
La celda compara `None` y `"balanceado"` con la misma `PHI` y el mismo `MU` que dejaste seleccionados.
Ambos ajustes usan `datos.ent`; todo el diagnóstico se calcula en `val_b`.

### celda: bloque-4-mira

Cada panel corresponde a una opción de pesos.
La longitud de cada barra indica los aciertos de una clase; su grosor depende del soporte, el número de casos de esa clase.
Las líneas verticales señalan los promedios macro y ponderado.
Macro da igual importancia a cada clase; ponderado usa sus frecuencias observadas.

Relaciona las barras con los aciertos por clase y el MCC multiclase impresos bajo cada opción.
Los pesos del ajuste y la ponderación de este resumen son operaciones distintas.
Mantén el promedio ponderado como diagnóstico; no lo presentes como sustituto de tu evaluación principal.

### celda: entrega-4

Conserva la figura y describe un compromiso observado: qué clase ganó y cuál perdió al usar pesos balanceados.
Apóyate en los valores impresos y relaciona el cambio con macro, ponderado y MCC en `val_b`.
Si tu ejecución no muestra ese compromiso, describe lo observado sin inventarlo.

### celda: bloque-5-predice

## 5 · Relaciona calibración y precio

**¿cómo afectaría una mala calibración si tuvieras que fijar la tasa de interés con este modelo?**

Escribe tu predicción antes de ejecutar.
Anticipa si la tasa del cliente típico aumentará, disminuirá o quedará cerca al recalibrar; después contrasta con la salida.
`ml.recalibrar` ajusta en `val_a`. Las curvas antes y después se evalúan en `val_b`.

Simplificamos el precio a «impago contra el resto» en un solo periodo.
Prestas 1: si el cliente queda al corriente o con atraso, cobras $1+\text{tasa}$; si hay impago, cobras 0.
La tasa de equilibrio iguala el cobro esperado al monto prestado.
Con $\widehat p$ como probabilidad anunciada de impago, resulta $\text{tasa}=\widehat p/(1-\widehat p)$.

El «cliente típico» es fijo: `uso` de 0.5, sin atrasos previos e ingreso mediano de `datos.ent`.
La celda imprime su probabilidad de impago y su tasa antes y después de recalibrar.
Usa esas cifras para responder; esta simplificación no incorpora otros costos ni periodos.

### celda: bloque-5-mira

Cada panel compara una clase contra el resto.
Cada punto agrupa clientes con probabilidades anunciadas parecidas: horizontalmente muestra la probabilidad media; verticalmente, la frecuencia observada de esa clase.
Las curvas unen esos grupos antes y después de recalibrar. La diagonal señala coincidencia entre probabilidad y frecuencia.
Las barras verticales muestran dos errores estándar; las barras al pie indican tamaños relativos de los grupos.

Si elegiste pesos balanceados, la probabilidad de impago anunciada sale inflada y la recalibración la regresa hacia las frecuencias observadas.
Examina cuánto ocurre en tu ejecución; no tomes esa descripción como una cifra para el cliente típico.
Decide con las curvas de `val_b` si conservarás la recalibración.

La celda colapsada de comprobación revisa los conjuntos registrados en `USADOS`, incluido el benchmark.
Comprueba que ningún índice de `cal` ni de la prueba aparece en ellos.
Debe imprimir «cal y prueba intactas: 0 índices compartidos».
Si falla, revisa el procedimiento antes de avanzar; no omitas la comprobación.

### celda: entrega-5

Conserva la figura con las curvas antes y después.
Responde la pregunta del profesor con un número de tu cliente típico y explica qué representa.
Declara si conservarás la recalibración y sustenta la decisión en `val_b`.
Mantén visible el resultado de la comprobación de `USADOS`.

### celda: bloque-6-predice

## 6 · Evalúa el procedimiento congelado

**Predice: ¿tu métrica principal en prueba será mayor, menor o cercana a la observada en validación?**

Escribe la dirección esperada y qué interpretación cambiaría si la incertidumbre fuera grande.
Después fija `ETIQUETAS`, la regla que decide la clase, y `PROBABILIDADES`, el modelo que anuncia probabilidades.
Deja `recal` o elige `modelo` en `PROBABILIDADES`, según tu decisión del bloque anterior.
Fija también `DELTA` antes de abrir la prueba.

`DELTA` corresponde a $\delta$, probabilidad de fallar, con cobertura objetivo $1-\delta$; aquí no es la transición de computabilidad ni el error de Markov.
La tarea usa conformal por clase porque la separación estratificada fija cuotas: con el modelo congelado, se supone intercambiabilidad dentro de cada clase.

Congela representación, pesos, regularización, recalibración y regla de decisión.
Ejecuta después la celda colapsada «Abre la prueba, una vez».
Esa celda abre `datos.prueba` y usa `cal` para conformal por clase.
No regreses a cambiar elecciones después de ver sus resultados.

### celda: bloque-6-mira

Lee primero pérdida logarítmica y aciertos en la forma **valor $\pm2\,\mathrm{EE}$**.
Son promedios por caso; su error estándar es $s_\ell/\sqrt{n_{\text{prueba}}}$.
Aquí $s_\ell$ es la desviación estándar de las contribuciones individuales y $n_{\text{prueba}}$ cuenta las filas de prueba.

Para MCC y aciertos balanceados, conserva el valor y su intervalo de percentiles 2.5–97.5.
Escribe «bootstrap por filas» junto a cada intervalo: `estratificar=False` deja variar los conteos por clase entre réplicas.
Ambas formas de incertidumbre suponen filas independientes y describen cuánto podría moverse la cifra en otra prueba del mismo uso.
Ninguna condiciona en los conteos por clase.

La última tabla muestra la cobertura conformal por clase en prueba.
Si la comentas, acompáñala del supuesto condicionado en el modelo congelado.
Una cobertura observada en esta prueba no constituye por sí sola una garantía para cada muestra futura.

### celda: entrega-6

Reporta las cuatro cifras finales con sus formas de incertidumbre y el conjunto donde se midieron.
Concluye en **hasta 10 renglones**, apoyándote en tres figuras: reservas, diagnóstico por clase y curvas de confiabilidad.
Vincula la conclusión con tu objetivo inicial y con el benchmark, identificando que este se evaluó en `val_b`.
Explica las limitaciones de esa comparación entre conjuntos distintos.

### celda: cierre

Revisa que el notebook conserve tus predicciones, las entregas, ambas tablas de CV y las tres figuras citadas.
Comprueba que se pueda seguir qué reserva intervino en cada decisión y que las salidas correspondan al procedimiento congelado.
Guarda el archivo con las celdas corridas y entrégalo por Canvas.
