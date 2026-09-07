---
id: desempeno-en-peas
title: P — ¿qué cuenta como hacerlo bien?
nav_title: "P: desempeño"
summary: La P de PEAS obliga a decir cómo se juzga una trayectoria antes de diseñar una recompensa o un algoritmo.
status: draft
estimated_time: 25m
tags: [peas, desempeno, objetivos, utilidad]
---

# P — ¿qué cuenta como hacerlo bien?

Una historia no se vuelve tarea porque le agregues «hazlo bien». Antes de
preguntar cómo decide un agente, decide **qué consecuencias prefieres**. Ésa es
la P de PEAS: *performance measure*, medida de desempeño.

::: figure {#aa-peas-p title="PEAS empieza por el criterio, no por el algoritmo"}
![El campo P de PEAS pregunta por las consecuencias preferidas y las restricciones antes de describir la interfaz](_assets/aa-peas.svg)
:::

## La pregunta que abre P

Completa esta oración: **«Al terminar una trayectoria, diremos que fue mejor si
___, siempre que no ___.»** La primera parte nombra qué buscamos; la segunda
evita que una solución absurda gane por atajo.

Para la estrategia de pits de una carrera simulada, una primera P podría ser:

> Terminar la carrera en menor tiempo total, respetando el reglamento ficticio,
> sin agotar combustible ni producir desgaste fuera del límite seguro.

Eso es mejor que «ganar». Dice qué se mide, durante cuánto tiempo y qué no se
acepta aunque parezca útil.

## Cuatro palabras que se parecen, pero trabajan en capas distintas

| Palabra | Pregunta que responde | Ejemplo de carrera simulada |
|---|---|---|
| **Objetivo** | ¿Hacia dónde queremos ir? | Terminar la carrera. |
| **Desempeño** | ¿Cómo juzgamos la trayectoria completa? | Tiempo total, reglas, combustible, desgaste y seguridad. |
| **Utilidad** | ¿Cómo comparamos resultados con intercambios? | ¿Cuánto tiempo vale aceptar un poco más de desgaste? |
| **Recompensa** | ¿Qué señal numérica recibe el agente durante una transición? | Penalización por tiempo/desgaste y premio al terminar. |

El objetivo es una brújula. La medida de desempeño es el criterio de evaluación.
La utilidad vuelve comparables consecuencias que chocan entre sí. La recompensa
es una señal que podría ayudar a aprender; **no sustituye** las otras tres.

> [!WARNING]
> «P = recompensa» es una confusión peligrosa. La P evalúa lo que en verdad
> quieres de una trayectoria; una recompensa es una manera imperfecta de
> orientar un agente. Si el agente explota la recompensa sin cumplir la P, el
> defecto está en el diseño, no en la ambición del agente.

## Una P se diseña mirando fallas plausibles

Empieza por un intento pobre y pregunta qué conducta premiaría.

| P demasiado corta | Atajo que podría incentivar | Reparación mínima |
|---|---|---|
| «Entregar lo más rápido posible» | Ignorar seguridad o abandonar pedidos lejanos. | Tiempo, seguridad, reglas y cobertura de pedidos. |
| «Recoger más objetos» | Dar vueltas donde los objetos reaparecen. | Completar el nivel, costo por tiempo y objetos únicos. |
| «Maximizar rendimiento de una cartera simulada» | Tomar riesgo ficticio ilimitado o ignorar costos. | Retorno simulado, riesgo declarado, costos y límites. |

No siempre necesitas pesos numéricos hoy. Sí necesitas hacer visibles los
intercambios. «No sabemos aún cuánto pesa la seguridad frente al tiempo» es una
respuesta honesta; ocultarla dentro de un número no lo es.

## Paso a paso: escribe una P que alguien pueda discutir

1. Elige el horizonte: ¿un paso, una partida, un día, toda una carrera?
2. Nombra el resultado principal que mejora una trayectoria.
3. Lista dos daños o límites que no aceptarías para lograrlo.
4. Busca un atajo: «si solo midiera esto, ¿qué haría un agente literal?»
5. Declara una incertidumbre si falta información en el caso.

La P no exige acordar valores universales. Exige que el desacuerdo sea visible y
revisable antes de entrenar, programar o evaluar.

## Ejercicios

::: exercise {#aa-ej-peas-p-reparar title="Repara el criterio de un repartidor"}
Un equipo escribió: «el agente debe entregar lo más rápido posible». Escribe dos
atajos que esa P podría premiar y reescribe una medida de desempeño para una
simulación de reparto. Incluye horizonte, resultado principal y dos límites.
:::

::: answer {#aa-resp-peas-p-reparar of="aa-ej-peas-p-reparar"}
Podría premiar exceder límites de seguridad o abandonar pedidos que quedan lejos.
Una P posible: «durante un turno simulado, completar pedidos con bajo retraso,
respetando límites de seguridad y presupuesto de energía, sin dejar zonas sin
atender». Si no sabemos si todos los pedidos valen igual, se declara como
supuesto en vez de esconderlo.
:::

::: exercise {#aa-ej-peas-p-capasy title="Ubica cada frase en su capa"}
Clasifica estas frases como objetivo, desempeño, utilidad o recompensa:

1. «Llegar a la base antes de que termine la batería».
2. «Recibir -0.01 por cada segundo de espera».
3. «Preferimos perder dos minutos a arriesgar una colisión».
4. «La trayectoria debe recuperar fichas y volver sin choques».
:::

::: answer {#aa-resp-peas-p-capasy of="aa-ej-peas-p-capasy"}
1. Objetivo. 2. Recompensa: es una señal por transición. 3. Utilidad o una
preferencia que luego puede volverse utilidad. 4. Medida de desempeño: juzga la
trayectoria completa. Una frase puede contribuir a más de una capa al diseñar un
sistema real, pero aquí separamos su trabajo principal.
:::

## Siguiente pregunta

Ya sabemos cómo juzgar. Ahora pregunta qué existe alrededor del agente y qué
queda fuera de su frontera: [[entorno-en-peas|E — el entorno de la tarea]].
