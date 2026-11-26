# §4 · LoRA por dentro: las matemáticas, y la cuenta en TU modelo.
# Publica CONFIG_LORA, lora_nuevo() (pone un adaptador nuevo, B = 0) y
# capas_lora(). Deja LM con un adaptador recién puesto.

# %% [texto] s04-intro

# %% [texto] s04-mates

# %% [codigo] s04-config
import tempfile

from peft import LoraConfig, PeftModel, get_peft_model
from peft.tuners.lora import LoraLayer

CONFIG_LORA = LoraConfig(r=P["rango"], lora_alpha=P["alfa"],
                         target_modules=P["modulos"], lora_dropout=0.05,
                         bias="none", task_type="CAUSAL_LM")


def lora_nuevo():
    """Quita el adaptador que hubiera y pone uno nuevo: A al azar, B = 0."""
    global LM
    if isinstance(LM, PeftModel):
        LM = LM.unload()                 # el modelo base, sin capas LoRA
    semilla(0)
    LM = get_peft_model(LM, CONFIG_LORA)
    for p in LM.parameters():            # adaptador en fp32 (ver §05)
        if p.requires_grad:
            p.data = p.data.float()
    return LM


def capas_lora():
    """{nombre: capa} de cada lineal que lleva LoRA."""
    return {n: m for n, m in LM.named_modules() if isinstance(m, LoraLayer)}


lora_nuevo()
capas = capas_lora()
print(f"{len(capas)} lineales con LoRA, por ejemplo:")
for n in list(capas)[:len(P["modulos"])]:
    print("  ", n)

# %% [codigo] s04-contar
# ¿Cuánto entrenas de verdad? Parámetros, % y MB, medidos en el modelo.
total = sum(p.numel() for p in LM.parameters())
entrenables = sum(p.numel() for p in LM.parameters() if p.requires_grad)
mb_modelo = sum(p.numel() * p.element_size() for p in LM.parameters()
                if not p.requires_grad) / 1e6
with tempfile.TemporaryDirectory() as d:  # el adaptador, guardado en disco
    LM.save_pretrained(d)
    mb_adaptador = sum(os.path.getsize(os.path.join(d, f))
                       for f in os.listdir(d)) / 1e6
display(pd.DataFrame({"valor": {
    "parámetros del modelo": f"{total - entrenables:,}",
    "parámetros entrenables (A y B)": f"{entrenables:,}",
    "% entrenable": f"{100 * entrenables / total:.3f} %",
    "MB del modelo (congelado)": f"{mb_modelo:,.0f}",
    "MB del adaptador en disco": f"{mb_adaptador:,.1f}"}}))

# Por tipo de capa, en la primera capa del modelo: d·k contra r(d + k).
filas = []
for n, m in capas.items():
    if ".layers.0." not in n:
        continue
    d, k = m.base_layer.weight.shape
    filas.append({"capa": n.split(".")[-1], "d (salida)": d, "k (entrada)": k,
                  "d·k": d * k, "r(d+k)": P["rango"] * (d + k),
                  "%": round(100 * P["rango"] * (d + k) / (d * k), 2)})
display(pd.DataFrame(filas).set_index("capa"))

# %% [codigo] s04-inicio
# Con B = 0, ΔW = 0: el modelo con LoRA da EXACTAMENTE lo mismo que el base.
x = TOK([formatear(PROMPTS[0])], return_tensors="pt",
        add_special_tokens=False).to(DEVICE)
with torch.no_grad():
    con = LM(**x).logits
    with LM.disable_adapter():
        sin = LM(**x).logits
print("max |logits con LoRA − logits base| =", (con - sin).abs().max().item())

# %% [texto] s04-lee
