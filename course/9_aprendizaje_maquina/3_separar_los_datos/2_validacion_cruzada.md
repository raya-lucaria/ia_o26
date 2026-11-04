---
id: ml-validacion-cruzada
title: "Validación cruzada: elegir sin gastar la prueba"
nav_title: "Validación cruzada"
summary: "Cómo la validación cruzada reutiliza los datos de desarrollo para elegir hiperparámetros con media y error estándar, la regla de un error estándar, qué esconde un pliegue anómalo, cuándo estratificar y cómo medir con CV anidada todo el procedimiento de selección."
status: ready
estimated_time: 65m
tags: [aprendizaje-maquina, validacion-cruzada, hiperparametros, seleccion-de-modelos]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 04 · Validación cruzada.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)
>
> **[👉 Abrir `04_validacion_cruzada.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)**

# Validación cruzada: elegir sin gastar la prueba

**¿Cómo eliges el grado si una sola validación de doce entregas decide por suerte?**

Al terminar tendrás:

- **Una cuenta:** $\mathrm{CV}_k$, el promedio de validación cruzada, calculada a mano con su error estándar (EE).
- **Un presupuesto:** el costo en ajustes de comparar $M$ candidatos.
- **Dos elecciones:** el mínimo y la regla de un EE, con un orden de complejidad declarado.
- **Un diagnóstico:** qué investigar cuando un pliegue concentra el error.
- **Un criterio:** cuándo estratificar y cuándo medir la selección con CV anidada.

> **Lo que traes de [[ml-entrenamiento-y-prueba|Entrenamiento y prueba]]:**
>
> Los tres conjuntos: @ml-c2-def-tres-conjuntos.
>
> El error estándar de la prueba: @ml-c2-teo-prueba-insesgada.
>
> El optimismo al elegir con una estimación: @ml-c2-obs-optimismo-seleccion.

Seguimos prediciendo minutos de entrega con polinomios. La pérdida es cuadrática: las pérdidas promedio y sus EE se expresan en minutos cuadrados.
Conservamos $L$ para la pérdida promedio (@ml-c1-def-perdida-en-conjunto) y $R$ para el riesgo (@ml-c1-def-riesgo).
Esta $L$ no es un lenguaje ni una clase de complejidad, ni la longitud de una racha de Markov.

La lectura toma unos 30 minutos; explorar el notebook, unos 35. La **validación cruzada** (*cross-validation*, CV) reutiliza el desarrollo para elegir, mientras la prueba sigue cerrada.

## 1 · Rotar la validación

Cada fila es un ajuste completo. Sigue el triángulo: señala las entregas que esa vuelta debe predecir sin haberlas usado para ajustar.

::: figure {#ml-c2-pliegues title="Validación cruzada con cinco pliegues"}
![Una rejilla de cinco por cinco: cada fila es una vuelta de la validación cruzada. En la vuelta m, el pliegue m, en oro con triángulo, valida, y los otros cuatro, en cian con círculo, ajustan beta gorro sin el pliegue m. A la derecha de cada fila, la pérdida en su pliegue de validación; una llave junta las cinco en CV 5, su promedio. Aparte, debajo, la prueba, con cuadrado y candado: cerrada, nunca rota. Cada observación de desarrollo valida exactamente una vez.](../_assets/ml-c2-pliegues.svg)
:::

Cada observación de desarrollo valida exactamente una vez. Las demás vueltas la usan para ajustar. La prueba nunca rota.

**Piensa: Cuando una entrega valida en la vuelta 3, ¿pudo haber participado en el ajuste de esa misma vuelta?**

No: esa vuelta la aparta antes de ajustar. Para seguir el recorrido a mano, toma seis entregas, A a F.
Reparte los pliegues como {A, B}, {C, D}, {E, F}. Cada fila rehace el ajuste desde sus datos.

::: table {#ml-c2-tab-traza-seis}
| Vuelta | Con qué se ajusta | A quién predice |
|---|---|---|
| 1 | C, D, E, F | A, B |
| 2 | A, B, E, F | C, D |
| 3 | A, B, C, D | E, F |
:::

Sigue a C: ¿en qué vuelta recibe su única predicción fuera de pliegue, y qué entregas ajustaron el modelo que la predijo?

En la vuelta 2; A, B, E, F ajustaron ese modelo. C sí ayudó a ajustar otros modelos, pero no el que la evaluó.

Ahora promedia las pérdidas de las vueltas. Esa es la cuenta del algoritmo 5.1 de [Goodfellow, Bengio y Courville](https://www.deeplearningbook.org/contents/ml.html).
$k$ cuenta pliegues; en Markov contaba estados, en juegos simulaciones y en la unidad 6 era índice de clase.
$m$ señala el pliegue; antes nombraba aristas, profundidad o tiempo medio de llegada.
$M$ cuenta candidatos, como en la unidad 6; no es la escala de finales ni una máquina de Turing.

::: definition {#ml-c2-def-validacion-cruzada title="Validación cruzada de k pliegues"}
Parte los datos de desarrollo $\mathcal D_{\text{ent}}\cup\mathcal D_{\text{val}}$ en $k$ pliegues disjuntos $\mathcal D_1,\dots,\mathcal D_k$ de tamaños casi iguales.
Para $m=1,\dots,k$, ajusta $\widehat\beta^{(-m)}$ con todos los pliegues salvo $\mathcal D_m$ y evalúalo en $\mathcal D_m$.
El superíndice $(-m)$ se lee «sin el pliegue $m$». La estimación es

$$\mathrm{CV}_k=\frac1k\sum_{m=1}^{k}L_{\mathcal D_m}\bigl(\widehat\beta^{(-m)}\bigr),$$

y su error estándar entre pliegues,

$$\mathrm{EE}_{\mathrm{CV}}=\frac{1}{\sqrt k}\sqrt{\frac{1}{k-1}\sum_{m=1}^{k}\Bigl(L_{\mathcal D_m}\bigl(\widehat\beta^{(-m)}\bigr)-\mathrm{CV}_k\Bigr)^2}.$$

Primero calculas la desviación de las pérdidas entre vueltas; luego divides entre $\sqrt k$.
Para elegir entre $M$ candidatos se calcula una $\mathrm{CV}_k$ por candidato: $M\cdot k$ ajustes, más uno.
Ese último ajuste usa todo el desarrollo para el candidato elegido. La prueba no entra en ningún ajuste ni en ninguna elección.

$\mathrm{CV}_k$ estima el error **del procedimiento** entrenado con $(n_{\text{ent}}+n_{\text{val}})(k-1)/k$ datos (aproximadamente, si los pliegues difieren de tamaño), promediado sobre entrenamientos, $E_{\mathcal D}[R(\widehat\beta)]$, más que el $R(\widehat\beta)$ del modelo final; su $\mathrm{EE}$ entre pliegues es aproximado, porque los pliegues no son independientes.

Esa distinción la estudian [Bates, Hastie y Tibshirani](https://arxiv.org/abs/2104.00673).
Además, esa misma dependencia impide usar las pérdidas fuera de pliegue como si fueran independientes para comparar dos modelos: con CV, la comparación es descriptiva.
:::

::: remark {#ml-c2-obs-ee-de-cv title="Las barras de la CV son aproximadas"}
Los $k$ ajustes comparten buena parte de sus datos. Sus pérdidas no son independientes.
No existe un estimador universal insesgado de la varianza de $\mathrm{CV}_k$: [Bengio y Grandvalet](https://www.jmlr.org/papers/v5/grandvalet04a.html) demuestran ese límite.

Con el proceso de las entregas y grado 4, la desviación real de $\mathrm{CV}_5$ entre 200 muestras es 3.1.
El EE promedio reportado es 2.2: aquí subestima la variación. Usa las barras como guía, no como intervalo exacto.

Recuerda: comparar dos modelos con CV es descriptivo; la clase 3 dice por qué.
:::

Los pliegues hacen el papel de validación dentro del desarrollo. $n_{\text{ent}}$ sigue contando solo $\mathcal D_{\text{ent}}$.
Con cinco vueltas, cada ajuste usa aproximadamente cuatro quintas partes del desarrollo. **La CV elige y la prueba reporta.**

::: exercise {#ml-c2-ej-cinco-pliegues title="Calcula el promedio y su EE"}
Cinco pliegues dan $L_{\mathcal D_m}=9.2,\ 9.0,\ 9.1,\ 8.7,\ 8.8$, en minutos cuadrados.
(a) Calcula $\mathrm{CV}_5$. (b) Calcula $\mathrm{EE}_{\mathrm{CV}}$.
:::
::: hint {#ml-c2-pista-cinco-pliegues-1 of="ml-c2-ej-cinco-pliegues" title="Pista 1 · La dispersión"}
¿Con qué divisor va la desviación de cinco números?
:::
::: answer {#ml-c2-resp-cinco-pliegues of="ml-c2-ej-cinco-pliegues" title="Respuesta · Promediar las vueltas"}
**(a)** $\mathrm{CV}_5=8.96$. Las desviaciones respecto de esa media son $0.24,0.04,0.14,-0.26,-0.16$.

**(b)** Sus cuadrados suman $0.172$. La desviación es $s=\sqrt{0.172/4}\approx0.207$; por tanto, $\mathrm{EE}_{\mathrm{CV}}\approx0.093$.
El divisor de la varianza muestral es cuatro; el EE divide después la desviación entre $\sqrt5$.
:::

> [!TIP] **Míralo correr: bloque 1 · Los pliegues, dibujados**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## 2 · Elegir con una CV por candidato

Ya mediste un grado. Para elegir, repite el recorrido: cada capa es una CV completa con un grado fijo.

::: figure {#ml-c2-costo-cv title="Lo que cuesta elegir con validación cruzada"}
![Tres rejillas de cinco por cinco apiladas y desplazadas, una por candidato: grado 2, grado 4 y grado 8; cada una es una validación cruzada completa. Un contador dice M por k más 1 igual a 3 por 5 más 1, 16 ajustes: 3 candidatos por 5 pliegues, más 1. Una flecha lleva al más 1: el reajuste del elegido con todo el desarrollo, entrenamiento unión validación. Al pie: con 13 grados y 5 pliegues, 13 por 5 más 1, 66 ajustes.](../_assets/ml-c2-costo-cv.svg)
:::

El costo crece con candidatos por pliegues. La flecha final importa: ningún modelo de pliegue es el que usarás al final.

**Piensa: ¿Cuántos modelos entrenas para elegir entre 13 grados con 5 pliegues, y cuál de todos ellos usas al final?**

Haces $13\cdot5+1=66$ ajustes. Usas el último, reajustado con todo el desarrollo después de elegir el grado.
Conserva la distinción de @ml-c1-def-param-hiper: ajustas coeficientes para cada candidato y eliges el grado comparando estimaciones.

$$\widehat N\in\operatorname*{arg\,min}_{N\in\{0,\dots,N_{\max}\}}\mathrm{CV}_k(N),$$

con empate, el más simple: el menor $N$.

La CV mide; el $\arg\min$ elige. Limitar el grado restringe la capacidad (@ml-c1-def-capacidad-como-restriccion).
Cada ajuste sigue siendo lineal en parámetros (@ml-c1-def-modelo-lineal), aunque la curva se doble.

Con un hiperparámetro continuo puedes explorar una rejilla en escala logarítmica: separas candidatos por factores, no por incrementos iguales.
Una búsqueda aleatoria sortea candidatos en el rango declarado; una rejilla fija sus combinaciones.
Ambas necesitan presupuesto. La elección entre una validación y CV también depende de cuánto puedes esperar y guardar.

::: table {#ml-c2-tab-cuando-cual title="Cuándo una validación y cuándo validación cruzada"}
| Datos | Cómputo, tiempo y memoria | Qué usar | Por qué |
|---|---|---|---|
| Muchos | Poco cómputo | Una validación aparte | Si ya es estable, CV multiplica el costo por $k$. |
| Muchos | Mucho cómputo | CV con $k$ chico (3–5) o validación | Puedes ganar poco con CV. |
| Pocos | Poco cómputo | CV con $k=5$ | Una validación chica puede decidir por suerte. |
| Pocos | Mucho cómputo | CV con $k=10$, repetida, o anidada para reportar | Cada observación cuenta; la anidada mide el procedimiento. |
| Cualquiera | Mucho cómputo, pero poco tiempo o poca memoria | CV en paralelo si los ajustes caben; si no, una validación | Repartir los ajustes ahorra tiempo, pero necesita memoria. |
:::

En el experimento de 200 muestras, la validación de doce entregas tiene desviación 4.9; la CV sobre 48, 3.1.
Sus EE promedio son 4.4 y 2.2, respectivamente. Aquí la CV varía menos; no es una garantía para cualquier problema.
El bloque 3 permite comparar esas distribuciones. Aún falta decidir cuánto peso dar a una pequeña diferencia entre medias.

::: exercise {#ml-c2-ej-costo title="Cuenta los ajustes"}
Comparas 13 grados. (a) ¿Cuántos ajustes haces con $k=5$?
(b) ¿Y con dejar-uno-fuera, que usa cada observación como un pliegue, y $n=60$?
Incluye el reajuste final.
:::
::: hint {#ml-c2-pista-costo-1 of="ml-c2-ej-costo" title="Pista 1 · El ajuste que falta"}
¿Cuántas veces ajusta cada candidato, y qué falta al final?
:::
::: answer {#ml-c2-resp-costo of="ml-c2-ej-costo" title="Respuesta · Candidatos por vueltas, más uno"}
**(a)** $13\cdot5+1=66$.

**(b)** $13\cdot60+1=781$. Cada candidato requiere una vuelta por observación; después reajustas solo el elegido.
:::

> [!TIP] **Míralo correr: bloques 2 y 3 · CV contra el grado y contra una sola validación**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## 3 · Leer las barras y la regla de un EE

Cada triángulo es el promedio de cinco pliegues; la barra, su error estándar aproximado.
El eje horizontal recorre grados; el vertical mide pérdida cuadrática.

::: figure {#ml-c2-cv-capacidad title="La validación cruzada contra el grado"}
![CV 5 con barras de ±1 EE contra el grado N de 0 a 12. El mínimo está en N = 6, con CV 9.69 ± 1.33; el umbral mínimo más un EE es 11.02 y la regla de un EE también elige N = 6. L_ent baja siempre, de 51.2 a 4.5. El riesgo R de cada grado, que solo existe en el simulador, es mínimo en N = 4 (11.0) y vale 27.3 en el elegido. Piso 9.0; benchmark, la media de entrenamiento, 51.4.](../_assets/ml-c2-cv-capacidad.svg)
:::

La raya-punto muestra un punto de comparación (*benchmark*): la media de entrenamiento como punto de comparación; la clase 3 lo define.
La curva de riesgo solo existe en el simulador. El piso de esta pérdida es $R_{\text{Bayes}}=\sigma_\varepsilon^2=9.0$; $\varepsilon$ conserva su sentido de ruido.

**Piensa: Si dos grados tienen $\mathrm{CV}_5$ casi iguales, ¿estás obligado a quedarte con el que salió más bajo?**

No: puedes declarar una preferencia por simplicidad antes de medir.
Aquí el mínimo elige $N=6$, con $9.69\pm1.33$. Sumar su EE fija una tolerancia de 11.02.
La regla de un EE elige el primer grado, de simple a complejo, cuyo triángulo no supera ese umbral.
Que su barra lo cruce no basta: comparas la media.

::: definition {#ml-c2-def-regla-un-ee title="La regla de un error estándar"}
Antes de medir, ordena los candidatos de más simple a más complejo.
Para el grado, usa $N$ creciente; para regularización, de más fuerte a más débil.
Sea $\widehat N_{\min}$ el candidato con menor $\mathrm{CV}_k$.
La regla elige el primero de la lista ordenada que cumpla

$$\mathrm{CV}_k(N)\le\mathrm{CV}_k\bigl(\widehat N_{\min}\bigr)+\mathrm{EE}_{\mathrm{CV}}\bigl(\widehat N_{\min}\bigr).$$

«Más simple» lo da el orden declarado antes de medir, no el valor numérico del hiperparámetro.
:::

El grado 2 queda fuera: su media 11.37 supera 11.02, aunque su EE sea 1.45.
El primero que entra es el 6. En esta semilla ambas reglas coinciden; la regla no siempre baja el grado.

La caída de $L_{\text{ent}}$ recuerda @ml-c1-teo-optimismo-entrenamiento.
La CV primero baja y luego sube; la página siguiente de la clase explica esa forma.
El elegido reajustado tiene $R=27.3$, frente al mejor $R=11.0$ del grado 4, que la elección no vio.
El grado 6 se dobla en los bordes. La brecha de @ml-c1-def-brecha sigue siendo $R-L_{\text{ent}}$, no CV menos entrenamiento.

¿Qué podemos hacer con los intervalos de la gráfica? Usarlos como tolerancia orientativa; no prueban igualdad de riesgos.
Los triángulos bajo el benchmark son una señal descriptiva. Sus pérdidas dependen entre sí y elegiste el grado con ellas.
La confirmación requiere la prueba, abierta una vez, y la diferencia pareada de pérdidas de los modelos ya fijados.

> [!WARNING]
> Lectura equivocada: «La regla de un EE prueba que los dos modelos son igual de buenos».
>
> Lectura correcta: **La regla prefiere el modelo más simple dentro de una tolerancia; no demuestra que sus riesgos sean iguales.**

::: exercise {#ml-c2-ej-elige-un-ee title="Elige por la media"}
Estos datos son inventados para practicar. El orden de simplicidad es $N$ creciente.

| Grado | CV | EE |
|---|---:|---:|
| 1 | 14.0 | 0.6 |
| 2 | 10.2 | 0.5 |
| 3 | 9.6 | 0.4 |
| 4 | 9.5 | 0.4 |
| 5 | 9.8 | 0.5 |

(a) ¿Qué elige el mínimo? (b) ¿Qué elige la regla de un EE? Justifica por qué entra o queda fuera el grado 2.
:::
::: hint {#ml-c2-pista-elige-un-ee-1 of="ml-c2-ej-elige-un-ee" title="Pista 1 · Leer el umbral"}
¿Qué candidato fija la altura del umbral, y comparas con él la media o la barra?
:::
::: answer {#ml-c2-resp-elige-un-ee of="ml-c2-ej-elige-un-ee" title="Respuesta · Una barra que cruza no basta"}
**(a)** El mínimo elige $N=4$; el umbral es $9.5+0.4=9.9$.

**(b)** La regla elige $N=3$, cuya media es 9.6.
El grado 2 no entra: su barra baja a 9.7, pero su media 10.2 supera 9.9.
El grado 3 es el primero cuya media no supera el umbral.
:::

> [!TIP] **Míralo correr: bloque 2 · CV contra el grado, con barras**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## 4 · Mirar dentro de los pliegues

La media decidió, pero puede esconder fragilidad. Ahora cada triángulo es un pliegue, no un promedio; la altura mide pérdida en escala logarítmica.

::: figure {#ml-c2-pliegue-anomalo title="Un pliegue que carga casi todo el error"}
![Caso 16, cinco pliegues, un triángulo por pliegue y una raya en la media, para los grados 1, 4 y 8, en escala logarítmica. Con grado 1 los cinco quedan juntos: el mayor es 1.39 veces la mediana de los otros. Con grado 8, los pliegues 2 y 3, los que traen una entrega lejana, se disparan: el pliegue 3 da 88482, miles de veces la mediana de los otros.](../_assets/ml-c2-pliegue-anomalo.svg)
:::

El promedio esconde qué pliegues cargan el error. En este caso son dos: los pliegues que traen una entrega lejana.

**Piensa: ¿Qué puede hacer que un solo pliegue tenga diez veces más error que los otros, y solo en el grado alto?**

Puede traer distancias fuera del intervalo con que se ajustó ese modelo.
En el caso 16, grado 1 da $13.8,16.1,13.0,11.3,18.6$; el máximo es 1.39 veces la mediana de los otros.
Grado 8 da $13,5991,88482,8,5$. Las entregas lejanas están en los pliegues 2 y 3: el grado alto extrapola y falla en ambos.

Puedes investigar otros estadísticos por pliegue. El residual con signo es $y_i-\widehat y_i$, calculado con $\widehat\beta^{(-m)}$.
Para la proporción de errores grandes, fija antes un umbral en minutos.
Usa pérdida 1 si $\lvert y_i-\widehat y_i\rvert$ lo supera y 0 si no; después aplica el mismo promedio de CV.

La varianza del residual necesita otra cuenta: centra los residuales en la media de su pliegue.
Suma sus cuadrados centrados y divide entre el tamaño del pliegue menos uno.
Luego promedia esas varianzas y calcula el mismo EE entre pliegues.
No es un promedio de pérdidas individuales; en `validacion_cruzada` lo pide `estadistico`, no `elegir`.

Una media menor con mucha dispersión puede revelar fragilidad. Reporta ambas e investiga la composición del pliegue antes de decidir.

> [!WARNING]
> Lectura equivocada: «Quito el pliegue raro y repito».
>
> Lectura correcta: **Si esos casos pueden llegar al despliegue, quitar el pliegue esconde justo el riesgo que necesitas medir.**

::: exercise {#ml-c2-ej-pliegue-raro title="Investiga antes de borrar"}
En otro reparto, con $N=1$ los cinco pliegues dan errores parecidos; con $N=8$, el pliegue 2 da diez veces más.
(a) ¿Qué buscas en el pliegue 2 antes de decidir? (b) ¿Qué harías si contiene los extremos de distancia?
:::
::: hint {#ml-c2-pista-pliegue-raro-1 of="ml-c2-ej-pliegue-raro" title="Pista 1 · Localizar las entregas"}
¿Dónde caen, en el eje de la distancia, las entregas de ese pliegue?
:::
::: answer {#ml-c2-resp-pliegue-raro of="ml-c2-ej-pliegue-raro" title="Respuesta · Revisar la extrapolación"}
**(a)** Busca si trae los extremos de distancia, ausentes del ajuste que lo predice.

**(b)** Ahí el grado 8 extrapola. La CV avisa que falla fuera del centro de los datos.
Puedes preferir el grado bajo o ampliar los datos en esa zona; borrar el pliegue oculta el problema.
:::

> [!TIP] **Míralo correr: bloque 4 · Mirar dentro de los pliegues**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## 5 · Estratificar cuando una clase es rara

La composición también importa al clasificar. Cambiamos a un juguete de clasificación porque los tiempos de entrega no muestran una clase rara.
Cada caja es un pliegue; cada marca, un positivo.

::: figure {#ml-c2-estratificada title="Pliegues al azar y estratificados"}
![Sesenta casos con 6 positivos en cinco pliegues. Arriba, una partición al azar: positivos por pliegue 2, 2, 1, 0, 1. Abajo, la estratificada: 1, 1, 1, 1, 2. En 1000 particiones de cada método, al azar 88 % dejan algún pliegue sin positivos; estratificando, 0 %.](../_assets/ml-c2-estratificada.svg)
:::

Al azar puede faltar la clase rara en un pliegue. Estratificar reparte sus casos: aquí cada pliegue recibe uno o dos positivos.

**Piensa: Con cinco pliegues y una clase que tiene solo tres casos, ¿cuántos pliegues pueden validar esa clase, estratifiques o no?**

A lo más tres: cada caso pertenece a un único pliegue. Ninguna forma de repartir puede llenar los cinco.

::: definition {#ml-c2-def-estratificada title="Separación y validación cruzada estratificadas"}
Una separación o partición es estratificada si conserva la proporción de cada clase tanto como permiten los conteos.
Divide el número de casos de una clase entre $k$.
Cada pliegue recibe ese cociente redondeado hacia abajo o hacia arriba.
Con seis positivos y cinco pliegues, recibe uno o dos.
:::

Primero decide cómo simularás los casos nuevos: primero la estructura del despliegue (@ml-c2-def-simulacro); dentro de ella, estratifica cuando sea compatible.
No rompas una separación por tiempo o grupos para conservar proporciones.
La [documentación de scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html) distingue estas necesidades.

Con seis positivos, en 1000 particiones por método, algún pliegue queda sin positivos el 88 % de las veces al azar.
Estratificando ocurre el 0 %. Son cifras del experimento, no probabilidades universales.
Si hay menos casos que pliegues, baja $k$ o reúne más datos.
Estratificar tampoco corrige otro despliegue ni observaciones dependientes.

::: exercise {#ml-c2-ej-tres-positivos title="Reparte tres positivos"}
Tienes $k=5$ y tres positivos.
(a) ¿Cuántos pliegues tienen al menos uno si estratificas?
(b) ¿Y en el mejor caso al azar? (c) ¿Qué cambia con $k=3$?
:::
::: hint {#ml-c2-pista-tres-positivos-1 of="ml-c2-ej-tres-positivos" title="Pista 1 · Un lugar por caso"}
¿Puede un positivo estar en dos pliegues?
:::
::: answer {#ml-c2-resp-tres-positivos of="ml-c2-ej-tres-positivos" title="Respuesta · No alcanzan para cinco"}
**(a)** Estratificar garantiza tres pliegues con un positivo.

**(b)** Al azar, a lo más tres; podrían ser menos. Por el principio del palomar, siempre quedan al menos dos vacíos.

**(c)** Con $k=3$, estratificar coloca uno en cada pliegue.
:::

> [!TIP] **Míralo correr: bloque 5 · Estratificar**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## 6 · Medir al que elige: la CV anidada

Ya cuidaste los pliegues; falta medir la elección misma. Cada caja grande es una vuelta externa; lo de adentro no ve su pliegue externo.

::: figure {#ml-c2-anidada title="Afuera se estima; adentro se elige"}
![Validación cruzada anidada. Arriba, cinco pliegues externos; en la vuelta externa 2, el pliegue externo 2 mide. Dentro de esa vuelta, una validación cruzada interna con los otros cuatro pliegues, que no ve el pliegue externo 2, elige el grado N gorro 2 y lo reajusta con los cuatro; una flecha lleva al elegido al pliegue externo, que lo evalúa. Afuera, la pérdida del elegido en cada pliegue externo se promedia en las cinco vueltas. Rótulo: afuera se estima, adentro se elige. La prueba sigue cerrada.](../_assets/ml-c2-anidada.svg)
:::

El número de afuera mide todo el procedimiento, incluida la elección.

**Piensa: Si anuncias la $\mathrm{CV}_5$ del grado que ganó la CV, ¿no estás repitiendo el engaño de elegir con la prueba?**

Sí: escogiste el mínimo entre estimaciones ruidosas. Es el optimismo por selección de @ml-c2-obs-optimismo-seleccion.
Para medirlo, la elección debe ocurrir entera dentro de cada vuelta externa.

::: definition {#ml-c2-def-cv-anidada title="Validación cruzada anidada"}
Parte el desarrollo en $k$ pliegues externos.
En cada vuelta externa $m$, elige el hiperparámetro con una $\mathrm{CV}_k$ interna usando solo los demás pliegues externos.
Reajusta con ellos y evalúa en el pliegue externo $m$.

El promedio externo estima el riesgo esperado del procedimiento entrenado con $(k-1)/k$ del desarrollo, promediado sobre entrenamientos.
No estima el $R$ del modelo final, reajustado con todo el desarrollo, que suele ser algo menor.
Con $k$ pliegues adentro y afuera cuesta $k\,(M\cdot k+1)$ ajustes: cada vuelta externa paga una selección y un reajuste.
:::

Separa dos efectos: elegir el mínimo empuja la estimación hacia abajo; entrenar con menos datos suele empujarla hacia arriba.
Compara al mismo tamaño. En 30 repeticiones con grados 0–8, la CV ganadora promedia $10.0\pm0.5$ y la anidada $11.8\pm0.7$.
El riesgo del procedimiento replicado a cuatro quintas partes del desarrollo es $12.7\pm1.1$.

Aparte, el riesgo del modelo final con todo el desarrollo es $11.4\pm0.6$. Cada $\pm$ indica un EE de Monte Carlo entre repeticiones.

Con una prueba final bien hecha, la anidada no es obligatoria: la prueba mide el modelo final.
La anidada permite evaluar la selección cuando no alcanza para reservar una prueba aparte.

::: remark {#ml-c2-obs-variantes title="Otras formas de rotar"}
Dejar-uno-fuera tiene casi ningún sesgo por tamaño, pero cuesta muchos ajustes y sus cifras están muy correlacionadas.
La CV repetida rehace la partición con otras semillas y promedia para reducir el ruido de la partición.
Las versiones temporal y por grupos respetan el despliegue; llegan en la clase 5.
:::

::: exercise {#ml-c2-ej-anidada-costo title="Cuenta las vueltas internas"}
Comparas 13 candidatos con cinco pliegues adentro y afuera.
¿Cuántos ajustes cuesta evaluar el procedimiento completo con CV anidada?
:::
::: hint {#ml-c2-pista-anidada-costo-1 of="ml-c2-ej-anidada-costo" title="Pista 1 · Mirar dentro de cada caja"}
¿Cuántas CV internas completas hay, y qué cuesta cada una con su reajuste?
:::
::: answer {#ml-c2-resp-anidada-costo of="ml-c2-ej-anidada-costo" title="Respuesta · Repetir la selección completa"}
$5\cdot(13\cdot5+1)=330$ ajustes. Cada vuelta externa selecciona con cinco pliegues internos y reajusta su elegido antes de evaluarlo afuera.
:::

> [!TIP] **Míralo correr: bloque 6 · La CV anidada**
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/04_validacion_cruzada.ipynb)

## Ejercicio final

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#ml-c2-ej-final-validacion-cruzada title="Calcula, elige y cuenta"}
Tres pliegues de igual tamaño dan pérdidas $4,\ 5,\ 6$ para el grado 1 y $4.2,\ 4.8,\ 5.4$ para el grado 5.
Son datos inventados para el ejercicio, en minutos cuadrados. No hay más candidatos.
Declaraste el orden de simple a complejo: grado 1, grado 5, y usarás la regla de un EE.

La idea nueva es sostener una regla declarada antes de medir, aunque no elija la media más baja.
La prueba permanece cerrada y es independiente del desarrollo.

1. Calcula $\mathrm{CV}_3$ de cada grado y $\mathrm{EE}_{\mathrm{CV}}$ del ganador por el mínimo.
2. Indica qué elige el mínimo y qué elige la regla de un EE. Justifica con las medias y el umbral.
3. Cuenta los ajustes necesarios para comparar los dos candidatos y reajustar el elegido.
4. Explica qué harías para reportar el error del elegido y con qué incertidumbre.
5. Explica por qué no puedes cambiar de regla después de ver la prueba.
:::
::: hint {#ml-c2-pista-final-validacion-cruzada-1 of="ml-c2-ej-final-validacion-cruzada" title="Pista 1 · ¿Qué fija el umbral?"}
¿Qué candidato decide la altura de la tolerancia, y con qué EE?
:::
::: hint {#ml-c2-pista-final-validacion-cruzada-2 of="ml-c2-ej-final-validacion-cruzada" title="Pista 2 · Revisa tu borrador"}
¿Qué candidatos quedan por debajo de esa altura, y cuál va primero en el orden que declaraste?
:::
::: answer {#ml-c2-resp-final-validacion-cruzada of="ml-c2-ej-final-validacion-cruzada" title="Respuesta · Elegir sin abrir la prueba"}
**1.** Las medias son $\mathrm{CV}_3=5$ y $4.8$.
Para el grado 5, la desviación es $\sqrt{(0.36+0+0.36)/2}=0.6$; su $\mathrm{EE}_{\mathrm{CV}}=0.6/\sqrt3\approx0.346$.

**2.** El mínimo elige grado 5. El umbral llega a $\approx5.146$.
La media del grado 1 cumple $5\le5.146$ y ese grado va primero: la regla de un EE elige grado 1.

**3.** Son $2\cdot3+1=7$ ajustes, incluido el reajuste del elegido.

**4.** Reajusta con todo el desarrollo y abre la prueba una vez.
Reporta $L_{\text{prueba}}\pm2\,\mathrm{EE}$, como resumen aproximado bajo las condiciones de @ml-c2-teo-prueba-insesgada.

**5.** Cambiar la regla tras ver la prueba sería elegir con ella: @ml-c2-obs-optimismo-seleccion.
Dejaría de ser una evaluación independiente del desarrollo.
:::

**Punto de control:** deberías poder calcular $\mathrm{CV}_k$ y su EE, elegir con la regla de un EE con un orden declarado, y decir cuántos ajustes cuesta.

## Para profundizar

- Goodfellow, Bengio y Courville, [§5.3.1 y algoritmo 5.1](https://www.deeplearningbook.org/contents/ml.html): cómo rotar los pliegues.
- Bates, Hastie y Tibshirani, [«Cross-validation: what does it estimate and how well does it do it?»](https://arxiv.org/abs/2104.00673): distinguir el procedimiento del modelo final.
- Bengio y Grandvalet, [«No unbiased estimator of the variance of K-fold cross-validation»](https://www.jmlr.org/papers/v5/grandvalet04a.html): el límite de las barras.
- Varma y Simon, [«Bias in error estimation when using cross-validation for model selection»](https://link.springer.com/article/10.1186/1471-2105-7-91): el optimismo al reportar la CV del ganador.
- Hastie, Tibshirani y Friedman, [*The Elements of Statistical Learning*](https://hastie.su.domains/Papers/ESLII.pdf), segunda edición, §7.10: validación cruzada y regla de un EE.

## Lo que hay que llevarse

Elegir entre 13 grados con cinco pliegues cuesta $M\cdot k+1=66$ ajustes.
En las entregas, ambas reglas eligen grado 6: $\mathrm{CV}_5=9.69\pm1.33$, con umbral 11.02.
La media del grado 2, 11.37, queda fuera aunque su barra cruce el umbral.

Una vez fijado y reajustado el elegido, las doce entregas de prueba reportan $112.5\pm147.0$.
El benchmark en esa misma prueba da $82.3\pm40.3$; ambas cifras llevan $\pm2\,\mathrm{EE}$.
Una entrega en el borde vuelve enorme y ruidosa la pérdida del elegido. Insesgada no significa exacta: doce entregas son pocas para precisar este riesgo.
En el simulador, $R=27.3$ para el elegido, frente a 11.0 del grado 4; el benchmark tiene riesgo 51.4.

El EE de CV también requiere cuidado: en 200 muestras, reporta 2.2 en promedio ante una desviación real de 3.1.
Con seis positivos y cinco pliegues, el azar deja algún pliegue sin positivos el 88 % de las veces; estratificar, el 0 %.
Con tres positivos, siempre quedan al menos dos pliegues vacíos, estratifiques o no.

Continúa con [[ml-tarea-2|Tarea 2]].
