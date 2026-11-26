---
id: dl-clase-3-finetuning-lora
title: "Clase 3 · Fine-tuning con LoRA: imágenes y texto"
nav_title: "Clase 3 · Fine-tuning con LoRA"
summary: "La clase son dos notebooks de Colab, uno de imágenes (Stable Diffusion) y otro de texto (un LLM chico). En cada uno subes tu propio dataset en un zip, entrenas un LoRA, ves qué cambió por dentro, entiendes cada métrica y lo pruebas en test una sola vez."
status: ready
estimated_time: 120m
tags: [deep-learning, fine-tuning, lora, colab]
prerequisites: [dl-clase-2-entender-una-red]
---

> [!WARNING]
> **▶▶ ESTA CLASE SON DOS NOTEBOOKS: ABRE EL DE TU DATASET EN COLAB ◀◀**
>
> **¿Trajiste imágenes?** Abre el notebook 3:
>
> [![Abrir el notebook 3 en Colab](../_assets/dl-abrir-colab-3.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)
>
> **¿Trajiste texto?** Abre el notebook 4:
>
> [![Abrir el notebook 4 en Colab](../_assets/dl-abrir-colab-4.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/04_finetuning_llm.ipynb)
>
> **[👉 Notebook 3 · `03_finetuning_lora.ipynb`](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb)** · **[👉 Notebook 4 · `04_finetuning_llm.ipynb`](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/04_finetuning_llm.ipynb)**

# Clase 3 · Fine-tuning con LoRA: imágenes y texto

> [!IMPORTANT]
> **Tarea para el lunes 30 de noviembre:** trae tu propio dataset de imágenes o de texto, en un zip con el formato de [[dl-tarea-dataset|la página de la tarea]], para hacer fine-tuning en clase.

**Esta página no tiene notas: la clase son los notebooks.** En
[[dl-clase-2-entender-una-red|la clase 2]] entrenaste una red desde cero.
Aquí partes de un modelo que ya sabe mucho y le enseñas algo tuyo moviendo
muy pocos números. Es la idea de LoRA.

| | Notebook 3 · imágenes | Notebook 4 · texto |
|---|---|---|
| Modelo | Stable Diffusion 1.5 | Qwen2.5-0.5B-Instruct, un LLM chico |
| Tu zip | `imagenes.zip`: `metadata.csv` + `images/` | `texto.zip`: `datos.jsonl` |
| Aprende | un estilo o un tipo de objeto | a responder de cierta forma |
| Sin zip | usa un demo de caras de anime | usa un demo de texto → SQL |

## Cómo correrlo

1. Abre el notebook que toca con el botón de arriba.
2. En Colab: **Entorno de ejecución → Cambiar tipo de entorno → T4 GPU → Guardar**.
3. **Arrastra tu zip** al panel de archivos 📁, a la izquierda de Colab. Si
   pesa mucho, súbelo a tu Drive; el notebook explica cómo leerlo de ahí.
4. **Entorno de ejecución → Ejecutar todas.** Si no subiste nada, corre con el demo.

`MODO = "corto"`, en la primera celda de código, deja la corrida en unos 25
minutos en una T4. `MODO = "largo"` entrena más pasos y con más datos.

## Las mismas ocho secciones en los dos

- **1 · Instalar.** Paquetes, GPU y semillas.
- **2 · Tu zip.** Dónde subirlo, la revisión del formato y la partición en train, validation y test.
- **3 · Antes.** Qué hace el modelo base con tus `prompts.txt`.
- **4 · LoRA por dentro.** $W=W_0+\frac{\alpha}{r}BA$: cuántos parámetros entrenas y cuánto pesa el adaptador.
- **5 · Entrenar.** Un solo LoRA, con sus curvas de train y validation.
- **6 · Ver LoRA.** El rango de $\Delta W$, las capas que más cambiaron y la perilla $\lambda$, que va del modelo base al tuyo.
- **7 · Las métricas.** Qué mide cada una, qué valor es bueno y su trampa.
- **8 · Testeo.** Base contra LoRA en test, una sola vez; olvido; descargar tu adaptador.

> [!CAUTION]
> Todas las decisiones se toman con **validation**. Test se mira **una sola vez, al final**, con el modelo ya elegido.
