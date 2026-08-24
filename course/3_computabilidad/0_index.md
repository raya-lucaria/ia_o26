---
id: computabilidad
title: Computabilidad e incompletitud
nav_title: Computabilidad
summary: Qué puede demostrar un sistema formal y qué puede calcular una máquina — dos preguntas que resultaron ser la misma.
status: ready
estimated_time: 45m
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

## La preparación: un video

Para la sesión del **miércoles 26 de agosto** hay que ver y entender un video que
cuenta los tres resultados como una sola historia, que es como conviene verlos la
primera vez.

Hay **dos versiones del mismo video** y eliges una:

| Versión | Video | Duración |
|---|---|---|
| Inglés, la original | [Math's Fundamental Flaw](https://www.youtube.com/watch?v=HeQX2HjkcNo) | 34 min |
| Español, doblaje oficial | [Las Matemáticas Tienen Una FALLA Descomunal](https://www.youtube.com/watch?v=RRg38oNQ9vk) | 33 min |

Son el mismo contenido y **ninguna de las dos es la versión buena**: escoge la que
te deje entender mejor, no la que suene más seria. Si quieres la original pero el
inglés te cuesta, YouTube trae subtítulos automáticos y traducción de subtítulos,
y puedes apoyarte en un traductor o en cualquier herramienta que uses
normalmente. Nada de eso está prohibido: la única condición es que **entiendas lo
que viste**.

Y ojo con esa condición, porque no es un video para dejar de fondo. Son más de
treinta minutos densos, con media docena de ideas que se apoyan una en la otra, y
verlo sin entenderlo no sirve de nada en la sesión. Pausa, regresa, y busca por tu
cuenta lo que no quede claro.

Vale la pena decir por qué es un video y no una lectura. Estos tres resultados se
explican mucho mejor con animación que con prosa: la diagonalización, en
particular, es un dibujo. Las fuentes originales vienen después, cuando ya sepas
qué estás leyendo.

## Con qué tienes que llegar a la sesión

Llega pudiendo explicar **con tus palabras** estas ocho cosas. Son sobre las que
vamos a discutir:

1. Qué es una **máquina de Turing**.
2. Qué es un **axioma** y qué es una **teoría aritmética**.
3. Qué es **computabilidad**.
4. Qué es el ***halting problem***, el problema de la parada.
5. Qué es **diagonalización**.
6. Qué dice intuitivamente el **primer teorema de incompletitud de Gödel**, y qué
   significa eso para las matemáticas — la intuición, no la demostración formal.
7. Lo mismo para el **segundo teorema de Gödel**.
8. Qué dicen intuitivamente los **axiomas de Peano**.

**Dos avisos, para que no busques respuestas donde no están.** El segundo teorema
el video lo menciona de pasada, en una sola frase, así que para contestar la 7
vas a tener que investigar un poco por tu cuenta. Y los axiomas de Peano no
aparecen en el video, ni por nombre: la 8 se busca aparte, completa.

Explicarlo con tus palabras es el punto. Si solo puedes repetir la frase del
video, todavía no está. No hay cuestionario ni nada que entregar: la tarea es
llegar entendiendo.

## Recorrido

Esta unidad está en construcción. Por ahora existe la preparación; las páginas
de sesión se agregan conforme avancemos.
