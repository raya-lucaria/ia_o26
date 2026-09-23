---
id: opt-objetivo-juego-practica
title: Elegir una jugada cuando el rival responde
nav_title: Juego
summary: "Representar la elección del rival y comprobar por qué conservar más fichas puede llevarnos a perder."
status: ready
estimated_time: 20m
tags: [optimizacion, modelado, juegos]
---

# Elegir una jugada cuando el rival responde

Hasta ahora comparábamos decisiones usando datos sobre sus consecuencias.
En un juego aparece otra dificultad: **la consecuencia también depende de
lo que decida otra persona**. Queremos ganar, pero el rival también.

Usaremos un juego pequeño cuyos resultados conocemos por completo. No
necesitamos saber ajedrez ni estudiar todavía un algoritmo para elegir jugadas.

## 1 · Separar nuestra jugada de la respuesta rival

Puedes **Guardar** una ficha o **Sacrificarla**. Después, el rival observa
tu acción y elige una respuesta llamada I o D. Las letras solo distinguen
sus dos opciones.

No hay azar: una misma combinación de acciones produce siempre el mismo
resultado. El juego es **determinista**. Después de esas dos decisiones,
los movimientos restantes son obligatorios y nadie puede cambiar el final.

Las columnas I y D son las respuestas del rival. Los valores son tus puntos:
+1 si ganas y −1 si pierdes.

| Acción | I | D |
|---|---:|---:|
| Guardar | +1 | −1 |
| Sacrificar | +1 | +1 |

Solo valoramos ganar: ni conservar fichas ni terminar antes da puntos.
El rival recibe la puntuación contraria. Ambas puntuaciones suman cero;
por eso es un juego de **suma cero**, no simplemente porque haya dos jugadores.

Ambos conocen la tabla. Suponemos que el rival elige la respuesta que más
le conviene: si puede hacernos perder, lo hace.

**¿Conocer las dos respuestas significa que podemos elegir una por él?**

No. Nosotros elegimos una fila; el rival elige una columna de esa fila.
Para escribir el modelo, separamos los datos de esas decisiones:

- $A$ es el conjunto de nuestras acciones permitidas.
- $B(a)$ contiene las respuestas permitidas al rival después de nuestra acción $a$.
- $U(a,b)$ es nuestra puntuación final, o **utilidad**, para esa combinación.

Los conjuntos son finitos y no vacíos. Son datos conocidos, igual que $U$.
Elegimos $a$; el rival elige $b$ después de observarnos. Las acciones no
tienen unidades físicas; la utilidad se mide en los puntos acordados.

## 2 · Construir el valor de una acción

**Si una fila permite ganar o perder, ¿qué resultado puede imponernos el rival?**

Como su utilidad es $-U$, obtener más puntos para él significa dejarnos
menos a nosotros. Para una acción propia ya fijada, el valor que podemos
asegurar es el menor entre sus respuestas permitidas:

$$v(a)=\min_{b\in B(a)}U(a,b).$$

Este número resume una fila de la tabla y se mide en los mismos puntos
que $U$. No podemos elegirlo libremente: depende de la acción y de los
resultados que deja disponibles al rival.

Ahora comparamos nuestras acciones. Queremos que ese valor sea lo más
alto posible, por lo que el modelo completo es

$$\begin{aligned}
\max_a\quad &\min_{b\in B(a)}U(a,b)\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

**El máximo representa nuestra elección; el mínimo, la del rival.** Los
conjuntos $A$ y $B(a)$ contienen los dominios y todas las jugadas permitidas.
No hay otras restricciones de recursos. Maximizar conjuntamente sobre
$a$ y $b$ nos daría control sobre ambos jugadores y cambiaría el problema.

## 3 · Comprobar el modelo con los resultados conocidos

Abreviamos Guardar con $G$ y Sacrificar con $S$. Al sustituir los datos,
los conjuntos son $A=\{G,S\}$ y $B(G)=B(S)=\{I,D\}$. El modelo queda

$$\max_{a\in\{G,S\}}\min\{U(a,I),U(a,D)\}.$$

Cada acción recibe este valor:

$$v(G)=\min\{1,-1\}=-1,\qquad v(S)=\min\{1,1\}=1.$$

Sacrificar asegura la victoria con estas reglas. Guardar deja al rival
una respuesta que nos derrota. Si miráramos solo el mejor resultado de
cada fila, ambas recibirían un 1 y ocultaríamos esa diferencia.

Un máximo y un mínimo no implican por sí solos que exista un rival. En
salones podíamos atender al grupo con mayor molestia sin suponer que nadie
nos atacara. Aquí sí hay otra persona eligiendo según sus intereses.

Si quisiéramos aprovechar errores frecuentes de un rival, necesitaríamos
datos sobre cómo responde y otro modelo de su conducta. La tabla de
resultados no proporciona probabilidades para promediar sus columnas.

## 4 · Revisar un programa que solo cuenta fichas

**¿Tener más fichas es lo mismo que estar más cerca de ganar?**

Conservamos el juego, pero examinamos un programa que deja de mirar justo
después de la respuesta rival, antes de completar los movimientos obligatorios.
Para valorar la posición alcanzada, cuenta únicamente nuestras fichas.
Las columnas siguen siendo I y D; ahora los valores se miden en fichas:

| Acción | I | D |
|---|---:|---:|
| Guardar | 3 | 2 |
| Sacrificar | 0 | 0 |

Llamamos $s(a,b)$ a esa posición y $h(s)$ a la cantidad de fichas que
cuenta el programa. Ambas quedan determinadas por las jugadas; no son
nuevas decisiones libres. La regla del programa toma el menor conteo de
cada fila y recomienda la acción cuyo conteo mínimo es mayor.

El modelo completo de **esa regla dada al programa** es

$$\begin{aligned}
\max_a\quad &\min_{b\in B(a)}h(s(a,b))\\
\text{sujeto a}\quad &a\in A.
\end{aligned}$$

Conservamos $A=\{G,S\}$ y $B(a)=\{I,D\}$. Para Guardar, el mínimo es
$\min\{3,2\}=2$; para Sacrificar, $\min\{0,0\}=0$. El programa recomienda
Guardar. Calculó bien su criterio, pero la primera tabla muestra que esa
jugada permite al rival derrotarnos.

El programa usa fichas; nosotros comprobamos su recomendación con las
utilidades finales. **Resolver correctamente un modelo no corrige una
puntuación que premia algo distinto de lo que queremos.** Tampoco hemos
supuesto que el rival realmente prefiera quitarnos fichas a ganar.

## 5 · Justificar una puntuación mejor

Una puntuación mejor debe apoyarse en señales que permitan reconocer una
victoria o una derrota. Aquí conocemos los finales y podemos comprobar si
la valoración coincide con ellos. En juegos más grandes, una valoración
aproximada, llamada **heurística**, necesita justificación y puede recomendar
una acción distinta de la que elegiríamos con todos los finales conocidos.
La [[opt-objetivo-juego-modelo|consulta opcional sobre valoraciones]] desarrolla cómo usar esas señales y qué límites tienen.

## 6 · Pasar de dos decisiones a varios turnos

Si después hubiera nuevas decisiones, tendríamos que representar también
esos turnos. Un árbol puede mostrar cada posición y las jugadas que llevan
a otras. En nuestros turnos buscamos valores altos; en los del rival,
valores bajos para nosotros. Esa alternancia lleva a la formulación **minimax**.

Al terminar el juego conocemos la utilidad. Si dejamos de explorar antes,
usamos una evaluación de la posición. Más adelante estudiaremos cómo recorrer
esos árboles y cómo la **poda alfa–beta** permite omitir ramas sin cambiar
el valor de la búsqueda correspondiente. Aquí dejamos planteado qué se compara.

Continúa con [[opt-construir-objetivo|los problemas para practicar]].
