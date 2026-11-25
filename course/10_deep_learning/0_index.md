---
id: deep-learning
title: Aprendizaje profundo
nav_title: Aprendizaje profundo
summary: "Redes neuronales profundas como composición de funciones con parámetros: su notación, el pase hacia adelante, la retropropagación y el descenso de gradiente, con la regularización como lagrangeano; y luego, en un notebook de Colab, qué cambia el error al entrenar una red de verdad; y, en otro, cómo ajustar un modelo generativo con LoRA."
status: ready
estimated_time: 425m
tags: [deep-learning, redes-neuronales]
prerequisites: [aprendizaje-maquina]
---

# Aprendizaje profundo

> [!WARNING]
> **▶▶ CLASE 3 · FINE-TUNING CON LoRA: ÁBRELA EN COLAB ◀◀**
>
> [![Abrir el notebook 3 en Colab](_assets/dl-abrir-colab-3.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)
>
> **[👉 Abrir `03_finetuning_lora.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)** · En Colab elige **T4 GPU** y luego **Ejecutar todas**.

> [!TIP]
> **Notebook de la clase 2:** [![Abrir el notebook 2 en Colab](_assets/dl-abrir-colab.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)

Esta unidad continúa [[aprendizaje-maquina|la de aprendizaje de máquina]].
La pregunta es la misma: cómo ajustar un modelo a datos sin engañarse.
Lo que cambia es el modelo: una función larga, hecha de capas, con muchos parámetros.
Se entrena con el mismo descenso por gradiente.
Los gradientes salen de la regla de la cadena.

## Las clases

::: table {#dl-u-clases title="Las clases de la unidad"}
| Clase | Qué trabaja | Notebooks | Minutos |
|---|---|---|---:|
| 1 · Redes neuronales | Notación, composición, pérdida y lagrangeano, retropropagación y descenso | 01 | 185 |
| 2 · Entender una red | Entrenar en MNIST cambiando un factor a la vez: batch, learning rate, optimizers, early stopping, tamaño, activaciones, batch normalization y dropout | 02 | 120 |
| 3 · Fine-tuning con LoRA | Stable Diffusion aprende un estilo: fine-tuning completo, LoRA, QLoRA y rangos; cuánto cambia el modelo, memorización y olvido | 03 | 120 |
:::

- [[dl-clase-1-redes-neuronales|Clase 1 · Redes neuronales: la formulación matemática]]
- [[dl-clase-2-entender-una-red|Clase 2 · Entender una red entrenándola]]: la clase es un notebook de Colab.
- [[dl-clase-3-finetuning-lora|Clase 3 · Fine-tuning generativo con LoRA]]: la clase es un notebook de Colab.

## Las hojas de consulta

- [[notacion-deep-learning|Toda la notación de redes neuronales, en una hoja]]: cada símbolo, su dimensión y su página.
  También avisa qué letras cambian de sentido respecto a la unidad 9.

Empieza por [[dl-clase-1-redes-neuronales|la clase 1]].
