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

Hay dos salones, R y S. Cada uno tiene 30 lugares, cuenta con proyector y
está disponible durante toda esa hora. La asignación debe respetar lo siguiente:

- Cada curso necesita exactamente un salón durante toda la hora.
- El salón debe tener lugar para todo su grupo.
- A necesita proyector; B no lo necesita.
- Los cursos no pueden compartir salón porque ocurren al mismo tiempo.

No hay otras condiciones. El horario está fijado: solo decidimos los salones.

**Piensa: ¿tener suficientes lugares nos dice cuál salón le conviene más a cada grupo?**

La capacidad permite comprobar si un grupo cabe. No nos dice qué tan cómodo
estará ni cuánto importa su comodidad frente a la del otro grupo. Primero
escribiremos las obligaciones; después elegiremos cómo comparar las opciones.

## 2 · Representar una asignación

**Piensa: ¿qué tendría que significar una variable para elegir un salón completo?**

Usaremos una decisión de sí o no por cada pareja curso–salón. Llamemos $C$
al conjunto de cursos y $\mathcal R$ al conjunto de salones; ambos son finitos
y no vacíos. Todos los cursos de este modelo se imparten durante la misma hora.
Definimos

$$
x_{cr}=\begin{cases}
1&\text{si asignamos el curso }c\text{ al salón }r,\\
0&\text{si no lo asignamos.}
\end{cases}
$$

Cada variable es **binaria**, con dominio $x_{cr}\in\{0,1\}$. No cuenta
estudiantes ni fracciones de salón. Los dos subíndices identifican una misma
asignación, no dos decisiones independientes.

Para escribir las reglas con parámetros, damos nombre a los datos conocidos:

- $n_c$: estudiantes del curso $c$.
- $k_r$: lugares del salón $r$.
- $e_c\in\{0,1\}$: vale uno si el curso requiere proyector.
- $p_r\in\{0,1\}$: vale uno si el salón tiene proyector.
- $v_r\in\{0,1\}$: vale uno si el salón está disponible toda la hora.

## 3 · Construir las obligaciones

**Piensa: al sumar las decisiones de un curso, ¿qué estás contando? ¿Y las de un salón?**

Para un curso fijo $c$, sumamos sobre sus posibles salones. La suma cuenta
cuántos le asignamos. Como debe recibir exactamente uno,

$$\sum_{r\in\mathcal R}x_{cr}=1\qquad(c\in C).$$

Para un salón fijo $r$, sumamos sobre los cursos. Esta cuenta no puede
superar uno: dos cursos ocuparían el salón al mismo tiempo.

$$\sum_{c\in C}x_{cr}\le1\qquad(r\in\mathcal R).$$

El producto $k_rx_{cr}$ aporta los lugares del salón cuando lo elegimos
y cero cuando no. Como cada curso recibe un único salón, sumar esos
productos da la capacidad elegida. Debe alcanzar para el grupo:

$$\sum_{r\in\mathcal R}k_rx_{cr}\ge n_c\qquad(c\in C).$$

Con el proyector hacemos lo mismo: la suma indica si el salón elegido
cuenta con él. La disponibilidad funciona como permiso; un cero impide
asignar el salón, mientras que un uno permite usarlo sin obligarnos a hacerlo.

$$
\begin{aligned}
&\sum_{r\in\mathcal R}p_rx_{cr}\ge e_c &&(c\in C),\\
&x_{cr}\le v_r &&(c\in C,r\in\mathcal R).
\end{aligned}
$$

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

| Curso | R | S |
|---|---:|---:|
| A | 0 | 4 |
| B | 4 | 6 |

**Piensa: ¿cómo contarías la molestia de las asignaciones elegidas y dejarías fuera las demás?**

Llamemos $m_{cr}\ge0$ a los puntos del grupo de $c$ si usa $r$. El producto
$m_{cr}x_{cr}$ aporta esos puntos cuando elegimos la asignación y cero cuando
la descartamos. La molestia del grupo queda determinada por

$$M_c(x)=\sum_{r\in\mathcal R}m_{cr}x_{cr}.$$

Una primera propuesta es sumar las molestias de todos los grupos. Supone
que cada punto cuenta igual y que aceptamos compensar más molestia de un
grupo con menos de otro. El modelo completo, usando el conjunto ya definido, es

$$\min_{x\in F}\quad\sum_{c\in C}M_c(x).$$

El objetivo está en puntos. Las restricciones siguen midiendo asignaciones,
lugares, equipo y disponibilidad: no sumamos estudiantes a puntos ni convertimos
una molestia alta en una prohibición que nadie pidió.

## 5 · Sustituir los datos sin perder condiciones

**Piensa: si todas las opciones tienen proyector, ¿desaparece ese requisito del relato?**

El requisito sigue existiendo, aunque con estos datos no descarte ninguna
opción. Lo mantenemos visible al escribir el modelo numérico completo.
En los subíndices, A y B nombran cursos; R y S nombran salones.

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

La penúltima fila representa la disponibilidad. Para el modelo numérico de
mera factibilidad, el objetivo sería cero con estas mismas restricciones
y dominios. Varias filas son redundantes aquí, pero explican qué reglas
necesitaríamos conservar si cambiaran los datos.

## 6 · Revisar qué preferencia expresa la suma

**Piensa: ¿reducir la molestia total siempre ayuda al grupo que recibe más molestia?**

Comparemos dos asignaciones factibles. Las columnas A y B muestran los
puntos de molestia de cada grupo.

| Asignación | A | B |
|---|---:|---:|
| A en R, B en S | 0 | 6 |
| A en S, B en R | 4 | 4 |

La primera suma $0+6=6$ puntos; la segunda, $4+4=8$. La suma prefiere la
primera, aunque B recibe más molestia. Si queremos atender al grupo con
**mayor molestia**, compararemos 6 con 4 y preferiremos la segunda.

Esa otra prioridad conserva las asignaciones permitidas y cambia el objetivo:

$$\min_{x\in F}\quad\max_{c\in C}M_c(x).$$

Con estos datos, el máximo compara $4x_{AS}$ con $4x_{BR}+6x_{BS}$.
No hay un rival que elija perjudicarnos: comparamos los efectos de nuestra
propia asignación sobre grupos distintos.

Minimizar el máximo no garantiza igualdad ni distingue asignaciones con el
mismo máximo y distinta suma. Además, los puntos son por grupo; si los grupos
tuvieran tamaños distintos, dar el mismo peso a grupos o a personas requeriría
otra decisión. Capacidad y equipo no resuelven ninguna de esas preferencias.

Continúa con [[opt-objetivo-panaderia-practica|cómo decidir cuánto pan producir cuando la demanda es incierta]].

Para practicar después: [[opt-practica-horarios|decidir también las horas de inicio]]. La [[opt-objetivo-salones-modelo|consulta opcional de salones y horarios]] reúne la formulación más general.
