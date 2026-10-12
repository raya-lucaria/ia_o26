# Código que acompaña

Cadena: **fuente → generadores → (notebook, animación) → pruebas**. Comandos y orden de corrida: `verificacion.md`. Generadores existentes y qué produce cada uno: `tools/README.md` § Generadores.

## 0 · ¿Hay algo ejecutable? (se decide en G2)

| La unidad tiene… | Se crea |
|---|---|
| cálculo o algoritmo cuyos números cita la prosa | `tools/<unidad>.py` + `test_<unidad>.py` |
| diagramas propios | `tools/gen_<unidad>.py` con catálogo `DIAGRAMAS` + su prueba |
| algoritmo que el alumno puede correr | notebook generado + badge Colab |
| algoritmo con traza paso a paso | animación (patrón de § 5) |
| solo lectura, concepto o cronología | **nada de lo anterior** |

- **DEBE**: si no hay cálculo, no se inventa un `<unidad>.py` ni un notebook. Filosofía no tiene código; complejidad solo generador (`tools/gen_complejidad.py:1826`).

## 1 · Fuente única de los números

- **DEBE**: todo número que cite una página (prosa, tabla, figura, pie) sale de una función de `tools/<unidad>.py`, y una aserción de `test_<unidad>.py` lo fija con el valor escrito en la prosa (`tools/juegos.py:1`, `tools/test_juegos.py:19`). Cambiar una regla sin tocar la prosa tiene que romper la suite.
- **DEBE**: esa prueba busca la cifra **en el texto de la página**, además de en la fuente: cambiar la prosa sin tocar la regla también tiene que romperla. Contraejemplo: `tools/test_juegos.py:91` se llama «números de la prosa» y no lee ninguna página (`defectos.md` #39).
- **DEBE**: nada se copia a mano: figuras, notebook y animación leen de la fuente o de la página.
- **DEBE**: los datos de tarea **no** entran a la fuente nueva (las tareas quedan fuera de alcance; ver SKILL.md).
- **DEBE**: el bloque ```python de cada página corre y decide lo que la página dice: se extrae y se ejecuta (`tools/test_pseudocodigo_juegos.py:99`).
- **DEBERÍA**: aritmética exacta (`Fraction`) si la prosa cita fracciones (`tools/juegos.py:20`).
- **CRITERIO**: una función por hecho citado, nombrada por lo que la prosa afirma (`contar_arbol`, `partida_mas_larga` en `tools/test_juegos.py:20`).

## 2 · Generadores de figuras

- **DEBE**: `gen_<unidad>.py` con paleta en constantes, una función por diagrama, catálogo `DIAGRAMAS` compartido con su prueba y prefijo de id propio (`tools/gen_juegos.py:2807`). Convenciones del SVG: CLAUDE.md § Computabilidad y complejidad.
- **DEBE**: lo dibujado se calcula con la fuente y una prueba lo coteja (`tools/test_gen_juegos.py:105`).
- **DEBE**: tras correrlo, `git status` limpio: `scripts/generadores_limpios.sh`.

## 3 · Dos clases de prueba

| Clase | Ejemplo | Si alguien edita el archivo a mano |
|---|---|---|
| regenera y revisa forma | fixture `tools/test_gen_juegos.py:24` | se sobrescribe callado y pasa |
| compara sin escribir | `tools/test_traza_web.py:51`, `tools/test_cuaderno_juegos.py:106` | **falla** con «corre el generador» |

- **DEBERÍA**: todo generador nuevo expone una función pura (`contenido()`, `serializar()`) y su prueba compara bytes contra el archivo comiteado sin escribir. La primera clase solo para catálogos heredados.

## 4 · Notebook (solo si hay algoritmo ejecutable)

- **DEBE**: se genera desde el Python de las páginas, nunca se edita el `.ipynb`: extraer el bloque (`tools/gen_cuaderno_juegos.py:53`) y solo agregar instrumentación (`:115`). La prueba exige la función tal cual (`tools/test_cuaderno_juegos.py:187`) y lógica solo con biblioteca estándar (`:196`).
- **DEBE**: secciones = páginas, en orden de navegación; preparación en celdas plegadas (`tools/test_cuaderno_juegos.py:144`); sin salidas (`:113`); celdas ≤ 15 líneas, ≤ 36 la de algoritmo, ≤ 79 columnas (`:44`, `:131`).
- **DEBE**: cada sección cierra con **Pruébalo**: un cambio de un número, la respuesta en `<details>` y una celda corta (`tools/gen_cuaderno_juegos.py:580`).
- **DEBE**: badge «Abrir en Colab» en la primera celda (`tools/gen_cuaderno_juegos.py:142`, prueba `tools/test_cuaderno_juegos.py:123`) con URL `https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/<ruta del .ipynb>`.
- **DEBE**: el mismo badge en el cuadro «Míralo correr» de **cada página cuyo Python entra al notebook**, nombrando su sección (`course/7_juegos/2_mirar_todo_y_podar/2_minimax_como_algoritmo.md:40`). En ninguna otra.
- **DEBE**: la URL apunta a `main`: solo funciona tras el merge y se comprueba en vivo (compuerta 8, `scripts/en_vivo.sh`). Colab responde 200 aunque el archivo no exista.

## 5 · Animación (solo algoritmos): un patrón, no un generador genérico

`tools/gen_traza_web.py` sirve solo a `juegos.pasos_por_linea`. Se copia el patrón:

- **DEBE**: HTML escrito a mano cuyo JS solo pinta; los datos van incrustados entre marcadores (`tools/gen_traza_web.py:73`) y el generador reemplaza solo ese bloque, idempotente (`tools/test_traza_web.py:97`).
- **DEBE**: `compactar`/`expandir` sin pérdida (`tools/gen_traza_web.py:102`, `:153`; prueba `tools/test_traza_web.py:59`).
- **DEBE**: < 150 KB (`tools/test_traza_web.py:86`), sin recursos externos (`:79`), `:root` con la paleta del skin, `lang` y `<title>` (`:91`).
- **DEBE**: fragmentos `#<modo>-fila-N` (cierra la fila N de la tabla) y `#<modo>-paso-K`; las páginas enlazan por fila y una prueba abre cada enlace (`tools/test_traza_web.py:141`).
- **DEBE**: un paso por línea ejecutada, atado por una prueba de flujo con grafo de control escrito a mano (`tools/test_pasos_por_linea.py:40`, `:93`) y ninguna variable que cambie sin que su paso lo diga (`:323`).

## 6 · Prohibido sin permiso explícito del usuario

- **DEBE**: no editar a mano `_assets/` generados (SVG, `.ipynb`, bloque JSON), ni nada en `artifact/`; no correr `tools/gen_ilustraciones.py` (cuesta dinero; CLAUDE.md § The pytest suite guards content).

## Excepciones

- Historia usa JSON como fuente (`tools/hitos.json`, `tools/computo.json`): vale si una prueba lo ata igual.
- Los cuatro notebooks de `course/6_optimizacion/_assets/` no tienen generador: heredados; no se retrofitan salvo que la auditoría lo ponga en el plan.
- `tools/test_juegos.py:32` fija números de una tarea: heredado, solo lectura.
- Complejidad y computabilidad usan la clase «regenera»: no se migran de paso.
- **DEBE** en las páginas HTML de `_assets/`, nada de `text-transform` sobre texto con símbolos: convierte
  N(s) en N(S) y x en X, que el curso no tiene (`hoeffding_en_vivo.html`, `bandido_en_vivo.html`, `cd58ed7`).
