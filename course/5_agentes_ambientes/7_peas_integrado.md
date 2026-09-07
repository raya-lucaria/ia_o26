---
id: peas-integrado
title: Integrar PEAS — una ficha que no se contradice
nav_title: Integrar PEAS
summary: Un PEAS completo conecta desempeño, entorno, actuadores y sensores para la misma decisión y expone los supuestos.
status: draft
estimated_time: 25m
tags: [peas, integracion, modelado, ejercicios]
---

# Integrar PEAS — una ficha que no se contradice

Ahora sí escribe PEAS completo. No es rellenar cuatro casillas independientes:
P debe poder juzgar la trayectoria que E hace posible; A debe contener solo
acciones permitidas por E; S debe declarar la información que realmente llega
desde E. Una inconsistencia entre dos letras es un diagnóstico útil.

::: figure {#aa-peas-integrado title="PEAS es una sola especificación vista desde cuatro lados"}
![Los cuatro campos P, E, A y S se conectan alrededor de una misma decisión de estrategia de carrera](_assets/aa-peas.svg)
:::

## Caso guiado: pits en una carrera simulada

**Decisión:** antes de la siguiente vuelta, ¿seguir, entrar a pits o cambiar el
ritmo dentro del rango permitido?

::: figure {#aa-ilus-carrera-peas title="Una decisión de estrategia tiene información, acciones y consecuencias"}
![Un equipo original de estrategia observa una carrera lluviosa y compara dos rutas abstractas iluminadas](_assets/ilus-estrategia-carrera.jpg)
:::

*(Esta imagen es una ilustración generada, no una transmisión ni datos de una carrera real.)*

| Letra | Ficha mínima | Comprobación |
|---|---|---|
| **P** | Menor tiempo total, sin infringir reglas ni agotar combustible o desgaste seguro. | No basta ganar una vuelta rápida. |
| **E** | Pista, clima, rivales, reglamento, combustible, llantas, equipo de pits y simulador. | Lluvia y rivales cambian sin permiso del agente. |
| **A** | Seguir, entrar en ventana de pits, elegir compuesto permitido, ajustar ritmo o mantenerlo. | No puede cambiar el clima ni reparar fuera de pits. |
| **S** | Tiempo, posición, telemetría estimada, combustible y reporte de clima retrasado. | El clima real y desgaste exacto no llegan necesariamente. |

### Prueba de coherencia 1: de P a A

Si P penaliza quedarse sin combustible, ¿A permite una acción que reduzca ese
riesgo? Si no, quizá añadiste una restricción que el agente no puede cumplir. A
veces es correcto: una tarea puede ser imposible desde cierto estado. Pero debes
decirlo y no culpar después al agente.

### Prueba de coherencia 2: de E a S

Si E contiene lluvia, ¿S entrega lluvia perfecta, un reporte retrasado o nada?
Cada respuesta cambia qué puede inferir el agente. No copies una variable de E
a S solo porque sería conveniente verla.

### Prueba de coherencia 3: de A a P

Si A permite «no hacer nada», P debe evaluar cuándo esa abstención es prudente.
Si A solo permite entrar o seguir, no castigues después al agente por no elegir
una tercera acción inexistente.

## Cambiar una letra cambia el problema

| Cambio | Lo que **no** cambia | Lo que sí cambia |
|---|---|---|
| Añadir cámara que ve toda la pista | P: tiempo y seguridad deseados. | S: menos información oculta; quizá basta menos memoria. |
| Permitir escoger ritmo continuo | E: clima, pista y rivales. | A: espacio de acción más fino; hacen falta decisiones de precisión. |
| Agregar costo alto de llantas | E y P, si el costo importa al desempeño. | La política preferible y la recompensa que usarías después. |

Este cuadro es la razón para separar letras: puedes cambiar una sin fingir que
todas las demás cambiaron solas.

## Clínica: encuentra el choque entre letras

Un bot de museo tiene P = «recoger todas las fichas y volver en menos de diez
minutos sin choques». E dice que hay puertas con horario. A dice «moverse al
norte, sur, este u oeste». S dice «cámara local y reloj». Falta una decisión
importante: ¿cómo sabe si una puerta está abierta? Hay tres respuestas válidas:

1. Añadir a S un indicador de puerta visible o el horario publicado.
2. Declarar en E que el horario es fijo y conocido; el agente puede usarlo como
   conocimiento previo, pero hay que decir dónde lo almacena.
3. Aceptar que S no basta y diseñar luego una creencia/estrategia de exploración.

Lo inválido es escribir «el bot evita puertas cerradas» como si ese dato hubiera
llegado mágicamente.

## Ejercicios

::: exercise {#aa-ej-peas-integrado title="Completa y prueba una ficha"}
Para una cartera **simulada** de tres activos ficticios, escribe P, E, A y S.
Incluye costo de transacción ficticio, la acción «no operar» y al menos un dato
que S no entrega. Después escribe una prueba de coherencia entre dos letras.
:::

::: answer {#aa-resp-peas-integrado of="aa-ej-peas-integrado"}
Una respuesta posible: **P** aumentar valor simulado dentro de un límite de
riesgo y costo; **E** precios ficticios, saldo, mercado simulado y reglas;
**A** comprar una unidad, vender una unidad o no operar; **S** precios retrasados,
saldo y estimación de volatilidad, pero no precios futuros. Coherencia: si P
incluye costo, E debe definirlo y A debe permitir no operar para evitar un costo
sin beneficio. No es consejo financiero: solo una tarea de decisión simulada.
:::

::: exercise {#aa-ej-peas-integrado-reparar title="Repara una contradicción"}
Caso: P exige «nunca chocar»; E contiene peatones que aparecen detrás de una
esquina; A solo permite avanzar; S es una cámara frontal. Señala dos problemas y
propón una modificación mínima para cada uno.
:::

::: answer {#aa-resp-peas-integrado-reparar of="aa-ej-peas-integrado-reparar"}
Primero, A no permite frenar, girar ni esperar, así que no ofrece forma de evitar
un peligro. Segundo, S no ve peatones detrás de la esquina; «nunca» puede ser
imposible bajo esa información. Podrías añadir freno a A y sensor lateral a S;
o suavizar P a un riesgo mínimo bajo límites declarados. Las dos correcciones
cambian tareas distintas y por eso conviene nombrarlas.
:::

## Siguiente bloque

PEAS deja la tarea especificada. Ahora sí podemos diagnosticar las propiedades
de su entorno, una por una y con evidencia:
[[diagnosticar-el-entorno|las siete perillas del entorno]].
