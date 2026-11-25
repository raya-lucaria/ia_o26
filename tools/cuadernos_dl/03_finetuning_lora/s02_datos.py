# §2 · Datos: caras de anime (moeimouto) de AnimeFaceColorization.
# Define DATOS = {"train", "validation", "test"} (listas de PIL RGB de
# P["res"] px) y CONTROL = las primeras caras de train (para s11).

# %% [texto] s02-intro

# %% [codigo] s02-manifiesto
import re
from concurrent.futures import ThreadPoolExecutor

from huggingface_hub import HfApi, hf_hub_download

# Versión del dataset fijada por commit: mismas caras en cada corrida.
REV_DATOS = "e8deff76ecee132a5eead1b03941789ba60098fa"
API = HfApi()


def listar(carpeta):
    """Rutas dentro de una carpeta del dataset (la API pagina sola)."""
    return [x.path for x in API.list_repo_tree(
        DATASET, repo_type="dataset", path_in_repo=carpeta, revision=REV_DATOS)]


# Solo las carpetas reference/NNN_<personaje>; AnimeDiffusion_* no son caras.
CARPETAS = sorted(r for r in listar("reference")
                  if re.match(r"^\d{3}_", r.split("/")[-1]))
azar = random.Random(0)
ELEGIDOS = sorted(azar.sample(CARPETAS, P["n_personajes"]))
with ThreadPoolExecutor(16) as pool:
    ARCHIVOS = dict(zip(ELEGIDOS, pool.map(listar, ELEGIDOS)))

# Manifiesto explícito: N caras por personaje, elegidas con semilla.
# Pedimos 4 de más por si la deduplicación descarta alguna.
MANIFIESTO = {}
for carpeta, rutas in ARCHIVOS.items():
    pngs = sorted(r for r in rutas if r.endswith(".png"))
    MANIFIESTO[carpeta] = azar.sample(pngs, min(len(pngs),
                                                P["n_por_personaje"] + 4))
print(f"{len(CARPETAS)} personajes en el dataset; usamos {len(ELEGIDOS)}:")
print(", ".join(c.split("/")[-1][4:] for c in ELEGIDOS))

# %% [codigo] s02-descargar
import hashlib

from PIL import Image


def bajar(ruta):
    """Descarga una cara (≈ 100 KB) y la abre como RGB."""
    local = hf_hub_download(DATASET, ruta, repo_type="dataset",
                            revision=REV_DATOS)
    return Image.open(local).convert("RGB")


def huella(img):
    """Hash de la imagen reducida a 16×16: detecta duplicados casi exactos."""
    return hashlib.md5(img.resize((16, 16), Image.BILINEAR).tobytes()).hexdigest()


todas = [r for rutas in MANIFIESTO.values() for r in rutas]
with ThreadPoolExecutor(16) as pool:
    IMAGENES = dict(zip(todas, pool.map(bajar, todas)))

# Deduplicar ANTES de partir: una cara repetida en train y en test
# haría que test premie memorizar.
vistas, DATOS = set(), {"train": [], "validation": [], "test": []}
filas, duplicadas = [], 0
for carpeta, rutas in MANIFIESTO.items():
    caras = []
    for r in rutas:
        h = huella(IMAGENES[r])
        if h in vistas:
            duplicadas += 1
            continue
        vistas.add(h)
        caras.append(IMAGENES[r])
    caras = caras[:P["n_por_personaje"]]
    # Partición por imagen DENTRO de cada personaje: 80 / 10 / 10.
    n_val = n_test = max(1, round(0.1 * len(caras)))
    partes = {"train": caras[n_val + n_test:], "validation": caras[:n_val],
              "test": caras[n_val:n_val + n_test]}
    for nombre, lista in partes.items():
        # 252 px → P["res"] con interpolación bicúbica.
        DATOS[nombre] += [im.resize((P["res"], P["res"]), Image.BICUBIC)
                          for im in lista]
    filas.append({"personaje": carpeta.split("/")[-1][4:],
                  **{k: len(v) for k, v in partes.items()}})

random.Random(0).shuffle(DATOS["train"])    # mezcla los personajes
CONTROL = DATOS["train"][:2 if RAPIDO else 16]
conteo = pd.DataFrame(filas).set_index("personaje")
conteo.loc["total"] = conteo.sum()
display(conteo)
print(f"duplicadas descartadas: {duplicadas} · CONTROL: {len(CONTROL)} caras"
      f" · tamaño original {IMAGENES[todas[0]].size} → {DATOS['train'][0].size}")

# %% [texto] s02-tira-explica

# %% [codigo] s02-tira
# Tira de 8 caras reales de train, a 128 px: la única vez que se muestran.
tira = DATOS["train"][:8]
fig, ejes = plt.subplots(1, len(tira), figsize=(1.6 * len(tira), 1.9))
for ax, img in zip(np.atleast_1d(ejes), tira):
    ax.imshow(img.resize((128, 128), Image.BICUBIC))
    ax.axis("off")
fig.suptitle(f"Caras reales de train (de {len(DATOS['train'])})", fontsize=10)
fig.tight_layout()
plt.show()
