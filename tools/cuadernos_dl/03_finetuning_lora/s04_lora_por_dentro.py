# §4 · LoRA por dentro: la fórmula, y la cuenta de parámetros en TU UNet.
# Define MODULOS (las lineales que recibirán LoRA), CAPAS (una fila por
# capa adaptada: d, k, dk, r(d+k)), N_UNET y N_LORA.

# %% [texto] s04-intro

# %% [codigo] s04-contar
# Las lineales de la atención, como en el notebook 3 y en casi todo LoRA de SD.
MODULOS = ("to_q", "to_k", "to_v", "to_out.0")


def es_objetivo(nombre):
    """La misma regla que peft: el nombre es el módulo o termina en .módulo."""
    return any(nombre == m or nombre.endswith("." + m) for m in MODULOS)


r = P["rango"]
filas = []
for nombre, m in UNET.named_modules():
    nombre = nombre.removesuffix(".base_layer")     # si ya hay adaptador
    if isinstance(m, torch.nn.Linear) and es_objetivo(nombre):
        d, k = m.out_features, m.in_features         # W0 es d × k
        filas.append({"capa": nombre, "d": d, "k": k,
                      "dk": d * k, "r(d+k)": r * (d + k)})
CAPAS = pd.DataFrame(filas).set_index("capa")
N_LORA = int(CAPAS["r(d+k)"].sum())
N_UNET = sum(p.numel() for n, p in UNET.named_parameters() if "lora_" not in n)
N_PIPE = N_UNET + sum(p.numel() for p in PIPE.vae.parameters()) + sum(
    p.numel() for p in PIPE.text_encoder.parameters())

print(f"{len(CAPAS)} capas lineales reciben LoRA. Sus formas (d × k):")
display(CAPAS.groupby(["d", "k"]).size().rename("capas").to_frame())
MB = 1e6
display(pd.DataFrame({
    "parámetros": [N_PIPE, N_UNET, int(CAPAS["dk"].sum()), N_LORA],
    "MB": [2 * N_PIPE / MB, 2 * N_UNET / MB, 2 * CAPAS["dk"].sum() / MB,
           4 * N_LORA / MB],
    "% del UNet": [100 * N_PIPE / N_UNET, 100.0,
                   100 * CAPAS["dk"].sum() / N_UNET, 100 * N_LORA / N_UNET]},
    index=["Stable Diffusion completo (fp16)", "UNet (fp16)",
           "las W0 que se adaptan (fp16)", f"LoRA r={r}: A y B (fp32)"]
).style.format({"parámetros": "{:,.0f}", "MB": "{:,.1f}",
                "% del UNet": "{:.2f} %"}))
print(f"Entrenas {N_LORA:,} números: {100 * N_LORA / N_UNET:.2f} % del UNet.")
