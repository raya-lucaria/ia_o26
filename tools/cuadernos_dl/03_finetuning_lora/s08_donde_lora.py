# Notebook 03 · §8 · Dónde poner LoRA.
# Corto: ‖ΔW‖_F/‖W₀‖_F por capa de "lora_r8" (de s07), agrupada por zona del
# UNet (down / mid / up) y por tipo (self- / cross-attention).
# ➕ Produce "s08_atencion_mlp" (atención + MLP) y "s08_solo_up" (atención
# solo en up_blocks); las compara con "lora_r8" (curvas, tabla, malla).

# %% [texto] s08-intro

# %% [codigo] s08-normas
import pandas as pd
import matplotlib.pyplot as plt

ZONAS_S08 = {"down": "down_blocks", "mid": "mid_block", "up": "up_blocks"}
COLOR_S08 = {"down": "#9467bd", "mid": "#8c564b", "up": "#17becf"}


def zona_s08(capa):
    """down / mid / up según el nombre de la capa en el UNet."""
    return next((z for z, n in ZONAS_S08.items() if n in capa), "otra")


def tipo_s08(capa):
    """attn1 = self-attention, attn2 = cross-attention, ff = MLP."""
    if "attn1" in capa:
        return "self-attention"
    if "attn2" in capa:
        return "cross-attention"
    return "MLP" if ".ff." in capa else "otra"


def por_capa_s08(nombre):
    """norma_relativa de una corrida, en orden down → mid → up."""
    s = norma_relativa(nombre)
    df = pd.DataFrame({"capa": s.index, "norma": s.values})
    df["zona"] = df["capa"].map(zona_s08)
    df["tipo"] = df["capa"].map(tipo_s08)
    orden = {z: i for i, z in enumerate(list(ZONAS_S08) + ["otra"])}
    # sort estable: dentro de cada zona se conserva el orden del UNet
    return df.sort_values("zona", key=lambda z: z.map(orden), kind="stable")


R8_S08 = CORRIDAS.get("lora_r8")
if R8_S08 is None or R8_S08.error:
    print("lora_r8 no está lista (sección 07): no hay ΔW que medir.")
else:
    df = por_capa_s08("lora_r8").reset_index(drop=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4),
                                 gridspec_kw={"width_ratios": [2, 1]})
    a1.bar(df.index, df["norma"], color=df["zona"].map(COLOR_S08).fillna("gray"))
    for z, color in COLOR_S08.items():
        a1.bar([], [], color=color, label=z)          # solo para la leyenda
    a1.set(xlabel="capa adaptada (down → mid → up)",
           ylabel=r"$\|\Delta W\|_F\,/\,\|W_0\|_F$",
           title="lora_r8: cuánto se movió cada capa")
    a1.legend()
    resumen = df.pivot_table(index="zona", columns="tipo", values="norma",
                             aggfunc="mean").reindex(list(ZONAS_S08))
    resumen.plot.bar(ax=a2, rot=0, title="promedio por zona y tipo")
    fig.tight_layout()
    plt.show()
    display(resumen.style.format("{:.2e}"))
    print(f"{len(df)} capas adaptadas; la que más se movió: "
          f"{df.loc[df['norma'].idxmax(), 'capa']}")

# %% [texto] s08-variantes

# %% [codigo] s08-entrenar
ATENCION_S08 = ("to_q", "to_k", "to_v", "to_out.0")
MLP_S08 = ("ff.net.0.proj", "ff.net.2")      # las dos lineales del MLP
# Un solo texto con «(» o «*» la caja lo pasa a peft como REGEX, que debe
# coincidir con el nombre COMPLETO de la capa: atención, solo en up_blocks.
SOLO_UP_S08 = (r"up_blocks\..*\.(to_q|to_k|to_v|to_out\.0)",)

# Todo lo demás es igual a lora_r8 (rango, lr, pasos, schedule, semilla).
VARIANTES_S08 = ["lora_r8", "s08_atencion_mlp", "s08_solo_up"]
if LARGO:
    for c in (Corrida("s08_atencion_mlp", modulos=ATENCION_S08 + MLP_S08),
              Corrida("s08_solo_up", modulos=SOLO_UP_S08)):
        c = entrenar(c)
        print(f"{c.nombre}: " + (c.error or "lista"))
else:
    print("(solo en MODO largo)")

# %% [codigo] s08-comparar
OK_S08 = [n for n in VARIANTES_S08
          if n in CORRIDAS and CORRIDAS[n].error is None]
if not LARGO:
    print("(solo en MODO largo)")
elif len(OK_S08) < 2:
    print(f"Solo terminó {OK_S08}: no hay nada que comparar.")
else:
    display(tabla(OK_S08))
    curvas(OK_S08, "Dónde poner LoRA: train (delgada) y validation (gruesa)")
    # ‖ΔW‖ relativa promedio por zona: ¿dónde se concentra el cambio?
    zonas = pd.DataFrame({n: por_capa_s08(n).groupby("zona")["norma"].mean()
                          for n in OK_S08}).reindex(list(ZONAS_S08))
    display(zonas.style.format("{:.2e}", na_rep="—"))
    imgs = []
    for n in OK_S08:
        imgs += generar(n, PROMPT, P["semillas"])
    malla(imgs, filas=len(OK_S08),
          titulo=f"«{PROMPT}» · una fila por dónde va LoRA, mismas semillas",
          etiquetas=[f"{n} · s{s}" for n in OK_S08 for s in P["semillas"]])

# %% [texto] s08-que-mirar
