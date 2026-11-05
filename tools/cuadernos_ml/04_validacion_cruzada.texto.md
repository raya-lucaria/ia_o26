<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c2-guion-04
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_2 (sha256 a764ccaf)
Rama de origen: aprendizaje-maquina-clase-2@9a0d9c8f4c48a34dcdf28b19eb974fc0d4d4b24e
Archivos permitidos: tools/cuadernos_ml/04_validacion_cruzada.texto.md
-->

### celda: portada

# Notebook 4 · Validación cruzada

Acompaña la página [Validación cruzada](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/validacion-cruzada/). Duración: ~35 min.

Ejecuta primero la celda de arranque. Antes de abrir cada «Juega», escribe tu
apuesta; luego mueve los controles, lee la figura y abre «Explicación».
Puedes recorrerlo por tu cuenta: la prueba permanece cerrada mientras eliges.

### celda: idea

La validación cruzada (*cross-validation*) rota la reserva dentro del
desarrollo. Promedia las pérdidas de esas vueltas, como explica [Validación cruzada](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/validacion-cruzada/):

$$
\mathrm{CV}_k(N)=\frac{1}{k}\sum_{m=1}^{k}L_{\mathcal D_m}(\widehat\beta^{(-m)}(N)),
\qquad
\widehat N\in\operatorname*{arg\,min}_N\mathrm{CV}_k(N).
$$

Con empate, el más simple: el menor $N$. No necesitas observar un empate para aplicar la regla.

Aquí $k$ cuenta pliegues; $m$ identifica el reservado; $\widehat\beta^{(-m)}$ se ajusta sin él.
Con $k=5$, promedias cinco pérdidas. $L$ conserva su sentido de pérdida promedio.
Avisos de letras: $k$ ya no cuenta estados, simulaciones ni clases;
$m$ no indica aristas, profundidad ni tiempo medio de llegada.

### celda: bloque-1-predice

**Predice.** Con $k=5$ y 48 entregas de desarrollo, ¿con cuántas entregas se ajusta cada modelo de pliegue?

Apuesta un número antes de ejecutar. Elige entre usar todas, usar solo las
reservadas o usar las restantes. Conserva «pliegues k» en 5 y recorre «vuelta m».

### celda: bloque-1-mira

**Mira.** A la izquierda, cada columna representa una entrega; la fila activa muestra qué pliegue valida. La prueba queda aparte.
A la derecha, los círculos ajustan y los triángulos validan. La curva es
$\widehat\beta^{(-m)}$: cambia al cambiar «vuelta m».

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Con los valores iniciales, la vuelta 1 ajusta con 38 entregas y valida con 10.
Las 48 no se reparten exactamente entre cinco pliegues: otras vueltas ajustan con 39.

Cada entrega valida una vez y participa en el ajuste de las otras vueltas.
La prueba nunca rota. La fórmula de «Validación cruzada»,
$\mathrm{CV}_k=\frac{1}{k}\sum_{m=1}^{k}L_{\mathcal D_m}(\widehat\beta^{(-m)})$,
promedia errores de modelos distintos: cada uno excluyó su pliegue de validación.
Por eso, mover «vuelta m» cambia tanto los triángulos como la curva.

</details>

### celda: bloque-2-predice

**Predice.** ¿Elegirá la CV el mismo grado que el entrenamiento? ¿Y la regla de un EE, uno mayor o menor que el mínimo?

Apuesta un número para cada grado elegido. Para «un EE», admite también
«igual». Compara «mínimo» y «un EE» en «regla»; después activa «mostrar la realidad R».

### celda: bloque-2-mira

**Mira.** Los triángulos muestran medias CV; las barras, EE aproximados. Compara medias con el umbral, ambas marcas y $L_{\text{ent}}$; la curva crema muestra $R$.
Bajar de la raya-punto del punto de comparación (*benchmark*) es una señal.

Al mover «semilla», cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

Con los valores iniciales, ambas reglas eligen $N=6$: CV $9.69\pm1.33$; 66 ajustes. El entrenamiento prefiere 12.
Compara con el benchmark impreso: «la media de entrenamiento como punto de comparación; la clase 3 lo define».
En el despliegue, su $R=27.3$ supera 11.0 del grado 4; compara también $R$ en $N=0$.

El grado 6 se dobla en los bordes. En general, CV no favorece el grado máximo; tampoco garantiza el menor $R$.
«Validación cruzada» toma el menor $N$ cuya media cumple
$\mathrm{CV}_k(N)\le\mathrm{CV}_k(\widehat N_{\min})+\mathrm{EE}_{\mathrm{CV}}(\widehat N_{\min})$:
un grado igual o menor que el mínimo.
Las pérdidas fuera de pliegue dependen: comparar da una señal.

</details>

### celda: bloque-3-predice

**Predice.** ¿Qué varía menos entre muestras: $\mathrm{CV}_5$ o $L_{\text{val}}$ con 12 entregas? ¿Siempre?

Apuesta un número para la desviación de cada estimador. Elige CV, una
validación o dispersión parecida. En «estimador», pasa de «una validación» a
«ambos» para comparar los histogramas.

### celda: bloque-3-mira

**Mira.** Cada histograma reúne estimaciones de muestras distintas; su ancho muestra cuánto varían.
La línea vertical señala $E_{\mathcal D}[R]$ del ajuste evaluado por la validación.
Debajo, compara «desviación real» con «EE medio reportado»: una se mide entre
muestras; el otro se calcula dentro de cada muestra. Lee también el costo en ajustes.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Con los valores iniciales, la desviación real es 4.85 para validación y 3.12
para CV. Sus EE medios reportados son 4.37 y 2.24, respectivamente.
Aquí CV varía menos; su EE reportado queda por debajo de su dispersión real.
Cuesta cinco ajustes, frente a uno.

La fórmula $\mathrm{CV}_k=\frac{1}{k}\sum_{m=1}^{k}L_{\mathcal D_m}(\widehat\beta^{(-m)})$
de «Validación cruzada» promedia vueltas que comparten datos de ajuste.
Sus pérdidas dependen entre sí; las barras no son intervalos de confianza exactos.
La observación sobre el EE de CV explica esa cautela.
Con otros procesos cambia la ganancia: CV no tiene siempre menor varianza.

</details>

### celda: bloque-4-predice

**Predice.** En el caso 16, ¿qué grado tendrá un pliegue con error enorme: el 1 o el 8?

Apuesta un número para el mayor error por pliegue. Elige grado 1, grado 8 o
ambos. Conserva «datos» en «caso 16» y «estadístico» en «pérdida cuadrática».

### celda: bloque-4-mira

**Mira.** Cada triángulo es el resultado de un pliegue; cada caja reúne los de un grado.
Busca los triángulos que se escapan y el rótulo del pliegue 3. Compara los
grados 1, 4 y 8 con el grado 0, el benchmark. Cambia «estadístico»: la altura pasa a representar otra cantidad,
no necesariamente una pérdida.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Con los valores iniciales, el grado 8 se dispara en los pliegues 2 y 3.
El grado 1 tiene pérdidas por pliegue entre 11.33 y 18.61.
La caja del grado 0 muestra el benchmark en los mismos pliegues.
Ambos fallan en la zona escasamente cubierta: el pliegue 2 interpola y el 3 extrapola; la figura rotula el 3.

En «Validación cruzada», $e_i=y_i-\widehat y_i$ y $\ell_i=e_i^2$ conectan residual y pérdida cuadrática.
La varianza usa residuales con signo y divide entre el tamaño del pliegue menos uno.
La proporción cuenta errores absolutos mayores que `UMBRAL_MIN`.
Cada estadístico se calcula dentro del pliegue; después se promedian los resultados por igual.

</details>

### celda: bloque-5-predice

**Predice.** Con 6 positivos y 5 pliegues al azar, ¿qué tan seguido queda algún pliegue sin positivos? ¿Y estratificando?

Apuesta un número porcentual para cada método: nunca, pocas veces o casi
siempre. Cambia «pliegues» entre «al azar» y «estratificados»; conserva
«positivos» en 6 y «k» en 5.

### celda: bloque-5-mira

**Mira.** Cada columna es una observación; el color distingue su etiqueta y la fila muestra dónde valida.
Cuenta positivos en cada pliegue de esta partición. Debajo aparecen las
fracciones de particiones con algún pliegue vacío de positivos: compara ambos
métodos, no solo el dibujo de una semilla.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

Con los valores iniciales, las fracciones son 88 % al azar y 0 % estratificando.
La partición al azar con semilla 0 reparte los positivos como 2, 2, 1, 0, 1.

Estratificar garantiza positivos en cada pliegue mientras haya al menos tantos
positivos como pliegues. Si $\text{positivos}<k$, necesariamente alguno queda
vacío: es el principio del palomar de «Validación cruzada».
Prueba 3 positivos con $k=5$: ningún método puede llenar todos. Baja $k$.
Si el despliegue exige separar por tiempo o grupos, esa estructura manda;
conservar proporciones no basta para decidir la separación.

</details>

### celda: bloque-6-predice

**Predice.** La $\mathrm{CV}_5$ del grado ganador, ¿sobreestima, acierta o subestima el error del procedimiento entrenado con el mismo tamaño?

Apuesta un número para la diferencia promedio. Elige positiva, cero o negativa.
En «repeticiones», compara 10, 20 y 30. El precálculo se hace una vez;
el control muestra una parte de sus resultados.

### celda: bloque-6-mira

**Mira.** Cada punto promedia repeticiones; las barras muestran dos EE de Monte Carlo.
Compara las tres primeras marcas al tamaño aproximado de una vuelta externa.
La cuarta usa todo el desarrollo; la quinta muestra «R del benchmark».
Los riesgos vienen del visor de la realidad, `datos.despliegue`: solo existe en el simulador.

### celda: bloque-6-explica

<details><summary>Explicación</summary>

Con los valores iniciales, 30 repeticiones y grados de 0 a 8, la CV del ganador
promedia 10.00; la anidada, 11.79. El $R$ del procedimiento a 4/5 promedia
12.69; el del modelo final, 11.43.
La quinta columna, «R del benchmark», evalúa la media ajustada con todo el desarrollo.

En promedio, elegir el mínimo favorece estimaciones bajas por azar:
$E[L_{\text{val}}]\le E[R]$ expresa el efecto de selección en «Entrenamiento y prueba».
La anidada evalúa la elección completa sin usar el pliegue externo para elegir.
Estima el riesgo del procedimiento al tamaño de una vuelta externa.
El modelo final usa más datos y suele mejorar: selección y tamaño son efectos distintos.

</details>

### celda: taller-intro

**Taller.** Ejecuta la celda visible. Después copia una alternativa comentada
y deja la llamada a `ml.taller` al final.

- Con otra $f$, cambia la forma del proceso y observa si cambia el grado elegido.
- Con el caso 16, busca los pliegues que traen una entrega lejana.
- Con los mismos datos, compara `k=3` y `k=10`: anota la elección y el costo en ajustes.

Conserva `que="elegir"` y `regla="un_ee"` para comparar la misma regla.
La última asignación a `datos` determina qué ejemplo usa el taller.

### celda: galeria-intro

**Galería.** Abre los casos 13–16 como misterios. Lee la pregunta de cada caso,
anota tu apuesta y busca una pista visual antes de abrir la explicación.

En el caso 13, compara $L_{\text{prueba}}$ con $R$: el polinomio usa solo la distancia, sin tiempo, y la prueba al azar casi no engaña.
Contrasta lo que ves con la explicación: la página muestra el engaño con vecinos en distancia y tiempo.
En el caso 16, busca en qué pliegues distintos caen las dos entregas lejanas y cuánto sube el error de cada uno.
En cada misterio, identifica qué decisión cambió y qué comparación permite juzgarla.

### celda: ejercicio-cinco-pliegues

**Ejercicio.**

Cinco pliegues dan $L_{\mathcal D_m}=9.2,\ 9.0,\ 9.1,\ 8.7,\ 8.8$, en minutos cuadrados.
(a) Calcula $\mathrm{CV}_5$. (b) Calcula $\mathrm{EE}_{\mathrm{CV}}$.

**Pista:** ¿Con qué divisor va la desviación de cinco números?

### celda: ejercicio-cinco-pliegues-respuesta

<details><summary>Explicación</summary>

**(a)** $\mathrm{CV}_5=8.96$. Las desviaciones respecto de esa media son $0.24,0.04,0.14,-0.26,-0.16$.

**(b)** Sus cuadrados suman $0.172$. La desviación es $s=\sqrt{0.172/4}\approx0.207$; por tanto, $\mathrm{EE}_{\mathrm{CV}}\approx0.093$.
El divisor de la varianza muestral es cuatro; el EE divide después la desviación entre $\sqrt5$.

</details>

### celda: cierre

La CV rota la validación dentro del desarrollo y permite elegir el grado sin
abrir la prueba. Con los valores iniciales, ambas reglas eligieron grado 6;
eso no garantizó el menor riesgo. Mira también los pliegues y distingue la
evaluación del procedimiento de la del modelo final.

La pregunta que sigue es: ¿de dónde sale la U?
