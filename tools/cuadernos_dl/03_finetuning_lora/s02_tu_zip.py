# §2 · Tu zip: dónde subirlo, buscarlo, el demo si no hay, revisar_zip
# (copia literal de la página de la tarea), cargar y partir 80 / 10 / 10.
# Define RUTA_ZIP, ES_DEMO, PROMPTS, LEEME, IMGS y TEXTOS = {"train",
# "validation", "test"} (listas paralelas de PIL RGB de P["res"] px y de
# captions) y malla().

# %% [texto] s02-intro

# %% [codigo] s02-buscar
RUTA_ZIP = ""   # vacío: lo busco yo. O escribe la ruta, p. ej.
#                 "/content/drive/MyDrive/imagenes.zip"

# Alternativas (quita el # de la que quieras usar):
# from google.colab import files; files.upload()                 # un botón
# from google.colab import drive; drive.mount("/content/drive")  # tu Drive

from pathlib import Path

NB4 = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/"
       "main/course/10_deep_learning/_assets/04_finetuning_llm.ipynb")


def buscar(patron):
    """Zips que coinciden con `patron` en /content y en la carpeta actual,
    del más reciente al más viejo."""
    vistos = {p.resolve() for c in (Path("/content"), Path.cwd())
              if c.is_dir() for p in c.glob(patron) if p.is_file()}
    return sorted(vistos, key=lambda p: p.stat().st_mtime, reverse=True)


if RUTA_ZIP:
    if not Path(RUTA_ZIP).is_file():
        raise FileNotFoundError(f"No existe {RUTA_ZIP!r}. Revisa la ruta en el "
                                "panel 📁 (clic derecho → Copiar ruta).")
elif buscar("imagenes*.zip"):          # «imagenes (1).zip» también cuenta
    RUTA_ZIP = str(buscar("imagenes*.zip")[0])
elif buscar("texto*.zip"):
    raise ValueError(
        f"Encontré {buscar('texto*.zip')[0].name}: es un dataset de TEXTO. "
        f"Este notebook es el de imágenes. Abre el notebook 4:\n{NB4}")
ES_DEMO = not RUTA_ZIP
if ES_DEMO:
    otros = [p.name for p in buscar("*.zip")]
    if otros:
        print("Hay estos zip, pero ninguno se llama imagenes*.zip:", otros)
        print("Si uno es el tuyo, escribe su ruta en RUTA_ZIP y corre de nuevo.")
    print("No encontré tu imagenes.zip: uso el dataset DEMO (caras de anime).")
else:
    print("Uso tu zip:", RUTA_ZIP)

# %% [texto] s02-demo-explica

# %% [codigo] s02-demo
import csv
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw

DATASET_DEMO = "ComputerVisionAnimeProject/AnimeFaceColorization"
REV_DEMO = "e8deff76ecee132a5eead1b03941789ba60098fa"   # versión fija
PROMPTS_DEMO = ["an anime face with short green hair",
                "an anime face wearing glasses",
                "an anime face, smiling, red eyes",
                "an anime face of an old man"]


def caras_reales():
    """N caras por personaje, personajes y caras elegidos con semilla 0."""
    from huggingface_hub import HfApi, hf_hub_download
    api = HfApi()

    def listar(carpeta):
        return [x.path for x in api.list_repo_tree(
            DATASET_DEMO, repo_type="dataset", path_in_repo=carpeta,
            revision=REV_DEMO)]

    def bajar(ruta):
        return Image.open(hf_hub_download(
            DATASET_DEMO, ruta, repo_type="dataset", revision=REV_DEMO))

    # Solo las carpetas reference/NNN_<personaje>: son las caras.
    personajes = sorted(r for r in listar("reference")
                        if re.match(r"^\d{3}_", r.split("/")[-1]))
    azar = random.Random(0)
    elegidos = sorted(azar.sample(personajes, P["demo_personajes"]))
    with ThreadPoolExecutor(16) as pool:
        rutas = []
        for lista in pool.map(listar, elegidos):
            pngs = sorted(r for r in lista if r.endswith(".png"))
            rutas += azar.sample(pngs, min(len(pngs), P["demo_por_personaje"]))
        return [im.convert("RGB") for im in pool.map(bajar, rutas)]


def caras_de_juguete(n=50):
    """Para la prueba en CPU: óvalos de colores, sin descargar nada."""
    azar, salida = random.Random(0), []
    for _ in range(n):
        im = Image.new("RGB", (64, 64), tuple(azar.choices(range(256), k=3)))
        ImageDraw.Draw(im).ellipse((12, 8, 52, 58),
                                   fill=tuple(azar.choices(range(256), k=3)))
        salida.append(im)
    return salida

# %% [codigo] s02-demo-armar
def armar_demo(carpeta=Path("demo/imagenes")):
    """Escribe el demo en el formato de la tarea y lo empaqueta en un zip."""
    shutil.rmtree(carpeta, ignore_errors=True)
    (carpeta / "images").mkdir(parents=True)
    caras = caras_de_juguete() if RAPIDO else caras_reales()
    with open(carpeta / "metadata.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file_name", "text"])
        for i, im in enumerate(caras):
            im.save(carpeta / f"images/{i:04d}.jpg", quality=95)
            w.writerow([f"images/{i:04d}.jpg", "an anime face"])
    (carpeta / "prompts.txt").write_text("\n".join(PROMPTS_DEMO) + "\n",
                                         encoding="utf-8")
    (carpeta / "LEEME.md").write_text(
        "# Dataset demo\n"
        "- **Qué quiero que aprenda el modelo:** el estilo «cara de anime»\n"
        "- **Ruta:** imágenes\n"
        f"- **Fuente:** https://huggingface.co/datasets/{DATASET_DEMO}\n"
        "- **Licencia:** CC-BY-4.0 (las caras son de personajes con derechos"
        " de sus autores; solo para estudiar el método)\n"
        f"- **Cuántos ejemplos y cómo los elegí:** {len(caras)} caras, "
        "personajes y caras al azar con semilla 0\n", encoding="utf-8")
    return shutil.make_archive(str(carpeta), "zip", carpeta)


if ES_DEMO:
    RUTA_ZIP = armar_demo()
    print("Demo armado en", RUTA_ZIP)
else:
    print("(tienes tu zip: no hace falta el demo)")

# %% [texto] s02-revisar-explica

# %% [codigo] s02-revisar-funcion
# Copia literal de la página de la tarea (sección 5).
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

# %% [codigo] s02-revisar
try:
    with zipfile.ZipFile(RUTA_ZIP) as z:
        NOMBRES_ZIP = z.namelist()
except zipfile.BadZipFile:
    raise ValueError(f"{RUTA_ZIP} no es un zip válido: vuelve a empaquetarlo "
                     "(página de la tarea, sección 5).") from None
if "metadata.csv" not in NOMBRES_ZIP and "datos.jsonl" in NOMBRES_ZIP:
    raise ValueError("Este zip es un dataset de TEXTO (trae datos.jsonl). "
                     f"Este notebook es el de imágenes. Abre el notebook 4:\n{NB4}")
try:
    revisar_zip(RUTA_ZIP)
except AssertionError as e:
    pista = ""
    if any(n.endswith("/metadata.csv") for n in NOMBRES_ZIP):
        pista = ("\nPista: metadata.csv está dentro de una carpeta. Comprime "
                 "los archivos, no la carpeta.")
    raise ValueError(f"Tu zip no sigue el formato de la tarea: {e}{pista}\n"
                     "Corrígelo con la página de la tarea (secciones 2 y 5) "
                     "y vuelve a subirlo.") from None

# %% [texto] s02-cargar-explica

# %% [codigo] s02-cargar
import tempfile

from PIL import ImageOps

# Una carpeta temporal NUEVA en cada corrida: nunca es la de tu zip.
CARPETA_ZIP = Path(tempfile.mkdtemp(prefix="datos_zip_"))
with zipfile.ZipFile(RUTA_ZIP) as z:
    FILAS = list(csv.DictReader(io.StringIO(
        z.read("metadata.csv").decode("utf-8"))))
    PROMPTS = [p.strip() for p in z.read("prompts.txt").decode("utf-8")
               .split("\n") if p.strip()]
    LEEME = z.read("LEEME.md").decode("utf-8")
    if len(FILAS) > P["max_imagenes"]:
        print(f"Tu zip trae {len(FILAS)} imágenes; tomo {P['max_imagenes']} "
              "al azar con semilla 0 (P['max_imagenes']).")
        FILAS = random.Random(0).sample(FILAS, P["max_imagenes"])
    for fila in FILAS:                 # solo las imágenes de la muestra
        z.extract(fila["file_name"], CARPETA_ZIP)


def abrir(fila):
    """Abre, endereza (EXIF), recorta al centro y deja a P["res"] px."""
    im = Image.open(CARPETA_ZIP / fila["file_name"])
    im.draft("RGB", (P["res"], P["res"]))   # un JPEG enorme se lee ya reducido
    im = ImageOps.exif_transpose(im).convert("RGB")
    lado = min(im.size)
    return ImageOps.fit(im, (P["res"], P["res"]), Image.BICUBIC), lado


with ThreadPoolExecutor(8) as pool:
    ABIERTAS = list(pool.map(abrir, FILAS))
shutil.rmtree(CARPETA_ZIP, ignore_errors=True)   # ya están en memoria
chicas = sum(lado < 512 for _, lado in ABIERTAS)
print(f"{len(ABIERTAS)} imágenes cargadas de {RUTA_ZIP}")
if chicas and not RAPIDO:
    print(f"Ojo: {chicas} imágenes tienen el lado corto < 512 px; se agrandan "
          "y quedan más suaves. El modelo también aprende esa suavidad.")

# %% [codigo] s02-partir
def dhash(im):
    """Huella perceptual de 64 bits: ¿cada pixel de una miniatura 9×8 en
    grises es más claro que su vecino de la derecha? Sobrevive a JPEG."""
    g = np.asarray(im.convert("L").resize((9, 8), Image.BILINEAR), np.int16)
    return int("".join("1" if b else "0" for b in (g[:, 1:] > g[:, :-1]).flat), 2)


# Duplicados visuales: huellas a distancia de Hamming ≤ 4 van al mismo grupo
# (union-find), y cada grupo completo va a UN solo split. Así una copia en
# train y otra en test no hacen que test premie memorizar.
huellas = [dhash(im) for im, _ in ABIERTAS]
padre = list(range(len(huellas)))


def raiz(i):
    while padre[i] != i:
        padre[i] = padre[padre[i]]
        i = padre[i]
    return i


for i in range(len(huellas)):
    for j in range(i + 1, len(huellas)):
        if (huellas[i] ^ huellas[j]).bit_count() <= 4:
            padre[raiz(j)] = raiz(i)
GRUPOS = {}
for i in range(len(huellas)):
    GRUPOS.setdefault(raiz(i), []).append(i)
GRUPOS = list(GRUPOS.values())

# Partición ≈ 80 / 10 / 10 por grupos, con semilla 0.
random.Random(0).shuffle(GRUPOS)
meta = max(1, round(0.1 * len(ABIERTAS)))
PARTES = {"validation": [], "test": [], "train": []}
for grupo in GRUPOS:
    destino = next(k for k in ("validation", "test", "train")
                   if k == "train" or len(PARTES[k]) < meta)
    PARTES[destino] += grupo
vacios = [k for k, v in PARTES.items() if not v]
if vacios:
    raise ValueError(
        f"Tu zip tiene {len(FILAS)} filas pero solo {len(GRUPOS)} imágenes "
        f"distintas (las demás son copias casi idénticas): no alcanzan para "
        f"{', '.join(vacios)}. Trae al menos 50 imágenes DISTINTAS.")
if len(GRUPOS) < 50:
    print(f"Ojo: solo {len(GRUPOS)} imágenes distintas; el mínimo de la "
          "tarea son 50 y las métricas serán muy ruidosas.")
IMGS = {k: [ABIERTAS[i][0] for i in PARTES[k]] for k in ("train", "validation",
                                                          "test")}
TEXTOS = {k: [FILAS[i]["text"].strip() for i in PARTES[k]] for k in IMGS}
display(pd.DataFrame({k: {"imágenes": len(v),
                          "captions distintos": len(set(TEXTOS[k]))}
                      for k, v in IMGS.items()}))
print(f"{len(GRUPOS)} imágenes distintas; "
      f"{len(ABIERTAS) - len(GRUPOS)} son copias casi idénticas de otra "
      "(se quedan, pero siempre en el mismo split que su original)")

# %% [texto] s02-muestra-explica

# %% [codigo] s02-muestra
import math
import textwrap


def malla(imagenes, filas, titulo, etiquetas=None):
    """Malla de imágenes (≤ 256 px). etiquetas: una por imagen (título
    chico) o una por fila (a la izquierda)."""
    n = len(imagenes)
    cols = max(1, math.ceil(n / filas))
    fig, ejes = plt.subplots(filas, cols, figsize=(1.9 * cols, 2.0 * filas),
                             squeeze=False, dpi=80)
    for i, eje in enumerate(ejes.flat):
        eje.axis("off")
        if i >= n:
            continue
        im = imagenes[i].copy()
        im.thumbnail((256, 256))
        eje.imshow(im)
        if etiquetas is not None and len(etiquetas) == n:
            eje.set_title(textwrap.shorten(etiquetas[i], 28), fontsize=7)
    if etiquetas is not None and len(etiquetas) == filas and filas != n:
        for f in range(filas):
            ejes[f, 0].text(-0.05, 0.5, textwrap.fill(etiquetas[f], 22),
                            fontsize=8, ha="right", va="center",
                            transform=ejes[f, 0].transAxes)
    fig.suptitle(titulo, fontsize=10)
    plt.tight_layout()
    plt.show()


k = min(8, len(IMGS["train"]))
malla(IMGS["train"][:k], filas=1 if k <= 4 else 2,
      titulo=f"Imágenes de train (de {len(IMGS['train'])}), con su caption",
      etiquetas=TEXTOS["train"][:k])
print("Tus prompts de prueba (prompts.txt):")
for p in PROMPTS:
    print("  ·", p)
print("\nTu ficha (LEEME.md):\n" + LEEME)
