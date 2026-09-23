---
id: opt-objetivo-panaderia-modelo
title: "El modelo general de una decisión incierta"
nav_title: "Panadería: modelo general"
summary: "Separar decisión, escenarios y consecuencias antes de elegir entre pérdida esperada y peor pérdida."
status: ready
tags: [optimizacion, modelado, practica]
---

# El modelo general de una decisión incierta

**Primero intenta los [[opt-objetivo-panaderia-practica|dos problemas de panadería]].**
La pregunta común es: **¿cuánto producir cuando hay que decidir antes de
conocer la demanda?** El cálculo de las consecuencias y el criterio para
compararlas son dos partes distintas del modelo.

## 1 · Ordenar los momentos de la decisión

Primero se elige la producción; después se observa la demanda; finalmente
se cuentan las piezas sobrantes y las que no se pudieron atender.
Evaluar varios escenarios no permite elegir una producción distinta en cada
uno. Eso correspondería a otro problema, con otra información disponible.

| Dato | Significado |
|---|---|
| $S$ | Conjunto finito no vacío de escenarios considerados |
| $d_s\in\mathbb Z_{\ge0}$ | Demanda del escenario $s$, en piezas |
| $Q\in\mathbb Z_{\ge0}$ | Capacidad de producción, en piezas |
| $c_o,c_f>0$ | Pérdidas por sobrante y faltante, en pesos/pieza |
| $p_s$, cuando se conoce | Probabilidad del escenario, no negativa; las probabilidades suman uno |

La variable $q\in\mathbb Z_{\ge0}$ cuenta piezas producidas y cumple $q\le Q$.
Ni la demanda ni sus probabilidades son decisiones de la panadería.

## 2 · Evaluar cualquier producción

Si $q>d_s$, sobran $q-d_s$ piezas; si $q<d_s$, faltan $d_s-q$.
Cuando son iguales, ambas consecuencias valen cero. Una sola expresión
recoge los tres casos:

$$L(q,d_s)=c_o\max(q-d_s,0)+c_f\max(d_s-q,0).$$

La expresión mide pesos perdidos bajo el convenio de costos del relato.
No representa automáticamente utilidad, ingresos ni desperdicio ambiental.
Agregar esos propósitos requeriría datos y criterios adicionales.

La pérdida depende de una decisión y de un escenario. Para convertirla en
objetivo todavía debemos decir **cómo comparar la lista de pérdidas** de
cada decisión.

## 3 · Comparar promedios con probabilidades

Si las probabilidades son datos justificados y se acepta el promedio
monetario como criterio, el modelo completo es

$$
\begin{aligned}
\min\quad &\sum_{s\in S}p_sL(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Una pérdida esperada pequeña puede combinar pérdidas pequeñas frecuentes
con una pérdida grande poco frecuente. El objetivo no controla por separado
la peor consecuencia. Su valor tampoco es una predicción exacta de la
pérdida del siguiente día.

Las probabilidades hacen calculable el promedio; **preferir ese promedio**
es el criterio elegido por quien decide. Conocer probabilidades no obliga a
ser indiferente ante la dispersión o ante una pérdida difícil de soportar.

## 4 · Protegerse ante la mayor pérdida

Si se adopta la protección frente al peor escenario incluido, usamos

$$
\begin{aligned}
\min\quad &\max_{s\in S}L(q,d_s)\\
\text{sujeto a}\quad &0\le q\le Q,\\
&q\in\mathbb Z.
\end{aligned}
$$

Podemos expresar la misma preferencia con una variable auxiliar $z$, en pesos,
que debe alcanzar todas las pérdidas:

$$
\begin{aligned}
\min\quad &z\\
\text{sujeto a}\quad &z\ge L(q,d_s) &&\text{para cada }s\in S,\\
&0\le q\le Q,\\
&q\in\mathbb Z,\quad z\in\mathbb R_{\ge0}.
\end{aligned}
$$

Para cada producción, el menor $z$ permitido es su mayor pérdida. Por eso
minimizarlo recupera el criterio anterior. $z$ no cambia las consecuencias
físicas; sirve para expresar su comparación.

No se supone que la demanda sea un rival que elige perjudicarnos. Se adopta
una regla para valorar incertidumbre. Y “sin probabilidades” no significa
“todos los escenarios tienen la misma probabilidad”.

## 5 · Revisar el criterio ante un caso límite

Con los datos de la práctica, las producciones 20 y 65 tienen pérdidas
$(0,360)$ y $(90,90)$ pesos. El promedio con probabilidades $(0.8,0.2)$
prefiere 20 entre esas alternativas; la peor pérdida prefiere 65.
No es una contradicción: expresan preferencias diferentes.

Una condición como **“ningún escenario incluido puede perder más de $B$
pesos”**, con $B\ge0$ fijado por la responsable, se escribe
$L(q,d_s)\le B$ para cada $s$. Es una obligación y puede hacer inviable el
problema. Para elegir entre las producciones que la cumplen todavía puede
hacer falta un objetivo, como el promedio si se tienen probabilidades.

Antes de aceptar el modelo, revisa también el conjunto $S$. Una protección
calculada solo para demandas 20 y 80 no es una garantía frente a cualquier
demanda imaginable. Ampliar escenarios puede cambiar las decisiones y las
garantías que realmente se pueden afirmar.

## Qué razonamiento puedes reutilizar

**Separa qué decides, qué puede ocurrir y cómo valoras las consecuencias.**
Primero formula la pérdida de cualquier decisión en cada escenario. Después
justifica cómo conviertes esas pérdidas en un criterio único. No rellenes
la información que falta como si fuera un dato del problema.

[[opt-objetivo-panaderia-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
