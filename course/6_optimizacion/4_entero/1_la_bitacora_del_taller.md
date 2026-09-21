---
id: la-bitacora-del-taller
title: La bitácora del taller
nav_title: La bitácora
summary: "Separar datos y decisiones, construir reglas por casos y escribir cuatro modelos enteros completos antes de resolverlos."
status: ready
estimated_time: 20m
tags: [optimizacion, modelado, entera]
---

# La bitácora del taller

**Tu tarea:** escribir cuatro modelos completos a partir de una bitácora.
Sigue esta secuencia en cada uno: **datos → variables → reglas en palabras →
ecuaciones → modelo completo**. Los modelos construidos paso a paso aparecen en
la página siguiente; primero intenta construir los tuyos.

Un dato ya está fijado por el relato: una disponibilidad, un consumo por
aparato o un máximo autorizado. Una variable representa algo que debemos
decidir. Por ejemplo, «quedan 24 kg» informa un dato; «cuántos rovers fabricar»
requiere una variable. Ponerle una letra a un dato lo convierte en un
**parámetro**, no en una nueva decisión.

Trabajaremos con pocas variables para poder leer cada renglón. La práctica que
buscamos sirve también con miles: identificar las condiciones, construir una
expresión para cada una y comprobar que el modelo completo las contiene. Aquí
no hace falta buscar el mejor plan, eliminar restricciones ni deducir cotas
más ajustadas.

## Problema 1 · Taller original

> **Bitácora — día 214.**
>
> El taller debe fabricar el equipo que baja al planeta: **rovers** y **sondas
> de superficie**. Se entregan aparatos completos, listos para funcionar; no se
> aceptan fracciones de equipo.
>
> Quedan **24 kg de aleación** y **6 horas de calibración** antes de la ventana
> de descenso. El taller consume la misma electricidad, fabrique lo que fabrique.
>
> Un rover requiere **6 kg y 1 hora**, y transmite **5 MB al día**. Una sonda
> requiere **4 kg y 2 horas**, y transmite **4 MB al día**. Queremos maximizar la
> transmisión total diaria.
>
> El comandante cierra la reunión: «Y no me hagan **más de cuatro rovers**».

### Separar los datos de las decisiones

Encierra los datos y subraya las decisiones. La disponibilidad de aleación no
se elige; la cantidad fabricada de cada equipo sí. La transmisión por equipo
es un dato; la transmisión total depende de las cantidades elegidas.

| Paso | Lo que debes escribir |
|---|---|
| Datos | Disponibilidades, consumo y transmisión por equipo, máximo de rovers |
| Variables | Cantidades que elegimos, con su significado y sus unidades |
| Reglas | Qué queremos maximizar y qué condiciones debe cumplir cualquier plan |
| Ecuaciones | Una expresión construida a partir de cada regla |
| Modelo completo | Objetivo, todas las restricciones y dominio de cada variable |

La electricidad es constante y el relato no fija un presupuesto eléctrico;
ese dato no agrega una restricción. En cambio, **la orden de fabricar como
máximo cuatro rovers debe aparecer explícitamente en el modelo**. Conserva
cada condición del enunciado al formular.

### Construir una expresión antes de poner números

Puedes llamar $x_1$ a la cantidad de rovers y $x_2$ a la de sondas. Para
construir el consumo de un recurso, empieza en palabras:

> Consumo total = consumo por rover × cantidad de rovers + consumo por sonda
> × cantidad de sondas.

Por ejemplo, llama $a_1$ y $a_2$ a los kg de aleación por rover y por sonda, y
$A$ a los kg disponibles. Construye la desigualdad con esos parámetros;
después sustituye $a_1=6$, $a_2=4$ y $A=24$. Sigue la misma secuencia para las
horas, la transmisión y el máximo autorizado. Las letras de los parámetros
permiten reconocer la regla aunque cambien los datos del taller.

### Decidir el dominio

Una cantidad de aparatos no puede ser negativa. Además, el enunciado exige
aparatos completos: fabricar $3/2$ sondas no es una opción permitida.

Son dos condiciones distintas: **no negatividad** e **integralidad**. Ambas
forman parte del modelo. El límite de cuatro rovers también debe quedar
escrito; no sustituye ninguna de ellas.

### Escribe el modelo del problema 1

::: exercise {#opt-ent-ej-modelo-base title="Problema 1 · Taller original"}
1. Separa los datos de las decisiones y define las variables con sus unidades.
2. Escribe en palabras qué mide el objetivo y cada condición del taller.
3. Construye las expresiones usando parámetros para los datos y después
   sustituye sus valores. Revisa las unidades de cada término.
4. Reúne en un solo modelo la función objetivo, las dos restricciones de
   recursos, la orden del comandante y los dominios. No dejes condiciones
   solamente en la explicación que precede al modelo.
:::

Antes de continuar, revisa tu hoja:

- Cada variable tiene un significado y un dominio.
- Cada término de una restricción tiene la misma unidad que su lado derecho.
- El objetivo mide MB/día y se maximiza.
- Cada condición del relato tiene un renglón en el modelo completo.
- Puedes explicar de qué frase salió cada expresión.

**Punto de control:** deberías tener un modelo completo, aunque todavía no
sepas resolverlo. Conserva tu intento para compararlo después.

## Tres cambios al taller original

Los siguientes problemas son **independientes**: cada uno parte del
**problema 1 · Taller original** y cambia solo la condición que se indica.
No combines los cambios de un problema con los del siguiente.

| Problema | Qué cambia | Qué conserva del problema 1 |
|---|---|---|
| **2 · Preparar la línea de ensamble de rovers** | Agrega 3 horas de preparación si se fabrican rovers | Recursos disponibles, consumo por equipo, transmisión y máximo de cuatro rovers |
| **3 · Fabricar cero rovers o un lote de al menos tres** | Prohíbe fabricar solamente uno o dos rovers | Todos los datos originales; no agrega horas de preparación |
| **4 · Compartir la antena entre los rovers** | Reduce la transmisión del tercero y del cuarto rover | Todos los recursos originales; no exige preparación adicional ni lote mínimo |

En cada ejercicio escribe el **modelo completo**, incluidas las condiciones
que se conservan. Para las reglas condicionales, describe primero los casos,
construye después una expresión que funcione en todos ellos y sustituye al
final los parámetros por sus valores. Las pistas están plegadas para que
puedas intentarlo.

## Problema 2 · Preparar la línea de ensamble de rovers

Para representar decisiones con dos opciones usaremos variables **binarias**:
solo pueden tomar 0 o 1. Al definir cada una, escribe qué significa elegir
cero y qué significa elegir uno.

::: exercise {#opt-ent-ej-intento-encender title="Problema 2 · Preparar la línea de ensamble de rovers"}
Parte del **problema 1 · Taller original** y agrega esta condición:

> Antes de fabricar rovers hay que ajustar y calibrar las máquinas de su
> **línea de ensamble**, es decir, el conjunto de máquinas con las que se arman
> los rovers. Prepararlas requiere **3 horas una sola vez**, sin importar
> cuántos rovers se fabriquen. Esas horas salen de las **mismas 6 horas de
> calibración** disponibles en la bitácora.
>
> **Además**, cada rover necesita su hora de calibración individual. Cada
> sonda sigue necesitando 2 horas y puede fabricarse sin preparar las máquinas
> de los rovers. Si no fabricamos rovers, no necesitamos esa preparación.

Para los rovers hay dos consumos de tiempo: preparar las máquinas y calibrar
cada aparato. Las horas de las sondas se cuentan aparte:

| Trabajo | Cuándo consume horas |
|---|---|
| Preparar las máquinas para ensamblar rovers | 3 horas en total si se preparan |
| Calibrar los rovers terminados | 1 hora por cada rover |
| Calibrar las sondas terminadas | 2 horas por cada sonda |

1. Distingue los datos de las decisiones. Conserva $x_1$ y $x_2$ e introduce
   una variable binaria para decidir si se prepara la línea. Explica sus dos
   valores. Llama $U$ al máximo autorizado por el comandante: $U=4$.
2. Escribe dos casos: sin preparación, ¿cuántos rovers se permiten? Con
   preparación, ¿cuál es el máximo autorizado? Construye una expresión para
   ese límite que tome el valor correcto en cada caso.
3. Llama $s$ a las horas de preparación. Construye el término que consume
   cero horas al no preparar y $s$ horas al preparar; después usa $s=3$.
   Súmalo al tiempo de calibración individual de los equipos. Comprueba las
   unidades: todos son términos de **horas**, no de dinero.
4. Escribe el modelo completo con la aleación, las horas, el enlace entre
   preparación y cantidad, la orden del comandante, la transmisión y todos
   los dominios. Usa $U=4$ como dato; no busques un máximo distinto a partir
   de los recursos.
:::

::: hint {#opt-ent-pista-intento-encender of="opt-ent-ej-intento-encender" title="Separar la preparación de la cantidad fabricada"}
Introduce $y=0$ para «no preparamos las máquinas» y $y=1$ para «sí las
preparamos», con $y\in\{0,1\}$. Primero escribe los límites en cada caso:

| Preparación | Cantidad de rovers permitida por el enlace |
|---|---|
| $y=0$ | $x_1=0$ |
| $y=1$ | $0\leq x_1\leq U$ |

**Primero, una regla general.** Si una cantidad debe valer $k_0$ cuando
$y=0$ y $k_1$ cuando $y=1$, escríbela como

$$k_0(1-y)+k_1y.$$

$k_0$ y $k_1$ son datos conocidos; $y$ es la decisión. Al sustituir $y=0$
queda $k_0$; al sustituir $y=1$ queda $k_1$.

Para el máximo de rovers, la tabla da $k_0=0$ y $k_1=U$. Sustituye esos
datos en la regla y usa $0(1-y)+Uy$ como lado derecho de una desigualdad.
Solo al final sustituye $U=4$.

Para las horas, llama $s_0$ al consumo fijo sin preparar y $s_1$ al consumo
fijo al preparar. La expresión general es $s_0(1-y)+s_1y$.
En este relato, no preparar consume $s_0=0$ horas y preparar consume
$s_1=s=3$ horas. Al sustituir, queda $0(1-y)+3y=3y$.
Ese término cuenta las tres horas una sola vez. La hora individual
de cada rover se cuenta aparte. Agregar preparación al consumo de horas no
reemplaza el enlace: revisa si permitiría $x_1=1$ con $y=0$ cuando se omite
ese enlace.

Preparar habilita la fabricación; no obliga a fabricar un lote mínimo. Las
restricciones de recursos se agregan a estos casos y también deben cumplirse.
:::

## Problema 3 · Fabricar cero rovers o un lote de al menos tres

::: exercise {#opt-ent-ej-intento-lote title="Problema 3 · Fabricar cero rovers o un lote de al menos tres"}
Regresa al **problema 1 · Taller original**. Este problema **no incluye las
3 horas de preparación del problema 2**. Cada rover vuelve a consumir
únicamente su hora de calibración habitual.

> Si decidimos fabricar rovers, debemos fabricar **al menos tres**. También
> podemos decidir no fabricar ninguno. La orden del comandante de fabricar
> **como máximo cuatro** sigue vigente.

Aquí un **lote** es el grupo de rovers que decidimos fabricar. «Al menos tres»
permite que tenga tres o cuatro rovers; no significa «exactamente tres» ni
«múltiplos de tres».

1. Llama $L$ al mínimo del lote y $U$ al máximo autorizado. Registra los
   datos $L=3$ y $U=4$, separados de las variables de decisión.
2. Conserva las cantidades $x_1$ y $x_2$ e introduce una binaria para elegir
   entre no fabricar rovers y fabricar el lote. Escribe el mínimo y el máximo
   de $x_1$ en cada caso, usando primero $L$ y $U$.
3. Construye por separado una expresión para el mínimo y otra para el máximo
   que dependan de la binaria. Forma las desigualdades y comprueba los dos
   casos antes de sustituir los valores de $L$ y $U$.
4. Escribe el modelo completo con el objetivo, los recursos, la orden del
   comandante, los enlaces del lote y todos los dominios. Las sondas no
   tienen un tamaño mínimo de lote.
:::

::: hint {#opt-ent-pista-intento-lote of="opt-ent-ej-intento-lote" title="Un mínimo y un máximo que dependen de la decisión"}
Usa $y\in\{0,1\}$: $y=0$ significa «no fabricamos rovers» y $y=1$
significa «fabricamos el lote». Esta es una variable del **problema 3**; no
representa la preparación de máquinas del problema 2.

| Decisión | Condición sobre la cantidad | Mínimo | Máximo |
|---|---|---|---|
| $y=0$: no fabricar | $x_1=0$ | $0$ | $0$ |
| $y=1$: fabricar el lote | $L\leq x_1\leq U$ | $L$ | $U$ |

Construye primero el máximo: debe valer cero cuando $y=0$ y $U$ cuando
$y=1$. Escribe $0(1-y)+Uy$ y simplifica. Después construye el mínimo con
$0(1-y)+Ly$. Coloca cada expresión en el lado apropiado de una desigualdad
para $x_1$.

Sustituye ambos valores de $y$ para verificar que recuperas exactamente los
dos casos de la tabla. Finalmente usa $L=3$ y $U=4$. Un solo enlace puede
dejar pasar planes prohibidos; revisa el mínimo y el máximo por separado.
:::

## Problema 4 · Compartir la antena entre los rovers

::: exercise {#opt-ent-ej-intento-antena title="Problema 4 · Compartir la antena entre los rovers"}
Regresa al **problema 1 · Taller original**. Este problema **no incluye las
3 horas de preparación del problema 2 ni el lote mínimo del problema 3**.
Se pueden fabricar desde cero hasta cuatro rovers, siempre que alcancen los
recursos originales.

> Los rovers comparten una antena de comunicación. Los **primeros dos**
> transmiten **5 MB/día cada uno**. Si fabricamos un tercero o un cuarto, cada
> uno de esos rovers adicionales transmite **3 MB/día**. Los primeros dos
> conservan sus 5 MB/día. Cada sonda sigue transmitiendo 4 MB/día.

1. Distingue los datos de las decisiones. Llama $K$ a la capacidad del primer
   tramo y $U$ al máximo total; aquí $K=2$ y $U=4$. Conserva $x_1$ como
   cantidad total de rovers y $x_2$ como cantidad de sondas.
2. Introduce $u$ para contar los rovers del primer tramo y $v$ para los del
   segundo. Escribe cómo recuperas $x_1$ y qué capacidad tiene cada tramo,
   usando primero $K$ y $U$.
3. La regla permite usar el segundo tramo **solo si el primero está lleno**.
   Introduce una binaria y describe los dos casos: segundo tramo deshabilitado
   o habilitado. Escribe los límites de $u$ y $v$ en cada caso y construye
   los enlaces que los imponen. Esta binaria no representa preparación ni
   elección de lote.
4. Construye la transmisión a partir de $u$, $v$ y $x_2$. Reúne el modelo
   completo, con $x_1$ en los recursos originales, la orden del comandante,
   la relación entre el total y los tramos, las capacidades, los enlaces y
   todos los dominios. Sustituye los parámetros por sus datos al final.
5. Como comprobación local, fija un rover y ninguna sonda: el modelo debe
   contarlo en el primer tramo. Revisa también que usar un rover del segundo
   tramo obligue a tener llenas las dos plazas del primero. Estas
   comprobaciones revisan la formulación; no buscan el plan óptimo.
:::

::: hint {#opt-ent-pista-intento-antena of="opt-ent-ej-intento-antena" title="Construir los dos casos de la antena"}
La cantidad total sigue siendo $x_1$: agrega $x_1=u+v$. Las capacidades
son $K$ para el primer tramo y $U-K$ para el segundo. Ambas cantidades son
enteras y no negativas.

Usa $q\in\{0,1\}$ para habilitar el segundo tramo. Construye primero esta
tabla:

| Caso | Primer tramo | Segundo tramo |
|---|---|---|
| $q=0$: segundo deshabilitado | $0\leq u\leq K$ | $v=0$ |
| $q=1$: segundo habilitado | $u=K$ | $0\leq v\leq U-K$ |

Ya tienes límites comunes de capacidad. Falta que el mínimo de $u$ cambie
de $0$ a $K$, y que el máximo de $v$ cambie de $0$ a $U-K$. Construye
cada límite con $1-q$ y $q$, como en el ejercicio anterior, y conviértelo
en una desigualdad. Después comprueba los dos valores de $q$ y sustituye
$K=2$ y $U=4$.

La condición $q=1$ permite usar el segundo tramo; puede ocurrir $v=0$ si
el primero está lleno. Lo que debe quedar prohibido es $v>0$ con $u<K$.
Esa prohibición debe salir de las restricciones, independientemente del
objetivo. Así, cualquier asignación permitida contabiliza la transmisión
que corresponde a la cantidad fabricada.
:::

## Antes de abrir las soluciones

Ya deberías tener cuatro intentos, identificados como **problemas 1, 2, 3 y
4**, con sus nombres. En los problemas 2, 3 y 4 señala qué cambió respecto del
**problema 1 · Taller original** y verifica que copiaste todas las condiciones
que se conservan.

En cada modelo debes poder seguir el recorrido desde un dato y una regla
hasta su ecuación. Comprueba las reglas condicionales sustituyendo los dos
valores de su binaria. No necesitas conocer ningún óptimo para hacer esta
revisión.

La siguiente página desarrolla esos mismos cuatro modelos y explica cómo se
construye cada renglón: [[el-modelo-del-taller|los modelos, escritos]]. Después
retomaremos únicamente el **problema 1** para aprender enumeración y
ramificación y cotas.
