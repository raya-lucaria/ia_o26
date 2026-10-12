# Revisión adversarial

Las lentes buscan **romper** la unidad, no aprobarla (casi nada de `defectos.md` lo vio `raya validate`).

## Lentes, en paralelo, sin contexto previo

| Lente | Recibe | Hace | Plantilla |
|---|---|---|---|
| Corrección | páginas, fuente Python, generadores, pruebas | recalcula, corre cada bloque, coteja prosa ↔ figura ↔ fuente | `prompts/lente-correccion.md` |
| Alumno | páginas en orden de navegación, nada más | orden, carga, definiciones, ejercicios | `prompts/lente-alumno.md` |
| Render | **franjas** de captura + `inventario.tsv`, no Markdown | lo que solo se ve en pantalla | `prompts/lente-render.md` |
| Consistencia (auditoría) | páginas + referencias | vocabulario, ids, esqueleto, notación | `prompts/lente-consistencia.md` |

- **DEBE**: cada lente es un subagente Opus nuevo, sin el historial del escritor; todas salen en un solo mensaje.
- **DEBE**: solo lectura sobre la rama. Scripts propios, al scratchpad. Una lente que necesite correr pruebas o
  generadores (los `test_gen_*` reescriben `_assets/`) lo hace en un worktree desechable:
  `git worktree add --detach <scratch>/lente-<n> HEAD` y al final `git worktree remove --force <scratch>/lente-<n>`.
- **DEBE**: Render ve capturas a **390 y 1280 px** con los `<details>` del artículo abiertos (`scripts/capturas.sh`
  tras `raya build`), cortadas en franjas ≤2000 px, más `inventario.tsv` y los AVISO de `scripts/revisar_desborde.py`.
  Una lente lee pocas imágenes por corrida: **≤6 páginas por lente Render**, varias en paralelo.
- **CRITERIO**: Alumno no recibe plan ni fuente: lo que necesite tiene que estar en la página (`1ca1043`: V llegaba sin anunciarse).

## Errores sembrados

- **DEBE**: cada ronda lleva **1–2 defectos conocidos** plantados por el orquestador, de `defectos.md` o de la
  auditoría y de la especialidad de la lente (número falso → Corrección; pista que filtra → Alumno; tabla de 6
  columnas → Render); se anota en `estado.json` (`ruta:línea`, defecto esperado). La lente no sabe que existe.
- **DEBE**: **nunca** se siembra en la rama de trabajo: worktree desechable (`<scratch>/siembra-R<n>`, como arriba;
  se construye ahí) o copia de la página en `<scratch>/siembra/` que la lente recibe en lugar de la original.
- **DEBE**: antes de cada commit, `git diff` de la rama no contiene el texto sembrado (grep) y `git worktree list`
  no lista `siembra-*` ni `lente-*`.
- **DEBE**: si la lente no reporta el sembrado, **la ronda no cuenta**: lente nueva, otro sembrado; dos fallos
  seguidos → se reescribe su prompt. El hallazgo del sembrado se descarta al adjudicar.
- **DEBE**: en rondas sobre diff, la lente lee **la copia sembrada**, no el parche: el parche sale de la rama y no
  trae el sembrado (7.3, ronda 3: la lente leyó el parche y no vio 0.99→0.97). El parche solo dice dónde mirar.

## Evidencia y formato
- **DEBE**: todo hallazgo trae `ruta:línea` o `franja.png` + zona; sin evidencia se descarta. «Sin hallazgos» solo
  vale con la **lista de lo comprobado**. Un hallazgo de ausencia (falta una prueba) cita dónde debería estar.
- **DEBE**: el orquestador reproduce cada hallazgo antes de arreglarlo.

```
H<n> · <alta|media|baja> · <DEBE|DEBERÍA|CRITERIO> <referencia § regla>
evidencia: <ruta:línea | franja + zona>
qué pasa: <una o dos frases; cita el texto o el número>
arreglo: <cambio mínimo; «a decidir» si toca qué se enseña>
```

- **DEBE**: dos escalas que no se mezclan. **Severidad** = efecto: alta = falso, no corre, no se ve o regala la
  respuesta; media = confunde u obliga a releer; baja = forma. **Capa** = si la regla se negocia
  (DEBE/DEBERÍA/CRITERIO). Un DEBE de forma (id, preámbulo literal) puede ser baja. En Corrección la
  «referencia § regla» es opcional: «dato correcto» basta.
- **DEBE**: un defecto que ya es fila abierta de `defectos.md` se reporta en una línea, `[conocido #N] ruta:línea`, sin re-argumentar.
- **CRITERIO**: una línea citada en las referencias como modelo lo es solo del patrón nombrado; no exime al resto de su página.

## Rondas y terminación

- **DEBE**: máximo **3 rondas**: la 1 sobre toda la unidad, la 2 y la 3 solo sobre el diff de los arreglos
  (`git diff <base-ronda>..HEAD`), con lentes y sembrado nuevos. Alcance: «toda la unidad» | «sección <ruta>» | «diff: <archivo>».
- **DEBE**: termina con **0 altas abiertas + 0 hallazgos nuevos aceptados + compuertas verdes** (`verificacion.md`).
  Lee el código de salida de pytest; entubado a `tail` un rojo parece verde (`958fa25`).
- **DEBE**: al cerrar, cada hallazgo se **adjudica** (arreglado / rechazado con razón / pendiente) y va al reporte
  de G3. Altas tras la ronda 3 → pregunta al usuario.

## Aprender del defecto
- **DEBE**: todo defecto arreglado entra a `defectos.md` en el mismo commit.
- **DEBE**: un defecto que aparece **2 veces** → se propone una guarda en `tools/` (`2dac49c`: publicado dos veces,
  se volvió `tools/test_aceptacion.py::test_extra_el_vocabulario_de_arbol_no_se_usa_antes_de_presentarlo`).
- **DEBE**: la guarda se prueba **mordiendo**: reintroducir el defecto (worktree desechable o caso sintético) la hace
  fallar; luego se revierte. Patrón: `tools/test_gen_optimizacion.py::test_la_guarda_de_rotulos_si_puede_fallar`.

## Excepciones

- Diff que no toca prosa ni figuras (solo generador o prueba): basta Corrección.
- Render no se omite por simple: las tablas partidas solo se vieron en captura (`dc313cc`).
- Texto o CSS del framework («At a glance», «Page connections»): fuera del repo del curso; Render lo pone en «Framework (aviso)», nunca como hallazgo.
