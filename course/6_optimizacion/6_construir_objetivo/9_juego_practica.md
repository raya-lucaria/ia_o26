---
id: opt-objetivo-juego-practica
title: Elegir una jugada cuando el rival responde
nav_title: Juego · Practicar
summary: "Formular cómo elegir una jugada y comprobar por qué conservar más fichas puede llevarnos a perder."
status: ready
tags: [optimizacion, modelado, juegos, practica]
---

# Elegir una jugada cuando el rival responde

**Queremos ganar, pero no elegimos las jugadas del rival.** Él observa lo que
hacemos y responde buscando su propia victoria. ¿Cómo tener eso en cuenta al
escribir nuestro objetivo?

Usaremos un juego pequeño, con todos los resultados en una tabla. No necesitas
conocer ajedrez ni otro juego de tablero. Tu tarea es **formular cómo elegir**;
no vamos a estudiar todavía un algoritmo para explorar jugadas.

## Problema 9 · Guardar una ficha o sacrificarla

::: exercise {#opt-obj-juego-ej-1 title="Elegir una jugada sabiendo que el rival responderá"}
Tienes dos acciones posibles: **Guardar** una ficha o **Sacrificarla**.
Después juega el rival: observa tu acción y elige una de sus dos respuestas,
llamadas **I** y **D**. Esas son todas las opciones; las letras solo sirven
para distinguirlas.

No hay azar. El juego es **determinista**: una misma combinación de acciones
siempre produce el mismo resultado.

Después de la respuesta rival, los movimientos que faltan son obligatorios.
Ninguno de los jugadores puede cambiar lo que ocurrirá. Por eso podemos dar
una tabla que indica cómo terminará cada combinación:

Las columnas I y D son las respuestas del rival; los valores son tus puntos
finales: +1 si ganas y −1 si pierdes.

| Acción | I | D |
|---|---:|---:|
| Guardar | +1 | −1 |
| Sacrificar | +1 | +1 |

Los puntos representan lo único que te interesa: **ganar**. Recibes +1 por
una victoria y −1 por una derrota; conservar fichas no da puntos. El rival
recibe la puntuación contraria: cuando tú ganas, él pierde, y viceversa.

Ambos conocen las opciones y la tabla. Suponemos que el rival quiere ganar
y que, si tiene una respuesta que le da la victoria, la elige. Conoces lo
que **puede** responder; todavía no ha elegido su respuesta.

Escribe un modelo completo para elegir tu primera acción. Antes de escribir
el objetivo, explica:

- Qué eliges tú y qué elige el rival.
- Cómo compararías dos acciones cuando cada una admite respuestas distintas.
- Si bastaría con mirar el mejor resultado que podrías obtener con cada acción.

Incluye las acciones permitidas y justifica cómo tu objetivo representa el
comportamiento del rival. No hace falta buscar un método para resolverlo.
:::

### Escribe primero tu intento

Anota quién toma cada decisión y qué información conoce. Si te atoras,
abre una pista y vuelve a tu planteamiento antes de seguir.

::: hint {#opt-obj-juego-pista-1a of="opt-obj-juego-ej-1" title="Pista 1 · Quién decide cada jugada"}
Estos son los datos que necesitas separar:

- Tú eliges Guardar o Sacrificar: una fila de la tabla.
- El rival ve esa elección y puede responder I o D: una columna de esa fila.
- Los resultados finales ya se conocen. Las fichas conservadas no dan puntos.

La respuesta rival no es una segunda elección que puedas hacer tú.
:::

::: hint {#opt-obj-juego-pista-1b of="opt-obj-juego-ej-1" title="Pista 2 · Qué puede hacer el rival"}
Si una fila contiene una victoria y una derrota para ti, ¿cuál puede provocar
un rival que quiere ganar? ¿Cómo resumirías entonces lo que esa fila te ofrece?
:::

**Compara la respuesta con tu modelo:** fíjate especialmente en quién controla
cada elección.

::: answer {#opt-obj-juego-resp-1 of="opt-obj-juego-ej-1" title="Respuesta · Tener en cuenta la elección del rival"}
**1. Separar las opciones de las decisiones.** Para poder escribir el modelo
con más acciones, llamamos $A$ al conjunto de nuestras acciones posibles.
Si elegimos una acción $a$, el rival puede responder con alguna de las
opciones del conjunto $B(a)$.

Ambos conjuntos son finitos y no vacíos. La notación $B(a)$ permite que,
en otro juego, nuestras acciones dejen disponibles respuestas distintas.

- $A$: Nuestras acciones permitidas.
- $B(a)$: Respuestas permitidas al rival después de $a$.
- $U(a,b)$: Nuestra puntuación final si jugamos $a$ y el rival responde $b$.

Los conjuntos y la función $U$ son datos conocidos. **Elegimos $a$; el rival
elige $b$ después de observarnos.** Las acciones no tienen unidades físicas.
La función $U$, que llamamos *utilidad*, se mide en los puntos con los que
valoramos el resultado final.

**2. Explicar qué busca el rival.** Aquí su puntuación es el negativo de la
nuestra. Las dos puntuaciones suman cero en cada resultado: por eso se llama
juego de **suma cero**. Tener dos jugadores, por sí solo, no bastaría para
afirmar esto.

En este juego ganar y perder son los únicos resultados. Si el rival puede
hacernos perder, lo hace. En un modelo más general, $U$ podría tomar otros
valores: suponemos que el rival conoce los resultados y elige la respuesta
que le da más puntos a él, es decir, la que nos da menos a nosotros.

**3. Construir el valor de una acción.** Imagina que ya fijamos $a$.
Todavía quedan varias respuestas posibles, pero no podemos escoger la que
más nos convenga. Bajo el comportamiento supuesto, la puntuación que
obtendremos es la menor de las que permite esa acción:

$$v(a)=\min_{b\in B(a)}U(a,b).$$

Así convertimos las puntuaciones de una fila en un solo valor. $v(a)$ se
mide en los mismos puntos que $U$ y se calcula a partir de los datos; no es
una puntuación que podamos elegir libremente.

**4. Escribir el modelo completo.** Ahora sí comparamos nuestras acciones:
queremos la que tenga el mayor valor $v(a)$.

$$
\begin{aligned}
\max_a\quad &v(a)=\min_{b\in B(a)}U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}
$$

El mínimo representa la elección del rival; el máximo, la nuestra. Los
conjuntos $A$ y $B(a)$ indican todo lo que puede jugar cada persona.
No hay otras restricciones de recursos en este relato.

**5. Sustituir los datos.** Abreviamos Guardar con $G$ y Sacrificar con $S$.
Los conjuntos permitidos son:

$$A=\{G,S\},\qquad B(G)=B(S)=\{I,D\}.$$

La tabla da las puntuaciones:

$$U(G,I)=1,\qquad U(G,D)=-1,\qquad U(S,I)=U(S,D)=1.$$

Por tanto, el modelo del ejercicio queda:

$$\max_{a\in\{G,S\}}\min\{U(a,I),U(a,D)\}.$$

Podemos comprobar cómo interpreta la tabla sin desarrollar un algoritmo:

$$v(G)=\min\{1,-1\}=-1,\qquad v(S)=\min\{1,1\}=1.$$

Sacrificar asegura la victoria bajo las reglas dadas. Guardar permite que
el rival elija una respuesta con la que perdemos.

**6. Comprobar qué expresa el objetivo.** Si miráramos solo el mejor resultado
de cada fila, ambas acciones tendrían valor 1. Ese empate ocultaría que
una de ellas deja al rival la posibilidad de derrotarnos.

La utilidad elegida cuenta victorias y derrotas; no valora la duración ni
las fichas conservadas. El mínimo, por su parte, supone que el rival elige
una respuesta que nos perjudica lo más posible. En el problema de horarios
podíamos minimizar una molestia máxima sin suponer que alguien nos atacara;
aquí sí hay otra persona tomando una decisión.

Si quisiéramos aprovechar errores frecuentes de un rival, necesitaríamos
datos sobre sus respuestas y otra descripción de su conducta. La tabla de
resultados no nos dice con qué frecuencia se equivoca: no permite inventar
probabilidades para promediar las columnas.
:::

## Problema 10 · Elegir una jugada contando fichas

::: exercise {#opt-obj-juego-ej-2 title="Comprobar la elección de un programa que cuenta fichas"}
**El juego es el mismo:** conservamos las acciones, las respuestas del rival
y todos los resultados finales del problema 9.

Ahora vamos a revisar un programa que recomienda jugadas. El programa solo
examina la posición que queda justo después de la respuesta rival. Deja de
mirar antes de completar los movimientos obligatorios que llevan a ganar
o perder.

Para valorar esa posición, **cuenta únicamente nuestras fichas**. Llama
$h$ a esa puntuación y recibe estos datos:

Las columnas I y D son las respuestas del rival; los valores se miden en
fichas.

| Acción | I | D |
|---|---:|---:|
| Guardar | 3 | 2 |
| Sacrificar | 0 | 0 |

Su regla está dada: para cada acción toma la menor cantidad de fichas que
podría quedar después de la respuesta rival. Recomienda la acción cuyo
valor así calculado sea mayor.

**Nosotros también conocemos los resultados finales.** Podemos usar la tabla
del problema 9 para comprobar la recomendación. No hay información secreta:
lo que queremos revisar es si la puntuación que usa el programa sirve para
el propósito de ganar.

Para mejorar esa puntuación, contamos además con estas señales observables:

- **Después de Guardar e I**: La llegada a la meta es inevitable: ganaremos.
- **Después de Guardar y D**: Hay un bloqueo inevitable: perderemos.
- **Después de Sacrificar, con I o D**: La llegada a la meta es inevitable: ganaremos.

Son datos del juego pequeño; no necesitas conocer reglas de tablero para
justificarlos. Con esta información:

1. Formula el modelo que representa la regla del programa y comprueba qué
   acción recomienda.
2. Compara esa recomendación con los resultados finales. Explica si conservar
   más fichas basta para elegir bien.
3. Propón una nueva puntuación que use las señales dadas y escribe el modelo
   revisado. Explica qué tendrías que comprobar antes de usarlo en otro juego.
:::

### Escribe primero qué usa el programa

Distingue la información con la que recomienda una jugada de la que usamos
para comprobar si esa recomendación nos lleva a ganar.

::: hint {#opt-obj-juego-pista-2a of="opt-obj-juego-ej-2" title="Pista 1 · Tres datos que cumplen papeles distintos"}

- **Cantidad de fichas**: Es la puntuación del programa actual.
- **Victoria o derrota final**: Permite comprobar su recomendación.
- **Llegada inevitable o bloqueo**: Permite proponer una nueva puntuación.

Las acciones y las respuestas posibles siguen siendo las del problema 9.
La tabla de fichas y la tabla de victorias miden cosas distintas.
:::

::: hint {#opt-obj-juego-pista-2b of="opt-obj-juego-ej-2" title="Pista 2 · Qué debería contar para ganar"}
Si una posición lleva inevitablemente a perder, ¿qué valor debería recibir
en comparación con otra que lleva a ganar? ¿Cambiar esa puntuación modifica
las jugadas permitidas?
:::

**Compara tu respuesta con la propuesta:** separa el modelo del programa,
la comprobación de su resultado y la revisión de su puntuación.

::: answer {#opt-obj-juego-resp-2 of="opt-obj-juego-ej-2" title="Respuesta · Cambiar qué valora el programa"}
**1. Conservar las decisiones y nombrar la posición.** Seguimos eligiendo
una acción $a\in A$; el rival responde con $b\in B(a)$. Llamamos $s(a,b)$
a la posición alcanzada después de esas dos jugadas.

La letra $s$ representa todo lo que ha quedado en el juego en ese momento.
El programa solo extrae un dato de esa posición: $h(s)$, nuestra cantidad
de fichas. Esta puntuación está fijada por la regla del programa y se mide
en **fichas**, mientras que $U(a,b)$ mide puntos por ganar o perder.

Ni la posición ni su puntuación son decisiones libres. Una vez elegidas
las dos jugadas, ambas quedan determinadas.

**2. Construir lo que compara el programa.** Para una acción propia $a$,
la posición final de su examen todavía depende de la respuesta rival.
La regla dada toma la menor puntuación entre esas posiciones:

$$\min_{b\in B(a)}h(s(a,b)).$$

Después compara nuestras acciones mediante ese número. El modelo completo
de su recomendación es:

$$
\begin{aligned}
\max_a\quad &\min_{b\in B(a)}h(s(a,b))\\
\text{sujeto a}\quad &a\in A.
\end{aligned}
$$

El programa aplica la misma forma de protegerse frente a una respuesta
rival, pero reemplaza la utilidad final por su puntuación intermedia.
Eso cambia lo que optimiza, aunque las jugadas permitidas sean las mismas.

**3. Sustituir los datos.** Conservamos los conjuntos del problema 9:

$$A=\{G,S\},\qquad B(G)=B(S)=\{I,D\}.$$

La tabla de fichas establece:

$$
\begin{aligned}
h(s(G,I))&=3, &h(s(G,D))&=2,\\
h(s(S,I))&=0, &h(s(S,D))&=0.
\end{aligned}
$$

El modelo queda:

$$\max_{a\in\{G,S\}}\min\{h(s(a,I)),h(s(a,D))\}.$$

Guardar recibe un valor mínimo de 2 fichas; Sacrificar, de 0. Por tanto,
**el programa recomienda Guardar**. Ha elegido lo mejor según la puntuación
que le dimos.

**4. Comprobar la recomendación.** Como revisores —o *auditores*—, podemos
consultar además los resultados finales. Al hacerlo, encontramos valores
mínimos de −1 para Guardar y +1 para Sacrificar.

La recomendación del programa permite que el rival nos derrote. Conservar
más fichas no basta para ganar: esas fichas pueden quedar en una posición
que lleva a perder. El defecto está en qué valora el programa, no en haber
calculado mal su puntuación.

**5. Construir otra puntuación con las señales dadas.** Necesitamos distinguir
una victoria inevitable de una derrota inevitable. Para cada posición
introducimos dos indicadores conocidos:

- $W(s)$ vale 1 si la señal observada certifica una victoria inevitable,
  y 0 en otro caso.
- $D(s)$ vale 1 si la señal observada certifica una derrota inevitable,
  y 0 en otro caso.

Ambos toman valores en $\{0,1\}$ y, en estos datos, nunca valen 1 a la vez.
Podemos asignar +1 a la victoria certificada y −1 a la derrota certificada
mediante:

$$h'(s)=W(s)-D(s).$$

Esta nueva puntuación usa la escala de utilidad del juego. **Ya no cuenta
fichas.** Las señales del enunciado dan:

$$
\begin{aligned}
h'(s(G,I))&=1, &h'(s(G,D))&=-1,\\
h'(s(S,I))&=1, &h'(s(S,D))&=1.
\end{aligned}
$$

El modelo revisado conserva las acciones y sustituye la puntuación:

$$\max_{a\in A}\min_{b\in B(a)}h'(s(a,b)).$$

Con los conjuntos de este ejercicio, queda:

$$\max_{a\in\{G,S\}}\min\{h'(s(a,I)),h'(s(a,D))\}.$$

Ahora recomienda Sacrificar. La revisión usa hechos observables y la relación
que el enunciado establece entre esos hechos y ganar o perder.

**6. Reconocer hasta dónde sirve la revisión.** En este juego pequeño,
las señales bastan para certificar todos los resultados. En uno más grande,
puede haber posiciones donde ninguna señal se active.

Si $W(s)=D(s)=0$, la nueva puntuación vale cero. Eso significa que no tenemos
una certificación; **no demuestra que el juego terminará en empate**. Haría
falta examinar más jugadas o justificar otra manera de valorar esas posiciones.

Una *función heurística* es una valoración aproximada de posiciones.
Puede ayudarnos cuando no conocemos los resultados finales, pero no garantiza
la misma decisión que tomaríamos si los conociéramos todos.
:::

Después de comparar tus modelos, pasa a [[opt-objetivo-juego-modelo|la formulación general para elegir una jugada]].
