### celda: portada

# Notebook 10 · ¿Son iid? Fugas

Acompaña la página [¿Son iid? Fugas](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/supuestos-y-metodologia/son-iid-y-fugas/).
Duración del recorrido en clase: ~45 min.

Ejecuta primero la celda de arranque y sigue los bloques en orden.
Antes de abrir cada «Juega», escribe tu predicción.
Después mueve los controles, lee «Mira» y abre «Explicación».
En clase recorrerás los cinco bloques; el taller, la galería y los ejercicios son de casa.

### celda: idea

**¿La validación reproduce lo que sabrás al predecir una entrega nueva?**
Un cliente puede repetir pedidos, el tráfico puede cambiar y una columna puede aparecer después de entregar.
Cada situación exige revisar qué información comparten las filas y qué estará disponible al usar el modelo.

Separaremos dos preguntas: si las observaciones son iid (independientes e idénticamente distribuidas) y si representan la población del uso.
Después revisaremos las fugas (*leakage*): información que entra en la evaluación pero no estará disponible al decidir.

La tubería (*pipeline*) vuelve a ajustar las transformaciones dentro de cada pliegue de validación cruzada (*cross-validation*).
La representación estimada sin el pliegue $m$ se escribe $\widehat\phi^{(-m)}$.
Aquí $m$ identifica el pliegue; no cuenta aristas ni profundidad, como en otras unidades.

$$\widehat\phi^{(-m)}=\phi\ \text{ajustada con }\mathcal A_m$$

Aquí $\mathcal A_m$ son las filas de ajuste de la partición $m$.

Consulta la definición de [Tubería](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/supuestos-y-metodologia/son-iid-y-fugas/#raya-object-ml-c5-def-tuberia) en la página que acompaña el notebook.

### celda: bloque-1-predice

**Predice.** Sacas 200 bolas en 20 puñados de 10, en lugar de una por una. ¿La proporción de rojas varía de muestra a muestra más, igual o menos de lo que promete el error estándar de la clase 2?

Elige una explicación antes de ejecutar:

- Varía igual: sigues contando la misma cantidad de bolas.
- Varía más: las bolas de un puñado comparten su mezcla.

En «Cómo se saca», compara «una por una (iid)» y «a puñados».
Conserva «Tamaño del puñado» en 10.
Luego prueba «de una bolsa que se tiñe» y «de otra bolsa».
El tamaño solo interviene cuando eliges puñados.

### celda: bloque-1-mira

**Mira.** Cada estimación del histograma es la proporción de rojas de una muestra.
Cada barra reúne estimaciones cercanas; no representa una bola.
La banda cubre dos errores estándar a cada lado del centro de las proporciones simuladas.
La línea discontinua marca la proporción de la bolsa del uso: 0.40.

Lee debajo la desviación real de las 200 proporciones y la que promete la fórmula iid.
Con puñados o una bolsa que se tiñe, busca dispersión fuera de la banda.
Con otra bolsa, compara el centro del histograma con la línea discontinua.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Con puñados, compartir la mezcla induce dependencia: contar más bolas no equivale a obtener tantas observaciones independientes.
La bolsa que se tiñe también introduce estructura entre extracciones.
Por eso la dispersión puede superar la que promete la fórmula iid.

La otra bolsa produce una muestra iid y precisa, pero de otra población.
Su histograma puede ser angosto y quedar lejos de la proporción del uso.
La definición de iid (`ml-c5-def-iid`) separa ambas preguntas: cómo obtuviste la muestra y qué población quieres describir.

</details>

### celda: bloque-2-predice

**Predice.** En la otra ciudad las distancias son las mismas, pero el tráfico cambió cuánto tarda cada kilómetro. ¿La validación adversarial lo detecta?

Elige: sí, porque las entregas tardan distinto; o no, porque el detector recibe las entradas y no los tiempos de entrega.

Son las entregas de la clase 2 con más columnas: distancia, hora, lluvia y contexto temporal.
En «Qué cambió», empieza por «nada» y después elige «el tráfico (caso 28)».
Compara también «el mes que viene (deriva en distancia)», «ruido con memoria» y «mismas marginales, otra correlación».

En «Clasificador», alterna «bosque» y «logistica».
El bosque (*random forest*) y la logística buscan distinguir los orígenes con capacidades distintas.
Con «Mostrar valores p» encendido, debajo de los paneles se imprime la tabla de KS con el valor p de cada variable.

### celda: bloque-2-mira

**Mira.** A la izquierda, cada barra reúne probabilidades estimadas de pertenecer al despliegue; los colores distinguen el origen real.
La línea marca $\bar o$, la proporción de filas cuyo origen es el despliegue.
Compara la pérdida logarítmica con su punto de comparación (*benchmark*); el MCC usa ese corte.

En el centro, cada barra horizontal muestra la distancia máxima entre las distribuciones acumuladas de una variable: $\mathrm{KS}_j$.
Con deriva en distancia, busca una barra mayor para esa columna.
Aquí ves barras, no las curvas acumuladas.

A la derecha, cada punto es un residual de validación, ordenado por el tiempo $t$.
Las barras del recuadro son autocorrelaciones por rezago.
Busca ondas y barras persistentes con memoria; una barra aislada fuera de la banda también puede aparecer sin memoria.

Con «mismas marginales, otra correlación», compara lo que distingue el bosque con lo que distingue la logística.
La celda «Comprueba» imprime la pérdida logarítmica contra su benchmark para cada escenario usando el bosque.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

La validación adversarial y KS miran las entradas, no la relación entre esas entradas y el tiempo de entrega.
El cambio del tráfico modifica $f$ sin cambiar su distribución de entradas.
Además, aquí los residuales se calculan en validación, no en la otra ciudad: tampoco muestran ese cambio.

KS revisa cada variable por separado.
Puede pasar por alto una relación distinta entre distancia y hora, aunque sus distribuciones individuales permanezcan iguales.
La adversarial puede detectarla con el bosque y perderla con la logística.

La observación «Un resultado negativo no demuestra iid» (`ml-c5-obs-negativo-no-demuestra`) recoge el límite común.
Un detector callado no certifica que las filas sean independientes ni que el modelo funcione en el uso.

</details>

### celda: bloque-3-predice

**Predice.** Cada cliente tiene su propio retraso habitual y repite pedidos. ¿La CV al azar promete más o menos error del que tendrás con clientes nuevos?

Elige: menos, porque el ajuste reconoce clientes; o un error parecido, porque cada pedido tiene su propia respuesta.

En «Datos», conserva «clientes que repiten».
En «Modelo», compara «el de la clase 2» con «lineal en x».
Recorre las opciones de «Fuerza» y repite con «días seguidos».
Compara siempre las separaciones con el mismo modelo y la misma fuerza.

### celda: bloque-3-mira

**Mira.** Cada marca de CV resume el error de los pliegues para una separación: al azar, por grupos o temporal.
La referencia $R$ aproxima el riesgo en el despliegue.
La tabla imprime `estimado` y `R`; menor error es mejor.
Son pérdidas cuadráticas de los tiempos de entrega, expresadas en minutos cuadrados.

Busca si la CV al azar queda por debajo del riesgo cuando el modelo aprovecha la cercanía.
Después cambia al lineal: observa si las cifras se acercan.
Aquí la CV trabaja sobre entrenamiento y validación; ninguna celda abre la prueba.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

La CV al azar puede prometer menos error porque deja información de clientes conocidos a ambos lados de la separación.
El modelo con dummies del cliente aprovecha esa información.
En días seguidos, los vecinos sobre entrada y tiempo aprovechan la cercanía temporal.
El control lineal puede no aprovecharla del mismo modo.

La observación «Cuándo miente la CV al azar» (`ml-c5-obs-cuando-miente`) requiere considerar juntos el proceso y el modelo.
No basta con que haya clientes repetidos o una serie temporal.

La definición de CV por grupos (`ml-c5-def-cv-grupos`) mantiene juntos los pedidos de cada cliente.
La de CV temporal (`ml-c5-def-cv-temporal`) respeta el orden para evaluar hacia adelante.
Elige la separación que reproduzca el uso que quieres medir.

</details>

### celda: bloque-4-predice

**Predice.** Aquí $y$ es llegó tarde (sí o no). Agregas la calificación que deja el cliente al recibir el pedido. ¿Qué le pasa al MCC que promete la CV, y al MCC con el modelo ya en uso?

Elige: ambos mejoran porque la calificación informa; o mejora el MCC de la CV, pero esa ventaja no llega al despliegue.

En «Fuga», pasa de «ninguna» a «calificación posterior».
Después explora «escalar e imputar antes de separar» y «pedidos duplicados».
«Intensidad» cambia la comparación de la izquierda; «Fuga» elige el caso cuya importancia aparece a la derecha.

### celda: bloque-4-mira

**Mira.** A la izquierda, cada ruta tiene barras para el MCC de la CV y el MCC en el despliegue.
La tabla los llama `estimado` y `en_uso`.
El benchmark es 0; un MCC mayor es mejor.
Al cambiar «Fuga», las rutas siguen juntas en este panel.

A la derecha, cada barra mide cuánto cambia el MCC en validación al permutar una variable.
Busca si `calificacion` concentra la importancia cuando eliges «calificación posterior».
Compara después con «ninguna»: una columna importante requiere revisar cuándo estará disponible.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

La calificación llega después del pedido: informa sobre una respuesta que todavía no conoces cuando necesitas predecir.
La CV puede aprovecharla, pero el modelo en uso no dispone de ella al decidir.
Es una fuga según `ml-c5-def-fuga`: la evaluación recibe información que el uso no tendrá.

Un MCC demasiado bueno y una importancia concentrada son señales para investigar, como plantea `ml-c5-obs-detectar-fuga`.
No prueban por sí solas que haya una fuga.
Con duplicados, revisa si una copia aparece en ajuste y otra en validación.

Escalar e imputar antes de separar casi no cambia la CV en este ejemplo.
Sigue siendo un error de procedimiento, aunque la cifra apenas se mueva.
Lee la diferencia entre el MCC de la CV y el del despliegue, sin trasladar conclusiones entre métricas.

</details>

### celda: bloque-5-predice

**Predice.** Metes escalar, imputar y elegir variables dentro de la tubería. ¿Cuáles de las cuatro fugas desaparecen?

Elige: las cuatro, porque todo pasa por la tubería; o las de ajustar transformaciones y elegir variables fuera de cada pliegue.

En «Fuga», compara «escalar e imputar antes» y «elegir variables antes».
La selección de variables usa el caso 26 con la logística: el objetivo no depende de ninguna columna.
Este selector ofrece esas dos rutas; para la calificación y los duplicados, razona con el bloque anterior.

### celda: bloque-5-mira

**Mira.** Para cada ruta, la gráfica muestra juntas las versiones «sin tubería» y «con tubería».
Cada versión compara el MCC de la CV con el MCC en el despliegue mediante barras.
Busca cuánto cambia la diferencia entre ambos al elegir variables dentro del pliegue.
Al escalar e imputar, el cambio puede ser pequeño.

El interruptor «Ajustar dentro de cada pliegue (tubería)» cambia el mensaje final, pero la gráfica conserva ambas versiones.
Con «escalar e imputar antes» y el interruptor encendido, también aparece $\Phi$.
Cada fila corresponde a un pedido y cada columna a una entrada transformada; identifica `distancia_falta` y las columnas estandarizadas.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

La tubería vuelve a aprender la imputación, la escala y la selección usando solo las filas de ajuste de cada pliegue.
Para limpiar la selección, debe volver a elegir desde todas las columnas originales.
Elegir otra vez desde las columnas previamente seleccionadas conserva información de las respuestas de validación.

La definición de tubería (`ml-c5-def-tuberia`) fija esa separación entre ajustar y transformar.
La de imputación simple (`ml-c5-def-imputacion-simple`) explica cómo completar faltantes con estadísticas aprendidas en ajuste.
La matriz muestra la representación resultante; aquí el modelo del ejemplo con imputación sigue siendo vecinos.

La tubería no vuelve disponible una calificación futura ni separa copias del mismo pedido.
Esos problemas se corrigen en las columnas disponibles y en las filas antes de separar.
Por eso la respuesta abarca dos rutas de ajuste, no las cuatro fugas.

</details>

### celda: taller-intro

**Taller de casa.** El taller, la galería y los tres ejercicios se trabajan fuera del recorrido en clase.
Ejecuta el ejemplo activo y después cambia una alternativa a la vez.
`taller(datos, clase=5)` organiza cinco lecturas:

1. Compara las entradas de entrenamiento y despliegue mediante validación adversarial, con bosque por omisión y pliegues por grupos cuando hay `grupo`.
   Lee el histograma, la pérdida logarítmica contra su benchmark, «señal» o «sin señal» y el MCC con corte en $\bar o$.
2. Presenta las tres mayores $\mathrm{KS}_j$ disponibles entre las variables numéricas: cada una compara entrenamiento con despliegue.
3. Si hay `t`, muestra residuales contra el tiempo y autocorrelaciones sobre entrenamiento y validación.
4. Compara CV al azar y estructurada con el desempeño en el despliegue, usando lineal y vecinos.
   Usa grupos si hay `grupo`; en su ausencia, usa separación temporal si hay `t`.
5. Busca una pérdida de CV sospechosamente inferior al piso de esa pérdida, o una variable que concentre más de la mitad de la importancia.
   La alarma pide investigar; no demuestra una fuga.

En regresión, $R$ es el riesgo en el despliegue.
En clasificación, lee «MCC en el despliegue» y compara con el MCC de la CV.
La alarma basada en pérdidas no convierte el piso en un límite para el MCC.

El ejemplo activo usa clientes repetidos y `despliegue="grupos_nuevos"`.
Los comentarios proponen tres cambios:

- Tiempo: sustituye el ruido por `ar1(persistencia=0.9)` y usa `despliegue="futuro"`.
  Aquí $R$ mide el error a largo plazo con otra realización del ruido.
- Otra ciudad: usa `despliegue="otra_poblacion"` y agrega la deriva de distancia que aparece comentada.
- Una fuga: después de crear `datos`, aplica `sembrar_fuga(datos, tipo="duplicados")` antes de llamar al taller.

En las dos primeras alternativas, edita los argumentos de `proceso`; descomentar una línea suelta no los sustituye.
Conserva la llamada al taller al final.

### celda: galeria-intro

**Galería de casa.** Lee cada pregunta y escribe una predicción antes de abrir su explicación.

- Caso 13, días seguidos: ¿qué cambia al separar al azar observaciones con memoria?
- Caso 14, grupos: ¿qué información comparte un cliente que repite pedidos?
- Caso 15, población distinta: ¿a quién representa la muestra que evalúas?
- Caso 16, subgrupo raro: ¿qué pudo concentrarse en un solo pliegue?
- Caso 19, variable posterior: ¿qué le pasa al MCC que promete la CV?
- Caso 20, preprocesar antes de separar: ¿cuánto cambia la CV?
- Caso 21, duplicados entre conjuntos: ¿qué promete la CV?
- Caso 26, selección previa: si ninguna columna tiene que ver con $y$, ¿qué promete la CV?
- Caso 27, categoría nueva: ¿qué predice el modelo para un pedido del sur?
- Caso 28, cambio de concepto: ¿lo ve la validación adversarial?

### celda: ejercicio-pliegue-raro

**Ejercicio de casa.** Error bajo en todos los pliegues menos en uno. ¿Qué pudo pasar?

Usa el caso 16 de la galería.
Propón una explicación relacionada con quiénes quedaron en ese pliegue y otra relacionada con cuándo se observaron.
Indica qué separación usarías para investigar cada explicación.

### celda: ejercicio-pliegue-raro-respuesta

<details><summary>Explicación</summary>

Un grupo o un periodo poco representado puede haberse concentrado en ese pliegue.
El promedio de los otros pliegues oculta esa dificultad.
Repite la CV por grupos o temporal, según la explicación, y revisa si desaparece el patrón de un único pliegue difícil.
También revisa qué población representa cada pliegue; cambiar la separación no garantiza que el problema desaparezca.

</details>

### celda: ejercicio-submuestra

**Ejercicio de casa.** Alguien dice: “como es una submuestra, elegir variables con todas las filas no importa”. Usa el caso 26 (`seleccion_previa`) con n = 100 y n = 1 000 y mide cuánto infla.

Para cada tamaño, compara la selección previa con la selección dentro de cada pliegue.
Anota el MCC de la CV y el MCC en el despliegue; después calcula su diferencia.
Conserva el universo completo de columnas al construir la versión limpia.

Para medirlo, abre la celda de B5, cambia `n=100` por `n=1000` en el caso 26 y vuelve a correrla: la tabla impresa trae los dos MCC de «elegir variables antes».

### celda: ejercicio-submuestra-respuesta

<details><summary>Explicación</summary>

Elegir variables con todas las respuestas deja que las respuestas de validación influyan en lo que recibe el modelo.
Llamar submuestra al conjunto no borra esa información.
Con muchas columnas de ruido, la selección previa puede seguir inflando el MCC de la CV.
La magnitud se mide por separado para cada tamaño; no tiene que ser igual.

La versión limpia vuelve a seleccionar desde todas las columnas dentro de cada pliegue.
No basta con reajustar la logística sobre las columnas que se eligieron antes.

Las cifras de cada tamaño son las que imprime B5 al correrla con cada `n`.

</details>

### celda: ejercicio-residuos-alternos

**Ejercicio de casa.** Los residuales son $(1,-1,1,-1,1,-1)$.
¿Cuál es su autocorrelación de rezago 1?

El estimador compara productos de residuales vecinos con la suma de cuadrados de toda la serie centrada.
Escribe $e_t$ para el residual en el tiempo $t$ y $\bar e$ para su promedio.
Con denominador común, el rezago 1 se calcula así:

$$
\frac{\sum_{t=1}^{n-1}(e_t-\bar e)(e_{t+1}-\bar e)}
     {\sum_{t=1}^{n}(e_t-\bar e)^2}.
$$

Cuenta los productos del numerador y los cuadrados del denominador.
Comprueba con `ml.autocorrelacion([1, -1, 1, -1, 1, -1], rezagos=1)`.
Explica por qué una media cero no basta para descartar estructura.

### celda: ejercicio-residuos-alternos-respuesta

<details><summary>Explicación</summary>

La media es cero y cada producto de vecinos vale $-1$.
El numerador suma cinco productos y el denominador suma seis cuadrados iguales a uno.
Por eso `autocorrelacion` devuelve $-5/6$ en el rezago 1.

La correlación de Pearson entre la serie recortada y su desplazamiento daría $-1$, como `pandas.Series.autocorr`.
Es otro cálculo: aquí el denominador conserva la suma de cuadrados de toda la serie.
Los signos alternan perfectamente; tener media cero no elimina esa estructura.

</details>

### celda: cierre

Te llevas dos preguntas distintas: si la muestra es iid y si representa el uso.
Los detectores dan señales limitadas; la separación debe reproducir el uso y las transformaciones deben ajustarse dentro de cada pliegue.
La tubería no corrige columnas futuras ni pedidos duplicados.

Ya sabes medir bien; ¿en qué orden se trabaja?
