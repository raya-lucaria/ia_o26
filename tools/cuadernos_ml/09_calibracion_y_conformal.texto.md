### celda: portada

# Calibración y predicción conformal

**Si un modelo anuncia 0.8 de probabilidad de fraude, ¿puedes tomar esa cifra al pie de la letra?**

Al terminar tendrás:

- **Diagnóstico:** distinguirás una probabilidad confiable de un puntaje desplazado por los pesos.
- **Recalibración:** separarás los mensajes usados para ajustar de los usados para juzgar.
- **Conjuntos:** compararás cobertura y tamaño al cambiar cuánto error admites.
- **Garantía:** explicarás por qué una cobertura global puede esconder fallas entre los fraudes.

Corre las celdas en orden. Antes de mover cada control, escribe tu predicción. Abre la explicación después de mirar el resultado.

La [página de calibración y conformal](https://raya-lucaria.github.io/ia_o26/aprendizaje-maquina/clasificacion/calibracion-y-conformal/) acompaña este recorrido.

### celda: idea

Una probabilidad está calibrada si, entre los casos con un valor anunciado parecido, la frecuencia de fraude coincide con ese valor.

La predicción conformal cambia la pregunta: devuelve un conjunto de etiquetas, $C(x)$, y busca incluir la etiqueta verdadera. Su garantía es $\Pr(y\in C(x))\ge1-\delta$. Aquí $\delta$ es la probabilidad de fallar: pedir cobertura 0.90 significa admitir $\delta=0.10$. No es la función de transición de computabilidad ni el error matricial de Markov.

La garantía requiere intercambiabilidad de calibración y del caso nuevo, condicionada en el modelo congelado. El entrenamiento no debe depender de ellos. La probabilidad abarca tanto la calibración como el caso nuevo.

Este es el mapa de reservas; cada renglón tiene un trabajo distinto:

- `ent` → ajusta $\beta$ y permite elegir $\mu$ y los pesos.
- `val_a` → ajusta Platt y permite elegir el umbral $\tau$.
- `val_b` → diagnostica y permite elegir el procedimiento.
- `cal` → fija el corte conformal $\widehat c$; **`cal` se aparta primero**.
- prueba → se abre una vez, cuando el procedimiento ya está fijado.

Aquí $\beta$ son parámetros, no el $\beta$ de la poda alfa-beta de la unidad de juegos. $\mu$ controla la regularización, no es una distribución de Markov. $\tau$ es el umbral de clasificación, no un tablero ni un tiempo de llegada.

Los bloques binarios usan `datos`, `val_a` y `val_b`; no necesitan `cal`. Los bloques de tres clases tienen sus propias reservas. La prueba permanece cerrada en este recorrido.

### celda: bloque-1-predice

## 1 · Lee las probabilidades anunciadas

**Entre los mensajes a los que el modelo con pesos balanceados les anuncia cerca de 0.8, ¿qué fracción es fraude: cerca de 0.8, más o mucho menos?**

Elige una respuesta antes de ejecutar. En «modelo», comienza con «con pesos balanceados» y después compara «sin pesos» y «proporción (benchmark)». Este último es el punto de comparación (*benchmark*): anuncia siempre la proporción de fraude de entrenamiento.

En «con qué se dibuja», compara «100 casos de val_b», «toda val_b (N)» y «realidad (100 000)». En el control, N se sustituye por el tamaño que imprime la celda. Después cambia «grupos» sin cambiar el modelo.

### celda: bloque-1-mira

Con «toda val_b (N)», **la curva y el Brier se miran en `val_b`**. Cada punto reúne mensajes con probabilidades parecidas. Su posición horizontal es la probabilidad media anunciada; su altura es la fracción observada de fraudes.

La diagonal representa coincidencia entre anuncio y frecuencia. Un punto debajo indica que el modelo anuncia demasiado fraude. El benchmark forma un punto porque da la misma probabilidad a todos los mensajes.

Con «100 casos de val_b» usas una submuestra fija: mover «grupos» no vuelve a sortearla. Observa cuánto cambia la curva con pocos mensajes por grupo. «realidad (100 000)» usa una muestra enorme del proceso simulado; no son datos disponibles para el alumno en una aplicación real.

La curva verdadera usa las probabilidades del proceso. Las cifras impresas de Brier y pérdida logarítmica siguen midiéndose en `val_b`, cualquiera que sea la muestra dibujada. Ambas comparan probabilidades con etiquetas; menor es mejor. Mira sus valores junto a los del benchmark.

### celda: bloque-1-explica

<details><summary>Explicación</summary>

La respuesta es **mucho menos**. Los pesos balanceados aumentan la influencia del fraude durante el ajuste. Eso puede ayudar a decidir etiquetas, pero no convierte las salidas en probabilidades calibradas.

El resultado poblacional precisa el desplazamiento: sin regularización y con el modelo bien especificado, los pesos suman $\ln(w_1/w_0)$ al puntaje logístico. Aquí $w_y$ es el peso de clase, no una cadena ni el valor de un hijo en juegos.

Con razón de pesos 19, un cliente con probabilidad verdadera de fraude 0.05 recibe probabilidad ponderada 0.5. El cambio refleja el objetivo ponderado. No significa que la frecuencia real de fraude haya aumentado.

Este ajuste usa una muestra finita y regularización. Por eso el desplazamiento teórico orienta la lectura, pero no promete una corrección exacta del modelo ajustado.

La curva también depende de cuántos casos caen en cada grupo. Una curva irregular con pocos datos no basta para atribuir cada desviación al modelo. Cambiar los grupos cambia el diagnóstico dibujado; no cambia sus predicciones.

</details>

### celda: bloque-2-predice

## 2 · Juzga la recalibración con otros mensajes

**Si ajustas la recalibración y la evalúas con los mismos mensajes, ¿la curva se verá mejor o peor que en mensajes nuevos?**

Anota «mejor», «peor» o «casi igual». En «método», compara «ninguno», «platt» e «isotonica». Para cada opción, cambia «evaluar con los mismos datos que recalibraron» y observa si mantendrías tu respuesta.

### celda: bloque-2-mira

**Platt se ajusta en `val_a` y se juzga en `val_b`.** La isotónica también se ajusta en `val_a`. Con el interruptor apagado, la curva usa `val_b`; encendido, usa `val_a`, los mismos mensajes que ajustaron la recalibración.

Cada punto sigue siendo un grupo de probabilidades anunciadas frente a su frecuencia observada. La curva «realidad» permite comparar con una muestra enorme del proceso. Mira si la cercanía a la diagonal persiste fuera de `val_a`.

Prueba especialmente «isotonica» con el interruptor encendido. Después apágalo. Las cifras «antes» y «después» siempre corresponden a `val_b`: el interruptor cambia la curva seleccionada, no el conjunto de esas cifras.

### celda: bloque-2-explica

<details><summary>Explicación</summary>

La curva suele verse mejor con los mismos mensajes. La isotónica ajusta una transformación creciente flexible y puede quedar sobre la diagonal en sus propios datos. Esa apariencia no garantiza que funcione igual en mensajes nuevos.

Platt transforma el puntaje logístico mediante una pendiente y un intercepto ajustados. En este ejemplo cambia poco al alternar los conjuntos. Compara también las pérdidas en `val_b`; la curva agrupada no resume por sí sola todo el diagnóstico.

Recalibrar es **otro ajuste**. Los coeficientes que imprime Platt son parámetros de esa recalibración. Elegir «platt» o «isotonica» es elegir un hiperparámetro: el método. `val_a` estima los parámetros; `val_b` permite juzgar el resultado y elegir entre procedimientos.

> [!WARNING]
> Lectura equivocada: «La isotónica coincide con la diagonal, así que ya comprobé que generaliza».
>
> Lectura correcta: **si miraste `val_a`, juzgaste el ajuste con los mismos datos que lo construyeron**.

</details>

### celda: bloque-3-predice

## 3 · Pide un conjunto de etiquetas

**Si pides cobertura 0.99 en lugar de 0.90, ¿los conjuntos crecen, se encogen o quedan igual?**

En «δ (1 − cobertura)», pasa de 0.10 a 0.01. Conserva el mismo «mensaje» mientras comparas. Después recorre «claro», «ambiguo» y «difícil». Anota si cambia cada conjunto particular.

Aquí empieza otro proceso: `datos3` tiene tres clases. `cal3` es la pieza `cal` del proceso de tres clases y se aparta primero. `modelo3` se ajusta con `datos3.ent`. La regularización se elige por validación cruzada (*cross-validation*) estratificada dentro de ese entrenamiento.

### celda: bloque-3-mira

Mira las probabilidades impresas del mensaje y las etiquetas incluidas en $C(x)$. Cada etiqueta incluida cuenta como un elemento del conjunto. Observa el corte $\widehat c$ junto al mensaje: ese número decide qué etiquetas entran.

La gráfica evalúa los conjuntos en `datos3.despliegue`. La cobertura es la fracción de mensajes cuyo conjunto incluye la etiqueta verdadera. El tamaño medio cuenta cuántas etiquetas devuelve, en promedio, por mensaje. Mira ambos valores impresos al cambiar $\delta$.

### celda: bloque-3-explica

<details><summary>Explicación</summary>

Los conjuntos **crecen o quedan iguales** al pedir más cobertura. Para un mensaje particular pueden quedarse iguales: las etiquetas entran de manera discreta. No se encogen si conservas el modelo y la calibración.

Conformal mide qué tan poco probable parecía la etiqueta verdadera en cada caso de `cal3`. Ese puntaje de no conformidad es $c_i=1-\widehat p_{y_i}(x_i)$. Aquí $\widehat p_{y_i}(x_i)$ es la probabilidad que el modelo asignó a la etiqueta verdadera del caso. Cuanto menor fue esa probabilidad, mayor es el puntaje.

El corte $\widehat c$ es un cuantil corregido de esos puntajes. Entra una etiqueta candidata si su puntaje no supera ese corte. Pedir más cobertura aumenta el corte o lo deja igual. Aquí $c$ nombra puntajes y $C$ conjuntos de predicción; no certificados, caras del dado ni casillas de juegos.

La garantía promedia sobre calibraciones y casos nuevos, con el modelo congelado. **Esta calibración concreta puede quedar un poco debajo de la cobertura pedida**, incluso al evaluar muchos mensajes. No promete cobertura para cada mensaje ni para cada clase por separado.

Conformal tampoco necesita que las probabilidades estén perfectamente calibradas. Probabilidades más informativas pueden permitir conjuntos menores. Una garantía de cobertura pierde utilidad si casi siempre devuelve todas las etiquetas.

</details>

### celda: bloque-4-predice

## 4 · Revisa quién queda sin cubrir

**Con 2 % de fraude y $1-\delta=0.90$, ¿la cobertura entre los fraudes también será cerca de 0.90?**

Elige «sí», «puede ser mucho menor» o «debe ser mayor». Deja «δ» en 0.10. Compara «conformal por clase» apagado y encendido, primero con 10 000 en «casos en la muestra» y después con 2000.

La reserva cumple el papel de `cal3`: la pieza `cal` del proceso de tres clases. En esta celda se llama `cal` y se guarda en `D4` para cada tamaño. Se aparta antes del ajuste; no reutiliza la reserva del bloque anterior.

### celda: bloque-4-mira

Cada barra representa la cobertura dentro de una clase en `d4.despliegue`: 0 es legítimo, 1 publicidad y 2 fraude. Compara la barra de fraude con la línea de cobertura pedida. Mira también el tamaño medio por clase: cubrir más etiquetas tiene un costo.

Al activar «conformal por clase», se calcula un corte distinto con los casos de cada clase en la reserva. Con 2000 casos, mira cuántos fraudes quedaron en `cal`. Si su corte es infinito, la etiqueta fraude entra en todos los conjuntos.

### celda: bloque-4-explica

<details><summary>Explicación</summary>

La cobertura entre los fraudes **puede ser mucho menor**. La garantía marginal promedia entre todas las clases. Una clase rara pesa poco en ese promedio, aunque falle casi siempre.

Conformal por clase calcula el corte usando solo los puntajes de la clase correspondiente. Bajo intercambiabilidad dentro de cada clase, condicionada en el modelo congelado, la garantía se aplica por clase. Sigue promediando sobre las posibles calibraciones: tampoco garantiza el resultado de una reserva concreta.

Con $\delta=0.1$ necesitas al menos 9 casos de una clase en calibración para obtener un corte finito. Con menos, la posición corregida rebasa los puntajes disponibles. El procedimiento usa un corte infinito e incluye siempre esa etiqueta.

Así, la cobertura del fraude puede ser completa aunque el procedimiento distinga poco. Incluir fraude en todos los mensajes hace crecer los conjuntos. No significa que todas las demás etiquetas entren siempre: cada una tiene su propio corte.

</details>

### celda: taller-intro

## Taller · Cambia una decisión

Edita una línea de la celda visible y vuelve a correr. Antes, escribe qué esperas que cambie: calibración, cobertura o tamaño de los conjuntos.

- Cambia la proporción de fraude y compara el diagnóstico.
- Contrasta `pesos=(None,)` con `pesos=("balanceado",)`; estas son las opciones que recibe el taller.
- Prueba `mensajes3` con `separar="estratificado"` y `por_clase=True`.
- Repite el proceso con `separar="azar"` para observar también la versión marginal.

Con separación estratificada se fijan los conteos por clase; la reserva conformal no permite invocar aquí la garantía marginal de una separación al azar.
La versión por clase conserva el supuesto pertinente dentro de cada clase; la reserva se aparta antes de ajustar o elegir el modelo.

Describe un cambio que mejore cobertura y otro que reduzca el tamaño medio. Si entran en tensión, explica cuál priorizarías y por qué.

### celda: galeria-intro

## Galería · Compara las curvas

En cada caso, pregunta si las probabilidades anunciadas coinciden con las frecuencias observadas. Revisa si los pesos desplazan la curva y si la recalibración mejora el diagnóstico en datos distintos.

En el caso 22, **¿el techo de aciertos también se ve en la curva de confiabilidad?** No tiene por qué aparecer como descalibración. Un modelo puede anunciar probabilidades confiables y aun así equivocarse al convertirlas en una sola etiqueta.

### celda: ejercicio-cinco-puntajes

## Ejercicio · Ordena cinco puntajes

Tienes cinco puntajes de no conformidad en la reserva. El modelo ya está congelado.

Los puntajes de calibración son 0.1, 0.2, 0.4, 0.6 y 0.8.

Para un mensaje nuevo, las probabilidades de las etiquetas son:

$\widehat p=(0.45,0.35,0.20)$.

1. Ordena los puntajes y localiza la posición corregida para $\delta=1/3$.
2. Encuentra el corte y compara con él el puntaje de cada etiqueta del mensaje nuevo.
3. Repite con $\delta=1/6$. Explica por qué el conjunto no puede encogerse.

Pista: ¿la posición se calcula con el tamaño de calibración o con ese tamaño más uno? ¿Qué haces si un puntaje empata con el corte?

### celda: ejercicio-cinco-puntajes-respuesta

<details><summary>Respuesta y comprobación</summary>

La corrección reserva un lugar para el caso nuevo. Multiplica el tamaño de calibración más uno por la cobertura pedida. Redondea hacia arriba para obtener la posición en la lista ordenada.

Con $\delta=1/3$, la cuenta es $(5+1)(1-1/3)=4$. Tomas el cuarto puntaje: $\widehat c=0.6$. El conjunto esperado es $C(x)=\{0\}$.

Con $\delta=1/6$, la cuenta es $(5+1)(1-1/6)=5$. Tomas el quinto puntaje: $\widehat c=0.8$. El conjunto esperado es $C(x)=\{0,1,2\}$.

Los puntajes del mensaje nuevo son $1-0.45=0.55$, $1-0.35=0.65$ y $1-0.20=0.80$. Con $\widehat c=0.6$ solo $0.55\le0.6$, así que entra la clase 0. Con $\widehat c=0.8$ entran las tres; la clase 2, por la igualdad $0.80\le0.8$.

La posición y el corte aumentan al exigir más cobertura.

</details>

### celda: ejercicio-tasa

## Ejercicio · Calcula la tasa de equilibrio

Un cliente típico tiene probabilidad de impago 0.05. El modelo con pesos balanceados anuncia 0.5 para ese cliente. Supón que, si paga, recuperas el capital más intereses; si incumple, pierdes todo el capital. Omite otros costos.

La tasa de equilibrio iguala los intereses esperados con la pérdida esperada. Se calcula como probabilidad de impago dividida entre probabilidad de pago.

Calcula la tasa usando cada probabilidad. Explica qué supuesto falla al usar directamente la salida ponderada.

Pista: ¿los pesos cambiaron el comportamiento del cliente o el objetivo del ajuste?

### celda: ejercicio-tasa-respuesta

<details><summary>Respuesta y comprobación</summary>

Usando la probabilidad de impago del cliente, la tasa es $0.05/(1-0.05)\approx0.053$. La cuenta divide la pérdida esperada por la fracción de clientes que pagan intereses.

Con la probabilidad ponderada, obtienes $0.5/(1-0.5)=1$: una tasa de 100 %. **Ponderar no cambió la probabilidad real de impago.** Cambió el objetivo que ajusta el modelo.

La comprobación consiste en multiplicar cada tasa por su probabilidad de pago: así recuperas la probabilidad de impago usada en cada cuenta. La tasa redondeada del primer cálculo da una igualdad aproximada.

El segundo cálculo es aritméticamente correcto, pero usa una probabilidad que no representa al cliente. Para esta decisión necesitas probabilidades confiables, además de revisar los supuestos económicos del ejemplo.

</details>

### celda: cierre

**Punto de control:** explica por qué `val_a`, `val_b` y `cal` no son intercambiables en sus funciones. Después distingue una curva calibrada, una cobertura global y una cobertura por clase.

Los pesos cambian el objetivo del ajuste; la recalibración se juzga con otros mensajes. Conformal intercambia tamaño de conjuntos por cobertura. La garantía marginal puede dejar descubierta una clase rara, y un corte infinito puede cubrirla sin distinguir casos.

Todo esto supuso que, con el modelo ya congelado, calibración, prueba y uso son intercambiables, y que el entrenamiento no depende de ellos. La clase 5 da maneras de buscar violaciones de ese supuesto, y ninguna demuestra que se cumple.
