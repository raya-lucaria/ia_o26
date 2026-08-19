# tools/

Scripts y datos de soporte para la unidad `course/1_introduccion/2_historia_ia/`.
Nada de esto se publica en el sitio; son los generadores, inventarios y pruebas
detrás de lo que sí se publica (`_assets/`, `_official/`).

Los generadores y `bajar_lecturas.py`/`lecturas.py` no corren automáticamente
en ninguna parte: hay que ejecutarlos a mano cuando algo cambie. La suite de
pruebas sí corre sola, en CI (ver H16 más abajo).

## Dependencias

```bash
pip install pillow pyyaml pypdf pytest
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

119 pruebas, deben pasar todas antes de comitear un cambio que toque
`_assets/`, `_official/`, o cualquier `tools/*.json`/`tools/*.tsv`. Desde el
commit `47697d2` esto también corre en CI, como job `checks` que bloquea el
deploy (ver H16), pero eso no exime de correrlo en local antes de comitear.

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

## Reconstruir un cuadernillo de lecturas (`filosofia_ia/clase_1` … `clase_4`)

`bajar_lecturas.py` y `lecturas.py` no son parte de la unidad de historia de
la IA, pero comparten `tools/` y su suite corre junto con el resto:

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_1   # descarga y verifica las fuentes abiertas
python3 tools/lecturas.py       filosofia_ia/clase_1   # arma el PDF del cuadernillo
```

A diferencia de los generadores de arriba, `lecturas.py` no escribe su
resultado directo en `course/`: el PDF sale en
`lecturas/filosofia_ia/clase_1/lecturas/filosofia_ia_clase_1_cuadernillo.pdf`
y **se copia a mano** a
`course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf`. La
portada también se regenera a mano, con `pdftoppm`:

```bash
cp lecturas/filosofia_ia/clase_1/lecturas/filosofia_ia_clase_1_cuadernillo.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf
pdftoppm -png -r 106 -f 1 -l 1 -singlefile \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_1_accelerate.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_portada
```

El conteo de páginas y el peso del PDF resultante viven repetidos en varios
lugares del curso (la página del módulo, la tarea oficial, el visor, y este
mismo README junto con `lecturas/filosofia_ia/clase_1/README.md`); léelos del
PDF ya copiado, no los estimes.

Los módulos 2, 3 y 4 son el mismo procedimiento con sus propios nombres:
`clase_2` → `cuadernillo_modulo_2_left_future.pdf` / `cuadernillo_portada_modulo_2`,
`clase_3` → `cuadernillo_modulo_3_exit_nrx.pdf` / `cuadernillo_portada_modulo_3`, y
`clase_4` → `cuadernillo_modulo_4_long_future.pdf` / `cuadernillo_portada_modulo_4`.
`test_lecturas.py` compara cada cifra de páginas solo contra la de su propio
módulo, y desde el módulo 3 también comprueba que el PDF publicado venga del
`introduccion.md` de hoy: editar la introducción sin reconstruir el PDF ya no
pasa callado.

**Y una advertencia sobre volver a descargar los módulos 1 y 2.** El arreglo de
`_limpiar` que trajo el módulo 3 —«I» y «A» dejaron de pegarse a la palabra
siguiente— cambia dos palabras de `clase_1` y siete de `clase_2` respecto de los
`.txt` versionados, que se descargaron antes. Y las fuentes de `clase_2` ya no
reproducen desde la web por deriva del HTML de origen, que es un problema
distinto y anterior. Volver a correr `bajar_lecturas.py` sobre esos dos módulos
ensucia el árbol sin arreglar nada; `lecturas/filosofia_ia/clase_3/README.md`
documenta el caso completo.

El módulo 4 estrenó dos formas de fuente en `bajar_lecturas.py`, las dos para
material publicado en abierto: `lesswrong=<id>`, que trae un ensayo por la API
pública del sitio porque su HTML devuelve 429 a un script, y
`pdf=(url, cortes)`, que baja un PDF gratuito y le saca el texto con
`pdftotext -layout` (hace falta `poppler-utils`). Ninguna de las dos sirve para
material de pago: eso sigue en `PDFS`, sin versionarse.

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
| `ilustraciones.json` | Catálogo de prompts para `gpt-image-2`. Ya no es un solo estilo: la clave `ilustraciones` (historia) pide fondo violeta muy oscuro opaco con atmosfera nocturna (JPEG), y `ilustraciones_filosofia` pide fondo plano horneado al color exacto del skin (PNG, ver `FONDO_OBJETIVO` en `test_ilustraciones.py`) | `gen_ilustraciones.py` |
| `commons.tsv` | Manifiesto de fotos a descargar de Wikimedia Commons: título en Commons, descripción, en qué página se usa, y la columna `unidad` (`historia`/`filosofia`) que enruta cada fila a su `_assets/` vía `ASSETS_POR_UNIDAD` | `bajar_commons.py` |
| `imagenes_heredadas.tsv` | Inventario de las ~91 imágenes del deck heredado, con la decisión `conservar`/`descartar` por cada una y por qué. Es el registro auditable de la curaduría, no solo una lista de archivos | `curar_imagenes.py`, y `test_curar_imagenes.py` |
| `unidades.py` | Módulo compartido (no dato): `ASSETS_POR_UNIDAD` mapea cada unidad a su `_assets/`, `filas_de_creditos()` parsea `CREDITOS.md`, y las constantes `CELDA_NOMBRE`/`CELDA_ORIGEN`/`CELDA_LICENCIA` fijan el índice de columna. Única fuente de estas tres cosas — se importa, no se copia | `test_aceptacion.py`, `test_curar_imagenes.py`, `test_commons.py` |
| `lecturas/filosofia_ia/clase_*/introduccion.md` | Fuente única de la introducción general del cuadernillo de lecturas; la página del curso (`course/2_filosofia_ia/1_accelerate_what.md`) lleva una copia literal de su sección «Cómo leer este cuadernillo» | `lecturas.py` (la incrusta en el PDF), `test_lecturas.py` (comprueba que la copia de la página del curso no haya derivado) |

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
| `test_lecturas.py` | Los cuatro cuadernillos de lecturas de `filosofia_ia/`: la introducción general de la página del módulo 1 no ha derivado de su `introduccion.md`, cada lectura de los tres módulos trae su ficha de cuatro apartados, el orden es consecutivo (1..6, 1..4, 1..4, 1..6), el PDF publicado de cada módulo es byte-idéntico al construido **y contiene la introducción vigente**, la cifra total de páginas coincide en los cinco o seis lugares donde cada módulo la declara, y funciones puras de `lecturas.py` (Markdown básico, huecos de páginas externas, orden de las secciones en el HTML final) |
| `test_repaso.py` | Las nueve páginas de repaso de filosofía (módulos 1 a 4), cada una con su cifra esperada de citas — 2, 6, 0, 4, 0, 11, 0, 14 y 0: cada cita textual aparece, literal, en su registro de `docs/verificacion/filosofia_ia/`, sin marcador de plantilla sin llenar, y cada fila de ese registro está marcada como verificada. Las cuatro páginas de discusión no citan, y su registro tiene que decir por qué no trae tabla |
| `test_skin.py` | Que `tokens.color.surface` de `skins/eva-cyberpunk.yaml` siga siendo `#211033`, el valor que `gen_ilustraciones.py`, `test_ilustraciones.py` y `test_aceptacion.py` tienen hardcodeado por triplicado |

## H16 — resuelto: `pytest tools/` ya corre en CI

`.github/workflows/pages.yml` tiene un job `checks` que instala `pillow
pyyaml pypdf pytest` y corre `python -m pytest tools/ -q` en cada push y PR. El job
`course-pages` (que delega en el workflow reutilizable de Raya para
`raya validate` + `raya build`) declara `needs: checks`, así que un fallo en
la suite bloquea el deploy en vez de correr en paralelo y publicarse de
todos modos. Esto se resolvió en el commit `47697d2` — las pruebas más caras
del proyecto (la que atrapó el bug de tamaño intrínseco en los SVG, la que
exige verificación por fila en vez de por archivo, y ahora las guardas del
cuadernillo de lecturas) ya no dependen de que alguien se acuerde de
correrlas a mano, aunque seguir corriéndolas en local antes de comitear
sigue siendo lo responsable.
