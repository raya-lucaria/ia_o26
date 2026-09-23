---
id: opt-objetivo-salones-practica
title: Asignar salones y decidir qué significa comodidad
nav_title: "Salones: ejemplo guiado"
summary: "Construir una asignación permitida y distinguir reducir la molestia total de atender al grupo con mayor molestia."
status: ready
estimated_time: 30m
tags: [optimizacion, modelado, entera]
---

# Asignar salones y decidir qué significa comodidad

La coordinación debe asignar salón a dos cursos. Parece una tarea pequeña,
pero permite separar dos preguntas: **¿qué asignaciones cumplen las reglas?**
y **¿cuál preferimos entre las que cumplen?**

Vamos a construir el modelo despacio. Antes de cada explicación encontrarás
una pregunta breve: intenta responderla antes de seguir. Los datos son didácticos.

## 1 · Entender qué se necesita

Los cursos A y B se imparten de 9 a 10. Cada uno tiene 20 estudiantes;
sus docentes son distintos y ningún estudiante cursa ambos.

Hay dos salones, 1 y 2. Cada uno tiene 30 lugares, cuenta con proyector y
está disponible durante toda esa hora. La asignación debe respetar lo siguiente:

- Cada curso necesita exactamente un salón durante toda la hora.
- El salón debe tener lugar para todo su grupo.
- A necesita proyector; B no lo necesita.
- Los cursos no pueden compartir salón porque ocurren al mismo tiempo.

Esta es una versión simplificada: **la hora de 9 a 10 está fija para todos**;
solo elegimos el salón. Por eso el modelo no necesita un índice de horario.

**Piensa: ¿basta con que cada grupo quepa en un salón para poder asignarles salón a los dos?**

Además de caber, cada grupo necesita un salón disponible, con el equipo que
requiere y que no se asigne al otro curso. Con los datos de este ejemplo sí
podemos cumplir esas condiciones. Primero escribiremos las reglas que hacen
válida una asignación; después elegiremos cuál preferimos.

## 2 · Representar una asignación

Llamemos $\mathcal C$ al conjunto de cursos y $\mathcal S$ al conjunto de
salones; ambos son finitos y no vacíos. Usaremos el índice $c\in\mathcal C$
para nombrar un curso y el índice $s\in\mathcal S$ para nombrar un salón.
En nuestro ejemplo,

$$\mathcal C=\{A,B\},\qquad\mathcal S=\{1,2\}.$$

**Piensa: ¿cómo registrarías si asignamos el curso A al salón 1?**

Para cada curso $c\in\mathcal C$ y cada salón $s\in\mathcal S$ usamos una
**variable binaria** $x_{cs}\in\{0,1\}$: vale 1 si asignamos el curso $c$ al
salón $s$ y 0 si no.
Por ejemplo, $x_{A1}=1$ significa que A va al salón 1: el primer subíndice
identifica el curso y el segundo, el salón.

La misma definición sirve con más cursos y salones; solo cambian los elementos
de los conjuntos.

Para escribir las reglas con parámetros, damos nombre a los datos conocidos:

- $n_c$: número de estudiantes del curso $c$.
- $a_s$: aforo del salón $s$, en lugares.
- $r_c\in\{0,1\}$: vale 1 si el curso $c$ requiere proyector y 0 si no.
- $p_s\in\{0,1\}$: vale 1 si el salón $s$ tiene proyector y 0 si no.
- $d_s\in\{0,1\}$: disponibilidad del salón $s$ **antes de asignar los cursos**.
  Vale 1 si está libre y autorizado para estos cursos durante toda la hora;
  vale 0 si está cerrado, bloqueado o reservado para otra actividad.

En este ejemplo, $d_1=d_2=1$. Este dato se conoce de antemano y no cambia
cuando elegimos los valores de $x_{cs}$.

## 3 · Construir las obligaciones

**Piensa: ¿cómo escribimos que cada curso debe recibir exactamente un salón?**

Para A, la suma $x_{A1}+x_{A2}$ cuenta los unos: cuántos salones le asignamos.
Debe valer 1. Para cualquier curso $c$, la misma regla se escribe

$$\sum_{s\in\mathcal S}x_{cs}=1\qquad(c\in\mathcal C).$$

**Piensa: ¿cómo evitamos asignar ambos cursos al mismo salón?**

Para el salón 1, $x_{A1}+x_{B1}$ cuenta cuántos cursos lo ocuparían.
Esta cuenta no puede superar 1. La condición para cada salón es

$$\sum_{c\in\mathcal C}x_{cs}\le1\qquad(s\in\mathcal S).$$

El producto $a_sx_{cs}$ aporta los lugares del salón cuando lo elegimos
y cero cuando no. Como cada curso recibe un único salón, sumar esos
productos da la capacidad elegida. Debe alcanzar para el grupo:

$$\sum_{s\in\mathcal S}a_sx_{cs}\ge n_c\qquad(c\in\mathcal C).$$

Con el proyector hacemos lo mismo: la suma indica si el salón elegido
cuenta con él. Debe tenerlo cuando el curso lo requiere:

$$\sum_{s\in\mathcal S}p_sx_{cs}\ge r_c\qquad(c\in\mathcal C).$$

Por último, solo podemos asignar un salón disponible:

$$x_{cs}\le d_s\qquad(c\in\mathcal C,\ s\in\mathcal S).$$

Aquí conviene distinguir **el dato y la decisión**. Que $d_1=1$ permite
asignar A al salón 1, pero no obliga a elegir $x_{A1}=1$. Si $d_1=0$, la
desigualdad obliga a que $x_{A1}=x_{B1}=0$. La disponibilidad indica si
podemos usar ese salón; la suma sobre los cursos evita que lo compartan.

Llamaremos $x$ a la asignación completa, formada por los valores de todas
las variables $x_{cs}$.

Llamaremos **conjunto factible** $F$ al conjunto de asignaciones que cumplen
estas cinco familias de restricciones y todos los dominios binarios.
Escribir $x\in F$ abrevia esas condiciones, sin eliminar ninguna.

Si solo quisiéramos encontrar alguna asignación permitida, el modelo sería

$$\min_{x\in F}\quad 0.$$

El objetivo constante deja empatadas todas las asignaciones factibles.
Todavía no hemos expresado una preferencia por la comodidad.

## 4 · Construir una medida de comodidad

La coordinación pidió a cada grupo valorar el uso de cada salón. Acordaron
una escala común de **puntos de molestia por grupo**: menos es mejor.
Son valoraciones, no distancias ni minutos de traslado.

| Curso | Salón 1 | Salón 2 |
|---|---:|---:|
| A | 0 | 4 |
| B | 4 | 6 |

**Piensa: ¿cómo contarías la molestia de las asignaciones elegidas y dejarías fuera las demás?**

Llamemos $m_{cs}\ge0$ a los puntos del grupo de $c$ si usa el salón $s$. El producto
$m_{cs}x_{cs}$ aporta esos puntos cuando elegimos la asignación y cero cuando
la descartamos. La molestia del grupo queda determinada por

$$M_c(x)=\sum_{s\in\mathcal S}m_{cs}x_{cs}.$$

Una primera propuesta es sumar las molestias de todos los grupos. Supone
que cada punto cuenta igual y que aceptamos compensar más molestia de un
grupo con menos de otro. El modelo completo, usando el conjunto ya definido, es

$$\min_{x\in F}\quad\sum_{c\in\mathcal C}M_c(x).$$

El objetivo está en puntos. Las restricciones siguen midiendo asignaciones,
lugares, equipo y disponibilidad: no sumamos estudiantes a puntos ni convertimos
una molestia alta en una prohibición que nadie pidió.

## 5 · Reunir el modelo general

**Piensa: ¿cómo reunimos la molestia total y todas las reglas en un solo modelo?**

Usamos $M_c(x)$, la molestia del curso $c$ definida en la sección anterior.
El modelo completo es

$$
\begin{aligned}
&\min_x\quad\sum_{c\in\mathcal C}M_c(x)\\
&\text{sujeto a}\\
&\sum_{s\in\mathcal S}x_{cs}=1 &&(c\in\mathcal C),\\
&\sum_{c\in\mathcal C}x_{cs}\le1 &&(s\in\mathcal S),\\
&\sum_{s\in\mathcal S}a_sx_{cs}\ge n_c &&(c\in\mathcal C),\\
&\sum_{s\in\mathcal S}p_sx_{cs}\ge r_c &&(c\in\mathcal C),\\
&x_{cs}\le d_s &&\left(\substack{c\in\mathcal C\\s\in\mathcal S}\right),\\
&x_{cs}\in\{0,1\} &&\left(\substack{c\in\mathcal C\\s\in\mathcal S}\right).
\end{aligned}
$$

Las condiciones entre paréntesis indican para qué cursos o salones debe
cumplirse cada restricción. Las dos últimas se aplican a **cada pareja
curso–salón**.

Para nuestro caso, los datos son:

- Estudiantes: $n_A=n_B=20$.
- Aforo: $a_1=a_2=30$.
- Requieren proyector: $r_A=1$, $r_B=0$.
- Tienen proyector: $p_1=p_2=1$.
- Están disponibles: $d_1=d_2=1$.
- Molestias $m_{cs}$: los valores 0, 4, 4 y 6 de la tabla anterior.

Aquí la capacidad y el proyector no descartan ninguna asignación que cumpla
las otras reglas. Conservamos esas restricciones porque el modelo también
sirve cuando cambian los datos. Para buscar solo una asignación factible,
sustituimos el objetivo por cero y mantenemos todas las restricciones y dominios.

## 6 · Revisar qué preferencia expresa la suma

**Piensa: ¿reducir la molestia total siempre ayuda al grupo que recibe más molestia?**

Comparemos dos asignaciones factibles. Las columnas A y B muestran los
puntos de molestia de cada grupo.

| Asignación | A | B |
|---|---:|---:|
| A en 1, B en 2 | 0 | 6 |
| A en 2, B en 1 | 4 | 4 |

La primera suma $0+6=6$ puntos; la segunda, $4+4=8$. La suma prefiere la
primera, aunque B recibe más molestia. Si queremos atender al grupo con
**mayor molestia**, compararemos 6 con 4 y preferiremos la segunda.

Esa otra prioridad conserva las asignaciones permitidas y cambia el objetivo:

$$\min_{x\in F}\quad\max_{c\in\mathcal C}M_c(x).$$

Con estos datos, el máximo compara $4x_{A2}$ con $4x_{B1}+6x_{B2}$.
No hay un rival que elija perjudicarnos: comparamos los efectos de nuestra
propia asignación sobre grupos distintos.

Minimizar el máximo no garantiza igualdad ni distingue asignaciones con el
mismo máximo y distinta suma. Además, los puntos son por grupo; si los grupos
tuvieran tamaños distintos, dar el mismo peso a grupos o a personas requeriría
otra decisión. Capacidad y equipo no resuelven ninguna de esas preferencias.

## 7 · Resumen del modelo

Todos los cursos ocurren durante la misma hora fija. Los cursos tienen
docentes distintos y ningún estudiante cursa más de uno. Distinguimos los
**datos conocidos** de las **variables que elegimos**; los índices permiten
escribir las mismas reglas para cualquier cantidad de cursos y salones.

| Símbolo | Qué representa |
|---|---|
| $\mathcal C$ | Conjunto de cursos |
| $\mathcal S$ | Conjunto de salones |
| $c$ | Índice de curso |
| $s$ | Índice de salón |
| $x_{cs}$ | Asignar curso a salón |
| $x$ | Asignación completa |
| $x^*$ | Asignación óptima |
| $n_c$ | Número de estudiantes |
| $a_s$ | Aforo en lugares |
| $r_c$ | Requiere proyector |
| $p_s$ | Proyector en el salón |
| $d_s$ | Disponibilidad previa |
| $m_{cs}$ | Molestia por asignación |
| $M_c(x)$ | Molestia del grupo |
| $z$ | Cota de molestia |
| $F$ | Asignaciones factibles |

Los conjuntos $\mathcal C$ y $\mathcal S$ son finitos y no vacíos, con
índices $c\in\mathcal C$ y $s\in\mathcal S$.

La **variable binaria** $x_{cs}$ vale 1 si asignamos el curso $c$ al salón $s$
y 0 si no. La colección de todos esos valores forma la asignación $x$.
Estas son las decisiones sobre qué haremos con los cursos. Su dominio es
$\{0,1\}$: una decisión del mundo no tiene por qué ser una variable continua.

Los **datos** $n_c$ y $a_s$ son enteros no negativos: cuentan estudiantes
y lugares, respectivamente. Los datos $r_c$, $p_s$ y $d_s$ son binarios:

- $r_c=1$ si el curso requiere proyector; 0 si no.
- $p_s=1$ si el salón tiene proyector; 0 si no.
- $d_s=1$ si el salón está libre y autorizado toda la hora; 0 si está cerrado,
  bloqueado o reservado. Es un dato **previo a la asignación**.

El dato $m_{cs}\ge0$ es real y mide puntos de molestia del grupo de $c$ al
usar $s$. La **expresión** $M_c(x)$ calcula la molestia de ese grupo, en puntos:

$$M_c(x)=\sum_{s\in\mathcal S}m_{cs}x_{cs}.$$

El **conjunto factible** $F$ reúne las asignaciones que cumplen las cinco
familias de restricciones y el dominio binario del modelo siguiente.

Para **minimizar la molestia total**, el modelo completo es

$$
\begin{aligned}
&\min_x\quad\sum_{c\in\mathcal C}\sum_{s\in\mathcal S}m_{cs}x_{cs}\\
&\text{sujeto a}\\
&\sum_{s\in\mathcal S}x_{cs}=1 &&(c\in\mathcal C),\\
&\sum_{c\in\mathcal C}x_{cs}\le1 &&(s\in\mathcal S),\\
&\sum_{s\in\mathcal S}a_sx_{cs}\ge n_c &&(c\in\mathcal C),\\
&\sum_{s\in\mathcal S}p_sx_{cs}\ge r_c &&(c\in\mathcal C),\\
&x_{cs}\le d_s &&\left(\substack{c\in\mathcal C\\s\in\mathcal S}\right),\\
&x_{cs}\in\{0,1\} &&\left(\substack{c\in\mathcal C\\s\in\mathcal S}\right).
\end{aligned}
$$

Las cinco familias exigen, en orden: un salón por curso, como máximo un
curso por salón, capacidad suficiente, proyector cuando se requiere y
disponibilidad previa. Las dos últimas filas se aplican a cada pareja
curso–salón.

Este es un modelo de **programación lineal entera binaria**, con estructura
de asignación: el objetivo y las restricciones son lineales, pero las
decisiones $x_{cs}$ solo pueden valer 0 o 1.

**El mínimo es un valor; una asignación que lo alcanza es una decisión.**
Si $F$ no está vacío, podemos elegir una asignación óptima escribiendo

$$x^*\in\operatorname*{arg\,min}_{x\in F}
\sum_{c\in\mathcal C}M_c(x).$$

`arg min` recoge las asignaciones que alcanzan el menor valor. Usamos
pertenencia porque puede haber varias empatadas; no devuelve necesariamente
una única asignación.

Si la prioridad es reducir la **mayor molestia de un grupo**, conservamos
las mismas restricciones y dominios y cambiamos solo el objetivo:

$$\min_{x\in F}\quad\max_{c\in\mathcal C}M_c(x).$$

Si hay asignaciones factibles, elegimos una bajo esta otra prioridad con

$$x^*\in\operatorname*{arg\,min}_{x\in F}
\max_{c\in\mathcal C}M_c(x).$$

El máximo no es una expresión lineal. Podemos escribir un modelo equivalente
con una variable real $z$ que acote por arriba la molestia de cada grupo:

$$
\begin{aligned}
&\min_{x,z}\quad z\\
&\text{sujeto a}\quad x\in F,\\
&z\ge M_c(x) &&(c\in\mathcal C),\\
&z\in\mathbb R_{\ge0}.
\end{aligned}
$$

Al minimizar $z$, esa cota baja hasta la mayor molestia. Esta formulación es
**programación lineal entera mixta**: combina las variables binarias de la
asignación con la variable continua $z$, mediante expresiones lineales.

$z$ es una **variable auxiliar** de la reformulación: no decide otro salón.
Aquí «real» describe su dominio $\mathbb R_{\ge0}$. En cambio, $m_{cs}$ es un
dato real conocido y $M_c(x)$ es una expresión calculada; ninguno es una
decisión adicional.

Para buscar únicamente una asignación factible, usamos el objetivo constante
cero con esas mismas condiciones: $\min_{x\in F}0$.
Es un problema de **factibilidad de una asignación binaria con restricciones
lineales**; basta encontrar una asignación permitida.

Si $F$ no está vacío, todas sus asignaciones alcanzan el mismo valor cero:

$$x^*\in\operatorname*{arg\,min}_{x\in F}0=F.$$

Si no hay asignaciones factibles, no existe una decisión que devolver.

**¿Cómo podrían resolverse?** En una instancia pequeña podemos enumerar las
asignaciones, descartar las prohibidas y comparar las restantes según el
objetivo; para factibilidad, podemos detenernos al encontrar una permitida.

Sean $N=|\mathcal C|$ cursos y $R=|\mathcal S|$ salones. Elegir un salón para
cada curso genera $R^N$ candidatos, incluidos los que incumplen otras reglas.
Una comprobación directa que recorra las $NR$ variables y evalúe el objetivo
cuesta $O(NR)$ operaciones por candidato. Para ese procedimiento,

$$T_{\mathrm{enum}}=O\!\left(NR\cdot R^N\right).$$

Esta cota corresponde a la enumeración descrita. Con pocos salones y cursos
puede bastar; para $R\ge2$ fijo, el número de candidatos crece
exponencialmente con $N$.

La [[ramificar-y-acotar|ramificación y acotación]] también puede resolver
las formulaciones lineales enteras y, en el caso general, puede explorar un
árbol exponencial. Esa posibilidad del método no implica que este modelo
de asignación necesite una búsqueda exponencial.

## 8 · Practicar con dos horas posibles

**Haz primero un esfuerzo por escribir tu propio modelo, sin abrir las pistas ni la solución y sin pedir ayuda a ChatGPT. Después de intentarlo, usa las pistas una por una y vuelve a tu hoja antes de abrir la respuesta.**

::: exercise {#opt-obj-sal-dos-horas title="Cuatro clases, dos salones y un proyector"}
La coordinación debe organizar las clases A, B, C y D. Cada una tiene
20 estudiantes, dura una hora completa y debe impartirse exactamente una
vez. Sus docentes son distintos y ningún estudiante toma más de una de
estas clases.

Puede usar dos bloques: de 9 a 10 y de 10 a 11. **Ninguna clase tiene una
hora fijada**; docentes y estudiantes están disponibles en ambos bloques.

Hay dos salones, llamados 1 y 2, con 30 lugares cada uno. Ambos están
disponibles durante los dos bloques. Solo el salón 1 tiene proyector:
A y C lo necesitan; B y D no. No se puede trasladar el proyector.

Cada clase debe ocupar un único salón durante su hora completa. Dos clases
no pueden compartir salón a la misma hora. La coordinación solo pide
**encontrar un horario que cumpla las reglas**; no ha establecido preferencias
por salón ni por hora.

Formula un modelo general: define los conjuntos, los índices, los datos,
las decisiones y todas las condiciones. Después usa estos datos para dar
un horario de ejemplo y comprueba que cumple las reglas. Indica qué tipo
de modelo obtuviste y un método para buscar una solución, distinguiendo
cuántos candidatos revisa del costo de revisar cada uno.
:::

::: hint {#opt-obj-sal-dos-horas-p1 of="opt-obj-sal-dos-horas" title="Pista 1 · Qué hay que decidir ahora"}
Antes la hora estaba fijada. Ahora piensa qué información debe contener
la decisión correspondiente a una clase para que podamos colocarla en
una agenda. Separa esa elección de las características y la disponibilidad
de cada salón, que ya conocemos.
:::

::: hint {#opt-obj-sal-dos-horas-p2 of="opt-obj-sal-dos-horas" title="Pista 2 · Qué ocupaciones son incompatibles"}
Elegir el mismo salón para dos clases no siempre provoca un conflicto.
¿Qué otra parte de sus asignaciones tendría que coincidir? Revisa también
cómo distinguirías exigir proyector de tenerlo disponible. Al final,
comprueba si has impartido alguna clase dos veces o dejado alguna fuera.
:::

::: answer {#opt-obj-sal-dos-horas-resp of="opt-obj-sal-dos-horas" title="Respuesta · Elegir salón y hora para cada clase"}
**1. Separar datos y decisiones.** Sean $\mathcal C$, $\mathcal S$ y
$\mathcal H$ conjuntos finitos, no vacíos, de clases, salones y bloques de
una hora. Los índices $c\in\mathcal C$, $s\in\mathcal S$ y
$h\in\mathcal H$ identifican una clase, un salón y un bloque.

Todas las clases duran un bloque completo y pueden impartirse en cualquiera
de ellos. Los docentes son distintos, están disponibles en todos los bloques
y ningún estudiante cursa más de una clase. Cada salón puede recibir una
sola clase por bloque.

| Signo | Qué representa |
|---|---|
| $\mathcal C$ | Clases |
| $\mathcal S$ | Salones |
| $\mathcal H$ | Bloques de una hora |
| $c,s,h$ | Clase, salón, bloque |
| $n_c$ | Estudiantes de la clase |
| $a_s$ | Aforo del salón |
| $r_c$ | Requiere proyector |
| $p_s$ | Salón con proyector |
| $d_{sh}$ | Disponibilidad previa |
| $x_{csh}$ | Clase en salón y bloque |
| $x$ | Horario completo |
| $F_{\mathrm{hor}}$ | Horarios factibles |

Los datos $n_c$ y $a_s$ son enteros no negativos. Los datos $r_c$, $p_s$ y
$d_{sh}$ son binarios. La disponibilidad $d_{sh}=1$ significa que el salón
$s$ está libre y autorizado en el bloque $h$ **antes de asignar las clases**;
si vale cero, no podemos usarlo en ese bloque.

Usamos una **variable binaria** $x_{csh}$: vale 1 si impartimos la clase $c$
en el salón $s$ durante el bloque $h$, y 0 si no. La colección de todas
esas decisiones forma el horario $x$. Ahora elegimos también la hora;
el índice $h$ no es un dato fijo de cada clase.

**2. Reunir el modelo.** Una clase debe recibir exactamente una pareja
salón–bloque. Un salón puede reutilizarse en otro bloque; por eso la
exclusividad se exige para cada pareja $s,h$.

$$
\begin{aligned}
&\min_x\quad 0\\
&\text{sujeto a}\\
&\sum_{s\in\mathcal S}\sum_{h\in\mathcal H}x_{csh}=1
&& (c\in\mathcal C),\\
&\sum_{c\in\mathcal C}x_{csh}\le1
&& \left(\substack{s\in\mathcal S\\h\in\mathcal H}\right),\\
&\sum_{s\in\mathcal S}\sum_{h\in\mathcal H}a_sx_{csh}\ge n_c
&& (c\in\mathcal C),\\
&\sum_{s\in\mathcal S}\sum_{h\in\mathcal H}p_sx_{csh}\ge r_c
&& (c\in\mathcal C),\\
&x_{csh}\le d_{sh}
&& \left(\substack{c\in\mathcal C\\s\in\mathcal S\\h\in\mathcal H}\right),\\
&x_{csh}\in\{0,1\}
&& \left(\substack{c\in\mathcal C\\s\in\mathcal S\\h\in\mathcal H}\right).
\end{aligned}
$$

Las dos sumas de capacidad y proyector recuperan las características del
único salón–bloque elegido para cada clase. Las últimas dos filas se
aplican a cada triple $c,s,h$.

Llamamos $F_{\mathrm{hor}}$ al conjunto de horarios que cumplen todas estas
condiciones. Si no está vacío, el valor óptimo es cero y cualquier horario
factible lo alcanza:

$$x^*\in\operatorname*{arg\,min}_{x\in F_{\mathrm{hor}}}0.$$

No añadimos costos de molestia: el enunciado no proporciona esas preferencias.
Los parámetros son datos y las únicas decisiones son las variables binarias;
este modelo no necesita variables auxiliares continuas.

**3. Usar los datos y comprobar un horario.** En esta instancia,

$$\mathcal C=\{A,B,C,D\},\qquad\mathcal S=\{1,2\}.$$

Los bloques son $\mathcal H=\{1,2\}$: el 1 va de 9 a 10 y el 2, de 10 a 11.
Los demás datos son:

- $n_c=20$ para cada clase y $a_1=a_2=30$.
- $r_A=r_C=1$ y $r_B=r_D=0$.
- $p_1=1$ y $p_2=0$.
- $d_{sh}=1$ para ambos salones en ambos bloques.

Un horario permitido es el siguiente:

| Bloque | Salón 1 | Salón 2 |
|---|---|---|
| 9–10 | A | B |
| 10–11 | C | D |

En variables, $x_{A,1,1}$, $x_{B,2,1}$, $x_{C,1,2}$ y $x_{D,2,2}$ valen 1;
las demás valen 0. Cada clase aparece una vez, ningún salón recibe dos clases
en un bloque y todos los grupos caben. A y C usan el salón con proyector,
en horas distintas. Los dos bloques y los dos salones estaban disponibles.
Por tanto, el horario pertenece a $F_{\mathrm{hor}}$.

**4. Tipo de modelo, método y costo.** Es un problema de factibilidad con
variables binarias y restricciones lineales: puede escribirse como
programación lineal entera binaria con objetivo cero.

Para enumerar, sean $N=|\mathcal C|$, $R=|\mathcal S|$ y $H=|\mathcal H|$.
Cada clase puede elegir una de $RH$ parejas salón–bloque. Esto produce
$(RH)^N$ candidatos antes de comprobar las otras reglas. Recorrer todas las
$NRH$ variables para revisar un candidato cuesta $O(NRH)$ operaciones.
La cota para esa enumeración directa es

$$T_{\mathrm{enum}}=O\!\left(NRH\cdot(RH)^N\right).$$

Aquí hay $N=4$, $R=2$ y $H=2$: son $4^4=256$ candidatos, no 256 horarios
factibles. Podemos detenernos al encontrar uno que cumpla las reglas;
si ninguno las cumple, se agota la búsqueda. Las cuentas usan operaciones
aritméticas como unidades y describen este procedimiento, no un costo
obligatorio de todos los métodos. También puede aplicarse ramificación y
acotación a la formulación binaria.
:::

Continúa con [[opt-objetivo-panaderia-practica|cómo decidir cuánto pan producir cuando la demanda es incierta]].

Para practicar después: [[opt-practica-horarios|decidir también las horas de inicio]]. La [[opt-objetivo-salones-modelo|consulta opcional de salones y horarios]] reúne la formulación más general.
