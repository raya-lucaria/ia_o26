# §5 · Entrenar un LoRA r = 8 con la loss solo en los tokens del completion.
# Publica tokenizar, TOKS, lote, perdida_suma, perdida_val, entrenar, HIST,
# curvas. Deja LM con el adaptador entrenado.

# %% [texto] s05-intro

# %% [codigo] s05-tokenizar
import html

import torch.nn.functional as F
from transformers import get_cosine_schedule_with_warmup


def tokenizar(ej):
    """ids del prompt + completion y labels con -100 en el prompt."""
    p_txt = formatear(ej["prompt"])
    completo = TOK.apply_chat_template(
        [{"role": "user", "content": ej["prompt"]},
         {"role": "assistant", "content": ej["completion"]}], tokenize=False)
    if completo.startswith(p_txt):       # «completion<|im_end|>»
        c_txt = completo[len(p_txt):].rstrip("\n")
    else:                                # plantilla rara: a mano
        c_txt = ej["completion"] + TOK.eos_token
    p = TOK(p_txt, add_special_tokens=False)["input_ids"]
    c = TOK(c_txt, add_special_tokens=False)["input_ids"]
    return {"ids": (p + c)[:P["max_len"]],
            "labels": ([-100] * len(p) + c)[:P["max_len"]],
            "n_prompt": len(p), "cortado": len(p) + len(c) > P["max_len"]}


TOKS, RESUMEN = {}, {}
for parte, ejs in DATOS.items():
    todos = [dict(tokenizar(e), i=i) for i, e in enumerate(ejs)]  # i: su fila
    # sin ningún token de completion (el prompt solo ya llena max_len): fuera
    TOKS[parte] = [t for t in todos if any(l != -100 for l in t["labels"])]
    RESUMEN[parte] = {"ejemplos": len(todos),
                      "cortados": sum(t["cortado"] for t in todos),
                      "descartados": len(todos) - len(TOKS[parte]),
                      "tokens (mediana)": int(np.median(
                          [len(t["ids"]) for t in todos]))}
# El resumen de test espera a §08: aquí todavía puedes cambiar max_len.
display(pd.DataFrame({k: RESUMEN[k] for k in ["train", "validation"]}).T)
assert TOKS["train"], "ningún ejemplo de train cabe en max_len: acorta prompts"

# %% [texto] s05-mascara-explica

# %% [codigo] s05-mascara
def ver_mascara(t, antes=40, despues=60):
    """El ejemplo token por token: gris = prompt (label -100, no cuenta en la
    loss), verde = completion (sí cuenta)."""
    i0 = max(0, t["n_prompt"] - antes)
    piezas = [] if i0 == 0 else ["… "]
    for i, l in zip(t["ids"][i0:t["n_prompt"] + despues],
                    t["labels"][i0:t["n_prompt"] + despues]):
        txt = html.escape(TOK.decode([i])).replace("\n", "↵")
        fondo = "#dddddd" if l == -100 else "#a8e6b4"
        piezas.append(f'<span style="background:{fondo};color:#000;'
                      f'border:1px solid #fff;padding:0 1px">{txt}</span>')
    try:
        from IPython.display import HTML
        display(HTML("<div style='font-family:monospace;line-height:1.9'>"
                     + "".join(piezas) + "</div>"))
    except ImportError:
        pass
    n = t["n_prompt"]
    filas = [{"posición": j, "token": repr(TOK.decode([t["ids"][j]])),
              "id": t["ids"][j], "label": t["labels"][j],
              "¿cuenta en la loss?": "sí" if t["labels"][j] != -100 else "no"}
             for j in range(max(0, n - 4), min(len(t["ids"]), n + 4))]
    display(pd.DataFrame(filas).set_index("posición"))
    print(f"{len(t['ids'])} tokens: {n} de prompt (no cuentan) y "
          f"{len(t['ids']) - n} de completion (sí cuentan)")


ver_mascara(TOKS["train"][0])

# %% [codigo] s05-perdida
def lote(items):
    """Relleno a la derecha: pad en ids, 0 en la máscara, -100 en labels."""
    largo = max(len(t["ids"]) for t in items)
    ids = torch.full((len(items), largo), TOK.pad_token_id)
    labels = torch.full((len(items), largo), -100)
    mascara = torch.zeros((len(items), largo), dtype=torch.long)
    for i, t in enumerate(items):
        n = len(t["ids"])
        ids[i, :n], labels[i, :n] = torch.tensor(t["ids"]), torch.tensor(t["labels"])
        mascara[i, :n] = 1
    return {"ids": ids.to(DEVICE), "mascara": mascara.to(DEVICE),
            "labels": labels.to(DEVICE)}


def perdida_suma(b):
    """(suma de −log p del token correcto, número de tokens que cuentan).
    El logit de la posición i predice el token i + 1: de ahí el corrimiento."""
    logits = LM(input_ids=b["ids"], attention_mask=b["mascara"]).logits
    objetivo = b["labels"][:, 1:]
    suma = F.cross_entropy(logits[:, :-1].float().flatten(0, 1),
                           objetivo.flatten(), ignore_index=-100,
                           reduction="sum")
    return suma, (objetivo != -100).sum()


@torch.no_grad()
def perdida_val(parte="validation", lora=True, n=None):
    """Loss media por token de completion en las filas 0…n−1 de `parte`
    (n = n_val_loss por omisión). NaN si ninguna conserva su completion."""
    n = P["n_val_loss"] if n is None else n
    items, suma, cuenta = [t for t in TOKS[parte] if t["i"] < n], 0.0, 0
    estaba = LM.training
    LM.eval()
    with _sin_adaptador(LM, not lora):
        for i in range(0, len(items), 2 * P["batch"]):
            with torch.autocast("cuda", dtype=torch.float16, enabled=AMP):
                s, k = perdida_suma(lote(items[i:i + 2 * P["batch"]]))
            suma, cuenta = suma + s.item(), cuenta + k.item()
    LM.train(estaba)
    if cuenta == 0:
        print(f"(loss de {parte}: NaN, ninguna de sus primeras {n} filas "
              "conserva tokens de completion dentro de max_len)")
        return float("nan")
    return suma / cuenta

# %% [texto] s05-entrenar-explica

# %% [codigo] s05-entrenar
def _preparar():
    """Adaptador nuevo, checkpointing, AdamW, cosine con warmup, GradScaler."""
    lora_nuevo()
    liberar()
    if CUDA:
        torch.cuda.reset_peak_memory_stats()
    LM.gradient_checkpointing_enable(
        gradient_checkpointing_kwargs={"use_reentrant": False})
    LM.enable_input_require_grads()
    LM.config.use_cache = False           # el caché no sirve al entrenar
    entrenables = [p for p in LM.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(entrenables, lr=P["lr"], weight_decay=0.0)
    sched = get_cosine_schedule_with_warmup(
        opt, num_warmup_steps=max(1, round(0.05 * P["pasos"])),
        num_training_steps=P["pasos"])
    return entrenables, opt, sched, torch.amp.GradScaler("cuda", enabled=AMP)


def _batches(semilla_=0):
    """Batches de train sin fin: cada época, un orden nuevo (y fijo)."""
    g, train = np.random.default_rng(semilla_), TOKS["train"]
    n = min(P["batch"], len(train))
    while True:
        orden = g.permutation(len(train))
        for i in range(0, len(orden) - n + 1, n):     # batches completos
            yield lote([train[j] for j in orden[i:i + n]])

# %% [codigo] s05-bucle
_DESBORDE = ("paso {}: {} (inf/NaN). Me detengo en vez de contar "
             "un paso que no actualizó nada. Baja P['lr'] (p. ej. 1e-4) o "
             "P['max_len'] y vuelve a correr §05.")


def entrenar():
    """Un LoRA desde cero. Devuelve el historial de loss train/validation."""
    semilla(0)
    entrenables, opt, sched, escalador = _preparar()
    hist = {"train": [], "validation": [(0, perdida_val())], "seg": []}
    fuente, paso, intentos = _batches(), 0, 0
    LM.train()
    while paso < P["pasos"] and intentos < 2 * P["pasos"]:
        intentos += 1
        t0 = time.perf_counter()
        lotes = [next(fuente) for _ in range(P["acum"])]
        n_tok = sum((b["labels"][:, 1:] != -100).sum() for b in lotes)
        opt.zero_grad(set_to_none=True)
        total = 0.0
        for b in lotes:                   # acumula acum gradientes
            with torch.autocast("cuda", dtype=torch.float16, enabled=AMP):
                s, _ = perdida_suma(b)
            perdida = s / n_tok           # media sobre TODOS los tokens del paso
            if not torch.isfinite(perdida):
                raise FloatingPointError(_DESBORDE.format(paso + 1,
                                                        "la loss no es finita"))
            escalador.scale(perdida).backward()
            total += perdida.item()
        escalador.unscale_(opt)
        norma = torch.nn.utils.clip_grad_norm_(entrenables, 1.0)
        if not AMP and not torch.isfinite(norma):   # fp32: nada que reescalar
            raise FloatingPointError(_DESBORDE.format(paso + 1,
                                                    "el gradiente no es finito"))
        escala_previa = escalador.get_scale()
        escalador.step(opt)
        escalador.update()
        if AMP and escalador.get_scale() == 0:      # ya no hay a dónde bajar
            raise FloatingPointError(_DESBORDE.format(paso + 1,
                                                    "la escala llegó a 0"))
        if escalador.get_scale() < escala_previa:   # inf/NaN: paso saltado
            continue
        paso += 1
        sched.step()
        if CUDA:
            torch.cuda.synchronize()
        hist["seg"].append(time.perf_counter() - t0)
        hist["train"].append((paso, total))
        if paso % P["val_cada"] == 0 or paso == P["pasos"]:
            hist["validation"].append((paso, perdida_val()))
    if paso < P["pasos"]:
        print(f"¡Ojo! solo {paso} pasos válidos de {P['pasos']} (inf/NaN)")
    LM.eval()
    LM.config.use_cache = True            # para generar rápido
    return hist

# %% [codigo] s05-correr
inicio = time.perf_counter()
HIST = entrenar()
seg = HIST["seg"][3:] or HIST["seg"]
print(f"✓ {len(HIST['train'])} pasos en {time.perf_counter() - inicio:.0f} s "
      f"({np.mean(seg):.2f} s/paso)")
print(f"loss de validation: {HIST['validation'][0][1]:.3f} (base) → "
      f"{HIST['validation'][-1][1]:.3f} (LoRA)")
if CUDA:
    print(f"memoria pico de la GPU: {torch.cuda.max_memory_allocated() / 1e9:.1f} GB")

# %% [codigo] s05-curvas
def curvas(hist, titulo="Loss solo en el completion"):
    """Train delgada y tenue (un batch por punto); validation gruesa."""
    fig, eje = plt.subplots(figsize=(7.5, 3.6))
    eje.plot(*zip(*hist["train"]), color=COLORES["train"], lw=0.8,
             alpha=0.5, label="train (cada paso)")
    eje.plot(*zip(*hist["validation"]), color=COLORES["validation"], lw=2.5,
             marker="o", ms=4, label="validation")
    eje.set(xlabel="paso", ylabel="loss por token (nats)", title=titulo)
    eje.legend()
    plt.tight_layout()
    plt.show()


curvas(HIST)

# %% [texto] s05-lee
