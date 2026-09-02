---
id: especificar-la-tarea
title: Especificar la tarea
nav_title: PEAS
summary: "PEAS vuelve revisable una historia: desempeño, entorno, actuadores y sensores."
status: draft
estimated_time: 20m
tags: [peas, desempeno, objetivos]
---

# Especificar la tarea

Una historia atractiva todavía no es una tarea. «Haz un buen bot de carrera»
oculta qué significa bueno, qué controla y qué información recibe. PEAS es una
lista corta para abrir esas cuatro cajas antes de inventar soluciones.

::: figure {#aa-peas-figura title="PEAS: no una taxonomía de agentes, una ficha de tarea"}
![Cuatro campos conectados: medida de desempeño, entorno, actuadores y sensores](_assets/aa-peas.svg)
:::

## Las cuatro preguntas PEAS

| Letra | Pregunta | Ejemplo: estrategia de pits en una carrera simulada |
|---|---|---|
| **P**: desempeño | ¿Qué consecuencias preferimos y qué restricciones importan? | Menor tiempo total, sin exceder desgaste o combustible ficticio. |
| **E**: entorno | ¿Qué está fuera y evoluciona? | Pista, clima, rivales, reglamento y simulador. |
| **A**: actuadores | ¿Qué puede alterar el agente? | Entrar a pits, elegir compuesto permitido, ajustar ritmo. |
| **S**: sensores | ¿Qué información le llega? | Tiempo, clima estimado, desgaste medido, posición y avisos. |

PEAS describe la **tarea y su interfaz**. No dice todavía si conviene memoria,
búsqueda o aprendizaje. Por eso no confundas una ficha PEAS con una taxonomía de
agentes.

## La P es donde viven los desacuerdos importantes

Estas palabras se relacionan, pero no son intercambiables:

| Palabra | Uso práctico |
|---|---|
| Objetivo | Dirección amplia: «terminar la carrera». |
| Medida de desempeño | Cómo evaluará la tarea una trayectoria completa: tiempo, seguridad, reglas. |
| Utilidad | Una comparación de consecuencias cuando hay intercambios: por ejemplo, rapidez frente a riesgo. |
| Recompensa | Señal numérica que un diseñador o entorno entrega durante o después de una transición. Puede aproximar el desempeño, pero puede estar mal diseñada. |

Una tarea puede tener objetivo sin haber especificado una utilidad útil. Un
algoritmo de refuerzo puede recibir recompensa sin que esa recompensa represente
bien lo que queríamos. La pregunta correcta no es «¿qué número pongo?» sino
«¿qué conducta incentivará este número a lo largo de la trayectoria?».

## PEAS no inventa los hechos: declara supuestos

Para la carrera simulada, podríamos asumir que los actuadores solo permiten
elegir en una ventana de pits, que la lluvia se observa con retraso y que las
reglas prohíben ciertos compuestos. Si mañana el simulador cambia esas reglas,
la ficha debe cambiar. Eso no es una falla: es el trabajo de modelar.

::: figure {#aa-ilus-carrera title="Decidir con un mapa incompleto"}
![Un equipo original de estrategia observa una carrera lluviosa y compara dos rutas abstractas iluminadas](_assets/ilus-estrategia-carrera.jpg)
:::

*(Esta imagen es una ilustración generada, no una transmisión ni datos de una carrera real.)*

## Ejercicios

::: exercise {#aa-ej-peas-pits title="Llena una ficha PEAS"}
Para la carrera simulada, escribe dos elementos por cada letra. En P incluye una
restricción: algo que no aceptarías aunque mejorara el tiempo. Marca con
«supuesto» cualquier detalle que el caso no te haya dado.
:::

::: answer {#aa-resp-peas-pits of="aa-ej-peas-pits"}
Una ficha posible: **P** tiempo total y posiciones ganadas, sin rebasar desgaste
seguro ni infringir reglas; **E** pista y clima, rivales y simulador; **A** entrar
a pits y elegir compuesto/ritmo permitido; **S** tiempo por vuelta y desgaste,
pronóstico retrasado y posición. «El desgaste se mide con error» sería un buen
supuesto explícito. No hay una lista única correcta: sí hay listas que mezclan
una acción con una observación y deben corregirse.
:::

::: exercise {#aa-ej-reparar-p title="Repara una P demasiado corta"}
Un equipo escribió para un repartidor autónomo: «P = entregar lo más rápido
posible». Da dos consecuencias malas que esa frase podría incentivar y reescribe
la P como una medida de desempeño más completa, sin elegir aún un algoritmo.
:::

::: answer {#aa-resp-reparar-p of="aa-ej-reparar-p"}
Podría incentivar exceder límites de seguridad o abandonar pedidos lejanos.
Una mejor P: «completar pedidos a tiempo, con seguridad, dentro de reglas y
presupuesto de combustible; comparar retrasos y cancelaciones explícitamente».
No hace falta asignar pesos numéricos aún, pero sí nombrar los intercambios que
no queremos esconder.
:::

## A dónde va esto

Ya tenemos una tarea revisable. Ahora toca diagnosticar las propiedades del
entorno que cambian qué tan difícil es decidir:
[[diagnosticar-el-entorno|el diagnóstico del entorno]].
