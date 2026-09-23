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

Continúa con [[opt-objetivo-panaderia-practica|cómo decidir cuánto pan producir cuando la demanda es incierta]].

Para practicar después: [[opt-practica-horarios|decidir también las horas de inicio]]. La [[opt-objetivo-salones-modelo|consulta opcional de salones y horarios]] reúne la formulación más general.
