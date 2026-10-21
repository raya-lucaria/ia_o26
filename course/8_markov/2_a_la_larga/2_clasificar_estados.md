---
id: mkv-clasificar-estados
title: "Clasificar los estados"
nav_title: "Clasificar los estados"
summary: "Comunicar, clase cerrada, transitorio, recurrente y periodo para partir cualquier cadena finita en piezas, decidir cuáles retienen a la cadena y clasificar a mano una cadena de cinco estados."
status: ready
estimated_time: 28m
tags: [markov, grafos, clasificacion]
---

# Clasificar los estados

**¿En qué piezas se parte una cadena, y en cuáles se queda atrapada para siempre?**

Al terminar tendrás:

- **Las clases de una cadena:** agruparás los estados que se alcanzan mutuamente.
- **Cerradas y abiertas:** decidirás si una clase deja salir a la cadena.
- **Transitorios y recurrentes:** justificarás, en cadenas finitas, por qué recurrente equivale a cerrada.
- **El periodo:** lo calcularás y reconocerás cuándo un lazo basta para que valga 1.
- **Un procedimiento a mano:** clasificarás una cadena de cinco estados de principio a fin.

## Lo que traes

- **Alcanzar.** De [[mkv-algebra-y-limites|Lo que necesitas de álgebra y límites]]: $s\to s'$ si hay un camino de $s$ a $s'$ con flechas positivas, de cualquier número de pasos (@mkv-c2-def-alcanzar).
- **Grafo y matriz.** En [[mkv-cadena-en-general|La cadena de Markov, en general]], cada entrada positiva de $P$ es una flecha del grafo (@mkv-c1-matriz-transicion).
- **Potencias.** $(P^t)_{ss'}$ es la probabilidad de ir de $s$ a $s'$ en exactamente $t$ pasos (@mkv-c1-teo-potencias).
- **Irreducible.** En [[mkv-ajustar-contando|Ajustar contando]], @mkv-c1-teo-recuperar pidió que desde cada estado se pudiera llegar a cualquier otro.

**Página de concepto:** sin simulación ni código. Todo vale para una cadena finita y homogénea de $k$ estados; el juguete es para poder trazarlo.

---

## 1 · Agrupar los estados que se comunican

**Piensa: ¿cuándo dos estados pertenecen a la misma pieza de la cadena?**

Cuando cada uno alcanza al otro: puedes ir y volver. Contamos también el camino de cero pasos, porque $P^0=I_k$ da $(P^0)_{ss}=1$.

::: definition {#mkv-c2-def-comunican title="Estados que se comunican"}
$$
\begin{aligned}
s\leftrightarrow s'
\quad&\Longleftrightarrow\quad
s\to s'\ \text{ y }\ s'\to s,\\
s\to s'
\quad&\Longleftrightarrow\quad
(P^t)_{ss'}>0\\
&\qquad\text{para algún }t\ge0.
\end{aligned}
$$

- **Qué es:** una relación entre dos estados: hay camino de ida y camino de vuelta.
- **Cómo se calcula:** en el grafo, buscas un camino en cada sentido; los números de las flechas no importan, solo que sean positivos.
- **Qué significa:** la cadena puede pasar de uno al otro y regresar, tantas veces como quiera.
- **Qué no es:** alcanzar no es comunicar; $s\to s'$ sin camino de vuelta deja a los dos en piezas distintas.
:::

Comunicar es una relación de equivalencia: parte los estados en grupos que no se traslapan.

::: theorem {#mkv-c2-cl-teo-clases title="Comunicar parte los estados en clases"}
En una cadena homogénea, para todos los estados $s,s',s''$:

$$
\begin{aligned}
&s\leftrightarrow s,\\
&s\leftrightarrow s'\ \Longrightarrow\ s'\leftrightarrow s,\\
&s\leftrightarrow s',\ s'\leftrightarrow s''
\ \Longrightarrow\ s\leftrightarrow s''.
\end{aligned}
$$

Una **clase** $\mathcal C$, «ce caligráfica» (la C recta sigue siendo la consonante), reúne los estados que se comunican con uno dado. Cada estado está en exactamente una.

- **Condición.** Ninguna más allá de la cadena: vale con cualquier número de estados.
- **Lectura.** Las clases son las piezas de la cadena; dentro de una, todos van y vuelven entre sí.
- **Casos nulos.** Un estado sin camino de vuelta desde ningún otro forma una clase de un solo estado.
:::

::: proof {#mkv-c2-cl-dem-clases of="mkv-c2-cl-teo-clases"}
**Reflexiva:** el camino de cero pasos. **Simétrica:** la definición pide los dos sentidos.

**Transitiva:** si $(P^{a})_{ss'}>0$ y $(P^{b})_{s's''}>0$, el término intermedio $s'$ de @mkv-c1-teo-potencias da

$$
\begin{aligned}
(P^{a+b})_{ss''}
&\ge(P^{a})_{ss'}(P^{b})_{s's''}>0.
\end{aligned}
$$

La vuelta se arma igual. Una relación con las tres propiedades parte el conjunto en clases disjuntas.
:::

**En el juguete.** Usaremos toda la página una cadena de cinco estados, con sus flechas:

$$
P=
\begin{pmatrix}
0&1/2&0&1/2&0\\
0&0&1&0&0\\
0&1&0&0&0\\
0&0&0&1/2&1/2\\
0&0&0&1&0
\end{pmatrix}.
$$

- **Desde $s_1$:** a $s_2$ y a $s_4$, con $1/2$ cada una. Ninguna flecha llega a $s_1$.
- **Entre $s_2$ y $s_3$:** van y vienen con probabilidad 1.
- **Entre $s_4$ y $s_5$:** $s_4$ se queda o pasa a $s_5$; $s_5$ vuelve a $s_4$.
- **Clases:** $\{s_1\}$, $\{s_2,s_3\}$ y $\{s_4,s_5\}$. $s_1$ alcanza a todos, pero nadie lo alcanza a él.

::: exercise {#mkv-c2-cl-ej-clases-t4 title="Encuentra las clases de tres estados"}
Con estados $s_1,s_2,s_3$, ¿qué clases tiene esta matriz?

$$
P=
\begin{pmatrix}
1/2&1/4&1/4\\
0&1&0\\
0&0&1
\end{pmatrix}
$$
:::

::: hint {#mkv-c2-cl-pista-clases-t4 of="mkv-c2-cl-ej-clases-t4" title="¿Hay camino de vuelta a s₁?"}
¿Alguna fila distinta de la primera tiene un número positivo en la columna de $s_1$?
:::

::: answer {#mkv-c2-cl-resp-clases-t4 of="mkv-c2-cl-ej-clases-t4"}
**Tres clases:** $\{s_1\}$, $\{s_2\}$ y $\{s_3\}$. $s_1$ alcanza a los otros dos, pero la columna de $s_1$ solo tiene positiva la entrada de $s_1$: nadie vuelve.
:::

Ya sabemos partir la cadena. Falta saber si una pieza deja salir a la cadena.

---

## 2 · Encontrar las clases cerradas

**Piensa: una vez dentro de una clase, ¿puede salir la cadena?**

Depende de una sola cosa: si alguna flecha sale de la clase. Si ninguna sale, la clase es cerrada.

::: definition {#mkv-c2-def-clase-cerrada title="Clase cerrada y estado absorbente"}
$$
\begin{aligned}
\mathcal C\ \text{cerrada}
\ &\Longleftrightarrow\
P_{ss'}=0\\
&\qquad\text{si }s\in\mathcal C,\ s'\notin\mathcal C,\\
&\Longleftrightarrow\
\sum_{s'\in\mathcal C}P_{ss'}=1\\
&\qquad\text{para todo }s\in\mathcal C.\\
s\ \text{absorbente}
\ &\Longleftrightarrow\ P_{ss}=1.
\end{aligned}
$$

- **Qué es:** una clase sin flechas hacia afuera. Si no es cerrada, decimos que es **abierta**.
- **Cómo se calcula:** para cada estado de la clase, revisas su fila: toda la probabilidad debe caer en columnas de la clase.
- **Qué significa:** si la cadena entra, ya no sale. Un estado absorbente es una clase cerrada de un solo estado.
- **Qué no es:** cerrada no prohíbe entrar; pueden llegarle flechas desde afuera.
:::

Una cadena finita siempre tiene dónde quedarse.

::: theorem {#mkv-c2-cl-teo-hay-cerrada title="Toda cadena finita tiene una clase cerrada"}
Si la cadena tiene $k$ estados, con $k$ finito, al menos una de sus clases es cerrada.

- **Condición.** Finita. Es suficiente, no necesaria.
- **Lectura.** Siguiendo flechas de clase en clase, llegas a una de la que no se sale.
- **Casos nulos.** Si todo se comunica, la única clase es todo $\mathcal S$, y es cerrada: no hay afuera.
:::

::: proof {#mkv-c2-cl-dem-hay-cerrada of="mkv-c2-cl-teo-hay-cerrada"}
Empieza en cualquier clase. Si es abierta, sigue una flecha que sale a otra clase. Nunca regresas a una clase ya visitada: si regresaras, sus estados se comunicarían y serían una sola clase. Con un número finito de clases, el recorrido se detiene en una clase sin flechas que salgan.
:::

- **Contraejemplo infinito:** en $\{0,1,2,\dots\}$ con $i\to i+1$ con probabilidad 1, cada $\{i\}$ es una clase abierta. Ninguna es cerrada.

**Una sola clase.** Si todos los estados se comunican, la cadena es **irreducible**. Es la condición de @mkv-c1-teo-recuperar, ahora con nombre de clase: **una sola clase que lo abarca todo**, y por eso cerrada.

**En el juguete.** Revisamos la fila de cada estado:

- **$\{s_2,s_3\}$ es cerrada:** $s_2$ solo va a $s_3$, y $s_3$ solo a $s_2$.
- **$\{s_4,s_5\}$ es cerrada:** las filas de $s_4$ y $s_5$ reparten todo entre $s_4$ y $s_5$.
- **$\{s_1\}$ es abierta:** su fila manda $1/2$ a $s_2$ y $1/2$ a $s_4$.
- **No es irreducible:** tiene tres clases. Tampoco hay estados absorbentes.

::: exercise {#mkv-c2-cl-ej-cerradas-t4 title="Señala las clases cerradas"}
En la matriz de tres estados del ejercicio anterior, ¿qué clases son cerradas? ¿Hay estados absorbentes? ¿Es irreducible?
:::

::: hint {#mkv-c2-cl-pista-cerradas-t4 of="mkv-c2-cl-ej-cerradas-t4" title="¿Qué dice la diagonal?"}
¿Qué filas tienen toda su probabilidad dentro de su propia clase?
:::

::: answer {#mkv-c2-cl-resp-cerradas-t4 of="mkv-c2-cl-ej-cerradas-t4"}
- **Cerradas:** $\{s_2\}$ y $\{s_3\}$; $P_{s_2s_2}=P_{s_3s_3}=1$, así que los dos son absorbentes.
- **Abierta:** $\{s_1\}$, que manda $1/4$ a cada uno de los otros.
- **No es irreducible:** tiene tres clases y dos de ellas cerradas.
:::

Cerrada habla de flechas. ¿Qué dice eso de las visitas de la cadena a cada estado?

---

## 3 · Separar transitorios y recurrentes

**Piensa: ¿a qué estados vuelve la cadena una y otra vez?**

A los recurrentes: los que, una vez visitados, se vuelven a visitar seguro. $\Pr_s$ es la probabilidad empezando en $s$ (@mkv-c2-def-esperanza).

::: definition {#mkv-c2-def-transitorio title="Estado transitorio y estado recurrente"}
$$
\begin{aligned}
f_s&=\Pr_s\bigl(S_t=s\\
&\qquad\text{para algún }t\ge1\bigr),\\
s\ \text{recurrente}
\ &\Longleftrightarrow\ f_s=1,\\
s\ \text{transitorio}
\ &\Longleftrightarrow\ f_s<1.
\end{aligned}
$$

- **Qué es:** $f_s$, «efe sub ese», es la probabilidad de volver a estar en $s$ en algún paso $t\ge1$, empezando en $s$. Quedarse por un lazo cuenta como regreso.
- **Cómo se calcula:** sumas las probabilidades de los caminos que regresan a $s$ por primera vez.
- **Qué significa:** cada regreso vuelve a empezar la cadena en $s$, por la propiedad de Markov. Un recurrente se visita una y otra vez sin fin; un transitorio, un número finito de veces.
- **Qué no es:** transitorio no quiere decir que nunca regrese. Puede regresar, solo que no seguro.
:::

**Contamos desde $t\ge1$.** El paso 0 no cuenta como regreso; por eso $f_s$ puede ser 0.

El teorema central de la página convierte esa pregunta sobre visitas en una pregunta sobre flechas.

::: theorem {#mkv-c2-teo-recurrente-cerrada title="En una cadena finita, recurrente equivale a cerrada"}
En una cadena finita y homogénea, los estados de una misma clase son todos recurrentes o todos transitorios, y

$$
\mathcal C\ \text{recurrente}
\quad\Longleftrightarrow\quad
\mathcal C\ \text{cerrada}.
$$

- **Condición.** Finita, para la dirección «cerrada ⇒ recurrente». La otra vale siempre.
- **Lectura.** Para saber si la cadena regresa no hace falta calcular $f_s$: basta preguntar si sale una flecha de la clase.
- **Casos nulos.** Un estado absorbente es recurrente: $f_s=1$ en un paso. Un estado al que ninguna flecha regresa tiene $f_s=0$.
:::

::: proof {#mkv-c2-cl-dem-recurrente-cerrada of="mkv-c2-teo-recurrente-cerrada"}
**Abierta ⇒ transitoria.** Sea $s\in\mathcal C$ con una flecha a $s'\notin\mathcal C$. Desde $s'$ no hay camino de vuelta a $\mathcal C$: si lo hubiera, $s'$ estaría en $\mathcal C$. Para cualquier $u\in\mathcal C$, toma un camino más corto de $u$ a $s$ y añade la flecha a $s'$. Tiene probabilidad positiva, no repite $u$ y no regresa. Entonces $f_u<1$.

**Cerrada ⇒ recurrente (idea).** Dentro de una clase cerrada, la cadena pasa infinitos pasos en un número finito de estados. Si todos fueran transitorios, cada uno se visitaría finitas veces: no alcanzarían para tantos pasos. Así que alguno es recurrente. Que todos los de una clase compartan el tipo es un resultado clásico que citamos sin probarlo.
:::

> [!WARNING]
> **Creer que «cerrada ⇒ recurrente» vale siempre.** En los enteros, la caminata que sube con probabilidad $2/3$ y baja con $1/3$ tiene una sola clase, cerrada.
> **Aun así la cadena se va hacia arriba y no regresa seguro: con infinitos estados, cerrada no basta.**

**En el juguete.**

- **$s_1$ es transitorio:** ninguna flecha llega a $s_1$, así que $f_{s_1}=0$. Su clase es abierta.
- **$s_2$ y $s_3$ son recurrentes:** desde $s_2$, la cadena está otra vez en $s_2$ en el paso 2, seguro.
- **$s_4$ y $s_5$ son recurrentes:** desde $s_4$, regresa en el paso 1 con $1/2$, o en el paso 2 pasando por $s_5$ con $1/2$.

::: exercise {#mkv-c2-cl-ej-regreso-t4 title="Calcula un regreso que no es seguro"}
En la matriz de tres estados de los ejercicios anteriores, ¿cuánto vale $f_{s_1}$? ¿Es $s_1$ transitorio?
:::

::: hint {#mkv-c2-cl-pista-regreso-t4 of="mkv-c2-cl-ej-regreso-t4" title="¿Qué pasa si la cadena sale de s₁?"}
Si el primer paso va a $s_2$ o a $s_3$, ¿puede volver después?
:::

::: answer {#mkv-c2-cl-resp-regreso-t4 of="mkv-c2-cl-ej-regreso-t4"}
$$
f_{s_1}=P_{s_1s_1}=\tfrac12<1.
$$

**Sí, transitorio:** solo regresa por el lazo en el paso 1. Si sale, cae en un absorbente y no vuelve. Regresa a veces, pero no seguro.
:::

Clasificar en recurrentes ya dice dónde se queda la cadena. Falta saber **cuándo** puede regresar.

---

## 4 · Medir el periodo

**Piensa: ¿en qué pasos puede regresar la cadena a un estado?**

En los que tengan un camino de regreso con esa longitud. El periodo es el ritmo común de esas longitudes.

::: definition {#mkv-c2-def-periodo title="Periodo y estado aperiódico"}
Si la cadena puede regresar a $s$:

$$
\begin{aligned}
d(s)&=\operatorname{mcd}\{t\ge1:(P^t)_{ss}>0\},\\
s\ \text{aperiódico}
\ &\Longleftrightarrow\ d(s)=1.
\end{aligned}
$$

- **Qué es:** $d(s)$, «de de ese», es el máximo común divisor de los pasos en que es posible regresar a $s$.
- **Cómo se calcula:** tomas los recorridos que empiezan y terminan en $s$, aunque repitan estados intermedios, y sacas el máximo común divisor de sus longitudes.
- **Qué significa:** con $d(s)=d$, empezando en $s$, la cadena solo puede volver a estar en $s$ en pasos múltiplos de $d$.
- **Qué no es:** $d(s)=2$ no garantiza regresar en el paso 2; solo prohíbe regresar en pasos impares.
:::

- **Sin regreso:** si ningún camino vuelve a $s$, el conjunto es vacío y no definimos $d(s)$.

El periodo es de la clase, no de un estado suelto, y un lazo lo resuelve.

::: theorem {#mkv-c2-cl-teo-periodo-clase title="La clase comparte el periodo y un lazo lo vuelve 1"}
Si $s\leftrightarrow s'$ y la cadena puede regresar a $s$ en algún paso $t\ge1$, entonces $d(s)=d(s')$. Si algún estado de la clase tiene $P_{ss}>0$, toda la clase es aperiódica.

- **Condición.** Los dos estados se comunican y hay algún regreso; con $s\ne s'$ siempre lo hay: ir y volver. El lazo es suficiente, **no necesario**.
- **Lectura.** Basta calcular el periodo en el estado más fácil de la clase.
- **Casos nulos.** Una clase de un solo estado sin lazo no tiene regreso, y por eso no tiene periodo.
:::

::: proof {#mkv-c2-cl-dem-periodo-clase of="mkv-c2-cl-teo-periodo-clase"}
Sean $a$ y $b$ las longitudes de un camino de $s$ a $s'$ y de uno de $s'$ a $s$. Ir y volver da un regreso a $s$ de $a+b$ pasos. Si además hay un regreso a $s'$ de $t$ pasos, intercalarlo da otro regreso a $s$ de $a+t+b$ pasos.

$d(s)$ divide a $a+b$ y a $a+t+b$, luego divide a $t$. Así $d(s)$ divide a $d(s')$; por simetría, son iguales. Con un lazo, $t=1$ es un regreso y el máximo común divisor es 1.
:::

**En el juguete.**

- **$\{s_2,s_3\}$ tiene periodo 2:** los regresos a $s_2$ ocurren en los pasos 2, 4, 6, … y nunca en un impar.
- **$\{s_4,s_5\}$ es aperiódica:** $s_4$ tiene lazo. En $s_5$ se ve igual: regresa en 2 y en 3 pasos, y $\operatorname{mcd}\{2,3\}=1$.
- **$\{s_1\}$ no tiene periodo:** la cadena nunca regresa a $s_1$.

**Las dos cadenas de la clase 1.** La de la frase V/C tiene una sola clase cerrada, aperiódica: los dos estados se comunican y V tiene lazo, $2/11$. La alternante, con filas $(0,\ 1)$ y $(1,\ 0)$, tiene una sola clase cerrada con periodo 2.

::: exercise {#mkv-c2-cl-ej-periodo-4-6 title="Interpreta un periodo"}
La cadena puede regresar a $s$ en 4 y en 6 pasos, y en ningún número impar. ¿Cuánto vale $d(s)$? ¿Puede asegurarse que regresa en 2 pasos?
:::

::: hint {#mkv-c2-cl-pista-periodo-4-6 of="mkv-c2-cl-ej-periodo-4-6" title="¿Qué divide a todas las longitudes?"}
¿Qué te dice cada dato por separado: el mcd de 4 y 6, y la ausencia de regresos impares?
:::

::: answer {#mkv-c2-cl-resp-periodo-4-6 of="mkv-c2-cl-ej-periodo-4-6"}
**$d(s)=2$.** Con regresos de 4 y 6 pasos, $d(s)$ divide a 2; sin regresos impares, $d(s)$ es par. No se puede asegurar el regreso en 2 pasos: el dato no lo confirma ni lo excluye. El periodo solo dice que todo regreso es par.
:::

Falta un orden para hacer todas estas preguntas con una matriz concreta.

---

## 5 · Clasificar a mano una cadena

**Piensa: con una matriz en la mano, ¿en qué orden haces las preguntas?**

Primero las piezas, luego las flechas que salen, al final el periodo. Para $k$ estados:

1. **Dibuja el grafo.** Una flecha por cada entrada positiva de $P$; los números no importan.
2. **Lista lo alcanzable.** Desde cada estado, anota a qué estados llega por algún camino.
3. **Agrupa.** $s$ y $s'$ van juntos si cada uno aparece en la lista del otro: son las clases.
4. **Pregunta por la salida.** ¿Sale alguna flecha de la clase? Si sale, es abierta y transitoria; si no, cerrada y recurrente, por @mkv-c2-teo-recurrente-cerrada.
5. **Mide el periodo** de cada clase cerrada: busca un lazo; si no hay, el máximo común divisor de las longitudes de los regresos, aunque repitan estados.

**En el juguete.** Los pasos 2 y 3, con las flechas de la sección 1:

::: table {#mkv-c2-cl-tabla-alcanza title="Lo que alcanza cada estado del juguete"}
| Estado | Alcanza a | Clase |
|---|---|---|
| $s_1$ | $s_1,s_2,s_3,s_4,s_5$ | $\{s_1\}$ |
| $s_2$ | $s_2,s_3$ | $\{s_2,s_3\}$ |
| $s_3$ | $s_2,s_3$ | $\{s_2,s_3\}$ |
| $s_4$ | $s_4,s_5$ | $\{s_4,s_5\}$ |
| $s_5$ | $s_4,s_5$ | $\{s_4,s_5\}$ |
:::

Los pasos 4 y 5:

::: table {#mkv-c2-cl-tabla-clases title="Las tres clases del juguete"}
| Clase | ¿Sale? | Tipo | Periodo |
|---|---|---|---|
| $\{s_1\}$ | sí | abierta, transitoria | no tiene |
| $\{s_2,s_3\}$ | no | cerrada, recurrente | 2 |
| $\{s_4,s_5\}$ | no | cerrada, recurrente | 1 |
:::

De $\{s_1\}$ salen flechas a $s_2$ y a $s_4$. El periodo 1 de $\{s_4,s_5\}$ lo da el lazo en $s_4$.

::: figure {#mkv-c2-fig-grafo-clasificar title="Las tres clases del juguete de cinco estados"}
![Grafo de cinco estados. s1, en un recuadro punteado rotulado abierta, manda flechas de 1/2 a s2 y a s4. s2 y s3, en un recuadro rotulado cerrada, periodo 2, se mandan flechas de 1. s4 y s5, en un recuadro rotulado cerrada, aperiódica, tienen la flecha de s4 a s5 de 1/2, la de s5 a s4 de 1 y un lazo en s4 de 1/2.](../_assets/mkv-c2-grafo-clasificar.svg)
:::

- **Lo que se lee:** desde $s_1$, la cadena sale en el primer paso, seguro. Cae en $\{s_2,s_3\}$ o en $\{s_4,s_5\}$ con $1/2$ cada una, y ahí se queda.
- **En general:** con $k$ estados el procedimiento es el mismo; solo crecen las listas del paso 2.

::: exercise {#mkv-c2-cl-ej-cambia-s5 title="Reclasifica tras cambiar una fila"}
En el juguete, cambia solo la fila de $s_5$: ahora va a $s_4$ con $1/2$ y a $s_1$ con $1/2$. ¿Qué clases quedan y cuáles son cerradas?
:::

::: hint {#mkv-c2-cl-pista-cambia-s5 of="mkv-c2-cl-ej-cambia-s5" title="¿Quién alcanza ahora a s₁?"}
¿Qué estados tienen ahora a $s_1$ en su lista de alcanzables?
:::

::: answer {#mkv-c2-cl-resp-cambia-s5 of="mkv-c2-cl-ej-cambia-s5"}
- **$\{s_1,s_4,s_5\}$:** $s_1\to s_4\to s_5\to s_1$. Es abierta: $s_1$ manda una flecha a $s_2$. Sus tres estados son transitorios.
- **$\{s_2,s_3\}$:** sigue cerrada, con periodo 2. Es la única clase cerrada.
:::

Con esto sabemos dónde puede quedarse la cadena. La pregunta siguiente es qué distribución tiene, a la larga, dentro de esas clases.

---

## Ejercicios

::: exercise {#mkv-c2-cl-ej-sin-lazo title="Clasifica una cadena sin lazos"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Una cadena de cinco estados tiene estas flechas, y ninguna más: $s_1\to s_2$ y $s_1\to s_4$, con $1/2$ cada una; $s_2\to s_3$, con 1; $s_3\to s_2$ y $s_3\to s_1$, con $1/2$ cada una; $s_4\to s_5$ y $s_5\to s_4$, con 1.

**Cambia una idea:** cambian las flechas del juguete y ningún estado tiene lazo.

1. **Agrupa:** encuentra las clases.
2. **Decide:** di cuáles son cerradas y qué estados son transitorios o recurrentes. Justifica.
3. **Mide:** calcula el periodo de cada clase.
4. **Concluye:** ¿es irreducible? ¿Basta un lazo para ser aperiódica, o es necesario?
:::

::: hint {#mkv-c2-cl-pista-sin-lazo-1 of="mkv-c2-cl-ej-sin-lazo" title="Pista 1 · ¿Desde dónde se vuelve a s₁?"}
¿Qué estados alcanza cada uno? ¿Cuáles aparecen en la lista del otro?
:::

::: hint {#mkv-c2-cl-pista-sin-lazo-2 of="mkv-c2-cl-ej-sin-lazo" title="Pista 2 · ¿Anotaste todas las longitudes?"}
Para cada estado, ¿revisaste todos los recorridos de regreso, no solo el más corto? ¿Revisaste cada flecha que sale de cada grupo?
:::

::: answer {#mkv-c2-cl-resp-sin-lazo of="mkv-c2-cl-ej-sin-lazo" title="Respuesta · Clasificación de la cadena sin lazos"}
**1. Agrupa.** $s_1\to s_2\to s_3\to s_1$, así que $\{s_1,s_2,s_3\}$ es una clase. $\{s_4,s_5\}$ es otra: nadie de ahí regresa a $s_1$.

**2. Decide.** $\{s_1,s_2,s_3\}$ es abierta por la flecha $s_1\to s_4$: sus estados son transitorios. $\{s_4,s_5\}$ es cerrada: sus estados son recurrentes, por @mkv-c2-teo-recurrente-cerrada.

**3. Mide.** En $s_2$ hay regresos de 2 pasos ($s_2\to s_3\to s_2$) y de 3 ($s_2\to s_3\to s_1\to s_2$): $d=1$. En $\{s_4,s_5\}$ solo hay regresos pares: $d=2$.

**4. Concluye.** No es irreducible: tiene dos clases. La clase grande es aperiódica sin lazo: **el lazo basta, pero no es necesario**.
:::

::: exercise {#mkv-c2-cl-ej-ciclo-k title="Clasifica un ciclo de k estados"}
**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin pedir ayuda a ChatGPT.**

Con $k\ge2$ estados, la cadena va de $s_i$ a $s_{i+1}$ con probabilidad 1, y de $s_k$ a $s_1$.

**Cambia una idea:** ahora $k$ es cualquiera, y después se agrega un lazo.

1. **Clasifica:** ¿cuántas clases hay? ¿Son cerradas? ¿Es irreducible?
2. **Mide:** calcula el periodo.
3. **Modifica:** cambia solo la fila de $s_1$ a $P_{s_1s_1}=P_{s_1s_2}=1/2$. ¿Qué cambia en tus respuestas 1 y 2?
:::

::: hint {#mkv-c2-cl-pista-ciclo-k-1 of="mkv-c2-cl-ej-ciclo-k" title="Pista 1 · ¿Cuántos pasos tarda una vuelta?"}
Empezando en $s_1$, ¿en qué pasos puede estar otra vez en $s_1$?
:::

::: hint {#mkv-c2-cl-pista-ciclo-k-2 of="mkv-c2-cl-ej-ciclo-k" title="Pista 2 · ¿Comprobaste con k = 2?"}
¿Tu respuesta coincide con la alternante de la clase 1? Tras el cambio, ¿siguen las filas sumando 1 y sigue habiendo camino de vuelta?
:::

::: answer {#mkv-c2-cl-resp-ciclo-k of="mkv-c2-cl-ej-ciclo-k" title="Respuesta · Clasificación del ciclo"}
**1. Clasifica.** Siguiendo la vuelta, todos se alcanzan entre sí: una sola clase, cerrada e irreducible. Sus estados son recurrentes.

**2. Mide.** Desde $s_1$ solo se regresa en los pasos $k,2k,3k,\dots$: $d=k$. Con $k=2$ es la alternante, de periodo 2.

**3. Modifica.** La vuelta sigue existiendo, así que la clase sigue siendo una, cerrada e irreducible. El lazo en $s_1$ hace $d=1$ para todos los estados.
:::

**Punto de control:** deberías poder partir una cadena en clases, decir cuáles son cerradas, justificar con @mkv-c2-teo-recurrente-cerrada qué estados son recurrentes y calcular el periodo de cada clase cerrada.

---

## Lo que hay que llevarse

- **Comunicar** (@mkv-c2-def-comunican): ida y vuelta por caminos. Parte los estados en clases.
- **Cerrada** (@mkv-c2-def-clase-cerrada): ninguna flecha sale. Una cadena finita tiene al menos una.
- **Irreducible:** una sola clase que lo abarca todo; es la condición de @mkv-c1-teo-recuperar.
- **Recurrente o transitorio** (@mkv-c2-def-transitorio): regresar seguro o no. En finitas, recurrente ⇔ cerrada (@mkv-c2-teo-recurrente-cerrada); con infinitos estados, cerrada no basta.
- **Periodo** (@mkv-c2-def-periodo): $d(s)=\operatorname{mcd}\{t\ge1:(P^t)_{ss}>0\}$, igual en toda la clase donde está definido. Un lazo basta para $d=1$; no es necesario.
- **El juguete:** $\{s_1\}$ abierta y transitoria; $\{s_2,s_3\}$ cerrada con periodo 2; $\{s_4,s_5\}$ cerrada y aperiódica.
- **La clase 1:** la frase V/C es una clase cerrada aperiódica; la alternante, una cerrada con periodo 2.

Continúa con [[mkv-la-estacionaria|La estacionaria y sus cuatro teoremas]].
