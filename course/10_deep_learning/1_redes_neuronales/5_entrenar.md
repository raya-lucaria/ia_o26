---
id: dl-entrenar
title: "Entrenar la red: bajar por el gradiente"
nav_title: "Entrenar"
summary: "Descenso de gradiente con tasa de aprendizaje y decaimiento de pesos, minibatch y época, el ciclo completo de cinco pasos en una sola fórmula, y las curvas de RMSE de un entrenamiento sin y con μ."
status: ready
estimated_time: 45m
tags: [deep-learning, descenso-de-gradiente, minibatch, epoca, regularizacion]
prerequisites: [dl-retropropagacion]
---

> [!WARNING]
> **▶▶ ABRE EL NOTEBOOK EN COLAB ◀◀**
>
> **Notebook 01 · Una red desde cero.** Corre en tu navegador, sin instalar nada.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)
>
> **[👉 Abrir `01_red_desde_cero.ipynb` en Colab](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)**

# Entrenar la red: bajar por el gradiente

**Ya sabes cuánto cambia la pérdida con cada peso. ¿Cómo conviertes eso en una red que predice bien datos que no vio?**

Al terminar tendrás:

- **La regla del paso:** $\theta\leftarrow\theta-\eta\nabla_\theta\mathcal L$, y qué le hace $\mu$ a cada peso.
- **Lotes y épocas:** qué gradiente se usa en cada paso y cuántos pasos hay por época.
- **El ciclo completo:** los cinco pasos del entrenamiento en una sola fórmula.
- **Una lectura de curvas:** por qué el RMSE de validación sube sin $\mu$ y casi no sube con $\mu$.

> **Lo que traes**
>
> De [[dl-retropropagacion|la retropropagación]]: $\nabla_{\mathbf W^{(l)}}\ell=\mathbf{δ}^{(l)}\mathbf a^{(l-1)\mathsf T}$ y $\nabla_{\mathbf b^{(l)}}\ell=\mathbf{δ}^{(l)}$. En el hilo, $\partial\ell/\partial w^{(3)}_{11}=-0.436$ y $\partial\ell/\partial b^{(3)}=-0.908$, con $\widehat y=0.546$, $y=1$ y $\ell=0.206$.
>
> De [[dl-perdida-lagrangeano|la pérdida y el lagrangeano]]: $\mathcal L(\theta,\mu)=L(\theta)+\mu(\Omega(\theta)-d)$, con $\Omega=\sum_l\lVert\mathbf W^{(l)}\rVert_F^2$.
>
> De la unidad 6, [[bajar-la-pendiente|bajar la pendiente]]: el descenso de gradiente y su tamaño de paso (@opt-tamano-de-paso).
>
> De la unidad 9: la brecha entre entrenamiento y riesgo (@ml-c1-def-brecha) y [[ml-lagrangeano-en-accion|el lagrangeano en acción]].

## 1 · Dar un paso contra el gradiente

**Piensa: si $\partial\ell/\partial w^{(3)}_{11}=-0.436$, ¿subes o bajas ese peso?**

Lo subes. El gradiente apunta hacia donde la pérdida crece; para bajarla, das un paso en contra.
Es el descenso de gradiente de la unidad 6, aplicado a todos los parámetros $\theta$ a la vez.

::: definition {#dl-def-descenso title="Descenso de gradiente sobre la red"}
Con una tasa de aprendizaje $\eta>0$, cada paso cambia todos los parámetros a la vez:

$$
\theta\leftarrow\theta-\eta\,\nabla_\theta\mathcal L .
$$

Por bloques, con el castigo de ridge:

$$
\begin{aligned}
\mathbf W^{(l)}&\leftarrow\mathbf W^{(l)}-\eta\bigl(\nabla_{\mathbf W^{(l)}}L+2\mu\mathbf W^{(l)}\bigr),\\
\mathbf b^{(l)}&\leftarrow\mathbf b^{(l)}-\eta\,\nabla_{\mathbf b^{(l)}}L .
\end{aligned}
$$
:::

$\eta$ es el tamaño de paso $\alpha$ de la unidad 6; en redes se escribe $\eta$, como en los libros del tema.
Esta $\eta$ no es la probabilidad verdadera $\eta(x)$ de la clase de clasificación de la unidad 9.
El $-\mu d$ del lagrangeano no depende de $\theta$: no aparece en el gradiente.

La línea de $\mathbf W^{(l)}$ se puede reordenar:

$$
\mathbf W^{(l)}\leftarrow(1-2\eta\mu)\,\mathbf W^{(l)}-\eta\,\nabla_{\mathbf W^{(l)}}L .
$$

Antes del paso de siempre, cada peso se encoge por el factor $1-2\eta\mu$.
Por eso a ridge en redes se le llama **decaimiento de pesos** (*weight decay*).
Con $\eta=0.1$ y $\mu=0.01$, el factor es $0.998$.

**Un paso en el hilo.** Con $\eta=0.1$, sin $\mu$ y con la única observación del hilo:

$$
w^{(3)}_{11}\leftarrow0.7-0.1\,(-0.436)\approx0.744 .
$$

Tras actualizar los 20 parámetros, la salida pasa de $\widehat y=0.546$ a $0.879$, y la pérdida de $0.206$ a $0.015$.

El mismo paso con $\mu=0.01$ deja la pérdida también en $0.015$.
La diferencia está en el tamaño de los pesos.
$\Omega$ valía $2.24$; el paso sin $\mu$ la sube a $2.401$ y el paso con $\mu$ a $2.392$.
Para subir $\widehat y$ los pesos crecen, y el castigo frena un poco ese crecimiento.

::: exercise {#dl-ej-paso-con-mu title="Da un paso con castigo"}
Con $\eta=0.1$ y $\mu=0.01$, actualiza a mano dos parámetros del hilo:

(a) $w^{(3)}_{11}=0.7$, con $\partial\ell/\partial w^{(3)}_{11}=-0.436$.

(b) $b^{(3)}=0.3$, con $\partial\ell/\partial b^{(3)}=-0.908$.
:::

::: hint {#dl-pista-paso-con-mu-1 of="dl-ej-paso-con-mu" title="Pista 1 · Elige la línea"}
¿Qué línea de @dl-def-descenso actualiza cada uno de los dos parámetros? Sustituye los números en esa línea antes de operar.
:::

::: answer {#dl-resp-paso-con-mu of="dl-ej-paso-con-mu" title="Respuesta · El sesgo no se encoge"}
(a) $0.7-0.1\,\bigl(-0.436+2(0.01)(0.7)\bigr)=0.7-0.1(-0.422)\approx0.742$.
Sin $\mu$ quedaba en $0.744$: el castigo le quitó un poco de subida.

(b) $0.3-0.1\,(-0.908)\approx0.391$, igual que sin $\mu$: los sesgos no entran en $\Omega$.
:::

## 2 · Promediar sobre un lote

**Piensa: con 80 observaciones, ¿necesitas retropropagar las 80 antes de dar un solo paso?**

No. El gradiente exacto de $L(\theta)$ es el promedio de los 80 gradientes de $\ell$.
Un promedio sobre unas cuantas observaciones al azar ya apunta casi hacia el mismo lado, y cuesta mucho menos.

::: definition {#dl-def-lote-epoca title="Lote y época"}
Un **lote** (*minibatch*) $\mathcal B$ es un subconjunto de las observaciones de entrenamiento; $\lvert\mathcal B\rvert$ es su tamaño.
Cada paso usa la pérdida promedio del lote, $L_{\mathcal B}(\theta)=\frac1{\lvert\mathcal B\rvert}\sum_{k\in\mathcal B}\ell(f_\theta(\mathbf x_k),\mathbf y_k)$, y su gradiente:

$$
\nabla_{\mathbf W^{(l)}}L_{\mathcal B}=\frac1{\lvert\mathcal B\rvert}\sum_{k\in\mathcal B}\mathbf{δ}^{(l)}_k\,\mathbf a^{(l-1)\mathsf T}_k,
\qquad
\nabla_{\mathbf b^{(l)}}L_{\mathcal B}=\frac1{\lvert\mathcal B\rvert}\sum_{k\in\mathcal B}\mathbf{δ}^{(l)}_k .
$$

Una **época** es una pasada por todas las observaciones: se barajan y se parten en lotes, y se da un paso por lote.
:::

$L_{\mathcal B}$ es la $L_{\mathcal D}$ de la unidad 9 con el lote como conjunto.
Esta $\mathcal B$ caligráfica no es el número $B$ de árboles de un bosque.

Con $n=80$ y lotes de 20, cada época da 4 pasos.
Si el lote es todo el conjunto, hay un paso por época con el gradiente exacto: es el descenso de la unidad 6.
Con lotes chicos y barajados, el método se llama **descenso de gradiente estocástico**: cada paso usa un gradiente con ruido, pero barato.

::: exercise {#dl-ej-contar-pasos title="Cuenta los pasos"}
El entrenamiento de la sección 4 usa 80 observaciones, lotes de 20 y 1500 épocas.

(a) ¿Cuántos pasos de descenso da en total?

(b) ¿Cuántas retropropagaciones de una observación?
:::

::: hint {#dl-pista-contar-pasos-1 of="dl-ej-contar-pasos" title="Pista 1 · Una época a la vez"}
¿Cuántos lotes caben en una época? ¿Cuántas observaciones toca una época?
:::

::: answer {#dl-resp-contar-pasos of="dl-ej-contar-pasos" title="Respuesta · Pasos contra observaciones"}
(a) $80/20=4$ pasos por época; $4\times1500=6000$ pasos.

(b) Cada época retropropaga las 80 una vez: $80\times1500=120\,000$.
Con el lote completo serían las mismas retropropagaciones, pero solo 1500 pasos.
:::

## 3 · Cerrar el ciclo

**Piensa: ¿qué se calcula, en qué orden, en cada paso del entrenamiento?**

Primero se toma un lote $\mathcal B$: es la entrada del ciclo, no uno de sus pasos.
Con él se calculan cinco cosas, y cada una usa la anterior.

1. **Adelante.** Para cada $\mathbf x_k$ del lote: $\mathbf a^{(0)}=\mathbf x_k$, $\mathbf z^{(l)}=\mathbf W^{(l)}\mathbf a^{(l-1)}+\mathbf b^{(l)}$, $\mathbf a^{(l)}=g^{(l)}(\mathbf z^{(l)})$. Se guardan todas las $\mathbf z^{(l)}$ y $\mathbf a^{(l)}$.
2. **Pérdida.** $\ell_k=(\widehat y_k-y_k)^2$ y su promedio $L_{\mathcal B}$, más $\mu\Omega$.
3. **Atrás.** $\mathbf{δ}^{(L)}$ y luego $\mathbf{δ}^{(L-1)},\dots,\mathbf{δ}^{(1)}$ con las dos ecuaciones (@dl-teo-dos-ecuaciones).
4. **Gradientes.** $\mathbf{δ}^{(l)}_k\mathbf a^{(l-1)\mathsf T}_k$ y $\mathbf{δ}^{(l)}_k$, promediados en el lote, más $2\mu\mathbf W^{(l)}$.
5. **Actualizar.** $\theta\leftarrow\theta-\eta\cdot$ gradiente. Siguiente lote.

Los cinco pasos caben en una sola fórmula:

$$
\theta\ \leftarrow\ \theta-\eta\,\nabla_\theta\Bigl[\frac1{\lvert\mathcal B\rvert}\sum_{k\in\mathcal B}\ell\bigl(f_\theta(\mathbf x_k),\mathbf y_k\bigr)+\mu\,\Omega(\theta)\Bigr].
$$

Detrás de la fórmula hay tres ideas, una por cada pieza:

- **El pase hacia adelante es la composición** $f_\theta=f^{(L)}\circ\cdots\circ f^{(1)}$: calcula la predicción.
- **La retropropagación es la regla de la cadena en sentido inverso:** multiplica por jacobianas traspuestas de la salida a la entrada y entrega $\nabla_\theta$.
- **El descenso usa esos gradientes:** un paso de largo $\eta$ en contra, una y otra vez.

::: figure {#dl-ciclo title="El ciclo de entrenamiento"}
![El ciclo de entrenamiento en cinco pasos, en círculo: 1, pase hacia adelante, z(l) y a(l) de cada capa hasta ŷ; 2, la pérdida promediada en el lote, L_ℬ, más μΩ(θ); 3, pase hacia atrás, de δ(L) a δ(1); 4, los gradientes, δ(l) a(l−1) traspuesta promediado en el lote, más 2μW(l); 5, actualizar θ ← θ − η ∇ℒ(θ, μ). Luego, de nuevo con el siguiente lote. Al centro, la entrada del ciclo: tomar un lote ℬ de |ℬ| pares (xₖ, yₖ), que alimenta el paso 1. Debajo: θ son todos los W(l) y b(l); una vuelta es un paso de descenso y pasar por todos los lotes es una época.](../_assets/dl-ciclo.svg)
:::

En pseudocódigo, con los números de paso de la lista al margen:

```text
ENTRENAR(red, datos, η, μ, épocas, tamaño)
INPUT:  red con θ inicial; n pares (x_k, y_k)
OUTPUT: la red con θ entrenado
 1  repetir épocas veces:
 2    barajar las n observaciones
 3    para cada lote de ese tamaño:
 4      para cada k del lote:
 5        adelante: guardar z(l), a(l)  # 1
 6        ℓ_k = (ŷ_k − y_k)²            # 2
 7        atrás: δ(L), …, δ(1)          # 3
 8        acumular δ(l)a(l−1)ᵀ y δ(l)   # 4
 9      promediar en el lote; sumar 2μW(l)  # 4
10      θ ← θ − η · gradiente           # 5
```

En el notebook, `paso` hace las líneas 4 a 10 y `entrenar` el ciclo completo.

## 4 · Leer un entrenamiento

**Piensa: si la pérdida de entrenamiento baja en cada época, ¿la red mejora en cada época?**

Para contestarlo hay que medir también en datos que la red no ve.
El ejemplo usa datos sintéticos, para conocer el piso.

- **Los datos.** $\mathbf x$ uniforme en el cuadrado $[-1,1]^2$ y $y=\sin(\pi x_1)\cos(\pi x_2/2)+\varepsilon$, con ruido normal de desviación $0.3$.
- **Los conjuntos.** 80 observaciones de entrenamiento y 200 de validación.
- **La red.** 2–32–32–1, ocultas ReLU y salida identidad: más de mil parámetros para 80 datos.
- **El descenso.** $\eta=0.03$, lotes de 20 y 1500 épocas.
- **Dos corridas.** Una con $\mu=0$ y otra con $\mu=0.003$, con los mismos pesos iniciales y el mismo barajado.

En la figura, el eje horizontal es la época, de 0 a 1500, y el vertical el RMSE.
**Un punto es el RMSE de todo un conjunto al final de una época**, en una sola corrida, sin promediar.

::: figure {#dl-curvas-rmse title="RMSE contra época, sin castigo y con castigo"}
![Dos gráficas de RMSE de entrenamiento y de validación contra la época, de 0 a 1500, con la misma red, los mismos datos y los mismos pesos iniciales. Arriba, sin μ: el RMSE de entrenamiento baja hasta 0.196; el de validación llega a su mínimo, 0.328, en la época 285 y después sube hasta 0.418. Abajo, con μ igual a 0.003: el de entrenamiento termina más arriba, en 0.247, y el de validación termina en 0.316, con su mínimo, 0.310, en la época 894.](../_assets/dl-curvas-rmse.svg)
:::

**Sin $\mu$, las dos curvas se separan.**
El RMSE de entrenamiento sigue bajando hasta $0.196$.
El de validación toca su mínimo, $0.328$, en la época 285, y luego sube hasta $0.418$.

El ruido marca el piso.
Aun conociendo la función verdadera, su riesgo en datos nuevos sería $0.3^2=0.09$: un RMSE de $0.3$, la desviación del ruido.
Un RMSE de entrenamiento de $0.196$ está **por debajo del piso**: la red ya sigue el ruido de esas 80 observaciones.
Es el sobreajuste de la unidad 9, con su brecha creciente (@ml-c1-def-brecha), igual que el polinomio de grado 12.

**Con $\mu=0.003$, el entrenamiento cede y la validación gana.**
El RMSE de entrenamiento termina más alto, en $0.247$.
El de validación termina en $0.316$ y su mínimo, $0.310$, llega hasta la época 894: casi no sube.
Queda cerca del piso de $0.3$.

Es la definición de regularizar (@ml-c3-def-regularizacion): subir el error de entrenamiento para cerrar la brecha.
El castigo no deja crecer los pesos lo que haría falta para perseguir cada punto.

$\mu$ y la época en que paras son hiperparámetros (@ml-c1-def-param-hiper): se eligen con validación, como en la unidad 9.
Detenerse en el mínimo de validación también regulariza; se llama parada temprana (*early stopping*), y la menciona [[ml-la-metodologia|la metodología]].
Las cifras son de una sola corrida: otra semilla las mueve.

> [!WARNING]
> Lectura equivocada: «La pérdida de entrenamiento bajó hasta el final, así que la red mejoró hasta el final».
>
> Lectura correcta: **lo que importa es la validación: sin $\mu$, la red empeoró en datos nuevos desde la época 285.**

> [!TIP]
> **Míralo correr: entrena la red**
>
> Corre las dos curvas, cambia $\mu$ y el tamaño del lote, y busca dónde se separan.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/10_deep_learning/_assets/01_red_desde_cero.ipynb)

::: exercise {#dl-ej-detener title="Decide cuándo parar"}
Usa la corrida sin $\mu$.

(a) Si detienes el entrenamiento en el mínimo de validación, ¿en qué época paras y qué RMSE de validación tienes?

(b) ¿Es esa cifra una estimación honesta del error en datos nuevos?
:::

::: hint {#dl-pista-detener-1 of="dl-ej-detener" title="Pista 1 · Pregunta quién eligió"}
¿Con qué datos elegiste la época? ¿Pueden esos mismos datos medir lo que eligieron?
:::

::: answer {#dl-resp-detener of="dl-ej-detener" title="Respuesta · Elegir gasta la validación"}
(a) Paras en la época 285, con RMSE de validación $0.328$.

(b) No del todo. Elegiste la época como el mínimo de 1501 valores en esa misma validación: la cifra es optimista.
Para reportar, mides una sola vez en un conjunto de prueba que no participó, como en la unidad 9 (@ml-c2-obs-optimismo-seleccion).
:::

## 5 · Ver lo que falta

**Piensa: ¿qué de esta clase cambia cuando las redes crecen?**

Las piezas, no el ciclo.
Los pesos iniciales de la sección 4 son normales escalados por $\sqrt{2/d_{l-1}}$, con sesgos en cero; elegirlos bien es un tema propio.
El paso puede adaptarse por parámetro, como en Adam.
Las capas pueden cambiar de forma, como en las convoluciones o la atención.

Las tres ideas se quedan: adelante es una composición, atrás es la regla de la cadena al revés, y el descenso usa esos gradientes.

## Ejercicio final

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#dl-ej-final-entrenar title="Entrena con un castigo de lasso"}
Quieres que la red use pocos pesos, como lasso en la unidad 9.
La idea nueva: el castigo es $\Omega_1(\theta)=\sum_l\sum_{i,j}\lvert w^{(l)}_{ij}\rvert$, no la suma de cuadrados.
Los sesgos siguen sin castigo. Toma $\eta=0.1$ y $\mu=0.01$.

1. Escribe el gradiente del castigo respecto de un peso $w\ne0$.
2. Escribe la actualización de $\mathbf W^{(l)}$ y la de $\mathbf b^{(l)}$.
3. Sin contar el gradiente de $L_{\mathcal B}$, ¿cuánto se acercan a cero en un paso un peso de $0.7$ y uno de $0.001$, con ridge y con lasso?
4. ¿Qué cambia en los cinco pasos del ciclo?
5. ¿Cómo eliges $\mu$?
:::

::: hint {#dl-pista-final-entrenar-1 of="dl-ej-final-entrenar" title="Pista 1 · Deriva un valor absoluto"}
¿Cuánto vale la derivada de $\lvert w\rvert$ si $w>0$? ¿Y si $w<0$? ¿Depende de qué tan grande es $w$?
:::

::: hint {#dl-pista-final-entrenar-2 of="dl-ej-final-entrenar" title="Pista 2 · Revisa tu propuesta"}
Comprueba con dos preguntas: ¿tu paso de ridge depende del tamaño del peso, y el de lasso? ¿Tocaste la retropropagación, o solo un término que se suma al final?
:::

::: answer {#dl-resp-final-entrenar of="dl-ej-final-entrenar" title="Respuesta · Un empujón fijo hacia cero"}
**1. Gradiente.** $\partial\lvert w\rvert/\partial w=\operatorname{sign}(w)$: $+1$ si $w>0$, $-1$ si $w<0$.
En $w=0$ no hay derivada; en código se toma 0.

**2. Actualización.** Con el signo aplicado entrada por entrada:

$$
\mathbf W^{(l)}\leftarrow\mathbf W^{(l)}-\eta\bigl(\nabla_{\mathbf W^{(l)}}L_{\mathcal B}+\mu\operatorname{sign}(\mathbf W^{(l)})\bigr),
\qquad
\mathbf b^{(l)}\leftarrow\mathbf b^{(l)}-\eta\,\nabla_{\mathbf b^{(l)}}L_{\mathcal B}.
$$

**3. Cuánto encoge.** Ridge resta $2\eta\mu w$: $0.002\cdot0.7=0.0014$ al peso grande y $0.000002$ al chico.
Lasso resta $\eta\mu=0.001$ a los dos.
Ridge encoge en proporción; lasso empuja lo mismo a todos.
El peso chico cae justo en cero, $0.001-0.001=0$, pero solo porque en este ejemplo $\eta\mu=0.001$ coincide con el peso.

**4. El ciclo.** Solo cambia el término del castigo en los pasos 2 y 4. Adelante y atrás no se tocan.
Con pasos de descenso, un peso cerca de cero en general lo cruza y oscila: uno de $0.0005$ pasa a $-0.0005$ y en el paso siguiente regresa a $0.0005$.
No queda en cero exacto; la fórmula de umbral de la unidad 9, en cambio, sí da ceros exactos.

**5. Elegir $\mu$.** Es un hiperparámetro: una rejilla logarítmica y validación, y la prueba al final, una sola vez.
:::

**Punto de control:** deberías poder escribir el paso con $\eta$ y $\mu$, contar pasos por época y explicar por qué una curva de validación sube mientras la de entrenamiento baja.

## Lo que hay que llevarse

- **El paso:** $\theta\leftarrow\theta-\eta\nabla_\theta\mathcal L$; con ridge, cada peso se encoge por $1-2\eta\mu$ antes del paso. En el hilo, un paso con $\eta=0.1$ lleva $\widehat y$ de $0.546$ a $0.879$ y $\ell$ de $0.206$ a $0.015$.
- **Lotes y épocas:** el gradiente de cada paso es el promedio del lote. Con 80 datos y lotes de 20, una época son 4 pasos.
- **El ciclo:** adelante, pérdida, atrás, gradientes, actualizar. Adelante es la composición; atrás, la cadena al revés; el descenso usa esos gradientes.
- **Las curvas:** sin $\mu$, entrenamiento baja a $0.196$, bajo el piso de $0.3$, y validación sube de $0.328$ (época 285) a $0.418$. Con $\mu=0.003$, entrenamiento queda en $0.247$ y validación en $0.316$.

Aquí termina la clase 1. Regresa al [[dl-clase-1-redes-neuronales|índice de la clase]].
