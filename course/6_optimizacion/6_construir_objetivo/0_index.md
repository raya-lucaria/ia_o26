---
id: opt-construir-objetivo
title: Problemas para practicar
nav_title: Practicar
summary: "Doce problemas de modelado con dos pistas y respuesta plegada; modelos generales como consulta opcional."
status: ready
estimated_time: 5h
tags: [optimizacion, modelado, practica]
---

# Problemas para practicar

**Elige una situación y escribe tu modelo antes de abrir las ayudas.** Este
banco reúne doce problemas. Los diez primeros forman cinco parejas; los dos
últimos amplían los ejemplos de horarios y panadería.

Si necesitas ver cómo se construye un modelo, vuelve a [[opt-practica-modelado|6.5 · Modelar problemas de optimización]].
Aquí la tarea es intentarlo por tu cuenta. No necesitas encontrar los óptimos
ni desarrollar algoritmos de resolución.

## Elige qué practicar

- **Problemas 1 y 2 · Café.** Prepara una mezcla al menor costo. Primero puedes
  comprar fracciones de kilogramo; después solo se venden paquetes completos.

  [[opt-practica-cafe|Intentar los problemas de café]].

- **Problemas 3 y 4 · Aviones.** Asigna un avión con suficientes asientos a cada
  vuelo. Después añade una prohibición de operación y conserva las reglas anteriores.

  [[opt-practica-vuelos|Intentar los problemas de aviones]].

- **Problemas 5 y 6 · Talleres.** Elige qué ofrecer con un presupuesto y un tiempo
  disponibles. Después decide también cuánto dura cada taller.

  [[opt-practica-evento|Intentar los problemas de talleres]].

- **Problemas 7 y 8 · Red neuronal.** Ajusta una regla compartida a los puntajes
  de cuatro clips de audio. Después impón un límite al tamaño de los pesos.

  [[opt-practica-red|Intentar los problemas de la red]].

- **Problemas 9 y 10 · Aprendizaje.** Elige actividades para una sesión y revisa
  qué cambia al contar aciertos posteriores sin ayuda.

  [[opt-objetivo-aprendizaje-practica|Intentar los problemas de aprendizaje]].

- **Problema 11 · Horarios.** Decide cuándo empiezan cursos que ocupan distintos
  números de bloques. Compara la molestia total con la del grupo peor atendido.

  [[opt-practica-horarios|Intentar el problema de horarios]].

- **Problema 12 · Ganancias y oportunidades perdidas.** Sin probabilidades
  justificadas, compara asegurar una ganancia con limitar lo que dejas de ganar
  por no conocer la demanda a tiempo.

  [[opt-practica-riesgo|Intentar el problema de panadería]].

## Cómo trabajar cada problema

1. **Separa datos y decisiones.** Indica su significado, unidades y dominios.
   Distingue también lo incierto o lo que decide otra persona.
2. **Construye las expresiones.** Explica cómo calculas el objetivo y cómo
   representas cada condición. Comprueba las unidades antes de sumar.
3. **Reúne el modelo completo.** Escribe objetivo, restricciones y dominios,
   primero con parámetros y después con los datos del ejercicio.
4. **Revisa el significado.** Comprueba que acepta las decisiones permitidas
   y rechaza las prohibidas. Cuando debas justificar un objetivo, explica qué
   mide, qué supuesto permite usarlo y qué deja fuera.

Conserva cada condición del relato, aunque resulte redundante con los números
pequeños. No necesitas resolver el problema para deducir sus restricciones.
Las cifras son didácticas y los enunciados dan los datos necesarios.

## Usa las ayudas por etapas

- **Pista 1:** organiza la información para retomar tu intento.
- **Pista 2:** plantea una pregunta que ayuda a construir el modelo.
- **Respuesta:** explica la formulación para compararla con la tuya.

Las ayudas empiezan cerradas y se abren por separado. Vuelve a tu hoja después
de cada pista. En las parejas, intenta primero el problema inicial y después
su variante.

## Consultas opcionales

Estas páginas generalizan las formulaciones y explican variantes o formas
estándar. **No hace falta leerlas todas para completar la práctica.** Abre la
que corresponda después de revisar tu intento, si quieres extender el razonamiento.

- [[opt-modelo-cafe|Mezclas y paquetes]].
- [[opt-modelo-vuelos|Asignación de aviones y permisos]].
- [[opt-modelo-evento|Selección y duración de talleres]].
- [[opt-modelo-red|Ajuste de una salida con pesos compartidos]].
- [[opt-objetivo-aprendizaje-modelo|Selección de actividades e indicadores]].
- [[opt-objetivo-salones-modelo|Salones, horarios y prioridades]].
- [[opt-objetivo-panaderia-modelo|Producción, ganancia y oportunidad perdida]].
- [[opt-objetivo-clasificacion-modelo|Objetivos para clasificación]].
- [[opt-objetivo-juego-modelo|Utilidad y evaluación de jugadas]].

## Tiempo y conexión con lo que sigue

Reserva aproximadamente **45 minutos por pareja**, **35 para horarios** y
**40 para ganancias y oportunidades perdidas**: unas **cinco horas** si haces
los doce problemas con sus intentos y revisión de respuestas. Es un banco
seleccionable para varias sesiones, no una clase única ni una tarea que debas
hacer completa de una vez. Las consultas opcionales requieren tiempo adicional.

El [[opt-objetivo-juego-practica|ejemplo guiado del juego]] prepara el paso a
árboles de decisiones, minimax y poda alfa–beta. Formular qué se valora y por
qué sigue siendo necesario antes de estudiar cómo recorrer esos árboles.
