---
id: ml-tarea-4
title: "Tarea de la clase 4 · Tres desenlaces y uno que importa"
nav_title: "Tarea"
summary: "Un notebook de crédito con tres desenlaces muy desbalanceados: elegir y justificar la métrica, ponderar la pérdida, revisar y corregir la calibración, y abrir la prueba una sola vez. Se entrega el .ipynb por Canvas."
status: ready
estimated_time: 120m
tags: [aprendizaje-maquina, tarea, clasificacion, desbalanceo, calibracion]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook de la tarea 4 · Tres desenlaces y uno que importa** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_4_desbalanceo_multiclase.ipynb)
>
> **[👉 Abrir `tarea_4_desbalanceo_multiclase.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_4_desbalanceo_multiclase.ipynb)**

# Tarea de la clase 4 · Tres desenlaces y uno que importa

> [!WARNING]
> La fecha la da el profesor. Se entrega el `.ipynb` por Canvas, con las celdas corridas.

## 1 · Abrir el notebook

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_4_desbalanceo_multiclase.ipynb)

## 2 · Qué entregas

Completa las celdas `entrega-<k>`:

1. Justifica tu métrica principal y dos compañeras en ≤6 renglones.
   Nombra objetivo, criterio de selección y evaluación; dibuja el mapa de las cinco reservas.
2. Incluye la tabla del punto de comparación (*benchmark*) en `val_b`:
   MCC, aciertos balanceados, aciertos y pérdida logarítmica.
3. Explica qué elegiste y con qué criterio. Reporta la cifra de validación
   cruzada (*cross-validation*) y su dispersión entre pliegues, como descripción.
4. Describe qué clase ganó y cuál perdió con los pesos, usando el diagnóstico en `val_b`.
5. Incluye las curvas antes y después de recalibrar. Responde con un número:
   ¿cómo afectaría una mala calibración si tuvieras que fijar la tasa de interés con este modelo?
6. Concluye en ≤10 renglones, apoyándote en tres figuras, tras congelar todo y abrir la prueba una sola vez.

## 3 · Cómo se evalúa

Rúbrica corta (10 puntos):

- Métrica y separación justificadas antes de correr, con objetivo, criterio de
  selección y evaluación nombrados, y el mapa de las cinco reservas (2).
- Benchmark presente en `val_b` y comparado en cada cifra (1).
- Pesos y $\mu$ elegidos sin tocar `val_a`, `val_b`, `cal` ni prueba, con su criterio (2).
- Diagnóstico por clase con macro y ponderado bien leídos (2).
- Calibración evaluada fuera de los datos que la ajustaron, con la pregunta de la tasa respondida (2).
- Prueba abierta una sola vez, cada cifra con su incertidumbre en la forma común
  de las tareas 4 y 5b (valor $\pm2\,\mathrm{EE}$ para promedios por caso;
  valor con su intervalo de percentiles 2.5–97.5 y el esquema dicho para MCC
  y $A_{\text{bal}}$) y conclusión coherente (1).

Se evalúa la coherencia del procedimiento, no alcanzar un MCC dado.

Penaliza: reportar una cifra ponderada como evaluación; llamar $R$ a un MCC;
elegir con prueba o con `cal`; benchmark o diagnóstico con toda la validación
o con `cal`; usar «precisión» por aciertos.

## 4 · Lo que necesitas de la clase

- [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]]
- [[ml-calibracion-y-conformal|Calibración y conformal]]
