---
id: mkv-max-y-punto-fijo
title: "Lo que necesitas: el máximo y el punto fijo"
nav_title: "Lo que necesitas"
summary: "El máximo y el argmax con empates, condicionar en el primer paso y el punto fijo de una función: cuándo iterar llega, se acerca o no."
status: ready
estimated_time: 18m
tags: [markov, decidir, punto-fijo, argmax]
---

# Lo que necesitas: el máximo y el punto fijo

**¿Qué herramientas faltan para pasar de promediar lo que hace una cadena a elegir lo que conviene?**

> [!NOTE]
> **Por qué estudiamos esto.** En las clases 1 y 2 la cadena se movía sola: tú solo calculabas promedios. En esta clase, en cada estado **eliges** qué hacer, y cada elección cambia a dónde puedes ir después.
>
> - Un robot elige caminar o correr; correr es rápido, pero puede resbalar.
> - Un jugador elige cuánto apostar; la apuesta cambia su capital y sus opciones siguientes.
>
> **Lo difícil:** lo que vale una elección depende de lo que elijas después, y eso a su vez depende de esta. Tres herramientas bastan para escribirlo: quedarse con la mejor opción, partir la cuenta en el primer paso y resolver una ecuación cuya incógnita aparece de los dos lados. **Esta página las reúne, con funciones sueltas.**

Al terminar tendrás:

- **El máximo y el argmax:** el número más alto y el conjunto de opciones que lo alcanzan, con empates.
- **El primer paso, otra vez:** lo que falta se escribe como un paso más lo que falta desde donde caes.
- **El punto fijo:** un número que la función deja quieto, y por qué aparece al partir en el primer paso.
- **Iterar:** aplicar la función una y otra vez llega, se acerca sin llegar o no sirve, según la pendiente.

## Lo que traes

De la clase 2, [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]] y [[mkv-absorcion|Cuánto falta para terminar]]:

- **Valor esperado:** $E_s[X]$ promedia $X$ empezando en $s$ (@mkv-c2-def-esperanza).
- **Condicionar en el primer paso:** $E[X]=\sum_s\Pr(S_1=s)\,E[X\mid S_1=s]$ (@mkv-c2-teo-primer-paso).
- **Tiempo medio de llegada:** $m(s)=1+\sum_{s'\in\mathcal T}P_{ss'}m(s')$, si desde todo $s\in\mathcal T$ se llega con probabilidad 1 (@mkv-c2-teo-absorcion).
- **Límite y tolerancia:** una sucesión se acerca a $x$ si la distancia queda bajo toda $\mathrm{tol}$ (@mkv-c2-def-limite).

De la unidad de juegos, [[diagnosticar-el-juego|Diagnosticar el juego]] y [[cuando-decide-un-dado|Cuando decide un dado]]:

- **Número y jugada:** el valor es un $\max$; la jugada, un elemento del $\operatorname{arg\,max}$ (@jue-c1-valor-jugada-estrategia).
- **Azar:** en un nodo de azar se promedia, en uno de MAX se toma el máximo (@jue-c2-valor-esperado).

---

## 1 · Elegir con el máximo y el argmax

**Piensa: si cada opción trae un número, ¿con qué número te quedas, y con qué opción?**

Con el más alto, y con **todas** las opciones que lo alcanzan: pueden ser varias.

::: definition {#mkv-c3-def-argmax title="Máximo y argmax de un conjunto finito"}
$$
\begin{aligned}
&\mathcal A(s)\ \text{finito y no vacío},\qquad
f:\mathcal A(s)\to\mathbb R,\\
&\max_{a\in\mathcal A(s)}f(a)
=\text{el mayor de los números }f(a),\\
&\operatorname*{arg\,max}_{a\in\mathcal A(s)}f(a)
=\Bigl\{a\in\mathcal A(s):\ f(a)=\max_{a'\in\mathcal A(s)}f(a')\Bigr\}.
\end{aligned}
$$

- **Qué es:** el máximo es **un número**; el argmax es **un conjunto** de opciones, las que empatan en ese número.
- **Cómo se calcula:** se recorre $\mathcal A(s)$ una vez, guardando el mayor valor visto y las opciones que lo alcanzan.
- **Qué significa:** elegir bien es tomar cualquier $a$ del argmax; con empates, todas valen lo mismo.
- **Qué no es:** «la» mejor opción, porque puede haber varias; y con un conjunto infinito, como $-1/a$ en los enteros positivos, el máximo puede no existir.
:::

- **Notación.** $\mathcal A(s)$ son las opciones disponibles en $s$; en esta clase serán acciones. Va en caligráfica porque $A$ ya es el conjunto de llegada de la clase 2; juegos escribió $A(s)$ para las jugadas.
- **Costos.** Si cada opción trae un costo, se busca el menor. Es lo mismo con signo cambiado: $\min_a\text{costo}(a)=-\max_a\bigl(-\text{costo}(a)\bigr)$, con el mismo conjunto de opciones elegidas.

**En el juguete.** Tres opciones, izquierda, centro y derecha, con valores $-3$, $-1$ y $-1$:

$$
\max=-1,\qquad
\operatorname*{arg\,max}=\{\text{centro},\ \text{derecha}\}.
$$

- **Desempate:** las dos valen $-1$; si hace falta una sola, se fija una regla de antemano, como «la primera de la lista».

> [!WARNING]
> **Error típico: escribir $\max$ donde va $\operatorname{arg\,max}$.** El máximo responde «cuánto obtengo»; el argmax, «qué hago». **La lectura correcta: el valor de un estado es un número; la decisión es una opción del argmax.**

::: exercise {#mkv-c3-mx-ej-empate title="Separa el número de la opción"}
Cuatro opciones traen costos 2, 5, 2 y 7. ¿Cuál es el menor costo y qué opciones lo alcanzan? ¿Cuánto valen $\max$ y $\operatorname{arg\,max}$ de los costos con signo cambiado?
:::

::: hint {#mkv-c3-mx-pista-empate of="mkv-c3-mx-ej-empate" title="¿Cuántas opciones empatan?"}
¿Cuántas veces aparece el costo más chico en la lista?
:::

::: answer {#mkv-c3-mx-resp-empate of="mkv-c3-mx-ej-empate"}
**El menor costo es 2,** y lo alcanzan la primera y la tercera. Con signo cambiado los valores son $-2,-5,-2,-7$: el máximo es $-2$ y el argmax es el mismo conjunto, $\{\text{primera},\ \text{tercera}\}$.
:::

El máximo decide un paso. Para decidir el siguiente hay que saber cuánto vale lo que viene después.

---

## 2 · Partir la cuenta en el primer paso

**Piensa: si un estado puede devolverte a sí mismo, ¿cómo escribes lo que vas a pagar desde ahí?**

Un paso más lo que falte desde donde caigas; y si caes en el mismo estado, lo que falta es **la misma incógnita**.

Es @mkv-c2-teo-primer-paso con un pago en cada paso. Si $X$ es lo que se recibe hasta terminar y el primer paso desde $s$ da un pago fijo, entonces, para cada $s'$ con $P_{ss'}>0$,

$$
\begin{aligned}
E_s[X\mid S_1=s']
&=(\text{pago del primer paso})+E_{s'}[X],\\
E_s[X]
&=(\text{pago del primer paso})\\
&\qquad+\sum_{s'\in\mathcal T}P_{ss'}\,E_{s'}[X],
\end{aligned}
$$

con $E_{s'}[X]=0$ en los estados donde ya se terminó.

- **Markov:** dado $S_1=s'$, lo que sigue es la cadena empezando en $s'$ (@mkv-c1-cadena).
- **Con pago 1:** es el tiempo medio de llegada, $m(s)=1+\sum_{s'}P_{ss'}m(s')$ (@mkv-c2-teo-absorcion).
- **La condición:** la de ese teorema, terminar con probabilidad 1 desde todo estado; sin ella el promedio puede no ser finito.
- **Signo:** en esta clase un costo se cuenta como pago negativo. Pagar 1 por paso es recibir $-1$.

**En el juguete.** Un estado $s$: en cada paso pagas 1; con probabilidad $1/2$ terminas y con $1/2$ te quedas en $s$. Sea $x=E_s[X]$:

$$
\begin{aligned}
x&=\tfrac12(-1)+\tfrac12(-1+x)=-1+\tfrac12x,\\
x&=-2.
\end{aligned}
$$

- **Comprobación:** es una racha con probabilidad de seguir $1/2$; dura $1/(1-\tfrac12)=2$ pasos en promedio y pagas 2.
- **Lo nuevo:** $x$ aparece de los dos lados. Aquí se despeja; con un máximo adentro, no.

::: exercise {#mkv-c3-mx-ej-dos-pagos title="Plantea con dos pagos"}
Cambia el juguete: el paso cuesta 1 si terminas y 3 si te quedas, cada caso con probabilidad $1/2$. Escribe la ecuación de $x$ y resuélvela.
:::

::: hint {#mkv-c3-mx-pista-dos-pagos of="mkv-c3-mx-ej-dos-pagos" title="¿Qué pagas en cada caso del primer paso?"}
¿Cuánto recibes en el primer paso si terminas, y cuánto más lo que falta si te quedas?
:::

::: answer {#mkv-c3-mx-resp-dos-pagos of="mkv-c3-mx-ej-dos-pagos"}
$$
\begin{aligned}
x&=\tfrac12(-1)+\tfrac12(-3+x)=-2+\tfrac12x,\\
x&=-4.
\end{aligned}
$$

**El pago del primer paso es su promedio,** $-2$; el resto es igual que antes.
:::

Una ecuación de la forma $x=f(x)$ tiene nombre propio, y una manera de resolverla que no necesita despejar.

---

## 3 · Buscar un punto fijo iterando

**Piensa: ¿qué número no cambia al aplicarle $f$?**

Un **punto fijo** de $f$: la $x$ que cumple $x=f(x)$. En la gráfica, donde $y=f(x)$ cruza la diagonal $y=x$.

::: definition {#mkv-c3-def-punto-fijo title="Punto fijo e iteración"}
$$
\begin{aligned}
&f:\mathbb R\to\mathbb R,\qquad
x^*\ \text{es punto fijo}\iff f(x^*)=x^*,\\
&\text{iterar:}\quad x^{(t+1)}=f\bigl(x^{(t)}\bigr),
\qquad x^{(0)}\ \text{dado}.
\end{aligned}
$$

- **Qué es:** un número que $f$ deja quieto. Puede no haber ninguno, haber uno o haber muchos.
- **Cómo se calcula:** despejando, cuando se puede; si no, iterando desde algún $x^{(0)}$ y viendo si $x^{(t)}$ se acerca a algo.
- **Qué significa:** si la iteración tiene límite y $f$ es continua, ese límite es un punto fijo.
- **Qué no es:** iterar no garantiza nada por sí solo: la sucesión puede no acercarse, o acercarse a un punto fijo que no es el que buscas.
:::

- **Rondas.** $x^{(t)}$ es el valor tras $t$ **rondas**, aplicaciones de $f$. Una ronda no es un paso de la cadena.
- **En inglés:** *fixed point*.

::: theorem {#mkv-c3-mx-teo-pendiente title="Iterar una recta: llega, se acerca o no"}
Sea $f(x)=f(0)+q\,x$, con pendiente $q\in[0,1]$.

- **Si $q<1$:** hay un solo punto fijo, $x^*=f(0)/(1-q)$, y desde cualquier $x^{(0)}$
  $$
  x^{(t)}-x^*=q^t\bigl(x^{(0)}-x^*\bigr).
  $$
  Con $q=0$ llega en una ronda; con $0<q<1$ se acerca sin llegar, y el error se multiplica por $q$ en cada ronda.
- **Si $q=1$ y $f(0)\ne0$:** no hay punto fijo; cada ronda suma $f(0)$ y la sucesión se va a $\pm\infty$.
- **Si $q=1$ y $f(0)=0$:** todo número es punto fijo; la iteración se queda donde empezó.

**Condición.** $f$ es una recta con pendiente entre 0 y 1; en los juguetes, $q$ es la probabilidad de seguir, como en las rachas.

**Lectura.** La pendiente es lo que el ciclo devuelve a la incógnita. Sin ciclo, $q=0$ y una ronda basta.

**Casos nulos.** Si $x^{(0)}=x^*$, la iteración no se mueve.
:::

::: proof {#mkv-c3-mx-dem-pendiente of="mkv-c3-mx-teo-pendiente"}
Con $q<1$, $x^*=f(0)+q\,x^*$ se despeja. Resta esa igualdad a $x^{(t+1)}=f(0)+q\,x^{(t)}$:

$$
x^{(t+1)}-x^*=q\,\bigl(x^{(t)}-x^*\bigr).
$$

Aplicada $t$ veces da la fórmula. Con $q=1$, $x=f(0)+x$ exige $f(0)=0$, y entonces vale para toda $x$.
:::

**En el juguete.** La ecuación de la sección 2 es $x=f(x)$ con $f(x)=-1+x/2$: $q=1/2$ y $x^*=-2$. Desde $x^{(0)}=0$:

$$
x^{(t)}=-2+2^{1-t}:\quad
0,\ -1,\ -\tfrac32,\ -\tfrac74,\ -\tfrac{15}8,\ \dots
$$

- **El error** vale $2^{1-t}$: se parte a la mitad en cada ronda y nunca llega a cero.
- **Lectura:** $x^{(t)}$ es lo que pagas en promedio si te obligan a parar tras $t$ pasos. Con $t=2$: pagas 1 seguro, y 1 más con probabilidad $1/2$.
- **Cuándo parar:** nunca llega; hace falta una tolerancia (@mkv-c2-def-limite).

::: figure {#mkv-c3-fig-punto-fijo title="Iterar f(x) = −1 + x/2 desde 0: una telaraña que se cierra en −2"}
![Gráfica con la recta y = −1 + x/2 y la diagonal y = x, que se cruzan en x = −2. Desde x = 0, una telaraña de segmentos verticales y horizontales rebota entre la recta y la diagonal y visita 0, −1, −3/2, −7/4 y −15/8, cada vez más cerca de −2 sin llegar; la distancia a −2 se parte a la mitad en cada ronda](../_assets/mkv-c3-punto-fijo.svg)
:::

> [!TIP]
> **Ejemplo y contraejemplo.**
>
> - **Lo cumple:** $f(x)=-1+x/2$ cruza $y=x$ una sola vez, en $-2$, e iterar se acerca a ese cruce desde cualquier inicio.
> - **No lo cumple:** $f(x)=x$ coincide con la diagonal; todo número es punto fijo y la ecuación no dice cuál es la respuesta.

::: figure {#mkv-c3-fig-ej-punto-fijo title="Un cruce o una recta encimada en la diagonal"}
![Dos paneles. Arriba, marcado como cumple: la recta y = −1 + x/2 y la diagonal y = x se cruzan en un solo punto, x = −2, y la iteración desde 0 se acerca a él. Abajo, marcado como no cumple: la recta y = x queda encimada en la diagonal; todo punto es fijo y la iteración se queda donde empieza. Pie: sin un solo cruce, la ecuación x = f(x) no determina la respuesta](../_assets/mkv-c3-ej-punto-fijo.svg)
:::

> [!WARNING]
> **Error típico: tomar la primera solución que sale.** Con $f(x)=x$, iterar desde 0 se queda en 0 con cambio cero, y eso parece una respuesta. **La lectura correcta: si la ecuación tiene muchas soluciones, falta una condición que diga cuál es la buena.**

**Con Python.** La misma iteración para cuatro rectas, con fracciones exactas:

```python
from fractions import Fraction as F

def iterar(f, x, rondas):
    """Devuelve x(0), x(1), ..., x(rondas)."""
    traza = [x]
    for _ in range(rondas):
        x = f(x)              # una ronda: x <- f(x)
        traza.append(x)
    return traza

funciones = {
    "-3       ": lambda x: F(-3),
    "-1 + x/2 ": lambda x: -1 + x / 2,
    "x - 1    ": lambda x: x - 1,
    "x        ": lambda x: x,
}
for nombre, f in funciones.items():
    traza = iterar(f, F(0), 5)
    print(nombre, [str(v) for v in traza])
```

```text
-3        ['0', '-3', '-3', '-3', '-3', '-3']
-1 + x/2  ['0', '-1', '-3/2', '-7/4', '-15/8', '-31/16']
x - 1     ['0', '-1', '-2', '-3', '-4', '-5']
x         ['0', '0', '0', '0', '0', '0']
```

- **Los cuatro casos del teorema:** llega ($-3$), se acerca ($-1+x/2$), baja sin fin ($x-1$) y se queda donde empezó ($x$).

::: exercise {#mkv-c3-mx-ej-cuantas-rondas title="Cuenta las rondas"}
Con $f(x)=-1+x/2$ desde 0, ¿tras cuántas rondas el error queda por primera vez en $1/100$ o menos?
:::

::: hint {#mkv-c3-mx-pista-cuantas-rondas of="mkv-c3-mx-ej-cuantas-rondas" title="¿Cuánto vale el error en la ronda t?"}
¿Qué potencia de 2 es la primera en pasar de 100?
:::

::: answer {#mkv-c3-mx-resp-cuantas-rondas of="mkv-c3-mx-ej-cuantas-rondas"}
**Ocho rondas.** El error es $2^{1-t}$ y pide $2^{t-1}\ge100$; $2^6=64$ no basta y $2^7=128$ sí, así que $t-1=7$.
:::

Con las tres herramientas puedes escribir y resolver una ecuación con una sola opción por estado. Antes de juntarlas con el máximo, practícalas.

---

## Ejercicios

::: exercise {#mkv-c3-mx-ej-un-cuarto title="Resuelve un ciclo más lento"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Un estado $s$: en cada paso pagas 1; con probabilidad $1/4$ terminas y con $3/4$ te quedas en $s$.

**Cambia una idea:** terminar es menos probable que en el juguete, $1/4$ en lugar de $1/2$, así que el ciclo devuelve más a la incógnita.

1. **Plantea** $x=f(x)$ para $x=E_s[X]$, condicionando en el primer paso.
2. **Resuelve** el punto fijo y compruébalo con la fórmula de las rachas.
3. **Itera** desde $x^{(0)}=0$ tres rondas y escribe el error en la ronda $t$.
4. **Rompe la condición:** si nunca terminas, ¿qué pasa con $f$, con el punto fijo y con la iteración?
:::

::: hint {#mkv-c3-mx-pista-un-cuarto-1 of="mkv-c3-mx-ej-un-cuarto" title="Pista 1 · ¿Qué pasa en cada caso del primer paso?"}
¿Cuánto recibes si terminas en ese paso, y cuánto si te quedas, contando lo que falta? ¿Cuál es la pendiente $q$ de tu $f$?
:::

::: hint {#mkv-c3-mx-pista-un-cuarto-2 of="mkv-c3-mx-ej-un-cuarto" title="Pista 2 · ¿Cómo compruebas tu punto fijo?"}
¿Tu $x^*$ cumple $f(x^*)=x^*$ al sustituirlo? ¿Coincide con menos la duración media de una racha con probabilidad de seguir $3/4$?
:::

::: answer {#mkv-c3-mx-resp-un-cuarto of="mkv-c3-mx-ej-un-cuarto" title="Respuesta · Un punto fijo que solo se alcanza en el límite"}
**1. Plantea.**

$$
x=\tfrac14(-1)+\tfrac34(-1+x)=-1+\tfrac34x,
\qquad f(x)=-1+\tfrac34x.
$$

**2. Resuelve.** Con $q=3/4$, $x^*=-1/(1-\tfrac34)=-4$. Comprueba: $f(-4)=-1-3=-4$. La racha dura $1/(1-\tfrac34)=4$ pasos en promedio y pagas 4.

**3. Itera.**

$$
\begin{aligned}
x^{(t)}&=-4+4\bigl(\tfrac34\bigr)^t:\quad
0,\ -1,\ -\tfrac74,\ -\tfrac{37}{16},\\
\text{error}&=4\bigl(\tfrac34\bigr)^t.
\end{aligned}
$$

Tras tres rondas el error es $27/16\approx1.69$. Se encoge más despacio que con $q=1/2$: llegar a $1/100$ toma 21 rondas, no 8.

**4. Rompe la condición.** Sin terminar nunca, $f(x)=-1+x$: pendiente 1 y $f(0)\ne0$. No hay punto fijo, y la iteración da $0,-1,-2,\dots$ sin fin. Coincide con lo que pasa: pagas 1 en cada paso, para siempre.
:::

---

**Punto de control:** deberías poder dar el máximo y el argmax de una lista con empates, y pasar de costos a valores con el signo. También, plantear lo que falta condicionando en el primer paso y reconocer la ecuación $x=f(x)$. Y decir, por la pendiente, si iterar llega, se acerca o no sirve.

---

## Lo que hay que llevarse

- **Máximo y argmax:** el máximo es un número; el argmax, el conjunto de opciones que lo alcanzan. Con valores $-3,-1,-1$: máximo $-1$, dos opciones en el argmax.
- **Costos:** $\min_a\text{costo}(a)=-\max_a\bigl(-\text{costo}(a)\bigr)$; un costo es un pago negativo.
- **Primer paso:** lo que falta es el pago del primer paso más el promedio de lo que falta desde donde caes. Pagar 1 y terminar con $1/2$ da $x=-1+x/2$, así que $x=-2$.
- **Punto fijo:** $x^*=f(x^*)$; iterar es $x^{(t+1)}=f(x^{(t)})$.
- **Recta con pendiente $q$:** con $q<1$, un solo punto fijo y error multiplicado por $q$ cada ronda; $f(x)=-1+x/2$ da $0,-1,-\tfrac32,-\tfrac74,\dots\to-2$. Con $q=1$, ninguno ($x-1$) o todos ($x$).

Continúa con [[mkv-la-escalera|De contar a decidir: la escalera]]: ¿cómo se usa el máximo cuando hay que decidir muchas veces seguidas?
