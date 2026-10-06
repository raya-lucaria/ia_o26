---
id: simular-en-vez-de-evaluar
title: Simular en vez de evaluar
nav_title: Simular
summary: "La otra respuesta cuando el árbol no cabe: estimar cuánto vale una jugada jugando muchas partidas al azar hasta el final y promediando. Es la búsqueda de árbol Monte Carlo, la base de AlphaGo."
status: ready
estimated_time: 15m
tags: [juegos, busqueda-adversarial, monte-carlo]
---

# Simular en vez de evaluar

**¿Se puede estimar una posición sin escribir una función de evaluación?**

Sí. Al terminar conocerás la **búsqueda de árbol Monte Carlo**, o **MCTS**
(del inglés *Monte Carlo tree search*): su idea, sus cuatro pasos y en qué
se distingue de cortar y evaluar. Es un adelanto: no la calculamos a mano.

> **Notación de la clase 1.** $\mathrm{Pl}(s)$ es el jugador de turno, como
> en [[escribir-el-juego|Escribir el juego]]. La utilidad es $U=+1$ si gana
> MAX y $U=-1$ si gana MIN.

## 1 · Jugar al azar y promediar

**Piensa: si no sabes cuánto vale una posición, ¿cómo lo averiguarías sin
escribir ninguna regla sobre el juego?**

Jugando. Desde esa posición, juega muchas partidas eligiendo cada jugada al
azar, hasta el final. Anota la $U$ de cada una y promedia.

::: definition {#jue-c3-simulacion title="Simulación"}
Una **simulación** desde un estado $s$ es una partida que empieza en $s$ y
sigue hasta un final, eligiendo en cada estado una jugada al azar de
$A(s)$. Su resultado es la $U$ del final al que llega.

**Qué significa:** el promedio de muchas simulaciones estima qué tan buena
es $s$ para MAX, en la escala de $U$: entre $-1$ y $+1$.

**Qué no es:** no es el valor $V(s)$. Un rival al azar no es un rival que
piensa: una posición puede ganarse en casi todas las simulaciones y
perderse contra quien encuentra la única respuesta buena.
:::

Por ejemplo, supón que de 10 simulaciones desde $s$ MAX gana 7 y pierde 3.
El promedio es

$$\frac{7\cdot(+1)+3\cdot(-1)}{10}=0.4.$$

## 2 · Qué cambia respecto de la evaluación

**Piensa: ¿qué necesita saber del juego este método, además de las
reglas?**

Nada. Esa es la diferencia con [[cortar-y-evaluar|cortar y evaluar]]:

::: table {#jue-c3-eval-contra-mcts title="Cortar y evaluar contra Monte Carlo"}
| | Cortar y evaluar | Monte Carlo |
|---|---|---|
| Qué necesita, además de las reglas | Una $\mathrm{EVAL}$ escrita a mano | Nada: solo jugar con $A$ y $T$ hasta un final |
| Dónde se detiene | En la profundidad de corte | En los finales, dentro de cada simulación |
| Qué número da | El minimax de $\mathrm{EVAL}$ | Un promedio de $U$ |
| Cómo mejora | Más profundidad o una $\mathrm{EVAL}$ mejor | Más simulaciones |
:::

Por eso sirve en juegos donde nadie sabe escribir una buena evaluación.
El ejemplo clásico es el **Go**.

## 3 · Los cuatro pasos

Simular solo desde la raíz desperdicia tiempo: reparte igual las partidas
entre jugadas buenas y malas. MCTS **construye un árbol poco a poco** y
manda más simulaciones a las jugadas que van mejor.

Cada nodo del árbol guarda dos números: cuántas simulaciones pasaron por
él y la suma de sus resultados. Con ellos se calcula su promedio.

Cada vuelta tiene cuatro pasos:

1. **Selección.** Desde la raíz, baja por el árbol ya construido. En cada
   nodo elige al hijo con mejor puntaje (sección 4), hasta llegar a un
   nodo con alguna jugada que todavía no está en el árbol.
2. **Expansión.** Agrega al árbol un hijo nuevo: $T(s,a)$ para una de esas
   jugadas $a$.
3. **Simulación.** Desde ese hijo, juega una partida al azar hasta un final
   y anota su $U$.
4. **Retropropagación.** Sube por el camino recorrido hasta la raíz. En cada
   nodo, suma 1 a sus simulaciones y suma el resultado a su total.

Si la selección llega a un final, no hay nada que expandir ni simular: su
$U$ es el resultado de la vuelta.

Las vueltas se repiten mientras haya tiempo. Al final se juega la jugada de
la raíz **por la que pasaron más simulaciones**. Como la profundización
iterativa de [[jugar-contra-el-reloj|la página anterior]], siempre tiene una
jugada lista.

## 4 · Explorar o aprovechar

**Piensa: ¿conviene seguir probando la jugada que va mejor, o darle otra
oportunidad a una que casi no se ha probado?**

Las dos cosas. **Aprovechar** es elegir lo que ya funcionó; **explorar** es
probar lo poco probado, por si es mejor. La regla más usada, llamada
**UCT**, le suma a cada promedio un bono que crece si la jugada se ha
probado poco:

$$\text{puntaje}(s')=\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

- $s$ es el nodo donde se elige y $s'$, uno de sus hijos.
- $\bar u(s')$ es el promedio de las simulaciones que pasaron por $s'$,
  visto desde el jugador $\mathrm{Pl}(s)$: si es MIN, se le cambia el signo.
- $N(s)$ y $N(s')$ cuentan las simulaciones que pasaron por cada nodo.
- $\ln$ es el logaritmo natural; aquí solo importa que crece muy despacio.
- $c$ es un número positivo que elegimos: más grande, más exploración.

El primer término aprovecha; el segundo explora. Un hijo que nunca se ha
probado tiene $N(s')=0$ y se prueba antes que los demás. Con muchas
simulaciones el bono se encoge y manda el promedio.

::: exercise {#jue-c3-ej-mcts title="Decide qué jugada entrega MCTS"}
Tras 100 vueltas, las tres jugadas de la raíz, donde mueve MAX, tienen:

| Jugada | Simulaciones | Promedio |
|---|---:|---:|
| x | 60 | 0.5 |
| y | 30 | 0.6 |
| z | 10 | 0.2 |

1. Si el tiempo se acaba ahora, ¿qué jugada se entrega?
2. ¿Cuál de las tres recibe el bono de exploración más grande?
:::

::: answer {#jue-c3-resp-mcts of="jue-c3-ej-mcts"}
1. **x**: es la que tiene más simulaciones, aunque y promedie un poco más.
   Con solo 30 partidas, el 0.6 de y es menos confiable.
2. **z**: el bono tiene $N(s')$ abajo, y z es la menos probada.
:::

## 5 · El ancla: AlphaGo

- **Desde 2006**, cuando Rémi Coulom le dio nombre al método, los programas
  de Go más fuertes usan MCTS.
- **En marzo de 2016, AlphaGo**, de DeepMind, venció 4 a 1 a Lee Sedol, uno
  de los mejores jugadores de Go del mundo. Combinaba MCTS con **redes
  neuronales**: una sugería qué jugadas explorar y otra estimaba cuánto
  valía una posición.
- **AlphaZero, en 2017**, quitó las simulaciones al azar y se quedó con el
  árbol y las redes, que aprende jugando contra sí mismo.

La pregunta es la de toda la unidad: qué hará el rival. Lo que cambia es
cómo se estima lo que no se alcanza a calcular.

**Punto de control:** deberías poder decir los cuatro pasos de MCTS, en qué
se distingue de cortar y evaluar y qué papel tienen los dos términos del
puntaje.

## Lo que hay que llevarse

- MCTS estima una jugada simulando partidas al azar hasta el final y
  promediando su $U$. No necesita $\mathrm{EVAL}$: solo las reglas.
- Cada vuelta tiene cuatro pasos: selección, expansión, simulación y
  retropropagación. Al final se juega la jugada más simulada.
- El puntaje equilibra aprovechar lo que va bien y explorar lo poco
  probado.
- AlphaGo (2016) combinó MCTS con redes neuronales y venció a Lee Sedol.

Continúa con [[tarea-cuando-no-cabe|la tarea de refuerzo]].
