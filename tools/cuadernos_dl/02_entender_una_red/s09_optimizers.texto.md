### celda: s09-intro

## 9 · Optimizers

Un *optimizer* (optimizador) convierte el gradiente de un mini-batch (lote
pequeño) en un cambio de los parámetros $\theta$. En la clase 1 hiciste
*gradient descent* (descenso de gradiente) a mano. En PyTorch,
`torch.optim.SGD` aplica esa misma regla al llamar a `opt.step()` en el
loop de la sección 3.

Justo antes del paso $t$, los parámetros son $\theta_t$. El gradiente del
mini-batch $\mathcal B_t$ es
$\mathbf g_t = \nabla_\theta L_{\mathcal B_t}(\theta_t)$.
La letra $g^{(l)}$ sigue nombrando la activación de la capa $l$.
El *learning rate* (tasa de aprendizaje) es $\eta$.

**SGD** (*stochastic gradient descent*, descenso de gradiente estocástico)
usa el gradiente del mini-batch actual. Multiplica ese gradiente por $\eta$
y da un paso en el sentido opuesto.

$$
\theta_{t+1} = \theta_t - \eta\,\mathbf g_t.
$$

**SGD con momentum** (inercia) acumula gradientes. El acumulador
$\mathbf m_0$ empieza en cero y $\beta$ indica cuánto se conserva del
acumulador anterior. Si los gradientes apuntan en la misma dirección,
se refuerzan. Si alternan de signo, la suma puede amortiguar el zigzag.

$$
\mathbf m_t = \beta\,\mathbf m_{t-1} + \mathbf g_t,
\qquad
\theta_{t+1} = \theta_t - \eta\,\mathbf m_t.
$$

**Adam** lleva dos promedios por parámetro. El primero, $\mathbf m_t$,
promedia los gradientes recientes. El segundo, $\mathbf v_t$, promedia sus
cuadrados. Los factores $\beta_1$ y $\beta_2$ controlan cuánto pesa el
historial en cada promedio.

$$
\begin{aligned}
\mathbf m_t &= \beta_1\mathbf m_{t-1} + (1-\beta_1)\mathbf g_t,\\
\mathbf v_t &= \beta_2\mathbf v_{t-1} + (1-\beta_2)\mathbf g_t^2,\\
\widehat{\mathbf m}_t &= \frac{\mathbf m_t}{1-\beta_1^t},
&
\widehat{\mathbf v}_t &= \frac{\mathbf v_t}{1-\beta_2^t},\\
\theta_{t+1} &= \theta_t -
\eta\,\frac{\widehat{\mathbf m}_t}{\sqrt{\widehat{\mathbf v}_t}+\varepsilon}.
\end{aligned}
$$

Ambos promedios arrancan en cero. En los primeros pasos, parte del
peso de cada promedio todavía corresponde a ese cero. Dividir entre
$1-\beta_1^t$ y $1-\beta_2^t$ corrige ese sesgo. En el primer paso queda
$\widehat{\mathbf m}_1=\mathbf g_1$ y
$\widehat{\mathbf v}_1=\mathbf g_1^2$. El cuadrado, la raíz y la división de
la actualización se calculan componente a componente.
$\varepsilon$ es una constante pequeña que evita dividir entre cero.

Al dividir por la escala reciente de cada componente del gradiente, Adam
adapta el tamaño del paso a cada parámetro. En el primer paso, si la
magnitud de la componente supera ampliamente a $\varepsilon$, el cambio
en ese parámetro tiene magnitud cercana a $\eta$. El mismo $\eta$ puede
dar pasos de tamaños muy distintos en Adam y en SGD.

**AdamW** usa la actualización de Adam y aplica por separado el *weight
decay* (encogimiento de los pesos). Verás cómo funciona después de la
primera comparación.

Las cuatro corridas usan la arquitectura de la línea base, los mismos
parámetros iniciales, el mismo orden de batches y el mismo presupuesto de
epochs (vueltas por los datos de train). SGD y SGD con momentum comparten
el learning rate. Adam y AdamW también. En esta comparación, el decay
se activa solo en AdamW. La celda de código muestra los valores.

### celda: s09-apuesta

**Apuesta.** Con el mismo presupuesto de epochs, ¿qué configuración
terminará con la menor loss de validation? ¿Esperas que SGD sin momentum
quede atrás o que alcance a las demás? Escribe tu predicción antes de
ejecutar la siguiente celda.

Las gráficas que siguen muestran también test en cada epoch. Mirar test
en cada epoch está mal: test se usa una sola vez, al final, para
reportar. Aquí aparece solo de manera didáctica, para aprender a leer
las curvas. Todas las decisiones se toman con validation.

### celda: s09-apuesta-respuesta

SGD sin momentum suele bajar más despacio al inicio. Con momentum o con
Adam, la loss puede bajar más rápido. Adam y AdamW pueden quedar casi
encimados, porque el encogimiento directo de AdamW es pequeño en esta
corrida. El orden entre momentum y Adam puede variar con la semilla.
Un empate también es un resultado. El orden depende de la configuración
completa, incluido el learning rate.

La primera figura usa un panel por corrida con los mismos ejes. Cada
conjunto (train, validation y test) tiene su color. En la segunda figura
todas las curvas son de validation, así que comparten su color; el estilo
de línea y el marcador identifican cada corrida. La loss de validation
está a la izquierda, en escala logarítmica, y la accuracy de validation,
a la derecha.

Para resolver tu apuesta, compara el último punto de las curvas de loss
de validation y los valores finales que imprime la primera celda. La
tabla maestra responde otra pregunta. Para cada corrida, reporta las
métricas de la epoch con menor loss de validation.

### celda: s09-l2-vs-adamw

### Weight decay: Adam + L2 contra AdamW

En la unidad 9, $\mu$ era el multiplicador del lagrangeano. En la clase 1
lo usaste para penalizar pesos grandes, como en ridge. La penalización
L2 es $\mu\Omega(\theta)$, donde
$\Omega(\theta)=\sum_{l=1}^{L}\lVert\mathbf W^{(l)}\rVert_F^2$.
Es decir, sumas los cuadrados de todos los pesos. El lagrangeano es
$\mathcal L(\theta,\mu)=L(\theta)+\mu(\Omega(\theta)-d)$, donde $d$ es
la cota sobre esa suma.

Para una matriz de pesos $\mathbf W^{(l)}$, la penalización añade
$2\mu\mathbf W^{(l)}$ a su gradiente. De ahí sale
`weight_decay = 2μ` para el caso acoplado en PyTorch. Al entrenar aquí,
el decay se aplica a los pesos y los sesgos se actualizan solo con el
gradiente de los datos.

Veamos el paso para una matriz de pesos. Escribe $\mathbf W_t$ para sus
valores antes del paso y $\mathbf G_t$ para el gradiente de la loss del
mini-batch con respecto a esa matriz. Con SGD sin momentum, sumar la
penalización al gradiente da la misma actualización que multiplicar los
pesos por $1-2\eta\mu$ y luego restar $\eta\mathbf G_t$.

**Adam + L2** (decay acoplado) usa `torch.optim.Adam` con
`weight_decay`. Suma la penalización al gradiente de los datos antes de
actualizar los dos promedios de Adam.

$$
\mathbf G_t \leftarrow \mathbf G_t + 2\mu\mathbf W_t.
$$

El término L2 influye tanto en el numerador como en el denominador
del paso de Adam. Su efecto depende de los gradientes y del historial
de cada peso.

**AdamW** (decay desacoplado) usa `torch.optim.AdamW`. El factor
$1-2\eta\mu$ encoge todos los pesos en la misma proporción. Luego se
resta $\mathbf D_t$, el paso de Adam calculado con el gradiente de los
datos.

$$
\mathbf W_{t+1} = (1-2\eta\mu)\mathbf W_t - \mathbf D_t.
$$

**Un paso a mano.** Empieza con $(w_1,w_2)=(1,2)$, con gradiente de los
datos y momentos en cero. Usa $\eta=0.1$ y
$\texttt{weight\_decay}=0.1=2\mu$, así que $\mu=0.05$.

- **Adam + L2.** Entra $\mathbf g_1=(0.1,0.2)$. En el primer paso,
  $\widehat{\mathbf m}_1=\mathbf g_1$ y
  $\sqrt{\widehat{\mathbf v}_1}=(0.1,0.2)$. Al dividir cada componente
  por su magnitud más $\varepsilon$, ambas dan casi uno. Adam resta
  cerca de $0.1$ a cada peso. El resultado es aproximadamente $(0.9,1.9)$.
- **AdamW.** El paso de Adam es cero porque los gradientes y momentos
  son cero. El decay multiplica los pesos por $1-0.1\cdot 0.1=0.99$.
  El resultado es $(0.99,1.98)$.

El código aplica las ecuaciones y verifica el resultado contra
`torch.optim.Adam` y `torch.optim.AdamW`.

### celda: s09-paso-que-viste

En la tabla, Adam + L2 resta casi $0.1$ a cada peso. Es alrededor del
$10\%$ de $w_1$ y del $5\%$ de $w_2$. AdamW resta $0.01$ y $0.02$,
respectivamente. Cada peso pierde el $1\%$ de su valor con AdamW.

En la gráfica, sigue los dos pesos a lo largo de los pasos. Con
Adam + L2, las curvas bajan casi en paralelo. El peso más chico se
acerca primero a cero y el cociente $w_2/w_1$ aumenta. Con AdamW, los
dos pesos se multiplican por el mismo factor en cada paso, así que su
cociente se mantiene en $2$. El código imprime el cociente para ambas
reglas.

En este ejemplo, AdamW conserva el encogimiento proporcional que
dedujiste para SGD con L2 en la clase 1. Durante el entrenamiento, el
gradiente de los datos también mueve los pesos. Con Adam + L2, además,
ese gradiente se mezcla con el de la penalización en los dos promedios.

### celda: s09-mnist-intro

Ahora usamos una red con una capa oculta más ancha en MNIST. Las tres
corridas parten de los mismos parámetros y comparten learning rate,
orden de batches y presupuesto de epochs. Adam + L2 y AdamW reciben el
mismo valor de `weight_decay`. Adam sin decay sirve de control.

A la izquierda verás la norma de los pesos por epoch, desde los pesos
iniciales. Es la raíz de la suma de cuadrados de todos los pesos. A la
derecha verás la loss de validation, en escala logarítmica. Cada corrida
conserva su estilo de línea y su marcador en los dos paneles. La tabla también da la accuracy final de validation.
Las diferencias en validation pueden ser imperceptibles, sobre todo entre
AdamW y el control; puede que aquí no cambie nada, y eso también es una
respuesta. Empieza por
comparar cómo cambia la norma de los pesos.

**Apuesta.** ¿Cuál de las tres corridas terminará con la norma más chica?

### celda: s09-que-viste

### Qué viste

En la primera comparación, fíjate en qué curva baja más rápido al
principio y en cuáles terminan cerca. Eso te permite distinguir un
avance inicial más rápido de una diferencia que dura hasta el final
del presupuesto.

En la comparación de decay, sigue primero la norma de los pesos. Sin
decay puede crecer a lo largo del entrenamiento. AdamW puede quedar
cerca del control porque $1-2\eta\mu$ está muy cerca de uno en cada
paso. Adam + L2 suele frenar mucho más el crecimiento. En pesos cuyo gradiente
de los datos es pequeño, el término L2 puede dominar el gradiente que
Adam usa para actualizar sus promedios. Lee el orden de las normas en
la gráfica y confirma el valor final en la tabla. Un mismo valor de
`weight_decay` puede producir efectos de distinta magnitud.

Después mira la loss de validation. Si las curvas casi coinciden a
pesar de que las normas se separan, el decay cambió el tamaño de los
pesos con poco efecto visible en la loss de validation. Si, en cambio,
la curva de Adam + L2 queda por encima de las otras dos, es la otra cara
de lo mismo: con Adam + L2, ese valor de `weight_decay` regulariza con
mucha más fuerza que con AdamW. En la unidad 9,
$\mu$ controlaba cuánto penalizabas la capacidad del modelo. Aquí, con
Adam, la forma de aplicar ese control cambia cómo se mueven los pesos.
