### celda: s07-intro

## 07 · Métricas, explicadas

Mirar mallas convence, pero no mide. Aquí van cinco números; para cada uno, **qué mide, en qué rango vive, qué es bueno y cuál es su trampa**. Todos se calculan en **validation**, que es el conjunto para mirar y decidir.

**Con qué se mide.** Casi todas usan **CLIP** (`openai/clip-vit-base-patch32`), un modelo que lleva imágenes y textos al mismo espacio de vectores: si una imagen y un texto «dicen lo mismo», sus vectores apuntan parecido. Con vectores de norma 1, el parecido es el coseno:

$$\cos(u,v)=u^\top v\in[-1,1].$$

**Qué se genera.** `generadas` toma `P["n_gen"]` captions de validation (en ciclo, si hay menos) y genera una imagen por caption con el base y con LoRA, con las **mismas** parejas (caption, semilla). Así cada diferencia entre las dos columnas es del adaptador.

- Con pocas imágenes los números brincan de una corrida a otra. Lee diferencias grandes, no la tercera cifra decimal.

### celda: s07-loss-explica

**1 · Loss de difusión (validation)**

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| qué tan bien predice el UNet el ruido sumado a **tus** imágenes de validation, con $(t,\varepsilon)$ fijos | $\ge 0$ | **más baja** que la del base | **no es calidad visual**: una baja chica puede venir con imágenes muy cambiadas, y al revés. Además depende de qué $t$ se fijaron |

- Es la misma función `perdida` de la sección 05, una vez con el adaptador apagado y otra prendido.

### celda: s07-clipscore-explica

**2 · CLIP score**

$$\text{CLIP score}=\frac{100}{N}\sum_{i=1}^{N}\cos\big(\text{imagen}_i,\ \text{caption}_i\big).$$

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| si cada imagen generada **corresponde a su caption**, según CLIP | $[-100,100]$; con este CLIP suele quedar entre 20 y 35 | alto, y que LoRA **no caiga** mucho frente al base | premia «que se vea el objeto», no el estilo: una foto genérica de una cara puede sacar más que tu ilustración. Si tus captions son todos iguales, mide solo eso |

### celda: s07-estilo-explica

**3 · Parecido al estilo**

Se promedian los vectores CLIP de las imágenes **reales** de validation y se normaliza: es el centroide $\bar e$, «cómo se ve tu dataset». Luego:

$$\text{estilo}=\frac{1}{N}\sum_{i=1}^{N}\cos\big(\text{generada}_i,\ \bar e\big).$$

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| si las generadas **se parecen a tus imágenes reales** en conjunto | $[-1,1]$; más cerca de 1, más parecido | LoRA **más alto** que el base, acercándose a la referencia | un modelo que copia train saca un valor altísimo. Por eso va junto con la métrica 4 |

- **Referencia:** el mismo número para tus imágenes reales de train. Es «cuánto se parece algo de verdad de tu dataset».

### celda: s07-memoria-explica

**4 · Memorización: el vecino más cercano en train**

Para cada imagen generada se busca la imagen de **train** más parecida según CLIP, y se guarda ese coseno máximo. Se promedia.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| si las generadas son **copias** de imágenes de train | $[-1,1]$; cerca de 1 es casi la misma imagen | **cerca de la referencia** | si tu dataset es muy homogéneo (todas casi iguales), cualquier imagen del estilo tiene un vecino cercano: por eso hay referencia |

- **Referencia:** el mismo número para imágenes **reales de validation**, que el modelo nunca vio. Ese es el parecido «honesto» al vecino: una imagen nueva de tu estilo.
- Si LoRA queda **muy por encima** de la referencia, está repitiendo train. Con pocas imágenes y muchos pasos es lo que pasa.

### celda: s07-olvido-explica

**5 · Olvido: prompts ajenos**

Se generan imágenes para tres prompts que no tienen nada que ver con tu dataset, con el base y con LoRA, mismas semillas, y se compara su CLIP score.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| si el adaptador **estropea** lo que el modelo ya sabía hacer | como el CLIP score | LoRA ≈ base | un perro «con tu estilo» baja un poco el score sin que el modelo haya olvidado nada: eso es interferencia, no olvido. Olvido es que **el perro deje de verse** |

- LoRA no borra nada de $W_0$: con el adaptador apagado (o $\lambda=0$) vuelve el base tal cual. El «olvido» aquí es lo que pasa **con el adaptador prendido**.

### celda: s07-resumen-explica

**Todo junto, en validation.** Una fila por métrica, con base, LoRA, la referencia cuando la hay, la diferencia y qué es bueno. Debajo, cuatro imágenes de validation: la real, la del base y la de LoRA con el mismo caption y semilla.

**Cómo leer la tabla.** Ninguna métrica sola dice «salió bien». Un buen LoRA de estilo suele verse así: loss un poco más baja, estilo más alto, CLIP score parecido, vecino en train cerca de la referencia y olvido ≈ base. Si algo no cuadra, la receta de la sección 08 dice qué mover.
