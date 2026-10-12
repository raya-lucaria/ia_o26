---
id: mas-alla-del-horizonte
title: Más allá del horizonte
nav_title: Más allá del horizonte
summary: "Una búsqueda cortada no ve lo que queda detrás del corte: el efecto horizonte. Mirar las capturas antes de evaluar, la búsqueda de quietud, arregla los intercambios, pero no todo."
status: ready
estimated_time: 20m
tags: [juegos, busqueda-adversarial, evaluacion]
---

# Más allá del horizonte

**¿Qué pasa con lo que la búsqueda no alcanza a ver?**

Al terminar tendrás:

- **el efecto horizonte**: señalar, en una posición de peones, qué jugada
  queda detrás del corte y qué valor cambia por ella;
- **sus dos formas**: la simple, una respuesta que queda detrás, y la
  clásica, una pérdida que el programa aplaza;
- **la búsqueda de quietud**: calcular a mano cuánto vale cada jugada a
  profundidad 1 si antes de evaluar se miran las capturas;
- **su límite**: decir qué horizontes arregla y cuáles no.

> **Las reglas, en el tablero de 4×4.** Columnas a–d y filas 1–4; Blancas
> (B) empieza con cuatro peones en la fila 1 y Negras (N) con cuatro en la
> fila 4. Un peón avanza una casilla si está vacía o captura en diagonal
> hacia delante. Gana quien llega a la fila del rival, captura todo o deja
> al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$ si gana Negras.

> **Las piezas que usa esta página.** Las de
> [[escribir-el-juego|Escribir el juego]]: $A(s)$ (@jue-c1-acciones),
> $T(s,a)$ (@jue-c1-transicion) y $U(s)$ (@jue-c1-utilidad). Y las de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: $\mathrm{EVAL}$
> (@jue-c3-evaluacion) y el valor con corte (@jue-c3-valor-con-corte).

> **Supuestos de esta página.** Los de
> [[cortar-y-evaluar|Cortar y evaluar a mano]]: un juego por turnos, sin
> azar y a la vista, cuyo árbol no cabe; la búsqueda se corta.

Seguimos con la posición de la clase y la misma evaluación,
$\mathrm{EVAL}=10\cdot\text{material}+\text{avance}$. El material es peones
blancos menos peones negros; el avance, avance blanco menos avance negro. En
los finales, $100\cdot U=\pm100$. Como siempre, $d$ es **la profundidad que
queda**.

::: table {#jue-c3-horizonte-posicion title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

Éstos son los valores de @jue-c3-profundidades, en
[[cortar-y-evaluar|Cortar y evaluar a mano]]. La última es el valor
exacto: el valor del juego, $V$, por 100 para usar la misma escala.

::: table {#jue-c3-horizonte-valores title="Cada jugada, cortada a profundidad 1, 2 y 3, y su valor del juego"}
| Jugada | Prof. 1 | Prof. 2 | Prof. 3 | Exacto, $100\cdot V$ |
|---|---:|---:|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 2 | $-10$ | $-9$ | $-100$ |
| $\text{d2}\textbf{-}\text{d3}$ | 2 | 1 | 100 | 100 |
| $\text{d2}\textbf{x}\text{c3}$ | 13 | 0 | 1 | $-100$ |
:::

## 1 · Reconocer el efecto horizonte

**Piensa: a profundidad 1, ¿qué no alcanzó a ver Blancas cuando eligió
capturar?**

A profundidad 1, $\text{d2}\textbf{x}\text{c3}$ valía 13 y las otras dos
jugadas, 2. El algoritmo vio **la ganancia**: un peón de más. No vio **la
respuesta**: Negras recaptura con $\text{b4}\textbf{x}\text{c3}$ y el peón
de ventaja desaparece. A profundidad 2 la captura bajó a 0, y Blancas
cambió de jugada.

La recaptura existía desde el principio. Estaba una jugada más allá de la
línea donde se corta, y el algoritmo no mira detrás de esa línea. **A la
línea donde se corta la llamamos horizonte.**

::: definition {#jue-c3-efecto-horizonte title="Efecto horizonte"}
El **efecto horizonte** ocurre cuando una consecuencia importante de una
jugada queda detrás del horizonte. La búsqueda evalúa la posición antes de
esa consecuencia, y la valora mal.

**Qué significa:** el número del nodo de corte describe una posición a
mitad de algo que todavía no termina.

**El caso clásico.** Hans Berliner le dio nombre en 1973 pensando en otra
forma: una **pérdida inevitable que el programa aplaza**. El programa
intercala jugadas que el rival tiene que contestar, y cada una empuja la
pérdida dos jugadas más lejos. Cuando sale del horizonte, el programa cree
que la evitó.

Por ejemplo, un programa de ajedrez que va a perder la dama
da un jaque tras otro. No salva la dama: solo deja de ver su pérdida.
:::

El ejemplo de esta página es la forma simple: **una sola respuesta, la
recaptura, queda detrás del horizonte**. En ajedrez pasa igual cuando una
pieza captura un peón defendido y el corte cae antes de la recaptura.

::: figure {#jue-c3-fig-horizonte title="El efecto horizonte: la recaptura queda detrás"}
![La posición de la clase arriba; la flecha d2xc3 lleva a un nodo de corte con EVAL = 13, un peón de más. Debajo, una línea punteada marca el horizonte, donde se corta con d = 1 en la raíz. Detrás está la recaptura b4xc3, en una caja punteada con «?»: la búsqueda no la genera. Con ella, EVAL bajaría a 0](../_assets/jue-c3-horizonte.svg)
:::

> [!WARNING]
> **Subir la profundidad no elimina el efecto horizonte: lo mueve.** A
> profundidad 2 la recaptura ya se ve, pero el horizonte sigue ahí, una
> jugada más abajo. A cualquier profundidad fija puede quedar algo
> importante justo detrás.

::: exercise {#jue-c3-ej-detras title="Encuentra lo que queda detrás a profundidad 2"}
En @jue-c3-horizonte-valores, $\text{d2}\textbf{-}\text{d3}$ vale 1 a
profundidad 2 y 100 a profundidad 3.

1. ¿Qué jugada queda detrás del horizonte de profundidad 2 y hace saltar
   ese valor?
2. ¿Cambia la jugada que Blancas elige a profundidad 2?
:::

::: hint {#jue-c3-pista-detras-1 of="jue-c3-ej-detras" title="Qué agrega un nivel"}
La profundidad 3 agrega una sola jugada, de Blancas. ¿Qué tendría que pasar
en esa jugada para que el número salte de 1 a 100?
:::

::: answer {#jue-c3-resp-detras of="jue-c3-ej-detras"}
1. **$\text{d3}\textbf{-}\text{d4}$.** Tras $\text{d2}\textbf{-}\text{d3}$,
   Negras solo puede avanzar a3 o b3. Después, Blancas lleva el peón de d3
   a la fila 4 y gana: $100\cdot U=100$. A profundidad 2, el corte cae
   justo antes de esa jugada.
2. **No cambia.** A profundidad 2, $\text{d2}\textbf{-}\text{d3}$ ya era la
   mayor: 1 contra 0 y $-10$. El horizonte escondió **cuánto** vale, no
   **cuál** es la mejor. El efecto horizonte hace daño cuando cambia la
   decisión, como a profundidad 1.
:::

## 2 · Buscar un poco más donde hay capturas

**Piensa: ¿en qué posiciones es peligroso detenerse a evaluar?**

En las que tienen **capturas pendientes**: ahí $\mathrm{EVAL}$ cambiará en
la jugada siguiente. En [[minimax-con-corte|Minimax con corte]] intentamos
adivinarlas con un rasgo que resta 10 por cada captura de Negras. La
captura todavía ganaba, 3 contra 2. En vez de adivinar las capturas, se
pueden **mirar**.

::: definition {#jue-c3-quietud title="Posición quieta y búsqueda de quietud"}
Una posición es **quieta** si el jugador de turno no tiene ninguna captura
disponible. En ella, $\mathrm{EVAL}$ es más confiable.

La **búsqueda de quietud** cambia lo que pasa en un nodo de corte que no
es quieto. En vez de evaluar ahí, sigue mirando **solo las capturas** hasta
llegar a posiciones quietas, y evalúa en ellas. En cada paso, el jugador de
turno elige entre capturar o **quedarse** con la $\mathrm{EVAL}$ de la
posición.

**Qué significa:** el corte ya no cae en medio de un intercambio.

**Qué no es:** no es buscar una jugada más en todas partes. Solo se siguen
las capturas, y solo desde los nodos de corte.
:::

Quedarse representa las jugadas que no son captura: nadie está obligado a
capturar, y la quietud no las mira. En DECIDIR-CON-CORTE solo cambia la
línea 9: en vez de devolver $\mathrm{EVAL}(s)$, llama a la búsqueda de
quietud.

**Ejemplo: la captura, a profundidad 1.**

- **El nodo de corte.** Tras $\text{d2}\textbf{x}\text{c3}$ queda $d=0$ y
  mueven Negras. El peón de b4 tiene al peón blanco de c3 en su diagonal:
  la posición no es quieta.
- **Las dos opciones de Negras.** Quedarse, con $\mathrm{EVAL}=13$, o
  capturar con $\text{b4}\textbf{x}\text{c3}$.
- **Tras la captura.** Mueven Blancas, con peones en a1 y c2. Ninguno tiene
  un peón negro en su diagonal: la posición es quieta. Se evalúa: 0.
- **Lo que elige Negras.** Es MIN: $\min(13,0)=0$. La captura vale **0**.

Es el mismo 0 que a profundidad 2, pero sin mirar todas las respuestas de
Negras: solo su captura.

::: exercise {#jue-c3-ej-quietud title="Calcula la quietud de las otras dos jugadas"}
Haz lo mismo con $\text{a1}\textbf{-}\text{a2}$ y
$\text{d2}\textbf{-}\text{d3}$, a profundidad 1. En el corte, las dos
tienen $\mathrm{EVAL}=2$.

1. ¿Es quieta la posición tras cada una? Si no lo es, ¿qué captura tiene
   Negras?
2. ¿Qué valor recibe cada jugada con la búsqueda de quietud?
3. Con los tres valores, ¿qué jugada elige Blancas? Compárala con la
   columna del valor exacto de @jue-c3-horizonte-valores.
:::

::: hint {#jue-c3-pista-quietud-1 of="jue-c3-ej-quietud" title="Los mismos cuatro pasos"}
Recorre, para cada jugada, los cuatro pasos del ejemplo. ¿Qué peones negros
tienen un peón blanco en una diagonal de enfrente, hacia abajo? Y si hay
captura, ¿la posición que deja es quieta para Blancas?
:::

::: answer {#jue-c3-resp-quietud of="jue-c3-ej-quietud"}
1. Tras **$\text{a1}\textbf{-}\text{a2}$**, el peón de c3 puede capturar en
   d2: $\text{c3}\textbf{x}\text{d2}$. Tras
   **$\text{d2}\textbf{-}\text{d3}$**, el peón de c3 tiene c2 ocupada
   enfrente y nada en b2 ni en d2: la posición es quieta.
2. En $\text{a1}\textbf{-}\text{a2}$, Negras elige entre quedarse, 2, y
   $\text{c3}\textbf{x}\text{d2}$. Tras esa captura, Blancas tiene peones
   en a2 y c2 y nada que capturar: es quieta, con $\mathrm{EVAL}=-10$.
   Negras toma $\min(2,-10)=-10$. $\text{d2}\textbf{-}\text{d3}$ es quieta
   y se queda con su 2.
3. Los valores son $-10$, 2 y 0. Blancas elige
   **$\text{d2}\textbf{-}\text{d3}$**, la que gana: su valor exacto es 100.
   Con solo mirar las capturas, la profundidad 1 dejó de elegir la captura
   perdedora.
:::

Mirar las capturas suele costar poco, porque en muchas posiciones hay
pocas. Y en este juego la búsqueda de quietud siempre termina: cada captura
quita un peón, y los peones se acaban.

## 3 · Clasificar horizontes por tu cuenta

**Piensa: ¿la búsqueda de quietud arregla cualquier efecto horizonte?**

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-clasifica title="Clasifica dos horizontes"}
- **Programa B** busca a profundidad 1 **con** búsqueda de quietud. Valora
  $\text{d2}\textbf{-}\text{d3}$ en 2, y su valor exacto es 100.
- **Programa C** juega ajedrez a profundidad fija. Va a perder la dama sin
  remedio. En vez de aceptarlo, da un jaque tras otro, y con esos jaques la
  pérdida queda detrás del horizonte.

1. ¿Cuál de los dos es el caso clásico y cuál la forma simple?
2. En B, ¿qué queda detrás del horizonte, y por qué la búsqueda de quietud
   no lo ve?
3. En C, ¿lo arregla buscar dos jugadas más?
4. ¿En cuál de los dos el error cambia la jugada que elige el programa?
:::

::: hint {#jue-c3-pista-clasifica-1 of="jue-c3-ej-clasifica" title="Pista 1 · Quién juega hasta la consecuencia"}
Para cada programa, escribe la consecuencia que no ve. Entre el corte y esa
consecuencia, ¿quién mueve: solo el rival, o también el propio programa?
:::

::: hint {#jue-c3-pista-clasifica-2 of="jue-c3-ej-clasifica" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿La jugada que B no ve es de las
que la búsqueda de quietud sigue? Si C busca dos jugadas más, ¿qué hace si
todavía le queda un jaque por dar?
:::

::: answer {#jue-c3-resp-clasifica of="jue-c3-ej-clasifica" title="Respuesta · Una victoria escondida y una pérdida aplazada"}
1. **C es el caso clásico; B, la forma simple.** En C, el programa mueve
   entre el corte y la pérdida: sus jaques la aplazan. En B nadie aplaza
   nada. La victoria está a dos jugadas, y el corte cae antes.
2. **Detrás queda $\text{d3}\textbf{-}\text{d4}$**, tras cualquier avance
   de Negras. No es una captura: es un avance. La posición tras
   $\text{d2}\textbf{-}\text{d3}$ es quieta, así que la quietud evalúa ahí
   y se queda con 2. La búsqueda de quietud solo arregla los intercambios.
3. **No necesariamente.** Si quedan jaques, el programa da uno más y la
   pérdida vuelve a quedar detrás. El horizonte se mueve, no desaparece.
   Mientras haya jugadas para aplazar, ninguna profundidad fija alcanza.
4. **En C.** El programa juega los jaques en lugar de la jugada que reduce
   el daño, y la dama se pierde igual. En B la decisión es correcta: 2 le
   gana a 0 y a $-10$. Solo el valor está mal.
:::

**Punto de control:** deberías poder señalar qué jugada queda detrás del
horizonte en una posición de peones. Y decir si la posición donde se corta es
quieta, y calcular a mano su valor con quietud.

## Lo que hay que llevarse

- **El horizonte es la línea donde se corta.** A profundidad 1,
  $\text{d2}\textbf{x}\text{c3}$ valía 13 porque la recaptura
  $\text{b4}\textbf{x}\text{c3}$, que la deja en 0, quedaba detrás.
- **Dos formas.** La simple: una respuesta queda detrás. La clásica, que
  nombró Berliner en 1973: el programa aplaza una pérdida inevitable hasta
  sacarla del horizonte.
- **Subir la profundidad mueve el horizonte, no lo quita.** A profundidad
  2, $\text{d2}\textbf{-}\text{d3}$ vale 1 y la victoria, 100, sigue
  detrás.
- **La búsqueda de quietud** sigue solo las capturas desde los nodos de
  corte. A profundidad 1 da $-10$, 2 y 0, y elige
  $\text{d2}\textbf{-}\text{d3}$, la jugada que gana. No ve lo que no es
  captura: con ella, $\text{d2}\textbf{-}\text{d3}$ sigue valiendo 2.

Continúa con [[jugar-contra-el-reloj|jugar contra el reloj]].
