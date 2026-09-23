---
id: opt-objetivo-salones-practica
title: Asignar salones y elegir horarios
nav_title: "Salones: práctica"
summary: "Dos modelos para distinguir horarios admisibles, molestia total y atención al grupo peor situado."
status: ready
tags: [optimizacion, modelado, practica]
---

# Asignar salones y elegir horarios

Un horario puede cumplir todas las reglas y aun así resultar incómodo para
algún grupo. En estos dos problemas tendrás que distinguir esas dos preguntas:
qué opciones se permiten y con qué criterio conviene compararlas.

**Tu tarea es formular los modelos y explicar sus objetivos.** No hace falta
buscar el horario óptimo. Los datos son didácticos.

## Problema 1 · Asignar salones con horarios fijos

::: exercise {#opt-obj-sal-fijos title="¿Qué significa una buena asignación?"}
La coordinación debe asignar salón a los cursos A y B. Ambos se imparten de
9 a 10 y tienen 20 estudiantes cada uno. Sus docentes son distintos y ningún
estudiante cursa ambos.

Hay dos salones disponibles durante toda esa hora: R y S. Cada uno tiene
30 lugares y cuenta con proyector. La asignación debe respetar estas condiciones:

- Cada curso necesita exactamente un salón durante toda la hora.
- El salón debe tener lugar para todo el grupo.
- A necesita proyector; B no lo necesita.
- Dos cursos simultáneos no pueden compartir salón.

No hay otras condiciones.

La coordinación quiere que los grupos estén cómodos. Pidió a cada grupo valorar
la molestia de usar cada salón y acordó una escala común de **puntos de molestia por grupo**: menos puntos significan menos molestia.
Son valoraciones de los grupos; no representan distancias ni minutos de traslado.

Todavía falta decidir cómo compararemos la comodidad de una asignación completa.

| Curso | R | S |
|---|---:|---:|
| A | 0 | 4 |
| B | 4 | 6 |

Prepara dos formulaciones:

1. Un modelo que describa **qué asignaciones cumplen las condiciones**, sin
   preferir ninguna.
2. Un modelo que permita compararlas mediante un objetivo. Justifica qué
   entiendes por comodidad y qué preferencia representa tu elección.

Escribe ambos modelos completos, primero con parámetros y luego con estos datos.
Al terminar, explica si capacidad y equipo bastan para determinar qué asignación
es mejor.
:::

### Primero intenta plantearlo

Antes de abrir las pistas, escribe qué decidirías y qué condiciones debe cumplir
tu asignación.

::: hint {#opt-obj-sal-fijos-p1 of="opt-obj-sal-fijos" title="PISTA 1 · Ordenar los datos"}

- **Cursos**: A y B; 20 estudiantes cada uno; misma hora.
- **Recursos**: R y S; 30 lugares y proyector en ambos.
- **Equipo requerido**: A necesita proyector; B no.
- **Disponibilidad**: Ambos salones durante toda la hora.
- **Exclusividad**: Un curso por salón a la vez.
- **Preferencias**: La tabla expresa molestias por grupo.

La decisión pendiente es qué salón asignar a cada curso. Tanto las características
de los salones como las valoraciones de los grupos ya son datos conocidos.
:::

::: hint {#opt-obj-sal-fijos-p2 of="opt-obj-sal-fijos" title="PISTA 2 · Una pregunta para avanzar"}
¿Qué parte de tu modelo rechaza una asignación imposible y qué parte permite
comparar dos que sí cumplen? ¿Una molestia alta viola alguna regla del enunciado?
:::

Antes de leer la respuesta, vuelve a tu intento y revisa qué pudiste formular
con ayuda de las pistas.

::: answer {#opt-obj-sal-fijos-resp of="opt-obj-sal-fijos" title="Respuesta · Factibilidad y preferencia"}
**1. Separar los datos.** Sean $C$ los cursos y $R$ el conjunto de salones.
Todos los cursos de este primer modelo ocurren en la misma hora.

- $n_c$: Estudiantes del curso $c$.
- $k_r$: Lugares del salón $r$.
- $e_c\in\{0,1\}$: Si el curso requiere proyector.
- $p_r\in\{0,1\}$: Si el salón tiene proyector.
- $v_r\in\{0,1\}$: Si el salón está disponible toda la hora.
- $m_{cr}\ge0$: Molestia del grupo de $c$ en $r$, en puntos comparables.

**2. Definir decisiones y construir condiciones.** $x_{cr}=1$ significa
asignar el curso $c$ al salón $r$; $x_{cr}=0$ significa no hacerlo.
Son decisiones binarias, sin unidades físicas.

Podemos leer las condiciones a partir de lo que cuentan estas decisiones:

- Al sumar las decisiones de un curso sobre todos los salones, contamos cuántos
  salones le asignamos. Esa cuenta debe ser exactamente uno.
- Al sumar las decisiones de un salón sobre todos los cursos, contamos cuántos
  cursos lo usan durante la misma hora. Esa cuenta no puede superar uno.

El producto $k_rx_{cr}$ aporta la capacidad del salón $r$ solo si lo elegimos
para el curso $c$. Como elegimos exactamente un salón, la expresión

$$\sum_{r\in R}k_rx_{cr}$$

es la capacidad seleccionada, en lugares. Debe alcanzar para los $n_c$
estudiantes del curso. La suma con $p_r$ funciona de la misma manera: indica
si el salón elegido tiene el proyector que se requiere.

La disponibilidad funciona como un permiso. Si $v_r=0$, la condición
$x_{cr}\le v_r$ impide usar el salón; si $v_r=1$, permite elegirlo sin obligarnos
a hacerlo.

**3. Formular la factibilidad.** Minimizar la constante cero deja empatadas
las asignaciones admisibles. Sirve para expresar «encuentra alguna que cumpla»;
no mide comodidad.

$$
\begin{aligned}
\min\quad &0\\
\text{sujeto a}\quad
&\sum_{r\in R}x_{cr}=1 &&(c\in C),\\
&\sum_{c\in C}x_{cr}\le1 &&(r\in R),\\
&\sum_{r\in R}k_rx_{cr}\ge n_c &&(c\in C),\\
&\sum_{r\in R}p_rx_{cr}\ge e_c &&(c\in C),\\
&x_{cr}\le v_r &&(c\in C,r\in R),\\
&x_{cr}\in\{0,1\} &&(c\in C,r\in R).
\end{aligned}
$$

**4. Elegir una preferencia explícita.** Una respuesta defendible es minimizar
la suma de molestias. Esto supone que cada punto cuenta igual y que aceptamos
compensar más molestia de un grupo con menos de otro.

El producto $m_{cr}x_{cr}$ aporta los puntos de molestia de una asignación cuando
la elegimos; aporta cero cuando no la elegimos. Al sumar sobre cursos y salones
obtenemos la molestia total:

$$\sum_{c\in C}\sum_{r\in R}m_{cr}x_{cr}.$$

El modelo general de comodidad conserva **todas las restricciones y los dominios**
del modelo anterior. Solo reemplaza el objetivo constante $0$ por esta expresión,
que está medida en puntos.

Las capacidades determinan qué opciones caben, pero no imponen una única función
de comodidad. Tampoco hemos sumado estudiantes a puntos ni agregado un límite
obligatorio de molestia: el enunciado no pide ese límite.

**5. Sustituir los datos.** En los subíndices siguientes R y S nombran salones.
El modelo de comodidad total es:

$$
\begin{aligned}
\min\quad &0x_{AR}+4x_{AS}+4x_{BR}+6x_{BS}\\
\text{sujeto a}\quad
&x_{AR}+x_{AS}=1,\\
&x_{BR}+x_{BS}=1,\\
&x_{AR}+x_{BR}\le1,\\
&x_{AS}+x_{BS}\le1,\\
&30x_{AR}+30x_{AS}\ge20,\\
&30x_{BR}+30x_{BS}\ge20,\\
&x_{AR}+x_{AS}\ge1 &&\text{(proyector de A)},\\
&x_{BR}+x_{BS}\ge0 &&\text{(proyector de B)},\\
&x_{cr}\le1 &&c\in\{A,B\},r\in\{R,S\},\\
&x_{cr}\in\{0,1\} &&c\in\{A,B\},r\in\{R,S\}.
\end{aligned}
$$

La penúltima fila representa la disponibilidad. Aunque aquí varias condiciones
sean redundantes, quedan visibles para conservar el relato. Para el modelo
numérico de mera factibilidad, el objetivo es $0$ con estas mismas restricciones
y dominios.

**6. Poner a prueba el criterio.** Compara dos asignaciones admisibles:

Los valores de A y B son los puntos de molestia de cada grupo.

| Asignación | A | B |
|---|---:|---:|
| A en R, B en S | 0 | 6 |
| A en S, B en R | 4 | 4 |

Con la primera asignación, la suma es $0+6=6$ y la mayor molestia es $6$.
Con la segunda, la suma es $4+4=8$ y la mayor molestia es $4$.

La suma prefiere la primera, aunque el grupo B queda peor. **Atender al grupo
peor situado sería otra prioridad** y requeriría revisar el objetivo.
Ambas asignaciones cumplen capacidad, equipo y horario: las reglas obligatorias
no resuelven esa elección de preferencia.
:::

## Problema 2 · Elegir el horario de cada curso

::: exercise {#opt-obj-sal-horarios title="Dos maneras de comparar horarios"}
La coordinación ahora también puede decidir a qué hora empieza cada curso.
Conservamos A y B, sus grupos distintos de 20 estudiantes y sus docentes
distintos. A sigue necesitando proyector y B sigue sin necesitarlo.

La disponibilidad cambia: **S está cerrado** y solo queda R, con sus 30 lugares
y su proyector. R está disponible en tres bloques consecutivos de una hora,
numerados 1, 2 y 3.

Las condiciones de esta nueva situación son:

- A dura **dos bloques consecutivos** y puede empezar en 1 o en 2.
- B dura **un bloque** y puede empezar en 1 o en 3.
- Cada curso se imparte exactamente una vez, completo y sin cambiar de salón.
- Los cursos no pueden ocupar R al mismo tiempo.
- Los docentes están disponibles para todos los inicios permitidos.

No hay otras restricciones ni traslados entre cursos compartidos por estudiantes.

Las valoraciones anteriores por salón se **sustituyen** por estas molestias
según la hora de inicio, en la misma escala común por grupo:

| Curso | Inicio | Molestia |
|---|---:|---:|
| A | 1 | 0 |
| A | 2 | 4 |
| B | 1 | 4 |
| B | 3 | 6 |

La coordinación considera dos maneras de atender a los grupos:

1. Reducir **la molestia total de los dos grupos**. Cada punto cuenta igual:
   reducir un punto para un grupo puede compensar que el otro reciba un punto más.
2. Dar prioridad al **grupo con el puntaje de molestia más alto** y reducirlo
   tanto como sea posible. Se acepta una molestia total mayor si con ello mejora
   la situación del grupo más afectado.

Construye un criterio para cada petición y formula los dos modelos completos,
primero con parámetros y luego con estos datos. Explica qué preferencia cambia
de un modelo al otro.

En ambos debes representar la ocupación de todos los bloques de A. La tarea
termina con la formulación; no hace falta buscar el horario óptimo.
:::

### Primero intenta plantearlo

Escribe un primer intento para los dos criterios antes de abrir las ayudas.
Revisa también cómo representarías la duración de cada curso.

::: hint {#opt-obj-sal-horarios-p1 of="opt-obj-sal-horarios" title="PISTA 1 · Ordenar los datos"}
La duración se mide en bloques consecutivos. La fila «Proyector» indica si
el curso lo requiere; los inicios son los permitidos.

| Dato | A | B |
|---|---|---|
| Bloques | 2 | 1 |
| Inicio | 1 o 2 | 1 o 3 |
| Estudiantes | 20 | 20 |
| Proyector | Sí | No |

R es el único salón disponible: 30 lugares, proyector y tres bloques libres.
Las molestias están en la tabla del enunciado; ahora dependen del inicio.
:::

::: hint {#opt-obj-sal-horarios-p2 of="opt-obj-sal-horarios" title="PISTA 2 · Una pregunta para avanzar"}
Si A comienza en el bloque 1, ¿qué bloques deja ocupados? Para evaluar al grupo
peor atendido, ¿necesitas sumar sus molestias o comparar sus valores individuales?
:::

Antes de leer la respuesta, vuelve a tu intento y revisa qué pudiste formular
con ayuda de las pistas.

::: answer {#opt-obj-sal-horarios-resp of="opt-obj-sal-horarios" title="Respuesta · Ocupar intervalos y comparar grupos"}
**1. Datos y decisiones.** Llamemos $C$ al conjunto de cursos y $T$ al conjunto
de bloques del horario. Para cada curso necesitamos conocer estos datos:

- $S_c$: Inicios permitidos.
- $d_c\in\mathbb Z_{>0}$: Duración en bloques.
- $n_c$: Número de estudiantes.
- $e_c\in\{0,1\}$: Si requiere proyector.
- $m_{cs}\ge0$: Molestia del grupo por iniciar en $s$, en puntos.

El único salón tiene capacidad $k$ y proyector $p\in\{0,1\}$. Su disponibilidad
se indica con $v_t\in\{0,1\}$: vale uno cuando puede usarse durante el bloque $t$.

Elegir un inicio reserva todos los bloques necesarios para terminar el curso.
Si comienza en $s$ y dura $d_c$ bloques, ocupará el conjunto

$$O_{cs}=\{s,\ldots,s+d_c-1\}.$$

Ese intervalo completo debe quedar dentro de $T$. Conocemos la duración de cada
curso; la decisión consiste en elegir uno de sus inicios permitidos.

Usamos $y_{cs}\in\{0,1\}$, que vale uno si el curso $c$ empieza en $s$.
El producto $m_{cs}y_{cs}$ aporta la molestia de ese inicio solo cuando se elige.
Como cada curso empieza una sola vez, su molestia es

$$M_c(y)=\sum_{s\in S_c}m_{cs}y_{cs},$$

medida en puntos. La suma de estas expresiones compara la molestia total de los
grupos.

**2. Un modelo general para la suma.** Hay que revisar **cada bloque ocupado**:
dos cursos pueden comenzar a horas distintas y necesitar el salón al mismo tiempo.
Para un bloque $t$, sumamos las decisiones de inicio cuyos intervalos contienen
ese bloque.

Una suma de cero indica que el salón queda libre; una suma de uno, que un curso
lo ocupa. Una suma de dos indicaría un traslape. Por eso la cuenta no puede
superar $v_t$: como máximo un curso si está disponible y ninguno si está cerrado.

Además, cada curso debe elegir exactamente un inicio. Las condiciones de
capacidad y proyector se aplican al inicio elegido. Con esas condiciones,
el modelo completo es:

$$
\begin{aligned}
\min\quad &\sum_{c\in C}\sum_{s\in S_c}m_{cs}y_{cs}\\
\text{sujeto a}\quad
&\sum_{s\in S_c}y_{cs}=1 &&(c\in C),\\
&\sum_{c\in C}\sum_{s\in S_c:\ t\in O_{cs}}y_{cs}\le v_t &&(t\in T),\\
&n_cy_{cs}\le k &&(c\in C,s\in S_c),\\
&e_cy_{cs}\le p &&(c\in C,s\in S_c),\\
&y_{cs}\in\{0,1\} &&(c\in C,s\in S_c).
\end{aligned}
$$

**3. El modelo general para el grupo con mayor molestia.** Ahora queremos atender la mayor
molestia individual. Conservamos las mismas decisiones, restricciones y dominios;
el nuevo objetivo es

$$\min\quad\max_{c\in C}M_c(y).$$

Podemos expresar esa misma preferencia mediante una variable auxiliar
$z\in\mathbb R_{\ge0}$, medida en puntos. Exigimos que alcance la molestia de
cada grupo:

$$M_c(y)\le z\qquad(c\in C).$$

Estas desigualdades convierten a $z$ en una **cota común**: ningún grupo puede
tener más molestia que ella. Si minimizamos $z$, la cota baja hasta coincidir
con la mayor molestia del horario elegido. Así, el segundo modelo conserva
todas las condiciones del primero, añade estas desigualdades y el dominio de
$z$, y minimiza $z$.

**4. Sustituir los datos.** Las decisiones son $y_{A1},y_{A2},y_{B1},y_{B3}$.
A en 1 ocupa $\{1,2\}$; A en 2 ocupa $\{2,3\}$. El modelo completo de suma es:

$$
\begin{aligned}
\min\quad &0y_{A1}+4y_{A2}+4y_{B1}+6y_{B3}\\
\text{sujeto a}\quad
&y_{A1}+y_{A2}=1,\\
&y_{B1}+y_{B3}=1,\\
&y_{A1}+y_{B1}\le1 &&\text{(bloque 1)},\\
&y_{A1}+y_{A2}\le1 &&\text{(bloque 2)},\\
&y_{A2}+y_{B3}\le1 &&\text{(bloque 3)},\\
&20y_{cs}\le30 &&(c,s)\in K,\\
&e_cy_{cs}\le1 &&(c,s)\in K,\\
&y_{cs}\in\{0,1\} &&(c,s)\in K,
\end{aligned}
$$

donde $K=\{(A,1),(A,2),(B,1),(B,3)\}$, $e_A=1$ y $e_B=0$.
Capacidad y equipo siguen presentes aunque no eliminen opciones en este ejemplo.
El modelo completo para reducir la mayor molestia es:

$$
\begin{aligned}
\min\quad &z\\
\text{sujeto a}\quad
&y_{A1}+y_{A2}=1,\\
&y_{B1}+y_{B3}=1,\\
&y_{A1}+y_{B1}\le1,\\
&y_{A1}+y_{A2}\le1,\\
&y_{A2}+y_{B3}\le1,\\
&20y_{cs}\le30 &&(c,s)\in K,\\
&e_cy_{cs}\le1 &&(c,s)\in K,\\
&0y_{A1}+4y_{A2}\le z,\\
&4y_{B1}+6y_{B3}\le z,\\
&y_{cs}\in\{0,1\} &&(c,s)\in K,\\
&z\in\mathbb R_{\ge0}.
\end{aligned}
$$

**5. Comprobar qué expresa cada criterio.** Podemos comparar los criterios
con dos horarios que cumplen las reglas:

Los valores de A y B son los puntos de molestia de cada grupo.

| Horario | A | B |
|---|---:|---:|
| A empieza en 1; B en 3 | 0 | 6 |
| A empieza en 2; B en 1 | 4 | 4 |

La suma compara $0+6=6$ con $4+4=8$ y prefiere el primer horario. El máximo
compara $6$ con $4$ y prefiere el segundo. Los criterios expresan prioridades
distintas: reducir la molestia total o atender al grupo peor situado.

Minimizar el máximo tampoco decide todo. Si dos horarios tienen la misma mayor
molestia, este criterio los deja empatados aunque sus sumas sean diferentes.

Las molestias son por grupo, y aquí los grupos tienen igual tamaño. Si fueran
desiguales, dar el mismo peso a grupos o a personas sería otra decisión de modelado.
No hemos introducido un adversario: el máximo compara consecuencias del horario.
:::

Después de tus intentos, consulta [[opt-objetivo-salones-modelo|el modelo general de horarios y prioridades]].
