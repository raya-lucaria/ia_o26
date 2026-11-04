<!--

Tipo: guion_notebook_clase
Etiqueta: codex-red-c3-nb07
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_3 (sha256 5b6a9181)
Rama de origen: aprendizaje-maquina-clase-3@74d2d1b
Archivo permitido: tools/cuadernos_ml/07_el_lagrangeano_en_accion.texto.md

## Decisiones del registro que aplican

- D-005: se aplica la lista negra del linter de notación.
- D-008: «Ningún plan, página, notebook, tarea ni objeto oficial lleva fechas de clase o de entrega». Recorrido autónomo completo.
- D-009.1: se traduce a la notación del curso. D-009.5: sin cifras de corrida en la prosa; solo cuentas del brief.
- D-009.9: «En los pasos iterativos de la receta de metodología (DL cap. 11) se usa validación, no prueba».
- D-012: ejecución autorizada; sin fusión ni push.
- D-013c-c3 y D-013c-c2: API, nombres, referencias e hipótesis ratificados según el brief.
- D-015: «Se aceptan las filas aditivas con “Se presenta en”».

Se aplica la anatomía de notebook: portada, idea, seis bloques, taller,
galería, ejercicios con respuesta y cierre. Las claves siguientes reproducen
las de texto del código, en orden. El título de nivel uno vive solo en
portada; dentro de una celda no hay encabezados de nivel tres. El generador
escribe el badge y el arranque. Este guion no lleva frontmatter ni directivas Raya.
-->

### celda: portada

# Notebook 7 · El lagrangeano en acción

Acompaña la página [El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/). Duración: ~28 min.

Ejecuta primero el arranque y sigue de arriba abajo. En cada bloque, anota
tu predicción, ejecuta «Juega», mueve los controles y abre «Explicación».
Puedes hacer el recorrido solo en casa.

### celda: idea

Puedes limitar los coeficientes con un presupuesto o cobrar por su tamaño.
El lagrangeano conecta ambas formas:
$\mathcal L(\beta,\mu)=L_{\text{ent}}(\beta)+\mu\,\bigl(\Omega(\beta)-d\bigr),\ \mu\ge0$.
Aquí $L_{\text{ent}}$ es la pérdida cuadrática promedio, $\Omega$ mide capacidad
y $d$ es su presupuesto. Con $\mu$ fijo, minimizarlo equivale a minimizar
$L_{\text{ent}}(\beta)+\mu\Omega(\beta)$: el término $-\mu d$ no depende de $\beta$.
Con $\mu=0$ recuperas el ajuste sin penalizar.

Como explica [El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/),
$\mu$ es el multiplicador de KKT, no una distribución de Markov.
$\Omega$ mide capacidad, no una cota asintótica; $L$ mide pérdida, no un lenguaje.
Ridge, lasso y red elástica (*elastic net*) penalizan las pendientes; dejan libre el intercepto $\beta_0$.

### celda: bloque-1-predice

**Predice.** Si achicas el presupuesto $d$ a la mitad, ¿en cuál región queda $\widehat\beta_1$ exactamente en 0: en el disco, en el diamante o en ninguna?

Elige una opción. En «presupuesto d, como fracción de Ω sin penalizar», pasa
de 1 a 0.5. Compara disco y diamante con «región Ω ≤ d».
Activa «mostrar μ» y «ver la curva del presupuesto: mejor L_ent contra d».

### celda: bloque-1-mira

**Mira.** Los ejes son las pendientes; las elipses tienen igual $L_{\text{ent}}$ y su centro es el ajuste sin penalizar.
Busca el punto óptimo dentro de la región; debajo aparecen $d$, $\widehat\beta$ y $\mu$.
A la derecha, cada punto de la curva es el mejor error permitido por un presupuesto; la recta toca el presupuesto elegido.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

En el diamante. Para estos datos, la elipse toca una esquina sobre el eje:
$\widehat\beta_1=0$. El disco tiene borde suave y aquí conserva ambas pendientes.
La equivalencia restringido–penalizado de
[El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/)
vale para estas tres penalizaciones con $d>0$.

Cuando la fracción llega a 1, el presupuesto admite el ajuste sin penalizar
y $\mu=0$. Es la holgura complementaria: no pagas por relajar una restricción
que ya no limita el ajuste.
En la curva $v(d)$, el mejor $L_{\text{ent}}$ permitido, la recta de apoyo tiene pendiente $-\mu$.
Ese precio mide cuánto puede bajar el error al ampliar el presupuesto.

</details>

### celda: bloque-2-predice

**Predice.** Con $\mu=1$, ¿sobrevive a lasso un coeficiente cuya pendiente sin penalizar es 0.4?

Anota «sigue distinto de cero» o «se anula». Pon «b: pendiente sin penalizar»
en 0.4, «μ» en 1 y «penalización» en «lasso».
Después compara con «ridge» usando los mismos valores.

### celda: bloque-2-mira

**Mira.** El eje horizontal muestra $b$; el vertical, la pendiente ajustada. El punto negro marca tu elección.
Busca la zona plana de lasso entre $-\mu/2$ y $\mu/2$, y compárala con la recta de ridge.
Debajo, `encoger_1d` da la cuenta y `ajustar` la comprueba con datos cuya pendiente sin penalizar es exactamente $b$.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

No sobrevive: $0.4\le\mu/2=0.5$, así que lasso devuelve cero.
El umbral suave de [El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/)
resta $\mu/2$ a la magnitud de $b$, sin atravesar cero.
Ridge divide entre $1+\mu$: aquí deja $0.4/(1+1)=0.2$.
Con una variable estandarizada, lasso anula un intervalo entero; ridge solo da cero cuando $b=0$.

</details>

### celda: bloque-3-predice

**Predice.** En la clase 2, el grado 12 sobre las entregas sobreajustaba. Si dejas el grado en 12 y subes $\mu$ desde casi 0 hasta 100, ¿la curva pasa por una forma parecida a $f$ antes de aplanarse?

Anota sí o no. Conserva «semilla» en 0 y recorre «log₁₀ μ» de izquierda a derecha.
En «qué ver», compara «el ajuste», «las tres vistas en validación» y «la U contra μ».
La U se calcula la primera vez que la pides para cada semilla.

Si exploras «semilla», cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

### celda: bloque-3-mira

**Mira.** En «el ajuste», los puntos son entregas y las curvas son $f$ y el ajuste; sigue sus oscilaciones al mover $\mu$.
En las tres vistas, cada punto es una entrega de validación: el centro residual casi no se mueve; con $\mu$ grande aparece forma en $e$ contra $x$.
En la U, los círculos son $L_{\text{ent}}$, los triángulos son $\mathrm{CV}_5$ y la línea crema es $R$; ubica «tú».

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Sí. La curva pasa por una forma cercana a $f$ antes de aplanarse.
Sigue siendo de grado 12, curva en $x$ y lineal en $\beta$.
Cambias su capacidad al penalizar las pendientes.
Cuando $\mu\to\infty$, queda la media de entrenamiento: el punto de comparación (*benchmark*),
como explica [El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/).

La validación cruzada (*cross-validation*) usa $k=5$ pliegues; aquí $k$ cuenta
pliegues, no clases. Sus triángulos muestran la U contra $\mu$.
El riesgo es enorme con $\mu$ chica y sube con $\mu$ grande; no sigue una U limpia en medio.
El $R$ impreso aproxima la pérdida esperada con una muestra enorme;
esa información no está disponible para elegir en un problema real.

El intercepto libre mantiene el centro residual cerca de cero; ese centro
no mide el sesgo de una predicción. Con solo 12 filas de validación, el ancho salta.
Una penalización grande deja estructura sin seguir: aparece forma en los residuales.

`polinomio(12, escalar=True)` lleva $x$ a $[-1,1]$ antes de elevar;
`estandarizar` transforma las columnas después.
Estandarizar potencias de valores alejados de cero no elimina su correlación.
Con distribución simétrica, las potencias pares e impares no se correlacionan; centrar sin simetría no basta.

</details>

### celda: bloque-4-predice

**Predice.** Al subir $\mu$ en lasso, ¿las 5 variables útiles son siempre las últimas en volverse cero?

Elige «siempre» o «una espuria puede sobrevivir a una útil».
Pon «penalización» en «lasso» y lee las trayectorias de izquierda a derecha: $\mu$ aumenta en el eje.
Activa «una útil con una gemela casi idéntica» y compara con «red elástica».
Explora «ρ (solo red elástica)», que controla la mezcla de penalizaciones.

Con «semilla», cambia la semilla: la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

### celda: bloque-4-mira

**Mira.** Cada línea sigue una pendiente al aumentar $\mu$; busca dónde llega a cero y si permanece allí.
Las útiles están en color; las espurias, en gris, salvo la gemela `x6`, también resaltada cuando activas el interruptor.
Compara `x1` y `x6`; el conteo inferior resume su conservación en muestras distintas, no puntos de una trayectoria.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

No siempre. Una útil débil puede apagarse antes que una espuria favorecida por la muestra.
En estos datos, con la gemela, suele conservar `x1` y a veces `x6`;
la red elástica tiende a conservar ambas.

> [!WARNING]
> Lectura equivocada: «Lasso encuentra las variables verdaderas».
>
> Lectura correcta: **Conservar una variable no certifica que genere la señal.**

El conteo usa 100 réplicas con $\mu=0.3$; la primera vez tarda unos segundos.
La correlación entre la útil y su gemela es 0.95, no identidad:
la elección puede cambiar entre muestras aunque cada ajuste tenga un mínimo único.
Con columnas idénticas, lasso puede tener varios mínimos; el algoritmo muestra uno.

Es la distinción sobre variables correlacionadas de
[El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/).
Ridge aquí no apaga variables. En general puede cruzar cero por cancelación en un valor aislado de $\mu$.
Eso difiere de permanecer en cero en un intervalo, como lasso.

</details>

### celda: bloque-5-predice

**Predice.** Si dejas que $L_{\text{ent}}$ elija $\mu$ entre $10^{-4}$ y $10^{3}$, ¿cuál elige?

Elige la menor, una intermedia o la mayor. Pon «elige con» en «L_ent»
y «regla» en «el mínimo»; compara ambas opciones de «penalización».
Después usa «CV con k = 5» y «un EE», un error estándar.
La primera selección con CV y lasso tarda unos segundos.

La regla de un EE solo funciona con CV; con «L_ent» o «L_val» se usa el mínimo.
El orden se declara antes de medir: $\mu$ de mayor a menor, de simple a complejo.

### celda: bloque-5-mira

**Mira.** Los círculos son $L_{\text{ent}}$; con CV, los triángulos son medias con barras de EE; la línea crema es $R$.
Recorre $\mu$ de mayor a menor: busca la primera media bajo «mínimo + 1 EE»; los números cuentan pendientes distintas de cero.
La prueba está en una celda aparte que no cambia con los controles: si cambiara con ellos, elegirías con la prueba.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

Elige la menor, $10^{-4}$, en esta rejilla.
El teorema de monotonía de [El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/)
dice que $L_{\text{ent}}$ no disminuye al aumentar $\mu$.
Por eso eliges el hiperparámetro con datos reservados o CV.
Estas curvas miden pérdidas; no suman $\mu\Omega$.

Con CV, un EE prefiere la mayor $\mu$ cuya media no excede el umbral.
Usa el triángulo, no el extremo de su barra.
Con «L_val» ves triángulos sin barras; allí no se aplica esa regla.
Cada pliegue estima su propia estandarización.

La celda de prueba fija lasso, CV₅ y un EE antes de abrir la reserva.
Evalúa `modelo_final`, reajustado con entrenamiento y validación, e imprime
$L_{\text{prueba}}\pm2\,\mathrm{EE}$ y el benchmark de la media.
La diferencia pareada resta sus pérdidas sobre las mismas observaciones; trae su propio EE.
Ese contraste evalúa el procedimiento fijado, sin volver a elegir con su resultado.

</details>

### celda: bloque-6-predice

**Predice.** Con la misma $\mu$ de lasso, si mides $x_2$ en metros en lugar de kilómetros, ¿$x_2$ se apaga antes o después?

Elige antes, después o igual. Apaga «estandarizar con entrenamiento» y
compara «× 1» con «× 1000» en «x2 multiplicada por».
Conserva «log₁₀ μ» y «y multiplicada por (caso 24)» en sus valores iniciales.
Después activa la estandarización; finalmente prueba multiplicar $y$.

### celda: bloque-6-mira

**Mira.** Cada línea sigue una pendiente; la marca vertical señala tu $\mu$ y debajo aparecen $\widehat\beta$ y las columnas de $\Phi$.
Sin estandarizar, `x2` multiplicada por 1000 persiste más; con estandarización, cambiar sus unidades deja las trayectorias iguales.
Con $y$ multiplicada por 1000, las pendientes persisten más; pueden seguir distintas de cero en todo el intervalo mostrado.

### celda: bloque-6-explica

<details><summary>Explicación</summary>

Después. Al multiplicar la columna por 1000, el mismo efecto necesita un
coeficiente dividido entre 1000. Lasso cobra también mil veces menos por ese efecto.
Estandarizar con entrenamiento evita ese trato desigual por unidades.
Es la observación sobre estandarización de
[El lagrangeano en acción](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/el-lagrangeano-en-accion/).

Sin penalizar y con $\Phi$ de rango completo, cambiar unidades no cambia
las predicciones. Con rango deficiente, solo se garantizan las de entrenamiento.

Multiplicar $y$ por 1000 cambia la escala del objetivo.
Para conservar el encogimiento relativo, lasso necesita $1000\mu$; ridge conserva la misma $\mu$.
La galería muestra esta diferencia con muchas variables en el caso 24.

</details>

### celda: taller-intro

**Taller.** Ejecuta el ejemplo y cambia una alternativa comentada: penalización,
variables correlacionadas o unidades. Al copiar un proceso, quita los signos
de comentario y deja `ml.taller(datos, clase=3, que="lagrangeano", ...)` al final.
La última asignación a `datos` es la que usa el taller.

Compara las trayectorias, la elección por CV₅ y los coeficientes frente a
`beta_verdadero`. El orden de simplicidad es $\mu$ de mayor a menor.
Las diferencias contra la media usan los mismos pliegues y son descriptivas;
«señal» no es una confirmación con datos nuevos.
Conserva esta lectura: «elegiste con esta misma CV: la señal es optimista; se confirma en una reserva».

El riesgo del elegido y del benchmark revela lo que sabe la muestra enorme.
La prueba permanece cerrada. Validación ya participó en el reajuste final:
su error no sería una evaluación independiente.

### celda: galeria-intro

**Galería.** Recorre los casos 9, 10, 23 y 24 con el análisis «lagrangeano».
Antes de abrir cada explicación, anota qué cambia al penalizar.
En el 9 observa ridge; en el 23, la estabilización con $\mu$;
en el 24, el cambio de escala de $y$ y cuántas variables sobreviven.

### celda: ejercicio-cero-a-mano

**Ejercicio.** Para $b=(3,0.4)$ y $\mu=1$, calcula las pendientes de lasso y ridge
aplicando a cada coordenada la cuenta de una variable estandarizada.
Comprueba con `encoger_1d` en una línea, o usa cada valor de $b$ en el bloque 2.

**Pista:** ¿cuál regla resta un umbral y cuál divide la pendiente?

### celda: ejercicio-cero-a-mano-respuesta

<details><summary>Respuesta</summary>

Lasso resta $\mu/2=0.5$ a cada magnitud sin atravesar cero: queda $(2.5,0)$.
Ridge divide entre $1+\mu=2$: queda $(1.5,0.2)$.
Puedes comprobar ambas cuentas con esta línea:

```python
[[ml.encoger_1d(b, 1, p) for b in (3, 0.4)] for p in ("l1", "l2")]
```

</details>

### celda: ejercicio-grupo

**Ejercicio de papel.** Resuelve sin ajustar nada.

(a) Escribe el lagrangeano de una penalización que solo castiga a las 45 espurias, no a las 5 útiles.

(b) Alguien propone hacerlo con `ajustar` multiplicando por 1000 las columnas estandarizadas de las útiles.
Escribe cuánto paga entonces cada útil por unidad de su efecto.
¿Con cualquier factor finito, por grande que sea, queda sin castigo?

**Pista:** ¿qué coeficiente mantiene el mismo efecto cuando multiplicas la columna?

### celda: ejercicio-grupo-respuesta

<details><summary>Respuesta</summary>

(a) Restringes solo las pendientes de las espurias:

$$
\min_\beta L_{\text{ent}}(\beta)
\quad\text{sujeto a}\quad
\sum_{j\in\text{espurias}}\lvert\beta_j\rvert\le d.
$$

Su lagrangeano es

$$
\mathcal L(\beta,\mu)=L_{\text{ent}}(\beta)
+\mu\left(\sum_{j\in\text{espurias}}\lvert\beta_j\rvert-d\right),
\quad\mu\ge0.
$$

(b) Con la columna $1000\,\widetilde x_j$, el mismo efecto requiere
$\beta_j/1000$. Paga $\mu\lvert\beta_j\rvert/1000$:
por unidad de efecto, $\mu/1000$.
Con $\mu>0$, ningún factor finito elimina el castigo.
Quitarlo exige pesos de penalización por coordenada, que `ajustar` no ofrece.

</details>

### celda: cierre

El lagrangeano reúne error y presupuesto:
$\mathcal L(\beta,\mu)=L_{\text{ent}}(\beta)+\mu(\Omega(\beta)-d)$.
Ya puedes leer cuándo una pendiente encoge, se anula o comparte señal con otra.
Puedes elegir $\mu$ con CV, cuidar las unidades y reservar la prueba para evaluar el procedimiento fijado.
La pregunta que abre la clase 4 es: ¿y si $y$ es una clase?
