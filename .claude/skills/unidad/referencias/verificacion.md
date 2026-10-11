# Verificación: ocho compuertas, en este orden

`R` = raíz del worktree (`git rev-parse --show-toplevel`); `S` = `.claude/skills/unidad/scripts`; `SCR` = el scratchpad. **Ninguna salida va al repo.** Lee siempre el **código de salida**: entubado a `tail`, un rojo parece verde (`958fa25`).

| # | Compuerta | Corre en la fase | Pasa si |
|---|---|---|---|
| 1 | generadores → `git status` limpio | 5 (al final, tú), 7, antes de cada commit | sale 0 |
| 2 | `pytest tools/` | 3 y 5 (`-k` de lo tocado), 7 completo, antes de cada commit | 0 fallas y ningún skip prohibido |
| 3 | `raya validate` y `raya build` | 4 tras cada ola (validate), 6 y 7 (build) | sin errores ni advertencias |
| 4 | pruebas que leen `artifact/` | 7, después de 3 | 0 skips |
| 5 | capturas 390/1280 miradas | 6 (lente Render), 7 sobre lo tocado | cada PNG visto, sin desborde |
| 6 | mutaciones | 3, 5 u 8, cada vez que nace una guarda | la guarda falla con el defecto |
| 7 | CI tras el merge | G3 | `checks` y `course-pages` verdes |
| 8 | en vivo, Colab incluido | G3, tras el deploy | `en_vivo.sh` sale 0 |

- **DEBE**: si una compuerta falla, se arregla y se vuelve a correr **desde la 1**; un arreglo de prosa puede mover una cifra que lee un generador.
- **DEBE**: en G3 se reporta cada compuerta con su cifra (pruebas, páginas, capturas, mutaciones).

## 1 · Generadores

```bash
$S/generadores_limpios.sh course/<unidad>                # antes de publicar: árbol limpio
$S/generadores_limpios.sh --sin-commit course/<unidad>   # durante el trabajo: la corrida no cambia nada
```
- **DEBE**: detecta los `tools/gen_*.py` de la unidad; nunca corre `gen_ilustraciones.py`. Un cambio que aparece aquí y no buscabas es un archivo editado a mano (`codigo.md` § 3).

## 2 · Suite

```bash
cd $R && python3 -m pytest tools/ -q -rs
```
- **DEBE**: `-rs` lista los skips. En esta máquina **cuenta como falla** el skip de `test_1`/`test_2` de `tools/test_aceptacion.py` (falta el CLI `raya`; CLAUDE.md § The pytest suite) y el de las pruebas de Chrome de `tools/test_traza_web.py`. Un `-k` nunca sustituye la corrida completa de la fase 7.
- **DEBE**: si la unidad está en `UNIDADES_CONTRATO`, también `python3 tools/contrato_unidad.py course/<unidad> --estricto`.

## 3 y 4 · Raya, y lo que lee `artifact/`

```bash
cd /home/uumami/itam/raya_lucaria
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya validate $R
UV_PROJECT_ENVIRONMENT=.venv-local uv run raya build    $R    # ~70 s; escribe $R/artifact/ (gitignorado)
```
- **DEBE**: con `$R` del worktree, no del checkout principal. Validate verde no es render correcto (CLAUDE.md § The build toolchain): por eso existen 4 y 5.
- **DEBE**: tras el build, `python3 -m pytest tools/test_aceptacion.py -q -rs` sin ningún «No hay artifact/ construido».

## 5 · Capturas, y mirarlas

```bash
$S/capturas.sh $SCR/cap <ruta-del-sitio>/ … course/<unidad>/_assets/<id>.svg …
$S/revisar_desborde.py --unidad <segmento-de-la-unidad>/              # medido, a 390 px
```
- **DEBE**: cada página y SVG tocados, a 390 y 1280, con los `<details>` del artículo abiertos; abre cada PNG con Read (recorta con PIL si mide > 8000 px). Un SVG se mira en navegador, no con ImageMagick (CLAUDE.md § Computabilidad y complejidad).
- **DEBE**: `revisar_desborde.py` sale 0: sin scroll de página, fórmula más ancha que su bloque, tramo partido en celda ni error de MathJax. Una figura o tabla con scroll propio no cuenta.

## 6 · Mutaciones

- **DEBE**: toda guarda nueva se prueba plantando su defecto en un worktree desechable: la prueba **tiene que fallar**; luego se borra:
```bash
git -C $R worktree add --detach $SCR/mut-1 HEAD     # plantar el defecto ahí
cd $SCR/mut-1 && python3 -m pytest tools/test_<x>.py::<guarda> -q; git -C $R worktree remove --force $SCR/mut-1
```
- **DEBERÍA**: si el defecto no se puede plantar en archivo, un caso sintético dentro de la prueba (`tools/test_gen_optimizacion.py:750`). Cuenta cuántas mutaciones murieron (`defectos.md` #35).

## 7 · CI

- **DEBE**: `gh run list --branch main --limit 3` y `gh run watch <id> --exit-status`: `checks` y `course-pages` verdes (`needs: checks`, `.github/workflows/pages.yml:42`).

## 8 · En vivo

`$S/en_vivo.sh --comparar <ruta>/ …`: 200, recursos 200, Colab con notebook en `main`, idéntica al build.
- **DEBE**: toda página tocada y toda página con badge de Colab. Colab da 200 aunque el notebook falte: el script lo busca en `raw.githubusercontent.com`.
- **DEBE**: `--comparar` contra un `raya build` de `main` ya mergeado. El build es determinista: la página publicada es byte a byte la local.
- **DEBERÍA**: el CDN guarda 10 min (`max-age=600`): si falla justo tras el deploy, espera y repite antes de concluir.

## Excepciones

- CI no corre generadores ni builds con Chrome: 1, 4 y 5 son solo locales, y por eso no se saltan.
- Sin playwright, `capturas.sh` cae a Chrome sin `<details>` abiertos y `revisar_desborde.py` no corre: la compuerta 5
  **no pasa**. Instálalo (`pip install playwright && playwright install chromium`) o pregunta al usuario; nunca la des por verde.
