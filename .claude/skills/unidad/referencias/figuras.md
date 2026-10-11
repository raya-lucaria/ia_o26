# Figuras

Abreviaturas: `J2/` = `course/7_juegos/2_mirar_todo_y_podar/`, `B&B` = `course/6_optimizacion/4_entero/4_ramificar_y_acotar.md`.
Cómo se generan, se prueban y se regeneran los SVG: `codigo.md` y CLAUDE.md (secciones de computabilidad y complejidad).
Aquí: qué se dibuja, en qué orden y cómo se nombra.

## Series: el mismo objeto en estados sucesivos

- **DEBE** una traza ilustrada ser una **serie del mismo objeto** (mismo árbol, misma posición de nodos) en estados
  sucesivos, no figuras sueltas con encuadres distintos. Patrón: `jue-t1-ab-1..3` (`J2/4_alfa_beta.md:273`, `:292`, `:304`);
  `opt-ent-arbol-paso-0..4` (`B&B:267`, `:285`, `:310`, `:342`, `:365`).
- **DEBE** elegir cada instantánea por **EVENTO** (la raíz se actualiza, un corte, el fin), no por conteo de filas.
  El generador la busca con un predicado sobre la traza, no con un número fijo: `_pasos_ab_t` toma
  `f["corta"] == "beta"`, `f["corta"] == "alfa"` y la última fila (`tools/gen_juegos.py:1790–1795`).
- **DEBE** ir de **parciales a resuelta**: primero los pasos, al final la vista completa y su tabla resumen
  (`B&B:401` figura del árbol completo, `B&B:409` tabla con una fila por nodo; `J2/4_alfa_beta.md:481` tras `:460` y `:464`).
- **DEBERÍA** abrir la serie con la **tabla de estados** que la figura usa, si los nodos cambian de estado
  (`B&B:259`: POR RESOLVER, SIGUIENTE, PENDIENTE, DIVIDIDO, CERRADO).
- **CRITERIO** 3–5 instantáneas por traza; más, solo si cada una tiene su evento propio.

## Orden en la página: tabla → viñetas → figura

- **DEBE** cada tramo ir en el orden **tabla de la traza → viñetas que citan filas** («**Fila 5:** …») **→ figura**
  del estado al cerrar el tramo. Patrón: `J2/2_minimax_como_algoritmo.md:234` (tabla), `:242` (viñetas), `:248` (figura).
- Contraejemplos: `J2/4_alfa_beta.md:265–280` pone la figura antes de las viñetas; `J2/5_alfa_beta_como_algoritmo.md:306–330`
  apila tres figuras y luego las viñetas, sin tabla.

## Títulos y vocabulario

- **DEBE** el `title` nombrar **el evento**, no el número de figura: «T, fila 12: el corte beta en C2» (`J2/4_alfa_beta.md:375`),
  «Guardamos 20 y queda un subproblema por resolver» (`B&B:365`). Nunca solo «Paso 3».
- **DEBE** usar «fila N» **solo si la tabla de la página numera filas** (columna `#`, `J2/4_alfa_beta.md:265`); el número es
  el de la página, no el de la traza interna (`tools/test_gen_juegos.py::test_las_figuras_de_alfa_beta_en_t_citan_la_fila_de_la_pagina`).
- **DEBE** haber **un vocabulario por página** para las partes de una serie (fila, o tramo, o paso), el mismo en `title`,
  `alt` y texto dentro del SVG. Contraejemplos: `J2/4_alfa_beta.md` usa «fila» (`:273`) y «parte» (`:460`); el SVG de
  `jue-t-ab-*` dice «paso N» (`tools/gen_juegos.py:1801`) bajo un título que dice «fila».

## Leyenda y señales

- **DEBE** haber **una sola leyenda por unidad**, en `A_notacion.md` § «En las figuras» (`course/7_juegos/A_notacion.md:156–166`).
  Una marca nueva entra ahí antes de usarse; ninguna figura redefine una marca.
- **DEBE** el color **nunca ser la única señal**: cada distinción lleva forma, trazo o texto además del color. Patrón: el
  nodo dice «MAX»/«MIN» y no solo su color (`tools/gen_juegos.py:146–148`); final = borde doble, sin expandir = punteado,
  nunca generado = caja punteada con «?» (`A_notacion.md:160–165`).
- **DEBE** el **borde grueso de acento** marcar **lo nuevo de ese paso** y nada más (`A_notacion.md:162`;
  `nodo_svg(nuevo=True)`, `tools/gen_juegos.py:173`). Colores por rol desde constantes (`tools/gen_juegos.py:27–29`).

## Directiva y composición

- **DEBE** toda imagen ir en `::: figure {#id title="…"}` (ver `lectura.md`); el `id` lleva el **prefijo de la unidad**
  y es único en el curso (`jue-c2-…`, `opt-ent-…`; ver CLAUDE.md § Authoring contract).
- **DEBE** los *small multiples* (varios estados que se comparan lado a lado) ser **una figura compuesta**, no varias
  figuras: «Una vuelta de MCTS, en cuatro pasos» (`course/7_juegos/3_cuando_no_cabe/4_simular_en_vez_de_evaluar.md:163`),
  «Profundizar mientras haya tiempo» (`course/7_juegos/3_cuando_no_cabe/3_jugar_contra_el_reloj.md:200`).

## Figuras generadas

- **DEBE** medir ≤600 px de ancho (`tools/gen_juegos.py:78–88`; `tools/test_gen_juegos.py::test_ninguna_figura_pasa_de_600_de_ancho`).
- **DEBE** el `aria-label` del SVG y el `alt` de la página **nombrar el estado y los valores** que se ven («I muestra v = 3…
  mejor_jugada = izq y mejor_valor = 3», `J2/2_minimax_como_algoritmo.md:249`), coherentes con el texto
  (`tools/test_gen_juegos.py::test_ningun_aria_label_deja_una_frase_vacia`).
- **DEBE** llevar el fondo del skin horneado (`FONDO = "#211033"`, `tools/gen_optimizacion.py:28`; `tools/test_skin.py`).
- **DEBE** revisarse **renderizada en Chrome headless, nunca con ImageMagick** (pierde flechas y subíndices; comando en
  CLAUDE.md, sección de computabilidad y complejidad), a 390 y a 1280 px.

## Excepciones

- **Concepto a mano** sin tabla de traza: la serie va figura → viñetas («Paso 1: valorar n6»,
  `J2/1_minimax.md:175`); el título sigue nombrando el evento.
- **Figura única de problema** (el objeto antes de empezar): no es evento, se titula por el objeto
  («El árbol T: el problema», `J2/2_minimax_como_algoritmo.md:212`).
- **Cronología y lectura:** líneas del tiempo y genealogías son figuras únicas, sin serie ni tabla previa
  (`course/1_introduccion/2_historia_ia/3_arco_historico.md:14`).
