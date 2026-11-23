### celda: s12-intro

## 12 · La forma de la red

![Una red en forma de embudo](ilustracion:embudo)
*(Ilustración generada con gpt-image-2.)*

- Cinco formas reparten **unos 102 mil parámetros**.
- Con $d_l$ neuronas en la capa $l$, el total con sesgos es $\sum_{l=1}^{L}d_l(d_{l-1}+1)$.
- La primera capa oculta concentra la mayoría porque cada neurona recibe los 784 píxeles.

### celda: s12-apuesta

- **Apuesta.** ¿Qué forma acertará más en validation y cuál menos?
- Elige entre embudo, invertido, cuello de dos, rectangular y una capa oculta. Justifica en una frase.

### celda: s12-entrenar-explica

- **Misma receta para las cinco formas.** ReLU, inicialización He, Adam, learning rate, batch, semillas y ocho epochs.
- El subconjunto estratificado de train conserva la representación de los diez dígitos.

### celda: s12-curvas-lee

- **Compara las formas en la misma epoch.** Los paneles comparten escala.
- Una loss más alta incluso en train apunta a underfitting.
- Elige el checkpoint por loss de validation. Test se grafica para practicar y se reserva para el informe final.

### celda: s12-apuesta-respuesta

- **El cuello ajustó peor** en train y validation. Las otras cuatro formas quedaron cerca.
- El cuello comprime a dos activaciones y añade profundidad. Ambos cambios pueden afectar el ajuste.

### celda: s12-que-viste

- **El cuello quedó atrás con una brecha de accuracy parecida** a las demás.
- Las formas sin cuello casi empataron. Su orden puede cambiar en otra corrida.

| Forma | Capas ocultas | Qué se ve en las curvas |
| --- | --- | --- |
| Embudo | Se estrecha | Loss baja pronto |
| Invertido | Se ensancha | Loss baja pronto |
| Cuello de dos | Comprime y ensancha | Loss baja despacio |
| Rectangular | Ancho constante | Loss baja pronto |
| Una capa | Sin capas ocultas adicionales | Loss baja pronto |
