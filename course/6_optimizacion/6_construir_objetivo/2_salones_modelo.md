---
id: opt-objetivo-salones-modelo
title: Cómo modelar salones, horarios y comodidad
nav_title: "Salones: modelo general"
summary: "Asignaciones, intervalos ocupados y objetivos que expresan prioridades distintas entre grupos."
status: ready
tags: [optimizacion, modelado, entera]
---

# Cómo modelar salones, horarios y comodidad

Antes de continuar, intenta [[opt-objetivo-salones-practica|los dos problemas de salones]].
Allí cambiamos la decisión de salón por la decisión de horario; aquí reunimos
ambas: **dónde y cuándo impartir cada curso**.

Construiremos primero las opciones que cumplen las reglas. Después veremos
cómo compararlas cuando nos importan consecuencias distintas para los grupos.

## 1 · Construir las opciones de cada curso

- $C,R,T$: Conjuntos finitos de cursos, salones y bloques horarios.
- $n_c,k_r$: Estudiantes del curso y lugares del salón.
- $d_c\in\mathbb Z_{>0}$: Duración del curso en bloques consecutivos.
- $e_c,p_r\in\{0,1\}$: Necesidad y existencia de proyector.
- $v_{rt}\in\{0,1\}$: Disponibilidad del salón durante el bloque.
- $S_c$: Inicios permitidos por calendario y disponibilidad del docente.
- $G$: Grupos de estudiantes cuya molestia queremos comparar.
- $C_g\subseteq C$: Cursos que cursa el grupo $g$.
- $H$: Parejas de cursos que comparten docente o estudiantes.

Cada curso se imparte una vez, en un solo salón y sin interrupciones. Además
de conocer sus necesidades, debemos saber qué cursos comparten personas:
los datos de matrícula y de docentes determinan esas parejas de conflicto.
Si un grupo cursa dos materias, la pareja correspondiente debe figurar en $H$.

Una opción $(c,r,s)$ significa impartir el curso $c$ en el salón $r$, comenzando
en el bloque $s$. La duración determina todos los bloques que esa opción ocupa:

$$O_{cs}=\{s,\ldots,s+d_c-1\}.$$

Antes de combinar opciones de cursos distintos, revisamos si cada opción puede
usarse por sí sola. Para admitirla deben cumplirse estas condiciones:

- El inicio está permitido para el curso y su intervalo completo queda dentro de $T$.
- La capacidad del salón alcanza para sus estudiantes.
- El salón cuenta con el proyector si el curso lo requiere.
- El salón está disponible en **todos los bloques ocupados**.

Llamamos $K$ al conjunto de opciones que pasan esas comprobaciones. En símbolos:

$$
\begin{aligned}
K=\{(c,r,s):\;&c\in C,\ r\in R,\ s\in S_c,\\
&O_{cs}\subseteq T,\\
&k_r\ge n_c,\ p_r\ge e_c,\\
&v_{rt}=1\text{ para todo }t\in O_{cs}\}.
\end{aligned}
$$

Capacidad, equipo y disponibilidad ya están incorporados en $K$. Al usar
únicamente sus opciones, seguimos respetando esas condiciones.

Si un curso no tiene ninguna opción en $K$, no será posible impartirlo con
estos datos. Cambiar la preferencia del objetivo no crea un salón ni un horario
que cumpla sus necesidades.

## 2 · Decidir una opción y evitar conflictos

Para cada $(c,r,s)\in K$, elegimos $x_{crs}\in\{0,1\}$: vale uno si el curso
usa ese salón con ese inicio. Los subíndices identifican tres datos de una misma
elección; no son tres decisiones independientes.

Una opción puede ser válida por sí sola y entrar en conflicto con otra cuando
armamos el horario. Para evitarlos, debemos comprobar tres cosas:

1. **Una opción por curso.** Contamos sus elecciones sobre todos los salones e
   inicios admitidos en $K$; la cuenta debe ser uno.
2. **Un curso por salón y bloque.** Contamos las opciones elegidas que usan ese
   salón durante ese bloque; la cuenta no puede superar uno.
3. **Sin cursos simultáneos para una misma persona.** Para cada pareja de $H$,
   contamos si sus cursos ocupan el mismo bloque, aunque sea en salones distintos.
   La cuenta tampoco puede superar uno.

El objetivo constante $0$ deja empatados los horarios que cumplen las reglas.
Con él, el modelo de factibilidad completo se escribe como:

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

Las tres primeras filas corresponden a las tres comprobaciones anteriores.
El dominio binario permite interpretar cada variable como elegir o descartar
una opción.

Llamaremos $F$ al conjunto de asignaciones que cumple **todas estas restricciones
y los dominios binarios**, usando el $K$ ya definido. Así, escribir $x\in F$
conserva también los requisitos de capacidad, equipo y disponibilidad que usamos
para construir $K$.

Los dos ejercicios se obtienen al fijar algunos de estos datos:

- En el primero, cada $S_c$ contiene solo el inicio fijo y todos los cursos
  duran un bloque.
- En el segundo, $R$ contiene un único salón, $S_A=\{1,2\}$, $S_B=\{1,3\}$
  y las duraciones son $d_A=2$ y $d_B=1$.

En ambos, $H$ está vacío porque los grupos y los docentes son distintos.
Aunque no haya conflictos entre personas, sigue siendo necesario evitar
que dos cursos ocupen el mismo salón al mismo tiempo.

## 3 · Medir antes de combinar

Para comparar horarios necesitamos datos sobre sus consecuencias. Supongamos
que conocemos los puntos de molestia $m_{gcrs}\ge0$ que la opción $(c,r,s)$
aporta al grupo $g$, cuando ese grupo cursa la materia: $c\in C_g$.
Las escalas deben ser comparables entre grupos.

El producto $m_{gcrs}x_{crs}$ aporta esos puntos cuando elegimos la opción y
aporta cero cuando la descartamos. **Si suponemos que las aportaciones se suman**,
podemos reunir las molestias de los cursos que lleva el grupo:

$$M_g(x)=\sum_{(c,r,s)\in K:\ c\in C_g}m_{gcrs}x_{crs}.$$

La expresión $M_g(x)$ queda medida en puntos y su valor depende del horario
elegido. No podemos reducirla por separado de las decisiones que producen
esa molestia.

El supuesto de sumar aportaciones no sirve para todos los criterios. Por ejemplo,
caminar entre dos clases depende de **las dos asignaciones**, de su orden, de
quién cursa ambas y de las distancias. Contar edificios usados no basta para
medir ese traslado: harían falta esos datos y una representación de las transiciones.

## 4 · Dos modelos completos, dos preferencias

Una primera prioridad es reducir la molestia de los grupos en conjunto. Si cada
punto cuenta igual, podemos sumar sus molestias; así aceptamos que una mejora
para un grupo compense un empeoramiento igual para otro. El modelo es:

$$\min_{x\in F}\quad\sum_{g\in G}M_g(x).$$

Aquí $F$ incluye las variables binarias y todas las restricciones del apartado 2;
$M_g$ es la expresión del apartado 3. Esta escritura abreviada conserva el modelo
completo. Mide puntos totales de molestia según la escala acordada.

Una segunda prioridad es atender al grupo que quede peor situado. Para medirlo,
nos interesa la mayor molestia individual.

Introducimos una variable auxiliar $z$, en puntos, y exigimos que alcance la
molestia de cada grupo. El modelo busca la cota común más pequeña:

$$
\begin{aligned}
\min_{x,z}\quad &z\\
\text{sujeto a}\quad
&x\in F,\\
&M_g(x)\le z &&(g\in G),\\
&z\in\mathbb R_{\ge0}.
\end{aligned}
$$

Cada desigualdad obliga a que $z$ sea al menos tan grande como la molestia de
un grupo. Como deben cumplirse todas, $z$ debe alcanzar la mayor molestia.
Al minimizarla, hacemos que coincida con ella.

**Minimizar la mayor molestia no garantiza igualdad.** Este objetivo tampoco
mide la diferencia entre grupos.

En la práctica, las opciones con molestias $(0,6)$ y $(4,4)$ exhiben el
conflicto: la suma puede concentrar la molestia; el máximo puede aceptar una
suma mayor. Ninguno es universalmente justo sin explicar qué se protege.

## 5 · Pesos, prioridades y límites

También podemos dar distinta importancia a los grupos mediante pesos positivos
$w_g$, fijados **antes de resolver**. Cada peso multiplica la contribución de su
grupo al objetivo; un peso mayor le da mayor prioridad. El modelo resultante es

$$\min_{x\in F}\quad\sum_g w_gM_g(x).$$

La interpretación de la medida sigue siendo necesaria. Multiplicar por el tamaño
del grupo solo tiene sentido si $M_g$ representa una molestia por persona
comparable, no un total ya agregado. Además, cambiar la escala de un indicador
sin ajustar sus pesos cambia el criterio.

Un peso grande elegido a ojo no expresa necesariamente una prioridad estricta.
Si queremos que reducir la mayor molestia tenga precedencia sobre reducir la
suma, podemos formular dos decisiones sucesivas:

1. Minimizar la mayor molestia y llamar $z^\star$ al valor obtenido.
2. Minimizar la suma entre los horarios que conservan esa primera prioridad.
   Para ello exigimos $M_g(x)\le z^\star$ para todos los grupos.

El segundo modelo queda así:

$$
\begin{aligned}
\min_{x}\quad &\sum_{g\in G}M_g(x)\\
\text{sujeto a}\quad &x\in F,\\
&M_g(x)\le z^\star &&(g\in G).
\end{aligned}
$$

Esto desempata sin sacrificar la prioridad inicial. Se conoce como prioridad
lexicográfica; no necesitamos desarrollar un algoritmo para formularla.

Por último, una condición puede expresar una obligación en lugar de una
preferencia. Si se fija un límite $L_g$ de molestia que el grupo no debe superar,
lo escribimos como

$$M_g(x)\le L_g.$$

Agregar una penalización al objetivo no impone ese límite: el criterio todavía
podría aceptar una violación a cambio de otra mejora. En cambio, un límite
obligatorio elimina las opciones que lo incumplen. Si es demasiado exigente,
puede dejar sin opciones al conjunto factible.

## Qué razonamiento puedes reutilizar

**Primero define qué horarios se permiten. Después justifica cómo compararlos.**
Cambiar el objetivo conserva las opciones; cambiar una restricción puede
eliminarlas. Para combinar varios propósitos hacen falta unidades, escalas
y prioridades explícitas. Para medir consecuencias nuevas pueden hacer falta
datos nuevos, no solamente una fórmula más larga.

[[opt-objetivo-salones-practica|Volver a los ejercicios]] · [[opt-construir-objetivo|Volver a la guía]].
