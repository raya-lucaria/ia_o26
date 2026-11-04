<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c2-guion-05
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_2 (sha256 a764ccaf)
Rama de origen: aprendizaje-maquina-clase-2-completo@64a50c219de098a5b4600323dbdd55342fbab6b7
Archivo permitido: tools/cuadernos_ml/05_sesgo_y_varianza.texto.md

Decisiones del registro que aplican
D-008: sin fechas ni plazos; recorrido autónomo y repaso en clase.
D-009.1: notación traducida a la del curso; D-009.3: parámetro e
hiperparámetro se retoman de la clase 1; D-009.5: cifras del brief.
D-009.6: el caso 13 elige proceso y modelo para exhibir el engaño temporal.
D-013, incluida D-013c-c2: API, nombres e ids ratificados para este lote.
D-015: notación aditiva admitida según la regla por omisión.
Se conserva el encabezado HTML del modelo. Se aplica la anatomía del
notebook, sin frontmatter, badge, directivas ni cierre de página.
-->

### celda: portada

# Notebook 5 · Sesgo y varianza

Acompaña [Sesgo y varianza: de dónde sale el error](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/). Duración: ~35 min.

Ejecuta primero la celda de arranque. Recorre los bloques en orden: apuesta
antes de ejecutar «Juega», mueve un control y contrasta tu respuesta con
«Explicación». Puedes hacerlo por tu cuenta.

Ubica el punto de comparación (*benchmark*) en las salidas:
la media de entrenamiento como punto de comparación; la clase 3 lo define.

### celda: idea

Una recta puede equivocarse casi igual con cada muestra; una curva flexible
puede cambiar mucho entre muestras. Separaremos ese desplazamiento, esa
dispersión y el ruido de una entrega nueva. Con pérdida cuadrática:

$$E_{\mathcal D,\varepsilon}\bigl[(y-\widehat f(x))^2\mid x\bigr]=\sigma_\varepsilon^2(x)+\text{sesgo}(x)^2+\text{varianza}(x).$$

La identidad [Ruido, sesgo y varianza](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-teo-sesgo-varianza)
promedia sobre entrenamientos y ruido nuevo, independiente del entrenamiento.
Supone segundos momentos finitos, todas las variables visibles y
$E[\varepsilon\mid x]=0$. Aquí $\varepsilon$ es ruido; recuerda los avisos de
letras del curso. En el proceso inicial, su aportación es $9.0$.

### celda: bloque-1-predice

**Predice.** ¿Qué grado tendrá el abanico más ancho en $x_0=5$: 1, 4 o 12?

Apuesta un número: el grado. Conserva «x0 (km)» en 5 y compara «grado N».
Activa «ver la diana». Aquí $x_0$ es un punto fijo de $x$, no el centro
de Taylor de la clase 1.

### celda: bloque-1-mira

**Mira.** Cada línea delgada viene de otra muestra; la gruesa discontinua
promedia ajustes; la verde muestra $E[y\mid x]$. En la diana, cada marca
es una predicción; las dos líneas indican promedio y verdad.
El control evita los bordes: el grado 12 puede extrapolar allí y perder
escala. Consulta sesgo y varianza impresos al mover «x0 (km)».

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Con los valores iniciales, $E[y\mid x_0]=31.5$. Al comparar los grados en
ese punto, gana el 12 en anchura: desviación 3.5, frente a 0.9 del grado 1.
Sus sesgos son $-0.5$ y $1.5$, respectivamente, con 100 muestras.

En [La diana en x = 5](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-diana),
$\text{sesgo}(x)=E_{\mathcal D}[\widehat f(x)]-f(x)$ mide el desplazamiento;
$\text{varianza}(x)=\operatorname{Var}_{\mathcal D}(\widehat f(x))$ mide la dispersión.
Aquí $f(x)=E[y\mid x]$.

En este punto domina el sesgo cuadrado del grado 1 y la varianza del 12.
La recta se equivoca parecido; el grado alto cambia más entre muestras.
Es una comparación local: verifica las cifras al cambiar $x_0$.

</details>

### celda: bloque-2-predice

**Predice.** Si duplicas el ruido $\sigma_\varepsilon$, ¿qué barra crece: el ruido, el sesgo², la varianza o varias?

Apuesta un número: el factor por el que cambiará la aportación del ruido.
En «ruido σ», pasa de 3 a 6; deja «entregas n» en 60.
La etiqueta del control nombra $\sigma_\varepsilon$, la desviación del ruido.

### celda: bloque-2-mira

**Mira.** A la izquierda, cada barra apila ruido, sesgo² y varianza de un
grado; la estrella marca el menor total. Algunas barras salen del eje.
A la derecha, cada punto resume validación cruzada (*cross-validation*)
con cinco pliegues; el eje es logarítmico. Compara ambos mínimos y el
benchmark impreso. En $\mathrm{CV}_k$, $k$ cuenta pliegues: recuerda el aviso de letras.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

Con los valores iniciales, el menor total calculado está en grado 2;
la CV de una muestra elige 6. El ruido aporta 9.0.

La identidad de [Sesgo y varianza: de dónde sale el error](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-teo-sesgo-varianza)
suma $\sigma_\varepsilon^2(x)+\text{sesgo}(x)^2+\text{varianza}(x)$.
Duplicar $\sigma_\varepsilon$ cuadruplica el ruido y también aumenta la
varianza del ajuste. En mínimos cuadrados, con entradas fijas y ruido
centrado, no cambia el ajuste esperado; las barras estimadas sí fluctúan.

Más ruido tiende a favorecer grados menores; más datos, mayores.
Consulta el mínimo impreso de cada combinación. La estrella corresponde al
óptimo teórico, aproximado repitiendo muestras; el gorro corresponde a la
elección con datos. Una muestra puede discrepar del promedio.

</details>

### celda: bloque-3-predice

**Predice.** Al pasar de 30 a 960 entregas, ¿cuál baja más: el grado 1 o el 10?

Apuesta un número: cuánto esperas que baje el riesgo de la recta.
Puedes elegir el grado 1, el 10 o una caída parecida.
Compara «1 y 10» en «modelos»; después activa «panel del grado elegido».

### celda: bloque-3-mira

**Mira.** Los círculos muestran $L_{\text{ent}}$, pérdida promedio en entrenamiento;
las líneas crema, $R$ en el despliegue. Son medianas de 50 muestras por
tamaño. La punteada marca el piso cuadrático.
Abajo, cada cuadrado resume el grado elegido por CV: mediana de 20 muestras.
Los estilos distinguen grados.
La última línea impresa da el benchmark: la media de entrenamiento como punto de
comparación (la clase 3 lo define), evaluada en el despliegue.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Con los valores iniciales, baja más el grado 10, que empieza arriba de la
recta. Las medianas de $R$ del grado 1 son 14.7, 13.8 y 13.8 con
30, 480 y 960 entregas. Las del grado 10 son 9.1 y 9.0 con 480 y 960;
el piso es 9.0.

En general, más datos pueden reducir la varianza sin corregir una familia
inadecuada. [Ruido, sesgo y varianza](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-teo-sesgo-varianza)
da $E_{\mathcal D}[R(\widehat f)]=R_{\text{Bayes}}+E_x[\text{sesgo}(x)^2]+E_x[\text{varianza}(x)]$.
La identidad habla de medias; aquí miras medianas.

La recta conserva error de aproximación. La CV tiende a elegir más capacidad:
su mediana pasa de 3 a 10. En una repetición puede bajar.

</details>

### celda: bloque-4-predice

**Predice.** Proceso misterioso A: ¿sobreajuste, no aprende, subajuste o listo?

Apuesta un número: cuánto esperas reducir la CV al subir el grado.
Repite la pregunta para B, C y D en «proceso».
Sobreajuste (*overfitting*) y subajuste (*underfitting*) son dos diagnósticos posibles.
Antes de revelar el piso, usa las curvas y la comparación con el benchmark.

### celda: bloque-4-mira

**Mira.** Cada círculo mide entrenamiento; cada triángulo, CV por grado;
la raya-punto marca el benchmark. Lee las dos líneas: (a) decide la
comparación pareada en validación; (b) da una señal descriptiva de CV.
Activa «revelar el piso y R (solo en el simulador)»: `datos.despliegue`
es el visor de la realidad; solo existe en el simulador.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Con los valores iniciales, A muestra subajuste: CV $15.1\pm0.9$ frente a 9.7
con grado 8. B muestra sobreajuste: entrenamiento 5.7 frente a CV 262.2.
C no aprende: diferencia pareada $-0.1$ (EE 0.3). D está listo, con CV 9.7.

En general, bajar CV más de un EE es heurística. En (a), ambos modelos
están fijados; la validación no los eligió. Usa el EE de la diferencia
pareada de pérdidas para la regla de dos EE. En (b), A y D dan «señal»;
C, «falta evidencia»: las pérdidas fuera de pliegue dependen entre sí.

Al revelar, lee $R-R_{\text{Bayes}}$, incluso en D.
[Ruido, sesgo y varianza](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-teo-sesgo-varianza)
da $E_{\mathcal D}[R(\widehat f)]-R_{\text{Bayes}}=E_x[\text{sesgo}(x)^2]+E_x[\text{varianza}(x)]$.

</details>

### celda: taller-intro

**Taller.** Ejecuta el ejemplo activo. Después copia una alternativa comentada
y quita sus signos `#`; conserva la llamada final a
`ml.taller(datos, clase=2, que="descomponer")`.

Otra $f$ cambia la forma que intentas aprender. Más ruido cambia
`sigma_e`: observa el piso y la dispersión. Con $n=200$, explora qué grados
aprovechan más datos. Cambia una alternativa por vez; la última asignación
a `datos` determina el proceso.

Antes de ejecutar, predice qué componente cambiará. Compara las barras con
el caso inicial y explica si necesitas otra familia, más datos o mejores
variables.

### celda: galeria-intro

**Galería.** Los casos 13–16 son misterios: abre cada caso, lee su pregunta
y escribe tu diagnóstico antes de revelar «¿Qué se ve?».
Busca qué comparación sostiene tu respuesta y qué dato te haría cambiarla.

En el caso 13, el proceso y el modelo se eligieron para que la separación
al azar engañe. Con un modelo que no usa el tiempo, casi no engaña.
Toma el caso como un aviso para revisar cómo separas los datos.

### celda: ejercicio-tres-predicciones

**Ejercicio.** En un $x$ fijo, $f(x)=11$. Un procedimiento predice $8$, $10$ o $12$,
cada una con probabilidad $1/3$ según la muestra, y el ruido nuevo tiene varianza 4.
Calcula sesgo, varianza y error cuadrático esperado.

**Pista:** ¿Alrededor de qué número se mide la varianza: de $f(x)$ o del promedio de las predicciones?

### celda: ejercicio-tres-predicciones-respuesta

<details><summary>Explicación</summary>

El promedio es 10. El sesgo es $-1$: el procedimiento predice, en promedio,
por debajo de $f(x)=11$.
La varianza mide las desviaciones cuadráticas respecto de 10:

$$\frac{4+0+4}{3}=\frac83.$$

Por [Ruido, sesgo y varianza](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/sesgo-y-varianza/#raya-object-ml-c2-teo-sesgo-varianza),
el error cuadrático esperado es

$$4+1+\frac83=\frac{23}{3}.$$

El sesgo puede ser negativo; su contribución al error es su cuadrado.
El ruido nuevo se suma aunque el ajuste promedio acierte.

</details>

### celda: cierre

Repetir muestras separa desplazamiento y dispersión. Con 960 entregas,
la mediana del riesgo del grado 10 llega a 9.0; la recta conserva 13.8.
Más datos ayudan de manera distinta según la familia. Una curva aislada
no cuenta toda la historia.

¿Cómo bajo la varianza sin bajar el grado? (clase 3).
