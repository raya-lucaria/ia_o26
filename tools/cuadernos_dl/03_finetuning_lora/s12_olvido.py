# Notebook 03 · §12 · Olvido (o interferencia).
# Prompts fuera del dominio, mismas semillas, modelo base vs "lora_r8";
# malla y tabla de clip_score. Consume "lora_r8" de s07; no entrena nada.

# %% [texto] s12-intro

# %% [codigo] s12-olvido
import pandas as pd

PROMPTS_S12 = ["a photo of a dog", "a city street at night", "a bowl of fruit"]
SEM_S12 = P["semillas"][:3]
# Una imagen por (prompt, semilla), en orden prompt-mayor; misma semilla en
# las dos versiones: lo único que cambia es el adaptador.
base_s12 = generar(None, PROMPTS_S12, SEM_S12)
lora_s12 = generar("lora_r8", PROMPTS_S12, SEM_S12)

n = len(SEM_S12)
imgs, etiquetas, filas = [], [], []
for j, prompt in enumerate(PROMPTS_S12):
    b, l = base_s12[j * n:(j + 1) * n], lora_s12[j * n:(j + 1) * n]
    imgs += b + l
    etiquetas += [f"base · {prompt[:18]}"] * n + [f"lora_r8 · {prompt[:18]}"] * n
    filas.append({"prompt": prompt, "base": clip_score(b, prompt),
                  "lora_r8": clip_score(l, prompt)})
malla(imgs, filas=2 * len(PROMPTS_S12),
      titulo="fuera del dominio: base (fila de arriba) vs lora_r8 (abajo)",
      etiquetas=etiquetas)

# Referencia: el prompt del dominio, con las mismas semillas.
filas.append({"prompt": f"{PROMPT} (dominio)",
              "base": clip_score(generar(None, PROMPT, SEM_S12), PROMPT),
              "lora_r8": clip_score(generar("lora_r8", PROMPT, SEM_S12), PROMPT)})
tabla_s12 = pd.DataFrame(filas).set_index("prompt")
tabla_s12["lora_r8 − base"] = tabla_s12["lora_r8"] - tabla_s12["base"]
display(tabla_s12.round(3))

# %% [texto] s12-que-viste
