# Contrato de lectura

Abreviaturas: `J2/` = `course/7_juegos/2_mirar_todo_y_podar/`, `M/` = `course/6_optimizacion/5_practica_de_modelado/`.
Lo medible lo mide `tools/contrato_unidad.py` (guarda opt-in: la unidad entra en `UNIDADES_CONTRATO` de
`tools/test_contrato_unidad.py`). **Mide exactamente las métricas de la tabla de abajo, ni una más.** Si el script y esta
hoja difieren en cómo cuenta (qué es frase, qué es párrafo), manda el script y se corrige esta hoja.
Lo que no se puede medir (definir, ordenar, repetir) lo revisa la **lente del alumno** (`prompts/`, `revision.md`).

## Umbrales medibles (DEBE)

| Métrica | Tope | Cómo se cuenta |
|---|---|---|
| Frase, percentil 90 | ≤22 palabras | Prosa de la página, sin código, fórmulas display ni tablas |
| Frase más larga | ≤40 palabras | Igual |
| Negrita media | ≤1.2 por párrafo | Tramos `**…**` / párrafos de prosa |
| Negrita en un párrafo | ≤3 | Igual |
| Párrafo | ≤70 palabras | Bloque de prosa entre líneas en blanco |
| Columnas de tabla | ≤5 | Celdas de la fila de encabezado |
| Palabras por minuto | ≤90 algoritmo y modelado; ≤150 lectura | Palabras de la página **sin** `::: answer` ni `::: hint`, entre su `estimated_time` |
| Suma de minutos | página = fila de su clase; clase = Σ páginas sin filas «aparte»; unidad = Σ clases | `estimated_time`, tabla de recorrido, `::: table` de clases y total en prosa |
| Imágenes | 0 fuera de `::: figure` | Todo `![…](…)` debe estar dentro de un bloque figure |

- La suma de minutos ya la vigila, solo para juegos, `tools/test_tiempos_juegos.py`
  (`::test_la_clase_dura_la_suma_de_sus_paginas_sin_la_tarea`, `::test_la_unidad_dura_la_suma_de_sus_clases_en_el_frontmatter_y_en_la_prosa`);
  `contrato_unidad.py` la generaliza. Una página nueva entra con su `estimated_time` y su fila en el mismo commit.
- Tipos sin tope propio (concepto a mano, cronología): **DEBE** usar el de algoritmo (≤90) salvo decisión registrada en G2.
- Contraejemplos reales: `M/3_clasificacion_practica.md` declara `20m` (`:7`) para 1042 líneas, muy por encima de 90 pal/min;
  `M/4_regresion_practica.md:46` es un `![…]` suelto, sin «Figura N» (19 así en `M/`).
- Referencia que cumple el ritmo: `J2/2_minimax_como_algoritmo.md`, tramos de tabla de 5 columnas (`:234`).

## Lo que revisa la lente del alumno

- **DEBE** definir todo término **la primera vez que se usa**, antes o en la misma frase, no después. Patrón: «Cómo leer la
  traza» define cada columna antes de la tabla (`J2/2_minimax_como_algoritmo.md:218–230`); tarjeta de vocabulario prestado
  (`course/7_juegos/1_leer_y_escribir/2_escribir_el_juego.md:191`). La guarda
  `tools/test_aceptacion.py::test_extra_el_vocabulario_de_arbol_no_se_usa_antes_de_presentarlo` cubre un caso; el resto, a ojo.
- **DEBERÍA** pasar a lista lo que es enumeración, a tabla lo que tiene dos ejes y a diagrama lo que tiene forma
  («Cada pieza del modelo, en su línea», `J2/2_minimax_como_algoritmo.md:177`).
- **DEBERÍA** repetir cuando ahorra un salto atrás: reglas del hilo en cuatro líneas en cada página
  (`J2/2_minimax_como_algoritmo.md:23`), cifras clave en «Lo que hay que llevarse» (`J2/4_alfa_beta.md:595`).
- **CRITERIO** una idea por frase; la negrita marca la idea que hay que llevarse del párrafo, no términos sueltos.
- **CRITERIO** ningún símbolo sin leerse en palabras la primera vez («$v$ es lo mejor que ha visto **este** nodo»,
  `J2/2_minimax_como_algoritmo.md:95`).

## Excepciones

- **Trazas:** hasta 7 columnas. El script las reconoce por su primera columna `#` o por un `::: table` con «traza» en id o
  título. **DEBERÍA** ir en `::: table {#id title="…"}` (numera y se cita), y **DEBE** tener el scroll horizontal
  **probado a 390 px** (`verificacion.md` § 5). `J2/4_alfa_beta.md:265` pasa el script pero va en tabla suelta.
- **«Lo que traes» y «Lo que hay que llevarse»** no cuentan para ningún tope (repetición útil): ni frases, ni negrita, ni
  palabras por minuto.
- **`**Piensa: …?**`**, uno por `##` explicativo, no cuenta para la negrita media ni para el tope por párrafo.
- Una página >20 % sobre su tope de palabras por minuto no se recorta a ciegas: en `unidad` es disparador de pregunta
  (SKILL.md); en `unidad-auditar` es hallazgo **media** con la cifra (pal/min contra tope).
