---
id: aprendizaje-maquina
title: Aprendizaje de máquina
nav_title: Aprendizaje de máquina
summary: "Aprender a partir de datos sin engañarse: qué se quiere aprender, cómo se mide el error que importa, cómo se limita la capacidad y qué supuestos hay detrás de cada cifra."
status: ready
estimated_time: 755m
tags: [aprendizaje-maquina]
prerequisites: [markov]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 01 · ¿Qué es f?** Es el primero de la unidad. Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)
>
> **[👉 Abrir `01_que_es_f.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)**

# Aprendizaje de máquina

**Un modelo acierta en los datos con que se ajustó. ¿Cómo sabes si
acertará con datos nuevos?**

Esta unidad trata del aprendizaje de máquina clásico. Hay una relación que
no vemos y solo tenemos datos con ruido. Queremos un modelo que funcione
con datos nuevos, y una cifra honesta de qué tan bien lo hará.

## Las clases

::: figure {#ml-u-mapa title="La unidad en seis clases"}
![Mapa de la unidad en seis clases, en orden. Clase 0, Qué es aprender: repaso, sin notebook. Clase 1, El problema: notebooks 01 y 02 y la tarea 1. Clase 2, Separar los datos: notebooks 03 a 05 y la tarea 2. Clase 3, Leer el error y regularizar: notebooks 06 y 07 y la tarea 3. Clase 4, Clasificación: notebooks 08 y 09 y la tarea 4. Clase 5, Supuestos y metodología: el notebook 10 y las tareas 5a a 5c. Al pie, lo que recorre todas las clases: el lagrangeano, comparar siempre contra un benchmark y la muestra enorme que deja ver cuánto miente cada cifra](_assets/ml-u-mapa.svg)
:::

::: table {#ml-u-clases title="Las clases de la unidad"}
| Clase | Qué trabaja | Notebooks | Minutos |
|---|---|---|---:|
| 0 · Qué es aprender | Mitchell, supervisado y no supervisado, dónde cae el aprendizaje de máquina | ninguno | 20 |
| 1 · El problema | El proceso, el piso, el riesgo, la representación y la capacidad | 01 y 02 y tarea 1 | 120 |
| 2 · Separar los datos | Entrenamiento, validación y prueba; validación cruzada; sesgo y varianza | 03 a 05 y tarea 2 | 205 |
| 3 · Leer el error y regularizar | Residuales, benchmarks y el lagrangeano: ridge, lasso y red elástica | 06 y 07 y tarea 3 | 140 |
| 4 · Clasificación | Pérdida contra métrica, umbral, desbalanceo, calibración y conformal | 08 y 09 y tarea 4 | 130 |
| 5 · Supuestos y metodología | iid, grupos, tiempo, fugas, tuberías, la receta de trabajo y otras familias | 10 y tareas 5a a 5c | 140 |
:::

- [[ml-clase-0-que-es-aprender|Clase 0 · Qué es aprender]]
- [[ml-clase-1-el-problema|Clase 1 · El problema]]
- [[ml-clase-2-separar-los-datos|Clase 2 · Separar los datos]]
- [[ml-clase-3-leer-el-error|Clase 3 · Leer el error y regularizar]]
- [[ml-clase-4-clasificacion|Clase 4 · Clasificación]]
- [[ml-clase-5-supuestos-y-metodologia|Clase 5 · Supuestos y metodología]]

El recorrido suma **12 horas y 35 minutos** de lectura y notebooks. Las
tareas van aparte: cada una está en el índice de su clase.

## Cómo se trabaja

Cada página tiene su notebook en Colab, salvo el repaso de la clase 0 y la
página de metodología. Corren en tu navegador, sin instalar nada. Antes de
mover un control, apuesta qué va a pasar; después, explica qué cambió.

Todos los notebooks usan la misma biblioteca, `ml_lab`. Genera datos de
procesos que conoces y guarda una muestra enorme de la población. Con ella
ves el riesgo que en la práctica nunca se ve.

## Las hojas de consulta

Dos hojas aparte del recorrido, para buscar algo a media lectura:

- [[notacion-aprendizaje-maquina|Toda la notación, en una hoja]]: cada símbolo de la unidad, qué es y dónde se presentó, con los avisos de letras y la leyenda de las figuras.
- [[ml-laboratorio|El laboratorio ml_lab, en una hoja]]: cómo carga cada notebook la biblioteca y qué hace cada función.

Empieza por [[ml-clase-0-que-es-aprender|la clase 0]].
