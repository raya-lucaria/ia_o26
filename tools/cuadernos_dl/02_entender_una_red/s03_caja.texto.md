### celda: s03-intro

## 03 · La caja de herramientas

- `construir_red` recibe los anchos de las capas. Con `[784, 10]` obtienes una regresión logística multiclase.
- Cada capa oculta aplica `nn.Linear` y luego una activación, como ReLU, $\max(0,z)$. Si las activas, batch normalization va antes de la activación y dropout después.
- **La última capa entrega logits**, uno por dígito.
- La inicialización He usa varianza $2/d_{l-1}$, con $d_{l-1}$ el ancho anterior. He y la inicialización ortogonal ponen los sesgos en cero.

### celda: s03-punta-a-punta-explica

- **Cada dígito ocupa una fila.** El notebook 01 usaba columnas, con $\mathbf z=\mathbf W\mathbf x+\mathbf b$. Aquí usamos `xb @ W.T + b`.
- `CrossEntropyLoss` recibe logits y etiquetas enteras. Su loss es el promedio de $-\log \widehat p_{k,y_k}$ tras aplicar softmax.
- `argmax(dim=1)` predice el dígito con mayor logit en cada fila. Con probabilidades uniformes, la loss sería $\log 10 \approx 2.30$.

### celda: s03-loop-explica

- **Un batch produce una actualización.** `zero_grad()` borra lo acumulado antes del forward y el cálculo de la loss.
- `backward()` calcula los gradientes. Con SGD, `step()` aplica $p \leftarrow p - \eta\,\nabla_p L_{\mathcal B}$, como en el notebook 01.
- La demo muestrea con reemplazo. `entrenar` baraja train y recorre sus $n$ ejemplos en $\lceil n/B\rceil$ batches. Con batch normalization, un batch final de un ejemplo se fusiona con el anterior.

### celda: s03-config-explica

- **`Config` define la corrida.** `id` y `seccion` son obligatorios. Puedes fijar la red, los datos, las semillas y el presupuesto.
- `config_profunda` prepara las redes de las secciones 13 a 15 con SGD e inicialización ortogonal.
- `Corrida` guarda el historial y dos checkpoints. Uno corresponde a la menor loss de validation y otro a la última evaluación.
- Al repetir un `id`, `CORRIDAS` reemplaza el resultado anterior.

### celda: s03-evaluar-explica

- **`medir` calcula loss y accuracy sin gradientes**, en modo `eval()`. Dropout se apaga y batch normalization usa sus estadísticas acumuladas.
- `crear_optimizer` aplica weight decay a matrices y filtros. `adam_l2` suma la penalización al gradiente y `adamw` aplica el decaimiento por separado.
- `cargar(corrida, "mejor")` recupera el checkpoint elegido con validation. Usa `"ultima"` para recuperar el último.

### celda: s03-entrenar-explica

- `entrenar` prepara train con la escala, el subconjunto y el ruido de etiquetas solicitados. Mide antes de actualizar los pesos y luego por epoch o por pasos.
- **La loss de validation elige el mejor checkpoint** y activa early stopping si se agota la paciencia. Una loss no finita también detiene la corrida.
- El reloj mide solo el entrenamiento. Con `medir_por_paso` se guardan dos medidas por capa. Son la norma del gradiente y el cambio relativo $\lVert \mathbf W_{t+1}-\mathbf W_t\rVert/\lVert \mathbf W_t\rVert$.

### celda: s03-graficas-explica

- `curvas` muestra loss o accuracy por epoch, pasos, ejemplos vistos o tiempo. `rejilla` dibuja un panel por corrida.
- **`tabla_maestra` compara las corridas en su mejor evaluación según validation.** La brecha es la accuracy de train menos la de validation.
- `dibujar_red` usa una columna por capa. Los puntos suspensivos indican nodos omitidos.

### celda: s03-demo-explica

**Ubica el punto de partida en la epoch 0.** En el otro panel, sigue la red desde los píxeles hasta los logits.
Usa test una vez al final. Aquí se grafica por epoch solo para practicar la lectura de curvas.

### celda: s03-que-viste

Qué viste

- **La loss baja en los tres conjuntos.** La caída es mayor al comienzo.
- Las curvas siguen juntas. En otra corrida, validation puede dejar de mejorar mientras train sigue bajando.
