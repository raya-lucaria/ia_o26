### celda: s10-intro

## 10 · Early stopping

¿Hasta cuándo conviene entrenar? Vamos a usar una red grande y pocos
ejemplos de train (entrenamiento) para hacer visible el **overfitting**
(sobreajuste): 2000 ejemplos de train, dos capas ocultas de 256 neuronas,
Adam con learning rate $10^{-3}$, batch 64 y 80 epochs, sin parar antes.
La celda dibuja la red e imprime cuántos parámetros tiene por ejemplo de
train.

Al 20 % de las etiquetas de train le asignamos al azar otra clase, con
una semilla fija. Imagina un dígito tres al que le ponemos la etiqueta «siete». El
cambio no sigue ningún patrón en los píxeles. Es una forma de introducir
el **ruido irreducible** de la unidad 9. Una red con suficiente capacidad
puede memorizar qué etiqueta falsa recibió una imagen concreta.
Validation (validación) y test (prueba) conservan las etiquetas verdaderas.
En MNIST, con etiquetas limpias, el overfitting puede ser difícil de ver.
El ruido deliberado hace más fácil observarlo.

Con **early stopping** (parada temprana) miramos la loss (pérdida) de
validation al final de cada epoch (pasada por train). Cada vez que baja
del mínimo anterior, guardamos un **checkpoint** (punto de guardado)
con los parámetros de la red. La **paciencia** fija cuántas evaluaciones
seguidas podemos pasar sin mejorar antes de detenernos. Al final
restauramos el checkpoint con la menor loss de validation.

En la unidad 9 elegías el grado $N$ del polinomio con validation. Aquí
eliges cuántas epochs entrenar. Cada pasada le da a la red más oportunidad
de ajustar detalles de train. **Elegir la epoch es elegir capacidad**:
la duración del entrenamiento es otro hiperparámetro que elegimos con
validation, nunca con test.

![Parar a tiempo](ilustracion:parar_a_tiempo)
*(Ilustración generada con gpt-image-2.)*

### celda: s10-apuesta

**Apuesta.** Escribe tus respuestas antes de correr el entrenamiento.

- ¿Esperas que la loss de train baje en cada epoch?
- ¿La loss de validation seguirá bajando o llegará a un mínimo y luego subirá?
- Al final, entre los ejemplos con etiqueta cambiada, ¿en cuántos esperas que
  la red prediga la etiqueta falsa que vio durante train?

### celda: s10-apuesta-respuesta

Esperamos que la loss de train baje mucho, con posibles repuntes entre
epochs. Al principio, la red aprende trazos que sirven para reconocer
dígitos nuevos y la loss de validation baja. Más adelante, esperamos que
la red repita muchas de las etiquetas falsas de train y que la loss de
validation suba.

Como vimos en §6, la accuracy (proporción de aciertos) de validation puede
cambiar poco aunque suba su loss. Si la red se equivoca en las mismas
imágenes pero con más confianza, la accuracy queda igual y la loss aumenta.
La intensidad de estas tendencias puede variar entre corridas.

### celda: s10-paciencia-explica

Primero entrenamos hasta completar el presupuesto de epochs. La celda
siguiente simula la parada sobre ese historial. Solo lee la loss de
validation, desde la evaluación de la red recién inicializada. Cuenta las
evaluaciones consecutivas sin un nuevo mínimo. Si aparece un nuevo mínimo,
reinicia el contador. Un empate cuenta como una evaluación sin mejora.

La primera vez que el contador alcanza la paciencia, esa es la epoch en la
que se habría detenido la corrida. Si el historial se acaba antes, la
simulación lo dice: la corrida no habría parado. Los pasos con mini-batches (lotes pequeños)
pueden hacer oscilar la loss de validation. La paciencia da margen para
que una subida aislada sea seguida por una mejora.

Si se activa la parada, la mejor epoch **hasta ese momento** quedó atrás.
Ese es el checkpoint que se restaura al usar early stopping. Casi siempre
coincide con el mínimo de toda la corrida; si validation volviera a
mejorar después de la parada, no coincidirían, y la celda lo avisa.

### celda: s10-memoriza-explica

El panel de la izquierda muestra la loss y el de la derecha la accuracy.
Los dos muestran train y validation. La línea negra discontinua marca el
mínimo de la loss de validation en la corrida completa. Si la simulación
encontró una parada, la línea roja punteada la marca y la sombra indica
las epochs posteriores que se habrían ahorrado.

Busca el tramo donde la loss de train sigue bajando mientras la de
validation se estanca o sube. Es el mismo patrón de overfitting que
buscabas al variar el grado del polinomio. Aquí el eje horizontal cuenta
epochs. La accuracy de train se mide con las etiquetas que vio la red.
Si es muy alta, la red también está acertando etiquetas falsas.

La tabla y las barras comparan el mejor checkpoint y el último de la
corrida completa. Para cada uno, mira estas fracciones:

- Entre las etiquetas limpias, cuántas veces se predice la clase verdadera.
- Entre las etiquetas cambiadas, cuántas veces se repite la etiqueta falsa.
- En ese mismo grupo, cuántas veces se predice la clase verdadera.

Compara en especial la barra de las etiquetas falsas. Si crece del mejor
checkpoint al último, la red terminó memorizando más ruido.

### celda: s10-restaurar-explica

`entrenar` guardó en CPU los checkpoints de la mejor epoch por loss de
validation y de la última epoch. `cargar` coloca los parámetros elegidos
en una red en `DEVICE` y activa el modo de evaluación con `eval()`.

La tabla vuelve a calcular loss y accuracy para los dos checkpoints.
Mide train en el subconjunto con las etiquetas usadas al entrenar.
Mide validation y test completos con las etiquetas verdaderas. Compara
estas métricas con las de las epochs correspondientes del historial.

En un proyecto, eliges el checkpoint con validation y usas test una sola
vez al final para reportar el resultado del modelo elegido. Como en §6,
el notebook registra test en cada epoch con fines didácticos. Aquí la
tabla muestra test para el mejor checkpoint y el último, para ver qué
puede costar seguir entrenando. La elección depende solo de validation.

Busca si el último checkpoint consigue una loss menor en train y una
mayor en validation y test. La accuracy puede moverse poco si el cambio
principal está en la confianza de las predicciones.

### celda: s10-corrida-paciencia-explica

Ahora repetimos el entrenamiento con la misma configuración y con
paciencia activada (`paciencia=6`). `entrenar` aplica la regla durante la corrida y
conserva el mejor checkpoint que encuentra. Si se agota la paciencia,
se ahorra el trabajo de las epochs restantes.

Las semillas fijan los pesos iniciales y el orden de los batches (lotes).
Esperamos que la parada real coincida con la simulada. Pequeñas
diferencias numéricas en GPU pueden moverla. La celda imprime ambos
resultados. La tabla pone el checkpoint que entrega early stopping junto
a los dos del control: debería parecerse al mejor del control y no al
último. La gráfica superpone las curvas de loss de validation; la línea
roja marca dónde se detuvo la corrida con paciencia. La tabla maestra
muestra las dos corridas.

### celda: s10-que-viste

**Qué viste.** Una red grande puede seguir mejorando en train mientras
empeora en validation. Si al final repite más etiquetas falsas de train,
la comparación de checkpoints muestra cuánto ruido llegó a memorizar.

Early stopping usa validation para elegir hasta dónde ajustar la red.
La paciencia da margen a las oscilaciones y el checkpoint recupera el
mejor estado alcanzado. Test queda para reportar al final.

En §9, weight decay (decaimiento de pesos) limita el ajuste al favorecer
pesos pequeños. Aquí lo limitamos con la duración del entrenamiento.
En §15 usaremos `s10-control` para ver si dropout (desactivación aleatoria
de neuronas) también reduce la memorización.
