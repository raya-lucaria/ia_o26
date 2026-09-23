---
id: opt-objetivo-panaderia-modelo
title: "Calcular la ganancia y decidir qué proteger"
nav_title: "Panadería: modelo general"
summary: "Construir ingresos, costos y ganancias para distinguir el promedio, la ganancia mínima y la oportunidad perdida."
status: ready
tags: [optimizacion, modelado, practica]
---

# Calcular la ganancia y decidir qué proteger

Esta es una **consulta opcional** que amplía el [[opt-objetivo-panaderia-practica|ejemplo guiado de panadería]] y el [[opt-practica-riesgo|problema 12 de ganancias y oportunidades perdidas]].
La pregunta común es **cuánto pan producir antes de conocer la demanda**.
Para responderla, necesitamos calcular qué pasaría con cada producción y
explicar qué resultado queremos favorecer.

Vender más, gastar menos y ganar más no siempre llevan a la misma decisión.
Incluso si elegimos comparar ganancias, una producción puede ganar poco
en ambos escenarios y otra, mucho en uno y poco en el otro. ¿Cuál de esas
situaciones preferimos?

## 1 · Producir hoy para vender mañana

Primero se elige la producción; después se conoce la demanda y se vende
cuanto sea posible. **La decisión se toma una sola vez**, antes de saber
qué demanda ocurrirá. Evaluar varias demandas no permite cambiar la
producción para cada una.

Llamamos *escenario* a cada caso de demanda que incluimos en la comparación.
Los siguientes datos describen el problema general:

- $S$: Conjunto finito no vacío de escenarios.
- $d_s\in\mathbb Z_{\ge0}$: Demanda del escenario $s$, en piezas.
- $Q\in\mathbb Z_{\ge0}$: Capacidad de producción, en piezas.
- $v$: Precio de venta, en pesos/pieza.
- $c$: Costo de producción, en pesos/pieza.

Suponemos $v>c>0$, que producir una pieza siempre ocasiona su costo y que
los sobrantes no tienen valor de recuperación. Se atiende toda la demanda
que permita la producción, sin otros costos ni ingresos.

Si conocemos probabilidades justificadas, también tenemos un dato $p_s$
para cada escenario, con

$$p_s\ge0,\qquad \sum_{s\in S}p_s=1.$$

La variable $q$ cuenta **piezas producidas**. Sus condiciones son

$$0\le q\le Q,\qquad q\in\mathbb Z.$$

Ni la demanda ni sus probabilidades son decisiones de la panadería.

## 2 · De las piezas vendidas al dinero ganado

Si la producción alcanza, se vende lo que se pide; si no alcanza, se vende
todo lo producido. El número de piezas vendidas es, por tanto,

$$\min(q,d_s).$$

El precio se cobra por las piezas vendidas. El costo se paga por las
producidas, aunque algunas sobren:

$$
I(q,d_s)=v\min(q,d_s),
\qquad C(q)=cq.
$$

Cada producto multiplica pesos por pieza por un número de piezas. Tanto
el ingreso $I$ como el costo $C$ se miden en pesos. Al restarlos obtenemos
la **ganancia**:

$$\Pi(q,d_s)=I(q,d_s)-C(q)=v\min(q,d_s)-cq.$$

La ganancia puede ser negativa si el ingreso no cubre la producción. Esta
expresión solo recoge el dinero descrito en el relato: incluir otros costos,
valor de recuperación o consecuencias ambientales requeriría nuevos datos.

La expresión ya permite evaluar una producción en cada escenario. Todavía
no dice cómo comparar producciones: cada una tiene una lista de ganancias,
una por escenario.

## 3 · Comparar cuánto esperamos ganar

Cuando las probabilidades están justificadas, podemos calcular la ganancia
promedio ponderando cada resultado por su probabilidad. Si aceptamos ese
promedio como criterio, el modelo es

$$
\begin{aligned}
\max\quad &\sum_{s\in S}p_s\Pi(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

El objetivo se llama **ganancia esperada** y se mide en pesos. No es una
predicción exacta de mañana ni una ganancia mínima asegurada: un promedio
favorable puede incluir algún resultado difícil de soportar.

Las probabilidades permiten calcular el promedio; **preferirlo es una
elección de quien decide**. Conocer probabilidades no obliga a ignorar
la diferencia entre resultados ni a aceptar cualquier ganancia baja.

### Cuándo sirve maximizar ingresos o minimizar costos

La ganancia es ingreso menos costo. Si todas las decisiones comparadas
cuestan lo mismo, maximizar el ingreso también maximiza la ganancia.
Si todas producen el mismo ingreso, minimizar el costo también maximiza
la ganancia.

En la panadería, ni los ingresos ni los costos son constantes entre todas
las producciones. Con las probabilidades del ejemplo guiado, producir 65 piezas
da más ingreso esperado que producir 20, pero deja menos ganancia esperada:

Las columnas comparan producir 20 y 65 piezas; los resultados están en pesos.

| Resultado | 20 | 65 |
|---|---:|---:|
| Ingreso esperado | 160 | 232 |
| Costo de producción | 40 | 130 |
| Ganancia esperada | 120 | 102 |

Minimizar solo el costo tampoco representa ganar más: producir cero ahorra
la producción, pero deja ganancia cero. Producir 20 cuesta 40 pesos y deja
una ganancia de 120 pesos en ambos escenarios.

Sí podemos cambiar siempre la maximización de la ganancia por la
minimización de su negativo:

$$-\Pi(q,d_s)=C(q)-I(q,d_s).$$

Ese **costo neto** descuenta los ingresos. Minimizarlo no es lo mismo que
minimizar únicamente el gasto de producción.

## 4 · Comparar con lo que habríamos ganado sabiendo la demanda

Imagina, solo como comparación, que hubiéramos conocido la demanda antes
de producir. Como $v>c$, convendría preparar las piezas que pudieran
venderse, hasta donde alcanzara la capacidad. Su ganancia sería

$$B_s=(v-c)\min(d_s,Q).$$

Este **referente** cambia con la demanda. No elimina la incertidumbre de
nuestra decisión real: sirve para medir cuánto se deja de ganar por haber
elegido sin conocerla.

Llamamos **oportunidad perdida** a esa diferencia:

$$R(q,d_s)=B_s-\Pi(q,d_s).$$

Se mide en pesos y es no negativa. Una oportunidad perdida no es
necesariamente un desembolso: se puede ganar dinero y, al mismo tiempo,
ganar menos que si se hubiera conocido la demanda.

Cuando la capacidad alcanza para la demanda del escenario, $Q\ge d_s$,
el referente se reduce a $(v-c)d_s$. La diferencia tiene entonces dos
explicaciones sencillas:

- Cada pieza sobrante costó $c$ pesos y no se vendió.
- Cada pieza faltante habría dejado $v-c$ pesos después de pagar su
  producción. Esa ganancia no se obtuvo.

El número de sobrantes es $\max(q-d_s,0)$ y el de faltantes es
$\max(d_s-q,0)$. Usamos el máximo con cero para no contar cantidades
negativas; solo una de ellas puede ser positiva. Por tanto, bajo esa
condición de capacidad,

$$
R(q,d_s)
=c\max(q-d_s,0)+(v-c)\max(d_s-q,0).
$$

En la práctica, $v=8$, $c=2$ y ambas demandas caben en la capacidad. Así
obtenemos los 2 pesos por sobrante y los 6 por faltante: **son contribuciones
a la oportunidad perdida**, construidas desde el precio y el costo.

### Una equivalencia cuando comparamos promedios

Con probabilidades justificadas,

$$
\sum_{s\in S}p_sR(q,d_s)
=\sum_{s\in S}p_sB_s-\sum_{s\in S}p_s\Pi(q,d_s).
$$

El promedio de los referentes no cambia al elegir otra producción.
Por eso **maximizar la ganancia esperada equivale a minimizar la oportunidad
perdida esperada**: las dos comparaciones ordenan igual las decisiones.

En el ejemplo guiado, ese promedio fijo es $0.8(120)+0.2(480)=192$ pesos.
Para una producción de 20 piezas, la ganancia esperada de 120 deja una
oportunidad perdida esperada de 72; para 65 piezas, las cantidades son
102 y 90 pesos. Los dos criterios prefieren 20 entre esas alternativas.

## 5 · Elegir qué proteger en el peor caso

Sin probabilidades justificadas, no podemos calcular aquellos promedios.
Eso no determina una única preferencia. Podemos querer asegurar una
ganancia mínima. También podemos compararnos con lo que habríamos ganado
conociendo la demanda y buscar que la diferencia sea pequeña.

**Proteger la ganancia mínima** significa tomar la menor ganancia de cada
producción y buscar que sea lo más alta posible:

$$
\begin{aligned}
\max\quad &\min_{s\in S}\Pi(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

**Protegerse frente a la mayor oportunidad perdida** significa calcular la
diferencia frente a cada referente y buscar que la mayor sea lo más pequeña
posible:

$$
\begin{aligned}
\min\quad &\max_{s\in S}R(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Ambos criterios consideran el peor resultado según su propia medida.
Se llaman criterios *robustos* porque buscan protección frente a todos
los escenarios incluidos. No suponen que el escenario peor vaya a ocurrir
ni que la demanda sea un rival que elige perjudicarnos.

### Por qué ya no son equivalentes

El referente es de 120 pesos para la demanda baja y de 480 para la alta.
Esa diferencia importa al buscar el peor resultado:

Las columnas comparan producir 20 y 65 piezas; los resultados están en pesos.

| Resultado | 20 | 65 |
|---|---:|---:|
| Ganancia si se piden 20 | 120 | 30 |
| Ganancia si se piden 80 | 120 | 390 |
| Ganancia mínima | 120 | 30 |
| Oportunidad perdida máxima | 360 | 90 |

La ganancia mínima favorece 20; la oportunidad perdida máxima favorece 65.
Estas comparaciones no resuelven los modelos completos, pero sí muestran
que expresan prioridades distintas.

En el promedio podíamos separar una misma cantidad fija respecto de la
producción. En el peor caso no podemos sacar los distintos $B_s$ como si
fueran una constante común: al pasar de ganancias a oportunidades perdidas
puede cambiar el escenario que determina el peor resultado.

### Otra forma de escribir la mayor oportunidad perdida

Podemos introducir una cantidad $z$, en pesos, que sea al menos tan grande
como la oportunidad perdida de cualquier escenario. Si buscamos el menor
$z$ posible, expresamos la misma preferencia:

$$
\begin{aligned}
\min\quad &z\\
\text{sujeto a}\quad &z\ge R(q,d_s) &&\text{para cada }s\in S,\\
&0\le q\le Q,\\
&q\in\mathbb Z,\quad z\in\mathbb R_{\ge0}.
\end{aligned}
$$

Para una producción fija, el menor $z$ permitido es exactamente su mayor
oportunidad perdida. La variable auxiliar no cambia las ventas ni los
costos; solo permite escribir cómo comparamos los resultados.

## 6 · Revisar qué protección ofrece el modelo

Elegir un criterio de peor caso expresa una preferencia. No conocer las
probabilidades no obliga a elegir uno de estos dos criterios, ni permite
suponer que todos los escenarios tienen la misma probabilidad.

También puede haber una obligación independiente del objetivo. Por ejemplo,
si la responsable fija un límite $H\ge0$ a la oportunidad perdida en
cualquier escenario, escribimos

$$R(q,d_s)\le H\qquad\text{para cada }s\in S.$$

Ese límite puede hacer inviable el problema. Entre las producciones que
lo cumplen todavía puede hacer falta un objetivo para elegir, como la
ganancia esperada si se cuenta con probabilidades justificadas.

Por último, revisa qué demandas incluimos en $S$. Una protección calculada
solo para 20 y 80 piezas no garantiza nada frente a cualquier demanda
imaginable. Ampliar los escenarios puede cambiar las decisiones y las
garantías que podemos afirmar.

## Qué razonamiento puedes reutilizar

**Construye primero las consecuencias y después decide cómo compararlas.**
En la panadería, eso significa distinguir lo producido, lo vendido y lo
ganado antes de escribir una función objetivo.

Para cambiar de maximizar a minimizar, identifica qué estás restando o
cambiando de signo. Después comprueba que la transformación conserva la
preferencia, incluida la forma de tratar la incertidumbre. Una equivalencia
entre promedios no se traslada automáticamente al peor caso.

[[opt-objetivo-panaderia-practica|Volver al ejemplo guiado]] · [[opt-practica-riesgo|Practicar la comparación de riesgos]] · [[opt-construir-objetivo|Volver al banco de práctica]].
