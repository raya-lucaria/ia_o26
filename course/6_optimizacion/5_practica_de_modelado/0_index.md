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

Esta guía reúne ocho problemas: cuatro situaciones y una variación de cada una.
**Tu tarea es escribir modelos completos**, con un objetivo, restricciones y
dominios. No hace falta encontrar las mejores decisiones numéricas.

En cada situación ya sabemos qué se quiere conseguir: por ejemplo, gastar lo
menos posible o impartir tantas horas como permitan los recursos. Tu trabajo
es construir las expresiones que representen ese propósito y las condiciones
que debe cumplir la decisión.

Las cifras son didácticas y todos los datos necesarios están en los enunciados.
No necesitas conocimientos previos de café, aviación, organización de eventos
o redes neuronales. Aquí no trabajaremos con probabilidad ni con métodos para
resolver los modelos.

## Elige una situación

Cada situación tiene dos páginas: **práctica** y **modelo general**. Intenta
primero los problemas. La segunda página explica cómo conservar el razonamiento
cuando hay más ingredientes, aviones, talleres o ejemplos.

- **Café.** Elige cuánto comprar de cada origen para preparar una mezcla.
  Después cambia la venta: solo puedes comprar paquetes completos.

  [[opt-practica-cafe|Intentar los problemas de café]] · [[opt-modelo-cafe|Consultar el modelo de una mezcla]].

- **Vuelos.** Asigna un avión con suficientes asientos a cada vuelo.
  Después añade una prohibición de operación sin perder las condiciones anteriores.

  [[opt-practica-vuelos|Intentar los problemas de vuelos]] · [[opt-modelo-vuelos|Consultar el modelo de asignación]].

- **Un evento.** Elige qué talleres ofrecer dentro del presupuesto y del tiempo
  disponible. En la variante también decides cuánto dura cada uno.

  [[opt-practica-evento|Intentar los problemas del evento]] · [[opt-modelo-evento|Consultar el modelo de talleres y duraciones]].

- **Una red neuronal.** Ajusta una regla para aproximar los puntajes de claridad
  de varios clips de audio. Después limita el tamaño de sus pesos.

  [[opt-practica-red|Intentar los problemas de clips de audio]] · [[opt-modelo-red|Consultar el modelo de ajuste de la salida]].

## Qué debes entregar en cada ejercicio

1. **Datos.** Explica qué cantidades conoces y en qué unidades se expresan.
2. **Decisiones.** Define qué representa cada variable, sus unidades y los
   valores que puede tomar.
3. **Expresiones.** Explica cómo calculas lo que quieres optimizar y cómo
   representas cada condición del relato. Comprueba las unidades antes de sumar.
4. **Modelo completo.** Reúne objetivo, restricciones y dominios. Escríbelo
   primero con parámetros y después sustituye los datos del ejercicio.

Usa un renglón por restricción y conserva cada condición, aunque otra parezca
implicarla. Las restricciones deben salir del relato: no hace falta probar
combinaciones ni encontrar el óptimo para saber cuáles escribir.

## Primero intenta plantearlo

Escribe un primer intento antes de abrir las pistas. Si te atoras, consulta
la primera y vuelve a tu hoja; pasa a la segunda si todavía necesitas ayuda.
Deja la respuesta para comparar con lo que hayas escrito.

- **Pista 1**: Los mismos datos del relato, ordenados.
- **Pista 2**: Una pregunta para dirigir tu atención.
- **Respuesta**: La construcción del modelo, sin resolverlo.

Las ayudas empiezan cerradas y puedes abrirlas por separado. Trabaja un
problema por vez; no necesitas terminar los ocho en una sesión. Después de
revisar la pareja de problemas, consulta su modelo general.

## Cómo comprobar tu planteamiento

- ¿Cada variable es una decisión y cada parámetro es un dato?
- ¿Cada condición del relato aparece en el modelo completo?
- ¿Las unidades coinciden y los signos expresan lo que dice la historia?
- ¿El modelo permite las opciones válidas y excluye las prohibidas?
- ¿La misma formulación seguiría funcionando con más elementos?

Las páginas generales muestran también cómo escribir el mismo modelo en
**forma estándar**, siguiendo las convenciones del curso:

- Para los modelos lineales, maximizar y escribir restricciones con $\le$,
  conservando los dominios.
- Para los modelos convexos, minimizar una función convexa, escribir las
  desigualdades convexas como $g(x)\le0$ y conservar las igualdades afines, si las hay.

Cambiar la presentación debe conservar las decisiones permitidas y cuáles
se prefieren.

Si necesitas recuperar el método, vuelve a [[la-bitacora-del-taller|separar datos y decisiones]] o a [[el-modelo-del-taller|construir un modelo completo]].

## Tiempo y siguiente paso

Reserva aproximadamente 45 minutos por pareja, unas tres horas si haces las
cuatro con sus modelos generales. Es un banco de práctica para varias sesiones;
el tiempo depende de tus intentos y de las ayudas que necesites.

Después, [[opt-construir-objetivo|en 6.6 construirás y justificarás también la función objetivo]].
