---
id: tarea-mirar-todo-y-podar
title: "Tarea de refuerzo · Calcular y podar"
nav_title: Tarea
summary: "Dos ejercicios para practicar sin ayuda: modelar y resolver monedas en fila, comparar juego perfecto y azar, y resolver n1 de hexapawn cuando quedarse sin jugada es empate."
status: ready
estimated_time: 45m
tags: [juegos, minimax, alfa-beta, practica]
---

# Tarea de refuerzo · Calcular y podar

**¿Puedes escribir un juego, calcular cuánto asegura MAX y elegir su jugada?**

Esta tarea no se entrega. Sirve para comprobar que puedes hacerlo **sin ayuda** y explicar qué permite podar con alfa-beta.

- **El primer ejercicio presenta monedas en fila.** El pago cuenta pesos en vez de victorias y derrotas.
- **El segundo cambia una regla de hexapawn.** Es la misma modificación de la [[tarea-leer-y-escribir|tarea de la clase 1]].

**Haz primero un esfuerzo propio, sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT. Después de intentarlo, abre las pistas una por una y vuelve a tu hoja antes de consultar la respuesta.**

---

## 1 · Resolver monedas en fila

> **Monedas en fila.** Hay cuatro monedas de **2, 1, 5 y 3 pesos**, en ese orden de izquierda a derecha. Dos jugadores se turnan; en cada turno, quien mueve toma una moneda de un extremo.
>
> Cuando no quedan monedas, cada quien conserva lo que tomó. **MAX empieza y mide el resultado en pesos:** lo que sumó MAX menos lo que sumó el rival.

::: exercise {#jue-tarea-2-ej-monedas title="Escribe y resuelve monedas en fila"}

1. **Escribe las siete piezas.** Define qué guarda un estado $(S)$, $s_0$, $S_F$, $\mathrm{Pl}$, $A$, $T$ y $U$; declara la escala de $U$.
2. **Escribe el problema.** Separa lo **dado** de lo que hay que **encontrar**.
3. **Cuenta el árbol completo.** ¿Cuántos nodos tiene y cuántos son finales?
4. **Resuelve con minimax.** Calcula $V(s_0)$, elige la primera moneda de MAX y di con cuántos pesos termina cada jugador bajo juego perfecto.
5. **Prueba la regla codiciosa.** Si MAX siempre toma la moneda mayor disponible y el rival juega perfecto, ¿cómo termina?
6. **Busca lo que se puede reutilizar.** ¿Cuántos subproblemas distintos hay si solo importa qué monedas quedan, qué valores comparten y por qué basta con eso?
7. **Considera la poda.** Si recorres el árbol con alfa-beta, ¿esperas ahorrar mucho y qué decide ese ahorro?
8. **Señala un límite del valor.** Di algo que el número calculado no te diga.
9. **Cambia al rival por un volado.** Toma la izquierda con probabilidad $p$ y la derecha con $1-p$; si queda una sola moneda, la toma. Calcula cuánto espera MAX con cada primera jugada para $p=\tfrac12$ y $p=\tfrac34$, elige en cada caso y compara con lo que asegura esa jugada ante un rival que juega perfecto.

:::

::: hint {#jue-tarea-2-pista-monedas-a of="jue-tarea-2-ej-monedas" title="Pista 1 · Qué guarda el estado"}

Las monedas restantes forman un tramo seguido de la fila original: puedes identificarlo con los índices de sus extremos. Pero el pago también depende de lo que ya tomó cada jugador: ¿qué número necesitas guardar para leer $U$ al final sin reconstruir la historia?

:::

::: hint {#jue-tarea-2-pista-monedas-b of="jue-tarea-2-ej-monedas" title="Pista 2 · Empieza por los tramos cortos"}

Para cada tramo, calcula la diferencia futura que asegura **quien mueve**. Con una moneda, la toma; con dos, compara los extremos; con tres, usa los valores de los tramos de dos que ya resolviste.

:::

::: hint {#jue-tarea-2-pista-monedas-c of="jue-tarea-2-ej-monedas" title="Pista 3 · El rival que tira un volado"}

Tras la primera jugada de MAX, solo el primer volado del rival tiene dos salidas: después MAX elige y la última moneda queda forzada. Sigue cada salida hasta el final y pondera su pago con la probabilidad correspondiente.

:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **El estado basta para calcular $U$.** Puedes leer el pago final sin reconstruir la historia.
- **El problema está completo.** Separaste «dado» y «encontrar».
- **Calculaste de corto a largo.** Resolviste los tramos cortos antes de usarlos en los largos.
- **Separaste valor y jugada.** Escribiste tanto el número como la moneda que lo alcanza.
- **Usaste el rival correcto.** Comparaste la regla codiciosa contra juego perfecto, no contra otro jugador codicioso.
- **Promediaste donde hay azar.** Ponderaste cada salida del volado por su probabilidad.

::: answer {#jue-tarea-2-resp-monedas of="jue-tarea-2-ej-monedas" title="Respuesta · Monedas en fila"}

**1 · Las siete piezas.**

Un estado guarda el tramo de la moneda $i$ a la $j$, el turno y $\Delta$: **los pesos acumulados por MAX menos los del rival**. Las monedas restantes no revelan esa diferencia; por eso también va en el estado.

| Pieza | En monedas en fila |
|---|---|
| $S$ | Estados alcanzables: $(i,j,\text{turno},\Delta)$ |
| $s_0$ | $(1,4,\text{MAX},0)$ |
| $S_F$ | Estados sin monedas |
| $\mathrm{Pl}(s)$ | Lee el turno: MAX o MIN |
| $A(s)$ | $\{$izquierda, derecha$\}$ |
| $T(s,a)$ | Retira, actualiza $\Delta$ y cambia el turno |
| $U(s)$ | $\Delta$ pesos, desde MAX |

Con una moneda hay **una sola jugada**; sin monedas, ninguna. Si la moneda tomada vale $x$, $T$ actualiza el extremo correspondiente y suma $x$ a $\Delta$ si movió MAX, o lo resta si movió MIN.

**Aquí $U$ copia un marcador en pesos; no vale $\pm1$.** Es la opción de contar puntos de [[escribir-el-juego|Escribir el juego]].

**2 · El problema.**

**Dado:** las siete piezas del juego.

**Encontrar:** en cada estado donde mueve MAX, la moneda que le asegura la mayor diferencia si MIN responde lo mejor que puede.

**3 · El árbol completo.**

Toda partida dura **4 jugadas**. Con dos o más monedas hay dos hijos; con una, solo uno. Por niveles:

$$
1+2+4+8+8=\mathbf{23\text{ nodos}}.
$$

Los **8 nodos del último nivel son finales**.

**4 · Minimax.**

Para reutilizar los tramos, define $W$ como la **diferencia futura que asegura quien mueve**, contando solo las monedas restantes. El tramo vacío vale $W=0$; en cualquier otro tramo se elige el mayor de estos números:

- **Tomar la izquierda da** $\text{izquierda}-W(\text{lo que queda})$.
- **Tomar la derecha da** $\text{derecha}-W(\text{lo que queda})$.

Esta recurrencia es la forma *negamax* de minimax: resta lo que el rival puede asegurar después. **$W$ cambia de perspectiva con el turno; $V$ siempre se mide desde MAX.** Se relacionan así:

$$
V(s)=
\begin{cases}
\Delta+W(\text{tramo}) & \text{si mueve MAX},\\
\Delta-W(\text{tramo}) & \text{si mueve MIN}.
\end{cases}
$$

**Con el tramo vacío, $W=0$ y $V(s)=U(s)=\Delta$.**

Con una sola moneda, $W(2)=2$, $W(1)=1$, $W(5)=5$ y $W(3)=3$. Los demás tramos quedan así:

| Tramo | Cuenta | $W$ |
|---|---|---:|
| $(2,1)$ | $\max\{2-1,\ 1-2\}$ | $1$ |
| $(1,5)$ | $\max\{1-5,\ 5-1\}$ | $4$ |
| $(5,3)$ | $\max\{5-3,\ 3-5\}$ | $2$ |
| $(2,1,5)$ | $\max\{2-4,\ 5-1\}$ | $4$ |
| $(1,5,3)$ | $\max\{1-2,\ 3-4\}$ | $-1$ |
| $(2,1,5,3)$ | $\max\{2-(-1),\ 3-4\}$ | **$3$** |

En $s_0$ mueve MAX y $\Delta=0$, así que **$V(s_0)=+3$**. Cada jugada vale lo que vale su hijo: $Q(s,a)=V(T(s,a))$.

| Primera jugada | $Q(s_0,a)$ |
|---|---:|
| Tomar el 2 | $+3$ |
| Tomar el 3 | $-1$ |

**MAX debe tomar el 2, la moneda menor.** Deja $(1,5,3)$ al rival; este tome el 1 o el 3, MAX toma después el 5. MAX termina con **7 pesos** y el rival con **4**.

**5 · La trampa codiciosa.**

Si MAX toma el 3, deja $(2,1,5)$ al rival, que toma el 5. Después MAX toma el 2 y el rival el 1: MAX suma **5**, el rival **6**, y el pago es **$-1$**.

**Tomar la mayor ahora le regaló al rival la moneda de 5.**

**6 · Los subproblemas que se reutilizan.**

Hay $4+3+2+1=10$ tramos con monedas, más el vacío: **11 subproblemas: uno por tramo**, frente a los 23 nodos del árbol.

- **Los 11 subproblemas no son los estados del modelo.** Dos estados con el mismo tramo y distinta $\Delta$ son distintos y pueden tener distinto $V$.
- **El valor reutilizado es $W$.** Depende del tramo; cada estado recupera su $V$ sumando o restando ese $W$ a su propia $\Delta$, según quién mueve.
- **Basta un nodo por tramo.** Se omiten $\Delta$ y el turno porque $W$ mide la diferencia futura desde quien mueve; la tabla anterior calcula esos valores.

**7 · El ahorro de alfa-beta.**

Se recorre el árbol sin reutilizar subproblemas, con ventana inicial $(-\infty,+\infty)$. El orden indicado se aplica en cada nodo:

| Primer extremo que revisa | Nodos generados |
|---|---:|
| Izquierda | **23** |
| Derecha | **21** |

Ahorra poco porque el árbol es chico y cada nodo tiene a lo más dos hijos: una poda solo puede saltarse el segundo. Con la izquierda primero, las condiciones de poda se cumplen solo cuando ya no queda hijo por revisar; con la derecha primero, se salta una rama de dos nodos.

**Alfa-beta nunca genera más que minimax, pero no siempre ahorra mucho:** lo deciden el orden y la forma del árbol.

**8 · Lo que el valor no dice.**

El $+3$ supone que el rival juega perfecto: es lo que MAX **asegura**, no lo que puede obtener contra un rival que se equivoca, que puede ser más.

- **Con la jugada minimax no hay más que ganar.** Tomar el 2 y después el 5 da exactamente $+3$ ante las dos respuestas del rival: 7 contra 4.
- **Para aprovechar un error hay que arriesgar.** Tomar el 3 da $+5$ si el rival toma el 2, pero $-1$ si responde bien.

**9 · El rival que tira un volado.**

Cambia el modelo: los turnos del rival pasan a ser nodos **AZAR**, con $\Pr(\text{izquierda}\mid s)=p$. MAX sigue eligiendo; donde actúa el volado se calcula la esperanza $E[U]$, en pesos desde MAX.

- **Tomar el 2 da $+3$ en ambas salidas.** Si el rival toma el 1, MAX toma el 5 y queda el 3; si toma el 3, MAX toma el 5 y queda el 1.
- **Tomar el 3 permite dos pagos.** Si el rival toma el 2, MAX toma el 5 y obtiene $+5$; si toma el 5, MAX toma el 2 y obtiene $-1$.

Por tanto:

$$
E[U\mid\text{tomar el }2]=3,
$$

$$
E[U\mid\text{tomar el }3]=5p-(1-p)=6p-1.
$$

| $p$ | Tomar 2 | Tomar 3 | MAX elige |
|---|---:|---:|---|
| $\tfrac12$ | $+3$ | $+2$ | El 2 |
| $\tfrac34$ | $+3$ | $+3.5$ | El 3 |

Con $p=\tfrac12$, MAX conserva la jugada que asegura $+3$. Con $p=\tfrac34$, prefiere el 3 por su esperanza, pero **esa jugada solo asegura $-1$ si el rival en realidad juega perfecto**.

**La esperanza depende del modelo del rival; la garantía adversarial considera su mejor respuesta.**

:::

---

## 2 · Resolver n1 cuando quedarse sin jugada es empate

Retoma la regla de la [[tarea-leer-y-escribir|tarea de la clase 1]]: todo sigue igual, salvo que **quedarse sin jugada produce un empate**, con pago 0.

> **Las reglas.** El tablero es de 3×3. Blancas (B, MAX) empieza abajo, en la fila 1; Negras (N, MIN), arriba, en la fila 3. Empiezan Blancas.
>
> Un peón avanza una casilla vacía o captura en diagonal hacia delante. Gana quien llega a la fila rival o captura todos los peones rivales.
>
> **El pago, siempre desde MAX:** $U=+1$ si Blancas llegó a la fila rival o capturó todos los peones negros; $U=-1$ en los casos simétricos. Solo si nadie llegó ni capturó todo, quedarse sin jugada es empate: $U=0$.

Usa el subgrafo de n1 de [[minimax|Minimax a mano]], con la misma numeración. El **orden fijo** es el del dibujo; el **invertido** revierte la lista de hijos en cada nodo.

::: exercise {#jue-tarea-2-ej-empate title="Resuelve n1 con la regla del empate"}

1. **Revisa los finales.** ¿Cuáles cambian de $U$ y cuánto valen ahora?
2. **Resuelve con minimax.** Calcula los valores de n3 y n1 e identifica las jugadas que alcanzan el de n1.
3. **Recorre con el orden fijo.** ¿Cuántos estados genera alfa-beta, dónde poda y con qué corte?
4. **Invierte el orden.** Repite el recorrido y registra lo mismo.
5. **Compara con la regla original.** Con orden fijo se generaban 5 estados; ¿por qué ahora se generan más?
6. **Desempata entre las dos jugadas de n1.** Si Negras pudiera equivocarse, ¿cuál jugarías y por qué?

:::

::: hint {#jue-tarea-2-pista-empate-a of="jue-tarea-2-ej-empate" title="Pista 1 · Qué finales cambian"}

Solo cambian los finales donde alguien se quedó **sin jugada**. En el subgrafo de n1 hay dos: con la regla original, uno lo gana Blancas y el otro Negras.

:::

::: hint {#jue-tarea-2-pista-empate-b of="jue-tarea-2-ej-empate" title="Pista 2 · El primer α"}

Con el orden fijo, ¿cuánto vale n2 ahora? Ese es el $\alpha$ que recibe n3: compáralo con lo que devuelve su primer hijo.

:::

**Antes de abrir la respuesta, revisa tu hoja:**

- **Cambiaste solo los finales afectados.** Son los que dejan al jugador de turno sin jugada.
- **Anotaste la ventana en cada nodo.** Registraste $\alpha$ y $\beta$ al llegar, también donde no hubo poda.
- **Nombraste cada poda.** Indicaste corte alfa o corte beta y los estados que no se generaron.
- **Separaste valor y jugada.** Distinguiste cuánto vale n1 de cuál jugada elegirías.

::: answer {#jue-tarea-2-resp-empate of="jue-tarea-2-ej-empate" title="Respuesta · n1 con empate"}

**1 · Los finales que cambian.**

Cambian **n2**, donde Negras no tiene jugada, y **n13**, donde no la tiene Blancas. **Los dos pasan a valer 0.**

Los otros cinco finales son llegadas de Blancas a la fila 3 y conservan $U=+1$.

**2 · Los valores y las jugadas.**

Las ramas de n4 y n6 conservan su valor $+1$. Como n13 ahora vale 0:

$$
V(\text{n3})=\min\{+1,\ +1,\ 0\}=0.
$$

En n1, las dos jugadas quedan así:

| Jugada $a$ | Lleva a | $Q(\text{n1},a)$ |
|---|---|---:|
| $\text{c1}\textbf{-}\text{c2}$ | n2 | $0$ |
| $\text{c1}\textbf{x}\text{b2}$ | n3 | $0$ |

$$
V(\text{n1})=\max\{0,\ 0\}=\mathbf{0}.
$$

**Las dos jugadas alcanzan el valor de n1: ambas aseguran el empate.**

**3 · Orden fijo: 10 estados.**

n2 devuelve 0, así que n3 recibe $\alpha=0$. Su primer hijo, n4, devuelve $+1$: como $+1>0$, n3 no poda y baja $\beta$ a $+1$.

n6 recibe $(\alpha,\beta)=(0,+1)$; n7 y n8 heredan esa misma ventana.

- **En n8, mueve MAX.** n9 devuelve $+1$ y $v=+1\ge\beta=+1$: hay **corte beta** y n10 no se genera.
- **En n6, mueve MAX.** n7 devuelve $+1$ y $v=+1\ge\beta=+1$: hay **corte beta** y n11 y n12 no se generan.

Después se visita n13, que vale 0. n3 devuelve 0 y la raíz también; en n3 ya no quedan hijos pendientes.

Se generan, en este orden: **n1, n2, n3, n4, n5, n6, n7, n8, n9 y n13**.

**4 · Orden invertido: 8 estados.**

n3 se visita primero. Su primer hijo, n13, devuelve 0, así que $\beta$ baja a 0.

- **En n6, mueve MAX.** Su primer hijo, n12, devuelve $+1$ y $v=+1\ge\beta=0$: hay **corte beta** y no se generan n11 ni n7 con sus descendientes.
- **La rama de n4 devuelve $+1$ por n5.** n3 conserva el 0; después n2 devuelve 0 y la raíz también conserva ese valor.

Se generan, en este orden: **n1, n3, n13, n6, n12, n4, n5 y n2**.

**5 · Por qué ahora se poda menos.**

Con la regla original, n2 daba $+1$ y n3 recibía $\alpha=+1$. Bastaba que n4 devolviera $+1$ para cumplir $v\le\alpha$ y podar los hijos restantes de n3.

Ahora n2 solo asegura 0. Cuando n4 devuelve $+1$, todavía es posible que la rama de n3 mejore lo que MAX tiene asegurado; hay que seguir.

**Un $\alpha$ más bajo poda menos.** Aquí el cambio de $+1$ a 0 hace pasar de 5 a 10 estados con el mismo orden.

**6 · Cuál jugar si Negras puede equivocarse.**

Con juego perfecto, las dos jugadas empatan, pero dejan oportunidades distintas:

- **$\text{c1}\textbf{-}\text{c2}$ empata de inmediato.** Negras se queda sin jugada.
- **$\text{c1}\textbf{x}\text{b2}$ deja dos maneras de equivocarse a Negras.** Solo $\text{c3}\textbf{x}\text{b2}$ conserva el empate; sus otras dos respuestas permiten a Blancas asegurar la victoria.

**Conviene $\text{c1}\textbf{x}\text{b2}$: conserva el empate garantizado y permite aprovechar un error.** Es un desempate dentro del $\operatorname{arg\,max}$, como preferir ganar rápido; no cambia $U$ ni los valores calculados.

:::

**Punto de control:** deberías poder escribir el modelo de un juego pequeño, resolverlo con minimax, recorrerlo con alfa-beta en dos órdenes y explicar por qué cambió el ahorro.

---

## Lo que hay que llevarse

- **El estado guarda lo que necesita la utilidad.** En monedas incluye $\Delta$; para reutilizar la diferencia futura $W$ basta el tramo.
- **$V$ siempre se mide desde MAX; $W$, desde quien mueve.** Se relacionan con $V=\Delta+W$ si mueve MAX y $V=\Delta-W$ si mueve MIN; en un final, $V=U=\Delta$.
- **La regla codiciosa puede perder.** Minimax considera la mejor respuesta del rival, aunque tomar la moneda mayor parezca atractivo.
- **El azar se pondera con sus probabilidades.** Una esperanza mayor puede recomendar otra jugada sin mejorar su garantía ante un rival que juega perfecto.
- **Cambiar los finales cambia lo que poda alfa-beta.** Un $\alpha$ más bajo poda menos: en n1, el mismo orden pasa de 5 a 10 estados.
- **Las jugadas con el mismo valor admiten un desempate.** Puedes preferir la que deje oportunidades de aprovechar errores sin cambiar la utilidad.

Continúa con [[juegos-cuando-no-cabe|la clase 3]], donde el árbol ya no cabe.
