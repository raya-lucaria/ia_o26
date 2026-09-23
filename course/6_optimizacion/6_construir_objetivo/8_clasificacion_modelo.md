---
id: opt-objetivo-clasificacion-modelo
title: Elegir qué significa ajustar un clasificador
nav_title: Clasificación · Modelo general
summary: "Separar parámetros, probabilidades y etiquetas, y justificar una función sustituta sin confundirla con la medida final."
status: ready
tags: [optimizacion, modelado, clasificacion]
---

# Elegir qué significa ajustar un clasificador

**Primero intenta los [[opt-objetivo-clasificacion-practica|dos problemas de clasificación]].**
La familia de reglas y las decisiones pueden permanecer iguales mientras
cambia qué entendemos por un buen ajuste.

## 1 · Separar datos, decisiones y expresiones

Generalizamos a varios atributos por ejemplo. Todas las entradas están en
escalas numéricas sin unidades físicas, como en la práctica.

| Símbolo | Significado | Papel |
|---|---|---|
| $I,J$ | Conjuntos finitos no vacíos de ejemplos y atributos | Datos |
| $n=|I|$ | Número de ejemplos | Dato |
| $x_{ij}$ | Atributo $j$ del ejemplo $i$ | Dato real |
| $y_i$ | Etiqueta correcta del ejemplo $i$ | Dato en $\{0,1\}$ |
| $M>0$ | Límite de magnitud de cada parámetro | Dato |
| $w_j,b$ | Pesos y constante compartidos | Decisiones reales |

La familia elegida produce

$$p_i(w,b)=\sigma\left(\sum_{j\in J}w_jx_{ij}+b\right),
\qquad \sigma(z)=\frac{1}{1+e^{-z}}.$$

$p_i$ representa la probabilidad asignada a la clase 1. La probabilidad
de la clase 0 es $1-p_i$. Ambas son expresiones de las decisiones; elegirlas
libremente para cada ejemplo cambiaría el problema.

Con umbral 0.5 y empate favorable a clase 1, definimos
$\widehat y_i=\mathbf1\{p_i\ge0.5\}$. El símbolo $\mathbf1\{P\}$ vale 1
cuando $P$ es verdadera y 0 en caso contrario. El conjunto permitido es

$$\Theta=\{(w,b):w_j\in\mathbb R,\ -M\le w_j\le M\ (j\in J),
\ b\in\mathbb R,\ -M\le b\le M\}.$$

Las cotas son parte de este relato. No son una propiedad obligatoria de
todos los clasificadores.

## 2 · Contar aciertos

Cada ejemplo aporta un 1 si la etiqueta anunciada coincide con su referencia.
El promedio es accuracy:

$$\begin{aligned}
\max_{w,b}\quad &\frac1n\sum_{i\in I}
\mathbf1\{\widehat y_i(w,b)=y_i\}\\
\text{sujeto a}\quad &(w,b)\in\Theta.
\end{aligned}$$

Es una proporción sin unidades. Todos los ejemplos pesan igual: acertar uno
compensa fallar otro en la misma cantidad. No registra si un acierto tenía
probabilidad 0.51 o 0.99 para su clase correcta.

Su evaluación es directa. Como función de los parámetros es constante por
regiones: pequeñas modificaciones que conservan todas las etiquetas dejan
igual el objetivo. Esa propiedad limita la información que ofrece para
orientar un ajuste por gradientes; no significa que contar aciertos sea
difícil. Aquí formulamos el problema, sin elegir un algoritmo.

## 3 · Conservar información probabilística

Si la probabilidad de la clase correcta es $r_i$, su pérdida es $-\ln r_i$.
Según la etiqueta, $r_i$ será $p_i$ o $1-p_i$. Al sustituir ambas posibilidades:

$$\ell_i(w,b)=-y_i\ln p_i(w,b)-(1-y_i)\ln(1-p_i(w,b)).$$

El modelo completo alternativo conserva exactamente el conjunto permitido:

$$\begin{aligned}
\min_{w,b}\quad &\frac1n\sum_{i\in I}\ell_i(w,b)\\
\text{sujeto a}\quad &(w,b)\in\Theta.
\end{aligned}$$

La sigmoide mantiene $0<p_i<1$ para parámetros finitos. La función asigna
mayor penalización a una probabilidad correcta menor; el promedio se expresa
en nats por ejemplo cuando usamos logaritmos naturales. Es una medida
probabilística, no una cuenta de errores. La definición corresponde a la
[pérdida logarítmica binaria documentada por scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html).

En esta familia, la función es suave en los parámetros: conserva cambios
que el umbral oculta. Si lo que finalmente importa es accuracy, emplearla
como **función sustituta** cambia el criterio del ajuste. Si también importa
la calidad de las probabilidades, log loss puede ser una medida de interés
por derecho propio. En ninguno de esos casos se vuelve idéntica a accuracy.

## 4 · Sustituir los datos y comprobar una afirmación

La práctica toma un atributo, $w_1=a$, $M=4$, entradas 0, 1 y 2, y etiquetas
0, 1 y 1. Por tanto,

$$\begin{aligned}
A(a,b)&=\frac{\mathbf1\{\sigma(b)<0.5\}
+\mathbf1\{\sigma(a+b)\ge0.5\}
+\mathbf1\{\sigma(2a+b)\ge0.5\}}3,\\
L(a,b)&=\frac{-\ln(1-\sigma(b))-\ln\sigma(a+b)-\ln\sigma(2a+b)}3.
\end{aligned}$$

Los dos problemas son maximizar $A(a,b)$ o minimizar $L(a,b)$, sujetos a
$a,b\in[-4,4]$. Para $a=0$, las probabilidades son constantes.

| Parámetros permitidos | Accuracy | Log loss |
|---|---:|---:|
| $a=0$, $b=\ln9\approx2.197$ | 2/3 | 0.838 |
| $a=0$, $b=\ln(0.49/0.51)\approx-0.040$ | 1/3 | 0.700 |

Este contraejemplo basta para rechazar que bajar una pérdida garantice
subir accuracy en cada comparación. No identifica los parámetros óptimos
ni demuestra que los óptimos de ambos objetivos sean distintos aquí.

## 5 · Revisar lo que todavía falta

La igualdad de peso entre ejemplos es un supuesto en ambos modelos. Si un
error sobre la clase 1 cuesta más, harían falta datos sobre esos costos y
una decisión explícita sobre cómo incorporarlos. Si solo tenemos estos
tres ejemplos, tampoco podemos afirmar que cualquiera de las medidas
describa el desempeño futuro: ese juicio necesita otros datos.

**El objetivo sustituto requiere una justificación y una comprobación
frente al propósito original.** Anota qué información aprovecha, qué deja
fuera y cuál será la medida con la que evaluarás la decisión obtenida.

[[opt-objetivo-clasificacion-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
