# Créditos de las imágenes — Aprendizaje profundo

Los diagramas SVG de esta unidad los produce `tools/gen_deep_learning.py`. No
se editan a mano: se cambia la función del generador y se vuelve a correr
(`tools/test_gen_deep_learning.py` los regenera antes de revisarlos). Toda
cifra de una figura sale de `tools/redes.py`: las curvas de `dl-curvas-rmse.svg`
son `redes.entrenar_ejemplo()` sin μ y con μ, y una prueba coteja cada punto.

Los notebooks (`.ipynb`) de este directorio no llevan fila: no son imágenes.

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `dl-red-2-3-2-1.svg` | La red 2–3–2–1 del hilo: capas 0 a 3 con su ancho d_l, cada neurona rotulada aᵢ⁽ˡ⁾, todas las flechas de peso, w₁₁⁽¹⁾ y w₃₂⁽¹⁾ rotulados y el tamaño de cada W⁽ˡ⁾ | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-peso-wij.svg` | Un peso de cerca: de aⱼ⁽ˡ⁻¹⁾ (origen j, capa l − 1) a zᵢ⁽ˡ⁾ (destino i, capa l), la suma de zᵢ⁽ˡ⁾ y cómo se leen los tres índices de wᵢⱼ⁽ˡ⁾ | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-matriz-w.svg` | W⁽¹⁾ en forma general, 3×2, con filas «destino i» y columnas «origen j» rotuladas; la fila 3, la columna 2 y su cruce w₃₂⁽¹⁾ como flechas de la red | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-composicion.svg` | La red como cadena de funciones x → f⁽¹⁾ → a⁽¹⁾ → f⁽²⁾ → a⁽²⁾ → f⁽³⁾ → ŷ → ℓ, con W⁽ˡ⁾ y b⁽ˡ⁾ entrando a cada capa | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-retropropagacion.svg` | La misma cadena con el pase hacia atrás debajo: δ⁽³⁾ → δ⁽²⁾ → δ⁽¹⁾ con W⁽ˡ⁺¹⁾ᵀ y ⊙ g⁽ˡ⁾′, y los gradientes de W⁽ˡ⁾ y b⁽ˡ⁾ | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-ciclo.svg` | El ciclo de entrenamiento en cinco pasos: adelante, pérdida, atrás, gradientes, actualizar θ, con el lote al centro como entrada | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
| `dl-curvas-rmse.svg` | RMSE de entrenamiento y de validación contra época, sin μ y con μ, con el mínimo de validación marcado | Generado con `tools/gen_deep_learning.py` | Propio, CC BY-SA 4.0 |
