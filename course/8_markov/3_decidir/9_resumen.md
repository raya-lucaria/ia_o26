---
id: mkv-resumen-decidir
title: "Resumen de la clase: el formulario"
nav_title: "Resumen"
summary: "Nada nuevo: las definiciones, los teoremas con su condición, los tres algoritmos y lo que más se confunde, en una sola página."
status: ready
estimated_time: 14m
tags: [markov, decidir, resumen]
---

# Resumen de la clase: el formulario

**¿Qué hay que llevarse de la clase?** Las definiciones, los teoremas con su condición y los tres algoritmos. Aquí no hay nada nuevo. Cada renglón resume algo ya demostrado o calculado en su página. Si un renglón no te queda claro, vuelve a ella.

**Qué V usa esta página.** Las cuatro de la clase, cada una con su marca: $V_\pi$, $V^*$, $V^{(k)}$ y $V$ a secas solo como incógnita. La tabla de abajo las separa.

::: table {#mkv-c3-rs-tabla-cuatro-v title="Las cuatro V"}
| Se escribe | Qué es | Dónde aparece |
|---|---|---|
| $V_\pi(s)$ | Lo que vale $s$ si sigues una política fija $\pi$, buena o mala | Evaluar una política |
| $V^*(s)$ | Lo que vale $s$ con la mejor política: $V^*(s)=\max_\pi V_\pi(s)$ | Bellman y los tres algoritmos |
| $V^{(k)}(s)$ | La aproximación de un algoritmo tras $k$ rondas | Iteración de valores |
| $V(s)$ | Una incógnita: números que buscamos en una ecuación o un PL | Bellman y el programa lineal |
:::

## 1 · La idea en tres viñetas

¿Qué cuenta la clase en breve? Que decidir es elegir filas, y que el máximo es lo único que cambia.

- **Decidir es elegir filas.** En un MDP cada acción trae su propia matriz $P_a$. Una política $\pi$ elige, en cada estado, de qué matriz sale la fila. Así arma una cadena de Markov $P_\pi$, como las de la clase 2.
- **Con la política fija, su valor sale de un sistema lineal.** El valor de esa política, $V_\pi$, sale de condicionar en el primer paso. Es lo mismo que el tiempo medio de llegada de la clase 2. El sistema tiene solución única si la política termina con probabilidad 1.
- **Elegir la acción mete un máximo.** El valor con la mejor política, $V^*$, es el punto fijo de la ecuación de Bellman. Sin ciclos basta una pasada hacia atrás. Con ciclos hay tres caminos: iterar valores, iterar políticas o un programa lineal.

::: figure {#mkv-c3-fig-mapa-decidir title="El mapa de la clase: pregunta, ecuación, algoritmo"}
![Mapa de la clase en tres columnas: pregunta, ecuación y algoritmo. Primer renglón: ¿cuánto falta pagar en la escalera, sin ciclos? lleva a costo(s) = mínimo de pisar s + a más costo(s + a), y a la pasada HACIA-ATRÁS. Segundo renglón: ¿cuánto vale una política fija? lleva a V_π = r_π + P_π,T V_π, y a EVALUAR-POLÍTICA, un sistema lineal. Tercer renglón: ¿cuál es la mejor política? lleva a la ecuación de Bellman con su máximo, y a tres algoritmos: iteración de valores, iteración de políticas y programa lineal. En el pasillo de dos casillas los tres dan V* = (−5, −2) y la política caminar–correr.](../_assets/mkv-c3-mapa-decidir.svg)
:::

---

## 2 · Las definiciones

¿Qué objetos usa la clase? Nueve, uno por definición.

- **Argmax** (@mkv-c3-def-argmax): el conjunto de las acciones que alcanzan el máximo. Con empates tiene más de un elemento.
- **Punto fijo** (@mkv-c3-def-punto-fijo): una $x$ con $x=f(x)$. Iterar $x\leftarrow f(x)$ puede llegar, acercarse o no moverse hacia ningún lado.
- **MDP** (@mkv-c3-def-mdp): $\langle\mathcal S,\mathcal A,P,r\rangle$. Trae las acciones $\mathcal A(s)$ de cada estado y una matriz $P_a$ por acción, con filas que suman 1. También trae la recompensa esperada $r(s,a)$. Aquí $r\le0$: un costo es una recompensa negativa.
- **Política** (@mkv-c3-def-politica): una regla $\pi(s)\in\mathcal A(s)$ que elige **una sola** acción por estado, siempre la misma. Hay $\prod_{s\in\mathcal T}\lvert\mathcal A(s)\rvert$ políticas.
- **Cadena de la política** (@mkv-c3-def-cadena-politica): $P_\pi$ toma la fila $s$ de $P_{\pi(s)}$. Su bloque entre no terminales es $P_{\pi,\mathcal T}$, y $r_\pi(s)=r(s,\pi(s))$.
- **Valor de una política** (@mkv-c3-def-valor): $V_\pi(s)=E^\pi_s[G_0]$, el retorno esperado desde $s$ si sigues la política fija $\pi$. El retorno $G_t$ suma las recompensas hasta llegar a $\mathcal F$.
- **Terminar con probabilidad 1** (@mkv-c3-def-termina): desde todo estado de $\mathcal T$, la cadena $P_\pi$ llega a $\mathcal F$ con probabilidad 1.
- **Valor de acción** (@mkv-c3-def-q): $Q_\pi(s,a)$ es el valor de tomar $a$ primero y seguir $\pi$ después.
- **Óptimos** (@mkv-c3-def-optimo): $V^*(s)=\max_\pi V_\pi(s)$, el mayor valor que alcanza alguna política desde $s$. $Q^*$ es su valor de acción.

En el pasillo mojado hay cuatro políticas. La tabla da el valor $V_\pi$ de cada una. La óptima es caminar–correr: caminar junto al hueco, correr junto al barandal. Su fila, $(-5,-2)$, es también $V^*$.

::: table {#mkv-c3-rs-tabla-politicas title="Las cuatro políticas del pasillo"}
| Política | $V_\pi(1)$ | $V_\pi(2)$ |
|---|---:|---:|
| caminar–caminar | −6 | −3 |
| caminar–correr | **−5** | **−2** |
| correr–caminar | −15 | −3 |
| correr–correr | −14 | −2 |
:::

---

## 3 · Los teoremas, con su condición

¿Qué garantiza cada resultado, y cuándo? Cada renglón es un teorema de su página: @mkv-c3-teo-hacia-atras, @mkv-c3-teo-evaluar, @mkv-c3-teo-bellman, @mkv-c3-teo-codiciosa, @mkv-c3-teo-iterar-valores, @mkv-c3-teo-iterar-politicas y @mkv-c3-teo-lineal, en ese orden.

::: table {#mkv-c3-rs-tabla-teoremas title="Los siete teoremas y su condición"}
| Teorema | Condición | Qué dice |
|---|---|---|
| Pasada hacia atrás | Grafo finito y sin ciclos | Una sola pasada, de la meta al inicio, da el costo exacto de cada escalón |
| Evaluar una política | $\pi$ termina con probabilidad 1 desde todo $s\in\mathcal T$; equivale a que $I-P_{\pi,\mathcal T}$ sea invertible | $V_\pi=r_\pi+P_{\pi,\mathcal T}V_\pi$ tiene solución única |
| Bellman | Finito; terminal con valor 0; existe una política que termina; toda política que no termina vale $-\infty$ en algún estado | Buscamos números $V(s)$ con $V(s)=\max_a[r(s,a)+\sum_{s'}P(s'\mid s,a)V(s')]$ en $\mathcal T$ y $V(s)=0$ en $\mathcal F$. La única solución es $V^*$ |
| La codiciosa del óptimo | Las de Bellman | Elegir en cada estado una acción del argmax con $V^*$ da una política óptima |
| Iteración de valores | Las de Bellman | $V^{(k)}\to V^*$; desde $V^{(0)}=0$ y con $r\le0$, baja monótona |
| Iteración de políticas | Las de Bellman; empezar con una política que termina; conservar la acción en los empates | Ninguna ronda empeora $V_\pi$; se detiene en rondas finitas en una política óptima |
| Programa lineal | Las de Bellman | Las incógnitas son $V(s)$. El mínimo de $\sum_sV(s)$ sujeto a $V(s)\ge r(s,a)+\sum_{s'}P(s'\mid s,a)V(s')$ para toda $(s,a)$ es $V^*$ |
:::

- **Sin descuento, la condición es terminar.** Aquí $\gamma=1$. Basta que una política termine. Y toda política que no termina debe valer $-\infty$ en algún estado. El recuadro de [[mkv-bellman|la ecuación de Bellman]] cuenta qué cambia con $\gamma<1$.

---

## 4 · Los tres algoritmos

¿Cuál de los tres caminos usar? Los tres buscan $V^*$ resolviendo Bellman. Difieren en qué garantizan y cuánto cuestan.

::: table {#mkv-c3-rs-tabla-algoritmos title="Los tres caminos para resolver Bellman"}
| Algoritmo | Qué calcula | Qué garantiza | Cuánto cuesta |
|---|---|---|---|
| Iteración de valores | La aproximación $V^{(k)}$: lo mejor con $k$ pasos restantes. Al final, su codiciosa | Se acerca a $V^*$, pero en el pasillo no llega en rondas finitas. Para con el residuo y la cota | Una ronda recorre cada $(s,a)$ y sus llegadas; en el pasillo de 200, 451 rondas hasta tol $10^{-9}$ |
| Iteración de políticas | Evalúa $V_\pi$ con un sistema lineal y mejora con la codiciosa | Llega a una política óptima en rondas finitas, a lo más $\prod_s\lvert\mathcal A(s)\rvert$; suele bastar con pocas | Un sistema lineal por ronda; en el pasillo de 200, 2 rondas desde caminar siempre |
| Programa lineal | $V^*$ como el mínimo de un PL | Exacto bajo las condiciones de Bellman | Una variable por estado y una desigualdad por par $(s,a)$; lo resuelve `linprog` |
:::

- **Cuál usar.**
  - Iterar valores es lo más simple, y cada ronda es barata. Pero solo se acerca a $V^*$.
  - Iterar políticas paga un sistema lineal por ronda. A cambio, termina.
  - El programa lineal entrega todo el problema a otro programa, de una vez.
- **Contar las políticas no es opción.** El pasillo de 200 casillas tiene $2^{200}\approx1.6\times10^{60}$ políticas. Los tres algoritmos lo resuelven sin recorrerlas.

---

## 5 · Lo que más se confunde

¿Dónde se equivoca uno más? En nueve lugares, uno por viñeta.

> [!WARNING]
> - **Lo que rompe la pasada hacia atrás es el ciclo, no el azar.** Si un brinco puede dejarte donde estabas, el costo de ese escalón depende de sí mismo.
> - **La codiciosa de un paso no es la codiciosa de $V^*$.** En la escalera, pisar el siguiente más barato cuesta 5. La óptima cuesta 4. Y la codiciosa de un $U$ equivocado, $U=(-8,-8)$, da caminar–caminar, que no es óptima.
> - **Una solución de Bellman no siempre es $V^*$.** Con esperar gratis, esperar siempre no termina y vale 0, no $-\infty$. Entonces la incógnita $V$ de Bellman tiene infinitas soluciones, como $(0,0)$, $(-5,-2)$ y $(-1,-1)$. Solo una es $V^*$: $V^*=(0,0)$.
> - **El programa lineal también se engaña ahí.** Con esperar gratis su región no cambia. Su mínimo sigue en $(-5,-2)$, el $V_\pi$ de caminar–correr, que ya no es $V^*$. Con esperar a costo 1, esperar siempre vale $-\infty$ y todo vuelve a funcionar.
> - **El PL minimiza; no maximiza.** La región no tiene techo: maximizar no tiene sentido.
> - **Un residuo chico no garantiza un error chico.** El error es la distancia de $V^{(k)}$ a $V^*$. Con un lazo de 99/100 y costo 1, el error es 99 veces el residuo. Lo que garantiza es la cota $\tfrac{m}{1-\beta}\operatorname{res}^{(k)}$. En el pasillo, $m=3$ y $\beta=1/2$ dan 6 veces el residuo.
> - **Ronda no es turno.** La ronda $k$ es una pasada del algoritmo sobre todos los estados. $V^{(k)}$ es lo mejor con $k$ pasos restantes. El turno del robot sigue siendo $t$.
> - **Cambiar en un empate puede no terminar.** Con caminar a costo 2 en la casilla 2, las dos acciones empatan. Si la mejora cambia en el empate, alterna para siempre.
> - **La política elige una acción, no una mezcla.** Aquí $\pi(s)$ es una sola acción. En agentes se escribió $\pi(a\mid s)$.

---

## 6 · Autoevaluación

¿Lo puedes hacer sin mirar? Cinco preguntas, una por idea. Contesta antes de abrir la respuesta.

::: exercise {#mkv-c3-rs-ej-evaluar title="Evalúa correr–correr con castigo 4"}
En el pasillo, caer al hueco cuesta 4 en lugar de 10. Así, $r(1,\text{correr})=-3$. La política es correr en las dos casillas. Escribe sus dos ecuaciones y resuélvelas. Las incógnitas $V(1)$ y $V(2)$ serán su valor $V_\pi$.
:::
::: hint {#mkv-c3-rs-pista-evaluar of="mkv-c3-rs-ej-evaluar" title="¿Por cuál casilla conviene empezar?"}
Una de las dos ecuaciones solo tiene una incógnita.
:::
::: answer {#mkv-c3-rs-resp-evaluar of="mkv-c3-rs-ej-evaluar"}
En la casilla 2, $V(2)=-1+\tfrac12V(2)$, así que $V(2)=-2$. En la casilla 1, $V(1)=-3+\tfrac12V(1)+\tfrac12V(2)$, así que $\tfrac12V(1)=-4$ y $V(1)=-8$. El valor de correr–correr es $V_\pi=(-8,-2)$.
:::

::: exercise {#mkv-c3-rs-ej-iterar title="Dos rondas de iteración de valores"}
En el pasillo, empieza con $V^{(0)}=(0,0)$ y haz dos rondas síncronas. ¿Cuánto vale el residuo en la ronda 2?
:::
::: hint {#mkv-c3-rs-pista-iterar of="mkv-c3-rs-ej-iterar" title="¿Qué valores usa cada ronda?"}
Cada ronda usa solo los valores de la ronda anterior, en las dos casillas.
:::
::: answer {#mkv-c3-rs-resp-iterar of="mkv-c3-rs-ej-iterar"}
Ronda 1: $V^{(1)}(1)=\max(-3+0,\,-6+0)=-3$ y $V^{(1)}(2)=\max(-3,\,-1+0)=-1$.

Ronda 2: $V^{(2)}(1)=\max(-3-1,\,-6-\tfrac32-\tfrac12)=-4$ y $V^{(2)}(2)=\max(-3,\,-1-\tfrac12)=-\tfrac32$.

El residuo es $\max(1,\tfrac12)=1$.
:::

::: exercise {#mkv-c3-rs-ej-politicas title="Una ronda de iteración de políticas"}
Empieza con caminar–caminar, que vale $V_\pi=(-6,-3)$. Haz la mejora codiciosa con ese valor. ¿Qué política sale?
:::
::: hint {#mkv-c3-rs-pista-politicas of="mkv-c3-rs-ej-politicas" title="¿Qué se compara en cada casilla?"}
En cada casilla, compara el valor de caminar contra el de correr, usando $(-6,-3)$ para lo que sigue.
:::
::: answer {#mkv-c3-rs-resp-politicas of="mkv-c3-rs-ej-politicas"}
En 1: caminar da $-3-3=-6$ y correr da $-6-3-\tfrac32=-10.5$, así que caminar. En 2: caminar da $-3$ y correr da $-1-\tfrac32=-2.5$, así que correr. Sale caminar–correr, que vale $V_\pi=(-5,-2)$. Una ronda más no la cambia: es la óptima, y ese valor es $V^*$.
:::

::: exercise {#mkv-c3-rs-ej-esperar title="Esperar gratis"}
Agrega en las dos casillas la acción esperar, que te deja donde estás y cuesta 0. ¿Qué condición de Bellman falla? ¿Por qué $(-4,-2)$ resuelve la ecuación, con $V(1)=-4$ y $V(2)=-2$ como incógnitas?
:::
::: hint {#mkv-c3-rs-pista-esperar of="mkv-c3-rs-ej-esperar" title="¿Cuánto vale esperar siempre?"}
Piensa en cuánto suma una política que nunca llega a la meta y nunca paga.
:::
::: answer {#mkv-c3-rs-resp-esperar of="mkv-c3-rs-ej-esperar"}
Esperar siempre no termina y vale 0, no $-\infty$. Falla «toda política que no termina vale $-\infty$ en algún estado». Con $(-4,-2)$, en 2 queda $\max(-3,\,-1-1,\,-2)=-2$, y en 1 queda $\max(-3-2,\,-6-2-1,\,-4)=-4$. Se cumple, igual que con $(0,0)$ y con $(-5,-2)$. Ninguna de esas soluciones es $V^*$ salvo $(0,0)$.
:::

::: exercise {#mkv-c3-rs-ej-lineal title="El PL con castigo 4"}
Con castigo 4, $r(1,\text{correr})=-3$. Escribe las cuatro desigualdades del programa lineal del pasillo y halla su mínimo. ¿Cuáles quedan apretadas, y qué política dicen?
:::
::: hint {#mkv-c3-rs-pista-lineal of="mkv-c3-rs-ej-lineal" title="¿Qué acota cada desigualdad?"}
Las incógnitas son $V(1)$ y $V(2)$. Despeja cada desigualdad: es una cota inferior de $V(1)$ o de $V(2)$. Empieza por las de la casilla 2.
:::
::: answer {#mkv-c3-rs-resp-lineal of="mkv-c3-rs-ej-lineal"}
Son $V(1)\ge-3+V(2)$, $V(1)\ge-3+\tfrac12V(1)+\tfrac12V(2)$, $V(2)\ge-3$ y $V(2)\ge-1+\tfrac12V(2)$. Despejadas: $V(1)\ge V(2)-3$, $V(1)\ge V(2)-6$, $V(2)\ge-3$ y $V(2)\ge-2$. El mínimo es $V(2)=-2$ y $V(1)=-5$, con suma $-7$. Quedan apretadas caminar en 1 y correr en 2. La política es caminar–correr, y $(-5,-2)$ es su $V_\pi$, que es también $V^*$.
:::

Vuelve al [[markov-decidir|índice de la clase 3]].
