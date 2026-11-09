---
id: notacion-aprendizaje-maquina
title: Toda la notación, en una hoja
nav_title: Notación
summary: "Cada símbolo que usa la unidad de aprendizaje de máquina, qué significa y en qué página se presentó, con los avisos de letras que cambian de sentido y la leyenda única de las figuras."
status: ready
estimated_time: 15m
tags: [aprendizaje-maquina, referencia, notacion]
---

# Toda la notación, en una hoja

Todos los símbolos están definidos en su página. Si encuentras uno a media
lectura y no recuerdas qué era, búscalo aquí en vez de retroceder.

**Cómo leer la flecha:** al final de cada renglón, *→ página* dice dónde se
**presentó** el símbolo. Si algo te resulta opaco, vuelve a esa página.

## Cuatro convenciones que valen en toda la unidad

- **Gorro para lo estimado.** Lo que sale de una muestra lleva gorro:
  $\widehat\beta$, $\widehat f$, $\widehat y_i$, $\widehat N$. Siempre es el
  gorro ancho, $\widehat{\ \cdot\ }$.
- **Estrella para el óptimo teórico.** Desde la clase 1, la estrella marca
  el mejor valor de un problema sobre la población, como $N^\star$. El
  $\beta^\star$ de la clase 0 y de la unidad 6 se escribe, en esta notación,
  $\widehat\beta$: depende de la muestra.
- **El argmin es un conjunto.** Se escribe
  $\widehat\beta\in\operatorname*{arg\,min}_\beta L_{\text{ent}}(\beta)$.
  Va «$=$» solo si el texto dice que el mínimo es único; con empates, el
  texto nombra la regla, por ejemplo «el menor $N$».
- **La constante va dentro de $\phi$.** La primera coordenada de $\phi(x)$
  es 1, así que $\beta_0$ es el intercepto y $q$ cuenta todas las columnas
  de $\Phi$. Cuando el intercepto va aparte, la página lo dice.

## Lo que traes de la unidad 6 y de antes

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $n$, $i$ | Número de observaciones y su índice. *→ Repaso: qué es aprender* |
| $x_i$, $y_i$ | Entrada y respuesta de la observación $i$. *→ Repaso: qué es aprender* |
| $\beta$, $\beta_0$, $\beta_j$ | Los parámetros; el intercepto; el coeficiente de la columna $j$. *→ Repaso: qué es aprender* |
| $\beta^\star$ | El minimizador del ajuste a datos, en la clase 0 y en la unidad 6. Desde la clase 1 se escribe $\widehat\beta$. *→ Repaso: qué es aprender* |
| $f_\beta(x)$ | El modelo con parámetros $\beta$, evaluado en $x$. *→ Repaso: qué es aprender* |
| $\widehat y_i$, $e_i$ | La predicción y el residual, $e_i=y_i-\widehat y_i$. *→ Repaso: qué es aprender; residual en Leer el error* |
| $\ell_i$, $L$ | La pérdida de la observación $i$ y su promedio. *→ ¿Qué es f?* |
| $\mathrm{MAE}$, $\mathrm{MSE}$, $\mathrm{RMSE}$ | Error absoluto medio, cuadrático medio y su raíz, $\mathrm{RMSE}=\sqrt{\mathrm{MSE}}$. *→ Repaso: qué es aprender; RMSE en Leer el error* |
| $N$, $N_{\max}$ | Grado del polinomio y su tope. *→ ¿Qué es f?* |
| $z_i$, $\sigma(z)$, $p_i$ | Puntaje, sigmoide $\sigma(z)=1/(1+e^{-z})$ y probabilidad que anuncia el modelo, $p_i=\sigma(z_i)$. *→ Pérdida, métrica y desbalanceo* |
| $A$, $K$ | Aciertos y número de clases. *→ Pérdida, métrica y desbalanceo* |
| $\mathcal L$, $\mu\ge0$ | El lagrangeano y su multiplicador de desigualdad. *→ Repaso: qué es aprender; en uso, El lagrangeano en acción* |
| $g(\beta)\le d$ | Una restricción de desigualdad. *→ Polinomios, capacidad y supuestos* |
| $\Pr(\cdot)$, $E[\cdot]$ | Probabilidad y valor esperado. *→ Repaso: qué es aprender* |
| $\cdot^{\mathsf T}$ | Traspuesta: $\beta^{\mathsf T}\phi(x)=\sum_j\beta_j[\phi(x)]_j$. *→ ¿Qué es f?* |

## Clase 0 · Qué es aprender

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $T$, $E$, $P$ | Tarea, experiencia y desempeño en la definición de Mitchell. Solo viven en esa definición: después no se usan con ese sentido. *→ Repaso: qué es aprender* |
| $\phi(x)$ | Lo que el modelo ve de cada entrada; por ejemplo, $\phi(3)=(1,3,9)$. Se presenta en palabras y con una figura. *→ Repaso: qué es aprender* |

## Clase 1 · El problema

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $f$ | La función verdadera del proceso, sobre todas las variables. *→ ¿Qué es f?* |
| $\varepsilon$ | El ruido: $y=f(x)+\varepsilon$, con $E[\varepsilon\mid x]=0$. *→ ¿Qué es f?* |
| $\sigma_\varepsilon^2(x)$, $\sigma_\varepsilon^2$ | Varianza del ruido dado $x$, y el caso constante. El ruido lleva siempre subíndice: $\sigma$ sola es la sigmoide. *→ ¿Qué es f?* |
| $\operatorname{Var}(\cdot)$ | Varianza. $\operatorname{Var}(\varepsilon)$ es la del ruido sin condicionar. *→ ¿Qué es f?* |
| $E[y\mid x_{\text{visibles}}]$ | La media de $y$ con lo que el modelo ve: el mejor predictor cuadrático con esas variables. *→ ¿Qué es f?* |
| $J$, $j$, $x_{ij}$, $X$ | Número de variables, su índice, la variable $j$ de la observación $i$ y la matriz de datos $n\times J$. *→ ¿Qué es f?* |
| $x_1, x_2, \dots$ | Con número, son variables (columnas), no observaciones. *→ ¿Qué es f?* |
| $\Phi$, $q$ | La matriz de diseño $n\times q$ y su número de columnas, intercepto incluido. Para un polinomio, $q=N+1$. *→ ¿Qué es f?* |
| $[\phi(x)]_h$ | La componente $h$ de $\phi(x)$. Nunca $\phi_h$. *→ ¿Qué es f?* |
| $r$, $\theta$ | Radio y ángulo de las coordenadas polares, en los anillos. *→ ¿Qué es f?* |
| $\widehat\beta$, $\widehat f$ | El ajuste a una muestra y la función que da: $\widehat f=f_{\widehat\beta}$. *→ ¿Qué es f?* |
| $R(\beta)$, $R(\widehat\beta)$ | El riesgo: la pérdida esperada con datos nuevos. En $\widehat\beta$ es el error de generalización. *→ ¿Qué es f?* |
| $\mathcal D$, $n_{\mathcal D}$, $L_{\mathcal D}$ | Un conjunto de datos, su tamaño y su pérdida promedio. *→ ¿Qué es f?* |
| $\mathcal D_{\text{ent}}$, $n_{\text{ent}}$, $L_{\text{ent}}$ | El conjunto de entrenamiento, su tamaño y su pérdida promedio. *→ ¿Qué es f?* |
| $R_{\text{Bayes}}$ | El piso: el riesgo del mejor predictor con las variables visibles, para una pérdida dada. *→ ¿Qué es f?* |
| $\bar y$ | El promedio de $y$ en un conjunto; en clasificación binaria, la proporción de positivos. *→ ¿Qué es f?* |
| $\ln$ | Logaritmo natural, en toda fórmula. $\log_{10}$ solo aparece en ejes. *→ ¿Qué es f?* |
| $\pi$, $\sin$, $\cos$ | El número pi, seno y coseno, en el proceso del seno y sus ejercicios. *→ Polinomios, capacidad y supuestos* |
| $\phi_N$, $\mathcal H_N$ | $\phi_N(x)=(1,x,\dots,x^N)$, el polinomio de grado $N$, y el conjunto de polinomios de grado $\le N$. *→ Polinomios, capacidad y supuestos* |
| $x_0$, $\xi$ | Centro de Taylor y punto del resto de Taylor. *→ Polinomios, capacidad y supuestos* |
| $x_{\min}$, $x_{\max}$ | Extremos del intervalo de Stone–Weierstrass. *→ Polinomios, capacidad y supuestos* |
| $\Omega(\beta)$, $d$ | Una medida de capacidad y su cota, $\Omega(\beta)\le d$. *→ Polinomios, capacidad y supuestos* |
| $\operatorname{grado}(f_\beta)$ | El grado del polinomio: la $\Omega$ del caso duro, $N\le N_{\max}$. *→ Polinomios, capacidad y supuestos* |
| $\mathrm{brecha}(\widehat\beta)$ | $R(\widehat\beta)-L_{\text{ent}}(\widehat\beta)$. *→ Polinomios, capacidad y supuestos* |

## Clase 2 · Separar los datos

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $\mathcal D_{\text{val}}$, $\mathcal D_{\text{prueba}}$ | Los conjuntos de validación y de prueba. *→ Entrenamiento y prueba* |
| $n_{\text{val}}$, $n_{\text{prueba}}$ | Sus tamaños. *→ Entrenamiento y prueba* |
| $L_{\text{val}}$, $L_{\text{prueba}}$ | La misma pérdida promedio $L$, medida en cada conjunto. *→ Entrenamiento y prueba* |
| $\widehat N$ | El grado que eligen los datos: con empate, el menor $N$. *→ Entrenamiento y prueba* |
| $\mathrm{EE}$, $s_\ell$ | Error estándar, $s_\ell/\sqrt n$, y la desviación estándar de las pérdidas $\ell_i$ (no de los residuales). *→ Entrenamiento y prueba* |
| $k$, $\mathcal D_1,\dots,\mathcal D_k$ | Número de pliegues y los pliegues. *→ Validación cruzada* |
| $m$, $\widehat\beta^{(-m)}$ | El índice de pliegue y el ajuste hecho sin el pliegue $m$. *→ Validación cruzada* |
| $\mathrm{CV}_k$ | La estimación por validación cruzada: el promedio de $L_{\mathcal D_m}(\widehat\beta^{(-m)})$. *→ Validación cruzada* |
| $M$ | Número de candidatos de hiperparámetro. *→ Validación cruzada* |
| $E_{\mathcal D}[\cdot]$ | Valor esperado sobre conjuntos de entrenamiento distintos. *→ Validación cruzada* |
| $\text{sesgo}(x)$, $\text{varianza}(x)$ | En un punto $x$: $E_{\mathcal D}[\widehat f(x)]-f(x)$ y cuánto se mueve $\widehat f(x)$ de un conjunto a otro. *→ Sesgo y varianza* |
| $N^\star$ | El grado que minimiza el error total esperado: el óptimo teórico. *→ Sesgo y varianza* |

## Clase 3 · Leer el error y regularizar

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $\operatorname{corr}(\cdot,\cdot)$, $\operatorname{cov}(\cdot,\cdot)$ | Correlación y covarianza; por ejemplo, $\operatorname{corr}(x_1,x_3)$. *→ Leer el error* |
| $Z$ | Una normal estándar, en $\varepsilon=\sigma_\varepsilon(x_1)\,Z$. *→ Leer el error* |
| $R^2$ | $1-\mathrm{MSE}/\operatorname{Var}(y)$. **No es el riesgo al cuadrado**; se prefiere decir «mejora sobre el benchmark». *→ Leer el error* |
| $\mu$ | La fuerza de regularización: el multiplicador, con $\mu\ge0$. *→ El lagrangeano en acción* |
| $\Omega_1$, $\Omega_2$, $\Omega_\rho$ | Las capacidades de lasso, ridge y red elástica, sobre las pendientes $\beta_j$, $j\ge1$. *→ El lagrangeano en acción* |
| $\rho$ | La mezcla de la red elástica: $\Omega_\rho=\rho\,\Omega_1+(1-\rho)\,\Omega_2$. *→ El lagrangeano en acción* |
| $\lVert\beta\rVert_1$, $\lVert\beta\rVert_2$ | Suma de valores absolutos y raíz de la suma de cuadrados. *→ El lagrangeano en acción* |
| $\widehat\beta_{\text{MC}}$, $b$, $b_j$ | El ajuste de mínimos cuadrados sin penalizar y sus pendientes. *→ El lagrangeano en acción* |
| $\operatorname{sign}(b)$ | El signo de $b$: $+1$, $-1$ o 0. *→ El lagrangeano en acción* |
| $v(d)$ | El mejor $L_{\text{ent}}$ con $\Omega(\beta)\le d$. Su pendiente de apoyo es $-\mu$. *→ El lagrangeano en acción* |
| $I$ | La matriz identidad, en $\frac1n\Phi^{\mathsf T}\Phi=I$. *→ El lagrangeano en acción* |

## Clase 4 · Clasificación

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $y\in\{0,\dots,K-1\}$ | Las etiquetas: binario, $\{0,1\}$. *→ Pérdida, métrica y desbalanceo* |
| $p_{i,y}$, $z_{i,y}$ | Probabilidad y puntaje de la clase $y$ en la observación $i$, con softmax. *→ Pérdida, métrica y desbalanceo* |
| $\beta_{0,y}$, $\beta_y$ | Intercepto y pendientes de la clase $y$. *→ Pérdida, métrica y desbalanceo* |
| $\widehat p$ | Una probabilidad anunciada por un modelo ajustado. *→ Pérdida, métrica y desbalanceo* |
| $\tau$ | El umbral: se predice $y=1$ si $\widehat p\ge\tau$. *→ Pérdida, métrica y desbalanceo* |
| $w_y$, $n_y$ | El peso de la clase $y$ y su número de casos en entrenamiento. *→ Pérdida, métrica y desbalanceo* |
| $L^w_{\text{ent}}$ | La pérdida ponderada de entrenamiento. Solo es objetivo de ajuste: nunca se reporta. *→ Pérdida, métrica y desbalanceo* |
| $\eta(x)$, $p^{w}(x)$ | La probabilidad verdadera $\Pr(y=1\mid x)$ y la que anuncia el modelo ponderado en población. *→ Pérdida, métrica y desbalanceo* |
| $\mathrm{MCC}$, $A_{\text{bal}}$ | Coeficiente de correlación de Matthews y aciertos balanceados. Son métricas: mayor es mejor. *→ Pérdida, métrica y desbalanceo* |
| $\mathrm{VP}$, $\mathrm{FP}$, $\mathrm{FN}$ | Verdaderos positivos, falsos positivos y falsos negativos. *→ Pérdida, métrica y desbalanceo* |
| $\mathbf 1\{\cdot\}$ | Indicadora: vale 1 si se cumple lo de adentro y 0 si no. *→ Pérdida, métrica y desbalanceo* |
| $\mathrm{Brier}$ | El promedio de $(y-\widehat p)^2$: una pérdida de calibración. *→ Calibración y predicción conformal* |
| $c_i$, $\widehat c$ | El puntaje de no conformidad del caso $i$ y su cuantil corregido. *→ Calibración y predicción conformal* |
| $C(x)$ | El conjunto de predicción: las clases con puntaje $\le\widehat c$. *→ Calibración y predicción conformal* |
| $n_{\text{cal}}$ | El tamaño del conjunto de calibración. *→ Calibración y predicción conformal* |
| $1-\delta$, $\delta$ | La cobertura prometida y la probabilidad de fallar. *→ Calibración y predicción conformal* |

## Clase 5 · Supuestos y metodología

| Símbolo | Qué es y dónde se presenta |
|---|---|
| $\mathcal S_i$, $\bigcap$ | Conjuntos de valores posibles de una fila, y la intersección de eventos en la definición de iid. *→ ¿Son iid? Fugas* |
| $t$, $e_t$ | El tiempo, como el paso $t$ de Markov, y el residual en ese paso. *→ ¿Son iid? Fugas* |
| $\mathrm{KS}_j$, $\widehat F$ | El estadístico de Kolmogorov–Smirnov de la variable $j$ y la distribución acumulada empírica. *→ ¿Son iid? Fugas* |
| $\bar o$ | La proporción de filas con origen 1 en la validación adversarial. *→ ¿Son iid? Fugas* |
| $\widehat{\operatorname{med}}_j$ | La mediana de los valores observados de la variable $j$, para imputar. *→ ¿Son iid? Fugas* |
| $\mathbf Q$ | Una matriz invertible: reescalar columnas es cambiar $\Phi$ por $\Phi\mathbf Q$. *→ ¿Son iid? Fugas* |
| $\mathcal R_h$, $H$ | Las hojas de un árbol y su número; $[\phi(x)]_h=\mathbf 1\{x\in\mathcal R_h\}$, sin columna de unos. *→ La metodología* |
| $B$, $\widehat f^{(b)}$ | El número de árboles de un bosque y cada uno de ellos. *→ La metodología* |
| $\nu$ | La tasa de boosting, $\nu\in(0,1]$. *→ La metodología* |
| $\gamma_h$, $\gamma_{0,h}$ | Pesos y constante de la unidad $h$ de una red de una capa. Cuando la página cuenta unidades, dice «unidades», no $q$. *→ La metodología* |

## En el código

Los notebooks y `ml_lab` usan los nombres de las páginas. La hoja
[[ml-laboratorio|El laboratorio ml_lab]] lista cada función.

| Nombre | Es |
|---|---|
| `beta_gorro`, `f_gorro`, `y_gorro` | $\widehat\beta$, $\widehat f$, $\widehat y$ |
| `L_ent`, `L_val`, `L_prueba` | $L_{\text{ent}}$, $L_{\text{val}}$, $L_{\text{prueba}}$ |
| `R`, `R_bayes` | $R$ contra la muestra de despliegue y el piso $R_{\text{Bayes}}$; la función que lo calcula es `piso` |
| `mu`, `rho`, `tau`, `delta` | $\mu$, $\rho$, $\tau$, $\delta$ |
| `N`, `N_max`, `k`, `m`, `M`, `J` | $N$, $N_{\max}$, $k$, $m$, $M$, $J$ |
| `w` | El diccionario `{y: w_y}` de pesos de clase |
| `sigma_e`, `sigma2_e`, `s_l` | $\sigma_\varepsilon$, $\sigma_\varepsilon^2$, $s_\ell$ |
| `Phi`, `phi` | $\Phi$ y $\phi$ |
| `t_student`, `veces` | La $t$ de Student y el factor de un intervalo: no chocan con $t$ ni con el puntaje $z$ |

Cuando scikit-learn usa otro nombre para $\mu$, la conversión vive dentro de
`ml_lab`, con un comentario. Los notebooks no la repiten.

## Avisos de letras

Algunas letras ya significaban otra cosa en unidades anteriores. Cada
renglón dice dónde y qué son aquí.

| Letra | Antes | Aquí |
|---|---|---|
| $\varepsilon$ | Computabilidad: la cadena vacía. Markov: una cantidad positiva. Juegos: un margen. | El ruido. |
| $\mu$ | Markov: una distribución sobre estados. | El multiplicador de la unidad 6, $\mu\ge0$. |
| $\Omega$ | Complejidad: la cota inferior asintótica. | La medida de capacidad. |
| $L$ | Computabilidad: un lenguaje. Complejidad: espacio logarítmico. Markov: la longitud de una racha. | La pérdida promedio de la unidad 6. |
| $k$ | Markov: el número de estados. Juegos: de simulaciones. Unidad 6: el índice de clase. | El número de pliegues. |
| $\beta_0$, $\beta_{0,y}$ | En la logística de la unidad 6, el intercepto se llamaba alfa, con subíndice $k$. | El intercepto. La letra alfa no se usa en esta unidad. |
| $y$ como índice | Unidad 6: clases de 1 a $K$, índice $k$ y suma sobre $j$. | Clases de 0 a $K-1$, índice $y$ y suma sobre $y'$. |
| $M$ | Juegos: la escala de los finales. Computabilidad: una máquina de Turing. | El número de candidatos, como en la unidad 6. No es $m$. |
| $m$ | Complejidad: el número de aristas. Juegos: la profundidad máxima. Markov: el tiempo medio de llegada. | El índice de pliegue. |
| $\tau$ | Juegos: un tablero. Markov: $\tau_A$, un tiempo de llegada. | El umbral. |
| $\delta$ | Computabilidad: la función de transición. Markov: el error al recuperar una matriz. | La probabilidad de fallar. |
| $r$ | Markov: la recompensa $r(s,a)$. | El radio polar. |
| $q$ | Markov: la probabilidad de seguir en consonante. | Las columnas de $\Phi$, todas. |
| $c$, $C$ | Complejidad: una constante o un certificado. Markov: las caras del dado. Juegos: las casillas. | El puntaje conformal y el conjunto de predicción. |
| $w$ | Juegos: lo que devuelve un hijo. Computabilidad: una cadena. | El peso de clase $w_y$. |
| $\beta$ | Juegos: el umbral de MIN. | Los parámetros, como en la unidad 6. |
| lambda | Markov: un factor de convergencia. En el curso, el multiplicador de igualdad. | No aparece. La regularización usa $\mu$; los libros la escriben con lambda. |
| $\mathcal H$ | Unidad 6: los bloques de una hora en Salones. | El conjunto de polinomios de grado $\le N$, $\mathcal H_N$. |
| $x_0$ | Unidad 6: el punto inicial del descenso. Markov: el primer término. | El centro de Taylor. |
| $\gamma$ | Markov: el descuento. | Los pesos de una unidad sigmoide. |

Tres avisos más valen en toda la unidad:

- **Subíndices de $x$.** $x_i$, con la letra $i$, es la observación $i$;
  $x_1, x_2, \dots$, con número, son variables (columnas); $x_{ij}$ es la
  variable $j$ de la observación $i$.
- **Subíndice numérico de $\phi$.** $\phi_N$ es solo el polinomio de grado
  $N$: $\phi_1(x)=(1,x)$, $\phi_2(x)=(1,x,x^2)$. Las capas de una red se
  dicen «capa 1 → capa 2», nunca $\phi_1, \phi_2$.
- **$R^2$ no es $R$ al cuadrado.** Es otra cifra, y se usa poco.

## En las figuras

Todas las figuras y gráficas de la unidad usan una sola leyenda. El color
nunca es la única señal: cada rol tiene además su marca o su trazo.

| Rol | Marca | Color en el sitio |
|---|---|---|
| entrenamiento | círculo ● | cian |
| validación o CV | triángulo ▲ | oro |
| prueba | cuadrado ■ | rosa |
| realidad, riesgo $R$ | línea discontinua – – | crema |
| $f$ verdadera | línea continua gruesa | verde |
| $\widehat f$ | línea continua delgada | cian |
| piso $R_{\text{Bayes}}$ | línea punteada ··· | lila |
| observaciones nuevas | punto pequeño · | crema tenue |
| benchmark | raya y punto –·– | magenta |

Las observaciones nuevas son casos que el ajuste no vio, antes de que
exista la prueba. En los notebooks, el tema claro conserva las marcas y
cambia los colores.
