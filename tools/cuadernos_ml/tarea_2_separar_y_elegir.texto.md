<!--
Tipo: guion_notebook_tarea
Etiqueta: codex-red-c2-guion-tarea
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_2 (sha256 a764ccaf)
Rama de origen: aprendizaje-maquina-clase-2@9a0d9c8f4c48a34dcdf28b19eb974fc0d4d4b24e
Archivo permitido: tools/cuadernos_ml/tarea_2_separar_y_elegir.texto.md

Se aplica la anatomía de tarea: portada, idea, seis bloques con Predice,
Mira y Entrega, y cierre. El orden y las claves vienen del código.
El generador aporta el arranque y el badge.
-->

### celda: portada

# Tarea 2 · Separar, elegir y reportar

**¿Cómo elegirás un grado y reportarás su error sin gastar la prueba en la decisión?**

Duración de trabajo: aproximadamente 120 min.
Acompaña la página [Tarea 2 · Separar, elegir y reportar](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/tarea/).

Al terminar tendrás:

- **Separación:** justificarás la reserva con el contrato de uso.
- **Selección:** dejarás tus apuestas y la regla que elegiste antes de medir.
- **Reporte:** compararás el modelo y el benchmark en la misma prueba.
- **Auditoría:** examinarás los pliegues y medirás el engaño de elegir con la prueba.

Se entrega el `.ipynb` por Canvas, con las celdas corridas.
Completa las seis celdas `entrega-<k>`. La fecha la da el profesor.

> **Colab:** guarda una copia propia y ejecuta primero la celda de arranque.
> Después avanza por bloques; escribe cada predicción antes de ejecutar su código.

En el bloque 1, sustituye el cero de `SEMILLA` por los últimos cuatro dígitos
de tu clave única. Si comienzan con ceros, escribe el entero sin esos ceros.
Conserva esa semilla durante la tarea; no busques una que dé mejores resultados.

Al editar `SEMILLA`, cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

### celda: idea

Reservar la prueba significa guardar entregas para evaluar una decisión ya
tomada. El contrato es iid: «se usará con entregas nuevas de esta misma ciudad,
sacadas igual que la muestra». El proceso tiene ruido independiente entre
entregas e independiente de la distancia. No incluye tiempo ni cliente.

Aquí $x$ es la distancia en kilómetros y $y$ es el tiempo en minutos.
El código genera $n=150$ entregas con $y=f(x)+\varepsilon$,
$f(x)=10+12/x$, $x\sim U(1,5)$ y $\varepsilon\sim\mathcal N(0,2^2)$.
La función $f$ es estructural; $\varepsilon$ es ruido, no la cadena vacía.

Usarás pérdida cuadrática: $L$ es la pérdida promedio, no un lenguaje.
Sus unidades son minutos². La validación cruzada (*cross-validation*) ayudará
a elegir el grado; la prueba estimará el riesgo del ajuste elegido.
El *benchmark* es «la media de entrenamiento como punto de comparación; la clase 3 lo define».
Repasa [Entrenamiento y prueba](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/entrenamiento-y-prueba/)
y [Validación cruzada](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/validacion-cruzada/).

### celda: bloque-1-predice

## 1 · Justifica la separación

**Predice.** ¿Qué tan ancho esperas el intervalo $\pm2\,\mathrm{EE}$ de la prueba con 30 entregas, comparado con el de una prueba de 120?
Apuesta la razón entre el ancho con 30 entregas y el ancho con 120.

Escribe tu apuesta numérica en `entrega-1` antes de correr el bloque.
Pon tu `SEMILLA` y conserva `fracciones=(0.8, 0, 0.2)`.
El desarrollo está en `datos.ent`; dentro de él se harán los pliegues para elegir.
La reserva de prueba queda aparte.

### celda: bloque-1-mira

**Mira.** Cada punto de la nube es una entrega de desarrollo: distancia horizontal y tiempo vertical.
La leyenda dice «desarrollo»; el renglón impreso da los tamaños de desarrollo y prueba.
La figura oculta $f$ y muestra solo desarrollo a propósito: la prueba queda cerrada hasta el bloque 4.

### celda: entrega-1

**Entrega 1.** Escribe aquí tu apuesta sobre la razón entre los anchos de los intervalos y, después de correr, los tamaños observados de desarrollo y prueba.
En dos renglones, justifica por qué separar al azar imita este contrato de uso.
No basta decir que el azar «es más justo».

En otros dos renglones, responde la transferencia sin calcular:
«Si el contrato fuera *el mes que viene* o *clientes nuevos*, ¿qué columna necesitarías y cómo separarías?».
No supongas que esas columnas ya existen.

### celda: bloque-2-predice

## 2 · Apuesta antes de mirar

**Predice.** ¿Qué tres números apostarías para el grado que elegirá la CV, la diferencia $L_{\text{prueba}}$ del modelo final menos la del benchmark y la $\mathrm{CV}_5$ del grado 12?

Sustituye los tres `None` de `MIS_APUESTAS` por números antes de continuar.
Escribe la diferencia con signo y la $\mathrm{CV}_5$ del grado 12 en minutos².
Aclara si tu apuesta de grado corresponde al mínimo o a un error estándar (EE).
Todavía no ejecutes el bloque 3 ni abras la prueba.

### celda: bloque-2-mira

**Mira.** Cada renglón reproduce una entrada de `MIS_APUESTAS`; aquí no hay una gráfica ni errores medidos.
Comprueba que los tres renglones contienen números y que desapareció «¡falta tu apuesta!».
Corresponden al grado que elegirá la CV, a la diferencia $L_{\text{prueba}}$ del modelo final menos la del benchmark y a la $\mathrm{CV}_5$ del grado 12; las dos últimas apuestas están en minutos².
Conserva esta salida para contrastarla con los bloques 3 y 4.

### celda: entrega-2

**Entrega 2.** Copia tus tres apuestas originales: el grado que elegirá la CV, la diferencia $L_{\text{prueba}}$ del modelo final menos la del benchmark y la $\mathrm{CV}_5$ del grado 12.
Anota la regla a la que corresponde el grado apostado y expresa las otras dos apuestas en minutos².
Explica en una frase qué significa el signo de tu diferencia para la comparación con el benchmark.
No corrijas las apuestas después de ver los resultados.

### celda: bloque-3-predice

## 3 · Declara la regla y elige el grado

**Predice.** ¿Qué grado numérico esperas que seleccione cada regla: mínimo y un EE?

Anota ambas apuestas en `entrega-3`.
Antes de medir, conserva `ORDEN` de simple a complejo y fija `REGLA`
como `"minimo"` o `"un_ee"`. Los candidatos van del grado 0 al 12.
Declara cuál usarás, aunque las dos reglas terminen eligiendo el mismo grado.

La llamada `elegir(..., con="cv", k=5)` mide dentro del desarrollo y muestra
las dos elecciones en una corrida. Aquí $k$ cuenta pliegues, no estados,
simulaciones ni clases. Con empate, el más simple: el menor $N$.
El grado es el hiperparámetro; los parámetros del polinomio se ajustan en cada entrenamiento.

### celda: bloque-3-mira

**Mira.** Cada punto es un grado; su altura es la CV y su barra representa un EE.
La tabla da `candidato`, `valor` y `ee`; la línea punteada marca «mínimo + 1 EE».
Los símbolos destacados ubican ambas elecciones; `N_hat` indica la que usarás.

El grado 0 es el benchmark. Mira su fila en la tabla y el renglón que imprime su CV ± EE.

Las barras no son intervalos de confianza exactos. La CV da una señal para
elegir; no demuestra que el modelo le gane al benchmark.
Las pérdidas fuera de pliegue dependen entre sí.

### celda: entrega-3

**Entrega 3.** Conserva la tabla impresa y registra tus dos apuestas,
`ORDEN` y la `REGLA` declarada antes de correr.
Escribe el grado de cada regla y el `N_hat` que usarás.
Justifica tu elección con la regla declarada, la CV y su EE.

Describe lo que ocurrió con tu semilla; no lo presentes como una ley
para cualquier muestra.

### celda: bloque-4-predice

## 4 · Abre la prueba y reporta

**Predice.** ¿Cuánto esperas que valga en prueba la diferencia «modelo menos benchmark», en minutos²?

Anota un número con signo en `entrega-4`; puede ser negativo, cero o positivo.
El modelo ya está fijado: `sel.modelo_final` está reajustado con todo el desarrollo.
El benchmark también queda fijado con ese desarrollo.
Ejecuta esta celda una sola vez y conserva su salida.
Esta es la única vez que abres tu reserva de prueba.

### celda: bloque-4-mira

**Mira.** Los primeros renglones comparan modelo y benchmark en la misma prueba; cada «±» muestra dos EE.
El último renglón da la diferencia pareada `d` y su EE, `ee`, calculados con las mismas entregas.
La decisión impresa usa `d + 2 * ee < 0`.

El EE resume la incertidumbre del promedio de pérdidas; no mide el error
de una predicción individual. La prueba estima el riesgo bajo el contrato
de uso; su pérdida observada no es el riesgo exacto.

### celda: entrega-4

**Entrega 4.** Conserva tu apuesta y completa el reporte con los valores impresos:

«Para [contrato], el error esperado es … ± … minutos², contra … del benchmark;
la diferencia pareada es … ± …».
En el primer margen usa dos EE; en el de la diferencia, identifica que reportas su EE.
Ambos errores se miden en prueba. La diferencia también se expresa en minutos².

Indica si puedes decir «le gana al benchmark por más de dos EE».
Usa el EE de la diferencia pareada de pérdidas y el criterio impreso.
Si no se cumple, escribe que falta evidencia con esta prueba.
No uses la CV ni compares por separado las barras de los dos modelos.

La conclusión corresponde a los dos modelos ya fijados y a esta reserva,
que no intervino en ninguna decisión. Conserva grado, regla y reporte
durante la auditoría y el experimento final.

### celda: bloque-5-predice

## 5 · Audita los pliegues

**Predice.** Con cinco pliegues, ¿cuántos esperas ver claramente separados de los demás para el grado 8?

Apuesta un número en `entrega-5` antes de ejecutar.
La celda añade dos entregas lejanas a una copia del desarrollo llamada `auditar`.
Observa esa intervención y compara las salidas para `k=3`, `k=5` y `k=20`.
Este experimento no vuelve a elegir tu modelo final.

### celda: bloque-5-mira

**Mira.** En cada gráfico, un triángulo es la pérdida promedio de un pliegue para un grado; la raya es la media entre pliegues.
Compara los grados 0, 1, 4 y 8; el grado 0 es el benchmark.
La etiqueta señala un pliegue alejado de los otros.
El eje vertical usa escala logarítmica: lee los valores, no solo las distancias.

El título cuenta «13·k + 1 ajustes para 13 grados»: seleccionar entre los 13 grados con $k$ pliegues y reajustar el elegido.
La figura muestra solo cuatro grados; esta auditoría no hace ese reajuste.
Las dos entregas lejanas no se fijan a un mismo pliegue.
Usa las etiquetas para investigar en cuál o cuáles se concentra el error.

### celda: entrega-5

**Entrega 5.** Contrasta tu apuesta con la figura e identifica qué cambió
la celda en el desarrollo. Explica cómo esa intervención puede producir
las pérdidas que observas. No atribuyas automáticamente toda separación
entre triángulos a la misma causa.

Compara los tres valores de $k$ en costo, sesgo y ruido de la estimación.
Distingue el tamaño usado para entrenar del tamaño de cada pliegue reservado.
Separa lo que muestran tus figuras de las tendencias que esperarías al repetir.
No afirmes que aumentar $k$ siempre reduce el ruido.

### celda: bloque-6-predice

## 6 · Elige con la prueba para medir cuánto te habrías engañado

**Predice.** Tras 200 repeticiones, ¿cuánto esperas que valga el promedio de «anunciado menos real», en minutos²?

Escribe un número con signo en `entrega-6` antes de correr.
Esta celda elige deliberadamente el menor error de prueba en muestras nuevas.
El «visor de la realidad» usa `datos.despliegue` para aproximar el riesgo
del elegido; solo existe en el simulador.

La fábrica de este experimento usa `fracciones=(0.6, 0.2, 0.2)`.
Compara `L_prueba` y `R` del mismo ajuste de cada repetición.
No reemplaza el reporte del bloque 4 ni repite la selección por CV del bloque 3.

### celda: bloque-6-mira

**Mira.** Cada barra del histograma agrupa repeticiones según su diferencia «anunciado − real»; la línea de referencia está en cero.
Una diferencia negativa significa que se anunció menos error que el riesgo aproximado por el visor.
El renglón «sesgo medio eligiendo con la prueba» resume esa diferencia y su EE de Monte Carlo.

Ese EE describe la precisión del promedio entre repeticiones; no es
el EE pareado de tu reporte. El visor aproxima $R$ con una muestra grande,
no lo conoce de manera exacta.

Aquí mides el sesgo de elegir con la prueba, no el error de un modelo;
por eso esta salida no lleva benchmark.

### celda: entrega-6

**Entrega 6.** Escribe tu apuesta, el sesgo medio observado y el EE de
Monte Carlo, con sus unidades y el rótulo «anunciado menos real».
Explica en dos renglones el resultado usando la palabra «mínimo».
Distingue elegir con la prueba de evaluar una elección ya fijada.

### celda: cierre

Antes de entregar, revisa que las seis celdas de entrega estén llenas.
Deben conservarse las apuestas originales, la tabla de CV, la regla declarada
y el reporte de prueba. No se califica que todos obtengan el mismo grado.

La rúbrica suma 10 puntos:

| Evidencia | Puntos |
|---|---:|
| Separación justificada y transferencia a tiempo y clientes | 2 |
| Predicciones escritas antes de correr | 1 |
| Selección trazable con regla declarada | 2 |
| Reporte con EE, benchmark, alcance y comparación pareada en prueba | 2 |
| Auditoría del pliegue y de los valores de k | 1.5 |
| Engaño medido y explicado | 1.5 |

**Punto de control:** tu conclusión sobre el benchmark debe salir de la
diferencia pareada en prueba. Las decisiones anteriores deben poder
reconstruirse sin mirar esa reserva.

Te llevas un procedimiento: declarar el uso, separar, apostar, elegir y
reportar. Queda una pregunta para seguir: ¿qué cambiarías en ese procedimiento
si las entregas nuevas dejaran de parecerse a la muestra?
