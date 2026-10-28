---
id: mkv-hacia-refuerzo
title: "Hacia el aprendizaje por refuerzo"
nav_title: "Hacia refuerzo"
summary: "Qué cambia cuando el estado se ve o no y el modelo se conoce o no: el mapa de dos ejes que lleva al aprendizaje por refuerzo."
status: ready
estimated_time: 18m
tags: [markov, ocultas, refuerzo]
---

# Hacia el aprendizaje por refuerzo

**¿Qué le falta a lo que ya sabes para llegar al aprendizaje por refuerzo?**

Al terminar tendrás:

- **Un mapa de dos ejes:** si el estado se ve y si el modelo se conoce, con la clase donde viste cada casilla.
- **Dos formas de no conocer:** no ver el estado y no conocer el modelo. Y por qué mirar no es explorar.
- **Tres cosas que se pueden aprender:** el modelo, los valores o la política.
- **Una analogía con su límite:** el modelo de lenguaje como política, y por qué solo no es refuerzo.
- **La pregunta que falta:** cómo decidir bien sin conocer el modelo.

## Lo que traes

- **Decidir viendo el estado.** En [[mkv-el-mdp|El proceso de decisión de Markov]] y [[mkv-bellman|La ecuación de Bellman]] tenías escritas $P(s'\mid s,a)$ y $r(s,a)$. Con ellas calculaste $V_\pi$, $Q_\pi(s,a)$ y $V^*$ (@mkv-c3-def-valor, @mkv-c3-def-q, @mkv-c3-def-optimo).
- **Decidir sin verlo.** En [[mkv-decidir-sin-ver|Decidir sin ver el estado]] elegiste con la creencia $b=\Pr(\text{lluvia})$. En el problema de un día: llevar el paraguas si $b>1/4$, y mirar conviene si $1/6<b<1/2$.
- **Aprender un modelo.** En [[mkv-ajustar-contando|Ajustar contando]] estimaste $P$ contando. En [[mkv-aprender-lo-oculto|Aprender un modelo oculto]] viste la idea de Baum-Welch.
- **Predecir la palabra.** En [[mkv-lenguaje-pequeno|Un modelo de lenguaje pequeño]] el modelo daba la distribución de la siguiente palabra.
- **El vocabulario del agente.** En [[de-consecuencias-a-refuerzo|De consecuencias a refuerzo]], de la unidad de agentes: estado, observación, acción, política y recompensa.
- **Qué usa esta página:** $\pi$, $V_\pi$, $Q_\pi$, $V^*$, $Q^*$ y la creencia $b_t$. No hay cuentas nuevas.

---

## 1 · Dibujar el mapa de dos ejes

**Piensa: para decidir, en la clase 3 y en esta, ¿qué tuviste siempre, aunque no vieras el clima?**

Siempre tuviste el modelo. En la clase 3, $P(s'\mid s,a)$ y $r(s,a)$ venían escritas. En esta, $\mu_0$, $P$ y $B$ del paraguas, y los costos del día. Lo que cambió fue si veías el estado. Cada pregunta es un eje.

- **¿Se ve el estado?** Si se ve, la política elige con $s$. Si no, elige con las señales, resumidas en la creencia $b_t$.
- **¿Se conoce el modelo?** Conocerlo es tener escritas las transiciones, las emisiones si las hay, y las recompensas. Si no, hay que sacar lo necesario de la experiencia.

Con estado oculto, el problema es un POMDP: proceso de decisión de Markov parcialmente observable (*partially observable Markov decision process*). Arriba a la derecha se conoce; abajo a la derecha, no.

::: table {#mkv-c4-hr-tabla-mapa title="El mapa de dos ejes"}
| El modelo | Estado visible | Estado oculto |
|---|---|---|
| Se conoce | **Planificar un MDP.** Bellman, iterar valores o políticas (clase 3) | **Planificar en un POMDP.** Creencia, filtrar, decidir con $b$ (clase 4) |
| No se conoce | **Refuerzo clásico.** Aprender de episodios | **Refuerzo con observación parcial.** Aprender sin ver el estado ni tener el modelo |
:::

- **Arriba todo se calcula, sin actuar.** A la derecha, sobre la creencia, que es un estado de información, no el clima.
- **Abajo ya no basta calcular.** Los números que pide Bellman no están escritos. Hacen falta datos de interacción, propios o registrados.

::: figure {#mkv-c4-fig-mapa-2x2 title="El mapa de dos ejes, con dónde se vio cada casilla"}
![Cuadro de dos por dos. Columnas: estado visible y estado oculto. Renglones: modelo conocido y modelo desconocido. Arriba a la izquierda, «Planificar un MDP», con la marca «clase 3: Bellman, iterar valores y políticas». Arriba a la derecha, «Planificar en un POMDP», con la marca «clase 4: creencia, filtrar, decidir con b». Estas dos casillas van rellenas: ya se vieron. Abajo a la izquierda, «Refuerzo clásico», con «falta: el modelo; se aprende de episodios». Abajo a la derecha, «Refuerzo con observación parcial», con «falta: el modelo y el estado». Las dos de abajo van solo con borde punteado: no se han visto. Fuera de las casillas, una flecha horizontal sobre el renglón de arriba dice «se deja de ver el estado», y una vertical a la izquierda dice «se deja de conocer el modelo».](../_assets/mkv-c4-mapa-2x2.svg)
:::

::: exercise {#mkv-c4-hr-ej-ubica title="Ubica tres problemas del curso"}
¿En qué casilla va cada uno? (a) El pasillo mojado de la clase 3. (b) El día del paraguas con la creencia. (c) El mismo pasillo, pero sin saber con qué probabilidad resbalas al correr.
:::

::: hint {#mkv-c4-hr-pista-ubica of="mkv-c4-hr-ej-ubica" title="¿Qué está escrito?"}
En cada caso, ¿ves el estado? ¿Tienes $P$ y $r$ escritas?
:::

::: answer {#mkv-c4-hr-resp-ubica of="mkv-c4-hr-ej-ubica"}
- **(a)** Planificar un MDP: ves la casilla y tienes $P$ y $r$.
- **(b)** Planificar en un POMDP: no ves el clima, pero tienes $\mu_0$, $P$, $B$ y los costos.
- **(c)** Refuerzo clásico: ves la casilla, pero te falta una parte de $P$.
:::

---

## 2 · Separar dos formas de no conocer

**Piensa: ¿mirar por la ventana es lo mismo que probar una acción para ver qué pasa?**

No. Reducen dos ignorancias distintas.

- **No conocer el estado.** El modelo está escrito; falta saber el estado de hoy. Lo reduces con señales: un paraguas lleva $b_0(\text{lluvia})$ a $9/11$, y dos lo llevan a $621/703$. Ninguna señal cambia lo que sabes de $P$ o de $B$.
- **No conocer el modelo.** Faltan las probabilidades y las recompensas. No hay ventana que las muestre. Hay que **aprender de la experiencia**: juntar corridas y contar.

::: remark {#mkv-c4-hr-obs-mirar title="Mirar no es explorar"}
- **Mirar** informa sobre el estado de hoy, con el modelo conocido. Su costo y su beneficio se calculan antes: en el problema de un día, mirar conviene estrictamente si $1/6<b<1/2$.
- **Explorar** es elegir una acción, a veces una que parece peor, para informarte de lo que no conoces. Esa información mejora el modelo, los valores o la política de después.
:::

Las dos formas se tocan en [[mkv-aprender-lo-oculto|Aprender un modelo oculto]]. Baum-Welch estima $P$ y $B$ solo con señales. Calcula conteos esperados con las creencias sobre los estados de toda la secuencia. Pero ahí nadie actúa ni recibe recompensas: las señales llegan solas. Es aprender un modelo, no aprendizaje por refuerzo.

> [!WARNING]
> **Error típico:** «mirar es explorar, porque gano información». **Mirar informa del estado de hoy; explorar, de cómo responden las acciones.** Con el modelo conocido no hay nada que explorar.

::: exercise {#mkv-c4-hr-ej-informacion title="Clasifica tres formas de ganar información"}
Para cada caso, di si reduce la incertidumbre del estado, si aprende el modelo actuando o si lo aprende sin actuar.

- **(a)** Ver el cielo antes de salir.
- **(b)** Correr diez veces en el pasillo para estimar cuánto resbalas.
- **(c)** Correr Baum-Welch sobre un año de señales del paraguas.
:::

::: hint {#mkv-c4-hr-pista-informacion of="mkv-c4-hr-ej-informacion" title="¿Qué cambia después?"}
Después de cada caso, ¿cambió lo que sabes de hoy o lo que sabes de $P$?
:::

::: answer {#mkv-c4-hr-resp-informacion of="mkv-c4-hr-ej-informacion"}
(a) Reduce la incertidumbre del estado. (b) Aprende el modelo actuando: es explorar. (c) Aprende el modelo sin actuar: nadie eligió las señales.
:::

---

## 3 · Elegir qué se aprende

**Piensa: si no conoces el modelo, ¿necesitas aprenderlo entero antes de decidir?**

No necesariamente. Se pueden aprender tres cosas distintas.

::: table {#mkv-c4-hr-tabla-aprender title="Tres cosas que se pueden aprender"}
| Qué se aprende | Cómo lo obtuviste en el curso | Qué permite |
|---|---|---|
| El modelo: $P$, $r$ y, si hay, $B$ | $P$ contando (clase 1); $P$ y $B$ con Baum-Welch (clase 4); $r$, nunca | Planificar como en la clase 3 |
| Los valores: $Q_\pi$, $V^*$, $Q^*$ | Con Bellman y el modelo escrito (clase 3) | Con $Q^*$, elegir sin el modelo |
| La política $\pi$ | La codiciosa de $V^*$ (clase 3) | Actuar directamente |
:::

- **$Q^*$ basta y $V^*$ no.** Para comparar acciones con $V^*$ necesitas $r(s,a)$ y $P(s'\mid s,a)$. Con $Q^*(s,a)$ comparas acciones directamente.
- **En la clase 3 todo se calculaba.** $V_\pi$ salía de un sistema lineal y $V^*$ de Bellman, con $P$ y $r$ a la mano.
- **En refuerzo esos números se estiman de episodios.** Un episodio es una corrida de principio a fin. $V_\pi(s)$ se estima promediando los retornos desde $s$ con esa política.

Eso trae dos cosas que no había:

- **Interacción.** El agente elige una acción y el ambiente responde con un estado y una recompensa. Los datos dependen de lo que hizo; no llegan solos, como las señales del paraguas.
- **Explorar frente a explotar.** Explotar es usar la acción que hoy parece mejor. Explorar es probar otra para aprender, aunque hoy cueste más. Si nunca exploras, una acción mal estimada al inicio puede no corregirse nunca.

::: exercise {#mkv-c4-hr-ej-q title="Compara V y Q sin modelo"}
Tienes $V^*=(-5,-2)$ del pasillo, pero no $P$ ni $r$. ¿Puedes decir qué hacer en la casilla 1? ¿Y si tuvieras $Q^*(1,\text{caminar})$ y $Q^*(1,\text{correr})$?
:::

::: hint {#mkv-c4-hr-pista-q of="mkv-c4-hr-ej-q" title="¿Qué pide comparar dos acciones?"}
Con $V^*$, ¿qué tienes que sumar a cada acción para compararlas?
:::

::: answer {#mkv-c4-hr-resp-q of="mkv-c4-hr-ej-q"}
Con $V^*$ sola no puedes: comparar caminar y correr pide $r(1,a)+\sum_{s'}P(s'\mid1,a)V^*(s')$. Con $Q^*(1,\cdot)$ eliges la acción con el número mayor, sin $P$ ni $r$.
:::

---

## 4 · Leer el modelo de lenguaje como política

**Piensa: un modelo de lenguaje elige la siguiente palabra según el texto. ¿Eso ya es aprendizaje por refuerzo?**

Por sí solo, no. La analogía sirve para leer cómo se describen los modelos que se afinan con refuerzo. Ojo: no es lo que hizo la página 6.

::: table {#mkv-c4-hr-tabla-lenguaje title="El modelo de lenguaje con las piezas del refuerzo"}
| Pieza | En la analogía | En la página 6 |
|---|---|---|
| Estado | El texto hasta ahora | La categoría oculta |
| Acción | La siguiente palabra, elegida | La palabra era una señal emitida |
| Política | $\pi(\text{palabra}\mid\text{texto})$: el modelo | Solo la predicción $b_tPB$ |
| Ambiente | Algo que responde a lo escrito | No hay |
| Recompensa | Una calificación del resultado | No hay |
:::

- **La transición es trivial.** El siguiente estado es el texto con la palabra pegada.
- **Con ambiente y recompensa se puede afinar con refuerzo.** Si alguien califica cada respuesta, esa calificación es la recompensa, y la política se ajusta para recibir más.
- **En la página 6 nadie elegía ni calificaba.** Las palabras salían de un estado oculto.

> [!WARNING]
> **Error típico:** «predecir la siguiente palabra es aprendizaje por refuerzo». **Predecir es la pregunta de filtrar y predecir.** Refuerzo pide acciones con consecuencias y una recompensa que las califique.

::: exercise {#mkv-c4-hr-ej-teclado title="Encuentra la pieza que falta"}
El teclado de tu celular sugiere la siguiente palabra con un modelo de lenguaje. (a) Nadie registra si aceptas la sugerencia. ¿Qué piezas del refuerzo faltan? (b) Ahora se registra si la aceptas, y eso se usa para ajustar el modelo. ¿Qué cambió?
:::

::: hint {#mkv-c4-hr-pista-teclado of="mkv-c4-hr-ej-teclado" title="¿Quién responde?"}
¿Hay algo que responda a la sugerencia y un número que la califique?
:::

::: answer {#mkv-c4-hr-resp-teclado of="mkv-c4-hr-ej-teclado"}
(a) Faltan la respuesta del ambiente y la recompensa: es solo predecir. (b) Tú eres el ambiente que responde, y aceptar o no es la recompensa. Ahora sí se puede plantear como refuerzo.
:::

---

## 5 · Nombrar la pregunta que falta

**Piensa: después de cuatro clases, ¿qué no sabes hacer todavía?**

Decidir bien sin conocer el modelo. Para decidir, siempre tuviste $P$, $B$ y las recompensas escritas. Esta clase deja tres cosas fuera, a propósito:

- **No da un algoritmo de refuerzo.** No estima $Q$ de episodios ni trata la exploración con un método.
- **No resuelve el POMDP en general.** El problema de un día se resolvió a mano. La ecuación sobre creencias se escribió, sin demostrar garantías para ella.
- **No toca la casilla de abajo a la derecha,** donde se suman las dos dificultades.

::: exercise {#mkv-c4-hr-ej-quitar title="Quita un dato de la clase 3"}
Quieres el valor de caminar–correr en el pasillo, pero no tienes $P$ ni $r$. Solo puedes recorrer el pasillo con esa política. ¿Qué datos cambias por qué?
:::

::: hint {#mkv-c4-hr-pista-quitar of="mkv-c4-hr-ej-quitar" title="¿Qué es el valor?"}
¿Cómo se define $V_\pi(s)$ en la clase 3?
:::

::: answer {#mkv-c4-hr-resp-quitar of="mkv-c4-hr-ej-quitar"}
Cambias $P$ y $r$ por episodios. $V_\pi(s)$ es el retorno esperado desde $s$. Recorres muchas veces desde $s$ con caminar–correr, sumas las recompensas, que son negativas, y promedias. El promedio se acerca a $(-5,-2)$.
:::

---

## Ejercicios

::: exercise {#mkv-c4-hr-ej-cuatro-casos title="Clasifica cuatro problemas en el mapa"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

**Cambia una idea:** la casilla no viene dada; la decides tú con los dos ejes.

- **(a)** Un robot de almacén ve su posición exacta. Su meta, el costo de cada movimiento y la probabilidad de que falle están escritos.
- **(b)** El mismo robot, pero un sensor ruidoso le da la posición con error. El modelo sigue escrito, con la tabla de errores del sensor.
- **(c)** Un termostato nuevo lee la temperatura exacta. No sabe qué tan rápido se calienta la casa. Paga por consumo y por incomodidad.
- **(d)** Un sistema de recomendaciones no ve el gusto del usuario; solo ve sus clics. Tampoco sabe cómo responde el usuario a cada recomendación.

1. **Ubica** cada caso en una casilla del mapa.
2. **Justifica** con los dos ejes: qué se ve y qué se conoce.
3. **Nombra** qué calcularías en (a) y en (b).
4. **Elige** qué conviene que aprenda el termostato para decidir sin modelo: el modelo, los valores o la política. Di por qué tiene que explorar.
5. **Decide:** en (b), el robot puede pagar por una lectura exacta de su posición. ¿Eso es explorar?
:::

::: hint {#mkv-c4-hr-pista-cuatro-casos-1 of="mkv-c4-hr-ej-cuatro-casos" title="Pista 1 · ¿Qué preguntas le haces a cada caso?"}
¿Qué recibe el agente en cada paso? ¿Qué números pide Bellman, y cuáles vienen escritos?
:::

::: hint {#mkv-c4-hr-pista-cuatro-casos-2 of="mkv-c4-hr-ej-cuatro-casos" title="Pista 2 · ¿Tu borrador separa los dos ejes?"}
En cada justificación, ¿dijiste qué falta: el estado de hoy, las probabilidades o las dos? En tu entregable 5, ¿la lectura cambia lo que sabes de las probabilidades?
:::

::: answer {#mkv-c4-hr-resp-cuatro-casos of="mkv-c4-hr-ej-cuatro-casos" title="Respuesta · Cuatro casillas, una por caso"}
**1. Ubica.** (a) Planificar un MDP. (b) Planificar en un POMDP. (c) Refuerzo clásico. (d) Refuerzo con observación parcial.

**2. Justifica.**

- **(a)** Ve su posición y tiene $P$ y $r$.
- **(b)** No ve su posición, pero tiene $P$, los costos y la tabla del sensor, que hace de $B$.
- **(c)** Ve la temperatura, pero no tiene $P$.
- **(d)** No ve el gusto ni tiene el modelo.

**3. Nombra.** En (a), $V^*$ con Bellman y su política codiciosa. En (b), la creencia sobre la posición con el filtro, y decidir con ella.

**4. Elige.** Los valores $Q^*$: con ellos elige la acción sin saber cómo se calienta la casa. Aprender el modelo también serviría, pero después habría que planificar. Tiene que explorar porque los datos dependen de lo que hace. Si siempre usa la acción que hoy parece mejor, nunca sabe qué pasa con las otras.

**5. Decide.** No es explorar. Es mirar: reduce la incertidumbre de la posición de hoy con el modelo conocido. No cambia lo que sabe de $P$ ni del sensor.
:::

**Punto de control:** debes poder ubicar un problema en el mapa con sus dos ejes, distinguir mirar de explorar, decir qué se aprende cuando falta el modelo y explicar por qué un modelo de lenguaje solo no es refuerzo.

---

## Lo que hay que llevarse

- **Dos ejes, cuatro casillas.** ¿Se ve el estado? ¿Se conoce el modelo? La clase 3 vivió en planificar un MDP; esta clase, en planificar en un POMDP.
- **Dos formas de no conocer.** Sin ver el estado, filtras: un paraguas da $9/11$ y dos dan $621/703$. Sin el modelo, aprendes de la experiencia.
- **Mirar no es explorar.** Mirar informa del estado, con el modelo conocido; en el día del paraguas conviene si $1/6<b<1/2$. Explorar actúa para aprender el modelo, los valores o la política.
- **Baum-Welch aprende un modelo sin actuar.** No hay acciones ni recompensas: no es refuerzo.
- **Se aprende el modelo, los valores o la política.** Con $Q^*$ eliges sin el modelo; con $V^*$ sola, no.
- **Lo nuevo del refuerzo:** interacción, episodios en vez de $P$ y $r$, y explorar frente a explotar.
- **El modelo de lenguaje como política es una analogía.** Sin ambiente que responda y sin recompensa, no hay refuerzo.

Si ya no tienes $P$ ni $r$, solo episodios, ¿cómo decides bien?

Continúa con [[mkv-resumen-lo-oculto|Resumen de la clase: el formulario]].
