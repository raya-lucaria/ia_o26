---
id: elegir-el-algoritmo
title: Elegir el algoritmo
nav_title: Elegir el algoritmo
summary: "Dado un juego, cuatro preguntas eligen entre los siete algoritmos de la radiografía: si el árbol cabe, si hay dados, si hay una buena EVAL y si hay reloj. Con el juego real donde se usó cada uno, el número que sostiene su jugada y lo que suponen todos: dos jugadores, suma cero o constante, por turnos y todo a la vista."
status: ready
estimated_time: 30m
tags: [juegos, busqueda-adversarial, mcts]
---

# Elegir el algoritmo

**Dado un juego, ¿qué algoritmo uso?**

Depende de lo que el juego ofrece: si su árbol cabe, si tiene dados, si hay con qué estimar y cuánto tiempo hay. Al terminar podrás:

- **Ponerle nombre al número** que sostiene cada jugada: un valor exacto, un valor con corte o una estimación.
- **Elegir con dos tablas** cuál de los siete algoritmos conviene, qué le cuesta y en qué juego real se usó.
- **Recorrer un mapa de cuatro preguntas** en el árbol de resultados y en la posición de la clase.
- **Reconocer los cuatro supuestos** que comparten todos, y qué se usa cuando falla alguno.
- **Diagnosticar un juego nuevo** y justificar su algoritmo.

## Lo que traes

- **Siete algoritmos, un mapa.** En [[un-arbol-todos-los-algoritmos|la radiografía]] corrieron minimax, alfa-beta, expectiminimax, minimax con corte, Monte Carlo plano, Monte Carlo con actualización minimax y UCT. Cada uno tiene su ficha.
- **El valor exacto se mide desde MAX.** $V(s)$ supone que los dos juegan lo mejor, y $Q(s,a)=V(T(s,a))$ valora una jugada. Con dados, $V$ promedia el azar con sus probabilidades.
- **El valor con corte usa otra escala.** $V_d$ toma EVAL donde se corta y $M\cdot U$ en los finales, con $M=100$ y $|\mathrm{EVAL}|<M$. Estima $M\cdot V$.
- **La estimación lleva gorro.** $\widehat Q$ sale de partidas simuladas: en Monte Carlo plano estima $Q_{\text{azar}}$, lo que paga la jugada si los dos siguen al azar; en la actualización minimax y en UCT estima $Q$, con las condiciones de su ficha.
- **Solo $V$ es el valor del juego.** $Q_{\text{azar}}$ también es exacto, pero contesta otra pregunta.

> **El árbol de resultados, en tres líneas.** La raíz R es de MAX, con izq, centro y der hacia I, C y D, de MIN. Los finales valen $+1$ o $-1$, y hay un solo empate, $0$. Minimax juega centro con $V=0$.

> **Supuestos de esta página.** Los cuatro de toda la unidad: dos jugadores, suma cero (o constante), por turnos y todo a la vista. El azar, solo donde hay dados. La sección 4 los revisa uno por uno.

---

## 1 · Ponerle nombre a cada número

**Piensa: dos algoritmos devuelven $0$ en la raíz del árbol de resultados. ¿Dicen lo mismo?**

No necesariamente. Un $0$ puede ser el valor exacto, un valor con corte que vino de finales, o un promedio que coincide por casualidad. Antes de elegir un algoritmo hay que saber leer su número.

::: exercise {#jue-c3-cmp-ej-ponle-nombre title="Ponle nombre a cada número"}
Seis números que salieron del árbol de resultados. Para cada uno, di cuál es: $V$, valor con corte o $\widehat Q$. Di también si es el $V$ del juego sin dado. Las corridas con azar usan semilla 0, y UCT usa $c=1$.

1. $0$, de alfa-beta con los hijos al revés.
2. $60$, del corte a $d=1$.
3. $0$, de la profundización iterativa con $d=1,2,3$.
4. $1/3$, de expectiminimax con D como dado.
5. $0$, la $\widehat Q$ de centro tras 40 vueltas de UCT.
6. $0$, la $\widehat Q$ de centro tras 10 partidas de la actualización minimax.
:::

::: hint {#jue-c3-cmp-pista-ponle-nombre-1 of="jue-c3-cmp-ej-ponle-nombre" title="Qué algoritmo lo dio"}
¿Qué número da ese algoritmo, según la tabla «Qué supone cada número» de la radiografía? ¿Llegó a los finales esa vez? ¿En qué escala está su número?
:::

::: answer {#jue-c3-cmp-resp-ponle-nombre of="jue-c3-cmp-ej-ponle-nombre"}
1. **$V$, y sí es el del juego.** Alfa-beta da en la raíz el mismo $V$ que minimax, en cualquier orden.
2. **Valor con corte; no.** Es $V_1(\text{R})=\mathrm{EVAL}(\text{I})$, en la escala $M\cdot U$ con $M=100$. Izq tiene $Q=-1$: ese $60$ no demuestra nada.
3. **Valor con corte; sí, esta vez.** Con $d=3$, todo lo que suma viene de finales: $V_3(\text{R})=100\,V(\text{R})=0$.
4. **$V$, pero de otro juego**: el que tiene un dado en D. Sin dado, $V=0$.
5. **$\widehat Q$; no.** Coincide con $Q$ por casualidad: a la vuelta 100 ya es $1/83$.
6. **$\widehat Q$, provisional; no.** Coincide con $Q=0$, pero debajo de C1 falta descubrir una hoja, e izq sigue sin visitar: desconocida, no cero.
:::

Leer el número dice qué tanto confiar en la jugada. Falta lo práctico: cuál algoritmo conviene, y en qué juego.

---

## 2 · Elegir por lo que tiene el juego

**Piensa: Deep Blue y AlphaGo vencieron a campeones humanos. ¿Por qué no usaron el mismo algoritmo?**

Porque sus juegos no ofrecen lo mismo. En ajedrez hay una estimación razonable que se escribe a mano: contar piezas, con su valor. En Go no hay una cuenta tan sencilla: un grupo de piedras puede valer mucho o nada según cómo termine la partida. **Lo que el juego ofrece decide el algoritmo.**

**Cómo leer las dos tablas.** Cada fila es un algoritmo de la radiografía. «Conviene cuando» dice qué tiene que ofrecer el juego; «Le cuesta», qué paga a cambio.

- **«Cabe»** quiere decir que una búsqueda exacta termina en el tiempo que hay, aunque no recorra todo el árbol. Por ejemplo, alfa-beta con tablas de transposición.
- **Minimax pide más:** que quepa recorrer todo el árbol, sin poda.
- **«Minimax con corte»** incluye las dos versiones de la radiografía: por nivel o por reloj (profundización iterativa), con o sin búsqueda de quietud.

::: table {#jue-c3-cmp-cuando title="Cuándo conviene cada algoritmo"}
| Algoritmo | Conviene cuando |
|---|---|
| Minimax | Cabe sin poda, sin dados |
| Alfa-beta | Cabe y no hay dados |
| Expectiminimax | Cabe y hay dados |
| Minimax con corte | No cabe; hay EVAL buena |
| Monte Carlo plano | Sin EVAL; como base |
| Actualización minimax | Sin EVAL; cabe en memoria |
| UCT | Sin EVAL; árbol enorme |
:::

**Dónde se usó cada uno**, en el mismo orden:

- **Minimax:** gato.
- **Alfa-beta:** Conecta 4, resuelto en 1988 con búsqueda y reglas. Hoy alfa-beta con tablas de transposición lo resuelve sola.
- **Expectiminimax:** en la unidad, el ejemplo exacto es el árbol de resultados con un dado en D. El árbol completo del backgammon no cabe: TD-Gammon (1992) miraba dos jugadas, promediaba los dados y estimaba con una red.
- **Minimax con corte:** ajedrez (Deep Blue, 1997) y damas (Chinook, con bases de finales).
- **Monte Carlo plano:** Go, de 1993 a 2005.
- **Actualización minimax:** Kocsis y Szepesvári (2006), *Bandit based Monte-Carlo Planning*, llaman a este método *Monte-Carlo planning with minimax value update* (MMMC) y lo compararon con UCT en árboles de juego aleatorios. Con presupuestos prácticos falló más que Monte Carlo plano.
- **UCT:** Go (MoGo, 2006) y Hex (MoHex).

::: table {#jue-c3-cmp-cuesta title="Qué le cuesta a cada algoritmo"}
| Algoritmo | Le cuesta |
|---|---|
| Minimax | Del orden de $b^m$ nodos |
| Alfa-beta | Hasta $b^m$, menos ordenando bien |
| Expectiminimax | Cada dado multiplica las ramas |
| Minimax con corte | Escribir EVAL; el horizonte |
| Monte Carlo plano | Supone a ambos al azar |
| Actualización minimax | Guardar lo descubierto; lenta |
| UCT | Muchas simulaciones; elegir $c$ |
:::

- **Monte Carlo plano promedia como si los dos jugaran al azar**, y por eso puede elegir mal aunque simule para siempre.
- **La actualización minimax sí converge a $V$**, pero en el peor caso tiene que descubrir todo el árbol. Mientras tanto, un máximo con pocas muestras se fía de la jugada con más suerte.
- **Las tres últimas filas suponen que el árbol no cabe.** Las tres simulan hasta un final, sin EVAL.
- **Se pueden interrumpir (*anytime*)** la profundización iterativa y los tres Monte Carlo: si el reloj los detiene, ya tienen una jugada.

**Tres matices que las tablas no alcanzan a decir:**

- **Deep Blue y Chinook no buscaban hasta los finales.** Cortaban y estimaban; por eso no están en las filas de minimax y alfa-beta. Las damas sí se resolvieron en 2007, combinando varias búsquedas con bases de finales: con juego perfecto son tablas.
- **La quietud arregla los intercambios a medias, no todo.** Lo que no es captura sigue detrás del horizonte, como viste en [[jugar-contra-el-reloj|Hasta dónde mirar]].
- **UCT tiende a la jugada de minimax con vueltas sin límite**, con cualquier $c>0$ fija en un árbol finito. Con presupuesto fijo no garantiza acertar. En el mismo artículo, Kocsis y Szepesvári acotaron qué tan rápido, con una $c$ grande; la $c=1$ del curso no tiene esa cota, aunque aquí funcionó. De dónde sale la de UCB1 lo viste en [[de-donde-sale-el-bono|De dónde sale el bono]].

::: exercise {#jue-c3-cmp-ej-tdgammon title="Ubica a TD-Gammon en la tabla"}
TD-Gammon aparece junto a expectiminimax, porque el backgammon tiene dados, pero no buscaba hasta los finales.

1. ¿Qué fila de la primera tabla describe mejor lo que hacía?
2. ¿Qué número daba su búsqueda: $V$, valor con corte o $\widehat Q$?
:::

::: hint {#jue-c3-cmp-pista-tdgammon of="jue-c3-cmp-ej-tdgammon" title="Lo que hacía debajo"}
Cuando dejaba de mirar jugadas, ¿con qué valoraba esa posición? ¿Qué fila de la tabla hace lo mismo?
:::

::: answer {#jue-c3-cmp-resp-tdgammon of="jue-c3-cmp-ej-tdgammon"}
1. **La de minimax con corte**, pero con nodos de azar. Miraba dos jugadas, promediaba los dados como expectiminimax y estimaba debajo del corte con su red, que hacía de EVAL.
2. **Valor con corte**, no $V$. Promediar los dados no lo vuelve exacto: lo que queda debajo del corte es una estimación.
:::

La tabla se lee de algoritmo a juego. Con un juego nuevo en la mano hace falta lo contrario: ¿en qué orden se hacen las preguntas?

---

## 3 · Recorrer el mapa de decisión

**Piensa: de todas las preguntas de la tabla, ¿cuál hay que hacer primero?**

La de si cabe. Si el árbol cabe, la búsqueda exacta calcula $V$, y ninguna estimación es más fiable que ese valor exacto. Solo falta saber si hay dados, para elegir cuál búsqueda exacta. Las otras preguntas solo se hacen cuando no cabe. En [[diagnosticar-el-juego|Diagnosticar el juego]] ya era la quinta pregunta, la que decide el método.

**El mapa, en orden.** Tres preguntas eligen la rama: ¿cabe?, ¿hay dados?, ¿hay una EVAL buena? La cuarta, ¿hay reloj?, elige la versión dentro de la rama:

1. **¿Cabe el árbol en el tiempo que hay?** Sin dados: alfa-beta. Da $V$ y la jugada de minimax, y nunca genera más nodos que minimax; con buen orden, muchos menos. Con dados: expectiminimax, que da el $V$ del juego con dado.
2. **No cabe: ¿hay dados?** Con una EVAL: corte con nodos de azar, que se promedian, como TD-Gammon. Sin EVAL, ninguna de las siete fichas cubre ese caso: haría falta extender MCTS con nodos de AZAR, por ejemplo sorteando cada resultado con su $\Pr(a\mid s)$. Esa variante no se desarrolla en esta unidad.
3. **Sin dados, ¿hay una EVAL buena?** Sí: alfa-beta con corte. Con capturas, quietud; si hay reloj, profundización iterativa, que entrega la última búsqueda completa.
4. **Sin dados ni EVAL:** UCT, de la familia MCTS. Solo pide las reglas, para simular. Con reloj o sin él, se interrumpe cuando sea y entrega la jugada más visitada.

**En el caso sin dados, las otras dos simulaciones son variantes de la rama 4.** Monte Carlo plano es la versión sin árbol: más simple, y puede elegir mal. La actualización minimax converge a $V$, pero guarda todo lo que descubre y, con poco presupuesto, puede jugar peor.

**Las ramas 3 y 4 eligen entre las versiones de esta unidad.** Fuera de ella, MCTS también puede usar una evaluación: AlphaGo valoraba sus hojas con una red y con simulaciones.

**En el árbol de resultados.** Tiene 15 nodos y no tiene dados: cabe, rama 1. Alfa-beta juega centro con $V=0$ y genera 12. Los demás habrían pagado por nada, o algo peor:

- **El corte a $d=1$** elige izq, con $60$.
- **Monte Carlo plano** elige der.
- **La actualización minimax y UCT** eligen centro, pero con una estimación, no con $V$ demostrado.

Si D fuera un dado, seguiría en la rama 1, ahora con dados: expectiminimax juega der, que vale $1/3$.

**En la posición de la clase.** La de [[cortar-y-evaluar|Cortar y evaluar]] se trató como si no cupiera, para hacer las cuentas a mano. No tiene dados, y en la computadora sí cabe: rama 1. Su árbol completo tiene 389 nodos, y alfa-beta lo resuelve generando 78. Juega $\text{d2}\textbf{-}\text{d3}$, que gana: $V=+1$. El tablero de 4×4 entero, con 4 197 973 nodos, también cabe; así se sabe que gana el primero.

**Si no cupiera**, la posición tiene EVAL: sería la rama 3.

- **El corte a $d=1$** elige $\text{d2}\textbf{x}\text{c3}$, con $13$, que pierde.
- **Con quietud** elige $\text{d2}\textbf{-}\text{d3}$.
- **Sin EVAL, Monte Carlo plano también acierta al converger.** Si desde $\text{d2}\textbf{-}\text{d3}$ los dos juegan al azar hasta el final, $Q_{\text{azar}}=8/9$, lo más alto de las tres jugadas. Con pocas simulaciones puede equivocarse.

::: exercise {#jue-c3-cmp-ej-mapa title="Corre el mapa en tres juegos"}
Recorre las cuatro preguntas para cada juego y di en qué rama acaba.

1. Hexapawn, con sus 252 nodos.
2. El ajedrez, con reloj de torneo.
3. El backgammon.
:::

::: hint {#jue-c3-cmp-pista-mapa of="jue-c3-cmp-ej-mapa" title="Por dónde empezar"}
¿En cuál de los tres te detienes en la primera pregunta? En los otros dos, ¿qué tiene uno que el otro no?
:::

::: answer {#jue-c3-cmp-resp-mapa of="jue-c3-cmp-ej-mapa"}
1. **Hexapawn: rama 1.** Cabe y no hay dados; alfa-beta da $V$ exacto.
2. **Ajedrez: rama 3.** No cabe, no hay dados y contar piezas es una EVAL razonable. Alfa-beta con corte, quietud por las capturas e iterativa por el reloj: lo de Deep Blue.
3. **Backgammon: rama 2.** No cabe y hay dados: corte con nodos de azar, y la estimación que haya debajo. TD-Gammon la aprendió con una red.
:::

El mapa da por hecho que hay dos jugadores, que lo que gana uno lo pierde el otro, y que todo está a la vista. ¿Qué pasa si no?

---

## 4 · Lo que supone todo esto

**Piensa: MAX maximiza $U$ y MIN lo minimiza. ¿Por qué MIN se conforma con el número de MAX en vez de tener uno propio?**

Porque en suma cero no le hace falta. Cada final tiene un solo número, y lo que gana uno lo pierde el otro. El final que para MAX vale $-1$ es el mejor que le puede pasar a MIN: **el $-1$ de MAX es el máximo de MIN**. Minimizar lo de MAX es maximizar lo suyo, como viste en [[diagnosticar-el-juego|Diagnosticar el juego]].

**De ahí salen dos atajos de la unidad:**

- **Alfa-beta poda por lo mismo.** Lo que MAX ya tiene asegurado es justo lo que MIN ya no le puede quitar, porque los dos miden con el mismo número.
- **Dejar de buscar al ver lo mejor posible.** En [[jugar-contra-el-reloj|Hasta dónde mirar]], la raíz entrega una jugada que vale $+M$ sin mirar las demás. En I, si ix fuera su primera hoja, MIN pararía igual al ver $\text{ix}=-1$: el $-1$ de MAX es su máximo.

**Con dos jugadores también se rompe, si la suma no es constante.** Cada final lleva un vector $(U_1,U_2)$, y el segundo maximiza $U_2$; no necesariamente minimiza $U_1$.

- **El atajo de dejar de buscar se pierde.** Un final que paga $(-1,0)$ es pésimo para MAX, pero si otra hoja le da $+1$ al segundo, este sigue buscando.
- **También puede haber cooperación.** Dos amigos arman por turnos un rompecabezas, y los dos ganan si lo terminan. Minimax trataría al compañero como rival: calcularía una garantía pesimista que no describe lo que él quiere.

**Con tres jugadores se rompe del todo.** Un final en el que tú pierdes puede ser victoria de B o de C, y a B le importa cuál. Un número ya no basta: cada final necesita uno por jugador, $(U_1,\dots,U_n)$, y lo peor para ti deja de ser lo mejor para cada rival.

**Los cuatro supuestos de la unidad, y qué los rompe:**

- **Dos jugadores.** Con tres o más no hay un MIN: hay varios rivales, cada uno con su meta.
- **Suma cero o constante.** Si cada uno tiene su propio pago, suponer que el otro quiere dañarte es un error de modelado. Lo resume [[un-arbol-todos-los-algoritmos|la nota de suma cero de la radiografía]].
- **Por turnos.** Si eligen a la vez, ya no hay árbol donde uno responde al otro. Queda fuera de esta unidad.
- **Todo a la vista.** En póker no ves las cartas del rival: no sabes en qué nodo estás. Es información oculta, y queda fuera de esta unidad.

### Para ubicar

**Lo que se usa cuando se le pide más a MCTS, o cuando hay más de dos jugadores o la suma no es constante.** Una línea cada uno; no se estudian en el curso.

- **MCTS-Solver** (Winands, Björnsson y Saito, 2008): sube hacia arriba las victorias y derrotas ya demostradas, con máximo o mínimo, dentro de UCT. La versión original no trataba empates demostrados, porque eran raros en *Lines of Action*, el juego donde se probó.
- **MCTS con evaluación.** AlphaGo (2016) valora cada hoja mezclando una red de valor con una simulación; un peso, $\lambda$, decide cuánto cuenta la simulación.
- **Sin simulaciones hasta el final.** AlphaGo Zero (2017) y AlphaZero valoran la hoja de cada vuelta con la red. La selección con PUCT, un puntaje que suma lo que la red sugiere, ya venía de AlphaGo.

**Con más jugadores o suma no constante, cada final lleva un número por jugador.** Cuando mueves tú, eliges por el tuyo; lo que cambia es qué se supone de los rivales:

::: table {#jue-c3-cmp-no-suma-cero title="Más de dos jugadores o suma no constante, para ubicar"}
| Algoritmo | Cada rival elige | ¿Poda? |
|---|---|---|
| $\max^n$ | Lo mejor para él | Solo superficial |
| Paranoico | Lo peor para ti | Sí: alfa-beta |
| UCT con vectores | Por su propio promedio | No: simula |
:::

- **$\max^n$** (Luckhardt e Irani, 1986): quien mueve elige por su componente y copia el vector del hijo. En árboles finitos, por turnos y con todo a la vista, da un equilibrio, pero sin la garantía escalar de minimax.
- **Pide una regla de desempate fija.** Si un rival tiene dos jugadas que le dan lo mismo a él pero no a ti, el resultado depende de cuál supongas que elige.
- **Su poda es solo superficial.** Korf (1991) mostró que necesita cotas por jugador y sobre la suma, y que no da el ahorro de alfa-beta.
- **El paranoico (*paranoid*)** (Sturtevant y Korf, 2000) junta a los rivales en una coalición MIN. Recupera alfa-beta, pero resuelve un juego más pesimista que el real.
- **UCT con vectores** (Sturtevant, 2008) guarda un promedio por jugador, y cada uno selecciona por el suyo. Bajo sus condiciones puede dar equilibrios mixtos; lo probó, entre otros, en damas chinas.

::: exercise {#jue-c3-cmp-ej-cartas title="Señala qué supuestos rompe"}
Un juego de cartas para tres: cada uno ve solo su mano, se juega por turnos y quien hace más puntos gana. ¿Qué supuestos de la unidad rompe, y cuál de ellos lo deja fuera incluso de «para ubicar»?
:::

::: hint {#jue-c3-cmp-pista-cartas of="jue-c3-cmp-ej-cartas" title="Uno por uno"}
Recorre la lista de los cuatro supuestos. ¿Cuántos jugadores hay? ¿Qué no ve cada uno?
:::

::: answer {#jue-c3-cmp-resp-cartas of="jue-c3-cmp-ej-cartas"}
Rompe **dos jugadores** (son tres) y **todo a la vista** (las manos están ocultas). Sigue siendo por turnos. Las herramientas de varios jugadores de la tabla suponen todo a la vista; **la información oculta** lo deja fuera, como el póker.
:::

Con los supuestos y el mapa ya puedes elegir sin ayuda. Pruébalo en un juego que no está en ninguna tabla.

---

## 5 · Elegir en un juego nuevo

**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

::: exercise {#jue-c3-cmp-ej-fronteras title="Elige el algoritmo para Fronteras"}
**Fronteras** se juega en un tablero de 11×11 casillas, vacío al empezar. Por turnos, Rojo y Azul pintan una casilla vacía de su color; empieza Rojo. Una casilla pintada no se borra. La partida acaba cuando no queda casilla vacía, tras 121 jugadas. Gana quien tenga el grupo más grande de casillas de su color unidas por un lado. Si los dos grupos miden igual, es empate.

Simplificaciones: no hay dados ni cartas, los dos ven el tablero, y cada jugada tiene 10 segundos de reloj. Los que lo juegan dicen que contar el grupo más grande a mitad de partida engaña: un grupo chico bien puesto termina uniendo dos grandes. Nadie tiene otra estimación a la mano.

Lo nuevo frente a la página: no hay tabla ni árbol dados; el diagnóstico es tuyo, y una variante tiene tres jugadores.

1. Contesta: ¿cabe el árbol?, ¿hay dados?, ¿hay una EVAL buena?, ¿hay reloj?, ¿es de suma cero entre dos?
2. Recorre el mapa de la sección 3 y di en qué rama acabas.
3. Di qué jugada entrega tu algoritmo al acabarse el reloj, qué número usa para entregarla y qué valor estima. ¿Alguno de esos valores es $V$?
4. Variante: el tablero es de 3×3. ¿Cambia tu elección?
5. Variante: juegan Rojo, Azul y Verde, por turnos. ¿Qué supuesto se rompe, y qué buscarías en «para ubicar»?
:::

::: hint {#jue-c3-cmp-pista-fronteras-1 of="jue-c3-cmp-ej-fronteras" title="Pista 1 · Qué dato contesta cada pregunta"}
Para cada pregunta del punto 1, ¿qué frase del enunciado la contesta? ¿Cuál no se contesta con las reglas, sino con lo que dicen quienes lo juegan?
:::

::: hint {#jue-c3-cmp-pista-fronteras-2 of="jue-c3-cmp-ej-fronteras" title="Pista 2 · Revisa tu elección"}
Comprueba tu propuesta con dos preguntas. ¿Tu algoritmo necesita algo que el enunciado no te da? Con tres jugadores, ¿quién haría de MIN?
:::

::: answer {#jue-c3-cmp-resp-fronteras of="jue-c3-cmp-ej-fronteras" title="Respuesta · Simular, porque no hay con qué estimar"}
**1. Las cinco respuestas.** No cabe: hay 121 jugadas y la partida siempre las juega todas, así que hay $121!$ órdenes posibles, un número de 201 cifras. Aun contando cada posición una sola vez, como hace una tabla de transposición, son un número de 57 cifras.

No hay dados. No se tiene una EVAL confiable: la obvia, el grupo más grande, engaña según quienes lo juegan, y no hay otra. Hay reloj: 10 segundos. Y sí es suma cero entre dos: $U=+1$, $-1$ o $0$, y lo que gana uno lo pierde el otro.

**2. El mapa.** No cabe, no hay dados, no se tiene EVAL: **rama 4, UCT**. Simular es fácil: se llena al azar lo que queda y se cuentan los grupos. Toda simulación acaba, a lo más en 121 jugadas. Es el caso de Go y Hex en la tabla.

La actualización minimax también es de la rama 4, pero tendría que guardar todo lo descubierto, y en 10 segundos un máximo con pocas muestras engaña.

**3. Lo que entrega.** Al acabarse los 10 segundos, UCT entrega la jugada **más visitada**: compara $N(s_{\text{raíz}},a)$, no $\widehat Q$. El $\widehat Q(s_{\text{raíz}},a)$ asociado estima el valor de la jugada, pero no decide la entrega y, con presupuesto finito, no es $Q$ ni $V$. En un árbol finito, con una $c>0$ fija y vueltas sin límite, la jugada más visitada tendería a una de minimax; 10 segundos no son tiempo sin límite.

**4. Tablero de 3×3.** Son 9 jugadas: $9!=$ 362 880 partidas. Cabe: rama 1, alfa-beta, y la jugada sale con su $V$ exacto. El tamaño cambia la primera respuesta del mapa, y con ella todo lo demás.

**5. Tres jugadores.** Se rompe **dos jugadores**: no hay un solo MIN, y cada final necesita un número por jugador. Como no se tiene una EVAL confiable, lo cercano de la tabla es **UCT con vectores**. $\max^n$ y el paranoico llegan a los finales si el árbol cabe; aquí tendrían que cortar y estimar con una EVAL, y no hay con qué.
:::

**Punto de control:** deberías poder decir, para un juego nuevo, si cabe, si tiene dados, si hay una EVAL buena y si hay reloj. Con eso eliges el algoritmo con el mapa y dices qué número sostiene su jugada. También deberías reconocer cuándo un juego rompe los supuestos de la unidad.

## Lo que hay que llevarse

- **Un árbol, siete algoritmos.** En el árbol de resultados, minimax juega centro con $V=0$ en 15 nodos, y alfa-beta lo mismo en 12. El corte a $d=1$ elige izq, con $60$, y la quietud lo corrige: centro. Monte Carlo plano elige der; la actualización minimax y UCT vuelven a centro. Con un dado en D, la jugada es der, que vale $1/3$.
- **Qué número da cada uno.** $V$ es el valor del juego. El valor con corte lo estima con EVAL donde se corta. $\widehat Q$ lo estima simulando: Monte Carlo plano converge a $Q_{\text{azar}}$; la actualización minimax y UCT, a $Q$, con las condiciones de su ficha.
- **Cuándo conviene.** Si cabe, alfa-beta, o expectiminimax si hay dados: gato, Conecta 4. Si no cabe y hay una EVAL buena, minimax con corte: Deep Blue, Chinook. Si no la hay, UCT: MoGo, MoHex. Sin caber y con dados, corte con nodos de azar: TD-Gammon.
- **El mapa empieza por «¿cabe?».** La posición de la clase sí cabía en la computadora: 389 nodos, 78 con alfa-beta, y $\text{d2}\textbf{-}\text{d3}$ gana. El corte a $d=1$ elegía $\text{d2}\textbf{x}\text{c3}$, con $13$.
- **Todo supone dos jugadores, suma cero o constante, por turnos y todo a la vista.** En suma cero, el $-1$ de MAX es el máximo de MIN. Con pagos propios o tres jugadores eso se rompe: cada final lleva un vector, y entran $\max^n$, el paranoico o UCT con vectores.

Vuelve al [[juegos|índice de la unidad]].
