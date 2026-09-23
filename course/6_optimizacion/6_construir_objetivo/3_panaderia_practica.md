---
id: opt-objetivo-panaderia-practica
title: "Producir antes de conocer la demanda"
nav_title: "Panadería: práctica"
summary: "Formular una decisión antes de conocer la demanda y justificar cómo comparar sus posibles pérdidas."
status: ready
tags: [optimizacion, modelado, practica]
---

# Producir antes de conocer la demanda

**Tu tarea:** construir dos modelos para decidir cuánto producir antes de
saber cuánto se venderá. Los números y escenarios son didácticos. No necesitas
encontrar la producción óptima; sí explicar qué significa que una sea mejor.
Intenta cada ejercicio antes de abrir sus ayudas.

## Problema 3 · Con probabilidades conocidas

::: exercise {#opt-obj-pan-ej-probabilidades title="La producción de mañana"}
Una panadería decide esta noche cuántas piezas producirá mañana. Puede
producir entre **0 y 100 piezas enteras**. Una vez tomada la decisión, no puede
ajustarla al observar la demanda.

Para este ejercicio solo hay dos demandas posibles: **20 piezas**, con
probabilidad **0.8**, y **80 piezas**, con probabilidad **0.2**. Se supone que
esas probabilidades describen adecuadamente la incertidumbre de mañana.

Cada pieza sobrante ocasiona una pérdida de **2 pesos** y cada pieza que un
cliente pide pero no puede recibir ocasiona una pérdida de **6 pesos**.
Estos valores resumen las consecuencias que interesa comparar: no agregues
ingresos ni otros costos. Se atiende toda la demanda que permita la producción.

La panadería acepta comparar las decisiones por su **pérdida monetaria
promedio según estas probabilidades**. Define datos, decisiones, pérdida en
cada escenario, objetivo, restricciones y dominios. Explica qué protección
ofrece ese criterio y qué deja fuera.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-obj-pan-pista-probabilidades-datos of="opt-obj-pan-ej-probabilidades" title="PISTA 1 · Solo si te atoraste"}
| Información conocida | Valor |
|---|---|
| Capacidad | 100 piezas |
| Demandas y probabilidades | 20 con 0.8; 80 con 0.2 |
| Pérdida por sobrante | 2 pesos/pieza |
| Pérdida por pieza no atendida | 6 pesos/pieza |

La producción se elige esta noche. La demanda se conoce después. Los sobrantes
y faltantes se obtienen al comparar esas dos cantidades.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-pan-pista-probabilidades-guia of="opt-obj-pan-ej-probabilidades" title="PISTA 2 · Solo si te atoraste"}
Si produces más de lo que se pide, ¿cuántas piezas faltan? ¿Cómo escribirías
una cantidad que vale cero cuando no hay faltantes?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-pan-resp-probabilidades of="opt-obj-pan-ej-probabilidades" title="Respuesta · Decidir antes, evaluar después"}
**1. Separar la decisión del escenario.** Elegimos una producción común a
ambas demandas. Escribir una producción distinta para cada demanda permitiría
usar información que todavía no se tiene.

**2. Definir parámetros y decisión.** Sea $S$ el conjunto finito de escenarios.

| Parámetro | Significado y unidad |
|---|---|
| $Q$ | Capacidad, en piezas; entero no negativo |
| $d_s$ | Demanda del escenario $s$, en piezas |
| $p_s$ | Probabilidad del escenario $s$; $p_s\ge0$ y $\sum_{s\in S}p_s=1$ |
| $c_o,c_f>0$ | Pérdida por pieza sobrante y por pieza faltante, en pesos/pieza |

Elegimos $q\in\mathbb Z_{\ge0}$, **piezas producidas antes de observar la demanda**.

**3. Construir las consecuencias.** En el escenario $s$ sobran
$\max(q-d_s,0)$ piezas y faltan $\max(d_s-q,0)$. El máximo con cero impide
contar un sobrante o faltante negativo. No pueden ser ambos positivos.
La pérdida de ese escenario es

$$L(q,d_s)=c_o\max(q-d_s,0)+c_f\max(d_s-q,0).$$

Multiplicar pesos/pieza por piezas da pesos. Las probabilidades no tienen
unidades; ponderar estas pérdidas conserva la unidad monetaria.

**4. Reunir el modelo general.**

$$
\begin{aligned}
\min\quad &\sum_{s\in S}p_s\bigl[c_o\max(q-d_s,0)+c_f\max(d_s-q,0)\bigr]\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

El objetivo es la **pérdida esperada**, medida en pesos. Es defendible si
aceptamos las probabilidades y preferimos el menor promedio monetario. No
impone un límite a la pérdida de cada día.

**5. Sustituir los datos.**

$$
\begin{aligned}
\min\quad
&0.8\bigl[2\max(q-20,0)+6\max(20-q,0)\bigr]\\
&\quad+0.2\bigl[2\max(q-80,0)+6\max(80-q,0)\bigr]\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

**Comprobación y límite.** Comparamos dos producciones permitidas, sin
afirmar que esa comparación resuelve todo el problema:

| Producción | Pérdida si se piden 20 | Pérdida si se piden 80 | Pérdida esperada |
|---|---:|---:|---:|
| 20 piezas | 0 pesos | 360 pesos | 72 pesos |
| 80 piezas | 120 pesos | 0 pesos | 96 pesos |

El promedio prefiere la primera a la segunda, aunque expone a una pérdida
mayor si ocurre la demanda alta. **72 pesos no es la pérdida garantizada de
mañana.** Si fuera indispensable limitar cualquier pérdida, tendríamos que
añadir esa obligación al modelo o cambiar el criterio de comparación.
:::

## Problema 4 · Sin probabilidades justificadas

::: exercise {#opt-obj-pan-ej-escenarios title="Los mismos escenarios, otra información"}
Conserva la decisión previa de producción, las piezas enteras, la capacidad
de 100, las demandas posibles de 20 y 80, y las pérdidas de 2 pesos por
sobrante y 6 por faltante. **Ahora no hay probabilidades justificadas** para
los escenarios: los valores 0.8 y 0.2 del problema anterior ya no son datos.

La panadería quiere decidir cómo protegerse ante esa incertidumbre. Considera
esta propuesta de su responsable: **elegir la producción cuya mayor pérdida
entre los escenarios sea lo más pequeña posible**.

Formula el modelo completo correspondiente a esa propuesta. Explica qué
preferencia expresa, qué información utiliza y por qué desconocer las
probabilidades no obliga a adoptar esa única función objetivo.
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SIN INTENTARLO. ÚSALA SOLO SI TE ATORASTE.**

::: hint {#opt-obj-pan-pista-escenarios-datos of="opt-obj-pan-ej-escenarios" title="PISTA 1 · Solo si te atoraste"}
Se conserva cómo calcular sobrantes, faltantes y pérdidas. Cambia la
información disponible para comparar escenarios: conocemos cuáles se
consideran posibles, pero no sus probabilidades.
:::

**NO ABRAS LA PISTA 2 SIN INTENTARLO. ÚSALA SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-pan-pista-escenarios-guia of="opt-obj-pan-ej-escenarios" title="PISTA 2 · Solo si te atoraste"}
Si anotas la pérdida de una producción en cada escenario, ¿qué número de esa
lista representa la protección que pide la responsable?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-pan-resp-escenarios of="opt-obj-pan-ej-escenarios" title="Respuesta · Elegir cómo tratar lo desconocido"}
**1. Identificar lo que cambia.** Conservamos $Q,d_s,c_o,c_f$ y la única
decisión previa $q$. Quitamos $p_s$: asignar probabilidades iguales también
sería un supuesto adicional, no una consecuencia de desconocerlas.

**2. Construir el criterio.** Para una producción fija, calculamos
$L(q,d_s)$ en todos los escenarios. Su mayor valor es
$\max_{s\in S}L(q,d_s)$. La propuesta pide minimizar ese valor, en pesos.

**3. Reunir el modelo general.**

$$
\begin{aligned}
\min\quad &\max_{s\in S}\bigl[c_o\max(q-d_s,0)+c_f\max(d_s-q,0)\bigr]\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Este criterio **robusto** protege frente a la mayor pérdida entre los
escenarios incluidos. No necesita probabilidades y no afirma que el escenario
peor vaya a ocurrir. Expresa una preferencia por limitar esa exposición.

**4. Sustituir los datos.**

$$
\begin{aligned}
\min\quad &\max\left\{
2\max(q-20,0)+6\max(20-q,0),\right.\\
&\hspace{3em}\left.2\max(q-80,0)+6\max(80-q,0)\right\}\\
\text{sujeto a}\quad &0\le q\le100,\\
&q\in\mathbb Z.
\end{aligned}
$$

**5. Comprobar qué distingue esta preferencia.** Producir 65 piezas pierde
90 pesos en cualquiera de los dos escenarios: $2(65-20)=90$ y
$6(80-65)=90$. Producir 20 pierde como máximo 360 pesos. El criterio robusto
prefiere 65 a 20 entre esas dos alternativas.

Si recuperáramos las probabilidades del problema 3, sus pérdidas
esperadas serían 90 y 72 pesos, respectivamente: las dos preferencias
ordenan esas alternativas de manera distinta. **En esta variante no podemos
atribuirles esos promedios**, porque retiramos las probabilidades.

El criterio deja fuera cuán frecuente es cada escenario y no protege contra
demandas que omitimos. Una revisión posible es ampliar los escenarios; otra,
recopilar información para justificar probabilidades y volver a comparar
promedios. Elegir la mayor pérdida es una decisión sobre cómo valorar la
incertidumbre, no una verdad deducida de la falta de información.
:::

Después de tus intentos, consulta [[opt-objetivo-panaderia-modelo|el modelo general de producción incierta]].
