---
id: ml-polinomios-y-capacidad
title: "Polinomios, capacidad y supuestos"
nav_title: "Polinomios y capacidad"
summary: "Taylor y Stone–Weierstrass: aproximar no es aprender. La capacidad, la brecha entre el error de entrenamiento y el riesgo, por qué el entrenamiento no puede elegir el grado, extrapolar y no free lunch."
status: ready
estimated_time: 65m
tags: [aprendizaje-maquina, capacidad, brecha, hiperparametro, extrapolar, no-free-lunch]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 02 · Polinomios, capacidad y supuestos.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)
>
> **[👉 Abrir `02_polinomios_y_capacidad.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)**

# Polinomios, capacidad y supuestos

**Si los polinomios pueden aproximar casi cualquier curva, ¿por qué no usar siempre el mayor grado?**

~35 min de lectura y ~30 con el notebook.

Al terminar tendrás:

- **Una distinción:** distinguirás aproximar de aprender.
- **Una lectura de la capacidad:** leerás su curva y señalarás la brecha.
- **Una demostración:** demostrarás por qué el entrenamiento miente a tu favor.
- **Un criterio de elección:** dirás qué es un hiperparámetro y por qué $L_{\text{ent}}$ no lo puede elegir.
- **Un límite general:** enunciarás no free lunch y explicarás lo que implica.

> [!TIP]
> **Míralo correr: polinomios y capacidad**
>
> Recorre los seis bloques de `02_polinomios_y_capacidad.ipynb` junto con la lectura.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

> **Lo que traes**
>
> El riesgo que importa (@ml-c1-def-riesgo) y su piso (@ml-c1-def-error-bayes).
>
> Un modelo lineal en sus parámetros, con representación fija (@ml-c1-def-modelo-lineal).
>
> La monotonía con familias anidadas de [[opt-objetivo-regresion-practica|Regresión, en la unidad 6]].

## 1 · Aproximar cerca de un punto

::: figure {#ml-c1-taylor-vs-mco title="Taylor contra mínimos cuadrados"}
![La curva 2 más 5 entre x, 20 datos con ruido y tres polinomios. Taylor de grado 3 y de grado 9, centrados en x0 igual a 1, se pegan a la curva cerca del centro y se abren en los bordes; a la derecha de x igual a 2, subir el grado empeora: en x igual a 2.5 el error de Taylor pasa de 10.1 con grado 3 a 115.3 con grado 9. El polinomio de grado 3 ajustado por mínimos cuadrados reparte el error donde hay datos: en x igual a 2.5 se equivoca 0.11.](../_assets/ml-c1-taylor-vs-mco.svg)
:::

La curva es $f=2+5/x$; la franja sombreada contiene los datos.
Taylor copia la curva cerca del centro, pero se separa al alejarse.
La línea en $x=2$ señala dónde aumentar el grado empeora esta aproximación.

**Piensa: ¿quién acierta mejor lejos del centro: el polinomio que copia las derivadas de $f$ o el que se ajusta a los datos?**

Aquí gana mínimos cuadrados: en $x=2.5$, el grado 3 se equivoca 0.11.
Taylor pasa de error 10.1 a 115.3 al subir de grado 3 a 9.
Son polinomios que resuelven problemas distintos: copiar derivadas locales o repartir error entre observaciones.

::: remark {#ml-c1-obs-taylor title="El polinomio de Taylor"}
Si $f$ tiene $N+1$ derivadas continuas entre $x_0$ y $x$,

$$
f(x)=f(x_0)+f'(x_0)(x-x_0)+\dots+\frac{f^{(N)}(x_0)}{N!}(x-x_0)^N+\frac{f^{(N+1)}(\xi)}{(N+1)!}(x-x_0)^{N+1}
$$

para algún $\xi$ entre $x_0$ y $x$. El último término es el error. Si la
derivada $N+1$ está acotada en ese segmento, el error es pequeño cerca de
$x_0$: es una garantía **local**. Si las derivadas crecen con $N$, subir $N$
puede empeorarlo lejos de $x_0$.
:::

Aquí el centro es 1; $x_0$ no es el inicio del descenso de la unidad 6 ni de una sucesión de Markov.
Para $1/x$, las derivadas crecen y la serie centrada en 1 solo converge en $(0,2)$.
Más grado no siempre mejora ni siquiera la aproximación.
Además, aprender exige trabajar sin conocer esas derivadas.

> [!TIP]
> **Míralo correr: bloque 1 · Taylor contra mínimos cuadrados**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-taylor title="Calcula el error de Taylor"}
Taylor de grado 1 de $1/x$ centrado en 1 es $2-x$.

(a) ¿Qué predice en $x=2$?

(b) ¿Cuánto se equivoca?
:::

::: hint {#ml-c1-pista-taylor-1 of="ml-c1-ej-taylor" title="Pista 1 · Recupera la recta"}
¿Qué vale $1/x$ y su derivada en 1?
:::

::: answer {#ml-c1-resp-taylor of="ml-c1-ej-taylor" title="Respuesta · El error lejos del centro"}
(a) Predice 0.

(b) El valor verdadero es 0.5; el error absoluto es 0.5.
Coincidir en valor y pendiente en el centro no obliga a acertar lejos.
:::

## 2 · Aproximar en todo un intervalo

::: figure {#ml-c1-weierstrass title="Aproximar en todo un intervalo"}
![La función valor absoluto de x menos 0.5 en el intervalo de 0 a 1, con un pico sin derivada en 0.5, y sus ajustes por mínimos cuadrados en una malla fina con polinomios de grado 2, 6 y 14. El error máximo baja: 0.094 con grado 2, 0.043 con grado 6, 0.021 con grado 14. El mejor polinomio en máximo de cada grado se equivoca a lo más eso.](../_assets/ml-c1-weierstrass.svg)
:::

Taylor no sirve en el pico de $\lvert x-0.5\rvert$: ahí no existe la derivada.
Aun así, los polinomios se acercan en todo el intervalo.
Estos ajustes minimizan cuadrados sobre una malla fina, sin ruido; el mejor polinomio en error máximo se equivoca a lo más lo indicado.

**Piensa: si existe un polinomio tan cerca como quieras de $f$, ¿lo vas a encontrar con 20 datos ruidosos?**

No necesariamente: aproximar no es aprender.
La existencia de una buena curva no explica cómo elegirla con observaciones incompletas.
Los errores máximos 0.094, 0.043 y 0.021 muestran aproximación, no aprendizaje desde una muestra ruidosa.

Para reunir las potencias escribimos $\phi_N(x)=(1,x,\dots,x^N)$.
El subíndice indica solo el grado: $\phi_1(x)=(1,x)$ y $\phi_2(x)=(1,x,x^2)$; nunca indica una capa.

::: theorem {#ml-c1-teo-stone-weierstrass title="Stone–Weierstrass, para polinomios en un intervalo"}
Sea $f$ continua en el intervalo cerrado $[x_{\min},x_{\max}]$ y
$\phi_N(x)=(1,x,\dots,x^N)$. Entonces

$$
\lim_{N\to\infty}\ \min_{\beta\in\mathbb R^{N+1}}\ \max_{x_{\min}\le x\le x_{\max}}\ \bigl\lvert f(x)-\beta^{\mathsf T}\phi_N(x)\bigr\rvert=0 .
$$

Es decir, para cualquier tolerancia hay un polinomio que se queda a menos de
ella de $f$ en todo el intervalo.
:::

El máximo mira el peor punto; el mínimo busca el mejor polinomio para ese criterio.
El teorema no fija un grado ni garantiza nada fuera del intervalo o sobre datos ruidosos.
$\widehat f$ debe dar valores parecidos a $f$, no necesariamente la misma forma.
Una garantía emparentada, la de Cybenko, aparecerá al estudiar redes.

> [!WARNING]
> Lectura equivocada: «Stone–Weierstrass garantiza que el polinomio aprenderá $f$».
>
> Lectura correcta: **Garantiza que existe uno cercano, no que los datos lo elijan, ni que sirva fuera de $[x_{\min},x_{\max}]$.**

::: exercise {#ml-c1-ej-weierstrass title="Revisa la hipótesis"}
(a) ¿El teorema aplica a $1/x$ en $(0,1]$?

(b) ¿Y en $[0.1,1]$?
:::

::: hint {#ml-c1-pista-weierstrass-1 of="ml-c1-ej-weierstrass" title="Pista 1 · Revisa el dominio"}
¿Es cerrado el intervalo y es $f$ continua en todo él?
:::

::: answer {#ml-c1-resp-weierstrass of="ml-c1-ej-weierstrass" title="Respuesta · El extremo importa"}
(a) No: $(0,1]$ no es cerrado y $1/x$ no está acotada ahí.

(b) Sí: $[0.1,1]$ es cerrado y $1/x$ es continua en todo él.
:::

## 3 · Ampliar la familia

::: figure {#ml-c1-tres-ajustes title="Subajuste, capacidad adecuada y sobreajuste"}
![Tres ajustes a los mismos 20 datos de la curva 2 más 5 entre x, con 200 observaciones nuevas del mismo proceso al fondo. grado 1, subajuste: error de entrenamiento 4.35 y riesgo 5.36; grado 4, capacidad adecuada: error de entrenamiento 0.18 y riesgo 0.44; grado 15, sobreajuste: error de entrenamiento 0.03 y riesgo 1450.97. El de grado 15 pasa cerca de casi todos los datos y entre ellos se dispara.](../_assets/ml-c1-tres-ajustes.svg)
:::

Los círculos son los 20 datos de entrenamiento; los puntos pequeños, 200 observaciones nuevas.

**Piensa: el grado 15 pasa por casi todos los datos: ¿qué hace entre ellos?**

Se dispara: logra $L_{\text{ent}}=0.03$, pero $R$ supera mil.
Eso es sobreajuste (*overfitting*): ajustar peculiaridades de la muestra perjudica la generalización.
El grado 1 tiene subajuste (*underfitting*): su familia no sigue la curvatura, con errores 4.35 y 5.36.
El grado 4 combina 0.18 en entrenamiento con riesgo 0.44.

::: definition {#ml-c1-def-capacidad title="Espacio de hipótesis y capacidad"}
El espacio de hipótesis es el conjunto de funciones entre las que el ajuste
puede elegir. Para polinomios de grado a lo más $N$,

$$
\mathcal H_N=\bigl\{f_\beta(x)=\beta^{\mathsf T}\phi_N(x):\ \beta\in\mathbb R^{N+1}\bigr\},\qquad \mathcal H_1\subset\mathcal H_2\subset\cdots
$$

La capacidad es qué tan variadas son las funciones de esa familia: más
capacidad, más formas que puede seguir, incluido el ruido. Su versión formal
para clasificación binaria es la dimensión VC: el mayor número de puntos tal
que **existe** un conjunto de ese tamaño que la familia etiqueta de todas las
formas posibles (una recta en el plano: 3).
:::

Esta $\mathcal H$ no es la de los bloques de una hora de [[opt-objetivo-salones-practica|Salones]].
La monotonía de la unidad 6 garantiza que ampliar la familia no aumenta el mínimo de entrenamiento.

::: remark {#ml-c1-obs-capacidad-efectiva title="Capacidad que se tiene y capacidad que se usa"}
La capacidad de la familia es la representacional. La efectiva puede ser menor:
el algoritmo no siempre encuentra la mejor función de la familia. Ese es el
error de optimización, que va aparte de las cuatro fuentes de
@ml-c1-obs-cuatro-fuentes (azar, variables que no medimos, familia
equivocada, pocos datos). No es una quinta fuente: es lo que se agrega
cuando el ajuste no llega al mínimo de $L_{\text{ent}}$.
:::

> [!TIP]
> **Míralo correr: bloque 2 · Las figuras 5.2 y 5.3 en vivo**
>
> Compara los ajustes y la curva de la sección siguiente.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-vc title="Cuenta las etiquetas"}
(a) ¿Una recta en el plano puede etiquetar de todas las formas tres puntos que no estén alineados?

(b) ¿Y los cuatro puntos del ejercicio final de la página anterior?
:::

::: hint {#ml-c1-pista-vc-1 of="ml-c1-ej-vc" title="Pista 1 · Recorre las posibilidades"}
Con tres puntos, ¿cuántas etiquetas distintas hay? ¿Alguna no se separa?
:::

::: answer {#ml-c1-resp-vc of="ml-c1-ej-vc" title="Respuesta · Un conjunto no basta"}
(a) Sí: puedes separar las 8 etiquetas de tres puntos no alineados.

(b) Esos cuatro no: falla la etiqueta del producto.
Eso solo demuestra que ese conjunto falla.
Para afirmar dimensión VC de 3 hay que descartar todos los conjuntos de cuatro.
Sin demostrarlo aquí: en posición convexa fallan las etiquetas alternadas.
Con un punto dentro del triángulo de los otros tres, falla la etiqueta que aísla al interior.
Los casos con puntos alineados tampoco permiten todas las etiquetas.
:::

## 4 · Mirar el error que no optimizamos

::: figure {#ml-c1-capacidad-brecha title="La brecha de generalización, medida"}
![Arriba, la curva de capacidad de los polinomios de grado 1 a 15 sobre 20 datos de la curva 2 más 5 entre x, en escala logarítmica. El error de entrenamiento nunca sube y en grado 15 vale 0.034, abajo del piso 0.25. El riesgo, medido con la muestra enorme, hace una U: es mínimo en grado 6, con 0.366, y en grado 15 llega a 1537; la brecha sombreada crece. El benchmark, la media, tiene riesgo 10.5. Abajo, el mismo proceso con 200 datos: el riesgo casi no sube después de grado 5 y en grado 15 vale 0.266; la U es de este experimento, no una ley.](../_assets/ml-c1-capacidad-brecha.svg)
:::

Cada grado tiene un ajuste; los ejes verticales son logarítmicos.
Arriba, con 20 datos, $R$ alcanza 0.366 en $N=6$ y cerca de 1537 en $N=15$.
La media es el punto de comparación (*benchmark*), con riesgo 10.5.
La figura no rotula las zonas: el extremo rígido subajusta; el flexible sobreajusta.

**Piensa: ¿por qué la curva de entrenamiento nunca sube, y la de $R$ sí?**

Las familias están anidadas: el mínimo de $L_{\text{ent}}$ no puede subir.
Pero el ajuste no optimiza $R$, aquí aproximado con la muestra enorme del mismo proceso.
Abajo, con 200 datos, $R$ casi no sube desde $N=5$: pasa de 0.274 a 0.266 en $N=15$.
La U pertenece al experimento, no es una ley.

La separación entre ambos errores mide cuánto difiere el desempeño observado del esperado en uso.

::: definition {#ml-c1-def-brecha title="Brecha de generalización"}

$$
\mathrm{brecha}(\widehat\beta)=R(\widehat\beta)-L_{\text{ent}}(\widehat\beta).
$$

:::

La brecha suele crecer con la capacidad: es una observación experimental de la figura.
Lo que sí se demuestra es que en promedio no es negativa (@ml-c1-teo-optimismo-entrenamiento).
El ajuste aprovecha particularidades de los mismos datos donde después calculas su error.

::: theorem {#ml-c1-teo-optimismo-entrenamiento title="El entrenamiento miente a tu favor, en promedio"}
Supón que las $n_{\text{ent}}$ observaciones de entrenamiento son
independientes y salen del mismo proceso que el despliegue, que $\ell\ge0$ y
que $\widehat\beta\in\operatorname*{arg\,min}_\beta L_{\text{ent}}(\beta)$.
Con la esperanza sobre la muestra de entrenamiento,

$$
E\bigl[L_{\text{ent}}(\widehat\beta)\bigr]\ \le\ \inf_\beta R(\beta)\ \le\ E\bigl[R(\widehat\beta)\bigr],
$$

así que $E\bigl[\mathrm{brecha}(\widehat\beta)\bigr]\ge0$.
:::

::: proof {#ml-c1-dem-optimismo-entrenamiento of="ml-c1-teo-optimismo-entrenamiento"}
1. Para un $\beta$ fijo de antemano, cada $\ell_i(\beta)$ tiene esperanza
   $R(\beta)$, así que $E[L_{\text{ent}}(\beta)]=R(\beta)$.
2. Como $\widehat\beta$ minimiza $L_{\text{ent}}$, $L_{\text{ent}}(\widehat\beta)\le L_{\text{ent}}(\beta)$
   para todo $\beta$; tomando esperanza, $E[L_{\text{ent}}(\widehat\beta)]\le R(\beta)$
   para todo $\beta$, y por tanto $\le\inf_\beta R(\beta)$.
3. Para cada muestra, $R(\widehat\beta)\ge\inf_\beta R(\beta)$; tomando esperanza, la otra desigualdad.
:::

El ínfimo es el menor riesgo alcanzable o aproximable dentro de la familia.
En 500 muestras, con $\beta$ fijo, la media de entrenamiento es 0.30 frente a $R(\beta)=0.31$.
Con $\widehat\beta$ de grado 4, las medias son 0.21 en entrenamiento y 0.71 de riesgo.
Una muestra concreta puede salir al revés: ocurrió en 9 de 500.

> [!WARNING]
> Lectura equivocada: «El piso es $\sigma_\varepsilon^2$, así que ningún error baja de ahí».
>
> Lectura correcta: **Ningún $R$ baja; $L_{\text{ent}}$ sí, porque memoriza el ruido.**

El piso cuadrático es 0.25; en grado 15 el entrenamiento llega a 0.034 y la brecha ronda 1537.
La clase 2 enseña a medir sin la muestra enorme.

::: exercise {#ml-c1-ej-bajo-el-piso title="Lee la curva"}
Con $N=15$, $L_{\text{ent}}=0.034$ y $R_{\text{Bayes}}=0.25$.

(a) ¿Contradice el piso?

(b) ¿Qué error debes comparar con él?
:::

::: hint {#ml-c1-pista-bajo-el-piso-1 of="ml-c1-ej-bajo-el-piso" title="Pista 1 · Revisa qué se acota"}
¿El piso habla de $L_{\text{ent}}$ o de $R$?
:::

::: answer {#ml-c1-resp-bajo-el-piso of="ml-c1-ej-bajo-el-piso" title="Respuesta · El piso acota el riesgo"}
(a) No: minimizar sobre la muestra permite ajustar parte de su ruido.

(b) El piso acota $R$, que promedia una observación nueva, no $L_{\text{ent}}$.
:::

## 5 · Decidir quién elige el grado

::: figure {#ml-c1-elegir-con-entrenamiento title="¿Quién elige el grado?"}
![En 200 muestras de 20 datos de la curva 2 más 5 entre x, se elige el grado de 1 a 15. Arriba, el que minimiza el error de entrenamiento: 200 de 200 veces el máximo, grado 15. Abajo, el de menor riesgo, repartido: 1 veces grado 1, 2 veces grado 2, 8 veces grado 3, 46 veces grado 4, 69 veces grado 5, 43 veces grado 6, 17 veces grado 7, 10 veces grado 8, 3 veces grado 9, 1 veces grado 10.](../_assets/ml-c1-elegir-con-entrenamiento.svg)
:::

El entrenamiento elige grado 15: 200 de 200 veces.
El menor riesgo cae entre 3 y 6 en 166; predomina 5.

**Piensa: si le dejas a $L_{\text{ent}}$ elegir el grado, ¿cuál escoge?**

El máximo gana o empata.
Limitar grado no limita curvatura.

::: definition {#ml-c1-def-capacidad-como-restriccion title="La capacidad como restricción"}
Con $\phi=\phi_{N_{\max}}$ fija, limitar el grado es resolver

$$
\min_\beta\ L_{\text{ent}}(\beta)\quad\text{s.a.}\quad \operatorname{grado}(f_\beta)\le N,
$$

donde $\operatorname{grado}(f_\beta)$ es el mayor exponente con coeficiente
distinto de cero. Es la forma $g(\beta)\le d$ de la unidad 6, con
$\Omega(\beta)=\operatorname{grado}(f_\beta)$ como medida de capacidad y $d=N$
como su cota; @opt-regresion-ej-capacidad ya la escribió con un tope de
coeficientes. La clase 3 cambia el grado por una medida continua
$\Omega(\beta)$ y escribe el lagrangeano con su multiplicador $\mu\ge0$.
:::

Esta $\Omega$ no es la cota asintótica de complejidad; mide capacidad.
$\mu$ es el multiplicador de KKT, no la distribución de Markov.
Tú eliges $N$; el ajuste elige $\widehat\beta$.

::: definition {#ml-c1-def-param-hiper title="Parámetro contra hiperparámetro"}
Un **parámetro** es lo que elige minimizar $L_{\text{ent}}$ dentro de un
problema ya planteado: $\beta$. Un **hiperparámetro** es lo que fija ese
problema —la familia, la representación, la cota $d$—: aquí, $N$. Ninguno
se elige minimizando $L_{\text{ent}}$. Con uno que fija la capacidad, como
$N$, se ve por qué: con familias anidadas,

$$
\min_{1\le N\le N_{\max}}\ \min_{\beta}\ L_{\text{ent}}(\beta\,;N)
$$

se alcanza en $N=N_{\max}$, la máxima capacidad (el conjunto de grados que
lo alcanzan siempre contiene a $N_{\max}$ y puede contener grados menores
empatados). Un hiperparámetro se elige con datos que no tocaron el ajuste.
:::

«Ninguno» alude a hiperparámetros; $\beta$ sí minimiza $L_{\text{ent}}$.
«;$N$» indica el grado.
No todos los hiperparámetros miden capacidad.

> [!TIP]
> **Míralo correr: bloque 3 · ¿Quién elige el grado?**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-elegir-grado title="Decide qué lo elige"}
Deja que $L_{\text{ent}}$ elija $N$ entre 1 y 12 para las seis entregas.

(a) ¿Qué escoge?

(b) ¿$N$ es parámetro o hiperparámetro?

(c) ¿Y los seis coeficientes del grado 5?
:::

::: hint {#ml-c1-pista-elegir-grado-1 of="ml-c1-ej-elegir-grado" title="Pista 1 · Amplía la familia"}
¿Qué pasa con el mínimo de $L_{\text{ent}}$ cuando agregas una columna a $\Phi$?
:::

::: answer {#ml-c1-resp-elegir-grado of="ml-c1-ej-elegir-grado" title="Respuesta · El empate también cuenta"}
(a) Grado 5 o más: desde 5 todos pueden interpolar las seis entregas y empatan con error 0.
Si eliges el menor grado entre los empatados, escoges 5; el máximo sigue siendo un ganador.

(b) $N$ es hiperparámetro: fija la familia.

(c) Los seis coeficientes son parámetros: los elige el ajuste dentro de ella.
:::

En la tarea vas a elegir el periodo y la $\phi$ así, mirando la nube y $L_{\text{ent}}$, por falta de otra herramienta.
Son propuestas exploratorias sin validar; la clase 2 te la da: validación y validación cruzada (*cross-validation*).

## 6 · Elegir la representación antes que el grado

::: figure {#ml-c1-inverso-vs-potencias title="Una columna correcta contra diez potencias"}
![Arriba, 60 datos de la curva 2 más 5 entre x con x desde 0.05, el polinomio de grado 10 y el modelo con la columna 1 entre x, que estima 2.03 más 5.00 entre x. Abajo, el riesgo en el despliegue, en escala logarítmica: grado 1, 82.4; grado 4, 18.2; grado 10, 1.28; la columna 1 entre x, 0.25, en el piso de 0.25. El benchmark, la media, tiene 120.8.](../_assets/ml-c1-inverso-vs-potencias.svg)
:::

También puedes cambiar las columnas.
Con 60 datos desde $x=0.05$, la recíproca cambia rápidamente.
Las barras inferiores comparan riesgos en escala logarítmica; la media tiene 120.8.

**Piensa: para una curva recíproca, ¿preferirías diez potencias o una columna $1/x$?**

Aquí conviene $\phi=(1,1/x)$: el ajuste da $\widehat\beta=(2.03,\ 5.00)$, cerca de $(2,5)$.
Su riesgo es 0.25, en el piso; diez potencias dan 1.28.
Los grados 1 y 4 dan 82.4 y 18.2.
Elegir una representación adecuada reduce el error de aproximación sin exigir una familia polinomial mayor.

Salgámonos del mundo de Stone–Weierstrass: no necesitas aproximar con potencias una forma que puedes incluir como columna.
Eso es ingeniería de variables.
La curva sigue siendo lineal en $\beta$, aunque se curve en $x$.
El supuesto recíproco permite usar pocos coeficientes; no lo descubrirá automáticamente el ajuste.

Con $J$ variables, un polinomio completo de grado a lo más $N$ tiene $\binom{J+N}{N}$ columnas, incluida la constante.
La cuenta reúne todos los productos de variables cuyo grado total no supera $N$.
Subir el grado por fuerza bruta aumenta también almacenamiento y cálculo.

> [!WARNING]
> Lectura equivocada: «Con más potencias el error de entrenamiento subió: la monotonía falla».
>
> Lectura correcta: **Falla la aritmética: las potencias sin escalar dan una $\Phi$ casi singular. Escala $x$ y la monotonía vuelve.**

En el caso con 100 datos, sin escalar, $L_{\text{ent}}$ pasa de 1.11 a 13.4 entre grados 10 y 25.
Escalando, el grado 25 da 0.18.
El mal condicionamiento dificulta el cálculo y puede producir coeficientes enormes; no cambia la inclusión entre familias.

> [!TIP]
> **Míralo correr: bloque 4 · Elegir la representación contra fuerza bruta**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-columnas title="Cuenta las columnas"}
(a) ¿Cuántas columnas tiene un polinomio completo de grado 3 en 5 variables?

(b) ¿Y en 20?
:::

::: hint {#ml-c1-pista-columnas-1 of="ml-c1-ej-columnas" title="Pista 1 · Cuenta los productos"}
¿Cuántos monomios de grado a lo más 3 hay con 5 letras?
:::

::: answer {#ml-c1-resp-columnas of="ml-c1-ej-columnas" title="Respuesta · Las columnas se multiplican"}
(a) $\binom{8}{3}=56$.

(b) $\binom{23}{3}=1771$.
Ambas cuentas incluyen el intercepto y los productos cruzados, no solo las potencias de cada variable por separado.
:::

## 7 · Saber dónde se usará el modelo

::: figure {#ml-c1-extrapolar title="Dónde se usará el modelo"}
![Tres procesos con la zona de los datos sombreada. Entregas, datos de 0 a 6 km: de 6 a 9 km la recta tiene riesgo de zona 1.14 y el polinomio de grado 7 se dispara, con más de un millón. Seno, datos de 0 a 2: el grado 7 tiene 0.10 dentro y 609 entre 2 y 3. Recursivo, con la x creciendo en el tiempo: la recta en x falla dentro, 5.5, y a un paso en el futuro, 36.4; con el tiempo anterior como columna queda en 1.05 y 1.05, cerca del piso de 1.](../_assets/ml-c1-extrapolar.svg)
:::

Arriba, la recta prolonga bien las entregas; el grado 7 se dispara.
En medio, el polinomio no repite el seno.
Abajo, el eje cuenta pasos y compara rectas a un paso.

**Piensa: si el modelo acierta dentro del rango de los datos, ¿puedes prometer lo mismo fuera?**

No: en entregas, la recta tiene riesgos de zona 1.03 dentro y 1.14 fuera; el grado 7 supera un millón fuera.
Para el seno, el grado 7 pasa de 0.10 a 609.
«Riesgo de zona» supone uso uniforme en esa zona; la figura no cambia el despliegue del experimento.

::: remark {#ml-c1-obs-donde-se-usa title="Interpolar, extrapolar y el riesgo"}
Interpolar es predecir para $x$ dentro del rango de los datos de entrenamiento;
extrapolar, fuera. $R$ promedia la pérdida según dónde caen las $x$ del
despliegue: si casi todas caen dentro, lo que pase fuera casi no pesa; si caen
fuera, $R$ es otro número y el entrenamiento no dice nada de él.
:::

En el recursivo, $x$ crece con el tiempo: fuera del rango está el futuro.
Hay además una dependencia omitida: el tiempo de hoy depende del de ayer.
Ninguna potencia de $x$ observa el tiempo anterior: falta una variable (@ml-c1-obs-cuatro-fuentes), aun dentro del rango.

La recta en $x$ da 5.5 dentro y 36.4 en el futuro.
Al incluir el tiempo anterior observado en $\phi$, con la constante 1, sigue siendo lineal en $\beta$.
Da 1.05 en ambas zonas, cerca del piso 1, a un paso.
A varios pasos, usando sus propias predicciones, el error se acumula.
Cuando las observaciones dependen unas de otras, cambia cómo separas los datos; lo verás en la clase 5.

> [!TIP]
> **Míralo correr: bloque 5 · Extrapolar**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-donde-se-usa title="Encuentra la extrapolación"}
El modelo de entregas se ajustó con distancias de 1 a 6 km.
Se usará en una zona nueva con entregas de 5 a 12 km.

(a) ¿Qué parte del uso es extrapolación?

(b) ¿Te basta su error en entregas viejas?
:::

::: hint {#ml-c1-pista-donde-se-usa-1 of="ml-c1-ej-donde-se-usa" title="Pista 1 · Ubica el uso"}
¿Dónde caerán las $x$ de las entregas que todavía no llegan?
:::

::: answer {#ml-c1-resp-donde-se-usa of="ml-c1-ej-donde-se-usa" title="Respuesta · El uso rebasa los datos"}
(a) Las distancias mayores que 6 y hasta 12 km.

(b) No: el error en las viejas no mide esa zona.
Necesitas medir con entregas que se parezcan al uso previsto.
:::

## 8 · Elegir supuestos

::: figure {#ml-c1-no-free-lunch title="No free lunch, exacto"}
![Las 256 funciones de etiquetas de 3 bits, con entrenamiento en 000, 011, 101 y 110, agrupadas por rugosidad. El vecino más cercano y la mayoría aciertan 100 % fuera de la muestra en las funciones más suaves y 0 % en las más rugosas; siempre 1 acierta 50  % en cada grupo. Promediando sobre las 256 funciones, cada regla acierta exactamente la mitad.](../_assets/ml-c1-no-free-lunch.svg)
:::

Comparamos las 256 funciones de etiquetas de 3 bits: 8 entradas.

**Piensa: si una regla gana en los problemas suaves, ¿qué le pasa en los demás?**

Compensa ganancias con pérdidas.
La rugosidad cuenta aristas del cubo que cambian de etiqueta; pertenece a la función completa.
La mayoría desempata hacia 1.

Ponderando por el número de funciones de cada grupo, todas promedian $\tfrac12$.
La inducción no es lógicamente válida; aprendes reglas probablemente correctas bajo supuestos.

::: theorem {#ml-c1-teo-no-free-lunch title="No free lunch (Wolpert, 1996)"}
Sea un conjunto finito de entradas posibles; de ellas, unas aparecen con su
etiqueta en el entrenamiento y las demás no. Supón que la etiqueta 0 o 1 de
cada entrada se elige al azar, cada una con probabilidad $\tfrac12$ e
independiente de las demás: es lo mismo que promediar sobre todas las
funciones de etiquetas posibles.

Entonces, para cualquier regla de aprendizaje,
la proporción esperada de aciertos en las entradas que no vio es $\tfrac12$.
Ninguna regla generaliza mejor que otra promediando sobre todos los problemas.
:::

::: proof {#ml-c1-dem-no-free-lunch of="ml-c1-teo-no-free-lunch"}
1. La regla solo ve las etiquetas del entrenamiento, así que su predicción
   para una entrada no vista es una función de ellas (y de su propio azar, si
   tiene).
2. La etiqueta de esa entrada es independiente de las del
   entrenamiento y vale 1 con probabilidad $\tfrac12$.
3. Por tanto acierta con
   probabilidad $\tfrac12$, sea cual sea su predicción.
4. Promediando sobre las
   entradas no vistas, la proporción esperada es $\tfrac12$.
:::

::: remark {#ml-c1-obs-no-parametrico title="Modelos sin un número fijo de parámetros"}
Un modelo es **no paramétrico** si el número de cantidades que guarda crece
con $n$. Vecinos más cercanos predice con la $y$ del dato de entrenamiento más
parecido: guarda todos los datos y alcanza $L_{\text{ent}}=0$ si no hay dos
$x$ iguales. El número de vecinos es un hiperparámetro.
:::

La regla “memorizar” de la clase 0
(@ml-c0-memorizar-contra-ajustar) es el vecino más cercano: por eso tenía cero en lo visto.

::: remark {#ml-c1-obs-supuestos title="Elegir modelo es elegir supuestos"}
Lo que hace funcionar a un modelo son los supuestos que trae sobre $f$:
suavidad (vecinos), linealidad en $\phi$ (regresión), periodicidad, que la
etiqueta no cambie al mover la imagen. Si el problema real los cumple, el
modelo gana; si no, pierde. Por eso hay que conocer el problema antes de
elegir.
:::

> [!WARNING]
> Lectura equivocada: «No free lunch dice que todos los modelos sirven igual».
>
> Lectura correcta: **Dice que empatan promediando sobre todos los problemas; en los problemas reales, que no son todos, el que trae los supuestos correctos gana.**

Considera estructura lineal, temporal o espacial, datos y uso.
Los dos procesos y modelos del notebook ilustran especialización; no demuestran el teorema.

> [!TIP]
> **Míralo correr: bloque 6 · No free lunch**
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/9_aprendizaje_maquina/_assets/02_polinomios_y_capacidad.ipynb)

::: exercise {#ml-c1-ej-cuatro-futuros title="Cuenta los futuros"}
Dos entradas tienen etiqueta conocida y dos no.

(a) ¿Cuántas formas hay de etiquetar las dos desconocidas?

(b) Si tu regla predice «1, 1», ¿cuántos aciertos tiene en promedio sobre esas formas?
:::

::: hint {#ml-c1-pista-cuatro-futuros-1 of="ml-c1-ej-cuatro-futuros" title="Pista 1 · Enumera los casos"}
¿Cómo queda la tabla de las cuatro formas?
:::

::: answer {#ml-c1-resp-cuatro-futuros of="ml-c1-ej-cuatro-futuros" title="Respuesta · Cada futuro pesa igual"}
(a) Hay 4 formas: «1, 1», «1, 0», «0, 1» y «0, 0».

(b) La predicción tiene 2, 1, 1 y 0 aciertos, respectivamente.
El promedio es 1 de 2: sin preferir unas funciones sobre otras, conocer las primeras etiquetas no informa las restantes.
:::

## Ejercicio final

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#ml-c1-ej-final-polinomios-y-capacidad title="Propón la representación de un patrón par e impar"}
En los enteros $x=1,\dots,8$, el tiempo extra de una ruta vale 5 si $x$ es par y 0 si es impar.
Simplificamos: no hay ruido y solo interesan entradas enteras.
La idea nueva es una regularidad periódica, no suave.

1. Describe qué hace el polinomio de grado 7 que pasa por los ocho puntos, dentro y en $x=9,10$.
2. Identifica qué supuesto le falta.
3. Propón una $\phi$ con dos columnas que dé la función exacta; di si el modelo es lineal en $\beta$.
4. Decide cuál de las dos reglas extrapola y qué supuesto lo hace posible.
:::

::: hint {#ml-c1-pista-final-polinomios-y-capacidad-1 of="ml-c1-ej-final-polinomios-y-capacidad" title="Pista 1 · Compara pares e impares"}
¿Qué tienen en común $x=2,4,6$ que no tengan $1,3,5$, escrito con una función que ya conoces?
:::

::: hint {#ml-c1-pista-final-polinomios-y-capacidad-2 of="ml-c1-ej-final-polinomios-y-capacidad" title="Pista 2 · Revisa la continuación"}
¿Tu $\phi$ da el mismo valor en todos los pares? ¿Necesita saber cuántos enteros hay?
:::

::: answer {#ml-c1-resp-final-polinomios-y-capacidad of="ml-c1-ej-final-polinomios-y-capacidad" title="Respuesta · Una columna periódica"}
**1. El polinomio.** Interpola los ocho puntos, pero predice 640 en $x=9$ y 4485 en $x=10$.
Pasar por los datos no le exige repetir el patrón.

**2. El supuesto.** Le falta periodicidad: la alternancia continúa después de la última entrada observada.

**3. La representación.** Sirve $\phi=(1,\cos\pi x)$, con $f=2.5+2.5\cos\pi x$.
En enteros pares el coseno vale 1; en impares, −1.
La regla da exactamente 5 y 0, respectivamente, y es lineal en $\beta$.

**4. La extrapolación.** La representación periódica acierta en todo entero si continúa esa misma alternancia.
Lo permite el supuesto correcto, no una mayor capacidad.
:::

**Punto de control:** ¿por qué no puedes elegir $N$ con $L_{\text{ent}}$, y qué tendría que cumplir el conjunto con el que sí lo eliges?
El entrenamiento premia ampliar la familia; necesitas datos que no tocaron el ajuste y que representen el uso.

> [!NOTE]
> **Un modelo exitoso**
>
> - El error de entrenamiento es pequeño.
> - La brecha es pequeña.
> - **Los datos con que lo mides imitan la realidad en la que se usará.**

## Para profundizar

- Stone (1948), *Mathematics Magazine*: la forma general de Stone–Weierstrass trata álgebras de funciones continuas sobre un espacio compacto Hausdorff.
  Si contienen las constantes y separan puntos, aproximan uniformemente cualquier función continua real.
- Wolpert (1996), *Neural Computation* 8(7): no free lunch y las condiciones del promedio sobre problemas.
- Goodfellow, Bengio y Courville, *Deep Learning*, §5.2: capacidad, dimensión VC, Bayes y no free lunch; §5.11.2: el ejemplo del tablero.
- Vapnik y Chervonenkis (1971): la relación entre familias de clasificadores y generalización.

## Lo que hay que llevarse

- **Aproximar no es aprender:** en $x=2.5$, Taylor pasa de error 10.1 a 115.3 al subir de grado 3 a 9; mínimos cuadrados da 0.11.
- **El mínimo de entrenamiento nunca sube con el grado:** las familias están anidadas. Eso no garantiza menor riesgo.
- **La U es del experimento:** con 20 datos, $R$ alcanza 0.366 en $N=6$; en $N=15$ ronda 1537, aunque $L_{\text{ent}}=0.034$.
  Con 200 datos, el riesgo casi no sube desde grado 5.
- **El entrenamiento no elige bien la capacidad:** eligió $N_{\max}=15$ en 200 de 200 muestras; el menor riesgo cayó entre 3 y 6 en 166.
- **La representación puede ganar a la fuerza bruta:** $(1,1/x)$ logra riesgo 0.25 contra 1.28 de diez potencias.
- **Generalizar exige supuestos:** en las 256 funciones, toda regla promedia exactamente 0.5 de aciertos fuera de la muestra.

**¿Cómo medimos $R$ sin la muestra enorme, con un conjunto que imite la realidad?**

Continúa con [[ml-clase-1-el-problema|Clase 1 · El problema]].
