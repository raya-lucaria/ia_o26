<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c2-guion-03
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_2 (sha256 a764ccaf)
Rama de origen: aprendizaje-maquina-clase-2@9a0d9c8f4c48a34dcdf28b19eb974fc0d4d4b24e
Archivo permitido: tools/cuadernos_ml/03_entrenamiento_y_prueba.texto.md
-->

### celda: portada

# Notebook 3 · Entrenamiento y prueba

Acompaña la página [Entrenamiento y prueba](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/entrenamiento-y-prueba/).

Duración del recorrido: ~40 min.

Ejecuta primero la celda de arranque y sigue el orden del notebook.
Antes de cada «Juega», escribe tu apuesta. Después mueve los controles,
lee la gráfica y abre «Explicación».

### celda: idea

Con entrenamiento ajustas los parámetros $\beta$ para cada grado $N$; con validación eliges ese hiperparámetro.
[Entrenamiento y prueba](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/separar-los-datos/entrenamiento-y-prueba/) separa las decisiones:

$$\widehat N\in\operatorname*{arg\,min}_{N\in\{0,\dots,N_{\max}\}}L_{\text{val}}\bigl(\widehat\beta(N)\bigr),\qquad \widehat\beta(N)\in\operatorname*{arg\,min}_{\beta}\ L_{\text{ent}}(\beta)\ \ \text{s.a.}\ \ \text{grado}\le N.$$

Con empate, el más simple: el menor $N$; si $\Phi$ no tiene rango completo, los coeficientes de norma mínima.
La prueba estima el riesgo del elegido cuando ya no decides con ella.

Aquí $L$ es pérdida promedio, no lenguaje, clase de complejidad ni longitud de racha.
Usamos pérdida cuadrática, en minutos².
El *benchmark* es «la media de entrenamiento como punto de comparación; la clase 3 lo define».

### celda: bloque-1-predice

**Predice.** Si eliges el grado entre 0 y 12 con el menor $L_{\text{ent}}$, ¿qué grado sale? Apuesta un número.

Puedes apostar por el grado inicial, uno intermedio o el máximo.
Deja «entregas n» y «semilla» como están; recorre «grado N» y después activa «mostrar la realidad R».

### celda: bloque-1-mira

**Mira.** Los círculos de la derecha miden $L_{\text{ent}}$; $N=0$ es el benchmark en entrenamiento.
Al activar «mostrar la realidad R», compara la curva crema con la raya-punto del benchmark.

cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Con los valores iniciales, el menor $L_{\text{ent}}$ corresponde al grado 12.
En general, las familias anidadas permiten conservar el ajuste anterior: el mínimo de entrenamiento no sube al aumentar el grado.
Eso no garantiza menor riesgo $R$.

Como recuerda «Entrenamiento y prueba», $\phi_N(x)=(1,x,\dots,x^N)$ añade columnas a $\Phi$.
Un polinomio de grado 12 sigue siendo lineal en $\beta$.
Cambiar «grado N» cambia la familia; ajustar sus parámetros no decide qué familia generaliza mejor.

La curva crema estima $R$ en la realidad; su benchmark se evalúa en esa misma muestra.
Esa comparación solo existe en el simulador. El hiperparámetro necesita otros datos.

</details>

### celda: bloque-2-predice

**Predice.** Con el modelo congelado y 20 entregas de prueba, ¿cuánto crees que se aleja $L_{\text{prueba}}$ de $R$ en una prueba típica: 1, 5 o 20 minutos²?

Apuesta un número antes de cambiar «n_prueba». Después compara el ancho del histograma y activa «mostrar intervalos ±2 EE».

### celda: bloque-2-mira

**Mira.** Cada barra cuenta pruebas nuevas con errores promedio parecidos; la línea vertical marca $R$.
El visor de la realidad, `datos.despliegue`, solo existe en el simulador: de ahí salen estas pruebas nuevas.
Debajo aparece el benchmark en el despliegue. Activa «mostrar intervalos ±2 EE» para leer la cobertura.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

Con los valores iniciales, $R=11.78$ en el despliegue; las 500 estimaciones tienen desviación 3.81 minutos².
La apuesta 5 es la más cercana. Los intervalos cubren $R$ en 89 % de las pruebas.
Compara con la media de entrenamiento evaluada en el despliegue, impresa debajo del histograma.

En «Entrenamiento y prueba», el ancho baja como $1/\sqrt{n_{\text{prueba}}}$ para pérdidas independientes con varianza finita.
Con 200 entregas, la desviación es 1.10 y la cobertura, 96 %.
Insesgada significa correcta en promedio, no exacta en cada muestra.
$L_{\text{prueba}}\pm2\,\mathrm{EE}$ es un intervalo aproximado; EE significa error estándar del promedio, no de una predicción individual.

</details>

### celda: bloque-3-predice

**Predice.** Si eliges el grado con la prueba y anuncias ese error, ¿anuncias más, igual o menos que el error real del elegido, en promedio?

Elige una opción y apuesta un número para «anunciado − real».
Después cambia «elegir con» y «candidatos M». $M$ cuenta candidatos, como en la unidad 6; no es el índice de pliegue.

### celda: bloque-3-mira

**Mira.** Las barras cuentan repeticiones según $L_{\text{prueba}}-R$ del elegido: a la izquierda de cero anuncias de menos.
En ambos modos se anuncia la prueba; cambia el conjunto que elige al ganador.
El título recuerda «sin reajuste». Compara la media con su EE de Monte Carlo, la mediana y el porcentaje optimista.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Con los valores iniciales, elegir con la prueba da una media de −7.53 ± 1.77 minutos²; 74 % anuncia de menos.
El ± corresponde al EE de Monte Carlo.
Con validación, la mediana es −0.65 y 56 % anuncia de menos; unas pocas repeticiones extremas arrastran la media.

«Entrenamiento y prueba» distingue elegir de anunciar:
$E[L_{\text{val}}]\le E[R]=E[L_{\text{prueba}}]$ para el elegido con validación y una prueba independiente del procedimiento, de la misma población.
Elegir el mínimo favorece estimaciones afortunadas.
Con $M=1$ no hay selección entre candidatos; la media simulada puede diferir de cero.
Más candidatos pueden agravar el optimismo, sin garantizar monotonía en esta tabla.

</details>

### celda: bloque-4-predice

**Predice.** En «el mes que viene», ¿la prueba al azar promete menos, igual o más error del que darás en el futuro?

Elige una opción y apuesta un número para $L_{\text{prueba}}-R$.
Selecciona «el mes que viene» en «contrato»; compara «al azar» y «como el contrato» en «cómo separar».

### celda: bloque-4-mira

**Mira.** El cuadrado rosa mide $L_{\text{prueba}}$; la línea crema, $R$ en el despliegue de cada contrato.
La raya-punto es la media de entrenamiento evaluada en ese despliegue.
El eje es logarítmico. Para «más de lo mismo», usa «al azar»: es la separación que imita ese contrato.
No tiene una separación alternativa «como el contrato».

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Con los valores iniciales, «más de lo mismo» deja $R$ dentro de $L_{\text{prueba}}\pm2\,\mathrm{EE}$.
Compara también el benchmark impreso: la media de entrenamiento evaluada en el despliegue de ese contrato.

En «Entrenamiento y prueba», la prueba debe imitar el uso previsto.
En «el mes que viene», al azar promete menos: este modelo aprovecha vecinos temporales; sin usar tiempo casi no miente.
Separar temporalmente acerca la estimación, sin igualarla: $L_{\text{prueba}}=119.4$ frente a $R=155.6$ en el despliegue.
Justo después de la muestra puede salir menor.

Con pacientes nuevos, compartir pacientes entre conjuntos promete de menos.
Para otra ciudad, ninguna separación de esta muestra reproduce el despliegue: declara el alcance.

</details>

### celda: bloque-5-predice

**Predice.** Si mandas 50 % de las entregas a prueba, ¿qué empeora: el modelo, la medición o los dos?

Elige una opción y apuesta un número para $R$.
Sube «fracción de prueba»; después repite con otro «n total».
Compara por separado el riesgo del modelo y la dispersión de la medición.

### celda: bloque-5-mira

**Mira.** La curva superior muestra el $R$ medio del modelo; la inferior, la dispersión de $L_{\text{prueba}}-R$ entre repeticiones.
Cada punto corresponde a una fracción de prueba. La marca vertical señala la fracción elegida.
Abajo se mide cuánto se equivoca la prueba sobre su propio modelo, cuyo riesgo también cambia.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

Con $n=60$ y 20 % para prueba, el riesgo medio en el despliegue es 10.40 minutos².
La desviación de $L_{\text{prueba}}-R$ es 4.58 minutos².
Debajo se imprime el benchmark de una muestra: su media de entrenamiento evaluada en el despliegue.

En general, reservar más para prueba deja menos para ajustar: tiende a empeorar el modelo y mejorar la medición.
«Entrenamiento y prueba» explica la escala $1/\sqrt{n_{\text{prueba}}}$ para el error estándar, con un modelo fijo y pérdidas independientes de varianza finita.
Aquí también cambia el modelo: no esperes esa escala exacta.

Importa el tamaño absoluto; con más datos puede bastar una fracción menor.
Entre fracciones vecinas puede haber oscilaciones de Monte Carlo.

</details>

### celda: taller-intro

**Taller.** Ejecuta el ejemplo activo. Después prueba una alternativa comentada: otra $f$ cambia la forma de las entregas; el futuro cambia el contrato; pocos datos reducen la muestra.
Quita el comentario de todas las líneas de una sola alternativa, incluida su continuación.
Conserva `ml.taller(datos, clase=2, que="elegir")`; la última asignación a `datos` manda.

El taller usa validación cruzada (*cross-validation*) para elegir $N$, con las reglas del mínimo y de un EE, y después reajusta.
Identifica qué conjunto produjo cada cifra: prueba con su intervalo $\pm2\,\mathrm{EE}$, benchmark y riesgo en el despliegue.
Compara las reglas antes de abrir la prueba; no uses su resultado para volver a elegir.

Con los datos iniciales, el modelo final pierde frente al benchmark: el taller imprime $L_{\text{prueba}}=112.55\pm146.96$ contra 82.26 del benchmark, con diferencia pareada +30.3.
La prueba tiene solo 12 entregas y una del borde domina el promedio; esto indica que la prueba es imprecisa y no contradice la elección.
El taller imprime la línea de prueba en cada corrida: compara las reglas en la tabla de CV, decide y lee la prueba una sola vez, al final.

### celda: galeria-intro

**Galería.** Recorre los casos 13–16 como misterios.
En el 13, compara $L_{\text{prueba}}$ con $R$: el polinomio usa solo la distancia, sin tiempo, y la prueba al azar casi no engaña.
Contrasta lo que ves con la explicación: la página muestra el engaño con vecinos en distancia y tiempo.
En el 14, busca qué cambia al recibir pacientes nuevos.
En el 15, identifica qué queda fuera del alcance de la muestra al cambiar de ciudad.
En el 16, busca en qué pliegues distintos caen las dos entregas lejanas y cuánto sube el error de cada uno.

Lee cada pregunta y escribe una explicación antes de abrir «¿Qué se ve?».
Después contrasta tu explicación con la del caso: identifica qué comparación permitió resolver el misterio.

### celda: ejercicio-optimismo-m

**Ejercicio.** ¿Con cuántos candidatos el anuncio medio queda más de 2 minutos² por debajo del riesgo del elegido?

En el bloque 3, selecciona «elegir con la prueba» y busca el primer $M$ cuya media «anunciado − real» sea menor que −2.
Anota también la media del número anterior de candidatos.

**Pista:** ¿buscas una mediana, un porcentaje o la media con su signo?

### celda: ejercicio-optimismo-m-respuesta

<details><summary>Explicación</summary>

En este experimento, el primer cruce ocurre con $M=7$: la media es −2.46 minutos².
Con $M=6$ era −1.44 minutos², todavía por encima de −2.
Los candidatos son los grados de $0$ a $M-1$.

El signo negativo indica que anuncias menos error del que tiene el elegido en el despliegue.
El cruce pertenece a estas 300 repeticiones; no es un umbral universal.
La tabla tampoco baja en cada paso: pasa de −7.42 con $M=11$ a −7.12 con $M=12$.

</details>

### celda: cierre

Entrenamiento ajusta; validación elige; una prueba independiente del procedimiento estima el riesgo cuando imita el despliegue.
El error de prueba puede bailar aunque congeles el modelo.
Si lo usas para elegir, deja de ser una evaluación reservada.

¿Y si una sola validación decide por suerte?
