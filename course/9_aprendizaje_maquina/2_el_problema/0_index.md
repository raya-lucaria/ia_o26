---
id: ml-clase-1-el-problema
title: "Clase 1 · El problema: qué queremos aprender y por qué es difícil"
nav_title: "Clase 1 · El problema"
summary: "Existe una f que no vemos y solo tenemos datos con ruido: el piso que ningún modelo baja, el riesgo contra el error de entrenamiento, la representación y la capacidad."
status: ready
estimated_time: 120m
tags: [aprendizaje-maquina, riesgo, representacion, capacidad]
prerequisites: [ml-clase-0-que-es-aprender]
---

> [!WARNING]
> **▶▶ ABRE LOS NOTEBOOKS EN COLAB ◀◀**
>
> **Notebook 01 · ¿Qué es f?** y **Notebook 02 · Polinomios, capacidad y supuestos**. Corren en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb) [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)
>
> **[👉 Abrir `01_que_es_f.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)**
>
> **[👉 Abrir `02_polinomios_y_capacidad.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)**

# Clase 1 · El problema

**En la unidad 6 el optimizador eligió el polinomio de grado 5 y su error fue cero. ¿Qué le falta a ese error para decir si el modelo sirve?**

Falta saber cómo predice en entregas nuevas. El error cero solo describe
las entregas con las que se ajustó.

> [!TIP]
> Puedes acompañar la lectura con dos notebooks en Colab, uno por página, sin instalar nada.
> Abre los accesos de «Los notebooks» y recorre cada uno junto con su página.

## Lo que traes

Si algún concepto no te suena, vuelve a la página indicada.

::: table {#ml-c1-tab-lo-que-traes title="Lo que traes a esta clase"}
| Concepto | Página |
|---|---|
| Aprender según Mitchell: tarea, experiencia y desempeño | Qué es aprender (clase 0) |
| Aprendizaje supervisado | Qué es aprender (clase 0) |
| Mínimos cuadrados y familias anidadas | Regresión, en la unidad 6 |
| Pérdida logarítmica | Clasificación, en la unidad 6 |
| El gorro de lo estimado | El problema de Markov |
| El lagrangeano con $\mu\ge0$ | Los signos del lagrangeano |
:::

- [[ml-repaso-que-es-aprender|Qué es aprender (clase 0)]]
- [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]]
- [[opt-objetivo-clasificacion-practica|Clasificación, en la unidad 6]]
- [[mkv-el-problema-de-markov|El problema de Markov]]
- [[los-signos-del-lagrangeano|Los signos del lagrangeano]]

## Qué vas a poder hacer

Lo que te llevas de la clase:

- **Proceso y riesgo:** cómo se escriben el proceso que genera las entregas y el riesgo que mide el error al predecir sus tiempos.
- **Fuentes de error:** qué baja cada remedio: medir otra variable, cambiar la representación, ampliar la familia o reunir más datos.
- **Linealidad:** cuándo un modelo es lineal en sus parámetros $\beta$, aunque use potencias de la distancia.
- **Capacidad:** por qué el error de entrenamiento $L_{\text{ent}}$ no basta para elegir el grado $N$ del polinomio.
- **Límites:** el principio de que ningún método gana en todos los problemas (*no free lunch*).

## El hilo de la clase

Retomas las entregas de la unidad 6 para predecir sus tiempos a partir de la distancia.
El polinomio con error cero lleva a preguntar qué ocurre con entregas nuevas.
Los anillos entran para mostrar cómo cambiar las variables puede facilitar la clasificación.

## Recorrido

Las dos páginas y sus notebooks toman 120 minutos en total: 55 + 65.

::: table {#ml-c1-tab-recorrido title="Las páginas de esta clase"}
| # | Página | Minutos |
|---|---|---:|
| 1 | ¿Qué es f? El proceso, el piso y la representación | 55 |
| 2 | Polinomios, capacidad y supuestos | 65 |
:::

1. [[ml-que-es-f|¿Qué es f? El proceso, el piso y la representación]]
2. [[ml-polinomios-y-capacidad|Polinomios, capacidad y supuestos]]

La tarea (proponer una representación) llega en la siguiente entrega.

## Los notebooks

Cada notebook se puede recorrer solo en casa, de arriba abajo.

El notebook 01, `01_que_es_f.ipynb`, toma unos 25 minutos, incluidos en el recorrido.
Te permite explorar el ruido, el riesgo y la representación con las entregas y los anillos.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)

El notebook 02, `02_polinomios_y_capacidad.ipynb`, toma unos 30 minutos, incluidos en el recorrido.
Recorres Taylor y la curva de capacidad, y distingues quién elige el grado del polinomio.
Exploras qué pasa al extrapolar y por qué ningún método gana en todos los problemas.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

El notebook de la tarea queda pendiente de publicación.

## Qué no cubre esta clase

- Cómo medir el riesgo $R$ sin una muestra enorme: validación, prueba y validación cruzada, junto con sesgo y varianza, corresponden a la clase 2.
- El lagrangeano con $\mu$ se retoma en la clase 3.
- Las métricas de clasificación se estudian en la clase 4.

Empieza por [[ml-que-es-f|¿Qué es f?]].
