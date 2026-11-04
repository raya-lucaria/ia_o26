---
id: ml-clase-3-leer-el-error
title: "Clase 3 · Leer el error y regularizar"
nav_title: "Clase 3"
summary: "Leer un error antes de cambiar nada, y regularizar como un lagrangeano: ridge, lasso y red elástica, por qué lasso hace ceros y cómo elegir μ."
status: ready
estimated_time: 140m
tags: [aprendizaje-maquina, residuales, benchmark, regularizacion, lagrangeano]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 06 · Leer el error.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/06_leer_el_error.ipynb)
>
> **[👉 Abrir `06_leer_el_error.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/06_leer_el_error.ipynb)**

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 07 · El lagrangeano en acción.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/07_el_lagrangeano_en_accion.ipynb)
>
> **[👉 Abrir `07_el_lagrangeano_en_accion.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/07_el_lagrangeano_en_accion.ipynb)**

# Clase 3 · Leer el error y regularizar

**En la clase 2 aprendiste a medir el error de generalización sin engañarte. Si ese error no te gusta, ¿cómo sabes qué cambiar, y cuándo basta con pedirle al modelo que sea más simple?**

> [!TIP]
> **Míralo correr: lee el error y regulariza.**
> Recorre las páginas junto con sus notebooks:
>
> `06_leer_el_error`
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/06_leer_el_error.ipynb)
>
> `07_el_lagrangeano_en_accion`
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/07_el_lagrangeano_en_accion.ipynb)

## Lo que traes

::: table {#ml-c3-tab-lo-que-traes title="Lo que traes a esta clase"}
| Concepto | Dónde nació | Para qué sirve aquí |
|---|---|---|
| Proceso generador: $y=f(x)+\varepsilon$ | Clase 1 · @ml-c1-def-proceso-generador | Distinguir lo que genera los datos de lo que ajusta el modelo. |
| Cuatro fuentes: azar, variables que no medimos, familia equivocada y pocos datos | Clase 1 · @ml-c1-obs-cuatro-fuentes | Preguntar de dónde viene el error antes de cambiar el ajuste. |
| Riesgo y error de generalización | Clase 1 · @ml-c1-def-riesgo | Separar la pérdida esperada de lo que mide una muestra. |
| Piso $R_{\text{Bayes}}$ | Clase 1 · @ml-c1-def-error-bayes | Juzgar cuánto margen queda para la pérdida elegida y las variables visibles. |
| Modelo lineal en parámetros y matriz de diseño $\Phi$ | Clase 1 · @ml-c1-def-modelo-lineal | Distinguir la representación de las entradas de los coeficientes que ajustas. |
| Capacidad como restricción | Clase 1 · @ml-c1-def-capacidad-como-restriccion | Pasar de limitar una familia a penalizar sus coeficientes. |
| Brecha | Clase 1 · @ml-c1-def-brecha | Distinguir el error de entrenamiento del error de generalización. |
| Parámetro contra hiperparámetro | Clase 1 · @ml-c1-def-param-hiper | Separar el ajuste de coeficientes de la elección de la penalización. |
| Tres conjuntos: entrenamiento, validación y prueba | Clase 2 · @ml-c2-def-tres-conjuntos | Diagnosticar y elegir sin usar la prueba para decidir. |
| Validación cruzada (*cross-validation*), $\mathrm{CV}_k$, y regla de un EE | Clase 2 · @ml-c2-def-validacion-cruzada; @ml-c2-def-regla-un-ee | Comparar penalizaciones y elegir con una regla declarada antes de medir. |
| Sesgo y varianza de una predicción | Clase 2 · @ml-c2-teo-sesgo-varianza | Leer qué cambia al restringir la capacidad del modelo. |
| Lagrangeano con $\mu\ge0$ y condiciones KKT | Unidad 6 · @opt-lagrangeano-general; @opt-kkt | Reconocer la regularización como un problema de optimización con una restricción. |
:::

## Qué vas a poder hacer

- Leer un diagnóstico de residuales en validación y reconocer sus límites.
- Juzgar el error frente a un punto de comparación (*benchmark*) y al piso de la misma pérdida.
- Plantear ridge, lasso y red elástica (*elastic net*) como un lagrangeano, y explicar por qué lasso hace ceros.
- Elegir $\mu$ con validación cruzada, estandarizando solo con el entrenamiento de cada pliegue.

## El hilo de la clase

Primero lees el error: miras los residuales en validación y comparas la pérdida con un benchmark y su piso.
Después, si lo que sobra es capacidad, restringes el modelo mediante una penalización.
La muestra enorme del laboratorio permite contrastar cada lectura y descubrir cuándo te engaña.
Regularizar es una respuesta posible al diagnóstico; no corrige todas las fuentes de error.

## Recorrido

::: table {#ml-c3-tab-recorrido title="Recorrido de la clase 3"}
| Página | Minutos | Notebook |
|---|---:|---|
| Leer el error | 65 | `06` |
| El lagrangeano en acción | 75 | `07` |
| Tarea 3 | aparte | `tarea_3` |
:::

El recorrido suma 140 minutos; la tarea se hace aparte.

1. [[ml-leer-el-error|Leer el error]]
2. [[ml-lagrangeano-en-accion|El lagrangeano en acción]]

## Los notebooks

**06 · Leer el error.** Exploras los residuales y comparas el error con un benchmark y el piso de la pérdida.
Contrastas el diagnóstico con una muestra enorme para reconocer lo que los residuales no te dicen.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/06_leer_el_error.ipynb)

**07 · El lagrangeano en acción.** Comparas ridge, lasso y red elástica al cambiar la fuerza de regularización.
Observas el efecto en los coeficientes y eliges $\mu$ con validación cruzada, estandarizando con entrenamiento.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/07_el_lagrangeano_en_accion.ipynb)

**Tarea 3 · `tarea_3_cincuenta_variables`.** Es la tarea para trabajar en casa (~150 min).
Encuentras su página en el menú de la clase como «Tarea 3».

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_3_cincuenta_variables.ipynb)

## Qué no cubre esta clase

- La clasificación y su pérdida se presentan en la clase 4.
- Los métodos causales para tratar la endogeneidad quedan fuera del curso.
- Para resolver lasso usas descenso por coordenadas; aquí no programas el algoritmo.
- La selección de variables paso a paso queda fuera del recorrido.
- La clase 5 comprueba por qué estandarizar con todos los datos es una fuga (*leakage*).

Empieza por [[ml-leer-el-error|Leer el error]].
