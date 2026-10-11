# Revisión adversarial

Las lentes buscan **romper** la unidad, no aprobarla (casi nada de `defectos.md` lo vio `raya validate`).

## Tres lentes, en paralelo, sin contexto previo

| Lente | Recibe | Hace | Plantilla |
|---|---|---|---|
| Corrección | páginas, fuente Python, generadores, pruebas | recalcula, corre cada bloque, coteja prosa ↔ figura ↔ fuente | `prompts/lente-correccion.md` |
| Alumno | páginas en orden de navegación, nada más | orden, carga, definiciones, ejercicios | `prompts/lente-alumno.md` |
| Render | **capturas**, no Markdown | lo que solo se ve en pantalla | `prompts/lente-render.md` |

- **DEBE**: cada lente es un subagente Opus nuevo, sin el historial del
  escritor; las tres salen en un solo mensaje. Solo lectura sobre la rama:
  Corrección escribe scripts solo en el scratchpad.
- **DEBE**: Render recibe capturas de página completa a **390 y 1280 px** con
  todo `<details>` abierto (pistas y respuestas son `<details>`, ver CLAUDE.md
  § Authoring contract); las toma `scripts/capturas.sh` tras `raya build`.
- **CRITERIO**: Alumno no recibe plan ni fuente: lo que necesite tiene que
  estar en la página (`1ca1043`: V llegaba sin anunciarse).

## Errores sembrados

- **DEBE**: cada ronda lleva **1–2 defectos conocidos** plantados por el
  orquestador. El sembrado sale de `defectos.md` o de la auditoría, es de la
  especialidad de la lente (número falso → Corrección; pista que filtra →
  Alumno; tabla de 6 columnas → Render) y se anota en `estado.json`
  (`ruta:línea`, defecto esperado). La lente no sabe que existe.
- **DEBE**: **nunca** se siembra en la rama de trabajo. Dos vías:
  1. Worktree desechable: `git worktree add --detach <scratch>/siembra-R<n> HEAD`,
     plantar y construir ahí, pasar esa ruta (o sus capturas) a la lente, y
     al cerrar `git worktree remove --force <scratch>/siembra-R<n>`.
  2. Copia: `cp` la página a `<scratch>/siembra/`, plantar en la copia y
     pasarla a la lente en lugar de la original.
- **DEBE**: antes de cada commit, `git diff` de la rama no contiene el texto
  sembrado (grep) y `git worktree list` no lista `siembra-*`.
- **DEBE**: si la lente no reporta el sembrado, **la ronda no cuenta**: lente
  nueva, otro sembrado; dos fallos seguidos → se reescribe su prompt. El
  hallazgo del sembrado se descarta al adjudicar.

## Evidencia y formato
- **DEBE**: todo hallazgo trae `ruta:línea` o `captura.png` + zona. Sin
  evidencia se descarta. «Sin hallazgos» solo vale con la **lista de lo
  comprobado** (números recalculados, bloques corridos, capturas vistas).
- **DEBE**: el orquestador reproduce cada hallazgo antes de arreglarlo.

```
H<n> · <alta|media|baja> · <DEBE|DEBERÍA|CRITERIO> <referencia § regla>
evidencia: <ruta:línea | captura + zona>
qué pasa: <una o dos frases; cita el texto o el número>
arreglo: <cambio mínimo; «a decidir» si toca qué se enseña>
```

**alta** = falso, no corre, no se ve o regala la respuesta; **media** = confunde; **baja** = estilo.

## Rondas y terminación

- **DEBE**: máximo **3 rondas**. La 1 sobre toda la unidad; la 2 y la 3 solo
  sobre el diff de los arreglos (`git diff <base-ronda>..HEAD`), con lentes y
  sembrado nuevos.
- **DEBE**: termina con **0 altas abiertas + 0 hallazgos nuevos aceptados +
  compuertas verdes** (`verificacion.md`). Lee el código de salida de pytest;
  entubado a `tail` un rojo parece verde (`958fa25`).
- **DEBE**: al cerrar, cada hallazgo se **adjudica** (arreglado / rechazado con razón /
  pendiente) y va al reporte de G3. Altas tras la ronda 3 → pregunta al usuario.

## Aprender del defecto
- **DEBE**: todo defecto arreglado entra a `defectos.md` en el mismo commit.
- **DEBE**: un defecto que aparece **2 veces** → se propone una guarda en
  `tools/` (`2dac49c`: publicado dos veces, se volvió
  `tools/test_aceptacion.py::test_extra_el_vocabulario_de_arbol_no_se_usa_antes_de_presentarlo`).
- **DEBE**: la guarda se prueba **mordiendo**: reintroducir el defecto
  (worktree desechable o caso sintético) la hace fallar; luego se revierte.
  Patrón: `tools/test_gen_optimizacion.py::test_la_guarda_de_rotulos_si_puede_fallar`.

## Excepciones

- Diff que no toca prosa ni figuras (solo generador o prueba): basta Corrección.
- Render no se omite por simple: las tablas partidas solo se vieron en captura (`dc313cc`).
