---
id: ml-tarea-3
title: "Tarea 3 · Cincuenta variables y una decisión defendible"
nav_title: "Tarea 3"
summary: "Elegir μ con validación cruzada en un problema de 50 variables con escalas mezcladas, explicar qué hizo lasso y abrir la prueba una sola vez."
status: ready
estimated_time: 150m
tags: [aprendizaje-maquina, tarea, lasso, validacion-cruzada]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Tarea 3 · Cincuenta variables.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_3_cincuenta_variables.ipynb)
>
> **[👉 Abrir `tarea_3_cincuenta_variables.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_3_cincuenta_variables.ipynb)**

# Tarea 3 · Cincuenta variables y una decisión defendible

## 1 · Qué vas a decidir

Vas a elegir $\mu$ para lasso con validación cruzada (*cross-validation*).
Tienes 50 variables, 5 útiles y una gemela: $x_6$ tiene correlación 0.95 con $x_1$.
Los datos son sintéticos y representan nuevas observaciones del mismo proceso; por eso puedes separarlos al azar.
Antes de empezar, lee [[ml-leer-el-error|Leer el error]] y [[ml-lagrangeano-en-accion|El lagrangeano en acción]].

## 2 · Abrir el notebook

> [!TIP]
> **Míralo correr: Tarea 3 · Cincuenta variables**
> Abre `tarea_3_cincuenta_variables.ipynb` y guarda una copia para trabajar.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/tarea_3_cincuenta_variables.ipynb)

En `SEMILLA`, escribe los últimos cuatro dígitos de tu clave única.
Tendrás 300 observaciones: 180 de entrenamiento, 60 de validación y 60 de prueba.
Las escalas de las columnas van de $10^{-4}$ a $10^{5}$.
La rejilla tiene 16 valores de $\mu$, entre $10^{-2}$ y $10$, en escala logarítmica.

Recorre los bloques en orden. Escribe cada predicción antes de correr su celda.
En el bloque de diagnóstico, compara con los puntos de comparación (*benchmark*): la media y la mediana de entrenamiento.
Después, la validación cruzada usa entrenamiento ∪ validación; estandariza dentro de cada pliegue.

Para probar la red elástica (*elastic net*), cambia `PENALIZACION = "l1"` a `"elastica"` en el bloque de interpretación.
Para comparar sin estandarizar, conserva la rejilla y la regla de elección.
Al final, congela el procedimiento antes de abrir la prueba con `sel.modelo_final`.
La salida muestra $L_{\text{prueba}}\pm2\,\mathrm{EE}$; para reportar $\pm\mathrm{EE}$, divide entre dos el margen mostrado.

## 3 · Las seis entregas

1. Escribe una predicción concreta: qué variables esperas que lasso apague y por qué. Debe poder contrastarse con lo que observes; no se califica que aciertes.
2. Reporta $L_{\text{ent}}$, $L_{\text{val}}$ y los dos benchmarks, cada número con su conjunto. Decide si mínimos cuadrados le gana a la media por más de 2 EE usando la diferencia pareada en validación. Explica por qué `val` sirve aquí como reserva. Propón una hipótesis de qué sobra o falta.
3. Reporta la $\mu$ elegida por mínimo y por un EE. Incluye el orden de simplicidad declarado antes de medir y justifícalo. Di qué regla usas y por qué. Escribe el lagrangeano del problema resuelto, con su $\mu\ge0$. Si comparas contra la media con CV, usa `diferencia_por_pliegue`: escribe solo «señal» o «sin señal», pendiente de confirmarse en una reserva.
4. Explica qué hizo lasso en tres frases: distingue un cero estimado de un coeficiente verdadero cero; describe qué pasó con la gemela; prueba la red elástica y explica si cambia eso. Apóyate en las trayectorias, los coeficientes y las frecuencias de selección en 100 réplicas.
5. Describe qué cambió al repetir la elección sin estandarizar. Identifica qué variable se apagó y explica por qué, con la cuenta de unidades y su efecto sobre el castigo.
6. Reporta $L_{\text{prueba}}\pm\mathrm{EE}$ y compáralo con el benchmark mediante la diferencia pareada y su EE. Di si le gana por más de 2 EE y compara también con el riesgo $R$. Escribe qué habría pasado si hubieras elegido con la prueba. Ábrela una sola vez, con el procedimiento congelado y reajustado con entrenamiento ∪ validación. No vuelvas a elegir.

## 4 · Cómo se evalúa

La rúbrica suma 100 puntos.

| Entrega | Puntos | Qué se mira |
|---|---:|---|
| E1 predicción | 10 | La predicción existe, es concreta y verificable. |
| E2 benchmarks y diagnóstico | 15 | Cada número lleva su conjunto y su benchmark. Decides «le gana» con la diferencia pareada y su EE en un `val` que todavía no eligió nada. Explicas por qué vale ahí y propones una hipótesis coherente con las vistas. |
| E3 elegir μ y lagrangeano | 25 | Usas CV con estandarización dentro del pliegue. Declaras antes de medir el orden de simplicidad: $\mu$ de mayor a menor. Justificas la regla. No afirmas ninguna «mejora» con un EE de CV. Escribes el lagrangeano con su signo y $\mu\ge0$. |
| E4 interpretar | 20 | Distingues cero estimado, utilidad y coeficiente verdadero. Explicas qué pasó con la gemela. |
| E5 sin estandarizar | 15 | Conectas la cuenta de unidades con el castigo. |
| E6 prueba una vez | 15 | Abres la prueba una sola vez. Comparas contra el benchmark con la diferencia pareada en prueba y contra $R$. No vuelves a elegir. |

Penalizaciones transversales: elegir algo con la prueba resta 15 puntos en el bloque donde ocurra.
Un número sin conjunto resta 2 puntos, hasta un máximo de 10 puntos.

No se exige recuperar las 5 útiles.

## 5 · Cómo se entrega

Se entrega el `.ipynb` por Canvas, con las celdas corridas. La fecha la da el profesor en clase.
