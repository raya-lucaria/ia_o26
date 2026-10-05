---
id: tarea-sin-turnos
title: "Tarea de refuerzo · Mezclar y reconocer"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: modelar el saque en tenis como juego simultáneo y resolverlo como programa lineal, y diagnosticar el juego de la gallina, que no es de suma cero."
status: ready
estimated_time: 50m
tags: [juegos, estrategias-mixtas, equilibrio-de-nash, practica]
---

# Tarea de refuerzo · Mezclar y reconocer

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin
ayuda** lo de la clase: escribir un juego simultáneo, resolver su mejor
mezcla y reconocer cuándo el maximin ya no es la herramienta.

El primer ejercicio es un juego nuevo de suma cero, que hay que modelar
desde la descripción. El segundo es un complemento: un juego que no es de
suma cero.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

## 1 · Modelar el saque en tenis

Una entrenadora de tenis revisó cientos de puntos de una jugadora que saca y
de la rival que le resta. Te deja estas notas:

> **[1]** Quien saca elige, en cada punto, sacar **Abierto**, hacia la orilla
> de la cancha, o **Al centro**.
>
> **[2]** Quien resta se cubre **Abierto** o **Centro**. El saque va tan
> rápido que tiene que moverse antes de ver hacia dónde va la pelota.
>
> **[3]** Si saca abierto y la otra se cubre abierto, quien saca gana 60 de
> cada 100 puntos. Si saca abierto y la otra se cubre al centro, gana 80.
>
> **[4]** Si saca al centro y la otra se cubre abierto, quien saca gana 70 de
> cada 100. Si saca al centro y la otra también se cubre al centro, solo
> gana 40.
>
> **[5]** Quien saca bota la pelota tres veces antes de cada saque.
>
> **[6]** Cada punto lo gana una de las dos: nunca hay empate.

::: exercise {#jue-tarea-4-ej-saque title="Modela y resuelve el saque"}
1. Separa datos y decisiones: ¿quién decide qué, y qué números están dados?
   ¿Qué nota sobra?
2. Diagnostica el juego: ¿por turnos o a la vez? ¿Es de suma cero?
3. Escribe la tabla de pagos con quien saca en las filas, en % de puntos que
   gana quien saca. Calcula el maximin puro y el minimax puro. ¿Hay punto de
   silla?
4. Escribe la mezcla de quien saca como $(p,1-p)$, con $p$ la probabilidad de
   sacar abierto, y escribe su programa lineal.
5. Dibuja las dos rectas para $p$ entre 0 y 1, marca la envolvente inferior y
   encuentra $p$ y $v$.
6. Escribe la mezcla de quien resta como $(q,1-q)$, con $q$ la probabilidad
   de cubrirse abierto. Encuentra su mejor $q$ y comprueba que el valor
   coincide con el $v$ del inciso 5.
:::

::: hint {#jue-tarea-4-pista-saque-a of="jue-tarea-4-ej-saque" title="Pista 1 · Datos, diagnóstico y tabla"}
¿Qué nota dice quién ve qué antes de decidir? Si quien saca gana 60 de cada
100 puntos, ¿cuántos gana quien resta? Para la tabla, cada número de las
notas 3 y 4 corresponde a una pareja (saque, cobertura): ¿en qué fila y en
qué columna va cada uno?
:::

::: hint {#jue-tarea-4-pista-saque-b of="jue-tarea-4-ej-saque" title="Pista 2 · Las rectas"}
Contra quien se cubre abierto, el pago esperado de quien saca es una recta
en $p$. ¿Cuánto vale en $p=0$ y en $p=1$? Haz lo mismo con la otra columna.
Para cada $p$, ¿cuál de las dos rectas manda, y en qué $p$ queda más alta
esa recta?
:::

::: answer {#jue-tarea-4-resp-saque of="jue-tarea-4-ej-saque" title="Respuesta · El saque en tenis"}
**1. Separar datos y decisiones.** Hay dos jugadoras. Quien saca decide hacia
dónde saca: Abierto o Al centro. Quien resta decide hacia dónde se cubre:
Abierto o Centro. Los datos son los cuatro porcentajes de las notas 3 y 4.
La nota 5 **sobra**: botar la pelota no cambia ningún pago. Las notas 2 y 6
no dan números, pero son esenciales para el diagnóstico.

Las decisiones del modelo son $p$, la probabilidad de sacar abierto, y $v$,
el porcentaje que quien saca asegura.

**2. Diagnosticar el juego.** Es **simultáneo**: por la nota 2, quien resta
elige antes de ver el saque, así que ninguna ve la decisión de la otra. Es
de **suma cero** en porcentaje: por la nota 6, cada punto lo gana una de las
dos, así que cada punto porcentual que gana quien saca lo pierde quien resta.
Basta con escribir los pagos de quien saca. Le toca una tabla de pagos y,
si no hay punto de silla, una mezcla.

**3. Escribir la tabla y buscar un punto de silla.**

| Saca ↓ · Se cubre → | Abierto | Centro |
|---|:---:|:---:|
| **Abierto** | 60 | 80 |
| **Al centro** | 70 | 40 |

Los peores casos de las filas son 60 y 40: el **maximin puro es 60**,
sacando siempre abierto. Los mayores de las columnas son 70 y 80: el
**minimax puro es 70**, cubriéndose siempre abierto. Como $60\ne70$, **no hay
punto de silla**: hay que mezclar.

**4. Reunir el modelo.**

$$\begin{aligned}
\max_{p,\,v}\quad & v\\
\text{sujeto a}\quad & 60p+70(1-p)\ \ge\ v \quad \text{(se cubre abierto)},\\
& 80p+40(1-p)\ \ge\ v \quad \text{(se cubre al centro)},\\
& 0\le p\le 1,\\
& v \text{ libre}.
\end{aligned}$$

**5. Usar los datos: el dibujo.** Las rectas son $70-10p$, que baja de 70 a
60, y $40+40p$, que sube de 40 a 80. Los vértices de arriba de la envolvente
inferior son:

| Vértice | $v$ |
|---|---:|
| $p=0$ | 40 |
| Cruce de las rectas | **64** |
| $p=1$ | 60 |

El cruce sale de igualar las rectas:

$$70-10p=40+40p\ \Longrightarrow\ 30=50p\ \Longrightarrow\ p=\tfrac35,$$

con $v=70-10\cdot\tfrac35=64$. Quien saca saca abierto con probabilidad
$3/5$ y al centro con $2/5$, y asegura **64 %** de los puntos, 4 puntos más
que el mejor saque fijo.

**6. Comprobar con quien resta.** Contra un saque abierto, la mezcla
$(q,1-q)$ deja a quien saca en $60q+80(1-q)=80-20q$; contra un saque al
centro, en $70q+40(1-q)=40+30q$. Igualando,

$$80-20q=40+30q\ \Longrightarrow\ 40=50q\ \Longrightarrow\ q=\tfrac45.$$

Con esa $q$, los dos saques dan $80-16=64$. Quien resta se cubre abierto con
probabilidad $4/5$ y asegura que quien saca no pase de **64 %**. Los dos
números coinciden, como dice el teorema minimax: el valor del juego es 64.

**7. Tipo de modelo, método y costo.** Es un juego simultáneo de suma cero,
y la mejor mezcla es un programa **lineal continuo** con dos variables, $p$
y $v$, y dos restricciones de columna. Con dos acciones se resuelve
dibujando: basta evaluar la envolvente en tres vértices, $p=0$, $p=1$ y el
cruce, cada uno con un par de multiplicaciones. Con $I$ saques y $J$
coberturas serían $I+1$ variables y $J$ restricciones, y se resolvería con
simplex.

**8. Límite.** El modelo supone que los porcentajes son fijos y conocidos, y
que cada punto es una decisión aislada. Una jugadora real que alterna con un
patrón, por ejemplo abierto, abierto, centro, deja de mezclar de verdad: si
la rival descubre el patrón, ya no está en el caso de la tabla. Además, los
porcentajes son estimaciones de cientos de puntos y cambian con el
cansancio o con la superficie.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Separaste quién decide qué de los números dados, y dijiste qué nota sobra.
- Justificaste que es simultáneo y de suma cero con las notas, no de
  memoria.
- La tabla tiene a quien saca en las filas y los pagos en % de puntos que
  gana quien saca.
- Calculaste maximin y minimax puros antes de mezclar.
- Tu programa tiene una restricción por cada columna de quien resta y $v$
  libre.
- Comprobaste el valor desde las dos jugadoras.

## 2 · Diagnosticar el juego de la gallina

Dos autos van de frente por un camino angosto. Al mismo tiempo, cada
conductor elige **Desviarse** o **Seguir**. Quien se desvía solo pierde un
poco de orgullo; si los dos siguen, chocan. Los pagos, como (conductor de la
fila, conductor de la columna), son:

| Fila ↓ · Columna → | Desviarse | Seguir |
|---|:---:|:---:|
| **Desviarse** | (0, 0) | (−1, 1) |
| **Seguir** | (1, −1) | (−10, −10) |

::: exercise {#jue-tarea-4-ej-gallina title="Diagnostica la gallina"}
1. ¿Es un juego de suma cero? Justifícalo con una casilla.
2. Encuentra la mejor respuesta de cada conductor a cada acción del otro.
3. Encuentra todos los equilibrios de Nash puros.
4. ¿Por qué el modelo no dice cuál de ellos va a ocurrir?
5. (Opcional) Si el conductor de la columna sigue con probabilidad $1/10$,
   ¿cuánto espera ganar el de la fila con cada acción?
6. ¿Qué haría un conductor que usa maximin? ¿Eso predice qué pasa?
:::

::: hint {#jue-tarea-4-pista-gallina-a of="jue-tarea-4-ej-gallina" title="Pista 1 · Suma cero y mejores respuestas"}
¿Cuánto suman los dos pagos de cada casilla? Para las mejores respuestas,
fija la acción del otro: ¿qué pagos tuyos comparas, como en el dilema del
prisionero?
:::

::: hint {#jue-tarea-4-pista-gallina-b of="jue-tarea-4-ej-gallina" title="Pista 2 · Los equilibrios"}
Toma una casilla y pregunta a cada conductor: si el otro se queda quieto,
¿gano cambiando solo mi acción? Haz esa pregunta en las cuatro casillas, no
solo en las que parecen probables.
:::

::: answer {#jue-tarea-4-resp-gallina of="jue-tarea-4-ej-gallina" title="Respuesta · Los dos equilibrios de la gallina"}
**1. Diagnosticar el juego.** Es simultáneo y **no** es de suma cero. En
tres casillas los pagos suman 0, pero en (Seguir, Seguir) suman −20:
**chocar es malo para los dos**. Hay un resultado que ambos quieren evitar,
así que el otro no es un rival puro. Le toca una tabla con un par
$(U_1,U_2)$ por casilla.

**2. Encontrar las mejores respuestas.** Para el conductor de la fila:

| Si el otro… | Desviarse le da | Seguir le da | Mejor respuesta |
|---|---:|---:|---|
| Se desvía | 0 | 1 | Seguir |
| Sigue | −1 | −10 | Desviarse |

El juego es simétrico, así que el de la columna responde igual: **hacer lo
contrario que el otro**.

**3. Encontrar los equilibrios puros.** Son **(Desviarse, Seguir)** y
**(Seguir, Desviarse)**. En (Desviarse, Seguir), el de la fila pasaría de
−1 a −10 si cambiara a Seguir, y el de la columna pasaría de 1 a 0 si
cambiara a Desviarse: ninguno quiere moverse. El otro caso es el espejo. En
(Desviarse, Desviarse) cada uno querría seguir, y en (Seguir, Seguir) cada
uno querría desviarse.

**4. Explicar por qué no se sabe cuál ocurre.** Los dos equilibrios son
estables, pero cada conductor prefiere uno distinto: el que le toca seguir.
El modelo dice qué resultados son estables, no cuál se elige. Para saberlo
haría falta algo fuera de la tabla: una convención, una comunicación previa
o una reputación.

**5. Calcular la mezcla (opcional).** Si el otro sigue con probabilidad
$1/10$:

$$\text{Desviarse: } \tfrac{9}{10}(0)+\tfrac{1}{10}(-1)=-\tfrac{1}{10},\qquad
\text{Seguir: } \tfrac{9}{10}(1)+\tfrac{1}{10}(-10)=-\tfrac{1}{10}.$$

Las dos acciones dan lo mismo: el conductor de la fila queda **indiferente**.
Si los dos siguen con probabilidad $1/10$, ninguno gana cambiando su mezcla;
es un tercer equilibrio, con mezclas. Encontrar equilibrios así en general
queda fuera de esta clase.

**6. Leer lo que diría un maximin.** El peor caso de Desviarse es −1 y el de
Seguir es −10, así que un conductor maximin **se desvía**. Es una decisión
prudente, pero no predice el resultado: si los dos razonan así, llegan a
(Desviarse, Desviarse), que no es equilibrio, porque cada uno querría haber
seguido. El maximin supone un rival que busca dañarte, y aquí el otro solo
busca su propio pago.

**7. Tipo de modelo, método y costo.** Es un juego simultáneo de suma
general con dos acciones por jugador. Se analiza con mejores respuestas y
equilibrios de Nash puros, no con un programa lineal de maximin. El método
revisa las $2\cdot2=4$ casillas y, en cada una, compara el pago de cada
conductor con el de su otra acción: 8 comparaciones. Con $I$ filas y $J$
columnas serían $I\cdot J$ casillas, cada una con $(I-1)+(J-1)$
comparaciones.

**8. Límite.** Los pagos son inventados para el ejemplo: el modelo solo usa
su orden, no la cifra exacta, salvo en la mezcla del inciso 5, que sí
cambia si cambia el −10. Y la tabla no dice cómo llegan los conductores a un
equilibrio, ni si llegan: con dos equilibrios puros y uno mixto, chocar
sigue siendo posible.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Justificaste que no es suma cero con una casilla concreta.
- Para cada acción del otro, marcaste una mejor respuesta.
- Revisaste las cuatro casillas, no solo las que parecían probables.
- Explicaste por qué tener dos equilibrios deja abierta la pregunta.

**Punto de control:** deberías poder tomar la descripción de un juego
simultáneo de 2×2, decidir si es de suma cero y, según el diagnóstico,
resolver su mejor mezcla con un programa lineal o encontrar sus equilibrios
de Nash puros.

## Lo que hay que llevarse

- En suma cero, la mejor mezcla sale de un programa lineal, y el valor se
  puede comprobar desde los dos jugadores.
- Fuera de la suma cero se buscan mejores respuestas y equilibrios; puede
  haber más de uno, y la tabla no dice cuál ocurre.
- El maximin siempre se puede calcular, pero solo describe bien al otro
  cuando sus intereses son los opuestos de los tuyos.

Continúa con [[juegos|el inicio de la unidad de juegos]], para repasar el recorrido completo.
