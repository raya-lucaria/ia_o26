---
id: ml-tarea-1
title: "Tarea de la clase 1 · Propón la representación"
nav_title: "Tarea"
summary: "Un notebook de unos 90 minutos: predecir antes de mover, elegir φ para un proceso periódico y para una nube que no se separa con polares, y decir dónde se usará el modelo."
status: ready
estimated_time: 90m
tags: [aprendizaje-maquina, tarea, representacion]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Tarea 1 · Propón la representación.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_1_proponer_phi.ipynb)
>
> **[👉 Abrir `tarea_1_proponer_phi.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_1_proponer_phi.ipynb)**

# Tarea de la clase 1 · Propón la representación

**¿Puedes proponer una $\phi$ mirando solo los datos, y decir con honestidad cuánto te equivocaste?**

Se entrega el `.ipynb` por Canvas; la fecha la da el profesor.
Entrega `tarea_1_proponer_phi.ipynb` con las celdas corridas, sus salidas
visibles y las seis celdas `entrega-<k>` llenas.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_1_proponer_phi.ipynb)

## 1 · Qué vas a hacer

1. **Predice antes de tocar.** Un proceso dado y tres cambios: subir el ruido $\sigma_\varepsilon$, subir $n$ y subir el grado $N$.
   Predices qué pasa con $L_{\text{ent}}$, $R$ y el piso, y después lo compruebas.
2. **Un proceso periódico.** No sabes el periodo. Lo propones mirando la nube y $L_{\text{ent}}$.
   Lo comparas con un polinomio de grado fijo, que da el notebook.
3. **Una nube nueva.** Clasificación con dos variables. La logística en cartesianas no sirve.
   Propones una $\phi$ que no sea polar.
4. **Muestra la matriz.** Imprimes $\Phi$ de tu $\phi$ del bloque 3.
5. **Dónde se usará.** Los dos ajustes del bloque 2, dentro del rango de los datos y fuera.
6. **Veredicto.** Se abre el proceso y nombras el error que queda.

## 2 · Qué entregas

1. Tus predicciones para los tres cambios, escritas antes de correr; después, cuáles acertaste y por qué.
2. Tu $\phi$ periódica, el periodo que propones y con qué lo propones.
   Si el periodo es parámetro o hiperparámetro, y por qué $L_{\text{ent}}$ no basta para elegirlo.
   Tras la revelación, qué tan lejos quedó tu propuesta.
3. Tu $\phi$ para la nube, registrada antes de revelar, con su frontera dibujada. Solo puede usar $x_1$ y $x_2$.
   Tras la revelación, sus aciertos en el despliegue contra la moda y contra el techo de Bayes, que se estima con la muestra enorme.
   Y cuánto los exageraban los aciertos de entrenamiento.
4. Cuatro filas de $\Phi$, y qué es parámetro y qué hiperparámetro en tu modelo.
5. El error dentro y fuera del rango de los datos, y por qué difieren.
6. Un veredicto de 150 palabras o menos: qué error queda, con las cuatro fuentes, y la limitación de tus propuestas.

## 3 · Cómo se evalúa

La tarea vale 10 puntos:

- **2 puntos:** predicciones registradas antes y revisadas con honestidad.
- **1.5 puntos:** periódica razonada con la nube, reconocida como exploratoria y auditada con $R$.
- **2 puntos:** una $\phi$ de la nube que funciona, comparada con la moda y con la distancia entre entrenamiento y despliegue.
- **1.5 puntos:** $\Phi$ correcta y parámetros separados de hiperparámetros.
- **1 punto:** interpolar contra extrapolar, bien argumentado.
- **1 punto:** veredicto con las cuatro fuentes del error y la limitación de elegir con entrenamiento.
- **1 punto:** no usaste $R$ para elegir; tu propuesta quedó registrada antes de revelar.

No se premia coincidir con el periodo verdadero.
Se premia el razonamiento y la honestidad sobre lo que todavía no está validado.

## 4 · Antes de empezar

- Lee antes [[ml-que-es-f|¿Qué es f?]] y [[ml-polinomios-y-capacidad|Polinomios y capacidad]].
- En los bloques 2 y 3 sigues tres pasos: **propón** con la nube y $L_{\text{ent}}$, **registra** tu propuesta con `REGISTRAR = True`, que la congela, y solo entonces **revela**. Copias lo registrado en `entrega-<k>`.
- Tus elecciones de los bloques 2 y 3 son propuestas exploratorias. Las haces con datos que tocaron el ajuste, porque en la clase 1 no hay otros. La definición de hiperparámetro dice que eso no basta.
- La muestra enorme solo sirve para revisar una propuesta ya registrada, nunca para elegir. En la vida real no existe; la clase 2 te da la herramienta que sí.
- No abras el código de la celda «Prepara los procesos» hasta el bloque 6.

Después, sigue con [[ml-clase-2-separar-los-datos|Clase 2 · Separar los datos]].
