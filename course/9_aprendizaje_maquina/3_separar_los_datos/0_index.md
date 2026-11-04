---
id: ml-clase-2-separar-los-datos
title: "Clase 2 · Separar los datos: medir lo que no vemos"
nav_title: "Clase 2 · Separar los datos"
summary: "Cómo medir el error que importa: entrenamiento, validación y prueba, la prueba como simulacro del uso real y validación cruzada con su error estándar para elegir hiperparámetros."
status: ready
estimated_time: 140m
tags: [aprendizaje-maquina, clase-2]
prerequisites: [ml-clase-1-el-problema]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 03 · Entrenamiento y prueba.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)
>
> **[👉 Abrir `03_entrenamiento_y_prueba.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)**

# Clase 2 · Separar los datos

**En la clase 1 el error de entrenamiento eligió siempre el grado más alto. ¿Con qué datos se elige entonces?**

Eliges con validación y reservas la prueba para medir después de fijar el modelo.
Con las entregas de la unidad 6 verás por qué esa separación importa.
La prueba estima el riesgo; no lo revela exactamente.

## Lo que traes

Si necesitas repasar una pieza, usa su enlace debajo de la tabla.

::: table {#ml-c2-tab-lo-que-traes title="Lo que traes a esta clase"}
| Concepto | Qué recuperas | Página |
|---|---|---|
| Riesgo | La pérdida esperada en el uso real | ¿Qué es f? |
| $L_{\mathcal D}$ | La pérdida promedio en un conjunto de datos | ¿Qué es f? |
| Brecha | La diferencia entre riesgo y error de entrenamiento | Polinomios y capacidad |
| Parámetro e hiperparámetro | La distinción que usarás al elegir con validación | Polinomios y capacidad |
| Capacidad como restricción | Limitar qué ajustes permite la familia | Polinomios y capacidad |
| Piso | El menor riesgo con las variables visibles y una pérdida dada | ¿Qué es f? |
| $\widehat\beta$ aleatorio | El ajuste depende de la muestra que recibes | ¿Qué es f? |
| Entregas de la unidad 6 | Predecir tiempos a partir de la distancia | Regresión |
:::

- Riesgo: [[ml-que-es-f|¿Qué es f?]]
- Pérdida en un conjunto: [[ml-que-es-f|¿Qué es f?]]
- Brecha: [[ml-polinomios-y-capacidad|Polinomios y capacidad]]
- Parámetro e hiperparámetro: [[ml-polinomios-y-capacidad|Polinomios y capacidad]]
- Capacidad como restricción: [[ml-polinomios-y-capacidad|Polinomios y capacidad]]
- Piso: [[ml-que-es-f|¿Qué es f?]]
- Ajuste aleatorio: [[ml-que-es-f|¿Qué es f?]]
- Entregas: [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]]

## Qué vas a poder hacer

- **Separación:** distinguir qué datos sirven para ajustar, cuáles para elegir y cuáles para medir al final.
- **Prueba:** diseñar una reserva que imite las entregas donde usarás el modelo.
- **Incertidumbre:** interpretar el error estándar de una pérdida promedio, sin confundirlo con el error de una entrega individual.
- **Elección:** comparar grados mediante validación cruzada (*cross-validation*) y aplicar la regla de un error estándar.
- **Reporte:** explicar qué decisiones tocaron cada conjunto y qué límites tiene la medición que anuncias.

## El hilo de la clase

Primero vas a medir: separas las entregas y construyes una prueba que se parezca al uso real.
Después vas a elegir: rotas la validación entre partes de los datos y comparas grados sin gastar la prueba.
Al explicar el resultado, distingues el error medido de la incertidumbre de esa medición.

La página 3 llega después, con la descomposición del error en ruido, sesgo y varianza.
El notebook 05 acompaña esa página.

## Recorrido

Las dos páginas y sus notebooks suman 140 minutos.
Cada fila incluye la lectura y el trabajo en Colab; la tarea va aparte.

::: table {#ml-c2-tab-recorrido title="Las páginas de esta clase"}
| Página | Minutos de lectura + notebook |
|---|---:|
| 1 · Entrenamiento y prueba: la prueba imita la realidad | 75 |
| 2 · Validación cruzada: elegir sin gastar la prueba | 65 |
| Aparte · Tarea: separar, elegir y reportar | Aparte |
:::

1. [[ml-entrenamiento-y-prueba|Entrenamiento y prueba: la prueba imita la realidad]]
2. [[ml-validacion-cruzada|Validación cruzada: elegir sin gastar la prueba]]

## Los notebooks

Puedes recorrer cada notebook por tu cuenta, de arriba abajo, o usarlo junto con su página.
Los tiempos de 03 y 04 ya están incluidos en el recorrido.

**Notebook 03 · Entrenamiento y prueba.** Separa las entregas y observa qué pasa cuando usas la prueba para elegir.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Notebook 04 · Validación cruzada.** Compara grados y examina cuánto cambia la pérdida entre las partes usadas para validar.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Tarea · Separar, elegir y reportar.** Usa el notebook para documentar tus decisiones y explicar la medición final.
La fecha la da el profesor.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_2_separar_y_elegir.ipynb)

*Se abre en Google Colab, en otra pestaña.*

## Qué no cubre

CV temporal y por grupos, fugas, iid formal: clase 5; regularización: clase 3; métricas de clasificación: clase 4.

Empieza por [[ml-entrenamiento-y-prueba|Entrenamiento y prueba]].
