# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **course source repository**, not an application. It holds authored Markdown/YAML for the ITAM course *Inteligencia Artificial — Otoño 2026*, consumed by the Raya Lucaria framework (Glintstone static builder) to generate a static site published to GitHub Pages.

There is no application code here — only 10 tracked files: `raya.yaml`, `course/`, `skins/`, and `.github/workflows/pages.yml`.

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

There is no test suite in this repo; the CLI's tests live in `raya_lucaria`. Validation of this course *is* the test.

## `artifact/` is generated — never edit it

`artifact/` is gitignored build output (`manifest.json`, `data/*.json`, `site/`). Regenerate it with `raya build`; do not hand-edit it or commit it. To change what appears on the site, change `course/`, `raya.yaml`, or `skins/`.

## Authoring contract

The rules below are enforced by `raya validate` and are the ones most likely to bite.

**Ordering and stable identity.** Numeric prefixes on files and directories (`1_unit/`, `2_topic/`, `1_inicio_de_cursos.yaml`) define authoring order *only*. They are stripped from rendered URLs, labels, and stable IDs, and renumbering must not break anything. Durable references use the frontmatter `id` (e.g. `course-root`), not the filename. `A_`-prefixed directories are appendix/anexo material.

**Pages.** Every rendered directory needs a `0_index.md` landing page. Frontmatter stays compact: `id`, `title`, `nav_title`, `summary`, `status`, and optionally `estimated_time`, `tags`, `prerequisites`, `aliases`. Cross-page links prefer `raya:<stable-id>` or wikilinks `[[target]]` / `[[target|label]]`; ambiguous or missing wikilinks fail validation.

**Official learning objects.** YAML under `_official/<family>/` — families include `tasks`, `cards`, `quizzes`, `prompts`. Objects colocated beside a quantum may omit `scope.quantum` (it is inferred from the nearest directory page); objects under source-root `course/_official/` **must** declare it explicitly. This repo uses the latter — every task carries `scope: {quantum: course-root}`. Shape used here:

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

## Mantenimiento de la unidad de historia de la IA

`course/1_introduccion/2_historia_ia/` es la única unidad escrita hasta ahora.
Dos cosas hay que saber para mantenerla.

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
python3 -m pytest tools/ -q      # 42 guardas de regresión
```

`docs/verificacion/` guarda, por página, la fuente de cada afirmación datable.
Toda fecha nueva se verifica antes de escribirse y se registra ahí; hay una
prueba que falla si una fila queda sin verificar. `tools/README.md` explica qué
hace cada script y cuáles son de un solo uso.

## Skins

`raya.yaml` selects the course skin by ID (`render.skin: eva-cyberpunk`), resolved against `skins/*.yaml` at the repo root plus built-in profiles. A section can override it with `<section>/_raya/skin.yaml` containing `render.skin`; that file must sit beside a `0_index.md`, and the deepest matching selector wins.

Skin files carry **semantic tokens only** — `tokens.color`, `tokens.graph.group_1..8`, `tokens.font`, `tokens.density`. Raw CSS or extra keys are rejected. The builder enforces a **4.5:1 contrast minimum** on three pairs: `text`/`page`, `accent`/`page`, and `text`/`accent_soft`. A dark skin like `eva-cyberpunk` is easy to break here — run `raya validate` after any palette edit.

## CI / publishing

`.github/workflows/pages.yml` calls a reusable workflow from `raya-lucaria/raya-lucaria.github.io`, pinned to a commit SHA, with `course_path: .`. It runs on every push and pull request and deploys to GitHub Pages (concurrency group `pages`, cancel-in-progress). Bumping the framework version means bumping that pinned SHA. Because CI validates and builds from source, a local `raya validate` pass is the gate before pushing.
