---
id: opt-objetivo-panaderia-practica
title: "¿Cuánto pan conviene producir?"
nav_title: "Panadería: práctica"
summary: "Construir la ganancia de una producción y distinguir criterios para compararla cuando la demanda es incierta."
status: ready
tags: [optimizacion, modelado, practica]
---

# ¿Cuánto pan conviene producir?

Una panadería tiene que preparar el pan antes de saber cuántos clientes
llegarán. Producir más permite atender una demanda alta, pero también cuesta
dinero si las piezas se quedan sin vender.

**Tu tarea es construir los modelos, no encontrar la producción óptima.**
En el primer problema compararás ganancias promedio; en el segundo,
distinguirás dos maneras de protegerse ante la incertidumbre. Los datos son
didácticos. Intenta cada problema antes de abrir sus ayudas.

## Problema 3 · ¿Cuánto esperamos ganar?

::: exercise {#opt-obj-pan-ej-probabilidades title="La producción de mañana"}
Esta noche, la panadería decide cuántas piezas producirá mañana. Puede
preparar entre **0 y 100 piezas enteras**. Una vez elegida la producción,
no puede ajustarla al conocer la demanda.

| Por cada pieza | Pesos |
|---|---:|
| Precio de venta | 8 |
| Costo de producción | 2 |

El costo se paga por **todas las piezas producidas**, incluidas las que no
se venden. Los sobrantes no tienen valor de recuperación. Se vende toda la
cantidad que permitan la producción y la demanda; no se incluyen otros
costos ni ingresos.

Para mañana se consideran dos escenarios:

| Demanda | Probabilidad |
|---|---:|
| 20 piezas | 0.8 |
| 80 piezas | 0.2 |

Se supone que esas probabilidades describen adecuadamente la incertidumbre.
La responsable quiere elegir la producción con la **mayor ganancia monetaria
promedio** según esos datos.

Construye un modelo que permita tomar esa decisión:

1. Distingue los datos de la decisión. Expresa cuántas piezas se venden en
   cada escenario y, a partir de ellas, los ingresos, el costo y la ganancia.
2. Formula el objetivo, las restricciones y los dominios. Explica qué permite
   comparar el promedio y qué garantía no ofrece sobre mañana.
3. Examina si maximizar los ingresos o minimizar solo el costo de producción
   expresa la misma preferencia. Puedes comparar producciones permitidas;
   no necesitas resolver los problemas de optimización.
:::

### Primero intenta plantearlo

Empieza con tu propia formulación. Si no sabes cómo separar las cantidades,
abre la primera pista.

::: hint {#opt-obj-pan-pista-probabilidades-datos of="opt-obj-pan-ej-probabilidades" title="Pista 1 · Qué se elige y qué ocurre después"}
La producción se elige esta noche; la demanda se conoce mañana. Distingue
las piezas producidas de las vendidas: ¿siempre son la misma cantidad?
¿Cuál de las dos determina lo que se paga por producir?
:::

Si ya identificaste esas cantidades, pero no logras relacionarlas, prueba
con la segunda pista.

::: hint {#opt-obj-pan-pista-probabilidades-guia of="opt-obj-pan-ej-probabilidades" title="Pista 2 · Los límites de una venta"}
Piensa primero en una producción mayor que la demanda y después en una
menor. En cada caso, ¿qué impide vender una pieza más? Usa esa observación
para escribir una expresión que funcione en ambos casos.
:::

Compara la respuesta con tu intento: fíjate tanto en las expresiones como
en las razones para elegirlas.

::: answer {#opt-obj-pan-resp-probabilidades of="opt-obj-pan-ej-probabilidades" title="Respuesta · De las ventas a la ganancia"}
**La producción es una sola decisión previa.** Usamos la misma cantidad en
los dos escenarios. Permitir que cambiara con la demanda daría a la panadería
información que todavía no tiene al decidir.

**1. Identificar datos y decisión.** Sea $S$ el conjunto finito no vacío de
escenarios. Para escribir primero un modelo general, usamos estos parámetros:

- $Q\in\mathbb Z_{\ge0}$: Capacidad, en piezas.
- $d_s\in\mathbb Z_{\ge0}$: Demanda del escenario $s$, en piezas.
- $v$: Precio de venta, en pesos/pieza.
- $c$: Costo de producción, en pesos/pieza.
- $p_s$: Probabilidad del escenario $s$.

En este relato, $v>c>0$. Las probabilidades son no negativas y suman uno:

$$p_s\ge0,\qquad \sum_{s\in S}p_s=1.$$

La decisión $q$ cuenta piezas producidas. Debe ser entera, no negativa y no
rebasar $Q$.

**2. Construir lo que ocurre en un escenario.** Si alcanza el pan, se vende
lo que los clientes piden. Si no alcanza, se vende toda la producción.
Por tanto, las piezas vendidas son

$$\min(q,d_s).$$

El ingreso se obtiene multiplicando esas ventas por el precio. El costo,
en cambio, corresponde a toda la producción:

$$
I(q,d_s)=v\min(q,d_s),
\qquad C(q)=cq.
$$

En ambos casos, pesos por pieza multiplicados por piezas dan pesos.
La **ganancia es lo que queda del ingreso después de pagar la producción**:

$$\Pi(q,d_s)=I(q,d_s)-C(q)=v\min(q,d_s)-cq.$$

Puede ser negativa: producir no garantiza vender lo suficiente para
recuperar el costo.

**3. Comparar ganancias promedio.** Una producción tiene una ganancia en
cada escenario. Para obtener el promedio solicitado, ponderamos cada una
por su probabilidad. El modelo general es

$$
\begin{aligned}
\max\quad &\sum_{s\in S}p_s\bigl[v\min(q,d_s)-cq\bigr]\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

El objetivo es la **ganancia esperada**, medida en pesos. Las probabilidades
no tienen unidades, de modo que el promedio conserva la unidad monetaria.
Preferir este promedio es una decisión de la responsable; conocer las
probabilidades permite calcularlo, pero no obliga a elegir ese criterio.

Al sustituir los datos obtenemos

$$
\begin{aligned}
\max\quad
&0.8\bigl[8\min(q,20)-2q\bigr]\\
&\quad+0.2\bigl[8\min(q,80)-2q\bigr]\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

**4. Revisar qué estamos maximizando.** Comparemos dos producciones
permitidas. Esta comprobación no determina cuál es la mejor entre todas.

Las columnas comparan producir 20 y 65 piezas; los resultados están en pesos.

| Resultado | 20 | 65 |
|---|---:|---:|
| Ingreso si se piden 20 | 160 | 160 |
| Ingreso si se piden 80 | 160 | 520 |
| Ingreso esperado | 160 | 232 |
| Costo de producción | 40 | 130 |
| Ganancia esperada | 120 | 102 |

Producir 65 deja un ingreso esperado mayor, pero el aumento del costo supera
al del ingreso. **Más ingreso no significa necesariamente más ganancia.**

Minimizar solo el costo tampoco expresa la prioridad de la responsable.
Producir cero cuesta cero y deja ganancia cero; producir 20 cuesta 40 pesos
y deja una ganancia de 120 pesos en cualquiera de los dos escenarios.
Ahorrar todo el costo también elimina esas ventas.

Maximizar ingresos y maximizar ganancia son equivalentes si el costo total
es el mismo en todas las decisiones comparadas. De manera análoga,
minimizar costos equivale a maximizar ganancia si el ingreso es el mismo.
Esas condiciones no se cumplen en el conjunto de producciones de este problema.

**5. Entender el límite del promedio.** Para la producción de 65 piezas,
las ganancias posibles son 30 y 390 pesos. Su promedio de 102 pesos no es
una ganancia garantizada ni una predicción exacta de mañana.

Una ganancia esperada alta puede combinar resultados frecuentes modestos
con otros poco frecuentes y muy favorables. Si la responsable necesita
asegurar un mínimo en cada escenario, debe expresar esa prioridad en el
modelo: el promedio por sí solo no la incorpora.
:::

## Problema 4 · Producir sin saber qué demanda es más probable

::: exercise {#opt-obj-pan-ej-escenarios title="Los mismos escenarios, dos maneras de protegerse"}
La panadería sigue decidiendo esta noche cuánto producir. Se conservan
las condiciones del problema anterior:

- Producción entera entre 0 y 100 piezas, elegida antes de conocer la demanda.
- Demandas posibles de 20 y 80 piezas.
- Precio de venta de 8 pesos y costo de producción de 2 pesos por pieza.
- Venta de cuanto permitan producción y demanda, sin recuperación por los
  sobrantes ni otros costos o ingresos.

**Ahora no hay probabilidades justificadas.** Los valores 0.8 y 0.2 ya no
son datos disponibles para comparar las decisiones.

En la panadería se discuten dos prioridades:

- La responsable quiere que **la menor ganancia entre los escenarios sea
  lo más alta posible**.
- Su socio compara la ganancia de cada producción con lo que habría ganado
  **si hubiera conocido la demanda a tiempo**. Le preocupa la diferencia
  entre ambas cantidades. Quiere que esa diferencia sea lo más pequeña
  posible incluso en el escenario donde resulte mayor.

Construye ese referente y formula un modelo para cada propuesta, usando
la misma decisión y las mismas condiciones de producción. Explica qué
protege cada uno y comprueba si ordenan de la misma manera las producciones
de 20 y 65 piezas.

No necesitas encontrar una producción óptima. La pregunta es **qué criterio
responde a cada prioridad**, y por qué desconocer las probabilidades no
obliga a adoptar una única manera de decidir.
:::

### Primero intenta plantearlo

Usa tu expresión de ganancia del problema anterior. Si te cuesta distinguir
las propuestas, abre la primera pista.

::: hint {#opt-obj-pan-pista-escenarios-datos of="opt-obj-pan-ej-escenarios" title="Pista 1 · Dos preguntas sobre el mismo resultado"}
Fija una producción y piensa en cada demanda posible. La responsable
pregunta cuánto ganaría; el socio pregunta cuánto mejor le habría ido de
haber conocido la demanda a tiempo. ¿Qué cantidad debes construir para
responder esta segunda pregunta?
:::

Si ya distinguiste las cantidades, intenta escribir cómo las compara cada
persona antes de abrir la siguiente ayuda.

::: hint {#opt-obj-pan-pista-escenarios-guia of="opt-obj-pan-ej-escenarios" title="Pista 2 · Qué resultado preocupa en cada propuesta"}
Para una producción, anota las ganancias en los dos escenarios. Haz lo
mismo con las diferencias respecto del referente. ¿Cuál de los dos valores
de cada lista necesita vigilar la persona que propuso ese criterio?
:::

Antes de leer la respuesta, revisa si tus dos modelos expresan prioridades
distintas o si cambiaste de nombre a una misma cantidad.

::: answer {#opt-obj-pan-resp-escenarios of="opt-obj-pan-ej-escenarios" title="Respuesta · Dos prioridades para comparar ganancias"}
**1. Conservar las consecuencias y retirar las probabilidades.** La ganancia
sigue siendo

$$\Pi(q,d_s)=v\min(q,d_s)-cq.$$

Se conserva una sola decisión previa $q$, junto con $Q,d_s,v,c$. Retiramos
$p_s$: asignar probabilidades iguales sería un supuesto adicional, no una
consecuencia de desconocerlas.

**2. Proteger la ganancia mínima.** Para una producción fija, la responsable
observa sus ganancias en todos los escenarios y se queda con la menor.
Luego compara producciones buscando que ese mínimo sea lo más alto posible:

$$
\begin{aligned}
\max\quad &\min_{s\in S}\Pi(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Con los datos de la panadería, el modelo queda

$$
\begin{aligned}
\max\quad &\min\left\{
8\min(q,20)-2q,\;
8\min(q,80)-2q\right\}\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

Este criterio valora el nivel de ganancia que la producción asegura entre
los escenarios considerados. No afirma que ocurrirá el menos favorable.

**3. Calcular lo que habríamos ganado conociendo la demanda.** Como el precio es mayor que el
costo, cada pieza que se puede vender aporta $v-c$ pesos de ganancia. Si
conociéramos la demanda antes de producir, prepararíamos solo las piezas
que pudiéramos vender, hasta donde alcance la capacidad.

La ganancia de ese referente es

$$B_s=(v-c)\min(d_s,Q).$$

Para calcular el referente imaginamos conocer la demanda antes de producir.
Esa información no está disponible hoy, cuando elegimos nuestra producción.
Usamos el referente únicamente para evaluar cuánto se deja de ganar por
haber decidido sin esa información.

Llamaremos **oportunidad perdida** a la diferencia entre ese referente y
la ganancia de la producción elegida:

$$R(q,d_s)=B_s-\Pi(q,d_s).$$

Se mide en pesos y es no negativa. No es necesariamente dinero que sale
de la caja: podemos tener una ganancia positiva y, aun así, haber ganado
menos que el referente.

En esta instancia, la capacidad alcanza para ambas demandas, por lo que
$B_s=6d_s$. Podemos entender la diferencia observando dos casos:

- Si sobra pan, cada pieza sobrante costó 2 pesos y no produjo ingreso.
- Si falta pan, cada venta que no se pudo atender habría aportado
  $8-2=6$ pesos netos. Esa ganancia se dejó de obtener; no fue un pago.

Así, **cuando $Q\ge d_s$**, la misma diferencia se escribe como

$$
R(q,d_s)
=c\max(q-d_s,0)+(v-c)\max(d_s-q,0).
$$

Los máximos con cero cuentan piezas sobrantes y faltantes sin permitir
cantidades negativas. Ambas cantidades no pueden ser positivas a la vez.
Con los precios del ejercicio obtenemos

$$
R(q,d_s)=6d_s-\Pi(q,d_s)
=2\max(q-d_s,0)+6\max(d_s-q,0).
$$

Los coeficientes 2 y 6 surgieron de comparar ganancias: no eran dos costos
de desembolso dados por el relato.

**4. Protegerse frente a la mayor oportunidad perdida.** El socio calcula
$R$ en todos los escenarios y toma su mayor valor. Prefiere la producción
que haga ese valor lo más pequeño posible:

$$
\begin{aligned}
\min\quad &\max_{s\in S}\bigl[B_s-\Pi(q,d_s)\bigr]\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Al sustituir los datos, usando la expresión que acabamos de construir,

$$
\begin{aligned}
\min\quad &\max\left\{
2\max(q-20,0)+6\max(20-q,0),\right.\\
&\hspace{3em}\left.2\max(q-80,0)+6\max(80-q,0)\right\}\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

**5. Comprobar la diferencia entre prioridades.** El referente es de
120 pesos si se piden 20 piezas y de 480 pesos si se piden 80. Comparemos
las dos producciones solicitadas:

Las columnas comparan producir 20 y 65 piezas; los resultados están en pesos.

| Resultado | 20 | 65 |
|---|---:|---:|
| Ganancia si se piden 20 | 120 | 30 |
| Ganancia si se piden 80 | 120 | 390 |
| Ganancia mínima | 120 | 30 |
| Oportunidad perdida si se piden 20 | 0 | 90 |
| Oportunidad perdida si se piden 80 | 360 | 90 |
| Oportunidad perdida máxima | 360 | 90 |

Entre estas alternativas, la responsable prefiere 20: garantiza una ganancia
mayor. El socio prefiere 65: se aleja menos del referente en su peor caso,
aunque acepta ganar menos si la demanda resulta baja.

**Los dos criterios no son equivalentes.** Responden a prioridades distintas.
El referente cambia de un escenario a otro; restarlo puede cambiar cuál
es el escenario más desfavorable para una producción.

Con las probabilidades del problema 3 sí hay una equivalencia entre
**maximizar la ganancia esperada y minimizar la oportunidad perdida
esperada**. En efecto,

$$
\sum_s p_sR(q,d_s)=\sum_s p_sB_s-\sum_s p_s\Pi(q,d_s).
$$

El primer término no depende de la producción. Con aquellas probabilidades
vale $0.8(120)+0.2(480)=192$ pesos: cada peso adicional de ganancia esperada
reduce en un peso la oportunidad perdida esperada. Para 20 y 65 piezas,
estas últimas serían 72 y 90 pesos, respectivamente.

Esta comparación recupera probabilidades solo para explicar la equivalencia.
**En el problema 4 no podemos atribuir esos promedios a las decisiones:**
las probabilidades fueron retiradas. Tampoco podemos trasladar la equivalencia
del promedio a los criterios de peor caso, como muestra la tabla.

Ambas propuestas protegen frente a los escenarios incluidos, con criterios
distintos. Ninguna protege automáticamente frente a demandas omitidas ni
considera cuán frecuente es cada escenario. Ampliar los escenarios o reunir
información que justifique probabilidades puede cambiar la comparación.
:::

Después de tus intentos, consulta [[opt-objetivo-panaderia-modelo|el modelo general de producción incierta]].
