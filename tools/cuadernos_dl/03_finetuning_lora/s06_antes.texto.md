### celda: s06-intro

## 06 · Antes de entrenar

- El modelo base genera caras con «an anime face». Cada semilla de `P["semillas"]` fija el ruido inicial $x_T$.
- **Cómo leer la malla.** Una columna por semilla. Mira estilo, proporciones y fondo. En s07 volvemos a generar esta referencia con el mismo prompt y las mismas semillas.

### celda: s06-comparar

El modelo base ya puede producir rasgos de anime. LoRA ajusta esa capacidad al estilo del dataset.

| Fila | Prompt | Qué mirar |
|---|---|---|
| 1 | «a face» | Qué estilo elige el modelo por defecto |
| 2 | «an anime face, colorful illustration, detailed» | Cómo cambia al pedir una ilustración detallada |

**Cómo leer la malla.** Compara las dos filas dentro de cada columna. Se usan las dos primeras semillas de la malla anterior.
