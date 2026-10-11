# Anatomía: página, bloques por tipo e índices

Abreviaturas de ruta: `J2/` = `course/7_juegos/2_mirar_todo_y_podar/`, `J1/` = `course/7_juegos/1_leer_y_escribir/`,
`M/` = `course/6_optimizacion/5_practica_de_modelado/`. Frontmatter, ids, wikilinks y directivas: CLAUDE.md § Authoring contract.

## Núcleo común de toda página de contenido
1. **DEBE** abrir con la **pregunta guía en negrita** tras el `#` (`J2/2_minimax_como_algoritmo.md:13`).
2. **DEBE** seguir «Al terminar tendrás:» con ≤5 viñetas, cada una un resultado verificable (`J2/2_minimax_como_algoritmo.md:16`).
3. **DEBERÍA** llevar tarjetas `>` opcionales: «Lo que traes de [[id|…]]» (`J2/4_alfa_beta.md:25`), «Supuestos de esta página»
   (`J2/2_minimax_como_algoritmo.md:30`), reglas del hilo en cuatro líneas (`J2/2_minimax_como_algoritmo.md:23`).
4. **DEBE** numerar el cuerpo `## N · Verbo + objeto` (`J2/2_minimax_como_algoritmo.md:49`); sin matemáticas ni enlaces en
   encabezados (`tools/test_aceptacion.py::test_extra_ningun_encabezado_lleva_matematicas`, `…_lleva_un_enlace_dentro`).
5. **DEBERÍA** abrir cada `##` explicativo con `**Piensa: …?**` respondido en el párrafo siguiente (`J2/2_minimax_como_algoritmo.md:51`).
6. **CRITERIO** el material opcional va en `## Para profundizar` con `###` (`J2/2_minimax_como_algoritmo.md:583`).
7. **DEBE** cerrar con «## Lo que hay que llevarse» que **repite las cifras clave** (nodos, valores, líneas)
   (`J2/4_alfa_beta.md:595`: «12 de 14… 11… 5 de 13»), y luego `Continúa con [[id|…]].` (`J2/2_minimax_como_algoritmo.md:686`).
8. **DEBE** el error típico de lectura ir en `> [!WARNING]`, con la lectura correcta en negrita (`course/4_complejidad/2_o_grande.md:54`).

## Bloques por tipo de página

**Concepto a mano** (`J2/1_minimax.md`)
- **DEBE** cada concepto nuevo en `::: definition`: qué es y cómo se calcula (`J2/1_minimax.md:90`, `:96`); «Qué no es» solo si hay
  un confusor real (`pedagogia.md` § Error típico; `J2/1_minimax.md:115`).
- **DEBERÍA** avanzar el ejemplo hilo en pasos con una tabla acumulada «El juego hasta ahora · k de 7» (`J1/2_escribir_el_juego.md:203`).

**Algoritmo** (`J2/2_minimax_como_algoritmo.md`, `J2/5_alfa_beta_como_algoritmo.md`)
- **DEBE** plantear el problema como cita `> **Dado:** … **Encontrar:** …` con referencias `@id` a cada pieza (`:59`).
- **DEBE** dar pseudocódigo en ` ```text ` con cabecera `INPUT/OUTPUT`, líneas numeradas y comentarios `#` compactos al
  margen o en su renglón (`:100–131`); máx. ~54 columnas.
- **DEBE** seguir un **gemelo Python** completo con `# (n)` = línea del pseudocódigo (`:136–175`); lo ejecutan
  `tools/test_pseudocodigo_juegos.py::test_cada_pseudocodigo_trae_su_python_y_define_lo_que_dice` y `…caben_en_un_telefono` (≤64 col).
- **DEBERÍA** mapear «Cada pieza del modelo, en su línea» (`:177`) y escribir los cambios como delta de líneas
  («La línea 9 es la nueva», `course/7_juegos/3_cuando_no_cabe/2_minimax_con_corte.md:168`).
- **DEBE** trazar en **tramos** `### Tramo k · evento` con tabla + viñetas + figura (`:232–250`); ver `figuras.md`.
- **DEBE** incluir corrección (`:448`), terminación y costo en `::: remark` (`:622`, `:639`).
- **DEBE** poner el cuadro `> [!TIP] **Míralo correr: …**` **solo si existen** animación y/o notebook: enlace a la
  animación con `#ancla` y badge Colab con la sección (`:39–47`). Sin ellos, no hay cuadro; ver `codigo.md`.

**Modelado** (`M/1_salones_practica.md`)
- **DEBE** seguir el orden relato con datos precisos y simplificación explícita (`:20`, `:31`) → representar con cada
  símbolo y su papel: dato / decisión / expresión calculada / auxiliar (`:43`, `:251–267`, `:332`; tabla «Signo | Papel»,
  `M/3_clasificacion_practica.md:1019`) → modelo general (`:155`) → **modelo otra vez** como resumen (`:222`).
- **DEBERÍA** auditar el objetivo con **dos objetivos** sobre el mismo $F$ y un caso donde discrepan (`:193–215`).
- **DEBE** cerrar con tipo (`:292`) → método → costo contando candidatos × costo de revisar cada uno (`:348–357`).

**Lectura / ideas** (`course/2_filosofia_ia/1_aceleracionismo/1_las_ideas.md`)
- **DEBE** declarar minutos por sección en el `##` (`:29`, «· ~3 min») y en la entrada (`:15–17`).
- **DEBE** cada cita textual llevar `— cuadernillo, p. N` y su fila en el registro (`:108`;
  `tools/test_repaso.py::test_toda_cita_de_la_pagina_esta_en_el_registro`).

**Cronología** (`course/1_introduccion/2_historia_ia/3_arco_historico.md`)
- **DEBE** abrir con la línea del tiempo en figura (`:14`) y encabezados `## Año · Hecho` (`:53`); fechas desde
  `tools/hitos.json` y verificadas (`tools/test_aceptacion.py::test_7_toda_fecha_y_atribucion_tiene_fuente_verificada`).

## Índice de unidad (`course/7_juegos/0_index.md`)

**DEBE**, en orden: pregunta/tesis en negrita (`:13`) → por qué en un curso de IA (`:22`) → el hilo de la unidad (`:35`)
y «Cada clase cambia una sola cosa» con tabla qué cambia / herramienta (`:46`) → `::: table` de clases con minutos (`:58`)
→ total en prosa (`:72`) → hoja de notación (`:109`) → `Empieza por [[id|…]].` (`:112`).

## Índice de clase (`J2/0_index.md`)

**DEBE**, en orden: pregunta de repaso en negrita (`:13`) → TIP de animaciones/notebook si existen (`:23`) →
«Lo que traes» en `::: table` ≤12 filas con enlace a su definición (`:32`) → «Qué vas a poder hacer» (`:80`) →
«El hilo de la clase» (`:95`) → «Recorrido» con `::: table` de páginas y minutos + lista numerada de wikilinks (`:102–124`)
→ «Las animaciones y el notebook» si hay (`:126`) → «Qué no cubre» (`:158`) → `Empieza por` (`:165`).
- **DEBE** la tarea ser fila «aparte» **sin wikilink** y sin entrada en la lista, con el comentario
  `<!-- TAREA: la dispara el usuario -->` junto a la fila. (`J2/0_index.md:116` y `:124` son el formato viejo, con enlace.)
- **DEBE** la última página de contenido de la clase continuar al siguiente índice de clase, no a la tarea.

## Convenciones de notación del repo
- **DEBE** jugadas como $\text{c1}\textbf{-}\text{c2}$ y $\text{c1}\textbf{x}\text{b2}$ (`J2/0_index.md:46`); jugador de turno
  $\mathrm{Pl}$, nunca $P$ (`tools/test_juegos.py::test_la_unidad_escribe_pl_y_no_p`); óptimo con ∗ unicode, $a^{∗}$
  (`J2/2_minimax_como_algoritmo.md:68`); `\mathbf`, nunca `\boldsymbol` (el renderizador lo rechaza; CLAUDE.md § Authoring contract).
- **DEBE** cada símbolo nuevo aparecer en `A_notacion.md` de la unidad (`course/7_juegos/A_notacion.md:23–102`).

## Excepciones
- Página de cronología o de lectura: sin `## N ·` numerado ni Piensa por sección (`3_arco_historico.md:53`).
- Página de modelado: puede abrir con el relato y llevar las dos preguntas guía en negrita dentro (`M/1_salones_practica.md:13–15`).
- Una unidad sin algoritmo ejecutable no lleva TIP, animación ni notebook (decisión de G2).
