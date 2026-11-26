# §6 · Ver LoRA: (a) valores singulares de ΔW, (b) qué capas cambiaron más,
# (c) la perilla λ y (d) merge_and_unload da lo mismo que el adaptador.
# Publica delta_w, NORMAS, escala_lora.

# %% [texto] s06-intro

# %% [codigo] s06-delta
def delta_w(capa):
    """ΔW = (α/r)·B·A de una capa LoRA, en CPU y fp32: [d_salida, d_entrada]."""
    A = capa.lora_A["default"].weight.detach().float().cpu()
    B = capa.lora_B["default"].weight.detach().float().cpu()
    return capa.scaling["default"] * (B @ A)


filas = []
for n, m in capas_lora().items():
    dw, w0 = delta_w(m), m.base_layer.weight.detach().float().cpu()
    filas.append({"nombre": n, "bloque": int(n.split(".layers.")[1].split(".")[0]),
                  "lineal": n.split(".")[-1],
                  "relativa": (dw.norm() / w0.norm()).item()})
NORMAS = pd.DataFrame(filas)
mayor = NORMAS.loc[NORMAS["relativa"].idxmax()]
print(f"La capa que más cambió: {mayor['nombre']} "
      f"(‖ΔW‖/‖W₀‖ = {mayor['relativa']:.4f})")

# %% [texto] s06-svd-explica

# %% [codigo] s06-svd
# (a) Valores singulares de ΔW en la capa que más cambió, y de su W₀.
capa = capas_lora()[mayor["nombre"]]
s_dw = torch.linalg.svdvals(delta_w(capa))
s_w0 = torch.linalg.svdvals(capa.base_layer.weight.detach().float().cpu())
r, k = P["rango"], min(3 * P["rango"], len(s_dw))
fig, eje = plt.subplots(figsize=(7.5, 3.4))
eje.semilogy(range(1, k + 1), s_w0[:k] / s_w0[0], "o-", color="gray",
             ms=3, label="W₀ (congelada)")
eje.semilogy(range(1, k + 1), (s_dw[:k] / s_dw[0]).clamp_min(1e-12), "o-",
             color=COLORES["validation"], ms=4, label="ΔW (LoRA)")
eje.axvline(r + 0.5, color="black", ls="--", lw=1)
eje.text(r + 0.7, 1e-3, f"r = {r}", fontsize=9)
eje.set(xlabel="índice del valor singular", ylabel="σᵢ / σ₁ (escala log)",
        title=f"Valores singulares · {mayor['lineal']} del bloque "
              f"{mayor['bloque']}")
eje.legend()
plt.tight_layout()
plt.show()
if len(s_dw) > r:
    print(f"σ_{r + 1} / σ_1 de ΔW = {(s_dw[r] / s_dw[0]).item():.1e}  "
          f"(cero numérico: rank(ΔW) ≤ {r})")

# %% [texto] s06-capas-explica

# %% [codigo] s06-capas
# (b) ‖ΔW‖_F / ‖W₀‖_F por bloque y por lineal.
tabla_n = NORMAS.pivot(index="bloque", columns="lineal", values="relativa")
tabla_n = tabla_n[[m for m in P["modulos"] if m in tabla_n.columns]]
ancho = 0.8 / len(tabla_n.columns)
fig, eje = plt.subplots(figsize=(10, 3.6))
for j, lineal in enumerate(tabla_n.columns):
    eje.bar(tabla_n.index + (j - (len(tabla_n.columns) - 1) / 2) * ancho,
            tabla_n[lineal], width=ancho, color=plt.cm.tab10(j), label=lineal)
eje.set(xlabel="bloque del transformer (0 = el más cercano a la entrada)",
        ylabel="‖ΔW‖ / ‖W₀‖", title="¿Qué capas cambió más tu LoRA?")
eje.legend(ncol=len(tabla_n.columns), fontsize=8)
plt.tight_layout()
plt.show()
display(tabla_n.mean().rename("promedio por lineal").to_frame().T.round(4))

# %% [texto] s06-lambda-explica

# %% [codigo] s06-lambda
@contextlib.contextmanager
def escala_lora(lam):
    """Multiplica α/r de TODAS las capas LoRA por λ; al salir, lo restaura."""
    capas = list(capas_lora().values())
    antes = [dict(m.scaling) for m in capas]
    try:
        for m in capas:
            for nombre in m.scaling:
                m.scaling[nombre] *= lam
        yield
    finally:
        for m, a in zip(capas, antes):
            m.scaling.update(a)


# (c) La perilla: el mismo prompt, greedy (sin azar), cuatro valores de λ.
PROMPTS_L = [PROMPTS[0], DATOS["validation"][0]["prompt"]]
por_lambda = {}
for lam in [0, 0.5, 1, 1.5]:
    with escala_lora(lam):
        por_lambda[f"λ = {lam}"] = generar(PROMPTS_L)
mostrar(respuestas(PROMPTS_L, **por_lambda))
print("λ = 0 da lo mismo que el base:",
      por_lambda["λ = 0"] == generar(PROMPTS_L, lora=False))

# %% [texto] s06-merge-explica

# %% [codigo] s06-merge
# (d) merge_and_unload sobre una COPIA: W = W₀ + (α/r)BA en una sola matriz.
import copy

copia = copy.deepcopy(LM)
fusionado = copia.merge_and_unload()
print("capas LoRA que quedan tras fusionar:",
      sum(isinstance(m, LoraLayer) for m in fusionado.modules()))
print(f"parámetros: base {n_lm:,} · fusionado "
      f"{sum(p.numel() for p in fusionado.parameters()):,}")
TOK.padding_side = "left"
x = TOK([formatear(p) for p in PROMPTS], return_tensors="pt", padding=True,
        add_special_tokens=False).to(DEVICE)
TOK.padding_side = "right"
with torch.no_grad():
    con_adaptador = LM(**x).logits.float()
    con_fusion = fusionado(**x).logits.float()
dif = (con_adaptador - con_fusion).abs().max().item()
print(f"max |logits adaptador − logits fusionado| = {dif:.2e} "
      f"(escala de los logits: {con_adaptador.abs().max().item():.1f})")
iguales = generar(PROMPTS) == generar(PROMPTS, modelo=fusionado)
print("¿mismas respuestas greedy en prompts.txt?", iguales)
del copia, fusionado, con_adaptador, con_fusion
liberar()
