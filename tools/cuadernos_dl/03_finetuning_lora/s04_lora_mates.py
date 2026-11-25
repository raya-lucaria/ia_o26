# Notebook 03 · §4 · LoRA y QLoRA en matemáticas.
# Consume: nada de la caja (corre sola). Publica: LoraLineal.
# La celda de código verifica a mano tres afirmaciones del texto:
# ΔW = 0 al inicio, ∂L/∂A = 0 en el primer backward, y el conteo de
# parámetros. La segunda celda hace la cuenta de memoria de AdamW.

# %% [texto] s04-intro

# %% [texto] s04-lora

# %% [codigo] s04-lora-a-mano
# LoRA escrita a mano sobre una lineal 768 → 768 (el ancho de la atención
# de SD 1.5). W0 queda congelada; solo A y B reciben gradiente.
import torch
from torch import nn


class LoraLineal(nn.Module):
    def __init__(self, base, r=8, alfa=8.0):
        super().__init__()
        self.base = base.requires_grad_(False)            # W0 congelada
        d, k = base.out_features, base.in_features
        self.A = nn.Parameter(torch.randn(r, k) / r)      # A aleatoria, r×k
        self.B = nn.Parameter(torch.zeros(d, r))          # B = 0, d×r
        self.s = alfa / r                                 # s = α/r

    def forward(self, x):
        # h = W0 x + s·B(Ax): nunca se forma la matriz d×k de ΔW
        return self.base(x) + self.s * (x @ self.A.T) @ self.B.T

    def delta_w(self):
        return self.s * self.B @ self.A


torch.manual_seed(0)
capa = LoraLineal(nn.Linear(768, 768), r=8, alfa=8.0)
x, y = torch.randn(16, 768), torch.randn(16, 768)

# 1) Al inicio ΔW = 0: la capa da exactamente lo mismo que la base.
print("max |ΔW| al inicio:", capa.delta_w().abs().max().item())
print("max |h − W0 x|:     ", (capa(x) - capa.base(x)).abs().max().item())

# 2) Primer backward: ∂L/∂A = s·Bᵀ g xᵀ = 0 porque B = 0; solo B se mueve.
perdida = ((capa(x) - y) ** 2).mean()
perdida.backward()
print("‖∂L/∂A‖ en el 1.er backward:", capa.A.grad.norm().item())
print("‖∂L/∂B‖ en el 1.er backward:", round(capa.B.grad.norm().item(), 6))

# Tras unos pasos B ≠ 0, A ya recibe gradiente, y rank(ΔW) ≤ r.
opt = torch.optim.SGD([capa.A, capa.B], lr=0.1)
for _ in range(5):
    opt.step()
    opt.zero_grad()
    ((capa(x) - y) ** 2).mean().backward()
print("‖∂L/∂A‖ tras 5 pasos:      ", round(capa.A.grad.norm().item(), 6))
print("rank(ΔW) tras 5 pasos:", torch.linalg.matrix_rank(capa.delta_w()).item(),
      "≤ r = 8")

# 3) Parámetros entrenables: d·k contra r(d + k).
completo = capa.base.weight.numel()
lora = capa.A.numel() + capa.B.numel()
print(f"completo d·k = {completo:,}   LoRA r(d+k) = {lora:,}   "
      f"({100 * lora / completo:.2f} %)")
assert (completo, lora) == (589_824, 12_288)

# %% [texto] s04-memoria

# %% [codigo] s04-memoria-cuenta
# Memoria de AdamW en fp32: peso 4 + gradiente 4 + m 4 + v 4 = 16 bytes por
# parámetro entrenable, antes de activaciones y temporales. n_unet es el
# UNet real si ya está cargado; si no, el de SD 1.5 (≈ 8.6·10⁸).
# (No se llama P: P es el diccionario de configuración de §1.)
_unet = globals().get("unet")
if isinstance(_unet, nn.Module):
    n_unet, origen = sum(p.numel() for p in _unet.parameters()), "UNet cargado"
else:
    n_unet, origen = 8.6e8, "referencia de SD 1.5"
GB, GIB = 1e9, 2 ** 30
print(f"P = {n_unet:,.0f} parámetros ({origen})")
for que, bytes_por_param in [("completo con AdamW (fp32)", 16),
                             ("solo W0 en fp16", 2),
                             ("solo W0 en NF4 (sin escalas)", 0.5)]:
    b = bytes_por_param * n_unet
    print(f"{que:30s} {b / GB:6.2f} GB = {b / GIB:6.2f} GiB")
print("Colab da ≈ 15 GiB en una T4, y aún faltan las activaciones.")

# %% [texto] s04-qlora
