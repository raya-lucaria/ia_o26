# §7 · Métricas, explicadas y medidas en VALIDATION (base vs LoRA).
# Define CLIP, emb_imagenes, emb_textos, clip_score, generadas, m_loss,
# m_clip, m_estilo, m_memoria, PROMPTS_AJENOS, m_olvido y resumen; s08 las
# reusa tal cual sobre test.

# %% [texto] s07-intro

# %% [codigo] s07-clip
from transformers import CLIPModel, CLIPProcessor

CLIP = CLIPModel.from_pretrained(MODELO_CLIP).to(DEVICE).eval()
PROC = CLIPProcessor.from_pretrained(MODELO_CLIP)


def _vector(salida):
    """get_*_features devuelve un tensor o (versiones nuevas) un objeto."""
    if torch.is_tensor(salida):
        return salida
    for campo in ("image_embeds", "text_embeds", "pooler_output"):
        if getattr(salida, campo, None) is not None:
            return getattr(salida, campo)
    raise TypeError(type(salida))


@torch.no_grad()
def emb_imagenes(imgs):
    """(N, D) con norma 1: el coseno entre dos imágenes es su producto punto."""
    out = []
    for i in range(0, len(imgs), 32):
        x = PROC(images=imgs[i:i + 32], return_tensors="pt").to(DEVICE)
        out.append(_vector(CLIP.get_image_features(**x)).float().cpu())
    return F.normalize(torch.cat(out), dim=-1)


@torch.no_grad()
def emb_textos(textos):
    x = PROC(text=list(textos), return_tensors="pt", padding=True,
             truncation=True, max_length=77).to(DEVICE)
    return F.normalize(_vector(CLIP.get_text_features(**x)).float().cpu(), dim=-1)


def clip_score(imgs, textos, emb=None):
    """100 · coseno(imagen_i, texto_i), promediado sobre las parejas."""
    emb = emb_imagenes(imgs) if emb is None else emb
    return float(100 * (emb * emb_textos(textos)).sum(-1).mean())


def generadas(conjunto, semilla0):
    """P["n_gen"] imágenes con los captions de `conjunto` (en ciclo), base y
    LoRA con las MISMAS parejas (caption, semilla), y sus embeddings CLIP."""
    textos = TEXTOS[conjunto]
    pares = [(textos[i % len(textos)], semilla0 + i) for i in range(P["n_gen"])]
    gen = {"textos": [t for t, _ in pares], "emb": {}}
    for k, lora in (("base", False), ("LoRA", True)):
        gen[k] = generar(pares, lora=lora)
        gen["emb"][k] = emb_imagenes(gen[k])
    return gen


EMB_TRAIN = emb_imagenes(IMGS["train"])        # para estilo y memorización
GEN_VAL = generadas("validation", 1000)
print(f"{P['n_gen']} imágenes de validation generadas con el base y con LoRA")

# %% [texto] s07-loss-explica

# %% [codigo] s07-loss
def m_loss(conjunto):
    """Loss de difusión con (t, ε) fijos, sin y con el adaptador."""
    return {"base": perdida(conjunto, lora=False),
            "LoRA": perdida(conjunto, lora=True)}


VAL = {"loss de difusión": m_loss("validation")}
print(pd.Series(VAL["loss de difusión"]).round(4).to_string())

# %% [texto] s07-clipscore-explica

# %% [codigo] s07-clipscore
def m_clip(gen):
    return {k: clip_score(None, gen["textos"], gen["emb"][k])
            for k in ("base", "LoRA")}


VAL["CLIP score"] = m_clip(GEN_VAL)
print(pd.Series(VAL["CLIP score"]).round(2).to_string())

# %% [texto] s07-estilo-explica

# %% [codigo] s07-estilo
def m_estilo(conjunto, gen):
    """Coseno medio entre las generadas y el centroide CLIP de las reales
    de `conjunto`. Referencia: las reales de train contra ese centroide."""
    centro = F.normalize(emb_imagenes(IMGS[conjunto]).mean(0), dim=-1)
    salida = {k: float((gen["emb"][k] @ centro).mean()) for k in ("base", "LoRA")}
    salida["referencia"] = float((EMB_TRAIN @ centro).mean())
    return salida


VAL["parecido al estilo"] = m_estilo("validation", GEN_VAL)
print(pd.Series(VAL["parecido al estilo"]).round(3).to_string())

# %% [texto] s07-memoria-explica

# %% [codigo] s07-memoria
def vecino(emb):
    """Coseno CLIP del vecino más cercano en train, para cada fila."""
    return (emb @ EMB_TRAIN.T).max(dim=1).values


def m_memoria(conjunto, gen):
    """Media del coseno al vecino de train: generadas (base, LoRA) y, como
    referencia, imágenes reales de `conjunto` que el modelo nunca vio."""
    salida = {k: float(vecino(gen["emb"][k]).mean()) for k in ("base", "LoRA")}
    salida["referencia"] = float(vecino(emb_imagenes(IMGS[conjunto])).mean())
    return salida


VAL["vecino en train"] = m_memoria("validation", GEN_VAL)
print(pd.Series(VAL["vecino en train"]).round(3).to_string())

# %% [texto] s07-olvido-explica

# %% [codigo] s07-olvido
# Prompts que no tienen nada que ver con el dataset demo. Si tu dataset ES
# de perros, ciudades o fruta, cambia esta lista por otros temas ajenos.
PROMPTS_AJENOS = ["a photo of a dog", "a city street at night",
                  "a bowl of fruit"]


def m_olvido(semillas):
    """CLIP score de cada prompt ajeno, base vs LoRA, mismas semillas.
    Devuelve la tabla por prompt y las imágenes (prompt por prompt)."""
    pares = combinar(PROMPTS_AJENOS, semillas)
    imgs = {"base": generar(pares, lora=False), "LoRA": generar(pares, lora=True)}
    n, filas = len(semillas), []
    for j, prompt in enumerate(PROMPTS_AJENOS):
        filas.append({"prompt": prompt, **{
            k: clip_score(v[j * n:(j + 1) * n], [prompt] * n)
            for k, v in imgs.items()}})
    return pd.DataFrame(filas).set_index("prompt"), imgs


OLVIDO_VAL, _ = m_olvido(P["semillas"])
VAL["olvido"] = OLVIDO_VAL.mean().to_dict()
display(OLVIDO_VAL.assign(**{"LoRA − base": OLVIDO_VAL["LoRA"] -
                             OLVIDO_VAL["base"]}).round(2))

# %% [texto] s07-resumen-explica

# %% [codigo] s07-resumen
BUENO = {"loss de difusión": "más baja",
         "CLIP score": "alto; que LoRA no caiga mucho",
         "parecido al estilo": "LoRA más alto que base",
         "vecino en train": "cerca de la referencia",
         "olvido": "LoRA ≈ base"}


def resumen(medidas):
    """Una fila por métrica: base, LoRA, referencia y qué es bueno."""
    tabla = pd.DataFrame(medidas).T.reindex(columns=["base", "LoRA",
                                                     "referencia"])
    tabla["LoRA − base"] = tabla["LoRA"] - tabla["base"]
    tabla["qué es bueno"] = pd.Series(BUENO)
    return tabla


display(resumen(VAL).style.format(
    {c: "{:.4f}" for c in ("base", "LoRA", "referencia", "LoRA − base")},
    na_rep="—").set_caption("VALIDATION · base vs LoRA"))
k = min(4, len(IMGS["validation"]), P["n_gen"])
malla(IMGS["validation"][:k] + GEN_VAL["base"][:k] + GEN_VAL["LoRA"][:k],
      filas=3, titulo="validation · real / base / LoRA (mismo caption y semilla)",
      etiquetas=["real", "base", "LoRA"])
