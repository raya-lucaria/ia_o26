---
id: dl-clase-1-redes-neuronales
title: "Clase 1 · Redes neuronales: la formulación matemática"
nav_title: "Clase 1 · Redes neuronales"
summary: "Una red profunda es una composición de funciones con parámetros: su notación, el pase hacia adelante, la pérdida con su lagrangeano, la retropropagación y el descenso de gradiente."
status: ready
estimated_time: 185m
tags: [deep-learning, redes-neuronales, retropropagacion]
prerequisites: [aprendizaje-maquina]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 01 · Una red desde cero.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)
>
> **[👉 Abrir `01_red_desde_cero.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)**

# Clase 1 · Redes neuronales: la formulación matemática

**Una red profunda es una composición de funciones con parámetros. ¿Cómo se
calcula qué cambiar en cada parámetro para que el error baje?**

La clase pone en una sola notación todo lo que los videos de 3Blue1Brown
enseñan con dibujos. Es una clase corta y directa: son las mismas ideas de
la unidad de aprendizaje de máquina, con una función más larga.

## Lo que traes

- **La pérdida y el lagrangeano**, de [[ml-lagrangeano-en-accion|El lagrangeano en acción]], en la unidad 9: aquí la regularización es la misma restricción $\Omega(\theta)\le d$.
- **La tarea de los cuatro videos** de 3Blue1Brown: si los viste, la clase ordena lo que ya sabes.
- **Matrices y derivadas parciales**, de cálculo y álgebra lineal.

La notación está en [[notacion-deep-learning|una hoja aparte]]. Si no recuerdas un símbolo a media lectura, búscalo ahí.

## Qué vas a poder hacer

- **Leer una red** como una composición de funciones: qué guarda cada $w^{(l)}_{ij}$ y qué forma tiene cada $\mathbf W^{(l)}$.
- **Calcular el pase hacia adelante** de una red pequeña, capa por capa.
- **Escribir la pérdida** de la red y su lagrangeano, igual que en la unidad 9.
- **Retropropagar:** obtener $\mathbf{δ}^{(l)}$ y los gradientes de pesos y sesgos con la regla de la cadena.
- **Dar un paso de descenso** y explicar el ciclo completo de entrenamiento.

## Recorrido

Las cinco páginas y el notebook toman 185 minutos en total.

::: table {#dl-c1-tab-recorrido title="Las páginas de esta clase"}
| # | Página | Minutos |
|---|---|---:|
| 1 | La red: capas, pesos y sesgos | 35 |
| 2 | La red como composición de funciones | 30 |
| 3 | La pérdida y el lagrangeano | 25 |
| 4 | Retropropagación: la regla de la cadena hacia atrás | 50 |
| 5 | Entrenar la red: bajar por el gradiente | 45 |
| Aparte | La tarea de la clase: cuatro videos de 3Blue1Brown | 75 |
:::

1. [[dl-la-red|La red: capas, pesos y sesgos]]
2. [[dl-composicion|La red como composición de funciones]]
3. [[dl-perdida-lagrangeano|La pérdida y el lagrangeano]]
4. [[dl-retropropagacion|Retropropagación: la regla de la cadena hacia atrás]]
5. [[dl-entrenar|Entrenar la red: bajar por el gradiente]]

La tarea previa de la clase son los cuatro videos de 3Blue1Brown; sus enlaces están en la página de tarea.

## El hilo de la clase

Una red pequeña, de dos entradas, dos capas ocultas de tres y dos neuronas
y una salida. Se usa en todas las páginas con los mismos números, y el
notebook la recorre completa.

Siguen: [[dl-la-red|la página 1]].
