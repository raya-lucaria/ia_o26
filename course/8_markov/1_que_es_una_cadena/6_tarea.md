---
id: tarea-que-es-una-cadena
title: "Tarea de la clase 1 · Tres videos y cuatro ejercicios"
nav_title: Tarea
summary: "Tres videos (dos de repaso y uno que adelanta la próxima clase), tres ejercicios de la clase y uno nuevo: qué pasa si dejas correr la cadena."
status: ready
estimated_time: 120m
tags: [markov, tarea, video, practica]
---

# Tarea de la clase 1 · Tres videos y cuatro ejercicios

**¿Puedes hacer sin ayuda lo que la clase hizo con la frase, en problemas que
cambian una idea?**

La tarea tiene tres partes: **tres videos**, **tres ejercicios** de las
páginas y **uno nuevo** que adelanta la próxima clase. Es la tarea para la
próxima sesión: sirve para comprobar que puedes hacerlo solo.

---

## 1 · Ver tres videos

Los tres están en inglés; los subtítulos automáticos ayudan si los
necesitas. Velos en este orden: el primero repasa, el segundo cuenta la
historia y la abre, y el tercero adelanta la próxima clase.

1. **[Markov Chains: Data Science Basics](https://www.youtube.com/watch?v=prZMpThbU3E)**
   — ritvikmath, unos diez minutos. **Repaso:** estados, la matriz de
   transición y cómo se multiplica para predecir varios pasos, como en
   [[mkv-predecir|Predecir]].
2. **[The Strange Math That Predicts (Almost) Anything](https://www.youtube.com/watch?v=KZeIEiBrT_w)**
   — Veritasium, poco más de media hora. **Repaso e historia:** la disputa
   entre Nekrásov y Markov y el conteo de vocales en *Eugenio Oneguin*, como
   en [[mkv-el-problema-de-markov|El problema de Markov]], y casi al final el
   texto predictivo de [[mkv-generar-texto|Generar texto]]. En medio habla de
   Monte Carlo y de cómo ordena Google las páginas; al final, de cuántas
   veces hay que barajar un mazo. Todo eso ya pregunta **qué pasa a la
   larga**.
3. **[Markov Chain Stationary Distribution](https://www.youtube.com/watch?v=4sXiCxZDrTU)**
   — ritvikmath, corto. **Adelanto:** la distribución que deja de cambiar
   al multiplicar por la matriz. Velo **después** del último ejercicio de
   esta página.

> [!WARNING]
> **El tercer video escribe $\pi$ para esa distribución.** Es la letra de los
> libros de cadenas. En este curso $\pi$ es la política de un agente, así que
> aquí se escribe $\mu$: el video dice $\pi P=\pi$ y nosotros, **$\mu P=\mu$**.

**Páralos cuando reconozcas algo de la clase.** Si un número de un video no
coincide con el de una página, quédate con el de la página: los nuestros
salen del texto ruso como lo contó Markov y de nuestro *Quijote*.

### Con qué llegas a clase

Pudiendo explicar con tus palabras, sin leerlas:

1. Qué sostenía Nekrásov y qué mostró Markov en contra.
2. Por qué «sin memoria» no quiere decir «independiente».
3. Cómo se predicen varios pasos con la matriz, y cómo escribe texto un
   modelo que solo mira la letra o la palabra anterior.
4. Qué es una distribución que no cambia al multiplicar por la matriz, y
   una pregunta sobre **qué pasa a la larga** que la clase no contestó.

---

## 2 · Resolver tres ejercicios de la clase

Cada página cierra con `## Ejercicios`: problemas **modificados**, que cambian
una idea del ejemplo resuelto o el juguete por uno más grande. **Todos sirven
para estudiar;** de tarea van estos tres, los que tocan lo central de la
clase. Están en su página, con dos pistas y la respuesta plegadas.

**Haz primero un esfuerzo propio, sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT. Después de intentarlo, abre las pistas una por una y
vuelve a tu hoja antes de consultar la respuesta.** La pista 1 te ayuda a
organizar el problema; la pista 2 revisa tu borrador.

1. **Leer una matriz.** Pasa un grafo de tres estados a su matriz, en
   [[mkv-el-problema-de-markov|El problema de Markov]] (@mkv-c1-ej-grafo-tres).
2. **Ajustar contando.** Ajusta una cadena de tres símbolos, con y sin
   suavizado, en [[mkv-ajustar-contando|Ajustar contando]]
   (@mkv-c1-ej-tres-simbolos).
3. **Predecir.** Predice dos pasos con tres estados, en
   [[mkv-predecir|Predecir]] (@mkv-c1-ej-tres-estados).

**Si te atoras,** vuelve a la sección de la página que resolvió el mismo
problema con la frase. Cada ejercicio cambia una sola idea respecto de ese
ejemplo, y su enunciado dice cuál.

---

## 3 · Adelantar la próxima clase

**Piensa: si dejas correr la cadena mucho tiempo, ¿importa dónde empezó?**

La clase solo predijo tres pasos. Este ejercicio deja correr la cadena más
lejos y plantea la pregunta de la próxima clase. No tiene que salirte la
explicación: basta con que veas qué pasa y lo digas.

::: exercise {#mkv-c1-ej-a-la-larga title="Deja correr la cadena"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

Usa la matriz de la frase, $\widehat P$, con filas $(2/11,\ 9/11)$ y
$(2/3,\ 1/3)$, y el Python de PREDECIR de [[mkv-predecir|Predecir]].
**Cambia una idea:** en lugar de tres pasos, mira ocho, y desde los dos
inicios.

1. **Calcula.** $\Pr(S_t=V)$ para $t=0,\dots,8$, desde C, $\mu_0=(0,1)$, y
   desde V, $\mu_0=(1,0)$, con tres decimales.
2. **Compara.** ¿Qué pasa con la distancia entre las dos sucesiones?
3. **Cambia la matriz.** Haz lo mismo con la cadena que **siempre cambia de
   estado**, con filas $(0,\ 1)$ y $(1,\ 0)$, desde V. Y desde
   $\mu_0=(1/2,\ 1/2)$.
4. **Pregunta.** ¿Qué tiene la primera matriz que no tiene la segunda?
   Escribe una conjetura en una frase.
5. **Comprueba con el tercer video.** Después de verlo, multiplica
   $\mu=(22/49,\ 27/49)$ por $\widehat P$. ¿Qué sale, y a qué número se
   acercaban tus dos sucesiones?
:::

::: hint {#mkv-c1-pista-a-la-larga-1 of="mkv-c1-ej-a-la-larga" title="Pista 1 · ¿Qué llamada a predecir te da cada renglón?"}
¿Qué $\mu_0$ y qué $t$ le pasas a `predecir` para cada número? ¿Puedes pedir
los nueve pasos de una vez con un ciclo?
:::

::: hint {#mkv-c1-pista-a-la-larga-2 of="mkv-c1-ej-a-la-larga" title="Pista 2 · ¿Comparaste en el mismo paso?"}
¿Restaste las dos sucesiones paso a paso? En la segunda matriz, ¿puede la
cadena quedarse donde está? Al multiplicar el vector del video, ¿usaste
vector fila a la izquierda, como en PREDECIR?
:::

::: answer {#mkv-c1-resp-a-la-larga of="mkv-c1-ej-a-la-larga" title="Respuesta · Una se acerca y la otra oscila"}
**1. Las dos sucesiones.**

- **Desde C:** 0.000, 0.667, 0.343, 0.500, 0.424, 0.461, 0.443, 0.452, 0.448.
- **Desde V:** 1.000, 0.182, 0.579, 0.386, 0.479, 0.434, 0.456, 0.446, 0.451.

**2. Se acercan.** La distancia baja de 1 en $t=0$ a 0.003 en $t=8$: cada
paso la deja en menos de la mitad. En esta matriz, después de unos pasos
ya casi no importa dónde empezó.

**3. La otra no.** Desde V la probabilidad de vocal es 1, 0, 1, 0, …: nunca
se asienta. Desde $(1/2,\ 1/2)$ se queda en $1/2$ en cada paso.

**4. Una conjetura posible.** En la primera, desde cada estado se puede
quedarse o cambiar; en la segunda, siempre se cambia y la cadena alterna.
Cuándo una cadena olvida su inicio, y bajo qué condiciones, es la pregunta de
la próxima clase.

**5. No cambia.** $(22/49,\ 27/49)\,\widehat P=(22/49,\ 27/49)$, y
$22/49\approx0.449$: el número al que se acercaban las dos sucesiones de
la frase. Es la distribución del tercer video, con $\mu$ en lugar de
$\pi$.
:::

---

**Punto de control:** deberías poder resolver los tres ejercicios de la
clase sin abrir las respuestas, explicar las cuatro preguntas de los videos
y llegar con tu conjetura del último ejercicio.

Regresa al [[markov-que-es-una-cadena|índice de la clase]].
