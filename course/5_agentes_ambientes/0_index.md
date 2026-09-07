---
id: agentes-ambientes
title: Agentes, ambientes y modelado de decisiones
nav_title: Agentes y ambientes
summary: Antes de escoger un modelo, aprende a dibujar qué decide un sistema, qué observa, qué puede hacer y cómo se juzgan sus consecuencias.
status: draft
estimated_time: 4h15m
tags: [agentes, ambientes, modelado, decision, refuerzo]
---

# Agentes, ambientes y modelado de decisiones

Hasta aquí el curso preguntó qué puede calcular una máquina y cuánto cuesta
hacerlo. Ahora cambia de pregunta: **si un sistema puede observar y actuar,
¿cómo decidimos qué debe hacer?**

No vamos a empezar con un algoritmo. Primero vamos a aprender a tomar una
situación concreta —un portero, un juego, una carrera, una cartera ficticia— y
dibujar el problema que realmente tenemos enfrente.

::: figure {#aa-lienzo title="El orden para modelar antes de elegir una herramienta"}
![Diez pasos que van de identificar una decisión a diseñar la capacidad mínima de un agente](_assets/aa-lienzo-modelado.svg)
:::

## Lo que vas a poder hacer

- Distinguir una predicción de una decisión que cambia el futuro.
- Trazar la frontera entre agente, cuerpo, controlador y entorno.
- Separar mundo, observación, estado interno y acción.
- Especificar una tarea con PEAS y no confundir desempeño, objetivo, utilidad y recompensa.
- Diagnosticar un entorno con evidencia, no con etiquetas memorizadas.
- Elegir la capacidad mínima que un agente necesita antes de pensar en algoritmos.

## Recorrido

| | Página | Qué resuelve | |
|---|---|---|---:|
| 1 | [[de-prediccion-a-decision|De predicción a decisión]] | Qué añade actuar a estimar algo | 15m |
| 2 | [[dibujar-el-bucle|Dibujar el bucle]] | Frontera, observación, creencia y acción | 20m |
| 3 | [[desempeno-en-peas|P — desempeño]] | Qué cuenta como una trayectoria buena y qué no permitimos | 25m |
| 4 | [[entorno-en-peas|E — entorno]] | Entidades, reglas, recursos y dinámica fuera del agente | 20m |
| 5 | [[actuadores-en-peas|A — actuadores]] | Acciones posibles, precisión, legalidad y abstención | 15m |
| 6 | [[sensores-en-peas|S — sensores]] | Observación, ruido, retraso y zonas ciegas | 20m |
| 7 | [[peas-integrado|Integrar PEAS]] | Una ficha completa y pruebas para detectar contradicciones | 25m |
| 8 | [[diagnosticar-el-entorno|Diagnosticar el entorno]] | Siete propiedades, una por una, con evidencia | 35m |
| 9 | [[disenar-el-agente|Diseñar el agente]] | Capacidades que responden a cada limitación | 30m |
| 10 | [[de-consecuencias-a-refuerzo|De consecuencias a refuerzo]] | Política, recompensa y retorno | 20m |

Y una hoja para usar frente a un caso nuevo:

- [[lienzo-de-modelado|El lienzo de modelado]] — los diez pasos, tarjetas de caso y supuestos permitidos.

**Si vas con poco tiempo**, lee 1, 2, las cuatro páginas PEAS (3–7) y 8. Con
eso ya puedes especificar y diagnosticar un problema de decisión; las dos
páginas posteriores explican qué capacidad necesita el agente y cómo conecta
con refuerzo.

## El principio de esta unidad

> No me des una etiqueta. Dame la evidencia del caso que justifica esa
> etiqueta.

Decir que un mundo es «parcialmente observable» sólo sirve si puedes señalar
qué información relevante no llega al agente. Decir que un agente necesita un
modelo sólo sirve si puedes explicar qué recuerda o infiere que no estaba
visible.
