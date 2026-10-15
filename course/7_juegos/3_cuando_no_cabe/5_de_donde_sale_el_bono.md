---
id: de-donde-sale-el-bono
title: De dónde sale el bono
nav_title: De dónde sale el bono
summary: "El bono de UCT se usa primero por fe: premia lo poco probado y hace volver a lo olvidado. Luego se justifica: la desigualdad de Hoeffding da el margen de un promedio con N fijo, y pedir un fallo δ = N(s)⁻⁴ da la constante de UCB1 en el bandido estacionario. MIN usa la otra cola sin cambiar c; en la práctica c se afina; en el árbol, la cuenta es solo intuición."
status: ready
estimated_time: 40m
tags: [juegos, mcts, exploracion]
---

# De dónde sale el bono

**¿Por qué el puntaje de UCT suma justo $c\sqrt{\ln N(s)/N(s,a)}$, y qué $c$ conviene usar?**

Primero lo usarás tal cual y verás qué hace. Después lo sacarás de una desigualdad de probabilidad.

- **Con la regla en la mano**, leerás qué hace cada pieza del bono y por qué vuelve una jugada olvidada.
- **Con Hoeffding**, medirás cuánto puede engañar un promedio y despejarás su margen.
- **Con los límites a la vista**, distinguirás lo que la cuenta demuestra en un bandido de lo que solo sugiere en el árbol.

## Lo que traes

- **El valor se mide desde MAX.** $Q(s,a)=V(T(s,a))$ supone juego óptimo de ambos; $Q_{\text{azar}}(s,a)$ supone que los dos eligen al azar (@jue-c3-simulacion).
- **UCT guarda por arista.** Cada jugada lleva sus visitas $N(s,a)$ y su promedio $\widehat Q(s,a)$; el estado lleva $N(s)$. Lo viste en [[monte-carlo-en-un-arbol-grande|MCTS con UCT]].
- **UCT selecciona con un puntaje.** MAX baja por el mayor $\widehat Q(s,a)+\text{bono}$ y MIN por el menor $\widehat Q(s,a)-\text{bono}$. Al final se juega la jugada con más visitas, sin bono.
- **Los pagos van de $-1$ a $+1$.** $U=+1$ si gana MAX, $-1$ si gana MIN y $0$ si empatan.

> **Supuestos de esta página.** Del bloque 1 al 5 hay **una sola decisión**, repetida: elegir entre unas pocas jugadas cuyas simulaciones son independientes y siguen una regla fija. El bloque 6 vuelve al árbol, donde eso deja de valer.

---

## 1 · UCB por fe

**Piensa: si una jugada lleva pocas visitas y un mal promedio, ¿debe volver a probarse?**

A veces sí: su promedio todavía puede estar muy lejos de lo que vale. El bono le da otra oportunidad, en proporción a cuánto se ignora.

**La regla.** En un nodo $s$ donde mueve MAX, cada jugada $a$ con $N(s,a)>0$ recibe el puntaje

$$
\mathbf{\widehat Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}}
$$

y la selección baja por el mayor. $N(s)$ es el **reloj** del nodo: las vueltas que ya pasaron por él.

- **$\widehat Q(s,a)$ aprovecha (*exploitation*).** Favorece lo que ya pagó bien.
- **$N(s,a)$ abajo encoge el bono.** Una jugada muy probada recibe poco beneficio de la duda.
- **$\ln N(s)$ arriba lo hace crecer.** Si una jugada deja de elegirse, su $N(s,a)$ se congela pero el reloj avanza: su bono sube, despacio, hasta que vuelve a probarse.
- **$c$ pesa la exploración (*exploration*).** Con $c=0$ no hay bono y la regla solo aprovecha. Duplicar $c$ duplica el bono con los mismos datos, pero no necesariamente duplica las exploraciones.
- **Una jugada sin visitas se atiende primero.** La fórmula solo se usa cuando todas tienen $N(s,a)>0$.

**Ejemplo real: el árbol de resultados tras 12 vueltas.** UCT con $c=1$ y semilla 0; en la raíz, $N(s)=12$.

::: table {#jue-c3-tabla-uct-12 title="El árbol de resultados tras 12 vueltas, c = 1"}
| Jugada | $N(s,a)$ | $\widehat Q$ | Bono | Puntaje |
|---|---:|---:|---:|---:|
| izq | 1 | $-1$ | 1.576 | **0.576** |
| centro | 4 | $-0.250$ | 0.788 | 0.538 |
| der | 7 | $-0.143$ | 0.596 | 0.453 |
:::

- **La siguiente vuelta va a izq.** Tiene el peor promedio, pero una sola visita: su bono compensa la diferencia.
- **Si el tiempo se acaba aquí, se juega der.** Es la más visitada; el puntaje solo decide dónde gastar la vuelta.
- **Nadie programó «prueba izq».** La exploración **emerge** de la fórmula: el bono crece donde falta información.

**Sin bono, la regla se atora.** Para verlo, quita el árbol de debajo: queda una decisión repetida, el **bandido**. Cada jugada es una palanca que paga al azar; la pregunta es cuál jalar en la vuelta que sigue.

::: definition {#jue-c3-mu title="La esperanza de una jugada"}
**Qué es.** Si después de $a$ la partida sigue una regla fija, el pago $U$ tiene una esperanza fija. Si esa regla es elegir al azar, es $Q_{\text{azar}}(s,a)$, entre $-1$ y $+1$, desde MAX.

**Cómo se estima.** Con el promedio $\widehat Q(s,a)$ de las $N(s,a)$ simulaciones hechas.

**Qué significa.** Es el blanco del promedio: nadie lo ve, solo se ve $\widehat Q(s,a)$.

**Qué no es.** No es $Q(s,a)$: supone una regla fija para lo que sigue, no juego óptimo.
:::

El bandido de esta página tiene tres jugadas con $U=\pm1$. Sus esperanzas están fijadas para poder comprobar cada regla; la regla no las ve.

| Jugada | $Q_{\text{azar}}$ | $\Pr(U=+1)$ |
|---|---:|---:|
| x | 0.6 | 0.80 |
| y | 0.3 | 0.65 |
| z | $-0.2$ | 0.40 |

La regla más simple prueba cada jugada una vez y luego elige **siempre el mejor promedio**; en empate, la primera en el orden x, y, z. Con la semilla 36, las tres primeras vueltas salen así: x pierde, y pierde, z gana.

::: exercise {#jue-c3-ej-atora title="Encuentra dónde se atora"}
Tras esas tres vueltas, $\widehat Q(\text{x})=-1$, $\widehat Q(\text{y})=-1$ y $\widehat Q(\text{z})=+1$. La regla sigue con «siempre el mejor promedio».

1. **La vuelta 4.** ¿Qué jugada elige?
2. **El regreso.** ¿Puede volver a elegir x alguna vez? ¿Por qué?
:::

::: hint {#jue-c3-pista-atora-1 of="jue-c3-ej-atora" title="El piso"}
¿Cuál es el valor más bajo que puede tener un promedio de $U$? ¿Puede llegar ahí una jugada que ya ganó una vez?
:::

::: answer {#jue-c3-resp-atora of="jue-c3-ej-atora"}
1. **z**, con $\widehat Q=+1$.
2. **Nunca, en esta corrida.** x e y no se vuelven a probar y se quedan en $-1$, el mínimo posible. z ya ganó una vez, así que su promedio nunca baja a $-1$. Tras 1000 vueltas, x e y llevan una simulación cada una y z, 998: la regla se atoró en la peor jugada.
:::

**Los dos errores no cuestan lo mismo.** Mientras una jugada sobreestimada encabeza, sigue recibiendo muestras: su promedio puede subir o bajar y, si recibe muestras sin límite, converge a su esperanza con probabilidad 1. Si deja de elegirse, puede quedar congelada, pero ya no es la elegida. Una jugada subestimada puede no volver a probarse nunca.

::: table {#jue-c3-tabla-optimismo title="Equivocarse por arriba o por abajo"}
| Error | Qué puede pasar |
|---|---|
| Creer buena una mala | Mientras encabece recibe muestras; su $\widehat Q$ puede subir o bajar. Con muestras sin límite converge a su esperanza; si deja de elegirse puede quedar congelada, pero ya no es la elegida |
| Creer mala una buena | Puede dejar de probarse y **conservar para siempre** una subestimación |
:::

**Moraleja: sin bono, la regla cree un promedio hecho con una sola simulación.** El bono le enseña a dudar; falta decir cuánto.

---

## 2 · Hoeffding tal cual

**Piensa: con 100 simulaciones, ¿qué tan seguido queda el promedio 0.2 o más por debajo de su esperanza?**

Con probabilidad a lo más 13.5 %, si se cumplen las condiciones del lema. La cuenta no depende de la jugada.

::: definition {#jue-c3-margen title="El margen y el fallo"}
**Qué es.** El **margen** $\varepsilon>0$ es una distancia en la escala de $U$. El promedio **falla por debajo** si $\widehat Q(s,a)\le Q_{\text{azar}}(s,a)-\varepsilon$.

**Qué significa.** Subestimó la jugada en $\varepsilon$ o más: es el error que puede congelarla.
:::

::: theorem {#jue-c3-teo-hoeffding title="Desigualdad de Hoeffding, citada"}
Toma **una jugada**, **una regla de continuación fija** y $N$ simulaciones **independientes**, con $N$ fijado de antemano. Cada resultado está entre $-1$ y $+1$ y su esperanza es $Q_{\text{azar}}(s,a)$. Para todo $\varepsilon>0$, el promedio $\widehat Q(s,a)$ cumple

$$
\mathbf{\Pr\bigl(\widehat Q(s,a)\le Q_{\text{azar}}(s,a)-\varepsilon\bigr)\le e^{-N\varepsilon^2/2}}.
$$

La otra cola, $\widehat Q(s,a)\ge Q_{\text{azar}}(s,a)+\varepsilon$, tiene la misma cota.

**Fuente:** W. Hoeffding, «Probability inequalities for sums of bounded random variables», *Journal of the American Statistical Association*, 1963, teorema 2.
:::

Aquí $N=N(s,a)$: las simulaciones de una sola jugada.

**Qué dice y qué no dice.**

- **Habla de $Q_{\text{azar}}$.** No mide el error respecto del $Q$ minimax: la esperanza es la de la regla fija.
- **La probabilidad es del muestreo.** La esperanza está fija; lo que cambia al repetir es el promedio. No dice dónde caerá la siguiente simulación.
- **Pide $N$ fijo.** Si la cantidad de muestras depende de los resultados, como en UCB, el lema no se aplica tal cual.

**¿Por qué esta desigualdad?**

- **Solo pide resultados independientes y acotados.** No hay que conocer la varianza ni la forma de la distribución.
- **Vale para todo $N$**, también para 3 o 10. La aproximación normal pide muchas simulaciones, y MCTS decide con pocas.
- **Cae exponencialmente** con $N$. Otras cotas generales bajan solo como $1/N$.

**Mover el margen.** Con $N=100$ fijo, pedir un error más grande da una cota mucho menor. Los datos no mejoraron: la pregunta es más extrema.

::: table {#jue-c3-tabla-mover-eps title="La cota con 100 simulaciones"}
| $\varepsilon$ | Cota |
|---:|---:|
| 0.1 | 60.65 % |
| 0.2 | 13.53 % |
| 0.4 | 0.0335 % |
:::

**Mover las simulaciones.** Con $\varepsilon=0.2$ fijo, más simulaciones bajan la cota. La tabla la compara con lo medido para la jugada y, con $Q_{\text{azar}}=0.3$: en 20 000 tiradas, cuántas veces $\widehat Q\le0.1$ al llegar a cada $N$.

::: table {#jue-c3-tabla-hoeffding title="La jugada y: el fallo baja rápido con N"}
| $N$ | Medido | Cota |
|---:|---:|---:|
| 10 | 24.7 % | 81.9 % |
| 50 | 7.1 % | 36.8 % |
| 100 | 2.4 % | 13.5 % |
| 200 | 0.2 % | 1.8 % |
:::

**La cota es holgada.** En estas filas queda muy arriba de lo medido; acota la probabilidad, no cada frecuencia que pudiera observarse. A cambio, vale para cualquier jugada acotada.

::: figure {#jue-c3-fig-hoeffding title="La cota baja con ε; el margen baja con N"}
![Dos paneles. Arriba, la cota de Hoeffding e^(−Nε²/2) contra el margen ε, con N = 100: baja muy rápido; marcas en ε = 0.1, 0.2 y 0.4, con 60.65 %, 13.53 % y 0.0335 %. Abajo, el margen ε = √(2·ln(1/δ)/N) contra N, de 10 a 200, en la escala de U, para δ = 0.05 y δ = 0.005: las dos curvas bajan como 1/√N y la de δ menor queda un tercio más arriba; con N = 100, 0.245 y 0.326](../_assets/jue-c3-hoeffding.svg)
:::

::: exercise {#jue-c3-ej-fila-cota title="Calcula una fila de la cota"}
1. **La cuenta.** Con $N=100$ y $\varepsilon=0.2$, calcula la cota. ¿Coincide con la tabla?
2. **La lectura.** Lo medido fue 2.4 %. ¿Contradice eso la cota?
:::

::: hint {#jue-c3-pista-fila-cota-1 of="jue-c3-ej-fila-cota" title="El exponente"}
¿Cuánto vale $N\varepsilon^2/2$ con esos números?
:::

::: answer {#jue-c3-resp-fila-cota of="jue-c3-ej-fila-cota"}
1. **Sí coincide.** $100\cdot0.04/2=2$ y $e^{-2}\approx0.135$: el 13.5 % de la tabla.
2. **No la contradice.** La cota dice «a lo más»; 2.4 % queda muy por debajo.
:::

> [!TIP]
> **▶ [Hoeffding en vivo](../_assets/hoeffding_en_vivo.html)**: miles de promedios a la vez. Mueve la esperanza, las simulaciones y el margen, y compara la frecuencia de fallo con la cota.

---

## 3 · Del lema al bono

**Piensa: si aceptas fallar 5 % de las veces, ¿cuánto margen necesitas con 100 simulaciones?**

Unos 0.24. Basta igualar la cota a lo que aceptas y despejar.

::: definition {#jue-c3-delta title="La probabilidad de fallo"}
**Qué es.** $\delta$, entre 0 y 1, es la probabilidad de fallar por debajo que **tú eliges** tolerar.

**Cómo se usa.** Se pide $\Pr\bigl(\widehat Q(s,a)\le Q_{\text{azar}}(s,a)-\varepsilon\bigr)\le\delta$ y se busca el $\varepsilon$ que lo cumple.

**Qué no es.** No es algo que el algoritmo descubra. El algoritmo recibe $c$; $\delta$ es la lectura de esa $c$.
:::

**El despeje.** Iguala la cota a $\delta$, saca logaritmo y despeja:

$$
e^{-N\varepsilon^2/2}=\delta
\quad\Longrightarrow\quad
\mathbf{\varepsilon=\sqrt{\frac{2\ln(1/\delta)}{N}}}.
$$

- **En palabras:** salvo una mala suerte de probabilidad a lo más $\delta$, el promedio no queda más de $\varepsilon$ por debajo de su esperanza.
- **Ejemplo:** con $\delta=e^{-2}\approx0.14$ y $N=100$, sale $\varepsilon=0.2$, la fila de 100 leída al revés. Con 5 %, $\ln20\approx3.00$ y $\varepsilon\approx0.24$.

::: exercise {#jue-c3-ej-despeja title="Mueve una perilla a la vez"}
1. **Más simulaciones.** Si $N$ se multiplica por 4, ¿qué le pasa a $\varepsilon$?
2. **Menos fallo.** Si pides un $\delta$ más chico, ¿el margen crece o se encoge? ¿Rápido o despacio?
:::

::: hint {#jue-c3-pista-despeja-1 of="jue-c3-ej-despeja" title="Dónde aparece cada cosa"}
¿Está $N$ arriba o abajo de la fracción, y dentro de qué raíz? ¿Qué función envuelve a $1/\delta$?
:::

::: answer {#jue-c3-resp-despeja of="jue-c3-ej-despeja"}
1. **Se divide entre 2.** $N$ está abajo, dentro de una raíz, y $\sqrt4=2$.
2. **Crece, pero despacio.** $1/\delta$ entra por un logaritmo: pedir diez veces menos fallo, de 0.05 a 0.005, hace crecer el margen solo un tercio. Con $N=100$, pasa de 0.245 a 0.326.
:::

**Sumar el margen: la cota optimista.** El error que congela es quedarse corto. Por eso se suma el margen, en vez de restarlo.

::: definition {#jue-c3-cota-optimista title="La cota optimista"}
**Qué es.** La **cota optimista** de una jugada de MAX es $\widehat Q(s,a)+\varepsilon$, en la escala de $U$ y desde MAX.

**Qué significa.** Es un límite probabilístico para $N$ fijo: al repetir el muestreo, la esperanza lo supera con probabilidad a lo más $\delta$, porque $Q_{\text{azar}}>\widehat Q+\varepsilon$ es un caso del fallo por debajo. Elegir con **optimismo** es elegir la cota más alta.

**Qué no es.** No es un pago: es un **puntaje**. Puede pasar de $+1$, y no es la $\beta$ de alfa-beta ni una cota segura de la tabla de transposición.
:::

**Con $\delta$ fijo, la cota puede quedarse congelada.** Su margen depende solo de su propia $N(s,a)$: si la jugada deja de elegirse, su cota no se mueve. Y el 5 % acota el fallo de **una** comprobación con $N$ fijo; no es una frecuencia. En miles de vueltas se hacen miles de comprobaciones, y la probabilidad de que alguna falle ya no queda acotada por ese 5 %.

**El arreglo: pedir más confianza conforme avanza el reloj.** Con $\delta=N(s)^{-4}$, $\ln(1/\delta)=4\ln N(s)$ y el margen queda

$$
\varepsilon=\sqrt{\frac{8\ln N(s)}{N(s,a)}}=\mathbf{2\sqrt2\,\sqrt{\frac{\ln N(s)}{N(s,a)}}}.
$$

**Es el bono con $c=2\sqrt2\approx2.83$: la constante de UCB1** (Auer, Cesa-Bianchi y Fischer, 2002) **en el bandido estacionario**, con pagos en $[-1,1]$. El puntaje del bloque 1 es la cota optimista.

- **Una jugada olvidada ya no se congela.** Su $N(s,a)$ queda quieta, pero $N(s)$ crece y su bono también, sin tope.
- **El 4 es una elección, no una ley.** Hace los fallos tan raros que, sumados sobre todas las vueltas, siguen siendo pocos. Otro exponente da otra $c$.
- **Esto no demuestra la garantía de UCB1, y menos la de UCT.** $N(s,a)$ depende de los resultados, y el lema pedía $N$ fijo. La prueba de UCB1 suma sobre todos los tamaños posibles; no la cubrimos.

**En la corrida de la semilla 36, con bono.** Las cinco primeras vueltas eligen x, y, z, z, z y pagan $-1,-1,+1,-1,-1$. Con $N(s)=5$, $\delta=5^{-4}=1/625$ y $\ln5\approx1.61$:

| Jugada | $N(s,a)$ | $\widehat Q$ | Bono | Puntaje |
|---|---:|---:|---:|---:|
| x | 1 | $-1$ | 3.59 | **2.59** |
| y | 1 | $-1$ | 3.59 | 2.59 |
| z | 3 | $-1/3$ | 2.07 | 1.74 |

**Se le da otra oportunidad a x**: empata con y, pero va primero. Una derrota en una simulación casi no informa, y la cota lo dice.

**La regla no lee la cota como un valor: solo la compara.** Una cota de 2.59, por encima de $+1$, solo dice «aún no sé casi nada de esta jugada».

**Tras 1000 vueltas**, x se lleva 817, y 145 y z 38; sin bono, z se llevaba 998.

**Cada $c$ pide su propio $\delta$.** Al igualar el margen con el bono, con $c>0$ y $N(s)>1$, sale $\delta=N(s)^{-c^2/2}$.

::: table {#jue-c3-tabla-c-delta title="La c del puntaje y el δ que pide"}
| $c$ | $\delta$ | Con $N(s)=100$ |
|---|---|---:|
| $1$ | $N(s)^{-1/2}$ | 10 % |
| $2\sqrt2$ | $N(s)^{-4}$ | $10^{-8}$ |
:::

**Ese 10 % es una cota nominal para $N$ fijo, no una tasa real de errores.** El algoritmo recibe $c$; $\delta$ solo interpreta esa elección.

::: figure {#jue-c3-fig-bono title="El bono baja con N(s,a) y sube con N(s)"}
![Gráfica. Eje horizontal: N(s,a), simulaciones de la jugada, de 0 a 200. Eje vertical: el bono 2√2·√(ln N(s)/N(s,a)), en la escala de U, de 0 a 4. Tres curvas, una por N(s): 100 continua, 1 000 con rayas y 10 000 con puntos; las tres bajan al crecer N(s,a), y con más N(s) quedan más arriba, pero poco: el logaritmo crece despacio. Las de N(s) = 100 acaban en N(s,a) = 100. Puntos sobre la curva de 100 en N(s,a) = 10, 30 y 60: el bono vale 1.92, 1.11 y 0.78. Una cuarta curva, c = 1 con N(s) = 100, queda muy por debajo: 0.68 en N(s,a) = 10](../_assets/jue-c3-bono.svg)
:::

**Con $N(s,a)$ fijo, el bono sube de una curva a la siguiente.** Es la jugada olvidada: su bono crece con el reloj.

---

## 4 · MIN usa la otra cola

**Piensa: en un nodo de MIN, ¿hay que cambiar el signo de $c$?**

No. Cambia el lado optimista, no la duda.

| Mueve | Elige |
|---|---|
| MAX | El mayor $\mathbf{\widehat Q(s,a)+\text{bono}}$ |
| MIN | El menor $\mathbf{\widehat Q(s,a)-\text{bono}}$ |

- **MIN quiere $\widehat Q$ bajo.** Su optimismo es que la jugada valga para MAX menos de lo que parece; usa la otra cola: $\Pr\bigl(Q_{\text{azar}}<\widehat Q-\varepsilon\bigr)\le\delta$.
- **$c$ no cambia de signo ni de tamaño.** La duda es la misma de los dos lados, porque Hoeffding es simétrica.
- **Una traducción, una vez.** Elegir el menor $\widehat Q-\text{bono}$ es lo mismo que elegir el mayor $-\widehat Q+\text{bono}$.
- **Supone suma cero o constante.** Que MIN minimice el pago de MAX requiere pagos opuestos; el lema mismo no lo pide.

**Ejemplo.** Un nodo de MIN lleva $N(s)=50$ vueltas. Sus hijos p, q, r tienen $\widehat Q$ de $-0.2$, $0.25$ y $0.5$, medidos desde MAX, con $N(s,a)$ de 30, 16 y 4. Con $c=2\sqrt2$, los bonos son 1.02, 1.40 y 2.80.

::: figure {#jue-c3-fig-min-volteado title="MIN usa la otra cola: el bono se resta"}
![Tres jugadas de un nodo de MIN, p, q y r, con Q̂ de −0.2, 0.25 y 0.5 y N(s,a) de 30, 16 y 4; N(s) = 50 y c = 2√2; bonos 1.02, 1.40 y 2.80. Fila de arriba, «si eligiera MAX»: cada bigote sale hacia la derecha del punto, hasta Q̂ + bono. Fila de abajo, «elige MIN»: el mismo bigote sale hacia la izquierda, hasta Q̂ − bono: −1.22, −1.15 y −2.30. MIN elige r, el extremo más bajo](../_assets/jue-c3-min-volteado.svg)
:::

Los puntajes de MIN son $-1.22$, $-1.15$ y $-2.30$. **Baja por r:** el peor promedio para MIN, pero con solo 4 simulaciones.

**Intenta el ejercicio sin abrir las pistas ni la respuesta, y sin pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-bono title="Aplica el bono en un nodo de MIN"}
Usa el nodo del ejemplo. Trata a cada hijo como una jugada del bandido: no importa qué pasa debajo. Usa $\ln50\approx3.91$ y $\ln20\approx3.00$.

1. **Un margen.** Con $\delta=0.05$, calcula el margen de p. ¿Qué lado de su esperanza le importa a MIN?
2. **Otra $c$.** Repite la selección con $c=1$. ¿Por cuál baja?
3. **Entregar.** Si $s$ fuera la raíz y se acabara el tiempo, ¿qué jugada se entrega?
4. **El signo.** Si MIN usara $\widehat Q+\text{bono}$ y eligiera el menor, ¿qué haría con las jugadas poco probadas?
:::

::: hint {#jue-c3-pista-final-bono-1 of="jue-c3-ej-final-bono" title="Pista 1 · Desde qué lado"}
¿Qué número quiere MIN que sea chico? ¿Qué parte del puntaje no depende de quién elige?
:::

::: hint {#jue-c3-pista-final-bono-2 of="jue-c3-ej-final-bono" title="Pista 2 · Revisa tu borrador"}
¿El hijo menos probado recibió el bono más grande? ¿Qué número miraste en el inciso 3, y es el mismo que en el 2?
:::

::: answer {#jue-c3-resp-final-bono of="jue-c3-ej-final-bono" title="Respuesta · Optimismo desde el lado de MIN"}
1. **El margen de p es 0.45.** $\varepsilon=\sqrt{2\cdot3.00/30}\approx0.45$. A MIN le importa que la esperanza sea **más baja** de lo que parece: su cota optimista es el piso $-0.2-0.45=-0.65$. El bono con $c=2\sqrt2$, 1.02, es más del doble: pide $\delta=50^{-4}$, mucho menos que 5 %.
2. **Con $c=1$ baja por p.** Bonos 0.36, 0.49 y 0.99; puntajes $-0.56$, $-0.24$ y $-0.49$. La $c$ chica casi no explora.
3. **Se entrega p**, la de más visitas, 30. Entregar no usa el bono.
4. **Huiría de lo incierto.** Con $c=2\sqrt2$, los puntajes serían 0.82, 1.65 y 3.30: elegiría p y dejaría r congelada.

**La constante no se voltea: el bono empuja hacia el extremo que favorece a quien mueve.**
:::

---

## 5 · ¿Qué constante c usar?

**Piensa: si $2\sqrt2$ sale de la cuenta de UCB1, ¿es la que mejor juega?**

No necesariamente. Esa constante hace válida la prueba de UCB1; jugar bien con un presupuesto dado es otra pregunta.

**Lo que garantiza.** Con $c=2\sqrt2$ en el bandido estacionario, UCB1 asegura que, en esperanza, las vueltas gastadas en una jugada peor crecen a lo más como $\ln N(s)$. La cota trae constantes que dependen de cuánto pierde esa jugada; una $c$ menor no hereda esa prueba.

**Lo que explora.** Con $N(s)=100$, la de UCB1 da bonos casi tres veces más grandes que $c=1$.

::: table {#jue-c3-tabla-bono title="El bono con N(s) = 100"}
| $N(s,a)$ | $c=2\sqrt2$ | $c=1$ |
|---:|---:|---:|
| 10 | 1.92 | 0.68 |
| 30 | 1.11 | 0.39 |
| 60 | 0.78 | 0.28 |
:::

**Cuatro reglas en el bandido x, y, z.** Siempre el mejor promedio; a veces al azar, que tras probar las tres elige al azar con probabilidad 0.1; UCB con $c=2\sqrt2$; y UCB con $c=1$. Cada una corre 40 veces, con las semillas 1 a 40, y cada **corrida** tiene 10 000 vueltas. Una corrida está **atorada** si deja en x menos de la mitad de sus vueltas.

::: table {#jue-c3-tabla-corridas title="Cuántas corridas encuentran x"}
| Regla | En x | Atoradas |
|---|---:|---:|
| Mejor promedio | 34 | 6 |
| Al azar 10 % | 40 | 0 |
| UCB, $c=2\sqrt2$ | 40 | 0 |
| UCB, $c=1$ | 40 | 0 |
:::

- **Sin bono es todo o nada.** De las 6 atoradas, 5 se quedan en y y 1 en z; desde la vuelta 100, el 85 % de las elecciones va a x, que es $34/40$.
- **Las otras tres no se atoran.** Su peor corrida deja en x 0.90, 0.92 y 0.96 de sus vueltas.
- **La semilla 36 no tiene regreso.** x quedó en $-1$ y z ya ganó. En las otras 5, x quedó en 0 o en $-0.2$: una racha mala muy larga de y podría devolverla.

**El pago** de una vuelta es su $U$; la tabla da el promedio acumulado por vuelta, sobre las 40 corridas. Lo mejor posible es 0.6, siempre x.

::: table {#jue-c3-tabla-pagos-finales title="Pago promedio por vuelta, 40 corridas"}
| Regla | Vuelta 10 | Vuelta 10 000 |
|---|---:|---:|
| Mejor promedio | 0.400 | 0.543 |
| Al azar 10 % | 0.385 | 0.564 |
| UCB, $c=2\sqrt2$ | 0.295 | 0.580 |
| UCB, $c=1$ | 0.340 | 0.598 |
:::

- **Explorar cuesta al principio.** En la vuelta 10, la regla sin bono gana más que las dos UCB.
- **Sin bono se queda abajo.** Con 34, 5 y 1 corridas en x, y, z se espera $(34\cdot0.6+5\cdot0.3-0.2)/40=0.5425$.
- **A veces al azar no se atora, pero sigue tirando.** Ya en x, la elige $0.9+0.1/3\approx93.3\,\%$ de las veces.
- **Aquí $c=1$ juega mejor.** Explora menos, llega antes y paga 0.598; la de UCB1, 0.580.

**Lo mismo en el árbol de resultados.** Con 500 semillas de 200 vueltas, las dos $c$ terminan con centro como la más visitada. Cambia desde qué vuelta lo es sin soltarlo, hasta la 200.

::: table {#jue-c3-tabla-c-semillas title="Vuelta desde la que centro es la más visitada"}
| $c$ | Mediana | 90 % llega en |
|---|---:|---:|
| $1$ | 18 | 31 o antes |
| $2\sqrt2$ | 29 | 36 o antes |
:::

**En la práctica, $c$ se afina.** No hay una $c$ óptima universal: depende de la escala, el árbol, la simulación y el presupuesto.

1. **Fija lo que no cambia.** Escala de los pagos, algoritmo y presupuesto por jugada.
2. **Barre una rejilla.** Por ejemplo 0.25, 0.5, 1, 2, $2\sqrt2$ y 4 en $[-1,1]$, y compara siempre con $c=0$.
3. **Mide la jugada entregada.** En varias posiciones y semillas, o en partidas completas contra un rival fijo.
4. **Valida aparte.** Confirma la elegida en posiciones y semillas que no usaste para elegirla.

En la literatura, $c$ varía por dominio y suele ajustarse a mano (Browne y coautores, 2012, *A survey of Monte Carlo tree search methods*); con mejoras como RAVE, en Go la mejor resultó 0.

**Al cambiar la escala de los pagos, cambia la del bono.** El margen mide distancias en unidades de $U$:

| Pagos | Cota | $c$ de UCB1 |
|---|---|---:|
| $[0,1]$ | $e^{-2N\varepsilon^2}$ | $\sqrt2$ |
| $[-1,1]$ | $e^{-N\varepsilon^2/2}$ | $2\sqrt2$ |
| $[-100,100]$ | $e^{-N\varepsilon^2/20000}$ | $200\sqrt2$ |

**Otros textos** usan la escala de 0 a 1, $(U+1)/2$, y escriben $c=\sqrt2$. Es la misma regla: pasar a $[-1,1]$ multiplica cada puntaje por 2 y resta 1, y con ello dobla $c$. Con la **misma** $c$ en las dos escalas, en cambio, la de 0 a 1 explora como si $c$ fuera el doble.

> [!TIP]
> **▶ [Bandido en vivo](../_assets/bandido_en_vivo.html)**: x, y, z con su esperanza oculta. Mueve $c$ y mira cuántas vueltas van a la mejor.
>
> **Notebook en Colab**: la sección 8 repite estas simulaciones para que las corras tú.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

---

## 6 · Por qué en el árbol es solo intuición

**Piensa: en UCT, ¿las simulaciones que pasan por una jugada siguen siendo muestras de una esperanza fija?**

No. UCT pone un bandido en cada nodo, y debajo de cada jugada hay otros bandidos que van aprendiendo.

- **La selección adaptativa ya existía en UCB1.** Cuántas veces se prueba cada jugada depende de lo que salió; la prueba de UCB1 ya lo cubre.
- **En UCT, además, cambia lo que se mide.** El árbol crece y la selección de abajo se mueve: la distribución de las continuaciones cambia mientras se promedia.
- **El blanco se desplaza.** Los resultados de una jugada no son muestras de un $Q_{\text{azar}}$ fijo. Por eso el bono no es un intervalo de confianza alrededor de $Q(s,a)$.

**El bono conserva la forma del margen, pero ese margen, aquí, no se aplica directo.**

**Lo que sí se demostró, aparte.** Kocsis y Szepesvári (2006), *Bandit based Monte-Carlo Planning*, probaron que, con una constante bastante grande, la probabilidad de que UCT elija en la raíz una jugada peor que la de minimax tiende a 0 al crecer las vueltas.

- **Llega a la jugada de minimax**, no a la de mayor $Q_{\text{azar}}$.
- **Su constante no es la $2\sqrt2$ de UCB1.** La ajustan para cubrir cuánto se mueven los promedios de abajo.
- **Llegar no pide una $c$ grande.** En un árbol finito, con cualquier $c>0$ fija y vueltas sin límite, el bono de una jugada poco probada sigue creciendo con $\ln N(s)$: UCT termina probándolas todas.
- **El argumento sube desde los finales.** Las jugadas peores reciben una fracción de visitas que se encoge, y cada promedio se acerca al de la mejor respuesta. La $c$ grande es la que da una cota de qué tan rápido.

**Punto de control:** deberías poder leer cada pieza del bono, despejar el margen dados $\delta$ y $N$, leer una $c$ como un $\delta$, y calcular el puntaje en un nodo de MAX o de MIN.

## Lo que hay que llevarse

- **El bono hace emerger la exploración.** Baja con $N(s,a)$ y sube con $\ln N(s)$; sin él, una corrida deja 998 de 1000 vueltas en la peor jugada.
- **Hoeffding acota cuánto falla un promedio** de $N$ simulaciones independientes en $[-1,1]$, con $N$ fijo: a lo más $e^{-N\varepsilon^2/2}$. Habla de $Q_{\text{azar}}$, no de $Q$.
- **Despejar da el margen,** $\varepsilon=\sqrt{2\ln(1/\delta)/N}$, y $\delta$ la eliges tú. Con $\delta=N(s)^{-4}$ sale $c=2\sqrt2$, la de UCB1 en el bandido estacionario.
- **MIN usa la otra cola:** elige el menor $\widehat Q-\text{bono}$, y $c$ no cambia de signo.
- **La $c$ de UCB1 hace válida su prueba, no juega mejor.** Aquí $c=1$ paga 0.598 contra 0.580; en la práctica, $c$ se afina con partidas y validación, en la escala de los pagos.
- **En el árbol, la cuenta es intuición.** Las continuaciones cambian mientras se promedia; la convergencia de UCT se prueba aparte.

Continúa con la [[tarea-cuando-no-cabe|tarea de la clase]].
