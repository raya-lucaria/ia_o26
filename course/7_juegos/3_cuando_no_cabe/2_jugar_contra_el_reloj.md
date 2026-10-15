---
id: jugar-contra-el-reloj
title: "Hasta dónde mirar: profundidad, tiempo y horizonte"
nav_title: Hasta dónde mirar
summary: "Un corte a profundidad fija puede dejar detrás la respuesta decisiva: es el efecto horizonte. La búsqueda de quietud sigue las capturas desde los nodos de corte; la profundización iterativa busca con d = 1, 2, 3 mientras haya reloj y entrega la jugada de la última búsqueda completa, primero sin poda y después con alfa-beta y la jugada anterior primero. Una tabla de transposición guarda si cada número es un valor, un piso o un techo."
status: ready
estimated_time: 72m
tags: [juegos, busqueda-adversarial, evaluacion, algoritmos]
aliases: [mas-alla-del-horizonte]
---

# Hasta dónde mirar: profundidad, tiempo y horizonte

**¿Qué pasa con lo que la búsqueda no alcanza a ver, y qué jugada entregamos si se acaba el tiempo?**

Las dos preguntas tienen la misma raíz: el corte decide hasta dónde se mira. Al terminar tendrás:

- **el efecto horizonte**: señalar, en una posición de peones, qué jugada queda detrás del corte y qué valor cambia por ella;
- **la búsqueda de quietud**: calcular a mano cuánto vale cada jugada si, antes de evaluar, se miran las capturas, y decir qué horizontes arregla;
- **la profundización iterativa**: qué jugada entrega un programa según cuándo se acaba el reloj, en una versión sin poda y otra con alfa-beta, línea por línea;
- **la tabla de transposición**: si un número guardado es un valor, un piso o un techo.

## Lo que traes

- **Las reglas generan el juego.** $S_F$ reconoce finales (@jue-c1-finales); $\mathrm{Pl}(s)$ lee quién mueve (@jue-c1-pl); $A(s)$ enumera jugadas (@jue-c1-acciones); $T(s,a)$ da el estado siguiente (@jue-c1-transicion); $U$ paga los finales (@jue-c1-utilidad).
- **El valor se mide desde MAX.** $V(s)$ supone que los dos juegan lo mejor; $Q(s,a)=V(T(s,a))$ valora una jugada (@jue-c1-valor-jugada-estrategia).
- **El corte estima donde se detiene.** De [[cortar-y-evaluar|Cortar y evaluar]]: $\mathrm{EVAL}$ (@jue-c3-evaluacion), la escala $M\cdot U$ con $M=100$ y $|\mathrm{EVAL}|<M$ (@jue-c3-orden-finales), y el valor con corte $V_d$ (@jue-c3-valor-con-corte).
- **Alfa-beta poda con una ventana.** De [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]]: $(\alpha,\beta)$, el corte alfa y el corte beta.

> **Las reglas del 4×4** son las de [[cortar-y-evaluar|Cortar y evaluar]]. Un peón avanza una casilla vacía o captura en diagonal hacia delante. Gana quien llega a la fila rival, captura todo o deja al rival sin jugada. Blancas (B) es MAX y Negras (N) es MIN: $U=+1$ si gana Blancas y $U=-1$ si gana Negras.

> **Supuestos.** Los de [[cortar-y-evaluar|Cortar y evaluar]]: dos jugadores por turnos, sin azar, todo a la vista, toda partida termina y suma cero (o constante). No alcanza para llegar a los finales, y hay uno más: **hay un reloj**. El tablero espera a que juegues; el tiempo para decidir, no.

> [!TIP]
> **Míralo correr: profundización iterativa en el árbol de resultados**
>
> - **▶ [Animación paso a paso](../_assets/traza_arbol_t.html#iterativa)**: el árbol, la línea del
>   código que corre y el valor de cada variable. Avanza con ▶ o con las flechas.
> - **Notebook en Colab**, sección 7: el mismo Python de esta página,
>   corriendo; cámbiale un número y mira qué pasa.
>
> [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/raya-lucaria/ia_o26/blob/main/course/7_juegos/_assets/01_decidir_en_el_arbol_t.ipynb)

---

## 1 · El problema: lo que no se ve y el tiempo que no alcanza

**Piensa: si el corte decide hasta dónde mirar, ¿qué puede salir mal?**

Dos cosas: que lo decisivo quede justo detrás, y que el tiempo se acabe antes de terminar.

Seguimos con la posición de [[cortar-y-evaluar|Cortar y evaluar]] y la misma evaluación, ${\mathrm{EVAL}=10\cdot\text{material}+\text{avance}}$. El material es peones blancos menos peones negros; el avance, avance blanco menos avance negro. En los finales, ${M\cdot U=\pm100}$. Como allá, $d$ es **la profundidad que queda**: en la raíz, la de toda la búsqueda.

::: table {#jue-c3-posicion-horizonte title="La posición de la clase · mueven Blancas"}
| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | N | · | · |
| **3** | · | · | N | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |
:::

La tabla copia @jue-c3-profundidades. En la búsqueda con $d$ en la raíz, cada jugada vale $V_{d-1}(T(s,a))$: le quedan $d-1$ jugadas por mirar. La raíz toma el máximo. La última columna es el valor exacto, en la misma escala.

::: table {#jue-c3-horizonte-valores title="Valor de cada jugada de Blancas en cada búsqueda, y su valor exacto"}
| Jugada | $d=1$ | $d=2$ | $d=3$ | $100\,Q$ |
|---|---:|---:|---:|---:|
| $\text{a1}\textbf{-}\text{a2}$ | 2 | −10 | −9 | −100 |
| $\text{d2}\textbf{-}\text{d3}$ | 2 | **1** | **100** | **100** |
| $\text{d2}\textbf{x}\text{c3}$ | **13** | 0 | 1 | −100 |
:::

En negrita, el máximo de cada columna: la jugada que elige Blancas. $100\,Q$ abrevia $100\,Q(s_{\text{raíz}},a)$.

La tabla plantea tres preguntas, y la página las contesta en orden:

- **¿Qué no vio $d=1$?** Eligió la captura con 13, y la captura pierde.
- **¿Cuánto mirar si no sabes cuánto tiempo queda?** Con $d=3$ ya se ve la victoria; con un reloj corto, quizá no se alcanza.
- **¿Cuánto cuesta repetir?** Buscar con $d=1$, luego 2 y luego 3 parece trabajar tres veces.

> **Dado:** un estado $s$ donde mueve MAX, las reglas, una $\mathrm{EVAL}$ con $|\mathrm{EVAL}|<M$ y un reloj que nadie sabe cuándo se acaba.
>
> **Encontrar:** una jugada lista para entregar en cualquier momento, que no caiga en lo que el corte esconde.

---

## 2 · El efecto horizonte

**Piensa: a profundidad 1, ¿qué no alcanzó a ver Blancas cuando eligió capturar?**

La respuesta de Negras. Con $d=1$, $\text{d2}\textbf{x}\text{c3}$ valía 13 y las otras dos jugadas, 2. El algoritmo vio **la ganancia**: un peón de más. No vio **la respuesta**: Negras recaptura con $\text{b4}\textbf{x}\text{c3}$ y el peón de ventaja desaparece. Con $d=2$ la captura bajó a 0, y Blancas cambió de jugada.

La recaptura existía desde el principio. Estaba una jugada más allá de la línea donde se corta, y el algoritmo no mira detrás de esa línea. **A la línea donde se corta la llamamos horizonte.**

::: definition {#jue-c3-efecto-horizonte title="Efecto horizonte"}
**Qué es.** El **efecto horizonte** (*horizon effect*) ocurre cuando una consecuencia importante de una jugada queda detrás del horizonte.

**Cómo se produce.** La búsqueda evalúa la posición antes de esa consecuencia, y la valora mal. En la captura de la clase, se detiene antes de la recaptura.

**Qué significa.** El número del nodo de corte describe una posición a mitad de algo que todavía no termina.

**Qué no es.** No siempre cambia la jugada elegida: también puede equivocar solo el valor.

**El caso clásico.** Hans Berliner le dio nombre en 1973; la forma más citada es otra: una **pérdida inevitable que el programa aplaza**. El programa intercala jugadas que el rival tiene que contestar, y cada una empuja la pérdida dos jugadas más lejos. Cuando sale del horizonte, el programa cree que la evitó.

Por ejemplo, un programa de ajedrez que va a perder la dama da un jaque tras otro. No salva la dama: solo deja de ver su pérdida.
:::

El ejemplo de esta página es la forma simple: **una sola respuesta, la recaptura, queda detrás del horizonte**. En ajedrez pasa igual cuando una pieza captura un peón defendido y el corte cae antes de la recaptura.

::: figure {#jue-c3-fig-horizonte title="El efecto horizonte: la recaptura queda detrás"}
![A profundidad 1, la búsqueda ve la captura d2xc3 y evalúa en 13: un peón de más. Una línea punteada marca el horizonte, donde se corta con d = 1 en la raíz. Detrás está la recaptura b4xc3, en una caja punteada con «?»: la búsqueda no la genera. Con ella, EVAL bajaría a 0](../_assets/jue-c3-horizonte.svg)
:::

> [!WARNING]
> **Mientras el corte no llegue a todos los finales, subir la profundidad
> no elimina el efecto horizonte: lo mueve.** Con $d=2$ la recaptura
> ya se ve, pero el horizonte sigue ahí, una jugada más abajo. Si el corte
> llega a todos los finales, el efecto desaparece; en un juego grande no
> suele haber una profundidad práctica que lo logre en toda posición.

::: exercise {#jue-c3-ej-detras title="Encuentra lo que queda detrás a profundidad 2"}
En @jue-c3-horizonte-valores, $\text{d2}\textbf{-}\text{d3}$ vale 1 con $d=2$ y 100 con $d=3$.

1. Con ${d=2}$ en la raíz, ¿en qué nodos de la rama de $\text{d2}\textbf{-}\text{d3}$ cae el corte, y qué $\mathrm{EVAL}$ recibe cada uno? ¿Qué jugada queda detrás del horizonte y hace saltar el valor?
2. ¿Cambia la jugada que Blancas elige con $d=2$?
:::

::: hint {#jue-c3-pista-detras-1 of="jue-c3-ej-detras" title="Qué agrega un nivel"}
Tras $\text{d2}\textbf{-}\text{d3}$ mueve Negras: ¿con qué $d$ llegan sus respuestas? La profundidad 3 agrega una sola jugada, de Blancas. ¿Qué tendría que pasar en esa jugada para que el número salte de 1 a 100?
:::

::: answer {#jue-c3-resp-detras of="jue-c3-ej-detras"}
1. Tras $\text{d2}\textbf{-}\text{d3}$, Negras solo puede avanzar: $\text{a4}\textbf{-}\text{a3}$ o $\text{b4}\textbf{-}\text{b3}$. Esos dos nodos llegan con ${d=0}$, no son finales, y reciben ${\mathrm{EVAL}=1}$ los dos: la rama vale ${\min(1,1)=1}$. Detrás queda **$\text{d3}\textbf{-}\text{d4}$**: Blancas lleva el peón de d3 a la fila 4 y gana, ${M\cdot U=100}$.
2. **No cambia.** Con $d=2$, $\text{d2}\textbf{-}\text{d3}$ ya era la mayor: 1 contra 0 y ${-10}$. El horizonte escondió **cuánto** vale, no **cuál** es la mejor. El efecto horizonte hace daño cuando cambia la decisión, como con $d=1$.
:::

---

## 3 · Minimax con corte, más allá del nivel fijo

**Piensa: si no se puede quitar el horizonte, ¿qué se puede cambiar?**

Dónde cae y cuántas veces se busca. La página cambia dos piezas del corte de [[cortar-y-evaluar|Cortar y evaluar]] y conserva el resto:

- **La búsqueda de quietud** cambia lo que pasa **en un nodo de corte**: antes de evaluar, mira las capturas.
- **La profundización iterativa** cambia **cuántas veces** se busca: con $d=1$, luego 2, luego 3, mientras haya reloj.

Las dos comparten el mapa del corte:

- **Qué valor rastrea:** $V_d$, el minimax del árbol cortado (@jue-c3-valor-con-corte). La quietud cambia lo que vale un nodo de corte; la poda puede devolver cotas.
- **Dónde lo guarda:** en la pila de llamadas, como minimax. La iterativa guarda además la jugada lista; la tabla de transposición, lo ya valorado.
- **Cómo sube:** máximo en MAX y mínimo en MIN, desde $\mathrm{EVAL}$ o desde $M\cdot U$.
- **A qué converge:** no promedia nada. Da $M\cdot V$ solo si alcanza los finales sin evaluar ni activar la quietud.

::: figure {#jue-c3-fig-flujo-reloj title="El corte, en palabras: por nivel o por reloj"}
![Diagrama de flujo del corte. Un nodo final vale 100·U y vuelve al padre; si no es final y d = 0, vale EVAL; si no, baja a cada hijo con d − 1 y, al volver, MAX se queda con el mayor y MIN con el menor. En la raíz juega la jugada de mayor valor. Por reloj, repite con d = 1, 2, 3… y juega la de la última búsqueda completa](../_assets/jue-c3-rx-flujo-corte.svg)
:::

Las dos se ponen a prueba en el **árbol de resultados**, con finales en $M\cdot U$ y una $\mathrm{EVAL}$ inventada: I 60, C 20, D 10, C1 10 y C2 50. La de I es mala a propósito: no ve que la captura ix pierde. Como $|\mathrm{EVAL}|<100$, aquí sí se cumple @jue-c3-orden-finales.

---

### Búsqueda de quietud

**Piensa: ¿en qué posiciones es peligroso detenerse a evaluar?**

En las que tienen **capturas pendientes**: ahí $\mathrm{EVAL}$ cambiará en la jugada siguiente. En [[cortar-y-evaluar|Cortar y evaluar]] intentamos adivinarlas con un rasgo que resta 10 por cada captura de Negras (@jue-c3-ej-rasgo). La captura todavía ganaba, 3 contra 2. En vez de adivinar las capturas, se pueden **mirar**.

- **Qué valor rastrea:** el **valor con quietud**: el valor con corte, salvo en los nodos de corte que tienen capturas.
- **Dónde lo guarda:** igual que el corte; la pila crece con cada captura que sigue.
- **Cómo sube:** máximo y mínimo, como siempre; en un nodo de corte también compite quedarse con su $\mathrm{EVAL}$.
- **A qué converge:** a $M\cdot V$ solo si la búsqueda llega a los finales **antes** de activar la quietud.

::: definition {#jue-c3-quietud title="Posición quieta y búsqueda de quietud"}
**Qué es.** Una posición es **quieta** si el jugador de turno no tiene ninguna captura disponible. En ella, $\mathrm{EVAL}$ es más confiable. La **búsqueda de quietud** (*quiescence search*) cambia lo que pasa en un nodo de corte que no es quieto.

**Cómo se calcula.** No devuelve sin más la $\mathrm{EVAL}$ del nodo de corte: la usa como opción de **quedarse** y la compara con **las capturas**; cada captura sigue hasta un final o una posición quieta. En cada paso, quien mueve elige entre capturar o quedarse con la $\mathrm{EVAL}$ de la posición, aunque esta todavía tenga capturas.

**Qué significa.** Reduce los cortes a mitad de un intercambio. El número que da es el **valor con quietud**: sigue estimando con $\mathrm{EVAL}$, y puede devolver la de una posición que no es quieta, si quedarse sale mejor.

**Qué no es.** No es buscar una jugada más en todas partes. Solo se siguen las capturas, y solo desde los nodos de corte.
:::

#### 1 · Exploración: cómo obtiene su número

**La regla.** En MINIMAX-CON-CORTE solo cambia la línea que devuelve $\mathrm{EVAL}(s)$: en su lugar, llama a la búsqueda de quietud. Desde MAX:

1. **Revisa si es final.** Un final vale $M\cdot U$, como siempre.
2. **Toma la opción de quedarse.** El nodo empieza valiendo su $\mathrm{EVAL}$.
3. **Sigue cada captura.** Cada una se valora con la misma búsqueda, hasta un final o una posición quieta.
4. **Se queda con el mayor.** MAX compara quedarse con cada captura y toma el máximo.

| Quién mueve | Valor con quietud |
|---|---|
| MAX | $\mathbf{\max(\mathrm{EVAL}(s),\ \text{cada captura})}$ |
| MIN | $\mathbf{\min(\mathrm{EVAL}(s),\ \text{cada captura})}$ |

Quedarse no es una jugada legal: es una aproximación, que en inglés se llama *stand pat* («plantarse»). Supone que quien mueve tiene alguna jugada que no captura y que es al menos tan buena para quien mueve como quedarse: para MAX, ${\geq \mathrm{EVAL}}$; para MIN, ${\leq \mathrm{EVAL}}$.

La quietud no mira esas jugadas. Puede fallar si esa jugada no existe —por ejemplo, si todas son capturas— o si toda jugada empeora su posición.

**Ejemplo mínimo:** un nodo de MAX con $\mathrm{EVAL}=20$ y una sola captura.

| La captura llega a | Compara | El nodo vale |
|---|---|---|
| Una posición quieta con 50 | $\max(20,50)$ | 50: la sigue |
| Una posición quieta con $-10$ | $\max(20,-10)$ | 20: se planta |

Ese 20 supone que MAX tiene alguna jugada sin captura que conserve el 20. Si todas las que tiene pierden, el 20 es demasiado optimista.

---

**Recorrido: la captura de la clase, con $d=1$.**

- **El nodo de corte.** Tras $\text{d2}\textbf{x}\text{c3}$ queda ${d=0}$ y mueven Negras. El peón de b4 tiene al peón blanco de c3 en su diagonal: la posición no es quieta.
- **Las dos opciones de Negras.** Quedarse, con ${\mathrm{EVAL}=13}$, o capturar con $\text{b4}\textbf{x}\text{c3}$.
- **Tras la captura.** Mueven Blancas, con peones en a1 y c2. Ninguno tiene un peón negro en su diagonal: la posición es quieta. Se evalúa: 0.
- **Lo que elige Negras.** Es MIN: ${\min(13,0)=0}$. La captura vale **0**.

Es el mismo 0 que con $d=2$, pero sin mirar todas las respuestas de Negras: solo su captura.

::: exercise {#jue-c3-ej-quietud title="Calcula la quietud de las otras dos jugadas"}
Haz lo mismo con $\text{a1}\textbf{-}\text{a2}$ y $\text{d2}\textbf{-}\text{d3}$, con $d=1$. En el corte, las dos tienen ${\mathrm{EVAL}=2}$.

1. ¿Es quieta la posición tras cada una? Si no lo es, ¿qué captura tiene Negras?
2. ¿Qué valor recibe cada jugada con la búsqueda de quietud?
3. Con los tres valores, ¿qué jugada elige Blancas? Compárala con la columna $100\,Q$ de @jue-c3-horizonte-valores.
:::

::: hint {#jue-c3-pista-quietud-1 of="jue-c3-ej-quietud" title="Los mismos cuatro pasos"}
Recorre, para cada jugada, los cuatro pasos del recorrido. ¿Qué peones negros tienen un peón blanco en una diagonal de enfrente, hacia abajo? Y si hay captura, ¿la posición que deja es quieta para Blancas?
:::

::: answer {#jue-c3-resp-quietud of="jue-c3-ej-quietud"}
1. Tras **$\text{a1}\textbf{-}\text{a2}$**, el peón de c3 puede capturar en d2: $\text{c3}\textbf{x}\text{d2}$. Tras **$\text{d2}\textbf{-}\text{d3}$**, el peón de c3 tiene c2 ocupada enfrente y nada en b2 ni en d2: la posición es quieta.
2. En $\text{a1}\textbf{-}\text{a2}$, Negras elige entre quedarse, 2, y $\text{c3}\textbf{x}\text{d2}$. Tras esa captura, Blancas tiene peones en a2 y c2 y nada que capturar: es quieta, con ${\mathrm{EVAL}=-10}$. Negras toma ${\min(2,-10)=-10}$. $\text{d2}\textbf{-}\text{d3}$ es quieta y se queda con su 2.
3. Los valores son ${-10}$, 2 y 0. Blancas elige **$\text{d2}\textbf{-}\text{d3}$**, la que gana: su $100\,Q$ es 100. Con solo mirar las capturas, $d=1$ dejó de elegir la captura perdedora.
:::

**Recorrido: el árbol de resultados, con $d=1$.**

El corte simple juega izq, con 60: no ve la captura ix. Con quietud, I no es quieto: MIN tiene la captura ix.

| Hijo de R | Quedarse | Capturas | Valor con quietud |
|---|---:|---|---:|
| I | 60 | ix: −100 | −100 |
| C | 20 | ninguna | 20 |
| D | 10 | ninguna | 10 |

En I mueve MIN: compara 60 con ${-100}$ y captura. C y D no tienen capturas y se quedan en 20 y 10.

::: figure {#jue-c3-fig-resultados-quietud title="Búsqueda de quietud con d = 1 en el árbol de resultados: juega centro"}
![Búsqueda de quietud con corte a profundidad 1 en el árbol de resultados, finales en 100·U: genera 5 nodos, R, I, C, D y la captura ix. En I, que no está quieto, MIN compara quedarse con la EVAL, 60, con capturar, −100, y toma el menor: I vale −100. C y D no tienen capturas y valen su EVAL: izq −100, centro 20, der 10. Juega centro, con 20](../_assets/jue-c3-rx-quietud.svg)
:::

La quietud juega **centro**, con 20, y genera 5 nodos: los 4 del corte más ix. **Arregla la jugada, pero no el valor**: 20 no es el ${100\,V=0}$. El 20 es la $\mathrm{EVAL}$ de C, que es quieta.

#### 2 · Elección: qué jugada juega

Como el corte por nivel: al terminar, la jugada de la raíz con **mayor valor con quietud**. En empate, la primera en el orden dado. Interrumpida antes de terminar, no garantiza nada.

| Decisión | Qué compara |
|---|---|
| Explorar, desde un nodo de corte | $\mathrm{EVAL}$ contra cada captura |
| Jugar, en la raíz | Valores con quietud |

#### 3 · Propiedades

Lo que cambia frente al corte de [[cortar-y-evaluar|Cortar y evaluar]]:

- **Número que da:** el valor con quietud de cada jugada; no es $V$ ni $M\cdot V$.
- **Usa EVAL:** sí, en las posiciones quietas y, como valor de quedarse, también en las que tienen capturas.
- **Garantía:** da $M\cdot V$ solo si llega a los finales **antes de activar la quietud**. Corrige muchos intercambios a medias, no todos.
- **Se puede interrumpir:** no; como el corte por nivel, entrega al terminar.
- **Complejidad:** ya no está limitada a $d$: una cadena de capturas puede llegar al final de la partida. En el peor caso, tiempo $O(b^m)$ y memoria $O(bm)$, con $m$ el largo máximo de una partida. En los programas de ajedrez, los nodos de quietud suelen ser muchos.
- **Frente a los demás:** mira poco más que el corte y cambia la decisión donde $\mathrm{EVAL}$ engaña más: a mitad de un intercambio. En ajedrez la usaba Deep Blue.
- **Supuestos:** los del corte. Con más jugadores, $\mathrm{EVAL}$ y la idea de «quieta» tienen que ser por jugador, con pagos vectoriales y $\max^n$.

En este juego la búsqueda de quietud siempre termina: cada captura quita un peón, y los peones se acaban.

#### 4 · Casos borde

- **Un final en medio de las capturas:** se revisa antes que quedarse y vale $M\cdot U$.
- **Una sola jugada legal:** ya está decidida; su número sigue dependiendo de la aproximación de quedarse.
- **Captura obligada:** si quien mueve está obligado a capturar, quedarse puede ocultar su única jugada legal.
- **Todas las jugadas son capturas:** quedarse supone una jugada tranquila que no existe; el ejemplo de abajo vale 0 y en verdad pierde.
- **Las capturas llegan a todos los finales:** aun así, quedarse compite. En el árbol de resultados, si todas las jugadas bajo $d=1$ fueran capturas, C1 se plantaría en su 10 en vez de jugar c1a, que vale 0: centro valdría 10, no 0.

::: remark {#jue-c3-quedarse-falla title="Cuando quedarse engaña"}
Desde el inicio del 4×4 se juega $\text{a1}\textbf{-}\text{a2}$, $\text{b4}\textbf{-}\text{b3}$, $\text{d1}\textbf{-}\text{d2}$, $\text{b3}\textbf{-}\text{b2}$, $\text{a2}\textbf{-}\text{a3}$, $\text{c4}\textbf{-}\text{c3}$, $\text{d2}\textbf{-}\text{d3}$ y $\text{c3}\textbf{-}\text{c2}$. Quedan Blancas en b1, c1, a3 y d3, Negras en b2, c2, a4 y d4, y mueven Blancas.

Blancas solo tiene dos jugadas, $\text{b1}\textbf{x}\text{c2}$ y $\text{c1}\textbf{x}\text{b2}$: las dos son capturas, y tras cualquiera Negras llega a la fila 1 en la jugada siguiente. Si el corte cae aquí, la quietud compara quedarse, con ${\mathrm{EVAL}=0}$, contra esas dos capturas, que valen ${-100}$, y devuelve **0**. El valor exacto de este estado es ${100\cdot V=-100}$: quedarse supuso una jugada tranquila que Blancas no tiene.
:::

#### Intuición

- **La quietud arregla la jugada, no el valor.** En la clase y en el árbol de resultados elige la jugada buena; sus números siguen siendo estimaciones.
- **Mira solo lo que cambia rápido.** Una captura mueve $\mathrm{EVAL}$ unos 10 puntos de golpe; un avance tranquilo, uno.
- **No ve lo que no es captura.** Con quietud, $\text{d2}\textbf{-}\text{d3}$ sigue valiendo 2 aunque gane: la victoria llega por un avance.

#### Ejercicios

::: exercise {#jue-c3-cmp-ej-quietud title="Señala lo que la quietud no mira"}
En el árbol de resultados, la quietud con ${d=1}$ da 20 en C, y el valor exacto de C es $0$.

1. ¿Por qué la quietud no sigue ninguna jugada bajo C?
2. ¿Qué elección de MIN tendría que mirar para llegar a $0$?
:::

::: hint {#jue-c3-cmp-pista-quietud-1 of="jue-c3-cmp-ej-quietud" title="Qué jugadas sigue"}
En un nodo de corte, ¿qué clase de jugadas sigue la quietud? ¿Hay alguna bajo C?
:::

::: answer {#jue-c3-cmp-resp-quietud of="jue-c3-cmp-ej-quietud"}
1. Solo sigue capturas, y ninguna jugada bajo C lo es: C es quieta y se evalúa ahí.
2. La de C1 contra C2. El error de C no es un intercambio a medias: es que MIN puede mandar a C1, donde MAX solo empata. Eso solo lo ve buscar más hondo, como con ${d=3}$.
:::

**Piensa: ¿la búsqueda de quietud arregla cualquier efecto horizonte?**

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-clasifica title="Pon a prueba la quietud en dos programas"}
Los dos programas usan la búsqueda de quietud. La idea nueva: **la quietud puede seguir varias capturas seguidas**, una tras otra, y toparse con un final en medio de ellas.

**El programa de peones** busca con $d=1$ en esta posición nueva del 4×4. Mueven Blancas:

| | a | b | c | d |
|---|:---:|:---:|:---:|:---:|
| **4** | N | · | N | · |
| **3** | · | N | · | · |
| **2** | · | · | B | B |
| **1** | B | · | · | · |

Blancas tiene cuatro jugadas: $\text{a1}\textbf{-}\text{a2}$, $\text{c2}\textbf{-}\text{c3}$, $\text{c2}\textbf{x}\text{b3}$ y $\text{d2}\textbf{-}\text{d3}$. Con $\mathrm{EVAL}$ en seco, sin quietud, valen 2, 2, 13 y 2.

**El programa de ajedrez** busca a profundidad fija. Va a perder la dama sin remedio. En vez de aceptarlo, da un jaque tras otro, ninguno con captura, y con esos jaques la pérdida queda detrás del horizonte.

1. Con quietud, $\text{a1}\textbf{-}\text{a2}$ vale ${-10}$ y $\text{c2}\textbf{-}\text{c3}$ vale 2. Calcula el valor con quietud de $\text{c2}\textbf{x}\text{b3}$ y de $\text{d2}\textbf{-}\text{d3}$.
2. ¿Qué jugada elige el programa de peones con quietud, y cuál sin ella?
3. ¿Por qué la quietud no salva al programa de ajedrez? ¿Lo arregla buscar dos jugadas más?
:::

::: hint {#jue-c3-pista-clasifica-1 of="jue-c3-ej-clasifica" title="Pista 1 · Un árbol solo de capturas"}
Para cada jugada, dibuja desde el nodo de corte un árbol que tenga solo capturas. En cada nodo, ¿quién mueve, cuánto vale quedarse y qué capturas tiene? Para el ajedrez: ¿qué clase de jugadas sigue la quietud, y de qué clase son las que usa el programa para aplazar?
:::

::: hint {#jue-c3-pista-clasifica-2 of="jue-c3-ej-clasifica" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. Antes de evaluar cada posición, ¿revisaste si la partida ya terminó? ¿En cada nodo comparaste quedarse con todas las capturas, del lado de quien mueve?
:::

::: answer {#jue-c3-resp-clasifica of="jue-c3-ej-clasifica" title="Respuesta · Los dos programas, uno por uno"}
1. **$\text{c2}\textbf{x}\text{b3}$ vale 0.** Mueven Negras, con ${\mathrm{EVAL}=13}$. Sus dos recapturas, $\text{a4}\textbf{x}\text{b3}$ y $\text{c4}\textbf{x}\text{b3}$, dejan posiciones quietas con 0. Negras toma ${\min(13,0,0)=0}$.

   **$\text{d2}\textbf{-}\text{d3}$ vale 1.** Mueven Negras, con ${\mathrm{EVAL}=2}$, y tienen dos capturas:
   - **$\text{b3}\textbf{x}\text{c2}$:** mueven Blancas, con ${-10}$. Pero $\text{d3}\textbf{x}\text{c4}$ llega a la fila 4: es un final y vale 100. Blancas toma ${\max(-10,100)=100}$.
   - **$\text{c4}\textbf{x}\text{d3}$:** mueven Blancas, con ${-11}$. $\text{c2}\textbf{x}\text{d3}$ deja una posición quieta con 1. $\text{c2}\textbf{x}\text{b3}$ deja una posición donde Negras puede quedarse, con 1, o recapturar con $\text{a4}\textbf{x}\text{b3}$, con ${-12}$: vale ${\min(1,-12)=-12}$. Blancas toma ${\max(-11,1,-12)=1}$.

   Negras toma ${\min(2,100,1)=1}$: la quietud siguió **tres capturas seguidas**.
2. Con quietud los valores son ${-10}$, 2, 0 y 1: elige **$\text{c2}\textbf{-}\text{c3}$**. Sin ella elige $\text{c2}\textbf{x}\text{b3}$, con 13. La computadora comprobó que $\text{c2}\textbf{-}\text{c3}$ gana y $\text{c2}\textbf{x}\text{b3}$ pierde. Aquí el horizonte caía en medio de un intercambio, y eso sí lo arregla la quietud.
3. **Los jaques sin captura quedan fuera de esta versión**, que solo sigue capturas, y el corte puede caer a mitad de la serie. La de los programas de ajedrez puede seguir también jaques y otras jugadas forzadas (Deep Blue lo hacía), y aun así no quita todo efecto horizonte.

   Buscar dos jugadas más **no necesariamente** basta: si le queda un jaque, el programa lo da y la pérdida vuelve a quedar detrás. Es el caso clásico: el propio programa aplaza la pérdida. Mientras le queden jugadas para aplazar y el corte no llegue a los finales, subir la profundidad solo mueve el horizonte.
:::

---

### Profundización iterativa

**Piensa: si no sabes cuánto tiempo te queda, ¿con qué profundidad buscas?**

Con todas, de menor a mayor. En un torneo hay reloj: el tablero espera, el reloj no. Si eliges $d$ demasiado grande, el tiempo se acaba a mitad de la búsqueda y no tienes jugada. Si lo eliges pequeño, desperdicias tiempo y juegas peor, como $d=1$ con la captura.

La salida es no elegir: **buscar con ${d=1}$, luego con ${d=2}$, luego con ${d=3}$**, mientras haya tiempo. Cuando el reloj se acaba, se juega la mejor jugada de la **última búsqueda completa**.

- **Qué valor rastrea:** el valor con corte $V_d$ de la última búsqueda completa; con poda, exacto solo para la jugada elegida.
- **Dónde lo guarda:** la pila de la búsqueda en curso, más la jugada lista de la anterior.
- **Cómo sube:** como alfa-beta con corte, dentro de cada búsqueda.
- **A qué converge:** a $M\cdot V$ cuando la última búsqueda completa llega a todos los finales.

> **Dado:** un estado $s$ donde mueve MAX, las reglas del juego (@jue-c1-finales, @jue-c1-pl, @jue-c1-acciones, @jue-c1-transicion, @jue-c1-utilidad), $\mathrm{EVAL}$ (@jue-c3-evaluacion) y un reloj que nadie sabe cuándo se acaba.
>
> **Encontrar:** una jugada lista para entregar en cualquier momento, tan buena como lo permita el tiempo que hubo.

::: definition {#jue-c3-profundizacion-iterativa title="Profundización iterativa"}
**Qué es.** La **profundización iterativa** (*iterative deepening*) repite la búsqueda con corte con ${d=1,2,3,\dots}$ mientras quede tiempo.

**Cómo se calcula.** Guarda la mejor jugada de cada búsqueda que termina, y al acabarse el reloj entrega la de la última búsqueda completa.

**Qué significa.** Siempre tiene una jugada lista, y la mejora mientras haya tiempo.

**Qué no es.** No usa lo que dejó una búsqueda interrumpida, ni cumple un plazo estricto si solo mira el reloj entre búsquedas o entre hijos.
:::

#### 1 · Exploración: cómo obtiene su número

**La regla**, en cinco pasos:

1. **Guarda un respaldo.** Antes de buscar, guarda la primera jugada legal: así siempre hay algo que entregar.
2. **Busca con la profundidad actual.** Empieza desde la raíz y prueba primero la jugada guardada; después, las demás en el orden dado.
3. **Revisa el reloj.** Antes de cada búsqueda y tras cada hijo de la raíz, sin interrumpir a ese hijo. Si se acabó, descarta la búsqueda en curso y entrega la jugada guardada.
4. **Reconoce una victoria.** Si un hijo devuelve $+M$, entrega esa jugada de inmediato: ninguna $\mathrm{EVAL}$ alcanza $M$.
5. **Guarda y profundiza.** Si la búsqueda termina, guarda su mejor jugada, sube $d$ en uno y vuelve al paso 2.

**El invariante:** `jugada` es el respaldo o la mejor de la última búsqueda completa. Lo que deja una búsqueda en curso se guarda aparte.

---

**Recorrido: el reloj en la posición de la clase.**

**Estamos aquí:** la posición de la clase, mueven Blancas. Las columnas $d=1$, 2 y 3 de @jue-c3-horizonte-valores son lo que deja cada búsqueda.

::: exercise {#jue-c3-ej-reloj title="Encuentra la jugada que se entrega"}
Para cada caso, ¿qué jugada entrega el programa?

1. El reloj se acaba mientras busca con ${d=2}$.
2. El reloj se acaba mientras busca con ${d=3}$.
3. El reloj alcanza para terminar ${d=3}$.
:::

::: hint {#jue-c3-pista-reloj-1 of="jue-c3-ej-reloj" title="Columna por columna"}
En cada caso, ¿cuáles búsquedas terminaron antes de que sonara el reloj? De la última de ellas, ¿qué jugada tiene el número mayor?
:::

::: answer {#jue-c3-resp-reloj of="jue-c3-ej-reloj"}
1. La última búsqueda completa es ${d=1}$, y su mayor número es 13: entrega **$\text{d2}\textbf{x}\text{c3}$**, que pierde.
2. La última completa es ${d=2}$, con 1: entrega **$\text{d2}\textbf{-}\text{d3}$**, que gana.
3. Entrega **$\text{d2}\textbf{-}\text{d3}$**, y además ya sabe que gana: vale 100.

Una búsqueda a medias no se usa: puede no haber revisado la mejor jugada. Es la elección simple y segura, no la única. Los programas reales prueban primero la jugada anterior, y si la búsqueda a medias ya encontró una que la supera, la usan.
:::

La figura lo dibuja en el tiempo. Cada barra es una búsqueda **sin poda**, con DECIDIR-CON-CORTE, y su largo es cuántos nodos genera.

::: figure {#jue-c3-fig-profundizacion title="El reloj decide qué jugada se entrega"}
![Tres búsquedas seguidas sobre la posición de la clase, con d = 1, 2 y 3; el largo de cada barra es el número de nodos que genera: 4 con d = 1, 12 con d = 2, 33 con d = 3. Cada búsqueda completa deja lista una jugada: d = 1: d2xc3 (13), d = 2: d2-d3 (1), d = 3: d2-d3 (100). Dos líneas punteadas, reloj 1 y reloj 2, marcan dos momentos en que se acaba el tiempo; se entrega la jugada de la última búsqueda completa](../_assets/jue-c3-profundizacion.svg)
:::

El reloj decide la calidad de la jugada. **Si el tiempo solo alcanza para ${d=1}$, el programa captura y pierde.**

---

**La versión sin poda.**

**Piensa: ¿qué le falta a DECIDIR-CON-CORTE para jugar contra un reloj?**

Solo un ciclo alrededor: llamarla con ${d=1,2,3,\dots}$ y recordar la jugada de la última búsqueda que terminó. Qué guarda cada nombre:

- **$s$:** el estado donde le toca jugar a MAX.
- **$d$:** la profundidad de la búsqueda en curso.
- **`jugada`:** la mejor de la última búsqueda **completa**: la que se entrega.
- **`nueva`:** lo que devuelve la búsqueda en curso cuando termina.

```text
INPUT   un estado s donde mueve MAX; las
        reglas S_F, Pl, A, T y U; una
        función EVAL; y un reloj.
OUTPUT  una jugada de A(s), la mejor de la
        última búsqueda completa.

 1 function PROFUNDIZAR-SIN-PODA(s)
     # respaldo: siempre hay algo que entregar
 2   jugada ← la primera jugada de A(s)
 3   d ← 1
     # cada vuelta, una búsqueda más honda
 4   while quede tiempo
       # la de Cortar y evaluar, entera
 5     nueva ← DECIDIR-CON-CORTE(s, d)
       # se acabó mientras corría: no cuenta
 6     if el tiempo se acabó: return jugada
 7     jugada ← nueva       # ya terminó
 8     d ← d + 1
 9   return jugada
```

- **La línea 2 guarda el respaldo:** la primera jugada legal.
- **La línea 5 es la búsqueda de [[cortar-y-evaluar|Cortar y evaluar]]**, sin cambiar nada.
- **La línea 6 mira el reloj solo al terminar** cada búsqueda. Si se acabó mientras corría, esa búsqueda no cuenta y se entrega la anterior.
- **Por eso la última puede pasarse del límite:** si cada búsqueda cuesta unas $B$ veces la anterior, la última cuesta cerca de ${B-1}$ veces todo lo ya gastado. En la posición de la clase, 33 nodos contra 16.

**En el árbol de resultados**, R prueba sus hijos en el orden izq, centro, der:

- **${d=1}$ deja lista la trampa:** izq parece valer 60, porque no ve la captura ix; genera 4 nodos.
- **${d=2}$ corrige la jugada:** izq ya vale ${-100}$ y centro, 10; genera 11 nodos.
- **${d=3}$ sigue con centro**, que ahora vale 0; genera 15 nodos y ya llega a todos los finales.

Son los valores de @jue-c3-t-por-profundidad, en [[cortar-y-evaluar|Cortar y evaluar]]. Las tres búsquedas generan ${4+11+15=30}$ nodos. Si el reloj se acaba durante ${d=2}$, se entrega izq; durante ${d=3}$, centro.

::: exercise {#jue-c3-ej-orden-sin-poda title="Comprueba si el orden importa"}
Cambia el orden en que R prueba sus hijos: en cada búsqueda va primero la jugada lista de la anterior. Con ${d=2}$, R prueba izq, centro, der; con ${d=3}$, centro, izq, der.

1. ¿Cambia la jugada lista de alguna búsqueda?
2. ¿Cambia el número de nodos?
:::

::: hint {#jue-c3-pista-orden-sin-poda-1 of="jue-c3-ej-orden-sin-poda" title="Qué línea podría notarlo"}
¿Hay alguna línea de DECIDIR-CON-CORTE o de MINIMAX-CON-CORTE que deje de generar un hijo? ¿Y cuándo podría cambiar el ganador de `w > mejor_valor`?
:::

::: answer {#jue-c3-resp-orden-sin-poda of="jue-c3-ej-orden-sin-poda"}
1. **No.** El `>` estricto solo distingue el orden cuando hay empate en el máximo. Con $d=2$ empatan izq y der, con ${-100}$, pero el máximo es el 10 de centro. Las listas siguen siendo izq, centro y centro.
2. **No.** Sin poda, cada búsqueda genera todos los hijos, en el orden que sea: 4, 11 y 15.

Poner primero la jugada lista solo sirve si la búsqueda puede saltarse algo. Eso es lo que trae alfa-beta.
:::

---

**Pasar a alfa-beta.**

**Piensa: si la búsqueda nueva ya sabe cuál fue la mejor jugada de la anterior, ¿cómo puede ahorrar trabajo?**

Probándola primero. Con alfa-beta, una buena jugada probada primero **sube $\alpha$ pronto** y las demás se podan antes; lo viste en [[alfa-beta-como-algoritmo|Alfa-beta como algoritmo]].

Para aprovecharlo, se abre la línea 5 de la versión corta: en vez de una sola llamada a DECIDIR-CON-CORTE, el ciclo sobre los hijos de la raíz queda a la vista. Ahí entran cuatro cambios, y los números de línea son los del bloque completo. Los nombres nuevos:

- **$\alpha$:** lo que MAX ya asegura en la raíz **en el árbol cortado a esa profundidad**, durante la búsqueda en curso: hace de `mejor_valor`.
- **`mejor_jugada`:** la mejor de la búsqueda **en curso**, como en DECIDIR.
- **$w$:** lo que devuelve un hijo de la raíz.

El bloque completo va primero: PROFUNDIZACIÓN-ITERATIVA, en las líneas 1–13, y su auxiliar, ALFA-BETA-CON-CORTE, en las líneas 14–32. Debajo, los cuatro cambios lo recorren de uno en uno.

```text
INPUT   un estado s donde mueve MAX; las
        reglas S_F, Pl, A, T y U; una
        función EVAL; y un reloj.
        No recibe el grafo.
OUTPUT  una jugada de A(s), la mejor de la
        última búsqueda completa.

 1 function PROFUNDIZACIÓN-ITERATIVA(s)
     # respaldo: siempre hay algo que entregar
 2   jugada ← la primera jugada de A(s)
 3   d ← 1
     # cada vuelta, una búsqueda más honda
 4   while quede tiempo
 5     α ← −∞ ; mejor_jugada ← jugada
       # la anterior primero: α sube pronto
 6     for each a in A(s), jugada primero
 7       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, +∞)
         # a medias no sirve: va la anterior
 8       if el tiempo se acabó: return jugada
 9       if w = 100: return a  # gana seguro
10       if w > α: α ← w ; mejor_jugada ← a
11     jugada ← mejor_jugada   # ya terminó
12     d ← d + 1
13   return jugada

14 function ALFA-BETA-CON-CORTE(s, d, α, β)
15   if s ∈ S_F: return 100 · U(s)
16   if d = 0: return EVAL(s)  # se estima
17   if Pl(s) = MAX
18     v ← −∞
19     for each a in A(s)
20       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, β)
21       v ← max(v, w)
22       if v ≥ β: return v    # corte beta
23       α ← max(α, v)
24     return v
25   else
26     v ← +∞
27     for each a in A(s)
28       w ← ALFA-BETA-CON-CORTE(
               T(s, a), d − 1, α, β)
29       v ← min(v, w)
30       if v ≤ α: return v    # corte alfa
31       β ← min(β, v)
32     return v
```

**Cambio 1 · Valorar cada hijo con alfa-beta.** La raíz recorre sus hijos como DECIDIR-ALFA-BETA. La línea 5 pone ${\alpha=-\infty}$. La línea 7 valora cada hijo con ALFA-BETA-CON-CORTE y le pasa la ventana ${(\alpha,+\infty)}$: el hijo recibe lo que la raíz ya asegura. Si ${w>\alpha}$, la línea 10 sube $\alpha$ y anota la jugada en `mejor_jugada`.

**Cambio 2 · La jugada anterior primero.** La línea 6 recorre $A(s)$ empezando por `jugada`, la que dejó lista la búsqueda anterior. Sin poda, el orden no cambiaba nada. Con alfa-beta, si esa jugada es buena, $\alpha$ sube con el primer hijo y los demás se podan antes.

**Cambio 3 · El reloj entre dos hijos.** La versión corta miraba el reloj solo al terminar cada búsqueda. La línea 8 lo mira tras cada hijo de la raíz. Si se acabó, la búsqueda en curso no cuenta y se entrega `jugada`.

**Cambio 4 · La salida con 100.** Si un hijo devuelve 100, gana seguro y no hay nada mejor que buscar: la línea 9 lo entrega en ese momento.

El mismo procedimiento en Python, línea por línea. El reloj es una función, `queda_tiempo()`, que dice si sigue habiendo tiempo. El número entre paréntesis es la línea del pseudocódigo de arriba:

```python
from math import inf

# Las reglas: es_final(s), pl(s), acciones(s),
# transicion(s, a), utilidad(s) y evaluar(s),
# que es EVAL. pl(s) da "MAX" o "MIN".

def profundizacion_iterativa(s):   # (1)
    jugada = acciones(s)[0]        # (2)
    d = 1                          # (3)
    while queda_tiempo():          # (4)
        alfa = -inf                # (5)
        mejor_jugada = jugada
        # (6) La jugada anterior va primero.
        resto = [a for a in acciones(s)
                 if a != jugada]
        for a in [jugada] + resto:
            # (7) Le quedan d - 1 jugadas.
            w = alfa_beta_con_corte(
                transicion(s, a),
                d - 1, alfa, inf)
            # (8) A medias: se descarta.
            if not queda_tiempo():
                return jugada
            # (9) Victoria asegurada.
            if w == 100:
                return a
            # (10) Mejor que lo visto.
            if w > alfa:
                alfa = w
                mejor_jugada = a
        jugada = mejor_jugada      # (11)
        d = d + 1                  # (12)
    return jugada                  # (13)

# (14) El alfa-beta de la clase 2, con d.
def alfa_beta_con_corte(s, d, alfa, beta):
    if es_final(s):                # (15)
        return 100 * utilidad(s)
    if d == 0:                     # (16) EVAL
        return evaluar(s)
    if pl(s) == "MAX":             # (17)
        v = -inf                   # (18)
        for a in acciones(s):      # (19)
            w = alfa_beta_con_corte(  # (20)
                transicion(s, a),
                d - 1, alfa, beta)
            v = max(v, w)          # (21)
            if v >= beta:          # (22) beta
                return v
            alfa = max(alfa, v)    # (23)
        return v                   # (24)
    else:                          # (25)
        v = inf                    # (26)
        for a in acciones(s):      # (27)
            w = alfa_beta_con_corte(  # (28)
                transicion(s, a),
                d - 1, alfa, beta)
            v = min(v, w)          # (29)
            if v <= alfa:          # (30) alfa
                return v
            beta = min(beta, v)    # (31)
        return v                   # (32)
```

**Lo que queda igual y lo que viene de otro lado:**

- **Se quedan igual** las líneas 2, 3, 4, 12 y 13: son las 2, 3, 4, 8 y 9 de la versión corta. La 11, `jugada ← mejor_jugada`, es su línea 7.
- **Las líneas 5, 7 y 10 son DECIDIR-ALFA-BETA** (sus líneas 2, 4 y 5), y la 6 es su línea 3 con otro orden.
- **La línea 8 se pasa del tiempo** si un hijo tarda mucho: espera a que ese hijo termine. Un programa real mira el reloj también por dentro.
- **La línea 9 no se confunde con una estimación.** Como $|\mathrm{EVAL}|<M$ en todo estado que no es final, un 100 solo viene de finales ganados. En la posición de la clase, $|\mathrm{EVAL}|$ nunca pasa de 36.

Las líneas 14–32 son el [[alfa-beta-como-algoritmo|ALFA-BETA de la clase 2]] con lo de [[cortar-y-evaluar|Cortar y evaluar]]. La tabla pone cada línea junto a la suya:

::: table {#jue-c3-lineas-alfa-beta title="ALFA-BETA-CON-CORTE contra el ALFA-BETA de la clase 2"}
| Aquí | Clase 2 | Qué cambia |
|---|---|---|
| 14 | 7 | recibe $d$ |
| 15 | 8 | el final vale ${100\cdot U}$ |
| 16 | — | nueva: con ${d=0}$ se estima |
| 17–⁠32 | 9–⁠24 | nada, salvo ${d-1}$ en 20 y 28 |
:::

- **Por la línea 16, todo queda corrido en uno:** el corte beta, su 14, es aquí la 22; el corte alfa, su 22, es aquí la 30.

::: remark {#jue-c3-entrega-iterativa title="Qué entrega y cuándo termina"}
PROFUNDIZACIÓN-ITERATIVA siempre devuelve una jugada de $A(s)$: la línea 2 la pone antes de buscar. Lo que devuelve es la jugada de la última búsqueda completa, con el mayor valor con corte de esa $d$, o una jugada que gana seguro (línea 9).

Termina cuando un hijo gana seguro (línea 9) o cuando se acaba el reloj (línea 8 o 4). Si ninguna jugada gana, la 9 nunca actúa. Cuando $d$ ya alcanza todos los finales, cada vuelta repite la misma búsqueda: gasta el tiempo, pero no cambia la jugada.

Ojo: este pseudocódigo solo mira el reloj entre búsquedas (línea 4) y entre hijos de la raíz (línea 8). ALFA-BETA-CON-CORTE no recibe el reloj, así que un hijo que tarda mucho puede pasarse del límite. Un plazo estricto pide que la búsqueda recursiva también mire el reloj y abandone la búsqueda en curso.
:::

::: exercise {#jue-c3-ej-linea title="Señala qué línea actúa"}
En la posición de la clase, el reloj se acaba durante la búsqueda con ${d=2}$. Ya se valoró $\text{d2}\textbf{x}\text{c3}$, que va primero, y faltan las otras dos jugadas.

1. ¿Qué línea actúa y qué jugada se entrega?
2. ¿Por qué no basta con devolver `mejor_jugada` en ese momento?
:::

::: hint {#jue-c3-pista-linea-1 of="jue-c3-ej-linea" title="Sigue las líneas en orden"}
Tras la línea 7, ¿cuál es la primera que mira el reloj? Para la parte 2: ¿en qué línea recibe su valor cada una de las dos variables, y cuántas jugadas se habían valorado cuando eso pasó?
:::

::: answer {#jue-c3-resp-linea of="jue-c3-ej-linea"}
1. Actúa la **línea 8** y entrega `jugada`, la de la última búsqueda completa: con ${d=1}$ era **$\text{d2}\textbf{x}\text{c3}$**.
2. `mejor_jugada` solo compara las jugadas ya valoradas en esta búsqueda; las que faltan podrían ser mejores. Aquí todavía tiene lo que le puso la línea 5, porque la línea 8 corre antes que la 10. Las dos variables dicen $\text{d2}\textbf{x}\text{c3}$, pero $\text{d2}\textbf{-}\text{d3}$, la que gana, estaba sin valorar.

   Entregar `jugada` es lo simple y seguro, no lo único: los programas reales usan la de la búsqueda a medias si ya superó a la anterior, que prueban primero.
:::

---

**Recorrido: la tercera búsqueda en el árbol de resultados.**

**Piensa: con ${d=3}$, centro va primero. ¿Qué podan I y D con lo que centro ya aseguró?**

Casi todo lo que les queda. Las dos primeras búsquedas son cortas:

- **Con ${d=1}$**, R ve 60, 20 y 10: deja lista izq, con 4 nodos.
- **Con ${d=2}$**, izq ya iba primero en el orden dado. I mira sus dos finales y vale ${-100}$; centro vale 10. D llega con ${\alpha=10}$ y su primera hoja, d1, vale ${-100}$: corte alfa, y d2 y d3 no se generan. Deja lista centro, con 9 nodos.

La tercera búsqueda prueba centro primero, luego izq y der. Dentro de C, primero C1. Cada tramo va en dos tablas con el mismo número de fila: dónde está la búsqueda y qué números maneja.

- **línea · pila:** la línea que corre y el camino desde R al nodo activo.
- **$(\alpha,\beta)$:** la ventana del nodo activo **al terminar** la fila, como en la clase 2.
- **$v$:** el de ese nodo. En las filas de R, su $\alpha$, que hace de `mejor_valor`.
- **$w$:** lo que acaba de devolver un hijo; entre paréntesis, cuál. Una hoja va por su $M\cdot U$.
- **compara:** la comparación de la fila. En un nodo de MAX, ${v\ge\beta}$, y un «sí» es un corte beta. En uno de MIN, ${v\le\alpha}$, y un «sí» es un corte alfa. En R, ${w>\alpha}$ de la línea 10: un «sí» no poda nada, solo sube $\alpha$.
- **`mejor_jugada`** vale centro en las 18 filas: la línea 5 la pone así y ningún hijo la supera.

**Tramo 1 · C1 devuelve 0.**

::: table {#jue-c3-t-traza-d3-donde title="Búsqueda con d = 3, filas 1–6: dónde está"}
| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 1 | 5 · R | (−∞,+∞) |
| 2 | 26 · R›C | (−∞,+∞) |
| 3 | 18 · R›C›C1 | (−∞,+∞) |
| 4 | 20–23 · R›C›C1 | (0,+∞) |
| 5 | 20–23 · R›C›C1 | (0,+∞) |
| 6 | 28–31 · R›C | (−∞,0) |
:::

::: table {#jue-c3-t-traza-d3-numeros title="Búsqueda con d = 3, filas 1–6: qué números maneja"}
| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 1 | −∞ |  |  |
| 2 | +∞ |  |  |
| 3 | −∞ |  |  |
| 4 | 0 | 0 (c1a) | 0≥+∞: no |
| 5 | 0 | −100 (c1b) | 0≥+∞: no |
| 6 | 0 | 0 (C1) | 0≤−∞: no |
:::

- **Fila 1:** la línea 5 pone ${\alpha=-\infty}$ y `mejor_jugada ← jugada`: centro, la que dejó lista ${d=2}$.
- **Filas 4 y 5:** C1 es de MAX y sus dos hijos son finales: c1a, 0, y c1b, ${-100}$. Se queda con ${\max(0,-100)=0}$.
- **Fila 6:** C es de MIN y recibe 0 de C1. Su $\beta$ baja a 0: la ventana de C pasa a ser ${(-\infty,0)}$, y con ella llama a C2.

**Tramo 2 · Centro asegura 0.**

| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 7 | 18 · R›C›C2 | (−∞,0) |
| 8 | 20–22 · R›C›C2 | (−∞,0) |
| 9 | 28–31 · R›C | (−∞,0) |
| 10 | 7–10 · R | (0,+∞) |

| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 7 | −∞ |  |  |
| 8 | 100 | 100 (c2a) | 100≥0: sí |
| 9 | 0 | 100 (C2) | 0≤−∞: no |
| 10 | 0 | 0 (C) | 0>−∞: sí |

- **Fila 8:** C2 es de MAX y su primera hoja, c2a, vale 100. Como ${100\ge0}$, corte beta en la línea 22: c2b no se genera. La línea 23 no llega a correr, así que la ventana de C2 sigue en ${(-\infty,0)}$.
- **Fila 9:** C2 devuelve 100, y C se queda con ${\min(0,100)=0}$.
- **Fila 10:** ${0>-\infty}$, así que la línea 10 sube $\alpha$ a 0. Mejora lo asegurado, pero no poda nada.

Al cerrar el tramo 2, C vale 0, C1 vale 0 y C2 devolvió 100, con la hoja c2b podada.

**Tramo 3 · Izq y der, con alfa en 0.**

::: exercise {#jue-c3-ej-traza-d3 title="Completa el tramo 3 de la búsqueda con d = 3"}
Sigue la misma búsqueda desde la fila 11: R prueba izq y luego der. Dentro de I, primero i1.

| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 11 | 26 · R›I | ? |
| 12 | 28–31 · R›I | ? |
| 13 | 28–30 · R›I | (0,100) |
| 14 | 7–10 · R | (0,+∞) |
| 15 | 26 · R›D | ? |
| 16 | 28–30 · R›D | ? |
| 17 | 7–10 · R | (0,+∞) |
| 18 | 11–12 · R | ? |

| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 11 | +∞ |  |  |
| 12 | ? | 100 (i1) | ? |
| 13 | ? | −100 (ix) | ? |
| 14 | 0 | −100 (I) | ? |
| 15 | +∞ |  |  |
| 16 | −100 | −100 (d1) | ? |
| 17 | ? | −100 (D) | ? |
| 18 | ? |  |  |

1. Llena los «?».
2. ¿Qué hojas de I y de D no se generan? Contando los tramos 1 y 2, ¿cuántos nodos genera la búsqueda?
3. ¿Qué devuelven I y D: su valor, o un número que solo lo acota?
:::

::: hint {#jue-c3-pista-traza-d3-1 of="jue-c3-ej-traza-d3" title="Qué compara cada fila"}
En cada fila de compara, ¿de quién es el nodo: de MAX, de MIN o es R? ¿Con qué número compara su $v$ o su $w$, y en qué línea?
:::

::: answer {#jue-c3-resp-traza-d3 of="jue-c3-ej-traza-d3"}
En negrita, lo que era «?».

| # | línea · pila | $(\alpha,\beta)$ |
|---:|---|---|
| 11 | 26 · R›I | **(0,+∞)** |
| 12 | 28–31 · R›I | **(0,100)** |
| 13 | 28–30 · R›I | (0,100) |
| 14 | 7–10 · R | (0,+∞) |
| 15 | 26 · R›D | **(0,+∞)** |
| 16 | 28–30 · R›D | **(0,+∞)** |
| 17 | 7–10 · R | (0,+∞) |
| 18 | 11–12 · R | **(0,+∞)** |

| # | $v$ | $w$ | compara |
|---:|---:|---|---|
| 11 | +∞ |  |  |
| 12 | **100** | 100 (i1) | **100≤0: no** |
| 13 | **−100** | −100 (ix) | **−100≤0: sí** |
| 14 | 0 | −100 (I) | **−100>0: no** |
| 15 | +∞ |  |  |
| 16 | −100 | −100 (d1) | **−100≤0: sí** |
| 17 | **0** | −100 (D) | **−100>0: no** |
| 18 | **0** |  |  |

1. **I y D son de MIN** y llegan con ${\alpha=0}$. En I, la primera hoja, i1, vale 100 y no poda: solo baja $\beta$ a 100. La segunda, ix, vale ${-100}$ y cumple ${v\le\alpha}$: corte alfa en la línea 30. En D, la primera hoja ya poda. En R, ninguno de los dos ${-100}$ supera 0, así que $\alpha$ y `mejor_jugada` no cambian.

   Las ventanas guardan lo último que corrió: I devuelve en la línea 30 sin bajar $\beta$ a ${-100}$, y D, sin tocar su $+\infty$.
2. I genera sus dos hojas: el corte alfa llega cuando ya no le quedan. De D no se generan d2 ni d3; en el tramo 2 tampoco se generó c2b. Se generan **12** nodos: R, C, C1, c1a, c1b, C2, c2a, I, i1, ix, D y d1.
3. **Cotas.** I y D devuelven ${-100}$, y la ventana solo certifica que valen **a lo más** eso. Basta para saber que no superan a centro. Aquí, además, ese techo demuestra el valor: ningún pago baja de ${-100}$.
:::

> **▶ [Recorre las tres búsquedas paso a paso](../_assets/traza_arbol_t.html#iterativa)** — ${d=1}$, 2 y 3 seguidas, con la jugada anterior primero.

La tabla resume las tres búsquedas.

::: table {#jue-c3-t-iterativa title="Cada búsqueda de la profundización iterativa en el árbol de resultados"}
| $d$ | orden: $w$ | Lista |
|---|---|---|
| 1 | **I** 60 · C 20 · D 10 | izq |
| 2 | **I** −100 · C 10 · D ≤−100 | centro |
| 3 | **C** 0 · I ≤−100 · D ≤−100 | centro |
:::

- **Cómo leer la tabla:** «orden: $w$» da los hijos de R en el orden en que se prueban, con el $w$ que devuelve cada uno. En negrita, el que va primero: la primera jugada legal con $d=1$, la jugada lista de la búsqueda anterior después.
- **Nodos generados:** 4, 9 y 12, que suman 25. Sin poda eran 30 (4, 11 y 15).
- **Podas:** con ${d=1}$, ninguna. Con ${d=2}$, un corte alfa en D. Con ${d=3}$, un corte beta en C2 y dos cortes alfa, en I y en D; el de I no ahorra nada.
- **${d=1}$ deja lista la trampa**, izq, y por la línea 6 izq va primero con ${d=2}$. Ahí ya se ve que vale ${-100}$: la búsqueda corrige la jugada.

::: figure {#jue-c3-t-fig-iterativa title="Profundización iterativa en el árbol de resultados: izq con d = 1, centro desde d = 2"}
![Tres búsquedas de alfa-beta con corte sobre el árbol de resultados, finales en 100·U, cada una con la jugada que dejó lista la anterior primero. Con d = 1, la raíz prueba izq, centro y der, ve sus EVAL 60, 20 y 10, genera 4 nodos y deja lista izq, con 60. Con d = 2 prueba izq, centro y der; I vale −100, C vale 10 y D se poda tras d1; genera 9 nodos y deja lista centro, con 10. Con d = 3 prueba centro primero y ve 0; poda c2b con un corte beta en C2 y d2 y d3 con un corte alfa en D; I y D devuelven una cota. Genera 12 nodos y deja lista centro, con 0. En total, 25 nodos](../_assets/jue-t-iterativa.svg)
:::

**En la posición de la clase.** Con ${d=3}$ se prueba primero $\text{d2}\textbf{-}\text{d3}$, la jugada que dejó lista ${d=2}$. Vale 100, y la línea 9 la entrega sin mirar las otras dos. Los valores $-9$ y 1 de @jue-c3-horizonte-valores están ahí para comparar, pero el programa ya no los calcula.

Las dos tablas juntan todas las cuentas de nodos de la clase. En el árbol de resultados, el orden fijo es izq, centro, der.

En la posición de la clase, el orden fijo va por la fila de la casilla de origen, de la 1 a la 4, y dentro de la fila por columna, de a a d. En cada peón va primero el avance y luego las capturas. Para Blancas da $\text{a1}\textbf{-}\text{a2}$, $\text{d2}\textbf{-}\text{d3}$, $\text{d2}\textbf{x}\text{c3}$. La iterativa pone primero la jugada lista y sale con 100 (línea 9).

::: table {#jue-c3-nodos-generados title="Nodos generados en el árbol de resultados, por búsqueda"}
| $d$ | sin poda | α-β fijo | iterativa |
|---|---:|---:|---:|
| 1 | 4 | 4 | 4 |
| 2 | 11 | 9 | 9 |
| 3 | 15 | 12 | 12 |
| Total | 30 | 25 | 25 |
:::

::: table {#jue-c3-nodos-generados-posicion title="Nodos generados en la posición de la clase, por búsqueda"}
| $d$ | sin poda | α-β fijo | iterativa |
|---|---:|---:|---:|
| 1 | 4 | 4 | 4 |
| 2 | 12 | 12 | 10 |
| 3 | 33 | 22 | 9 |
| Total | 49 | 38 | 23 |
:::

«α-β fijo» es alfa-beta con el orden fijo y sin la salida en 100.

- **En el árbol de resultados, la iterativa no ahorra frente a alfa-beta con orden fijo:** los dos generan 4, 9 y 12. Con ${d=2}$, la lista izq ya iba primera. Con ${d=3}$, poner centro primero no salva nada, porque I mira sus dos hojas en cualquier caso: i1 vale 100 y no poda.
- **En la posición de la clase sí ahorra:** 23 contra 38. Casi todo el ahorro está en ${d=3}$, 9 contra 22: la jugada que va primero gana, y la línea 9 sale sin mirar más.

#### 2 · Elección: qué jugada juega

Por reloj, la jugada de la **última búsqueda completa**; si no terminó ninguna, el respaldo.

::: table {#jue-c3-tab-eleccion-reloj title="Qué jugada entrega el corte, según la versión"}
| Versión | Jugada que entrega | Cuándo |
|---|---|---|
| Por nivel | Mayor valor con corte | Al terminar |
| Por reloj | Última búsqueda completa | Al vencer el plazo |
| Por reloj, con $+M$ | Esa jugada | Al encontrarla |
:::

- **Un empate conserva el orden de esa búsqueda:** solo cambia de jugada si otra devuelve un valor estrictamente mayor. Como la anterior va primero, conserva los empates.
- **La salida con $+M$ no rompe la regla:** ya demostró una victoria, y ninguna otra jugada puede superarla.
- **El reloj va antes que la salida:** si la línea 8 ve el plazo vencido, entrega la jugada anterior aunque el hijo haya devuelto 100.

#### 3 · Propiedades

- **Número que da:** el valor con corte de la última búsqueda completa. Con alfa-beta, solo el de la jugada elegida es exacto en ese árbol; los demás pueden ser cotas.
- **Usa EVAL:** sí, en los nodos de corte; los finales valen $M\cdot U$, en la misma escala.
- **Garantía:** no garantiza $V$, salvo si la última búsqueda completa llega a los finales sin evaluar. Entonces da $M\cdot V$.
- **Se puede interrumpir:** sí (*anytime*): tiene un respaldo legal desde el inicio, y la jugada de una búsqueda completa desde que termina $d=1$.
- **Complejidad:** cada búsqueda cuesta lo de alfa-beta con corte, entre $O(b^{d/2})$ y $O(b^d)$. Repetir las anteriores cuesta poco si la búsqueda crece parejo (@jue-c3-costo-iterativa). Sin tabla de transposición, la memoria es $O(bd)$; con tabla, crece con lo que se guarde.
- **Frente a los demás:** juega con lo que dé el tiempo y aprovecha cada búsqueda para ordenar la siguiente. Es lo que usan los programas de ajedrez de torneo, como Deep Blue.
- **Supuestos:** los del corte y de alfa-beta. La salida con $+M$ usa que $M$ es el mayor pago posible para MAX. Con suma no constante o más jugadores hacen falta pagos vectoriales y $\max^n$; ni la poda ordinaria ni esa salida se trasladan directo.

::: remark {#jue-c3-costo-iterativa title="Costo de la profundización iterativa"}
Si cada búsqueda es unas $B$ veces más grande que la anterior (${B>1}$, un crecimiento parejo) y la última completa llega a $d$ en la raíz, la de $d$ cuesta del orden de $B^d$, y todas las anteriores juntas suman

$$B+B^2+\dots+B^{d-1}=\frac{B^d-B}{B-1}<\frac{B^d}{B-1}.$$

Es cerca de ${1/(B-1)}$ de la última. El tiempo total es

$$\text{tiempo}=O\!\left(B^d\cdot\frac{B}{B-1}\right)=O(B^d),$$

el mismo orden que una sola búsqueda a profundidad $d$.

| Crecimiento | Lo que se repite | Total |
|---|---|---|
| $B=10$ | $1/9$, cerca de 11 % | $10/9$ de la última |
| $B=2$ | casi otra búsqueda | casi el doble |

Sin poda, en un árbol uniforme con exactamente $b>1$ jugadas en cada estado, ${B=b}$. Con alfa-beta, el crecimiento depende también del orden y de las ramas podadas: no se deduce $B=b$ solo de la ramificación.

Sin ese crecimiento, repetir puede costar más. Que haya a lo más $b$ jugadas por estado no lo asegura: si tras la raíz casi todo es forzado, cada búsqueda agrega apenas unos nodos a la anterior, y las anteriores juntas pueden costar varias veces la última.
:::

Cuando la búsqueda crece parejo, la última domina el costo. Repetir las otras es casi gratis cuando $B$ es grande.

#### 4 · Casos borde

- **El reloj vence antes de terminar $d=1$:** entrega el respaldo, la primera jugada legal.
- **Una búsqueda a medias no se usa:** puede no haber revisado la mejor jugada.
- **El último hijo regresa con el reloj vencido:** la línea 8 entrega la jugada anterior, porque la 11 todavía no guardó la nueva.
- **El reloj no es estricto:** se mira entre hijos de la raíz, y un hijo lento se pasa del plazo.
- **Crecimiento no parejo:** si cada búsqueda agrega poco, repetir puede costar varias veces la última.
- **Un reloj corto entrega la trampa:** en la clase, $\text{d2}\textbf{x}\text{c3}$; en el árbol de resultados, izq.
- **Encontrar $+M$ permite terminar** solo porque $M$ es la cota global de los pagos y ninguna $\mathrm{EVAL}$ la alcanza. Un promedio o una estimación alta no bastan.
- **Una sola jugada legal:** el respaldo ya es esa jugada; buscar solo afina su valor.
- **Finales a distintas profundidades:** cada uno vale $M\cdot U$ al reconocerse; $\mathrm{EVAL}$ solo sustituye estados no finales.
- **`mejor_jugada` empieza en la jugada lista, no en «ninguna»:** si la ventana de la raíz abriera en $-M$ y todas las jugadas perdieran, ninguna superaría a $\alpha$ y la raíz se quedaría sin jugada.

#### Intuición

- **El reloj decide la calidad de la jugada.** El mismo programa captura y pierde con poco tiempo, y gana con un poco más.
- **Cada búsqueda prepara la siguiente.** La jugada lista va primero y sube $\alpha$ pronto; repetir lo de arriba cuesta poco.
- **Más hondo no quita el horizonte.** Cada búsqueda lo mueve una jugada más abajo; solo desaparece al llegar a todos los finales.

#### Ejercicios

::: exercise {#jue-c3-ej-costo title="Calcula lo que se repite"}
Usa las barras de @jue-c3-fig-profundizacion: 4, 12 y 33 nodos.

1. ¿Cuántos nodos genera en total profundizar hasta terminar ${d=3}$?
2. ¿Cuántos de ellos son repetición? ¿Es más o menos que la mitad de la última búsqueda?
:::

::: hint {#jue-c3-pista-costo-1 of="jue-c3-ej-costo" title="Qué se habría hecho igual"}
Un programa que supiera de antemano que llega a ${d=3}$, ¿qué búsquedas habría hecho? Lo demás es lo que se repite.
:::

::: answer {#jue-c3-resp-costo of="jue-c3-ej-costo"}
1. ${4+12+33=}$ **49** nodos.
2. Se repiten las búsquedas con ${d=1}$ y ${d=2}$: ${4+12=}$ **16** nodos, **menos de la mitad** de los 33 de la última. La cuenta de ${1/(B-1)}$ es una guía, no una ley: supone que cada búsqueda crece parejo. Aquí no crece por el máximo, ${b=5}$ jugadas. Con el crecimiento medido aquí en el último paso, ${33/12=2.75}$, da ${1/(2.75-1)\approx0.57}$, cerca de lo medido, ${16/33\approx0.48}$.
:::

**Piensa: si cambias el orden inicial de las jugadas, ¿qué cambia, la jugada que se entrega o lo que cuesta llegar a ella?**

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-ej-final-reloj title="Corre la iterativa con otro orden y un reloj"}
Mismo árbol de resultados y misma $\mathrm{EVAL}$ (I 60, C 20, D 10, C1 10, C2 50). Lo que cambia es el orden de $A(R)$: **der, centro, izq**. Así la línea 2 deja ${\text{jugada}=\text{der}}$. Dentro de C, primero C1, como siempre.

Dos simplificaciones. El reloj se mide en **nodos generados**, contando las tres búsquedas seguidas, raíz incluida en cada una. Y se mira solo en las líneas 4 y 8: se acaba cuando la cuenta llega al tope.

1. Corre PROFUNDIZACIÓN-ITERATIVA con ${d=1}$, 2 y 3. Para cada búsqueda, da el orden en que R prueba sus hijos, la jugada lista y los nodos generados.
2. ¿Dónde se poda con ${d=2}$, y con qué $\alpha$? Compáralo con el orden de la página.
3. ¿Cuántos nodos suman las tres búsquedas? Compáralo con los 25 de la página. ¿Por qué?
4. Con un reloj de 10 nodos, ¿qué línea actúa y qué jugada se entrega? ¿Y con uno de 20?
:::

::: hint {#jue-c3-pista-final-reloj-1 of="jue-c3-ej-final-reloj" title="Pista 1 · Qué va primero"}
Antes de cada búsqueda, ¿qué jugada está lista y dónde la pone la línea 6? Después, para cada hijo de R, ¿con qué $\alpha$ llega? Ojo con el ${\le}$ de la línea 30.
:::

::: hint {#jue-c3-pista-final-reloj-2 of="jue-c3-ej-final-reloj" title="Pista 2 · Revisa tu borrador"}
Comprueba tu propuesta con dos preguntas. ¿Cuántos nodos llevas en total cada vez que un hijo de R devuelve su $w$? Cuando la cuenta llega al tope, ¿la búsqueda en curso ya había terminado?
:::

::: answer {#jue-c3-resp-final-reloj of="jue-c3-ej-final-reloj" title="Respuesta · Las tres búsquedas y los dos relojes"}
**1. Las tres búsquedas.**

| $d$ | Orden de R | Lista | Nodos |
|---|---|---|---:|
| 1 | der, centro, izq | izq | 4 |
| 2 | izq, der, centro | centro | 9 |
| 3 | centro, der, izq | centro | 12 |

Con ${d=1}$, R ve 10, 20 y 60: queda izq, la trampa. Con ${d=2}$, izq va primero y vale ${-100}$; centro vale 10. Con ${d=3}$, centro va primero y vale 0; der e izq quedan debajo.

**2. La poda con ${d=2}$.** D llega con ${\alpha=-100}$, porque solo se valoró I. Su primera hoja, d1, vale ${-100}$, y ${-100\le-100}$: corte alfa, d2 y d3 no se generan. Con el orden de la página también se podaban, pero con ${\alpha=10}$, porque centro iba antes que der.

**3. El total.** **25** nodos (4, 9 y 12), igual que en la página, con la misma jugada entregada, centro. Desde ${d=2}$, la línea 6 pone primero la jugada lista, que no depende del orden inicial: izq con ${d=2}$ y centro con ${d=3}$. Las demás conservan su orden relativo, y en este árbol eso no cambia ninguna poda.

**4. El reloj.** Con 10 nodos: la primera búsqueda termina en 4. La segunda llega a 8 tras izq, y a 10 tras der. La línea 8 ve el reloj agotado y entrega **izq**, de ${d=1}$: la trampa. Con 20 nodos: la segunda búsqueda termina en 13. La tercera llega a 20 tras centro, y la línea 8 entrega **centro**, de ${d=2}$.

El orden inicial decidió el respaldo y el orden de ${d=1}$; desde ahí, la primera jugada de cada búsqueda la pone la anterior. Con poco tiempo, el reloj decide qué se entrega: un reloj corto entrega la trampa.
:::

---

## 4 · Recordar posiciones ya valoradas

**Piensa: si dos órdenes de jugadas llegan al mismo tablero, ¿hace falta valorarlo dos veces?**

No. Como en [[minimax-como-algoritmo|minimax]], un estado al que se llega por varios caminos —una **transposición**— no hace falta valorarlo dos veces. El estado incluye el turno: el mismo tablero con otro jugador por mover es otra entrada. Una **tabla de transposición** guarda cada estado ya valorado; el Python de esta página no la incluye.

Con corte y con poda, guardar «el estado y su valor» no basta. Cada entrada guarda tres cosas:

- **El número** que devolvió la búsqueda.
- **La profundidad que quedaba**, $d$. Un número calculado con ${d=1}$ no sirve a una búsqueda que llega con ${d=3}$: miró menos. Los programas lo reutilizan si se calculó con al menos la profundidad que queda ahora.

  Si se calculó con más, ya no es exactamente el valor con corte de esta búsqueda, sino uno que miró más hondo. En el árbol de resultados, C vale 20 sin nada debajo, 10 con un nivel y 0 con dos. Se acepta porque mirar más hondo suele estimar mejor, aunque el resultado ya no es exactamente $V_d$ y la jugada puede cambiar frente a una búsqueda sin tabla.
- **Qué tipo de número es**, según la ventana de entrada $(\alpha_0,\beta_0)$, con $\alpha_0<\beta_0$, y el $v$ que devolvió el nodo.

| Si | Tipo | Qué garantiza |
|---|---|---|
| $\mathbf{\alpha_0<v<\beta_0}$ | valor | $V_d(s)=v$ |
| $\mathbf{v\ge\beta_0}$ | piso | $V_d(s)\ge v$ |
| $\mathbf{v\le\alpha_0}$ | techo | $V_d(s)\le v$ |

Un **valor** cae dentro de la ventana y es el valor con corte a la profundidad con que se calculó. Un **piso** dice «al menos»; un **techo**, «a lo más».

Ojo con los nombres: piso y techo describen el número guardado, no la ventana. $\alpha$ y $\beta$ son alternativas del camino; un nodo que toca $\beta_0$ deja guardado un piso.

El tipo se lee de la ventana **de entrada**, no de los extremos que el nodo movió ni de si podó. Un nodo puede devolver una cota sin haber podado él: basta con que poden sus hijos y le devuelvan cotas.

::: table {#jue-c3-transposicion-iterativa title="Tipo de cada número en la búsqueda con d = 3, centro primero"}
| Nodo | Ventana al llegar | $v$ | Tipo |
|---|---|---:|---|
| C | (−∞,+∞) | 0 | valor |
| C1 | (−∞,+∞) | 0 | valor |
| C2 | (−∞,0) | 100 | piso |
| I | (0,+∞) | −100 | techo |
| D | (0,+∞) | −100 | techo |
:::

Un techo de ${-100}$ en I no dice «I vale ${-100}$»: dice «a lo más ${-100}$». Sirve para descartar I en cualquier búsqueda donde MAX ya asegure ${-100}$ o más. Aquí, además, demuestra el valor, porque ningún pago baja de ${-100}$: eso no lo dice la ventana, lo dice la escala.

**Caso borde: guardar una cota como si fuera un valor.** La ventana solo certifica techos y pisos. Aquí guardarlos como exactos no falla, porque las tres cotas tocan un extremo de la escala, ${-100}$ o 100, y eso las demuestra. Con un techo que no toca el extremo, una búsqueda posterior usaría como exacto un número que solo acota, y podría elegir mal.

::: exercise {#jue-c3-ej-clase title="Clasifica lo que se guarda"}
Ahora alfa-beta con ${d=3}$ y el orden fijo: R prueba izq, centro, der. I llega con ${(-\infty,+\infty)}$ y devuelve ${-100}$. C2 llega con $(-100,0)$ y devuelve 100. D llega con ${(0,+\infty)}$ y devuelve ${-100}$.

1. ¿Qué tipo de número guarda la tabla para I, para C2 y para D?
2. Compara I con la tabla de arriba. ¿Por qué cambia su tipo?
:::

::: hint {#jue-c3-pista-clase-1 of="jue-c3-ej-clase" title="Con cuál extremo"}
Para cada nodo, ¿su $v$ cae dentro de la ventana, o toca o pasa uno de los extremos? ¿Cuál?
:::

::: answer {#jue-c3-resp-clase of="jue-c3-ej-clase"}
1. **I: valor**, porque ${-100}$ cae dentro de ${(-\infty,+\infty)}$. **C2: piso**, porque ${100\ge0}$. **D: techo**, porque ${-100\le0}$.
2. Con el orden fijo, I va primero y llega sin nada asegurado: su ${-100}$ es su valor. Con centro primero, I llega con ${\alpha=0}$, y la ventana solo certifica que su ${-100}$ es un techo; que también sea su valor lo demuestra la escala, no la ventana. **El mismo nodo, con el mismo número, cambia de tipo porque cambió la ventana con que se llamó.**
:::

---

**Punto de control:** deberías poder…

- **señalar** qué jugada queda detrás del horizonte en una posición de peones;
- **decir** si una posición de corte es quieta y **calcular** a mano su valor con quietud;
- **decir** qué entrega PROFUNDIZACIÓN-ITERATIVA si el reloj se acaba entre dos hijos de la raíz (línea 8) o si un hijo devuelve 100 (línea 9), y por qué la jugada lista va primero;
- **clasificar** un número guardado como valor, piso o techo según su ventana.

> [!NOTE]
> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, en el orden del curso.
>
> | Algoritmo | Qué número da |
> |---|---|
> | Minimax | $V$; lo garantiza |
> | Alfa-beta | $V$ en la raíz; lo garantiza |
> | Expectiminimax | El $V$ del juego con dado; lo garantiza |
> | Minimax con corte | Valor con corte; no garantiza $V$. Con todos los finales, da $M\cdot V$ |
> | **Búsqueda de quietud (estás aquí)** | **Valor con quietud; no garantiza $V$. Con todos los finales antes de activar la quietud, da $M\cdot V$** |
> | **Profundización iterativa (estás aquí)** | **Valor con corte de la última búsqueda; no garantiza $V$. Con todos los finales, da $M\cdot V$** |

## Lo que hay que llevarse

- **El horizonte es la línea donde se corta.** Con $d=1$, $\text{d2}\textbf{x}\text{c3}$ valía 13 porque la recaptura $\text{b4}\textbf{x}\text{c3}$, que la deja en 0, quedaba detrás. La forma clásica, que nombró Berliner en 1973: el programa aplaza una pérdida inevitable.
- **Subir la profundidad mueve el horizonte, no lo quita**, mientras el corte no llegue a todos los finales. Con $d=2$, $\text{d2}\textbf{-}\text{d3}$ vale 1 y la victoria, 100, sigue detrás.
- **La búsqueda de quietud** sigue solo las capturas desde los nodos de corte, y quedarse con $\mathrm{EVAL}$ es una aproximación, no una jugada. Con $d=1$ da ${-10}$, 2 y 0 en la clase, y elige $\text{d2}\textbf{-}\text{d3}$; en el árbol de resultados juega centro con 20. **Arregla la jugada, no el valor.**
- **La profundización iterativa** busca con ${d=1,2,3,\dots}$ y entrega lo mejor de la **última búsqueda completa**. Un reloj que se acaba durante ${d=2}$ entrega $\text{d2}\textbf{x}\text{c3}$, que pierde; durante ${d=3}$, $\text{d2}\textbf{-}\text{d3}$, que gana.
- **Repetir cuesta poco si crece parejo:** cerca de ${1/(B-1)}$ de la última búsqueda. En la clase, sin poda, 16 nodos contra 33. Si no crece parejo puede costar más: en el árbol de resultados, con alfa-beta y la jugada anterior primero, las dos primeras búsquedas suman 13 nodos contra 12 de la última.
- **La poda ahorra siempre; la jugada anterior primero, solo a veces:** en el árbol de resultados, 25 nodos contra 30 sin poda, y la iterativa empata con alfa-beta de orden fijo. En la clase, 23 contra 38 de alfa-beta fijo y 49 sin poda.
- **La tabla de transposición** guarda número, profundidad y tipo según la ventana: valor si ${\alpha_0<v<\beta_0}$, piso si ${v\ge\beta_0}$, techo si ${v\le\alpha_0}$, con $(\alpha_0,\beta_0)$ la ventana con que se llamó al nodo.

Continúa con [[simular-en-vez-de-evaluar|Simular partidas]].
