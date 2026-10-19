---
id: markov-que-es-una-cadena
title: "Clase 1 · Qué es una cadena"
nav_title: Qué es una cadena
summary: "Qué es una cadena de Markov y cómo se usa con un texto: la probabilidad que hace falta, el problema original de Markov, ajustar la matriz contando, predecir multiplicando y generar texto."
status: ready
estimated_time: 199m
tags: [markov, probabilidad, cadenas]
prerequisites: [juegos]
---

# Clase 1 · Qué es una cadena

**En español, después de una «q» casi siempre viene una «u». ¿Cuánto de un
texto se explica mirando solo la letra anterior, y qué se puede hacer con
eso?** Al final tendrás la respuesta contada en el *Quijote* completo. Y un
programa que escribe texto «a su estilo».

> [!TIP]
> **Míralo correr: el generador de texto.** Escribe texto del *Quijote*
> símbolo por símbolo, con memoria 0, 1, 2 o 3. Para cada símbolo muestra
> el contexto, su fila de probabilidades, el uniforme $u$ sorteado y dónde
> cae en la suma acumulada.
>
> **▶ [Abre el generador](../_assets/generador_texto.html#h=2&semilla=2034&largo=200&paso=148)**. La página 6 lo explica.

## Lo que traes

Esta clase usa tres cosas de unidades anteriores. Si un renglón no te
suena, vuelve a su página.

- **Una probabilidad dentro de un modelo.** En
  [[cuando-decide-un-dado|Cuando decide un dado]], $\Pr(a\mid s)$ decía qué
  tan probable era cada resultado del dado en el estado $s$, y esas
  probabilidades sumaban 1. Aquí cada **estado** tendrá su lista de
  probabilidades de **qué sigue**.
- **Un promedio de muchas repeticiones.** En
  [[simular-en-vez-de-evaluar|Simular partidas]], Monte Carlo plano jugaba
  muchas partidas al azar y promediaba su resultado. Aquí simularemos
  muchas **réplicas** para comprobar una cuenta.
- **Una $P$ que dice a dónde lleva el ambiente.** En
  [[de-consecuencias-a-refuerzo|De consecuencias a refuerzo]] apareció la
  forma $\langle S,A,P,R,\gamma\rangle$. Su $P$ es la misma que estudia esta
  unidad, pero sin acciones: solo **qué estado sigue a cuál**.

Lo que necesitas de probabilidad (evento, probabilidad condicional,
independencia) **no se da por sabido**: lo construye la primera página, con
números de una frase.

## Qué vas a poder hacer al terminar esta clase

- Explicar la **propiedad de Markov** como independencia **condicional**:
  el pasado no agrega nada **dado** el presente. Y por qué eso no es
  independencia.
- **Ajustar una cadena contando** en un texto, decir qué maximiza ese
  conteo y qué pasa con lo que nunca se vio.
- Elegir **qué es el estado**: memoria 0, 1 o 2. Y explicar qué gana y qué
  pierde una memoria mayor con datos limitados.
- **Predecir** la probabilidad de cada estado exactamente $t$ pasos
  después. A mano, con el algoritmo y
  simulando réplicas con su error.
- **Generar texto** con la cadena ajustada y relacionarlo con las
  aproximaciones de Shannon.

---

## El hilo de la clase

**El texto es una trayectoria observada.** Contar en él da frecuencias y una
matriz estimada, $\widehat P$. Que el texto lo haya generado una cadena es
una hipótesis útil, no un hecho. La matriz que contamos es la de la cadena
que solo mira la letra anterior y que hace más probable lo que leímos.

Cada idea se dice primero **en general**, con $k$ estados y cualquier
alfabeto. Después se sigue a mano en una frase del *Quijote*, **«Con la
iglesia hemos dado, Sancho»**, con dos estados, V (vocal) y C (consonante),
en ese orden. Y se corre en el libro completo.

**Las páginas 1 y 2 son de conceptos,** sin simulación. Desde la 3, cada
idea se resuelve de tres formas: a mano en la frase, con un algoritmo que
sirve para cualquier tamaño y simulando.

## Recorrido

Seis páginas, en orden. La 1 da la probabilidad y la 2, la cadena en
general: matriz, vectores y dimensiones. Las demás la usan con el texto.

**Los minutos son de lectura.** Cada página cierra con uno o dos
ejercicios finales con pistas y respuesta plegadas: resolverlos toma
tiempo aparte, que no está en la tabla.

::: table {#mkv-ruta-1 title="Las páginas de esta clase"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 33m | **Lo que necesitas de probabilidad.** Evento, probabilidad condicional, independencia e independencia condicional, contadas en la frase |
| 2 | 30m | **La cadena de Markov, en general.** La definición formal, la matriz $k\times k$, las distribuciones como vectores fila, las dimensiones de cada producto, $P^t$ y cómo se mueve una cadena |
| 3 | 37m | **El problema de Markov.** Por qué las letras no son tiradas de un dado; la cadena V/C, la probabilidad de una trayectoria, matrices de 2 y 3 estados, cómo se muestrea una fila y las rachas |
| 4 | 38m | **Ajustar contando.** Contar transiciones da la matriz más verosímil; lo que nunca se vio, el suavizado y cuánta memoria aguantan los datos |
| 5 | 30m | **Predecir.** La probabilidad de cada estado exactamente $t$ pasos después: con un árbol, con un vector por una matriz y simulando |
| 6 | 31m | **Generar texto.** Escribir al estilo del corpus muestreando fila tras fila, con más o menos memoria |
| 7 | 120m, aparte | **Tarea.** Tres videos, tres ejercicios de la clase y uno que adelanta la próxima |
:::

1. [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]]
2. [[mkv-cadena-en-general|La cadena de Markov, en general]]
3. [[mkv-el-problema-de-markov|El problema de Markov]]
4. [[mkv-ajustar-contando|Ajustar contando]]
5. [[mkv-predecir|Predecir]]
6. [[mkv-generar-texto|Generar texto]]

Aparte del recorrido: [[tarea-que-es-una-cadena|la tarea de la clase 1]].

## El generador de texto

Una página aparte, sin nada que instalar, donde se ve correr el algoritmo
de la página 6. No se cuenta en el tiempo de la clase.

- [El generador de texto](../_assets/generador_texto.html): elige la memoria,
  la semilla y el largo, y avanza un símbolo a la vez con ▶.

## Qué no cubre esta clase

- **Qué pasa a la larga.** Si la distribución se estabiliza o si olvida de
  dónde salió. Aquí solo se observa en una matriz y queda como pregunta
  abierta.
- **Decidir** entre varias matrices y **estados que no se ven** tampoco
  están aquí.

Empieza por [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]].
