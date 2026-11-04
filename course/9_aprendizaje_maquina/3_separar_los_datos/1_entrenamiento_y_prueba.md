---
id: ml-entrenamiento-y-prueba
title: "Entrenamiento y prueba: la prueba imita la realidad"
nav_title: "Entrenamiento y prueba"
summary: "Por qué el error de entrenamiento no sirve para elegir, cómo una prueba que no tocó ninguna decisión estima el riesgo con su error estándar, por qué elegir con la prueba engaña y cómo construir una prueba que se parezca al uso real."
status: ready
estimated_time: 75m
tags: [aprendizaje-maquina, separacion, entrenamiento, validacion, prueba, error-de-generalizacion]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 03 · Entrenamiento y prueba.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)
>
> **[👉 Abrir `03_entrenamiento_y_prueba.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)**

# Entrenamiento y prueba: la prueba imita la realidad

En la clase 1 quedaron dos anuncios: elegir el grado con validación y validación cruzada (*cross-validation*), y medir el riesgo sin una muestra enorme. Aquí empiezas por separar las entregas según la decisión que tocarán.

**¿Con qué datos puedes medir el error de un modelo que vas a usar mañana?**

~35 min de lectura y ~40 con el notebook 03.

Al terminar tendrás:

- **Una razón:** por qué el entrenamiento no sirve para elegir ni reportar, con una desigualdad.
- **Un cálculo:** el error estándar de una prueba, a mano.
- **Una medida del engaño:** cuánto optimismo introduce elegir con la prueba, en 300 repeticiones.
- **Tres conjuntos:** qué decisión toca cada uno.
- **Una separación justificada:** los datos apartados imitan cómo usarás el modelo.

> **Lo que traes**
>
> De [[ml-que-es-f|¿Qué es f?]]: el riesgo $R$ (@ml-c1-def-riesgo) y la pérdida $L_{\mathcal D}$ (@ml-c1-def-perdida-en-conjunto).
>
> De [[ml-polinomios-y-capacidad|Polinomios y capacidad]]: la brecha (@ml-c1-def-brecha) y parámetro contra hiperparámetro (@ml-c1-def-param-hiper).
>
> De [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]]: las entregas y por qué el error en los mismos datos premia el grado mayor.

## 1 · Separar dos decisiones

::: figure {#ml-c2-dos-niveles title="Dos decisiones, dos conjuntos"}
![Dos cajas anidadas. La de afuera elige el grado N comparando los candidatos con la pérdida de validación, y su flecha va al conjunto de validación, que solo mide. La de adentro elige beta con N fijo minimizando la pérdida de entrenamiento con grado a lo más N, y su flecha va al conjunto de entrenamiento, que ajusta; devuelve un beta gorro por candidato. Al pie: si afuera se mirara el entrenamiento, ganaría siempre la caja más grande.](../_assets/ml-c2-dos-niveles.svg)
:::

Hay dos optimizaciones, una dentro de otra. Mira qué datos usa cada caja: adentro ajustas coeficientes; afuera comparas grados. Si ambas usaran entrenamiento, la caja más grande nunca perdería.

**Piensa: Si dejas que el error de entrenamiento elija el grado entre 0 y 12, ¿qué grado sale, y por qué no puede salir otro?**

En este hilo sale 12: $L_{\text{ent}}$ baja de 51.2 a 7.7 y a 4.5 con grados 0, 3 y 12. La razón general admite empates. Cada familia contiene a las anteriores, así que el mínimo no sube; $N_{\max}$ nunca pierde, aunque otro grado pueda empatarlo.

@ml-c1-def-param-hiper distingue parámetro e hiperparámetro; aquí decidimos con qué datos elegirlos. Usaremos $\mathcal D_{\text{val}}$, el conjunto de validación, y $L_{\text{val}}$, su pérdida promedio. Como en @ml-c1-def-capacidad-como-restriccion, el grado impone $\Omega(\beta)\le d$ con $d=N$:

$$\widehat N\in\operatorname*{arg\,min}_{N\in\{0,\dots,N_{\max}\}}L_{\text{val}}\bigl(\widehat\beta(N)\bigr),\qquad \widehat\beta(N)\in\operatorname*{arg\,min}_{\beta}\ L_{\text{ent}}(\beta)\ \ \text{s.a.}\ \ \text{grado}\le N.$$

El $\arg\min$ es un conjunto. Si varios grados empatan en validación, eliges el menor; si $\Phi$ no tiene rango completo, eliges los coeficientes de norma mínima. Así quedan definidos $\widehat N$ y $\widehat\beta(N)$.

Primero ajustas un candidato por grado; después comparas sus pérdidas en otras entregas. El grado 12 sigue siendo lineal en $\beta$ (@ml-c1-def-modelo-lineal): tiene más columnas en $\Phi$.

La tabla separa las perillas del modelo de las decisiones sobre cómo medirlo. $\mathrm{CV}_k$ anuncia la validación cruzada con $k$ pliegues. Esta $k$ cuenta pliegues: en Markov contaba estados; en juegos, simulaciones; en la unidad 6, clases mediante un índice.

::: table {#ml-c2-tab-param-hiper title="Qué es parámetro, qué es hiperparámetro y qué es del procedimiento"}
| Perilla | Qué fija | Con qué se elige | Se presenta |
|---|---|---|---|
| coeficientes $\beta$ | la función dentro de la familia | minimizar $L_{\text{ent}}$ (es **parámetro**) | clase 1 |
| grado $N$ | la familia: cuántas columnas tiene $\Phi$ | $L_{\text{val}}$ o $\mathrm{CV}_k$ | clase 1 |
| fuerza de regularización $\mu$ | la capacidad, de forma continua | $L_{\text{val}}$ o $\mathrm{CV}_k$ | clase 3 |
| mezcla $\rho$ de la red elástica | la forma de la penalización | $L_{\text{val}}$ o $\mathrm{CV}_k$ | clase 3 |
| umbral $\tau$ | cuándo una probabilidad se vuelve «sí» | validación, con la métrica elegida | clase 4 |
| pesos de clase $w_y$ | cuánto pesa cada clase en la pérdida | validación, con una métrica sin pesos | clase 4 |
| número de vecinos; profundidad de un árbol | la capacidad de esas familias | $L_{\text{val}}$ o $\mathrm{CV}_k$ | clase 1 (vecinos), clase 5 (árboles) |
| número de pliegues $k$, semilla, fracciones, $n_{\text{prueba}}$ | **cómo se mide**, no el modelo | se fijan antes de medir; no se eligen con datos | clase 2 |

Aquí $\mu$ conserva el sentido de multiplicador de la unidad 6; en Markov nombraba una distribución. $\tau$ será un umbral; en juegos era un tablero y en Markov, un tiempo de llegada. $w_y$ será un peso de clase; no es el valor de un hijo en juegos ni una cadena en computabilidad.
:::

Las perillas de capacidad se irían al extremo si las eligiera $L_{\text{ent}}$. El umbral y los pesos de clase no entran del mismo modo en ese problema (@ml-c1-def-param-hiper).


> [!WARNING]
> Lectura equivocada: «Yo no entrené con la prueba; solo elegí el grado con ella».
>
> Lectura correcta: **Elegir también es ajustar: el grado elegido ya «vio» la prueba, y su error deja de ser una estimación honesta.**

::: exercise {#ml-c2-ej-clasifica-perillas title="Clasifica las perillas"}
Clasifica como parámetro, hiperparámetro o del procedimiento:

- (a) El coeficiente de $x^3$ en un polinomio de grado 5.
- (b) El grado 5.
- (c) La semilla con que se partieron los datos.
- (d) $n_{\text{prueba}}=200$, el tamaño de la prueba.
- (e) El coeficiente de $1/x$ en $\phi(x)=(1,1/x)$.
:::

::: hint {#ml-c2-pista-clasifica-perillas-1 of="ml-c2-ej-clasifica-perillas" title="Pista 1 · ¿Qué cambia durante el ajuste?"}
¿Cuáles cambian si minimizas $L_{\text{ent}}$ con todo lo demás fijo?
:::

::: answer {#ml-c2-resp-clasifica-perillas of="ml-c2-ej-clasifica-perillas" title="Respuesta · Ubicar cada decisión"}
(a) y (e) son parámetros: el ajuste elige esos coeficientes dentro de una familia fija. (b) es hiperparámetro: delimita la familia. (c) y (d) son del procedimiento: fijan cómo separas y mides, sin cambiar la regla de predicción.
:::

> [!TIP]
> **Míralo correr: bloque 1 · Separar dos decisiones**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

## 2 · Apartar una prueba

::: figure {#ml-c2-ajustes-con-prueba title="Grados 1, 4 y 12 con entrenamiento y prueba"}
![Tres paneles con las mismas 60 entregas: círculos de entrenamiento y cuadrados de prueba, la f verdadera y el ajuste. Grado 1: L_ent 18.5, L_prueba 15.3. Grado 4: L_ent 7.1, L_prueba 13.3. Grado 12: L_ent 4.5, el más bajo, pero la curva pasa cerca de los círculos y se dispara en los bordes, y su L_prueba es enorme, 15919.](../_assets/ml-c2-ajustes-con-prueba.svg)
:::

Cada círculo es una entrega usada para ajustar; cada cuadrado, una que el ajuste no vio. Los ejes muestran distancia y tiempo. La curva delgada es $\widehat f$; la gruesa verde, $f$. El grado 12 pasa cerca de los círculos y falla lejos de ellos.

**Piensa: ¿Por qué un conjunto que el ajuste no vio da una cifra honesta, y qué tendría que pasar para que dejara de darla?**

Porque el modelo no pudo acomodarse a sus pérdidas, siempre que las entregas sean independientes del desarrollo y representen el despliegue. Apartar filas por sí solo no asegura eso.

El entrenamiento miente a tu favor, en promedio, al elegir coeficientes con esos datos (@ml-c1-teo-optimismo-entrenamiento). El mismo argumento para elegir con la prueba llegará en @ml-c2-obs-optimismo-seleccion.

En los grados 1 y 4, entrenamiento da 18.5 y 7.1; prueba da 15.3 y 13.3. Sus riesgos son 14.8 y 11.8. En grado 12, entrenamiento da 4.5, pero prueba y riesgo superan mil. Aquí mostramos el contraste; estas curvas no son una regla para elegir con la prueba.

::: theorem {#ml-c2-teo-prueba-insesgada title="La prueba estima el riesgo si no tocó nada y se parece al despliegue"}
Supón que:

1. La prueba no tocó **ninguna** decisión: ni ajuste, ni elección de hiperparámetros, ni preprocesamiento.
2. Sus observaciones salen del **mismo proceso que el despliegue** y son independientes de entrenamiento y validación. No comparten pacientes, clientes ni momentos con ellas; así, $\widehat\beta$ es independiente de la prueba.

Sea $\ell=\ell\bigl(y,f_{\widehat\beta}(x)\bigr)$ la pérdida en una observación nueva del despliegue, con $E[\ell]$ finita. Entonces

$$E\bigl[L_{\text{prueba}}(\widehat\beta)\mid\widehat\beta\bigr]=R(\widehat\beta).$$

Aquí $L_{\text{prueba}}$ es la pérdida promedio en $\mathcal D_{\text{prueba}}$, el conjunto de prueba. La igualdad dice que, congelado el modelo, promediar pruebas nuevas recupera su riesgo.

Para el error estándar ($\mathrm{EE}$), además:

3. Las $n_{\text{prueba}}$ observaciones de prueba son independientes **entre sí** y $E[\ell^2]$ es finita.

Entonces

$$\operatorname{Var}\bigl(L_{\text{prueba}}(\widehat\beta)\mid\widehat\beta\bigr)=\frac{\operatorname{Var}(\ell\mid\widehat\beta)}{n_{\text{prueba}}},\qquad \mathrm{EE}\approx\frac{s_\ell}{\sqrt{n_{\text{prueba}}}},\qquad s_\ell^2=\frac{1}{n_{\text{prueba}}-1}\sum_{i\in\mathcal D_{\text{prueba}}}\bigl(\ell_i-L_{\text{prueba}}\bigr)^2.$$

$s_\ell$ es la desviación estándar muestral de las pérdidas. Dividirla entre la raíz del tamaño estima cuánto fluctúa su promedio. Con pérdidas $1,1,4,4$, el promedio es 2.5 y su EE es aproximadamente 0.87.
:::

::: proof {#ml-c2-dem-prueba-insesgada of="ml-c2-teo-prueba-insesgada"}
1. Por (1) y la independencia respecto del desarrollo en (2), condicionar en $\widehat\beta$ deja fijo el modelo. La distribución de cada observación de prueba no cambia. No abrirla sería insuficiente si compartiera pacientes con entrenamiento.
2. Por (2), cada pérdida tiene la distribución de $\ell$ dado $\widehat\beta$. Su esperanza es $R(\widehat\beta)$, por @ml-c1-def-riesgo.


3. La esperanza del promedio es el promedio de esperanzas. Para esta igualdad no hace falta independencia entre las pérdidas.
4. Con (3), la varianza del promedio es la varianza individual entre $n_{\text{prueba}}$. La desviación muestral $s_\ell$ estima la desviación de las pérdidas. Sin (3), aparecen covarianzas entre pares; su signo decide hacia dónde cambia la incertidumbre.
5. Si falla (1), el modelo depende de la prueba y el primer paso deja de valer. Eso ocurrirá al elegir el grado con ella.
:::

**Otra población:** con observaciones independientes, la prueba sigue siendo insesgada para el riesgo de esa población, no para el del despliegue.

**Dependencia:** compartir clientes, pacientes o momentos con entrenamiento puede desplazar la media. Dentro de la prueba, $s_\ell/\sqrt{n_{\text{prueba}}}$ puede subestimar o sobreestimar el EE. Con correlación positiva dentro del grupo, lo subestima. La clase 5 trabaja estos casos.

El intervalo $L_{\text{prueba}}\pm2\,\mathrm{EE}$ es aproximado: usa una aproximación normal del promedio, no una garantía.

> [!WARNING]
> Lectura equivocada: «El EE dice cuánto me voy a equivocar en una entrega».
>
> Lectura correcta: **El EE mide cuánto puede moverse la estimación del riesgo, no el error de una entrega individual.**

::: exercise {#ml-c2-ej-ee-a-mano title="Calcula el error estándar a mano"}
Un modelo fijo deja en cuatro entregas de prueba los residuales $1,-1,2,-2$ minutos. Calcula $L_{\text{prueba}}$ con pérdida cuadrática y su $\mathrm{EE}$.
:::

::: hint {#ml-c2-pista-ee-a-mano-1 of="ml-c2-ej-ee-a-mano" title="Pista 1 · ¿Qué valores promedias?"}
¿Qué promedia la pérdida cuadrática: los residuales o sus cuadrados?
:::

::: answer {#ml-c2-resp-ee-a-mano of="ml-c2-ej-ee-a-mano" title="Respuesta · Promediar las pérdidas"}
Las pérdidas son $\ell_i=1,1,4,4$, así que $L_{\text{prueba}}=2.5$. Las cuatro distan 1.5 del promedio:

$$s_\ell^2=\frac{(1.5^2)\cdot4}{3}=3,\qquad s_\ell=\sqrt3\approx1.73,\qquad \mathrm{EE}=\frac{\sqrt3}{2}\approx0.87.$$

La cuenta usa $1,1,4,4$, no los residuales con signo. Tanto la pérdida promedio como su EE están en minutos cuadrados.
:::

> [!TIP]
> **Míralo correr: bloque 2 · Apartar una prueba y medir cuánto baila**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

## 3 · Medir cuánto baila una prueba

::: figure {#ml-c2-prueba-ruidosa title="Una prueba honesta también baila"}
![Dos histogramas de L_prueba del mismo modelo de grado 4, congelado, con 500 pruebas nuevas cada uno. Con 20 entregas por prueba la nube es ancha, desviación 3.8, y el intervalo de ±2 EE cubre R en 89 % de las pruebas; con 200, desviación 1.1 y cobertura 94 %. Las dos nubes se centran en R = 11.8.](../_assets/ml-c2-prueba-ruidosa.svg)
:::

Ahora el modelo está congelado: grado 4, ajustado una sola vez. Cada barra cuenta pruebas cuyo promedio cae en ese tramo del eje horizontal. Cada prueba sortea nuevas entregas; la línea crema discontinua marca $R=11.8$.

**Piensa: Si dos pruebas honestas del mismo modelo dan números distintos, ¿cuál de las dos está mal?**

Ninguna tiene que estar mal. Insesgada no significa exacta: no tiene una dirección sistemática de error al repetirla. En 500 pruebas nuevas, la desviación de $L_{\text{prueba}}$ es 3.8 con 20 entregas y 1.1 con 200.

Las dos nubes se centran en el riesgo, pero la primera es más ancha. Los intervalos $\pm2\,\mathrm{EE}$ lo cubren en 89 % y 94 % de las pruebas, respectivamente. La cola de las pérdidas dificulta la aproximación con pocas observaciones.

La raíz del denominador explica el costo de precisar: el ancho baja como $1/\sqrt{n_{\text{prueba}}}$. Cuadruplicar la prueba reduce el EE esperado a la mitad. Solo cambia la evaluación; el modelo no aprende de esas entregas adicionales.

Reporta $L_{\text{prueba}}\pm2\,\mathrm{EE}$ junto al punto de comparación (*benchmark*): la media de entrenamiento como punto de comparación; la clase 3 lo define. Una pérdida aislada no dice si mejoraste sobre esa referencia.

Las pruebas nuevas del bloque 2 salen de `datos.despliegue`, la muestra enorme del despliegue simulado, no de `datos.prueba`. Nada lee la prueba reservada para tomar decisiones. Falta ver qué pasa si rompes esa separación.

::: exercise {#ml-c2-ej-cuadruplicar title="Reduce la incertidumbre"}
Con $n_{\text{prueba}}=100$ obtuviste $\mathrm{EE}=0.8$. ¿Qué EE esperas con 400? ¿Cuántas observaciones necesitas para $\mathrm{EE}\approx0.2$?
:::

::: hint {#ml-c2-pista-cuadruplicar-1 of="ml-c2-ej-cuadruplicar" title="Pista 1 · ¿Cómo cambia la raíz?"}
¿Cómo cambia $1/\sqrt n$ si $n$ se multiplica por cuatro?
:::

::: answer {#ml-c2-resp-cuadruplicar of="ml-c2-ej-cuadruplicar" title="Respuesta · Pagar por precisión"}
Con 400 observaciones esperas $\mathrm{EE}=0.4$. Para llegar a 0.2 necesitas 1600. Cada reducción a la mitad exige cuadruplicar el tamaño, suponiendo la misma dispersión de pérdidas y observaciones independientes.
:::

## 4 · Ver el engaño de elegir con la prueba

::: figure {#ml-c2-optimismo title="El engaño de elegir con la prueba"}
![Dos histogramas con 300 repeticiones del hilo: lo anunciado menos el riesgo real del grado elegido, sin reajuste. Arriba, eligiendo con la prueba: la nube se corre a la izquierda de 0, la media es −7.5 y 74 % de las repeticiones anuncian menos error del real. Abajo, eligiendo con validación y anunciando en prueba: la mediana queda en −0.6 y 56 % anuncian de menos. Los valores fuera de -30 a 20 se apilan en los bordes.](../_assets/ml-c2-optimismo.svg)
:::

Cada barra cuenta repeticiones: nuevos datos, elección de grado y comparación de lo anunciado con el riesgo real. El eje horizontal muestra $L_{\text{prueba}}-R$; debajo de cero, anuncias menos error del que tendrás. Ambos paneles son sin reajuste: conservan el mismo entrenamiento; solo cambia quién elige el grado.

**Piensa: Si pruebas trece grados en la misma prueba y anuncias el mejor, ¿por qué tu anuncio sale casi siempre optimista aunque cada cifra, por separado, sea honesta?**

Es como elegir el termómetro que hoy marca menos: eliges también su error de medición favorable. Arriba, eligiendo con la prueba, 74 % de los anuncios son optimistas. La media de anunciado menos real es $-7.5\pm1.8$, donde el margen es un EE de Monte Carlo: incertidumbre del promedio entre repeticiones.

::: remark {#ml-c2-obs-optimismo-seleccion title="El mínimo de estimaciones honestas sale optimista"}
Condiciona en $\mathcal D_{\text{ent}}$: los candidatos $\widehat\beta(N)$ quedan fijos. Por @ml-c2-teo-prueba-insesgada, cada pérdida de prueba es insesgada para el riesgo de su candidato. El mínimo nunca supera a ninguno; su esperanza tampoco supera la menor esperanza:

$$E\Bigl[\min_{N}L_{\text{prueba}}\bigl(\widehat\beta(N)\bigr)\Bigm|\mathcal D_{\text{ent}}\Bigr]\le\min_{N}R\bigl(\widehat\beta(N)\bigr)\le R\bigl(\widehat\beta(\widehat N)\bigr),$$

con $\widehat N\in\operatorname*{arg\,min}_N L_{\text{prueba}}(\widehat\beta(N))$; si empatan, eliges el menor. La segunda desigualdad vale para cualquier candidato elegido. Al promediar también ese riesgo aleatorio, lo reportado queda, en promedio, no por encima del riesgo del elegido.

La desigualdad es no estricta y no requiere independencia entre estimaciones. El argumento también vale con $\mathcal D_{\text{val}}$ en lugar de la prueba.
:::

Elegir con la prueba causa una mala estimación del error de generalización, pero vamos por buen camino: falta otro conjunto.

::: figure {#ml-c2-tres-conjuntos title="Tres conjuntos, tres decisiones"}
![Una barra con la muestra partida en tres: entrenamiento, 60 por ciento, con círculo, ajusta beta gorro de N para cada candidato; validación, 20 por ciento, con triángulo, elige N gorro; prueba, 20 por ciento, con cuadrado y candado, se abre una vez, al final. Una llave junta entrenamiento y validación en la casilla del modelo final: el elegido, reajustado con entrenamiento unión validación; una flecha lleva el modelo final a la prueba, que estima su riesgo R.](../_assets/ml-c2-tres-conjuntos.svg)
:::

::: definition {#ml-c2-def-tres-conjuntos title="Tres conjuntos, tres decisiones"}
La muestra se parte en tres conjuntos disjuntos, con tamaños $n_{\text{ent}}$, $n_{\text{val}}$ y $n_{\text{prueba}}$:

- $\mathcal D_{\text{ent}}$ ajusta los parámetros: $\widehat\beta(N)$.
- $\mathcal D_{\text{val}}$ elige los hiperparámetros: $\widehat N$.
- $\mathcal D_{\text{prueba}}$ se abre una vez, al final, para estimar $R$ del modelo final. Este se reajusta con $\mathcal D_{\text{ent}}\cup\mathcal D_{\text{val}}$, conservando el grado elegido.

En todos calculas la pérdida promedio de @ml-c1-def-perdida-en-conjunto:

$$L_{\text{val}}(\beta)=L_{\mathcal D_{\text{val}}}(\beta),\qquad L_{\text{prueba}}(\beta)=L_{\mathcal D_{\text{prueba}}}(\beta).$$

Cambia la decisión que tocó cada conjunto, no la fórmula.
:::

En el hilo repartimos 60 entregas en 36/12/12. «El elegido», $\widehat\beta(\widehat N)$, solo vio entrenamiento al ajustar coeficientes: es el de los histogramas. «El modelo final» los reajusta con entrenamiento y validación. Goodfellow, Bengio y Courville usan un reajuste semejante tras detener el entrenamiento en su algoritmo 7.2; es un antecedente.

La prueba intacta es insesgada para cualquiera de los dos modelos elegidos sin ella. El final suele aprovechar mejor los datos, pero su riesgo es otro.

Para el elegido por validación, @ml-c2-obs-optimismo-seleccion y @ml-c2-teo-prueba-insesgada demuestran:

$$E\bigl[L_{\text{val}}\bigl(\widehat\beta(\widehat N)\bigr)\bigr]\le E\bigl[R\bigl(\widehat\beta(\widehat N)\bigr)\bigr]=E\bigl[L_{\text{prueba}}\bigl(\widehat\beta(\widehat N)\bigr)\bigr].$$

En este experimento, sin reajuste, las medias de entrenamiento, validación y prueba son 8.5, 9.1 y 12.6. Las diferencias son $0.64\pm0.28$ y $3.53\pm0.56$, cada una con su EE de Monte Carlo. Ambas superan dos EE. Ese orden observado no es un teorema; tampoco se afirma para el modelo final.

Abajo, con validación, la mediana de anunciado menos real es −0.6 y 56 % de los anuncios son optimistas. La media es $-42.0\pm37.2$: está a menos de dos EE de cero. Pocos grados altos que explotan en los bordes arrastran la media; escribir solo «aproximadamente cero» ocultaría esa incertidumbre.

::: remark {#ml-c2-obs-prueba-se-gasta title="La prueba también se gasta despacio"}
Volver a abrir la misma prueba tras cada cambio es elegir con ella, una decisión a la vez. También ocurre en una comunidad: reutilizar durante años una prueba pública favorece cifras optimistas (Goodfellow et al., §5.3).
:::

> [!WARNING]
> Lectura equivocada: «Si el error de prueba del mejor grado salió bajo, el modelo es bueno».
>
> Lectura correcta: **Si elegiste con esa prueba, la cifra está sesgada hacia abajo; repórtala con una prueba que no tocó la elección.**

::: exercise {#ml-c2-ej-termometros title="Compara trece termómetros"}
Trece grados tienen exactamente el mismo riesgo, 10. Para cada uno mides una prueba honesta. ¿El mínimo de las trece cifras tiene esperanza 10, mayor o menor? ¿Y si mides con una prueba nueva el grado que ganó?
:::

::: hint {#ml-c2-pista-termometros-1 of="ml-c2-ej-termometros" title="Pista 1 · ¿Qué puede superar el mínimo?"}
¿Puede el mínimo de trece números ser mayor que el primero de ellos?
:::

::: answer {#ml-c2-resp-termometros of="ml-c2-ej-termometros" title="Respuesta · Separar elección y medición"}
La esperanza del mínimo es menor que 10, salvo que todas las cifras sean idénticas con probabilidad uno. Cada cifra tiene esperanza 10; tomar el mínimo aprovecha las desviaciones favorables. Con una prueba nueva e independiente, la esperanza vuelve a 10: el grado ganador no pudo adaptarse a ella.
:::

> [!TIP]
> **Míralo correr: bloque 3 · El engaño de elegir con la prueba**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

## 5 · Imitar el despliegue

::: figure {#ml-c2-simulacro title="La prueba imita cómo se usará el modelo"}
![Cuatro contratos de uso, uno por fila, cada uno con la barra de la muestra y sus celdas de prueba marcadas con cuadrados. Más de lo mismo: celdas sueltas al azar; separación correcta, al azar. El mes que viene: el último tramo del eje de tiempo; separación correcta, el último tramo de tiempo. Pacientes nuevos: un paciente entero a prueba; separación correcta, pacientes enteros a un lado. Otra ciudad: ninguna fila de la muestra es de la otra ciudad; ninguna separación la imita, se declara el alcance.](../_assets/ml-c2-simulacro.svg)
:::

Cada fila es un contrato de uso; los cuadrados marcan lo apartado. El azar solo responde a la primera fila. Las demás piden respetar tiempo, pacientes o población.

**Piensa: ¿Qué tendría que pasar para que una prueba intacta, que no tocó ninguna decisión, aun así midiera mal?**

Que sus entregas no representaran el uso real. La consigna del profesor es «replicar de la manera más fiel posible lo que ocurrirá en la realidad».

::: definition {#ml-c2-def-simulacro title="La prueba es un simulacro del despliegue"}
Construyes la prueba respondiendo cómo se usará el modelo. Para predecir el mes que viene, apartas el último tramo de tiempo. Para atender pacientes nuevos, apartas pacientes enteros. Para otra población, necesitas prueba de esa población.

Separar al azar vale cuando el despliegue se parece a sacar más observaciones independientes del mismo proceso que generó la muestra. Una separación que no lo imita reporta mal $R(\widehat\beta)$ aunque nadie la haya tocado.
:::

::: figure {#ml-c2-prueba-miente title="Lo que promete la prueba según cómo se separó"}
![Por contrato, lo que promete la prueba contra el riesgo del despliegue, en escala logarítmica. Más de lo mismo, al azar: 11.9 contra R 9.3. El mes que viene, al azar: 57.6 contra R 135.6; por tiempo: 119.4 contra R 155.6. Pacientes nuevos, al azar: 1.9 contra R 17.9; por paciente: 20.3 contra R 18.0. Otra ciudad, al azar: 13.1 contra R 109.5; ninguna separación de la muestra la imita. La raya y punto es el benchmark, la media de entrenamiento.](../_assets/ml-c2-prueba-miente.svg)
:::

Cada par compara lo que promete la prueba con el riesgo del despliegue; el eje vertical usa escala logarítmica. En «más de lo mismo», $11.9\pm5.9$ contiene $R=9.3$: el margen es dos EE, no exactitud.

Compara también con el benchmark. Estas filas corresponden a los modelos ajustados tras separar al azar:

| Contrato | $L_{\text{prueba}}$ | $R$ | Benchmark en despliegue |
|---|---:|---:|---:|
| Más de lo mismo | 11.9 | 9.3 | 50.9 |
| El mes que viene | 57.6 | 135.6 | 132.1 |
| Pacientes nuevos | 1.9 | 17.9 | 59.4 |
| Otra ciudad | 13.1 | 109.5 | 86.1 |

Al azar, «el mes que viene» promete 57.6 frente a 135.6; por tiempo, 119.4 frente a 155.6. Cambia el entrenamiento, por eso cambia también el riesgo. Para pacientes nuevos, separar al azar da 1.9 frente a 17.9; apartar pacientes da 20.3 frente a 18.0.

En “el mes que viene”, $R$ es el error **a largo plazo**: un mes cualquiera del futuro, sin aprovechar lo que el ruido de los últimos días recuerda; justo después de la muestra el error puede salir menor.

Los modelos se fijaron antes de mirar la prueba. El caso temporal usa vecinos sobre distancia y tiempo para aprovechar cercanía temporal. Se eligió para exhibir el engaño: un modelo lineal que solo usa distancia casi no miente, con 103.3 frente a 98.9.

En otra ciudad, 13.1 frente a 109.5 muestra el límite: sin datos de ella, ninguna separación la imita. Solo puedes declarar el alcance. Entrenaste con el tren de ayer; el contrato exige viajar con el de mañana.

Nada que aprenda de los datos, como escalar o imputar, se ajusta antes de separar. Es el anuncio de las fugas (*leakage*); la clase 5 trabaja estas y las condiciones para separar al azar.

> [!WARNING]
> Lectura equivocada: «La prueba es siempre el 20 % al azar».
>
> Lectura correcta: **Primero escribe cómo se usará el modelo; el 20 % al azar es la respuesta de un solo contrato.**

::: exercise {#ml-c2-ej-categoria-ausente title="Interpreta una colonia ausente"}
Separas al azar tiempos de entrega de tres colonias, A, B y C. Por mala suerte, todas las entregas de C caen en la prueba, junto con algunas de A y de B.

Calculas el error de la prueba dos veces: solo con sus entregas de C, y con toda la prueba. ¿Qué mide cada cifra, y a qué contrato de uso corresponde?
:::

::: hint {#ml-c2-pista-categoria-ausente-1 of="ml-c2-ej-categoria-ausente" title="Pista 1 · ¿Qué colonia conocía el modelo?"}
¿El modelo vio alguna vez una entrega de C antes de predecir? ¿Y una de A?
:::

::: answer {#ml-c2-resp-categoria-ausente of="ml-c2-ej-categoria-ausente" title="Respuesta · Nombrar la población evaluada"}
Solo C mide entregas de una colonia nueva: «otra ciudad» en chico. Toda la prueba mezcla colonias conocidas y nuevas según cuántas entregas cayeron de cada una. No representa por sí sola ninguno de los dos contratos propuestos.

Para «más entregas de estas tres colonias», procura que las tres aparezcan en ambos lados: la página siguiente anuncia cómo estratificar. Para «colonias nuevas», aparta una colonia entera y reporta solo su error. La composición de la prueba debe venir del uso previsto, no de un accidente del sorteo.
:::

> [!TIP]
> **Míralo correr: bloque 4 · Imitar el despliegue**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

## 6 · Repartir los datos

::: figure {#ml-c2-reparto title="Aprender y medir compiten por los mismos datos"}
![Contra la fracción de la muestra que va a prueba, de 5 a 50 por ciento, con 60 entregas. Arriba, el riesgo medio del modelo: 10.2 con 10 por ciento, 10.4 con 20 y 11.3 con 50: empeora al quitarle datos. Abajo, la desviación de L_prueba menos R: 7.2 con 10 por ciento, 4.6 con 20 y 3.0 con 50: la medición mejora. Marcas en 20 y 50 por ciento.](../_assets/ml-c2-reparto.svg)
:::

Con el contrato fijado, queda repartir 60 entregas. El eje horizontal es la fracción de prueba; cada punto resume 100 repeticiones. Arriba ves el riesgo medio; abajo, la dispersión de $L_{\text{prueba}}-R(\widehat f)$: cuánto se equivoca la prueba sobre su propio modelo.

**Piensa: Si pones más datos en la prueba, ¿mejora tu modelo o solo tu medición?**

Mejora la precisión esperada de la medición, pero le quitas datos al ajuste. Con 10 %, 20 % y 50 % a prueba, el riesgo medio es 10.2, 10.4 y 11.3. La dispersión del error de estimación baja: 7.2, 4.6 y 3.0. Estos extremos muestran la competencia; no prometen monotonía en cada punto.

Aquí cambia el modelo entre repeticiones. Medir la desviación de $L_{\text{prueba}}$ sola mezclaría esos cambios con el ruido de evaluación. Restar el riesgo de cada modelo separa ambas cosas.

Usaremos 60/20/20 con validación aparte; con validación cruzada, 80/20 para desarrollo/prueba y pliegues dentro del 80 %. Con muchos datos, una prueba del 1 % puede bastar. Importa el tamaño absoluto.

Si quieres un margen aproximado de dos EE menor que una tolerancia, despeja la raíz de la fórmula:

$$n_{\text{prueba}}\approx(2s_\ell/\text{tolerancia})^2.$$

Estima la dispersión con validación, antes de abrir la prueba. El grado elegido con 80 % puede no ser el óptimo para 100 %; la página 3 retoma esa diferencia.

::: exercise {#ml-c2-ej-tamano-prueba title="Calcula cuánta prueba necesitas"}
Tus pérdidas en validación tienen $s_\ell\approx10$. Quieres reportar con $\mathrm{EE}\le0.5$. ¿Cuántas observaciones de prueba necesitas?
:::

::: hint {#ml-c2-pista-tamano-prueba-1 of="ml-c2-ej-tamano-prueba" title="Pista 1 · ¿Cómo despejas el tamaño?"}
¿Qué obtienes al despejar $n$ de $s_\ell/\sqrt n\le0.5$?
:::

::: answer {#ml-c2-resp-tamano-prueba of="ml-c2-ej-tamano-prueba" title="Respuesta · Fijar el tamaño antes de medir"}
Necesitas $n\ge(10/0.5)^2=400$ observaciones. Aquí el límite pedido es para un EE, no para el margen de dos EE. Es una previsión basada en la dispersión de validación y en observaciones independientes.
:::

> [!TIP]
> **Míralo correr: bloque 5 · Repartir los datos**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/03_entrenamiento_y_prueba.ipynb)

## Ejercicio final · Dos contratos para los mismos datos

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#ml-c2-ej-final-entrenamiento-y-prueba title="Dos contratos para los mismos datos"}
Una empresa tiene 2 400 entregas de 40 clientes durante 12 meses, 200 por mes. Firmará uno de dos contratos:

- A: predecir las entregas del mes próximo de esos mismos 40 clientes.
- B: atender clientes nuevos en la misma ciudad.

Simplifica: cada cliente tiene exactamente 5 entregas cada mes, 60 en el año. El modelo es un polinomio en la distancia, con grado entre 0 y 8. La dificultad nueva son dos estructuras, tiempo y cliente; cada contrato respeta una distinta. Hay varias separaciones válidas; justifica la tuya.

1. Para cada contrato, indica qué observaciones van a prueba.
2. Explica cómo eliges el grado sin tocar esa prueba.
3. Di qué reportas al final: $L_{\text{prueba}}$ es el promedio por entrega. ¿Vale $s_\ell/\sqrt{n_{\text{prueba}}}$ para su EE? Si no, identifica una unidad independiente y escribe la fórmula para esa misma cifra, con sus supuestos; no necesitas un número.
4. Explica qué esperarías si eligieras el grado con la prueba y reportaras su error.
5. En B, si todos tus clientes son de una sola zona, ¿qué afirmación no puedes hacer?
:::

::: hint {#ml-c2-pista-final-entrenamiento-y-prueba-1 of="ml-c2-ej-final-entrenamiento-y-prueba" title="Pista 1 · ¿Qué es «nuevo» en cada contrato?"}
¿Qué información sobre el cliente y el mes existiría ya en el momento de predecir?
:::

::: hint {#ml-c2-pista-final-entrenamiento-y-prueba-2 of="ml-c2-ej-final-entrenamiento-y-prueba" title="Pista 2 · Revisa tu borrador"}
¿Hay alguna observación de prueba que se parezca a una de entrenamiento más de lo que se parecerá el uso real a tus datos?
:::

::: answer {#ml-c2-resp-final-entrenamiento-y-prueba of="ml-c2-ej-final-entrenamiento-y-prueba" title="Respuesta · Respetar lo nuevo de cada contrato"}
**1. Apartar.** Una opción en A es reservar el último mes, con todos los clientes. En B, apartar 8 clientes enteros, con todos sus meses.

**2. Elegir.** Dentro de lo restante, valida con el penúltimo mes en A y con clientes apartados en B. Compara grados ahí. La validación cruzada de la página siguiente también debe respetar la estructura.

**3. Reportar.** Reajusta con desarrollo y abre la prueba una vez. Reporta $L_{\text{prueba}}$ y el benchmark. Las entregas de un cliente pueden depender entre sí: no puedes aplicar automáticamente el EE de entregas independientes. Con dependencia positiva, ese EE subestima la incertidumbre; en general, puede subestimarla.

Si supones clientes independientes entre sí, usa como unidad el cliente. Promedia sus pérdidas y calcula el EE como la desviación de esos promedios entre la raíz del número de clientes. En B hay 8: espera un EE ancho. En A hay 40, para el mes observado.

Esta es la incertidumbre de la misma cifra: cada cliente aporta igual número de entregas, 60 en B y 5 en A. Por eso el promedio por entrega coincide con el promedio de los promedios por cliente.

Sin tamaños iguales, cambias de cifra. Un cliente con 1 entrega de pérdida 0 y otro con 9 de pérdida 10 dan 9 por entrega y 5 por cliente. El contrato debe decidir qué cuenta igual; la independencia de clientes no vuelve iguales esos promedios.

En A la cifra corresponde al mes reservado, no promedia meses futuros. La fórmula por cliente requiere independencia entre esos promedios; no cubre automáticamente la variación entre meses. La clase 5 trabaja ese límite.

**4. Anticipar.** Elegir con la prueba introduce optimismo por selección (@ml-c2-obs-optimismo-seleccion): favoreces pérdidas accidentalmente bajas y reportas esas mismas cifras.

**5. Delimitar.** En B no puedes afirmar el mismo desempeño en otra zona. El simulacro no contiene clientes de ella.
:::

**Punto de control:** deberías poder explicar por qué $L_{\text{prueba}}$ deja de estimar $R$ si eliges con ella, y escribir la separación de un contrato de uso.

## Para profundizar

- Goodfellow, Bengio y Courville, *Deep Learning*: §5.2, capacidad y ajuste; §5.3, hiperparámetros y validación; §5.4.3, varianza y error estándar.
- Hastie, Tibshirani y Friedman, *The Elements of Statistical Learning*, 2.ª ed., §7.2: sesgo, varianza y complejidad del modelo.

## Lo que hay que llevarse

- El entrenamiento elige grado 12: obtiene 4.5 en los datos que ajustaron sus coeficientes.
- Elegir con la prueba anuncia 7.5 menos error en promedio, con EE de Monte Carlo 1.8; el modelo elegido no se reajusta.
- Elegir con validación deja mediana −0.6 y 56 % de anuncios optimistas. La media $-42.0\pm37.2$ queda a menos de dos EE de cero; unas pocas repeticiones pesan mucho.
- Con el modelo congelado, la prueba baila 3.8 con 20 entregas y 1.1 con 200. Una prueba honesta también tiene incertidumbre.
- Para «el mes que viene», separar al azar promete 57.6 y el despliegue da 135.6. Apartar datos sirve si imita cómo usarás el modelo.

Continúa con [[ml-validacion-cruzada|Validación cruzada]].
