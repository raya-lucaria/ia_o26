### celda: s08-intro

## 08 · Testeo, una sola vez

- **Esta es la única vez que se usa el test.** Todo lo anterior (curvas, métricas, la perilla) se decidió con validation. Ya no cambies nada por lo que veas aquí: si lo haces, este número deja de ser honesto.
- La tabla tiene las mismas métricas de §07, ahora en ejemplos que **nadie** miró antes.
- Esperamos números parecidos a los de validation. Si test sale mucho peor, validation se usó de más para decidir (o los dos conjuntos son muy chicos y el azar pesa).

### celda: s08-prompts-explica

**Tus prompts, antes y después.** Los de `prompts.txt` no están en el dataset: es lo más cercano a cómo usarías el modelo de verdad. La columna `base` es la misma de §03.

### celda: s08-olvido-explica

**Olvido.** Ajustar un modelo a tu tarea puede hacerle **perder** algo de lo que ya sabía (*catastrophic forgetting*). LoRA lo limita, porque $W_0$ no se mueve, pero no lo impide.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| si el modelo sigue contestando bien preguntas **ajenas** a tu dataset | sin número: se lee | respuestas de LoRA tan buenas como las del base | tres preguntas son una muestra mínima; y un LoRA que contesta todo **en el formato de tu dataset** (todo en SQL, todo en verso) también es olvido, aunque la respuesta no sea falsa |

**Cómo leer la tabla:** busca si LoRA cambió el estilo (más corto, en el formato de tus datos) o el contenido (datos falsos). Lo primero es común y a veces es lo que querías; lo segundo es olvido de verdad.

### celda: s08-guardar-explica

**Tu adaptador.** Se guarda solo lo que entrenaste: $A$ y $B$ de cada capa (`adapter_model.safetensors`), la configuración (`adapter_config.json`) y una ficha con tu dataset y tus números de test. Lo descargas como `mi_lora_texto.zip`.

Para usarlo otro día, en cualquier máquina con el mismo modelo base:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
modelo = PeftModel.from_pretrained(base, "mi_lora_texto")
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
```

(En `MODO = "largo"`, el base es `Qwen/Qwen2.5-1.5B-Instruct`.) Si Colab no abre la descarga, búscala en el panel 📁 Archivos: clic derecho → Descargar.

### celda: s08-receta

**Si salió mal, qué mover**

| Lo que ves | Qué pasa | Qué mover |
|---|---|---|
| validation casi no baja desde el paso 0 | el base ya contestaba así, o la tarea es difícil para este modelo | más `pasos`; `MODO = "largo"` (modelo de 1.5B y LoRA en el MLP) |
| train baja y validation sube al final | memoriza train | menos `pasos`; más datos |
| loss en `nan` o el aviso de pasos saltados | fp16 se desbordó | baja `lr` a `1e-4` |
| las respuestas no paran hasta `max_new` | no aprendió a terminar | más `pasos`; revisa que tus completions no traigan relleno al final |
| las respuestas salen cortadas a media frase | el tope `max_new` | sube `P["max_new"]` |
| muchos ejemplos «cortados» en §05 | `max_len` corta tus ejemplos | acorta prompts o completions; o sube `P["max_len"]` (más memoria) |
| exact match 0 con F1 alto | casi bien, falla un detalle | lee los ejemplos; quizá tu tarea pide F1, no exact match |
| LoRA contesta todo en tu formato (§08, olvido) | se pasó de ajuste | menos `pasos`, o $\lambda<1$ al generar (§06) |
| memoria agotada (*CUDA out of memory*) | ejemplos largos o modelo grande | baja `P["batch"]` a 2 y sube `P["acum"]` a 4: mismo batch efectivo |

### celda: s08-cierre

**Lo que te llevas**

- Un LoRA de $r=8$ mueve una fracción mínima del modelo y aun así cambia **cómo contesta**: primero el formato, luego el contenido.
- La loss solo en el completion le enseña a responder, no a repetir tus preguntas.
- $\Delta W$ tiene rango $\le r$, se puede **subir o bajar** con $\lambda$, y se **fusiona** sin costo.
- Cada métrica tiene su trampa: loss y perplexity no generan, exact match es todo o nada, F1 ignora el orden, y el olvido hay que leerlo.
- El test se usa **una vez**. Lo que muestres de este notebook es ese número.
