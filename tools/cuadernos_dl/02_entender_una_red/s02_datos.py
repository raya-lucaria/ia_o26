# §2 · Los datos: MNIST, split 50k/10k/10k, pruebas del split, muestra,
# distribución por dígito, subir a la GPU y normalizar, subconjuntos fijos.

# %% [texto] s02-intro

# %% [codigo] s02-descarga
# torchvision baja MNIST una vez; si ya está en la carpeta, no vuelve a bajarlo.
MNIST_DIR = os.environ.get("MNIST_DIR", "./datos_mnist")
mnist_train = torchvision.datasets.MNIST(MNIST_DIR, train=True, download=True)
mnist_test = torchvision.datasets.MNIST(MNIST_DIR, train=False, download=True)

# .data son las imágenes como enteros 0–255 [n, 28, 28]; .targets, los dígitos.
imagenes_60k, etiquetas_60k = mnist_train.data, mnist_train.targets
imagenes_test, etiquetas_test = mnist_test.data, mnist_test.targets

# El split: los primeros 50 000 de train son train; los últimos 10 000,
# validation. Guardamos los ÍNDICES de origen para poder verificar el split.
ORIGEN = {
    "train": torch.arange(0, 50_000),
    "validation": torch.arange(50_000, 60_000),
    "test": torch.arange(0, 10_000),  # índices dentro del archivo de test
}
CRUDOS = {
    "train": (imagenes_60k[ORIGEN["train"]], etiquetas_60k[ORIGEN["train"]]),
    "validation": (imagenes_60k[ORIGEN["validation"]],
                   etiquetas_60k[ORIGEN["validation"]]),
    "test": (imagenes_test, etiquetas_test),
}
for nombre, (imgs, etqs) in CRUDOS.items():
    print(f"{nombre:>10}: imágenes {tuple(imgs.shape)} {imgs.dtype}, "
          f"etiquetas {tuple(etqs.shape)} {etqs.dtype}")

# %% [texto] s02-pruebas-explica

# %% [codigo] s02-pruebas
# 1) Tamaños exactos.
assert len(CRUDOS["train"][0]) == 50_000
assert len(CRUDOS["validation"][0]) == 10_000
assert len(CRUDOS["test"][0]) == 10_000
# 2) Train y validation salen del mismo archivo: sus índices de origen
#    no pueden compartir ni uno.
comunes = set(ORIGEN["train"].tolist()) & set(ORIGEN["validation"].tolist())
assert len(comunes) == 0, "train y validation comparten índices"
print("✓ tamaños 50 000 / 10 000 / 10 000 y train ∩ validation = ∅ por índice")


# 3) Imágenes con píxeles idénticos (por hash). Se REPORTAN, no fallan:
#    MNIST trae unas pocas repetidas y no las vamos a limpiar aquí.
def huellas(imgs):
    """Un hash MD5 por imagen, de sus 784 bytes."""
    return [hashlib.md5(img.numpy().tobytes()).hexdigest() for img in imgs]


HUELLAS = {nombre: huellas(imgs) for nombre, (imgs, _) in CRUDOS.items()}
for nombre, hs in HUELLAS.items():
    repetidas = len(hs) - len(set(hs))
    print(f"dentro de {nombre:>10}: {repetidas} imágenes repetidas")
pares = [("train", "validation"), ("train", "test"), ("validation", "test")]
for a, b in pares:
    cruce = set(HUELLAS[a]) & set(HUELLAS[b])
    print(f"idénticas entre {a} y {b}: {len(cruce)}")

# %% [codigo] s02-por-digito
# 4) Proporción de cada dígito en los tres conjuntos: tabla y barras agrupadas.
POR_DIGITO = pd.DataFrame({
    nombre: pd.Series(etqs.numpy()).value_counts(normalize=True).sort_index()
    for nombre, (_, etqs) in CRUDOS.items()
})
POR_DIGITO.index.name = "dígito"
print((100 * POR_DIGITO).round(2).astype(str) + " %")

fig, ax = plt.subplots(figsize=(9, 3.5))
ancho = 0.27
for j, nombre in enumerate(POR_DIGITO.columns):
    ax.bar(POR_DIGITO.index + (j - 1) * ancho, 100 * POR_DIGITO[nombre],
           width=ancho, color=COLORES[nombre], label=nombre)
ax.axhline(10, color="gray", ls="--", lw=1, label="10 % (reparto parejo)")
ax.set_xticks(range(10))
ax.set_xlabel("dígito")
ax.set_ylabel("% del conjunto")
ax.set_title("Proporción de cada dígito en train, validation y test")
ax.legend(ncol=4, fontsize=8, loc="lower center")
plt.show()

# %% [texto] s02-muestra-explica

# %% [codigo] s02-muestra
# Las dos primeras imágenes de cada dígito en train, con su etiqueta.
imgs, etqs = CRUDOS["train"]
fig, ejes = plt.subplots(2, 10, figsize=(10, 2.4))
for d in range(10):
    cuales = torch.nonzero(etqs == d).flatten()[:2]
    for fila, i in enumerate(cuales.tolist()):
        ejes[fila, d].imshow(imgs[i], cmap="gray_r")
        ejes[fila, d].set_title(f"y = {d}", fontsize=8)
for ax in ejes.flat:
    ax.axis("off")
fig.suptitle("Muestra de train: 28 × 28 píxeles, de 0 (blanco) a 255 (negro)")
plt.show()
print("Una imagen es una matriz 28 × 28; la red la ve aplanada como 784 números:",
      tuple(imgs[0].flatten().shape))

# %% [texto] s02-gpu-explica

# %% [codigo] s02-gpu
def estratos(etiquetas, n, semilla=SEMILLA):
    """n índices que alternan los dígitos 0, 1, …, 9, 0, 1, … (≈ n/10 de cada
    uno), en un orden barajado con semilla fija: siempre los mismos."""
    g = torch.Generator().manual_seed(semilla)
    llave = torch.empty(len(etiquetas), dtype=torch.int64)
    for d in range(10):
        de_d = torch.nonzero(etiquetas == d).flatten()
        rango = torch.randperm(len(de_d), generator=g)
        llave[de_d[rango]] = torch.arange(len(de_d)) * 10 + d
    return torch.sort(torch.argsort(llave)[:n]).values


# Con RAPIDO nos quedamos con un pedazo estratificado: 3000 / 1000 / 1000.
if RAPIDO:
    tope = {"train": 3000, "validation": 1000, "test": 1000}
    CRUDOS = {k: (im[estratos(et, tope[k])], et[estratos(et, tope[k])])
              for k, (im, et) in CRUDOS.items()}
    print("RAPIDO: conjuntos recortados a", tope)

# Media y desviación estándar de los píxeles en [0, 1], calculadas SOLO en train.
x01_train = CRUDOS["train"][0].flatten(1).float() / 255
MEDIA, DESV = x01_train.mean().item(), x01_train.std().item()
print(f"MEDIA = {MEDIA:.4f}, DESV = {DESV:.4f} (de train)")

# DATOS[escala][conjunto] = (X [n, 784] float32, y [n] int64), ya en DEVICE.
DATOS = {"crudo": {}, "01": {}, "estandar": {}}
for nombre, (imgs, etqs) in CRUDOS.items():
    crudo = imgs.flatten(1).float()          # aplanar: [n, 28, 28] → [n, 784]
    y = etqs.long().to(DEVICE)
    DATOS["crudo"][nombre] = (crudo.to(DEVICE), y)
    DATOS["01"][nombre] = ((crudo / 255).to(DEVICE), y)
    DATOS["estandar"][nombre] = (((crudo / 255 - MEDIA) / DESV).to(DEVICE), y)

# Las imágenes de test en [0, 1], en CPU, alineadas con DATOS[...]["test"].
IMAGENES_TEST = CRUDOS["test"][0].float() / 255
for nombre in ("train", "validation", "test"):
    X, y = DATOS["estandar"][nombre]
    print(f"{nombre:>10}: X {tuple(X.shape)} en {X.device}, y {tuple(y.shape)}")
if DEVICE.type == "cuda":
    print(f"memoria de GPU ocupada: {torch.cuda.memory_allocated() / 2**20:.0f} MB")

# %% [texto] s02-subconjunto-explica

# %% [codigo] s02-subconjunto
def subconjunto(n, semilla=0):
    """Índices fijos de un subconjunto estratificado de DATOS[...]["train"]:
    ≈ n/10 por dígito, siempre los mismos para la misma semilla."""
    return estratos(DATOS["01"]["train"][1].cpu(), n, semilla)


idx = subconjunto(1000)
cuenta = torch.bincount(DATOS["01"]["train"][1].cpu()[idx], minlength=10)
print("subconjunto(1000), ejemplos por dígito:", cuenta.tolist())
assert torch.equal(idx, subconjunto(1000)), "el subconjunto no es determinista"

# %% [texto] s02-que-viste
