# §6 · Ver LoRA por dentro: (a) valores singulares de ΔW en una capa,
# (b) ‖ΔW‖/‖W0‖ por capa, (c) la perilla λ con el mismo prompt y semilla.
# Define DW (una fila por capa adaptada, con su ΔW) y la función zona.

# %% [texto] s06-intro

# %% [codigo] s06-capas
from peft.tuners.lora import LoraLayer


def zona(capa):
    """down / mid / up según el nombre de la capa en el UNet."""
    for z, clave in [("down", "down_blocks"), ("mid", "mid_block"),
                     ("up", "up_blocks")]:
        if clave in capa:
            return z
    return "otra"


def tipo(capa):
    """attn1 = self-attention (la imagen consigo misma), attn2 = cross-
    attention (la imagen mira al texto)."""
    return {"attn1": "self-attention", "attn2": "cross-attention"}.get(
        next((p for p in capa.split(".") if p.startswith("attn")), ""), "otra")


filas = []
for nombre, m in UNET.named_modules():
    if isinstance(m, LoraLayer) and "default" in m.lora_A:
        A = m.lora_A["default"].weight.detach().float().cpu()     # r × k
        B = m.lora_B["default"].weight.detach().float().cpu()     # d × r
        dw = m.scaling["default"] * (B @ A)                        # d × k
        w0 = m.base_layer.weight.detach().float().cpu()
        filas.append({"capa": nombre, "zona": zona(nombre),
                      "tipo": tipo(nombre), "dw": dw,
                      "‖ΔW‖/‖W0‖": (dw.norm() / w0.norm()).item()})
DW = pd.DataFrame(filas).set_index("capa")
print(f"{len(DW)} capas con adaptador · ‖ΔW‖/‖W0‖ mediana "
      f"{DW['‖ΔW‖/‖W0‖'].median():.2e}, máxima {DW['‖ΔW‖/‖W0‖'].max():.2e}")
if DW["‖ΔW‖/‖W0‖"].max() == 0:
    print("ΔW = 0 en todas las capas: el adaptador no se movió (¿corrió la 05?)")

# %% [texto] s06-svd-explica

# %% [codigo] s06-svd
def espectro(capa, ax):
    """σ_i / σ_1 de ΔW en escala log; la línea punteada marca r."""
    s = torch.linalg.svdvals(DW.loc[capa, "dw"]).numpy()
    s = s[: 3 * P["rango"]]
    ax.semilogy(np.arange(1, len(s) + 1), np.maximum(s / max(s[0], 1e-30),
                                                       1e-12), "o-", ms=3,
                label=f"{zona(capa)} · {capa.split('.')[-1]} · {tipo(capa)}")
    return s


fig, ax = plt.subplots(figsize=(7.5, 3.6))
mayor = DW["‖ΔW‖/‖W0‖"].idxmax()            # la capa que más se movió
capas = [mayor]
if LARGO:                                   # ➕ una capa más por zona
    capas += [DW[DW["zona"] == z]["‖ΔW‖/‖W0‖"].idxmax()
              for z in ("down", "mid", "up") if (DW["zona"] == z).any()]
for capa in dict.fromkeys(capas):
    s = espectro(capa, ax)
r = P["rango"]
ax.axvline(r, color="gray", ls="--", lw=1)
ax.text(r + 0.3, 1e-10, f"r = {r}", color="gray")
ax.set(xlabel="índice i", ylabel="σ_i / σ_1", ylim=(1e-12, 3),
       title="Valores singulares de ΔW: después de r, nada")
ax.legend(fontsize=7)
plt.tight_layout()
plt.show()
s = torch.linalg.svdvals(DW.loc[mayor, "dw"])
print(f"{mayor}: ΔW es {tuple(DW.loc[mayor, 'dw'].shape)}; rango numérico "
      f"{torch.linalg.matrix_rank(DW.loc[mayor, 'dw']).item()} (r = {r}); "
      f"σ_{r + 1}/σ_1 = {(s[r] / s[0]).item():.1e}")

# %% [texto] s06-barras-explica

# %% [codigo] s06-barras
COLOR_ZONA = {"down": "#9467bd", "mid": "#8c564b", "up": "#17becf",
              "otra": "gray"}
orden = {"down": 0, "mid": 1, "up": 2, "otra": 3}
tabla_dw = DW.sort_values("zona", key=lambda z: z.map(orden), kind="stable")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 3.8),
                             gridspec_kw={"width_ratios": [2, 1]})
a1.bar(range(len(tabla_dw)), tabla_dw["‖ΔW‖/‖W0‖"],
       color=tabla_dw["zona"].map(COLOR_ZONA))
for z in ("down", "mid", "up"):
    a1.bar([], [], color=COLOR_ZONA[z], label=z)          # solo la leyenda
a1.set(xlabel="capa adaptada (down → mid → up)",
       ylabel=r"$\|\Delta W\|_F\,/\,\|W_0\|_F$",
       title="Cuánto se movió cada capa")
a1.legend()
resumen = tabla_dw.pivot_table(index="zona", columns="tipo",
                               values="‖ΔW‖/‖W0‖", aggfunc="mean")
resumen.reindex([z for z in orden if z in resumen.index]).plot.bar(
    ax=a2, rot=0, title="promedio por zona y tipo")
plt.tight_layout()
plt.show()
display(tabla_dw.nlargest(5, "‖ΔW‖/‖W0‖")[["zona", "tipo", "‖ΔW‖/‖W0‖"]]
        .style.format({"‖ΔW‖/‖W0‖": "{:.2e}"}))

# %% [texto] s06-perilla-explica

# %% [codigo] s06-perilla
LAMBDAS = [0.0, 0.5, 1.0, 1.5]
pares = combinar(PROMPTS[:1], P["semillas"][:2])   # el mismo prompt y semillas
imgs = []
for lam in LAMBDAS:
    imgs += generar(pares, lora=True, escala=lam)
malla(imgs, filas=len(LAMBDAS), titulo=f"La perilla λ · «{PROMPTS[0]}»",
      etiquetas=[f"λ = {lam}" for lam in LAMBDAS])

# λ = 0 contra el modelo base (adaptador apagado), píxel por píxel.
base = generar(pares, lora=False)
dif = [np.abs(np.asarray(a, np.float32) - np.asarray(b, np.float32))
       for a, b in zip(imgs[:len(pares)], base)]
print(f"λ = 0 contra el base: diferencia media {np.mean([d.mean() for d in dif]):.3f}"
      f", máxima {max(d.max() for d in dif):.0f} (escala 0–255)")
