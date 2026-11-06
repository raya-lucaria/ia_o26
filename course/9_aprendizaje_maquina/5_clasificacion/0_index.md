---
id: ml-clase-4-clasificacion
title: "Clase 4 · Clasificación: la pérdida, la métrica y el desbalanceo"
nav_title: "Clase 4 · Clasificación"
summary: "Clasificar es estimar probabilidades, decidir con un umbral y juzgar con una métrica. Con clases raras, los aciertos engañan; los pesos cambian el problema y descalibran; conformal da una garantía marginal."
status: ready
estimated_time: 130m
tags: [aprendizaje-maquina, clasificacion, desbalanceo, mcc, calibracion, conformal]
prerequisites: [ml-clase-3-leer-el-error]
---

# Clase 4 · Clasificación: la pérdida, la métrica y el desbalanceo

**¿Con qué cifra juzgarías un filtro que casi nunca ve fraudes?**

Los aciertos pueden premiar al filtro que deja pasar todos los fraudes.
Compararás su desempeño con MCC y aciertos balanceados; también revisarás qué significan las probabilidades que anuncia.

> [!TIP]
> **Míralo correr: pérdida, métrica y probabilidades**
>
> Abre los notebooks en tu navegador. Predice antes de mover cada control y explica después lo que cambió.
>
> Notebook 08 · Pérdida, métrica y desbalanceo.
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/08_perdida_metrica_y_desbalanceo.ipynb)
>
> Notebook 09 · Calibración y conformal.
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/09_calibracion_y_conformal.ipynb)

## Lo que traes

Si una pieza no te suena, repásala antes de seguir.

::: table {#ml-c4-tab-lo-que-traes title="Las piezas que vuelves a usar"}
| Pieza | Para qué la usarás | Dónde retomarla |
|---|---|---|
| Logística de la unidad 6 | Convertir un puntaje en probabilidad y ajustar con pérdida logarítmica. | [Clasificación](raya:opt-objetivo-clasificacion-practica) |
| Riesgo | Distinguir la pérdida esperada de una métrica de clasificación. | @ml-c1-def-riesgo |
| Entrenamiento, validación y prueba | Separar el ajuste, las decisiones y la evaluación final. | @ml-c2-def-tres-conjuntos |
| Validación cruzada (*cross-validation*) estratificada | Repartir las clases entre pliegues y reconocer cuándo escasean los fraudes. | @ml-c2-def-estratificada |
| Lagrangeano de capacidad | Mantener la penalización al cambiar la pérdida. | @ml-c3-def-lagrangeano-capacidad |
| Punto de comparación (*benchmark*) | Juzgar el modelo frente a la moda y la proporción de entrenamiento. | @ml-c3-def-benchmark |
| Verosimilitud gaussiana | Conectar el cambio de pérdida con otro modelo para las etiquetas. | @ml-c3-obs-mse-verosimilitud |
:::

## Qué vas a poder hacer

- **Ajuste:** escribirás la logística regularizada y su extensión multiclase con softmax.
- **Evaluación:** distinguirás la pérdida de ajuste, el umbral de decisión y la métrica que eliges para juzgar.
- **Desbalanceo:** compararás MCC y aciertos balanceados con los aciertos; explicarás qué cambian los pesos de clase.
- **Probabilidades:** evaluarás la calibración y recalibrarás con datos separados del ajuste.
- **Garantía:** construirás conjuntos de predicción conformal y explicarás el alcance marginal de su cobertura.

## El hilo de la clase

Cambia $\ell$, la pérdida por observación: pasas de la cuadrática a la logarítmica.
Conservas la idea de ajustar parámetros y limitar capacidad.
Ahora el filtro anuncia probabilidades, decide con un umbral y recibe una evaluación con la métrica elegida.
Son decisiones distintas: mejorar el objetivo de ajuste no asegura mejorar la cifra con que juzgas.

El desbalanceo vuelve visible esa separación.
La regla que siempre anuncia «legítimo» obtiene aciertos de 0.99, pero MCC de 0 en el ejemplo de la moda.
Los pesos cambian cuánto contribuye cada clase al ajuste; también pueden descalibrar sus probabilidades.

Después revisarás esos anuncios y construirás conjuntos de etiquetas cuando haya incertidumbre.
Conformal ofrece una garantía marginal bajo intercambiabilidad de los casos de calibración y el caso nuevo, condicionada en el modelo congelado.
Esa garantía global no asegura la misma cobertura en cada clase.

## Recorrido

Recorre las páginas en este orden, con su notebook abierto.
Los 130 minutos incluyen lectura y exploración; la tarea va aparte.

::: table {#ml-c4-tab-recorrido title="Las páginas y los notebooks de la clase"}
| Página | Minutos | Notebook |
|---|---:|---|
| Pérdida, métrica y desbalanceo | 75 | 08 · Pérdida, métrica y desbalanceo |
| Calibración y predicción conformal | 55 | 09 · Calibración y conformal |
| Tarea · Tres desenlaces y uno que importa | Aparte · 120 | Tarea · Desbalanceo multiclase |
:::

1. [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]]
2. [[ml-calibracion-y-conformal|Calibración y predicción conformal]]
3. [[ml-tarea-4|Tarea · Tres desenlaces y uno que importa]]

## Los notebooks

**08 · Pérdida, métrica y desbalanceo.** Cambiarás el umbral, la proporción de clases y los pesos.
Compararás métricas y observarás su variación entre pliegues.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/08_perdida_metrica_y_desbalanceo.ipynb)

**09 · Calibración y conformal.** Contrastarás probabilidades anunciadas con frecuencias observadas.
Explorarás la recalibración y compararás cobertura global con cobertura por clase.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/09_calibracion_y_conformal.ipynb)

**Tarea · Tres desenlaces y uno que importa.** Llevarás las decisiones a un problema de crédito: al corriente, atraso e impago.
Defenderás tu métrica y evaluarás la clase que te importa.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_4_desbalanceo_multiclase.ipynb)

## Qué no cubre

- Los supuestos iid, las fugas, las tuberías y otras familias de modelos quedan para la clase 5.
- La matriz de confusión y la curva ROC aparecen solo en un recuadro de consulta.
- La calibración multiclase completa queda fuera: revisar cada clase por separado no equivale a calibrar el vector de probabilidades.

Empieza por [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]].
