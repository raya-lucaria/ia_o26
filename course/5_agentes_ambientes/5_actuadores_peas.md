---
id: actuadores-en-peas
title: A — ¿qué puede hacer de verdad?
nav_title: "A: actuadores"
summary: "La A de PEAS define el espacio de acción: qué acciones son posibles, cuándo son legales y con qué precisión se ejecutan."
status: draft
estimated_time: 15m
tags: [peas, acciones, actuadores, decision]
---

# A — ¿qué puede hacer de verdad?

Un agente no elige «ganar». Elige una acción que su cuerpo o interfaz puede
ejecutar. La A de PEAS describe esas palancas: actuadores físicos, botones de
software, mensajes o decisiones permitidas por una regla.

## La pregunta que abre A

Completa: **«En este instante, el agente puede ___, ___ o ___.»** Cada verbo
tiene que ser ejecutable, distinguible y permitido por la E que describiste.

En una carrera simulada, «mejorar mi posición» no es acción. «Entrar a pits en
esta vuelta», «elegir un compuesto permitido» y «ajustar ritmo dentro del rango
permitido» sí pueden serlo. Si los pits solo abren en cierta zona, «entrar» no
es una acción legal en todos los estados; eso también se modela.

## Un espacio de acción tiene cuatro decisiones

| Decisión | Pregunta | Ejemplo |
|---|---|---|
| Alcance | ¿Qué puede cambiar el agente? | Acelerar, frenar, entrar a pits; no cambiar el clima. |
| Granularidad | ¿Opciones contables o valores graduados? | Izquierda/derecha frente a ángulo de giro continuo. |
| Momento | ¿Cuándo puede actuar? | Cada 0.1 s; al turno; solo en la ventana de pits. |
| Legalidad | ¿Qué opciones quedan prohibidas en este estado? | No cambiar llanta fuera del garaje; no rebasar por una zona cerrada. |

Elegir la granularidad es modelar, no descubrir una verdad única. Un bot de
plataformas puede tener acciones discretas `izquierda`, `derecha`, `saltar`,
`esperar`; otro modelo puede representar cuánto se presiona el control. Empieza
por la versión que permite formular el caso sin inventar precisión innecesaria.

## La acción olvidada: no hacer nada

Esperar, mantener rumbo, no apostar, no mandar alerta y no entrar a pits son
acciones si el agente puede escogerlas. Omitirlas fuerza intervenciones inútiles
y puede hacer que el modelo parezca más activo de lo que la tarea permite.

> [!WARNING]
> No pongas en A algo que el agente solo **observa**. «Cámara», «precio» y
> «posición del rival» son candidatos a S. No pongas en A algo que desea: «meta»
> pertenece a P. A responde únicamente: «¿qué señal puedo enviar al mundo?».

## Ejercicios

::: exercise {#aa-ej-peas-a-plataformas title="Escribe acciones para plataformas"}
Un explorador ve una plataforma móvil. Propón un espacio de acciones discreto
de cuatro o cinco opciones, incluyendo una forma de no intervenir. Después di
una acción que parece razonable pero no puedes incluir sin agregar un actuador.
:::

::: answer {#aa-resp-peas-a-plataformas of="aa-ej-peas-a-plataformas"}
Una versión mínima: caminar izquierda, caminar derecha, saltar, esperar y
retroceder. «Detener el mecanismo» no cabe si el personaje no tiene interruptor
ni herramienta para hacerlo: sería cambiar E o agregar un actuador. También es
válido modelar combinaciones como caminar-y-saltar si declaras que el control lo
permite.
:::

::: exercise {#aa-ej-peas-a-alertas title="El costo de omitir abstención"}
Un sistema solo puede mandar una alerta o no hacer nada; un equipo escribe A =
«mandar alerta». ¿Qué comportamiento queda imposible de representar y por qué
esa omisión podría empeorar P?
:::

::: answer {#aa-resp-peas-a-alertas of="aa-ej-peas-a-alertas"}
Queda imposible la abstención: el agente tendría que alertar aun cuando la señal
sea débil. Si P penaliza falsas alarmas, el modelo se contradice: evalúa una
conducta prudente que A no permite. La reparación es incluir «no alertar» como
acción explícita.
:::

## Siguiente pregunta

Tener una palanca no significa saber cuándo usarla. Falta declarar qué señales
llegan realmente al agente: [[sensores-en-peas|S — los sensores]].
