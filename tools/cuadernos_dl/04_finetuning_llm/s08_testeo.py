# §8 · Testeo, UNA sola vez: base contra LoRA en test, tus prompts antes y
# después, olvido en preguntas generales, guardar y descargar el adaptador.

# %% [texto] s08-intro

# %% [codigo] s08-test
# El test, por primera y única vez.
TEST_TABLA, TEST_PRED = evaluar("test")
display(TEST_TABLA.round(3))
mostrar(por_ejemplo("test", TEST_PRED))

# %% [texto] s08-prompts-explica

# %% [codigo] s08-prompts
# Tus prompts de prueba: el base de §03 contra tu LoRA.
mostrar(respuestas(PROMPTS, base=BASE_PROMPTS, LoRA=generar(PROMPTS)))

# %% [texto] s08-olvido-explica

# %% [codigo] s08-olvido
# Tres preguntas que no tienen nada que ver con tu dataset.
AJENAS = ["¿Cuál es la capital de Francia? Contesta en una frase.",
          "Explica en dos frases qué es la fotosíntesis.",
          "Escribe un haiku sobre el mar."]
mostrar(respuestas(AJENAS, base=generar(AJENAS, lora=False, max_new=96),
                   LoRA=generar(AJENAS, max_new=96)))

# %% [texto] s08-guardar-explica

# %% [codigo] s08-guardar
# Solo A y B (y su configuración) a una carpeta, y la carpeta a un zip.
import shutil

CARPETA = "mi_lora_texto"
LM.save_pretrained(CARPETA)
with open(os.path.join(CARPETA, "LEEME.md"), "w", encoding="utf-8") as f:
    f.write(f"# Mi LoRA de texto\n\n- Modelo base: {MODELO}\n"
            f"- r = {P['rango']}, α = {P['alfa']}, capas: {P['modulos']}\n"
            f"- {len(HIST['train'])} pasos, lr = {P['lr']}\n\n"
            f"## Mi dataset\n\n{LEEME}\n\n## Test (una vez)\n\n"
            f"{TEST_TABLA.round(3).to_string()}\n")
zip_lora = shutil.make_archive(CARPETA, "zip", CARPETA)
print(f"{zip_lora}: {os.path.getsize(zip_lora) / 1e6:.1f} MB")
try:
    from google.colab import files
    files.download(zip_lora)              # baja a tu computadora
except ImportError:
    print("(fuera de Colab: el zip queda en la carpeta actual)")

# %% [texto] s08-receta

# %% [texto] s08-cierre
