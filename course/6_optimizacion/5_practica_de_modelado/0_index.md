---
id: opt-practica-modelado
title: Modelar problemas de optimización
nav_title: Modelar problemas
summary: "Cuatro ejemplos guiados para construir decisiones, restricciones y objetivos, y revisar qué representan."
status: ready
estimated_time: 1h35m
tags: [optimizacion, modelado]
---

# Modelar problemas de optimización

**Un modelo empieza con una situación y una decisión pendiente.** Antes de
buscar la mejor opción, necesitamos describir cuáles se permiten y explicar
qué significa que una sea mejor que otra.

En estas cuatro páginas construiremos modelos paso a paso. Las explicaciones
están abiertas: detente en las preguntas breves y escribe una idea antes de
seguir leyendo. Aquí no hace falta resolver los modelos ni aprender algoritmos.

## Cuatro ejemplos guiados

Empieza por salones. Allí construimos con más calma la diferencia entre datos,
decisiones y condiciones. Los siguientes ejemplos retoman esos pasos y se
concentran en una dificultad nueva.

1. **Salones: cumplir las reglas y comparar la comodidad.** Asignamos un salón
   a cada curso, comprobamos las obligaciones y construimos una medida para
   comparar asignaciones permitidas. También preguntamos a qué grupo favorece.

   [[opt-objetivo-salones-practica|Leer el ejemplo de salones]] · 30 minutos.

2. **Panadería: decidir antes de conocer la demanda.** Construimos las ventas,
   los ingresos, los costos y la ganancia. Después distinguimos una ganancia
   promedio de la protección frente a una demanda desfavorable.

   [[opt-objetivo-panaderia-practica|Leer el ejemplo de panadería]] · 25 minutos.

3. **Clasificación: acertar etiquetas y evaluar probabilidades.** Ajustamos una
   regla compartida y comparamos dos objetivos que aprovechan información
   distinta. Mejorar uno no garantiza mejorar el otro en cada comparación.

   [[opt-objetivo-clasificacion-practica|Leer el ejemplo de clasificación]] · 20 minutos.

4. **Juego: elegir una jugada y planear los turnos siguientes.** Modelamos
   la respuesta del rival y representamos las opciones en un árbol.
   Calculamos su valor desde los resultados finales mediante inducción hacia atrás.

   [[opt-objetivo-juego-practica|Leer el ejemplo del juego]] · 20 minutos.

## Qué debes poder reconstruir

En cada ejemplo, busca estas cinco partes:

- **La situación:** quién decide y qué información tiene al hacerlo.
- **Las decisiones y las reglas:** qué representa cada variable, qué valores
  admite y qué condiciones debe cumplir.
- **El objetivo:** cómo se construye, qué mide y qué preferencia representa.
- **El modelo completo:** objetivo, restricciones y dominios reunidos.
- **Los límites:** qué deja fuera y cuándo convendría revisar el modelo.

Las cifras son didácticas. No necesitas conocer aviación, aprendizaje automático
ni juegos especializados. Una fórmula correcta debe representar el relato;
un objetivo bien escrito también necesita una razón para preferirlo.

## Tiempo y práctica

El recorrido guiado suma aproximadamente **95 minutos**. Puedes repartirlo en
varias sesiones y volver a los pasos que necesites reconstruir.

Los tres primeros ejemplos incluyen ejercicios para practicar. Cada ejercicio tiene dos pistas y una respuesta ocultas.
Resolver esos ejercicios requiere tiempo de práctica adicional a los 95 minutos
del recorrido guiado.
