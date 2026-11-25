### celda: s08-intro

## 08 · Dónde poner LoRA

- LoRA no va en todo el UNet: va en las capas lineales que nombra `target_modules`. Aquí, por omisión, las cuatro proyecciones de atención `to_q, to_k, to_v, to_out.0`.
- El UNet tiene tres zonas: **down** (baja la resolución), **mid** (la más chica) y **up** (la sube y reconstruye el detalle).
- Cada zona tiene **self-attention** (`attn1`: la imagen consigo misma) y **cross-attention** (`attn2`: la imagen consulta el texto del prompt).
- Medimos cuánto se movió cada capa relativo a su tamaño:

$$\frac{\lVert\Delta W\rVert_F}{\lVert W_0\rVert_F},\qquad \lVert M\rVert_F=\sqrt{\textstyle\sum_{ij}M_{ij}^2}$$

**Cómo leer la gráfica.** Izquierda: una barra por capa, en orden down → mid → up, color por zona. Derecha: el promedio por zona y tipo de atención. Es una sola corrida y no hay barras de error: diferencias chicas entre zonas pueden ser ruido.

### celda: s08-variantes

**➕ Tres lugares para el mismo adaptador** (mismo rango, lr, pasos y semilla):

| Corrida | `target_modules` | Qué cambia |
|---|---|---|
| `lora_r8` | atención en todo el UNet | la referencia de §07 |
| `s08_atencion_mlp` | atención + `ff.net.0.proj`, `ff.net.2` | también el MLP de cada bloque: más parámetros |
| `s08_solo_up` | atención solo en `up_blocks` | solo la mitad que reconstruye: menos parámetros |

- `s08_solo_up` pasa en `modulos` una **regex**, `up_blocks\..*\.(to_q|to_k|to_v|to_out\.0)`: peft la compara con el nombre completo de cada capa, así que solo entran las de `up_blocks`.
- **Qué podría pasar.** Más capas no garantiza menor loss de validation: con pocos pasos las tres curvas pueden quedar casi encimadas. Si `s08_solo_up` queda cerca de `lora_r8`, el estilo vive sobre todo en la parte que reconstruye; si queda claramente arriba, también hace falta mover down y mid.

### celda: s08-que-mirar

**Qué mirar**

| Dónde | Pregunta |
|---|---|
| Columna de parámetros entrenables y MB | ¿Cuánto cuesta cada opción? |
| Curvas de validation | ¿Alguna baja más, o son indistinguibles? |
| Tabla por zona | ¿El cambio se concentra en las mismas zonas en las tres corridas? |
| Malla | A igual semilla, ¿cambia el estilo o solo detalles? |

- Si una opción más barata da curva y malla parecidas, es la que conviene: menos parámetros, archivo más chico.
