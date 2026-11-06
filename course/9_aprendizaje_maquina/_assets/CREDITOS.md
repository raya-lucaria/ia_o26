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

## Clase 5

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c5-modelo-exitoso.svg` | Diagrama: tres requisitos de un modelo exitoso; los dos primeros (clases 1 a 4) atenuados y el tercero, la prueba imita la realidad, encendido | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de la diapositiva 04-33 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c5-bolsas.svg` | Diagrama: cuatro maneras de sacar bolas de una bolsa (iid, a puñados, una bolsa que se tiñe, otra bolsa), en dos grupos: la muestra y el uso | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de la diapositiva 03-38 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c5-detectores.svg` | Tres detectores (validación adversarial, KS por variable, residuales contra t con su autocorrelación) con el mismo proceso y con deriva | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` y `tools/ml_cifras_c5.py` | Propio, CC BY-SA 4.0 |
| `ml-c5-particiones.svg` | Diagrama: tres rejillas de cinco pliegues, al azar, por grupos y temporal | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; plantilla de rejilla de la diapositiva 05-07 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c5-cv-miente.svg` | CV al azar, CV por grupos o temporal y R en el despliegue para el modelo de la clase 2 y el lineal en x, casos 13 y 14 (mediana y rango intercuartil entre semillas) | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` (casos 13 y 14) y `tools/ml_cifras_c5.py` | Propio, CC BY-SA 4.0 |
| `ml-c5-momento-decision.svg` | Diagrama: la línea del tiempo de un pedido y el momento en que se conoce cada columna | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de los materiales del curso (F9) con datos de entregas | Propio, CC BY-SA 4.0 |
| `ml-c5-fugas.svg` | MCC de la CV contra MCC en el despliegue en «llegó tarde», por ruta de fuga, con el benchmark de la moda | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` (casos 19, 20, 21 y 26) y `tools/ml_cifras_c5.py`; idea de los notebooks del profesor, sin sus datos | Propio, CC BY-SA 4.0 |
| `ml-c5-tuberia.svg` | Diagrama: ajustar todo antes de separar contra ajustar dentro de cada pliegue, con flechas de ajustar y aplicar | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de los materiales del curso (F10) y de Goodfellow et al., *Deep Learning*, §11.5 | Propio, CC BY-SA 4.0 |
| `ml-c5-imputacion.svg` | Imputar con la mediana: el pico, el error con y sin la indicadora y la pendiente con el centinela −5 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` y `tools/ml_cifras_c5.py`; idea de los notebooks del profesor, sin sus datos | Propio, CC BY-SA 4.0 |
| `ml-c5-receta.svg` | Diagrama: la receta de trabajo en pasos, con el lazo en validación, la prueba cerrada y las reservas cal, val_a y val_b | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de Goodfellow et al., *Deep Learning*, cap. 11, y de las diapositivas 07-94 y 07-96 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c5-trampa-dummy.svg` | La matriz de seis pedidos con intercepto y tres dummies; dos β̂ con las mismas predicciones y el de ridge | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos de `tools/ml_cifras_c5.py` | Propio, CC BY-SA 4.0 |
| `ml-c5-diagnostico.svg` | Curvas de aprendizaje: la brecha con CV al azar contra por grupos, y dos procesos altos y juntos, uno lejos del piso y otro sobre él | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` y `tools/ml_cifras_c5.py`; idea de Goodfellow et al., *Deep Learning*, §11.3–11.5 | Propio, CC BY-SA 4.0 |
| `ml-c5-arbol-escalones.svg` | La frontera x2 > x1 con árboles de profundidad 1, 3 y 6 y su MCC en validación | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 5.7 | Propio, CC BY-SA 4.0 |
| `ml-c5-familias-capacidad.svg` | Bosque y boosting: el mecanismo (promediar árboles, sumar correcciones) y su perilla con la misma partición de CV | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` y `tools/ml_cifras_c5.py`; idea de Goodfellow et al., *Deep Learning*, §7.11 y §7.8, y de Hastie et al., *ESL*, ec. 15.1 | Propio, CC BY-SA 4.0 |
| `ml-c5-phi-aprendida.svg` | Diagrama: la φ escrita a mano en las clases 1 a 4 contra la φ de unidades sigmoides que se aprende | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); diagrama propio; idea de Goodfellow et al., *Deep Learning*, figs. 1.2 y 1.5 | Propio, CC BY-SA 4.0 |
| `ml-c5-cybenko.svg` | Aproximación con 1, 3 y 10 sigmoides sin ruido, y curvas de aprendizaje de la φ polar contra la aprendida en los anillos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c5.py`); datos sintéticos de `ml_lab` y `tools/ml_cifras_c5.py`; idea de la diapositiva 03-55 del profesor y de Cybenko (1989) | Propio, CC BY-SA 4.0 |
