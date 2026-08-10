# tools/

Scripts y datos de soporte para la unidad `course/1_introduccion/2_historia_ia/`.
Nada de esto se publica en el sitio; son los generadores, inventarios y pruebas
detrás de lo que sí se publica (`_assets/`, `_official/`).

Nada de esto corre automáticamente en ninguna parte (ver H16 más abajo):
hay que ejecutarlo a mano cuando algo cambie.

## Dependencias

```bash
pip install pillow pyyaml pytest
```

- **Pillow** (`PIL`): recompresión y generación de imágenes (`gen_life.py`,
  `curar_imagenes.py`, `bajar_commons.py`, `gen_ilustraciones.py`, y sus pruebas).
- **PyYAML** (`yaml`): lee las tarjetas oficiales en `test_oficiales.py`.
- **pytest**: corre toda la suite.
- **ImageMagick** (`montage`, binario del sistema, no de pip): solo lo usa
  `curar_imagenes.py` para armar hojas de contacto. No hace falta para nada más.
- **El CLI `raya`**, en el repo hermano `/home/uumami/itam/raya_lucaria`: solo
  lo invoca `test_aceptacion.py` (vía `uv run --offline raya ...`). Sin ese
  repo clonado y sin `UV_PROJECT_ENVIRONMENT=.venv-local uv sync` corrido ahí,
  `test_1` y `test_2` de `test_aceptacion.py` fallan por entorno, no por un
  error real en este repo.
- **`OPENAI_API_KEY`**: solo lo necesita `gen_ilustraciones.py` (llama a
  `gpt-image-2`). Ninguna prueba la requiere: las pruebas de ilustraciones
  verifican los archivos ya generados en `_assets/`, no vuelven a llamar la API.

## Correr toda la suite

```bash
cd /home/uumami/itam/ia_o26
python3 -m pytest tools/ -q
```

36+ pruebas, deben pasar todas antes de comitear un cambio que toque
`_assets/`, `_official/`, o cualquier `tools/*.json`/`tools/*.tsv`. Ver H16:
esto **no corre en CI todavía** — es responsabilidad de quien comitea.

## Generadores (infraestructura viva del curso)

Regenerar es seguro y esperado cada vez que cambie su fuente de datos. Ninguno
pide red ni credenciales (salvo `gen_ilustraciones.py`).

| Script | Fuente | Genera | Cuándo correrlo |
|---|---|---|---|
| `gen_timeline.py` | `hitos.json` | `_assets/v1-panorama.svg`, `_assets/v1-tramo-*.svg` (9 archivos) | Al agregar, quitar o mover un hito |
| `gen_computo.py` | `computo.json` | `_assets/v9-computo.svg` | Al agregar un modelo o actualizar una cifra de cómputo |
| `gen_life.py` | (patrón fijo en el propio script) | `_assets/v13-game-of-life.png` | Rara vez — el patrón no cambia; existe por si se ajusta la paleta o el tamaño de celda |
| `gen_ilustraciones.py` | `ilustraciones.json` + API de `gpt-image-2` | `_assets/ilus-*.jpg` | Al agregar una ilustración nueva al catálogo. Requiere `OPENAI_API_KEY` (`set -a && . ./.env && set +a`) y cuesta dinero por llamada: no es para correr "por si acaso" |
| `bajar_commons.py` | `commons.tsv` | `_assets/foto-*.jpg` + bloque de filas para `CREDITOS.md` (impreso en stdout, no escrito solo) | Al agregar una fotografía nueva desde Wikimedia Commons |

Cada uno tiene su prueba homónima (`test_gen_timeline.py`, `test_gen_computo.py`,
`test_commons.py`) que regenera el archivo antes de comparar, así que correr
`pytest` ya certifica que el archivo comiteado coincide con lo que el generador
produciría hoy.

## `curar_imagenes.py` — de un solo uso, ya ejecutado

Extrae imágenes del deck heredado `legacy/02_historia_del_ai.pptx` (archivo
local, ignorado por git — no está en el repo) y las recomprime según las
decisiones ya registradas en `imagenes_heredadas.tsv`. La curaduría real
—qué imagen se conserva, cuál se descarta y por qué— ya se hizo; ese trabajo
vive en `imagenes_heredadas.tsv`, no en el script. No hay razón para volver a
correrlo salvo que aparezca una versión nueva del deck original.

## Datos e inventarios (no son scripts)

| Archivo | Qué es | Quién lo consume |
|---|---|---|
| `hitos.json` | Única fuente de verdad de fechas de la unidad. Ver su campo `"nota"` antes de tocarlo | `gen_timeline.py` |
| `computo.json` | Cómputo de entrenamiento por modelo (fuente: Epoch AI) | `gen_computo.py` |
| `ilustraciones.json` | Catálogo de prompts para `gpt-image-2`, con el estilo compartido | `gen_ilustraciones.py` |
| `commons.tsv` | Manifiesto de fotos a descargar de Wikimedia Commons: título en Commons, descripción, y en qué página se usa | `bajar_commons.py` |
| `imagenes_heredadas.tsv` | Inventario de las ~91 imágenes del deck heredado, con la decisión `conservar`/`descartar` por cada una y por qué. Es el registro auditable de la curaduría, no solo una lista de archivos | `curar_imagenes.py`, y `test_curar_imagenes.py` expone `filas_de_creditos()` reutilizado por `test_commons.py` |

**Si borras un archivo de `_assets/` porque quedó sin usar, actualiza también
el inventario que lo generó** (quita la fila de `commons.tsv`, o cambia la
`decision` a `descartar` en `imagenes_heredadas.tsv`) — si no, la próxima
corrida del generador correspondiente lo vuelve a traer.

## Pruebas

| Archivo | Qué verifica |
|---|---|
| `test_aceptacion.py` | Los diez criterios de aceptación del diseño de la unidad (validate/build de `raya`, navegación, objetos oficiales, créditos de imágenes, verificación de fuentes, peso del repositorio, legibilidad de SVG, `.env` ignorado) |
| `test_gen_timeline.py` | `gen_timeline.py` produce SVG bien formados y que el título declarado de cada tramo (cuando trae un rango de años) coincide con el rango real de sus hitos |
| `test_gen_computo.py` | `gen_computo.py` produce un SVG consistente con `computo.json`, que regenerarlo no cambia el archivo comiteado, y que ninguna etiqueta de modelo se encima con otra |
| `test_commons.py` | Cada fila de `commons.tsv` está descargada, recomprimida a ≤1400px, y tiene una fila de créditos con licencia reconocible |
| `test_curar_imagenes.py` | El inventario `imagenes_heredadas.tsv` está bien formado, lo `conservar` existe y está recomprimido, y toda imagen de `_assets/` tiene fila en `CREDITOS.md` con origen y licencia |
| `test_ilustraciones.py` | Cada ilustración del catálogo existe, mide 1024px de ancho, pesa menos de 400 KB, está acreditada como generada, y ningún prompt pide una persona real o personaje protegido |
| `test_oficiales.py` | Las tarjetas oficiales (`_official/cards/*.yaml`) tienen forma válida: `type`, `authority`, anverso/reverso no vacíos, sin bloque `scope`, ids únicos |

## H16 — recomendación pendiente de decisión del profesor

`.github/workflows/pages.yml` delega en el workflow reutilizable de Raya, que
corre `raya validate` + `raya build` en cada push y PR, pero **no corre
`pytest tools/`**. Este README no cambia eso — modificar el workflow de CI es
una decisión del profesor, no de esta tarea. Recomendación: agregar un paso
`pip install pillow pyyaml pytest && python3 -m pytest tools/ -q` antes (o en
paralelo) del paso de Raya, para que las pruebas más caras del proyecto —la
que atrapó el bug de tamaño intrínseco en los SVG, la que exige verificación
por fila en vez de por archivo— dejen de depender de que alguien se acuerde
de correrlas a mano.
