---
id: ml-laboratorio
title: "El laboratorio ml_lab, en una hoja"
nav_title: Laboratorio
summary: "Qué es ml_lab, cómo lo carga cada notebook en Colab y qué hace cada una de sus funciones públicas, agrupadas por propósito, con los notebooks que la usan."
status: ready
estimated_time: 15m
tags: [aprendizaje-maquina, referencia, laboratorio]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 01 · ¿Qué es f?** Es el primero que carga `ml_lab`. Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)
>
> **[👉 Abrir `01_que_es_f.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/01_que_es_f.ipynb)**

# El laboratorio ml_lab, en una hoja

Todos los notebooks de la unidad usan la misma biblioteca: `ml_lab`. Esta
hoja dice qué hace cada función. No hace falta leerla de corrido: búscala
cuando una celda llame algo que no recuerdas.

## Qué es

`ml_lab` es un solo archivo de Python, `ml_lab.py`, con nombres en español.
Genera datos de procesos que tú conoces, ajusta modelos, mide errores y
dibuja. Por dentro usa numpy, pandas, matplotlib, seaborn, scipy y
scikit-learn; Colab ya los trae todos.

Su ventaja es que conoce la población. Cada proceso trae, además de tu
muestra, una muestra enorme de la misma población. Con ella se calcula el
riesgo $R$ que en la práctica nunca ves. Así puedes comparar lo que anuncia
cada método con lo que de verdad pasa.

El archivo se lee de arriba abajo, en el orden de esta hoja. Cada función
trae una explicación corta y un ejemplo de una línea:
`help(ml.proceso)` lo muestra en el notebook.

## Cómo lo carga un notebook

La primera celda de cada notebook se llama **«▶ Corre esta celda primero»**.
Hace cuatro cosas:

1. Busca `ml_lab.py` en la carpeta del notebook y lo usa si su versión
   sirve.
2. Si no, lo baja del repositorio del curso.
3. Si no hay red, usa una copia comprimida que viaja dentro del propio
   notebook.
4. Llama a `ml.requiere(...)` con la versión con que se escribió el
   notebook, fija el tema claro de las gráficas e importa todo.

Después de esa celda tienes `ml` y también cada función suelta:
`ml.proceso(...)` y `proceso(...)` son lo mismo.

Una versión sirve si comparte el primer número y el segundo es igual o
mayor: un notebook escrito con 1.2 corre con 1.6, no con 2.0. Si la
celda dice que la versión no alcanza, reinicia el entorno de ejecución y
córrela otra vez.

Los controles usan ipywidgets. Sin ipywidgets, o con la variable de
entorno `ML_LAB_PRUEBA=1`, cada laboratorio corre una vez con los valores
iniciales.

## Los notebooks, por clave

En las tablas, la columna «Notebooks» usa estas claves. Un guion (—)
quiere decir que ningún notebook la llama directo: la usan otras
funciones del laboratorio, o queda para que la pruebes tú.

- **01**, **02**: clase 1, [[ml-que-es-f|¿Qué es f?]] y [[ml-polinomios-y-capacidad|Polinomios, capacidad y supuestos]].
- **03**, **04**, **05**: clase 2, [[ml-entrenamiento-y-prueba|Entrenamiento y prueba]], [[ml-validacion-cruzada|Validación cruzada]] y [[ml-sesgo-y-varianza|Sesgo y varianza]].
- **T2**: [[ml-tarea-2|Tarea 2 · Separar, elegir y reportar]].
- **06**, **07**: clase 3, [[ml-leer-el-error|Leer el error]] y [[ml-lagrangeano-en-accion|El lagrangeano en acción]].
- **T3**: [[ml-tarea-3|Tarea 3 · Cincuenta variables]].
- **08**, **09**: clase 4, [[ml-perdida-metrica-desbalanceo|Pérdida, métrica y desbalanceo]] y [[ml-calibracion-y-conformal|Calibración y predicción conformal]].
- **T4**: [[ml-tarea-4|Tarea de la clase 4]].
- **10**: clase 5, [[ml-son-iid-y-fugas|¿Son iid? Fugas]].
- **T5a**, **T5b**, **T5c**: [[ml-tareas-5|Tarea de la clase 5]], series de tiempo, fugas y otras familias.

## Versión y tema

| Función | Qué hace | Notebooks |
|---|---|---|
| `VERSION` | La versión del archivo cargado, como `"1.6"`. | todos |
| `requiere(version)` | Detiene el notebook si el `ml_lab` cargado no es compatible con esa versión. | todos |
| `CAMBIOS` | Qué trajo cada versión, en un diccionario. | — |
| `tema(nombre)` | Fija el estilo de las gráficas: `"claro"` en los notebooks, `"sitio"` con el fondo del curso. | todos |
| `NoAplica` | El error que sale cuando una medida no existe para una familia; por ejemplo, la matriz $\Phi$ de un árbol. | — |

## Piezas aleatorias

Una pieza es una distribución. Sirve como variable $x$ o como ruido
$\varepsilon$ dentro de `proceso`.

| Función | Qué hace | Notebooks |
|---|---|---|
| `normal(media, desv)` | Normal con esa media y desviación estándar. | 01 02 05 06 07 T2 T3 T5b |
| `uniforme(a, b)` | Uniforme entre `a` y `b`. | 01 02 03 05 06 10 T2 T4 T5b T5c |
| `categorica(...)` | Elige una categoría; por omisión, todas igual de probables. | 10 T4 T5a T5b T5c |
| `lognormal(media, desv)` | $e^{Z}$ con $Z$ normal: positiva y sesgada a la derecha. | 06 T4 |
| `t_student(...)` | Centrada en 0, con colas más pesadas que la normal. | 06 |
| `cauchy(...)` | Centrada en 0, sin media ni varianza: el MSE no se asienta. | 06 |
| `pareto(...)` | Cola larga a la derecha. | 06 |
| `heterocedastico(...)` | Ruido cuya desviación depende de $x$. | — |
| `ar1(a, ...)` | Ruido con memoria: crea la columna `t` y hace $\varepsilon_t=a\,\varepsilon_{t-1}+\text{ruido}$. | 10 T5a |
| `efecto_grupo(...)` | Crea la columna `grupo`; el ruido es el efecto del grupo más uno individual. | 10 T5b T5c |
| `Pieza`, `Mecanismo` | Los tipos de las piezas: independiente, o con contexto como `t` y `grupo`. | — |

## Procesos y casos borde

Un proceso devuelve un `Datos`: la muestra ya partida en `ent`, `val` y
`prueba`, más `realidad` y `despliegue`, las dos muestras enormes. Cambiar
la semilla cambia la muestra; la población y $f$ se quedan.

| Función | Qué hace | Notebooks |
|---|---|---|
| `proceso(n, x, f, ruido, ...)` | Datos de regresión $y=f(x)+\varepsilon$ de un proceso que tú escribes. `separar` dice cómo se parte; `despliegue`, de dónde sale el uso. | 01 02 05 06 07 10 T2 T3 T5a T5c |
| `proceso_clasificacion(...)` | Datos de clasificación con $\Pr(y\mid x)$ conocida: binaria o con $K$ clases. | 10 T4 T5b |
| `anillos(...)` | Dos anillos concéntricos para clasificar; $y=1$ es el exterior. | 01 08 |
| `muchas_variables(J, utiles, ...)` | $J$ variables normales; solo las primeras `utiles` entran en $f$. | 07 |
| `entregas_curvas(...)` | Las entregas de la clase 1 con una $f$ curva y una zona de tráfico. Los notebooks la llaman por `PROCESOS`. | — |
| `PROCESOS` | Los procesos con nombre: `"entregas"`, `"entregas_curvas"`, `"lluvia"`, `"seno"`, `"fraude"`, `"mensajes3"` y otros. | 01 02 03 04 05 07 08 09 10 |
| `caso(numero_o_nombre, ...)` | Construye un caso borde; lo que agregas cambia su proceso. | 01 02 03 04 06 08 10 |
| `CASOS_BORDE`, `CasoBorde` | Los 28 casos borde: cómo se construye cada uno, qué preguntar y qué se ve. | — |
| `Datos` | Lo que devuelve un proceso. `datos.rehacer(semilla)` da otra muestra de la misma población. | 10 T4 |

## Separar los datos

| Función | Qué hace | Notebooks |
|---|---|---|
| `separar(df, como, ...)` | Parte una tabla en entrenamiento, validación y prueba: al azar, estratificado, por tiempo o por grupo. Los notebooks lo piden con el argumento `separar=` de `proceso` y `caso`. | — |
| `partir(df, fraccion, ...)` | Parte un solo conjunto en dos piezas; por ejemplo, ajuste y calibración. | 09 T4 |
| `pliegues(df, k, ...)` | Los $k$ pliegues de la validación cruzada; cada fila valida una sola vez. | 04 T5a T5b T5c |
| `Particion` | El tipo del argumento `como`: un nombre o una función propia. | — |

## Representaciones φ

Una $\phi$ dice qué ve el modelo de cada entrada. Todas se ajustan con
entrenamiento y se aplican igual a los demás conjuntos.

| Función | Qué hace | Notebooks |
|---|---|---|
| `polinomio(N, variable)` | Las potencias $x, x^2, \dots, x^N$ de una variable. | 01 02 03 04 05 07 10 T2 T5c |
| `columnas(...)` | Columnas por nombre o expresiones simples, como `"1/x2"` o `"x1*x3"`. | 01 02 06 07 08 09 10 T3 T4 T5a T5b T5c |
| `polares(...)` | Radio $r$ y ángulo $\theta$ de $(x_1,x_2)$. | 01 08 |
| `periodicas(variable, periodo, armonicos)` | Senos y cosenos de la variable con ese periodo. | — |
| `dummies(variable, ...)` | Indicadoras de una variable categórica, con las categorías de entrenamiento. | 01 03 10 T5a |
| `interacciones(...)` | Columnas producto, como `"x1*x2"`. | 06 |
| `combinar(...)` | Junta varias $\phi$ en una sola $\Phi$, con la columna de unos si hay intercepto. | 01 02 03 06 10 T5a T5c |
| `taylor(N, centro, ...)` | El polinomio de Taylor de grado $N$ de una $f$ del laboratorio. | 02 |
| `estandarizar(phi)` | Centra y escala cada columna con la media y la desviación de entrenamiento. | 07 08 09 10 T3 T4 T5b |
| `seleccionar(phi, k)` | Se queda con las $k$ columnas más correlacionadas con $y$, medido solo en entrenamiento. | 10 T5b |
| `Phi` | El tipo común de todas las anteriores. | — |

## Ajustar

| Función | Qué hace | Notebooks |
|---|---|---|
| `ajustar(datos, phi, mu, penalizacion, ...)` | Ajusta un modelo lineal en parámetros con entrenamiento: regresión o logística. Con `mu` y `penalizacion` es ridge, lasso o red elástica; acepta `pesos`. | todos |
| `ajustar_otro(datos, familia, ...)` | Un modelo que no es lineal en parámetros: vecinos más cercanos, árbol, bosque o boosting. | 02 03 10 T5a T5c |
| `Modelo` | Lo que devuelve `ajustar`: `.predecir`, `.predecir_prob`, `.L`, `.Phi` y `.n_parametros`. | 01 10 |

## Pérdidas y métricas

| Función | Qué hace | Notebooks |
|---|---|---|
| `perdida(modelo, df, ...)` | La pérdida $\ell_i$ de cada observación: un arreglo, no un promedio. | 03 04 05 T2 |
| `L(modelo, df)` | La pérdida promedio $L$ del modelo en esa tabla, sin pesos. | 01 02 03 04 06 07 T3 |
| `evaluar(modelo, df, criterio)` | La pérdida promedio o una métrica en esa tabla, sin pesos. | 01 T5a T5b |
| `riesgo(modelo, datos)` | $R$: la pérdida en la muestra enorme del despliegue. Solo pérdidas. | 01 02 03 04 06 07 10 T3 |
| `desempeno(modelo, datos, criterio)` | Cualquier pérdida o métrica en la muestra enorme. | 01 |
| `piso(datos, perdida)` | $R_{\text{Bayes}}$: el menor riesgo posible con las variables visibles. | 01 02 04 05 06 |
| `benchmarks(datos, df_eval)` | Los puntos de comparación sin $x$, ajustados con entrenamiento: media y mediana, o moda y proporción. | 01 02 03 05 06 07 08 09 T3 T4 |
| `mse`, `mae`, `rmse` | Error cuadrático medio, absoluto medio y la raíz del primero, a partir de $y$ y $\widehat y$. | — |
| `r2(y, y_gorro)` | $R^2$, que compara contra predecir la media del mismo $y$. No es el riesgo al cuadrado. | — |
| `peores_errores(modelo, df, k)` | Las $k$ filas con mayor $\lvert e\rvert$. | 06 |
| `aciertos(y, y_gorro)` | Fracción de etiquetas acertadas, $A$. | 08 |
| `aciertos_balanceados(...)` | $A_{\text{bal}}$: los aciertos dentro de cada clase, promediados. | 08 |
| `mcc(...)` | El MCC: la correlación entre lo real y lo predicho, sobre las $K$ clases. | 08 T4 T5b |
| `brier(y, p)` | El promedio de $(y-p)^2$ en clasificación binaria. | 09 |
| `log_loss(y, prob)` | La pérdida logarítmica media, con $\ln$. | 09 |
| `matriz_confusion(...)` | Cuántos casos de cada clase real fueron a cada clase predicha. | — |
| `por_clase(...)`, `promediar(...)` | Una métrica dentro de cada clase, y su promedio macro o ponderado. | 08 T4 |
| `con_clases(metrica, clases)` | Fija las clases de una métrica para usarla dentro de la validación cruzada. | 08 |
| `clasificar(prob, tau)` | Etiquetas a partir de probabilidades, con el umbral $\tau$. | — |
| `pesos_de_clase(y, ...)` | Los pesos $w_y$ de cada clase; `"balanceado"` hace que cada clase pese lo mismo. | — |
| `Criterio`, `SENTIDO` | Los nombres de pérdidas y métricas, y si cada una se minimiza o se maximiza. | — |

## Medir y elegir

| Función | Qué hace | Notebooks |
|---|---|---|
| `error_estandar(perdidas)` | $\mathrm{EE}=s_\ell/\sqrt n$ de una pérdida promedio. | 03 04 T2 T3 T4 |
| `intervalo(valor, ee)` | El intervalo valor $\pm$ dos EE, como (bajo, alto). | — |
| `diferencia_pareada(a, b)` | La diferencia media entre dos modelos fila por fila, con su EE. | 05 06 07 T2 T3 |
| `diferencia_por_pliegue(...)` | Esa diferencia en cada pliegue y su media. | 05 |
| `validacion_cruzada(df, construir, k)` | $\mathrm{CV}_k$: ajusta sin el pliegue $m$ y mide en él, para $m=1,\dots,k$. | 04 05 08 10 T2 T5a T5b T5c |
| `elegir(datos, candidatos, con, regla)` | Elige un candidato con entrenamiento, validación, prueba o CV. Con empate, el más simple; `regla="un_ee"` aplica la regla de un EE. | 03 04 05 07 08 09 T2 T3 T4 T5a |
| `cv_anidada(...)` | Elige con una CV interna y mide al elegido con una externa. | 04 |
| `repetir(experimento, repeticiones)` | Corre un experimento con muchas semillas y apila los resultados. | 02 04 |
| `optimismo_por_seleccion(...)` | Cuánto promete de más elegir con la prueba, repetido muchas veces. | 03 T2 |
| `capacidad_elegida(...)` | Qué hiperparámetro elige la CV para cada tamaño de muestra. | 05 |
| `reparto(...)` | Cuánto pierde el modelo y cuánto gana la medición según lo que va a prueba. | 03 |
| `incertidumbre(modelo, df, criterio)` | Bootstrap de una cifra: su EE y su intervalo; `grupo=` remuestrea grupos completos. | T4 T5b |
| `error_por_zona(...)` | El riesgo si el uso cayera en cada zona de $x$; sirve para ver qué pasa al extrapolar. | 02 |
| `no_free_lunch(bits)` | Cuánto acierta cada regla fuera de la muestra, promediado sobre todas las funciones booleanas. | 02 |
| `ResultadoCV`, `Seleccion`, `Incertidumbre` | Lo que devuelven `validacion_cruzada`, `elegir` e `incertidumbre`. | — |

## Capacidad, sesgo y varianza

| Función | Qué hace | Notebooks |
|---|---|---|
| `curva_capacidad(datos, candidatos)` | $L$ de cada candidato en cada conjunto, con su EE. | 02 03 05 07 |
| `sesgo_varianza(fabrica, candidatos)` | Parte el error esperado en ruido, sesgo al cuadrado y varianza. | 05 |
| `curva_aprendizaje(...)` | $L_{\text{ent}}$ y $R$ de cada candidato contra $n$. | 05 |
| `SesgoVarianza` | Lo que devuelve `sesgo_varianza`. | — |

## Regularización

| Función | Qué hace | Notebooks |
|---|---|---|
| `trayectorias(datos, phi, mus, ...)` | Cada pendiente $\widehat\beta_j$ contra $\mu$. | 07 T3 |
| `optimo_restringido(...)` | El mejor $L_{\text{ent}}$ con $\Omega(\beta)\le d$ y su $\mu$ equivalente, para dos pendientes. | 07 |
| `encoger_1d(b, mu, penalizacion)` | La pendiente penalizada de un solo coeficiente, dada la de mínimos cuadrados $b$. | 07 |
| `beta_repetido(fabrica, ...)` | $\widehat\beta$ en muchas muestras nuevas: una fila por muestra. | 06 07 T3 |
| `beta_verdadero(datos, phi)` | Los coeficientes estructurales, para compararlos con los ajustados. | T3 |

## Clasificación: umbral, pesos, calibración y conformal

| Función | Qué hace | Notebooks |
|---|---|---|
| `elegir_umbral(modelo, df, metrica)` | El umbral $\tau$ que optimiza una métrica en validación, nunca en prueba. | 08 |
| `ajustes_por_mu(...)`, `AjustesPorMu` | Ajusta una vez por cada $\mu$ y guarda los modelos para dibujar y medir. | 08 |
| `contribucion_por_clase(...)` | Cuánto aporta cada clase a la pérdida logarítmica. | 08 |
| `efecto_de_pesos(...)` | Ajusta con varias razones $w_1/w_0$ y mide intercepto, probabilidad y métricas. | 08 |
| `metricas_vs_proporcion(...)` | Cómo cambian las métricas cuando la clase positiva se vuelve rara. | 08 |
| `perfil_en_beta(...)` | Pérdida y métricas al mover la pendiente $\beta_1$, con el intercepto reoptimizado. | — |
| `calibracion(modelo, df)` | La tabla de la curva de confiabilidad: probabilidad anunciada contra frecuencia observada. | 09 T4 |
| `recalibrar(modelo, df_cal)` | Recalibra las probabilidades con datos que el ajuste no tocó. | 09 T4 |
| `conformal(modelo, df_cal, delta)` | El corte $\widehat c$ de la predicción conformal y los conjuntos $C(x)$, con cobertura $1-\delta$. | 09 T4 T5b |
| `Conformal` | Lo que devuelve `conformal`. | — |

## Supuestos y fugas

| Función | Qué hace | Notebooks |
|---|---|---|
| `imputador(...)`, `Imputador` | Un paso sin ajustar que llena faltantes con la mediana o la moda de entrenamiento y agrega la indicadora `<col>_falta`. | 10 T5b |
| `imputar_simple(df_ent, ...)` | La misma imputación, ya aprendida en `df_ent`. | T5b |
| `tuberia(*pasos, modelo)` | Un `construir` que ajusta todo, imputación y $\phi$ incluidas, con el entrenamiento de cada pliegue. | 10 T5b |
| `sembrar_fuga(datos, tipo)` | Otro `Datos` con una fuga sembrada a propósito. | 10 |
| `medir_fugas(...)` | Cuánto promete de más la CV con cada fuga. | 10 |
| `importancia(modelo, df)` | Cuánto empeora el criterio al revolver cada columna. | 10 T5b |
| `validacion_adversarial(df_a, df_b)`, `ResultadoAdversarial` | ¿Se distinguen dos tablas mirando solo $x$? Hace CV de un clasificador de origen. | 10 T5b |
| `ks_por_variable(df_a, df_b)` | El estadístico de Kolmogorov–Smirnov de cada variable, una por una. | 10 |
| `autocorrelacion(residuales, rezagos)` | La autocorrelación de los residuales en cada rezago. | T5a |
| `sellar(df)`, `Sellada` | Sella la prueba: no se lee hasta `.abrir()`, que cuenta cuántas veces la abriste. | T5b |

## Gráficas

Todas dibujan con la leyenda única de la unidad (ver
[[notacion-aprendizaje-maquina|la hoja de notación]]). `ROLES` guarda esa
leyenda: marca, trazo y color de cada rol.

| Función | Qué dibuja | Notebooks |
|---|---|---|
| `imprimir_Phi(modelo, df)` | Imprime las primeras filas de $\Phi$, con la columna de unos primero. | 01 02 03 06 07 08 10 T3 |
| `dibujar_proceso(datos)` | La muestra contra la primera $x$ y, si se puede, la $f$ verdadera. | 01 07 T2 |
| `dibujar_ajuste(...)` | Una o varias curvas ajustadas; con ventana, la extrapolación sombreada. | 01 02 03 07 |
| `dibujar_frontera(modelo, datos)` | La frontera de decisión de un clasificador binario sobre $(x_1,x_2)$. | 01 08 |
| `dibujar_piso(...)` | El riesgo de varios modelos contra la línea del piso. | 01 |
| `dibujar_curva_capacidad(...)` | $L_{\text{ent}}$ y $R$ por candidato. | 02 03 05 |
| `dibujar_elecciones(...)` | Cuántas veces se eligió cada valor, en dos histogramas. | 02 |
| `dibujar_no_free_lunch(...)` | Aciertos fuera de la muestra de cada regla. | 02 |
| `dibujar_pliegues(...)` | Qué filas ajustan y cuáles validan en cada vuelta. | 04 T5a |
| `dibujar_histograma_estimaciones(...)` | Estimaciones repetidas contra el valor verdadero. | 03 04 10 T2 |
| `dibujar_cv(...)` | La curva con que se eligió, el umbral de un EE y el elegido. | 04 05 07 T2 T3 |
| `dibujar_cajas_pliegues(...)` | La pérdida de cada pliegue y candidato, con su media. | 04 T2 |
| `dibujar_contratos(...)` | Lo que promete la prueba contra el riesgo del despliegue, por contrato. | 03 10 |
| `dibujar_reparto(...)` | El resultado de `reparto`, contra la fracción de prueba. | 03 |
| `dibujar_abanico(...)` | Las $\widehat f$ de cada repetición, su promedio y $E[y\mid x]$. | 05 |
| `dibujar_sesgo_varianza(...)` | Ruido, sesgo al cuadrado y varianza apilados por candidato. | 05 |
| `dibujar_curva_aprendizaje(...)` | El error contra $n$, en escala logarítmica. | 05 |
| `dibujar_diana(...)` | Las predicciones repetidas en un punto, su promedio y el valor verdadero. | 05 |
| `dibujar_tres_paneles(modelo, df)` | $\widehat y$ contra $y$, el histograma de residuales y el residual contra $x$. | 06 07 T3 |
| `dibujar_benchmarks(...)` | El error del modelo, de los benchmarks y del piso, en barras. | 06 T3 |
| `dibujar_media_acumulada(...)` | El promedio acumulado de $e^2$ o $\lvert e\rvert$ contra $n$. | 06 |
| `dibujar_peso_de_filas(...)` | Qué fracción del MSE y del MAE se llevan las peores filas. | 06 |
| `dibujar_residuales_plano(...)` | El signo y el tamaño de cada residual sobre el plano $(x_1,x_2)$. | 06 |
| `dibujar_beta_repetido(...)` | La distribución de $\widehat\beta$ de `beta_repetido`. | 06 |
| `dibujar_encoger_1d(...)` | Cómo encogen ridge, lasso y la red elástica un solo coeficiente. | 07 |
| `dibujar_trayectorias(...)` | Cada pendiente contra $\log_{10}\mu$. | 07 T3 |
| `dibujar_regiones(...)` | Las curvas de nivel de $L_{\text{ent}}$ y la región $\Omega(\beta)\le d$. | 07 |
| `dibujar_presupuesto(...)` | El mejor $L_{\text{ent}}$ contra $d$ y su recta de apoyo de pendiente $-\mu$. | 07 |
| `dibujar_umbral(...)` | Histogramas por clase y métricas al mover $\tau$. | 08 |
| `dibujar_separable(...)` | Qué hace $\mu$ cuando las clases se separan sin error. | 08 |
| `dibujar_metrica_por_pliegue(...)` | MCC y $A_{\text{bal}}$ de cada pliegue. | 08 |
| `dibujar_contribucion_por_clase(...)` | El resultado de `contribucion_por_clase`, en barras apiladas. | 08 |
| `dibujar_efecto_de_pesos(...)` | El resultado de `efecto_de_pesos`. | 08 |
| `dibujar_promedios(...)` | La métrica de cada clase, con grosor según su número de casos. | 08 T4 |
| `dibujar_metricas_vs_proporcion(...)` | Las métricas contra la proporción de positivos. | 08 |
| `dibujar_calibracion(...)` | La curva de confiabilidad. | 09 T4 |
| `dibujar_cobertura_por_clase(...)` | La cobertura de cada clase contra la meta $1-\delta$. | 09 |
| `dibujar_conformal(...)` | Los conjuntos $C(x)$ o los intervalos de regresión. | 09 |
| `dibujar_adversarial(...)` | El resultado de la validación adversarial. | 10 |
| `dibujar_ks(...)` | El estadístico KS de cada variable, de mayor a menor. | 10 |
| `dibujar_residual_tiempo(...)` | Los residuales en el orden del tiempo y su autocorrelación. | 10 T5a |
| `dibujar_fugas(...)` | Cuánto infla cada fuga lo que promete la CV. | 10 |
| `dibujar_importancia(...)` | Una importancia en barras, la mayor arriba. | 10 T5b |
| `dibujar_perdida_1d`, `dibujar_perfil_en_beta`, `dibujar_confusion`, `dibujar_roc_pr`, `dibujar_sigmoides` | Un perfil de $L_{\text{ent}}$, el resultado de `perfil_en_beta`, la matriz de confusión, las curvas ROC y precisión–recall, y la suma de sigmoides del puente a redes. | — |

## Controles y taller

| Función | Qué hace | Notebooks |
|---|---|---|
| `laboratorio(funcion, **controles)` | Corre una función con controles; se recalcula al soltar cada control. | 01 a 10 |
| `deslizador(etiqueta, minimo, maximo, paso, valor)` | Un deslizador con etiqueta en español. | 01 a 10 |
| `selector(etiqueta, opciones)` | Un menú de opciones. | 01 a 10 |
| `interruptor(etiqueta, valor)` | Una casilla de sí o no. | 01 a 10 |
| `galeria(clase, casos)` | Un botón por caso borde: lo carga, lo dibuja con el análisis de la clase y pregunta. | 01 a 10, T5a T5c |
| `taller(datos, clase)` | Corre el análisis de esa clase sobre tus propios datos. | 01 a 10, T5a T5c |
| `ANALISIS_TALLER` | El análisis que registra cada clase, de la 1 a la 5. | — |

## Un recorrido mínimo

Estas cinco líneas hacen lo que hace casi cualquier notebook de la unidad:

```python
datos = ml.proceso(n=50, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 4 * d["x"])
m = ml.ajustar(datos, phi=ml.polinomio(3))
print(ml.L(m, datos.ent), ml.L(m, datos.val), ml.riesgo(m, datos))
ml.benchmarks(datos, datos.val)
ml.taller(datos, 1)
```

La primera genera los datos y la segunda ajusta. La tercera mide en
entrenamiento, en validación y en el despliegue. La cuarta da el punto de
comparación, y la última corre el análisis de la clase 1 sobre tus datos.
