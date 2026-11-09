---
id: ml-tareas-5
title: "Tarea de la clase 5 · Series, fugas y otras familias"
nav_title: "Tarea"
summary: "Dos notebooks obligatorios (validación cruzada con series de tiempo; encontrar y arreglar fugas) y uno opcional (árbol, bosque y boosting con la misma validación). Se entregan los .ipynb por Canvas."
status: ready
estimated_time: 165m
tags: [aprendizaje-maquina, tarea, series-de-tiempo, fugas]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 5a · Series de tiempo** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5a_series_de_tiempo.ipynb)
>
> **[👉 Abrir `tarea_5a_series_de_tiempo.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5a_series_de_tiempo.ipynb)**

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 5b · Una victoria sospechosa (la separación mal hecha es la de un compañero; tu prueba está sellada)** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5b_fugas.ipynb)
>
> **[👉 Abrir `tarea_5b_fugas.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5b_fugas.ipynb)**

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 5c · Otras familias (opcional)** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5c_otras_familias.ipynb)
>
> **[👉 Abrir `tarea_5c_otras_familias.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5c_otras_familias.ipynb)**

# Tarea de la clase 5 · Series, fugas y otras familias

**¿Qué evidencia necesitas para confiar en una evaluación de entregas o de reingresos hospitalarios?**

En estas tareas compararás evaluaciones, revisarás cómo se obtuvieron y justificarás cuál corresponde al uso previsto.
Las tareas 5a y 5b son obligatorias: aproximadamente 165 minutos en total.
La 5c es opcional y requiere unos 45 minutos adicionales.

> [!WARNING]
> Se entrega el `.ipynb` por Canvas; la fecha la da el profesor.
> Entrega cada notebook con las celdas corridas, sus salidas y tus explicaciones.

Al terminar tendrás:

- **Una comparación temporal:** explicarás cuándo cambia la promesa de error al cambiar los pliegues.
- **Una auditoría:** documentarás tus sospechas, tus arreglos y la evaluación con la prueba sellada.
- **Una comparación opcional:** elegirás entre árbol, bosque y boosting con la misma validación.

> [!TIP]
> **Míralo correr: las tareas de la clase 5**
>
> 5a · Series de tiempo:
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5a_series_de_tiempo.ipynb)
>
> 5b · Una victoria sospechosa:
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5b_fugas.ipynb)
>
> 5c · Otras familias, opcional:
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5c_otras_familias.ipynb)

> **Lo que traes**
>
> Usarás validación cruzada (*cross-validation*, CV) y un punto de comparación (*benchmark*).
>
> Revisarás las rutas de fuga (*leakage*) y la tubería (*pipeline*) de [[ml-son-iid-y-fugas|¿Son iid? Fugas]].
>
> Aplicarás la elección con validación de [[ml-la-metodologia|La metodología]].

Escribe cada predicción antes de ejecutar su bloque. Después conserva las salidas y responde lo solicitado en «Entrega».
En B1 de la tarea 5b solo lees el código y planteas tus sospechas; todavía no corres evaluaciones.

La celda que genera los datos está colapsada y marcada «no la abras hasta entregar».
El repositorio es público y nada depende de que esté oculta.

## 1 · Series de tiempo

Tiempo aproximado: 75 minutos. Compararás la CV al azar y la temporal para pronosticar minutos promedio de entrega.

> [!TIP]
> **Míralo correr: tarea 5a · Series de tiempo, bloques B1–B5**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5a_series_de_tiempo.ipynb)

Trabajarás con una sola serie de 720 días. Los días 1–600 son tu historia; los días 601–720 son el despliegue.
El despliegue continúa la misma serie. No es otra muestra.

Al cierre del día $t$ predecirás los minutos promedio del día siguiente.
Conoces el calendario de mañana, la lluvia de hoy y los minutos de entrega de hoy y de días anteriores.
No conoces la lluvia de mañana.

Los parámetros se ajustan al inicio de cada bloque de validación y quedan fijos dentro del bloque.
Para el despliegue, se ajustan al cierre del día 600.
Las entradas sí se actualizan cada día. Este protocolo vale tanto para los candidatos como para el benchmark.

La CV temporal tiene 5 cortes, con bloques de 100 días y hueco 0: el primer ajuste usa los días 1–100 y valida con los 101–200.
Si agregas un promedio móvil, calcúlalo solo con días ya cerrados; como predices un día adelante, el hueco sigue en 0.
La CV al azar usa los mismos 600 días en 5 pliegues, con las mismas entradas.

Compararás un modelo lineal, vecinos y un bosque (*random forest*).
El lineal usa el día de la semana con dummies y la lluvia de hoy.
Vecinos y bosque también usan el tiempo.
Tu benchmark será «el valor de ayer», evaluado con el mismo protocolo.

### Qué haces y qué entregas

| Bloque | Trabajo y entrega | Peso |
|---|---|---:|
| B1 · Qué se sabe al predecir | Llena la tabla «columna · ¿se conoce al emitir?». Entrega la tabla y tu predicción inicial. | 10 % |
| B2 · Los cortes | Examina ambas particiones. Entrega qué días ve cada iteración y la fracción de días de validación cuyo día anterior está en entrenamiento. | 10 % |
| B3 · Las promesas | Compara los tres candidatos y el benchmark. Entrega una tabla 4 × 2 con ambas CV; nombra el conjunto de cada cifra. | 25 % |
| B4 · Pasado y futuro | Elige con la historia y evalúa en los días 601–720. Entrega cuánto mentía cada CV, en veces, para cada candidato. | 25 % |
| B5 · Cuándo no miente | Compara los escenarios con y sin memoria, y con y sin deriva. Entrega tu explicación de ambos efectos, incluido el caso en que la diferencia es chica. | 30 % |

En B1 escribes tu clasificación. En B2 completas el conteo; en B3, el benchmark; en B4, la partición para elegir.
El código para dibujar, evaluar y comparar los escenarios está dado.
Usa los residuales contra el tiempo y la autocorrelación para sustentar B5.

Rotula la evaluación final «error en los días 601–720».
Al expresar una relación en veces, identifica qué cantidad divides entre cuál.
Las comparaciones de CV son descriptivas.
Se califica que expliques **cuándo y por qué** cambia la promesa de error, no un número exacto.

## 2 · Fugas

Tiempo aproximado: 90 minutos.
Auditarás una evaluación de reingreso hospitalario en 30 días.
El procedimiento del compañero contiene al menos tres fugas; te toca encontrarlas y justificar los arreglos.

> [!TIP]
> **Míralo correr: tarea 5b · Una victoria sospechosa, bloques B1–B5**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5b_fugas.ipynb)

El notebook se titula «Tarea 5b · Una victoria sospechosa (la separación mal hecha es la de un compañero; tu prueba está sellada)».
Trabajarás con pacientes que pueden tener varias visitas, cada una con su fecha.
La proporción de reingresos ronda el 15 %.

Desarrollo contiene las visitas de unos 800 pacientes.
La prueba sellada contiene las de unos 200 pacientes distintos, apartados por paciente antes de todo.
Diagnostica, compara y elige usando solo desarrollo.

La decisión de alertar se toma por visita, al dar de alta.
Cada visita tiene el mismo peso en la evaluación.
Reporta MCC como métrica principal y aciertos balanceados como acompañamiento, siempre con su conjunto y benchmark.

### Qué haces y qué entregas

| Bloque | Trabajo y entrega | Peso |
|---|---|---:|
| B1 · La victoria sospechosa | Lee el procedimiento del compañero sin correr evaluaciones. Entrega las rutas que sospechas y el efecto que predices para cada arreglo. | 15 % |
| B2 · Detecta | Ejecuta los detectores dados. Entrega qué señaló cada uno y qué no puede ver ninguno. | 15 % |
| B3 · Repara una cosa a la vez | Escribe y compara tus arreglos. Entrega la tabla «arreglo → MCC de CV», con mediana, rango entre pliegues y benchmark. | 25 % |
| B4 · La tubería | Completa los pasos que pide tu diagnóstico. Entrega la CV limpia y explica por qué ahora sí es creíble. | 20 % |
| B5 · La prueba sellada | Fija todo y completa el reajuste con desarrollo. Abre la prueba una vez. Entrega las métricas finales, sus intervalos y las dos comparaciones descritas abajo. | 25 % |

La partición de B3 está dada: 5 pliegues por pacientes y estratificados.
Usa la misma partición para comparar los arreglos y para evaluar la tubería de B4.
La mediana y el rango entre pliegues describen la CV; ese rango no es un intervalo de incertidumbre.

El modelo usa pesos balanceados, recalculados solo con las filas de ajuste de cada pliegue.
El umbral está fijo en 0.5 desde el inicio.
Esta tarea no elige el umbral, no recalibra ni usa predicción conformal.
Por eso el reajuste final utiliza todo desarrollo, sin reservas de calibración.

### Qué reportas al abrir la prueba

Evalúa tu modelo y el del compañero en la misma apertura, con ambos procedimientos ya fijados.
Reporta MCC y aciertos balanceados con sus intervalos por pacientes.
Incluye el benchmark. No reportes pérdida logarítmica.

Se remuestrean pacientes completos 1 000 veces, sin estratificar.
Reporta el valor, el intervalo de percentiles 2.5–97.5 y el esquema en palabras: «remuestreando pacientes».
La evaluación sigue dando el mismo peso a cada visita.

En la tarea 4 se remuestreaban filas independientes; aquí lo independiente es el paciente.
Por eso cambia la unidad remuestreada: sus visitas permanecen juntas.
El MCC no es un promedio de pérdidas por visita.
Un error estándar calculado como si las visitas fueran independientes no cumple esta entrega.

Distingue estas dos comparaciones:

1. **Optimismo de la evaluación del compañero:** resta a su MCC reportado en validación el MCC de su mismo modelo en prueba.
2. **Comparación de procedimientos:** resta al MCC de tu modelo el del compañero, ambos en prueba. Incluye el intervalo pareado: cada remuestreo evalúa ambos modelos sobre los mismos pacientes.

La diferencia entre procedimientos lleva también el intervalo de percentiles 2.5–97.5 y la frase «remuestreando pacientes».
Después de abrir la prueba, no uses sus resultados para cambiar el procedimiento.

> [!WARNING]
> **Pierdes B5 entero si abres la prueba sellada antes de B5 o la usas para decidir un arreglo.**
>
> Deja escrito que la abriste una sola vez, con todas las decisiones fijadas.

## 3 · Otras familias (opcional)

Tiempo aproximado: 45 minutos. Compararás árbol, bosque y boosting para estimar minutos de entrega con clientes nuevos.
El proceso tiene una curva fuerte en distancia y una interacción entre lluvia y hora.
Es regresión de minutos, sin pesos de clase.

> [!TIP]
> **Míralo correr: tarea 5c · Otras familias, bloques B1–B5**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_5c_otras_familias.ipynb)

### Qué haces y qué entregas

| Bloque | Trabajo | Entrega |
|---|---|---|
| B1 · Misma partición | Reutiliza una sola partición por clientes para todas las familias. | Explica por qué mantienes los mismos pliegues. |
| B2 · Árbol | Examina la curva de capacidad y completa la regla de un error estándar (EE). | Da la profundidad elegida y justifícala con esa regla. |
| B3 · Bosque | Compara de 10 a 300 árboles con tres semillas del bosque. Los datos no cambian. | Explica si se estabiliza, considerando también cuánto difieren las semillas. |
| B4 · Boosting | Compara etapas con una tasa fija y después con dos tasas. | Da las etapas elegidas y explica qué pasa con la tasa más chica. |
| B5 · Comparar y extrapolar | Escribe la comparación de error de CV ± EE, benchmark y tiempo de ajuste. Predice a una distancia doble de la mayor observada. | Explica una victoria y una limitación de cada familia. |

El código de B1, B3 y B4 está dado. En B2 completas la elección; en B5 escribes tu comparación.
El EE entre pliegues es descriptivo: no demuestra que una familia sea superior.
Distingue lo que observas en CV de lo que muestran las predicciones fuera del rango de distancias.

Conserva tus predicciones iniciales, las cinco entregas y las salidas que las sustentan.
Cuánto suma esta tarea opcional a tu calificación lo anuncia el profesor.

## 4 · Cómo se califica

Las rúbricas de 5a y 5b distribuyen el peso entre sus bloques.
En cada entrega se aplican estos criterios comunes:

| Criterio | Qué debe quedar escrito | Peso |
|---|---|---:|
| Identificar las cifras | Cada número nombra su conjunto y su benchmark. | 40 % |
| Explicar | Tu explicación dice por qué, apoyada en lo que hiciste y observaste. | 30 % |
| Respetar la prueba | La prueba se abre una sola vez y lo dices. | 30 % |

En 5b, registra la única apertura de la prueba sellada.
En 5a, documenta que elegiste con los días 1–600 antes de evaluar en los días 601–720.
La tarea 5c no abre una prueba.

Revisa que tus notebooks conserven las predicciones anteriores a cada bloque y las explicaciones posteriores.
Una tabla de números sin conjuntos ni razones deja incompleta la entrega.

**Punto de control:** puedes reconstruir cada comparación con tus salidas y explicar qué datos usaste para decidir.
