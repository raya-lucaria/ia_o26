# Créditos de las imágenes — Aprendizaje de máquina

Los diagramas y las gráficas de esta unidad los produce
`tools/gen_aprendizaje_maquina.py` (las figuras de cada clase viven en
`tools/figuras_ml_c<N>.py`). No se editan a mano: se cambia la función del
generador y se vuelve a correr. Los datos de toda gráfica son sintéticos y
salen de `ml_lab` (`tools/aprendizaje_maquina.py`). Las figuras inspiradas
en un libro se reproducen como idea, con datos propios.

Los notebooks (`.ipynb`), la copia `ml_lab.py` y las páginas HTML de este
directorio no llevan fila: no son imágenes.

Cada bloque `## Clase N` lo llena solo la rama de esa clase.

## Unidad

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-u-mapa.svg` | Mapa de la unidad: las seis clases en orden, con la pregunta de cada una, sus notebooks y su tarea, y al pie los tres hilos que recorren todas las clases | Generado con `tools/gen_aprendizaje_maquina.py` | Propio, CC BY-SA 4.0 |

## Clase 0

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c0-tres-reglas-en-lo-visto.svg` | Cuatro entregas vistas y tres reglas ajustadas con ellas (memorizar, la recta 11 + 3.6x, el promedio de 20 min), su error medio en lo visto y lo que cada una anuncia para 5 y 6 km | Generado con `tools/gen_aprendizaje_maquina.py`; datos de la unidad 6 (seis entregas) y sintéticos de `tools/ml_cifras_c0.py` | Propio, CC BY-SA 4.0 |
| `ml-c0-memorizar-contra-ajustar.svg` | Las mismas tres reglas en las cuatro vistas y en las dos nuevas: error medio 0 / 0.8 / 4 en lo visto y 7 / 1.2 / 12 en lo nuevo | Generado con `tools/gen_aprendizaje_maquina.py`; datos de la unidad 6 (seis entregas) y sintéticos de `tools/ml_cifras_c0.py` | Propio, CC BY-SA 4.0 |
| `ml-c0-con-y-sin-y.svg` | Las seis entregas con la columna de tiempo (supervisado) y sin ella, con dos agrupaciones posibles (no supervisado) | Generado con `tools/gen_aprendizaje_maquina.py`; datos de la unidad 6 (seis entregas) y sintéticos de `tools/ml_cifras_c0.py` | Propio, CC BY-SA 4.0 |
| `ml-c0-jerarquia.svg` | La caja del aprendizaje de máquina de la taxonomía de historia, vista de cerca: aprendizaje de máquina, de representaciones y profundo como rectángulos anidados | Generado con `tools/gen_aprendizaje_maquina.py`; idea de Goodfellow et al., *Deep Learning*, fig. 1.4, como zoom de `v3-taxonomia.svg` | Propio, CC BY-SA 4.0 |
| `ml-c0-quien-elige-phi.svg` | Cuatro maneras de construir un sistema (reglas, clásico, representaciones, profundo) según quién elige la representación y si se arma en capas | Generado con `tools/gen_aprendizaje_maquina.py`; idea de Goodfellow et al., *Deep Learning*, fig. 1.5 | Propio, CC BY-SA 4.0 |

## Clase 1

### Clase 1 · tramo 1a

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c1-ganador-imposible.svg` | Las seis entregas con la recta y el polinomio de grado 5 extrapolados a 7 km: 37.4 contra −25 minutos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos de la unidad 6 (seis entregas) | Propio, CC BY-SA 4.0 |
| `ml-c1-mismo-mundo.svg` | La misma f y tres muestras de 20 entregas con sus rectas ajustadas, sobre observaciones nuevas del proceso | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-reducible.svg` | Diagrama: el residual de una observación partido en la parte reducible y el azar | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`) | Propio, CC BY-SA 4.0 |
| `ml-c1-aprender-es-minimizar.svg` | Veinte entregas con su recta y la pérdida de entrenamiento como función de la pendiente, con su mínimo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 5.1 | Propio, CC BY-SA 4.0 |
| `ml-c1-piso.svg` | Riesgo del oráculo, la recta y la media contra el piso de Bayes, con ruido 1 y 2 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-dos-franjas.svg` | Entregas sin y con la lluvia coloreada: dos franjas paralelas y el piso de 10 a 1 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-cuatro-fuentes.svg` | Diagrama de las cuatro fuentes del error (azar, lo que no se mide, aproximación, estimación) y, aparte, la optimización | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`) | Propio, CC BY-SA 4.0 |
| `ml-c1-anillos-polares.svg` | La misma regresión logística sobre dos anillos en cartesianas y en polares, con sus aciertos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 1.1 | Propio, CC BY-SA 4.0 |
| `ml-c1-matriz-phi.svg` | Diagrama: tres matrices de diseño de las seis entregas y la misma multiplicación Φβ | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos de la unidad 6 (seis entregas) | Propio, CC BY-SA 4.0 |

### Clase 1 · tramo 1b

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

### Clase 1 · tramo tarea

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

## Clase 2

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

## Clase 3

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

## Clase 4

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c4-moda-99.svg` | Mosaico de 100 mensajes con un fraude: la regla «siempre legítimo» y sus aciertos, aciertos balanceados y MCC | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); diagrama propio; idea de las presentaciones del profesor (07·19/30) y de Goodfellow et al., *Deep Learning*, §11.1 | Propio, CC BY-SA 4.0 |
| `ml-c4-separable.svg` | Curvas p̂(x) del caso separable con tres μ y la norma de las pendientes estandarizadas contra log₁₀ μ, separable y con ruido | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, §7.3 | Propio, CC BY-SA 4.0 |
| `ml-c4-cadena-decision.svg` | Diagrama: del dato a la etiqueta, con la pérdida, el umbral y la métrica | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); diagrama propio; idea de las presentaciones del profesor (07·14–17) | Propio, CC BY-SA 4.0 |
| `ml-c4-perdida-vs-metrica.svg` | Pérdida logarítmica, aciertos y MCC contra la pendiente, con el intercepto reoptimizado | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, §8.1.2 | Propio, CC BY-SA 4.0 |
| `ml-c4-umbral.svg` | Histogramas de p̂ por clase y MCC, aciertos balanceados y aciertos contra el umbral | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de los notebooks del profesor | Propio, CC BY-SA 4.0 |
| `ml-c4-contribucion-clases.svg` | Fracción de casos, de peso total y pérdida media por clase a 50 % y 1 % de fraude | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de las presentaciones del profesor (07·64) | Propio, CC BY-SA 4.0 |
| `ml-c4-metricas-vs-proporcion.svg` | MCC, aciertos balanceados y aciertos de la moda y de la logística sin y con pesos contra la proporción de fraude, con la banda de validación | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de los notebooks del profesor | Propio, CC BY-SA 4.0 |
| `ml-c4-pesos-umbral.svg` | Fronteras con pesos y con umbral equivalente, intercepto contra ln(w₁/w₀) y métricas contra la razón de pesos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de Elkan (2001) | Propio, CC BY-SA 4.0 |
| `ml-c4-anillos-metricas.svg` | El caso 25: fronteras lineal sin y con pesos y cuadrática con pesos, con su MCC en el despliegue | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 1.1 | Propio, CC BY-SA 4.0 |
| `ml-c4-mcc-por-pliegue.svg` | MCC y aciertos balanceados de cada pliegue de una CV estratificada con k = 3, 5 y 10 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c4-softmax.svg` | Diagrama: regresión softmax con tres clases | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); diagrama propio; redibujo con la notación del curso de las presentaciones del profesor (07·40–43) | Propio, CC BY-SA 4.0 |
| `ml-c4-fronteras-tres-clases.svg` | Regiones de decisión de softmax con tres clases 90/8/2, sin y con pesos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de las presentaciones del profesor (07·39) | Propio, CC BY-SA 4.0 |
| `ml-c4-macro-ponderado.svg` | Aciertos por clase del ejemplo de noticias con sus promedios macro y ponderado | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); cifras recalculadas del ejemplo de las presentaciones del profesor (07·57–63) | Propio, CC BY-SA 4.0 |
| `ml-c4-recuadro-confusion.svg` | Matriz de confusión, curva ROC y curva PR del modelo del bloque 2 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c4-confiabilidad.svg` | Curvas de confiabilidad sin pesos, con pesos, la verdadera y el benchmark en val_b | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab`; idea de los notebooks del profesor | Propio, CC BY-SA 4.0 |
| `ml-c4-tasa.svg` | Tasa de interés de equilibrio contra la probabilidad anunciada, con el cliente típico sin y con pesos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); curva cerrada; idea de los notebooks del profesor | Propio, CC BY-SA 4.0 |
| `ml-c4-mapa-reservas.svg` | Diagrama: el mapa único de reservas (ent, val_a, val_b, cal, prueba) y qué ajusta cada pieza | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); diagrama propio | Propio, CC BY-SA 4.0 |
| `ml-c4-conformal-rangos.svg` | Diagrama: cinco puntajes de calibración, el corte y los puntajes de un mensaje nuevo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); diagrama propio; idea de Angelopoulos y Bates, *A Gentle Introduction to Conformal Prediction* | Propio, CC BY-SA 4.0 |
| `ml-c4-conformal-conjuntos.svg` | Tamaño de C(x) por región con tres clases iguales y la cobertura medida contra 1 − δ | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c4-cobertura-por-clase.svg` | Cobertura por clase en el despliegue, marginal y por clase, promediada sobre 30 calibraciones | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c4.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |

## Clase 5

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
