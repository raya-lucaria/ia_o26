---
id: dl-clase-3-finetuning-lora
title: "Clase 3 · Fine-tuning generativo con LoRA"
nav_title: "Clase 3 · Fine-tuning con LoRA"
summary: "La clase es un notebook de Colab: Stable Diffusion 1.5 aprende el estilo «cara de anime» y comparas fine-tuning completo, LoRA, QLoRA y rangos por loss de validation, memoria, tiempo e imágenes, con las matemáticas de LoRA en forma compacta."
status: ready
estimated_time: 120m
tags: [deep-learning, fine-tuning, lora, colab]
prerequisites: [dl-clase-2-entender-una-red]
---

> [!WARNING]
> **▶▶ ESTA CLASE ES UN NOTEBOOK: ÁBRELO EN COLAB ◀◀**
>
> [![Abrir el notebook 3 en Colab](../_assets/dl-abrir-colab-3.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)
>
> **[👉 Abrir `03_finetuning_lora.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)**

# Clase 3 · Fine-tuning generativo con LoRA

> [!IMPORTANT]
> **Tarea para el lunes 30 de noviembre:** trae tu propio dataset de imágenes o de texto, en un zip con el formato de [[dl-tarea-dataset|la página de la tarea]], para hacer fine-tuning en clase.

**Esta página no tiene notas: la clase es el notebook.** En
[[dl-clase-2-entender-una-red|la clase 2]] entrenaste una red desde cero.
Aquí partes de un modelo ya entrenado, Stable Diffusion 1.5, y le enseñas un
estilo nuevo. La pregunta es cuánto del modelo hay que mover, y con qué
precisión, para lograrlo.

## Cómo correrlo

1. Abre el notebook con el botón de arriba.
2. En Colab: **Entorno de ejecución → Cambiar tipo de entorno → T4 GPU → Guardar**.
3. Luego: **Entorno de ejecución → Ejecutar todas**.

La primera celda de código fija `MODO`:

- `MODO = "corto"` (por omisión): lo esencial, unos 30 minutos en una T4.
- `MODO = "largo"`: además rangos, módulos y learning rates extra, unos 75 minutos.

## Lo que vas a ver, sección por sección

- **1–3 · Instalar, datos y difusión.** Caras de anime partidas en train, validation y test, y la loss de difusión, que es un MSE.
- **4 · LoRA y QLoRA en matemáticas.** $\Delta W=\frac{\alpha}{r}BA$, por qué arranca en cero, cuántos parámetros entrena y cuánta memoria ahorra.
- **5 · La caja de herramientas.** Entrenar, generar y medir, en funciones.
- **6 · Antes de entrenar.** Qué dibuja el modelo base con el mismo prompt.
- **7 · Los cuatro casos.** Fine-tuning completo (no cabe), LoRA, QLoRA y varios rangos.
- **8–9 · Dónde poner LoRA, y learning rate y schedule.** Variantes del modo largo.
- **10 · Cuánto cambia el modelo.** La norma de $\Delta W$ por capa, su rango efectivo y la perilla $\lambda$.
- **11 · Memorización.** ¿Las caras generadas son nuevas o copias de train?
- **12 · Olvido.** Qué le pasa a un prompt fuera del estilo, como un perro o una calle.
- **13 · Cierre.** Test una vez, la tabla de todas las corridas, una receta práctica de LoRA y la tarea.

## Un aviso sobre test y sobre las caras

> [!CAUTION]
> Todas las decisiones del notebook se toman con **validation**. Test se mira **una sola vez, al final**, con el modelo ya elegido.

Las caras son de personajes de anime con derechos de sus autores y se usan solo para estudiar el método. Se entrena con un único prompt genérico, `"an anime face"`, sin nombres de personajes: el modelo aprende un estilo, no identidades.

## Ábrelo

[![Abrir el notebook 3 en Colab](../_assets/dl-abrir-colab-3.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)

**[👉 Abrir `03_finetuning_lora.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)**
