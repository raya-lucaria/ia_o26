---
id: tarea-cuando-no-cabe
title: "Tarea de refuerzo · Evaluar sin llegar al final"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: proponer, usar y criticar una evaluación de gato a profundidad 2, y seguir una posición de peones donde mirar más no basta."
status: ready
estimated_time: 50m
tags: [juegos, evaluacion, practica]
---

# Tarea de refuerzo · Evaluar sin llegar al final

Esta tarea no se entrega. Sirve para comprobar que puedes hacer **sin
ayuda** lo de la clase: proponer una función de evaluación, calcular minimax
con corte a mano y decir qué deja fuera la evaluación.

El primer ejercicio vuelve a gato, ahora para evaluarlo sin llegar al final. El segundo es otra
posición de peones de 4×4.

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas
ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las
pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

## 1 · Evaluar gato a profundidad 2

Gato se juega en una cuadrícula de 3×3. X empieza; por turnos, cada jugador
pone su marca en una casilla vacía. Gana quien completa una de las **8
líneas**: 3 filas, 3 columnas y 2 diagonales. Si se llena la cuadrícula sin
línea, es empate. X es MAX y O es MIN.

Supón que X no puede calcular el árbol completo y necesita una función de
evaluación.

::: exercise {#jue-tarea-3-ej-gato title="Propón, usa y critica una evaluación de gato"}
1. Propón una evaluación con dos o tres rasgos y di qué preferencia expresa.
   Escríbela en tu hoja **antes de seguir leyendo**.
2. Ahora usa esta evaluación de referencia:
   $\mathrm{EVAL}(s)=(\text{abiertas para X})-(\text{abiertas para O})$.
   Una línea está **abierta para X** si no tiene ninguna O: X todavía podría
   completarla. Una línea está abierta para O si no tiene ninguna X. Calcula
   $\mathrm{EVAL}$ de la cuadrícula vacía, y después de que X pone en el
   centro.
3. Desde la cuadrícula vacía, X busca con **profundidad 2**: su jugada, la
   respuesta de O y luego evalúa. Por simetría basta con tres tipos de
   primera jugada: **centro**, **esquina** y **borde** (casilla del medio de
   un lado). Para cada una, encuentra la mejor respuesta de O y el valor.
4. ¿Qué jugada elige X?
5. ¿Qué preferencia expresa la evaluación de referencia? Escribe al menos
   dos cosas que deja fuera, y compárala con la tuya.
6. Con juego perfecto, gato termina en empate. ¿Lo sabe la evaluación? ¿Qué
   valor le darías a un final para que la evaluación respete el orden de los
   finales?
:::

::: hint {#jue-tarea-3-pista-gato-a of="jue-tarea-3-ej-gato" title="Pista 1 · Cuántas líneas pasan por cada casilla"}
¿Cuántas de las 8 líneas pasan por el centro, por una esquina y por un
borde? Esa cuenta te sirve para elegir rasgos en el inciso 1 y para usar la
evaluación de referencia: una marca de X cierra para O todas las líneas que
pasan por su casilla.
:::

::: hint {#jue-tarea-3-pista-gato-b of="jue-tarea-3-ej-gato" title="Pista 2 · Qué busca O"}
O es MIN: quiere dejar el número más bajo. ¿Dónde cierra **más** líneas de X
una sola marca de O? Con X en el centro, compara a O en una esquina con O en
un borde.
:::

::: answer {#jue-tarea-3-resp-gato of="jue-tarea-3-ej-gato" title="Respuesta · Gato elige el centro"}
**1. Proponer una evaluación.** No hay una sola respuesta correcta. Una
propuesta posible usa dos rasgos: las **amenazas**, líneas con dos marcas
propias y la tercera casilla vacía, y las líneas abiertas:

$$\mathrm{EVAL}_{\text{propia}}(s)=5\cdot\text{amenazas}+\text{abiertas},$$

donde **amenazas** son las de X menos las de O, y **abiertas**, las líneas
abiertas para X menos las abiertas para O.

Expresa que una amenaza vale lo mismo que cinco líneas abiertas: prefiere
estar a una jugada de ganar antes que tener muchas opciones lejanas. Lo que
importa es que tu propuesta diga qué rasgos mira, cómo los pesa y qué
preferencia expresa ese peso.

**2. Contar líneas.** Por el centro pasan 4 líneas: su fila, su columna y
las dos diagonales. Por una esquina pasan 3: fila, columna y una diagonal.
Por un borde pasan 2: fila y columna.

En la cuadrícula vacía, las 8 líneas están abiertas para los dos:
$\mathrm{EVAL}=8-8=0$. Con X en el centro, X conserva 8 líneas abiertas y O
pierde las 4 que pasan por el centro: $\mathrm{EVAL}=8-4=4$.

**3. Profundidad 2.** En cada caso, O pone su marca y se cuentan las líneas:

| Primera jugada de X | Mejor respuesta de O | Abiertas para X | Abiertas para O | Valor |
|---|---|---:|---:|---:|
| Centro | Una esquina | $8-3=5$ | $8-4=4$ | **1** |
| Esquina | El centro | $8-4=4$ | $8-3=5$ | $-1$ |
| Borde | El centro | $8-4=4$ | $8-2=6$ | $-2$ |

Con X en el centro, O en un borde dejaría $6-4=2$; la esquina deja menos, así
que O elige esquina. Cada esquina vale $-1$ y cada borde, $-2$.

**4. Elegir la jugada.** X compara $1$, $-1$ y $-2$ y elige el **centro**.

**5. Leer qué deja fuera.** La evaluación de referencia prefiere tener
muchas líneas posibles y quitárselas al rival. Dice que una línea abierta
vale lo mismo esté vacía o casi completa: no ve **amenazas**, porque dos X en
línea con la tercera casilla vacía cuentan igual que una línea sin marcas.
Tampoco distingue **a quién le toca**, aunque una amenaza vale mucho más si
puedes completarla ahora. Y no ve **dobles amenazas**, que es como se gana en
gato. Una propuesta como la del paso 1 cubre las amenazas, pero sigue sin
saber a quién le toca.

**6. Valorar el empate y los finales.** La computadora calcula que gato vale
**0**: con juego perfecto nadie gana, y comprueba que **cualquier** primera
jugada de X empata. La evaluación dice 1 para el centro y $-1$ para una
esquina, y no sabe que las dos llevan al mismo resultado. Como la evaluación
de referencia queda siempre entre $-8$ y $8$, basta con valorar los finales
en $+100$ si gana X, $-100$ si gana O y $0$ si empatan. Con tu propia
evaluación, el valor de ganar tiene que quedar por encima de lo más alto que
pueda dar.

**7. Tipo de modelo, método y costo.** Juego por turnos, determinista, de
información completa y suma cero, resuelto con **minimax con corte a
profundidad 2** y una evaluación escrita a mano. Mirar todas las parejas de
jugada y respuesta son $9\cdot8=72$ posiciones evaluadas; la simetría lo
reduce a tres casos, cada uno con sus respuestas de O.

**8. Límite.** El valor con corte es el minimax de la evaluación, no el del
juego: aquí distingue centro, esquina y borde, aunque las tres primeras
jugadas empatan con juego perfecto. La preferencia por el centro es un
supuesto de la evaluación, no un resultado del juego.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Escribiste tu propia evaluación y su preferencia antes de usar la de
  referencia.
- Contaste las líneas abiertas para **los dos** jugadores, no solo para X.
- En la profundidad 2, O eligió la respuesta **más baja** para X.
- Escribiste qué deja fuera la evaluación como supuestos, no como errores de
  cuenta.

## 2 · Otra posición de peones donde mirar más no basta

Las reglas son las de la clase: tablero de 4×4, gana quien llega a la fila
del rival, captura todo o deja al rival sin jugada, y los finales valen
$100\cdot U=\pm100$. La evaluación es la misma:

$$\mathrm{EVAL}(s)=10\cdot\text{material}+\text{avance},$$

donde **material** es peones blancos menos peones negros, y **avance** es el
avance blanco menos el avance negro.

::: exercise {#jue-tarea-3-ej-peones title="Sigue la decisión al crecer la profundidad"}
Mueven Blancas en esta posición:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | N |
| **2** | B | · | · | B |
| **1** | · | B | B | · |

1. Escribe $A(s)$ y calcula $\mathrm{EVAL}(s)$.
2. Calcula el valor de cada jugada a **profundidad 1**. ¿Cuál elige Blancas?
3. A **profundidad 2**, b1-b2 y c1-c2 valen $-11$ cada una. Calcula el valor
   de a2-a3 y el de d2xc3, escribiendo cada respuesta de Negras con su
   $\mathrm{EVAL}$. ¿Cuál elige Blancas?
4. La computadora calcula los valores exactos: b1-b2, c1-c2 y d2xc3 valen
   $-1$; **a2-a3 vale $+1$**. Y a más profundidad da:

   | Jugada | Prof. 3 | Prof. 4 | Prof. 5 |
   |---|---:|---:|---:|
   | b1-b2 | 1 | $-100$ | $-100$ |
   | c1-c2 | 1 | $-100$ | $-100$ |
   | a2-a3 | 0 | $-1$ | 100 |
   | d2xc3 | 0 | $-1$ | 12 |

   ¿Qué jugadas elige Blancas a cada profundidad, de 1 a 5? ¿Qué te dice eso
   sobre subir la profundidad?
5. ¿En qué profundidades aparece el efecto horizonte? Señala qué respuesta o
   qué final quedó detrás del corte.
:::

::: hint {#jue-tarea-3-pista-peones-a of="jue-tarea-3-ej-peones" title="Pista 1 · Las capturas de Negras"}
Tras cada jugada de Blancas, busca qué peones negros pueden capturar en
diagonal hacia abajo. ¿Cuánto cambia la evaluación cuando desaparece un
peón?
:::

::: hint {#jue-tarea-3-pista-peones-b of="jue-tarea-3-ej-peones" title="Pista 2 · La recaptura"}
Tras d2xc3, el peón blanco queda en c3. ¿Qué peón negro lo tiene en diagonal?
Tras a2-a3, ¿qué peón negro lo tiene en diagonal?
:::

::: answer {#jue-tarea-3-resp-peones of="jue-tarea-3-ej-peones" title="Respuesta · La captura engaña a dos profundidades"}
**1. Leer la posición.** $A(s)=\{\text{b1-b2},\ \text{c1-c2},\ \text{a2-a3},\ \text{d2xc3}\}$.
El peón de d2 tiene d3 ocupada enfrente, pero puede capturar en c3. Cada lado
tiene 4 peones; el avance de Blancas es $1+1=2$ (a2 y d2) y el de Negras,
$1+1=2$ (c3 y d3). $\mathrm{EVAL}=0$.

**2. Mirar a profundidad 1.** Las tres jugadas que avanzan suben el avance
blanco a 3: valen $0+(3-2)=1$. La captura deja 4 peones contra 3, con avance
blanco 3 (a2, y el peón que llegó a c3) y negro 1: $10+(3-1)=12$. Blancas
elige **d2xc3**.

**3. Mirar a profundidad 2.** Negras elige la respuesta de menor evaluación:

| Jugada | Respuestas de Negras y su $\mathrm{EVAL}$ | Valor |
|---|---|---:|
| a2-a3 | c3-c2: 0 · c3xd2: $-11$ · b4-b3: 0 · b4xa3: $-12$ | $-12$ |
| d2xc3 | d3-d2: 11 · a4-a3: 11 · b4-b3: 11 · b4xc3: $-1$ | $-1$ |

Con b1-b2 y c1-c2 en $-11$, Blancas compara $-11$, $-11$, $-12$ y $-1$, y
**sigue eligiendo d2xc3**. La recaptura b4xc3 ya se ve, pero las otras jugadas
también regalan un peón.

**4. Seguir la decisión al crecer la profundidad.** La jugada elegida es un
$a^{∗}\in\operatorname*{arg\,max}$, así que puede haber empates:

| Profundidad | Mejor valor | Jugadas empatadas |
|---:|---:|---|
| 1 | 12 | d2xc3 |
| 2 | $-1$ | d2xc3 |
| 3 | 1 | b1-b2, c1-c2 |
| 4 | $-1$ | a2-a3, d2xc3 |
| 5 | 100 | a2-a3 |

Solo a2-a3 gana, y solo a profundidad 5 la búsqueda la elige sin empate. La
elección cambió **varias veces**: de la captura a dos jugadas perdedoras,
luego a un empate entre la buena y la captura, y por fin a la buena.

**5. Nombrar el efecto horizonte.** Es **efecto horizonte** cada vez que una
consecuencia decisiva queda justo detrás del corte. A profundidad 1, d2xc3
vale 12 porque la recaptura b4xc3 queda detrás del horizonte; a profundidad 2
ya se ve y la captura baja a $-1$. A profundidad 3, b1-b2 y c1-c2 parecen
valer 1, y a profundidad 4 aparece que pierden ($-100$): esa derrota estaba
detrás del horizonte. Y la victoria de a2-a3 solo aparece a profundidad 5.

**6. Tipo de modelo, método y costo.** El mismo árbol MAX/MIN de un juego
por turnos, determinista y de suma cero, cortado con $d$ jugadas por mirar y
valorado con $\mathrm{EVAL}$ y $100\cdot U$: **minimax con corte**. Cuesta
$O(b^d)$ con ramificación $b$; cada profundidad más multiplica el trabajo por
hasta $b$, y aquí Blancas tiene cuatro jugadas en la raíz.

**7. Límite.** **Más profundidad no siempre basta**: el valor con corte no se
acerca al exacto de forma ordenada, y a una profundidad dada puede elegir una
jugada que pierde. Solo los valores $\pm100$ son seguros; los demás son
estimaciones de la evaluación.
:::

**Antes de abrir la respuesta, revisa tu hoja:**

- Encontraste las cuatro jugadas, incluida la captura de d2.
- A profundidad 2, revisaste **todas** las respuestas de Negras, también las
  capturas.
- Señalaste los empates en lugar de elegir una jugada al azar.
- Nombraste qué quedó detrás del horizonte en cada cambio de decisión.

**Punto de control:** deberías poder proponer una evaluación para un juego
nuevo, decir qué preferencia expresa, y seguir a mano cómo cambia la jugada
elegida al subir la profundidad.

## Lo que hay que llevarse

- Una evaluación es un modelo escrito a mano: expresa una preferencia y deja
  fuera cosas como las amenazas o quién mueve.
- Minimax con corte se calcula igual que minimax; solo cambia lo que vale una
  hoja de corte.
- Subir la profundidad no garantiza acercarse a la jugada correcta: la
  elección puede cambiar varias veces, y esos cambios delatan lo que estaba
  detrás del horizonte.

Continúa con [[juegos-sin-turnos|la clase 4]], donde los dos jugadores eligen a la vez.
