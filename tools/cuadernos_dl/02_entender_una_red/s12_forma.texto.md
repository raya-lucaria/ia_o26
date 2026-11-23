### celda: s12-intro

## 12 · La forma de la red

![Una red en forma de embudo](ilustracion:embudo)
*(Ilustración generada con gpt-image-2.)*

Las cinco formas reparten **unos 102 mil parámetros** de maneras distintas.
Con $d_l$ neuronas en la capa $l$, el total es $\sum_{l=1}^{L}d_l(d_{l-1}+1)$, incluidos los sesgos.
La primera capa oculta concentra la mayoría, pues cada neurona recibe los 784 píxeles.
El cuello de dos neuronas también añade profundidad. Las curvas comparan el ajuste alcanzado en ocho epochs.

### celda: s12-apuesta

**Apuesta.** ¿Qué forma tendrá más aciertos en validation y cuál menos?
Elige entre embudo, embudo invertido, cuello de dos, rectangular y una capa oculta. Justifica en una frase.

### celda: s12-entrenar-explica

**Misma receta para las cinco formas.** Todas usan ReLU, inicialización de He y Adam.
Comparten learning rate, tamaño de batch, número de epochs y semillas.
El subconjunto estratificado de train conserva la representación de los diez dígitos.

### celda: s12-curvas-lee

**Compara las formas en la misma epoch.** Los paneles de cada figura comparten escala.
Busca si el cuello ajusta peor incluso en train. Eso apunta a underfitting.
Test se reporta una sola vez, al final. Aquí se grafica para practicar. El checkpoint se elige por loss de validation.

### celda: s12-apuesta-respuesta

**El cuello ajustó peor** en train y validation. Las otras cuatro formas quedaron cerca.
El cuello comprime cada imagen a dos activaciones. La profundidad adicional también puede dificultar la optimización.

### celda: s12-que-viste

- El cuello quedó atrás pese a tener **una brecha de accuracy parecida** a las demás.
- Las cuatro formas sin cuello casi empataron en validation. En otra corrida puede cambiar su orden.
- Las curvas dejan abierta la contribución de la capacidad y de la dificultad de optimización.
