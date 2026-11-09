### celda: portada

# Notebook 8 · Pérdida, métrica y desbalanceo

**¿Cómo puedes acertar casi siempre y dejar pasar todos los fraudes?**

Este notebook acompaña [Pérdida, métrica y desbalanceo](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/clasificacion/perdida-metrica-y-desbalanceo/). Dedica unos 35 minutos a leer, mover controles y comprobar tus predicciones. Puedes dejar el bloque de pliegues para recorrerlo en casa.

Al terminar tendrás:

- **Una distinción:** separarás lo que minimiza el ajuste de lo que mide su utilidad.
- **Una regla de decisión:** elegirás el umbral con validación.
- **Una comparación:** reconocerás qué cambia al dar más peso al fraude.

Ejecuta las celdas en orden. Antes de cada control, responde «Predice»; después consulta «Mira» y abre la explicación.

### celda: idea

La [página](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/clasificacion/perdida-metrica-y-desbalanceo/) distingue ajustar probabilidades y decidir. El lagrangeano combina pérdida ponderada de entrenamiento $L^w_{\text{ent}}$ y penalización de pendientes $\beta$, sin penalizar el intercepto. Aquí $\beta$ son parámetros, no el $\beta$ de la poda alfa-beta de la unidad de juegos; $\mu$ regula la penalización, no es una distribución de la unidad de Markov. `L_ent` nombra la pérdida de entrenamiento sin ponderar. Se entrena con la pérdida, se decide con $\tau$, se juzga con MCC.

$$
\min L^{w}_{\text{ent}}+\mu\lVert\beta\rVert_2^2
$$

### celda: bloque-1-predice

## 1 · Sigue las pendientes

**Predice:** Con datos separables y $\mu$ casi 0, ¿deja de crecer $\lVert\widehat\beta\rVert_2$ en cuanto aciertas todos los casos de entrenamiento?

Elige: se detiene al acertarlos todos, sigue creciendo o empieza a disminuir. Aquí la norma mide las pendientes estandarizadas; deja fuera el intercepto.

Mueve «log₁₀ μ» hacia valores menores. Luego cambia «datos separables (caso 17)» para comparar con etiquetas reasignadas.

### celda: bloque-1-mira

**Mira:** A la izquierda, cada punto es un caso de entrenamiento y la curva muestra la probabilidad estimada. Con datos separables, observa cómo se acerca a un escalón.

A la derecha, cada curva muestra la norma de las pendientes frente al valor del control. El rombo marca el ajuste actual. Sigue la curva separable hacia valores menores de `mu`: sube casi en recta; con ruido tiende a aplanarse.

Debajo aparecen los aciertos $A$ y la pérdida $L$ en entrenamiento y validación. Compara cada pérdida con su punto de comparación (*benchmark*), que predice la proporción de clases.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

Sigue creciendo: acertar la etiqueta todavía permite reducir la pérdida logarítmica al aumentar la probabilidad asignada a la clase correcta. Con datos separables y sin penalización, no hay un óptimo finito.

Con $\mu>0$ recuperas un óptimo finito, aunque sus pendientes pueden ser grandes. Al reducir `mu`, la norma crece aproximadamente como $\ln(1/\mu)$: aumenta por décadas, sin una explosión exponencial.

</details>

### celda: bloque-2-predice

## 2 · Mueve la decisión

**Predice:** Si mueves $\tau$ de 0.5 a 0.2 sin reentrenar, ¿qué le pasa a la pérdida logarítmica en validación: sube, baja o no cambia?

Prueba con «umbral τ». $\tau$ es el umbral para anunciar fraude; aquí no es un tablero ni un tiempo de llegada. `tau` cambia la decisión sobre las probabilidades que ya entrega `modelo`.

### celda: bloque-2-mira

**Mira:** Arriba hay histogramas de probabilidades, separados por clase real. Sus barras cuentan casos; la línea vertical marca el umbral. Al bajarlo, más casos quedan del lado anunciado como fraude.

Abajo, cada curva corresponde a una métrica: MCC, aciertos balanceados $A_{\text{bal}}$ o aciertos $A$. MCC resume la asociación entre etiquetas reales y predichas. Los puntos señalan las métricas del umbral actual. Mira el título: la pérdida permanece igual.

Activa «marcar el τ que elige validación». Compara esa marca con tu elección. La salida inferior muestra también el MCC en el despliegue.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

No cambia: la pérdida logarítmica usa probabilidades y clases reales; no usa `tau`. Las métricas de clasificación sí cambian cuando cambian las etiquetas predichas.

La celda elige `mu` mediante validación cruzada (*cross-validation*) estratificada dentro de entrenamiento. Después, `ml.elegir_umbral` elige el umbral con MCC en validación. El despliegue sirve para observar el resultado, no para elegir.

En el ejemplo de dos reglas de la página, la regla A tiene pérdida 0.186, aciertos 0.75 y MCC 0.577. La regla B tiene pérdida 0.511, aciertos 1 y MCC 1. La menor pérdida y el mayor MCC pueden pertenecer a reglas distintas.

</details>

### celda: bloque-3-predice

## 3 · Compara con la moda

**Predice:** Con 1 % de fraudes, ¿cuántos aciertos saca la regla que siempre dice “legítimo”, y cuánto vale su MCC? ¿Y si le pones pesos a la logística?

Decide si acertar casi todos implica detectar fraudes. Después anticipa si los pesos mejorarán todas las métricas o si habrá un intercambio.

Elige «1 %» en «proporción de fraude Pr(y=1)». Activa «con pesos balanceados (los explica el bloque 4)» y después «medir en validación».

### celda: bloque-3-mira

**Mira:** Cada punto resume una métrica para un modelo y una proporción de fraude. Las barras muestran dos errores estándar entre repeticiones. La línea vertical marca la proporción elegida; la referencia de moda siempre anuncia la clase más frecuente.

Compara los paneles de MCC, aciertos balanceados y aciertos. Al activar los pesos, busca la mejora en detección junto con la caída en aciertos globales. Con «medir en validación», observa la banda superpuesta: pocos fraudes vuelven inestable la medición. Con 1 %, muchas validaciones chicas no traen ningún fraude: ahí los aciertos balanceados no se pueden medir y su banda las deja fuera, mientras el MCC las cuenta como 0.

La tabla inferior separa fracción de casos, fracción del peso, contribución a `L_ent` y pérdida media por clase. Localiza la fila de fraude: una clase puede pesar poco y tener una pérdida media grande.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

La moda obtiene aciertos 0.99, aciertos balanceados 0.5 y MCC 0. No detecta fraudes. La logística sin pesos puede acercarse a esa regla; con pesos puede mejorar MCC y aciertos balanceados mientras pierde aciertos globales.

La pérdida sin pesos promedia por caso. Por eso, la clase rara recibe aproximadamente su proporción del peso total. Su fracción de la pérdida puede ser distinta: también depende de cuánto se equivoca el modelo con ella.

La moda es el benchmark de clasificación. Para la pérdida logarítmica, predecir la proporción de clases tiene como benchmark la entropía, explicada en la página. Ninguna referencia elimina la incertidumbre de medir con pocos fraudes.

</details>

### celda: bloque-4-predice

## 4 · Cambia el peso del fraude

**Predice:** Si el fraude pesa nueve veces más que lo legítimo, ¿qué le pasa al $\widehat p$ promedio que anuncia el modelo en la realidad?

Elige: se mantiene junto a la proporción real, sube o baja. Mueve «log₁₀(w₁/w₀)» y activa «comparar con mover τ en el modelo sin pesos».

$w_y$ es el peso de la clase $y$; aquí $w$ no es una cadena ni el resultado de un hijo. El cociente del control compara el peso del fraude con el de lo legítimo.

### celda: bloque-4-mira

**Mira:** En el panel de fronteras, cada punto es un caso de entrenamiento. Las líneas comparan el modelo ponderado y el modelo sin pesos con un umbral distinto. Observa cuánto se acercan; no supongas coincidencia exacta.

En los paneles centrales, sigue el cambio del intercepto y el promedio de probabilidades anunciado. Este promedio se separa de la proporción real cuando aumenta el peso del fraude.

A la derecha, cada curva mide el desempeño en despliegue contra la razón de pesos. Compara sus máximos: favorecer más al fraude no mejora indefinidamente MCC. Lee debajo la razón balanceada calculada en entrenamiento y ubícala sobre el eje.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

El promedio anunciado sube: ahora equivocarse con un fraude cuesta más durante el ajuste. Los pesos cambian el objetivo; no cambian la proporción de fraude en la realidad.

En población, con $\mu=0$ y un modelo bien especificado, ponderar equivale a desplazar el intercepto por $\ln(w_1/w_0)$. También equivale a mover el umbral del modelo sin pesos. Fuera de esas condiciones, la equivalencia puede fallar.

Los pesos balanceados igualan el peso total de las clases. En el ejemplo con 950 legítimos y 50 fraudes, los pesos son $w_0=0.526$ y $w_1=10$. El primer valor está redondeado; con los valores completos, la suma de pesos es 1000.

En el caso ideal, la razón balanceada optimiza los aciertos balanceados; no tiene por qué optimizar MCC. Elige la razón en validación con la métrica que vas a juzgar. Pesos y umbral son decisiones distintas: puedes combinarlos, pero no corregir dos veces de memoria.

> [!WARNING]
> Lectura equivocada: «Los pesos corrigen las probabilidades».
>
> Lectura correcta: **Los pesos cambian el objetivo de ajuste.** Una mejor clasificación puede acompañarse de peor calibración: las probabilidades anunciadas dejan de corresponder a las frecuencias observadas.

</details>

### celda: bloque-5-predice

## 5 · Distingue los promedios

**Predice:** Con 90 % legítimo, 8 % publicidad y 2 % fraude, ¿el promedio ponderado de los aciertos por clase queda cerca del macro o de los aciertos $A$?

El macro da la misma importancia a cada clase. El ponderado usa su soporte: cuántos casos de esa clase hay en el conjunto evaluado.

Elige entre «coincide con el macro», «coincide con los aciertos» y «no coincide necesariamente con ninguno». Cambia «proporciones» y luego «pesos balanceados».

### celda: bloque-5-mira

**Mira:** Los colores de fondo indican qué clase anuncia el modelo en cada región. Los puntos son 600 casos de validación tomados al azar, con las proporciones reales; su marca identifica la clase real.

En las barras, la longitud representa los aciertos de cada clase y el grosor representa su soporte. Las líneas verticales marcan macro y ponderado. Busca si el promedio ponderado oculta una barra corta de la clase rara.

La salida inferior compara el MCC multiclase del modelo con el de la moda. La matriz $\Phi$ impresa arriba muestra las columnas que recibe el modelo, incluida la constante.

### celda: bloque-5-explica

<details><summary>Explicación</summary>

El promedio ponderado coincide exactamente con los aciertos $A$: cada clase aporta según cuántos casos tiene. El macro coincide con los aciertos balanceados $A_{\text{bal}}$: todas las clases cuentan igual.

Estos promedios se calculan sobre la validación observada, incluso si entrenaste con pesos. No confundas ponderar los aciertos por soporte con ponderar la pérdida durante el ajuste. El MCC multiclase es una medida global; no es el promedio de los MCC de cada clase.

</details>

### celda: bloque-6-predice

## 6 · Mira cada pliegue

**Predice:** Con 10 fraudes y $k=10$ estratificado, cada pliegue de validación tiene un fraude. ¿Cuánto puede cambiar el MCC de un pliegue a otro?

Elige: casi nada, mucho o nada porque estratificaste. Aquí $k$ cuenta pliegues; no es el índice de clase de la unidad de optimización.

Para recordar cómo se reparten los casos raros, vuelve al bloque 5 del notebook 04.

Mueve «pliegues k» y «fraudes en la muestra». La partición siempre es estratificada; lee el conteo real que imprime la celda.

### celda: bloque-6-mira

**Mira:** Cada punto corresponde a la métrica de un pliegue de validación. La raya horizontal indica su media. Compara la dispersión al aumentar los fraudes disponibles y al reducir el número de pliegues.

Busca las marcas «no estimable» y «0 por convención». La primera corresponde a aciertos balanceados cuando falta una clase real. La segunda advierte que un MCC nulo procede de la convención para ese caso, no de una evaluación informativa del fraude.

### celda: bloque-6-explica

<details><summary>Explicación</summary>

Puede cambiar mucho: con pocos fraudes, acertar o fallar uno altera la medición del pliegue. Estratificar reparte los disponibles; no crea observaciones nuevas. La media resume los pliegues, pero no vuelve precisa una medición con poca información.

Un MCC nulo sin fraudes no demuestra que el modelo pueda reconocerlos. Reducir `k` deja más casos para validar en cada pliegue. Reunir más fraudes también ayuda; juntar clases exige que esa agrupación tenga sentido para el problema.

El bloque 5 del notebook 04 muestra el reparto que explica estas limitaciones.

</details>

### celda: taller-intro

## Taller · Elige qué vas a juzgar

Cambia una opción de la celda y vuelve a ejecutarla. Conserva primero el proceso de fraude; después prueba una alternativa comentada. Para los anillos, usa también la representación polar indicada en el comentario.

Antes de comparar modelos, escribe qué métrica te importa y qué error quieres reducir. Elige y diagnostica con las reservas de validación que imprime el mapa: `val_a` para la recalibración y el umbral $\tau$; `val_b` para comparar y elegir. `cal` queda fuera de toda elección; solo fija el corte conformal. Observa en `datos.despliegue` cómo se comporta la elección sobre la población simulada.

Lee el mapa de reservas que imprime el taller: aparta `cal`, `val_a` y `val_b` para funciones distintas. Su salida indica predicción conformal por clase de manera automática en este proceso estratificado. El notebook 09 desarrolla esa parte; aquí concentra tu comparación en pérdida, umbral y métrica.

### celda: galeria-intro

## Galería · Busca dónde falla la regla

Recorre los casos separable, desbalanceado, multiclase y de clase rara en el centro. Antes de tocar un control, identifica la clase que una regla constante dejaría pasar.

Compara la frontera, el MCC y los aciertos balanceados con sus referencias. Pregúntate si el problema es el peso de la clase o la representación que recibe el modelo. Dar más peso al fraude no permite dibujar cualquier frontera.

### celda: ejercicio-moda

## Ejercicio · Calcula la moda

Con 2 % de fraudes, una regla siempre anuncia «legítimo». Anticipa sus aciertos, sus aciertos balanceados y su MCC. Después copia este código en una celda nueva y ejecútalo:

```python
y = np.r_[np.zeros(98, dtype=int), np.ones(2, dtype=int)]
y_gorro = np.zeros_like(y)
print("A:", ml.aciertos(y, y_gorro))
print("A_bal:", ml.aciertos_balanceados(y, y_gorro, clases=[0, 1]))
print("MCC:", ml.mcc(y, y_gorro, clases=[0, 1]))
```

Explica por qué sus aciertos pueden parecer buenos aunque no detecte ningún fraude. Como pista, compara lo que le ocurre a cada clase antes de promediar.

### celda: ejercicio-moda-respuesta

<details><summary>Explicación</summary>

Obtienes aciertos 0.98, aciertos balanceados 0.5 y MCC 0. La regla acierta todos los legítimos y falla todos los fraudes. Los aciertos globales reflejan el predominio de los legítimos; el promedio balanceado da igual importancia a ambas clases.

Como la predicción es constante, MCC toma el valor nulo por convención. No hay asociación útil entre la predicción y la presencia de fraude.

</details>

### celda: ejercicio-regresion-y-sigmoide

## Ejercicio · Compara los objetivos de ajuste

¿Basta ajustar una recta por mínimos cuadrados y pasar su salida por la sigmoide para obtener una logística? Predice cuál tendrá menor pérdida logarítmica en validación. Usa los mismos datos y columnas del bloque de umbral.

Copia el código en una celda nueva. `beta_mse` guarda los coeficientes que minimizan el error cuadrático medio, MSE; `modelo` es la logística ya seleccionada. Reutiliza `modelo.Phi` para conservar la transformación aprendida en entrenamiento. La sigmoide convierte la salida de la recta en valores entre cero y uno.

```python
datos = datos2
beta_mse = np.linalg.lstsq(modelo.Phi(datos.ent), datos.ent["y"], rcond=None)[0]
p_mse = 1 / (1 + np.exp(-(modelo.Phi(datos.val) @ beta_mse)))
print("Recta y sigmoide:", ml.log_loss(datos.val["y"], p_mse))
print("Logística:", ml.log_loss(datos.val["y"], modelo.predecir_p(datos.val)))
```

Lee los resultados y justifica la diferencia sin cambiar el umbral. Pista: ¿qué objetivo eligió los coeficientes antes de aplicar la sigmoide?

### celda: ejercicio-regresion-y-sigmoide-respuesta

<details><summary>Explicación</summary>

No basta. La recta se ajustó para acercar su salida a las etiquetas mediante pérdida cuadrática. Aplicar después una sigmoide no vuelve a elegir sus coeficientes con pérdida logarítmica.

La logística ajusta los coeficientes usando la pérdida logarítmica y su penalización. Compara las pérdidas impresas en validación: esa salida decide cuál gana en esta muestra. El objetivo de entrenamiento no garantiza el orden de las pérdidas en toda validación posible.

</details>

### celda: cierre

La pérdida guía el ajuste de los parámetros. El umbral convierte probabilidades en decisiones y se elige en validación. La métrica juzga esas decisiones: acertar casi todos los casos puede ocultar que pierdes todos los fraudes.

Antes de continuar con calibración en el notebook 09, deja planteada esta pregunta: «ese 0.8 con pesos, ¿todavía significa ocho de cada diez?».
