---
id: ml-clase-5-supuestos-y-metodologia
title: "Clase 5 · Los supuestos y la metodología"
nav_title: "Clase 5 · Supuestos y metodología"
summary: "Cuándo el error que mides es el que tendrás al usar el modelo: iid y cómo comprobarlo, grupos, tiempo, fugas, tuberías y la receta de trabajo; cierra con otras familias y el puente a redes."
status: ready
estimated_time: 140m
tags: [aprendizaje-maquina, iid, fugas, metodologia]
prerequisites: [ml-clase-4-clasificacion]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 10 · ¿Son iid? Fugas** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/10_son_iid_y_fugas.ipynb)
>
> **[👉 Abrir `10_son_iid_y_fugas.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/10_son_iid_y_fugas.ipynb)**

# Clase 5 · Los supuestos y la metodología

**Tu prueba dio un error pequeño. ¿Qué tendría que ser cierto mañana para que ese número siga valiendo?**

La prueba debe parecerse al uso previsto y quedar fuera de las decisiones del ajuste.
Revisarás ambas condiciones con los pedidos de entregas.

> [!TIP]
> **Míralo correr: ¿Son iid? Fugas**
>
> Abre el notebook 10. Predice antes de mover cada control y explica después qué cambió en la evaluación.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/10_son_iid_y_fugas.ipynb)

## Lo que traes

Si una pieza no te suena, vuelve a su página antes de seguir.

::: table {#ml-c5-tab-lo-que-traes title="Lo que traes a la clase 5"}
| Concepto | Dónde nació |
|---|---|
| Riesgo $R$ y despliegue | Clase 1 · ¿Qué es f? El proceso, el piso y la representación |
| Proceso generador | Clase 1 · ¿Qué es f? El proceso, el piso y la representación |
| Parámetro e hiperparámetro | Clase 1 · Polinomios, capacidad y supuestos |
| Entrenamiento, validación y prueba: tres conjuntos | Clase 2 · Entrenamiento y prueba: la prueba imita la realidad |
| La prueba imita la realidad | Clase 2 · Entrenamiento y prueba: la prueba imita la realidad |
| Prueba insesgada y sus dos hipótesis | Clase 2 · Entrenamiento y prueba: la prueba imita la realidad |
| Validación cruzada (*cross-validation*) y estratificada | Clase 2 · Validación cruzada: elegir sin gastar la prueba |
| Punto de comparación (*benchmark*) | Clase 3 · Leer el error |
| Estandarizar con entrenamiento | Clase 3 · El lagrangeano en acción: regularizar |
| Lagrangeano de capacidad | Clase 3 · El lagrangeano en acción: regularizar |
| MCC y pérdida logarítmica | Clase 4 · Pérdida, métrica y desbalanceo |
| Por qué no remuestrear; mapa de reservas de calibración y conformal | Clase 4 · Pérdida, métrica y desbalanceo; Calibración y predicción conformal |
:::

- [[ml-que-es-f|¿Qué es f? El proceso, el piso y la representación]]
- [[ml-polinomios-y-capacidad|Polinomios, capacidad y supuestos]]
- [[ml-entrenamiento-y-prueba|Entrenamiento y prueba: la prueba imita la realidad]]
- [[ml-validacion-cruzada|Validación cruzada: elegir sin gastar la prueba]]
- [[ml-leer-el-error|Leer el error]]
- [[ml-lagrangeano-en-accion|El lagrangeano en acción: regularizar]]
- [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]]
- [[ml-calibracion-y-conformal|Calibración y predicción conformal]]

## Qué vas a poder hacer

- **Detectores:** comprobarás si separar al azar es defendible con tres detectores: validación adversarial, comparación de distribuciones y revisión temporal de residuales.
- **Separación:** apartarás grupos completos o respetarás el orden temporal según el uso previsto.
- **Fugas:** encontrarás una fuga (*leakage*) y medirás cuánto infla el desempeño reportado.
- **Tubería:** ajustarás la preparación de datos y el modelo dentro de cada pliegue con una tubería (*pipeline*).
- **Metodología:** seguirás la receta de principio a fin y decidirás los cambios con validación.

## El hilo de la clase

Los pedidos de entregas ahora llevan fecha y cliente.
También registrarás cuándo se conoce cada columna: al pedir la entrega o después de completarla.
Un dato disponible después no sirve para predecir al recibir el pedido.

Revisarás si las observaciones son independientes e idénticamente distribuidas (iid) y si la muestra representa el uso.
Los pedidos de un cliente pueden parecerse entre sí; los pedidos futuros pueden venir de un proceso distinto.
Los detectores buscan señales de esos problemas. No encontrar señales no demuestra que los supuestos se cumplan.

Después ordenarás el trabajo: fijar el uso, separar, ajustar, evaluar en validación y decidir qué cambiar.
La prueba queda cerrada hasta fijar el procedimiento.
Con esa misma receta explorarás otras familias y el paso de construir variables a aprender una representación.

## Recorrido

Los 140 minutos incluyen las páginas y el trabajo con el notebook 10.
La tarea se hace en casa y queda fuera de esa suma.

::: table {#ml-c5-tab-recorrido title="Recorrido de la clase 5"}
| Página | Qué haces | Minutos |
|---|---|---:|
| 1 · ¿Son iid? Fugas | Mirar el tercer requisito; definir iid con bolsas; comprobar con tres detectores; separar como se usará: grupos y tiempo; encontrar una fuga; meter todo en la tubería. | 90 |
| 2 · La metodología | Seguir la receta; escribir las categóricas como columnas; decidir qué cambiar; probar otras familias; aprender la representación. | 50 |
| Tarea de la clase 5 · Series, fugas y otras familias (aparte) | Trabajar series de tiempo y fugas; explorar otras familias como opción adicional. | 165 en casa |
:::

1. [[ml-son-iid-y-fugas|¿Son iid? Fugas]]
2. [[ml-la-metodologia|La metodología]]

## El notebook

En `10_son_iid_y_fugas` compararás detectores y separaciones por grupos o por tiempo.
Encontrarás fugas y observarás qué cambia al ajustar la preparación dentro de cada pliegue.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/10_son_iid_y_fugas.ipynb)

## Qué no cubre esta clase

- La teoría de series de tiempo queda fuera: no desarrollarás modelos ARIMA ni la estacionariedad formal.
- No usarás imputación con modelos; la página de fugas explica por qué usa imputación simple.
- No harás búsqueda fina de hiperparámetros: una rejilla recorre combinaciones prefijadas; una búsqueda aleatoria las muestrea.
- No entrenarás redes; ese trabajo corresponde a la siguiente unidad.

Empieza por [[ml-son-iid-y-fugas|¿Son iid? Fugas]].
