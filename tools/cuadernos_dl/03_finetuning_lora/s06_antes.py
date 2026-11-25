# Sección 6 · Antes de entrenar.
# El modelo base, sin adaptador, con el prompt del notebook y las semillas
# fijas de P["semillas"]: es la fila de referencia de todas las mallas.
# Produce IMGS_BASE_S06 (no entrena nada).

# %% [texto] s06-intro

# %% [codigo] s06-base
# Modelo base (nombre=None), una imagen por semilla. Las mismas semillas
# vuelven en s07 para que cada columna compare el mismo ruido inicial.
IMGS_BASE_S06 = generar(None, PROMPT, P["semillas"])
malla(IMGS_BASE_S06, filas=1,
      titulo=f"Modelo base · «{PROMPT}»",
      etiquetas=[f"semilla {s}" for s in P["semillas"]])

# %% [texto] s06-comparar

# %% [codigo] s06-prompts
# Dos prompts vecinos: uno sin «anime» y uno que pide el estilo con más
# detalle. Mismas semillas: solo cambia el texto.
PROMPTS_S06 = ["a face", "an anime face, colorful illustration, detailed"]
SEMILLAS_S06 = P["semillas"][:2]
imgs = generar(None, PROMPTS_S06, SEMILLAS_S06)       # orden prompt-mayor
malla(imgs, filas=len(PROMPTS_S06),
      titulo="Modelo base con dos prompts de comparación",
      etiquetas=[f"«{p}»" for p in PROMPTS_S06])     # una por fila
