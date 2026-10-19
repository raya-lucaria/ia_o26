---
id: markov-que-es-una-cadena
title: "Clase 1 · Qué es una cadena"
nav_title: Qué es una cadena
summary: "Qué es una cadena de Markov y cómo se usa con un texto: la probabilidad que hace falta, el problema original de Markov, ajustar la matriz contando, predecir multiplicando y generar texto."
status: ready
estimated_time: 160m
tags: [markov, probabilidad, cadenas]
prerequisites: [juegos]
---

# Clase 1 · Qué es una cadena

**En español, después de una «q» casi siempre viene una «u». ¿Cuánto de un
texto se explica mirando solo la letra anterior, y qué se puede hacer con
eso?** Al final tendrás la respuesta contada en el *Quijote* completo. Y un
programa que escribe texto «a su estilo».

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
- **Predecir** con $\mu_t=\mu_0\widehat P^{\,t}$ la probabilidad de cada
  estado exactamente $t$ pasos después. A mano, con el algoritmo y
  simulando réplicas con su error.
- **Generar texto** con la cadena ajustada y relacionarlo con las
  aproximaciones de Shannon.

---

## El hilo de la clase

**El texto es una trayectoria observada.** Contar en él da frecuencias y una
matriz estimada, $\widehat P$. Que el texto lo haya generado una cadena es
una hipótesis útil, no un hecho. $\widehat P$ es la cadena de memoria 1 que
hace más probable lo que leímos.

Todo se sigue a mano en una frase del *Quijote*: **«Con la iglesia hemos
dado, Sancho»**. Tiene dos estados, V (vocal) y C (consonante), en ese
orden. Cada idea se dice después **en general**, con $k$ estados y cualquier
alfabeto, y se corre en el libro completo.

**Cada idea se resuelve de tres formas:** a mano en la frase, con un
algoritmo que sirve para cualquier tamaño, y simulando. La primera página es
de conceptos y va sin simulación.

## Recorrido

Cinco páginas, en orden. La 1 y la 2 son de conceptos; la 3, la 4 y la 5
son algoritmos.

::: table {#mkv-ruta-1 title="Las páginas de esta clase"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 32m | **Lo que necesitas de probabilidad.** Evento, probabilidad condicional, independencia e independencia condicional, contadas en la frase |
| 2 | 35m | **El problema de Markov.** Por qué las letras no son tiradas de un dado; la definición de cadena, su matriz, su grafo y cómo se muestrea una fila |
| 3 | 35m | **Ajustar contando.** Contar transiciones da la matriz más verosímil; lo que nunca se vio, el suavizado y cuánta memoria aguantan los datos |
| 4 | 30m | **Predecir.** La probabilidad de cada estado exactamente $t$ pasos después: con un árbol, con un vector por una matriz y simulando |
| 5 | 28m | **Generar texto.** Escribir al estilo del corpus muestreando fila tras fila, con más o menos memoria |
:::

1. [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]]
2. [[mkv-el-problema-de-markov|El problema de Markov]]
3. [[mkv-ajustar-contando|Ajustar contando]]
4. [[mkv-predecir|Predecir]]
5. [[mkv-generar-texto|Generar texto]]

## Qué no cubre esta clase

- **Qué pasa a la larga.** Si la distribución se estabiliza o si olvida de
  dónde salió. Aquí solo se observa en una matriz y queda como pregunta
  abierta.
- **Decidir** entre varias matrices y **estados que no se ven** tampoco
  están aquí.

Empieza por [[mkv-lo-que-necesitas|Lo que necesitas de probabilidad]].
