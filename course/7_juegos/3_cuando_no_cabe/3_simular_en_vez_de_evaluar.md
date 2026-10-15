---
id: simular-en-vez-de-evaluar
title: "Simular partidas: promedios y actualización minimax"
nav_title: Simular partidas
summary: "Cuando el árbol no cabe y no hay EVAL, se juegan partidas al azar hasta el final. Monte Carlo plano promedia su U por jugada de la raíz y converge a Q_azar, lo que paga jugar si los dos eligen al azar. La actualización minimax usa las mismas partidas, guarda lo que descubre y sube máximos y mínimos: converge a V en un árbol finito."
status: ready
estimated_time: 48m
tags: [juegos, busqueda-adversarial, monte-carlo]
---

# Simular partidas: promedios y actualización minimax

**¿Cómo puedes elegir una jugada sin recorrer todo el árbol ni escribir una función de evaluación?**

Puedes simular partidas hasta un final. El número que obtengas dependerá de cómo uses sus resultados.

- **Con Monte Carlo plano**, calcularás promedios que estiman el resultado de jugar al azar.
- **Con actualización minimax**, guardarás lo descubierto y subirás máximos y mínimos.
- **Con las trazas**, distinguirás una estimación, una jugada desconocida y un valor demostrado.

## Lo que traes

- **Las reglas generan el juego.** $S_F$ reconoce finales (@jue-c1-finales); $\mathrm{Pl}(s)$ lee quién mueve (@jue-c1-pl); $A(s)$ enumera jugadas (@jue-c1-acciones); $T(s,a)$ produce el siguiente estado (@jue-c1-transicion); $U$ paga los finales (@jue-c1-utilidad): $+1$ si gana MAX, $-1$ si gana MIN y $0$ si empatan.
- **El valor se mide desde MAX.** $V(s)$ supone juego óptimo de ambos; $Q(s,a)=V(T(s,a))$ valora una jugada (@jue-c1-valor-jugada-estrategia).
- **Cada turno tiene su operador.** MAX elige el mayor $Q$; MIN, el menor; AZAR promedia con $\Pr(a\mid s)$ (@jue-c2-valor-esperado).
- **El corte necesita una evaluación.** En [[cortar-y-evaluar|Cortar y evaluar]], $\mathrm{EVAL}$ estima lo que queda debajo de la frontera.

> **Las reglas del 4×4.** Las columnas son a–d y las filas, 1–4. Blancas (B, MAX) empieza con cuatro peones en la fila 1; Negras (N, MIN), en la fila 4.
>
> Empiezan Blancas. Un peón avanza una casilla vacía o captura en diagonal hacia delante. Gana quien llega a la fila rival, captura todo o deja al rival sin jugada. $U=+1$ si gana Blancas y $U=-1$ si gana Negras.

> **Supuestos.** Son juegos por turnos, deterministas y de información perfecta. Buscar todos los finales cuesta demasiado y no tenemos una $\mathrm{EVAL}$ confiable. Jugar una partida al azar hasta el final sí resulta barato.

---

## 1 · Un árbol que no cabe

**Piensa: sin EVAL y sin tiempo para explorar todo, ¿qué sigue disponible?**

Las reglas: permiten terminar una partida y leer su pago.

En este árbol, MAX y MIN alternan. Cada nodo tiene hasta $b$ jugadas y ninguna partida supera $m$. Los «…» indican que el dibujo continúa.

$$
\mathbf{U(s)}=
\begin{cases}
+1 & \text{si gana MAX},\\
0 & \text{si empatan},\\
-1 & \text{si gana MIN}.
\end{cases}
$$

- **El pago existe solo en los finales.** Un estado intermedio tiene valor $V$, pero todavía no tiene $U$.
- **La perspectiva permanece fija.** $+1$ favorece a MAX y $-1$ favorece a MIN, sin importar quién mueve.

::: figure {#jue-c3-mcg-fig-arbol title="Un árbol de juego grande"}
![Árbol con hasta b jugadas por nodo y m niveles. Los puntos suspensivos indican las ramas omitidas; los finales tienen su pago U.](../_assets/jue-c3-mcg-arbol.svg)
:::

### Qué cuesta cada alternativa

- **Minimax recorre todo.** Examina del orden de $b^m$ nodos.
- **Alfa-beta ahorra mediante poda.** Con orden perfecto baja a cerca de $b^{m/2}$; el crecimiento sigue siendo exponencial.
- **El corte reduce la profundidad.** Se detiene en $d$, pero depende de una buena $\mathrm{EVAL}$.

Una partida cuesta del orden de $m$ jugadas, frente a $b^m$ para explorar todas las continuaciones. Aquí suponemos que el presupuesto alcanza para muchas partidas.

> **Dado:** un estado no final $s_{\text{raíz}}$ donde mueve MAX, las reglas y un presupuesto de simulaciones. No hay función de evaluación.
>
> **Encontrar:** una jugada para MAX con la información reunida antes de agotar el presupuesto.

---

## 2 · Tres preguntas sobre una jugada

**Piensa: ¿qué significa decir que una jugada «vale» cierto número?**

Depende de cómo continuarán los dos jugadores. Llama $s'=T(s,a)$ al estado que resulta de jugar $a$ desde $s$.

| Pregunta | Número | Continuación |
|---|---|---|
| ¿Cuánto asegura MAX? | $Q(s,a)=V(s')$ | Ambos juegan óptimamente |
| ¿Cuánto paga al azar? | $Q_{\text{azar}}(s,a)$ | Ambos eligen uniformemente |
| ¿Qué estima el algoritmo? | $\widehat Q(s,a)$ | Depende de lo observado |

- **Los números sin gorro son exactos.** $Q$ y $Q_{\text{azar}}$ responden preguntas distintas sobre el mismo juego.
- **El gorro indica una estimación.** Cada algoritmo debe declarar qué valor intenta estimar y cómo cambia con los datos.

Para calcular $Q_{\text{azar}}$, tratamos a ambos jugadores como dados uniformes después de la jugada inicial:

$$
\mathbf{
V_{\text{azar}}(s)=
\begin{cases}
U(s) & \text{si }s\in S_F,\\
\displaystyle\sum_{a\in A(s)}
\frac{V_{\text{azar}}(T(s,a))}{|A(s)|}
& \text{si }s\notin S_F,
\end{cases}}
$$

$$
\mathbf{Q_{\text{azar}}(s,a)=V_{\text{azar}}(s')=E[U\mid s']}.
$$

La esperanza supone jugadas uniformes desde $s'$. **Cada camino pesa el producto de $1/|A(s)|$** en los estados que atraviesa. Por eso, en general, no basta promediar las hojas sin ponderarlas.

---

## 3 · Ficha A: Monte Carlo plano

**Piensa: ¿qué puedes aprender jugando muchas partidas al azar desde la misma jugada?**

Su pago promedio contra continuaciones al azar. Monte Carlo plano guarda ese promedio por jugada de la raíz, sin construir un árbol de búsqueda.

### El mapa

- **Qué rastrea.** $\widehat Q(s_{\text{raíz}},a)$ estima $Q_{\text{azar}}(s_{\text{raíz}},a)$.
- **Dónde lo guarda.** Conserva un contador $N(s_{\text{raíz}},a)$ y una suma de pagos por jugada de la raíz.
- **Cómo sube.** No respalda valores entre estados: cada pago actualiza únicamente la jugada inicial.
- **A qué converge.** Cada promedio converge a $Q_{\text{azar}}$ con probabilidad 1, si recibe infinitas simulaciones independientes bajo la misma regla de continuación.

::: figure {#jue-c3-fig-flujo-mc-plano title="Monte Carlo plano, en palabras"}
![Para cada jugada de la raíz, simula k partidas hasta un final y promedia sus pagos. Al terminar, entrega la jugada de mayor promedio.](../_assets/jue-c3-rx-flujo-mc-plano.svg)
:::

::: definition {#jue-c3-simulacion title="Simulación"}
**Qué es.** Una simulación (*rollout*) recorre una partida desde un estado hasta un final. En cada turno elige uniformemente entre las jugadas legales.

**Cómo se calcula.** Su resultado es el pago $U$ del final. El promedio de muchas simulaciones desde $s'=T(s_{\text{raíz}},a)$ es $\widehat Q(s_{\text{raíz}},a)$.

**Qué significa.** Estima $Q_{\text{azar}}$: lo que paga la jugada cuando después ambos juegan al azar.

**Qué no es.** No demuestra cuánto asegura MAX. Una jugada puede ganar casi todas las simulaciones y perder contra una respuesta certera.
:::

Una **simulación** recorre una partida; una **corrida** ejecuta el algoritmo completo, con todas sus simulaciones.

### Exploración: la regla

Fija un entero $k\ge1$. Para cada jugada $a$, en el orden dado, calcula $s'=T(s_{\text{raíz}},a)$ y repite:

1. **Simula hasta un final.** Desde $s'$, ambos eligen uniformemente; al terminar, lee $U$. Si $s'$ ya es final, toma directamente su pago.
2. **Actualiza la jugada inicial.** Suma $U$ a su acumulado y aumenta $N(s_{\text{raíz}},a)$ en una visita.
3. **Completa el presupuesto.** Repite hasta reunir $k$ simulaciones de esa jugada; después pasa a la siguiente.

$$
\mathbf{n=|A(s_{\text{raíz}})|\,k\le b\,k},
\qquad
\mathbf{\widehat Q(s_{\text{raíz}},a)=
\frac{\sum U}{N(s_{\text{raíz}},a)}}.
$$

- **La suma incluye solo las partidas de $a$.** Una victoria aporta $+1$; una derrota, $-1$; un empate, $0$.
- **Cada simulación recorre un camino.** Los estados intermedios se olvidan; distintos recorridos pueden repetir exactamente las mismas jugadas.
- **El invariante está en la raíz.** El contador y la suma corresponden a todas las simulaciones terminadas de esa jugada, siempre desde MAX.

::: figure {#jue-c3-mcg-fig-mc-plano title="Monte Carlo plano en un árbol grande"}
![Las simulaciones recorren caminos hasta finales lejanos. En la raíz quedan N y Q̂ por jugada; debajo no se conservan estados.](../_assets/jue-c3-mcg-mc-plano.svg)
:::

---

### El recorrido: calcular un promedio

**Piensa: MAX gana 7 de 10 simulaciones y pierde 3. ¿Qué promedio obtiene?**

Obtiene $0.4$, porque cada victoria suma $+1$ y cada derrota suma $-1$:

$$
\widehat Q=\frac{7\cdot(+1)+3\cdot(-1)}{10}=0.4.
$$

::: exercise {#jue-c3-ej-cinco title="Calcula dos promedios"}
Desde una jugada se completan 5 simulaciones.

1. **Primera muestra.** MAX gana 3 y pierde 2. ¿Cuánto vale $\widehat Q$?
2. **Segunda muestra.** MAX gana 2 y pierde 3. ¿Cuánto vale ahora?
:::

::: hint {#jue-c3-pista-cinco-1 of="jue-c3-ej-cinco" title="Qué suma cada partida"}
Escribe primero cuánto aporta una victoria y cuánto aporta una derrota.
:::

::: answer {#jue-c3-resp-cinco of="jue-c3-ej-cinco"}
1. **La primera da $0.2$.** $\widehat Q=(3-2)/5=0.2$.
2. **La segunda da $-0.2$.** $\widehat Q=(2-3)/5=-0.2$.

Cambiar una sola victoria por derrota mueve el promedio $0.4$. **Con pocas simulaciones, el número todavía brinca mucho.**
:::

### El recorrido: la posición de la clase

**Piensa: ¿la jugada con mejor promedio al azar también gana contra Negras jugando bien?**

Aquí sí: $\text{d2}\mathbf{-}\text{d3}$.

La tabla calcula $Q_{\text{azar}}$ exactamente, sin muestrear, y muestra sus decimales redondeados. «Corte» usa profundidad 1 y la escala de $\mathrm{EVAL}$, con finales multiplicados por 100.

::: table {#jue-c3-simulaciones title="Lo que paga cada jugada al azar en la posición de la clase"}
| Jugada | $Q_{\text{azar}}(s,a)$ | Corte | $Q(s,a)$ |
|---|---:|---:|---:|
| $\text{a1}\mathbf{-}\text{a2}$ | 0.21 | 2 | −1 |
| $\text{d2}\mathbf{-}\text{d3}$ | **0.89** | 2 | +1 |
| $\text{d2}\mathbf{x}\text{c3}$ | 0.15 | **13** | −1 |
:::

$Q_{\text{azar}}$ y $Q$ están en la escala de $U$, entre $-1$ y $+1$. La columna «Corte» está en otra escala.

**Aquí simular acierta:** favorece el avance ganador y deja última la captura. Las partidas incluyen muchas recapturas de Negras; así revelan que el peón adicional no dura.

### El recorrido: el árbol de resultados

**Piensa: ¿puede el promedio más alto recomendar una jugada que pierde?**

Sí. En este árbol recomendará der, aunque MAX debe jugar centro.

- **La raíz R pertenece a MAX.** Sus jugadas izq, centro y der llevan a I, C y D, donde mueve MIN.
- **I ofrece dos finales.** Sus pagos son $\text{i1}=+1$ e $\text{ix}=-1$.
- **C ofrece dos estados de MAX.** C1 tiene $\text{c1a}=0$ y $\text{c1b}=-1$; C2 tiene $\text{c2a}=+1$ y $\text{c2b}=-1$.
- **D ofrece tres finales.** Sus pagos son $\text{d1}=-1$, $\text{d2}=+1$ y $\text{d3}=+1$.

| Jugada | Cálculo con ambos al azar | $Q_{\text{azar}}$ | $Q$ |
|---|---|---:|---:|
| izq | $(1-1)/2$ | $0$ | $-1$ |
| centro | $((-1/2)+0)/2$ | $-1/4$ | $0$ |
| der | $(-1+1+1)/3$ | $1/3$ | $-1$ |

En centro, C1 promedia $(0-1)/2=-1/2$ y C2 promedia $(1-1)/2=0$. MAX se equivoca la mitad de las veces en ambos.

Con juego óptimo, MIN responde ix en I y d1 en D. En C elige C1, donde MAX asegura el empate con c1a.

**La cuenta que tienta:** si solo MIN jugara al azar, C1 valdría $0$ y C2 valdría $+1$. Centro daría $1/2$ y sería preferible a der. Las simulaciones uniformes también hacen jugar al azar a MAX.

> **Dado:** este árbol, 5 simulaciones por jugada, semilla 0 y orden izq, centro, der.
>
> **Encontrar:** los promedios y la jugada entregada. Cada tramo muestra el acumulado de una jugada.

#### Tramo 1 · Simular izq

| # | Final | $U$ | Suma | $\widehat Q$ |
|---:|---|---:|---:|---:|
| 1 | ix | −1 | −1 | $-1$ |
| 2 | ix | −1 | −2 | $-1$ |
| 3 | i1 | +1 | −1 | $-1/3$ |
| 4 | ix | −1 | −2 | $-1/2$ |
| 5 | ix | −1 | −3 | $-3/5$ |

**Fila 3:** una victoria sube el promedio, aunque MIN conserva la respuesta ix que hace perder a MAX.

#### Tramo 2 · Simular centro

| # | Final | $U$ | Suma | $\widehat Q$ |
|---:|---|---:|---:|---:|
| 6 | c2b | −1 | −1 | $-1$ |
| 7 | c2b | −1 | −2 | $-1$ |
| 8 | c1a | 0 | −2 | $-2/3$ |
| 9 | c2a | +1 | −1 | $-1/4$ |
| 10 | c1b | −1 | −2 | $-2/5$ |

**Fila 10:** centro termina con $-2/5$, por encima del $-3/5$ de izq. El promedio incluye errores de MAX, como elegir c1b.

#### Tramo 3 · Simular der y elegir

| # | Final | $U$ | Suma | $\widehat Q$ |
|---:|---|---:|---:|---:|
| 11 | d3 | +1 | +1 | $1$ |
| 12 | d3 | +1 | +2 | $1$ |
| 13 | d3 | +1 | +3 | $1$ |
| 14 | d1 | −1 | +2 | $1/2$ |
| 15 | d2 | +1 | +3 | $3/5$ |

**Fila 14:** apareció la refutación d1, pero solo redujo el promedio. Al terminar, las sumas son $-3,-2,+3$ y los promedios, $-3/5,-2/5,3/5$. **Entrega der.**

::: figure {#jue-c3-fig-resultados-mc-plano title="Monte Carlo plano: 5 simulaciones por jugada, juega der"}
![Corrida con semilla 0: izq suma −3, centro suma −2 y der suma +3. Cada jugada recibió 5 simulaciones; der tiene el mayor promedio.](../_assets/jue-c3-rx-mc-plano.svg)
:::

#### Repetir la corrida

**Piensa: ¿más simulaciones corregirán esta elección?**

No. La tabla reúne 1000 corridas con semillas distintas. «Sims» indica simulaciones por jugada; cada celda cuenta las corridas que entregaron esa jugada.

::: table {#jue-c3-cmp-reparto-mc title="Qué entrega Monte Carlo plano en 1000 corridas"}
| Sims | izq | centro | der |
|---:|---:|---:|---:|
| 5 | 353 | 106 | 541 |
| 10 | 269 | 53 | 678 |
| 50 | 39 | 1 | 960 |
:::

Por empate se decidieron 233, 157 y 15 corridas, respectivamente. El desempate favorece la primera jugada en el orden izq, centro, der.

Con pocas simulaciones influyen el ruido y los empates. Con 50, casi todas entregan der: **más simulaciones lo vuelven más seguro de la jugada equivocada.**

---

### Elección: qué jugada juega

Al terminar, MAX entrega la jugada de mayor $\widehat Q(s_{\text{raíz}},a)$. En empate, entrega la primera en el orden dado.

| Decisión | Qué compara | Usa resultados |
|---|---|---|
| Explorar | Completa $k$ por jugada | No |
| Jugar | Elige el mayor promedio | Sí |

- **El reparto es fijo.** Una jugada que parece mala recibe tantas simulaciones como una que parece buena.
- **Una interrupción deja cantidades desiguales.** Compara promedios entre jugadas muestreadas, nunca sumas; una jugada sin muestras sigue desconocida.

### Propiedades y supuestos

- **Número que da.** Estima $Q_{\text{azar}}$ por jugada de la raíz; en general, no estima $Q$.
- **Uso de EVAL.** No la necesita: genera jugadas, reconoce finales y lee $U$, sin multiplicar por 100.
- **Garantía.** Con regla fija, muestras independientes y $k\to\infty$, los promedios convergen a $Q_{\text{azar}}$. Ningún presupuesto finito garantiza la jugada minimax.
- **Interrupción.** Puede recomendar una jugada con lo observado (*anytime*); una comparación que incluya todas requiere al menos una simulación por jugada.
- **Tiempo.** Si elegir y aplicar una jugada cuesta $O(1)$, una simulación cuesta $O(m)$; las $n$ cuestan $O(nm)$.
- **Memoria.** Los contadores y sumas ocupan $O(b)$, más el estado de la partida activa. Esta cota supone avanzar sin almacenar todo el camino.
- **Frente a otros métodos.** Usa finales, como minimax, pero muestrea en lugar de recorrer $O(b^m)$ nodos. Evita diseñar EVAL a cambio de responder otra pregunta.
- **Cuándo sirve.** Es una alternativa cuando falta una buena evaluación. Brügmann exploró Monte Carlo en Go en 1993; fue una vía experimental entre 1993 y 2005.

::: table {#jue-c3-eval-contra-mcts title="Cortar y evaluar contra Monte Carlo plano"}
| Rasgo | Cortar y evaluar | Monte Carlo plano |
|---|---|---|
| Necesita | Reglas y $\mathrm{EVAL}$ | Reglas: $A,T,S_F,U$ |
| Se detiene | En profundidad $d$ | En finales |
| Calcula | Minimax del árbol truncado | Estimación de $Q_{\text{azar}}$ |
| Se afina con | Más $d$; mejor $\mathrm{EVAL}$ | Más simulaciones |
:::

Aumentar las simulaciones afina $Q_{\text{azar}}$; no lo convierte en $Q$. El Go ilustra por qué interesa prescindir de una evaluación escrita a mano.

- **Suma cero o constante.** Con dos jugadores, un pago desde MAX permite comparar sus intereses opuestos.
- **Otros intereses.** Con suma no constante o más jugadores, puede promediar $(U_1,\dots,U_n)$ contra políticas fijas. Eso no es $\max^n$ ni garantiza un equilibrio.

### Casos borde

- **Una sola jugada.** Ya está decidida; simularla solo estima cuánto paga con continuaciones al azar.
- **Un hijo final.** Todas sus simulaciones devuelven el mismo $U$; su valor es exacto desde la primera visita.
- **Empate de promedios.** Gana la primera jugada; así se decidieron 233 de las 1000 corridas con 5 simulaciones.
- **Una jugada no visitada.** No tiene promedio; asignarle 0 inventaría un dato.
- **Una respuesta certera tardía.** Actualiza el promedio en $1/N$ de la distancia al nuevo pago, aunque esa respuesta refute la jugada.
- **Finales a distinta profundidad.** Cada simulación termina al reconocer su final; igual $k$ puede costar distinto tiempo. No se favorece ganar pronto, salvo que $U$ lo indique.
- **Un final frente a EVAL.** Aquí siempre se usa $U$; la comparación entre $\mathrm{EVAL}$ y $100\cdot U$ pertenece al método con corte.
- **Ciclos sin terminación.** Una simulación podría no terminar. Hace falta una regla del juego que determine cómo termina y qué paga.

---

### Intuición: precisión y refutación

**Piensa: ¿qué hace más confiable un promedio, y qué deja sin resolver?**

Más muestras reducen su incertidumbre sobre $Q_{\text{azar}}$. No cambian el supuesto de que ambos juegan al azar.

La intuición de Hoeffding requiere pagos acotados, muestras independientes y una continuación fija. También fija de antemano el número de muestras.

- **El margen rodea $Q_{\text{azar}}$.** No mide la distancia al valor minimax.
- **El margen decrece como $1/\sqrt N$.** Cuatro veces más simulaciones permiten la mitad de margen, manteniendo la misma confianza.
- **El error observado puede aumentar.** Una nueva partida puede alejar el promedio, aunque el margen probable se reduzca.
- **Pocas muestras pueden engañar.** Una jugada mediocre puede encabezar la comparación por suerte.

Ahora MAX elige $a$ o $b$; después MIN elige un final:

| Jugada | Finales de MIN | $Q_{\text{azar}}$ | $Q$ |
|---|---|---:|---:|
| $a$ | $+1,+1,-1$ | $1/3$ | $-1$ |
| $b$ | $0,0$ | $0$ | $0$ |

- **La refutación gana.** MIN puede elegir $-1$ en $a$; su frecuencia durante las simulaciones no cambia esa posibilidad.
- **El promedio favorece $a$.** $(1+1-1)/3=1/3>0$; con muchas simulaciones la elige casi siempre y pierde contra MIN.
- **Más respuestas favorables agrandan la distancia.** Con una sola refutación, $Q_{\text{azar}}$ se acerca a $+1$ mientras $Q$ permanece en $-1$.

**Converge, pero al número equivocado para decidir contra juego óptimo.**

### Intuición: quién juega al azar

**Piensa: las tres aperturas de hexapawn valen $-1$. ¿Sus promedios al azar también son negativos?**

No: los tres son positivos. Negras puede asegurar la victoria, pero se equivoca seguido al elegir uniformemente.

::: table {#jue-c3-hexapawn-azar title="Hexapawn: uno o ambos jugadores al azar"}
| Apertura | Ambos al azar: $Q_{\text{azar}}$ | Solo Negras al azar |
|---|---:|---:|
| $\text{a1}\mathbf{-}\text{a2}$ | 7/36 | 5/9 |
| $\text{b1}\mathbf{-}\text{b2}$ | 5/24 | 3/4 |
| $\text{c1}\mathbf{-}\text{c2}$ | 7/36 | 5/9 |
:::

En la última columna Blancas elige lo mejor, como en [[cuando-decide-un-dado|Cuando decide un dado]]. Por eso $\text{b1}\mathbf{-}\text{b2}$ tiene tres números: $-1$, $5/24$ y $3/4$.

::: remark {#jue-c3-cmp-v-no-es-u title="El azar del juego y el azar del algoritmo"}
**El ejemplo mínimo.** MIN elige entre finales $+1$ y $-1$. Su valor es $V=-1$, pero $V_{\text{azar}}=0$: el promedio uniforme sí converge, a 0.

**El azar del juego.** Expectiminimax promedia transiciones que las reglas asignan a un dado. En los turnos de los jugadores mantiene sus elecciones óptimas.

**El azar del algoritmo.** Monte Carlo plano simula decisiones aleatorias, aunque el juego no tenga dados. Su límite es $Q_{\text{azar}}$, que puede diferir de $Q$.

**La misma cuenta puede responder otra pregunta.** En D, el promedio $1/3$ sería su valor si decidiera un dado uniforme. Con MIN decidiendo, $Q(\text{der})=-1$.
:::

---

### Ejercicios: interpretar y cambiar el modelo

::: exercise {#jue-c3-ej-promedio title="Traduce una esperanza a partidas ganadas"}
Sin empates, $U=\pm1$ y $p=(Q_{\text{azar}}+1)/2$, donde $p$ es la probabilidad de victoria de MAX.

1. **El avance ganador.** Si $\text{d2}\mathbf{-}\text{d3}$ tiene $Q_{\text{azar}}=8/9$, ¿con qué probabilidad gana Blancas al azar?
2. **La apertura de hexapawn.** Si $\text{b1}\mathbf{-}\text{b2}$ tiene $Q_{\text{azar}}=5/24$, ¿qué fracción gana? ¿Por qué es compatible con $Q=-1$?
3. **Una muestra observada.** Si sustituyes $Q_{\text{azar}}$ por $\widehat Q$, ¿qué representa la cuenta?
:::

::: hint {#jue-c3-pista-promedio-1 of="jue-c3-ej-promedio" title="Qué supone cada número"}
Identifica primero quién juega al azar. Después distingue una esperanza exacta de un promedio calculado con una muestra.
:::

::: answer {#jue-c3-resp-promedio of="jue-c3-ej-promedio"}
1. **La probabilidad es $17/18$.** $(8/9+1)/2=17/18$: gana 17 de cada 18 partidas en promedio, sin garantizar esa frecuencia en cada muestra.
2. **La probabilidad es $29/48$.** $(5/24+1)/2=29/48$, un poco más de 6 de cada 10; $Q=-1$ supone que Negras responde óptimamente.
3. **Sale una proporción observada.** Es la fracción de victorias en esa muestra; no la probabilidad verdadera.

El $3/4$ de la clase 2 corresponde a otro supuesto: Blancas elige óptimamente y solo Negras juega al azar.
:::

::: exercise {#jue-c3-ej-cambio title="Señala qué método hay que rehacer"}
Cambia una regla del 4×4: cada peón puede avanzar dos casillas en su primera jugada.

1. **Monte Carlo plano.** Con las reglas actualizadas, ¿puede conservar su procedimiento?
2. **Cortar y evaluar.** ¿Qué pieza debes revisar y por qué?
:::

::: hint {#jue-c3-pista-cambio-1 of="jue-c3-ej-cambio" title="Quién escribió cada pieza"}
Distingue el procedimiento de búsqueda, las reglas que consulta y la evaluación diseñada para el juego anterior.
:::

::: answer {#jue-c3-resp-cambio of="jue-c3-ej-cambio"}
1. **Sí.** Si $A,T,S_F,U$ describen el juego nuevo, sus simulaciones ya lo siguen.
2. **Debes revisar EVAL.** Un peón más rápido puede cambiar el valor de avanzar. El procedimiento minimax con corte sigue siendo el mismo.
:::

::: exercise {#jue-c3-cmp-ej-cambia-hoja title="Cambia una hoja y mira quién se mueve"}
En el árbol de resultados, cambia solo $\text{d2}$ a $-1$.

1. **Juego óptimo.** ¿Cambia $V$ o la jugada que lo alcanza?
2. **D como dado uniforme.** ¿Cuánto vale D y qué juega MAX? ¿Por qué cambiar d3 produciría lo mismo?
3. **Monte Carlo plano.** Con muchas simulaciones, ¿qué entrega y cuánto vale contra MIN?
:::

::: hint {#jue-c3-cmp-pista-cambia-hoja of="jue-c3-cmp-ej-cambia-hoja" title="Una pregunta por número"}
MIN ya podía responder d1. Para el dado, cuenta los pagos; para Monte Carlo plano, compara los tres $Q_{\text{azar}}$.
:::

::: answer {#jue-c3-cmp-resp-cambia-hoja of="jue-c3-cmp-ej-cambia-hoja"}
1. **No cambia.** $V=0$ por centro; der sigue valiendo $-1$ porque MIN ya elegía d1.
2. **D vale $-1/3$.** $(-1-1+1)/3=-1/3$, así que MAX elige centro y obtiene $0$. Cambiar d3 deja la misma distribución de pagos.
3. **Entrega izq.** Sus límites son $0,-1/4,-1/3$; gana el primero. Sin embargo, izq vale $-1$ contra la respuesta ix.
:::

::: exercise {#jue-c3-cmp-ej-mas-sims title="Predice con un millón de simulaciones"}
Con un millón de simulaciones por jugada, ¿qué entregaría Monte Carlo plano en casi todas las corridas del árbol de resultados? ¿Qué nodos deben dejar de elegir al azar para favorecer centro?
:::

::: hint {#jue-c3-cmp-pista-mas-sims-1 of="jue-c3-cmp-ej-mas-sims" title="A dónde se acerca cada promedio"}
Compara $0,-1/4,1/3$. Después cambia quién decide en C1 y C2, o en I y D.
:::

::: answer {#jue-c3-cmp-resp-mas-sims of="jue-c3-cmp-ej-mas-sims"}
**Entregaría der**, cuyo $Q_{\text{azar}}=1/3$ es el mayor. El problema persiste cuando desaparece el ruido.

- **MAX decide en C1 y C2.** Centro sube a $1/2$ y supera el $1/3$ de der.
- **MIN decide en I y D.** Izq y der bajan a $-1$, por debajo del $-1/4$ de centro.
- **Un solo nodo no basta.** Si únicamente MIN decide en D, der baja, pero izq conserva $0$ y supera a centro.
:::

**La pregunta cambia:** podemos usar el azar para descubrir continuaciones y mantener las elecciones de MAX y MIN al valorar lo descubierto.

---

## 4 · Ficha B: Monte Carlo con actualización minimax

**Piensa: ¿puedes conservar las mismas partidas al azar y valorar sus respuestas como lo harían MAX y MIN?**

Sí: guarda los estados descubiertos y sube máximos y mínimos. Kocsis y Szepesvári (2006) llaman a esta variante MMMC, *Monte-Carlo planning with minimax value update*.

### El mapa

- **Qué rastrea.** Guarda $\widehat Q(s,a)$ por jugada visitada y $\widehat V(s)$ por estado descubierto; estima $Q$ y $V$.
- **Dónde lo guarda.** Construye un árbol de búsqueda desde $s_{\text{raíz}}$, incorporando los estados recorridos.
- **Cómo sube.** Copia el valor del hijo y combina con máximo en MAX o mínimo en MIN.
- **A qué converge.** Converge casi seguramente a $V$ bajo el contrato de sus supuestos, que exige un árbol finito y determinista.

::: figure {#jue-c3-fig-flujo-mmmc title="Monte Carlo con actualización minimax, en palabras"}
![Simula uniformemente desde la raíz hasta un final. Guarda los estados descubiertos, asigna U al final y sube máximos y mínimos entre jugadas visitadas. Al terminar, entrega la mayor Q̂ disponible.](../_assets/jue-rx-flujo-mmmc.svg)
:::

::: definition {#jue-c3-actualizacion-minimax title="Monte Carlo con actualización minimax"}
**Qué es.** Muestrea partidas uniformemente, conserva lo descubierto y aplica minimax sobre las continuaciones visitadas.

**Cómo se calcula.** En un final $z$, $\widehat V(z)=U(z)$. Una jugada visitada copia $\widehat Q(s,a)=\widehat V(T(s,a))$; cada padre toma máximo o mínimo según su turno.

**Qué significa.** El azar decide qué se descubre. El respaldo representa las elecciones de los jugadores sobre la parte conocida.

**Qué no es.** No promedia el $U$ crudo por jugada. Esos promedios seguirían estimando $Q_{\text{azar}}$, aunque después eligieras el mayor.
:::

### Exploración: la regla

Cada repetición realiza estos pasos:

1. **Simula uniformemente.** Desde la raíz, ambos jugadores eligen entre todas sus jugadas legales hasta alcanzar un final real $z$.
2. **Conserva lo descubierto.** Agrega los estados nuevos del camino sin borrar los anteriores.
3. **Respalda desde el final.** Asigna $\widehat V(z)=U(z)$ y recalcula los antecesores hasta la raíz mediante respaldo minimax (*minimax backup*).

$$
\mathbf{\widehat Q(s,a)=\widehat V(T(s,a))}
\quad\text{para cada jugada visitada.}
$$

| Quién mueve | Regla de respaldo |
|---|---|
| MAX | $\mathbf{\widehat V(s)=\max_{a\text{ visitada}}\widehat Q(s,a)}$ |
| MIN | $\mathbf{\widehat V(s)=\min_{a\text{ visitada}}\widehat Q(s,a)}$ |

- **El invariante conserva la perspectiva.** Todo número mide el pago de MAX; el signo nunca cambia al subir.
- **Lo desconocido sigue desconocido.** Una jugada no visitada se marca «?», nunca 0; si ninguna se conoce, también $\widehat V$ es desconocido.
- **El respaldo suele ser provisional.** Faltan alternativas que podrían cambiarlo; una prueba de resolución permite declararlo exacto antes de descubrirlas todas.

**Ejemplo mínimo:** MIN tiene tres jugadas y los pagos posibles están entre $-1$ y $+1$.

- **Primer caso.** Visita un final $+1$: $\widehat V=+1$ es provisional. Las otras dos jugadas podrían ofrecer menos.
- **Segundo caso.** Descubre un final $-1$: $\widehat V=\min(+1,-1)=-1$ ya es exacto. Ninguna respuesta desconocida puede bajarlo.

Si las desconocidas valieran 0, el primer caso devolvería $\widehat V=0$: un número que ninguna visita aportó.

---

### El recorrido: una refutación tardía

**Piensa: después de 29 partidas favorables aparece una respuesta que derrota a MAX. ¿Cuánto cambia la jugada?**

El respaldo incorpora esa respuesta de inmediato. Un promedio solo añade otra observación.

> **Dado:** MAX elige A o B. A lleva a MIN, que elige p ($+10$), q ($+10$) o r. Tras r está x, donde MAX solo puede ir a un final $-30$.
>
> B termina con $-10$. Esta escala de pagos es propia del ejemplo.
>
> **Encontrar:** qué entrega cada método al descubrir r.

La decisión correcta es B:

$$
Q(A)=\min(10,10,-30)=-30,\qquad Q(B)=-10,\qquad V=-10.
$$

Monte Carlo plano acaba prefiriendo A:

$$
Q_{\text{azar}}(A)=\frac{10+10-30}{3}=-\frac{10}{3}>-10.
$$

Con presupuesto finito puede entregar B por azar. Su límite favorece A.

#### Tramo 1 · Las partidas favorables

La siguiente es una **secuencia impuesta de 31 simulaciones**, no una corrida aleatoria. Ambos operadores reciben exactamente los mismos caminos.

::: table {#jue-c3-tab-refutacion title="Secuencia impuesta: descubrir tarde la refutación"}
| Simulaciones | Camino y pago | Promedio de A | Minimax de A | Entregan |
|---|---|---:|---:|---|
| 1 | B: $-10$ | ? | ? | B · B |
| 2 a 30 | A: $+10$ | $10$ | $10$ | A · A |
| 31 | A, r, x: $-30$ | $26/3\approx8.67$ | $-30$ | A · B |
:::

Las 29 partidas favorables alternan p y q. La última hace que el promedio pase a $(29\cdot10-30)/30=26/3\approx8.67$.

**En la simulación 31**, el respaldo minimax salta a $-30$ y entrega B. El promedio conserva A; incluso su límite $-10/3$ seguirá por encima de B.

#### Tramo 2 · Subir la respuesta certera

::: table {#jue-c3-tab-propagacion title="Respaldo de la simulación 31"}
| Estado | Turno | Antes | Después | ¿Resuelto? |
|---|---|---|---|---|
| x | MAX | ? | $-30$ | Sí: única jugada final |
| Tras A | MIN | $10$ | $\min(10,10,-30)=-30$ | Sí: mínimo posible |
| Raíz | MAX | $10$: A | $\max(-30,-10)=-10$: B | Sí: ambos hijos exactos |
:::

- **El final fija su arista.** La jugada que llega directamente a él tiene $\widehat Q=U$ desde la primera visita.
- **El antecesor requiere una prueba.** Antes de la simulación 31, A parecía valer $10$ porque faltaba la respuesta r.

#### Tramo 3 · Comparar una corrida real

Con semilla 0 y 60 simulaciones, la primera visita a r ocurre en la novena. Aquí la raíz también se muestrea uniformemente; no se fija $k$ por jugada.

- **La actualización minimax cambia a B.** En la novena, A pasa de $10$ a $-30$; entrega B hasta la simulación 60.
- **El promedio empata en la novena.** A recibió $+10$ y $-30$, por lo que vale $-10$; el desempate con B favorece A.
- **El promedio termina prefiriendo A.** Tras 60 simulaciones, A recibió 29 y su media es $-150/29\approx-5.17$.

::: figure {#jue-c3-fig-refutacion title="La refutación descubierta tarde: promedio, actualización minimax y UCT"}
![Tres paneles con los mismos ejes sobre el árbol de la refutación (A con +10, +10 y −30; B con −10). Primero, el promedio de la secuencia impuesta: Q̂(A) se queda en 10 y baja a 8.67 tras el −30, con su límite −10/3 marcado arriba de B. Segundo, la actualización minimax: Q̂(A) salta de 10 a −30 y la jugada entregada cambia a B. Tercero, una corrida real de UCT con los pagos divididos entre 30, c = 1, semilla 0 y 60 vueltas: su promedio de A baja poco a poco desde la vuelta 5, queda debajo del de B en la vuelta 13 y llega a −20; B es la más visitada desde la vuelta 15](../_assets/jue-c3-refutacion-tres.svg)
:::

El panel de UCT usa pagos divididos entre 30, rango $[-1,1]$, $c=1$, semilla 0 y 60 vueltas. Descubre $-30$ en la vuelta 5; su promedio de A queda debajo del de B en la vuelta 13.

UCT cambia la selección de las continuaciones y sigue promediando. **Descubrir una refutación no convierte ese promedio en un mínimo.**

### El recorrido: el árbol de resultados

**Piensa: ¿qué entrega el respaldo minimax con partidas uniformes en el árbol de resultados?**

Centro desde la primera simulación de esta corrida. Su valor queda demostrado en la 12; la raíz completa queda resuelta en la 17.

> **Dado:** el árbol de resultados, semilla 0 y simulaciones uniformes desde la raíz.
>
> **Encontrar:** las estimaciones tras cada simulación y cuándo quedan resueltas.

Cada fila es una simulación. Las columnas izq, centro y der muestran $\widehat Q(R,a)$; «?» significa desconocida y ✓ significa exacta. En empate se entrega la primera jugada conocida.

#### Tramo 1 · Aparecen centro y der

| # | Final · $U$ | izq | centro | der | Entrega |
|---:|---|---:|---:|---:|---|
| 1 | c2a · $+1$ | ? | 1 | ? | centro |
| 2 | c2b · $-1$ | ? | 1 | ? | centro |
| 3 | c2b · $-1$ | ? | 1 | ? | centro |
| 4 | d1 · $-1$ | ? | 1 | $-1$ ✓ | centro |
| 5 | d1 · $-1$ | ? | 1 | $-1$ ✓ | centro |
| 6 | c1a · $0$ | ? | 0 | $-1$ ✓ | centro |

- **Fila 1.** C2 queda resuelto en $+1$, el máximo posible. C solo conoce ese hijo y conserva un $1$ provisional.
- **Fila 2.** $\max(1,-1)=1$: C2 no cambia. Un promedio sí habría bajado.
- **Fila 4.** D queda resuelto en $-1$: MIN encontró el mínimo posible sin visitar d2 ni d3.
- **Fila 6.** C1 recibe un $0$ provisional; C toma $\min(0,1)=0$.

#### Tramo 2 · Centro queda resuelto

| # | Final · $U$ | izq | centro | der | Entrega |
|---:|---|---:|---:|---:|---|
| 7 | d2 · $+1$ | ? | 0 | $-1$ ✓ | centro |
| 8 | d3 · $+1$ | ? | 0 | $-1$ ✓ | centro |
| 9 | d1 · $-1$ | ? | 0 | $-1$ ✓ | centro |
| 10 | c1a · $0$ | ? | 0 | $-1$ ✓ | centro |
| 11 | d2 · $+1$ | ? | 0 | $-1$ ✓ | centro |
| 12 | c1b · $-1$ | ? | 0 ✓ | $-1$ ✓ | centro |

- **Filas 7 y 8.** Los nuevos $+1$ no cambian el mínimo de D. Un promedio habría subido.
- **Fila 12.** C1 completa sus hijos: $\max(0,-1)=0$ es exacto. Como C2 ya estaba resuelto, C también queda resuelto.

#### Tramo 3 · La raíz queda resuelta

| # | Final · $U$ | izq | centro | der | Entrega |
|---:|---|---:|---:|---:|---|
| 13 | c2a · $+1$ | ? | 0 ✓ | $-1$ ✓ | centro |
| 14 | d2 · $+1$ | ? | 0 ✓ | $-1$ ✓ | centro |
| 15 | c2a · $+1$ | ? | 0 ✓ | $-1$ ✓ | centro |
| 16 | d1 · $-1$ | ? | 0 ✓ | $-1$ ✓ | centro |
| 17 | ix · $-1$ | $-1$ ✓ | 0 ✓ | $-1$ ✓ | centro |

- **Filas 13 a 16.** Nada cambia: el muestreo uniforme sigue entrando en ramas resueltas.
- **Fila 17.** Ix resuelve I en $-1$; las tres jugadas ya son exactas y $\widehat V(R)=0=V(R)$.

El resultado es $\widehat Q=(-1,0,-1)=Q$. No hizo falta visitar i1; el árbol completo aparece hasta la simulación 23.

Con las mismas 17 partidas, Monte Carlo plano obtiene $(-1,0,0)$ y entrega centro por desempate. Sus límites $(0,-1/4,1/3)$ favorecen der; coincidir ahora no significa converger al mismo objetivo.

La figura congela la corrida tras la fila 10: izq desconocida y centro todavía provisional.

::: figure {#jue-c3-fig-mmmc-arbol title="Actualización minimax en el árbol de resultados tras 10 simulaciones (semilla 0)"}
![El árbol de resultados tras las 10 primeras simulaciones de la traza: guarda 11 estados. D vale −1 y está resuelto; C vale 0 y C1 vale 0, los dos provisionales; C2 vale +1, resuelto. I, i1, ix y c1b no se han visitado: su Q̂ es desconocida, con «?». En la raíz, izq ?, centro 0 y der −1: entrega centro](../_assets/jue-rx-mmmc.svg)
:::

---

### Elección: qué jugada juega

MAX entrega la jugada con mayor $\widehat Q$ disponible en la raíz.

::: table {#jue-c3-tab-eleccion-mc title="Explorar y jugar con actualización minimax"}
| Decisión | Regla | Usa resultados |
|---|---|---|
| Explorar | Muestrea jugadas uniformemente | No |
| Jugar | Elige la mayor $\widehat Q$ conocida | Sí |
:::

- **Un empate conserva el orden.** Entrega la primera jugada que alcanza el mejor valor.
- **Sin muestras hay una salida definida.** Entrega la primera jugada legal.
- **Una desconocida no compite.** Por eso la primera fila entrega centro aunque izq y der sigan en «?».

### Propiedades y supuestos

- **Número que da.** Estima $Q$ y $V$ mediante respaldos del árbol descubierto; los valores resueltos son exactos.
- **Uso de EVAL.** No la utiliza: lee pagos terminales exactos en la escala de $U$.
- **Garantía.** Converge casi seguramente a $V$ si cumple todo el contrato siguiente. Con presupuesto finito, puede equivocarse.
- **Interrupción.** Siempre puede entregar la jugada definida por su regla, aunque todavía no tenga pruebas de su valor.
- **Tiempo.** Simular cuesta $O(m)$; revisar hasta $b$ hijos por estado del camino cuesta $O(bm)$. Con $n$ simulaciones, cuesta $O(nbm)$.
- **Memoria.** Cada simulación descubre a lo más $m+1$ estados; guarda $O(nm)$, sin superar el árbol completo.
- **Frente a minimax.** Descubre caminos al azar y conserva los estados, pero aplica el mismo respaldo. En el peor caso necesita descubrir todo; no realiza poda alfa-beta.
- **Presupuesto limitado.** En los experimentos de Kocsis y Szepesvári (2006), esta variante falló más que Monte Carlo plano, pese a su convergencia eventual.

**El contrato de convergencia** exige estas condiciones simultáneas:

1. **El árbol es finito.** El juego es determinista y tiene ramificación finita.
2. **Ninguna jugada queda oculta.** $A(s)$ enumera todas las legales; el muestreo uniforme mantiene positiva y fija la probabilidad de cada una.
3. **Las partidas terminan realmente.** Toda simulación llega a un final con pago exacto.
4. **Lo descubierto se conserva.** Los respaldos reutilizan los estados y sus valores.
5. **La frontera no queda sustituida por EVAL.** Un corte permanente cambiaría el problema resuelto.

Cada camino tiene probabilidad positiva de aparecer en cada simulación. En un árbol finito, casi seguramente se descubren todos; entonces el respaldo calcula minimax exacto.

- **Suma cero o constante.** Con dos jugadores, MIN minimiza el pago de MAX.
- **Suma no constante o más jugadores.** El respaldo se generaliza a $\max^n$: quien mueve maximiza su componente y copia el vector elegido.
- **El desempate debe ser fijo.** En árboles finitos de información perfecta y por turnos, ese respaldo vectorial permite obtener un equilibrio, sin la garantía escalar de minimax.

### Casos borde

- **Una jugada termina directamente.** Su $\widehat Q=U$ es exacta desde la primera visita, incluso si el final ya estaba guardado.
- **Solo hay una jugada.** Se copia el valor del hijo, como en x; su exactitud depende de la del hijo.
- **Aparece una respuesta certera.** Se incorpora en ese mismo respaldo; solo cambia los antecesores cuyo máximo o mínimo resulte afectado.
- **Falta una jugada.** Se mantiene desconocida; introducir 0 puede elevar artificialmente un máximo o reducir un mínimo.
- **Hay varios óptimos.** $\widehat V$ puede converger aunque existan empates; el orden fija la jugada entregada.
- **Los finales tienen distinta profundidad.** El algoritmo no prefiere ganar pronto, salvo que $U$ lo indique; sí cambia el costo del recorrido.
- **Se impone una frontera con EVAL.** El límite es el minimax truncado. En la escala normalizada del corte, un final se revisa primero y aporta $100\cdot U$.
- **Hay ciclos.** Hace falta una regla de terminación que produzca un árbol finito. Sin ella, no se afirma convergencia.

#### Cuándo queda resuelto un nodo

**Piensa: ¿un $-1$ basta para dejar de buscar?**

En un nodo de MIN, sí, si es un valor demostrado y $-1$ es el menor pago posible. Para MAX, la condición equivalente usa $+1$.

- **Todos los hijos son exactos.** Su máximo o mínimo también lo es.
- **Un hijo exacto alcanza el extremo favorable.** Ya determina el valor del padre, aunque falten otras jugadas.
- **Un promedio extremo no demuestra nada.** La frecuencia observada no descarta respuestas todavía desconocidas.

La implementación mantiene estas marcas, pero sigue muestreando hasta completar el presupuesto. Reconocer un nodo resuelto permite detener su búsqueda; no significa que toda corrida lo haga automáticamente.

La profundización iterativa puede detenerse con una victoria demostrada de 100. Alfa-beta puede hacer la poda correspondiente con ventana $(-1,+1)$ en la escala de $U$.

MCTS-Solver, de Winands, Björnsson y Saito (2008), incorpora pruebas de valores resueltos a MCTS. La interpretación de un mínimo como interés del rival requiere suma cero o constante.

#### El máximo también puede engañar

::: remark {#jue-c3-sesgo-maximo title="El sesgo del máximo"}
**Qué ocurre.** El máximo de estimaciones insesgadas puede quedar sesgado hacia arriba; el mínimo, hacia abajo. Elegir la muestra más favorable selecciona también su suerte.

**Ejemplo mínimo.** Dos jugadas tienen media 0. Cada una produce independientemente una muestra $+1$ o $-1$, con igual probabilidad.

Entre los cuatro pares posibles, el máximo vale $-1$ una vez y $+1$ tres veces:

$$
E[\max]=\frac{-1+1+1+1}{4}=\frac12,
\qquad E[\min]=-\frac12.
$$

**Qué significa.** El máximo verdadero de las medias es 0, pero el máximo observado tiene esperanza $1/2$. Esto importa al respaldar promedios ruidosos.

**Qué no ocurre en un final determinista.** Su pago exacto no tiene ese ruido. En nuestra variante, el riesgo provisional viene de las continuaciones todavía desconocidas.
:::

---

### Intuición: una respuesta no es un voto

- **El promedio cuenta frecuencias.** Una refutación pesa como una observación entre todas las anteriores.
- **Minimax representa decisiones.** MIN puede elegir la refutación cada vez, aunque el muestreo apenas la haya descubierto.
- **Un salto puede ser informativo.** Una hoja nueva puede cambiar varios respaldos de inmediato; antes del salto, sus valores eran provisionales.

### Ejercicios: reconocer pruebas y respaldar

::: exercise {#jue-c3-cmp-ej-puede-salir title="Señala dónde se puede dejar de buscar"}
En cada caso, decide si pueden omitirse las demás alternativas y explica por qué.

1. **Monte Carlo plano.** Una jugada de la raíz lleva 3 simulaciones ganadas y $\widehat Q=+1$.
2. **Minimax con corte.** Un hijo devuelve 36, la mayor $\mathrm{EVAL}$ de la posición de la clase.
3. **Alfa-beta sin corte.** Un hijo de la raíz de MAX devuelve $+1$, en un juego con pagos entre $-1$ y $+1$.
4. **D como dado.** En el árbol de resultados, el primer resultado examinado de D es $\text{d1}=-1$.
:::

::: hint {#jue-c3-cmp-pista-puede-salir-1 of="jue-c3-cmp-ej-puede-salir" title="Dos preguntas por caso"}
¿El número acredita el mejor pago posible para quien decide? ¿Proviene de un respaldo exacto, una cota suficiente, una evaluación o un promedio?
:::

::: answer {#jue-c3-cmp-resp-puede-salir of="jue-c3-cmp-ej-puede-salir"}
1. **No.** Tres victorias no descartan una respuesta que refute la jugada.
2. **No.** 36 es una estimación y está debajo del pago terminal ganador de 100.
3. **Sí.** Si $+1>\alpha$, el retorno acredita el máximo posible: es exacto o una cota inferior suficiente. Si $\alpha$ ya era $+1$, una jugada previa ya acreditaba la victoria.
4. **No.** D no elige el resultado favorable: promedia sus tres resultados. Falta conocer los demás pagos.
:::

::: exercise {#jue-c3-ej-mmmc title="Llena las dos estimaciones con las mismas partidas"}
Cuatro simulaciones del árbol de resultados terminan en d2 ($+1$), c1a ($0$), d1 ($-1$) y d3 ($+1$), en ese orden.

1. **Traza los respaldos.** Escribe $\widehat Q$ para izq, centro y der después de cada simulación; usa «?» para lo desconocido.
2. **Decide y certifica.** ¿Qué entrega tras la cuarta y qué números son exactos?
3. **Cambia el operador.** ¿Qué entrega Monte Carlo plano con las mismas partidas?
:::

::: hint {#jue-c3-pista-mmmc-1 of="jue-c3-ej-mmmc" title="Quién mueve en D"}
D pertenece a MIN. Compara lo que sabe tras d2 con lo que sabe al aparecer d1; después calcula el promedio de esos pagos.
:::

::: answer {#jue-c3-resp-mmmc of="jue-c3-ej-mmmc"}
| # | Final | izq | centro | der |
|---:|---|---:|---:|---:|
| 1 | d2 | ? | ? | 1 |
| 2 | c1a | ? | 0 | 1 |
| 3 | d1 | ? | 0 | $-1$ ✓ |
| 4 | d3 | ? | 0 | $-1$ ✓ |

1. **La traza está arriba.** D cambia al descubrir d1; d3 ya no puede modificar su mínimo.
2. **Entrega centro.** Solo der es exacta; centro sigue provisional porque faltan c1b y C2.
3. **El promedio entrega der.** $(1-1+1)/3=1/3$ supera el $0$ de centro. Tras la tercera simulación empataban en 0 y entregaba centro por orden.
:::

---

## 5 · Converge a lo que simulas

**Piensa: si todos usan pagos terminales, ¿por qué sus límites pueden diferir?**

Porque importan tanto las continuaciones que seleccionan como la forma de actualizar sus valores.

::: table {#jue-c3-tab-que-guarda-mc title="Converge a lo que simulas"}
| Algoritmo | Qué guarda | Cómo sube | Límite |
|---|---|---|---|
| Monte Carlo plano | $N$ y suma en la raíz | No respalda entre estados | $Q_{\text{azar}}$ |
| Actualización minimax | $\widehat Q$ y $\widehat V$ | Máximo y mínimo | $Q$ y $V$, bajo su contrato |
| UCT | $N(s,a),\widehat Q(s,a),N(s)$ | Promedia el mismo $U$ | $Q$ y $V$, bajo condiciones |
:::

**El promedio al azar sí converge, pero al valor de jugar al azar.** La actualización minimax converge a $V$ bajo su contrato, aunque puede requerir descubrir todo el árbol.

UCT pertenece a MCTS, la búsqueda en árbol de Monte Carlo. Construye su árbol con **vueltas**, guarda visitas y promedios por arista y promedia el mismo $U$, sin máximos ni mínimos: lo que cambia es que reparte las vueltas hacia lo que va mejor.

En el árbol de resultados, con $c=1$ y semilla 0, centro tiene $N=26$ y $\widehat Q=0$ tras 40 vueltas. Coincide con $Q=0$ por casualidad: en la vuelta 100, su promedio es $1/83$.

::: figure {#jue-c3-fig-tres-mc title="Los tres Monte Carlo en el árbol de resultados"}
![Los tres Monte Carlo en el árbol de resultados, por jugada de la raíz izq, centro y der. Exactos: Q = −1, 0, −1 y Q_azar = 0, −1/4, 1/3. Con 40 simulaciones o vueltas y semilla 0: Monte Carlo plano da +0.75, 0 y +0.22 y entrega izq; la actualización minimax, con las mismas partidas, da −1, 0, −1 y entrega centro; UCT con c = 1 da −0.6, 0 y −0.33 y entrega centro, la más visitada. Con más simulaciones, el plano iría a der](../_assets/jue-c3-tres-mc.svg)
:::

**Punto de control:** calcula ambos respaldos para una lista de simulaciones. Distingue valores desconocidos, provisionales y exactos; explica qué entrega cada método y a qué número converge.

> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | Alfa-beta | $V$ en la raíz; lo garantiza |
> | Minimax con corte | Valor con corte; no garantiza $V$, salvo si llega a los finales |
> | Búsqueda de quietud | Valor con quietud; no garantiza $V$, salvo si llega a los finales antes de cortar |
> | Profundización iterativa | Valor con corte de la última búsqueda; no garantiza $V$, salvo si llega a los finales |
> | **Monte Carlo plano (estás aquí)** | **$\bar u$; no garantiza $V$** |
> | **MCTS con UCT (estás aquí)** | **$\bar u$; no garantiza $V$ (con tiempo sin límite converge a él, con cualquier $c>0$)** |
>
> **Lo que viene.**
>
> Ya viste todos los algoritmos de la clase. [[un-arbol-todos-los-algoritmos|Radiografía: un árbol, cinco algoritmos]] los pone lado a lado.

## Lo que hay que llevarse

- **Monte Carlo plano** estima cada jugada de la raíz con el promedio de
  simulaciones al azar hasta el final. No necesita $\mathrm{EVAL}$: solo
  las reglas.
- **Ese promedio converge a $Q_{\text{azar}}$**, expectiminimax con los dos
  como dados, no a $Q$. En la posición de la clase acierta
  ($\text{d2}\textbf{-}\text{d3}$, ${8/9}$, 17 de cada 18 partidas); en
  hexapawn, $\text{b1}\textbf{-}\text{b2}$ da ${5/24}$ aunque vale ${-1}$.
- **Más simulaciones no arreglan una refutación.** En el árbol de
  resultados entrega der (${1/3}$; 960 de 1000 corridas con 50
  simulaciones), que vale ${-1}$. En la refutación, el promedio pasa de 10 a
  8.67, y su límite, ${-10/3}$, sigue arriba de ${-10}$.
- **La actualización minimax** usa las mismas partidas, guarda lo
  descubierto y sube: ${\widehat V(z)=U(z)}$, ${\widehat Q(s,a)=\widehat V(T(s,a))}$,
  máximo en MAX y mínimo en MIN. Las jugadas no visitadas son desconocidas,
  nunca cero. La refutación la lleva a ${-30}$ en el mismo respaldo.
- **Converge a $V$** en un árbol finito, determinista y de ramificación
  finita, con todas las jugadas posibles, finales reales y lo descubierto
  guardado. En el árbol de resultados queda resuelta en 17 simulaciones;
  en el peor caso hay que descubrir todo el árbol.
- **Muestrear parejo es caro:** las dos reparten las simulaciones sin mirar
  lo que ya saben. ¿Y si se gastaran donde importa?

Continúa con [[monte-carlo-en-un-arbol-grande|MCTS con UCT]].

---

## 4 · Dar una vuelta de MCTS

**Piensa: si tienes tiempo para 1000 simulaciones y tres jugadas, ¿las
repartirías por igual?**

No conviene: simular solo desde la raíz reparte igual las partidas entre
jugadas buenas y malas. MCTS **construye un árbol poco a poco** y manda más
simulaciones a las jugadas que van mejor.

Cada nodo $s'$ del árbol guarda dos números. $N(s')$ cuenta las
simulaciones que pasaron por él; aquí $N$ no es Negras. $G(s')$ cuenta en
cuántas de ellas ganó MAX, sea quien sea el que mueve en $s'$; aquí $G$ no
es el grafo de la clase 1.

De esos dos números sale el promedio de $U$. En este juego no hay
empates: cada simulación la gana MAX, con ${U=+1}$, o la gana MIN, con
${U=-1}$. De las $N(s')$ partidas, MAX ganó $G(s')$ y MIN las otras
${N(s')-G(s')}$. La suma de las $U$ es victorias menos derrotas: la misma
cuenta que el ${7\cdot(+1)+3\cdot(-1)}$ de la sección 1. Entre $N(s')$, da
el promedio:

$$\begin{aligned}
\bar u(s')&=\frac{G(s')-\bigl(N(s')-G(s')\bigr)}{N(s')}\\
&=\frac{2G(s')-N(s')}{N(s')}=2\,\frac{G(s')}{N(s')}-1.
\end{aligned}$$

En palabras: ${G/N}$ es la fracción de partidas que ganó MAX, y $\bar u$
la pasa a la escala de $U$. Es la relación ${p=(\bar u+1)/2}$ de la
sección 2, despejada, con $p$ medida en vez de calculada. $\bar u$ se mide
**siempre desde MAX**, también donde mueve MIN. En la raíz de la figura de
abajo, ${G/N=2/4}$: MAX ganó la mitad, y ${\bar u=2\cdot\tfrac24-1=0}$.

Cada vuelta tiene cuatro pasos:

1. **Selección.** Desde la raíz, baja por el árbol ya construido y para en
   el **primer nodo al que le falta algún hijo**: una jugada que todavía no
   está en el árbol. Por ahora, MAX baja al hijo de mayor $\bar u$ y MIN al
   de menor; la sección 5 cambia esta regla.
2. **Expansión.** Agrega al árbol un hijo nuevo bajo el nodo donde paró la
   selección: $T(s,a)$, con $s$ ese nodo y $a$ la primera de las jugadas
   que faltaban, en un orden fijo.
3. **Simulación.** Desde el hijo nuevo, juega una partida al azar hasta un
   final y anota su $U$. Es la primera simulación del hijo: cada nodo nace
   con la suya.
4. **Retropropagación.** Sube por el camino recorrido hasta la raíz. Cada
   nodo del camino, incluido el nuevo, suma 1 a sus simulaciones y, si
   ganó MAX, 1 a sus victorias. Eso vale también en los nodos de MIN.

Si la selección llega a un final, no hay nada que expandir ni simular: su
$U$ es el resultado de la vuelta, y cuenta como una simulación más.

Así, cada vuelta aporta un resultado, y decimos que esa simulación «pasó
por» cada nodo del camino. Pero solo el tramo debajo del hijo nuevo se
jugó al azar: arriba, el camino lo eligió la selección.

En la figura, cada caja dice ${G/N}$. La raíz y el ${2/3}$ ya tienen todas
sus jugadas en el árbol, dos cada uno, así que la selección pasa por ellos.
El ${0/1}$ al que baja MIN no tiene ningún hijo todavía: ahí para, y bajo
él nace el ${0/0}$.

Las cuentas salen de cómo nace cada nodo. La raíz es el estado de partida:
no nació en una expansión y no simula. Sus cuentas suman las de sus hijos,
${2/4=2/3+0/1}$. Cada otro nodo suma la suya y las de sus hijos: el
${2/3}$ es su simulación, que ganó MAX (${1/1}$), más ${1/1}$ y ${0/1}$.
Ahí mueve MIN, y su 2 cuenta igual victorias de MAX.

::: figure {#jue-c3-fig-mcts title="Una vuelta de MCTS: la raíz pasa de 2/4 a 3/5"}
![Cuatro paneles con el mismo árbol; cada caja dice G/N, victorias de MAX entre simulaciones que pasaron por ella. 1, selección: desde la raíz, 2/4, donde mueve MAX, se baja a 2/3; ahí mueve MIN y baja a 0/1, donde MAX ganó menos. 2, expansión: aparece un hijo nuevo, 0/0, bajo ese 0/1. 3, simulación: desde el hijo nuevo, una línea quebrada llega a un final con U = +1. 4, retropropagación: cada nodo del camino suma una simulación y una victoria; 2/4 pasa a 3/5, 2/3 a 3/4, 0/1 a 1/2 y 0/0 a 1/1. Los nodos fuera del camino, 1/1 y el otro 0/1, no cambian](../_assets/jue-c3-mcts-pasos.svg)
:::

Las vueltas se repiten mientras haya tiempo. Al final, en esta versión, se
juega la jugada de la raíz **por la que pasaron más simulaciones**, no la de
mejor promedio. Un promedio de pocas partidas puede ir alto por suerte; el
de la más simulada es el que tiene más evidencia detrás.

Es la convención
más común, no la única: otras versiones entregan la de mayor promedio.
Como la profundización
iterativa de [[jugar-contra-el-reloj|Jugar contra el reloj]], siempre tiene
una jugada lista.

::: exercise {#jue-c3-ej-retro title="Completa la vuelta con una derrota"}
Repite la vuelta de la figura con el mismo camino y el mismo hijo nuevo,
pero la simulación termina en ${U=-1}$: gana MIN.

1. ¿Qué ${G/N}$ quedan en los cuatro nodos del camino, de la raíz al nuevo?
2. ¿Cambia algún nodo fuera del camino?
3. ¿Cuánto vale ahora $\bar u$ en la raíz?
:::

::: hint {#jue-c3-pista-retro-1 of="jue-c3-ej-retro" title="Qué cuenta cada número"}
De los dos números de cada caja, ¿cuál cuenta todas las partidas que
pasaron por ahí y cuál solo algunas?
:::

::: answer {#jue-c3-resp-retro of="jue-c3-ej-retro"}
1. La raíz pasa de ${2/4}$ a ${2/5}$; el ${2/3}$, a ${2/4}$; el ${0/1}$ del camino,
   a ${0/2}$; el nuevo, de ${0/0}$ a ${0/1}$. Todos suman una simulación y
   ninguna victoria: un ${U=-1}$ no resta, solo deja de sumar.
2. No: el ${1/1}$ y el otro ${0/1}$ no estaban en el camino.
3. ${\bar u=(2\cdot2-5)/5=-0.2}$. Antes de la vuelta valía $0$.
:::

La regla provisional de la selección tiene un hueco. En la figura, el
${0/1}$ que cuelga de la raíz lleva ${\bar u=-1}$ tras **una sola**
partida. Bajando siempre por el mayor $\bar u$, MAX no vuelve a él nunca:
el ${2/3}$ ya ganó dos, y su $\bar u$ no puede bajar a ${-1}$. Una mala
suerte en su primera simulación lo condena. ¿Cómo darle otra oportunidad
sin repartir las vueltas a ciegas?

## 5 · Explorar o aprovechar

**Piensa: ¿conviene seguir probando la jugada que va mejor, o darle otra
oportunidad a una que casi no se ha probado?**

Las dos cosas. **Aprovechar** es elegir lo que ya funcionó; **explorar** es
probar lo poco probado, por si es mejor. La regla más usada se llama
**UCT** (del inglés *upper confidence bounds applied to trees*). Le suma a
cada promedio un bono que crece si la jugada se ha probado poco:

$$\text{puntaje}(s')=\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

- $s$ es el nodo donde se elige y $s'$, uno de sus hijos. Aquí $s$ ya no es
  solo la raíz del problema: es cualquier nodo por el que baja la selección.
- $\bar u(s')$ es el de la sección 4: el promedio de $U$ de las simulaciones
  que pasaron por $s'$, siempre desde MAX.
- $N(s)$ y $N(s')$ cuentan las simulaciones que pasaron por cada nodo.
- $\ln$ es el logaritmo natural; aquí solo importa que crece muy despacio.
- $c$ es un número positivo que elegimos: más grande, más exploración. En
  esta página, ${c=1}$.

Así escrito es el puntaje de MAX, que quiere $\bar u$ alto. MIN lo quiere
bajo, así que en un nodo de MIN el primer término es $-\bar u(s')$:

$$\text{puntaje}(s')=-\bar u(s')+c\sqrt{\frac{\ln N(s)}{N(s')}}.$$

Elegir el mayor de estos es elegir el hijo de ${\bar u-\text{bono}}$ más
bajo. El bono suma en los dos casos: explorar no tiene lado.

El primer término aprovecha; el segundo explora y se encoge con muchas
simulaciones. Un hijo con ${N(s')=0}$ tendría bono infinito, pero en el
árbol no los hay: cada nodo nace con su simulación. ${N=0}$ es una jugada
aún no expandida. Por eso la selección para en el primer nodo al que le
falta un hijo: ese hijo ganaría a cualquiera.

En la figura, MIN elige en el ${2/3}$, con ${N(s)=3}$, entre el ${1/1}$
(${\bar u=+1}$) y el ${0/1}$ (${\bar u=-1}$). Los dos llevan una
simulación, así que su bono es el mismo, ${\sqrt{\ln 3}\approx1.05}$. Sus
puntajes son ${-1+1.05=0.05}$ y ${+1+1.05=2.05}$: MIN baja al ${0/1}$.

Así corrige MCTS el defecto de la sección 2, el **rival al azar**. Donde ya
construyó árbol, MIN elige por puntaje, no al azar: lo que parece mejor para
él, más un bono para lo poco probado. Con suficientes vueltas se concentra
en su mejor respuesta. Solo la simulación, debajo del árbol, sigue jugando
al azar.

**La idea del bono viene del bandido:** elegir una y otra vez entre
jugadas que pagan al azar, sin árbol debajo. Ahí el bono es un margen de
error del promedio: cuánto podría errar una jugada con pocas partidas, del
lado que le importa a quien elige (abajo para MAX, arriba para MIN).

Por eso se encoge al crecer $N(s')$. Crece despacio con ${\ln N(s)}$: conforme
avanza la búsqueda, se pide más confianza antes de dar una jugada por mala.
Y $c$ fija cuánta.

[[de-donde-sale-el-bono|De dónde sale el bono]] dice de dónde sale $c$. En corto: si $N(s')$ se
fijara antes de ver los resultados, $\delta$ acotaría la probabilidad de
que el promedio quedara por debajo de su promedio límite en más que el
bono. Esa $\delta$ baja conforme crece $N(s)$, y $c$ fija qué tan rápido.
Nuestra ${c=1}$ pide ${\delta=1/\sqrt{N(s)}}$: 10 % con ${N(s)=100}$.

En la regla UCB, $N(s')$ depende de lo que salió: $\delta$ guía la
elección de $c$, pero no es una probabilidad garantizada. En UCT, además,
el blanco cambia: lo que se juega debajo de cada nodo va cambiando, y el
promedio no tiene un blanco fijo.

Muchos textos usan la fracción de victorias ${G/N}$ en vez de $\bar u$.
Como ${\bar u=2\,G/N-1}$, el puntaje es

$$\begin{aligned}
&\bar u+c\sqrt{\ln N(s)/N(s')}\\
&\quad=2\,\bigl(G/N+\tfrac c2\sqrt{\ln N(s)/N(s')}\bigr)-1.
\end{aligned}$$

Usar ${G/N}$ con la misma $c$ equivale a duplicar $c$: la ${c=\sqrt2}$ de
esos textos, con ${G/N}$, es ${c=2\sqrt2}$ con $\bar u$.

::: exercise {#jue-c3-ej-mcts title="Calcula qué se explora y qué se entrega"}
Tras 100 vueltas, las tres jugadas de la raíz, donde mueve MAX, tienen:

- **x:** ${N=60}$ simulaciones, promedio ${\bar u=0.5}$;
- **y:** ${N=30}$ simulaciones, promedio ${\bar u=0.6}$;
- **z:** ${N=10}$ simulaciones, promedio ${\bar u=0.2}$.

1. Si el tiempo se acaba ahora, ¿qué jugada se entrega?
2. Si queda tiempo para una vuelta más, calcula el puntaje de cada una con
   ${c=1}$ y ${\ln 100\approx4.61}$. ¿Por cuál baja la selección?
3. ¿Coinciden las dos respuestas? Explica por qué no hay contradicción.
:::

::: hint {#jue-c3-pista-mcts-1 of="jue-c3-ej-mcts" title="Cuándo se usa cada regla"}
¿Qué regla se aplica cuando el tiempo ya se acabó, y cuál mientras todavía
quedan vueltas? ¿Qué número de la lista mira cada una?
:::

::: answer {#jue-c3-resp-mcts of="jue-c3-ej-mcts"}
1. **x:** al final se entrega la jugada con más simulaciones, y x tiene 60.
2. Los puntajes son

   $$\begin{aligned}
   x&:\ 0.5+\sqrt{4.61/60}\\
   &\approx0.5+0.28=0.78,\\[4pt]
   y&:\ 0.6+\sqrt{4.61/30}\\
   &\approx0.6+0.39=0.99,\\[4pt]
   z&:\ 0.2+\sqrt{4.61/10}\\
   &\approx0.2+0.68=0.88.
   \end{aligned}$$

   La selección baja por **y**. La z recibe el bono más grande, pero su
   promedio bajo la deja segunda.
3. **No coinciden, y está bien.** Entregar busca la jugada más confiable:
   60 partidas pesan más que 30. Seleccionar decide dónde gastar la vuelta
   que sigue, y y todavía tiene poca evidencia para lo bien que va. Con
   ${G/N}$ o con ${c=\sqrt2}$ la selección iría a z: las dos le dan más
   peso al bono que nuestra ${c=1}$ (con ${G/N}$ es como usar ${c=2}$), y el
   bono favorece a z.
:::

Queda abierta la pregunta que esta sección pasó de largo: **¿de dónde sale
ese bono, y cuánto debe valer $c$?** La contesta
[[de-donde-sale-el-bono|De dónde sale el bono]].

## 6 · Ubicar MCTS en la historia

**Piensa: Deep Blue y AlphaGo ganaron con búsqueda. ¿Qué pieza cambió de
uno a otro?**

La que estima lo que no se alcanza a calcular:

- **Deep Blue venció a Kasparov en 1997.** Buscaba con alfa-beta y una
  función de evaluación compleja, ajustada en su mayoría a mano: cortar y
  evaluar.
- **Desde 2006**, cuando Rémi Coulom le dio nombre al método, los programas
  de Go más fuertes usan MCTS: simular en vez de evaluar.
- **En marzo de 2016, AlphaGo**, de DeepMind, venció 4 a 1 a Lee Sedol, uno
  de los mejores jugadores de Go del mundo. Combinaba MCTS con **redes
  neuronales**: una sugería qué jugadas explorar y otra estimaba cuánto
  valía una posición. Al valorar un nodo nuevo, AlphaGo mezclaba esa
  estimación, mitad y mitad (${\lambda=0.5}$), con el resultado de una
  simulación rápida guiada por una política rápida y sencilla.
- **AlphaGo Zero y AlphaZero, en 2017, quitaron las partidas simuladas
  hasta el final** (en inglés, *rollouts*): una red que aprende jugando
  contra sí misma sugiere jugadas y valora posiciones.

¿Sigue siendo MCTS sin esas partidas? Sí: sigue dando vueltas de MCTS, con
el árbol, las cuentas y la selección por puntaje. Lo que más cambia es el
paso 3: la red valora el hijo nuevo, sin jugar desde él una partida al
azar. También guía la selección y la expansión:
su puntaje no es el UCT, porque suma un término que premia la jugada que la
red sugiere.

**Punto de control:** deberías poder dar una vuelta de MCTS a mano, con
${G/N}$ en cada nodo y cualquier resultado. También, calcular el puntaje UCT
de un hijo y decir por qué un promedio de simulaciones no es $V$.

