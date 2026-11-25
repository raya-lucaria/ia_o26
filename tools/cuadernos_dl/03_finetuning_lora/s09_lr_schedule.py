# Notebook 03 · §9 · Learning rate y schedule.
# Corto: dibuja los dos schedules (warmup + cosine y constante) y explica qué
# se esperaría. ➕ Produce "s09_lr_1e-5", "s09_lr_1e-3" y "s09_constante";
# las compara con "lora_r8" (lr 1e-4, warmup + cosine) de s07.

# %% [texto] s09-intro

# %% [codigo] s09-schedules
import torch
import matplotlib.pyplot as plt
from diffusers.optimization import get_scheduler

R8_S09 = CORRIDAS.get("lora_r8")
PASOS_S09 = (R8_S09.pasos if R8_S09 and R8_S09.pasos else P["pasos"])
# El warmup que usa la caja; si la corrida no lo guardó, ~5 % de los pasos.
WARMUP_S09 = (R8_S09.warmup if R8_S09 and R8_S09.warmup is not None
              else max(1, PASOS_S09 // 20))


def lr_por_paso_s09(nombre_diffusers, lr=1e-4):
    """El learning rate en cada paso, con un optimizer de juguete."""
    opt = torch.optim.AdamW([torch.zeros(1, requires_grad=True)], lr=lr)
    sch = get_scheduler(nombre_diffusers, optimizer=opt,
                        num_warmup_steps=WARMUP_S09,
                        num_training_steps=PASOS_S09)
    valores = []
    for _ in range(PASOS_S09):
        valores.append(sch.get_last_lr()[0])
        opt.step()
        sch.step()
    return valores


fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(lr_por_paso_s09("cosine"), lw=2, label="warmup + cosine (lora_r8)")
ax.plot(lr_por_paso_s09("constant_with_warmup"), lw=2, ls="--",
        label="warmup + constante (s09_constante)")
ax.axvline(WARMUP_S09, color="gray", ls=":", lw=1)
ax.set(xlabel="paso", ylabel="learning rate", title=f"lr máximo 1e-4, "
       f"{PASOS_S09} pasos, warmup de {WARMUP_S09}")
ax.legend()
plt.show()

# %% [texto] s09-variantes

# %% [codigo] s09-entrenar
# Todo igual a lora_r8 salvo lo que se cambia.
VARIANTES_S09 = {"s09_lr_1e-5": dict(lr=1e-5),
                 "s09_lr_1e-3": dict(lr=1e-3),
                 "s09_constante": dict(schedule="constante")}
if LARGO:
    for nombre, cambio in VARIANTES_S09.items():
        c = entrenar(Corrida(nombre, **cambio))
        print(f"{nombre}: " + (c.error or "lista"))
else:
    print("(solo en MODO largo) — la tabla de arriba dice qué se esperaría.")

# %% [codigo] s09-comparar
def listas_s09(nombres):
    """Solo las corridas que existen y terminaron sin error."""
    return [n for n in nombres if n in CORRIDAS and CORRIDAS[n].error is None]


LR_S09 = listas_s09(["s09_lr_1e-5", "lora_r8", "s09_lr_1e-3"])
SCH_S09 = listas_s09(["lora_r8", "s09_constante"])
if not LARGO:
    print("(solo en MODO largo)")
elif len(LR_S09) + len(SCH_S09) < 3:
    print("Faltan corridas: no hay nada que comparar.")
else:
    display(tabla(listas_s09(["lora_r8", *VARIANTES_S09])))
    if len(LR_S09) > 1:
        curvas(LR_S09, "lr 1e-5 / 1e-4 / 1e-3: train (delgada), val (gruesa)")
    if len(SCH_S09) > 1:
        curvas(SCH_S09, "warmup + cosine vs constante (lr 1e-4)")
    filas = LR_S09 + [n for n in SCH_S09 if n not in LR_S09]
    imgs = []
    for n in filas:
        imgs += generar(n, PROMPT, P["semillas"])
    malla(imgs, filas=len(filas),
          titulo=f"«{PROMPT}» · una fila por lr / schedule, mismas semillas",
          etiquetas=[f"{n} · s{s}" for n in filas for s in P["semillas"]])

# %% [texto] s09-que-mirar
