---
id: computabilidad
title: Computabilidad e incompletitud
nav_title: Computabilidad
summary: Qué puede demostrar un sistema formal y qué puede calcular una máquina — dos preguntas que resultaron ser la misma.
status: ready
tags: [computabilidad, logica, godel, turing]
---

# Computabilidad e incompletitud

Las dos unidades anteriores preguntaron por la inteligencia desde afuera. [[historia-ia|La historia de la IA]]
contó cuántas veces se prometió una máquina que piensa y qué pasó cada vez.
[[filosofia-ia|La filosofía de la IA]] leyó a quienes discuten hacia dónde hay que empujarla.
Las dos son discusiones abiertas: se puede estar de un lado o del otro.

Esta unidad cambia de terreno. Hace una pregunta más chica, más vieja y —a
diferencia de las anteriores— **contestada**: ¿qué puede calcular una máquina?
La respuesta se demostró antes de que existiera la primera computadora, y no es
que todavía no sepamos cómo hacer ciertas cosas. Es que hay cosas que **ninguna
máquina va a poder hacer nunca**, y eso no es una limitación de la tecnología
sino un teorema.

## Por qué esto está en un curso de inteligencia artificial

Porque fija el techo. El curso entero, según [[el-curso|El curso]], trata la IA como un
problema de decisión bajo incertidumbre: dado un agente, un ambiente y un
objetivo, qué puede saber, qué puede calcular y qué le conviene hacer. Los
módulos que vienen se ocupan del **qué le conviene hacer**. Este se ocupa del
**qué puede calcular**, y lo hace primero porque es el que pone un límite duro:
ningún método posterior —por más datos, por más cómputo, por más listo que
sea— va a cruzarlo.

Hay una razón más. Casi todas las afirmaciones grandilocuentes sobre lo que la
inteligencia artificial va a lograr se hacen sin saber que esta frontera
existe. Saber dónde está es la diferencia entre un límite real y uno que solo
parece.

## Qué vas a poder hacer al terminar

- Explicar qué es una máquina de Turing y por qué sirve como definición de «lo
  que una computadora puede hacer».
- Distinguir un problema difícil de uno **indecidible**, y dar el ejemplo
  canónico: el problema de la parada.
- Reconstruir el argumento de diagonalización y reconocerlo cuando reaparece,
  porque reaparece en los tres resultados centrales de la unidad.
- Explicar intuitivamente qué dicen los dos teoremas de incompletitud de Gödel
  y qué **no** dicen, que es donde casi todo el mundo se equivoca.

## De qué está hecha la unidad

Son tres resultados y el aparato mínimo para entenderlos. Los tres son del
mismo medio siglo y los tres usan, por debajo, el mismo truco.

| | Resultado | La pregunta que contesta |
|---|---|---|
| 1 | Los **axiomas de Peano** (Peano, 1889) y qué es una teoría aritmética | ¿Qué es exactamente un sistema formal, y qué se le está pidiendo? |
| 2 | Los **teoremas de incompletitud** (Gödel, 1931) | ¿Puede un sistema formal demostrar todas las verdades de la aritmética? ¿Puede al menos demostrar que no se contradice? |
| 3 | La **máquina de Turing** y el **problema de la parada** (Turing, 1936) | ¿Puede un procedimiento mecánico decidir cualquier enunciado matemático? |

El orden no es cronológico por casualidad: cada uno necesita al anterior. Y la
herramienta que los une es la **diagonalización**, el argumento con el que
Cantor había demostrado, cuarenta años antes que Gödel, que hay más números
reales que naturales.

## Cómo se prepara

La unidad abre con un video que cuenta los tres resultados como una sola
historia, que es como conviene verlos la primera vez. Está asignado como tarea
para la sesión del **miércoles 26 de agosto**, en dos versiones equivalentes
—una en inglés y otra en español— y con ocho preguntas con las que hay que
llegar a clase. Los detalles están en la tarea, al final de esta página.

Vale la pena decir por qué es un video y no una lectura. Estos tres resultados
se explican mucho mejor con animación que con prosa: la diagonalización, en
particular, es un dibujo. Las fuentes originales vienen después, cuando ya
sepas qué estás leyendo.

## Recorrido

Esta unidad está en construcción. Por ahora existe la preparación; las páginas
de sesión se agregan conforme avancemos.
