---
id: de-donde-sale-el-bono
title: De dónde sale el bono
nav_title: De dónde sale el bono
summary: "El bono de UCT es el margen de error de un promedio: sumado, da la cota optimista de cada jugada. Sale de la desigualdad de Hoeffding con una probabilidad de fallo que baja conforme avanza la búsqueda, y esa probabilidad es la c del puntaje. Se usa para seleccionar, no para entregar."
status: ready
estimated_time: 37m
tags: [juegos, mcts, exploracion]
---

# De dónde sale el bono

**¿Cómo evitar que la regla de selección se atore, y por qué el bono tiene
justo esa forma?**

Al terminar tendrás:

- una corrida donde elegir **siempre el mejor promedio** se atora en la
  peor jugada, y la razón: no duda de un promedio;
- la **desigualdad de Hoeffding**, y de ella el **margen** $\varepsilon$
  que corresponde a una probabilidad de fallo $\delta$;
- la **cota optimista** ${\bar u+\varepsilon}$: qué significa, por qué se
  elige la más alta y cómo la usa MIN;
- la $c$ del puntaje leída como un $\delta$ que baja con $N(s)$:
  ${c=\sqrt{2k}}$ si ${\delta=N(s)^{-k}}$;
- cuatro reglas comparadas en 40 corridas, y el bono usado al
  **seleccionar** pero no al **entregar**.

> **Lo que traes de [[simular-en-vez-de-evaluar|Simular en vez de evaluar]].**
> Una simulación (@jue-c3-simulacion) termina en ${U=+1}$ o ${U=-1}$. Cada
> nodo $s'$ guarda $N(s')$ simulaciones y $G(s')$ victorias de MAX; su
> promedio $\bar u(s')$ va de ${-1}$ a ${+1}$, siempre visto desde MAX. La
> regla **UCT** baja al hijo de mayor puntaje: $\bar u(s')$ más el bono
> ${c\sqrt{\ln N(s)/N(s')}}$, donde $s$ es el padre; en un nodo de MIN,
> ${-\bar u(s')}$ más el bono. Allá usamos ${c=1}$.

> **El juego de esta página.** Tres jugadas en la raíz, x, y, z, como en el
> ejercicio de MCTS (@jue-c3-ej-mcts). Cada vuelta elige una, juega una
> simulación y anota ${U=\pm1}$. No hay árbol debajo: solo esta elección,
> repetida. La regla de UCT en un solo nodo se llama **UCB1**; UCT es UCB1
> repetida en cada nodo del árbol, y vuelve en la sección 8.

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
> - **Notebook en Colab**: en la sección 8 del notebook están las mismas
>   simulaciones de esta página, para correrlas tú.
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
   esta corrida, tras 1 000 vueltas, x e y tienen una simulación cada una y
   z, 998. La regla se atoró en la peor jugada.
:::

La regla se atoró porque **creyó** un promedio hecho con una sola
simulación. Le falta dudar. Pero ¿cuánto debería dudar de un promedio?
Para contestarlo hay que medir cuánto puede fallar uno.

## 2 · Medir cuánto falla un promedio

**Piensa: con 10 simulaciones, ¿qué tan seguido queda el promedio muy por
debajo del verdadero?**

Se puede medir. Toma la jugada y, con ${\mu=0.3}$. Juega $N(s')$
simulaciones, saca su promedio y repite todo 20 000 veces. Cuenta en
cuántas el promedio quedó al menos $\varepsilon$ por debajo.

**¿Por qué por debajo?** Es el error que atoró la regla de la sección 1:
x vale de verdad ${\mu=0.6}$, su única simulación la dejó en ${-1}$, y
nadie la volvió a probar. Un promedio que se pasa por arriba se corrige
solo, porque la regla lo sigue eligiendo y junta simulaciones. Uno que se
queda corto no se corrige nunca.

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
| 10 | 24.7 % | 81.9 % |
| 50 | 7.1 % | 36.8 % |
| 100 | 2.4 % | 13.5 % |
| 200 | 0.2 % | 1.8 % |
:::

En la gráfica, cada punto es la frecuencia de fallo de una $N(s')$,
contada en las 20 000 tiradas; la línea es la cota.

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

**Fuente:** W. Hoeffding, «Probability inequalities for sums of bounded
random variables», *Journal of the American Statistical Association*,
1963, teorema 2.
:::

**¿Por qué esta desigualdad y no otra?** Por tres cosas que nos sirven:

- **Solo pide resultados independientes y acotados.** No hay que saber la varianza ni la
  forma de la distribución: $U$ siempre está entre ${-1}$ y ${+1}$.
- **Vale para todo $N(s')$**, también para 3 o 10. La aproximación normal
  solo sirve con muchas simulaciones, y MCTS decide con pocas.
- **Cae exponencialmente** con $N(s')$. Otras cotas generales bajan solo
  como ${1/N(s')}$.

Nos basta **una cola**: el promedio por debajo, el error que no se corrige
solo. La otra cola sirve a MIN, en la sección 4.

::: exercise {#jue-c3-ej-fila-cota title="Calcula una fila de la cota"}
1. Con ${N(s')=100}$ y ${\varepsilon=0.2}$, calcula la cota de Hoeffding.
   ¿Coincide con la tabla?
2. Lo simulado fue 2.4 %. ¿Contradice eso la cota?
:::

::: hint {#jue-c3-pista-fila-cota-1 of="jue-c3-ej-fila-cota" title="El exponente"}
¿Cuánto vale ${N(s')\,\varepsilon^2/2}$ con esos números?
:::

::: answer {#jue-c3-resp-fila-cota of="jue-c3-ej-fila-cota"}
1. ${100\cdot0.04/2=2}$, y ${e^{-2}\approx0.14}$: el 13.5 % de la tabla.
2. No. La cota dice «a lo más»: 2.4 % está muy por debajo de 13.5 %. La
   cota es **holgada**, y a cambio vale para cualquier jugada acotada.
:::

Hoeffding dice qué tan seguido falla un promedio por un margen dado. Al
revés también sirve: si fijas qué tan seguido aceptas fallar, ¿qué margen
le das a cada promedio?

## 3 · Despejar el margen

**Piensa: si aceptas equivocarte con probabilidad 5 %, ¿cuánto margen
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

Léelo en palabras: $\varepsilon$ es cuánto por debajo de $\mu(s')$ puede
quedar el promedio, salvo una mala suerte de probabilidad $\delta$. Se
encoge con las simulaciones de la jugada y crece si pides menos fallo.

Por ejemplo, con ${\delta=e^{-2}\approx0.14}$ y ${N(s')=100}$, el margen es
${\sqrt{2\cdot2/100}=0.2}$: la fila de 100 de la tabla, leída al revés.
Con el 5 % de la pregunta y ${N(s')=100}$,
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

Ya cada jugada tiene su margen. ¿Qué se hace con él al elegir: sumarlo al
promedio, o restarlo?

## 4 · Elegir con optimismo

**Piensa: ¿por qué se suma el margen? ¿No sería más prudente restarlo?**

Porque los dos errores no cuestan lo mismo:

::: table {#jue-c3-tabla-optimismo title="Equivocarse por arriba o por abajo"}
| Error | Qué pasa |
|---|---|
| Creer buena una mala | Se prueba, su $\bar u$ baja, su margen también: **se corrige solo** |
| Creer mala una buena | No se prueba más: **nada la corrige** |
:::

Piensa en x tras la sección 1: perdió su única simulación. ¿Qué tan buena
podría ser sin que ese dato te contradiga? Bastante: una jugada que gana
cuatro de cada cinco veces pierde la primera con facilidad. Esa pregunta,
con un número por respuesta, es la cota optimista.

::: definition {#jue-c3-cota-optimista title="La cota optimista"}
La **cota optimista** de una jugada es su promedio más su margen,
${\bar u(s')+\varepsilon}$. Es un número en la escala de $U$, visto desde
MAX, y puede pasar de ${+1}$.

**Qué significa:** lo más que $\mu(s')$ podría valer sin que los datos lo
desmientan. Elegir con **optimismo** es elegir la jugada de cota más alta.

**Qué no es:** no es el techo $\beta$ de alfa-beta ni el techo de la tabla
de transposición. Aquí no hay ventana: hay un margen de error.
:::

**¿Qué tan seguido se equivoca?** La cota falla si queda en $\mu(s')$ o
por debajo. Pasa $\varepsilon$ al otro lado:

$$\begin{aligned}
&\bar u(s')+\varepsilon\le\mu(s')\\
&\iff\bar u(s')\le\mu(s')-\varepsilon.
\end{aligned}$$

Es justo el fallo por debajo de @jue-c3-margen, el que Hoeffding acota.
Con el $\varepsilon$ de la sección 3, antes de simular la probabilidad de
que la cota quede en $\mu(s')$ o por debajo es a lo más $\delta$.

**En la corrida de la sección 1.** Tras cinco vueltas, x tiene
${\bar u=-1}$ con una simulación; z, ${\bar u=-1/3}$ con tres. «Siempre el
mejor promedio» sigue en z. Toma un $\delta$ muy chico, ${1/625}$; la
sección 5 dice de dónde sale. Como ${\ln625\approx6.44}$:

- x: margen ${\sqrt{2\cdot6.44/1}\approx3.59}$, cota ${-1+3.59=2.59}$;
- z: margen ${\sqrt{2\cdot6.44/3}\approx2.07}$, cota ${-0.33+2.07=1.74}$.

La cota de x es la más alta: **se le da otra oportunidad a x**. Una
derrota en una simulación casi no informa, y la cota lo dice.

**¿Y una cota de 2.59, si $\mu$ nunca pasa de 1?** No estorba. La regla no
lee la cota como un valor: solo la compara con las otras. Lo que importa es
el orden, y una cota alta solo dice «aún no sé casi nada de esta jugada».

Si el optimismo se equivoca, probarla lo arregla. Sin margen pasa lo mismo
que con pesimismo: en la sección 1, x quedó creída mala tras una derrota y
nada la corrigió. Sumar el margen es lo que hace el bono de la página
anterior.

Dos casos extremos:

- **Una jugada sin probar** tiene ${N(s')=0}$: el bono divide entre 0 y
  vale infinito. Se prueba antes que cualquier otra.
- **En un nodo de MIN**, MIN quiere $\bar u$ bajo. Su cota optimista, desde
  su lado, es ${\bar u(s')-\varepsilon}$: lo más bajo que $\mu(s')$ podría
  ser. Elige la más baja. Falla si queda en $\mu(s')$ o por encima: la otra
  cola, que @jue-c3-teo-hoeffding acota igual.

::: exercise {#jue-c3-ej-optimismo title="Compara dos jugadas empatadas"}
Dos jugadas de MAX tienen ${\bar u=0.3}$. Una lleva 1 simulación; la
otra, 100.

1. ¿Cuál tiene la cota optimista más alta?
2. Si la de 1 simulación era en realidad mala, ¿qué pasa al probarla
   unas veces?
:::

::: hint {#jue-c3-pista-optimismo-1 of="jue-c3-ej-optimismo" title="Qué mueve cada número"}
¿Qué parte de la cota depende de $N(s')$? ¿Qué le pasa a $\bar u$ y a esa
parte cuando una jugada mala se prueba más?
:::

::: answer {#jue-c3-resp-optimismo of="jue-c3-ej-optimismo"}
1. La de **1 simulación**: mismo promedio, margen mucho mayor.
2. Su $\bar u$ baja hacia su $\mu$ y su margen se encoge con cada prueba.
   Su cota cae debajo de la de la otra y la selección vuelve a ella. El
   error costó unas cuantas vueltas, no la partida.
:::

Falta escoger $\delta$. ¿Sirve uno fijo, como el 5 %? ¿Y de dónde salió
el ${1/625}$ de la corrida?

## 5 · Pedir más confianza mientras avanza

**Piensa: ¿sirve un mismo $\delta$, digamos 5 %, durante toda la
búsqueda?**

No. Con $\delta$ fijo, el margen de una jugada solo depende de su propia
$N(s')$. Si deja de elegirse, su cota **se congela**. Y la búsqueda hace
miles de vueltas: un 5 % de mala suerte pasa muchas veces. Basta una
racha mala al inicio para que la mejor quede con una cota baja, congelada,
y no se vuelva a probar.

El arreglo es pedir **más confianza conforme avanza**. El reloj de la
búsqueda es $N(s)$, las vueltas que ya pasaron por el padre. Mira otra vez
el puntaje de la página anterior:

$$\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

No tiene $\delta$, pero tiene $\ln N(s)$. Prueba un $\delta$ que baje con
el reloj, ${\delta=N(s)^{-k}}$ para algún ${k>0}$. Entonces
${\ln(1/\delta)=k\ln N(s)}$, y el margen de la sección 3 queda

$$\begin{aligned}
\varepsilon&=\sqrt{\frac{2k\ln N(s)}{N(s')}}\\
&=\sqrt{2k}\,\sqrt{\frac{\ln N(s)}{N(s')}}.
\end{aligned}$$

**Es el bono del puntaje, con ${c=\sqrt{2k}}$.** La $c$ es $\delta$
disfrazada: cada $c$ pide un $\delta$, y al revés, ${k=c^2/2}$. El puntaje
es la cota optimista de la sección 4.

::: table {#jue-c3-tabla-c-delta title="La c del puntaje y el δ que pide"}
| $c$ | $k$ | $\delta$ | $\delta$ con ${N(s)=100}$ |
|---|---:|---|---:|
| $1$ | $1/2$ | $N(s)^{-1/2}$ | 10 % |
| $2\sqrt2$ | $4$ | $N(s)^{-4}$ | $10^{-8}$ |
:::

La ${c=1}$ de la página anterior es ${k=1/2}$: con 100 vueltas tolera
fallar una vez de cada diez. Pide poca confianza, y explora poco.

La regla **UCB1** de Auer, Cesa-Bianchi y Fischer (2002) toma ${k=4}$:

$$\delta=\frac{1}{N(s)^4}.$$

Entonces ${\ln(1/\delta)=4\ln N(s)}$, y el margen queda

$$\begin{aligned}
\varepsilon&=\sqrt{\frac{8\ln N(s)}{N(s')}}\\
&=2\sqrt2\,\sqrt{\frac{\ln N(s)}{N(s')}}.
\end{aligned}$$

**Es el bono de UCT, con ${c=2\sqrt2\approx2.83}$.** En la corrida de la
sección 4, ${N(s)=5}$, y ${5^{-4}=1/625}$: de ahí salía ese $\delta$.
Ahora una jugada que no se elige ya no se congela. Su $N(s')$ se queda
quieta, pero $N(s)$ sigue creciendo, y su bono también: despacio, por el
logaritmo, pero sin tope. Tarde o temprano vuelve a probarse.

El 4 es una **elección**, no una ley. Cuántas veces se prueba cada jugada
lo decide la regla con lo que ya salió, así que el margen no se usa una
vez sino en cada vuelta. El 4 hace que los fallos sean tan raros que,
sumados sobre todas las vueltas, siguen siendo pocos. Otro exponente daría
otra $c$.

> **En otros textos** el promedio se llama $Q(s,a)$, y verás
> ${c=\sqrt2}$ con la tasa ${G/N}$, de 0 a 1. Como
> ${\bar u=2\,G/N-1}$, cada puntaje nuestro es el doble del de ellos menos 1
> cuando ellos usan la mitad de nuestra $c$. Con ${b=\sqrt{\ln N(s)/N(s')}}$:
>
> $$\bar u+c\,b=2\Bigl(\frac GN+\frac c2\,b\Bigr)-1.$$
>
> Doblar y restar 1 no cambia el orden: su ${c=\sqrt2}$ es nuestra
> ${c=2\sqrt2}$, la misma regla. Con la **misma** $c$ en las dos escalas,
> en cambio, ${G/N}$ explora el doble, y la elección puede cambiar. Por lo
> mismo, con resultados entre 0 y 1 la cota de
> Hoeffding se escribe ${e^{-2N\varepsilon^2}}$: el intervalo es la mitad de ancho.

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

Los bonos con ${c=2\sqrt2}$ salen grandes porque ${\delta=N(s)^{-4}}$ pide
mucha confianza, a propósito. Por eso **$c$ es una perilla**: una $c$ más
chica pide un $\delta$ más grande y explora menos.

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

Con cualquier ${c>0}$ ninguna jugada queda olvidada para siempre. Pero
¿llega la regla a la mejor jugada, y qué tan pronto?

## 6 · Verlo converger

**Piensa: ¿cómo se compara una regla de selección con otra?**

Contando cuántas vueltas van a la mejor jugada. Volvamos a la corrida de la
sección 1, con la misma semilla, pero eligiendo por puntaje con
${c=2\sqrt2}$. Las vueltas 1 a 5 salen igual: x, y, z, z, z.

¿Por qué igual? Las vueltas 1 a 3 prueban cada jugada una vez. En la 4,
las tres llevan una simulación y el mismo bono, así que gana el mejor
promedio, z. En la 5, ${N(s)=4}$: z lleva ${\bar u=0}$ con dos; x e y,
${-1}$ con una. z gana por poco, ≈2.35 contra ≈2.33 de x y de y, empatadas.

En la vuelta 6, x e y tienen ${\bar u=-1}$ con una simulación cada una; z tiene
${\bar u=-1/3}$ con tres. ${N(s)=5}$.

::: exercise {#jue-c3-ej-vuelta-seis title="Comprueba la vuelta 6 con el puntaje"}
Usa ${\ln5\approx1.61}$ y ${2\sqrt2\approx2.83}$.

Calcula el puntaje de x y el de z. y empata con x; si hay empate, gana la
primera en orden x, y, z. ¿Qué jugada elige UCB1? ¿Coinciden los puntajes
con las cotas de la sección 4?
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

Elige **x**: empata con y, 2.59 las dos, y va primero. Gana por el bono:
x lleva una simulación y z, tres. El bono de x, 3.59, es unas 1.7 veces
el de z, 2.07 (${\sqrt3}$, porque z tiene el triple de simulaciones), y
compensa su peor promedio. «Siempre el mejor promedio» se quedaba en z.

Son las cotas de la sección 4: con ${N(s)=5}$, el $\delta$ de UCB1 es
${5^{-4}=1/625}$.

Tras 12 vueltas la secuencia es x y z z z x y x y x y x, y quedan
${N=5,4,3}$: la mayoría en x.
:::

Una corrida es suerte: con otra semilla, la regla sin bono pudo no
atorarse. Para comparar reglas hay que correr cada una muchas veces. Las
dos figuras que siguen comparan cuatro reglas en 40 corridas de 10 000
vueltas cada una, con las semillas 1 a 40. «A veces al azar (10 %)» elige
el mejor promedio, salvo una vuelta de cada diez, que elige al azar.

**La primera figura contesta: ¿cada regla encuentra la mejor jugada en
cada corrida?** Cada punto es **una corrida**. Su posición en el eje x es
la fracción de sus 10 000 vueltas que fue a x, la mejor: 1 si casi todas,
0 si casi ninguna. Hay una fila de 40 puntos por regla, y una raya marca
el promedio de la fila.

::: figure {#jue-c3-fig-bandido-corridas title="Cada corrida, un punto: sin bono es todo o nada"}
![Gráfica de puntos, una fila por regla: siempre el mejor promedio, a veces al azar (10 %), UCB con c = 2√2 y UCB con c = 1. Eje x: fracción de las 10 000 vueltas de una corrida que fueron a x, de 0 a 1. Cada punto es una corrida, con μ de x, y, z: 0.6, 0.3, −0.2; 40 por fila, semillas 1 a 40; una raya marca el promedio de la fila. Siempre el mejor promedio: 34 corridas cerca de 1 y 6 atoradas cerca de 0, 5 en y y 1 en z; su promedio, 0.85, cae entre los dos grupos, donde no hay ninguna corrida. A veces al azar, UCB con c = 2√2 y UCB con c = 1: ninguna atorada; la corrida más baja de cada una deja en x 0.90, 0.92 y 0.96 de sus vueltas](../_assets/jue-c3-bandido-corridas.svg)
:::

- **Siempre el mejor promedio** es todo o nada: 34 corridas van casi
  siempre a x y 6 se atoran lejos de ella, 5 en y y 1 en z. Su promedio,
  0.85 (casi ${34/40}$), no es «elige bien el 85 % de las veces»: en
  ninguna corrida pasa eso.
- **Las otras tres** no se atoran nunca. Su corrida más baja va a x 0.90,
  0.92 y 0.96 de las vueltas.

**La segunda figura contesta: ¿qué tan pronto llega cada regla?** La figura
promedia 40 corridas de 10 000 vueltas, pero mira cada momento de la
búsqueda. El eje x es la
vuelta $N(s)$. El eje y es la fracción **acumulada**: de las vueltas 1 a
$N(s)$, cuántas fueron a x. Una vuelta perdida al inicio pesa en toda la
curva.

::: figure {#jue-c3-fig-bandido title="La fracción acumulada: UCB paga al principio lo que explora"}
![Gráfica con eje x logarítmico. Eje x: N(s), vueltas, de 10 a 10 000. Eje y: fracción acumulada de las vueltas que fueron a la mejor jugada, x, desde la vuelta 1 hasta N(s), de 0 a 1. Promedio de 40 corridas, con μ de x, y, z: 0.6, 0.3, −0.2. Cuatro curvas: siempre el mejor promedio sube de 0.61 a 0.85 y se aplana; a veces al azar (10 %) sube de 0.60 a 0.93 y se queda cerca de ahí; UCB con c = 2√2 empieza más abajo, en 0.42, y llega a 0.94; UCB con c = 1 sube más rápido y llega a 0.99](../_assets/jue-c3-bandido.svg)
:::

- **Siempre el mejor promedio** se queda en 0.85: las 6 corridas atoradas
  ya no suben, y las otras 34 ya están arriba.
- **A veces al azar** llega a 0.93 y se queda cerca de ahí: aunque ya
  sepa cuál es la mejor, una vuelta de cada diez la sigue tirando al azar.
  Le atina a x en una de cada tres, así que en promedio se espera
  ${0.9+0.1/3\approx0.93}$; 14 de las 40 corridas lo pasan un poco.
- **UCB con ${c=2\sqrt2}$** empieza en 0.42, porque explora, y llega a
  0.94. Empieza abajo porque las primeras vueltas se reparten entre las
  tres, y el acumulado arrastra ese costo. Sigue subiendo: su bono se
  encoge donde ya hay evidencia.
- **UCB con ${c=1}$**, el de la página anterior, llega a 0.99: aquí llega
  antes, porque explora menos. Con ${c=0}$ no hay bono y es el mejor
  promedio, 0.85.

Lo que la teoría acota, con ${c=2\sqrt2}$, es cuántas vueltas se pierden
en las otras; con ${c=1}$ la prueba de UCB1 no da esa cota, aunque aquí
funcione mejor.

La búsqueda sí llega a la mejor jugada. Pero cuando se acaba el tiempo,
¿cuál se juega?

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

Todo esto pasó en un solo nodo, la raíz. ¿Qué cambia cuando hay árbol
debajo?

## 8 · Pasar del bandido al árbol

**Piensa: en MCTS, ¿las simulaciones que pasan por un nodo siguen siendo
independientes?**

No del todo. MCTS pone un bandido **en cada nodo** del árbol: elige entre
sus hijos con el mismo puntaje. Eso es **UCT**: UCB1 aplicado en cada nodo
del árbol. Pero debajo de cada hijo hay otros bandidos que van aprendiendo.

Así que los resultados de un hijo ya no son independientes: lo que se
elige abajo depende de lo que salió antes. Lo que promedian tampoco es el
$\mu(s')$ de la definición, que supone que los dos juegan al azar, sino
algo que cambia con la búsqueda.

Que cambie no basta para romper Hoeffding. El teorema no pide que todos
los resultados salgan de la misma forma de jugar: si sus promedios
verdaderos difieren, $\mu(s')$ es el promedio de ellos. Lo que lo rompe es
la dependencia. Por eso Hoeffding no se aplica al pie de la letra.

Kocsis y Szepesvári (2006) demostraron aparte que UCT, con una $c$
bastante grande, llega con suficientes vueltas a la jugada que elegiría
minimax, no a la de mayor $\mu(s')$. Esa prueba no la cubrimos.

Lo que te llevas es la intuición: el bono es un margen de error, la cota
optimista se elige porque el optimismo se corrige solo, y $c$ dice cuánta
confianza se pide.

## 9 · Aplicar el bono por tu cuenta

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin
pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-bono title="Aplica el bono en un nodo de MIN"}
Un nodo $s$ donde **mueve MIN** lleva ${N(s)=50}$ vueltas. Sus tres hijos
tienen, con $\bar u$ medido desde MAX:

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
   MIN le importa que $\mu(p)$ sea **más bajo** de lo que parece: la otra
   cola, que @jue-c3-teo-hoeffding acota igual. Su cota optimista, un
   piso, es ${-0.2-0.45=-0.65}$. Antes de simular, la probabilidad de que
   ese piso quede en $\mu(p)$ o por encima es a lo más 5 %.
2. **El puntaje con ${c=2\sqrt2}$.** MIN baja al hijo de cota optimista
   ${\bar u-\text{bono}}$ más baja. Es lo mismo que elegir el mayor
   puntaje ${-\bar u+\text{bono}}$, como en
   [[simular-en-vez-de-evaluar|Simular en vez de evaluar]]. Bonos: p 1.02,
   q 1.44, r 2.50. Puntajes: p ${0.2+1.02=1.22}$, q ${0+1.44=1.44}$, r
   ${-0.4+2.50=2.10}$. Baja por **r**: el peor promedio para MIN, pero
   con solo 5 simulaciones.

   El bono de p, 1.02, es más del doble del margen del inciso 1: con
   ${c=2\sqrt2}$ se pide ${\delta=1/50^4}$, mucho menos que 5 %.
3. **El puntaje con ${c=1}$.** Bonos 0.36, 0.51 y 0.88; puntajes 0.56,
   0.51 y 0.48. Baja por **p**: la $c$ chica casi no explora.
4. **Lo que se entrega.** **p**, la de más simulaciones, 30. Entregar no
   usa el bono.
:::

**Punto de control:** deberías poder despejar el margen de una jugada
dados $\delta$ y $N(s')$, leer la $c$ de un puntaje como un $\delta$, y
calcular la cota optimista en un nodo de MAX o de MIN.

## Lo que hay que llevarse

- **Sin dudar, la regla se atora.** «Siempre el mejor promedio», con una
  semilla, deja 998 de 1 000 vueltas en z, la peor: creyó una derrota de x.
- **Hoeffding mide cuánto falla un promedio** de resultados independientes
  entre ${-1}$ y ${+1}$: a lo más ${e^{-N(s')\varepsilon^2/2}}$. Con la
  jugada y, ${\varepsilon=0.2}$ y ${N(s')=100}$, la cota es 13.5 % y lo
  simulado, 2.4 %.
- **Despejar** da ${\varepsilon=\sqrt{2\ln(1/\delta)/N(s')}}$: el margen
  que solo falla con probabilidad $\delta$.
- **La cota optimista** ${\bar u+\varepsilon}$ es lo más que la jugada
  podría valer sin que los datos lo desmientan; se elige la más alta,
  porque el optimismo se corrige solo. MIN usa ${\bar u-\varepsilon}$ y
  elige la más baja; una jugada sin probar tiene bono infinito.
- **$c$ es $\delta$ disfrazada.** Con ${\delta=N(s)^{-k}}$, ${c=\sqrt{2k}}$.
  UCB1 pide ${\delta=N(s)^{-4}}$, y da ${c=2\sqrt2\approx2.83}$; con la
  tasa ${G/N}$ es ${c=\sqrt2}$, la misma regla. La ${c=1}$ de la página
  anterior es ${k=1/2}$.
- **Converge.** En 40 corridas, la regla sin bono es todo o nada: 34 en
  la mejor y 6 atoradas. A 10 000 vueltas, en la mejor: mejor promedio
  0.85, a veces al azar 0.93, UCB con ${c=2\sqrt2}$ 0.94, con ${c=1}$ 0.99.
- **Seleccionar usa el bono; entregar, no.** En el ejercicio de MCTS, con
  ${c=2\sqrt2}$ la selección va a z (2.12) y con ${c=1}$ a y; se entrega
  x, con 60 simulaciones.
- **En el árbol**, UCT es UCB1 en cada nodo; Hoeffding ya no vale al pie de
  la letra, pero la intuición sí.

Continúa con [[juegos-sin-turnos|la clase 4, cuando no hay turnos]].
