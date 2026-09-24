---
id: opt-objetivo-regresion-practica
title: Predecir un valor y elegir la complejidad del modelo
nav_title: Regresión
summary: "Ajustar tiempos de entrega, comparar errores y explorar qué ocurre al dejar que el algoritmo elija el grado de un polinomio."
status: ready
estimated_time: 50m
tags: [optimizacion, modelado, regresion]
---

# Predecir un valor y elegir la complejidad del modelo

Una empresa de reparto quiere estimar **cuántos minutos tardará una entrega**
a partir de su distancia. La respuesta es un número. Veremos cómo pasar de
entregas observadas a una regla de predicción, medir sus errores y elegir
cuánta flexibilidad necesita la regla.

## 1 · Empezar por las entregas observadas

Una entrega registrada aporta dos números: distancia y tiempo. Por ejemplo,
las primeras tres filas de **101 entregas simuladas** son estas (cifras
redondeadas):

| $i$ | Distancia $x_i$ (km) | Tiempo $y_i$ (min) |
|---|---:|---:|
| 1 | 0.526 | 3.589 |
| 2 | 0.676 | 14.494 |
| 3 | 0.969 | 13.073 |
| $\vdots$ | $\vdots$ | $\vdots$ |
| $n$ | $x_n$ | $y_n$ |

La última fila representa cualquier conjunto con $n\ge1$ entregas;
en esta simulación, $n=101$. Escribimos cada fila como $(x_i,y_i)$,
con $i=1,\ldots,n$. **$n$ cuenta entregas; $i$ señala una de ellas.**
Los datos ya fueron observados: no podemos elegirlos para que la
predicción resulte más fácil. Aquí distancias y tiempos observados
son no negativos.

En la siguiente nube cada punto representa una entrega. Los tiempos varían
incluso para distancias parecidas: también influyen el tráfico, la preparación
del pedido y otros factores. Para hacer visibles los tiempos atípicos,
**añadimos 25 minutos de retraso a siete entregas**. Estos datos son
simulados para aprender el método; no describen los repartos de una
empresa real.

![Entregas simuladas: el eje horizontal muestra distancia en kilómetros y el vertical, tiempo observado en minutos; la nube presenta dispersión y varias entregas tardías atípicas](../_assets/opt-regresion-datos.png)

El eje horizontal mide distancia y el vertical, tiempo. La dispersión nos
pide una regla que resuma la tendencia sin esperar que acierte cada punto.

## 2 · Probar primero una recta

La regla más sencilla que usaremos es

$$f_\beta(x)=\beta_0+\beta_1x.$$

$\beta_0$ es el tiempo que la recta predice para $x=0$; $\beta_1$ indica
cuánto cambia el tiempo predicho cuando la distancia aumenta un kilómetro.
Por ejemplo, con $\beta_0=10$ y $\beta_1=4$, para una entrega de $3$ km
predecimos **$10+4(3)=22$ minutos**. La suma completa da minutos.

Los dos números de la recta son las **decisiones del ajuste**:
$\beta=(\beta_0,\beta_1)\in\mathbb R^2$. Elegimos una sola pareja para
todas las entregas; los pares $(x_i,y_i)$ permanecen fijos. No imponemos
restricciones a los coeficientes en este primer modelo.

Para la entrega $i$, la predicción es $\widehat y_i(\beta)=f_\beta(x_i)$.
Llamamos **residuo** al error con signo:

$$e_i(\beta)=y_i-\widehat y_i(\beta)=y_i-\beta_0-\beta_1x_i.$$

Si $e_i>0$, la entrega tardó más de lo predicho; si $e_i<0$, tardó menos.
Una vez elegida la recta, cada residuo queda determinado por los datos.

## 3 · Ver el error en seis entregas

Para hacer las cuentas a mano, tomemos seis entregas ficticias. Son un
ejemplo pequeño y distinto de la nube anterior; la regla general sigue
usando $n$ observaciones.

| Caso $i$ | Distancia (km) | Tiempo (min) |
|---|---|---|
| 1 | 1 | 15 |
| 2 | 2 | 17 |
| 3 | 3 | 23 |
| 4 | 4 | 25 |
| 5 | 5 | 31 |
| 6 | 6 | 33 |

Tomemos como referencia $f_\beta(x)=10+4x$. **La escogemos para calcular;
todavía no hemos buscado la mejor recta.** Por ejemplo,

$$
\begin{aligned}
\widehat y_1&=10+4(1)=14,\\
e_1&=15-14=1,\\
\widehat y_2&=10+4(2)=18,\\
e_2&=17-18=-1.
\end{aligned}
$$

Los seis residuos son $(1,-1,1,-1,1,-1)$. El promedio con signo vale
$(1-1+1-1+1-1)/6=0$, aunque ninguna predicción da en el punto observado.

![Tiempos de seis entregas frente a distancia, recta de referencia 10 más 4x y segmentos verticales que muestran los residuos de un minuto](../_assets/opt-regresion-residuos.svg)

El eje horizontal mide distancia y el vertical, tiempo. **Si un punto cae
sobre la recta, su segmento vertical mide cero:** la predicción acierta.
Cuanto más lejos queda el punto de la recta en dirección vertical, mayor
es el tamaño del error. Los segmentos de la figura miden un minuto.

**Piensa: ¿sirve promediar los residuos con su signo?** Un retraso puede
cancelar un adelanto. Para contar el tamaño de ambos, podemos usar el valor
absoluto o el cuadrado de cada residuo.

El **error absoluto medio**, o MAE, promedia los tamaños:

$$\mathrm{MAE}(\beta)=\frac1n\sum_{i=1}^n|e_i(\beta)|.$$

En las seis entregas, $|1|=|-1|=1$, así que

$$\mathrm{MAE}=\frac{1+1+1+1+1+1}{6}=1\text{ minuto}.$$

Para dar mayor peso a errores grandes, primero cuadramos cada residuo.
El **error cuadrático medio**, MSE, es el promedio de esos cuadrados:

$$\mathrm{MSE}(\beta)=\frac1n\sum_{i=1}^n e_i(\beta)^2.$$

El MSE se expresa en minutos cuadrados. Tomamos la raíz **después de
promediar** para volver a minutos; obtenemos RMSE:

$$\mathrm{RMSE}(\beta)=\sqrt{\frac1n\sum_{i=1}^n e_i(\beta)^2}.$$

En el ejemplo, $1^2=(-1)^2=1$:

$$\mathrm{RMSE}=\sqrt{\frac{1+1+1+1+1+1}{6}}=1\text{ minuto}.$$

**Las medidas no valoran igual los errores grandes.** Un residuo que pasa
de 1 a 3 minutos aporta 1 y 3 al valor absoluto, pero 1 y 9 al cuadrado.
La raíz final devuelve RMSE a minutos sin deshacer esa diferencia de peso.

![Valor absoluto y cuadrado de un residuo en paneles separados: el eje horizontal es el error con signo, y los ejes verticales miden minutos y minutos cuadrados respectivamente](../_assets/opt-regresion-perdidas.svg)

La gráfica muestra las contribuciones de **un caso**. Para obtener MAE
hay que promediar los valores absolutos; para obtener RMSE hay que
promediar los cuadrados y después tomar la raíz.

## 4 · Ajustar la recta a las entregas

Una medida de error nos permite **elegir** la recta en vez de proponer sus
coeficientes a ojo. Si nos importa el error absoluto medio, resolvemos

$$\min_{\beta\in\mathbb R^2}\quad\mathrm{MAE}(\beta).$$

$$\beta^\star_{\mathrm{MAE}}\in
\operatorname*{arg\,min}_{\beta\in\mathbb R^2}\mathrm{MAE}(\beta).$$

Si queremos dar más peso a los errores grandes, resolvemos

$$\min_{\beta\in\mathbb R^2}\quad\mathrm{RMSE}(\beta).$$

$$\beta^\star_{\mathrm{RMSE}}\in
\operatorname*{arg\,min}_{\beta\in\mathbb R^2}\mathrm{RMSE}(\beta).$$

En ambos problemas elegimos **los dos coeficientes juntos**. El mínimo
es un valor de error; el argmin es el conjunto de parejas que lo alcanzan.
Usamos pertenencia porque puede haber varias soluciones.

**Son objetivos distintos y pueden elegir rectas diferentes.** Si queremos
penalizar especialmente los errores grandes, RMSE refleja esa preferencia.
MAE mide el tamaño de cada error sin elevarlo al cuadrado. La elección del
criterio debe responder al propósito de la predicción.

Con las seis entregas del cálculo manual, **resolver los dos problemas da
resultados diferentes**. El ajuste por RMSE es
$f_\beta(x)=10.6+(134/35)x$; un ajuste óptimo por MAE es
$f_\beta(x)=11.4+3.6x$. Evaluando ambas rectas obtenemos estos errores,
en minutos y redondeados:

| Ajuste | MAE | RMSE |
|---|---|---|
| Minimiza MAE | 0.800 | 1.033 |
| Minimiza RMSE | 0.914 | 0.956 |

Cada una gana con el objetivo para el que se ajustó. Estas rectas son
resultados de optimización, a diferencia de la referencia $10+4x$.

Volvamos ahora a las **101 entregas simuladas** del comienzo. Sus puntos
tienen dispersión y algunos tiempos atípicos. Al ajustar
**la misma nube** con MAE y con RMSE podemos ver cómo cambia la recta según
lo que penalizamos. La figura compara ambos ajustes; sus coeficientes y
errores se calcularon con los datos simulados.

![La misma nube simulada con dos rectas ajustadas: eje horizontal distancia en kilómetros, eje vertical tiempo en minutos; MAE y RMSE responden de modo distinto a las entregas tardías atípicas](../_assets/opt-regresion-ajustes.png)

El eje horizontal mide distancia y el vertical, tiempo. El ajuste por
MAE dio $f_\beta(x)=10.675+3.178x$; el ajuste por RMSE dio
$f_\beta(x)=8.556+3.705x$. Sus errores, en minutos, son:

| Ajuste | MAE | RMSE |
|---|---:|---:|
| Minimiza MAE | **3.630** | 7.166 |
| Minimiza RMSE | 4.270 | **6.841** |

Los coeficientes se muestran redondeados, pero los errores se calcularon
con los ajustes completos. Cada método logra el menor valor de su propia
medida. **La función objetivo expresa una preferencia:** RMSE carga más
peso a los residuos grandes y aquí mueve la recta hacia algunos puntos
atípicos.

### Minimizar RMSE mediante mínimos cuadrados

Ya definimos MSE como el promedio de los residuos al cuadrado. Para dos
parejas cualesquiera $\beta$ y $\gamma$, sus valores de MSE son
no negativos. Como la raíz cuadrada es estrictamente creciente,

$$
\begin{aligned}
\mathrm{MSE}(\beta)&\le\mathrm{MSE}(\gamma)\\
&\Longleftrightarrow\\
\sqrt{\mathrm{MSE}(\beta)}&\le\sqrt{\mathrm{MSE}(\gamma)}\\
&\Longleftrightarrow\\
\mathrm{RMSE}(\beta)&\le\mathrm{RMSE}(\gamma).
\end{aligned}
$$

Por tanto, **minimizar MSE y minimizar RMSE produce el mismo conjunto de
coeficientes óptimos**. El mínimo de RMSE es la raíz del mínimo de MSE.
Esta equivalencia no incluye a MAE.

MSE es una función **cuadrática, suave y convexa** de los coeficientes.
Este ajuste se conoce como [mínimos cuadrados en regresión lineal](https://cs229.stanford.edu/notes_archive/cs229-notes-all/cs229-notes1.pdf).
RMSE también es convexa: es la norma euclídea del vector de residuos dividida
entre $\sqrt n$. Puede no ser diferenciable cuando todos los residuos son
cero; por eso conviene distinguirla de MSE al hablar de derivadas.

## 5 · Ver qué pasa si cambiamos solo la pendiente

La optimización anterior mueve $\beta_0$ y $\beta_1$ a la vez. Para
imaginar la función objetivo, podemos hacer un **corte del problema**:
fijamos $\beta_0=10$ y dejamos variar solo $\beta_1$. Cada valor de la
pendiente produce una recta distinta y, al medir sus residuos sobre los
mismos datos, un valor de MAE y otro de RMSE.

![Errores MAE y RMSE de las entregas simuladas al variar la pendiente con intercepto fijo en 10: eje horizontal pendiente, eje vertical error en minutos](../_assets/opt-regresion-pendiente.png)

En esta figura, el eje horizontal es $\beta_1$ y el vertical es el error
en minutos. Los puntos más bajos señalan las mejores pendientes **entre las
rectas cuyo intercepto es 10**. No tienen por qué coincidir con los ajustes
completos de la sección anterior, donde ambos coeficientes eran libres.
En este corte, MAE alcanza su mínimo con $\beta_1\approx3.250$ y RMSE
con $\beta_1\approx3.526$; las pendientes del ajuste completo fueron
$3.178$ y $3.705$, respectivamente.

## 6 · Conocer otras familias de reglas

Una recta quizá no describa bien todos los patrones. También podemos
encontrar tendencias cuadráticas, cúbicas, senoidales o recíprocas.
**Elegir una familia** delimita qué formas podrá tener la regla antes
de ajustar sus parámetros.

En otro experimento simulado, independiente de las entregas, generamos
**120 observaciones por familia** en posiciones irregulares. Añadimos pequeñas
variaciones a sus respuestas para que los puntos no caigan perfectamente
sobre una curva. **En cada ejemplo hay un solo conjunto de datos:** usamos
esos mismos puntos para ajustar los coeficientes y calcular el error.

En cada figura, la vista superior muestra en detalle el **intervalo
observado**; la inferior incluye valores de $x$ fuera de él. Su franja
sombreada marca dónde están los datos. **Cada curva ajustada conserva
los mismos coeficientes en las dos vistas:** cambiar el intervalo
dibujado no equivale a volver a optimizar el modelo. Las escalas
verticales son distintas y se indican en los ejes.

Los primeros cuatro casos se ajustan en $[-1,1]$ y se dibujan hasta
$[-1.5,1.5]$; el recíproco se ajusta en $[1,5]$ y se dibuja en
$[0.5,6]$.

**Lineal.** La relación generadora es $4+2x$. Una recta puede seguir
esta tendencia que crece a ritmo constante. Compara los ajustes de
grados 1, 2 y 15 dentro de la zona observada y luego mira cómo
continúan fuera de ella: un buen ajuste local no fija por sí solo la
continuación.

![Datos simulados con tendencia lineal y polinomios ajustados: vista ampliada del intervalo observado y vista extendida; el sombreado señala dónde están los datos](../_assets/opt-regresion-forma-lineal.png)

**Cuadrática.** La relación es $4+1.5x+4x^2$. Una recta no puede
reproducir la curvatura de una parábola; el grado 2 sí puede describirla,
aunque los puntos ruidosos no caigan exactamente sobre ella. También se
muestra el ajuste de grado 15.

![Datos simulados con tendencia cuadrática y polinomios ajustados: vista ampliada del intervalo observado y vista extendida con los mismos ajustes](../_assets/opt-regresion-forma-cuadratica.png)

**Cúbica.** La relación $4+2x-2x^2+3x^3$ cambia de curvatura.
Comparamos grados 1, 3 y 15. Aquí también conviene distinguir entre
seguir la forma general y perseguir cada variación del ruido.

![Datos simulados con tendencia cúbica y polinomios ajustados, vistos dentro y fuera del intervalo observado](../_assets/opt-regresion-forma-cubica.png)

**Senoidal.** La relación es $4+2\sin(5x)$ y se muestran grados 1,
5 y 15. Un polinomio puede aproximar una parte de la onda en el
intervalo donde se ajustó. Esa aproximación no lo convierte en una
función periódica: al prolongarla puede dejar de repetir las
oscilaciones.

![Datos simulados con tendencia senoidal y polinomios ajustados: la vista extendida sombrea el intervalo observado](../_assets/opt-regresion-forma-senoidal.png)

**Recíproca.** La relación es $2+5/x$ y se muestran grados 1, 4 y 15.
La regla $1/x$ cambia con rapidez cuando $x$ se acerca a cero. Los datos
observados están lejos de ese punto; la vista extendida muestra qué
ocurre al acercarse, sin incluir $x=0$, donde la regla no está definida.

![Datos simulados con tendencia recíproca y polinomios ajustados: vista del intervalo observado y extensión hacia valores positivos más pequeños y grandes](../_assets/opt-regresion-forma-reciproca.png)

**Mira qué cambia al dar más grados al polinomio.** Más flexibilidad
permite acercarse a los puntos, pero también puede producir curvas que
oscilan mucho o se disparan al prolongarlas. **El error que calculamos en
los puntos no penaliza directamente esas formas.** Las figuras muestran
lo que sucede en estos ejemplos; no establecen que todo polinomio de
grado alto se comporte así.

Nos concentraremos en la familia de polinomios. Para un grado máximo
**fijo** $N$, la regla es

$$f_{\beta,N}(x)=\sum_{j=0}^{N}\beta_jx^j.$$

El índice $j=0,\ldots,N$ recorre los coeficientes. El término $j=0$ es
$\beta_0$, porque $x^0=1$. Para un $N$ fijo elegimos

$$\beta=(\beta_0,\ldots,\beta_N)\in\mathbb R^{N+1}.$$

**No confundamos $n$ con $N$:** $n$ cuenta las observaciones;
$N$ limita el grado y determina que ajustamos $N+1$ coeficientes.
El coeficiente de mayor índice puede ser cero; no exigimos grado exactamente
$N$.

La curva puede ser no lineal en $x$, pero sigue siendo **lineal en los
coeficientes que elegimos**: los valores $x_i^j$ son datos calculados.
Para cada grado fijo, minimizar MSE sigue siendo un problema convexo de
mínimos cuadrados. Una curva polinómica puede aproximar una onda o una
regla recíproca en un intervalo adecuado; eso **no la convierte en la
función seno ni en $1/x$ exactas**.

## 7 · Preguntar si conviene aumentar el grado

Si además elegimos el grado, necesitamos un límite finito conocido
$N_{\max}\ge1$, entero. Una primera propuesta sería

$$
\min_{\substack{N\in\{1,\ldots,N_{\max}\}\\
\beta\in\mathbb R^{N+1}}}\quad\mathrm{MSE}(\beta,N),
$$

con el error calculado sobre los mismos $n$ datos observados

$$\mathrm{MSE}(\beta,N)=\frac1n
\sum_{i=1}^n\bigl(y_i-f_{\beta,N}(x_i)\bigr)^2.$$

La misma selección conjunta podría escribirse con RMSE sin cambiar su
argmin. Es una elección discreta de $N$ entre problemas convexos; no
buscamos un gradiente respecto del número entero de grado.

**Piensa: ¿qué impide que una curva más flexible gane solo por ajustarse
mejor a estas entregas?**

Cualquier modelo permitido para $N$ también está permitido para $N+1$:
basta añadir un coeficiente cero. En efecto,

$$
\begin{aligned}
f_{(\beta,0),N+1}(x)
&=\sum_{j=0}^{N}\beta_jx^j+0x^{N+1}\\
&=f_{\beta,N}(x).
\end{aligned}
$$

Las predicciones y el error no cambian. Al minimizar sobre una familia
que contiene a la anterior, **el menor error en esos mismos datos no puede
aumentar**. Esto vale para MAE y RMSE, además de MSE. Puede quedarse igual:
no afirmamos que el optimizador siempre deba elegir el grado más alto.

Si las $n$ entradas son distintas y permitimos $N\ge n-1$, existe un
polinomio que pasa por todos los puntos y logra error cero en esos datos.
Si dos entregas tienen la misma distancia pero tiempos diferentes,
ninguna función de esa distancia puede acertar exactamente ambos tiempos.

**Subajuste:** la familia es demasiado limitada para seguir el patrón.
La recta del ejemplo cuadrático no puede doblarse para acompañar la nube,
por mucho que ajustemos sus dos coeficientes.

En el otro extremo, dar más flexibilidad permite seguir incluso pequeñas
irregularidades de los puntos. **Esa es la intuición que queremos abrir
sobre el sobreajuste:** una curva puede acercarse más a cada dato y, al mismo
tiempo, volverse muy ondulada. Un grado alto no obliga a que esto suceda;
observa las curvas concretas de los ejemplos.

Regresa a las figuras **lineal** y **cuadrática**. En la vista ampliada,
mira qué tanto se doblan las curvas para acercarse a los puntos. En la
vista extendida, mira cómo continúan **esos mismos polinomios**. Dibujarlos
fuera del intervalo no añade observaciones ni cambia el objetivo: solo
permite ver la forma de la regla que hemos elegido.

## 8 · Ver qué premia el objetivo al elegir el grado

Volvamos a las **mismas seis entregas** del cálculo manual. Para cada
$N=1,\ldots,5$, ajustamos los coeficientes por mínimos cuadrados y
calculamos RMSE sobre esos seis puntos.

![Polinomios de grados 1, 3 y 5 ajustados a las mismas seis entregas y RMSE sobre esos datos frente al grado permitido](../_assets/opt-regresion-grado.svg)

En las curvas, los ejes son distancia y tiempo. En la comparación de
errores, el eje horizontal es $N$ y el vertical es **RMSE en minutos**.

| Grado permitido $N$ | RMSE en las seis entregas |
|---|---:|
| 1 | 0.956 |
| 2 | 0.956 |
| 3 | 0.823 |
| 4 | 0.823 |
| 5 | 0.000 |

Las cifras están redondeadas. El polinomio de grado 5 pasa por todos los
puntos: **si solo pedimos el menor error en estas entregas, gana ese ajuste.**
El algoritmo cumple exactamente lo que le pedimos. No incluimos en el
objetivo ningún costo por usar más coeficientes ni por producir una curva
con tantas variaciones entre los puntos.

Ahora mira el error en los ejemplos **lineal y cuadrático de 120 puntos**.
Para cada uno conservamos su único conjunto de datos y comparamos los
grados $N=1,\ldots,16$.

![RMSE sobre los mismos puntos observados al aumentar el grado permitido, para los ejemplos lineal y cuadrático](../_assets/opt-regresion-error-grado.png)

El eje horizontal muestra $N$; el vertical, el RMSE en unidades de la
respuesta. La línea amarilla señala el grado de la curva original de
la simulación: 1 para la recta y 2 para la parábola. Sin embargo, **el
menor error en los puntos se alcanza con grado 16 en ambos ejemplos**,
señalado en rosa.

**Al permitir más grados, el menor error baja o se mantiene.**
La caída inicial del caso cuadrático tiene una razón visible: pasar de
una recta a una parábola permite seguir la curvatura de la nube. Seguir
aumentando el grado puede reducir el error un poco más, aunque la forma
resultante sea mucho más complicada.

**La pregunta que dejamos abierta:** si el algoritmo solo busca reducir
el error en estos puntos, ¿qué razón le hemos dado para preferir una curva
sencilla? Por ahora queremos reconocer ese límite del planteamiento.
Elegir el grado también es parte del problema de optimización, y el
objetivo debe reflejar qué esperamos de la regla además de acercarse a
los datos.

## 9 · Resumen de los modelos y sus métodos

| Signo | Qué representa |
|---|---|
| $n,i$ | Cantidad e índice de entregas |
| $x_i,y_i$ | Distancia y tiempo observados |
| $\beta_j\in\mathbb R$ | Coeficiente que elegimos |
| $\beta$ | Vector de coeficientes |
| $\beta^\star$ | Coeficientes de una solución óptima |
| $\gamma$ | Otro vector para comparar |
| $f_\beta,f_{\beta,N}$ | Reglas de predicción |
| $\widehat y_i,e_i$ | Predicción y residuo calculados |
| $u_i\ge0$ | Auxiliar para error absoluto |
| MAE, RMSE | Medidas de error, en minutos |
| MSE | Error en minutos cuadrados |
| $\beta^\star_{\mathrm{MAE}}$ | Ajuste por MAE |
| $\beta^\star_{\mathrm{RMSE}}$ | Ajuste por RMSE |
| $N\in\{1,\ldots,N_{\max}\}$ | Grado permitido, entero |
| $j=0,\ldots,N$ | Índice de coeficiente |
| $N_{\max}$ | Mayor grado candidato, dato |
| $\beta^\star(N)$ | Ajuste para el grado $N$ |
| $N^\star$ | Grado seleccionado |
| $T$ | Número de pasos del método |

**Decisiones y resultados.** Elegimos coeficientes reales y, al comparar
familias, un grado entero de un conjunto finito. Las predicciones, residuos
y medidas de error se calculan. Los $u_i$ son variables auxiliares de la
reformulación de MAE; no cambian los tiempos reales.

**Los dos modelos para la recta** eligen $\beta\in\mathbb R^2$:

$$\min_{\beta\in\mathbb R^2}\quad\mathrm{MAE}(\beta).$$

$$\min_{\beta\in\mathbb R^2}\quad\mathrm{RMSE}(\beta).$$

**Elegir grado y coeficientes por el error en los datos observados** es resolver

$$
\min_{\substack{N\in\{1,\ldots,N_{\max}\}\\
\beta\in\mathbb R^{N+1}}}\quad\mathrm{MSE}(\beta,N).
$$

Una solución reúne las dos decisiones:

$$
(N^\star,\beta^\star)\in
\operatorname*{arg\,min}_{\substack{N\in\{1,\ldots,N_{\max}\}\\
\beta\in\mathbb R^{N+1}}}\mathrm{MSE}(\beta,N).
$$

El grado determina cuántos coeficientes elegimos. Los datos $(x_i,y_i)$
permanecen fijos; todas las comparaciones usan esos mismos puntos.

Cada grado fijo da un ajuste convexo. La elección conjunta entre grados
no es un único problema convexo con todas las decisiones continuas: $N$
pertenece a un conjunto discreto.

**Recta con MAE.** Minimizamos $\mathrm{MAE}(\beta)$ sobre
$\beta\in\mathbb R^2$. Es un problema convexo, no suave en general.
La formulación con $u_i\ge\pm e_i$ y $u_i\ge0$ es un programa lineal.
Construir sus restricciones cuesta $O(n)$; resolverlo mediante un método
de programación lineal tiene un costo que depende del tamaño del problema,
el método y la precisión. No se deduce una resolución en $O(n)$ del costo
de escribir sus restricciones.

Para ver la reformulación completa, añadimos una variable auxiliar
$u_i\ge0$ por observación y exigimos $u_i\ge e_i(\beta)$ y
$u_i\ge-e_i(\beta)$. Las dos desigualdades implican
$u_i\ge|e_i(\beta)|$. Resolvemos

$$\min_{\beta\in\mathbb R^2,\ u\in\mathbb R^n}
\quad\frac1n\sum_{i=1}^n u_i$$

sujeto, para cada $i=1,\ldots,n$, a

$$
\begin{aligned}
u_i&\ge y_i-\beta_0-\beta_1x_i,\\
u_i&\ge-y_i+\beta_0+\beta_1x_i,\\
u_i&\ge0.
\end{aligned}
$$

Para coeficientes fijos, minimizar la suma lleva cada $u_i$ a su menor
valor permitido, $|e_i(\beta)|$. Así recuperamos exactamente MAE.
Los $u_i$ miden tamaños de error; no son tiempos observados. La
[reformulación del error absoluto como programa lineal](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf#page=308)
aparece en Boyd y Vandenberghe, sección 6.1.1.

**Recta con RMSE.** Minimizamos $\mathrm{RMSE}(\beta)$ sobre el mismo
dominio. Comparte argmin con MSE, una cuadrática convexa suave. Podemos
resolver mínimos cuadrados con factorización QR en $O(n)$ cuando las dos
columnas son independientes; para la recta basta que haya al menos dos
distancias distintas. Una descomposición SVD también permite tratar
coeficientes no determinados de manera única.

Un paso de gradiente de MSE con todos los datos cuesta $O(n)$; $T$ pasos
cuestan $O(Tn)$. $T$ depende del método, los datos y la precisión; no es
una constante garantizada. Evaluar MAE o RMSE de una recta fija cuesta
$O(n)$ y no equivale a resolver su problema de ajuste.

**Polinomio con grado fijo.** Tiene $N+1$ coeficientes y sigue siendo
lineal en ellos. Cuando $n\ge N+1$ y las columnas $1,x,\ldots,x^N$
son independientes, QR para mínimos cuadrados cuesta
$O\bigl(n(N+1)^2\bigr)$ en el conteo usual de operaciones aritméticas.
Con rango insuficiente podemos usar SVD. Evaluar el polinomio y calcular
su error en los $n$ puntos cuesta $O\bigl(n(N+1)\bigr)$.

**Selección de grado.** Llamamos $\beta^\star(N)$ a un ajuste óptimo
para el grado fijo $N$. Recorremos los candidatos finitos, ajustamos cada
uno y comparamos sus errores en los mismos datos. En caso de empate
podemos preferir el menor grado. El costo total suma los ajustes y las
evaluaciones de todos los grados considerados. Elegir $N$ es una decisión
discreta entre problemas convexos; no derivamos respecto de $N$.

## 10 · Elegir un modelo que quepa en el dispositivo

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#opt-regresion-ej-capacidad title="Comparar curvas con una capacidad limitada"}
El equipo quiere instalar el predictor de tiempo en un dispositivo que
puede guardar **como máximo $B$ coeficientes**, donde $B\ge2$ es un entero
conocido. Su implementación guarda todos los coeficientes de la regla,
incluso los que valen cero. Puede evaluar los polinomios candidatos con
$N\in\{1,\ldots,N_{\max}\}$.

Tenemos **un único conjunto de $n$ entregas observadas**. Queremos elegir
el grado y los coeficientes que den el menor RMSE en esas entregas, sin
exceder la capacidad del dispositivo.

1. Distingue los datos, las decisiones y las cantidades calculadas.
   Traduce la capacidad del dispositivo a una condición sobre el modelo.
2. Escribe el problema completo: objetivo, variables y restricciones.
   ¿Cómo resolverías un empate entre grados con el mismo error mínimo?
3. Describe un procedimiento finito para escoger la regla. ¿La capacidad
   del dispositivo basta para evitar una curva con muchas oscilaciones?
:::

::: hint {#opt-regresion-pista-capacidad of="opt-regresion-ej-capacidad" title="Pista 1 · Contar lo que debe guardar el dispositivo"}
Escribe los coeficientes de una recta y de un polinomio con término
cuadrático. ¿Cuántos lugares ocupan? Recuerda que el intercepto también
se guarda y que el dispositivo conserva los coeficientes cero.
:::

::: hint {#opt-regresion-pista-comparacion of="opt-regresion-ej-capacidad" title="Pista 2 · Separar las dos decisiones"}
Primero piensa qué grados caben. Si fijaras uno de ellos, ¿qué números
faltaría elegir y con qué objetivo? Después podrías comparar los
resultados. Recuerda que añadir un coeficiente cero conserva la curva.
:::

::: answer {#opt-regresion-respuesta-capacidad of="opt-regresion-ej-capacidad" title="Respuesta · Limitar el grado y minimizar el error"}

$B$ y $N_{\max}$ son datos enteros, además de los $n$ pares $(x_i,y_i)$.
Elegimos $N$ y sus $N+1$ coeficientes reales. Las predicciones y los
residuos se calculan a partir de esas decisiones.

Como el dispositivo guarda todos los coeficientes, la condición es
$N+1\le B$. El modelo completo queda

$$
\begin{aligned}
\min_{N,\,\beta}\quad &\mathrm{RMSE}(\beta,N)\\
\text{sujeto a}\quad &N\in\{1,\ldots,N_{\max}\},\\
&N+1\le B,\\
&\beta\in\mathbb R^{N+1}.
\end{aligned}
$$

Los grados disponibles forman el conjunto

$$\mathcal G=\{N\in\{1,\ldots,N_{\max}\}:N+1\le B\}.$$

Es finito y no vacío: $N=1$ está permitido porque $B\ge2$ y
$N_{\max}\ge1$. Para cada $N\in\mathcal G$ ajustamos los coeficientes:

$$\beta^\star(N)\in
\operatorname*{arg\,min}_{\beta\in\mathbb R^{N+1}}
\mathrm{MSE}(\beta,N).$$

Esto también minimiza RMSE. Si hay varios vectores óptimos, podemos
escoger el de menor suma de cuadrados de sus coeficientes. Después
comparamos **el error en las mismas entregas**:

$$N^\star\in\operatorname*{arg\,min}_{N\in\mathcal G}
\mathrm{RMSE}\bigl(\beta^\star(N),N\bigr).$$

En caso de empate elegimos el menor $N$. La solución del problema
conjunto es $(N^\star,\beta^\star(N^\star))$.

| Signo | Papel |
|---|---|
| $x_i,y_i$ | Datos de las $n$ entregas |
| $B$ | Capacidad conocida |
| $N_{\max}$ | Límite conocido |
| $\mathcal G$ | Grados permitidos |
| $N,\beta$ | Grado y coeficientes que elegimos |
| $\beta^\star(N)$ | Ajuste para un grado fijo |
| $N^\star$ | Grado seleccionado |

**Tipo, método y costo.** La selección es discreta y finita; cada ajuste
por MSE es convexo. Recorremos $\mathcal G$, ajustamos por QR o SVD y
comparamos RMSE. Sumamos los costos de esos ajustes y comparaciones,
con las condiciones de tamaño y rango explicadas en el resumen.

**La capacidad limita el grado, pero no controla cuánto se curva la
regla ni cuánto crecen sus valores.** Entre los grados que caben, el objetivo sigue premiando solo
el menor error en los puntos. Una restricción de almacenamiento resuelve
ese límite del dispositivo; por sí sola no expresa una preferencia por
curvas que cambien suavemente.
:::

Siguiente ejemplo: [[opt-objetivo-juego-practica|elegir una jugada cuando el rival responde]].
