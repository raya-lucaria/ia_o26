---
id: lienzo-de-modelado
title: El lienzo de modelado
nav_title: Lienzo
summary: Una hoja de consulta para convertir una historia en un problema de decisión revisable.
status: draft
estimated_time: 10m
tags: [lienzo, modelado, consulta]
---

# El lienzo de modelado

Úsalo en orden. No llenes los diez cuadros de una vez. Completa primero 1–5 y
8; vuelve a 6–7 y 9–10 cuando el caso tenga suficiente detalle. Un cuadro puede
decir «desconocido» si agregas la observación o supuesto que falta.

::: figure {#aa-lienzo-consulta title="Diez preguntas antes de escoger un algoritmo"}
![Un lienzo ordenado de diez pasos: decisión, frontera, entorno, observaciones, acciones, dinámicas, información oculta, desempeño, diagnóstico y capacidades](_assets/aa-lienzo-modelado.svg)
:::

| Paso | Pregunta para llenar | Revisión rápida |
|---:|---|---|
| 1 | ¿Qué decisión concreta ocurre ahora? | Hay un verbo y opciones reales. |
| 2 | ¿Dónde está la frontera del agente? | No mezclaste controlador, interfaz y mundo. |
| 3 | ¿Qué queda en el entorno? | Incluiste reglas y otras entidades que importan. |
| 4 | ¿Qué observa de verdad? | No escribiste información que el sensor no entrega. |
| 5 | ¿Qué acciones puede ejecutar? | «No hacer nada» aparece si es posible. |
| 6 | ¿Qué cambia tras una acción? | Nombraste consecuencias presentes y futuras. |
| 7 | ¿Qué es relevante pero no visible o incierto? | Distinguiste mundo, observación y creencia. |
| 8 | ¿Cómo se compara una buena trayectoria? | Hay desempeño y restricciones, no solo un eslogan. |
| 9 | ¿Qué propiedades del entorno tienen evidencia? | Cada etiqueta viene después de un hecho. |
| 10 | ¿Qué capacidad mínima necesita el agente? | Se deriva de 4, 6, 7 y 9; no de una moda. |

## Clínica guiada: recolector en un museo simulado

Un robot de museo recorre tres salas simuladas. Tiene cámara de corto alcance,
un mapa incompleto y batería limitada. Puede avanzar, girar, esperar o volver a
la base. Algunas puertas se cierran por horarios; visitantes simulados cambian
de lugar. Debe recoger fichas extraviadas y volver a la base sin chocar.

Empieza solo con estos cinco cuadros y el criterio:

1. **Decisión:** elegir avanzar, girar, esperar o regresar en el siguiente paso.
2. **Frontera:** controlador + sensores + motores del robot; museo, puertas,
   visitantes y fichas quedan fuera.
3. **Entorno:** salas, reglas de puertas, visitantes, fichas, batería que se
   consume por movimiento.
4. **Observación:** cámara local, nivel de batería y mapa parcial; no el museo
   completo ni la posición futura de visitantes.
5. **Acciones:** avanzar, girar, esperar, regresar siguiendo ruta conocida.
8. **Desempeño:** recuperar fichas y volver seguro; penalizar choques, batería
   agotada y tiempo excesivo.

Después puedes justificar: parcialmente observable (la cámara es local),
dinámico (visitantes y puertas cambian), secuencial (gastar batería hoy afecta
el regreso) y probablemente requiere memoria/modelo de mapa. Si supones que las
puertas siguen un horario publicado, anótalo: esa hipótesis cambia qué tan
«conocido» es el entorno.

## Tarjetas de casos para practicar

| Caso | Dato que falta a propósito | Pregunta que abre |
|---|---|---|
| Portera | ¿Ve la postura completa o solo una cámara lateral? | ¿La observación alcanza para anticipar? |
| Póker | ¿Cuántas rondas y qué apuestas se permiten? | ¿Cuáles son acciones y qué creencias importan? |
| Cartera simulada | ¿Hay costo al operar y límite de riesgo? | ¿«No hacer nada» es acción y cuál es la P? |
| Riego | ¿La humedad se mide en toda la parcela? | ¿Memoria/modelo o regla reactiva? |

Un buen modelador no llena el hueco silenciosamente. Dice «supongamos X» y
explica qué conclusión depende de X.
