### celda: portada

# Tarea 5b · Una victoria sospechosa (la separación mal hecha es la de un compañero; tu prueba está sellada)

Duración aproximada: 90 minutos.

Auditarás una evaluación de reingreso hospitalario en 30 días. Hay al menos tres fugas en el procedimiento del compañero.

Al terminar tendrás:

- **Diagnóstico:** dibujarás las rutas sospechadas y reunirás evidencia con los detectores.
- **Procedimiento:** compararás tus arreglos y construirás una tubería evaluada por pacientes.
- **Conclusión:** reportarás la evaluación final y la comparación con incertidumbre.

Ejecuta primero el arranque. Escribe cada predicción antes de correr las celdas del bloque; en B1 solo leerás el código visible.
Conserva las salidas y escribe lo solicitado en cada entrega.

Se entrega el `.ipynb` por Canvas, con las celdas corridas.

La celda que genera los datos está colapsada y marcada «no la abras hasta entregar».
El repositorio es público; nada depende de que esa celda esté oculta.
Mantén `prueba_sellada` cerrada hasta B5.

### celda: idea

Una cifra demasiado buena se audita antes de creerla; la prueba que no tocaste es la única que puede decidir si lo era.

Trabajas con visitas hospitalarias, fechas y pacientes que pueden aparecer en varias visitas.
El objetivo es predecir si habrá reingreso en 30 días. La proporción de reingresos ronda el 15 %.
`desarrollo` contiene las visitas de unos 800 pacientes; ahí diagnosticas, comparas y eliges.
La prueba sellada corresponde a unos 200 pacientes distintos.

La decisión de alertar se toma al dar de alta, por visita. Cada visita tiene el mismo peso en la evaluación.
El MCC es la métrica principal; lo acompañan los aciertos balanceados, $A_{\text{bal}}$. Para ambas métricas, mayor es mejor.
Cada cifra debe nombrar su conjunto y su punto de comparación (*benchmark*).

Lo que traes: MCC, aciertos balanceados, pesos de clase y validación cruzada (*cross-validation*, CV).
Usarás el diagnóstico de fuga (*leakage*) para decidir qué debe corregirse en la tubería (*pipeline*).

### celda: bloque-1-predice

## 1 · Examina la victoria sospechosa

**Predice:** «Tu compañero reporta un MCC de {cifra que imprime la celda} en su validación para predecir reingresos. Sin abrir nada, ¿te parece creíble? ¿Por qué?»

Ayuda: **propio**. Lee el código visible del compañero, incluida su tubería y su separación.
Dibuja la ruta de cada fuga que sospeches. No corras ninguna evaluación en este bloque.
La generación de datos sigue colapsada.

### celda: bloque-1-mira

Mira qué datos recibe cada operación del código visible y cómo llegan hasta la cifra reportada.
Sigue las rutas que sospechas y ubícalas entre las rutas 1–4 de `ml-c5-def-fuga`.
Conserva el dibujo y tu predicción del efecto de cada arreglo para contrastarlos después.

### celda: entrega-1

rutas sospechadas (1–4 de `ml-c5-def-fuga`) y qué efecto predice al arreglar cada una

### celda: bloque-2-predice

## 2 · Reúne evidencia con los detectores

**Predice:** «Si una sola columna explica casi todo, ¿qué esperas ver al revolverla?»

Ayuda: **dado**. Cada detector está en su propia celda y corre tal cual.
Ejecuta `importancia` en la validación del compañero.
Ejecuta `validacion_adversarial` entre su entrenamiento y su validación, con `particion` por pacientes.
Revisa también los conteos de pacientes y visitas duplicadas que aparecen en ambos lados.

### celda: bloque-2-mira

Mira la salida de `importancia` por columna y el resultado de la validación adversarial frente a su benchmark.
Lee por separado el conteo de pacientes compartidos y el de visitas duplicadas.
Relaciona cada señal con tus rutas sospechadas de B1. Registra también los límites de lo que estos detectores permiten concluir.

### celda: entrega-2

qué detector señaló qué, y qué no puede ver ninguno

### celda: bloque-3-predice

## 3 · Repara una cosa a la vez

**Predice:** «De tus arreglos, ¿cuál crees que baja más el MCC de la validación cruzada?»

Ayuda para la partición: **dado**. Usa los cinco pliegues por pacientes y estratificados de `pliegues(desarrollo, k=5, como="grupo", estratificar=True)`.
Ayuda para los arreglos: **propio**. Escribe cada arreglo en su celda y mídelo con esa misma partición sobre `desarrollo`.
La fila dada ya junta varios arreglos (sin la columna posterior, sin copias, por pacientes, imputando dentro del pliegue): úsala como base y cambia una sola cosa por fila a partir de ella.
Conserva el benchmark para comparar los resultados.

### celda: bloque-3-mira

Mira el MCC de cada pliegue para cada arreglo. Resume esos valores con la mediana y el rango entre pliegues.
Pon el benchmark junto a cada comparación e identifica qué cambiaste entre las filas de tu tabla.
Contrasta el orden observado con tu predicción inicial.

La dispersión entre pliegues es descriptiva. Ese rango no es un intervalo de incertidumbre ni demuestra por sí solo que un procedimiento sea mejor.

### celda: entrega-3

tabla «arreglo → MCC de CV (mediana y rango entre pliegues, descriptivo)» con el benchmark

### celda: bloque-4-predice

## 4 · Construye la tubería

**Predice:** «Con todo lo que se ajusta dentro del pliegue, ¿la CV queda cerca del benchmark, cerca de la cifra del compañero o en medio?»

Ayuda: **a completar**. Completa `tuberia(____, modelo={"familia": "logistica", "pesos": "balanceado"})` con los pasos que pide tu diagnóstico.
Consulta la lista de pasos disponibles en el docstring. Evalúa la tubería con la partición por pacientes de B3.

Los pesos balanceados se recalculan dentro de cada pliegue, usando solo sus filas de ajuste.
El umbral queda fijo desde el inicio en $\tau=0.5$.
Aquí $\tau$ es el umbral de clasificación, no el tablero de juegos ni un tiempo de llegada de Markov.

Esta tarea no elige el umbral, no recalibra y no usa predicción conformal. Por eso no aparta reservas de calibración.
Usar pesos también permite elegir otro umbral en validación; hacerlo requeriría `val_a` dentro de `desarrollo`.
Conserva las elecciones de esta tarea para el reajuste final.

### celda: bloque-4-mira

Mira la CV de la tubería completa junto al benchmark y la cifra de validación del compañero.
Identifica dónde se ajusta cada paso y qué filas puede usar.
Apoya tu explicación en ese recorrido y en tu diagnóstico, además de la cifra obtenida.

### celda: entrega-4

la CV limpia y por qué ahora sí es creíble

### celda: bloque-5-predice

## 5 · Abre la prueba sellada una vez

**Predice:** «¿Tu MCC en la prueba sellada quedará dentro del rango de tu CV por pacientes?»

Fija todo antes de continuar. Ayuda para la línea que reajusta, `bloque-5-juega`: **a completar**.
Reajusta el procedimiento elegido con todo `desarrollo`; no hay reservas de calibración que conservar en esta tarea.

Ayuda para la evaluación: **dado**. La celda siguiente, `bloque-5-prueba`, abre `prueba_sellada` una vez, con ambos modelos ya fijos.
Evalúa tu modelo y el del compañero, junto al benchmark, con MCC y $A_{\text{bal}}$.
Después de abrirla, no cambies el procedimiento ni elijas otro arreglo.

No reportamos la pérdida logarítmica: con pesos y sin recalibrar, las probabilidades salen corridas a propósito, y esa pérdida mediría ese corrimiento más que el modelo.

### celda: bloque-5-mira

Lee el MCC y los aciertos balanceados de ambos modelos en la prueba sellada, junto al benchmark.
Para el MCC final, conserva el valor y el intervalo de percentiles 2.5–97.5 que entrega `incertidumbre`.
La llamada usa `grupo="grupo"` y `repeticiones=1000`: remuestrea pacientes completos.
Conserva también `Incertidumbre.esquema` y escribe «remuestreando pacientes» junto al intervalo.

En la tarea 4 se remuestreaban filas, sin estratificar, porque eran independientes; aquí la unidad independiente es el paciente.
Cambia la unidad remuestreada: las visitas de un paciente permanecen juntas. Esta tarea tampoco estratifica el remuestreo.
La evaluación sigue dando el mismo peso a cada visita.

Distingue las dos comparaciones finales:

- (i) Optimismo: resta al MCC reportado en la validación del compañero el MCC de su mismo modelo en la prueba sellada.
- (ii) Comparación de procedimientos: resta al MCC de tu modelo el MCC del compañero, ambos en la prueba sellada.

Para (ii), conserva el intervalo pareado de `incertidumbre` con `contra=modelo_compa` y `grupo="grupo"`.
Cada remuestreo evalúa ambos modelos sobre los mismos pacientes. Reporta la diferencia con su intervalo de percentiles 2.5–97.5 y el esquema en palabras.

No uses `error_estandar` por visita: el MCC no es un promedio de pérdidas por fila y las visitas de un paciente son dependientes.
El rango de CV de B3 sigue siendo descriptivo, aunque lo compares con la cifra final.

### celda: entrega-5

el número final con su intervalo, el optimismo (i) y la comparación (ii)

### celda: cierre

La rúbrica por bloques es:

| Bloque | Peso |
|---|---:|
| B1 · La victoria sospechosa | 15 % |
| B2 · Detecta | 15 % |
| B3 · Repara una cosa a la vez | 25 % |
| B4 · La tubería | 20 % |
| B5 · Abre la prueba sellada una vez | 25 % |

Pierdes B5 entero si abres `prueba_sellada` antes de B5 o la usas para decidir un arreglo.
La cifra final de MCC y la diferencia (ii) deben llevar valor, intervalo de percentiles 2.5–97.5 y «remuestreando pacientes».
Un $\pm2\,\mathrm{EE}$ por visita no cuenta.

Revisa que conserves tus predicciones, las cinco entregas y las salidas que sustentan cada comparación.
Cada número debe identificar su conjunto y su benchmark. Deja dicho que abriste la prueba una sola vez, con todo fijado.
