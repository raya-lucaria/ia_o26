---
id: ml-sesgo-y-varianza
title: "Sesgo y varianza: de dónde sale el error"
nav_title: "Sesgo y varianza"
summary: "El error esperado se separa en ruido, sesgo al cuadrado y varianza: cien entrenamientos para verlo, una demostración y tres predicciones para calcularlo a mano."
status: ready
estimated_time: 20m
tags: [aprendizaje-maquina, sesgo, varianza, curva-de-aprendizaje, sobreajuste, subajuste]
---

# Sesgo y varianza: de dónde sale el error

**Si repites el mismo procedimiento con otra muestra, ¿por qué cambia la predicción, y qué parte de tu error es culpa de eso?**

Quieres predecir cuánto tardará una entrega. Ya separaste datos para medir
el error; ahora quieres explicar de dónde sale. Imagina repetir el
entrenamiento con otras 36 entregas del mismo proceso. Conservas el método
y el grado, pero recibes otras distancias y otros tiempos. La curva puede
moverse aunque hayas hecho todo igual.

Al terminar tendrás:

- **Identidad:** habrás derivado ruido + sesgo² + varianza en un punto.
- **Cálculo:** habrás obtenido sesgo y varianza a mano para tres predicciones.

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
![Tres paneles con 100 ajustes cada uno, uno por muestra del mismo proceso, su promedio y la verdadera E[y | x]. Grado 1: las rectas casi no se separan (desviación 0.9 en x = 5) pero su promedio se aleja de la curva. Grado 4: abanico angosto (desviación 1.1) y promedio pegado a la curva. Grado 12: el promedio sigue la curva, pero cada ajuste se sacude, sobre todo en los bordes (desviación 3.5 en x = 5).](../_assets/ml-c2-abanico.svg)
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

::: exercise {#ml-c2-ej-que-cambia}
Sin mirar la figura: con $n=36$, ¿qué abanico es más ancho en los extremos,
el de grado 2 o el de grado 10, y por qué?
:::

::: hint {#ml-c2-pista-que-cambia-1 of="ml-c2-ej-que-cambia" title="Pista 1"}
¿Cuántos coeficientes tiene que estimar cada uno con las mismas 36 entregas?
:::

::: answer {#ml-c2-resp-que-cambia of="ml-c2-ej-que-cambia" title="Respuesta"}
Esperamos un abanico más ancho para el grado 10. Estima más coeficientes
con los mismos datos y el ajuste resulta más sensible a la muestra.
Esa sensibilidad se nota especialmente en los extremos, donde hay menos
puntos que sujeten la curva. Es la comparación de este experimento,
no una ley para cualquier procedimiento.
:::

## 2 · Separar el error en tres partes

Fijemos la distancia para separar desplazamiento y dispersión.
Cada marca es la predicción de una muestra en el mismo $x_0$.
El eje del valor mide minutos; el apilamiento solo permite distinguir marcas.

::: figure {#ml-c2-diana title="La diana en x = 5"}
![Predicciones en x = 5 de 100 ajustes, cada uno con otra muestra, junto a E[y | x = 5] = 31.5. Grado 1: las cruces se agrupan apretadas (desviación 0.9) pero corridas 1.5 minutos del valor verdadero. Grado 12: centradas (sesgo −0.5) pero dispersas (desviación 3.5). Eje fijo de 15 a 55 minutos; ninguna predicción queda fuera.](../_assets/ml-c2-diana.svg)
:::

Sesgo es la distancia con signo de la línea discontinua a la verde;
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

::: exercise {#ml-c2-ej-tres-predicciones}
En un $x$ fijo, $f(x)=11$. Un procedimiento predice $8$, $10$ o $12$,
cada una con probabilidad $1/3$ según la muestra, y el ruido nuevo tiene varianza 4.
Calcula sesgo, varianza y error cuadrático esperado.
:::

::: hint {#ml-c2-pista-tres-predicciones-1 of="ml-c2-ej-tres-predicciones" title="Pista 1"}
¿Alrededor de qué número se mide la varianza: de $f(x)$ o del promedio de las predicciones?
:::

::: answer {#ml-c2-resp-tres-predicciones of="ml-c2-ej-tres-predicciones" title="Respuesta"}
El promedio es 10. El sesgo es $-1$: el procedimiento predice, en promedio,
por debajo de $f(x)=11$.
La varianza mide las desviaciones cuadráticas respecto de 10:

$$\frac{4+0+4}{3}=\frac83.$$

Aplicando @ml-c2-teo-sesgo-varianza, el error cuadrático esperado es

$$4+1+\frac83=\frac{23}{3}\approx7.67.$$

El sesgo puede ser negativo; su contribución al error es su cuadrado.
:::

**Punto de control:** deberías poder derivar la identidad, explicar por qué
desaparecen los productos cruzados y distinguir los dos promedios.
$E_{\mathcal D}$ recorre entrenamientos; $E_x$ recorre entradas del despliegue.

## Para profundizar

- Goodfellow y sus coautores, *Deep Learning*, §5.4: sesgo y varianza de estimadores; compara sus ecuaciones 5.53–5.54 con nuestra identidad.
- Domingos (2012), «A few useful things to know about machine learning», *Communications of the ACM* 55(10): la diana distingue desplazamiento y dispersión.

## Lo que hay que llevarse

Con pérdida cuadrática, el error esperado suma ruido, sesgo al cuadrado y
varianza. En la diana, el grado 1 tiene sesgo 1.5 y desviación 0.9 minutos;
el grado 12 tiene sesgo $-0.5$ y desviación 3.5. Son estimaciones con
100 muestras en $x_0=5$, no garantías para cada ajuste.

En el cálculo a mano, el sesgo es $-1$, la varianza $8/3$ y el total
$23/3$. Saber el promedio verdadero elimina el sesgo y la varianza del
ajuste; queda el ruido de la entrega nueva.

Continúa con [[ml-clase-3-leer-el-error|Clase 3]].
