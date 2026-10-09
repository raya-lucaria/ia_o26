---
id: juegos-mirar-todo-y-podar
title: "Clase 2 · Mirar todo y podar"
nav_title: Mirar todo y podar
summary: "Calcular quién gana un juego que cabe completo: minimax desde los finales, nodos de azar que promedian y alfa-beta para no generar ramas que no cambian la respuesta."
status: ready
estimated_time: 180m
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
> **Esta clase tiene animaciones y un notebook.** Minimax, azar y alfa-beta, corriendo en el árbol T:
>
> - **▶ Animaciones paso a paso:** [minimax](../_assets/traza_arbol_t.html#minimax) · [alfa-beta](../_assets/traza_arbol_t.html#alfa-beta). Cada página de
>   algoritmo abre la suya en un recuadro como éste.
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
| $\mathrm{Pl}(s)$ | Quién mueve en un estado no final. *Blancas es MAX; Negras es MIN* |
| $A(s)$ | Las jugadas permitidas en $s$. *En n1: $\text{c1}\textbf{-}\text{c2}$ y $\text{c1}\textbf{x}\text{b2}$* |
| $T(s,a)$ | El estado al que lleva la jugada $a$. *Desde n1, $\text{c1}\textbf{-}\text{c2}$ lleva a n2* |
| $U(s)$ | Lo que vale un final **para MAX**; para MIN vale $-U(s)$. *$+1$ si gana Blancas, $-1$ si gana Negras* |
| $V(s)$ | El **valor**: lo que MAX puede asegurar desde $s$ si MIN es racional. En un final, $V(s)=U(s)$. *$V(s_0)=-1$: gana Negras; esta clase lo calcula* |
| $a$ | Una jugada: lo que se hace ahora. *Ej.: $\text{c1}\textbf{-}\text{c2}$* |
| $\operatorname{arg\,max}$ | El **conjunto** de jugadas que alcanzan el máximo; puede tener varias |
:::

Y tres palabras que no son símbolos:

- **Racional:** elige lo mejor **según su utilidad**, con lo que sabe y lo
  que alcanza a calcular. No quiere decir que gane (@jue-c1-racional).
- **Estrategia:** una jugada para **cada** estado donde le toca a un
  jugador, no solo para el actual.
- **Supuestos:** por turnos, sin azar, todo a la vista, toda partida
  termina y lo que gana uno lo pierde el otro.

El problema de la unidad (@jue-c1-problema), escrito completo:

> **Dado:** las reglas del juego, $\bigl(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\
> T,\ U\bigr)$. No el grafo dibujado: las reglas para generarlo.
>
> **Encontrar:** en cada estado $s$ donde le toca a MAX, una jugada
>
> $$a^{∗}\in\operatorname*{arg\,max}_{a\in A(s)} V\bigl(T(s,a)\bigr),$$
>
> es decir, la jugada que lleva al hijo de mayor valor.
>
> **Qué significa:** si MAX juega $a^{∗}$ y sigue eligiendo así en cada
> turno, se asegura al menos $V(s)$ contra cualquier respuesta de MIN, y
> exactamente $V(s)$ si MIN es racional.

Lo único que falta para resolverlo es **cómo se calcula $V$**. Eso es la
primera página.

## Qué vas a poder hacer al terminar esta clase

- Calcular a mano el valor de un árbol pequeño, desde los finales hacia la
  raíz, y separar el valor de la jugada que lo alcanza.
- Decir qué **recibe** y qué **genera** minimax: recibe las reglas
  ($S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$), no el grafo, y genera los
  estados mientras recorre.
- Explicar por qué minimax es correcto, por qué termina y cuánto cuesta.
- Valorar un árbol con nodos de azar y decir cuándo tratar el azar como un
  rival, o a un rival como azar, es un error de modelado.
- Ejecutar alfa-beta a mano, marcar cada corte y decir qué nodos nunca se
  generan.
- Explicar por qué los cortes son seguros y por qué el orden de las jugadas
  decide cuánto ahorra alfa-beta.

## El hilo de la clase

Todo pasa en el subgrafo de **n1**, el que dibujaste en
[[el-juego-como-grafo|El juego como grafo]]: trece estados, numerados en el
orden en que los visita minimax. La utilidad es la de la clase 1, $+1$ si
gana Blancas y $-1$ si gana Negras: aquí no cambia ninguna regla.

## Recorrido

Cinco páginas, en orden, y una tarea de refuerzo al final. Las cuatro de
algoritmos van en pares: primero **a mano**, con números, y después **como
algoritmo**, en general.

::: table {#jue-ruta-2 title="Las páginas de esta clase"}
| | Página | Qué resuelve | Minutos |
|---|---|---|---:|
| 1 | Minimax a mano | Valorar n1 desde los finales y saber quién gana hexapawn | 25m |
| 2 | Minimax como algoritmo | Elegir la jugada con DECIDIR-MINIMAX, paso a paso en el árbol T, y por qué es correcto | 45m |
| 3 | Cuando decide un dado | El problema con azar, en general, y qué cambia si un nodo no lo decide nadie | 30m |
| 4 | Alfa-beta a mano | α, β y la regla de cada corte, en el árbol T que crece, y el recorrido de n1 en orden fijo | 35m |
| 5 | Alfa-beta como algoritmo | DECIDIR-ALFA-BETA línea por línea, por qué los cortes son seguros y por qué el orden importa | 45m |
| 6 | Tarea de refuerzo | Resolver monedas en fila y hexapawn con empate | 45m, aparte |
:::

1. [[minimax|Minimax a mano]]
2. [[minimax-como-algoritmo|Minimax como algoritmo]]
3. [[cuando-decide-un-dado|Cuando decide un dado]]
4. [[alfa-beta|Alfa-beta a mano]]
5. [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]]
6. [[tarea-mirar-todo-y-podar|Tarea de refuerzo]]

## Las animaciones y el notebook

Dos formas de ver correr los algoritmos de esta clase en el árbol T, sin
escribir nada. No se cuentan en el tiempo de la clase y no hay nada que
entregar.

**Las animaciones.** Una página con el árbol, el pseudocódigo con la
línea que corre y el valor de cada variable; avanzas un paso con ▶ o con las
flechas del teclado. Cada página de algoritmo la enlaza en su traza, y aquí
están todas:

- [Minimax](../_assets/traza_arbol_t.html#minimax)
- [Con azar](../_assets/traza_arbol_t.html#azar)
- [Alfa-beta](../_assets/traza_arbol_t.html#alfa-beta)

**El notebook.** El mismo Python de las páginas, instrumentado para que cada
paso muestre la fila de la traza y el árbol dibujado; un deslizador lo
recorre. Cada sección cierra con un «Pruébalo» de una línea.

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

*Se abre en Google Colab, en otra pestaña.*

**Dónde vive.** En este repositorio, en
`course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb`. Colab lo ejecuta en
el navegador sin instalar nada; en tu máquina necesitas `matplotlib` e
`ipywidgets`. Para empezar: «Entorno de ejecución → Ejecutar todas».

**Cuándo.** Después de cada página de algoritmo, su sección: minimax,
expectiminimax y alfa-beta. Las secciones de corte y profundización iterativa
son de la clase 3.

## Qué no cubre esta clase

Aquí el árbol siempre cabe: llegamos a todos los finales. Qué hacer cuando
no se puede, como en el ajedrez, es la clase 3. Tampoco hay jugadas
simultáneas ni juegos donde los dos puedan ganar a la vez: eso es la
clase 4.

Empieza por [[minimax|minimax a mano]].
