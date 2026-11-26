### celda: s07-intro

## 07 · Métricas, explicadas

Compara **base y LoRA en validation**. Si piensas probar ajustes, ejecuta hasta esta sección y reserva la 08 para tu configuración final. Para evaluar las generaciones, `generadas` recorre los captions del split y vuelve al primero si necesita más. Base y LoRA reciben las mismas parejas de caption y semilla.

CLIP representa imágenes y texto mediante embeddings. Con vectores normalizados $u$ y $v$, su similitud es $\cos(u,v)=u^\top v\in[-1,1]$. Un valor alto indica cercanía en el espacio de CLIP. Con pocas muestras, una sola imagen puede mover el promedio. Lee cada cifra junto con las mallas.

### celda: s07-loss-explica

**Loss de difusión**

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| MSE entre el ruido añadido a los latents reales y el ruido que predice el UNet. | $[0,\infty)$ | Una loss menor que la del base indica mejor denoising en esta evaluación. | Depende de los pares de ruido elegidos. Puede bajar aunque las generaciones sigan lejos del estilo buscado. |

Se reutiliza `perdida` de la sección 05 con los mismos pares $(t,\varepsilon)$ para ambos modelos.

### celda: s07-clipscore-explica

**CLIP score**

Para cada pareja, compara el embedding de la imagen generada $g_i$ con el de su caption $c_i$. El código promedia los cosenos y multiplica por cien.

$$
\text{CLIP score}=\frac{100}{N}\sum_{i=1}^N\cos(g_i,c_i).
$$

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Correspondencia entre la imagen generada y el caption, según CLIP. | $[-100,100]$ | LoRA mantiene o mejora la correspondencia con respecto al base. | Con captions genéricos, una imagen genérica puede puntuar bien. CLIP puede pasar por alto detalles del prompt o del estilo. |

### celda: s07-estilo-explica

**Parecido al estilo**

La celda promedia y normaliza los embeddings de las imágenes reales del split evaluado para obtener su centroide $m$. Luego promedia $\cos(g_i,m)$ sobre las imágenes generadas. La **referencia** calcula ese mismo promedio para las imágenes reales de **train** frente al mismo centroide.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Cercanía de las generaciones al centro del split real en el espacio de CLIP. | $[-1,1]$ | LoRA supera al base y se acerca a la referencia de train. | El centroide mezcla tema, encuadre y estilo. Repetir un motivo frecuente o copiar ejemplos puede elevar la cifra. |

### celda: s07-memoria-explica

**Vecino más cercano en train**

Para cada imagen, toma el mayor coseno CLIP con una imagen real de **train** y promedia esos máximos. La **referencia** aplica la misma operación a imágenes reales del split evaluado, aquí **validation**.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Qué tan cerca suele quedar una generación de algún ejemplo de train. | $[-1,1]$ | Si LoRA se parece más al estilo y queda cerca de la referencia, hay menos indicios de copia. | En un dataset homogéneo, una imagen nueva también puede tener un vecino cercano. Un coseno alto indica similitud en CLIP. |

Si LoRA supera ampliamente la referencia, busca parecidos concretos con train antes de atribuirlo a memorización.

### celda: s07-olvido-explica

**Olvido con el adaptador activo**

La celda compara el CLIP score de base y LoRA en tres prompts ajenos, con las mismas semillas para ambos modelos. Si alguno de los temas coincide con tu dataset, cambia `PROMPTS_AJENOS` antes de evaluar.

| Qué mide | Rango | Qué es bueno | Trampa |
|---|---|---|---|
| Si las imágenes de temas ajenos siguen correspondiendo a sus prompts al activar LoRA. | Score en $[-100,100]$. La diferencia LoRA menos base está en $[-200,200]$. | Scores parecidos por prompt. | Cambiar el estilo también puede alterar el score. Una media estable puede ocultar un prompt que empeoró. |

### celda: s07-resumen-explica

**Cómo leer la tabla.** La diferencia «LoRA − base» tiene un sentido distinto en cada fila. Una loss puede bajar, el parecido al estilo subir y el vecino en train mantenerse cerca de su referencia. Revisa también si los captions y los prompts ajenos se siguen respetando. Las dos referencias de la tabla responden a preguntas distintas, descritas junto a cada métrica.

**Cómo leer la malla.** Cada columna usa un caption de validation. Arriba ves la imagen real. En las dos filas inferiores, base y LoRA generan con el mismo caption y la misma semilla.
