<!--
Tipo: guion_notebook_clase
Etiqueta: codex-red-c3-nb06
Contrato: v5.1 · API ml_lab: 1.3 · Protocolo: p5.2
Plan: clase_3 (sha256 5b6a9181)
Rama de origen: aprendizaje-maquina-clase-3@74d2d1b
Archivo permitido: tools/cuadernos_ml/06_leer_el_error.texto.md

Decisiones del registro que aplican
D-005: lista negra de notación; vocabulario y símbolos del curso.
D-008: sin fechas ni plazos; recorrido autónomo con controles identificados.
D-009.1: notación traducida a la del curso.
D-009.5: sin cifras de corridas en la prosa; cuentas y parámetros del brief.
D-012: ejecución autorizada en el worktree; sin commit, fusión ni push.
D-013c-c3: API del lote de clase 3 ratificada; se respetan sus nombres.
D-013c-c2: no se necesitan referencias a sus dos objetos en este guion.
D-015: notación aditiva de clase 3 según la regla por omisión.

Anatomía: portada e idea; cinco bloques Predice → Juega → Mira → Explica;
taller, galería, dos ejercicios con respuesta y cierre. Las claves de código
pertenecen al .py. Solo portada lleva título de nivel 1; dentro de las celdas
no hay encabezados de nivel 3. El badge y el arranque los pone el generador.
-->

### celda: portada

# Notebook 6 · Leer el error

Acompaña la página [Leer el error](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/leer-el-error/). Duración: ~25 min.

Ejecuta primero la celda de arranque y recorre el notebook de arriba abajo.
Antes de correr cada «Juega», anota tu predicción. Mueve el control indicado,
lee la gráfica y después abre «Explicación».

### celda: idea

Lee el error antes de cambiar el modelo: su centro, ancho y forma cuentan
cosas distintas. El residual es $e_i=y_i-\widehat y_i$; $\bar e_{\mathcal D}$
es su promedio en un conjunto $\mathcal D$ de tamaño $n_{\mathcal D}$.
La identidad «Centro y ancho» de
[Leer el error](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/leer-el-error/leer-el-error/)
separa la pérdida cuadrática promedio en centro al cuadrado y dispersión:

$$
L_{\mathcal D}=\bar e_{\mathcal D}^{\,2}+\frac1{n_{\mathcal D}}\sum_{i\in\mathcal D}(e_i-\bar e_{\mathcal D})^2.
$$

### celda: bloque-1-predice

**Predice.** Con el modelo correcto, si duplicas el ruido $\sigma_\varepsilon$, ¿el histograma de residuales de validación se corre de lugar o solo se ensancha?

Elige: cambia el centro, cambia el ancho o cambian ambos sistemáticamente.
Deja «modelo» en «recta (el correcto)» y «dónde se leen» en «validación».
En «ruido σ_ε», pasa de 1 a 2 sin mover «semilla».

### celda: bloque-1-mira

**Mira.** Cada punto del primer panel compara predicción y observación; la diagonal indica igualdad. El histograma central cuenta residuales por intervalo.
Compara su ancho y el centro impreso; en el tercer panel, cada punto ubica un residual frente a $x_1$.
En el histograma, la línea punteada marca el 0, la continua el centro $\bar e$ y la banda sombreada va de una desviación por debajo a una por encima del centro.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Se ensancha; en promedio, el centro no se desplaza. En una muestra de
validación sí puede moverse un poco. «Centro y ancho» separa ambos efectos;
«El centro no es el sesgo» de Leer el error distingue ese promedio del sesgo
de una predicción.

Si después mueves el control «semilla», la población y $f$ se quedan; cambian los datos, el ajuste y, con él, su riesgo $R(\widehat\beta)$.

Prueba «recta a una curva»: la curvatura omitida aparece como U en el tercer
panel. El intercepto compensa su promedio, pero no elimina la forma.
Con esa familia equivocada, el centro de validación puede variar incluso sin
ruido. Con el modelo correcto y sin ruido, la recta recupera $f$.

Al elegir «entrenamiento», el centro es cero, salvo precisión numérica:
la ecuación del intercepto obliga a que los residuales sumen cero.
Debajo se imprimen $L$ y el centro del conjunto elegido.
La media de entrenamiento es el punto de comparación (*benchmark*);
$R$ aproxima el riesgo cuadrático en el despliegue.

</details>

### celda: bloque-2-predice

**Predice.** Si a todas las $y$ les sumas 1000, ¿cambia la mejora del modelo sobre el benchmark de la media?

Anota si aumenta, disminuye o queda igual. En «nivel: se suma a y», compara
0 con 1000, sin cambiar «fuerza de la señal».
Después fija la señal en 0.25 y activa
«dividir el RMSE entre el nivel ȳ (y no entre la dispersión de y)».

### celda: bloque-2-mira

**Mira.** Cada barra horizontal muestra RMSE o MAE: compara modelo, media y mediana en validación con el piso poblacional correspondiente.
Con nivel 1000 y señal 0.25, contrasta el cociente impreso con la cercanía entre las barras del modelo y la media.
Al apagar el interruptor, el denominador es la desviación de $y$ en entrenamiento; debajo aparece la diferencia pareada con su EE.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

La mejora queda igual. El intercepto absorbe la suma: observaciones,
predicciones y media se trasladan juntas. Se conservan sus errores.
Aquí ajustas sin penalizar y con $\Phi$ de rango completo.
Dividir el RMSE entre el nivel puede hacerlo parecer pequeño sin mejorar
ninguna predicción. Dividir entre la dispersión compara escalas pertinentes.

«Benchmark» en Leer el error compara pérdidas por observación sobre las
mismas filas. La diferencia es modelo menos media: un valor negativo favorece
al modelo. Su error estándar, EE, mide la incertidumbre de ese promedio.
La celda informa si queda por debajo de cero por más de 2 EE.

Aquí validación sirve porque no eligió nada: ambos modelos se fijaron con
entrenamiento. Si eliges la señal o el modelo mirando esos resultados,
necesitas otra reserva para confirmar la mejora.
«La validación cruzada no es una reserva» impide trasladar ese EE a la
validación cruzada (*cross-validation*).

Con señal débil, la mejora sobre la media puede ser pequeña y el modelo
estar cerca del piso. «El piso: error de Bayes» explica ese límite poblacional
para la pérdida elegida. Una barra muestral puede quedar a cualquiera de
sus lados.

</details>

### celda: bloque-3-predice

**Predice.** Con ruido de Pareto de exponente 1.5, si pasas de 100 a 10 000 observaciones de validación, ¿el MSE se estabiliza como con ruido normal?

Elige: se estabiliza o sigue dando saltos. Deja «dónde vive la cola» en
«en el ruido» y «qué se promedia» en «cuadrados (MSE)».
Compara «Pareto, exponente 1.5» con «normal» en «ruido».
Recorre el eje horizontal desde 100 hasta 10 000; no hay deslizador de tamaño.

La curva de la izquierda promedia el ruido de cada observación: es lo que
darían los residuales de validación de un modelo que acertara $f$ exactamente.

### celda: bloque-3-mira

**Mira.** A la izquierda, cada línea promedia ruido al cuadrado, o absoluto, para una semilla; compara las 20 trayectorias hacia la derecha.
A la derecha, las curvas acumulan fracciones del MSE y MAE de validación; ubica cuánto aporta el 1 % de filas con mayor error absoluto.
La tabla muestra los cinco peores errores de validación; con «en x (ruido normal)», cada punto izquierdo es un residual frente a $x$.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

No se estabiliza en un valor finito. Pareto de exponente 1.5 tiene segundo
momento infinito: los extremos provocan saltos del promedio cuadrático.
El piso cuadrático es infinito. «Colas largas» en Leer el error explica
por qué una muestra finita siempre entrega una cifra, aunque no haya un
riesgo finito que estimar.

Cambia «qué se promedia» a «valores absolutos (MAE)»: Pareto 1.5 tiene
primer momento absoluto finito y ese promedio sí converge.
Con «Cauchy», también el piso absoluto es infinito.
Un extremo de esta cola no es un outlier: pertenece al fenómeno.

Con «en x (ruido normal)», también cambia el proceso: $x$ es lognormal y
$f=2+e^{x/3}$, pero sigues ajustando una recta. Conservas tamaño y semilla.
Los errores grandes se concentran donde $x$ es raro y la recta extrapola
mal la curva. Con cola en el ruido pueden aparecer en cualquier $x$.

</details>

### celda: bloque-4-predice

**Predice.** Si el modelo no ve $x_2$, y $\operatorname{corr}(x_1,x_2)=0.3$, ¿dónde se centra el histograma de $\widehat\beta_1$ en 200 entrenamientos: en 2, en 2.9 o en 5?

El proceso es $y=1+2x_1+3x_2+\varepsilon$, con variables de varianza 1.
Elige una opción. Deja «qué no ve el modelo» en «x2», «corr(x1, x2)»
en 0.3 y «corr(x1, ε): endogeneidad» en 0.
Apaga «agregar la columna que falta». Una combinación nueva puede tardar
unos segundos.

### celda: bloque-4-mira

**Mira.** Cada entrenamiento aporta una pendiente al histograma; compara su centro con la línea verde del valor verdadero y la gris de la cuenta.
Con «el producto x1·x2», cada marca del plano es un residual: orientación y color indican signo; tamaño indica magnitud.
Activa «agregar la columna que falta»: compara el plano y las columnas de $\Phi$ antes y después, además de $L_{\text{val}}$ y el piso impresos.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

Se centra en $2+3\cdot0.3=2.9$. La recta atribuye a $x_1$ parte del efecto
de $x_2$. «Variable omitida» en Leer el error explica la cuenta.
Con varianzas unitarias, para este ajuste que solo ve $x_1$, se reduce a:

$$
2+3\,\operatorname{corr}(x_1,x_2)+\operatorname{corr}(x_1,\varepsilon).
$$

El segundo término recoge la variable omitida; el tercero, la endogeneidad.
Con ambos controles de correlación en cero, la cuenta vuelve a 2.
Las variables normales son entonces independientes: omitir $x_2$ solo sube
el piso cuadrático.

Pon «qué no ve el modelo» en «nada» y aumenta «corr(x1, ε): endogeneidad».
El centro puede desplazarse sin omitir variables.
«Endogeneidad» explica por qué los residuales no revelan ese sesgo del
estimador del coeficiente estructural. El mejor predictor cuadrático busca
$E[y\mid x_{\text{visibles}}]$, que aquí no coincide con $f$.

Combina «x2», «corr(x1, x2)» en 0 y endogeneidad en 0.4.
El piso impreso viene de `ml.piso(datos)` e incluye la variable omitida.
No uses el piso de la endogeneidad sola. Ese límite corresponde al riesgo
poblacional, no obliga a cada $L_{\text{val}}$ muestral a quedar encima.

Con «el producto x1·x2», ambas variables son visibles; falta su interacción
en $\Phi$. Agregar el producto incorpora una columna: el modelo sigue
siendo lineal en sus parámetros.

</details>

### celda: bloque-5-predice

**Predice.** Con $\operatorname{corr}(x_1,x_2)=0.99$, ¿qué varía más entre 200 entrenamientos: $\widehat\beta_1$ o la predicción en $x_1=x_2=1$?

Elige entre la pendiente y la predicción. Pon «corr(x1, x2)» en 0.99 y
«dónde predices» en «dentro de la nube: x1 = x2 = 1».
Cada correlación nueva calcula los entrenamientos una vez; espera unos
segundos antes de comparar las desviaciones impresas.

### celda: bloque-5-mira

**Mira.** Cada punto izquierdo reúne las dos pendientes de un entrenamiento; la nube se alarga donde su suma cambia poco.
El histograma derecho cuenta las predicciones de esos mismos entrenamientos en el punto elegido; compara su ancho con las desviaciones impresas.
En «dónde predices», cambia a «fuera de la diagonal de los datos: x1 = 1, x2 = −1» y observa cómo se ensancha.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

Varía más $\widehat\beta_1$. Con entradas muy parecidas, distintas pendientes
se compensan: la suma $\widehat\beta_1+\widehat\beta_2$ queda bien determinada.
«Colinealidad» en Leer el error muestra que la varianza de cada pendiente
crece con el factor $1/(1-\operatorname{corr}(x_1,x_2)^2)$.

En $x_1=x_2=1$, la predicción usa esa suma y el intercepto.
En $x_1=1,x_2=-1$, usa la diferencia de pendientes, que es inestable.
Predecir fuera de la diagonal extrapola hacia una región con pocos datos.
Ante esa inestabilidad, ¿podemos preferir una solución menos extrema?
El siguiente notebook explora esa posibilidad penalizando pendientes grandes.

</details>

### celda: taller-intro

**Taller.** Corre el proceso activo y cambia una sola línea por una alternativa
comentada. Conserva `ml.taller(datos, clase=3, que="error")`.
Para usar la interacción, cambia `f` y quita `omitir`.
Para los ruidos alternativos, sustituye el argumento `ruido`.

Compara centro, ancho, forma y errores frente al benchmark y al piso.
Después revisa las peores filas y las pendientes al repetir entrenamientos.
Anota qué cambió y qué evidencia gráfica lo muestra.
Con `ruido=ml.t_student(2)`, ignora «a más de 2 EE»: sin varianza finita de la pérdida, ese EE no mide incertidumbre (la definición del punto de comparación de la página exige $E[\ell^2]<\infty$).

### celda: galeria-intro

**Galería.** Pulsa un botón, lee su pregunta y responde antes de abrir
«¿Qué se ve?». Sustenta tu respuesta con una vista del error o con la
distribución de pendientes. Repite con otro botón y distingue qué mecanismo
produce el error en cada caso.
En el caso 6, ignora «a más de 2 EE»: sin varianza finita de la pérdida, ese EE no mide incertidumbre (la definición del punto de comparación de la página exige $E[\ell^2]<\infty$).

### celda: ejercicio-endogena

**Ejercicio.** Con endogeneidad 0.4, calcula en una línea la correlación entre
$e$ y $x_1$ en entrenamiento y en validación.
¿Por qué los residuales no delatan el problema?

En el taller, quita `omitir`, fija la correlación entre variables en 0 y
agrega `endogeno=0.4` a `ml.proceso`. Después ejecuta `m = ml.ajustar(datos)`.
Usa `datos.ent` y `datos.val`, con $e=y-\widehat y$.

**Pista:** ¿qué ecuación cumple el producto entre cada columna de $\Phi$
y los residuales de entrenamiento?

### celda: ejercicio-endogena-respuesta

<details><summary>Respuesta</summary>

```python
[(df["y"] - m.predecir(df)).corr(df["x1"]) for df in (datos.ent, datos.val)]
```

La correlación de entrenamiento es cero, salvo precisión numérica, por las
ecuaciones normales. La de validación fluctúa alrededor de cero.
El ajuste absorbe la parte predecible del ruido correlacionado con $x_1$.
Por eso una nube sin patrón puede acompañar un estimador sesgado del
coeficiente estructural: estimar ese coeficiente y predecir son problemas
distintos.

</details>

### celda: ejercicio-abanico

**Ejercicio.** Compara dos procesos que ven las mismas variables $x_1$ y $x_2$.
Ajusta ambos con la misma $\Phi$: constante, $x_1$, $x_2$.
En A, la desviación del ruido crece con $\lvert x_1\rvert$.
En B, falta representar el producto $x_1x_2$.
Ambos abren un abanico en el residual contra $x_1$.
Encuentra una vista que los distinga.

Copia estos procesos en el taller, después de haber corrido el primer bloque:

```python
A = ml.proceso(n=600, x={"x1": ml.normal(), "x2": ml.normal()}, f=lambda d: 1 + d.x1 + d.x2,
               ruido=ml.heterocedastico(lambda d: np.sqrt(0.25 + d.x1 ** 2)), semilla=0)
B = ml.proceso(n=600, x={"x1": ml.normal(), "x2": ml.normal()},
               f=lambda d: 1 + d.x1 + d.x2 + d.x1 * d.x2, ruido=ml.normal(0, 0.5), semilla=0)
```

Ejecuta `ml.taller(A, clase=3, que="error")` y luego la misma llamada con `B`.
Si necesitas otra vista, `ml.dibujar_residuales_plano(m, datos.val, "x1", "x2")`
acepta el modelo `m = ml.ajustar(datos)`, con `datos = A` o `datos = B`.

**Pista:** ¿qué información pierdes al poner solo $x_1$ en el eje horizontal?

### celda: ejercicio-abanico-respuesta

<details><summary>Respuesta</summary>

El plano $(x_1,x_2)$ conserva la variable que el abanico oculta.
En B, el signo del residual tiende a seguir al de $x_1x_2$:
aparece un patrón por cuadrantes. En A, los signos se mezclan;
crece la dispersión, pero no hay ese patrón en la media.

Respecto del predictor aditivo poblacional $1+x_1+x_2$, ambos errores tienen varianza condicional $0.25+x_1^2$ dado $x_1$.
Los ajustes finitos pueden alterar algo los abanicos.
La página Leer el error pide completar el argumento; aquí ya tienes
la vista que permite distinguirlos.

</details>

### celda: cierre

Lee centro, ancho y forma antes de resumir el error.
Compara con un benchmark y con el piso de la pérdida que usas.
Revisa qué filas dominan el promedio y qué variables o columnas faltan.
Repetir entrenamientos distingue pendientes inestables de predicciones
inestables.

El notebook 7 abre esta pregunta: ¿podemos preferir una solución menos extrema?
