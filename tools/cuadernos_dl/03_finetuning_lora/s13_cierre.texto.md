### celda: s13-intro

## 13 · Cierre

- **Test, una vez:** la loss de difusión de LoRA $r=8$ sobre los latents de test, el método que se eligió con validation.
- La tabla de todas las corridas, una receta práctica de LoRA y la tarea.

### celda: s13-test-leer

**Cómo leer el resultado**

- Si la loss de test queda cerca de la de validation, validation fue un buen juez para elegir.
- Comparar con el base dice cuánto del estilo se aprendió en datos que nadie miró.
- Las diferencias de loss de difusión suelen ser chicas: léelas contra la de validation y la del base, no en absoluto.
- Si test sale **peor** que el base o muy lejos de validation, es un resultado raro: coméntalo (pocos datos, partición desafortunada, pocos pasos de ruido $K$). No se corrige mirando test otra vez.

### celda: s13-tabla-texto

- Una fila por corrida: método, rango, módulos, learning rate, pasos, loss de validation final, memoria pico, segundos por paso, MB del adaptador, parámetros entrenables y error.
- Compara **loss de validation contra memoria y tamaño**: ese es el intercambio de LoRA.

### celda: s13-receta

**Receta práctica de LoRA (difusión)**

| Perilla | Por dónde empezar | Cuándo moverla |
|---|---|---|
| Rango $r$ | 4–16 | Sube si validation no mejora y el estilo no aparece; baja si memoriza |
| $\alpha$ | $\alpha=r$ (escala 1) | Si cambias $r$, mantener $\alpha/r$ fijo ayuda a no reajustar el learning rate |
| Módulos | Atención: `to_q, to_k, to_v, to_out.0` | Agrega el MLP (`ff.net.*`) si falta capacidad (§8) |
| Learning rate | $10^{-4}$ con AdamW | $10^{-3}$ puede romper la imagen; $10^{-5}$ casi no mueve nada (§9) |
| Schedule | Warmup corto + cosine | Constante sirve para corridas cortas |
| Pasos | Lo que diga la loss de validation y la malla | Para antes de que las caras se vuelvan copias de train (§11) |
| Precisión | LoRA sobre $W_0$ en fp16 | QLoRA solo si no cabe: ahorra memoria, no tiempo |
| Escala $\lambda$ | 1 | $<1$ suaviza el estilo, $>1$ lo exagera (§10) |

- Siempre: semillas fijas para comparar mallas, prompt genérico, y test una vez al final.

### celda: s13-tarea

**Tarea**

1. Corre el notebook en `MODO = "largo"` y comenta qué cambió en las conclusiones con rangos, módulos y learning rates extra.
2. **DreamBooth:** un token raro (`"a sks face"`) más regularización con imágenes del base. ¿Qué cambia frente al prompt genérico?
3. **Textual inversion:** entrena solo un embedding nuevo, sin tocar el UNet. Compara parámetros y resultados con LoRA.
4. **Colorear bocetos:** plantea cómo condicionar el modelo con el boceto de una cara (img2img o ControlNet) para que la coloree.
5. **SDXL:** repite LoRA $r=8$ y compara memoria y tiempo con SD 1.5.
6. **QLoRA en un LLM:** ajusta un modelo de lenguaje chico con QLoRA; la loss es la cross-entropy del notebook 2.
