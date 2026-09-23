---
id: opt-construir-objetivo
title: Construir la función objetivo
nav_title: Construir la función objetivo
summary: "Diez ejercicios para justificar qué optimizar: preferencias, incertidumbre, indicadores, pérdidas sustitutas y rivales."
status: ready
estimated_time: 4h10m
tags: [optimizacion, modelado, practica]
---

# Construir la función objetivo

**Antes de buscar la mejor decisión, hay que decidir qué significa mejor.**
En [[opt-practica-modelado|6.5 · Del problema al modelo]] practicamos con un
criterio suficientemente especificado. Aquí también debemos construirlo y
justificarlo. Puede faltar una preferencia, no conocerse el futuro o ser difícil
medir directamente lo que nos interesa.

La tarea sigue siendo **escribir modelos completos**, no elegir algoritmos ni
calcular óptimos. Los diez problemas usan cifras didácticas. Cuando falta un
dato deliberadamente, identifica qué falta y plantea una respuesta condicionada
a un supuesto explícito; no lo inventes como si fuera información conocida.

## Elige un tema

| Tema | Primero | Después | Qué hace difícil elegir el objetivo |
|---|---|---|---|
| Salones y horarios | Asignar salones con horarios fijos | Decidir inicios y comparar grupos | Varias preferencias pueden entrar en conflicto |
| Panadería | Producir con probabilidades conocidas | Decidir sin probabilidades justificadas | Una decisión tiene consecuencias distintas según la demanda |
| Aprendizaje | Asignar actividades por aciertos en sesión | Revisar el indicador con una prueba diferida | Lo observable puede premiar algo distinto del propósito |
| Clasificación | Ajustar por proporción de aciertos | Ajustar por pérdida logarítmica | Un objetivo sustituto aprovecha información distinta |
| Juego | Considerar la respuesta de un rival | Evaluar posiciones antes del final | Otro agente decide y una evaluación limitada puede equivocarse |

Cada tema conserva las dos páginas de 6.5: **práctica** y **modelo general**.
Las páginas generales se leen después del intento; reconstruyen el razonamiento
para más elementos y explican los límites de cada formulación.

- **Salones y horarios:** [[opt-objetivo-salones-practica|intentar los problemas 1 y 2]] · [[opt-objetivo-salones-modelo|ver el modelo general]].
- **Panadería:** [[opt-objetivo-panaderia-practica|intentar los problemas 3 y 4]] · [[opt-objetivo-panaderia-modelo|ver el modelo general]].
- **Aprendizaje:** [[opt-objetivo-aprendizaje-practica|intentar los problemas 5 y 6]] · [[opt-objetivo-aprendizaje-modelo|ver el modelo general]].
- **Clasificación:** [[opt-objetivo-clasificacion-practica|intentar los problemas 7 y 8]] · [[opt-objetivo-clasificacion-modelo|ver el modelo general]].
- **Juego:** [[opt-objetivo-juego-practica|intentar los problemas 9 y 10]] · [[opt-objetivo-juego-modelo|ver el modelo general]].

## Qué debes entregar

1. **Datos y decisiones:** qué conoces, qué eliges, sus unidades y dominios;
   separa también lo incierto y lo que decide otra persona.
2. **Construcción:** expresiones que representan consecuencias y condiciones.
3. **Modelo completo:** objetivo, restricciones y dominios, primero con
   parámetros y después con los datos del ejercicio.
4. **Justificación del objetivo:** qué mide, en qué unidades y qué preferencia
   o supuesto lo hace defendible.
5. **Comprobación crítica:** qué deja fuera, un caso en que pueda fallar y
   qué cambiarías en el modelo o qué información pedirías.

Puede haber varias respuestas defendibles. «Depende» no basta: escribe de qué
depende y muestra una formulación bajo el supuesto que elegiste. Una fórmula
bien resuelta puede seguir representando mal el propósito.

## Primero intenta plantearlo

**NO ABRAS LAS PISTAS ANTES DE ESCRIBIR TU INTENTO.**

| Ayuda plegada | Qué encontrarás |
|---|---|
| Pista 1 | Datos del relato ordenados |
| Pista 2 | Una pregunta para construir el modelo |
| Respuesta | Formulación razonada, supuestos y una comprobación del criterio |

Haz un problema por vez. Conserva todas las condiciones del relato, incluso
si una resulta redundante en los números pequeños. Al comparar dos alternativas
dadas, explica qué revela la comparación sobre el objetivo: no sustituye al
modelo ni te exige resolver todas las posibilidades.

## Tiempo y conexión con lo que sigue

Reserva aproximadamente 50 minutos por pareja, incluyendo intento, revisión y
modelo general: unas 4 horas y 10 minutos para todo el banco. Es una estimación
para distribuir en varias sesiones, no una sola clase ni una promesa de dominio.

La última pareja prepara la representación de decisiones como árboles: nuestras
acciones, respuestas del rival y valores de las posiciones. Después tendrá
sentido estudiar minimax y la poda alfa–beta. Aquí justificamos **qué problema
queremos resolver** antes de estudiar cómo recorrer ese árbol.
