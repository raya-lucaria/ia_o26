---
id: sensores-en-peas
title: S — ¿qué información llega de verdad?
nav_title: "S: sensores"
summary: "La S de PEAS describe las observaciones disponibles: qué mide la interfaz, con qué ruido, retraso y zonas ciegas."
status: draft
estimated_time: 20m
tags: [peas, sensores, observacion, incertidumbre]
---

# S — ¿qué información llega de verdad?

La S de PEAS no pregunta qué datos nos gustaría tener. Pregunta qué llega a la
interfaz del agente **en el momento de decidir**. Una cámara, una lectura de
temperatura, un tablero, una API retrasada o el registro de una acción pasada
son sensores en este sentido amplio.

::: figure {#aa-peas-s title="El entorno existe completo; S solo deja entrar una parte"}
![Un flujo que distingue el mundo externo, los sensores, la observación que entra al agente y el estado interno que este conserva](_assets/aa-mundo-observacion-creencia.svg)
:::

## La pregunta que abre S

Completa: **«Antes de actuar, el agente recibe ___; esa señal puede estar ___ y
no le dice ___.»** La segunda y tercera parte importan tanto como la primera.

En la carrera simulada, S podría incluir tiempo por vuelta, posición, nivel de
combustible, lectura estimada de desgaste y pronóstico de lluvia. Si el
pronóstico llega cada dos vueltas, no es «clima actual»: es una señal retrasada.
Si el desgaste se estima desde telemetría imperfecta, no es el desgaste exacto.

## Cuatro formas en que una observación puede quedarse corta

| Problema | Qué significa | Ejemplo |
|---|---|---|
| Cobertura | Algo relevante queda fuera de vista. | La cámara local no muestra la siguiente sala. |
| Ruido | La señal llega, pero con error. | Un sensor de humedad fluctúa. |
| Retraso | La señal describe el pasado, no el instante actual. | Reporte de lluvia cada dos vueltas. |
| Resolución | La señal agrupa detalles que importan. | «Desgaste alto» no dice cuánto ni en qué llanta. |

Estos defectos no vuelven inútil un sensor. Solo cambian lo que el controlador
debe hacer: quizá recordar, filtrar, estimar o actuar con cautela. La palabra
formal que aparecerá después es **observación parcial**. Por ahora basta decir
qué falta y cómo lo sabes.

## Mundo, observación y creencia: la distinción que evita trampas

| Caja | Carrera bajo lluvia |
|---|---|
| Mundo | Lluvia real, desgaste real, posiciones reales y decisiones de rivales. |
| Observación | Reporte retrasado, telemetría estimada, posición que muestra la interfaz. |
| Creencia interna | «Probablemente ya llueve fuerte» o «la llanta izquierda está cerca del límite». |

La creencia no tiene que ser una probabilidad elegante. Puede ser memoria de la
última lectura, un mapa parcial o una hipótesis. Lo importante es no escribirla
como si viniera gratis desde el sensor.

> [!WARNING]
> Si escribes «el agente observa el estado», pregunta inmediatamente: ¿cuál
> sensor entrega cada variable? En un MDP se puede modelar un estado suficiente;
> eso no autoriza a equipararlo sin más con la observación física o de software.

## Ejercicios

::: exercise {#aa-ej-peas-s-humedad title="Audita un sensor de riego"}
Un controlador de riego recibe una medida de humedad del suelo cada diez minutos
desde un único sensor, pero el terreno tiene zonas de sol y sombra. Escribe S y
nombra una cobertura, un retraso o un ruido que afecte la decisión. ¿Qué cosa no
puedes afirmar con esa señal?
:::

::: answer {#aa-resp-peas-s-humedad of="aa-ej-peas-s-humedad"}
S es la lectura de un sensor puntual cada diez minutos. Hay cobertura incompleta:
la zona soleada puede estar seca aunque el sensor en sombra marque humedad. Hay
retraso de hasta diez minutos y posible ruido de medición. No puedes afirmar que
todo el terreno tenga la lectura actual. Una mejora sería añadir sensores; otra,
mantener una estimación por zona declarando sus supuestos.
:::

::: exercise {#aa-ej-peas-s-cartas title="No confundas una carta con una creencia"}
En póker el agente ve sus cartas, cartas comunitarias y apuestas, pero no las
cartas privadas rivales. Separa tres elementos en: mundo, observación y
creencia. Da una creencia que podría actualizarse después de una apuesta alta.
:::

::: answer {#aa-resp-peas-s-cartas of="aa-ej-peas-s-cartas"}
Las cartas privadas rivales están en el mundo; las propias, comunitarias y las
apuestas son observaciones; «la rival probablemente tiene una mano fuerte» es
una creencia interna que se actualiza con la apuesta. La creencia puede ser mala,
pero sigue sin ser una observación: no llegó por un sensor.
:::

## Siguiente pregunta

Ya llenamos cada letra por separado. Falta comprobar que las cuatro describen
la **misma** tarea y no cuatro listas que se contradicen:
[[peas-integrado|integrar PEAS]].
