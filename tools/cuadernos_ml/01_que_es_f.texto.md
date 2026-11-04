<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c1-nb01
Contrato: v5.1 · API ml_lab: 1.1 · Protocolo: p5.2
Plan: clase_1 (sha256 478d429f)
Rama de origen: aprendizaje-maquina-clase-1@513a721705582d5c2b7244a578b561a0e7befa28
Archivo permitido: tools/cuadernos_ml/01_que_es_f.texto.md

Decisiones del registro que aplican
D-008: sin fechas ni plazos; recorrido autónomo en casa y repaso en clase.
D-009.1: notación del curso; D-009.5: cifras tomadas del brief y su código.
D-013a: API y cifras ratificadas; se conserva la URL indicada en el brief.
D-015: notación aditiva admitida según la regla por omisión.
Se aplica la anatomía del notebook; las reglas de página de U9 no añaden
frontmatter, directivas, wikilinks ni secciones ajenas a las claves del código.
-->

### celda: portada

# Notebook 1 · ¿Qué es f? El proceso, el piso y la representación

Acompaña la página [¿Qué es f?](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/). Duración: ~25 min.

Puedes recorrerlo solo en casa, de arriba abajo. Ejecuta primero la celda de
arranque. En cada bloque, escribe tu predicción antes de ejecutar «Juega»;
después mueve los controles, mira el resultado y abre «Explicación».

### celda: idea

En las entregas, $x$ reúne lo que describes y $y$ es el tiempo observado:
$y=f(x)+\varepsilon$, con $f$ como función del proceso y $\varepsilon$ como ruido,
no como cadena vacía.
Para un predictor $f_\beta$, con parámetros $\beta$, el riesgo
$R(\beta)=E[\ell(y,f_\beta(x))]$ promedia la pérdida $\ell$ en la población;
$E$ indica esperanza. Aquí usamos pérdida cuadrática para los tiempos.
[Proceso generador y Riesgo y error de generalización](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-def-proceso-generador) conectan ambas ecuaciones.

### celda: bloque-1-predice

**Predice.** Si cambias la semilla, ¿qué se mueve: los puntos, la línea verde ($f$), la recta ajustada?

Elige una respuesta: solo los puntos; los puntos y la recta; o también la línea
verde. Conserva «proceso» en «entregas», «ruido σ_ε» en 1 y «datos n» en 20.
Mueve únicamente «semilla» y compara la nube, ambas líneas y el riesgo impreso.
Después puedes explorar «recíproca», «mezcla de logaritmos» y «seno» en «proceso».

### celda: bloque-1-mira

**Mira.** En la gráfica, los círculos son las 20 entregas de entrenamiento; los puntos pequeños son 300 observaciones nuevas.
La línea gruesa verde es $f$; la delgada es la recta ajustada $\widehat f$.

Debajo, `L_ent` mide el error en entrenamiento; la media es el punto de comparación (*benchmark*).
La cifra impresa junto a $R(\widehat\beta)$ aproxima ese riesgo con las 100 000 observaciones del despliegue.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Al mover el control, cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

La función $R(\beta)=E[\ell(y,f_\beta(x))]$ permanece fija; cambia el ajuste
$\widehat\beta$ donde la evalúas. El gorro identifica lo estimado con los datos:
$\widehat f=f_{\widehat\beta}$. Es la distinción de
[Lo estimado lleva gorro](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-def-estimacion).

Aquí $L$ denota un error promedio, no un lenguaje. Con los controles iniciales,
la recta tiene $L_{\text{ent}}=0.450$ en
entrenamiento y riesgo aproximado 1.025 en el despliegue, frente a 49.073 de la
media en el despliegue. Esa aproximación usa 100 000 observaciones. En los otros
procesos, la recta no alcanza la forma de $f$: hay un problema de aproximación,
además del azar.

</details>

### celda: bloque-2-predice

**Predice.** Si duplicas $\sigma_\varepsilon$ de 1 a 2, ¿el piso se duplica o se cuadruplica?

Anota una de las dos opciones. En «ruido σ_ε», pasa de 1 a 2 y deja «datos n»
en 20. Compara el valor impreso de `R_Bayes` y la altura de la línea punteada.
El oráculo es el predictor que conoce $f$; tampoco puede conocer el ruido de
una entrega nueva.

### celda: bloque-2-mira

**Mira.** Cada barra muestra el riesgo aproximado en el despliegue del oráculo $f$, la recta ajustada o la media; la línea punteada marca el piso.
La barra del oráculo queda cerca de esa línea, un poco arriba o abajo; ninguna queda claramente por debajo.
Los renglones impresos separan $L_{\text{ent}}$, el error en entrenamiento, de $R$, el riesgo aproximado en el despliegue.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

Se cuadruplica: el piso pasa de 1 a 4. En este proceso,
$R_{\text{Bayes}}=\sigma_\varepsilon^2$, como explica
[El piso: error de Bayes](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-def-error-bayes).
La varianza del ruido, $\sigma_\varepsilon^2$, mide su dispersión cuadrática
alrededor de su media cero. El control mueve su desviación estándar
$\sigma_\varepsilon$; duplicarla cuadruplica la varianza.

Ni conocer $f$ permite bajar ese piso en la población. Con ruido 1, el oráculo
imprime un riesgo aproximado de 0.991 en el despliegue: las 100 000
observaciones aproximan la esperanza. Su $L_{\text{ent}}=0.489$ en entrenamiento
tampoco contradice el piso poblacional. Si mueves «datos n», ese error puede
quedar arriba o abajo del piso.

</details>

### celda: bloque-3-predice

**Predice.** ¿Qué baja más el error en el despliegue: subir el grado a 5 o medir si llovía?

Elige entre subir «grado N», activar «medir la lluvia x₂» o esperar una mejora
parecida. Primero deja el interruptor apagado y lleva «grado N» de 1 a 5;
anota $R$ en el despliegue. Luego vuelve al grado 1, activa el interruptor y
compara $R$ y el piso.

Aquí $x_1$ es la distancia y $x_2$ indica si llovía. $x_i$, con la letra $i$,
es la observación $i$; $x_1, x_2, \dots$, con número, son **variables**
(columnas); $x_{ij}$ es la variable $j$ de la observación $i$.

### celda: bloque-3-mira

**Mira.** A la izquierda, cada punto es una entrega; al medir la lluvia, los colores distinguen las dos franjas de la nube.
A la derecha, la barra es el riesgo aproximado en el despliegue y la línea punteada es el piso.
Compara también las columnas visibles impresas: al incorporar $x_2$, el piso pasa de 10 a 1.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Medir la lluvia baja más el error en este experimento. Sin medirla, el piso es
10 y el riesgo aproximado con grado 1 es 10.89 en el despliegue; medirla baja el
piso a 1.

Subir el grado no baja el piso y aquí empeora el ajuste: sin medir la lluvia, con grado 5 el riesgo sube de 10.89 a 15.73. Una curva más flexible de la distancia no revela si llovió, y con 20 datos persigue el ruido.

Con pérdida cuadrática, la mejor predicción con lo visible es la media
condicional $E[y\mid x_{\text{visibles}}]$: el tiempo promedio entre entregas
con esos valores visibles. No la confundas con $f$ si omitiste la lluvia.
[La lluvia: ruido que no es ruido](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-ejm-lluvia)
explica por qué el piso depende de lo que mides.

</details>

### celda: bloque-4-predice

**Predice.** En cartesianas, ¿la logística pasará de 60 % de aciertos? ¿Y en polares?

Anota sí o no para cada representación. Conserva «radio exterior» en 1.6,
«grosor» en 0.4 y «ruido» en 0.15. En «representación», compara «cartesianas
(1, x₁, x₂)» con «polares (1, r, θ)» mirando los aciertos en el despliegue.
Después elige «solo radio (1, r)» y observa la frontera.

Aquí $x_1,x_2$ son coordenadas del punto; $r$ es su radio, no una recompensa,
y $\theta$ es el ángulo, no un parámetro ajustado. La representación $\phi$
construye las variables que recibe el modelo; la matriz $\Phi$ las reúne, con
una fila por observación.

### celda: bloque-4-mira

**Mira.** Cada punto es una observación coloreada por su clase; la frontera separa las clases que predice la logística.
En polares, el eje horizontal es $\theta$ y el vertical es $r$: un radio fijo se ve horizontal; la frontera ajustada puede inclinarse un poco.

La línea punteada es la frontera ideal, $r=1.31$: el radio donde las dos clases son igual de probables.
Debajo aparecen cuatro filas de $\Phi$, con «1» primero; compara los aciertos en entrenamiento y en el despliegue con la moda y con los aciertos del oráculo.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Con los valores iniciales, cartesianas no pasa de 60 %: logra 48 % de aciertos
en el despliegue, frente al 50 % de la moda. Polares sí: logra 75 %; solo radio
también logra 75 %. Los aciertos del oráculo en el despliegue son 76 %;
el oráculo conoce las probabilidades del proceso y clasifica con ellas.
Con una muestra finita, esa cifra aproxima el techo de Bayes de la población;
no es una cota exacta para otros clasificadores en esa misma muestra.
La moda predice siempre la clase más frecuente del entrenamiento.

Cambió $\phi$, con la misma logística y el mismo optimizador. Compara sus
columnas: $(1,x_1,x_2)$, $(1,r,\theta)$ y $(1,r)$. La columna de unos permite
un término constante, como en
[Modelo lineal: lineal en sus parámetros](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-def-modelo-lineal).
Con solo radio, la frontera es exactamente horizontal:
$r=-\widehat\beta_0/\widehat\beta_1$. En polares, el coeficiente ajustado de
$\theta$ explica la pequeña inclinación.

Al aumentar «ruido», ni el oráculo llega al 100 % de aciertos en el despliegue.
Si una muestra resulta separable, la celda lo avisa: sin penalización, la
logística no tiene coeficientes óptimos finitos. Crecen hasta que el
optimizador se detiene; esa parada no es un óptimo finito.

</details>

### celda: bloque-5-predice

**Predice.** ¿Cuál de estas cuatro $\phi$ necesita un algoritmo distinto de mínimos cuadrados?

Elige una, todas o ninguna: $(1,x)$, $(1,x,x^2)$, $(1,1/x)$ y $(1,x)$ con un
indicador de lluvia. Conserva «proceso» en «entregas con lluvia» y recorre las
opciones de «φ». Compara la forma de la curva, las columnas de $\Phi$ y la
línea `m = ml.ajustar(datos, phi=...)` impresa bajo la gráfica.

### celda: bloque-5-mira

**Mira.** En la gráfica, las curvas muestran las predicciones; al incluir el indicador aparecen una curva sin lluvia y otra con lluvia.
Debajo, $\Phi$ muestra las variables transformadas: sus columnas cambian con «φ», mientras la llamada a `ml.ajustar` permanece igual.
Los renglones de errores comparan $L_{\text{ent}}$ en entrenamiento y $R$ aproximado en el despliegue con la media en cada conjunto.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

Ninguna necesita otro algoritmo: todas son lineales en $\beta$. Por ejemplo,
$f_\beta(x)=\beta_0+\beta_1x+\beta_2x^2$ curva la predicción en $x$, pero
combina las columnas de $\Phi$ linealmente en sus parámetros. Esa es la
distinción de
[Modelo lineal: lineal en sus parámetros](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/el-problema/que-es-f/#raya-object-ml-c1-def-modelo-lineal).

El indicador de lluvia agrega una columna con codificación de base mediante
`ml.dummies("x2")`. Si cambias «proceso» a «recíproca», esa opción no aplica:
el proceso no trae lluvia y la celda lo dice.

La elección de columnas también exige mirar el dominio. En «entregas con
lluvia», la distancia $x_1$ puede acercarse a cero: con $(1,1/x_1)$ este ajuste tiene riesgo verdadero infinito, porque su coeficiente de $1/x_1$ no es cero. El promedio finito impreso sobre observaciones del
despliegue no lo convierte en un riesgo finito; atiende el aviso de la celda.

</details>

### celda: taller-intro

**Taller.** Ejecuta el ejemplo activo y después copia una alternativa comentada:
recíproca, seno o lluvia con `ml.caso(2)`. Quita el signo de comentario de todas
las líneas de la alternativa elegida y conserva `ml.taller(datos, clase=1)` al
final. La última asignación a `datos` será la que use el taller.

Mira la nube con $f$ y el panel de errores de los polinomios. Identifica las
etiquetas de entrenamiento, riesgo en el despliegue, piso y media como
benchmark; por ahora basta ubicarlas. Si añades `phi=` a la llamada del taller,
también verás su matriz $\Phi$.

### celda: galeria-intro

**Galería.** Pulsa «Caso 1», lee la pregunta que aparece y escribe tu respuesta
antes de abrir «¿Qué se ve?». Haz lo mismo con «Caso 2».
En el caso 1 la celda no imprime coeficientes: antes de abrir «¿Qué se ve?», anota si esperas el coeficiente estimado de $x_1$ mayor, menor o igual que 1, y por qué; luego compáralo con la explicación.
En el caso 1, ignora por ahora la curva de capacidad: la retoma el notebook 02.
En el caso 2 la celda no imprime cifras: para leer el piso y el riesgo $R$ de tu
mejor recta, vuelve a las cifras que imprime el bloque 3 con el interruptor
apagado y el grado 1.

### celda: ejercicio-piso

**Ejercicio.** Con $\sigma_\varepsilon=0.5$, ¿cuánto vale el piso? Compruébalo en
el bloque 2. Anota tu cálculo y el valor de `R_Bayes` que imprime la celda.

**Pista:** ¿el deslizador mueve la desviación estándar o su cuadrado?

### celda: ejercicio-piso-respuesta

<details><summary>Explicación</summary>

El piso es $R_{\text{Bayes}}=0.5^2=0.25$. Al poner «ruido σ_ε» en 0.5,
`R_Bayes` imprime 0.250. La barra del oráculo aproxima ese piso con las
observaciones del despliegue; no tiene que coincidir exactamente con la línea.

</details>

### celda: ejercicio-phi

**Ejercicio.** Elige la $\phi$ del bloque 5 que da menor $R$ para la recíproca
y explica por qué su $\Phi$ tiene dos columnas. Cambia «proceso» a «recíproca»
y compara el riesgo aproximado en el despliegue de las opciones que aplican.

**Pista:** ¿qué transformación reproduce la forma recíproca y qué columna
permite sumar una constante?

### celda: ejercicio-phi-respuesta

<details><summary>Explicación</summary>

Gana $(1,1/x)$ en esta comparación: permite representar la forma recíproca
del proceso con una constante y un coeficiente que multiplica $1/x$.
$\Phi$ tiene dos columnas, la de unos y la de $1/x$; cada fila corresponde a
una observación. La opción con lluvia no compite porque este proceso no trae
esa variable.

</details>

### celda: cierre

Te llevas: $f$ no se ve; el piso depende de lo que mides; la representación decide.
La pregunta: ¿por qué no subir el grado hasta que el error sea cero? (notebook 02).
