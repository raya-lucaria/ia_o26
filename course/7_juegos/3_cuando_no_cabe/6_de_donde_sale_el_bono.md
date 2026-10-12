---
id: de-donde-sale-el-bono
title: De dónde sale el bono
nav_title: De dónde sale el bono
summary: "El bono de UCT es el margen de error de un promedio: cuánto podría valer de más una jugada poco probada. Sale de la desigualdad de Hoeffding y de pedir más confianza conforme avanza la búsqueda; se usa para seleccionar, no para entregar."
status: ready
estimated_time: 30m
tags: [juegos, mcts, exploracion]
---

# De dónde sale el bono

**¿Por qué el bono de UCT tiene justo esa forma?**

Al terminar tendrás:

- el bono leído como **margen de error** de un promedio, y por qué se
  **suma** en vez de restarse;
- la **desigualdad de Hoeffding**: qué dice, qué supone y una simulación
  que la comprueba;
- el bono despejado paso a paso, de un margen con probabilidad de fallo
  $\delta$ hasta ${c=2\sqrt2}$;
- cuatro reglas comparadas en las mismas tres jugadas: cuál se atora y
  cuál llega a la mejor;
- cuándo se usa el bono (al **seleccionar**) y cuándo no (al
  **entregar**), también en un nodo de MIN.

> **Lo que traes de [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].**
> Una simulación (@jue-c3-simulacion) termina en ${U=+1}$ o ${U=-1}$. Cada
> nodo $s'$ guarda $N(s')$ simulaciones y $G(s')$ victorias de MAX; su
> promedio $\bar u(s')$ va de ${-1}$ a ${+1}$. La selección baja al hijo de
> mayor puntaje: $\bar u(s')$ más el bono ${c\sqrt{\ln N(s)/N(s')}}$, donde
> $s$ es el padre. Allá usamos ${c=1}$.

> **El juego de esta página.** Tres jugadas en la raíz, x, y, z, como en el
> ejercicio de MCTS (@jue-c3-ej-mcts). Cada vuelta elige una, juega una
> simulación y anota ${U=\pm1}$. No hay árbol debajo: solo esta elección,
> repetida.

> **Supuestos de esta página.** Las simulaciones de una misma jugada son
> independientes. En la sección 8 vemos qué pasa cuando hay árbol y esto
> deja de valer.

> [!TIP]
> **Míralo correr: el margen y las tres jugadas**
>
> - **▶ [Hoeffding en vivo](../_assets/hoeffding_en_vivo.html)**: miles de
>   promedios a la vez. Mueve el promedio verdadero, las simulaciones y el
>   margen, y compara lo que pasa con la cota.
> - **▶ [Bandido en vivo](../_assets/bandido_en_vivo.html)**: x, y, z con
>   su promedio oculto. Mueve $c$ y mira cuántas vueltas van a la mejor.
> - **Notebook en Colab**, sección 8: las mismas simulaciones y las tres
>   gráficas de esta página.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

## 1 · Repetir una sola elección

**Piensa: si MCTS solo tuviera la raíz, sin árbol debajo, ¿qué haría en
cada vuelta?**

Elegir entre x, y, z, jugar una simulación y anotar el resultado. Otra vez,
y otra. Este problema se llama **bandido**, por las máquinas tragamonedas:
cada jugada es una palanca que paga al azar. La pregunta es qué palanca
jalar en la vuelta que sigue.

::: definition {#jue-c3-mu title="El promedio verdadero"}
El **promedio verdadero** $\mu(s')$ de una jugada es el promedio de $U$
que darían infinitas simulaciones desde $s'$. Es un número entre ${-1}$ y
${+1}$, en la escala de $U$ y visto desde MAX. En
[[simular-en-vez-de-evaluar|Simular en vez de evaluar]] lo llamamos
«promedio límite».

**Qué significa:** $\bar u(s')$ lo **estima** con las $N(s')$
simulaciones que hay. Nadie conoce $\mu(s')$; solo se ve $\bar u(s')$.

**Qué no es:** no es el valor $V(s')$. Supone que los dos juegan al azar.
:::

En esta página fijamos los promedios verdaderos para poder comprobar cada
regla: ${\mu(\text{x})=0.6}$, ${\mu(\text{y})=0.3}$ y
${\mu(\text{z})=-0.2}$. La mejor es **x**, la que el ejercicio de MCTS
entregaba. Con ${U=\pm1}$, x gana con probabilidad 0.8, y con 0.65 y z
con 0.4. La regla no ve estos números.

La regla más sencilla prueba cada jugada una vez y luego elige **siempre
el mejor promedio**. En una corrida con semilla fija, las tres primeras
vueltas salen así: x pierde, y pierde, z gana.

::: exercise {#jue-c3-ej-atora title="Encuentra dónde se atora"}
Tras esas tres vueltas, ${\bar u(\text{x})=-1}$, ${\bar u(\text{y})=-1}$ y
${\bar u(\text{z})=+1}$. La regla sigue con «siempre el mejor promedio».

1. ¿Qué jugada elige en la vuelta 4?
2. ¿Puede volver a elegir x alguna vez? ¿Por qué?
:::

::: hint {#jue-c3-pista-atora-1 of="jue-c3-ej-atora" title="El piso"}
¿Cuál es el valor más bajo que puede tener un promedio de $U$? ¿Puede
llegar ahí una jugada que ya ganó una vez?
:::

::: answer {#jue-c3-resp-atora of="jue-c3-ej-atora"}
1. **z**, con ${\bar u=+1}$.
2. **Nunca.** x e y no se vuelven a probar, así que se quedan en ${-1}$, el
   mínimo posible. z ya ganó una vez: su promedio nunca baja a ${-1}$. En
   esta corrida, tras 1 000 vueltas, x e y tienen una simulación cada una y
   z, 998. La regla se atoró en la peor jugada.
:::

A esta regla le falta algo: **dudar** de un promedio hecho con una sola
simulación. Eso es lo que hace el bono.

## 2 · Medir cuánto falla un promedio

**Piensa: con 10 simulaciones, ¿qué tan seguido queda el promedio muy por
debajo del verdadero?**

Se puede medir. Toma la jugada y, con ${\mu=0.3}$. Juega $N(s')$
simulaciones, saca su promedio y repite todo 20 000 veces. Cuenta en
cuántas el promedio quedó al menos $\varepsilon$ por debajo.

::: definition {#jue-c3-margen title="El margen y el fallo"}
El **margen** $\varepsilon$ es un número positivo, en la escala de $U$.
Decimos que el promedio **falla por debajo** si
${\bar u(s')\le\mu(s')-\varepsilon}$: subestimó la jugada en $\varepsilon$
o más.
:::

Con ${\varepsilon=0.2}$, fallar es sacar ${\bar u\le0.1}$. La tabla compara
la frecuencia simulada con una cota que veremos enseguida.

::: table {#jue-c3-tabla-hoeffding title="La jugada y: el fallo baja rápido con N(s′)"}
| $N(s')$ | Simulado | Cota |
|---:|---:|---:|
| 10 | 24.7 % | 81.9 % |
| 50 | 7.1 % | 36.8 % |
| 100 | 2.4 % | 13.5 % |
| 200 | 0.2 % | 1.8 % |
:::

::: figure {#jue-c3-fig-hoeffding title="Todos los puntos quedan bajo la cota"}
![Gráfica con eje y logarítmico. Eje x: N(s′), simulaciones de la jugada y, de 0 a 200. Eje y: frecuencia con que ū(s′) queda en μ(s′) − ε o menos, de 0.001 a 1, con μ = 0.3 y ε = 0.2. Los puntos, la frecuencia observada en 20 000 tiradas, bajan en zigzag; la línea, la cota exp(−N(s′)·ε²/2), baja recta y queda siempre por encima de los puntos: con N(s′) = 10, 24.7 % contra 81.9 %; con 50, 7.1 % contra 36.8 %; con 100, 2.4 % contra 13.5 %](../_assets/jue-c3-hoeffding.svg)
:::

Los puntos zigzaguean de verdad, no por ruido. El promedio solo toma
ciertos valores, con saltos de ${2/N(s')}$. Según $N(s')$, el umbral 0.1
cae justo en uno de ellos o entre dos.

La línea es una cota demostrada hace más de sesenta años. Aquí la
citamos, sin demostrarla:

::: theorem {#jue-c3-teo-hoeffding title="Desigualdad de Hoeffding, citada"}
Toma $N(s')$ resultados **independientes**, cada uno entre ${-1}$ y
${+1}$, con promedio verdadero $\mu(s')$. Para todo ${\varepsilon>0}$ y
todo $N(s')$, su promedio cumple

$$\begin{aligned}
&\Pr\bigl(\bar u(s')\le\mu(s')-\varepsilon\bigr)\\
&\qquad\le e^{-N(s')\,\varepsilon^2/2}.
\end{aligned}$$

Lo mismo vale para el otro lado: ${\bar u(s')\ge\mu(s')+\varepsilon}$.

No hace falta que todos salgan de la misma forma de jugar: si sus
promedios verdaderos difieren, $\mu(s')$ es el promedio de ellos.

**Fuente:** W. Hoeffding, «Probability inequalities for sums of bounded
random variables», *Journal of the American Statistical Association*,
1963, teorema 2.
:::

**¿Por qué esta desigualdad y no otra?** Por tres cosas que nos sirven:

- **Solo pide resultados acotados.** No hay que saber la varianza ni la
  forma de la distribución: $U$ siempre está entre ${-1}$ y ${+1}$.
- **Vale para todo $N(s')$**, también para 3 o 10. La aproximación normal
  solo sirve con muchas simulaciones, y MCTS decide con pocas.
- **Cae exponencialmente** con $N(s')$. Otras cotas generales bajan solo
  como ${1/N(s')}$.

Mira solo **una cola**: el promedio por debajo. La sección 5 explica por
qué es el error que el bono tiene que cubrir.

::: exercise {#jue-c3-ej-fila-cota title="Calcula una fila de la cota"}
1. Con ${N(s')=100}$ y ${\varepsilon=0.2}$, calcula la cota de Hoeffding.
   ¿Coincide con la tabla?
2. Lo simulado fue 2.4 %. ¿Contradice eso la cota?
:::

::: hint {#jue-c3-pista-fila-cota-1 of="jue-c3-ej-fila-cota" title="El exponente"}
¿Cuánto vale ${N(s')\,\varepsilon^2/2}$ con esos números?
:::

::: answer {#jue-c3-resp-fila-cota of="jue-c3-ej-fila-cota"}
1. ${100\cdot0.04/2=2}$, y ${e^{-2}\approx0.14}$: el 13.5 % de la tabla.
2. No. La cota dice «a lo más»: 2.4 % está muy por debajo de 13.5 %. La
   cota es **holgada**, y a cambio vale para cualquier jugada acotada.
:::

## 3 · Despejar el margen

**Piensa: si aceptas equivocarte con probabilidad 5 %, ¿cuánto margen
necesitas?**

Ponle nombre a esa probabilidad.

::: definition {#jue-c3-delta title="La probabilidad de fallo"}
$\delta$ es la probabilidad de fallar por debajo que toleras: un número
entre 0 y 1. Pedimos que
${\Pr\bigl(\bar u(s')\le\mu(s')-\varepsilon\bigr)\le\delta}$.
:::

Basta con que la cota de Hoeffding valga $\delta$:

$$e^{-N(s')\,\varepsilon^2/2}=\delta.$$

Saca logaritmo, ${-N(s')\,\varepsilon^2/2=-\ln(1/\delta)}$, y despeja:

$$\varepsilon=\sqrt{\frac{2\ln(1/\delta)}{N(s')}}.$$

Léelo así: ${\bar u(s')+\varepsilon}$ es el **techo** de la jugada.
Antes de simular, la probabilidad de que el techo quede en $\mu(s')$ o
por debajo es a lo más $\delta$. No es el techo $\beta$ de alfa-beta:
aquí es un margen de error.

Por ejemplo, con ${\delta=e^{-2}\approx0.14}$ y ${N(s')=100}$, el margen es
${\sqrt{2\cdot2/100}=0.2}$: la fila de 100 de la tabla, leída al revés.
Con el 5 % de la pregunta y ${N(s')=100}$,
${\sqrt{2\cdot3.00/100}\approx0.24}$, porque ${\ln20\approx3.00}$.

::: exercise {#jue-c3-ej-despeja title="Mueve una perilla a la vez"}
1. Si $N(s')$ se multiplica por 4, ¿qué le pasa a $\varepsilon$?
2. Si pides un $\delta$ más chico, ¿el margen crece o se encoge? ¿Rápido o
   despacio?
:::

::: hint {#jue-c3-pista-despeja-1 of="jue-c3-ej-despeja" title="Dónde aparece cada cosa"}
¿Está $N(s')$ arriba o abajo de la fracción, y dentro de qué raíz? ¿Qué
función envuelve a ${1/\delta}$?
:::

::: answer {#jue-c3-resp-despeja of="jue-c3-ej-despeja"}
1. Se **divide entre 2**: $N(s')$ está abajo, dentro de una raíz, y
   ${\sqrt4=2}$.
2. **Crece, pero despacio**: ${1/\delta}$ entra por un logaritmo. Pedir
   diez veces menos fallo, de 0.05 a 0.005, hace crecer el margen solo un
   tercio.
:::

## 4 · Pedir más confianza mientras avanza

**Piensa: ¿sirve un mismo $\delta$, digamos 5 %, durante toda la
búsqueda?**

No. Con $\delta$ fijo, el margen de una jugada solo depende de su propia
$N(s')$. Si deja de elegirse, su techo **se congela**. Y la búsqueda hace
miles de vueltas: un 5 % de mala suerte pasa muchas veces. Basta una
racha mala al inicio para que la mejor quede con un techo bajo, congelado,
y no se vuelva a probar.

El arreglo es pedir **más confianza conforme avanza**. El reloj de la
búsqueda es $N(s)$, las vueltas que ya pasaron por el padre. La regla
**UCB1** de Auer, Cesa-Bianchi y Fischer (2002) equivale a tomar

$$\delta=\frac{1}{N(s)^4}.$$

Entonces ${\ln(1/\delta)=4\ln N(s)}$, y el margen queda

$$\begin{aligned}
\varepsilon&=\sqrt{\frac{8\ln N(s)}{N(s')}}\\
&=2\sqrt2\,\sqrt{\frac{\ln N(s)}{N(s')}}.
\end{aligned}$$

**Es el bono de UCT, con ${c=2\sqrt2\approx2.83}$.** Ahora una jugada que
no se elige ya no se congela. Su $N(s')$ se queda quieta, pero $N(s)$
sigue creciendo, y su bono también: despacio, por el logaritmo, pero sin
tope. Tarde o temprano vuelve a probarse.

El 4 es una **elección**, no una ley. Cuántas veces se prueba cada jugada
lo decide la regla con lo que ya salió, así que el margen no se usa una
vez sino en cada vuelta. El 4 hace que los fallos sean tan raros que,
sumados sobre todas las vueltas, siguen siendo pocos. Otro exponente daría
otra $c$.

> **En otros textos** el promedio se llama $Q(s,a)$, y verás
> ${c=\sqrt2}$ con la tasa ${G/N}$.
> Aquí ${\bar u\in[-1,1]}$ y ${c=2\sqrt2}$: es la misma regla. Como
> ${\bar u=2\,G/N-1}$, cada puntaje nuestro es el doble del de ellos menos 1,
> y el orden no cambia. Por lo mismo, con resultados entre 0 y 1 la cota de
> Hoeffding se escribe ${e^{-2N\varepsilon^2}}$: el intervalo es la mitad
> de ancho.

[[simular-en-vez-de-evaluar|Simular en vez de evaluar]] usó ${c=1}$, que
**explora menos** de lo que pide la teoría. Con ${N(s)=100}$:

::: table {#jue-c3-tabla-bono title="El bono con N(s) = 100"}
| $N(s')$ | ${c=2\sqrt2}$ | ${c=1}$ |
|---:|---:|---:|
| 10 | 1.92 | 0.68 |
| 30 | 1.11 | 0.39 |
| 60 | 0.78 | 0.28 |
:::

::: figure {#jue-c3-fig-bono title="El bono baja con N(s′) y sube con N(s)"}
![Gráfica. Eje x: N(s′), simulaciones de la jugada, de 0 a 200. Eje y: el bono 2√2·√(ln N(s)/N(s′)), en unidades de ū, de 0 a 4. Tres curvas, una por N(s): 100 continua, 1 000 con rayas y 10 000 con puntos; las tres bajan al crecer N(s′), y con más N(s) quedan más arriba. Puntos sobre la curva de 100 en N(s′) = 10, 30 y 60: el bono vale 1.92, 1.11 y 0.78. Una cuarta curva, tenue y de raya y punto, c = 1 con N(s) = 100, queda muy por debajo: 0.68 en N(s′) = 10](../_assets/jue-c3-bono.svg)
:::

Un techo de más de 1 no informa nada: $\mu(s')$ nunca pasa de 1. Los
bonos salen tan grandes porque pedir ${\delta=N(s)^{-4}}$ es pedir mucha
confianza, a propósito. Por eso **$c$ es una perilla** que se ajusta: una
$c$ más chica pide menos confianza y explora menos.

::: exercise {#jue-c3-ej-teoria title="Recalcula el ejercicio de MCTS con la c de la teoría"}
En el ejercicio de MCTS (@jue-c3-ej-mcts), x tenía ${N=60}$ y
${\bar u=0.5}$; y, ${N=30}$ y ${0.6}$; z, ${N=10}$ y ${0.2}$. ${N(s)=100}$.
Con ${c=1}$ la selección iba a y.

1. Con los bonos de la tabla para ${c=2\sqrt2}$, calcula los tres
   puntajes.
2. ¿Por cuál baja ahora la selección?
:::

::: hint {#jue-c3-pista-teoria-1 of="jue-c3-ej-teoria" title="Qué fila va con qué jugada"}
Cada jugada usa la fila de su propia $N(s')$. ¿Cuál tiene la más chica?
:::

::: answer {#jue-c3-resp-teoria of="jue-c3-ej-teoria"}
1. x: ${0.5+0.78=1.28}$; y: ${0.6+1.11=1.71}$; z: ${0.2+1.92=2.12}$.
2. **z.** Con la $c$ de la teoría pesa más lo poco probado: la selección
   cambia de y a z.
:::

## 5 · Elegir con optimismo

**Piensa: ¿por qué se suma el margen? ¿No sería más prudente restarlo?**

Porque los dos errores no cuestan lo mismo:

::: table {#jue-c3-tabla-optimismo title="Equivocarse por arriba o por abajo"}
| Error | Qué pasa |
|---|---|
| Creer buena una mala | Se prueba, su $\bar u$ baja, su bono también: **se corrige solo** |
| Creer mala una buena | No se prueba más: **nada la corrige** |
:::

Sumar el margen es elegir con **optimismo**: cada jugada vale lo más que
podría valer. Si el optimismo se equivoca, probarla lo arregla. Sin
margen pasa lo mismo que con pesimismo: en la sección 1, x quedó creída
mala tras una derrota y nada la corrigió.

Por eso, para **construir** el bono basta una cola de Hoeffding: solo nos
asusta subestimar. La prueba de que la regla funciona usa también la
otra, la que hace bajar a una jugada sobreestimada al probarla.

Dos casos extremos:

- **Una jugada sin probar** tiene ${N(s')=0}$: el bono divide entre 0 y
  vale infinito. Se prueba antes que cualquier otra.
- **En un nodo de MIN**, MIN quiere $\bar u$ bajo. Su optimismo es desde
  su lado: imagina cada hijo tan bajo como podría ser. El ejercicio final
  lo pone en números.

::: exercise {#jue-c3-ej-optimismo title="Compara dos jugadas empatadas"}
Dos jugadas de MAX tienen ${\bar u=0.3}$. Una lleva 1 simulación; la
otra, 100.

1. ¿Cuál tiene el techo más alto?
2. Si la de 1 simulación era en realidad mala, ¿qué pasa al probarla
   unas veces?
:::

::: hint {#jue-c3-pista-optimismo-1 of="jue-c3-ej-optimismo" title="Qué mueve cada número"}
¿Qué parte del puntaje depende de $N(s')$? ¿Qué le pasa a $\bar u$ y a esa
parte cuando una jugada mala se prueba más?
:::

::: answer {#jue-c3-resp-optimismo of="jue-c3-ej-optimismo"}
1. La de **1 simulación**: mismo promedio, bono mucho mayor.
2. Su $\bar u$ baja hacia su $\mu$ y su bono se encoge con cada prueba.
   Su techo cae debajo del de la otra y la selección vuelve a ella. El
   error costó unas cuantas vueltas, no la partida.
:::

## 6 · Verlo converger

**Piensa: ¿cómo se compara una regla de selección con otra?**

Contando cuántas vueltas van a la mejor jugada. Volvamos a la corrida de la
sección 1, con la misma semilla, pero eligiendo por puntaje con
${c=2\sqrt2}$. Las vueltas 1 a 5 salen igual: x, y, z, z, z. En la vuelta
6, x e y tienen ${\bar u=-1}$ con una simulación cada una; z tiene
${\bar u=-1/3}$ con tres. ${N(s)=5}$.

::: exercise {#jue-c3-ej-vuelta-seis title="Decide la vuelta 6"}
Usa ${\ln5\approx1.61}$ y ${2\sqrt2\approx2.83}$.

Calcula el puntaje de x y el de z. y empata con x; si hay empate, gana la
primera en orden x, y, z. ¿Qué jugada elige UCB?
:::

::: hint {#jue-c3-pista-vuelta-seis-1 of="jue-c3-ej-vuelta-seis" title="Qué va en cada raíz"}
Dentro de la raíz va ${\ln N(s)}$ entre la $N(s')$ de cada jugada. ¿Cuál
es la $N(s')$ de x y cuál la de z?
:::

::: answer {#jue-c3-resp-vuelta-seis of="jue-c3-ej-vuelta-seis"}
- **x:** bono ${2.83\sqrt{1.61/1}\approx3.59}$;
  puntaje ${-1+3.59=2.59}$.
- **z:** bono ${2.83\sqrt{1.61/3}\approx2.07}$;
  puntaje ${-0.33+2.07=1.74}$, con ${-1/3\approx-0.33}$.

Elige **x**, por el empate con y. Gana por el bono: x lleva una simulación
y z, tres. El bono de x, 3.59, es casi el doble del de z, 2.07, y compensa
su peor promedio. «Siempre el mejor promedio» se quedaba en z.

Tras 12 vueltas la secuencia es x y z z z x y x y x y x, y quedan
${N=5,4,3}$: la mayoría en x.
:::

Una corrida es suerte. La figura promedia 40 corridas de 10 000 vueltas
y compara cuatro reglas. «A veces al azar (10 %)» elige el mejor promedio,
salvo una vuelta de cada diez, que elige al azar.

::: figure {#jue-c3-fig-bandido title="UCB empieza abajo y termina arriba"}
![Gráfica con eje x logarítmico. Eje x: N(s), vueltas, de 10 a 10 000. Eje y: fracción de las vueltas que fueron a la mejor jugada, x, de 0 a 1. Promedio de 40 corridas, con μ de x, y, z: 0.6, 0.3, −0.2. Cuatro curvas: siempre el mejor promedio sube de 0.61 a 0.85 y se aplana; a veces al azar (10 %) sube de 0.60 a 0.93 y no pasa de ahí; UCB con c = 2√2 empieza más abajo, en 0.42, y llega a 0.94; UCB con c = 1 sube más rápido y llega a 0.99](../_assets/jue-c3-bandido.svg)
:::

- **Siempre el mejor promedio** se queda en 0.85: en algunas corridas se
  atora, como en la sección 1.
- **A veces al azar** llega a 0.93 y se detiene: aunque ya sepa cuál es
  la mejor, una vuelta de cada diez la sigue tirando al azar.
- **UCB con ${c=2\sqrt2}$** empieza en 0.42, porque explora, y llega a
  0.94. Sigue subiendo: su bono se encoge donde ya hay evidencia.
- **UCB con ${c=1}$**, el de la página anterior, llega a 0.99: aquí llega
  antes. Con ${c=0}$ no hay bono y es el mejor promedio, 0.85; con
  ${c=5}$ explora de más y llega a 0.87.

Con cualquier ${c>0}$, el bono de una jugada olvidada crece sin tope:
ninguna se queda sin probar para siempre. Con ${c=0}$ eso sí puede pasar.
Lo que la teoría acota, con ${c=2\sqrt2}$, es cuántas vueltas se pierden
en las otras; con ${c=1}$ no hay esa cota, aunque aquí funcione mejor.

## 7 · Seleccionar no es entregar

**Piensa: cuando se acaba el tiempo, ¿se entrega la jugada de mayor
puntaje?**

No. Al terminar, el bono **se quita**:

::: table {#jue-c3-tabla-seleccionar title="Seleccionar no es entregar"}
| | Selección | Entrega |
|---|---|---|
| Cuándo | Cada vuelta | Al final |
| Mira | Puntaje | $N(s')$ |
| Bono | Sí | No |
| Busca | Qué probar | Lo más probado |
:::

El bono premia la ignorancia, y eso sirve para aprender. Para jugar de
verdad se quiere evidencia: la jugada con más simulaciones.

::: exercise {#jue-c3-ej-entregar title="Señala qué se entrega"}
En el ejercicio de MCTS, x tenía ${N=60}$ y ${\bar u=0.5}$; y, ${N=30}$ y
${0.6}$; z, ${N=10}$ y ${0.2}$. Con ${c=2\sqrt2}$ la selección iba a z. Se
acaba el tiempo.

1. ¿Qué jugada se entrega?
2. y tiene el mejor promedio. ¿Por qué no se entrega y?
:::

::: hint {#jue-c3-pista-entregar-1 of="jue-c3-ej-entregar" title="Promedio y evidencia"}
¿Qué cambia entre seleccionar y entregar: qué número mira cada uno?
:::

::: answer {#jue-c3-resp-entregar of="jue-c3-ej-entregar"}
1. **x**, la de más simulaciones, 60. Ni z, la que seleccionaba, ni y.
2. El 0.6 de y descansa en 30 simulaciones, la mitad que x: su margen es
   mayor y su promedio, menos confiable. Además, la selección manda más
   vueltas a lo que parece mejor, así que la más simulada es la que la
   búsqueda confirmó más veces.
:::

## 8 · Pasar del bandido al árbol

**Piensa: en MCTS, ¿las simulaciones que pasan por un nodo siguen siendo
independientes?**

No del todo. MCTS pone un bandido **en cada nodo** del árbol: elige entre
sus hijos con el mismo puntaje. Eso es **UCT**: UCB1 aplicado a árboles.
Pero debajo de cada hijo hay otros bandidos que van aprendiendo.

Así que los resultados de un hijo ya no son independientes: lo que se
elige abajo depende de lo que salió antes. Lo que promedian tampoco es el
$\mu(s')$ de la definición, que supone que los dos juegan al azar, sino
algo que cambia con la búsqueda.

Que cambie no basta para romper Hoeffding, que no pide la misma
distribución en cada simulación; lo que la rompe es la dependencia. Por
eso Hoeffding no se aplica al pie de la letra. Kocsis y Szepesvári (2006)
demostraron aparte que UCT, con una $c$ bastante grande, llega a la mejor
jugada con suficientes vueltas. Esa prueba no la cubrimos.

Lo que te llevas es la intuición: el bono es un margen de
error, y se suma porque el optimismo se corrige solo.

## 9 · Aplicar el bono por tu cuenta

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-bono title="Aplica el bono en un nodo de MIN"}
Un nodo $s$ donde **mueve MIN** lleva ${N(s)=50}$ vueltas. Sus tres hijos
tienen, con $\bar u$ medido desde MAX y sin cambiarle el signo:

- **p:** ${N=30}$, ${\bar u=-0.2}$;
- **q:** ${N=15}$, ${\bar u=0}$;
- **r:** ${N=5}$, ${\bar u=0.4}$.

Trata a cada hijo como una jugada del bandido: no importa qué pasa debajo
de él, ni cómo se llegó a esos números.

La idea nueva: ahora elige **MIN**, que quiere $\bar u$ bajo. Usa
${\ln50\approx3.91}$, ${\ln20\approx3.00}$ y ${2\sqrt2\approx2.83}$.

1. Con ${\delta=0.05}$, calcula el margen de p. ¿Qué lado de $\mu(p)$ le
   importa a MIN, y qué dice de él?
2. Calcula el puntaje de cada hijo con ${c=2\sqrt2}$. ¿Por cuál baja la
   selección?
3. Repite con ${c=1}$.
4. Si $s$ fuera la raíz y se acabara el tiempo, ¿qué jugada se entrega?
:::

::: hint {#jue-c3-pista-final-bono-1 of="jue-c3-ej-final-bono" title="Pista 1 · Desde qué lado"}
¿Qué número quiere MIN que sea chico? ¿Qué parte del puntaje no depende
de quién elige?
:::

::: hint {#jue-c3-pista-final-bono-2 of="jue-c3-ej-final-bono" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿El hijo menos probado recibió
el bono más grande? ¿Usaste el puntaje solo para seleccionar, y otra cosa
para entregar?
:::

::: answer {#jue-c3-resp-final-bono of="jue-c3-ej-final-bono" title="Respuesta · Optimismo desde el lado de MIN"}
1. **El margen de p.** ${\varepsilon=\sqrt{2\cdot3.00/30}\approx0.45}$. A
   MIN le importa que $\mu(p)$ sea **más bajo** de lo que parece, la otra
   cola. Su piso optimista es ${-0.2-0.45=-0.65}$. Antes de simular, la
   probabilidad de que ese piso quede en $\mu(p)$ o por encima es a lo más
   5 %.
2. **El puntaje con ${c=2\sqrt2}$.** MIN baja al hijo de piso
   ${\bar u-\text{bono}}$ más bajo. Es lo mismo que cambiar el signo, como
   en [[simular-en-vez-de-evaluar|Simular en vez de evaluar]], y elegir el
   mayor: puntaje ${=-\bar u+\text{bono}}$. Bonos: p 1.02, q 1.44, r 2.50.
   Puntajes: p ${0.2+1.02=1.22}$, q ${0+1.44=1.44}$, r
   ${-0.4+2.50=2.10}$. Baja por **r**: el peor promedio para MIN, pero
   con solo 5 simulaciones.

   El bono de p, 1.02, es más del doble del margen del inciso 1: con
   ${c=2\sqrt2}$ se pide ${\delta=1/50^4}$, mucho menos que 5 %.
3. **El puntaje con ${c=1}$.** Bonos 0.36, 0.51 y 0.88; puntajes 0.56,
   0.51 y 0.48. Baja por **p**: la $c$ chica casi no explora.
4. **Lo que se entrega.** **p**, la de más simulaciones, 30. Entregar no
   usa el bono.
:::

**Punto de control:** deberías poder despejar el margen de una jugada
dados $\delta$ y $N(s')$, decir por qué $\delta$ baja con $N(s)$, y
calcular el puntaje en un nodo de MAX o de MIN.

## Lo que hay que llevarse

- **El bono es un margen de error.** Hoeffding acota cuánto falla un
  promedio de resultados entre ${-1}$ y ${+1}$:
  ${e^{-N(s')\varepsilon^2/2}}$. Con la jugada y, ${\varepsilon=0.2}$ y
  ${N(s')=100}$, la cota es 13.5 % y lo simulado, 2.4 %.
- **Despejar** da ${\varepsilon=\sqrt{2\ln(1/\delta)/N(s')}}$. Pedir
  ${\delta=N(s)^{-4}}$, cada vez más confianza, da el bono de UCT con
  ${c=2\sqrt2\approx2.83}$; con la tasa ${G/N}$ es ${c=\sqrt2}$, la misma
  regla.
- **Se suma por optimismo:** creer buena una mala se corrige al probarla;
  creer mala una buena, nunca. MIN usa el piso, ${\bar u-\text{bono}}$;
  una jugada sin probar tiene bono infinito.
- **Siempre el mejor promedio se atora:** con una semilla, 998 de 1 000
  vueltas en z, la peor. A 10 000 vueltas, en la mejor: mejor promedio
  0.85, a veces al azar 0.93, UCB con ${c=2\sqrt2}$ 0.94, con ${c=1}$ 0.99.
  $c$ es una perilla.
- **Seleccionar usa el bono; entregar, no.** En el ejercicio de MCTS, con
  ${c=2\sqrt2}$ la selección va a z (2.12) y con ${c=1}$ a y; se entrega
  x, con 60 simulaciones.

Continúa con [[juegos-sin-turnos|la clase 4, cuando no hay turnos]].
