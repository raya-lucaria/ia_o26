# §3 · Antes: el modelo base, sin entrenar, contesta prompts.txt y tres
# ejemplos de validation. Publica TOK, LM, formatear, generar, respuestas,
# liberar y BASE_PROMPTS (las respuestas del base, para comparar en §08).

# %% [texto] s03-intro

# %% [codigo] s03-cargar
import contextlib
import gc
import math
import time

from packaging.version import Version
from transformers import AutoModelForCausalLM, AutoTokenizer

# transformers ≥ 4.56 llama «dtype» a lo que antes era «torch_dtype».
_DT = ("dtype" if Version(transformers.__version__) >= Version("4.56")
       else "torch_dtype")
TOK = AutoTokenizer.from_pretrained(MODELO)
if TOK.pad_token is None:
    TOK.pad_token = TOK.eos_token
LM = AutoModelForCausalLM.from_pretrained(MODELO, **{_DT: DTYPE}).to(DEVICE)
LM.requires_grad_(False)                 # congelado: solo LoRA va a entrenar
LM.eval()
# Generación greedy: sin azar ni penalizaciones (Qwen trae sampling por omisión).
_g = LM.generation_config
_g.do_sample, _g.temperature, _g.top_p, _g.top_k = False, None, None, None
_g.repetition_penalty = None
# Tope de tokens al generar: el completion más largo de train y validation
# (con su marca de fin), + 8 de holgura, sin pasar de max_len. Test no se mira.
P["max_new"] = min(P["max_len"], 8 + max(
    len(TOK(e["completion"], add_special_tokens=False)["input_ids"]) + 1
    for parte in ("train", "validation") for e in DATOS[parte]))
print("max_new =", P["max_new"], "tokens")
n_lm = sum(p.numel() for p in LM.parameters())
print(f"{MODELO}: {n_lm / 1e6:,.0f} M parámetros · "
      f"{n_lm * LM.dtype.itemsize / 1e9:.2f} GB en {LM.dtype}")


def liberar():
    """Suelta lo que ya no se usa de la memoria (GPU y RAM)."""
    gc.collect()
    if CUDA:
        torch.cuda.empty_cache()

# %% [texto] s03-plantilla-explica

# %% [codigo] s03-plantilla
def formatear(prompt):
    """El prompt dentro de la plantilla de chat del modelo, listo para que
    el asistente conteste."""
    return TOK.apply_chat_template([{"role": "user", "content": prompt}],
                                   tokenize=False, add_generation_prompt=True)


print(formatear(PROMPTS[0]))

# %% [texto] s03-generar-explica

# %% [codigo] s03-generar
def _sin_adaptador(modelo, apagar):
    """Contexto que apaga LoRA (si el modelo ya lo tiene y apagar=True)."""
    if apagar and hasattr(modelo, "disable_adapter"):
        return modelo.disable_adapter()
    return contextlib.nullcontext()


@torch.no_grad()
def generar(prompts, lora=True, max_new=None, modelo=None, lote=16):
    """Respuestas greedy, una por prompt. lora=False → el modelo base."""
    prompts = [prompts] if isinstance(prompts, str) else list(prompts)
    modelo = LM if modelo is None else modelo
    cfg = dict(max_new_tokens=max_new or P["max_new"],
               pad_token_id=TOK.pad_token_id)
    TOK.padding_side = "left"            # al generar, el relleno va a la izquierda
    salida = []
    with _sin_adaptador(modelo, not lora):
        modelo.eval()
        for i in range(0, len(prompts), lote):
            x = TOK([formatear(p) for p in prompts[i:i + lote]],
                    return_tensors="pt", padding=True,
                    add_special_tokens=False).to(DEVICE)
            y = modelo.generate(**x, **cfg)
            salida += TOK.batch_decode(y[:, x["input_ids"].shape[1]:],
                                       skip_special_tokens=True)
    TOK.padding_side = "right"           # al entrenar, a la derecha
    return [s.strip() for s in salida]


def respuestas(prompts, **columnas):
    """Tabla prompt → una columna por modelo (o por lo que pases)."""
    df = pd.DataFrame({"prompt": [recorta(p, 200) for p in prompts]})
    for nombre, textos in columnas.items():
        df[nombre] = [recorta(t, 400) for t in textos]
    return df

# %% [codigo] s03-antes
# El modelo base con tus prompts de prueba (los que NO están en el dataset).
t0 = time.perf_counter()
BASE_PROMPTS = generar(PROMPTS, lora=False)
mostrar(respuestas(PROMPTS, base=BASE_PROMPTS))

# Y tres ejemplos de validation, con la respuesta que pide tu dataset.
VAL3 = DATOS["validation"][:3]
mostrar(respuestas([e["prompt"] for e in VAL3],
                   esperado=[e["completion"] for e in VAL3],
                   base=generar([e["prompt"] for e in VAL3], lora=False)))
print(f"({time.perf_counter() - t0:.0f} s generando)")

# %% [texto] s03-lee
