### celda: s17-intro

## 17 · Una red convolucional, breve

Un MLP recibe una lista de $784$ píxeles. Una CNN aprovecha su **vecindad con pesos compartidos**.
Cada filtro recorre la imagen con una ventana de $3\times3$ y puede detectar el mismo trazo en distintas posiciones.

![Un filtro recorriendo un dígito](ilustracion:filtro)
*(Ilustración generada con gpt-image-2.)*

### celda: s17-filtro-lee

Los recuadros enlazan cada ventana del dígito con su posición en el mapa de salida.
El **filtro de bordes verticales** resta la tinta de la izquierda a la de la derecha. Aquí $b=0$.

$$z_{rc}=\sum_{u=-1}^{1}\sum_{v=-1}^{1}w_{uv}\,x_{r+u,c+v}+b.$$

Un borde de ceros de un píxel conserva el tamaño del mapa. PyTorch aplica los pesos tal como están escritos.
En una CNN, backpropagation ajusta los pesos y sesgos de cada filtro.

### celda: s17-arquitectura-lee

- `Unflatten` recompone la cuadrícula de $28\times28$ con un canal.
- La primera convolución produce $16$ mapas y tiene $16(9+1)=160$ parámetros.
- ReLU pone los negativos en cero. **Max-pooling** conserva el máximo de cada bloque de $2\times2$.
- La segunda convolución combina los $16$ canales con $32$ filtros y suma $32(16\cdot3\cdot3+1)=4\,640$ parámetros.
- Tras ReLU y max-pooling quedan $32\cdot7\cdot7=1\,568$ rasgos. La capa densa produce diez logits con $10(1\,568+1)=15\,690$ parámetros.

### celda: s17-apuesta

**Apuesta.** ¿La CNN ganará, empatará o perderá frente al MLP en accuracy de validation?
¿Cuál tendrá mayor brecha entre train y validation al final, o serán similares?

### celda: s17-curvas-lee

El MLP está a la izquierda y la CNN a la derecha. Cada fila comparte escala vertical.
**Busca overfitting** si la loss de train baja mientras la de validation sube.
La tabla usa el checkpoint de menor loss de validation. La CNN copia la escala, el batch y el presupuesto.
Revisa el optimizer y el learning rate de cada red antes de atribuir la diferencia a la arquitectura.
Test por epoch es didáctico. En un proyecto, decide con validation y mira test una vez al final.

### celda: s17-filtros-lee

- Los filtros usan una escala común. Rojo indica pesos positivos, azul negativos y blanco cercanos a cero.
- Cada **mapa de activación** muestra la respuesta de un filtro después de ReLU y antes de max-pooling.
- Los mapas tienen escalas propias. Compara dónde responden y qué parte del trazo resaltan.
- La CNN recibe el dígito en su escala de entrenamiento. Si está estandarizado, el fondo también puede activar filtros.

### celda: s17-que-viste

**Qué viste**

- Ambas losses de validation cayeron al inicio. La accuracy terminó alta en las dos redes.
- Algunos filtros resaltaron bordes o partes del trazo. Otros produjeron respuestas más dispersas.
- La CNN redujo los errores en casi todos los dígitos, especialmente en el 3. Se equivocó más en el 6.
- En otra corrida pueden cambiar los dígitos que más se benefician. Compara las casillas leyendo fila real y columna predicha.

### celda: s17-apuesta-respuesta

Debajo de la tabla se imprime CNN menos MLP. Aquí **la CNN ganó en accuracy** con menos parámetros.
Su brecha final entre train y validation fue pequeña, como la del MLP.
Con otra semilla puede haber empate o una ventaja para el MLP.
