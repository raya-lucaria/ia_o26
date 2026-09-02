---
id: diagnosticar-el-entorno
title: Diagnosticar el entorno
nav_title: Diagnóstico
summary: Las propiedades del entorno no son estampas; se justifican con evidencia que cambia el diseño.
status: draft
estimated_time: 25m
tags: [ambientes, aima, observabilidad, dinamica]
---

# Diagnosticar el entorno

Aquí aparece una taxonomía, pero la usaremos como una caja de herramientas, no
como una lista para memorizar. Cada propiedad responde una pregunta que cambia
qué debe poder hacer el agente. Esta es la taxonomía del **entorno**; no describe
tipos de agentes.

::: figure {#aa-perillas-entorno title="Cada perilla nace de una pregunta sobre el caso"}
![Un panel de preguntas para observar evidencia sobre información, azar, secuencia, cambio, continuidad, rivales y conocimiento del modelo](_assets/aa-perillas-entorno.svg)
:::

## Las preguntas de AIMA, con evidencia

| Pregunta | Dos extremos | Evidencia que buscarías | Qué obliga a considerar |
|---|---|---|---|
| ¿Llega toda la información relevante? | totalmente / parcialmente observable | cartas privadas, cámara recortada, sensor ruidoso | memoria o creencias sobre lo no visto |
| ¿Una acción fija el siguiente resultado? | determinista / estocástico / estratégico | azar físico; o las decisiones de otro agente | incertidumbre o modelado de otros |
| ¿Cada decisión se sostiene sola? | episódico / secuencial | ¿el salto actual cambia las opciones de después? | mirar consecuencias futuras |
| ¿Cambia mientras deliberas? | estático / dinámico / semidinámico | reloj que avanza; estado fijo pero puntaje/reloj cambiante | decidir rápido, actualizar o planificar en línea |
| ¿Las variables son contables o graduadas? | discretas / continuas | casillas y jugadas; posición, tiempo y aceleración | representación y acciones adecuadas |
| ¿Hay una sola voluntad decisora? | un agente / multiagente | rival que compite, compañero que coopera | coordinación, competencia o negociación |
| ¿Conoces la mecánica? | conocido / desconocido | reglas o física dadas frente a tener que estimarlas | aprender o experimentar con cuidado |

«Estratégico» merece una pausa: en AIMA es un caso donde el resultado depende de
las acciones de otros agentes, no solo de una moneda. Un rival inteligente puede
hacer que el ajedrez sea determinista en sus reglas y aun así estratégico para
nuestro jugador.

> [!WARNING]
> No conviertas esta tabla en etiquetas automáticas. «Ajedrez = observable,
> determinista...» no es una explicación. Escribe primero el hecho: «el tablero
> completo está visible»; entonces puedes justificar «totalmente observable».
> Además, cada clasificación depende de la frontera y de la resolución elegida.

## Ajedrez y póker: dos tableros, dos dificultades

| Rasgo | Ajedrez estándar | Póker de cartas privadas |
|---|---|---|
| Información del estado relevante | El tablero es visible. | Las manos de rivales no lo son. |
| Fuente de incertidumbre principal | La elección estratégica del rival. | Cartas ocultas, reparto aleatorio y rivales. |
| Consecuencia para el agente | Puede planear desde la posición visible, anticipando respuestas. | Debe razonar con creencias sobre manos posibles además de estrategia. |

Ambos son secuenciales y multiagente. No basta decir «póker tiene azar»:
también hay adversarios. Tampoco basta decir «ajedrez es determinista»: esa
propiedad de la transición no elimina la estrategia.

## Un diagnóstico es una cadena de tres frases

Practica este patrón:

1. **Hecho:** «La cámara muestra solo alrededor del personaje».
2. **Propiedad:** «Por eso el entorno es parcialmente observable para este
   agente».
3. **Implicación:** «Conviene conservar un mapa parcial o creencias sobre lo que
   quedó fuera de pantalla».

No todas las perillas deben llegar al mismo extremo. Una carrera simulada puede
ser continua en posición y tiempo, discreta en la elección de entrar/no entrar
a pits, dinámica porque el reloj y rivales avanzan, y conocida solo si el
simulador publica su física. Los modelos reales suelen mezclar tipos.

## Ejercicios

::: exercise {#aa-ej-ajedrez-poker title="Dos diagnósticos, no dos etiquetas"}
Para ajedrez y póker, justifica con una evidencia cada una de estas dos
distinciones: información disponible y fuente de incertidumbre. Después escribe
una capacidad que el agente de póker necesita y el de ajedrez no necesariamente.
:::

::: answer {#aa-resp-ajedrez-poker of="aa-ej-ajedrez-poker"}
En ajedrez se ve la posición de las piezas; en póker no se ven las cartas
privadas. El ajedrez tiene transiciones deterministas dadas dos jugadas, pero la
elección del rival lo vuelve estratégico. El póker añade reparto aleatorio y
cartas ocultas. Por eso un agente de póker necesita mantener creencias sobre
manos plausibles; un bot de ajedrez no necesita esa creencia para saber qué
piezas hay en el tablero.
:::

::: exercise {#aa-ej-diagnostico-carrera title="Diagnostica una carrera bajo lluvia"}
Caso: en una carrera simulada el clima puede cambiar, el reporte llega cada dos
vueltas, los rivales eligen su propia estrategia y el simulador no publica su
modelo de desgaste. Escribe cuatro cadenas hecho → propiedad → implicación.
Incluye al menos una que no sea sobre observabilidad.
:::

::: answer {#aa-resp-diagnostico-carrera of="aa-ej-diagnostico-carrera"}
Ejemplos: reporte cada dos vueltas → información parcialmente observable o
retrasada → mantener una estimación de lluvia actual; rivales eligen →
multiagente/estratégico → anticipar respuestas, no solo clima; clima y posiciones
cambian mientras se decide → dinámico → actualizar en línea; desgaste no publicado
→ modelo desconocido → estimarlo con experiencia o tratarlo como incertidumbre.
También podrías distinguir acciones discretas de variables continuas: depende de
cómo se haya definido el simulador.
:::

## A dónde va esto

Ahora sí podemos hablar del agente, pero sin mezclarlo con esta taxonomía del
entorno. La siguiente página pregunta qué **capacidad** mínima requiere el
diagnóstico: [[disenar-el-agente|Diseñar el agente]].
