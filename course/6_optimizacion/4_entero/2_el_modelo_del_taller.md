---
id: el-modelo-del-taller
title: El modelo, escrito
nav_title: El modelo
summary: "Construir cuatro modelos completos: separar datos y decisiones, traducir condiciones, derivar restricciones y sustituir los datos del taller."
status: ready
estimated_time: 30m
tags: [optimizacion, modelado, entera]
---

# El modelo, escrito

**Ten a la vista tus cuatro intentos de la bitácora.** Vamos a construir cada
modelo completo. Los números pequeños nos permiten seguir la escritura, pero
el procedimiento debe servir también con muchos productos y recursos.

En los cuatro problemas seguiremos la misma ruta:

1. **Datos:** qué conocemos y en qué unidades está expresado.
2. **Variables:** qué decidimos y qué valores puede tomar cada decisión.
3. **Condiciones:** qué exige el relato, incluyendo sus alternativas.
4. **Construcción:** cómo convertimos cada condición en una expresión.
5. **Modelo completo:** objetivo, todas las restricciones y dominios.

Primero escribiremos las reglas con parámetros; después sustituiremos los
datos del taller. Un **parámetro** es un dato conocido. Una **variable** es una
decisión cuyo valor todavía debemos elegir. Multiplicar un parámetro por una
variable conserva la linealidad; multiplicar dos variables, en general, no.

**Aquí formulamos.** Comprobaremos unidades y casos para detectar errores de
escritura. Conservaremos las condiciones del relato aunque alguna se pueda
deducir de otras. La búsqueda de la mejor solución comienza en las páginas de
los algoritmos.

## Problema 1 · Taller original

Retomamos el [problema 1 de la bitácora: Taller original](raya:la-bitacora-del-taller#raya-object-opt-ent-ej-modelo-base).
Queremos decidir cuántos rovers y sondas fabricar para maximizar su transmisión
diaria, respetando los recursos y la orden del comandante.

### Datos: nombrar productos, recursos y cantidades conocidas

Para escribir una regla que funcione con más productos, necesitamos indicar
**a cuál producto y a cuál recurso nos referimos**:

| Notación | Significado | En el taller |
|---|---|---|
| $J$ y $j$ | Conjunto de productos e índice de un producto | $J=\{1,2\}$: rover y sonda |
| $I$ y $i$ | Conjunto de recursos e índice de un recurso | $I=\{1,2\}$: aleación y calibración |
| $J_U$ | Productos con un máximo explícito de producción | $J_U=\{1\}$: el comandante limita los rovers |

Los conjuntos $I$ y $J$ son finitos, y $J_U\subseteq J$. Los máximos $U_j$
son datos enteros, finitos y no negativos.

Una expresión que diga «para cada $j\in J$» se aplica una vez a cada producto.
Si hubiera cinco mil productos, cambiaría la lista $J$, no esa regla de
escritura.

Ahora nombramos los datos:

| Parámetro | Qué mide | Datos del taller |
|---|---|---|
| $c_j$ | Transmisión diaria de una unidad del producto $j$ | $c_1=5$, $c_2=4$, en MB/día por equipo |
| $a_{ij}$ | Consumo del recurso $i$ por una unidad del producto $j$ | Aleación: $a_{11}=6$, $a_{12}=4$ kg; calibración: $a_{21}=1$, $a_{22}=2$ h |
| $b_i$ | Cantidad disponible del recurso $i$ | $b_1=24$ kg; $b_2=6$ h |
| $U_j$ | Máximo permitido para el producto $j\in J_U$ | $U_1=4$ rovers, por la orden del comandante |

No necesitamos encontrar una solución para conocer estos parámetros: vienen
del enunciado. Tampoco inventamos un máximo explícito para las sondas.

### Variables: contar lo que vamos a fabricar

Para cada producto $j$, definimos $x_j$ como la **cantidad de unidades que
vamos a fabricar**. En el taller, $x_1$ cuenta rovers y $x_2$, sondas.

::: definition {#opt-entera title="Variable entera"}
Una variable entera toma valores en $\mathbb Z=\{\ldots,-2,-1,0,1,2,\ldots\}$.
Eso no impide los negativos. Como contamos equipos completos y no negativos,
para cada $j\in J$ escribimos las dos condiciones:

$$x_j\in\mathbb Z,\qquad x_j\ge0.$$
:::

### Construir el objetivo: sumar las contribuciones

Una unidad del producto $j$ transmite $c_j$. Fabricar $x_j$ unidades aporta
$c_jx_j$. Al sumar las contribuciones de **todos** los productos obtenemos:

$$\text{transmisión total}=\sum_{j\in J}c_jx_j.$$

El símbolo $\sum$ indica que sumamos un término por cada producto. En el taller,
la expresión se convierte en $5x_1+4x_2$. Como queremos la mayor transmisión,
escribimos «maximizar» esa suma.

### Construir una restricción por recurso

Fijemos un recurso $i$. El producto $j$ consume $a_{ij}x_j$ unidades de ese
recurso. Sumamos los consumos y exigimos que no superen lo disponible:

$$\underbrace{\sum_{j\in J}a_{ij}x_j}_{\text{consumo del recurso }i}
\le\underbrace{b_i}_{\text{disponible}}.$$

Repetimos la misma construcción **para cada $i\in I$**:

| Recurso | Sustitución de sus datos | Unidad de ambos lados |
|---|---|---|
| Aleación, $i=1$ | $6x_1+4x_2\le24$ | kg |
| Calibración, $i=2$ | $x_1+2x_2\le6$ | horas |

Usamos $\le$ porque se permite dejar recursos sin utilizar. Si hubiera mil
recursos, escribiríamos mil filas con la misma regla.

### Escribir las condiciones que no son presupuestos de recursos

La orden del comandante es una condición de producción. Para cada producto
con un máximo explícito, escribimos:

$$x_j\le U_j\qquad(j\in J_U).$$

En el taller produce la restricción $x_1\le4$. La conservamos como una fila
propia: así podemos señalar qué frase del relato representa.

### Reunir el modelo completo

Con parámetros, el **problema 1** queda:

$$\begin{aligned}
\max\quad &\sum_{j\in J}c_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J}a_{ij}x_j\le b_i &&(i\in I),\\
&x_j\le U_j &&(j\in J_U),\\
&x_j\ge0 &&(j\in J),\\
&x_j\in\mathbb Z &&(j\in J).
\end{aligned}$$

Al sustituir los datos, sin eliminar ninguna condición, obtenemos:

$$\begin{aligned}
\max\quad &5x_1+4x_2\\
\text{sujeto a}\quad
&6x_1+4x_2\le24 &&\text{(aleación)},\\
&x_1+2x_2\le6 &&\text{(calibración)},\\
&x_1\le4 &&\text{(orden del comandante)},\\
&x_1,x_2\ge0,\\
&x_1,x_2\in\mathbb Z.
\end{aligned}$$

**Comprueba la escritura:** cada producto aporta al objetivo; cada recurso
tiene una restricción; la orden tiene su propia fila; todas las variables
tienen dominio. Todavía no hemos elegido cuántos equipos fabricar.

## Problema 2 · Preparar la línea de ensamble de rovers

Retomamos el [problema 2 de la bitácora: Preparar la línea de ensamble de rovers](raya:la-bitacora-del-taller#raya-object-opt-ent-ej-intento-encender).
Partimos del problema 1 y agregamos la preparación de las máquinas para
ensamblar rovers. Consume **3 horas una sola vez**, de las mismas 6 horas
disponibles. Además, cada rover conserva su hora de calibración individual.
Las sondas necesitan dos horas cada una y no requieren esa preparación.

### Datos nuevos y decisión nueva

Llamamos $r\in J_U$ al índice del producto que requiere preparación y tiene
un máximo explícito; aquí $r=1$, el rover. Su máximo conocido es $U_r=4$. El $U$ usado en la bitácora se escribe ahora $U_r$ para indicar a qué
producto corresponde. No calculamos otro máximo a partir de los recursos
para construir el enlace.

Para escribir primero el caso general, distinguimos dos datos por recurso:

- $d_{i,0}$: consumo fijo del recurso $i$ si **no preparamos** las máquinas.
- $d_{i,1}$: consumo fijo del recurso $i$ si **sí las preparamos**.

Son **parámetros conocidos**, no variables de decisión, y ambos son no
negativos. El primer subíndice identifica el recurso; el segundo, la opción.
Se miden en las unidades del recurso: kilogramos u horas en este taller.
Son distintos de $a_{ij}$, que mide el consumo **por equipo fabricado**.

$x_j$ sigue contando equipos. Ahora también debemos decidir si preparamos
las máquinas.

::: remark {#opt-binaria title="Representar una decisión con dos opciones"}
Una variable binaria solo toma los valores 0 y 1: $y\in\{0,1\}$.
En el problema 2, $y=0$ significa «no realizamos la preparación» y $y=1$
significa «sí la realizamos».
:::

::: remark {#opt-indicadora title="Dar significado a una indicadora"}
Una indicadora representa una decisión o condición mediante dos valores.
Su dominio binario no escribe automáticamente las consecuencias de elegir
cada opción. Debemos expresarlas como restricciones.
:::

### Construir el consumo fijo por casos

**1. Escribir los dos casos sin sustituir todavía los datos del taller.**

| Decisión | Consumo fijo del recurso $i$ |
|---|---:|
| $y=0$: no preparar | $d_{i,0}$ |
| $y=1$: preparar | $d_{i,1}$ |

**2. Construir una expresión que seleccione el consumo de cada opción.**

$$d_{i,0}(1-y)+d_{i,1}y.$$

El primer término cuenta el consumo de **no preparar**; el segundo, el de
**preparar**. Comprobamos ambas decisiones:

$$\begin{aligned}
y=0:&\quad d_{i,0}(1-0)+d_{i,1}\cdot0=d_{i,0},\\
y=1:&\quad d_{i,0}(1-1)+d_{i,1}\cdot1=d_{i,1}.
\end{aligned}$$

**3. Sumar ese consumo fijo al consumo por equipo.** Para cada recurso,

$$\sum_{j\in J}a_{ij}x_j+d_{i,0}(1-y)+d_{i,1}y\le b_i.
\qquad(i\in I)$$

El consumo fijo se cuenta **una vez**, sin multiplicarlo por la cantidad
fabricada. La restricción sigue siendo lineal: los dos parámetros son datos
y solo $y$ es variable en esos términos.

**4. Sustituir los datos del problema 2.** En este relato, no preparar las
máquinas no consume recursos adicionales. Por eso $d_{i,0}=0$. Llamamos
$d_i$ al consumo de una preparación, de modo que $d_{i,1}=d_i$.

| Recurso $i$ | Sin preparar: $d_{i,0}$ | Al preparar: $d_{i,1}=d_i$ |
|---|---:|---:|
| $1$: aleación | $0$ kg | $0$ kg |
| $2$: horas | $0$ horas | $3$ horas |

Ahora sí, la expresión general se convierte en $0(1-y)+d_i y=d_i y$.
El cero viene del relato; **no es una regla que debamos suponer en otros
problemas**. Si no preparar también consumiera algún recurso, conservaríamos
su parámetro $d_{i,0}$ con el valor correspondiente.

Para las horas, $d_{2,0}=0$ y $d_{2,1}=3$; las $s=3$ horas de la bitácora
corresponden a $d_{2,1}$. Sustituimos paso a paso:

$$\begin{aligned}
\text{Consumo fijo de horas:}\quad &0(1-y)+3y=3y,\\
\text{Presupuesto de horas:}\quad &x_1+2x_2+3y\le6.
\end{aligned}$$

El término $3y$ cuenta la preparación y $x_1$ cuenta la calibración
individual: preparar y calibrar dos rovers requiere $3+2$ horas, antes de
añadir las horas de las sondas. La fila de aleación permanece
$6x_1+4x_2\le24$, porque sus dos consumos fijos son cero.

### Construir el enlace entre preparación y producción

La condición del relato es: **si fabricamos el producto $r$, debemos realizar
su preparación**. Como $x_r\ge0$, podemos escribirla por casos:

| Decisión | Cantidad permitida por esta condición y el máximo conocido |
|---|---|
| $y=0$ | $0\le x_r\le0$ |
| $y=1$ | $0\le x_r\le U_r$ |

El límite inferior permanece en cero. El superior debe seleccionar entre cero
y $U_r$; lo construimos como $0(1-y)+U_r y$. Por tanto,

$$x_r\le0(1-y)+U_r y=U_r y.$$

Ahora sustituimos $r=1$ y $U_r=4$: **$x_1\le4y$**. El cuatro proviene de la
orden del comandante. No es un valor elegido al tanteo ni el resultado de
resolver el problema.

Este enlace impide elegir $x_r>0$ con $y=0$. El consumo fijo por sí solo no
lo impide: una variable binaria necesita tanto su significado como las
restricciones que lo hacen cumplir.

### Reunir el modelo completo

La formulación general conserva los dos parámetros de consumo fijo y los
máximos originales:

$$\begin{aligned}
\max\quad &\sum_{j\in J}c_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J}a_{ij}x_j+d_{i,0}(1-y)+d_{i,1}y\le b_i &&(i\in I),\\
&x_j\le U_j &&(j\in J_U),\\
&x_r\le U_r y,\\
&x_j\ge0 &&(j\in J),\\
&x_j\in\mathbb Z &&(j\in J),\\
&y\in\{0,1\}.
\end{aligned}$$

::: exercise {#opt-ej-encender title="Escribe completo el modelo del problema 2"}
Sustituye los datos del taller, incluidos $d_{i,0}=0$ y $d_{i,1}=d_i$.
Conserva la orden del comandante como una fila
propia. Identifica qué restricción contabiliza la preparación y cuál impide
fabricar rovers sin realizarla. Comprueba los casos $y=0$ y $y=1$.
:::

::: answer {#opt-resp-encender of="opt-ej-encender"}
$$\begin{aligned}
\max\quad &5x_1+4x_2\\
\text{sujeto a}\quad
&6x_1+4x_2\le24 &&\text{(aleación)},\\
&x_1+2x_2+3y\le6 &&\text{(equipos y preparación)},\\
&x_1\le4 &&\text{(orden del comandante)},\\
&x_1\le4y &&\text{(enlace de preparación)},\\
&x_1,x_2\ge0,\\
&x_1,x_2\in\mathbb Z,\\
&y\in\{0,1\}.
\end{aligned}$$

Con $y=0$, el enlace exige cero rovers y la preparación consume cero horas.
Con $y=1$, el enlace permite hasta cuatro rovers y la preparación consume tres
horas. En ambos casos también deben cumplirse los presupuestos de recursos.
Conservar la orden por separado hace visible su origen, aunque el enlace
también imponga ese máximo.
:::

::: exercise {#opt-ent-ej-preparacion-ampliacion title="Reutilizar la construcción sin resolver el modelo"}
Si otro taller permite como máximo $U_r=80$ equipos y prepararlo consume
$d_i$ unidades de cada recurso, ¿qué partes de la formulación cambian?
¿Preparar obliga a fabricar al menos una unidad?
:::

::: answer {#opt-ent-resp-preparacion-ampliacion of="opt-ent-ej-preparacion-ampliacion"}
El enlace pasa a $x_r\le80y$ y cada presupuesto incorpora su dato $d_i y$.
El resto se escribe con los consumos, rendimientos y capacidades de ese taller.
No hace falta enumerar planes para construir esas expresiones.

El relato exige preparar **para poder fabricar**; no prohíbe preparar y luego
no fabricar. Por eso el modelo permite $y=1,x_r=0$. Si el enunciado exigiera
además producir al menos una unidad al preparar, agregaríamos $x_r\ge y$,
aprovechando que la producción es entera. Esa sería una condición adicional,
no algo que deba suponerse.
:::

**Para varias preparaciones independientes:** llama $S\subseteq J_U$ al conjunto de
productos que requieren una preparación propia y tienen un máximo conocido. Introduce $y_j$ para cada
$j\in S$ y $d_{ij}$ para su consumo fijo del recurso $i$. En cada presupuesto
agrega $\sum_{j\in S}d_{ij}y_j$ y escribe un enlace $x_j\le U_jy_j$ por producto,
con $y_j\in\{0,1\}$. El consumo de preparar cada producto se cuenta una sola
vez; los consumos por equipo siguen en $\sum_{j\in J}a_{ij}x_j$.

## Problema 3 · Fabricar cero rovers o un lote de al menos tres

Retomamos el [problema 3 de la bitácora: Fabricar cero rovers o un lote de al menos tres](raya:la-bitacora-del-taller#raya-object-opt-ent-ej-intento-lote).
Este problema vuelve al **problema 1**: no tiene preparación adicional. Agrega
una alternativa: no fabricar rovers, o fabricar un lote de al menos tres,
respetando el máximo de cuatro.

### Datos y variables para representar la alternativa

Llamamos $r\in J_U$ al producto sujeto al lote y con máximo explícito;
aquí $r=1$. Los parámetros $L$ y $U$ de la bitácora se escriben $L_r$ y
$U_r$ para identificar ese producto. Sus datos son:

| Parámetro | Significado | En el taller |
|---|---|---:|
| $L_r$ | Mínimo de unidades si elegimos fabricar | 3 rovers |
| $U_r$ | Máximo permitido por el enunciado | 4 rovers |

Para esta regla suponemos mínimos y máximos enteros con $1\le L_r\le U_r$.
La cantidad $x_r$ sigue siendo una variable entera no negativa.

Definimos $y\in\{0,1\}$: $y=0$ elige no fabricar el producto y $y=1$ elige
fabricar el lote. Esta $y$ pertenece al **problema 3** y no representa la
preparación del problema 2.

### Traducir la frase a dos intervalos

«No fabricar» significa $x_r=0$. «Fabricar al menos $L_r$ sin exceder $U_r$»
significa $L_r\le x_r\le U_r$. Escribimos ambos casos antes de construir los
enlaces:

| Decisión | Límite inferior | Límite superior |
|---|---:|---:|
| $y=0$: no fabricar | 0 | 0 |
| $y=1$: fabricar el lote | $L_r$ | $U_r$ |

### Construir el límite superior que depende de la decisión

Necesitamos cero cuando $y=0$ y $U_r$ cuando $y=1$. La expresión

$$0(1-y)+U_r y$$

selecciona exactamente esos valores. Al usarla como límite superior obtenemos

$$x_r\le0(1-y)+U_r y=U_r y.$$

Este paso **construye un límite por casos**; no consiste en multiplicar
arbitrariamente una restricción existente por una variable. $U_r$ es un dato,
por lo que $U_r y$ es una expresión lineal.

### Construir el límite inferior de la misma manera

Ahora necesitamos cero cuando $y=0$ y $L_r$ cuando $y=1$. Construimos
$0(1-y)+L_r y$ y exigimos

$$x_r\ge0(1-y)+L_r y=L_r y.$$

Las dos desigualdades juntas son

$$L_r y\le x_r\le U_r y.$$

| Decisión | Sustitución en ambas desigualdades | Condición recuperada |
|---|---|---|
| $y=0$ | $0\le x_r\le0$ | No fabricar |
| $y=1$ | $L_r\le x_r\le U_r$ | Fabricar dentro del tamaño permitido |

El enlace superior por sí solo permitiría cantidades menores al lote mínimo
cuando $y=1$. El inferior por sí solo permitiría producir con $y=0$. Necesitamos
ambos para representar la alternativa completa.

### Reunir el modelo completo

El objetivo, los recursos y los máximos del problema 1 se conservan. Añadimos
los dos enlaces y el dominio de $y$:

$$\begin{aligned}
\max\quad &\sum_{j\in J}c_jx_j\\
\text{sujeto a}\quad
&\sum_{j\in J}a_{ij}x_j\le b_i &&(i\in I),\\
&x_j\le U_j &&(j\in J_U),\\
&x_r\ge L_r y,\\
&x_r\le U_r y,\\
&x_j\ge0 &&(j\in J),\\
&x_j\in\mathbb Z &&(j\in J),\\
&y\in\{0,1\}.
\end{aligned}$$

::: exercise {#opt-ej-lote title="Escribe completo el modelo del problema 3"}
Sustituye $r=1$, $L_r=3$ y $U_r=4$, junto con los datos originales del taller.
Señala de qué frase proviene cada fila. Explica qué opción se perdería si
escribieras $x_1\ge3$ sin la variable binaria.
:::

::: answer {#opt-resp-lote of="opt-ej-lote"}
$$\begin{aligned}
\max\quad &5x_1+4x_2\\
\text{sujeto a}\quad
&6x_1+4x_2\le24 &&\text{(aleación)},\\
&x_1+2x_2\le6 &&\text{(calibración)},\\
&x_1\le4 &&\text{(orden del comandante)},\\
&x_1\ge3y &&\text{(mínimo al elegir el lote)},\\
&x_1\le4y &&\text{(cero si no elegimos el lote)},\\
&x_1,x_2\ge0,\\
&x_1,x_2\in\mathbb Z,\\
&y\in\{0,1\}.
\end{aligned}$$

Con $y=0$ ambos enlaces exigen $x_1=0$. Con $y=1$ exigen $3\le x_1\le4$.
Escribir $x_1\ge3$ eliminaría la opción de no fabricar rovers. Las sondas
conservan sus restricciones originales; no les impusimos un lote mínimo.
:::

**Para reutilizar la regla:** si varios productos tienen esta alternativa,
introduce una indicadora propia $y_j$ para cada uno y escribe
$L_jy_j\le x_j\le U_jy_j$. Cada mínimo y máximo debe venir de los datos o de
un límite válido justificado. No es necesario resolver el modelo para escribir
la regla cuando esos límites ya están dados.

## Problema 4 · Compartir la antena entre los rovers

Retomamos el [problema 4 de la bitácora: Compartir la antena entre los rovers](raya:la-bitacora-del-taller#raya-object-opt-ent-ej-intento-antena).
Volvemos a los recursos del **problema 1**, sin preparación ni lote mínimo.
Cambia la transmisión: los primeros dos rovers transmiten 5 MB/día cada uno;
el tercero y el cuarto, 3 MB/día cada uno. Los primeros dos conservan su
rendimiento al añadir más rovers.

### Datos: describir los tramos sin elegir una producción

Un tramo agrupa unidades que tienen el mismo rendimiento. Para un producto
$r\in J_U$, con máximo explícito, describimos dos tramos consecutivos:

| Parámetro | Significado | En el taller |
|---|---|---:|
| $r$ | Producto cuyo rendimiento cambia por tramos | 1, el rover |
| $U_r$ | Máximo total permitido | 4 rovers |
| $K$ | Cantidad de unidades que caben en el primer tramo | 2 rovers |
| $p_1$ | Rendimiento por unidad del primer tramo | 5 MB/día |
| $p_2$ | Rendimiento por unidad del segundo tramo | 3 MB/día |

Suponemos $K$ y $U_r$ enteros con $1\le K<U_r$. Después de las primeras $K$
unidades caben como máximo otras $U_r-K$. Esta resta usa los tamaños dados;
no calcula una solución de producción.

### Conservar las variables originales y agregar el desglose

$x_j$ sigue contando la producción total de cada producto. Agregamos dos
variables enteras no negativas:

- $u$: unidades del producto $r$ que corresponden al primer tramo.
- $v$: unidades del mismo producto que corresponden al segundo tramo.

La suma debe ser exactamente la cantidad fabricada:

$$x_r=u+v.$$

Esta igualdad permite **conservar las restricciones originales sobre $x$**.
No hay que sustituir expresiones en todas las filas del modelo. Los recursos
siguen dependiendo de la producción total, no del rendimiento asignado a cada
tramo.

### Construir los límites de los tramos

El primer tramo contiene como máximo $K$ unidades y el segundo, $U_r-K$:

$$\begin{aligned}
0&\le u\le K,\\
0&\le v\le U_r-K.
\end{aligned}$$

Estos límites todavía permitirían usar el segundo tramo con el primero vacío.
Falta escribir la condición **«para usar el segundo tramo, el primero debe
estar completo»**.

### Traducir el orden de los tramos a dos casos

Introducimos $q\in\{0,1\}$ para representar si habilitamos el segundo tramo.
La palabra «habilitar» significa permitir su uso; no obliga a usarlo.

| Decisión | Primer tramo | Segundo tramo |
|---|---|---|
| $q=0$: no habilitar el segundo | $0\le u\le K$ | $v=0$ |
| $q=1$: habilitar el segundo | $u=K$ | $0\le v\le U_r-K$ |

Construimos primero el límite superior de $v$, igual que en los problemas
anteriores: debe ser cero o $U_r-K$, según la decisión.

$$v\le0(1-q)+(U_r-K)q=(U_r-K)q.$$

Después construimos el límite inferior de $u$: debe ser cero o $K$.

$$u\ge0(1-q)+Kq=Kq.$$

Conservamos también $u\le K$. Así, cuando $q=1$, las dos condiciones obligan
a $u=K$. Cuando $q=0$, el primer tramo puede contener desde cero hasta $K$
unidades, pero el segundo queda vacío.

Si $v>0$, el primer enlace obliga a $q=1$ y el segundo a completar el primer
tramo. La regla queda escrita en las restricciones; no depende de que el
objetivo favorezca una asignación particular.

### Construir el nuevo objetivo sin contar dos veces

Para el producto $r$ reemplazamos su contribución $c_rx_r$ por
$p_1u+p_2v$. Los demás productos conservan sus contribuciones:

$$\sum_{\substack{j\in J\\j\ne r}}c_jx_j+p_1u+p_2v.$$

La suma recorre todos los productos **excepto** $r$. En el taller queda
$4x_2+5u+3v$. No añadimos además $5x_1$: eso contaría dos veces la transmisión
de los rovers.

### Reunir el modelo completo

Conservamos los recursos y máximos originales y añadimos las relaciones de
los tramos:

$$\begin{aligned}
\max\quad &\sum_{\substack{j\in J\\j\ne r}}c_jx_j+p_1u+p_2v\\
\text{sujeto a}\quad
&\sum_{j\in J}a_{ij}x_j\le b_i &&(i\in I),\\
&x_j\le U_j &&(j\in J_U),\\
&x_r=u+v,\\
&0\le u\le K,\\
&0\le v\le U_r-K,\\
&u\ge Kq,\\
&v\le(U_r-K)q,\\
&x_j\ge0 &&(j\in J),\\
&x_j\in\mathbb Z &&(j\in J),\\
&u,v\in\mathbb Z,\\
&q\in\{0,1\}.
\end{aligned}$$

::: exercise {#opt-ej-antena-compartida title="Escribe completo el modelo del problema 4"}
Sustituye los datos del taller. Conserva $x_1$ y $x_2$ en las restricciones de
recursos. Comprueba por casos que no se pueda asignar un rover al segundo
tramo sin completar el primero. Identifica todas las variables y sus dominios.
:::

::: answer {#opt-resp-antena-compartida of="opt-ej-antena-compartida"}
$$\begin{aligned}
\max\quad &5u+3v+4x_2\\
\text{sujeto a}\quad
&6x_1+4x_2\le24 &&\text{(aleación)},\\
&x_1+2x_2\le6 &&\text{(calibración)},\\
&x_1\le4 &&\text{(orden del comandante)},\\
&x_1=u+v &&\text{(producción total)},\\
&0\le u\le2 &&\text{(primer tramo)},\\
&0\le v\le2 &&\text{(segundo tramo)},\\
&u\ge2q &&\text{(completar el primero)},\\
&v\le2q &&\text{(habilitar el segundo)},\\
&x_1,x_2\ge0,\\
&x_1,x_2,u,v\in\mathbb Z,\\
&q\in\{0,1\}.
\end{aligned}$$

Con $q=0$, $v=0$ y toda la producción de rovers está en el primer tramo.
Con $q=1$, $u=2$ y se permite usar el segundo. Por ejemplo, si fijamos tres
rovers para comprobar la escritura, las restricciones exigen $u=2,v=1,q=1$:
su transmisión es $5(2)+3(1)=13$ MB/día. Esto comprueba una representación;
no decide cuántos rovers conviene fabricar.

Con dos rovers, $u=2,v=0$ y ambos valores de $q$ son posibles. Representan
la misma producción y el mismo rendimiento: habilitar el segundo tramo no
obliga a ocuparlo.
:::

**Para reutilizar la construcción:** los parámetros describen los tamaños y
rendimientos; las variables auxiliares describen cómo se distribuye la
producción. Los enlaces obligan a respetar el orden incluso si el segundo
tramo tiene mayor rendimiento que el primero. No necesitamos resolver un
caso con otros rendimientos para justificar esa regla.

Si varios productos tienen dos tramos, introduce sus propias variables
$u_j,v_j,q_j$ y repite las igualdades y enlaces con los tamaños y rendimientos
de cada producto. Conserva $x_j$ en los recursos. En el objetivo, sustituye
únicamente la contribución de los productos con tramos, sin contarla dos veces.
No compartas una indicadora entre decisiones que el relato permite tomar
por separado.

## Revisar que los cuatro modelos estén completos

En cada problema, recorre el enunciado y señala su correspondencia:

| Parte del modelo | Pregunta de revisión |
|---|---|
| Datos | ¿Cada coeficiente, capacidad, mínimo y máximo tiene un origen y una unidad? |
| Variables | ¿Cada decisión tiene significado y dominio, incluidas las auxiliares? |
| Objetivo | ¿Cuenta una sola vez lo que queremos optimizar? |
| Restricciones | ¿Cada condición del relato está representada, en todos sus casos? |
| Modelo completo | ¿Se conservan las condiciones originales que el nuevo enunciado no cambió? |

Tener muchas variables cambia cuántos términos y filas escribimos. Las reglas
que acabamos de construir siguen siendo las mismas: sumar consumos, representar
alternativas y conectar decisiones mediante igualdades o desigualdades.

## Volver al problema 1 para estudiar los algoritmos

Terminamos los planteamientos. Ahora resolveremos el **problema 1: Taller
original**, sin los cambios de los problemas 2, 3 y 4. Su modelo completo sigue
siendo:

$$\begin{aligned}
\max\quad &5x_1+4x_2\\
\text{sujeto a}\quad &6x_1+4x_2\le24,\\
&x_1+2x_2\le6,\\
&x_1\le4,\\
&x_1,x_2\ge0,\\
&x_1,x_2\in\mathbb Z.
\end{aligned}$$

### Una notación compacta para el modelo completo

Más adelante los algoritmos recibirán matrices y vectores. $x$ reúne las
variables y $c$ sus coeficientes en el objetivo. $A$ reúne las filas de
restricciones y $b$ sus lados derechos. En la representación que acabamos de
escribir al regresar al problema 1:

$$A=\begin{pmatrix}6&4\\1&2\\1&0\end{pmatrix},\qquad
b=\begin{pmatrix}24\\6\\4\end{pmatrix},\qquad
c=\begin{pmatrix}5\\4\end{pmatrix}.$$

En esta notación, $b$ reúne los lados derechos de **todas** las filas: dos
presupuestos y la orden del comandante. No es solamente la lista de
disponibilidades de recursos usada al formular.

Hay $n=2$ variables y $m=3$ filas en $A$, incluida la orden del comandante.
No confundas $m$ con el número de recursos: también puede contar otras
condiciones. $c^{\mathsf T}x$ abrevia la suma del objetivo; $Ax\le b$ exige
cumplir **cada** desigualdad de la matriz.

Si escribimos otro de los cuatro modelos en forma matricial, el vector de
decisiones debe incluir **todas** sus variables, también las auxiliares.
Por ejemplo, el problema 4 tiene cinco: $(x_1,x_2,u,v,q)$. En ese orden, sus
coeficientes del objetivo son $(0,4,5,3,0)$. La matriz también debe incorporar
los enlaces y los límites de las binarias; declararlas enteras no basta.

::: definition {#opt-problema-entero title="Problema lineal entero"}
Una forma general para estos modelos de maximización es

$$\begin{aligned}
\max\quad &c^{\mathsf T}x\\
\text{sujeto a}\quad &Ax\le b,\\
&x\ge0,\\
&x\in\mathbb Z^n.
\end{aligned}$$

Las igualdades pueden representarse con dos desigualdades; una condición
$g(x)\ge d$ se puede escribir como $-g(x)\le-d$. Los modelos completos pueden
conservar esas formas originales para que su significado sea más legible.

El conjunto factible es el de las decisiones que cumplen todas las condiciones:

$$F=\{x\in\mathbb Z^n:x\ge0,\ Ax\le b\}.$$

Para los algoritmos de las siguientes páginas también necesitaremos una caja
con límites enteros finitos que contenga todas las soluciones factibles.
:::

### Una pregunta para pasar de formular a resolver

El modelo dice qué planes están permitidos y cómo medirlos. Todavía necesitamos
un procedimiento para encontrar el mejor y demostrar que no queda otro mejor.

Permitir fracciones produciría una relajación lineal: conservaríamos las
restricciones, pero permitiríamos valores reales. ¿Bastaría resolverla y
redondear? Redondear puede violar recursos; aunque produzca un plan factible,
por sí solo no demuestra que sea óptimo.

**Punto de parada:** ya tienes cuatro modelos completos y puedes justificar
cómo se construyó cada fila. Primero resolveremos el taller por
[[enumerar|enumeración]]. Después usaremos relajaciones dentro de
[[ramificar-y-acotar|ramificación y cotas]].
