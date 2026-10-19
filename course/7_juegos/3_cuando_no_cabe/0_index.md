---
id: juegos-cuando-no-cabe
title: "Clase 3 · Cuando el árbol no cabe"
nav_title: Cuando no cabe
summary: "Si no se puede llegar a los finales, hay dos salidas: cortar la búsqueda y estimar cada posición con una evaluación, o simular partidas hasta el final. La jugada que sale ya no es segura, y hay que entregarla antes de que se acabe el tiempo."
status: ready
estimated_time: 280m
tags: [juegos, busqueda-adversarial, evaluacion]
prerequisites: [juegos-mirar-todo-y-podar]
---

# Clase 3 · Cuando el árbol no cabe

**En la clase 2, alfa-beta resolvió hexapawn completo. ¿Cuántos nodos
tendría el árbol si el tablero fuera de 4×4? ¿Y en ajedrez?** En la primera
página verás que una computadora todavía resuelve el 4×4, aunque ya no se
pueda a mano; en ajedrez no se puede llegar a todos los finales, así que hay
que detenerse antes y **estimar**.

> [!TIP]
> **Esta clase tiene animaciones, tres interactivos y un notebook.** Minimax con corte y profundización iterativa en el árbol de resultados, el bono de UCT y todos los algoritmos en un mismo árbol:
>
> - **Animaciones paso a paso:** [corte](../_assets/traza_arbol_t.html#corte) · [iterativa](../_assets/traza_arbol_t.html#iterativa). Cada página de
>   algoritmo la muestra en una figura: púlsala y se abre. Todas juntas, con qué mirar en cada una, en [[animaciones-juegos|el anexo de animaciones]].
> - **Simulaciones en vivo:** [Hoeffding en vivo](../_assets/hoeffding_en_vivo.html) · [Bandido en vivo](../_assets/bandido_en_vivo.html). Las abre
>   la página «De dónde sale el bono».
> - **El mismo árbol, todos los algoritmos:** [ábrelo](../_assets/un_arbol_todos.html). Corre cada algoritmo de la unidad sobre el árbol de resultados. Lo abren «MCTS con UCT» y la radiografía.
> - **Notebook en Colab:** el mismo Python de las páginas, con el árbol dibujado en cada paso.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## Lo que traes de la clase 2

Todo lo que usa esta clase, en una tabla. Si un renglón no te suena, vuelve
a su página.

::: table {#jue-c3-repaso title="Lo que se usa de la clase 2"}
| Término | Qué es | Dónde se vio |
|---|---|---|
| $V(s)$ | El valor de un estado, desde MAX: sin azar, el pago si los dos juegan lo mejor; con dados, el valor esperado con los dos jugando lo mejor | Diagnosticar el juego y Cuando decide un dado |
| $Q(s,a)$ | El valor de una jugada: $Q(s,a)=V(T(s,a))$ | Diagnosticar el juego y Minimax a mano |
| DECIDIR-MINIMAX | Elige la jugada de la raíz con el mayor $Q$ | Minimax como algoritmo |
| Árbol de resultados | Juguete con la forma del árbol base, salvo que D tiene tres hijos: R de MAX; I, C y D de MIN; finales $+1$, $0$ o $-1$ | Minimax como algoritmo |
| $b$, $m$ | $b$: el máximo de jugadas en un estado; $m$: la partida más larga; minimax genera del orden de $b^m$ nodos | Minimax como algoritmo |
| $\alpha$, $\beta$ | Lo que MAX y MIN ya tienen asegurado en el camino | Alfa-beta a mano |
| Poda | Dejar de generar hermanos que no cambian la respuesta: un corte alfa o un corte beta | Alfa-beta a mano |
| Cota | Lo que devuelve un nodo cuyo retorno tocó o salió de su ventana de entrada: la ventana solo certifica «al menos» o «a lo más». Puede coincidir con el valor exacto si otra cosa lo demuestra, y puede pasar aunque ese nodo no pode | Alfa-beta a mano |
| DECIDIR-ALFA-BETA | Minimax con podas; el orden de las jugadas cambia cuántos nodos genera | Alfa-beta como algoritmo |
:::

Las páginas de la clase 2:
[[minimax|Minimax a mano]] ·
[[minimax-como-algoritmo|Minimax como algoritmo]] ·
[[alfa-beta|Alfa-beta a mano]] ·
[[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]] ·
[[cuando-decide-un-dado|Cuando decide un dado]].

## Qué vas a poder hacer al terminar esta clase

- Explicar por qué minimax completo no sirve para un juego como el ajedrez.
- Escribir una función de evaluación y decir qué preferencia expresa y qué
  deja fuera.
- Calcular a mano minimax con **corte** de profundidad, con los finales en
  la escala $M\cdot U$. Y distinguir el valor con corte del valor exacto.
- Reconocer el efecto horizonte y explicar qué hace la búsqueda de quietud.
- Explicar la profundización iterativa: qué jugada entregar cuando se acaba
  el tiempo y por qué repetir búsquedas cuesta poco.
- Estimar una jugada **simulando partidas**, sin función de evaluación.
  Monte Carlo plano converge a $Q_{\text{azar}}$ con muestras independientes
  bajo una regla fija; la actualización minimax mantiene $\widehat Q$ por
  jugada y $\widehat V$ por estado, y su raíz converge a $V$ bajo el contrato
  de su página.
- Explicar **MCTS** como familia de búsquedas en cuatro fases, y **UCT**
  como su miembro que selecciona con un bono. Calcular una vuelta a mano y
  decir qué jugada entrega.
- Explicar el bono de UCT como margen de error de un promedio. Por qué se
  suma y de dónde sale su tamaño. Y por qué sirve para seleccionar, no para
  entregar.

En el 4×4 y en el árbol de resultados, un final paga $U$ desde MAX: $+1$ si
gana, $-1$ si pierde y $0$ si hay empate. Cada juego define su propia escala;
la refutación, por ejemplo, usa $+10$, $-10$ y $-30$. Lo nuevo es lo que se hace cuando la búsqueda se detiene antes de un final.

---

## El hilo de la clase

Cuatro ejemplos, cada uno con su papel:

- **Una posición de peones de 4×4**, para las ideas. A profundidad 1 se
  elige ahí una jugada que pierde; las páginas comparan profundidad,
  quietud y simulación para no caer en eso.
- **El árbol de resultados**, para los algoritmos. Es tan chico que cada
  línea del pseudocódigo se sigue a mano. Lo corren todos: el corte, la
  quietud, la iterativa, los Monte Carlo y UCT.
- **La refutación A/B**, en las páginas 3 y 4, para comparar un promedio,
  la actualización minimax y UCT cuando la respuesta decisiva aparece tarde.
- **Un bandido de tres jugadas, x, y, z**, en la última página. Su
  esperanza está oculta para la regla, y sirve para ver de dónde sale el
  bono.

## Recorrido

Cinco páginas de lectura y una tarea, en orden. Las dos primeras **cortan y
estiman**; las tres siguientes **simulan**. La comparación de todos los
algoritmos tiene su propia sección, al final de la unidad:
[[juegos-radiografia|Radiografía de los algoritmos]].

::: table {#jue-ruta-3 title="Las páginas de esta clase"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 72m | **Cortar y evaluar.** Detenerse a cierta profundidad y estimar con EVAL, a mano en la posición de 4×4 y como algoritmo en el árbol de resultados |
| 2 | 72m | **Hasta dónde mirar.** El efecto horizonte, la búsqueda de quietud, la profundización iterativa contra el reloj y la tabla de transposición |
| 3 | 51m | **Simular partidas.** Monte Carlo plano promedia y converge a $Q_{\text{azar}}$ con muestras independientes bajo una regla fija; la actualización minimax guarda lo descubierto y converge a $V$ bajo su contrato |
| 4 | 45m | **MCTS con UCT.** Las cuatro fases de cada vuelta, la regla de selección con bono y la jugada más visitada |
| 5 | 40m | **De dónde sale el bono.** El margen de error de un promedio: Hoeffding, la constante de UCB1, MIN y la elección de $c$ |
| 6 | 70m, aparte | **Tarea de refuerzo.** Una evaluación de gato, otra posición de peones y tres Monte Carlo ante una respuesta certera |
:::

1. [[cortar-y-evaluar|Cortar y evaluar]]
2. [[jugar-contra-el-reloj|Hasta dónde mirar: profundidad, tiempo y horizonte]]
3. [[simular-en-vez-de-evaluar|Simular partidas: promedios y actualización minimax]]
4. [[monte-carlo-en-un-arbol-grande|MCTS con UCT]]
5. [[de-donde-sale-el-bono|De dónde sale el bono]]
6. [[tarea-cuando-no-cabe|Tarea de refuerzo]]

## Las animaciones y el notebook

Los mismos de la clase 2, con tres secciones más. Además, dos simulaciones
en vivo y un interactivo que compara los algoritmos. No se cuentan en el
tiempo de la clase.

- [La animación con corte](../_assets/traza_arbol_t.html#corte): cambia $d$ entre
  1, 2 y 3.
- [La animación de la profundización iterativa](../_assets/traza_arbol_t.html#iterativa): las
  tres búsquedas seguidas.
- [Hoeffding en vivo](../_assets/hoeffding_en_vivo.html): miles de promedios a
  la vez, contra la cota.
- [Bandido en vivo](../_assets/bandido_en_vivo.html): x, y, z con su esperanza
  oculta; mueve $c$.
- [El mismo árbol, todos los algoritmos](../_assets/un_arbol_todos.html): elige
  un algoritmo y mira qué nodos genera y qué número devuelve.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

*Se abre en Google Colab, en otra pestaña.* Las secciones de esta clase son
la 6, la 7 y la 8. Van con las páginas 1, 2 y 5.

## Qué no cubre esta clase

- **MCTS y UCT** se presentan con su mapa, sus cuatro fases y su regla de
  selección, que calculas con números. No escribimos su pseudocódigo.
- **De dónde sale el bono** se explica con simulaciones. La desigualdad de
  Hoeffding se cita, no se demuestra, y tampoco demostramos que UCT
  converge.
- **AlphaGo y AlphaZero** se mencionan, no se desarrollan.
- **La evaluación** la escribimos a mano; no la aprendemos de partidas.
- **Comparar todos los algoritmos** y elegir uno para un juego nuevo es la
  [[juegos-radiografia|radiografía]], al final de la unidad.

Empieza por [[cortar-y-evaluar|cortar y evaluar]].
