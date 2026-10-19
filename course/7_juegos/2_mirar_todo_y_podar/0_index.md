---
id: juegos-mirar-todo-y-podar
title: "Clase 2 · Mirar todo y podar"
nav_title: Mirar todo y podar
summary: "Calcular quién gana un juego que cabe completo: minimax desde los finales, alfa-beta para no generar ramas que no cambian la respuesta y expectiminimax cuando un dado decide."
status: ready
estimated_time: 203m
tags: [juegos, minimax, alfa-beta, algoritmos]
prerequisites: [juegos-leer-y-escribir]
---

# Clase 2 · Mirar todo y podar

**En la clase 1 jugaste tres partidas de hexapawn. Revísalas: ¿quién ganó?
¿Podía haber ganado el otro? Con nuestras reglas (quedarse sin jugada
pierde), ¿por qué quien juega segundo puede ganar siempre?** Al final de la
primera página tendrás la respuesta calculada, no adivinada.

La clase 1 escribió el juego; esta lo resuelve. Hexapawn cabe completo en la
memoria de una computadora, así que podemos **mirar todo** el árbol. Después
aprenderemos a **podar**: dejar ramas sin generar sin cambiar la respuesta.

> [!TIP]
> **Esta clase tiene animaciones y un notebook.** Minimax, alfa-beta y expectiminimax, corriendo en el árbol base:
>
> - **Animaciones paso a paso:** [minimax](../_assets/traza_arbol_t.html#minimax) · [alfa-beta](../_assets/traza_arbol_t.html#alfa-beta) · [con dados](../_assets/traza_arbol_t.html#azar). Cada página de
>   algoritmo la muestra en una figura: púlsala y se abre. Todas juntas, con qué mirar en cada una, en [[animaciones-juegos|el anexo de animaciones]].
> - **Notebook en Colab:** el mismo Python de las páginas, con el árbol dibujado en cada paso.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## Lo que traes de la clase 1

Todo lo que usa esta clase, en una tabla. Si un renglón no te suena, vuelve
a su definición en [[escribir-el-juego|Escribir el juego]] o en
[[diagnosticar-el-juego|Diagnosticar el juego]].

::: table {#jue-c2-repaso title="El juego, sus piezas y lo que se busca"}
| | Qué es, y en hexapawn |
|---|---|
| $s$ | Un estado: el tablero y a quién le toca. *Ej.: n1* |
| $s_0$ | El estado inicial. *Tres peones por lado; mueve Blancas* |
| $S_F$ | Los estados donde la partida terminó. *Alguien llegó, capturó todo o dejó al otro sin jugada* |
| $\mathrm{Pl}(s)$ | Quién mueve en un estado no final: lee el turno guardado en $s$. *Blancas es MAX; Negras es MIN* |
| $A(s)$ | Las jugadas permitidas en $s$. *En n1: $\text{c1}\textbf{-}\text{c2}$ y $\text{c1}\textbf{x}\text{b2}$* |
| $T(s,a)$ | El estado al que lleva la jugada $a$. *Desde n1, $\text{c1}\textbf{-}\text{c2}$ lleva a n2* |
| $U(s)$ | El pago de un final, **siempre desde MAX**. *$+1$ si gana Blancas, $-1$ si gana Negras* |
| $V(s)$ | El **valor de un estado**: el pago para MAX si, desde $s$, **los dos juegan lo mejor**. En un final, $V(s)=U(s)$. *$V(s_0)=-1$: gana Negras; esta clase lo calcula* |
| $Q(s,a)$ | El **valor de una jugada**: $Q(s,a)=V(T(s,a))$, lo que vale el hijo al que lleva. *Esta clase calcula los de n1* |
| $a$ | Una jugada: lo que se hace ahora. *Ej.: $\text{c1}\textbf{-}\text{c2}$* |
| $\operatorname{arg\,max}$ | El **conjunto** de jugadas que alcanzan el máximo; puede tener varias |
:::

Y tres palabras que no son símbolos:

- **Racional:** elige lo mejor **según su utilidad**, con lo que sabe y lo
  que alcanza a calcular. No quiere decir que gane (@jue-c1-racional).
- **Estrategia:** una jugada para **cada** estado donde le toca a un
  jugador, no solo para el actual.
- **Supuestos:** por turnos, sin azar, todo a la vista, toda partida
  termina y suma cero (o constante): lo que gana uno lo pierde el otro.

El problema de la unidad (@jue-c1-problema), escrito completo:

> **Dado:** las reglas del juego, $\bigl(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\
> T,\ U\bigr)$. No el grafo dibujado: las reglas para generarlo.
>
> **Encontrar:** en cada estado $s$ donde le toca a MAX, una jugada
>
> $$a^{*}\in\operatorname*{arg\,max}_{a\in A(s)} Q(s,a),$$
>
> es decir, la jugada que lleva al hijo de mayor valor.
>
> **Qué significa:** si MAX juega $a^{*}$ y sigue eligiendo así en cada
> turno, se asegura al menos $V(s)$ contra cualquier respuesta de MIN, y
> exactamente $V(s)$ si MIN juega lo mejor.

Lo único que falta para resolverlo es **cómo se calcula $V$**. Eso es la
primera página.

## Qué vas a poder hacer al terminar esta clase

- Calcular a mano $V$ y $Q$ en un árbol pequeño, desde los finales hacia la
  raíz. Y separar el valor de la jugada que lo alcanza.
- Decir qué **recibe** y qué **genera** minimax. Recibe las reglas, no el
  grafo, y genera los estados mientras recorre.
- Leer el **mapa** de cada algoritmo: qué valor rastrea, dónde lo guarda y
  cómo sube. Y sus propiedades: garantía, costo y si se puede interrumpir.
- Ejecutar alfa-beta a mano, marcar cada **poda** como corte alfa o corte
  beta y decir qué nodos nunca se generan.
- Explicar por qué las podas son seguras y por qué el orden de las jugadas
  decide cuánto ahorra alfa-beta.
- Valorar un árbol con nodos de azar con expectiminimax. Y decir cuándo
  tratar el azar como un rival, o a un rival como azar, es un error de
  modelado.

---

## El hilo de la clase

El juego de la clase es hexapawn, y su ejemplo, el subgrafo de **n1**, el
que dibujaste en [[el-juego-como-grafo|El juego como grafo]]. Son trece
estados, numerados en el orden en que los visita minimax. La utilidad es la
de la clase 1: $+1$ si gana Blancas y $-1$ si gana Negras.

Los algoritmos se siguen línea por línea en tres árboles de juguete:

- **El árbol base**, con MAX en la raíz, tres ramas y hojas de 2 a 12. Lo
  usan minimax, alfa-beta y los dados.
- **El árbol reducido**, el árbol base sin su rama del centro. Es la primera
  poda de alfa-beta, con siete nodos.
- **El árbol de resultados**, con finales $+1$, $0$ y $-1$. Cada página de
  algoritmo lo corre al final, para compararlos después en la radiografía.

## Recorrido

Cinco páginas, en orden, y una tarea de refuerzo al final. Las cuatro
primeras van en pares: primero **a mano**, con números, y después **como
algoritmo**, en general. La quinta agrega un dado.

::: table {#jue-ruta-2 title="Las páginas de esta clase"}
| | Minutos | Página y qué resuelve |
|---|---:|---|
| 1 | 30m | **Minimax a mano.** Calcular $V$ y $Q$ en n1 desde los finales y saber quién gana hexapawn |
| 2 | 47m | **Minimax como algoritmo.** DECIDIR-MINIMAX, su mapa y su traza en el árbol base, por qué es correcto y cuánto cuesta |
| 3 | 35m | **Alfa-beta a mano.** $\alpha$, $\beta$ y la regla de cada poda en el árbol reducido y el árbol base, la ventana y n1 |
| 4 | 55m | **Alfa-beta como algoritmo.** DECIDIR-ALFA-BETA línea por línea, qué guarda la pila, por qué las podas son seguras y por qué el orden importa |
| 5 | 36m | **Cuando decide un dado: expectiminimax.** Un nodo que no decide nadie vale una esperanza; con dados importan las distancias entre pagos |
| 6 | 45m, aparte | **Tarea de refuerzo.** Resolver monedas en fila, también con azar, y n1 cuando quedarse sin jugada es empate |
:::

1. [[minimax|Minimax a mano]]
2. [[minimax-como-algoritmo|Minimax como algoritmo]]
3. [[alfa-beta|Alfa-beta a mano]]
4. [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]]
5. [[cuando-decide-un-dado|Cuando decide un dado: expectiminimax]]
6. [[tarea-mirar-todo-y-podar|Tarea de refuerzo]]

## Las animaciones y el notebook

Dos formas de ver correr los algoritmos de esta clase, sin escribir nada. No
se cuentan en el tiempo de la clase y no hay nada que entregar.

**Las animaciones.** Una página con el árbol, el pseudocódigo con la línea
que corre y el valor de cada variable. Avanzas un paso con ▶ o con las
flechas del teclado. Cada página de algoritmo la muestra en su traza, y
[[animaciones-juegos|el anexo de animaciones]] dice qué mirar en cada una.
Aquí están todas:

- [Minimax](../_assets/traza_arbol_t.html#minimax)
- [Alfa-beta](../_assets/traza_arbol_t.html#alfa-beta)
- [Con dados](../_assets/traza_arbol_t.html#azar)

**El notebook.** El mismo Python de las páginas, instrumentado. Cada paso
muestra la fila de la traza y el árbol dibujado; un deslizador lo recorre.
Cada sección cierra con un «Pruébalo» de una línea.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Dónde vive.** En este repositorio, en
`course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb`. Colab lo ejecuta en
el navegador sin instalar nada; en tu máquina necesitas `matplotlib` e
`ipywidgets`. Para empezar: «Entorno de ejecución → Ejecutar todas».

**Cuándo.** Después de cada página de algoritmo, su sección: 3 · Minimax,
4 · Alfa-beta y 5 · Cuando decide un dado. Las secciones 6 a 8 son de la
clase 3.

## Qué no cubre esta clase

- **Aquí el árbol siempre cabe.** Resolvemos hasta los finales, sin corte
  heurístico. Qué hacer cuando no se puede, como en el ajedrez, es la
  clase 3.
- **Jugadas simultáneas, suma no constante y más jugadores** quedan fuera de
  la unidad. Cada página de algoritmo dice, en sus supuestos, qué cambiaría.

Empieza por [[minimax|minimax a mano]].
