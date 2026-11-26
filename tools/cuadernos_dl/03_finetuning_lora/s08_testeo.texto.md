### celda: s08-intro

## 08 · Testeo, una sola vez

> **Test se usa una vez, aquí, y no se vuelve a tocar.** Si después de ver estos números cambias pasos o learning rate y vuelves a correr, test deja de ser una medida honesta: ya lo usaste para decidir. Para decidir está validation.

- Las mismas cinco métricas de la sección 07, ahora sobre **test**: imágenes que ni el entrenamiento ni tus decisiones vieron.
- Se generan con semillas nuevas (3000 en adelante para los captions de test, 4000 en adelante para los prompts ajenos).
- La segunda tabla pone lado a lado los números de LoRA en validation y en test.

### celda: s08-tabla-leer

**Cómo leer las tablas.**

- **Validation contra test.** Si los números de LoRA se parecen, validation fue un buen juez. Si test sale mucho peor, la partición tuvo mala suerte o el dataset es chico; dilo en tu reporte, no lo corrijas mirando test otra vez.
- **Base contra LoRA.** Lee las cinco filas juntas, como en la sección 07. Un resultado raro (estilo que no sube, loss que sube) también es un resultado: coméntalo con la receta de abajo.

Debajo, dos mallas:

1. **Test:** la imagen real, la del base y la de LoRA con el mismo caption y la misma semilla.
2. **Tus prompts:** para cada prompt, la fila «antes» es la misma de la sección 03 y la fila «después» usa las **mismas semillas** con el adaptador. Compara columna por columna.

### celda: s08-olvido-explica

**Olvido, a la vista.** Para cada prompt ajeno, una fila con el base y otra con LoRA, mismas semillas.

- Si el perro sigue siendo perro pero «con tu estilo», es **interferencia**: $\Delta W$ actúa en la atención para cualquier prompt.
- Si el perro **deja de verse**, es olvido con el adaptador prendido. Baja $\lambda$ o entrena menos.
- La tabla es el CLIP score de cada prompt; la diferencia `LoRA − base` negativa dice cuánto se alejó del texto.

### celda: s08-guardar-explica

**Tu adaptador, a tu computadora.** Se guardan solo $A$ y $B$ de cada capa, en el formato de diffusers, en `mi_lora/pytorch_lora_weights.safetensors`, y Colab lo descarga. Compara sus MB con los del UNet: eso es LoRA.

- Si el navegador bloquea la descarga, búscalo en el panel 📁 (carpeta `mi_lora`), clic derecho → Descargar.
- Para usarlo después, en cualquier notebook con Stable Diffusion 1.5:

```python
pipe = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16).to("cuda")
pipe.load_lora_weights("mi_lora")            # la carpeta con el .safetensors
imagen = pipe("an anime face", cross_attention_kwargs={"scale": 1.0}).images[0]
```

### celda: s08-receta

**Si salió mal, qué mover.** Cambia **una** cosa a la vez, vuelve a correr desde la sección 05 y decide con validation.

| Lo que ves | Qué mover |
|---|---|
| LoRA ≈ base: las mallas casi no cambian y el estilo no sube | más `P["pasos"]`; o `P["lr"]` a $2\cdot10^{-4}$. Mira primero $\lambda=1.5$ en la sección 06: si ahí sí se nota, faltan pasos |
| Imágenes rotas, saturadas o ruido; la loss de validation sube | baja `P["lr"]` a $5\cdot10^{-5}$ |
| Vecino en train muy por encima de la referencia; ves copias de train | menos pasos, más imágenes, o `P["rango"]` más chico (4) |
| CLIP score cae mucho: ignora los prompts | captions más descriptivos y variados en `metadata.csv`; menos pasos |
| Los prompts ajenos salen con tu estilo o se pierden | al generar, $\lambda<1$; menos pasos |
| La loss baja pero las imágenes no se ven como tu estilo | normal al principio: la loss no es calidad. Más pasos, o `MODO = "largo"` |
| Error de memoria (*CUDA out of memory*) | `P["batch"]` a 2, y «Entorno de ejecución → Reiniciar» antes de volver a correr |

- **Lo que no es un bug:** con pocas imágenes los números de CLIP cambian si cambias las semillas. Por eso se leen diferencias grandes y se miran las mallas.
