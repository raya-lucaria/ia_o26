---
id: dl-clase-2-entender-una-red
title: "Clase 2 · Entender una red entrenándola"
nav_title: "Clase 2 · Entender una red"
summary: "La clase es un notebook de Colab: entrenas una red en MNIST y cambias un factor a la vez (normalización, batch, learning rate, optimizer, early stopping, tamaño, activaciones, batch normalization, dropout) para ver qué mueve el error."
status: ready
estimated_time: 120m
tags: [deep-learning, redes-neuronales, colab]
prerequisites: [dl-clase-1-redes-neuronales]
---

> [!WARNING]
> **▶▶ ESTA CLASE ES UN NOTEBOOK: ÁBRELO EN COLAB ◀◀**
>
> [![Abrir el notebook 2 en Colab](../_assets/dl-abrir-colab.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)
>
> **[👉 Abrir `02_entender_una_red.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)**

# Clase 2 · Entender una red entrenándola

**Esta página no tiene notas: la clase es el notebook.** En
[[dl-clase-1-redes-neuronales|la clase 1]] armaste una red 2–3–2–1 a mano.
Aquí entrenas redes de verdad con PyTorch sobre MNIST, dígitos escritos a mano.
Cada sección cambia un solo factor respecto a una línea base y lo compara con
las tres curvas de train, validation y test.

## Cómo correrlo

1. Abre el notebook con el botón de arriba.
2. En Colab: **Entorno de ejecución → Cambiar tipo de entorno → T4 GPU → Guardar**.
3. Luego: **Entorno de ejecución → Ejecutar todas**. La ejecución completa tarda unos 20 minutos en una T4.

El notebook ya viene ejecutado, con todas sus gráficas. Puedes leerlo completo sin correrlo y volver a ejecutarlo después.

## Lo que vas a ver, sección por sección

- **1–3 · Arranque, datos y caja de herramientas.** MNIST partido en train, validation y test, y el loop de entrenamiento a la vista.
- **4 · De la regresión logística a la red.** La regresión softmax de la unidad 9 es una red de una sola capa; le agregas una capa oculta.
- **5 · Normalizar la entrada.** Píxeles crudos, entre 0 y 1, o estandarizados.
- **6 · La línea base y las tres curvas.** Cómo leer train, validation y test en cada epoch.
- **7 · Gradient descent y el tamaño del batch.** Del paso con todos los ejemplos al mini-batch.
- **8 · El learning rate.** Pasos chicos, buenos y demasiado grandes.
- **9 · Optimizers.** SGD, momentum, Adam y AdamW con el mismo problema.
- **10 · Early stopping.** Overfitting a propósito, y dónde conviene parar.
- **11–12 · Tamaño y forma de la red.** Más ancha, más profunda, y el mismo presupuesto de parámetros repartido distinto.
- **13 · Activaciones.** ReLU, sigmoide, tanh y GELU, y por qué la sigmoide apaga el gradiente en una red profunda.
- **14 · El gradiente por capa (avanzado).** Cuánto gradiente llega a cada capa; se puede saltar.
- **15 · Batch normalization y dropout.** Qué cambia entre `train()` y `eval()`.
- **16 · Análisis del error.** Qué dígitos confunde la red y cuánta confianza tiene cuando falla.
- **17 · Una red convolucional, breve.** Una CNN contra los MLP.
- **18 · Softmax y la loss.** De los puntajes a las probabilidades, y la pérdida que se minimiza.
- **19 · Cierre.** Todas las corridas en una tabla: qué movió el error y qué no movió nada.

## Un aviso sobre test

> [!CAUTION]
> El notebook calcula la curva de **test en cada epoch solo de manera didáctica**, para que aprendas a leer las tres curvas juntas. **En un proyecto real eso está mal.** Las decisiones (learning rate, tamaño de la red, cuándo parar) se toman con validation. Test se mira **una sola vez, al final**, con el modelo ya elegido, para reportar el error en datos nuevos. Ninguna decisión del notebook usa test.

## Ábrelo

[![Abrir el notebook 2 en Colab](../_assets/dl-abrir-colab.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)

**[👉 Abrir `02_entender_una_red.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb)**
