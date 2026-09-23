---
id: opt-practica-riesgo
title: Comparar ganancias y oportunidades perdidas
nav_title: "Panadería: práctica"
summary: "Comparar dos maneras de protegerse ante demandas sin probabilidades justificadas."
status: ready
estimated_time: 40m
tags: [optimizacion, modelado, practica]
---

# Comparar ganancias y oportunidades perdidas

Una misma producción puede verse bien por la ganancia que asegura y mal por
lo que deja de ganar respecto de otra que hubiera aprovechado la demanda.
En este problema construirás los dos criterios. Los datos son didácticos.

Si necesitas ayuda para pasar de ventas y costos a ganancia, vuelve a [[opt-objetivo-panaderia-practica|el ejemplo guiado de panadería]].

## Problema 12 · Producir sin saber qué demanda es más probable

::: exercise {#opt-obj-pan-ej-escenarios title="Dos maneras de protegerse ante la demanda"}
Esta noche, una panadería decide cuántas piezas producirá mañana. Una vez
elegida la cantidad, no puede ajustarla al conocer la demanda. Estos son
los datos y las condiciones:

- Producción entera entre 0 y 100 piezas, elegida antes de conocer la demanda.
- Demandas posibles de 20 y 80 piezas.
- Precio de venta de 8 pesos y costo de producción de 2 pesos por pieza.
- Venta de cuanto permitan producción y demanda, sin recuperación por los
  sobrantes ni otros costos o ingresos.

**No hay probabilidades justificadas** para las dos demandas posibles.
Conocer esos escenarios no permite suponer que sean igual de probables.

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

Empieza por escribir cuántas piezas venderías y cuánto pagarías por producir.
Construye tu expresión de ganancia antes de comparar las dos propuestas.
Si te cuesta distinguirlas, abre la primera pista.

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
**1. Definir datos, decisión y ganancia.** Llamamos $S$ al conjunto finito
no vacío de escenarios. Usamos los siguientes datos:

- $Q\in\mathbb Z_{\ge0}$: capacidad de producción, en piezas.
- $d_s\in\mathbb Z_{\ge0}$: demanda del escenario $s$, en piezas.
- $v$: precio de venta, en pesos por pieza.
- $c$: costo de producción, en pesos por pieza; suponemos $v>c>0$.

Elegimos una sola producción previa $q\in\mathbb Z$, con $0\le q\le Q$.
En el ejercicio, $Q=100$, las demandas son 20 y 80, $v=8$ y $c=2$.

Se vende la menor cantidad entre lo producido y lo pedido, $\min(q,d_s)$.
El ingreso es $v\min(q,d_s)$, mientras que producir cuesta $cq$, se venda
o no todo el pan. La ganancia, en pesos, es

$$\Pi(q,d_s)=v\min(q,d_s)-cq.$$

No hay datos $p_s$ de probabilidad. Asignar probabilidades iguales sería un
supuesto adicional, no una consecuencia de desconocerlas.

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

Si en otra situación se justificaran probabilidades 0.8 para demanda 20 y
0.2 para demanda 80, como en el ejemplo guiado de panadería, habría una equivalencia entre
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
**En el problema 12 no podemos atribuir esos promedios a las decisiones:**
no tenemos probabilidades justificadas. Tampoco podemos trasladar la equivalencia
del promedio a los criterios de peor caso, como muestra la tabla.

Ambas propuestas protegen frente a los escenarios incluidos, con criterios
distintos. Ninguna protege automáticamente frente a demandas omitidas ni
considera cuán frecuente es cada escenario. Ampliar los escenarios o reunir
información que justifique probabilidades puede cambiar la comparación.
:::

Después de tus intentos, puedes consultar [[opt-objetivo-panaderia-modelo|el modelo general de producción incierta]].

[[opt-construir-objetivo|Volver al banco de práctica]].
