---
id: ml-sesgo-y-varianza
title: "Sesgo y varianza: de dónde sale el error"
nav_title: "Sesgo y varianza"
summary: "El error esperado en un punto se parte en ruido, sesgo al cuadrado y varianza; se deriva, se mide con cien entrenamientos y se lee en la curva en U, en las curvas de aprendizaje y en el diagnóstico de subajuste y sobreajuste."
status: ready
estimated_time: 65m
tags: [aprendizaje-maquina, sesgo, varianza, curva-de-aprendizaje, sobreajuste, subajuste]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 05 · Sesgo y varianza.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)
>
> **[👉 Abrir `05_sesgo_y_varianza.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)**

# Sesgo y varianza: de dónde sale el error

**Si repites el mismo procedimiento con otra muestra, ¿por qué cambia la predicción, y qué parte de tu error es culpa de eso?**

Ya separaste entregas para medir el error; ahora explicarás de dónde sale.
Repite el entrenamiento con otras 36 entregas del mismo proceso:
conservas método y grado, pero la curva puede moverse.

Al terminar tendrás:

- **Identidad:** habrás derivado ruido + sesgo² + varianza en un punto.
- **Cálculo:** habrás obtenido sesgo y varianza a mano para tres predicciones.
- **Comparación:** la curva en U calculada junto a la medida por CV.
- **Datos:** qué baja al aumentar la muestra y qué no.
- **Diagnóstico:** subajuste, sobreajuste o ruido a partir de dos curvas y un punto de comparación.

Dedica unos 30 minutos a leer y 35 al notebook; el ejercicio final va aparte.

> **Lo que traes**
>
> @ml-c1-def-estimacion: $\widehat f$ depende de la muestra de entrenamiento.
>
> @ml-c1-obs-cuatro-fuentes: azar, variables que no medimos, familia equivocada y pocos datos; la optimización va aparte.
>
> @ml-c1-def-error-bayes: el piso de error para una pérdida y unas variables visibles.
>
> @ml-c1-def-proceso-generador: cómo se producen las entregas y su ruido.
>
> De [[ml-validacion-cruzada|Validación cruzada]] (*cross-validation*), la U medida en @ml-c2-cv-capacidad.

## 1 · Repetir el entrenamiento cien veces

Cada línea delgada es el ajuste de una muestra distinta del mismo proceso.
El eje horizontal mide distancia en kilómetros; el vertical, predicción
en minutos. Compara cuánto cambian las curvas al recibir otras entregas.

::: figure {#ml-c2-abanico title="Cien muestras, cien ajustes"}
![Tres paneles con 100 ajustes cada uno, uno por muestra del mismo proceso, su promedio y la verdadera E[y | x]. Grado 1: las rectas casi no se separan (desviación 0.9 en x = 5) pero su promedio se aleja de la curva. Grado 4: abanico angosto (desviación 1.1) y promedio pegado a la curva. Grado 12: en el centro el promedio sigue la curva, pero en los bordes se aleja (llega a −32.8 en x = 6.0), y cada ajuste se sacude, sobre todo en los bordes (desviación 3.5 en x = 5).](../_assets/ml-c2-abanico.svg)
:::

En grado 1 el promedio se aleja de $f$; en grado 12 las líneas se abren.
El trazo cian grueso discontinuo es el promedio; el verde grueso es $f$.
El promedio de grado 12 se acerca a la curva en el centro.
En los bordes también se dispara, arrastrado por unos pocos ajustes.

El eje vertical está fijo de 0 a 50 minutos, así que en el grado 12 algunas curvas salen de él.

Aquí $x_0$ significa «un punto fijo de $x$»: usamos $x_0=5$ km, dentro del intervalo de distancias.
En la clase 1, $x_0$ nombraba el centro de Taylor; aquí no hacemos una expansión.

**Piensa: ¿qué grado cambiaría más su predicción en $x_0=5$ si te dieran otra muestra?**

El grado 12: su desviación entre muestras es 3.5 minutos, frente a 0.9 del grado 1.
Son cifras de esta simulación. El grado permanece fijo dentro de cada panel:
repetimos el ajuste, no la selección.

Como recuerda @ml-c1-def-estimacion, $\widehat f(x)$ es una variable aleatoria porque depende de $\mathcal D$.
Imagina cien equipos que reciben muestras diferentes y aplican el mismo método.
Para resumirlos, promedia sus predicciones en cada distancia:

$$\bar f(x)=E_{\mathcal D}[\widehat f(x)].$$

Es el **ajuste promedio**. El subíndice $\mathcal D$ indica que promediamos
sobre muestras posibles del mismo tamaño. Las 100 repeticiones lo aproximan.
El sesgo mide el desplazamiento del promedio respecto de $f$; la varianza,
la dispersión entre equipos. Un grupo puede estar muy unido y equivocarse
hacia el mismo lado, como las rectas del grado 1.

::: exercise {#ml-c2-ej-que-cambia title="Compara la dispersión de los ajustes"}
Sin mirar la figura: con $n=36$, ¿qué abanico es más ancho en los extremos,
el de grado 2 o el de grado 10, y por qué?
:::

::: hint {#ml-c2-pista-que-cambia-1 of="ml-c2-ej-que-cambia" title="Pista 1 · ¿Cuántos coeficientes estimas?"}
¿Cuántos coeficientes tiene que estimar cada uno con las mismas 36 entregas?
:::

::: answer {#ml-c2-resp-que-cambia of="ml-c2-ej-que-cambia" title="Respuesta · Comparar la sensibilidad a la muestra"}
Esperamos un abanico más ancho para el grado 10. Estima más coeficientes
con los mismos datos y el ajuste resulta más sensible a la muestra.
Esa sensibilidad se nota especialmente en los extremos, donde hay menos
puntos que sujeten la curva. Es la comparación de este experimento,
no una ley para cualquier procedimiento.
:::

> [!TIP]
> **Míralo correr: bloque 1 · Abanico y diana**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)

## 2 · Separar el error en tres partes

Fijemos la distancia para separar desplazamiento y dispersión.
Cada marca es la predicción de una muestra en el mismo $x_0$.
El eje del valor mide minutos; el apilamiento solo permite distinguir marcas.

::: figure {#ml-c2-diana title="La diana en x = 5"}
![Predicciones en x = 5 de 100 ajustes, cada uno con otra muestra, junto a E[y | x = 5] = 31.5. Grado 1: las cruces se agrupan apretadas (desviación 0.9) pero corridas 1.5 minutos del valor verdadero. Grado 12: centradas (sesgo −0.5) pero dispersas (desviación 3.5). El promedio de cada grado es una raya blanca discontinua; la banda gris marca E[y | x = 5] ± σε, de 28.5 a 34.5, la escala del ruido nuevo. Eje fijo de 15 a 55 minutos; ninguna predicción queda fuera.](../_assets/ml-c2-diana.svg)
:::

Sesgo es la distancia con signo de la raya blanca discontinua, el promedio, a la línea verde;
varianza, cuánto se dispersan las marcas. Aquí $f(x_0)=31.5$ minutos.
El grado 1 tiene sesgo 1.5; el grado 12, $-0.5$.
La banda $f(x_0)\pm\sigma_\varepsilon$ muestra la escala del ruido nuevo.
Ninguna predicción queda fuera del eje de la diana.

**Piensa: si conocieras $f$ exactamente y predijeras $f(x_0)$, ¿tu error al predecir una entrega nueva sería cero?**

No: todavía quedaría el ruido de esa entrega. Acertar el promedio no
elimina las variaciones alrededor de él. Al cuadrar el error aparecen
tres aportaciones: ruido, desplazamiento del ajuste promedio y dispersión
entre muestras. La identidad siguiente dice cómo sumarlas.

::: theorem {#ml-c2-teo-sesgo-varianza title="Ruido, sesgo y varianza"}
Supuestos: una observación nueva $y=f(x)+\varepsilon$ con
$E[\varepsilon\mid x]=0$ y $\operatorname{Var}(\varepsilon\mid x)=\sigma_\varepsilon^2(x)$
(@ml-c1-def-proceso-generador), independiente de la muestra de
entrenamiento $\mathcal D$ con que se calculó $\widehat f$; segundos
momentos finitos; pérdida cuadrática. Con
$\text{sesgo}(x)=E_{\mathcal D}[\widehat f(x)]-f(x)$ y
$\text{varianza}(x)=\operatorname{Var}_{\mathcal D}\bigl(\widehat f(x)\bigr)$,

$$E_{\mathcal D,\varepsilon}\bigl[(y-\widehat f(x))^2\mid x\bigr]=\sigma_\varepsilon^2(x)+\text{sesgo}(x)^2+\text{varianza}(x).$$

Promediando en las $x$ del despliegue:

$$E_{\mathcal D}\bigl[R(\widehat f)\bigr]=E_x\bigl[\sigma_\varepsilon^2(x)\bigr]+E_x\bigl[\text{sesgo}(x)^2\bigr]+E_x\bigl[\text{varianza}(x)\bigr],$$

donde $R(\widehat f)$ es el riesgo de la función ajustada, sea o no
paramétrica (para un polinomio, $R(\widehat\beta)$; para vecinos, no hay
$\beta$). Aquí $x$ son **todas** las variables y $f$ es la función
estructural; como $E[\varepsilon\mid x]=0$, $f(x)=E[y\mid x]$ y el primer
término promediado es $R_{\text{Bayes}}$ de @ml-c1-def-error-bayes.
:::

Si el modelo no ve todas las variables, cambia la referencia. Lo mismo
ocurre si hay endogeneidad. Sustituye $f(x)$ por la media condicional con
lo visible, $E[y\mid x_{\text{visibles}}]$, y $\sigma_\varepsilon^2(x)$ por
$\operatorname{Var}(y\mid x_{\text{visibles}})$. El sesgo se mide entonces
contra $E[y\mid x_{\text{visibles}}]$; la derivación es la misma.

El promedio del primer término es $R_{\text{Bayes}}$ respecto de lo visible.
Dejar de ver una variable **no lo disminuye y puede aumentarlo**.
Puede quedar igual si esa variable es independiente de $y$ y de las demás
(@ml-c1-def-error-bayes). Es la fuente «variables que no medimos» de
@ml-c1-obs-cuatro-fuentes.

::: proof {#ml-c2-dem-sesgo-varianza of="ml-c2-teo-sesgo-varianza"}
1. Fija $x$ y escribe $\bar f(x)=E_{\mathcal D}[\widehat f(x)]$, el «ajuste promedio».
   Suma y resta:

   $$y-\widehat f(x)=\varepsilon+\bigl(f(x)-\bar f(x)\bigr)+\bigl(\bar f(x)-\widehat f(x)\bigr).$$

2. Eleva al cuadrado: tres cuadrados y tres productos cruzados.

3. $E[\varepsilon^2\mid x]=\sigma_\varepsilon^2(x)$;
   $\bigl(f(x)-\bar f(x)\bigr)^2=\text{sesgo}(x)^2$ (no es aleatorio);
   $E_{\mathcal D}\bigl[(\bar f(x)-\widehat f(x))^2\bigr]=\text{varianza}(x)$.

4. Productos cruzados con $\varepsilon$: $\varepsilon$ es independiente de
   $\mathcal D$ y $E[\varepsilon\mid x]=0$, así que su esperanza es 0.

5. Producto cruzado restante:

   $$2\bigl(f(x)-\bar f(x)\bigr)\,E_{\mathcal D}\bigl[\bar f(x)-\widehat f(x)\bigr]=0,$$

   porque $E_{\mathcal D}[\widehat f(x)]=\bar f(x)$.

6. Sumando queda la identidad.

7. Para la versión promediada, toma $E_x$ de los tres términos y usa que

   $$E_{\mathcal D}[R(\widehat f)]=E_x\bigl[E_{\mathcal D,\varepsilon}[(y-\widehat f(x))^2\mid x]\bigr].$$
:::

Ningún modelo baja el primer término con las mismas variables visibles
y pérdida cuadrática. Es el piso: en este proceso, $\sigma_\varepsilon^2=9.0$.
Los otros términos miden qué añade nuestro procedimiento de ajuste.

Goodfellow y sus coautores dan la identidad para un estimador, sin ruido,
en las ecuaciones 5.53–5.54. Aquí predecimos una respuesta nueva con una
función ajustada, por eso aparece el ruido.
La identidad describe el promedio sobre entrenamientos posibles, no el
error de una sola prueba.

Recupera las cuatro fuentes: **azar, variables que no medimos, familia equivocada y pocos datos** (@ml-c1-obs-cuatro-fuentes).
La optimización va aparte. El ruido recoge el piso que fijan las dos primeras.
El sesgo se relaciona con la familia equivocada y la varianza con los pocos
datos, pero esas correspondencias no son identidades.

El error de aproximación pertenece a la familia: mide lo que falta aun
con infinitos datos. Compara su mejor función con $E[y\mid x_{\text{visibles}}]$.
El sesgo pertenece al procedimiento a tamaño finito: con todas las variables,
es $E_{\mathcal D}[\widehat f(x)]-f(x)$ para un $n$ dado.

Si el procedimiento converge en media cuadrática a la mejor función de
la familia, su sesgo tiende al desajuste de aproximación y su varianza a cero.
Con $n$ finito no son lo mismo: **no se garantiza que el sesgo quede
idéntico al cambiar el tamaño muestral**.

> [!WARNING]
> Lectura equivocada: «La varianza es lo ancho de los residuales».
>
> Lectura correcta: **la varianza es cuánto cambia la predicción en un mismo $x$ al cambiar la muestra de entrenamiento.** Lo ancho de los residuales mezcla ruido, sesgo y varianza.

Para comprobar la cuenta a mano, sustituye los cien ajustes por tres
predicciones posibles. Este ejemplo pequeño permite calcular exactamente
el promedio sobre muestras.

::: exercise {#ml-c2-ej-tres-predicciones title="Calcula sesgo, varianza y error esperado"}
En un $x$ fijo, $f(x)=11$. Un procedimiento predice $8$, $10$ o $12$,
cada una con probabilidad $1/3$ según la muestra, y el ruido nuevo tiene varianza 4.
Calcula sesgo, varianza y error cuadrático esperado.
:::

::: hint {#ml-c2-pista-tres-predicciones-1 of="ml-c2-ej-tres-predicciones" title="Pista 1 · ¿Respecto de qué promedio?"}
¿Alrededor de qué número se mide la varianza: de $f(x)$ o del promedio de las predicciones?
:::

::: answer {#ml-c2-resp-tres-predicciones of="ml-c2-ej-tres-predicciones" title="Respuesta · Sumar las tres partes del error"}
El promedio es 10. El sesgo es $-1$: el procedimiento predice, en promedio,
por debajo de $f(x)=11$.
La varianza mide las desviaciones cuadráticas respecto de 10:

$$\frac{4+0+4}{3}=\frac83.$$

Aplicando @ml-c2-teo-sesgo-varianza, el error cuadrático esperado es

$$4+1+\frac83=\frac{23}{3}\approx7.67.$$

El sesgo puede ser negativo; su contribución al error es su cuadrado.
:::

## 3 · Ver la curva en U

Arriba, cada barra suma las tres partes calculadas con $f$ conocida y cien muestras.
Abajo, la CV mide con una sola muestra. Los ejes son grado y error cuadrático,
en minutos cuadrados.

::: figure {#ml-c2-sesgo-varianza title="La U calculada y la U medida"}
![Dos paneles con el grado N de 0 a 12. Arriba, barras apiladas de ruido, sesgo al cuadrado y varianza calculadas con f conocida y 100 muestras: el ruido mide 9.0 en todos los grados, el sesgo al cuadrado baja de 43.8 en N = 0 a 0.90 en N = 2 y la varianza, salvo de N = 0 a 1, sube; el menor total, 10.89, está en N⋆ = 2. La varianza va abajo del sesgo² en cada barra. De N = 8 a 12 las barras salen del eje y llevan su total escrito (72 a 34200), casi todo varianza; ahí el sesgo² estimado vuelve a crecer (20.5 en N = 9, 64.9 en N = 12), arrastrado por los bordes. Abajo, en escala log, la CV 5 de una sola muestra, con mínimo en N = 6, junto al total calculado: las dos bajan y suben en la misma zona sin coincidir punto por punto; el total del grado 12 sale del eje.](../_assets/ml-c2-sesgo-varianza.svg)
:::

Las dos curvas bajan y suben en la misma zona, sin coincidir punto por punto.
Las barras de grados 8 a 12 salen del eje y llevan su total escrito; casi todo es varianza. Abajo usamos escala logarítmica.

**Piensa: ¿por qué la curva de la CV de una sola muestra es más irregular que la U calculada con cien?**

La CV fluctúa con la muestra y la partición. Además, entrena con
$(k-1)/k$ de los datos (@ml-c2-def-validacion-cruzada). Las cien muestras
estabilizan el cálculo del simulador, que usa entrenamientos completos.

De $N=0$ a $N=7$, el sesgo² estimado baja en conjunto: 43.8, 6.0, 0.90, 0.73, 0.45, 0.50, 0.24 y 0.27, con un repunte chico de $N=4$ a $N=5$. La varianza sube hasta 10.9 en $N=7$, salvo de $N=0$ a $N=1$, cuando baja de 1.43 a 0.88.

Desde $N=8$, el sesgo² estimado vuelve a crecer: 20.5 en $N=9$ y 64.9 en $N=12$. No es que el grado 12 «tenga sesgo», sino que unos pocos ajustes se disparan en los bordes y arrastran el promedio de cien, que tiene ruido de Monte Carlo. En el tramo interior, $0.5<x<5.5$, el sesgo² no pasa de 0.25 desde $N=6$.

Por eso la tendencia vale hasta $N\approx7$ y lees la barra alta del grado 12 como varianza.

El grado 2 suma ruido 9.0, sesgo² 0.90 y varianza 0.99: total 10.89.
La identidad no exige monotonía de cada término.
**La U es una tendencia observada**, no una ley.

Buscamos el grado de menor riesgo esperado sobre entrenamientos posibles:

$$N^\star\in\operatorname*{arg\,min}_N E_{\mathcal D}\bigl[R\bigl(\widehat\beta(N)\bigr)\bigr].$$

Con empate, elegimos el menor $N$; la estrella marca el óptimo teórico, como en esta regla; el que eligen los datos lleva gorro, $\widehat N$.
Obtenemos $N^\star=2$, calculado en el simulador, donde conocemos $f$:
100 muestras y el mismo grado con tres semillas maestras.
La CV de una muestra eligió $\widehat N=6$.

En la clase 3 cambiarás el grado por una perilla continua de regularización.
Ahora conservaremos el grado y aumentaremos las entregas.

::: exercise {#ml-c2-ej-u-y-cv title="Compara el óptimo teórico con la CV"}
La U calculada tiene mínimo en $N^\star=2$; la CV eligió $\widehat N=6$.
Sus totales son 10.89 y 14.58. ¿Está mal la CV? Compara riesgos.
:::

::: hint {#ml-c2-pista-u-y-cv-1 of="ml-c2-ej-u-y-cv" title="Pista 1 · ¿Cuánto difieren los riesgos?"}
¿Qué tan distintos son los totales calculados en esos dos grados?
:::

::: answer {#ml-c2-resp-u-y-cv of="ml-c2-ej-u-y-cv" title="Respuesta · Comparar riesgos"}
No necesariamente: una estimación ruidosa puede elegir un grado distinto
sin que el procedimiento esté mal. Aquí el grado 6 tiene mayor total:
14.58 frente a 10.89. No basta decir que ambos grados están cerca.

Si la diferencia de riesgos fuera menor que un EE pertinente,
podrías atribuir la elección al ruido de la comparación. El enunciado
no da ese EE: no permite afirmar equivalencia. La comparación útil
es entre riesgos, no entre números de grado.
:::

> [!TIP]
> **Míralo correr: bloque 2 · La U calculada y la U medida**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)

## 4 · Comprar más datos

Cada punto superior es la mediana de 50 muestras. El eje horizontal
duplica entregas de 30 a 960, en escala logarítmica; el vertical mide pérdida cuadrática.
La línea punteada marca el piso del riesgo.

::: figure {#ml-c2-curva-aprendizaje title="Más datos: a quién le ayudan"}
![Arriba, medianas de 50 muestras contra el número de entregas, de 30 a 960 en escala log: el riesgo R del grado 1 baja de 14.7 a 13.8 y se queda en 13.8, arriba del piso de 9.0; el del grado 10 empieza arriba de la recta y baja a 9.1 y 9.0, pegado al piso. Abajo, el grado que elige la CV 5 (mediana de 20 muestras) sube de 3 con 30 entregas a 10 con 960.](../_assets/ml-c2-curva-aprendizaje.svg)
:::

La recta se estanca: pasa de 14.7 con 30 entregas a 13.8 con 480 y con 960.
El grado 10 empieza arriba de ella; llega a 9.1 con 480 y a 9.0 con 960.
Son medianas; la identidad describe promedios.

**Piensa: ¿más entregas le ayudan igual a la recta que al polinomio de grado 10?**

No: la recta se estabiliza sin seguir toda la curvatura. El grado 10
se acerca al piso $R_{\text{Bayes}}=9.0$ al estabilizarse
(@ml-c1-def-error-bayes).

::: definition {#ml-c2-def-curva-aprendizaje title="Curva de aprendizaje"}
Para un procedimiento fijo, la **curva de aprendizaje** grafica
$L_{\text{ent}}$ y una estimación honesta del riesgo contra $n_{\text{ent}}$.
Puede usar $L_{\text{val}}$, $\mathrm{CV}_k$ o, en el simulador, $R$;
una horizontal marca $R_{\text{Bayes}}$, si se conoce.

Su separación estima la brecha (@ml-c1-def-brecha); la distancia del riesgo
al piso indica cuánto puedes ganar.
:::

::: remark {#ml-c2-obs-cota-generalizacion title="Lo que dice una cota y lo que se observa"}
**(a) La cota.** Con probabilidad alta, que uno fija de antemano,
la brecha queda bajo un término que crece con la capacidad y baja con $n$.
Puede usar la dimensión VC (@ml-c1-def-capacidad; Goodfellow et al., §5.2).

**(b) Sus condiciones.** Exige observaciones independientes del mismo proceso,
pérdida acotada y familia fijada antes de ver los datos.
Fuera de ellas no garantiza nada; la pérdida cuadrática del hilo no está acotada.

**(c) Lo observado.** La brecha medida crece con la capacidad y baja con $n$
en @ml-c2-cv-capacidad y @ml-c2-curva-aprendizaje: es una tendencia experimental.
Una cota superior creciente no obliga a crecer a la cantidad acotada.
Estas cotas son flojas: no predicen el número.
:::

::: remark {#ml-c2-obs-mas-datos-no-siempre title="Lo que más datos bajan y lo que no"}
Más datos reducen el riesgo **en general, no siempre**; aquí, principalmente
por la varianza. No quitan ruido ni error de aproximación de la familia.
El sesgo a tamaño finito puede cambiar con $n$; con la convergencia de §2,
se acerca al desajuste de aproximación.

El caso 23, a un tamaño fijo, interpola con $n=10$ y grado 12:
$L_{\text{ent}}\approx0$ y riesgo enorme. No compara tamaños muestrales.
:::

Aquí, $L_{\text{ent}}$ del modelo grande sube con $n$. Puede quedar
bajo el piso, que limita el riesgo, no la pérdida usada para ajustar.

Abajo, el grado elegido por CV, mediana de 20 repeticiones, sube de 3
con 30 entregas a 10 con 960. La capacidad elegida con 80 %
puede cambiar al reajustar con 100 %.

::: exercise {#ml-c2-ej-mas-datos title="Evalúa si más datos ayudan"}
El grado 1 tiene $R=13.8$ con $n_{\text{ent}}=480$ y con 960
(medianas); el piso es 9.0. ¿Cuánto bajará $R$ si duplicas otra vez?
:::

::: hint {#ml-c2-pista-mas-datos-1 of="ml-c2-ej-mas-datos" title="Pista 1 · ¿Qué limita a una recta?"}
¿Cuánto bajó en la última duplicación, y qué parte del error de una recta no depende de $n$?
:::

::: answer {#ml-c2-resp-mas-datos of="ml-c2-ej-mas-datos" title="Respuesta · Cambiar lo que limita"}
Esperamos que baje muy poco: la última duplicación dejó la misma cifra
redondeada. En esta simulación, a ese tamaño domina el error de aproximación
de la recta. Más entregas no le permiten curvarse; hace falta otra familia
o más capacidad.

No todo exceso sobre el piso es sesgo. Una familia flexible con pocos
datos también puede tener mucha varianza. La conclusión usa la familia
y la evolución de sus curvas, no solo la distancia al piso.
:::

> [!TIP]
> **Míralo correr: bloque 3 · Curvas de aprendizaje**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)

## 5 · Diagnosticar con dos curvas

Lee el árbol de arriba abajo con entrenamiento, CV y un *benchmark*: «la media de entrenamiento como punto de comparación; la clase 3 lo define».

::: figure {#ml-c2-diagnostico title="Diagnosticar con dos curvas y un benchmark"}
![Árbol de diagnóstico con cuatro preguntas que se leen de arriba abajo. Uno: la brecha entre validación, o CV, y entrenamiento es grande; si sí, sobreajuste: menos capacidad o más datos. Dos: le gana al benchmark, la media de entrenamiento; en una validación que no eligió el modelo, la diferencia pareada baja de cero a más de dos errores estándar; con CV solo da señal o falta evidencia; si no, no aprende: otras variables o familias. Tres: subir el grado baja la CV más de un error estándar, una heurística; si sí, subajuste: más capacidad o mejor phi. Cuatro: la prueba imita el despliegue; si sí, listo; si no, rehacer la separación.](../_assets/ml-c2-diagnostico.svg)
:::

El subajuste se reconoce al bajar el error honesto con más flexibilidad.
El piso solo se conoce en el simulador.

**Piensa: si los errores de entrenamiento y validación son altos y parecidos, ¿es subajuste o ruido? ¿Qué experimento harías para saberlo?**

Compara familias más flexibles y el benchmark. La CV da «señal»
o «falta evidencia»: es descriptiva. Confirma en una reserva que no tocó ninguna decisión.

1. **¿La brecha es grande?** Compara $L_{\text{val}}-L_{\text{ent}}$
   o $\mathrm{CV}_k-L_{\text{ent}}$. Si sí, diagnostica sobreajuste
   (*overfitting*): prueba menos capacidad, regularización o más datos.

2. **¿Le gana al benchmark?** Distingue dos casos.

   **(a) En validación, si la validación no eligió el modelo.**
   Ambos modelos se fijaron antes y se ajustaron solo con entrenamiento.
   Por entrega de validación, compara
   $d_i=\ell_i^{\text{modelo}}-\ell_i^{\text{benchmark}}$.
   Un valor negativo favorece al modelo.

   Le gana si la media queda bajo cero a más de dos EE
   de la diferencia pareada de pérdidas: $s_d/\sqrt{n_{\text{val}}}$,
   con $s_d$ la desviación de las diferencias. Es aproximado, para esos dos modelos.
   Si validación eligió el modelo, confirma en la prueba, abierta una vez.

   **(b) Con CV.** Compara medias y $k$ diferencias por pliegue
   usando la misma partición; el benchmark del hilo es $N=0$.
   Si la diferencia media no sale de la dispersión, falta evidencia.
   Si sale a favor del modelo, hay señal; confirma con (a).

   Las pérdidas fuera de pliegue dependen entre sí porque los entrenamientos se traslapan.
   Si elegiste el modelo con esa CV, la comparación es además optimista (@ml-c2-obs-optimismo-seleccion).

   Sin evidencia favorable, no demuestra aprendizaje aprovechable: puede haber ruido
   o variables pobres. Prueba otras variables y familias con CV;
   si ninguna supera al benchmark en una reserva intacta, decláralo.

3. **¿Subir la capacidad baja la CV más de un EE?** Lee la curva
   contra el grado. Es una heurística descriptiva, no una prueba.
   Si sí, diagnostica subajuste (*underfitting*): aumenta capacidad,
   mejora $\phi$ o las variables. Compara el nuevo modelo con el benchmark
   en una reserva que no lo eligió.

4. **¿Tu prueba imita el despliegue?** Si sí, listo: puede quedar ruido
   o patrones que esta familia y estas variables no captan.
   Si no, rehace la separación como en la página 1, §5.

El benchmark puede fallar mucho en ambos conjuntos y dejar una brecha casi cero.
Su brecha esperada es positiva: del orden de la varianza de $y$ entre $n_{\text{ent}}$.

> [!NOTE]
> **Un modelo exitoso**
>
> Le gana al benchmark por más de dos EE de la diferencia pareada en una reserva que no tocó ninguna decisión, con ambos modelos fijados. Usa la prueba una vez o validación que no eligió el modelo. Más flexibilidad no mejora la CV: señal heurística, no prueba.
>
> Tiene una brecha chica.
>
> **La prueba imita la realidad.**

::: exercise {#ml-c2-ej-cuatro-curvas title="Diagnostica con las curvas y el benchmark"}
Clasifica A–D y propón acciones. Supón que sus pruebas imitan el despliegue.
Los modelos se fijaron antes, ajustados solo con entrenamiento; validación
no eligió nada. Las pérdidas son cuadráticas.

| Proceso (grado actual) | $L_{\text{ent}}$ | $\mathrm{CV}_5\pm\mathrm{EE}$ | Mejor grado más flexible: CV |
|---|---:|---:|---|
| A (1) | 12.6 | 15.1 ± 0.9 | 8: 9.7 |
| B (12) | 5.7 | 262.2 ± 143.9 | — |
| C (1) | 59.2 | 66.3 ± 4.9 | 6: 67.4 |
| D (4) | 8.5 | 9.7 ± 0.5 | 8: 9.7 |

Las diferencias son «modelo menos benchmark»; CV es descriptiva:
media y rango de las cinco diferencias por pliegue.

| Proceso | Benchmark: $\mathrm{CV}_5\pm\mathrm{EE}$ | (a) Diferencia pareada en validación (EE) | (b) Diferencia de CV: media [rango] |
|---|---:|---:|---|
| A | 49.8 ± 3.7 | −40.2 (8.7) | −34.7 [−42.3, −25.0] |
| B | 56.7 ± 12.5 | 58.5 (49.3) | 205.5 [−26.6, 777.3] |
| C | 65.8 ± 4.9 | −0.1 (0.3) | 0.5 [−0.1, 1.3] |
| D | 49.8 ± 3.7 | −49.6 (9.5) | −40.1 [−50.2, −29.6] |
:::

::: hint {#ml-c2-pista-cuatro-curvas-1 of="ml-c2-ej-cuatro-curvas" title="Pista 1 · ¿Por dónde empiezas el diagnóstico?"}
¿Qué pregunta del árbol va primero, y con qué dos números se contesta?
:::

::: answer {#ml-c2-resp-cuatro-curvas of="ml-c2-ej-cuatro-curvas" title="Respuesta · Seguir el orden"}
- **A: subajuste.** Supera al benchmark en validación; subir el grado baja la CV más de un EE. Prueba más capacidad: es una heurística.
- **B: sobreajuste.** La CV es 262.2 frente a 5.7 de entrenamiento. Reduce capacidad o consigue más datos.
- **C: no aprende algo aprovechable.** La diferencia pareada no baja de cero a más de dos EE; la CV da «falta evidencia». Prueba otras variables.
- **D: listo.** Supera al benchmark en validación, tiene brecha chica y más grado no mejora la CV; la prueba imita el despliegue.

La CV sola no bastaba para afirmar que A o D superan al benchmark:
solo daba una señal.
:::

> [!TIP]
> **Míralo correr: bloque 4 · Cuatro procesos misteriosos**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/05_sesgo_y_varianza.ipynb)

## Ejercicio final · Un consultor con dos curvas

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#ml-c2-ej-final-sesgo-y-varianza title="Un consultor con dos curvas"}
Un consultor entrega dos modelos de tiempos de entrega y propone comprar
4000 entregas más. La idea nueva es decidir una inversión con las curvas,
además de nombrar el problema.

Estas cifras son medianas de 20 muestras de cada tamaño.
El modelo A usa grado 12; el B, grado 1. Suponemos que los datos nuevos
vendrían del mismo proceso. No conocemos su costo ni el valor económico
de reducir el error: recomienda si comprar ayudaría a predecir,
sin calcular rentabilidad.

| Modelo | $n_{\text{ent}}$ | $L_{\text{ent}}$ | $\mathrm{CV}_5$ |
|---|---:|---:|---:|
| A | 120 | 8.1 | 11.8 |
| A | 480 | 8.7 | 9.2 |
| B | 120 | 13.9 | 14.4 |
| B | 480 | 14.3 | 14.4 |

1. Diagnostica cada modelo a partir de sus dos tamaños.
2. Indica qué término de la identidad explica el problema de cada uno y qué no puedes distinguir.
3. Decide si comprar datos ayudaría a cada modelo y justifica tu recomendación.
4. Propón qué harías con el modelo que no mejora.
5. Explica qué necesitarías para afirmar que ya estás en el piso.
:::

::: hint {#ml-c2-pista-final-sesgo-y-varianza-1 of="ml-c2-ej-final-sesgo-y-varianza" title="Pista 1 · ¿Qué se mueve con n?"}
¿Cuál de los dos modelos cambió su $\mathrm{CV}_5$ al cuadruplicar los datos?
:::

::: hint {#ml-c2-pista-final-sesgo-y-varianza-2 of="ml-c2-ej-final-sesgo-y-varianza" title="Pista 2 · Revisa tu borrador"}
¿Tu recomendación se sostendría si el error que no baja fuera ruido y no sesgo?
:::

::: answer {#ml-c2-resp-final-sesgo-y-varianza of="ml-c2-ej-final-sesgo-y-varianza" title="Respuesta · Invertir donde los datos ayudan"}
**1. Diagnóstico.** A sobreajusta con 120 entregas: su brecha se cierra
al crecer la muestra. B se estanca con errores parecidos:
puede tener subajuste o ruido dominante.

**2. Términos.** En A, las curvas apuntan a varianza del ajuste.
En B, apuntan a sesgo o ruido; estas cifras no permiten separarlos.
Tampoco demuestran que la varianza de A supere al ruido en el error total.

**3. Compra.** Más datos ayudan a A en el tramo observado:
su CV baja de 11.8 a 9.2. Esperamos poca ganancia para B,
que permanece en 14.4. No extrapolaría esa mejora a 4000 entregas
sin revisar otra ampliación; las curvas no garantizan su magnitud.

**4. Alternativa.** Para B, probaría más capacidad o una mejor
representación $\phi$, comparadas mediante CV. Si mejora,
la recta estaba limitando el aprendizaje.

**5. Piso.** Haría falta una estimación del piso para estas variables
y pérdida. En datos reales no lo conocemos. Comparar familias más
flexibles con CV permite buscar mejoras; que ninguna mejore
no demuestra que ya alcanzamos el piso.
:::

**Punto de control:** deberías poder derivar la identidad, explicar qué baja
con más datos y distinguir señales de CV de comparaciones pareadas.

## Para profundizar

- Goodfellow y sus coautores, *Deep Learning*, §5.4: sesgo y varianza de estimadores; compara sus ecuaciones 5.53–5.54 con nuestra identidad. En §11.3, cómo decidir si hacen falta más datos.
- Domingos (2012), «A few useful things to know about machine learning», *Communications of the ACM* 55(10): la diana distingue desplazamiento y dispersión.

## Lo que hay que llevarse

El error esperado suma ruido + sesgo² + varianza. Con las entregas,
$N^\star=2$ da el menor total calculado en el simulador con $f$ conocida:
$9.0+0.90+0.99=10.89$. La estrella señala el óptimo teórico;
la CV de una muestra eligió $\widehat N=6$.

Más datos ayudan según qué parte domina. La recta se estanca en 13.8,
por encima del piso de 9.0; el grado 10 llega a 9.0 con 960 entregas.
La CV elige grado 3 con 30 datos y 10 con 960, medianas de 20 repeticiones.

Recuerda el recuadro «Un modelo exitoso»: comparación pareada favorable
en una reserva intacta, sin señal de mejora al flexibilizar, brecha chica
y prueba que imita la realidad.

Continúa con [[ml-clase-3-leer-el-error|Clase 3]].
