# §2 · Tu zip: dónde subirlo, encontrarlo (o armar el demo), revisarlo con la
# función literal de la tarea, verlo y partirlo 80/10/10 con semilla 0.
# Publica RUTA_ZIP, EJEMPLOS, PROMPTS, LEEME y DATOS (train/validation/test).

# %% [texto] s02-intro

# %% [codigo] s02-ruta
RUTA_ZIP = ""    # vacío: busca texto.zip; si no hay, arma el demo
# Si lo subiste a Drive, quita los # de estas dos líneas:
# from google.colab import drive; drive.mount("/content/drive")
# RUTA_ZIP = "/content/drive/MyDrive/texto.zip"
# O súbelo con un botón (detiene «Ejecutar todo» hasta que elijas):
# from google.colab import files; RUTA_ZIP = list(files.upload())[0]

import glob
import json
import zipfile

NB3 = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/"
       "main/course/10_deep_learning/_assets/03_finetuning_lora.ipynb")


def tipo_de_zip(ruta):
    """'texto', 'imagenes' o None, según lo que traiga en la raíz."""
    try:
        nombres = set(zipfile.ZipFile(ruta).namelist())
    except (zipfile.BadZipFile, OSError):
        return None
    if "datos.jsonl" in nombres:
        return "texto"
    return "imagenes" if "metadata.csv" in nombres else None


def buscar_zip():
    """El zip de texto que subiste: texto.zip, o cualquier .zip con
    datos.jsonl, en /content o en la carpeta actual."""
    carpetas = list(dict.fromkeys(["/content", os.getcwd()]))
    for c in carpetas:
        if os.path.exists(os.path.join(c, "texto.zip")):
            return os.path.join(c, "texto.zip")
    zips = [z for c in carpetas for z in sorted(glob.glob(f"{c}/*.zip"))
            if not z.endswith("texto_demo.zip")]
    for z in zips:
        if tipo_de_zip(z) == "texto":
            return z
    imagenes = [z for z in zips if tipo_de_zip(z) == "imagenes"]
    if imagenes:
        raise ValueError(
            f"{imagenes[0]} es un zip de IMÁGENES (trae metadata.csv).\n"
            f"Este notebook es de texto; las imágenes van en el notebook 3:\n"
            f"{NB3}")
    return None

# %% [codigo] s02-demo
def armar_demo(ruta, n):
    """Arma un texto.zip de demostración, en el formato de la tarea, con n
    ejemplos de b-mc2/sql-create-context (pregunta + tablas → SQL)."""
    from huggingface_hub import hf_hub_download
    archivo = hf_hub_download(DEMO, "sql_create_context_v4.json",
                              repo_type="dataset")
    with open(archivo, encoding="utf-8") as f:
        filas = random.Random(0).sample(json.load(f), n)
    datos = [{"prompt": f"Tablas: {e['context']}\nPregunta: {e['question']}",
              "completion": e["answer"]} for e in filas]
    # Cuatro prompts que no están en el dataset; «\n» es un salto de línea.
    prompts = [
        r"Tablas: CREATE TABLE students (name VARCHAR, age INTEGER)\n"
        r"Pregunta: How many students are older than 20?",
        r"Tablas: CREATE TABLE courses (id INTEGER, title VARCHAR, "
        r"credits INTEGER)\nPregunta: What is the title of course 7?",
        r"Tablas: CREATE TABLE songs (title VARCHAR, artist VARCHAR, "
        r"year INTEGER)\nPregunta: Which artists released songs in 1999?",
        r"Tablas: CREATE TABLE cities (name VARCHAR, country VARCHAR, "
        r"population INTEGER)\nPregunta: What is the total population of "
        r"cities in Mexico?"]
    leeme = (
        "# Mi dataset\n"
        "- **Qué quiero que aprenda el modelo:** escribir la consulta SQL "
        "que responde una pregunta sobre unas tablas\n"
        "- **Ruta:** texto\n"
        f"- **Fuente:** https://huggingface.co/datasets/{DEMO}\n"
        "- **Licencia:** CC BY 4.0\n"
        f"- **Cuántos ejemplos y cómo los elegí:** {n} al azar con semilla 0\n")
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("datos.jsonl", "".join(
            json.dumps(e, ensure_ascii=False) + "\n" for e in datos))
        z.writestr("prompts.txt", "\n".join(prompts) + "\n")
        z.writestr("LEEME.md", leeme)
    return ruta


if RUTA_ZIP:
    assert os.path.exists(RUTA_ZIP), f"no existe {RUTA_ZIP}: revisa la ruta"
else:
    RUTA_ZIP = buscar_zip()
    if RUTA_ZIP is None:
        print("No encontré tu texto.zip: armo el demo (texto → SQL).")
        RUTA_ZIP = armar_demo(os.path.join(os.getcwd(), "texto_demo.zip"),
                              P["n_demo"])
# El tipo se revisa ya resuelta la ruta, venga a mano o de la búsqueda.
if tipo_de_zip(RUTA_ZIP) == "imagenes":
    raise ValueError(f"{RUTA_ZIP} es un zip de IMÁGENES (trae metadata.csv).\n"
                     f"Este notebook es de texto; las imágenes van en el "
                     f"notebook 3:\n{NB3}")
ES_DEMO = RUTA_ZIP.endswith("texto_demo.zip")
print("Uso:", RUTA_ZIP, "(demo)" if ES_DEMO else "(tu zip)")

# %% [texto] s02-revisar-explica

# %% [codigo] s02-revisar
# La función de la tarea, copiada literal: dice OK o qué está mal.
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

revisar_zip(RUTA_ZIP)

# %% [codigo] s02-leer
_z = zipfile.ZipFile(RUTA_ZIP)
EJEMPLOS = [json.loads(l) for l in
            _z.read("datos.jsonl").decode("utf-8").splitlines() if l.strip()]
# En prompts.txt, «\n» escrito con dos caracteres es un salto de línea.
PROMPTS = [p.replace("\\n", "\n").strip() for p in
           _z.read("prompts.txt").decode("utf-8").split("\n") if p.strip()]
LEEME = _z.read("LEEME.md").decode("utf-8")
try:
    from IPython.display import Markdown
    display(Markdown(LEEME))
except ImportError:
    print(LEEME)

# %% [texto] s02-split-explica

# %% [codigo] s02-split
# 80 / 10 / 10 con semilla fija: siempre los mismos ejemplos en cada parte.
orden = np.random.default_rng(0).permutation(len(EJEMPLOS))
n_10 = max(1, round(0.1 * len(EJEMPLOS)))
DATOS = {"validation": [EJEMPLOS[i] for i in orden[:n_10]],
         "test": [EJEMPLOS[i] for i in orden[n_10:2 * n_10]],
         "train": [EJEMPLOS[i] for i in orden[2 * n_10:]]}
display(pd.Series({k: len(v) for k, v in DATOS.items()},
                  name="ejemplos").to_frame())

# %% [codigo] s02-muestra
# Solo train: el test no se mira (ni sus respuestas) hasta §08.
largos = pd.DataFrame({
    "prompt": [len(e["prompt"]) for e in DATOS["train"]],
    "completion": [len(e["completion"]) for e in DATOS["train"]]})
print(f"{len(EJEMPLOS)} ejemplos · {len(PROMPTS)} prompts de prueba · "
      "largos y muestra de train:")
display(largos.describe().loc[["mean", "50%", "max"]].round(0)
        .rename(index={"mean": "promedio (caracteres)",
                       "50%": "mediana", "max": "máximo"}))


def recorta(texto, n=300):
    return texto if len(texto) <= n else texto[:n] + " …"


muestra = random.Random(1).sample(DATOS["train"], 3)
mostrar(pd.DataFrame([{"prompt": recorta(e["prompt"]),
                       "completion": recorta(e["completion"])}
                      for e in muestra]))
