---
id: ml-repaso-que-es-aprender
title: "Repaso: qué es aprender"
nav_title: "Repaso"
summary: "Aprender según Mitchell y dónde se mide el desempeño, supervisado contra no supervisado, y el aprendizaje de máquina visto de cerca dentro de la IA."
status: ready
estimated_time: 20m
tags: [aprendizaje-maquina, repaso, mitchell, supervisado, representacion]
---

# Repaso: qué es aprender

**Un programa que se equivoca cero minutos en todas las entregas que ya vio, ¿aprendió a predecir cuánto tarda una entrega?**

Al terminar tendrás:

- **La definición de Mitchell:** tarea, experiencia, desempeño y dónde se mide.
- **Por qué un error de cero en lo visto no basta:** con cifras.
- **Supervisado contra no supervisado:** por lo que trae la experiencia.
- **Un mapa dentro de la IA:** quién elige lo que el modelo ve de cada entrada ($\phi$) y si se arma en capas.

~20 min de lectura, más lo que tardes en resolver los ejercicios; esta clase no tiene notebook.

> **Lo que traes**
> - Mínimos cuadrados, ${f_\beta(x)=\beta_0+\beta_1x}$ y seis entregas: [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]].
> - Error absoluto medio, $\mathrm{MAE}$, en minutos: [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]].
> - La taxonomía de la IA (@taxonomia-ia): [[que-es-inteligencia|Qué es la inteligencia]].

Estas ideas son el punto de partida de la unidad; aquí quedan por escrito, con el ejemplo de la unidad 6.

## 1 · Medir el aprendizaje en casos nuevos

Cada punto es una entrega (km, minutos): el programa vio (1, 15), (2, 17), (3, 23) y (4, 25), de la unidad 6. Las de 5 y 6 km llegarán después.

::: figure {#ml-c0-tres-reglas-en-lo-visto title="Tres reglas en las cuatro entregas que vio"}
![Cuatro entregas vistas, de 1 a 4 km, tiempo contra distancia. Memorizar copia el tiempo de la entrega vista más cercana y acierta las cuatro, error medio 0 min; la recta 11 + 3.6x falla en promedio por 0.8; el promedio fijo de 20 min, por 4. A la derecha, sin sus tiempos reales, lo que cada regla anuncia para 5 y 6 km: memorizar 25 y 25, el promedio 20 y 20, la recta 29 y 32.6.](../_assets/ml-c0-tres-reglas-en-lo-visto.svg)
:::

Ajustamos con esas cuatro:

- Memorizar copia el tiempo de la entrega vista más cercana. Para 5 y 6 km, es la de 4 km: anuncia 25.
- El promedio fijo de lo visto, 20 min, es el punto de comparación (*benchmark*): la regla más simple que usa datos.
- Mínimos cuadrados busca la recta con menor error promedio al cuadrado en las cuatro, con $n=4$:

$$\beta^\star\in\operatorname*{arg\,min}_{\beta_0,\beta_1}\ \frac1n\sum_{i=1}^{n}\bigl(y_i-\beta_0-\beta_1x_i\bigr)^2$$

Las cuatro distancias no son todas iguales, así que el mínimo es único: ${\beta^\star=(11,\ 3.6)}$, la recta ${11+3.6x}$.
Para 5 km anuncia ${11+3.6\cdot5=29}$ min.

Es el mismo problema de la unidad 6, ahora resuelto solo con las cuatro primeras; con las seis salía ${10.6+(134/35)x}$.

La recta se ajusta minimizando cuadrados, pero el error lo reportamos como MAE, en minutos: la clase 4 explica por qué la pérdida con que se ajusta y la medida con que se reporta pueden ser distintas.

En las vistas, memorizar gana: error medio 0, recta 0.8, promedio 4 min.

**Piensa: en las entregas de 5 y 6 km, que ninguna regla vio, ¿qué regla se equivocará menos?**

::: figure {#ml-c0-memorizar-contra-ajustar title="Cero error en lo que vio, siete minutos en lo nuevo"}
![Arriba: las cuatro entregas vistas; error medio de memorizar 0, de la recta 0.8 y del promedio 4. Abajo: las dos nuevas, de 5 y 6 km, tardaron 31 y 33 min; memorizar anuncia 25 y falla en promedio por 7; el promedio anuncia 20 y falla por 12; la recta anuncia 29 y 32.6 y falla por 1.2.](../_assets/ml-c0-memorizar-contra-ajustar.svg)
:::

En las nuevas, el MAE es: recta 1.2, memorizar 7, promedio 12 min. El orden se invierte: la recta pasa al primer lugar.

Memorizar no fracasa del todo: le gana al promedio. Lo que falla es usar su cero en lo visto como prueba de que acierta en lo nuevo. Estas dos entregas bastan como contraejemplo, pero no para medir cada regla.

Las nuevas, además, están más lejos que las vistas (extrapolar). En la clase 1 verás miles de casos nuevos, no dos.

::: definition {#ml-c0-def-aprender title="Aprender, según Mitchell"}
Un programa **aprende** de la experiencia $E$ respecto de una clase de tareas $T$ y una medida de desempeño $P$ si su desempeño en las tareas de $T$, medido con $P$, mejora con la experiencia $E$.

(Mitchell, 1997; citado en Goodfellow, Bengio y Courville, 2016, §5.1.)

Las letras $T$, $E$ y $P$ viven solo en esta definición. En el resto de la unidad, ${E[\cdot]}$ es la esperanza y $\Pr(\cdot)$ la probabilidad.
:::

La tarea es anunciar minutos; la experiencia, entregas con su tiempo; el desempeño, el error medio en minutos.

::: remark {#ml-c0-obs-desempeno-en-casos-nuevos title="Dónde se mide el desempeño"}
El desempeño se mide en casos que el programa **no usó** para ajustarse y parecidos a los que encontrará al usarse.

El error en lo visto, por sí solo, no demuestra acierto en casos nuevos. Memorizar lo lleva a cero y falla por 7 minutos en las nuevas (@ml-c0-memorizar-contra-ajustar).
La clase 1 nombra ese error; la clase 2 enseña a medirlo.
:::

La recta salió de optimizar los **parámetros** $\beta_0$ y $\beta_1$, y así seguirá la unidad. La clase 1 agrega una restricción de capacidad; la clase 3, un lagrangeano con multiplicador $\mu\ge0$, como en la unidad 6.

> [!WARNING]
> Lectura equivocada: «si el error en los datos que ya vio es cero, el programa aprendió».
>
> Lectura correcta: **el error en lo que ya vio, por sí solo, no demuestra que el programa acierte en casos nuevos; el desempeño se mide en casos nuevos.**

::: exercise {#ml-c0-ej-aprende-o-recuerda title="Decide si aprendió"}
Cada semana llegan 10 entregas más: misma zona, distancias parecidas. En 4 semanas, el error medio en lo visto baja de 3 a 1 minuto.
En entregas de la semana siguiente, aún no vistas, permanece en 6 minutos cada semana.

Según @ml-c0-obs-desempeno-en-casos-nuevos, ¿aprende? Di la tarea, la experiencia y el desempeño.
:::

::: hint {#ml-c0-pista-aprende-o-recuerda-1 of="ml-c0-ej-aprende-o-recuerda" title="Pista 1 · Dónde medir"}
¿En qué entregas se mide el desempeño de la tarea «predecir»?
:::

::: answer {#ml-c0-resp-aprende-o-recuerda of="ml-c0-ej-aprende-o-recuerda" title="Respuesta · No mejora donde importa"}
La tarea es anunciar los minutos de las entregas que vendrán. La experiencia son las entregas acumuladas. El desempeño es el error medio en entregas que no vio: sigue en 6 minutos.

No se observa mejora en el desempeño medido; con estos datos no hay evidencia de que aprenda. Bajar de 3 a 1 en lo visto no basta. Puede reproducir mejor lo que ya vio sin cambiar lo que anuncia para entregas nuevas.
:::

## 2 · Distinguir supervisado de no supervisado

Un niño distingue gatos de perros con fotos etiquetadas; ¿y sin etiquetas?

A las mismas seis entregas añadimos paquetes y zona. Cada punto es una entrega: arriba, en (distancia, tiempo), con la recta de la sección 1, ajustada solo con la distancia y las cuatro primeras; abajo, en (distancia, paquetes).

::: figure {#ml-c0-con-y-sin-y title="Las mismas seis entregas, con respuesta y sin ella"}
![Arriba: tabla con zona, distancia, paquetes y tiempo, y tiempo contra distancia con la recta 11 + 3.6x. Abajo: la misma tabla sin la columna de tiempo, y paquetes contra distancia con dos agrupaciones marcadas, una por distancia, cerca hasta 3.5 km y lejos después, y otra por paquetes, pocos, de 2 a 3, y muchos, de 9 a 11.](../_assets/ml-c0-con-y-sin-y.svg)
:::

**Piensa: si borras la columna del tiempo, ¿qué pregunta puedes seguir haciéndole a estas seis entregas?**

Con tiempos comparamos cada anuncio con uno observado y ajustamos ${11+3.6x}$. Sin tiempos ya no preguntas cuánto tarda una entrega, sino cómo se reparten. Ninguna agrupación es «la verdadera», pero cada una es buena según su criterio.

::: definition {#ml-c0-def-supervisado title="Supervisado y no supervisado"}
En el aprendizaje **supervisado**, la experiencia son $n$ pares $(x_i,y_i)$, ${i=1,\dots,n}$: cada observación trae sus entradas $x_i$ y la respuesta $y_i$. La tarea es anunciar $y$ para una $x$ nueva.

Si $y$ es una cantidad que se quiere estimar (minutos, un precio), es regresión. Si es una categoría que se quiere identificar (a tiempo o tarde, gato o perro), es clasificación. Esto vale aunque las categorías se guarden como números, por ejemplo 0 y 1.

En el aprendizaje **no supervisado**, la experiencia son solo las entradas $x_i$, ${i=1,\dots,n}$, sin respuesta. La tarea es describir cómo se reparten: qué grupos forman, en qué direcciones varían más, dónde se acumulan.
:::

Aquí $x_i$ reúne distancia y paquetes; $y_i$ indica minutos.

El no supervisado puede optimizar un objetivo sin respuestas; los dos caben en cualquier nivel de la sección 3.

::: remark {#ml-c0-obs-otras-experiencias title="No son solo dos cajas"}
En aprendizaje por refuerzo el programa actúa y recibe una recompensa, no la respuesta correcta: [[mkv-hacia-refuerzo|Hacia el aprendizaje por refuerzo]].

Predecir la siguiente palabra admite dos lecturas: supervisado, pues la palabra siguiente es la respuesta; no supervisado, pues aprende cómo se reparte el texto.
La respuesta sale del propio texto, sin que nadie la escriba: se llama **autosupervisado**. La frontera se borra (Goodfellow, Bengio y Courville, 2016, §5.1.3).
:::

Esta unidad es de aprendizaje supervisado. Casi todo es regresión, con un primer ejemplo de clasificación desde la clase 1 (los anillos); la clase 4 estudia la clasificación y sus métricas. El no supervisado queda fuera.

> [!WARNING]
> Lectura equivocada: «supervisado significa que alguien vigila el entrenamiento».
>
> Lectura correcta: **supervisado quiere decir que la experiencia trae la respuesta $y$ de cada observación.**

::: exercise {#ml-c0-ej-que-experiencia title="Clasifica la experiencia"}
(a) Predecir precios de casas con ventas pasadas y sus precios; (b) agrupar clientes de una tienda sin categorías previas.

(c) Un robot aprende a caminar con un puntaje según cuánto avanza.

(d) Rellenar palabras borradas al azar de millones de textos.

¿Supervisado, no supervisado o ninguno? Si admite dos lecturas, da ambas.
:::

::: hint {#ml-c0-pista-que-experiencia-1 of="ml-c0-ej-que-experiencia" title="Pista 1 · Lo que trae cada experiencia"}
¿La experiencia trae la respuesta que se quiere anunciar? Si la trae, ¿quién la escribió?
:::

::: answer {#ml-c0-resp-que-experiencia of="ml-c0-ej-que-experiencia" title="Respuesta · Cuatro experiencias distintas"}
(a) Supervisado, regresión. (b) No supervisado. (c) Ninguno: refuerzo; el puntaje premia lo que hizo, no le dice el paso correcto.

(d) Ambas lecturas valen: supervisado si cada palabra borrada es la respuesta; no supervisado si aprende cómo se reparte el texto. La respuesta sale del propio texto: es autosupervisado.
:::

## 3 · Ubicar el aprendizaje de máquina dentro de la IA

Abajo, vista de cerca, está la caja del aprendizaje de máquina (*machine learning*) de la @taxonomia-ia. La caja que la unidad de historia rotula «Aprendizaje máquina» es la misma que aquí llamamos aprendizaje de máquina.

::: figure {#ml-c0-jerarquia title="El aprendizaje de máquina, visto de cerca dentro de la IA"}
![Cinco ramas hermanas de la inteligencia artificial; la del aprendizaje de máquina se amplía y adentro muestra tres rectángulos anidados: aprendizaje de máquina con la regresión logística, aprendizaje de representaciones con un autoencoder poco profundo y aprendizaje profundo con una red de varias capas.](../_assets/ml-c0-jerarquia.svg)
:::

**Piensa: ¿toda la inteligencia artificial aprende de datos?**

No: hay enfoques de IA que no requieren aprender de datos; las otras ramas de la @taxonomia-ia pueden usar aprendizaje, pero no dependen de él. Solo dentro del aprendizaje hay anidamiento estricto.
La IA no es una cebolla.

La figura anida: aprendizaje de máquina (regresión logística, unidad 6) ⊃ aprendizaje de representaciones (*representation learning*; autoencoder poco profundo) ⊃ aprendizaje profundo (*deep learning*; red multicapa).

El autoencoder reconstruye su entrada pasando por un código más corto.

La figura de [[que-es-inteligencia|Qué es la inteligencia]] anida aprendizaje de máquina ⊃ redes profundas, sin el escalón intermedio de representaciones.

Entre niveles cambia quién elige cada pieza y cómo se arma. Cada tira es un sistema; una caja rellena indica qué aprende con datos.

::: figure {#ml-c0-quien-elige-phi title="Quién elige qué: cuatro maneras de construir un sistema"}
![Cuatro tiras. Reglas: todo a mano. Clásico: la representación fi de x a mano y el predictor con parámetros beta ajustado con datos. Representaciones: fi de x y el predictor, los dos con datos. Profundo: capa 1, capa 2 y más, una sobre otra, que juntas forman fi de x, y el predictor, todo con datos.](../_assets/ml-c0-quien-elige-phi.svg)
:::

La representación $\phi(x)$ es lo que el modelo ve de cada entrada: si eliges $(1,x,x^2)$, ve distancia y cuadrado; para 3 km, obtienes $\phi(3)=(1,3,9)$.

En el clásico eliges $\phi$ a mano; en representaciones la elige el ajuste; en profundo la compone en capas. En los tres, el ajuste elige $\beta$.

Elegir $x^2$ conserva la linealidad del modelo en $\beta$; la clase 1 define qué significa ser lineal en $\beta$.
Esta unidad elige $\phi$ a mano; aprenderla abre la unidad de redes.

> [!WARNING]
> Lectura equivocada: «usar $x^2$ como variable ya saca al modelo de los modelos lineales, o ya es aprendizaje profundo».
>
> Lectura correcta: **si una persona eligió $x^2$ y el ajuste solo elige $\beta$, es aprendizaje de máquina clásico, y el modelo sigue siendo lineal en $\beta$.**

::: exercise {#ml-c0-ej-donde-cae title="Ubica cuatro sistemas"}
Ubica en @ml-c0-jerarquia: caja más específica y las que la contienen.

- (a) Sistema experto de diagnóstico con reglas escritas por médicos.
- (b) Regresión sobre $(1,x,x^2)$, columnas que tú elegiste.
- (c) Autoencoder poco profundo: comprime imágenes y su código alimenta una regresión logística.
- (d) Modelo de lenguaje grande basado en un transformer.
:::

::: hint {#ml-c0-pista-donde-cae-1 of="ml-c0-ej-donde-cae" title="Pista 1 · Quién eligió qué"}
En cada sistema, ¿quién decidió lo que el modelo ve de la entrada: una persona o el ajuste con datos? Y si fue el ajuste, ¿en una etapa o en varias?
:::

::: answer {#ml-c0-resp-donde-cae of="ml-c0-ej-donde-cae" title="Respuesta · Cuatro cajas"}
(a) IA, rama de sistemas expertos, fuera del aprendizaje de máquina.

(b) Aprendizaje de máquina clásico: dentro del aprendizaje de máquina, fuera de representaciones.

(c) Aprendizaje de representaciones, dentro del aprendizaje de máquina y de la IA.

(d) Aprendizaje profundo, dentro de representaciones, aprendizaje de máquina e IA. Es una red profunda, un transformer, como en @taxonomia-ia.
:::

::: exercise {#ml-c0-ej-final-repaso-que-es-aprender title="Planea cómo juzgar el sistema en una zona nueva"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

La empresa de la unidad 6 abrirá otra zona urbana. Tiene 200 entregas con zona, distancia, paquetes y minutos; ninguna de la nueva.

La idea nueva es usar el sistema donde no obtuvo su experiencia. No
elijas algoritmo ni calcules. La respuesta desarrolla una opción.

1. Di la tarea, la experiencia y el desempeño.
2. ¿Es supervisado? ¿Cuál es la respuesta $y$?
3. ¿Con qué entregas medirías hoy, antes de abrir? ¿Por qué no basta el error en las 200?
4. Ubica en @ml-c0-quien-elige-phi una recta sobre distancia y paquetes, columnas que tú elegiste.
:::

::: hint {#ml-c0-pista-final-repaso-que-es-aprender-1 of="ml-c0-ej-final-repaso-que-es-aprender" title="Pista 1 · Separar lo que tienes de lo que vendrá"}
¿En qué se parecerán y en qué no las entregas que ya tienes y las que el sistema atenderá?
:::

::: hint {#ml-c0-pista-final-repaso-que-es-aprender-2 of="ml-c0-ej-final-repaso-que-es-aprender" title="Pista 2 · Revisar tu propuesta"}
¿Tu forma de medir conserva esa diferencia, usando solo las columnas que ya tienes? ¿Quién eligió las columnas que ve la recta?
:::

::: answer {#ml-c0-resp-final-repaso-que-es-aprender of="ml-c0-ej-final-repaso-que-es-aprender" title="Respuesta · Medir donde se va a usar"}
**1.** La tarea es anunciar los minutos de entregas en la zona nueva; la experiencia son las 200 entregas. El desempeño es el error medio en minutos en entregas de la zona nueva; se compara con el error de anunciar el promedio, el punto de comparación.

**2.** Es supervisado, regresión; $y$ son los minutos.

**3.** Hoy puedes apartar una zona actual completa como si fuera nueva, o hacerlo con cada zona por turnos. Ajusta con las demás y mide en la apartada. Así imitas el uso: casos de un lugar que el ajuste no vio.

El error en las 200 no basta: el ajuste ya usó esos casos. Apartar al azar parte de las 200 mezclaría las zonas; medirías en zonas que el ajuste sí conoce.
Cuando lleguen entregas reales de la zona nueva, mide también con ellas: más adelante en la unidad esta idea tiene nombre y método.

**4.** Aprendizaje de máquina clásico: tú elegiste $\phi$ y el ajuste elige $\beta$.
:::

**Punto de control:** explica con cifras por qué memorizar gana en lo visto y la recta en lo nuevo.

## Para profundizar

Goodfellow, Bengio y Courville (2016), [*Deep Learning*](https://www.deeplearningbook.org/), MIT Press: capítulo 1, figuras 1.4 y 1.5; §5.1.
Mitchell (1997), *Machine Learning*, McGraw-Hill: capítulo 1.
[[que-es-inteligencia|Qué es la inteligencia]].

## Lo que hay que llevarse

- Aprender mejora con experiencia el desempeño, medido en casos nuevos. El error de memorizar es 0 min en lo visto y 7 en lo nuevo; el de la recta, 0.8 y 1.2; el del promedio, 4 y 12.
- La recta salió de un problema de optimización, y la unidad sigue así.
- Supervisado trae $y$; no supervisado trae solo $x$. Esta unidad es supervisada: casi todo es regresión; hay clasificación desde la clase 1, estudiada en la clase 4.
- No toda la IA aprende de datos; dentro del aprendizaje de máquina cambia quién elige $\phi$ y si se arma en capas.

Continúa con [[ml-clase-1-el-problema|la clase 1, El problema]].
