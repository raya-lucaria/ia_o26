# Originales archivados de la unidad 7

Esta carpeta no se publica. Guarda, **byte por byte**, las páginas que la
homologación de la unidad 7 (rama `homologar-unidad-7`, octubre de 2026)
fundió en otras, para que nada útil se pierda y se pueda comparar.

**Por qué `.md.txt` y no `.md`.** La guarda
`test_extra_ningun_objeto_numerado_repite_id` recorre también `_drafts/`.
Muchos ids de estos originales viven hoy en páginas publicadas; como `.md`
chocarían con ellos. Como texto no los lee ninguna guarda ni el builder.

**Dónde está la versión de antes.** Todas las rutas con línea de este
archivo son del tag `antes-homologacion-unidad-7`. Para ver una pieza:
`git show antes-homologacion-unidad-7:<ruta>`.

Lo que salió del sitio sin fundirse en otra página no está aquí: la clase 4
anterior, «Cuando no hay turnos», vive como borrador `.md` en
`course/7_juegos/_drafts/4_sin_turnos/`, con sus ids `jue-c4-*` y
`jue-ruta-sin-turnos` reservados.

---

## Qué contiene cada archivo

| Archivo | Era | Adónde fue su contenido |
|---|---|---|
| `3_cuando_no_cabe__2_minimax_con_corte.md.txt` | Página «Minimax con corte» de la clase 3 | Se concatenó a «Cortar y evaluar» (`3_cuando_no_cabe/1_cortar_y_evaluar.md`), que conserva su id como alias, `minimax-con-corte` |
| `3_cuando_no_cabe__3_mas_alla_del_horizonte.md.txt` | Página «Más allá del horizonte» | Se fundió con «Jugar contra el reloj» en «Hasta dónde mirar» (`3_cuando_no_cabe/2_jugar_contra_el_reloj.md`), con alias `mas-alla-del-horizonte` |
| `3_cuando_no_cabe__5_simular_en_vez_de_evaluar.md.txt` | «Simular en vez de evaluar», con Monte Carlo plano y la primera presentación de MCTS | Monte Carlo plano, a «Simular partidas» (`3_simular_en_vez_de_evaluar.md`); MCTS, a «MCTS con UCT» (`4_monte_carlo_en_un_arbol_grande.md`) |
| `3_cuando_no_cabe__7_monte_carlo_en_un_arbol_grande.md.txt` | «Monte Carlo y UCT en un árbol grande» | La refutación, el crecimiento desigual y la mezcla, a «MCTS con UCT»; el árbol y Monte Carlo plano, a «Simular partidas» |
| `3_cuando_no_cabe__8_de_donde_sale_el_bono.md.txt` | «De dónde sale el bono», en siete secciones | Reorganizada en los seis bloques de `5_de_donde_sale_el_bono.md`; «Seleccionar no es entregar» pasó a «MCTS con UCT» |
| `3_cuando_no_cabe__borrador_7_un_arbol_todos_los_algoritmos.md.txt` | Borrador sin publicar de la comparación | Sus recorridos de UCT y la tabla de «dos filas que dicen 0» se rescataron en «MCTS con UCT»; lo demás lo cubren la radiografía y las páginas a detalle |
| `3_cuando_no_cabe__borrador_8_que_numero_da_cada_uno.md.txt` | Borrador sin publicar, «Qué número da cada uno» | Lo cubren la radiografía (`4_radiografia/1_un_arbol_todos_los_algoritmos.md`) y «Elegir el algoritmo» |

---

## Piezas archivadas y por qué

Ninguno de estos ids se reutiliza en una página publicada, ni con otro
significado.

**La tabla de adelanto de la clase 1.**

- `jue-c1-recibe-genera`, en
  `course/7_juegos/1_leer_y_escribir/3_el_juego_como_grafo.md:214`. Decía qué
  recibe y qué genera cada método antes de verlos, y contradecía lo que hoy
  muestra la radiografía. La idea de que una búsqueda recibe las reglas, no
  el grafo, se quedó en «El juego como grafo».

**Las fichas de siete rasgos.** Las reemplazan el mapa y las propiedades de
cada algoritmo (número que da, si usa EVAL, garantía, si se puede
interrumpir, complejidad, frente a los demás y supuestos).

- `jue-ficha-minimax`, en
  `course/7_juegos/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:678`.
- `jue-ficha-expectiminimax`, en
  `course/7_juegos/2_mirar_todo_y_podar/3_cuando_decide_un_dado.md:504`.
- `jue-ficha-alfa-beta`, en
  `course/7_juegos/2_mirar_todo_y_podar/5_alfa_beta_como_algoritmo.md:568`.
- `jue-ficha-corte`, en `course/7_juegos/3_cuando_no_cabe/2_minimax_con_corte.md:723`.
- `jue-ficha-quietud`, en
  `course/7_juegos/3_cuando_no_cabe/3_mas_alla_del_horizonte.md:367`.
- `jue-ficha-iterativa`, en
  `course/7_juegos/3_cuando_no_cabe/4_jugar_contra_el_reloj.md:894`.
- `jue-ficha-mc-plano` y `jue-ficha-uct`, en
  `course/7_juegos/3_cuando_no_cabe/5_simular_en_vez_de_evaluar.md:497` y `:511`.

**Copias de una misma tabla.**

- `jue-c3-posicion-corte` (`course/7_juegos/3_cuando_no_cabe/2_minimax_con_corte.md:86`) y
  `jue-c3-posicion-reloj` (`course/7_juegos/3_cuando_no_cabe/4_jugar_contra_el_reloj.md:59`): eran la cuarta y
  la tercera copia de la posición de la clase. Quedan `jue-c3-posicion`, en
  «Cortar y evaluar», y `jue-c3-posicion-horizonte`, en «Hasta dónde mirar».
- `jue-c3-reloj-por-d` (`course/7_juegos/3_cuando_no_cabe/4_jugar_contra_el_reloj.md:104`): la misma tabla que
  `jue-c3-horizonte-valores`, transpuesta.
- `jue-c3-t-sin-poda` (`course/7_juegos/3_cuando_no_cabe/4_jugar_contra_el_reloj.md:257`): los mismos números
  que `jue-c3-t-por-profundidad`, en «Cortar y evaluar».

**Ejercicios del bono que repetían cuentas.** Cada uno se archiva con su
pista y su respuesta. La auditoría de la clase 3 los marcó porque duplican
cuentas o contenido que la página ya hace.

- `jue-c3-ej-optimismo` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:346`): repetía el
  cálculo de la cota optimista que el bloque 3 hace con la corrida de cinco
  vueltas.
- `jue-c3-ej-teoria` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:481`): recalculaba los
  puntajes de MCTS con la $c$ de la teoría; la tabla de $c$ y $\delta$ ya lo
  muestra.
- `jue-c3-ej-vuelta-seis` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:521`): seguía una
  vuelta más de la corrida sembrada que el bloque 3 ya traza.
- `jue-c3-ej-entregar` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:693`): «seleccionar no
  es entregar». La tabla `jue-c3-tabla-seleccionar` pasó a «MCTS con UCT».
  La frase «la más visitada es la que la búsqueda confirmó más veces» pasó
  con ella y luego se reescribió, porque las visitas también cuentan la
  expansión y la exploración por el bono: hoy dice que entregar la más
  visitada es la regla de esta versión y que «las visitas no son pruebas de
  que una jugada sea mejor». La pregunta sobre seleccionar frente a entregar la retoma el
  ejercicio 3 de la tarea de la clase 3.

**Tres figuras del bono que decían lo mismo.** Se quitaron el SVG, su
entrada en el catálogo de `tools/gen_juegos.py` y su fila de créditos; las
funciones de `tools/juegos.py` que daban sus cifras se quedan, porque
alimentan las tablas.

- `jue-c3-fig-bandido-corridas` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:577`): su
  conclusión, 34, 5 y 1 corridas atoradas contra 40, 0 y 0, y el 85 %, vive
  en `jue-c3-tabla-corridas`.
- `jue-c3-fig-pago` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:594`): los pagos finales
  0.543, 0.564, 0.580 y 0.598 contra 0.6, y el 0.5425 esperado, viven en
  `jue-c3-tabla-pagos-finales`.
- `jue-c3-fig-eligiendo-x` (`course/7_juegos/3_cuando_no_cabe/8_de_donde_sale_el_bono.md:630`): el 93.3 % de
  «a veces al azar» vive en el bloque de elegir $c$.

**Piezas de los borradores de comparación.**

- `jue-c3-cmp-arbol`, `jue-c3-cmp-ej-poda` y `jue-c3-cmp-ej-reloj` (con sus
  pistas y respuestas), en
  `course/7_juegos/3_cuando_no_cabe/_drafts/7_un_arbol_todos_los_algoritmos.md:71`,
  `:98` y `:214` del tag; aquí, en
  `3_cuando_no_cabe__borrador_7_un_arbol_todos_los_algoritmos.md.txt`, mismas
  líneas. Los cubren la radiografía, «Alfa-beta como algoritmo» y «Hasta dónde
  mirar».
- `jue-c3-cmp-num-arbol`, en
  `course/7_juegos/3_cuando_no_cabe/_drafts/8_que_numero_da_cada_uno.md:36` del
  tag; aquí, en `3_cuando_no_cabe__borrador_8_que_numero_da_cada_uno.md.txt`,
  misma línea: otra figura del mismo árbol.

**Páginas cuyo id dejó de ser de una página.**

- `minimax-con-corte` y `mas-alla-del-horizonte` viven como **alias** de
  «Cortar y evaluar» y «Hasta dónde mirar». Sirven para enlaces internos,
  pero sus URL viejas ya no existen: Raya no redirige.
- `que-numero-da-cada-uno` era el borrador 8; se archiva entero.
