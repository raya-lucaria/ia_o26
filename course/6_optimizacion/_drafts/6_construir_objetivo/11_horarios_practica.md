---
id: opt-practica-horarios
title: Elegir el horario de cada curso
nav_title: "Horarios: práctica"
summary: "Formular horarios sin traslapes y comparar la molestia total con la del grupo peor atendido."
status: ready
estimated_time: 35m
tags: [optimizacion, modelado, practica]
---

# Elegir el horario de cada curso

Aquí practicarás una decisión nueva: elegir inicios cuando un curso ocupa
varios bloques. Formula los modelos antes de abrir las ayudas; no hace falta
buscar el horario óptimo. Los datos son didácticos.

Si necesitas recuperar la diferencia entre reglas y preferencias, vuelve a [[opt-objetivo-salones-practica|el ejemplo guiado de salones]].

## Problema 11 · Elegir el horario de cada curso

::: exercise {#opt-obj-sal-horarios title="Dos maneras de comparar horarios"}
La coordinación debe elegir a qué hora empiezan los cursos A y B. Cada uno
tiene un grupo de 20 estudiantes. Sus docentes son distintos y ningún
estudiante cursa ambos. A necesita proyector; B no lo necesita.

**El salón S está cerrado**. Solo se puede usar R, que tiene 30 lugares y
proyector. Está disponible en tres bloques consecutivos de una hora,
numerados 1, 2 y 3.

Las condiciones de esta nueva situación son:

- A dura **dos bloques consecutivos** y puede empezar en 1 o en 2.
- B dura **un bloque** y puede empezar en 1 o en 3.
- Cada curso se imparte exactamente una vez, completo y sin cambiar de salón.
- Los cursos no pueden ocupar R al mismo tiempo.
- Los docentes están disponibles para todos los inicios permitidos.

No hay otras restricciones ni traslados entre cursos compartidos por estudiantes.

Los grupos acordaron estos puntos de molestia según la hora de inicio.
La escala es común: menos puntos significan menos molestia. No son distancias
ni minutos de traslado; solo se valora el inicio del curso:

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

Después de tu intento, puedes consultar [[opt-objetivo-salones-modelo|el modelo general de horarios y prioridades]].

[[opt-construir-objetivo|Volver al banco de práctica]].
