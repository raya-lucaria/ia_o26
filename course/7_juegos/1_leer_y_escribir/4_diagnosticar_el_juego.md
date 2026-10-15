---
id: diagnosticar-el-juego
title: Diagnosticar el juego
nav_title: Diagnosticar
summary: "Cuatro preguntas sobre un juego deciden qué modelo le toca y qué queda fuera: jugar a la vez, información oculta, suma no constante o más de dos jugadores. Luego, qué es jugar bien: ser racional, el valor V de un estado y el Q de una jugada, siempre desde MAX, la estrategia y el problema de la unidad."
status: ready
estimated_time: 35m
tags: [juegos, modelado, diagnostico]
---

# Diagnosticar el juego

**¿Qué tipo de juego es, qué modelo le toca y qué respuesta buscamos?**

Primero se diagnostica el juego; después se dice qué es jugarlo bien. Al terminar tendrás:

- **Un mapa del diagnóstico al modelo**, con lo que queda fuera de esta unidad.
- **Una definición de racional** que dice respecto a qué se juega bien.
- **El valor de un estado y el de una jugada**, $V$ y $Q$, con el problema de la unidad escrito con ellos.

## Lo que traes

- **El juego tiene siete piezas.** $(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\ T,\ U)$, escritas en [[escribir-el-juego|Escribir el juego]] (@jue-c1-juego).
- **El estado incluye el turno.** En $s=(\text{tablero},\text{turno})$, $\mathrm{Pl}(s)$ lee quién mueve: Blancas es MAX y Negras es MIN (@jue-c1-pl).
- **El pago de un final se mide desde MAX.** $U(s)$ solo existe en los finales (@jue-c1-utilidad).
- **El estado n1 y su subgrafo.** Están en [[el-juego-como-grafo|El juego como grafo]] (@jue-c1-subgrafo-n1).

> **Las reglas, en cuatro líneas.** Tablero de 3×3; Blancas (B) abajo en la fila 1 y Negras (N) arriba en la fila 3. Empiezan Blancas.
>
> Un peón avanza una casilla si está vacía o captura en diagonal hacia delante. Gana quien llega a la fila del rival, captura todos los peones rivales o deja al rival sin jugada. Ganar vale $+1$ y perder, $-1$.

---

## 1 · Cuatro preguntas sobre el juego

**Piensa: ¿qué tienes que saber de un juego antes de escribir su modelo?**

[[diagnosticar-el-entorno|La unidad de agentes]] diagnosticaba un entorno con siete perillas. Para un juego bastan cuatro preguntas: tres vienen de esas perillas y una es nueva.

::: table {#jue-c1-perillas title="Las cuatro preguntas, y hexapawn"}
| Pregunta | Perilla | Hexapawn |
|---|---|---|
| ¿Por turnos o a la vez? | Ninguna: es nueva | Por turnos |
| ¿Decide el azar algo? | Determinismo | No |
| ¿Cada uno ve todo? | Observabilidad | Sí |
| ¿Son dos y uno pierde lo que gana el otro? | Número de agentes | Sí |
:::

- **Por turnos:** cada jugador ve la jugada anterior antes de elegir la suya. La pregunta es propia de los juegos.
- **Sin azar:** no hay dados ni cartas que decidan algo.
- **Información perfecta:** el tablero y las jugadas están a la vista de los dos.
- **Dos jugadores y suma cero:** lo que gana uno lo pierde el otro, así que basta un número por final.

**Hay una quinta pregunta, que no es del juego sino del cómputo: ¿cabe el árbol?** Hexapawn sí: 252 nodos. El ajedrez, no.

---

## 2 · Cada diagnóstico pide un modelo

**Piensa: si los dos eligen a la vez, ¿sigue sirviendo un árbol donde uno mueve y el otro responde?**

No. Las respuestas a las cuatro preguntas deciden cómo se escribe el juego, y algunas lo sacan del modelo de esta unidad:

::: table {#jue-c1-mapa title="Del diagnóstico al modelo"}
| Juego | Lo distingue | Modelo | ¿Aquí? |
|---|---|---|---|
| Hexapawn | Las cuatro respuestas de arriba | Árbol MAX y MIN | Sí |
| Un juego con dado | Un dado decide una parte | Árbol con azar | Sí |
| Ajedrez | El árbol no cabe | Árbol cortado y estimación | Sí |
| Pares o nones | Eligen a la vez | Tabla de pagos | No |
| Dilema del prisionero | A la vez, sin suma cero | Tabla con un pago por jugador | No |
| Damas chinas, de tres | Tres jugadores | Un pago por jugador | No |
| Póker | Cartas ocultas | Otro modelo | No |
:::

Tres modelos de la tabla son nuevos, y aquí basta una línea de cada uno:

- **Un nodo de azar** es un nodo donde no elige ningún jugador, sino un dado. Cada flecha lleva la probabilidad de que salga.
- **Una tabla de pagos** tiene una fila por jugada de un jugador y una columna por jugada del otro. En cada celda va lo que gana cada uno.
- **Un pago por jugador** es un vector $(U_1,\dots,U_n)$ en cada final, en lugar de un solo número.

**Cuando los dos eligen a la vez, ninguno ve la jugada del otro antes de decidir.** Un árbol donde Blancas mueve y Negras responde **viéndola** describiría otro juego.

### Qué queda fuera de esta unidad

El modelo de esta unidad supone turnos, todo a la vista, dos jugadores y suma cero. Cada una de estas variaciones lo rompe, y aquí solo se diagnostica:

- **A la vez:** ninguno ve la elección actual del otro. Pares o nones y el dilema del prisionero piden otro modelo.
- **Información oculta:** un jugador no sabe en qué estado está, solo lo que ve de él. Así pasa en el póker.
- **Suma no constante:** mejorar el pago de uno puede mejorar también el del otro. Ya no basta un número con el signo cambiado.
- **Más de dos jugadores:** cada uno persigue su propio pago. La nota siguiente dice qué cambia.

::: remark {#jue-c1-nota-jugadores title="Suma cero, suma no constante y más jugadores"}
**Con dos jugadores y suma cero, un número por final basta.** Para MIN el final vale $-U$, así que lo mejor para MIN es lo peor para MAX.

- **Suma constante:** se reduce al caso anterior. En ajedrez de torneo, 1, ½ y 0 suman 1 por partida; restar ½ y multiplicar por 2 da $+1$, $0$ y $-1$ (@jue-c1-utilidad).
- **Dos jugadores, suma no constante:** cada final lleva $(U_1,U_2)$. El segundo jugador maximiza $U_2$, que no necesariamente minimiza $U_1$.
- **Más jugadores: $\max^n$** (Luckhardt e Irani, 1986). Cada final lleva $(U_1,\dots,U_n)$; quien mueve elige el hijo con su componente más alta y **copia el vector entero** de ese hijo.
- **Lo que da $\max^n$:** con una regla de desempate fija, un equilibrio, en juegos finitos, por turnos y con todo a la vista. No da la garantía de dos jugadores: lo que obtiene cada uno depende de cómo desempaten los demás.
- **Con tres o más, la suma cero no basta para un solo rival.** Cada rival persigue su propia componente, no necesariamente la ruina de MAX.
- **El paranoico (*paranoid*)** (Sturtevant y Korf, 2000) junta a todos los rivales en una coalición MIN. Vuelve al caso de dos jugadores y suma cero, pero resuelve un juego más pesimista que el real.
:::

---

## 3 · Jugar bien: qué es ser racional

**Piensa: el problema de la unidad va a pedir que MIN «responda lo mejor que puede». ¿Lo mejor según quién, y con qué?**

::: definition {#jue-c1-racional title="Jugador racional"}
Un jugador es **racional** si, cada vez que le toca, elige la jugada que espera que le dé la mayor utilidad, **dado**:

1. **su función a optimizar**: su utilidad, la que está escrita;
2. **lo que sabe**: las reglas y lo que ha visto de la partida;
3. **lo que puede hacer**: sus jugadas, $A(s)$;
4. **lo que alcanza a calcular** con el tiempo y la memoria que tiene.

**Qué significa:** no existe «racional» a secas. Siempre es racional **respecto a** esas cuatro cosas, y la primera es la que manda: la racionalidad sale de la función a optimizar, no de ganar ni de parecer listo.
:::

Es la definición del libro de texto de IA, el de Russell y Norvig. Un agente racional elige la acción que espera que maximice su **medida de desempeño**, con lo que ha percibido y lo que sabe.

Es la misma medida de desempeño de [[desempeno-en-peas|la unidad de agentes]]. En un juego, esa medida es la utilidad $U$, el pago de cada final.

### Racional para MAX y para MIN

- **MAX racional** elige para que $U$ quede lo más alto posible.
- **MIN racional** elige para que **su** utilidad, $-U$, quede lo más alta posible. Es decir, para que $U$ quede lo más bajo posible.

**Por eso, y solo porque son dos y es suma cero, «lo mejor para MIN» es «lo peor para MAX».** Sin esos supuestos, la equivalencia deja de valer (@jue-c1-nota-jugadores).

### No hay racionalidad perfecta

Garantizar la jugada perfecta exige, en general, revisar muchísimas continuaciones. Hay atajos que se ahorran parte del árbol, pero no todo.

En hexapawn se puede revisar todo: son 252 nodos. En ajedrez nadie puede, ni la computadora más grande.

**Eso no vuelve irracional a quien juega ajedrez.** Lo racional es **lo mejor que puedes dado tu objetivo y tus límites**: si tienes un segundo, la mejor jugada que encuentras en un segundo.

Stuart Russell, uno de los autores de ese libro, lo llamó **racionalidad limitada**. En economía, Herbert Simon le había llamado racionalidad acotada.

::: table {#jue-c1-racional-limites title="Lo racional depende de lo que tiene el jugador"}
| Lo que tiene | Lo racional |
|---|---|
| Tiempo para todo el árbol | La jugada que asegura más contra cualquier respuesta |
| Un segundo por jugada | La mejor que encuentra en ese segundo |
| Una tabla de 24 cajas | Lo que dice la caja de ese tablero |
:::

**La jugada perfecta es una regla para medir, no una exigencia.** Lo que sí se exige es no desperdiciar: si tenías tiempo de ver que una jugada pierde y la hiciste, eso sí es irracional.

### Lo que racional no quiere decir

::: table {#jue-c1-racional-no title="Cuatro confusiones con «racional»"}
| No es | Por qué no |
|---|---|
| Ganar siempre | En hexapawn, Blancas pierde aun jugando perfecto |
| Ser inteligente o humano | La máquina de cerillos de Gardner son cajas |
| Saberlo o calcularlo todo | Elige con lo que sabe y alcanza a calcular |
| Querer lo que queremos | Persigue **su** $U$, sea cual sea |
:::

**La última fila es la importante: un jugador racional con una utilidad mal escrita hace mal las cosas con toda eficiencia.** El error está en $U$, no en el jugador. Por eso [[escribir-el-juego|Escribir el juego]] insiste en que la utilidad copia el reglamento.

### Que el rival sea racional es un supuesto

Lo anotamos igual que los supuestos del reglamento. Cuando no se cumple, el diagnóstico cambia:

- **Si Negras mueve al azar,** lo que Blancas calcula suponiéndola óptima se sigue cumpliendo como piso, si Blancas sigue eligiendo lo mejor. Pero puede dejar puntos sobre la mesa.
- **Si el árbol no cabe,** nadie calcula todo. Cortar y estimar es racionalidad limitada en la práctica.
- **Si eligen a la vez,** cada uno es racional **dado lo que hará el otro**. Ese caso queda fuera de esta unidad.

::: exercise {#jue-c1-ej-racional title="¿Racional o no?"}
Para cada caso, di si el jugador fue racional y, si algo salió mal, dónde está el error: en el jugador o en la utilidad.

1. En n1, Blancas juega $\text{c1}\textbf{-}\text{c2}$ y gana en esa jugada.
2. Un programa recibe $+1$ por ganar, $-1$ por perder y además $+3$ por cada peón que captura. En n1 juega $\text{c1}\textbf{x}\text{b2}$ en vez de $\text{c1}\textbf{-}\text{c2}$, y pierde.
3. Blancas juega perfecto desde el inicio y pierde.
4. Un programa juega suponiendo que Negras es racional, pero Negras mueve al azar.
5. Con un segundo por jugada, un programa de ajedrez mira 4 jugadas hacia delante y elige una que, vista con 20, pierde.
:::

::: hint {#jue-c1-pista-racional of="jue-c1-ej-racional" title="Las cuatro cosas dadas"}
En cada caso pregúntate qué función optimizaba el jugador, qué sabía y cuánto podía calcular. Si con eso eligió lo mejor, fue racional, aunque el resultado haya sido malo.

Para el caso 2, cuenta los puntos de cada jugada con **la utilidad del programa**, no con la del reglamento. Tras $\text{c1}\textbf{x}\text{b2}$, Negras gana de inmediato con $\text{c3}\textbf{x}\text{b2}$.
:::

::: answer {#jue-c1-resp-racional of="jue-c1-ej-racional"}
1. **Racional.** Gana en una jugada, y ganar es lo más alto que da $U$.
2. **Racional, con una utilidad mal escrita.** Para el programa, $\text{c1}\textbf{-}\text{c2}$ vale $+1$: gana sin capturar. Y $\text{c1}\textbf{x}\text{b2}$ vale $-1+3=+2$: pierde, pero capturó un peón.

   Con su utilidad, capturar es mejor. **El error está en $U$:** el reglamento no paga por capturar, y el programa hizo con toda eficiencia lo que su número le pedía.
3. **Racional.** En hexapawn, Negras puede asegurar la victoria haga lo que haga Blancas. Perder no prueba que se jugó mal; ser racional no es ganar.
4. **El programa es racional dado lo que supone**, pero el supuesto es falso. Lo que calculó lo sigue protegiendo: si sigue eligiendo lo mejor, nunca le irá peor que eso. Lo que pierde es la oportunidad de aprovechar los errores de Negras.
5. **Puede ser racional.** No tenía cómo ver 20 jugadas en un segundo, y perder no lo hace irracional. Pero mirar 4 tampoco lo demuestra: depende de si tenía a su alcance una búsqueda mejor en ese segundo y no la usó.
:::

---

## 4 · Valor, jugada y estrategia

**Piensa: cuando le pides a un programa «la respuesta», ¿qué esperas que te dé?**

Hay tres cosas distintas, y conviene no confundirlas. El valor, además, tiene dos versiones: la de un estado y la de una jugada.

::: definition {#jue-c1-valor-jugada-estrategia title="Valor, jugada y estrategia"}
**El valor de un estado,** $V(s)$, es el pago para MAX si, desde $s$, los dos juegan lo mejor. Es un número en la escala de $U$; en un final, $V(s)=U(s)$.

**El valor de una jugada,** $Q(s,a)$, es ese pago si en $s$ se juega primero $a$ y después los dos juegan lo mejor. Como cada jugada lleva a un solo hijo,

$$\mathbf{Q(s,a)=V\bigl(T(s,a)\bigr)}.$$

**El estado vale lo que la mejor jugada de quien mueve:**

$$\mathbf{V(s)=\begin{cases}U(s) & \text{si } s\in S_F,\\[2pt] \max_{a\in A(s)} Q(s,a) & \text{si } \mathrm{Pl}(s)=\text{MAX},\\[2pt] \min_{a\in A(s)} Q(s,a) & \text{si } \mathrm{Pl}(s)=\text{MIN}.\end{cases}}$$

**Una jugada** es una acción $a\in A(s)$: lo que haces ahora.

**Una estrategia** de MAX es una función que a cada estado $s$ con $\mathrm{Pl}(s)=\text{MAX}$ le asigna una jugada de $A(s)$. Dice qué hacer en **cada** estado donde le toca, no solo en el actual. Lo mismo para MIN.
:::

**El valor del estado es el resultado para MAX bajo juego óptimo; MAX elige el mayor $Q$ y MIN el menor.**

- **Siempre desde MAX.** $V$ y $Q$ no cambian de perspectiva con el turno: en un nodo de MIN, la mejor jugada es la de menor $Q$.
- **Qué no es:** no es lo que pasará en una partida real, donde alguno puede equivocarse. Es lo que pasa si ninguno se equivoca.

**En n1 ya hay un $Q$ que se lee directo.** La jugada $\text{c1}\textbf{-}\text{c2}$ lleva a n2, que es final y gana Blancas: $Q(\text{n1},\text{c1}\textbf{-}\text{c2})=V(\text{n2})=U(\text{n2})=+1$.

Como $+1$ es el pago más alto que existe en hexapawn, ninguna jugada supera a esa. Por eso $V(\text{n1})=+1$, sin conocer el $Q$ de la otra jugada.

### El número y la jugada

**El valor no es una jugada: dice cuánto vale el estado, no qué hacer.** Ya lo viste en la unidad de optimización, con $Q$ como la función que se optimiza:

- **$\max_{a\in A(s)} Q(s,a)$ es el número** más alto que se alcanza.
- **$\operatorname*{arg\,max}_{a\in A(s)} Q(s,a)$ es el conjunto de jugadas** que lo alcanzan. Es un conjunto porque puede haber empates.
- **En un nodo de MIN** se usan $\min$ y $\operatorname*{arg\,min}$.

### La estrategia es mucho más grande que una jugada

En hexapawn hay **37 estados** donde le toca a Negras y la partida no ha terminado. Una estrategia de Negras elige una jugada en cada uno.

Martin Gardner construyó una máquina que jugaba con Negras usando **24 cajas de cerillos**, una por tablero. Le alcanzaron menos de 37 porque varios tableros son el reflejo de otro, y basta guardar uno. La máquina aprendía qué jugada evitar en cada caja.

**Las 24 cajas no son el mínimo.** Si se identifican todos los reflejos, esos 37 estados quedan en 19.

**Por qué importa la estrategia:** el rival puede llevarte a estados que no esperabas. Un plan que solo dice cómo empezar se queda sin respuesta en cuanto el rival se desvía.

::: exercise {#jue-c1-ej-que-dice-v title="Decide qué dice el valor"}
En hexapawn, $V(s_0)=-1$. ¿Qué dice ese número y qué **no** dice?
:::

::: hint {#jue-c1-pista-que-dice-v of="jue-c1-ej-que-dice-v" title="Separa el número de la jugada"}
Recuerda desde dónde se mide $V$ y qué suponen los dos jugadores. Luego pregúntate si un número basta para saber qué jugada hacer.
:::

::: answer {#jue-c1-resp-que-dice-v of="jue-c1-ej-que-dice-v"}
**Dice** que, si los dos juegan lo mejor posible, Blancas pierde: Negras puede asegurar la victoria, haga lo que haga Blancas.

**No dice** qué jugada hacer en ningún estado. Para eso hace falta comparar los $Q$ de las jugadas y quedarse con una del $\operatorname{arg\,max}$, o tener una estrategia completa. Tampoco dice qué pasa si alguno de los dos se equivoca.
:::

---

## 5 · Tu turno

::: exercise {#jue-c1-ej-diagnostico title="Diagnostica cuatro juegos"}
Para cada juego, contesta las cuatro preguntas de la sección 1 y di qué modelo le toca, o por qué no es un juego para esta unidad.

1. **Serpientes y escaleras.** Cada jugador tira un dado y avanza esa cantidad de casillas; las escaleras suben y las serpientes bajan.
2. **Batalla naval.** Cada jugador esconde sus barcos en una cuadrícula y, por turnos, dispara a una casilla del rival.
3. **Conecta 4.** Por turnos se dejan caer fichas en un tablero vertical de 7 columnas; gana quien alinea cuatro.
4. **Damas chinas entre tres.** Por turnos, cada uno lleva sus fichas a la punta opuesta de una estrella; gana quien llega primero con todas.
:::

::: hint {#jue-c1-pista-diagnostico of="jue-c1-ej-diagnostico" title="Antes de las cuatro preguntas"}
Para cada juego, pregúntate primero si algún jugador **elige** algo. Si nadie elige, no hay nada que calcular para un jugador. Después busca qué no ve cada jugador y cuántos juegan.
:::

::: answer {#jue-c1-resp-diagnostico of="jue-c1-ej-diagnostico"}
1. **Serpientes y escaleras:** por turnos, con azar, todo visible y suma cero. Pero **nadie decide nada**: el dado fija cada movimiento. No hay jugada que elegir, así que no hay nada que calcular para un jugador.
2. **Batalla naval:** por turnos y sin azar una vez colocados los barcos, pero **no** ves los barcos del rival. Es información oculta, como en el póker: queda fuera de esta unidad.
3. **Conecta 4:** por turnos, sin azar, todo visible y suma cero. Le toca un **árbol con nodos MAX y MIN**, como a hexapawn.

   Pero su árbol es enorme: la quinta pregunta dice que no cabe completo, como en el ajedrez. Aun así se resolvió en 1988, con reglas de estrategia y búsqueda: gana quien empieza.
4. **Damas chinas entre tres:** por turnos, sin azar y todo visible, pero **son tres**. Hace falta un pago por jugador y $\max^n$ (@jue-c1-nota-jugadores): queda fuera de esta unidad.
:::

---

## 6 · La pregunta que falta: qué jugada elegir

**Piensa: en $s_0$, ¿pudo Blancas evitar perder?**

Una sola partida no lo dice. Para saberlo hay que considerar **todas** las respuestas de Negras, no solo las que hizo esta vez.

Eso es el problema de la unidad, y se escribe como en la unidad de optimización: qué te dan y qué tienes que encontrar.

::: definition {#jue-c1-problema title="El problema: elegir la jugada"}
**Dado:** el juego $(S,\ s_0,\ S_F,\ \mathrm{Pl},\ A,\ T,\ U)$: finito, por turnos, sin azar, todo a la vista, dos jugadores y suma cero.

**Encontrar:** en cada estado no final donde le toca a MAX, la jugada de $A(s)$ que le asegura el mayor pago posible **si los dos juegan lo mejor**.

**Qué supone de MIN:** que juega óptimamente, es decir, que responde siempre lo peor para MAX.
:::

**«Juega óptimamente» pide más que «es racional».** Un MIN racional con límites de cómputo (@jue-c1-racional) puede no encontrar su mejor respuesta; el problema supone que siempre la encuentra.

**Con $V$ y $Q$, el problema cabe en una línea.** En cada estado $s$ de MAX se busca

$$\mathbf{a^{*}\in\operatorname*{arg\,max}_{a\in A(s)} Q(s,a)},$$

y el pago que asegura es $V(s)$. El $\in$ deja que varias jugadas empaten.

**Por qué en cada estado, y no solo en $s_0$.** El rival puede llevarte a cualquier estado, así que la respuesta completa es una estrategia (@jue-c1-valor-jugada-estrategia), no una sola jugada.

**Punto de control:** deberías poder escribir cualquier tablero de hexapawn con las siete piezas y diagnosticar un juego nuevo con las cuatro preguntas. También, decir qué modelo le toca o qué lo deja fuera, respecto a qué es racional un jugador, distinguir $V$, $Q$, una jugada y una estrategia, y decir qué pide el problema de la unidad.

---

## Lo que hay que llevarse

- **Cuatro preguntas deciden el modelo:** turnos o a la vez, azar, información completa, y dos jugadores con suma cero. Una quinta decide el método: si el árbol cabe.
- **Turnos sin azar llevan a un árbol MAX/MIN; con azar, a un árbol con nodos de azar.** Jugar a la vez, ocultar información o tener más de dos jugadores sacan al juego de esta unidad.
- **Racional siempre es respecto a algo:** su utilidad, lo que sabe, lo que puede hacer y lo que alcanza a calcular. Una utilidad mal escrita se persigue con toda eficiencia.
- **El valor del estado es el resultado para MAX bajo juego óptimo; MAX elige el mayor $Q$ y MIN el menor.** Con $Q(s,a)=V(T(s,a))$, el valor es un número, la jugada lo que haces ahora y la estrategia un plan para cada estado.
- **El problema de la unidad:** en cada estado de MAX, una jugada que asegure $V(s)$ si los dos juegan lo mejor.

Continúa con la [[tarea-leer-y-escribir|tarea de refuerzo]].
