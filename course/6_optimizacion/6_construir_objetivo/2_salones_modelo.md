---
id: opt-objetivo-salones-modelo
title: Un modelo de horarios y prioridades
nav_title: "Salones: modelo general"
summary: "Asignaciones, intervalos ocupados y objetivos que expresan prioridades distintas entre grupos."
status: ready
tags: [optimizacion, modelado, entera]
---

# Un modelo de horarios y prioridades

**Primero intenta [[opt-objetivo-salones-practica|los dos problemas de salones]].**
Aquí reunimos las dos decisiones: dónde y cuándo impartir cada curso. Después
comparamos criterios sin alterar silenciosamente las reglas obligatorias.

## 1 · Construir las opciones de cada curso

| Dato | Significado |
|---|---|
| $C,R,T$ | Conjuntos finitos de cursos, salones y bloques horarios |
| $n_c,k_r$ | Estudiantes del curso y lugares del salón |
| $d_c\in\mathbb Z_{>0}$ | Duración del curso en bloques consecutivos |
| $e_c,p_r\in\{0,1\}$ | Necesidad y existencia de proyector |
| $v_{rt}\in\{0,1\}$ | Disponibilidad del salón durante el bloque |
| $S_c$ | Inicios permitidos por calendario y disponibilidad del docente |
| $G$ | Grupos de estudiantes cuya molestia queremos comparar |
| $C_g\subseteq C$ | Cursos que cursa el grupo $g$ |
| $H$ | Parejas de cursos que comparten docente o estudiantes |

Los datos de matrícula determinan los conflictos; no se deducen de los nombres
de los cursos. Si un grupo cursa dos materias, su pareja debe figurar en $H$.
Cada curso se imparte una vez, en un salón y sin interrupciones.

Para cada inicio $s$, definimos los bloques ocupados
$O_{cs}=\{s,\ldots,s+d_c-1\}$. Solo admitimos inicios cuyo intervalo completo
esté dentro de $T$. Una opción $(c,r,s)$ es admisible individualmente cuando
el salón tiene capacidad y equipo y está disponible en **todos** esos bloques.
Reunimos esas opciones en el conjunto conocido:

$$
K=\{(c,r,s):c\in C,r\in R,s\in S_c,\ O_{cs}\subseteq T,
\ k_r\ge n_c,\ p_r\ge e_c,
\ v_{rt}=1\text{ para todo }t\in O_{cs}\}.
$$

Así incorporamos capacidad, equipo y disponibilidad al construir las opciones;
no desaparecen del modelo. Si un curso no tiene opciones en $K$, el problema
es imposible bajo estos datos. No lo arregla cambiar el objetivo.

## 2 · Decidir una opción y evitar conflictos

Para cada $(c,r,s)\in K$, elegimos $x_{crs}\in\{0,1\}$: vale uno si el curso
usa ese salón con ese inicio. Los subíndices identifican tres datos de una misma
elección; no son tres decisiones independientes.

La factibilidad completa se escribe como:

$$
\begin{aligned}
\min\quad &0\\
\text{sujeto a}\quad
&\sum_{(r,s):(c,r,s)\in K}x_{crs}=1 &&(c\in C),\\
&\sum_{(c,s):(c,r,s)\in K,\ t\in O_{cs}}x_{crs}\le1
&&(r\in R,t\in T),\\
&\sum_{(r,s):(c,r,s)\in K,\ t\in O_{cs}}x_{crs}
+\sum_{(r,s):(c',r,s)\in K,\ t\in O_{c's}}x_{c'rs}\le1
&&((c,c')\in H,t\in T),\\
&x_{crs}\in\{0,1\} &&((c,r,s)\in K).
\end{aligned}
$$

La primera fila elige una opción por curso. La segunda evita compartir salón.
La tercera evita que una persona deba atender dos cursos simultáneos, incluso
en salones distintos. Son condiciones diferentes. Llamaremos $F$ al conjunto
de asignaciones que cumple **todas** estas filas, usando el $K$ ya definido.

En el primer ejercicio, cada $S_c$ contiene solo el inicio fijo y todos los
cursos duran un bloque. En el segundo, $R$ contiene solo un salón; $S_A=\{1,2\}$,
$S_B=\{1,3\}$ y $d_A=2,d_B=1$. En ambos, $H$ está vacío porque sus grupos y
docentes son distintos. La exclusividad del salón sigue siendo necesaria.

## 3 · Medir antes de combinar

Supongamos conocidos $m_{gcrs}\ge0$, puntos de molestia que la opción del
curso $c\in C_g$ aporta al grupo $g$. Las escalas deben ser comparables entre
grupos. Con el supuesto adicional de que estas aportaciones se suman,
la molestia del grupo es:

$$M_g(x)=\sum_{(c,r,s)\in K:\ c\in C_g}m_{gcrs}x_{crs}.$$

Es una expresión derivada, no una decisión que podamos reducir por separado.
El supuesto aditivo no sirve para todos los criterios. Por ejemplo, caminar
entre dos clases depende de **las dos** asignaciones, de su orden, de quién
cursa ambas y de las distancias. No puede obtenerse simplemente contando
edificios usados. Habría que dar esos datos y construir las transiciones.

## 4 · Dos modelos completos, dos preferencias

Si cada punto cuenta igual y aceptamos compensaciones entre grupos:

$$\min_{x\in F}\quad\sum_{g\in G}M_g(x).$$

Aquí $F$ incluye las variables binarias y todas las restricciones del apartado 2;
$M_g$ es la expresión del apartado 3. Esta escritura abreviada conserva el modelo
completo. Mide puntos totales de molestia según la escala acordada.

Si priorizamos al grupo con la mayor molestia:

$$
\begin{aligned}
\min_{x,z}\quad &z\\
\text{sujeto a}\quad
&x\in F,\\
&M_g(x)\le z &&(g\in G),\\
&z\in\mathbb R_{\ge0}.
\end{aligned}
$$

La variable auxiliar $z$ tiene unidades de puntos. Sus desigualdades obligan
que esté por encima de todas las molestias; minimizarla equivale a minimizar
la mayor. No mide la diferencia entre grupos ni garantiza igualdad.

En la práctica, las opciones con molestias $(0,6)$ y $(4,4)$ exhiben el
conflicto: la suma puede concentrar la molestia; el máximo puede aceptar una
suma mayor. Ninguno es universalmente justo sin explicar qué se protege.

## 5 · Pesos, prioridades y límites

Los pesos positivos $w_g$, fijados **antes** de resolver, dan el modelo
$\min_{x\in F}\sum_g w_gM_g(x)$. Dar mayor peso a un grupo representa mayor
prioridad. Multiplicar por el tamaño del grupo solo tiene sentido si $M_g$
representa una molestia por persona comparable, no un total ya agregado.
Cambiar la escala de un indicador sin ajustar sus pesos cambia el criterio.

Una prioridad estricta es diferente de un peso grande elegido a ojo. Podemos
primero minimizar la mayor molestia y llamar $z^\star$ al valor obtenido;
después minimizar la suma **conservando** $M_g(x)\le z^\star$ para todos los
grupos. Este segundo modelo es:

$$
\begin{aligned}
\min_{x}\quad &\sum_{g\in G}M_g(x)\\
\text{sujeto a}\quad &x\in F,\\
&M_g(x)\le z^\star &&(g\in G).
\end{aligned}
$$

Esto desempata sin sacrificar la prioridad inicial. Se conoce como prioridad
lexicográfica; no necesitamos desarrollar un algoritmo para formularla.

Por último, exigir $M_g(x)\le L_g$ expresa un límite obligatorio, con $L_g$
dado. Agregar una penalización al objetivo no impone ese límite: puede seguir
aceptando una violación a cambio de otra mejora. Un límite demasiado exigente
puede dejar $F$ sin opciones. Hay que distinguir preferencia de obligación.

## Qué razonamiento puedes reutilizar

**Primero define qué horarios se permiten. Después justifica cómo compararlos.**
Cambiar el objetivo conserva las opciones; cambiar una restricción puede
eliminarlas. Para combinar varios propósitos hacen falta unidades, escalas
y prioridades explícitas. Para medir consecuencias nuevas pueden hacer falta
datos nuevos, no solamente una fórmula más larga.

[[opt-objetivo-salones-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
