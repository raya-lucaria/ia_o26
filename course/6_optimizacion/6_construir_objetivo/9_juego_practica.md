---
id: opt-objetivo-juego-practica
title: Elegir frente a un rival
nav_title: Juego · Practicar
summary: "Modelar respuestas adversarias y auditar una valoración de posiciones que puede favorecer la decisión equivocada."
status: ready
tags: [optimizacion, modelado, juegos, practica]
---

# Elegir frente a un rival

En un horario podemos minimizar la mayor molestia sin que nadie intente
perjudicarnos. Aquí cambia el supuesto: **otro agente observa nuestra acción
y elige una respuesta con intereses opuestos**. Después veremos qué ocurre
si valoramos posiciones intermedias con una medida incompleta.

## Problema 9 · La mejor acción ante la peor respuesta

::: exercise {#opt-obj-juego-ej-1 title="Modelar una decisión con respuesta adversaria"}
Jugamos un pequeño juego determinista: no hay azar. Nuestra primera acción
puede ser **Guardar** una ficha o **Sacrificarla**. Después, el rival observa
la acción y elige su respuesta **I** o **D**. Estas son todas las opciones.

Tras esa respuesta, el desenlace queda forzado: ya no existen decisiones
que puedan cambiarlo. Los movimientos restantes, si los hay, solo lo
completan. Conocemos el resultado final de cada combinación:

| Nuestra acción | Si el rival responde I | Si el rival responde D |
|---|---:|---:|
| Guardar | Victoria: +1 | Derrota: −1 |
| Sacrificar | Victoria: +1 | Victoria: +1 |

Nuestra utilidad es +1 al ganar y −1 al perder. La del rival es el negativo
de la nuestra: es un juego de **suma cero**. Suponemos que el rival elige
una respuesta que minimiza nuestra utilidad. Las fichas conservadas no
dan puntos al final.

Plantea un problema de optimización para nuestra primera acción. Distingue
la decisión propia de la respuesta rival y explica qué utilidad debe
representar cada acción antes de compararlas. ¿Sería defendible evaluar
cada acción solo por su mejor desenlace posible?
:::

### Primero intenta plantearlo

**NO ABRAS LA PISTA 1 SI TODAVÍA NO HAS HECHO UN INTENTO.**

::: hint {#opt-obj-juego-pista-1a of="opt-obj-juego-ej-1" title="PISTA 1 · Solo si te atoraste"}
La tabla contiene datos conocidos. Elegimos una fila. El rival ve esa fila
y puede escoger cualquiera de sus dos columnas. La utilidad final no cuenta
fichas: solo ganar o perder.
:::

**ABRE LA PISTA 2 SOLO SI SIGUES ATORADO; DESPUÉS VUELVE A TU HOJA.**

::: hint {#opt-obj-juego-pista-1b of="opt-obj-juego-ej-1" title="PISTA 2 · Solo si te atoraste"}
Para una fila ya elegida, ¿qué número buscará un rival que quiere reducir
nuestra utilidad? Una vez resumida cada fila así, ¿qué número preferimos nosotros?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-juego-resp-1 of="opt-obj-juego-ej-1"}
**Datos y decisiones.** Sea $A$ el conjunto finito no vacío de acciones
propias. Para cada $a\in A$, $B(a)$ es el conjunto finito no vacío de
respuestas disponibles al rival. $U(a,b)$ es nuestra utilidad final
conocida. Las acciones no tienen unidades físicas; la utilidad usa los
puntos acordados de victoria y derrota.

Elegimos $a$. La respuesta $b$ la elige el rival después de observarla;
no es una segunda variable que podamos ajustar a nuestro favor.

**Construir el valor de una acción.** Bajo el supuesto adversarial,
el resultado que asignamos a $a$ es

$$v(a)=\min_{b\in B(a)}U(a,b).$$

El mínimo interior representa la elección rival. Nosotros buscamos la
acción con mayor valor. El **modelo general completo** es

$$\begin{aligned}
\max_a\quad &v(a)=\min_{b\in B(a)}U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

Los conjuntos de acciones son los dominios y las reglas de factibilidad;
no faltan restricciones de recursos en este relato.

**Con los datos del ejercicio**, escribimos $G$ por Guardar y $S$ por
Sacrificar. El dominio es $A=\{G,S\}$ y
$B(G)=B(S)=\{I,D\}$. Sustituir en el modelo da

$$\max_{a\in\{G,S\}}\min\{U(a,I),U(a,D)\},$$

con $U(G,I)=1$, $U(G,D)=-1$, $U(S,I)=U(S,D)=1$.
La comprobación es pequeña: $v(G)=\min\{1,-1\}=-1$ y
$v(S)=\min\{1,1\}=1$. Sacrificar asegura la victoria bajo las reglas dadas.

**Qué justifica el objetivo.** El rival observa nuestra acción, conoce los
resultados y busca reducir nuestra utilidad. No estamos promediando
respuestas aleatorias ni eligiéndolas nosotros. Si usáramos el mejor
desenlace de cada fila, ambas acciones tendrían valor 1: ese criterio no
distinguiría la vulnerabilidad de Guardar.

**Qué deja fuera y cómo revisarlo.** La utilidad representa solo ganar o
perder; no valora fichas ni duración. El mínimo tampoco representa una
frecuencia observada de errores del rival. Si quisiéramos aprovechar un
rival que se equivoca de una manera conocida, necesitaríamos datos sobre
sus respuestas y otro modelo de su conducta. Sin esos datos, una media
con pesos inventados no se justifica.
:::

## Problema 10 · Cuando conservar fichas parece ganar

::: exercise {#opt-obj-juego-ej-2 title="Auditar una evaluación de posiciones intermedias"}
Conserva las acciones, las respuestas y los desenlaces del problema 9.
Ahora auditamos un agente que solo examina la posición alcanzada justo
después de la respuesta rival. Se detiene antes de completar los movimientos
forzados que producen la victoria o la derrota.

El agente **valora únicamente las fichas que conserva** en esa posición.
Los valores de su función $h$ están dados en esta tabla:

| Nuestra acción | Posición tras I | Posición tras D |
|---|---:|---:|
| Guardar | 3 fichas | 2 fichas |
| Sacrificar | 0 fichas | 0 fichas |

El agente aplica el mismo criterio de protegerse frente a la respuesta
menos favorable, pero usando $h$ en lugar de la utilidad final.
**Nosotros, como auditores, conocemos también los desenlaces de la tabla
anterior.** No son secretos; la limitación que examinamos es qué información
emplea el agente para evaluar.

Plantea el modelo de su recomendación y compárala con la decisión del
problema 9. Explica por qué contar fichas puede fallar.

Para proponer una revisión, disponemos de una comprobación local de las
posiciones: tras Guardar-I hay llegada inevitable a la meta; tras Guardar-D,
bloqueo que nos hará perder; tras cualquiera de las respuestas a Sacrificar,
llegada inevitable a la meta. Estas señales son observables en este juego
pequeño. Define una valoración que las use y aclara qué tendrías que
comprobar antes de reutilizarla en un juego más grande.
:::

### Primero separa la recomendación de su auditoría

**NO ABRAS LA PISTA 1 SIN ESCRIBIR QUÉ VALORA CADA TABLA.**

::: hint {#opt-obj-juego-pista-2a of="opt-obj-juego-ej-2" title="PISTA 1 · Solo si te atoraste"}
| Información | Uso en esta variante |
|---|---|
| Acciones y respuestas | Las mismas del problema 9 |
| Fichas conservadas | Valoración usada por el agente limitado |
| Victoria o derrota final | Referencia para auditar su recomendación |
| Llegada inevitable o bloqueo | Señales disponibles para revisar la valoración |

Las dos tablas miden cosas distintas y usan escalas distintas.
:::

**ABRE LA PISTA 2 SOLO SI SIGUES ATORADO.**

::: hint {#opt-obj-juego-pista-2b of="opt-obj-juego-ej-2" title="PISTA 2 · Solo si te atoraste"}
¿Cambian las acciones permitidas al sustituir la utilidad final por el
número de fichas? ¿Qué señal debería pesar más si las fichas conservadas
ya no pueden evitar una derrota?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-juego-resp-2 of="opt-obj-juego-ej-2"}
**Datos y decisión.** Conservamos $A$, $B(a)$ y la acción propia $a$.
Llamamos $s(a,b)$ a la posición tras ambas jugadas. La función fija $h(s)$
cuenta nuestras fichas en ella. Ni la posición ni su valoración son
variables libres: resultan de las acciones y de la regla de evaluación.

**Modelo general de la recomendación limitada:**

$$\begin{aligned}
\max_a\quad &\min_{b\in B(a)}h(s(a,b))\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

**Con los datos**, el modelo es

$$\max_{a\in\{G,S\}}\min\{h(s(a,I)),h(s(a,D))\},$$

con valores $h(s(G,I))=3$, $h(s(G,D))=2$ y
$h(s(S,I))=h(s(S,D))=0$. Guardar obtiene mínimo 2 y Sacrificar mínimo 0:
el agente recomienda Guardar. Es el óptimo del criterio que le dimos.

**Auditoría.** La tabla de utilidades finales da valores mínimos $-1$ y $1$,
respectivamente. El criterio intermedio recomienda una acción con la que
el rival puede derrotarnos. Contar material omite el camino a la meta:
tener más fichas no asegura ganar y perder una ficha puede permitirlo.

**Una revisión concreta.** Definimos $W(s)=1$ cuando la señal observada
certifica victoria inevitable y 0 en otro caso; $D(s)=1$ cuando certifica
derrota inevitable y 0 en otro caso. En estos datos ambas señales nunca
valen 1 simultáneamente. Fijamos

$$h'(s)=W(s)-D(s).$$

La nueva escala es de utilidad, con +1 para victoria y −1 para derrota;
ya no es una cantidad de fichas. Las señales dadas producen

$$h'(s(G,I))=1,\quad h'(s(G,D))=-1,\quad
h'(s(S,I))=h'(s(S,D))=1.$$

El **modelo revisado completo** sustituye $h$ por $h'$:

$$\max_{a\in\{G,S\}}\min\{h'(s(a,I)),h'(s(a,D))\}.$$

Ahora recomienda Sacrificar. No elegimos arbitrariamente una puntuación
para favorecer esa acción: usamos señales observables y su relación
especificada con la victoria y la derrota.

**Límite de la revisión.** En este juego la comprobación local basta para
certificar todos los desenlaces. En uno mayor puede haber posiciones
sin ninguna señal concluyente: $W=D=0$ no demostraría empate. Haría falta
justificar otra aproximación o examinar más consecuencias. Una función
heurística, es decir, una valoración aproximada de posiciones, no garantiza
preservar la decisión que tomaríamos con todos los desenlaces conocidos.
:::

Después de comparar tus modelos, pasa a [[opt-objetivo-juego-modelo|la formulación general frente a un rival]].
