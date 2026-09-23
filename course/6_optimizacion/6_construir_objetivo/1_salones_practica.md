---
id: opt-objetivo-salones-practica
title: Salones y horarios que funcionan para quién
nav_title: "Salones: práctica"
summary: "Dos modelos para distinguir horarios admisibles, molestia total y atención al grupo peor situado."
status: ready
tags: [optimizacion, modelado, practica]
---

# Salones y horarios que funcionan para quién

**Tu tarea: formular, no encontrar el horario óptimo.** Los datos son didácticos.
En estos dos problemas, cumplir las reglas no basta para decir qué opción es
mejor. También tendrás que explicar qué preferencia representa tu objetivo.

## Problema 1 · Asignar salones con horarios fijos

::: exercise {#opt-obj-sal-fijos title="¿Qué significa una buena asignación?"}
Los cursos A y B se imparten simultáneamente de 9 a 10. Cada uno tiene un grupo
de 20 estudiantes; nadie cursa ambos y tienen docentes distintos. Cada curso
necesita exactamente un salón durante toda esa hora.

Los salones R y S tienen 30 lugares cada uno, ambos cuentan con proyector y
ambos están disponibles de 9 a 10. A necesita proyector; B no lo necesita.
No se puede compartir salón entre cursos simultáneos. No hay otras condiciones.

La coordinación quiere que los grupos estén cómodos. Recogió estas valoraciones
acordadas en una escala común de **puntos de molestia por grupo**: menos es mejor.
Representan una preferencia, no distancias ni minutos de traslado.

| Curso y su grupo | En R | En S |
|---|---:|---:|
| A | 0 | 4 |
| B | 4 | 6 |

**Primero formula qué asignaciones cumplen las condiciones, sin preferir ninguna.**
Después propone un objetivo para comparar las asignaciones y justifica qué
entiendes por comodidad. Escribe los modelos completos, primero con parámetros
y luego con estos datos. ¿Bastan capacidad y equipo para determinar qué es mejor?
:::

### Primero intenta plantearlo

**NO ABRAS LAS PISTAS ANTES DE ESCRIBIR TU INTENTO.**

::: hint {#opt-obj-sal-fijos-p1 of="opt-obj-sal-fijos" title="PISTA 1 · Ordenar los datos"}
| Parte | Información conocida |
|---|---|
| Cursos | A y B; 20 estudiantes cada uno; misma hora |
| Recursos | R y S; 30 lugares y proyector en ambos |
| Equipo requerido | A necesita proyector; B no |
| Disponibilidad | Ambos salones durante toda la hora |
| Exclusividad | Un curso por salón a la vez |
| Preferencias | La tabla expresa molestias por grupo |

Se elige el salón de cada curso, no la capacidad ni la valoración del grupo.
:::

::: hint {#opt-obj-sal-fijos-p2 of="opt-obj-sal-fijos" title="PISTA 2 · Una pregunta para avanzar"}
¿Qué parte de tu modelo rechaza una asignación imposible y qué parte permite
comparar dos que sí cumplen? ¿Una molestia alta viola alguna regla del enunciado?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-sal-fijos-resp of="opt-obj-sal-fijos" title="Respuesta · Factibilidad y preferencia"}
**1. Separar los datos.** Sean $C$ los cursos y $R$ el conjunto de salones.
Todos los cursos de este primer modelo ocurren en la misma hora.

| Parámetro | Significado y unidad |
|---|---|
| $n_c$ | Estudiantes del curso $c$ |
| $k_r$ | Lugares del salón $r$ |
| $e_c\in\{0,1\}$ | Si el curso requiere proyector |
| $p_r\in\{0,1\}$ | Si el salón tiene proyector |
| $v_r\in\{0,1\}$ | Si el salón está disponible toda la hora |
| $m_{cr}\ge0$ | Molestia del grupo de $c$ en $r$, en puntos comparables |

**2. Definir decisiones y construir condiciones.** $x_{cr}=1$ significa
asignar el curso $c$ al salón $r$; $x_{cr}=0$ significa no hacerlo.
Son decisiones binarias, sin unidades físicas.

Cada curso necesita una elección. Cada salón admite como máximo una.
Como elegimos un solo salón por curso, la suma de capacidades seleccionadas
es la capacidad de ese salón; lo mismo ocurre con su equipo. La disponibilidad
es un permiso, no una obligación de usar el salón.

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
la suma de molestias: cada punto cuenta igual y aceptamos compensar más molestia
de un grupo con menos de otro. Bajo ese supuesto, el modelo general conserva
**todas** las condiciones anteriores y reemplaza $0$ por
$\sum_{c\in C}\sum_{r\in R}m_{cr}x_{cr}$.

No sumamos estudiantes a puntos ni agregamos un límite de molestia que nadie
pidió. Tampoco hay una única función correcta dictada por las capacidades.

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

| Asignación | Molestia de A | Molestia de B | Suma | Mayor molestia |
|---|---:|---:|---:|---:|
| A en R, B en S | 0 | 6 | 6 | 6 |
| A en S, B en R | 4 | 4 | 8 | 4 |

La suma prefiere la primera, pero el grupo B queda peor. Si la prioridad fuera
atender al grupo peor situado, habría que revisar el objetivo. La suma no
representa esa prioridad. Ambas asignaciones cumplen capacidad, equipo y horario.
:::

## Problema 2 · Decidir también a qué hora

::: exercise {#opt-obj-sal-horarios title="La suma y el grupo peor atendido"}
Ahora cambian los horarios y la disponibilidad. **S está cerrado**. Solo queda
R, con 30 lugares y proyector, disponible en tres bloques consecutivos de una
hora: 1, 2 y 3. Conservamos A y B, sus grupos distintos de 20 estudiantes,
sus docentes distintos y el requisito de proyector de A.

A debe impartirse durante **dos bloques consecutivos**, empezando en 1 o en 2.
B dura **un bloque**, y solo puede comenzar en 1 o en 3. Cada curso se imparte
exactamente una vez, completo, sin cambiar de salón. No pueden ocupar R a la vez.
Los docentes están disponibles para todos los inicios permitidos. No hay otras
restricciones ni traslados entre cursos compartidos por estudiantes.

Las valoraciones anteriores por salón se **sustituyen** por estas molestias
según la hora de inicio, en la misma escala común por grupo:

| Curso | Inicio permitido | Molestia del grupo |
|---|---:|---:|
| A | 1 | 0 |
| A | 2 | 4 |
| B | 1 | 4 |
| B | 3 | 6 |

Formula dos modelos completos: uno que prefiera la menor suma de molestias y
otro que prefiera que **la mayor molestia entre los grupos sea lo menor posible**.
Explica qué preferencia cambia. Incluye la ocupación de todos los bloques de A;
no busques el horario óptimo.
:::

### Primero intenta plantearlo

**ESCRIBE LOS DOS CRITERIOS ANTES DE ABRIR LAS AYUDAS.**

::: hint {#opt-obj-sal-horarios-p1 of="opt-obj-sal-horarios" title="PISTA 1 · Ordenar los datos"}
| Parte | A | B |
|---|---|---|
| Duración | 2 bloques seguidos | 1 bloque |
| Inicios permitidos | 1 o 2 | 1 o 3 |
| Estudiantes | 20 | 20 |
| Proyector requerido | Sí | No |

R es el único salón disponible: 30 lugares, proyector y tres bloques libres.
Las molestias están en la tabla del enunciado; ahora dependen del inicio.
:::

::: hint {#opt-obj-sal-horarios-p2 of="opt-obj-sal-horarios" title="PISTA 2 · Una pregunta para avanzar"}
Si A comienza en el bloque 1, ¿qué bloques deja ocupados? Para evaluar al grupo
peor atendido, ¿necesitas sumar sus molestias o comparar sus valores individuales?
:::

**COMPARA CON TU INTENTO ANTES DE LEER LA RESPUESTA.**

::: answer {#opt-obj-sal-horarios-resp of="opt-obj-sal-horarios" title="Respuesta · Ocupar intervalos y comparar grupos"}
**1. Datos y decisiones.** Para cursos $C$ y bloques $T$, sean $S_c$ los inicios
permitidos, $d_c$ la duración entera en bloques y $m_{cs}$ la molestia por iniciar
en $s$. El conjunto $O_{cs}=\{s,\ldots,s+d_c-1\}$ indica todos los bloques
ocupados, y debe quedar dentro de $T$. El único salón tiene capacidad $k$,
proyector $p\in\{0,1\}$ y disponibilidad $v_t\in\{0,1\}$ por bloque.
Conservamos estudiantes $n_c$ y requisito $e_c$ de proyector.

Elegimos $y_{cs}\in\{0,1\}$: iniciar o no el curso $c$ en $s$.
No elegimos su duración. La molestia del grupo es la expresión
$M_c(y)=\sum_{s\in S_c}m_{cs}y_{cs}$, en puntos.

**2. Un modelo general para la suma.** La ocupación se cuenta por bloque,
no solo por inicio. Dos cursos con inicios distintos todavía pueden traslaparse.

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

**3. El modelo general para el peor grupo.** Conserva las mismas decisiones,
restricciones y dominios y minimiza $\max_{c\in C}M_c(y)$. Para escribirlo
sin un máximo en el objetivo introducimos $z\in\mathbb R_{\ge0}$, una cota de
molestia en puntos, y añadimos $M_c(y)\le z$ para cada grupo. Minimizamos $z$.
Al minimizar, esa cota baja hasta la mayor molestia del horario elegido.

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
El modelo completo para proteger al peor grupo es:

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

**5. Comprobar qué expresa cada criterio.** A en 1 y B en 3 da molestias
$(0,6)$; A en 2 y B en 1 da $(4,4)$. Ambos horarios cumplen las reglas.
La suma prefiere $6$ a $8$; el máximo prefiere $4$ a $6$. No se contradicen:
expresan prioridades distintas. Minimizar el máximo protege al peor situado,
pero por sí solo no distingue horarios con el mismo máximo y diferente suma.

Las molestias son por grupo, y aquí los grupos tienen igual tamaño. Si fueran
desiguales, dar el mismo peso a grupos o a personas sería otra decisión de modelado.
No hemos introducido un adversario: el máximo compara consecuencias del horario.
:::

Después de tus intentos, consulta [[opt-objetivo-salones-modelo|el modelo general de horarios y prioridades]].
