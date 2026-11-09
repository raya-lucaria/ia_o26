---
id: ml-tarea-2
title: "Tarea 2 · Separar, elegir y reportar"
nav_title: "Tarea 2"
summary: "Un notebook donde separas un proceso nuevo según cómo se usará, eliges el grado por validación cruzada, reportas en prueba con su error estándar y mides cuánto te habrías engañado eligiendo con la prueba."
status: ready
estimated_time: 120m
tags: [aprendizaje-maquina, tarea]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Tarea 2 · Separar y elegir.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_2_separar_y_elegir.ipynb)
>
> **[👉 Abrir `tarea_2_separar_y_elegir.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_2_separar_y_elegir.ipynb)**

# Tarea 2 · Separar, elegir y reportar

**¿Puedes defender, con números, el error que anuncias?**

## Qué entregas y cómo

Se entrega el `.ipynb` por Canvas; la fecha la da el profesor.
Entrega `tarea_2_separar_y_elegir.ipynb` con las celdas corridas, sus salidas
visibles y las seis celdas `entrega-<k>` llenas.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_2_separar_y_elegir.ipynb)

Sustituye el 0 de `SEMILLA = 0` por los últimos cuatro dígitos de tu clave única.
Conserva esa semilla durante la tarea. Tus cifras deben corresponder a esa
ejecución. Escribe las apuestas antes de correr las celdas que permiten
comprobarlas; conserva el orden y las salidas.

## Los seis bloques

1. **Contrato y separación.** Lee el contrato iid del proceso:
   «se usará con entregas nuevas de esta misma ciudad, sacadas igual que la muestra».
   El proceso tiene ruido independiente. Separa al azar 80/20:
   120 entregas para desarrollo y 30 para prueba. Dibuja la partición.

   En `entrega-1`, justifica en dos renglones por qué el azar imita este contrato.
   Después dedica dos renglones a la transferencia, sin calcular:
   «Si el contrato fuera *el mes que viene* o *clientes nuevos*, ¿qué columna necesitarías y cómo separarías?».
   Estos datos no tienen columna de tiempo ni de cliente.

   Se califica que relaciones cada separación con el uso anunciado.

2. **Antes de mirar.** Escribe tres apuestas numéricas en `entrega-2`.
   Predice el grado que elegirá la validación cruzada (*cross-validation*, CV).
   Predice $L_{\text{prueba}}$ del modelo final menos la del benchmark (min²).
   Predice $\mathrm{CV}_5$ del grado 12 (min²).
   Aquí $L$ es la pérdida promedio y $N$ es el grado.
   El *benchmark* es «la media de entrenamiento como punto de comparación; la clase 3 lo define».

   Las tres van en el diccionario `MIS_APUESTAS` del notebook.

   Se califica que las apuestas sean numéricas y anteriores a los resultados.

3. **Elegir el grado.** Declara el orden de complejidad y la regla que usarás antes de medir.
   Corre `elegir(..., con="cv", k=5)` y compara la regla del mínimo con la de un error estándar (EE).
   Aquí $k$ cuenta pliegues; repasa los avisos de letras indicados en «Antes de empezar».

   Conserva impresa la tabla $\mathrm{CV}\pm\mathrm{EE}$.
   En `entrega-3`, escribe el grado de cada regla y cuál usarás.
   Se califica que pueda seguirse la selección desde la regla declarada hasta el grado elegido.

4. **Reportar.** Con el grado fijado, reajusta con todo el desarrollo.
   Abre la prueba una vez, en la celda del reporte.
   Conserva impresos $L_{\text{prueba}}\pm2\,\mathrm{EE}$ y el benchmark evaluado en esa misma prueba.

   Calcula la diferencia pareada «modelo menos benchmark» con `diferencia_pareada`, usando las pérdidas por observación en prueba.
   Conserva también su EE. Los dos modelos deben estar fijados y la prueba no debe haber intervenido en ninguna decisión.

   En `entrega-4`, completa esta frase con tus resultados:
   «Para [contrato], el error esperado es … ± … minutos², contra … del benchmark;
   la diferencia pareada es … ± …».
   En el primer margen usa dos EE; en el de la diferencia, identifica que reportas su EE.

   Indica si puedes afirmar que le gana al benchmark por más de dos EE.
   Usa el EE de la diferencia pareada de pérdidas y considera su signo: calculaste «modelo menos benchmark».
   La CV del bloque 3 no sustenta esa afirmación: sus pérdidas fuera de pliegue dependen entre sí.

   Se califican el reporte, sus unidades, la comparación y su alcance para el contrato anunciado.
   La prueba estima el riesgo; no lo revela exactamente.

5. **Auditar.** Corre la celda que agrega dos entregas lejanas, a 9 y 10 km.
   Examina las cajas por pliegue y compara $k=3$, $k=5$ y $k=20$.

   En `entrega-5`, explica qué causó el pliegue anómalo.
   Describe qué cambia con pocos y muchos pliegues en costo, sesgo y ruido.
   Se califica que apoyes la explicación en las cajas y en las ejecuciones.

6. **Medir el engaño.** Elige con la prueba para medir cuánto te habrías engañado.

   Corre las 200 repeticiones que eligen con la prueba.
   Compara el error anunciado con $R$, estimado con la muestra enorme del proceso.
   Esta celda mide el engaño a propósito y conserva intacto el reporte del bloque 4.
   No uses sus resultados para cambiar aquel reporte.

   En `entrega-6`, escribe el sesgo medio y explica el resultado en dos renglones que incluyan la palabra «mínimo».
   Se califica la medición y la explicación de la diferencia entre lo anunciado y el riesgo.

## Rúbrica

La tarea vale 10 puntos:

- **2 puntos:** separación justificada por el contrato y transferencia correcta a los contratos de tiempo y de clientes.
- **1 punto:** predicciones escritas antes de correr; debe verse en el orden y las salidas.
- **2 puntos:** selección trazable con regla declarada.
- **2 puntos:** reporte con EE, benchmark y alcance. La afirmación «le gana al benchmark» se sostiene solo con la diferencia pareada en prueba, nunca con la CV.
- **1.5 puntos:** auditoría del pliegue y del número de pliegues.
- **1.5 puntos:** engaño medido y explicado.

No se califica que todos obtengan el mismo grado.

## Antes de empezar

- Lee antes [[ml-entrenamiento-y-prueba|Entrenamiento y prueba]] y [[ml-validacion-cruzada|Validación cruzada]].
- Dos letras con aviso: $L$ es la pérdida promedio de un conjunto, y $k$ es el número de pliegues.
