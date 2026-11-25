### celda: s12-intro

## 12 · ¿Olvidó lo que sabía?

`lora_r8` se entrenó con el prompt «an anime face». Comparamos el base y el adaptado con prompts fuera de ese dominio y semillas emparejadas. El **CLIP score** mide la alineación imagen–prompt: $100\times$ el coseno entre sus embeddings.

| Qué ves al activar LoRA | Interpretación |
|---|---|
| El perro sigue siendo reconocible y adquiere estilo anime | Interferencia de estilo |
| El perro deja de ser reconocible | Indicio de pérdida de capacidad con el adaptador activo |

Los efectos pueden ser sutiles si el adaptador cambia poco la salida o si CLIP sigue reconociendo el objeto pese al cambio de estilo. **Interferencia no es olvido:** LoRA no borra nada de $W_0$ y con $\lambda=0$ recuperamos el base (sección 10). Un perro «anime» es interferencia: $\Delta W$ actúa en la atención para cualquier prompt. Solo si el objeto deja de reconocerse con el adaptador activo hablamos de olvido.

**Cómo leer la malla.** Para cada prompt, el base va arriba y `lora_r8` abajo. Cada columna conserva la semilla.

### celda: s12-que-viste

**Qué viste**

- Una diferencia `lora_r8 − base` negativa indica menor alineación según CLIP. Revisa la malla para ver si se pierde el objeto pedido o cambia su estilo.
- Con pocas semillas, las diferencias pequeñas pueden variar entre muestras. La fila «(dominio)» muestra la comparación de scores con el prompt de entrenamiento.
