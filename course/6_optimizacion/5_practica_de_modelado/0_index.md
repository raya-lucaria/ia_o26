---
id: opt-practica-modelado
title: Del problema al modelo
nav_title: Del problema al modelo
summary: "Ocho ejercicios de formulación: café, vuelos, un evento y la salida de una red neuronal. Dos ayudas graduales y una respuesta explicada por ejercicio."
status: ready
estimated_time: 3h
tags: [optimizacion, modelado, practica]
---

# Del problema al modelo

**Escribe un modelo, no una respuesta numérica.** Esta guía tiene ocho
problemas: cuatro situaciones y una variación de cada una. Practicarás cómo
convertir una historia en un objetivo, restricciones y dominios.

Esta sección 6.5 incorpora el antiguo anexo 6.B. Aquí el criterio ya está
suficientemente especificado: practicamos cómo traducirlo. «Clásico» no
significa que todos los modelos sean lineales.

Son situaciones habituales con **cifras didácticas**. Todos los datos están dados;
no necesitas investigar café, conocer aviación, organizar un evento ni
conocer redes neuronales. No hay probabilidad ni métodos de resolución.

## Elige un tema

| Tema | Primero | Después |
|---|---|---|
| Café | Decidir las cantidades de una mezcla | Comprar presentaciones completas |
| Vuelos | Asignar aviones con suficientes asientos | Respetar las asignaciones autorizadas |
| Un evento | Elegir qué actividades ofrecer | Decidir también sus duraciones |
| Una red neuronal | Ajustar una salida a ejemplos conocidos | Limitar el tamaño de sus pesos |

Cada tema tiene dos páginas: **práctica** y **modelo general**. Intenta los
problemas antes de leer la segunda; esta explica cómo escribir la misma
estructura con muchos ingredientes, aviones, actividades o ejemplos.

- **Café:** [[opt-practica-cafe|intentar los dos problemas]] · [[opt-modelo-cafe|ver la forma general]].
- **Vuelos:** [[opt-practica-vuelos|intentar los dos problemas]] · [[opt-modelo-vuelos|ver la forma general]].
- **Evento:** [[opt-practica-evento|intentar los dos problemas]] · [[opt-modelo-evento|ver la forma general]].
- **Red neuronal:** [[opt-practica-red|intentar los dos problemas]] · [[opt-modelo-red|ver la forma general]].

## Qué debes entregar en cada ejercicio

1. **Datos:** significado y unidades de las cantidades conocidas.
2. **Decisiones:** variables con significado, unidades y dominio.
3. **Construcción:** una expresión por cada condición del relato.
4. **Modelo completo:** objetivo, todas las restricciones y dominios,
   primero con parámetros y después con los datos del ejercicio.

Usa un renglón por restricción. Conserva cada condición aunque otra parezca
implicarla. No busques el óptimo ni pruebes combinaciones para deducir qué
restricciones escribir.

## Primero intenta plantearlo

**NO ABRAS LAS PISTAS ANTES DE ESCRIBIR TU INTENTO.** Si te atoras, abre
solo la ayuda que necesites y vuelve a tu hoja:

| Ayuda | Qué encontrarás |
|---|---|
| Pista 1 | Los mismos datos del relato, ordenados |
| Pista 2 | Una pregunta para dirigir tu atención |
| Respuesta | La construcción del modelo, sin resolverlo |

Las ayudas empiezan cerradas. Puedes abrir una sin abrir las demás. Haz un
problema por vez; no necesitas terminar los ocho en una sesión.

## Cómo comprobar tu planteamiento

- ¿Cada variable es una decisión y cada parámetro es un dato?
- ¿Cada condición del relato aparece en el modelo completo?
- ¿Las unidades coinciden y los signos expresan lo que dice la historia?
- ¿El modelo permite las opciones válidas y excluye las prohibidas?
- ¿La misma formulación seguiría funcionando con más elementos?

Las páginas generales muestran también la **forma estándar**. Para problemas
lineales seguiremos la convención de la clase 2: maximizar, escribir
restricciones con $\le$ y conservar los dominios. Para problemas convexos
usaremos minimización convexa con restricciones convexas escritas contra cero.
Cambiar de presentación no debe cambiar las decisiones permitidas.

Si necesitas recuperar el método, vuelve a [[la-bitacora-del-taller|separar datos y decisiones]] o a [[el-modelo-del-taller|construir un modelo completo]].

## Tiempo y siguiente paso

Reserva aproximadamente 45 minutos por pareja, unas tres horas si haces las
cuatro con sus modelos generales. Es un banco de práctica para varias sesiones;
el tiempo depende de tus intentos y de las ayudas que necesites.

Después, [[opt-construir-objetivo|en 6.6 construirás y justificarás también la función objetivo]].
