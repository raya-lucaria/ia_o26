# Notebook 03 · §13 · Cierre.
# Consume: CORRIDAS["lora_r8"] (s07), LATENTS["test"] (s03), perdida_val,
# generar, malla, tabla, liberar (s05). No entrena nada.
# Es la ÚNICA sección que toca test, y lo hace una vez.

# %% [texto] s13-intro

# %% [codigo] s13-test
# Test, una sola vez, con el método elegido por validation: LoRA r = 8.
# La caja no guarda el UNet entrenado: lo reconstruimos con sus propias
# piezas (base congelado + el adaptador que entrenar() dejó en disco) y
# medimos la misma loss de difusión de validation, ahora sobre test.
from peft import set_peft_model_state_dict
from safetensors.torch import load_file


def unet_con_adaptador(c):
    """UNet base congelado + el adaptador LoRA de la corrida `c`."""
    unet = _cargar_unet(c.metodo)
    unet.add_adapter(_config_lora(c))
    set_peft_model_state_dict(unet, load_file(c.ruta))
    return unet.eval()


elegida = CORRIDAS.get("lora_r8")
if elegida is None or elegida.error or not elegida.ruta:
    print("No hay una corrida \"lora_r8\" sana: corre §7 antes del cierre.")
else:
    liberar()
    unet_test = unet_con_adaptador(elegida)
    with torch.no_grad():
        loss_test = perdida_val(unet_test, LATENTS["test"])
        unet_test.disable_adapters()        # el mismo UNet, sin LoRA
        loss_test_base = perdida_val(unet_test, LATENTS["test"])
    del unet_test
    liberar()
    loss_val = elegida.perdidas_val[-1][1]
    print(f"loss de validation final (lora_r8): {loss_val:.4f}")
    print(f"loss de TEST (lora_r8):             {loss_test:.4f}")
    print(f"loss de test del modelo base:       {loss_test_base:.4f}")
    # Semillas que ninguna sección usó: imágenes nuevas del modelo elegido.
    semillas_test = [100, 101] if RAPIDO else [100, 101, 102, 103]
    malla(generar("lora_r8", semillas=semillas_test), filas=1,
          titulo="lora_r8 · semillas nuevas (test)",
          etiquetas=[f"semilla {s}" for s in semillas_test])

# %% [texto] s13-test-leer

# %% [texto] s13-tabla-texto

# %% [codigo] s13-tabla
# Todas las corridas registradas, una fila por corrida. Se comparan con la
# loss de validation; las que fallaron (OOM, bitsandbytes) dicen por qué.
resumen = tabla()
if resumen.empty:
    print("CORRIDAS está vacío: ejecuta el notebook completo y vuelve aquí.")
else:
    print(f"{len(resumen)} corridas registradas en MODO {MODO!r}.")
    display(resumen)

# %% [texto] s13-receta

# %% [texto] s13-tarea
