# Defectos conocidos

Cada fila es un defecto que se publicó o casi. «Cómo se vio» es el commit que
lo arregló (`git show <hash>` cuenta la historia). Las lentes de
`revision.md` siembran desde aquí. Pruebas en `tools/`, sin el prefijo.

| # | Síntoma | Cómo se vio | Qué no lo vio | Qué lo atrapa hoy |
|---|---|---|---|---|
| 1 | Prosa ≠ número (peor caso 2^(n+1)−1, big-M «ajustada» que no lo era) | `8de1808` tres lentes | pytest, validate | Pruebas que fijan cada cifra en la fuente (`test_juegos.py::test_clase_3_numeros_de_la_prosa`; la prosa no, #39); lente Corrección |
| 2 | Prosa ≠ figura (pie dice «alfa-beta nunca la genera» en página previa; aria-label «fila 9» vs tabla «fila 10») | `b745adf`, `5645d82` | pytest | `test_gen_juegos.py::test_las_figuras_de_alfa_beta_en_t_citan_la_fila_de_la_pagina`; lente Corrección |
| 3 | Hecho falso en prosa: «las hojas… todas son distintas» y la hoja 2 sale dos veces | auditoría, `course/7_juegos/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:210` | todo | Lente Corrección (cotejar cada afirmación con la fuente) |
| 4 | El Python publicado no corría (imports faltantes, `linprog` con lista) | `8de1808` | validate, pytest | `test_pseudocodigo_juegos.py::test_cada_pseudocodigo_trae_su_python_y_define_lo_que_dice` (juegos); fuera de juegos, lente Corrección corre cada bloque |
| 5 | Figura cortada a 1280 («n1…», «no gene…»): SVG de 700 px | `5645d82`, mirando el build | pytest | `test_gen_juegos.py::test_ninguna_figura_pasa_de_600_de_ancho`; lente Render |
| 6 | Textos encimados en figura («el va▮lor», rótulo partido por un trazo) | `9a1ed66`, `75a03db` en Chrome | guarda de ancho, el ojo a tamaño normal | `test_gen_juegos.py::test_ningun_texto_de_leyenda_invade_la_muestra_siguiente`, `test_gen_optimizacion.py::test_ningun_rotulo_de_vertice_queda_partido_por_un_trazo` |
| 7 | SVG a ~300×150 por falta de `width`/`height` | `b8815d2`, Chrome headless | prueba que exigía lo contrario | La guarda de raíz de cada `test_gen_*.py` (p. ej. `test_gen_juegos.py::test_la_raiz_svg_trae_sus_convenciones`) |
| 8 | Fórmula recortada a 390 (casos, cadenas ⟹, PL con rótulos) | `dc313cc`, navegador a 390 | validate; MathJax recorta en su caja | Lente Render; comparar ancho de fórmula vs su caja |
| 9 | Fórmula en línea partida entre «V(s)» y «= max» a 390 | `1ca1043` | todo | Lente Render |
| 10 | Palabras partidas letra a letra en tablas de 4+ columnas | `dc313cc` | validate | Lente Render; `test_contrato_unidad.py` (≤5 columnas, opt-in) |
| 11 | Copias de tiempos que derivan (clase 145m, páginas 155m) | `4d21c13` revisión | — | `test_tiempos_juegos.py` |
| 12 | Tiempos irreales (1042 líneas en 20m) | auditoría, `course/6_optimizacion/5_practica_de_modelado/3_clasificacion_practica.md:7` | — | `lectura.md` (palabras/minuto); `test_contrato_unidad.py` (opt-in) |
| 13 | Notebook derivado del Python de la página | `3f5d99a` 2.ª ronda | — | `test_cuaderno_juegos.py::test_cada_funcion_es_la_de_la_pagina_tal_cual` |
| 14 | Archivo generado sin generador (notebook hecho en el scratchpad) | `25ee9f5` | — | `test_cuaderno_juegos.py::test_el_cuaderno_es_el_que_produce_el_generador` (compara sin escribir) |
| 15 | JSON incrustado en la animación, viejo respecto a la fuente | `c1333e4` diseño | — | `test_traza_web.py::test_el_bloque_incrustado_es_el_que_daria_hoy_pasos_por_linea` |
| 16 | SVG editado a mano: la prueba regenera antes de leer y pasa | `25ee9f5` (cuerpo) | pytest | `git status` limpio tras correr el generador (`verificacion.md`) |
| 17 | Concepto usado antes de presentarlo (código antes de la regla α/β; L, x̄ sin definir) | `4d21c13`, `5a303f4`, `2dac49c` | validate, pytest | Lente Alumno; vocabulario de árbol: `test_aceptacion.py::test_extra_el_vocabulario_de_arbol_no_se_usa_antes_de_presentarlo` |
| 18 | Figura o pie que nombra un algoritmo que viene después | `b745adf` | — | Lente Alumno |
| 19 | Una letra para dos cosas (P nodo y pivotes; k índice y conteo) | `5a303f4`, `0794808` | — | Lente Alumno; `A_notacion.md` |
| 20 | Matemáticas o enlace en un encabezado: «On This Page» imprime la sintaxis | `958fa25`; CLAUDE.md § Authoring contract | validate; pytest entubado a `tail` | `test_aceptacion.py::test_extra_ningun_encabezado_lleva_matematicas` y `::test_extra_ningun_encabezado_lleva_un_enlace_dentro` |
| 21 | Id de objeto numerado repetido en dos páginas: `validate` pasa, solo `build` lo rechaza | `08f92a2` (`jue-c3-ej-final` en p2 y p4) | validate | `test_aceptacion.py::test_extra_ningun_objeto_numerado_repite_id` |
| 22 | Wikilink sin etiqueta imprime el id estable | `758c1bc` | validate | `test_aceptacion.py::test_extra_ningun_wikilink_va_sin_etiqueta` |
| 23 | Wikilink partido por salto de línea, corchetes a la vista | `ed76aa0`, sitio desplegado | validate | `test_aceptacion.py::test_extra_ningun_wikilink_queda_partido_por_un_salto_de_linea` |
| 24 | `\boldsymbol` rompe el build | `6a7fd9b` | validate | `raya build` (compuerta); usar `\mathbf` |
| 25 | Etiquetas en inglés («Definition 3.9.1») | `6579b7a`, HTML generado | validate | `raya.yaml` `numbered_objects`; lente Render |
| 26 | Imagen suelta `![]()` sin «Figura N» | auditoría, `course/6_optimizacion/5_practica_de_modelado/4_regresion_practica.md:46` | validate | `test_contrato_unidad.py` (opt-in) |
| 27 | Animación que salta líneas del pseudocódigo | `86ebcea`, el profesor | — | `test_pasos_por_linea.py::test_a_la_secuencia_de_lineas_es_una_ejecucion_valida` |
| 28 | Panel que muestra el efecto de una línea antes de que corra | `5d6715d`, `e8f7557` | — | `test_pasos_por_linea.py::test_d_ninguna_variable_cambia_sin_que_su_paso_lo_diga` (juegos); lente Corrección |
| 29 | Animación y notebook publicados que nadie encuentra | `1fd4fd8`, `2a9bdbd`, el profesor | — | Callout arriba de cada página (`anatomia.md`); `test_traza_web.py::test_los_enlaces_de_las_paginas_abren_lo_que_prometen` |
| 30 | Asset que ninguna página usa | `fca787a` | — | `test_aceptacion.py::test_5b_toda_imagen_en_assets_esta_referenciada_por_alguna_pagina` (historia), `test_gen_juegos.py::test_ningun_svg_sin_pagina_que_lo_use` |
| 31 | Ejercicio sin pista | auditoría, `course/7_juegos/1_leer_y_escribir/4_diagnosticar_el_juego.md:108` | — | `test_juegos.py::test_cada_ejercicio_de_las_clases_2_y_3_trae_pista_y_respuesta` (solo 2–3); `test_contrato_unidad.py` (opt-in) |
| 32 | «Revisa tu hoja» después de la respuesta | auditoría, `course/7_juegos/1_leer_y_escribir/5_tarea.md:116` (respuesta en :66) | — | Lente Alumno |
| 33 | Pista que filtra el método o la respuesta | `36a13e3` | — | Prueba de fuga (`ejercicios.md`); lente Alumno |
| 34 | Respuesta con borrador dentro y un dato que no existe | `36a13e3` | — | Lente Alumno + Corrección |
| 35 | Pruebas que no muerden: 4 de 15 mutaciones vivas | `2c33b97` | pytest verde | Mutaciones (`revision.md` § Aprender) |
| 36 | Reemplazo de texto que no reemplazó nada y reportó éxito | `c25650d`, `6a7fd9b` | — | Afirmar cada reemplazo; `git diff` antes de reportar |
| 37 | Suite roja que pasa por verde (`pytest … \| tail`) | `958fa25` | — | Leer el código de salida (`verificacion.md`) |
| 38 | Contenido que se mueve o se sale de su tarjeta en la animación | `e62b8db`, recorrido Playwright | — | Lente Render (recorrido a 390 y 1280) |
| 39 | La prueba fija la fuente, no la prosa: una cifra cambiada en la página no rompe nada | auditoría, `tools/test_juegos.py:91` (no lee páginas) | pytest verde | 7.3: `test_juegos.py::test_prosa_clase_3_*` (`d99ef99`, 22 mutaciones muertas); resto del curso: nada (deuda) |
| 40 | Comentario HTML `<!-- … -->` en una página: Raya lo publica como texto (la skill lo pedía para la fila de la tarea) | `a32660a`, lente Render | validate, build | `test_aceptacion.py::test_extra_ninguna_pagina_lleva_un_comentario_html` |
| 41 | Página fragmentada: cada sección correcta, sin hilo; fórmula sin de dónde sale; objeto de dos páginas sin ligar ($c$ en p5, $\delta$ en p6) | el profesor, sitio desplegado, `aclarar-bono-y-mcts` | pytest, validate, 3 rondas de lentes | Lente Alumno § Hilo (`pedagogia.md` § Hilo narrativo) |
| 42 | Gráfica que promedia corridas de todo o nada: 0.85 = 34 en ≈1 y 6 en ≈0; enseña lo contrario | el profesor, `jue-c3-bandido`, `aclarar-bono-y-mcts` | pytest, lentes | Calculista mira la distribución; lente Corrección § 9 (`figuras.md` § Gráficas de datos) |

## Mantenimiento

- **DEBE**: cada defecto nuevo entra aquí **en el mismo commit que lo
  arregla**, con el hash corto en «Cómo se vio» (o `ruta:línea` si es de
  auditoría y sigue abierto).
- **DEBE**: cuando una prueba lo cubre, «Qué lo atrapa hoy» apunta a
  `archivo::prueba`. Una fila que solo atrapa una lente y aparece 2 veces →
  se propone guarda (`revision.md` § Aprender).
- **DEBE**: tope 45 filas (era 40; se subió el 2026-10-12 para no borrar guardas vigentes). Para hacer lugar sale primero la fila cuya guarda
  cubre todo el curso (no solo una unidad) y lleva tiempo sin morder.
