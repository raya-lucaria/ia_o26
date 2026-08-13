# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **course source repository**, not an application. It holds authored Markdown/YAML for the ITAM course *Inteligencia Artificial — Otoño 2026*, consumed by the Raya Lucaria framework (Glintstone static builder) to generate a static site published to GitHub Pages.

The published site comes from `raya.yaml`, `course/`, `skins/`, and `.github/workflows/pages.yml`. Around those sit three support trees that never render: `tools/` (Python generators + the pytest suite), `docs/verificacion/` (per-page source records for every datable claim), and `lecturas/` (the reading-booklet pipeline).

Course-facing content (page prose, titles, summaries, task instructions) is written in **Spanish**. Technical identifiers — `id`, `type`, `authority`, `scope`, filenames, tags, skin token names — stay in **English**.

## The build toolchain lives in a sibling repository

The `raya` CLI is not installed here. It lives at `/home/uumami/itam/raya_lucaria` (a separate git repo) and is invoked from there with this repo's path as an argument:

```bash
cd /home/uumami/itam/raya_lucaria
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya validate /home/uumami/itam/ia_o26
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya build    /home/uumami/itam/ia_o26
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya preview  /home/uumami/itam/ia_o26            # validate + build + serve
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya preview  /home/uumami/itam/ia_o26 --dry-run  # print plan only
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya artifacts inspect /home/uumami/itam/ia_o26/artifact
```

Docker equivalent, from the same directory: `docker compose run --rm dev uv run raya <cmd> <path>`.

`validate` is the fast feedback loop — it catches broken links, missing IDs, bad official-object scopes, and skin contrast failures without building. `build` implies validate. `preview` serves `artifact/site/` at `http://127.0.0.1:8000/index.html`, with an inspection view at `/_raya/inspect/index.html`.

The CLI's own tests live in `raya_lucaria`. This repo's tests are content guards, under `tools/` (see below) — `raya validate` and `pytest tools/` are two separate gates, and CI runs both.

## `artifact/` is generated — never edit it

`artifact/` is gitignored build output (`manifest.json`, `data/*.json`, `site/`). Regenerate it with `raya build`; do not hand-edit it or commit it. To change what appears on the site, change `course/`, `raya.yaml`, or `skins/`.

Otras rutas gitignoradas que sí existen en esta máquina y **no** en un clon
limpio: `legacy/` (el deck heredado y PDFs pesados que consume
`curar_imagenes.py`), `tools/anna.py` (cliente de recuperación bibliográfica,
local a propósito), `.env` (solo `OPENAI_API_KEY`, para `gen_ilustraciones.py`),
y `.superpowers/` + `docs/superpowers/`. Ningún script que corra en CI depende de
ellas; si una prueba parece necesitar una, es de las que se saltan solas.

## Authoring contract

The rules below are enforced by `raya validate` and are the ones most likely to bite.

**Ordering and stable identity.** Numeric prefixes on files and directories (`1_unit/`, `2_topic/`, `1_inicio_de_cursos.yaml`) define authoring order *only*. They are stripped from rendered URLs, labels, and stable IDs, and renumbering must not break anything. Durable references use the frontmatter `id` (e.g. `course-root`), not the filename. `A_`-prefixed directories are appendix/anexo material.

**Pages.** Every rendered directory needs a `0_index.md` landing page. Frontmatter stays compact: `id`, `title`, `nav_title`, `summary`, `status`, and optionally `estimated_time`, `tags`, `prerequisites`, `aliases`. Cross-page links prefer `raya:<stable-id>` or wikilinks `[[target]]` / `[[target|label]]`; ambiguous or missing wikilinks fail validation. Images and tables that need a number go inside a directive block — `::: figure {#id title="…"}` … `:::` — numbered per page hierarchy by the `render.numbered_objects` config in `raya.yaml`; a bare `![]()` renders without a "Figura N" caption.

**Official learning objects.** YAML under `_official/<family>/` — families include `tasks`, `cards`, `quizzes`, `prompts`. Objects colocated beside a quantum may omit `scope.quantum` (it is inferred from the nearest directory page); objects under source-root `course/_official/` **must** declare it explicitly. Both patterns are in use: the five calendar tasks in `course/_official/tasks/` carry `scope: {quantum: course-root}`, while unit-level objects (`course/1_introduccion/2_historia_ia/_official/`, `course/2_filosofia_ia/_official/`) carry no `scope` block at all — `test_oficiales.py` fails if a card grows one. Root-scoped shape:

```yaml
id: asueto-noviembre-2026        # durable, kebab-case, unique across the course
type: task
authority: official
scope:
  quantum: course-root
content:
  title: Asueto — no hay clase
  instructions: El lunes 2 de noviembre no hay sesión de Inteligencia Artificial.
  due: "2026-11-02"              # quoted; validated as a date
  status: published
  tags: [calendario, asueto]
```

Calendar tasks mirror the dates listed in `course/0_index.md` — when one changes, change both. `calesc2026.pdf` at the repo root is the ITAM academic calendar these dates come from.

**Support directories don't render.** `_official/`, `_assets/`, `_reviewed/`, `_drafts/`, `_partials/` are source support. Rendered Markdown may link into its own or an ancestor `_assets/`, never into the others.

## Las dos unidades escritas, y cómo se mantiene cada una

Hay dos, y se mantienen distinto:

- `course/1_introduccion/2_historia_ia/` — ocho páginas de prosa, con imágenes
  y SVG generados desde `tools/`, y un registro de fuentes por página en
  `docs/verificacion/`. Es la unidad que describe el resto de esta sección.
- `course/2_filosofia_ia/` — una unidad de lecturas: su contenido real es el
  cuadernillo PDF que produce `lecturas/` (ver más abajo). No tiene assets
  generados ni registro de verificación; lo que hay que cuidar ahí es que la
  copia del PDF y los textos duplicados no se desincronicen de la fuente.

Dos cosas hay que saber para mantener la unidad de historia.

**Qué caduca y qué no.** Solo `5_estado_actual.md` está diseñada para caducar:
declara su fecha de corte en el `summary`, usa únicamente tablas, y ninguna otra
página depende de ella. **Refréscala al inicio de cada semestre**, antes de la
primera sesión, y no toques el resto por antigüedad.

**Dónde viven las fechas.** `tools/hitos.json` es la única fuente de verdad de
los hitos de las líneas del tiempo, y `tools/computo.json` de las cifras de la
gráfica de cómputo. Tras editar cualquiera de los dos hay que regenerar:

```bash
python3 tools/gen_timeline.py    # las nueve líneas del tiempo
python3 tools/gen_computo.py     # la gráfica de escala de cómputo
python3 -m pytest tools/ -q      # las guardas de regresión
```

`docs/verificacion/` guarda, por página, la fuente de cada afirmación datable.
Toda fecha nueva se verifica antes de escribirse y se registra ahí; hay una
prueba que falla si una **fila** queda sin verificar (no basta un «sí» suelto en
el archivo). `tools/README.md` explica qué hace cada script y cuáles son de un
solo uso.

**Agregar, quitar o renombrar una página de esta unidad toca tres lugares**: el
archivo en `course/1_introduccion/2_historia_ia/`, su registro homónimo en
`docs/verificacion/`, y las dos listas literales al inicio de
`tools/test_aceptacion.py` (`PAGINAS`, por nombre de archivo, y
`PAGINAS_UNIDAD_EN_ORDEN`, por id estable y en orden de navegación).

## The pytest suite guards content, not code

`python3 -m pytest tools/ -q` (77 tests as of August 2026) is the
second gate alongside `raya validate`, and CI blocks the deploy on it. The tests
assert things prose review misses: every image in `_assets/` has a credit row
with a recognizable license in `CREDITOS.md`, every generated SVG still matches
what its generator would produce today, every illustration prompt avoids real
people and protected characters, every datable claim has a verified row in
`docs/verificacion/`, official cards keep their shape and unique ids.

```bash
pip install pillow pyyaml pypdf pytest    # lo que necesita la suite
python3 -m pytest tools/ -q               # todo
python3 -m pytest tools/test_lecturas.py -q                          # un archivo
python3 -m pytest tools/test_lecturas.py::test_la_introduccion_no_ha_derivado -q   # una prueba
python3 -m pytest tools/ -q -k cuadernillo                           # por nombre
```

Consequences worth internalizing:

- **Editing a generated `_assets/` file by hand fails the suite.** Change the
  JSON source and rerun the generator instead.
- **Deleting an unused asset means deleting its inventory row too** (in
  `commons.tsv`, or flipping `decision` to `descartar` in
  `imagenes_heredadas.tsv`) — otherwise the generator resurrects it.
- `test_aceptacion.py` shells out to the `raya` CLI in the sibling repo; two of
  its tests fail on environment, not on a real defect, if that repo is missing
  or unsynced.

## `lecturas/` — the reading-booklet pipeline

A second, self-contained toolchain that produces the PDF booklets linked from
course pages. Two steps, both declarative and both rerunnable:

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_1   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_1   # recorta y maqueta
```

`bajar_lecturas.py` only fetches public-domain texts, and every source declares
a `debe_contener` string so a wrong-but-plausibly-named download fails loudly.
`LecturaPDF` in `lecturas.py` carries the same field for the PDF path: the
excerpt is re-read after being cut and the build aborts if the phrase is not in
it, so a different edition behind the expected filename cannot pass as the
right pages. `lecturas.py` holds the `LECTURAS` list — adding a reading is
adding an entry with its excerpt rule and the reason it is read, not editing
code. It depends on
`weasyprint` and `pypdf`. Sources land in `fuentes/` exactly as downloaded so
the excerpt stays auditable, and each module's `README.md` records provenance
and any discrepancy with the syllabus pagination.

**In-copyright material is linked, never republished.** `.gitignore` excludes
`lecturas/**/fuentes/*.pdf` and the generated HTML viewer; keep it that way when
adding a module. Only the open-access sources (`fuentes/*.txt`) and the produced
excerpt PDFs are committed.

**Publicar un cuadernillo son tres copias a mano.** Nada enlaza entre `lecturas/`
y `course/`, así que regenerar el PDF no actualiza el sitio por sí solo:

```bash
python3 tools/lecturas.py filosofia_ia/clase_1
cp lecturas/filosofia_ia/clase_1/lecturas/filosofia_ia_clase_1_cuadernillo.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf
pdftoppm -png -r 106 -f 1 -l 1 -singlefile \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_portada
python3 -m pytest tools/test_lecturas.py -q
```

Tres duplicaciones deliberadas viven ahí, y `test_lecturas.py` falla si alguna
deriva — no las arregles editando la copia, edita la fuente y vuelve a copiar:

- El PDF publicado tiene que ser **byte-idéntico** al que produjo el pipeline.
- `lecturas/**/introduccion.md` es la fuente única de la introducción; la página
  del curso (`course/2_filosofia_ia/1_accelerate_what.md`) lleva una copia literal
  de su sección «Cómo leer este cuadernillo».
- El número de páginas del cuadernillo aparece en la página del módulo, la tarea
  oficial, el visor y dos `README.md`; léelo del PDF ya copiado, no lo estimes.

## Skins

`raya.yaml` selects the course skin by ID (`render.skin: eva-cyberpunk`), resolved against `skins/*.yaml` at the repo root plus built-in profiles. A section can override it with `<section>/_raya/skin.yaml` containing `render.skin`; that file must sit beside a `0_index.md`, and the deepest matching selector wins.

Skin files carry **semantic tokens only** — `tokens.color`, `tokens.graph.group_1..8`, `tokens.font`, `tokens.density`. Raw CSS or extra keys are rejected. The builder enforces a **4.5:1 contrast minimum** on three pairs: `text`/`page`, `accent`/`page`, and `text`/`accent_soft`. A dark skin like `eva-cyberpunk` is easy to break here — run `raya validate` after any palette edit.

## CI / publishing

`.github/workflows/pages.yml` runs two jobs on every push and pull request. `checks` runs `python -m pytest tools/ -q`; `course-pages` calls a reusable workflow from `raya-lucaria/raya-lucaria.github.io`, pinned to a commit SHA, with `course_path: .`, and deploys to GitHub Pages (concurrency group `pages`, cancel-in-progress).

The `needs: checks` line on `course-pages` is what makes the tests a real gate — without it both jobs race and the site publishes even when the suite fails. Do not drop it. Bumping the framework version means bumping the pinned SHA. Locally, `raya validate` plus `pytest tools/ -q` reproduce both gates; run them before pushing.
