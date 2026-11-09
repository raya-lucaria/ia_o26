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
| `ml-c1-taylor-vs-mco.svg` | La recíproca 2 + 5/x con Taylor de grados 3 y 9 en x₀ = 1 y el polinomio de grado 3 ajustado a 20 datos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-weierstrass.svg` | |x − 0.5| en [0, 1] y sus ajustes por mínimos cuadrados de grados 2, 6 y 14, con su error máximo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`) | Propio, CC BY-SA 4.0 |
| `ml-c1-tres-ajustes.svg` | Ajustes de grados 1, 4 y 15 a 20 datos de la recíproca, con observaciones nuevas: subajuste, capacidad adecuada y sobreajuste | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 5.2 | Propio, CC BY-SA 4.0 |
| `ml-c1-capacidad-brecha.svg` | Curva de capacidad medida (L_ent, R, brecha, piso y benchmark) con 20 y con 200 datos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 5.3 | Propio, CC BY-SA 4.0 |
| `ml-c1-elegir-con-entrenamiento.svg` | En 200 muestras, el grado que elige el error de entrenamiento contra el de menor riesgo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-inverso-vs-potencias.svg` | La recíproca cerca de cero: el polinomio de grado 10 contra φ = (1, 1/x) y sus riesgos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-extrapolar.svg` | Interpolar contra extrapolar en las entregas, el seno y un proceso que recuerda su paso anterior | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c1-no-free-lunch.svg` | Aciertos fuera de la muestra de tres reglas sobre las 256 funciones de 3 bits, por rugosidad | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c1.py`); cálculo exacto con `ml_lab` | Propio, CC BY-SA 4.0 |

### Clase 1 · tramo tarea

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

## Clase 2

### Clase 2 · tramo rápido

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c2-dos-niveles.svg` | Diagrama: dos optimizaciones anidadas; afuera se elige el grado N con validación, adentro β con N fijo y entrenamiento | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`) | Propio, CC BY-SA 4.0 |
| `ml-c2-tres-conjuntos.svg` | Diagrama: la muestra en entrenamiento, validación y prueba (60/20/20) con el rol de cada uno, el candado de la prueba y el modelo final reajustado con entrenamiento y validación | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); idea de las diapositivas 20, 57 y 58 del deck 04 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-simulacro.svg` | Diagrama: cuatro contratos de uso (más de lo mismo, el mes que viene, pacientes nuevos, otra ciudad) con su prueba marcada y la separación que imita cada uno | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); idea de las diapositivas 19, 25 y 26 del deck 04 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-pliegues.svg` | Diagrama: rejilla de cinco vueltas por cinco pliegues; en la vuelta m valida el pliegue m, y la prueba queda cerrada aparte | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); idea de las diapositivas 4 a 10 del deck 05 del profesor y de Goodfellow et al., *Deep Learning*, alg. 5.1 | Propio, CC BY-SA 4.0 |
| `ml-c2-costo-cv.svg` | Diagrama: tres validaciones cruzadas apiladas, una por candidato, y el contador M·k + 1 de ajustes con el reajuste final | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); idea de las diapositivas 11 a 15 del deck 05 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-anidada.svg` | Diagrama: la validación cruzada anidada; afuera cada pliegue externo mide, adentro una validación cruzada interna elige el grado | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`) | Propio, CC BY-SA 4.0 |
| `ml-c2-ajustes-con-prueba.svg` | Grados 1, 4 y 12 sobre las mismas 60 entregas, con círculos de entrenamiento, cuadrados de prueba, la f verdadera y el ajuste; arriba de cada panel, L_ent y L_prueba | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de la diapositiva 23 del deck 04 del profesor y de Goodfellow et al., *Deep Learning*, fig. 5.2 | Propio, CC BY-SA 4.0 |
| `ml-c2-prueba-ruidosa.svg` | Histogramas de L_prueba del mismo modelo congelado con 500 pruebas de 20 y de 200 entregas, contra R, con la cobertura de ±2 EE | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); Goodfellow et al., *Deep Learning*, §5.4.3 | Propio, CC BY-SA 4.0 |
| `ml-c2-optimismo.svg` | Lo anunciado menos el riesgo real del grado elegido, sin reajuste, eligiendo con la prueba y con validación | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de la diapositiva 55 del deck 04 y del ejercicio 04_tvt del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-prueba-miente.svg` | Por contrato de uso, L_prueba con separación al azar y con la que imita el contrato, contra R del despliegue y el benchmark | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`) (casos 13 a 15) | Propio, CC BY-SA 4.0 |
| `ml-c2-reparto.svg` | R medio del modelo y dispersión de L_prueba − R contra la fracción de la muestra que va a prueba | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de las diapositivas 27 y 28 del deck 04 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-cv-capacidad.svg` | CV con barras de ±1 EE contra el grado, con L_ent, R del simulador, piso, benchmark, el umbral de un EE y los elegidos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de Goodfellow et al., *Deep Learning*, fig. 5.3, y de la diapositiva 18 del deck 05 del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-pliegue-anomalo.svg` | La pérdida de cada uno de los cinco pliegues para los grados 1, 4 y 8 en el caso 16, con su media | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea del notebook ejercicios/06_cv_bias_variance del profesor | Propio, CC BY-SA 4.0 |
| `ml-c2-estratificada.svg` | Sesenta casos con 6 positivos en cinco pliegues, al azar y estratificados, con la fracción de 1000 particiones que deja algún pliegue sin positivos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de las diapositivas 29 y 98 del deck 07 del profesor | Propio, CC BY-SA 4.0 |

### Clase 2 · tramo m

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c2-abanico.svg` | Cien ajustes de grado 1, 4 y 12, uno por muestra del mismo proceso, con su promedio y la media verdadera de y dado x | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea del notebook _deprecated_bias_variance del profesor y de Goodfellow et al., *Deep Learning*, §5.4 | Propio, CC BY-SA 4.0 |
| `ml-c2-diana.svg` | Las predicciones en x = 5 de cien ajustes de grado 1 y 12, su promedio y el valor verdadero, con eje fijo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de la diapositiva 8 del deck 06 del profesor (Domingos 2012) | Propio, CC BY-SA 4.0 |

### Clase 2 · tramo completo

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c2-sesgo-varianza.svg` | Ruido, sesgo² y varianza por grado calculados con f conocida, y la CV 5 de una sola muestra junto al total calculado | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de Goodfellow et al., figura 5.6 | Propio, CC BY-SA 4.0 |
| `ml-c2-curva-aprendizaje.svg` | Medianas de L_ent y R de los grados 1 y 10 contra el número de entregas, con el piso, y el grado que elige la CV | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); datos sintéticos de `ml_lab` (`tools/ml_cifras_c2.py`); idea de Goodfellow et al., figura 5.4 | Propio, CC BY-SA 4.0 |
| `ml-c2-diagnostico.svg` | Árbol de diagnóstico: brecha, benchmark, capacidad y separación, con sus cinco hojas | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c2.py`); idea de Goodfellow et al., §11.3, y de las diapositivas 30–33 del deck 04 y 96 del deck 07 del profesor | Propio, CC BY-SA 4.0 |

## Clase 3

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
| `ml-c3-mismo-rmse.svg` | Dos modelos con el mismo RMSE de validación en sus tres vistas: la recta correcta con ruido grande y una recta ajustada a una curva | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de los notebooks del profesor (tres paneles) | Propio, CC BY-SA 4.0 |
| `ml-c3-benchmarks.svg` | Errores de validación del modelo, la media, la mediana y el piso, en barras: el caso 11 y una señal débil | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, §11.1 | Propio, CC BY-SA 4.0 |
| `ml-c3-media-acumulada.svg` | Promedio acumulado de e² en 20 semillas con ruido normal, Pareto 1.5 y Cauchy | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-fuentes-patologias.svg` | Diagrama: las cuatro fuentes del error de la clase 1 con su patología, y aparte la optimización y la endogeneidad | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); diagrama propio | Propio, CC BY-SA 4.0 |
| `ml-c3-diana-beta.svg` | Cuatro nubes de 200 estimaciones de (β̂1, β̂2): correcta, omitida correlacionada, colineal y endógena | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de la diana de Domingos, como en `ml-c2-diana` | Propio, CC BY-SA 4.0 |
| `ml-c3-interaccion-plano.svg` | Residuales de validación en el plano (x1, x2) sin y con la columna x1·x2 | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-colineal-prediccion.svg` | β̂1 con correlación 0 y 0.99, y la predicción dentro y fuera de la diagonal de los datos | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-un-coeficiente.svg` | La pérdida de un coeficiente más el castigo de ridge y de lasso para tres μ, con su mínimo | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); idea de Goodfellow et al., *Deep Learning*, fig. 5.1 | Propio, CC BY-SA 4.0 |
| `ml-c3-elipse-region.svg` | Curvas de nivel de la pérdida de entrenamiento y las regiones de ridge, lasso y red elástica | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 7.1, y Hastie et al., *ESL*, fig. 3.11 | Propio, CC BY-SA 4.0 |
| `ml-c3-encoger-1d.svg` | El coeficiente penalizado contra el sin penalizar con μ = 1: ridge, lasso y red elástica | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); idea de Goodfellow et al., *Deep Learning*, ec. 7.23 | Propio, CC BY-SA 4.0 |
| `ml-c3-grado-12-mu.svg` | Las entregas curvas de la clase 2 con el polinomio de grado 12 y ridge con tres μ, y la U contra μ | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de Goodfellow et al., *Deep Learning*, fig. 5.5 | Propio, CC BY-SA 4.0 |
| `ml-c3-trayectorias.svg` | Trayectorias de los coeficientes de ridge, lasso y red elástica con 50 variables, 5 útiles | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-ridge-colineal.svg` | La nube de (β̂1, β̂2) con correlación 0.99, sin penalizar y con ridge | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-estandarizar.svg` | Trayectorias de lasso del caso 10 sin y con estandarizar | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |
| `ml-c3-mu-cv.svg` | L_ent, CV5 con su EE, R y el benchmark contra μ con lasso y 50 variables, con el umbral de un EE | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab`; idea de la figura de glmnet de las presentaciones del profesor | Propio, CC BY-SA 4.0 |
| `ml-c3-recta-de-apoyo.svg` | El mejor L_ent contra el presupuesto d con lasso y su recta de apoyo de pendiente −μ | Generado con `tools/gen_aprendizaje_maquina.py` (`tools/figuras_ml_c3.py`); datos sintéticos de `ml_lab` | Propio, CC BY-SA 4.0 |

## Clase 4

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|

## Clase 5

| Archivo | Qué muestra | Origen | Licencia |
|---|---|---|---|
