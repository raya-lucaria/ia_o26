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

**Para elegir la mejor decisión, necesitamos explicar qué significa mejor.**
En [[opt-practica-modelado|6.5 · Del problema al modelo]] el criterio ya estaba
especificado. Aquí también tendrás que construirlo o examinar una propuesta:
qué queremos conseguir, cómo lo medimos y por qué esa medida ayuda a elegir.

Los diez problemas muestran dificultades distintas. A veces dos grupos tienen
preferencias que compiten; otras veces no sabemos qué ocurrirá mañana o solo
podemos observar una parte de lo que nos importa.

La tarea sigue siendo **escribir modelos completos y justificar sus objetivos**.
No hace falta elegir algoritmos ni calcular óptimos. Las cifras son didácticas.

Si falta deliberadamente un dato, explica cuál y formula bajo un supuesto
explícito. Distingue ese supuesto de la información que sí da el enunciado.

## Elige una situación

Cada situación conserva las dos páginas de 6.5: **práctica** y **modelo general**.
Lee el modelo general después de intentar los problemas. Allí se reconstruye
la formulación para más elementos y se explican sus límites.

- **Salones y horarios.** Asigna salones y después elige las horas de inicio.
  Compara reducir la molestia total con atender al grupo que recibe el mayor
  puntaje de molestia.

  [[opt-objetivo-salones-practica|Intentar los problemas 1 y 2]] · [[opt-objetivo-salones-modelo|Consultar el modelo de salones y horarios]].

- **Panadería.** Decide cuánto producir antes de conocer la demanda. Construye
  la ganancia a partir de las ventas y del costo de producción; después compara
  decisiones con probabilidades conocidas o sin ellas.

  Examina qué cambia al buscar una mayor ganancia promedio, proteger la menor
  ganancia o comparar con lo que habrías ganado conociendo la demanda a tiempo.

  [[opt-objetivo-panaderia-practica|Intentar los problemas 3 y 4]] · [[opt-objetivo-panaderia-modelo|Consultar el modelo de producción y ganancia]].

- **Aprendizaje.** Elige actividades para una sesión. Revisa qué nos dicen los
  aciertos durante la práctica y qué cambia al mirar una prueba posterior sin ayuda.

  [[opt-objetivo-aprendizaje-practica|Intentar los problemas 5 y 6]] · [[opt-objetivo-aprendizaje-modelo|Consultar el modelo de selección de actividades]].

- **Clasificación.** Ajusta una regla para distinguir mensajes normales de
  mensajes no deseados. Compara contar etiquetas acertadas con evaluar las
  probabilidades que asigna la regla.

  [[opt-objetivo-clasificacion-practica|Intentar los problemas 7 y 8]] · [[opt-objetivo-clasificacion-modelo|Consultar los modelos de clasificación]].

- **Juego.** Elige una acción teniendo en cuenta que el rival responderá.
  Después revisa un programa que recomienda jugadas contando fichas antes de
  llegar al final del juego.

  [[opt-objetivo-juego-practica|Intentar los problemas 9 y 10]] · [[opt-objetivo-juego-modelo|Consultar el modelo para elegir una jugada]].

## Qué debes entregar

1. **Datos y decisiones.** Distingue qué conoces y qué eliges, con sus unidades
   y dominios. Separa también lo incierto y lo que decide otra persona.
2. **Expresiones.** Escribe cómo calcular los resultados de una decisión y
   cómo representar las condiciones que debe cumplir.
3. **Modelo completo.** Escribe objetivo, restricciones y dominios, primero
   con parámetros y después con los datos del ejercicio.
4. **Justificación del objetivo.** Explica qué mide, en qué unidades y qué
   preferencia o supuesto te permite usarlo para comparar decisiones.
5. **Revisión.** Señala qué deja fuera y un caso en que pueda fallar. Explica
   qué cambiarías en el modelo o qué información pedirías.

Puede haber varias respuestas defendibles. Si tu respuesta depende de un
supuesto, escribe cuál y muestra la formulación que resulta al adoptarlo.
Una fórmula puede estar bien escrita y aun así medir algo distinto de lo
que queríamos conseguir.

## Primero intenta plantearlo

Escribe un primer intento antes de abrir las pistas. Consulta una ayuda a la
vez y vuelve a tu planteamiento. Después compara con la respuesta y revisa
qué supuestos habías usado.

- **Pista 1**: Datos del relato ordenados.
- **Pista 2**: Una pregunta para construir el modelo.
- **Respuesta**: Formulación razonada, supuestos y una comprobación del criterio.

Haz un problema por vez y consulta el modelo general después de revisar sus
dos ejercicios. Conserva todas las condiciones del relato, incluso si alguna
resulta redundante con los números del ejemplo.

Algunos problemas piden comparar alternativas dadas. Explica qué muestra esa
comparación sobre el objetivo. Es una forma de revisar el criterio; no sustituye
al modelo ni exige examinar todas las posibilidades.

## Tiempo y conexión con lo que sigue

Reserva aproximadamente 50 minutos por pareja, incluyendo intento, revisión y
modelo general: unas 4 horas y 10 minutos para todo el banco. Distribuye ese
tiempo en varias sesiones y ajústalo según las ayudas y revisiones que necesites.

Los problemas de juego preparan el siguiente paso: representar en un árbol
nuestras acciones, las respuestas del rival y los valores de las posiciones.
Después estudiaremos minimax y la poda alfa–beta para recorrer ese árbol.
Aquí primero justificamos **qué queremos conseguir al elegir una jugada**.
