---
id: dl-tarea-dataset
title: "Tarea de la clase 3 · Trae tu dataset para hacer fine-tuning"
nav_title: Tarea · tu dataset
summary: "Para el lunes 30 de noviembre: cada quien trae un dataset propio de imágenes o de texto, empaquetado en un zip con un formato fijo, listo para subirlo al notebook de fine-tuning en Colab."
status: ready
estimated_time: 60m
tags: [deep-learning, tarea, fine-tuning, dataset]
---

# Tarea de la clase 3 · Trae tu dataset para hacer fine-tuning

> [!WARNING]
> **Tarea para el lunes 30 de noviembre. Es individual.** Trae a clase **un
> zip** con un dataset de **imágenes** o de **texto**, en el formato de esta
> página. Trae lo que puedas: solo hay mínimos, **50 imágenes** o **200
> ejemplos de texto**, y no hay tope de peso. En clase lo subes a un notebook de Colab y haces fine-tuning de un
> modelo preentrenado con tus datos, como en [[dl-clase-3-finetuning-lora|la clase 3]].
> Si el zip no sigue el formato, el notebook no lo lee y pierdes la clase
> arreglándolo. Antes de venir, revísalo con la función de la sección 5.

---

## 1 · Elige qué quieres enseñarle al modelo

Eliges **una** de dos rutas:

| Ruta | Modelo que vas a ajustar | Qué aprende | Ejemplos de idea |
|---|---|---|---|
| **Imágenes** | Stable Diffusion 1.5, el de la clase 3 | Un estilo o un tipo de objeto | mariposas, flores, acuarelas, tus dibujos, fotos de tu ciudad |
| **Texto** | Un LLM chico (de 0.5 a 1.5 mil millones de parámetros) | Responder de cierta forma a cierta entrada | problemas de matemáticas, texto → SQL, instrucciones en español, poemas |

La idea es la misma que en el notebook 3: ver **cuánto cambia** el modelo y
**qué aprende** de tus datos. Elige algo que se note a simple vista. Por
ejemplo, «acuarelas de gatos» se ve en una imagen; «fotos variadas de
internet» casi no cambia nada.

---

## 2 · El formato: qué va dentro del zip

Los archivos van **en la raíz del zip**, no dentro de una carpeta. No separes
train, validation y test: el notebook los separa con una semilla fija, en
80 %, 10 % y 10 %, y usa el test **una sola vez**, al final.

### Ruta imágenes: `imagenes.zip`

```text
imagenes.zip
├── metadata.csv      ← una fila por imagen: file_name,text
├── prompts.txt       ← de 3 a 5 prompts de prueba, uno por línea, en inglés
├── LEEME.md          ← la ficha de la sección 3
└── images/
    ├── 0000.jpg
    ├── 0001.jpg
    └── …
```

`metadata.csv` se ve así:

```text
file_name,text
images/0000.jpg,a photo of a butterfly specimen
images/0001.jpg,a photo of a butterfly specimen
```

- **Cuántas:** las que puedas, con un **mínimo de 50**. Más ayuda: entre 100 y 1,000 se nota bien el cambio.
- **Archivos:** JPG o PNG, en color, con el lado corto de al menos 512 px.
  El notebook las recorta al centro a 512 × 512, así que conviene que lo
  importante esté al centro.
- **`text`:** una descripción corta **en inglés**, porque el text encoder de
  Stable Diffusion es CLIP y está entrenado en inglés. Puede ser **la misma
  para todas**, como «an anime face» en el notebook 3.
- **Peso:** no hay tope. Si el zip pesa mucho, súbelo a tu Drive y móntalo en Colab en vez de subirlo desde el navegador.

### Ruta texto: `texto.zip`

```text
texto.zip
├── datos.jsonl       ← un ejemplo por línea: {"prompt": …, "completion": …}
├── prompts.txt       ← de 3 a 5 prompts de prueba, uno por línea
└── LEEME.md          ← la ficha de la sección 3
```

`datos.jsonl` lleva un objeto JSON por línea, con exactamente esas dos llaves:

```text
{"prompt": "Escribe la consulta SQL. Tabla: alumnos(nombre, edad). Pregunta: ¿cuántos alumnos tienen más de 20 años?", "completion": "SELECT COUNT(*) FROM alumnos WHERE edad > 20"}
{"prompt": "Escribe la consulta SQL. Tabla: cursos(id, nombre). Pregunta: ¿cómo se llama el curso 7?", "completion": "SELECT nombre FROM cursos WHERE id = 7"}
```

- **Cuántos:** los que puedas, con un **mínimo de 200**. Más ayuda: entre 500 y 5,000 se nota bien el cambio.
- **`prompt`:** la entrada que le das al modelo. **`completion`:** lo que
  quieres que conteste. El modelo aprende a producir el `completion` dado el
  `prompt`.
- **Largo:** que `prompt` y `completion` juntos no pasen de unos 2,000
  caracteres. Lo más largo se corta y esa parte no se aprende.
- **Idioma:** español o inglés, pero uno solo en todo el dataset.
- **Archivo:** UTF-8. No hay tope de peso.
- **Si solo quieres un estilo** (poemas, letras, tus mensajes): usa un
  `prompt` fijo, como «Escribe un poema:», y en `completion` pon el texto.

### `prompts.txt`, en las dos rutas

Son de 3 a 5 entradas que **no** están en el dataset. El notebook genera con
ellas antes y después del fine-tuning, para ver cuánto cambió el modelo. Si
la ruta es de imágenes, escríbelos en inglés.

---

## 3 · La ficha: `LEEME.md`

Copia esta plantilla y llénala. Son cinco líneas.

```markdown
# Mi dataset
- **Qué quiero que aprenda el modelo:** (una frase)
- **Ruta:** imágenes / texto
- **Fuente:** (el enlace al dataset de Hugging Face, o «propio»)
- **Licencia:** (la del dataset; si es propio, «propio»)
- **Cuántos ejemplos y cómo los elegí:** (p. ej. «300 al azar con semilla 0»)
```

---

## 4 · De dónde sacarlo

### Opción A · Un dataset de Hugging Face

Todos estos existen y son públicos. No hay que descargarlos completos: los
scripts de abajo toman solo una muestra.

**Imágenes**

| Dataset | Qué trae | Columnas | Texto |
|---|---|---|---|
| `huggan/smithsonian_butterflies_subset` | 1,000 fotos de mariposas de museo | `image` | fijo: `a photo of a butterfly specimen` |
| `huggan/flowers-102-categories` | 8,189 fotos de flores | `image` | fijo: `a photo of a flower` |
| `huggan/wikiart` | 11,320 pinturas, con artista, género y estilo | `image` | fijo; elige un solo estilo |
| `ComputerVisionAnimeProject/AnimeFaceColorization` | caras de anime, el dataset del notebook 3 | `image` | fijo: `an anime face` |

**Texto**

| Dataset | Qué trae | `prompt` ← | `completion` ← |
|---|---|---|---|
| `openai/gsm8k` (config `main`) | problemas de matemáticas con su razonamiento | `question` | `answer` |
| `b-mc2/sql-create-context` | pregunta y tabla → consulta SQL | `context` + `question` | `answer` |
| `bertin-project/alpaca-spanish` | instrucciones en español | `instruction` + `input` | `output` |
| `databricks/databricks-dolly-15k` | instrucciones en inglés, por categoría | `instruction` + `context` | `response` |
| `merve/poetry` | 573 poemas en inglés | fijo: `Write a poem:` | `content` |

Puedes usar cualquier otro dataset de Hugging Face: busca uno en
[huggingface.co/datasets](https://huggingface.co/datasets) y cambia las
primeras líneas del script.

**Script de imágenes.** Córrelo en Colab, que ya trae `datasets`:

```python
# ── Cambia solo estas líneas ───────────────────────────────────────
REPO = "huggan/smithsonian_butterflies_subset"   # el dataset en Hugging Face
COL_IMAGEN, COL_TEXTO = "image", None   # sus columnas (None: no trae texto)
TEXTO_FIJO = "a photo of a butterfly specimen"   # el mismo texto para todas
N = 300                                 # cuántas imágenes
# ───────────────────────────────────────────────────────────────────
import csv, os
from datasets import load_dataset

os.makedirs("imagenes/images", exist_ok=True)
datos = load_dataset(REPO, split="train", streaming=True)
datos = datos.shuffle(seed=0, buffer_size=1000).take(N)
with open("imagenes/metadata.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file_name", "text"])
    for i, ej in enumerate(datos):
        im = ej[COL_IMAGEN].convert("RGB")
        if min(im.size) > 512:                    # lado corto a 512 px
            k = 512 / min(im.size)
            im = im.resize((round(im.width * k), round(im.height * k)))
        ruta = f"images/{i:04d}.jpg"
        im.save(f"imagenes/{ruta}", quality=90)
        w.writerow([ruta, TEXTO_FIJO or ej[COL_TEXTO]])
```

**Script de texto.** Solo cambia `REPO`, `CONFIG` y la función `a_ejemplo`:

```python
# ── Cambia solo estas líneas ───────────────────────────────────────
REPO, CONFIG = "openai/gsm8k", "main"   # CONFIG = None si no tiene
N = 1000

def a_ejemplo(ej):                      # una fila → prompt y completion
    return {"prompt": ej["question"], "completion": ej["answer"]}
# ───────────────────────────────────────────────────────────────────
import json, os
from datasets import load_dataset

os.makedirs("texto", exist_ok=True)
datos = load_dataset(REPO, CONFIG, split="train", streaming=True)
datos = datos.shuffle(seed=0, buffer_size=5000).take(N)
with open("texto/datos.jsonl", "w", encoding="utf-8") as f:
    for ej in datos:
        f.write(json.dumps(a_ejemplo(ej), ensure_ascii=False) + "\n")
```

Para `b-mc2/sql-create-context`, por ejemplo, la función queda así:

```python
def a_ejemplo(ej):
    return {"prompt": f"Tablas: {ej['context']}\nPregunta: {ej['question']}",
            "completion": ej["answer"]}
```

### Opción B · Datos tuyos

También puedes traer datos propios: tus dibujos, tus fotos, tus apuntes, las
letras de una banda o el reglamento de algo. El formato es el mismo. Con
imágenes, pon tus archivos en una carpeta `mis_imagenes/` y súbela a Colab.
En el script de imágenes deja `COL_IMAGEN = "image"`, escribe tu
`TEXTO_FIJO` y cambia las dos líneas que empiezan con `datos =` por estas:

```python
from pathlib import Path
from PIL import Image
EXT = {".jpg", ".jpeg", ".png", ".webp"}
datos = [{"image": Image.open(p)} for p in sorted(Path("mis_imagenes").iterdir())
         if p.suffix.lower() in EXT]
```

Con texto, cualquier forma de llegar a `datos.jsonl`
sirve. Una hoja de cálculo con columnas `prompt` y `completion`, exportada a
CSV, se convierte así:

```python
import pandas as pd
pd.read_csv("mis_datos.csv").to_json("texto/datos.jsonl", orient="records",
                                     lines=True, force_ascii=False)
```

**Lo que no se vale:**

- fotos de personas reales sin su permiso, ni datos personales de nadie;
- contenido sexual o violento;
- material cuya licencia no puedas escribir en la ficha.

---

## 5 · Empaquetar y revisar

Escribe a mano `prompts.txt` y `LEEME.md` dentro de la carpeta (`imagenes/`
o `texto/`). Después empaqueta y descarga:

```python
import shutil
from google.colab import files
shutil.make_archive("imagenes", "zip", "imagenes")   # o "texto", "zip", "texto"
files.download("imagenes.zip")                       # o "texto.zip"
```

`make_archive` deja los archivos en la raíz del zip. Si comprimes en tu
computadora, selecciona **los archivos**, no la carpeta.

Antes de venir, revisa el zip con esta función. No cambia nada: solo dice
`OK` o qué está mal.

```python
import csv, io, json, zipfile
from PIL import Image

def revisar_zip(ruta):
    """Dice si el zip sigue el formato de la tarea. No cambia nada."""
    z = zipfile.ZipFile(ruta)
    nombres = set(z.namelist())
    faltan = {"prompts.txt", "LEEME.md"} - nombres
    assert not faltan, f"faltan en la raíz del zip: {sorted(faltan)}"
    prompts = z.read("prompts.txt").decode("utf-8").split("\n")
    prompts = [p for p in prompts if p.strip()]
    assert 3 <= len(prompts) <= 5, f"prompts.txt: {len(prompts)} prompts, van de 3 a 5"
    if "metadata.csv" in nombres:                     # imágenes
        filas = list(csv.DictReader(io.StringIO(z.read("metadata.csv").decode("utf-8"))))
        assert filas and set(filas[0]) == {"file_name", "text"}, "columnas: file_name,text"
        assert len(filas) >= 50, f"solo {len(filas)} imágenes; mínimo 50"
        for fila in filas:
            assert fila["file_name"] in nombres, f"no está {fila['file_name']}"
            assert fila["text"].strip(), f"{fila['file_name']} sin texto"
            Image.open(z.open(fila["file_name"])).verify()
        print(f"OK · imágenes: {len(filas)} · prompts: {len(prompts)}")
    elif "datos.jsonl" in nombres:                    # texto
        lineas = z.read("datos.jsonl").decode("utf-8").splitlines()
        ejemplos = [json.loads(l) for l in lineas if l.strip()]
        assert len(ejemplos) >= 200, f"solo {len(ejemplos)} ejemplos; mínimo 200"
        for i, ej in enumerate(ejemplos, 1):
            assert set(ej) == {"prompt", "completion"}, f"línea {i}: llaves {sorted(ej)}"
            assert ej["completion"].strip(), f"línea {i}: completion vacío"
        print(f"OK · ejemplos: {len(ejemplos)} · prompts: {len(prompts)}")
    else:
        raise AssertionError("falta metadata.csv (imágenes) o datos.jsonl (texto)")

revisar_zip("imagenes.zip")   # o "texto.zip"
```

---

**Punto de control:** llegas a clase con el zip en tu computadora o en tu
Drive, `revisar_zip` imprime `OK`, y puedes decir en una frase qué quieres
que aprenda el modelo.
